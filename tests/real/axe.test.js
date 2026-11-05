/* axe-core trên Chromium thật (Playwright), quét cả trang, gồm tương phản màu và vùng chạm (WCAG 2.2 AA),
 * cho 10 trang mẫu × 2 cỡ màn hình × sáng/tối (ban-giao/dot-4.md việc 4.1). jsdom (tests/browser/a11y.test.js)
 * không tính được tương phản và bố cục, nên bộ này bắt được những lỗi jsdom bỏ sót.
 *
 *   npm run test:real                 # chặn: mọi vi phạm là lỗi
 *   AXE_REPORT=1 npm run test:real    # ghi verification/giao-dien/axe.md, không chặn (đo nền, đo trước/sau)
 */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
const { start, SAMPLES, VIEWPORTS, SCHEMES } = require("./server");

const AXE = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];
const REPORT = process.env.AXE_REPORT === "1";
const OUT = path.join(__dirname, "../../verification/giao-dien/axe.md");

let browser, srv;
const rows = [];

test.before(async () => {
  srv = await start();
  browser = await chromium.launch();
});

test.after(async () => {
  await browser?.close();
  srv?.server.close();
  if (!REPORT) return;
  const byRule = {};
  for (const r of rows) for (const v of r.violations) {
    byRule[v.id] ??= { impact: v.impact, help: v.help, nodes: 0, where: new Set() };
    byRule[v.id].nodes += v.nodes;
    byRule[v.id].where.add(r.page);
  }
  const L = ["# Đo axe trên trình duyệt thật", "",
    "Sinh bằng `AXE_REPORT=1 npm run test:real` (Chromium qua Playwright, axe-core 4.13.0, WCAG 2.2 AA, cả trang).",
    `10 trang mẫu × ${Object.keys(VIEWPORTS).length} cỡ màn hình × ${SCHEMES.length} chế độ màu = ${rows.length} lần quét.`, "",
    `**${Object.values(byRule).reduce((a, b) => a + b.nodes, 0)} phần tử vi phạm**, ${Object.keys(byRule).length} luật.`, "",
    "| Luật | Mức | Nghĩa | Phần tử (cộng mọi lần quét) | Trang |", "|---|---|---|---:|---|"];
  for (const [id, v] of Object.entries(byRule).sort((a, b) => b[1].nodes - a[1].nodes))
    L.push(`| \`${id}\` | ${v.impact} | ${v.help.replace(/\|/g, "\\|")} | ${v.nodes} | ${[...v.where].sort().join(", ")} |`);
  L.push("", "## Từng lần quét", "", "| Trang | Màn hình | Màu | Vi phạm (luật: số phần tử) |", "|---|---|---|---|");
  for (const r of rows)
    L.push(`| ${r.page} | ${r.vp} | ${r.scheme} | ${r.violations.map((v) => `\`${v.id}\`: ${v.nodes}`).join(", ") || "0"} |`);
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, L.join("\n") + "\n");
});

for (const page of SAMPLES) for (const [vp, size] of Object.entries(VIEWPORTS)) for (const scheme of SCHEMES) {
  test(`axe ${page} ${vp} ${scheme}`, async () => {
    const ctx = await browser.newContext({ viewport: size, colorScheme: scheme, reducedMotion: "reduce" });
    const p = await ctx.newPage();
    await p.goto(srv.origin + page, { waitUntil: "load" });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.addScriptTag({ content: AXE });
    const res = await p.evaluate(async (tags) => {
      const r = await window.axe.run(document, { runOnly: { type: "tag", values: tags } });
      return r.violations.map((v) => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length,
        targets: v.nodes.slice(0, 3).map((n) => n.target.join(" ")) }));
    }, TAGS);
    await ctx.close();
    rows.push({ page, vp, scheme, violations: res });
    if (!REPORT) assert.equal(res.length, 0, res.map((v) => `${v.id} (${v.impact}, ${v.nodes}): ${v.targets.join(" | ")}`).join("\n"));
  });
}

test("font tự host được tải và dùng (đợt 4.4)", async () => {
  const ctx = await browser.newContext();
  const p = await ctx.newPage();
  const fonts = [];
  p.on("response", (r) => { if (r.url().endsWith(".woff2")) fonts.push(r.status()); });
  await p.goto(srv.origin + "/logos/cau-hoi/tri-thuc/", { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready);
  const loaded = await p.evaluate(() => [...document.fonts].filter((f) => f.status === "loaded").map((f) => `${f.family} ${f.weight} ${f.style}`));
  await ctx.close();
  assert.ok(loaded.some((f) => f.startsWith('"Be Vietnam Pro" 400') || f.startsWith("Be Vietnam Pro 400")), loaded.join(", "));
  assert.ok(loaded.some((f) => /Noto Serif/.test(f)), loaded.join(", "));
  assert.ok(fonts.length > 0 && fonts.every((s) => s === 200), String(fonts));
});
