"""Đổi link SEP sang bản lưu theo quý (ban-giao/dot-2.md việc 2.4; quyết định 14: fall2026, cố định).

    python tools/sep_archive.py --dry-run               # mở thử bản lưu của mọi mục, in kết quả, không ghi
    python tools/sep_archive.py                         # mở thử rồi đổi link ở trang viết tay và hồ sơ
    python tools/sep_archive.py --cache FILE.json       # nhớ kết quả mở thử, chạy lại không gọi mạng lần nữa

`https://plato.stanford.edu/entries/<mục>/<phần còn lại>` → `https://plato.stanford.edu/archives/fall2026/entries/<mục>/<phần còn lại>`,
chỉ với mục mà bản lưu trả 200 (mở thật, theo chuyển hướng, đích vẫn là bản lưu của đúng mục đó). Mục không mở được
giữ link cũ và vào verification/lech/sep.md. Link đã là bản lưu của quý khác giữ nguyên, cũng ghi vào danh sách lệch.
Phạm vi: trang viết tay trong docs/ (theo content.yml) và hồ sơ data/people/*.yml; trang sinh tự động
(triet-gia/*.md, them/sach.md) được sinh lại bằng tool của chúng. Sau khi đổi: chạy lại kb_sources.py, ghi `accessed`
(ngày mở thử) cho các nguồn SEP đã có bản lưu.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

from lz import ROOT, registry

QUARTER = "fall2026"
SEP = re.compile(r"(https?://plato\.stanford\.edu/)entries/([A-Za-z0-9_.-]+)/")
OTHER_ARCHIVE = re.compile(r"https?://plato\.stanford\.edu/archives/(?!%s/)([a-z]+\d{4})/entries/([A-Za-z0-9_.-]+)/" % QUARTER)
LECH = ROOT / "verification" / "lech" / "sep.md"
UA = "Mozilla/5.0 (compatible; logos-sep-archive/1.0; +https://mtuann.github.io/logos/)"


def files(root: Path = ROOT) -> list[Path]:
    out = [p.file(root) for p in registry.load(root).select(generated=False)]
    return out + sorted((root / "data" / "people").glob("*.yml"))


def archive_url(entry: str, quarter: str = QUARTER) -> str:
    return f"https://plato.stanford.edu/archives/{quarter}/entries/{entry}/"


def probe(entry: str) -> dict:
    url = archive_url(entry)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            final = r.geturl()
            ok = r.status == 200 and f"/archives/{QUARTER}/entries/{entry}/" in final
            return {"status": r.status, "final": final, "ok": ok}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "final": url, "ok": False}
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return {"status": None, "final": url, "ok": False, "error": str(e)[:200]}


def collect(root: Path = ROOT) -> tuple[dict[str, list[str]], list[tuple[str, str]]]:
    """(mục → các file dùng nó, các link bản lưu quý khác)."""
    entries: dict[str, list[str]] = {}
    others = []
    for f in files(root):
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(root).as_posix()
        for m in SEP.finditer(text):
            entries.setdefault(m.group(2), [])
            if rel not in entries[m.group(2)]:
                entries[m.group(2)].append(rel)
        others += [(rel, m.group(0)) for m in OTHER_ARCHIVE.finditer(text)]
    return dict(sorted(entries.items())), others


def rewrite(text: str, ok: set[str]) -> tuple[str, int]:
    n = 0

    def sub(m: re.Match) -> str:
        nonlocal n
        if m.group(2) not in ok:
            return m.group(0)
        n += 1
        return f"https://plato.stanford.edu/archives/{QUARTER}/entries/{m.group(2)}/"
    return SEP.sub(sub, text), n


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="chỉ mở thử và in kết quả")
    ap.add_argument("--cache", type=Path, help="file JSON nhớ kết quả mở thử")
    args = ap.parse_args(argv)

    entries, others = collect()
    cache = json.loads(args.cache.read_text(encoding="utf-8")) if args.cache and args.cache.exists() else {}
    todo = [e for e in entries if e not in cache]
    if todo:
        with ThreadPoolExecutor(max_workers=6) as ex:
            for entry, res in zip(todo, ex.map(probe, todo)):
                cache[entry] = res
        if args.cache:
            args.cache.write_text(json.dumps(cache, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    ok = {e for e in entries if cache[e]["ok"]}
    bad = [e for e in entries if not cache[e]["ok"]]
    print(f"SEP: {len(entries)} mục; bản lưu {QUARTER} mở được {len(ok)}, không mở được {len(bad)}.")
    for e in bad:
        print(f"  không mở được: {e} — {cache[e]}")
    if args.dry_run:
        return 0

    total = 0
    for f in files():
        text = f.read_text(encoding="utf-8")
        new, n = rewrite(text, ok)
        if n:
            f.write_text(new, encoding="utf-8")
            total += n
    print(f"Đã đổi {total} link ở {len({x for e in ok for x in entries[e]})} file.")

    LECH.parent.mkdir(parents=True, exist_ok=True)
    L = ["# Danh sách lệch: link SEP", "",
         f"Sinh bằng `python tools/sep_archive.py` (bản lưu {QUARTER}, quyết định 14). Đầu vào cho đợt 5.", "",
         f"- {len(entries)} mục SEP; {len(ok)} đã đổi sang bản lưu; {len(bad)} giữ link cũ vì bản lưu không mở được.", "",
         f"## Bản lưu không mở được ({len(bad)})", ""]
    L += [f"- `{e}` ({', '.join(entries[e])}): {cache[e]}" for e in bad]
    L += ["", f"## Link bản lưu của quý khác, giữ nguyên ({len(others)})", "",
          "Đổi quý là việc kiểm lại nguồn (quyết định 14), không làm cơ học.", ""]
    L += [f"- `{rel}`: <{u}>" for rel, u in others]
    LECH.write_text("\n".join(L) + "\n", encoding="utf-8")

    # Sinh lại kho nguồn, ghi ngày mở thử cho nguồn SEP có bản lưu.
    sys.path.insert(0, str(ROOT / "tools"))
    import kb_sources
    out = kb_sources.OUT
    old = yaml.safe_load(out.read_text(encoding="utf-8")) if out.exists() else {}
    recs, _ = kb_sources.extract()
    recs = kb_sources.merge_kept(recs, old or {})
    today = datetime.date.today().isoformat()
    for r in recs.values():
        if r.get("archive") and f"/archives/{QUARTER}/" in r["archive"] and "accessed" not in r:
            r["accessed"] = today
    out.write_text(kb_sources.render(recs), encoding="utf-8")
    print(f"Đã cập nhật {out.relative_to(ROOT)}; chạy lại philosophers.py và book.py để sinh lại trang.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
