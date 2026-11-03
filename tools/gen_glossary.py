"""Sinh trang Từ điển (docs/them/tu-dien.md) từ docs/assets/data/terms.json.

Nội dung sinh ra nằm giữa hai dấu <!-- gen:glossary --> và <!-- /gen:glossary -->.
    python tools/gen_glossary.py          # ghi lại trang
    python tools/gen_glossary.py --check  # báo lỗi (mã thoát 1) nếu trang lệch dữ liệu
"""

from __future__ import annotations

import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "assets" / "data" / "terms.json"
PAGE = ROOT / "docs" / "them" / "tu-dien.md"
START, END = "<!-- gen:glossary -->", "<!-- /gen:glossary -->"

# Thứ tự chữ cái tiếng Việt cho chữ đầu.
ALPHABET = "a ă â b c d đ e ê g h i k l m n o ô ơ p q r s t u ư v x y".split()


def base_letter(word: str) -> str:
    ch = word[:1].lower()
    if ch == "đ":
        return "đ"
    decomposed = unicodedata.normalize("NFD", ch)
    # Giữ dấu mũ/trăng/móc (ă â ê ô ơ ư), bỏ dấu thanh.
    keep = {"̆", "̂", "̛"}
    letter = decomposed[0] + "".join(c for c in decomposed[1:] if c in keep)
    return unicodedata.normalize("NFC", letter)


def sort_key(term: dict):
    word = term["vi"].lower()
    letter = base_letter(word)
    idx = ALPHABET.index(letter) if letter in ALPHABET else len(ALPHABET)
    plain = unicodedata.normalize("NFD", word.replace("đ", "dz"))
    plain = "".join(c for c in plain if not unicodedata.combining(c))
    return (idx, plain, word)


def render(terms: list[dict]) -> str:
    out = []
    current = None
    for t in sorted(terms, key=sort_key):
        letter = base_letter(t["vi"]).upper()
        if letter != current:
            if current is not None:
                out.append("</dl>\n")
            out.append(f"## {letter}\n")
            out.append('<dl class="oz-glossary">')
            current = letter
        en = f' <span class="oz-en">({html.escape(t["en"])})</span>' if t.get("en") else ""
        han = f' <span class="oz-en">{html.escape(t["han"])}</span>' if t.get("han") else ""
        out.append(f'<dt id="{t["id"]}">{html.escape(t["vi"])}{en}{han}</dt>')
        parts = [html.escape(t["def"])]
        if t.get("example"):
            parts.append(f"<br><em>Ví dụ:</em> {html.escape(t['example'])}")
        if t.get("alt"):
            parts.append(f"<br><em>Cách dịch khác:</em> {html.escape(', '.join(t['alt']))}")
        if t.get("see"):
            href = "../../" + re.sub(r"(index)?\.md$", "", t["see"])
            parts.append(f' <a href="{href}">Đọc thêm →</a>')
        out.append(f"<dd>{''.join(parts)}</dd>")
    if current is not None:
        out.append("</dl>\n")
    return "\n".join(out)


def validate(data: dict) -> list[str]:
    errors = []
    seen = set()
    for t in data.get("terms", []):
        for k in ("id", "vi", "def"):
            if not t.get(k):
                errors.append(f"{t.get('id', '?')}: thiếu {k}")
        if t.get("id") in seen:
            errors.append(f"{t['id']}: id trùng")
        seen.add(t.get("id"))
        if t.get("id") and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", t["id"]):
            errors.append(f"{t['id']}: id phải là chữ thường không dấu, gạch nối")
        if t.get("see") and not (ROOT / "docs" / t["see"]).exists():
            errors.append(f"{t['id']}: trang liên quan không tồn tại: {t['see']}")
    return errors


def build_page(current: str, data: dict) -> str:
    body = f"{START}\n\n{render(data['terms'])}\n{END}"
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
            print("tu-dien.md lệch so với terms.json — chạy: python tools/gen_glossary.py", file=sys.stderr)
            return 1
        print(f"Từ điển khớp dữ liệu ({len(data['terms'])} thuật ngữ).")
        return 0
    PAGE.write_text(new, encoding="utf-8")
    print(f"Đã ghi {PAGE.relative_to(ROOT)} ({len(data['terms'])} thuật ngữ).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
