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
  for (const [q, want] of [["dao duc", /dao-duc/], ["tam tri", /tam-tri/], ["tâm trí", /tam-tri/],
                           ["tuong thich luan", /tu-do-y-chi/], ["Đạo đức", /dao-duc/], ["nguy bien", /nguy-bien/]]) {
    await p.goto(srv.origin + "/logos/", { waitUntil: "load" });   // trang mới: không đọc nhầm kết quả của câu trước
    const titles = await search(p, q);
    assert.ok(titles.some((t) => want.test(t)), `${q}: ${titles.join(" | ")}`);
  }
  await p.close();
});

test("đợt 7.1.3: mọi từ bắt buộc, chữ của địa chỉ trang vào tiêu đề trang (tên chủ đề tìm được)", async () => {
  const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  // Lượt 2 (24/11/2026): chỉ từ cuối giữ *, cộng điểm nguyên từ cuối — "tu do y chi" hạng 1, "tri thuc" hạng 4.
  for (const [q, want, n] of [["tri thuc", "/logos/cau-hoi/tri-thuc/", 5], ["ban nga", "/logos/cau-hoi/ban-nga-thoi-gian/", 3],
                              ["cai chet", "/logos/cau-hoi/cai-chet/", 1], ["tu do y chi", "/logos/cau-hoi/tu-do-y-chi/", 2]]) {
    await p.goto(srv.origin + "/logos/", { waitUntil: "load" });
    const top = (await search(p, q)).slice(0, n);
    assert.ok(top.includes(want), `${q}: ${top.join(" | ")}`);
  }
  await p.close();
});

test("đợt 7.1.3: tiêu đề kết quả không có mẩu thẻ tô sáng vỡ (chữ của địa chỉ trang gắn vào tiêu đề)", async () => {
  const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  for (const q of ["tri thuc", "tu do y chi", "ban nga"]) {
    await p.goto(srv.origin + "/logos/", { waitUntil: "load" });
    await search(p, q);
    // Chữ hiển thị (không phải HTML) không được chứa mẩu thẻ như "rk>" hay "<mark>".
    const texts = await p.$$eval(".md-search-result__item > a :is(h1,h2)", (hs) => hs.map((h) => h.textContent));
    for (const t of texts) assert.ok(!/[<>]/.test(t), `${q}: ${t}`);
  }
  await p.close();
});
