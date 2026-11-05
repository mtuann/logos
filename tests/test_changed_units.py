"""tools/changed_units.py: liệt kê đơn vị đổi giữa hai phiên bản. Chạy: python -m unittest discover -s tests"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import changed_units as cu  # noqa: E402
from lz import hashing  # noqa: E402

REG = """version: 1
pages:
  - {path: cau-hoi/x.md, type: cau-hoi, tier: loi, block: tri-thuc, generated: false}
  - {path: them/y.md, type: he-thong, tier: he-thong, block: null, generated: false}
  - {path: triet-gia/kant.md, type: triet-gia, tier: loi, block: triet-gia, generated: true}
data:
  - {path: docs/assets/data/terms.json, kind: thuat-ngu, tier: loi, block: thuat-ngu, generated: false}
"""
X = "# X\n\nMở đầu.\n\n## A {#a}\n\nNăm 1641.\n\n## B {#b}\n\nChữ *b*.\n\n## C {#c}\n\nc\n"


class TestChangedUnits(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="changed-units-"))
        self.files = {"content.yml": REG, "docs/cau-hoi/x.md": X, "docs/them/y.md": "# Y\n",
                      "docs/triet-gia/kant.md": "# Kant\n", "docs/assets/data/terms.json": "[]",
                      "verification/ledger.json": "{}"}
        self.write(self.files)
        self.git("init", "-q", "-b", "main")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "rong")
        self.git("add", "-A")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "goc")
        self._root = cu.ROOT
        cu.ROOT = self.repo

    def tearDown(self):
        cu.ROOT = self._root
        shutil.rmtree(self.repo, ignore_errors=True)

    def git(self, *a):
        subprocess.run(["git", *a], cwd=self.repo, check=True, capture_output=True)

    def write(self, files):
        for rel, text in files.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text, encoding="utf-8")

    def test_format_only_change_is_silent(self):
        self.write({"docs/cau-hoi/x.md": X.replace("*b*", "**b**")})
        changes, gen, data = cu.collect("HEAD", None)
        self.assertEqual((changes, gen, data), ([], [], []))
        self.assertIn("Không đơn vị nội dung nào đổi chữ", cu.report("HEAD", None, changes, gen, data))

    def test_edit_add_remove_and_ledger_status(self):
        key = "cau-hoi/x.md#a"
        ledger = {"version": 1, "units": {key: {"status": "frozen", "hash": "sha256:" + "0" * 64}}}
        new = X.replace("1641", "1642").replace("## C {#c}\n\nc\n", "## D {#d}\n\nd\n")
        self.write({"docs/cau-hoi/x.md": new, "docs/them/y.md": "# Y khác\n",
                    "docs/triet-gia/kant.md": "# Kant khác\n", "docs/assets/data/terms.json": "[1]",
                    "verification/ledger.json": json.dumps(ledger)})
        changes, gen, data = cu.collect("HEAD", None)
        got = [(c.key, c.kind, c.tier, c.status) for c in changes]
        self.assertEqual(got, [
            ("cau-hoi/x.md#a", "sua", "loi", "frozen"),
            ("cau-hoi/x.md#c", "bo", "loi", None),
            ("cau-hoi/x.md#d", "them", "loi", None),
            ("them/y.md#_dau", "sua", "he-thong", None),
        ])
        self.assertEqual(gen, ["triet-gia/kant.md"])
        self.assertEqual([f for f, _ in data], ["docs/assets/data/terms.json"])
        text = cu.report("HEAD", None, changes, gen, data)
        self.assertIn("**1 đã đóng băng**", text)
        self.assertIn("cần nhãn `doi-loi`", text)
        self.assertIn("`triet-gia/kant.md`", text)
        self.assertIn("Checklist cho đơn vị Lõi", text)

    def test_commit_to_commit_and_new_page(self):
        self.write({"docs/cau-hoi/z.md": "## Mới {#moi}\n\nx\n"})
        self.git("add", "-A")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "them")
        changes, _, _ = cu.collect("HEAD~1", "HEAD")
        self.assertEqual([(c.key, c.kind, c.tier) for c in changes],
                         [("cau-hoi/z.md#moi", "them", None)])
        self.assertEqual(cu.todo(changes[0]), "trang chưa có trong `content.yml`")

    def test_unit_hashes_match_library(self):
        h = cu.unit_hashes("cau-hoi/x.md", X)
        self.assertEqual(list(h), ["_dau", "a", "b", "c"])
        self.assertEqual(h["c"], hashing.unit_hash("## C {#c}\n\nc\n"))


if __name__ == "__main__":
    unittest.main()
