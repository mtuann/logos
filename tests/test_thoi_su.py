"""Kiểm thử tools/thoi_su_check.py (ban-giao/dot-3.md việc 3.1). Chạy: python -m unittest discover -s tests"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "tools")]

import thoi_su_check  # noqa: E402

FM = "---\npage: {page}\nupdated_to: 2026-10-22\nreview_by: {due}\nsources: []\n---\n"


class TestThoiSuCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.docs = self.root / "docs"
        (self.docs / "cau-hoi").mkdir(parents=True)
        (self.root / "data" / "thoi-su").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def block(self, key, body, page="cau-hoi/a.md", due="2027-10-22"):
        (self.root / "data" / "thoi-su" / f"{key}.md").write_text(FM.format(page=page, due=due) + body + "\n",
                                                                  encoding="utf-8")

    def page(self, rel, text):
        (self.docs / rel).write_text(text, encoding="utf-8")

    def errs(self):
        return thoi_su_check.problems(self.root, self.docs)

    def test_ok(self):
        self.block("cau-hoi.a.luat", "Một dòng.")
        self.page("cau-hoi/a.md", "Trước [[thoi-su:cau-hoi.a.luat]] sau.\n")
        self.assertEqual(self.errs(), [])

    def test_unused_twice_or_elsewhere(self):
        self.block("cau-hoi.a.luat", "Một dòng.")
        self.page("cau-hoi/a.md", "Không dùng.\n")
        self.page("cau-hoi/b.md", "[[thoi-su:cau-hoi.a.luat]]\n")
        e = self.errs()
        self.assertTrue(any("dùng khối 0 lần" in x for x in e), e)
        self.assertTrue(any(x.startswith("cau-hoi/b.md: dùng khối") for x in e), e)
        self.page("cau-hoi/a.md", "[[thoi-su:cau-hoi.a.luat]] và [[thoi-su:cau-hoi.a.luat]]\n")
        self.assertTrue(any("dùng khối 2 lần" in x for x in self.errs()))

    def test_missing_block_and_code_ignored(self):
        self.page("cau-hoi/a.md", "[[thoi-su:cau-hoi.a.khong-co]]\n\n`[[thoi-su:cau-hoi.a.trong-code]]`\n")
        e = self.errs()
        self.assertEqual(len(e), 1, e)
        self.assertIn("không có khối", e[0])

    def test_bad_id_schema_dates_body(self):
        self.block("sai-id", "x")
        self.block("cau-hoi.a.som", "x", due="2020-01-01")
        self.block("cau-hoi.a.rong", "\nx")
        self.page("cau-hoi/a.md", "[[thoi-su:sai-id]] [[thoi-su:cau-hoi.a.som]]\n\n[[thoi-su:cau-hoi.a.rong]]\n")
        e = "\n".join(self.errs())
        self.assertIn("id phải dạng cau-hoi.a.", e)
        self.assertIn("review_by trước updated_to", e)
        self.assertIn("dòng trống hoặc thụt lề", e)
        (self.root / "data" / "thoi-su" / "cau-hoi.a.thua.md").write_text(
            "---\npage: cau-hoi/a.md\nupdated_to: 2026-10-22\nreview_by: 2027-10-22\nsources: []\nla: 1\n---\nx\n",
            encoding="utf-8")
        self.assertIn("Additional properties", "\n".join(self.errs()))

    def test_multiline_must_stand_alone(self):
        self.block("cau-hoi.a.dai", "Dòng một.\n\nDòng hai.")
        self.page("cau-hoi/a.md", "Chữ [[thoi-su:cau-hoi.a.dai]]\n")
        self.assertTrue(any("đứng riêng một dòng" in x for x in self.errs()))
        self.page("cau-hoi/a.md", "    [[thoi-su:cau-hoi.a.dai]]\n")
        self.assertEqual(self.errs(), [])


if __name__ == "__main__":
    unittest.main()
