/* Logos Zero — quiz "Tự kiểm tra".
 * Dữ liệu: <div class="oz-quiz" data-id data-skill><script type="application/json">[…]</script></div> */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.quiz = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* Hàm thuần: chấm điểm. answers[i] là chỉ số lựa chọn hoặc null. */
  function grade(questions, answers) {
    var results = questions.map(function (q, i) {
      var a = answers[i];
      return { answered: a !== null && a !== undefined, correct: a === q.answer };
    });
    var score = results.filter(function (r) {
      return r.correct;
    }).length;
    return { score: score, total: questions.length, results: results };
  }

  function validate(questions) {
    if (!Array.isArray(questions) || !questions.length) return "Quiz rỗng";
    for (var i = 0; i < questions.length; i++) {
      var q = questions[i];
      if (!q || typeof q.q !== "string" || !Array.isArray(q.options) || q.options.length < 2)
        return "Câu " + (i + 1) + " thiếu nội dung";
      if (typeof q.answer !== "number" || q.answer < 0 || q.answer >= q.options.length)
        return "Câu " + (i + 1) + " có đáp án ngoài phạm vi";
      if (typeof q.explain !== "string" || !q.explain) return "Câu " + (i + 1) + " thiếu giải thích";
    }
    return null;
  }

  function init(box) {
    var U = window.OZ.util;
    if (!U.claim(box)) return;
    var src = box.querySelector('script[type="application/json"]');
    var questions;
    try {
      questions = JSON.parse(src.textContent);
    } catch (e) {
      box.appendChild(U.el("p", { class: "oz-error", text: "Không đọc được dữ liệu quiz." }));
      return;
    }
    var err = validate(questions);
    if (err) {
      box.appendChild(U.el("p", { class: "oz-error", text: err }));
      return;
    }
    var qid = box.dataset.id || "quiz";
    var skill = box.dataset.skill || "general";
    var say = U.live(box);
    var form = U.el("form", { class: "oz-quiz__form", novalidate: true });
    var feedbacks = [];

    questions.forEach(function (q, i) {
      var name = "oz-" + qid + "-" + i;
      var fs = U.el("fieldset", { class: "oz-quiz__q" }, [
        U.el("legend", null, [U.el("span", { class: "oz-quiz__num", text: "Câu " + (i + 1) + ". " }), q.q]),
      ]);
      q.options.forEach(function (opt, j) {
        var id = name + "-" + j;
        fs.appendChild(
          U.el("div", { class: "oz-choice" }, [
            U.el("input", { type: "radio", name: name, id: id, value: String(j) }),
            U.el("label", { for: id, text: opt }),
          ])
        );
      });
      var fb = U.el("div", { class: "oz-quiz__fb", hidden: true });
      feedbacks.push(fb);
      fs.appendChild(fb);
      form.appendChild(fs);
    });

    var result = U.el("p", { class: "oz-quiz__result", hidden: true });
    var check = U.el("button", { type: "submit", class: "md-button md-button--primary", text: "Xem kết quả" });
    var reset = U.el("button", { type: "button", class: "md-button", text: "Làm lại", hidden: true });
    form.appendChild(U.el("div", { class: "oz-actions" }, [check, reset]));
    form.appendChild(result);

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var answers = questions.map(function (q, i) {
        var c = form.querySelector('input[name="oz-' + qid + "-" + i + '"]:checked');
        return c ? Number(c.value) : null;
      });
      var g = grade(questions, answers);
      g.results.forEach(function (r, i) {
        var fb = feedbacks[i];
        fb.hidden = false;
        fb.className = "oz-quiz__fb " + (r.correct ? "is-correct" : "is-wrong");
        fb.textContent = "";
        var head = r.correct ? "Đúng. " : r.answered ? "Chưa đúng. " : "Bạn chưa chọn. ";
        if (!r.correct) head += "Đáp án: " + questions[i].options[questions[i].answer] + ". ";
        fb.appendChild(U.el("strong", { text: head }));
        fb.appendChild(document.createTextNode(questions[i].explain));
      });
      result.hidden = false;
      result.textContent = "Bạn trả lời đúng " + g.score + "/" + g.total + " câu.";
      say(result.textContent);
      reset.hidden = false;
      var P = window.OZ.progress;
      if (P) {
        P.update(function (s) {
          g.results.forEach(function (r, i) {
            if (r.answered) s = P.applyAnswer(s, skill, r.correct, P.today(), qid + ":" + i);
          });
          return P.applyQuiz(s, qid, g.score, g.total);
        });
      }
    });

    reset.addEventListener("click", function () {
      form.reset();
      feedbacks.forEach(function (fb) {
        fb.hidden = true;
      });
      result.hidden = true;
      reset.hidden = true;
      var first = form.querySelector("input");
      if (first) first.focus();
    });

    box.appendChild(form);
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-quiz"), init);
  }

  return { grade: grade, validate: validate, init: init, initAll: initAll };
});
