/* Kiểm thử hàm thuần của công cụ sơ đồ lập luận (không cần DOM). */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const src = fs.readFileSync(path.join(__dirname, "../../docs/assets/js/so-do-lap-luan.js"), "utf8");
const factory = new Function("module", "exports", "self", src + "\nreturn module.exports;");
const api = factory({ exports: {} }, {}, {});

function samplePassage() {
  return {
    id: "sodo-t",
    do_kho: 2,
    cau: [
      { id: "c1", nd: "Học sớm giúp trẻ đỡ vất vả." },
      { id: "c2", nd: "Chị Lan đang tìm lớp vẽ." },
      { id: "c3", nd: "Nên cho trẻ học sớm." },
      { id: "c4", nd: "Trẻ nhỏ tiếp thu nhanh." },
    ],
    dap_an: [
      { cau: "c1", vai_tro: "tien-de", ho_tro: ["c3"] },
      { cau: "c2", vai_tro: "khong-lien-quan" },
      { cau: "c3", vai_tro: "ket-luan" },
      { cau: "c4", vai_tro: "gia-dinh-ngam", ho_tro: ["c3"] },
    ],
    ghi_chu_tranh_cai: "c1 là tiền đề yếu nhưng vẫn là tiền đề.",
  };
}

test("splitItems: tách câu trong đoạn văn và ứng viên giả định ngầm", () => {
  const parts = api.splitItems(samplePassage());
  assert.deepEqual(parts.visible.map((c) => c.id), ["c1", "c2", "c3"]);
  assert.deepEqual(parts.implicit.map((c) => c.id), ["c4"]);
  assert.equal(parts.gold.c3, "ket-luan");
});

test("disputedIds: trích id câu tranh cãi từ ghi chú", () => {
  assert.deepEqual(api.disputedIds(samplePassage()), ["c1"]);
  assert.deepEqual(api.disputedIds({}), []);
});

test("grade: đúng hết cho điểm tối đa", () => {
  const res = api.grade({ c1: "tien-de", c2: "khong-lien-quan", c3: "ket-luan", c4: "gia-dinh-ngam" }, samplePassage());
  assert.equal(res.correct, 4);
  assert.equal(res.total, 4);
  assert.equal(res.note, null);
});

test("grade: sai một câu thường bị trừ điểm", () => {
  const res = api.grade({ c1: "tien-de", c2: "tien-de", c3: "ket-luan", c4: "gia-dinh-ngam" }, samplePassage());
  assert.equal(res.correct, 3);
  const c2 = res.perItem.find((p) => p.id === "c2");
  assert.equal(c2.correct, false);
});

test("grade: sai ở điểm tranh cãi vẫn tính đúng và hiện ghi chú", () => {
  const res = api.grade({ c1: "khong-lien-quan", c2: "khong-lien-quan", c3: "ket-luan", c4: "gia-dinh-ngam" }, samplePassage());
  const c1 = res.perItem.find((p) => p.id === "c1");
  assert.equal(c1.correct, true, "c1 tranh cãi: gán khác vẫn đúng");
  assert.equal(c1.disputed, true);
  assert.ok(res.note, "phải hiện ghi chú tranh cãi");
  assert.equal(res.correct, 4);
});

test("wrapLabel: ngắt dòng, tối đa 3 dòng", () => {
  const lines = api.wrapLabel("một câu rất dài cần được ngắt thành nhiều dòng nhỏ cho vừa hộp", 20);
  assert.ok(lines.length <= 3);
  assert.ok(lines.every((l) => l.length <= 24));
});

const VALID_ROLES = ["tien-de", "ket-luan", "gia-dinh-ngam", "khong-lien-quan"];

test("ngân hàng sơ đồ hợp lệ: 30 đoạn, 10/10/10, mỗi đoạn 1 kết luận + 1 câu nhiễu", () => {
  const data = JSON.parse(fs.readFileSync(path.join(__dirname, "../../docs/assets/data/lap-luan.json"), "utf8"));
  assert.equal(data.passages.length, 30);
  const byLevel = { 1: 0, 2: 0, 3: 0 };
  for (const p of data.passages) {
    byLevel[p.do_kho] = (byLevel[p.do_kho] || 0) + 1;
    const ids = new Set(p.cau.map((c) => c.id));
    const roles = {};
    for (const a of p.dap_an) {
      assert.ok(ids.has(a.cau), `${p.id}: dap_an trỏ câu không tồn tại (${a.cau})`);
      assert.ok(VALID_ROLES.includes(a.vai_tro), `${p.id}: vai trò lạ (${a.vai_tro})`);
      assert.ok(!roles[a.cau], `${p.id}: câu ${a.cau} gán 2 lần`);
      roles[a.cau] = a.vai_tro;
      for (const t of a.ho_tro || []) assert.ok(ids.has(t), `${p.id}: ho_tro trỏ câu lạ (${t})`);
    }
    assert.deepEqual(Object.keys(roles).sort(), [...ids].sort(), `${p.id}: mọi câu phải có vai trò`);
    const concl = p.dap_an.filter((a) => a.vai_tro === "ket-luan");
    assert.equal(concl.length, 1, `${p.id}: phải có đúng 1 kết luận`);
    assert.ok(!concl[0].ho_tro, `${p.id}: kết luận không được hỗ trợ câu khác`);
    const noise = p.dap_an.filter((a) => a.vai_tro === "khong-lien-quan");
    assert.equal(noise.length, 1, `${p.id}: phải có đúng 1 câu nhiễu`);
    assert.ok(!noise[0].ho_tro, `${p.id}: câu nhiễu không có cạnh đi ra`);
    // Đồ thị hỗ trợ không chu trình.
    const adj = {};
    p.dap_an.forEach((a) => ((a.ho_tro || []).forEach((t) => ((adj[a.cau] = adj[a.cau] || []).push(t)))));
    const state = {};
    let cyclic = false;
    function visit(n) {
      if (cyclic || state[n] === 2) return;
      if (state[n] === 1) {
        cyclic = true;
        return;
      }
      state[n] = 1;
      (adj[n] || []).forEach(visit);
      state[n] = 2;
    }
    // thăm từ mọi nút để chắc không có chu trình ở thành phần rời
    Object.keys(adj).forEach((n) => visit(n));
    assert.equal(cyclic, false, `${p.id}: đồ thị hỗ trợ có chu trình`);
    if (p.ghi_chu_tranh_cai) {
      assert.ok(/\bc\d+\b/.test(p.ghi_chu_tranh_cai), `${p.id}: ghi chú tranh cãi phải nêu id câu`);
    }
  }
  assert.deepEqual(byLevel, { 1: 10, 2: 10, 3: 10 });
});
