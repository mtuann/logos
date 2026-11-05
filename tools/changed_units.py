"""Báo cáo đơn vị thay đổi giữa hai phiên bản (KE-HOACH.md mục 8, 9; ban-giao/dot-1.md việc 1.6). Không chặn.

    python tools/changed_units.py --base main               # main → cây làm việc hiện tại
    python tools/changed_units.py --base A --head B         # commit A → commit B
    python tools/changed_units.py --base main -o bao-cao.md # ghi ra file (CI đăng thành bình luận PR / job summary)

Với mỗi trang Markdown đổi trong docs/: tách đơn vị theo H2 (lz.units) ở cả hai phiên bản, so mã băm
(lz.hashing) và liệt kê đơn vị sửa / thêm / bỏ, kèm tầng, khối, trạng thái trong sổ kiểm chứng, và việc
cần làm. Đổi định dạng mà chữ không đổi (mã băm giữ nguyên) thì không hiện. Trang sinh tự động và file dữ liệu
đổi được liệt kê theo file. Luôn thoát mã 0, trừ khi git lỗi.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from lz import ROOT, hashing, units

LEDGER = "verification/ledger.json"
EMPTY = hashing.digest("")
TIER_LABEL = {"loi": "Lõi", "mo-rong": "Mở rộng", "he-thong": "hệ thống", None: "chưa đăng ký"}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def read(rev: str | None, path: str) -> str | None:
    """Nội dung file ở commit `rev` (None = cây làm việc); None nếu file không có."""
    if rev is None:
        f = ROOT / path
        return f.read_text(encoding="utf-8") if f.exists() else None
    try:
        return git("show", f"{rev}:{path}")
    except subprocess.CalledProcessError:
        return None


def changed_files(base: str, head: str | None) -> list[str]:
    args = ["diff", "--name-only", "--no-renames", base] + ([head] if head else [])
    files = set(git(*args).split())
    if head is None:   # cây làm việc: tính cả file mới chưa add
        files |= set(git("ls-files", "--others", "--exclude-standard").split())
    return sorted(files)


@dataclass
class Change:
    key: str
    kind: str          # sua | them | bo
    tier: str | None
    block: str | None
    status: str | None


def unit_hashes(path: str, text: str | None) -> dict[str, str]:
    if text is None:
        return {}
    return {u.id: hashing.unit_hash(u.source) for u in units.split(path, text)}


# File dữ liệu báo theo bản ghi (khóa giống sổ kiểm chứng, xem tools/check_ledger.py).
RECORD_FILES = {"data/kb/people.yml": "people", "data/kb/works.yml": "works", "data/kb/quotes.yml": "quotes",
                "data/kb/events.yml": "events", "data/kb/sources.yml": "sources"}


def record_hashes(path: str, text: str | None) -> dict[str, str]:
    """{khóa bản ghi: mã băm} của một file dữ liệu ở một phiên bản."""
    if text is None:
        return {}
    if path in RECORD_FILES:
        d = yaml.safe_load(text) or {}
        return {f"{RECORD_FILES[path]}/{k}": hashing.record_hash(v) for k, v in d.items()}
    if path.startswith("data/people/") and path.endswith(".yml"):
        return {f"ho-so/{Path(path).stem}": hashing.record_hash(yaml.safe_load(text))}
    if path == "data/kb/philpapers-2020.json":
        return {f"philpapers/{q['id']}": hashing.record_hash(q) for q in json.loads(text).get("questions", [])}
    return {}


def collect(base: str, head: str | None):
    reg = yaml.safe_load(read(head, "content.yml") or "{}") or {}
    pages = {e["path"]: e for e in reg.get("pages", [])}
    data = {e["path"]: e for e in reg.get("data", [])}
    ledger = json.loads(read(head, LEDGER) or '{"units": {}}').get("units", {})

    changes: list[Change] = []
    generated: list[str] = []
    data_files: list[tuple[str, dict | None]] = []
    for f in changed_files(base, head):
        entry = data.get(f) or next((e for p, e in data.items() if p.endswith("/") and f.startswith(p)), None)
        old_r, new_r = record_hashes(f, read(base, f)), record_hashes(f, read(head, f))
        if old_r or new_r:
            for key in list(old_r) + [k for k in new_r if k not in old_r]:
                if old_r.get(key) == new_r.get(key):
                    continue
                kind = "them" if key not in old_r else "bo" if key not in new_r else "sua"
                changes.append(Change(key, kind, entry["tier"] if entry else None, entry["block"] if entry else None,
                                      ledger.get(key, {}).get("status")))
            continue
        if entry:
            data_files.append((f, entry))
            continue
        if not (f.startswith("docs/") and f.endswith(".md")):
            continue
        path = f[len("docs/"):]
        entry = pages.get(path)
        if entry and entry["generated"]:
            generated.append(path)
            continue
        old, new = unit_hashes(path, read(base, f)), unit_hashes(path, read(head, f))
        tier, block = (entry["tier"], entry["block"]) if entry else (None, None)
        for ident in list(old) + [i for i in new if i not in old]:
            if old.get(ident) == new.get(ident):
                continue
            kind = "them" if ident not in old else "bo" if ident not in new else "sua"
            if kind != "sua" and (old.get(ident) or new.get(ident)) == EMPTY:
                continue   # phần `#_dau` rỗng của trang mới/bị bỏ: không có gì để kiểm
            key = f"{path}#{ident}"
            changes.append(Change(key, kind, tier, block, ledger.get(key, {}).get("status")))
    return changes, generated, data_files


def todo(c: Change) -> str:
    if c.tier == "loi":
        if c.status == "frozen":
            return "**đơn vị đã đóng băng**: cần nhãn `doi-loi` (hoặc `[doi-loi]` trong commit), bằng chứng mới, cập nhật sổ"
        if c.kind == "bo":
            return "bỏ khỏi sổ kiểm chứng nếu đã ghi"
        if c.status in ("da-kiem", "chua-kiem"):
            return "kiểm lại theo `ban-giao/kiem-chung.md`, cập nhật mã băm trong sổ"
        return "kiểm khi tới đợt con của khối (đợt 5)"
    if c.tier == "mo-rong":
        return "agent kiểm độc lập phần thêm (`ban-giao/kiem-chung.md`)"
    if c.tier == "he-thong":
        return "không cần kiểm nội dung"
    return "trang chưa có trong `content.yml`"


def report(base: str, head: str | None, changes, generated, data_files) -> str:
    target = head or "cây làm việc"
    out = [f"### Đơn vị thay đổi ({base} → {target})", ""]
    if not (changes or generated or data_files):
        out.append("Không đơn vị nội dung nào đổi chữ (mã băm giữ nguyên).")
        return "\n".join(out) + "\n"
    kind_label = {"sua": "sửa", "them": "thêm", "bo": "bỏ"}
    if changes:
        core = [c for c in changes if c.tier == "loi"]
        frozen = [c for c in core if c.status == "frozen"]
        out.append(f"{len(changes)} đơn vị đổi chữ, trong đó {len(core)} thuộc Lõi"
                   + (f", **{len(frozen)} đã đóng băng**" if frozen else "") + ".")
        out += ["", "| Đơn vị | Tầng | Khối | Thay đổi | Sổ | Việc cần làm |", "|---|---|---|---|---|---|"]
        for c in changes:
            out.append(f"| `{c.key}` | {TIER_LABEL.get(c.tier, c.tier)} | {c.block or '—'} | {kind_label[c.kind]} "
                       f"| {c.status or 'chưa ghi'} | {todo(c)} |")
    if generated:
        out += ["", f"Trang sinh tự động đổi ({len(generated)}): " + ", ".join(f"`{p}`" for p in generated)
                + ". Kiểm nguồn của chúng, không kiểm trang sinh."]
    if data_files:
        out += ["", "File dữ liệu đổi: " + ", ".join(
            f"`{f}` ({TIER_LABEL.get(e['tier'] if e else None)})" for f, e in data_files)
                + "."]
    if any(c.tier == "loi" for c in changes):
        out += ["", "Checklist cho đơn vị Lõi (`ban-giao/kiem-chung.md`):", "",
                "- [ ] Dữ kiện (năm, tên, tác phẩm, trích dẫn, số liệu) có nguồn đã mở",
                "- [ ] `dung-nguon` · `manh-nhat` · `phan-bac` · `trung-lap` · `thuat-ngu`",
                "- [ ] Thay đổi cơ học: `tools/parity.py --base main` giống 100%"]
    return "\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", required=True, help="commit/nhánh/tag gốc")
    ap.add_argument("--head", help="commit đích (mặc định: cây làm việc hiện tại)")
    ap.add_argument("-o", "--output", type=Path, help="ghi báo cáo Markdown ra file thay vì in ra")
    args = ap.parse_args(argv)
    text = report(args.base, args.head, *collect(args.base, args.head))
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
