"""Đợt 3, việc 3.4: số đếm nội dung site gõ tay → [[count:…]] (hooks/kb.py).

    python tools/migrate/dot3_so_dem.py [--dry-run]

Chỉ thay số đếm nội dung của site (số bài theo loại trang, số đoạn ngụy biện, số triết gia), ở trang chủ và trang
hệ thống. Không thay: `description` trong front matter (hook không mở shortcode ở đó; ghi ở nhật ký), số trong
`them/cap-nhat.md` (nhật ký thay đổi: số của từng thời điểm), số theo phiên luyện tập ("10 đoạn", "5 thuật ngữ"),
số viết bằng chữ ("mười một chủ đề"), số liệu PhilPapers (việc 3.5).
"""

from __future__ import annotations

import argparse
import sys

from thay_shortcode import apply

SUBS = [
    ("index.md", 61, "15 bài:", "[[count:cong-cu]] bài:"),
    ("index.md", 69, "57 câu hỏi chưa", "[[count:cau-hoi]] câu hỏi chưa"),
    ("index.md", 77, "19 hướng dẫn đọc", "[[count:doc]] hướng dẫn đọc"),
    ("index.md", 93, "100 đoạn hội thoại", "[[count:nguy-bien]] đoạn hội thoại"),
    ("bat-dau/lo-trinh.md", 14, "15 bài công cụ", "[[count:cong-cu]] bài công cụ"),
    ("bat-dau/lo-trinh.md", 14, "57 bài về", "[[count:cau-hoi]] bài về"),
    ("bat-dau/lo-trinh.md", 14, "8 bài lịch sử", "[[count:lich-su]] bài lịch sử"),
    ("bat-dau/lo-trinh.md", 14, "19 hướng dẫn đọc", "[[count:doc]] hướng dẫn đọc"),
    ("bat-dau/lo-trinh.md", 32, "100 đoạn hội thoại", "[[count:nguy-bien]] đoạn hội thoại"),
    ("bat-dau/lo-trinh.md", 36, "Có 57 bài,", "Có [[count:cau-hoi]] bài,"),
    ("bat-dau/lo-trinh.md", 51, "8 bài theo thời kỳ", "[[count:lich-su]] bài theo thời kỳ"),
    ("bat-dau/lo-trinh.md", 53, "19 hướng dẫn đọc", "[[count:doc]] hướng dẫn đọc"),
    ("cau-hoi/index.md", 13, "**57 bài**", "**[[count:cau-hoi]] bài**"),
    ("lich-su/index.md", 12, "59 triết gia", "[[count:triet-gia]] triết gia"),
    ("cong-cu/index.md", 79, "100 đoạn hội thoại", "[[count:nguy-bien]] đoạn hội thoại"),
    ("luyen-tap/index.md", 16, "100 đoạn hội thoại", "[[count:nguy-bien]] đoạn hội thoại"),
]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    done, pages = apply(SUBS, args.dry_run)
    print(f"{'(thử) ' if args.dry_run else ''}Thay {done} số đếm ở {pages} trang.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
