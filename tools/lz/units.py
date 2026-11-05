"""Tách một trang Markdown thành đơn vị theo mục H2 (KE-HOACH.md mục 5.5).

- Đơn vị là một mục H2: từ dòng `## …` tới trước dòng `## …` kế tiếp (gồm cả H3, H4 bên trong).
- Phần trước H2 đầu tiên (sau front matter) là đơn vị `#_dau`; nó có mặt kể cả khi rỗng.
- Khóa đơn vị: `<đường dẫn trong docs>#<id>`, ví dụ `cau-hoi/tri-thuc.md#cac-lap-truong-chinh`.
- ID lấy từ thuộc tính viết tay `{#id}` trên dòng H2. Trang chưa gắn ID (trước việc 1.3) thì tính dự phòng
  theo đúng cách build đang làm: `hooks/slugs.py` + quy tắc chống trùng `_1`, `_2` của phần mở rộng toc,
  xét mọi tiêu đề của trang theo thứ tự. `Unit.explicit_id` cho biết ID đến từ đâu.
- Dòng `## ` trong khối code rào (```), trong khối sinh `<!-- gen:… -->`/`<!-- fig:… -->`, hoặc thụt lề
  (nằm trong admonition) không mở đơn vị mới.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from . import ROOT
from .normalize import FENCE, GEN_CLOSE, GEN_OPEN, heading_text

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
HEADING = re.compile(r"^(?P<indent>[ \t]*)(?P<hashes>#{1,6})[ \t]+(?P<body>.*?)[ \t]*#*[ \t]*$")
ATTR_ID = re.compile(r"\s*\{[^}]*?#(?P<id>[\w-]+)[^}]*\}\s*$")
ATTR_ANY = re.compile(r"\s*\{:?[^}]*\}\s*$")
IDCOUNT = re.compile(r"^(.*)_([0-9]+)$")
HEAD_ID = "_dau"


@dataclass(frozen=True)
class Unit:
    page: str            # đường dẫn trong docs/
    id: str              # "_dau" cho phần trước H2 đầu tiên
    title: str | None    # chữ của tiêu đề H2 (nguồn, đã bỏ `{…}`); None cho `_dau`
    explicit_id: bool    # True nếu ID viết tay `{#id}` (hoặc là `_dau`)
    start: int           # số dòng (đếm từ 1, tính cả front matter) của dòng đầu đơn vị
    end: int             # số dòng cuối (bao gồm)
    source: str          # văn bản nguồn của đơn vị

    @property
    def key(self) -> str:
        return f"{self.page}#{self.id}"


def _slugify():
    sys.path.insert(0, str(ROOT / "hooks"))
    try:
        from slugs import slugify
    finally:
        sys.path.pop(0)
    return slugify


def _unique(ident: str, used: set[str]) -> str:
    """Quy tắc chống trùng của markdown.extensions.toc.unique (Markdown 3.11)."""
    while ident in used or not ident:
        m = IDCOUNT.match(ident)
        ident = f"{m.group(1)}_{int(m.group(2)) + 1}" if m else f"{ident}_1"
    used.add(ident)
    return ident


def _scan(lines: list[str]):
    """Trả về (chỉ số dòng, độ thụt, cấp, phần thân) của mọi tiêu đề ATX nằm ngoài code rào và khối sinh."""
    fence = None
    gen = None
    for i, line in enumerate(lines):
        if fence:
            if line.strip().startswith(fence):
                fence = None
            continue
        if gen:
            if GEN_CLOSE.search(line) and gen in line:
                gen = None
            continue
        m = GEN_OPEN.search(line)
        if m:
            gen = f"<!-- /{m.group(1)}:{m.group(2)} -->"
            if gen in line:          # mở và đóng trên cùng một dòng
                gen = None
            continue
        m = FENCE.match(line)
        if m:
            fence = m.group(2)[0] * len(m.group(2))
            continue
        m = HEADING.match(line)
        if m:
            yield i, m.group("indent"), len(m.group("hashes")), m.group("body")


def split(path: str, text: str) -> list[Unit]:
    """Tách văn bản `text` của trang `path` (tính từ docs/) thành danh sách đơn vị theo thứ tự."""
    fm = FRONT_MATTER.match(text)
    offset = fm.group(0).count("\n") if fm else 0
    lines = text[fm.end() if fm else 0:].splitlines(keepends=True)

    heads = list(_scan(lines))
    # ID viết tay của mọi tiêu đề được toc giữ trước, rồi mới cấp ID tự sinh theo thứ tự.
    used: set[str] = set()
    for _, _, _, body in heads:
        m = ATTR_ID.search(body)
        if m:
            used.add(m.group("id"))
    slugify = _slugify()

    h2: list[tuple[int, str, str, bool]] = []      # (chỉ số dòng, id, tiêu đề, explicit)
    for i, indent, level, body in heads:
        m = ATTR_ID.search(body)
        title = ATTR_ANY.sub("", body)
        if m:
            ident, explicit = m.group("id"), True
        else:
            ident, explicit = _unique(slugify(heading_text(title)), used), False
        if level == 2 and not indent:
            h2.append((i, ident, title, explicit))

    units: list[Unit] = []
    bounds = [0] + [i for i, *_ in h2] + [len(lines)]
    meta = [(HEAD_ID, None, True)] + [(ident, title, explicit) for _, ident, title, explicit in h2]
    for (a, b), (ident, title, explicit) in zip(zip(bounds, bounds[1:]), meta):
        units.append(Unit(
            page=path, id=ident, title=title, explicit_id=explicit,
            start=offset + a + 1, end=offset + b, source="".join(lines[a:b]),
        ))
    seen: set[str] = set()
    for u in units:
        if u.id in seen:
            raise ValueError(f"{u.key}: ID mục trùng trong trang")
        seen.add(u.id)
    return units


def split_file(path: str, root: Path = ROOT) -> list[Unit]:
    return split(path, (root / "docs" / path).read_text(encoding="utf-8"))
