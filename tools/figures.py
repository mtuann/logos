"""Sinh hình minh họa SVG cho Logos.

Cách dùng trong bài viết — đặt cặp dấu ở chỗ muốn hiện hình:

    <!-- fig:ten-hinh -->
    <!-- /fig:ten-hinh -->

SVG được nhúng trực tiếp (inline) nên MỘT file duy nhất tự theo sáng/tối/in
qua CSS vars của site (var(--oz-...), currentColor) — không xuất 3 bản.
File .svg rời cũng được sinh ra ở docs/assets/img/ để tham khảo.

    python tools/figures.py          # sinh lại hình
    python tools/figures.py --check  # báo lỗi (mã thoát 1) nếu trang/file lệch
"""

from __future__ import annotations

import json
import math
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
IMG_DIR = DOCS / "assets" / "img"


def r(x: float) -> str:
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def box(x, y, w, h, label, dashed=False, fontsize=15):
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"'
        f' style="fill:var(--oz-paper);stroke:var(--oz-ink)" stroke-width="2"{dash}/>'
        f'<text x="{r(x + w / 2)}" y="{r(y + h / 2 + fontsize * 0.35)}" text-anchor="middle"'
        f' style="fill:currentColor" font-size="{fontsize}">{escape(label)}</text>'
    )


def arrow(x1, y1, x2, y2, dashed=False, color="var(--oz-ink)", w=2):
    dx, dy = x2 - x1, y2 - y1
    leng = math.hypot(dx, dy) or 1
    ux, uy = dx / leng, dy / leng
    ah_len, ah_w = 10, 7
    bx, by = x2 - ux * ah_len, y2 - uy * ah_len
    px, py = -uy, ux
    dash = ' stroke-dasharray="7 5"' if dashed else ""
    return (
        f'<line x1="{r(x1)}" y1="{r(y1)}" x2="{r(bx)}" y2="{r(by)}"'
        f' style="stroke:{color}" stroke-width="{w}"{dash}/>'
        f'<polygon points="{r(x2)},{r(y2)} {r(bx + px * ah_w / 2)},{r(by + py * ah_w / 2)}'
        f' {r(bx - px * ah_w / 2)},{r(by - py * ah_w / 2)}" style="fill:{color}"/>'
    )


def poly_arrow(pts, dashed=False, color="var(--oz-ink)", w=2):
    """Mũi tên gấp khúc qua các điểm: đường polyline + đầu tên ở điểm cuối."""
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    leng = math.hypot(dx, dy) or 1
    ux, uy = dx / leng, dy / leng
    ah_len, ah_w = 10, 7
    bx, by = x2 - ux * ah_len, y2 - uy * ah_len
    px, py = -uy, ux
    dash = ' stroke-dasharray="7 5"' if dashed else ""
    d = "M " + " L ".join(f"{r(x)},{r(y)}" for x, y in pts[:-1] + [(bx, by)])
    return (
        f'<path d="{d}" fill="none" style="stroke:{color}" stroke-width="{w}"{dash}/>'
        f'<polygon points="{r(x2)},{r(y2)} {r(bx + px * ah_w / 2)},{r(by + py * ah_w / 2)}'
        f' {r(bx - px * ah_w / 2)},{r(by - py * ah_w / 2)}" style="fill:{color}"/>'
    )


def circle(cx, cy, rad, label, fill, label_dy=0, fontsize=16):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{rad}" style="fill:{fill};stroke:var(--oz-ink)"'
        f' stroke-width="2" fill-opacity="0.14"/>'
        f'<text x="{cx}" y="{r(cy + label_dy)}" text-anchor="middle"'
        f' style="fill:currentColor" font-size="{fontsize}">{escape(label)}</text>'
    )


def svg_wrap(inner: str, width: int, height: int, label: str) -> str:
    return (
        f'<svg viewBox="0 0 {width} {height}" class="oz-fig__svg" role="img"'
        f' aria-label="{escape(label)}">{inner}</svg>'
    )


# ---------------- 2 hình đầu tiên ----------------

def fig_so_do_lap_luan() -> str:
    parts = [
        box(30, 30, 200, 60, "Tiền đề 1"),
        box(30, 120, 200, 60, "Tiền đề 2"),
        box(30, 210, 200, 60, "Kết luận"),
        box(300, 120, 230, 60, "Giả định ngầm", dashed=True),
        poly_arrow([(30, 60), (14, 60), (14, 240), (30, 240)]),
        arrow(130, 180, 130, 210),
        arrow(300, 150, 200, 210, dashed=True),
    ]
    return svg_wrap("".join(parts), 560, 300,
                    "Sơ đồ lập luận: hai tiền đề và một giả định ngầm cùng hỗ trợ kết luận")


def fig_dieu_kien_can_du() -> str:
    parts = [
        f'<text x="140" y="26" text-anchor="middle" style="fill:currentColor" font-size="15">'
        f'P là điều kiện ĐỦ của Q</text>',
        circle(140, 160, 95, "Q", "var(--oz-ok)", label_dy=-62),
        circle(140, 160, 48, "P", "var(--oz-accent)", label_dy=6),
        f'<text x="140" y="288" text-anchor="middle" style="fill:currentColor" font-size="13">'
        f'có P thì có Q (P → Q)</text>',
        f'<text x="420" y="26" text-anchor="middle" style="fill:currentColor" font-size="15">'
        f'P là điều kiện CẦN của Q</text>',
        circle(420, 160, 95, "P", "var(--oz-ok)", label_dy=-62),
        circle(420, 160, 48, "Q", "var(--oz-accent)", label_dy=6),
        f'<text x="420" y="288" text-anchor="middle" style="fill:currentColor" font-size="13">'
        f'không P thì không Q (Q → P)</text>',
    ]
    return svg_wrap("".join(parts), 560, 300,
                    "P là điều kiện đủ của Q: vòng P nằm trong vòng Q. "
                    "P là điều kiện cần của Q: vòng Q nằm trong vòng P")


def box2(x, y, w, h, title, sub="", dashed=False, tsize=15, ssize=12.5):
    """Hộp hai dòng: tiêu đề đậm + dòng phụ nhỏ."""
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    title_y = r(y + h / 2 - 4) if sub else r(y + h / 2 + tsize * 0.35)
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"'
        f' style="fill:var(--oz-paper);stroke:var(--oz-ink)" stroke-width="2"{dash}/>'
        f'<text x="{r(x + w / 2)}" y="{title_y}" text-anchor="middle"'
        f' style="fill:currentColor" font-size="{tsize}" font-weight="bold">{escape(title)}</text>'
    ]
    if sub:
        parts.append(
            f'<text x="{r(x + w / 2)}" y="{r(y + h / 2 + 17)}" text-anchor="middle"'
            f' style="fill:currentColor" font-size="{ssize}">{escape(sub)}</text>'
        )
    return "".join(parts)


# ---------------- 5 hình mới ----------------

def fig_jtb_venn() -> str:
    a, b, c, rad = (205, 140), (355, 140), (280, 265), 110
    parts = []
    for cx, cy in (a, b, c):
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{rad}"'
            f' style="fill:var(--oz-accent);stroke:var(--oz-ink)"'
            f' stroke-width="2" fill-opacity="0.16"/>'
        )
    parts.append('<text x="135" y="136" text-anchor="middle"'
                 ' style="fill:currentColor" font-size="14">Tin rằng p</text>')
    parts.append('<text x="430" y="136" text-anchor="middle"'
                 ' style="fill:currentColor" font-size="14">p đúng</text>')
    parts.append('<text x="280" y="358" text-anchor="middle"'
                 ' style="fill:currentColor" font-size="14">Có lý do tốt</text>')
    parts.append('<text x="280" y="184" text-anchor="middle"'
                 ' style="fill:currentColor" font-size="16" font-weight="bold">JTB?</text>')
    parts.append(arrow(400, 392, 300, 190, dashed=True))
    parts.append('<text x="552" y="408" text-anchor="end"'
                 ' style="fill:currentColor" font-size="13">Ví dụ Gettier: đủ cả ba điều kiện,</text>')
    parts.append('<text x="552" y="426" text-anchor="end"'
                 ' style="fill:currentColor" font-size="13">vẫn không phải tri thức.</text>')
    return svg_wrap("".join(parts), 560, 440,
                    "Biểu đồ Venn: tri thức là giao của niềm tin, chân lý và biện minh; "
                    "ví dụ Gettier nằm ở giữa mà vẫn không phải tri thức")


def fig_cay_tu_do_y_chi() -> str:
    parts = [
        box2(220, 16, 300, 52, "Tất định luận có loại trừ tự do?", tsize=14),
        box2(12, 120, 228, 64, "Bất tương thích luận", "không tương thích"),
        box2(246, 120, 228, 64, "Tương thích luận", "tự do = làm theo ý mình"),
        box2(480, 120, 228, 64, "Hoài nghi về trách nhiệm",
             "trách nhiệm tối hậu là ảo", dashed=True),
        box2(15, 250, 200, 64, "Tất định luận cứng", "không có tự do ý chí"),
        box2(235, 250, 200, 64, "Thuyết ý chí tự do", "tất định luận sai"),
        arrow(370, 68, 126, 120),
        arrow(370, 68, 360, 120),
        arrow(370, 68, 594, 120),
        arrow(126, 184, 115, 250),
        arrow(126, 184, 335, 250),
    ]
    return svg_wrap("".join(parts), 740, 336,
                    "Cây các lập trường về tự do ý chí: bất tương thích luận "
                    "(tất định luận cứng, thuyết ý chí tự do), tương thích luận, "
                    "và hoài nghi về trách nhiệm")


def bar_chart(rows: list[tuple[str, float]], title: str, note: str) -> str:
    label_w, bar_max, row_h, top = 220, 285, 42, 52
    w = label_w + bar_max + 64
    h = top + len(rows) * row_h + 38
    parts = [
        f'<text x="{w / 2}" y="26" text-anchor="middle"'
        f' style="fill:currentColor" font-size="15" font-weight="bold">{escape(title)}</text>'
    ]
    for i, (label, v) in enumerate(rows):
        y = top + i * row_h
        bw = v / 100 * bar_max
        parts.append(
            f'<text x="{label_w - 10}" y="{r(y + 22)}" text-anchor="end"'
            f' style="fill:currentColor" font-size="13">{escape(label)}</text>'
        )
        parts.append(
            f'<rect x="{label_w}" y="{r(y + 6)}" width="{r(bw)}" height="24" rx="5"'
            f' style="fill:var(--oz-accent)" fill-opacity="0.75"/>'
        )
        parts.append(
            f'<text x="{r(label_w + bw + 8)}" y="{r(y + 23)}"'
            f' style="fill:currentColor" font-size="13">{str(v).replace(".", ",")}%</text>'
        )
    parts.append(
        f'<text x="{w / 2}" y="{h - 12}" text-anchor="middle"'
        f' style="fill:currentColor" font-size="12">{escape(note)}</text>'
    )
    return svg_wrap("".join(parts), w, h, title + ". " + note)


NOTE_PP = "PhilPapers Survey 2020 — % chấp nhận hoặc nghiêng về"
PP_JSON = ROOT / "data" / "kb" / "philpapers-2020.json"
_PP: dict | None = None


def pp(qid: str, bars: list[tuple[str, str]]) -> list[tuple[str, float]]:
    """(nhãn trên hình, % của lựa chọn `oid` trong câu `qid`) — số đọc từ data/kb/philpapers-2020.json (đợt 3)."""
    global _PP
    if _PP is None:
        _PP = {q["id"]: q for q in json.loads(PP_JSON.read_text(encoding="utf-8"))["questions"]}
    opts = {o["id"]: o for o in _PP[qid]["options"]}
    return [(label, opts[oid]["pct"]) for label, oid in bars]


def ppv(qid: str, oid: str) -> str:
    """% của lựa chọn `oid` trong câu `qid`, một chữ số lẻ, dấu phẩy — để ghép vào chữ của hình (nhãn, alt, chú thích),
    không gõ tay số khảo sát (lint_so_lieu, luật du-lieu; cổng 5.2)."""
    pp(qid, [])                                   # nạp kho
    return f"{next(o for o in _PP[qid]['options'] if o['id'] == oid)['pct']:.1f}".replace(".", ",")


def ppn(qid: str) -> str:
    """Số người trả lời câu `qid` (kho làm tròn hàng chục), in kiểu Việt Nam: 1.020."""
    pp(qid, [])
    return f"{_PP[qid]['n']:,}".replace(",", ".")


def fig_philpapers_dao_duc() -> str:
    return bar_chart(
        pp("dao-duc-hoc-chuan-tac", [("Đạo đức học đức hạnh", "dao-duc-hoc-duc-hanh"),
                                     ("Nghĩa vụ luận", "nghia-vu-luan"), ("Hệ quả luận", "he-qua-luan")]),
        "Đạo đức học chuẩn tắc: ba lập trường lớn", NOTE_PP)


def fig_philpapers_tu_do() -> str:
    return bar_chart(
        pp("tu-do-y-chi", [("Tương thích luận", "tuong-thich-luan"),
                           ("Thuyết ý chí tự do", "thuyet-y-chi-tu-do-libertarianism"),
                           ("Không có tự do ý chí", "khong-co-tu-do-y-chi"), ("Khác", "khac")]),
        "Tự do ý chí: giới triết học nghĩ gì", NOTE_PP)


def fig_philpapers_jtb() -> str:
    return bar_chart(
        pp("phan-tich-khai-niem-tri-thuc", [("Niềm tin đúng được biện minh", "niem-tin-dung-duoc-bien-minh-jtb"),
                                            ("Một phân tích khác", "mot-phan-tich-khac"),
                                            ("Không có phân tích nào", "khong-co-phan-tich-nao"), ("Khác", "khac")]),
        "Tri thức là gì? Phân tích khái niệm", NOTE_PP)


# ---------------- 10 hình mới (đợt 2) ----------------

def fig_rawls_man_vo_tri() -> str:
    parts = [
        '<text x="320" y="26" text-anchor="middle"'
        ' style="fill:currentColor" font-size="16" font-weight="bold">'
        'Thí nghiệm tư duy: màn vô tri</text>',
        '<rect x="30" y="52" width="190" height="292" rx="12"'
        ' style="fill:var(--oz-paper);stroke:var(--oz-ink)" stroke-width="2"'
        ' stroke-dasharray="8 6"/>',
        '<text x="125" y="80" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">MÀN VÔ TRI</text>',
        '<text x="125" y="101" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">(không biết mình là ai)</text>',
        '<circle cx="125" cy="165" r="20"'
        ' style="fill:var(--oz-accent);stroke:var(--oz-ink)"'
        ' stroke-width="2" fill-opacity="0.35"/>',
        '<rect x="103" y="190" width="44" height="80" rx="20"'
        ' style="fill:var(--oz-accent);stroke:var(--oz-ink)"'
        ' stroke-width="2" fill-opacity="0.35"/>',
        '<text x="125" y="302" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">người chọn</text>',
        arrow(220, 165, 300, 110),
        arrow(220, 165, 300, 280),
        box2(310, 55, 300, 110, "A: Bình quân", "mọi người như nhau", tsize=14),
        box2(310, 225, 300, 110, "B: Chênh lệch", "người nghèo nhất khá hơn",
             tsize=14),
        '<text x="320" y="380" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">'
        'Bạn sẽ chọn A hay B — khi chưa biết mình là ai?</text>',
    ]
    return svg_wrap("".join(parts), 640, 400,
                    "Người sau màn vô tri chọn giữa xã hội bình quân "
                    "và xã hội chênh lệch nhưng người nghèo nhất khá hơn")


def fig_pascal_wager() -> str:
    parts = [
        '<text x="252" y="40" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">Chúa tồn tại</text>',
        '<text x="477" y="40" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">'
        'Chúa không tồn tại</text>',
        '<text x="70" y="126" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">Tin Chúa</text>',
        '<text x="70" y="246" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">Không tin</text>',
        # ô thắng được tô nhẹ
        '<rect x="140" y="60" width="225" height="120" rx="10"'
        ' style="fill:var(--oz-accent);stroke:var(--oz-ink)"'
        ' stroke-width="2" fill-opacity="0.16"/>',
        '<text x="252" y="116" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">'
        'Được cứu rỗi</text>',
        '<text x="252" y="137" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">lợi ích vô hạn</text>',
        box2(365, 60, 225, 120, "Không mất gì đáng kể", "chỉ tốn chút công sức",
             tsize=14),
        box2(140, 180, 225, 120, "Mất mát vô hạn", "hình phạt đời đời", tsize=14),
        box2(365, 180, 225, 120, "Không thêm, không bớt", "cả hai đều như nhau",
             tsize=14),
        '<text x="310" y="338" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">'
        'Pascal: \u201ctin\u201d là canh bạc khôn ngoan — được thì vô hạn,'
        ' mất thì hữu hạn.</text>',
    ]
    return svg_wrap("".join(parts), 620, 360,
                    "Ma trận canh bạc của Pascal: tin hay không tin, "
                    "nhân với Chúa tồn tại hay không tồn tại")


def fig_mctaggart_time() -> str:
    parts = [
        '<text x="320" y="28" text-anchor="middle"'
        ' style="fill:currentColor" font-size="15" font-weight="bold">'
        'Chuỗi A: quá khứ – hiện tại – tương lai</text>',
        '<line x1="60" y1="95" x2="272" y2="95"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        '<line x1="368" y1="95" x2="580" y2="95"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        '<text x="150" y="78" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">quá khứ</text>',
        '<text x="490" y="78" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">tương lai</text>',
        '<rect x="272" y="68" width="96" height="54" rx="8"'
        ' style="fill:var(--oz-accent);stroke:var(--oz-ink)"'
        ' stroke-width="2" fill-opacity="0.22"/>',
        '<text x="320" y="101" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13" font-weight="bold">HIỆN TẠI</text>',
        circle(190, 95, 6, "", "var(--oz-accent)"),
        circle(450, 95, 6, "", "var(--oz-accent)"),
        '<text x="190" y="124" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">sinh nhật bạn</text>',
        '<text x="450" y="124" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">Tết</text>',
        '<text x="320" y="152" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">'
        '\u201chiện tại\u201d trượt dọc trục theo thời gian</text>',
        '<text x="320" y="188" text-anchor="middle"'
        ' style="fill:currentColor" font-size="15" font-weight="bold">'
        'Chuỗi B: chỉ có trước – sau</text>',
        '<line x1="60" y1="240" x2="580" y2="240"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        circle(200, 240, 6, "", "var(--oz-accent)"),
        circle(440, 240, 6, "", "var(--oz-accent)"),
        '<text x="200" y="222" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">sinh nhật bạn</text>',
        '<text x="440" y="222" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">Tết</text>',
        '<text x="320" y="222" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13" font-weight="bold">trước</text>',
        '<text x="320" y="282" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">'
        'quan hệ \u201ctrước–sau\u201d không đổi dù hôm nay là ngày nào</text>',
    ]
    return svg_wrap("".join(parts), 640, 310,
                    "Chuỗi A: hiện tại di chuyển giữa quá khứ và tương lai. "
                    "Chuỗi B: chỉ có quan hệ trước–sau, không có hiện tại đặc biệt")


def fig_platon_hai_the_gioi() -> str:
    parts = [
        '<rect x="30" y="40" width="260" height="260" rx="12"'
        ' style="fill:var(--oz-paper);stroke:var(--oz-ink)" stroke-width="2"/>',
        '<text x="160" y="72" text-anchor="middle"'
        ' style="fill:currentColor" font-size="15" font-weight="bold">'
        'Thế giới Ý niệm</text>',
        '<text x="160" y="94" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">(vĩnh cửu, hoàn hảo)</text>',
        '<polygon points="160,120 100,230 220,230"'
        ' style="fill:var(--oz-accent);stroke:var(--oz-ink)"'
        ' stroke-width="2" fill-opacity="0.2"/>',
        '<text x="160" y="258" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">Tam giác lý tưởng</text>',
        '<text x="160" y="278" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">ba góc cộng đúng 180°</text>',
        '<rect x="350" y="40" width="260" height="260" rx="12"'
        ' style="fill:var(--oz-paper);stroke:var(--oz-ink)" stroke-width="2"/>',
        '<text x="480" y="72" text-anchor="middle"'
        ' style="fill:currentColor" font-size="15" font-weight="bold">'
        'Thế giới cảm giác</text>',
        '<text x="480" y="94" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">(đổi thay, bóng mờ)</text>',
        '<polygon points="480,125 423,232 537,224"'
        ' style="fill:var(--oz-accent);stroke:var(--oz-ink)"'
        ' stroke-width="2" stroke-dasharray="8 6" fill-opacity="0.12"/>',
        '<text x="480" y="258" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">hình vẽ tay</text>',
        '<text x="480" y="278" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">méo mó, phai dần</text>',
        arrow(350, 170, 290, 170),
        '<text x="320" y="155" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">tham dự</text>',
        '<text x="320" y="345" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">'
        'Vật cảm giác \u201ctham dự\u201d vào Ý niệm,'
        ' nhưng chỉ là bóng mờ của nó.</text>',
    ]
    return svg_wrap("".join(parts), 640, 380,
                    "Thế giới Ý niệm với tam giác lý tưởng và thế giới cảm giác "
                    "với hình vẽ tay méo mó, nối bằng quan hệ tham dự")


def fig_frankfurt_black() -> str:
    parts = [
        box2(220, 16, 200, 64, "Jones quyết định", "giết Smith", tsize=13),
        box2(30, 116, 250, 72, "Nhánh 1: Jones tự làm", "Black chỉ đứng nhìn",
             tsize=13),
        box2(360, 116, 250, 72, "Nhánh 2: Jones do dự",
             "Black can thiệp, ép tay", tsize=13),
        arrow(320, 80, 155, 116),
        arrow(320, 80, 485, 116),
        box2(220, 232, 200, 72, "Kết quả", "Smith chết — như nhau", tsize=13),
        arrow(155, 188, 320, 232),
        arrow(485, 188, 320, 232),
        '<text x="320" y="352" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">'
        'Jones chịu trách nhiệm ở cả hai nhánh — dù ở nhánh 2,'
        ' anh ta không thể làm khác.</text>',
    ]
    return svg_wrap("".join(parts), 640, 390,
                    "Hai nhánh: Jones tự quyết định hoặc Black can thiệp — "
                    "cùng dẫn đến một kết quả")


def fig_tuong_lai_phan_nhanh() -> str:
    parts = [
        '<line x1="320" y1="50" x2="320" y2="300"'
        ' style="stroke:var(--oz-ink)" stroke-width="1.5" stroke-dasharray="7 5"/>',
        '<text x="160" y="30" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">'
        'Tất định: một đường duy nhất</text>',
        '<text x="480" y="30" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">'
        'Tương lai mở: phân nhánh</text>',
        arrow(50, 175, 270, 175),
        circle(100, 175, 6, "", "var(--oz-accent)"),
        circle(160, 175, 6, "", "var(--oz-accent)"),
        circle(235, 175, 6, "", "var(--oz-accent)"),
        '<text x="100" y="207" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">quá khứ</text>',
        '<text x="160" y="207" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">hiện tại</text>',
        '<text x="235" y="207" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">tương lai</text>',
        '<line x1="360" y1="175" x2="430" y2="175"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        circle(360, 175, 6, "", "var(--oz-accent)"),
        arrow(430, 175, 548, 105),
        arrow(430, 175, 548, 175),
        arrow(430, 175, 548, 245),
        circle(555, 105, 6, "", "var(--oz-accent)"),
        circle(555, 175, 6, "", "var(--oz-accent)"),
        circle(555, 245, 6, "", "var(--oz-accent)"),
        '<text x="395" y="207" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">hiện tại</text>',
        '<text x="572" y="110" style="fill:currentColor" font-size="13">A</text>',
        '<text x="572" y="180" style="fill:currentColor" font-size="13">B</text>',
        '<text x="572" y="250" style="fill:currentColor" font-size="13">C</text>',
        '<text x="320" y="336" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">'
        'Cùng một \u201chiện tại\u201d, hai bức tranh khác nhau về tương lai.</text>',
    ]
    return svg_wrap("".join(parts), 640, 360,
                    "Một đường thẳng duy nhất so với cây phân nhánh: "
                    "hai cách hình dung tương lai")


def fig_popper_kiem_chung() -> str:
    parts = [
        box2(205, 40, 150, 66, "Giả thuyết", "đưa ra lý thuyết",
             tsize=13, ssize=12),
        box2(345, 177, 150, 66, "Dự đoán", "phải có thể sai",
             tsize=13, ssize=12),
        box2(205, 314, 150, 66, "Kiểm tra", "thí nghiệm, quan sát",
             tsize=13, ssize=12),
        box2(65, 177, 150, 66, "Bác bỏ?", "bỏ — hoặc tạm giữ",
             tsize=13, ssize=12),
        arrow(352, 100, 358, 177),
        arrow(420, 243, 360, 314),
        arrow(205, 347, 140, 243),
        arrow(140, 177, 205, 106),
        '<text x="280" y="406" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">'
        'Lý thuyết khoa học phải dám \u201csai\u201d: dự đoán càng mạo hiểm,'
        ' kiểm tra càng có giá trị.</text>',
    ]
    return svg_wrap("".join(parts), 560, 424,
                    "Vòng tròn bốn bước: giả thuyết, dự đoán, kiểm tra, "
                    "bác bỏ hoặc tạm giữ")


def fig_condorcet() -> str:
    parts = [
        '<text x="140" y="30" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">'
        'Thứ tự ưu tiên của 3 cử tri</text>',
        box2(30, 48, 220, 66, "Cử tri 1", "A > B > C", tsize=13),
        box2(30, 128, 220, 66, "Cử tri 2", "B > C > A", tsize=13),
        box2(30, 208, 220, 66, "Cử tri 3", "C > A > B", tsize=13),
        '<text x="450" y="30" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">'
        'Từng cặp: đa số thắng 2–1</text>',
        circle(450, 110, 30, "A", "var(--oz-accent)"),
        circle(545, 255, 30, "B", "var(--oz-accent)"),
        circle(355, 255, 30, "C", "var(--oz-accent)"),
        arrow(467, 136, 528, 229),
        arrow(513, 255, 387, 255),
        arrow(372, 229, 433, 136),
        '<text x="502" y="186" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12">2–1</text>',
        '<text x="450" y="244" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12">2–1</text>',
        '<text x="398" y="186" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12">2–1</text>',
        '<text x="450" y="207" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13" font-weight="bold">vòng tròn!</text>',
        '<text x="320" y="392" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">'
        'Mỗi cặp đều có đa số thắng, nhưng tập thể quay vòng —'
        ' không có người thắng chung cuộc.</text>',
    ]
    return svg_wrap("".join(parts), 640, 420,
                    "Ba cử tri với ba thứ tự ưu tiên tạo thành vòng tròn đa số "
                    "A thắng B, B thắng C, C thắng A")


def fig_tam_giac_quy_chieu() -> str:
    parts = [
        box2(200, 16, 160, 62, "Tư tưởng", "khái niệm \u201ccây\u201d", tsize=14),
        box2(24, 296, 160, 62, "Ký hiệu", 'chữ "cây"', tsize=14),
        box2(376, 296, 160, 62, "Vật", "cái cây thật", tsize=14),
        '<line x1="158" y1="296" x2="242" y2="78"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        '<line x1="402" y1="296" x2="318" y2="78"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        '<line x1="184" y1="327" x2="376" y2="327"'
        ' style="stroke:var(--oz-ink)" stroke-width="2" stroke-dasharray="8 6"/>',
        '<text x="160" y="190" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">tượng trưng</text>',
        '<text x="400" y="190" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">quy chiếu</text>',
        '<text x="280" y="356" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12.5">không có đường trực tiếp</text>',
    ]
    return svg_wrap("".join(parts), 560, 400,
                    "Tam giác Ogden và Richards: ký hiệu, tư tưởng, vật; "
                    "cạnh đáy đứt nét")


def fig_mary_room() -> str:
    parts = [
        '<line x1="320" y1="50" x2="320" y2="310"'
        ' style="stroke:var(--oz-ink)" stroke-width="1.5" stroke-dasharray="7 5"/>',
        '<text x="160" y="30" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">'
        'Trong phòng: chỉ đen – trắng</text>',
        '<text x="480" y="30" text-anchor="middle"'
        ' style="fill:currentColor" font-size="14" font-weight="bold">'
        'Bước ra ngoài: lần đầu thấy màu</text>',
        '<rect x="60" y="58" width="200" height="190" rx="10"'
        ' style="fill:var(--oz-paper);stroke:var(--oz-ink)" stroke-width="2"/>',
        '<line x1="78" y1="168" x2="242" y2="168"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        '<rect x="88" y="128" width="26" height="40"'
        ' style="fill:var(--oz-ink)" fill-opacity="0.55"/>',
        '<rect x="118" y="138" width="26" height="30"'
        ' style="fill:var(--oz-ink)" fill-opacity="0.35"/>',
        '<rect x="148" y="122" width="26" height="46"'
        ' style="fill:var(--oz-ink)" fill-opacity="0.7"/>',
        '<rect x="88" y="186" width="120" height="44" rx="6"'
        ' style="fill:var(--oz-ink);stroke:var(--oz-ink)"'
        ' stroke-width="2" fill-opacity="0.25"/>',
        '<text x="148" y="212" text-anchor="middle"'
        ' style="fill:currentColor" font-size="12">TV đen trắng</text>',
        '<circle cx="232" cy="112" r="11"'
        ' style="fill:var(--oz-ink)" fill-opacity="0.6"/>',
        '<rect x="223" y="125" width="18" height="36" rx="8"'
        ' style="fill:var(--oz-ink)" fill-opacity="0.6"/>',
        '<text x="160" y="278" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">biết HẾT vật lý về màu sắc</text>',
        '<text x="160" y="300" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">nhưng chưa từng thấy màu</text>',
        '<circle cx="480" cy="160" r="62"'
        ' style="fill:var(--oz-accent)" fill-opacity="0.35"/>',
        '<circle cx="430" cy="205" r="30"'
        ' style="fill:var(--oz-ok)" fill-opacity="0.35"/>',
        '<circle cx="535" cy="200" r="24"'
        ' style="fill:var(--oz-accent)" fill-opacity="0.55"/>',
        '<circle cx="490" cy="110" r="20"'
        ' style="fill:var(--oz-ok)" fill-opacity="0.5"/>',
        '<text x="480" y="278" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13" font-weight="bold">'
        'Cô ấy học được điều gì mới?</text>',
        '<text x="320" y="362" text-anchor="middle"'
        ' style="fill:currentColor" font-size="13">'
        'Jackson (1982): nếu Mary học được điều mới,'
        ' vật lý chưa nói hết mọi sự thật.</text>',
    ]
    return svg_wrap("".join(parts), 640, 400,
                    "Mary trong phòng đen trắng và Mary bước ra ngoài thấy màu sắc")


def _person(x, feet_y, fill="var(--oz-accent)"):
    """Hình người đơn giản: đầu tròn + thân chữ nhật bo."""
    return (
        f'<circle cx="{x}" cy="{r(feet_y - 35)}" r="9"'
        f' style="fill:{fill};stroke:var(--oz-ink)" stroke-width="2" fill-opacity="0.35"/>'
        f'<rect x="{x - 8}" y="{r(feet_y - 25)}" width="16" height="25" rx="8"'
        f' style="fill:{fill};stroke:var(--oz-ink)" stroke-width="2" fill-opacity="0.35"/>'
    )


def _polyline(pts, color="var(--oz-ink)", w=2, dashed=False):
    d = "M " + " L ".join(f"{r(x)},{r(y)}" for x, y in pts)
    dash = ' stroke-dasharray="7 5"' if dashed else ""
    return (f'<path d="{d}" fill="none" style="stroke:{color}"'
            f' stroke-width="{w}"{dash}/>')


def _t(text, x, y, size=13, anchor="middle", bold=False, color="currentColor"):
    b = ' font-weight="bold"' if bold else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}"'
            f' style="fill:{color}" font-size="{size}"{b}>{escape(text)}</text>')


# ---------------- 10 hình mới (đợt 3) ----------------

def fig_trolley() -> str:
    parts = [
        _t("Bài toán xe điện", 320, 30, 16, bold=True),
        box2(40, 58, 150, 66, "Cần gạt", "bẻ hay không bẻ?", tsize=14),
        _t("Không bẻ: xe đi thẳng → 5 người", 215, 80, 13, anchor="start"),
        _t("Bẻ ghi: xe rẽ nhánh → 1 người", 215, 102, 13, anchor="start"),
        # đường ray chính
        _polyline([(50, 330), (270, 330)], w=3),
        _polyline([(270, 330), (370, 210), (600, 210)], w=3),
        _polyline([(270, 330), (370, 430), (600, 430)], w=3),
        # xe điện
        '<rect x="60" y="294" width="90" height="34" rx="7"'
        ' style="fill:var(--oz-paper);stroke:var(--oz-ink)" stroke-width="2"/>'
        + _t("xe điện", 105, 317, 14),
        '<circle cx="85" cy="332" r="5"'
        ' style="fill:var(--oz-ink)" fill-opacity="0.6"/>'
        '<circle cx="125" cy="332" r="5"'
        ' style="fill:var(--oz-ink)" fill-opacity="0.6"/>',
        arrow(175, 312, 250, 312),
        # cần gạt nối xuống ngã rẽ
        poly_arrow([(115, 124), (115, 250), (256, 320)], dashed=True),
        # 5 người trên nhánh thẳng
        _t("5 người", 490, 152, 14, bold=True),
        "".join(_person(x, 210) for x in (400, 445, 490, 535, 580)),
        # 1 người trên nhánh rẽ
        _t("1 người", 490, 468, 14, bold=True),
        _person(490, 430),
    ]
    return svg_wrap("".join(parts), 640, 488,
                    "Xe điện lao tới ngã rẽ: đi thẳng thì cán năm người, "
                    "bẻ ghi thì rẽ sang nhánh có một người")


def fig_tam_giac_cai_ac() -> str:
    parts = [
        _t("Bộ ba bất tương thích", 280, 30, 15, bold=True),
        '<line x1="205" y1="120" x2="142" y2="266"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        '<line x1="355" y1="120" x2="418" y2="266"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        '<line x1="252" y1="301" x2="308" y2="301"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        box2(170, 52, 220, 66, "Thượng đế toàn năng", tsize=14),
        box2(32, 268, 220, 66, "Đau khổ tồn tại", tsize=14),
        box2(308, 268, 220, 66, "Thượng đế toàn thiện", tsize=14),
        '<rect x="160" y="168" width="240" height="64" rx="10"'
        ' style="fill:var(--oz-paper);stroke:var(--oz-ink)" stroke-width="1.5"/>'
        + _t("không thể cùng đúng?", 280, 195, 15, bold=True)
        + _t("ít nhất một mệnh đề phải xem lại", 280, 216, 12.5),
    ]
    return svg_wrap("".join(parts), 560, 356,
                    "Tam giác: Thượng đế toàn năng, Thượng đế toàn thiện, "
                    "đau khổ tồn tại — ba khẳng định không thể cùng đúng")


def fig_khe_uoc() -> str:
    parts = [
        _t("Lô-gíc của khế ước xã hội", 320, 32, 16, bold=True),
        box2(25, 92, 175, 88, "Trạng thái tự nhiên", "ai cũng chống ai",
             tsize=14),
        box2(232, 92, 175, 88, "Ký khế ước", "đồng thuận chung", tsize=14),
        box2(440, 92, 175, 88, "Nhà nước", "trật tự và luật lệ", tsize=14),
        arrow(200, 136, 232, 136),
        arrow(407, 136, 440, 136),
        _t("Hobbes, Locke, Rousseau: ba phiên bản của cùng một câu hỏi —", 320, 232, 13),
        _t("vì sao ta phải vâng lời, và chính quyền nào xứng đáng?", 320, 252, 13),
    ]
    return svg_wrap("".join(parts), 640, 280,
                    "Ba hộp nối bằng mũi tên: trạng thái tự nhiên, "
                    "ký khế ước, nhà nước")


def fig_cai_toi_chuoi() -> str:
    parts = [
        _t("Nghịch lý viên sĩ quan dũng cảm (Reid)", 320, 30, 15, bold=True),
        box2(25, 96, 175, 76, "Cậu bé", "bị đòn roi", tsize=14),
        box2(232, 96, 175, 76, "Sĩ quan trẻ", "nhớ chuyện bị đòn", tsize=14),
        box2(440, 96, 175, 76, "Tướng già", "nhớ thời sĩ quan", tsize=14),
        arrow(200, 134, 232, 134),
        arrow(407, 134, 440, 134),
        _t("nhớ", 216, 122, 12),
        _t("nhớ", 423, 122, 12),
        poly_arrow([(527, 172), (527, 262), (112, 262), (112, 172)],
                   dashed=True),
        _t("nhưng tướng già đã QUÊN chuyện bị đòn", 320, 288, 13, bold=True),
        _t("Theo Locke: A = B, B = C, mà A ≠ C — quan hệ “là cùng một", 320, 330, 13),
        _t("người” phải có tính bắc cầu, tiêu chí ký ức trực tiếp vi phạm nó.", 320, 350, 13),
    ]
    return svg_wrap("".join(parts), 640, 372,
                    "Chuỗi cậu bé, sĩ quan trẻ, tướng già: mũi tên nhớ nối tiếp "
                    "nhau, mũi tên đứt quên nối tướng già về cậu bé")


def fig_y_nghia_ba_ly_thuyet() -> str:
    parts = [
        _t("Ý nghĩa ở đâu? Ba hướng trả lời", 320, 30, 15, bold=True),
        box2(25, 76, 185, 100, "Siêu nhiên", "kế hoạch lớn hơn", tsize=14),
        box2(227, 76, 185, 100, "Chủ quan", "tự mình đặt ra", tsize=14),
        box2(430, 76, 185, 100, "Khách quan", "Wolf: điều đáng giá", tsize=14),
        _t("(tôn giáo)", 117, 164, 12),
        _t("(không cần trọng tài)", 319, 164, 12),
        _t("(dấn thân say mê)", 522, 164, 12),
        _t("Ba hướng không loại trừ nhau hoàn toàn —", 320, 224, 13),
        _t("một người có thể vừa thấy cái phi lý, vừa dấn thân theo Wolf.", 320, 246, 13),
    ]
    return svg_wrap("".join(parts), 640, 276,
                    "Ba hộp: siêu nhiên (kế hoạch lớn hơn), chủ quan "
                    "(tự mình đặt ra), khách quan (Wolf: dấn thân vào điều đáng giá)")


def fig_epicurus_chet() -> str:
    parts = [
        _t("Đối xứng sinh – tử (Epicurus, Lucretius)", 320, 30, 15, bold=True),
        _polyline([(130, 125), (320, 62), (510, 125)], dashed=True),
        _t("hai khoảng “không tồn tại” — có đối xứng không?", 320, 52, 13),
        _polyline([(70, 170), (570, 170)]),
        circle(170, 170, 7, "", "var(--oz-accent)"),
        circle(470, 170, 7, "", "var(--oz-accent)"),
        _t("sinh", 170, 198, 13),
        _t("chết", 470, 198, 13),
        _t("không tồn tại", 120, 142, 13),
        _t("ĐỜI SỐNG", 320, 142, 15, bold=True),
        _t("không tồn tại", 520, 142, 13),
        box(120, 222, 400, 62, "“Khi ta tồn tại, cái chết không có mặt”"),
        _t("— Epicurus, Thư gửi Menoeceus", 320, 310, 12.5),
    ]
    return svg_wrap("".join(parts), 640, 332,
                    "Trục thời gian: hai khoảng không tồn tại trước khi sinh "
                    "và sau khi chết đối xứng hai bên đời sống")


def fig_ai_kiem_soat() -> str:
    pts_ai = [(80, 288), (140, 282), (200, 270), (260, 250),
              (320, 220), (380, 180), (440, 130), (500, 70)]
    pts_ctrl = [(80, 288), (160, 278), (240, 268), (320, 260),
                (400, 254), (480, 250)]
    parts = [
        _t("Năng lực AI vs khả năng kiểm soát", 280, 30, 15, bold=True),
        '<line x1="70" y1="300" x2="512" y2="300"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        '<line x1="70" y1="300" x2="70" y2="52"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
        _t("thời gian →", 508, 322, 12.5, anchor="end"),
        _t("mức độ", 70, 40, 12.5),
        _polyline(pts_ai, color="var(--oz-accent)", w=3),
        _polyline(pts_ctrl, color="var(--oz-ok)", w=2.5, dashed=True),
        '<rect x="90" y="56" width="190" height="56" rx="8"'
        ' style="fill:var(--oz-paper);stroke:var(--oz-ink)" stroke-width="1.5"/>'
        '<line x1="102" y1="74" x2="132" y2="74"'
        ' style="stroke:var(--oz-accent)" stroke-width="3"/>'
        + _t("năng lực AI", 140, 78, 12.5, anchor="start")
        + '<line x1="102" y1="98" x2="132" y2="98"'
        ' style="stroke:var(--oz-ok)" stroke-width="2.5" stroke-dasharray="7 5"/>'
        + _t("khả năng kiểm soát", 140, 102, 12.5, anchor="start"),
        _t("Khoảng cách nới rộng theo thời gian —", 280, 342, 13),
        _t("lập luận cho nghiên cứu an toàn AI.", 280, 362, 13),
    ]
    return svg_wrap("".join(parts), 560, 384,
                    "Đồ thị hai đường: năng lực AI tăng dốc đứng, "
                    "khả năng kiểm soát tăng chậm, khoảng cách nới rộng")


def fig_ho_khai_niem() -> str:
    import math as _m
    cx, cy, ring, rad = 280, 215, 95, 78
    labels = ["hội họa", "âm nhạc", "văn học", "điện ảnh", "game / AI"]
    parts = [_t("Tương tự họ (Wittgenstein / Weitz)", 280, 30, 15, bold=True)]
    for i, lab in enumerate(labels):
        a = _m.radians(90 + i * 72)
        x, y = cx + ring * _m.cos(a), cy + ring * _m.sin(a)
        parts.append(circle(round(x), round(y), rad, lab, "var(--oz-accent)",
                              label_dy=5, fontsize=13))
    parts.append(_t("∅", 280, 224, 30, bold=True))
    parts.append(_t("Mỗi cặp kề nhau có điểm chung, nhưng không có", 280, 418, 13))
    parts.append(_t("một bản chất chung cho tất cả — đó là cách Weitz", 280, 438, 13))
    parts.append(_t("nhìn khái niệm “nghệ thuật”.", 280, 458, 13))
    return svg_wrap("".join(parts), 560, 478,
                    "Năm vòng tròn giao nhau từng cặp kề nhau nhưng không có "
                    "vùng chung cho cả năm")


def fig_vietnam_timeline() -> str:
    ticks = [90, 198, 306, 414, 522, 630]
    years = ["TK 13", "đầu TK 20", "1919", "1951", "1950–60", "1996"]
    labels = ["Trúc Lâm Yên Tử", "Phong trào Duy Tân", "Khoa cử cuối cùng",
              "Trần Đức Thảo", "Hiện sinh ở miền Nam", "Trần Đình Hượu"]
    parts = [
        _t("Triết học Việt Nam: một trục thời gian", 360, 30, 16, bold=True),
        '<line x1="90" y1="170" x2="630" y2="170"'
        ' style="stroke:var(--oz-ink)" stroke-width="2"/>',
    ]
    for i, x in enumerate(ticks):
        parts.append(
            f'<line x1="{x}" y1="158" x2="{x}" y2="182"'
            ' style="stroke:var(--oz-ink)" stroke-width="2"/>'
        )
        if i % 2 == 0:
            parts.append(_t(years[i], x, 118, 13, bold=True))
            parts.append(_t(labels[i], x, 140, 12.5))
        else:
            parts.append(_t(labels[i], x, 208, 12.5))
            parts.append(_t(years[i], x, 230, 13, bold=True))
    parts.append(_t("Từ thiền phái Trúc Lâm đến câu hỏi “đến hiện đại", 360, 282, 13))
    parts.append(_t("từ truyền thống” của Trần Đình Hượu.", 360, 302, 13))
    return svg_wrap("".join(parts), 720, 324,
                    "Trục thời gian: Trúc Lâm Yên Tử (thế kỷ 13), phong trào "
                    "Duy Tân (đầu thế kỷ 20), khoa cử cuối cùng (1919), "
                    "Trần Đức Thảo (1951), hiện sinh ở miền Nam, "
                    "Trần Đình Hượu (1996)")


def fig_hanh_phuc_may() -> str:
    parts = [
        _t("Cỗ máy trải nghiệm (Nozick, 1974)", 320, 30, 15, bold=True),
        box2(45, 66, 235, 104, "Cắm vào máy", "trải nghiệm hạnh phúc nhất",
             tsize=14),
        box2(360, 66, 235, 104, "Đời thực", "vui buồn lẫn lộn", tsize=14),
        _t("nhưng không thật", 162, 158, 12),
        _t("nhưng là thật", 477, 158, 12),
        _person(320, 310, fill="var(--oz-ink)"),
        _t("bạn", 320, 332, 13),
        arrow(292, 268, 190, 172),
        arrow(348, 268, 450, 172),
        _t(f"Bạn có bước vào không? {ppv('may-trai-nghiem-co-vao-khong', 'khong')}% triết gia được hỏi nói", 320, 366, 13),
        _t("KHÔNG (PhilPapers Survey 2020).", 320, 386, 13, bold=True),
    ]
    return svg_wrap("".join(parts), 640, 406,
                    "Một người đứng giữa hai lựa chọn: cắm vào máy để có mọi "
                    "trải nghiệm hạnh phúc (nhưng không thật) và sống đời thực "
                    "vui buồn lẫn lộn (nhưng là thật)")


def fig_duc_tri_phap_tri() -> str:
    parts = [
        '<text x="320" y="30" text-anchor="middle"'
        ' style="fill:currentColor" font-size="16" font-weight="bold">'
        'Đức trị vs Pháp trị: hai mô hình cai trị</text>',
        box2(20, 48, 290, 56, "ĐỨC TRỊ", "Khổng Tử – Mạnh Tử", tsize=14),
        box2(330, 48, 290, 56, "PHÁP TRỊ", "Hàn Phi", tsize=14),
    ]
    rows = [
        ("Con người: có thể cảm hóa", "Con người: xu lợi, tị hại"),
        ("Công cụ: đức, lễ, nêu gương", "Công cụ: pháp luật, thưởng–phạt"),
        ("Kẻ phạm lỗi: giáo hóa cho biết xấu hổ",
         "Kẻ phạm lỗi: trừng trị nghiêm để răn đe"),
        ("Luật: phụ trợ khi đức chưa đủ",
         "Luật: áp dụng đều, không thiên vị"),
        ("Điểm yếu: trông chờ minh quân",
         "Điểm yếu: luật thành công cụ của vua"),
    ]
    y = 116
    for left, right in rows:
        parts.append(
            f'<rect x="20" y="{y}" width="290" height="48" rx="8"'
            ' style="fill:var(--oz-paper);stroke:var(--oz-ink)"'
            ' stroke-width="1.5"/>'
            f'<rect x="330" y="{y}" width="290" height="48" rx="8"'
            ' style="fill:var(--oz-paper);stroke:var(--oz-ink)"'
            ' stroke-width="1.5"/>'
            f'<text x="165" y="{y + 29}" text-anchor="middle"'
            f' style="fill:currentColor" font-size="12.5">{left}</text>'
            f'<text x="475" y="{y + 29}" text-anchor="middle"'
            f' style="fill:currentColor" font-size="12.5">{right}</text>'
        )
        y += 56
    return svg_wrap("".join(parts), 640, y + 8,
                    "So sánh đức trị và pháp trị theo năm tiêu chí: "
                    "con người, công cụ, cách xử lý người phạm lỗi, "
                    "vai trò của luật, điểm yếu")


FIGURES = {
    "so-do-lap-luan": {
        "alt": "Sơ đồ lập luận: hai tiền đề và một giả định ngầm cùng hỗ trợ kết luận",
        "caption": "Mũi tên liền là hỗ trợ tường minh, mũi tên đứt là giả định ngầm.",
        "make": fig_so_do_lap_luan,
    },
    "dieu-kien-can-du": {
        "alt": "P là điều kiện đủ của Q (vòng P nằm trong vòng Q); P là điều kiện cần của Q (vòng Q nằm trong vòng P)",
        "caption": "Trái: P đủ cho Q (có P thì có Q). Phải: P cần cho Q (không P thì không Q).",
        "make": fig_dieu_kien_can_du,
    },
    "jtb-venn": {
        "alt": "Biểu đồ Venn ba vòng tròn: tin rằng p, p đúng, có lý do tốt. Giao của cả ba là JTB",
        "caption": "Ba vòng là ba điều kiện cần của định nghĩa JTB. Giao nhau của cả ba là ứng viên cho tri thức — nhưng các ví dụ Gettier cho thấy có trường hợp nằm ở giữa mà vẫn không phải tri thức.",
        "make": fig_jtb_venn,
    },
    "cay-tu-do-y-chi": {
        "alt": "Cây các lập trường: bất tương thích luận (tất định luận cứng, thuyết ý chí tự do), tương thích luận, hoài nghi về trách nhiệm",
        "caption": "Ba họ lập trường trong bài. Mũi tên đứt: hoài nghi về trách nhiệm đặt một câu hỏi khác, không trực tiếp trả lời câu hỏi tương thích.",
        "make": fig_cay_tu_do_y_chi,
    },
    "philpapers-dao-duc": {
        "alt": f"Biểu đồ cột: đạo đức học đức hạnh {ppv('dao-duc-hoc-chuan-tac', 'dao-duc-hoc-duc-hanh')}%, "
               f"nghĩa vụ luận {ppv('dao-duc-hoc-chuan-tac', 'nghia-vu-luan')}%, "
               f"hệ quả luận {ppv('dao-duc-hoc-chuan-tac', 'he-qua-luan')}%",
        "caption": "Tỉ lệ người chấp nhận hoặc nghiêng về (PhilPapers Survey 2020, Bourget & Chalmers 2023).",
        "make": fig_philpapers_dao_duc,
    },
    "philpapers-tu-do": {
        "alt": f"Biểu đồ cột: tương thích luận {ppv('tu-do-y-chi', 'tuong-thich-luan')}%, "
               f"thuyết ý chí tự do {ppv('tu-do-y-chi', 'thuyet-y-chi-tu-do-libertarianism')}%, "
               f"không có tự do ý chí {ppv('tu-do-y-chi', 'khong-co-tu-do-y-chi')}%",
        "caption": "Tỉ lệ người chấp nhận hoặc nghiêng về (PhilPapers Survey 2020, Bourget & Chalmers 2023).",
        "make": fig_philpapers_tu_do,
    },
    "philpapers-jtb": {
        "alt": f"Biểu đồ cột: JTB {ppv('phan-tich-khai-niem-tri-thuc', 'niem-tin-dung-duoc-bien-minh-jtb')}%, "
               f"một phân tích khác {ppv('phan-tich-khai-niem-tri-thuc', 'mot-phan-tich-khac')}%, "
               f"không có phân tích nào {ppv('phan-tich-khai-niem-tri-thuc', 'khong-co-phan-tich-nao')}%",
        "caption": f"Câu hỏi bổ sung, khoảng {ppn('phan-tich-khai-niem-tri-thuc')} người trả lời (PhilPapers Survey 2020).",
        "make": fig_philpapers_jtb,
    },
    "rawls-man-vo-tri": {
        "alt": "Người sau màn vô tri chọn giữa xã hội bình quân và xã hội chênh lệch nhưng người nghèo nhất khá hơn",
        "caption": "Sau màn vô tri, bạn không biết mình sẽ là ai — Rawls cho rằng ta sẽ chọn nguyên tắc maximin: ưu tiên cải thiện vị trí của người kém nhất.",
        "make": fig_rawls_man_vo_tri,
    },
    "pascal-wager": {
        "alt": "Ma trận 2×2: tin hay không tin × Chúa tồn tại hay không tồn tại, với kết quả mỗi ô",
        "caption": "Canh bạc của Pascal (Pensées, 1670): \"tin\" là lựa chọn khôn ngoan vì lợi vô hạn, hại hữu hạn. Đây là lập luận thực dụng, không phải bằng chứng cho sự tồn tại của Chúa.",
        "make": fig_pascal_wager,
    },
    "mctaggart-time": {
        "alt": "Chuỗi A với điểm hiện tại di chuyển; chuỗi B chỉ có quan hệ trước–sau, không có hiện tại đặc biệt",
        "caption": "McTaggart (1908): chuỗi B không có sự \"trôi\", chuỗi A thì mâu thuẫn — nên thời gian như ta hiểu không thật.",
        "make": fig_mctaggart_time,
    },
    "platon-hai-the-gioi": {
        "alt": "Thế giới Ý niệm với tam giác lý tưởng và thế giới cảm giác với hình vẽ tay méo mó, nối bằng quan hệ tham dự",
        "caption": "Theo Platon, vật cảm giác chỉ \"tham dự\" vào Ý niệm: tam giác vẽ tay không bao giờ hoàn hảo như Tam giác tự thân.",
        "make": fig_platon_hai_the_gioi,
    },
    "frankfurt-black": {
        "alt": "Hai nhánh — Jones tự quyết định hoặc Black can thiệp — cùng dẫn đến một kết quả",
        "caption": "Trường hợp Frankfurt: Jones chịu trách nhiệm dù ở nhánh 2 anh ta không thể làm khác — trách nhiệm gắn với diễn biến thực tế, không cần khả năng làm khác.",
        "make": fig_frankfurt_black,
    },
    "tuong-lai-phan-nhanh": {
        "alt": "Một đường thẳng duy nhất so với cây phân nhánh ba nhánh",
        "caption": "Tất định luận: tương lai là một đường duy nhất kéo dài từ hiện tại. Tương lai mở: hiện tại là điểm rẽ của nhiều nhánh khả dĩ.",
        "make": fig_tuong_lai_phan_nhanh,
    },
    "popper-kiem-chung": {
        "alt": "Vòng tròn bốn bước: giả thuyết, dự đoán, kiểm tra, bác bỏ hoặc tạm giữ",
        "caption": "Chu trình của Popper: khoa học tiến lên bằng cách đưa ra dự đoán mạo hiểm (có thể sai) rồi kiểm tra — lý thuyết sống sót chỉ được \"tạm giữ\", không bao giờ chứng minh xong.",
        "make": fig_popper_kiem_chung,
    },
    "condorcet": {
        "alt": "Ba cử tri với ba thứ tự ưu tiên tạo thành vòng tròn đa số: A thắng B, B thắng C, C thắng A",
        "caption": "Nghịch lý Condorcet: từng cặp đều có đa số thắng 2–1, nhưng tập thể quay vòng — \"ý chí chung\" không nhất quán.",
        "make": fig_condorcet,
    },
    "tam-giac-quy-chieu": {
        "alt": "Tam giác ký hiệu–tư tưởng–vật; cạnh đáy giữa ký hiệu và vật đứt nét",
        "caption": "Tam giác của Ogden & Richards (1923): chữ \"cây\" gợi lên khái niệm, khái niệm quy chiếu tới cái cây thật — nhưng chữ không trỏ thẳng vào vật (cạnh đáy đứt nét).",
        "make": fig_tam_giac_quy_chieu,
    },
    "mary-room": {
        "alt": "Mary trong phòng đen trắng với sách và TV xám; bên ngoài là những vệt màu",
        "caption": "Thí nghiệm của Jackson (1982): Mary biết hết vật lý về màu nhưng chưa từng thấy màu — khi thấy màu đỏ lần đầu, cô ấy có học được điều gì mới không?",
        "make": fig_mary_room,
    },
    "trolley": {
        "alt": "Xe điện lao tới ngã rẽ: đi thẳng thì cán năm người, bẻ ghi thì rẽ sang nhánh có một người",
        "caption": "Bài toán xe điện: không bẻ ghi thì năm người chết, bẻ ghi thì một người chết. Trực giác của bạn nói gì — và vì sao?",
        "make": fig_trolley,
    },
    "tam-giac-cai-ac": {
        "alt": "Tam giác: Thượng đế toàn năng, Thượng đế toàn thiện, đau khổ tồn tại — bộ ba bất tương thích",
        "caption": "Vấn đề sự dữ dưới dạng bộ ba của Mackie: ba khẳng định dường như không thể cùng đúng — ít nhất một trong ba phải được xem lại.",
        "make": fig_tam_giac_cai_ac,
    },
    "khe-uoc": {
        "alt": "Ba hộp nối bằng mũi tên: trạng thái tự nhiên, ký khế ước, nhà nước",
        "caption": "Lô-gíc chung của khế ước xã hội: từ trạng thái tự nhiên, qua hành vi ký kết, đến nhà nước. Hobbes, Locke, Rousseau chỉ khác nhau ở nội dung mỗi hộp.",
        "make": fig_khe_uoc,
    },
    "cai-toi-chuoi": {
        "alt": "Chuỗi cậu bé, sĩ quan trẻ, tướng già: mũi tên nhớ nối tiếp nhau, mũi tên đứt quên nối tướng già về cậu bé",
        "caption": "Phản ví dụ của Reid: tướng già nhớ thời sĩ quan, sĩ quan nhớ thời cậu bé, nhưng tướng già quên chuyện cậu bé bị đòn — quan hệ \"là cùng một người\" mất tính bắc cầu.",
        "make": fig_cai_toi_chuoi,
    },
    "y-nghia-ba-ly-thuyet": {
        "alt": "Ba hộp: siêu nhiên (kế hoạch lớn hơn), chủ quan (tự mình đặt ra), khách quan (Wolf: dấn thân vào điều đáng giá)",
        "caption": "Ba hướng trả lời câu hỏi ý nghĩa: tìm ở kế hoạch lớn hơn, tự đặt ra, hay dấn thân vào điều đáng giá. Cả ba đều tôn trọng câu hỏi — chỉ khác đáp án.",
        "make": fig_y_nghia_ba_ly_thuyet,
    },
    "epicurus-chet": {
        "alt": "Trục thời gian: hai khoảng không tồn tại trước khi sinh và sau khi chết đối xứng hai bên đời sống",
        "caption": "Lập luận đối xứng của Lucretius: nếu khoảng không-tồn-tại trước khi sinh không đáng sợ, thì vì sao khoảng sau khi chết lại đáng sợ?",
        "make": fig_epicurus_chet,
    },
    "ai-kiem-soat": {
        "alt": "Đồ thị hai đường: năng lực AI tăng dốc đứng, khả năng kiểm soát tăng chậm, khoảng cách nới rộng",
        "caption": "Nỗi lo của Bostrom và trường phái an toàn AI: đường năng lực dốc hơn đường kiểm soát — và khoảng cách giữa hai đường chính là rủi ro.",
        "make": fig_ai_kiem_soat,
    },
    "ho-khai-niem": {
        "alt": "Năm vòng tròn giao nhau từng cặp kề nhau nhưng không có vùng chung cho cả năm",
        "caption": "Tương tự họ: hội họa, âm nhạc, văn học, điện ảnh, game/AI — mỗi cặp kề nhau có điểm chung, nhưng không có một bản chất chung cho tất cả. Đó là cách Weitz nhìn khái niệm \"nghệ thuật\".",
        "make": fig_ho_khai_niem,
    },
    "vietnam-timeline": {
        "alt": "Trục thời gian: Trúc Lâm Yên Tử (thế kỷ 13), phong trào Duy Tân (đầu thế kỷ 20), khoa cử cuối cùng (1919), Trần Đức Thảo (1951), hiện sinh ở miền Nam (1950–60), Trần Đình Hượu (1996)",
        "caption": "Sáu mốc của triết học Việt Nam trên một trục — từ thiền phái Trúc Lâm đến câu hỏi \"đến hiện đại từ truyền thống\" của Trần Đình Hượu.",
        "make": fig_vietnam_timeline,
    },
    "hanh-phuc-may": {
        "alt": "Một người đứng giữa hai lựa chọn: cắm vào máy để có mọi trải nghiệm hạnh phúc (nhưng không thật) và sống đời thực vui buồn lẫn lộn (nhưng là thật)",
        "caption": "Thí nghiệm của Nozick (1974): bạn có đánh đổi đời thực để lấy một đời hạnh phúc giả lập không? Khảo sát PhilPapers 2020: "
                   f"{ppv('may-trai-nghiem-co-vao-khong', 'khong')}% triết gia nói không.",
        "make": fig_hanh_phuc_may,
    },
    "duc-tri-phap-tri": {
        "alt": "So sánh đức trị và pháp trị theo năm tiêu chí: con người (cảm hóa được / xu lợi tị hại), công cụ (đức lễ nêu gương / pháp luật thưởng phạt), kẻ phạm lỗi (giáo hóa / trừng trị răn đe), vai trò của luật (phụ trợ / áp dụng đều), điểm yếu (trông chờ minh quân / luật thành công cụ của vua)",
        "caption": "Năm điểm khác biệt cốt lõi giữa đức trị (Khổng – Mạnh) và pháp trị (Hàn Phi).",
        "make": fig_duc_tri_phap_tri,
    },
}


def render_block(name: str) -> str:
    meta = FIGURES[name]
    svg = meta["make"]()
    return (
        f"<!-- fig:{name} -->\n"
        f'<figure class="oz-fig">\n{svg}\n'
        f"<figcaption>{escape(meta['caption'])}</figcaption>\n"
        f"</figure>\n"
        f"<!-- /fig:{name} -->"
    )


def svg_filename(name: str) -> Path:
    return IMG_DIR / f"fig-{name}.svg"


def process_markdown(text: str) -> str:
    def repl(m: re.Match) -> str:
        name = m.group(1)
        if name not in FIGURES:
            raise SystemExit(f"Hình chưa định nghĩa: {name}")
        return render_block(name)

    # Cả cặp dấu trống lẫn khối đã điền: khối đã điền được sinh lại, nên --check bắt cả hình cũ (số, alt, chú thích
    # đổi theo kho mà trang chưa sinh lại; đợt 5.2).
    pattern = re.compile(r"<!-- fig:([a-z0-9-]+) -->.*?<!-- /fig:\1 -->", re.S)
    return pattern.sub(repl, text)


def main(argv: list[str]) -> int:
    check = "--check" in argv
    errors = []

    # 1. File SVG rời cho từng hình.
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for name, meta in FIGURES.items():
        svg_doc = (
            '<?xml version="1.0" encoding="UTF-8"?>\n' + meta["make"]() + "\n"
        )
        target = svg_filename(name)
        if check:
            if not target.exists() or target.read_text(encoding="utf-8") != svg_doc:
                errors.append(f"{target.relative_to(ROOT)} lệch mã nguồn — chạy: python tools/figures.py")
        else:
            target.write_text(svg_doc, encoding="utf-8")

    # 2. Điền dấu trong các trang.
    for page in sorted(DOCS.rglob("*.md")):
        current = page.read_text(encoding="utf-8")
        try:
            new = process_markdown(current)
        except SystemExit as e:
            print(str(e), file=sys.stderr)
            return 1
        if new != current:
            if check:
                errors.append(f"{page.relative_to(ROOT)} có hình chưa điền hoặc đã cũ — chạy: python tools/figures.py")
            else:
                page.write_text(new, encoding="utf-8")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if check:
        print(f"Hình khớp mã nguồn ({len(FIGURES)} hình).")
    else:
        print(f"Đã sinh {len(FIGURES)} hình.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
