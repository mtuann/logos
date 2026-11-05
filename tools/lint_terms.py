"""Linter thuật ngữ: cách dịch bị tránh và tên riêng sai trong Lõi viết tay (KE-HOACH.md mục 8).

    python tools/lint_terms.py            # in các chỗ vi phạm (chế độ cảnh báo, luôn thoát mã 0)
    python tools/lint_terms.py --write    # ghi báo cáo verification/lint/lint_terms.md
    python tools/lint_terms.py --strict   # thoát mã 1 khi có vi phạm (khi chuyển sang chặn)

Luật đọc từ data/style/terms-policy.yml (sinh từ HUONG-DAN-VIET.md mục 3 bằng tools/terms_policy.py).
Không kiểm: trích nguyên văn (!!! quote, > …), chữ trong ngoặc kép, chữ in nghiêng, mục Nguồn, code, đích link.
Có kiểm: thân bài, tiêu đề, quiz, `title` và `description` trong front matter.
"""

from __future__ import annotations

import re
import unicodedata

import yaml

from lz import ROOT, units
from lz.lint import Finding, blank, core_pages, main_guard, masked_lines, run, unit_at

POLICY = ROOT / "data" / "style" / "terms-policy.yml"
ITALIC = re.compile(r"(?<![*\w])\*(?!\*)[^*\n]+?(?<!\*)\*(?![*\w])|(?<![_\w])_(?!_)[^_\n]+?_(?![_\w])")
QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”')
RULES = {
    "thuat-ngu": "dùng cách dịch khác thay cho thuật ngữ bắt buộc",
    "thuat-ngu-mo-ho": "cách dịch khác trùng một từ thường hay thuật ngữ khác: người đọc xem lại, thường là đúng",
    "ten-rieng": "tên riêng không theo cách phiên quy định (ví dụ Plato → Platon)",
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


def collect():
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
