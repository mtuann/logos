/* Logos Zero — biểu đồ tiến độ.
 * <div class="oz-bieu-do"></div>
 * Vẽ SVG thuần (không thư viện ngoài): cột ngang theo từng kỹ năng (EMA + số câu)
 * và cột đứng cho 14 ngày hoạt động gần nhất. Màu dùng currentColor để hợp sáng/tối.
 * Mẫu UMD của repo: hàm thuần xuất qua module.exports; trình duyệt dùng OZReady(initAll). */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.bieudo = api;
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

  var ACTIVITY_DAYS = 14;

  function pad2(n) {
    return (n < 10 ? "0" : "") + n;
  }

  function isoDate(d) {
    return d.getFullYear() + "-" + pad2(d.getMonth() + 1) + "-" + pad2(d.getDate());
  }

  /* Hàm thuần: state → {skills:[{id,name,pct,n}], activity:[{date,n}]}.
   * todayStr (tùy chọn, "YYYY-MM-DD") để kiểm thử xác định; mặc định là hôm nay. */
  function chartData(state, todayStr) {
    var skills = (state && state.skills) || {};
    var days = (state && state.days) || {};
    var list = Object.keys(skills)
      .map(function (k) {
        var sk = skills[k] || {};
        return {
          id: k,
          name: SKILL_NAMES[k] || k,
          pct: sk.ema === null || sk.ema === undefined ? null : Math.round(sk.ema * 100),
          n: sk.n || 0,
        };
      })
      .filter(function (s) {
        return s.n > 0;
      })
      .sort(function (a, b) {
        return b.n - a.n;
      });

    var end = todayStr ? new Date(todayStr + "T12:00:00") : new Date();
    var activity = [];
    for (var i = ACTIVITY_DAYS - 1; i >= 0; i--) {
      var d = new Date(end.getTime());
      d.setDate(d.getDate() - i);
      var key = isoDate(d);
      var e = days[key] || {};
      activity.push({ date: key, n: e.n || 0 });
    }
    return { skills: list, activity: activity };
  }

  /* --- Vẽ SVG (chỉ chạy trên trình duyệt) --- */
  var SVGNS = "http://www.w3.org/2000/svg";

  function svgEl(tag, attrs, children) {
    var n = document.createElementNS(SVGNS, tag);
    if (attrs)
      Object.keys(attrs).forEach(function (k) {
        n.setAttribute(k, attrs[k]);
      });
    (children || []).forEach(function (c) {
      n.appendChild(c);
    });
    return n;
  }

  function svgText(x, y, str, attrs) {
    var t = svgEl("text", attrs || {});
    t.setAttribute("x", x);
    t.setAttribute("y", y);
    t.textContent = str;
    return t;
  }

  /* Biểu đồ cột ngang: mỗi kỹ năng một hàng (tên | thanh EMA | "n câu · pct%"). */
  function skillsChart(data) {
    var rows = data.skills;
    var W = 360,
      rowH = 26,
      labelW = 118,
      barW = 150;
    var H = rows.length * rowH + 8;
    var svg = svgEl("svg", {
      viewBox: "0 0 " + W + " " + H,
      role: "img",
      "aria-label": "Biểu đồ tiến độ theo kỹ năng",
      class: "oz-bieu-do__skills",
    });
    rows.forEach(function (s, i) {
      var y = i * rowH + 8;
      var g = svgEl("g", {});
      var label = s.name.length > 16 ? s.name.slice(0, 15) + "…" : s.name;
      g.appendChild(svgText(0, y + 15, label, { "font-size": "11", fill: "currentColor" }));
      g.appendChild(
        svgEl("rect", { x: labelW, y: y + 4, width: barW, height: 12, rx: 3, fill: "currentColor", opacity: "0.15" })
      );
      var w = s.pct === null ? 0 : Math.max(2, Math.round((barW * s.pct) / 100));
      var bar = svgEl("rect", { x: labelW, y: y + 4, width: w, height: 12, rx: 3, fill: "currentColor", opacity: "0.75" });
      var tip = svgEl("title", {});
      tip.textContent = s.name + ": " + s.n + " câu" + (s.pct === null ? "" : ", đúng " + s.pct + "%");
      bar.appendChild(tip);
      g.appendChild(bar);
      g.appendChild(
        svgText(labelW + barW + 8, y + 15, s.n + " câu" + (s.pct === null ? "" : " · " + s.pct + "%"), {
          "font-size": "11",
          fill: "currentColor",
          opacity: "0.7",
        })
      );
      svg.appendChild(g);
    });
    return svg;
  }

  /* Biểu đồ cột đứng: số câu trả lời mỗi ngày trong 14 ngày gần nhất. */
  function activityChart(data) {
    var W = 360,
      H = 110,
      padL = 8,
      padB = 18,
      padT = 8;
    var maxN = 1;
    data.activity.forEach(function (a) {
      if (a.n > maxN) maxN = a.n;
    });
    var plotH = H - padB - padT;
    var slot = (W - padL * 2) / data.activity.length;
    var barW = Math.max(4, Math.floor(slot * 0.6));
    var svg = svgEl("svg", {
      viewBox: "0 0 " + W + " " + H,
      role: "img",
      "aria-label": "Biểu đồ hoạt động 14 ngày gần nhất",
      class: "oz-bieu-do__activity",
    });
    data.activity.forEach(function (a, i) {
      var x = padL + i * slot + (slot - barW) / 2;
      var h = Math.round((plotH * a.n) / maxN);
      var g = svgEl("g", {});
      var bar = svgEl("rect", {
        x: x,
        y: padT + plotH - h,
        width: barW,
        height: Math.max(h, a.n > 0 ? 2 : 0),
        rx: 2,
        fill: "currentColor",
        opacity: a.n > 0 ? "0.75" : "0.12",
      });
      var tip = svgEl("title", {});
      tip.textContent = a.date + ": " + a.n + " câu";
      bar.appendChild(tip);
      g.appendChild(bar);
      if (i % 3 === 0 || i === data.activity.length - 1) {
        var parts = a.date.split("-");
        g.appendChild(
          svgText(x + barW / 2, H - 5, parts[2] + "/" + parts[1], {
            "font-size": "9",
            fill: "currentColor",
            opacity: "0.6",
            "text-anchor": "middle",
          })
        );
      }
      svg.appendChild(g);
    });
    return svg;
  }

  function render(box) {
    var U = window.OZ.util;
    var P = window.OZ.progress;
    box.textContent = "";
    var data = chartData(P.load());
    var hasSkills = data.skills.length > 0;
    var hasActivity = data.activity.some(function (a) {
      return a.n > 0;
    });
    if (!hasSkills && !hasActivity) {
      box.appendChild(U.el("p", { class: "oz-muted", text: "Hãy làm vài quiz để thấy biểu đồ." }));
      return;
    }
    if (hasSkills) {
      box.appendChild(U.el("h3", { text: "Theo kỹ năng" }));
      box.appendChild(skillsChart(data));
    }
    if (hasActivity) {
      box.appendChild(U.el("h3", { text: "Hoạt động 14 ngày gần nhất" }));
      box.appendChild(activityChart(data));
    } else {
      box.appendChild(U.el("p", { class: "oz-muted", text: "Chưa có hoạt động nào trong 14 ngày gần nhất." }));
    }
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-bieu-do"), function (box) {
      var U = window.OZ.util;
      if (!U.claim(box)) return;
      render(box);
    });
  }

  return { SKILL_NAMES: SKILL_NAMES, chartData: chartData, initAll: initAll };
});
