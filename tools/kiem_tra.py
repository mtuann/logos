"""Chạy mọi kiểm tra nhanh của repo song song (đợt 7, thay 24 bước một lệnh trong CI và các vòng lặp trong AGENTS.md).

    uv run python tools/kiem_tra.py        # mã thoát 1 nếu có kiểm tra đỏ; in phần cuối đầu ra của kiểm tra đỏ

Gồm: trang và dữ liệu sinh tự động khớp nguồn (--check), sổ đăng ký nội dung, id mục H2, sổ kiểm chứng, kho dữ kiện,
khối thời sự, nội dung có hạn dùng, sáu linter nội dung (--strict). Không gồm build, kiểm thử Python/JS (chạy riêng).
Các kiểm tra chỉ đọc, độc lập với nhau, nên chạy song song được.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GEN = ["gen_glossary", "figures", "review_check", "timeline", "influence", "philosophers", "book", "frontmatter_check",
       "quiz_bank", "terms_policy", "kb_sources", "kb_works", "kb_quotes", "kb_philpapers", "kb_events", "works_page",
       "verification_page", "nav_gen", "content_registry", "add_heading_ids", "check_ledger", "kb_check",
       "thoi_su_check"]
STRICT = ["lint_volatile", "lint_terms", "lint_structure", "lint_facts", "lint_quotes", "lint_so_lieu", "lint_lien_ket"]

CHECKS = [(t, ["--check"]) for t in GEN] + [(t, ["--strict", "-q"]) for t in STRICT]


def run(tool: str, args: list[str]) -> tuple[str, int, str, float]:
    t0 = time.time()
    p = subprocess.run([sys.executable, f"tools/{tool}.py", *args], cwd=ROOT, capture_output=True, text=True)
    return tool, p.returncode, (p.stdout + p.stderr).strip(), time.time() - t0


def main() -> int:
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        results = list(ex.map(lambda c: run(*c), CHECKS))
    bad = [r for r in results if r[1] != 0]
    for tool, code, out, dt in results:
        print(f"{'✓' if code == 0 else '✗'} {tool:<20} {dt:5.1f}s")
    for tool, _, out, _ in bad:
        print(f"\n--- {tool} ---\n" + "\n".join(out.splitlines()[-25:]))
    print(f"\n{len(results) - len(bad)}/{len(results)} kiểm tra xanh trong {time.time() - t0:.1f}s.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
