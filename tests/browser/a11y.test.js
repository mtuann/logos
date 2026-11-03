/* Kiểm tra khả năng tiếp cận bằng axe-core trên các trang tiêu biểu (sau khi công cụ đã dựng).
 * Tương phản màu được kiểm riêng trong tests/unit/contrast.test.js vì jsdom không tính được. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const { openPage, until } = require("./helpers");

const AXE = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
const PAGES = [
  "/logos/",
  "/logos/bat-dau/",
  "/logos/cau-hoi/tam-tri-va-ai/",
  "/logos/cau-hoi/dan-chu/",
  "/logos/cau-hoi/viet-hien-dai/",
  "/logos/cau-hoi/dao-duc-moi-truong/",
  "/logos/cau-hoi/cong-nghe-ai/",
  "/logos/cau-hoi/",
  "/logos/cau-hoi/sieu-dao-duc/",
  "/logos/cau-hoi/hanh-phuc/",
  "/logos/doc/luan-ngu/",
  "/logos/triet-gia/kant/",
  "/logos/triet-gia/",
  "/logos/lich-su/so-do-anh-huong/",
  "/logos/lich-su/dong-thoi-gian/",
  "/logos/cong-cu/nguy-bien/",
  "/logos/luyen-tap/nguy-bien/",
  "/logos/luyen-tap/the-ghi-nho/",
  "/logos/luyen-tap/ke-hoach/",
  "/logos/them/du-lieu/",
  "/logos/them/nhat-ky/",
  "/logos/them/tu-dien/",
];

for (const page of PAGES) {
  test(`axe: ${page}`, async () => {
    const { window, document } = await openPage(page);
    await until(() => !document.querySelector(".oz-fallacy-trainer > .oz-muted:only-child, .oz-flashcards > .oz-muted:only-child"));
    window.eval(AXE);
    const res = await window.axe.run(document.querySelector("article") || document, {
      runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"] },
      rules: { "color-contrast": { enabled: false }, region: { enabled: false } },
    });
    const bad = res.violations
      .filter((v) => ["serious", "critical"].includes(v.impact))
      .map((v) => `${v.id} (${v.impact}): ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
    assert.equal(bad.length, 0, bad.join("\n"));
    window.close();
  });
}
