/* Logos Zero — công cụ "Nhận ra ngụy biện".
 * <div class="oz-fallacy-trainer" data-count="10" data-level="all"></div>
 * Dữ liệu: assets/data/fallacies.json */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.fallacy = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var SKILL = "fallacy";
  var CONTEXTS = {
    "gia-dinh": "Gia đình",
    "cong-so": "Công sở",
    "quang-cao": "Quảng cáo",
    "bao-chi": "Báo chí",
    "mang-xa-hoi": "Mạng xã hội",
    "truong-hoc": "Trường học",
    "chinh-sach": "Chính sách",
    "suc-khoe": "Sức khỏe",
  };

  /* Trọng số chọn câu: câu chưa gặp và câu hay sai được ưu tiên. */
  function weight(stat) {
    if (!stat || !stat.n) return 3;
    var err = 1 - stat.c / stat.n;
    return 0.5 + 2.5 * err;
  }

  /* Hàm thuần: chọn `count` câu không lặp, theo cấp độ, có trọng số. */
  function pickQuestions(bank, opts) {
    opts = opts || {};
    var rand = opts.rng || Math.random;
    var items = opts.items || {};
    var level = opts.level === undefined ? "all" : String(opts.level);
    var pool = bank.filter(function (q) {
      return level === "all" || String(q.level) === level;
    });
    var count = Math.min(opts.count || 10, pool.length);
    var out = [];
    var ws = pool.map(function (q) {
      return weight(items["fallacy:" + q.id]);
    });
    while (out.length < count) {
      var total = ws.reduce(function (a, b) {
        return a + b;
      }, 0);
      var r = rand() * total;
      var k = 0;
      while (k < ws.length - 1 && r >= ws[k]) {
        r -= ws[k];
        k++;
      }
      out.push(pool[k]);
      pool.splice(k, 1);
      ws.splice(k, 1);
    }
    return out;
  }

  function validateBank(data) {
    var errors = [];
    var ids = {};
    (data.types || []).forEach(function (t) {
      ids[t.id] = t;
    });
    var seen = {};
    (data.questions || []).forEach(function (q) {
      if (seen[q.id]) errors.push(q.id + ": id trùng");
      seen[q.id] = true;
      if (!ids[q.answer]) errors.push(q.id + ": answer không hợp lệ " + q.answer);
      if (!Array.isArray(q.options) || q.options.length !== 4) errors.push(q.id + ": cần đúng 4 lựa chọn");
      else {
        if (q.options.indexOf(q.answer) === -1) errors.push(q.id + ": answer không nằm trong options");
        q.options.forEach(function (o) {
          if (!ids[o]) errors.push(q.id + ": option không hợp lệ " + o);
        });
        if (new Set(q.options).size !== 4) errors.push(q.id + ": option trùng");
      }
      if (q.highlight && q.passage.indexOf(q.highlight) === -1) errors.push(q.id + ": highlight không có trong passage");
      if (!q.explanation) errors.push(q.id + ": thiếu giải thích");
      if ([1, 2, 3].indexOf(q.level) === -1) errors.push(q.id + ": level không hợp lệ");
    });
    return errors;
  }

  function init(box) {
    var OZ = window.OZ;
    var U = OZ.util;
    if (!U.claim(box)) return;
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Luyện nhận ra ngụy biện");
    box.appendChild(U.el("p", { class: "oz-muted", text: "Đang tải câu hỏi…" }));
    U.fetchJSON("assets/data/fallacies.json")
      .then(function (data) {
        build(box, data);
      })
      .catch(function (e) {
        box.textContent = "";
        box.appendChild(U.el("p", { class: "oz-error", text: e.message }));
      });
  }

  function build(box, data) {
    var OZ = window.OZ;
    var U = OZ.util;
    var P = OZ.progress;
    var types = {};
    data.types.forEach(function (t) {
      types[t.id] = t;
    });
    var count = parseInt(box.dataset.count, 10) || 10;
    var level = box.dataset.level || "all";
    var say = U.live(box);
    var stage = U.el("div", { class: "oz-ft__stage" });
    box.textContent = "";

    // Chọn cấp độ
    var levels = [
      ["all", "Trộn"],
      ["1", "Dễ"],
      ["2", "Vừa"],
      ["3", "Khó"],
    ];
    var group = U.el("div", { class: "oz-segmented", role: "radiogroup", "aria-label": "Cấp độ" });
    levels.forEach(function (lv) {
      var b = U.el("button", {
        type: "button",
        role: "radio",
        "aria-checked": String(lv[0] === level),
        "data-level": lv[0],
        text: lv[1],
        onclick: function () {
          level = lv[0];
          Array.prototype.forEach.call(group.children, function (c) {
            c.setAttribute("aria-checked", String(c.dataset.level === level));
          });
          startRound();
        },
      });
      group.appendChild(b);
    });
    box.appendChild(U.el("div", { class: "oz-ft__head" }, [U.el("span", { class: "oz-muted", text: "Cấp độ: " }), group]));
    box.appendChild(stage);

    var round, idx, score, mistakes;

    function startRound() {
      var items = P ? P.load().items : {};
      round = pickQuestions(data.questions, { count: count, level: level, items: items });
      idx = 0;
      score = 0;
      mistakes = {};
      show();
    }

    function lessonLink(id) {
      if (id === "none") return null;
      return U.el("a", { href: OZ.base + "cong-cu/nguy-bien/#" + id, text: "Đọc thêm về " + types[id].vi.toLowerCase() + " →" });
    }

    function show() {
      stage.textContent = "";
      if (idx >= round.length) return finish();
      var q = round[idx];
      var passage = U.el("blockquote", { class: "oz-ft__passage" }, [q.passage]);
      var meta = U.el("p", { class: "oz-ft__meta" }, [
        U.el("span", { text: "Câu " + (idx + 1) + "/" + round.length }),
        U.el("span", { class: "oz-tag", text: CONTEXTS[q.context] || q.context }),
        U.el("span", { class: "oz-tag", text: ["", "Dễ", "Vừa", "Khó"][q.level] }),
      ]);
      var prompt = U.el("p", { class: "oz-ft__prompt", id: "oz-ft-prompt-" + idx, text: "Đoạn trên mắc lỗi lập luận nào, hay không mắc lỗi nào?" });
      var opts = U.el("div", { class: "oz-options", role: "group", "aria-labelledby": prompt.id });
      var fb = U.el("div", { class: "oz-ft__fb", hidden: true, tabindex: "-1" });
      U.shuffle(q.options).forEach(function (o) {
        var t = types[o];
        opts.appendChild(
          U.el(
            "button",
            {
              type: "button",
              class: "oz-option",
              "data-id": o,
              onclick: function () {
                answer(q, o, opts, fb, passage);
              },
            },
            [U.el("span", { class: "oz-option__vi", text: t.vi }), t.en && o !== "none" ? U.el("span", { class: "oz-option__en", text: t.en }) : null]
          )
        );
      });
      stage.appendChild(meta);
      stage.appendChild(passage);
      stage.appendChild(prompt);
      stage.appendChild(opts);
      stage.appendChild(fb);
    }

    function answer(q, chosen, opts, fb, passage) {
      var ok = chosen === q.answer;
      if (ok) score++;
      else mistakes[q.answer] = (mistakes[q.answer] || 0) + 1;
      Array.prototype.forEach.call(opts.children, function (b) {
        b.disabled = true;
        if (b.dataset.id === q.answer) b.classList.add("is-correct");
        else if (b.dataset.id === chosen) b.classList.add("is-wrong");
      });
      passage.textContent = "";
      passage.appendChild(U.highlight(q.passage, q.highlight));
      fb.hidden = false;
      fb.className = "oz-ft__fb " + (ok ? "is-correct" : "is-wrong");
      var t = types[q.answer];
      fb.appendChild(U.el("p", null, [U.el("strong", { text: (ok ? "Chính xác: " : "Chưa đúng. Đáp án: ") + t.vi + ". " }), q.explanation]));
      if (!ok && q.why_not && q.why_not[chosen])
        fb.appendChild(
          U.el("p", null, [
            U.el("strong", { text: chosen === "none" ? "Vì sao đây vẫn là một lỗi lập luận? " : "Vì sao không phải " + types[chosen].vi.toLowerCase() + "? " }),
            q.why_not[chosen],
          ])
        );
      var link = lessonLink(q.answer);
      var next = U.el("button", {
        type: "button",
        class: "md-button md-button--primary",
        text: idx + 1 < round.length ? "Câu tiếp" : "Xem kết quả",
        onclick: function () {
          idx++;
          show();
          var first = stage.querySelector(".oz-option");
          if (first) first.focus();
          else {
            var h = stage.querySelector("h3");
            if (h) h.focus();
          }
        },
      });
      fb.appendChild(U.el("div", { class: "oz-actions" }, [next, link]));
      say((ok ? "Chính xác. " : "Chưa đúng. Đáp án là " + t.vi + ". ") + q.explanation);
      if (P) P.record(SKILL, ok, "fallacy:" + q.id);
      next.focus();
    }

    function finish() {
      var list = Object.keys(mistakes).map(function (id) {
        var a = lessonLink(id);
        return U.el("li", null, [types[id].vi + " (" + mistakes[id] + ") ", a]);
      });
      stage.appendChild(U.el("h3", { tabindex: "-1", text: "Bạn nhận ra đúng " + score + "/" + round.length + " đoạn" }));
      if (list.length) {
        stage.appendChild(U.el("p", { text: "Những loại nên xem lại:" }));
        stage.appendChild(U.el("ul", null, list));
      } else stage.appendChild(U.el("p", { text: "Không sai câu nào. Thử cấp độ khó hơn xem sao." }));
      stage.appendChild(
        U.el("div", { class: "oz-actions" }, [
          U.el("button", { type: "button", class: "md-button md-button--primary", text: "Luyện lượt mới", onclick: startRound }),
        ])
      );
      say("Kết thúc lượt: đúng " + score + " trên " + round.length);
    }

    startRound();
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-fallacy-trainer"), init);
  }

  return { pickQuestions: pickQuestions, validateBank: validateBank, weight: weight, initAll: initAll };
});
