/* Điện thoại và máy tính (đợt 4.10): khối "Tóm tắt 5 phút" thu gọn được, nút In nằm trong dải thông tin. */
const test = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const { start } = require("./server");

let browser, srv;
test.before(async () => { srv = await start(); browser = await chromium.launch(); });
test.after(async () => { await browser?.close(); srv?.server.close(); });

for (const [name, viewport, open] of [["điện thoại", { width: 390, height: 844 }, false], ["máy tính", { width: 1280, height: 900 }, true]]) {
  test(`Tóm tắt 5 phút trên ${name}: mặc định ${open ? "mở" : "gọn"}, bấm để đổi`, async () => {
    const p = await browser.newPage({ viewport });
    await p.goto(srv.origin + "/logos/cau-hoi/tri-thuc/", { waitUntil: "load" });
    const btn = await p.waitForSelector(".admonition.summary .oz-tom-tat__nut");
    assert.equal(await btn.getAttribute("aria-expanded"), String(open));
    assert.equal(await p.isVisible(".oz-tom-tat__than"), open);
    await btn.click();
    assert.equal(await btn.getAttribute("aria-expanded"), String(!open));
    assert.equal(await p.isVisible(".oz-tom-tat__than"), !open);
    await p.close();
  });
}

test("nút In nằm trong dải thông tin; trang chủ không có nút In", async () => {
  const p = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await p.goto(srv.origin + "/logos/cau-hoi/tri-thuc/", { waitUntil: "load" });
  await p.waitForSelector(".oz-info .oz-print-btn");
  const box = await (await p.$(".oz-info")).boundingBox();
  assert.ok(box.y + box.height < 844, "dải thông tin phải nằm trong màn hình đầu");
  await p.goto(srv.origin + "/logos/", { waitUntil: "load" });
  await p.waitForTimeout(300);
  assert.equal(await p.$(".oz-print-btn"), null);
  await p.close();
});
