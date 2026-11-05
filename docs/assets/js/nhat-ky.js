/* Logos — Nhật ký: ghi chép suy nghĩ mỗi ngày, chỉ lưu trên trình duyệt này.
 * <div class="oz-nhat-ky"></div>. Dữ liệu gộp được qua trang Dữ liệu
 * (merge.js: mergeJournal — phía dài hơn thắng).
 * Mẫu UMD của repo: hàm thuần xuất qua module.exports; trình duyệt dùng OZReady(initAll). */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.nhatky = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var MAX_LEN = 2000;

  /* "2026-10-13" → "13/10/2026". */
  function fmtDate(d) {
    var p = String(d || "").split("-");
    if (p.length !== 3) return String(d || "");
    return p[2] + "/" + p[1] + "/" + p[0];
  }

  function nowHM(d) {
    d = d || new Date();
    function pad(n) {
      return (n < 10 ? "0" : "") + n;
    }
    return pad(d.getHours()) + ":" + pad(d.getMinutes());
  }

  /* Hàm thuần: tóm tắt hoạt động tự động theo ngày từ state.
   * Trả về {date: ["Đã trả lời 12 câu (đúng 9)", "Đã mở 2 bài"]}. */
  function autoLines(state) {
    var s = state || {};
    var per = {};
    var days = s.days || {};
    Object.keys(days).forEach(function (d) {
      var e = days[d] || {};
      var n = e.n || 0;
      var c = e.c || 0;
      (per[d] = per[d] || []).push("Đã trả lời " + n + " câu (đúng " + c + ")");
    });
    var readCount = {};
    var read = s.read || {};
    Object.keys(read).forEach(function (p) {
      var d = read[p];
      if (d) readCount[d] = (readCount[d] || 0) + 1;
    });
    Object.keys(readCount).forEach(function (d) {
      (per[d] = per[d] || []).push("Đã mở " + readCount[d] + " bài");
    });
    return per;
  }

  /* Hàm thuần: gộp ghi chép tay + dòng tự động theo ngày, ngày mới nhất trước.
   * Mỗi phần tử: {date, entries: [{t, text}], auto: [chuỗi]}. */
  function groupEntries(state) {
    var s = state || {};
    var journal = s.journal || {};
    var auto = autoLines(s);
    var seen = {};
    Object.keys(journal).forEach(function (d) {
      seen[d] = true;
    });
    Object.keys(auto).forEach(function (d) {
      seen[d] = true;
    });
    return Object.keys(seen)
      .sort()
      .reverse()
      .map(function (d) {
        return {
          date: d,
          entries: Array.isArray(journal[d]) ? journal[d].slice() : [],
          auto: auto[d] || [],
        };
      });
  }

  function entryEl(U, P, box, date, index, e) {
    var wrap = U.el("article", { class: "oz-journal-entry" });
    wrap.appendChild(U.el("div", { class: "oz-journal-time oz-muted", text: e.t || "" }));
    /* textContent qua U.el: HTML trong ghi chép của người dùng không bao giờ được render. */
    wrap.appendChild(U.el("p", { class: "oz-journal-text", text: e.text || "" }));
    wrap.appendChild(
      U.el("button", {
        type: "button",
        class: "md-button oz-danger oz-journal-del",
        text: "Xóa",
        "aria-label": "Xóa ghi chép lúc " + (e.t || ""),
        onclick: function () {
          if (!window.confirm("Xóa ghi chép này? Không thể hoàn tác.")) return;
          P.update(function (s) {
            var ns = JSON.parse(JSON.stringify(P.migrate(s)));
            var arr = ns.journal[date];
            if (Array.isArray(arr)) arr.splice(index, 1);
            return ns;
          });
          render(box);
          U.live(box)("Đã xóa ghi chép.");
        },
      })
    );
    return wrap;
  }

  function render(box) {
    var OZ = window.OZ;
    var U = OZ.util;
    var P = OZ.progress;
    box.textContent = "";
    var say = U.live(box);

    var areaId = "oz-journal-text";
    var area = U.el("textarea", {
      id: areaId,
      class: "oz-textarea",
      rows: "4",
      maxlength: String(MAX_LEN),
      placeholder: "Viết vài dòng suy nghĩ, câu hỏi, hay điều vừa đọc được…",
    });
    var saveBtn = U.el("button", {
      type: "button",
      class: "md-button md-button--primary",
      text: "Lưu",
      onclick: function () {
        var text = area.value.trim();
        if (!text) {
          say("Hãy viết vài chữ trước khi lưu.");
          area.focus();
          return;
        }
        P.update(function (s) {
          return P.addJournalEntry(s, P.today(), nowHM(), text);
        });
        area.value = "";
        render(box);
        U.live(box)("Đã lưu vào nhật ký.");
      },
    });
    box.appendChild(
      U.el("div", { class: "oz-journal-form" }, [
        U.el("label", { for: areaId, class: "oz-journal-label", text: "Hôm nay bạn nghĩ gì?" }),
        area,
        U.el("div", { class: "oz-actions" }, [saveBtn]),
      ])
    );

    var groups = groupEntries(P.migrate(P.load()));
    if (!groups.length) {
      box.appendChild(
        U.el("p", { class: "oz-muted", text: "Chưa có ghi chép nào. Những dòng bạn viết sẽ hiện ở đây, mới nhất trước." })
      );
      return;
    }
    groups.forEach(function (g) {
      var grp = U.el("section", { class: "oz-journal-day" });
      grp.appendChild(U.el("h2", { class: "oz-journal-date", text: fmtDate(g.date) }));
      g.auto.forEach(function (line) {
        grp.appendChild(U.el("p", { class: "oz-muted", text: "• " + line }));
      });
      g.entries.forEach(function (e, i) {
        grp.appendChild(entryEl(U, P, box, g.date, i, e));
      });
      box.appendChild(grp);
    });
  }

  function initAll(doc) {
    var U = window.OZ.util;
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-nhat-ky"), function (box) {
      if (!U.claim(box)) return;
      render(box);
    });
  }

  return { groupEntries: groupEntries, autoLines: autoLines, fmtDate: fmtDate, initAll: initAll };
});
