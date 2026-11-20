"""python mau_fix.py spec.json N : áp lô N; spec = [{"units":{unit:[mau_claim_idx...] hoặc {"copy_from":[unit_mau, idx]}}, "rows":[[p,o,n]]}]"""
import json, sys, subprocess
lot = json.load(open(sys.argv[1]))[int(sys.argv[2])]
for p, o, n in lot["rows"]:
    s = open(p).read(); assert s.count(o) == 1, (p, o[:50]); open(p, "w").write(s.replace(o, n))
fn = lambda d, u: f"verification/{d}/" + u.replace("/", "__").replace("#", "__") + ".json"
def h(u):
    out = subprocess.run(["uv","run","python","tools/check_ledger.py","--hash",u],capture_output=True,text=True).stdout
    return [x for x in out.split() if x.startswith("sha256:")][0]
for u, spec in lot["units"].items():
    hh = h(u)
    if isinstance(spec, list):  # mẫu có claim
        m = json.load(open(fn("mau/5.8", u))); new = []
        for i in spec:
            m["claims"][i]["fixed"] = True; new.append(m["claims"][i])
        m["hash"] = hh; m["notes"] = m.get("notes","") + " Sau mẫu: các claim sai đã sửa đúng fix trong bài (fixed), mã băm cập nhật."
        if m["result"] == "sua": m["result"] = "dat"
        open(fn("mau/5.8", u), "w").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
    else:
        mu, i = spec["copy_from"]; c = dict(json.load(open(fn("mau/5.8", mu)))["claims"][i]); c["fixed"] = True; c["text"] = spec["text"]; new = [c]
    e = json.load(open(fn("evidence", u)))
    for c in new:
        c = dict(c); c["fixed"] = True; e["claims"].append(c)
    e["hash"] = hh
    if "claude-sau-mau-5.8" not in e["checker"]: e["checker"] += " + claude-sau-mau-5.8"
    e["notes"] = e.get("notes","") + " Sau mẫu 5.8: thêm claim sai do kiểm mẫu tìm ra, đã sửa đúng fix (fixed)."
    open(fn("evidence", u), "w").write(json.dumps(e, ensure_ascii=False, indent=2) + "\n")
    print("ok", u)
