/* Kiểm thử hàm thuần recommend() của ke-hoach.js. */
const test = require("node:test");
const assert = require("node:assert/strict");
const KH = require("../../docs/assets/js/ke-hoach.js");

function emptyState() {
  return { v: 1, skills: {}, days: {}, quizzes: {}, read: {}, cards: {}, items: {}, journal: {}, imports: [] };
}

test("chưa có dữ liệu → nhóm nhập môn với 3 mục", () => {
  const groups = KH.recommend(emptyState());
  assert.equal(groups.length, 1);
  assert.equal(groups[0].level, "nhap-mon");
  assert.equal(groups[0].items.length, 3);
  assert.ok(groups[0].items.every((it) => it.title && it.path && it.kind));
});

test("kỹ năng yếu (ema < 0.6) → nhóm cần củng cố, 2 mục", () => {
  const s = emptyState();
  s.skills.fallacy = { ema: 0.4, n: 10, last: "2026-10-10", days: {} };
  const groups = KH.recommend(s);
  const g = groups.find((x) => x.level === "cung-co");
  assert.ok(g, "thiếu nhóm cung-co");
  assert.equal(g.skill, "fallacy");
  assert.equal(g.skillName, "Nhận ra ngụy biện");
  assert.equal(g.items.length, 2);
});

test("kỹ năng chưa từng thử → nhóm thử sức mới, 1 mục", () => {
  const s = emptyState();
  s.skills.fallacy = { ema: 0.9, n: 6, last: "2026-10-10", days: {} };
  const groups = KH.recommend(s);
  const g = groups.find((x) => x.skill === "logic" && x.level === "thu-suc");
  assert.ok(g, "thiếu nhóm thu-suc cho logic");
  assert.equal(g.items.length, 1);
  assert.equal(g.skillName, "Logic mệnh đề");
});

test("kỹ năng vững (ema >= 0.8, n >= 5) → nhóm đã vững", () => {
  const s = emptyState();
  s.skills.knowledge = { ema: 0.85, n: 8, last: "2026-10-10", days: {} };
  const groups = KH.recommend(s);
  const g = groups.find((x) => x.level === "vung");
  assert.ok(g, "thiếu nhóm vung");
  assert.equal(g.skill, "knowledge");
  assert.ok(g.items.length >= 1 && g.items.length <= 2);
});

test("kỹ năng đang học dở (0.6 <= ema < 0.8) → không gợi ý nhóm nào", () => {
  const s = emptyState();
  s.skills.mind = { ema: 0.7, n: 4, last: "2026-10-10", days: {} };
  const groups = KH.recommend(s);
  assert.ok(!groups.some((x) => x.skill === "mind"), "mind không nên vào nhóm nào");
});

test("ưu tiên mục chưa đọc trong nhóm củng cố", () => {
  const s = emptyState();
  s.skills.fallacy = { ema: 0.3, n: 5, last: "2026-10-10", days: {} };
  s.read["/cong-cu/nguy-bien/"] = "2026-10-09";
  const groups = KH.recommend(s);
  const g = groups.find((x) => x.level === "cung-co");
  assert.ok(g);
  assert.ok(
    g.items.some((it) => it.path === "/luyen-tap/nguy-bien/"),
    "phải ưu tiên mục chưa đọc, nhận được: " + g.items.map((it) => it.path).join(", ")
  );
});

test("thứ tự nhóm: củng cố trước, thử sức sau, đã vững cuối", () => {
  const s = emptyState();
  s.skills.fallacy = { ema: 0.4, n: 10, last: "2026-10-10", days: {} };
  s.skills.logic = { ema: 0.95, n: 10, last: "2026-10-10", days: {} };
  const groups = KH.recommend(s);
  const levels = groups.map((g) => g.level);
  assert.ok(levels.indexOf("cung-co") < levels.indexOf("vung"), "cung-co phải đứng trước vung");
  assert.ok(levels.indexOf("thu-suc") < levels.indexOf("vung"), "thu-suc phải đứng trước vung");
});

test("có mục đến hạn → nhóm ôn tập đứng đầu, trỏ đúng trang", () => {
  const s = emptyState();
  s.skills.fallacy = { ema: 0.4, n: 10, last: "2026-10-10", days: {} };
  const groups = KH.recommend(s, undefined, { dueTerms: 3, dueQuestions: 2 });
  assert.equal(groups[0].level, "on-tap");
  assert.equal(groups[0].skillName, "Ôn tập thông minh");
  assert.equal(groups[0].items.length, 1);
  assert.equal(groups[0].items[0].path, "/luyen-tap/on-tap/");
  assert.equal(groups[0].items[0].kind, "tool");
  assert.match(groups[0].items[0].title, /3.*thuật ngữ.*2.*câu hỏi/);
});

test("không có mục đến hạn → không có nhóm ôn tập", () => {
  const s = emptyState();
  s.skills.fallacy = { ema: 0.4, n: 10, last: "2026-10-10", days: {} };
  assert.ok(!KH.recommend(s).some((g) => g.level === "on-tap"));
  assert.ok(!KH.recommend(s, undefined, { dueTerms: 0, dueQuestions: 0 }).some((g) => g.level === "on-tap"));
});

test("chưa có dữ liệu nhưng có mục đến hạn → nhóm ôn tập trước nhóm nhập môn", () => {
  const groups = KH.recommend(emptyState(), undefined, { dueTerms: 1, dueQuestions: 0 });
  assert.equal(groups[0].level, "on-tap");
  assert.equal(groups[1].level, "nhap-mon");
});

test("integration: dueCounts từ on-tap.js → recommend hiện nhóm Ôn tập", () => {
  const OT = require("../../docs/assets/js/on-tap.js");
  const t = "2026-10-14";
  const terms = [{ id: "a" }];
  const items = [{ qid: "k", qindex: 0, article: "cau-hoi/x.md", q: "q", options: ["a", "b"], answer: 0, explain: "e" }];
  const cards = {
    a: { box: 1, due: "2026-10-14", intro: "2026-10-01", last: t },
    "quiz:k:0": { box: 2, due: "2026-10-13", intro: "2026-10-01", last: t },
  };
  // điểm nối production: refreshAll truyền thẳng OT.dueCounts(...) vào recommend
  const review = OT.dueCounts(terms, items, cards, t);
  const groups = KH.recommend(emptyState(), undefined, review);
  assert.equal(groups[0].level, "on-tap");
  assert.ok(groups[0].items[0].title.includes("1 thuật ngữ"));
  assert.ok(groups[0].items[0].title.includes("1 câu hỏi"));
});
