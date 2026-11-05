"""Số liệu PhilPapers 2020: data/kb/philpapers-2020.json là nguồn; tools/philpapers-2020.md sinh từ đó
(ban-giao/dot-2.md việc 2.7; KE-HOACH.md mục 10).

    python tools/kb_philpapers.py              # sinh lại tools/philpapers-2020.md từ JSON
    python tools/kb_philpapers.py --check      # mã thoát 1 khi .md lệch JSON (CI)
    python tools/kb_philpapers.py --import-md  # một lần (đợt 2): đọc .md hiện có, ghi JSON, kiểm sinh lại giống từng byte

JSON: `source.preamble` và `source.footer` là phần chữ trước và sau hai bảng, giữ nguyên văn. Mỗi câu: `id` (slug của
nhãn tiếng Việt; file gốc không có nhãn tiếng Anh), `title_vi`, `table` (1 = câu chính, 2 = câu bổ sung), `n` (≈, làm
tròn hàng chục), các lựa chọn: `id`, `label_vi`, `pct` (% chấp nhận hoặc nghiêng về, tính bao gồm), `pct_reject`
(câu cho phép bác bỏ từng lựa chọn), `pct_exclusive` (cột Loại trừ), và `raw` cho ô ghi lệch quy ước một chữ số
thập phân (giữ chữ gốc; liệt kê ở verification/lech/philpapers.md). Khóa số liệu: `<câu>.<lựa chọn>`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from kb_sources import slug

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "tools" / "philpapers-2020.md"
JSON = ROOT / "data" / "kb" / "philpapers-2020.json"
TABLE_TITLES = {1: "## Câu hỏi chính (Bảng 1)", 2: "## Câu hỏi bổ sung (Bảng 2)"}
TABLE_HEAD = "| Câu hỏi | Lựa chọn | % | Loại trừ |\n|---|---|---|---|"
N_SUFFIX = re.compile(r"^(?P<title>.*) \(n ≈ (?P<n>[\d.]+)\)$")


def num(cell: str) -> float | None:
    return float(cell.replace(",", ".")) if cell else None


def fmt(x: float | None) -> str:
    return "" if x is None else f"{x:.1f}".replace(".", ",")


def fmt_n(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def parse_md(text: str) -> dict:
    t1 = text.index(TABLE_TITLES[1])
    t2 = text.index(TABLE_TITLES[2])
    preamble = text[:t1]
    questions = []
    rest_after = ""
    for table, start, end in ((1, t1, t2), (2, t2, len(text))):
        block = text[start:end]
        lines = block.split("\n")
        assert lines[0] == TABLE_TITLES[table] and "\n".join(lines[2:4]) == TABLE_HEAD, lines[:4]
        i = 4
        while i < len(lines) and lines[i].startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            q, label, pct, excl = cells
            if q:
                m = N_SUFFIX.match(q)
                title, n = (m.group("title"), int(m.group("n").replace(".", ""))) if m else (q, None)
                questions.append({"id": slug(title), "title_vi": title, "table": table, "n": n, "options": []})
            accept, _, reject = pct.partition(" / ")
            opt = {"id": slug(label), "label_vi": label, "pct": num(accept),
                   "pct_reject": num(reject), "pct_exclusive": num(excl)}
            raw = {f: cell for f, cell in (("pct", accept), ("pct_reject", reject), ("pct_exclusive", excl))
                   if cell and fmt(num(cell)) != cell}
            if raw:   # ô không theo quy ước một chữ số thập phân: giữ chữ gốc, ghi vào danh sách lệch
                opt["raw"] = raw
            questions[-1]["options"].append(opt)
            i += 1
        if table == 2:
            rest_after = "\n".join(lines[i:])
        else:
            assert all(not ln for ln in lines[i:]), lines[i:]
    for q in questions:
        if q["n"] is None:
            del q["n"]
    return {"source": {"preamble": preamble, "footer": rest_after}, "questions": questions}


def cell(o: dict, f: str) -> str:
    return o.get("raw", {}).get(f) or fmt(o.get(f))


def render_md(data: dict) -> str:
    out = [data["source"]["preamble"].rstrip("\n"), ""]
    for table in (1, 2):
        out += [TABLE_TITLES[table], "", TABLE_HEAD]
        for q in (q for q in data["questions"] if q["table"] == table):
            head = q["title_vi"] + (f" (n ≈ {fmt_n(q['n'])})" if "n" in q else "")
            for i, o in enumerate(q["options"]):
                pct = cell(o, "pct") + (f" / {cell(o, 'pct_reject')}" if o.get("pct_reject") is not None else "")
                out.append(f"| {head if i == 0 else ''} | {o['label_vi']} | {pct} | {cell(o, 'pct_exclusive')} |")
        out.append("")
    return "\n".join(out) + data["source"]["footer"]


def write_lech(data: dict) -> None:
    raws = [(q, o) for q in data["questions"] for o in q["options"] if o.get("raw")]
    L = ["# Danh sách lệch: số liệu PhilPapers 2020", "",
         "Sinh bằng `python tools/kb_philpapers.py --import-md`. Đầu vào cho đợt 5 (đợt con 5.2).", "",
         f"- {len(data['questions'])} câu (câu chính {sum(q['table'] == 1 for q in data['questions'])}, "
         f"câu bổ sung {sum(q['table'] == 2 for q in data['questions'])}); khảo sát có 100 câu: còn thiếu "
         f"{100 - len(data['questions'])} câu. Bổ sung cần mở Bảng 1–2 của bài báo (DOI 10.3998/phimp.2109) và dịch nhãn: "
         "việc nội dung, để đợt 5.",
         "- id câu và lựa chọn là slug của nhãn tiếng Việt (file gốc không có nhãn tiếng Anh).", "",
         f"## Ô không theo quy ước một chữ số thập phân ({len(raws)})", "",
         "Có thể bài báo in số tròn, hoặc chép thiếu: đối chiếu với bảng gốc.", ""]
    L += [f"- `{q['id']}.{o['id']}`: " + ", ".join(f"{f} = \"{v}\"" for f, v in o["raw"].items()) for q, o in raws]
    out = ROOT / "verification" / "lech" / "philpapers.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")


def dump_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=1) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="báo lỗi khi .md lệch JSON")
    g.add_argument("--import-md", action="store_true", help="một lần: .md hiện có → JSON")
    args = ap.parse_args(argv)
    if args.import_md:
        md = MD.read_text(encoding="utf-8")
        data = parse_md(md)
        if render_md(data) != md:
            print("Không sinh lại được .md giống từng byte; không ghi JSON.", file=sys.stderr)
            return 1
        JSON.write_text(dump_json(data), encoding="utf-8")
        write_lech(data)
        print(f"Đã ghi {JSON.relative_to(ROOT)} ({len(data['questions'])} câu); sinh lại .md giống từng byte.")
        return 0
    data = json.loads(JSON.read_text(encoding="utf-8"))
    text = render_md(data)
    if args.check:
        if MD.read_text(encoding="utf-8") != text:
            print("tools/philpapers-2020.md lệch data/kb/philpapers-2020.json — chạy: python tools/kb_philpapers.py",
                  file=sys.stderr)
            return 1
        print(f"Số liệu PhilPapers: .md khớp JSON ({len(data['questions'])} câu).")
        return 0
    MD.write_text(text, encoding="utf-8")
    print(f"Đã sinh {MD.relative_to(ROOT)} từ JSON ({len(data['questions'])} câu).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
