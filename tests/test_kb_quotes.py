"""tools/kb_quotes.py: rút khối trích dẫn, ghép ngược đúng từng chữ. Chạy: python -m unittest discover -s tests"""

import contextlib
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import kb_quotes as kq  # noqa: E402

PAGE = '''# X

!!! quote "Platon, *Biện hộ*, 38a"
    "The unexamined life…"

    Một đời không được xét lại… *(bản dịch của Logos Zero)*

Văn xuôi.

??? note "Ngoài"
    !!! quote "Mạnh Tử, 2A6"
        > 今人乍見孺子
        >
        > *Kim nhân*

```text
!!! quote "trong code"
```
'''


class TestBlocks(unittest.TestCase):
    def test_page_blocks(self):
        got = kq.page_blocks("x.md", PAGE)
        self.assertEqual([(n, t) for n, t, _ in got], [(3, "Platon, *Biện hộ*, 38a"), (11, "Mạnh Tử, 2A6")])
        self.assertEqual(got[0][2], '"The unexamined life…"\n\nMột đời không được xét lại… *(bản dịch của Logos Zero)*')
        self.assertEqual(got[1][2], "> 今人乍見孺子\n>\n> *Kim nhân*")

    def test_base_key(self):
        self.assertEqual(kq.base_key("Platon, *Biện hộ của Socrates*, 38a"), "platon.bien-ho-cua-socrates")
        self.assertIsNone(kq.base_key("Biện hộ, 38a — bản dịch Benjamin Jowett"))


class TestRepo(unittest.TestCase):
    def test_counts_and_round_trip(self):
        recs, _ = kq.extract(ROOT)
        self.assertEqual(sum(len(r["used_in"]) for r in recs.values()), 156)   # 108 khối trong Lõi viết tay + 48 của hồ sơ
        for key, r in recs.items():
            if "body" not in r:
                continue
            page = r["used_in"][0].split("#")[0]
            blocks = kq.page_blocks(page, (ROOT / "docs" / page).read_text(encoding="utf-8"))
            self.assertIn((r["title"], r["body"]), [(t, b) for _, t, b in blocks], key)

    def test_file_is_current(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(kq.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
