"""Chuyển một lần (đợt 2, việc 2.2): philosophers.json + CONTENT trong tools/philosophers.py → data/kb/people.yml
và data/people/<id>.yml (quyết định 7). Giữ lại để biết dữ liệu đến từ đâu; chạy lại được vì đọc nguồn từ git.

    python tools/migrate/dot2_people.py [REV]    # REV mặc định 3be6485 (main trước việc 2.2)

Một–một, không đổi chữ: people.yml giữ đúng thứ tự của philosophers.json (thứ tự biên tập, hiện ở trang chỉ mục);
tuple của CONTENT (works, related, sources) thành ánh xạ có tên trường. Script tự kiểm đọc ngược ra đúng dữ liệu gốc.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
REV = sys.argv[1] if len(sys.argv) > 1 else "3be6485"


def git_show(path: str) -> str:
    return subprocess.run(["git", "show", f"{REV}:{path}"], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def old_content() -> dict:
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "philosophers_old.py"
        f.write_text(git_show("tools/philosophers.py"), encoding="utf-8")
        spec = importlib.util.spec_from_file_location("philosophers_old", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.CONTENT


def dump(obj) -> str:
    return yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=1_000_000, default_flow_style=False)


def person(p: dict) -> dict:
    return {"name": p["name"], "name_en": p["name_en"], "born": p["start"], "died": p["end"],
            "years_label": p["years"], "school": p["school"], "summary": p["summary"],
            "influence": p["influence"], "evidence": [], "verified": None}


def profile(c: dict) -> dict:
    out = {}
    for k, v in c.items():
        if k == "works":
            v = [{"year": y, "title": t, "note": n} for y, t, n in v]
        elif k == "related":
            v = [{"path": p, "title": t} for p, t in v]
        elif k == "sources":
            v = [{"text": t, "url": u} for t, u in v]
        out[k] = v
    return out


def main() -> int:
    data = json.loads(git_show("docs/assets/data/philosophers.json"))
    content = old_content()
    people = {p["id"]: person(p) for p in data}
    head = ("# Người có hồ sơ triết gia. Nguồn sự thật cho docs/assets/data/philosophers.json (sinh bởi tools/philosophers.py).\n"
            "# Thứ tự = thứ tự hiện ở trang chỉ mục. Schema: schema/kb/people.schema.json. Đặc tả: ban-giao/dot-2.md.\n")
    (ROOT / "data" / "kb").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "kb" / "people.yml").write_text(head + dump(people), encoding="utf-8")
    pdir = ROOT / "data" / "people"
    pdir.mkdir(parents=True, exist_ok=True)
    for pid in people:
        (pdir / f"{pid}.yml").write_text(
            f"# Hồ sơ {people[pid]['name']}: phần văn của docs/triet-gia/{pid}.md. Schema: schema/kb/person-profile.schema.json.\n"
            + dump(profile(content[pid])), encoding="utf-8")
    # đọc ngược
    back = yaml.safe_load((ROOT / "data" / "kb" / "people.yml").read_text(encoding="utf-8"))
    assert back == people and list(back) == [p["id"] for p in data]
    for pid in people:
        assert yaml.safe_load((pdir / f"{pid}.yml").read_text(encoding="utf-8")) == profile(content[pid]), pid
    print(f"Đã ghi data/kb/people.yml ({len(people)} người) và {len(people)} hồ sơ trong data/people/; đọc ngược khớp.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
