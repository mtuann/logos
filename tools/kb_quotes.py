"""Kho trích dẫn data/kb/quotes.yml: rút mọi khối `!!! quote` của Lõi viết tay và `quote` của hồ sơ
(ban-giao/dot-2.md việc 2.6). Trang chưa đổi sang shortcode (quyết định 3: trích dẫn đối chiếu bằng linter).

    python tools/kb_quotes.py           # rút lại, ghi data/kb/quotes.yml và verification/lech/quotes.md
    python tools/kb_quotes.py --check   # mã thoát 1 khi quotes.yml lệch các trang (CI)

Khối trong trang: `title` = tiêu đề khối (trong ngoặc kép), `body` = phần thân, nguyên văn, đã bỏ thụt lề của khối
(ghép ngược ra khối cho đúng từng chữ). Không tách nguyên văn và bản dịch bằng phỏng đoán. Trích dẫn của hồ sơ có sẵn
trường riêng: `title` = source, `original` = orig, `translation` = vi, `url`.
`translator: logos-zero` khi có chữ "(bản dịch của Logos Zero)"; còn lại `null`. `license: unknown` tới đợt 5.
Khóa `<tác giả>.<tác phẩm>` rút từ tiêu đề dạng "Tác giả, *Tác phẩm*, …" (thêm `-2`, `-3` khi trùng);
không rút được thì `trich.<phần đầu tiêu đề>` (tiêu đề rỗng: `trang.<đường dẫn>.<số thứ tự>`) và vào danh sách lệch. `work` trỏ tới works.yml khi tên in nghiêng
trùng một tên trong đó. Trường `locator`, `license`, `evidence`, `verified` được giữ khi rút lại.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

from kb_sources import slug
from kb_works import norm
from lz import ROOT, registry, units

OUT = ROOT / "data" / "kb" / "quotes.yml"
LECH = ROOT / "verification" / "lech" / "quotes.md"
WORKS = ROOT / "data" / "kb" / "works.yml"
KEEP = ("locator", "license", "evidence", "verified")
BLOCK = re.compile(r'^(?P<indent>[ \t]*)(?:!!!|\?\?\?\+?)[ \t]+quote(?:[ \t]+"(?P<title>.*)")?[ \t]*$')
FENCE = re.compile(r"^\s*(```|~~~)")
ITALIC = re.compile(r"\*([^*\n]+?)\*")
LZ_TRANSLATION = "(bản dịch của Logos Zero)"
HEAD = ("# Kho trích dẫn. RÚT TỰ ĐỘNG bằng tools/kb_quotes.py từ khối !!! quote của Lõi viết tay và quote của hồ sơ;\n"
        "# chỉ locator, license, evidence, verified được sửa ở đây. Schema: schema/kb/quotes.schema.json. Lệch: verification/lech/quotes.md.\n")


def page_blocks(path: str, text: str) -> list[tuple[int, str, str]]:
    """(số dòng, tiêu đề, thân) của mọi khối quote trong trang, theo thứ tự; thân đã bỏ thụt lề của khối."""
    lines = text.split("\n")
    out, i, fence = [], 0, False
    while i < len(lines):
        line = lines[i]
        if FENCE.match(line):
            fence = not fence
        m = None if fence else BLOCK.match(line)
        if not m:
            i += 1
            continue
        inner = len(m.group("indent")) + 4
        body, j = [], i + 1
        while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) >= inner):
            body.append(lines[j][inner:] if lines[j].strip() else "")
            j += 1
        while body and not body[-1]:
            body.pop()
        out.append((i + 1, m.group("title") or "", "\n".join(body)))
        i = j
    return out


def base_key(title: str) -> str | None:
    m = ITALIC.search(title)
    if not m:
        return None
    author = slug(title[:m.start()].strip(" ,;:—–-"), 24)
    work = slug(m.group(1), 40)
    return f"{author}.{work}" if author and work else None


def extract(root: Path = ROOT) -> tuple[dict, list[str]]:
    works = yaml.safe_load(WORKS.read_text(encoding="utf-8")) if WORKS.exists() else {}
    title_to_work = {}
    for k, w in (works or {}).items():
        for t in w["titles"]:
            title_to_work.setdefault(norm(t), k)
    recs: dict[str, dict] = {}
    unkeyed: list[str] = []

    def put(base: str, rec: dict) -> str:
        key, n = base, 2
        while key in recs:
            key, n = f"{base}-{n}", n + 1
        recs[key] = rec
        return key

    def work_of(title: str):
        m = ITALIC.search(title)
        return title_to_work.get(norm(m.group(1))) if m else None

    for p in registry.load(root).select(tier="loi", generated=False):
        raw = p.file(root).read_text(encoding="utf-8")
        us = units.split(p.path, raw)
        for idx, (lineno, title, body) in enumerate(page_blocks(p.path, raw), start=1):
            unit = next(u.key for u in us if u.start <= lineno <= u.end)
            same = next((r for r in recs.values() if r.get("title") == title and r.get("body") == body), None)
            if same is not None:   # cùng một khối ở nhiều trang: một bản ghi, nhiều nơi dùng
                if unit not in same["used_in"]:
                    same["used_in"].append(unit)
                continue
            rec = {"work": work_of(title), "title": title, "body": body,
                   "translator": "logos-zero" if LZ_TRANSLATION in body else None,
                   "license": "unknown", "used_in": [unit]}
            base = base_key(title)
            if base is None:   # không theo mẫu: khóa theo phần đầu tiêu đề (trước " — "), ổn định hơn số thứ tự
                head = slug(title.split(" — ")[0], 60)
                base = f"trich.{head}" if head else f"trang.{slug(p.path[:-3], 50)}.{idx}"
            key = put(base, rec)
            if key.startswith(("trich.", "trang.")):
                unkeyed.append(key)
    for f in sorted((root / "data" / "people").glob("*.yml")):
        q = yaml.safe_load(f.read_text(encoding="utf-8")).get("quote")
        if not q:
            continue
        rec = {"work": work_of(q["source"]), "title": q["source"], "original": q["orig"], "translation": q["vi"],
               "translator": None, "license": "unknown", "url": q["url"], "used_in": [f"people/{f.stem}"]}
        put(base_key(q["source"]) or f"{f.stem}.trich", rec)
    for r in recs.values():
        r.setdefault("evidence", [])
        r.setdefault("verified", None)
    return dict(sorted(recs.items())), unkeyed


def merge_kept(recs: dict, old: dict) -> dict:
    for key, r in recs.items():
        for f in KEEP:
            if f in (old.get(key) or {}):
                r[f] = old[key][f]
    return recs


def render(recs: dict) -> str:
    order = ["work", "locator", "title", "body", "original", "translation", "translator", "license", "url",
             "used_in", "evidence", "verified"]
    out = {k: {f: r[f] for f in order if f in r} for k, r in recs.items()}
    return HEAD + yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=1_000_000)


def render_lech(recs: dict, unkeyed: list[str]) -> str:
    nowork = [k for k, r in recs.items() if not r["work"]]
    suffixed = [k for k in recs if re.search(r"-\d+$", k) and re.sub(r"-\d+$", "", k) in recs]
    L = ["# Danh sách lệch: trích dẫn", "",
         "Sinh bằng `python tools/kb_quotes.py`. Đầu vào cho đợt 5 (đợt con 5.2): không sửa trong đợt 2.", "",
         f"- {len(recs)} khối trích dẫn; {sum(1 for r in recs.values() if r['translator'] == 'logos-zero')} có bản dịch của Logos Zero.",
         f"- {len(recs) - len(nowork)} ghép được với tác phẩm trong works.yml; {len(nowork)} chưa.", "",
         f"## Tiêu đề khối không theo mẫu \"Tác giả, *Tác phẩm*, vị trí\" ({len(unkeyed)})", ""]
    L += [f"- `{k}`: \"{recs[k]['title']}\" (`{recs[k]['used_in'][0]}`)" for k in unkeyed]
    L += ["", f"## Cùng tác giả và tác phẩm, nhiều khối ({len(suffixed)})", "",
          "Khóa thêm hậu tố; đợt 5 ghi `locator` (38a, §IV, 2A6…) để phân biệt, hoặc gộp khi trùng đoạn.", ""]
    L += [f"- `{k}`: \"{recs[k]['title']}\"" for k in suffixed]
    L += ["", f"## Chưa ghép được tác phẩm ({len(nowork)})", ""]
    L += [f"- `{k}`: \"{recs[k]['title']}\"" for k in nowork]
    return "\n".join(L) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="báo lỗi khi quotes.yml lệch các trang")
    args = ap.parse_args(argv)
    old = yaml.safe_load(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    recs, unkeyed = extract()
    recs = merge_kept(recs, old or {})
    text = render(recs)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("data/kb/quotes.yml lệch khối trích dẫn của các trang — chạy: python tools/kb_quotes.py", file=sys.stderr)
            return 1
        print(f"Kho trích dẫn khớp các trang ({len(recs)} khối).")
        return 0
    OUT.write_text(text, encoding="utf-8")
    LECH.parent.mkdir(parents=True, exist_ok=True)
    LECH.write_text(render_lech(recs, unkeyed), encoding="utf-8")
    print(f"Đã ghi data/kb/quotes.yml ({len(recs)} khối) và verification/lech/quotes.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
