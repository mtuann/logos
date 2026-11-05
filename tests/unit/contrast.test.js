/* Kiểm chứng tương phản màu WCAG AA (≥ 4.5 cho chữ thường) ở cả chế độ sáng và tối,
 * đọc trực tiếp giá trị từ oz.css. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const css = fs.readFileSync(path.join(__dirname, "../../docs/assets/css/oz.css"), "utf8");

function block(selectorStart) {
  const i = css.indexOf(selectorStart);
  const open = css.indexOf("{", i);
  const close = css.indexOf("}", open);
  const vars = {};
  for (const m of css.slice(open + 1, close).matchAll(/(--[\w-]+):\s*([^;]+);/g)) vars[m[1]] = m[2].trim();
  return vars;
}

function rgb(c) {
  c = c.trim();
  let m = c.match(/^#([0-9a-f]{6})$/i);
  if (m) return [0, 2, 4].map((i) => parseInt(m[1].slice(i, i + 2), 16)).concat(1);
  m = c.match(/^rgba?\(([^)]+)\)$/);
  if (m) {
    const p = m[1].split(",").map(Number);
    return [p[0], p[1], p[2], p[3] === undefined ? 1 : p[3]];
  }
  throw new Error("Không đọc được màu " + c);
}

function over(fg, bg) {
  const a = fg[3];
  return [0, 1, 2].map((i) => fg[i] * a + bg[i] * (1 - a)).concat(1);
}

function lum(c) {
  const [r, g, b] = c.slice(0, 3).map((v) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function ratio(fg, bg) {
  const B = rgb(bg);
  const F = over(rgb(fg), B);
  const [a, b] = [lum(F), lum(B)].sort((x, y) => y - x);
  return (a + 0.05) / (b + 0.05);
}

const light = block(":root,");
const dark = block('[data-md-color-scheme="slate"] {');
const resolve = (v, vars) => (v.startsWith("var(") ? vars[v.slice(4, -1)] : v);

const cases = [
  // [tên, chữ, nền, chế độ]
  ["chữ thường / nền giấy", "rgba(0, 0, 0, 0.87)", "--oz-paper", light],
  ["chữ phụ / nền giấy", "--md-default-fg-color--light", "--oz-paper", light],
  ["chữ phụ / nền ô", "--md-default-fg-color--light", "--oz-soft", light],
  ["liên kết / nền giấy", "--oz-accent", "--oz-paper", light],
  ["liên kết / nền ô", "--oz-accent", "--oz-soft", light],
  ["chữ trắng / nút nhấn", "#ffffff", "--oz-accent", light],
  ["chữ trắng / thanh đầu trang", "#ffffff", "--oz-ink", light],
  ["chữ thường / nền đúng", "rgba(0, 0, 0, 0.87)", "--oz-ok-bg", light],
  ["chữ thường / nền sai", "rgba(0, 0, 0, 0.87)", "--oz-bad-bg", light],
  ["màu báo lỗi / nền ô", "--oz-bad", "--oz-soft", light],
  ["liên kết / nền sai", "--oz-accent", "--oz-bad-bg", light],
  ["liên kết / nền đúng", "--oz-accent", "--oz-ok-bg", light],
  ["chữ thường / nền giấy (tối)", "--md-default-fg-color", "--oz-paper", dark],
  ["chữ phụ / nền giấy (tối)", "--md-default-fg-color--light", "--oz-paper", dark],
  ["chữ phụ / nền ô (tối)", "--md-default-fg-color--light", "--oz-soft", dark],
  ["liên kết / nền giấy (tối)", "--oz-accent", "--oz-paper", dark],
  ["liên kết / nền ô (tối)", "--oz-accent", "--oz-soft", dark],
  ["chữ tối / nút nhấn (tối)", "#1b1b1b", "--oz-accent", dark],
  ["chữ / nền đúng (tối)", "--md-default-fg-color", "--oz-ok-bg", dark],
  ["chữ / nền sai (tối)", "--md-default-fg-color", "--oz-bad-bg", dark],
  ["màu báo lỗi / nền ô (tối)", "--oz-bad", "--oz-soft", dark],
  ["liên kết / nền sai (tối)", "--oz-accent", "--oz-bad-bg", dark],
  ["liên kết / nền đúng (tối)", "--oz-accent", "--oz-ok-bg", dark],
];

for (const [name, fg, bg, vars] of cases) {
  test(`tương phản ≥ 4.5: ${name}`, () => {
    const f = fg.startsWith("--") ? resolve(vars[fg], vars) : fg;
    const b = resolve(vars[bg], vars);
    const r = ratio(f, b);
    assert.ok(r >= 4.5, `${name}: ${r.toFixed(2)} (${f} trên ${b})`);
  });
}
