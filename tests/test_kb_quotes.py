"""tools/kb_quotes.py: rút khối trích dẫn, ghép ngược đúng từng chữ. Chạy: python -m unittest discover -s tests"""

import contextlib
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import kb_quotes as kq  # noqa: E402
import yaml  # noqa: E402

PAGE = '''# X

!!! quote "Platon, *Biện hộ*, 38a"
    "The unexamined life…"

    Một đời không được xét lại… *(bản dịch của Logos)*

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
        self.assertEqual(got[0][2], '"The unexamined life…"\n\nMột đời không được xét lại… *(bản dịch của Logos)*')
        self.assertEqual(got[1][2], "> 今人乍見孺子\n>\n> *Kim nhân*")

    def test_base_key(self):
        self.assertEqual(kq.base_key("Platon, *Biện hộ của Socrates*, 38a"), "platon.bien-ho-cua-socrates")
        self.assertIsNone(kq.base_key("Biện hộ, 38a — bản dịch Benjamin Jowett"))

    def test_italic_title_keeps_key(self):
        """Đặt tên tác phẩm đứng đầu tiêu đề vào *…* (đợt 5.2) không đổi khóa `trich.*`."""
        for plain, italic in (("Biện hộ, 38a — bản dịch Benjamin Jowett", "*Biện hộ*, 38a — bản dịch Benjamin Jowett"),
                              ("Mạnh Tử 2A6 (thiên Công Tôn Sửu thượng) — x", "*Mạnh Tử* 2A6 (thiên Công Tôn Sửu thượng) — x")):
            self.assertIsNone(kq.base_key(italic))
            self.assertEqual(kq.slug(italic.split(" — ")[0], 60), kq.slug(plain.split(" — ")[0], 60))


class TestWorkMatch(unittest.TestCase):
    WORKS = {
        "platon.politeia": {"titles": ["Politeia"]},
        "chua-ro.cong-hoa": {"titles": ["Cộng hòa"], "same_as": "platon.politeia"},
        "marx.thesen-uber-feuerbach": {"titles": ["Thesen über Feuerbach"]},
        "chua-ro.apologia": {"titles": ["Apologia"]},
    }

    def test_work_name(self):
        self.assertEqual(kq.work_name("Augustine, *Tự thú* (*Confessions*), quyển I"), "Tự thú")
        self.assertEqual(kq.work_name("Karl Marx, “Thesen über Feuerbach” (1845), luận cương 11"), "Thesen über Feuerbach")
        self.assertEqual(kq.work_name("Trần Nhân Tông, kệ 'Cư trần lạc đạo' (bản dịch)"), "Cư trần lạc đạo")
        self.assertIsNone(kq.work_name("Winston Churchill, phát biểu tại Hạ viện Anh, 11/11/1947"))

    def test_work_of(self):
        index = kq.work_index(self.WORKS)
        self.assertEqual(kq.work_of("Platon, *Cộng hòa* X, 596a", index), "platon.politeia")   # same_as → bản gốc
        self.assertEqual(kq.work_of("*Biện hộ*, 38a — bản dịch Benjamin Jowett", index), "chua-ro.apologia")   # TEN_KHAC
        self.assertEqual(kq.work_of("Karl Marx, “Thesen über Feuerbach” (1845)", index), "marx.thesen-uber-feuerbach")
        self.assertIsNone(kq.work_of("Biện hộ, 38a — bản dịch Benjamin Jowett", index))   # chưa in nghiêng
        self.assertIsNone(kq.work_of("Clive Bell, *Art*, chương 1, 1914", index))

    def test_ten_khac_points_to_existing_original_works(self):
        works = yaml.safe_load((ROOT / "data" / "kb" / "works.yml").read_text(encoding="utf-8"))
        for name, key in kq.TEN_KHAC.items():
            self.assertIn(key, works, name)
            self.assertNotIn("same_as", works[key], name)


class TestKeepAndLech(unittest.TestCase):
    @staticmethod
    def rec(title, work=None, **extra):
        return {"work": work, "title": title, "body": "b", "translator": None, "license": "unknown",
                "used_in": ["a.md#x"], "evidence": [], "verified": None, **extra}

    def test_merge_kept_keeps_locator_and_work_note(self):
        recs = {"trich.a": self.rec("A")}
        old = {"trich.a": self.rec("A", work="cu.tac-pham", locator="§1", work_note="phát biểu, không phải tác phẩm")}
        got = kq.merge_kept(recs, old)["trich.a"]
        self.assertEqual((got["locator"], got["work_note"], got["work"]), ("§1", "phát biểu, không phải tác phẩm", None))
        self.assertLess(kq.render(recs).index("work_note:"), kq.render(recs).index("locator:"))

    def test_lech_open_items(self):
        recs = {"trich.ghep": self.rec("*Biện hộ*, 38a", work="chua-ro.apologia", locator="38a"),
                "trich.ly-do": self.rec("Winston Churchill, phát biểu", work_note="phát biểu, không phải tác phẩm"),
                "trich.mo": self.rec("Tâm kinh (T251)")}
        text = kq.render_lech(recs, ["trich.ghep", "trich.ly-do", "trich.mo"])
        mo = text.split("## Mục mở")[1].split("\n## ")[0]
        self.assertIn("(1)", mo)
        self.assertIn("`trich.mo`", mo)
        self.assertNotIn("`trich.ghep`", mo)
        self.assertNotIn("`trich.ly-do`", mo)
        self.assertIn("`trich.ghep` → `chua-ro.apologia`", text)
        self.assertIn("— phát biểu, không phải tác phẩm", text)
        del recs["trich.mo"]
        self.assertIn("Không còn mục mở.", kq.render_lech(recs, ["trich.ghep", "trich.ly-do"]))


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
