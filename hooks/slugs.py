"""Anchor tiếng Việt dễ đọc: 'Đọc văn bản gốc' -> 'doc-van-ban-goc'.

Mặc định Python-Markdown bỏ hẳn các ký tự như 'đ' khi tạo anchor ('Đọc' -> 'oc').
Hook này thay hàm slugify của phần mở rộng toc bằng hàm bỏ dấu tiếng Việt.
"""

from __future__ import annotations

import re
import unicodedata


def slugify(value: str, separator: str = "-") -> str:
    value = value.replace("đ", "d").replace("Đ", "D")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    value = re.sub(r"[^\w\s-]", "", value).strip()
    return re.sub(r"[%s\s]+" % re.escape(separator), separator, value)


def on_config(config, **kwargs):
    toc = config.mdx_configs.setdefault("toc", {})
    toc["slugify"] = slugify
    return config
