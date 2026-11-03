/* Logos Zero — "Dữ liệu của tôi": xem tóm tắt, tải bản sao lưu, xóa dữ liệu.
 * <div class="oz-mydata"></div> (đầy đủ) · <div class="oz-progress-summary"></div> (tóm tắt) */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.mydata = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var SKILL_NAMES = {
    intro: "Nhập môn",
    argument: "Nhận ra lập luận",
    deduction: "Suy diễn",
    induction: "Quy nạp",
    assumption: "Giả định ngầm",
    fallacy: "Nhận ra ngụy biện",
    logic: "Logic mệnh đề",
    knowledge: "Tri thức",
    mind: "Tâm trí và AI",
    freewill: "Tự do ý chí",
    vietnam: "Triết học Việt Nam",
    ethics: "Đạo đức học",
    politics: "Triết học chính trị",
    aesthetics: "Mỹ học",
    religion: "Triết học tôn giáo",
    metaphysics: "Siêu hình học",
    meaning: "Ý nghĩa cuộc sống",
    terms: "Thuật ngữ",
  };

  /* Hàm thuần: tóm tắt trạng thái thành số liệu hiển thị. */
  function summarize(state, P, date) {
    var s = P.migrate(state);
    var skills = Object.keys(s.skills)
      .sort()
      .map(function (k) {
        var sk = s.skills[k];
        return { id: k, name: SKILL_NAMES[k] || k, n: sk.n, pct: sk.ema === null ? null : Math.round(sk.ema * 100), last: sk.last };
      });
    return {
      read: Object.keys(s.read).length,
      answers: Object.keys(s.days).reduce(function (a, d) { return a + s.days[d].n; }, 0),
      streak: P.streak(s, date),
      cards: Object.keys(s.cards).length,
      quizzes: Object.keys(s.quizzes).length,
      skills: skills,
    };
  }

  function stat(U, value, label) {
    return U.el("div", { class: "oz-stat" }, [U.el("span", { class: "oz-stat__value", text: String(value) }), U.el("span", { class: "oz-stat__label", text: label })]);
  }

  function render(box, full) {
    var OZ = window.OZ;
    var U = OZ.util;
    var P = OZ.progress;
    box.textContent = "";
    var say = U.live(box);
    var sum = summarize(P.load(), P);
    box.appendChild(
      U.el("div", { class: "oz-stats" }, [
        stat(U, sum.read, "bài đã mở"),
        stat(U, sum.answers, "câu đã trả lời"),
        stat(U, sum.streak, "ngày liên tiếp"),
        stat(U, sum.cards, "thẻ đang ôn"),
      ])
    );
    if (sum.skills.length) {
      var rows = sum.skills.map(function (k) {
        return U.el("tr", null, [
          U.el("td", { text: k.name }),
          U.el("td", { text: String(k.n) }),
          U.el("td", { text: k.pct === null ? "—" : k.pct + "%" }),
          U.el("td", { text: k.last || "—" }),
        ]);
      });
      box.appendChild(
        U.el("table", { class: "oz-table" }, [
          U.el("caption", { text: "Theo kỹ năng (độ chính xác gần đây, có trọng số cho các lần mới)" }),
          U.el("thead", null, [U.el("tr", null, ["Kỹ năng", "Số câu", "Chính xác", "Lần cuối"].map(function (h) { return U.el("th", { scope: "col", text: h }); }))]),
          U.el("tbody", null, rows),
        ])
      );
    } else box.appendChild(U.el("p", { class: "oz-muted", text: "Chưa có dữ liệu luyện tập trên trình duyệt này." }));
    if (!full) return;

    var exportBtn = U.el("button", {
      type: "button",
      class: "md-button md-button--primary",
      text: "Tải bản sao lưu (JSON)",
      onclick: function () {
        var M = OZ.merge;
        var data = JSON.stringify(
          {
            app: "logos",
            version: 1,
            deviceId: M ? M.deviceId() : null,
            exported: new Date().toISOString(),
            state: P.load(),
          },
          null,
          2
        );
        var a = U.el("a", { href: URL.createObjectURL(new Blob([data], { type: "application/json" })), download: "logos-" + P.today() + ".json" });
        document.body.appendChild(a);
        a.click();
        setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
      },
    });
    var importBtn = U.el("button", { type: "button", class: "md-button", text: "Nhập bản sao lưu…" });
    var fileInput = U.el("input", {
      type: "file",
      accept: "application/json",
      class: "oz-sr-only",
      "aria-label": "Chọn file sao lưu JSON để nhập",
    });
    importBtn.addEventListener("click", function () {
      fileInput.click();
    });
    fileInput.addEventListener("change", function () {
      var f = fileInput.files && fileInput.files[0];
      fileInput.value = "";
      if (!f) return;
      var reader = new FileReader();
      reader.onload = function () {
        try {
          showPreview(box, JSON.parse(reader.result));
        } catch (e) {
          say("Không đọc được file: " + e.message);
        }
      };
      reader.onerror = function () {
        say("Không đọc được file đã chọn.");
      };
      reader.readAsText(f);
    });
    var clearBtn = U.el("button", {
      type: "button",
      class: "md-button oz-danger",
      text: "Xóa toàn bộ dữ liệu",
      onclick: function () {
        if (window.confirm("Xóa toàn bộ tiến độ, thẻ ghi nhớ và ghi chép trên trình duyệt này? Không thể hoàn tác.")) {
          P.clear();
          render(box, full);
        }
      },
    });
    box.appendChild(U.el("div", { class: "oz-actions" }, [exportBtn, importBtn, fileInput, clearBtn]));
  }

  /* Đọc file sao lưu do người dùng chọn, hiện xem trước rồi chờ xác nhận gộp. */
  function showPreview(box, data) {
    var OZ = window.OZ;
    var U = OZ.util;
    var P = OZ.progress;
    var M = OZ.merge;
    var say = U.live(box);
    if (!M) {
      say("Chưa tải được mô-đun gộp dữ liệu. Hãy tải lại trang.");
      return;
    }
    var v = M.validateBackup(data);
    if (!v.ok) {
      say(v.error);
      return;
    }
    var old = box.querySelector(".oz-merge-preview");
    if (old) old.remove();
    var pv = M.previewMerge(P.load(), v.state, v.meta);
    if (pv.alreadyImported) {
      say("File sao lưu này đã được nhập trước đây. Không có gì thay đổi.");
      return;
    }
    var panel = U.el("div", { class: "oz-merge-preview" });
    panel.appendChild(U.el("h3", { text: "Xem trước khi gộp" }));
    if (pv.summary.length) {
      var rows = pv.summary.map(function (r) {
        return U.el("tr", null, [
          U.el("td", { text: r.section }),
          U.el("td", { text: String(r.added) }),
          U.el("td", { text: String(r.updated) }),
        ]);
      });
      panel.appendChild(
        U.el("table", { class: "oz-table" }, [
          U.el("caption", { text: "Thay đổi sẽ áp dụng" }),
          U.el("thead", null, [
            U.el("tr", null, ["Mục", "Thêm mới", "Cập nhật"].map(function (h) {
              return U.el("th", { scope: "col", text: h });
            })),
          ]),
          U.el("tbody", null, rows),
        ])
      );
    } else {
      panel.appendChild(U.el("p", { class: "oz-muted", text: "File không có dữ liệu nào mới so với máy này." }));
    }
    pv.conflicts.forEach(function (c) {
      panel.appendChild(U.el("p", { class: "oz-muted", text: "• " + c }));
    });
    panel.appendChild(U.el("p", { class: "oz-muted", text: pv.emaNote }));
    var confirm = U.el("button", {
      type: "button",
      class: "md-button md-button--primary",
      text: "Xác nhận gộp",
      onclick: function () {
        P.save(pv.merged);
        render(box, true);
        U.live(box)("Đã gộp xong.");
      },
    });
    var cancel = U.el("button", {
      type: "button",
      class: "md-button",
      text: "Hủy",
      onclick: function () {
        panel.remove();
        say("Đã hủy nhập file.");
      },
    });
    panel.appendChild(U.el("div", { class: "oz-actions" }, [confirm, cancel]));
    box.appendChild(panel);
    say("Đã đọc file sao lưu. Xem lại thay đổi rồi bấm Xác nhận gộp.");
  }

  function initAll(doc) {
    var U = window.OZ.util;
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-mydata, .oz-progress-summary"), function (box) {
      if (!U.claim(box)) return;
      render(box, box.classList.contains("oz-mydata"));
    });
  }

  return { summarize: summarize, initAll: initAll };
});
