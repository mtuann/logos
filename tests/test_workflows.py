"""File workflow GitHub Actions đọc được bằng YAML (lỗi cú pháp làm CI hỏng ngay, không chạy bước nào).
Chạy: python -m unittest discover -s tests"""

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


class TestWorkflows(unittest.TestCase):
    def test_workflows_parse(self):
        files = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
        self.assertTrue(files)
        for f in files:
            with self.subTest(f.name):
                doc = yaml.safe_load(f.read_text(encoding="utf-8"))
                self.assertIn("jobs", doc)
                for job in doc["jobs"].values():
                    for step in job.get("steps", []):
                        self.assertIsInstance(step.get("name", ""), str)


if __name__ == "__main__":
    unittest.main()
