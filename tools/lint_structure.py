"""Linter cấu trúc trang theo loại (KE-HOACH.md mục 5.1, 8).

    python tools/lint_structure.py            # in các chỗ (chế độ cảnh báo, luôn thoát mã 0)
    python tools/lint_structure.py --write    # ghi báo cáo verification/lint/lint_structure.md
    python tools/lint_structure.py --strict   # thoát mã 1 khi có vi phạm

Luật:
  - `thieu-muc`: trang thiếu mục H2 bắt buộc theo `type` (KE-HOACH.md mục 5.1). So tiêu đề không phân biệt hoa
    thường, bỏ dấu `?`, `.`, `:` ở cuối và thuộc tính `{…}` (như tools/baseline_report.py). "Đọc văn bản gốc"
    của bài cau-hoi là tùy chọn nên không kiểm.
  - `thieu-tom-tat`: bài cau-hoi thiếu hộp `!!! summary "Tóm tắt 5 phút"`.
  - `nhan-chac-chan`: nhãn độ chắc chắn [chắc chắn] / [có cơ sở] / [suy đoán] nằm ngoài bài có đoạn chú giải
    "Cách đọc nhãn độ chắc chắn", hoặc nằm trong front matter, `philosophers.json`, `terms.json`, hồ sơ triết gia
    (HUONG-DAN-VIET.md mục 4: ở đó nó hiện ra trơ trọi).
"""

from __future__ import annotations

import re

from lz import ROOT, units
from lz.lint import FRONT, Finding, core_pages, main_guard, run

REQUIRED = {
    "cau-hoi": ["Thí nghiệm tư duy", "Câu hỏi thật sự là gì?", "Các lập trường chính", "Giới triết học ngày nay nghĩ gì",
                "Liên hệ đời sống", "Tự kiểm tra", "Tự viết", "Nguồn"],
    "cong-cu": ["Bài tập", "Tự kiểm tra", "Đi tiếp", "Nguồn"],
    "lich-su": ["Đọc tiếp", "Nguồn"],
    "doc": ["Bối cảnh", "Đọc từng đoạn", "Tái dựng lập luận", "Phản bác", "Hiểu lầm thường gặp", "Tự kiểm tra",
            "Câu hỏi để tự viết", "Đọc tiếp", "Nguồn"],
}
SUMMARY = re.compile(r'^!!! summary "Tóm tắt 5 phút"', re.M)
LABEL = re.compile(r"\[(chắc chắn|có cơ sở|suy đoán)\]")
LEGEND = "Cách đọc nhãn độ chắc chắn"
DATA_FILES = ["data/kb/people.yml", "docs/assets/data/terms.json"] + sorted(
    f"data/people/{f.name}" for f in (ROOT / "data" / "people").glob("*.yml"))
RULES = {
    "thieu-muc": "thiếu mục H2 bắt buộc theo loại trang (KE-HOACH.md mục 5.1)",
    "thieu-tom-tat": "bài cau-hoi thiếu hộp \"Tóm tắt 5 phút\"",
    "nhan-chac-chan": "nhãn độ chắc chắn ngoài bài có chú giải, hoặc trong front matter/dữ liệu",
}


def norm_heading(h: str) -> str:
    h = re.sub(r"\s*\{[^}]*\}\s*$", "", h).strip()
    # Đợt 5.4: phần ghi chú trong ngoặc ở cuối không đổi loại mục ("Đọc từng đoạn (diễn ý)").
    h = re.sub(r"\s*\([^)]*\)$", "", h).strip()
    return re.sub(r"[?.:!]+$", "", h).strip().lower()


def collect():
    for p in core_pages():
        raw = p.file().read_text(encoding="utf-8")
        us = units.split(p.path, raw)
        req = REQUIRED.get(p.type)
        if req:
            have = {norm_heading(u.title) for u in us[1:]}
            for h in req:
                if norm_heading(h) not in have:
                    yield Finding(p.path, 0, "", "thieu-muc", h, "thêm mục, hoặc ghi ngoại lệ (quyết định của chủ biên)")
        if p.type == "cau-hoi" and not SUMMARY.search(raw):
            yield Finding(p.path, 0, f"{p.path}#_dau", "thieu-tom-tat", "Tóm tắt 5 phút", "thêm hộp ở đầu bài")
        fm = FRONT.match(raw)
        fm_end = fm.group(0).count("\n") if fm else 0
        has_legend = LEGEND in raw
        for no, line in enumerate(raw.split("\n"), start=1):
            for m in LABEL.finditer(line):
                if no <= fm_end:
                    yield Finding(p.path, no, "", "nhan-chac-chan", m.group(0), "bỏ nhãn khỏi front matter (title, description)")
                elif not has_legend:
                    u = next((x.key for x in us if x.start <= no <= x.end), "")
                    yield Finding(p.path, no, u, "nhan-chac-chan", m.group(0),
                                  f"bài không có đoạn chú giải \"{LEGEND}\": thêm chú giải hoặc bỏ nhãn")
    for rel in DATA_FILES:
        f = ROOT / rel
        if not f.exists():
            continue
        for no, line in enumerate(f.read_text(encoding="utf-8").split("\n"), start=1):
            for m in LABEL.finditer(line):
                yield Finding(rel, no, "", "nhan-chac-chan", m.group(0), "bỏ nhãn khỏi dữ liệu (hiện ra trơ trọi ở chỉ mục, dòng thời gian)")


def main(argv: list[str]) -> int:
    return run("lint_structure", "Báo cáo linter cấu trúc",
               "Sinh bằng `python tools/lint_structure.py --write`. Phạm vi: Lõi viết tay và dữ liệu Lõi có văn xuôi. "
               "Đây là báo cáo nền của đợt 1: chỉ ghi lại; bổ sung mục hay ghi ngoại lệ là quyết định của chủ biên.",
               RULES, collect, argv, __doc__)


if __name__ == "__main__":
    main_guard(main)
