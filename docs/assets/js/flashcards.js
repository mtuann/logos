/* Logos Zero — thẻ ghi nhớ thuật ngữ, ôn tập ngắt quãng kiểu Leitner (5 hộp).
 * <div class="oz-flashcards" data-new="5" data-max="20"></div>  Dữ liệu: assets/data/terms.json */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.flashcards = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var INTERVAL = { 1: 1, 2: 2, 3: 4, 4: 8, 5: 16 }; // số ngày tới lần ôn sau, theo hộp

  function addDays(date, n) {
    var d = new Date(date + "T12:00:00Z");
    d.setUTCDate(d.getUTCDate() + n);
    return d.toISOString().slice(0, 10);
  }

  /* Hàm thuần: cập nhật một thẻ sau khi ôn. */
  function review(card, remembered, today) {
    var box = card && card.box ? card.box : 0;
    var nb = remembered ? Math.min(5, Math.max(1, box + 1)) : 1;
    return { box: nb, due: addDays(today, INTERVAL[nb]), intro: (card && card.intro) || today, last: today };
  }

  /* Hàm thuần: danh sách id thẻ cần ôn hôm nay (đến hạn trước, rồi thẻ mới). */
  function session(terms, cards, today, opts) {
    opts = opts || {};
    var newLimit = opts.newLimit === undefined ? 5 : opts.newLimit;
    var max = opts.max || 20;
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

  function boxCounts(terms, cards) {
    var c = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    terms.forEach(function (t) {
      c[(cards[t.id] && cards[t.id].box) || 0]++;
    });
    return c;
  }

  function init(box) {
    var OZ = window.OZ;
    var U = OZ.util;
    if (!U.claim(box)) return;
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Thẻ ghi nhớ thuật ngữ");
    box.appendChild(U.el("p", { class: "oz-muted", text: "Đang tải thẻ…" }));
    U.fetchJSON("assets/data/terms.json")
      .then(function (data) {
        build(box, data.terms);
      })
      .catch(function (e) {
        box.textContent = "";
        box.appendChild(U.el("p", { class: "oz-error", text: e.message }));
      });
  }

  function build(box, terms) {
    var OZ = window.OZ;
    var U = OZ.util;
    var P = OZ.progress;
    var byId = {};
    terms.forEach(function (t) {
      byId[t.id] = t;
    });
    var newLimit = parseInt(box.dataset["new"], 10);
    if (isNaN(newLimit)) newLimit = 5;
    var max = parseInt(box.dataset.max, 10) || 20;
    var say = U.live(box);
    var queue = [];
    var practice = false;
    var stats = U.el("p", { class: "oz-fc__stats oz-muted" });
    var stage = U.el("div", { class: "oz-fc__stage" });
    box.textContent = "";
    box.appendChild(stats);
    box.appendChild(stage);

    function cards() {
      return P ? P.load().cards : {};
    }

    function renderStats() {
      var c = boxCounts(terms, cards());
      stats.textContent =
        terms.length + " thuật ngữ · chưa học " + c[0] + " · hộp 1–5: " + [c[1], c[2], c[3], c[4], c[5]].join(" / ");
    }

    function start(isPractice) {
      practice = !!isPractice;
      queue = practice
        ? U.shuffle(terms.map(function (t) { return t.id; })).slice(0, 10)
        : session(terms, cards(), P ? P.today() : new Date().toISOString().slice(0, 10), { newLimit: newLimit, max: max });
      next();
    }

    function next() {
      renderStats();
      stage.textContent = "";
      if (!queue.length) {
        stage.appendChild(U.el("p", { text: practice ? "Xong lượt ôn thêm." : "Hôm nay bạn đã ôn hết thẻ đến hạn." }));
        stage.appendChild(
          U.el("div", { class: "oz-actions" }, [
            U.el("button", { type: "button", class: "md-button", text: "Ôn thêm 10 thẻ ngẫu nhiên", onclick: function () { start(true); } }),
          ])
        );
        return;
      }
      var t = byId[queue[0]];
      var c = cards()[t.id];
      var front = U.el("div", { class: "oz-card__front" }, [
        U.el("p", { class: "oz-card__term", text: t.vi }),
        t.en ? U.el("p", { class: "oz-card__en", text: t.en }) : null,
        U.el("p", { class: "oz-muted", text: c ? "Hộp " + c.box : "Thẻ mới" }),
      ]);
      var back = U.el("div", { class: "oz-card__back", hidden: true }, [
        U.el("p", { class: "oz-card__def", text: t.def }),
        t.example ? U.el("p", { class: "oz-card__ex" }, [U.el("em", { text: "Ví dụ: " }), t.example]) : null,
        t.han ? U.el("p", { class: "oz-muted", text: "Hán: " + t.han }) : null,
        t.alt && t.alt.length ? U.el("p", { class: "oz-muted", text: "Cách dịch khác: " + t.alt.join(", ") }) : null,
      ]);
      var card = U.el("div", { class: "oz-card", "aria-live": "polite" }, [front, back]);
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
        if (P && !practice) {
          P.update(function (s) {
            s.cards[t.id] = review(s.cards[t.id], ok, P.today());
            return P.applyAnswer(s, "terms", ok, P.today());
          });
        }
        queue.shift();
        if (!ok && practice) queue.push(t.id);
        next();
        var b = stage.querySelector("button");
        if (b) b.focus();
      }
      forgot.addEventListener("click", function () { grade(false); });
      knew.addEventListener("click", function () { grade(true); });
      stage.appendChild(U.el("p", { class: "oz-muted", text: "Còn " + queue.length + " thẻ" + (practice ? " (ôn thêm, không tính lịch)" : "") }));
      stage.appendChild(card);
      stage.appendChild(U.el("div", { class: "oz-actions" }, [flip, forgot, knew]));
    }

    start(false);
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-flashcards"), init);
  }

  return { review: review, session: session, boxCounts: boxCounts, addDays: addDays, INTERVAL: INTERVAL, initAll: initAll };
});
