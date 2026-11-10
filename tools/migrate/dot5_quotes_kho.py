"""Ghi kết quả kiểm chứng đợt con 5.2 vào kho trích dẫn: `locator`, `work_note` trong data/kb/quotes.yml và tên tác
phẩm in nghiêng trong tiêu đề khối (ban-giao/dot-5.md 5.2: `lint_quotes` = 0 trong Lõi, `verification/lech/quotes.md`
hết mục mở).

    python tools/migrate/dot5_quotes_kho.py --dry-run
    python tools/migrate/dot5_quotes_kho.py
    python tools/kb_quotes.py            # rút lại: giữ locator, work_note; work ghép theo tiêu đề mới

- `LOCATOR`: vị trí trích, lấy từ claim vị trí đã kiểm trong `verification/evidence/quotes__<khóa>.json` (claim
  `dung`, hoặc claim `sai` mức nhẹ có `fix`), viết gọn. Chín bản ghi không có claim vị trí (ghi chú "không có claim
  vị trí"): lấy từ tiêu đề hoặc claim tác giả/tác phẩm/nguyên văn đã kiểm. Chỉ đọc bằng chứng, không sửa.
- `WORK_NOTE`: lý do khối không ghép với tác phẩm nào trong works.yml (works.yml đóng băng từ 5.1, không thêm tác phẩm).
- `IN_NGHIENG`: trang Văn bản gốc có tiêu đề khối bắt đầu bằng tên một tác phẩm đã có trong works.yml (hoặc trong
  `kb_quotes.TEN_KHAC`) mà chưa in nghiêng: đặt tên đó trong `*…*`, như `doc/luan-ngu.md` ("*Luận ngữ*, thiên…").
  Khóa `trich.*` không đổi vì slug bỏ dấu `*`; thân khối không đổi.
Chạy lại không đổi gì. Khóa trong bảng mà không còn trong quotes.yml (hoặc ngược lại) thì dừng.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import kb_quotes  # noqa: E402

LOCATOR = {
    "alan-turing-computing-ma.mind": "§1 “The Imitation Game”, tr. 433",
    "anselm.proslogion": "chương 2",
    "anselm.proslogion-2": "chương 1",
    "aristotle.dao-duc-nicomachus": "III.1, 1109b30–35",
    "aristotle.dao-duc-nicomachus-2": "I.7, 1098a18–20",
    "augustine.confessions": "XI.14.17",
    "augustine.tu-thu": "I.1.1",
    "bentham.an-introduction-to-the-principles-of-mor": "chương I, đoạn 1",
    "bertrand-russell.the-problems-of-philosophy": "chương XII",
    "bertrand-russell.the-problems-of-philosophy-2": "chương VI",
    "blaise-pascal.pensees": "Brunschvicg 347, Lafuma 200",
    "boethius.an-ui-cua-triet-hoc": "quyển V, văn xuôi 3–6",
    "chu-hy.chu-tu-ngu-loai": "quyển 94",
    "chu-van-an.trich": "Bản kỷ quyển 7, năm Canh Tuất (1370)",
    "clive-bell.art": "chương I (The Aesthetic Hypothesis)",
    "david-hume.a-treatise-of-human-nature": "T 3.1.1.27 (SBN 469–70)",
    "david-hume.an-enquiry-concerning-human-understandin": "EHU 10.13 (SBN 115–6)",
    "democritus.trich": "Diogenes Laërtius IX.72",
    "descartes.suy-niem-ve-triet-hoc-de-nhat": "Suy niệm I",
    "descartes.suy-niem-ve-triet-hoc-de-nhat-2": "Suy niệm VI, đoạn 9",
    "diogenes-laertius.lives-of-the-eminent-philosophers": "VII.87",
    "duc-phat.trich": "SN 22.59:2.1–2.3",
    "edmund-husserl.logische-untersuchungen": "tập II, Dẫn nhập, §2 (tr. 7 bản 1901)",
    "epictetus.cam-nang": "§5",
    "epicurus.nhung-cham-ngon-chu-yeu": "câu 2 (Diogenes Laërtius X.139)",
    "epicurus.thu-gui-menoeceus": "§125 (Diogenes Laërtius X.125)",
    "friedrich-nietzsche.die-frohliche-wissenschaft": "§125",
    "gottlob-frege-uber-sinn.zeitschrift-fur-philosophie-und-philosop": "tr. 26–27",
    "han-phi.han-phi-tu": "thiên 6 Hữu độ",
    "hegel.grundlinien-der-philosophie-des-rechts": "Lời tựa, tr. xxx (bản Dyde 1896)",
    "heraclitus-manh-van-dk-2.early-greek-philosophy": "DK 22 B30 (Burnet, mảnh 20)",
    "herodotus.historiai": "I.74",
    "hume.an-enquiry-concerning-human-understandin": "EHU 8.23 (SBN 95)",
    "hume.an-enquiry-concerning-human-understandin-2": "EHU 4.2 và 4.4",
    "hume.an-enquiry-concerning-human-understandin-3": "EHU 4.21",
    "hume.an-enquiry-concerning-human-understandin-4": "EHU 5.6",
    "hume.an-enquiry-concerning-human-understandin-5": "EHU 7.6 và 7.28",
    "hume.an-enquiry-concerning-human-understandin-6": "EHU 5.6",
    "immanuel-kant.uber-ein-vermeintes-recht-aus-menschenli": "Ak 8:426, dòng 14–24",
    "j-s-mill.on-liberty": "chương I",
    "jeremy-bentham.an-introduction-to-the-principles-of-mor": "chương XVII, §1, đoạn IV, chú thích",
    "john-locke.khao-luan-ve-hieu-biet-cua-con-nguoi": "II.i.2",
    "john-locke.two-treatises-of-government": "khảo luận thứ hai, chương V, §27",
    "john-stuart-mill.utilitarianism": "chương II",
    "john-stuart-mill.utilitarianism-2": "chương II",
    "kant.beantwortung-der-frage-was-ist-aufklarun": "Ak 8:35, từ dòng 1",
    "kant.beantwortung-der-frage-was-ist-aufklarun-2": "Ak 8:35, dòng 9–16",
    "kant.beantwortung-der-frage-was-ist-aufklarun-3": "Ak 8:36–37",
    "kant.beantwortung-der-frage-was-ist-aufklarun-4": "Ak 8:36 và 8:37",
    "kant.grundlegung-zur-metaphysik-der-sitten": "Ak 4:429, dòng 10–12",
    "khong-tu.luan-ngu": "15.24",
    "kierkegaard-but-danh-joh.fear-and-trembling": "phần “Preliminary Expectoration”",
    "lao-tu.trich": "chương 64",
    "leibniz.don-tu-luan": "§32",
    "locke.an-essay-concerning-human-understanding": "II.xxvii.9",
    "ludwig-wittgenstein.tractatus-logico-philosophicus": "6.54",
    "mac-tu.trich": "thiên 15 Kiêm ái trung",
    "maimonides.chi-dan-cho-nguoi-hoang-mang": "phần I, chương 60",
    "manh-tu.manh-tu": "3B2",
    "marcus-aurelius.suy-tuong": "II.1",
    "marx.trich": "luận cương 11",
    "mill.on-liberty": "chương II, đoạn 1",
    "mill.on-liberty-2": "chương II, đoạn 2, 3 và 6",
    "mill.on-liberty-3": "chương II, đoạn 21 và 23",
    "mill.on-liberty-4": "chương II, đoạn 34",
    "mill.on-liberty-5": "chương I, đoạn 9",
    "nagarjuna.trung-luan": "24.14",
    "nguyen-trai-loi-tau-khi.dai-viet-su-ky-toan-thu": "Bản kỷ quyển 11",
    "nguyen-trai.binh-ngo-dai-cao": "đoạn mở đầu",
    "platon.bien-ho-cua-socrates": "38a",
    "platon.cong-hoa": "VI, 488e–489a",
    "platon.cong-hoa-2": "X, 596a",
    "platon.phaedo": "100c–d",
    "rene-descartes.luan-ve-phuong-phap": "phần IV",
    "rousseau.du-contrat-social": "quyển I, chương 1",              # không có claim vị trí: claim "Quyển I, chương 1"
    "russell.the-problems-of-philosophy": "chương XV, đoạn 3",
    "russell.the-problems-of-philosophy-2": "chương XV, đoạn 4",
    "russell.the-problems-of-philosophy-3": "chương XV, đoạn 7",
    "russell.the-problems-of-philosophy-4": "chương XV, đoạn 9 và 12",
    "sartre.l-existentialisme-est-un-humanisme": "phần “bị bỏ rơi”",  # không có claim vị trí: claim phần "bị bỏ rơi"
    "simone-de-beauvoir.le-deuxieme-sexe": "tập II, phần một, chương 1, câu mở đầu",
    "spinoza.dao-duc-hoc": "phần I, phụ lục",
    "thomas-aquinas.tong-luan-than-hoc": "I, q. 1, a. 8, ad 2",
    "thomas-hobbes.leviathan": "chương 13",                          # không có claim vị trí: claim tác phẩm, chương 13
    "thomas-hobbes.leviathan-2": "chương 13",                        # không có claim vị trí: claim tác phẩm, chương 13
    "tran-nhan-tong.cu-tran-lac-dao-phu": "hội thứ năm; bài kệ kết",  # không có claim vị trí: claim nguyên văn
    "tran-nhan-tong.cu-tran-lac-dao-phu-2": "hội thứ năm",           # không có claim vị trí: claim phiên âm
    "trang-tu.trang-tu": "thiên 4 Nhân gian thế, đoạn kết",
    "trich.bien-ho-21d": "21d",
    "trich.bien-ho-29ab": "29a–b",
    "trich.bien-ho-38a": "38a",
    "trich.bien-ho-40c": "40c",
    "trich.binh-ngo-dai-cao-cau-mo-dau-theo-toan-thu": "Toàn thư, Bản kỷ thực lục quyển 10; câu mở đầu",
    "trich.binh-ngo-dai-cao-theo-toan-thu": "Toàn thư, Bản kỷ thực lục quyển 10; đoạn Đại Việt văn hiến",
    "trich.binh-ngo-dai-cao-theo-toan-thu-2": "Toàn thư, Bản kỷ thực lục quyển 10; đoạn tội ác giặc Minh",
    "trich.binh-ngo-dai-cao-theo-toan-thu-3": "Toàn thư, Bản kỷ thực lục quyển 10; ba câu cách xa nhau",
    "trich.cam-nang-1": "§1",
    "trich.cam-nang-3": "§3",
    "trich.cam-nang-48": "§48",
    "trich.cam-nang-5": "§5",
    "trich.cam-nang-8": "§8",
    "trich.cong-hoa-515a-va-515c": "VII, 515a và 515c",
    "trich.cong-hoa-516b": "VII, 516b",
    "trich.cong-hoa-517a": "VII, 517a",
    "trich.cong-hoa-518bc-va-520c": "VII, 518b–c và 520c",
    "trich.dao-duc-kinh-chuong-1": "chương 1",
    "trich.dao-duc-kinh-chuong-11": "chương 11",
    "trich.dao-duc-kinh-chuong-2": "chương 2",
    "trich.dao-duc-kinh-chuong-44": "chương 44",
    "trich.dao-duc-kinh-chuong-8-va-78": "chương 8 và 78",
    "trich.dao-duc-nicomachus-i-2-1094a1822": "I.2, 1094a18–22",
    "trich.dao-duc-nicomachus-i-7-1098a1620": "I.7, 1098a16–20",
    "trich.dao-duc-nicomachus-ii-4-1105a3034": "II.4, 1105a30–34",
    "trich.dao-duc-nicomachus-ii-6-1106b361107a2": "II.6, 1106b36–1107a2",
    "trich.david-hume-of-the-standard-of-taste-1757": "đoạn 7 (bản Miller, tr. 226–7)",
    "trich.luan-ngu-thien-bat-dat-3-4": "3.4",
    "trich.luan-ngu-thien-hoc-nhi-1-1": "1.1",
    "trich.luan-ngu-thien-ly-nhan-4-16-va-thien-ve-linh-cong-15-21": "4.16 và 15.21",
    "trich.luan-ngu-thien-ung-da-6-11": "6.11",
    "trich.luan-ngu-thien-ve-linh-cong-15-24": "15.24",
    "trich.luan-ngu-thien-vi-chinh-2-17": "2.17",
    "trich.mac-tu-thien-14-kiem-ai-thuong": "thiên 14 Kiêm ái thượng",
    "trich.mac-tu-thien-16-kiem-ai-ha": "thiên 16 Kiêm ái hạ",
    "trich.mac-tu-thien-17-phi-cong-thuong": "thiên 17 Phi công thượng",
    "trich.mac-tu-thien-26-thien-chi-thuong": "thiên 26 Thiên chí thượng",
    "trich.man-giac-cao-tat-thi-chung-co-benh-bao-moi-nguoi": "trọn bài (sáu câu)",   # claim: "không có (bài thơ…)"
    "trich.manh-tu-2a2-thien-cong-ton-suu-thuong": "2A2",
    "trich.manh-tu-2a6-thien-cong-ton-suu-thuong": "2A6",
    "trich.manh-tu-6a2-thien-cao-tu-thuong": "6A2",
    "trich.manh-tu-6a8-thien-cao-tu-thuong": "6A8",
    "trich.suy-niem-i-12-at-7-22": "AT VII 22",
    "trich.suy-niem-i-3-at-7-18": "AT VII 18",
    "trich.suy-niem-i-5-va-8-at-7-1920": "AT VII 19–20",
    "trich.suy-niem-ii-11-va-16-at-7-30-34": "AT VII 30, 34",
    "trich.suy-niem-ii-3-at-7-25": "AT VII 25",
    "trich.suy-tuong-ii-1": "II.1",
    "trich.suy-tuong-ii-11-va-iv-48": "II.11 và IV.48",
    "trich.suy-tuong-ix-30": "IX.30",
    "trich.suy-tuong-viii-47": "VIII.47",
    "trich.suy-tuong-x-28": "X.28",
    "trich.tam-kinh-t251": "T251, đoạn “Xá Lợi Tử! Sắc bất dị không”",
    "trich.tam-kinh-t251-2": "T251, đoạn “Thị chư pháp không tướng”",
    "trich.tam-kinh-t251-cau-mo-dau": "T251, câu mở đầu",
    "trich.tam-kinh-t251-doan-ket": "T251, đoạn kết",
    "trich.tran-nhan-tong-ke-cu-tran-lac-dao-ban-dich-nghia-cua-logos": "bài kệ kết",
    "trich.tran-nhan-tong-xuan-hieu-sang-xuan": "trọn bài (bốn câu)",  # không có claim vị trí: claim nguyên văn bốn câu
    "trich.trang-tu-te-vat-luan": "Tề vật luận, ctext mục 12",
    "trich.trang-tu-te-vat-luan-cau-ket": "Tề vật luận, câu cuối (ctext mục 14)",
    "trich.trang-tu-te-vat-luan-doan-ket": "Tề vật luận, đoạn kết (ctext mục 14)",
    "trich.tuyen-ngon-quoc-te-nhan-quyen-1948-dieu-13": "Điều 13, khoản 1",
    "trich.van-hanh-thi-de-tu-bao-de-tu": "trọn bài (bốn câu)",       # không có claim vị trí: claim nguyên văn dòng 1–4
    "trich.winston-churchill-phat-bieu-tai-ha-vien-anh-11-11-1947": "HC Deb 11/11/1947, tập 444, cột 206–207",
    "tuan-tu.tuan-tu": "thiên 23 Tính ác",
    "tuan-tu.tuan-tu-2": "thiên 1 Khuyến học, đoạn mở đầu",
    "tue-trung-thuong-si.pham-thanh-bat-di": "hai câu, dẫn theo Nguyễn Huệ Chi (2014), tr. 188",  # không có claim vị trí
}

CHUA_CO = "tác phẩm chưa có bản ghi (đợt 7)"
WORK_NOTE = {
    "alan-turing-computing-ma.mind": f"bài báo trên tạp chí Mind; {CHUA_CO}",
    "boethius.an-ui-cua-triet-hoc": CHUA_CO,
    "chu-van-an.trich": f"đoạn chính sử trong Đại Việt sử ký toàn thư; {CHUA_CO}",
    "clive-bell.art": CHUA_CO,
    "democritus.trich": f"lời Democritus do Diogenes Laërtius dẫn; {CHUA_CO}",
    "diogenes-laertius.lives-of-the-eminent-philosophers": CHUA_CO,
    "gottlob-frege-uber-sinn.zeitschrift-fur-philosophie-und-philosop": f"bài báo trên tạp chí; {CHUA_CO}",
    "heraclitus-manh-van-dk-2.early-greek-philosophy": "mảnh văn DK 22 B30; chưa có nguồn gán vào tác phẩm nào trong kho",
    "nguyen-trai-loi-tau-khi.dai-viet-su-ky-toan-thu": f"lời tâu chép trong Đại Việt sử ký toàn thư; {CHUA_CO}",
    "trich.david-hume-of-the-standard-of-taste-1757": f"tiểu luận; {CHUA_CO}",
    "trich.man-giac-cao-tat-thi-chung-co-benh-bao-moi-nguoi": f"bài kệ lẻ trong Thiền uyển tập anh; {CHUA_CO}",
    "trich.tam-kinh-t251": f"kinh Phật (T251, Huyền Trang dịch); {CHUA_CO}",
    "trich.tam-kinh-t251-2": f"kinh Phật (T251, Huyền Trang dịch); {CHUA_CO}",
    "trich.tam-kinh-t251-cau-mo-dau": f"kinh Phật (T251, Huyền Trang dịch); {CHUA_CO}",
    "trich.tam-kinh-t251-doan-ket": f"kinh Phật (T251, Huyền Trang dịch); {CHUA_CO}",
    "trich.tran-nhan-tong-xuan-hieu-sang-xuan": f"bài thơ lẻ; {CHUA_CO}",
    "trich.tuyen-ngon-quoc-te-nhan-quyen-1948-dieu-13": "văn kiện LHQ, không phải tác phẩm",
    "trich.van-hanh-thi-de-tu-bao-de-tu": f"bài kệ lẻ trong Thiền uyển tập anh; {CHUA_CO}",
    "trich.winston-churchill-phat-bieu-tai-ha-vien-anh-11-11-1947": "phát biểu tại Hạ viện Anh, không phải tác phẩm",
}

# Trang → tên tác phẩm đứng đầu tiêu đề khối (mọi khối quote của trang đều bắt đầu bằng tên này).
IN_NGHIENG = {
    "docs/doc/platon-bien-ho.md": "Biện hộ",
    "docs/doc/platon-hang-dong.md": "Cộng hòa",
    "docs/doc/epictetus-cam-nang.md": "Cẩm nang",
    "docs/doc/descartes-suy-niem.md": "Suy niệm",
    "docs/doc/dao-duc-kinh.md": "Đạo đức kinh",
    "docs/doc/trang-tu-mong-ho-diep.md": "Trang Tử",
    "docs/doc/aristotle-dao-duc.md": "Đạo đức Nicomachus",
    "docs/doc/aurelius-suy-tuong.md": "Suy tưởng",
    "docs/doc/manh-tu-tinh-thien.md": "Mạnh Tử",
    "docs/doc/mac-tu-kiem-ai.md": "Mặc Tử",
    "docs/doc/nguyen-trai-binh-ngo.md": "Bình Ngô đại cáo",
}


def in_nghieng(text: str, name: str) -> tuple[str, int]:
    """Đặt `name` đứng đầu tiêu đề khối quote vào `*…*`; trả (văn bản mới, số tiêu đề đổi)."""
    pat = re.compile(r'^(?P<pre>[ \t]*(?:!!!|\?\?\?\+?)[ \t]+quote[ \t]+")' + re.escape(name) + r'(?=[ ,(])', re.M)
    return pat.subn(lambda m: f"{m.group('pre')}*{name}*", text)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="chỉ in, không ghi")
    a = ap.parse_args(argv)
    out = ROOT / "data" / "kb" / "quotes.yml"
    recs = yaml.safe_load(out.read_text(encoding="utf-8"))
    if set(LOCATOR) != set(recs) or not set(WORK_NOTE) <= set(recs):
        print("Bảng không khớp khóa của quotes.yml:", sorted(set(LOCATOR) ^ set(recs)),
              sorted(set(WORK_NOTE) - set(recs)), file=sys.stderr)
        return 1
    n_title = 0
    for rel, name in IN_NGHIENG.items():
        f = ROOT / rel
        text, n = in_nghieng(f.read_text(encoding="utf-8"), name)
        n_title += n
        if n:
            print(f"{rel}: {n} tiêu đề — *{name}*")
            if not a.dry_run:
                f.write_text(text, encoding="utf-8")
    n_loc = n_note = 0
    for key, r in recs.items():
        if r.get("locator") != LOCATOR[key]:
            r["locator"] = LOCATOR[key]
            n_loc += 1
        if key in WORK_NOTE and r.get("work_note") != WORK_NOTE[key]:
            r["work_note"] = WORK_NOTE[key]
            n_note += 1
    print(f"{n_title} tiêu đề in nghiêng tên tác phẩm; {n_loc} locator; {n_note} work_note.")
    if not a.dry_run:
        out.write_text(kb_quotes.render(recs), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
