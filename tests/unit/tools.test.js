const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const U = require("../../docs/assets/js/util.js");
const quiz = require("../../docs/assets/js/quiz.js");
const fallacy = require("../../docs/assets/js/fallacy.js");
const fc = require("../../docs/assets/js/flashcards.js");
const loader = require("../../docs/assets/js/loader.js");
const daily = require("../../docs/assets/js/daily.js");

const DATA = path.join(__dirname, "../../docs/assets/data");

test("shuffle giữ nguyên phần tử và tái lập được với cùng hạt giống", () => {
  const a = [1, 2, 3, 4, 5, 6, 7, 8];
  const x = U.shuffle(a, U.rng(1));
  assert.deepEqual([...x].sort(), a);
  assert.deepEqual(U.shuffle(a, U.rng(1)), x);
  assert.deepEqual(a, [1, 2, 3, 4, 5, 6, 7, 8]);
});

test("quiz.grade chấm đúng, câu bỏ trống không tính", () => {
  const qs = [
    { q: "a", options: ["x", "y"], answer: 1, explain: "." },
    { q: "b", options: ["x", "y"], answer: 0, explain: "." },
    { q: "c", options: ["x", "y"], answer: 0, explain: "." },
  ];
  const g = quiz.grade(qs, [1, 1, null]);
  assert.equal(g.score, 1);
  assert.deepEqual(g.results.map((r) => r.answered), [true, true, false]);
  assert.equal(quiz.validate(qs), null);
  assert.match(quiz.validate([{ q: "a", options: ["x"], answer: 0, explain: "." }]), /thiếu/);
  assert.match(quiz.validate([{ q: "a", options: ["x", "y"], answer: 2, explain: "." }]), /ngoài phạm vi/);
});

test("ngân hàng ngụy biện hợp lệ: 100 câu, mỗi loại ≥ 4 lần, có câu 'none'", () => {
  const data = JSON.parse(fs.readFileSync(path.join(DATA, "fallacies.json"), "utf8"));
  assert.deepEqual(fallacy.validateBank(data), []);
  assert.equal(data.questions.length, 100);
  const count = {};
  data.questions.forEach((q) => (count[q.answer] = (count[q.answer] || 0) + 1));
  data.types.forEach((t) => assert.ok((count[t.id] || 0) >= 4, `${t.id} chỉ có ${count[t.id] || 0} câu`));
  assert.ok(count.none >= 10);
  for (const lv of [1, 2, 3]) assert.ok(data.questions.filter((q) => q.level === lv).length >= 15);
});

test("pickQuestions: đúng số lượng, không lặp, lọc cấp độ, ưu tiên câu hay sai", () => {
  const bank = Array.from({ length: 30 }, (_, i) => ({ id: "q" + i, level: (i % 3) + 1 }));
  for (let seed = 1; seed < 50; seed++) {
    const p = fallacy.pickQuestions(bank, { count: 10, level: "2", rng: U.rng(seed) });
    assert.equal(p.length, 10);
    assert.equal(new Set(p.map((q) => q.id)).size, 10);
    assert.ok(p.every((q) => q.level === 2));
  }
  assert.equal(fallacy.pickQuestions(bank, { count: 99, rng: U.rng(3) }).length, 30);
  // q0 luôn sai, các câu khác luôn đúng → q0 xuất hiện thường xuyên hơn mức đều.
  const items = {};
  bank.forEach((q) => (items["fallacy:" + q.id] = { n: 5, c: q.id === "q0" ? 0 : 5 }));
  let hits = 0;
  for (let seed = 1; seed <= 400; seed++) if (fallacy.pickQuestions(bank, { count: 3, items, rng: U.rng(seed) }).some((q) => q.id === "q0")) hits++;
  assert.ok(hits / 400 > 0.3, "tỉ lệ chọn câu hay sai quá thấp: " + hits / 400);
  assert.ok(fallacy.weight(undefined) > fallacy.weight({ n: 4, c: 4 }));
});

test("flashcards.review: lên hộp khi nhớ, về hộp 1 khi quên, hạn ôn đúng", () => {
  let c = fc.review(undefined, true, "2026-10-13");
  assert.deepEqual(c, { box: 1, due: "2026-10-14", intro: "2026-10-13", last: "2026-10-13" });
  c = fc.review(c, true, "2026-10-14");
  assert.equal(c.box, 2);
  assert.equal(c.due, "2026-10-16");
  for (let i = 0; i < 10; i++) c = fc.review(c, true, "2026-11-01");
  assert.equal(c.box, 5);
  assert.equal(c.due, "2026-11-17");
  c = fc.review(c, false, "2026-11-17");
  assert.equal(c.box, 1);
  assert.equal(c.intro, "2026-10-13");
  assert.equal(fc.addDays("2026-12-31", 1), "2027-01-01");
});

test("flashcards.session: thẻ đến hạn trước, giới hạn thẻ mới mỗi ngày", () => {
  const terms = Array.from({ length: 12 }, (_, i) => ({ id: "t" + i }));
  const cards = {
    t0: { box: 3, due: "2026-10-10", intro: "2026-10-01" },
    t1: { box: 1, due: "2026-10-13", intro: "2026-10-12" },
    t2: { box: 2, due: "2026-10-20", intro: "2026-10-12" },
    t3: { box: 1, due: "2026-10-14", intro: "2026-10-13" },
  };
  const s = fc.session(terms, cards, "2026-10-13", { newLimit: 3, max: 20 });
  assert.deepEqual(s.slice(0, 2), ["t1", "t0"], "hộp thấp trước");
  assert.equal(s.length, 2 + 2, "đã giới thiệu 1 thẻ mới hôm nay → còn 2");
  assert.ok(!s.includes("t2"));
  assert.equal(fc.session(terms, cards, "2026-10-13", { newLimit: 3, max: 1 }).length, 1);
  const counts = fc.boxCounts(terms, cards);
  assert.equal(counts[0], 8);
});

test("loader.plan: chỉ nạp script cần thiết, đúng thứ tự, không trùng", () => {
  assert.deepEqual(loader.plan([]), []);
  assert.deepEqual(loader.plan([".oz-quiz"]), ["util.js", "quiz.js"]);
  assert.deepEqual(loader.plan([".oz-quiz", ".oz-fallacy-trainer"]), ["util.js", "quiz.js", "fallacy.js"]);
  assert.deepEqual(loader.plan([".oz-quiz"], ["util.js", "quiz.js"]), []);
  // Mọi script trong bảng phải tồn tại.
  loader.TOOLS.forEach((t) => t.js.forEach((f) => assert.ok(fs.existsSync(path.join(__dirname, "../../docs/assets/js", f)), f)));
});

test("daily.pickIndex xoay vòng đều qua các ngày", () => {
  const seen = new Set();
  for (let d = 1; d <= 7; d++) seen.add(daily.pickIndex(`2026-10-${String(d).padStart(2, "0")}`, 7));
  assert.equal(seen.size, 7);
  assert.equal(daily.pickIndex("2026-10-13", 1), 0);
});

test("terms.json hợp lệ", () => {
  const data = JSON.parse(fs.readFileSync(path.join(DATA, "terms.json"), "utf8"));
  assert.ok(data.terms.length >= 40);
  const ids = new Set();
  for (const t of data.terms) {
    assert.ok(t.id && t.vi && t.def, JSON.stringify(t));
    assert.ok(!ids.has(t.id), "trùng " + t.id);
    ids.add(t.id);
  }
});
