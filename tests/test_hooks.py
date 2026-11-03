"""Kiểm thử các hook MkDocs và script sinh trang. Chạy: python -m unittest discover -s tests"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "hooks"), str(ROOT / "tools")]

import gen_glossary  # noqa: E402
import search_vi  # noqa: E402
import slugs  # noqa: E402


class TestSearchVi(unittest.TestCase):
    def test_strip_accents(self):
        self.assertEqual(search_vi.strip_accents("Đạo đức học"), "Dao duc hoc")
        self.assertEqual(search_vi.strip_accents("Tương thích luận"), "Tuong thich luan")
        self.assertEqual(search_vi.strip_accents("abc"), "abc")

    def test_augment_keeps_title(self):
        doc = {"location": "x/", "title": "Tâm trí", "text": "<p>Ý thức</p>"}
        out = search_vi.augment(doc)
        # Phần hiển thị giữ nguyên; bản không dấu chỉ nằm trong thẻ ẩn để trường title
        # (được nhân trọng số) cũng khớp khi gõ không dấu.
        self.assertEqual(out["title"], 'Tâm trí<span hidden class="oz-noaccent"> Tam tri</span>')
        self.assertIn("Tam tri Tam tri Tam tri", out["text"])
        self.assertIn("Y thuc", out["text"])
        self.assertTrue(out["text"].startswith("<p>Ý thức</p>"))

    def test_augment_ascii_untouched(self):
        doc = {"location": "x/", "title": "Gettier", "text": "abc"}
        self.assertEqual(search_vi.augment(doc), doc)

    def test_strip_summaries(self):
        doc = {
            "location": "x/",
            "title": "T",
            "text": '<p>Mở đầu</p><p>Tóm tắt 5 phút</p> <ul> <li>tri thức tri thức</li> </ul><p>Thân bài</p>',
        }
        out = search_vi.strip_summaries(doc)
        self.assertNotIn("Tóm tắt 5 phút", out["text"])
        self.assertNotIn("tri thức tri thức", out["text"])
        self.assertIn("Mở đầu", out["text"])
        self.assertIn("Thân bài", out["text"])

    def test_strip_summaries_noop(self):
        doc = {"location": "x/", "title": "T", "text": "<p>Không có box</p>"}
        self.assertEqual(search_vi.strip_summaries(doc), doc)


class TestSlugs(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugs.slugify("Đọc văn bản gốc"), "doc-van-ban-goc")
        self.assertEqual(slugs.slugify("Câu hỏi thật sự là gì?"), "cau-hoi-that-su-la-gi")
        self.assertEqual(slugs.slugify("Thử ngay: Con tàu của Theseus"), "thu-ngay-con-tau-cua-theseus")


class TestGlossary(unittest.TestCase):
    def test_sort_vietnamese_alphabet(self):
        words = ["đạo", "dài", "ăn", "an", "âm", "ơn", "ôn", "ong", "ưu", "uống"]
        got = [t["vi"] for t in sorted(({"vi": w} for w in words), key=gen_glossary.sort_key)]
        self.assertEqual(got, ["an", "ăn", "âm", "dài", "đạo", "ong", "ôn", "ơn", "uống", "ưu"])

    def test_page_in_sync(self):
        self.assertEqual(gen_glossary.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
