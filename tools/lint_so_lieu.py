"""Linter số liệu khảo sát PhilPapers gõ tay (quyết định 3; rà soát 9/11/2026 mục 2.1; ban-giao/dot-5.md 5.2, 5.9).

    python tools/lint_so_lieu.py            # in các chỗ (chế độ cảnh báo, luôn thoát mã 0)
    python tools/lint_so_lieu.py --write    # ghi báo cáo verification/lint/lint_so_lieu.md
    python tools/lint_so_lieu.py --strict   # thoát mã 1 khi có vi phạm (từ đợt 5.9)

Số liệu PhilPapers chỉ có một chỗ: data/kb/philpapers-2020.json, in vào bài bằng `[[pp:…]]` (hooks/kb.py). Linter tìm
số % gõ tay trong Lõi viết tay ở ngữ cảnh khảo sát:
  - mục "Giới triết học ngày nay nghĩ gì", hộp "Tóm tắt 5 phút", dòng có chữ "PhilPapers", dòng nói "triết gia" cùng
    "chấp nhận"/"bác bỏ"/"nghiêng về"/"ủng hộ", hoặc số trùng giá trị của một câu khảo sát mà trang đã dùng;
  - bỏ qua: khối sinh, code, đích link, mục Nguồn, shortcode, số 0% và 100%.

Luật:
  - `go-tay`: số trùng một giá trị trong kho → đổi thành `[[pp:KHÓA]]%` (khóa gợi ý, ưu tiên câu trang đã dùng).
  - `ngoai-kho`: số không có trong kho → đối chiếu `tools/philpapers-2020.md`: số đúng mà kho thiếu thì thêm vào kho
    (có nguồn chính thức), số làm tròn thì viết rõ là làm tròn hoặc ghi miễn, số sai thì sửa.
  - `quiz`: số % trong câu hỏi, đáp án đúng hoặc lời giải của quiz mà kho không có. `quiz-bank.json` không mở shortcode
    nên quiz giữ số gõ tay, nhưng số phải khớp kho. Phương án nhiễu không kiểm.
  - `du-lieu`: số % trong `ghi_chu_khao_sat` của `docs/assets/data/thi-nghiem.json`, hoặc trong chữ của
    `tools/figures.py` (nhãn, alt, chú thích): nên đọc từ kho; số không có trong kho thì đối chiếu.
  - `mien-thua`: mục trong `data/style/so-lieu-allow.yml` không còn khớp chỗ nào (xóa mục).
Miễn: `data/style/so-lieu-allow.yml`, mỗi mục `page` (đường dẫn trong docs/), `text` (một đoạn của dòng chứa số; với quiz:
đúng chữ "câu N: số%" như báo cáo in), `reason`.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import yaml

from lz import ROOT, units
from lz.lint import Finding, core_pages, main_guard, masked_lines, run, unit_at

KB_FILE = Path("data") / "kb" / "philpapers-2020.json"
ALLOW_FILE = Path("data") / "style" / "so-lieu-allow.yml"
EXTRA_FILES = (Path("docs") / "assets" / "data" / "thi-nghiem.json", Path("tools") / "figures.py")

PCT = re.compile(r"(?<![\d,.])(\d{1,3}(?:,\d{1,2})?)\s?%")
SHORTCODE = re.compile(r"\[\[[a-z][a-z-]*:[^\]\s]+\]\]")
PP_REF = re.compile(r"\[\[pp:([a-z0-9][a-z0-9-]*)")
QUIZ = re.compile(r'<div class="oz-quiz"[^>]*>\s*<script type="application/json">\s*(.*?)\s*</script>\s*</div>', re.S)
SUMMARY = re.compile(r'^!!! summary "Tóm tắt 5 phút"')
CONTEXT = re.compile(r"PhilPapers")
CONTEXT_PAIR = (re.compile(r"triết gia"), re.compile(r"chấp nhận|bác bỏ|nghiêng về|ủng hộ"))
SURVEY_SECTION = "giới triết học ngày nay nghĩ gì"
SUFFIX = {"pct": "", "pct_exclusive": "/loai-tru", "pct_reject": "/bac-bo"}
RULES = {
    "go-tay": "% khảo sát gõ tay trùng số trong kho: đổi thành `[[pp:…]]%`",
    "ngoai-kho": "% trong ngữ cảnh khảo sát mà kho không có: đối chiếu số liệu chính thức",
    "quiz": "% trong câu hỏi, đáp án đúng hoặc lời giải của quiz mà kho không có",
    "du-lieu": "% khảo sát gõ tay trong dữ liệu luyện tập hoặc trong chữ của hình",
    "mien-thua": "mục miễn không còn khớp chỗ nào",
}


def fmt(v: float) -> str:
    return f"{v:.1f}".replace(".", ",")


def kb_values(data: dict) -> dict[str, list[str]]:
    """Giá trị in ra (một chữ số lẻ, dấu phẩy; hoặc `raw`) → các khóa shortcode cho ra giá trị đó."""
    out: dict[str, list[str]] = defaultdict(list)
    for q in data["questions"]:
        for o in q["options"]:
            for field, suf in SUFFIX.items():
                raw = (o.get("raw") or {}).get(field)
                if raw:
                    out[raw.rstrip("%").strip()].append(f"{q['id']}.{o['id']}{suf}")
                elif o.get(field) is not None:
                    out[fmt(o[field])].append(f"{q['id']}.{o['id']}{suf}")
    return dict(out)


def load_kb(root: Path = ROOT) -> dict[str, list[str]]:
    return kb_values(json.loads((root / KB_FILE).read_text(encoding="utf-8")))


def lookup(num: str, kb: dict[str, list[str]], prefer: set[str]) -> list[str]:
    """Khóa có giá trị bằng `num` ("59,2" hoặc "52" = "52,0"); câu trong `prefer` đứng trước."""
    keys = kb.get(num) or (kb.get(num + ",0") if "," not in num else None) or []
    return sorted(keys, key=lambda k: (k.split(".")[0] not in prefer, k))


def nearest(num: str, kb: dict[str, list[str]], prefer: set[str]) -> str:
    """Gợi ý khóa gần nhất (lệch ≤ 1) trong các câu trang đã dùng, cho số có thể là làm tròn."""
    try:
        x = float(num.replace(",", "."))
    except ValueError:
        return ""
    best = None
    for v, keys in kb.items():
        try:
            d = abs(float(v.replace(",", ".")) - x)
        except ValueError:
            continue
        for k in keys:
            if k.split(".")[0] in prefer and d <= 1.0 and (best is None or d < best[0]):
                best = (d, k, v)
    return f"; gần `[[pp:{best[1]}]]` ({best[2]})" if best else ""


def skip(num: str) -> bool:
    return num in ("0", "100")


def hint(keys: list[str]) -> str:
    more = f" (hoặc {len(keys) - 1} khóa khác cùng giá trị)" if len(keys) > 1 else ""
    return f"đổi thành `[[pp:{keys[0]}]]%`{more}"


def scan_page(path: str, raw: str, kb: dict[str, list[str]]) -> list[Finding]:
    us = units.split(path, raw)
    titles = {u.key: re.sub(r"\s*\{[^}]*\}\s*$", "", u.title or "").strip().rstrip("?").lower() for u in us}
    prefer = set(PP_REF.findall(raw))
    page_vals = {v for v, keys in kb.items() if any(k.split(".")[0] in prefer for k in keys)}
    out: list[Finding] = []

    # quiz: kiểm riêng, rồi xóa khỏi văn bản quét văn xuôi
    for m in QUIZ.finditer(raw):
        line = raw.count("\n", 0, m.start()) + 1
        try:
            items = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        for i, it in enumerate(items):
            opts = it.get("options") or []
            ans = it.get("answer")
            texts = [it.get("q", ""), it.get("explain", "")]
            if isinstance(ans, int) and 0 <= ans < len(opts):
                texts.append(opts[ans])
            for t in texts:
                for x in PCT.finditer(SHORTCODE.sub(" ", t)):
                    num = x.group(1)
                    if skip(num) or lookup(num, kb, prefer):
                        continue
                    out.append(Finding(path, line, unit_at(us, line), "quiz", f"câu {i + 1}: {num}%",
                                       "số không có trong kho: đối chiếu tools/philpapers-2020.md" + nearest(num, kb, prefer)))

    blanked = QUIZ.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), raw)
    lines = masked_lines(blanked, quotes=False, sources=True)
    in_box = False
    for no in range(1, len(lines)):
        line = lines[no]
        if SUMMARY.match(line):
            in_box = True
            continue
        if in_box and line.strip() and not line.startswith("    "):
            in_box = False
        text = SHORTCODE.sub(lambda g: " " * len(g.group(0)), line)
        unit = unit_at(us, no)
        context = (in_box or titles.get(unit, "").startswith(SURVEY_SECTION) or CONTEXT.search(text)
                   or all(p.search(text) for p in CONTEXT_PAIR))
        for x in PCT.finditer(text):
            num = x.group(1)
            if skip(num):
                continue
            keys = lookup(num, kb, prefer)
            if keys and (context or num in page_vals or num + ",0" in page_vals):
                out.append(Finding(path, no, unit, "go-tay", f"{num}%", hint(keys)))
            elif not keys and context:
                out.append(Finding(path, no, unit, "ngoai-kho", f"{num}%",
                                   "kho không có số này: đối chiếu tools/philpapers-2020.md" + nearest(num, kb, prefer)))
    return out


def scan_extra(rel: str, text: str, kb: dict[str, list[str]]) -> list[Finding]:
    out = []
    if rel.endswith(".json"):
        data = json.loads(text)
        for i, ex in enumerate(data.get("experiments", [])):
            note = ex.get("ghi_chu_khao_sat") or ""
            for x in PCT.finditer(note):
                num = x.group(1)
                if skip(num):
                    continue
                keys = lookup(num, kb, set())
                msg = (f"nên đọc từ kho ({hint(keys)})" if keys else "kho không có số này: đối chiếu tools/philpapers-2020.md")
                out.append(Finding(rel, 0, f"thi-nghiem/{ex.get('id', i)}", "du-lieu", f"{num}%", msg))
        return out
    for no, line in enumerate(text.split("\n"), start=1):
        for x in re.finditer(r"(?<![\d,.])(\d{1,3},\d)\s?%", line):
            keys = lookup(x.group(1), kb, set())
            msg = (f"nên đọc từ kho ({hint(keys)})" if keys else "kho không có số này: đối chiếu tools/philpapers-2020.md")
            out.append(Finding(rel, no, "", "du-lieu", f"{x.group(1)}%", msg))
    return out


def load_allow(root: Path = ROOT) -> list[dict]:
    f = root / ALLOW_FILE
    items = yaml.safe_load(f.read_text(encoding="utf-8")) if f.exists() else None
    items = items or []
    for it in items:
        if not all(isinstance(it.get(k), str) and it.get(k) for k in ("page", "text", "reason")):
            raise SystemExit(f"{ALLOW_FILE}: mỗi mục cần page, text, reason (chuỗi): {it}")
    return items


def apply_allow(findings: list[Finding], allow: list[dict], line_text) -> list[Finding]:
    used = [False] * len(allow)
    kept = []
    for f in findings:
        hit = None
        for i, a in enumerate(allow):
            if a["page"] == f.page and (a["text"] == f.found or (a["text"] in line_text(f)
                                                       and f.found.rstrip("%").split(": ")[-1] in a["text"])):
                hit = i
                break
        if hit is None:
            kept.append(f)
        else:
            used[hit] = True
    for i, a in enumerate(allow):
        if not used[i]:
            kept.append(Finding(str(ALLOW_FILE), 0, "", "mien-thua", f"{a['page']}: {a['text']}", "xóa mục miễn"))
    return kept


def collect():
    kb = load_kb()
    findings: list[Finding] = []
    texts: dict[str, list[str]] = {}
    for p in core_pages():
        raw = p.file().read_text(encoding="utf-8")
        texts[p.path] = raw.split("\n")
        findings += scan_page(p.path, raw, kb)
    for rel in EXTRA_FILES:
        f = ROOT / rel
        if f.exists():
            findings += scan_extra(rel.as_posix(), f.read_text(encoding="utf-8"), kb)

    def line_text(f: Finding) -> str:
        lines = texts.get(f.page)
        return lines[f.line - 1] if lines and 0 < f.line <= len(lines) else ""

    return apply_allow(findings, load_allow(), line_text)


def main(argv: list[str]) -> int:
    return run("lint_so_lieu", "Báo cáo linter số liệu khảo sát",
               "Sinh bằng `python tools/lint_so_lieu.py --write`. Phạm vi: Lõi viết tay, `thi-nghiem.json`, chữ trong "
               "`tools/figures.py`. Số liệu PhilPapers chỉ lấy từ `data/kb/philpapers-2020.json` (quyết định 3); số gõ tay trùng "
               "kho đổi thành `[[pp:…]]` sau khi `philpapers/*` đóng băng (ban-giao/dot-5.md 5.2).",
               RULES, collect, argv, __doc__)


if __name__ == "__main__":
    main_guard(main)
