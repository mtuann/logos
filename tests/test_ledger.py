"""tools/check_ledger.py: sổ kiểm chứng verification/ledger.json. Chạy: python -m unittest discover -s tests"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import check_ledger as cl  # noqa: E402
from lz import hashing  # noqa: E402

PAGE = "---\ntitle: X\n---\n\n# X\n\nMở đầu.\n\n## Nguồn {#nguon}\n\n1. SEP\n"
KEY = "cau-hoi/x.md#nguon"


class TestLedger(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="ledger-test-"))
        (self.root / "schema").mkdir()
        shutil.copy(ROOT / cl.SCHEMA, self.root / cl.SCHEMA)
        (self.root / "docs" / "cau-hoi").mkdir(parents=True)
        (self.root / "docs" / "cau-hoi" / "x.md").write_text(PAGE, encoding="utf-8")
        (self.root / "verification" / "evidence").mkdir(parents=True)
        cl._page_units.cache_clear()
        self.hash = hashing.unit_hash("## Nguồn {#nguon}\n\n1. SEP\n")
        self.evidence = cl.evidence_path(KEY)
        (self.root / self.evidence).write_text(json.dumps({"unit": KEY, "hash": self.hash}), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def ledger(self, **entry):
        e = {"status": "frozen", "hash": self.hash, "verified_on": "2027-01-12",
             "checker": "agent", "evidence": self.evidence, **entry}
        return {"version": 1, "units": {KEY: {k: v for k, v in e.items() if v is not None}}}

    def edit_page(self):
        (self.root / "docs" / "cau-hoi" / "x.md").write_text(PAGE.replace("SEP", "IEP"), encoding="utf-8")
        cl._page_units.cache_clear()

    def test_repo_ledger_is_valid(self):
        cl._page_units.cache_clear()
        self.assertEqual(cl.check(cl.load(ROOT), ROOT), ([], []))

    def test_frozen_unchanged_passes(self):
        self.assertEqual(cl.check(self.ledger(), self.root), ([], []))
        self.assertEqual(cl.current_hash(KEY, self.root), self.hash)

    def test_frozen_changed_blocks_unless_allowed(self):
        self.edit_page()
        errors, _ = cl.check(self.ledger(), self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("đã đóng băng", errors[0])
        errors, warnings = cl.check(self.ledger(), self.root, allow_core_change=True)
        self.assertEqual(errors, [])
        self.assertIn(cl.ALLOW_ENV, warnings[0])

    def test_unfrozen_change_only_warns(self):
        self.edit_page()
        errors, warnings = cl.check(self.ledger(status="chua-kiem", verified_on=None, checker=None, evidence=None),
                                    self.root)
        self.assertEqual(errors, [])
        self.assertIn("cần kiểm lại", warnings[0])

    def test_missing_unit_or_page(self):
        led = self.ledger()
        led["units"]["cau-hoi/x.md#khong-co"] = led["units"].pop(KEY)
        self.assertIn("không còn mục #khong-co", cl.check(led, self.root)[0][0])
        led = self.ledger()
        led["units"]["cau-hoi/y.md#nguon"] = led["units"].pop(KEY)
        self.assertIn("không còn trang", cl.check(led, self.root)[0][0])

    def test_schema_violations(self):
        cases = {
            "status 'xong' ngoài": self.ledger(status="xong"),
            "thiếu 'evidence'": self.ledger(evidence=None),
            "trường thừa 'by'": self.ledger(by="x"),
            "hash 'abc' sai mẫu": self.ledger(hash="abc"),
            "verified_on '12/1/2027' sai mẫu": self.ledger(verified_on="12/1/2027"),
        }
        for needle, led in cases.items():
            errors = cl.validate(led, cl.load_schema(self.root))
            self.assertTrue(any(needle in e for e in errors), f"{needle!r} không có trong {errors}")
        self.assertEqual(cl.validate({"version": 1, "units": {"Sai Khoa": {}}}, cl.load_schema(self.root))[0],
                         "sổ: Sai Khoa: khóa sai mẫu")

    def test_evidence_must_match(self):
        (self.root / self.evidence).write_text(json.dumps({"unit": "khac.md#a", "hash": "sha256:" + "0" * 64}),
                                               encoding="utf-8")
        errors, _ = cl.check(self.ledger(), self.root)
        self.assertTrue(any("ghi unit 'khac.md#a'" in e for e in errors))
        self.assertTrue(any("mã băm trong bằng chứng" in e for e in errors))
        (self.root / self.evidence).unlink()
        self.assertIn("không thấy file bằng chứng", cl.check(self.ledger(), self.root)[0][0])

    def test_evidence_path(self):
        self.assertEqual(cl.evidence_path("cau-hoi/tri-thuc.md#cac-lap-truong-chinh"),
                         "verification/evidence/cau-hoi__tri-thuc.md__cac-lap-truong-chinh.json")

    def test_data_records_not_yet_supported(self):
        with self.assertRaises(KeyError):
            cl.current_hash("people/kant", self.root)


class TestStatus(unittest.TestCase):
    def test_status_counts_core_units(self):
        cl._page_units.cache_clear()
        table = cl.status_table({"version": 1, "units": {}}, ROOT)
        self.assertIn("| **Tổng Lõi** | 987 | 987 | 0 | 0 | 0 | 0,0 |", table)


if __name__ == "__main__":
    unittest.main()
