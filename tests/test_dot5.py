"""Tên site (quyết định 27, 40). Chạy: python -m unittest discover -s tests

Script đổi tên một lần của đợt 5.0d (tools/migrate/dot5_ten.py) đã chạy xong; không còn kiểm thử chạy lại script đó."""

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Chỗ được giữ "Logos Zero": nói tới site song song logos-zero, hoặc lịch sử dự án (không hiện trên site).
GIU = {"KE-HOACH.md", "README.md", "pyproject.toml", "AGENTS.md", "tests/test_parity.py", "tests/test_dot5.py"}


class TestTenSite(unittest.TestCase):
    def test_no_old_name_outside_allowed_files(self):
        out = subprocess.run(["git", "grep", "-l", "Logos Zero"], cwd=ROOT, capture_output=True, text=True).stdout.split()
        left = [f for f in out if f not in GIU and not f.startswith(("ban-giao/", "verification/"))]
        self.assertEqual(left, [])

    def test_no_logos_zero_in_docs(self):
        """Quyết định 40 (21/11/2026): site không còn chữ "Logos Zero" hay anchor `logos-zero`, trừ mã JS nhận bản
        sao lưu cũ (khóa "logos-zero" ở merge.js, progress.js, sw.js)."""
        out = subprocess.run(["git", "grep", "-l", "-i", "-e", "logos zero", "-e", "logos-zero", "--", "docs"],
                             cwd=ROOT, capture_output=True, text=True).stdout.split()
        left = [f for f in out if f not in {"docs/assets/js/merge.js", "docs/assets/js/progress.js", "docs/sw.js"}]
        self.assertEqual(left, [])


if __name__ == "__main__":
    unittest.main()
