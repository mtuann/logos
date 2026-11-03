"""Chỉ mục không được tụt lại so với nội dung. Chạy: python -m unittest discover -s tests

Trước 22/10/2026, trang Những câu hỏi lớn chỉ liệt kê 35/53 bài và trang Đọc
văn bản 11/19 hướng dẫn mà không kiểm thử nào phát hiện. Các kiểm thử dưới đây
bắt lỗi đó ngay khi thêm bài mới.
"""

import re
import unittest
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

# Mỗi mục: mọi bài trong thư mục phải có link từ index.md của chính thư mục đó.
SECTIONS = ["cong-cu", "cau-hoi", "lich-su", "doc", "luyen-tap"]
LINK = re.compile(r"\]\(([a-z0-9-]+\.md)(?:#[^)]*)?\)")


class TestSectionIndexes(unittest.TestCase):
    def test_every_page_is_listed_in_its_section_index(self):
        for section in SECTIONS:
            folder = DOCS / section
            index = (folder / "index.md").read_text(encoding="utf-8")
            listed = set(LINK.findall(index))
            pages = {p.name for p in folder.glob("*.md") if p.name != "index.md"}
            with self.subTest(section=section):
                self.assertEqual(sorted(pages - listed), [],
                                 f"{section}/index.md thiếu link tới các bài này")


class TestStudyPlanCatalog(unittest.TestCase):
    def test_catalog_paths_exist(self):
        js = (DOCS / "assets" / "js" / "ke-hoach.js").read_text(encoding="utf-8")
        paths = re.findall(r'path: "(/[a-z0-9/-]*)"', js)
        self.assertGreater(len(paths), 50)
        for path in paths:
            rel = path.strip("/")
            with self.subTest(path=path):
                self.assertTrue((DOCS / f"{rel}.md").is_file() or (DOCS / rel / "index.md").is_file(),
                                f"CATALOG trỏ tới trang không có: {path}")


@unittest.skipUnless(SITE.is_dir(), "cần build site trước (mkdocs build)")
class TestNoProseInCodeBlocks(unittest.TestCase):
    """Đoạn văn lỡ thụt 4 dấu cách ngoài admonition thành khối code một dòng dài,
    không xuống dòng (lỗi ở 26 bài trước 22/10/2026). Công cụ tư duy dùng khối code
    có chủ đích cho dạng chuẩn và sơ đồ ASCII nên không xét."""

    VIET = re.compile(r"[ạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹđ]")

    def test_no_vietnamese_prose_in_pre(self):
        for section in ("cau-hoi", "doc", "lich-su", "triet-gia", "bat-dau"):
            for page in sorted((SITE / section).rglob("index.html")):
                article = page.read_text(encoding="utf-8").split("<article", 1)[-1]
                for block in re.findall(r"<pre[^>]*>(.*?)</pre>", article, re.S):
                    text = unescape(re.sub(r"<[^>]+>", "", block))
                    if len(text) > 120 and self.VIET.search(text) and " " in text.strip():
                        with self.subTest(page=str(page.relative_to(SITE))):
                            self.fail(f"văn xuôi trong khối code: {text.strip()[:80]}…")


if __name__ == "__main__":
    unittest.main()
