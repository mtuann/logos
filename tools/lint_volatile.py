"""Linter nội dung có hạn dùng trong Lõi viết tay (KE-HOACH.md mục 8; khối thời sự: mục 4, đợt 3).

    python tools/lint_volatile.py            # in các chỗ (chế độ cảnh báo tới hết đợt 3, luôn thoát mã 0)
    python tools/lint_volatile.py --write    # ghi báo cáo verification/lint/lint_volatile.md
    python tools/lint_volatile.py --strict   # thoát mã 1 khi có (chặn, từ đợt 3)

Tìm trong văn xuôi Lõi, ngoài khối thời sự, ngoài mục Nguồn, ngoài đích link, ngoài khối trích `!!! quote`/`>`
(lời của văn bản được trích, không phải lời của site):
  - `nam`: năm 2022 trở đi đứng riêng, trừ năm trong trích dẫn tác giả–năm ("Bourget & Chalmers 2023",
    "Hicks, Humphries và Slater (2024)", "Lucca và cộng sự 2025");
  - `cum-thoi-gian`: "hiện nay", "gần đây", "đến nay", "mới nhất"; "năm nay" trừ khi chỉ độ dài ("hai nghìn năm
    nay"); "tính đến" chỉ khi đi trước một mốc ("tính đến nay", "tính đến năm…"), không phải nghĩa "xét đến";
  - `van-ban-luat`: "Luật …" (viết hoa; trừ "Luật De Morgan" của logic), "Nghị định", "Bộ luật";
  - `thoi-su-qua-han`: khối thời sự trong data/thoi-su/ có `review_by` đã qua;
  - `mien-thua`: mục trong danh sách miễn không còn khớp chỗ nào (ngữ cảnh đã đổi chữ, hoặc chỗ đã dời đi).
Danh sách miễn data/style/volatile-allow.yml (quyết định 20): chỗ bị bắt nhưng không có hạn dùng, mỗi mục
`{unit, found, context, reason}`; chỉ có hiệu lực khi một dòng của đơn vị `unit` chứa đúng `context`.
So với tools/baseline_report.py (verification/bao-cao-nen.md mục 2): tính cả năm sau 2026, bỏ trích dẫn tác giả–năm,
bỏ khối trích và các nghĩa không chỉ thời điểm ở trên (đợt 3, việc 3.2).
"""

from __future__ import annotations

import datetime
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

from lz import ROOT, units
from lz.lint import Finding, core_pages, main_guard, masked_lines, run, unit_at

YEAR = re.compile(r"(?<![\d.,/-])(202[2-9]|20[3-9]\d)(?![\d])")
PHRASES = ["hiện nay", "gần đây", "tính đến", "đến nay", "mới nhất", "năm nay"]
PHRASE = re.compile(r"(?<![\wÀ-ỹ])(" + "|".join(PHRASES) + r")(?![\wÀ-ỹ])", re.I)
# "tính đến" là mốc thời gian chỉ khi theo sau là một mốc; còn lại là "xét đến" ("phải tính đến", "không tính đến").
TIME_MARK = re.compile(r"\s+(?:nay|năm|ngày|tháng|quý|thời điểm|hết|cuối|đầu|giữa|\d)", re.I)
# "năm nay" sau một số là độ dài ("hai nghìn năm nay"), không phải năm hiện tại.
DURATION = re.compile(r"(?:\d|nghìn|ngàn|trăm|chục|mươi|mấy|bao|nhiều)\s+$", re.I)
LAW = re.compile(r"(?<![\wÀ-ỹ])(Bộ luật|Nghị định|Luật (?!De Morgan)(?=[A-ZĐÂĂÊÔƠƯÁÀẢÃẠ]))")
# Năm trong trích dẫn tác giả–năm ("Bourget & Chalmers 2023", "(Kahane et al. 2022)") là năm xuất bản, không có
# hạn dùng: không tính. Tên tác giả viết hoa, có thể kèm "&"/"và" một tác giả thứ hai hoặc "et al.".
CITATION = re.compile(r"(?<!\S)(\S+?)(?:,? (?:&|và) (\S+?)| et al\.?| và (?:các )?cộng sự)?,? \(?$")
NOT_AUTHOR = {"năm", "tháng", "ngày", "từ", "đến", "trước", "sau"}


def is_citation(before: str) -> bool:
    m = CITATION.search(before)
    if not m:
        return False
    names = [n.strip("(;") for n in m.groups() if n]
    return all(n[:1].isupper() and n.lower() not in NOT_AUTHOR for n in names)
THOI_SU = ROOT / "data" / "thoi-su"
FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)
RULES = {
    "nam": "năm 2022 trở đi trong thân bài Lõi",
    "cum-thoi-gian": "cụm chỉ thời điểm (hiện nay, gần đây, tính đến…)",
    "van-ban-luat": "nhắc tới văn bản luật cụ thể",
    "thoi-su-qua-han": "khối thời sự quá hạn rà soát (`review_by`)",
    "mien-thua": "mục trong danh sách miễn không còn khớp chỗ nào",
}
HINT = "dời vào khối thời sự (data/thoi-su/) hoặc ghi vào danh sách miễn có lý do (quyết định 20)"
ALLOW = ROOT / "data" / "style" / "volatile-allow.yml"
REASONS = {
    "co-moc-thoi-gian": "câu đã gắn mốc ngày, nên đúng mãi",
    "vi-du-gia-dinh": "năm hoặc \"năm nay\" trong ví dụ, thí nghiệm tư duy, bài tập",
    "trang-thai-hoc-thuat": "\"đến nay/hiện nay\" nói về một tranh luận hay giới nghiên cứu, đổi theo thập kỷ",
    "chung-chung": "\"hiện nay\" nghĩa chung, không nêu dữ kiện kiểm được",
    "su-kien-lich-su": "văn bản pháp lý lịch sử có năm",
}


def ignored(rule: str, line: str, m: re.Match) -> bool:
    before = line[:m.start()]
    if rule == "nam":
        return is_citation(before)
    if rule == "cum-thoi-gian":
        word = m.group(0).lower()
        if word == "tính đến":
            return not TIME_MARK.match(line, m.end())
        if word == "năm nay":
            return bool(DURATION.search(before))
    return False


def raw_findings():
    """(Finding, dòng văn bản) của mọi chỗ bị bắt, trước khi xét danh sách miễn."""
    for p in core_pages():
        raw = p.file().read_text(encoding="utf-8")
        us = units.split(p.path, raw)
        for no, line in enumerate(masked_lines(raw, quotes=True, sources=True)):
            for rx, rule in ((YEAR, "nam"), (PHRASE, "cum-thoi-gian"), (LAW, "van-ban-luat")):
                for m in rx.finditer(line):
                    if not ignored(rule, line, m):
                        yield Finding(p.path, no, unit_at(us, no), rule, m.group(0).strip(), HINT), line


def load_allow(path: Path | None = None) -> list[dict]:
    path = path or ALLOW
    if not path.exists():
        return []
    entries = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    for i, e in enumerate(entries):
        bad = [k for k in ("unit", "found", "context", "reason") if not isinstance(e.get(k), str) or not e[k]]
        if bad or set(e) - {"unit", "found", "context", "reason", "note"}:
            raise ValueError(f"{path.name} mục {i + 1}: cần đúng các trường unit, found, context, reason (note tùy chọn)")
        if e["reason"] not in REASONS:
            raise ValueError(f"{path.name} mục {i + 1}: reason {e['reason']!r} không có trong {sorted(REASONS)}")
        if len(e["context"]) < 20 or e["found"].lower() not in e["context"].lower():
            raise ValueError(f"{path.name} mục {i + 1}: context phải ≥ 20 ký tự và chứa {e['found']!r}")
    return entries


def split_allowed(allow: list[dict] | None = None):
    """(chỗ còn lại, [(chỗ được miễn, mục)], mục không khớp chỗ nào)."""
    allow = load_allow() if allow is None else allow
    left, allowed, used = [], [], set()
    for f, line in raw_findings():
        hit = next((i for i, e in enumerate(allow) if e["unit"] == f.unit and e["found"].lower() == f.found.lower()
                    and e["context"] in line), None)
        if hit is None:
            left.append(f)
        else:
            used.add(hit)
            allowed.append((f, allow[hit]))
    return left, allowed, [e for i, e in enumerate(allow) if i not in used]


def collect(today: datetime.date | None = None):
    left, _, unused = split_allowed()
    yield from left
    for e in unused:
        page = e["unit"].split("#")[0]
        yield Finding(page, 0, e["unit"], "mien-thua", e["found"],
                      f"mục miễn ({e['reason']}) không còn khớp: ngữ cảnh \"{e['context']}\" đã đổi hoặc đã dời")
    if THOI_SU.is_dir():
        today = today or datetime.date.today()
        for f in sorted(THOI_SU.glob("*.md")):
            m = FRONT.match(f.read_text(encoding="utf-8"))
            meta = (yaml.safe_load(m.group(1)) or {}) if m else {}
            due = meta.get("review_by")
            if isinstance(due, str):
                due = datetime.date.fromisoformat(due)
            if isinstance(due, datetime.date) and due < today:
                yield Finding(str(f.relative_to(ROOT)), 0, "", "thoi-su-qua-han", str(due),
                              "rà soát lại, cập nhật `updated_to` và `review_by`")


def render_allowed(allowed) -> str:
    by = Counter(e["reason"] for _, e in allowed)
    L = ["", f"## Chỗ được miễn ({len(allowed)})", "",
         "Theo `data/style/volatile-allow.yml` (quyết định 20). Mục miễn hết hiệu lực khi ngữ cảnh đổi chữ.", "",
         "| Lý do | Nghĩa | Số chỗ |", "|---|---|---:|"]
    L += [f"| `{r}` | {d} | {by.get(r, 0)} |" for r, d in REASONS.items()]
    L += ["", "| Vị trí | Đơn vị | Tìm thấy | Lý do |", "|---|---|---|---|"]
    L += [f"| `{f.page}:{f.line}` | `{f.unit}` | {f.found} | `{e['reason']}` |" for f, e in allowed]
    return "\n".join(L) + "\n"


def main(argv: list[str]) -> int:
    code = run("lint_volatile", "Báo cáo linter nội dung có hạn dùng",
               "Sinh bằng `python tools/lint_volatile.py --write`. Phạm vi: Lõi viết tay, bỏ mục Nguồn, đích link, "
               "khối trích. Đầu đợt 1: 90 chỗ (luật cũ, `verification/bao-cao-nen.md` mục 2). Đợt 3 dời chỗ có hạn "
               "dùng vào khối thời sự (`data/thoi-su/`), chỗ còn lại vào danh sách miễn có lý do; đích là 0.",
               RULES, collect, argv, __doc__)
    if "--write" in argv:
        out = ROOT / "verification" / "lint" / "lint_volatile.md"
        _, allowed, _ = split_allowed()
        allowed.sort(key=lambda fe: (fe[0].page, fe[0].line, fe[0].found))
        out.write_text(out.read_text(encoding="utf-8") + render_allowed(allowed), encoding="utf-8")
    return code


if __name__ == "__main__":
    main_guard(main)
