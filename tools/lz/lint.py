"""Phần chung của các linter (lint_terms, lint_volatile, lint_structure; KE-HOACH.md mục 8).

Mỗi linter tạo danh sách `Finding` rồi gọi `run()`: in tóm tắt, tùy chọn ghi báo cáo Markdown vào
verification/lint/<tên>.md (chạy lại cho cùng kết quả, không ghi ngày giờ), và thoát mã 1 ở chế độ `--strict`.
Linter mới chạy ở chế độ cảnh báo (không `--strict`) hai tuần rồi mới chuyển sang chặn.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from . import ROOT, registry, units

FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
GEN_BLOCK = re.compile(r"<!-- (gen|fig):(\S+) -->.*?<!-- /\1:\2 -->", re.S)
FENCE_LINE = re.compile(r"^\s*(`{3,}|~{3,})")
ADMONITION = re.compile(r"^(\s*)(?:!!!|\?\?\?\+?)\s+([\w-]+)")
H2 = re.compile(r"^## +(.+?)\s*$")
LINK_TARGET = re.compile(r"\]\([^)]*\)|<(?:https?|mailto):[^>]+>|https?://\S+")
INLINE_CODE = re.compile(r"`[^`\n]*`")


@dataclass(frozen=True)
class Finding:
    page: str          # đường dẫn trong docs/ (hoặc đường dẫn file dữ liệu, tính từ gốc repo)
    line: int          # số dòng trong file, đếm từ 1 (0 = cả trang)
    unit: str          # khóa đơn vị (trang.md#id), "" nếu không áp dụng
    rule: str          # mã luật, ví dụ "thuat-ngu", "nam", "thieu-muc"
    found: str         # chữ tìm thấy
    message: str       # việc cần làm / giải thích


def core_pages(root: Path = ROOT) -> list[registry.Page]:
    """Trang Lõi viết tay: phạm vi mặc định của linter."""
    return registry.load(root).select(tier="loi", generated=False)


def unit_at(us: list[units.Unit], line: int) -> str:
    for u in us:
        if u.start <= line <= u.end:
            return u.key
    return us[-1].key if us else ""


def blank(s: str) -> str:
    """Thay mọi ký tự (trừ xuống dòng) bằng dấu cách, giữ nguyên vị trí cột."""
    return re.sub(r"[^\n]", " ", s)


def masked_lines(text: str, *, quotes: bool = True, sources: bool = True, meta: tuple[str, ...] = ()) -> list[str]:
    """Các dòng của trang (đếm từ 1 tại chỉ số 1; chỉ số 0 rỗng) với những vùng không phải văn xuôi của site
    bị thay bằng dấu cách: front matter, khối sinh gen/fig, khối code, đích link, code inline;
    và (tùy chọn) khối trích dẫn `!!! quote`/`> …` (`quotes`) cùng mục `## Nguồn` (`sources`).
    Dòng front matter có khóa trong `meta` (ví dụ "title", "description") được giữ, vì chúng cũng hiện ra."""
    m = FRONT.match(text)
    if m:
        fm = "\n".join(ln if any(ln.startswith(k + ":") for k in meta) else blank(ln)
                       for ln in m.group(0).split("\n"))
        text = fm + text[m.end():]
    text = GEN_BLOCK.sub(lambda g: blank(g.group(0)), text)
    lines = text.split("\n")
    out = [""]
    fence = None
    quote_indent: int | None = None
    in_sources = False
    for line in lines:
        if fence:
            out.append("")
            if line.strip().startswith(fence):
                fence = None
            continue
        f = FENCE_LINE.match(line)
        if f:
            fence = f.group(1)[0] * 3
            out.append("")
            continue
        h = H2.match(line)
        if h:
            in_sources = re.sub(r"\s*\{[^}]*\}\s*$", "", h.group(1)).strip() == "Nguồn"
        if sources and in_sources:
            out.append("")
            continue
        if quote_indent is not None:
            if line.strip() == "" or len(line) - len(line.lstrip()) > quote_indent:
                out.append("")
                continue
            quote_indent = None
        a = ADMONITION.match(line)
        if quotes and a and a.group(2) == "quote":
            quote_indent = len(a.group(1))
            out.append("")
            continue
        if quotes and line.lstrip().startswith(">"):
            out.append("")
            continue
        line = LINK_TARGET.sub(lambda g: blank(g.group(0)), line)
        line = INLINE_CODE.sub(lambda g: blank(g.group(0)), line)
        out.append(line)
    return out


def render(title: str, intro: str, findings: list[Finding], rules: dict[str, str]) -> str:
    by_rule = Counter(f.rule for f in findings)
    pages = {f.page for f in findings}
    L = [f"# {title}", "", intro, "",
         f"**{len(findings)} chỗ** ở **{len(pages)} trang/file**. Chế độ cảnh báo: chưa chặn CI.", "",
         "| Luật | Nghĩa | Số chỗ |", "|---|---|---:|"]
    for rule, desc in rules.items():
        L.append(f"| `{rule}` | {desc} | {by_rule.get(rule, 0)} |")
    if findings:
        L += ["", "## Chi tiết", "", "| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |", "|---|---|---|---|---|"]
        for f in findings:
            where = f"`{f.page}:{f.line}`" if f.line else f"`{f.page}`"
            cell = f.found.replace("|", "\\|")
            L.append(f"| {where} | {('`' + f.unit + '`') if f.unit else '—'} | `{f.rule}` | {cell} | {f.message} |")
    return "\n".join(L) + "\n"


def run(name: str, title: str, intro: str, rules: dict[str, str], collect, argv: list[str], doc: str) -> int:
    ap = argparse.ArgumentParser(description=doc.split("\n")[0])
    ap.add_argument("--write", action="store_true", help=f"ghi báo cáo vào verification/lint/{name}.md")
    ap.add_argument("--strict", action="store_true", help="thoát mã 1 khi có chỗ vi phạm (chế độ chặn)")
    ap.add_argument("-q", "--quiet", action="store_true", help="chỉ in tóm tắt")
    args = ap.parse_args(argv)
    findings = sorted(collect(), key=lambda f: (f.page, f.line, f.rule, f.found))
    if args.write:
        out = ROOT / "verification" / "lint" / f"{name}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(title, intro, findings, rules), encoding="utf-8")
    by_rule = Counter(f.rule for f in findings)
    summary = ", ".join(f"{r} {by_rule[r]}" for r in rules if by_rule[r]) or "không có"
    print(f"{name}: {len(findings)} chỗ ({summary}){' — chế độ cảnh báo' if not args.strict else ''}.")
    if not args.quiet:
        for f in findings:
            print(f"  {f.page}:{f.line}: [{f.rule}] {f.found} — {f.message}")
    return 1 if args.strict and findings else 0


def main_guard(fn) -> None:
    sys.exit(fn(sys.argv[1:]))
