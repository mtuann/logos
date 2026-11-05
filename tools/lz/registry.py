"""Đọc sổ đăng ký nội dung `content.yml` (đặc tả: ban-giao/dot-0.md; kiểm tra: tools/content_registry.py)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from . import ROOT

REGISTRY = "content.yml"


@dataclass(frozen=True)
class Page:
    path: str           # tính từ docs/, ví dụ "cau-hoi/tri-thuc.md"
    type: str
    tier: str
    block: str | None
    generated: bool

    def file(self, root: Path = ROOT) -> Path:
        return root / "docs" / self.path


@dataclass(frozen=True)
class DataFile:
    path: str           # tính từ gốc repo
    kind: str
    tier: str
    block: str | None
    generated: bool


@dataclass(frozen=True)
class Registry:
    pages: tuple[Page, ...]
    data: tuple[DataFile, ...]

    def page(self, path: str) -> Page:
        for p in self.pages:
            if p.path == path:
                return p
        raise KeyError(f"{path}: không có trong {REGISTRY}")

    def select(self, *, tier: str | None = None, type: str | None = None,
               block: str | None = None, generated: bool | None = None) -> list[Page]:
        """Các trang thỏa mọi điều kiện được cho (None = không lọc), theo thứ tự trong sổ."""
        return [
            p for p in self.pages
            if (tier is None or p.tier == tier)
            and (type is None or p.type == type)
            and (block is None or p.block == block)
            and (generated is None or p.generated == generated)
        ]


def load(root: Path = ROOT) -> Registry:
    raw = yaml.safe_load((root / REGISTRY).read_text(encoding="utf-8"))
    return Registry(
        pages=tuple(Page(**e) for e in raw.get("pages") or []),
        data=tuple(DataFile(**e) for e in raw.get("data") or []),
    )
