/* Thẻ di chuột trên Chromium thật (đợt 4.7): chuột, bàn phím, Esc, chạm giữ; axe khi thẻ đang mở. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const { chromium } = require("playwright");
const { start } = require("./server");

const AXE = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
let browser, srv;
test.before(async () => { srv = await start(); browser = await chromium.launch(); });
test.after(async () => { await browser?.close(); srv?.server.close(); });

async function firstLink(p) {
  return p.waitForSelector('.md-content article a[href*="triet-gia/platon"][data-oz-init="1"] >> visible=true', { timeout: 10000 });
}

test("rê chuột hiện thẻ, rời đi thì tắt; axe 0 khi thẻ mở", async () => {
  const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await p.goto(srv.origin + "/logos/cau-hoi/tri-thuc/", { waitUntil: "load" });
  const a = await firstLink(p);
  await a.hover();
  await p.waitForSelector("#oz-the:not([hidden])", { timeout: 3000 });
  const text = await p.textContent("#oz-the");
  assert.match(text, /Platon/);
  assert.match(text, /427|428/);
  assert.equal(await a.getAttribute("aria-describedby"), "oz-the");
  await p.addScriptTag({ content: AXE });
  const v = await p.evaluate(async () => (await axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"] } })).violations.map((x) => x.id));
  assert.deepEqual(v, []);
  await p.mouse.move(5, 5);
  await p.waitForSelector("#oz-the", { state: "hidden", timeout: 3000 });
  await p.close();
});

test("bàn phím: Tab tới link hiện thẻ, Esc đóng", async () => {
  const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await p.goto(srv.origin + "/logos/cau-hoi/tri-thuc/", { waitUntil: "load" });
  const a = await firstLink(p);
  await a.focus();
  await p.waitForSelector("#oz-the:not([hidden])", { timeout: 3000 });
  await p.keyboard.press("Escape");
  await p.waitForSelector("#oz-the", { state: "hidden", timeout: 3000 });
  await p.close();
});

test("điện thoại: chạm thường mở trang, chạm giữ hiện thẻ", async () => {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const p = await ctx.newPage();
  await p.goto(srv.origin + "/logos/cau-hoi/tri-thuc/", { waitUntil: "load" });
  const a = await firstLink(p);
  await a.scrollIntoViewIfNeeded();
  const box = await a.boundingBox();
  const cdp = await ctx.newCDPSession(p);
  const pt = { x: box.x + 5, y: box.y + box.height / 2 };
  await cdp.send("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [pt] });
  await p.waitForTimeout(700);
  await cdp.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
  await p.waitForSelector("#oz-the:not([hidden])", { timeout: 3000 });
  assert.match(new URL(p.url()).pathname, /cau-hoi\/tri-thuc/, "chạm giữ không được mở trang");
  await a.tap();
  await p.waitForURL(/triet-gia\/platon/, { timeout: 5000 });
  await ctx.close();
});
