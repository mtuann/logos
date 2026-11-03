/* Logos Zero — "Câu hỏi hôm nay" trên trang chủ.
 * <div class="oz-daily"> chứa một danh sách <li>; mỗi ngày làm nổi bật một mục.
 * Không có JavaScript thì người đọc vẫn thấy cả danh sách. */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.daily = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* Hàm thuần: chỉ số của câu hỏi cho một ngày (YYYY-MM-DD), xoay vòng đều. */
  function pickIndex(date, n) {
    var days = Math.floor(Date.parse(date + "T00:00:00Z") / 86400000);
    return ((days % n) + n) % n;
  }

  function init(box) {
    var U = window.OZ.util;
    if (!U.claim(box)) return;
    var items = box.querySelectorAll("li");
    if (!items.length) return;
    var P = window.OZ.progress;
    var today = P ? P.today() : new Date().toISOString().slice(0, 10);
    var i = pickIndex(today, items.length);
    box.classList.add("is-picked");
    Array.prototype.forEach.call(items, function (li, k) {
      if (k === i) li.classList.add("is-today");
    });
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-daily"), init);
  }

  return { pickIndex: pickIndex, initAll: initAll };
});
