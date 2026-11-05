"""Chuẩn hóa văn bản nguồn của một đơn vị thành một chuỗi (KE-HOACH.md mục 5.6, bước 2–4).

Làm việc trực tiếp trên nguồn Markdown, không qua thư viện render: mã băm không phụ thuộc phiên bản
Python-Markdown, pymdown-extensions hay theme, nên đổi nền tảng không mở khóa Lõi.

Bỏ:   front matter; khối `<!-- gen:… -->…<!-- /gen:… -->` và `<!-- fig:… -->…<!-- /fig:… -->`;
      comment HTML; thuộc tính `{#…}`, `{: …}`, `{.lớp}`; dấu nhấn (`*`, `_`, `**`, `__`, `==`, `^^`, `~~`);
      ký hiệu đầu dòng (`#`, `-`, `*`, `+`, `1.`, `>`, `:`); tên loại admonition; dòng kẻ ngang;
      dòng ngăn của bảng; dấu rào code và dấu backtick; thẻ HTML định dạng (`<p>`, `<small>`, `<em>`…).
Giữ:  chữ hiển thị (cả tiêu đề admonition và tiêu đề tab trong ngoặc kép); nội dung code nguyên văn;
      đích link ở dạng `⟨đích⟩` ngay sau chữ của link (cả link `<https://…>`); shortcode `[[…]]` nguyên dạng;
      ô bảng, ngăn bằng ` | `; widget `<div class="oz-…" data-…>` thành `⟨oz-… data-…=…⟩`.
Quiz: `<div class="oz-quiz" …>` + JSON được parse rồi in lại có sắp xếp khóa.
Cuối: thay thực thể HTML (`&amp;` → `&`), Unicode NFC, mọi chuỗi khoảng trắng thành một dấu cách, cắt hai đầu.
"""

from __future__ import annotations

import html
import json
import re
import unicodedata

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
GEN_OPEN = re.compile(r"<!-- (gen|fig):(\S+) -->")
GEN_CLOSE = re.compile(r"<!-- /(gen|fig):(\S+) -->")
GEN_BLOCK = re.compile(r"<!-- (gen|fig):(\S+) -->.*?<!-- /\1:\2 -->", re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)
FENCE = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")

ADMONITION = re.compile(r'^(?:!!!|\?\?\?\+?)[ \t]+[\w-]+(?:[ \t]+[\w-]+)*(?:[ \t]+"(?P<title>.*)")?[ \t]*$')
TAB = re.compile(r'^===\+?[ \t]+"(?P<title>.*)"[ \t]*$')
HEADING = re.compile(r"^#{1,6}[ \t]+(.*?)[ \t]*#*[ \t]*$")
RULE = re.compile(r"^(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")
TABLE_SEP = re.compile(r"^\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?$")
LIST = re.compile(r"^(?:[-*+]|\d+[.)])[ \t]+")
QUOTE = re.compile(r"^>[ \t]?")
DEFINITION = re.compile(r"^:[ \t]+")

ATTR = re.compile(r"[ \t]*\{:?[ \t]*[#.:][^{}\n]*\}|[ \t]*\{:[^{}\n]*\}")
# Ký tự thoát được của Python-Markdown (ESCAPED_CHARS) cộng `|` của phần mở rộng tables.
ESCAPE = re.compile(r"\\([\\`*_{}\[\]()>#+\-.!|])")
CODE_SPAN = re.compile(r"(`+)(.+?)\1", re.S)
AUTOLINK = re.compile(r"<((?:https?|mailto|ftp):[^>\s]+)>")
# [chữ](đích "tiêu đề") — chữ được lồng một cấp ngoặc vuông, đích được lồng một cấp ngoặc tròn.
LINK = re.compile(
    r"(?P<img>!?)\[(?P<text>(?:[^\[\]]|\[[^\[\]]*\])*)\]"
    r"\((?P<target><[^>]*>|(?:[^()\s]|\([^()\s]*\))*)(?:[ \t]+(?:\"[^\"]*\"|'[^']*'))?[ \t]*\)"
)
SHORTCODE = re.compile(r"\[\[[^\[\]]+\]\]")
TAG = re.compile(r"</?([a-zA-Z][a-zA-Z0-9-]*)((?:\s+[^\s=>/]+(?:=(?:\"[^\"]*\"|'[^']*'|[^\s>]+))?)*)\s*/?>")
TAG_ATTR = re.compile(r"([^\s=>/]+)(?:=(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+)))?")
QUIZ = re.compile(
    r"<div\b(?P<attrs>[^>]*\bclass=\"oz-quiz\"[^>]*)>\s*<script type=\"application/json\">(?P<json>.*?)</script>\s*</div>",
    re.S,
)
EMPHASIS = re.compile(r"\*+|==|\^\^|~~|(?<![^\W_])_+|_+(?![^\W_])")
SPACE = re.compile(r"\s+")

PH = "\x00{}\x00"
PH_RE = re.compile(r"\x00(\d+)\x00")


class _Protect:
    """Giữ chỗ cho các đoạn không được đụng tới (code, đích link, shortcode, ký tự thoát)."""

    def __init__(self) -> None:
        self.items: list[str] = []

    def __call__(self, s: str) -> str:
        self.items.append(s)
        return PH.format(len(self.items) - 1)

    def restore(self, s: str) -> str:
        while PH_RE.search(s):
            s = PH_RE.sub(lambda m: self.items[int(m.group(1))], s)
        return s


def _attrs(raw: str) -> dict[str, str]:
    out = {}
    for m in TAG_ATTR.finditer(raw):
        out[m.group(1)] = next((g for g in m.groups()[1:] if g is not None), "")
    return out


def _widget(attrs: dict[str, str]) -> str | None:
    """`<div class="oz-logic" data-count="10">` → `⟨oz-logic data-count=10⟩`; thẻ khác → None."""
    cls = attrs.get("class", "")
    if not cls.startswith("oz-"):
        return None
    data = " ".join(f"{k}={v}" for k, v in sorted(attrs.items()) if k.startswith("data-"))
    return f"⟨{cls}{' ' + data if data else ''}⟩"


def _quiz(m: re.Match, protect: _Protect) -> str:
    head = _widget(_attrs(m.group("attrs"))) or "⟨oz-quiz⟩"
    try:
        body = json.dumps(json.loads(m.group("json")), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except json.JSONDecodeError:
        body = m.group("json")          # JSON hỏng: giữ nguyên văn (kiểm thử quiz ở chỗ khác sẽ báo)
    return f"\n{head} {protect(body)}\n"


def _inline(s: str, protect: _Protect, targets: bool = True) -> str:
    s = ESCAPE.sub(lambda m: protect(m.group(1)), s)
    s = CODE_SPAN.sub(lambda m: protect(m.group(2).strip()), s)
    s = SHORTCODE.sub(lambda m: protect(m.group(0)), s)
    s = AUTOLINK.sub(lambda m: protect(m.group(1) + (f"⟨{m.group(1)}⟩" if targets else "")), s)

    def link(m: re.Match) -> str:
        target = m.group("target").strip("<>")
        return m.group("text") + (protect(f"⟨{target}⟩") if targets else "")

    prev = None
    while prev != s:                   # link lồng trong chữ của link (hiếm) được xử lý từ trong ra
        prev, s = s, LINK.sub(link, s)

    def tag(m: re.Match) -> str:
        if m.group(0).startswith("</"):
            return ""
        w = _widget(_attrs(m.group(2))) if m.group(1).lower() == "div" else None
        return f" {protect(w)} " if w else ("\n" if m.group(1).lower() in {"br", "p", "div"} else "")

    s = TAG.sub(tag, s)
    s = ATTR.sub("", s)
    s = EMPHASIS.sub("", s)
    return s


def heading_text(s: str) -> str:
    """Chữ hiển thị của một tiêu đề (không kèm đích link), dùng để tính slug dự phòng."""
    p = _Protect()
    return SPACE.sub(" ", html.unescape(p.restore(_inline(s, p, targets=False)))).strip()


def strip_generated(text: str) -> str:
    """Bỏ front matter, khối sinh gen/fig và comment HTML."""
    text = FRONT_MATTER.sub("", text, count=1)
    text = GEN_BLOCK.sub("", text)
    return COMMENT.sub("", text)


def normalize(text: str) -> str:
    """Văn bản nguồn của một đơn vị (hoặc cả trang) → chuỗi chuẩn hóa."""
    protect = _Protect()
    text = strip_generated(text.replace("\r\n", "\n"))
    text = QUIZ.sub(lambda m: _quiz(m, protect), text)

    out: list[str] = []
    fence: str | None = None
    for raw in text.split("\n"):
        if fence:
            if raw.strip().startswith(fence) and not raw.strip().strip(fence[0]):
                fence = None
            else:
                out.append(protect(raw))
            continue
        m = FENCE.match(raw)
        if m:
            fence = m.group(2)
            continue

        line = raw.strip()
        while True:                      # ký hiệu khối có thể chồng nhau: "> 1. **x**", "- > …"
            if (m := QUOTE.match(line)) or (m := LIST.match(line)) or (m := DEFINITION.match(line)):
                line = line[m.end():].lstrip()
                continue
            break
        if RULE.match(line) or (TABLE_SEP.match(line) and "|" in line):
            continue
        if m := ADMONITION.match(line):
            line = m.group("title") or ""
        elif m := TAB.match(line):
            line = m.group("title")
        elif m := HEADING.match(line):
            line = m.group(1)

        if line.startswith("|"):
            line = line[1:]
            if line.rstrip().endswith("|") and not line.rstrip().endswith("\\|"):
                line = line.rstrip()[:-1]
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)]
            line = " | ".join(cells)
        out.append(line)

    # Phần inline xử lý trên cả văn bản, vì chữ của một link hay một đoạn nhấn có thể ngắt sang dòng sau.
    s = protect.restore(_inline("\n".join(out), protect))
    s = html.unescape(s)
    s = unicodedata.normalize("NFC", s)
    return SPACE.sub(" ", s).strip()
