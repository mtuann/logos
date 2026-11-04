/* Kiểm thử luồng công cụ sơ đồ lập luận trên jsdom — không cần build site.
 * Nạp core/util/so-do-lap-luan/progress vào jsdom; fetch ngân hàng được giả lập. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM, VirtualConsole } = require("jsdom");

const JS = path.join(__dirname, "../../docs/assets/js");
const settle = (ms = 60) => new Promise((r) => setTimeout(r, ms));

function mockBank() {
  return {
    passages: [
      {
        id: "sodo-t1",
        do_kho: 1,
        cau: [
          { id: "c1", nd: "Học sớm giúp trẻ đỡ vất vả." },
          { id: "c2", nd: "Chị Lan đang tìm lớp vẽ." },
          { id: "c3", nd: "Nên cho trẻ học sớm." },
        ],
        dap_an: [
          { cau: "c1", vai_tro: "tien-de", ho_tro: ["c3"] },
          { cau: "c2", vai_tro: "khong-lien-quan" },
          { cau: "c3", vai_tro: "ket-luan" },
        ],
      },
    ],
  };
}

function makePage() {
  const errors = [];
  const records = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", (e) => errors.push(e.message || String(e)));
  vc.on("error", (e) => errors.push(String(e)));
  const dom = new JSDOM('<!DOCTYPE html><html><head></head><body><div class="oz-so-do"></div></body></html>', {
    url: "http://localhost/logos/cong-cu/so-do-lap-luan/",
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
  for (const f of ["core.js", "util.js", "so-do-lap-luan.js", "progress.js"]) {
    window.eval(fs.readFileSync(path.join(JS, f), "utf8"));
  }
  window.OZ.util.shuffle = (arr) => arr; // thứ tự cố định cho test
  const origRecord = window.OZ.progress.record;
  window.OZ.progress.record = function (skill, correct, itemId) {
    records.push({ skill, correct, itemId });
    return origRecord.call(this, skill, correct, itemId);
  };
  return { window, document: window.document, errors, records };
}

async function until(fn, ms = 2000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    if (fn()) return true;
    await settle(20);
  }
  return false;
}

function answer(document, passageId, roles) {
  for (const [cid, role] of Object.entries(roles)) {
    const radio = document.querySelector(`input[name="sodo-${passageId}-${cid}"][value="${role}"]`);
    assert.ok(radio, `không thấy radio ${cid}=${role}`);
    radio.checked = true;
  }
}

test("hiển thị đoạn văn và các nhóm vai trò", async () => {
  const { document, errors, window } = makePage();
  await until(() => document.querySelector(".oz-sodo__passage"));
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  assert.equal(document.querySelector(".oz-so-do").dataset.ozInit, "1");
  assert.equal(document.querySelectorAll(".oz-sodo__passage li").length, 3);
  assert.equal(document.querySelectorAll(".oz-sodo__item").length, 3, "3 nhóm radio cho 3 câu");
  window.close();
});

test("chọn đúng hết: điểm tối đa, hiện cây SVG, ghi nhận P.record", async () => {
  const { document, errors, records, window } = makePage();
  await until(() => document.querySelector(".oz-sodo__passage"));
  answer(document, "sodo-t1", { c1: "tien-de", c2: "khong-lien-quan", c3: "ket-luan" });
  document.querySelector(".oz-sodo__form .md-button--primary").click();
  await settle();
  const box = document.querySelector(".oz-so-do");
  assert.match(box.textContent, /đúng 3\/3/);
  const svg = box.querySelector("svg.oz-sodo__tree");
  assert.ok(svg, "phải vẽ cây SVG đáp án");
  assert.ok(svg.querySelectorAll("rect").length >= 2, "cây có ít nhất 2 hộp (tiền đề + kết luận)");
  assert.equal(records.length, 1);
  assert.equal(records[0].skill, "argument");
  assert.equal(records[0].correct, true);
  assert.equal(records[0].itemId, "sodo:sodo-t1");
  assert.deepEqual(errors, [], "lỗi JS trong luồng: " + errors.join("; "));
  window.close();
});

test("chọn sai: bị trừ điểm, P.record ghi correct=false", async () => {
  const { document, errors, records, window } = makePage();
  await until(() => document.querySelector(".oz-sodo__passage"));
  answer(document, "sodo-t1", { c1: "ket-luan", c2: "khong-lien-quan", c3: "ket-luan" });
  document.querySelector(".oz-sodo__form .md-button--primary").click();
  await settle();
  const box = document.querySelector(".oz-so-do");
  assert.match(box.textContent, /đúng 2\/3/);
  assert.equal(records.length, 1);
  assert.equal(records[0].correct, false);
  assert.deepEqual(errors, [], "lỗi JS trong luồng: " + errors.join("; "));
  window.close();
});

test("chưa gán hết vai trò: báo lỗi, không chấm", async () => {
  const { document, errors, records, window } = makePage();
  await until(() => document.querySelector(".oz-sodo__passage"));
  answer(document, "sodo-t1", { c1: "tien-de" });
  document.querySelector(".oz-sodo__form .md-button--primary").click();
  await settle();
  const box = document.querySelector(".oz-so-do");
  assert.match(box.textContent, /chưa gán vai trò|gán vai trò cho mọi câu/);
  assert.equal(records.length, 0, "không ghi nhận khi chưa chấm");
  assert.deepEqual(errors, [], "lỗi JS trong luồng: " + errors.join("; "));
  window.close();
});
