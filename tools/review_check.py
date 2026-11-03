"""Báo cáo tình trạng rà soát nội dung (docs/them/cap-nhat.md).

Quét mọi trang docs/**/*.md lấy ngày `updated:` trong front matter, rồi sinh
mục "Tình trạng rà soát" giữa hai dấu <!-- gen:review --> và <!-- /gen:review -->.

    python tools/review_check.py          # ghi lại mục
    python tools/review_check.py --check  # báo lỗi (mã thoát 1) nếu trang lệch

Lưu ý: --check chỉ kiểm tra mục sinh ra có khớp trang không (để trang luôn
trung thực), chứ không bắt bài phải "tươi" — việc rà soát là quyết định của
người biên tập, không phải của CI.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PAGE = ROOT / "docs" / "them" / "cap-nhat.md"
START, END = "<!-- gen:review -->", "<!-- /gen:review -->"

# Bài quá số tháng này mà chưa rà soát lại thì liệt vào "cần rà soát".
STALE_MONTHS = 12

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
FIELD = re.compile(r"^(title|updated):\s*(.+?)\s*$", re.M)
DATE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def page_meta(path: Path) -> tuple[str, date | None]:
    """Trả về (tiêu đề, ngày updated) của một trang Markdown."""
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    title, updated = path.stem, None
    if m:
        for key, val in FIELD.findall(m.group(1)):
            if key == "title":
                title = val.strip().strip("\"'")
            elif key == "updated":
                d = DATE.match(val.strip())
                if d:
                    updated = date(int(d.group(1)), int(d.group(2)), int(d.group(3)))
    return title, updated


def collect(today: date | None = None) -> tuple[list, list]:
    """Trả về (danh sách tươi, danh sách cần rà soát), mỗi mục (title, updated, relpath)."""
    today = today or date.today()
    fresh, stale = [], []
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS).as_posix()
        # Bỏ qua trang chỉ mục, trang hệ thống và chính trang cập nhật.
        if path.name in ("index.md", "cap-nhat.md"):
            continue
        title, updated = page_meta(path)
        if updated is None:
            stale.append((title, None, rel))
            continue
        months = (today.year - updated.year) * 12 + (today.month - updated.month)
        (stale if months >= STALE_MONTHS else fresh).append((title, updated, rel))
    stale.sort(key=lambda x: (x[1] is not None, x[1] or date.min))
    return fresh, stale


def render(today: date | None = None) -> str:
    today = today or date.today()
    fresh, stale = collect(today)
    lines = ["## Tình trạng rà soát", ""]
    lines.append(
        f"{len(fresh)} bài đã được rà soát trong {STALE_MONTHS} tháng qua "
        f"(tính từ ngày build)."
    )
    lines.append("")
    if not stale:
        lines.append("Không có bài nào quá hạn rà soát.")
    else:
        lines.append(f"**{len(stale)} bài cần rà soát lại** (quá {STALE_MONTHS} tháng chưa cập nhật):")
        lines.append("")
        for title, updated, rel in stale:
            when = updated.strftime("%d/%m/%Y") if updated else "không rõ ngày"
            lines.append(f"- [{title}](../{rel}) — cập nhật lần cuối: {when}")
    lines.append("")
    return "\n".join(lines)


def write() -> None:
    text = PAGE.read_text(encoding="utf-8")
    section = render()
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        text = before + START + "\n" + section + END + after
    else:
        text = text.rstrip("\n") + "\n\n" + START + "\n" + section + END + "\n"
    PAGE.write_text(text, encoding="utf-8")
    print(f"Đã cập nhật mục rà soát trong {PAGE.relative_to(ROOT)}")


def check() -> int:
    text = PAGE.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print("Trang cập nhật thiếu mục rà soát — chạy: python tools/review_check.py")
        return 1
    before, rest = text.split(START, 1)
    current, after = rest.split(END, 1)
    expected = "\n" + render() + ""
    if current != expected:
        print("Mục rà soát lệch với dữ liệu — chạy: python tools/review_check.py")
        return 1
    print("Mục rà soát khớp dữ liệu.")
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    write()
