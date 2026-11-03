/* Kiểm thử hàm thuần chartData() của bieu-do.js. */
const test = require("node:test");
const assert = require("node:assert/strict");
const BD = require("../../docs/assets/js/bieu-do.js");

function emptyState() {
  return { v: 1, skills: {}, days: {}, quizzes: {}, read: {}, cards: {}, items: {}, journal: {}, imports: [] };
}

test("state rỗng → skills rỗng, activity đủ 14 ngày toàn 0", () => {
  const d = BD.chartData(emptyState(), "2026-10-13");
  assert.deepEqual(d.skills, []);
  assert.equal(d.activity.length, 14);
  assert.ok(d.activity.every((a) => a.n === 0));
  assert.equal(d.activity[13].date, "2026-10-13");
  assert.equal(d.activity[0].date, "2026-09-30");
});

test("skills: pct từ ema, sắp xếp theo n giảm dần", () => {
  const s = emptyState();
  s.skills.fallacy = { ema: 0.8, n: 10, last: "2026-10-01", days: {} };
  s.skills.logic = { ema: 0.4321, n: 3, last: "2026-10-02", days: {} };
  const d = BD.chartData(s, "2026-10-13");
  assert.equal(d.skills.length, 2);
  assert.equal(d.skills[0].id, "fallacy");
  assert.equal(d.skills[0].pct, 80);
  assert.equal(d.skills[0].name, "Nhận ra ngụy biện");
  assert.equal(d.skills[1].id, "logic");
  assert.equal(d.skills[1].pct, 43);
});

test("activity: ngày có dữ liệu vào đúng vị trí, ngày thiếu = 0", () => {
  const s = emptyState();
  s.days = { "2026-10-13": { n: 5, c: 4 }, "2026-10-11": { n: 2, c: 1 } };
  const d = BD.chartData(s, "2026-10-13");
  const byDate = {};
  d.activity.forEach((a) => (byDate[a.date] = a.n));
  assert.equal(byDate["2026-10-13"], 5);
  assert.equal(byDate["2026-10-11"], 2);
  assert.equal(byDate["2026-10-12"], 0);
});

test("skill chưa có ema (n>0) → pct null nhưng vẫn hiện", () => {
  const s = emptyState();
  s.skills.terms = { ema: null, n: 2, last: "2026-10-13", days: {} };
  const d = BD.chartData(s, "2026-10-13");
  assert.equal(d.skills.length, 1);
  assert.equal(d.skills[0].pct, null);
});
