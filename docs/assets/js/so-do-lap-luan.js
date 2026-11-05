/* Logos — công cụ sơ đồ lập luận.
 * <div class="oz-so-do"></div>  Dữ liệu: assets/data/lap-luan.json
 * Người dùng gán vai trò cho từng câu (tiền đề / kết luận / giả định ngầm /
 * không liên quan), nộp bài, xem đáp án và cây sơ đồ SVG vẽ từ đáp án đúng.
 * Mẫu UMD của repo: hàm thuần xuất qua module.exports; trình duyệt dùng OZReady(initAll). */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.sodo = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var ROLE_LABEL = {
    "tien-de": "Tiền đề",
    "ket-luan": "Kết luận",
    "gia-dinh-ngam": "Giả định ngầm",
    "khong-lien-quan": "Không liên quan",
  };

  /* Hàm thuần: tách câu trong đoạn văn gốc và câu ứng viên giả định ngầm. */
  function splitItems(passage) {
    var gold = {};
    passage.dap_an.forEach(function (a) {
      gold[a.cau] = a.vai_tro;
    });
    var visible = [];
    var implicit = [];
    passage.cau.forEach(function (c) {
      if (gold[c.id] === "gia-dinh-ngam") implicit.push(c);
      else visible.push(c);
    });
    return { visible: visible, implicit: implicit, gold: gold };
  }

  /* Hàm thuần: các id câu được đánh dấu tranh cãi trong ghi chú. */
  function disputedIds(passage) {
    var note = passage.ghi_chu_tranh_cai || "";
    var ids = [];
    var re = /\bc\d+\b/g;
    var m;
    while ((m = re.exec(note))) {
      if (ids.indexOf(m[0]) < 0) ids.push(m[0]);
    }
    return ids;
  }

  /* Hàm thuần: chấm bài. Điểm tranh cãi: gán khác đáp án vẫn tính đúng + hiện ghi chú. */
  function grade(userRoles, passage) {
    var parts = splitItems(passage);
    var disputed = disputedIds(passage);
    var perItem = [];
    var correct = 0;
    var all = parts.visible.concat(parts.implicit);
    all.forEach(function (c) {
      var gold = parts.gold[c.id];
      var user = userRoles[c.id] || null;
      var isDisputed = disputed.indexOf(c.id) >= 0 && user !== gold;
      var ok = user === gold || isDisputed;
      if (ok) correct++;
      perItem.push({ id: c.id, nd: c.nd, user: user, gold: gold, correct: ok, disputed: isDisputed });
    });
    return {
      perItem: perItem,
      correct: correct,
      total: all.length,
      note: perItem.some(function (p) {
        return p.disputed;
      })
        ? passage.ghi_chu_tranh_cai
        : null,
    };
  }

  /* Hàm thuần: ngắt dòng cho nhãn trong SVG. */
  function wrapLabel(text, max) {
    var words = String(text).split(/\s+/);
    var lines = [];
    var cur = "";
    words.forEach(function (w) {
      if ((cur + " " + w).trim().length > max && cur) {
        lines.push(cur);
        cur = w;
      } else {
        cur = (cur + " " + w).trim();
      }
    });
    if (cur) lines.push(cur);
    if (lines.length > 3) {
      lines = lines.slice(0, 3);
      lines[2] += "…";
    }
    return lines;
  }

  /* Hàm thuần: cây SVG từ đáp án đúng (tiền đề → kết luận; giả định ngầm đứt nét). */
  function treeSVG(passage) {
    var parts = splitItems(passage);
    var gold = parts.gold;
    var nodes = parts.visible
      .concat(parts.implicit)
      .filter(function (c) {
        return gold[c.id] !== "khong-lien-quan";
      });
    var byId = {};
    nodes.forEach(function (n) {
      byId[n.id] = n;
    });
    var concl = nodes.filter(function (n) {
      return gold[n.id] === "ket-luan";
    })[0];
    var others = nodes.filter(function (n) {
      return gold[n.id] !== "ket-luan";
    });

    var W = 620;
    var nodeW = 170;
    var nodeH = 64;
    var gapX = 24;
    var perRow = Math.max(1, Math.floor((W + gapX) / (nodeW + gapX)));
    var rows = Math.ceil(others.length / perRow);
    var H = rows * (nodeH + 56) + nodeH + 40;

    var NS = "http://www.w3.org/2000/svg";
    function mk(tag, attrs, parent) {
      var n = document.createElementNS(NS, tag);
      Object.keys(attrs).forEach(function (k) {
        n.setAttribute(k, attrs[k]);
      });
      if (parent) parent.appendChild(n);
      return n;
    }
    var svg = mk("svg", {
      viewBox: "0 0 " + W + " " + H,
      class: "oz-sodo__tree",
      role: "img",
      "aria-label": "Sơ đồ lập luận của đáp án đúng",
    });
    var defs = mk("defs", {}, svg);
    var marker = mk("marker", { id: "oz-arrow", markerWidth: "8", markerHeight: "8", refX: "7", refY: "4", orient: "auto" }, defs);
    mk("path", { d: "M0,0 L8,4 L0,8 Z", fill: "currentColor" }, marker);

    var pos = {};
    others.forEach(function (n, i) {
      var r = Math.floor(i / perRow);
      var inRow = Math.min(perRow, others.length - r * perRow);
      var c = i % perRow;
      var x = (W - inRow * (nodeW + gapX) + gapX) / 2 + c * (nodeW + gapX);
      var y = 16 + r * (nodeH + 56);
      pos[n.id] = { x: x, y: y };
    });
    if (concl) pos[concl.id] = { x: (W - nodeW) / 2, y: H - nodeH - 16 };

    // Cạnh hỗ trợ.
    passage.dap_an.forEach(function (a) {
      (a.ho_tro || []).forEach(function (t) {
        if (!pos[a.cau] || !pos[t]) return;
        var p1 = pos[a.cau];
        var p2 = pos[t];
        var x1 = p1.x + nodeW / 2;
        var y1 = p1.y + nodeH;
        var x2 = p2.x + nodeW / 2;
        var y2 = p2.y;
        mk(
          "line",
          {
            x1: x1,
            y1: y1,
            x2: x2,
            y2: Math.max(y1 + 4, y2 - 6),
            stroke: "currentColor",
            "stroke-width": "1.5",
            "marker-end": "url(#oz-arrow)",
          },
          svg
        );
      });
    });

    // Hộp nút.
    nodes.forEach(function (n) {
      var p = pos[n.id];
      if (!p) return;
      var implicit = gold[n.id] === "gia-dinh-ngam";
      var g = mk("g", {}, svg);
      mk(
        "rect",
        {
          x: p.x,
          y: p.y,
          width: nodeW,
          height: nodeH,
          rx: "6",
          fill: "none",
          stroke: "currentColor",
          "stroke-width": implicit ? "1.5" : "2",
          "stroke-dasharray": implicit ? "6 4" : "none",
        },
        g
      );
      var lines = wrapLabel(n.nd, 22);
      lines.forEach(function (ln, i) {
        var t = mk(
          "text",
          {
            x: p.x + nodeW / 2,
            y: p.y + 22 + i * 15,
            "text-anchor": "middle",
            "font-size": "11",
            fill: "currentColor",
          },
          g
        );
        t.textContent = ln;
      });
      var tag = mk(
        "text",
        {
          x: p.x + nodeW / 2,
          y: p.y + nodeH - 7,
          "text-anchor": "middle",
          "font-size": "9",
          fill: "currentColor",
          opacity: "0.65",
        },
        g
      );
      tag.textContent = ROLE_LABEL[gold[n.id]];
    });
    return svg;
  }

  function init(box) {
    var U = window.OZ.util;
    if (!U.claim(box)) return;
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Sơ đồ lập luận");
    box.appendChild(U.el("p", { class: "oz-muted", text: "Đang tải đoạn văn…" }));
    U.fetchJSON("assets/data/lap-luan.json")
      .then(function (data) {
        build(box, data.passages || []);
      })
      .catch(function (e) {
        box.textContent = "";
        box.appendChild(U.el("p", { class: "oz-error", text: e.message }));
      });
  }

  function build(box, passages) {
    var U = window.OZ.util;
    var P = window.OZ.progress || window.OZProgress || null;
    var say = U.live(box);
    box.textContent = "";
    if (!passages.length) {
      box.appendChild(U.el("p", { class: "oz-error", text: "Chưa có đoạn văn." }));
      return;
    }
    var order = U.shuffle(passages.map(function (p, i) {
      return i;
    }));
    var idx = 0;
    var progress = U.el("p", { class: "oz-muted" });
    var stage = U.el("div", { class: "oz-sodo__stage" });
    box.appendChild(progress);
    box.appendChild(stage);

    function next() {
      if (idx >= order.length) {
        stage.textContent = "";
        progress.textContent = "Đã làm hết " + order.length + " đoạn.";
        stage.appendChild(U.el("p", { text: "Vẽ được cấu trúc là đã thắng một nửa mọi cuộc tranh luận." }));
        var again = U.el("button", {
          type: "button",
          class: "md-button md-button--primary",
          text: "Làm lại (xáo trộn)",
          onclick: function () {
            idx = 0;
            order = U.shuffle(order);
            next();
          },
        });
        stage.appendChild(U.el("div", { class: "oz-actions" }, [again]));
        return;
      }
      progress.textContent = "Đoạn " + (idx + 1) + "/" + order.length;
      show(passages[order[idx]]);
    }

    function roleRadios(name, options) {
      var wrap = U.el("div", { class: "oz-sodo__roles", role: "radiogroup" });
      options.forEach(function (opt) {
        var id = name + "-" + opt;
        var label = U.el("label", { class: "oz-sodo__role", for: id });
        var radio = U.el("input", { type: "radio", name: name, id: id, value: opt });
        label.appendChild(radio);
        label.appendChild(document.createTextNode(" " + ROLE_LABEL[opt]));
        wrap.appendChild(label);
      });
      return wrap;
    }

    function show(p) {
      var parts = splitItems(p);
      stage.textContent = "";
      var form = U.el("form", { class: "oz-sodo__form" });
      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
      });

      var ol = U.el("ol", { class: "oz-sodo__passage" });
      parts.visible.forEach(function (c, i) {
        ol.appendChild(U.el("li", { text: c.nd, value: i + 1 }));
      });
      form.appendChild(U.el("h3", { text: "Đoạn văn" }));
      form.appendChild(ol);

      form.appendChild(U.el("h4", { text: "Bước 1 — Mỗi câu trong đoạn văn đóng vai trò gì?" }));
      parts.visible.forEach(function (c, i) {
        var fs = U.el("fieldset", { class: "oz-sodo__item" });
        fs.appendChild(U.el("legend", { text: "Câu " + (i + 1) + ": “" + c.nd + "”" }));
        fs.appendChild(roleRadios("sodo-" + p.id + "-" + c.id, ["tien-de", "ket-luan", "khong-lien-quan"]));
        form.appendChild(fs);
      });

      if (parts.implicit.length) {
        form.appendChild(
          U.el("h4", { text: "Bước 2 — Những câu sau KHÔNG có trong đoạn văn. Câu nào là điều lập luận cần nhưng không nói ra?" })
        );
        parts.implicit.forEach(function (c) {
          var fs = U.el("fieldset", { class: "oz-sodo__item" });
          fs.appendChild(U.el("legend", { text: "“" + c.nd + "”" }));
          fs.appendChild(roleRadios("sodo-" + p.id + "-" + c.id, ["gia-dinh-ngam", "khong-lien-quan"]));
          form.appendChild(fs);
        });
      }

      var fb = U.el("div", { "aria-live": "polite" });
      var submit = U.el("button", { type: "button", class: "md-button md-button--primary", text: "Kiểm tra" });
      submit.addEventListener("click", function () {
        submit.disabled = true;
        check(p, parts, form, fb, submit);
      });
      form.appendChild(U.el("div", { class: "oz-actions" }, [submit]));
      form.appendChild(fb);
      stage.appendChild(form);
    }

    function check(p, parts, form, fb, submit) {
      var userRoles = {};
      var all = parts.visible.concat(parts.implicit);
      var unanswered = 0;
      all.forEach(function (c) {
        var sel = form.querySelector('input[name="sodo-' + p.id + "-" + c.id + '"]:checked');
        if (!sel) unanswered++;
        else userRoles[c.id] = sel.value;
      });
      if (unanswered) {
        say("Bạn còn " + unanswered + " câu chưa gán vai trò.");
        var warn = U.el("p", { class: "oz-error", text: "Hãy gán vai trò cho mọi câu rồi bấm Kiểm tra." });
        fb.textContent = "";
        fb.appendChild(warn);
        submit.disabled = false;
        return;
      }
      var res = grade(userRoles, p);
      fb.textContent = "";
      fb.appendChild(U.el("h4", { text: "Kết quả: đúng " + res.correct + "/" + res.total }));
      var ul = U.el("ul", { class: "oz-sodo__feedback" });
      res.perItem.forEach(function (it) {
        var mark = it.correct ? "✓" : "✗";
        var txt = mark + " “" + it.nd + "” — đáp án: " + ROLE_LABEL[it.gold];
        if (it.disputed) txt += " (điểm tranh cãi: cách gán của bạn cũng được chấp nhận)";
        else if (!it.correct && it.user) txt += " (bạn chọn: " + ROLE_LABEL[it.user] + ")";
        var li = U.el("li", { text: txt });
        li.className = it.correct ? "oz-ok" : "oz-bad";
        ul.appendChild(li);
      });
      fb.appendChild(ul);
      if (res.note) {
        fb.appendChild(U.el("p", { class: "oz-muted", text: "Ghi chú: " + res.note }));
      }
      fb.appendChild(U.el("h4", { text: "Sơ đồ của đáp án đúng" }));
      fb.appendChild(treeSVG(p));
      fb.appendChild(U.el("p", { class: "oz-muted", text: "Hộp đứt nét = giả định ngầm (điều lập luận cần nhưng không nói ra)." }));

      var ok = res.correct === res.total;
      if (P && P.record) P.record("argument", ok, "sodo:" + p.id);
      var nextBtn = U.el("button", {
        type: "button",
        class: "md-button md-button--primary",
        text: idx + 1 >= order.length ? "Xem kết thúc" : "Đoạn tiếp theo",
        onclick: function () {
          idx++;
          next();
        },
      });
      fb.appendChild(U.el("div", { class: "oz-actions" }, [nextBtn]));
      nextBtn.focus();
      say("Đúng " + res.correct + " trên " + res.total + " câu.");
    }

    next();
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-so-do"), init);
  }

  return {
    splitItems: splitItems,
    disputedIds: disputedIds,
    grade: grade,
    wrapLabel: wrapLabel,
    initAll: initAll,
  };
});
