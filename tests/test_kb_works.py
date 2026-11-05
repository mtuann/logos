"""tools/kb_works.py: rút kho tác phẩm. Chạy: python -m unittest discover -s tests"""

import contextlib
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import kb_works as kw  # noqa: E402


class TestKbWorks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recs = kw.extract(ROOT)

    def test_stephanus_is_not_a_year(self):
        self.assertIsNone(kw.WORK_YEAR.search("*Cộng hòa* (519a–520a)"))

    def test_patterns(self):
        m = kw.WORK_YEAR.search("trong *Cộng hòa* (k. 375 TCN) và *Suy niệm* (1641)")
        self.assertEqual((m.group(1), kw.year_of(m.group(2), m.group(3))), ("Cộng hòa", -375))
        self.assertEqual(kw.YEAR.match("1951, bản 6").group(1), "1951")
        self.assertIsNone(kw.YEAR.match("thế kỷ 5 TCN"))

    def test_profile_author_only_when_title_leads(self):
        r = self.recs["kant.kritik-der-reinen-vernunft"]
        self.assertEqual((r["author"], r["year"]), ("kant", 1781))
        herodotus = [k for k, r in self.recs.items() if r.get("author_name") == "Herodotus"]
        self.assertTrue(herodotus)
        self.assertTrue(all(k.startswith("chua-ro.") and self.recs[k]["author"] is None for k in herodotus))

    def test_prose_count_matches_baseline(self):
        """158 chỗ *Tác phẩm* (năm) trong Lõi viết tay: báo cáo nền đếm 159, gồm 1 chỗ là số trang Stephanus (*Cộng hòa* (519a…))."""
        n = sum(1 for _, _, where in kw.prose_mentions(ROOT) if not where.startswith("people/"))
        self.assertEqual(n, 158)

    def test_year_null_when_conflicting(self):
        for r in self.recs.values():
            if len(r["years_seen"]) == 1:
                self.assertEqual(r["year"], int(next(iter(r["years_seen"]))))
            else:
                self.assertIsNone(r["year"])

    def test_file_is_current(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(kw.main(["--check"]), 0)


class TestKeptFields(unittest.TestCase):
    def test_curated_fields_survive_reextraction(self):
        """Đợt 5.1: attribution, year_note do người kiểm ghi, tool giữ khi rút lại."""
        recs = {"chua-ro.x": {"author": None, "titles": ["X"], "year": None}}
        old = {"chua-ro.x": {"attribution": "Aldo Leopold", "year_note": "bản gốc 1949", "used_in": ["cu"]}}
        out = kw.merge_kept(recs, old)["chua-ro.x"]
        self.assertEqual((out["attribution"], out["year_note"]), ("Aldo Leopold", "bản gốc 1949"))
        self.assertNotIn("used_in", out)
        self.assertIn("attribution:", kw.render({"chua-ro.x": {**out, "years_seen": {}, "used_in": [], "evidence": [],
                                                               "verified": None}}))


if __name__ == "__main__":
    unittest.main()
