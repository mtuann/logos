"""Công cụ đợt con của đợt 5: phạm vi, ghi sổ, kiểm mẫu, đóng băng (ban-giao/dot-5.md, việc 5.0c).

    python tools/verify.py --pham-vi 5.1               # khóa đơn vị và bản ghi của đợt con
    python tools/verify.py --ghi-so 5.1                # ghi khóa chưa có vào sổ (chua-kiem, mã băm hiện tại)
    python tools/verify.py --ghi KHÓA…                 # bằng chứng hợp lệ, result dat → da-kiem
    python tools/verify.py --ghi-dot 5.1               # như --ghi cho mọi khóa của đợt con đã có bằng chứng đạt
    python tools/verify.py --tien-do 5.1               # đếm theo trạng thái; liệt kê khóa còn việc
    python tools/verify.py --mau 5.1                   # chọn mẫu 10% cố định → verification/mau/5.1.json + .md
    python tools/verify.py --so-mau 5.1                # đọc bằng chứng mẫu, tính tỉ lệ lỗi nghiêm trọng bị bỏ sót
    python tools/verify.py --dong-bang 5.1 --chu-bien-duyet 2027-01-10   # da-kiem → frozen

Bằng chứng: verification/evidence/<khóa>.json (ban-giao/kiem-chung.md, schema/evidence.schema.json).
Bằng chứng mẫu (agent kiểm thứ hai, không thấy bằng chứng gốc): verification/mau/5.N/<khóa>.json, cùng schema.

Một bằng chứng "đạt" để ghi da-kiem khi: đúng schema; `unit` là khóa; `hash` bằng mã băm hiện tại; `result` là
`dat`; không còn claim `chua-kiem-duoc`; mọi claim `sai` có mức `nhe` hoặc đã sửa (`fixed: true`); đơn vị trang
có `checklist`.

Mẫu: 10% số khóa của đợt con (làm tròn lên, ít nhất 3), chọn bằng random.Random("<đợt con>") trên danh sách khóa
đã sắp xếp, nên ai chạy cũng ra cùng mẫu. Chọn một lần; chạy lại không chọn lại. Một khóa trong mẫu tính là "lỗi
nghiêm trọng bị bỏ sót" khi bằng chứng mẫu có claim `sai` mức `nghiem-trong` chưa sửa. Cổng: tỉ lệ ≤ 2%
(KE-HOACH.md mục 7.4).
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from datetime import date
from pathlib import Path

import jsonschema

import check_ledger as cl
from lz import ROOT, registry, units

EVIDENCE_SCHEMA = cl.EVIDENCE_SCHEMA
MAU_DIR = Path("verification") / "mau"
NGUONG = 0.02   # KE-HOACH.md mục 7.4

# Đợt con → (loại bản ghi, khối trang Lõi). Theo ban-giao/dot-5.md bảng Việc.
DOT_CON: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "5.1": (("people", "works"), ()),
    "5.2": (("quotes", "events", "sources", "philpapers"), ()),
    "5.3": (("ho-so", "terms"), ()),
    "5.4": ((), ("van-ban",)),
    "5.5": (("fallacy-types", "fallacies", "lap-luan", "logic", "thi-nghiem"), ("cong-cu",)),
    "5.6": ((), ("lich-su", "bat-dau")),
    "5.7": ((), ("tri-thuc", "tam-tri", "tu-do", "dao-duc", "luan-ly-ung-dung")),
    "5.8": ((), ("chinh-tri", "my-hoc", "ton-giao", "sieu-hinh", "y-nghia", "viet-nam")),
}


# ---------------------------------------------------------------- phạm vi

def record_keys(kind: str, root: Path = ROOT) -> list[str]:
    if kind in cl.RECORD_FILES:
        return [f"{kind}/{k}" for k in (cl._load_yaml(cl.RECORD_FILES[kind], root) or {})]
    if kind == "ho-so":
        return [f"ho-so/{p.stem}" for p in sorted((root / "data" / "people").glob("*.yml"))]
    if kind == "philpapers":
        f = root / "data" / "kb" / "philpapers-2020.json"
        return [f"philpapers/{q['id']}" for q in json.loads(f.read_text(encoding="utf-8"))["questions"]]
    if kind in cl.JSON_RECORDS:
        rel, list_key = cl.JSON_RECORDS[kind]
        return [f"{kind}/{k}" for k in (cl._load_json_list(rel, list_key, root) or {})]
    raise KeyError(kind)


def scope(dot: str, root: Path = ROOT) -> list[str]:
    """Mọi khóa của đợt con, theo thứ tự: bản ghi theo loại, rồi đơn vị trang theo thứ tự `content.yml`."""
    if dot not in DOT_CON:
        raise SystemExit(f"đợt con {dot!r} không có (có: {', '.join(DOT_CON)})")
    kinds, blocks = DOT_CON[dot]
    keys = [k for kind in kinds for k in record_keys(kind, root)]
    for p in registry.load(root).select(tier="loi", generated=False):
        if p.block in blocks:
            keys += [u.key for u in units.split_file(p.path, root)]
    return keys


# ---------------------------------------------------------------- sổ

def save_ledger(ledger: dict, root: Path = ROOT) -> None:
    ledger["units"] = dict(sorted(ledger["units"].items()))
    (root / cl.LEDGER).write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ghi_so(dot: str, root: Path = ROOT) -> tuple[int, int, list[str]]:
    """Thêm khóa chưa có (chua-kiem). Khóa chua-kiem đã có thì cập nhật mã băm. Khóa của đợt con (cùng loại bản ghi
    hoặc cùng trang) không còn ứng với bản ghi nào (bản ghi rút nhầm bị bỏ, tác phẩm đổi khóa) thì bỏ khỏi sổ, trừ
    khóa đã đóng băng (check_ledger báo lỗi cho khóa đó). File bằng chứng cũ giữ nguyên. Trả (thêm, cập nhật, bỏ)."""
    ledger = cl.load(root)
    added = updated = 0
    keys = scope(dot, root)
    kinds, blocks = DOT_CON[dot]
    pages = {p.path for p in registry.load(root).select(tier="loi", generated=False) if p.block in blocks}
    live = set(keys)
    dropped = [k for k, e in ledger["units"].items()
               if k not in live and e["status"] != "frozen"
               and (k.split("/", 1)[0] in kinds or k.split("#", 1)[0] in pages)]
    for k in dropped:
        del ledger["units"][k]
    for key in keys:
        h = cl.current_hash(key, root)
        e = ledger["units"].get(key)
        if e is None:
            ledger["units"][key] = {"status": "chua-kiem", "hash": h}
            added += 1
        elif e["status"] == "chua-kiem" and e["hash"] != h:
            e["hash"] = h
            updated += 1
    save_ledger(ledger, root)
    return added, updated, dropped


# ---------------------------------------------------------------- bằng chứng

def load_evidence_schema(root: Path = ROOT) -> dict:
    return json.loads((root / EVIDENCE_SCHEMA).read_text(encoding="utf-8"))


def schema_errors(doc: object, schema: dict) -> list[str]:
    v = jsonschema.Draft202012Validator(schema)
    return [f"{'/'.join(map(str, e.absolute_path)) or '(gốc)'}: {e.message}"
            for e in sorted(v.iter_errors(doc), key=lambda e: list(map(str, e.absolute_path)))]


def evidence_problems(key: str, path: Path, root: Path = ROOT, schema: dict | None = None) -> list[str]:
    """Lý do bằng chứng chưa đủ để ghi da-kiem (rỗng = đạt)."""
    if not path.exists():
        return [f"không thấy {path.relative_to(root)}"]
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"JSON không hợp lệ ({exc})"]
    errs = schema_errors(doc, schema or load_evidence_schema(root))
    if errs:
        return ["schema: " + e for e in errs]
    out = []
    if doc["unit"] != key:
        out.append(f"unit là {doc['unit']!r}, không phải {key!r}")
    now = cl.current_hash(key, root)
    if doc["hash"] != now:
        out.append(f"hash {str(doc['hash'])[:15]}… khác mã băm hiện tại {now[:15]}…: kiểm lại phiên bản hiện tại")
    if doc["result"] != "dat":
        out.append(f"result là {doc['result']!r}")
    for i, c in enumerate(doc["claims"]):
        if c["verdict"] == "chua-kiem-duoc":
            out.append(f"claim {i}: chưa kiểm được")
        elif c["verdict"] == "sai" and c["severity"] != "nhe" and not c.get("fixed"):
            out.append(f"claim {i}: sai ({c['severity']}), chưa sửa")
    if "#" in key and "checklist" not in doc:
        out.append("đơn vị trang thiếu checklist")
    return out


def ghi(keys: list[str], root: Path = ROOT) -> tuple[list[str], dict[str, list[str]]]:
    """Ghi da-kiem cho khóa có bằng chứng đạt. Trả (đã ghi, {khóa: lý do chưa ghi})."""
    ledger = cl.load(root)
    schema = load_evidence_schema(root)
    done, fail = [], {}
    for key in keys:
        e = ledger["units"].get(key)
        if e is None:
            fail[key] = ["chưa có trong sổ (chạy --ghi-so)"]
            continue
        if e["status"] == "frozen":
            fail[key] = ["đã đóng băng"]
            continue
        rel = cl.evidence_path(key)
        probs = evidence_problems(key, root / rel, root, schema)
        if probs:
            fail[key] = probs
            continue
        doc = json.loads((root / rel).read_text(encoding="utf-8"))
        e.update(status="da-kiem", hash=doc["hash"], verified_on=doc["checked_on"], checker=doc["checker"],
                 evidence=rel)
        done.append(key)
    save_ledger(ledger, root)
    return done, fail


# ---------------------------------------------------------------- mẫu

def mau_path(dot: str, root: Path = ROOT) -> Path:
    return root / MAU_DIR / f"{dot}.json"


def mau_evidence_path(dot: str, key: str, root: Path = ROOT) -> Path:
    return root / MAU_DIR / dot / Path(cl.evidence_path(key)).name


def sample_size(n: int) -> int:
    return min(n, max(3, math.ceil(n / 10)))


def chon_mau(dot: str, root: Path = ROOT) -> list[str]:
    keys = sorted(scope(dot, root))
    return sorted(random.Random(dot).sample(keys, sample_size(len(keys))))


def mau(dot: str, root: Path = ROOT, today: str | None = None) -> dict:
    """Chọn mẫu (một lần) và ghi file trạng thái. Chạy lại thì giữ mẫu cũ."""
    p = mau_path(dot, root)
    if p.exists():
        state = json.loads(p.read_text(encoding="utf-8"))
    else:
        state = {"dot": dot, "chosen_on": today or date.today().isoformat(), "sample": chon_mau(dot, root),
                 "result": None, "chu_bien_duyet": None}
    write_mau(state, root)
    return state


def so_mau(dot: str, root: Path = ROOT) -> dict:
    """Đọc bằng chứng mẫu; ghi kết quả vào file trạng thái."""
    state = mau(dot, root)
    schema = load_evidence_schema(root)
    missing, invalid, missed = [], {}, []
    for key in state["sample"]:
        p = mau_evidence_path(dot, key, root)
        if not p.exists():
            missing.append(key)
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        errs = schema_errors(doc, schema)
        if not errs and doc["unit"] != key:
            errs = [f"unit là {doc['unit']!r}"]
        if not errs and doc["hash"] != cl.current_hash(key, root):
            errs = ["hash khác mã băm hiện tại"]
        if errs:
            invalid[key] = errs
            continue
        if any(c["verdict"] == "sai" and c["severity"] == "nghiem-trong" and not c.get("fixed") for c in doc["claims"]):
            missed.append(key)
    n = len(state["sample"])
    state["result"] = {
        "checked": n - len(missing) - len(invalid), "size": n, "missing": missing, "invalid": invalid,
        "missed_serious": missed, "rate": round(len(missed) / n, 4) if n else 0.0,
        "pass": not missing and not invalid and (len(missed) / n if n else 0.0) <= NGUONG,
    }
    write_mau(state, root)
    return state


def write_mau(state: dict, root: Path = ROOT) -> None:
    p = mau_path(state["dot"], root)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p.with_suffix(".md").write_text(render_mau(state), encoding="utf-8")


def render_mau(state: dict) -> str:
    dot, r = state["dot"], state["result"]
    L = [f"# Mẫu kiểm của đợt con {dot}", "",
         f"Sinh bằng `python tools/verify.py --mau {dot}` / `--so-mau {dot}`; không sửa tay (trạng thái ở `{dot}.json`).", "",
         f"- Chọn ngày {state['chosen_on']}: {len(state['sample'])} khóa (10%, ít nhất 3), hạt giống `{dot}`.",
         f"- Bằng chứng mẫu: `verification/mau/{dot}/<khóa>.json`, do agent kiểm thứ hai làm, không xem bằng chứng gốc."]
    if r:
        pct = f"{100 * r['rate']:.1f}".replace(".", ",")
        L.append(f"- Đã kiểm {r['checked']}/{r['size']}; lỗi nghiêm trọng bị bỏ sót: {len(r['missed_serious'])} "
                 f"({pct}%, ngưỡng 2%) — **{'đạt' if r['pass'] else 'chưa đạt'}**.")
    L.append(f"- Chủ biên duyệt: {state['chu_bien_duyet'] or 'chưa'}.")
    L += ["", "| Khóa | Bằng chứng gốc | Bằng chứng mẫu | Kết quả |", "|---|---|---|---|"]
    for key in state["sample"]:
        name = Path(cl.evidence_path(key)).name
        res = "—"
        if r:
            res = ("chưa có" if key in r["missing"] else "sai dạng" if key in r["invalid"]
                   else "**bỏ sót lỗi nghiêm trọng**" if key in r["missed_serious"] else "khớp")
        L.append(f"| `{key}` | [`{name}`](../evidence/{name}) | [`{name}`]({dot}/{name}) | {res} |")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- đóng băng, tiến độ

def dong_bang(dot: str, duyet: str, root: Path = ROOT) -> int:
    p = mau_path(dot, root)
    if not p.exists():
        raise SystemExit(f"chưa có mẫu cho {dot}: chạy --mau, kiểm mẫu, rồi --so-mau")
    state = json.loads(p.read_text(encoding="utf-8"))
    if not (state.get("result") or {}).get("pass"):
        raise SystemExit(f"mẫu {dot} chưa đạt (chạy --so-mau và xem {p.with_suffix('.md').relative_to(root)})")
    ledger = cl.load(root)
    keys = scope(dot, root)
    not_ready = [k for k in keys if ledger["units"].get(k, {}).get("status") not in ("da-kiem", "frozen")]
    if not_ready:
        raise SystemExit(f"{len(not_ready)} khóa của {dot} chưa da-kiem, ví dụ {not_ready[:5]}")
    changed = [k for k in keys if cl.current_hash(k, root) != ledger["units"][k]["hash"]]
    if changed:
        raise SystemExit(f"{len(changed)} khóa đổi mã băm sau khi kiểm, ví dụ {changed[:5]}: kiểm lại trước")
    n = 0
    for k in keys:
        if ledger["units"][k]["status"] == "da-kiem":
            ledger["units"][k]["status"] = "frozen"
            n += 1
    save_ledger(ledger, root)
    state["chu_bien_duyet"] = duyet
    write_mau(state, root)
    return n


def tien_do(dot: str, root: Path = ROOT) -> str:
    ledger = cl.load(root)
    keys = scope(dot, root)
    counts = {"chua-ghi": 0, "chua-kiem": 0, "da-kiem": 0, "frozen": 0}
    todo = []
    for k in keys:
        e = ledger["units"].get(k)
        counts[e["status"] if e else "chua-ghi"] += 1
        if e and e["status"] == "chua-kiem":
            ev = root / cl.evidence_path(k)
            if ev.exists():
                doc = json.loads(ev.read_text(encoding="utf-8"))
                todo.append(f"  {k}: bằng chứng result={doc.get('result')}")
    lines = [f"Đợt con {dot}: {len(keys)} khóa — " + ", ".join(f"{s} {n}" for s, n in counts.items())]
    if todo:
        lines += ["Có bằng chứng, chưa ghi da-kiem:"] + todo
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pham-vi", metavar="DOT")
    g.add_argument("--ghi-so", metavar="DOT")
    g.add_argument("--ghi", nargs="+", metavar="KHOA")
    g.add_argument("--ghi-dot", metavar="DOT")
    g.add_argument("--tien-do", metavar="DOT")
    g.add_argument("--mau", metavar="DOT")
    g.add_argument("--so-mau", metavar="DOT")
    g.add_argument("--dong-bang", metavar="DOT")
    ap.add_argument("--chu-bien-duyet", metavar="YYYY-MM-DD", help="ngày chủ biên duyệt mẫu (bắt buộc với --dong-bang)")
    a = ap.parse_args(argv)

    if a.pham_vi:
        print("\n".join(scope(a.pham_vi)))
        return 0
    if a.ghi_so:
        added, updated, dropped = ghi_so(a.ghi_so)
        print(f"Đợt con {a.ghi_so}: thêm {added} khóa chua-kiem, cập nhật mã băm {updated} khóa, bỏ {len(dropped)} khóa"
              + (": " + ", ".join(dropped) if dropped else "") + ".")
        return 0
    if a.ghi or a.ghi_dot:
        keys = a.ghi or [k for k in scope(a.ghi_dot) if (ROOT / cl.evidence_path(k)).exists()]
        done, fail = ghi(keys)
        print(f"Ghi da-kiem: {len(done)} khóa.")
        for k, why in fail.items():
            print(f"  chưa ghi {k}: " + "; ".join(why), file=sys.stderr)
        return 1 if fail else 0
    if a.tien_do:
        print(tien_do(a.tien_do))
        return 0
    if a.mau:
        state = mau(a.mau)
        print(f"Mẫu {a.mau}: {len(state['sample'])} khóa → {mau_path(a.mau).relative_to(ROOT)}")
        print("\n".join("  " + k for k in state["sample"]))
        return 0
    if a.so_mau:
        r = so_mau(a.so_mau)["result"]
        print(f"Mẫu {a.so_mau}: kiểm {r['checked']}/{r['size']}, bỏ sót lỗi nghiêm trọng {len(r['missed_serious'])}"
              f" ({100 * r['rate']:.1f}%) — {'đạt' if r['pass'] else 'chưa đạt'}.")
        return 0 if r["pass"] else 1
    if a.dong_bang:
        if not a.chu_bien_duyet:
            ap.error("--dong-bang cần --chu-bien-duyet YYYY-MM-DD")
        n = dong_bang(a.dong_bang, a.chu_bien_duyet)
        print(f"Đóng băng {n} khóa của đợt con {a.dong_bang}.")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
