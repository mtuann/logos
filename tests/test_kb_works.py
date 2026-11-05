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
        """159 chỗ *Tác phẩm* (năm) trong Lõi viết tay (verification/bao-cao-nen.md)."""
        n = sum(1 for _, _, where in kw.prose_mentions(ROOT) if not where.startswith("people/"))
        self.assertEqual(n, 159)

    def test_year_null_when_conflicting(self):
        for r in self.recs.values():
            if len(r["years_seen"]) == 1:
                self.assertEqual(r["year"], int(next(iter(r["years_seen"]))))
            else:
                self.assertIsNone(r["year"])

    def test_file_is_current(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(kw.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
