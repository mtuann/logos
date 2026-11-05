"""Gắn ID cố định `{#id}` cho mọi mục H2 của Lõi viết tay (KE-HOACH.md mục 5.5; ban-giao/dot-1.md việc 1.3).

    python tools/add_heading_ids.py            # gắn ID còn thiếu (cần site/ đã build từ đúng nguồn hiện tại)
    python tools/add_heading_ids.py --site DIR # đọc anchor từ bản build ở DIR
    python tools/add_heading_ids.py --check    # mã thoát 1 khi còn H2 của Lõi viết tay chưa có ID

ID lấy đúng anchor đang có trong HTML đã build, theo thứ tự (kể cả hậu tố `_1`, `_2` của tiêu đề trùng), để
link cũ không gãy. Trước khi ghi, tool đối chiếu ba nguồn cho từng trang: số H2 trong nguồn, ID trong HTML,
và ID mà `lz.units` tính theo quy tắc của toc. Lệch ở bất kỳ trang nào thì dừng, không ghi file nào.
Phạm vi: trang `tier: loi`, `generated: false` trong content.yml. Trang sinh tự động lấy ID từ tool sinh ra nó.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lz import ROOT, registry, units

H2_ID = re.compile(r'<h2 id="([^"]+)"')


def html_for(site: Path, page: str) -> Path:
    rel = page[: -len("index.md")] if page.endswith("index.md") else page[:-3] + "/"
    return site / rel / "index.html"


def plan(site: Path, root: Path = ROOT) -> tuple[dict[str, list[tuple[int, str]]], list[str]]:
    """(trang → [(số dòng của H2, id cần gắn)], danh sách lỗi đối chiếu)."""
    todo: dict[str, list[tuple[int, str]]] = {}
    errors: list[str] = []
    for p in registry.load(root).select(tier="loi", generated=False):
        us = units.split_file(p.path, root)[1:]
        html = html_for(site, p.path)
        if not html.exists():
            errors.append(f"{p.path}: không thấy {html}")
            continue
        built = H2_ID.findall(html.read_text(encoding="utf-8"))
        mine = [u.id for u in us]
        if built != mine:
            errors.append(f"{p.path}: anchor trong HTML {built} khác ID tính từ nguồn {mine}")
            continue
        missing = [(u.start, u.id) for u in us if not u.explicit_id]
        if missing:
            todo[p.path] = missing
    return todo, errors


def apply(todo: dict[str, list[tuple[int, str]]], root: Path = ROOT) -> int:
    n = 0
    for page, items in todo.items():
        f = root / "docs" / page
        lines = f.read_text(encoding="utf-8").split("\n")
        for lineno, ident in items:
            line = lines[lineno - 1]
            if not line.startswith("## "):
                raise RuntimeError(f"{page}:{lineno}: không phải dòng H2: {line!r}")
            lines[lineno - 1] = f"{line.rstrip()} {{#{ident}}}"
            n += 1
        f.write_text("\n".join(lines), encoding="utf-8")
    return n


def missing_ids(root: Path = ROOT) -> list[str]:
    return [
        f"{u.page}:{u.start}: H2 \"{u.title}\" chưa có ID cố định (gợi ý {{#{u.id}}})"
        for p in registry.load(root).select(tier="loi", generated=False)
        for u in units.split_file(p.path, root)[1:]
        if not u.explicit_id
    ]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="chỉ kiểm: báo H2 của Lõi viết tay chưa có ID")
    ap.add_argument("--site", type=Path, default=ROOT / "site", help="thư mục site đã build (mặc định site/)")
    args = ap.parse_args(argv)

    if args.check:
        miss = missing_ids()
        if miss:
            print(f"ID mục H2: {len(miss)} mục của Lõi viết tay chưa có ID cố định:")
            for m in miss[:50]:
                print("  - " + m)
            print("Chạy: uv run properdocs build -f mkdocs.yml && uv run python tools/add_heading_ids.py")
            return 1
        print("ID mục H2: mọi mục của Lõi viết tay đã có ID cố định.")
        return 0

    todo, errors = plan(args.site)
    if errors:
        print("Không ghi file nào: nguồn và bản build lệch nhau (build lại từ nguồn hiện tại rồi chạy lại).")
        for e in errors:
            print("  - " + e)
        return 1
    n = apply(todo)
    print(f"Đã gắn {n} ID mục H2 ở {len(todo)} trang.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
