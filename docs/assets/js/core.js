/* Logos Zero — lõi: OZReady, đường dẫn gốc, service worker, nút in.
 * Mỗi công cụ gọi window.OZReady(init). init chạy mỗi khi một trang được hiển thị
 * (kể cả khi chuyển trang bằng instant navigation của Material). init phải idempotent. */
(function () {
  "use strict";
  var OZ = (window.OZ = window.OZ || {});
  var handlers = [];
  var pageReady = false;

  // Đường dẫn gốc của site, suy ra từ vị trí của core.js (…/assets/js/core.js).
  var me = document.currentScript && document.currentScript.src;
  OZ.base = me ? me.replace(/assets\/js\/core\.js(\?.*)?$/, "") : "/";

  function safe(fn) {
    try {
      fn(document);
    } catch (e) {
      if (window.console) console.error("[Logos Zero]", e);
    }
  }

  window.OZReady = function (fn) {
    handlers.push(fn);
    if (pageReady) safe(fn);
  };

  function onPage() {
    pageReady = true;
    handlers.forEach(safe);
  }

  OZ.onPage = onPage;

  // Nút "In bài này" cho mọi bài (trừ trang chủ và trang không có h1).
  window.OZReady(function () {
    var article = document.querySelector("article.md-content__inner");
    if (!article || article.querySelector(".oz-print-btn")) return;
    if (document.querySelector(".oz-home")) return;
    var h1 = article.querySelector("h1");
    if (!h1) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "oz-print-btn md-button";
    btn.textContent = "In bài này";
    btn.setAttribute("aria-label", "In bài này");
    btn.addEventListener("click", function () {
      window.print();
    });
    // Đợt 4.10: có dải thông tin (hooks/kb.py) thì nút In nằm cuối dải, gọn, không chiếm màn hình đầu trên điện thoại.
    var strip = article.querySelector(".oz-info");
    if (strip) {
      btn.className = "oz-print-btn oz-print-btn--dai";
      strip.appendChild(btn);
    } else {
      h1.insertAdjacentElement("afterend", btn);
    }
  });

  // Khối "Tóm tắt 5 phút" thu gọn được (đợt 4.10): tiêu đề thành nút có aria-expanded; màn hẹp mặc định thu gọn,
  // màn rộng mặc định mở. Không đổi HTML khi build (chữ của bài giữ nguyên).
  var NARROW = "(max-width: 44.984375em)";
  window.OZReady(function () {
    document.querySelectorAll(".md-typeset .admonition.summary").forEach(function (box, i) {
      var title = box.querySelector(":scope > .admonition-title");
      if (!title || box.dataset.ozGon || title.textContent.trim() !== "Tóm tắt 5 phút") return;
      box.dataset.ozGon = "1";
      var body = document.createElement("div");
      body.className = "oz-tom-tat__than";
      body.id = "oz-tom-tat-" + i;
      while (title.nextSibling) body.appendChild(title.nextSibling);
      box.appendChild(body);
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "oz-tom-tat__nut";
      btn.setAttribute("aria-controls", body.id);
      while (title.firstChild) btn.appendChild(title.firstChild);
      title.appendChild(btn);
      function set(open) {
        btn.setAttribute("aria-expanded", open ? "true" : "false");
        body.hidden = !open;
        box.classList.toggle("oz-tom-tat--gon", !open);
      }
      btn.addEventListener("click", function () {
        set(btn.getAttribute("aria-expanded") !== "true");
      });
      set(!(window.matchMedia && window.matchMedia(NARROW).matches));
    });
  });

  function start() {
    if (window.document$ && typeof window.document$.subscribe === "function") {
      window.document$.subscribe(onPage);
    } else if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", onPage);
    } else {
      onPage();
    }
  }
  start();

  // PWA: đăng ký service worker (chỉ trên https hoặc localhost).
  if ("serviceWorker" in navigator && /^(https:|http:\/\/(localhost|127\.0\.0\.1))/.test(location.href)) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register(OZ.base + "sw.js", { scope: OZ.base }).catch(function () {});
    });
  }
})();
