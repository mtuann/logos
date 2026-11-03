"""Sinh trang Sơ đồ ảnh hưởng (docs/lich-su/so-do-anh-huong.md) từ
trường "influence" trong docs/assets/data/philosophers.json.

Nội dung sinh ra nằm giữa hai dấu <!-- gen:influence --> và <!-- /gen:influence -->.
    python tools/influence.py          # ghi lại trang
    python tools/influence.py --check  # báo lỗi (mã thoát 1) nếu trang lệch dữ liệu
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "assets" / "data" / "philosophers.json"
PAGE = ROOT / "docs" / "lich-su" / "so-do-anh-huong.md"
START, END = "<!-- gen:influence -->", "<!-- /gen:influence -->"

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

# Hai đồ thị rời nhau: phương Tây và phương Đông. Cạnh nối giữa hai đồ thị
# (ví dụ Husserl → Trần Đức Thảo) không vẽ, nhưng có trong danh sách bản text.
WEST_COLS = ["Tiền Socrates", "Hy Lạp cổ đại", "La Mã", "Trung cổ", "Cận đại", "Thế kỷ 19", "Thế kỷ 20"]
# Trung Hoa đứng trước Ấn Độ: cột Ấn Độ chỉ có hai người ở trên cùng, nên cạnh Trung Hoa → Việt Nam
# đi qua vùng trống, còn cạnh Ấn Độ → Việt Nam không phải cắt ngang cột Trung Hoa.
EAST_COLS = ["Trung Hoa", "Ấn Độ", "Việt Nam"]

NODE_W, NODE_H = 140, 30
COL_GAP = 48
ROW_GAP = 14
PAD_X, PAD_TOP = 16, 14
ARC_PAD = 46  # chỗ cho cung nối hai người cùng cột, hai bên mép sơ đồ


def validate(data: list) -> list[str]:
    errors = []
    ids = {p.get("id") for p in data}
    for p in data:
        for inf in p.get("influence", []):
            if inf not in ids:
                errors.append(f"{p.get('id')}: influence lạ: {inf}")
    return errors


def layout(data: list, cols: list[str]) -> tuple[dict, int, int]:
    """Xếp node theo cột trường phái, trong cột xếp theo năm sinh.

    Trả về (pos, width, height), pos[id] = (cx, cy) là tâm node.
    """
    pos: dict[str, tuple[float, float]] = {}
    max_rows = 0
    col_nodes: dict[str, list] = {}
    for c in cols:
        group = sorted([p for p in data if p["school"] == c], key=lambda p: (p["start"], p["name"]))
        col_nodes[c] = group
        max_rows = max(max_rows, len(group))
    width = PAD_X * 2 + len(cols) * NODE_W + (len(cols) - 1) * COL_GAP
    height = PAD_TOP * 2 + max_rows * (NODE_H + ROW_GAP) - ROW_GAP
    for ci, c in enumerate(cols):
        x = PAD_X + ci * (NODE_W + COL_GAP)
        for ri, p in enumerate(col_nodes[c]):
            y = PAD_TOP + ri * (NODE_H + ROW_GAP)
            pos[p["id"]] = (x + NODE_W / 2, y + NODE_H / 2)
    return pos, width, height, col_nodes


def render_graph(data: list, cols: list[str], label: str, uid: str) -> str:
    # Bỏ cột chưa có triết gia nào (tránh cột trống trong sơ đồ).
    cols = [c for c in cols if any(p["school"] == c for p in data)]
    by_id = {p["id"]: p for p in data}
    pos, w, h, col_nodes = layout(data, cols)
    out = []
    a = out.append
    # role="group" chứ không phải "img": các node là link (axe: nested-interactive).
    a(f'<svg viewBox="{-ARC_PAD} 0 {w + 2 * ARC_PAD} {h}" role="group" '
      f'aria-label="Sơ đồ ảnh hưởng: {html.escape(label)}" '
      f'xmlns="http://www.w3.org/2000/svg" class="oz-influence">')
    a("<style>")
    a(":root{--inf-text:#333;--inf-edge:#8a8a8a;}")
    a("@media (prefers-color-scheme: dark){:root{--inf-text:#ddd;--inf-edge:#777;}}")
    a(".inf-name{fill:var(--inf-text);font-size:12px}")
    a(".oz-influence a{text-decoration:none}")
    a(".inf-col{fill:var(--inf-text);font-size:12px;font-weight:bold}")
    a(".inf-edge{stroke:var(--inf-edge);stroke-width:1.4;fill:none;opacity:.75}")
    a("</style>")
    a("<defs>")
    a(f'<marker id="inf-arrow-{uid}" viewBox="0 0 10 10" refX="8" refY="5" '
      'markerWidth="7" markerHeight="7" orient="auto-start-reverse">')
    a('<path d="M 0 1 L 9 5 L 0 9 z" fill="var(--inf-edge)"/></marker>')
    a("</defs>")

    # Tên cột.
    for ci, c in enumerate(cols):
        x = PAD_X + ci * (NODE_W + COL_GAP) + NODE_W / 2
        a(f'<text x="{x:.1f}" y="{PAD_TOP - 4}" text-anchor="middle" class="inf-col">'
          f'{html.escape(c)}</text>')

    # Cạnh vẽ trước, node vẽ sau (node đè lên đầu/cuối cạnh).
    edges = []
    for p in data:
        if p["school"] not in cols:
            continue
        for t in p.get("influence", []):
            if t in pos and p["id"] in pos:
                edges.append((p["id"], t))
    rank = {p["id"]: i for c in cols for i, p in enumerate(col_nodes[c])}
    for s, t in edges:
        x1, y1 = pos[s]
        x2, y2 = pos[t]
        if abs(x1 - x2) < 1:
            # Cùng cột: cung lượn ra bên cạnh, càng xa càng cong, để các cạnh không chồng
            # lên nhau và không cắt qua node ở giữa. Cạnh đi xuống lượn bên phải, cạnh
            # đi ngược lên (người sinh sau ảnh hưởng người sinh trước) lượn bên trái.
            span = rank[t] - rank[s]
            bulge = min(10 + 6 * abs(span), ARC_PAD - 4)
            side = 1 if span > 0 else -1
            ex = x1 + side * (NODE_W / 2 - 2)
            cx = ex + side * bulge
            a(f'<path d="M {ex:.1f} {y1 + 7:.1f} C {cx:.1f} {y1 + 7:.1f}, {cx:.1f} {y2 - 7:.1f}, '
              f'{ex:.1f} {y2 - 7:.1f}" class="inf-edge" marker-end="url(#inf-arrow-{uid})"/>')
            continue
        sx = x1 + NODE_W / 2 - 2  # mép phải node nguồn
        tx = x2 - NODE_W / 2 + 2  # mép trái node đích
        mx = (sx + tx) / 2
        a(f'<path d="M {sx:.1f} {y1:.1f} C {mx:.1f} {y1:.1f}, {mx:.1f} {y2:.1f}, '
          f'{tx:.1f} {y2:.1f}" class="inf-edge" marker-end="url(#inf-arrow-{uid})"/>')

    for c in cols:
        for p in col_nodes[c]:
            cx, cy = pos[p["id"]]
            x, y = cx - NODE_W / 2, cy - NODE_H / 2
            color = SCHOOL_COLORS[p["school"]]
            tip = f'{p["name"]} ({p["name_en"]}), {p["years"]}: {p["summary"]}'
            a("<g>")
            a(f"<title>{html.escape(tip)}</title>")
            a(f'<rect x="{x:.1f}" y="{y:.1f}" width="{NODE_W}" height="{NODE_H}" rx="8" '
              f'fill="{color}" fill-opacity="0.22" stroke="{color}" stroke-width="1.6"/>')
            a(f'<a href="../../triet-gia/{p["id"]}/">'
              f'<text x="{cx:.1f}" y="{cy + 4:.1f}" text-anchor="middle" class="inf-name">'
              f'{html.escape(p["name"])}</text></a>')
            a("</g>")
    a("</svg>")
    # Một dòng duy nhất: Markdown bọc <svg> nhiều dòng chứa <style> vào <p>,
    # khiến trình duyệt đóng svg rỗng (bug live 14/10/2026). figures.py cũng một dòng.
    return "".join(out)


def render_fallback(data: list) -> str:
    by_id = {p["id"]: p for p in data}
    lines = ["<details markdown=\"1\">", "<summary>Danh sách ảnh hưởng (bản text)</summary>", ""]
    for p in data:
        if not p.get("influence"):
            continue
        targets = ", ".join(by_id[t]["name"] for t in p["influence"] if t in by_id)
        lines.append(f"- **{p['name']}** ảnh hưởng tới: {targets}")
    lines.append("")
    lines.append("</details>")
    return "\n".join(lines)


def render(data: list) -> str:
    west = render_graph(data, WEST_COLS, "triết học phương Tây", "west")
    east = render_graph(data, EAST_COLS, "triết học Ấn Độ, Trung Hoa và Việt Nam", "east")
    return (
        "### Phương Tây: từ tiền Socrates tới thế kỷ 20\n\n" + west +
        "\n\n### Phương Đông: Ấn Độ, Trung Hoa, Việt Nam\n\n" + east +
        "\n\n" + render_fallback(data) + "\n"
    )


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
            print("so-do-anh-huong.md lệch so với philosophers.json — chạy: python tools/influence.py",
                  file=sys.stderr)
            return 1
        print(f"Sơ đồ ảnh hưởng khớp dữ liệu ({len(data)} triết gia).")
        return 0
    PAGE.write_text(new, encoding="utf-8")
    print(f"Đã ghi {PAGE.relative_to(ROOT)} ({len(data)} triết gia).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
