"""Đổi tên site "Logos Zero" thành "Logos" (đợt 5, việc 5.0d; quyết định 27).

    python tools/migrate/dot5_ten.py --dry-run   # in bảng chỗ đổi và chỗ giữ, không ghi
    python tools/migrate/dot5_ten.py             # ghi

Đổi mọi chữ "Logos Zero" trong nguồn viết tay của site: trang `docs/**/*.md` không sinh tự động, hồ sơ
`data/people/*.yml`, dữ liệu `docs/assets/data/*.json`, JS, CSS, service worker, manifest, biểu tượng, `mkdocs.yml`,
mẫu báo lỗi, hướng dẫn viết, và các generator/kiểm thử in chữ đó. Trang sinh tự động (`docs/triet-gia/*`,
`docs/them/sach.md`, `docs/them/kiem-chung.md`) và `data/kb/quotes.yml` được sinh lại bằng tool của chúng sau khi
chạy script, không sửa ở đây.

Giữ nguyên (nói tới site song song logos-zero, hoặc là lịch sử dự án): `KE-HOACH.md`, `ban-giao/*`, `README.md`,
`pyproject.toml`, `verification/*` (báo cáo nền), dòng 1 của `AGENTS.md` mục 1, `tests/test_parity.py` (HTML mẫu).
Thông báo lỗi khi nhập bản sao lưu (`merge.js`) nhận cả bản của logos-zero nên ghi cả hai tên.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OLD, NEW = "Logos Zero", "Logos"

# Thay riêng, làm trước phép thay chung (khóa: file; giá trị: các cặp cũ → mới, mỗi cặp phải gặp đúng một lần).
SPECIAL = {
    "docs/assets/js/merge.js": [
        ('"Đây không phải bản sao lưu của Logos Zero."', '"Đây không phải bản sao lưu của Logos hay Logos Zero."'),
    ],
    "AGENTS.md": [
        ('Bản dịch của site ghi "(bản dịch của Logos Zero)".', 'Bản dịch của site ghi "(bản dịch của Logos)".'),
    ],
    "tools/kb_quotes.py": [
        ('`translator: logos-zero` khi có chữ "(bản dịch của Logos Zero)"',
         '`translator: logos` khi có chữ "(bản dịch của Logos)" (trước đợt 5.0d: `logos-zero`)'),
        ('"translator": "logos-zero" if', '"translator": "logos" if'),
        ("r['translator'] == 'logos-zero'", "r['translator'] == 'logos'"),
    ],
}
# Tiêu đề H2 có chữ "Logos Zero" mà chưa có ID cố định: giữ anchor cũ (luật 5, link cũ không gãy).
SPECIAL.update({
    "docs/index.md": [("# Logos Zero\n", "# Logos {#logos-zero}\n"),
                      ("## Logos Zero là gì\n", "## Logos là gì {#logos-zero-la-gi}\n")],
    "docs/bat-dau/index.md": [("## Đọc Logos Zero thế nào?\n", "## Đọc Logos thế nào? {#doc-logos-zero-the-nao}\n")],
})
SPECIAL["tools/book.py"] = [('out.append("# Logos Zero — Sách in")', 'out.append("# Logos — Sách in {#logos-zero-sach-in}")')]
SPECIAL["tools/philosophers.py"] = [('L.append("## Đọc thêm trên Logos Zero")',
                                     'L.append("## Đọc thêm trên Logos {#doc-them-tren-logos-zero}")')]

# File chỉ thay riêng (SPECIAL), không thay chung.
ONLY_SPECIAL = {"AGENTS.md"}

FIXED = [
    "mkdocs.yml", "docs/manifest.webmanifest", "docs/sw.js", "docs/assets/img/icon.svg", "docs/assets/css/oz.css",
    ".github/ISSUE_TEMPLATE/bao-loi.yml", "package.json", "HUONG-DAN-VIET.md",
    "tools/book.py", "tools/figures.py", "tools/philosophers.py", "tools/verification_page.py", "tools/kb_quotes.py",
    "tests/test_book.py", "tests/test_kb_quotes.py",
    # Trang sinh tự động có đoạn viết tay ngoài khối gen (khối gen không chứa chữ này).
    "docs/lich-su/so-do-anh-huong.md", "docs/them/tu-dien.md",
]


def targets() -> list[str]:
    reg = yaml.safe_load((ROOT / "content.yml").read_text(encoding="utf-8"))
    generated = {"docs/" + e["path"] for e in reg["pages"] if e.get("generated")}
    files = [str(p.relative_to(ROOT)) for p in sorted((ROOT / "docs").rglob("*.md"))]
    files = [f for f in files if f not in generated]
    files += [str(p.relative_to(ROOT)) for p in sorted((ROOT / "docs" / "assets" / "js").glob("*.js"))]
    files += [str(p.relative_to(ROOT)) for p in sorted((ROOT / "docs" / "assets" / "data").glob("*.json"))]
    files += [str(p.relative_to(ROOT)) for p in sorted((ROOT / "data" / "people").glob("*.yml"))]
    return sorted(set(files + FIXED + list(SPECIAL)))


def convert(path: str, text: str) -> tuple[str, int]:
    """Phép thay riêng được giữ chỗ bằng dấu tạm trong lúc thay chung, để chữ mới của nó (có thể chứa "Logos Zero",
    như thông báo của merge.js) không bị thay tiếp. Chạy lại lần hai không đổi gì."""
    n = 0
    held: list[str] = []

    def hold(s: str) -> str:
        held.append(s)
        return f"\x00{len(held) - 1}\x00"

    for old, new in SPECIAL.get(path, []):
        if text.count(old) == 0 and new in text:      # đã đổi ở lần chạy trước
            text = text.replace(new, hold(new))
            continue
        if text.count(old) != 1:
            raise SystemExit(f"{path}: {old!r} gặp {text.count(old)} lần, phải đúng 1")
        text = text.replace(old, hold(new))
        n += 1
    if path not in ONLY_SPECIAL:
        n += text.count(OLD)
        text = text.replace(OLD, NEW)
    for k, s in enumerate(held):
        text = text.replace(f"\x00{k}\x00", s)
    return text, n


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    total = 0
    rows = []
    for f in targets():
        p = ROOT / f
        text = p.read_text(encoding="utf-8")
        new, n = convert(f, text)
        if n:
            rows.append((f, n))
            total += n
            if not a.dry_run:
                p.write_text(new, encoding="utf-8")
    for f, n in rows:
        print(f"{n:4d}  {f}")
    print(f"{'Sẽ đổi' if a.dry_run else 'Đã đổi'} {total} chỗ ở {len(rows)} file.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
