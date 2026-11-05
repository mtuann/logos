"""Thay chữ gõ tay bằng shortcode, có kiểm (đợt 3, việc 3.4–3.5). Dùng chung cho dot3_so_dem.py, dot3_philpapers.py.

Mỗi phép thay: (trang trong docs/, số dòng đếm từ 1, chữ cũ, chữ mới chứa shortcode). Chữ cũ phải xuất hiện đúng
một lần trong dòng; mở shortcode của dòng mới (hooks/kb.py, cùng dữ liệu khi build) phải ra đúng dòng cũ.
Sai một phép là dừng, không ghi gì. Phép thay đã làm (dòng đã chứa chữ mới, không còn chữ cũ) thì bỏ qua.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "hooks"), str(ROOT / "tools")]
import kb  # noqa: E402

DOCS = ROOT / "docs"


def apply(subs: list[tuple[str, int, str, str]], dry_run: bool = False) -> tuple[int, int]:
    """(số phép thay đã áp, số trang đổi)."""
    ctx = kb.load_context(ROOT)
    pages: dict[str, list[str]] = {}
    done = 0
    for page, lineno, old, new in subs:
        lines = pages.setdefault(page, (DOCS / page).read_text(encoding="utf-8").split("\n"))
        line = lines[lineno - 1]
        if line.count(old) == 0 and new in line:
            continue
        if line.count(old) != 1:
            raise SystemExit(f"{page}:{lineno}: {old!r} gặp {line.count(old)} lần trong dòng, phải đúng 1")
        new_line = line.replace(old, new, 1)
        back = kb.expand(new_line, ctx, page)
        if back != kb.expand(line, ctx, page):
            raise SystemExit(f"{page}:{lineno}: mở shortcode không ra chữ cũ:\n  cũ: {line}\n  mới: {back}")
        lines[lineno - 1] = new_line
        done += 1
    changed = 0
    for page, lines in pages.items():
        text = "\n".join(lines)
        if text != (DOCS / page).read_text(encoding="utf-8"):
            changed += 1
            if not dry_run:
                (DOCS / page).write_text(text, encoding="utf-8")
    return done, changed
