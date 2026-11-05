"""Linter trích dẫn: khối !!! quote trong trang so với bản ghi đang lưu ở data/kb/quotes.yml (KE-HOACH.md mục 8;
quyết định 3: trích dẫn đối chiếu bằng linter, không thay bằng shortcode; ban-giao/dot-2.md việc 2.9).

    python tools/lint_quotes.py            # in các chỗ (chế độ cảnh báo, luôn thoát mã 0)
    python tools/lint_quotes.py --write    # ghi báo cáo verification/lint/lint_quotes.md
    python tools/lint_quotes.py --strict   # thoát mã 1 khi có

Luật:
  - `khong-khop`: khối trong trang không trùng (tiêu đề, thân) với bản ghi nào trong quotes.yml — chữ trích đã đổi
    mà kho chưa cập nhật (sau đợt 5: đổi một trích dẫn đã kiểm phải đi qua kho, có bằng chứng);
  - `mo-coi`: bản ghi trỏ tới một đơn vị không còn chứa khối đó;
  - `chua-ghep-tac-pham`: bản ghi chưa có `work` (thông tin cho đợt con 5.2);
  - `chua-co-vi-tri`: bản ghi chưa có `locator` (38a, §IV, 2A6…; điền ở đợt 5).
"""

from __future__ import annotations

import yaml

from kb_quotes import page_blocks
from lz import ROOT, units
from lz.lint import Finding, core_pages, main_guard, run

QUOTES = ROOT / "data" / "kb" / "quotes.yml"
RULES = {
    "khong-khop": "khối trích trong trang không khớp bản ghi nào trong quotes.yml",
    "mo-coi": "bản ghi trỏ tới đơn vị không còn chứa khối trích",
    "chua-ghep-tac-pham": "bản ghi chưa ghép với tác phẩm trong works.yml",
    "chua-co-vi-tri": "bản ghi chưa có vị trí trích (locator)",
}


def collect():
    recs = yaml.safe_load(QUOTES.read_text(encoding="utf-8")) or {}
    stored = {(r["title"], r["body"]): k for k, r in recs.items() if "body" in r}
    seen: dict[str, set] = {}
    for p in core_pages():
        raw = p.file().read_text(encoding="utf-8")
        us = units.split(p.path, raw)
        for lineno, title, body in page_blocks(p.path, raw):
            unit = next(u.key for u in us if u.start <= lineno <= u.end)
            key = stored.get((title, body))
            if key is None:
                yield Finding(p.path, lineno, unit, "khong-khop", f"\"{title}\"",
                              "chạy tools/kb_quotes.py; nếu là trích dẫn đã kiểm, kiểm lại và cập nhật bằng chứng")
            else:
                seen.setdefault(key, set()).add(unit)
    for key, r in recs.items():
        where = r["used_in"][0]
        if "body" in r and where not in seen.get(key, set()):
            yield Finding("data/kb/quotes.yml", 0, where, "mo-coi", key, "chạy tools/kb_quotes.py")
        if not r.get("work"):
            yield Finding("data/kb/quotes.yml", 0, where, "chua-ghep-tac-pham", key, f"\"{r['title']}\"")
        if not r.get("locator"):
            yield Finding("data/kb/quotes.yml", 0, where, "chua-co-vi-tri", key, f"\"{r['title']}\"")


def main(argv: list[str]) -> int:
    return run("lint_quotes", "Báo cáo linter trích dẫn",
               "Sinh bằng `python tools/lint_quotes.py --write`. So khối `!!! quote` của Lõi viết tay với "
               "`data/kb/quotes.yml`. Đây là báo cáo nền của đợt 2: chỉ ghi lại, bổ sung ở đợt 5.",
               RULES, collect, argv, __doc__)


if __name__ == "__main__":
    main_guard(main)
