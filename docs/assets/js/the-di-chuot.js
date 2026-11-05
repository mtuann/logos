/* Logos Zero — thẻ di chuột (đợt 4.7): rê chuột, đưa phím Tab tới, hoặc chạm giữ một link tới trang triết gia
 * (…/triet-gia/<id>/) hay mục từ điển (…/them/tu-dien/#<id>) trong bài thì hiện một thẻ nhỏ: tên, năm, một dòng tóm
 * tắt (docs/assets/data/philosophers.json) hoặc định nghĩa (terms.json). Thẻ là role="tooltip", gắn vào link bằng
 * aria-describedby; Esc đóng; rê chuột sang thẻ thì thẻ không tắt (WCAG 1.4.13). Không có trong HTML khi build. */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.theDiChuot = api;
    if (root.OZReady) root.OZReady(api.init);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  var SHOW_MS = 250, HIDE_MS = 200, HOLD_MS = 500;
  var cache = {};
  var card = null, owner = null, showT = 0, hideT = 0, holdT = 0, swallowClick = false;

  /* Hàm thuần: href (tuyệt đối) → {kind, id} hoặc null. */
  function target(href) {
    var u;
    try { u = new URL(href); } catch (e) { return null; }
    var m = u.pathname.match(/\/triet-gia\/([a-z0-9-]+)\/?$/);
    if (m) return { kind: "triet-gia", id: m[1] };
    if (/\/them\/tu-dien\/?$/.test(u.pathname) && u.hash.length > 1) return { kind: "thuat-ngu", id: decodeURIComponent(u.hash.slice(1)) };
    return null;
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  /* Hàm thuần: bản ghi → HTML của thẻ. */
  function render(kind, rec) {
    if (kind === "triet-gia") {
      var sub = [rec.years, rec.school].filter(Boolean).join(" · ");
      return '<p class="oz-the__ten">' + esc(rec.name) + (rec.name_en && rec.name_en !== rec.name ? ' <span lang="en">(' + esc(rec.name_en) + ")</span>" : "") +
        "</p>" + (sub ? '<p class="oz-the__phu">' + esc(sub) + "</p>" : "") + '<p class="oz-the__tom">' + esc(rec.summary) + "</p>";
    }
    return '<p class="oz-the__ten">' + esc(rec.vi) + (rec.en ? ' <span lang="en">(' + esc(rec.en) + ")</span>" : "") + "</p>" +
      '<p class="oz-the__tom">' + esc(rec.def) + "</p>";
  }

  function load(kind) {
    var base = (window.OZ && window.OZ.base) || "";
    var file = kind === "triet-gia" ? "philosophers.json" : "terms.json";
    if (!cache[file]) {
      cache[file] = fetch(base + "assets/data/" + file).then(function (r) { return r.json(); }).then(function (d) {
        var list = kind === "triet-gia" ? d : d.terms, map = {};
        list.forEach(function (x) { map[x.id] = x; });
        return map;
      });
    }
    return cache[file];
  }

  function ensureCard() {
    if (card && document.body.contains(card)) return card;
    card = document.createElement("div");
    card.className = "oz-the";
    card.id = "oz-the";
    card.setAttribute("role", "tooltip");
    card.hidden = true;
    card.addEventListener("pointerenter", function () { clearTimeout(hideT); });
    card.addEventListener("pointerleave", scheduleHide);
    document.body.appendChild(card);
    return card;
  }

  function place(a) {
    var r = a.getBoundingClientRect(), c = card.getBoundingClientRect();
    var vw = document.documentElement.clientWidth, vh = window.innerHeight;
    var left = Math.min(Math.max(8, r.left), vw - c.width - 8);
    var top = r.bottom + 6 + c.height > vh && r.top - 6 - c.height > 0 ? r.top - 6 - c.height : r.bottom + 6;
    card.style.left = left + window.scrollX + "px";
    card.style.top = top + window.scrollY + "px";
  }

  function show(a) {
    var t = target(a.href);
    if (!t) return;
    load(t.kind).then(function (map) {
      var rec = map[t.id];
      if (!rec || owner !== a) return;
      ensureCard().innerHTML = render(t.kind, rec);
      card.hidden = false;
      place(a);
      a.setAttribute("aria-describedby", "oz-the");
    }).catch(function () {});
  }

  function hide() {
    clearTimeout(showT);
    if (card) card.hidden = true;
    if (owner) owner.removeAttribute("aria-describedby");
    owner = null;
  }

  function scheduleHide() {
    clearTimeout(hideT);
    hideT = setTimeout(hide, HIDE_MS);
  }

  function link(ev) {
    var a = ev.target && ev.target.closest && ev.target.closest(".md-content a[href]");
    return a && target(a.href) ? a : null;
  }

  function open(a, delay) {
    clearTimeout(hideT);
    if (owner === a && card && !card.hidden) return;
    hide();
    owner = a;
    showT = setTimeout(function () { show(a); }, delay);
  }

  var SEL = '.md-content a[href*="triet-gia/"], .md-content a[href*="tu-dien/#"]';   // như loader.js
  var bound = false;
  function init(doc) {
    doc = doc || document;
    hide();
    doc.querySelectorAll(SEL).forEach(function (a) { a.dataset.ozInit = "1"; });
    if (bound) return;   // sự kiện gắn ở document: một lần cho mọi trang (instant navigation)
    bound = true;
    document.addEventListener("pointerover", function (ev) {
      if (ev.pointerType === "touch") return;
      var a = link(ev);
      if (a) open(a, SHOW_MS);
    });
    document.addEventListener("pointerout", function (ev) {
      var a = link(ev);
      if (a && a === owner && !(ev.relatedTarget && (a.contains(ev.relatedTarget) || (card && card.contains(ev.relatedTarget))))) scheduleHide();
    });
    document.addEventListener("focusin", function (ev) {
      var a = link(ev);
      if (a) open(a, 0);
      else if (!(card && card.contains(ev.target))) hide();
    });
    document.addEventListener("focusout", function (ev) {
      if (link(ev)) scheduleHide();
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && card && !card.hidden) hide();
    });
    // Điện thoại: chạm giữ để xem thẻ; chạm thường vẫn mở trang như cũ.
    document.addEventListener("pointerdown", function (ev) {
      if (ev.pointerType !== "touch") return;
      var a = link(ev);
      if (!a) {
        if (!(card && card.contains(ev.target))) hide();
        return;
      }
      clearTimeout(holdT);
      holdT = setTimeout(function () { swallowClick = true; open(a, 0); }, HOLD_MS);
    });
    ["pointerup", "pointercancel", "pointermove"].forEach(function (n) {
      document.addEventListener(n, function (ev) { if (n !== "pointermove" || ev.pointerType === "touch") clearTimeout(holdT); });
    });
    document.addEventListener("click", function (ev) {
      if (swallowClick && link(ev)) { ev.preventDefault(); }
      swallowClick = false;
    }, true);
    document.addEventListener("contextmenu", function (ev) { if (owner && link(ev) === owner) ev.preventDefault(); });
    window.addEventListener("scroll", function () { if (card && !card.hidden && owner) place(owner); }, { passive: true });
  }

  return { init: init, target: target, render: render };
});
