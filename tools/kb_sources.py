"""Kho nguồn data/kb/sources.yml: rút từ mọi mục Nguồn của trang viết tay và `sources` của hồ sơ triết gia
(ban-giao/dot-2.md việc 2.3).

    python tools/kb_sources.py           # rút lại, ghi data/kb/sources.yml và verification/lech/sources.md
    python tools/kb_sources.py --check   # mã thoát 1 khi sources.yml lệch các trang (CI)

Mỗi mục Nguồn (một dòng danh sách trong mục `## Nguồn`, hoặc một phần tử `sources` của hồ sơ) ứng với một bản ghi.
Khóa theo URL đầu tiên của mục (`sep.<mục>`, `iep.<mục>`, `gutenberg.<số>`, `doi.<doi>`, `ctext.<đường dẫn>`,
`wikisource.<ngôn ngữ>.<tên>`, `web.<tên miền>.<đường dẫn>`), hoặc theo chữ của mục khi không có URL (`sach.<…>`).
Các mục có cùng URL đầu (sau chuẩn hóa: https, bỏ www., bỏ / cuối, bỏ #…) được gộp; chữ khác nhau ghi ở `texts_seen`.
URL thứ hai trở đi của một mục ghi ở `also`.

Nguồn SEP dẫn bằng bản lưu fall2026 (quyết định 14): `url` là link gốc của mục, `archive` là bản lưu.
Trường biên tập thêm sau (`accessed`: ngày đã mở bản lưu, ghi bởi tools/sep_archive.py; `verified`) được giữ nguyên khi rút lại. Đây là chỉ mục của các
mục Nguồn đang có, không phải nơi sửa nguồn: sửa ở trang hoặc hồ sơ rồi chạy lại tool.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

from lz import ROOT, registry, units

OUT = ROOT / "data" / "kb" / "sources.yml"
LECH = ROOT / "verification" / "lech" / "sources.md"
PEOPLE = ROOT / "data" / "people"
KEEP = ("accessed", "verified")
SEP_QUARTER = "fall2026"   # quyết định 14: bản lưu SEP dùng trên site
SEP_ARCHIVE = re.compile(r"https?://plato\.stanford\.edu/archives/%s/entries/([A-Za-z0-9_.-]+)/" % SEP_QUARTER)
URL = re.compile(r"<(https?://[^>\s]+)>|\]\((https?://[^)\s]+)\)|(?<![<(\w])(https?://[^\s)>\]]+)")
ITEM = re.compile(r"^(?:\d+\.|[-*+])\s+")
HEAD = ("# Kho nguồn: mỗi mục Nguồn (trang viết tay, hồ sơ triết gia) một bản ghi. RÚT TỰ ĐỘNG bằng tools/kb_sources.py;\n"
        "# chỉ các trường accessed, verified được sửa ở đây (tool giữ nguyên khi rút lại). Schema: schema/kb/sources.schema.json.\n")


def slug(s: str, limit: int = 60) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFKD", unquote(s))
    s = "".join(c for c in s if not unicodedata.combining(c)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:limit].rstrip("-")


def norm_url(u: str) -> str:
    p = urlsplit(u)
    host = p.netloc.lower().removeprefix("www.")
    path = p.path.rstrip("/")
    return f"https://{host}{path}" + (f"?{p.query}" if p.query else "")


def classify(url: str | None, text: str) -> tuple[str, str]:
    """(type, khóa chưa khử trùng)."""
    if not url:
        plain = re.sub(r"[*_`\[\]()<>]", "", text)
        return "sach", "sach." + (slug(plain) or hashlib.sha1(text.encode()).hexdigest()[:10])
    p = urlsplit(url)
    host = p.netloc.lower().removeprefix("www.")
    segs = [x for x in p.path.split("/") if x]
    if host == "plato.stanford.edu" and "entries" in segs:
        return "sep", "sep." + slug(segs[segs.index("entries") + 1])
    if host == "iep.utm.edu" and segs:
        return "iep", "iep." + slug(segs[0])
    if host.endswith("gutenberg.org"):
        num = next((m.group(1) for m in [re.search(r"(?:ebooks|files|epub)/(\d+)", p.path)] if m), None)
        return "gutenberg", "gutenberg." + (num or slug(p.path))
    if host.endswith("wikisource.org"):
        lang = host.split(".")[0]
        title = slug("/".join(segs[1:] if segs[:1] == ["wiki"] else segs))
        return "wikisource", f"wikisource.{lang}." + (title or hashlib.sha1(p.path.encode()).hexdigest()[:10])
    if host == "ctext.org":
        return "ctext", "ctext." + (slug(p.path + ("-" + p.query if p.query else "")) or "goc")
    if "cbeta" in host:
        return "cbeta", "cbeta." + (slug(p.path + p.query) or hashlib.sha1(url.encode()).hexdigest()[:10])
    if host in ("doi.org", "dx.doi.org"):
        return "doi", "doi." + slug(p.path, 80)
    rest = slug(p.path + ("-" + p.query if p.query else ""), 50)
    return "khac", "web." + slug(host) + (f".{rest}" if rest else "")


def page_items(root: Path = ROOT):
    """(đơn vị, chữ của mục) cho mọi mục danh sách trong mục Nguồn của trang viết tay."""
    for p in registry.load(root).select(generated=False):
        for u in units.split_file(p.path, root):
            if u.id == "_dau" or not re.match(r"Nguồn\b", u.title or ""):
                continue
            cur: list[str] | None = None
            for line in u.source.split("\n")[1:]:
                if ITEM.match(line):
                    if cur:
                        yield u.key, " ".join(cur)
                    cur = [ITEM.sub("", line).strip()]
                elif cur is not None and line.strip() and line[:1] in " \t":
                    cur.append(line.strip())
                else:
                    if cur:
                        yield u.key, " ".join(cur)
                    cur = None
            if cur:
                yield u.key, " ".join(cur)


def profile_items(root: Path = ROOT):
    for f in sorted((root / "data" / "people").glob("*.yml")):
        for s in yaml.safe_load(f.read_text(encoding="utf-8")).get("sources", []):
            yield f"people/{f.stem}", s["text"] + (f" <{s['url']}>" if s["url"] else "")


def urls_of(text: str) -> list[str]:
    return [next(g for g in m.groups() if g) for m in URL.finditer(text)]


def extract(root: Path = ROOT) -> tuple[dict, dict]:
    """(bản ghi theo khóa, số liệu cho danh sách lệch)."""
    by_norm: dict[str, str] = {}      # URL chuẩn hóa (hoặc khóa sách) → khóa
    recs: dict[str, dict] = {}
    stats = {"items": 0, "multi": [], "http": [], "no_url": 0}
    for where, text in list(page_items(root)) + list(profile_items(root)):
        stats["items"] += 1
        urls = urls_of(text)
        first = urls[0] if urls else None
        typ, base = classify(first, text)
        if typ == "sep":
            ident = base                       # mọi dạng link SEP (có/không bản lưu) cùng một mục
        else:
            ident = norm_url(first) if first else "sach:" + text   # sách: chỉ gộp khi ghi giống hệt
        if not first:
            stats["no_url"] += 1
        if len(urls) > 1:
            stats["multi"].append((where, text))
        stats["http"] += [(where, u) for u in urls if u.startswith("http://")]
        key = by_norm.get(ident)
        if key is None:
            key, n = base, 2
            while key in recs:
                key, n = f"{base}-{n}", n + 1
            by_norm[ident] = key
            recs[key] = {"type": typ, "text": text}
            if first:
                recs[key]["url"] = first
            m = SEP_ARCHIVE.match(first or "")
            if m:   # nguồn SEP dẫn bằng bản lưu: url là link gốc của mục, archive là bản lưu
                recs[key]["url"] = f"https://plato.stanford.edu/entries/{m.group(1)}/"
                recs[key]["archive"] = first
            recs[key]["used_in"] = []
        r = recs[key]
        if text != r["text"] and text not in r.get("texts_seen", []):
            r.setdefault("texts_seen", []).append(text)
        for u in urls[1:]:
            if u not in r.get("also", []):
                r.setdefault("also", []).append(u)
        if where not in r["used_in"]:
            r["used_in"].append(where)
    for r in recs.values():
        r["used_in"].sort()
    return dict(sorted(recs.items())), stats


def merge_kept(recs: dict, old: dict) -> dict:
    for key, r in recs.items():
        for f in KEEP:
            if f in (old.get(key) or {}):
                r[f] = old[key][f]
    return recs


def render(recs: dict) -> str:
    order = ["type", "text", "texts_seen", "url", "also", "archive", "accessed", "used_in", "verified"]
    out = {k: {f: r[f] for f in order if f in r} for k, r in recs.items()}
    return HEAD + yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=1_000_000)


def render_lech(recs: dict, stats: dict) -> str:
    by_type: dict[str, int] = {}
    for r in recs.values():
        by_type[r["type"]] = by_type.get(r["type"], 0) + 1
    multi_text = [(k, r) for k, r in recs.items() if r.get("texts_seen")]
    L = ["# Danh sách lệch: nguồn", "",
         "Sinh bằng `python tools/kb_sources.py`. Đầu vào cho đợt 5: không sửa trong đợt 2.", "",
         f"- {stats['items']} mục Nguồn (trang viết tay + hồ sơ) → {len(recs)} bản ghi.",
         "- Theo loại: " + ", ".join(f"{t} {n}" for t, n in sorted(by_type.items())) + ".",
         f"- {stats['no_url']} mục không có URL (sách in, hoặc thiếu link).", "",
         f"## Cùng một nguồn, chữ khác nhau ({len(multi_text)})", "",
         "Cùng URL đầu nhưng các trang ghi tác giả, tiêu đề, năm khác nhau: thống nhất ở đợt 5.", ""]
    for k, r in multi_text:
        L.append(f"- `{k}` ({len(r['texts_seen']) + 1} cách ghi; dùng ở {', '.join(f'`{u}`' for u in r['used_in'])})")
    dup = [k for k in recs if re.match(r"(.*)-\d+$", k) and re.match(r"(.*)-\d+$", k).group(1) in recs
           and recs[re.match(r"(.*)-\d+$", k).group(1)]["type"] == recs[k]["type"]]
    L += ["", f"## Sách có thể trùng ({len(dup)})", "",
          "Sách in không có URL, ghi gần giống nhau ở các trang (khác chương, trang, nhà xuất bản): xem có phải một nguồn.", ""]
    L += [f"- `{k}`: {recs[k]['text']}" for k in dup]
    L += ["", f"## Mục có nhiều URL ({len(stats['multi'])})", "",
          "Bản ghi lấy URL đầu; các URL sau ghi ở `also`. Xem có nên tách thành nhiều mục Nguồn không.", ""]
    L += [f"- `{w}`: {t}" for w, t in stats["multi"]]
    L += ["", f"## Link http:// ({len(stats['http'])})", ""]
    L += [f"- `{w}`: <{u}>" for w, u in stats["http"]]
    return "\n".join(L) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="báo lỗi khi sources.yml lệch các trang")
    args = ap.parse_args(argv)
    old = yaml.safe_load(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    recs, stats = extract()
    recs = merge_kept(recs, old or {})
    text = render(recs)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("data/kb/sources.yml lệch mục Nguồn của các trang — chạy: python tools/kb_sources.py", file=sys.stderr)
            return 1
        print(f"Kho nguồn khớp các trang ({len(recs)} bản ghi từ {stats['items']} mục Nguồn).")
        return 0
    OUT.write_text(text, encoding="utf-8")
    LECH.parent.mkdir(parents=True, exist_ok=True)
    LECH.write_text(render_lech(recs, stats), encoding="utf-8")
    print(f"Đã ghi data/kb/sources.yml ({len(recs)} bản ghi từ {stats['items']} mục Nguồn) và verification/lech/sources.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
