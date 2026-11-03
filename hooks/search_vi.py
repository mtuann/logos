"""Tìm kiếm tiếng Việt không dấu.

Sau khi plugin search của Material ghi search/search_index.json, hook này thêm bản
không dấu (bỏ dấu, đổi đ → d) của tiêu đề và nội dung vào trường text của mỗi mục.
Tiêu đề không dấu được lặp lại để giữ thứ hạng khi người dùng gõ không dấu.
Tiêu đề hiển thị giữ nguyên.

Bản không dấu của tiêu đề cũng được thêm (trong thẻ ẩn) vào chính trường title, vì
trường này được nhân trọng số rất lớn: nếu chỉ có ở text, tiêu đề "tâm trí" không bao giờ
khớp khi gõ "tam tri", trong khi một tiêu đề có sẵn chữ "tri" (như "bức màn vô tri") lại
khớp và vượt lên (22/10/2026: "tam tri" rớt khỏi top-5 khi thêm trang Rawls, Chu Hy).
"""

from __future__ import annotations

import json
import logging
import re
import unicodedata
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.search_vi")

TAG_RE = re.compile(r"<[^>]+>")
TITLE_REPEAT = 3

# Box "Tóm tắt 5 phút" chỉ diễn đạt lại nội dung thân bài. Nếu index cả box,
# các từ trong tóm tắt bị đếm trùng (double-counting) làm méo xếp hạng BM25
# (14/10/2026: "tam tri" rớt khỏi top-5 vì "tri thức" lặp lại trong tóm tắt).
SUMMARY_RE = re.compile(r"<p>Tóm tắt 5 phút</p>\s*<ul>.*?</ul>", re.S)


def strip_summaries(doc: dict) -> dict:
    """Loại box tóm tắt khỏi chỉ mục tìm kiếm (nội dung đã có trong thân bài)."""
    text = doc.get("text", "") or ""
    if "Tóm tắt 5 phút" in text:
        doc = dict(doc)
        doc["text"] = SUMMARY_RE.sub(" ", text)
    return doc


def strip_accents(text: str) -> str:
    """Bỏ dấu tiếng Việt: 'Đạo đức học' -> 'Dao duc hoc'."""
    text = text.replace("đ", "d").replace("Đ", "D")
    decomposed = unicodedata.normalize("NFD", text)
    return unicodedata.normalize("NFC", "".join(c for c in decomposed if not unicodedata.combining(c)))


def augment(doc: dict) -> dict:
    title = doc.get("title", "") or ""
    text = doc.get("text", "") or ""
    plain_title = strip_accents(TAG_RE.sub(" ", title))
    plain_text = strip_accents(TAG_RE.sub(" ", text))
    extra = []
    if plain_title != title:
        extra.append(" ".join([plain_title] * TITLE_REPEAT))
    if plain_text != TAG_RE.sub(" ", text):
        extra.append(plain_text)
    if extra:
        # Bọc trong thẻ ẩn để đoạn trích kết quả không hiện phần lặp không dấu.
        doc = dict(doc)
        doc["text"] = text + '<span hidden class="oz-noaccent"> ' + " ".join(extra) + "</span>"
    if plain_title != title:
        doc = dict(doc)
        doc["title"] = title + '<span hidden class="oz-noaccent"> ' + plain_title + "</span>"
    return doc


def on_post_build(config, **kwargs):
    path = Path(config["site_dir"]) / "search" / "search_index.json"
    if not path.exists():
        log.warning("Không thấy search_index.json — bỏ qua tìm kiếm không dấu")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    data["docs"] = [augment(strip_summaries(d)) for d in data.get("docs", [])]
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    log.info("search_vi: đã thêm bản không dấu cho %d mục", len(data["docs"]))
