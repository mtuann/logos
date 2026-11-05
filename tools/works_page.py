"""Sinh trang chỉ mục tác phẩm docs/tac-pham/index.md từ data/kb/works.yml (đợt 4.8, quyết định 23).

    python tools/works_page.py          # ghi lại trang
    python tools/works_page.py --check  # mã thoát 1 khi trang lệch dữ liệu (CI)

Chỉ tác phẩm đã biết tác giả (`author` trỏ tới data/kb/people.yml); tác phẩm `chua-ro.*` chờ đợt 5 gán tác giả.
Xếp tác giả theo năm sinh, tác phẩm theo năm rồi theo tên. Năm: `year` khi các trang thống nhất, không thì mọi năm
gặp được (`years_seen`). "Nhắc tới trong": mỗi trang một link (tới mục đầu tiên nhắc tác phẩm), hồ sơ triết gia
dẫn tới trang triết gia. Dữ liệu chưa kiểm chứng: trang ghi rõ. Chưa có URL riêng cho từng tác phẩm (quyết định 23).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PAGE = DOCS / "tac-pham" / "index.md"
WORKS = ROOT / "data" / "kb" / "works.yml"
PEOPLE = ROOT / "data" / "kb" / "people.yml"
TITLE = re.compile(r'^title:\s*"?(.*?)"?\s*$', re.M)

HEAD = """---
title: Tác phẩm
description: Các tác phẩm triết học được nhắc tới trên site, xếp theo tác giả, kèm những bài nhắc tới chúng.
updated: 2026-11-05
---

# Tác phẩm

!!! warning "Danh sách chưa kiểm chứng"
    Danh sách này được rút tự động từ các bài viết và hồ sơ triết gia. Tên, năm và tác giả chưa được kiểm chứng: khi một tác phẩm ghi nhiều năm, đó là các năm khác nhau mà các bài đang dùng. Thấy chỗ sai, hãy dùng link "Báo lỗi trang này" ở cuối trang.

"""
START, END = "<!-- gen:tac-pham: không sửa tay; sinh bằng tools/works_page.py -->", "<!-- /gen:tac-pham -->"


def year_text(y: int) -> str:
    return f"{-y} TCN" if y < 0 else str(y)


def born(p: dict) -> int:
    b = p.get("born")
    return (b.get("year") if isinstance(b, dict) else b) or 0


def page_title(path: str, cache: dict) -> str:
    if path not in cache:
        m = TITLE.search((DOCS / path).read_text(encoding="utf-8").split("\n---", 1)[0])
        cache[path] = m.group(1) if m else path
    return cache[path]


def render(works: dict, people: dict) -> str:
    by_author: dict[str, list] = {}
    for key, w in works.items():
        if w.get("author") in people:
            by_author.setdefault(w["author"], []).append((key, w))
    titles: dict[str, str] = {}
    out = [START, ""]
    n = 0
    for pid in sorted(by_author, key=lambda p: (born(people[p]), people[p]["name"])):
        p = people[pid]
        out += [f"## {p['name']} {{#{pid}}}", "", f"{p.get('years_label', '')} · [Trang triết gia](../triet-gia/{pid}.md)", ""]
        items = sorted(by_author[pid], key=lambda kw: (kw[1].get("year") if kw[1].get("year") is not None
                                                     else min((int(y) for y in kw[1]["years_seen"]), default=99999),
                                                     kw[1]["titles"][0]))
        for key, w in items:
            n += 1
            years = [w["year"]] if w.get("year") is not None else sorted(int(y) for y in w.get("years_seen", {}))
            year = f" ({'; '.join(year_text(y) for y in years)})" if years else ""
            links, seen = [], set()
            for u in w.get("used_in", []):
                if u.startswith("people/"):
                    target, text = f"../triet-gia/{u.split('/', 1)[1]}.md", "hồ sơ " + people.get(u.split("/", 1)[1], {}).get("name", u)
                    page = target
                else:
                    page, _, anchor = u.partition("#")
                    target = f"../{page}" + (f"#{anchor}" if anchor and anchor != "_dau" else "")
                    text = page_title(page, titles)
                if page in seen:
                    continue
                seen.add(page)
                links.append(f"[{text}]({target})")
            other = [t for t in w["titles"][1:]]
            alt = f" (còn ghi: {', '.join('*' + t + '*' for t in other)})" if other else ""
            out.append(f"- *{w['titles'][0]}*{year}{alt}" + (f" — nhắc tới trong: {', '.join(links)}" if links else ""))
        out.append("")
    out += [f"*{n} tác phẩm của {len(by_author)} tác giả.*", "", END]
    return HEAD + "\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    text = render(yaml.safe_load(WORKS.read_text(encoding="utf-8")), yaml.safe_load(PEOPLE.read_text(encoding="utf-8")))
    if args.check:
        if not PAGE.exists() or PAGE.read_text(encoding="utf-8") != text:
            print("docs/tac-pham/index.md lệch data/kb/works.yml — chạy: python tools/works_page.py", file=sys.stderr)
            return 1
        print("Trang tác phẩm khớp kho tác phẩm.")
        return 0
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(text, encoding="utf-8")
    print(f"Đã ghi {PAGE.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
