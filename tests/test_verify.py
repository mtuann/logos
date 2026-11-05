"""tools/verify.py: công cụ đợt con của đợt 5 (ban-giao/dot-5.md, việc 5.0c). Chạy: python -m unittest discover -s tests"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import check_ledger as cl  # noqa: E402
import verify  # noqa: E402

PAGE = "---\ntitle: Biện hộ\n---\n\n# Biện hộ\n\nMở đầu.\n\n## Bối cảnh {#boi-canh}\n\nNăm 399 TCN.\n"
REGISTRY = """pages:
  - {path: doc/x.md, type: doc, tier: loi, block: van-ban, generated: false}
  - {path: doc/y.md, type: doc, tier: mo-rong, block: van-ban, generated: false}
data: []
"""
SRC = [{"url": "https://plato.stanford.edu/archives/fall2026/entries/plato/", "quote": "399 BCE"}]
CHECKLIST = {"dung-nguon": True, "manh-nhat": True, "phan-bac": None, "trung-lap": True, "thuat-ngu": True}


class Base(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="verify-test-"))
        r = self.root
        (r / "schema").mkdir()
        for s in (cl.SCHEMA, cl.EVIDENCE_SCHEMA):
            shutil.copy(ROOT / s, r / s)
        (r / "docs" / "doc").mkdir(parents=True)
        (r / "docs" / "doc" / "x.md").write_text(PAGE, encoding="utf-8")
        (r / "docs" / "doc" / "y.md").write_text(PAGE, encoding="utf-8")
        (r / "content.yml").write_text(REGISTRY, encoding="utf-8")
        (r / "data" / "kb").mkdir(parents=True)
        (r / "data" / "kb" / "people.yml").write_text(
            "".join(f"p{i}: {{name: Người {i}, born: {1700 + i}}}\n" for i in range(25)), encoding="utf-8")
        (r / "data" / "kb" / "works.yml").write_text("w1: {title: Tác phẩm}\n", encoding="utf-8")
        (r / "verification" / "evidence").mkdir(parents=True)
        (r / cl.LEDGER).write_text('{"version": 1, "units": {}}\n', encoding="utf-8")
        cl._page_units.cache_clear()
        cl._load_yaml.cache_clear()
        self.addCleanup(shutil.rmtree, r)
        self.addCleanup(cl._load_yaml.cache_clear)
        self.addCleanup(cl._page_units.cache_clear)

    def evidence(self, key, *, path=None, **over):
        doc = {"unit": key, "hash": cl.current_hash(key, self.root), "checked_on": "2027-01-05", "checker": "agent-kiem-1",
               "claims": [{"text": "Năm 399 TCN", "kind": "du-kien", "verdict": "dung", "sources": SRC}],
               "result": "dat"}
        if "#" in key:
            doc["checklist"] = CHECKLIST
        doc.update(over)
        p = path or self.root / cl.evidence_path(key)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        return p

    def ledger(self):
        return cl.load(self.root)["units"]


class TestScope(Base):
    def test_scope_records_and_core_pages_only(self):
        self.assertEqual(verify.scope("5.4", self.root), ["doc/x.md#_dau", "doc/x.md#boi-canh"])  # doc/y.md là mo-rong
        keys = verify.scope("5.1", self.root)
        self.assertEqual(len(keys), 26)
        self.assertIn("works/w1", keys)
        with self.assertRaises(SystemExit):
            verify.scope("5.9", self.root)

    def test_real_repo_scope_sizes(self):
        cl._page_units.cache_clear()
        cl._load_yaml.cache_clear()
        sizes = {d: len(verify.scope(d, ROOT)) for d in verify.DOT_CON}
        self.assertEqual(sum(sizes[d] for d in ("5.4", "5.6", "5.7", "5.8")) + 171, 987)   # 171 đơn vị cong-cu ở 5.5
        self.assertEqual(sizes["5.7"], 253)
        self.assertEqual(sizes["5.8"], 299)


class TestLedgerFlow(Base):
    def test_ghi_so_adds_then_refreshes_unchecked_hash(self):
        self.assertEqual(verify.ghi_so("5.4", self.root), (2, 0, []))
        self.assertEqual(self.ledger()["doc/x.md#boi-canh"]["status"], "chua-kiem")
        (self.root / "docs/doc/x.md").write_text(PAGE.replace("399", "400"), encoding="utf-8")
        cl._page_units.cache_clear()
        self.assertEqual(verify.ghi_so("5.4", self.root), (0, 1, []))

    def test_ghi_so_resets_checked_unit_that_changed(self):
        verify.ghi_so("5.4", self.root)
        key = "doc/x.md#boi-canh"
        self.evidence(key)
        verify.ghi([key], self.root)
        (self.root / "docs/doc/x.md").write_text(PAGE.replace("399", "400"), encoding="utf-8")
        cl._page_units.cache_clear()
        self.assertEqual(verify.ghi_so("5.4", self.root)[1], 1)
        self.assertEqual(self.ledger()[key], {"status": "chua-kiem", "hash": cl.current_hash(key, self.root)})

    def test_ghi_so_drops_vanished_records(self):
        verify.ghi_so("5.1", self.root)
        (self.root / "data/kb/works.yml").write_text("w2: {title: Khác}\n", encoding="utf-8")
        cl._load_yaml.cache_clear()
        self.assertEqual(verify.ghi_so("5.1", self.root), (1, 0, ["works/w1"]))
        self.assertNotIn("works/w1", self.ledger())
        self.assertEqual(cl.check(cl.load(self.root), self.root), ([], []))

    def test_ghi_requires_good_evidence(self):
        verify.ghi_so("5.4", self.root)
        key = "doc/x.md#boi-canh"
        done, fail = verify.ghi([key], self.root)
        self.assertIn("không thấy", fail[key][0])
        self.evidence(key, result="sua")
        self.assertIn("result là 'sua'", verify.ghi([key], self.root)[1][key][0])
        self.evidence(key, claims=[{"text": "Năm 399 TCN", "kind": "du-kien", "verdict": "sai", "severity": "nghiem-trong",
                                    "fix": "Năm 399 TCN", "sources": SRC}])
        self.assertIn("chưa sửa", verify.ghi([key], self.root)[1][key][0])
        self.evidence(key, checklist=None)
        self.assertTrue(verify.ghi([key], self.root)[1][key][0].startswith("schema:"))
        self.evidence(key, hash="sha256:" + "0" * 64)
        self.assertIn("khác mã băm hiện tại", verify.ghi([key], self.root)[1][key][0])
        # Claim sai đã sửa (fixed) hoặc mức nhẹ thì vẫn đạt.
        self.evidence(key, claims=[{"text": "x", "kind": "du-kien", "verdict": "sai", "severity": "vua", "fix": "y",
                                    "fixed": True, "sources": SRC},
                                   {"text": "z", "kind": "dien-giai", "verdict": "sai", "severity": "nhe", "fix": "w",
                                    "sources": SRC}])
        done, fail = verify.ghi([key], self.root)
        self.assertEqual((done, fail), ([key], {}))
        e = self.ledger()[key]
        self.assertEqual((e["status"], e["checker"], e["verified_on"]), ("da-kiem", "agent-kiem-1", "2027-01-05"))
        self.assertEqual(cl.check(cl.load(self.root), self.root), ([], []))

    def test_dung_claim_needs_source_or_kb(self):
        verify.ghi_so("5.1", self.root)
        self.evidence("people/p1", claims=[{"text": "sinh 1701", "kind": "du-kien", "verdict": "dung"}])
        self.assertTrue(verify.ghi(["people/p1"], self.root)[1]["people/p1"][0].startswith("schema:"))
        self.evidence("people/p1", claims=[{"text": "sinh 1701", "kind": "du-kien", "verdict": "dung", "kb": "works/w1"}])
        self.assertEqual(verify.ghi(["people/p1"], self.root)[0], ["people/p1"])

    def test_check_ledger_rejects_bad_evidence_schema(self):
        verify.ghi_so("5.4", self.root)
        key = "doc/x.md#boi-canh"
        p = self.evidence(key)
        verify.ghi([key], self.root)
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["claims"][0]["verdict"] = "co-le"
        p.write_text(json.dumps(doc), encoding="utf-8")
        errors, _ = cl.check(cl.load(self.root), self.root)
        self.assertTrue(any("sai schema" in e for e in errors), errors)


class TestSampleAndFreeze(Base):
    def test_sample_is_deterministic_and_sized(self):
        self.assertEqual(verify.sample_size(26), 3)
        self.assertEqual(verify.sample_size(253), 26)
        self.assertEqual(verify.sample_size(2), 2)
        a = verify.chon_mau("5.1", self.root)
        self.assertEqual(a, verify.chon_mau("5.1", self.root))
        self.assertEqual(len(a), 3)
        state = verify.mau("5.1", self.root, today="2027-01-08")
        (self.root / "data/kb/people.yml").write_text("p99: {name: X}\n" * 1, encoding="utf-8")
        cl._load_yaml.cache_clear()
        self.assertEqual(verify.mau("5.1", self.root)["sample"], state["sample"])     # chọn một lần
        self.assertTrue((self.root / "verification/mau/5.1.md").exists())

    def _all_checked(self):
        verify.ghi_so("5.1", self.root)
        for k in verify.scope("5.1", self.root):
            self.evidence(k)
        done, fail = verify.ghi(verify.scope("5.1", self.root), self.root)
        self.assertEqual(fail, {})

    def test_freeze_needs_passing_sample(self):
        self._all_checked()
        with self.assertRaises(SystemExit):
            verify.dong_bang("5.1", "2027-01-10", self.root)          # chưa có mẫu
        state = verify.mau("5.1", self.root)
        r = verify.so_mau("5.1", self.root)["result"]
        self.assertEqual((r["checked"], r["pass"], len(r["missing"])), (0, False, 3))
        bad = state["sample"][0]
        for k in state["sample"]:
            claims = [{"text": "sinh 1701", "kind": "du-kien", "verdict": "sai", "severity": "nghiem-trong", "fix": "1702",
                       "sources": SRC}] if k == bad else [{"text": "ok", "kind": "du-kien", "verdict": "dung", "sources": SRC}]
            self.evidence(k, path=verify.mau_evidence_path("5.1", k, self.root), checker="agent-kiem-2", claims=claims)
        r = verify.so_mau("5.1", self.root)["result"]
        self.assertEqual((r["missed_serious"], r["pass"]), ([bad], False))   # 1/3 > 2%
        with self.assertRaises(SystemExit):
            verify.dong_bang("5.1", "2027-01-10", self.root)
        self.evidence(bad, path=verify.mau_evidence_path("5.1", bad, self.root), checker="agent-kiem-2")
        self.assertTrue(verify.so_mau("5.1", self.root)["result"]["pass"])
        self.assertEqual(verify.dong_bang("5.1", "2027-01-10", self.root), 26)
        self.assertTrue(all(e["status"] == "frozen" for e in self.ledger().values()))
        self.assertIn("Chủ biên duyệt: 2027-01-10", (self.root / "verification/mau/5.1.md").read_text(encoding="utf-8"))
        self.assertEqual(cl.check(cl.load(self.root), self.root), ([], []))

    def test_freeze_refuses_changed_unit(self):
        self._all_checked()
        state = verify.mau("5.1", self.root)
        for k in state["sample"]:
            self.evidence(k, path=verify.mau_evidence_path("5.1", k, self.root))
        verify.so_mau("5.1", self.root)
        (self.root / "data/kb/works.yml").write_text("w1: {title: Tác phẩm khác}\n", encoding="utf-8")
        cl._load_yaml.cache_clear()
        with self.assertRaises(SystemExit) as cm:
            verify.dong_bang("5.1", "2027-01-10", self.root)
        self.assertIn("đổi mã băm", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
