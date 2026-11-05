/* Chụp ảnh 10 trang mẫu (ban-giao/dot-4.md) × máy tính/điện thoại × sáng/tối vào site-anh/ để chủ biên duyệt.
 *   npm run anh               # cần site/ đã build và Chromium của Playwright (npx playwright install chromium)
 * Ảnh máy tính chụp màn hình đầu (1280×900); ảnh điện thoại chụp cả trang tới tối đa 4 màn hình. */
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
const { start, SAMPLES, VIEWPORTS, SCHEMES } = require("./server");

const OUT = path.join(__dirname, "../../site-anh");

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = await start();
  const browser = await chromium.launch();
  const list = [];
  for (const page of SAMPLES) for (const [vp, size] of Object.entries(VIEWPORTS)) for (const scheme of SCHEMES) {
    const ctx = await browser.newContext({ viewport: size, colorScheme: scheme, deviceScaleFactor: vp === "dien-thoai" ? 2 : 1 });
    const p = await ctx.newPage();
    await p.goto(srv.origin + page, { waitUntil: "load" });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(400);
    const name = `${page.replace(/^\/logos\//, "").replace(/\/$/, "").replace(/\//g, "_") || "trang-chu"}.${vp}.${scheme}.png`;
    const full = vp === "dien-thoai";
    const clip = full ? { x: 0, y: 0, width: size.width, height: Math.min(await p.evaluate(() => document.body.scrollHeight), size.height * 4) } : undefined;
    await p.screenshot({ path: path.join(OUT, name), fullPage: full, clip });
    list.push(name);
    await ctx.close();
  }
  await browser.close();
  srv.server.close();
  fs.writeFileSync(path.join(OUT, "danh-sach.json"), JSON.stringify(list, null, 1));
  console.log(`Đã chụp ${list.length} ảnh vào site-anh/.`);
})();
