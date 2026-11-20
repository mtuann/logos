"""Sinh trang chỉ mục tác phẩm docs/tac-pham/index.md từ data/kb/works.yml (đợt 4.8, quyết định 23).

    python tools/works_page.py          # ghi lại trang
    python tools/works_page.py --check  # mã thoát 1 khi trang lệch dữ liệu (CI)

Tác phẩm có `author` trỏ tới data/kb/people.yml xếp dưới triết gia đó; tác phẩm `chua-ro.*` có `attribution` trùng tên
(hoặc tên tiếng Anh) một triết gia có hồ sơ cũng xếp dưới triết gia đó; bản ghi `same_as` gộp vào tác phẩm nó trỏ tới
(tên khác vào "còn ghi", trang nhắc tới gộp chung); `attribution` còn lại vào mục cuối "Tác giả chưa có trang triết gia"
(đợt 5.9). Xếp tác giả theo năm sinh, tác phẩm theo năm rồi theo tên. Năm: `year` khi các trang thống nhất, không thì mọi năm
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
updated: 2026-11-20
---

# Tác phẩm

!!! info "Danh sách rút tự động"
    Danh sách này được rút tự động từ các bài viết và hồ sơ triết gia. Tên, năm và tác giả của từng tác phẩm đã được kiểm chứng ở đợt 5 (xem [Kiểm chứng](../them/kiem-chung.md)); khi một tác phẩm ghi nhiều năm, đó là các năm khác nhau mà các bài đang dùng (năm bản gốc, năm bản dịch hoặc bản sửa). Thấy chỗ sai, hãy dùng link "Báo lỗi trang này" ở cuối trang.

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


def _years(w: dict) -> list[int]:
    return [w["year"]] if w.get("year") is not None else sorted(int(y) for y in w.get("years_seen", {}))


def _sort_key(w: dict):
    ys = _years(w)
    return (ys[0] if ys else 99999, w["titles"][0])


def _links(w: dict, people: dict, titles: dict) -> list[str]:
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
    return links


def _line(w: dict, people: dict, titles: dict, who: str = "") -> str:
    years = _years(w)
    year = f" ({'; '.join(year_text(y) for y in years)})" if years else ""
    other = w["titles"][1:]
    alt = f" (còn ghi: {', '.join('*' + t + '*' for t in other)})" if other else ""
    links = _links(w, people, titles)
    return f"- *{w['titles'][0]}*{year}{alt}{who}" + (f" — nhắc tới trong: {', '.join(links)}" if links else "")


def _merged(works: dict) -> dict:
    """Gộp bản ghi same_as vào bản ghi đích: thêm tên khác, trang nhắc tới, năm gặp."""
    out = {k: {**w, "titles": list(w["titles"]), "used_in": list(w.get("used_in", [])),
               "years_seen": dict(w.get("years_seen", {}))} for k, w in works.items()}
    for k, w in works.items():
        t = w.get("same_as")
        if w.get("author") or not t or t not in out:
            continue
        d = out[t]
        d["titles"] += [x for x in w["titles"] if x not in d["titles"]]
        d["used_in"] += [u for u in w.get("used_in", []) if u not in d["used_in"]]
        for y, us in w.get("years_seen", {}).items():
            d["years_seen"].setdefault(y, [])
        out.pop(k)
    return out


def render(works: dict, people: dict) -> str:
    works = _merged(works)
    by_name = {}
    for pid, p in people.items():
        for n in (p.get("name"), p.get("name_en")):
            if n:
                by_name[n] = pid
    by_author: dict[str, list] = {}
    others: list = []
    for key, w in works.items():
        pid = w.get("author") if w.get("author") in people else by_name.get(w.get("attribution"))
        if pid:
            by_author.setdefault(pid, []).append((key, w))
        elif w.get("attribution"):
            others.append((key, w))
    titles: dict[str, str] = {}
    out = [START, ""]
    n = 0
    for pid in sorted(by_author, key=lambda p: (born(people[p]), people[p]["name"])):
        p = people[pid]
        out += [f"## {p['name']} {{#{pid}}}", "", f"{p.get('years_label', '')} · [Trang triết gia](../triet-gia/{pid}.md)", ""]
        for key, w in sorted(by_author[pid], key=lambda kw: _sort_key(kw[1])):
            n += 1
            out.append(_line(w, people, titles))
        out.append("")
    if others:
        out += ["## Tác giả chưa có trang triết gia {#tac-gia-khac}", "",
                "Tác phẩm của các tác giả, nhà biên soạn chưa có trang triết gia trên site, xếp theo tên tác giả.", ""]
        for key, w in sorted(others, key=lambda kw: (kw[1]["attribution"].casefold(), _sort_key(kw[1]))):
            n += 1
            out.append(_line(w, people, titles, f" — {w['attribution']}"))
        out.append("")
    out += [f"*{n} tác phẩm của {len(by_author)} triết gia có trang riêng và {len({w['attribution'] for _, w in others})} tác giả khác.*", "", END]
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
