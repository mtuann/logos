"""Linter: terms_policy, lint_terms, lint_volatile, lint_structure, lint_facts, lint_quotes, lint_so_lieu, lint_lien_ket
và phần chung lz.lint.
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

import lint_facts  # noqa: E402
import lint_lien_ket  # noqa: E402
import lint_quotes  # noqa: E402
import lint_so_lieu  # noqa: E402
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

    def test_allow(self):
        """Miễn theo (trang, từ, số chỗ) chỉ cho thuat-ngu-mo-ho; số chỗ đổi → mien-lech; mục thừa → mien-thua."""
        F = lint_terms.Finding
        fs = [F("a.md", 1, "", "thuat-ngu-mo-ho", "tinh thần", ""), F("a.md", 2, "", "thuat-ngu-mo-ho", "Tinh thần", ""),
              F("a.md", 3, "", "thuat-ngu", "ý chí tự do", ""), F("b.md", 1, "", "thuat-ngu-mo-ho", "mệnh đề", "")]
        ok = lint_terms.apply_allow(fs, [{"page": "a.md", "word": "tinh thần", "count": 2, "reason": "x"}])
        self.assertEqual(sorted((f.page, f.rule) for f in ok), [("a.md", "thuat-ngu"), ("b.md", "thuat-ngu-mo-ho")])
        lech = lint_terms.apply_allow(fs, [{"page": "a.md", "word": "tinh thần", "count": 1, "reason": "x"}])
        self.assertIn("mien-lech", [f.rule for f in lech])
        self.assertEqual(sum(f.rule == "thuat-ngu-mo-ho" for f in lech), 3)
        thua = lint_terms.apply_allow(fs, [{"page": "c.md", "word": "hiểu biết", "count": 1, "reason": "x"}])
        self.assertIn("mien-thua", [f.rule for f in thua])
        cung = lint_terms.apply_allow(fs, [{"page": "a.md", "word": "ý chí tự do", "count": 1, "reason": "x"}])
        self.assertIn(("a.md", "thuat-ngu"), [(f.page, f.rule) for f in cung])   # luật cứng không miễn được


class TestLintVolatile(unittest.TestCase):
    def test_year_and_citation(self):
        self.assertTrue(lint_volatile.YEAR.search("năm 2023"))
        self.assertFalse(lint_volatile.YEAR.search("PhilPapers 2020"))
        self.assertFalse(lint_volatile.YEAR.search("trang 12023"))
        self.assertTrue(lint_volatile.is_citation("(Bourget & Chalmers "))
        self.assertTrue(lint_volatile.is_citation("Kahane et al. "))
        self.assertFalse(lint_volatile.is_citation("từ năm "))
        self.assertFalse(lint_volatile.is_citation("gay gắt. Năm "))
        self.assertTrue(lint_volatile.is_citation("Hicks, Humphries và Slater ("))
        self.assertTrue(lint_volatile.is_citation("(Lucca và cộng sự "))
        self.assertFalse(lint_volatile.is_citation("Một nghiên cứu năm "))

    def hits(self, line):
        out = []
        for rx, rule in ((lint_volatile.YEAR, "nam"), (lint_volatile.PHRASE, "cum-thoi-gian"),
                         (lint_volatile.LAW, "van-ban-luat")):
            out += [m.group(0) for m in rx.finditer(line) if not lint_volatile.ignored(rule, line, m)]
        return out

    def test_meanings_not_time(self):
        # "tính đến" = "xét đến"; "hai nghìn năm nay" = độ dài; "Luật De Morgan" là luật logic
        for line in ("thông tin đó là điều bạn phải tính đến.", "đều không tính đến — một giá trị",
                     "từ hơn hai nghìn năm nay, các triết gia", "Luật De Morgan: phủ định của hội"):
            self.assertEqual(self.hits(line), [], line)
        for line, want in (("Tính đến năm 2026, có", ["2026", "Tính đến"]), ("tính đến nay vẫn", ["tính đến"]),
                           ("năm nay sao xấu", ["năm nay"]), ("Luật Bảo vệ dữ liệu", ["Luật "]),
                           ("phần lớn tạng ghép hiện nay", ["hiện nay"])):
            self.assertEqual(sorted(self.hits(line)), sorted(want), line)

    def test_allowlist(self):
        f = lint_volatile.Finding("a.md", 3, "a.md#x", "cum-thoi-gian", "đến nay", "")
        line = "Cuộc tranh luận này, đến nay, vẫn là một trong những điểm nóng nhất."
        old = lint_volatile.raw_findings
        lint_volatile.raw_findings = lambda: iter([(f, line)])
        try:
            ok = {"unit": "a.md#x", "found": "đến nay", "context": "tranh luận này, đến nay, vẫn là", "reason": "chung-chung"}
            stale = dict(ok, context="tranh luận ấy, đến nay, vẫn là")
            left, allowed, unused = lint_volatile.split_allowed([ok])
            self.assertEqual((left, len(allowed), unused), ([], 1, []))
            left, allowed, unused = lint_volatile.split_allowed([stale])
            self.assertEqual((left, allowed, unused), ([f], [], [stale]))   # đổi chữ: hết miễn, mục thành thừa
        finally:
            lint_volatile.raw_findings = old

    def test_allowlist_validation(self):
        tmp = Path(tempfile.mkdtemp(prefix="allow-"))
        try:
            for bad in ('- {unit: a.md#x, found: đến nay, context: ngắn đến nay, reason: chung-chung}',
                        '- {unit: a.md#x, found: đến nay, context: "một đoạn đủ dài nhưng thiếu cụm", reason: chung-chung}',
                        '- {unit: a.md#x, found: đến nay, context: "một đoạn đủ dài, đến nay vẫn vậy", reason: khac}',
                        '- {unit: a.md#x, found: đến nay, context: "một đoạn đủ dài, đến nay vẫn vậy"}'):
                (tmp / "a.yml").write_text(bad, encoding="utf-8")
                with self.assertRaises(ValueError, msg=bad):
                    lint_volatile.load_allow(tmp / "a.yml")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

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
        """Báo cáo nền (verification/bao-cao-nen.md mục 5) có hai trang; đợt 5.4: mục "Đọc từng đoạn (diễn ý)"
        của Sartre được nhận, còn luan-cu-thep (5.5)."""
        got = sorted((f.page, f.found) for f in lint_structure.collect() if f.rule == "thieu-muc")
        self.assertEqual(got, [("cong-cu/luan-cu-thep.md", "Bài tập"), ("cong-cu/luan-cu-thep.md", "Tự kiểm tra")])

    def test_norm_heading(self):
        self.assertEqual(lint_structure.norm_heading("Câu hỏi thật sự là gì? {#cau-hoi}"), "câu hỏi thật sự là gì")
        self.assertEqual(lint_structure.norm_heading("Đọc từng đoạn (diễn ý) {#doc-tung-doan-dien-y}"), "đọc từng đoạn")


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


class TestLintFacts(unittest.TestCase):
    def test_life_pattern(self):
        m = lint_facts.LIFE.search("vua [Trần Nhân Tông](../triet-gia/tran-nhan-tong.md) (1258–1308) sau khi")
        self.assertEqual((m.group("id"), m.group("b"), m.group("d")), ("tran-nhan-tong", "1258", "1308"))
        m = lint_facts.LIFE.search("Socrates (k. 469–399 TCN) hỏi")
        self.assertEqual((m.group("name"), m.group("b"), m.group("dtcn")), ("Socrates", "469", " TCN"))

    def test_repo_only_unsettled_years(self):
        rules = {f.rule for f in lint_facts.collect()}
        self.assertLessEqual(rules, {"nam-chua-chot"})   # kho rút từ chính các trang: chỉ còn chỗ chưa chốt


class TestLintQuotes(unittest.TestCase):
    def test_repo_blocks_match_store(self):
        rules = {f.rule for f in lint_quotes.collect()}
        self.assertNotIn("khong-khop", rules)
        self.assertNotIn("mo-coi", rules)

    def test_work_note_and_locator(self):
        """`work_note` (lý do không ghép tác phẩm) thay cho `work`; thiếu cả hai, hoặc thiếu `locator`, thì báo."""
        base = {"title": "X", "original": "o", "translation": "t", "translator": None, "license": "unknown",
                "url": "https://example.org", "used_in": ["people/x"], "evidence": [], "verified": None}
        recs = {"x.co-ly-do": {"work": None, "work_note": "phát biểu, không phải tác phẩm", "locator": "§1", **base},
                "x.co-tac-pham": {"work": "x.tac-pham", "locator": "38a", **base},
                "x.chua": {"work": None, **base}}
        tmp = Path(tempfile.mkdtemp(prefix="quotes-"))
        (tmp / "quotes.yml").write_text(yaml.safe_dump(recs, allow_unicode=True), encoding="utf-8")
        old = lint_quotes.QUOTES
        lint_quotes.QUOTES = tmp / "quotes.yml"
        try:
            got = {(f.rule, f.found) for f in lint_quotes.collect() if f.page == "data/kb/quotes.yml"}
        finally:
            lint_quotes.QUOTES = old
            shutil.rmtree(tmp, ignore_errors=True)
        self.assertEqual(got, {("chua-ghep-tac-pham", "x.chua"), ("chua-co-vi-tri", "x.chua")})


class TestLintSoLieu(unittest.TestCase):
    KB = {"questions": [{"id": "tu-do-y-chi", "options": [
        {"id": "tuong-thich-luan", "pct": 59.2, "pct_reject": None, "pct_exclusive": None},
        {"id": "khac", "pct": 11.4, "pct_reject": 3.0, "pct_exclusive": None}]}]}
    PAGE = """---
title: T
---

# T

!!! summary "Tóm tắt 5 phút"
    - Đa số (59,2%) theo tương thích luận.

Văn xuôi: 92% người dùng ứng dụng X hài lòng.

## Giới triết học ngày nay nghĩ gì {#gioi-triet-hoc-ngay-nay-nghi-gi}

Khoảng 61% chấp nhận; [[pp:tu-do-y-chi.khac]]% khác; tổng không bằng 100%.

## Tự kiểm tra {#tu-kiem-tra}

<div class="oz-quiz" data-id="t"><script type="application/json">
[{"q": "Bao nhiêu?", "options": ["20%", "59,2%", "70%"], "answer": 1, "explain": "Khoảng 60%."}]
</script></div>

## Nguồn {#nguon}

1. Số 59,2% ở đây không tính.
"""

    def test_kb_values_and_lookup(self):
        kb = lint_so_lieu.kb_values(self.KB)
        self.assertEqual(kb["59,2"], ["tu-do-y-chi.tuong-thich-luan"])
        self.assertEqual(kb["3,0"], ["tu-do-y-chi.khac/bac-bo"])
        self.assertEqual(lint_so_lieu.lookup("3", kb, set()), ["tu-do-y-chi.khac/bac-bo"])   # "3%" = "3,0"
        self.assertEqual(lint_so_lieu.lookup("59", kb, set()), [])

    def test_scan_page(self):
        found = lint_so_lieu.scan_page("cau-hoi/t.md", self.PAGE, lint_so_lieu.kb_values(self.KB))
        self.assertEqual(sorted((f.rule, f.found) for f in found),
                         [("go-tay", "59,2%"), ("ngoai-kho", "61%"), ("quiz", "câu 1: 60%")])
        go = next(f for f in found if f.rule == "go-tay")
        self.assertIn("[[pp:tu-do-y-chi.tuong-thich-luan]]%", go.message)

    def test_allow(self):
        f = lint.Finding("cau-hoi/t.md", 3, "", "ngoai-kho", "61%", "")
        q = lint.Finding("cau-hoi/t.md", 9, "", "quiz", "câu 1: 60%", "")
        allow = [{"page": "cau-hoi/t.md", "text": "Khoảng 61% chấp nhận", "reason": "r"},
                 {"page": "cau-hoi/t.md", "text": "câu 1: 60%", "reason": "r"},
                 {"page": "cau-hoi/khac.md", "text": "x", "reason": "r"}]
        kept = lint_so_lieu.apply_allow([f, q], allow, lambda x: "Khoảng 61% chấp nhận; …" if x.line == 3 else "<div>")
        self.assertEqual([k.rule for k in kept], ["mien-thua"])

    def test_repo_runs(self):
        rules = {f.rule for f in lint_so_lieu.collect()}
        self.assertLessEqual(rules, set(lint_so_lieu.RULES))
        self.assertNotIn("mien-thua", rules)


class TestLintLienKet(unittest.TestCase):
    PEOPLE = {"kant": {"name": "Immanuel Kant", "name_en": "Immanuel Kant"},
              "khong-tu": {"name": "Khổng Tử", "name_en": "Kongzi (Confucius)"},
              "zeno": {"name": "Zeno xứ Citium", "name_en": "Zeno of Citium"},
              "anselm": {"name": "Anselm xứ Canterbury", "name_en": "Anselm of Canterbury"}}
    PAGE = """---
title: T
---

# T

Theo Kant, đạo đức là bổn phận; người *Kantian* không tính. Khổng Tử dạy nhân.

## Nguồn {#nguon}

1. Anselm, *Proslogion*.
"""

    def test_aliases(self):
        a = lint_lien_ket.aliases(self.PEOPLE)
        self.assertEqual(a["kant"], {"Immanuel Kant", "Kant"})
        self.assertEqual(a["khong-tu"], {"Khổng Tử", "Kongzi"})
        self.assertEqual(a["anselm"], {"Anselm xứ Canterbury", "Anselm of Canterbury", "Anselm"})
        self.assertNotIn("zeno", a)

    def test_scan_page(self):
        names = lint_lien_ket.aliases(self.PEOPLE)
        display = {k: v["name"] for k, v in self.PEOPLE.items()}
        found = lint_lien_ket.scan_page("cau-hoi/t.md", self.PAGE, names, display)
        self.assertEqual(sorted(f.found for f in found), ["Kant (kant)", "Khổng Tử (khong-tu)"])   # Nguồn không tính
        kant = next(f for f in found if f.found.startswith("Kant"))
        self.assertEqual((kant.line, kant.rule), (7, "thieu-link"))
        self.assertIn("[Immanuel Kant](../triet-gia/kant.md)", kant.message)
        linked = self.PAGE.replace("Theo Kant", "Theo [Kant](../triet-gia/kant.md)")
        self.assertEqual([f.found for f in lint_lien_ket.scan_page("cau-hoi/t.md", linked, names, display)],
                         ["Khổng Tử (khong-tu)"])

    def test_repo_runs(self):
        rules = {f.rule for f in lint_lien_ket.collect()}
        self.assertLessEqual(rules, set(lint_lien_ket.RULES))
        self.assertNotIn("mien-thua", rules)


if __name__ == "__main__":
    unittest.main()
