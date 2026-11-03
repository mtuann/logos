/* Tìm kiếm có dấu và không dấu: dựng chỉ mục lunr giống Material (trường title được
 * nhân trọng số, pipeline rỗng, cùng separator) từ search_index.json đã build. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const lunr = require("lunr");
const { SITE } = require("./helpers");

const data = JSON.parse(fs.readFileSync(path.join(SITE, "search/search_index.json"), "utf8"));
lunr.tokenizer.separator = new RegExp(data.config.separator);
const strip = (s) => s.replace(/<[^>]+>/g, " ");
const index = lunr(function () {
  this.pipeline.reset();
  this.searchPipeline.reset();
  this.ref("location");
  this.field("title", { boost: 1e3 });
  this.field("text");
  data.docs.forEach((d) => this.add({ location: d.location, title: strip(d.title), text: strip(d.text) }));
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
  ["tri thuc", "cau-hoi/tri-thuc/"],
  ["nguy bien", "cong-cu/nguy-bien/"],
  ["người rơm", "cong-cu/nguy-bien/"],
  ["nguoi rom", "cong-cu/nguy-bien/"],
  ["suy dien", "cong-cu/suy-dien/"],
  ["quy nap", "cong-cu/quy-nap/"],
  ["gia dinh ngam", "cong-cu/gia-dinh-ngam/"],
  ["dao duc hoc", null],
];

test("chỉ mục có bản không dấu", () => {
  assert.ok(data.docs.some((d) => /oz-noaccent/.test(d.text)));
  assert.deepEqual(data.config.pipeline, []);
});

for (const [q, want] of CASES) {
  test(`tìm "${q}"`, () => {
    const top = topPages(q);
    if (want === null) assert.ok(top.length > 0, "không có kết quả");
    else assert.ok(top.includes(want), `${want} không nằm trong 5 kết quả đầu: ${top.join(", ")}`);
  });
}
