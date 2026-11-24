"""Kho trích dẫn data/kb/quotes.yml: rút mọi khối `!!! quote` của Lõi viết tay và `quote` của hồ sơ
(ban-giao/dot-2.md việc 2.6). Trang chưa đổi sang shortcode (quyết định 3: trích dẫn đối chiếu bằng linter).

    python tools/kb_quotes.py           # rút lại, ghi data/kb/quotes.yml và verification/lech/quotes.md
    python tools/kb_quotes.py --check   # mã thoát 1 khi quotes.yml lệch các trang (CI)

Khối trong trang: `title` = tiêu đề khối (trong ngoặc kép), `body` = phần thân, nguyên văn, đã bỏ thụt lề của khối
(ghép ngược ra khối cho đúng từng chữ). Không tách nguyên văn và bản dịch bằng phỏng đoán. Trích dẫn của hồ sơ có sẵn
trường riêng: `title` = source, `original` = orig, `translation` = vi, `url`.
`translator: logos` khi có chữ "(bản dịch của Logos)" (trước đợt 5.0d: `logos-zero`); còn lại `null`. `license: unknown` tới đợt 5.
Khóa `<tác giả>.<tác phẩm>` rút từ tiêu đề dạng "Tác giả, *Tác phẩm*, …" (thêm `-2`, `-3` khi trùng);
không rút được thì `trich.<phần đầu tiêu đề>` (tiêu đề rỗng: `trang.<đường dẫn>.<số thứ tự>`) và vào danh sách lệch.
`work` trỏ tới works.yml khi tên tác phẩm trong tiêu đề — tên in nghiêng đầu tiên; không có chữ in nghiêng thì tên
đầu tiên trong ngoặc “…” hoặc '…' — trùng một tên trong `titles` của works.yml hoặc một tên khác trong `TEN_KHAC`;
bản ghi tác phẩm có `same_as` (tên khác của một tác phẩm đã có, đợt 5.1) được thay bằng bản ghi gốc.
Khối không thuộc tác phẩm nào trong kho (phát biểu, văn kiện, thơ lẻ, tác phẩm chưa có bản ghi) ghi lý do ở
`work_note`. Trường `locator`, `work_note`, `license`, `evidence`, `verified` được giữ khi rút lại.
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
KEEP = ("locator", "work_note", "license", "evidence", "verified")
BLOCK = re.compile(r'^(?P<indent>[ \t]*)(?:!!!|\?\?\?\+?)[ \t]+quote(?:[ \t]+"(?P<title>.*)")?[ \t]*$')
FENCE = re.compile(r"^\s*(```|~~~)")
ITALIC = re.compile(r"\*([^*\n]+?)\*")
QUOTED = re.compile(r"“([^”\n]+)”|'([^'\n]+)'")
LZ_TRANSLATION = "(bản dịch của Logos)"
HEAD = ("# Kho trích dẫn. RÚT TỰ ĐỘNG bằng tools/kb_quotes.py từ khối !!! quote của Lõi viết tay và quote của hồ sơ;\n"
        "# chỉ locator, work_note, license, evidence, verified được sửa ở đây. Schema: schema/kb/quotes.schema.json. Lệch: verification/lech/quotes.md.\n")
# Tên khác (tên Việt, tên rút gọn) của tác phẩm đã có trong works.yml, đúng như viết trong tiêu đề khối → khóa tác
# phẩm. Đợt 5.2, theo claim tác giả/tác phẩm đã kiểm trong verification/evidence/quotes__*.json và tên Việt ghi trong
# hồ sơ data/people/*.yml. Tác phẩm chưa có bản ghi thì không thêm ở đây (works.yml đóng băng từ 5.1): ghi `work_note`.
TEN_KHAC = {
    "Biện hộ": "chua-ro.apologia",                                   # doc/platon-bien-ho.md
    "Biện hộ của Socrates": "chua-ro.apologia",                      # hồ sơ Socrates
    "Chỉ dẫn cho người hoang mang": "maimonides.dalalat-al-hairin",
    "Cư trần lạc đạo": "tran-nhan-tong.cu-tran-lac-dao-phu",          # bài kệ kết của bài phú
    "City of God": "augustine.de-civitate-dei",                       # bí danh works/chua-ro.city-of-god bỏ ở 7.1.1 lô 5
    "Confessions": "augustine.confessiones",                         # bí danh works/chua-ro.confessions bỏ ở 7.1.1 lô 5
    "Đạo đức học": "spinoza.ethica-ordine-geometrico-demonstrata",
    "Đạo đức kinh": "lao-tu.lao-tu",
    "Đạo đức Nicomachus": "aristotle.ethica-nicomachea",
    "Đơn tử luận": "leibniz.la-monadologie",
    "Khảo luận về hiểu biết của con người": "locke.an-essay-concerning-human-understanding",
    "Những châm ngôn chủ yếu": "epicurus.kuriai-doxai",
    "Suy niệm": "descartes.meditationes-de-prima-philosophia",        # doc/descartes-suy-niem.md
    "Suy niệm về Triết học Đệ nhất": "descartes.meditationes-de-prima-philosophia",
    "Thư gửi Menoeceus": "epicurus.letter-to-menoeceus",
    "Tổng luận Thần học": "aquinas.summa-theologiae",
    "Trung luận": "nagarjuna.mulamadhyamakakarika",
    "Tự thú": "augustine.confessiones",
}


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


def work_index(works: dict) -> dict[str, str]:
    """Tên đã chuẩn hóa → khóa tác phẩm: mọi tên trong `titles` của works.yml, rồi `TEN_KHAC`. Bản ghi có `same_as`
    trỏ về bản ghi gốc (theo chuỗi `same_as` tới bản ghi không còn `same_as`)."""
    def goc(k: str) -> str:
        seen = {k}
        while (works.get(k) or {}).get("same_as") and works[k]["same_as"] not in seen:
            k = works[k]["same_as"]
            seen.add(k)
        return k
    index: dict[str, str] = {}
    for k, w in works.items():
        for t in w["titles"]:
            index.setdefault(norm(t), goc(k))
    for name, k in TEN_KHAC.items():
        index.setdefault(norm(name), goc(k))
    return index


def work_name(title: str) -> str | None:
    """Tên tác phẩm trong tiêu đề: tên in nghiêng đầu tiên; không có chữ in nghiêng thì tên đầu tiên trong “…”/'…'."""
    m = ITALIC.search(title)
    if m:
        return m.group(1)
    m = QUOTED.search(title)
    return (m.group(1) or m.group(2)) if m else None


def work_of(title: str, index: dict[str, str]) -> str | None:
    name = work_name(title)
    return index.get(norm(name)) if name else None


def extract(root: Path = ROOT) -> tuple[dict, list[str]]:
    works = yaml.safe_load(WORKS.read_text(encoding="utf-8")) if WORKS.exists() else {}
    index = work_index(works or {})
    recs: dict[str, dict] = {}
    unkeyed: list[str] = []

    def put(base: str, rec: dict) -> str:
        key, n = base, 2
        while key in recs:
            key, n = f"{base}-{n}", n + 1
        recs[key] = rec
        return key

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
            rec = {"work": work_of(title, index), "title": title, "body": body,
                   "translator": "logos" if LZ_TRANSLATION in body else None,
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
        rec = {"work": work_of(q["source"], index), "title": q["source"], "original": q["orig"], "translation": q["vi"],
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
    order = ["work", "work_note", "locator", "title", "body", "original", "translation", "translator", "license",
             "url", "used_in", "evidence", "verified"]
    out = {k: {f: r[f] for f in order if f in r} for k, r in recs.items()}
    return HEAD + yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=1_000_000)


def render_lech(recs: dict, unkeyed: list[str]) -> str:
    """Mục mở: khối chưa ghép được tác phẩm và chưa có `work_note`. Tiêu đề không theo mẫu mà đã ghép tác phẩm hoặc
    có `work_note` thì đã xử lý (khóa `trich.*` giữ nguyên); khối cùng tác phẩm phân biệt bằng `locator`."""
    nowork = [k for k, r in recs.items() if not r["work"]]
    noted = [k for k in nowork if recs[k].get("work_note")]
    open_ = [k for k in nowork if not recs[k].get("work_note")]
    matched = [k for k in unkeyed if recs[k]["work"]]
    suffixed = [k for k in recs if re.search(r"-\d+$", k) and re.sub(r"-\d+$", "", k) in recs]
    L = ["# Danh sách lệch: trích dẫn", "",
         "Sinh bằng `python tools/kb_quotes.py`. Mở ở đợt 2; đợt con 5.2 ghép tác phẩm, ghi `work_note` và `locator`.", "",
         f"- {len(recs)} khối trích dẫn; {sum(1 for r in recs.values() if r['translator'] == 'logos')} có bản dịch của Logos.",
         f"- {len(recs) - len(nowork)} ghép được với tác phẩm trong works.yml; {len(noted)} không thuộc tác phẩm nào "
         f"trong kho (có `work_note`); {len(open_)} chưa xử lý.",
         f"- {sum(1 for r in recs.values() if r.get('locator'))} có `locator`.", "",
         f"## Mục mở: chưa ghép được tác phẩm, chưa có `work_note` ({len(open_)})", ""]
    L += [f"- `{k}`: \"{recs[k]['title']}\" (`{recs[k]['used_in'][0]}`)" for k in open_] or ["Không còn mục mở."]
    L += ["", f"## Đã xử lý: không thuộc tác phẩm nào trong kho, có `work_note` ({len(noted)})", ""]
    L += [f"- `{k}`: \"{recs[k]['title']}\" — {recs[k]['work_note']}" for k in noted]
    L += ["", f"## Đã xử lý: tiêu đề khối không theo mẫu \"Tác giả, *Tác phẩm*, vị trí\", đã ghép tác phẩm ({len(matched)})",
          "", "Khóa lấy từ phần đầu tiêu đề (`trich.*`), giữ nguyên khi tiêu đề chỉ thêm dấu in nghiêng.", ""]
    L += [f"- `{k}` → `{recs[k]['work']}`: \"{recs[k]['title']}\" (`{recs[k]['used_in'][0]}`)" for k in matched]
    L += ["", f"## Cùng tác giả và tác phẩm, nhiều khối ({len(suffixed)})", "",
          "Khóa thêm hậu tố; `locator` phân biệt các khối (`lint_quotes` báo khối chưa có `locator`).", ""]
    L += [f"- `{k}`: \"{recs[k]['title']}\" — `locator`: {recs[k].get('locator') or 'chưa có'}" for k in suffixed]
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
