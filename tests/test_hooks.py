"""Kiểm thử các hook MkDocs và script sinh trang. Chạy: python -m unittest discover -s tests"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "hooks"), str(ROOT / "tools")]

import gen_glossary  # noqa: E402
import kb  # noqa: E402
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



class TestKbShortcode(unittest.TestCase):
    """hooks/kb.py: shortcode [[count:…]] đọc content.yml; khóa sai thì build dừng."""

    @classmethod
    def setUpClass(cls):
        cls.reg = kb.load_registry(ROOT)

    def test_counts_match_registry(self):
        expect = {"cau-hoi": "57", "cong-cu": "15", "lich-su": "8", "doc": "19", "triet-gia": "59",
                  "bat-dau": "1", "cau-hoi/dao-duc": "7", "cau-hoi/viet-nam": "3"}
        for key, n in expect.items():
            self.assertEqual(kb.expand(f"[[count:{key}]]", self.reg), n, key)

    def test_code_untouched(self):
        src = "Có [[count:cau-hoi]] bài; `[[count:x]]`.\n\n```text\n[[count:y]]\n```\n"
        self.assertEqual(kb.expand(src, self.reg), "Có 57 bài; `[[count:x]]`.\n\n```text\n[[count:y]]\n```\n")

    def test_unknown_kind_or_key_stops_build(self):
        for bad in ("[[count:khong-co]]", "[[count:cau-hoi/khong-co]]", "[[fact:kant]]", "[[count:he-thong]]"):
            with self.assertRaises(kb.PluginError, msg=bad) as cm:
                kb.expand(bad, self.reg, "x.md")
            self.assertIn("x.md: shortcode", str(cm.exception))

    def test_not_a_shortcode(self):
        for s in ("[[Count:cau-hoi]]", "[[count: cau-hoi]]", "[ [count:cau-hoi]]", "[[count]]"):
            self.assertEqual(kb.expand(s, self.reg), s)

    def test_thousands(self):
        self.assertEqual(kb.fmt_int(1234567), "1.234.567")

if __name__ == "__main__":
    unittest.main()
