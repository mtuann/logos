/* Logos — tiện ích dùng chung cho các công cụ. */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.util = api;
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // Bộ sinh số ngẫu nhiên có hạt giống (để kiểm thử tái lập được).
  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

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

  // Tạo phần tử DOM: el("button", {class: "x", onclick: f}, ["chữ", el(...)])
  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs)
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v === null || v === undefined || v === false) return;
        if (k.slice(0, 2) === "on" && typeof v === "function") n.addEventListener(k.slice(2), v);
        else if (k === "class") n.className = v;
        else if (k === "text") n.textContent = v;
        else n.setAttribute(k, v === true ? "" : v);
      });
    (children || []).forEach(function (c) {
      if (c === null || c === undefined || c === false) return;
      n.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return n;
  }

  var cache = {};
  function fetchJSON(path) {
    var base = (window.OZ && window.OZ.base) || "";
    var url = base + path;
    if (!cache[url])
      cache[url] = fetch(url).then(function (r) {
        if (!r.ok) throw new Error("Không tải được " + path + " (" + r.status + ")");
        return r.json();
      });
    return cache[url];
  }

  // Thông báo cho trình đọc màn hình qua vùng aria-live.
  function live(container) {
    var r = container.querySelector(".oz-live");
    if (!r) {
      r = el("div", { class: "oz-live oz-sr-only", "aria-live": "polite", role: "status" });
      container.appendChild(r);
    }
    return function (msg) {
      r.textContent = "";
      setTimeout(function () {
        r.textContent = msg;
      }, 30);
    };
  }

  // Chèn <mark> quanh chuỗi con (an toàn: dùng textNode).
  function highlight(text, part) {
    var frag = document.createDocumentFragment();
    var i = part ? text.indexOf(part) : -1;
    if (i < 0) {
      frag.appendChild(document.createTextNode(text));
      return frag;
    }
    frag.appendChild(document.createTextNode(text.slice(0, i)));
    frag.appendChild(el("mark", null, [part]));
    frag.appendChild(document.createTextNode(text.slice(i + part.length)));
    return frag;
  }

  function claim(node) {
    if (node.dataset.ozInit) return false;
    node.dataset.ozInit = "1";
    return true;
  }

  return { rng: rng, shuffle: shuffle, el: el, fetchJSON: fetchJSON, live: live, highlight: highlight, claim: claim };
});
