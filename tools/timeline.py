"""Sinh trang Dòng thời gian (docs/lich-su/dong-thoi-gian.md) từ
docs/assets/data/philosophers.json.

Nội dung sinh ra nằm giữa hai dấu <!-- gen:timeline --> và <!-- /gen:timeline -->.
    python tools/timeline.py          # ghi lại trang
    python tools/timeline.py --check  # báo lỗi (mã thoát 1) nếu trang lệch dữ liệu
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "assets" / "data" / "philosophers.json"
PAGE = ROOT / "docs" / "lich-su" / "dong-thoi-gian.md"
START, END = "<!-- gen:timeline -->", "<!-- /gen:timeline -->"

T0, T1 = -600, 2026  # trục thời gian
W = 1200
X0, X1 = 215, 1170  # vùng vẽ (sau cột tên)
ROW_H = 26
TOP_PAD = 56  # chỗ cho chú thích màu
AXIS_H = 44

# Màu theo trường phái (đủ phân biệt trên cả nền sáng và tối).
SCHOOL_COLORS = {
    "Tiền Socrates": "#bab0ac",
    "Hy Lạp cổ đại": "#4e79a7",
    "La Mã": "#ff9da7",
    "Trung cổ": "#9c755f",
    "Cận đại": "#f28e2b",
    "Thế kỷ 19": "#e15759",
    "Thế kỷ 20": "#59a14f",
    "Trung Hoa": "#edc948",
    "Ấn Độ": "#b07aa1",
    "Việt Nam": "#76b7b2",
}

SCHOOL_ORDER = list(SCHOOL_COLORS.keys())


def validate(data: list) -> list[str]:
    errors = []
    seen = set()
    for p in data:
        for k in ("id", "name", "name_en", "years", "start", "end", "school", "summary", "influence"):
            if k not in p:
                errors.append(f"{p.get('id', '?')}: thiếu {k}")
        if p.get("id") in seen:
            errors.append(f"{p['id']}: id trùng")
        seen.add(p.get("id"))
        if p.get("school") not in SCHOOL_COLORS:
            errors.append(f"{p.get('id')}: school lạ: {p.get('school')}")
        if not (isinstance(p.get("start"), int) and isinstance(p.get("end"), int)):
            errors.append(f"{p.get('id')}: start/end phải là số nguyên")
        elif p["start"] >= p["end"]:
            errors.append(f"{p['id']}: start >= end")
        for inf in p.get("influence", []):
            if inf not in seen and inf not in [q.get("id") for q in data]:
                errors.append(f"{p.get('id')}: influence lạ: {inf}")
    return errors


def x(year: float) -> float:
    return X0 + (year - T0) / (T1 - T0) * (X1 - X0)


def year_label(y: int) -> str:
    if y < 0:
        return f"{-y} TCN"
    if y == 0:
        return "0"
    return str(y)


def render_svg(data: list) -> str:
    ps = sorted(data, key=lambda p: (p["start"], SCHOOL_ORDER.index(p["school"]), p["name"]))
    n = len(ps)
    h = TOP_PAD + n * ROW_H + AXIS_H
    out = []
    a = out.append
    # data-search-exclude: chữ trong SVG bị nối liền trong chỉ mục tìm kiếm ("Tiền SocratesHy Lạp cổ đại…"), mà
    # mọi dữ kiện đã có ở trang từng triết gia (đợt 4.5).
    # role="group" chứ không phải "img": SVG chứa link tới trang triết gia, mà con của role="img"
    # bị coi là trang trí nên trình đọc màn hình không với tới link (axe: nested-interactive).
    a(f'<svg viewBox="0 0 {W} {h}" role="group" '
      f'aria-label="Dòng thời gian {n} triết gia từ năm 600 TCN đến nay" '
      f'xmlns="http://www.w3.org/2000/svg" class="oz-timeline" data-search-exclude>')
    a("<style>")
    a(":root{--tl-text:#333;--tl-grid:#d8d8d8;--tl-axis:#888;}")
    a("@media (prefers-color-scheme: dark){:root{--tl-text:#ddd;--tl-grid:#3a3a3a;--tl-axis:#999;}}")
    a(".tl-name{fill:var(--tl-text);font-size:13px}")
    a(".oz-timeline a{text-decoration:none}")
    a(".tl-axis{fill:var(--tl-axis);font-size:11px}")
    a(".tl-grid{stroke:var(--tl-grid);stroke-width:1}")
    a(".tl-legend{fill:var(--tl-text);font-size:12px}")
    a("</style>")

    # Chú thích màu theo trường phái.
    lx = 12
    for school in SCHOOL_ORDER:
        if not any(p["school"] == school for p in ps):
            continue
        c = SCHOOL_COLORS[school]
        a(f'<rect x="{lx}" y="14" width="14" height="14" rx="3" fill="{c}"/>')
        a(f'<text x="{lx + 19}" y="26" class="tl-legend">{html.escape(school)}</text>')
        lx += 19 + len(school) * 8 + 26

    # Lưới + trục năm.
    for y in range(-600, 2001, 200):
        xx = x(y)
        a(f'<line x1="{xx:.1f}" y1="{TOP_PAD - 8}" x2="{xx:.1f}" y2="{h - AXIS_H + 6}" class="tl-grid"/>')
        a(f'<text x="{xx:.1f}" y="{h - AXIS_H + 24}" text-anchor="middle" class="tl-axis">'
          f'{year_label(y)}</text>')

    # Mỗi triết gia một hàng: tên + thanh thời gian sống.
    for i, p in enumerate(ps):
        cy = TOP_PAD + i * ROW_H + ROW_H / 2
        x1, x2 = x(p["start"]), x(p["end"])
        if x2 - x1 < 3:
            x2 = x1 + 3
        c = SCHOOL_COLORS[p["school"]]
        tip = f'{p["name"]} ({p["name_en"]}), {p["years"]}: {p["summary"]}'
        a("<g>")
        a(f"<title>{html.escape(tip)}</title>")
        a(f'<a href="../../triet-gia/{p["id"]}/">'
          f'<text x="200" y="{cy + 4.5:.1f}" text-anchor="end" class="tl-name">'
          f'{html.escape(p["name"])}</text></a>')
        a(f'<rect x="{x1:.1f}" y="{cy - 5:.1f}" width="{x2 - x1:.1f}" height="10" rx="5" fill="{c}"/>')
        a("</g>")
    a("</svg>")
    # Một dòng duy nhất: Markdown bọc <svg> nhiều dòng chứa <style> vào <p>,
    # khiến trình duyệt đóng svg rỗng (bug live 14/10/2026). figures.py cũng một dòng.
    return "".join(out)


def render_fallback(data: list) -> str:
    """Danh sách text dự phòng khi SVG không hiện (và cho máy tìm kiếm)."""
    lines = ["<details markdown=\"1\">", "<summary>Danh sách triết gia theo thời gian (bản text)</summary>", ""]
    for school in SCHOOL_ORDER:
        group = sorted([p for p in data if p["school"] == school], key=lambda p: p["start"])
        if not group:
            continue
        lines.append(f"**{school}**")
        lines.append("")
        for p in group:
            lines.append(f"- **{p['name']}** ({p['name_en']}, {p['years']}): {p['summary']}")
        lines.append("")
    lines.append("</details>")
    return "\n".join(lines)


def render(data: list) -> str:
    return render_svg(data) + "\n\n" + render_fallback(data) + "\n"


def build_page(current: str, data: list) -> str:
    body = f"{START}\n\n{render(data)}\n{END}"
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(current):
        raise SystemExit(f"Không thấy dấu {START} trong {PAGE}")
    return pattern.sub(lambda m: body, current)


def main(argv: list[str]) -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    current = PAGE.read_text(encoding="utf-8")
    new = build_page(current, data)
    if "--check" in argv:
        if new != current:
            print("dong-thoi-gian.md lệch so với philosophers.json — chạy: python tools/timeline.py",
                  file=sys.stderr)
            return 1
        print(f"Dòng thời gian khớp dữ liệu ({len(data)} triết gia).")
        return 0
    PAGE.write_text(new, encoding="utf-8")
    print(f"Đã ghi {PAGE.relative_to(ROOT)} ({len(data)} triết gia).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
