/* Kiểm thử các hàm thuần của on-tap.js (phiên ôn tập thông minh). */
const test = require("node:test");
const assert = require("node:assert/strict");
const OT = require("../../docs/assets/js/on-tap.js");
const FC = require("../../docs/assets/js/flashcards.js");

test("INTERVAL đồng bộ với flashcards.js", () => {
  assert.deepEqual(OT.INTERVAL, FC.INTERVAL);
});

test("quizKey namespaced, merge.js gộp được", () => {
  assert.equal(OT.quizKey("ethics-cai-ac", 0), "quiz:ethics-cai-ac:0");
});

test("reviewCard: đúng lên hộp, sai về hộp 1", () => {
  const t = "2026-10-14";
  let c = OT.reviewCard(undefined, true, t);
  assert.equal(c.box, 1);
  assert.equal(c.due, OT.addDays(t, 1));
  assert.equal(c.intro, t);
  assert.equal(c.last, t);
  c = OT.reviewCard({ box: 4, due: "2026-10-14", intro: "2026-09-01", last: "2026-10-13" }, true, t);
  assert.equal(c.box, 5);
  assert.equal(c.due, OT.addDays(t, 16));
  assert.equal(c.intro, "2026-09-01");
  c = OT.reviewCard({ box: 5, due: t, intro: t, last: t }, true, t);
  assert.equal(c.box, 5); // không vượt hộp 5
  c = OT.reviewCard({ box: 3, due: t, intro: t, last: t }, false, t);
  assert.equal(c.box, 1);
  assert.equal(c.due, OT.addDays(t, 1));
});

test("reviewCard khớp flashcards.review (cùng logic Leitner)", () => {
  const t = "2026-10-14";
  for (const [card, ok] of [
    [undefined, true],
    [{ box: 2, due: t, intro: t, last: t }, true],
    [{ box: 4, due: t, intro: t, last: t }, false],
    [{ box: 5, due: t, intro: t, last: t }, true],
  ]) {
    assert.deepEqual(OT.reviewCard(card, ok, t), FC.review(card, ok, t));
  }
});

const TERMS = [{ id: "a" }, { id: "b" }, { id: "c" }, { id: "d" }];

test("dueTermIds: đến hạn trước (hộp thấp trước), rồi thẻ mới giới hạn", () => {
  const t = "2026-10-14";
  const cards = {
    a: { box: 3, due: "2026-10-14", intro: "2026-10-01", last: t },
    b: { box: 1, due: "2026-10-10", intro: "2026-10-01", last: t },
    c: { box: 2, due: "2026-10-20", intro: "2026-10-01", last: t }, // chưa đến hạn
  };
  const ids = OT.dueTermIds(TERMS, cards, t, { termNew: 5, termMax: 10 });
  assert.deepEqual(ids, ["b", "a", "d"]); // b hộp 1 trước a hộp 3; d là thẻ mới
});

test("dueTermIds: tôn trọng termNew", () => {
  const t = "2026-10-14";
  const ids = OT.dueTermIds(TERMS, {}, t, { termNew: 1, termMax: 10 });
  assert.deepEqual(ids, ["a"]);
});

function q(qid, i, article) {
  return { qid, qindex: i, skill: "ethics", article: article || "cau-hoi/x.md", q: "?", options: ["A", "B"], answer: 0, explain: "e" };
}

test("dueQuizItems: đúng lên hộp / sai về hộp 1 qua buildSession", () => {
  const t = "2026-10-14";
  const items = [q("k1", 0), q("k1", 1), q("k2", 0)];
  const cards = {
    "quiz:k1:0": { box: 2, due: "2026-10-14", intro: "2026-10-01", last: t },
    "quiz:k1:1": { box: 2, due: "2026-10-20", intro: "2026-10-01", last: t }, // chưa đến hạn
  };
  const got = OT.dueQuizItems(items, cards, t, { qMax: 10, qNew: 1, read: {} });
  assert.equal(got.length, 2);
  assert.equal(OT.quizKey(got[0].qid, got[0].qindex), "quiz:k1:0"); // đến hạn trước
  // câu mới: k2:0 (k1:1 cũng mới nhưng room chỉ 1)
  const freshKey = OT.quizKey(got[1].qid, got[1].qindex);
  assert.equal(freshKey, "quiz:k2:0");
});

test("dueQuizItems: ưu tiên câu mới của bài đã đọc", () => {
  const t = "2026-10-14";
  const items = [q("u1", 0, "cau-hoi/chua-doc.md"), q("u2", 0, "cau-hoi/da-doc.md")];
  const got = OT.dueQuizItems(items, {}, t, { qMax: 10, qNew: 1, read: { "cau-hoi/da-doc.md": "2026-10-13" } });
  assert.equal(got.length, 1);
  assert.equal(got[0].qid, "u2");
});

test("buildSession + mixSession: trộn đủ thẻ và câu hỏi", () => {
  const t = "2026-10-14";
  const items = [q("k1", 0), q("k1", 1)];
  const ses = OT.buildSession(TERMS, items, {}, t, { termNew: 2, termMax: 10, qNew: 2, qMax: 10 });
  assert.deepEqual(ses.terms, ["a", "b"]);
  assert.equal(ses.questions.length, 2);
  const seeded = () => 0.5;
  const mixed = OT.mixSession(ses.terms, ses.questions, seeded);
  assert.equal(mixed.length, 4);
  assert.equal(mixed.filter((x) => x.kind === "term").length, 2);
  assert.equal(mixed.filter((x) => x.kind === "question").length, 2);
  // shuffle với rand cố định cho kết quả ổn định
  assert.deepEqual(OT.mixSession(["a", "b"], [q("k", 0)], seeded), OT.mixSession(["a", "b"], [q("k", 0)], seeded));
});

test("dueCounts chỉ đếm mục đến hạn, không tính mục mới", () => {
  const t = "2026-10-14";
  const terms = [{ id: "a" }, { id: "b" }];
  const items = [q("k1", 0), q("k1", 1)];
  const cards = {
    a: { box: 1, due: "2026-10-14", intro: "2026-10-01", last: t },
    "quiz:k1:0": { box: 3, due: "2026-10-13", intro: "2026-10-01", last: t },
  };
  assert.deepEqual(OT.dueCounts(terms, items, cards, t), { terms: 1, questions: 1 });
});

test("streakDays: chuỗi ngày liên tiếp", () => {
  assert.equal(OT.streakDays({}, "2026-10-14"), 0);
  const d = { "2026-10-14": { n: 5, c: 4 } };
  assert.equal(OT.streakDays(d, "2026-10-14"), 1);
  const d2 = { "2026-10-12": { n: 1, c: 1 }, "2026-10-13": { n: 2, c: 2 }, "2026-10-14": { n: 1, c: 0 } };
  assert.equal(OT.streakDays(d2, "2026-10-14"), 3);
  // hôm nay nghỉ nhưng hôm qua có học → vẫn tính
  const d3 = { "2026-10-12": { n: 1, c: 1 }, "2026-10-13": { n: 1, c: 1 } };
  assert.equal(OT.streakDays(d3, "2026-10-14"), 2);
  // đứt quãng
  const d4 = { "2026-10-10": { n: 1, c: 1 }, "2026-10-14": { n: 1, c: 1 } };
  assert.equal(OT.streakDays(d4, "2026-10-14"), 1);
});

test("buildSession: max giới hạn tổng số mục", () => {
  const t = "2026-10-14";
  const terms = Array.from({ length: 40 }, (_, i) => ({ id: "t" + i }));
  const items = Array.from({ length: 40 }, (_, i) => q("k", i));
  const ses = OT.buildSession(terms, items, {}, t, { max: 20, termNew: 40, qNew: 40 });
  assert.ok(ses.terms.length + ses.questions.length <= 20);
  assert.equal(ses.terms.length, 10);
  assert.equal(ses.questions.length, 10);
});

test("canonArticleKey: chuẩn hóa URL path và bank path", () => {
  assert.equal(OT.canonArticleKey("/cau-hoi/tri-thuc/"), "cau-hoi/tri-thuc");
  assert.equal(OT.canonArticleKey("cau-hoi/tri-thuc.md"), "cau-hoi/tri-thuc");
  assert.equal(OT.canonArticleKey("cau-hoi/tri-thuc"), "cau-hoi/tri-thuc");
  assert.equal(OT.canonArticleKey("/"), "");
  assert.equal(OT.canonArticleKey("index.md"), "");
});

test("dueQuizItems: ưu tiên bài đã đọc với key URL path (production)", () => {
  const t = "2026-10-14";
  const items = [
    { qid: "k", qindex: 0, article: "cau-hoi/chua-doc.md", q: "q0", options: ["a", "b"], answer: 0, explain: "e" },
    { qid: "k", qindex: 1, article: "cau-hoi/da-doc.md", q: "q1", options: ["a", "b"], answer: 0, explain: "e" },
  ];
  // read key dạng URL path như loader.js ghi (location.pathname)
  const read = { "/cau-hoi/da-doc/": { n: 1 } };
  const out = OT.dueQuizItems(items, {}, t, { qNew: 2, read });
  assert.equal(out[0].article, "cau-hoi/da-doc.md");
});
