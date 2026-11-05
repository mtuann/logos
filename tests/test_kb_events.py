"""tools/kb_events.py: ứng viên sự kiện. Chạy: python -m unittest discover -s tests"""

import contextlib
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import kb_events as ke  # noqa: E402


class TestKbEvents(unittest.TestCase):
    def test_year_pattern(self):
        ys = [m.group(0) for m in ke.YEAR.finditer("năm 1075, khoảng 500 TCN, 1.785 người, 30% và trang 1258")]
        self.assertEqual(ys, ["1075", "500 TCN", "1258"])
        self.assertIsNone(ke.YEAR.search("1.785 triết gia"))

    def test_skip_spans(self):
        s = "Trần Nhân Tông (1258–1308) viết *Cư trần lạc đạo phú* (1300) và năm 1293 nhường ngôi."
        lives, works = ke.spans(ke.LIFESPAN, s), ke.spans(ke.WORK_YEAR, s)
        kept = [m.group(0) for m in ke.YEAR.finditer(s) if not ke.inside(m.start(), lives + works)]
        self.assertEqual(kept, ["1293"])

    def test_repo(self):
        recs, skipped = ke.extract(ROOT)
        self.assertGreater(len(recs), 50)
        self.assertTrue(all(k.split(".")[0] in ke.BLOCKS for k in recs))
        self.assertTrue(any(r["certainty"] == "chac-chan" for r in recs.values()))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ke.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
