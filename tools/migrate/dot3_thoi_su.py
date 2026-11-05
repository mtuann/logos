"""Đợt 3, việc 3.3: dời đoạn có hạn dùng ra khối thời sự data/thoi-su/<id>.md (quyết định 20).

    python tools/migrate/dot3_thoi_su.py           # dời (chạy lại không đổi gì: đoạn đã dời thì bỏ qua)
    python tools/migrate/dot3_thoi_su.py --dry-run # chỉ in việc sẽ làm

Mỗi mục của MOVES: trang, tên ngắn, dòng (đếm từ 1, chỉ để chắc chắn đúng chỗ), mốc đầu và mốc cuối của đoạn
trong dòng (None, None = cả dòng, bỏ thụt lề), nguồn thêm (khóa trong data/kb/sources.yml, lấy từ mục Nguồn của trang).
Đoạn được cắt nguyên văn, thay bằng `[[thoi-su:<id>]]` tại chỗ. Front matter: `updated_to` = `updated` của trang,
`review_by` = updated_to + 1 năm, `sources` = link trong đoạn + nguồn thêm. Script tự kiểm: mở lại shortcode
(hooks/kb.py) thì được đúng từng byte trang cũ; không thì không ghi gì.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "hooks"), str(ROOT / "tools")]
import kb  # noqa: E402

DOCS = ROOT / "docs"
OUT = ROOT / "data" / "thoi-su"
LINK = re.compile(r"\]\((https?://[^)\s]+)\)|<(https?://[^>\s]+)>")

MOVES = [
    ("cau-hoi/an-tu-hinh.md", "dpic-minh-oan", 64, "Theo Death Penalty Information Center", "mình vô tội.",
     ["web.deathpenaltyinfo-org.policy-issues-innocence"]),
    ("cau-hoi/chan-ly.md", "chatbot-ao-giac", 126, None, None, []),
    ("cau-hoi/chan-ly.md", "bo-luat-to-tung-hinh-su", 128, None, None, []),
    ("cau-hoi/hien-tang.md", "nguon-tang-viet-nam", 93, "**Ở Việt Nam: nguồn tạng", "còn rất hạn chế.", []),
    ("cau-hoi/nho-giao-viet.md", "du-hoc", 126, "Mỗi năm hàng chục nghìn", "các năm gần đây).", []),
    ("cau-hoi/quyen-rieng-tu-so.md", "luat-du-lieu-ca-nhan", 94, None, None,
     ["web.thuvienphapluat-vn.van-ban-quyen-dan-su-nghi-dinh-356-2025-nd-cp-huon"]),
    ("cau-hoi/tu-do-y-chi.md", "bo-luat-hinh-su", 171, None, None,
     ["sach.bo-luat-hinh-su-so-100-2015-qh13-sua-doi-bo-sung-nam-2017-di"]),
]


def block_id(page: str, name: str) -> str:
    return page[:-3].replace("/", ".") + "." + name


def front(page: str, updated: datetime.date, sources: list[str]) -> str:
    due = updated.replace(year=updated.year + 1)
    src = "".join(f"\n  - {s}" for s in sources) if sources else " []"
    return f"---\npage: {page}\nupdated_to: {updated.isoformat()}\nreview_by: {due.isoformat()}\nsources:{src}\n---\n"


def cut(text: str, page: str, name: str, lineno: int, start, end, extra) -> tuple[str, str] | None:
    """(trang mới, nội dung file khối), hoặc None khi đoạn đã dời."""
    key = block_id(page, name)
    if f"[[thoi-su:{key}]]" in text:
        return None
    lines = text.split("\n")
    line = lines[lineno - 1]
    if start is None:
        a, b = len(line) - len(line.lstrip()), len(line.rstrip())
    else:
        a = line.index(start)
        b = line.index(end, a) + len(end)
    frag = line[a:b]
    if text.count(frag) != 1:
        raise SystemExit(f"{page}:{lineno}: đoạn gặp {text.count(frag)} lần, phải đúng 1")
    lines[lineno - 1] = line[:a] + f"[[thoi-su:{key}]]" + line[b:]
    updated = datetime.date.fromisoformat(re.search(r"^updated: (\d{4}-\d{2}-\d{2})$", text, re.M).group(1))
    urls = [u or v for u, v in LINK.findall(frag)]
    return "\n".join(lines), front(page, updated, urls + extra) + frag + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    orig: dict[str, str] = {}
    pages: dict[str, str] = {}
    files: dict[str, str] = {}
    for page, name, lineno, start, end, extra in MOVES:
        if page not in pages:
            orig[page] = pages[page] = (DOCS / page).read_text(encoding="utf-8")
        r = cut(pages[page], page, name, lineno, start, end, extra)
        if r:
            pages[page], files[block_id(page, name)] = r
    blocks = kb.load_thoi_su(ROOT)
    for key, body in files.items():
        m = kb.FRONT.match(body)
        blocks[key] = {"meta": yaml.safe_load(m.group(1)), "body": body[m.end():-1]}
    for page, new in pages.items():   # trang cũ có thể đã chứa khối dời ở lần chạy trước: so sau khi mở cả hai
        if kb.expand_thoi_su(new, blocks, page) != kb.expand_thoi_su(orig[page], blocks, page):
            raise SystemExit(f"{page}: mở lại shortcode không ra đúng trang cũ; không ghi gì")
    for key in files:
        print(f"{'(thử) ' if args.dry_run else ''}dời → data/thoi-su/{key}.md")
    if args.dry_run or not files:
        print("Không có gì để dời." if not files else "")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for key, body in files.items():
        (OUT / f"{key}.md").write_text(body, encoding="utf-8")
    changed = [p for p in pages if pages[p] != orig[p]]
    for page in changed:
        (DOCS / page).write_text(pages[page], encoding="utf-8")
    print(f"Đã dời {len(files)} đoạn ở {len(changed)} trang.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
