"""Kiểm tra frontmatter YAML hợp lệ cho mọi trang docs/**/*.md.

MkDocs parse frontmatter bằng YAML strict: một block lỗi (thường do title/
description chứa ': ' mà không được quote) khiến TOÀN BỘ frontmatter rơi ra
body dưới dạng text (bug live 14/10/2026, 40 trang).

    python tools/frontmatter_check.py          # báo cáo
    python tools/frontmatter_check.py --check  # mã thoát 1 nếu có file lỗi
"""

from __future__ import annotations

import glob
import re
import sys

import yaml

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def invalid_files() -> list[tuple[str, str]]:
    bad = []
    for path in sorted(glob.glob("docs/**/*.md", recursive=True)):
        text = open(path, encoding="utf-8").read()
        m = FRONT_MATTER.match(text)
        if not m:
            continue
        try:
            yaml.safe_load(m.group(1))
        except yaml.YAMLError as e:
            bad.append((path, str(e).split("\n")[0]))
    return bad


def main(argv: list[str]) -> int:
    bad = invalid_files()
    if bad:
        print(f"Frontmatter YAML lỗi ở {len(bad)} file:", file=sys.stderr)
        for path, err in bad:
            print(f"  {path}: {err}", file=sys.stderr)
        print("Gợi ý: quote title/description bằng \"...\" khi chứa ': '.", file=sys.stderr)
        return 1
    print("Frontmatter hợp lệ ở mọi trang.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
