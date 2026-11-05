/* Máy chủ tĩnh cho site/ đã build, phục vụ dưới /logos/ như GitHub Pages. Dùng cho kiểm thử trên trình duyệt thật. */
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");

const SITE = path.join(__dirname, "../../site");
const BASE = "/logos/";
const TYPES = {
  ".html": "text/html; charset=utf-8", ".js": "application/javascript", ".css": "text/css",
  ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".woff2": "font/woff2",
  ".webmanifest": "application/manifest+json", ".xml": "application/xml", ".txt": "text/plain",
};

function start() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
      if (!p.startsWith(BASE)) { res.writeHead(404); return res.end(); }
      p = p.slice(BASE.length);
      let f = path.join(SITE, p);
      if (!f.startsWith(SITE)) { res.writeHead(403); return res.end(); }
      if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, "index.html");
      if (!fs.existsSync(f)) { res.writeHead(404); return res.end("not found"); }
      res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(res);
    });
    server.listen(0, "127.0.0.1", () => resolve({ server, origin: `http://127.0.0.1:${server.address().port}` }));
  });
}

/* 10 trang mẫu của đợt 4 (ban-giao/dot-4.md). */
const SAMPLES = [
  "/logos/", "/logos/bat-dau/", "/logos/cau-hoi/tri-thuc/", "/logos/cau-hoi/tu-do-y-chi/",
  "/logos/cong-cu/lap-luan-la-gi/", "/logos/lich-su/dong-thoi-gian/", "/logos/doc/platon-bien-ho/",
  "/logos/triet-gia/kant/", "/logos/them/tu-dien/", "/logos/luyen-tap/nguy-bien/",
];
const VIEWPORTS = { "may-tinh": { width: 1280, height: 900 }, "dien-thoai": { width: 390, height: 844 } };
const SCHEMES = ["light", "dark"];

module.exports = { start, SAMPLES, VIEWPORTS, SCHEMES, SITE };
