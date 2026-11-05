"""Linter nội dung có hạn dùng trong Lõi viết tay (KE-HOACH.md mục 8; khối thời sự: mục 4, đợt 3).

    python tools/lint_volatile.py            # in các chỗ (chế độ cảnh báo tới hết đợt 3, luôn thoát mã 0)
    python tools/lint_volatile.py --write    # ghi báo cáo verification/lint/lint_volatile.md
    python tools/lint_volatile.py --strict   # thoát mã 1 khi có (chặn, từ đợt 3)

Tìm trong văn xuôi Lõi, ngoài khối thời sự và ngoài mục Nguồn, ngoài đích link:
  - `nam`: năm 2022 trở đi đứng riêng, trừ năm trong trích dẫn tác giả–năm ("Bourget & Chalmers 2023");
  - `cum-thoi-gian`: "hiện nay", "gần đây", "tính đến", "đến nay", "mới nhất", "năm nay";
  - `van-ban-luat`: "Luật …" (viết hoa), "Nghị định", "Bộ luật";
  - `thoi-su-qua-han`: khối thời sự trong data/thoi-su/ có `review_by` đã qua (khi thư mục đó có, từ đợt 3).
Cách đếm giống tools/baseline_report.py (để so với verification/bao-cao-nen.md mục 2), trừ hai điểm: tính cả năm
sau 2026 (dự báo "năm 2030"…), và bỏ năm trong trích dẫn tác giả–năm.
"""

from __future__ import annotations

import datetime
import re

import yaml

from lz import ROOT, units
from lz.lint import Finding, core_pages, main_guard, masked_lines, run, unit_at

YEAR = re.compile(r"(?<![\d.,/-])(202[2-9]|20[3-9]\d)(?![\d])")
PHRASES = ["hiện nay", "gần đây", "tính đến", "đến nay", "mới nhất", "năm nay"]
PHRASE = re.compile(r"(?<![\wÀ-ỹ])(" + "|".join(PHRASES) + r")(?![\wÀ-ỹ])", re.I)
LAW = re.compile(r"(?<![\wÀ-ỹ])(Bộ luật|Nghị định|Luật (?=[A-ZĐÂĂÊÔƠƯÁÀẢÃẠ]))")
# Năm trong trích dẫn tác giả–năm ("Bourget & Chalmers 2023", "(Kahane et al. 2022)") là năm xuất bản, không có
# hạn dùng: không tính. Tên tác giả viết hoa, có thể kèm "&"/"và" một tác giả thứ hai hoặc "et al.".
CITATION = re.compile(r"(?<!\S)(\S+?)(?:,? (?:&|và) (\S+?)| et al\.?)?,? $")
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
}
HINT = "dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5)"


def collect(today: datetime.date | None = None):
    for p in core_pages():
        raw = p.file().read_text(encoding="utf-8")
        us = units.split(p.path, raw)
        for no, line in enumerate(masked_lines(raw, quotes=False, sources=True)):
            for rx, rule in ((YEAR, "nam"), (PHRASE, "cum-thoi-gian"), (LAW, "van-ban-luat")):
                for m in rx.finditer(line):
                    if rule == "nam" and is_citation(line[:m.start()]):
                        continue
                    yield Finding(p.path, no, unit_at(us, no), rule, m.group(0).strip(), HINT)
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


def main(argv: list[str]) -> int:
    return run("lint_volatile", "Báo cáo linter nội dung có hạn dùng",
               "Sinh bằng `python tools/lint_volatile.py --write`. Phạm vi: Lõi viết tay, bỏ mục Nguồn và đích link. "
               "Đây là báo cáo nền của đợt 1 (so với `verification/bao-cao-nen.md` mục 2); "
               "đợt 3 dời các chỗ này vào khối thời sự, đích là 0.",
               RULES, collect, argv, __doc__)


if __name__ == "__main__":
    main_guard(main)
