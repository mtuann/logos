"""Ngoặc kép hiển thị (đợt 6.2, quyết định 26 và 39): đổi ngoặc thẳng "…" thành ngoặc cong “…” trong chữ của bài
lúc build (thân bài ở on_page_content, cho cả chỉ mục tìm kiếm; menu và mục lục ở on_post_page). Nguồn Markdown không đổi; mã băm của sổ kiểm chứng vốn bỏ qua kiểu ngoặc, nên không đơn vị nào bị mở khóa.

Chỉ đổi trong nút chữ của HTML (giữa các thẻ), không đổi trong thuộc tính, và bỏ qua toàn bộ nội dung của
<code>, <pre>, <script>, <style>, <kbd>, <svg>, <textarea>. Mở hay đóng xét theo ký tự đứng trước (kể cả ký tự cuối của
nút chữ trước đó): đầu đoạn, khoảng trắng, hoặc dấu mở ( [ { — – / thì là ngoặc mở “, còn lại là ngoặc đóng ”.
Thực thể &quot; trong nút chữ cũng được đổi.
"""

from __future__ import annotations

import re

SKIP = ("code", "pre", "script", "style", "kbd", "svg", "textarea")
TAG = re.compile(r"(<!--.*?-->|<[^>]+>)", re.S)
TAGNAME = re.compile(r"</?\s*([a-zA-Z0-9]+)")
OPENERS = set(" \t\n\r ([{—–/“‘")
BLOCK = {"p", "li", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "div", "blockquote", "figcaption", "dt", "dd",
         "summary", "br", "tr", "table", "ul", "ol", "section", "details", "figure", "article", "aside", "header", "footer"}


def curl(html: str) -> str:
    out: list[str] = []
    depth = 0          # đang ở trong thẻ bỏ qua (lồng được)
    prev = "\n"        # ký tự chữ đứng trước
    for part in TAG.split(html):
        if not part:
            continue
        if part.startswith("<"):
            m = TAGNAME.match(part)
            name = m.group(1).lower() if m else ""
            closing = part.startswith("</")
            selfclose = part.endswith("/>")
            if name in SKIP and not selfclose:
                depth = max(0, depth - 1) if closing else depth + 1
                prev = "x"
            elif name in BLOCK:
                prev = "\n"
            out.append(part)
            continue
        if depth:
            out.append(part)
            if part.strip():
                prev = part[-1]
            continue
        text = part.replace("&quot;", '"')
        buf = []
        for ch in text:
            if ch == '"':
                ch = "“" if prev in OPENERS else "”"
            buf.append(ch)
            prev = ch
        out.append("".join(buf))
    return "".join(out)


def on_page_content(html, page, config, files, **kwargs):
    return curl(html)


def on_post_page(output, page, config, **kwargs):
    """Cả trang (menu, mục lục, tiêu đề tab): chỉ đổi phần <body>; <head> giữ nguyên (meta, JSON-LD)."""
    i = output.find("<body")
    j = output.find(">", i) + 1 if i >= 0 else 0
    return output[:j] + curl(output[j:]) if j else output
