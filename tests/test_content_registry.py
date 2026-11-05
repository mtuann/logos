"""Sổ đăng ký nội dung (content.yml) và công cụ kiểm tra của nó. Chạy: python -m unittest discover -s tests"""

import copy
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import content_registry as cr  # noqa: E402


class TestRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = cr.load_registry(ROOT)

    def page(self, reg, path):
        return next(e for e in reg["pages"] if e["path"] == path)

    def assertError(self, reg, needle):
        errors = cr.check(reg, ROOT)
        self.assertTrue(any(needle in e for e in errors), f"không thấy lỗi chứa {needle!r} trong {errors}")

    def test_registry_matches_pages_and_data(self):
        self.assertEqual(cr.check(copy.deepcopy(self.reg), ROOT), [])

    def test_block_list_matches_plan(self):
        """Danh sách khối trong schema phải đúng mục 5.3 của KE-HOACH.md."""
        plan = (ROOT / "KE-HOACH.md").read_text(encoding="utf-8")
        section = plan.split("### 5.3", 1)[1].split("###", 1)[0]
        first_line = next(l for l in section.splitlines() if l.startswith("`"))
        self.assertEqual(re.findall(r"`([a-z-]+)`", first_line), cr.schema_enums(ROOT)["block"])

    def test_init_covers_every_page_once(self):
        reg, _ = cr.build_registry(ROOT)
        paths = [e["path"] for e in reg["pages"]]
        files = sorted(p.relative_to(ROOT / "docs").as_posix() for p in (ROOT / "docs").rglob("*.md"))
        self.assertEqual(sorted(paths), files)
        self.assertEqual(cr.check(reg, ROOT), [])

    def test_dump_round_trips(self):
        reg, sections = cr.build_registry(ROOT)
        import yaml
        self.assertEqual(yaml.safe_load(cr.dump_registry(reg, sections)), reg)

    def test_detects_missing_and_ghost_pages(self):
        reg = copy.deepcopy(self.reg)
        reg["pages"] = [e for e in reg["pages"] if e["path"] != "cau-hoi/tri-thuc.md"]
        self.assertError(reg, "cau-hoi/tri-thuc.md: có trong docs/ nhưng thiếu")
        reg = copy.deepcopy(self.reg)
        reg["pages"].append({"path": "cau-hoi/khong-co.md", "type": "cau-hoi", "tier": "loi", "block": "tri-thuc", "generated": False})
        self.assertError(reg, "không còn file docs/cau-hoi/khong-co.md")

    def test_detects_duplicates_bad_values_and_wrong_shape(self):
        reg = copy.deepcopy(self.reg)
        reg["pages"].append(copy.deepcopy(self.page(reg, "cau-hoi/tri-thuc.md")))
        self.assertError(reg, "đường dẫn trùng")
        reg = copy.deepcopy(self.reg)
        self.page(reg, "cau-hoi/tri-thuc.md")["tier"] = "lõi"
        self.assertError(reg, "tier 'lõi'")
        reg = copy.deepcopy(self.reg)
        self.page(reg, "cau-hoi/tri-thuc.md")["block"] = "nhan-thuc"
        self.assertError(reg, "không thuộc KE-HOACH.md mục 5.3")
        reg = copy.deepcopy(self.reg)
        del self.page(reg, "cau-hoi/tri-thuc.md")["generated"]
        self.assertError(reg, "thiếu ['generated']")

    def test_detects_rule_violations(self):
        reg = copy.deepcopy(self.reg)
        self.page(reg, "doc/luan-ngu.md")["type"] = "cau-hoi"
        self.assertError(reg, "theo thư mục phải là 'doc'")
        reg = copy.deepcopy(self.reg)
        self.page(reg, "them/du-lieu.md")["block"] = "luyen-tap"
        self.assertError(reg, "trang he-thong phải có tier: he-thong, block: null")
        reg = copy.deepcopy(self.reg)
        self.page(reg, "triet-gia/kant.md")["generated"] = False
        self.assertError(reg, "generated phải là true")
        reg = copy.deepcopy(self.reg)
        self.page(reg, "cau-hoi/tri-thuc.md")["block"] = "lich-su"
        self.assertError(reg, "phải thuộc một trong 11 khối chủ đề")

    def test_detects_unregistered_data_file(self):
        reg = copy.deepcopy(self.reg)
        reg["data"] = [e for e in reg["data"] if e["path"] != "docs/assets/data/terms.json"]
        self.assertError(reg, "docs/assets/data/terms.json: có trong docs/assets/data/ nhưng thiếu")



class TestFrontMatterSync(unittest.TestCase):
    def test_every_hand_written_page_carries_tier(self):
        reg = cr.load_registry(ROOT)
        for e in reg["pages"]:
            if e["generated"]:
                continue
            meta = cr.yaml.safe_load(cr.FRONT_MATTER.match((ROOT / "docs" / e["path"]).read_text(encoding="utf-8")).group(1))
            self.assertEqual({k: meta.get(k) for k in cr.frontmatter_fields(e)}, cr.frontmatter_fields(e), e["path"])

    def test_sync_only_touches_tier_and_block(self):
        import tempfile
        root = Path(tempfile.mkdtemp(prefix="registry-test-"))
        (root / "docs" / "cau-hoi").mkdir(parents=True)
        f = root / "docs" / "cau-hoi" / "x.md"
        f.write_text("---\ntitle: X\nupdated: 2026-10-22\ntier: mo-rong\n---\n\n# X\n", encoding="utf-8")
        reg = {"pages": [{"path": "cau-hoi/x.md", "type": "cau-hoi", "tier": "loi", "block": "tri-thuc", "generated": False},
                         {"path": "index.md", "type": "he-thong", "tier": "he-thong", "block": None, "generated": True}]}
        self.assertEqual(cr.sync_frontmatter(reg, root), 1)
        self.assertEqual(f.read_text(encoding="utf-8"),
                         "---\ntitle: X\nupdated: 2026-10-22\ntier: loi\nblock: tri-thuc\n---\n\n# X\n")
        self.assertEqual(cr.sync_frontmatter(reg, root), 0)
        self.assertEqual(cr.frontmatter_fields(reg["pages"][1]), {"tier": "he-thong"})

    def test_front_matter_block_mismatch_is_an_error(self):
        reg = copy.deepcopy(cr.load_registry(ROOT))
        e = self.page_entry(reg, "cau-hoi/tri-thuc.md")
        e["block"] = "tam-tri"
        self.assertTrue(any("front matter block" in x for x in cr.check(reg, ROOT)))

    def test_data_directory_entry(self):
        reg = copy.deepcopy(cr.load_registry(ROOT))
        e = next(x for x in reg["data"] if x["path"] == "data/people/")
        e["path"] = "data/khong-co/"
        errors = cr.check(reg, ROOT)
        self.assertTrue(any("data/khong-co/: không còn thư mục" in x for x in errors), errors)

    @staticmethod
    def page_entry(reg, path):
        return next(e for e in reg["pages"] if e["path"] == path)

if __name__ == "__main__":
    unittest.main()
