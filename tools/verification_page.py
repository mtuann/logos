"""Sinh trang Tình trạng kiểm chứng docs/them/kiem-chung.md từ verification/ledger.json và content.yml (đợt 4.8).

    python tools/verification_page.py          # ghi lại trang
    python tools/verification_page.py --check  # mã thoát 1 khi trang lệch sổ kiểm chứng (CI)

Số đơn vị theo khối (mục H2 của bài Lõi viết tay, gồm phần trước H2 đầu tiên) và theo trạng thái trong sổ; số bản
ghi trong kho dữ kiện. Dùng chung cách đếm với `tools/check_ledger.py --status`. Không ghi ngày: trang chỉ đổi khi
sổ hoặc danh sách trang đổi, nên `--check` ổn định.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import check_ledger as cl
from lz import ROOT

PAGE = ROOT / "docs" / "them" / "kiem-chung.md"
BLOCKS = {  # tên đọc được, theo nav (KE-HOACH.md mục 5.3)
    "bat-dau": "Bắt đầu", "cong-cu": "Công cụ tư duy", "tri-thuc": "Tri thức và chân lý",
    "tam-tri": "Tâm trí, AI và cái tôi", "tu-do": "Tự do và trách nhiệm", "dao-duc": "Đạo đức học",
    "luan-ly-ung-dung": "Luân lý ứng dụng", "chinh-tri": "Triết học chính trị", "my-hoc": "Cái đẹp và nghệ thuật",
    "ton-giao": "Tôn giáo", "sieu-hinh": "Siêu hình học", "y-nghia": "Ý nghĩa cuộc sống",
    "viet-nam": "Tư tưởng Việt Nam", "lich-su": "Lịch sử", "van-ban": "Đọc văn bản", "triet-gia": "Triết gia",
}
RECORDS = {"people": "Người (năm sinh mất, trường phái)", "works": "Tác phẩm", "quotes": "Trích dẫn",
           "events": "Sự kiện (ứng viên)", "sources": "Nguồn", "ho-so": "Hồ sơ triết gia",
           "philpapers": "Câu hỏi khảo sát PhilPapers 2020", "terms": "Thuật ngữ (Từ điển)",
           "fallacy-types": "Loại ngụy biện", "fallacies": "Đoạn luyện nhận diện ngụy biện",
           "lap-luan": "Đoạn luyện sơ đồ lập luận", "logic": "Bài tập logic", "thi-nghiem": "Thí nghiệm tư duy"}

HEAD = """---
title: Tình trạng kiểm chứng
description: Bao nhiêu phần của Logos Zero đã được kiểm chứng với nguồn, theo từng mảng nội dung.
updated: {updated}
---

# Tình trạng kiểm chứng

Mỗi bài thuộc phần **Lõi** (kiến thức kinh điển) được chia thành các mục, theo tiêu đề lớn trong bài. Từng mục được đối chiếu với nguồn đã mở được (năm, tên, tác phẩm, trích dẫn, số liệu, cách trình bày các lập trường), ghi bằng chứng vào sổ kiểm chứng, rồi đóng băng: sau đó mục chỉ được sửa khi có bằng chứng mới. Dải thông tin dưới tiêu đề mỗi bài cho biết bài đã được kiểm tới đâu.

"""
START, END = "<!-- gen:kiem-chung: không sửa tay; sinh bằng tools/verification_page.py -->", "<!-- /gen:kiem-chung -->"


def render(ledger: dict, root: Path = ROOT) -> str:
    entries = ledger.get("units", {})
    rows: dict[str, dict[str, int]] = {}
    for key, block in cl.core_units(root):
        r = rows.setdefault(block, {"tong": 0, "da-kiem": 0, "frozen": 0})
        r["tong"] += 1
        st = entries.get(key, {}).get("status")
        if st in r:
            r[st] += 1
    total = {k: sum(r[k] for r in rows.values()) for k in ("tong", "da-kiem", "frozen")}

    def pct(a, b):
        return f"{100 * a / b:.0f}%" if b else "—"
    started = any(e.get("status") in ("da-kiem", "frozen") for e in entries.values())
    L = [START, ""] + ([] if started else ["Việc kiểm chứng chưa bắt đầu: các con số dưới đây sẽ tăng dần.", ""]) + [
         "## Bài viết {#bai-viet}", "", "| Mảng | Số mục | Đã kiểm | Đã đóng băng | Tỉ lệ đóng băng |",
         "|---|---:|---:|---:|---:|"]
    for block, r in rows.items():
        L.append(f"| {BLOCKS.get(block, block)} | {r['tong']} | {r['da-kiem']} | {r['frozen']} | {pct(r['frozen'], r['tong'])} |")
    L.append(f"| **Tổng** | **{total['tong']}** | **{total['da-kiem']}** | **{total['frozen']}** | "
             f"**{pct(total['frozen'], total['tong'])}** |")
    other = set(entries) - {k for k, _ in cl.core_units(root)}
    L += ["", "## Dữ kiện {#du-kien}", "", "Năm, tên, tác phẩm, trích dẫn và số liệu dùng chung cho nhiều bài nằm trong kho dữ kiện; mỗi bản ghi cũng được kiểm một lần.", "",
          "| Loại | Số bản ghi | Đã đóng băng |", "|---|---:|---:|"]
    for kind, n in cl.record_counts(root).items():
        frozen = sum(1 for k in other if k.startswith(kind + "/") and entries[k]["status"] == "frozen")
        L.append(f"| {RECORDS.get(kind, kind)} | {n} | {frozen} |")
    L += ["", END]
    # Ngày cập nhật: ngày kiểm mới nhất trong sổ, không có thì ngày trang ra đời (để --check không phụ thuộc hôm nay).
    dates = [str(e["verified_on"]) for e in entries.values() if e.get("verified_on")]
    return HEAD.replace("{updated}", max(dates + ["2026-11-05"])) + "\n".join(L) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    text = render(cl.load())
    if args.check:
        if not PAGE.exists() or PAGE.read_text(encoding="utf-8") != text:
            print("docs/them/kiem-chung.md lệch sổ kiểm chứng — chạy: python tools/verification_page.py", file=sys.stderr)
            return 1
        print("Trang Tình trạng kiểm chứng khớp sổ.")
        return 0
    PAGE.write_text(text, encoding="utf-8")
    print(f"Đã ghi {PAGE.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
