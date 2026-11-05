"""Đợt 3 (ban-giao/dot-3.md): script dời và thay chữ bằng shortcode. Chạy: python -m unittest discover -s tests"""

import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "tools" / "migrate"), str(ROOT / "tools")]

import dot3_philpapers as pp  # noqa: E402
import dot3_so_dem  # noqa: E402
import dot3_thoi_su  # noqa: E402
import thay_shortcode  # noqa: E402


class TestDot3(unittest.TestCase):
    def test_norm_titles(self):
        self.assertEqual(pp.norm("Tự do ý chí (câu chính, n ≈ 1.760)"), "tự do ý chí")
        self.assertEqual(pp.norm("Án tử hình — câu bổ sung, n ≈ 1.120"), "án tử hình")
        self.assertEqual(pp.norm("Biện minh tri thức (*epistemic justification*)"), "biện minh tri thức")
        self.assertEqual(pp.norm("Phổ quát nội tại (kiểu [Aristotle](../triet-gia/aristotle.md))"), "phổ quát nội tại")

    def test_col_role(self):
        self.assertEqual([pp.col_role(h) for h in ("%", "% loại trừ", "Chấp nhận hoặc nghiêng về",
                                                     "Chỉ chọn lựa chọn này", "Lựa chọn")],
                         ["pct", "pct_exclusive", "pct", "pct_exclusive", None])

    def test_no_philpapers_cell_left_to_replace(self):
        """Ô số trong bảng PhilPapers mà khớp JSON từng chữ thì phải là shortcode (ô lệch: verification/lech/)."""
        import json
        qs = json.loads(pp.JSON.read_text(encoding="utf-8"))["questions"]
        left = []
        for p in pp.registry.load(ROOT).select(generated=False):
            if p.path == "them/cap-nhat.md":
                continue
            text = (pp.DOCS / p.path).read_text(encoding="utf-8")
            left += pp.plan_tables(p.path, text, qs, [], Counter()) + pp.plan_prose(p.path, text, Counter(), [])
        left += pp.plan_manual(qs, Counter())
        self.assertEqual([(s[0], s[1]) for s in left], [])

    def test_counts_and_thoi_su_done(self):
        # Theo nội dung, không theo số dòng (trang chủ đổi bố cục ở đợt 4.9): mọi chữ đã thay vẫn còn trong trang.
        for page, _, _, new in dot3_so_dem.SUBS:
            self.assertIn(new, (thay_shortcode.DOCS / page).read_text(encoding="utf-8"), page)
        self.assertEqual(dot3_thoi_su.main(["--dry-run"]), 0)


if __name__ == "__main__":
    unittest.main()
