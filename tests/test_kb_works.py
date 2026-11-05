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
        """157 chỗ *Tác phẩm* (năm) trong Lõi viết tay: báo cáo nền đếm 159, gồm 1 chỗ là số trang Stephanus
        (*Cộng hòa* (519a…)) và 1 chỗ "(100 nhà sản xuất…)" (đợt 5.1, không phải năm)."""
        n = sum(1 for _, _, where in kw.prose_mentions(ROOT) if not where.startswith("people/"))
        self.assertEqual(n, 157)

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



class TestExtractionFixes(unittest.TestCase):
    """Đợt 5.1: lỗi trình rút do agent kiểm tìm ra."""

    def test_number_followed_by_words_is_not_a_year(self):
        line = "*CDP Carbon Majors Report 2017* (100 nhà sản xuất nhiên liệu hóa thạch)"
        self.assertEqual(kw.WORK_YEAR.findall(line), [])
        self.assertEqual(kw.WORK_YEAR.findall("*Confessiones* (397), rồi *De civitate Dei* (413–426)"),
                         [("Confessiones", "397", ""), ("De civitate Dei", "413", "")])
        self.assertEqual(kw.WORK_YEAR.findall("*Nephelai* (423 TCN)"), [("Nephelai", "423", " TCN")])

    def test_own_titles_belong_to_profile_owner(self):
        recs = kw.extract()
        self.assertIn("averroes.chu-giai-lon-ve-de-anima-cua-aristotle", recs)
        self.assertEqual(recs["averroes.chu-giai-lon-ve-de-anima-cua-aristotle"]["year"], 1186)
        self.assertEqual(recs["tran-duc-thao.la-phenomenologie-de-lesprit-et-son-contenu-reel"]["titles"],
                         ["La Phénoménologie de l’esprit et son contenu réel"])
        self.assertFalse(any(r.get("author_name") in ("Chú giải lớn về", "“La") for r in recs.values()))

    def test_year_fixed_and_same_as_kept(self):
        """Đợt 5.1: year_fixed thay year; same_as, years_ok giữ khi rút lại; tác phẩm đã chốt không vào danh sách lệch."""
        recs = {"mill.u": {"author": "mill", "titles": ["U"], "year": None, "years_seen": {"1861": ["a"], "1863": ["b"]},
                           "used_in": ["a", "b"], "evidence": [], "verified": None}}
        old = {"mill.u": {"year_fixed": 1861, "years_ok": [1863], "same_as": "mill.x"}}
        r = kw.merge_kept(recs, old)["mill.u"]
        self.assertEqual((r["year"], r["years_ok"], r["same_as"]), (1861, [1863], "mill.x"))
        self.assertIn("0 tác phẩm gặp với hơn một năm", kw.render_lech(recs))

    def test_repo_works_all_attributed(self):
        works = kw.extract()
        import yaml
        cur = yaml.safe_load(kw.OUT.read_text(encoding="utf-8"))
        self.assertTrue(all(r.get("author") or r.get("attribution") or r.get("same_as") for r in cur.values()))
        self.assertTrue(all(cur[r["same_as"]] for r in cur.values() if r.get("same_as")))
        self.assertEqual(set(works), set(cur))

if __name__ == "__main__":
    unittest.main()
