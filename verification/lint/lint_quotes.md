# Báo cáo linter trích dẫn

Sinh bằng `python tools/lint_quotes.py --write`. So khối `!!! quote` của Lõi viết tay với `data/kb/quotes.yml`. Đây là báo cáo nền của đợt 2: chỉ ghi lại, bổ sung ở đợt 5.

**237 chỗ** ở **1 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `khong-khop` | khối trích trong trang không khớp bản ghi nào trong quotes.yml | 0 |
| `mo-coi` | bản ghi trỏ tới đơn vị không còn chứa khối trích | 0 |
| `chua-ghep-tac-pham` | bản ghi chưa ghép với tác phẩm trong works.yml | 82 |
| `chua-co-vi-tri` | bản ghi chưa có vị trí trích (locator) | 155 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `data/kb/quotes.yml` | `cau-hoi/tam-tri-va-ai.md#doc-van-ban-goc` | `chua-co-vi-tri` | alan-turing-computing-ma.mind | "Alan Turing, “Computing Machinery and Intelligence”, *Mind*, 1950" |
| `data/kb/quotes.yml` | `cau-hoi/luan-chung-ton-giao.md#doc-van-ban-goc` | `chua-co-vi-tri` | anselm.proslogion | "Anselm, *Proslogion*, chương 2, 1077–1078 (bản tiếng Anh của S. N. Deane)" |
| `data/kb/quotes.yml` | `people/anselm` | `chua-co-vi-tri` | anselm.proslogion-2 | "Anselm, *Proslogion*, chương 1 — bản dịch tiếng Anh của Sidney Norton Deane (1903)" |
| `data/kb/quotes.yml` | `cau-hoi/trach-nhiem.md#doc-van-ban-goc` | `chua-co-vi-tri` | aristotle.dao-duc-nicomachus | "Aristotle, *Đạo đức Nicomachus*, Quyển III, chương 1 (bản tiếng Anh của W. D. Ross)" |
| `data/kb/quotes.yml` | `people/aristotle` | `chua-co-vi-tri` | aristotle.dao-duc-nicomachus-2 | "Aristotle, *Đạo đức Nicomachus* I.7 (1098a) — bản dịch tiếng Anh của D. P. Chase" |
| `data/kb/quotes.yml` | `cau-hoi/thoi-gian.md#doc-van-ban-goc` | `chua-co-vi-tri` | augustine.confessions | "Augustine, *Confessions*, Quyển XI, chương 14 (bản tiếng Anh của Edward Pusey, 1838)" |
| `data/kb/quotes.yml` | `people/augustine` | `chua-co-vi-tri` | augustine.tu-thu | "Augustine, *Tự thú* (*Confessions*), quyển I, chương 1 — bản dịch tiếng Anh của Edward B. Pusey (1838)" |
| `data/kb/quotes.yml` | `people/bentham` | `chua-co-vi-tri` | bentham.an-introduction-to-the-principles-of-mor | "Bentham, *An Introduction to the Principles of Morals and Legislation* (1789), chương I, đoạn 1 — nguyên văn tiếng Anh, bản Clarendon Press 1907 in lại ấn bản 1823" |
| `data/kb/quotes.yml` | `cau-hoi/chan-ly.md#doc-van-ban-goc` | `chua-co-vi-tri` | bertrand-russell.the-problems-of-philosophy | "Bertrand Russell, *The Problems of Philosophy* (1912), chương XII — nguyên văn tiếng Anh" |
| `data/kb/quotes.yml` | `people/russell` | `chua-co-vi-tri` | bertrand-russell.the-problems-of-philosophy-2 | "Bertrand Russell, *The Problems of Philosophy* (1912), chương VI “On Induction” — nguyên văn tiếng Anh" |
| `data/kb/quotes.yml` | `people/pascal` | `chua-co-vi-tri` | blaise-pascal.pensees | "Blaise Pascal, *Pensées* (1670), đoạn 347 theo Brunschvicg (200 theo Lafuma) — bản dịch tiếng Anh của W. F. Trotter (1910)" |
| `data/kb/quotes.yml` | `cau-hoi/dinh-menh.md#doc-van-ban-goc` | `chua-co-vi-tri` | boethius.an-ui-cua-triet-hoc | "Boethius, *An ủi của Triết học*, Quyển V (khoảng 524; bản dịch tiếng Anh của H. R. James, 1897)" |
| `data/kb/quotes.yml` | `people/chu-hy` | `chua-co-vi-tri` | chu-hy.chu-tu-ngu-loai | "Chu Hy, *Chu Tử ngữ loại* (朱子語類), quyển 94, lời đáp học trò về Thái cực — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/chu-van-an` | `chua-co-vi-tri` | chu-van-an.trich | "*Đại Việt sử ký toàn thư*, Bản kỷ quyển 7, tiểu sử Chu An chép ở năm 1370 — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `cau-hoi/nghe-thuat.md#doc-van-ban-goc` | `chua-co-vi-tri` | clive-bell.art | "Clive Bell, *Art*, chương 1, 1914" |
| `data/kb/quotes.yml` | `cau-hoi/sieu-dao-duc.md#doc-van-ban-goc` | `chua-co-vi-tri` | david-hume.a-treatise-of-human-nature | "David Hume, *A Treatise of Human Nature*, quyển 3 (1740), phần 1, mục 1 — nguyên văn tiếng Anh, bản Project Gutenberg (chính tả đã hiện đại hóa một phần)" |
| `data/kb/quotes.yml` | `cau-hoi/loi-chung.md#doc-van-ban-goc` | `chua-co-vi-tri` | david-hume.an-enquiry-concerning-human-understandin | "David Hume, *An Enquiry Concerning Human Understanding*, mục X 'Of Miracles', 1748" |
| `data/kb/quotes.yml` | `people/democritus` | `chua-co-vi-tri` | democritus.trich | "Democritus, dẫn theo Diogenes Laërtius IX.72 — bản dịch tiếng Anh của R. D. Hicks (1925)" |
| `data/kb/quotes.yml` | `cau-hoi/tri-thuc.md#doc-van-ban-goc` | `chua-co-vi-tri` | descartes.suy-niem-ve-triet-hoc-de-nhat | "Descartes, *Suy niệm về Triết học Đệ nhất*, Suy niệm I, 1641 (bản tiếng Anh của John Veitch)" |
| `data/kb/quotes.yml` | `cau-hoi/van-de-tam-tri.md#doc-van-ban-goc` | `chua-co-vi-tri` | descartes.suy-niem-ve-triet-hoc-de-nhat-2 | "Descartes, *Suy niệm về Triết học Đệ nhất*, Suy niệm VI, 1641 (bản tiếng Anh của John Veitch)" |
| `data/kb/quotes.yml` | `people/zeno` | `chua-co-vi-tri` | diogenes-laertius.lives-of-the-eminent-philosophers | "Diogenes Laërtius, *Lives of the Eminent Philosophers* VII.87 — bản dịch tiếng Anh của R. D. Hicks (1925)" |
| `data/kb/quotes.yml` | `people/duc-phat` | `chua-co-vi-tri` | duc-phat.trich | "*Kinh Vô ngã tướng* (SN 22.59) — bản dịch tiếng Anh của Bhikkhu Sujato, SuttaCentral (CC0)" |
| `data/kb/quotes.yml` | `people/husserl` | `chua-co-vi-tri` | edmund-husserl.logische-untersuchungen | "Edmund Husserl, *Logische Untersuchungen*, tập II (1901), Dẫn nhập, §2 — nguyên văn tiếng Đức bản in lần đầu (chính tả hiện đại hóa)" |
| `data/kb/quotes.yml` | `people/epictetus` | `chua-co-vi-tri` | epictetus.cam-nang | "Epictetus, *Cẩm nang* (*Encheiridion*), chương 5 — bản dịch tiếng Anh của George Long (1877)" |
| `data/kb/quotes.yml` | `cau-hoi/cai-chet.md#doc-van-ban-goc` | `chua-co-vi-tri` | epicurus.nhung-cham-ngon-chu-yeu | "Epicurus, *Những châm ngôn chủ yếu*, câu 2 (bản dịch tiếng Anh của C. D. Yonge, 1853)" |
| `data/kb/quotes.yml` | `people/epicurus` | `chua-co-vi-tri` | epicurus.thu-gui-menoeceus | "Epicurus, *Thư gửi Menoeceus* 125, chép trong Diogenes Laërtius X — bản dịch tiếng Anh của R. D. Hicks (1925)" |
| `data/kb/quotes.yml` | `people/nietzsche` | `chua-co-vi-tri` | friedrich-nietzsche.die-frohliche-wissenschaft | "Friedrich Nietzsche, *Die fröhliche Wissenschaft* (1882), §125 “Người điên” — bản dịch tiếng Anh của Thomas Common (*The Joyful Wisdom*, 1910)" |
| `data/kb/quotes.yml` | `people/frege` | `chua-co-vi-tri` | gottlob-frege-uber-sinn.zeitschrift-fur-philosophie-und-philosop | "Gottlob Frege, “Über Sinn und Bedeutung”, *Zeitschrift für Philosophie und philosophische Kritik* 100 (1892), tr. 26–27 — nguyên văn tiếng Đức (chữ ſ viết thành s)" |
| `data/kb/quotes.yml` | `people/han-phi` | `chua-co-vi-tri` | han-phi.han-phi-tu | "Hàn Phi, *Hàn Phi Tử*, thiên 6 “Hữu độ” (有度) — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/hegel` | `chua-co-vi-tri` | hegel.grundlinien-der-philosophie-des-rechts | "Hegel, *Grundlinien der Philosophie des Rechts* (1821), Lời tựa (đề ngày 25/6/1820) — bản dịch tiếng Anh của S. W. Dyde (1896)" |
| `data/kb/quotes.yml` | `people/heraclitus` | `chua-co-vi-tri` | heraclitus-manh-van-dk-2.early-greek-philosophy | "Heraclitus, mảnh văn DK 22 B30 — bản dịch tiếng Anh của John Burnet, *Early Greek Philosophy* (1908)" |
| `data/kb/quotes.yml` | `people/thales` | `chua-co-vi-tri` | herodotus.historiai | "Herodotus, *Historiai* I.74 — bản dịch tiếng Anh của G. C. Macaulay (1890)" |
| `data/kb/quotes.yml` | `cau-hoi/tu-do-y-chi.md#doc-van-ban-goc` | `chua-co-vi-tri` | hume.an-enquiry-concerning-human-understandin | "Hume, *An Enquiry Concerning Human Understanding*, 1748, mục VIII, đoạn 73" |
| `data/kb/quotes.yml` | `doc/hume-nhan-qua.md#doc-tung-doan` | `chua-co-vi-tri` | hume.an-enquiry-concerning-human-understandin-2 | "Hume, *An Enquiry concerning Human Understanding* (1748), EHU 4.2 và 4.4 — bản Selby-Bigge (1902)" |
| `data/kb/quotes.yml` | `doc/hume-nhan-qua.md#doc-tung-doan` | `chua-co-vi-tri` | hume.an-enquiry-concerning-human-understandin-3 | "Hume, *An Enquiry concerning Human Understanding* (1748), EHU 4.21 — bản Selby-Bigge (1902)" |
| `data/kb/quotes.yml` | `doc/hume-nhan-qua.md#doc-tung-doan` | `chua-co-vi-tri` | hume.an-enquiry-concerning-human-understandin-4 | "Hume, *An Enquiry concerning Human Understanding* (1748), EHU 5.6 — bản Selby-Bigge (1902)" |
| `data/kb/quotes.yml` | `doc/hume-nhan-qua.md#doc-tung-doan` | `chua-co-vi-tri` | hume.an-enquiry-concerning-human-understandin-5 | "Hume, *An Enquiry concerning Human Understanding* (1748), EHU 7.6 và 7.28 — bản Selby-Bigge (1902)" |
| `data/kb/quotes.yml` | `people/hume` | `chua-co-vi-tri` | hume.an-enquiry-concerning-human-understandin-6 | "Hume, *An Enquiry concerning Human Understanding* (1748), mục V, phần 1 — nguyên văn tiếng Anh, bản L. A. Selby-Bigge in lại ấn bản 1777" |
| `data/kb/quotes.yml` | `cau-hoi/noi-doi.md#doc-van-ban-goc` | `chua-co-vi-tri` | immanuel-kant.uber-ein-vermeintes-recht-aus-menschenli | "Immanuel Kant, *Über ein vermeintes Recht aus Menschenliebe zu lügen* (1797) — bản dịch tiếng Anh của T. K. Abbott (lần in thứ 4, 1889)" |
| `data/kb/quotes.yml` | `cau-hoi/tu-do-ngon-luan.md#cac-lap-truong-chinh` | `chua-co-vi-tri` | j-s-mill.on-liberty | "J. S. Mill, *On Liberty* (1859), chương 1" |
| `data/kb/quotes.yml` | `cau-hoi/dao-duc-ung-dung.md#doc-van-ban-goc` | `chua-co-vi-tri` | jeremy-bentham.an-introduction-to-the-principles-of-mor | "Jeremy Bentham, *An Introduction to the Principles of Morals and Legislation*, chương 17, 1789" |
| `data/kb/quotes.yml` | `people/locke` | `chua-co-vi-tri` | john-locke.khao-luan-ve-hieu-biet-cua-con-nguoi | "John Locke, *Khảo luận về hiểu biết của con người* (1689), quyển II, chương 1, §2 — nguyên văn tiếng Anh" |
| `data/kb/quotes.yml` | `cau-hoi/tai-san-rieng.md#cac-lap-truong-chinh` | `chua-co-vi-tri` | john-locke.two-treatises-of-government | "John Locke, *Two Treatises of Government* (1689), §27" |
| `data/kb/quotes.yml` | `cau-hoi/dao-duc-hanh-dong.md#doc-van-ban-goc` | `chua-co-vi-tri` | john-stuart-mill.utilitarianism | "John Stuart Mill, *Utilitarianism*, chương 2, 1863" |
| `data/kb/quotes.yml` | `cau-hoi/noi-doi.md#doc-van-ban-goc` | `chua-co-vi-tri` | john-stuart-mill.utilitarianism-2 | "John Stuart Mill, *Utilitarianism* (1863), chương 2 — theo lần in thứ 7 (1879), Project Gutenberg" |
| `data/kb/quotes.yml` | `doc/kant-khai-sang.md#doc-tung-doan` | `chua-co-vi-tri` | kant.beantwortung-der-frage-was-ist-aufklarun | "Kant, *Beantwortung der Frage: Was ist Aufklärung?* (1784), Ak 8:35 — nguyên văn tiếng Đức" |
| `data/kb/quotes.yml` | `doc/kant-khai-sang.md#doc-tung-doan` | `chua-co-vi-tri` | kant.beantwortung-der-frage-was-ist-aufklarun-2 | "Kant, *Beantwortung der Frage: Was ist Aufklärung?* (1784), Ak 8:35 — nguyên văn tiếng Đức" |
| `data/kb/quotes.yml` | `doc/kant-khai-sang.md#doc-tung-doan` | `chua-co-vi-tri` | kant.beantwortung-der-frage-was-ist-aufklarun-3 | "Kant, *Beantwortung der Frage: Was ist Aufklärung?* (1784), Ak 8:36–37 — nguyên văn tiếng Đức" |
| `data/kb/quotes.yml` | `doc/kant-khai-sang.md#doc-tung-doan` | `chua-co-vi-tri` | kant.beantwortung-der-frage-was-ist-aufklarun-4 | "Kant, *Beantwortung der Frage: Was ist Aufklärung?* (1784), Ak 8:36 và 8:37 — nguyên văn tiếng Đức" |
| `data/kb/quotes.yml` | `people/kant` | `chua-co-vi-tri` | kant.grundlegung-zur-metaphysik-der-sitten | "Kant, *Grundlegung zur Metaphysik der Sitten* (1785), mục II, Akademie-Ausgabe 4:429 — nguyên văn tiếng Đức" |
| `data/kb/quotes.yml` | `people/khong-tu` | `chua-co-vi-tri` | khong-tu.luan-ngu | "Khổng Tử, *Luận ngữ* 15.24 (thiên Vệ Linh Công) — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/kierkegaard` | `chua-co-vi-tri` | kierkegaard-but-danh-joh.fear-and-trembling | "Kierkegaard (bút danh Johannes de Silentio), *Fear and Trembling* (1843), phần “Preliminary Expectoration”, đoạn tả “hiệp sĩ đức tin” — bản dịch tiếng Anh của L. M. Hollander (1923)" |
| `data/kb/quotes.yml` | `people/lao-tu` | `chua-co-vi-tri` | lao-tu.trich | "*Đạo đức kinh*, chương 64 — nguyên văn chữ Hán theo bản lưu hành (ctext.org) và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/leibniz` | `chua-co-vi-tri` | leibniz.don-tu-luan | "Leibniz, *Đơn tử luận* (viết năm 1714), §32 — bản dịch tiếng Anh của Robert Latta (1898)" |
| `data/kb/quotes.yml` | `cau-hoi/cai-toi.md#doc-van-ban-goc` | `chua-co-vi-tri` | locke.an-essay-concerning-human-understanding | "Locke, *An Essay Concerning Human Understanding*, II.xxvii, 1689/1694" |
| `data/kb/quotes.yml` | `people/wittgenstein` | `chua-co-vi-tri` | ludwig-wittgenstein.tractatus-logico-philosophicus | "Ludwig Wittgenstein, *Tractatus Logico-Philosophicus* (1921), mệnh đề 6.54 — bản dịch tiếng Anh của C. K. Ogden (1922)" |
| `data/kb/quotes.yml` | `people/mac-tu` | `chua-co-vi-tri` | mac-tu.trich | "*Mặc Tử*, thiên 15 “Kiêm ái trung” (兼愛中) — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/maimonides` | `chua-co-vi-tri` | maimonides.chi-dan-cho-nguoi-hoang-mang | "Maimonides, *Chỉ dẫn cho người hoang mang*, phần I, chương 60 — bản dịch tiếng Anh của M. Friedländer (1904)" |
| `data/kb/quotes.yml` | `people/manh-tu` | `chua-co-vi-tri` | manh-tu.manh-tu | "Mạnh Tử, *Mạnh Tử* 3B2 (thiên Đằng Văn công hạ), lời đáp Cảnh Xuân về các thuyết khách — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/marcus-aurelius` | `chua-co-vi-tri` | marcus-aurelius.suy-tuong | "Marcus Aurelius, *Suy tưởng* II.1 — bản dịch tiếng Anh của George Long (1862)" |
| `data/kb/quotes.yml` | `people/marx` | `chua-co-vi-tri` | marx.trich | "Karl Marx, “Thesen über Feuerbach” (viết mùa xuân 1845), luận cương 11 — nguyên văn tiếng Đức theo bản Engels in năm 1888" |
| `data/kb/quotes.yml` | `doc/mill-tu-do.md#doc-tung-doan` | `chua-co-vi-tri` | mill.on-liberty | "Mill, *On Liberty* (1859), chương II, đoạn 1 — nguyên văn, bản Project Gutenberg" |
| `data/kb/quotes.yml` | `doc/mill-tu-do.md#doc-tung-doan` | `chua-co-vi-tri` | mill.on-liberty-2 | "Mill, *On Liberty* (1859), chương II, đoạn 2, 3 và 6 — nguyên văn, bản Project Gutenberg" |
| `data/kb/quotes.yml` | `doc/mill-tu-do.md#doc-tung-doan` | `chua-co-vi-tri` | mill.on-liberty-3 | "Mill, *On Liberty* (1859), chương II, đoạn 21 và 23 — nguyên văn, bản Project Gutenberg" |
| `data/kb/quotes.yml` | `doc/mill-tu-do.md#doc-tung-doan` | `chua-co-vi-tri` | mill.on-liberty-4 | "Mill, *On Liberty* (1859), chương II, đoạn 34 — nguyên văn, bản Project Gutenberg" |
| `data/kb/quotes.yml` | `people/mill` | `chua-co-vi-tri` | mill.on-liberty-5 | "Mill, *On Liberty* (1859), chương I — nguyên văn tiếng Anh" |
| `data/kb/quotes.yml` | `people/nagarjuna` | `chua-co-vi-tri` | nagarjuna.trung-luan | "Nagarjuna, *Trung luận* 24.14 — bản Hán dịch của Cưu-ma-la-thập (đầu thế kỷ 5), nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/nguyen-trai` | `chua-co-vi-tri` | nguyen-trai-loi-tau-khi.dai-viet-su-ky-toan-thu | "Nguyễn Trãi, lời tâu khi dâng bản vẽ khánh đá (1437), chép trong *Đại Việt sử ký toàn thư*, Bản kỷ quyển 11 — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `cau-hoi/nho-giao-viet.md#doc-van-ban-goc` | `chua-co-vi-tri` | nguyen-trai.binh-ngo-dai-cao | "Nguyễn Trãi, *Bình Ngô đại cáo*, 1428 (câu dịch trong sách giáo khoa)" |
| `data/kb/quotes.yml` | `people/socrates` | `chua-co-vi-tri` | platon.bien-ho-cua-socrates | "Platon, *Biện hộ của Socrates* 38a — bản dịch tiếng Anh của Benjamin Jowett" |
| `data/kb/quotes.yml` | `cau-hoi/dan-chu.md#doc-van-ban-goc` | `chua-co-vi-tri` | platon.cong-hoa | "Platon, *Cộng hòa*, Quyển VI (bản dịch tiếng Anh của Benjamin Jowett, phạm vi công cộng)" |
| `data/kb/quotes.yml` | `people/platon` | `chua-co-vi-tri` | platon.cong-hoa-2 | "Platon, *Cộng hòa* X, 596a — bản dịch tiếng Anh của Benjamin Jowett" |
| `data/kb/quotes.yml` | `cau-hoi/pho-quat.md#doc-van-ban-goc` | `chua-co-vi-tri` | platon.phaedo | "Platon, *Phaedo*, 100c–d (bản tiếng Anh của Benjamin Jowett)" |
| `data/kb/quotes.yml` | `people/descartes` | `chua-co-vi-tri` | rene-descartes.luan-ve-phuong-phap | "René Descartes, *Luận về phương pháp* (1637), phần IV — bản dịch tiếng Anh của John Veitch" |
| `data/kb/quotes.yml` | `people/rousseau` | `chua-co-vi-tri` | rousseau.du-contrat-social | "Rousseau, *Du contrat social* (1762), quyển I, chương 1 — bản dịch tiếng Anh của G. D. H. Cole (1913)" |
| `data/kb/quotes.yml` | `doc/russell-gia-tri.md#doc-tung-doan` | `chua-co-vi-tri` | russell.the-problems-of-philosophy | "Russell, *The Problems of Philosophy* (1912), chương XV, đoạn 3 — nguyên văn, bản in 1912" |
| `data/kb/quotes.yml` | `doc/russell-gia-tri.md#doc-tung-doan` | `chua-co-vi-tri` | russell.the-problems-of-philosophy-2 | "Russell, *The Problems of Philosophy* (1912), chương XV, đoạn 4 — nguyên văn, bản in 1912" |
| `data/kb/quotes.yml` | `doc/russell-gia-tri.md#doc-tung-doan` | `chua-co-vi-tri` | russell.the-problems-of-philosophy-3 | "Russell, *The Problems of Philosophy* (1912), chương XV, đoạn 7 — nguyên văn, bản in 1912" |
| `data/kb/quotes.yml` | `doc/russell-gia-tri.md#doc-tung-doan` | `chua-co-vi-tri` | russell.the-problems-of-philosophy-4 | "Russell, *The Problems of Philosophy* (1912), chương XV, đoạn 9 và 12 — nguyên văn, bản in 1912" |
| `data/kb/quotes.yml` | `doc/sartre-hien-sinh.md#doc-tung-doan-dien-y` | `chua-co-vi-tri` | sartre.l-existentialisme-est-un-humanisme | "Sartre, *L'existentialisme est un humanisme* (bài nói 1945, in 1946), phần “bị bỏ rơi” — nguyên văn tiếng Pháp (trích ngắn)" |
| `data/kb/quotes.yml` | `people/beauvoir` | `chua-co-vi-tri` | simone-de-beauvoir.le-deuxieme-sexe | "Simone de Beauvoir, *Le Deuxième Sexe*, tập II (Paris: Gallimard, 1949), phần một, chương 1 “Enfance”, câu mở đầu — trích một câu; tác phẩm còn bản quyền" |
| `data/kb/quotes.yml` | `people/spinoza` | `chua-co-vi-tri` | spinoza.dao-duc-hoc | "Spinoza, *Đạo đức học* (1677), phần I, phụ lục — bản dịch tiếng Anh của R. H. M. Elwes (1883–1884)" |
| `data/kb/quotes.yml` | `people/aquinas` | `chua-co-vi-tri` | thomas-aquinas.tong-luan-than-hoc | "Thomas Aquinas, *Tổng luận Thần học* I, câu 1, mục 8, trả lời phản bác 2 — bản dịch tiếng Anh của Fathers of the English Dominican Province (1920)" |
| `data/kb/quotes.yml` | `cau-hoi/khe-uoc-xa-hoi.md#doc-van-ban-goc` | `chua-co-vi-tri` | thomas-hobbes.leviathan | "Thomas Hobbes, *Leviathan*, chương 13, 1651" |
| `data/kb/quotes.yml` | `people/hobbes` | `chua-co-vi-tri` | thomas-hobbes.leviathan-2 | "Thomas Hobbes, *Leviathan* (1651), chương 13 — nguyên văn tiếng Anh, chính tả theo bản in đầu tiên" |
| `data/kb/quotes.yml` | `doc/tho-van-ly-tran.md#doc-tung-doan` | `chua-co-vi-tri` | tran-nhan-tong.cu-tran-lac-dao-phu | "Trần Nhân Tông, *Cư trần lạc đạo phú*, hội 5 (chữ Nôm) và bài kệ kết (chữ Hán) — nguyên văn, phiên âm, diễn nghĩa của Logos Zero" |
| `data/kb/quotes.yml` | `people/tran-nhan-tong` | `chua-co-vi-tri` | tran-nhan-tong.cu-tran-lac-dao-phu-2 | "Trần Nhân Tông, *Cư trần lạc đạo phú*, hội thứ năm — chữ Nôm và phiên âm quốc ngữ theo Wikisource tiếng Việt" |
| `data/kb/quotes.yml` | `people/trang-tu` | `chua-co-vi-tri` | trang-tu.trang-tu | "Trang Tử, *Trang Tử*, thiên 4 “Nhân gian thế” (人間世), đoạn kết — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `doc/platon-bien-ho.md#doc-tung-doan` | `chua-co-vi-tri` | trich.bien-ho-21d | "Biện hộ, 21d — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-bien-ho.md#doc-tung-doan` | `chua-co-vi-tri` | trich.bien-ho-29ab | "Biện hộ, 29a–b — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-bien-ho.md#doc-tung-doan` | `chua-co-vi-tri` | trich.bien-ho-38a | "Biện hộ, 38a — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-bien-ho.md#doc-tung-doan` | `chua-co-vi-tri` | trich.bien-ho-40c | "Biện hộ, 40c — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/nguyen-trai-binh-ngo.md#doc-tung-doan` | `chua-co-vi-tri` | trich.binh-ngo-dai-cao-cau-mo-dau-theo-toan-thu | "Bình Ngô đại cáo, câu mở đầu (theo Toàn thư) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/nguyen-trai-binh-ngo.md#doc-tung-doan` | `chua-co-vi-tri` | trich.binh-ngo-dai-cao-theo-toan-thu | "Bình Ngô đại cáo (theo Toàn thư) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/nguyen-trai-binh-ngo.md#doc-tung-doan` | `chua-co-vi-tri` | trich.binh-ngo-dai-cao-theo-toan-thu-2 | "Bình Ngô đại cáo (theo Toàn thư) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/nguyen-trai-binh-ngo.md#doc-tung-doan` | `chua-co-vi-tri` | trich.binh-ngo-dai-cao-theo-toan-thu-3 | "Bình Ngô đại cáo (theo Toàn thư) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-co-vi-tri` | trich.cam-nang-1 | "Cẩm nang §1 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-co-vi-tri` | trich.cam-nang-3 | "Cẩm nang §3 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-co-vi-tri` | trich.cam-nang-48 | "Cẩm nang §48 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-co-vi-tri` | trich.cam-nang-5 | "Cẩm nang §5 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-co-vi-tri` | trich.cam-nang-8 | "Cẩm nang §8 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/platon-hang-dong.md#doc-tung-doan` | `chua-co-vi-tri` | trich.cong-hoa-515a-va-515c | "Cộng hòa, 515a và 515c — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-hang-dong.md#doc-tung-doan` | `chua-co-vi-tri` | trich.cong-hoa-516b | "Cộng hòa, 516b — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-hang-dong.md#doc-tung-doan` | `chua-co-vi-tri` | trich.cong-hoa-517a | "Cộng hòa, 517a — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-hang-dong.md#doc-tung-doan` | `chua-co-vi-tri` | trich.cong-hoa-518bc-va-520c | "Cộng hòa, 518b–c và 520c — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-co-vi-tri` | trich.dao-duc-kinh-chuong-1 | "Đạo đức kinh, chương 1 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-co-vi-tri` | trich.dao-duc-kinh-chuong-11 | "Đạo đức kinh, chương 11 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-co-vi-tri` | trich.dao-duc-kinh-chuong-2 | "Đạo đức kinh, chương 2 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-co-vi-tri` | trich.dao-duc-kinh-chuong-44 | "Đạo đức kinh, chương 44 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-co-vi-tri` | trich.dao-duc-kinh-chuong-8-va-78 | "Đạo đức kinh, chương 8 và 78 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/aristotle-dao-duc.md#doc-tung-doan` | `chua-co-vi-tri` | trich.dao-duc-nicomachus-i-2-1094a1822 | "Đạo đức Nicomachus I.2, 1094a18–22 — bản dịch W. D. Ross (1925)" |
| `data/kb/quotes.yml` | `doc/aristotle-dao-duc.md#doc-tung-doan` | `chua-co-vi-tri` | trich.dao-duc-nicomachus-i-7-1098a1620 | "Đạo đức Nicomachus I.7, 1098a16–20 — bản dịch W. D. Ross (1925)" |
| `data/kb/quotes.yml` | `doc/aristotle-dao-duc.md#doc-tung-doan` | `chua-co-vi-tri` | trich.dao-duc-nicomachus-ii-4-1105a3034 | "Đạo đức Nicomachus II.4, 1105a30–34 — bản dịch W. D. Ross (1925)" |
| `data/kb/quotes.yml` | `doc/aristotle-dao-duc.md#doc-tung-doan` | `chua-co-vi-tri` | trich.dao-duc-nicomachus-ii-6-1106b361107a2 | "Đạo đức Nicomachus II.6, 1106b36–1107a2 — bản dịch W. D. Ross (1925)" |
| `data/kb/quotes.yml` | `cau-hoi/cai-dep.md#doc-van-ban-goc` | `chua-co-vi-tri` | trich.david-hume-of-the-standard-of-taste-1757 | "David Hume, 'Of the Standard of Taste', 1757" |
| `data/kb/quotes.yml` | `doc/luan-ngu.md#doc-tung-doan` | `chua-co-vi-tri` | trich.luan-ngu-thien-bat-dat-3-4 | "*Luận ngữ*, thiên Bát dật, 3.4 — nguyên văn theo ctext.org" |
| `data/kb/quotes.yml` | `doc/luan-ngu.md#doc-tung-doan` | `chua-co-vi-tri` | trich.luan-ngu-thien-hoc-nhi-1-1 | "*Luận ngữ*, thiên Học nhi, 1.1 — nguyên văn theo ctext.org" |
| `data/kb/quotes.yml` | `doc/luan-ngu.md#doc-tung-doan` | `chua-co-vi-tri` | trich.luan-ngu-thien-ly-nhan-4-16-va-thien-ve-linh-cong-15-21 | "*Luận ngữ*, thiên Lý nhân, 4.16 và thiên Vệ Linh Công, 15.21 — nguyên văn theo ctext.org" |
| `data/kb/quotes.yml` | `doc/luan-ngu.md#doc-tung-doan` | `chua-co-vi-tri` | trich.luan-ngu-thien-ung-da-6-11 | "*Luận ngữ*, thiên Ung dã, 6.11 — nguyên văn theo ctext.org" |
| `data/kb/quotes.yml` | `doc/luan-ngu.md#doc-tung-doan` | `chua-co-vi-tri` | trich.luan-ngu-thien-ve-linh-cong-15-24 | "*Luận ngữ*, thiên Vệ Linh Công, 15.24 — nguyên văn theo ctext.org" |
| `data/kb/quotes.yml` | `doc/luan-ngu.md#doc-tung-doan` | `chua-co-vi-tri` | trich.luan-ngu-thien-vi-chinh-2-17 | "*Luận ngữ*, thiên Vi chính, 2.17 — nguyên văn theo ctext.org" |
| `data/kb/quotes.yml` | `doc/mac-tu-kiem-ai.md#doc-tung-doan` | `chua-co-vi-tri` | trich.mac-tu-thien-14-kiem-ai-thuong | "Mặc Tử, thiên 14 Kiêm ái thượng — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/mac-tu-kiem-ai.md#doc-tung-doan` | `chua-co-vi-tri` | trich.mac-tu-thien-16-kiem-ai-ha | "Mặc Tử, thiên 16 Kiêm ái hạ — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/mac-tu-kiem-ai.md#doc-tung-doan` | `chua-co-vi-tri` | trich.mac-tu-thien-17-phi-cong-thuong | "Mặc Tử, thiên 17 Phi công thượng — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/mac-tu-kiem-ai.md#doc-tung-doan` | `chua-co-vi-tri` | trich.mac-tu-thien-26-thien-chi-thuong | "Mặc Tử, thiên 26 Thiên chí thượng — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/tho-van-ly-tran.md#doc-tung-doan` | `chua-co-vi-tri` | trich.man-giac-cao-tat-thi-chung-co-benh-bao-moi-nguoi | "Mãn Giác, “Cáo tật thị chúng” (Có bệnh, bảo mọi người) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/manh-tu-tinh-thien.md#doc-tung-doan` | `chua-co-vi-tri` | trich.manh-tu-2a2-thien-cong-ton-suu-thuong | "Mạnh Tử 2A2 (thiên Công Tôn Sửu thượng) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/manh-tu-tinh-thien.md#doc-tung-doan` | `chua-co-vi-tri` | trich.manh-tu-2a6-thien-cong-ton-suu-thuong | "Mạnh Tử 2A6 (thiên Công Tôn Sửu thượng) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/manh-tu-tinh-thien.md#doc-tung-doan` | `chua-co-vi-tri` | trich.manh-tu-6a2-thien-cao-tu-thuong | "Mạnh Tử 6A2 (thiên Cáo Tử thượng) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/manh-tu-tinh-thien.md#doc-tung-doan` | `chua-co-vi-tri` | trich.manh-tu-6a8-thien-cao-tu-thuong | "Mạnh Tử 6A8 (thiên Cáo Tử thượng) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-niem-i-12-at-7-22 | "Suy niệm I, §12 (AT 7:22) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-niem-i-3-at-7-18 | "Suy niệm I, §3 (AT 7:18) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-niem-i-5-va-8-at-7-1920 | "Suy niệm I, §5 và §8 (AT 7:19–20) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-niem-ii-11-va-16-at-7-30-34 | "Suy niệm II, §11 và §16 (AT 7:30, 34) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-niem-ii-3-at-7-25 | "Suy niệm II, §3 (AT 7:25) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-tuong-ii-1 | "Suy tưởng II.1 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-tuong-ii-11-va-iv-48 | "Suy tưởng II.11 và IV.48 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-tuong-ix-30 | "Suy tưởng IX.30 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-tuong-viii-47 | "Suy tưởng VIII.47 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-co-vi-tri` | trich.suy-tuong-x-28 | "Suy tưởng X.28 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/tam-kinh.md#doc-tung-doan` | `chua-co-vi-tri` | trich.tam-kinh-t251 | "Tâm kinh (T251) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/tam-kinh.md#doc-tung-doan` | `chua-co-vi-tri` | trich.tam-kinh-t251-2 | "Tâm kinh (T251) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/tam-kinh.md#doc-tung-doan` | `chua-co-vi-tri` | trich.tam-kinh-t251-cau-mo-dau | "Tâm kinh (T251), câu mở đầu — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/tam-kinh.md#doc-tung-doan` | `chua-co-vi-tri` | trich.tam-kinh-t251-doan-ket | "Tâm kinh (T251), đoạn kết — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `cau-hoi/truc-lam.md#doc-van-ban-goc` | `chua-co-vi-tri` | trich.tran-nhan-tong-ke-cu-tran-lac-dao-ban-dich-nghia-cua-logos-z | "Trần Nhân Tông, kệ 'Cư trần lạc đạo' (bản dịch nghĩa của Logos Zero)" |
| `data/kb/quotes.yml` | `doc/tho-van-ly-tran.md#doc-tung-doan` | `chua-co-vi-tri` | trich.tran-nhan-tong-xuan-hieu-sang-xuan | "Trần Nhân Tông, “Xuân hiểu” (Sáng xuân) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/trang-tu-mong-ho-diep.md#doc-tung-doan` | `chua-co-vi-tri` | trich.trang-tu-te-vat-luan | "Trang Tử, Tề vật luận — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/trang-tu-mong-ho-diep.md#doc-tung-doan` | `chua-co-vi-tri` | trich.trang-tu-te-vat-luan-cau-ket | "Trang Tử, Tề vật luận, câu kết — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/trang-tu-mong-ho-diep.md#doc-tung-doan` | `chua-co-vi-tri` | trich.trang-tu-te-vat-luan-doan-ket | "Trang Tử, Tề vật luận, đoạn kết — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `cau-hoi/bien-gioi-di-cu.md#doc-van-ban-goc` | `chua-co-vi-tri` | trich.tuyen-ngon-quoc-te-nhan-quyen-1948-dieu-13 | "Tuyên ngôn Quốc tế Nhân quyền (1948), Điều 13" |
| `data/kb/quotes.yml` | `doc/tho-van-ly-tran.md#doc-tung-doan` | `chua-co-vi-tri` | trich.van-hanh-thi-de-tu-bao-de-tu | "Vạn Hạnh, “Thị đệ tử” (Bảo đệ tử) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `chua-co-vi-tri` | trich.winston-churchill-phat-bieu-tai-ha-vien-anh-11-11-1947 | "Winston Churchill, phát biểu tại Hạ viện Anh, 11/11/1947" |
| `data/kb/quotes.yml` | `cau-hoi/ban-tinh-con-nguoi.md#doc-van-ban-goc` | `chua-co-vi-tri` | tuan-tu.tuan-tu | "Tuân Tử, *Tuân Tử*, thiên 23 *Tính ác* (性惡), thế kỷ 3 TCN — nguyên văn theo ctext.org" |
| `data/kb/quotes.yml` | `people/tuan-tu` | `chua-co-vi-tri` | tuan-tu.tuan-tu-2 | "Tuân Tử, *Tuân Tử*, thiên 1 “Khuyến học” (勸學), đoạn mở đầu — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/tue-trung` | `chua-co-vi-tri` | tue-trung-thuong-si.pham-thanh-bat-di | "Tuệ Trung Thượng Sĩ, *Phàm thánh bất dị*, hai câu — phiên âm Hán Việt theo Nguyễn Huệ Chi (2014)" |
| `data/kb/quotes.yml` | `cau-hoi/tam-tri-va-ai.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | alan-turing-computing-ma.mind | "Alan Turing, “Computing Machinery and Intelligence”, *Mind*, 1950" |
| `data/kb/quotes.yml` | `cau-hoi/trach-nhiem.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | aristotle.dao-duc-nicomachus | "Aristotle, *Đạo đức Nicomachus*, Quyển III, chương 1 (bản tiếng Anh của W. D. Ross)" |
| `data/kb/quotes.yml` | `people/aristotle` | `chua-ghep-tac-pham` | aristotle.dao-duc-nicomachus-2 | "Aristotle, *Đạo đức Nicomachus* I.7 (1098a) — bản dịch tiếng Anh của D. P. Chase" |
| `data/kb/quotes.yml` | `people/augustine` | `chua-ghep-tac-pham` | augustine.tu-thu | "Augustine, *Tự thú* (*Confessions*), quyển I, chương 1 — bản dịch tiếng Anh của Edward B. Pusey (1838)" |
| `data/kb/quotes.yml` | `cau-hoi/dinh-menh.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | boethius.an-ui-cua-triet-hoc | "Boethius, *An ủi của Triết học*, Quyển V (khoảng 524; bản dịch tiếng Anh của H. R. James, 1897)" |
| `data/kb/quotes.yml` | `people/chu-van-an` | `chua-ghep-tac-pham` | chu-van-an.trich | "*Đại Việt sử ký toàn thư*, Bản kỷ quyển 7, tiểu sử Chu An chép ở năm 1370 — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `cau-hoi/nghe-thuat.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | clive-bell.art | "Clive Bell, *Art*, chương 1, 1914" |
| `data/kb/quotes.yml` | `people/democritus` | `chua-ghep-tac-pham` | democritus.trich | "Democritus, dẫn theo Diogenes Laërtius IX.72 — bản dịch tiếng Anh của R. D. Hicks (1925)" |
| `data/kb/quotes.yml` | `cau-hoi/tri-thuc.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | descartes.suy-niem-ve-triet-hoc-de-nhat | "Descartes, *Suy niệm về Triết học Đệ nhất*, Suy niệm I, 1641 (bản tiếng Anh của John Veitch)" |
| `data/kb/quotes.yml` | `cau-hoi/van-de-tam-tri.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | descartes.suy-niem-ve-triet-hoc-de-nhat-2 | "Descartes, *Suy niệm về Triết học Đệ nhất*, Suy niệm VI, 1641 (bản tiếng Anh của John Veitch)" |
| `data/kb/quotes.yml` | `people/zeno` | `chua-ghep-tac-pham` | diogenes-laertius.lives-of-the-eminent-philosophers | "Diogenes Laërtius, *Lives of the Eminent Philosophers* VII.87 — bản dịch tiếng Anh của R. D. Hicks (1925)" |
| `data/kb/quotes.yml` | `cau-hoi/cai-chet.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | epicurus.nhung-cham-ngon-chu-yeu | "Epicurus, *Những châm ngôn chủ yếu*, câu 2 (bản dịch tiếng Anh của C. D. Yonge, 1853)" |
| `data/kb/quotes.yml` | `people/frege` | `chua-ghep-tac-pham` | gottlob-frege-uber-sinn.zeitschrift-fur-philosophie-und-philosop | "Gottlob Frege, “Über Sinn und Bedeutung”, *Zeitschrift für Philosophie und philosophische Kritik* 100 (1892), tr. 26–27 — nguyên văn tiếng Đức (chữ ſ viết thành s)" |
| `data/kb/quotes.yml` | `people/heraclitus` | `chua-ghep-tac-pham` | heraclitus-manh-van-dk-2.early-greek-philosophy | "Heraclitus, mảnh văn DK 22 B30 — bản dịch tiếng Anh của John Burnet, *Early Greek Philosophy* (1908)" |
| `data/kb/quotes.yml` | `people/locke` | `chua-ghep-tac-pham` | john-locke.khao-luan-ve-hieu-biet-cua-con-nguoi | "John Locke, *Khảo luận về hiểu biết của con người* (1689), quyển II, chương 1, §2 — nguyên văn tiếng Anh" |
| `data/kb/quotes.yml` | `people/lao-tu` | `chua-ghep-tac-pham` | lao-tu.trich | "*Đạo đức kinh*, chương 64 — nguyên văn chữ Hán theo bản lưu hành (ctext.org) và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/leibniz` | `chua-ghep-tac-pham` | leibniz.don-tu-luan | "Leibniz, *Đơn tử luận* (viết năm 1714), §32 — bản dịch tiếng Anh của Robert Latta (1898)" |
| `data/kb/quotes.yml` | `people/maimonides` | `chua-ghep-tac-pham` | maimonides.chi-dan-cho-nguoi-hoang-mang | "Maimonides, *Chỉ dẫn cho người hoang mang*, phần I, chương 60 — bản dịch tiếng Anh của M. Friedländer (1904)" |
| `data/kb/quotes.yml` | `people/marx` | `chua-ghep-tac-pham` | marx.trich | "Karl Marx, “Thesen über Feuerbach” (viết mùa xuân 1845), luận cương 11 — nguyên văn tiếng Đức theo bản Engels in năm 1888" |
| `data/kb/quotes.yml` | `people/nagarjuna` | `chua-ghep-tac-pham` | nagarjuna.trung-luan | "Nagarjuna, *Trung luận* 24.14 — bản Hán dịch của Cưu-ma-la-thập (đầu thế kỷ 5), nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/nguyen-trai` | `chua-ghep-tac-pham` | nguyen-trai-loi-tau-khi.dai-viet-su-ky-toan-thu | "Nguyễn Trãi, lời tâu khi dâng bản vẽ khánh đá (1437), chép trong *Đại Việt sử ký toàn thư*, Bản kỷ quyển 11 — nguyên văn chữ Hán và phiên âm Hán Việt" |
| `data/kb/quotes.yml` | `people/socrates` | `chua-ghep-tac-pham` | platon.bien-ho-cua-socrates | "Platon, *Biện hộ của Socrates* 38a — bản dịch tiếng Anh của Benjamin Jowett" |
| `data/kb/quotes.yml` | `people/spinoza` | `chua-ghep-tac-pham` | spinoza.dao-duc-hoc | "Spinoza, *Đạo đức học* (1677), phần I, phụ lục — bản dịch tiếng Anh của R. H. M. Elwes (1883–1884)" |
| `data/kb/quotes.yml` | `people/aquinas` | `chua-ghep-tac-pham` | thomas-aquinas.tong-luan-than-hoc | "Thomas Aquinas, *Tổng luận Thần học* I, câu 1, mục 8, trả lời phản bác 2 — bản dịch tiếng Anh của Fathers of the English Dominican Province (1920)" |
| `data/kb/quotes.yml` | `doc/platon-bien-ho.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.bien-ho-21d | "Biện hộ, 21d — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-bien-ho.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.bien-ho-29ab | "Biện hộ, 29a–b — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-bien-ho.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.bien-ho-38a | "Biện hộ, 38a — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-bien-ho.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.bien-ho-40c | "Biện hộ, 40c — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/nguyen-trai-binh-ngo.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.binh-ngo-dai-cao-cau-mo-dau-theo-toan-thu | "Bình Ngô đại cáo, câu mở đầu (theo Toàn thư) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/nguyen-trai-binh-ngo.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.binh-ngo-dai-cao-theo-toan-thu | "Bình Ngô đại cáo (theo Toàn thư) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/nguyen-trai-binh-ngo.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.binh-ngo-dai-cao-theo-toan-thu-2 | "Bình Ngô đại cáo (theo Toàn thư) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/nguyen-trai-binh-ngo.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.binh-ngo-dai-cao-theo-toan-thu-3 | "Bình Ngô đại cáo (theo Toàn thư) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.cam-nang-1 | "Cẩm nang §1 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.cam-nang-3 | "Cẩm nang §3 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.cam-nang-48 | "Cẩm nang §48 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.cam-nang-5 | "Cẩm nang §5 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/epictetus-cam-nang.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.cam-nang-8 | "Cẩm nang §8 — bản dịch George Long (1877)" |
| `data/kb/quotes.yml` | `doc/platon-hang-dong.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.cong-hoa-515a-va-515c | "Cộng hòa, 515a và 515c — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-hang-dong.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.cong-hoa-516b | "Cộng hòa, 516b — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-hang-dong.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.cong-hoa-517a | "Cộng hòa, 517a — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/platon-hang-dong.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.cong-hoa-518bc-va-520c | "Cộng hòa, 518b–c và 520c — bản dịch Benjamin Jowett" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.dao-duc-kinh-chuong-1 | "Đạo đức kinh, chương 1 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.dao-duc-kinh-chuong-11 | "Đạo đức kinh, chương 11 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.dao-duc-kinh-chuong-2 | "Đạo đức kinh, chương 2 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.dao-duc-kinh-chuong-44 | "Đạo đức kinh, chương 44 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/dao-duc-kinh.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.dao-duc-kinh-chuong-8-va-78 | "Đạo đức kinh, chương 8 và 78 — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/aristotle-dao-duc.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.dao-duc-nicomachus-i-2-1094a1822 | "Đạo đức Nicomachus I.2, 1094a18–22 — bản dịch W. D. Ross (1925)" |
| `data/kb/quotes.yml` | `doc/aristotle-dao-duc.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.dao-duc-nicomachus-i-7-1098a1620 | "Đạo đức Nicomachus I.7, 1098a16–20 — bản dịch W. D. Ross (1925)" |
| `data/kb/quotes.yml` | `doc/aristotle-dao-duc.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.dao-duc-nicomachus-ii-4-1105a3034 | "Đạo đức Nicomachus II.4, 1105a30–34 — bản dịch W. D. Ross (1925)" |
| `data/kb/quotes.yml` | `doc/aristotle-dao-duc.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.dao-duc-nicomachus-ii-6-1106b361107a2 | "Đạo đức Nicomachus II.6, 1106b36–1107a2 — bản dịch W. D. Ross (1925)" |
| `data/kb/quotes.yml` | `cau-hoi/cai-dep.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | trich.david-hume-of-the-standard-of-taste-1757 | "David Hume, 'Of the Standard of Taste', 1757" |
| `data/kb/quotes.yml` | `doc/mac-tu-kiem-ai.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.mac-tu-thien-14-kiem-ai-thuong | "Mặc Tử, thiên 14 Kiêm ái thượng — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/mac-tu-kiem-ai.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.mac-tu-thien-16-kiem-ai-ha | "Mặc Tử, thiên 16 Kiêm ái hạ — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/mac-tu-kiem-ai.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.mac-tu-thien-17-phi-cong-thuong | "Mặc Tử, thiên 17 Phi công thượng — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/mac-tu-kiem-ai.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.mac-tu-thien-26-thien-chi-thuong | "Mặc Tử, thiên 26 Thiên chí thượng — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/tho-van-ly-tran.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.man-giac-cao-tat-thi-chung-co-benh-bao-moi-nguoi | "Mãn Giác, “Cáo tật thị chúng” (Có bệnh, bảo mọi người) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/manh-tu-tinh-thien.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.manh-tu-2a2-thien-cong-ton-suu-thuong | "Mạnh Tử 2A2 (thiên Công Tôn Sửu thượng) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/manh-tu-tinh-thien.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.manh-tu-2a6-thien-cong-ton-suu-thuong | "Mạnh Tử 2A6 (thiên Công Tôn Sửu thượng) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/manh-tu-tinh-thien.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.manh-tu-6a2-thien-cao-tu-thuong | "Mạnh Tử 6A2 (thiên Cáo Tử thượng) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/manh-tu-tinh-thien.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.manh-tu-6a8-thien-cao-tu-thuong | "Mạnh Tử 6A8 (thiên Cáo Tử thượng) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-niem-i-12-at-7-22 | "Suy niệm I, §12 (AT 7:22) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-niem-i-3-at-7-18 | "Suy niệm I, §3 (AT 7:18) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-niem-i-5-va-8-at-7-1920 | "Suy niệm I, §5 và §8 (AT 7:19–20) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-niem-ii-11-va-16-at-7-30-34 | "Suy niệm II, §11 và §16 (AT 7:30, 34) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/descartes-suy-niem.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-niem-ii-3-at-7-25 | "Suy niệm II, §3 (AT 7:25) — bản dịch John Veitch (1853)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-tuong-ii-1 | "Suy tưởng II.1 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-tuong-ii-11-va-iv-48 | "Suy tưởng II.11 và IV.48 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-tuong-ix-30 | "Suy tưởng IX.30 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-tuong-viii-47 | "Suy tưởng VIII.47 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.suy-tuong-x-28 | "Suy tưởng X.28 — bản dịch George Long (1862)" |
| `data/kb/quotes.yml` | `doc/tam-kinh.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.tam-kinh-t251 | "Tâm kinh (T251) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/tam-kinh.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.tam-kinh-t251-2 | "Tâm kinh (T251) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/tam-kinh.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.tam-kinh-t251-cau-mo-dau | "Tâm kinh (T251), câu mở đầu — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/tam-kinh.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.tam-kinh-t251-doan-ket | "Tâm kinh (T251), đoạn kết — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `cau-hoi/truc-lam.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | trich.tran-nhan-tong-ke-cu-tran-lac-dao-ban-dich-nghia-cua-logos-z | "Trần Nhân Tông, kệ 'Cư trần lạc đạo' (bản dịch nghĩa của Logos Zero)" |
| `data/kb/quotes.yml` | `doc/tho-van-ly-tran.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.tran-nhan-tong-xuan-hieu-sang-xuan | "Trần Nhân Tông, “Xuân hiểu” (Sáng xuân) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/trang-tu-mong-ho-diep.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.trang-tu-te-vat-luan | "Trang Tử, Tề vật luận — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/trang-tu-mong-ho-diep.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.trang-tu-te-vat-luan-cau-ket | "Trang Tử, Tề vật luận, câu kết — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `doc/trang-tu-mong-ho-diep.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.trang-tu-te-vat-luan-doan-ket | "Trang Tử, Tề vật luận, đoạn kết — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `cau-hoi/bien-gioi-di-cu.md#doc-van-ban-goc` | `chua-ghep-tac-pham` | trich.tuyen-ngon-quoc-te-nhan-quyen-1948-dieu-13 | "Tuyên ngôn Quốc tế Nhân quyền (1948), Điều 13" |
| `data/kb/quotes.yml` | `doc/tho-van-ly-tran.md#doc-tung-doan` | `chua-ghep-tac-pham` | trich.van-hanh-thi-de-tu-bao-de-tu | "Vạn Hạnh, “Thị đệ tử” (Bảo đệ tử) — nguyên văn, phiên âm, bản dịch của Logos Zero" |
| `data/kb/quotes.yml` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `chua-ghep-tac-pham` | trich.winston-churchill-phat-bieu-tai-ha-vien-anh-11-11-1947 | "Winston Churchill, phát biểu tại Hạ viện Anh, 11/11/1947" |
