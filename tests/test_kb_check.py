"""tools/kb_check.py: schema và tham chiếu chéo của kho dữ kiện. Chạy: python -m unittest discover -s tests"""

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import kb_check as kc  # noqa: E402

PERSON = {"name": "Immanuel Kant", "name_en": "Immanuel Kant", "born": 1724, "died": 1804, "years_label": "1724–1804",
          "school": "Cận đại", "summary": "Một dòng.", "influence": ["hume"], "evidence": [], "verified": None}
HUME = {**PERSON, "name": "David Hume", "name_en": "David Hume", "born": 1711, "died": 1776, "years_label": "1711–1776",
        "influence": []}
PROFILE = {"desc": "Mô tả.", "bio": ["Đoạn."], "works": [{"year": "1781", "title": "*Phê phán*", "note": ""}],
           "thoughts": ["Ý."], "argument": {"title": "T", "premises": ["P1"], "conclusion": "K"},
           "misread": [], "related": [{"path": "cau-hoi/x.md", "title": "X"}],
           "sources": [{"text": "SEP", "url": "https://plato.stanford.edu/entries/kant/"}]}
DATA = {
    "people": {"kant": PERSON, "hume": HUME},
    "works": {"kant.phe-phan-ly-tinh-thuan-tuy": {
        "author": "kant", "titles": ["Phê phán lý tính thuần túy"], "year": 1781,
        "years_seen": {"1781": ["cau-hoi/x.md#nguon"]}, "used_in": ["cau-hoi/x.md#nguon"], "evidence": ["sep.kant"],
        "verified": None}},
    "quotes": {"kant.phe-phan-ly-tinh-thuan-tuy.a51": {
        "work": "kant.phe-phan-ly-tinh-thuan-tuy", "locator": "A51/B75", "title": "Kant", "original": "…",
        "translation": "…", "translator": "logos-zero", "license": "public-domain", "used_in": ["people/kant"],
        "evidence": [], "verified": None}},
    "events": {"dai-viet.khoa-thi-1075": {"year": 1075, "text": "khoa thi", "certainty": "chac-chan",
                                          "used_in": ["cau-hoi/x.md#_dau"], "evidence": [], "verified": None}},
    "sources": {"sep.kant": {"type": "sep", "text": "SEP, Kant", "url": "https://plato.stanford.edu/entries/kant/",
                             "archive": "https://plato.stanford.edu/archives/fall2026/entries/kant/",
                             "accessed": "2026-11-05", "used_in": ["cau-hoi/x.md#nguon"]}},
    "philpapers": {"source": {"preamble": "", "footer": ""}, "questions": [{"id": "free-will", "table": 1, "n": 1770,
                                                "options": [{"id": "compatibilism", "pct": 59.2}]}]},
}


class TestKbCheck(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="kb-test-"))
        shutil.copytree(ROOT / kc.SCHEMAS, self.root / kc.SCHEMAS)
        (self.root / "docs" / "cau-hoi").mkdir(parents=True)
        (self.root / "docs" / "cau-hoi" / "x.md").write_text("# X\n\n## Nguồn {#nguon}\n\n1. A\n", encoding="utf-8")
        self.write(DATA, {"kant": PROFILE, "hume": PROFILE})

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def write(self, data, profiles=None):
        for kind, d in data.items():
            f = self.root / kc.FILES[kind][0]
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps(d, ensure_ascii=False) if f.suffix == ".json"
                         else yaml.safe_dump(d, allow_unicode=True), encoding="utf-8")
        for pid, prof in (profiles or {}).items():
            f = self.root / kc.PEOPLE_DIR / f"{pid}.yml"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(yaml.safe_dump(prof, allow_unicode=True), encoding="utf-8")

    def errors(self):
        return kc.check(self.root)[0]

    def assertError(self, needle):
        errs = self.errors()
        self.assertTrue(any(needle in e for e in errs), f"không thấy {needle!r} trong {errs}")

    def test_valid_sample_passes(self):
        errs, counts = kc.check(self.root)
        self.assertEqual(errs, [])
        self.assertEqual(counts, {"people": 2, "works": 1, "quotes": 1, "events": 1, "sources": 1, "philpapers": 1,
                                  "people-profiles": 2})

    def test_repo_kb_is_valid(self):
        self.assertEqual(kc.check(ROOT)[0], [])

    def test_schema_violations(self):
        d = copy.deepcopy(DATA)
        d["people"]["kant"]["school"] = "Hậu hiện đại"
        d["people"]["kant"]["born"] = "1724"
        d["sources"]["sep.kant"].pop("accessed")
        d["events"]["Sai Khoa"] = d["events"]["dai-viet.khoa-thi-1075"]
        self.write(d)
        for needle in ("people.yml: kant/school", "people.yml: kant/born", "sources.yml: sep.kant: 'accessed' is a required",
                       "events.yml: (gốc): 'Sai Khoa' does not match"):
            self.assertError(needle)

    def test_cross_references(self):
        d = copy.deepcopy(DATA)
        d["people"]["kant"]["influence"] = ["leibniz"]
        d["works"]["kant.phe-phan-ly-tinh-thuan-tuy"]["author"] = "khong-co"
        d["quotes"]["kant.phe-phan-ly-tinh-thuan-tuy.a51"]["work"] = "kant.khong-co"
        d["works"]["kant.phe-phan-ly-tinh-thuan-tuy"]["evidence"] = ["sep.khong-co"]
        d["events"]["dai-viet.khoa-thi-1075"]["used_in"] = ["cau-hoi/x.md#khong-co", "cau-hoi/y.md#a", "people/khong-co"]
        self.write(d)
        for needle in ("influence 'leibniz'", "author 'khong-co'", "work 'kant.khong-co'", "evidence 'sep.khong-co'",
                       "trang không có mục #khong-co", "không có trang docs/cau-hoi/y.md", "used_in people/khong-co"):
            self.assertError(needle)

    def test_author_may_be_unknown(self):
        # Không đoán tác giả: author null hợp lệ (khóa chua-ro.*), gán ở đợt 5.
        d = copy.deepcopy(DATA)
        d["works"]["kant.phe-phan-ly-tinh-thuan-tuy"]["author"] = None
        self.write(d)
        self.assertEqual(self.errors(), [])

    def test_duplicate_yaml_key(self):
        f = self.root / kc.FILES["people"][0]
        f.write_text(f.read_text(encoding="utf-8") + "kant:\n  name: X\n", encoding="utf-8")
        self.assertError("khóa trùng 'kant'")

    def test_profiles_one_to_one_and_related(self):
        (self.root / kc.PEOPLE_DIR / "hume.yml").unlink()
        bad = copy.deepcopy(PROFILE)
        bad["related"] = [{"path": "cau-hoi/khong-co.md", "title": "?"}]
        bad.pop("sources")
        self.write({}, {"platon": PROFILE, "kant": bad})
        for needle in ("thiếu hồ sơ hume.yml", "data/people/platon.yml: không có 'platon'",
                       "related 'cau-hoi/khong-co.md'", "'sources' is a required property"):
            self.assertError(needle)

    def test_philpapers_duplicates(self):
        d = copy.deepcopy(DATA)
        q = d["philpapers"]["questions"][0]
        q["options"].append({"id": "compatibilism", "pct": 1.0})
        d["philpapers"]["questions"].append(copy.deepcopy(q))
        self.write(d)
        self.assertError("câu 'free-will' trùng")
        self.assertError("lựa chọn 'compatibilism' trùng")

    def test_philpapers_survey_from_preamble(self):
        d = copy.deepcopy(DATA)
        d["philpapers"]["source"]["preamble"] = "1.785 triết gia; 100 câu hỏi"
        d["philpapers"]["source"]["survey"] = {"nguoi-tra-loi": 1785, "so-cau": 100, "cau-chinh": 41,
                                               "cau-bo-sung": 100, "cau-bo-sung-moi-nguoi": 1785}
        self.write(d)
        self.assertError("source.survey.cau-chinh = 41 không có trong source.preamble")


if __name__ == "__main__":
    unittest.main()
