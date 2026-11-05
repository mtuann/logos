"""tools/kb_sources.py: rút kho nguồn từ mục Nguồn. Chạy: python -m unittest discover -s tests"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import kb_sources as ks  # noqa: E402


class TestClassify(unittest.TestCase):
    def test_keys(self):
        cases = {
            "https://plato.stanford.edu/entries/knowledge-analysis/": ("sep", "sep.knowledge-analysis"),
            "https://plato.stanford.edu/archives/fall2026/entries/kant/": ("sep", "sep.kant"),
            "https://iep.utm.edu/thales/": ("iep", "iep.thales"),
            "https://www.gutenberg.org/cache/epub/5827/pg5827.txt": ("gutenberg", "gutenberg.5827"),
            "https://www.gutenberg.org/ebooks/5827": ("gutenberg", "gutenberg.5827"),
            "https://doi.org/10.1093/analys/23.6.121": ("doi", "doi.10-1093-analys-23-6-121"),
            "https://ctext.org/mengzi/gong-sun-chou-i": ("ctext", "ctext.mengzi-gong-sun-chou-i"),
            "https://en.wikisource.org/wiki/Leviathan": ("wikisource", "wikisource.en.leviathan"),
            "https://survey2020.philpeople.org/survey/results/all": ("khac", "web.survey2020-philpeople-org.survey-results-all"),
        }
        for url, want in cases.items():
            self.assertEqual(ks.classify(url, ""), want, url)
        self.assertEqual(ks.classify(None, "Nguyễn Tài Thư (1993), *Lịch sử tư tưởng Việt Nam*"),
                         ("sach", "sach.nguyen-tai-thu-1993-lich-su-tu-tuong-viet-nam"))

    def test_norm_url(self):
        self.assertEqual(ks.norm_url("http://www.Gutenberg.org/ebooks/5827/#x"), "https://gutenberg.org/ebooks/5827")

    def test_urls_of(self):
        t = "A <https://a.org/x> (văn bản: <https://a.org/y.txt>), [B](https://b.org/z) và https://c.org/w."
        self.assertEqual(ks.urls_of(t), ["https://a.org/x", "https://a.org/y.txt", "https://b.org/z", "https://c.org/w."])


class TestRepo(unittest.TestCase):
    def test_every_item_maps_to_a_record(self):
        recs, stats = ks.extract(ROOT)
        used = {u for r in recs.values() for u in r["used_in"]}
        for where, _ in list(ks.page_items(ROOT)) + list(ks.profile_items(ROOT)):
            self.assertIn(where, used)
        self.assertEqual(stats["items"], sum(1 for _ in ks.page_items(ROOT)) + sum(1 for _ in ks.profile_items(ROOT)))

    def test_file_is_current(self):
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ks.main(["--check"]), 0)

    def test_kept_fields_survive(self):
        recs, _ = ks.extract(ROOT)
        key = next(iter(recs))
        merged = ks.merge_kept({key: dict(recs[key])}, {key: {"archive": "https://x.org/", "accessed": "2026-11-05"}})
        self.assertEqual(merged[key]["archive"], "https://x.org/")
        self.assertIn("archive: https://x.org/", ks.render(merged))


if __name__ == "__main__":
    unittest.main()
