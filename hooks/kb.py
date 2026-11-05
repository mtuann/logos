"""Shortcode dữ kiện: in số đếm, số liệu, dữ kiện từ dữ liệu lúc build (KE-HOACH.md mục 4, quyết định 3).

Cú pháp (chốt ở đợt 1, việc 1.8): `[[loại:khóa]]`, viết liền, chữ thường, không dấu cách.

    [[count:cau-hoi]]            số trang loại cau-hoi trong content.yml          → 57
    [[count:cau-hoi/dao-duc]]    số trang loại cau-hoi thuộc khối dao-duc          → 7
    [[count:lich-su]]            số bài lịch sử (không tính Dòng thời gian, Sơ đồ) → 8
    [[count:triet-gia]]          số trang triết gia (không tính index.md)          → 59

Loại `count` đọc content.yml: đếm trang có `type` cho trước, lọc thêm theo `block` nếu có `/khối`. Không đếm
trang he-thong và trang sinh tự động (lich-su/dong-thoi-gian.md…), trừ trang triết gia: mỗi trang là một hồ sơ. Số từ 1.000 trở lên in kiểu Việt Nam (1.234).
Các loại khác (số liệu PhilPapers, dữ kiện trong kho) được thêm ở đợt 2–3 bằng cách đăng ký vào HANDLERS.

Shortcode trong khối code (```…```) và code inline (`…`) được giữ nguyên, để tài liệu có thể viết ra cú pháp.
Loại hoặc khóa không tồn tại thì build dừng (PluginError), kèm tên trang: không bao giờ in ra số sai hay chỗ trống.
Mã băm đơn vị (tools/lz/normalize.py) giữ shortcode nguyên dạng, nên số đếm đổi không mở khóa đơn vị Lõi.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

import yaml

try:
    from properdocs.exceptions import PluginError
except ImportError:  # chạy dưới mkdocs 1.6.1 (lối lùi ở KE-HOACH.md mục 11)
    from mkdocs.exceptions import PluginError

SHORTCODE = re.compile(r"\[\[([a-z][a-z-]*):([a-z0-9][a-z0-9/._-]*)\]\]")
FENCE = re.compile(r"^([ \t]*)(`{3,}|~{3,})[^\n]*\n.*?^\1\2[ \t]*$", re.S | re.M)
CODE_SPAN = re.compile(r"(`+)(?!`).+?(?<!`)\1(?!`)", re.S)

_registry: dict | None = None


def load_registry(root: Path) -> dict:
    return yaml.safe_load((root / "content.yml").read_text(encoding="utf-8"))


def fmt_int(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def count(key: str, registry: dict) -> str:
    kind, _, block = key.partition("/")
    # Đếm "bài": bỏ trang he-thong và trang sinh tự động (Dòng thời gian, Sơ đồ ảnh hưởng…), trừ trang triết gia,
    # vì mỗi trang triết gia sinh ra là một hồ sơ.
    pages = [p for p in registry["pages"]
             if p["type"] != "he-thong" and (not p["generated"] or p["type"] == "triet-gia")]
    types = {p["type"] for p in pages}
    if kind not in types:
        raise KeyError(f"loại trang {kind!r} không có trong content.yml (có: {', '.join(sorted(types))})")
    hits = [p for p in pages if p["type"] == kind]
    if block:
        blocks = {p["block"] for p in hits}
        if block not in blocks:
            raise KeyError(f"khối {block!r} không có trang loại {kind} (có: {', '.join(sorted(b for b in blocks if b))})")
        hits = [p for p in hits if p["block"] == block]
    return fmt_int(len(hits))


HANDLERS: dict[str, Callable[[str, dict], str]] = {"count": count}


def expand(markdown: str, registry: dict, where: str = "") -> str:
    """Thay mọi shortcode ngoài code; KeyError/PluginError khi loại hay khóa không tồn tại."""
    def sub(m: re.Match) -> str:
        kind, key = m.group(1), m.group(2)
        handler = HANDLERS.get(kind)
        if handler is None:
            raise PluginError(f"{where}: shortcode [[{kind}:{key}]]: loại {kind!r} chưa có "
                              f"(có: {', '.join(sorted(HANDLERS))})")
        try:
            return handler(key, registry)
        except KeyError as exc:
            raise PluginError(f"{where}: shortcode [[{kind}:{key}]]: {exc.args[0]}") from None

    pos = 0
    protected = sorted([m.span() for m in FENCE.finditer(markdown)])
    # code inline chỉ tính ngoài khối code rào
    spans = []
    for a, b in protected + [(len(markdown), len(markdown))]:
        chunk = markdown[pos:a]
        cpos = 0
        for m in CODE_SPAN.finditer(chunk):
            spans.append(SHORTCODE.sub(sub, chunk[cpos:m.start()]))
            spans.append(m.group(0))
            cpos = m.end()
        spans.append(SHORTCODE.sub(sub, chunk[cpos:]))
        spans.append(markdown[a:b])
        pos = b
    return "".join(spans)


def on_config(config, **kwargs):
    global _registry
    _registry = load_registry(Path(config["config_file_path"]).resolve().parent)
    return config


def on_page_markdown(markdown, page, config, files, **kwargs):
    if "[[" not in markdown:
        return markdown
    return expand(markdown, _registry, page.file.src_uri)
