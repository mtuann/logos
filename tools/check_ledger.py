"""Sổ kiểm chứng `verification/ledger.json` (KE-HOACH.md mục 4, 7; ban-giao/dot-1.md việc 1.5).

    python tools/check_ledger.py --check          # CI: mã thoát 1 khi sổ sai dạng, hoặc đơn vị frozen lệch mã băm
    python tools/check_ledger.py --status         # tiến độ kiểm chứng theo khối
    python tools/check_ledger.py --hash KHÓA…     # in mã băm hiện tại của đơn vị (để ghi vào bằng chứng)

`--check` báo lỗi khi:
  - sổ không đúng schema/ledger.schema.json (trường thừa/thiếu, giá trị ngoài danh sách, sai mẫu);
  - một khóa trong sổ không còn ứng với đơn vị nào (trang bị đổi tên, mục bị bỏ hay đổi ID);
  - đơn vị `frozen` có mã băm hiện tại khác mã băm trong sổ — trừ khi biến môi trường LZ_ALLOW_CORE_CHANGE=1
    (CI đặt biến này khi PR có nhãn `doi-loi`, hoặc commit được push có `[doi-loi]` trong message);
    khi đó chỉ cảnh báo, và đơn vị phải được kiểm lại, cập nhật sổ trong cùng thay đổi;
  - đơn vị `da-kiem`/`frozen` thiếu file bằng chứng, hoặc file bằng chứng ghi khóa khác, mã băm khác.
Đơn vị `chua-kiem`/`da-kiem` lệch mã băm chỉ bị cảnh báo (cần kiểm lại trước khi đóng băng).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from functools import lru_cache
from pathlib import Path

from lz import ROOT, hashing, registry, units

LEDGER = Path("verification") / "ledger.json"
SCHEMA = Path("schema") / "ledger.schema.json"
ALLOW_ENV = "LZ_ALLOW_CORE_CHANGE"


def load(root: Path = ROOT) -> dict:
    return json.loads((root / LEDGER).read_text(encoding="utf-8"))


def load_schema(root: Path = ROOT) -> dict:
    return json.loads((root / SCHEMA).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- schema (kiểm tay, không cần thư viện jsonschema)

def validate(ledger: object, schema: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(ledger, dict):
        return ["sổ: phải là một object JSON"]
    allowed_top = set(schema["properties"])
    for k in sorted(set(ledger) - allowed_top):
        errors.append(f"sổ: trường thừa {k!r}")
    for k in schema["required"]:
        if k not in ledger:
            errors.append(f"sổ: thiếu trường {k!r}")
    if "version" in ledger and ledger["version"] != schema["properties"]["version"]["const"]:
        errors.append(f"sổ: version phải là {schema['properties']['version']['const']}")
    entries = ledger.get("units", {})
    if not isinstance(entries, dict):
        return errors + ["sổ: units phải là object"]
    key_re = re.compile(schema["properties"]["units"]["propertyNames"]["pattern"])
    entry = schema["$defs"]["entry"]
    props = entry["properties"]
    statuses = schema["$defs"]["status"]["enum"]
    cond_status = entry["if"]["properties"]["status"]["enum"]
    cond_required = entry["then"]["required"]
    for key, e in entries.items():
        where = f"sổ: {key}"
        if not key_re.search(key):
            errors.append(f"{where}: khóa sai mẫu")
        if not isinstance(e, dict):
            errors.append(f"{where}: phải là object")
            continue
        for f in sorted(set(e) - set(props)):
            errors.append(f"{where}: trường thừa {f!r}")
        need = list(entry["required"]) + (cond_required if e.get("status") in cond_status else [])
        for f in need:
            if f not in e:
                errors.append(f"{where}: thiếu {f!r}" + (f" (bắt buộc khi status {e.get('status')})"
                                                         if f in cond_required else ""))
        if "status" in e and e["status"] not in statuses:
            errors.append(f"{where}: status {e['status']!r} ngoài {statuses}")
        for f, spec in props.items():
            if f not in e or "type" not in spec:
                continue
            v = e[f]
            if not isinstance(v, str):
                errors.append(f"{where}: {f} phải là chuỗi")
            elif "pattern" in spec and not re.search(spec["pattern"], v):
                errors.append(f"{where}: {f} {v!r} sai mẫu")
            elif len(v) < spec.get("minLength", 0):
                errors.append(f"{where}: {f} rỗng")
    return errors


# ---------------------------------------------------------------- mã băm hiện tại của một khóa

@lru_cache(maxsize=None)
def _page_units(path: str, root: Path) -> dict[str, str] | None:
    f = root / "docs" / path
    if not f.exists():
        return None
    return {u.id: u.source for u in units.split_file(path, root)}


def current_hash(key: str, root: Path = ROOT) -> str:
    """Mã băm hiện tại của đơn vị `key`. KeyError (kèm lý do) nếu khóa không còn ứng với đơn vị nào."""
    if "#" in key:
        path, ident = key.split("#", 1)
        us = _page_units(path, root)
        if us is None:
            raise KeyError(f"không còn trang docs/{path}")
        if ident not in us:
            raise KeyError(f"trang {path} không còn mục #{ident}")
        return hashing.unit_hash(us[ident])
    kind = key.split("/", 1)[0]
    raise KeyError(f"loại bản ghi {kind!r} chưa có trong kho dữ kiện (đợt 2)")


def evidence_path(key: str) -> str:
    """Đường dẫn file bằng chứng theo ban-giao/kiem-chung.md: thay "/" và "#" bằng "__"."""
    return "verification/evidence/" + key.replace("/", "__").replace("#", "__") + ".json"


# ---------------------------------------------------------------- kiểm tra

def check(ledger: dict, root: Path = ROOT, allow_core_change: bool = False) -> tuple[list[str], list[str]]:
    """(lỗi, cảnh báo)."""
    errors = validate(ledger, load_schema(root))
    warnings: list[str] = []
    if errors:
        return errors, warnings
    for key, e in sorted(ledger["units"].items()):
        try:
            now = current_hash(key, root)
        except KeyError as exc:
            errors.append(f"{key}: {exc.args[0]}")
            continue
        if now != e["hash"]:
            msg = f"{key}: mã băm đổi ({e['hash'][:15]}… → {now[:15]}…)"
            if e["status"] == "frozen":
                if allow_core_change:
                    warnings.append(msg + f" — đơn vị đã đóng băng; được phép vì {ALLOW_ENV}=1, phải kiểm lại và cập nhật sổ")
                else:
                    errors.append(msg + " — đơn vị đã đóng băng: chỉ sửa trong thay đổi mang nhãn doi-loi, kèm bằng chứng mới")
            else:
                warnings.append(msg + f" — trạng thái {e['status']}: cần kiểm lại")
        if e["status"] in ("da-kiem", "frozen"):
            ev = root / e["evidence"]
            if not ev.exists():
                errors.append(f"{key}: không thấy file bằng chứng {e['evidence']}")
                continue
            try:
                doc = json.loads(ev.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{key}: file bằng chứng {e['evidence']} không phải JSON hợp lệ ({exc})")
                continue
            if doc.get("unit") != key:
                errors.append(f"{key}: file bằng chứng ghi unit {doc.get('unit')!r}")
            if doc.get("hash") not in (None, e["hash"]):
                errors.append(f"{key}: mã băm trong bằng chứng ({doc.get('hash')}) khác sổ ({e['hash']})")
    return errors, warnings


# ---------------------------------------------------------------- tiến độ

def core_units(root: Path = ROOT) -> list[tuple[str, str]]:
    """(khóa, khối) của mọi đơn vị trang trong Lõi viết tay, gồm cả `#_dau`."""
    out = []
    for p in registry.load(root).select(tier="loi", generated=False):
        out += [(u.key, p.block) for u in units.split_file(p.path, root)]
    return out


def status_table(ledger: dict, root: Path = ROOT) -> str:
    entries = ledger.get("units", {})
    rows: dict[str, dict[str, int]] = {}
    for key, block in core_units(root):
        r = rows.setdefault(block, {"tong": 0, "chua-ghi": 0, "chua-kiem": 0, "da-kiem": 0, "frozen": 0})
        r["tong"] += 1
        r[entries[key]["status"] if key in entries else "chua-ghi"] += 1
    total = {k: sum(r[k] for r in rows.values()) for k in ("tong", "chua-ghi", "chua-kiem", "da-kiem", "frozen")}
    lines = ["| Khối | Đơn vị | Chưa ghi sổ | Chưa kiểm | Đã kiểm | Đóng băng | % đóng băng |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for block, r in list(rows.items()) + [("**Tổng Lõi**", total)]:
        pct = f"{100 * r['frozen'] / r['tong']:.1f}".replace(".", ",") if r["tong"] else "—"
        lines.append(f"| {block} | {r['tong']} | {r['chua-ghi']} | {r['chua-kiem']} | {r['da-kiem']} | {r['frozen']} | {pct} |")
    other = sorted(set(entries) - {k for k, _ in core_units(root)})
    if other:
        lines += ["", f"Ngoài Lõi viết tay (bản ghi dữ liệu, Mở rộng): {len(other)} khóa trong sổ."]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="kiểm tra sổ (CI)")
    g.add_argument("--status", action="store_true", help="in tiến độ kiểm chứng theo khối")
    g.add_argument("--hash", nargs="+", metavar="KHOA", help="in mã băm hiện tại của các đơn vị")
    args = ap.parse_args(argv)

    if args.hash:
        bad = 0
        for key in args.hash:
            try:
                print(f"{current_hash(key)}  {key}")
            except KeyError as exc:
                print(f"LỖI  {key}: {exc.args[0]}", file=sys.stderr)
                bad = 1
        return bad

    ledger = load()
    if args.status:
        print(status_table(ledger))
        return 0

    allow = os.environ.get(ALLOW_ENV) == "1"
    errors, warnings = check(ledger, allow_core_change=allow)
    for w in warnings:
        print("  cảnh báo: " + w)
    if errors:
        print(f"Sổ kiểm chứng: {len(errors)} lỗi:", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1
    n = len(ledger["units"])
    frozen = sum(1 for e in ledger["units"].values() if e["status"] == "frozen")
    print(f"Sổ kiểm chứng khớp: {n} khóa, {frozen} đơn vị đóng băng"
          + (f", {len(warnings)} cảnh báo" if warnings else "") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
