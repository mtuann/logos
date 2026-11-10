"""Linter thuật ngữ: cách dịch bị tránh và tên riêng sai trong Lõi viết tay (KE-HOACH.md mục 8).

    python tools/lint_terms.py            # in các chỗ vi phạm (chế độ cảnh báo, luôn thoát mã 0)
    python tools/lint_terms.py --write    # ghi báo cáo verification/lint/lint_terms.md
    python tools/lint_terms.py --strict   # thoát mã 1 khi có vi phạm (khi chuyển sang chặn)

Luật đọc từ data/style/terms-policy.yml (sinh từ HUONG-DAN-VIET.md mục 3 bằng tools/terms_policy.py).
Không kiểm: trích nguyên văn (!!! quote, > …), chữ trong ngoặc kép, chữ in nghiêng, mục Nguồn, code, đích link.
Có kiểm: thân bài, tiêu đề, quiz, `title` và `description` trong front matter.

Miễn (đợt 5.3): `data/style/terms-allow.yml`, chỉ cho luật `thuat-ngu-mo-ho` (cách dịch khác trùng từ thường hay thuật
ngữ khác, người đọc đã xem từng chỗ). Mỗi mục `page`, `word`, `count` (số chỗ đã xem), `reason`. Số chỗ đổi thì linter
báo `mien-lech` (xem lại chỗ mới rồi sửa `count`, hoặc sửa chữ); mục không còn chỗ nào thì báo `mien-thua`.
"""

from __future__ import annotations

import re
import unicodedata

import yaml

from lz import ROOT, units
from lz.lint import Finding, blank, core_pages, main_guard, masked_lines, run, unit_at

POLICY = ROOT / "data" / "style" / "terms-policy.yml"
ALLOW = ROOT / "data" / "style" / "terms-allow.yml"
ITALIC = re.compile(r"(?<![*\w])\*(?!\*)[^*\n]+?(?<!\*)\*(?![*\w])|(?<![_\w])_(?!_)[^_\n]+?_(?![_\w])")
QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”')
RULES = {
    "thuat-ngu": "dùng cách dịch khác thay cho thuật ngữ bắt buộc",
    "thuat-ngu-mo-ho": "cách dịch khác trùng một từ thường hay thuật ngữ khác: người đọc xem lại, thường là đúng",
    "ten-rieng": "tên riêng không theo cách phiên quy định (ví dụ Plato → Platon)",
    "mien-lech": "số chỗ của một mục miễn đã đổi: xem lại các chỗ, rồi sửa `count` hoặc sửa chữ",
    "mien-thua": "mục miễn không còn khớp chỗ nào (xóa mục)",
}


def compile_rules(policy: dict) -> list[tuple[re.Pattern, str, str, str]]:
    """(regex, luật, chữ tìm, gợi ý)."""
    out = []
    for t in policy["terms"]:
        for a in t["avoid"]:
            ctx = t.get("context", {}).get(a, {})
            before = "".join(f"(?<!{re.escape(x)})" for x in ctx.get("not_after", []))
            after = "".join(f"(?!{re.escape(x)})" for x in ctx.get("not_before", []))
            rx = re.compile(before + r"(?<!\w)" + re.escape(a) + r"(?!\w)" + after, re.I)
            rule = "thuat-ngu-mo-ho" if a in t.get("ambiguous", {}) else "thuat-ngu"
            hint = f"dùng \"{t['use']}\" ({t['en']})"
            if rule == "thuat-ngu-mo-ho":
                hint += f"; {t['ambiguous'][a]}"
            out.append((rx, rule, a, hint))
    for n in policy["names"]:
        for a in n["avoid"]:
            out.append((re.compile(r"(?<!\w)" + re.escape(a) + r"(?!\w)"), "ten-rieng", a, f"viết \"{n['use']}\""))
    return out


def prose(line: str) -> str:
    line = ITALIC.sub(lambda m: blank(m.group(0)), line)
    return QUOTED.sub(lambda m: blank(m.group(0)), line)


def load_allow() -> list[dict]:
    items = (yaml.safe_load(ALLOW.read_text(encoding="utf-8")) or []) if ALLOW.exists() else []
    for it in items:
        if not (all(isinstance(it.get(k), str) and it.get(k) for k in ("page", "word", "reason"))
                and isinstance(it.get("count"), int)):
            raise SystemExit(f"{ALLOW.relative_to(ROOT)}: mỗi mục cần page, word, reason (chuỗi) và count (số): {it}")
    return items


def apply_allow(findings: list[Finding], allow: list[dict]) -> list[Finding]:
    groups: dict[tuple[str, str], list[Finding]] = {}
    for f in findings:
        if f.rule == "thuat-ngu-mo-ho":
            groups.setdefault((f.page, f.found.lower()), []).append(f)
    drop: set[int] = set()
    extra: list[Finding] = []
    rel = str(ALLOW.relative_to(ROOT))
    for a in allow:
        g = groups.get((a["page"], a["word"].lower()))
        if not g:
            extra.append(Finding(rel, 0, "", "mien-thua", f"{a['page']}: {a['word']}", "xóa mục miễn"))
        elif len(g) != a["count"]:
            extra.append(Finding(rel, 0, "", "mien-lech", f"{a['page']}: {a['word']} — {len(g)} chỗ, miễn ghi {a['count']}",
                                 "xem lại các chỗ của từ này trong trang"))
        else:
            drop.update(id(f) for f in g)
    return [f for f in findings if id(f) not in drop] + extra


def collect():
    return apply_allow(list(collect_raw()), load_allow())


def collect_raw():
    policy = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    rules = compile_rules(policy)
    skip = set(policy["exceptions"]["pages"])
    for p in core_pages():
        if p.path in skip:
            continue
        raw = p.file().read_text(encoding="utf-8")
        us = units.split(p.path, raw)
        for no, line in enumerate(masked_lines(raw, meta=("title", "description"))):
            if not line.strip():
                continue
            text = prose(unicodedata.normalize("NFC", line))
            for rx, rule, word, hint in rules:
                for m in rx.finditer(text):
                    yield Finding(p.path, no, unit_at(us, no), rule, m.group(0), hint)


def main(argv: list[str]) -> int:
    return run("lint_terms", "Báo cáo linter thuật ngữ",
               "Sinh bằng `python tools/lint_terms.py --write`. Phạm vi: Lõi viết tay. "
               "Luật: `data/style/terms-policy.yml` (từ `HUONG-DAN-VIET.md` mục 3). "
               "Đây là báo cáo nền của đợt 1: chỉ ghi lại, sửa ở đợt 5.",
               RULES, collect, argv, __doc__)


if __name__ == "__main__":
    main_guard(main)
