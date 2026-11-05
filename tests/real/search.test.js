/* Tìm kiếm trên Chromium thật (đợt 4.5, quyết định 22): worker riêng bỏ dấu, chỉ mục chỉ tải khi có ý tìm. */
const test = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const { start } = require("./server");

let browser, srv;
test.before(async () => { srv = await start(); browser = await chromium.launch(); });
test.after(async () => { await browser?.close(); srv?.server.close(); });

async function search(p, q) {
  await p.click(".md-search__input");
  await p.fill(".md-search__input", q);
  await p.waitForFunction(() => document.querySelectorAll(".md-search-result__item").length > 0, null, { timeout: 15000 });
  return p.$$eval(".md-search-result__item > a", (as) => as.slice(0, 8).map((a) => new URL(a.href).pathname));
}

test("chỉ mục chưa tải khi chưa đụng tới ô tìm; tải khi rê chuột vào", async () => {
  const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const got = [];
  p.on("request", (r) => { if (r.url().includes("search_index.json")) got.push(r.url()); });
  await p.goto(srv.origin + "/logos/cau-hoi/tri-thuc/", { waitUntil: "load" });
  await p.waitForTimeout(800);
  assert.equal(got.length, 0, "search_index.json bị tải ngay khi mở trang");
  await p.hover(".md-search__input");
  await p.waitForTimeout(800);
  assert.equal(got.length, 1);
  await p.close();
});

test("gõ không dấu ra bài có dấu; gõ có dấu vẫn ra", async () => {
  const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  // "tu do y chi" không có ở đây: xếp kém cả trước đợt 4.5 (ban-giao/viec-cho.md, 5/11/2026).
  for (const [q, want] of [["dao duc", /dao-duc/], ["tam tri", /tam-tri/], ["tâm trí", /tam-tri/],
                           ["tuong thich luan", /tu-do-y-chi/], ["Đạo đức", /dao-duc/], ["nguy bien", /nguy-bien/]]) {
    await p.goto(srv.origin + "/logos/", { waitUntil: "load" });   // trang mới: không đọc nhầm kết quả của câu trước
    const titles = await search(p, q);
    assert.ok(titles.some((t) => want.test(t)), `${q}: ${titles.join(" | ")}`);
  }
  await p.close();
});
