#!/usr/bin/env python3
"""Sinh "Sách in" (docs/them/sach.md) từ các bài viết của Logos Zero.

Mọi bài đọc trong các mục Bắt đầu, Công cụ tư duy, Câu hỏi lớn, Lịch sử,
Đọc văn bản (trừ các trang index) được gộp thành một cuốn sách in được,
theo đúng thứ tự nav trong mkdocs.yml:

- Trang bìa: tên sách, ngày cập nhật (lấy từ mtime mới nhất của các bài
  nguồn theo múi giờ local; --check chuẩn hóa bỏ dòng ngày vì mtime đổi
  sau mỗi git checkout và khác múi giờ giữa máy dev/CI).
- Mục "Tình trạng rà soát" (tái dùng logic review_check.py, giới hạn trong
  các bài của sách).
- Mục lục theo mục, link về bài gốc trên web.
- Toàn bộ nội dung các bài nối nhau; mỗi bài bắt đầu bằng
  <div class="oz-page-break"></div> để khi in mỗi bài sang trang mới.
- Quiz tương tác (oz-quiz) được giữ nguyên (nội dung câu hỏi/đáp án vẫn
  đọc được khi in; CSS in đã xử lý).
- Các <div class="oz-..."> chứa công cụ tương tác khác được thay bằng dòng
  chú thích "[Công cụ tương tác — trải nghiệm trên web]".
- Link tương đối trong bài được viết lại cho đúng khi nhìn từ docs/them/.

    python3 tools/book.py          # sinh lại
    python3 tools/book.py --check  # báo lỗi nếu file sinh lệch nội dung
"""

from __future__ import annotations

import datetime
import importlib.util
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
THEM = os.path.join(DOCS, "them")
BOOK_PAGE = os.path.join(THEM, "sach.md")
NAV = os.path.join(ROOT, "mkdocs.yml")

SECTIONS = ["Bắt đầu", "Công cụ tư duy", "Câu hỏi lớn", "Lịch sử", "Đọc văn bản"]

COVER_DATE_RE = re.compile(r"Nội dung cập nhật đến ngày \d{2}/\d{2}/\d{4}")
UPDATED_LINE_RE = re.compile(r"^updated: \d{4}-\d{2}-\d{2}$", re.M)
# ID cố định `{#id}` của mục H2 (KE-HOACH.md mục 5.5) chỉ có nghĩa trong trang của nó: trong sách gộp,
# "## Nguồn {#nguon}" của mọi bài sẽ trùng nhau. Bỏ đi để toc tự đánh số như trước (nguon, nguon_1…).
H2_ID_RE = re.compile(r"^(## .*?)[ \t]*\{#[\w-]+\}[ \t]*$", re.M)


def normalize_cover_date(text: str) -> str:
    """Chuẩn hóa dòng ngày bìa để --check không vỡ vì ngày.

    Ngày bìa lấy từ mtime mới nhất của các bài nguồn. Git không giữ mtime
    (sau checkout, mtime = giờ checkout) và múi giờ máy dev khác CI, nên
    cùng một nội dung có thể sinh ra hai ngày khác nhau (ví dụ push lúc
    20:23 CDT ngày 13 nhưng CI checkout lúc 01:25 UTC ngày 14). Chuẩn hóa
    để --check chỉ bắt lệch nội dung thật, không bắt lệch ngày sinh.
    """
    return COVER_DATE_RE.sub("Nội dung cập nhật đến ngày <ngày>", text)


def normalize_generated(text: str) -> str:
    """Chuẩn hóa mọi dấu vết "ngày sinh" trước khi so sánh trong --check."""
    text = normalize_cover_date(text)
    return UPDATED_LINE_RE.sub("updated: <ngày>", text)


TOOL_NOTE = "> *[Công cụ tương tác — trải nghiệm trên web]*"

# Các div oz-* được giữ nguyên khi in (nội dung tĩnh, đọc được trên giấy).
PRINTABLE_DIVS = {"oz-quiz", "oz-timeline", "oz-influence", "oz-fig"}


# ----------------------------------------------------------------------------
# Đọc nav trong mkdocs.yml (parser tối giản theo thụt đầu dòng)
# ----------------------------------------------------------------------------
def parse_nav(path: str) -> list[tuple[str, list[tuple[str | None, str, str]]]]:
    """Trả về [(tên mục, [(tên nhóm con|None, tiêu đề, đường dẫn tương đối)])]."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    # Tìm dòng "nav:" ở cấp cao nhất (không nhầm với nav: trong validation).
    i = 0
    while i < len(lines) and lines[i] != "nav:":
        i += 1
    i += 1
    sections: list[tuple[str, list[tuple[str | None, str, str]]]] = []
    cur: tuple[str, list[tuple[str | None, str, str]]] | None = None
    field: str | None = None
    for line in lines[i:]:
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent < 2:
            break  # hết khối nav
        stripped = line.strip()
        if indent == 2 and stripped.startswith("- "):
            name = stripped[2:].strip().rstrip(":").strip('"')
            if name in SECTIONS:
                cur = (name, [])
                sections.append(cur)
                field = None
            else:
                cur = None
        elif cur is not None and indent == 6 and stripped.startswith("- "):
            item = stripped[2:].strip()
            if item.endswith(":") and not item.endswith(".md"):
                field = item[:-1].strip().strip('"')
            else:
                title, _, rel = item.rpartition(":")
                title, rel = title.strip().strip('"'), rel.strip()
                if rel.endswith(".md") and not rel.endswith("/index.md"):
                    cur[1].append((field, title, rel))
        elif cur is not None and indent == 10 and stripped.startswith("- ") and field:
            item = stripped[2:].strip()
            title, _, rel = item.rpartition(":")
            title, rel = title.strip().strip('"'), rel.strip()
            if rel.endswith(".md"):
                cur[1].append((field, title, rel))
    return sections


# ----------------------------------------------------------------------------
# Front matter tối giản
# ----------------------------------------------------------------------------
def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta: dict = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        meta[k.strip()] = v
    body = text[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    return meta, body


# ----------------------------------------------------------------------------
# Viết lại link tương đối cho đúng khi nhìn từ docs/them/
# ----------------------------------------------------------------------------
ABS_URL = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|#|mailto:|tel:)")


def _resolve(url: str, article_dir: str) -> str:
    if not url or ABS_URL.match(url):
        return url
    target = os.path.normpath(os.path.join(article_dir, url))
    return os.path.relpath(target, THEM).replace(os.sep, "/")


MD_LINK = re.compile(r"(\]\()([^)\s]+)(\))")
REF_DEF = re.compile(r"^(\[[^\]]+\]:\s*)(\S+)(\s*)$")
HTML_ATTR = re.compile(r'\b(?:src|href)="([^"]+)"')


def rewrite_links(body: str, relpath: str) -> str:
    article_dir = os.path.join(DOCS, os.path.dirname(relpath))
    body = MD_LINK.sub(
        lambda m: m.group(1) + _resolve(m.group(2), article_dir) + m.group(3), body
    )
    lines = []
    for line in body.splitlines():
        m = REF_DEF.match(line)
        if m:
            lines.append(m.group(1) + _resolve(m.group(2), article_dir) + m.group(3))
        else:
            lines.append(line)
    body = "\n".join(lines)
    body = HTML_ATTR.sub(
        lambda m: m.group(0)[: m.group(0).index('"') + 1]
        + _resolve(m.group(1), article_dir)
        + '"',
        body,
    )
    return body


# ----------------------------------------------------------------------------
# Thay các div công cụ tương tác (trừ quiz/hình tĩnh) bằng dòng chú thích
# ----------------------------------------------------------------------------
DIV_OPEN = re.compile(r'<div\b[^>]*\bclass="oz-([a-z0-9-]+)"[^>]*>', re.I)


def strip_tool_divs(body: str) -> str:
    out = []
    pos = 0
    for m in DIV_OPEN.finditer(body):
        cls = "oz-" + m.group(1).lower()
        if cls in PRINTABLE_DIVS:
            continue
        # Tìm </div> đóng tương ứng (đếm lồng nhau).
        depth = 1
        i = m.end()
        tag = re.compile(r"</?div\b[^>]*>", re.I)
        end = None
        for t in tag.finditer(body, i):
            if t.group(0).startswith("</"):
                depth -= 1
            else:
                depth += 1
            if depth == 0:
                end = t.end()
                break
        if end is None:
            continue  # div không đóng: để nguyên, không đoán mò
        out.append(body[pos : m.start()])
        out.append("\n\n" + TOOL_NOTE + "\n\n")
        pos = end
    out.append(body[pos:])
    return "".join(out)


# ----------------------------------------------------------------------------
# Mục "Tình trạng rà soát" (tái dùng review_check.py, giới hạn trong sách)
# ----------------------------------------------------------------------------
def load_review_check():
    spec = importlib.util.spec_from_file_location(
        "review_check", os.path.join(ROOT, "tools", "review_check.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def render_review_section(articles: list[dict], today: date | None = None) -> str:
    rc = load_review_check()
    fresh_all, stale_all = rc.collect(today or date.today())
    rels = {a["rel"] for a in articles}
    fresh = [x for x in fresh_all if x[2] in rels]
    stale = [x for x in stale_all if x[2] in rels]
    lines = ["## Tình trạng rà soát", ""]
    lines.append(
        f"{len(fresh)} bài trong sách đã được rà soát trong "
        f"{rc.STALE_MONTHS} tháng qua (tính từ ngày build)."
    )
    lines.append("")
    if not stale:
        lines.append("Không có bài nào quá hạn rà soát.")
    else:
        lines.append(
            f"**{len(stale)} bài cần rà soát lại** "
            f"(quá {rc.STALE_MONTHS} tháng chưa cập nhật):"
        )
        lines.append("")
        for title, updated, rel in stale:
            when = updated.strftime("%d/%m/%Y") if updated else "không rõ ngày"
            lines.append(f"- [{title}](../{rel}) — cập nhật lần cuối: {when}")
    lines.append("")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------
def load_articles(
    sections: list[tuple[str, list[tuple[str | None, str, str]]]],
) -> list[dict]:
    articles = []
    for sec_name, items in sections:
        for field, nav_title, rel in items:
            path = os.path.join(DOCS, rel)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            meta, body = parse_front_matter(text)
            title = meta.get("title") or nav_title
            body = H2_ID_RE.sub(r"\1", body)
            body = rewrite_links(body, rel)
            body = strip_tool_divs(body)
            articles.append(
                {
                    "section": sec_name,
                    "field": field,
                    "title": title,
                    "rel": rel,
                    "web_rel": os.path.relpath(
                        os.path.join(DOCS, rel), THEM
                    ).replace(os.sep, "/"),
                    "body": body,
                    "mtime": os.path.getmtime(path),
                }
            )
    return articles


def render_book(
    articles: list[dict], updated: str, review_section: str, today: str
) -> str:
    out = []
    out.append("---")
    out.append("title: Logos Zero — Sách in")
    out.append(
        "description: Toàn bộ bài viết của Logos Zero gộp thành một cuốn sách in được."
    )
    out.append(f"updated: {today}")
    out.append("search:")
    out.append("  exclude: true")
    out.append("---")
    out.append("")
    out.append("# Logos Zero — Sách in")
    out.append("")
    out.append(
        "*Bản tổng hợp các bài viết của Logos Zero để in ra đọc. "
        f"Nội dung cập nhật đến ngày {updated}.*"
    )
    out.append("")
    out.append('!!! note "Lưu ý khi in"')
    out.append("    Mỗi bài bắt đầu ở một trang mới.")
    out.append(
        "    Các công cụ tương tác được thay bằng dòng chú thích — "
        "hãy trải nghiệm chúng trên web."
    )
    out.append("")
    out.append(review_section.rstrip())
    out.append("")
    out.append("## Mục lục")
    out.append("")
    last_sec = last_field = None
    for a in articles:
        if a["section"] != last_sec:
            out.append(f"### {a['section']}")
            out.append("")
            last_sec = a["section"]
            last_field = None
        if a["field"] != last_field:
            out.append(f"#### {a['field']}")
            out.append("")
            last_field = a["field"]
        out.append(f"- [{a['title']}]({a['web_rel']})")
    out.append("")
    for a in articles:
        out.append('<div class="oz-page-break"></div>')
        out.append("")
        out.append(a["body"].rstrip())
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def build() -> tuple[str, int]:
    """Sinh nội dung sách; trả về (nội dung, số bài)."""
    sections = parse_nav(NAV)
    articles = load_articles(sections)
    if not articles:
        raise RuntimeError("không quét được bài nào từ nav")
    updated = datetime.datetime.fromtimestamp(
        max(a["mtime"] for a in articles)
    ).strftime("%d/%m/%Y")
    today = date.today().strftime("%Y-%m-%d")
    review_section = render_review_section(articles)
    return render_book(articles, updated, review_section, today), len(articles)


def main() -> int:
    check = "--check" in sys.argv
    try:
        book, n = build()
    except RuntimeError as e:
        print(f"LỖI: {e}", file=sys.stderr)
        return 1
    errs = []
    if check:
        if not os.path.exists(BOOK_PAGE):
            errs.append(f"Sách in: thiếu file {os.path.relpath(BOOK_PAGE, ROOT)}")
        else:
            with open(BOOK_PAGE, encoding="utf-8") as f:
                have = f.read()
            # Bỏ qua các dòng ngày sinh: mtime đổi sau mỗi checkout và khác
            # múi giờ giữa các máy, nên ngày sinh có thể lệch dù nội dung khớp.
            if normalize_generated(have) != normalize_generated(book):
                errs.append("Sách in lệch với bài nguồn: chạy 'python3 tools/book.py'")
    else:
        with open(BOOK_PAGE, "w", encoding="utf-8") as f:
            f.write(book)
    for e in errs:
        print("LỖI:", e, file=sys.stderr)
    if not errs and not check:
        print(f"Sách in: {n} bài -> {os.path.relpath(BOOK_PAGE, ROOT)}")
    if not errs and check:
        print(f"Sách in: {n} bài, nội dung khớp.")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
