/* Logos — công cụ logic mệnh đề: kiểm tra tính hợp lệ, tìm phản ví dụ.
 * <div class="oz-logic"></div> — hai tab: "Tự kiểm tra" (nhập tự do) và "Luyện tập" (ngân hàng logic.json).
 * CHỈ xử lý logic mệnh đề (không có lượng từ, vị từ) — UI ghi rõ giới hạn này.
 * Mẫu UMD của repo: hàm thuần xuất qua module.exports; trình duyệt dùng OZReady(initAll). */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.logic = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* ================= Phần thuần (kiểm thử được) ================= */

  function err(message) {
    return new Error(message);
  }

  /* Tách chuỗi công thức thành token. Chấp nhận ASCII và ký hiệu Unicode. */
  function tokenize(src) {
    var tokens = [];
    var i = 0;
    while (i < src.length) {
      var c = src[i];
      if (/\s/.test(c)) {
        i++;
        continue;
      }
      var rest = src.slice(i);
      var m;
      if (/^<->/.test(rest)) {
        tokens.push({ t: "iff" });
        i += 3;
      } else if (/^->/.test(rest)) {
        tokens.push({ t: "impl" });
        i += 2;
      } else if (/^&&/.test(rest)) {
        tokens.push({ t: "and" });
        i += 2;
      } else if (/^\|\|/.test(rest)) {
        tokens.push({ t: "or" });
        i += 2;
      } else if (c === "(" || c === ")") {
        tokens.push({ t: c });
        i++;
      } else if (c === "!" || c === "~" || c === "¬") {
        tokens.push({ t: "not" });
        i++;
      } else if (c === "&" || c === "∧") {
        tokens.push({ t: "and" });
        i++;
      } else if (c === "|" || c === "∨") {
        tokens.push({ t: "or" });
        i++;
      } else if (c === "⊕" || c === "^") {
        tokens.push({ t: "xor" });
        i++;
      } else if (c === "→") {
        tokens.push({ t: "impl" });
        i++;
      } else if (c === "↔") {
        tokens.push({ t: "iff" });
        i++;
      } else if ((m = /^[A-Za-z][0-9]*/.exec(rest))) {
        tokens.push({ t: "var", name: m[0].toUpperCase() });
        i += m[0].length;
      } else {
        throw err("Ký tự lạ: '" + c + "'");
      }
    }
    tokens.push({ t: "eof" });
    return tokens;
  }

  /* Ngữ pháp (độ ưu tiên tăng dần): ↔ | → (kết hợp phải) | ∨, ⊕ | ∧ | ¬ | atom */
  function parse(src) {
    var tokens = tokenize(src);
    var pos = 0;
    function peek() {
      return tokens[pos];
    }
    function next() {
      return tokens[pos++];
    }
    function parseIff() {
      var l = parseImpl();
      while (peek().t === "iff") {
        next();
        l = { t: "iff", l: l, r: parseImpl() };
      }
      return l;
    }
    function parseImpl() {
      var l = parseOr();
      if (peek().t === "impl") {
        next();
        return { t: "impl", l: l, r: parseImpl() };
      }
      return l;
    }
    function parseOr() {
      var l = parseAnd();
      for (;;) {
        var t = peek().t;
        if (t === "or" || t === "xor") {
          next();
          l = { t: t, l: l, r: parseAnd() };
        } else return l;
      }
    }
    function parseAnd() {
      var l = parseNot();
      while (peek().t === "and") {
        next();
        l = { t: "and", l: l, r: parseNot() };
      }
      return l;
    }
    function parseNot() {
      if (peek().t === "not") {
        next();
        return { t: "not", x: parseNot() };
      }
      return parseAtom();
    }
    function parseAtom() {
      var tk = peek();
      if (tk.t === "var") {
        next();
        return { t: "var", name: tk.name };
      }
      if (tk.t === "(") {
        next();
        var e = parseIff();
        if (peek().t !== ")") throw err("Thiếu dấu đóng ngoặc ')'");
        next();
        return e;
      }
      throw err("Chỗ này cần một mệnh đề (chữ cái in hoa) hoặc dấu '('");
    }
    var ast = parseIff();
    if (peek().t !== "eof") throw err("Thừa ký tự sau công thức — kiểm tra lại");
    return ast;
  }

  function evalAst(node, assign) {
    switch (node.t) {
      case "var":
        return !!assign[node.name];
      case "not":
        return !evalAst(node.x, assign);
      case "and":
        return evalAst(node.l, assign) && evalAst(node.r, assign);
      case "or":
        return evalAst(node.l, assign) || evalAst(node.r, assign);
      case "xor":
        return evalAst(node.l, assign) !== evalAst(node.r, assign);
      case "impl":
        return !evalAst(node.l, assign) || evalAst(node.r, assign);
      case "iff":
        return evalAst(node.l, assign) === evalAst(node.r, assign);
    }
    throw err("Cây cú pháp lạ");
  }

  function varsOf(node) {
    var acc = {};
    (function walk(n) {
      if (n.t === "var") acc[n.name] = true;
      else {
        if (n.x) walk(n.x);
        if (n.l) walk(n.l);
        if (n.r) walk(n.r);
      }
    })(node);
    return Object.keys(acc).sort();
  }

  /* Kiểm tra lập luận bằng bảng chân trị đầy đủ.
   * Trả về { valid, counterexample (gán đúng/sai) | null, vars, rows }. */
  function checkArgument(premiseSrcs, conclusionSrc) {
    if (!premiseSrcs.length) throw err("Cần ít nhất một tiền đề");
    var premises = premiseSrcs.map(parse);
    var conclusion = parse(conclusionSrc);
    var seen = {};
    var vars = [];
    premises
      .concat([conclusion])
      .forEach(function (p) {
        varsOf(p).forEach(function (v) {
          if (!seen[v]) {
            seen[v] = true;
            vars.push(v);
          }
        });
      });
    vars.sort();
    var n = vars.length;
    var total = Math.pow(2, n);
    var counterexample = null;
    for (var i = 0; i < total && !counterexample; i++) {
      var assign = {};
      for (var j = 0; j < n; j++) assign[vars[j]] = !!(i & (1 << (n - 1 - j)));
      var allTrue = premises.every(function (p) {
        return evalAst(p, assign);
      });
      if (allTrue && !evalAst(conclusion, assign)) counterexample = assign;
    }
    return { valid: counterexample === null, counterexample: counterexample, vars: vars, rows: total };
  }

  /* Liệt kê mọi dòng của bảng chân trị (để vẽ bảng). */
  function truthTable(premiseSrcs, conclusionSrc) {
    var premises = premiseSrcs.map(parse);
    var conclusion = parse(conclusionSrc);
    var seen = {};
    var vars = [];
    premises
      .concat([conclusion])
      .forEach(function (p) {
        varsOf(p).forEach(function (v) {
          if (!seen[v]) {
            seen[v] = true;
            vars.push(v);
          }
        });
      });
    vars.sort();
    var rows = [];
    var total = Math.pow(2, vars.length);
    for (var i = 0; i < total; i++) {
      var assign = {};
      for (var j = 0; j < vars.length; j++) assign[vars[j]] = !!(i & (1 << (vars.length - 1 - j)));
      var pVals = premises.map(function (p) {
        return evalAst(p, assign);
      });
      var cVal = evalAst(conclusion, assign);
      rows.push({
        assign: assign,
        premises: pVals,
        conclusion: cVal,
        isCounterexample: pVals.every(Boolean) && !cVal,
      });
    }
    return { vars: vars, rows: rows };
  }

  var PRETTY = [
    ["<->", "↔"],
    ["->", "→"],
    ["&&", "∧"],
    ["||", "∨"],
    ["!", "¬"],
  ];

  /* ASCII -> ký hiệu đẹp để hiển thị. */
  function prettify(src) {
    var out = src;
    PRETTY.forEach(function (p) {
      out = out.split(p[0]).join(p[1]);
    });
    return out;
  }

  function formatAssignment(assign) {
    return Object.keys(assign)
      .sort()
      .map(function (v) {
        return v + "=" + (assign[v] ? "đúng" : "sai");
      })
      .join(", ");
  }

  /* Đọc cách gán do người dùng nhập: "M=đúng, U=sai" | "M đúng U sai" | "M=T U=F". */
  function parseAssignment(input, vars) {
    var TRUE = { đúng: 1, dung: 1, d: 1, t: 1, true: 1, 1: 1 };
    var FALSE = { sai: 1, f: 1, false: 1, 0: 1 };
    function isVal(s) {
      var k = s.toLowerCase();
      return k in TRUE || k in FALSE;
    }
    var norm = String(input).replace(/[;:]/g, "=").replace(/,/g, " ").replace(/=\s+/g, "=").trim();
    if (!norm) throw err("Hãy gán đúng/sai cho các biến, ví dụ: M=đúng, U=sai");
    var raw = norm.split(/\s+/);
    var parts = [];
    for (var i = 0; i < raw.length; i++) {
      var cur = raw[i];
      var nxt = raw[i + 1];
      if (/^[A-Za-z][0-9]*$/.test(cur) && nxt && isVal(nxt)) {
        parts.push(cur + "=" + nxt);
        i++;
      } else parts.push(cur);
    }
    var assign = {};
    parts.forEach(function (p) {
      var m = /^([A-Za-z][0-9]*)=(\S+)$/.exec(p);
      if (!m) throw err("Không hiểu '" + p + "' — viết dạng M=đúng, U=sai");
      var v = m[1].toUpperCase();
      var val = m[2].toLowerCase();
      if (val in TRUE) assign[v] = true;
      else if (val in FALSE) assign[v] = false;
      else throw err("'" + m[2] + "' phải là đúng hoặc sai");
    });
    var missing = vars.filter(function (v) {
      return !(v in assign);
    });
    if (missing.length) throw err("Chưa gán giá trị cho: " + missing.join(", "));
    var extra = Object.keys(assign).filter(function (v) {
      return vars.indexOf(v) < 0;
    });
    if (extra.length) throw err("Biến lạ (không có trong lập luận): " + extra.join(", "));
    return assign;
  }

  /* ================= Phần giao diện ================= */

  var MAX_VARS = 5; // quá 5 biến (32 dòng) thì không vẽ bảng, chỉ kiểm tra

  function boolText(b) {
    return b ? "Đ" : "S";
  }

  function showMsg(el, text, isError) {
    el.textContent = "";
    el.appendChild(el.ownerDocument.createTextNode(text));
    el.classList.remove("oz-logic__msg--ok", "oz-logic__msg--error");
    el.classList.add(isError ? "oz-logic__msg--error" : "oz-logic__msg--ok");
  }

  function renderTable(U, box, tt, premiseSrcs, conclusionSrc) {
    var table = U.el("table", { class: "oz-table oz-logic__table" });
    var head = U.el("tr", null, []);
    tt.vars.forEach(function (v) {
      head.appendChild(U.el("th", { scope: "col", text: v }));
    });
    premiseSrcs.forEach(function (p, i) {
      head.appendChild(U.el("th", { scope: "col", text: "TĐ" + (i + 1) + " " + prettify(p), title: prettify(p) }));
    });
    head.appendChild(U.el("th", { scope: "col", text: "KL " + prettify(conclusionSrc), title: prettify(conclusionSrc) }));
    table.appendChild(U.el("thead", null, [head]));
    var body = U.el("tbody", null, []);
    tt.rows.forEach(function (r) {
      var tr = U.el("tr", { class: r.isCounterexample ? "oz-logic__ce" : "" });
      tt.vars.forEach(function (v) {
        tr.appendChild(U.el("td", { text: boolText(r.assign[v]) }));
      });
      r.premises.forEach(function (p) {
        tr.appendChild(U.el("td", { text: boolText(p) }));
      });
      tr.appendChild(U.el("td", { text: boolText(r.conclusion) }));
      body.appendChild(tr);
    });
    table.appendChild(body);
    return table;
  }

  function freeMode(U, P, pane) {
    var say = U.live(pane);
    pane.appendChild(
      U.el("p", { class: "oz-muted", text: "Nhập mỗi tiền đề một dòng, rồi nhập kết luận. Dùng chữ cái in hoa cho mệnh đề đơn (P, Q…)." })
    );
    var opHelp = U.el("p", { class: "oz-muted" });
    opHelp.innerHTML =
      "Phép nối: <code>!</code> phủ định · <code>&amp;&amp;</code> và · <code>||</code> hoặc · " +
      "<code>-&gt;</code> kéo theo · <code>&lt;-&gt;</code> khi và chỉ khi · <code>⊕</code> hoặc loại trừ";
    pane.appendChild(opHelp);
    var preTa = U.el("textarea", {
      class: "oz-logic__premises",
      rows: "3",
      placeholder: "P -> Q\nP",
      "aria-label": "Các tiền đề, mỗi tiền đề một dòng",
    });
    var conInput = U.el("input", {
      class: "oz-logic__conclusion",
      type: "text",
      placeholder: "Q",
      "aria-label": "Kết luận",
    });
    var checkBtn = U.el("button", { type: "button", class: "md-button md-button--primary", text: "Kiểm tra tính hợp lệ" });
    var result = U.el("div", { class: "oz-logic__result", "aria-live": "polite" });
    pane.appendChild(U.el("p", null, [U.el("strong", { text: "Tiền đề:" }), preTa]));
    pane.appendChild(U.el("p", null, [U.el("strong", { text: "Kết luận:" }), conInput]));
    pane.appendChild(U.el("div", { class: "oz-actions" }, [checkBtn]));
    pane.appendChild(result);

    checkBtn.addEventListener("click", function () {
      result.textContent = "";
      var premiseSrcs = preTa.value
        .split("\n")
        .map(function (s) {
          return s.trim();
        })
        .filter(Boolean);
      var conclusionSrc = conInput.value.trim();
      try {
        if (!premiseSrcs.length) throw err("Hãy nhập ít nhất một tiền đề.");
        if (!conclusionSrc) throw err("Hãy nhập kết luận.");
        var r = checkArgument(premiseSrcs, conclusionSrc);
        if (r.vars.length > MAX_VARS)
          throw err("Lập luận có " + r.vars.length + " biến (" + r.vars.join(", ") + ") — công cụ chỉ vẽ bảng tới 5 biến. Hãy rút gọn.");
        var verdict = U.el("p", {
          class: r.valid ? "oz-logic__verdict oz-logic__verdict--valid" : "oz-logic__verdict oz-logic__verdict--invalid",
          text: r.valid ? "HỢP LỆ — mọi dòng làm các tiền đề đúng đều làm kết luận đúng." : "KHÔNG HỢP LỆ — đã tìm thấy phản ví dụ:",
        });
        result.appendChild(verdict);
        if (!r.valid) {
          result.appendChild(U.el("p", { text: "Phản ví dụ: " + formatAssignment(r.counterexample) }));
          result.appendChild(
            U.el("p", { class: "oz-muted", text: "Với cách gán này, mọi tiền đề đều đúng nhưng kết luận sai — các dòng đó được tô màu trong bảng." })
          );
        }
        var tt = truthTable(premiseSrcs, conclusionSrc);
        result.appendChild(renderTable(U, pane, tt, premiseSrcs, conclusionSrc));
        say(r.valid ? "Lập luận hợp lệ." : "Lập luận không hợp lệ. Đã tìm thấy phản ví dụ.");
      } catch (e) {
        showMsg(result, e.message || "Lỗi không rõ.", true);
        say(e.message || "Lỗi không rõ.");
      }
    });
  }

  function practiceMode(U, P, pane) {
    var say = U.live(pane);
    pane.appendChild(U.el("p", { class: "oz-muted", text: "Đang tải bài tập…" }));
    U.fetchJSON("assets/data/logic.json")
      .then(function (data) {
        buildPractice(U, P, pane, say, data.exercises || data.questions || []);
      })
      .catch(function (e) {
        pane.textContent = "";
        pane.appendChild(U.el("p", { class: "oz-error", text: e.message }));
      });
  }

  function buildPractice(U, P, pane, say, exercises) {
    pane.textContent = "";
    if (!exercises.length) {
      pane.appendChild(U.el("p", { class: "oz-error", text: "Chưa có bài tập." }));
      return;
    }
    var order = U.shuffle(exercises.map(function (e, i) {
      return i;
    }));
    var idx = 0;
    var done = 0;
    var stage = U.el("div", { class: "oz-logic__stage" });
    var progress = U.el("p", { class: "oz-muted" });
    pane.appendChild(progress);
    pane.appendChild(stage);

    function renderProgress() {
      progress.textContent = "Câu " + Math.min(idx + 1, order.length) + "/" + order.length + " · đã xong " + done;
    }

    function next() {
      if (idx >= order.length) {
        stage.textContent = "";
        stage.appendChild(U.el("p", { text: "Hết bài tập! Bạn đã làm " + done + "/" + order.length + " câu." }));
        var again = U.el("button", {
          type: "button",
          class: "md-button md-button--primary",
          text: "Làm lại (xáo trộn)",
          onclick: function () {
            idx = 0;
            done = 0;
            order = U.shuffle(order);
            next();
          },
        });
        stage.appendChild(U.el("div", { class: "oz-actions" }, [again]));
        renderProgress();
        return;
      }
      renderProgress();
      askValidity(exercises[order[idx]]);
    }

    function askValidity(ex) {
      stage.textContent = "";
      var r;
      try {
        r = checkArgument(ex.premises, ex.conclusion);
      } catch (e) {
        stage.appendChild(U.el("p", { class: "oz-error", text: "Bài " + ex.id + " lỗi công thức: " + e.message }));
        var skip = U.el("button", {
          type: "button",
          class: "md-button",
          text: "Bỏ qua",
          onclick: function () {
            idx++;
            next();
          },
        });
        stage.appendChild(U.el("div", { class: "oz-actions" }, [skip]));
        return;
      }
      stage.appendChild(U.el("p", { class: "oz-logic__debai", text: ex.de_bai }));
      var formula = U.el("p", { class: "oz-logic__formula" });
      ex.premises.forEach(function (p) {
        formula.appendChild(U.el("div", { text: "Tiền đề: " + prettify(p) }));
      });
      formula.appendChild(U.el("div", { text: "Kết luận: " + prettify(ex.conclusion) }));
      stage.appendChild(formula);
      var fb = U.el("div", { "aria-live": "polite" });
      var btnValid = U.el("button", { type: "button", class: "md-button md-button--primary", text: "Hợp lệ" });
      var btnInvalid = U.el("button", { type: "button", class: "md-button", text: "Không hợp lệ" });
      function answer(userSaysValid) {
        var actuallyValid = r.valid;
        var judgmentRight = userSaysValid === actuallyValid;
        btnValid.disabled = true;
        btnInvalid.disabled = true;
        if (!judgmentRight) {
          fb.appendChild(
            U.el("p", {
              class: "oz-logic__msg oz-logic__msg--error",
              text: "Chưa đúng — lập luận này " + (actuallyValid ? "HỢP LỆ." : "KHÔNG HỢP LỆ."),
            })
          );
          showExplanation(fb, ex, r);
          finish(false);
          return;
        }
        if (actuallyValid) {
          fb.appendChild(U.el("p", { class: "oz-logic__msg oz-logic__msg--ok", text: "Đúng — lập luận hợp lệ." }));
          showExplanation(fb, ex, r);
          finish(true);
        } else {
          fb.appendChild(
            U.el("p", { class: "oz-logic__msg oz-logic__msg--ok", text: "Đúng — lập luận không hợp lệ. Giờ hãy tìm một phản ví dụ." })
          );
          askCounterexample(ex, r, fb);
        }
      }
      btnValid.addEventListener("click", function () {
        answer(true);
      });
      btnInvalid.addEventListener("click", function () {
        answer(false);
      });
      stage.appendChild(U.el("div", { class: "oz-actions" }, [btnValid, btnInvalid]));
      stage.appendChild(fb);

      function finish(ok) {
        if (P) P.record("logic", ok, "logic:" + ex.id);
        done++;
        var nextBtn = U.el("button", {
          type: "button",
          class: "md-button md-button--primary",
          text: idx + 1 >= order.length ? "Xem kết quả" : "Câu tiếp theo",
          onclick: function () {
            idx++;
            next();
          },
        });
        stage.appendChild(U.el("div", { class: "oz-actions" }, [nextBtn]));
        var b = stage.querySelector(".oz-actions:last-child button");
        if (b) b.focus();
        say(ok ? "Đúng." : "Chưa đúng. " + ex.giai_thich);
      }
    }

    function askCounterexample(ex, r, fb) {
      var wrap = U.el("div", { class: "oz-logic__ce-ask" });
      wrap.appendChild(
        U.el("p", {
          class: "oz-muted",
          text: "Gán ĐÚNG/SAI cho " + r.vars.join(", ") + " sao cho mọi tiền đề đúng mà kết luận sai. Ví dụ: " + r.vars[0] + "=đúng" + (r.vars[1] ? ", " + r.vars[1] + "=sai" : ""),
        })
      );
      var input = U.el("input", { type: "text", class: "oz-logic__ce-input", "aria-label": "Phản ví dụ của bạn" });
      var checkBtn = U.el("button", { type: "button", class: "md-button md-button--primary", text: "Kiểm tra phản ví dụ" });
      var msg = U.el("div", { "aria-live": "polite" });
      wrap.appendChild(input);
      wrap.appendChild(U.el("div", { class: "oz-actions" }, [checkBtn]));
      wrap.appendChild(msg);
      fb.appendChild(wrap);
      input.focus();

      function finishCE(ok) {
        if (P) P.record("logic", ok, "logic:" + ex.id);
        done++;
        var nextBtn = U.el("button", {
          type: "button",
          class: "md-button md-button--primary",
          text: idx + 1 >= order.length ? "Xem kết quả" : "Câu tiếp theo",
          onclick: function () {
            idx++;
            next();
          },
        });
        fb.appendChild(U.el("div", { class: "oz-actions" }, [nextBtn]));
        nextBtn.focus();
      }

      checkBtn.addEventListener("click", function () {
        msg.textContent = "";
        try {
          var assign = parseAssignment(input.value, r.vars);
          var premises = ex.premises.map(parse);
          var conclusion = parse(ex.conclusion);
          var pVals = premises.map(function (p) {
            return evalAst(p, assign);
          });
          var cVal = evalAst(conclusion, assign);
          if (pVals.every(Boolean) && !cVal) {
            showMsg(msg, "Đúng — đây là một phản ví dụ hợp lệ.", false);
            showExplanation(fb, ex, r);
            checkBtn.disabled = true;
            say("Phản ví dụ đúng.");
            finishCE(true);
          } else {
            var why = !pVals.every(Boolean)
              ? "có tiền đề bị sai"
              : "kết luận vẫn đúng";
            showMsg(msg, "Chưa phải phản ví dụ: với cách gán này " + why + ". Thử lại.", true);
            say("Chưa phải phản ví dụ.");
          }
        } catch (e) {
          showMsg(msg, e.message || "Lỗi không rõ.", true);
        }
      });
    }

    function showExplanation(container, ex, r) {
      container.appendChild(U.el("p", { text: "Giải thích: " + ex.giai_thich }));
      if (!r.valid && r.counterexample) {
        container.appendChild(U.el("p", { class: "oz-muted", text: "Một phản ví dụ: " + formatAssignment(r.counterexample) }));
      }
    }

    next();
  }

  function init(box) {
    var U = window.OZ.util;
    if (!U.claim(box)) return;
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Công cụ logic mệnh đề");
    var tabs = U.el("div", { class: "oz-tabs", role: "tablist" });
    var panes = {};
    [["tu-do", "Tự kiểm tra"], ["luyen-tap", "Luyện tập"]].forEach(function (pair, i) {
      var id = pair[0],
        label = pair[1];
      var tab = U.el("button", {
        type: "button",
        role: "tab",
        "aria-selected": i === 0 ? "true" : "false",
        class: "oz-tab" + (i === 0 ? " is-active" : ""),
        text: label,
      });
      var pane = U.el("div", { class: "oz-logic__pane", role: "tabpanel", hidden: i !== 0 });
      panes[id] = { tab: tab, pane: pane };
      tab.addEventListener("click", function () {
        Object.keys(panes).forEach(function (k) {
          var active = k === id;
          panes[k].tab.setAttribute("aria-selected", active ? "true" : "false");
          panes[k].tab.classList.toggle("is-active", active);
          panes[k].pane.hidden = !active;
        });
      });
      tabs.appendChild(tab);
      box.appendChild(pane);
    });
    box.insertBefore(tabs, box.firstChild);
    var P = window.OZ.progress;
    freeMode(U, P, panes["tu-do"].pane);
    practiceMode(U, P, panes["luyen-tap"].pane);
    box.appendChild(
      U.el(
        "p",
        { class: "oz-muted" },
        [
          U.el("strong", { text: "Giới hạn: " }),
          box.ownerDocument.createTextNode("công cụ chỉ xử lý logic mệnh đề (Đúng/Sai, phép nối). "),
          box.ownerDocument.createTextNode("Nó không hiểu lượng từ (\u201CMọi\u201D, \u201CTồn tại\u201D) hay vị từ \u2014 đó là logic vị từ, vượt ngoài phạm vi."),
        ]
      )
    );
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-logic"), init);
  }

  return {
    parse: parse,
    tokenize: tokenize,
    evalAst: evalAst,
    varsOf: varsOf,
    checkArgument: checkArgument,
    truthTable: truthTable,
    prettify: prettify,
    formatAssignment: formatAssignment,
    parseAssignment: parseAssignment,
    MAX_VARS: MAX_VARS,
    initAll: initAll,
  };
});
