const test = require("node:test");
const assert = require("node:assert/strict");
const L = require("../../docs/assets/js/logic-menh-de.js");

test("parse: các phép nối và độ ưu tiên", () => {
  // ¬P ∧ Q -> R tương đương ((¬P) ∧ Q) -> R
  const ast = L.parse("!P && Q -> R");
  assert.equal(ast.t, "impl");
  assert.equal(ast.l.t, "and");
  assert.equal(ast.l.l.t, "not");
  // -> kết hợp phải: P -> Q -> R = P -> (Q -> R)
  const r = L.parse("P -> Q -> R");
  assert.equal(r.r.t, "impl");
  // ngoặc đổi ưu tiên
  const p = L.parse("P && (Q || R)");
  assert.equal(p.r.t, "or");
});

test("parse: chấp nhận ký hiệu Unicode và chữ thường", () => {
  const a = L.parse("¬P ∧ Q");
  assert.equal(a.t, "and");
  const b = L.parse("p -> q");
  assert.deepEqual(L.varsOf(b), ["P", "Q"]);
  assert.deepEqual(L.varsOf(L.parse("(P1 || Q2) && R")), ["P1", "Q2", "R"]);
});

test("parse: báo lỗi thân thiện với công thức sai", () => {
  for (const bad of ["P ->", "(P && Q", "P &&& Q", "P Q", ""]) {
    assert.throws(() => L.parse(bad), /./, "phải báo lỗi: " + bad);
  }
});

test("evalAst: bảng chân trị các phép nối", () => {
  const T = { P: true, Q: true }, F = { P: false, Q: false }, TF = { P: true, Q: false };
  assert.equal(L.evalAst(L.parse("P && Q"), T), true);
  assert.equal(L.evalAst(L.parse("P && Q"), TF), false);
  assert.equal(L.evalAst(L.parse("P || Q"), F), false);
  assert.equal(L.evalAst(L.parse("P -> Q"), TF), false);
  assert.equal(L.evalAst(L.parse("P -> Q"), F), true); // kéo theo rỗng đúng
  assert.equal(L.evalAst(L.parse("P <-> Q"), TF), false);
  assert.equal(L.evalAst(L.parse("P <-> Q"), F), true);
  assert.equal(L.evalAst(L.parse("P ⊕ Q"), T), false);
  assert.equal(L.evalAst(L.parse("P ⊕ Q"), TF), true);
  assert.equal(L.evalAst(L.parse("!P"), T), false);
});

test("checkArgument: các dạng suy luận kinh điển", () => {
  // Modus Ponens — hợp lệ
  assert.equal(L.checkArgument(["P -> Q", "P"], "Q").valid, true);
  // Modus Tollens — hợp lệ
  assert.equal(L.checkArgument(["P -> Q", "!Q"], "!P").valid, true);
  // Tam đoạn luận giả định — hợp lệ
  assert.equal(L.checkArgument(["P -> Q", "Q -> R"], "P -> R").valid, true);
  // Tam đoạn luận tuyển — hợp lệ
  assert.equal(L.checkArgument(["P || Q", "!P"], "Q").valid, true);
  // Khẳng định hậu kiện — KHÔNG hợp lệ
  const ac = L.checkArgument(["P -> Q", "Q"], "P");
  assert.equal(ac.valid, false);
  assert.ok(ac.counterexample, "phải có phản ví dụ");
  assert.equal(ac.counterexample.P, false);
  assert.equal(ac.counterexample.Q, true);
  // Phủ định tiền kiện — KHÔNG hợp lệ
  assert.equal(L.checkArgument(["P -> Q", "!P"], "!Q").valid, false);
  // Khẳng định một vế của tuyển (hoặc bao hàm) — KHÔNG hợp lệ
  assert.equal(L.checkArgument(["P || Q", "P"], "!Q").valid, false);
});

test("checkArgument: phản ví dụ tìm được phải đúng", () => {
  const cases = [
    [["P -> Q", "Q"], "P"],
    [["P -> Q", "!P"], "!Q"],
    [["P || Q", "P"], "!Q"],
    [["(P -> Q) && (P -> R)", "Q"], "R"],
    [["P -> Q"], "!P -> !Q"],
  ];
  for (const [prems, con] of cases) {
    const r = L.checkArgument(prems, con);
    assert.equal(r.valid, false, prems.join("; ") + " ⊢ " + con + " phải không hợp lệ");
    const ce = r.counterexample;
    for (const p of prems) assert.equal(L.evalAst(L.parse(p), ce), true, "tiền đề phải đúng ở phản ví dụ");
    assert.equal(L.evalAst(L.parse(con), ce), false, "kết luận phải sai ở phản ví dụ");
  }
});

test("truthTable: đủ dòng, đánh dấu phản ví dụ", () => {
  const tt = L.truthTable(["P -> Q", "Q"], "P");
  assert.equal(tt.rows.length, 4);
  const ces = tt.rows.filter((r) => r.isCounterexample);
  assert.equal(ces.length, 1);
  assert.deepEqual([ces[0].assign.P, ces[0].assign.Q], [false, true]);
  const tt2 = L.truthTable(["P -> Q", "P"], "Q");
  assert.ok(tt2.rows.every((r) => !r.isCounterexample), "MP không có phản ví dụ");
});

test("parseAssignment: đọc nhiều cách viết", () => {
  const vars = ["M", "U"];
  assert.deepEqual(L.parseAssignment("M=đúng, U=sai", vars), { M: true, U: false });
  assert.deepEqual(L.parseAssignment("M đúng U sai", vars), { M: true, U: false });
  assert.deepEqual(L.parseAssignment("M=T U=F", vars), { M: true, U: false });
  assert.deepEqual(L.parseAssignment("m: true, u: 0", vars), { M: true, U: false });
  assert.throws(() => L.parseAssignment("M=đúng", vars), /Chưa gán/);
  assert.throws(() => L.parseAssignment("M=đúng, U=sai, X=đúng", vars), /Biến lạ/);
  assert.throws(() => L.parseAssignment("M=maybe, U=sai", vars), /đúng hoặc sai/);
  assert.throws(() => L.parseAssignment("", vars), /Hãy gán/);
});

test("prettify và formatAssignment", () => {
  assert.equal(L.prettify("P -> Q && !R <-> S"), "P → Q ∧ ¬R ↔ S");
  assert.equal(L.formatAssignment({ Q: true, P: false }), "P=sai, Q=đúng");
});
