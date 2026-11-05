"""Linter dữ kiện: năm của tác phẩm và năm sinh mất trong văn xuôi Lõi so với kho dữ kiện (KE-HOACH.md mục 8;
ban-giao/dot-2.md việc 2.9).

    python tools/lint_facts.py            # in các chỗ (chế độ cảnh báo, luôn thoát mã 0)
    python tools/lint_facts.py --write    # ghi báo cáo verification/lint/lint_facts.md
    python tools/lint_facts.py --strict   # thoát mã 1 khi có (chặn, sau hai tuần cảnh báo)

Luật:
  - `nam-tac-pham`: "*Tên* (năm)" mà tác phẩm trong data/kb/works.yml đã chốt một năm khác;
  - `nam-chua-chot`: "*Tên* (năm)" mà works.yml chưa chốt năm (các chỗ dùng ghi khác nhau; xem verification/lech/works.md);
  - `nam-song`: "[Tên](../triet-gia/<id>.md) (năm–năm)" hoặc "Tên (năm–năm)" với Tên là tên trong people.yml,
    mà năm khác `born`/`died` của người đó.
"""

from __future__ import annotations

import re

import yaml

from kb_works import WORK_YEAR, norm, year_of
from lz import ROOT, units
from lz.lint import Finding, core_pages, main_guard, masked_lines, run

KB = ROOT / "data" / "kb"
LIFE = re.compile(r"(?:\[(?P<link>[^\]]+)\]\((?:\.\./)*triet-gia/(?P<id>[a-z0-9-]+)\.md\)|(?P<name>[A-ZÀ-Ỹ][\w'’.-]*(?: [A-ZÀ-Ỹ][\w'’.-]*){0,3}))"
                  r" \((?:k\. |khoảng )?(?P<b>\d{1,4})(?P<btcn> TCN)?\s*[–-]\s*(?:k\. |khoảng )?(?P<d>\d{1,4})(?P<dtcn> TCN)?\)")
RULES = {
    "nam-tac-pham": "năm của tác phẩm khác năm đã chốt trong works.yml",
    "nam-chua-chot": "tác phẩm có nhiều năm khác nhau giữa các trang, works.yml chưa chốt",
    "nam-song": "năm sinh mất khác people.yml",
}


def collect():
    works = yaml.safe_load((KB / "works.yml").read_text(encoding="utf-8")) or {}
    people = yaml.safe_load((KB / "people.yml").read_text(encoding="utf-8")) or {}
    by_title = {}
    for k, w in works.items():
        for t in w["titles"]:
            by_title.setdefault(norm(t), k)
    by_name = {norm(p["name"]): pid for pid, p in people.items()}
    for p in core_pages():
        raw = p.file().read_text(encoding="utf-8")
        us = units.split(p.path, raw)
        for no, line in enumerate(masked_lines(raw, quotes=False, sources=True)):
            if not line.strip():
                continue
            unit = next(u.key for u in us if u.start <= no <= u.end)
            for m in WORK_YEAR.finditer(line):
                key = by_title.get(norm(m.group(1).strip()))
                if not key:
                    continue
                y, w = year_of(m.group(2), m.group(3)), works[key]
                if w["year"] is None:
                    yield Finding(p.path, no, unit, "nam-chua-chot", f"*{m.group(1)}* ({y})",
                                  f"`{key}` gặp với các năm {', '.join(w['years_seen'])}")
                elif y != w["year"]:
                    yield Finding(p.path, no, unit, "nam-tac-pham", f"*{m.group(1)}* ({y})", f"`{key}`: {w['year']}")
            # đích link đã bị che trong masked_lines: đọc lại dòng gốc cho mẫu link triết gia
            src = raw.split("\n")[no - 1] if no - 1 < len(raw.split("\n")) else ""
            for m in LIFE.finditer(src):
                pid = m.group("id") or by_name.get(norm(m.group("name") or ""))
                if not pid or pid not in people:
                    continue
                b = -int(m.group("b")) if m.group("btcn") or m.group("dtcn") else int(m.group("b"))
                d = -int(m.group("d")) if m.group("dtcn") else int(m.group("d"))
                if len(m.group("d")) < len(m.group("b")) and not m.group("dtcn"):
                    continue   # dạng rút gọn "1724–04": bỏ qua, không đoán
                rec = people[pid]
                if (b, d) != (rec["born"], rec["died"]):
                    yield Finding(p.path, no, unit, "nam-song", m.group(0),
                                  f"people.yml `{pid}`: {rec['years_label']} (born {rec['born']}, died {rec['died']})")


def main(argv: list[str]) -> int:
    return run("lint_facts", "Báo cáo linter dữ kiện",
               "Sinh bằng `python tools/lint_facts.py --write`. Phạm vi: Lõi viết tay, bỏ mục Nguồn. So với "
               "`data/kb/works.yml` và `data/kb/people.yml`. Đây là báo cáo nền của đợt 2: chỉ ghi lại, sửa ở đợt 5.",
               RULES, collect, argv, __doc__)


if __name__ == "__main__":
    main_guard(main)
