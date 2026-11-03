/* Kiểm thử luồng công cụ thí nghiệm tư duy trên jsdom — không cần build site.
 * Nạp core/util/thi-nghiem/progress vào jsdom; fetch ngân hàng được giả lập. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM, VirtualConsole } = require("jsdom");

const JS = path.join(__dirname, "../../docs/assets/js");
const settle = (ms = 60) => new Promise((r) => setTimeout(r, ms));

function mockBank() {
  return {
    experiments: [
      {
        id: "tn-1",
        ten: "Thí nghiệm mẫu",
        hoan_canh: "Tình huống tưởng tượng.",
        cau_hoi: "Bạn chọn gì?",
        lua_chon: [
          { id: "a", nd: "Chọn A", lap_truong: "Phe A", giai_thich: "Vì A tốt." },
          { id: "b", nd: "Chọn B", lap_truong: "Phe B", giai_thich: "Vì B tốt." },
        ],
        phan_bien_manh_nhat: { a: "Steelman chống A.", b: "Steelman chống B." },
        so_lieu_khao_sat: { a: 63.4, b: 13.3, nguon: "PhilPapers Survey 2020" },
        nguon: ["Tác giả (2020)"],
      },
      {
        id: "tn-2",
        ten: "Thí nghiệm không khảo sát",
        hoan_canh: "Tình huống khác.",
        cau_hoi: "Bạn chọn gì?",
        lua_chon: [
          { id: "a", nd: "Chọn A", lap_truong: "Phe A", giai_thich: "Vì A." },
          { id: "b", nd: "Chọn B", lap_truong: "Phe B", giai_thich: "Vì B." },
        ],
        phan_bien_manh_nhat: { a: "Steelman A.", b: "Steelman B." },
        so_lieu_khao_sat: null,
        nguon: ["Tác giả (2021)"],
      },
    ],
  };
}

function makePage() {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", (e) => errors.push(e.message || String(e)));
  vc.on("error", (e) => errors.push(String(e)));
  const dom = new JSDOM('<!DOCTYPE html><html><head></head><body><div class="oz-thi-nghiem"></div></body></html>', {
    url: "http://localhost/logos-zero/cong-cu/thi-nghiem-tu-duy/",
    runScripts: "dangerously",
    virtualConsole: vc,
    beforeParse(window) {
      window.fetch = () =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockBank()),
        });
      window.addEventListener("error", (e) => errors.push(e.message));
    },
  });
  const { window } = dom;
  for (const f of ["core.js", "util.js", "thi-nghiem.js", "progress.js"]) {
    window.eval(fs.readFileSync(path.join(JS, f), "utf8"));
  }
  // Thứ tự cố định cho test (bản thật vẫn xáo trộn).
  window.OZ.util.shuffle = (arr) => arr;
  return { window, document: window.document, errors };
}

async function until(fn, ms = 2000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    if (fn()) return true;
    await settle(20);
  }
  return false;
}

test("hiển thị thí nghiệm và các lựa chọn", async () => {
  const { document, errors, window } = makePage();
  await until(() => document.querySelector(".oz-thi-nghiem h3"));
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  assert.equal(document.querySelector(".oz-thi-nghiem").dataset.ozInit, "1");
  assert.match(document.querySelector(".oz-thi-nghiem h3").textContent, /Thí nghiệm/);
  assert.equal(document.querySelectorAll(".oz-thi-nghiem .oz-actions button").length, 2, "hai nút lựa chọn");
  window.close();
});

test("chọn đáp án: hiện steelman + thanh khảo sát, không chấm điểm", async () => {
  const { document, errors, window } = makePage();
  await until(() => document.querySelector(".oz-thi-nghiem h3"));
  const btns = document.querySelectorAll(".oz-thi-nghiem .oz-actions button");
  btns[0].click();
  await settle();
  const box = document.querySelector(".oz-thi-nghiem");
  // Steelman chống lại chính lựa chọn đã chọn.
  assert.match(box.textContent, /Steelman chống A/);
  // Thanh khảo sát với phần trăm đúng định dạng Việt Nam.
  const bars = box.querySelectorAll(".oz-tn__bar");
  assert.equal(bars.length, 2);
  assert.match(bars[0].textContent, /63,4%/);
  assert.match(box.textContent, /PhilPapers Survey 2020/);
  // Không có ngôn ngữ chấm điểm.
  assert.doesNotMatch(box.textContent, /điểm|đúng\/sai|chính xác/i);
  assert.deepEqual(errors, [], "lỗi JS trong luồng: " + errors.join("; "));
  window.close();
});

test("thí nghiệm không khảo sát: hiện thông báo thay vì thanh số liệu", async () => {
  const { document, errors, window } = makePage();
  await until(() => document.querySelector(".oz-thi-nghiem h3"));
  const next = async () => {
    const b = document.querySelector(".oz-thi-nghiem .oz-actions button");
    b.click();
    await settle();
  };
  await next(); // chọn đáp án ở thí nghiệm 1
  const nextBtn = [...document.querySelectorAll(".oz-thi-nghiem button")].find((b) =>
    /tiếp theo|kết thúc/.test(b.textContent)
  );
  nextBtn.click();
  await until(() => /Thí nghiệm 2\/2/.test(document.querySelector(".oz-thi-nghiem").textContent));
  const btns2 = document.querySelectorAll(".oz-thi-nghiem .oz-actions button");
  btns2[0].click();
  await settle();
  const box = document.querySelector(".oz-thi-nghiem");
  assert.match(box.textContent, /Chưa có khảo sát đáng tin cậy/);
  assert.equal(box.querySelectorAll(".oz-tn__bar").length, 0);
  assert.deepEqual(errors, [], "lỗi JS trong luồng: " + errors.join("; "));
  window.close();
});
