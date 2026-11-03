/* Kiểm thử luồng gộp sao lưu trên jsdom — không cần build site.
 * Nạp trực tiếp core/util/merge/progress/mydata vào jsdom rồi mô phỏng:
 * chọn file → xem trước → xác nhận gộp. */
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
  const dom = new JSDOM('<!DOCTYPE html><html><head></head><body><div class="oz-mydata"></div></body></html>', {
    url: "http://localhost/logos-zero/them/du-lieu/",
    runScripts: "dangerously",
    virtualConsole: vc,
    beforeParse(window) {
      window.FileReader = class {
        readAsText(file) {
          this.result = file._content;
          setTimeout(() => this.onload && this.onload(), 0);
        }
      };
      window.addEventListener("error", (e) => errors.push(e.message));
      if (storage) window.localStorage.setItem("logos-zero", JSON.stringify(storage));
    },
  });
  const { window } = dom;
  for (const f of ["core.js", "util.js", "merge.js", "progress.js", "mydata.js"]) {
    window.eval(fs.readFileSync(path.join(JS, f), "utf8"));
  }
  return { window, document: window.document, errors };
}

function stateA() {
  return {
    v: 1,
    skills: { fallacy: { ema: 0.8, n: 10, last: "2026-10-01", days: { "2026-10-01": { n: 10, c: 8 } } } },
    days: { "2026-10-01": { n: 10, c: 8 } },
    quizzes: {},
    read: { "/a/": "2026-10-01" },
    cards: {},
    items: {},
    journal: {},
    imports: [],
  };
}

function backupB() {
  return {
    app: "logos-zero",
    version: 1,
    deviceId: "may-b",
    exported: "2026-10-13T10:00:00.000Z",
    state: {
      v: 1,
      skills: { fallacy: { ema: 0.6, n: 10, last: "2026-10-03", days: { "2026-10-03": { n: 10, c: 6 } } } },
      days: { "2026-10-03": { n: 10, c: 6 } },
      quizzes: { "mind-1": { best: 4, total: 5, tries: 1, last: "2026-10-03" } },
      read: { "/b/": "2026-10-02" },
      cards: {},
      items: {},
      journal: {},
      imports: [],
    },
  };
}

async function chooseFile(document, window, json) {
  const input = document.querySelector('input[type="file"]');
  assert.ok(input, "thiếu input file");
  Object.defineProperty(input, "files", { value: [{ _content: json, name: "backup.json" }], configurable: true });
  input.dispatchEvent(new window.Event("change", { bubbles: true }));
  await settle(120); // FileReader giả lập + say() đều bất đồng bộ
}

test("luồng nhập → xem trước → xác nhận gộp", async () => {
  const { window, document, errors } = makePage(stateA());
  await settle();
  assert.deepEqual(errors, [], "lỗi JS khi tải trang: " + errors.join("; "));
  assert.equal(document.querySelector(".oz-mydata").dataset.ozInit, "1", "mydata chưa khởi tạo");
  assert.equal(document.querySelector(".oz-merge-preview"), null);

  await chooseFile(document, window, JSON.stringify(backupB()));
  const panel = document.querySelector(".oz-merge-preview");
  assert.ok(panel, "không hiện panel xem trước");
  assert.match(panel.textContent, /Kỹ năng/, "thiếu dòng kỹ năng");
  assert.match(panel.textContent, /Bài quiz/, "thiếu dòng quiz");
  assert.match(panel.textContent, /Bài đã đọc/, "thiếu dòng bài đọc");
  assert.match(panel.textContent, /EMA.*xấp xỉ/, "thiếu ghi chú EMA");

  panel.querySelector(".md-button--primary").click(); // "Xác nhận gộp"
  await settle();
  assert.equal(document.querySelector(".oz-merge-preview"), null, "panel chưa đóng sau khi gộp");
  const saved = JSON.parse(window.localStorage.getItem("logos-zero"));
  assert.deepEqual(saved.days["2026-10-01"], { n: 10, c: 8 });
  assert.deepEqual(saved.days["2026-10-03"], { n: 10, c: 6 });
  assert.equal(saved.skills.fallacy.n, 20);
  assert.equal(saved.skills.fallacy.ema, 0.7);
  assert.equal(saved.quizzes["mind-1"].best, 4);
  assert.equal(saved.read["/b/"], "2026-10-02");
  assert.deepEqual(saved.imports, [{ deviceId: "may-b", exportedAt: "2026-10-13T10:00:00.000Z" }]);
  assert.deepEqual(errors, [], "lỗi JS trong luồng: " + errors.join("; "));
  window.close();
});

test("nhập lại cùng file → báo đã nhập, không nhân đôi", async () => {
  const { window, document, errors } = makePage(stateA());
  await settle();
  const json = JSON.stringify(backupB());
  await chooseFile(document, window, json);
  document.querySelector(".oz-merge-preview .md-button--primary").click();
  await settle();
  const before = window.localStorage.getItem("logos-zero");
  await chooseFile(document, window, json);
  assert.match(document.querySelector(".oz-live").textContent, /đã được nhập trước đây/);
  assert.equal(window.localStorage.getItem("logos-zero"), before, "dữ liệu bị thay đổi khi nhập lại");
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  window.close();
});

test("file lạ → báo lỗi thân thiện, không crash", async () => {
  const { window, document, errors } = makePage(stateA());
  await settle();
  await chooseFile(document, window, JSON.stringify({ app: "ung-dung-khac" }));
  assert.equal(document.querySelector(".oz-merge-preview"), null);
  assert.match(document.querySelector(".oz-live").textContent, /không phải bản sao lưu/);
  await chooseFile(document, window, "không phải json {{{");
  assert.match(document.querySelector(".oz-live").textContent, /Không đọc được file/);
  assert.deepEqual(errors, [], "lỗi JS: " + errors.join("; "));
  window.close();
});
