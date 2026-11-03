/* Mở trang đã build (site/) trong jsdom, qua bộ tải thật của site.
 * Script của Material được thay bằng rỗng (jsdom không chạy nổi), nên core.js
 * dùng nhánh DOMContentLoaded thay cho document$. fetch được giả lập bằng đọc file. */
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM, VirtualConsole, requestInterceptor } = require("jsdom");

const SITE = path.join(__dirname, "../../site");
const ORIGIN = "http://localhost";
const BASE = "/logos/";

function fileFor(url) {
  const u = new URL(url);
  let p = decodeURIComponent(u.pathname);
  if (!p.startsWith(BASE)) return null;
  p = p.slice(BASE.length);
  if (p === "" || p.endsWith("/")) p += "index.html";
  return path.join(SITE, p);
}

function siteInterceptor(log) {
  return requestInterceptor((request) => {
    const url = request.url;
    if (!url.startsWith(ORIGIN)) return new Response("", { status: 200 });
    log.push(url);
    if (/\/assets\/javascripts\//.test(url)) return new Response("", { headers: { "Content-Type": "application/javascript" } }); // Material
    const f = fileFor(url);
    if (!f || !fs.existsSync(f)) return new Response("not found", { status: 404 });
    const type = f.endsWith(".js") ? "application/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "application/octet-stream";
    return new Response(fs.readFileSync(f), { headers: { "Content-Type": type } });
  });
}

function listPages() {
  const out = [];
  (function walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) {
        if (["assets", "search", "sach"].includes(e.name)) continue;
        walk(p);
      } else if (e.name === "index.html") out.push(BASE + path.relative(SITE, dir).split(path.sep).join("/") + (dir === SITE ? "" : "/"));
    }
  })(SITE);
  return out.map((p) => p.replace(/\/\/$/, "/")).sort();
}

async function openPage(pagePath, opts = {}) {
  const errors = [];
  const requests = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", (e) => errors.push(e.message || String(e)));
  vc.on("error", (e) => errors.push(String(e)));
  const file = fileFor(ORIGIN + pagePath);
  const html = fs.readFileSync(file, "utf8");
  const dom = new JSDOM(html, {
    url: ORIGIN + pagePath,
    runScripts: "dangerously",
    resources: { interceptors: [siteInterceptor(requests)] },
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(window) {
      window.fetch = (url) => {
        const f = fileFor(new URL(url, window.location.href).href);
        if (!f || !fs.existsSync(f)) return Promise.resolve({ ok: false, status: 404 });
        const body = fs.readFileSync(f, "utf8");
        return Promise.resolve({ ok: true, status: 200, json: () => Promise.resolve(JSON.parse(body)), text: () => Promise.resolve(body) });
      };
      window.print = () => {};
      window.confirm = () => true;
      window.addEventListener("error", (e) => errors.push(e.message));
      if (opts.storage) window.localStorage.setItem("logos", JSON.stringify(opts.storage));
    },
  });
  await new Promise((r) => dom.window.addEventListener("load", r));
  await settle();
  const toolScripts = requests.filter((u) => /\/assets\/js\//.test(u)).map((u) => u.split("/assets/js/")[1]);
  return { dom, window: dom.window, document: dom.window.document, errors, requests, toolScripts };
}

function settle(ms = 30) {
  return new Promise((r) => setTimeout(r, ms));
}

async function until(fn, ms = 2000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    if (fn()) return true;
    await settle(15);
  }
  return false;
}

module.exports = { SITE, BASE, listPages, openPage, settle, until };
