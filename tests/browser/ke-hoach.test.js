/* Kiểm thử luồng kế hoạch học + biểu đồ trên jsdom — không cần build site.
 * Nạp trực tiếp core/util/progress/ke-hoach/bieu-do vào jsdom rồi kiểm tra render. */
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
  const dom = new JSDOM(
    '<!DOCTYPE html><html><head></head><body><div class="oz-ke-hoach"></div><div class="oz-bieu-do"></div></body></html>',
    {
      url: "http://localhost/logos-zero/luyen-tap/ke-hoach/",
      runScripts: "dangerously",
      virtualConsole: vc,
      beforeParse(window) {
        window.addEventListener("error", (e) => errors.push(e.message));
        if (storage) window.localStorage.setItem("logos-zero", JSON.stringify(storage));
      },
    }
  );
  const { window } = dom;
  for (const f of ["core.js", "util.js", "progress.js", "ke-hoach.js", "bieu-do.js"]) {
    window.eval(fs.readFileSync(path.join(JS, f), "utf8"));
  }
  return { window, document: window.document, errors };
}

/* Ngày trong dữ liệu mẫu tính lùi từ hôm nay: biểu đồ hoạt động chỉ vẽ 14 ngày gần nhất,
 * nên ngày cố định (bản cũ dùng 12/10/2026) làm kiểm thử tự hỏng sau 14 ngày. */
function isoDaysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
}

function stateWithData() {
  const d1 = isoDaysAgo(1), d2 = isoDaysAgo(2), d3 = isoDaysAgo(3);
  return {
    v: 1,
    skills: {
      fallacy: { ema: 0.4, n: 10, last: d1, days: { [d1]: { n: 10, c: 4 } } },
      logic: { ema: 0.95, n: 8, last: d1, days: { [d1]: { n: 8, c: 8 } } },
    },
    days: { [d1]: { n: 18, c: 12 }, [d2]: { n: 5, c: 5 } },
    quizzes: {},
    read: { "/cong-cu/nguy-bien/": d3 },
    cards: {},
    items: {},
    journal: {},
    imports: [],
  };
}

test("có dữ liệu → render nhóm gợi ý + biểu đồ SVG", async () => {
  const { window, document, errors } = makePage(stateWithData());
  await settle();
  assert.deepEqual(errors, [], "lỗi JS khi tải trang: " + errors.join("; "));

  const plan = document.querySelector(".oz-ke-hoach");
  assert.equal(plan.dataset.ozInit, "1", "ke-hoach chưa khởi tạo");
  assert.match(plan.textContent, /Cần củng cố/, "thiếu nhóm củng cố (fallacy ema 0.4)");
  assert.match(plan.textContent, /Nhận ra ngụy biện/, "thiếu tên kỹ năng");
  assert.match(plan.textContent, /Thử sức mới/, "thiếu nhóm thử sức");
  assert.match(plan.textContent, /Đã vững/, "thiếu nhóm đã vững (logic ema 0.95)");
  const links = plan.querySelectorAll("a[href]");
  assert.ok(links.length >= 3, "quá ít link gợi ý: " + links.length);
  assert.ok(plan.querySelector("button"), "thiếu nút Làm mới");

  const chart = document.querySelector(".oz-bieu-do");
  assert.equal(chart.dataset.ozInit, "1", "bieu-do chưa khởi tạo");
  const svgs = chart.querySelectorAll("svg");
  assert.equal(svgs.length, 2, "phải có 2 SVG (kỹ năng + hoạt động), nhận được " + svgs.length);
  assert.match(chart.textContent, /Nhận ra ngụy biện/, "biểu đồ thiếu tên kỹ năng");
  window.close();
});

test("chưa có dữ liệu → gợi ý nhập môn + text fallback biểu đồ", async () => {
  const { window, document, errors } = makePage(null);
  await settle();
  assert.deepEqual(errors, [], "lỗi JS khi tải trang: " + errors.join("; "));

  const plan = document.querySelector(".oz-ke-hoach");
  assert.match(plan.textContent, /Bắt đầu từ đây/, "thiếu nhóm nhập môn");

  const chart = document.querySelector(".oz-bieu-do");
  assert.match(chart.textContent, /Hãy làm vài quiz/, "thiếu text fallback biểu đồ");
  assert.equal(chart.querySelectorAll("svg").length, 0, "không nên vẽ SVG khi chưa có dữ liệu");
  window.close();
});

test("nút Làm mới đọc lại state mới nhất", async () => {
  const { window, document, errors } = makePage(null);
  await settle();
  const plan = document.querySelector(".oz-ke-hoach");
  assert.match(plan.textContent, /Bắt đầu từ đây/);

  window.OZ.progress.save(stateWithData());
  plan.querySelector("button").click();
  await settle();
  assert.match(plan.textContent, /Cần củng cố/, "Làm mới chưa đọc state mới");
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  window.close();
});
