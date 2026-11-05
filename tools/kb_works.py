"""Kho tác phẩm data/kb/works.yml: rút từ các chỗ "*Tác phẩm* (năm)" và danh sách tác phẩm của hồ sơ
(ban-giao/dot-2.md việc 2.5).

    python tools/kb_works.py           # rút lại, ghi data/kb/works.yml và verification/lech/works.md
    python tools/kb_works.py --check   # mã thoát 1 khi works.yml lệch trang và hồ sơ (CI)

Hai nguồn:
  1. `works` của hồ sơ data/people/<id>.yml. Tên in nghiêng đứng đầu dòng → tác giả là chủ hồ sơ. Có chữ đứng
     trước tên (ví dụ "Herodotus, *Historiai* I.74") → tác phẩm của người khác: `author: null`, `author_name` là
     đúng chữ đó. Năm lấy khi trường `year` bắt đầu bằng một năm ("1781", "k. 380 TCN", "1951, bản 6").
  2. Văn xuôi Lõi viết tay và hồ sơ (bio, thoughts, misread, argument): mẫu `*Tên* (năm)`, như báo cáo nền.
     Tên trùng (không phân biệt hoa thường) với một tác phẩm đã biết tác giả → gộp vào đó; không thì
     `author: null`, khóa `chua-ro.<tên>`. Không đoán tác giả: gán ở đợt 5.
Mỗi bản ghi giữ mọi cách viết tên (`titles`) và mọi năm gặp được (`years_seen`: năm → đơn vị). `year` chỉ điền khi
mọi chỗ cùng một năm; khác nhau thì `null` và vào verification/lech/works.md (năm bản gốc và năm bản dịch/bản in
khác nhau là chuyện thường: đợt 5 xem từng trường hợp). Trường `title_orig`, `attribution`, `year_note`, `evidence`, `verified` được giữ khi rút lại (đợt 5.1).
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

import yaml

from kb_sources import slug
from lz import ROOT, registry, units
from lz.lint import masked_lines

OUT = ROOT / "data" / "kb" / "works.yml"
LECH = ROOT / "verification" / "lech" / "works.md"
KEEP = ("title_orig", "attribution", "year_note", "evidence", "verified")
# Số dính chữ cái ngay sau ("519a": số trang Stephanus) không phải năm.
# Sau năm (và "TCN") phải là dấu đóng ngoặc, phẩy, chấm phẩy hay gạch nối: "(100 nhà sản xuất…)" không phải năm
# (đợt 5.1, `works/chua-ro.cdp-carbon-majors-report-2017`).
WORK_YEAR = re.compile(r"\*([^*\n]{2,160}?)\*\s*\((?:khoảng |k\. |năm )?(\d{3,4})(?![\w])(\s*TCN)?(?=\s*[),;–—-])")
ITALIC = re.compile(r"\*([^*\n]+?)\*")
YEAR = re.compile(r"^(?:k\. |khoảng )?(\d{3,4})(\s*TCN)?\b")
HEAD = ("# Kho tác phẩm. RÚT TỰ ĐỘNG bằng tools/kb_works.py từ \"*Tên* (năm)\" trong bài và danh sách tác phẩm của hồ sơ;\n"
        "# chỉ title_orig, attribution, year_note, evidence, verified được sửa ở đây. Schema: schema/kb/works.schema.json. Lệch: verification/lech/works.md.\n")


def norm(title: str) -> str:
    return " ".join(unicodedata.normalize("NFC", title).casefold().split())


def year_of(num: str, tcn: str | None) -> int:
    return -int(num) if tcn else int(num)


# Tên trong hồ sơ có chữ đứng trước phần in nghiêng nhưng chữ đó là một phần của tên (chú giải, bài báo), không phải
# tác giả khác: tác phẩm của chủ hồ sơ, tên = cả dòng bỏ dấu nhấn và ngoặc kép (đợt 5.1; bằng chứng
# works/chua-ro.de-anima, works/chua-ro.sieu-hinh-hoc, works/chua-ro.phenomenologie-de-lesprit).
OWN_TITLES = {
    "Chú giải lớn về *De Anima* của Aristotle",
    "Chú giải lớn về *Siêu hình học* của Aristotle",
    "“La *Phénoménologie de l’esprit* et son contenu réel”",
}


def profile_works(root: Path):
    """(người, chữ trước tên, tên, năm hoặc None, đơn vị) từ `works` của hồ sơ."""
    for f in sorted((root / "data" / "people").glob("*.yml")):
        for w in yaml.safe_load(f.read_text(encoding="utf-8")).get("works", []):
            m = ITALIC.search(w["title"])
            if not m:
                continue
            if w["title"] in OWN_TITLES:
                y = YEAR.match(w["year"])
                plain = w["title"].replace("*", "").strip("“”\"")
                yield f.stem, "", plain, (year_of(y.group(1), y.group(2)) if y else None), f"people/{f.stem}"
                continue
            prefix = w["title"][:m.start()].strip(" ,;:")
            y = YEAR.match(w["year"])
            yield f.stem, prefix, m.group(1).strip(), (year_of(y.group(1), y.group(2)) if y else None), f"people/{f.stem}"


def prose_mentions(root: Path):
    """(tên, năm, đơn vị) cho mẫu *Tên* (năm) trong văn xuôi Lõi viết tay và hồ sơ."""
    for p in registry.load(root).select(tier="loi", generated=False):
        raw = p.file(root).read_text(encoding="utf-8")
        us = units.split(p.path, raw)
        for no, line in enumerate(masked_lines(raw, quotes=False, sources=False)):
            for m in WORK_YEAR.finditer(line):
                unit = next(u.key for u in us if u.start <= no <= u.end)
                yield m.group(1).strip(), year_of(m.group(2), m.group(3)), unit
    for f in sorted((root / "data" / "people").glob("*.yml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        texts = d.get("bio", []) + d.get("thoughts", []) + d.get("misread", [])
        a = d.get("argument") or {}
        texts += [a.get(k, "") for k in ("intro", "objection", "reply", "conclusion")] + a.get("premises", [])
        for t in texts:
            for m in WORK_YEAR.finditer(t):
                yield m.group(1).strip(), year_of(m.group(2), m.group(3)), f"people/{f.stem}"


def extract(root: Path = ROOT) -> dict:
    recs: dict[str, dict] = {}
    by_title: dict[str, str] = {}      # tên chuẩn hóa → khóa (chỉ tác phẩm đã biết tác giả)

    def add(key, title, year, where, **fields):
        r = recs.setdefault(key, {**fields, "titles": [], "years_seen": {}, "used_in": []})
        if title not in r["titles"]:
            r["titles"].append(title)
        if year is not None:
            seen = r["years_seen"].setdefault(str(year), [])
            if where not in seen:
                seen.append(where)
        if where not in r["used_in"]:
            r["used_in"].append(where)

    for pid, prefix, title, year, where in profile_works(root):
        if prefix:
            add(f"chua-ro.{slug(title, 50)}", title, year, where, author=None, author_name=prefix)
        else:
            key = f"{pid}.{slug(title, 50)}"
            by_title.setdefault(norm(title), key)
            add(key, title, year, where, author=pid)
    for title, year, where in prose_mentions(root):
        key = by_title.get(norm(title)) or f"chua-ro.{slug(title, 50)}"
        add(key, title, year, where, author=None) if key not in recs else add(key, title, year, where)
    for r in recs.values():
        ys = sorted(r["years_seen"], key=int)
        r["years_seen"] = {y: sorted(r["years_seen"][y]) for y in ys}
        r["year"] = int(ys[0]) if len(ys) == 1 else None
        r["used_in"].sort()
        r.setdefault("evidence", [])
        r.setdefault("verified", None)
    return dict(sorted(recs.items()))


def merge_kept(recs: dict, old: dict) -> dict:
    for key, r in recs.items():
        for f in KEEP:
            if f in (old.get(key) or {}):
                r[f] = old[key][f]
    return recs


def render(recs: dict) -> str:
    order = ["author", "author_name", "attribution", "titles", "title_orig", "year", "year_note", "years_seen", "used_in", "evidence", "verified"]
    out = {k: {f: r[f] for f in order if f in r} for k, r in recs.items()}
    return HEAD + yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=1_000_000)


def render_lech(recs: dict) -> str:
    multi = {k: r for k, r in recs.items() if len(r["years_seen"]) > 1}
    unknown = [k for k, r in recs.items() if r["author"] is None]
    L = ["# Danh sách lệch: tác phẩm", "",
         "Sinh bằng `python tools/kb_works.py`. Đầu vào cho đợt 5 (đợt con 5.1): không sửa trong đợt 2.", "",
         f"- {len(recs)} tác phẩm; {len(recs) - len(unknown)} đã biết tác giả (từ hồ sơ), {len(unknown)} chưa rõ tác giả (`chua-ro.*`).",
         f"- {len(multi)} tác phẩm gặp với hơn một năm.", "",
         f"## Tác phẩm có hơn một năm ({len(multi)})", "",
         "Năm bản gốc, năm bản sửa, năm bản dịch có thể khác nhau hợp lệ: xem từng chỗ, rồi chốt `year` và cách ghi.", "",
         "| Tác phẩm | Các năm và nơi dùng |", "|---|---|"]
    for k, r in multi.items():
        cells = "<br>".join(f"**{y}**: " + ", ".join(f"`{u}`" for u in where) for y, where in r["years_seen"].items())
        L.append(f"| `{k}` ({r['titles'][0]}) | {cells} |")
    L += ["", f"## Chưa rõ tác giả ({len(unknown)})", "",
          "Gặp trong văn xuôi dạng *Tên* (năm) nhưng không khớp tác phẩm nào trong hồ sơ; gán tác giả ở đợt 5.", ""]
    L += [f"- `{k}`: *{recs[k]['titles'][0]}*" + (f" — {recs[k]['author_name']}" if recs[k].get("author_name") else "")
          for k in unknown]
    return "\n".join(L) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="báo lỗi khi works.yml lệch trang và hồ sơ")
    args = ap.parse_args(argv)
    old = yaml.safe_load(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    recs = merge_kept(extract(), old or {})
    text = render(recs)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("data/kb/works.yml lệch trang và hồ sơ — chạy: python tools/kb_works.py", file=sys.stderr)
            return 1
        print(f"Kho tác phẩm khớp trang và hồ sơ ({len(recs)} tác phẩm).")
        return 0
    OUT.write_text(text, encoding="utf-8")
    LECH.parent.mkdir(parents=True, exist_ok=True)
    LECH.write_text(render_lech(recs), encoding="utf-8")
    print(f"Đã ghi data/kb/works.yml ({len(recs)} tác phẩm) và verification/lech/works.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
