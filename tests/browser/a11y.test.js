/* Kiểm tra khả năng tiếp cận bằng axe-core trên các trang tiêu biểu (sau khi công cụ đã dựng).
 * Tương phản màu được kiểm riêng trong tests/unit/contrast.test.js vì jsdom không tính được. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const { openPage, until } = require("./helpers");

const AXE = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
const PAGES = [
  "/logos-zero/",
  "/logos-zero/bat-dau/",
  "/logos-zero/cau-hoi/tam-tri-va-ai/",
  "/logos-zero/cau-hoi/dan-chu/",
  "/logos-zero/cau-hoi/viet-hien-dai/",
  "/logos-zero/cau-hoi/dao-duc-moi-truong/",
  "/logos-zero/cau-hoi/cong-nghe-ai/",
  "/logos-zero/cau-hoi/",
  "/logos-zero/cau-hoi/sieu-dao-duc/",
  "/logos-zero/cau-hoi/hanh-phuc/",
  "/logos-zero/doc/luan-ngu/",
  "/logos-zero/triet-gia/kant/",
  "/logos-zero/triet-gia/",
  "/logos-zero/lich-su/so-do-anh-huong/",
  "/logos-zero/lich-su/dong-thoi-gian/",
  "/logos-zero/cong-cu/nguy-bien/",
  "/logos-zero/luyen-tap/nguy-bien/",
  "/logos-zero/luyen-tap/the-ghi-nho/",
  "/logos-zero/luyen-tap/ke-hoach/",
  "/logos-zero/them/du-lieu/",
  "/logos-zero/them/nhat-ky/",
  "/logos-zero/them/tu-dien/",
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
