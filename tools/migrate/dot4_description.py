"""Đợt 4, việc 4.10: số đếm gõ tay trong `description` → [[count:…]] (hook kb.py mở shortcode trong description từ 4.10).

    python tools/migrate/dot4_description.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys

from thay_shortcode import apply

SUBS = [
    ("cau-hoi/index.md", 3, 'description: "57 câu hỏi', 'description: "[[count:cau-hoi]] câu hỏi'),
    ("doc/index.md", 3, 'description: "19 hướng dẫn', 'description: "[[count:doc]] hướng dẫn'),
]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    done, pages = apply(SUBS, args.dry_run)
    print(f"{'(thử) ' if args.dry_run else ''}Thay {done} số đếm trong description ở {pages} trang.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
