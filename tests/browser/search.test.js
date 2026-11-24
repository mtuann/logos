/* Tìm kiếm có dấu và không dấu: dựng chỉ mục lunr giống Material (trường title được
 * nhân trọng số, pipeline rỗng, cùng separator) từ search_index.json đã build, cộng bước bỏ dấu của worker
 * docs/assets/js/search-worker.js (đợt 4.5): mỗi từ có dấu được ghi thêm dạng không dấu. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const lunr = require("lunr");
const { SITE } = require("./helpers");

const data = JSON.parse(fs.readFileSync(path.join(SITE, "search/search_index.json"), "utf8"));
lunr.tokenizer.separator = new RegExp(data.config.separator);
const strip = (s) => s.replace(/<[^>]+>/g, " ");
const WORKER = fs.readFileSync(path.join(__dirname, "../../docs/assets/js/search-worker.js"), "utf8");
// Lấy đúng hai hàm boDau và ozBoDau từ worker, để kiểm thử chạy cùng mã với trình duyệt.
const { boDau, ozBoDau } = new Function(
  WORKER.slice(WORKER.indexOf("  function boDau"), WORKER.indexOf("  lunr.Pipeline.registerFunction")) +
  "return { boDau, ozBoDau };")();
lunr.Pipeline.registerFunction(ozBoDau, "ozBoDau");
const index = lunr(function () {
  this.pipeline.reset();
  this.searchPipeline.reset();
  this.pipeline.add(ozBoDau);
  this.ref("location");
  this.field("title", { boost: 1e3 });
  this.field("text");
  // Như worker (đợt 7.1.3): mục đại diện cả trang thêm chữ của địa chỉ trang vào tiêu đề.
  const theoDiaChi = (loc) => (loc.includes("#") ? "" : " " + ((loc.match(/([^\/]+)\/$/) || [, ""])[1]).replace(/-/g, " "));
  data.docs.forEach((d) => this.add({ location: d.location, title: strip(d.title) + theoDiaChi(d.location), text: strip(d.text) }));
});

function topPages(q, n = 5) {
  const pages = [];
  for (const r of index.search(q.split(/\s+/).map((t) => "+" + t).join(" "))) {
    const p = r.ref.split("#")[0];
    if (!pages.includes(p)) pages.push(p);
    if (pages.length >= n) break;
  }
  return pages;
}

const CASES = [
  ["tâm trí", "cau-hoi/tam-tri-va-ai/"],
  ["tam tri", "cau-hoi/tam-tri-va-ai/"],
  ["căn phòng tiếng trung", "cau-hoi/tam-tri-va-ai/"],
  ["can phong tieng trung", "cau-hoi/tam-tri-va-ai/"],
  ["tự do ý chí", "cau-hoi/tu-do-y-chi/"],
  ["tu do y chi", "cau-hoi/tu-do-y-chi/"],
  ["tương thích luận", "cau-hoi/tu-do-y-chi/"],
  ["tuong thich luan", "cau-hoi/tu-do-y-chi/"],
  ["gettier", "cau-hoi/tri-thuc/"],
  // Đợt 4.5: chỉ mục thôi có bản sao không dấu, nên từ không dấu sẵn (Gettier, tri…) không còn được đếm hai lần;
  // "tri thuc" từ hạng 5 xuống hạng 6 trong mô hình này (bằng đúng hạng của "tri thức"). Trên Chromium với Material,
  // 5 kết quả đầu như bản cũ (đo ngày 5/11/2026, ban-giao/nhat-ky-dot-4.md).
  ["tri thuc", "cau-hoi/tri-thuc/", 6],
  ["nguy bien", "cong-cu/nguy-bien/"],
  ["người rơm", "cong-cu/nguy-bien/"],
  ["nguoi rom", "cong-cu/nguy-bien/"],
  ["suy dien", "cong-cu/suy-dien/"],
  ["quy nap", "cong-cu/quy-nap/"],
  ["gia dinh ngam", "cong-cu/gia-dinh-ngam/"],
  ["dao duc hoc", null],
];

test("chỉ mục không còn bản sao không dấu (bỏ dấu ở trình duyệt)", () => {
  assert.ok(!data.docs.some((d) => /oz-noaccent/.test(d.text) || /oz-noaccent/.test(d.title)));
  assert.deepEqual(data.config.pipeline, []);
  assert.equal(boDau("Đạo đức học, Tương thích luận"), "Dao duc hoc, Tuong thich luan");
  assert.match(WORKER, /importScripts\("\.\.\/javascripts\/workers\/search\.[0-9a-f]+\.min\.js"\)/);
  const material = WORKER.match(/workers\/(search\.[0-9a-f]+\.min\.js)/)[1];
  assert.ok(fs.existsSync(path.join(SITE, "assets/javascripts/workers", material)), `thiếu worker của Material: ${material}`);
});

test("trang Dòng thời gian và Sơ đồ ảnh hưởng: chỉ mục không có chữ SVG dính liền", () => {
  const t = data.docs.filter((d) => /^lich-su\/(dong-thoi-gian|so-do-anh-huong)\//.test(d.location)).map((d) => d.text).join(" ");
  assert.ok(t.length > 0);
  assert.ok(!/SocratesHy Lạp|600 TCN400 TCN/.test(t), "còn chữ SVG trong chỉ mục");
});

for (const [q, want, n = 5] of CASES) {
  test(`tìm "${q}"`, () => {
    const top = topPages(q, n);
    if (want === null) assert.ok(top.length > 0, "không có kết quả");
    else assert.ok(top.includes(want), `${want} không nằm trong ${n} kết quả đầu: ${top.join(", ")}`);
  });
}

for (const [a, b] of [["tâm trí", "tam tri"], ["tương thích luận", "tuong thich luan"], ["căn phòng tiếng trung",
  "can phong tieng trung"], ["người rơm", "nguoi rom"], ["tri thức", "tri thuc"]]) {
  test(`kết quả đầu của "${a}" nằm trong 5 kết quả đầu của "${b}"`, () => {
    assert.ok(topPages(b, 5).includes(topPages(a, 1)[0]), `${topPages(a, 1)[0]} / ${topPages(b, 5).join(", ")}`);
  });
}

/* Đợt 6.1 (quyết định 38) và 7.1.3: Material thêm `*` cuối mọi từ của câu truy vấn, và lunr giữ `*` trong chữ của từ
 * (cờ wildcard = 0). Mô hình đi đúng đường ấy: câu "từ* từ*" qua QueryParser, mọi từ REQUIRED (ozBatBuoc); có sửa thì
 * áp ozBoSao (từ không phải từ cuối và từ cuối ≤ 2 chữ cái khớp nguyên từ) và ozNguyenTu (cộng điểm nguyên từ cuối).
 * (Mô hình cũ của 6.1 đặt cờ wildcard nên không thấy rằng bước ozTuNgan chưa từng có tác dụng trên trình duyệt.) */
const { ozBoSao, ozNguyenTu } = new Function("lunr",
  WORKER.slice(WORKER.indexOf("  function ozBatBuoc"), WORKER.indexOf("  lunr.Index.prototype.search")) +
  "return { ozBoSao, ozNguyenTu };")(lunr);
function truyVan(q, coSua) {
  const s = q.split(/\s+/).map((t) => t + "*").join(" ");
  return (qq) => {
    new lunr.QueryParser(s, qq).parse();
    for (const c of qq.clauses) c.presence = lunr.Query.presence.REQUIRED;
    if (coSua) { ozBoSao(qq.clauses); ozNguyenTu(qq); }
  };
}
function hangMaterial(q, want, coSua) {
  const pages = [];
  for (const r of index.query(truyVan(q, coSua))) { const p = r.ref.split("#")[0]; if (!pages.includes(p)) pages.push(p); }
  return pages.indexOf(want) + 1 || Infinity;
}
const CASES_6 = [...CASES.filter(([, w]) => w), ["y nghia song", "cau-hoi/y-nghia-song/"],
  ["tu do ngon luan", "cau-hoi/tu-do-ngon-luan/"], ["cong ly", "cau-hoi/cong-ly/"], ["cai chet", "cau-hoi/cai-chet/"]];
// Mô hình không có bước tính lại điểm và gom theo trang của Material: "tri thuc" hạng 7 ở đây, hạng 4 trên Chromium
// (tests/real/search.test.js giữ ngưỡng 5 kết quả đầu).
const NGUONG_MO_HINH = { "tri thuc": 7 };
for (const [q, want] of CASES_6) {
  const n = NGUONG_MO_HINH[q] || 5;
  test(`7.1.3: "${q}" nằm trong ${n} kết quả đầu với câu truy vấn kiểu Material`, () => {
    assert.ok(hangMaterial(q, want, true) <= n, `${q}: ${hangMaterial(q, want, false)} → ${hangMaterial(q, want, true)}`);
  });
}
test("7.1.3: chỉ từ cuối giữ *, trừ khi ≤ 2 chữ cái; từ cuối có thêm mệnh đề nguyên từ", () => {
  const q = new lunr.Query(["title", "text"]);
  new lunr.QueryParser("tri* thuc*", q).parse();
  ozBoSao(q.clauses);
  assert.deepEqual(q.clauses.map((c) => c.term), ["tri", "thuc*"]);
  const q2 = new lunr.Query(["title", "text"]);
  new lunr.QueryParser("tu* do* y*", q2).parse();
  ozBoSao(q2.clauses);
  assert.deepEqual(q2.clauses.map((c) => c.term), ["tu", "do", "y"]);
  ozNguyenTu(q);
  assert.equal(q.clauses.length, 3);
  assert.equal(q.clauses[2].term, "thuc");
  assert.equal(q.clauses[2].presence, lunr.Query.presence.OPTIONAL);
  assert.ok(hangMaterial("tu do y chi", "cau-hoi/tu-do-y-chi/", true) < hangMaterial("tu do y chi", "cau-hoi/tu-do-y-chi/", false));
  assert.ok(hangMaterial("tri thuc", "cau-hoi/tri-thuc/", true) < hangMaterial("tri thuc", "cau-hoi/tri-thuc/", false));
});
