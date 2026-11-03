"""Báo cáo nền: số đo nội dung trước khi làm lại, để so ở các đợt 1–3.

    python tools/baseline_report.py            # ghi verification/bao-cao-nen.md
    python tools/baseline_report.py --stdout   # in ra màn hình

Chạy lại cho cùng kết quả (không ghi ngày giờ). Đây là số nền: không chạy lại ở các đợt sau,
mà viết công cụ đo riêng rồi so với file này. Đặc tả: ban-giao/dot-0.md, mục "Đặc tả báo cáo nền".
Phạm vi chính: Lõi viết tay (tier: loi, generated: false trong content.yml). Hồ sơ triết gia (văn nằm trong
tools/philosophers.py) đếm riêng trên trang sinh triet-gia/*.md. Số đếm gõ tay (mục 3) quét mọi trang viết tay,
vì phần lớn nằm ở trang hệ thống (trang chủ, các index.md).
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "verification" / "bao-cao-nen.md"

FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
FENCE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.S | re.M)
GENBLOCK = re.compile(r"<!-- (gen|fig):([^ ]+) -->.*?<!-- /\1:\2 -->", re.S)
SVG = re.compile(r"<svg\b.*?</svg>", re.S | re.I)
H2 = re.compile(r"^## +(.+?)\s*$", re.M)
LINK_TARGET = re.compile(r"\]\([^)]*\)|<https?://[^>]+>|https?://\S+")

YEAR = re.compile(r"(?<![\d.,/-])(202[2-6])(?![\d])")
PHRASES = ["hiện nay", "gần đây", "tính đến", "đến nay", "mới nhất", "năm nay"]
PHRASE = re.compile(r"(?<![\wÀ-ỹ])(" + "|".join(PHRASES) + r")(?![\wÀ-ỹ])", re.I)
LAW = re.compile(r"(?<![\wÀ-ỹ])(Bộ luật|Nghị định|Luật (?=[A-ZĐÂĂÊÔƠƯÁÀẢÃẠ]))")
COUNT_NOUNS = ["bài", "hướng dẫn", "đoạn hội thoại", "đoạn", "câu hỏi", "câu quiz", "câu", "thuật ngữ", "triết gia",
               "chặng", "chủ đề", "hồ sơ", "thí nghiệm", "công cụ", "bài tập", "trang"]
HAND_COUNT = re.compile(r"(?<![\d.,])(\d{1,3}(?:\.\d{3})*)\s+(" + "|".join(sorted(COUNT_NOUNS, key=len, reverse=True)) + r")(?![\wÀ-ỹ])")
WORK_YEAR = re.compile(r"\*[^*\n]{2,160}?\*\s*\((?:khoảng |k\. |năm )?\d{3,4}")
QUOTE = re.compile(r"^\s*(?:!!!|\?\?\?\+?) quote\b", re.M)
LIST_ITEM = re.compile(r"^ {0,3}(?:\d+\.|[-*+]) +\S", re.M)
TABLE_ROW = re.compile(r"^\|.*\|\s*$", re.M)

REQUIRED = {  # KE-HOACH.md mục 5.1
    "cau-hoi": ["Thí nghiệm tư duy", "Câu hỏi thật sự là gì?", "Các lập trường chính", "Giới triết học ngày nay nghĩ gì",
                "Liên hệ đời sống", "Tự kiểm tra", "Tự viết", "Nguồn"],
    "cong-cu": ["Bài tập", "Tự kiểm tra", "Đi tiếp", "Nguồn"],
    "lich-su": ["Đọc tiếp", "Nguồn"],
    "doc": ["Bối cảnh", "Đọc từng đoạn", "Tái dựng lập luận", "Phản bác", "Hiểu lầm thường gặp", "Tự kiểm tra",
            "Câu hỏi để tự viết", "Đọc tiếp", "Nguồn"],
}
SUMMARY = re.compile(r'^!!! summary "Tóm tắt 5 phút"', re.M)

# Số đo ngày 23/10/2026 (ban-giao/dot-0.md): (giá trị, nhãn, phạm vi khớp, ghi chú). Cách đếm ngày đó không được
# ghi lại; phạm vi khớp được chọn theo số gần nhất, và ghi chú giải thích chỗ lệch.
REFERENCE = {
    "time_markers": (139, "dấu thời gian", "loi", ""),
    "time_pages": (66, "trang có dấu thời gian", "loi", ""),
    "work_year": (394, "chỗ “*Tác phẩm* (năm)”", "loi+tg", "số ngày 23/10 tính cả trang triết gia"),
    "quotes": (157, "khối `!!! quote`", "loi+tg", "số ngày 23/10 tính cả trang triết gia"),
    "sources": (628, "mục trong danh sách Nguồn", "loi", ""),
    "philpapers": (35, "bài có bảng PhilPapers", "loi", "4 bài ghi số kèm dấu % và thêm cột “Chỉ chọn lựa chọn này” "
                   "(`cau-hoi/binh-dang.md`, `cong-ly.md`, `nu-quyen.md`, `tai-san-rieng.md`); số ngày 23/10 chỉ tính bảng theo mẫu chuẩn"),
    "h2": (888, "mục H2", "loi", ""),
}


def body(text: str) -> str:
    """Bỏ front matter, khối code, khối sinh (gen/fig)."""
    return GENBLOCK.sub("", FENCE.sub("", FRONT.sub("", text, count=1)))


def split_sources(text: str) -> tuple[str, str]:
    """(phần trước mục Nguồn, mục Nguồn)."""
    m = re.search(r"^## +Nguồn\s*$", text, re.M)
    if not m:
        return text, ""
    rest = text[m.end():]
    n = re.search(r"^## ", rest, re.M)
    return text[:m.start()] + (rest[n.start():] if n else ""), rest[:n.start()] if n else rest


def norm_heading(h: str) -> str:
    h = re.sub(r"\s*\{[^}]*\}\s*$", "", h).strip()
    return re.sub(r"[?.:!]+$", "", h).strip().lower()


def section(text: str, title: str) -> str:
    m = re.search(r"^## +" + re.escape(title) + r"[^\n]*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    n = re.search(r"^## ", rest, re.M)
    return rest[:n.start()] if n else rest


def area_of(path: str) -> str:
    return path.split("/", 1)[0] if "/" in path else "(trang chủ)"


def measure(registry: dict) -> dict:
    pages = registry["pages"]
    r: dict = {"areas": {}, "time": [], "counts": [], "missing": [], "totals": Counter(), "gen": Counter()}
    for e in pages:
        path = e["path"]
        raw = (DOCS / path).read_text(encoding="utf-8")
        a = r["areas"].setdefault(area_of(path), Counter())
        a["pages"] += 1
        a["chars"] += len(SVG.sub("", FRONT.sub("", raw, count=1)))
        text = body(raw)
        h2 = len(H2.findall(text))
        if e["generated"]:
            a["pages_gen"] += 1
            a["h2_gen"] += h2
            if e["type"] == "triet-gia" and not path.endswith("index.md"):
                r["gen"]["triet_gia_pages"] += 1
                r["gen"]["work_year"] += len(WORK_YEAR.findall(text))
                r["gen"]["quotes"] += len(QUOTE.findall(text))
                r["gen"]["sources"] += len(LIST_ITEM.findall(split_sources(text)[1]))
            continue
        a["h2"] += h2
        prose, sources = split_sources(text)
        plain = LINK_TARGET.sub("", prose)
        for m in HAND_COUNT.finditer(plain):
            r["counts"].append((path, f"{m.group(1)} {m.group(2)}"))
        if e["tier"] != "loi":
            continue
        r["totals"]["loi_pages"] += 1
        r["totals"]["h2"] += h2
        n_year, n_phr, n_law = len(YEAR.findall(plain)), len(PHRASE.findall(plain)), len(LAW.findall(plain))
        if n_year + n_phr + n_law:
            r["time"].append((path, n_year, n_phr, n_law))
        r["totals"]["work_year"] += len(WORK_YEAR.findall(text))
        r["totals"]["quotes"] += len(QUOTE.findall(text))
        r["totals"]["sources"] += len(LIST_ITEM.findall(sources))
        if "PhilPapers" in text and TABLE_ROW.search(section(text, "Giới triết học ngày nay nghĩ gì")):
            r["totals"]["philpapers"] += 1
        req = REQUIRED.get(e["type"])
        if req:
            have = {norm_heading(h) for h in H2.findall(text)}
            miss = [h for h in req if norm_heading(h) not in have]
            if e["type"] == "cau-hoi" and not SUMMARY.search(text):
                miss.append('hộp !!! summary "Tóm tắt 5 phút"')
            if miss:
                r["missing"].append((path, miss))
    r["totals"]["time_markers"] = sum(y + p + l for _, y, p, l in r["time"])
    r["totals"]["time_pages"] = len(r["time"])
    return r


def render(r: dict) -> str:
    t = r["totals"]
    L = ["# Báo cáo nền", "",
         "Sinh bằng `tools/baseline_report.py` trên commit đầu của đợt 0 (nội dung nguyên trạng từ `logos-zero@ecb2bb8`).",
         "Chạy lại cho cùng kết quả. Không sửa tay; không chạy lại ở các đợt sau: đây là số nền để so.", "",
         "Phạm vi chính: **Lõi viết tay** (`tier: loi`, `generated: false` trong `content.yml`): " + str(t["loi_pages"]) + " bài cần kiểm bằng tay. "
         "Trang sinh tự động chỉ được đếm số trang, số mục H2 và dung lượng; hồ sơ triết gia (văn nằm trong "
         "`tools/philosophers.py`) có cột riêng ở mục 4. Số đếm gõ tay (mục 3) quét mọi trang viết tay.", "",
         "## Đối chiếu với số đo ngày 23/10/2026", "",
         "| Chỉ số | 23/10/2026 | Lõi viết tay | Lõi viết tay + trang triết gia | Lệch (cột khớp) | Ghi chú |",
         "|---|---:|---:|---:|---:|---|"]
    g = r["gen"]
    for key, (ref, label, scope, note) in REFERENCE.items():
        loi = t[key]
        both = loi + g.get(key, 0) if key in ("work_year", "quotes", "sources") else None
        now = both if scope == "loi+tg" else loi
        dev = (now - ref) / ref * 100 if ref else 0
        L.append(f"| {label} | {ref} | {loi} | {'—' if both is None else both} | {f'{dev:+.1f}'.replace('.', ',')}% | {note} |")
    L += ["", "## 1. Theo khu vực", "",
          "| Khu vực | Trang | Trong đó sinh tự động | Mục H2 (viết tay) | Mục H2 (trang sinh) | Dung lượng (nghìn ký tự, bỏ SVG) |",
          "|---|---:|---:|---:|---:|---:|"]
    tot = Counter()
    for area in sorted(r["areas"]):
        a = r["areas"][area]
        tot.update(a)
        L.append(f"| `{area}` | {a['pages']} | {a['pages_gen']} | {a['h2']} | {a['h2_gen']} | {a['chars'] / 1000:.0f} |")
    L.append(f"| **Tổng** | **{tot['pages']}** | **{tot['pages_gen']}** | **{tot['h2']}** | **{tot['h2_gen']}** | **{tot['chars'] / 1000:.0f}** |")
    L += ["", "## 2. Dấu thời gian", "",
          f"Trong Lõi viết tay, sau khi bỏ front matter, khối code, khối sinh, mục Nguồn và địa chỉ link. Tổng **{t['time_markers']}** dấu ở **{t['time_pages']}** trang.",
          "Cột: năm 2022–2026; cụm " + ", ".join(f"“{p}”" for p in PHRASES) + "; văn bản luật (“Luật …”, “Nghị định”, “Bộ luật”).", "",
          "| Trang | Năm | Cụm thời gian | Luật | Tổng |", "|---|---:|---:|---:|---:|"]
    for path, y, p, l in sorted(r["time"], key=lambda x: (-(x[1] + x[2] + x[3]), x[0])):
        L.append(f"| `{path}` | {y} | {p} | {l} | {y + p + l} |")
    by_page = Counter(p for p, _ in r["counts"])
    L += ["", "## 3. Số đếm gõ tay trong văn xuôi", "",
          f"Số đi trước danh từ chỉ nội dung của site (bài, hướng dẫn, câu hỏi, thuật ngữ, triết gia…). Tổng **{len(r['counts'])}** chỗ ở **{len(by_page)}** trang. "
          "Không phải chỗ nào cũng là số đếm của site (ví dụ “2 bài tập” trong một bài); đợt 3 lọc lại khi thay bằng shortcode.", "",
          "| Trang | Chỗ |", "|---|---|"]
    grouped: dict[str, list[str]] = {}
    for path, phrase in r["counts"]:
        grouped.setdefault(path, []).append(phrase)
    for path in sorted(grouped):
        L.append(f"| `{path}` | " + "; ".join(grouped[path]) + " |")
    L += ["", "## 4. Dữ kiện gõ tay", "",
          "| Chỉ số | Lõi viết tay | Trang triết gia (sinh) |", "|---|---:|---:|",
          f"| Chỗ dạng “*Tác phẩm* (năm)” | {t['work_year']} | {g['work_year']} |",
          f"| Khối `!!! quote` | {t['quotes']} | {g['quotes']} |",
          f"| Mục trong danh sách Nguồn | {t['sources']} | {g['sources']} |",
          f"| Bài có bảng PhilPapers (trong mục “Giới triết học ngày nay nghĩ gì”) | {t['philpapers']} | — |",
          "", f"Trang triết gia đếm: {g['triet_gia_pages']} (không tính `triet-gia/index.md`).",
          "", "## 5. Trang thiếu mục bắt buộc (KE-HOACH.md mục 5.1)", ""]
    if r["missing"]:
        L += [f"{len(r['missing'])} trang.", "", "| Trang | Thiếu |", "|---|---|"]
        for path, miss in sorted(r["missing"]):
            L.append(f"| `{path}` | " + " · ".join(miss) + " |")
    else:
        L.append("Không trang nào thiếu.")
    L += ["", "## Cách đếm", "",
          "- Mục H2: dòng bắt đầu bằng `## ` ngoài khối code và ngoài khối sinh.",
          "- Năm: số 2022–2026 đứng riêng (không nằm trong số khác, ngày dạng 2026-10-12 vẫn tính một lần).",
          "- “*Tác phẩm* (năm)”: chữ in nghiêng ngay trước ngoặc đơn mở đầu bằng năm 3–4 chữ số (cho phép “khoảng”, “k.”, “năm” đứng trước), ví dụ “*Cộng hòa* (khoảng 375 TCN)”.",
          "- Mục Nguồn: dòng danh sách (`1.`, `-`, `*`) thụt không quá 3 dấu cách trong mục `## Nguồn`.",
          "- Mục bắt buộc: so tiêu đề H2 không phân biệt hoa thường, bỏ dấu `?`, `.`, `:` ở cuối và thuộc tính `{…}`.", ""]
    return "\n".join(L)


def main(argv: list[str]) -> int:
    registry = yaml.safe_load((ROOT / "content.yml").read_text(encoding="utf-8"))
    text = render(measure(registry))
    if "--stdout" in argv:
        sys.stdout.write(text)
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"Đã ghi {OUT.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
