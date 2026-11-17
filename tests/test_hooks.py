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
        cls.reg = kb.load_context(ROOT)

    def test_counts_match_registry(self):
        expect = {"cau-hoi": "57", "cong-cu": "15", "lich-su": "8", "doc": "19", "triet-gia": "59",
                  "bat-dau": "1", "cau-hoi/dao-duc": "7", "cau-hoi/viet-nam": "3",
                  "nguy-bien": "100", "thuat-ngu": "249", "quiz": "433"}
        for key, n in expect.items():
            self.assertEqual(kb.expand(f"[[count:{key}]]", self.reg), n, key)

    def test_philpapers(self):
        want = {"tu-do-y-chi.tuong-thich-luan": "59,2", "tu-do-y-chi/n": "1.760",
                "khao-sat/nguoi-tra-loi": "1.785", "khao-sat/so-cau": "100", "khao-sat/cau-chinh": "40",
                "chan-ly.thuyet-tuong-ung-correspondence/loai-tru": "48,3"}
        for key, v in want.items():
            self.assertEqual(kb.expand(f"[[pp:{key}]]", self.reg), v, key)
        for bad in ("[[pp:khong-co.x]]", "[[pp:tu-do-y-chi.khong-co]]", "[[pp:tu-do-y-chi]]",
                    "[[pp:tu-do-y-chi.khac/loai-tru]]", "[[pp:khao-sat/x]]", "[[pp:tu-do-y-chi.khac/sai]]"):
            with self.assertRaises(kb.PluginError, msg=bad):
                kb.expand(bad, self.reg, "x.md")

    def test_code_untouched(self):
        src = "Có [[count:cau-hoi]] bài; `[[count:x]]`.\n\n```text\n[[count:y]]\n```\n"
        self.assertEqual(kb.expand(src, self.reg), "Có 57 bài; `[[count:x]]`.\n\n```text\n[[count:y]]\n```\n")

    def test_json_assets(self):
        """Chuỗi trong JSON_ASSETS mở được shortcode (build xong mới mở; khóa sai thì dừng như trong trang)."""
        import json
        nested = {"a": ["[[pp:tu-do-y-chi.tuong-thich-luan]]%", {"b": "[[count:cau-hoi]] bài"}], "n": 3}
        self.assertEqual(kb.expand_json(nested, self.reg), {"a": ["59,2%", {"b": "57 bài"}], "n": 3})
        for rel in kb.JSON_ASSETS:
            data = json.loads((ROOT / "docs" / rel).read_text(encoding="utf-8"))
            out = json.dumps(kb.expand_json(data, self.reg, rel), ensure_ascii=False)
            self.assertNotIn("[[", out, rel)

    def test_unknown_kind_or_key_stops_build(self):
        for bad in ("[[count:khong-co]]", "[[count:cau-hoi/khong-co]]", "[[fact:kant]]", "[[count:he-thong]]",
                    "[[count:quiz/cong-cu]]"):
            with self.assertRaises(kb.PluginError, msg=bad) as cm:
                kb.expand(bad, self.reg, "x.md")
            self.assertIn("x.md: shortcode", str(cm.exception))

    def test_not_a_shortcode(self):
        for s in ("[[Count:cau-hoi]]", "[[count: cau-hoi]]", "[ [count:cau-hoi]]", "[[count]]"):
            self.assertEqual(kb.expand(s, self.reg), s)

    def test_thousands(self):
        self.assertEqual(kb.fmt_int(1234567), "1.234.567")


class TestInfoStrip(unittest.TestCase):
    """hooks/kb.py: dải thông tin và nhãn Mới (đợt 4.6–4.7)."""

    def test_strip(self):
        import datetime
        ctx = {"pages": {"a.md": {"tier": "loi"}, "b.md": {"tier": "he-thong"}, "c.md": {"tier": "mo-rong"}},
               "ledger": {"a.md#x": {"status": "frozen"}, "a.md#y": {"status": "chua-kiem"}}}
        html = "<h1>T</h1><h2 id='x'>X</h2><h2 id='y'>Y</h2>"
        s = kb.info_strip("a.md", ["Câu hỏi lớn", "Tri thức"], datetime.date(2026, 10, 22), html, ctx)
        self.assertIn("data-oz-sinh", s)
        self.assertIn("data-search-exclude", s)
        self.assertIn("Câu hỏi lớn › Tri thức", s)
        self.assertIn("Cập nhật 22/10/2026", s)
        self.assertIn("Đã kiểm chứng 1/3 mục", s)
        self.assertIsNone(kb.info_strip("b.md", [], None, html, ctx))
        self.assertIn("Chưa kiểm chứng", kb.info_strip("c.md", [], None, html, ctx))
        self.assertIn(">Mới<", kb.info_strip("c.md", [], None, html, ctx, new=True))

    def test_is_new(self):
        import datetime
        d = datetime.date(2027, 5, 1)
        self.assertTrue(kb.is_new({"tier": "mo-rong"}, {"added": "2027-04-01"}, d))
        self.assertFalse(kb.is_new({"tier": "mo-rong"}, {"added": "2027-01-01"}, d))
        self.assertFalse(kb.is_new({"tier": "loi"}, {"added": "2027-04-01"}, d))
        self.assertFalse(kb.is_new({"tier": "mo-rong"}, {}, d))


class TestThoiSuShortcode(unittest.TestCase):
    """hooks/kb.py: [[thoi-su:id]] chèn nguyên văn thân khối data/thoi-su/<id>.md (ban-giao/dot-3.md)."""

    @classmethod
    def setUpClass(cls):
        import tempfile
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        d = root / "data" / "thoi-su"
        d.mkdir(parents=True)
        fm = "---\npage: a/b.md\nupdated_to: 2026-10-22\nreview_by: 2027-10-22\nsources: []\n---\n"
        (d / "a.b.mot-dong.md").write_text(fm + "**hơn 200 người** (số liệu [[count:x]])\n", encoding="utf-8")
        (d / "a.b.nhieu-dong.md").write_text(fm + "Dòng một.\n\nDòng ba [link](c.md).\n", encoding="utf-8")
        cls.blocks = kb.load_thoi_su(root)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_inline(self):
        got = kb.expand_thoi_su("Có [[thoi-su:a.b.mot-dong]] bị kết án.", self.blocks, "a/b.md", wrap=False)
        self.assertEqual(got, "Có **hơn 200 người** (số liệu [[count:x]]) bị kết án.")

    def test_block_keeps_indent(self):
        src = "- mục\n\n    [[thoi-su:a.b.nhieu-dong]]\n\nSau."
        got = kb.expand_thoi_su(src, self.blocks, "a/b.md", wrap=False)
        self.assertEqual(got, "- mục\n\n    Dòng một.\n\n    Dòng ba [link](c.md).\n\nSau.")

    def test_wrap_inline_and_block(self):
        import datetime
        got = kb.expand_thoi_su("Có [[thoi-su:a.b.mot-dong]] bị.", self.blocks, "a/b.md", today=datetime.date(2027, 1, 1))
        self.assertEqual(got, 'Có <span class="oz-ts">**hơn 200 người** (số liệu [[count:x]])<span class="oz-ts-nhan" '
                              'data-oz-sinh data-search-exclude> thời sự · đúng tới 22/10/2026</span></span> bị.')
        late = kb.expand_thoi_su("[[thoi-su:a.b.mot-dong]]", self.blocks, "a/b.md", today=datetime.date(2027, 10, 23))
        self.assertIn('class="oz-ts oz-ts--qua-han"', late)
        self.assertIn("cần rà lại", late)
        block = kb.expand_thoi_su("- mục\n\n    [[thoi-su:a.b.nhieu-dong]]\n", self.blocks, "a/b.md",
                                  today=datetime.date(2027, 1, 1))
        self.assertEqual(block.split("\n")[2:9], [
            '    <div class="oz-ts oz-ts-khoi" markdown>', "",
            '    <p class="oz-ts-nhan" data-oz-sinh data-search-exclude>thời sự · đúng tới 22/10/2026</p>', "",
            "    Dòng một.", "", "    Dòng ba [link](c.md)."])

    def test_block_must_stand_alone(self):
        with self.assertRaises(kb.PluginError):
            kb.expand_thoi_su("Chữ [[thoi-su:a.b.nhieu-dong]]", self.blocks, "a/b.md")

    def test_wrong_page_or_missing(self):
        for src, where in (("[[thoi-su:a.b.mot-dong]]", "x.md"), ("[[thoi-su:khong-co]]", "a/b.md")):
            with self.assertRaises(kb.PluginError, msg=src):
                kb.expand_thoi_su(src, self.blocks, where)

    def test_code_untouched(self):
        src = "`[[thoi-su:khong-co]]`\n\n```\n[[thoi-su:khong-co]]\n```\n"
        self.assertEqual(kb.expand_thoi_su(src, self.blocks, "a/b.md"), src)

    def test_expand_opens_thoi_su_first(self):
        ctx = dict(kb.load_context(ROOT), thoi_su=self.blocks)
        with self.assertRaises(kb.PluginError) as cm:   # [[count:x]] trong thân khối cũng được mở (và sai)
            kb.expand("[[thoi-su:a.b.mot-dong]]", ctx, "a/b.md")
        self.assertIn("[[count:x]]", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
