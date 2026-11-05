"""Đợt 3, việc 3.5: số liệu PhilPapers gõ tay → [[pp:…]] (hooks/kb.py, data/kb/philpapers-2020.json).

    python tools/migrate/dot3_philpapers.py            # thay, ghi verification/lech/philpapers-bang.md
    python tools/migrate/dot3_philpapers.py --dry-run  # chỉ in số liệu thống kê

Phạm vi: trang viết tay (trừ them/cap-nhat.md, nhật ký thay đổi).
  1. Bảng PhilPapers (có cột %, "Chấp nhận hoặc nghiêng về", "Loại trừ", "Chỉ chọn lựa chọn này"). Hai bố cục:
     cột đầu là "Câu hỏi…" (mỗi nhóm dòng một câu), hoặc tiêu đề bảng chính là câu hỏi. Ghép câu của bài với
     câu trong JSON theo tiêu đề (bỏ ngoặc, dấu nhấn, phần "câu chính, n ≈ …"), không được thì theo nhãn lựa chọn
     và số của mọi dòng. Ghép lựa chọn theo nhãn (bỏ ngoặc, dấu nhấn). Một ô chỉ được thay khi chữ trong ô bằng
     đúng chữ shortcode in ra; "n ≈ 1.760" trong ô câu hỏi cũng vậy.
  2. Số tổng của khảo sát trong văn xuôi có nhắc khảo sát/PhilPapers: 1.785 triết gia (người tham gia), 100 câu
     hỏi, 40 câu chính, 60 câu bổ sung, "ngẫu nhiên 10 câu".
Không thay: % và n trong văn xuôi (gắn với câu nào là việc đọc hiểu: đợt 5, `lint_facts`), ô lệch JSON.
Mọi chỗ còn gõ tay ghi vào verification/lech/philpapers-bang.md. Phép thay đi qua thay_shortcode.apply (mở lại
shortcode phải ra đúng dòng cũ). Chạy lại: ô đã thay không còn số, nên không đổi gì.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter

from thay_shortcode import DOCS, ROOT, apply

sys.path.insert(0, str(ROOT / "tools"))
from lz import registry  # noqa: E402

JSON = ROOT / "data" / "kb" / "philpapers-2020.json"
LECH = ROOT / "verification" / "lech" / "philpapers-bang.md"
SEP = re.compile(r"^\|[-| :]+\|\s*$")
NUM = re.compile(r"(?<![\d,.])\d+(?:,\d+)?(?![\d,])")
N_IN_Q = re.compile(r"n ≈ (\d{1,3}(?:\.\d{3})*)")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def fmt(x) -> str:
    return f"{x:.1f}".replace(".", ",")


def fmt_n(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def norm(s: str, drop_paren: bool = True) -> str:
    s = LINK.sub(r"\1", unicodedata.normalize("NFC", s))
    s = re.sub(r"\s+[—–-]\s+câu (?:chính|bổ sung).*$", "", s)
    s = re.sub(r"\((?:[^()]*?(?:câu chính|câu bổ sung|n ≈|PhilPapers)[^()]*)\)", "", s)
    if drop_paren:
        s = re.sub(r"\([^()]*\)", "", s)
    s = re.sub(r"[*\"“”‘’'?:]", "", s).casefold()
    return " ".join(s.split())


def value(o: dict, field: str) -> str | None:
    raw = o.get("raw", {}).get(field)
    return raw or (fmt(o[field]) if o.get(field) is not None else None)


def key_of(qid: str, o: dict, field: str) -> str:
    return f"[[pp:{qid}.{o['id']}{ {'pct': '', 'pct_reject': '/bac-bo', 'pct_exclusive': '/loai-tru'}[field]}]]"


def col_role(head: str) -> str | None:
    h = head.casefold()
    if "loại trừ" in h or "chỉ chọn" in h:
        return "pct_exclusive"
    if h.strip() == "%" or "chấp nhận" in h:
        return "pct"
    return None


def tables(text: str):
    """(dòng tiêu đề, [ô tiêu đề], [(số dòng, [ô])]) cho mọi bảng có cột số liệu PhilPapers."""
    lines = text.split("\n")
    i = 0
    while i + 1 < len(lines):
        if lines[i].startswith("|") and SEP.match(lines[i + 1]):
            head = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            j, rows = i + 2, []
            while j < len(lines) and lines[j].startswith("|"):
                rows.append((j + 1, lines[j]))
                j += 1
            if any(col_role(h) for h in head[1:]):
                yield i + 1, head, rows
            i = j
        else:
            i += 1


def cells(line: str) -> list[str]:
    return line.strip().strip("|").split("|")


def match_option(q: dict, label: str):
    lab = norm(label)
    hits = [o for o in q["options"] if norm(o["label_vi"]) == lab]
    if not hits:
        hits = [o for o in q["options"] if norm(o["label_vi"]).startswith(lab) or lab.startswith(norm(o["label_vi"]))]
    return hits[0] if len(hits) == 1 else None


def first_value(cell: str) -> str:
    m = NUM.search(cell)
    return m.group(0) if m else ""


DONE = re.compile(r"\[\[pp:([a-z0-9-]+)[./]")


def pick_question(title: str, group: list[tuple[str, list[str]]], questions: list[dict]):
    """group: [(nhãn, [ô số])] với ô số đầu là cột pct."""
    done = {m.group(1) for _, vals in group for v in vals for m in DONE.finditer(v)} | \
        {m.group(1) for m in DONE.finditer(title)}
    if len(done) == 1:   # đã thay ở lần chạy trước
        q = next((q for q in questions if q["id"] in done), None)
        if q:
            return q, "da-thay"
    t = norm(title)
    by_title = [q for q in questions if norm(q["title_vi"]) == t
                or (len(t) > 3 and (norm(q["title_vi"]).startswith(t) or t.startswith(norm(q["title_vi"]))))]

    def score(q):
        n = 0
        for label, vals in group:
            o = match_option(q, label)
            if o and vals and first_value(vals[0]) and first_value(vals[0]) == value(o, "pct"):
                n += 1
        return n
    if by_title:
        best = max(by_title, key=score)
        return best, "tieu-de"
    rows = sum(1 for _, vals in group if vals and first_value(vals[0]))
    scored = sorted(((score(q), q["id"], q) for q in questions), key=lambda x: -x[0])
    if rows >= 2 and scored[0][0] == rows and (len(scored) < 2 or scored[1][0] < rows):
        return scored[0][2], "so-lieu"
    return None, None


def plan_tables(page: str, text: str, questions: list[dict], lech: list, stats: Counter):
    subs = []
    for hl, head, rows in tables(text):
        layout_a = head[0].casefold().startswith("câu hỏi")
        roles = [col_role(h) for h in head]
        # nhóm dòng theo câu hỏi
        groups: list[tuple[str, int | None, list]] = []
        if layout_a:
            for ln, line in rows:
                c = cells(line)
                if c[0].strip():
                    groups.append((c[0].strip(), ln, []))
                if groups:
                    groups[-1][2].append((ln, line, c, 1))
        else:
            groups.append((head[0], None, [(ln, line, cells(line), 0) for ln, line in rows]))
            title_line = hl
        for title, qline, rws in groups:
            label_col = rws[0][3]
            group = [(c[label_col].strip(), [c[k] for k in range(label_col + 1, len(c)) if k < len(roles) and roles[k]])
                     for _, _, c, _ in rws]
            stats["cau"] += 1
            if any((page, ln) in MANUAL_LINES for ln, *_ in rws):
                stats["ghep-tay"] += 1
                continue
            q, how = pick_question(title, group, questions)
            if not q:
                stats["cau-chua-ghep"] += 1
                lech.append(f"- `{page}:{qline or title_line}` câu chưa ghép được: \"{title}\"")
                continue
            stats[f"ghep-{how}"] += 1
            # n trong ô câu hỏi (bố cục A: ô đầu của dòng đầu nhóm) hoặc tiêu đề bảng (bố cục B: dòng tiêu đề)
            n_cell = None
            m = N_IN_Q.search(title)
            if m and "n" in q:
                if m.group(1) == fmt_n(q["n"]):
                    n_cell = (m.group(0), f"n ≈ [[pp:{q['id']}/n]]")
                    stats["n-thay"] += 1
                else:
                    stats["n-lech"] += 1
                    lech.append(f"- `{page}:{qline or title_line}` `{q['id']}/n`: bài ghi {m.group(1)}, "
                                f"JSON {fmt_n(q['n'])}")
            if "[[pp:" in title:
                stats["n-thay"] += 1
            if n_cell and not layout_a:
                hline = text.split("\n")[title_line - 1]
                subs.append((page, title_line, hline, hline.replace(n_cell[0], n_cell[1], 1)))
            for idx, (ln, line, c, lc) in enumerate(rws):
                label = c[lc].strip()
                o = match_option(q, label)
                new = list(c)
                if n_cell and layout_a and idx == 0:
                    new[0] = new[0].replace(n_cell[0], n_cell[1], 1)
                for k in range(lc + 1, len(c)):
                    role = roles[k] if k < len(roles) else None
                    if role and "[[pp:" in c[k]:
                        stats["o-so"] += 1
                        stats["o-thay"] += 1
                        if NUM.search(re.sub(r"\[\[pp:[^\]]*\]\]", "", c[k])):
                            raise SystemExit(f"{page}:{ln}: ô vừa có shortcode vừa có số gõ tay")
                        continue
                    if not role or not NUM.search(c[k]):
                        continue
                    stats["o-so"] += 1
                    if not o:
                        stats["o-chua-ghep-lua-chon"] += 1
                        lech.append(f"- `{page}:{ln}` `{q['id']}`: lựa chọn \"{label}\" chưa ghép được")
                        continue
                    fields = [role] if role == "pct_exclusive" else ["pct", "pct_reject"]
                    toks = list(NUM.finditer(c[k]))
                    out, pos = [], 0
                    for tok, field in zip(toks, fields):
                        want = value(o, field)
                        out.append(c[k][pos:tok.start()])
                        if want == tok.group(0):
                            out.append(key_of(q["id"], o, field))
                            stats["o-thay"] += 1
                        else:
                            out.append(tok.group(0))
                            stats["o-lech"] += 1
                            lech.append(f"- `{page}:{ln}` `{q['id']}.{o['id']}` ({field}): bài ghi \"{tok.group(0)}\", "
                                        f"JSON {want if want is not None else 'không có'}")
                        pos = tok.end()
                    out.append(c[k][pos:])
                    new[k] = "".join(out)
                if new != c:
                    lead = line[:len(line) - len(line.lstrip())]
                    rebuilt = lead + "|" + "|".join(new) + "|" + line[len(line.rstrip()):]
                    if rebuilt.strip().strip("|").split("|") != new:
                        raise SystemExit(f"{page}:{ln}: không dựng lại được dòng bảng")
                    subs.append((page, ln, line, rebuilt))
    return subs


# Bảng đảo cấu trúc: lựa chọn của câu "Những tâm trí khác" đứng ở chỗ câu hỏi, "Chấp nhận / bác bỏ" là nhãn.
# Ghép tay (trang, dòng, chữ cũ của ô, lựa chọn, trường của từng số trong ô); vẫn qua phép kiểm của apply.
OTHER_MINDS = "nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha"
MANUAL = [
    ("cau-hoi/tam-tri-va-ai.md", 110, "3,4 / 82,4", "he-thong-ai-hien-tai-nam-2020", ["pct", "pct_reject"]),
    ("cau-hoi/tam-tri-va-ai.md", 111, "39,2 / 26,8", "he-thong-ai-tuong-lai", ["pct", "pct_reject"]),
    ("cau-hoi/cong-nghe-ai.md", 98, "3,4", "he-thong-ai-hien-tai-nam-2020", ["pct"]),
    ("cau-hoi/cong-nghe-ai.md", 99, "82,4", "he-thong-ai-hien-tai-nam-2020", ["pct_reject"]),
    ("cau-hoi/cong-nghe-ai.md", 100, "39,2", "he-thong-ai-tuong-lai", ["pct"]),
    ("cau-hoi/cong-nghe-ai.md", 101, "26,8", "he-thong-ai-tuong-lai", ["pct_reject"]),
]


MANUAL_LINES = {(p, ln) for p, ln, *_ in MANUAL}


def plan_manual(questions: list[dict], stats: Counter) -> list:
    q = next(q for q in questions if q["id"] == OTHER_MINDS)
    subs = []
    for page, ln, old, oid, fields in MANUAL:
        line = (DOCS / page).read_text(encoding="utf-8").split("\n")[ln - 1]
        o = next(o for o in q["options"] if o["id"] == oid)
        new = " / ".join(key_of(q["id"], o, f) for f in fields)
        if f"| {new} |" in line:
            stats["o-thay"] += len(fields)   # đã thay ở lần chạy trước
            continue
        if f"| {old} |" not in line:
            raise SystemExit(f"{page}:{ln}: không thấy ô {old!r}")
        subs.append((page, ln, line, line.replace(f"| {old} |", f"| {new} |", 1)))
        stats["o-thay"] += len(fields)
    stats["o-so"] += sum(len(f) for *_, f in MANUAL)
    return subs


SURVEY = [  # (regex trên dòng, khóa); chỉ ở dòng có nhắc khảo sát / PhilPapers
    (re.compile(r"(?<![\d.,])1\.785(?=(?:\*\*)? (?:triết gia|người tham gia))"), "nguoi-tra-loi"),
    (re.compile(r"(?<![\d.,])100(?=(?:\*\*)? câu hỏi)"), "so-cau"),
    (re.compile(r"(?<![\d.,])40(?= câu chính)"), "cau-chinh"),
    (re.compile(r"(?<![\d.,])60(?= câu bổ sung)"), "cau-bo-sung"),
    (re.compile(r"(?<=ngẫu nhiên )10(?= câu)"), "cau-bo-sung-moi-nguoi"),
]
CONTEXT = re.compile(r"khảo sát|PhilPapers", re.I)
PROSE_NUM = re.compile(r"\d+(?:,\d+)?%|(?<![\d.,])\d{1,3}(?:\.\d{3})+(?= (?:triết gia|người))|(?<![\d.,])\d{3}(?= (?:triết gia|người))")


def plan_prose(page: str, text: str, stats: Counter, prose_left: list):
    subs = []
    in_pp = False
    for ln, line in enumerate(text.split("\n"), start=1):
        if line.startswith("## "):
            in_pp = "gioi-triet-hoc-ngay-nay-nghi-gi" in line
        if line.lstrip().startswith("|"):
            continue
        new = line
        if CONTEXT.search(line):
            for rx, key in SURVEY:
                new = rx.sub(f"[[pp:khao-sat/{key}]]", new)
        stats["tong-thay"] += new.count("[[pp:khao-sat/")   # gồm cả chỗ đã thay ở lần chạy trước
        if new != line:
            subs.append((page, ln, line, new))
        if in_pp:
            left = PROSE_NUM.findall(new)
            if left:
                prose_left.append((page, ln, len(left)))
    return subs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    data = json.loads(JSON.read_text(encoding="utf-8"))
    questions = data["questions"]
    stats: Counter = Counter()
    lech: list[str] = []
    prose_left: list = []
    subs = []
    for p in registry.load(ROOT).select(generated=False):
        if p.path == "them/cap-nhat.md":
            continue
        text = (DOCS / p.path).read_text(encoding="utf-8")
        subs += plan_tables(p.path, text, questions, lech, stats)
        subs += plan_prose(p.path, text, stats, prose_left)
    subs += plan_manual(questions, stats)
    seen = Counter((page, ln) for page, ln, _, _ in subs)
    if max(seen.values(), default=1) > 1:
        raise SystemExit(f"một dòng có hai phép thay: {[k for k, v in seen.items() if v > 1]}")
    done, pages = apply(subs, args.dry_run)
    print(f"{'(thử) ' if args.dry_run else ''}Bảng: {stats['cau']} câu (ghép theo tiêu đề {stats['ghep-tieu-de']}, "
          f"theo số liệu {stats['ghep-so-lieu']}, ghép tay {stats['ghep-tay']}, đã thay trước {stats['ghep-da-thay']}, chưa ghép {stats['cau-chua-ghep']}); ô số {stats['o-so']}: thay "
          f"{stats['o-thay']}, lệch {stats['o-lech']}, chưa ghép lựa chọn {stats['o-chua-ghep-lua-chon']}; n thay "
          f"{stats['n-thay']}, lệch {stats['n-lech']}. Số tổng trong văn xuôi: thay {stats['tong-thay']}. "
          f"Dòng đổi: {done}, trang đổi: {pages}.")
    if not args.dry_run:
        write_lech(stats, lech, prose_left)
    return 0


def write_lech(stats: Counter, lech: list[str], prose_left: list) -> None:
    L = ["# Danh sách lệch: số liệu PhilPapers còn gõ tay trong trang", "",
         "Sinh bằng `python tools/migrate/dot3_philpapers.py` (đợt 3, việc 3.5). Đầu vào cho đợt 5: ô nào ghi khác JSON "
         "thì đối chiếu với Bảng 1–2 của bài báo, sửa bài hoặc JSON, rồi thay bằng `[[pp:…]]`.", "",
         f"- Bảng: {stats['cau']} câu; ô số {stats['o-so']}, đã thay {stats['o-thay']}; n trong ô câu hỏi đã thay "
         f"{stats['n-thay']}.",
         f"- Số tổng của khảo sát trong văn xuôi đã thay: {stats['tong-thay']}.", "",
         f"## Ô và câu chưa thay ({len(lech)})", ""]
    L += lech or ["(không có)"]
    L += ["", f"## Số liệu trong văn xuôi mục \"Giới triết học ngày nay nghĩ gì\" còn gõ tay ({sum(n for *_, n in prose_left)} "
          f"chỗ ở {len(prose_left)} dòng)", "",
          "% và số người trả lời trong câu văn: gắn với câu và lựa chọn nào là việc đọc hiểu, không làm cơ học. "
          "`lint_facts` (đợt 5) đối chiếu với JSON.", ""]
    L += [f"- `{p}:{ln}`: {n}" for p, ln, n in prose_left]
    LECH.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
