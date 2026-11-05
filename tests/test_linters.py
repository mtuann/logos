"""Linter đợt 1: terms_policy, lint_terms, lint_volatile, lint_structure và phần chung lz.lint.
Chạy: python -m unittest discover -s tests"""

import contextlib
import datetime
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import lint_structure  # noqa: E402
import lint_terms  # noqa: E402
import lint_volatile  # noqa: E402
import terms_policy  # noqa: E402
import yaml  # noqa: E402
from lz import lint  # noqa: E402


class TestMaskedLines(unittest.TestCase):
    PAGE = """---
title: Tiêu đề
updated: 2026-10-22
---

Văn [xuôi](../a.md) và `mã`.

!!! quote "Platon, *Cộng hòa*"
    Trích nguyên văn.

> Cũng là trích.

```text
code
```

## Nguồn {#nguon}

1. Nguồn A
"""

    def test_masks(self):
        lines = lint.masked_lines(self.PAGE, meta=("title",))
        text = "\n".join(lines)
        self.assertEqual(lines[2], "title: Tiêu đề")        # giữ khóa được yêu cầu, đúng số dòng
        self.assertNotIn("2026-10-22", text)
        self.assertIn("Văn [xuôi", text)
        for gone in ("../a.md", "mã", "Trích nguyên văn", "Cũng là trích", "code", "Nguồn A"):
            self.assertNotIn(gone, text)
        self.assertEqual(len(lines), self.PAGE.count("\n") + 2)

    def test_optional_masks(self):
        text = "\n".join(lint.masked_lines(self.PAGE, quotes=False, sources=False))
        self.assertIn("Trích nguyên văn", text)
        self.assertIn("Nguồn A", text)


class TestTermsPolicy(unittest.TestCase):
    def test_policy_file_matches_guide(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(terms_policy.main(["--check"]), 0)

    def test_parse_avoid(self):
        self.assertEqual(terms_policy.parse_avoid("quyết định luận, thuyết định mệnh (sai)"),
                         (["quyết định luận", "thuyết định mệnh"], None))
        self.assertEqual(terms_policy.parse_avoid("suy diễn hồi quy, abduction"), (["suy diễn hồi quy"], None))
        self.assertEqual(terms_policy.parse_avoid("— không nhầm với X"), ([], "không nhầm với X"))

    def test_names(self):
        policy = terms_policy.build((ROOT / "HUONG-DAN-VIET.md").read_text(encoding="utf-8"))
        self.assertIn({"use": "Platon", "avoid": ["Plato"]}, policy["names"])


class TestLintTerms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = lint_terms.compile_rules(yaml.safe_load(lint_terms.POLICY.read_text(encoding="utf-8")))

    def hits(self, line):
        text = lint_terms.prose(line)
        return [(rule, m.group(0)) for rx, rule, _, _ in self.rules for m in rx.finditer(text)]

    def test_avoid_and_context(self):
        self.assertEqual(self.hits("Họ tin vào ý chí tự do."), [("thuat-ngu", "ý chí tự do")])
        self.assertEqual(self.hits("Thuyết ý chí tự do (libertarianism)."), [])
        self.assertEqual(self.hits("Bản luận cứ thép."), [])
        self.assertEqual(self.hits("Cuộc tranh luận cứ xoay vòng."), [])
        self.assertEqual(self.hits("Ba luận cứ tốt nhất."), [("thuat-ngu", "luận cứ")])

    def test_ambiguous_and_names(self):
        self.assertEqual(self.hits("Logic mệnh đề."), [("thuat-ngu-mo-ho", "mệnh đề")])
        self.assertEqual(self.hits("Plato viết; Platon viết; Platonism."), [("ten-rieng", "Plato")])

    def test_italic_and_quotes_skipped(self):
        self.assertEqual(self.hits('*Plato* và "ý chí tự do" và “luận cứ”.'), [])


class TestLintVolatile(unittest.TestCase):
    def test_year_and_citation(self):
        self.assertTrue(lint_volatile.YEAR.search("năm 2023"))
        self.assertFalse(lint_volatile.YEAR.search("PhilPapers 2020"))
        self.assertFalse(lint_volatile.YEAR.search("trang 12023"))
        self.assertTrue(lint_volatile.is_citation("(Bourget & Chalmers "))
        self.assertTrue(lint_volatile.is_citation("Kahane et al. "))
        self.assertFalse(lint_volatile.is_citation("từ năm "))
        self.assertFalse(lint_volatile.is_citation("gay gắt. Năm "))

    def test_overdue_thoi_su(self):
        tmp = Path(tempfile.mkdtemp(prefix="thoi-su-"))
        (tmp / "a.md").write_text("---\npage: x.md\nreview_by: 2027-01-01\n---\nX\n", encoding="utf-8")
        old = lint_volatile.THOI_SU
        lint_volatile.THOI_SU = tmp
        orig_root = lint_volatile.ROOT
        lint_volatile.ROOT = tmp.parent
        try:
            late = [f for f in lint_volatile.collect(datetime.date(2027, 2, 1)) if f.rule == "thoi-su-qua-han"]
            early = [f for f in lint_volatile.collect(datetime.date(2026, 12, 1)) if f.rule == "thoi-su-qua-han"]
        finally:
            lint_volatile.THOI_SU, lint_volatile.ROOT = old, orig_root
            shutil.rmtree(tmp, ignore_errors=True)
        self.assertEqual(len(late), 1)
        self.assertEqual(early, [])


class TestLintStructure(unittest.TestCase):
    def test_baseline_missing_sections(self):
        """Khớp verification/bao-cao-nen.md mục 5 (hai trang thiếu mục)."""
        got = sorted((f.page, f.found) for f in lint_structure.collect() if f.rule == "thieu-muc")
        self.assertEqual(got, [("cong-cu/luan-cu-thep.md", "Bài tập"), ("cong-cu/luan-cu-thep.md", "Tự kiểm tra"),
                               ("doc/sartre-hien-sinh.md", "Đọc từng đoạn")])

    def test_norm_heading(self):
        self.assertEqual(lint_structure.norm_heading("Câu hỏi thật sự là gì? {#cau-hoi}"), "câu hỏi thật sự là gì")


class TestReports(unittest.TestCase):
    def test_render_is_deterministic(self):
        """Báo cáo nền không ghi ngày giờ: cùng nội dung thì sinh lại y hệt."""
        findings = sorted(lint_structure.collect(), key=lambda f: (f.page, f.line, f.rule, f.found))
        a = lint.render("T", "I", findings, lint_structure.RULES)
        b = lint.render("T", "I", list(reversed(findings))[::-1], lint_structure.RULES)
        self.assertEqual(a, b)
        self.assertIn("| `thieu-muc` | ", a)

    def test_cli_warning_vs_strict(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(lint_structure.main(["-q"]), 0)
            self.assertEqual(lint_structure.main(["-q", "--strict"]), 1)
        self.assertIn("chế độ cảnh báo", out.getvalue())

if __name__ == "__main__":
    unittest.main()
