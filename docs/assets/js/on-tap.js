/* Logos Zero — Ôn tập thông minh: phiên ôn gộp thẻ thuật ngữ + câu hỏi trắc nghiệm.
 * <div class="oz-on-tap"></div>
 * Mỗi câu quiz có một "thẻ" riêng trong progress.cards với khóa "quiz:<qid>:<i>",
 * cùng quy tắc Leitner 5 hộp như flashcards.js. Không thêm section mới vào state:
 * chỉ dùng cards (merge được qua merge.js) + skills/days qua applyAnswer.
 * Mẫu UMD của repo: hàm thuần xuất qua module.exports; trình duyệt dùng OZReady(initAll). */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.onTap = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* Cùng INTERVAL với flashcards.js (giữ đồng bộ bằng tay; xem test). */
  var INTERVAL = { 1: 1, 2: 2, 3: 4, 4: 8, 5: 16 }; // số ngày tới lần ôn sau, theo hộp

  function addDays(date, n) {
    var d = new Date(date + "T12:00:00Z");
    d.setUTCDate(d.getUTCDate() + n);
    return d.toISOString().slice(0, 10);
  }

  /* Khóa thẻ của câu hỏi số i trong quiz qid. */
  function quizKey(qid, qindex) {
    return "quiz:" + qid + ":" + qindex;
  }

  /* Hàm thuần: cập nhật một thẻ sau khi ôn (giống hệt flashcards.review). */
  function reviewCard(card, remembered, today) {
    var box = card && card.box ? card.box : 0;
    var nb = remembered ? Math.min(5, Math.max(1, box + 1)) : 1;
    return { box: nb, due: addDays(today, INTERVAL[nb]), intro: (card && card.intro) || today, last: today };
  }

  /* Hàm thuần: id thuật ngữ đến hạn + thuật ngữ mới (giới hạn), cùng thứ tự flashcards.session. */
  function dueTermIds(terms, cards, today, opts) {
    opts = opts || {};
    var newLimit = opts.termNew === undefined ? 5 : opts.termNew;
    var max = opts.termMax || 15;
    var due = [];
    var fresh = [];
    var introducedToday = 0;
    terms.forEach(function (t) {
      var c = cards[t.id];
      if (!c) fresh.push(t.id);
      else {
        if (c.intro === today) introducedToday++;
        if (c.due <= today) due.push(t.id);
      }
    });
    due.sort(function (a, b) {
      return cards[a].box - cards[b].box || (cards[a].due < cards[b].due ? -1 : cards[a].due > cards[b].due ? 1 : 0);
    });
    var out = due.slice(0, max);
    var room = Math.max(0, Math.min(newLimit - introducedToday, max - out.length));
    return out.concat(fresh.slice(0, room));
  }

  /* Chuẩn hóa key bài đọc: "/cau-hoi/x/" (URL, từ loader) và "cau-hoi/x.md" (bank)
   * đều về "cau-hoi/x" để so khớp. */
  function canonArticleKey(k) {
    return String(k || "")
      .replace(/^\/+|\/+$/g, "")
      .replace(/\.md$/, "")
      .replace(/(^|\/)index$/, "");
  }

  /* Hàm thuần: câu hỏi đến hạn + câu mới (ưu tiên bài đã đọc), giới hạn số lượng. */
  function dueQuizItems(items, cards, today, opts) {
    opts = opts || {};
    var qMax = opts.qMax || 15;
    var qNew = opts.qNew === undefined ? 5 : opts.qNew;
    var read = opts.read || {};
    var readCanon = {};
    Object.keys(read).forEach(function (k) {
      readCanon[canonArticleKey(k)] = true;
    });
    var due = [];
    var fresh = [];
    var introducedToday = 0;
    items.forEach(function (it, idx) {
      var c = cards[quizKey(it.qid, it.qindex)];
      if (!c) fresh.push(idx);
      else {
        if (c.intro === today) introducedToday++;
        if (c.due <= today) due.push(idx);
      }
    });
    function cardOf(idx) {
      return cards[quizKey(items[idx].qid, items[idx].qindex)];
    }
    due.sort(function (a, b) {
      var ca = cardOf(a),
        cb = cardOf(b);
      return ca.box - cb.box || (ca.due < cb.due ? -1 : ca.due > cb.due ? 1 : 0);
    });
    fresh.sort(function (a, b) {
      var ra = readCanon[canonArticleKey(items[a].article)] ? 0 : 1;
      var rb = readCanon[canonArticleKey(items[b].article)] ? 0 : 1;
      return ra - rb || a - b;
    });
    var out = due.slice(0, qMax);
    var room = Math.max(0, Math.min(qNew - introducedToday, qMax - out.length));
    return out.concat(fresh.slice(0, room)).map(function (idx) {
      return items[idx];
    });
  }

  /* Hàm thuần: phiên ôn gộp. Trả về {terms: [id], questions: [item]}.
   * opts.max giới hạn tổng (chia đôi cho hai loại); có thể ghi đè bằng
   * opts.termMax / opts.qMax. opts.read: map bài đã đọc (ưu tiên câu mới). */
  function buildSession(terms, items, cards, today, opts) {
    opts = opts || {};
    var max = opts.max || 30;
    return {
      terms: dueTermIds(terms, cards, today, {
        termMax: opts.termMax || Math.ceil(max / 2),
        termNew: opts.termNew,
      }),
      questions: dueQuizItems(items, cards, today, {
        qMax: opts.qMax || Math.floor(max / 2),
        qNew: opts.qNew,
        read: opts.read,
      }),
    };
  }

  /* Fisher–Yates (giống util.shuffle) để trộn thẻ + câu hỏi trong một phiên. */
  function shuffle(arr, rand) {
    rand = rand || Math.random;
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rand() * (i + 1));
      var t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  /* Hàm thuần: trộn danh sách thẻ và câu hỏi thành một hàng đợi chung. */
  function mixSession(termIds, questionItems, rand) {
    var q = termIds.map(function (id) {
      return { kind: "term", id: id };
    });
    questionItems.forEach(function (it) {
      q.push({ kind: "question", item: it });
    });
    return shuffle(q, rand);
  }

  /* Hàm thuần: số mục ĐẾN HẠN hôm nay (không tính mục mới) — cho màn hình chờ và ke-hoach. */
  function dueCounts(terms, items, cards, today) {
    var dt = 0,
      dq = 0;
    terms.forEach(function (t) {
      var c = cards[t.id];
      if (c && c.due <= today) dt++;
    });
    items.forEach(function (it) {
      var c = cards[quizKey(it.qid, it.qindex)];
      if (c && c.due <= today) dq++;
    });
    return { terms: dt, questions: dq };
  }

  /* Hàm thuần: số ngày liên tiếp có hoạt động, tính đến hôm nay (hoặc hôm qua). */
  function streakDays(daysMap, todayStr) {
    var set = {};
    Object.keys(daysMap || {}).forEach(function (d) {
      if (d <= todayStr) set[d] = true;
    });
    var cur = set[todayStr] ? todayStr : addDays(todayStr, -1);
    var n = 0;
    while (set[cur]) {
      n++;
      cur = addDays(cur, -1);
    }
    return n;
  }

  function init(box) {
    var OZ = window.OZ;
    var U = OZ.util;
    var P = OZ.progress;
    if (!U.claim(box)) return;
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Ôn tập thông minh");
    box.appendChild(U.el("p", { class: "oz-muted", text: "Đang tải dữ liệu ôn tập…" }));
    var say = U.live(box);
    var maxTotal = parseInt(box.dataset.max, 10) || 30;
    var termNew = parseInt(box.dataset.termNew, 10);
    if (isNaN(termNew)) termNew = 5;
    var qNew = parseInt(box.dataset.qNew, 10);
    if (isNaN(qNew)) qNew = 5;
    var today = P ? P.today() : new Date().toISOString().slice(0, 10);
    var byTermId = {};
    var queue = [];
    var isPractice = false;
    var done = 0,
      correct = 0;

    Promise.all([U.fetchJSON("assets/data/terms.json"), U.fetchJSON("assets/data/quiz-bank.json")])
      .then(function (res) {
        var terms = res[0].terms || [];
        var bank = res[1].items || [];
        terms.forEach(function (t) {
          byTermId[t.id] = t;
        });
        landing(terms, bank);
      })
      .catch(function (e) {
        box.textContent = "";
        box.appendChild(U.el("p", { class: "oz-error", text: e.message }));
      });

    function cards() {
      return P ? P.load().cards : {};
    }

    function landing(terms, bank) {
      box.textContent = "";
      var dc = dueCounts(terms, bank, cards(), today);
      var total = dc.terms + dc.questions;
      box.appendChild(
        U.el("p", {
          class: "oz-muted",
          text:
            total > 0
              ? "Hôm nay có " + dc.terms + " thuật ngữ và " + dc.questions + " câu hỏi đến hạn ôn lại."
              : "Hôm nay không có mục nào đến hạn. Bạn vẫn có thể ôn thêm.",
        })
      );
      var st = P ? streakDays(P.load().days, today) : 0;
      if (st > 0) box.appendChild(U.el("p", { class: "oz-muted", text: "Chuỗi ngày học: " + st + " ngày." }));
      box.appendChild(
        U.el("div", { class: "oz-actions" }, [
          U.el("button", {
            type: "button",
            class: "md-button md-button--primary",
            text: "Bắt đầu ôn tập",
            onclick: function () {
              start(terms, bank, false);
            },
          }),
          U.el("button", {
            type: "button",
            class: "md-button",
            text: "Ôn thêm 10 câu hỏi ngẫu nhiên",
            onclick: function () {
              start(terms, bank, true);
            },
          }),
        ])
      );
    }

    function start(terms, bank, practice) {
      done = 0;
      correct = 0;
      isPractice = !!practice;
      if (practice) {
        var qs = shuffle(bank, Math.random)
          .slice(0, 10)
          .map(function (it) {
            return { kind: "question", item: it };
          });
        queue = qs;
      } else {
        var ses = buildSession(terms, bank, cards(), today, {
          max: maxTotal,
          termNew: termNew,
          qNew: qNew,
          read: P ? P.load().read : {},
        });
        queue = mixSession(ses.terms, ses.questions, Math.random);
      }
      next();
      say(practice ? "Bắt đầu ôn thêm." : "Bắt đầu phiên ôn tập.");
    }

    function recordTerm(id, ok) {
      if (P && !isPractice)
        P.update(function (s) {
          var now = P.today();
          s.cards[id] = reviewCard(s.cards[id], ok, now);
          return P.applyAnswer(s, "terms", ok, now);
        });
    }

    function recordQuestion(item, ok) {
      if (isPractice) return;
      var key = quizKey(item.qid, item.qindex);
      if (P)
        P.update(function (s) {
          var now = P.today();
          s.cards[key] = reviewCard(s.cards[key], ok, now);
          return P.applyAnswer(s, item.skill, ok, now, key);
        });
    }

    function head() {
      box.textContent = "";
      box.appendChild(
        U.el("p", { class: "oz-muted", text: "Còn " + queue.length + " mục" + (isPractice ? " (ôn thêm, không tính lịch)" : "") })
      );
    }

    function next() {
      if (!queue.length) {
        finish();
        return;
      }
      var cur = queue[0];
      if (cur.kind === "term") nextTerm(cur.id);
      else nextQuestion(cur.item);
    }

    function nextTerm(id) {
      var t = byTermId[id];
      var c = cards()[id];
      head();
      var front = U.el("div", { class: "oz-card__front" }, [
        U.el("p", { class: "oz-card__term", text: t.vi }),
        t.en ? U.el("p", { class: "oz-card__en", text: t.en }) : null,
        U.el("p", { class: "oz-muted", text: c ? "Hộp " + c.box : "Thẻ mới" }),
      ]);
      var back = U.el("div", { class: "oz-card__back", hidden: true }, [
        U.el("p", { class: "oz-card__def", text: t.def }),
        t.example ? U.el("p", { class: "oz-card__ex" }, [U.el("em", { text: "Ví dụ: " }), t.example]) : null,
      ]);
      box.appendChild(U.el("div", { class: "oz-card", "aria-live": "polite" }, [front, back]));
      var flip = U.el("button", { type: "button", class: "md-button md-button--primary", text: "Lật thẻ" });
      var forgot = U.el("button", { type: "button", class: "md-button", text: "Chưa nhớ", hidden: true });
      var knew = U.el("button", { type: "button", class: "md-button md-button--primary", text: "Nhớ rồi", hidden: true });
      flip.addEventListener("click", function () {
        back.hidden = false;
        flip.hidden = true;
        forgot.hidden = false;
        knew.hidden = false;
        knew.focus();
        say(t.def);
      });
      function grade(ok) {
        recordTerm(id, ok);
        done++;
        if (ok) correct++;
        queue.shift();
        next();
      }
      forgot.addEventListener("click", function () {
        grade(false);
      });
      knew.addEventListener("click", function () {
        grade(true);
      });
      box.appendChild(U.el("div", { class: "oz-actions" }, [flip, forgot, knew]));
    }

    function nextQuestion(item) {
      head();
      box.appendChild(U.el("p", { class: "oz-card__term", text: item.q }));
      var fb = U.el("div", { class: "oz-quiz__fb", hidden: true });
      var answered = false;
      item.options.forEach(function (opt, j) {
        var btn = U.el("button", {
          type: "button",
          class: "md-button oz-on-tap__opt",
          text: opt,
          onclick: function () {
            if (answered) return;
            answered = true;
            var ok = j === item.answer;
            fb.hidden = false;
            fb.className = "oz-quiz__fb " + (ok ? "is-correct" : "is-wrong");
            fb.textContent = "";
            fb.appendChild(U.el("strong", { text: ok ? "Đúng. " : "Chưa đúng. Đáp án: " + item.options[item.answer] + ". " }));
            fb.appendChild(document.createTextNode(item.explain));
            recordQuestion(item, ok);
            done++;
            if (ok) correct++;
            say(fb.textContent);
            var nextBtn = U.el("button", {
              type: "button",
              class: "md-button md-button--primary",
              text: "Tiếp tục",
              onclick: function () {
                queue.shift();
                next();
              },
            });
            box.appendChild(U.el("div", { class: "oz-actions" }, [nextBtn]));
            nextBtn.focus();
          },
        });
        box.appendChild(U.el("div", { class: "oz-on-tap__opts" }, [btn]));
      });
      box.appendChild(fb);
    }

    function finish() {
      box.textContent = "";
      var pct = done ? Math.round((correct / done) * 100) : 0;
      box.appendChild(
        U.el("p", { text: "Xong phiên ôn: đúng " + correct + "/" + done + " mục (" + pct + "%)." })
      );
      var st = P ? streakDays(P.load().days, today) : 0;
      if (st > 0) box.appendChild(U.el("p", { class: "oz-muted", text: "Chuỗi ngày học: " + st + " ngày. Hẹn gặp lại ngày mai!" }));
      say("Xong phiên ôn tập. Đúng " + correct + " trên " + done + " mục.");
    }
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-on-tap"), init);
  }

  return {
    INTERVAL: INTERVAL,
    addDays: addDays,
    quizKey: quizKey,
    canonArticleKey: canonArticleKey,
    reviewCard: reviewCard,
    dueTermIds: dueTermIds,
    dueQuizItems: dueQuizItems,
    buildSession: buildSession,
    mixSession: mixSession,
    dueCounts: dueCounts,
    streakDays: streakDays,
    initAll: initAll,
  };
});
