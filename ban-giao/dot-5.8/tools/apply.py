"""Áp lô thứ N của lots.json: sửa trang, đặt fixed:true cho claim. python apply.py N"""
import json, sys, glob
import os as _os
import tempfile as _tf
if _os.path.exists(_os.path.join(_tf.gettempdir(), "logos-5.8-STOP")): sys.exit("STOP: dừng trước lô mới")
D = "/Users/mitu/Desktop/work/projects/logos/ban-giao/dot-5.8/sua/"
import os
lot = json.load(open(D + os.environ.get("LOTS", "lots.json")))[int(sys.argv[1])]
for p, old, new in lot["rows"]:
    s = open(p, encoding="utf-8").read(); n = s.count(old)
    assert n == 1, (p, old[:60], n)
    open(p, "w", encoding="utf-8").write(s.replace(old, new))
for unit, idxs in lot["units"].items():
    f = "verification/evidence/" + unit.replace("/", "__").replace("#", "__") + ".json"
    e = json.load(open(f))
    for i in idxs:
        assert e["claims"][i]["verdict"] == "sai"; e["claims"][i]["fixed"] = True
    open(f, "w", encoding="utf-8").write(json.dumps(e, ensure_ascii=False, indent=2) + "\n")
print("áp", lot["page"], list(lot["units"]), len(lot["rows"]), "mục")
