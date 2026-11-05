"""Thư viện dùng chung cho các công cụ kiểm chứng của Logos (KE-HOACH.md mục 4, 5.5, 5.6).

    registry   đọc content.yml (sổ đăng ký nội dung)
    units      tách một trang thành đơn vị theo mục H2; khóa `đường-dẫn#id`, phần trước H2 đầu tiên là `#_dau`
    normalize  chuẩn hóa văn bản nguồn của một đơn vị (mục 5.6, bước 2–4)
    hashing    mã băm `sha256:<hex>` của văn bản đã chuẩn hóa (mục 5.6, bước 5)

Chỉ dùng thư viện chuẩn và PyYAML (đã ghim). Các tool trong tools/ nhập bằng `import lz` hoặc `from lz import …`.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DOCS = ROOT / "docs"
