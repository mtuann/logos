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

    def test_word_count_not_year(self):
        """Số chữ gợi ý cho bài viết không phải năm (đợt 5.2: rút nhầm 300, 200, 350 ở mục Tự viết)."""
        for s in ("Gợi ý độ dài: 150–300 chữ.", "Gợi ý độ dài: 200–350 chữ.", "Viết 250–400 chữ.",
                  "bản chữ Hán thông dụng chỉ có 260 chữ, kể cả câu chú", "khoảng 300 - 500 chữ"):
            self.assertEqual([m.group(0) for m in ke.YEAR.finditer(s)], [], s)
        # Năm thật vẫn được rút, kể cả khi chữ "chữ" đứng sau ở chỗ khác trong câu.
        ys = [m.group(0) for m in ke.YEAR.finditer("Năm 1919 có khoa thi cuối; bài phú 300 chữ viết năm 1300.")]
        self.assertEqual(ys, ["1919", "1300"])
        self.assertEqual([m.group(0) for m in ke.YEAR.finditer("khoảng năm 1930: sáng đọc Khổng Tử")], ["1930"])

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
        self.assertEqual([k for k, r in recs.items() if r["text"].startswith("Gợi ý độ dài")], [])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ke.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
