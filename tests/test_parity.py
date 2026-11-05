"""tools/parity.py: trích văn bản hiển thị và so hai bản build. Chạy: python -m unittest discover -s tests"""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import parity  # noqa: E402

PAGE = """<!doctype html><html><head><title>Tri thức - Logos Zero</title>
<meta name="description" content="Mô tả &amp; tóm tắt"></head><body>
<nav>Thanh điều hướng</nav>
<article class="md-content__inner md-typeset">
<h1 id="tri-thuc">Tri   thức</h1>
<p>Năm <em>1641</em>, Descartes.<script>var x = "không hiện";</script></p>
<h2 id="nguon">Nguồn<a class="headerlink" href="#nguon">#</a></h2>
<ul><li>SEP</li></ul>
</article>
<footer>Chân trang</footer></body></html>"""


def site(files: dict[str, str]) -> Path:
    d = Path(tempfile.mkdtemp(prefix="parity-test-"))
    for rel, text in files.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(text, encoding="utf-8")
    return d


class TestExtract(unittest.TestCase):
    def test_visible_text_only(self):
        t = parity.extract(PAGE)
        self.assertEqual(t.title, "Tri thức - Logos Zero")
        self.assertEqual(t.description, "Mô tả & tóm tắt")
        self.assertEqual(t.lines, ("Tri thức", "Năm 1641, Descartes.", "Nguồn#", "SEP"))
        self.assertEqual(t.ids, ("tri-thuc", "nguon"))

    def test_markup_change_is_invisible(self):
        a = parity.extract(PAGE)
        b = parity.extract(PAGE.replace("<em>1641</em>", "<strong>1641</strong>"))
        self.assertEqual(a, b)


class TestCompare(unittest.TestCase):
    def test_identical(self):
        problems, n = parity.compare(site({"a/index.html": PAGE}), site({"a/index.html": PAGE}))
        self.assertEqual((problems, n), ([], 1))

    def test_detects_text_title_description_ids_and_missing_pages(self):
        changed = (PAGE.replace("1641", "1642").replace("Tri thức -", "Tri thức mới -")
                   .replace("Mô tả", "Mô tả khác").replace('id="nguon"', 'id="nguon-1"'))
        problems, n = parity.compare(site({"a/index.html": PAGE, "b/index.html": PAGE}),
                                     site({"a/index.html": changed, "c/index.html": PAGE}))
        text = "\n".join(problems)
        self.assertEqual(n, 3)
        for needle in ("b/index.html: chỉ có ở bản trước", "c/index.html: chỉ có ở bản sau",
                       "<title> lệch", "description lệch", "văn bản hiển thị lệch", "-Năm 1641", "+Năm 1642",
                       "id lệch (mất ['nguon'], thêm ['nguon-1']"):
            self.assertIn(needle, text)

    def test_search_index(self):
        idx = lambda text: '{"config": {}, "docs": [{"location": "a/", "title": "T", "text": "%s"}]}' % text
        same, _ = parity.compare(site({"search/search_index.json": idx("x")}), site({"search/search_index.json": idx("x")}))
        self.assertEqual(same, [])
        diff, _ = parity.compare(site({"search/search_index.json": idx("x")}), site({"search/search_index.json": idx("y")}))
        self.assertEqual(diff, ["search_index.json lệch: 1 mục, ví dụ ['a/']"])

    def test_expected_substitution(self):
        import re
        a, b = site({"x.html": PAGE}), site({"x.html": PAGE.replace("SEP", "SEP (bản lưu)")})
        self.assertNotEqual(parity.compare(a, b)[0], [])
        self.assertEqual(parity.compare(a, b, [(re.compile(r"\bSEP\b"), "SEP (bản lưu)")])[0], [])

    def test_generated_ui_ignored(self):
        ui = PAGE.replace('<h1 id="tri-thuc">', '<div class="oz-info" data-oz-sinh><span>Lõi</span> · <b id="x">chưa kiểm</b><br>'
                          '<img src="a.png" data-oz-sinh></div><h1 id="tri-thuc">')
        self.assertEqual(parity.extract(ui), parity.extract(PAGE))
        moved = PAGE.replace("<p>Năm", '<div class="oz-thoi-su"><p data-oz-sinh>Có hạn dùng</p><p>Năm').replace("</p>\n<h2", "</p></div>\n<h2")
        self.assertEqual(parity.extract(moved).lines, parity.extract(PAGE).lines)

    def test_exempt_and_new_pages(self):
        a = site({"index.html": PAGE, "x/index.html": PAGE})
        b = site({"index.html": PAGE.replace("Descartes", "Kant"), "x/index.html": PAGE, "moi/index.html": PAGE})
        problems, _ = parity.compare(a, b)
        self.assertEqual(len(problems), 2)
        notes = []
        problems, _ = parity.compare(a, b, exempt=["index.html"], new_ok=["moi/*"], notes=notes)
        self.assertEqual(problems, [])
        self.assertEqual(len(notes), 2)
        self.assertIn("ngoại lệ", notes[1] if "ngoại lệ" in notes[1] else notes[0])

    def test_cli_exit_codes(self):
        a, b = site({"x.html": PAGE}), site({"x.html": PAGE.replace("SEP", "IEP")})
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(parity.main([str(a), str(a)]), 0)
            self.assertEqual(parity.main([str(a), str(b)]), 1)
        self.assertIn("giống 100%", out.getvalue())
        self.assertIn("LỆCH", out.getvalue())


if __name__ == "__main__":
    unittest.main()
