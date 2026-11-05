/* Kiểm thử hàm thuần của the-di-chuot.js (đợt 4.7). */
const test = require("node:test");
const assert = require("node:assert/strict");
const T = require("../../docs/assets/js/the-di-chuot.js");

test("nhận ra link tới trang triết gia và mục từ điển", () => {
  assert.deepEqual(T.target("https://x.org/logos/triet-gia/kant/"), { kind: "triet-gia", id: "kant" });
  assert.deepEqual(T.target("https://x.org/logos/triet-gia/kant/#tac-pham"), { kind: "triet-gia", id: "kant" });
  assert.deepEqual(T.target("https://x.org/logos/them/tu-dien/#ac-than"), { kind: "thuat-ngu", id: "ac-than" });
  for (const u of ["https://x.org/logos/triet-gia/", "https://x.org/logos/them/tu-dien/", "https://x.org/logos/cau-hoi/tri-thuc/", "khong-phai-url"])
    assert.equal(T.target(u), null, u);
});

test("thẻ thoát ký tự HTML và có đủ trường", () => {
  const h = T.render("triet-gia", { name: "Kant", name_en: "Immanuel Kant", years: "1724–1804", school: "Cận đại", summary: "<b>x</b> & y" });
  assert.match(h, /Kant.*Immanuel Kant/);
  assert.match(h, /1724–1804 · Cận đại/);
  assert.match(h, /&lt;b&gt;x&lt;\/b&gt; &amp; y/);
  assert.doesNotMatch(T.render("triet-gia", { name: "Platon", name_en: "Platon", summary: "s" }), /\(Platon\)/);
  assert.match(T.render("thuat-ngu", { vi: "ác thần", en: "evil demon", def: "Định nghĩa" }), /ác thần.*evil demon.*Định nghĩa/);
});
