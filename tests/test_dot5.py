"""Script đợt 5 (ban-giao/dot-5.md). Chạy: python -m unittest discover -s tests"""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "migrate"))

import dot5_ten  # noqa: E402

# Chỗ được giữ "Logos Zero" (quyết định 27): nói tới site song song logos-zero, hoặc lịch sử dự án.
GIU = {"KE-HOACH.md", "README.md", "pyproject.toml", "AGENTS.md", "tests/test_parity.py", "tests/test_dot5.py",
       "docs/assets/js/merge.js", "tools/migrate/dot5_ten.py"}


class TestTenSite(unittest.TestCase):
    def test_no_old_name_outside_allowed_files(self):
        out = subprocess.run(["git", "grep", "-l", "Logos Zero"], cwd=ROOT, capture_output=True, text=True).stdout.split()
        left = [f for f in out if f not in GIU and not f.startswith(("ban-giao/", "verification/"))]
        self.assertEqual(left, [])

    def test_script_is_idempotent(self):
        for f in dot5_ten.targets():
            text = (ROOT / f).read_text(encoding="utf-8")
            self.assertEqual(dot5_ten.convert(f, text), (text, 0), f)

    def test_special_text_is_not_rewritten(self):
        src = 'error: "Đây không phải bản sao lưu của Logos Zero." }; /* Logos Zero */'
        out, n = dot5_ten.convert("docs/assets/js/merge.js", src)
        self.assertEqual(out, 'error: "Đây không phải bản sao lưu của Logos hay Logos Zero." }; /* Logos */')
        self.assertEqual(n, 2)

    def test_old_anchors_kept(self):
        self.assertIn("## Logos là gì {#logos-zero-la-gi}", (ROOT / "docs/index.md").read_text(encoding="utf-8"))
        self.assertIn("{#doc-logos-zero-the-nao}", (ROOT / "docs/bat-dau/index.md").read_text(encoding="utf-8"))
        self.assertIn("## Đọc thêm trên Logos {#doc-them-tren-logos-zero}",
                      (ROOT / "docs/triet-gia/kant.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
