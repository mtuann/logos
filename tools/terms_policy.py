"""Sinh data/style/terms-policy.yml từ bảng thuật ngữ bắt buộc ở HUONG-DAN-VIET.md mục 3.

    python tools/terms_policy.py          # sinh lại
    python tools/terms_policy.py --check  # mã thoát 1 khi file lệch HUONG-DAN-VIET.md (CI)

Nguồn sự thật là bảng trong HUONG-DAN-VIET.md (người viết đọc ở đó); file YAML là bản máy đọc cho
tools/lint_terms.py. Mỗi dòng bảng thành một mục `terms`: `en`, `use`, `avoid` (các cách dịch khác bằng tiếng
Việt; bỏ chữ "(sai)"; cụm tiếng Anh như "abduction" không bị cấm vì được viết trong ngoặc sau thuật ngữ Việt),
`note`. Dòng "Tên riêng … Platon (không viết Plato)" thành mục `names`.

Phần viết tay (giữ trong tool này, không sinh từ bảng):
  - AMBIGUOUS: cách dịch khác trùng một từ thường hoặc một thuật ngữ khác (ví dụ "mệnh đề" trong
    "logic mệnh đề"); linter chỉ gợi ý (`thuat-ngu-mo-ho`), không cảnh báo;
  - CONTEXT: cụm đúng có chứa cách dịch bị tránh ("thuyết ý chí tự do", "luận cứ thép");
  - EXCEPTIONS: nơi không kiểm (trích nguyên văn, từ điển, tên riêng và tên tác phẩm in nghiêng…).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "HUONG-DAN-VIET.md"
OUT = ROOT / "data" / "style" / "terms-policy.yml"

AMBIGUOUS = {
    "mệnh đề": "cũng là thuật ngữ đúng cho proposition (logic mệnh đề)",
    "hiểu biết": "cũng là từ thường",
    "tinh thần": "cũng là từ thường (tinh thần, tâm lý; spirit)",
    "diễn dịch": "cũng nghĩa là diễn giải, chuyển ngữ",
    "đúng đắn": "cũng là từ thường",
    "hợp logic": "cũng là từ thường",
    "sự chứng thực": "cũng là từ thường",
    "thuyết định mệnh": "đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism",
}
# Cách dịch bị tránh nhưng nằm trong một cụm đúng: (cụm bị tránh, regex phần đứng trước, regex phần đứng sau).
CONTEXT = {
    "ý chí tự do": {"not_after": ["thuyết "]},
    "luận cứ": {"not_before": [" thép"], "not_after": ["tranh "]},   # "luận cứ thép"; "tranh luận cứ xoay vòng"
}
EXCEPTIONS = {
    "pages": ["them/tu-dien.md"],
    "data": ["docs/assets/data/terms.json"],
    "contexts": [
        "trích nguyên văn: khối !!! quote và dòng > …",
        "chữ trong ngoặc kép (\"…\", “…”): thường là lời người khác hoặc tên gọi",
        "chữ in nghiêng *…*: tên tác phẩm, thuật ngữ gốc",
        "mục ## Nguồn",
        "code, đích link",
    ],
}
NAME_RULE = re.compile(r"(\w[\w ]*?) \(không viết (\w[\w ]*?)\)")


def table_rows(guide: str) -> list[list[str]]:
    sec = guide.split("## 3. Thuật ngữ thống nhất", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in sec.splitlines():
        if not line.startswith("|") or re.match(r"^\|[-\s|]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == "Tiếng Anh":
            continue
        rows.append((cells + ["", "", ""])[:3])
    return rows


def parse_avoid(cell: str) -> tuple[list[str], str | None]:
    note = None
    if "—" in cell:
        cell, note = cell.split("—", 1)
        note = note.strip()
    avoid = []
    for item in (x.strip() for x in cell.split(",")):
        item = re.sub(r"\s*\(sai\)$", "", item).strip()
        if not item or item == "—":
            continue
        if re.fullmatch(r"[A-Za-z][A-Za-z ()/-]*", item):
            continue   # cụm tiếng Anh: được dùng trong ngoặc sau thuật ngữ Việt
        avoid.append(item)
    return avoid, note


def build(guide: str) -> dict:
    terms = []
    for en, use, other in table_rows(guide):
        avoid, note = parse_avoid(other)
        t = {"en": en, "use": use, "avoid": avoid}
        if note:
            t["note"] = note
        for a in avoid:
            if a in AMBIGUOUS:
                t.setdefault("ambiguous", {})[a] = AMBIGUOUS[a]
            if a in CONTEXT:
                t.setdefault("context", {})[a] = CONTEXT[a]
        terms.append(t)
    names_line = next((ln for ln in guide.splitlines() if ln.startswith("Tên riêng:")), "")
    names = [{"use": u, "avoid": [a]} for u, a in NAME_RULE.findall(names_line)]
    unused = (set(AMBIGUOUS) | set(CONTEXT)) - {a for t in terms for a in t["avoid"]}
    if unused:
        raise SystemExit(f"terms_policy.py: AMBIGUOUS/CONTEXT nhắc tới cụm không còn trong bảng: {sorted(unused)}")
    return {"version": 1, "terms": terms, "names": names, "exceptions": EXCEPTIONS}


def render(policy: dict) -> str:
    head = ("# Chính sách thuật ngữ, bản máy đọc. SINH TỰ ĐỘNG từ HUONG-DAN-VIET.md mục 3 bằng tools/terms_policy.py.\n"
            "# Không sửa tay: sửa bảng trong HUONG-DAN-VIET.md (hoặc AMBIGUOUS/CONTEXT/EXCEPTIONS trong tool) rồi chạy lại.\n"
            "# Dùng bởi tools/lint_terms.py.\n")
    return head + yaml.safe_dump(policy, allow_unicode=True, sort_keys=False, width=120)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="báo lỗi nếu file lệch HUONG-DAN-VIET.md")
    args = ap.parse_args(argv)
    text = render(build(GUIDE.read_text(encoding="utf-8")))
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"{OUT.relative_to(ROOT)} lệch HUONG-DAN-VIET.md — chạy: python tools/terms_policy.py", file=sys.stderr)
            return 1
        print(f"Chính sách thuật ngữ khớp HUONG-DAN-VIET.md ({text.count('- en:')} thuật ngữ).")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"Đã ghi {OUT.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
