/* Kiểm thử hàm thuần addJournalEntry (progress.js) và groupEntries (nhat-ky.js). */
const test = require("node:test");
const assert = require("node:assert/strict");
const P = require("../../docs/assets/js/progress.js");
const NK = require("../../docs/assets/js/nhat-ky.js");

test("addJournalEntry: thêm mới vào ngày chưa có", () => {
  const s1 = P.addJournalEntry(P.emptyState(), "2026-10-13", "21:30", "Hôm nay đọc về hoài nghi luận.");
  assert.deepEqual(s1.journal["2026-10-13"], [{ t: "21:30", text: "Hôm nay đọc về hoài nghi luận." }]);
});

test("addJournalEntry: nhiều entry cùng ngày giữ đúng thứ tự", () => {
  let s = P.emptyState();
  s = P.addJournalEntry(s, "2026-10-13", "09:00", "Sáng");
  s = P.addJournalEntry(s, "2026-10-13", "21:00", "Tối");
  s = P.addJournalEntry(s, "2026-10-12", "10:00", "Hôm qua");
  assert.equal(s.journal["2026-10-13"].length, 2);
  assert.equal(s.journal["2026-10-13"][0].t, "09:00");
  assert.equal(s.journal["2026-10-13"][1].text, "Tối");
  assert.equal(s.journal["2026-10-12"][0].text, "Hôm qua");
});

test("addJournalEntry: cắt text quá 2000 ký tự", () => {
  const s = P.addJournalEntry(P.emptyState(), "2026-10-13", "12:00", "x".repeat(2500));
  assert.equal(s.journal["2026-10-13"][0].text.length, 2000);
  const s2 = P.addJournalEntry(P.emptyState(), "2026-10-13", "12:00", "y".repeat(2000));
  assert.equal(s2.journal["2026-10-13"][0].text.length, 2000, "đúng 2000 ký tự thì giữ nguyên");
});

test("addJournalEntry: trim text hai đầu", () => {
  const s = P.addJournalEntry(P.emptyState(), "2026-10-13", "12:00", "  hello\n ");
  assert.equal(s.journal["2026-10-13"][0].text, "hello");
});

test("addJournalEntry: không sửa state gốc", () => {
  const s0 = P.emptyState();
  const s1 = P.addJournalEntry(s0, "2026-10-13", "12:00", "abc");
  assert.deepEqual(s0.journal, {}, "state gốc phải giữ nguyên");
  assert.notEqual(s1, s0);
  s1.journal["2026-10-13"].push({ t: "13:00", text: "x" });
  assert.deepEqual(s0.journal, {}, "đẩy thêm vào state mới không ảnh hưởng state gốc");
});

test("addJournalEntry: hoạt động trên state thô thiếu khóa journal", () => {
  const s = P.addJournalEntry({ v: 1 }, "2026-10-13", "12:00", "abc");
  assert.equal(s.journal["2026-10-13"][0].text, "abc");
  const sNull = P.addJournalEntry(null, "2026-10-13", "12:00", "abc");
  assert.equal(sNull.journal["2026-10-13"][0].t, "12:00");
});

test("addJournalEntry: text null/undefined thành chuỗi rỗng", () => {
  const s1 = P.addJournalEntry(P.emptyState(), "2026-10-13", "12:00", null);
  assert.equal(s1.journal["2026-10-13"][0].text, "");
  const s2 = P.addJournalEntry(P.emptyState(), "2026-10-13", "12:00", undefined);
  assert.equal(s2.journal["2026-10-13"][0].text, "");
});

test("addJournalEntry: xuất hiện trong export của progress.js", () => {
  assert.equal(typeof P.addJournalEntry, "function");
});

test("groupEntries: ngày mới nhất trước, gộp entry tay và dòng tự động", () => {
  const state = {
    journal: { "2026-10-12": [{ t: "08:00", text: "a" }] },
    days: { "2026-10-13": { n: 12, c: 9 } },
    read: { "/x/": "2026-10-13", "/y/": "2026-10-13", "/z/": "2026-10-11" },
  };
  const g = NK.groupEntries(state);
  assert.equal(g.length, 3, "3 ngày có hoạt động");
  assert.equal(g[0].date, "2026-10-13", "ngày mới nhất trước");
  assert.deepEqual(g[0].entries, []);
  assert.ok(g[0].auto.some((l) => l.includes("12 câu")), "dòng trả lời câu: " + g[0].auto);
  assert.ok(g[0].auto.some((l) => l.includes("2 bài")), "dòng mở bài: " + g[0].auto);
  assert.equal(g[1].date, "2026-10-12");
  assert.equal(g[1].entries[0].text, "a");
  assert.deepEqual(g[1].auto, []);
  assert.equal(g[2].date, "2026-10-11");
  assert.ok(g[2].auto.some((l) => l.includes("1 bài")));
});

test("groupEntries: state rỗng → mảng rỗng, không crash", () => {
  assert.deepEqual(NK.groupEntries(null), []);
  assert.deepEqual(NK.groupEntries({}), []);
  assert.deepEqual(NK.groupEntries(P.emptyState()), []);
});

test("fmtDate: định dạng ngày Việt Nam", () => {
  assert.equal(NK.fmtDate("2026-10-13"), "13/10/2026");
  assert.equal(NK.fmtDate("abc"), "abc");
  assert.equal(NK.fmtDate(""), "");
});

test("addJournalEntry: trim về 365 ngày gần nhất", () => {
  let s = P.emptyState();
  const base = new Date(2020, 0, 1);
  for (let i = 0; i < 400; i++) {
    const dt = new Date(base.getTime() + i * 86400000);
    const ds = dt.toISOString().slice(0, 10);
    s = P.addJournalEntry(s, ds, "09:00", "entry " + i);
  }
  const keys = Object.keys(s.journal);
  assert.equal(keys.length, 365);
  assert.ok(!keys.includes("2020-01-01"), "ngày cũ nhất phải bị trim");
  assert.ok(keys.includes("2021-02-03"), "ngày mới nhất phải còn");
});
