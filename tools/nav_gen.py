"""Sinh phần `nav:` của mkdocs.yml từ mục `nav` trong content.yml (đợt 4.9).

    python tools/nav_gen.py          # chép nav vào mkdocs.yml (giữa `# gen:nav` và `# /gen:nav`)
    python tools/nav_gen.py --check  # mã thoát 1 khi mkdocs.yml lệch content.yml (CI)

content.yml là nguồn chính của nav. Khối `nav:` được chép nguyên văn (cùng cú pháp nav của MkDocs), nên thứ tự,
tiêu đề nav và cấu trúc nhóm giữ đúng như viết. Kiểm "mọi trang trong `pages` có trong nav và ngược lại" nằm ở
tools/content_registry.py --check.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content.yml"
MKDOCS = ROOT / "mkdocs.yml"
START = "# gen:nav — không sửa tay: sửa mục `nav` trong content.yml rồi chạy python tools/nav_gen.py\n"
END = "# /gen:nav\n"
TOP = re.compile(r"^[A-Za-z_][\w-]*:", re.M)


def nav_block(text: str) -> str:
    """Khối `nav:` (dòng `nav:` và mọi dòng thụt lề hoặc chú thích sau nó) của một file YAML."""
    m = re.search(r"^nav:\s*$", text, re.M)
    if not m:
        raise SystemExit("content.yml: không có mục nav")
    rest = text[m.end():]
    nxt = TOP.search(rest)
    block = text[m.start():m.end() + (nxt.start() if nxt else len(rest))]
    lines = block.rstrip("\n").split("\n")
    while lines and lines[-1].lstrip().startswith("#"):   # chú thích của mục sau không thuộc nav
        lines.pop()
    return "\n".join(lines) + "\n"


def render(mkdocs: str, nav: str) -> str:
    i, j = mkdocs.find(START), mkdocs.find(END)
    if i < 0 or j < i:
        raise SystemExit("mkdocs.yml: thiếu dấu `# gen:nav` / `# /gen:nav`")
    return mkdocs[:i + len(START)] + nav + mkdocs[j:]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    old = MKDOCS.read_text(encoding="utf-8")
    new = render(old, nav_block(CONTENT.read_text(encoding="utf-8")))
    if args.check:
        if new != old:
            print("mkdocs.yml: nav lệch content.yml — chạy: python tools/nav_gen.py", file=sys.stderr)
            return 1
        print("Nav của mkdocs.yml khớp content.yml.")
        return 0
    MKDOCS.write_text(new, encoding="utf-8")
    print("Đã chép nav từ content.yml vào mkdocs.yml.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
