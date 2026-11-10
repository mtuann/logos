"""Ứng viên sự kiện data/kb/events.yml (ban-giao/dot-2.md việc 2.8). Đợt con 5.2 lọc và kiểm.

    python tools/kb_events.py           # rút lại, ghi data/kb/events.yml và verification/lech/events.md
    python tools/kb_events.py --check   # mã thoát 1 khi events.yml lệch các trang (CI)

Phạm vi: văn xuôi Lõi viết tay của khối `lich-su` và `viet-nam`, cộng mọi câu có nhãn độ chắc chắn ở bài khác
(bỏ code, đích link, mục Nguồn; giữ trích dẫn). Mỗi năm (200–2029, hoặc kèm "TCN") cùng câu chứa nó thành một ứng viên:
`year`, `year_label` (chữ gốc), `text` (câu, tối đa 240 ký tự), `certainty` theo nhãn trong câu, `used_in`.
Số đứng ngay trước đơn vị đếm ("300 trang", "500 người") hay trước "chữ", kể cả số đầu một khoảng ("150–300 chữ",
"200–350 chữ": độ dài gợi ý cho bài viết; đợt 5.2), không phải năm.
Bỏ qua, có lý do (ghi ở verification/lech/events.md):
  - `nam-tac-pham`: năm trong "*Tên* (năm)" — thuộc works.yml;
  - `nam-song`: khoảng năm "(1258–1308)", "(k. 470–399 TCN)", và khoảng năm trong ô bảng niên biểu — năm sinh mất;
  - `quiz`: năm trong JSON của quiz; `philpapers`: "PhilPapers 2020".
Khóa: `<khối>.<trang>.<năm>` (thêm `-2`, `-3` khi một trang có nhiều câu cùng năm). Không thêm ngữ nghĩa: đây là danh
sách để kiểm, không phải danh sách sự kiện đã chọn. Trường `evidence`, `verified` được giữ khi rút lại.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

from kb_sources import slug
from lz import ROOT, registry, units
from lz.lint import masked_lines

OUT = ROOT / "data" / "kb" / "events.yml"
LECH = ROOT / "verification" / "lech" / "events.md"
KEEP = ("evidence", "verified")
BLOCKS = {"lich-su", "viet-nam"}
# Sau số không được là: chữ số, %, phần thập phân, đơn vị đếm (người, trang, câu, bài), hay "chữ" — kể cả khi số là
# đầu một khoảng ("200–350 chữ": cả 200 lẫn 350 là số chữ gợi ý cho bài viết, không phải năm; đợt 5.2).
YEAR = re.compile(r"(?<![\d.,/:§-])(?P<y>1\d{3}|20[0-2]\d|[2-9]\d{2})(?P<tcn>\s*TCN)?"
                  r"(?![\d%]|[.,]\d|\s*(?:người|trang|câu|bài)|(?:\s*[–-]\s*\d+)?\s*chữ)")
LABEL = re.compile(r"\[(chắc chắn|có cơ sở|suy đoán)\]")
CERTAINTY = {"chắc chắn": "chac-chan", "có cơ sở": "co-co-so", "suy đoán": "suy-doan"}
WORK_YEAR = re.compile(r"\*[^*\n]{2,160}?\*\s*\((?:khoảng |k\. |năm )?\d{3,4}[^)]*\)")
LIFESPAN = re.compile(r"\((?:k\. |khoảng )?\d{3,4}(?:\s*TCN)?\s*[–-]\s*(?:k\. )?\d{2,4}(?:\s*TCN)?\)")
RANGE = re.compile(r"(?:k\. )?\d{3,4}(?:/\d{3,4})?(?:\s*TCN)?\s*[–-]\s*(?:k\. )?\d{2,4}(?:\s*TCN)?")
PHILPAPERS = re.compile(r"PhilPapers(?: Survey)? 2020")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Ỹ\"“*(\[])")
HEAD = ("# Ứng viên sự kiện. RÚT TỰ ĐỘNG bằng tools/kb_events.py (năm + câu); đợt con 5.2 lọc và kiểm.\n"
        "# Chỉ evidence, verified được sửa ở đây. Schema: schema/kb/events.schema.json. Bỏ qua: verification/lech/events.md.\n")


def sentences(line: str):
    """(vị trí đầu, câu) của một dòng văn xuôi."""
    pos = 0
    for part in SENTENCE_END.split(line):
        start = line.index(part, pos)
        pos = start + len(part)
        yield start, part


def spans(rx: re.Pattern, s: str) -> list[tuple[int, int]]:
    return [m.span() for m in rx.finditer(s)]


def inside(i: int, sp: list[tuple[int, int]]) -> bool:
    return any(a <= i < b for a, b in sp)


def clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip(" -*>")
    return s if len(s) <= 240 else s[:239].rstrip() + "…"


def extract(root: Path = ROOT) -> tuple[dict, Counter]:
    recs: dict[str, dict] = {}
    skipped: Counter = Counter()
    for p in registry.load(root).select(tier="loi", generated=False):
        raw = p.file(root).read_text(encoding="utf-8")
        us = units.split(p.path, raw)
        whole = p.block in BLOCKS
        for no, line in enumerate(masked_lines(raw, quotes=False, sources=True)):
            if not line.strip() or (not whole and not LABEL.search(line)):
                continue
            if line.lstrip().startswith(("{", "[", "]")):
                skipped["quiz"] += len(YEAR.findall(line))
                continue
            table_row = line.lstrip().startswith("|")
            unit = next(u.key for u in us if u.start <= no <= u.end)
            for _, sent in sentences(line):
                if not whole and not LABEL.search(sent):
                    continue
                works, lives = spans(WORK_YEAR, sent), spans(LIFESPAN, sent)
                if table_row:   # bảng niên biểu: khoảng năm trong ô là năm sinh mất
                    lives += spans(RANGE, sent)
                pp = spans(PHILPAPERS, sent)
                lab = LABEL.search(sent)
                for m in YEAR.finditer(sent):
                    if inside(m.start(), works):
                        skipped["nam-tac-pham"] += 1
                        continue
                    if inside(m.start(), lives):
                        skipped["nam-song"] += 1
                        continue
                    if inside(m.start(), pp):
                        skipped["philpapers"] += 1
                        continue
                    year = -int(m.group("y")) if m.group("tcn") else int(m.group("y"))
                    base = f"{p.block}.{slug(p.path.split('/')[-1][:-3], 40)}.{str(year).replace('-', 'tcn')}"
                    text = clean(sent)
                    dup = next((k for k, r in recs.items() if k.startswith(base) and r["text"] == text), None)
                    if dup:
                        continue
                    key, n = base, 2
                    while key in recs:
                        key, n = f"{base}-{n}", n + 1
                    recs[key] = {"year": year, "year_label": m.group(0).strip(), "text": text,
                                 "certainty": CERTAINTY[lab.group(1)] if lab else None, "used_in": [unit],
                                 "evidence": [], "verified": None}
    return dict(sorted(recs.items())), skipped


def merge_kept(recs: dict, old: dict) -> dict:
    for key, r in recs.items():
        for f in KEEP:
            if f in (old.get(key) or {}):
                r[f] = old[key][f]
    return recs


def render(recs: dict) -> str:
    return HEAD + yaml.safe_dump(recs, allow_unicode=True, sort_keys=False, width=1_000_000)


def render_lech(recs: dict, skipped: Counter) -> str:
    by_cert = Counter(r["certainty"] or "khong-nhan" for r in recs.values())
    by_block = Counter(k.split(".")[0] for k in recs)
    L = ["# Danh sách lệch: sự kiện", "",
         "Sinh bằng `python tools/kb_events.py`. Đầu vào cho đợt con 5.2: lọc ứng viên nào là sự kiện cần kiểm.", "",
         f"- {len(recs)} ứng viên; theo khối: " + ", ".join(f"{b} {n}" for b, n in sorted(by_block.items())) + ".",
         "- Theo nhãn trong câu: " + ", ".join(f"{c} {n}" for c, n in sorted(by_cert.items())) + ".", "",
         "## Năm bỏ qua, có lý do", "",
         f"- `nam-tac-pham` ({skipped['nam-tac-pham']}): năm trong \"*Tên* (năm)\", đã ở `data/kb/works.yml`.",
         f"- `nam-song` ({skipped['nam-song']}): khoảng năm sinh mất trong ngoặc, thuộc `data/kb/people.yml` "
         "(người chưa có hồ sơ: đợt 5 xét thêm bản ghi người); gồm cả khoảng năm trong ô bảng niên biểu.",
         f"- `quiz` ({skipped['quiz']}): năm trong JSON của quiz (kiểm theo trang ở đợt 5).",
         f"- `philpapers` ({skipped['philpapers']}): \"PhilPapers 2020\" là tên khảo sát, không phải sự kiện."]
    return "\n".join(L) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="báo lỗi khi events.yml lệch các trang")
    args = ap.parse_args(argv)
    old = yaml.safe_load(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    recs, skipped = extract()
    recs = merge_kept(recs, old or {})
    text = render(recs)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("data/kb/events.yml lệch các trang — chạy: python tools/kb_events.py", file=sys.stderr)
            return 1
        print(f"Ứng viên sự kiện khớp các trang ({len(recs)} bản ghi).")
        return 0
    OUT.write_text(text, encoding="utf-8")
    LECH.parent.mkdir(parents=True, exist_ok=True)
    LECH.write_text(render_lech(recs, skipped), encoding="utf-8")
    print(f"Đã ghi data/kb/events.yml ({len(recs)} ứng viên) và verification/lech/events.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
