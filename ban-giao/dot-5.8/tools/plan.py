"""Chia các mục sửa thành lô ≤3 đơn vị: python plan.py trang1 trang2 ... -> in danh sách lô (JSON) vào lots.json"""
import json, sys
D = "/Users/mitu/Desktop/work/projects/logos/ban-giao/dot-5.8/sua/"
lots = []
for page in sys.argv[1:]:
    rows = json.load(open(D + page + ".json"))
    mp = json.load(open(D + page + ".map.json"))
    units = {}
    for m in mp:
        if m.get("applied"):
            units.setdefault(m["unit"], {"rows": set(), "claims": []})
            units[m["unit"]]["rows"].update(m["rows"]); units[m["unit"]]["claims"].append(m["claim_index"])
    keys = sorted(units)
    for i in range(0, len(keys), 3):
        ch = keys[i:i+3]
        rr = sorted(set().union(*[units[k]["rows"] for k in ch]))
        lots.append({"page": page, "units": {k: units[k]["claims"] for k in ch}, "rows": [rows[j] for j in rr]})
import os
json.dump(lots, open(D + os.environ.get("LOTS", "lots.json"), "w"), ensure_ascii=False, indent=1)
print(len(lots), "lô")
