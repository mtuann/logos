/* Logos — bộ tải theo nhu cầu.
 * Quét trang, tìm phần tử công cụ và chỉ nạp script cần thiết, đúng thứ tự phụ thuộc
 * (tải song song, chạy tuần tự nhờ async = false). Trang chỉ có chữ không nạp gì thêm. */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.loader = api;
    api.start();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // Bộ chọn → danh sách script (theo thứ tự phụ thuộc). Thêm công cụ mới: thêm một dòng.
  var TOOLS = [
    { sel: ".oz-quiz", js: ["util.js", "quiz.js"] },
    { sel: ".oz-fallacy-trainer", js: ["util.js", "fallacy.js"] },
    { sel: ".oz-logic", js: ["util.js", "logic-menh-de.js"] },
    { sel: ".oz-thi-nghiem", js: ["util.js", "thi-nghiem.js"] },
    { sel: ".oz-so-do", js: ["util.js", "so-do-lap-luan.js"] },
    { sel: ".oz-flashcards", js: ["util.js", "flashcards.js"] },
    { sel: ".oz-on-tap", js: ["util.js", "on-tap.js"] },
    { sel: ".oz-daily", js: ["util.js", "daily.js"] },
    { sel: ".oz-mydata, .oz-progress-summary", js: ["util.js", "merge.js", "mydata.js"] },
    { sel: ".oz-ke-hoach", js: ["util.js", "on-tap.js", "ke-hoach.js"] },
    { sel: ".oz-bieu-do", js: ["util.js", "bieu-do.js"] },
    { sel: ".oz-nhat-ky", js: ["util.js", "nhat-ky.js"] },
    { sel: ".oz-steelman", js: ["util.js", "steelman.js"] },
    { sel: '.md-content a[href*="triet-gia/"], .md-content a[href*="tu-dien/#"]', js: ["the-di-chuot.js"] },
  ];

  /* Hàm thuần: cho danh sách bộ chọn có mặt, trả về danh sách script cần nạp, không trùng. */
  function plan(present, already) {
    var out = [];
    var seen = {};
    (already || []).forEach(function (f) {
      seen[f] = true;
    });
    TOOLS.forEach(function (t) {
      if (present.indexOf(t.sel) === -1) return;
      t.js.forEach(function (f) {
        if (!seen[f]) {
          seen[f] = true;
          out.push(f);
        }
      });
    });
    return out;
  }

  var loaded = [];

  function scan(doc) {
    var present = TOOLS.filter(function (t) {
      return doc.querySelector(t.sel);
    }).map(function (t) {
      return t.sel;
    });
    var files = plan(present, loaded);
    var base = (window.OZ && window.OZ.base) || "";
    files.forEach(function (f) {
      loaded.push(f);
      var s = doc.createElement("script");
      s.src = base + "assets/js/" + f;
      s.async = false;
      s.dataset.ozTool = f;
      doc.head.appendChild(s);
    });
    return files;
  }

  function start() {
    if (typeof window.OZReady !== "function") return;
    window.OZReady(function (doc) {
      scan(doc);
      // Ghi nhận trang đã đọc (chỉ các bài có tiêu đề h1, không tính trang chủ).
      var P = window.OZ && window.OZ.progress;
      if (P && doc.querySelector("article h1") && !doc.querySelector(".oz-home")) {
        var path = location.pathname.replace(window.OZ.base.replace(/^https?:\/\/[^/]+/, ""), "/");
        P.update(function (s) {
          return P.markRead(s, path);
        });
      }
    });
  }

  return { TOOLS: TOOLS, plan: plan, scan: scan, start: start, _loaded: loaded };
});
