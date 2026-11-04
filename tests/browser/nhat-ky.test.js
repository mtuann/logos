/* Kiểm thử luồng nhật ký trên jsdom — không cần build site.
 * Nạp trực tiếp core/util/progress/nhat-ky vào jsdom rồi mô phỏng:
 * gõ text → bấm Lưu → kiểm tra entry hiện ra và localStorage có dữ liệu. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM, VirtualConsole } = require("jsdom");

const JS = path.join(__dirname, "../../docs/assets/js");
const settle = (ms = 60) => new Promise((r) => setTimeout(r, ms));

function makePage(storage) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", (e) => errors.push(e.message || String(e)));
  vc.on("error", (e) => errors.push(String(e)));
  const dom = new JSDOM('<!DOCTYPE html><html><head></head><body><div class="oz-nhat-ky"></div></body></html>', {
    url: "http://localhost/logos/them/nhat-ky/",
    runScripts: "dangerously",
    virtualConsole: vc,
    beforeParse(window) {
      window.confirm = () => true;
      window.addEventListener("error", (e) => errors.push(e.message));
      if (storage) window.localStorage.setItem("logos", JSON.stringify(storage));
    },
  });
  const { window } = dom;
  for (const f of ["core.js", "util.js", "progress.js", "nhat-ky.js"]) {
    window.eval(fs.readFileSync(path.join(JS, f), "utf8"));
  }
  return { window, document: window.document, errors };
}

function saveText(document, window, text) {
  const box = document.querySelector(".oz-nhat-ky");
  const area = box.querySelector("textarea");
  assert.ok(area, "thiếu textarea");
  area.value = text;
  box.querySelector("button").click(); // nút "Lưu"
}

test("mount: khởi tạo, có textarea và nút Lưu", async () => {
  const { document, errors, window } = makePage(null);
  await settle();
  assert.deepEqual(errors, [], "lỗi JS khi tải trang: " + errors.join("; "));
  const box = document.querySelector(".oz-nhat-ky");
  assert.equal(box.dataset.ozInit, "1", "nhat-ky chưa khởi tạo");
  assert.ok(box.querySelector("textarea"), "thiếu textarea");
  assert.equal(box.querySelector("button").textContent, "Lưu");
  assert.match(box.textContent, /Chưa có ghi chép nào/);
  window.close();
});

test("gõ text → Lưu → entry hiện ra, localStorage có dữ liệu, textarea trống", async () => {
  const { window, document, errors } = makePage(null);
  await settle();
  saveText(document, window, "Hôm nay tôi tự hỏi: biết là gì?");
  await settle();
  const P = window.OZ.progress;
  const d = P.today();
  const saved = JSON.parse(window.localStorage.getItem("logos"));
  assert.ok(saved.journal[d], "localStorage thiếu journal[" + d + "]");
  assert.equal(saved.journal[d].length, 1);
  assert.equal(saved.journal[d][0].text, "Hôm nay tôi tự hỏi: biết là gì?");
  assert.match(saved.journal[d][0].t, /^\d{2}:\d{2}$/, "giờ lưu sai định dạng HH:MM");
  const box = document.querySelector(".oz-nhat-ky");
  assert.ok(box.textContent.includes("Hôm nay tôi tự hỏi: biết là gì?"), "entry không hiện trên trang");
  assert.equal(box.querySelector("textarea").value, "", "textarea chưa được xóa sau khi lưu");
  assert.deepEqual(errors, [], "lỗi JS trong luồng: " + errors.join("; "));
  window.close();
});

test("HTML trong ghi chép bị escape, không render thành phần tử", async () => {
  const { window, document, errors } = makePage(null);
  await settle();
  saveText(document, window, "<b>in đậm?</b> <img src=x onerror=alert(1)>");
  await settle();
  const box = document.querySelector(".oz-nhat-ky");
  assert.equal(box.querySelector(".oz-journal-text b"), null, "thẻ b bị render");
  assert.equal(box.querySelector(".oz-journal-text img"), null, "thẻ img bị render");
  assert.ok(box.querySelector(".oz-journal-text").textContent.includes("<b>in đậm?</b>"), "text gốc bị mất");
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  window.close();
});

test("bấm Lưu khi trống → nhắc viết, không tạo entry", async () => {
  const { window, document, errors } = makePage(null);
  await settle();
  const box = document.querySelector(".oz-nhat-ky");
  box.querySelector("button").click();
  await settle(120); // U.live dùng setTimeout 30ms
  assert.match(document.querySelector(".oz-live").textContent, /vài chữ/);
  const saved = JSON.parse(window.localStorage.getItem("logos") || "{}");
  assert.deepEqual(saved.journal || {}, {}, "đã tạo entry rỗng");
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  window.close();
});

test("xóa entry sau khi confirm", async () => {
  const d = "2026-10-13";
  const storage = { v: 1, journal: { [d]: [{ t: "09:00", text: "ghi chép cũ" }] } };
  const { window, document, errors } = makePage(storage);
  await settle();
  const box = document.querySelector(".oz-nhat-ky");
  assert.ok(box.textContent.includes("ghi chép cũ"), "entry seed không hiện");
  const del = box.querySelector(".oz-journal-del");
  assert.ok(del, "thiếu nút xóa");
  del.click(); // confirm() đã stub → true
  await settle();
  const saved = JSON.parse(window.localStorage.getItem("logos"));
  assert.deepEqual(saved.journal[d], [], "entry chưa bị xóa khỏi state");
  assert.ok(!box.textContent.includes("ghi chép cũ"), "entry vẫn hiện trên trang");
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  window.close();
});

test("dòng thời gian tự động từ days/read, gộp dưới entry tay cùng ngày", async () => {
  const storage = {
    v: 1,
    days: { "2026-10-13": { n: 12, c: 9 } },
    read: { "/a/": "2026-10-13", "/b/": "2026-10-13" },
    journal: { "2026-10-13": [{ t: "20:00", text: "tay" }] },
  };
  const { window, document, errors } = makePage(storage);
  await settle();
  const box = document.querySelector(".oz-nhat-ky");
  assert.match(box.textContent, /Đã trả lời 12 câu \(đúng 9\)/);
  assert.match(box.textContent, /Đã mở 2 bài/);
  assert.ok(box.textContent.includes("tay"), "entry tay bị mất");
  const auto = box.querySelector(".oz-journal-day").textContent;
  assert.ok(auto.indexOf("tay") > -1 && auto.indexOf("Đã trả lời") > -1, "thiếu một trong hai loại dòng");
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  window.close();
});
