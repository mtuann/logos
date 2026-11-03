"""Kiểm thử tools/review_check.py. Chạy: python -m unittest discover -s tests"""

import sys
import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "tools")]

import review_check  # noqa: E402


class TestPageMeta(unittest.TestCase):
    def _write(self, tmp, name, body):
        p = Path(tmp) / name
        p.write_text(body, encoding="utf-8")
        return p

    def test_reads_title_and_date(self):
        with TemporaryDirectory() as tmp:
            p = self._write(tmp, "a.md", "---\ntitle: Bài kiểm tra\nupdated: 2026-05-01\n---\n\nNội dung.\n")
            title, updated = review_check.page_meta(p)
            self.assertEqual(title, "Bài kiểm tra")
            self.assertEqual(updated, date(2026, 5, 1))

    def test_missing_date_returns_none(self):
        with TemporaryDirectory() as tmp:
            p = self._write(tmp, "b.md", "---\ntitle: Không ngày\n---\n\nNội dung.\n")
            title, updated = review_check.page_meta(p)
            self.assertEqual(title, "Không ngày")
            self.assertIsNone(updated)

    def test_no_front_matter_falls_back_to_stem(self):
        with TemporaryDirectory() as tmp:
            p = self._write(tmp, "c.md", "Không có front matter.\n")
            title, updated = review_check.page_meta(p)
            self.assertEqual(title, "c")
            self.assertIsNone(updated)


class TestCollect(unittest.TestCase):
    def test_stale_threshold(self):
        # Dùng monkeypatch nhẹ: gọi collect với today giả định trên dữ liệu thật
        # thì mọi bài đều tươi (đều updated 2026-10-13, today 2026-10-13).
        fresh, stale = review_check.collect(date(2026, 10, 13))
        self.assertEqual(stale, [])
        self.assertGreater(len(fresh), 40)

    def test_old_date_becomes_stale(self):
        fresh, stale = review_check.collect(date(2028, 10, 13))
        self.assertGreater(len(stale), 40)
        self.assertEqual(fresh, [])

    def test_render_lists_stale(self):
        out = review_check.render(date(2028, 1, 1))
        self.assertIn("cần rà soát lại", out)
        self.assertIn("cập nhật lần cuối", out)

    def test_render_clean_when_fresh(self):
        out = review_check.render(date(2026, 10, 13))
        self.assertIn("Không có bài nào quá hạn rà soát.", out)


if __name__ == "__main__":
    unittest.main()
