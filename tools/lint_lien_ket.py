"""Linter link tới trang triết gia (README "Thêm nội dung" bước 2; rà soát 9/11/2026 mục 2.2; ban-giao/dot-5.md 5.9).

    python tools/lint_lien_ket.py            # in các chỗ (chế độ cảnh báo, luôn thoát mã 0)
    python tools/lint_lien_ket.py --write    # ghi báo cáo verification/lint/lint_lien_ket.md
    python tools/lint_lien_ket.py --strict   # thoát mã 1 khi có vi phạm (từ đợt 5.9)

Luật:
  - `thieu-link`: bài Lõi viết tay nhắc tên một triết gia đã có hồ sơ (`data/kb/people.yml`) mà cả bài không có link
    nào tới `triet-gia/<id>.md`. Đặt link ở lần nhắc đầu tiên trong văn xuôi.
  - `mien-thua`: mục trong `data/style/lien-ket-allow.yml` không còn khớp chỗ nào (xóa mục).

Tên được tìm: tên trên site (`name`), tên tiếng Anh (`name_en`, bỏ phần trong ngoặc), và họ của tên phương Tây nhiều chữ
("Kant", "Mill", "Beauvoir"); tên Trung Hoa, Việt Nam chỉ tìm đủ chữ. Bỏ Zeno xứ Citium (trùng tên Zeno xứ Elea).
Chỉ đếm văn xuôi: bỏ front matter, khối sinh, code, đích link, mục Nguồn và quiz (giữ chữ hiển thị của link).
Miễn: `data/style/lien-ket-allow.yml`, mỗi mục `page` (đường dẫn trong docs/), `person` (id), `reason`.
"""

from __future__ import annotations

import posixpath
import re
from pathlib import Path

import yaml

from lz import ROOT, units
from lz.lint import Finding, core_pages, main_guard, masked_lines, run, unit_at

PEOPLE = Path("data") / "kb" / "people.yml"
ALLOW_FILE = Path("data") / "style" / "lien-ket-allow.yml"
QUIZ = re.compile(r'<div class="oz-quiz"[^>]*>.*?</div>', re.S)
WORD = "A-Za-zÀ-ỹĐđ"
SKIP = {"zeno"}
FULL_NAME_ONLY = {"lao-tu", "khong-tu", "mac-tu", "manh-tu", "trang-tu", "tuan-tu", "han-phi", "chu-hy", "duc-phat",
                  "tran-nhan-tong", "chu-van-an", "nguyen-trai", "tran-duc-thao", "marcus-aurelius", "tue-trung"}
EXTRA = {"tue-trung": {"Tuệ Trung"}, "anselm": {"Anselm"}, "marcus-aurelius": {"Aurelius"}, "nagarjuna": {"Long Thụ"},
         "han-phi": {"Hàn Phi Tử"}}
RULES = {
    "thieu-link": "bài nhắc triết gia đã có hồ sơ mà không link tới trang hồ sơ",
    "mien-thua": "mục miễn không còn khớp chỗ nào",
}


def aliases(people: dict) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for pid, rec in people.items():
        if pid in SKIP:
            continue
        names = set()
        for field in ("name", "name_en"):
            v = (rec.get(field) or "").strip()
            v = re.sub(r"\s*\(.*?\)", "", v).strip()
            if not v:
                continue
            names.add(v)
            if pid not in FULL_NAME_ONLY and " " in v and " xứ " not in v and " of " not in v:
                names.add(v.split()[-1])
        names |= EXTRA.get(pid, set())
        out[pid] = {n for n in names if len(n) >= 4}
    return out


def pattern(names: set[str]) -> re.Pattern:
    alt = "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
    return re.compile(rf"(?<![{WORD}])(?:{alt})(?![{WORD}])")


def scan_page(path: str, raw: str, names: dict[str, set[str]], display: dict[str, str]) -> list[Finding]:
    us = units.split(path, raw)
    blanked = QUIZ.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), raw)
    lines = masked_lines(blanked, quotes=False, sources=True)
    out = []
    for pid, ns in names.items():
        if not ns or f"triet-gia/{pid}.md" in raw:
            continue
        pat = pattern(ns)
        for no in range(1, len(lines)):
            m = pat.search(lines[no])
            if m:
                rel = posixpath.relpath(f"triet-gia/{pid}.md", posixpath.dirname(path) or ".")
                out.append(Finding(path, no, unit_at(us, no), "thieu-link", f"{m.group(0)} ({pid})",
                                   f"đặt link ở lần nhắc đầu: [{display[pid]}]({rel})"))
                break
    return out


def load_allow(root: Path = ROOT) -> list[dict]:
    f = root / ALLOW_FILE
    items = (yaml.safe_load(f.read_text(encoding="utf-8")) if f.exists() else None) or []
    for it in items:
        if not all(isinstance(it.get(k), str) and it.get(k) for k in ("page", "person", "reason")):
            raise SystemExit(f"{ALLOW_FILE}: mỗi mục cần page, person, reason (chuỗi): {it}")
    return items


def collect():
    people = yaml.safe_load((ROOT / PEOPLE).read_text(encoding="utf-8"))
    names = aliases(people)
    display = {pid: rec["name"] for pid, rec in people.items()}
    findings = []
    for p in core_pages():
        findings += scan_page(p.path, p.file().read_text(encoding="utf-8"), names, display)
    allow = load_allow()
    used = [False] * len(allow)
    kept = []
    for f in findings:
        pid = f.found.rsplit("(", 1)[-1].rstrip(")")
        hit = next((i for i, a in enumerate(allow) if a["page"] == f.page and a["person"] == pid), None)
        if hit is None:
            kept.append(f)
        else:
            used[hit] = True
    for i, a in enumerate(allow):
        if not used[i]:
            kept.append(Finding(str(ALLOW_FILE), 0, "", "mien-thua", f"{a['page']}: {a['person']}", "xóa mục miễn"))
    return kept


def main(argv: list[str]) -> int:
    return run("lint_lien_ket", "Báo cáo linter link triết gia",
               "Sinh bằng `python tools/lint_lien_ket.py --write`. Phạm vi: Lõi viết tay. Lần đầu nhắc một triết gia đã có "
               "hồ sơ thì đặt link tới trang hồ sơ (README, \"Thêm nội dung\"); sửa trong đợt con của trang (ban-giao/dot-5.md).",
               RULES, collect, argv, __doc__)


if __name__ == "__main__":
    main_guard(main)
