"""tools/kb_philpapers.py: JSON ↔ tools/philpapers-2020.md. Chạy: python -m unittest discover -s tests"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import kb_philpapers as kp  # noqa: E402


class TestPhilPapers(unittest.TestCase):
    def test_md_is_rendered_from_json(self):
        data = json.loads(kp.JSON.read_text(encoding="utf-8"))
        self.assertEqual(kp.render_md(data), kp.MD.read_text(encoding="utf-8"))

    def test_parse_render_round_trip(self):
        md = kp.MD.read_text(encoding="utf-8")
        self.assertEqual(kp.render_md(kp.parse_md(md)), md)

    def test_values(self):
        data = json.loads(kp.JSON.read_text(encoding="utf-8"))
        q = {q["id"]: q for q in data["questions"]}
        fw = q["tu-do-y-chi"]
        self.assertEqual((fw["table"], fw["n"]), (1, 1760))
        self.assertEqual({o["id"]: o["pct"] for o in fw["options"]}["tuong-thich-luan"], 59.2)
        self.assertEqual(len(data["questions"]), 87)

    def test_formatting(self):
        self.assertEqual(kp.fmt(18.0), "18,0")
        self.assertEqual(kp.fmt_n(1760), "1.760")
        self.assertEqual(kp.cell({"pct": 9.0, "raw": {"pct": "9"}}, "pct"), "9")


if __name__ == "__main__":
    unittest.main()
