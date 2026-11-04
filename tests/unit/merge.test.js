const test = require("node:test");
const assert = require("node:assert/strict");
const M = require("../../docs/assets/js/merge.js");

/* Bộ sinh số ngẫu nhiên có hạt giống (tái lập được), cùng thuật toán với util.js. */
function rng(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const pad = (n) => (n < 10 ? "0" : "") + n;
function randDate(rand) {
  return `2026-${pad(1 + Math.floor(rand() * 12))}-${pad(1 + Math.floor(rand() * 28))}`;
}
function pick(rand, arr) {
  return arr[Math.floor(rand() * arr.length)];
}

function randCounters(rand, keys, withLast) {
  const out = {};
  const n = Math.floor(rand() * 4);
  for (let i = 0; i < n; i++) {
    const k = pick(rand, keys);
    const cur = out[k] || { n: 0, c: 0 };
    const addN = 1 + Math.floor(rand() * 5);
    out[k] = { n: cur.n + addN, c: cur.c + Math.floor(rand() * (addN + 1)) };
    if (withLast) out[k].last = randDate(rand);
  }
  return out;
}

function randState(rand) {
  const skills = {};
  for (const sk of ["argument", "fallacy", "logic", "terms"]) {
    if (rand() < 0.6) {
      skills[sk] = {
        ema: Math.round(rand() * 1000) / 1000,
        n: 1 + Math.floor(rand() * 40),
        last: randDate(rand),
        days: randCounters(rand, ["2026-10-01", "2026-10-02", "2026-10-03"], false),
      };
    }
  }
  const quizzes = {};
  for (const q of ["mind-1", "arg-2", "fal-3"]) {
    if (rand() < 0.5) {
      quizzes[q] = {
        best: Math.floor(rand() * 6),
        total: rand() < 0.2 ? 6 : 5, // thỉnh thoảng lệch total để test xung đột
        tries: 1 + Math.floor(rand() * 4),
        last: randDate(rand),
      };
    }
  }
  const cards = {};
  for (const c of ["t1", "t2", "t3", "t4"]) {
    if (rand() < 0.5) {
      cards[c] = { box: 1 + Math.floor(rand() * 5), due: randDate(rand), intro: randDate(rand), last: randDate(rand) };
    }
  }
  return {
    v: 1,
    skills,
    days: randCounters(rand, ["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04"], false),
    quizzes,
    read: rand() < 0.5 ? { "/a/": "2026-10-01", "/b/": "2026-10-03" } : { "/b/": "2026-10-02" },
    cards,
    items: randCounters(rand, ["fallacy:f1", "logic:l2"], true),
    journal: {},
    imports: [],
  };
}

test("validateBackup từ chối file lạ, chấp nhận file đúng", () => {
  assert.equal(M.validateBackup(null).ok, false);
  assert.equal(M.validateBackup("x").ok, false);
  assert.equal(M.validateBackup({ app: "psyche-zero", state: {} }).ok, false);
  assert.equal(M.validateBackup({ app: "logos-zero" }).ok, false);
  const v = M.validateBackup({ app: "logos", deviceId: "d1", exported: "2026-10-13T00:00:00Z", state: { v: 1 } });
  assert.equal(v.ok, true);
  assert.deepEqual(v.meta, { deviceId: "d1", exportedAt: "2026-10-13T00:00:00Z" });
});

test("validateBackup nhận bản sao lưu xuất từ logos-zero (chuyển tiến độ sang site mới)", () => {
  assert.equal(M.validateBackup({ app: "logos-zero", deviceId: "d0", state: { v: 1 } }).ok, true);
});

test("mergeStates không sửa đầu vào", () => {
  const rand = rng(5);
  const a = randState(rand), b = randState(rand);
  const fa = JSON.stringify(a), fb = JSON.stringify(b);
  M.mergeStates(a, b, { deviceId: "d", exportedAt: "e" });
  assert.equal(JSON.stringify(a), fa);
  assert.equal(JSON.stringify(b), fb);
});

test("mergeStates: một bên trống thì giữ nguyên bên kia", () => {
  const rand = rng(1);
  const a = randState(rand);
  const m = M.mergeStates(a, {}, { deviceId: "d2", exportedAt: "e2" });
  assert.deepEqual(m.skills, a.skills);
  assert.deepEqual(m.days, a.days);
  assert.deepEqual(m.read, a.read);
  assert.deepEqual(m.cards, a.cards);
  assert.equal(m.imports.length, 1);
});

test("P1 — nhập lại cùng file là no-op (không nhân đôi)", () => {
  const rand = rng(42);
  for (let i = 0; i < 300; i++) {
    const a = randState(rand);
    const b = randState(rand);
    const meta = { deviceId: "dev-" + i, exportedAt: "2026-10-13T10:00:00Z" };
    const once = M.mergeStates(a, b, meta);
    const twice = M.mergeStates(once, b, meta);
    assert.deepEqual(twice, once, "lần lặp " + i);
  }
});

test("P2 — giao hoán: merge(a,b) deep-equal merge(b,a)", () => {
  const rand = rng(7);
  for (let i = 0; i < 300; i++) {
    const a = randState(rand);
    const b = randState(rand);
    const meta = { deviceId: "d", exportedAt: "e" + i };
    assert.deepEqual(M.mergeStates(a, b, meta), M.mergeStates(b, a, meta), "cặp " + i);
  }
});

test("P3 — không mất dữ liệu, đúng quy tắc từng mục", () => {
  const a = {
    v: 1,
    skills: { fallacy: { ema: 0.8, n: 10, last: "2026-10-01", days: { "2026-10-01": { n: 10, c: 8 } } } },
    days: { "2026-10-01": { n: 10, c: 8 } },
    quizzes: { q1: { best: 3, total: 5, tries: 1, last: "2026-10-01" } },
    read: { "/a/": "2026-10-05" },
    cards: { t1: { box: 2, due: "2026-10-10", intro: "2026-10-01", last: "2026-10-02" } },
    items: { i1: { n: 4, c: 3, last: "2026-10-01" } },
    journal: {},
    imports: [],
  };
  const b = {
    v: 1,
    skills: {
      fallacy: { ema: 0.6, n: 10, last: "2026-10-03", days: { "2026-10-03": { n: 10, c: 6 } } },
      logic: { ema: 1, n: 5, last: "2026-10-03", days: {} },
    },
    days: { "2026-10-03": { n: 10, c: 6 } },
    quizzes: {
      q1: { best: 5, total: 5, tries: 2, last: "2026-10-03" },
      q2: { best: 2, total: 4, tries: 1, last: "2026-10-02" },
    },
    read: { "/a/": "2026-10-01", "/b/": "2026-10-02" },
    cards: {
      t1: { box: 3, due: "2026-10-12", intro: "2026-10-01", last: "2026-10-04" },
      t2: { box: 1, due: "2026-10-06", intro: "2026-10-03", last: "2026-10-03" },
    },
    items: { i1: { n: 2, c: 2, last: "2026-10-04" } },
    journal: {},
    imports: [],
  };
  const m = M.mergeStates(a, b, { deviceId: "d", exportedAt: "e" });
  assert.deepEqual(m.days["2026-10-01"], { n: 10, c: 8 });
  assert.deepEqual(m.days["2026-10-03"], { n: 10, c: 6 });
  assert.equal(m.skills.fallacy.n, 20);
  assert.equal(m.skills.fallacy.ema, 0.7);
  assert.equal(m.skills.fallacy.last, "2026-10-03");
  assert.ok(m.skills.logic, "skill chỉ bên b có được giữ");
  assert.deepEqual(m.quizzes.q1, { best: 5, total: 5, tries: 3, last: "2026-10-03" });
  assert.ok(m.quizzes.q2, "quiz chỉ bên b có được giữ");
  assert.equal(m.read["/a/"], "2026-10-01", "giữ ngày đọc sớm nhất");
  assert.equal(m.read["/b/"], "2026-10-02");
  assert.equal(m.cards.t1.box, 3, "thẻ giữ bản ôn gần nhất");
  assert.ok(m.cards.t2, "thẻ chỉ bên b có được giữ");
  assert.deepEqual(m.items.i1, { n: 6, c: 5, last: "2026-10-04" });
});

test("P4 — EMA gộp nằm giữa hai EMA đầu vào", () => {
  const rand = rng(99);
  for (let i = 0; i < 300; i++) {
    const a = randState(rand);
    const b = randState(rand);
    const m = M.mergeStates(a, b, { deviceId: "d", exportedAt: "e" + i });
    for (const k of Object.keys(m.skills)) {
      const ex = (a.skills[k] || {}).ema;
      const ey = (b.skills[k] || {}).ema;
      const e = m.skills[k].ema;
      if (ex === undefined) {
        assert.equal(e, ey);
        continue;
      }
      if (ey === undefined) {
        assert.equal(e, ex);
        continue;
      }
      assert.ok(e >= Math.min(ex, ey) - 1e-9 && e <= Math.max(ex, ey) + 1e-9, `ema ${k}: ${e} ngoài [${ex}, ${ey}]`);
    }
  }
});

test("previewMerge: phát hiện đã nhập, tóm tắt và xung đột", () => {
  const base = { v: 1, skills: {}, days: {}, quizzes: {}, read: {}, cards: {}, items: {}, journal: {}, imports: [] };
  const a = { ...base, quizzes: { q1: { best: 3, total: 5, tries: 1, last: "2026-10-01" } } };
  const b = {
    ...base,
    quizzes: { q1: { best: 4, total: 6, tries: 1, last: "2026-10-02" } },
    read: { "/x/": "2026-10-02" },
  };
  const meta = { deviceId: "d", exportedAt: "e" };
  const pv = M.previewMerge(a, b, meta);
  assert.equal(pv.alreadyImported, false);
  assert.ok(pv.summary.some((r) => r.section === "Bài quiz" && r.updated === 1));
  assert.ok(pv.summary.some((r) => r.section === "Bài đã đọc" && r.added === 1));
  assert.equal(pv.conflicts.length, 1);
  assert.ok(pv.conflicts[0].includes("q1"));
  assert.ok(pv.emaNote.length > 0);
  const pv2 = M.previewMerge(pv.merged, b, meta);
  assert.equal(pv2.alreadyImported, true, "nhập lại cùng file phải báo đã nhập");
});

test("_mergeJournal: union không mất entry, dedupe trùng", () => {
  const a = { "2026-10-13": [{ t: "09:00", text: "Suy nghĩ A" }] };
  const b = { "2026-10-13": [{ t: "10:00", text: "Suy nghĩ B" }] };
  const out = M._mergeJournal(a, b);
  assert.equal(out["2026-10-13"].length, 2);
  assert.deepEqual(out["2026-10-13"].map((e) => e.t), ["09:00", "10:00"]);
});

test("_mergeJournal: entry trùng (cùng giờ + text) chỉ giữ một", () => {
  const e = { t: "09:00", text: "Suy nghĩ A" };
  const out = M._mergeJournal({ d: [e] }, { d: [{ t: "09:00", text: "Suy nghĩ A" }] });
  assert.equal(out.d.length, 1);
});

test("_mergeJournal: khóa chỉ một bên có được giữ nguyên", () => {
  const out = M._mergeJournal({ d1: [{ t: "09:00", text: "A" }] }, { d2: [{ t: "10:00", text: "B" }] });
  assert.equal(out.d1.length, 1);
  assert.equal(out.d2.length, 1);
});

test("_mergeJournal: không sửa input gốc", () => {
  const a = { d: [{ t: "09:00", text: "A" }] };
  M._mergeJournal(a, { d: [{ t: "10:00", text: "B" }] });
  assert.equal(a.d.length, 1);
});
