/* Logos Zero — service worker: đọc ngoại tuyến các trang đã mở.
 * HTML: mạng trước, hết mạng thì dùng bản đã lưu. Tài nguyên tĩnh: bản lưu trước, cập nhật ngầm.
 * Tăng VERSION khi đổi chiến lược lưu trữ. */
// Tên cache có tiền tố "logos-": logos-zero chạy trên cùng origin với cache "oz-v1",
// nên khi kích hoạt chỉ xóa cache cũ của chính logos.
var PREFIX = "logos-";
var VERSION = PREFIX + "v1";
var CORE = ["./", "assets/css/oz.css", "assets/fonts/be-vietnam-pro-400.woff2", "assets/js/core.js", "assets/js/progress.js", "assets/js/loader.js", "assets/img/icon.svg"];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(VERSION).then(function (c) {
      return c.addAll(CORE).catch(function () {});
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k.indexOf(PREFIX) === 0 && k !== VERSION; }).map(function (k) { return caches.delete(k); })
      );
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  var isPage = req.mode === "navigate" || (req.headers.get("accept") || "").indexOf("text/html") !== -1;
  if (isPage || /search_index\.json$|\.json$/.test(req.url)) {
    e.respondWith(
      fetch(req).then(function (res) {
        var copy = res.clone();
        if (res.ok) caches.open(VERSION).then(function (c) { c.put(req, copy); });
        return res;
      }).catch(function () {
        return caches.match(req).then(function (hit) { return hit || caches.match("./"); });
      })
    );
    return;
  }
  // Tài nguyên tĩnh: trả bản đã lưu ngay, đồng thời cập nhật ngầm (stale-while-revalidate).
  e.respondWith(
    caches.open(VERSION).then(function (c) {
      return c.match(req).then(function (hit) {
        var net = fetch(req).then(function (res) {
          if (res.ok) c.put(req, res.clone());
          return res;
        });
        if (hit) {
          net.catch(function () {});
          return hit;
        }
        return net;
      });
    })
  );
});
