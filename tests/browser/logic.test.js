/* Kiểm thử luồng công cụ logic mệnh đề trên jsdom — không cần build site.
 * Nạp core/util/logic-menh-de/progress vào jsdom; fetch ngân hàng được giả lập. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM, VirtualConsole } = require("jsdom");

const JS = path.join(__dirname, "../../docs/assets/js");
const settle = (ms = 60) => new Promise((r) => setTimeout(r, ms));

function mockBank() {
  return {
    exercises: [
      {
        id: "t-valid",
        de_bai: "Bài đúng mẫu",
        premises: ["P -> Q", "P"],
        conclusion: "Q",
        dap_an: "hop-le",
        giai_thich: "Modus Ponens.",
      },
      {
        id: "t-invalid",
        de_bai: "Bài sai mẫu",
        premises: ["P -> Q", "Q"],
        conclusion: "P",
        dap_an: "khong-hop-le",
        giai_thich: "Khẳng định hậu kiện. Phản ví dụ: P=sai, Q=đúng.",
      },
    ],
  };
}

function makePage(bank) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", (e) => errors.push(e.message || String(e)));
  vc.on("error", (e) => errors.push(String(e)));
  const dom = new JSDOM('<!DOCTYPE html><html><head></head><body><div class="oz-logic"></div></body></html>', {
    url: "http://localhost/logos-zero/cong-cu/suy-dien/",
    runScripts: "dangerously",
    virtualConsole: vc,
    beforeParse(window) {
      window.fetch = () =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(bank || mockBank()),
        });
      window.addEventListener("error", (e) => errors.push(e.message));
    },
  });
  const { window } = dom;
  for (const f of ["core.js", "util.js", "logic-menh-de.js", "progress.js"]) {
    window.eval(fs.readFileSync(path.join(JS, f), "utf8"));
  }
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

test("tự kiểm tra: lập luận hợp lệ hiện bảng chân trị", async () => {
  const { window, document, errors } = makePage();
  await settle();
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  assert.equal(document.querySelector(".oz-logic").dataset.ozInit, "1");
  // Giới hạn phạm vi được ghi rõ.
  assert.match(document.querySelector(".oz-logic").textContent, /chỉ xử lý logic mệnh đề/);

  document.querySelector(".oz-logic__premises").value = "P -> Q\nP";
  document.querySelector(".oz-logic__conclusion").value = "Q";
  document.querySelector(".oz-logic__pane .md-button--primary").click();
  await settle();
  const result = document.querySelector(".oz-logic__result");
  assert.match(result.textContent, /HỢP LỆ/);
  assert.equal(result.querySelectorAll("tbody tr").length, 4, "bảng 2 biến phải có 4 dòng");
  assert.deepEqual(errors, [], "lỗi JS trong luồng: " + errors.join("; "));
  window.close();
});

test("tự kiểm tra: lập luận không hợp lệ chỉ ra phản ví dụ", async () => {
  const { window, document, errors } = makePage();
  await settle();
  document.querySelector(".oz-logic__premises").value = "P -> Q\nQ";
  document.querySelector(".oz-logic__conclusion").value = "P";
  document.querySelector(".oz-logic__pane .md-button--primary").click();
  await settle();
  const result = document.querySelector(".oz-logic__result");
  assert.match(result.textContent, /KHÔNG HỢP LỆ/);
  assert.match(result.textContent, /P=sai, Q=đúng/);
  assert.ok(result.querySelector("tr.oz-logic__ce"), "dòng phản ví dụ phải được tô màu");
  window.close();
});

test("tự kiểm tra: công thức sai báo lỗi thân thiện", async () => {
  const { window, document, errors } = makePage();
  await settle();
  document.querySelector(".oz-logic__premises").value = "P ->";
  document.querySelector(".oz-logic__conclusion").value = "Q";
  document.querySelector(".oz-logic__pane .md-button--primary").click();
  await settle();
  assert.match(document.querySelector(".oz-logic__result").textContent, /cần một mệnh đề/);
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  window.close();
});

test("luyện tập: trả lời đúng + tìm phản ví dụ, có ghi tiến độ", async () => {
  const bank = {
    exercises: [
      {
        id: "t-invalid",
        de_bai: "Bài sai mẫu",
        premises: ["P -> Q", "Q"],
        conclusion: "P",
        dap_an: "khong-hop-le",
        giai_thich: "Khẳng định hậu kiện. Phản ví dụ: P=sai, Q=đúng.",
      },
    ],
  };
  const { window, document, errors } = makePage(bank);
  await settle();
  // Chuyển sang tab Luyện tập.
  const tabs = [...document.querySelectorAll(".oz-tab")];
  tabs.find((t) => t.textContent.includes("Luyện tập")).click();
  assert.ok(await until(() => document.querySelector(".oz-logic__debai")), "không tải được câu hỏi");
  assert.match(document.querySelector(".oz-logic__stage").textContent, /Bài sai mẫu/);

  // Trả lời "Không hợp lệ" (đúng) → được yêu cầu tìm phản ví dụ.
  [...document.querySelectorAll(".oz-logic__stage .md-button")].find((b) => b.textContent === "Không hợp lệ").click();
  await settle();
  assert.ok(document.querySelector(".oz-logic__ce-input"), "không hiện ô nhập phản ví dụ");

  // Nhập sai trước.
  const input = document.querySelector(".oz-logic__ce-input");
  input.value = "P=đúng, Q=đúng";
  [...document.querySelectorAll(".oz-logic__stage .md-button")].find((b) => b.textContent.includes("Kiểm tra phản ví dụ")).click();
  await settle();
  assert.match(document.querySelector(".oz-logic__ce-ask").textContent, /Chưa phải phản ví dụ/);

  // Nhập đúng.
  input.value = "P=sai, Q=đúng";
  [...document.querySelectorAll(".oz-logic__stage .md-button")].find((b) => b.textContent.includes("Kiểm tra phản ví dụ")).click();
  await settle();
  assert.match(document.querySelector(".oz-logic__stage").textContent, /một phản ví dụ hợp lệ/);

  // Tiến độ được ghi vào skill logic.
  const saved = JSON.parse(window.localStorage.getItem("logos-zero"));
  assert.ok(saved.skills.logic && saved.skills.logic.n >= 1, "chưa ghi skill logic");
  assert.ok(saved.items["logic:t-invalid"], "chưa ghi item");
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  window.close();
});

test("luyện tập: trả lời sai hiện giải thích", async () => {
  const bank = {
    exercises: [
      {
        id: "t-valid",
        de_bai: "Bài đúng mẫu",
        premises: ["P -> Q", "P"],
        conclusion: "Q",
        dap_an: "hop-le",
        giai_thich: "Modus Ponens.",
      },
    ],
  };
  const { window, document, errors } = makePage(bank);
  await settle();
  [...document.querySelectorAll(".oz-tab")].find((t) => t.textContent.includes("Luyện tập")).click();
  assert.ok(await until(() => document.querySelector(".oz-logic__debai")), "không tải được câu hỏi");
  [...document.querySelectorAll(".oz-logic__stage .md-button")].find((b) => b.textContent === "Không hợp lệ").click();
  await settle();
  assert.match(document.querySelector(".oz-logic__stage").textContent, /Chưa đúng/);
  assert.match(document.querySelector(".oz-logic__stage").textContent, /Modus Ponens/);
  const saved = JSON.parse(window.localStorage.getItem("logos-zero"));
  assert.equal(saved.skills.logic.n, 1);
  assert.equal(saved.skills.logic.ema, 0, "trả lời sai thì EMA = 0");
  window.close();
});
