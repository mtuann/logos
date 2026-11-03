const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { SITE, listPages, openPage, until } = require("./helpers");

const CORE = ["core.js", "progress.js", "loader.js"];
const TOOL_SELECTORS = {
  ".oz-quiz": ["util.js", "quiz.js"],
  ".oz-fallacy-trainer": ["util.js", "fallacy.js"],
  ".oz-logic": ["util.js", "logic-menh-de.js"],
  ".oz-thi-nghiem": ["util.js", "thi-nghiem.js"],
  ".oz-so-do": ["util.js", "so-do-lap-luan.js"],
  ".oz-flashcards": ["util.js", "flashcards.js"],
  ".oz-on-tap": ["util.js", "on-tap.js"],
  ".oz-daily": ["util.js", "daily.js"],
  ".oz-mydata, .oz-progress-summary": ["util.js", "merge.js", "mydata.js"],
  ".oz-ke-hoach": ["util.js", "on-tap.js", "ke-hoach.js"],
  ".oz-bieu-do": ["util.js", "bieu-do.js"],
  ".oz-nhat-ky": ["util.js", "nhat-ky.js"],
  ".oz-steelman": ["util.js", "steelman.js"],
};

assert.ok(fs.existsSync(path.join(SITE, "index.html")), "Chưa build site — chạy: mkdocs build --strict");
const pages = listPages();

test("có đủ các trang của Giai đoạn 1", () => {
  for (const p of [
    "/logos-zero/",
    "/logos-zero/bat-dau/",
    "/logos-zero/cong-cu/nguy-bien/",
    "/logos-zero/cau-hoi/tam-tri-va-ai/",
    "/logos-zero/cau-hoi/tri-thuc/",
    "/logos-zero/cau-hoi/tu-do-y-chi/",
    "/logos-zero/luyen-tap/nguy-bien/",
    "/logos-zero/luyen-tap/the-ghi-nho/",
    "/logos-zero/them/du-lieu/",
  ])
    assert.ok(pages.includes(p), "thiếu " + p);
});

for (const page of pages) {
  test(`trang ${page}: không lỗi JS, công cụ khởi tạo, không tải script thừa`, async () => {
    const { document, errors, toolScripts, window } = await openPage(page);
    const expected = new Set(CORE);
    const present = [];
    for (const [sel, files] of Object.entries(TOOL_SELECTORS)) {
      if (document.querySelector(sel)) {
        present.push(sel);
        files.forEach((f) => expected.add(f));
      }
    }
    // Chờ các công cụ tải dữ liệu xong.
    await until(() => present.every((sel) => [...document.querySelectorAll(sel)].every((n) => n.dataset.ozInit === "1")));
    await until(() => !document.querySelector(".oz-fallacy-trainer .oz-muted:only-child, .oz-flashcards > .oz-muted:only-child"));
    assert.deepEqual(errors, [], "lỗi JS");
    assert.deepEqual(new Set(toolScripts), expected, "script tải về khác dự kiến");
    assert.equal(toolScripts.length, new Set(toolScripts).size, "một script bị tải hai lần");
    for (const sel of present)
      for (const n of document.querySelectorAll(sel)) {
        assert.equal(n.dataset.ozInit, "1", sel + " chưa khởi tạo");
        assert.equal(n.querySelector(".oz-error"), null, sel + " báo lỗi: " + (n.querySelector(".oz-error") || {}).textContent);
      }
    // Mỗi bài (trừ trang chủ) có nút In.
    if (document.querySelector("article h1") && !document.querySelector(".oz-home"))
      assert.ok(document.querySelector(".oz-print-btn"), "thiếu nút In bài này");
    window.close();
  });
}

test("trang chỉ có chữ không tải script công cụ nào", async () => {
  const { toolScripts, window } = await openPage("/logos-zero/lich-su/");
  assert.deepEqual(toolScripts.sort(), [...CORE].sort());
  window.close();
});

test("quiz: chọn đáp án, xem kết quả, ghi tiến độ", async () => {
  const { document, window } = await openPage("/logos-zero/cau-hoi/tam-tri-va-ai/");
  const box = document.querySelector(".oz-quiz");
  const qs = JSON.parse(box.querySelector('script[type="application/json"]').textContent);
  // Trả lời đúng mọi câu trừ câu đầu.
  qs.forEach((q, i) => {
    const pick = i === 0 ? (q.answer + 1) % q.options.length : q.answer;
    box.querySelectorAll("fieldset")[i].querySelectorAll("input")[pick].click();
  });
  box.querySelector("form").dispatchEvent(new window.Event("submit", { cancelable: true }));
  assert.match(box.querySelector(".oz-quiz__result").textContent, new RegExp(`${qs.length - 1}/${qs.length}`));
  assert.ok(box.querySelector(".oz-quiz__fb.is-wrong"));
  const saved = JSON.parse(window.localStorage.getItem("logos-zero"));
  assert.equal(saved.quizzes["mind-1"].best, qs.length - 1);
  assert.equal(saved.skills.mind.n, qs.length);
  window.close();
});

test("nhận ra ngụy biện: trả lời, xem giải thích, đi hết một lượt", async () => {
  const { document, window } = await openPage("/logos-zero/luyen-tap/nguy-bien/");
  const box = document.querySelector(".oz-fallacy-trainer");
  await until(() => box.querySelector(".oz-option"));
  const data = JSON.parse(fs.readFileSync(path.join(SITE, "assets/data/fallacies.json"), "utf8"));
  const count = Number(box.dataset.count);
  for (let i = 0; i < count; i++) {
    const passage = box.querySelector(".oz-ft__passage").textContent;
    const q = data.questions.find((x) => x.passage === passage);
    assert.ok(q, "không tìm thấy câu hỏi trong dữ liệu");
    if (i === 0) {
      // Câu đầu cố ý chọn sai: nút đã chọn bị đánh dấu sai, nút đáp án được đánh dấu đúng.
      const wrong = q.options.find((o) => o !== q.answer);
      box.querySelector(`.oz-option[data-id="${wrong}"]`).click();
      assert.ok(box.querySelector(".oz-ft__fb.is-wrong"), "phản hồi sai không hiện");
      assert.ok(box.querySelector(`.oz-option[data-id="${wrong}"]`).classList.contains("is-wrong"));
      assert.ok(box.querySelector(`.oz-option[data-id="${q.answer}"]`).classList.contains("is-correct"));
      assert.match(box.querySelector(".oz-ft__fb").textContent, new RegExp(data.types.find((t) => t.id === q.answer).vi));
    } else {
      box.querySelector(`.oz-option[data-id="${q.answer}"]`).click();
      assert.ok(box.querySelector(".oz-ft__fb.is-correct"), "phản hồi đúng không hiện");
      assert.ok(box.querySelector(`.oz-option[data-id="${q.answer}"]`).classList.contains("is-correct"));
    }
    if (q.highlight) assert.equal(box.querySelector(".oz-ft__passage mark").textContent, q.highlight);
    assert.ok([...box.querySelectorAll(".oz-option")].every((b) => b.disabled));
    box.querySelector(".oz-ft__fb .md-button--primary").click();
  }
  assert.match(box.querySelector("h3").textContent, new RegExp(`${count - 1}/${count}`));
  const saved = JSON.parse(window.localStorage.getItem("logos-zero"));
  assert.equal(saved.skills.fallacy.n, count);
  assert.ok(saved.skills.fallacy.ema > 0.9 && saved.skills.fallacy.ema < 1);
  // Đổi cấp độ: lượt mới chỉ gồm câu cấp 3.
  box.querySelector('.oz-segmented [data-level="3"]').click();
  const p = box.querySelector(".oz-ft__passage").textContent;
  assert.equal(data.questions.find((x) => x.passage === p).level, 3);
  window.close();
});

test("thẻ ghi nhớ: lật thẻ, chấm, lưu hộp Leitner", async () => {
  const { document, window } = await openPage("/logos-zero/luyen-tap/the-ghi-nho/");
  const box = document.querySelector(".oz-flashcards");
  await until(() => box.querySelector(".oz-card"));
  const term = box.querySelector(".oz-card__term").textContent;
  const buttons = () => [...box.querySelectorAll(".oz-actions button")];
  buttons().find((b) => b.textContent === "Lật thẻ").click();
  assert.equal(box.querySelector(".oz-card__back").hidden, false);
  buttons().find((b) => b.textContent === "Nhớ rồi").click();
  const saved = JSON.parse(window.localStorage.getItem("logos-zero"));
  const terms = JSON.parse(fs.readFileSync(path.join(SITE, "assets/data/terms.json"), "utf8")).terms;
  const id = terms.find((t) => t.vi === term).id;
  assert.equal(saved.cards[id].box, 1);
  assert.notEqual(box.querySelector(".oz-card__term").textContent, term, "thẻ tiếp theo phải khác");
  window.close();
});

test("dữ liệu của tôi: hiển thị tóm tắt và xóa dữ liệu", async () => {
  const storage = { v: 1, skills: { fallacy: { ema: 0.8, n: 10, last: "2026-10-12", days: {} } }, days: { "2026-10-12": { n: 10, c: 8 } }, read: { "/a/": "2026-10-12" } };
  const { document, window } = await openPage("/logos-zero/them/du-lieu/", { storage });
  const box = document.querySelector(".oz-mydata");
  assert.match(box.textContent, /Nhận ra ngụy biện/);
  assert.match(box.textContent, /80%/);
  [...box.querySelectorAll("button")].find((b) => /Xóa/.test(b.textContent)).click();
  assert.equal(window.localStorage.getItem("logos-zero"), null);
  assert.match(box.textContent, /Chưa có dữ liệu/);
  window.close();
});

test("trang chủ: nổi bật đúng một câu hỏi hôm nay", async () => {
  const { document, window } = await openPage("/logos-zero/");
  assert.equal(document.querySelectorAll(".oz-daily li.is-today").length, 1);
  window.close();
});
