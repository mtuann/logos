"""Ghi kết quả kiểm chứng đợt con 5.1 vào data/kb/works.yml (trường sửa tay, tool kb_works.py giữ khi rút lại).

    python tools/migrate/dot5_works_kho.py --dry-run
    python tools/migrate/dot5_works_kho.py

Mỗi giá trị dưới đây lấy từ file bằng chứng `verification/evidence/works__<khóa>.json` (claims và notes của agent
kiểm), đã duyệt tay; bảng việc: verification/viec-sua/5.1.md. Quy ước năm: quyết định 28 (KE-HOACH.md).

- `same_as`: bản ghi là tên khác (tiếng Việt, tiếng Anh) của một tác phẩm đã có; năm và tác giả theo bản ghi đích.
- `attribution`: tác giả theo nguồn, cho tác phẩm chưa có hồ sơ tác giả, hoặc ghi chú tác giả (đồng tác giả, người
  biên tập, quy cho theo truyền thống).
- `year_fixed`: năm đã chốt (năm công bố lần đầu; tác phẩm cổ/di cảo chưa rõ năm in: năm soạn). `year` = giá trị này.
- `years_ok`: năm khác hợp lệ mà văn xuôi được phép ghi khi nói rõ (năm soạn, bản in sách, bản dịch).
- `year_note`: giải thích.
Chạy lại không đổi gì. Khóa không còn trong works.yml thì dừng.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import kb_works  # noqa: E402

SAME_AS = {
    "chua-ro.ban-ve-tu-do": "mill.on-liberty",
    "chua-ro.ben-kia-thien-va-ac": "nietzsche.jenseits-von-gut-und-bose",
    "chua-ro.beyond-good-and-evil": "nietzsche.jenseits-von-gut-und-bose",
    "chua-ro.cac-nguyen-ly-cua-triet-hoc": "descartes.principia-philosophiae",
    "chua-ro.cac-nguyen-ly-triet-hoc": "descartes.principia-philosophiae",
    "chua-ro.cac-nguyen-ly-triet-hoc-cua-descartes": "spinoza.renati-des-cartes-principiorum-philosophiae-pars-i",
    "chua-ro.city-of-god": "augustine.de-civitate-dei",
    "chua-ro.con-nguoi-qua-doi-con-nguoi": "nietzsche.menschliches-allzumenschliches",
    "chua-ro.confessions": "augustine.confessiones",
    "chua-ro.cong-hoa": "platon.politeia",
    "chua-ro.critique-of-pure-reason": "kant.kritik-der-reinen-vernunft",
    "chua-ro.discourse-on-the-method": "descartes.discours-de-la-methode",
    "chua-ro.doan-ban-ve-chinh-quyen": "bentham.a-fragment-on-government",
    "chua-ro.eichmann-in-jerusalem": "arendt.eichmann-in-jerusalem-a-report-on-the-banality-of",
    "chua-ro.either-or": "kierkegaard.enteneller",
    "chua-ro.ethics": "spinoza.ethica-ordine-geometrico-demonstrata",
    "chua-ro.fear-and-trembling": "kierkegaard.frygt-og-bven",
    "chua-ro.hien-tuong-hoc-tinh-than": "hegel.phanomenologie-des-geistes",
    "chua-ro.hien-tuong-luan-va-duy-vat-bien-chung": "tran-duc-thao.phenomenologie-et-materialisme-dialectique",
    "chua-ro.khao-cuu-logic": "husserl.logische-untersuchungen",
    "chua-ro.khao-cuu-triet-hoc": "wittgenstein.philosophische-untersuchungen",
    "chua-ro.khao-luan-ve-ban-tinh-con-nguoi": "hume.a-treatise-of-human-nature",
    "chua-ro.khoa-hoc-vui": "nietzsche.die-frohliche-wissenschaft",
    "chua-ro.khung-hoang-cua-cac-khoa-hoc-chau-au": "husserl.die-krisis-der-europaischen-wissenschaften",
    "chua-ro.lao-tu": "lao-tu.lao-tu",
    "chua-ro.lich-su-triet-hoc-phuong-tay": "russell.a-history-of-western-philosophy",
    "chua-ro.luan-van-than-hocchinh-tri": "spinoza.tractatus-theologico-politicus",
    "chua-ro.luan-ve-nguon-goc-cua-bat-binh-dang": "rousseau.discours-sur-lorigine-et-les-fondements-de-linegal",
    "chua-ro.luan-ve-phuong-phap": "descartes.discours-de-la-methode",
    "chua-ro.may": "chua-ro.nephelai",                                  # cùng vở hài kịch; tên gốc làm bản chính
    "chua-ro.meditations-on-first-philosophy": "descartes.meditationes-de-prima-philosophia",
    "chua-ro.metaphysica": "aristotle.metaphysica",
    "chua-ro.metaphysik-der-sitten": "chua-ro.die-metaphysik-der-sitten",
    "chua-ro.mot-vai-suy-nghi-ve-giao-duc": "locke.some-thoughts-concerning-education",
    "chua-ro.nen-tang-sieu-hinh-hoc-cua-dao-duc": "kant.grundlegung-zur-metaphysik-der-sitten",
    "chua-ro.nhung-van-de-cua-triet-hoc": "russell.the-problems-of-philosophy",
    "chua-ro.pha-he-cua-dao-duc": "nietzsche.zur-genealogie-der-moral",
    "chua-ro.phenomenology-of-spirit": "hegel.phanomenologie-des-geistes",
    "chua-ro.philosophical-investigations": "wittgenstein.philosophische-untersuchungen",
    "chua-ro.sach-ve-cac-nguy-bien": "bentham.the-book-of-fallacies",
    "chua-ro.su-ra-doi-cua-bi-kich": "nietzsche.die-geburt-der-tragodie",
    "chua-ro.summa-theologica": "aquinas.summa-theologiae",
    "chua-ro.suy-niem-ve-triet-hoc-thu-nhat": "descartes.meditationes-de-prima-philosophia",
    "chua-ro.the-communist-manifesto": "marx.manifest-der-kommunistischen-partei",
    "chua-ro.the-gay-science": "nietzsche.die-frohliche-wissenschaft",
    "chua-ro.the-guide-for-the-perplexed": "maimonides.dalalat-al-hairin",
    "chua-ro.the-logic-of-scientific-discovery": "popper.logik-der-forschung",
    "chua-ro.thus-spoke-zarathustra": "nietzsche.also-sprach-zarathustra",
    "chua-ro.ton-tai-va-hu-vo": "sartre.l-etre-et-le-neant",
    "chua-ro.ton-tai-va-thoi-gian": "heidegger.sein-und-zeit",
    "chua-ro.triet-hoc-so-hoc": "husserl.philosophie-der-arithmetik",
    "chua-ro.tu-va-vat": "quine.word-and-object",
    "chua-ro.tuyen-ngon-cua-dang-cong-san": "marx.manifest-der-kommunistischen-partei",
    "chua-ro.xa-hoi-mo-va-ke-thu-cua-no": "popper.the-open-society-and-its-enemies",
    "chua-ro.zarathustra-da-noi-nhu-the": "nietzsche.also-sprach-zarathustra",
}

ATTRIBUTION = {
    # chua-ro.* không trùng tác phẩm nào đã có
    "chua-ro.a-sand-county-almanac": "Aldo Leopold",
    "chua-ro.against-democracy": "Jason Brennan",
    "chua-ro.against-method": "Paul Feyerabend",
    "chua-ro.an-inquiry-into-the-human-mind": "Thomas Reid",
    "chua-ro.anh-em-nha-karamazov": "Fyodor Dostoevsky",
    "chua-ro.animal-liberation": "Peter Singer",
    "chua-ro.anthropologie-in-pragmatischer-hinsicht": "Immanuel Kant",
    "chua-ro.apologia": "Platon",
    "chua-ro.basic-color-terms": "Brent Berlin và Paul Kay",
    "chua-ro.beantwortung-der-frage-was-ist-aufklarung": "Immanuel Kant",
    "chua-ro.candide": "Voltaire",
    "chua-ro.canh-duc-truyen-dang-luc": "Đạo Nguyên (道原) biên soạn",
    "chua-ro.capitalism-socialism-and-democracy": "Joseph A. Schumpeter",
    "chua-ro.contra-mendacium": "Augustine",
    "chua-ro.de-mendacio": "Augustine",
    "chua-ro.de-revolutionibus": "Nicolaus Copernicus",
    "chua-ro.dieu-tra": "David Hume",
    "chua-ro.den-hien-dai-tu-truyen-thong": "Trần Đình Hượu",
    "chua-ro.die-fragmente-der-vorsokratiker": "Hermann Diels và Walther Kranz (biên tập)",
    "chua-ro.die-metaphysik-der-sitten": "Immanuel Kant",
    "chua-ro.ethics-inventing-right-and-wrong": "J. L. Mackie",
    "chua-ro.evil-and-the-god-of-love": "John Hick",
    "chua-ro.god-freedom-and-evil": "Alvin Plantinga",
    "chua-ro.historiai": "Herodotus",
    "chua-ro.hoang-viet-van-tuyen": "Bùi Huy Bích tuyển (văn nhiều tác giả)",
    "chua-ro.hopi-time": "Ekkehart Malotki",
    "chua-ro.how-to-do-things-with-words": "J. L. Austin",
    "chua-ro.in-a-different-voice": "Carol Gilligan",
    "chua-ro.just-and-unjust-wars": "Michael Walzer",
    "chua-ro.killing-in-war": "Jeff McMahan",
    "chua-ro.la-technique": "Jacques Ellul",
    "chua-ro.lam-son-thuc-luc": "Nguyễn Trãi soạn, Lê Lợi đề tựa",
    "chua-ro.language-truth-and-logic": "A. J. Ayer",
    "chua-ro.liberalism-and-the-limits-of-justice": "Michael Sandel",
    "chua-ro.living-without-free-will": "Derk Pereboom",
    "chua-ro.meaning-in-life-and-why-it-matters": "Susan Wolf",
    "chua-ro.memorabilia": "Xenophon",
    "chua-ro.nephelai": "Aristophanes",
    "chua-ro.philosophical-essays": "Bertrand Russell",
    "chua-ro.principia": "Isaac Newton",
    "chua-ro.principia-ethica": "G. E. Moore",
    "chua-ro.reason-truth-and-history": "Hilary Putnam",
    "chua-ro.respect-for-nature": "Paul W. Taylor",
    "chua-ro.spheres-of-justice": "Michael Walzer",
    "chua-ro.stanford-encyclopedia-of-philosophy": "Metaphysics Research Lab, Đại học Stanford (chủ biên Edward N. Zalta)",
    "chua-ro.stoicorum-veterum-fragmenta": "Hans von Arnim (sưu tập, biên tập)",
    "chua-ro.superintelligence": "Nick Bostrom",
    "chua-ro.tai-san-la-gi": "Pierre-Joseph Proudhon",
    "chua-ro.the-case-for-animal-rights": "Tom Regan",
    "chua-ro.the-concept-of-mind": "Gilbert Ryle",
    "chua-ro.the-conscious-mind": "David J. Chalmers",
    "chua-ro.the-reasons-of-love": "Harry G. Frankfurt",
    "chua-ro.the-structure-of-scientific-revolutions": "Thomas Kuhn",
    "chua-ro.three-essays-moral-and-political": "David Hume",
    "chua-ro.tu-truyen": "John Stuart Mill",
    "chua-ro.uber-ein-vermeintes-recht-aus-menschenliebe-zu-lug": "Immanuel Kant",
    "chua-ro.viet-nam-su-luoc": "Trần Trọng Kim",
    # tác phẩm có `author` nhưng cần ghi rõ người soạn (bằng chứng lô 13–20)
    "khong-tu.le-ky": "Đái Thánh (戴聖, Tây Hán) biên tập; văn của học trò Khổng Tử và nho gia đời sau",
    "khong-tu.luan-ngu": "lời Khổng Tử và học trò, do các thế hệ học trò biên soạn",
    "khong-tu.xuan-thu": "theo truyền thống (Mạnh Tử 3B9) do Khổng Tử soạn",
    "mac-tu.mac-kinh": "Mặc gia hậu kỳ (khuyết danh), trong sách Mặc Tử",
    "mac-tu.mac-tu": "khuyết danh, nhiều thế hệ Mặc gia",
    "han-phi.han-phi-tu": "quy cho Hàn Phi; việc ông viết cả sách còn tranh luận",
    "chu-hy.can-tu-luc": "Chu Hy cùng Lã Tổ Khiêm (呂祖謙) biên soạn",
    "chu-hy.chu-tu-ngu-loai": "lời giảng của Chu Hy do học trò ghi lại",
    "epictetus.cam-nang": "Arrian ghi lại lời dạy của Epictetus",
    "epictetus.dien-tu": "Arrian ghi lại lời dạy của Epictetus",
    "democritus.great-diacosmos": "phái Theophrastus quy cho Leucippus (Diogenes Laërtius IX.46)",
    "thales.on-the-solstice": "chỉ được quy cho Thales theo một số người (Diogenes Laërtius I.23)",
    "tue-trung.tue-trung-thuong-si-ngu-luc": "Pháp Loa biên tập sau khi Tuệ Trung mất",
    "russell.principia-mathematica": "Alfred North Whitehead và Bertrand Russell",
    "marx.manifest-der-kommunistischen-partei": "Karl Marx và Friedrich Engels",
    "marx.die-deutsche-ideologie": "Karl Marx và Friedrich Engels",
}

# (year_fixed, years_ok, year_note). year_fixed None = giữ năm rút được, chỉ thêm years_ok/year_note.
YEARS = {
    "bentham.an-introduction-to-the-principles-of-morals-and-le": (1789, [1780], "in 1780, xuất bản (có bổ sung) 1789"),
    "leibniz.nouveaux-essais-sur-l-entendement-humain": (1765, [1704], "hoàn thành 1704, in lần đầu 1765"),
    "marx.okonomisch-philosophische-manuskripte": (1932, [1844], "soạn 1844, in lần đầu 1932"),
    "marx.die-deutsche-ideologie": (1932, [1845, 1846], "soạn 1845–46 cùng Engels, in đầy đủ 1932"),
    "marx.thesen-uber-feuerbach": (1888, [1845], "soạn xuân 1845; Engels in bản đã biên tập năm 1888; nguyên bản in 1924"),
    "hobbes.the-elements-of-law-natural-and-politic": (1650, [1640], "lưu hành bản chép tay 1640; in lần đầu 1650"),
    "tran-duc-thao.van-de-con-nguoi-va-chu-nghia-ly-luan-khong-co-con": (1988, [1989], "in lần đầu tháng 9/1988, lần hai tháng 1/1989"),
    "chua-ro.den-hien-dai-tu-truyen-thong": (1994, [1996], "in lần đầu 1994; bản NXB Văn hóa 1996"),
    "mill.utilitarianism": (1861, [1863], "đăng kỳ trên Fraser’s Magazine 1861, in thành sách 1863"),
    "sartre.l-existentialisme-est-un-humanisme": (1946, [1945], "bài giảng cuối năm 1945, in 1946"),
    "chua-ro.lam-son-thuc-luc": (1431, [1944], "nguyên bản chữ Hán soạn 1431; 1944 là năm bản dịch Mạc Bảo Thần"),
    "popper.logik-der-forschung": (None, [1935, 1959], "in mùa thu 1934, trang tên đề 1935; bản tiếng Anh The Logic of Scientific Discovery 1959"),
    "aquinas.summa-theologiae": (None, [1267], "soạn khoảng 1265–1273 (SEP: 1267–73), bỏ dở"),
    "augustine.confessiones": (None, [396], "soạn k. 396–400"),
    "augustine.de-civitate-dei": (None, [412], "soạn 413–426 (SEP ghi khởi 412)"),
    "augustine.de-libero-arbitrio": (None, [], "soạn 388–395"),
    "augustine.de-trinitate": (None, [], "soạn 399–419 hoặc muộn tới 426"),
    "anselm.cur-deus-homo": (None, [], "soạn 1095–98"),
    "anselm.de-veritate": (None, [], "soạn khoảng 1080–86"),
    "anselm.monologion": (None, [1076, 1077], "soạn 1075–76 (IEP ghi 1077)"),
    "anselm.proslogion": (None, [1078], "soạn 1077–78"),
    "aquinas.summa-contra-gentiles": (None, [], "soạn 1259–65"),
    "averroes.al-kashf-an-manahij-al-adilla": (None, [1180], "1179/80, chưa chắc"),
    "averroes.fasl-al-maqal": (None, [1179], "1178/9 (SEP)"),
    "averroes.tahafut-al-tahafut": (None, [1181], "soạn khoảng 1180/81"),
    "arendt.eichmann-in-jerusalem-a-report-on-the-banality-of": (None, [1965], "bản sửa và mở rộng 1965"),
    "arendt.on-revolution": (None, [1965], "bản sửa 1965"),
    "beauvoir.pyrrhus-et-cineas": (None, [1943], "viết 1943, in 1944"),
    "chua-ro.anh-em-nha-karamazov": (None, [1879], "xuất bản 1879–1880"),
    "chua-ro.dieu-tra": (None, [1751], "tên chung cho hai cuốn An Enquiry concerning Human Understanding (1748) và An Enquiry concerning the Principles of Morals (1751) (kiểm mẫu 5.1)"),
    "chua-ro.die-fragmente-der-vorsokratiker": (1903, [1951], "bản đầu 1903; bản thứ 6 năm 1951 là bản chuẩn được trích dẫn (DK)"),
    "chua-ro.hoang-viet-van-tuyen": (None, [], "1825 (Minh Mệnh 6) là năm bản khắc in Hi Văn Đường"),
    "chua-ro.how-to-do-things-with-words": (None, [1955, 1975], "in sau khi tác giả mất, từ bài giảng William James 1955; bản 2 năm 1975"),
    "chua-ro.stanford-encyclopedia-of-philosophy": (None, [2004, 2008, 2026], "bách khoa trực tuyến từ 1995; các năm trích là năm của từng mục"),
    "chua-ro.stoicorum-veterum-fragmenta": (None, [1905], "ba tập 1903–1905; tập I (Zeno) năm 1905"),
    "chua-ro.nephelai": (None, [], "diễn lần đầu 423 TCN; bản còn lại là bản sửa sau đó"),
    "platon.politeia": (-380, [], "niên đại ước đoán; IEP: c. 380–360 TCN"),
    "averroes.chu-giai-lon-ve-sieu-hinh-hoc-cua-aristotle": (None, [], "soạn sau 1190 (SEP)"),
    "descartes.le-monde": (None, [1633], "soạn 1629–1633, in sau khi tác giả mất năm 1664"),
    "frege.grundgesetze-der-arithmetik": (None, [1903], "tập I 1893, tập II 1903"),
    "hegel.enzyklopadie-der-philosophischen-wissenschaften": (None, [1827, 1830], "in lần đầu 1817; bản sửa 1827, 1830"),
    "hegel.grundlinien-der-philosophie-des-rechts": (None, [1820], "ra năm 1820, trang tên đề 1821"),
    "hegel.wissenschaft-der-logik": (None, [], "xuất bản 1812–16 thành nhiều phần"),
    "heidegger.holzwege": (None, [], "các bài soạn 1935–46, in 1950"),
    "heidegger.uberlegungen-iixv": (None, [], "ba tập GA94–96, in 2014; viết 1931–1941"),
    "heraclitus.peri-physeos": (None, [], "ước đoán theo thời tác giả hoạt động (k. 500 TCN); tên sách do người sau gán"),
    "hume.a-treatise-of-human-nature": (None, [1740], "quyển 1–2 năm 1739, quyển 3 năm 1740"),
    "hume.an-enquiry-concerning-human-understanding": (None, [1758], "in 1748 với tên Philosophical Essays concerning Human Understanding; tên hiện nay từ bản 1758"),
    "hume.dialogues-concerning-natural-religion": (None, [], "in sau khi tác giả mất; soạn từ đầu thập niên 1750"),
    "hume.the-history-of-england": (None, [1762], "6 tập in từ 1754 đến 1762"),
    "husserl.die-krisis-der-europaischen-wissenschaften": (None, [1954], "năm 1936 chỉ in hai phần đầu trên tạp chí ở Belgrade; toàn văn trong Husserliana 6 (1954)"),
    "husserl.logische-untersuchungen": (None, [1901], "tập I 1900, tập II 1901; bản sửa 1913"),
    "husserl.meditations-cartesiennes": (None, [1929, 1950], "từ bài giảng ở Paris 1929; bản Pháp 1931; bản Đức trong Husserliana 1 (1950)"),
    "kant.kritik-der-reinen-vernunft": (None, [1787], "bản A 1781; bản B sửa lớn 1787"),
    "leibniz.discours-de-metaphysique": (None, [], "năm soạn; in sau khi tác giả mất"),
    "leibniz.la-monadologie": (None, [], "năm soạn; in sau khi tác giả mất"),
    "marcus-aurelius.suy-tuong": (None, [], "soạn k. 170–180 (IEP: c. 171–175)"),
    "nguyen-trai.binh-ngo-dai-cao": (None, [], "Toàn thư chép sau ngày 12 tháng 12 Đinh Mùi, trước mục Mậu Thân (1428)"),
    "nietzsche.also-sprach-zarathustra": (None, [1884, 1885], "phần I–II 1883, III 1884, IV 1885"),
    "nietzsche.die-frohliche-wissenschaft": (None, [1887], "bản mở rộng 1887"),
    "nietzsche.menschliches-allzumenschliches": (None, [1879, 1880], "tập 1 năm 1878; tập 2 năm 1879–1880"),
    "parfit.on-what-matters": (None, [2017], "2011; tập 3 năm 2017"),
    "pascal.les-provinciales": (None, [1657], "các thư ra từng lá, 1/1656–3/1657"),
    "pascal.pensees": (None, [], "in sau khi tác giả mất, bản Port-Royal 1670"),
    "pascal.traite-du-triangle-arithmetique": (None, [1654], "soạn 1653–54, in sau khi tác giả mất"),
    "popper.the-poverty-of-historicism": (None, [1944, 1945], "ba bài trên Economica 1944–45, in thành sách 1957"),
    "quine.pursuit-of-truth": (None, [1992], "bản sửa 1992"),
    "rousseau.discours-sur-les-sciences-et-les-arts": (None, [1750], "đoạt giải Viện Hàn lâm Dijon 1750; SEP ghi in 1751, IEP ghi 1750"),
    "russell.a-history-of-western-philosophy": (None, [1946], "bản Mỹ 1945; bản Anh 1946"),
    "russell.principia-mathematica": (None, [1912, 1913], "ba tập, 1910–1913"),
    "sartre.critique-de-la-raison-dialectique": (None, [1985], "tập 1 năm 1960; tập 2 (di cảo) 1985"),
    "spinoza.ethica-ordine-geometrico-demonstrata": (None, [], "di cảo, in trong Opera posthuma 1677"),
    "spinoza.tractatus-politicus": (None, [], "di cảo, dang dở; in 1677"),
    "wittgenstein.the-blue-and-brown-books": (None, [], "đọc chép 1933–35, in 1958"),
    "wittgenstein.tractatus-logico-philosophicus": (None, [1922], "bản Đức 1921; bản song ngữ mang tên Latin 1922"),
    "wittgenstein.uber-gewiheit": (None, [], "ghi chép hai năm cuối đời, in sau khi tác giả mất"),
}


# Trường bỏ khỏi bản ghi (kết quả kiểm mẫu: `same_as` sai).
REMOVE = {"chua-ro.dieu-tra": ["same_as"]}


def apply(works: dict) -> int:
    n = 0
    for k, fields in REMOVE.items():
        for f in fields:
            n += f in works[k]
            works[k].pop(f, None)
    for table in (SAME_AS, ATTRIBUTION, YEARS):
        missing = sorted(set(table) - set(works))
        if missing:
            raise SystemExit(f"khóa không còn trong works.yml: {missing}")
    for k, v in SAME_AS.items():
        if v not in works:
            raise SystemExit(f"{k}: same_as {v!r} không có")
        n += works[k].get("same_as") != v
        works[k]["same_as"] = v
    for k, v in ATTRIBUTION.items():
        n += works[k].get("attribution") != v
        works[k]["attribution"] = v
    for k, (fixed, ok, note) in YEARS.items():
        r = works[k]
        if fixed is not None:
            n += r.get("year_fixed") != fixed
            r["year_fixed"] = fixed
        if ok:
            n += r.get("years_ok") != ok
            r["years_ok"] = ok
        n += r.get("year_note") != note
        r["year_note"] = note
    return n


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    works = yaml.safe_load(kb_works.OUT.read_text(encoding="utf-8"))
    n = apply(works)
    print(f"{'Sẽ ghi' if a.dry_run else 'Đã ghi'} {n} trường.")
    if not a.dry_run and n:
        kb_works.OUT.write_text(kb_works.render(kb_works.merge_kept(kb_works.extract(), works)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
