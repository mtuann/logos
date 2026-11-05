"""Kiểm thử tools/book.py. Chạy: python -m unittest discover -s tests"""

import importlib.util
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_book_tool():
    spec = importlib.util.spec_from_file_location(
        "book_tool", os.path.join(ROOT, "tools", "book.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestBookCoverDate(unittest.TestCase):
    def test_check_ignores_cover_date(self):
        # Ngày bìa lấy từ mtime: git checkout không giữ mtime và múi giờ
        # máy dev khác CI, nên cùng nội dung có thể sinh hai ngày khác nhau.
        # --check phải bỏ qua dòng ngày, chỉ bắt lệch nội dung thật.
        book = load_book_tool()
        line = ("*Bản tổng hợp các bài viết của Logos Zero để in ra đọc. "
                "Nội dung cập nhật đến ngày 13/10/2026.*")
        other_day = line.replace("13/10/2026", "14/10/2026")
        self.assertEqual(book.normalize_cover_date(line),
                         book.normalize_cover_date(other_day))
        self.assertIn("<ngày>", book.normalize_cover_date(line))

    def test_cover_date_pattern_matches_rendered_book(self):
        # Regex phải khớp đúng dòng do render_book sinh ra.
        book = load_book_tool()
        rendered = book.render_book([], "13/10/2026", "", "2026-10-13")
        self.assertRegex(rendered, r"Nội dung cập nhật đến ngày 13/10/2026")
        self.assertNotRegex(book.normalize_cover_date(rendered), r"\d{2}/\d{2}/\d{4}")

    def test_updated_line_normalized(self):
        # Dòng updated: trong front matter cũng là "ngày sinh" (ngày chạy
        # generator), phải được chuẩn hóa trong --check để không vỡ CI.
        book = load_book_tool()
        a = book.render_book([], "13/10/2026", "", "2026-10-13")
        b = book.render_book([], "14/10/2026", "", "2026-10-14")
        self.assertNotEqual(a, b)  # ngày sinh thật sự khác nhau
        self.assertEqual(book.normalize_generated(a), book.normalize_generated(b))

    def test_check_catches_real_content_drift(self):
        # --check phải bắt được lệch nội dung thật, không chỉ lệch ngày.
        book = load_book_tool()
        base = book.render_book([], "13/10/2026", "", "2026-10-13")
        drifted = base.replace("Mỗi bài bắt đầu ở một trang mới.",
                               "Mỗi bài bắt đầu ở một trang mới. Thêm dòng này.")
        self.assertEqual(
            book.normalize_generated(base),
            book.normalize_generated(base.replace("13/10/2026", "14/10/2026")),
        )
        self.assertNotEqual(book.normalize_generated(base),
                            book.normalize_generated(drifted))


class TestNavParsing(unittest.TestCase):
    def test_book_covers_reading_sections_in_nav_order(self):
        # Sách phải quét đúng các mục đọc theo thứ tự nav, bỏ index.
        book = load_book_tool()
        sections = book.parse_nav(os.path.join(ROOT, "mkdocs.yml"))
        names = [s[0] for s in sections]
        self.assertEqual(names, ["Bắt đầu", "Công cụ tư duy", "Câu hỏi lớn",
                                 "Lịch sử", "Đọc văn bản"])
        rels = [rel for _, items in sections for _, _, rel in items]
        self.assertNotIn("them/sach.md", rels)
        self.assertFalse(any(r.endswith("/index.md") for r in rels))
        self.assertTrue(all(r.endswith(".md") for r in rels))



class TestBookHeadingIds(unittest.TestCase):
    def test_h2_ids_stripped(self):
        # "## Nguồn {#nguon}" của mọi bài sẽ trùng nhau trong sách gộp; chỉ H2 bị bỏ ID.
        book = load_book_tool()
        src = "## Nguồn {#nguon}\n### Người rơm {#straw-man}\n## A"
        self.assertEqual(book.H2_ID_RE.sub(r"\1", src), "## Nguồn\n### Người rơm {#straw-man}\n## A")

if __name__ == "__main__":
    unittest.main()
