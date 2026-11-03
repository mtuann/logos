const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const S = require("../../docs/assets/js/steelman.js");

const DOCS = path.join(__dirname, "../../docs");

test("10 preset, mỗi preset đủ trường và bài viết tồn tại", () => {
  assert.equal(S.PRESETS.length, 10);
  const ids = new Set();
  for (const p of S.PRESETS) {
    assert.ok(p.id && p.ten && p.bai && p.tinh_huong, JSON.stringify(p.id));
    assert.ok(!ids.has(p.id), "trùng id " + p.id);
    ids.add(p.id);
    assert.ok(fs.existsSync(path.join(DOCS, p.bai)), "bài viết không tồn tại: " + p.bai);
    assert.ok(Array.isArray(p.doi_lap) && p.doi_lap.length >= 2 && p.doi_lap.length <= 3, p.id);
    p.doi_lap.forEach((g) => assert.ok(g.trim().length > 10, p.id));
    for (const step of [1, 2, 3, 4]) assert.ok(p.mau[step] !== undefined, `${p.id} thiếu ví dụ bước ${step}`);
    assert.equal(p.mau[2].length, 3, p.id);
    p.mau[2].forEach((a) => assert.ok(a.trim().length >= 15, p.id));
    for (const step of [1, 3, 4]) assert.ok(p.mau[step].trim().length >= 20, `${p.id} b${step}`);
  }
});

test("presetById: tìm đúng, không có trả về null", () => {
  assert.equal(S.presetById("pha-thai").ten, "Phá thai");
  assert.equal(S.presetById("dan-chu").bai, "cau-hoi/dan-chu.md");
  assert.equal(S.presetById("khong-co"), null);
});

test("chuDeCua: ưu tiên preset, rồi đến chủ đề tự nhập", () => {
  assert.equal(S.chuDeCua({ presetId: "an-tu-hinh", chuDeRieng: "  x  " }), "Án tử hình");
  assert.equal(S.chuDeCua({ presetId: null, chuDeRieng: "  Có nên bỏ bài tập về nhà? " }), "Có nên bỏ bài tập về nhà?");
  assert.equal(S.chuDeCua({}), "");
});

test("examplesFor: ví dụ của chủ đề đứng đầu, xoay vòng được", () => {
  const e2 = S.examplesFor("pha-thai", 2);
  assert.equal(e2.length, 3, "1 ví dụ preset + 2 ví dụ chung");
  assert.equal(e2[0].chuDe, "Phá thai");
  assert.ok(Array.isArray(e2[0].noiDung) && e2[0].noiDung.length === 3);
  for (const step of [1, 3, 4]) {
    const e = S.examplesFor("tu-do-y-chi", step);
    assert.ok(e.length >= 3, `bước ${step}`);
    assert.equal(typeof e[0].noiDung, "string");
    assert.equal(e[0].chuDe, "Tự do ý chí");
  }
  // Chủ đề lạ / tự nhập: chỉ còn ví dụ chung.
  const g = S.examplesFor("khong-co", 1);
  assert.equal(g.length, 2);
  assert.ok(g.every((x) => typeof x.noiDung === "string"));
});

test("validateStep bước 0: phải chọn chủ đề hoặc tự nhập", () => {
  assert.match(S.validateStep(0, {}), /chủ đề/);
  assert.match(S.validateStep(0, { chuDeRieng: "   " }), /chủ đề/);
  assert.equal(S.validateStep(0, { presetId: "cai-chet" }), null);
  assert.equal(S.validateStep(0, { chuDeRieng: "Ăn chay?" }), null);
});

test("validateStep các bước 1–4: chặn câu trả lời quá ngắn", () => {
  const du = {
    b1: "x".repeat(30),
    b2a: "y".repeat(15),
    b2b: "y".repeat(15),
    b2c: "y".repeat(15),
    b3: "z".repeat(20),
    b4: "w".repeat(20),
  };
  for (const step of [1, 2, 3, 4]) assert.equal(S.validateStep(step, du), null, `bước ${step}`);
  assert.match(S.validateStep(1, { b1: "ngắn" }), /quá ngắn/);
  assert.match(S.validateStep(2, { ...du, b2b: "ngắn" }), /3 luận cứ/);
  assert.match(S.validateStep(3, { b3: "" }), /cụ thể/);
  assert.match(S.validateStep(4, { b4: "không" }), /đổi ý/);
  assert.match(S.validateStep(9, du), /không hợp lệ/);
});

test("buildSummary: đủ 4 phần, bản text chứa mọi nội dung", () => {
  const d = {
    presetId: "binh-dang",
    b1: "Phe cơ hội nói: " + "x".repeat(40),
    b2a: "Luận cứ một " + "a".repeat(20),
    b2b: "Luận cứ hai " + "b".repeat(20),
    b2c: "Luận cứ ba " + "c".repeat(20),
    b3: "Bằng chứng " + "d".repeat(20),
    b4: "Đổi ý nếu " + "e".repeat(20),
  };
  const s = S.buildSummary(d);
  assert.equal(s.chuDe, "Bình đẳng và bất bình đẳng");
  assert.equal(s.phan.length, 4);
  assert.deepEqual(
    s.phan.map((p) => p.tieuDe),
    ["Phe đối lập ở dạng mạnh nhất", "Ba luận cứ tốt nhất của họ", "Bằng chứng mạnh nhất họ viện dẫn", "Điều gì sẽ làm tôi đổi ý"]
  );
  assert.ok(Array.isArray(s.phan[1].noiDung) && s.phan[1].noiDung.length === 3);
  assert.match(s.phan[1].noiDung[0], /^1\. Luận cứ một/);
  for (const key of ["b1", "b2a", "b3", "b4"]) assert.ok(s.vanBan.includes(d[key].trim()), key);
  assert.match(s.vanBan, /LUẬN CỨ THÉP/);
  // Chủ đề tự nhập cũng lên tiêu đề.
  const s2 = S.buildSummary({ ...d, presetId: null, chuDeRieng: "Ăn chay" });
  assert.equal(s2.chuDe, "Ăn chay");
  assert.ok(s2.vanBan.includes("ĂN CHAY"));
});

test("STEPS và MIN_LEN: 4 bước, ngưỡng hợp lý", () => {
  assert.equal(S.STEPS.length, 4);
  S.STEPS.forEach((s) => assert.ok(s.tieuDe && s.goiY));
  assert.deepEqual(S.MIN_LEN, { 1: 30, 2: 15, 3: 20, 4: 20 });
});
