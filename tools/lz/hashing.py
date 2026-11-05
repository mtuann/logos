"""Mã băm của đơn vị và bản ghi (KE-HOACH.md mục 5.6, bước 5)."""

from __future__ import annotations

import hashlib
import json
import unicodedata

from .normalize import normalize

PREFIX = "sha256:"


def digest(normalized: str) -> str:
    """`sha256:<hex>` của một chuỗi đã chuẩn hóa (UTF-8)."""
    return PREFIX + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def unit_hash(source: str) -> str:
    """Mã băm của văn bản nguồn một đơn vị trang: chuẩn hóa (5.6 bước 2–4) rồi băm."""
    return digest(normalize(source))


def record_hash(record: object, ignore: tuple[str, ...] = ("verified",)) -> str:
    """Mã băm của một bản ghi dữ liệu (JSON/YAML đã parse): in lại có sắp xếp khóa, bỏ các trường `ignore`
    ở cấp ngoài cùng (mặc định `verified`, để ghi nhận kiểm chứng không làm đổi mã băm)."""
    if isinstance(record, dict):
        record = {k: v for k, v in record.items() if k not in ignore}
    text = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return digest(unicodedata.normalize("NFC", text))
