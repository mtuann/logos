/* Kiểm thử hàm thuần của công cụ thí nghiệm tư duy (không cần DOM). */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const src = fs.readFileSync(path.join(__dirname, "../../docs/assets/js/thi-nghiem.js"), "utf8");
const sandbox = { module: { exports: {} }, self: {} };
sandbox.window = undefined;
vm.createContext(sandbox);
// Giả lập môi trường CommonJS: module.exports được điền bởi UMD.
const factory = new Function("module", "exports", "self", src + "\nreturn module.exports;");
const api = factory(sandbox.module, sandbox.module.exports, sandbox.self);

const CHOICES = [
  { id: "a", nd: "Kéo cần gạt", lap_truong: "Hệ quả luận", giai_thich: "Ít chết hơn." },
  { id: "b", nd: "Không kéo", lap_truong: "Nghĩa vụ luận", giai_thich: "Không giết." },
];

test("surveyRows: ánh xạ đúng id sang nhãn lựa chọn", () => {
  const rows = api.surveyRows({ a: 63.4, b: 13.3, nguon: "PhilPapers" }, CHOICES);
  assert.equal(rows.length, 2);
  assert.equal(rows[0].nd, "Kéo cần gạt");
  assert.equal(rows[0].pct, 63.4);
  assert.equal(rows[1].nd, "Không kéo");
});

test("surveyRows: bỏ qua khóa không phải số (nguon) và id lạ", () => {
  const rows = api.surveyRows({ a: 50, z: 10, nguon: "X" }, CHOICES);
  assert.equal(rows.length, 1, "chỉ còn a");
});

test("surveyRows: trả null khi không có khảo sát", () => {
  assert.equal(api.surveyRows(null, CHOICES), null);
});

test("choiceById: tìm đúng lựa chọn", () => {
  assert.equal(api.choiceById(CHOICES, "b").lap_truong, "Nghĩa vụ luận");
  assert.equal(api.choiceById(CHOICES, "zzz"), null);
});

const EXPECTED_IDS = ["xe-dien", "cau-cau", "phong-tieng-trung", "may-trai-nghiem", "may-dich-chuyen", "tau-theseus", "gettier", "frankfurt"];
const EXPECTED_SURVEY = {
  "xe-dien": { a: 63.4, b: 13.3 },
  "cau-cau": { a: 22, b: 56 },
  "phong-tieng-trung": { a: 17.8, b: 67.1 },
  "may-trai-nghiem": { a: 13.3, b: 76.9 },
  "may-dich-chuyen": { a: 35.2, b: 40.1 },
};

test("ngân hàng thí nghiệm hợp lệ: 8 thí nghiệm, schema đầy đủ, steelman cân sức", () => {
  const data = JSON.parse(fs.readFileSync(path.join(__dirname, "../../docs/assets/data/thi-nghiem.json"), "utf8"));
  assert.deepEqual(data.experiments.map((e) => e.id).sort(), EXPECTED_IDS.slice().sort());
  for (const e of data.experiments) {
    for (const k of ["ten", "hoan_canh", "cau_hoi", "lua_chon", "phan_bien_manh_nhat", "nguon"]) {
      assert.ok(e[k], `${e.id}: thiếu trường ${k}`);
    }
    assert.ok(e.lua_chon.length >= 2 && e.lua_chon.length <= 3, `${e.id}: cần 2-3 lựa chọn`);
    for (const c of e.lua_chon) {
      for (const k of ["id", "nd", "lap_truong", "giai_thich"]) assert.ok(c[k], `${e.id}: lựa chọn thiếu ${k}`);
      assert.ok(!/bạn là/i.test(c.lap_truong + c.nd), `${e.id}: không gắn nhãn "bạn là…"`);
      const steel = e.phan_bien_manh_nhat[c.id];
      assert.ok(steel && steel.length > 100, `${e.id}/${c.id}: steelman quá ngắn hoặc thiếu`);
    }
    assert.ok(e.nguon.length > 0, `${e.id}: thiếu nguồn triết học`);
  }
});

test("số liệu khảo sát khớp PhilPapers 2020; Theseus/Gettier/Frankfurt null", () => {
  const data = JSON.parse(fs.readFileSync(path.join(__dirname, "../../docs/assets/data/thi-nghiem.json"), "utf8"));
  for (const e of data.experiments) {
    const s = e.so_lieu_khao_sat;
    if (EXPECTED_SURVEY[e.id]) {
      for (const [k, v] of Object.entries(EXPECTED_SURVEY[e.id])) {
        assert.equal(s[k], v, `${e.id}: số liệu ${k} sai (mong ${v})`);
      }
    } else {
      assert.equal(s, null, `${e.id}: phải null (chưa có khảo sát)`);
    }
  }
  const theseus = data.experiments.find((e) => e.id === "tau-theseus");
  // Không mượn số của câu khác (trước 22/10/2026 từng gán số "bản sắc cá nhân" cho các lựa chọn về con tàu).
  assert.equal(theseus.so_lieu_khao_sat, null);
  assert.match(theseus.ghi_chu_khao_sat, /không hỏi về con tàu Theseus/);
});
