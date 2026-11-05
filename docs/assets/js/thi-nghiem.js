/* Logos — công cụ thí nghiệm tư duy.
 * <div class="oz-thi-nghiem"></div>  Dữ liệu: assets/data/thi-nghiem.json
 * KHÔNG chấm điểm, KHÔNG gọi P.record — không có đáp án đúng trong thí nghiệm tư duy.
 * Mẫu UMD của repo: hàm thuần xuất qua module.exports; trình duyệt dùng OZReady(initAll). */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.thinghiem = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* Hàm thuần: hàng số liệu khảo sát cho từng lựa chọn. */
  function surveyRows(survey, choices) {
    if (!survey) return null;
    var byId = {};
    choices.forEach(function (c) {
      byId[c.id] = c;
    });
    return Object.keys(survey)
      .filter(function (k) {
        return byId[k] && typeof survey[k] === "number";
      })
      .map(function (k) {
        return { id: k, nd: byId[k].nd, pct: survey[k] };
      });
  }

  function choiceById(choices, id) {
    for (var i = 0; i < choices.length; i++) {
      if (choices[i].id === id) return choices[i];
    }
    return null;
  }

  function init(box) {
    var U = window.OZ.util;
    if (!U.claim(box)) return;
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Thí nghiệm tư duy");
    box.appendChild(U.el("p", { class: "oz-muted", text: "Đang tải thí nghiệm…" }));
    U.fetchJSON("assets/data/thi-nghiem.json")
      .then(function (data) {
        build(box, data.experiments || []);
      })
      .catch(function (e) {
        box.textContent = "";
        box.appendChild(U.el("p", { class: "oz-error", text: e.message }));
      });
  }

  function build(box, experiments) {
    var U = window.OZ.util;
    var say = U.live(box);
    box.textContent = "";
    if (!experiments.length) {
      box.appendChild(U.el("p", { class: "oz-error", text: "Chưa có thí nghiệm." }));
      return;
    }
    var order = U.shuffle(experiments.map(function (e, i) {
      return i;
    }));
    var idx = 0;
    var progress = U.el("p", { class: "oz-muted" });
    var stage = U.el("div", { class: "oz-tn__stage" });
    box.appendChild(progress);
    box.appendChild(stage);

    function renderProgress() {
      progress.textContent = "Thí nghiệm " + Math.min(idx + 1, order.length) + "/" + order.length;
    }

    function next() {
      if (idx >= order.length) {
        stage.textContent = "";
        progress.textContent = "Đã xem hết " + order.length + " thí nghiệm.";
        stage.appendChild(
          U.el("p", { text: "Không có đáp án đúng ở đây — chỉ có những câu hỏi giúp bạn thấy rõ mình đang đứng ở đâu." })
        );
        var again = U.el("button", {
          type: "button",
          class: "md-button md-button--primary",
          text: "Xem lại (xáo trộn)",
          onclick: function () {
            idx = 0;
            order = U.shuffle(order);
            next();
          },
        });
        stage.appendChild(U.el("div", { class: "oz-actions" }, [again]));
        return;
      }
      renderProgress();
      show(experiments[order[idx]]);
    }

    function show(ex) {
      stage.textContent = "";
      stage.appendChild(U.el("h3", { text: ex.ten }));
      String(ex.hoan_canh)
        .split(/\n+/)
        .forEach(function (para) {
          if (para.trim()) stage.appendChild(U.el("p", { text: para.trim() }));
        });
      stage.appendChild(U.el("p", null, [U.el("strong", { text: ex.cau_hoi })]));
      var fb = U.el("div", { "aria-live": "polite" });
      var btns = U.el("div", { class: "oz-actions" });
      ex.lua_chon.forEach(function (c) {
        var b = U.el("button", { type: "button", class: "md-button", text: c.nd });
        b.addEventListener("click", function () {
          choose(ex, c, btns, fb);
        });
        btns.appendChild(b);
      });
      stage.appendChild(btns);
      stage.appendChild(fb);
    }

    function choose(ex, c, btns, fb) {
      Array.prototype.forEach.call(btns.querySelectorAll("button"), function (b) {
        b.disabled = true;
        if (b.textContent === c.nd) b.classList.add("md-button--primary");
      });
      // Lập trường của lựa chọn.
      fb.appendChild(U.el("h4", { text: "Lập trường của bạn: " + c.lap_truong }));
      fb.appendChild(U.el("p", { text: c.giai_thich }));
      // Steelman chống lại chính lựa chọn đó.
      var steel = ex.phan_bien_manh_nhat && ex.phan_bien_manh_nhat[c.id];
      if (steel) {
        fb.appendChild(U.el("h4", { text: "Phản biện mạnh nhất chống lại lựa chọn này" }));
        fb.appendChild(U.el("p", { text: steel }));
      }
      // Số liệu khảo sát (nếu có).
      var rows = surveyRows(ex.so_lieu_khao_sat, ex.lua_chon);
      if (rows && rows.length) {
        fb.appendChild(U.el("h4", { text: "Các triết gia chọn thế nào?" }));
        var list = U.el("div", { class: "oz-tn__survey" });
        rows.forEach(function (r) {
          var bar = U.el("div", { class: "oz-tn__bar" });
          bar.appendChild(U.el("span", { class: "oz-tn__bar-label", text: r.nd + " — " + String(r.pct).replace(".", ",") + "%" }));
          var fill = U.el("span", { class: "oz-tn__bar-fill" });
          fill.style.width = Math.max(0, Math.min(100, r.pct)) + "%";
          bar.appendChild(fill);
          list.appendChild(bar);
        });
        fb.appendChild(list);
        var src = ex.so_lieu_khao_sat.nguon || "PhilPapers Survey 2020";
        var note = "Nguồn: " + src + " (khảo sát cuối năm 2020, trước khi ChatGPT ra mắt).";
        if (ex.ghi_chu_khao_sat) note += " " + ex.ghi_chu_khao_sat;
        fb.appendChild(U.el("p", { class: "oz-muted", text: note }));
      } else {
        fb.appendChild(U.el("p", { class: "oz-muted", text: "Chưa có khảo sát đáng tin cậy cho thí nghiệm này." + (ex.ghi_chu_khao_sat ? " " + ex.ghi_chu_khao_sat : "") }));
      }
      if (ex.nguon && ex.nguon.length) {
        fb.appendChild(U.el("p", { class: "oz-muted", text: "Nguồn triết học: " + ex.nguon.join("; ") + "." }));
      }
      var nextBtn = U.el("button", {
        type: "button",
        class: "md-button md-button--primary",
        text: idx + 1 >= order.length ? "Xem kết thúc" : "Thí nghiệm tiếp theo",
        onclick: function () {
          idx++;
          next();
        },
      });
      fb.appendChild(U.el("div", { class: "oz-actions" }, [nextBtn]));
      nextBtn.focus();
      say("Bạn chọn: " + c.nd + ". " + (steel ? "Hãy đọc phản biện mạnh nhất." : ""));
      // Cố ý KHÔNG gọi P.record: không có đáp án đúng thì không chấm điểm.
    }

    next();
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-thi-nghiem"), init);
  }

  return { surveyRows: surveyRows, choiceById: choiceById, initAll: initAll };
});
