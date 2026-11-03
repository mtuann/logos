const test = require("node:test");
const assert = require("node:assert/strict");
const P = require("../../docs/assets/js/progress.js");

test("migrate đưa dữ liệu hỏng về cấu trúc rỗng", () => {
  for (const bad of [null, undefined, 42, "x", [], { skills: [] }]) {
    const s = P.migrate(bad);
    assert.equal(s.v, P.VERSION);
    assert.deepEqual(s.skills, {});
  }
});

test("applyAnswer: EMA, đếm theo ngày, không sửa trạng thái cũ", () => {
  const s0 = P.emptyState();
  const s1 = P.applyAnswer(s0, "fallacy", true, "2026-10-01", "fallacy:f-001");
  assert.deepEqual(s0.skills, {}, "trạng thái cũ phải giữ nguyên");
  assert.equal(s1.skills.fallacy.ema, 1);
  const s2 = P.applyAnswer(s1, "fallacy", false, "2026-10-01", "fallacy:f-001");
  assert.equal(s2.skills.fallacy.ema, 0.7);
  assert.deepEqual(s2.skills.fallacy.days["2026-10-01"], { n: 2, c: 1 });
  assert.deepEqual(s2.days["2026-10-01"], { n: 2, c: 1 });
  assert.deepEqual(s2.items["fallacy:f-001"], { n: 2, c: 1, last: "2026-10-01" });
  assert.equal(s2.skills.fallacy.last, "2026-10-01");
});

test("EMA luôn nằm trong [0, 1]", () => {
  let s = P.emptyState();
  let seed = 7;
  for (let i = 0; i < 500; i++) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    s = P.applyAnswer(s, "x", seed % 3 === 0, "2026-01-01");
    assert.ok(s.skills.x.ema >= 0 && s.skills.x.ema <= 1);
  }
  assert.equal(s.skills.x.n, 500);
});

test("applyQuiz giữ điểm cao nhất", () => {
  let s = P.applyQuiz(P.emptyState(), "mind-1", 3, 5, "2026-10-01");
  s = P.applyQuiz(s, "mind-1", 2, 5, "2026-10-02");
  assert.deepEqual(s.quizzes["mind-1"], { best: 3, total: 5, tries: 2, last: "2026-10-02" });
});

test("markRead chỉ ghi ngày đọc đầu tiên", () => {
  let s = P.markRead(P.emptyState(), "/a/", "2026-10-01");
  s = P.markRead(s, "/a/", "2026-10-05");
  assert.equal(s.read["/a/"], "2026-10-01");
});

test("streak đếm ngày liên tiếp, cho phép hôm nay chưa học", () => {
  let s = P.emptyState();
  for (const d of ["2026-10-08", "2026-10-09", "2026-10-10", "2026-10-12"]) s = P.applyAnswer(s, "a", true, d);
  assert.equal(P.streak(s, "2026-10-12"), 1);
  assert.equal(P.streak(s, "2026-10-13"), 1);
  s = P.applyAnswer(s, "a", true, "2026-10-11");
  assert.equal(P.streak(s, "2026-10-13"), 5);
  assert.equal(P.streak(s, "2026-10-15"), 0);
});

test("today định dạng YYYY-MM-DD", () => {
  assert.equal(P.today(new Date(2026, 0, 5)), "2026-01-05");
});
