"""Cập nhật bằng chứng + sổ cho đơn vị frozen sửa theo [doi-loi].
python doiloi.py spec.json ; spec = [{"key":..., "replace": {"<chuỗi trong text claim cũ>": {claim mới}}, "add":[claims], "note": "..."}]"""
import json, subprocess, sys
from pathlib import Path
CHECKER = "claude-doi-loi-5.9"
DAY = "2026-11-20"
spec = json.load(open(sys.argv[1]))
L = json.load(open("verification/ledger.json"))
units = L.get("units", L)
for s in spec:
    k = s["key"]
    h = subprocess.run(["uv", "run", "python", "tools/check_ledger.py", "--hash", k], capture_output=True, text=True).stdout.split()
    h = [x for x in h if x.startswith("sha256:")][0]
    ev = units[k]["evidence"]
    e = json.load(open(ev))
    for old, new in s.get("replace", {}).items():
        idx = [i for i, c in enumerate(e["claims"]) if old in c["text"]]
        assert len(idx) == 1, (k, old, idx)
        e["claims"][idx[0]] = new
    e["claims"] += s.get("add", [])
    e["hash"] = h
    e["checked_on"] = DAY
    if CHECKER not in e["checker"]:
        e["checker"] += " + " + CHECKER
    e["notes"] = (e.get("notes", "") + " [doi-loi] " + s["note"]).strip()
    Path(ev).write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    u = units[k]
    u["hash"] = h; u["verified_on"] = DAY
    if CHECKER not in u["checker"]:
        u["checker"] += "; " + CHECKER
    print(k, h[:20])
Path("verification/ledger.json").write_text(json.dumps(L, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
