"""Mã băm của đơn vị và bản ghi (KE-HOACH.md mục 5.6, bước 4–5).

Kiểu ngoặc không vào mã băm (quyết định 26): `“ ”` được coi như `"`, `‘ ’` như `'`, nên chọn kiểu ngoặc hiển thị
về sau không mở khóa đơn vị nào. Việc gộp chỉ làm khi băm; `normalize()` vẫn giữ nguyên ngoặc."""

from __future__ import annotations

import hashlib
import json
import unicodedata

from .normalize import normalize

PREFIX = "sha256:"

QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})


def fold_quotes(s: str) -> str:
    """Gộp ngoặc cong về ngoặc thẳng (quyết định 26)."""
    return s.translate(QUOTES)


def _fold(value: object) -> object:
    if isinstance(value, str):
        return fold_quotes(value)
    if isinstance(value, list):
        return [_fold(v) for v in value]
    if isinstance(value, dict):
        return {fold_quotes(k) if isinstance(k, str) else k: _fold(v) for k, v in value.items()}
    return value


def digest(normalized: str) -> str:
    """`sha256:<hex>` của một chuỗi đã chuẩn hóa (UTF-8)."""
    return PREFIX + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def unit_hash(source: str) -> str:
    """Mã băm của văn bản nguồn một đơn vị trang: chuẩn hóa (5.6 bước 2–4) rồi băm."""
    return digest(fold_quotes(normalize(source)))


def record_hash(record: object, ignore: tuple[str, ...] = ("verified",)) -> str:
    """Mã băm của một bản ghi dữ liệu (JSON/YAML đã parse): in lại có sắp xếp khóa, bỏ các trường `ignore`
    ở cấp ngoài cùng (mặc định `verified`, để ghi nhận kiểm chứng không làm đổi mã băm). Ngoặc trong mọi chuỗi
    được gộp trước khi in, để `“` và `"` (in ra thành `\\"`) cho cùng mã băm."""
    if isinstance(record, dict):
        record = {k: v for k, v in record.items() if k not in ignore}
    text = json.dumps(_fold(record), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return digest(unicodedata.normalize("NFC", text))
