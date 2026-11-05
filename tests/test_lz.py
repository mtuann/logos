"""Thư viện tools/lz: sổ đăng ký, tách đơn vị, chuẩn hóa và băm (KE-HOACH.md mục 5.5, 5.6).

Mỗi hệ quả ở mục 5.6 có một kiểm thử riêng:
- đổi định dạng (`*nhấn*` → `**nhấn**`, `!!! note` → `!!! tip`, kiểu danh sách, căn bảng, ngắt dòng…) → mã băm không đổi;
- đổi nền tảng render → mã băm không đổi (chuẩn hóa không dùng thư viện render nào);
- sửa một chữ, một năm, một link → mã băm đổi.
Chạy: python -m unittest discover -s tests
"""

import re
import subprocess
import sys
import unittest
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from lz import hashing, registry, units  # noqa: E402
from lz.normalize import normalize  # noqa: E402

H = hashing.unit_hash

UNIT = """## Các lập trường chính {#cac-lap-truong-chinh}

Năm 1641, *René Descartes* viết [Suy niệm](../triet-gia/descartes.md) về **Triết học Đệ nhất**.

!!! note "Ghi chú"
    Theo SEP: <https://plato.stanford.edu/entries/descartes/>.

- Hoài nghi luận
- Duy lý luận

| Lập trường | Tỉ lệ |
|---|---:|
| Tương thích luận | 59,2 |

<div class="oz-quiz" data-id="knowledge-1" data-skill="knowledge" markdown="0">
<script type="application/json">
[
 {"q": "Câu hỏi?", "options": ["A", "B"], "answer": 1, "explain": "Vì B."}
]
</script>
</div>
"""


def variant(old: str, new: str, text: str = UNIT) -> str:
    assert old in text, old
    return text.replace(old, new)


class TestFormatChangesKeepHash(unittest.TestCase):
    """Đổi định dạng, không đổi chữ hiển thị → mã băm không đổi."""

    def same(self, other: str):
        self.assertEqual(normalize(UNIT), normalize(other))
        self.assertEqual(H(UNIT), H(other))

    def test_emphasis_style(self):
        self.same(variant("*René Descartes*", "**René Descartes**"))
        self.same(variant("*René Descartes*", "_René Descartes_"))
        self.same(variant("**Triết học Đệ nhất**", "Triết học Đệ nhất"))

    def test_admonition_type(self):
        self.same(variant('!!! note "Ghi chú"', '!!! tip "Ghi chú"'))
        self.same(variant('!!! note "Ghi chú"', '??? warning "Ghi chú"'))
        self.same(variant('!!! note "Ghi chú"', '???+ note "Ghi chú"'))

    def test_list_marker(self):
        self.same(variant("- Hoài nghi luận\n- Duy lý luận", "* Hoài nghi luận\n* Duy lý luận"))
        self.same(variant("- Hoài nghi luận\n- Duy lý luận", "1. Hoài nghi luận\n2. Duy lý luận"))

    def test_table_layout(self):
        self.same(variant("|---|---:|", "|:---|:---:|"))
        self.same(variant("| Tương thích luận | 59,2 |", "|Tương thích luận|59,2|"))

    def test_line_wrapping_and_whitespace(self):
        self.same(variant("viết [Suy niệm]", "viết\n[Suy niệm]"))
        self.same(variant("Năm 1641,", "Năm   1641,"))
        self.same(UNIT.replace("\n", "\r\n"))

    def test_heading_id_attribute(self):
        self.same(variant(" {#cac-lap-truong-chinh}", ""))
        self.same(variant("{#cac-lap-truong-chinh}", "{#cac-lap-truong-chinh .lop}"))

    def test_unicode_composition(self):
        self.same(unicodedata.normalize("NFD", UNIT))

    def test_quiz_json_layout(self):
        self.same(variant(
            '{"q": "Câu hỏi?", "options": ["A", "B"], "answer": 1, "explain": "Vì B."}',
            '{"answer": 1,\n  "q": "Câu hỏi?",  "explain": "Vì B.", "options": ["A","B"]}',
        ))

    def test_link_title_and_angle_target(self):
        self.same(variant("(../triet-gia/descartes.md)", '(../triet-gia/descartes.md "Descartes")'))
        self.same(variant("(../triet-gia/descartes.md)", "(<../triet-gia/descartes.md>)"))

    def test_comments_front_matter_and_generated_blocks_ignored(self):
        self.same("<!-- ghi chú biên tập -->\n" + UNIT)
        page = "---\ntitle: T\nupdated: 2026-10-01\n---\n" + UNIT
        self.assertEqual(H(page), H(page.replace("2026-10-01", "2026-11-05")))
        self.assertEqual(H(page), H(UNIT))
        gen = UNIT + "\n<!-- gen:bang -->\n| a | 1 |\n<!-- /gen:bang -->\n"
        self.assertEqual(H(gen), H(gen.replace("| a | 1 |", "| a | 2 |\n| b | 3 |")))
        fig = UNIT + "\n<!-- fig:hinh -->\n<svg><text>A</text></svg>\n<!-- /fig:hinh -->\n"
        self.assertEqual(H(fig), H(fig.replace(">A<", ">B<")))


class TestRendererIndependence(unittest.TestCase):
    """Đổi nền tảng render → mã băm không đổi: chuẩn hóa làm trên nguồn, không nạp thư viện render nào."""

    def test_no_renderer_imported(self):
        code = (
            "import sys; sys.path.insert(0, 'tools');"
            "from lz import hashing, units, normalize, registry;"
            "bad = [m for m in ('markdown', 'pymdownx', 'mkdocs', 'properdocs', 'material') if m in sys.modules];"
            "print(','.join(bad))"
        )
        out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, check=True)
        self.assertEqual(out.stdout.strip(), "")

    def test_golden_value(self):
        # Neo thuật toán: đổi cách chuẩn hóa hay cách băm thì mọi đơn vị đã đóng băng bị mở khóa.
        # Kiểm thử này đỏ nghĩa là thay đổi đó phải là một quyết định có chủ ý (KE-HOACH.md mục 5.6).
        self.assertEqual(
            normalize(UNIT),
            'Các lập trường chính Năm 1641, René Descartes viết Suy niệm⟨../triet-gia/descartes.md⟩ về '
            'Triết học Đệ nhất. Ghi chú Theo SEP: https://plato.stanford.edu/entries/descartes/'
            '⟨https://plato.stanford.edu/entries/descartes/⟩. Hoài nghi luận Duy lý luận Lập trường | Tỉ lệ '
            'Tương thích luận | 59,2 ⟨oz-quiz data-id=knowledge-1 data-skill=knowledge⟩ '
            '[{"answer":1,"explain":"Vì B.","options":["A","B"],"q":"Câu hỏi?"}]',
        )
        self.assertEqual(H(UNIT), hashing.digest(normalize(UNIT)))
        self.assertEqual(hashing.digest("abc"),
                         "sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")


class TestContentChangesChangeHash(unittest.TestCase):
    """Sửa chữ, năm, link → mã băm đổi."""

    def differ(self, other: str):
        self.assertNotEqual(H(UNIT), H(other))

    def test_word(self):
        self.differ(variant("Hoài nghi luận", "Hoài nghi thuyết"))
        self.differ(variant('"Ghi chú"', '"Lưu ý"'))         # tiêu đề admonition là chữ hiển thị

    def test_year_and_number(self):
        self.differ(variant("1641", "1642"))
        self.differ(variant("59,2", "59,3"))

    def test_link_target(self):
        self.differ(variant("../triet-gia/descartes.md", "../triet-gia/leibniz.md"))
        self.differ(variant("entries/descartes/>", "entries/descartes-works/>"))

    def test_quiz_answer_and_id(self):
        self.differ(variant('"answer": 1', '"answer": 0'))
        self.differ(variant('data-id="knowledge-1"', 'data-id="knowledge-2"'))

    def test_heading_and_table_cell(self):
        self.differ(variant("## Các lập trường chính", "## Các lập trường"))
        self.differ(variant("| Tương thích luận |", "| Bất tương thích luận |"))


class TestNormalizeDetails(unittest.TestCase):
    def test_code_kept_verbatim(self):
        src = "Câu:\n\n```text\nP1. *không* phải nhấn\n```\n\nvà `a_b*c`."
        self.assertEqual(normalize(src), "Câu: P1. *không* phải nhấn và a_b*c.")

    def test_escapes_and_entities(self):
        self.assertEqual(normalize(r"2 \* 3 &amp; \_x\_"), "2 * 3 & _x_")

    def test_intraword_underscore_kept(self):
        self.assertEqual(normalize("snake_case và _nhấn_"), "snake_case và nhấn")

    def test_shortcode_kept(self):
        self.assertEqual(normalize("Có [[count:cau-hoi]] bài **hay**."), "Có [[count:cau-hoi]] bài hay.")

    def test_blockquote_in_admonition(self):
        src = '!!! quote "Mạnh Tử, 2A6"\n    > 今人乍見孺子\n    >\n    > *Kim nhân*'
        self.assertEqual(normalize(src), "Mạnh Tử, 2A6 今人乍見孺子 Kim nhân")

    def test_widgets(self):
        self.assertEqual(normalize('<div class="oz-fallacy-trainer" data-count="10"></div>'),
                         "⟨oz-fallacy-trainer data-count=10⟩")
        self.assertEqual(normalize("<small>Platon, *Biện hộ*</small>"), "Platon, Biện hộ")

    def test_link_with_parentheses_in_target(self):
        self.assertEqual(normalize("[Gettier](https://vi.wikipedia.org/wiki/A_(B))"),
                         "Gettier⟨https://vi.wikipedia.org/wiki/A_(B)⟩")

    def test_link_text_across_lines(self):
        self.assertEqual(normalize("[Thiền Trúc\nLâm](../cau-hoi/truc-lam.md)."),
                         "Thiền Trúc Lâm⟨../cau-hoi/truc-lam.md⟩.")

    def test_horizontal_rule_dropped(self):
        self.assertEqual(normalize("a\n\n---\n\nb"), "a b")


class TestUnits(unittest.TestCase):
    PAGE = """---
title: T
---

# Tiêu đề

Mở đầu.

## Câu hỏi thật sự là gì? {#cau-hoi}

```text
## không phải mục
```

!!! note "x"
    ## cũng không phải mục

## Nguồn

1. A
## Nguồn
"""

    def test_split(self):
        us = units.split("cau-hoi/x.md", self.PAGE)
        self.assertEqual([u.key for u in us], ["cau-hoi/x.md#_dau", "cau-hoi/x.md#cau-hoi",
                                               "cau-hoi/x.md#nguon", "cau-hoi/x.md#nguon_1"])
        self.assertEqual([u.explicit_id for u in us], [True, True, False, False])
        self.assertEqual(us[1].title, "Câu hỏi thật sự là gì?")
        self.assertIn("## không phải mục", us[1].source)
        self.assertEqual((us[0].start, us[1].start, us[-1].end), (4, 9, 21))

    def test_units_cover_body(self):
        us = units.split("x.md", self.PAGE)
        self.assertEqual("".join(u.source for u in us), self.PAGE.split("---\n", 2)[2])

    def test_empty_head_unit(self):
        us = units.split("x.md", "## A\n\nb\n")
        self.assertEqual([u.id for u in us], ["_dau", "a"])
        self.assertEqual(us[0].source, "")

    def test_duplicate_explicit_id_rejected(self):
        with self.assertRaises(ValueError):
            units.split("x.md", "## A {#a}\n\n## B {#a}\n")

    def test_explicit_ids_reserved_before_slugs(self):
        # toc giữ ID viết tay trước, nên mục "A" đứng trước vẫn phải nhận a_1.
        us = units.split("x.md", "## A\n\n## B {#a}\n")
        self.assertEqual([u.id for u in us[1:]], ["a_1", "a"])

    def test_ids_match_built_site(self):
        """ID dự phòng khớp anchor H2 trong HTML đã build (bỏ qua trang có H2 nằm trong khối sinh)."""
        site = ROOT / "site"
        if not (site / "index.html").exists():
            self.skipTest("chưa build site/")
        reg = registry.load(ROOT)
        checked = 0
        for p in reg.pages:
            src = p.file(ROOT).read_text(encoding="utf-8")
            gen = re.findall(r"<!-- (gen|fig):(\S+) -->(.*?)<!-- /\1:\2 -->", src, re.S)
            if any(re.search(r"^## ", body, re.M) for *_, body in gen):
                continue
            rel = p.path[: -len("index.md")] if p.path.endswith("index.md") else p.path[:-3] + "/"
            built = re.findall(r'<h2 id="([^"]+)"', (site / rel / "index.html").read_text(encoding="utf-8"))
            self.assertEqual([u.id for u in units.split(p.path, src)[1:]], built, p.path)
            checked += 1
        self.assertGreater(checked, 170)


class TestRegistry(unittest.TestCase):
    def test_load_and_select(self):
        reg = registry.load(ROOT)
        self.assertEqual(len(reg.pages), 180)
        self.assertEqual(reg.page("cau-hoi/tri-thuc.md").block, "tri-thuc")
        core = reg.select(tier="loi", generated=False)
        self.assertTrue(all(p.tier == "loi" and not p.generated for p in core))
        self.assertEqual(len(reg.select(type="cau-hoi")), 57)
        with self.assertRaises(KeyError):
            reg.page("khong-co.md")

    def test_core_unit_count(self):
        """887 mục H2 trong Lõi viết tay (verification/bao-cao-nen.md); đổi số này phải có lý do."""
        reg = registry.load(ROOT)
        n = sum(len(units.split_file(p.path, ROOT)) - 1 for p in reg.select(tier="loi", generated=False))
        self.assertEqual(n, 887)


class TestHeadingIds(unittest.TestCase):
    def test_core_h2_all_have_explicit_ids(self):
        """Mọi mục H2 của Lõi viết tay có ID cố định (việc 1.3); mục mới phải được gắn ID khi thêm."""
        sys.path.insert(0, str(ROOT / "tools"))
        import add_heading_ids
        self.assertEqual(add_heading_ids.missing_ids(ROOT), [])


class TestRecordHash(unittest.TestCase):
    def test_key_order_and_verified_ignored(self):
        a = {"id": "kant", "born": 1724, "verified": None}
        b = {"born": 1724, "id": "kant", "verified": {"date": "2027-01-05", "by": "agent"}}
        self.assertEqual(hashing.record_hash(a), hashing.record_hash(b))
        self.assertNotEqual(hashing.record_hash(a), hashing.record_hash({**a, "born": 1725}))


if __name__ == "__main__":
    unittest.main()
