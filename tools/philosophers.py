"""Sinh trang triết gia (docs/triet-gia/<id>.md) và trang chỉ mục
(docs/triet-gia/index.md) từ docs/assets/data/philosophers.json.

Nội dung (tiểu sử, tác phẩm, tư tưởng, một lập luận tiêu biểu, hiểu lầm
thường gặp, nguồn) nằm trong CONTENT của tool này. Hai phần được tính tự
động, không viết tay:

- "Chịu ảnh hưởng từ": đảo ngược trường "influence" của JSON.
- "Các bài khác nhắc tới": quét docs/ tìm các bài có link tới trang triết
  gia (../triet-gia/<id>.md). Vì vậy thêm link tới một triết gia trong bài
  nào thì phải chạy lại tool này (CI --check sẽ nhắc).

    python tools/philosophers.py          # sinh lại toàn bộ trang
    python tools/philosophers.py --check  # báo lỗi (mã thoát 1) nếu trang lệch
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = DOCS / "assets" / "data" / "philosophers.json"
OUT = DOCS / "triet-gia"
MARKER = "<!-- gen:philosophers: không sửa tay -->"
UPDATED = "2026-10-22"

SCHOOLS = ["Tiền Socrates", "Hy Lạp cổ đại", "La Mã", "Trung cổ", "Cận đại",
           "Thế kỷ 19", "Thế kỷ 20", "Trung Hoa", "Ấn Độ", "Việt Nam"]

# Nhãn độ chắc chắn chỉ có nghĩa trong các bài có chú giải nhãn; lọt vào dữ
# liệu triết gia thì nó hiện ra trơ trọi ở chỉ mục và dòng thời gian.
CERTAINTY_LABEL = re.compile(r"\[(chắc chắn|có cơ sở|suy đoán)\]")

# Mỗi mục:
#   desc      một câu cho thẻ mô tả (front matter);
#   bio       3-4 đoạn tiểu sử và bối cảnh, mỗi phần tử một đoạn;
#   works     tác phẩm chính: (năm, tên gốc in nghiêng, tên/diễn giải tiếng Việt);
#   thoughts  3-5 ý tưởng chính;
#   argument  (tùy chọn) một lập luận tiêu biểu: title, premises, conclusion,
#             objection (phản bác chính), reply (cách đáp lại);
#   misread   (tùy chọn) hiểu lầm thường gặp;
#   quote     (tùy chọn) trích văn bản thuộc phạm vi công cộng: source, orig, vi;
#   related   2-5 trang trong docs/ nên đọc tiếp;
#   sources   2-6 nguồn (nhãn Markdown, URL), ít nhất một mục SEP hoặc IEP.
# Không bịa: năm, tên tác phẩm, trích dẫn đều phải kiểm chứng được qua nguồn.
CONTENT = {
"thales": {
"desc": "Người được Aristotle coi là triết gia đầu tiên: hỏi muôn vật từ đâu mà ra và trả lời bằng một nguyên lý tự nhiên (nước), không bằng thần thoại.",
"bio": [
"Có hai giai thoại về Thales, vẽ ra hai chân dung trái ngược. Trong *Theaetetus* của Platon, ông mải ngẩng nhìn sao đến nỗi rơi xuống giếng, và một cô hầu gái người Thrace trêu rằng ông nóng lòng biết chuyện trên trời mà không thấy cái ở dưới chân. Còn Aristotle, trong *Chính trị học*, kể rằng khi bị chê nghèo vì theo đuổi thứ triết học vô ích, Thales nhìn trời đoán trước một mùa ô-liu bội thu, từ mùa đông đã thuê hết máy ép dầu ở Miletus và Chios, đến vụ thì cho thuê lại với giá tùy ý — để chứng tỏ triết gia muốn giàu thì dễ, chỉ là họ không nhắm tới điều đó. Cả hai đều là tương truyền, nhưng câu hỏi chúng đặt ra vẫn còn: nghĩ về những điều xa xôi thì có ích gì?",
"Thales sống ở Miletus, một thành phố Hy Lạp bên bờ biển phía tây Tiểu Á (nay thuộc Thổ Nhĩ Kỳ), khoảng đầu thế kỷ 6 TCN, và được xếp vào hàng “Bảy hiền nhân”. Ông không để lại cuốn sách nào chắc chắn là của mình; mọi điều ta biết đều qua lời kể lại. Herodotus chép rằng Thales đã báo trước cho người Ionia năm sẽ có một lần ngày hóa thành đêm; nhật thực ấy đến giữa lúc quân Lydia và quân Media đang giao chiến, khiến hai bên ngừng đánh. Các nhà thiên văn hiện đại cho đó là trận nhật thực ngày 28/5/585 TCN. Diogenes Laërtius, viết hơn tám trăm năm sau, kể thêm rằng ông đo chiều cao kim tự tháp bằng cách chờ đến giờ bóng người dài đúng bằng người.",
"Điều khiến Aristotle gọi Thales là người mở đầu việc nghiên cứu tự nhiên là một câu hỏi: muôn vật từ đâu mà ra? Theo Aristotle, Thales đáp: từ nước — và trái đất nổi trên nước. Ông còn được thuật lại là cho rằng nam châm có linh hồn vì nó làm sắt chuyển động, và “mọi vật đầy thần linh”. Nghe xa lạ, nhưng bước ngoặt nằm ở chỗ khác: lời giải thích không còn là chuyện thần linh nổi giận hay ban ơn, mà là một nguyên lý nằm ngay trong tự nhiên.",
"Quan trọng hơn câu trả lời là điều xảy ra sau đó: người ta cãi lại. Anaximander, được xem là học trò và người kế nghiệp Thales, cho rằng gốc của muôn vật không thể là nước. Từ đó một chuỗi tranh luận nối dài qua Heraclitus, Parmenides, Democritus: mỗi người đưa ra một câu trả lời có lý do, để người sau phê phán. Mỗi khi bạn hỏi “có lời giải thích tự nhiên nào cho chuyện này không?” trước một lời đồn “tâm linh”, là bạn đang đi trên con đường ấy.",
],
"works": [
("", "*On the Solstice*, *On the Equinox*", "Về chí điểm, về điểm phân: hai chuyên luận một số người xưa gán cho ông (Diogenes Laërtius I.23); không còn, có thể chưa từng có"),
("thế kỷ 5 TCN", "Herodotus, *Historiai* I.74–75", "lời kể sớm nhất còn lại: dự đoán nhật thực, chuyện nắn dòng sông Halys (chính Herodotus không tin chuyện sau)"),
("thế kỷ 4 TCN", "Aristotle, *Metaphysica* I.3; *De Anima* I.2, I.5", "nguồn chính cho thuyết “muôn vật từ nước” và “mọi vật đầy thần linh”"),
("1951, bản 6", "Diels–Kranz, *Die Fragmente der Vorsokratiker*, chương 11", "bộ sưu tập chuẩn; với Thales chỉ có lời thuật lại, không có mảnh văn nào chắc chắn của chính ông"),
],
"thoughts": [
"**Nguyên lý đầu tiên** (*archē*): đằng sau muôn hình vạn trạng có thể có một cái gốc chung. Hỏi như vậy là đã giả định thế giới có trật tự và trí óc con người hiểu được nó — rồi đưa ra lý do để người khác cân nhắc, bác bỏ, thay vì một lời phán.",
"Vật chất không chết: với Thales, nam châm “có linh hồn” và “mọi vật đầy thần linh”. Ranh giới sống – không sống của ông khác hẳn của ta; đọc người xưa, đừng vội gán khái niệm của mình cho họ.",
"Học qua lời kể lại: không còn chữ nào của Thales. Tìm hiểu ông là một bài tập về nguồn: ai kể, kể khi nào, cách sự kiện bao xa, có lý do gì để tin.",
],
"argument": {
"title": "Vì sao muôn vật từ nước?",
"intro": "Thales không để lại lập luận nào. Đây là phỏng đoán của Aristotle (*Siêu hình học* I.3, 983b) về lý do của ông — chính Aristotle dè dặt rằng Thales “có lẽ” rút ra ý này từ quan sát.",
"premises": [
"Mọi vật được nuôi dưỡng bằng cái ẩm; ngay cả hơi ấm của sự sống cũng sinh ra từ cái ẩm và nhờ nó mà duy trì.",
"Hạt giống của mọi vật đều có bản chất ẩm.",
"Cái mà muôn vật sinh ra từ đó và nhờ đó mà tồn tại là nguyên lý của chúng.",
"Nước là gốc của mọi thứ ẩm.",
],
"conclusion": "Vậy nước là nguyên lý của muôn vật.",
"objection": "Anaximander phản đối: nước, lửa, đất, khí luôn biến đổi qua lại, nên chọn riêng một thứ làm gốc là thiên vị; gốc của muôn vật phải là một cái khác hẳn, “cái vô hạn định” (*apeiron*). Hơn nữa, đi từ sinh vật sang mọi vật (đá, kim loại, lửa) là khái quát vội.",
"reply": "Thales không để lại lời đáp, nhưng có thể dựng lại: với ông, ranh giới giữa sống và không sống không rõ như với ta (nam châm “có linh hồn”), nên khái quát từ sự sống sang mọi vật không vội như ta tưởng. Và chính vì nước biến hóa được — bốc hơi, đông lại, lắng thành đất — mà nó đủ tư cách làm gốc; theo Aëtius, cả lửa của mặt trời và các vì sao cũng được nuôi bằng hơi nước.",
},
"quote": {
"source": "Herodotus, *Historiai* I.74 — bản dịch tiếng Anh của G. C. Macaulay (1890)",
"orig": "And this change of the day Thales the Milesian had foretold to the Ionians laying down as a limit this very year in which the change took place.",
"vi": "Và việc ngày hóa thành đêm ấy, Thales người Miletus đã báo trước cho người Ionia, định hạn đúng vào năm mà sự đổi thay xảy ra.",
"url": "https://www.gutenberg.org/ebooks/2707",
},
"misread": [
"**“Thales nghĩ mọi thứ thực chất đều là nước.”** Thực ra ta không chắc. Mọi điều ta biết đi qua Aristotle, người đọc các bậc tiền bối bằng khung “nguyên nhân vật chất” của chính mình — cách đọc mà học giả nay coi là gán ghép. Có thể Thales chỉ muốn nói muôn vật *sinh ra từ* nước.",
"**“Thales tính ra chính xác ngày nhật thực 28/5/585 TCN.”** Thực ra Herodotus chỉ nói ông báo trước nhật thực sẽ xảy ra trong năm ấy. Ngày 28/5/585 TCN là tính toán của thiên văn học hiện đại; ông làm cách nào, và có thật làm được không, vẫn còn tranh cãi.",
],
"related": [
("lich-su/hy-lap-co-dai.md", "Hy Lạp cổ đại: từ thần thoại đến lý trí"),
],
"sources": [
("O’Grady, Patricia, “Thales of Miletus”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/thales/"),
("Curd, Patricia, “Presocratic Philosophy”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/presocratics/"),
("Herodotus, *The History*, quyển I, bản dịch G. C. Macaulay (1890), Project Gutenberg.", "https://www.gutenberg.org/ebooks/2707"),
("Diogenes Laërtius, *Lives of the Eminent Philosophers*, quyển I, bản dịch R. D. Hicks (1925), Wikisource.", "https://en.wikisource.org/wiki/Lives_of_the_Eminent_Philosophers/Book_I"),
("Platon, *Theaetetus* (174a), bản dịch Benjamin Jowett, Project Gutenberg.", "https://www.gutenberg.org/ebooks/1726"),
("Aristotle, *Politics* I.11 (1259a), bản dịch William Ellis, Project Gutenberg.", "https://www.gutenberg.org/ebooks/6762"),
],
},
"heraclitus": {
"desc": "Triết gia của biến đổi và sự thống nhất các mặt đối lập: thế giới là ngọn lửa sống mãi, bùng lên và tắt đi theo chừng mực, theo một logos chung.",
"bio": [
"Hôm nay bạn tắm ở một khúc sông quê, mai quay lại: vẫn con sông ấy, nhưng không còn giọt nước nào của hôm qua. Vậy “cùng một con sông” nghĩa là gì? Câu đố nhỏ này gắn với tên Heraclitus, người Ephesus, sống quanh năm 500 TCN. Và ông đi xa hơn: có lẽ mọi thứ bền vững quanh ta, kể cả cơ thể ta, đều tồn tại theo cách của dòng sông.",
"Ephesus là một thành phố Hy Lạp giàu có ở Ionia, gần Miletus của Thales, khi ấy thuộc quyền người Ba Tư. Đời Heraclitus ít được biết chắc. Một lời kể nói ông được hưởng tước hiệu “vua” theo dòng dõi nhưng nhường lại cho người anh em; nhiều chuyện khác — như chuyện ông chết vì vùi mình trong chuồng bò để chữa bệnh phù — có vẻ được người sau bịa ra từ chính những câu văn của ông. Ông viết một cuốn sách duy nhất, tương truyền gửi trong đền Artemis; nay chỉ còn hơn một trăm mảnh văn, ngắn và cô đọng như lời sấm. Ông coi thường lối học nhiều mà không hiểu, chê cả các nhà thơ sử thi lẫn Pythagoras.",
"Điều Heraclitus muốn người ta nắm là *logos* — cái lẽ chung mà mọi việc diễn ra theo đó. “Lắng nghe không phải tôi mà là logos, thì khôn ngoan là đồng ý rằng muôn vật là một”, ông viết; vậy mà đa số “sống như thể mỗi người có một trí khôn riêng”. Thế giới với ông là một ngọn lửa sống mãi, bùng lên và tắt đi theo chừng mực. Các mặt đối lập gắn với nhau: nước biển vừa sạch nhất vừa bẩn nhất — cá uống được, người uống thì chết; cây cung và cây đàn lia hài hòa nhờ những lực kéo ngược chiều.",
"Ít triết gia cổ nào để lại dấu vết dài như vậy. Platon dựng thế giới cảm giác hay đổi thay theo hình mẫu Heraclitus; phái Khắc kỷ lấy vật lý học của ông làm nền; hoàng đế Marcus Aurelius nhiều lần dẫn lời ông; Hegel viết rằng không có mệnh đề nào của Heraclitus mà ông không đưa vào sách *Logic* của mình. Hôm nay, khi hỏi một công ty, một đội bóng hay một con người có còn là “nó” sau mọi đổi thay, ta vẫn đang giải câu đố dòng sông.",
],
"works": [
("k. 500 TCN", "*Peri physeōs*", "*Về tự nhiên*, tên Diogenes Laërtius ghi cho cuốn sách duy nhất của ông, chia ba phần (vũ trụ, chính trị, thần học); đã mất"),
("1951, bản 6", "Diels–Kranz, *Die Fragmente der Vorsokratiker*, chương 22", "chỉ còn mảnh văn (Diels–Kranz, phần B: hơn một trăm câu được người đời sau trích lại) cùng lời thuật lại"),
],
"thoughts": [
"**Biến đổi theo chừng mực**: thế giới là “ngọn lửa sống mãi” (B30). Cái ổn định không phải một vật đứng yên mà là quy luật, “chừng mực” của sự đổi thay — như cơ thể sống được nhờ trao đổi chất.",
"**Logos chung**: có một lẽ chung ai cũng có thể nắm, nhưng đa số sống như thể mình có trí khôn riêng (B2). Hiểu là thấy được cái chung ấy, không phải chất chồng thông tin: học nhiều thứ không dạy cho người ta hiểu (B40).",
"**Thống nhất các mặt đối lập**: nước biển tốt cho cá mà độc cho người (B61). Nhiều đối lập là hai mặt của một quan hệ; hỏi “đối với ai, xét về mặt nào” thì mâu thuẫn bớt mâu thuẫn.",
"**Căng thẳng tạo hài hòa**: như cây cung và cây đàn lia, hài hòa đến từ những lực kéo ngược chiều (B51). Xung đột không phải lúc nào cũng là dấu hiệu tan vỡ.",
],
"argument": {
"title": "Dòng sông vẫn là nó nhờ không ngừng đổi khác",
"intro": "Heraclitus không viết theo dạng tiền đề – kết luận. Đây là cách tái dựng ý của mảnh văn B12 — mảnh duy nhất về dòng sông được nhiều học giả coi là nguyên văn — theo cách đọc của Daniel Graham (SEP).",
"premises": [
"Những người bước xuống cùng những dòng sông thì nước chảy tới luôn khác và khác (B12).",
"Vậy mà đó vẫn là cùng những dòng sông: năm nay hay năm ngoái, ta vẫn tắm trên một con sông.",
"Nếu nước ngừng chảy, nó không còn là sông nữa mà thành hồ hay lòng sông cạn.",
],
"conclusion": "Có những thứ giữ được mình chính nhờ thay đổi: cái bền vững của chúng là khuôn mẫu, “chừng mực” của sự đổi thay, chứ không phải một khối vật chất đứng yên.",
"objection": "Platon (*Cratylus* 402a) thuật lại Heraclitus theo hướng triệt để: “mọi vật đều trôi đi, không gì đứng yên”, không thể bước hai lần xuống cùng một dòng sông; Cratylus, một môn đồ, còn nói không bước được dù một lần. Nếu mọi thứ đổi thay về mọi mặt thì không gì gọi tên hay biết được — Platon và Aristotle đều cho rằng Heraclitus rốt cuộc phủ nhận nguyên lý không mâu thuẫn.",
"reply": "Những người đọc theo B12 (Kirk, Marcovich, Graham) đáp: chính mảnh văn ấy khẳng định những dòng sông là *cùng một*; Heraclitus không phủ nhận sự đồng nhất mà giải thích nó. Các câu nghe như mâu thuẫn của ông thường ngầm chứa “đối với ai, xét về mặt nào”, nên không vi phạm logic. Còn câu “không bước hai lần” có lẽ là một cách đọc lệch, bắt nguồn từ Cratylus.",
},
"quote": {
"source": "Heraclitus, mảnh văn DK 22 B30 — bản dịch tiếng Anh của John Burnet, *Early Greek Philosophy* (1908)",
"orig": "This world, which is the same for all, no one of gods or men has made; but it was ever, is now, and ever shall be an ever-living Fire, with measures kindling, and measures going out.",
"vi": "Thế giới này, vốn chung cho mọi người, không thần nào hay người nào làm ra; nó đã luôn là, đang là và sẽ mãi là một ngọn Lửa sống mãi, bùng lên theo chừng mực và tắt đi theo chừng mực.",
"url": "https://www.gutenberg.org/ebooks/67097",
},
"misread": [
"**“Heraclitus nói: không ai tắm hai lần trên cùng một dòng sông.”** Thực ra câu ấy là lời thuật lại của Platon và Plutarch. Mảnh văn được nhiều học giả coi là nguyên văn (B12) lại nhấn mạnh rằng sông vẫn là *cùng một*, chính nhờ nước luôn đổi thay.",
"**“Heraclitus cho rằng đời là hỗn loạn, chẳng có gì chắc chắn.”** Thực ra ông nhấn mạnh trật tự: lửa bùng lên và tắt đi “theo chừng mực”, mọi việc diễn ra theo một logos chung; cái ông chê là con người không chịu nhìn ra trật tự ấy.",
],
"related": [
("lich-su/hy-lap-co-dai.md", "Hy Lạp cổ đại: từ thần thoại đến lý trí"),
],
"sources": [
("Graham, Daniel W., “Heraclitus”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/heraclitus/"),
("Graham, Daniel W., “Heraclitus (fl. c. 500 B.C.E.)”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/heraclit/"),
("Burnet, John, *Early Greek Philosophy*, bản 2 (1908), Project Gutenberg.", "https://www.gutenberg.org/ebooks/67097"),
("Diogenes Laërtius, *Lives of the Eminent Philosophers*, quyển IX, bản dịch R. D. Hicks (1925), Wikisource.", "https://en.wikisource.org/wiki/Lives_of_the_Eminent_Philosophers/Book_IX"),
("Hegel, G. W. F., *Lectures on the History of Philosophy*, tập 1, bản dịch E. S. Haldane (1892), Project Gutenberg.", "https://www.gutenberg.org/ebooks/51635"),
],
},
"democritus": {
"desc": "“Triết gia hay cười” xứ Abdera: vạn vật chỉ là nguyên tử chuyển động trong khoảng trống, còn hạnh phúc là một tâm hồn an vui, không sợ hãi.",
"bio": [
"Vị ngọt của ly nước mía, màu đỏ của trái ớt, cái nóng trưa hè — chúng có thật “ở ngoài kia”, hay chỉ có trong ta? Democritus trả lời bằng một câu còn sót lại: ngọt, đắng, nóng, lạnh, màu sắc chỉ có “theo quy ước”; trong thực tại chỉ có nguyên tử và khoảng trống. Câu trả lời ấy táo bạo đến mức hơn hai nghìn năm sau người ta vẫn còn tranh luận.",
"Democritus sinh khoảng năm 460 TCN ở Abdera, một thành phố ở miền bắc Hy Lạp, nên là người trẻ cùng thời với Socrates. Ông học với Leucippus, người đặt nền cho thuyết nguyên tử mà ông hệ thống hóa. Diogenes Laërtius kể ông tiêu hết phần gia tài vào những chuyến đi Ai Cập, Ba Tư, và khi đến Athens thì “chẳng ai biết tôi”; người xưa gọi ông là “triết gia hay cười” vì ông đề cao sự an vui; tương truyền ông thọ tới 109 tuổi. Ông viết rất nhiều, từ đạo đức, vật lý đến toán học và âm nhạc, nhưng không tác phẩm nào còn; ta biết ông chủ yếu qua Aristotle, người coi ông là đối thủ đáng gờm, và qua những câu trích rải rác.",
"Bức tranh của ông gọn đến kinh ngạc. Có vô số hạt nhỏ đến mức không thấy được, đặc, không thể cắt (*atomos*), khác nhau về hình dạng, kích thước và cách sắp xếp, chuyển động mãi trong khoảng trống vô hạn. Chúng va vào nhau, móc vào nhau thành cụm; đá, cây, con người, cả linh hồn đều là những cụm như thế, sinh ra rồi tan rã, kể cả các thế giới. Không cần thần linh hay mục đích nào điều khiển. Nhưng chính bức tranh ấy đặt ra câu hỏi khó cho tri thức: nếu màu sắc, mùi vị không có trong nguyên tử, mà giác quan là lối duy nhất ta có tới sự thật, thì ta biết được gì?",
"Democritus cũng là một nhà đạo đức. Các châm ngôn mang tên ông đặt điều tốt ở bên trong — một tâm hồn an vui (*euthymia*), không sợ hãi — đạt được bằng chừng mực và bớt lệ thuộc vào may rủi. Khoảng một thế kỷ sau, Epicurus tiếp nhận cả vật lý lẫn tinh thần ấy. Và khi các nhà khoa học thế kỷ 17 như Gassendi, Boyle tìm tiền thân cho khoa học mới, họ quay về thuyết nguyên tử Hy Lạp.",
],
"works": [
("", "*Lesser Diacosmos*", "Tiểu hệ thống thế giới: vũ trụ luận theo thuyết nguyên tử; ông tự ghi viết 730 năm sau khi thành Troy thất thủ (Diogenes Laërtius IX.41); đã mất"),
("", "*Great Diacosmos*", "Đại hệ thống thế giới: đôi khi gán cho ông, nhưng Theophrastus nói là của Leucippus; đã mất"),
("", "*Of Tranquillity*", "Về sự an vui: tác phẩm đạo đức trong danh mục do Thrasyllus lập (Diogenes Laërtius IX.46); đã mất"),
("1951, bản 6", "Diels–Kranz, *Die Fragmente der Vorsokratiker*, chương 68", "chỉ còn mảnh văn và lời thuật lại; phần lớn mảnh văn là châm ngôn đạo đức, chép trong tuyển tập của Stobaeus (thế kỷ 5)"),
],
"thoughts": [
"**Nguyên tử và khoảng trống**: mọi khác biệt ta thấy quy về hình dạng, thứ tự, vị trí của nguyên tử — như chữ cái: A khác N về hình, AN khác NA về thứ tự.",
"**Đảo chiều một lập luận**: phái Elea nói nếu không có khoảng trống thì không có chuyển động, nên chuyển động là ảo giác. Các nhà nguyên tử dùng đúng câu điều kiện ấy theo chiều ngược lại: chuyển động rõ ràng có, vậy khoảng trống phải có — một phép **modus tollens** (phủ định hậu kiện).",
"**Phẩm chất cảm giác và thực tại**: ngọt, đắng, màu sắc có “theo quy ước”; thực tại chỉ là nguyên tử và khoảng trống. Cái giá: giác quan vừa là lối duy nhất tới sự thật vừa không đáng tin trọn vẹn — mầm mống của **hoài nghi luận** (*skepticism*).",
"**An vui** (*euthymia*): điều tốt nằm ở trạng thái bên trong — tâm hồn bình thản, không sợ hãi — chứ không ở của cải hay vận may.",
],
"argument": {
"title": "Vì sao phải có nguyên tử? Lập luận chia đến cùng",
"intro": "Không còn văn bản nào của Democritus trình bày lập luận này. Aristotle thuật lại nó (*Về sinh thành và hủy diệt* I.2); đây là cách tái dựng phổ biến.",
"premises": [
"Giả sử một vật có thể chia ở mọi điểm. Khi đó không gì ngăn ta hình dung nó đã được chia xong ở mọi điểm.",
"Chia xong, phần còn lại hoặc là những mẩu có độ lớn (như bụi), hoặc là những điểm không có độ lớn, hoặc không còn gì.",
"Nếu còn mẩu có độ lớn thì việc chia chưa xong. Nếu chỉ còn điểm hay hư không thì vật ban đầu được ghép từ những thứ không có độ lớn — mà bao nhiêu cái không có độ lớn gộp lại cũng không thành một vật có độ lớn.",
],
"conclusion": "Vậy việc chia phải dừng ở những hạt nhỏ nhất không thể chia: nguyên tử (*atomos*, “không cắt được”).",
"objection": "Aristotle, người phê bình Democritus kỹ nhất, chỉ ra cái giá của “độ lớn nhỏ nhất”: một hạt nhỏ nhất không có mép nên chẳng thể có hình dạng; nếu nguyên tử không thể đi “được nửa đường” thì chuyển động phải là những bước nhảy rời rạc. Ngoài ra, nếu nguyên tử có kích thước và hình dạng thì ít nhất trong ý nghĩ nó vẫn có nửa trái, nửa phải — tức vẫn chia được.",
"reply": "Người theo thuyết nguyên tử tách hai chuyện. Nguyên tử không thể bị bẻ vỡ vì nó đặc, không có khoảng trống bên trong cho vết cắt đi qua. Epicurus nói rõ hơn: nguyên tử có những “phần tối thiểu” chỉ phân biệt được trong ý nghĩ nhưng không thể tồn tại tách riêng; nhờ vậy nguyên tử vẫn có hình dạng, kích thước khác nhau mà chuỗi chia vô tận vẫn bị chặn lại.",
},
"quote": {
"source": "Democritus, dẫn theo Diogenes Laërtius IX.72 — bản dịch tiếng Anh của R. D. Hicks (1925)",
"orig": "Opinion says hot or cold, but the reality is atoms and empty space. … Of a truth we know nothing, for truth is in a well.",
"vi": "Ý kiến nói nóng hay lạnh, nhưng thực tại là nguyên tử và khoảng trống. … Thật ra ta chẳng biết gì, vì sự thật nằm dưới đáy giếng.",
"url": "https://en.wikisource.org/wiki/Lives_of_the_Eminent_Philosophers/Book_IX",
},
"misread": [
"**“Democritus đã tìm ra nguyên tử của vật lý hiện đại.”** Thực ra nguyên tử của ông là kết luận của lý lẽ, không phải của thí nghiệm, và “không thể chia” theo định nghĩa; nguyên tử của vật lý hiện đại thì chia được.",
"**“Democritus là người vô thần.”** Thực ra không rõ. Ông giải thích hiểu biết về thần linh bằng những “hình ảnh” (*eidōla*) khổng lồ đến từ bên ngoài; học giả còn tranh cãi đó là cách hạ bệ thần linh hay coi chúng là sinh thể có thật.",
],
"related": [
("lich-su/hy-lap-co-dai.md", "Hy Lạp cổ đại: từ thần thoại đến lý trí"),
],
"sources": [
("Berryman, Sylvia, “Democritus”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/democritus/"),
("Berryman, Sylvia, “Ancient Atomism”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/atomism-ancient/"),
("Konstan, David, “Epicurus”, *Stanford Encyclopedia of Philosophy* (mục 3: phê phán của Aristotle và lời đáp của Epicurus).", "https://plato.stanford.edu/entries/epicurus/"),
("Diogenes Laërtius, *Lives of the Eminent Philosophers*, quyển IX, bản dịch R. D. Hicks (1925), Wikisource.", "https://en.wikisource.org/wiki/Lives_of_the_Eminent_Philosophers/Book_IX"),
],
},
"socrates": {
"desc": "Người không viết chữ nào mà thay đổi triết học: hỏi đến cùng những ai tưởng mình biết, và chọn cái chết thay vì thôi hỏi.",
"bio": [
"Hãy hình dung một ông già chân đất, xấu xí, giữa chợ chặn một vị tướng, một nhà thơ nổi tiếng, một chính khách lại hỏi: “Ông nói về lòng can đảm suốt ngày — vậy can đảm là gì?” Hỏi tiếp, hỏi nữa, cho đến khi người kia nhận ra mình không trả lời được. Athens thế kỷ 5 TCN có một người như thế. Ông tên là Socrates, và cuối cùng Athens xử tử ông.",
"Socrates sinh khoảng năm 469 TCN; mẹ ông là bà đỡ, và ông tự ví mình như người đỡ đẻ cho ý tưởng của người khác. Ông từng cầm khiên ra trận cho Athens, và hai lần đứng một mình trước quyền lực: dưới chế độ dân chủ, ông là người duy nhất trong ban chủ tọa phản đối việc xử chung các tướng lĩnh trái luật; dưới chính quyền Ba Mươi, khi được lệnh đi bắt Leon xứ Salamis để xử tử, ông lặng lẽ về nhà. Ông không viết gì; ta biết ông qua Aristophanes, Xenophon và Platon.",
"Theo *Biện hộ* của Platon, bạn ông là Chaerephon từng hỏi đền Delphi có ai khôn ngoan hơn Socrates không, và được trả lời: không ai. Bối rối, ông đi chất vấn chính khách, nhà thơ, thợ thủ công, rồi nhận ra họ không biết mà tưởng mình biết, còn ông thì không biết và cũng không tưởng mình biết. Từ đó ông coi việc hỏi han là sứ mệnh: hỏi người Athens có xấu hổ không khi lo tiền bạc, danh tiếng hơn là sự tốt đẹp của linh hồn.",
"Năm 399 TCN, Meletus cùng Anytus và Lycon kiện ông tội bất kính với thần linh và làm hư hỏng thanh niên. Bồi thẩm đoàn kết tội; ông đề nghị nộp phạt ba mươi mina do bạn bè bảo lãnh nhưng bị bác, và lãnh án tử. Án hoãn chừng một tháng vì chuyến tàu lễ tới đảo Delos; ông từ chối trốn đi rồi uống thuốc độc cần. Cái chết ấy thành “huyền thoại khởi nguồn” của triết học. Platon đưa ông vào hầu hết các đối thoại của mình, phái Khắc kỷ coi ông là mẫu mực; hơn hai nghìn năm sau, Kierkegaard viết luận án về sự mỉa mai của Socrates, còn Nietzsche công kích ông dữ dội.",
],
"works": [
("423 TCN", "Aristophanes, *Nephelai*", "*Mây*: hài kịch giễu Socrates như một kẻ ngụy biện nghiên cứu chuyện trên trời dưới đất — chân dung sớm nhất, vẽ khi ông còn sống"),
("sau 399 TCN", "Platon, *Apologia*, *Euthyphro*, *Crito*, *Phaedo*", "*Biện hộ của Socrates* trước tòa, rồi những ngày cuối: trước phiên tòa, trong tù, lúc uống thuốc độc"),
("sau 399 TCN", "Xenophon, *Memorabilia*", "*Hồi ức về Socrates*: chân dung do một học trò khác ghi lại, khác Socrates của Platon ở nhiều điểm"),
],
"thoughts": [
"**Phép vấn đáp** (*elenchus*): lấy định nghĩa người kia tự tin đưa ra, rút từ chính niềm tin của họ một hệ quả trái với nó. Mục đích không phải thắng cãi mà là gỡ bỏ cái tưởng-là-biết.",
"**Biết giới hạn của mình**: sự khôn ngoan của Socrates chỉ hơn người ở chỗ không tưởng mình biết điều mình không biết. Nhưng ông vẫn dám khẳng định: làm điều bất công là xấu và đáng hổ thẹn (*Biện hộ* 29b).",
"**Chăm lo linh hồn**: sống thế nào cho đúng quan trọng hơn tiền bạc và danh tiếng; vì thế “cuộc đời không được xem xét thì không đáng sống” (*Biện hộ* 38a).",
],
"argument": {
"title": "Thế lưỡng nan Euthyphro",
"intro": "Trong *Euthyphro* của Platon (10a–11b), ngay trước phiên tòa, Euthyphro định nghĩa **mộ đạo** (*piety*, *hosion*) là “điều được mọi vị thần yêu”. Socrates hỏi: các thần yêu điều mộ đạo vì nó mộ đạo, hay nó mộ đạo vì được các thần yêu?",
"premises": [
"Euthyphro chấp nhận vế đầu: các thần yêu điều mộ đạo *vì* nó mộ đạo.",
"Còn một thứ “được thần yêu” là *vì* các thần yêu nó: việc yêu có trước, việc được yêu theo sau.",
"Nếu “mộ đạo” chỉ có nghĩa là “được mọi thần yêu”, thì thay vào P1 ta được: các thần yêu điều được-thần-yêu vì nó được-thần-yêu — trái với P2.",
],
"conclusion": "Vậy “được mọi thần yêu” chỉ là một đặc điểm đi kèm của điều mộ đạo, chưa phải bản chất của nó: ta vẫn chưa biết mộ đạo là gì.",
"objection": "Người theo **thuyết mệnh lệnh thần linh** (*divine command theory*) cho rằng Euthyphro nhượng bộ sai chỗ: cứ nhận vế sau — điều đúng là đúng vì Thượng đế muốn — thì định nghĩa vẫn đứng. Bản hiện đại của Robert Adams chỉ nói *nghĩa vụ* đạo đức phụ thuộc vào mệnh lệnh của một Thượng đế công bằng và nhân từ, nên mệnh lệnh không tùy tiện.",
"reply": "Người theo hướng Socrates hỏi tiếp: nếu “thiện” chỉ có nghĩa là “được Thượng đế muốn” thì câu “Thượng đế là thiện” gần như rỗng — Ngài chỉ sống đúng chuẩn do chính Ngài đặt ra. Còn nếu Thượng đế đáng tôn kính vì Ngài công bằng và nhân từ, thì công bằng và nhân từ đã là chuẩn mực có trước mệnh lệnh; ta vẫn phải tự hỏi điều thiện là gì.",
},
"quote": {
"source": "Platon, *Biện hộ của Socrates* 38a — bản dịch tiếng Anh của Benjamin Jowett",
"orig": "…daily to discourse about virtue, and of those other things about which you hear me examining myself and others, is the greatest good of man, and that the unexamined life is not worth living…",
"vi": "…mỗi ngày bàn luận về đức hạnh và về những điều khác mà các vị nghe tôi xem xét chính mình và người khác, là điều tốt đẹp nhất cho con người, và cuộc đời không được xem xét thì không đáng sống…",
"url": "https://www.gutenberg.org/ebooks/1656",
},
"misread": [
"**“Socrates nói: tôi chỉ biết một điều là tôi không biết gì.”** Thực ra câu gọn như châm ngôn ấy không có trong *Biện hộ*. Socrates của Platon nói: người kia không biết mà tưởng mình biết, còn ông không biết và cũng không tưởng mình biết (21d). Ông vẫn tự tin khẳng định nhiều điều, chẳng hạn tri thức khác với ý kiến đúng (*Meno* 98b).",
"**“Đọc Platon là biết Socrates nghĩ gì.”** Thực ra Socrates của Aristophanes, của Xenophon và của Platon khác nhau đáng kể; tách Socrates lịch sử khỏi nhân vật văn chương là “vấn đề Socrates” mà học giả còn tranh luận. Nhiều người cho rằng các đối thoại thời kỳ đầu gần Socrates thật hơn — một giả thuyết, không phải sự kiện.",
],
"related": [
("doc/platon-bien-ho.md", "Đọc “Biện hộ của Socrates” (Platon)"),
("cong-cu/bien-chung-socrates.md", "Phép biện chứng Socrates"),
("cau-hoi/sieu-dao-duc.md", "Đúng sai có khách quan không?"),
("cong-cu/dinh-nghia-phan-vi-du.md", "Thế nào là một định nghĩa tốt?"),
("lich-su/hy-lap-co-dai.md", "Hy Lạp cổ đại: từ thần thoại đến lý trí"),
],
"sources": [
("Nails, Debra & S. Sara Monoson, “Socrates”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/socrates/"),
("Platon, *Apology*, bản dịch Benjamin Jowett, Project Gutenberg.", "https://www.gutenberg.org/ebooks/1656"),
("Platon, *Euthyphro*, bản dịch Benjamin Jowett, Project Gutenberg.", "https://www.gutenberg.org/ebooks/1642"),
("Platon, *Theaetetus*, bản dịch Benjamin Jowett, Project Gutenberg.", "https://www.gutenberg.org/ebooks/1726"),
("Murphy, Mark, “Theological Voluntarism”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/voluntarism-theological/"),
],
},
"platon": {
"desc": "Học trò của Socrates, người lập Học viện và viết triết học thành đối thoại; nổi tiếng với thuyết Ý niệm, ẩn dụ hang động và giấc mơ “triết vương”.",
"bio": [
"Năm 399 TCN, Platon chừng gần ba mươi tuổi. Ông có mặt ở phiên tòa xử Socrates, là một trong những người bạn xin bảo lãnh tiền phạt cho thầy, và chứng kiến Athens kết án tử người mà *Phaedo* gọi là “khôn ngoan nhất, công chính nhất và tốt nhất” trong những người cùng thời. Hôm thầy uống thuốc độc, theo chính *Phaedo*, Platon ốm không đến được. Có lẽ không ngẫu nhiên mà câu hỏi lớn trong các tác phẩm của ông là: phải sống và tổ chức thành bang thế nào để công lý không thua ý kiến đám đông?",
"Platon sinh khoảng năm 428 TCN trong một gia đình quyền thế ở Athens; tên thật có lẽ là Aristocles, còn “Platon” (gần với *platos*, “rộng”) tương truyền là biệt danh. Sau cái chết của thầy, ông rời Athens một thời gian, rồi trở về lập trường học trong khu vườn thờ anh hùng Academus ở ngoại ô — chữ “academic” bắt nguồn từ đó. Học viện là nhà của ông đến cuối đời; Aristotle học ở đây hai mươi năm. Theo *Bức thư thứ bảy*, văn bản mà học giả còn tranh cãi có phải của ông không, Platon từng ba lần sang Syracuse ở Sicily, mong giúp một bạo chúa trở thành người cai trị hiểu triết học; lần nào cũng thất bại, có lần ông bị giam lỏng.",
"Platon viết triết học thành đối thoại và gần như không bao giờ tự nói bằng giọng mình: Socrates thường là người dẫn dắt, người đọc phải tự cân nhắc lý lẽ. Ông đặt ra phần lớn những câu hỏi lớn của triết học phương Tây: tri thức là gì, công lý là gì, linh hồn có bất tử không, ai nên cai trị. Câu trả lời nổi tiếng nhất của ông là thuyết **Ý niệm** (*Forms*): bên trên những vật đẹp, vật bằng nhau, việc công bằng mà ta gặp, có cái Đẹp, cái Bằng, cái Công bằng tự thân — bất biến, chỉ trí tuệ nắm bắt được.",
"Richard Kraut viết rằng triết học, hiểu như sự khảo sát chặt chẽ, có hệ thống các vấn đề đạo đức, chính trị, siêu hình học và tri thức luận, “có thể gọi là phát minh của Platon”. Học trò Aristotle phản bác ông; Augustine đọc ông qua phái Tân Platon để diễn đạt đức tin Kitô giáo; thế kỷ 20, Karl Popper buộc tội *Cộng hòa* là mầm mống của chủ nghĩa toàn trị. Khi tranh luận nên giao quyền cho chuyên gia hay số đông, hay hỏi con số có tồn tại độc lập với con người không, ta vẫn đang nói chuyện với Platon.",
],
"works": [
("", "*Euthyphro*", "mộ đạo là gì? — nơi xuất hiện thế lưỡng nan Euthyphro"),
("", "*Phaedo*", "ngày cuối của Socrates; các lập luận về linh hồn bất tử và về Ý niệm"),
("", "*Symposium*", "*Bữa tiệc*: tình yêu như nấc thang dẫn tới cái Đẹp tự thân"),
("", "*Politeia*", "*Cộng hòa*: công lý trong linh hồn và thành bang, triết vương, ẩn dụ hang động"),
("", "*Parmenides*", "Platon tự đưa ra những phản bác sắc nhất với thuyết Ý niệm"),
],
"thoughts": [
"**Ý niệm và vật cảm giác**: vật đẹp thì đẹp mặt này mà xấu mặt khác, đẹp hôm nay mà tàn ngày mai; cái Đẹp tự thân thì không. Vật cảm giác “tham dự” vào Ý niệm, như cái bóng so với vật thật.",
"**Tri thức khác ý kiến đúng**: ý kiến đúng như những pho tượng của Daedalus, không buộc lại thì “bỏ chạy”; nó chỉ thành tri thức khi được buộc chặt bằng lời giải thích lý do (*Meno* 97d–98a).",
"**Công lý là sự hài hòa**: theo *Cộng hòa*, linh hồn có ba phần — lý trí, khí phách, ham muốn; người công chính giữ cho mỗi phần làm đúng việc của nó, hòa với nhau như các nốt nhạc, dưới sự dẫn dắt của lý trí.",
"**Triết vương**: chừng nào triết gia chưa làm vua, hoặc vua chưa thật sự học triết, thì thành bang không dứt được tai họa (*Cộng hòa* 473c–d).",
],
"argument": {
"title": "Vì sao phải có Ý niệm?",
"intro": "Platon rải lập luận này qua nhiều đối thoại (*Phaedo*, *Cộng hòa* V và X). Đây là cách tái dựng phổ biến, xoay quanh nguyên tắc “một trên nhiều”.",
"premises": [
"Khi nhiều vật cùng mang một tên — “đẹp”, “bằng nhau”, “công bằng” — chúng có chung một cái gì đó làm cho chúng như thế (*Cộng hòa* X, 596a).",
"Không vật cảm giác nào là cái chung ấy: vật đẹp nào cũng xấu xét theo một mặt khác, việc công bằng nào cũng có lúc thành bất công (*Cộng hòa* V, 479a).",
"Cái làm cho mọi vật đẹp thì phải đẹp trọn vẹn, không pha lẫn cái xấu.",
],
"conclusion": "Vậy có cái Đẹp tự thân — một Ý niệm — khác với mọi vật đẹp và hoàn hảo hơn chúng.",
"objection": "Lập luận “con người thứ ba”, do chính Platon nêu trong *Parmenides* (132a–b) và được Aristotle đặt tên: nếu cái Đẹp tự thân cũng đẹp (P3), nó cùng các vật đẹp lập thành một nhóm vật đẹp mới; theo P1 lại cần một Ý niệm Đẹp thứ hai đứng trên nhóm ấy, rồi thứ ba, thứ tư… vô tận. Mỗi Ý niệm không còn là “một”.",
"reply": "Các nhà bình giải chỉ ra hai giả định ngầm: Ý niệm Đẹp “đẹp” theo đúng nghĩa một bông hoa đẹp, và Ý niệm không bao giờ đồng nhất với cái tham dự vào nó. Bỏ một trong hai — chẳng hạn hiểu “cái Đẹp là đẹp” như một câu về bản chất của sự đẹp, không như “bông hoa là đẹp” — thì cái Đẹp không gia nhập nhóm vật đẹp, và chuỗi vô tận không khởi động.",
},
"quote": {
"source": "Platon, *Cộng hòa* X, 596a — bản dịch tiếng Anh của Benjamin Jowett",
"orig": "Whenever a number of individuals have a common name, we assume them to have also a corresponding idea or form.",
"vi": "Hễ nhiều cá thể có chung một tên gọi, ta giả định rằng chúng cũng có một ý niệm hay mô thức tương ứng.",
"url": "https://www.gutenberg.org/ebooks/1497",
},
"misread": [
"**“Mọi điều Socrates nói trong đối thoại đều là quan điểm của Platon.”** Thực ra Platon không bao giờ phát biểu bằng giọng mình trong đối thoại; ông để các nhân vật lập luận, phản bác, có khi bế tắc. Muốn biết Platon nghĩ gì, phải đọc cả cuộc đối thoại.",
"**“Platon coi thế giới cảm giác là ảo ảnh vô giá trị.”** Thực ra nó “kém thật” hơn Ý niệm, như cái bóng so với vật, nhưng không vô nghĩa. Trong *Cộng hòa* (519d), người đã ra khỏi hang còn bị buộc phải quay xuống, chia sẻ việc khó nhọc với những người còn trong hang.",
],
"related": [
("doc/platon-hang-dong.md", "Đọc ẩn dụ hang động (Platon, “Cộng hòa” VII)"),
("cau-hoi/pho-quat.md", "Cái đỏ của hoa hồng và cái đỏ của máu: phổ quát có thật không?"),
("cau-hoi/cai-gi-ton-tai.md", "Cái gì thực sự tồn tại?"),
("cau-hoi/ai-nen-cai-tri.md", "Ai nên cai trị: số đông hay người hiểu biết?"),
("cau-hoi/tinh-yeu.md", "Tình yêu là gì?"),
],
"sources": [
("Kraut, Richard, “Plato”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/plato/"),
("Brickhouse, Thomas & Nicholas D. Smith, “Plato”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/plato/"),
("Rickless, Samuel, “Plato’s Parmenides”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/plato-parmenides/"),
("Brown, Eric, “Plato’s Ethics and Politics in The Republic”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/plato-ethics-politics/"),
("Platon, *The Republic*, bản dịch Benjamin Jowett, Project Gutenberg.", "https://www.gutenberg.org/ebooks/1497"),
("Platon, *Phaedo*, bản dịch Benjamin Jowett, Project Gutenberg.", "https://www.gutenberg.org/ebooks/1658"),
],
},
"aristotle": {
"desc": "Học trò hai mươi năm của Platon rồi thành người phê bình ông; đặt nền cho logic học, sinh học và đạo đức học đức hạnh.",
"bio": [
"Người Việt quen câu “một con én không làm nên mùa xuân”. Câu ấy có trong một cuốn sách đạo đức viết hơn hai nghìn ba trăm năm trước, để nói rằng một ngày vui chưa làm nên một đời hạnh phúc. Tác giả của nó, Aristotle, đã viết về gần như mọi lĩnh vực tri thức thời mình: logic, vật lý, sinh học, tâm lý học, đạo đức, chính trị, tu từ và thi ca.",
"Aristotle sinh năm 384 TCN ở Stagira, miền bắc Hy Lạp; cha ông là thầy thuốc của vua xứ Macedonia. Khoảng mười bảy tuổi, ông đến Athens học ở Học viện của Platon và ở lại hai mươi năm, đến khi thầy mất (347 TCN). Sau đó ông sang Assos, rồi đảo Lesbos, cùng Theophrastus miệt mài quan sát sinh vật, nhất là sinh vật biển. Năm 343 TCN, vua Philip mời ông dạy cậu con trai mười ba tuổi Alexander — về sau là Alexander Đại đế — dù thực ra ta biết rất ít về những bài học ấy. Năm 335 TCN, ông trở lại Athens lập trường Lyceum; học trò ông được gọi là phái Peripatetic, có lẽ theo tên lối đi có mái (*peripatos*) trong trường.",
"Khi Alexander mất năm 323 TCN, làn sóng chống Macedonia nổi lên ở Athens. Aristotle rời thành phố — tương truyền ông nói không muốn để Athens “phạm tội với triết học lần thứ hai”, ám chỉ cái chết của Socrates — và mất năm sau ở Chalcis. Ông để lại có lẽ tới hai trăm chuyên luận, nay còn khoảng ba mươi mốt; phần lớn là bài giảng và bản nháp cho học trò, nên khô và khó đọc hơn hẳn đối thoại của Platon.",
"Aristotle là học trò lớn nhất và cũng là người phê bình sắc nhất của Platon: với ông, cái phổ quát không nằm ở một thế giới Ý niệm riêng mà ở ngay trong sự vật. Hơn một nghìn năm sau, tác phẩm của ông thành nền cho triết học Hồi giáo (Avicenna, Averroes — người mà châu Âu gọi là “Nhà bình giải”), Do Thái giáo (Maimonides) và Kitô giáo (Thomas Aquinas, người gọi ông đơn giản là “Nhà triết học”). Từ cuối thập niên 1950, đạo đức học đức hạnh hồi sinh, phần lớn theo hướng của ông.",
],
"works": [
("", "*Organon*", "các khảo luận logic (*Categoriae*, *Analytica Priora*…), trong đó có lý thuyết tam đoạn luận"),
("", "*Physica*", "*Vật lý học*: tự nhiên, chuyển động, bốn nguyên nhân"),
("", "*Metaphysica*", "*Siêu hình học*: bản thể; quyển I điểm lại các triết gia đi trước, bắt đầu từ Thales"),
("", "*Ethica Nicomachea*", "*Đạo đức Nicomachus*: hạnh phúc, đức hạnh, trung dung, tình bạn"),
("", "*Politica*", "*Chính trị học*: con người “tự bản tính là động vật chính trị”"),
],
"thoughts": [
"**Logic hình thức**: lần đầu tiên, suy luận được nghiên cứu theo hình thức, độc lập với nội dung — **tam đoạn luận** (*syllogism*) kiểu “mọi A là B, mọi B là C, vậy mọi A là C” đúng dù A, B, C là gì.",
"**Bốn nguyên nhân**: muốn hiểu một vật, hỏi bốn câu — làm bằng gì, có hình thức gì, do đâu mà có, để làm gì. Con dao: thép, hình dạng lưỡi, người thợ rèn, để cắt.",
"**Hình thức ở trong vật**: không cần một thế giới Ý niệm riêng; cái phổ quát chỉ có trong các vật riêng. Aristotle cũng là người đặt tên cho một phản bác nổi tiếng với Platon: lập luận “con người thứ ba”.",
"**Trung dung**: đức hạnh nằm giữa hai thái cực — can đảm giữa hèn nhát và liều lĩnh — nhưng là “giữa đối với ta”, tùy người tùy cảnh, không phải trung bình cộng.",
],
"argument": {
"title": "Chức năng của con người",
"intro": "Hạnh phúc (*eudaimonia*) là gì? Trong *Đạo đức Nicomachus* I.7 (1097b–1098a), Aristotle trả lời bằng lập luận về **chức năng** (*ergon*, có khi dịch là “công năng”).",
"premises": [
"Với mọi thứ có một chức năng — người thổi sáo, nhà điêu khắc, con mắt, bàn tay — cái tốt của nó nằm ở việc thực hiện tốt chức năng ấy.",
"Con người cũng có chức năng riêng: thợ mộc, thợ giày còn có việc của mình, lẽ nào con người sinh ra mà không có việc gì?",
"Chức năng riêng ấy không phải sống hay cảm giác (cây cỏ, súc vật cũng có), mà là hoạt động của linh hồn theo lý trí.",
"Thực hiện tốt một chức năng là thực hiện nó theo đức hạnh, tức sự xuất sắc (*aretē*).",
],
"conclusion": "Vậy cái tốt cho con người là hoạt động của linh hồn theo đức hạnh — và trong cả một đời trọn vẹn.",
"objection": "Tiền đề 2 là chỗ yếu: con mắt có chức năng vì nó phục vụ cơ thể, người thợ có chức năng vì vai trò trong xã hội; còn “con người” nói chung thì phục vụ cái gì? Bernard Williams (1985) và nhiều người khác cho rằng câu trả lời của Aristotle dựa vào một **mục đích luận** (*teleology*) về tự nhiên mà khoa học hiện đại không còn chấp nhận.",
"reply": "Những người theo Aristotle hiện đại như Philippa Foot, Rosalind Hursthouse đáp: không cần một vũ trụ có mục đích. Nói một con voi sống tốt hay không là nhận định dựa trên sự thật sinh học về loài voi; nói về con người cũng vậy. Ta là động vật xã hội biết suy nghĩ, nên sống tốt với ta gắn với việc dùng lý trí và các đức tính như công bằng, can đảm, rộng lượng.",
},
"quote": {
"source": "Aristotle, *Đạo đức Nicomachus* I.7 (1098a) — bản dịch tiếng Anh của D. P. Chase",
"orig": "…for as it is not one swallow or one fine day that makes a spring, so it is not one day or a short time that makes a man blessed and happy.",
"vi": "…vì như một con én hay một ngày đẹp trời không làm nên mùa xuân, một ngày hay một thời gian ngắn cũng không làm cho con người được phúc và hạnh phúc.",
"url": "https://www.gutenberg.org/ebooks/8438",
},
"misread": [
"**“Trung dung là ba phải, việc gì cũng chọn điểm giữa.”** Thực ra “giữa” của Aristotle tương đối với người và hoàn cảnh; và ông nói rõ có những việc không có mức vừa phải nào — ngoại tình, trộm cắp, giết người thì làm bao nhiêu cũng sai (*Đạo đức Nicomachus* II.6).",
"**“Hạnh phúc theo Aristotle là cảm giác vui vẻ.”** Thực ra *eudaimonia* là sống tốt và làm tốt, một hoạt động trải dài cả đời, không phải một tâm trạng. Người chỉ thấy vui mà sống tệ thì với ông chưa thể gọi là hạnh phúc.",
],
"related": [
("doc/aristotle-dao-duc.md", "Hướng dẫn đọc Đạo đức Nicomachus (quyển I–II)"),
("cau-hoi/dao-duc-hanh-dong.md", "Hành động đúng là gì? Ba lý thuyết lớn của đạo đức học"),
("cau-hoi/ban-tinh-con-nguoi.md", "Bản tính con người thiện hay ác?"),
("cau-hoi/trach-nhiem.md", "Ta có đáng bị trách không?"),
("cau-hoi/dinh-menh.md", "Mọi thứ đã được viết sẵn?"),
],
"sources": [
("Shields, Christopher, “Aristotle”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/aristotle/"),
("Kraut, Richard, “Aristotle’s Ethics”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/aristotle-ethics/"),
("Hursthouse, Rosalind & Glen Pettigrove, “Virtue Ethics”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/ethics-virtue/"),
("Aristotle, *The Nicomachean Ethics*, bản dịch D. P. Chase, Project Gutenberg.", "https://www.gutenberg.org/ebooks/8438"),
("Aristotle, *Politics*, bản dịch William Ellis, Project Gutenberg.", "https://www.gutenberg.org/ebooks/6762"),
("Diogenes Laërtius, *Lives of the Eminent Philosophers*, quyển V, bản dịch R. D. Hicks (1925), Wikisource.", "https://en.wikisource.org/wiki/Lives_of_the_Eminent_Philosophers/Book_V"),
],
},
"epicurus": {
"desc": "Người thầy của Khu Vườn: hạnh phúc là thân không đau, tâm không xao động; triết học là thuốc chữa nỗi sợ thần linh và nỗi sợ cái chết.",
"bio": [
"“Gửi cho tôi một hũ pho mát nhỏ, để khi nào muốn, tôi có thể ăn một bữa thịnh soạn.” Người viết dòng ấy là Epicurus — cái tên mà tiếng Anh nay mượn để gọi người sành ăn, ham hưởng thụ (*epicure*). Nghịch lý là chính ông tự nhận bằng lòng với bánh mì và nước lã; với ông, một miếng pho mát đã là yến tiệc.",
"Epicurus sinh năm 341 TCN trên đảo Samos, trong một gia đình công dân Athens định cư ở đó. Mười tám tuổi ông về Athens, rồi sang Colophon học với Nausiphanes, một người theo Democritus. Ông dạy học ở Mytilene và Lampsacus, rồi năm 307/306 TCN trở lại Athens, mua một ngôi nhà có vườn giá tám mươi mina. “Khu Vườn” thành tên trường: bạn bè từ khắp nơi đến sống chung, đạm bạc, có cả phụ nữ và người nô lệ của ông. Ông tin rằng trong mọi thứ sự khôn ngoan đem lại cho một đời hạnh phúc, quý nhất là tình bạn.",
"Triết học của Epicurus là một liều thuốc. Ông thấy nỗi khổ lớn nhất của con người đến từ hai nỗi sợ: sợ thần linh trừng phạt và sợ cái chết. Thuốc chữa là hiểu đúng tự nhiên: mọi thứ là nguyên tử và khoảng trống; thần linh có, nhưng chẳng bận tâm đến chuyện người; linh hồn tan rã cùng thân xác. Còn hạnh phúc là thân không đau, tâm không xao động — đạt được bằng cách phân biệt ham muốn tự nhiên, cần thiết với những ham muốn rỗng như khao khát vương miện hay tượng đài vinh danh.",
"Năm 270 TCN, sau hai tuần đau đớn vì sỏi thận, ông viết cho bạn: “Vào ngày hạnh phúc này, cũng là ngày cuối đời tôi…”, rằng nỗi đau thân xác được bù lại bằng niềm vui khi nhớ những cuộc trò chuyện cũ; di chúc của ông dặn lo cho con cái của bạn bè. Trường phái ông tồn tại nhiều thế kỷ; nhà thơ La Mã Lucretius viết cả một trường ca để truyền bá nó, và hoàng đế Khắc kỷ Marcus Aurelius vẫn trích lời ông với thiện cảm. Giữa một thời lo âu vì áp lực thành công và mạng xã hội, câu hỏi của ông vẫn đáng hỏi: ta thật sự cần gì để sống yên?",
],
"works": [
("", "*Peri physeōs*", "*Về tự nhiên*: bộ bài giảng 37 cuộn; chỉ còn những mảnh giấy cói cháy dở tìm thấy ở Herculaneum, thành phố bị núi lửa Vesuvius vùi năm 79"),
("", "*Letter to Herodotus*", "*Thư gửi Herodotus*: tóm tắt vật lý học nguyên tử, chép trong Diogenes Laërtius quyển X"),
("", "*Letter to Menoeceus*", "*Thư gửi Menoeceus*: đạo đức học trong vài trang — thần linh, cái chết, ham muốn, khoái lạc"),
("", "*Kuriai doxai*", "*Những học thuyết chính*: các châm ngôn cốt lõi để ghi nhớ; một tuyển tập khác, *Châm ngôn Vatican*, còn trong một bản chép tay riêng"),
],
"thoughts": [
"**Khoái lạc hiểu đúng**: mục đích là thân không đau (*aponia*), tâm không xao động (*ataraxia*). Vì thế có lúc phải bỏ qua một khoái lạc kéo theo phiền toái lớn hơn, hay chịu một nỗi đau nhỏ để tránh nỗi đau lớn (*Thư gửi Menoeceus* 129).",
"**Ba loại ham muốn**: tự nhiên và cần thiết (uống khi khát), tự nhiên mà không cần thiết (món ăn đắt tiền), và không tự nhiên cũng không cần thiết, sinh từ ảo tưởng (vương miện, tượng đài). Hạnh phúc dễ hơn ta tưởng nếu biết phân loại (*Những học thuyết chính* 29).",
"**Thần linh không can thiệp**: thần linh có, nhưng không như đám đông tin; kẻ bất kính thật sự là người gán cho thần những điều đám đông nghĩ về họ (*Thư gửi Menoeceus* 123).",
"**Triết học là thuốc**: “không tuổi nào là quá sớm hay quá muộn để chăm lo sức khỏe của tâm hồn” (*Thư gửi Menoeceus* 122).",
],
"argument": {
"title": "Chết không là gì với ta",
"intro": "Trong *Thư gửi Menoeceus* (124–125), Epicurus muốn gỡ nỗi sợ lớn nhất của con người. Đây là lập luận của ông ở dạng chuẩn.",
"premises": [
"Mọi điều tốt và xấu đều nằm ở cảm giác: chỉ cái gì ta cảm nhận được mới có thể tốt hay xấu cho ta.",
"Chết là mất hết mọi cảm giác.",
"Khi ta còn thì cái chết chưa đến; khi cái chết đến thì ta không còn.",
],
"conclusion": "Vậy cái chết không là gì với ta; sợ nó chỉ là một nỗi đau vô cớ trong lúc chờ đợi.",
"objection": "Thomas Nagel (bài “Death”, 1970) chỉ ra một lỗ hổng ở P1: một điều có thể xấu cho ta không phải vì nó gây cảm giác đau, mà vì nó **tước đi** (*deprive*) những điều tốt ta lẽ ra còn có. Cái chết lấy đi mọi buổi sáng, mọi cuộc trò chuyện còn lại; vì thế chết trẻ bi thảm hơn chết già.",
"reply": "Người theo Epicurus hỏi lại: tước đoạt *của ai*, và *vào lúc nào*? Khi ta còn sống thì chưa mất gì; khi đã chết thì không còn ai để bị mất. Lucretius thêm lập luận đối xứng: ta không khổ vì khoảng thời gian vô tận trước khi sinh ra, vậy cớ gì sợ khoảng vô tận sau khi chết?",
},
"quote": {
"source": "Epicurus, *Thư gửi Menoeceus* 125, chép trong Diogenes Laërtius X — bản dịch tiếng Anh của R. D. Hicks (1925)",
"orig": "Death, therefore, the most awful of evils, is nothing to us, seeing that, when we are, death is not come, and, when death is come, we are not.",
"vi": "Vậy cái chết, điều đáng sợ nhất trong mọi điều xấu, chẳng là gì với ta, bởi khi ta còn thì cái chết chưa đến, và khi cái chết đến thì ta không còn.",
"url": "https://en.wikisource.org/wiki/Lives_of_the_Eminent_Philosophers/Book_X",
},
"misread": [
"**“Epicurus cổ vũ ăn chơi hưởng lạc.”** Thực ra ông viết rõ: khi nói khoái lạc là mục đích, ông không nói đến khoái lạc của kẻ phóng đãng hay của tiệc tùng, mà là thân không đau, tâm không rối (*Thư gửi Menoeceus* 131–132). Nguồn vui lớn nhất với ông là tình bạn và suy nghĩ tỉnh táo.",
"**“Epicurus là người vô thần.”** Thực ra ông khẳng định thần linh có thật; ông chỉ phủ nhận rằng thần bận tâm trừng phạt hay ban thưởng con người — và vì thế, theo ông, ta không cần sợ thần.",
],
"related": [
("cau-hoi/cai-chet.md", "Chết có đáng sợ không?"),
("cau-hoi/hanh-phuc.md", "Hạnh phúc là gì?"),
("lich-su/hy-lap-co-dai.md", "Hy Lạp cổ đại: từ thần thoại đến lý trí"),
],
"sources": [
("Konstan, David, “Epicurus”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/epicurus/"),
("Luper, Steven, “Death”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/death/"),
("Diogenes Laërtius, *Lives of the Eminent Philosophers*, quyển X (có ba bức thư và *Những học thuyết chính*), bản dịch R. D. Hicks (1925), Wikisource.", "https://en.wikisource.org/wiki/Lives_of_the_Eminent_Philosophers/Book_X"),
("Nagel, Thomas, “Death”, *Noûs* 4 (1970): 73–80.", "https://doi.org/10.2307/2214297"),
],
},
"zeno": {
"desc": "Thương nhân đắm tàu trở thành người sáng lập phái Khắc kỷ: sống phù hợp với tự nhiên; chỉ đức hạnh là điều thiện, mọi thứ khác “không thiện không ác”.",
"bio": [
"Khoảng ba mươi tuổi, một thương nhân người Citium bị đắm tàu trên đường chở thuốc nhuộm tím từ Phoenicia tới cảng Piraeus. Lên Athens, ông ngồi trong một hiệu sách đọc quyển II cuốn *Hồi ức về Socrates* của Xenophon, say mê đến mức hỏi: tìm đâu ra những người như thế? Đúng lúc ấy triết gia Crates đi ngang, người bán sách chỉ tay: “Hãy theo ông ấy.” Về sau Zeno nói: “Tôi đã có một chuyến đi suôn sẻ khi bị đắm tàu.” Chuyện do Diogenes Laërtius chép, có nhiều dị bản, nhưng nó tóm được tinh thần của người sáng lập phái Khắc kỷ: biến tai họa thành dịp học.",
"Citium là một thành phố Hy Lạp trên đảo Cyprus, có người Phoenicia đến định cư; Crates gọi đùa Zeno là “anh chàng Phoenicia nhỏ”. Ông học Crates phái Khuyển nho, rồi Stilpo phái Megara, Xenocrates và Polemo ở Học viện, cùng nhà biện chứng Diodorus Cronus. Khoảng năm 300 TCN, ông bắt đầu giảng dạy, vừa nói vừa đi lại dưới Stoa Poikile, “hành lang vẽ” bên khu chợ Athens. Học trò ông thoạt tiên được gọi là “người theo Zeno”, sau thành “người của Stoa” — phái Khắc kỷ.",
"Ông sống đạm bạc mà được Athens kính trọng: người ta gửi ông chìa khóa tường thành, tặng vương miện vàng, xây mộ cho ông ở Kerameikos bằng tiền công, với lời tuyên dương rằng ông khuyên thanh niên sống đức hạnh, tiết độ và lấy chính đời mình làm gương, hoàn toàn khớp với lời dạy. Theo học trò Persaeus, ông mất năm bảy mươi hai tuổi; Diogenes Laërtius chép một con số khác: chín mươi tám.",
"Không tác phẩm nào của Zeno còn nguyên; ta biết ông qua lời trích và lời kể. Nhưng ông đã dựng bộ khung mà phái Khắc kỷ giữ gần năm thế kỷ: triết học gồm logic, vật lý và đạo đức; mục đích đời người là sống phù hợp với tự nhiên; chỉ đức hạnh là điều thiện. Cleanthes, rồi Chrysippus hệ thống hóa học thuyết; ở La Mã, Seneca, Epictetus và Marcus Aurelius làm nó sống lại. Ngày nay nhiều người tìm đến Khắc kỷ để giữ bình tĩnh giữa áp lực, phần lớn qua những người đến sau ấy — còn nền móng là của Zeno.",
],
"works": [
("", "*Politeia*", "*Cộng hòa*: viết khi còn theo Crates; người đương thời đùa là viết “trên đuôi chó”, ý nói còn đậm chất Khuyển nho (Diogenes Laërtius VII.4); đã mất"),
("", "*On the Nature of Man*", "*Về bản tính con người*: theo Diogenes Laërtius (VII.87), nơi Zeno lần đầu gọi mục đích đời người là “sống phù hợp với tự nhiên”; đã mất"),
("1903–1905", "von Arnim, *Stoicorum Veterum Fragmenta*, tập I", "bộ sưu tập chuẩn các mảnh văn và lời thuật lại về Zeno và học trò"),
],
"thoughts": [
"**Ba phần của triết học**: logic, vật lý, đạo đức gắn với nhau; từ Zeno trở đi, phái Khắc kỷ học cả ba, vì sống tốt cần hiểu đúng thế giới và lập luận đúng.",
"**Sống phù hợp**: theo Stobaeus, Zeno nói mục đích là “sống phù hợp” — theo một lý lẽ nhất quán, không giằng xé; Diogenes Laërtius chép rằng ông nói “sống phù hợp với tự nhiên”, tức sống theo đức hạnh.",
"**Chỉ đức hạnh là điều thiện**: sức khỏe, của cải, danh tiếng “không thiện không ác” (*adiaphora*), dù có thứ “được ưu tiên”. Đó là chỗ Zeno dung hòa Polemo của Học viện (có những điều tốt bên ngoài) với Stilpo phái Megara (không gì bên ngoài là tốt hay xấu).",
"**Lập luận gọn và phép nhại**: Zeno thích những tam đoạn luận ngắn như “cái biết suy luận tốt hơn cái không biết suy luận; không gì tốt hơn vũ trụ; vậy vũ trụ biết suy luận”. Cicero, qua nhân vật Cotta, nhại lại: theo kiểu ấy thì vũ trụ cũng biết đọc sách. Giữ cấu trúc, thay nội dung — một cách thử lập luận.",
],
"argument": {
"title": "Sức khỏe và tiền bạc không phải là điều thiện",
"intro": "Zeno không để lại văn bản trình bày lập luận này; Diogenes Laërtius (VII.102–103) chép nó như học thuyết chung của các nhà Khắc kỷ thời đầu, dựng trên luận điểm của Zeno.",
"premises": [
"Cái thật sự tốt thì tự bản chất luôn đem lại lợi ích, như cái nóng luôn làm ấm, không bao giờ làm lạnh.",
"Của cải và sức khỏe có thể dùng vào việc tốt lẫn việc xấu: chúng không đem lại lợi ích nhiều hơn tác hại.",
"Chỉ đức hạnh — sự khôn ngoan biết dùng mọi thứ cho đúng — là luôn đem lại lợi ích.",
],
"conclusion": "Vậy của cải, sức khỏe, danh tiếng không phải điều thiện mà “không thiện không ác” (dù vẫn “được ưu tiên”); chỉ đức hạnh là thiện.",
"objection": "Các nhà phê bình thời cổ thuộc Học viện và phái Peripatetic cho rằng đây chỉ là trò đổi tên: nếu sức khỏe “có giá trị”, “được ưu tiên” và người khôn ngoan theo đuổi nó, thì nó là một điều tốt bên ngoài mang tên mới. Và khó tin rằng một người đức hạnh bị tra tấn vẫn hạnh phúc trọn vẹn — điều Aristotle cho là không ai chấp nhận nổi.",
"reply": "Người Khắc kỷ đáp: khác biệt nằm ở cách sống, không ở chữ. Người khôn ngoan chọn sức khỏe vì đó là lựa chọn hợp lý, nhưng kết quả — thật sự khỏe hay không — không làm đời họ tốt hay xấu hơn; như người múa giỏi, điều đáng kể là múa đúng, không phải thứ gì giành được bên ngoài. Vì thế mất sức khỏe hay của cải không lấy đi hạnh phúc của họ.",
},
"quote": {
"source": "Diogenes Laërtius, *Lives of the Eminent Philosophers* VII.87 — bản dịch tiếng Anh của R. D. Hicks (1925)",
"orig": "This is why Zeno was the first (in his treatise On the Nature of Man) to designate as the end “life in agreement with nature” (or living agreeably to nature), which is the same as a virtuous life, virtue being the goal towards which nature guides us.",
"vi": "Vì thế Zeno là người đầu tiên (trong chuyên luận *Về bản tính con người*) xác định mục đích là “sống phù hợp với tự nhiên” (hay sống thuận theo tự nhiên), điều cũng chính là sống theo đức hạnh, vì đức hạnh là đích mà tự nhiên dẫn ta tới.",
"url": "https://en.wikisource.org/wiki/Lives_of_the_Eminent_Philosophers/Book_VII",
},
"misread": [
"**“Zeno dạy phân biệt điều trong và ngoài tầm kiểm soát.”** Thực ra công thức nổi tiếng ấy mở đầu *Cẩm nang* của Epictetus, người sống hơn ba trăm năm sau. Zeno nói bằng ngôn ngữ khác: chỉ đức hạnh là thiện, còn sức khỏe, của cải, danh tiếng “không thiện không ác” — nền móng mà Epictetus về sau dựa vào.",
"**“Người Khắc kỷ đè nén mọi cảm xúc, sống như cỗ máy.”** Thực ra họ muốn diệt những cảm xúc sinh từ phán đoán sai, như sợ mất của cải vì tưởng đó là điều xấu. Người hiền triết Khắc kỷ vẫn có “cảm xúc tốt”: niềm vui, sự thận trọng, lòng mong muốn điều tốt.",
],
"related": [
("doc/epictetus-cam-nang.md", "Đọc “Cẩm nang” của Epictetus"),
("lich-su/hy-lap-co-dai.md", "Hy Lạp cổ đại: từ thần thoại đến lý trí"),
],
"sources": [
("Durand, Marion, Simon Shogry & Dirk Baltzly, “Stoicism”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/stoicism/"),
("Pigliucci, Massimo, “Stoicism”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/stoicism/"),
("Diogenes Laërtius, *Lives of the Eminent Philosophers*, quyển VII, bản dịch R. D. Hicks (1925), Wikisource.", "https://en.wikisource.org/wiki/Lives_of_the_Eminent_Philosophers/Book_VII"),
("Cicero, *On the Nature of the Gods* III.22–23, bản dịch C. D. Yonge, Project Gutenberg.", "https://www.gutenberg.org/ebooks/14988"),
("Epictetus, *The Enchiridion*, bản dịch Thomas Wentworth Higginson, Project Gutenberg.", "https://www.gutenberg.org/ebooks/45109"),
],
},
"epictetus": {
"desc": "Từng là nô lệ, Epictetus dạy rằng tự do thật nằm ở phán đoán của chính mình: điều làm ta khổ không phải sự việc, mà là cách ta nhìn sự việc.",
"bio": [
"Một đêm, Epictetus nghe tiếng động ngoài cửa. Chạy ra thì chiếc đèn sắt cạnh bàn thờ trong nhà đã bị lấy mất. Ông không đuổi theo, cũng không nguyền rủa. Ông nghĩ: kẻ lấy đèn chẳng làm điều gì lạ, hắn cũng tin rằng điều tốt nằm ở đồ vật, như chính ta vẫn tin; ngày mai ta sẽ dùng đèn đất nung, vì người ta chỉ mất được cái mình đang có. Câu chuyện do chính ông kể trong *Diễn từ* (I.18), và nó gói gọn triết học của ông: đừng đặt sự bình an của mình vào những thứ người khác lấy đi được.",
"Ông sinh vào khoảng những năm 50 sau Công nguyên ở Hierapolis, một thành Hy Lạp ở Tiểu Á, và có một thời là nô lệ của Epaphroditus, một quan chức trong triều hoàng đế Nero ở Rome. Ông từng theo học Musonius Rufus, một triết gia **Khắc kỷ** (*Stoicism*). Được trả tự do, ông mở lớp ở Rome, cho tới khi hoàng đế Domitian trục xuất các triết gia khỏi Ý (theo cách tính thường gặp là năm 89). Ông sang Nicopolis, ven biển tây bắc Hy Lạp, lập trường và dạy học tới khi mất, khoảng năm 135. Ông đi khập khiễng: tương truyền người chủ cũ đã bẻ gãy chân ông, nhưng nhà chú giải Simplicius (thế kỷ 6) chỉ nói ông yếu ớt và tật chân từ nhỏ. Ông không lấy vợ; về già, ông nhận nuôi một đứa trẻ mà cha mẹ nghèo không nuôi nổi.",
"Giống Socrates, người ông thường lấy làm gương, Epictetus giảng dạy bằng lời. Theo lời tựa của Arrian, học trò của ông (về sau là nhà sử học), *Diễn từ* là những gì Arrian ghi lại từ các buổi học; bộ sách nguyên có từ tám quyển trở lên, nay còn bốn. *Cẩm nang* (*Encheiridion*) là bản tóm lược ngắn để mang theo người. Đọc *Diễn từ*, ta gặp một người thầy lúc tha thiết, lúc châm chọc, luôn kéo học trò từ chỗ nói hay về triết học sang chỗ sống như một triết gia.",
"Hoàng đế Marcus Aurelius chưa từng là học trò ông, nhưng đọc *Diễn từ* và tự coi mình là người đi theo. Mười lăm thế kỷ sau, Pascal vừa khâm phục vừa tranh cãi với ông. Thế kỷ 20, những dạng đầu tiên của liệu pháp nhận thức – hành vi, như công trình của Albert Ellis, có chung ý tưởng cốt lõi với ông. Kẹt xe giờ tan tầm, bị sếp mắng, bị chê trên mạng: câu hỏi của Epictetus vẫn dùng được ngay, rằng trong chuyện này, phần nào thật sự thuộc về mình?",
],
"works": [
("đầu thế kỷ 2", "*Diễn từ* (*Discourses*)", "Bài giảng do Arrian ghi lại; nguyên có từ tám quyển trở lên, nay còn bốn"),
("đầu thế kỷ 2", "*Cẩm nang* (*Encheiridion*)", "Bản tóm lược ngắn của *Diễn từ* do Arrian soạn, rất được ưa chuộng ở châu Âu thế kỷ 16–17"),
],
"thoughts": [
"Hai loại sự việc: thuộc quyền ta là phán đoán, ý muốn, điều ta theo đuổi hay né tránh; không thuộc quyền ta là thân thể, tài sản, danh tiếng, chức vụ. Phần lớn nỗi khổ đến từ chỗ nhầm hai loại này (*Cẩm nang* 1).",
"Dừng lại trước ấn tượng đầu tiên: khi một hình ảnh hay cảm giác ập tới, hãy bảo nó đợi một chút để mình xem xét, rồi mới đồng ý hay không (*Diễn từ* II.18). Tự do nằm trong khoảng lặng ấy.",
"Không ai cưỡng được ý chí: người ta có thể xiềng chân ông, nhưng ý chí của ông thì đến thần Zeus cũng không khuất phục được (*Diễn từ* I.1). Lời ấy đến từ một người từng là nô lệ.",
"Thôi đổ lỗi: người chưa học triết học trách người khác về cảnh ngộ của mình, người mới học trách chính mình, người học xong không trách ai (*Cẩm nang* 5).",
],
"argument": {
"title": "Điều gì thật sự thuộc về ta?",
"intro": "Lập luận ghép từ chương 1 và chương 5 của *Cẩm nang* trả lời câu hỏi: muốn không ai tước được sự bình an của mình, phải đặt nó vào đâu?",
"premises": [
"Có những thứ thuộc quyền ta (phán đoán, ý muốn, ham muốn và né tránh) và những thứ không (thân thể, tài sản, danh tiếng, chức vụ).",
"Thứ thuộc quyền ta thì tự do, không ai cản trở được; thứ không thuộc quyền ta thì mong manh, lệ thuộc, nằm trong tay người khác.",
"Điều làm ta bất an không phải bản thân sự việc, mà là phán đoán của ta về sự việc.",
],
"conclusion": "Vậy ai đặt hạnh phúc vào thứ không thuộc quyền mình sẽ luôn bị cản trở, than thở và oán trách; ai đặt nó vào phán đoán và lựa chọn của chính mình thì không ai ép buộc hay làm hại được.",
"objection": "Pascal, người rất khâm phục Epictetus, chê rằng ông tưởng chỉ cần nói “cái đó hoặc thuộc quyền ta, hoặc không” là đủ chứng minh, mà không thấy rằng điều khiển trái tim mình đâu có nằm trong tầm tay ta (*Pensées*, đoạn 467 trong bản dịch của Trotter). Ai từng mất người thân hay trải qua trầm cảm đều biết: không phải cứ muốn đổi phán đoán là đổi được. Và lối chia đôi dễ biến thành thái độ cam chịu trước bất công.",
"reply": "Người theo Epictetus đáp: ông chưa bao giờ nói việc này dễ. Chính vì phán đoán thường bật ra trước khi ta kịp nghĩ, triết học phải là luyện tập hằng ngày: tập dừng lại trước ấn tượng đầu tiên rồi mới đồng ý hay không (*Diễn từ* II.18). Phân biệt hai loại sự việc cũng không phải khoanh tay: ông vẫn đòi học trò làm tròn bổn phận với gia đình và thành bang; điều cần buông là đòi hỏi kết quả phải chiều theo ý mình.",
},
"quote": {
"source": "Epictetus, *Cẩm nang* (*Encheiridion*), chương 5 — bản dịch tiếng Anh của George Long (1877)",
"orig": "Men are disturbed not by the things which happen, but by the opinions about the things; for example, death is nothing terrible, for if it were it would have seemed so to Socrates; for the opinion about death that it is terrible, is the terrible thing.",
"vi": "Con người bị xáo trộn không phải bởi những gì xảy ra, mà bởi ý kiến về những điều ấy; chẳng hạn, cái chết chẳng có gì khủng khiếp, vì nếu có thì Socrates đã thấy nó khủng khiếp rồi; chính ý kiến cho rằng cái chết khủng khiếp mới là điều khủng khiếp.",
"url": "https://www.gutenberg.org/ebooks/10661",
},
"misread": [
"**“Khắc kỷ là đè nén cảm xúc, sống như tượng đá.”** Thực ra các nhà Khắc kỷ phân biệt những “đam mê” không lành mạnh (đau buồn, sợ hãi, thèm khát, khoái lạc quá đà) với những trạng thái lành mạnh (thận trọng, mong muốn đúng đắn, niềm vui). Đam mê, với họ, là một phán đoán sai mà ta đã gật đầu đồng ý; còn phản ứng tự động như giật mình trước nguy hiểm thì không ai tránh được.",
"**“Epictetus đã viết cuốn *Cẩm nang*.”** Thực ra, theo lời tựa của Arrian, *Diễn từ* là ghi chép của học trò (dù vài học giả nghi ngờ điều này), còn *Cẩm nang* chỉ là bản tóm lược, làm mỏng đi nhiều lập luận. Thích *Cẩm nang* thì nên đọc tiếp *Diễn từ*.",
],
"related": [
("doc/epictetus-cam-nang.md", "Đọc “Cẩm nang” của Epictetus"),
("doc/aurelius-suy-tuong.md", "Hướng dẫn đọc Suy tưởng của Marcus Aurelius"),
],
"sources": [
("Graver, Margaret, “Epictetus”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/epictetus/"),
("Pigliucci, Massimo, “Stoicism”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/stoicism/"),
("Epictetus, *A Selection from the Discourses of Epictetus with the Encheiridion*, bản dịch George Long, Project Gutenberg.", "https://www.gutenberg.org/ebooks/10661"),
("Pascal, Blaise, *Pensées*, bản dịch W. F. Trotter (1910), Project Gutenberg — các đoạn 466–467 bàn về Epictetus.", "https://www.gutenberg.org/ebooks/18269"),
],
},
"marcus-aurelius": {
"desc": "Người quyền lực nhất đế chế La Mã viết sổ tay để tự nhắc mình: đừng oán trách, đừng giận người làm sai, hãy làm tốt phần việc của một con người.",
"bio": [
"Có lần, người đàn ông quyền lực nhất đế chế La Mã tự dặn mình trong sổ tay: coi chừng, đừng để mình hóa thành một “Caesar”, đừng để bị nhuộm thứ màu ấy; hãy giữ mình giản dị, tử tế, chuộng công lý (*Suy tưởng* VI.30). Người viết chính là một Caesar: hoàng đế Marcus Aurelius. Cuốn sổ ấy không định cho ai đọc. Nó gồm hàng trăm ghi chú ngắn về cái chết, về sự phù du của danh vọng, về cơn bực bội với những người xung quanh, và về việc sống sao cho xứng với triết học mà ông theo. Thời cổ đại không để lại cho ta văn bản riêng tư nào khác giống như thế.",
"Marcus sinh năm 121 ở Rome. Trong sự sắp đặt nối ngôi của hoàng đế Hadrian, năm 138 ông được Antoninus Pius nhận làm con nuôi. Ông học hùng biện với Fronto, hai thầy trò còn để lại cả một tập thư, rồi rời hùng biện để theo triết học. Trong số các thầy, ông biết ơn nhất những người theo phái **Khắc kỷ** (*Stoicism*), như Rusticus, người cho ông mượn bản ghi các bài giảng của Epictetus. Năm 161 ông lên ngôi, ban đầu cùng trị vì với Lucius Verus, từ năm 169 thì một mình. Gần hai mươi năm ấy là chiến tranh ở biên giới phía bắc, những cuộc nổi loạn và một trận dịch lớn; ông ở nơi chiến dịch phần lớn thời gian và mất năm 180 trong doanh trại.",
"Cuốn sổ được viết bằng tiếng Hy Lạp, ít nhất một phần trong những năm chinh chiến cuối đời (một ước đoán là khoảng 171–175). Nó vốn không có tên: nhan đề *Ta eis heauton* (“Gửi chính mình”) chỉ được ghi nhận từ khoảng năm 900, còn tên *Suy tưởng* (*Meditations*) do một người biên tập đời sau đặt. Quyển I là lời cảm ơn những người đã cho ông tấm gương tốt; các quyển sau là những ghi chú rời, nhiều câu như khẩu hiệu ông tự hô cho mình. Ông viết để luyện chính mình, nhắc lại những điều đã tin mà chưa sống được.",
"Ông không phải nhà lý thuyết lớn như Platon hay Aristotle, và chính ông thừa nhận mình còn xa mới sống được như một triết gia. Nhưng *Suy tưởng* cho thấy triết học thời cổ là một cách sống: một người nắm mọi quyền lực vẫn phải tập từng ngày để không giận dữ, không kiêu ngạo, không sợ chết. Ông còn lập ở Athens bốn ghế giảng dạy cho bốn trường phái lớn, kể cả phái Epicurus mà ông không theo. Hôm nay, khi ta mất bình tĩnh vì một bình luận trên mạng hay một cuộc họp dài lê thê, những trang ông viết cho riêng mình vẫn như viết cho ta.",
],
"works": [
("k. 170–180", "*Suy tưởng* (*Ta eis heauton*, tiếng Anh *Meditations*)", "12 quyển ghi chú viết bằng tiếng Hy Lạp cho riêng mình"),
("k. 138–166", "Thư từ với Fronto", "Thư trao đổi với người thầy dạy hùng biện; bản chép được tìm thấy lại năm 1815"),
],
"thoughts": [
"Cái nhìn từ trên cao: hãy ôm cả vũ trụ và thời gian vô tận vào tầm mắt; thấy đời người ngắn ngủi giữa hai khoảng vô tận trước khi sinh và sau khi chết, nhiều nỗi phiền sẽ tự nhỏ lại (*Suy tưởng* IX.32).",
"Đừng thêm vào ấn tượng đầu tiên: có người nói xấu mình, đó là điều được báo; còn “mình bị hại” là phán đoán mình tự thêm vào (VIII.49).",
"Con người sinh ra vì nhau: ta và người làm điều sai cùng chung lý trí, sinh ra để hợp tác như hai bàn tay, hai hàm răng; giận ghét họ là chống lại chính bản tính ấy (II.1).",
"Nhớ rằng mình sẽ chết: vì có thể rời cuộc đời ngay lúc này, hãy để ý nghĩ ấy điều chỉnh mọi việc làm và suy nghĩ (II.11).",
"Làm hơn nói: ông tự nhắc thôi bàn luận người tốt phải ra sao, mà hãy trở thành người như thế (X.16).",
],
"argument": {
"title": "Thiên ý hay nguyên tử?",
"intro": "Chín lần trong *Suy tưởng*, Marcus đặt trước mình hai khả năng về vũ trụ. Theo cách tái dựng phổ biến, lập luận nhắm vào một thói quen rất người: oán trách số phận.",
"premises": [
"Hoặc vũ trụ được một trí tuệ sắp đặt (thiên ý, như phái Khắc kỷ tin), hoặc nó chỉ là những nguyên tử va chạm ngẫu nhiên (như phái Epicurus tin).",
"Nếu là thiên ý, mọi chuyện xảy ra đều thuộc về một trật tự chung, nên oán trách là trách sai chỗ.",
"Nếu chỉ là nguyên tử ngẫu nhiên, thì chẳng có ai để trách, và oán trách cũng chẳng đổi được gì.",
],
"conclusion": "Dù vũ trụ là thế nào, oán trách điều đã xảy ra đều vô ích; việc của ta là sửa những gì sửa được và làm tốt phần việc của mình.",
"objection": "Đây là một **lưỡng nan** (*dilemma*): nó chỉ đứng vững nếu hai nhánh bao quát hết khả năng và nhánh nào cũng dẫn tới kết luận. Người phản bác nhắm vào nhánh thứ hai: nếu thế giới không có trật tự nào, sao ta không nên phẫn nộ trước bất công, khi chính sự phẫn nộ đã thúc người ta sửa luật, chống dịch, chống áp bức? Còn nhánh thứ nhất vấp phải câu hỏi cũ: một trật tự tốt đẹp sao lại để trẻ con chết vì dịch?",
"reply": "Marcus không bảo ta khoanh tay. Ngay ở *Suy tưởng* VIII.17 ông dặn: nếu sửa được nguyên nhân thì sửa, không thì sửa chính sự việc; chỉ khi chẳng làm được gì nữa thì trách móc mới vô ích. Điều lưỡng nan muốn dập tắt là sự cay đắng, không phải hành động. Các nhà nghiên cứu cũng lưu ý ông vẫn tin vũ trụ có trật tự; lưỡng nan là lời tự nhắc lúc yếu lòng, giống người cai thuốc giữ thêm một lý do phụ cho những khi lý do chính không đủ sức.",
},
"quote": {
"source": "Marcus Aurelius, *Suy tưởng* II.1 — bản dịch tiếng Anh của George Long (1862)",
"orig": "Begin the morning by saying to thyself, I shall meet with the busybody, the ungrateful, arrogant, deceitful, envious, unsocial. All these things happen to them by reason of their ignorance of what is good and evil.",
"vi": "Hãy bắt đầu buổi sáng bằng việc tự nhủ: hôm nay ta sẽ gặp kẻ tọc mạch, kẻ vô ơn, kẻ ngạo mạn, kẻ dối trá, kẻ đố kỵ, kẻ khó gần. Tất cả những điều ấy xảy đến với họ vì họ không biết đâu là thiện, đâu là ác.",
"url": "https://www.gutenberg.org/ebooks/15877",
},
"misread": [
"**“Marcus Aurelius là vị vua triết gia hoàn hảo.”** Thực ra chính ông tự trách mình còn xa triết học (*Suy tưởng* VIII.1), và triều đại của ông có những trang tối: năm 177, nhiều tín hữu Kitô bị xử tử ở Lyon, theo một lá thư được sử gia Eusebius lưu lại. *Suy tưởng* đáng đọc không phải vì tác giả hoàn hảo, mà vì ông thành thật về khoảng cách giữa điều mình tin và điều mình làm.",
],
"related": [
("doc/aurelius-suy-tuong.md", "Hướng dẫn đọc Suy tưởng của Marcus Aurelius"),
("doc/epictetus-cam-nang.md", "Đọc “Cẩm nang” của Epictetus"),
("lich-su/hy-lap-co-dai.md", "Hy Lạp cổ đại: từ thần thoại đến lý trí"),
],
"sources": [
("Kamtekar, Rachana, “Marcus Aurelius”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/marcus-aurelius/"),
("Sellars, John, “Marcus Aurelius”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/marcus/"),
("Marcus Aurelius, *Thoughts of Marcus Aurelius Antoninus*, bản dịch George Long (kèm tiểu sử của người dịch), Project Gutenberg.", "https://www.gutenberg.org/ebooks/15877"),
],
},
"augustine": {
"desc": "Từ cậu thiếu niên hái trộm lê cho vui đến vị giám mục viết “Tự thú”: Augustine đặt nội tâm, ý chí và cái ác vào trung tâm triết học phương Tây.",
"bio": [
"Năm mười sáu tuổi, Augustine cùng đám bạn đi rung trộm cây lê gần vườn nho nhà mình. Không phải vì đói: lê ấy chẳng ngon, nhà ông có lê ngon hơn, và hái xong cả bọn ném cho lợn ăn. Gần ba mươi năm sau, trong *Tự thú* (*Confessions*), ông vẫn day dứt: điều gì khiến người ta làm điều sai chỉ vì nó sai? Câu hỏi nhỏ ấy dẫn ông tới những câu hỏi lớn về ý chí, tự do và nguồn gốc của cái ác.",
"Ông sinh năm 354 ở Thagaste, miền Bắc Phi thuộc La Mã (nay là Souk Ahras, Algeria). Mẹ ông là một tín hữu Kitô sùng đạo; cha ông đến lúc hấp hối mới chịu rửa tội. Năm mười chín tuổi, đọc cuốn *Hortensius* của Cicero, ông say mê đi tìm sự khôn ngoan, rồi theo đạo Mani, một tôn giáo nhị nguyên, suốt chín năm. Ông dạy hùng biện ở Carthage, Rome rồi Milan, nơi những bài giảng của giám mục Ambrose và mấy cuốn sách của phái Platon dịch sang tiếng Latin cho ông một cách hiểu mới về Thượng đế và về cái ác. Mùa hè năm 386, sau một cơn khủng hoảng kéo dài, ông cải đạo; lễ Phục sinh năm 387, ông chịu phép rửa.",
"Về lại châu Phi, năm 391, dường như ngoài ý muốn, ông được phong linh mục ở thành cảng Hippo Regius, khoảng năm 396 thành giám mục, và gắn bó ở đó tới cuối đời. Ông viết không ngừng: còn lại khoảng một trăm cuốn sách, ba trăm lá thư và sáu trăm bài giảng, phần lớn sinh ra từ những cuộc tranh luận với phái Mani, phái Donatus và phái Pelagius. Ông mất năm 430, khi người Vandal đang vây thành Hippo.",
"Augustine sống ở cuối thời cổ đại nhưng thường được xếp là triết gia trung cổ đầu tiên, vì suốt một nghìn năm sau, thần học và triết học phương Tây gần như luôn đối thoại với ông. Anselm và Aquinas xây trên nền của ông; Pascal nói mình mượn cách nhìn về thân phận con người từ ông; Hannah Arendt viết luận án tiến sĩ về khái niệm tình yêu ở ông; còn Wittgenstein mở đầu *Philosophical Investigations* bằng một đoạn *Tự thú* để phản bác. Đọc ông hôm nay, ta gặp một người suy nghĩ ở ngôi thứ nhất: tôi lầm, tôi muốn, tôi không hiểu nổi chính mình.",
],
"works": [
("386", "*Contra Academicos*", "Chống phái Hàn lâm: phản bác hoài nghi luận; tác phẩm sớm nhất còn lại của ông"),
("388–k. 395", "*De libero arbitrio*", "Về sự tự do lựa chọn của ý chí: nếu Thượng đế toàn thiện thì cái ác từ đâu ra?"),
("k. 397–400", "*Confessiones*", "*Tự thú*: triết học viết như tự truyện, với những trang nổi tiếng về ký ức và thời gian (quyển X–XI)"),
("399–419 hoặc muộn hơn", "*De trinitate*", "Về Ba Ngôi: phân tích tâm trí con người như hình ảnh của Thượng đế"),
("413–426", "*De civitate Dei*", "*Thành phố của Thiên Chúa*: viết sau khi Rome bị cướp phá năm 410; hai “thành phố” xây trên hai thứ tình yêu"),
],
"thoughts": [
"Tin để hiểu: đức tin đi trước về thời gian, nhưng sự hiểu mới quý hơn; lý trí có bổn phận soi sáng điều mình tin. Về sau Anselm gọi chương trình ấy là “đức tin đi tìm hiểu biết”.",
"Cái ác là sự thiếu vắng điều thiện (**thuyết thiếu vắng**, *privation theory*): cái ác không phải một “chất” do Thượng đế tạo ra, mà là sự thiếu hụt ở nơi đáng lẽ phải có điều tốt, như ý chí quay lưng khỏi điều thiện cao hơn.",
"Ân sủng và tội tổ tông: chống lại phái Pelagius, ông cho rằng sau sự sa ngã, con người không thể tự mình muốn và làm điều thiện trọn vẹn mà cần ân sủng chữa lành; quan niệm này định hình Kitô giáo phương Tây suốt nhiều thế kỷ.",
"Thời gian ở trong tâm hồn: quá khứ không còn, tương lai chưa tới, hiện tại không có bề dày; ta đo thời gian bằng ký ức, sự chú tâm và chờ đợi của chính tâm trí (*Tự thú* XI).",
"Không được nói dối, kể cả để cứu người: ông phân tám loại nói dối, loại nào cũng là tội, chỉ nặng nhẹ khác nhau, vì không ai được đổi sự sống đời đời lấy sự sống ở đời này (*De mendacio*).",
],
"argument": {
"title": "Nếu tôi lầm, tôi tồn tại",
"intro": "Phái Hàn lâm, những người theo **hoài nghi luận** (*skepticism*), cho rằng người khôn ngoan không nên tin chắc điều gì. Trong *Thành phố của Thiên Chúa* (XI.26), Augustine đáp bằng một lập luận ngắn (*si fallor, sum*) mà nhiều nhà nghiên cứu cho là có lẽ đã gợi hứng cho câu “Tôi tư duy, vậy tôi tồn tại” của Descartes mười hai thế kỷ sau.",
"premises": [
"Cái gì không tồn tại thì không thể bị lừa hay lầm lẫn.",
"Vậy nếu tôi lầm, thì tôi tồn tại.",
"Giả sử niềm tin “tôi tồn tại” của tôi là một sự lầm: theo P2, khi ấy tôi vẫn tồn tại, nghĩa là niềm tin ấy đúng.",
],
"conclusion": "Niềm tin “tôi tồn tại” không thể sai; vậy có ít nhất một điều ta biết chắc, và khẳng định “không biết chắc được gì” của phái hoài nghi là sai.",
"objection": "Các nhà phê bình đáp: thắng như vậy là thắng quá nhỏ. Lập luận chỉ cho biết có một kẻ đang nghĩ, đang lầm, chưa nói gì về thế giới bên ngoài, về thân thể, hay về việc “tôi” là gì. Một người hoài nghi cổ đại sẽ nói đó chỉ là hiểu biết về trạng thái chủ quan, không phải tri thức về thực tại.",
"reply": "Augustine chỉ cần một phản ví dụ: phái Hàn lâm nói không gì biết chắc được, nên một tri thức chắc chắn duy nhất đã đủ bác bỏ họ. Từ đó ông còn đi xa hơn: tôi biết mình tồn tại, biết rằng mình biết, và biết mình yêu hai điều ấy; tôi chắc mình đang muốn như chắc mình đang tồn tại, nên ý chí là của tôi và tôi chịu trách nhiệm về nó.",
},
"quote": {
"source": "Augustine, *Tự thú* (*Confessions*), quyển I, chương 1 — bản dịch tiếng Anh của Edward B. Pusey (1838)",
"orig": "Thou awakest us to delight in Thy praise; for Thou madest us for Thyself, and our heart is restless, until it repose in Thee.",
"vi": "Ngài đánh thức chúng con để chúng con vui sướng ca ngợi Ngài; vì Ngài đã dựng nên chúng con cho Ngài, và lòng chúng con khắc khoải cho tới khi được nghỉ yên trong Ngài.",
"url": "https://www.gutenberg.org/ebooks/3296",
},
"misread": [
"**“Theo Augustine, cái ác không có thật.”** Thực ra ông nói cái ác không phải một *thực thể*, không phải “chất liệu” do Thượng đế tạo ra, chứ không nói nó vô hại hay chỉ là ảo giác. Mù lòa là sự thiếu thị lực, nhưng không vì thế mà bớt đau đớn.",
],
"related": [
("cau-hoi/cai-ac.md", "Cái ác là gì?"),
("cau-hoi/thoi-gian.md", "Thời gian có trôi không? Hay quá khứ–hiện tại–tương lai đều thật?"),
("cau-hoi/noi-doi.md", "Có bao giờ được nói dối?"),
("cau-hoi/ban-tinh-con-nguoi.md", "Bản tính con người thiện hay ác?"),
("lich-su/trung-co.md", "Trung cổ: đức tin gặp lý trí"),
],
"sources": [
("Tornau, Christian, “Augustine of Hippo”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/augustine/"),
("Augustine, *The Confessions of St. Augustine*, bản dịch E. B. Pusey, Project Gutenberg.", "https://www.gutenberg.org/ebooks/3296"),
("Augustine, *The City of God*, tập I, bản dịch Marcus Dods, Project Gutenberg (quyển XI, chương 26).", "https://www.gutenberg.org/ebooks/45304"),
("Augustine, *On Lying* (*De mendacio*), bản dịch H. Browne, *Nicene and Post-Nicene Fathers* (1887), New Advent.", "https://www.newadvent.org/fathers/1312.htm"),
],
},
"avicenna": {
"desc": "Ibn Sina (Avicenna): nhà bác học có sách y khoa được dạy ở châu Âu tới thế kỷ 17, người nghĩ ra “người bay” để hỏi cái tôi có cần thân xác không.",
"bio": [
"Hãy tưởng tượng bạn vừa được tạo ra, trưởng thành ngay tức khắc, nhưng mắt bị che kín, lơ lửng giữa khoảng không, không chạm vào bất cứ thứ gì. Bạn không thấy, không nghe, không cảm nhận được cả thân thể mình. Bạn có biết mình đang tồn tại không? Ibn Sina, người châu Âu Latin gọi là Avicenna, cho rằng có. Và từ **thí nghiệm tư duy** (*thought experiment*) ấy ông hỏi tiếp: vậy cái “tôi” mà ta biết chắc kia có phải là thân thể không?",
"Ông sinh ở Afshana, một làng gần Bukhara (nay thuộc Uzbekistan), dưới triều Samanid. Năm sinh không chắc: tư liệu cũ thường ghi 980, nhưng nhà nghiên cứu Dimitri Gutas cho rằng con số ấy tính nhầm và ông sinh vào thập niên 970. Theo tự truyện do học trò al-Juzjani lưu giữ và viết tiếp, ông tự học gần hết các môn và thông thạo khi mới mười tám tuổi; nhờ chữa bệnh cho vua Samanid, cậu thiếu niên được vào thư viện hoàng gia, nơi có những cuốn sách mà trước đó và sau này ông không gặp lại. Ông cũng kể đã đọc *Siêu hình học* của Aristotle mà không hiểu nó nhằm điều gì, cho tới khi đọc một chuyên luận ngắn của al-Farabi.",
"Năm 999 triều Samanid sụp đổ, và đời ông thành những chuyến đi tìm người bảo trợ: Gurganj, Jurjan, Rayy, Hamadan, nơi ông vừa làm thầy thuốc vừa làm cố vấn chính trị, có lúc làm tể tướng. Khoảng mười ba năm cuối đời ông sống ở Isfahan và hoàn thành bộ bách khoa triết học *Chữa lành* (*al-Shifa*). Tương truyền ông viết nhiều phần của bộ sách này mà không cần sách tham khảo, và soạn cuốn *Cứu rỗi* ngay trong một cuộc hành quân. Ông mất năm 1037 ở Hamadan.",
"Trong thế giới Hồi giáo, triết học của ông chi phối đời sống trí thức nhiều thế kỷ; ngay người phản bác như al-Ghazali cũng lấy ông làm đích chính. Ở châu Âu, bản dịch Latin bộ *Quy tắc y học* là sách giáo khoa y ở các đại học tới thế kỷ 17, còn siêu hình học của ông in dấu đậm trên Thomas Aquinas. Dante đặt ông vào vòng Limbo trong *Thần khúc*, cạnh Galen và Hippocrates. Với người học triết hôm nay, câu hỏi của ông vẫn còn nguyên: hiểu biết về chính mình có phải bắt đầu từ giác quan không?",
],
"works": [
("", "*Kitab al-Shifa* (*Chữa lành*)", "Bộ bách khoa triết học lớn nhất của ông: logic, khoa học tự nhiên, toán học, siêu hình học; hoàn thành ở Isfahan"),
("", "*al-Qanun fi al-Tibb* (*Quy tắc y học*)", "Bộ sách y khoa mà bản dịch Latin được dạy ở các đại học châu Âu tới thế kỷ 17"),
("", "*al-Najat* (*Cứu rỗi*)", "Bản trình bày triết học rút gọn, soạn sau *Chữa lành*"),
("", "*al-Isharat wa-l-Tanbihat* (*Chỉ dẫn và nhắc nhở*)", "Bộ tổng luận cuối cùng, viết theo lối gợi mở để người học tự suy nghĩ"),
],
"thoughts": [
"Tất yếu và khả hữu: mọi vật quanh ta có thể có mà cũng có thể không, nên cần nguyên nhân để tồn tại; chuỗi nguyên nhân ấy dẫn tới một Đấng Tất yếu Tồn tại, không có nguyên nhân nào cả.",
"Bản chất và tồn tại: biết một vật *là gì* chưa cho biết nó *có* hay không; với mọi vật trừ Thượng đế, tồn tại không nằm sẵn trong bản chất. Phân biệt này về sau được Aquinas tiếp thu.",
"Tự ý thức trực tiếp: theo “người bay”, ta biết mình tồn tại không phải nhờ giác quan hay nhờ cảm nhận thân thể.",
"Một hệ thống cho mọi tri thức: logic, khoa học tự nhiên, toán học, siêu hình học và cả giáo lý tôn giáo được ông xếp vào một tòa nhà lý trí duy nhất, nhất quán.",
],
"argument": {
"title": "Người bay",
"intro": "Thí nghiệm này mở đầu phần bàn về linh hồn trong *Chữa lành*. Theo cách tái dựng phổ biến:",
"premises": [
"Một người vừa được tạo ra, trưởng thành trọn vẹn nhưng bị che mắt, lơ lửng trong khoảng không và không chạm vào gì, nên không nhận được gì qua giác quan, kể cả về thân thể mình.",
"Người ấy vẫn khẳng định được rằng mình tồn tại.",
"Nhưng người ấy không khẳng định sự tồn tại của thân thể mình hay bất kỳ bộ phận nào của nó.",
],
"conclusion": "Vậy cái “tôi” mà người ấy biết chắc không phải là thân thể hay một bộ phận của nó: linh hồn là một cái gì khác thân thể.",
"objection": "Biết A mà không biết B không chứng tỏ A khác B. Người xưa biết nước mà không biết nước là H₂O; người bay có thể biết “tôi” mà không biết “tôi” thật ra là một bộ não đang hoạt động. Phản bác này, cũng nhắm vào lập luận tương tự của Descartes sáu thế kỷ sau, cho rằng thí nghiệm chỉ nói về điều ta *biết*, không nói về cái ta *là*.",
"reply": "Người bênh vực đáp rằng ít nhất thí nghiệm cũng chứng tỏ một điều quan trọng: sự tự ý thức cơ bản là trực tiếp, không đến từ giác quan và không phụ thuộc vào việc ý thức về thân thể hay về vật gì khác. Muốn chứng minh linh hồn tách khỏi thân thể thì cần thêm lập luận, nhưng kết luận khiêm tốn này đã đủ thách thức quan điểm cho rằng mọi hiểu biết, kể cả hiểu biết về chính mình, đều bắt đầu từ giác quan.",
},
"misread": [
"**“Avicenna chỉ là người chép lại Aristotle.”** Thực ra ông tổng hợp và sửa đổi di sản Hy Lạp thành một hệ thống của riêng mình, từ phân biệt bản chất và tồn tại đến học thuyết về Đấng Tất yếu. Chính hệ thống ấy, chứ không phải Aristotle trực tiếp, là thứ các nhà tư tưởng Hồi giáo về sau chấp nhận, sửa đổi hoặc bác bỏ suốt nhiều thế kỷ.",
],
"related": [
("lich-su/trung-co.md", "Trung cổ: đức tin gặp lý trí"),
],
"sources": [
("Gutas, Dimitri, “Ibn Sina [Avicenna]”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/ibn-sina/"),
("Rizvi, Sajjad H., “Avicenna (Ibn Sina)”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/avicenna-ibn-sina/"),
("Lizzini, Olga, “Ibn Sina’s Metaphysics”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/ibn-sina-metaphysics/"),
("Smith, Joel, “Self-Consciousness”, *Stanford Encyclopedia of Philosophy* (mục 1, về “người bay”).", "https://plato.stanford.edu/entries/self-consciousness/"),
("Dante Alighieri, *Divine Comedy: Hell*, khúc IV, bản dịch H. W. Longfellow, Project Gutenberg.", "https://www.gutenberg.org/ebooks/1001"),
],
},
"anselm": {
"desc": "Tu sĩ, rồi Tổng giám mục Canterbury, Anselm muốn chứng minh Thượng đế tồn tại chỉ bằng phân tích một khái niệm: luận chứng gây tranh cãi suốt gần nghìn năm.",
"bio": [
"Hãy thử nghĩ tới một thứ mà không thể nghĩ ra cái gì lớn hơn nó. Bạn vừa nghĩ tới, vậy nó đã có trong trí hiểu của bạn. Nhưng nếu nó chỉ có trong trí hiểu, ta lại nghĩ ra được một thứ lớn hơn: chính nó, cộng thêm việc có thật. Vậy nó phải có thật. Khoảng năm 1077–1078, một tu sĩ ở tu viện Bec, vùng Normandy, viết lập luận ấy trong vài trang sách mỏng tên *Proslogion*. Gần một nghìn năm sau, giới triết học vẫn chưa thống nhất được nó sai ở đâu, hay có sai thật không. Như Bertrand Russell nhận xét, tin rằng nó hỏng thì dễ, chỉ ra nó hỏng ở đâu mới khó.",
"Anselm sinh năm 1033 gần Aosta, khi ấy là một thị trấn thuộc Burgundy giáp Lombardy, nay ở miền bắc nước Ý. Năm hai mươi ba tuổi ông rời nhà, lang thang vài năm rồi đến tu viện Bec, nơi trường học của Lanfranc nổi tiếng về biện chứng pháp. Ông vào tu năm 1060, làm phó viện trưởng năm 1063 rồi viện trưởng năm 1078. Các tác phẩm triết học chính của ông ra đời trong những năm ở Bec.",
"Năm 1093 ông miễn cưỡng nhận chức Tổng giám mục Canterbury, và nhiệm kỳ ấy sóng gió đúng như ông lo: hai lần phải sống lưu vong vì không chịu để vua Anh nắm quyền trên Giáo hội, lần đầu dưới thời William Rufus, lần sau dưới thời Henry I (1103–1107). Giữa những biến động đó ông vẫn viết, trong đó có *Cur Deus Homo* (*Vì sao Thiên Chúa làm người*). Ông mất ngày 21 tháng 4 năm 1109, được phong thánh năm 1494 và được tôn làm Tiến sĩ Hội Thánh năm 1720.",
"Phương châm của Anselm là “đức tin đi tìm hiểu biết” (*fides quaerens intellectum*), cũng là cái tên đầu tiên ông đặt cho *Proslogion*. Ông không định thay đức tin bằng lý lẽ: đức tin là điểm xuất phát, nhưng lý lẽ phải thuyết phục được cả người không tin, nên *Monologion* được viết như một suy niệm chỉ dựa vào lý trí, không viện dẫn thẩm quyền Kinh thánh. Ông tự nhận không nói điều gì trái với Augustine, và xin ai thấy sách mình mới lạ hãy đọc kỹ các sách *Về Ba Ngôi* của Augustine trước đã. Với người học triết hôm nay, luận chứng của ông vẫn là bài tập tuyệt vời: “tồn tại” là gì, và có thể suy ra thực tại chỉ từ một định nghĩa không?",
],
"works": [
("1075–1076", "*Monologion*", "“Độc thoại”: suy niệm bằng lý lẽ về sự hiện hữu và bản tính của Thượng đế"),
("1077–1078", "*Proslogion*", "Tên ban đầu là *Đức tin đi tìm hiểu biết*; chứa luận chứng bản thể luận (chương 2–3)"),
("1080–1086", "*De veritate*, *De libertate arbitrii*, *De casu diaboli*", "Ba cuộc đối thoại về chân lý, tự do lựa chọn và sự sa ngã của quỷ dữ"),
("1095–1098", "*Cur Deus Homo*", "Vì sao Thiên Chúa làm người: lý giải sự Nhập thể bằng lý lẽ"),
],
"thoughts": [
"Từ những điều tốt đến cái Tốt tối cao: ở chương đầu *Monologion*, ông lập luận rằng những vật tốt nhiều ít khác nhau đều tốt nhờ một cái gì đó chung; cái ấy tốt tự thân, nên là cái tốt tối cao. Lối nghĩ này đậm màu truyền thống Platon – Augustine mà ông thừa hưởng.",
"Một lập luận tự đứng được: sau sáu mươi lăm chương chằng chịt của *Monologion*, ông muốn tìm một lập luận duy nhất không cần gì ngoài chính nó, và tìm thấy nó trong khái niệm “cái không thể nghĩ ra gì lớn hơn”.",
"Chân lý là sự ngay thẳng (*rectitudo*): một vật “đúng” khi nó làm đúng điều nó sinh ra để làm; câu nói đúng khi nói rằng cái đang có là có (*De veritate*).",
"Tự do không phải là khả năng làm điều xấu: tự do lựa chọn là khả năng giữ sự ngay thẳng của ý chí vì chính nó; Thượng đế không thể phạm tội mà vẫn tự do hơn ai hết (*De libertate arbitrii*).",
],
"argument": {
"title": "Luận chứng bản thể luận",
"intro": "Ở chương 2 của *Proslogion*, Anselm muốn thuyết phục cả “kẻ ngu dại” trong Thánh vịnh, người “nói trong lòng rằng không có Thượng đế”. Đây là **luận chứng bản thể luận** (*ontological argument*) theo cách đọc phổ biến nhất.",
"premises": [
"Thượng đế là cái mà không thể nghĩ ra cái gì lớn hơn. Ngay kẻ ngu dại nghe cụm từ ấy cũng hiểu, nên nó có trong trí hiểu của y, như bức tranh có trong đầu họa sĩ trước khi vẽ.",
"Tồn tại cả trong trí hiểu lẫn trong thực tại thì lớn hơn chỉ tồn tại trong trí hiểu.",
"Nếu cái không thể nghĩ ra gì lớn hơn chỉ có trong trí hiểu, ta lại nghĩ ra được một cái lớn hơn nó (chính nó, nhưng có thật): mâu thuẫn.",
],
"conclusion": "Vậy cái không thể nghĩ ra gì lớn hơn, tức Thượng đế, tồn tại cả trong thực tại.",
"objection": "Gaunilo, một tu sĩ ở tu viện Marmoutier, viết ngay bài “Bênh vực kẻ ngu dại”: thay “Thượng đế” bằng “hòn đảo tuyệt hảo nhất có thể nghĩ”, cùng chuỗi lập luận ấy sẽ “chứng minh” được hòn đảo có thật, điều rõ ràng vô lý; vậy lập luận phải hỏng ở đâu đó. Bảy thế kỷ sau, Kant chỉ ra một chỗ hỏng khả dĩ: “tồn tại” không phải là một thuộc tính cộng thêm vào khái niệm, nên không làm khái niệm “lớn hơn”.",
"reply": "Anselm đáp Gaunilo rằng lập luận chỉ áp dụng cho đúng một khái niệm, cái không thể nghĩ ra gì lớn hơn, chứ không cho “cái lớn hơn mọi thứ khác” như một hòn đảo; ai tìm được thứ gì khác hợp với lập luận, ông hứa sẽ tìm ra và tặng người ấy hòn đảo đã mất, để nó không bao giờ mất nữa. Những người bênh vực về sau nói thêm: phẩm chất làm nên một hòn đảo tuyệt vời (nhiều trái cây, bãi cát đẹp) không có mức tối đa, nên “hòn đảo tuyệt hảo nhất” là khái niệm rỗng; còn tri thức hay quyền năng thì có mức tối đa.",
},
"quote": {
"source": "Anselm, *Proslogion*, chương 1 — bản dịch tiếng Anh của Sidney Norton Deane (1903)",
"orig": "For I do not seek to understand that I may believe, but I believe in order to understand. For this also I believe,—that unless I believed, I should not understand.",
"vi": "Vì con không tìm hiểu để rồi mới tin, nhưng con tin để có thể hiểu. Bởi con còn tin điều này nữa: nếu không tin, con sẽ không hiểu.",
"url": "https://www.ccel.org/ccel/anselm/basic_works.iii.ii.html",
},
"misread": [
"**“Anselm nghĩ cứ định nghĩa một thứ là chứng minh được nó tồn tại.”** Thực ra, trả lời Gaunilo, ông khẳng định lập luận chỉ đúng với một khái niệm duy nhất: cái không thể nghĩ ra gì lớn hơn. Ông chưa bao giờ nói định nghĩa một hòn đảo, một con kỳ lân hay một người yêu hoàn hảo thì chúng sẽ có thật.",
],
"related": [
("cau-hoi/luan-chung-ton-giao.md", "Có thể chứng minh Chúa tồn tại bằng lý trí?"),
],
"sources": [
("Williams, Thomas, “Anselm of Canterbury”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/anselm/"),
("Oppy, Graham, Joshua Rasmussen & Joseph Schmid, “Ontological Arguments”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/ontological-arguments/"),
("Himma, Kenneth Einar, “Ontological Argument”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/ont-arg/"),
("Anselm, *Proslogium; Monologium; An Appendix in Behalf of the Fool by Gaunilon; and Cur Deus Homo*, bản dịch Sidney Norton Deane (1903), Christian Classics Ethereal Library.", "https://www.ccel.org/ccel/anselm/basic_works.i.html"),
],
},
"averroes": {
"desc": "Thẩm phán, thầy thuốc, nhà chú giải Aristotle lừng danh: Ibn Rushd lập luận rằng chính Luật thiêng đòi người có khả năng phải học triết học.",
"bio": [
"Có một ghi chép kể rằng khalip Abu Yaqub Yusuf của triều Almohad đã chính thức nhờ Ibn Rushd chú giải các tác phẩm của Aristotle cho dễ hiểu. Ông nhận lời, và dành phần lớn đời mình cho việc ấy: viết chú giải gần như toàn bộ Aristotle, nhiều tác phẩm được chú giải tới ba lần, từ bản tóm lược, bản diễn giải đến bản giảng từng câu. Với ông, chưa ai sau Aristotle thêm được điều gì đáng kể vào những gì Aristotle đã nói. Châu Âu Latin biết ông qua cái tên bị đọc chệch: Averroes.",
"Ông sinh năm 1126 ở Córdoba, trong một dòng họ thẩm phán danh tiếng; ông nội ông, cũng tên Ibn Rushd, là thẩm phán và luật gia lớn của trường phái Maliki. Bản thân ông vừa làm thẩm phán, vừa là thầy thuốc trưởng của khalip ở Marrakesh, vừa viết về luật học, y học, thiên văn và triết học. Cuối đời, vì những lý do đến nay vẫn chưa rõ, ông bị thất sủng và bị đày ra Lucena, cách Córdoba chừng 60 km; ông mất năm 1198 ở Marrakesh.",
"Câu hỏi lớn của ông là câu hỏi của mọi người có đạo mà ham hiểu biết: nếu lý trí dẫn tới một kết luận trái với kinh sách thì sao? Trước đó, nhà thần học al-Ghazali đã viết *Sự sụp đổ của các triết gia*, bác bỏ việc triết gia cho rằng các học thuyết của họ đã được chứng minh. Ibn Rushd đáp lại bằng *Sự sụp đổ của sự sụp đổ*, và trong *Bàn luận quyết định* ông lập luận rằng chính Luật thiêng đòi người có khả năng phải học triết học.",
"Ở châu Âu, các bản dịch Latin từ khoảng năm 1220 khiến ông nổi tiếng tới mức từ thập niên 1230 người ta đã gọi ông là “Nhà chú giải”; Dante xếp ông vào vòng Limbo trong *Thần khúc* và gọi ông là người làm nên bản chú giải lớn. Nhưng vài luận điểm gắn với tên ông, như mọi người chung một trí tuệ hay thế giới vĩnh cửu, làm dấy lên tranh cãi dữ dội ở Paris; Thomas Aquinas, người trong phần lớn vấn đề vẫn dựa vào ông khi đọc Aristotle, đã viết hẳn một chuyên luận để bác thuyết “một trí tuệ chung”.",
],
"works": [
("1178/1179", "*Fasl al-Maqal* (*Bàn luận quyết định*)", "Bàn về quan hệ giữa Luật thiêng và triết học"),
("k. 1179/1180", "*al-Kashf ʿan manahij al-adilla*", "Trình bày các phương pháp chứng minh trong giáo lý, thay cho thần học phái Ashʿari"),
("1180/1181", "*Tahafut al-Tahafut* (*Sự sụp đổ của sự sụp đổ*)", "Trả lời từng điểm cuốn sách tấn công triết học của al-Ghazali"),
("1186", "Chú giải lớn về *De Anima* của Aristotle", "Nay chỉ còn bản Latin; nơi ông trình bày thuyết trí tuệ chung cho mọi người"),
("sau 1190", "Chú giải lớn về *Siêu hình học* của Aristotle", "Một trong năm bộ chú giải từng câu của những năm cuối đời"),
],
"thoughts": [
"Một chân lý, nhiều cách nói: chứng minh dành cho người đủ sức suy lý, lập luận biện chứng và lời lẽ hùng biện dành cho số đông; Luật thiêng nói với mỗi người bằng cách hợp với người ấy.",
"Đọc nghĩa bóng có điều kiện: chỉ khi một chứng minh thật sự vênh với câu chữ kinh sách mới cần hiểu câu chữ ấy theo nghĩa bóng, và những cách diễn giải như vậy không nên đem giảng cho số đông.",
"Phép lạ không phải bằng chứng chính của lời tiên tri: điều chứng tỏ một nhà tiên tri là bộ luật ông mang lại có ích cho hạnh phúc của mọi người.",
"Trí tuệ chung: ông cho rằng cả loài người chung một trí năng tiếp nhận, nhưng suy nghĩ vẫn là của tôi vì chính trí tưởng tượng của tôi khởi động nó; có học giả gọi đây là phát biểu đầy đủ đầu tiên của thuyết “tâm trí mở rộng”.",
],
"argument": {
"title": "Học triết học là bổn phận",
"intro": "Mở đầu *Bàn luận quyết định*, Ibn Rushd đặt câu hỏi như một thẩm phán: theo Luật thiêng, học triết học và logic là được phép, bị cấm, hay bắt buộc?",
"premises": [
"Triết học, xét đến cùng, là xem xét các vật hiện hữu như những dấu chỉ dẫn tới Đấng Tạo tác: càng hiểu tác phẩm, càng hiểu người làm ra nó.",
"Kinh Qur’an nhiều lần kêu gọi con người dùng lý trí suy xét các vật hiện hữu, chẳng hạn lời kêu gọi những ai có mắt nhìn hãy suy ngẫm.",
"Cách suy xét hoàn hảo nhất là chứng minh; muốn chứng minh phải học logic, và được học cả từ người đi trước không cùng tôn giáo, như con dao hiến tế dùng được bất kể chủ nó theo đạo nào, miễn đúng cách.",
],
"conclusion": "Vậy với người có khả năng, học triết học không bị cấm mà còn là bổn phận do chính Luật thiêng đặt ra; và vì chân lý không chống lại chân lý, chỗ nào câu chữ kinh sách có vẻ trái với một chứng minh thì phải hiểu theo nghĩa bóng.",
"objection": "Phía thần học, như al-Ghazali trước đó, đáp rằng nhiều “chứng minh” siêu hình của triết gia, như chứng minh thế giới vĩnh cửu, thật ra chưa hề được chứng minh; ở những điểm ấy mặc khải nói điều ngược lại và phải được ưu tiên. Và nếu hễ lý trí vênh với kinh sách là kinh sách phải lùi về nghĩa bóng, chẳng phải lý trí đã ngồi lên trên mặc khải sao?",
"reply": "Ibn Rushd đáp rằng không có thứ bậc nào ở đây: triết học và Luật thiêng chân chính nói cùng một chân lý bằng những cách khác nhau cho những người khác nhau. Diễn giải nghĩa bóng chỉ được phép khi có chứng minh thật sự, và dành cho người đủ khả năng; còn những điều cốt lõi mà ai cũng phải tin, như sự tồn tại của Thượng đế, sứ mệnh của các nhà tiên tri, hạnh phúc hay khổ đau ở đời sau, thì không được diễn giải lệch đi. Với al-Ghazali, ông trả lời từng điểm trong *Sự sụp đổ của sự sụp đổ*.",
},
"misread": [
"**“Averroes dạy thuyết ‘hai chân lý’: điều đúng trong triết học có thể sai trong tôn giáo.”** Thực ra ông viết điều ngược lại: chân lý không chống lại chân lý mà phù hợp và làm chứng cho nhau. Lời buộc tội “hai chân lý” xuất hiện ở Paris năm 1277, nhắm vào một số giáo sư Latin, và giới nghiên cứu ngày nay đồng ý rằng không tác giả trung cổ nào thực sự giữ thuyết vô lý ấy.",
"**“Thế giới Hồi giáo quay lưng với Ibn Rushd; chỉ châu Âu mới đọc ông.”** Thực ra ảnh hưởng của ông trong thế giới Hồi giáo không sánh được với Ibn Sina, nhưng không hề bằng không: ông có hàng chục học trò trực tiếp, và sách của ông còn được dùng ở Andalus và Maghreb nhiều thế kỷ sau, cả trong quá trình học của Ibn Khaldun.",
],
"related": [
("lich-su/trung-co.md", "Trung cổ: đức tin gặp lý trí"),
],
"sources": [
("Ben Ahmed, Fouad & Robert Pasnau, “Ibn Rushd [Averroes]”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/ibn-rushd/"),
("Thijssen, Hans, “Condemnation of 1277”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/condemnation/"),
("Griffel, Frank, “Al-Ghazali”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/al-ghazali/"),
("Ibn Rushd, *On the Harmony of Religion and Philosophy* (*Kitab fasl al-maqal*), bản dịch George F. Hourani, London: Luzac (E. J. W. Gibb Memorial).", ""),
("Dante Alighieri, *Divine Comedy: Hell*, khúc IV, bản dịch H. W. Longfellow, Project Gutenberg.", "https://www.gutenberg.org/ebooks/1001"),
],
},
"maimonides": {
"desc": "Thầy thuốc, nhà luật học, triết gia Do Thái lớn nhất thời Trung cổ: Maimonides dạy rằng về Thượng đế, nói “không phải” trung thực hơn nói “là”.",
"bio": [
"Một học trò giỏi băn khoăn: em tin Kinh thánh, nhưng em cũng đã học logic và khoa học theo Aristotle, và hai bên dường như vênh nhau, em phải theo bên nào? Câu trả lời của người thầy dài thành ba quyển sách: *Chỉ dẫn cho người hoang mang* (*Dalalat al-Ha’irin*), viết bằng tiếng Ả Rập dưới dạng những lá thư gửi người học trò tên Joseph, hoàn thành năm 1190. Người thầy là Moses ben Maimon, người phương Tây gọi là Maimonides, người nói tiếng Hebrew gọi là Rambam.",
"Ông sinh ở Córdoba, cùng thành phố với Ibn Rushd, vào năm 1138 theo nghiên cứu gần đây (nhiều sách cũ ghi 1135). Năm 1148, triều Almohad chiếm Córdoba và buộc người không theo Hồi giáo phải cải đạo, lưu vong hoặc chết. Gia đình ông bỏ đi, lang bạt nhiều năm, tới Fez (Morocco) năm 1160, ghé qua Đất Thánh, năm 1166 tới Ai Cập rồi định cư ở Fustat, khu phố cổ của Cairo.",
"Người em trai buôn bán giỏi, chỗ dựa của cả nhà, mất tích trên biển trong một chuyến đi qua Ấn Độ Dương; Maimonides viết rằng nỗi mất mát ấy khiến ông rơi vào trầm uất. Từ đó ông sống bằng nghề y, về sau làm thầy thuốc cho vị tể tướng cai quản Ai Cập dưới quyền Saladin. Cùng lúc, ông là thẩm phán của cộng đồng Do Thái và là tác giả *Mishneh Torah*, bộ pháp điển 14 quyển hệ thống hóa toàn bộ luật Do Thái, tới nay vẫn được học. Ông mất năm 1204.",
"Với Maimonides, đọc Kinh thánh theo nghĩa đen, như tay Chúa, mắt Chúa, cơn giận của Chúa, là nguy hiểm, vì nó dẫn tới hình dung Thượng đế như một thân thể, mà theo ông thế là thờ ngẫu tượng. *Chỉ dẫn* từng bị cấm ở vài giới rabbi, nhưng ảnh hưởng của nó vượt xa Do Thái giáo: Aquinas, Spinoza và Leibniz đều chịu ảnh hưởng của ông. Câu hỏi của người học trò năm xưa vẫn là câu hỏi của nhiều người hôm nay, khi niềm tin của gia đình gặp những điều học được ở giảng đường.",
],
"works": [
("1168", "*Chú giải Mishnah*", "Trong đó có mười ba nguyên tắc đức tin, lần đầu tiên đưa “tín điều” vào Do Thái giáo"),
("", "*Mishneh Torah*", "Bộ pháp điển 14 quyển, cố chỉ ra rằng mỗi điều luật đều có lý do hợp lý"),
("1190", "*Dalalat al-Ha’irin* (*Chỉ dẫn cho người hoang mang*)", "Tác phẩm triết học chính, viết bằng tiếng Ả Rập"),
("1191", "*Chuyên luận về sự phục sinh*", "Đáp lời buộc tội rằng ông không thật sự tin vào sự sống lại của thân xác"),
],
"thoughts": [
"Thượng đế không có thân thể: những đoạn Kinh thánh nói về tay, mắt, cơn giận của Chúa phải đọc như ẩn dụ, vì lý trí chứng minh được Thượng đế không phải là thân thể hay một lực trong thân thể.",
"**Thần học phủ định** (*negative theology*): càng chứng minh được nhiều điều Thượng đế không phải, ta càng đến gần sự hiểu biết về Ngài; càng gán nhiều thuộc tính, ta càng nhân hóa Ngài. Lời ca ngợi cao nhất là im lặng.",
"Biết giới hạn của lý trí: theo ông, chỉ bằng logic không chứng minh được thế giới được tạo dựng hay vĩnh cửu; ông nghiêng về sáng tạo nhưng thừa nhận mình chỉ làm cán cân lệch đi được một chút.",
"Luật có lý do: mọi điều răn đều nhằm hai đích, sự lành mạnh của thân thể và, cao hơn, sự hoàn thiện của tâm hồn bằng hiểu biết.",
],
"argument": {
"title": "Chỉ nói được điều Thượng đế không phải",
"intro": "Trong phần I của *Chỉ dẫn*, Maimonides lập luận rằng mọi thuộc tính khẳng định gán cho Thượng đế đều dẫn ta đi sai.",
"premises": [
"Thượng đế là một tuyệt đối, đơn nhất, không có bất kỳ sự phức hợp nào.",
"Gán cho Ngài một thuộc tính khẳng định (khôn ngoan, quyền năng, sống) là đưa vào Ngài sự phức hợp, Ngài cộng với thuộc tính, hoặc đặt Ngài lên cùng một thang đo với tạo vật.",
"Phủ định thì không làm thế: nói Ngài “không phải là thân thể”, “không bất lực” chỉ loại bỏ sai lầm, không tuyên bố hiểu được bản chất của Ngài.",
],
"conclusion": "Vậy ta chỉ biết được Thượng đế qua những phủ định (và qua công việc của Ngài trong thế giới), không bao giờ biết Ngài là gì.",
"objection": "Aquinas, người gọi ông là “Rabbi Moses”, phản bác (*Tổng luận Thần học* I, câu 13, mục 2): nếu “Thượng đế sống” chỉ nghĩa là “Ngài không giống vật vô tri”, thì không giải thích được vì sao ta gọi Ngài bằng tên này mà không bằng tên khác; hơn nữa, người nói “Thượng đế sống” rõ ràng muốn nói nhiều hơn thế. Một Thượng đế chỉ còn là chuỗi phủ định thì quá mỏng để người thường thờ phượng.",
"reply": "Maimonides đáp bằng hình ảnh con tàu (*Chỉ dẫn* I.60): một người biết có thứ gọi là “tàu” nhưng không biết nó là gì; lần lượt biết nó không phải khoáng vật, không phải cây, không phẳng như tấm ván, không đặc ruột, đến phủ định thứ mười thì đã gần như hình dung đúng con tàu. Mỗi phủ định được chứng minh là một bước tới gần. Còn lời ca ngợi trong kinh nguyện, ông hiểu hoặc là phủ định, hoặc là nói về việc làm của Thượng đế trong thế giới, không bao giờ là hiểu biết về bản chất của Ngài.",
},
"quote": {
"source": "Maimonides, *Chỉ dẫn cho người hoang mang*, phần I, chương 60 — bản dịch tiếng Anh của M. Friedländer (1904)",
"orig": "In the same manner you will come nearer to the knowledge and comprehension of God by the negative attributes. But you must be careful, in what you negative, to negative by proof, not by mere words, for each time you ascertain by proof that a certain thing, believed to exist in the Creator, must be negatived, you have undoubtedly come one step nearer to the knowledge of God.",
"vi": "Cũng vậy, bạn sẽ đến gần hơn sự hiểu biết và lĩnh hội về Thượng đế nhờ những thuộc tính phủ định. Nhưng phải cẩn thận: điều gì bạn phủ định thì phủ định bằng chứng minh, không chỉ bằng lời; vì mỗi lần bạn xác lập được bằng chứng minh rằng một điều người ta tưởng có nơi Đấng Tạo hóa phải bị phủ định, chắc chắn bạn đã tiến thêm một bước tới sự hiểu biết về Thượng đế.",
"url": "https://www.sacred-texts.com/jud/gfp/gfp070.htm",
},
"misread": [
"**“Thần học phủ định nghĩa là chẳng nói được gì, nên cứ im lặng là xong.”** Thực ra Maimonides đòi mỗi phủ định phải được chứng minh chứ không chỉ nói suông, và chỉ người đã chịu khó học và suy xét mới chứng minh được. Im lặng là đích đến sau một con đường dài suy luận, không phải cái cớ để khỏi suy nghĩ.",
],
"related": [
("lich-su/trung-co.md", "Trung cổ: đức tin gặp lý trí"),
],
"sources": [
("Seeskin, Kenneth, “Maimonides”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/maimonides/"),
("Jacobs, Jonathan, “Maimonides”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/maimonid/"),
("Maimonides, *The Guide for the Perplexed*, bản dịch M. Friedländer (1904), Internet Sacred Text Archive.", "https://www.sacred-texts.com/jud/gfp/index.htm"),
("Thomas Aquinas, *Summa Theologiae* I, câu 13, mục 2, bản dịch Fathers of the English Dominican Province (1920), New Advent.", "https://www.newadvent.org/summa/1013.htm"),
],
},
"aquinas": {
"desc": "Tu sĩ dòng Đa Minh để lại hơn tám triệu chữ với một xác tín: đức tin và lý trí không đối đầu, vì ân sủng không phá hủy tự nhiên mà hoàn thiện nó.",
"bio": [
"Lời mở đầu bộ *Tổng luận Thần học* (*Summa Theologiae*) hứa rằng sách được viết sao cho hợp với việc dạy người mới bắt đầu. Ngày nay hầu như không ai coi bộ sách đồ sộ ấy là sách nhập môn, nhưng lời hứa đó nói lên phong cách của Thomas Aquinas: chia câu hỏi lớn thành những câu nhỏ, nêu những phản bác mạnh nhất trước, rồi mới trả lời từng điểm. Một trang triết học tốt hôm nay vẫn làm như thế.",
"Ông sinh khoảng năm 1225 gần Aquino, giữa Rome và Naples, là con út trong ít nhất chín người con của một gia đình quyền thế có lâu đài ở Roccasecca. Gia đình mong ông giữ vai trò lãnh đạo ở tu viện danh tiếng Monte Cassino, nơi ông học từ nhỏ; nhưng khi lên Naples học, chàng thanh niên bị cuốn theo dòng Đa Minh, một dòng tu mới chuyên giảng đạo và học thuật. Ông gia nhập năm mười chín tuổi; cha mẹ giữ ông ở nhà suốt một năm rồi mới chịu buông. Sau ba năm học triết ở Paris, năm 1248 ông được gửi sang Cologne học với Albert Cả, người tin chắc rằng đức tin Kitô chỉ được lợi khi đối thoại sâu với triết học và khoa học Hy Lạp, Ả Rập.",
"Phần đời còn lại là giảng dạy và viết: hai nhiệm kỳ làm giáo sư thần học ở Đại học Paris, xen giữa là gần mười năm ở Ý, nơi ông phát triển hai bộ *Tổng luận*; ông còn chú giải phần lớn các tác phẩm chính của Aristotle. Chỉ trong khoảng hai mươi năm, ông để lại hơn tám triệu chữ. Cuối năm 1273 ông bỗng ngừng viết; theo lời kể lại, ông nói mọi điều mình đã viết giờ chỉ như rơm rác so với những gì vừa được tỏ lộ. Vài tháng sau, ngày 7 tháng 3 năm 1274, ông mất ở tu viện Fossanova.",
"Ông được phong thánh năm 1323, được tôn làm Tiến sĩ Hội Thánh năm 1567, và từ năm 1879, khi giáo hoàng Leo XIII kêu gọi phục hưng việc học Aquinas, ông trở thành nhà tư tưởng trung tâm của triết học Công giáo. Nhưng không chỉ người Công giáo đọc ông: các cuộc tranh luận hôm nay về **luật tự nhiên** (*natural law*), chiến tranh chính nghĩa, quan hệ giữa linh hồn và thân thể vẫn thường bắt đầu từ những trang của ông.",
],
"works": [
("1252–1256", "*De ente et essentia*", "Về hữu thể và bản chất: tiểu luận ngắn về những khái niệm nền của siêu hình học"),
("1259–1265", "*Summa contra gentiles*", "*Tổng luận chống dân ngoại*, tác phẩm quan trọng thứ hai của ông"),
("k. 1265–1273", "*Summa Theologiae*", "*Tổng luận Thần học*, bỏ dở; chứa “năm con đường” (phần I, câu 2, mục 3)"),
("1270", "*De unitate intellectus contra Averroistas*", "Bác thuyết mọi người chung một trí tuệ, gắn với tên Averroes"),
],
"thoughts": [
"Ân sủng hoàn thiện tự nhiên: lý trí tự nhiên đi được đến đâu thì đi; đức tin không xóa bỏ lý trí mà tiếp nối nó.",
"Luật tự nhiên: nguyên tắc đầu tiên của lý trí thực tiễn là điều thiện phải được làm và theo đuổi, điều ác phải tránh; từ đó lý trí nhận ra những nguyên tắc đạo đức phổ quát (I-II, câu 94).",
"Linh hồn là mô thức của thân thể: con người là một thể thống nhất với một linh hồn duy nhất, không phải linh hồn bị nhốt trong xác, cũng không phải nhiều linh hồn chồng lên nhau.",
"Chiến tranh chính nghĩa cần ba điều kiện: thẩm quyền chính đáng, lý do chính đáng và ý định đúng đắn (II-II, câu 40).",
],
"argument": {
"title": "Con đường thứ hai, từ chuỗi nguyên nhân",
"intro": "Đây là một trong “năm con đường” của *Tổng luận Thần học* (phần I, câu 2, mục 3). Điểm mấu chốt hay bị bỏ qua: Aquinas không nói về một vụ nổ đầu tiên trong quá khứ, mà về những nguyên nhân đang tác động ngay lúc này.",
"premises": [
"Trong thế giới, ta thấy những chuỗi nguyên nhân tác động: cái này làm ra cái kia.",
"Không gì tự làm ra chính nó, vì như thế nó phải có trước chính nó.",
"Một chuỗi nguyên nhân như vậy không thể lùi vô hạn: bỏ nguyên nhân đầu tiên đi thì cũng chẳng còn nguyên nhân trung gian hay kết quả cuối cùng nào.",
],
"conclusion": "Vậy phải có một nguyên nhân tác động đầu tiên, mà theo lời Aquinas, ai cũng gọi là Thượng đế.",
"objection": "Hume, trong *Đối thoại về tôn giáo tự nhiên*, và nhiều người sau ông hỏi: vì sao chuỗi nguyên nhân không thể lùi mãi, như con do cha sinh, cha do ông sinh, cứ thế không cùng? Và nếu đã chấp nhận một điểm dừng không cần nguyên nhân, sao điểm dừng ấy không thể là chính vũ trụ, mà phải là Thượng đế?",
"reply": "Aquinas đã lường trước nửa đầu: ông thừa nhận một chuỗi nguyên nhân “ngẫu nhiên” như cha sinh con có thể kéo dài vô hạn (I, câu 46, mục 2). Thứ không thể lùi vô hạn là chuỗi nguyên nhân “tự thân”, nơi mỗi mắt xích chỉ tác động khi đang được mắt xích trước tác động, như hòn đá chỉ chuyển động khi cây gậy đẩy, cây gậy chỉ đẩy khi bàn tay cầm. Còn câu hỏi vì sao điểm dừng là Thượng đế, ông dành các câu hỏi tiếp theo (câu 3–11) để lập luận rằng nguyên nhân đầu tiên ấy đơn giản, hoàn hảo, vô hạn, bất biến, vĩnh cửu và duy nhất.",
},
"quote": {
"source": "Thomas Aquinas, *Tổng luận Thần học* I, câu 1, mục 8, trả lời phản bác 2 — bản dịch tiếng Anh của Fathers of the English Dominican Province (1920)",
"orig": "Since therefore grace does not destroy nature but perfects it, natural reason should minister to faith as the natural bent of the will ministers to charity.",
"vi": "Vậy, vì ân sủng không phá hủy tự nhiên mà hoàn thiện nó, lý trí tự nhiên phải phục vụ đức tin, như khuynh hướng tự nhiên của ý chí phục vụ đức ái.",
"url": "https://www.newadvent.org/summa/1001.htm",
},
"misread": [
"**“Năm con đường của Aquinas nhằm chứng minh vũ trụ có khởi đầu.”** Thực ra Aquinas cho rằng lý trí không chứng minh được thế giới có khởi đầu trong thời gian; ông tin điều đó nhờ đức tin. Các con đường của ông nhắm vào cái đang duy trì sự tồn tại của mọi vật ngay lúc này, nên chúng vẫn đứng được ngay cả khi vũ trụ vĩnh cửu.",
"**“Thời ấy ai cũng đồng thuận với Aquinas.”** Thực ra năm 1277, ba năm sau khi ông mất, giám mục Paris kết án 219 mệnh đề, trong đó có những mệnh đề dường như nhắm vào học thuyết của ông; cũng năm ấy ở Oxford, hai học thuyết đặc trưng của ông bị kết án.",
],
"related": [
("cau-hoi/luan-chung-ton-giao.md", "Có thể chứng minh Chúa tồn tại bằng lý trí?"),
("lich-su/trung-co.md", "Trung cổ: đức tin gặp lý trí"),
("cau-hoi/chien-tranh-chinh-dang.md", "Chiến tranh có bao giờ chính đáng không?"),
("cau-hoi/pho-quat.md", "Cái đỏ của hoa hồng và cái đỏ của máu: phổ quát có thật không?"),
("cau-hoi/van-de-su-du.md", "Nếu Chúa toàn năng và tốt lành, vì sao có đau khổ?"),
],
"sources": [
("Pasnau, Robert, “Thomas Aquinas”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/aquinas/"),
("Thomas Aquinas, *Summa Theologiae*, bản dịch Fathers of the English Dominican Province (1920), New Advent: I, câu 1, 2, 46; I-II, câu 94; II-II, câu 40.", "https://www.newadvent.org/summa/"),
("Thomas Aquinas, *Summa Theologica, Part I (Prima Pars)*, Project Gutenberg (lời mở đầu).", "https://www.gutenberg.org/ebooks/17611"),
],
},
"hobbes": {
"desc": "Triết gia của nỗi sợ và trật tự: vì sao những người không hề độc ác vẫn rơi vào “chiến tranh của mọi người chống mọi người”, và vì sao cần một Leviathan.",
"bio": [
"Một tối, đèn giao thông ở ngã tư đông xe bỗng tắt. Không ai là kẻ xấu, nhưng ai cũng sợ nhường thì thiệt, và chỉ vài phút sau giao lộ đã tắc cứng. Thomas Hobbes đã gọi tên kiểu tình huống ấy: điều xảy ra khi không có “một quyền lực chung giữ cho mọi người khiếp sợ”. Câu hỏi của ông thẳng thừng: nếu không có nhà nước thì sao, và vì sao ta phải vâng lời một quyền lực mà ta chưa từng ký giấy đồng ý?",
"Hobbes sinh ngày 5 tháng 4 năm 1588 ở Malmesbury, miền tây nam nước Anh, đúng năm hạm đội Armada của Tây Ban Nha kéo đến định đánh chiếm nước Anh. Về già, trong bài thơ tự thuật bằng tiếng Latin, ông kể rằng khi tin đồn hạm đội sắp tới lan khắp các thị trấn, mẹ ông sợ đến mức “sinh đôi: tôi và nỗi sợ”. Một người chú làm nghề găng tay nuôi ông ăn học ở Oxford, nơi ông thấy triết học kinh viện theo Aristotle chẳng mấy hữu ích. Từ năm 1608, ông vào làm cho dòng họ quý tộc Cavendish, ban đầu là gia sư, rồi gắn bó với họ gần như suốt đời; nhờ vậy ông có sách để đọc và được theo họ đi khắp châu Âu.",
"Cuối năm 1640, khi nước Anh trượt vào nội chiến, Hobbes, vốn thuộc phe bảo hoàng và có lý do sợ bị trừng phạt vì đã bênh vực chủ quyền tuyệt đối, trốn sang Paris và ở đó mười năm. Ông viết một bộ phản bác in kèm *Suy niệm* của Descartes (1641), rồi cuối thời lưu vong thì viết *Leviathan* (1651). Tên sách lấy từ con thủy quái trong sách Gióp: nhà nước là một “vị thần phải chết” do chính con người tạo ra bằng khế ước.",
"Về lại Anh năm 1651, ông còn sống gần ba mươi năm, tranh luận không mệt mỏi (chẳng hạn với giám mục Bramhall về tự do và tất yếu), và ngoài tám mươi tuổi còn dịch *Iliad* và *Odyssey*. Ông mất ngày 4 tháng 12 năm 1679, thọ 91 tuổi. Hobbes được xem là người đặt nền cho triết học chính trị hiện đại: quyền lực phải được biện minh bằng những lý do mà mỗi người, tự tính toán cho mình, có thể chấp nhận.",
],
"works": [
("1640", "*The Elements of Law, Natural and Politic*", "Các nguyên lý của luật tự nhiên và luật chính trị; lưu hành dạng chép tay, in năm 1650"),
("1642", "*De Cive*", "Về công dân"),
("1651", "*Leviathan*", "Về chất liệu, hình thức và quyền lực của nhà nước"),
("1655", "*De Corpore*", "Về vật thể; nơi có biến thể “con tàu thứ hai” của câu đố con tàu Theseus"),
("1658", "*De Homine*", "Về con người"),
],
"thoughts": [
"**Trạng thái tự nhiên** (*state of nature*) là một mô hình hơn là một giai đoạn lịch sử. Xung đột có ba nguồn: cạnh tranh (vì lợi), nghi kỵ (vì an toàn), ham danh (vì tiếng tăm, có khi chỉ vì “một lời nói, một nụ cười”). Không cần ai độc ác, chỉ cần không có ai phân xử.",
"Lý trí là tính toán: suy luận “chẳng qua là tính toán (cộng và trừ)” (*Leviathan*, chương 5). Gọi ông là ông tổ của trí tuệ nhân tạo, như vài người vẫn làm, thì theo SEP là hơi quá.",
"Tự do và tất yếu không loại trừ nhau: dòng nước chảy theo lòng kênh vừa tự do vừa tất yếu, hành động của ta cũng vậy (*Leviathan*, chương 21). Đây là một hình thức cổ điển của **tương thích luận** (*compatibilism*).",
"Quyền lực tuyệt đối nhưng có điều kiện: không ai có nghĩa vụ tự giết hay tự hại mình, và nghĩa vụ vâng lời chỉ kéo dài chừng nào chủ quyền còn bảo vệ được dân, vì “mục đích của sự vâng lời là sự bảo vệ”.",
],
"argument": {
"title": "Từ trạng thái tự nhiên đến Leviathan",
"intro": "Theo cách tái dựng phổ biến của *Leviathan*, chương 13–17:",
"premises": [
"Khi không có quyền lực chung, con người đại khái ngang sức (kẻ yếu nhất vẫn giết được kẻ mạnh nhất bằng mưu mẹo hay liên minh), cùng muốn những thứ khan hiếm, và không tin nhau.",
"Trong hoàn cảnh ấy, ra tay trước là khôn ngoan với từng người, nên đó là “chiến tranh của mọi người chống mọi người”, nơi đời người “cô độc, nghèo nàn, bẩn thỉu, tàn bạo và ngắn ngủi”.",
"Người có lý trí muốn trước hết thoát khỏi cái chết bạo lực, nên muốn hòa bình.",
"Lời hứa suông không giữ được hòa bình (“khế ước không có thanh gươm chỉ là lời nói”); chỉ một quyền lực chung đủ mạnh mới buộc mọi người giữ lời.",
],
"conclusion": "Vậy người có lý trí có lý do cùng thỏa thuận trao quyền cho một chủ quyền (một người hay một hội đồng) có quyền lực không bị chia cắt, và vâng lời chủ quyền ấy.",
"objection": "Locke (*Khảo luận thứ hai về chính quyền*, §93) chế giễu: ai lại cẩn thận đề phòng chồn và cáo, rồi yên tâm để sư tử nuốt mình? Trao quyền tuyệt đối để thoát bạo lực giữa người với người là mở cửa cho bạo lực lớn hơn từ chính kẻ cầm quyền.",
"reply": "Hobbes đáp rằng gánh nặng của một chính quyền, dù tệ đến đâu, cũng “khó mà cảm thấy” so với tai họa của nội chiến; còn quyền lực bị chia cắt hay bị giới hạn sẽ sinh ra tranh chấp không ai phân xử, tức là quay về chiến tranh. Vả lại, chủ quyền của ông không đòi phục tùng vô điều kiện (xem ý cuối ở trên).",
},
"quote": {
"source": "Thomas Hobbes, *Leviathan* (1651), chương 13 — nguyên văn tiếng Anh, chính tả theo bản in đầu tiên",
"orig": "For as the nature of Foule weather, lyeth not in a showre or two of rain; but in an inclination thereto of many dayes together: So the nature of War, consisteth not in actuall fighting; but in the known disposition thereto, during all the time there is no assurance to the contrary. All other time is PEACE.",
"vi": "Cũng như bản chất của thời tiết xấu không nằm ở một hai cơn mưa rào mà ở xu hướng mưa kéo dài nhiều ngày, bản chất của chiến tranh không nằm ở việc đánh nhau thật, mà ở thái độ sẵn sàng đánh nhau mà ai cũng biết, suốt thời gian không có gì bảo đảm điều ngược lại. Mọi thời gian khác là HÒA BÌNH.",
"url": "https://www.gutenberg.org/ebooks/3207",
},
"misread": [
"**“Hobbes cho rằng con người bẩm sinh độc ác.”** Thực ra, cũng trong chương 13, ông viết rằng mình không buộc tội bản tính con người: ham muốn và đam mê “tự chúng không phải là tội”. Chiến tranh nảy sinh từ hoàn cảnh chứ không từ sự xấu xa; cách đọc “theo Hobbes, ai cũng hoàn toàn ích kỷ” nay bị phần lớn giới nghiên cứu bác bỏ.",
"**“Hobbes bênh vực chế độ quân chủ chuyên chế.”** Thực ra, điều ông bảo vệ là chủ quyền không bị chia cắt, dù nằm trong tay một vị vua hay một hội đồng; ông chỉ nghiêng về quân chủ vì vài lý do thực dụng.",
],
"related": [
("cau-hoi/khe-uoc-xa-hoi.md", "Vì sao phải vâng lời nhà nước? Khế ước xã hội"),
("cau-hoi/ban-tinh-con-nguoi.md", "Bản tính con người thiện hay ác?"),
("bat-dau/index.md", "Triết học là gì, và không phải là gì?"),
("cau-hoi/cai-toi.md", "Cái “tôi” là gì? Bạn của mười năm trước có còn là bạn?"),
],
"sources": [
("Duncan, Stewart, “Thomas Hobbes”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/hobbes/"),
("Lloyd, Sharon A. & Susanne Sreedhar, “Hobbes’s Moral and Political Philosophy”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/hobbes-moral/"),
("Williams, Garrath, “Hobbes, Thomas: Moral and Political Philosophy”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/hobmoral/"),
("Hobbes, Thomas, *Leviathan* (1651), Project Gutenberg.", "https://www.gutenberg.org/ebooks/3207"),
("Hobbes, Thomas, bài thơ tự thuật *Vita* và các chương của *De Corpore*, trong Mary Whiton Calkins (tuyển), *The Metaphysical System of Hobbes*, Chicago: Open Court, 1905 — Internet Archive.", "https://archive.org/details/cu31924029010565"),
],
},
"descartes": {
"desc": "Nhà toán học nghi ngờ mọi thứ để tìm một điều chắc chắn: “Tôi tư duy, vậy tôi tồn tại” — và để lại cho ta bài toán tâm trí và thân xác.",
"bio": [
"Có bao giờ bạn tỉnh dậy mà vẫn tưởng giấc mơ là thật? René Descartes biến trải nghiệm quen thuộc ấy thành một phép thử: nếu tôi không chắc mình đang thức, thì tôi thật sự biết được gì? Thay vì sửa từng niềm tin sai, ông quyết định dỡ cả ngôi nhà tri thức đến tận nền, gạt bỏ “đất xốp và cát” để tìm “đá hay đất sét” mà xây lại.",
"Descartes sinh ngày 31 tháng 3 năm 1596 ở La Haye, vùng Touraine (thị trấn nay mang tên ông); mẹ mất khi ông mới hơn một tuổi. Học xong trường dòng Tên La Flèche và lấy bằng luật, năm 1618 ông sang Hà Lan làm quân nhân tình nguyện. Đêm 10 tháng 11 năm 1619, trú đông ở một thị trấn miền nam nước Đức, ông có ba giấc mơ mà ông hiểu là một sứ mệnh: cải tổ toàn bộ tri thức, bắt đầu từ triết học. Từ cuối năm 1628, ông sống ở Hà Lan, thường đổi chỗ ở theo châm ngôn “ai sống kín đáo là sống tốt”.",
"Trước hết, ông là một nhà toán học lớn, người mở đường cho hình học giải tích (hệ tọa độ vuông góc về sau mang tên ông để ghi công). Nghe tin Galileo bị kết án năm 1633, ông cất bản thảo *Thế giới* đi không in. *Suy niệm về triết học thứ nhất* (1641) được in kèm các bộ phản bác của Hobbes, Gassendi, Arnauld và những người khác, cùng lời đáp của ông. Từ năm 1643, ông thư từ với công chúa Elisabeth xứ Bohemia, người đặt câu hỏi hóc búa nhất cho học thuyết của ông.",
"Năm 1649, ông nhận lời mời của nữ hoàng Christina sang Thụy Điển, lâm bệnh và mất ngày 11 tháng 2 năm 1650. Ông để lại hai món quà khó chịu: một phương pháp (chỉ chấp nhận điều mình thấy rõ ràng, phân minh) và một câu hỏi chưa ai khép lại được (tâm trí và thân xác liên hệ thế nào?). Mỗi khi ta hỏi liệu thế giới có phải là một mô phỏng, hay máy có “thật sự” nghĩ không, ta đang đi tiếp con đường ông mở.",
],
"works": [
("1637", "*Discours de la méthode*", "Luận về phương pháp, kèm ba tiểu luận Quang học, Khí tượng học, Hình học"),
("1641", "*Meditationes de prima philosophia*", "Suy niệm về triết học thứ nhất, kèm các bộ phản bác và lời đáp"),
("1644", "*Principia philosophiae*", "Các nguyên lý của triết học"),
("1649", "*Les passions de l'âme*", "Những đam mê của tâm hồn"),
("1664", "*Le Monde*", "Thế giới: cất đi sau vụ Galileo, in sau khi ông mất"),
],
"thoughts": [
"Hoài nghi có phương pháp: nghi ngờ không phải để dừng ở nghi ngờ. Ông tự phân biệt mình với những người hoài nghi “chỉ nghi ngờ để mà nghi ngờ”; mục đích của ông là tìm điều chắc chắn.",
"*Cogito*: dù có một kẻ lừa đảo quyền năng tột bậc, chừng nào tôi còn đang nghĩ thì tôi tồn tại. Đây mới là viên đá đầu tiên: từ đó ông còn phải chứng minh Thượng đế tồn tại và không lừa dối, rồi mới tin lại được vào thế giới bên ngoài.",
"Tiêu chuẩn rõ ràng và phân minh: điều gì tôi nhận thức thật rõ ràng, phân minh thì đúng. Arnauld vặn lại: dùng tiêu chuẩn này để chứng minh Thượng đế, rồi dùng Thượng đế để bảo đảm tiêu chuẩn, phải chăng là đi vòng tròn?",
"**Nhị nguyên luận** (*dualism*): tâm trí là vật biết tư duy, không có quảng tính; vật chất là vật có quảng tính, không tư duy. Thân thể người và động vật vận hành như cỗ máy, ý tưởng mở đường cho sinh lý học cơ giới.",
],
"argument": {
"title": "Tâm trí khác biệt với thân thể",
"intro": "Tâm trí có phải chỉ là một phần của thân thể? Ở *Suy niệm* VI, Descartes lập luận rằng không; theo cách tái dựng phổ biến:",
"premises": [
"Tôi có một ý niệm rõ ràng và phân minh về chính mình như một vật biết tư duy, không có quảng tính.",
"Tôi có một ý niệm rõ ràng và phân minh về thân thể như một vật có quảng tính, không tư duy.",
"Những gì tôi hiểu rõ ràng và phân minh là tách biệt thì Thượng đế có thể làm cho chúng tồn tại tách rời; mà hai thứ có thể tồn tại tách rời thì thật sự là hai thứ khác nhau.",
],
"conclusion": "Vậy tâm trí (cái “tôi”) khác biệt thực sự với thân thể và có thể tồn tại không cần thân thể.",
"objection": "Hình dung được A tách khỏi B chưa chứng tỏ A thật sự tách được khỏi B; có thể ta chỉ đang không biết đủ. (SEP ví von: Joker có thể nghi ngờ Bruce Wayne còn sống trong khi biết chắc Batman đang đứng trước mặt, nhưng hai người là một.) Và dù chấp nhận nhị nguyên, câu hỏi của Elisabeth (1643) vẫn còn đó: một tâm trí không có quảng tính làm sao đẩy được cánh tay?",
"reply": "Descartes đáp rằng ở *Suy niệm* VI, ông không dựa vào việc nghi ngờ được thân thể, mà dựa vào hiểu biết rõ ràng, phân minh về bản chất của tư duy và của quảng tính. Về sự tương tác, chính ông thừa nhận với Elisabeth rằng mình chưa có câu trả lời tốt; người đi sau tìm những lối ra khác: thuyết duyên cớ (Thượng đế làm trung gian), nhất nguyên của Spinoza, hòa hợp tiền định của Leibniz.",
},
"quote": {
"source": "René Descartes, *Luận về phương pháp* (1637), phần IV — bản dịch tiếng Anh của John Veitch",
"orig": "But immediately upon this I observed that, whilst I thus wished to think that all was false, it was absolutely necessary that I, who thus thought, should be somewhat; and as I observed that this truth, I think, therefore I am (COGITO ERGO SUM), was so certain and of such evidence that no ground of doubt, however extravagant, could be alleged by the sceptics capable of shaking it […]",
"vi": "Nhưng ngay sau đó tôi nhận ra rằng, trong khi tôi muốn nghĩ như thế rằng mọi thứ đều sai, thì chính tôi, kẻ đang nghĩ như thế, nhất thiết phải là một cái gì đó; và thấy rằng chân lý này, tôi tư duy, vậy tôi tồn tại, chắc chắn và hiển nhiên đến mức mọi lý do nghi ngờ của những người hoài nghi, dù ngông cuồng đến đâu, cũng không lay chuyển được […]",
"url": "https://www.gutenberg.org/ebooks/59",
},
"misread": [
"**“‘Cogito, ergo sum’ là câu trong *Suy niệm*, và là một tam đoạn luận.”** Thực ra, câu ấy xuất hiện trước hết bằng tiếng Pháp (“je pense, donc je suis”) trong *Luận về phương pháp* (1637), rồi bằng tiếng Latin trong *Các nguyên lý của triết học* (1644); *Suy niệm* II viết “tôi là, tôi tồn tại”. Descartes cũng nói rõ ông không suy ra sự tồn tại từ tư duy bằng tam đoạn luận, mà nhận ra nó bằng trực giác.",
"**“Descartes là một người hoài nghi.”** Thực ra, ông dùng hoài nghi làm công cụ để đạt tới sự chắc chắn. Hume phê phán chính chỗ này: nếu thật sự nghi ngờ cả các năng lực của mình, ta không còn công cụ nào để thoát ra.",
],
"related": [
("doc/descartes-suy-niem.md", "Đọc “Suy niệm” I–II của Descartes"),
("cau-hoi/van-de-tam-tri.md", "Thân xác và tâm trí: vấn đề lâu đời nhất của triết học"),
("cau-hoi/linh-hon.md", "Con người có linh hồn không?"),
("cau-hoi/tri-thuc.md", "Biết một điều nghĩa là gì?"),
("cau-hoi/mo-phong.md", "Ta có đang sống trong mô phỏng?"),
],
"sources": [
("Hatfield, Gary, “René Descartes”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/descartes/"),
("Newman, Lex, “Descartes’ Epistemology”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/descartes-epistemology/"),
("Descartes, René, *Discourse on the Method* (1637), bản dịch John Veitch, Project Gutenberg.", "https://www.gutenberg.org/ebooks/59"),
("Descartes, René, *Meditations on First Philosophy* (1641), bản dịch John Veitch, Wikisource.", "https://en.wikisource.org/wiki/Meditations_on_First_Philosophy"),
("Hume, David, *An Enquiry Concerning Human Understanding* (1748), mục XII, Project Gutenberg.", "https://www.gutenberg.org/ebooks/9662"),
],
},
"pascal": {
"desc": "Thiên tài toán học và nhà biện hộ Kitô giáo: con người nhỏ bé giữa hai vô tận, lý trí có giới hạn, và một ván cược nổi tiếng về đức tin.",
"bio": [
"Mỗi lần xem dự báo “70% khả năng mưa” hay cân nhắc có nên mua bảo hiểm, bạn đang dùng một công cụ mà Blaise Pascal góp phần đặt nền: lý thuyết xác suất, ra đời từ những lá thư ông trao đổi với Fermat năm 1654 về các bài toán cờ bạc. Vậy mà người ta nhớ ông nhiều nhất vì một ván cược khác: đặt cược vào sự tồn tại của Chúa.",
"Pascal sinh ngày 19 tháng 6 năm 1623 ở Clermont (nay là Clermont-Ferrand, Pháp). Mẹ mất khi ông lên ba; ông không đến trường mà được cha, một nhà toán học giỏi, dạy ở nhà. Tuổi trẻ của ông là một chuỗi thành tựu: khảo luận về đường conic năm 1640, khi mới khoảng mười sáu tuổi; chiếc máy tính cơ học ra mắt năm 1645; các thí nghiệm khí áp, trong đó năm 1648 người anh rể theo chỉ dẫn của ông mang ống thủy ngân lên núi Puy-de-Dôme và thấy cột thủy ngân thấp dần theo độ cao. Theo lời người chị, từ năm mười tám tuổi ông không ngày nào không đau.",
"Năm 1646, gia đình ông tiếp xúc với phái Jansen, một trào lưu Công giáo khắc khổ theo tinh thần thánh Augustine. Đêm 23 tháng 11 năm 1654, Pascal trải qua một trải nghiệm tôn giáo mãnh liệt; ông ghi lại trên một mảnh giấy (*Mémorial*), khâu vào lớp lót áo và mang theo đến lúc chết. Từ đó ông dồn sức cho tôn giáo, chỉ thỉnh thoảng quay lại với toán học. Năm 1656–1657, dưới một bút danh, ông viết loạt *Thư gửi người tỉnh lẻ*, châm biếm các nhà thần học dòng Tên để bênh vực Antoine Arnauld.",
"Những năm cuối, ông ghi chép cho một cuốn sách bênh vực Kitô giáo nhưng không kịp viết xong: ông mất ngày 19 tháng 8 năm 1662, mới 39 tuổi. Các ghi chép được in năm 1670 với tên *Pensées* (*Suy tưởng*); vì chúng không có thứ tự rõ ràng, mỗi ấn bản đánh số một kiểu (trang này dùng số của Brunschvicg, như bản dịch tiếng Anh của Trotter). Ông vẫn được đọc vì đã nhìn thẳng vào thân phận con người, nhỏ bé giữa hai vô tận, và nói thành lời nỗi sợ trước “sự im lặng đời đời của những không gian vô tận này”.",
],
"works": [
("1640", "*Essai pour les coniques*", "Khảo luận về đường conic"),
("1647", "*Expériences nouvelles touchant le vide*", "Những thí nghiệm mới về chân không"),
("1653–1654", "*Traité du triangle arithmétique*", "Khảo luận về tam giác số học (“tam giác Pascal”), in sau khi ông mất"),
("1656–1657", "*Les Provinciales*", "Thư gửi người tỉnh lẻ"),
("1670", "*Pensées*", "Suy tưởng: ghi chép cho một cuốn sách bênh vực Kitô giáo, in sau khi ông mất"),
],
"thoughts": [
"Hai vô tận: giữa cái vô cùng lớn của vũ trụ và cái vô cùng nhỏ của vật chất, con người là “một hư không so với vô tận, một tất cả so với hư không” (đoạn 72). Biết mình đứng ở khoảng giữa là bước đầu của sự khiêm tốn trí tuệ.",
"Giải trí (*divertissement*): săn bắn, cờ bạc, chuyện phiếm giúp ta khỏi phải nghĩ về thân phận mình; “mọi bất hạnh của con người đều đến từ một điều: họ không thể ngồi yên trong phòng mình” (đoạn 139). Người đọc hôm nay khó mà không nghĩ đến chiếc điện thoại trong túi.",
"Lý trí biết giới hạn của nó: “bước cuối cùng của lý trí là nhận ra có vô số điều vượt quá nó” (đoạn 267). Pascal cũng coi các chứng minh siêu hình về Chúa là ít giá trị; lời biện hộ của ông nhắm vào cả con người, không chỉ vào lý trí.",
],
"argument": {
"title": "Canh bạc của Pascal",
"intro": "Nếu lý trí không phân xử được Chúa có tồn tại hay không, ta nên sống thế nào? Đoạn “Vô hạn – không” (*Infini – rien*; đoạn 233 theo Brunschvicg, 418 theo Lafuma), theo cách tái dựng phổ biến:",
"premises": [
"Lý trí không quyết định được Chúa có tồn tại hay không (“lý trí không quyết định được gì ở đây”).",
"Nhưng ta không thể đứng ngoài: sống là đã đặt cược, hoặc như thể Chúa tồn tại, hoặc như thể Ngài không tồn tại (“bạn đã ở trên thuyền rồi”).",
"Nếu tin mà Chúa tồn tại, ta được hạnh phúc vô hạn; nếu tin mà Ngài không tồn tại, ta chỉ mất một thứ hữu hạn.",
"Khi có thể được vô hạn mà chỉ phải đặt cược hữu hạn, và cơ hội thắng không bằng không, thì đặt cược vào bên ấy là hợp lý.",
],
"conclusion": "Vậy người có lý trí nên “đặt cược không do dự rằng Ngài tồn tại”, tức là sống và vun đắp niềm tin.",
"objection": "“Nhiều thần”: Diderot (1746) nhận xét một vị imam cũng có thể lập luận y như thế; nếu nhiều tôn giáo cùng hứa phần thưởng vô hạn, ma trận của Pascal không chỉ ra nên cược vào đâu. Ngoài ra, niềm tin không bật tắt được theo ý muốn, và một Thượng đế toàn tri có thể không trân trọng thứ đức tin vì tính toán.",
"reply": "Pascal đã lường trước phản bác thứ hai: người “không thể tin” hãy bắt đầu bằng cách hành động như người tin (dùng nước thánh, xin lễ), bớt đi đam mê, và niềm tin sẽ dần đến. Với phản bác “nhiều thần”, những người bênh vực cho rằng canh bạc nhắm vào người đang phân vân giữa vài lựa chọn có thật trong đời mình, không phải giữa mọi vị thần có thể tưởng tượng ra, và không phải giả thuyết nào cũng đáng tin như nhau.",
},
"quote": {
"source": "Blaise Pascal, *Pensées* (1670), đoạn 347 theo Brunschvicg (200 theo Lafuma) — bản dịch tiếng Anh của W. F. Trotter (1910)",
"orig": "Man is but a reed, the most feeble thing in nature; but he is a thinking reed. […] But, if the universe were to crush him, man would still be more noble than that which killed him, because he knows that he dies and the advantage which the universe has over him; the universe knows nothing of this.",
"vi": "Con người chỉ là một cây sậy, thứ yếu ớt nhất trong tự nhiên; nhưng đó là một cây sậy biết suy nghĩ. […] Nhưng nếu vũ trụ có nghiền nát con người, con người vẫn cao quý hơn cái đã giết mình, vì con người biết mình chết và biết ưu thế của vũ trụ đối với mình; còn vũ trụ chẳng biết gì về điều đó.",
"url": "https://www.gutenberg.org/ebooks/18269",
},
"misread": [
"**“Canh bạc Pascal là một chứng minh rằng Chúa tồn tại.”** Thực ra, Pascal mở đầu bằng thừa nhận lý trí không quyết định được gì ở đây. Canh bạc chỉ cho rằng *tin* là lựa chọn khôn ngoan: đó là lý do thực dụng, không phải bằng chứng.",
"**“‘Trái tim có những lý lẽ mà lý trí không biết’ (đoạn 277) nghĩa là cứ nghe theo cảm xúc.”** Thực ra, “trái tim” của Pascal là năng lực nắm bắt trực tiếp: nhờ nó ta biết các nguyên lý đầu tiên như không gian, thời gian, chuyển động, con số, rồi lý trí xây tiếp trên đó (đoạn 282 theo Brunschvicg, 110 theo Lafuma). Ông cảnh giác cả hai thái cực: “loại bỏ lý trí, và chỉ thừa nhận lý trí” (đoạn 253).",
],
"related": [
("cau-hoi/duc-tin-ly-tri.md", "Có nên tin mà không cần bằng chứng?"),
("cau-hoi/luan-chung-ton-giao.md", "Có thể chứng minh Chúa tồn tại bằng lý trí?"),
],
"sources": [
("Clarke, Desmond & William Wood, “Blaise Pascal”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/pascal/"),
("Hájek, Alan, “Pascal’s Wager”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/pascal-wager/"),
("Simpson, David, “Pascal, Blaise”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/pascal-b/"),
("Pascal, Blaise, *Pensées* (1670), bản dịch tiếng Anh của W. F. Trotter (1910), Project Gutenberg.", "https://www.gutenberg.org/ebooks/18269"),
("*Pensées de Blaise Pascal*, ấn bản điện tử có bảng đối chiếu số đoạn Brunschvicg – Lafuma – Sellier.", "https://www.penseesdepascal.fr/"),
],
},
"locke": {
"desc": "Người đặt nền cho duy nghiệm luận Anh: mọi ý niệm đến từ kinh nghiệm, chính quyền chỉ chính đáng khi được dân ủy thác, và ý thức nối dài làm nên cái tôi.",
"bio": [
"Một đứa trẻ sinh ra đã biết “cái gì có thì có” chưa? Hay phải nhìn, chạm, nếm, nghe rồi mới có những ý niệm đầu tiên? John Locke cược vào khả năng thứ hai. Hãy hình dung tâm trí lúc mới sinh như một tờ giấy trắng, ông đề nghị, rồi hỏi: mọi chữ trên đó từ đâu mà có?",
"Locke sinh năm 1632 ở Wrington, miền tây nam nước Anh, trong một gia đình Thanh giáo khiêm tốn; cha ông là một luật sư từng đi lính kỵ binh bên phe Thanh giáo thời nội chiến. Ông học ở trường Westminster rồi Christ Church, Oxford, chán lối triết học kinh viện theo Aristotle được dạy ở đó, và tìm thấy hứng thú ở khoa học thực nghiệm: ông học y, coi Robert Boyle là thầy, và đọc Descartes như một lối thoát khỏi kinh viện. Năm 1666, một cuộc gặp tình cờ khiến ông thành bác sĩ riêng, thư ký rồi bạn thân của Lord Ashley, về sau là bá tước Shaftesbury, một trong những người giàu và có thế lực nhất nước Anh.",
"Gắn với Shaftesbury, Locke bị cuốn vào chính trường thời khủng hoảng Exclusion, khi phe đối lập tìm cách ngăn người em theo Công giáo của vua Charles II lên ngôi. Năm 1683, sau khi âm mưu Rye House bại lộ, ông sang lưu vong ở Hà Lan và hoàn tất bộ *Khảo luận về hiểu biết của con người* tại đó. Cách mạng Vinh quang cho ông trở về vào tháng 2 năm 1689. Ngay năm ấy, hai tác phẩm làm nên tên tuổi ông ra đời gần như cùng lúc: *Khảo luận* và *Hai khảo luận về chính quyền* (cuốn sau in khuyết danh); trang tên sách của cả hai ghi năm 1690.",
"Những năm cuối đời, Locke sống ở Oates (hạt Essex) trong nhà của bạn ông, nhà triết học Damaris Masham. Ông sửa *Khảo luận* qua nhiều lần tái bản; chương nổi tiếng về đồng nhất cá nhân được thêm vào bản thứ hai năm 1694. Ông mất ngày 28 tháng 10 năm 1704. Mỗi khi ta nói “tôi có quyền”, đòi chính quyền phải dựa trên sự đồng thuận của dân, hay hỏi bạn của mười năm trước có còn là bạn, ta đang dùng những khái niệm Locke góp phần định hình.",
],
"works": [
("1689", "*A Letter Concerning Toleration*", "Thư về lòng khoan dung: không được dùng cưỡng bức để đưa ai đến đức tin; bản gốc tiếng Latin, in khuyết danh"),
("1689", "*An Essay Concerning Human Understanding*", "Khảo luận về hiểu biết của con người (trang tên sách ghi 1690)"),
("1689", "*Two Treatises of Government*", "Hai khảo luận về chính quyền, in khuyết danh (trang tên sách ghi 1690)"),
("1693", "*Some Thoughts Concerning Education*", "Vài suy nghĩ về giáo dục"),
],
"thoughts": [
"Mọi “vật liệu” của tri thức đến từ hai nguồn: **cảm giác** (*sensation*) về thế giới bên ngoài, và **phản tỉnh** (*reflection*) về hoạt động của chính tâm trí (*Khảo luận*, quyển II, chương 1). Đây là nền của **duy nghiệm luận** (*empiricism*).",
"**Đồng nhất cá nhân** (*personal identity*): điều làm bạn hôm nay là cùng một người với bạn mười năm trước không phải cùng thân xác hay cùng linh hồn, mà là ý thức nối dài về quá khứ. Thí nghiệm tư duy của ông: linh hồn một hoàng tử nhập vào thân xác một anh thợ giày.",
"Chính quyền là sự ủy thác: con người lập ra xã hội chính trị để bảo vệ “sinh mạng, tự do và tài sản” (ông gọi chung là *property*); khi chính quyền phản bội sự ủy thác, dân có quyền thay đổi nó (*Khảo luận thứ hai*, §123, §149).",
"Tài sản từ lao động: ai “trộn” sức lao động của mình vào vật ở trạng thái tự nhiên thì biến nó thành của mình, miễn là “còn đủ, và tốt như thế, cho người khác” (§27). Giới nghiên cứu cũng chỉ ra mặt trái: lý thuyết này cho phép Locke coi đất săn bắn của người bản địa châu Mỹ là đất bỏ trống, ai khai phá thì được.",
],
"argument": {
"title": "Không có nguyên lý bẩm sinh",
"intro": "Thời Locke, nhiều người tin một số chân lý như “cái gì có thì có” được khắc sẵn trong tâm trí từ lúc sinh ra, bằng chứng là ai cũng đồng ý. Locke phản bác (*Khảo luận*, quyển I, chương 2):",
"premises": [
"Nếu có nguyên lý bẩm sinh, mọi người phải biết và đồng ý với nó, vì nói một điều “khắc trong tâm trí” mà tâm trí không hề nhận biết thì gần như vô nghĩa.",
"Trẻ nhỏ (và, theo cách nói của Locke, những người thiểu năng) không hề có chút hiểu biết nào về các nguyên lý ấy.",
"Kể cả khi mọi người cùng đồng ý một điều, sự đồng thuận ấy vẫn có thể giải thích bằng cách khác, qua kinh nghiệm và học hỏi.",
],
"conclusion": "Vậy không có nguyên lý bẩm sinh; tri thức phải được xây từ kinh nghiệm.",
"objection": "Leibniz, trong *Những khảo luận mới* (xong năm 1704), đáp rằng ý niệm bẩm sinh có thể nằm trong tâm trí dưới dạng thiên hướng, như vân trong khối cẩm thạch gợi sẵn hình tượng cho nhà điêu khắc. Hơn nữa, kinh nghiệm chỉ cho ta từng trường hợp riêng lẻ, không bao giờ cho được tính tất yếu và phổ quát của chân lý toán học.",
"reply": "Locke đã lường trước: nếu “bẩm sinh” chỉ có nghĩa là tâm trí có *khả năng* biết, thì mọi chân lý ta từng biết đều “bẩm sinh”, và khái niệm ấy trở nên rỗng. Ông cũng không phủ nhận các năng lực bẩm sinh, chỉ phủ nhận nội dung có sẵn; cuộc tranh luận giữa thiên hướng bẩm sinh và học hỏi vẫn còn tiếp diễn đến hôm nay.",
},
"quote": {
"source": "John Locke, *Khảo luận về hiểu biết của con người* (1689), quyển II, chương 1, §2 — nguyên văn tiếng Anh",
"orig": "Let us then suppose the mind to be, as we say, white paper, void of all characters, without any ideas:—How comes it to be furnished? […] Whence has it all the MATERIALS of reason and knowledge? To this I answer, in one word, from EXPERIENCE.",
"vi": "Vậy hãy giả sử tâm trí, như ta vẫn nói, là một tờ giấy trắng, không có chữ nào, không có ý niệm nào: làm sao nó được lấp đầy? […] Nó lấy đâu ra mọi VẬT LIỆU của lý trí và tri thức? Tôi xin trả lời bằng một chữ: từ KINH NGHIỆM.",
"url": "https://www.gutenberg.org/ebooks/10615",
},
"misread": [
"**“Theo Locke, con người sinh ra hoàn toàn trống rỗng.”** Thực ra, ông chỉ bác bỏ ý niệm và nguyên lý bẩm sinh, không bác bỏ năng lực bẩm sinh: ta sinh ra đã có khả năng cảm nhận, ghi nhớ, phân biệt và kết hợp ý niệm. Trong *Khảo luận*, hình ảnh ông dùng là “tờ giấy trắng” (*white paper*); chữ Latin *tabula rasa* là cách gọi quen thuộc về sau.",
"**“Locke viết *Hai khảo luận* để biện hộ cho Cách mạng Vinh quang 1688.”** Thực ra, lời tựa viết sau năm 1688 tạo ấn tượng ấy, nhưng ngày nay giới nghiên cứu cho rằng sách được viết trong khủng hoảng Exclusion khoảng năm 1681, có thể để biện minh cho một cuộc nổi dậy đang được trù tính.",
],
"related": [
("cau-hoi/khe-uoc-xa-hoi.md", "Vì sao phải vâng lời nhà nước? Khế ước xã hội"),
("cau-hoi/tai-san-rieng.md", "Tài sản riêng có chính đáng không?"),
("cau-hoi/cai-toi.md", "Cái “tôi” là gì? Bạn của mười năm trước có còn là bạn?"),
("cau-hoi/ban-nga-thoi-gian.md", "Cái tôi qua thời gian — tôi của mười năm trước còn là tôi không?"),
("cau-hoi/ban-tinh-con-nguoi.md", "Bản tính con người thiện hay ác?"),
],
"sources": [
("Uzgalis, William, “John Locke”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/locke/"),
("Tuckness, Alex, “Locke’s Political Philosophy”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/locke-political/"),
("Gordon-Roth, Jessica, “Locke on Personal Identity”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/locke-personal-identity/"),
("Look, Brandon C., “Gottfried Wilhelm Leibniz”, *Stanford Encyclopedia of Philosophy* (mục 6.3, về ý niệm bẩm sinh).", "https://plato.stanford.edu/entries/leibniz/"),
("Locke, John, *An Essay Concerning Human Understanding* (1689), tập 1, Project Gutenberg.", "https://www.gutenberg.org/ebooks/10615"),
("Locke, John, *Second Treatise of Government* (1689), Project Gutenberg.", "https://www.gutenberg.org/ebooks/7370"),
],
},
"spinoza": {
"desc": "Bị cộng đồng khai trừ năm 1656, Spinoza dựng một hệ thống theo lối hình học: Thượng đế chính là Tự nhiên, và tự do là hiểu được tính tất yếu.",
"bio": [
"Một người chen ngang khiến bạn giận sôi lên. Spinoza sẽ hỏi: nếu bạn hiểu hết chuỗi nguyên nhân khiến người kia làm vậy, và khiến chính bạn nổi giận, cơn giận ấy còn giữ được sức mạnh như cũ không? Với ông, hiểu là bước đầu của tự do: càng thấy vì sao mọi sự phải như thế, ta càng bớt làm nô lệ cho cảm xúc.",
"Bento Spinoza (tiếng Hebrew là Baruch, tiếng Latin là Benedictus; cả ba đều nghĩa là “được ban phúc”) sinh năm 1632 ở Amsterdam, trong cộng đồng Do Thái gốc Bồ Đào Nha. Ông là học trò giỏi của trường Talmud Torah, nhưng năm mười bảy tuổi phải nghỉ học để phụ việc buôn bán của gia đình. Ngày 27 tháng 7 năm 1656, cộng đồng ra lệnh khai trừ (*herem*) ông, lệnh nặng nề nhất từng ban ra ở đó và không bao giờ được rút lại. Lý do chính xác không được ghi rõ, nhưng nhiều khả năng là những ý tưởng sau này nằm trong sách của ông: linh hồn không bất tử, Thượng đế không phải đấng quan phòng siêu việt, Lề luật không do Thượng đế trực tiếp ban.",
"Ông rời Amsterdam, sống giản dị ở Rijnsburg, Voorburg rồi The Hague. Cuốn sách duy nhất in tên ông khi còn sống là bản trình bày *Các nguyên lý triết học của Descartes* (1663). *Luận văn thần học–chính trị* (1670) in khuyết danh, đọc Kinh Thánh như một văn bản lịch sử và bênh vực tự do tư tưởng; một nhà phê bình gọi nó là cuốn sách “do quỷ dữ rèn ở địa ngục”. Tháng 11 năm 1676, Leibniz đến thăm và bàn về bản thảo *Đạo đức học*. Spinoza mất ở The Hague năm 1677; bạn bè in ngay *Đạo đức học* cùng các bản thảo khác.",
"*Đạo đức học* được trình bày “theo trật tự hình học”: định nghĩa, tiên đề, mệnh đề, chứng minh, như sách của Euclid. Nhưng mục đích của cả bộ máy chặt chẽ ấy là đạo đức: chỉ ra rằng hạnh phúc không nằm ở những của cải chóng tàn hay ở mê tín, mà ở đời sống của lý trí. SEP xếp ông vào số những triết gia thế kỷ 17 gần gũi nhất với hôm nay: tự do ý chí, quan hệ tâm–thân, khoan dung tôn giáo, dân chủ đều là những đề tài ông đã bàn.",
],
"works": [
("1663", "*Renati Des Cartes Principiorum Philosophiae Pars I et II*", "Các nguyên lý triết học của Descartes, trình bày theo lối hình học"),
("1670", "*Tractatus theologico-politicus*", "Luận văn thần học–chính trị, in khuyết danh"),
("1677", "*Ethica, ordine geometrico demonstrata*", "Đạo đức học, chứng minh theo trật tự hình học; in sau khi ông mất"),
("1677", "*Tractatus politicus*", "Luận văn chính trị, dở dang"),
],
"thoughts": [
"Chỉ có một **thực thể** (*substance*): Thượng đế, hay Tự nhiên (*Deus sive Natura*). Đá, cây, con người, ý nghĩ đều là những “cách thức” (*modes*) của thực thể ấy, không phải những thực thể độc lập.",
"Tâm và thân là một vật được diễn đạt theo hai cách: tư duy và quảng tính là hai thuộc tính của cùng một thực thể, nên không cần hỏi chúng “tương tác” ra sao — một lối ra khỏi bài toán Descartes để lại.",
"Tất định triệt để: “trong vũ trụ không có gì là ngẫu nhiên” (*Đạo đức học* I, mệnh đề 29). Ta gọi một việc là ngẫu nhiên chỉ vì hiểu biết của ta chưa đủ.",
"Tự do là hiểu: hiểu nguyên nhân của một cảm xúc làm giảm sức mạnh của nó đối với ta. “Người tự do ít nghĩ đến cái chết hơn mọi điều khác; sự khôn ngoan của người ấy là suy ngẫm về sự sống” (IV, mệnh đề 67).",
"Tự do tư tưởng: theo phụ đề của *Luận văn thần học–chính trị*, cho phép tự do triết học không hại gì đến lòng mộ đạo và hòa bình, còn đàn áp nó mới là mối nguy cho cả hai.",
],
"argument": {
"title": "Chỉ có một thực thể",
"intro": "Spinoza chứng minh điều này ở phần I *Đạo đức học* (mệnh đề 1–15); có thể rút gọn thành ba bước:",
"premises": [
"Hai thực thể không thể có chung một thuộc tính, tức một bản chất (mệnh đề 5).",
"Thượng đế, thực thể có vô hạn thuộc tính, tất yếu tồn tại (mệnh đề 11).",
"Thực thể nào cũng phải có ít nhất một thuộc tính, mà Thượng đế đã có mọi thuộc tính.",
],
"conclusion": "Vậy ngoài Thượng đế không thể có thực thể nào khác; mọi thứ khác đều ở “trong” Thượng đế (mệnh đề 14–15).",
"objection": "Leibniz nêu trực tiếp với Spinoza: hai thực thể có thể chung thuộc tính A mà vẫn khác nhau, vì thực thể này còn có thuộc tính B, thực thể kia có thuộc tính C. Nếu vậy, mệnh đề 5 không đứng vững, và cả chứng minh sụp theo. Ngày nay phần lớn triết gia coi lập luận này là thất bại.",
"reply": "Spinoza không trả lời trực tiếp. Một số nhà nghiên cứu hiện đại, như Michael Della Rocca, bênh ông dựa trên tính độc lập về khái niệm của các thuộc tính: vì mỗi thuộc tính phải được hiểu qua chính nó (mệnh đề 10), sự khác biệt ở B hay C không thể giải thích vì sao, xét dưới thuộc tính A, lại có hai thực thể chứ không phải một.",
},
"quote": {
"source": "Spinoza, *Đạo đức học* (1677), phần I, phụ lục — bản dịch tiếng Anh của R. H. M. Elwes (1883–1884)",
"orig": "Herefrom it follows, first, that men think themselves free inasmuch as they are conscious of their volitions and desires, and never even dream, in their ignorance, of the causes which have disposed them so to wish and desire.",
"vi": "Từ đó suy ra, trước hết, rằng con người tưởng mình tự do vì họ ý thức được những ý muốn và ham muốn của mình, còn trong sự thiếu hiểu biết, họ chẳng bao giờ mơ tới những nguyên nhân đã khiến họ muốn và ham muốn như thế.",
"url": "https://www.gutenberg.org/ebooks/3800",
},
"misread": [
"**“Spinoza là nhà phiếm thần, tôn thờ thiên nhiên.”** Thực ra, ông đồng nhất Thượng đế với Tự nhiên nhưng không coi Tự nhiên là đối tượng để sùng bái. Steven Nadler (SEP) cho rằng gọi ông là nhà phiếm thần theo nghĩa tôn giáo là sai: con đường đến với Thượng đế của Spinoza là triết học và khoa học, không phải lòng kính sợ. Người đương thời thì gọi ông là kẻ vô thần.",
"**“Vì mọi thứ đều tất định, Spinoza khuyên ta buông xuôi.”** Thực ra, *Đạo đức học* là một cuốn sách về sự giải phóng: ta không thể chọn khác đi, nhưng có thể hiểu, và càng hiểu càng ít bị ngoại cảnh điều khiển. Người tự do của ông bình thản trước được mất và chăm lo cho người khác.",
],
"related": [
("lich-su/can-dai.md", "Cận đại: lý trí lên ngôi"),
],
"sources": [
("Nadler, Steven, “Baruch Spinoza”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/spinoza/"),
("Waller, Jason, “Spinoza, Benedict de: Metaphysics”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/spinoz-m/"),
("Spinoza, Benedict de, *Ethics* (1677), bản dịch R. H. M. Elwes, Project Gutenberg.", "https://www.gutenberg.org/ebooks/3800"),
],
},
"leibniz": {
"desc": "Người phát minh phép tính vi tích phân độc lập với Newton, triết gia của nguyên lý lý do đầy đủ và các đơn tử, tin rằng đây là thế giới tốt nhất có thể có.",
"bio": [
"Ngắm bầu trời đêm, có bao giờ bạn tự hỏi: vì sao lại có một thế giới, chứ không phải chẳng có gì cả? Gottfried Wilhelm Leibniz phát biểu câu hỏi ấy rõ ràng vào năm 1714, như hệ quả của nguyên tắc ông đặt làm nền cho mọi suy luận: không có gì xảy ra mà không có **lý do đầy đủ** (*sufficient reason*) để nó như thế mà không khác đi.",
"Leibniz sinh ngày 1 tháng 7 năm 1646 ở Leipzig, khi cuộc Chiến tranh Ba mươi năm sắp kết thúc. Cha ông, giáo sư triết học đạo đức, mất khi ông lên sáu; cậu bé được tự do lục thư viện của cha. Lấy bằng tiến sĩ luật năm 1667, ông từ chối ghế giảng dạy để làm việc cho các triều đình. Bốn năm ở Paris (1672–1676) là bước ngoặt: ông học toán với Christiaan Huygens, được đọc bản thảo chưa in của Descartes và Pascal, chế tạo một máy tính cơ học làm được cả bốn phép tính, và bắt đầu hình thành phép tính vi phân.",
"Trên đường về Hanover nhận chức thủ thư cho công tước Brunswick, tháng 11 năm 1676 ông ghé Hà Lan gặp Spinoza, bàn về bản thảo *Đạo đức học* chưa in. Bốn mươi năm còn lại, ông sống chủ yếu ở Hanover, làm thủ thư, sử gia, cố vấn triều đình, và thư từ với hơn 1.100 người. Ông không để lại một kiệt tác hệ thống: ngoài *Biện thần luận* và *Những khảo luận mới*, tư tưởng của ông nằm rải rác trong bài báo, bản thảo và thư từ.",
"Cuối đời ông buồn bã: cuộc tranh cãi gay gắt với phe Newton về quyền phát minh vi tích phân, triều đình chê bộ tóc giả lỗi mốt, và khi công tước Georg Ludwig sang London làm vua George I, Leibniz bị bảo ở lại Hanover. Ông mất ngày 14 tháng 11 năm 1716. Giấc mơ thời trẻ về một “ngôn ngữ phổ quát” và một phép tính logic cho mọi lập luận theo ông suốt đời; năm 1900, Bertrand Russell viết hẳn một cuốn sách phê bình triết học của ông.",
],
"works": [
("1666", "*Dissertatio de arte combinatoria*", "Luận về nghệ thuật tổ hợp"),
("1686", "*Discours de métaphysique*", "Luận về siêu hình học"),
("1704", "*Nouveaux essais sur l'entendement humain*", "Những khảo luận mới về giác tính con người: đối thoại phản biện Locke, in năm 1765"),
("1710", "*Essais de Théodicée*", "Biện thần luận: về lòng tốt của Thượng đế, tự do của con người và nguồn gốc sự dữ"),
("1714", "*La Monadologie*", "Đơn tử luận, in lần đầu bằng bản dịch tiếng Đức năm 1720"),
],
"thoughts": [
"Mọi suy luận dựa trên hai nguyên lý: mâu thuẫn và lý do đầy đủ (*Đơn tử luận* §31–32). Nguyên lý thứ hai vẫn gây tranh cãi: trong khảo sát PhilPapers 2020 (câu bổ sung), số triết gia chấp nhận hoặc nghiêng về “sai” nhiều hơn số chọn “đúng”.",
"**Đơn tử** (*monads*): thực tại cuối cùng gồm những thực thể đơn giản, “không có cửa sổ” cho bất cứ gì ra vào (§7); mỗi đơn tử là “tấm gương sống” phản chiếu cả vũ trụ từ góc nhìn riêng (§56).",
"**Hòa hợp tiền định** (*pre-established harmony*): tâm và thân không tác động lên nhau mà được Thượng đế sắp đặt để luôn ăn khớp, như hai chiếc đồng hồ chạy đúng giờ — lời giải của Leibniz cho bài toán tương tác mà Descartes để lại.",
"Cái cối xay: phóng to một cỗ máy biết nghĩ để bước vào như vào cối xay, ta chỉ thấy các bộ phận đẩy nhau, không thấy gì giải thích được tri giác (§17). Hãy thử đặt lập luận này cạnh các tranh luận hôm nay về việc máy có ý thức hay không.",
],
"argument": {
"title": "Thế giới tốt nhất trong các thế giới khả hữu",
"intro": "Nếu Thượng đế toàn năng và hoàn toàn tốt lành, vì sao có đau khổ? Câu trả lời của Leibniz (*Biện thần luận*; *Đơn tử luận* §53–55), tái dựng ở dạng chuẩn:",
"premises": [
"Thượng đế toàn tri nên thấy hết mọi thế giới khả hữu và biết thế giới nào hoàn hảo nhất.",
"Theo nguyên lý lý do đầy đủ, việc Ngài tạo ra thế giới này chứ không phải thế giới khác phải có lý do; lý do ấy chỉ có thể nằm ở mức độ hoàn hảo của các thế giới.",
"Thượng đế hoàn toàn tốt lành và toàn năng nên chọn và tạo ra thế giới tốt nhất; chọn cái kém hơn đã là một khuyết điểm (“một điều tốt nhỏ hơn cũng là một kiểu sự dữ”).",
"Nếu không có thế giới nào tốt nhất, Thượng đế đã không tạo ra thế giới nào; mà thế giới thì đang tồn tại.",
],
"conclusion": "Vậy thế giới của chúng ta là thế giới tốt nhất trong các thế giới khả hữu, kể cả với những sự dữ có trong nó.",
"objection": "Trong *Candide* (1759), Voltaire cho thầy Pangloss khăng khăng rằng mọi sự đều tốt đẹp nhất trong “thế giới tốt nhất trong các thế giới khả hữu” này, ngay giữa đắm tàu và động đất ở Lisbon. Về lý lẽ: biết đâu luôn có một thế giới tốt hơn, như không có số tự nhiên lớn nhất; và nếu buộc phải chọn cái tốt nhất, Thượng đế còn tự do không?",
"reply": "Leibniz không nói thế giới không có sự dữ hay từng chi tiết của nó là tốt nhất; ông nói tổng thể không thể tốt hơn. Nhìn một góc nhỏ của bức tranh, ta chỉ thấy những vệt màu lộn xộn; nhà soạn nhạc cũng đan nốt nghịch tai vào hòa âm. Với phản bác thứ hai, ông viện chính sự tồn tại của thế giới; với phản bác thứ ba, ông cho rằng Thượng đế chọn cái tốt nhất do tất yếu đạo đức chứ không do tất yếu siêu hình, nên vẫn tự do.",
},
"quote": {
"source": "Leibniz, *Đơn tử luận* (viết năm 1714), §32 — bản dịch tiếng Anh của Robert Latta (1898)",
"orig": "And that of sufficient reason, in virtue of which we hold that there can be no fact real or existing, no statement true, unless there be a sufficient reason, why it should be so and not otherwise, although these reasons usually cannot be known by us.",
"vi": "Và [nguyên lý] lý do đầy đủ, nhờ nó ta cho rằng không thể có sự kiện nào là thật hay hiện hữu, không có mệnh đề nào đúng, nếu không có một lý do đầy đủ vì sao nó như thế mà không khác đi, dù phần lớn những lý do ấy ta không thể biết.",
"url": "https://archive.org/details/monadologyotherp00leib_2",
},
"misread": [
"**“Leibniz cho rằng thế giới này hoàn hảo, mọi chuyện đều tốt đẹp.”** Thực ra, ông thừa nhận đầy đủ sự dữ và đau khổ; điều ông khẳng định là không có thế giới khả hữu nào, xét toàn thể, tốt hơn. Thầy Pangloss của Voltaire là một bức biếm họa, không phải Leibniz.",
"**“Leibniz đánh cắp phép tính vi tích phân của Newton.”** Thực ra, đó là cáo buộc của phe Newton. Phần lớn sử gia toán học ngày nay cho rằng hai người phát triển độc lập: Newton nghĩ ra trước, Leibniz công bố trước.",
],
"related": [
("cau-hoi/vu-tru-khoi-dau.md", "Vũ trụ có khởi đầu không?"),
("lich-su/can-dai.md", "Cận đại: lý trí lên ngôi"),
("cau-hoi/van-de-tam-tri.md", "Thân xác và tâm trí: vấn đề lâu đời nhất của triết học"),
("cau-hoi/tri-thuc.md", "Biết một điều nghĩa là gì?"),
],
"sources": [
("Look, Brandon C., “Gottfried Wilhelm Leibniz”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/leibniz/"),
("Feeney, Thomas, “Leibniz on the Problem of Evil”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/leibniz-evil/"),
("Leibniz, *The Monadology and Other Philosophical Writings*, bản dịch Robert Latta, Oxford: Clarendon Press, 1898 — Internet Archive.", "https://archive.org/details/monadologyotherp00leib_2"),
("Leibniz, *Principes de la nature et de la grâce fondés en raison* (1714), §7, Wikisource tiếng Pháp.", "https://fr.wikisource.org/wiki/Principes_de_la_nature_et_de_la_gr%C3%A2ce_fond%C3%A9s_en_raison"),
("Voltaire, *Candide, ou l'optimisme* (1759), Project Gutenberg.", "https://www.gutenberg.org/ebooks/4650"),
],
},
"hume": {
"desc": "Nhà hoài nghi người Scotland: ta chưa từng thấy nhân quả, lý trí không biện minh được quy nạp, và đạo đức bắt nguồn từ tình cảm hơn là lý trí.",
"bio": [
"Sáng nào bạn cũng tin mặt trời sẽ mọc, và tin bánh mì sẽ làm no bụng như hôm qua. David Hume hỏi một câu nghe như đùa: lý trí cho ta quyền tin như thế ở chỗ nào? Ông sinh năm 1711 ở Edinburgh (Scotland), vào đại học năm mười một tuổi, rời trường năm mười lăm, rồi bỏ con đường luật mà gia đình mong muốn để dốc sức cho triết học — đến mức suy sụp tinh thần năm 1729. Năm 1734, ông sang La Flèche ở Pháp và, mới 23 tuổi, bắt đầu viết *Khảo luận về bản tính con người*.",
"Hai quyển đầu ra năm 1739, quyển ba năm 1740, đều không ký tên. Hume than rằng cuốn sách “chết yểu ngay khi rời nhà in” — một lời nói quá, nhưng sách quả không được đón nhận như ông mong, lại mang về cho ông tiếng vô thần và hoài nghi. Vì tiếng ấy, ông trượt ghế giáo sư ở Edinburgh (1745) rồi Glasgow (1751), và không bao giờ có chỗ trong đại học. Ông viết lại tư tưởng của mình cho dễ đọc hơn trong hai cuốn *Điều tra* (1748, 1751), làm thủ thư ở Edinburgh, và lúc sinh thời nổi tiếng chủ yếu nhờ các tiểu luận cùng bộ *Lịch sử nước Anh* sáu tập.",
"Từ năm 1763 ông sang Paris làm thư ký cho đại sứ Anh và được giới trí thức Pháp tôn vinh — điều ông khao khát cả đời. Năm 1766, ông giúp Rousseau sang Anh lánh nạn, rồi chứng kiến tình bạn ấy đổ vỡ vì Rousseau ngờ ông âm mưu hại mình. Biết mình mắc bệnh nan y năm 1775, Hume lo liệu để *Đối thoại về tôn giáo tự nhiên* — cuốn sách bạn bè khuyên ông đừng in khi còn sống — được xuất bản sau khi ông mất. Ông ra đi thanh thản năm 1776; cuốn sách ra mắt năm 1779.",
"Hume là triết gia của sự khiêm tốn trí tuệ. Ông cho thấy lý trí đơn thuần không chứng minh được nhân quả, quy nạp hay một cái tôi bền vững — vậy mà ta vẫn sống được, nhờ thói quen và bản tính. Kant thừa nhận chính Hume đã cắt ngang “giấc ngủ giáo điều” của mình; Bentham đọc Hume và thấy “như vảy rơi khỏi mắt”; Karl Popper chấp nhận phê phán quy nạp của Hume và dựng triết học khoa học của mình quanh việc bác bỏ giả thuyết.",
],
"works": [
("1739–1740", "*A Treatise of Human Nature*", "Khảo luận về bản tính con người"),
("1748", "*An Enquiry concerning Human Understanding*", "Điều tra về trí năng con người — viết lại quyển I của *Khảo luận* cho dễ đọc"),
("1751", "*An Enquiry concerning the Principles of Morals*", "Điều tra về các nguyên tắc đạo đức — cuốn ông tự coi là hay nhất của mình"),
("1754–1762", "*The History of England*", "Lịch sử nước Anh, sáu tập"),
("1779", "*Dialogues concerning Natural Religion*", "Đối thoại về tôn giáo tự nhiên — in sau khi ông mất"),
],
"thoughts": [
"**Mọi ý niệm bắt nguồn từ ấn tượng.** Những gì ta nghĩ đều là bản sao, nhạt hơn, của những gì ta từng cảm nhận. Nghi một từ triết học rỗng nghĩa? Hãy hỏi: ý niệm ấy đến từ ấn tượng nào?",
"**Nhân quả và thói quen.** Ta chỉ thấy A rồi B lặp đi lặp lại, chưa bao giờ thấy “sức mạnh” nối chúng; ý niệm về sự tất yếu nhân quả đến từ thói quen kỳ vọng của tâm trí.",
"**Cái tôi là một “bó” tri giác.** Nhìn vào bên trong, Hume chỉ bắt gặp nóng, lạnh, yêu, ghét… nối nhau, không bao giờ bắt gặp một “cái tôi” đứng sau chúng (*Khảo luận*, I.4.6).",
"**Lý trí là nô lệ của đam mê.** Lý trí cho biết sự thật và cách đạt mục tiêu, nhưng tự nó không đẩy ta hành động: “lý trí là, và chỉ nên là, nô lệ của đam mê” (*Khảo luận*, II.3.3). Đạo đức vì thế bắt nguồn từ tình cảm.",
"**Từ “là” đến “phải”.** Hume nhận xét nhiều tác giả đạo đức lặng lẽ chuyển từ câu “là” sang câu “phải” mà không giải thích (*Khảo luận*, III.1.1); cách hiểu phổ biến coi đây là nguyên tắc không suy ra được “phải” chỉ từ “là”, dù ý ông vẫn còn tranh cãi.",
],
"argument": {
"title": "Vấn đề quy nạp",
"intro": "Trong *Điều tra về trí năng con người* (mục IV), Hume hỏi: dựa vào đâu ta suy từ những gì đã thấy sang những gì chưa thấy — từ “bánh mì vẫn nuôi tôi” sang “miếng bánh mì này sẽ nuôi tôi”? Tái dựng ở dạng chuẩn:",
"premises": [
"Mọi suy luận thuộc một trong hai loại: **suy diễn** (*deductive*) dựa trên quan hệ giữa các ý niệm, như toán học; hoặc suy luận dựa trên kinh nghiệm về sự kiện.",
"Suy luận từ quá khứ sang tương lai không thể là suy diễn: nghĩ rằng tự nhiên đổi khác — tuyết rơi xuống mà mặn như muối, cây cối xanh tốt giữa mùa đông rồi tàn úa vào mùa hè — không hề mâu thuẫn.",
"Nó cũng không thể dựa trên kinh nghiệm mà không đi vòng tròn: mọi suy luận từ kinh nghiệm đều đã giả định sẵn rằng tương lai sẽ giống quá khứ — chính điều đang cần chứng minh.",
],
"conclusion": "Niềm tin **quy nạp** (*inductive*) không được lý trí biện minh; nó đến từ thói quen (*custom*) của tâm trí.",
"objection": "Một số triết gia hiện đại (Van Cleve 1984, Papineau 1992) cho rằng dùng quy nạp để biện minh cho quy nạp chỉ là “vòng tròn quy tắc” — dùng một quy tắc để kiểm tra chính nó — chứ không phải vòng tròn tiền đề, và điều đó không đáng ngại: miễn là quy tắc ấy thực sự đáng tin cậy, niềm tin rút ra từ nó vẫn được biện minh.",
"reply": "Người theo Hume đáp: lối biện minh ấy chứng minh quá nhiều. Một quy tắc phi lý như “phản quy nạp” — từ “phần lớn A đã thấy đều là B” suy ra “phần lớn A không phải là B” — cũng tự “biện minh” được theo đúng kiểu vòng tròn ấy (Salmon 1963), nên nó không thể thuyết phục người hoài nghi.",
},
"quote": {
"source": "Hume, *An Enquiry concerning Human Understanding* (1748), mục V, phần 1 — nguyên văn tiếng Anh, bản L. A. Selby-Bigge in lại ấn bản 1777",
"orig": "Custom, then, is the great guide of human life. It is that principle alone which renders our experience useful to us, and makes us expect, for the future, a similar train of events with those which have appeared in the past.",
"vi": "Vậy thì thói quen là người dẫn đường vĩ đại của đời người. Chỉ nhờ nguyên lý ấy mà kinh nghiệm mới có ích cho ta, và khiến ta trông đợi ở tương lai một chuỗi sự kiện giống như những gì đã xuất hiện trong quá khứ.",
"url": "https://www.gutenberg.org/ebooks/9662",
},
"misread": [
"**“Hume bảo đừng tin vào kinh nghiệm hay khoa học.”** Thực ra Hume cho rằng ta không thể sống mà không suy luận từ kinh nghiệm: “là người hành động, tôi hoàn toàn yên tâm; nhưng là triết gia…”, ông muốn biết lý trí biện minh cho nó ra sao. Chính ông khuyên “người khôn ngoan cân niềm tin của mình theo bằng chứng” (*Điều tra…*, mục X).",
"**“Theo Hume, đạo đức chỉ là cảm xúc riêng, ai thích gì thì tùy.”** Thực ra Hume nói phán đoán đạo đức bắt nguồn từ tình cảm, nhưng không tùy tiện: ta đồng cảm với những người chịu ảnh hưởng và phán xét từ một “quan điểm chung” mà ai cũng có thể đứng vào, vì vậy phán đoán đạo đức của con người khá thống nhất (*Khảo luận*, III.3.1).",
],
"related": [
("doc/hume-nhan-qua.md", "Đọc Hume về nhân quả (“Điều tra về trí năng con người”)"),
("cau-hoi/nhan-qua-ban-chat.md", "Nhân quả là gì?"),
("cong-cu/quy-nap.md", "Khi bằng chứng chỉ làm cho có lẽ đúng"),
("cau-hoi/sieu-dao-duc.md", "Đúng sai có khách quan không?"),
("cau-hoi/cai-toi.md", "Cái 'tôi' là gì? Bạn của mười năm trước có còn là bạn?"),
],
"sources": [
("Qu, Hsueh & Elizabeth S. Radcliffe, “David Hume”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/hume/"),
("Hume, David, *An Enquiry concerning Human Understanding* (1748), bản L. A. Selby-Bigge, Project Gutenberg.", "https://www.gutenberg.org/ebooks/9662"),
("Hume, David, *A Treatise of Human Nature* (1739–1740), Project Gutenberg.", "https://www.gutenberg.org/ebooks/4705"),
("Henderson, Leah, “The Problem of Induction”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/induction-problem/"),
("Cohon, Rachel, “Hume’s Moral Philosophy”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/hume-moral/"),
],
},
"rousseau": {
"desc": "Triết gia của tự do và bình đẳng: xã hội làm con người hư hỏng ra sao, và khi nào vâng theo luật vẫn là tự do — Khế ước xã hội, ý chí chung, Émile.",
"bio": [
"Bạn đăng một tấm ảnh rồi chốc chốc lại mở điện thoại xem thêm được bao nhiêu lượt thích? Gần ba thế kỷ trước, Jean-Jacques Rousseau đã gọi tên cơn khát ấy: *amour-propre*, lòng tự ái so bì — muốn được người khác coi trọng, và coi trọng hơn người khác. Ông sinh năm 1712 ở Genève, khi ấy là một nước cộng hòa độc lập; mẹ mất chín ngày sau khi ông chào đời, cha là thợ đồng hồ. Rời Genève năm mười sáu tuổi, ông lang bạt làm người hầu, thầy dạy nhạc, người chép nhạc, rồi lên Paris, kết thân với Diderot và viết bài cho bộ *Bách khoa toàn thư*.",
"Năm 1749, trên đường đi bộ tới Vincennes thăm Diderot đang bị giam, ông đọc được đề thi của Viện Hàn lâm Dijon: khoa học và nghệ thuật có làm phong hóa tốt lên không? Theo lời ông kể sau này, ngay lúc ấy ông bừng hiểu rằng con người vốn tốt, chỉ bị xã hội làm cho hư hỏng. Bài luận trả lời “không” đoạt giải nhất năm 1750 và làm ông nổi tiếng. *Luận về nguồn gốc của bất bình đẳng* (1755) đi xa hơn: từ khi có tư hữu và sự so bì, người ta phụ thuộc vào nhau và phải đóng kịch với nhau để được việc. Năm 1762, *Khế ước xã hội* và *Émile* ra đời — đỉnh cao sự nghiệp, nhưng cũng là tai họa: sách bị kết án ở Paris và Genève vì những quan điểm về tôn giáo, và ông phải bỏ trốn.",
"Đời ông đầy nghịch lý. Người viết cả một cuốn sách dày về cách nuôi dạy trẻ, theo chính lời ông kể, đã gửi cả năm đứa con với Thérèse Levasseur vào nhà nuôi trẻ bị bỏ rơi — điều Voltaire về sau đem ra công kích ông. Năm 1766, theo lời mời của David Hume, ông sang Anh lánh nạn; chẳng bao lâu Rousseau tin rằng chính Hume đang âm mưu hại mình, và tình bạn tan vỡ. Tự truyện *Tự thú* (*Les Confessions*) chỉ được in sau khi ông mất năm 1778. Năm 1794, những người cách mạng Pháp đưa hài cốt ông vào điện Panthéon.",
"Vì sao còn đọc Rousseau? Vì ông hỏi câu mà mọi nền chính trị hiện đại phải trả lời: làm sao sống chung dưới luật lệ mà vẫn tự do? Người ngưỡng mộ thấy ở ông nguồn cảm hứng cho dân chủ tham gia, người phê phán thấy mầm mống của chuyên chế nhân danh “nhân dân”. Và câu hỏi về sự so bì vẫn còn nguyên trong thời mạng xã hội: khi giá trị của ta nằm trong mắt người khác, ta còn tự do không?",
],
"works": [
("1751", "*Discours sur les sciences et les arts*", "Luận về khoa học và nghệ thuật — bài đoạt giải của Viện Hàn lâm Dijon"),
("1755", "*Discours sur l’origine et les fondements de l’inégalité parmi les hommes*", "Luận về nguồn gốc và nền tảng của sự bất bình đẳng giữa người với người"),
("1761", "*Julie, ou la Nouvelle Héloïse*", "Julie, hay nàng Héloïse mới — tiểu thuyết thư từ"),
("1762", "*Du contrat social*", "Khế ước xã hội — ý chí chung và nền tảng của quyền lực chính đáng"),
("1762", "*Émile, ou De l’éducation*", "Émile, hay Về giáo dục — nuôi dạy một con người tự chủ"),
],
"thoughts": [
"**Tốt bẩm sinh, hư vì xã hội.** Nhưng “tốt” không có nghĩa là có đức hạnh: con người trong trạng thái tự nhiên chỉ có lòng yêu mình (*amour de soi*), tức bản năng sống còn, và lòng thương (*pitié*) trước nỗi đau của kẻ khác, chưa biết thiện ác theo nghĩa đạo đức.",
"**Lòng tự ái so bì** (*amour-propre*). Sống thành cộng đồng, ta so mình với người khác và khao khát được nhìn nhận; trong xã hội bất bình đẳng, nhu cầu ấy thành ganh đua, giả dối và lệ thuộc. Nhiều nhà nghiên cứu ngày nay cho rằng giáo dục và thể chế phù hợp có thể uốn nó thành lòng tự trọng lành mạnh.",
"**Ý chí chung** (*general will*). Luật chính đáng là điều mọi công dân cùng muốn khi nghĩ với tư cách công dân, hướng tới lợi ích chung; nó phải đến từ mọi người và áp dụng cho mọi người (*Khế ước xã hội*, II.4).",
"**Giáo dục “tiêu cực”** (*Émile*). Thay vì nhồi kiến thức theo chương trình định sẵn, người thầy sắp đặt hoàn cảnh để đứa trẻ tự khám phá và tự rút ra kết luận. Câu hỏi để ngỏ: tự do ấy là thật, hay là sự dàn dựng khéo léo của người thầy?",
],
"argument": {
"title": "Làm sao vâng lời mà vẫn tự do?",
"intro": "*Khế ước xã hội* mở đầu bằng một nghịch lý: con người sinh ra tự do mà đâu đâu cũng mang xiềng — điều gì có thể làm cho tình trạng ấy chính đáng? Câu trả lời ở quyển I, theo cách tái dựng phổ biến:",
"premises": [
"Sức mạnh không tạo ra quyền: chịu khuất phục trước kẻ mạnh là chuyện bất đắc dĩ, không phải bổn phận (I.3).",
"Từ bỏ tự do của mình là từ bỏ tư cách làm người; một thỏa thuận lập ra quyền lực tuyệt đối ở một bên và sự phục tùng vô hạn ở bên kia là vô hiệu (I.4).",
"Vậy quyền lực chính đáng chỉ có thể dựa trên một thỏa ước giữ được tự do: mỗi người trao mình cho toàn thể theo cùng điều kiện như mọi người khác, nên không phải trao mình cho riêng ai (I.6).",
"Khi ấy luật là ý chí chung của chính các công dân, và “vâng theo luật do chính mình đặt ra là tự do” (I.8).",
],
"conclusion": "Nhà nước chỉ chính đáng khi người dân vâng theo những luật do chính họ, với tư cách công dân, cùng làm ra; trong một nhà nước như thế, vâng lời không làm mất tự do.",
"objection": "Ngay quyển I, Rousseau viết rằng ai không chịu theo ý chí chung sẽ bị toàn thể cộng đồng buộc phải theo — tức là “bị buộc phải tự do” (I.7). Những người phê phán, như Isaiah Berlin trong bài “Hai khái niệm tự do” (1958), cảnh báo rằng quan niệm tự do như “tự làm chủ” — mà lý thuyết của Rousseau là ví dụ rõ nhất — dễ bị kẻ cầm quyền biến thành lý lẽ đàn áp nhân danh chính tự do.",
"reply": "Người bênh vực Rousseau dựa vào chính văn bản: ý chí chung phải đến từ mọi người và áp dụng như nhau cho mọi người (II.4), nên nó không thể là ý muốn của một phe hay một nhà cầm quyền nhắm vào ai đó. Còn “buộc phải tự do”, Rousseau giải thích ngay trong câu ấy: luật chung bảo đảm cho mỗi công dân khỏi “mọi sự lệ thuộc cá nhân”. Hiểu như vậy, đó là tự do theo nghĩa cộng hòa: không phải được làm mọi điều mình muốn, mà là không phải sống dưới quyền tùy tiện của bất kỳ ai.",
},
"quote": {
"source": "Rousseau, *Du contrat social* (1762), quyển I, chương 1 — bản dịch tiếng Anh của G. D. H. Cole (1913)",
"orig": "Man is born free; and everywhere he is in chains. One thinks himself the master of others, and still remains a greater slave than they.",
"vi": "Con người sinh ra tự do, mà đâu đâu cũng mang xiềng xích. Kẻ tưởng mình là chủ của người khác thì vẫn là nô lệ hơn cả họ.",
"url": "https://www.gutenberg.org/ebooks/46333",
},
"misread": [
"**“Rousseau ca ngợi ‘người man rợ cao quý’ và muốn ta quay về sống trong rừng.”** Thực ra cụm *noble savage* có từ một vở kịch của John Dryden in năm 1672, và Rousseau không dùng nó (Ellingson 2001). Con người tự nhiên của ông không cao quý mà chưa có đạo đức; còn ý “quay về rừng sống giữa muông thú”, chính ông gọi là lối suy diễn của đối thủ (chú thích trong *Luận về bất bình đẳng*).",
"**“Ý chí chung là ý kiến của số đông.”** Thực ra Rousseau phân biệt ý chí chung, chỉ nhắm tới lợi ích chung, với “ý chí của mọi người”, chỉ là tổng các ý muốn riêng. Lá phiếu chỉ là cách để tìm ra ý chí chung, và có thể sai khi các phe nhóm lấn át (*Khế ước xã hội*, II.3).",
],
"related": [
("cau-hoi/khe-uoc-xa-hoi.md", "Vì sao phải vâng lời nhà nước? Khế ước xã hội"),
("cau-hoi/ban-tinh-con-nguoi.md", "Bản tính con người thiện hay ác?"),
("cau-hoi/tai-san-rieng.md", "Tài sản riêng có chính đáng không?"),
],
"sources": [
("Bertram, Christopher, “Jean Jacques Rousseau”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/rousseau/"),
("Delaney, James J., “Rousseau, Jean-Jacques”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/rousseau/"),
("Rousseau, Jean-Jacques, *The Social Contract & Discourses*, bản dịch tiếng Anh của G. D. H. Cole (1913), Project Gutenberg.", "https://www.gutenberg.org/ebooks/46333"),
("Carter, Ian & Ilkin Huseynli, “Positive and Negative Liberty”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/liberty-positive-negative/"),
("Ellingson, Ter, *The Myth of the Noble Savage*, Berkeley: University of California Press, 2001.", "https://music.washington.edu/research/publications/myth-noble-savage"),
],
},
"kant": {
"desc": "Triết gia Königsberg hỏi ta có thể biết gì, phải làm gì, được hy vọng gì: tâm trí cấu trúc kinh nghiệm, đạo đức là mệnh lệnh tuyệt đối của lý trí.",
"bio": [
"Tương truyền hàng xóm ở Königsberg chỉnh đồng hồ theo giờ Immanuel Kant ra khỏi nhà đi dạo — giai thoại do nhà thơ Heinrich Heine kể lại năm 1834, ba mươi năm sau khi Kant mất. Thật hay không, nó nói đúng một điều: đời sống bề ngoài của Kant rất đều đặn và phẳng lặng. Ông sinh năm 1724 ở Königsberg (nay là Kaliningrad, Nga), con một thợ làm yên cương, học ở một trường của phái Pietism, phong trào Tin Lành đề cao lòng sùng đạo cá nhân (ông ghét lối bắt học trò tự mổ xẻ tâm hồn ở đó), rồi vào đại học ngay tại thành phố. Ngoài mấy năm làm gia sư ở vùng lân cận, ông sống và dạy học cả đời ở đó.",
"Suốt mười lăm năm (1755–1770), Kant là giảng viên không lương, sống nhờ học phí sinh viên trả trực tiếp, mỗi tuần đứng lớp khoảng hai mươi giờ: lô-gích, siêu hình học, đạo đức, cả toán, vật lý và địa lý. Năm 1770, ở tuổi 46, ông mới được giữ ghế giáo sư lô-gích và siêu hình học. Rồi ông gần như im lặng suốt mười năm, để năm 1781 cho ra *Phê phán lý tính thuần túy*. Những tác phẩm lớn khác nối nhau ra đời trong mười năm sau đó. Cuốn sách về tôn giáo ông cho in năm 1793, sau khi một phần đã bị cơ quan kiểm duyệt bác, khiến ông bị vua Phổ khiển trách bằng một chỉ dụ đề ngày 1/10/1794.",
"Kant tự tóm mọi mối quan tâm của lý trí vào ba câu hỏi: Tôi có thể biết gì? Tôi phải làm gì? Tôi được phép hy vọng gì? Có hai người đã lay động ông. Hume, ông thú nhận, là người đầu tiên cắt ngang “giấc ngủ giáo điều” của ông. Rousseau thì dạy ông kính trọng con người: Kant ghi lại rằng có thời ông cho rằng chỉ tri thức mới làm nên phẩm giá, khinh đám đông chẳng biết gì, và “Rousseau đã chỉnh lại tôi”. Tương truyền chân dung Rousseau là bức tranh duy nhất treo trong nhà Kant.",
"Kant được coi là nhân vật trung tâm của triết học hiện đại: ông tổng hợp **duy lý luận** (*rationalism*) và **duy nghiệm luận** (*empiricism*), và đặt khung cho phần lớn triết học thế kỷ 19 và 20. Ông mất năm 1804, chỉ ít lâu trước sinh nhật thứ tám mươi.",
],
"works": [
("1781/1787", "*Kritik der reinen Vernunft*", "Phê phán lý tính thuần túy — giới hạn của tri thức"),
("1785", "*Grundlegung zur Metaphysik der Sitten*", "Nền tảng siêu hình học của đạo đức — mệnh lệnh tuyệt đối"),
("1788", "*Kritik der praktischen Vernunft*", "Phê phán lý tính thực hành — tự do và luật đạo đức"),
("1790", "*Kritik der Urteilskraft*", "Phê phán năng lực phán đoán — cái đẹp và mục đích trong tự nhiên"),
("1795", "*Zum ewigen Frieden*", "Hướng tới hòa bình vĩnh cửu — liên bang các quốc gia tự do"),
],
"thoughts": [
"**Bước ngoặt Copernicus.** Thay vì giả định tri thức phải khớp theo đối tượng, Kant thử giả định ngược lại: đối tượng phải khớp theo cách tâm trí ta nhận biết — như Copernicus thử cho người quan sát quay thay vì cho các vì sao quay (*Phê phán lý tính thuần túy*, lời tựa lần in thứ hai).",
"**Hiện tượng và vật tự thân.** Không gian, thời gian và các phạm trù như nhân quả là “khuôn” mà tâm trí áp lên mọi kinh nghiệm; nhờ thế ta biết chắc, một cách **tiên nghiệm** (*a priori*), rằng mọi kinh nghiệm đều theo chúng. Cái giá: ta chỉ biết thế giới như nó hiện ra với ta, không biết vật tự thân.",
"**Tự trị.** Luật đạo đức không đến từ Chúa, phong tục hay ham muốn, mà từ chính lý trí: lý trí tự đặt luật cho mình. Vì thế **mệnh lệnh tuyệt đối** (*categorical imperative*) ràng buộc mọi hữu thể có lý trí bất kể họ muốn gì — khác mệnh lệnh có điều kiện kiểu “muốn khỏe thì tập thể dục”.",
],
"argument": {
"title": "Phép thử phổ quát hóa và lời hứa dối",
"intro": "Trong *Nền tảng siêu hình học của đạo đức* (1785), Kant đề ra một phép thử cho mọi châm ngôn hành động và thử nó trên một tình huống ai cũng có thể gặp: cần tiền gấp.",
"premises": [
"Một hành động chỉ được phép nếu ta có thể đồng thời muốn châm ngôn của nó trở thành luật phổ quát cho mọi người (công thức luật phổ quát).",
"Châm ngôn “khi cần tiền, tôi sẽ vay và hứa trả, dù biết mình sẽ không trả” không thể phổ quát hóa: nếu ai cũng làm thế, chẳng ai còn tin lời hứa, và chính việc hứa để vay tiền trở nên vô nghĩa — châm ngôn ấy tự hủy.",
"Người hứa dối chỉ thành công nhờ lòng tin mà châm ngôn của chính anh ta, nếu thành luật chung, sẽ phá hủy; anh ta tự biến mình thành ngoại lệ.",
],
"conclusion": "Hứa dối là sai — kể cả khi, trong trường hợp cụ thể, nó có thể mang lại kết quả tốt.",
"objection": "Mill (*Thuyết vị lợi*, chương 1) cho rằng Kant không chỉ ra được mâu thuẫn logic nào: ông chỉ cho thấy hậu quả của việc ai cũng làm thế là điều không ai muốn — tức là ngầm dùng lập luận **hệ quả luận** (*consequentialism*). Benjamin Constant thì chỉ ra cái giá của việc cấm nói dối tuyệt đối: chẳng lẽ không được nói dối kẻ sát nhân đang hỏi bạn mình trốn ở đâu? Trong một bài viết năm 1797, Kant vẫn trả lời là không.",
"reply": "Người theo Kant đáp: mâu thuẫn không nằm ở hậu quả xấu, mà ở chỗ không thể muốn một cách nhất quán — kẻ hứa dối vừa cần, vừa phá đi chính tập quán tin lời hứa. Về kẻ sát nhân, Christine Korsgaard (1986) lập luận rằng nếu áp dụng đúng công thức phổ quát, lời nói dối với một kẻ đang che giấu ý định giết người là được phép; sự cứng nhắc của Kant bắt nguồn từ một lý tưởng đẹp về quan hệ giữa người với người, và đối phó với cái ác cần những nguyên tắc riêng.",
},
"quote": {
"source": "Kant, *Grundlegung zur Metaphysik der Sitten* (1785), mục II, Akademie-Ausgabe 4:429 — nguyên văn tiếng Đức",
"orig": "Handle so, daß du die Menschheit sowohl in deiner Person, als in der Person eines jeden andern jederzeit zugleich als Zweck, niemals bloß als Mittel brauchst.",
"vi": "Hãy hành động sao cho bạn luôn đối xử với nhân tính, nơi chính bạn cũng như nơi bất kỳ ai khác, đồng thời như một mục đích, không bao giờ chỉ như một phương tiện.",
"url": "https://www.korpora.org/Kant/aa04/429.html",
},
"misread": [
"**“Kant cấm dùng người khác làm phương tiện.”** Thực ra công thức nói “không bao giờ *chỉ* như phương tiện”. Đi xe ôm, ta dùng người tài xế làm phương tiện để tới nơi — điều đó không sai; sai là đối xử với họ như một món đồ, chẳng hạn quỵt tiền hay lừa họ vào điều họ không thể đồng ý.",
"**“Với Kant, hậu quả chẳng quan trọng gì.”** Thực ra Kant nói *giá trị đạo đức* của một hành động không nằm ở kết quả trông đợi, mà ở nguyên tắc của ý chí. Ông vẫn coi góp phần vào hạnh phúc của người khác là một bổn phận — bổn phận “không hoàn hảo”: phải giúp người, lúc này lúc khác, ở mức nào đó.",
],
"related": [
("cau-hoi/dao-duc-hanh-dong.md", "Hành động đúng là gì? Ba lý thuyết lớn của đạo đức học"),
("cau-hoi/noi-doi.md", "Có bao giờ được nói dối?"),
("doc/kant-khai-sang.md", "“Khai sáng là gì?” — Immanuel Kant (1784)"),
("cau-hoi/cai-dep.md", "Cái đẹp ở trong mắt người nhìn?"),
("cau-hoi/luan-chung-ton-giao.md", "Có thể chứng minh Chúa tồn tại bằng lý trí?"),
],
"sources": [
("Rohlf, Michael, “Immanuel Kant”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/kant/"),
("Johnson, Robert & Adam Cureton, “Kant’s Moral Philosophy”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/kant-moral/"),
("Kant, Immanuel, *Fundamental Principles of the Metaphysic of Morals* (*Grundlegung*, 1785), bản dịch tiếng Anh của T. K. Abbott, Project Gutenberg.", "https://www.gutenberg.org/ebooks/5682"),
("Kant, Immanuel, *Grundlegung zur Metaphysik der Sitten* (1785) và “Über ein vermeintes Recht aus Menschenliebe zu lügen” (1797), nguyên văn tiếng Đức theo Akademie-Ausgabe (tập 4 và 8), korpora.org.", "https://www.korpora.org/Kant/aa04/429.html"),
("Korsgaard, Christine M., “The Right to Lie: Kant on Dealing with Evil” (1986), in lại trong *Creating the Kingdom of Ends*, Cambridge University Press, 1996.", "https://doi.org/10.1017/CBO9781139174503.006"),
("Kant, Immanuel, *Der Streit der Fakultäten* (1798), Lời tựa — chỉ dụ của vua Friedrich Wilhelm II, ngày 1/10/1794, AA VII: 6.", "https://www.korpora.org/Kant/aa07/006.html"),
],
},
"bentham": {
"desc": "Nhà cải cách người Anh đặt nền cho thuyết vị lợi: đúng sai đo bằng hạnh phúc và đau khổ, của cả loài vật — “chúng có biết đau khổ không?”",
"bio": [
"Ở University College London hôm nay, bạn vẫn có thể gặp Jeremy Bentham: bộ xương của ông, mặc quần áo ông thường mặc, được trưng bày cho công chúng; chiếc đầu thật đã được thay bằng tượng sáp từ lâu. Đó là di nguyện của ông — ngay cả người chết cũng nên có ích cho người sống. Bentham sinh năm 1748 ở London, con một luật sư, vào Đại học Oxford năm mười hai tuổi và được đào tạo để theo nghề luật. Nhưng ngồi nghe William Blackstone giảng về luật Anh, ông chỉ thấy những lập luận sai và những lời biện hộ cho mọi thứ đang có.",
"Năm 1769, đúng năm được nhận vào giới luật sư, ông tìm thấy nguyên tắc vị lợi trong sách của Hume, Helvétius và Beccaria; đọc Hume, ông kể, ông thấy “như vảy rơi khỏi mắt”. Từ đó ông gần như không hành nghề nữa, để theo một việc lớn hơn: viết lại toàn bộ luật pháp dựa trên một thước đo duy nhất là hạnh phúc. *Đoạn bàn về chính quyền* (1776) tuyên bố rằng hạnh phúc lớn nhất cho số đông nhất là thước đo của đúng và sai; *Dẫn nhập vào các nguyên lý đạo đức và lập pháp* (in năm 1780, xuất bản năm 1789) dựng nền móng cho cả học thuyết.",
"Bentham là một nhà cải cách không biết mệt. Từ ý tưởng của người em trai, ông phát triển Panopticon (1791), nhà tù hình tròn nơi người gác ở tháp giữa thấy mọi phòng giam mà tù nhân không thấy người gác, vì tin rằng “càng bị giám sát chặt, ta càng cư xử tốt”; dự án bị bỏ dở, và năm 1812 nhà nước bồi thường cho ông 23.000 bảng Anh. Ông chế giễu học thuyết quyền tự nhiên là “vô nghĩa đi cà kheo”, nhưng lại đòi mở rộng quyền bầu cử, bỏ phiếu kín, và từ năm 1809 phản đối án tử hình trong mọi trường hợp. Ông mất ở London năm 1832, ngay trước khi Đạo luật Cải cách lớn của nước Anh được ký.",
"Bentham quan trọng vì ông biến một trực giác giản dị — đau khổ là xấu, hạnh phúc là tốt, và hạnh phúc của mỗi người đều đáng kể như nhau — thành công cụ để phê phán luật lệ. Câu hỏi của ông vẫn nằm sau mọi chính sách hôm nay: xây bệnh viện hay đường cao tốc, cấm hay cho phép một điều gì, thì ai được lợi, ai chịu khổ, nhiều đến đâu? Vì tính cả nỗi đau của loài vật, ông là điểm khởi đầu của tranh luận hiện đại về đạo đức với động vật, từ Peter Singer (1975) trở đi. Ông cũng là người thầy tinh thần của John Stuart Mill.",
],
"works": [
("1776", "*A Fragment on Government*", "Đoạn bàn về chính quyền — phê phán Blackstone"),
("1780/1789", "*An Introduction to the Principles of Morals and Legislation*", "Dẫn nhập vào các nguyên lý đạo đức và lập pháp — in năm 1780, xuất bản năm 1789"),
("1791", "*Panopticon; or, The Inspection House*", "Panopticon, hay Ngôi nhà giám sát"),
("1817", "*Plan of Parliamentary Reform*", "Kế hoạch cải cách nghị viện — mở rộng quyền bầu cử, bỏ phiếu kín"),
("1824", "*The Book of Fallacies*", "Sách về các ngụy biện — những lối lý sự dùng để chặn cải cách"),
],
"thoughts": [
"**Nguyên tắc vị lợi** (*principle of utility*). Một hành động, hay một đạo luật, đáng tán thành theo mức nó có xu hướng làm tăng hạnh phúc của những người liên quan, đáng phản đối theo mức nó làm giảm. Hạnh phúc, với Bentham, là khoái lạc và sự vắng mặt của đau khổ.",
"**“Phép tính hạnh phúc”.** Để so sánh các lựa chọn, hãy xét mỗi khoái lạc hay đau khổ về cường độ, độ dài, độ chắc chắn, độ gần hay xa, khả năng nó kéo theo cảm giác cùng loại hay trái loại, và số người chịu ảnh hưởng (*Dẫn nhập…*, chương IV). Bản thân cái tên “phép tính hạnh phúc” là do người đời sau đặt.",
"**Mỗi người tính là một.** Theo Mill, châm ngôn của Bentham là “mỗi người tính là một, không ai được tính hơn một”: trên bàn cân, niềm vui và nỗi đau của người ăn mày nặng ngang với của ông vua.",
"**Ngụy biện chính trị.** *Sách về các ngụy biện* (1824) vạch ra, bằng giọng giễu cợt, những lối lý sự mà những kẻ có quyền lợi riêng hay dùng để chặn các đề xuất cải cách.",
],
"argument": {
"title": "“Chúng có biết đau khổ không?”",
"intro": "Trong một chú thích ở chương XVII cuốn *Dẫn nhập…*, Bentham hỏi vì sao luật pháp bỏ mặc quyền lợi của loài vật, xếp chúng vào hàng đồ vật. Theo cách tái dựng phổ biến:",
"premises": [
"Điều làm cho một hành động đúng hay sai là nó làm tăng hay giảm hạnh phúc — khoái lạc và sự vắng mặt của đau khổ — của những ai chịu ảnh hưởng.",
"Vậy điều quyết định một sinh vật có được tính đến hay không là nó có thể cảm thấy khoái lạc và đau khổ hay không, chứ không phải nó biết suy luận hay biết nói. (Một con ngựa hay con chó trưởng thành còn biết suy luận và giao tiếp hơn đứa trẻ mới vài ngày tuổi — vậy mà ta vẫn tính đến đứa trẻ.)",
"Nhiều loài vật có thể đau khổ.",
],
"conclusion": "Nỗi đau của loài vật phải được tính đến trong đạo đức và luật pháp: câu hỏi không phải là chúng có biết suy luận không, có biết nói không, mà là chúng có biết đau khổ không.",
"objection": "Truyền thống theo Kant cho rằng tư cách đạo đức đầy đủ gắn với lý trí: chỉ hữu thể có lý trí mới là mục đích tự thân. Với loài vật, ta chỉ có bổn phận *gián tiếp* — theo các bài giảng đạo đức của Kant, kẻ tàn nhẫn với vật rồi cũng sẽ chai sạn với người. Nếu vậy, tiền đề 2 sai: biết đau thôi chưa đủ.",
"reply": "Người theo Bentham đáp bằng chính ví dụ của ông, về sau gọi là vấn đề “các trường hợp biên”: trẻ sơ sinh chưa biết suy luận, người hôn mê không còn biết suy luận, nhưng hành hạ họ là sai — sai *với chính họ*, chứ không chỉ vì làm hỏng tính người của kẻ ra tay. Nếu lý trí là ranh giới thì những người ấy rơi ra ngoài; không chấp nhận điều đó nghĩa là thừa nhận khả năng đau khổ mới là điều quyết định. (Một số người theo Kant, như Allen Wood, đáp lại bằng cách mở rộng phạm vi những ai “gắn với bản tính lý trí”.)",
},
"quote": {
"source": "Bentham, *An Introduction to the Principles of Morals and Legislation* (1789), chương I, đoạn 1 — nguyên văn tiếng Anh, bản Clarendon Press 1907 in lại ấn bản 1823",
"orig": "Nature has placed mankind under the governance of two sovereign masters, pain and pleasure. It is for them alone to point out what we ought to do, as well as to determine what we shall do.",
"vi": "Tự nhiên đã đặt loài người dưới quyền cai quản của hai ông chủ tối cao: đau khổ và khoái lạc. Chỉ chúng mới chỉ ra điều ta nên làm, cũng như quyết định điều ta sẽ làm.",
"url": "https://archive.org/details/introductiontoth033476mbp",
},
"misread": [
"**“Bentham tưởng có thể cân đo hạnh phúc chính xác như cân gạo trước mỗi quyết định.”** Thực ra chính ông viết rằng không nên trông đợi quy trình ấy được làm đầy đủ trước mỗi phán đoán đạo đức hay quyết định lập pháp; nó là một mô hình để luôn ghi nhớ (*Dẫn nhập…*, chương IV, đoạn VI).",
"**“Bentham đòi mọi người ăn chay vì động vật biết đau.”** Thực ra trong cùng chú thích ấy, ông cho rằng giết vật để ăn có thể chấp nhận được: chúng không phải chịu nỗi lo sợ dai dẳng về tương lai như con người, và cái chết dưới tay ta có thể nhanh hơn cái chết ngoài tự nhiên. Điều ông phản đối là hành hạ chúng; bước từ “chúng biết đau” đến “không nên ăn thịt chúng” là chuyện các triết gia đời sau, như Peter Singer, mới tranh luận.",
],
"related": [
("cau-hoi/dao-duc-ung-dung.md", "Ăn thịt có sai không? Đạo đức học ứng dụng"),
("cau-hoi/dao-duc-hanh-dong.md", "Hành động đúng là gì? Ba lý thuyết lớn của đạo đức học"),
("cau-hoi/hanh-phuc.md", "Hạnh phúc là gì?"),
("cau-hoi/noi-doi.md", "Có bao giờ được nói dối?"),
],
"sources": [
("Crimmins, James E., “Jeremy Bentham”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/bentham/"),
("Bentham, Jeremy, *An Introduction to the Principles of Morals and Legislation* (in năm 1780, xuất bản năm 1789), Oxford: Clarendon Press, 1907 (in lại ấn bản 1823), Internet Archive.", "https://archive.org/details/introductiontoth033476mbp"),
("Gruen, Lori & Susana Monsó, “The Moral Status of Animals”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/moral-animal/"),
("Mill, John Stuart, *Utilitarianism* (1863), chương V (châm ngôn “mỗi người tính là một”), Project Gutenberg.", "https://www.gutenberg.org/ebooks/11224"),
],
},
"hegel": {
"desc": "Triết gia của biện chứng và lịch sử: một ý tưởng chỉ hiểu được trong toàn bộ quá trình của nó, và tự do chỉ có giữa những người công nhận lẫn nhau.",
"bio": [
"Cuối năm 1806, khi quân của Napoléon chiếm thành phố đại học Jena, một triết gia 36 tuổi đang viết nốt bản thảo cuốn sách lớn đầu tiên của mình: *Hiện tượng học Tinh thần*, in năm 1807. Georg Wilhelm Friedrich Hegel sinh năm 1770 ở Stuttgart, học triết học rồi thần học ở Tübingen (1788–1793), nơi ông kết bạn với hai người sau này cũng thành danh: nhà thơ Hölderlin và triết gia Schelling.",
"Con đường của ông không thẳng. Ra trường, ông làm gia sư ở Bern rồi Frankfurt; ở Jena, ông bị coi là “người theo” Schelling dù lớn hơn bạn năm tuổi. Khi chiến tranh làm trường đại học tê liệt, ông làm biên tập báo ở Bamberg, rồi hiệu trưởng một trường trung học ở Nürnberg (1808–1815), nơi ông lập gia đình và viết *Khoa học Lô-gích*. Năm 1818 ông nhận ghế triết học ở Berlin, vị trí danh giá nhất của giới triết học Đức, và nổi tiếng lẫy lừng ở đó cho đến khi mất năm 1831.",
"*Hiện tượng học Tinh thần* dẫn người đọc qua từng “hình thái ý thức”: từ niềm tin ngây thơ vào giác quan, qua tự ý thức, đến đời sống xã hội, tôn giáo và triết học. Mỗi hình thái vấp phải mâu thuẫn bên trong và nhường chỗ cho một hình thái đầy đủ hơn. Phần nổi tiếng nhất là cuộc đấu tranh giành **sự công nhận** (*Anerkennung*) giữa chủ và tớ: ý thức về mình như một chủ thể tự do không thể hình thành trong cô độc.",
"Sau khi Hegel mất, học trò chia thành các phe tả, hữu và trung tâm; từ phe tả, Karl Marx tiếp thu nhiều ý tưởng của ông và đặt chúng trên nền duy vật. Kierkegaard chống lại tham vọng xây hệ thống, dù giới nghiên cứu ngày nay cho rằng đích nhắm chính của ông là những người theo Hegel ở Đan Mạch. Karl Popper buộc tội Hegel đã mở đường cho các xã hội khép kín, còn Sartre và Beauvoir mượn biện chứng chủ – tớ để bàn về quan hệ với người khác và về thân phận phụ nữ. Ít ai ngày nay tin trọn hệ thống Hegel, nhưng thói quen nhìn sự vật trong vận động, xung đột và lịch sử mang dấu ấn sâu đậm của ông.",
],
"works": [
("1807", "*Phänomenologie des Geistes*", "Hiện tượng học Tinh thần — hành trình của ý thức, có biện chứng chủ – tớ"),
("1812–1816", "*Wissenschaft der Logik*", "Khoa học Lô-gích — ba quyển: tồn tại, bản chất, khái niệm"),
("1817", "*Enzyklopädie der philosophischen Wissenschaften*", "Bách khoa thư các khoa học triết học — toàn bộ hệ thống, dạng giáo trình"),
("1821", "*Grundlinien der Philosophie des Rechts*", "Các nguyên lý của triết học pháp quyền — gia đình, xã hội dân sự, nhà nước"),
],
"thoughts": [
"**Biện chứng.** Một quan niệm, khi được nghĩ đến cùng, tự lộ ra mâu thuẫn bên trong và chuyển thành một quan niệm đầy đủ hơn, vừa phủ định vừa giữ lại cái cũ — Hegel gọi là *aufheben* (“vượt bỏ”). Mâu thuẫn không phải lỗi cần xóa, mà là động lực của tư duy.",
"**“Cái đúng là cái toàn thể.”** Một ý tưởng, một thể chế hay một thời đại chỉ được hiểu đúng khi đặt trong toàn bộ quá trình phát triển của nó; ngay cả cái Tuyệt đối, theo Hegel, “chỉ ở cuối cùng mới là cái nó thật sự là” (*Hiện tượng học Tinh thần*, Lời tựa).",
"**Tinh thần (*Geist*).** Ta không chỉ là những cá nhân rời rạc: ngôn ngữ, phong tục, luật pháp, nghệ thuật, tôn giáo là một “tinh thần” chung mà ta sống bên trong, như khi nói “tinh thần thời đại”. Hegel đọc lịch sử thế giới như “tiến trình của ý thức về tự do”, từ phương Đông qua Hy Lạp, La Mã đến các dân tộc German theo Kitô giáo — một sơ đồ mà người đọc hôm nay, nhất là ở châu Á, khó không thấy là lấy châu Âu làm trung tâm.",
"**Tự do cần thể chế.** Với Hegel, tự do không chỉ là làm điều mình muốn; nó thành hiện thực trong những thể chế nơi con người công nhận lẫn nhau — gia đình, xã hội dân sự, nhà nước (*Các nguyên lý của triết học pháp quyền*).",
],
"argument": {
"title": "Chủ và tớ, hay vì sao ta cần người khác để là chính mình",
"intro": "Chương IV của *Hiện tượng học Tinh thần* (1807) là phần nổi tiếng nhất của sách. Theo cách tái dựng phổ biến:",
"premises": [
"Muốn chắc mình là một chủ thể tự do, ta cần điều đó được xác nhận từ bên ngoài; đồ vật không làm được việc ấy, chỉ một ý thức khác mới làm được — “tự ý thức chỉ đạt được sự thỏa mãn trong một tự ý thức khác”.",
"Nếu sự công nhận bị giành bằng sức mạnh — kẻ thắng cuộc đấu sinh tử thành chủ, kẻ sợ chết thành tớ — thì đó chỉ là “sự công nhận một chiều và bất bình đẳng”: người chủ được công nhận bởi một người mà chính ông không coi là ngang hàng, nên lời công nhận ấy chẳng mấy giá trị.",
"Trong khi đó, người tớ, qua sợ hãi và lao động — “lao động là ham muốn bị kìm lại; nó tạo hình” — nhìn thấy chính mình trong thế giới do tay mình làm ra.",
],
"conclusion": "Tự do và ý thức trọn vẹn về mình chỉ có được trong sự công nhận lẫn nhau giữa những người ngang hàng — rốt cuộc là trong một trật tự quyền bảo đảm sự công nhận ấy cho mọi người.",
"objection": "Theo truyền thống từ Descartes, ý thức về chính mình là điều trực tiếp nhất: tôi biết mình đang nghĩ mà chẳng cần ai xác nhận. Hơn nữa, câu chuyện chủ – tớ giống một ẩn dụ lịch sử hơn là một chứng minh: vì sao hai ý thức gặp nhau thì nhất thiết phải đấu tranh sinh tử?",
"reply": "Nhiều người đọc Hegel ngày nay hiểu “công nhận” không phải là được khen, mà là điều kiện của một *tư cách*: là người có quyền, có trách nhiệm, có tiếng nói đáng nghe. Biết mình đang nghĩ thì có thể không cần ai, nhưng tư cách ấy chỉ tồn tại khi người khác và các thể chế cùng thừa nhận nó — điều mà cuộc đấu sinh tử, dù kết thúc thế nào, không mang lại được. Axel Honneth (*Đấu tranh vì sự công nhận*) dùng ý tưởng này để giải thích những xung đột xã hội của các nhóm người bị coi thường đòi được công nhận.",
},
"quote": {
"source": "Hegel, *Grundlinien der Philosophie des Rechts* (1821), Lời tựa (đề ngày 25/6/1820) — bản dịch tiếng Anh của S. W. Dyde (1896)",
"orig": "When philosophy paints its grey in grey, one form of life has become old, and by means of grey it cannot be rejuvenated, but only known. The owl of Minerva takes its flight only when the shades of night are gathering.",
"vi": "Khi triết học tô màu xám lên nền xám, thì một hình thái của đời sống đã già cỗi; bằng màu xám, triết học không làm nó trẻ lại được, mà chỉ hiểu được nó. Con cú của thần Minerva chỉ cất cánh khi bóng đêm buông xuống.",
"url": "https://archive.org/details/cu31924014578979",
},
"misread": [
"**“Biện chứng Hegel là công thức chính đề – phản đề – hợp đề.”** Thực ra Hegel không dùng bộ ba thuật ngữ này để mô tả triết học của mình; nó gắn với Fichte, và Hegel còn chê lối áp “bộ ba” một cách máy móc là biến nó thành “lược đồ không hồn” (*Hiện tượng học Tinh thần*, Lời tựa). Gustav Mueller (1958) gọi đây là một “truyền thuyết” về Hegel.",
"**“‘Cái gì hợp lý thì hiện thực’ nghĩa là mọi thứ đang tồn tại đều đúng.”** Thực ra Hegel phân biệt “hiện thực” (*Wirklichkeit*) với sự tồn tại đơn thuần: điều ngẫu nhiên, sai lầm, xấu xa cũng tồn tại, nhưng không đáng gọi là hiện thực theo nghĩa của ông. Chính ông viết: ai mà chẳng đủ tinh để thấy quanh mình nhiều điều không như lẽ ra phải thế (*Bách khoa thư*, §6).",
],
"related": [
("lich-su/the-ky-19.md", "Thế kỷ 19: hệ thống vỡ vụn"),
],
"sources": [
("Redding, Paul, “Georg Wilhelm Friedrich Hegel”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/hegel/"),
("Maybee, Julie E., “Hegel’s Dialectics”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/hegel-dialectics/"),
("Iser, Mattias, “Recognition”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/recognition/"),
("Hegel, G. W. F., *Phänomenologie des Geistes* (1807), nguyên văn tiếng Đức, Project Gutenberg.", "https://www.gutenberg.org/ebooks/6698"),
("Hegel, G. W. F., *Hegel’s Philosophy of Right*, bản dịch tiếng Anh của S. W. Dyde, London: George Bell & Sons, 1896, Internet Archive.", "https://archive.org/details/cu31924014578979"),
("Hegel, G. W. F., *The Logic of Hegel* (phần Lô-gích của *Bách khoa thư*), bản dịch tiếng Anh của William Wallace, Project Gutenberg.", "https://www.gutenberg.org/ebooks/55108"),
],
},
"mill": {
"desc": "Triết gia nói tiếng Anh có ảnh hưởng nhất thế kỷ 19: hạnh phúc có phẩm chất, nguyên tắc gây hại, tự do ngôn luận và bình đẳng nam nữ.",
"bio": [
"Ba tuổi học tiếng Hy Lạp, tám tuổi học tiếng La-tinh, mười hai tuổi đã đọc gần hết các tác phẩm kinh điển: tuổi thơ của John Stuart Mill là một cuộc thí nghiệm giáo dục. Ông sinh năm 1806 ở London. Cha ông, James Mill, là bạn thân và đồng minh của Jeremy Bentham, tự tay dạy con để đào tạo một thủ lĩnh cho thế hệ cấp tiến kế tiếp. Mill không học đại học; ông đọc Bentham, biên tập một cuốn sách của Bentham, và sớm thành một cây bút trẻ tuyên truyền cho **thuyết vị lợi** (*utilitarianism*).",
"Năm 20 tuổi, ông rơi vào khủng hoảng. Ông tự hỏi: giả sử mọi cải cách mình theo đuổi thành hiện thực ngay lúc này, mình có hạnh phúc không? Một tiếng nói trong ông đáp: “Không!”. Mill tìm lại mình nhờ thơ Wordsworth, và từ đó tin rằng nuôi dưỡng cảm xúc quan trọng không kém cải cách xã hội. Năm 1830 ông gặp Harriet Taylor; họ là đôi bạn tri kỷ gần hai mươi năm và cưới nhau năm 1851, hai năm sau khi chồng bà mất. Mill coi bà gần như đồng tác giả của nhiều tác phẩm; bà mất năm 1858, và *Bàn về tự do* (1859) được đề tặng bà.",
"Mill làm việc gần 35 năm cho Công ty Đông Ấn, soạn công văn cho bộ máy cai trị Ấn Độ; ngay trong *Bàn về tự do*, ông viết rằng nguyên tắc tự do chưa áp dụng cho những xã hội ông coi là “lạc hậu” — giới hạn mà người đọc ở những nước từng là thuộc địa khó bỏ qua. Mặt khác, khi là nghị sĩ (1865–1868), ông trình lên Hạ viện Anh bản kiến nghị đại chúng đầu tiên đòi quyền bầu cử cho phụ nữ (1866), và năm 1867 đề nghị sửa luật bầu cử, thay chữ “đàn ông” bằng “người” (thua với 73 phiếu thuận, 196 phiếu chống). Ông mất năm 1873 ở Avignon (Pháp) và được chôn cạnh vợ.",
"Vì sao Mill vẫn quan trọng? Ông cố giữ cùng lúc hai điều tưởng khó đi chung: một đạo đức lấy hạnh phúc chung làm thước đo, và một vùng tự do cá nhân mà cả nhà nước lẫn đám đông không được xâm phạm. Mỗi khi ta tranh cãi nên cấm hay để yên một phát ngôn trên mạng, một việc chỉ hại cho chính người làm, hay một điều luật “vì lợi ích của chính bạn”, ta đang đứng trên sân mà Mill đã vạch ra.",
],
"works": [
("1843", "*A System of Logic*", "Hệ thống lô-gích — quy nạp và phương pháp khoa học"),
("1859", "*On Liberty*", "Bàn về tự do — nguyên tắc gây hại, tự do ngôn luận, quyền được sống khác người"),
("1861/1863", "*Utilitarianism*", "Thuyết vị lợi — đăng báo năm 1861, in thành sách năm 1863"),
("1869", "*The Subjection of Women*", "Sự lệ thuộc của phụ nữ — chống lại sự lệ thuộc pháp lý của giới này vào giới kia"),
],
"thoughts": [
"**Hạnh phúc có phẩm chất.** Hành động đúng theo mức nó có xu hướng làm tăng hạnh phúc, sai theo mức nó gây ra điều ngược lại. Nhưng khác Bentham, Mill cho rằng khoái lạc khác nhau cả về phẩm chất: “thà làm con người bất mãn còn hơn làm con lợn mãn nguyện; thà làm Socrates bất mãn còn hơn làm kẻ ngốc mãn nguyện”.",
"**Nguyên tắc gây hại** (*harm principle*). Lý do duy nhất để quyền lực can thiệp vào một người trái ý họ là ngăn họ gây hại cho người khác; “vì lợi ích của chính anh” chỉ đủ để khuyên nhủ, không đủ để cưỡng ép.",
"**Chuyên chế của đa số.** Mối nguy cho tự do không chỉ đến từ nhà nước mà còn từ áp lực của dư luận và phong tục — thứ “thâm nhập sâu hơn nhiều vào chi tiết đời sống” và muốn đúc mọi tính cách theo một khuôn.",
"**Bình đẳng nam nữ.** Không ai biết “bản tính” phụ nữ thật sự ra sao khi họ chưa bao giờ được tự do phát triển như nam giới; những khác biệt ta thấy phần lớn là sản phẩm của cách nuôi dạy (*Sự lệ thuộc của phụ nữ*).",
],
"argument": {
"title": "Vì sao không được bịt miệng ngay cả một ý kiến sai",
"intro": "Chương II của *Bàn về tự do* (1859) bảo vệ tự do tư tưởng và thảo luận. Theo cách tái dựng phổ biến:",
"premises": [
"Muốn cấm một ý kiến vì “chắc chắn nó sai”, người cấm phải coi sự chắc chắn của mình là chắc chắn tuyệt đối — tức là tự cho mình không thể sai.",
"Không người nào, không thời đại nào không thể sai: nhiều điều từng được cả xã hội tin chắc, về sau bị coi là sai, thậm chí phi lý.",
"Ngay cả khi ý kiến bị cấm là sai, việc phải đối mặt với nó giúp ta hiểu vì sao chân lý là chân lý; không bị thách thức, chân lý thành định kiến rồi thành giáo điều chết. Và ý kiến sai thường vẫn chứa một phần sự thật.",
],
"conclusion": "Bịt miệng một ý kiến, dù đúng hay sai, là “cướp đi của cả nhân loại”; cả chính quyền lẫn đa số đều không có quyền làm vậy.",
"objection": "Mill tự nêu phản bác mạnh nhất: chính phủ và cá nhân luôn phải hành động theo niềm tin tốt nhất của mình dù có thể sai — đánh thuế, tuyên chiến. Cấm truyền bá điều mình tin là sai và nguy hại cũng chỉ là hành động theo niềm tin như thế, đâu phải tự cho mình không thể sai.",
"reply": "Mill đáp: hai việc khác nhau rất xa. Ta được phép coi một ý kiến là đúng để hành động *vì* nó đã đứng vững trước mọi cơ hội phản bác; còn cấm phản bác nó là tước đi chính điều kiện cho phép ta tin nó một cách có lý. Tự do phản bác là cái giá của sự tự tin hợp lý.",
},
"quote": {
"source": "Mill, *On Liberty* (1859), chương I — nguyên văn tiếng Anh",
"orig": "That principle is, that the sole end for which mankind are warranted, individually or collectively, in interfering with the liberty of action of any of their number, is self-protection. That the only purpose for which power can be rightfully exercised over any member of a civilised community, against his will, is to prevent harm to others.",
"vi": "Nguyên tắc ấy là: mục đích duy nhất cho phép loài người, từng cá nhân hay tập thể, can thiệp vào tự do hành động của bất kỳ ai trong số họ, là tự vệ. Rằng mục đích duy nhất để quyền lực được thực thi chính đáng đối với bất kỳ thành viên nào của một cộng đồng văn minh, trái với ý muốn của người đó, là ngăn người đó gây hại cho người khác.",
"url": "https://www.gutenberg.org/ebooks/34901",
},
"misread": [
"**“Theo Mill, ai muốn nói gì cũng được, ở đâu cũng được.”** Thực ra Mill viết rằng ý kiến mất quyền được miễn trừ khi được nói ra trong hoàn cảnh biến nó thành lời kích động trực tiếp: viết trên báo rằng lái buôn ngũ cốc làm dân chết đói thì được, nhưng hô điều đó trước đám đông đang giận dữ tụ tập trước nhà một lái buôn thì có thể bị trừng phạt (*Bàn về tự do*, chương III).",
"**“Thuyết vị lợi của Mill là chủ nghĩa hưởng lạc: sướng càng nhiều càng tốt.”** Thực ra Mill phân biệt khoái lạc cao và thấp, và thước đo của ông là hạnh phúc của *mọi người* liên quan, mỗi người được tính ngang nhau — không phải khoái lạc của riêng người hành động.",
],
"related": [
("doc/mill-tu-do.md", "Tự do ngôn luận — John Stuart Mill, “Bàn về tự do” chương 2 (1859)"),
("cau-hoi/tu-do-ngon-luan.md", "Tự do ngôn luận: được nói đến đâu?"),
("cau-hoi/dao-duc-hanh-dong.md", "Hành động đúng là gì? Ba lý thuyết lớn của đạo đức học"),
("cau-hoi/nu-quyen.md", "Triết học nữ quyền là gì?"),
("cau-hoi/noi-doi.md", "Có bao giờ được nói dối?"),
],
"sources": [
("Macleod, Christopher, “John Stuart Mill”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/mill/"),
("Schefczyk, Michael, “John Stuart Mill: Ethics”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/mill-eth/"),
("Mill, John Stuart, *On Liberty* (1859), Project Gutenberg.", "https://www.gutenberg.org/ebooks/34901"),
("Mill, John Stuart, *Utilitarianism* (1863), Project Gutenberg.", "https://www.gutenberg.org/ebooks/11224"),
("Mill, John Stuart, *The Subjection of Women* (1869), Project Gutenberg.", "https://www.gutenberg.org/ebooks/27083"),
("UK Parliament, “Presenting the 1866 petition” (Living Heritage).", "https://www.parliament.uk/about/living-heritage/transformingsociety/electionsvoting/womenvote/parliamentary-collections/1866-suffrage-petition/presenting-the-petition/"),
],
},
"kierkegaard": {
"desc": "Triết gia Đan Mạch viết bằng nhiều bút danh: cá nhân trước hệ thống, ba lĩnh vực tồn tại, lo âu là “chóng mặt của tự do”, đức tin như một sự dấn thân.",
"bio": [
"Copenhagen, năm 1841. Một chàng trai 28 tuổi trả lại chiếc nhẫn đính hôn cho vị hôn thê Regine Olsen, chịu tiếng là kẻ bạc tình, rồi bỏ sang Berlin. Trong vài năm sau đó, anh cho ra đời một loạt sách ký bằng những cái tên lạ: Victor Eremita, Johannes de Silentio, Vigilius Haufniensis. Đó là Søren Kierkegaard, sinh ngày 5/5/1813, con út trong bảy người con của một thương gia giàu có, sùng đạo và u uất. Ông học thần học và triết học ở Copenhagen, viết luận văn về sự mỉa mai của Socrates (1841) — hình mẫu suốt đời của ông — và không bao giờ lấy vợ.",
"Vì sao lại dùng bút danh? Kierkegaard tin rằng chân lý về cách sống không thể trao tay như một công thức: người đọc phải tự vật lộn với nó. Các bút danh giống những nhân vật trong một cuốn tiểu thuyết lớn — chàng thẩm mỹ chán đời, vị thẩm phán mẫu mực, Johannes “Im lặng” ngưỡng mộ Abraham mà không hiểu nổi ông. Đối thủ của ông là thói giải thích mọi thứ bằng một hệ thống mà quên mất con người cụ thể đang sống. Ông hay được coi là kẻ thù số một của Hegel, nhưng giới nghiên cứu gần đây cho rằng mục tiêu chính là các môn đồ Hegel ở Đan Mạch, và nhiều ý tưởng của ông phát triển từ chính Hegel.",
"Những năm 1845–1846, tờ báo trào phúng *Corsair* đem ông ra giễu cợt, chế nhạo cả ngoại hình; người vốn thích dạo phố trò chuyện với mọi người trở nên khép kín. Từ đó ông viết về “công chúng” như một bóng ma vô danh do báo chí tạo ra, nhân danh nó mà người ta san phẳng mọi cá nhân — những trang nhiều người đọc lại khi nghĩ về đám đông trên mạng xã hội. Những năm cuối đời, ông công kích Giáo hội nhà nước Đan Mạch vì đã biến Kitô giáo thành tập tục. Ông ngã quỵ giữa phố và mất ngày 11/11/1855, khi mới 42 tuổi.",
"Kierkegaard thường được gọi là “cha đẻ của chủ nghĩa hiện sinh”, dù nhãn ấy che khuất một điều: ông là một nhà tư tưởng Kitô giáo. Ông ảnh hưởng tới Heidegger, Sartre, Beauvoir, và cả Wittgenstein, người gọi ông là nhà tư tưởng sâu sắc nhất thế kỷ 19; sách của ông còn được dịch sang tiếng Nhật trước cả tiếng Anh. Câu hỏi của ông vẫn nguyên đó: biết rất nhiều về cuộc đời có giúp ta biết mình phải sống thế nào không?",
],
"works": [
("1843", "*Enten–Eller*", "*Hoặc/hoặc*: đời sống thẩm mỹ đối diện đời sống đạo đức"),
("1843", "*Frygt og Bæven*", "*Kính sợ và run rẩy*, bút danh Johannes de Silentio: Abraham và đức tin"),
("1844", "*Begrebet Angest*", "*Khái niệm lo âu*, bút danh Vigilius Haufniensis"),
("1846", "*Afsluttende uvidenskabelig Efterskrift*", "*Tái bút phi khoa học kết thúc*, bút danh Johannes Climacus"),
("1847", "*Kjerlighedens Gjerninger*", "*Những việc làm của tình yêu*, ký tên thật"),
("1849", "*Sygdommen til Døden*", "*Căn bệnh đến cái chết*, bút danh Anti-Climacus: tuyệt vọng và cái tôi"),
],
"thoughts": [
"**Cá nhân trước hệ thống.** Một hệ thống có thể giải thích cả lịch sử thế giới mà vẫn không trả lời câu hỏi của một người cụ thể: *mình* nên sống thế nào? Suy xét thôi chưa đủ, vì suy xét có thể kéo dài vô tận; đến một lúc phải có quyết định, và không ai quyết định thay ai.",
"**Ba lĩnh vực tồn tại.** Thẩm mỹ (sống theo hứng thú, sợ nhất là chán), đạo đức (tự ràng buộc vào cam kết như hôn nhân, nghề nghiệp), tôn giáo (đứng trước Thượng đế). Đây không phải ba nấc thang tự động leo lên mà là những lối sống cạnh tranh nhau; chuyển từ lối này sang lối khác đòi hỏi cả con người phải đổi khác.",
"**Lo âu là chóng mặt của tự do.** Trong *Khái niệm lo âu*, lo âu là cảm giác khi ta nhìn xuống những khả năng của chính mình: vừa bị hút về, vừa muốn lùi lại. Việc cần làm không phải xóa bỏ lo âu mà là học cách lo âu cho đúng.",
],
"argument": {
"title": "Abraham — đức tin có đứng trên đạo đức không?",
"intro": "Trong *Kính sợ và run rẩy*, qua bút danh Johannes de Silentio, Kierkegaard biến chuyện Abraham được lệnh hiến tế con trai Isaac (Sáng thế ký 22) thành một thế lưỡng nan, theo cách tái dựng phổ biến:",
"premises": [
"Nếu đạo đức — những đòi hỏi phổ quát, giải thích được bằng lý lẽ chung cho mọi người — là tầng cao nhất của đời sống, thì không gì biện minh được việc giết một đứa con vô tội.",
"Abraham sẵn sàng làm điều đó vì một quan hệ riêng với Thượng đế mà ông không thể giải thích cho ai — khác với người anh hùng bi kịch như Agamemnon, người còn viện dẫn được lợi ích của cả đoàn quân.",
"Thế nhưng truyền thống lại tôn vinh Abraham là “cha của đức tin”.",
],
"conclusion": "Vậy hoặc có một “sự đình chỉ có mục đích của đạo đức” — quan hệ của cá nhân với Thượng đế đứng cao hơn cái phổ quát — hoặc Abraham chỉ là kẻ suýt giết con, và mọi lời ca ngợi ông đều sai.",
"objection": "Từ năm 1798, Kant đã viết rằng trước một giọng nói tự xưng là của Thượng đế, Abraham lẽ ra phải đáp: việc ta không được giết đứa con ngoan của mình là hoàn toàn chắc chắn, còn việc ngươi là Thượng đế thì ta không chắc và không bao giờ chắc được. Nếu đức tin đứng trên đạo đức, lấy gì phân biệt Abraham với kẻ cuồng tín nghe “tiếng gọi” rồi làm hại người khác?",
"reply": "Chính Johannes tự nhận mình đứng ngoài đức tin và không hiểu nổi Abraham, nên cuốn sách không phải lời khuyên làm theo. Giới nghiên cứu cũng cảnh báo cách đọc coi thông điệp chính là sự vâng lời: điều Johannes kinh ngạc là niềm tin của Abraham rằng mình sẽ nhận lại Isaac ngay trong đời này, cùng nỗi sợ hãi và run rẩy đi kèm — trái ngược sự chắc chắn thanh thản của kẻ cuồng tín.",
},
"quote": {
"source": "Kierkegaard (bút danh Johannes de Silentio), *Fear and Trembling* (1843), phần “Preliminary Expectoration”, đoạn tả “hiệp sĩ đức tin” — bản dịch tiếng Anh của L. M. Hollander (1923)",
"orig": "He attends to his business, and when one sees him one might think he was a clerk who had lost his soul in doing double bookkeeping, he is so exact.",
"vi": "Ông lo việc làm ăn của mình, và ai thấy ông cũng có thể tưởng đó là một anh thư ký đã đánh mất linh hồn vào sổ sách kế toán kép, vì ông chỉn chu đến thế.",
"url": "https://www.gutenberg.org/ebooks/60333",
},
"misread": [
"**“Kierkegaard nói chân lý là chủ quan, ai tin gì thì cái đó đúng với người ấy.”** Thực ra câu “chân lý là tính chủ thể” là của bút danh Johannes Climacus, và nó nói về *cách* một người nắm giữ những niềm tin quyết định đời mình, chứ không nói rằng tin gì cũng đúng. Điều Kierkegaard chống là thói biết rất nhiều mà không sống theo điều mình biết.",
"**“Đức tin theo Kierkegaard là thứ cuồng nhiệt, khác người.”** Thực ra “hiệp sĩ đức tin” mà Johannes tưởng tượng trông y như một ông thư ký chỉn chu, đi lễ ngày Chủ nhật, háo hức với bữa tối ở nhà (xem trích đoạn trên): đức tin, nếu có, không lộ ra bằng dấu hiệu bên ngoài nào.",
],
"related": [
("cau-hoi/duc-tin-ly-tri.md", "Có nên tin mà không cần bằng chứng?"),
("lich-su/the-ky-19.md", "Thế kỷ 19: hệ thống vỡ vụn"),
],
"sources": [
("Lippitt, John & C. Stephen Evans, “Søren Kierkegaard”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/kierkegaard/"),
("McDonald, William, “Søren Kierkegaard”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/kierkega/"),
("Kierkegaard, Søren, *Selections from the Writings of Kierkegaard*, L. M. Hollander dịch (1923), Project Gutenberg.", "https://www.gutenberg.org/ebooks/60333"),
("Kant, Immanuel, *Der Streit der Fakultäten* (1798), Ak 7:63 (chú thích về Abraham).", "https://www.korpora.org/Kant/aa07/063.html"),
],
},
"marx": {
"desc": "Triết gia, nhà kinh tế học, nhà hoạt động cách mạng thế kỷ 19: duy vật lịch sử, tha hóa, giá trị thặng dư, và luận cương “điều cốt yếu là thay đổi thế giới”.",
"bio": [
"Nhiều sinh viên Việt Nam gặp Karl Marx lần đầu qua môn triết học Mác – Lênin. Trang này nhìn ông như một triết gia thế kỷ 19, được đào tạo bài bản về triết học, với những lập luận mà giới nghiên cứu còn tranh luận đến nay.",
"Marx sinh ngày 5/5/1818 ở Trier (vương quốc Phổ), trong một gia đình gốc Do Thái; cha ông, một luật sư, đã cải sang đạo Tin Lành. Ông học luật và triết học ở Bonn rồi Berlin, nơi triết học Hegel đang thống trị, và nhập nhóm “Hegel trẻ”. Năm 1841 ông nhận bằng tiến sĩ ở Jena với luận án về triết học tự nhiên của Democritus và Epicurus. Khi cánh cửa đại học đóng lại với nhóm Hegel trẻ, ông chuyển sang làm báo: tờ *Rheinische Zeitung* do ông làm chủ bút bị đình bản; ông sang Paris (1843), bị trục xuất sang Brussels (1845), rồi từ năm 1849 sống ở London cho đến cuối đời.",
"Qua một tạp chí ở Paris, ông quen Friedrich Engels, người cùng ông viết *Tuyên ngôn của Đảng Cộng sản* (1848) và về sau chu cấp cho gia đình ông. Những năm 1850 ở London là những năm túng quẫn: cả nhà sống trong hai căn phòng nhỏ ở khu Soho, và bốn trong bảy người con của ông mất khi còn nhỏ. Ông vẫn ngày ngày nghiên cứu ở thư viện Bảo tàng Anh, cùng Engels viết gần 500 bài cho tờ *New York Tribune*, và năm 1867 in tập 1 bộ *Tư bản*; hai tập sau do Engels biên tập, in năm 1885 và 1894. Marx mất ngày 14/3/1883 ở London.",
"Tư tưởng của Marx truyền cảm hứng cho các phong trào công nhân và các nhà nước cộng sản thế kỷ 20 — một di sản lịch sử phức tạp mà người ủng hộ và người phê phán đánh giá rất khác nhau. Trong học thuật, những khái niệm như giai cấp, ý thức hệ, tha hóa đã đi vào xã hội học, sử học, kinh tế học; ngay cả nhà kinh tế không theo Marx như Joan Robinson vẫn đánh giá cao phân tích của ông về xung đột lợi ích giữa lao động và tư bản, và về chu kỳ bùng nổ – suy thoái. Trên mộ ông ở nghĩa trang Highgate (London) có khắc một câu trích từ *Luận cương về Feuerbach*.",
],
"works": [
("1844", "*Ökonomisch-philosophische Manuskripte*", "*Bản thảo kinh tế – triết học*: lao động bị tha hóa (gần một thế kỷ sau mới công bố)"),
("1845", "*Thesen über Feuerbach*", "*Luận cương về Feuerbach*, Engels in lần đầu năm 1888"),
("1845–1846", "*Die deutsche Ideologie*", "*Hệ tư tưởng Đức* (cùng Engels), in năm 1932"),
("1848", "*Manifest der Kommunistischen Partei*", "*Tuyên ngôn của Đảng Cộng sản* (cùng Engels)"),
("1859", "*Zur Kritik der politischen Ökonomie*", "*Góp phần phê phán kinh tế chính trị học*: lời tựa tóm tắt duy vật lịch sử"),
("1867", "*Das Kapital*, tập 1", "*Tư bản*: hàng hóa, giá trị thặng dư, bóc lột"),
],
"thoughts": [
"**Con người là sinh thể sản xuất.** Trước khi làm chính trị hay nghệ thuật, con người phải cùng nhau làm ra cái ăn, cái mặc; muốn hiểu một xã hội, hãy bắt đầu từ cách nó tổ chức lao động. Bản chất con người, trong hiện thực của nó, là “tổng hòa các quan hệ xã hội” (luận cương 6 về Feuerbach).",
"**Tha hóa.** Trong bản thảo 1844, người lao động dưới chủ nghĩa tư bản bị tách khỏi sản phẩm mình làm ra, khỏi chính hoạt động lao động, khỏi người khác và khỏi bản chất người của mình — như người thợ đứng chuyền cả ngày lặp lại một thao tác.",
"**Duy vật lịch sử.** Lực lượng sản xuất (công cụ, kỹ thuật, kỹ năng) định hình quan hệ sản xuất; trên nền kinh tế ấy mọc lên pháp luật, nhà nước và các hình thức ý thức. Khi một trật tự kinh tế trở thành “xiềng xích” kìm hãm sức sản xuất, nó sẽ bị thay thế.",
"**Ý thức hệ.** Trong mỗi thời đại, tư tưởng thống trị là tư tưởng của giai cấp thống trị: điều phục vụ lợi ích của một nhóm thường được trình bày như lẽ tự nhiên, phổ quát.",
],
"argument": {
"title": "Lợi nhuận từ đâu ra? Lập luận về bóc lột",
"intro": "Nếu trên thị trường mọi thứ đều được mua bán đúng giá, lợi nhuận của nhà tư bản từ đâu mà có? Đây là câu trả lời của *Tư bản*, theo cách trình bày phổ biến:",
"premises": [
"Giá trị của một hàng hóa do lượng lao động xã hội cần thiết để làm ra nó quyết định (thuyết giá trị lao động).",
"Nhà tư bản không mua “lao động” mà mua *sức lao động* của công nhân trong một ngày, và trả đúng giá trị của nó: giá trị những thứ người ấy cần để sống qua ngày — giả sử bằng bốn giờ lao động.",
"Nhưng ngày làm việc dài hơn, chẳng hạn tám giờ: bốn giờ đầu tạo ra giá trị bằng tiền công, bốn giờ sau tạo ra *giá trị thặng dư* thuộc về nhà tư bản.",
],
"conclusion": "Vậy lợi nhuận bắt nguồn từ phần lao động không được trả công, ngay cả khi mọi trao đổi đều “ngang giá” và không ai gian lận. Marx gọi quan hệ ấy là bóc lột.",
"objection": "Thuyết giá trị lao động bị nhiều nhà kinh tế coi là đã lỗi thời; chính Marx gặp khó khi giải thích vì sao giá cả lệch khỏi giá trị (“bài toán chuyển hóa”), và John Roemer chỉ ra có thể dựng một “thuyết giá trị ngô” với cấu trúc y hệt. Robert Nozick (1974) kết luận: thuyết giá trị lao động sai thì thuyết bóc lột của Marx sụp theo.",
"reply": "Nhiều người theo Marx, như G. A. Cohen và John Roemer, đáp rằng lời buộc tội cốt lõi không cần thuyết giá trị lao động: người làm công bỏ ra nhiều giờ lao động hơn số giờ lao động chứa trong những gì tiền công mua được, và buộc phải chấp nhận vì không sở hữu tư liệu sản xuất. Điều đó có *bất công* không thì còn bỏ ngỏ — thú vị là chính Marx chưa bao giờ nói thẳng rằng chủ nghĩa tư bản bất công.",
},
"quote": {
"source": "Karl Marx, “Thesen über Feuerbach” (viết mùa xuân 1845), luận cương 11 — nguyên văn tiếng Đức theo bản Engels in năm 1888",
"orig": "Die Philosophen haben die Welt nur verschieden interpretirt; es kommt aber darauf an, sie zu verändern.",
"vi": "Các triết gia mới chỉ giải thích thế giới theo những cách khác nhau; nhưng điều cốt yếu là thay đổi nó.",
"url": "https://de.wikisource.org/wiki/Thesen_%C3%BCber_Feuerbach",
},
"misread": [
"**“Marx nói tôn giáo là thuốc phiện để chế giễu người có đạo.”** Thực ra câu ấy (1844) nằm trong một đoạn văn gần như cảm thông: tôn giáo vừa là biểu hiện của nỗi khổ có thật vừa là lời phản kháng chống lại nó, là “tiếng thở dài của sinh linh bị áp bức, trái tim của một thế giới không có trái tim”. Marx vẫn coi nó là liều giảm đau tạo ảo tưởng, nhưng điều ông nhắm tới là những điều kiện sống khiến con người cần đến nó.",
"**“Marx đã vẽ sẵn bản thiết kế chi tiết cho xã hội tương lai.”** Thực ra ông nổi tiếng là ngại mô tả cụ thể xã hội cộng sản: ông phê phán những nhà xã hội chủ nghĩa “không tưởng” chuyên vẽ kế hoạch chi tiết, và cho rằng cấu trúc của xã hội mới sẽ do chính tiến trình lịch sử đưa tới, không phải hiện thực hóa một bản vẽ có trước.",
],
"related": [
("cau-hoi/viet-hien-dai.md", "Triết học Việt Nam hiện đại, từ Nho học đến Marx và hiện sinh"),
("lich-su/the-ky-19.md", "Thế kỷ 19: hệ thống vỡ vụn"),
("lich-su/nhat-ban-viet-nam.md", "Nhật Bản và Việt Nam: triết học ở phương Đông"),
],
"sources": [
("Wolff, Jonathan & David Leopold, “Karl Marx”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/marx/"),
("Feuer, Lewis S. và các tác giả khác, “Karl Marx”, *Encyclopaedia Britannica*.", "https://www.britannica.com/biography/Karl-Marx"),
("“Das Kapital”, *Encyclopaedia Britannica*.", "https://www.britannica.com/topic/Das-Kapital"),
("Marx, Karl, “Thesen über Feuerbach” (1845; in 1888), Wikisource tiếng Đức.", "https://de.wikisource.org/wiki/Thesen_%C3%BCber_Feuerbach"),
("Marx, Karl, “Zur Kritik der Hegel’schen Rechtsphilosophie. Einleitung”, *Deutsch-Französische Jahrbücher* (1844), Wikisource tiếng Đức.", "https://de.wikisource.org/wiki/Zur_Kritik_der_Hegel%E2%80%99schen_Rechtsphilosophie"),
],
},
"nietzsche": {
"desc": "Nhà ngữ văn cổ điển thành triết gia: “Chúa đã chết”, phả hệ của đạo đức, vĩnh cửu luân hồi — và một di sản từng bị em gái ông và người Quốc xã bóp méo.",
"bio": [
"Năm 1869, Friedrich Nietzsche được mời làm giáo sư ngữ văn cổ điển ở Đại học Basel khi mới 24 tuổi — người trẻ nhất từng giữ chức ấy. Ông sinh ngày 15/10/1844 ở Röcken, gần Leipzig; cha ông, một mục sư Lutheran, mất khi ông lên bốn, và cậu bé lớn lên ở Naumburg giữa mẹ, bà, hai cô và em gái Elisabeth. Người thầy của ông viết trong thư giới thiệu rằng chàng trai này “muốn làm gì cũng làm được”.",
"Cuốn sách đầu tay, *Sự ra đời của bi kịch* (1872), bị giới ngữ văn chê thậm tệ: không phải một khảo cứu cẩn trọng mà là một tuyên ngôn đặt hy vọng phục hưng văn hóa Đức vào nhạc kịch của người bạn thân Richard Wagner. Tình bạn ấy tan vỡ khi Nietzsche gửi Wagner cuốn *Con người, quá đỗi con người* (1878). Bệnh tật — đau đầu dữ dội, buồn nôn, mắt kém — buộc ông thôi dạy năm 1879. Từ đó ông sống lang bạt giữa nước Ý và vùng núi Thụy Sĩ, gần như năm nào cũng ra một cuốn: *Khoa học vui* (1882), *Zarathustra đã nói như thế* (1883–1885), *Bên kia thiện và ác* (1886), *Phả hệ của đạo đức* (1887).",
"Tháng 1/1889, ông gục ngã trên phố ở Turin và không bao giờ hồi phục trí tuệ; ông sống thêm mười một năm trong sự chăm sóc của mẹ rồi của em gái, và mất ngày 25/8/1900 ở Weimar. Elisabeth nắm toàn quyền di cảo của anh, biên tập từ các sổ tay của ông một cuốn *Ý chí quyền lực* không đúng với kế hoạch của tác giả và nhuốm quan điểm bài Do Thái của chính bà.",
"Nietzsche viết bằng châm ngôn, ẩn dụ, giọng mỉa mai: dễ trích, khó hiểu. Cùng với Marx và Freud, ông thuộc dòng tư tưởng “diễn giải bằng nghi ngờ”, truy tìm những động cơ khuất lấp sau những giá trị ta tưởng cao quý. Ảnh hưởng của ông trải từ Freud, Heidegger, các nhà hiện sinh tới triết học Pháp những năm 1960–1980. Câu hỏi của ông vẫn còn đó: khi những chỗ dựa cũ không còn thuyết phục, ta lấy gì để nói một cuộc đời là đáng sống?",
],
"works": [
("1872", "*Die Geburt der Tragödie*", "*Sự ra đời của bi kịch*: Hy Lạp, Dionysos và Wagner"),
("1878", "*Menschliches, Allzumenschliches*", "*Con người, quá đỗi con người*: lối viết châm ngôn, chia tay Wagner"),
("1882/1887", "*Die fröhliche Wissenschaft*", "*Khoa học vui*: người điên báo tin “Chúa đã chết” (§125)"),
("1883–1885", "*Also sprach Zarathustra*", "*Zarathustra đã nói như thế*: siêu nhân, vĩnh cửu luân hồi"),
("1886", "*Jenseits von Gut und Böse*", "*Bên kia thiện và ác*"),
("1887", "*Zur Genealogie der Moral*", "*Phả hệ của đạo đức*: ba khảo luận về nguồn gốc các giá trị đạo đức"),
],
"thoughts": [
"**Phả hệ của đạo đức.** Có hai lối đánh giá: “tốt/xấu” của tầng lớp quý tộc, đề cao sự xuất chúng, và “thiện/ác”, đề cao lòng vị tha, khiêm nhường, bình đẳng. Theo Nietzsche, lối thứ hai thắng thế nhờ một “cuộc nổi dậy của nô lệ trong đạo đức”: những người bị áp bức mà bất lực ủ một sự oán hận (*ressentiment*) và đảo ngược bảng giá trị của kẻ mạnh.",
"**Thuyết viễn cảnh.** Không có cái nhìn từ hư không: mọi hiểu biết đều xuất phát từ một góc nhìn. Nhưng góc nhìn không chỉ là chướng ngại: “khách quan”, với Nietzsche, là khả năng đặt nhiều góc nhìn, nhiều cái thích và không thích cạnh nhau để hiểu sự việc đầy đủ hơn (*Phả hệ*, III, 12).",
"**Vĩnh cửu luân hồi như một phép thử.** Một con quỷ thì thầm rằng bạn sẽ phải sống lại cuộc đời này y hệt, vô số lần (*Khoa học vui*, §341). Bạn sẽ nguyền rủa nó, hay đáp “chưa bao giờ tôi nghe điều gì thiêng liêng hơn”? Câu hỏi ấy đo xem ta khẳng định được cuộc đời mình đến đâu.",
"**Siêu nhân.** *Übermensch* trong *Zarathustra* là hình ảnh một con người tự tạo ra giá trị thay vì thừa hưởng; giới nghiên cứu còn tranh cãi nên hiểu nó là một lý tưởng, một kiểu người, hay một ý niệm tự mâu thuẫn.",
],
"argument": {
"title": "Hỏi về giá trị của chính các giá trị",
"intro": "Ta thường hỏi một hành động có đạo đức không. Nietzsche hỏi sâu hơn: bản thân đạo đức có giá trị gì, và tốt cho ai? Đây là cách tái dựng ý chính của *Phả hệ của đạo đức* (1887):",
"premises": [
"Những giá trị ta coi là hiển nhiên — vị tha, khiêm nhường, bình đẳng, tránh khổ — có một lịch sử: chúng đã thay thế những bảng giá trị khác.",
"Lịch sử ấy cho thấy chúng đáp ứng nhu cầu tâm lý của một kiểu người — sự oán hận của kẻ bất lực — chứ không được khám phá như chân lý vĩnh cửu.",
"Một bảng giá trị đòi áp dụng như nhau cho mọi người có thể kìm hãm chính những cá nhân có khả năng đạt tới sự xuất chúng cao nhất.",
],
"conclusion": "Vậy không thể coi giá trị của đạo đức là điều đã được bảo đảm; phải đặt nó thành câu hỏi và đánh giá nó qua tác động của nó lên đời sống con người.",
"objection": "Đây có vẻ là **ngụy biện nguồn gốc** (*genetic fallacy*): nguồn gốc của một niềm tin không quyết định nó đúng hay sai. Dù lòng thương người có ra đời từ oán hận đi nữa, điều đó không chứng minh lòng thương người là xấu. Hơn nữa, thước đo “sự xuất chúng của số ít” mà Nietzsche dùng có vẻ tinh hoa, và cũng cần biện minh không kém.",
"reply": "Chính Nietzsche đã lường trước điểm này: trong *Khoa học vui* (§345), ông viết rằng một nền đạo đức có thể mọc lên từ một sai lầm mà điều đó vẫn chưa chạm tới vấn đề giá trị của nó. Phả hệ không nhằm bác bỏ đạo đức bằng nguồn gốc, mà phá vỡ vầng hào quang khiến ta không dám hỏi; câu hỏi về giá trị sau đó phải được trả lời bằng tác động thực của nó. Còn thước đo của ông có tinh hoa hay không thì vẫn là chỗ tranh luận lớn.",
},
"quote": {
"source": "Friedrich Nietzsche, *Die fröhliche Wissenschaft* (1882), §125 “Người điên” — bản dịch tiếng Anh của Thomas Common (*The Joyful Wisdom*, 1910)",
"orig": "God is dead! God remains dead! And we have killed him! How shall we console ourselves, the most murderous of all murderers?",
"vi": "Chúa đã chết! Chúa vẫn chết! Và chính chúng ta đã giết Người! Chúng ta, những kẻ sát nhân bậc nhất trong mọi kẻ sát nhân, sẽ lấy gì tự an ủi?",
"url": "https://www.gutenberg.org/ebooks/52881",
},
"misread": [
"**“Nietzsche hả hê tuyên bố Chúa đã chết; ông là kẻ hư vô.”** Thực ra trong *Khoa học vui* (§125), câu ấy là của một người điên, nói với giọng kinh hoàng trước đám đông không tin Chúa đang cười cợt anh: họ chưa hiểu hệ quả của điều chính họ đã làm. Nietzsche coi chủ nghĩa hư vô là căn bệnh của thời đại cần vượt qua, và đi tìm cách khẳng định cuộc đời thay vì phủ nhận nó.",
"**“Nietzsche là triết gia của Quốc xã.”** Thực ra em gái ông — vợ một nhà hoạt động bài Do Thái — đã biên tập di cảo theo ý mình và về sau giao du với Hitler và Mussolini; người Quốc xã cắt ghép có chọn lọc các đoạn văn của ông. Bản thân Nietzsche đau lòng vì thái độ bài Do Thái của em gái và nhiều lần công kích giới bài Do Thái. Nhưng ông cũng không phải người dân chủ: nhiều trang của ông khinh miệt “bầy đàn” và đề cao kẻ mạnh, và người đọc nên thấy cả hai mặt.",
],
"related": [
("lich-su/the-ky-19.md", "Thế kỷ 19: hệ thống vỡ vụn"),
],
"sources": [
("Anderson, R. Lanier, “Friedrich Nietzsche”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/nietzsche/"),
("Wicks, Robert, “Nietzsche’s Life and Works”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/nietzsche-life-works/"),
("Leiter, Brian, “Nietzsche’s Moral and Political Philosophy”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/nietzsche-moral-political/"),
("Nietzsche, Friedrich, *The Joyful Wisdom*, Thomas Common dịch (1910), Project Gutenberg.", "https://www.gutenberg.org/ebooks/52881"),
],
},
"frege": {
"desc": "Nhà toán học ở Jena đặt nền cho logic hiện đại và triết học ngôn ngữ phân tích: logic vị từ, nghĩa và vật được chỉ, ý nghĩ như một nội dung khách quan.",
"bio": [
"Gottlob Frege gắn gần trọn đời làm việc với Đại học Jena. Sinh ngày 8/11/1848 ở Wismar, ông vào Đại học Jena năm 1869, lấy bằng tiến sĩ toán ở Göttingen (1873), rồi về dạy toán ở Jena cho đến khi nghỉ hưu năm 1917. Lúc sinh thời ông ít được biết đến: cuốn sách nhỏ *Begriffsschrift* (1879), nơi ông dựng hệ thống mà ngày nay ta coi là logic vị từ đầu tiên, vừa khó đọc vì lối ký hiệu trải theo hai chiều, vừa bị đón nhận lạnh nhạt.",
"Dự án của đời ông là chứng minh rằng số học thực chất là logic: mọi khái niệm số học định nghĩa được bằng khái niệm logic, mọi định lý suy ra được từ định luật logic. *Die Grundlagen der Arithmetik* (1884) phác thảo dự án bằng văn xuôi; hai tập *Grundgesetze der Arithmetik* (1893, 1903) thực hiện nó bằng ký hiệu. Để làm nền cho dự án ấy, ông xây cả một triết học về ngôn ngữ, với bài báo nền móng “Về nghĩa và vật được chỉ” (1892). Một số nghiên cứu gần đây còn cho thấy ông vay mượn khá nhiều từ logic học của phái Khắc kỷ.",
"Ngày 16/6/1902, khi đang sửa bản in tập II, Frege nhận thư của Bertrand Russell: từ một tiên đề của ông (Định luật cơ bản V) có thể suy ra mâu thuẫn — nghịch lý về tập hợp của mọi tập hợp không chứa chính nó. Frege viết thêm một phụ lục cho tập II để đối mặt với nghịch lý, nhưng không bao giờ cứu được dự án. Ông vẫn dạy học; Rudolf Carnap là một trong những sinh viên ghi chép bài giảng của ông. Nhật ký năm 1924 cho thấy ông có cảm tình với chủ nghĩa phát xít và bài Do Thái. Ông mất ngày 26/7/1925 ở Bad Kleinen.",
"Danh tiếng của Frege đến chủ yếu sau khi ông mất, qua Russell, Wittgenstein và Carnap. Hệ thống lượng từ (“mọi”, “có ít nhất một”) mà ông đặt nền vẫn là cốt lõi của phần lớn các hệ logic ngày nay; còn câu hỏi ông nêu — vì sao hai cái tên cùng chỉ một vật lại cho ta biết thêm điều mới — vẫn ở trung tâm của triết học ngôn ngữ.",
],
"works": [
("1879", "*Begriffsschrift*", "*Ký pháp khái niệm*: logic vị từ đầu tiên"),
("1884", "*Die Grundlagen der Arithmetik*", "*Cơ sở của số học*: số là gì; nguyên lý ngữ cảnh"),
("1892", "“Über Sinn und Bedeutung”", "“Về nghĩa và vật được chỉ”: câu đố Sao Mai – Sao Hôm"),
("1893/1903", "*Grundgesetze der Arithmetik*", "*Các định luật cơ bản của số học*, hai tập; tập II kèm phụ lục về nghịch lý Russell"),
("1918", "“Der Gedanke”", "“Ý nghĩ”: chân lý và ý nghĩ như một nội dung khách quan"),
],
"thoughts": [
"**Logic vị từ.** Frege phân tích câu thành hàm và đối số (“yêu” là một hàm có hai chỗ trống: *x* yêu *y*), thêm các lượng từ “mọi” và “có ít nhất một”, nhờ đó viết được cả những câu như “ai cũng yêu một người nào đó”. Lần đầu tiên có một ngôn ngữ hình thức đủ sức viết lại từng bước một chứng minh toán học.",
"**Nghĩa và vật được chỉ.** Một cái tên vừa chỉ tới một vật (*Bedeutung*), vừa trình bày vật ấy theo một cách nhất định (*Sinn*, nghĩa). “Sao Mai” và “Sao Hôm” cùng chỉ sao Kim nhưng khác cách trình bày, nên “Sao Mai là Sao Hôm” là một phát hiện thiên văn, còn “Sao Mai là Sao Mai” chẳng cho ta biết gì.",
"**Số là phát biểu về khái niệm.** Cùng một bó đũa có thể là 1 bó, 10 đôi hay 20 chiếc: câu hỏi “bao nhiêu?” chỉ có nghĩa khi đã nói rõ đếm *cái gì*. Cùng tinh thần ấy là nguyên lý ngữ cảnh: đừng bao giờ hỏi nghĩa của một từ khi tách nó khỏi câu (*Grundlagen*, 1884).",
"**Ý nghĩ là của chung.** Ý nghĩ (*Gedanke*) không phải hoạt động chủ quan trong đầu ai đó, mà là nội dung khách quan “có thể là tài sản chung của nhiều người” (1892). Logic nói điều gì theo sau từ điều gì, chứ không mô tả đầu óc ta thường vận hành ra sao.",
],
"argument": {
"title": "Câu đố Sao Mai – Sao Hôm",
"intro": "Bài “Về nghĩa và vật được chỉ” (1892) mở đầu bằng một câu đố về các câu đồng nhất. Lời giải của Frege, tái dựng ở dạng chuẩn:",
"premises": [
"“Sao Mai là Sao Mai” đúng một cách hiển nhiên, không cần quan sát gì; còn “Sao Mai là Sao Hôm” là một phát hiện thiên văn, mở rộng hiểu biết của ta.",
"Nếu nghĩa của một cái tên chỉ là vật nó chỉ tới, thì vì “Sao Mai” và “Sao Hôm” cùng chỉ sao Kim, hai câu trên phải có cùng nội dung và cùng giá trị nhận thức.",
"Nhưng chúng rõ ràng khác nhau về giá trị nhận thức.",
],
"conclusion": "Vậy nghĩa của một cái tên không chỉ là vật nó chỉ tới: ngoài vật được chỉ (*Bedeutung*), mỗi tên còn có một *nghĩa* (*Sinn*) — cách thức vật ấy được trao cho ta.",
"objection": "Saul Kripke (1972) phản bác cách hiểu “nghĩa” như một mô tả gắn với tên. Ta nói hợp lý rằng “Nguyễn Du có thể đã không viết *Truyện Kiều*”; nhưng nếu nghĩa của “Nguyễn Du” là “tác giả *Truyện Kiều*” thì câu ấy thành “tác giả *Truyện Kiều* có thể đã không viết *Truyện Kiều*”. Lại có nhiều người dùng đúng một cái tên mà không biết gì đủ để phân biệt người mang tên ấy với người khác. Theo Kripke, tên chỉ trực tiếp tới vật, qua một chuỗi truyền miệng bắt đầu từ lần đặt tên.",
"reply": "Người theo Frege đáp: thuyết quy chiếu trực tiếp vẫn chưa giải được câu đố ban đầu — nếu nghĩa của tên chỉ là vật được chỉ, vì sao “Sao Mai là Sao Hôm” cần kính thiên văn còn “Sao Mai là Sao Mai” thì không? Hơn nữa, Frege định nghĩa nghĩa là *cách thức* đối tượng được trao cho ta, không bắt buộc đó phải là một mô tả; và một số người theo thuyết mô tả chuyển sang dùng mô tả được “cố định hóa” để tránh phản bác của Kripke.",
},
"quote": {
"source": "Gottlob Frege, “Über Sinn und Bedeutung”, *Zeitschrift für Philosophie und philosophische Kritik* 100 (1892), tr. 26–27 — nguyên văn tiếng Đức (chữ ſ viết thành s)",
"orig": "Es liegt nun nahe, mit einem Zeichen (Namen, Wortverbindung, Schriftzeichen) außer dem Bezeichneten, was die Bedeutung des Zeichens heißen möge, noch das verbunden zu denken, was ich den Sinn des Zeichens nennen möchte, worin die Art des Gegebenseins enthalten ist. […] Es würde die Bedeutung von „Abendstern“ und „Morgenstern“ dieselbe sein, aber nicht der Sinn.",
"vi": "Vậy tự nhiên ta nghĩ rằng gắn với một ký hiệu (tên gọi, cụm từ, chữ viết), ngoài cái được ký hiệu chỉ tới — có thể gọi là vật được chỉ của ký hiệu — còn có cái mà tôi muốn gọi là nghĩa của ký hiệu, chứa đựng cách thức vật ấy được trao cho ta. […] Vật được chỉ của “Sao Hôm” và “Sao Mai” sẽ là một, nhưng nghĩa thì không.",
"url": "https://www.deutschestextarchiv.de/book/show/frege_sinn_1892",
},
"misread": [
"**“Nghịch lý Russell đã xóa sổ công trình của Frege.”** Thực ra hệ tiên đề của *Grundgesetze* đúng là mâu thuẫn, nhưng logic vị từ, các định nghĩa và phương pháp của ông vẫn đứng vững. Năm 1993, Richard Heck chỉ ra rằng phần Frege suy ra các tiên đề số học từ “nguyên lý Hume” vẫn hợp lệ mà không cần tiên đề gây mâu thuẫn; kết quả này ngày nay được gọi là “định lý Frege”.",
"**“Frege trước hết là một triết gia ngôn ngữ.”** Thực ra triết học ngôn ngữ của ông ra đời để làm nền cho một dự án toán học — chứng minh số học là logic — và cả đời ông giảng dạy ở khoa toán.",
],
"related": [
("lich-su/the-ky-20.md", "Thế kỷ 20: triết học chia hai ngả"),
("cau-hoi/chan-ly.md", "Sự thật là gì?"),
("cau-hoi/sieu-dao-duc.md", "Đúng sai có khách quan không?"),
],
"sources": [
("Zalta, Edward N., “Gottlob Frege”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/frege/"),
("Michaelson, Eliot, “Reference”, *Stanford Encyclopedia of Philosophy* (thuyết mô tả và phản bác của Kripke).", "https://plato.stanford.edu/entries/reference/"),
("Frege, Gottlob, “Über Sinn und Bedeutung” (1892), Deutsches Textarchiv.", "https://www.deutschestextarchiv.de/book/show/frege_sinn_1892"),
],
},
"husserl": {
"desc": "Người sáng lập hiện tượng luận: chống tâm lý luận, ý hướng tính, đặt ngoặc thái độ tự nhiên, thế giới đời sống; ảnh hưởng từ Heidegger, Sartre đến Trần Đức Thảo.",
"bio": [
"Paris, khoảng năm 1932. Trong một quán bar, Raymond Aron kể với Jean-Paul Sartre về một triết học mới từ Đức: với nó, người ta có thể mô tả đồ vật đúng như mình nhìn thấy và chạm vào — kể cả ly cocktail mơ trên bàn — và rút ra triết học từ đó. Theo hồi ký của Simone de Beauvoir, Sartre lập tức lao vào tìm đọc. Triết học ấy là hiện tượng luận, và người sáng lập nó là Edmund Husserl.",
"Husserl sinh ngày 8/4/1859 ở Proßnitz (Moravia, nay thuộc Cộng hòa Séc), trong một gia đình Do Thái. Ông học toán ở Leipzig và Berlin, lấy bằng tiến sĩ toán ở Vienna (1883); các bài giảng của Franz Brentano khiến ông chuyển hẳn sang triết học. Cuốn sách đầu, *Triết học số học* (1891), muốn đặt toán học trên nền tâm lý học và bị Frege phê bình là “tâm lý luận”. Bộ *Khảo cứu logic* (1900–1901), mà chính ông gọi là “bước đột phá”, mang lại cho ông ghế giảng ở Göttingen (1901–1916); sau đó ông về Freiburg, nơi Martin Heidegger làm trợ lý cho ông (1919–1923) và kế nhiệm ghế giáo sư của ông năm 1928.",
"Dưới chế độ Quốc xã, dù đã theo đạo Tin Lành từ năm 1886, Husserl bị gạt khỏi mọi hoạt động học thuật vì gốc Do Thái, mất quyền giảng dạy, xuất bản, rồi mất cả quốc tịch Đức. Ông vẫn viết mỗi ngày; *Khủng hoảng của các khoa học châu Âu* (1936) là lời bênh vực lý tính giữa lúc châu Âu trượt vào phi lý. Ông mất ngày 27/4/1938, để lại khoảng 45.000 trang bản thảo. Một tu sĩ dòng Phanxicô trẻ, Van Breda, đã bí mật đưa chúng sang Bỉ; Kho lưu trữ Husserl ở Leuven ra đời ngay trước Thế chiến II.",
"Ảnh hưởng của Husserl lan khắp triết học châu Âu thế kỷ 20: Heidegger, Edith Stein, Merleau-Ponty, Sartre, Levinas, Derrida… Với người Việt có một mối liên hệ đặc biệt: Trần Đức Thảo, khi ở Paris những năm 1940, là một trong những người đầu tiên nghiên cứu Husserl nghiêm túc ở Pháp, đọc cả các bản thảo chưa in của ông, rồi viết *Hiện tượng luận và duy vật biện chứng* (1951) để nối hiện tượng luận với Marx.",
],
"works": [
("1891", "*Philosophie der Arithmetik*", "*Triết học số học*: bị Frege phê bình năm 1894"),
("1900–1901", "*Logische Untersuchungen*", "*Khảo cứu logic*: phê phán tâm lý luận, phân tích ý hướng tính"),
("1913", "*Ideen I*", "*Ý tưởng cho một hiện tượng luận thuần túy*, tập I: đặt ngoặc, bước ngoặt siêu nghiệm"),
("1931", "*Méditations cartésiennes*", "*Suy niệm kiểu Descartes*: các bài giảng ở Paris, bản tiếng Pháp in trước"),
("1936", "*Die Krisis der europäischen Wissenschaften*", "*Khủng hoảng của các khoa học châu Âu*: thế giới đời sống"),
],
"thoughts": [
"**Trở về với chính các sự vật.** Đừng vội dựng lý thuyết hay cãi nhau bằng chữ suông; hãy mô tả cái thực sự hiện ra trong kinh nghiệm trước khi giải thích. Đi quanh một cái cây, ta chỉ thấy từng mặt mà vẫn thấy *một* cái cây: hiện tượng luận hỏi điều đó diễn ra thế nào.",
"**Ý hướng tính.** Mọi trạng thái ý thức đều hướng về một cái gì đó: nghi ngờ *rằng* trời sẽ mưa, mong *rằng* trời mưa, thấy cuốn hộ chiếu trong ngăn kéo. Husserl nhận ý tưởng này từ Brentano và phân tích nó tỉ mỉ: nghĩ đến cuốn hộ chiếu khác với nhìn thấy nó tận mắt.",
"**Đặt ngoặc thái độ tự nhiên.** Thường ngày ta mặc nhiên coi thế giới là có đó. *Epoché* không phủ nhận điều ấy, chỉ tạm treo hiệu lực của nó để hỏi một câu khác: thế giới hiện ra *như thế nào* để ta có thể coi nó là thật?",
"**Thế giới đời sống.** Khoa học chính xác là thành tựu lớn, nhưng nó mọc lên từ thế giới đời sống quen thuộc và không thay thế được thế giới ấy. Người bán cam ngoài chợ cần cân đúng một ký, không cần cân đến micrôgam: độ chính xác “đủ” tùy vào ngữ cảnh.",
],
"argument": {
"title": "Logic không phải là tâm lý học",
"intro": "Cuối thế kỷ 19, nhiều người cho rằng logic là một nhánh của tâm lý học, vì suy luận là hoạt động của đầu óc. Phần đầu *Khảo cứu logic* (1900) phản bác:",
"premises": [
"Quy luật tâm lý là khái quát từ kinh nghiệm về cách người ta thực sự suy nghĩ, nên chỉ có thể gần đúng và mang tính xác suất, như mọi quy luật kinh nghiệm.",
"Quy luật logic, như luật không mâu thuẫn, thì chính xác và chắc chắn; ta không cần khảo sát thêm ai để biết nó còn đúng không.",
"Khi bạn và tôi cùng nghĩ về định lý Pythagoras, hai quá trình tâm lý khác nhau, nhưng điều được nghĩ là một; nếu không, ta chẳng thể hiểu nhau hay xây dựng khoa học.",
],
"conclusion": "Vậy logic không thể quy về tâm lý học: nó nói về những cấu trúc lý tưởng — nghĩa, mệnh đề, quan hệ suy luận — chứ không về các diễn biến trong đầu.",
"objection": "Người theo tự nhiên luận đáp: chính sự chắc chắn của logic có thể là một sự kiện tâm lý, sản phẩm của tiến hóa và thói quen. Quine (1951) còn cho rằng không mệnh đề nào miễn nhiễm với sửa đổi, kể cả luật logic — luật bài trung từng được đề xuất bỏ đi để đơn giản hóa cơ học lượng tử.",
"reply": "Người theo Husserl đáp: hiểu biết của ta *về* logic có thể sai và thay đổi, nhưng điều đó không biến *hiệu lực* của một luật logic thành một sự kiện tâm lý; hành vi nghĩ diễn ra trong thời gian, điều được nghĩ thì không. Hơn nữa, để lập luận rằng logic chỉ là tâm lý học, người phản bác vẫn phải dựa vào các quy tắc suy luận như những chuẩn mực có hiệu lực cho mọi người — tức là dựa vào chính điều mình phủ nhận.",
},
"quote": {
"source": "Edmund Husserl, *Logische Untersuchungen*, tập II (1901), Dẫn nhập, §2 — nguyên văn tiếng Đức bản in lần đầu (chính tả hiện đại hóa)",
"orig": "Wir wollen uns schlechterdings nicht mit „bloßen Worten“, das ist mit einem bloß symbolischen Wortverständnis zufrieden geben. […] Wir wollen auf die „Sachen selbst“ zurückgehen.",
"vi": "Chúng ta tuyệt đối không muốn bằng lòng với “chữ suông”, tức là với một cách hiểu từ ngữ chỉ thuần ký hiệu. […] Chúng ta muốn quay về với “chính các sự vật”.",
"url": "https://archive.org/details/logischeuntersuc00hussuoft",
},
"misread": [
"**“Đặt ngoặc nghĩa là nghi ngờ thế giới bên ngoài, như Descartes.”** Thực ra *epoché* không phủ nhận hay nghi ngờ thế giới: ta vẫn giữ niềm tin tự nhiên ấy nhưng tạm treo hiệu lực của nó để khảo sát cách thế giới hiện ra. Husserl coi Descartes là người mở đường cho bước ngoặt về chủ thể, nhưng gạt bỏ gần hết học thuyết cụ thể của Descartes.",
"**“Hiện tượng luận là nội quan: tự quan sát cảm xúc của mình.”** Thực ra Husserl về sau hối tiếc vì từng gọi hiện tượng luận là “tâm lý học mô tả”: nó không thu thập dữ kiện tâm lý của từng người mà tìm những cấu trúc chung của mọi kinh nghiệm.",
],
"related": [
("cau-hoi/viet-hien-dai.md", "Triết học Việt Nam hiện đại, từ Nho học đến Marx và hiện sinh"),
("lich-su/the-ky-20.md", "Thế kỷ 20: triết học chia hai ngả"),
("lich-su/nhat-ban-viet-nam.md", "Nhật Bản và Việt Nam: triết học ở phương Đông"),
],
"sources": [
("Zahavi, Dan, “Edmund Husserl”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/husserl/"),
("Reynolds, Jack & Pierre-Jean Renaudie, “Jean-Paul Sartre”, *Stanford Encyclopedia of Philosophy* (Sartre phát hiện hiện tượng luận; Trần Đức Thảo).", "https://plato.stanford.edu/entries/sartre/"),
("Husserl, Edmund, *Logische Untersuchungen*, tập II (Halle: Niemeyer, 1901), bản quét tại Internet Archive.", "https://archive.org/details/logischeuntersuc00hussuoft"),
("Banaji, Jairus, “Tran Duc Thao”, *Historical Materialism* (trang nhân vật, dựa trên Courtine 2013 và McHale 2002).", "https://www.historicalmaterialism.org/figure/tran-duc-thao/"),
],
},
"russell": {
"desc": "Nhà logic học, triết gia, nhà văn và nhà hoạt động: nghịch lý Russell, lý thuyết mô tả, “Những vấn đề của triết học”, phản đối vũ khí hạt nhân và chiến tranh Việt Nam.",
"bio": [
"Năm 1966, khi đã ngoài 90 tuổi, Bertrand Russell lập Tòa án Quốc tế về Tội ác Chiến tranh, trong chiến dịch phản đối sự can dự của phương Tây vào chiến tranh Việt Nam. Đó là chặng cuối của một cuộc đời dài gần một thế kỷ: nhà logic học đặt nền cho triết học phân tích, nhà văn đoạt giải Nobel, và người hai lần vào tù vì phản chiến và chống vũ khí hạt nhân.",
"Russell sinh ngày 18/5/1872 ở Trelleck, Monmouthshire (nay thuộc xứ Wales), trong một gia đình quý tộc; mồ côi cha mẹ từ nhỏ, ông được ông bà nội nuôi dạy — ông nội là cựu Thủ tướng Anh John Russell. Năm 11 tuổi, anh trai dạy ông hình học, và ông vào Trinity College, Cambridge năm 1890 để học toán. Năm 1901 ông phát hiện nghịch lý mang tên mình, rồi viết thư báo cho Frege (1902); cùng Alfred North Whitehead, ông viết *Principia Mathematica* (1910–1913), nỗ lực suy ra toán học từ logic.",
"Cùng G. E. Moore, Russell được xem là người sáng lập triết học phân tích hiện đại: dùng logic để phơi bày cấu trúc ẩn sau ngữ pháp, như trong bài “Về sự biểu thị” (1905). Ông là thầy, rồi là bạn và đối thủ tranh luận của Ludwig Wittgenstein. Thế chiến I biến ông thành nhà hoạt động: năm 1916 ông bị phạt và mất ghế giảng ở Trinity vì một truyền đơn phản chiến; năm 1918 ông ngồi tù năm tháng, và trong tù viết *Nhập môn triết học toán học*.",
"Russell tự coi mình trước hết là người viết — hộ chiếu ghi nghề “tác giả” — và viết cho mọi tầng lớp độc giả, từ *Những vấn đề của triết học* (1912) đến *Lịch sử triết học phương Tây* (1945). Ông nhận giải Nobel Văn học năm 1950, cùng Einstein ra tuyên ngôn chống vũ khí hạt nhân (1955), và năm 1961, ở tuổi 89, lại ngồi tù một tuần vì biểu tình chống hạt nhân. Ông cũng không phải thánh nhân: những bình luận của ông về ưu sinh và chủng tộc, và việc sau Thế chiến II ông từng chủ trương chiến tranh phòng ngừa với Liên Xô (điều về sau ông phủ nhận), vẫn bị phê phán. Ông mất ngày 2/2/1970 ở xứ Wales.",
],
"works": [
("1903", "*The Principles of Mathematics*", "*Các nguyên lý của toán học*"),
("1905", "“On Denoting”", "“Về sự biểu thị”: lý thuyết mô tả"),
("1910–1913", "*Principia Mathematica*", "cùng A. N. Whitehead, ba tập: suy ra toán học từ logic"),
("1912", "*The Problems of Philosophy*", "*Những vấn đề của triết học*: sách nhập môn kinh điển"),
("1918", "“The Philosophy of Logical Atomism”", "“Triết học nguyên tử luận logic”: loạt bài giảng ở London"),
("1945", "*A History of Western Philosophy*", "*Lịch sử triết học phương Tây*"),
],
"thoughts": [
"**Phân tích logic.** Ngữ pháp bề mặt có thể đánh lừa: một câu trông như nói về một vật có khi thực ra là một khẳng định phức hợp. Làm rõ hình thức logic ẩn bên dưới có thể làm tan biến nhiều câu đố triết học.",
"**Nghịch lý Russell.** Xét tập hợp gồm mọi tập hợp không chứa chính nó: nó có chứa chính nó không? Nếu có thì không, nếu không thì có. Phát hiện này cho thấy không thể tùy tiện gom mọi thứ thỏa một điều kiện thành một tập hợp, và đẩy ông tới lý thuyết kiểu (*theory of types*).",
"**Nhất nguyên luận trung tính.** Từ khoảng 1919, Russell cho rằng thế giới chỉ làm từ một loại “chất liệu”, không thuần tinh thần cũng không thuần vật chất; “tinh thần” và “vật chất” là hai cách sắp xếp cùng những dữ kiện ấy, như cùng một danh bạ có thể xếp theo vần hoặc theo địa chỉ.",
"**Triết học và hoài nghi đúng mức.** Triết học không cho ta câu trả lời chắc chắn, nhưng gỡ bỏ sự quả quyết giáo điều và mở rộng những gì ta có thể nghĩ tới (*Những vấn đề của triết học*, chương XV).",
],
"argument": {
"title": "Vua nước Pháp hiện nay có hói không? Lý thuyết mô tả",
"intro": "Câu “Vua nước Pháp hiện nay bị hói” có nghĩa, dù nước Pháp không có vua. Vậy nó đúng hay sai, và nói về ai? Bài “Về sự biểu thị” (1905) giải câu đố này như sau:",
"premises": [
"Theo hình thức logic thật của nó, câu ấy khẳng định ba điều: có ít nhất một người là vua nước Pháp hiện nay; có nhiều nhất một người như thế; và người đó bị hói.",
"Điều thứ nhất sai: nước Pháp là một nền cộng hòa.",
"Một câu khẳng định đồng thời nhiều điều sẽ sai nếu một trong các điều ấy sai.",
],
"conclusion": "Vậy câu ấy đơn giản là sai — không cần giả định một “ông vua không tồn tại” để nó có nghĩa. Cụm “vua nước Pháp hiện nay” không phải là một cái tên chỉ tới ai; ngữ pháp bề mặt đã che mất hình thức logic.",
"objection": "P. F. Strawson (“On Referring”, 1950) phản bác: khi không có vua Pháp, người bình thường không bảo câu ấy *sai* mà thấy câu hỏi đúng–sai không đặt ra, vì câu nói *giả định* chứ không *khẳng định* rằng có một vua Pháp. Russell, theo Strawson, đã lẫn lộn câu chữ với việc dùng câu chữ trong một hoàn cảnh cụ thể.",
"reply": "Russell không nhượng bộ (“Mr. Strawson on Referring”, 1957). Lý thuyết của ông giữ được logic cổ điển: mỗi câu hoặc đúng hoặc sai, và câu phủ định được hiểu theo hai cách — “có một vua Pháp và ông ta không hói” (sai) hoặc “không có chuyện một vua Pháp bị hói” (đúng) — nên luật bài trung vẫn đứng vững. Cuộc tranh luận giữa hai cách nhìn vẫn tiếp diễn trong triết học ngôn ngữ ngày nay.",
},
"quote": {
"source": "Bertrand Russell, *The Problems of Philosophy* (1912), chương VI “On Induction” — nguyên văn tiếng Anh",
"orig": "The man who has fed the chicken every day throughout its life at last wrings its neck instead, showing that more refined views as to the uniformity of nature would have been useful to the chicken.",
"vi": "Người đã cho con gà ăn mỗi ngày suốt đời nó, rốt cuộc lại vặn cổ nó, cho thấy rằng những quan niệm tinh tế hơn về tính đồng nhất của tự nhiên lẽ ra đã có ích cho con gà.",
"url": "https://www.gutenberg.org/ebooks/5827",
},
"misread": [
"**“Russell và Whitehead mất hàng trăm trang chỉ để chứng minh 1 + 1 = 2.”** Thực ra mục tiêu của *Principia Mathematica* không phải chứng minh 1 + 1 = 2 cho chắc ăn, mà cho thấy cả số học có thể dựng lên từ vài nguyên lý logic; định lý nổi tiếng ấy chỉ là một trạm nhỏ trên đường đi, nằm ở tập II.",
"**“Triết học phân tích chỉ là mổ xẻ chữ nghĩa, xa rời đời sống.”** Một trong những người sáng lập nó viết về giáo dục, hôn nhân, tôn giáo, chiến tranh, lập một trường học thực nghiệm, và là chủ tịch đầu tiên của Chiến dịch Giải trừ Vũ khí Hạt nhân (1958) ở Anh.",
],
"related": [
("doc/russell-gia-tri.md", "Giá trị của triết học — Bertrand Russell (1912)"),
("bat-dau/index.md", "Triết học là gì, và không phải là gì?"),
("cau-hoi/chan-ly.md", "Sự thật là gì?"),
("cau-hoi/tri-thuc.md", "Biết một điều nghĩa là gì?"),
("lich-su/the-ky-20.md", "Thế kỷ 20: triết học chia hai ngả"),
],
"sources": [
("Irvine, Andrew David, “Bertrand Russell”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/russell/"),
("Linsky, Bernard & Andrew David Irvine, “Principia Mathematica”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/principia-mathematica/"),
("Russell, Bertrand, *The Problems of Philosophy* (1912), Project Gutenberg.", "https://www.gutenberg.org/ebooks/5827"),
("Strawson, P. F., “On Referring”, *Mind* 59 (1950), tr. 320–344.", "https://doi.org/10.1093/mind/LIX.235.320"),
],
},
"heidegger": {
"desc": "Tác giả “Tồn tại và thời gian” (1927): tồn-tại-trong-thế-giới, hướng-tới-cái-chết, phê phán kỹ thuật — và hồ sơ gắn bó với Quốc xã cần được đọc tỉnh táo.",
"bio": [
"Martin Heidegger sinh ngày 26/9/1889 ở Messkirch, một thị trấn nông thôn miền tây nam nước Đức; cha ông là thợ đóng thùng và người giữ nhà thờ Công giáo. Tuổi thơ giữa nghề thủ công và nhịp sống nông nghiệp in dấu lên triết học của ông. Ông học thần học Công giáo rồi triết học ở Freiburg, làm trợ lý cho Husserl (1919–1923); các bài giảng của ông ở Marburg (1923–1928) thu hút sinh viên khắp nước Đức, trong đó có Hannah Arendt, Hans-Georg Gadamer, Hans Jonas.",
"*Tồn tại và thời gian* (1927), đề tặng Husserl “trong tình bạn và lòng ngưỡng mộ”, đặt lại câu hỏi mà ông cho là triết học đã lãng quên: “tồn tại” nghĩa là gì? Ta hiểu ngầm chữ “là” mỗi ngày mà hiếm khi hỏi về nó. Ông không bắt đầu từ một chủ thể đứng ngoài quan sát thế giới, mà từ *Dasein* — cách tồn tại của con người, vốn luôn đã ở giữa công việc, đồ vật, người khác, và biết mình sẽ chết. Năm 1928 ông kế nhiệm ghế giáo sư của Husserl ở Freiburg.",
"Tháng 4/1933, ít lâu sau khi Hitler lên nắm quyền, Heidegger được bầu làm hiệu trưởng Đại học Freiburg và tháng 5 gia nhập Đảng Quốc xã; trên cương vị ấy, ông lo việc “đồng bộ hóa” trường đại học theo mục tiêu của đảng. Ông từ chức sau một năm nhưng vẫn là đảng viên đến khi chế độ sụp đổ; sau chiến tranh, chính quyền quân sự Pháp cấm ông giảng dạy đến năm 1949. Năm 2014, những cuốn sổ tay ông viết từ 1931 đến 1941 — *Sổ đen* — được in, kèm những đoạn bài Do Thái làm dấy lên một làn sóng tranh luận mới. Ngày nay các sự kiện cơ bản không còn bị nghi ngờ; điều còn tranh luận là chúng thấm vào triết học của ông đến đâu.",
"Ảnh hưởng của ông lên thế kỷ 20 rất sâu rộng: Sartre, Beauvoir, Arendt, Merleau-Ponty, Gadamer, Derrida, Foucault, cả trường phái Kyoto ở Nhật Bản; ngày nay triết học về trí tuệ nhân tạo và khoa học nhận thức vẫn đọc ông. Bài giảng “Câu hỏi về kỹ thuật” (1953) — kỹ thuật hiện đại biến mọi thứ, kể cả con người, thành “nguồn dự trữ” — vẫn thường được nhắc tới khi bàn về công nghệ. Ông mất ngày 26/5/1976 ở Freiburg và được chôn ở quê nhà Messkirch.",
],
"works": [
("1927", "*Sein und Zeit*", "*Tồn tại và thời gian*: phân tích Dasein, tồn-tại-trong-thế-giới, hướng-tới-cái-chết (dở dang)"),
("1929", "*Kant und das Problem der Metaphysik*", "*Kant và vấn đề siêu hình học*; cùng năm, cuộc tranh luận với Ernst Cassirer ở Davos"),
("1950", "*Holzwege*", "*Những lối mòn trong rừng*: các bài giảng 1935–1946, có bài về nguồn gốc của tác phẩm nghệ thuật"),
("1954", "“Die Frage nach der Technik”", "“Câu hỏi về kỹ thuật” (giảng năm 1953): kỹ thuật như sự “đặt bày” (*Gestell*)"),
("2014", "*Überlegungen II–XV* (*Schwarze Hefte*)", "*Sổ đen*: sổ tay 1931–1941, in sau khi ông mất"),
],
"thoughts": [
"**Câu hỏi về tồn tại.** Khoa học hỏi cái gì tồn tại và vận hành ra sao; Heidegger hỏi điều đứng trước đó: *tồn tại* nghĩa là gì? Theo ông có nhiều *cách* tồn tại — của đồ dùng, của vật thể tự nhiên, của con người — và triết học sai khi gộp tất cả vào khuôn “vật thể có thuộc tính”.",
"**“Người ta”.** Phần lớn thời gian, ta sống theo “người ta” (*das Man*): người ta nghĩ thế, người ta làm thế. Chính những chuẩn mực chung ấy làm thế giới thường ngày dễ hiểu với ta; nhưng chúng cũng gỡ khỏi vai ta gánh nặng phải tự chọn.",
"**Hướng-tới-cái-chết.** Cái chết là khả thể riêng nhất của mỗi người: không ai chết thay ai. Đối diện với sự hữu hạn ấy — thay vì trốn vào câu chuyện của “người ta” — là mở ra khả năng sống *chân thực*, tự nhận lấy đời mình.",
"**Kỹ thuật như sự đặt bày.** Kỹ thuật hiện đại không chỉ là công cụ mà là một cách khiến mọi thứ hiện ra như nguồn dự trữ chờ khai thác: dòng sông thành nguồn thủy điện, tình bạn thành “quan hệ”, con người thành “nguồn nhân lực”.",
],
"argument": {
"title": "Cái búa và thế giới",
"intro": "Từ Descartes, triết học thường hình dung con người là một chủ thể đứng ngoài, quan sát những vật thể có thuộc tính rồi tự hỏi làm sao biết chúng có thật. *Tồn tại và thời gian* lập luận rằng hình dung ấy đặt ngược thứ tự (theo cách tái dựng phổ biến):",
"premises": [
"Trong đời sống thường ngày, ta không gặp sự vật như những khối vật chất trung tính, mà như đồ dùng “sẵn tay” trong một mạng lưới mục đích: cây bút dẫn tới tờ giấy, tờ giấy tới cái bàn, tất cả để viết một lá thư — và khi dùng thạo, ta hầu như không để ý đến chúng.",
"Ta chỉ “nhìn” một vật như đối tượng với kích thước, khối lượng khi dừng tay đứng ngoài, hoặc khi đồ dùng hỏng — cái búa gãy cán bỗng hiện ra như một khúc gỗ và một cục sắt.",
"Chế độ quan sát ấy nảy sinh khi ta rút khỏi sự tham dự thường ngày, nên không thể là điểm xuất phát để giải thích sự tham dự ấy.",
],
"conclusion": "Vậy con người trước hết là tồn-tại-trong-thế-giới, luôn đã sống giữa một mạng lưới ý nghĩa thực hành; bắt đầu từ một chủ thể cô lập rồi hỏi làm sao nó “chạm” được tới thế giới là đặt câu hỏi sai.",
"objection": "Thứ tự trong trải nghiệm chưa chắc là thứ tự của thực tại: việc ta *gặp* cái búa như đồ dùng trước khi *thấy* nó là gỗ và sắt không chứng minh rằng thực tại không phải là vật chất với các thuộc tính như vật lý mô tả. Một số nhà nghiên cứu còn cảnh báo: nếu “tồn tại” gắn với việc ta hiểu được nó, Heidegger có nguy cơ trượt về duy tâm.",
"reply": "Người bênh vực Heidegger đáp rằng ông không phủ nhận vật lý: ông chủ trương có nhiều cách tồn tại, và coi tính “sẵn tay” chỉ là lớp ý nghĩa chủ quan phủ lên những vật thể “thật ra” trung tính là một sai lầm. Điều ông bác bỏ là tham vọng dựng lại toàn bộ thế giới có ý nghĩa từ những dữ kiện trung tính — một điểm về sau vẫn được dùng trong các tranh luận về trí tuệ nhân tạo và khoa học nhận thức.",
},
"misread": [
"**“Heidegger ghét công nghệ và muốn quay về thời tiền công nghiệp.”** Thực ra mối nguy ông nói tới không phải máy móc mà là một *cách nhìn* biến mọi thứ thành nguồn dự trữ để tối ưu hóa. Nhiều nhà nghiên cứu (Dreyfus, Thomson, Wrathall) đọc ông như lời kêu gọi nuôi dưỡng những thực hành khác chứ không phải đập bỏ máy móc; còn các nhà phê bình như Andrew Feenberg cho rằng ý tưởng về “một bản chất duy nhất” của kỹ thuật quá trừu tượng và dễ dẫn tới thái độ buông xuôi.",
"**“Đọc Heidegger thì phải chọn: hoặc bỏ qua chuyện Quốc xã, hoặc vứt bỏ toàn bộ triết học của ông.”** Thực ra giới nghiên cứu trải rộng giữa hai cực: Julian Young cho rằng triết học của ông tách được khỏi chủ nghĩa Quốc xã, Emmanuel Faye cho rằng không thể. Bách khoa toàn thư Triết học Stanford đề nghị một lối đọc tỉnh táo: tư tưởng của ông vẫn nuôi dưỡng nghiên cứu ở nhiều lĩnh vực, nhưng người đọc cần tự hỏi những quan điểm dân tộc chủ nghĩa và phân biệt chủng tộc của ông đã làm méo mó cách ông hiểu lịch sử đến đâu.",
],
"related": [
("cau-hoi/cong-nghe-ai.md", "AI thay đổi con người thế nào? Triết học công nghệ"),
("cau-hoi/cai-chet.md", "Chết có đáng sợ không?"),
("lich-su/the-ky-20.md", "Thế kỷ 20: triết học chia hai ngả"),
],
"sources": [
("Wrathall, Mark, “Martin Heidegger”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/heidegger/"),
("Korab-Karpowicz, W. J., “Martin Heidegger”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/heidegge/"),
("Mitchell, Andrew J. & Peter Trawny (chủ biên), *Heidegger’s Black Notebooks: Responses to Anti-Semitism*, Columbia University Press, 2017.", "https://doi.org/10.7312/mitc18044"),
],
},
"wittgenstein": {
"desc": "Từ “Tractatus” với giới hạn của điều nói được đến “Khảo cứu triết học”: nghĩa là cách dùng, trò chơi ngôn ngữ, tương đồng gia đình, không có ngôn ngữ riêng tư.",
"bio": [
"Đầu năm 1918, Bertrand Russell giảng ở London một loạt bài mà ông nói phần lớn để trình bày “những ý tưởng tôi học được từ người bạn và học trò cũ Ludwig Wittgenstein”, và thú nhận mình không biết anh còn sống hay đã chết. Lúc ấy Wittgenstein đang ở bên kia chiến tuyến, trong quân đội Áo, và đang viết *Tractatus Logico-Philosophicus*.",
"Wittgenstein sinh ngày 26/4/1889 ở Vienna, trong một gia đình công nghiệp giàu có, giữa đời sống văn hóa sôi động của thành phố. Ông học kỹ thuật hàng không ở Manchester; mối quan tâm đến nền tảng của toán học dẫn ông tới Frege, và theo lời khuyên của Frege, năm 1911 ông đến Cambridge học với Russell. Chỉ một năm sau, Russell viết rằng ông yêu quý chàng trai ấy và tin anh sẽ giải được những vấn đề mà ông đã quá già để giải. Năm 1913, chính lời phê phán của người học trò khiến Russell bỏ dở cả một bản thảo về lý thuyết tri thức.",
"Từ tháng 11/1918, ông làm tù binh chín tháng ở Ý; *Tractatus* được in bằng tiếng Đức năm 1921, tiếng Anh năm 1922. Tin rằng mình đã giải xong các vấn đề triết học, ông cho đi phần gia sản, làm giáo viên, làm vườn, làm kiến trúc sư ở Vienna và vùng lân cận. Năm 1929 ông trở lại Cambridge và dần lật lại chính những gì mình từng viết; bản thảo *Khảo cứu triết học* hoàn tất năm 1945 nhưng ông rút lại, chỉ cho in sau khi mình mất. Ông mất vì ung thư năm 1951 ở Cambridge; tương truyền lời cuối của ông là: “Hãy nói với họ rằng tôi đã có một cuộc đời tuyệt vời.”",
"Hai cuốn sách mở ra hai lối làm triết học. Chủ nghĩa kinh nghiệm logic của Vòng Vienna mang nặng dấu ấn *Tractatus*; *Khảo cứu triết học* (1953) chuyển trọng tâm từ logic hình thức sang ngôn ngữ thường ngày, và coi triết học như một liệu pháp: gỡ những nút thắt mà chính ngôn ngữ buộc vào suy nghĩ — như ông viết, chỉ cho con ruồi lối ra khỏi cái chai bẫy ruồi.",
],
"works": [
("1921/1922", "*Tractatus Logico-Philosophicus*", "bản tiếng Đức 1921; bản song ngữ Anh–Đức của C. K. Ogden 1922"),
("1953", "*Philosophische Untersuchungen*", "*Khảo cứu triết học* (in sau khi ông mất): nghĩa là cách dùng, trò chơi ngôn ngữ, ngôn ngữ riêng tư"),
("1958", "*The Blue and Brown Books*", "*Sách Xanh và Sách Nâu*: ghi chép thời kỳ giữa, khi ông bắt đầu rời xa *Tractatus*"),
("1969", "*Über Gewißheit*", "*Về sự chắc chắn*: hoài nghi và những mệnh đề làm “bản lề” cho mọi nghi ngờ"),
],
"thoughts": [
"**Thuyết hình ảnh.** Trong *Tractatus*, một câu có nghĩa khi nó là bức tranh về một sự kiện có thể xảy ra, và đúng khi bức tranh khớp với thực tại. Những gì không phải là bức tranh như thế — đạo đức, ý nghĩa cuộc đời, cả hình thức logic — không thể *nói* ra, chỉ có thể *tự hiển lộ*.",
"**Nghĩa là cách dùng.** “Với một lớp lớn các trường hợp — dù không phải mọi trường hợp” — nghĩa của một từ là cách nó được dùng trong ngôn ngữ (*Khảo cứu triết học*, §43). Muốn hiểu “tôi hứa” hay “phạt đền”, đừng tìm một vật được chỉ; hãy nhìn việc người ta *làm* với chữ ấy.",
"**Trò chơi ngôn ngữ và tương đồng gia đình.** Ra lệnh, kể chuyện, đùa, cầu nguyện… là những trò chơi ngôn ngữ khác nhau, gắn với những hình thức sống. Nhiều khái niệm như “trò chơi” không có một bản chất chung, chỉ có những nét giống nhau đan chéo như giữa các thành viên trong một gia đình: đừng nghĩ, hãy nhìn (§66).",
],
"argument": {
"title": "Có thể có một ngôn ngữ chỉ mình ta hiểu không?",
"intro": "Từ Descartes, nhiều người coi cảm giác của ta là điều chắc chắn nhất, và chỉ ta biết. *Khảo cứu triết học* (§§243–315) thử hình dung một ngôn ngữ gọi tên những cảm giác ấy mà về nguyên tắc chỉ người nói hiểu được. Cách tái dựng phổ biến của đoạn “cuốn nhật ký” (§258):",
"premises": [
"Giả sử tôi muốn ghi nhật ký về một cảm giác lặp lại, đánh dấu nó bằng chữ “S” và “định nghĩa” S bằng cách tập trung chú ý vào cảm giác lúc nó xuất hiện.",
"Để “S” là một từ có nghĩa, phải phân biệt được giữa dùng nó đúng và chỉ *tưởng* là dùng đúng.",
"Nhưng ở đây không có gì để đối chiếu ngoài ấn tượng của chính tôi: cái gì *có vẻ* đúng thì cũng là đúng — như mua thêm vài tờ cùng số báo sáng nay để kiểm tra tin trên báo (§265).",
],
"conclusion": "Vậy không thể có một ngôn ngữ mà về nguyên tắc chỉ một người hiểu được; ngay cả từ ngữ về cảm giác cũng sống nhờ những tiêu chuẩn công cộng: hành vi, hoàn cảnh, cách dùng chung.",
"objection": "A. J. Ayer (1954) phản bác: nếu vậy thì ngôn ngữ chung cũng sụp, vì mọi sự kiểm tra công cộng rốt cuộc cũng dựa vào trí nhớ và tri giác của từng người. Và một Robinson Crusoe bị cô lập từ lúc lọt lòng vẫn có thể tự đặt tên cho cây cỏ và cảm giác của mình — sao lại không gọi đó là ngôn ngữ?",
"reply": "Nhiều nhà nghiên cứu đáp rằng lập luận không nghi ngờ trí nhớ: vấn đề là ngay từ đầu chẳng có quy tắc nào được xác lập để mà nhớ, nên “có vẻ đúng” và “đúng” không tách ra được. Crusoe cũng không phải phản ví dụ: ngôn ngữ của anh ta về nguyên tắc người khác học được, như ván cờ tự đánh với mình vẫn là cờ.",
},
"quote": {
"source": "Ludwig Wittgenstein, *Tractatus Logico-Philosophicus* (1921), mệnh đề 6.54 — bản dịch tiếng Anh của C. K. Ogden (1922)",
"orig": "My propositions are elucidatory in this way: he who understands me finally recognizes them as senseless, when he has climbed out through them, on them, over them. (He must so to speak throw away the ladder, after he has climbed up on it.)",
"vi": "Các mệnh đề của tôi làm sáng tỏ theo cách này: ai hiểu tôi thì rốt cuộc sẽ nhận ra chúng vô nghĩa, khi đã trèo ra khỏi chúng — nhờ chúng, trên chúng, vượt qua chúng. (Có thể nói, người ấy phải vứt cái thang đi sau khi đã trèo lên.)",
"url": "https://en.wikisource.org/wiki/Tractatus_Logico-Philosophicus/6",
},
"misread": [
"**“‘Điều gì không thể nói thì phải im lặng’ nghĩa là đạo đức, tôn giáo, ý nghĩa cuộc đời đều vô giá trị.”** Thực ra ngay trước câu kết ấy, *Tractatus* viết rằng dù mọi câu hỏi khoa học đã được trả lời, các vấn đề của đời sống vẫn chưa hề được chạm tới (6.52), và “quả thật có cái không thể diễn đạt; nó tự hiển lộ” (6.522).",
"**“Wittgenstein cho rằng cảm giác không có thật, hoặc ta không thể nói về chúng.”** Thực ra lập luận ngôn ngữ riêng tư không phủ nhận đau đớn hay đời sống nội tâm — ta vẫn nói về chúng hằng ngày bằng ngôn ngữ chung. Nó chỉ nhắm vào ý tưởng về một ngôn ngữ mà về nguyên tắc chỉ người nói hiểu được.",
],
"related": [
("cau-hoi/ngon-ngu.md", "Ngôn từ có định hình tư duy? Ngôn ngữ và tri thức"),
("cong-cu/dinh-nghia-phan-vi-du.md", "Thế nào là một định nghĩa tốt?"),
("cau-hoi/chan-ly.md", "Sự thật là gì?"),
("cau-hoi/nghe-thuat.md", "Cái gì làm nên nghệ thuật?"),
("lich-su/the-ky-20.md", "Thế kỷ 20: triết học chia hai ngả"),
],
"sources": [
("Biletzki, Anat & Anat Matar, “Ludwig Wittgenstein”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/wittgenstein/"),
("Candlish, Stewart & George Wrisley, “Private Language”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/private-language/"),
("Wittgenstein, Ludwig, *Tractatus Logico-Philosophicus*, C. K. Ogden dịch (1922), Wikisource.", "https://en.wikisource.org/wiki/Tractatus_Logico-Philosophicus"),
("Russell, Bertrand, “The Philosophy of Logical Atomism”, *The Monist* 28(4), 1918.", "https://archive.org/details/sim_monist_1918-10_28_4"),
("Ayer, A. J. & Rush Rhees, “Can There Be a Private Language?”, *Proc. Aristotelian Society, Supp. Vol.* 28 (1954).", "https://doi.org/10.1093/aristoteliansupp/28.1.63"),
],
},
"popper": {
"desc": "Popper hỏi điều gì làm nên khoa học và trả lời: dám đưa ra dự đoán có thể sai. Từ đó ông đi tới một triết lý về xã hội mở, nơi chính quyền cũng phải chịu phê phán.",
"bio": [
"Một thầy bói phán: “Năm nay anh có hạn, nhưng biết giữ mình thì qua.” Gặp chuyện xui, lời bói đúng; bình an vô sự, lời bói vẫn đúng, vì “anh đã biết giữ mình”. Karl Popper dành cả đời để chỉ ra chỗ khác nhau giữa kiểu lời nói ấy và khoa học. Theo lời ông kể, ngay từ mùa thu năm 1919, khi mới mười bảy tuổi, ông đã nhận ra điều sẽ thành tiêu chuẩn nổi tiếng nhất của triết học khoa học: một lý thuyết giải thích được mọi thứ thì thực ra chẳng nói gì về thế giới.",
"Popper sinh ngày 28 tháng 7 năm 1902 ở Vienna, trong một gia đình gốc Do Thái mê sách: cha là luật sư say mê triết học, mẹ truyền cho ông tình yêu âm nhạc. Năm 1919 chàng trai trẻ theo chủ nghĩa Marx một thời gian ngắn rồi sớm vỡ mộng vì tính giáo điều của nó; ông cũng nghe Einstein giảng về thuyết tương đối, và những năm 1920 làm tình nguyện với trẻ em nghèo ở một cơ sở của nhà tâm lý học Alfred Adler. Sự tương phản theo ông suốt đời: học thuyết của Marx, Freud, Adler dường như được “xác nhận” ở khắp nơi, còn Einstein dám đưa ra dự đoán mà nếu sai thì cả lý thuyết sụp đổ, như dự đoán ánh sáng bị bẻ cong khi đi gần Mặt Trời, được kiểm tra năm 1919. Ông học nghề đóng tủ, lấy bằng giáo viên, rồi đỗ tiến sĩ năm 1928 với nhà tâm lý học Karl Bühler.",
"Cuốn *Logik der Forschung* in ở Vienna mùa thu năm 1934 (trang bìa ghi 1935) trình bày có hệ thống câu trả lời của ông, tranh luận thẳng với Trường phái Vienna. Năm 1937 ông sang dạy triết học ở Canterbury University College (Christchurch, New Zealand) và ở lại đó suốt Thế chiến II. Việc Đức sáp nhập Áo năm 1938 khiến ông chuyển sang triết học chính trị: *The Open Society and Its Enemies* (1945), mà ông gọi là phần “đóng góp vào cuộc chiến” của mình, truy tìm gốc rễ triết học của chủ nghĩa toàn trị ngược về tận Platon, Hegel và Marx.",
"Năm 1946 ông về Trường Kinh tế London (LSE), từ 1949 là giáo sư logic và phương pháp khoa học của Đại học London; trong số học trò có Imre Lakatos và Paul Feyerabend, hai người về sau phê phán chính thầy mình. Ông được phong tước hiệp sĩ năm 1965, nghỉ hưu năm 1969 nhưng vẫn viết và giảng cho tới khi mất năm 1994. Bản thân Popper hay tranh cãi và khó chấp nhận phê bình nhắm vào mình, một nghịch lý ở người coi phê phán là linh hồn của lý trí. Nhưng câu hỏi ông để lại thì rất hợp với đời thường: mỗi lần đọc “theo khoa học thì…” trên mạng, hãy hỏi như Popper: kết quả nào sẽ cho thấy điều này sai?",
],
"works": [
("1934", "*Logik der Forschung*", "Logic của nghiên cứu khoa học; trang bìa ghi 1935; bản tiếng Anh mở rộng *The Logic of Scientific Discovery* (1959)"),
("1945", "*The Open Society and Its Enemies*", "Xã hội mở và những kẻ thù của nó, hai tập, viết ở New Zealand trong chiến tranh"),
("1957", "*The Poverty of Historicism*", "Sự nghèo nàn của chủ nghĩa lịch sử; đăng trên tạp chí *Economica* 1944–1945, in thành sách 1957"),
("1963", "*Conjectures and Refutations*", "Phỏng đoán và bác bỏ: tri thức khoa học lớn lên như thế nào"),
("1976", "*Unended Quest*", "Cuộc tìm kiếm chưa kết thúc: tự truyện trí tuệ"),
],
"thoughts": [
"**Khả bác bỏ** (*falsifiability*) là ranh giới giữa khoa học thực nghiệm và phi khoa học, không phải giữa có nghĩa và vô nghĩa. Một lý thuyết khoa học phải “cấm” một số điều có thể quan sát được; lý thuyết khớp với mọi kết quả thì không nói gì về thế giới, dù nó vẫn có thể gợi mở. Ông xếp phân tâm học vào loại “tiền khoa học”, còn chiêm tinh là giả khoa học.",
"Khoa học bắt đầu từ vấn đề chứ không từ quan sát thuần túy, vì mọi quan sát đều đã mang sẵn lý thuyết. Tri thức lớn lên bằng phỏng đoán táo bạo và nỗ lực bác bỏ; lý thuyết sống sót chỉ được “củng cố” (*corroborated*) tạm thời, không bao giờ được chứng minh xong. Nghịch lý thú vị: lý thuyết càng nói nhiều, tức càng khó có khả năng đúng, lại càng có giá trị khoa học, vì nó càng dễ bị kiểm tra.",
"Ông phê phán **chủ nghĩa lịch sử** (*historicism*), niềm tin rằng lịch sử có những quy luật tất yếu cho phép ta tiên tri tương lai, và truy gốc nó tới Platon, Hegel, Marx. Thay vì dựng lại cả xã hội theo một bản thiết kế không tưởng, ông đề nghị “kỹ thuật xã hội từng phần” (*piecemeal social engineering*): sửa từng chỗ, theo dõi hậu quả, sẵn sàng rút lại khi sai, như làm thí nghiệm.",
"Về dân chủ, Popper đề nghị đổi câu hỏi “Ai nên cai trị?” thành “Tổ chức thể chế thế nào để kẻ cai trị tồi hay bất tài không gây quá nhiều thiệt hại?”. Giá trị của dân chủ là cho phép thay chính quyền mà không đổ máu. Cũng trong *Xã hội mở*, ông nêu **nghịch lý khoan dung**: khoan dung vô hạn sẽ dẫn tới sự biến mất của khoan dung; nhưng ông chỉ chấp nhận đàn áp khi phía không khoan dung từ chối tranh luận bằng lý lẽ.",
],
"argument": {
"title": "Vì sao là khả bác bỏ, chứ không phải kiểm chứng?",
"intro": "Lập luận bất đối xứng trong *Logik der Forschung* (§1, §6), tái dựng gọn. Popper chấp nhận phê phán của Hume về quy nạp, nhưng không vì thế mà rơi vào hoài nghi luận:",
"premises": [
"Các quy luật khoa học là những khẳng định phổ quát, nói về vô số trường hợp: “mọi con thiên nga đều trắng”, “không có cỗ máy chuyển động vĩnh cửu”.",
"Không một số lượng quan sát hữu hạn nào chứng minh được một khẳng định phổ quát: thấy bao nhiêu thiên nga trắng cũng không suy ra hợp lệ rằng mọi thiên nga đều trắng (vấn đề quy nạp của Hume).",
"Nhưng chỉ một quan sát trái ngược, nếu được chấp nhận (“ở chỗ này có một con thiên nga đen”), là đủ để suy diễn rằng quy luật sai, theo modus tollens (phủ định hậu kiện).",
],
"conclusion": "Vậy dấu hiệu của khoa học thực nghiệm không phải là có thể được kiểm chứng, mà là có thể bị kinh nghiệm bác bỏ: lý thuyết phải chỉ ra từ trước những quan sát nào sẽ làm nó sai.",
"objection": "Kuhn, Lakatos và Putnam chỉ ra rằng một lý thuyết không bao giờ đối mặt với kinh nghiệm một mình: nó đi kèm các giả thuyết phụ và điều kiện ban đầu, nên khi dự đoán sai ta luôn có thể đổ lỗi cho giả thuyết phụ. Chẳng hạn, khi quỹ đạo sao Thiên Vương lệch khỏi tính toán, các nhà thiên văn không bỏ cơ học Newton mà đoán có một hành tinh chưa biết, và tìm ra sao Hải Vương. Lakatos còn thêm: nếu “bác bỏ” dựa trên những khẳng định cơ sở mà ta quyết định chấp nhận, ta có thể loại nhầm một lý thuyết đúng.",
"reply": "Popper đồng ý rằng trong thực hành, bác bỏ không bao giờ là chung cuộc: logic thì đơn giản, phương pháp thì phức tạp, và việc chấp nhận một khẳng định cơ sở giống phán quyết của bồi thẩm đoàn, luôn có thể xét lại. Điều ông đòi hỏi là một quy tắc phương pháp: chỉ chấp nhận giả thuyết phụ nào làm tăng chứ không làm giảm khả năng bị bác bỏ của cả hệ thống (§20). Giả thuyết “có một hành tinh chưa biết” đạt chuẩn vì nó đưa ra dự đoán mới, có thể sai, và đã đúng; những lần vá víu chỉ để né bằng chứng thì không. Các nhà phê bình đáp rằng nhượng bộ này đã làm tiêu chuẩn của ông mềm đi đáng kể.",
},
"misread": [
"**“Khả bác bỏ nghĩa là đã bị bác bỏ, tức là sai.”** Thực ra đó là một tính chất logic: lý thuyết *có thể* bị kinh nghiệm bác bỏ vì nó nói đủ rõ để có thể sai. Lý thuyết tốt nhất theo Popper là lý thuyết rất dễ bị bác bỏ mà vẫn chưa bị bác bỏ, như thuyết tương đối sau phép đo năm 1919.",
"**“Theo Popper, cái gì không khoa học là vô nghĩa và vô giá trị.”** Thực ra ông tách mình khỏi Trường phái Vienna đúng ở điểm này: tiêu chuẩn của ông vạch ranh giới giữa khoa học thực nghiệm và những hệ thống siêu hình “hoàn toàn có nghĩa”, chứ không phải giữa có nghĩa và vô nghĩa. Ông thừa nhận lý thuyết phi khoa học có thể khai sáng, thậm chí gợi ý cho khoa học về sau.",
],
"related": [
("cau-hoi/khoa-hoc.md", "Khoa học khác gì với phi khoa học? Vấn đề phân giới"),
("cau-hoi/tu-do-ngon-luan.md", "Tự do ngôn luận: được nói đến đâu?"),
("cau-hoi/dan-chu.md", "Dân chủ là gì, và vì sao nó đáng giá?"),
("cau-hoi/ai-nen-cai-tri.md", "Ai nên cai trị: số đông hay người hiểu biết?"),
],
"sources": [
("Thornton, Stephen, “Karl Popper”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/popper/"),
("Shea, Brendan, “Karl Popper: Philosophy of Science”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/pop-sci/"),
("Gorton, William, “Karl Popper: Political Philosophy”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/popp-pol/"),
("Popper, Karl, *The Logic of Scientific Discovery*, London: Routledge Classics, 2002 (bản dịch của *Logik der Forschung*, Vienna: Julius Springer, 1934; xem Lời người dịch và §1, §4, §6, §11, §20).", ""),
],
},
"sartre": {
"desc": "Sartre, gương mặt nổi tiếng nhất của thuyết hiện sinh: không có bản tính người định sẵn, ta tự làm nên mình qua lựa chọn, và không có cớ nào để viện.",
"bio": [
"Vào khoảng cuối năm 1932, đầu năm 1933, trong một quán bar ở Paris, Raymond Aron kể cho người bạn Jean-Paul Sartre về phương pháp hiện tượng học của Husserl, lấy ngay ly cocktail mơ trên bàn làm ví dụ: triết học có thể bắt đầu từ chính những thứ ta đang thấy và chạm vào. Theo Simone de Beauvoir, Sartre tái mặt vì xúc động. Đó là điều ông tìm kiếm: một triết học mô tả sự vật đúng như ta trải nghiệm chúng. Từ cuộc gặp ấy, con đường dẫn tới thuyết hiện sinh bắt đầu.",
"Sartre sinh năm 1905 ở Paris, mồ côi cha từ nhỏ và lớn lên giữa sách vở trong nhà ông bà ngoại; một bên mắt ông gần như không nhìn được. Ông học ở Trường Sư phạm Cao cấp (École Normale Supérieure), trượt kỳ thi thạc sĩ triết học lần đầu, rồi năm 1929 đỗ đầu, trên Simone de Beauvoir, người trở thành bạn đời trí tuệ suốt đời của ông. Ông dạy triết ở các trường trung học, đáng chú ý là ở Le Havre (1931–1936), và có một năm ở Viện Pháp tại Berlin để nghiên cứu Husserl. Tiểu thuyết *La Nausée* (1938) diễn tả cơn chóng mặt trước sự tồn tại trần trụi, vô cớ của mọi vật.",
"Chiến tranh làm ông đổi khác. Là lính khí tượng, ông bị quân Đức bắt năm 1940 và bị giam gần một năm; trong trại tù binh, ông còn giảng Heidegger cho bạn tù. *L'Être et le néant* (1943) ra đời giữa thời chiếm đóng. Cuối năm 1945, hàng nghìn người Paris chen chúc nghe bài giảng *L'existentialisme est un humanisme*, phiên bản dễ hiểu của cuốn sách khó ấy; cùng năm, ông cùng Beauvoir và Merleau-Ponty sáng lập tạp chí *Les Temps Modernes*. Ông viết tiểu thuyết, kịch, phê bình, và trở thành hình mẫu của người trí thức dấn thân: lên tiếng chống chính sách thực dân của Pháp, nhất là ở Algérie, rồi tìm cách nối thuyết hiện sinh với chủ nghĩa Marx trong *Critique de la raison dialectique* (1960).",
"Năm 1964 ông từ chối giải Nobel Văn học; năm 1968 ông tích cực tham gia phong trào tháng Năm. Ông mất năm 1980, và theo các ước tính, từ năm mươi nghìn đến một trăm nghìn người đã theo đám tang ông qua đường phố Paris. Sartre còn có một mối dây với Việt Nam: từ tháng 11 năm 1949 đến tháng 1 năm 1950, ông và Trần Đức Thảo ghi âm một loạt cuộc đối thoại về thuyết hiện sinh và chủ nghĩa Marx; cuộc đối thoại đổ vỡ giữa chừng. Thảo phản đối nỗ lực của Sartre muốn hòa giải hai học thuyết ấy: theo ông, Sartre không coi chủ nghĩa Marx là một triết học thực thụ.",
],
"works": [
("1938", "*La Nausée*", "Buồn nôn: tiểu thuyết triết học về sự tồn tại vô cớ"),
("1943", "*L'Être et le néant*", "Tồn tại và hư vô: tiểu luận về bản thể học hiện tượng học"),
("1946", "*L'existentialisme est un humanisme*", "Thuyết hiện sinh là một thuyết nhân bản; bài giảng cuối năm 1945"),
("1960", "*Critique de la raison dialectique*", "Phê phán lý tính biện chứng, tập I: nối thuyết hiện sinh với chủ nghĩa Marx"),
("1964", "*Les Mots*", "Những từ ngữ: tự truyện về thời thơ ấu"),
],
"thoughts": [
"**Hiện hữu có trước bản chất**: con dao rọc giấy được làm theo một ý niệm có sẵn trong đầu người thợ, nên bản chất của nó có trước sự tồn tại. Nếu không có Thượng đế nào hình dung ra con người, thì con người tồn tại trước, rồi mới tự định nghĩa mình bằng hành động: ta chẳng là gì khác ngoài điều ta tự làm nên.",
"**Bị kết án phải tự do**: ta không tự tạo ra mình, nhưng một khi đã bị ném vào đời thì phải chịu trách nhiệm về mọi điều mình làm; không chọn cũng là một lựa chọn. Khi chọn cho mình, ta đồng thời khẳng định một hình ảnh con người mà ta cho là nên có, nên chọn cho mình là chọn cho cả nhân loại. Chàng học trò phân vân giữa ở lại chăm mẹ và đi theo lực lượng Pháp Tự do không thể tìm lời giải trong một học thuyết đạo đức nào: anh phải tự đặt ra luật cho mình.",
"**Đức tin xấu** (*mauvaise foi*): tự lừa dối để trốn tránh tự do, như người bồi bàn đóng vai bồi bàn quá nhập tâm, cố biến mình thành một vật có bản chất cố định. Ta có một hoàn cảnh thật (là bồi bàn, là con của ai), nhưng không bao giờ bị thu gọn hoàn toàn vào đó.",
"**Cái nhìn** (*le regard*) của người khác: đang nhìn trộm qua lỗ khóa, chợt nghe tiếng bước chân, ta xấu hổ và nhận ra mình là một đối tượng trong mắt người khác. Với Sartre, người khác vừa là điều kiện để ta biết mình, vừa là mối đe dọa với tự do của ta.",
],
"argument": {
"title": "Hiện hữu có trước bản chất",
"intro": "Lập luận trong bài giảng *L'existentialisme est un humanisme* (1945, in năm 1946), tái dựng gọn:",
"premises": [
"Với một đồ vật được chế tạo, như con dao rọc giấy, ý niệm và công dụng của nó có trước trong đầu người thợ: bản chất có trước sự tồn tại.",
"Nếu con người có một bản tính định sẵn, thì bản tính ấy phải được một đấng sáng tạo hình dung trước, như người thợ hình dung con dao.",
"Không có Thượng đế nào để hình dung ra con người (tiền đề của thuyết hiện sinh vô thần).",
],
"conclusion": "Vậy con người không có bản tính định sẵn: ta tồn tại trước, rồi tự làm nên mình qua lựa chọn và hành động, nên chịu trách nhiệm trọn vẹn về con người mình trở thành, không có cớ nào để viện.",
"objection": "Tiền đề thứ hai bị chất vấn: người vô thần vẫn có thể nói về bản tính người dựa trên sinh học, tiến hóa và tâm lý học, tức những năng lực, nhu cầu chung của loài, mà không cần đấng sáng tạo nào. Mặt khác, quan niệm tự do triệt để của Sartre bị phê phán là không tính đến những giới hạn của hoàn cảnh: người bị áp bức, đói nghèo, bị đối xử như đồ vật có thật sự “tự do lựa chọn” như người khác không?",
"reply": "Sartre không phủ nhận những giới hạn chung: ông nói không có bản tính người nhưng có một thân phận người phổ quát, là phải sống trong thế giới, phải lao động và phải chết, và ta luôn ở trong một hoàn cảnh cụ thể. Điểm của ông là ý nghĩa của hoàn cảnh tùy vào dự phóng của ta: tự do là việc ta luôn phải lựa chọn thái độ và hành động trước hoàn cảnh, không phải quyền năng đạt được mọi thứ. Về sau, trong *Critique de la raison dialectique*, ông dành chỗ lớn hơn nhiều cho sự khan hiếm vật chất và những cấu trúc xã hội đè nặng lên tự do.",
},
"misread": [
"**“Theo Sartre, tự do nghĩa là muốn làm gì thì làm.”** Thực ra tự do của ông đi liền với trách nhiệm và nỗi lo âu: chọn cho mình là khẳng định một hình ảnh con người cho mọi người, nên không có lựa chọn nào là chuyện riêng vô hại. Ông cũng nói rõ tự do không phải là quyền năng đạt được mọi thứ ta muốn.",
"**“Thuyết hiện sinh là chủ nghĩa bi quan, tuyệt vọng.”** Thực ra bài giảng năm 1945 được viết chính để đáp lại lời buộc tội rằng thuyết hiện sinh mời gọi người ta buông xuôi trong tuyệt vọng. Sartre gọi nó là một thuyết nhân bản, vì nó đặt vận mệnh con người vào tay con người; nỗi lo âu ông nói tới là cảm giác trách nhiệm, không phải sự buông xuôi.",
],
"related": [
("doc/sartre-hien-sinh.md", "Hướng dẫn đọc Sartre: Thuyết hiện sinh là một thuyết nhân bản"),
("cau-hoi/ban-tinh-con-nguoi.md", "Bản tính con người thiện hay ác?"),
("cau-hoi/viet-hien-dai.md", "Triết học Việt Nam hiện đại, từ Nho học đến Marx và hiện sinh"),
("lich-su/the-ky-20.md", "Thế kỷ 20: triết học chia hai ngả"),
],
"sources": [
("Reynolds, Jack & Pierre-Jean Renaudie, “Jean-Paul Sartre”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/sartre/"),
("Onof, Christian J., “Sartre, Jean Paul: Existentialism”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/sartre-ex/"),
("Sartre, Jean-Paul, *Existentialism Is a Humanism* (bài giảng 1945, in 1946), bản dịch tiếng Anh của Philip Mairet, trong W. Kaufmann (biên tập), *Existentialism from Dostoevsky to Sartre*, trên Marxists Internet Archive.", "https://www.marxists.org/reference/archive/sartre/works/exist/sartre.htm"),
("The Nobel Prize in Literature 1964, NobelPrize.org.", "https://www.nobelprize.org/prizes/literature/1964/summary/"),
("O’Sullivan, Rory, “The tragedy of Trần Đức Thảo”, *Aeon*.", "https://aeon.co/essays/the-tragic-life-and-principled-politics-of-tran-duc-thao"),
],
},
"arendt": {
"desc": "Hannah Arendt hỏi điều gì đã làm chủ nghĩa toàn trị và tội ác của nó trở nên khả dĩ, và tìm câu trả lời trong hành động, tư duy và trách nhiệm của từng người.",
"bio": [
"Năm 1961, Hannah Arendt đến Jerusalem theo dõi phiên xử Adolf Eichmann, kẻ đã tổ chức việc đưa người Do Thái khắp châu Âu tới các trại hủy diệt, để viết bài cho tạp chí *The New Yorker*. Bà muốn tận mắt thấy một kẻ gây ra “cái ác triệt để” trông như thế nào. Điều bà thấy không phải quỷ dữ mà là một người nói toàn sáo ngữ, với “một sự bất lực thật sự, kỳ lạ, trong việc suy nghĩ”. Từ trải nghiệm ấy ra đời một cụm từ gây tranh cãi kéo dài: “tính tầm thường của cái ác”.",
"Arendt sinh năm 1906 ở Hannover trong một gia đình Do Thái không theo đạo, thời thơ ấu sống ở Königsberg, thành phố của Kant. Năm 1924 bà đến Marburg học với Martin Heidegger, nghe Edmund Husserl giảng một học kỳ ở Freiburg, rồi năm 1926 sang Heidelberg học với Karl Jaspers, người hướng dẫn luận án tiến sĩ của bà về khái niệm tình yêu ở Augustine (1929). Hiện tượng học của Heidegger để lại dấu ấn lâu dài trên cách bà nghĩ về “thế giới” và sự hiện diện giữa người khác; Jaspers trở thành người bạn trí tuệ suốt đời.",
"Năm 1933, khi Hitler lên nắm quyền, bà buộc phải rời Đức; qua Praha và Genève, bà sang Paris, làm việc cho các tổ chức giúp người tị nạn Do Thái. Khi chiến tranh nổ ra, bà bị giam trong trại với tư cách “ngoại kiều thù địch”, rồi năm 1941 cùng chồng là Heinrich Blücher và mẹ trốn sang Hoa Kỳ. Ở New York, bà viết *The Origins of Totalitarianism* (1951), cuốn sách sớm thành kinh điển về các chế độ Quốc xã và Stalin, rồi *The Human Condition* (1958), tác phẩm triết học quan trọng nhất của bà. Bà giảng dạy ở Princeton, Berkeley, Chicago và gắn bó lâu nhất với New School for Social Research ở New York.",
"*Eichmann in Jerusalem* (1963) gây một cuộc tranh cãi dữ dội: người ta trách giọng văn mỉa mai, trách những trang bà viết về vai trò của một số Hội đồng Do Thái, và đọc chữ “tầm thường” thành bào chữa. Bà vẫn theo đuổi câu hỏi mà phiên tòa đặt ra: nếu cái ác lớn có thể do những người không suy nghĩ gây ra, thì chính việc suy nghĩ có giúp ta tránh làm điều ác không? Câu hỏi ấy dẫn tới công trình dang dở *The Life of the Mind*; bà mất ở New York ngày 4 tháng 12 năm 1975, khi mới bắt đầu tập ba về phán đoán. Trong những bộ máy lớn hôm nay, nơi mỗi người chỉ “làm đúng quy trình”, câu hỏi của Arendt vẫn nguyên giá trị.",
],
"works": [
("1951", "*The Origins of Totalitarianism*", "Nguồn gốc của chủ nghĩa toàn trị: chủ nghĩa bài Do Thái, chủ nghĩa đế quốc và các chế độ Quốc xã, Stalin"),
("1958", "*The Human Condition*", "Thân phận con người: lao động, chế tác và hành động"),
("1963", "*Eichmann in Jerusalem: A Report on the Banality of Evil*", "Eichmann ở Jerusalem: tường thuật về tính tầm thường của cái ác"),
("1963", "*On Revolution*", "Bàn về cách mạng: so sánh cách mạng Mỹ và cách mạng Pháp"),
("1978", "*The Life of the Mind*", "Đời sống của tâm trí (tư duy, ý chí), in sau khi bà mất"),
],
"thoughts": [
"**Chủ nghĩa toàn trị** (*totalitarianism*) không chỉ là chuyên chế tàn bạo hơn mà là một hình thức cai trị mới: dùng hệ tư tưởng và khủng bố để thống trị toàn diện, biến con người thành những “bó phản ứng” có thể thay thế nhau, rốt cuộc thành “thừa thãi”. Trại tập trung là “định chế trung tâm” của nó, phòng thí nghiệm kiểm chứng niềm tin rằng “mọi thứ đều có thể”.",
"**Đời sống hoạt động** (*vita activa*) gồm ba phần: **lao động** (*labor*) để duy trì sự sống, lặp lại và tiêu hao; **chế tác** (*work*) tạo ra một thế giới đồ vật bền lâu; và **hành động** (*action*), tức lời nói và việc làm giữa những người khác. Thời hiện đại, theo bà, đánh dấu “chiến thắng của con vật lao động”: giá trị của năng suất và tiêu dùng lấn át cả sự bền lâu lẫn tự do chính trị.",
"Hành động gắn với **tính khởi sinh** (*natality*) và **tính đa nguyên** (*plurality*). Mỗi lần một con người ra đời là một khởi đầu mới, nên tự do trước hết là năng lực bắt đầu điều chưa ai lường trước. Và chính trị tồn tại vì trên trái đất có “những con người, chứ không phải Con Người”: ai cũng là người, nhưng không ai giống ai.",
"Quyền lực khác bạo lực: quyền lực nảy sinh khi nhiều người cùng hành động vì một mục đích chung và dựa trên sự đồng thuận, thuyết phục; bạo lực chỉ là công cụ cưỡng ép. Còn suy nghĩ, cuộc đối thoại thầm lặng của ta với chính mình, và phán đoán theo “lối nghĩ mở rộng” mượn từ Kant (đặt mình vào chỗ đứng của người khác) là những năng lực giúp con người không bị cuốn theo đám đông.",
],
"argument": {
"title": "Tính tầm thường của cái ác",
"intro": "Bài học bà rút ra từ phiên xử Eichmann (*Eichmann in Jerusalem*, 1963; *The Life of the Mind*), theo cách tái dựng phổ biến:",
"premises": [
"Eichmann đã tổ chức việc đưa người Do Thái khắp châu Âu tới cái chết: một tội ác khủng khiếp, mà theo bà hắn phải chịu trách nhiệm đầy đủ.",
"Thế nhưng điều lộ ra ở phiên tòa không phải lòng căm thù cuồng tín, bệnh lý hay một ác tâm sâu xa, mà là sự nông cạn: sáo ngữ, sự tận tụy với Hitler, và sự bất lực trong việc nhìn sự việc từ quan điểm của người khác.",
"Nếu một tội ác cỡ ấy có thể được thực hiện mà không cần động cơ quỷ dữ, thì cái ác không nhất thiết có “chiều sâu”: nó có thể lan ra như nấm mốc trên bề mặt.",
],
"conclusion": "Vậy cái ác cực độ không đòi hỏi kẻ ác phi thường; sự không suy nghĩ (*thoughtlessness*) cũng đủ. Vì thế năng lực suy nghĩ và phán đoán của từng người mang ý nghĩa đạo đức.",
"objection": "Nhiều nhà sử học (như David Cesarani, Deborah Lipstadt, Bettina Stangneth) cho rằng Eichmann thật là một kẻ bài Do Thái cuồng tín, và Arendt đã nhầm hắn với một viên chức bàn giấy. Nếu vậy, bà đã đọc sai chính trường hợp làm nên khái niệm của mình; và chữ “tầm thường” dễ bị hiểu thành giảm nhẹ tội ác.",
"reply": "Người bảo vệ Arendt đáp rằng bà chưa bao giờ viết Eichmann chỉ “làm theo lệnh”: bà ghi nhận hắn hăng hái, thậm chí trái lệnh cấp trên để “Giải pháp cuối cùng” thật sự cuối cùng, và bà ủng hộ bản án tử hình. Chữ “tầm thường” mô tả tính cách nông cạn của người làm, không phải mức độ của việc làm, cũng không phải một lý thuyết chung về mọi cái ác. Còn hiện tượng những người bình thường góp tay vào tội ác hành chính thì không phụ thuộc riêng vào một trường hợp.",
},
"misread": [
"**“Theo Arendt, Eichmann chỉ là một bánh răng vô can, làm theo lệnh.”** Thực ra bà bác bỏ đúng lời bào chữa ấy: theo bà, Eichmann không phải một bánh răng thụ động mà là người hăng hái đưa người Do Thái tới cái chết, phải chịu trách nhiệm đầy đủ. Cái “tầm thường” là sự nông cạn trong suy nghĩ của hắn, không phải sự nhẹ đi của tội.",
"**“‘Tính tầm thường của cái ác’ nghĩa là cái ác là chuyện vặt.”** Thực ra cụm từ chỉ xuất hiện ở tiêu đề phụ và thêm một lần trong sách, để mô tả một điều bà quan sát được ở một kẻ gây tội. Về sau bà viết cho Gershom Scholem rằng cái ác chỉ “cực độ” chứ không bao giờ “triệt để”: nó không có chiều sâu, nhưng chính vì thế có thể lan khắp thế giới như nấm mốc trên bề mặt; chỉ điều thiện mới có chiều sâu.",
],
"related": [
("cau-hoi/cai-ac.md", "Cái ác là gì?"),
("them/tu-dien.md", "Từ điển thuật ngữ"),
],
"sources": [
("Tömmel, Tatjana & Maurizio Passerin d’Entreves, “Hannah Arendt”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/arendt/"),
("Yar, Majid, “Arendt, Hannah”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/arendt/"),
("Arendt, Hannah, *The Human Condition*, Chicago: University of Chicago Press, 1958.", ""),
("Arendt, Hannah, *Eichmann in Jerusalem: A Report on the Banality of Evil*, New York: Viking Press, 1963.", ""),
],
},
"quine": {
"desc": "Triết gia Mỹ của tự nhiên luận: “Hai giáo điều của duy nghiệm luận”, mạng lưới niềm tin, tính không xác định của phép dịch và con thỏ “gavagai”.",
"bio": [
"Willard Van Orman Quine sinh ngày 25/6/1908 ở Akron, bang Ohio (Mỹ). Học toán ở Oberlin College với hướng đọc về triết học toán học, ông viết luận án tiến sĩ ở Harvard (1932) về *Principia Mathematica* của Whitehead và Russell. Về sau Quine kể rằng nhiều người như ông đã đến với nghề triết vì sách của Russell — vì sự dí dỏm và cảm giác sáng rõ mới mẻ về những nét cốt lõi của thực tại.",
"Năm 1932–1933, một học bổng đưa ông tới Vienna, Warsaw và Prague, nơi Rudolf Carnap đang giảng dạy; cuộc tranh luận với Carnap theo ông suốt đời. Ông dạy ở Harvard từ 1936 đến 1978, gián đoạn mấy năm làm tình báo hải quân Mỹ trong Thế chiến II. Bài “Hai giáo điều của duy nghiệm luận” (đọc năm 1950, in năm 1951) tấn công thẳng vào hai trụ cột của chủ nghĩa kinh nghiệm logic: phân biệt phân tích/tổng hợp, và niềm tin rằng mỗi câu có nghĩa đều quy được về những câu nói về kinh nghiệm trực tiếp; *Từ và vật* (1960) đưa ra luận đề về tính không xác định của phép dịch.",
"Quine là một nhà logic học thực thụ — viết sách giáo khoa logic, đề xuất cả một hệ lý thuyết tập hợp riêng — nhưng nổi tiếng nhất với một ý tưởng triết học: không có “triết học đầu tiên” đứng ngoài khoa học. Tri thức luận, theo ông, là “một chương của tâm lý học”: dùng chính các phương pháp của khoa học để hỏi con người đi từ những kích thích lên giác quan tới lý thuyết khoa học như thế nào.",
"Sau Quine, khó ai còn coi ranh giới giữa chân lý “do nghĩa” và chân lý “do sự kiện” là điều hiển nhiên, và triết học được nhìn như họ hàng gần của khoa học. Trớ trêu thay, hai học trò của ông là Saul Kripke và David Lewis lại trở thành những gương mặt hàng đầu của siêu hình học, theo những hướng mà chính Quine hẳn sẽ phản đối. Ông mất ngày 25/12/2000 ở Boston, thọ 92 tuổi.",
],
"works": [
("1940", "*Mathematical Logic*", "*Logic toán học*"),
("1951", "“Two Dogmas of Empiricism”", "“Hai giáo điều của duy nghiệm luận”, in lại trong *From a Logical Point of View* (1953)"),
("1960", "*Word and Object*", "*Từ và vật*: dịch thuật triệt để, “gavagai”, tính không xác định của phép dịch"),
("1969", "*Ontological Relativity and Other Essays*", "*Tính tương đối bản thể học và các tiểu luận khác*, có bài “Epistemology Naturalized”"),
("1990", "*Pursuit of Truth*", "*Truy tìm chân lý*"),
],
"thoughts": [
"**Không có ranh giới rõ giữa “đúng do nghĩa” và “đúng do sự kiện”.** Mọi cố gắng định nghĩa “phân tích” — bằng đồng nghĩa, định nghĩa, quy tắc ngữ nghĩa — đều vòng vo quay lại chính khái niệm cần định nghĩa.",
"**Mạng lưới niềm tin.** Tri thức của ta, từ địa lý, lịch sử tới vật lý, toán và logic, là “một tấm vải do con người dệt”, chỉ chạm vào kinh nghiệm ở mép. Khi một quan sát trái kỳ vọng, ta có thể sửa ở nhiều chỗ, và thường chọn chỗ gây xáo trộn ít nhất; nhưng về nguyên tắc, không mệnh đề nào miễn nhiễm với sửa đổi.",
"**Tự nhiên luận.** Không có chỗ đứng nào bên ngoài khoa học để phán xét khoa học: triết học tiếp nối khoa học, chỉ khác ở chỗ bàn những câu hỏi tổng quát và trừu tượng hơn.",
"**Tính không xác định của phép dịch.** Một nhà ngôn ngữ học nghe người bản xứ nói “gavagai” khi con thỏ chạy qua. Mọi bằng chứng hành vi đều khớp với nhiều cách dịch: “thỏ”, “giai đoạn-thỏ”, “phần không tách rời của con thỏ”… Theo Quine, không có một “nghĩa” ẩn nào để quyết định cách nào mới là đúng.",
],
"argument": {
"title": "Có câu nào đúng chỉ nhờ nghĩa của từ?",
"intro": "Các nhà thực chứng logic như Carnap dựa vào phân biệt giữa câu *phân tích* (đúng nhờ nghĩa, như “người độc thân là người chưa kết hôn”) và câu *tổng hợp* (đúng nhờ sự kiện). “Hai giáo điều của duy nghiệm luận” (1951) lập luận rằng phân biệt ấy không đứng vững:",
"premises": [
"Muốn nói một câu là phân tích, ta phải giải thích “đúng nhờ nghĩa” bằng một khái niệm khác: đồng nghĩa, định nghĩa, khả năng thay thế cho nhau mà không đổi chân trị, hay quy tắc ngữ nghĩa.",
"Xét kỹ, khái niệm nào trong số đó cũng ngầm dựa vào chính tính phân tích, hoặc vào một khái niệm chẳng rõ ràng hơn nó: ta chạy vòng tròn.",
"Lối thoát kiểu thực chứng — mỗi câu có một tập kinh nghiệm riêng xác nhận hay bác bỏ nó — cũng không ổn, vì các câu chỉ đối diện với kinh nghiệm như một khối (toàn thể luận).",
],
"conclusion": "Vậy không có ranh giới nguyên tắc giữa câu phân tích và câu tổng hợp: câu nào cũng có thể được giữ lại nếu ta điều chỉnh đủ mạnh ở chỗ khác, và không câu nào, kể cả định luật logic, miễn nhiễm với sửa đổi.",
"objection": "H. P. Grice và P. F. Strawson (“In Defense of a Dogma”, 1956) đáp: người ta áp dụng các khái niệm “đồng nghĩa”, “phân tích” khá nhất quán, nên phân biệt ấy hẳn đánh dấu một điều có thật; không định nghĩa được bằng những từ hoàn toàn khác không có nghĩa là khái niệm rỗng. Họ còn cảnh báo: hoài nghi đến cùng về “nghĩa” thì ta không giải thích nổi việc hiểu nhau.",
"reply": "Quine đáp rằng hoài nghi về “nghĩa” như những thực thể không phải là hoài nghi về việc lời nói *có nghĩa*: ta vẫn giao tiếp trôi chảy, và điều đó giải thích được bằng hành vi. Về sau ông chấp nhận một khái niệm “phân tích” khiêm tốn — một câu là phân tích với một người nếu người ấy biết câu đó đúng nhờ học cách dùng các từ trong nó, như “người độc thân thì chưa kết hôn” — nhưng khái niệm này không bao gồm toán học và không làm được việc mà Carnap cần.",
},
"misread": [
"**“Quine nói vật lý học cũng chỉ là thần thoại, như các vị thần của Homer.”** Thực ra trong “Hai giáo điều”, ông viết rằng về mặt nhận thức, vật thể vật lý và thần Homer đều là những “thứ được đặt ra” để sắp xếp kinh nghiệm; nhưng ngay sau đó ông nói mình tin vào vật thể vật lý chứ không tin thần Homer, và coi tin ngược lại là một sai lầm khoa học. “Huyền thoại” vật thể vượt trội vì nó hiệu quả hơn hẳn trong việc dự đoán kinh nghiệm.",
"**“Theo Quine, không bản dịch nào đúng, chẳng ai thật sự hiểu ai.”** Thực ra ông không nghi ngờ rằng giao tiếp và dịch thuật thành công vẫn diễn ra, được đo bằng sự trôi chảy của trao đổi; luận đề của ông là có thể có *nhiều hơn một* cách dịch đúng, và không có “ý nghĩa trong đầu” nào để phân xử giữa chúng.",
],
"related": [
("cau-hoi/ngon-ngu.md", "Ngôn từ có định hình tư duy? Ngôn ngữ và tri thức"),
("lich-su/the-ky-20.md", "Thế kỷ 20: triết học chia hai ngả"),
("cau-hoi/chan-ly.md", "Sự thật là gì?"),
],
"sources": [
("Hylton, Peter & Gary Kemp, “Willard Van Orman Quine”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/quine/"),
("Rocknak, Stefanie, “Willard Van Orman Quine: The Analytic/Synthetic Distinction”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/quine/"),
("Quine, W. V., “Two Dogmas of Empiricism”, *The Philosophical Review* 60 (1951), tr. 20–43.", "https://doi.org/10.2307/2181906"),
("Grice, H. P. & P. F. Strawson, “In Defense of a Dogma”, *The Philosophical Review* 65 (1956), tr. 141–158.", "https://doi.org/10.2307/2182828"),
],
},
"beauvoir": {
"desc": "Beauvoir hỏi: là phụ nữ có nghĩa là gì? Giới tính thứ hai (1949) mở đường cho triết học nữ quyền hiện đại và một đạo đức của tự do có tình thế.",
"bio": [
"Năm 1946, ngồi ở quán cà phê Deux Magots ở Paris, Simone de Beauvoir tự hỏi một câu tưởng như đơn giản: đối với tôi, là đàn bà có nghĩa là gì? Thoạt đầu bà nghĩ điều đó chẳng quan trọng; rồi bà nhận ra thế giới quanh mình từ trước tới nay vẫn là thế giới của đàn ông. Câu hỏi ấy thành cuốn *Le Deuxième Sexe* (1949), một trong những văn bản nữ quyền quan trọng nhất thế kỷ 20. Ở Việt Nam, nơi con gái từng được dạy “công, dung, ngôn, hạnh”, câu hỏi của bà vẫn rất gần: những nết “con gái” ấy sinh ra đã có, hay được dạy mà thành?",
"Beauvoir sinh ngày 9 tháng 1 năm 1908 ở Paris, trong một gia đình tư sản Công giáo. Năm mười bốn tuổi bà thôi tin vào Thượng đế; gia đình sa sút từ năm 1919 khiến con đường lấy chồng theo nề nếp tư sản trở nên khó khăn, và bà chọn đời sống trí thức như một cách tự lập. Bà học triết ở Sorbonne, viết luận văn về Leibniz, và năm 1929, mới hai mươi mốt tuổi, đỗ kỳ thi thạc sĩ triết học (*agrégation*) ở vị trí thứ hai, ngay sau Jean-Paul Sartre; bà là người trẻ nhất từng đỗ kỳ thi ấy tính đến lúc đó. Hai người thành bạn đời trí tuệ suốt đời: họ dựa vào nhau như những người đối thoại, và Sartre thường cần đến sự sắc sảo của bà để phát triển ý tưởng của mình.",
"Những năm 1930 bà dạy triết ở các trường trung học. Cuộc chiếm đóng của Đức Quốc xã khiến bà chú ý nhiều hơn tới đạo đức và tới cách hoàn cảnh ràng buộc tự do. Bà viết tiểu thuyết, tiểu luận triết học (*Pyrrhus et Cinéas*, 1944; *Pour une morale de l'ambiguïté*, 1947), và năm 1945 cùng Sartre, Merleau-Ponty sáng lập tạp chí *Les Temps Modernes*. Tiểu thuyết *Les Mandarins* (1954) đoạt giải Goncourt. Dù vậy bà thường tự nhận là nhà văn chứ không phải triết gia, và suốt nhiều thập kỷ bị đọc như cái bóng của Sartre; phải nhờ công trình của các nhà nghiên cứu, phần lớn là các học giả nữ quyền, bà mới được công nhận là một triết gia với những đóng góp riêng.",
"*Le Deuxième Sexe* dần biến bà thành biểu tượng của phong trào phụ nữ. Năm 1971 bà soạn và ký “Tuyên ngôn 343”, trong đó 343 phụ nữ công khai thừa nhận từng phá thai khi việc ấy còn bị cấm ở Pháp; năm 1972 bà lần đầu tự nhận mình là người theo nữ quyền. Bà còn viết *La Vieillesse* (1970), cho thấy xã hội cũng biến người già thành “kẻ khác”. Bà mất ngày 14 tháng 4 năm 1986. Mỗi khi ai đó nói “con gái thì phải thế này”, câu hỏi của Beauvoir lại hiện ra: ai quyết định chữ “phải” ấy, và vì sao?",
],
"works": [
("1944", "*Pyrrhus et Cinéas*", "Tiểu luận triết học đầu tiên: tự do, hành động và người khác"),
("1947", "*Pour une morale de l'ambiguïté*", "Vì một đạo đức của sự mơ hồ"),
("1949", "*Le Deuxième Sexe*", "Giới tính thứ hai, hai tập: tập I về sự kiện và huyền thoại, tập II về trải nghiệm sống"),
("1954", "*Les Mandarins*", "Tiểu thuyết về giới trí thức cánh tả Pháp sau Thế chiến II; giải Goncourt"),
("1970", "*La Vieillesse*", "Tuổi già: người già như “kẻ khác” của xã hội"),
],
"thoughts": [
"Phụ nữ bị định nghĩa là **Kẻ Khác** (*the Other*): đàn ông được coi là chủ thể, là chuẩn mực của “con người”, còn phụ nữ được nghĩ đến trong quan hệ với đàn ông. Bà xây khái niệm này từ biện chứng chủ–tớ của Hegel, nhưng khác Hegel ở chỗ không coi nó là phổ quát: quan hệ nam–nữ là một kiểu áp bức riêng, cần được phân tích riêng.",
"Thân thể là một **tình thế** (*situation*). Bà không phủ nhận khác biệt sinh học, nhưng cho rằng ý nghĩa của nó do xã hội và do cách mỗi người sống thân thể mình mà thành. Thử hỏi “phụ nữ là phái yếu”: yếu theo tiêu chí nào, sức cơ bắp phần thân trên hay tuổi thọ?",
"Huyền thoại “nữ tính vĩnh cửu” giam phụ nữ trong **sự nội tại** (*immanence*: lặp lại, thụ động, khép kín) thay vì **sự siêu việt** (*transcendence*: những dự phóng mở ra tương lai). Bà thẳng thắn ở một điểm khó nghe: phụ nữ thường đồng lõa với vai Kẻ Khác, vì vai ấy cũng đem lại sự công nhận và cảm giác được biện minh.",
"Từ *Pyrrhus et Cinéas* đến *Pour une morale de l'ambiguïté*, con người “mơ hồ” vì vừa tự do vừa bị ràng buộc, vừa là chủ thể vừa là đối tượng trong mắt người khác. Tự do của tôi gắn với tự do của người khác: dự phóng của tôi chỉ có tương lai khi người khác tiếp nhận nó (“lời kêu gọi”); núp sau quyền uy của người khác hay áp đặt quyền uy lên người khác đều là trốn tránh trách nhiệm của tự do.",
],
"argument": {
"title": "Người ta không sinh ra là đàn bà",
"intro": "Lập luận trung tâm của *Le Deuxième Sexe* (1949), theo cách tái dựng phổ biến:",
"premises": [
"Nếu “đàn bà”, với những nét người ta gán cho nó như dịu dàng, thụ động, sống vì người khác, là một bản chất tự nhiên, thì nó phải do sinh học quyết định và giống nhau ở mọi thời, mọi nơi.",
"Nhưng các sự kiện sinh học tự chúng không mang ý nghĩa xã hội: “yếu” hay “mạnh” tùy tiêu chí ta chọn; còn những nét “nữ tính” được hình thành qua giáo dục, huyền thoại, sự phụ thuộc kinh tế, và thay đổi theo lịch sử.",
"Theo cái nhìn hiện sinh, con người không có bản chất định sẵn, chỉ có những tình thế mà mỗi người sống và vượt qua.",
],
"conclusion": "Vậy người ta không sinh ra là đàn bà mà trở thành đàn bà: vị trí Kẻ Khác của phụ nữ là sản phẩm của lịch sử và xã hội, vừa bị áp đặt vừa được chính phụ nữ đảm nhận, nên có thể và cần được thay đổi.",
"objection": "Ý tưởng rằng khác biệt tâm lý và hành vi giữa nam và nữ có nguyên nhân sinh học chưa bao giờ biến mất. Những năm 1990, báo chí còn phổ biến giả thuyết rằng khác biệt ở thể chai (bó dây thần kinh nối hai bán cầu não) giải thích “trực giác phụ nữ” hay khả năng đọc bản đồ. Nếu một phần khác biệt có gốc sinh học, thì nói “nữ tính” hoàn toàn do xã hội nặn ra là phủ nhận dữ kiện.",
"reply": "Người theo Beauvoir đáp rằng bà không phủ nhận khác biệt giới tính: bà coi thân thể là một tình thế có thật; điều bà bác bỏ là bước nhảy từ “khác biệt” sang “số phận” và “thấp kém”. Hơn nữa, nhiều “bằng chứng” sinh học đã bị chất vấn: nhà sinh học Anne Fausto-Sterling chỉ ra thể chai rất khác nhau giữa các cá nhân, khác biệt thấy ở người lớn lại không thấy ở trẻ sơ sinh (có thể chính là kết quả của cách đối xử khác nhau), và kỹ năng không gian cải thiện được nhờ luyện tập.",
},
"quote": {
"source": "Simone de Beauvoir, *Le Deuxième Sexe*, tập II (Paris: Gallimard, 1949), phần một, chương 1 “Enfance”, câu mở đầu — trích một câu; tác phẩm còn bản quyền",
"orig": "On ne naît pas femme : on le devient.",
"vi": "Người ta không sinh ra là đàn bà: người ta trở thành đàn bà.",
"url": "https://plato.stanford.edu/entries/beauvoir/",
},
"misread": [
"**“Beauvoir chỉ diễn giải lại triết học của Sartre.”** Thực ra chính bà từng nói vậy, và vì thế bị đọc như học trò của Sartre suốt nhiều thập kỷ. Giới nghiên cứu đã cho thấy những đóng góp riêng của bà cho hiện sinh luận và hiện tượng học, như ý tưởng tự do có tình thế và phân tích thân thể được sống; hai người đối thoại và phê bình nhau, chứ không phải một người nghĩ, một người chép.",
"**“‘Người ta không sinh ra là đàn bà’ nghĩa là giới tính sinh học không có thật.”** Thực ra bà khẳng định thực tại của khác biệt giới tính và cho rằng bỏ qua nó là đi ngược hiện tượng học; điều bà phủ nhận là dùng khác biệt ấy làm lý do cho sự lệ thuộc của phụ nữ. Bà đòi bình đẳng, chứ không đòi phụ nữ phải giống đàn ông.",
],
"related": [
("cau-hoi/nu-quyen.md", "Triết học nữ quyền là gì?"),
("cau-hoi/ban-tinh-con-nguoi.md", "Bản tính con người thiện hay ác?"),
],
"sources": [
("Bergoffen, Debra & Megan Burke, “Simone de Beauvoir”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/beauvoir/"),
("Mikkola, Mari, “Feminist Perspectives on Sex and Gender”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/feminism-gender/"),
("Beauvoir, Simone de, *Le Deuxième Sexe*, 2 tập, Paris: Gallimard, 1949.", ""),
("Beauvoir, Simone de, *Pour une morale de l'ambiguïté*, Paris: Gallimard, 1947.", ""),
],
},
"rawls": {
"desc": "John Rawls hồi sinh triết học chính trị bằng một câu hỏi: nếu không biết mình sẽ là ai trong xã hội, ta sẽ chọn những nguyên tắc công lý nào?",
"bio": [
"Mẹ bảo hai anh em chia chiếc bánh: một đứa cắt, đứa kia được chọn trước. Đứa cắt bỗng trở nên rất cẩn thận, vì nó biết miếng còn lại mới là của mình. John Rawls biến trực giác ấy thành một phương pháp: hãy tưởng tượng ta chọn luật chơi cho cả xã hội mà không biết mình sẽ sinh ra giàu hay nghèo, nam hay nữ, tài giỏi hay kém may mắn. Những nguyên tắc được chọn trong hoàn cảnh công bằng ấy, theo ông, chính là những nguyên tắc công lý.",
"Rawls sinh năm 1921 ở Baltimore, Maryland; cha là một luật sư có tiếng, mẹ là chủ tịch một chi hội của Liên đoàn Cử tri Nữ. Thời sinh viên ở Princeton, ông viết một luận văn tốt nghiệp thấm đẫm tinh thần tôn giáo và từng tính chuyện học để làm linh mục. Nhưng làm lính bộ binh trong Thế chiến II, chứng kiến cái chết tùy tiện nơi chiến trường và biết tin về Holocaust, ông mất đức tin Kitô giáo. Sau chiến tranh, ông học tiếp ở Princeton, làm việc ở Oxford bên cạnh H. L. A. Hart và Isaiah Berlin, dạy ở Cornell và MIT, rồi từ năm 1962 dạy ở Harvard hơn ba mươi năm.",
"Đời ông chủ yếu diễn ra trên trang giấy, với hai ngoại lệ là hai cuộc chiến. Cuộc thứ hai là chiến tranh Việt Nam: những năm 1960, Rawls lên tiếng phản đối chế độ quân dịch vì nó phân biệt đối xử với người da đen và người nghèo, và cuộc chiến mà ông coi là bất công đã thúc ông phân tích những khiếm khuyết của nền chính trị Mỹ, cũng như câu hỏi công dân có thể phản kháng thế nào, theo tiếng gọi lương tâm, trước những chính sách hiếu chiến của chính phủ mình. Năm 1971 ông xuất bản *A Theory of Justice*, cuốn sách được coi là đã hồi sinh triết học chính trị trong truyền thống phân tích. Ba năm sau, Robert Nozick, đồng nghiệp của ông ở Harvard, đáp lại bằng *Anarchy, State, and Utopia*.",
"Phần đời còn lại, Rawls không ngừng sửa lý thuyết của mình trước phê bình. *Political Liberalism* (1993) hỏi làm sao những người theo các tôn giáo và triết lý khác nhau vẫn có thể cùng chấp nhận một luật chơi chung; *The Law of Peoples* (1999) mở rộng câu hỏi sang quan hệ giữa các dân tộc. Ông mất năm 2002. Ở Việt Nam, mỗi khi tranh luận về điểm ưu tiên tuyển sinh hay thuế thu nhập lũy tiến, người ta đang dùng ngôn ngữ của Rawls mà không biết: bất bình đẳng nào là chính đáng, nếu nhìn từ chỗ đứng của người kém may mắn nhất?",
],
"works": [
("1971", "*A Theory of Justice*", "Một lý thuyết về công lý; bản sửa 1999"),
("1993", "*Political Liberalism*", "Chủ nghĩa tự do chính trị: tính chính đáng và sự ổn định trong một xã hội đa nguyên"),
("1999", "*The Law of Peoples*", "Luật của các dân tộc: công lý trong quan hệ quốc tế"),
("2001", "*Justice as Fairness: A Restatement*", "Công lý như là sự công bằng: trình bày lại"),
],
"thoughts": [
"Đối tượng chính của công lý là **cấu trúc cơ bản** (*basic structure*) của xã hội: hiến pháp, hệ thống pháp luật, nền kinh tế, gia đình…, những thể chế định hình triển vọng của mỗi người từ lúc chào đời. Việc sinh ra giàu hay nghèo, nam hay nữ, thuộc chủng tộc nào, tài năng bẩm sinh ra sao là điều “tùy tiện về mặt đạo đức”, nên tự nó không là lý do để thể chế ưu ái ai. Trong một xã hội công bằng, công dân “đồng ý chia sẻ số phận của nhau”.",
"Hai nguyên tắc công lý: (1) mỗi người có quyền ngang nhau với một hệ thống đầy đủ các tự do cơ bản; (2) bất bình đẳng kinh tế, xã hội chỉ chấp nhận được khi gắn với những vị trí mở cho mọi người trong điều kiện bình đẳng cơ hội công bằng, và khi nó mang lại lợi ích lớn nhất cho những người kém may mắn nhất (**nguyên tắc chênh lệch**, *difference principle*). Nguyên tắc (1) được ưu tiên: không được đổi tự do cơ bản lấy tăng trưởng kinh tế.",
"**Cân bằng phản tư** (*reflective equilibrium*): đối chiếu những phán đoán ta tin chắc nhất (“chế độ nô lệ là sai”) với các nguyên tắc chung, sửa chỗ này hay chỗ kia cho tới khi chúng ăn khớp và soi sáng lẫn nhau. Với Rawls, triết học đạo đức không xuất phát từ một tiên đề bất khả nghi.",
"Trong một xã hội tự do, những người có lý trí và thiện chí vẫn sẽ bất đồng về tôn giáo, triết học, đạo đức; Rawls gọi đó là “thực tế của đa nguyên hợp lý”. Vì vậy quyền lực chính trị chỉ chính đáng khi được thực thi theo một hiến pháp mà mọi công dân tự do, bình đẳng đều có thể chấp nhận một cách hợp lý, và sự ổn định tốt nhất là một **đồng thuận gối chồng** (*overlapping consensus*): mỗi người ủng hộ cùng một quan niệm chính trị về công lý từ bên trong thế giới quan của mình.",
"Nozick phản bác rằng nguyên tắc chênh lệch là một nguyên tắc phân phối theo khuôn mẫu, đòi can thiệp liên tục vào những trao đổi tự nguyện, và coi tài năng của người giỏi như phương tiện cho người khác. Rawls đáp rằng nguyên tắc ấy không áp một khuôn mẫu quan sát được lên từng giao dịch, mà đặt sự công bằng của phân phối vào một quá trình xã hội công bằng, vận hành qua các thể chế của cấu trúc cơ bản.",
],
"argument": {
"title": "Từ bức màn vô tri đến hai nguyên tắc công lý",
"intro": "Lập luận từ **vị trí nguyên thủy** (*original position*) trong *A Theory of Justice*, ở phép so sánh đầu tiên giữa hai nguyên tắc của Rawls và chủ nghĩa vị lợi trung bình, tái dựng gọn:",
"premises": [
"Nguyên tắc công lý là những nguyên tắc mà các bên tự do và bình đẳng sẽ đồng ý trong một hoàn cảnh công bằng: sau một **bức màn vô tri** (*veil of ignorance*), không ai biết chủng tộc, giai cấp, giới tính, tài năng hay quan niệm về cuộc sống tốt của người mình đại diện.",
"Khi không có cơ sở để ước lượng xác suất, và lựa chọn lại hệ trọng, không thể làm lại, thì cách chọn hợp lý là quy tắc **maximin**: chọn phương án mà kết cục tệ nhất của nó là tốt nhất.",
"Chủ nghĩa vị lợi trung bình cho phép hy sinh tự do cơ bản của một thiểu số nếu điều đó làm tăng phúc lợi trung bình; hai nguyên tắc của Rawls thì bảo đảm tự do ngang nhau, cơ hội công bằng và một mức sống tối thiểu thỏa đáng cho mọi người.",
],
"conclusion": "Vậy các bên sẽ chọn hai nguyên tắc của Rawls chứ không chọn chủ nghĩa vị lợi; đó là nội dung của “công lý như là sự công bằng”.",
"objection": "John Harsanyi (1975) phản bác rằng maximin là quá sợ rủi ro: khi không biết mình sẽ là ai, người có lý trí nên coi khả năng rơi vào mỗi vị trí là ngang nhau và tối đa hóa giá trị kỳ vọng, và phép tính ấy dẫn thẳng tới chủ nghĩa vị lợi trung bình. Ai lại từ bỏ một xã hội tốt hơn hẳn cho số đông chỉ để phòng kịch bản xấu nhất?",
"reply": "Rawls đáp rằng các bên không được giả định là sợ rủi ro; maximin chỉ hợp lý trong hoàn cảnh đặc biệt của vị trí nguyên thủy: không có cơ sở cho xác suất, mức tối thiểu mà hai nguyên tắc bảo đảm là chấp nhận được, còn phương án kia có thể dẫn tới những kết cục không thể chấp nhận, như mất tự do tín ngưỡng. Ông thêm lập luận về “sức chịu đựng của cam kết”: không ai có thể thành tâm cam kết với những nguyên tắc mà mình có thể không chịu nổi khi bức màn được vén lên. Về sau ông nói hai điều kiện cuối mới là then chốt, và ông dùng maximin chủ yếu để bảo vệ nguyên tắc thứ nhất và bình đẳng cơ hội, chứ không phải nguyên tắc chênh lệch.",
},
"misread": [
"**“Rawls muốn chia đều mọi thứ.”** Thực ra nguyên tắc chênh lệch *cho phép* bất bình đẳng, miễn là nó mang lại lợi ích lớn nhất cho người kém may mắn nhất; và nó đứng sau quyền tự do ngang nhau cùng bình đẳng cơ hội công bằng. Chia đều chỉ là điểm xuất phát của lập luận, không phải đích đến bắt buộc.",
"**“Rawls tin rằng loài người từng thật sự ký một khế ước.”** Thực ra vị trí nguyên thủy là một thí nghiệm tư duy: nó mô hình hóa những điều kiện công bằng để lọc ra các nguyên tắc, chứ không mô tả một sự kiện lịch sử. Theo Rawls, Hobbes, Locke, Rousseau và Kant cũng đều coi khế ước xã hội là một giả định.",
],
"related": [
("cau-hoi/cong-ly.md", "Công lý là gì? Rawls và bức màn vô tri"),
("cau-hoi/binh-dang.md", "Bình đẳng nghĩa là gì: cơ hội bằng nhau hay kết quả bằng nhau?"),
("cau-hoi/khe-uoc-xa-hoi.md", "Vì sao phải vâng lời nhà nước? Khế ước xã hội"),
("cau-hoi/sieu-dao-duc.md", "Đúng sai có khách quan không?"),
],
"sources": [
("Wenar, Leif, “John Rawls”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/rawls/"),
("Freeman, Samuel, “Original Position”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/original-position/"),
("Rawls, John, *A Theory of Justice*, Cambridge, MA: Harvard University Press, 1971 (bản sửa 1999).", ""),
("Harsanyi, John C., “Can the Maximin Principle Serve as a Basis for Morality? A Critique of John Rawls’s Theory”, *American Political Science Review* 69 (2), 1975, tr. 594–606.", "https://doi.org/10.2307/1959090"),
],
},
"nozick": {
"desc": "Robert Nozick bảo vệ quyền cá nhân và nhà nước tối thiểu bằng những thí nghiệm tư duy khó quên: Wilt Chamberlain, cỗ máy trải nghiệm, lon nước cà chua đổ xuống biển.",
"bio": [
"Một triệu người tự nguyện bỏ tiền xem một ngôi sao thi đấu; cuối mùa, ngôi sao giàu hơn hẳn mọi người. Có ai bị đối xử bất công không? Câu hỏi nghe đơn giản ấy, được Robert Nozick kể bằng câu chuyện về cầu thủ bóng rổ Wilt Chamberlain, là một trong những đòn mạnh nhất từng nhắm vào các lý thuyết công lý phân phối, kể cả lý thuyết của đồng nghiệp ông ở Harvard, John Rawls.",
"Nozick sinh năm 1938 ở Brooklyn, New York, trong một gia đình di dân Do Thái gốc Nga. Ông học triết ở Đại học Columbia (tốt nghiệp năm 1959), làm luận án tiến sĩ về lý thuyết quyết định ở Princeton dưới sự hướng dẫn của Carl Hempel (1963), dạy ở Princeton, Harvard và Đại học Rockefeller, rồi về hẳn Harvard từ năm 1969. Thời trẻ, như nhiều trí thức cùng thế hệ, ông nghiêng về phong trào Cánh tả Mới và chủ nghĩa xã hội; chính việc đọc những người bênh vực chủ nghĩa tư bản như Hayek, Mises, Rothbard và Ayn Rand khiến ông đổi hướng, và chuyển mối quan tâm sang triết học chính trị.",
"Kết quả là *Anarchy, State, and Utopia* (1974), cuốn sách cùng với *A Theory of Justice* của Rawls được coi là hai tác phẩm kinh điển đã hồi sinh triết học chính trị phân tích. Nozick lập luận rằng chỉ một **nhà nước tối thiểu** (*minimal state*), bảo vệ người dân khỏi bạo lực, lừa đảo, trộm cắp và duy trì tòa án, ngoài ra không làm gì thêm, là chính đáng; mọi nhà nước rộng hơn đều vi phạm quyền cá nhân. Lạ ở chỗ sau đó ông gần như rời bỏ triết học chính trị và không bao giờ trả lời làn sóng phê bình khổng lồ nhắm vào cuốn sách.",
"Ông chuyển sang tri thức luận, siêu hình học, lý thuyết về sự hợp lý: *Philosophical Explanations* (1981), với lý thuyết tri thức như niềm tin “bám theo sự thật” và thuyết “người tiếp nối gần nhất” về bản sắc cá nhân, rồi *The Examined Life* (1989), *The Nature of Rationality* (1993), *Invariances* (2001). Ông mất năm 2002 vì ung thư dạ dày. Ở Việt Nam, mỗi khi ai đó nói “tiền tôi làm ra, nhà nước lấy bằng thuế là thiệt cho tôi”, người ấy đang nói ngôn ngữ của Nozick; và ông buộc phía bên kia phải trả lời nghiêm túc: lấy của người này cho người kia, dựa trên quyền gì?",
],
"works": [
("1974", "*Anarchy, State, and Utopia*", "Vô chính phủ, nhà nước và không tưởng: bảo vệ nhà nước tối thiểu"),
("1981", "*Philosophical Explanations*", "Những giải thích triết học: tri thức, bản sắc cá nhân, tự do ý chí"),
("1989", "*The Examined Life*", "Cuộc đời được suy xét: suy tưởng về những điều quan trọng trong đời"),
("1993", "*The Nature of Rationality*", "Bản chất của sự hợp lý"),
("2001", "*Invariances*", "Những bất biến: cấu trúc của thế giới khách quan"),
],
"thoughts": [
"Quyền là **ràng buộc bên lề** (*side constraints*), không phải mục tiêu để tối đa hóa: có những điều không được làm với một người, dù làm vậy đem lại lợi ích cho người khác. Theo Nozick, các ràng buộc ấy phản ánh “sự thật về những đời sống tách biệt” của chúng ta: không có một “thực thể xã hội” nào được lợi khi một người bị hy sinh, chỉ có những con người riêng lẻ. Ông mượn ý của Kant: con người là mục đích, không phải phương tiện.",
"**Lý thuyết quyền hưởng** (*entitlement theory*): của cải là chính đáng nếu được chiếm hữu ban đầu một cách chính đáng, chuyển nhượng tự nguyện (mua bán, tặng cho), hoặc là kết quả của việc sửa chữa một bất công trong quá khứ. Công lý nằm ở lịch sử của quá trình, không ở khuôn mẫu của kết quả; vì vậy đánh thuế thu nhập để tái phân phối, theo ông, “ngang với lao động cưỡng bức”.",
"Ông giữ “điều kiện của Locke” ở dạng nới lỏng: một sự chiếm hữu là bất chính nếu nó làm người khác tệ đi so với khi vật ấy chưa bị chiếm hữu, và ông cho rằng kinh tế thị trường thường dễ dàng thỏa điều kiện này. Ông cũng thừa nhận lịch sử sở hữu thực tế đầy giết chóc, cướp bóc, nô dịch và lừa đảo, nên nguyên tắc sửa chữa có thể đòi chuyển giao của cải, dù ông không xây dựng chi tiết lý thuyết sửa chữa ấy.",
"**Cỗ máy trải nghiệm** (*experience machine*): nếu một cỗ máy có thể cho bạn mọi trải nghiệm bạn muốn, bạn có cắm vào suốt đời không? Nozick cho rằng cắm vào là một sai lầm lớn, vì ta muốn thật sự làm những việc ấy và thật sự là một kiểu người nào đó, chứ không chỉ có cảm giác ấy; đây là một trong những phản bác nổi tiếng nhất nhắm vào thuyết khoái lạc.",
],
"argument": {
"title": "Wilt Chamberlain, hay tự do phá vỡ khuôn mẫu",
"intro": "Lập luận trong mục “How Liberty Upsets Patterns” của *Anarchy, State, and Utopia* (tr. 160–164), tái dựng gọn:",
"premises": [
"Hãy bắt đầu từ một cách phân phối D1 mà bạn cho là công bằng nhất, theo bất kỳ khuôn mẫu nào bạn thích: chia đều, theo công trạng, hay theo nguyên tắc chênh lệch.",
"Nếu D1 công bằng thì mỗi người có quyền dùng phần của mình tùy ý, miễn là không xâm phạm phần chính đáng của ai.",
"Một triệu người hâm mộ, mỗi người tự nguyện trả 25 xu để xem Wilt Chamberlain thi đấu; cuối mùa ông có thêm 250.000 đô la, và ta có phân phối D2. Không ai bị cưỡng ép, và những người đứng ngoài vẫn giữ nguyên phần của mình.",
],
"conclusion": "Vậy D2 cũng công bằng. Và vì những trao đổi tự nguyện như thế diễn ra liên tục, không khuôn mẫu phân phối nào có thể duy trì được mà không can thiệp liên tục vào đời sống của con người: tự do phá vỡ khuôn mẫu.",
"objection": "Nhiều người cho rằng Nozick đã giả định điều cần chứng minh: theo lý thuyết khuôn mẫu, quyền sở hữu ở D1 chưa bao giờ là tuyệt đối mà ngay từ đầu đã đi kèm thuế và luật lệ ai cũng biết trước. Bản thân Rawls (*Political Liberalism*, tr. 282–283) đáp rằng nguyên tắc chênh lệch không áp một khuôn mẫu quan sát được lên phân phối, mà đặt sự công bằng của phân phối vào một quá trình xã hội công bằng, vận hành qua các thể chế của cấu trúc cơ bản, chứ không nhắm vào từng giao dịch như vụ mua vé.",
"reply": "Người theo Nozick đáp rằng vấn đề nằm ngay bên trong mọi lý thuyết khuôn mẫu: nếu D1 công bằng và mỗi bước từ D1 sang D2 đều không bất công, thì cần giải thích bất công đã len vào D2 từ đâu, và người thứ ba lấy đâu ra quyền đòi một phần của món tiền vừa được trao tay. Trao cho người ta phần của họ rồi lại giành quyền can thiệp vào cách họ dùng nó là, theo câu nói của Hillel Steiner, “tạo ra quyền để can thiệp vào chính những quyền mình vừa tạo ra”.",
},
"misread": [
"**“Theo Nozick, ai xứng đáng thì được hưởng.”** Thực ra phân phối theo công trạng chính là một nguyên tắc khuôn mẫu mà ông bác bỏ. Câu hỏi của ông không phải “ai xứng đáng” mà “ai có quyền hưởng, nhờ một chuỗi chiếm hữu và chuyển nhượng chính đáng”: người được tặng quà có quyền hưởng món quà dù không “xứng đáng” hơn ai.",
"**“Về sau Nozick đã chối bỏ chủ nghĩa tự do cá nhân.”** Điều này phóng đại. Trong *The Examined Life* (1989), ông có vẻ rút lại một số điểm của *Anarchy, State, and Utopia*; nhưng trong một cuộc phỏng vấn năm 2001, ông nói tin đồn về sự “bỏ đạo” của mình “bị phóng đại nhiều”, và vẫn tự đặt mình trong khuôn khổ chung của chủ nghĩa tự do cá nhân.",
],
"related": [
("cau-hoi/cong-ly.md", "Công lý là gì? Rawls và bức màn vô tri"),
("cau-hoi/tai-san-rieng.md", "Tài sản riêng có chính đáng không?"),
("cau-hoi/hanh-phuc.md", "Hạnh phúc là gì?"),
],
"sources": [
("Mack, Eric, “Robert Nozick’s Political Philosophy”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/nozick-political/"),
("Feser, Edward, “Nozick, Robert”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/nozick/"),
("Freeman, Samuel, “Original Position”, *Stanford Encyclopedia of Philosophy* (phản bác của Nozick và lời đáp của Rawls).", "https://plato.stanford.edu/entries/original-position/"),
("Crisp, Roger, “Well-Being”, *Stanford Encyclopedia of Philosophy* (về cỗ máy trải nghiệm).", "https://plato.stanford.edu/entries/well-being/"),
("Nozick, Robert, *Anarchy, State, and Utopia*, New York: Basic Books, 1974.", ""),
],
},
"parfit": {
"desc": "Parfit dùng những thí nghiệm tư duy kỳ lạ, như máy dịch chuyển hay bộ não bị chia đôi, để hỏi điều gì thật sự quan trọng khi ta sống sót, và ta nợ gì thế hệ chưa sinh.",
"bio": [
"Bạn bước vào một buồng dịch chuyển. Máy ghi lại vị trí từng tế bào, phá hủy cơ thể bạn, rồi dựng lại một người giống hệt ở nơi khác, từ Trái Đất lên sao Hỏa hay, cho gần hơn, từ Hà Nội vào TP.HCM, với đầy đủ ký ức và tính cách của bạn. Người bước ra là bạn, hay chỉ là một bản sao vừa ra đời? Derek Parfit dùng những thí nghiệm tư duy như thế để đi tới một kết luận gây sốc: câu hỏi “có phải vẫn là tôi không” có thể không quan trọng như ta tưởng.",
"Parfit sinh ngày 11 tháng 12 năm 1942 ở Thành Đô, Tứ Xuyên (Trung Quốc), nơi cha mẹ ông, đều là bác sĩ, làm việc trong một phái đoàn truyền giáo y tế; năm 1945 gia đình về Anh. Ông học ở Eton, rồi học sử ở Balliol College, Oxford. Hai năm học bổng Harkness ở Columbia và Harvard (1964–1966) khiến ông đổi hẳn sang triết học. Năm 1967 ông được bầu vào All Souls College ở Oxford và gắn bó với nơi này suốt đời, dù chưa bao giờ lấy bằng sau đại học về triết học: bài báo đầu tay “Personal Identity” (1971) đã đủ đưa ông lên tầm quốc tế.",
"Cuốn sách đầu tiên ra đời dưới áp lực: All Souls cảnh báo rằng nếu đến năm 1984 không có một cuốn sách đủ tầm, ông sẽ mất chỗ. Kết quả là *Reasons and Persons* (1984), một trong những tác phẩm đạo đức học có ảnh hưởng nhất của nửa sau thế kỷ 20, đi từ lý trí và thời gian, bản sắc cá nhân, đến nghĩa vụ với các thế hệ tương lai. Ông viết rằng việc nhận ra bản sắc của mình chỉ là chuyện mức độ, chứ không phải một sự thật sâu xa, khiến ông thấy được giải phóng và an ủi: bớt bận tâm về tương lai và cái chết của chính mình, quan tâm nhiều hơn đến người khác.",
"Về sau ông dạy thêm ở Harvard, Đại học New York và Rutgers, một phần, theo lời ông, để có tiền cho thú chụp ảnh kiến trúc Venice và St Petersburg, rồi để có thêm tiền làm từ thiện. Công trình cuối đời, *On What Matters* (hai tập năm 2011, tập ba năm 2017), bảo vệ niềm tin rằng có những điều thật sự quan trọng. Ông được trao giải Rolf Schock năm 2014 và mất đột ngột ở London ngày 2 tháng 1 năm 2017, chỉ vài giờ sau khi gửi đi bài viết cuối cùng, một lần nữa về những người chưa sinh ra.",
],
"works": [
("1971", "“Personal Identity”", "Bài báo trên *Philosophical Review*: điều quan trọng trong sự sống sót không phải là bản sắc"),
("1984", "*Reasons and Persons*", "Lý lẽ và con người: lý trí, thời gian, bản sắc cá nhân và các thế hệ tương lai"),
("1995", "“Equality or Priority?”", "Bình đẳng hay ưu tiên? Nền móng của thuyết ưu tiên (*prioritarianism*)"),
("2011/2017", "*On What Matters*", "Về những điều quan trọng, ba tập: hiện thực luận về lý lẽ và sự hội tụ của các học thuyết đạo đức"),
],
"thoughts": [
"**Quan điểm quy giản** (*reductionist view*) về con người: sự tồn tại của một người chỉ gồm sự tồn tại của một bộ não, một thân thể và một chuỗi sự kiện tâm lý, thể chất liên kết với nhau; không có thêm một “sự kiện bổ sung” nào như một cái tôi hay linh hồn tách biệt. Ở Phụ lục J của *Reasons and Persons*, ông trích kinh điển Phật giáo (*Thanh tịnh đạo*, ví dụ cỗ xe) và viết rằng Đức Phật hẳn sẽ đồng ý.",
"**Vấn đề non-identity** (*non-identity problem*): chính sách hôm nay quyết định cả việc *ai* sẽ ra đời. Nếu một cộng đồng chọn khai thác cạn kiệt tài nguyên, người sống trong hai thế kỷ tới sẽ khá hơn đôi chút, nhưng sau đó chất lượng sống sụt mạnh; thế mà nếu chọn khác, chính những người chịu thiệt kia đã không tồn tại. Vậy lựa chọn ấy đã làm hại ai? Câu đố này nằm ở trung tâm tranh luận về trách nhiệm với khí hậu và thế hệ tương lai.",
"**Kết luận ghê tởm** (*Repugnant Conclusion*): theo một số lý thuyết hấp dẫn, với bất kỳ dân số mười tỷ người có chất lượng sống rất cao nào, sẽ có một dân số lớn hơn nhiều, mà đời ai cũng chỉ “vừa đủ đáng sống”, lại tốt hơn. Parfit thấy kết luận ấy không thể chấp nhận và dành nhiều năm tìm một lý thuyết tránh được nó; đến nay vẫn chưa có lời giải được đồng thuận.",
"Trong *On What Matters*, Parfit bảo vệ một hiện thực luận không khoan nhượng: có những lý lẽ khách quan, có những điều thật sự quan trọng bất kể ta muốn gì. Ông còn lập luận rằng các phiên bản tốt nhất của đạo đức học Kant, của khế ước luận và của hệ quả luận rốt cuộc hội tụ, như những người leo cùng một ngọn núi từ những sườn khác nhau.",
],
"argument": {
"title": "Ca phân đôi và điều thật sự quan trọng",
"intro": "Lập luận từ trường hợp “phân đôi” (*fission*) trong *Reasons and Persons*, Phần Ba, tái dựng gọn:",
"premises": [
"Người ta có thể sống sót khi chỉ còn một bán cầu não hoạt động: y học từng cắt bỏ cả một bán cầu não để chữa động kinh nặng, và người bệnh vẫn là chính họ.",
"Hãy tưởng tượng hai bán cầu não của tôi được ghép vào hai cơ thể khác nhau. Mỗi người tỉnh dậy đều liên tục về tâm lý với tôi (ký ức, tính cách, dự định) đầy đủ như khi chỉ một nửa được ghép.",
"Tôi không thể là cả hai người, vì họ sẽ sống hai cuộc đời khác nhau, và cũng không có lý do gì để là người này mà không phải người kia; vậy nói chặt chẽ, tôi không đồng nhất với ai trong hai người.",
"Nhưng quan hệ giữa tôi và mỗi người ấy chứa mọi thứ có trong sự sống sót bình thường; khó mà coi một thành công gấp đôi là một thất bại.",
],
"conclusion": "Vậy bản sắc không phải điều quan trọng trong sự sống sót; điều quan trọng là sự liên kết và liên tục tâm lý mà Parfit gọi là Quan hệ R.",
"objection": "Kết luận này đi ngược nỗi lo sâu xa nhất của ta: nghĩ đến cơn đau sắp tới của chính mình khác hẳn nghĩ đến cơn đau của một người giống hệt mình. Bernard Williams (1970) dựng những tình huống cho thấy trực giác ấy rất mạnh, và một số triết gia (như Ernest Sosa, Trenton Merricks) bảo vệ rằng bản sắc tự nó quan trọng. Hơn nữa, quan điểm này hàm ý: giữ lại một nửa bộ não thì tôi sống, giữ cả hai nửa thì tôi chết; một hệ quả khó tin.",
"reply": "Parfit chấp nhận hệ quả ấy và cho rằng chính nó cho thấy bản sắc không đáng để ta bám vào: chuyện có một hay hai người tiếp nối không thể là chuyện sống hay chết. Trực giác ngược lại, theo ông, dựa trên niềm tin vào một cái tôi tách biệt, một “sự kiện bổ sung” mà quan điểm quy giản phủ nhận. Ông thừa nhận rất khó tin trọn quan điểm này; nhưng cũng như Đức Phật, ông cho rằng tin được là điều có thể.",
},
"misread": [
"**“Parfit cho rằng con người không tồn tại, cái tôi chỉ là ảo tưởng.”** Thực ra ông viết rằng con người có tồn tại; chỉ là sự tồn tại ấy gồm những sự kiện cụ thể hơn về não, thân và các sự kiện tâm lý liên kết, nên về nguyên tắc có thể mô tả trọn thực tại mà không cần nói tới “con người”. Điều ông phủ nhận là một cái tôi tách biệt, tồn tại thêm ngoài những sự kiện ấy.",
"**“Vấn đề non-identity cho thấy ta chẳng nợ gì thế hệ tương lai.”** Parfit không rút ra kết luận ấy. Với ông, câu đố cho thấy nguyên tắc đạo đức ta cần tìm (ông gọi là “Lý thuyết X”) không thể chỉ dựa vào câu hỏi “có làm ai tệ đi không”; cái khó là những lý thuyết thay thế lại dễ vấp phải kết luận ghê tởm.",
],
"related": [
("cau-hoi/cai-toi.md", "Cái “tôi” là gì? Bạn của mười năm trước có còn là bạn?"),
("cau-hoi/ban-nga-thoi-gian.md", "Cái tôi qua thời gian — tôi của mười năm trước còn là tôi không?"),
("cau-hoi/khi-hau-trach-nhiem.md", "Ai chịu trách nhiệm cho khí hậu? Công lý liên thế hệ"),
("cau-hoi/hanh-phuc.md", "Hạnh phúc là gì?"),
("cau-hoi/sieu-dao-duc.md", "Đúng sai có khách quan không?"),
],
"sources": [
("Olson, Eric T., “Personal Identity”, *Stanford Encyclopedia of Philosophy* (SEP chưa có mục riêng về Parfit).", "https://plato.stanford.edu/entries/identity-personal/"),
("Dancy, Jonathan, “Derek Antony Parfit, 11 December 1942 – 2 January 2017”, *Biographical Memoirs of Fellows of the British Academy* XIX (2020), tr. 37–57.", "https://www.thebritishacademy.ac.uk/documents/890/19-Memoirs-03-Parfit.pdf"),
("Roberts, M. A., “The Nonidentity Problem”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/nonidentity-problem/"),
("Arrhenius, Gustaf, Jesper Ryberg & Torbjörn Tännsjö, “The Repugnant Conclusion”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/repugnant-conclusion/"),
("Donegan, Peter, “Was The Buddha a Reductionist About The Self?”, *Philosophical Readings* XII.3 (2020), tr. 376–389.", "https://open.unive.it/ojs/index.php/pr/article/view/98"),
("Parfit, Derek, *Reasons and Persons*, Oxford: Clarendon Press, 1984.", ""),
],
},
"lao-tu": {
"desc": "Lão Tử, nhân vật nửa huyền thoại gắn với Đạo đức kinh: Đạo không thể gọi tên, vô vi, mềm thắng cứng, và lời cảnh báo về chính quyền can thiệp quá tay.",
"bio": [
"Tương truyền, thấy nhà Chu suy, một viên quan giữ kho sách bỏ kinh đô ra đi. Đến cửa ải, viên quan coi ải là Doãn Hỉ nài: ngài sắp đi ẩn rồi, xin gắng viết cho tôi một cuốn sách. Ông viết hai thiên, hơn năm nghìn chữ bàn về đạo và đức, rồi đi, “không ai biết ông đi đâu”. Đó là câu chuyện Tư Mã Thiên chép trong *Sử ký* khoảng năm 100 TCN, và gần như là tất cả những gì truyền thống biết về Lão Tử.",
"Theo *Sử ký*, ông họ Lý tên Nhĩ, tên chữ là Đam, người nước Sở, làm quan giữ kho sách nhà Chu. Khổng Tử từng đến hỏi ông về lễ, ra về bảo học trò: chim ta biết nó bay, cá ta biết nó bơi, còn rồng thì không biết nó cưỡi mây gió lên trời thế nào; “hôm nay ta gặp Lão Tử, ông ấy như rồng vậy!” Nhưng chính Tư Mã Thiên cũng không chắc: ông chép thêm rằng có người cho Lão Tử là Lão Lai Tử, có người cho là quan thái sử Đam, có người bảo ông sống hơn một trăm sáu mươi tuổi, rồi kết luận đời không ai biết đúng sai. Học giới hiện đại vẫn chia rẽ: có người tin có một Lão Đam thật, lớn tuổi hơn Khổng Tử; có người cho ông hoàn toàn là truyền thuyết (Chan, SEP).",
"Cuốn sách thì có thật, và ngày càng cổ hơn người ta tưởng. Cuối năm 1993, một ngôi mộ nước Sở ở Quách Điếm (Hồ Bắc), niên đại khoảng năm 300 TCN, cho ra những thẻ tre chép khoảng hai nghìn chữ trùng với *Lão Tử*, chừng hai phần năm bản hiện hành; năm 1973, Mã Vương Đôi (Hồ Nam) đã cho hai bản chép trên lụa từ trước năm 168 TCN. Nhiều học giả nay cho rằng những tập lời nói gắn với tên Lão Tử được chép từ thế kỷ 5 TCN, gom dần lại, đến giữa thế kỷ 3 TCN mới tương đối ổn định: *Đạo đức kinh* có thể là kết tinh của nhiều thế hệ hơn là của một người.",
"Năm nghìn chữ ấy đi rất xa. Nó để lại dấu ấn trong sách *Trang Tử*, được Hàn Phi chú giải, thành kinh điển của Đạo giáo, nơi Lão Tử được tôn làm thần; nhà Đường còn nhận ông là tổ tiên dòng họ Lý của mình. Theo một thống kê năm 2022 mà SEP dẫn, sách đã có hơn hai nghìn bản dịch. Người Việt vẫn nói “biết đủ” (tri túc) hay “hành trình nghìn dặm bắt đầu từ một bước chân” mà ít khi nghĩ rằng mình đang trích *Lão Tử*.",
],
"works": [
("k. TK 4–3 TCN", "*Lão Tử*, sau gọi là *Đạo đức kinh* (道德經)", "Khoảng năm nghìn chữ, 81 chương trong bản lưu hành; truyền thống cho là của Lão Tử, nhiều học giả cho là kết tinh qua nhiều thế hệ"),
("k. 300 TCN", "Thẻ tre Quách Điếm (郭店楚簡)", "Bản cổ nhất được biết, khoảng 2.000 chữ chia ba nhóm; khai quật năm 1993"),
("trước 168 TCN", "Bản lụa Mã Vương Đôi (馬王堆帛書)", "Hai bản chép tay trên lụa, khai quật năm 1973"),
("TK 3", "Vương Bật (王弼, 226–249), chú giải *Lão Tử*", "Một trong hai dòng văn bản lưu hành chính trước các phát hiện khảo cổ"),
],
"thoughts": [
"**Đạo không thể gọi tên.** “Đạo nói ra được thì không phải Đạo thường hằng; tên gọi được thì không phải tên thường hằng” (chương 1). Đạo vừa là cội nguồn vừa là cách vận hành của muôn vật, nhưng mọi khái niệm đều cắt nó ra từng mảnh; người hiểu Đạo vì thế dè dặt với chữ nghĩa.",
"**Vô vi (無為) và tự nhiên (自然).** Vô vi không phải ngồi yên, mà là làm mà không cưỡng ép, để mọi vật tự thành theo tính của nó: người theo đất, đất theo trời, trời theo Đạo, Đạo theo tự nhiên (chương 25). Trị nước lớn như nấu cá nhỏ (chương 60): vẫn phải nấu, nhưng đừng đảo lia lịa kẻo nát.",
"**Mềm thắng cứng, rỗng mà dùng được.** Trong thiên hạ không gì mềm yếu hơn nước, mà công phá cái cứng mạnh thì không gì hơn nó (chương 78). Ba mươi nan hoa chung một trục, nhờ khoảng rỗng ở giữa mà xe mới dùng được; cái bình, căn phòng cũng vậy (chương 11).",
"**Đảo ngược điều hiển nhiên.** “Đạo lớn bị bỏ thì mới có nhân nghĩa” (chương 18): khi người ta phải rao giảng nhân nghĩa, ấy là vì nó đã mất. Lão Tử hay lật ngược cái ta cho là đương nhiên (“trở lại là sự vận động của Đạo”, chương 40), một bài tập tư duy vẫn hữu ích: cái ta tưởng là thuốc chữa có khi lại là triệu chứng.",
],
"argument": {
"title": "Càng nhiều lệnh cấm, dân càng nghèo (chương 57)",
"intro": "Hiếm khi *Đạo đức kinh* lập luận lộ liễu, nhưng chương 57 thì có. Sau lời khuyên “lấy vô sự mà giữ thiên hạ”, văn bản hỏi: “Ta lấy gì mà biết được như vậy?” rồi đưa ra bằng chứng. Đoạn này có mặt cả trong bản thẻ tre Quách Điếm.",
"premises": [
"Thiên hạ càng nhiều điều cấm kỵ thì dân càng nghèo; người càng nhiều mánh khéo thì vật lạ càng sinh; pháp lệnh càng chồng chất thì trộm cướp càng nhiều.",
"Vậy can thiệp của người cầm quyền thường sinh ra chính cái loạn mà nó muốn dẹp.",
"Khi không bị quấy nhiễu, dân có khả năng tự chuyển hóa, tự ngay ngắn, tự làm giàu.",
],
"conclusion": "Người cai trị khôn ngoan nên vô vi: “ta vô vi mà dân tự hóa, ta thích tĩnh mà dân tự chính, ta vô sự mà dân tự giàu, ta không ham muốn mà dân tự chất phác”.",
"objection": "Tương quan chưa phải nhân quả: có thể luật lệ nhiều lên chính vì trộm cướp đã nhiều, chứ không phải ngược lại. Hàn Phi, người từng chú giải Lão Tử, đọc cùng thực tế ấy theo chiều khác: người đông mà của ít thì dân tranh nhau, nên phải thưởng phạt nghiêm (thiên “Ngũ đố”). Và tiền đề thứ ba giả định bản tính con người vốn chất phác, điều Tuân Tử bác bỏ.",
"reply": "Người theo Lão Tử có thể nhận rằng ở đây có một vòng luẩn quẩn: trộm nhiều thì luật nhiều, luật nhiều thì người ta tìm cách lách, rồi lại sinh luật mới. Muốn thoát vòng ấy phải bớt chứ không thể cứ thêm. Vô vi cũng không phải vô chính phủ: vẫn nấu cá, chỉ là đừng đảo liên tục. Ai từng thấy một thủ tục rườm rà đẻ ra cả nghề “dịch vụ làm hộ” sẽ hiểu vì sao lời cảnh báo này còn được nhắc.",
},
"quote": {
"source": "*Đạo đức kinh*, chương 64 — nguyên văn chữ Hán theo bản lưu hành (ctext.org) và phiên âm Hán Việt",
"orig": "合抱之木，生於毫末；九層之臺，起於累土；千里之行，始於足下。 — Hợp bão chi mộc, sinh ư hào mạt; cửu tằng chi đài, khởi ư lũy thổ; thiên lý chi hành, thủy ư túc hạ.",
"vi": "Cây to một vòng tay ôm mọc lên từ mầm nhỏ như sợi lông; đài cao chín tầng dựng lên từ từng sọt đất; đường xa nghìn dặm bắt đầu từ chỗ đặt chân.",
"url": "https://ctext.org/dao-de-jing/zh",
},
"misread": [
"**“Vô vi là không làm gì cả.”** Thực ra *Đạo đức kinh* nói “vô vi mà không gì không làm” (chương 37). Vô vi là không cưỡng ép, không làm quá tay: “làm thì hỏng, nắm thì mất” (chương 64), như người nấu cá nhỏ biết để yên cho cá chín.",
"**“Lão Tử sáng lập Đạo giáo, tôn giáo thờ thần tiên.”** Thực ra cần phân biệt Đạo gia, một dòng tư tưởng, với Đạo giáo, một tôn giáo có tổ chức xuất hiện từ thế kỷ 2 (phái Thiên Sư), trong đó Lão Tử được tôn làm thần (Chan, SEP). Hai dòng đan vào nhau, nhưng *Đạo đức kinh* có trước tôn giáo ấy hàng mấy thế kỷ.",
],
"related": [
("doc/dao-duc-kinh.md", "Hướng dẫn đọc Đạo đức kinh"),
("lich-su/trung-hoa.md", "Trung Hoa: trăm nhà đua tiếng"),
("doc/tam-kinh.md", "Hướng dẫn đọc Bát nhã Tâm kinh"),
],
"sources": [
("Chan, Alan, “Laozi”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/laozi/"),
("*Đạo đức kinh* (道德經), nguyên văn chữ Hán kèm bản dịch tiếng Anh của James Legge, ctext.org.", "https://ctext.org/dao-de-jing"),
("Tư Mã Thiên, *Sử ký*, “Lão Tử Hàn Phi liệt truyện” (老子韓非列傳), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/shiji/lao-zi-han-fei-lie-zhuan/zh"),
],
},
"khong-tu": {
"desc": "Khổng Tử, người thầy cuối thời Xuân Thu: nhân, lễ, chính danh và lý tưởng người quân tử, nền móng của Nho giáo suốt hơn hai nghìn năm ở Đông Á.",
"bio": [
"Có lần lạc mất học trò ở nước Trịnh, Khổng Tử đứng một mình ở cổng thành phía đông. Một người qua đường tả ông với Tử Cống: trán giống vua Nghiêu, vai giống Tử Sản, nhưng dáng vẻ thất thểu “như con chó nhà có tang”. Nghe kể lại, ông vui vẻ cười: hình dáng là chuyện ngọn, còn bảo ta giống con chó nhà có tang thì “đúng thế, đúng thế!” Đó chỉ là giai thoại Tư Mã Thiên chép lại ba thế kỷ sau, nhưng nó vẽ đúng nửa sau cuộc đời ông: một người thầy đi qua nhiều nước tìm một ông vua chịu nghe mình, và không tìm được.",
"Ông tên Khâu, tên chữ là Trọng Ni, theo truyền thống sinh năm 551 TCN ở nước Lỗ (nay thuộc Sơn Đông). Cha mất khi ông còn nhỏ, nhà nghèo nhưng vẫn có chút địa vị. Về sau ông tự nhận: “thuở nhỏ ta hèn mọn, nên biết làm nhiều việc tầm thường” (*Luận ngữ* 9.6). Ông từng coi kho lúa, coi bãi chăn nuôi; theo *Tả truyện*, có lúc làm tới chức tư khấu, coi việc hình án nước Lỗ. Rời Lỗ, ông qua Vệ, Tống, Trần, Thái, Sở, cuối đời trở về dạy học và mất năm 479 TCN, thọ 73 tuổi. Tư Mã Thiên chép ông có chừng ba nghìn học trò.",
"Câu hỏi của ông rất thực tế: khi nhà Chu suy, lễ nhạc đổ nát, chư hầu đánh nhau, làm sao dựng lại một xã hội tử tế mà không cần đến roi vọt? Câu trả lời bắt đầu từ chính mỗi người: học, sửa mình, giữ lễ, thương người; người cầm quyền phải làm gương trước. Câu “tam thập nhi lập” mà người Việt hay nhắc là một dòng trong bản tự thuật sáu câu của ông (2.4): mười lăm tuổi dốc chí vào học, ba mươi đứng vững, bốn mươi không còn nghi hoặc, năm mươi biết mệnh trời, sáu mươi nghe gì cũng thuận tai, bảy mươi theo lòng muốn mà không vượt khuôn phép.",
"Lời ông đến với ta chủ yếu qua *Luận ngữ*, theo truyền thống do học trò và học trò của học trò biên soạn; nhiều học giả nay cho rằng sách chỉ lưu hành rộng từ thế kỷ 1 TCN (Csikszentmihalyi, SEP). Từ khi Chu Hy đưa *Luận ngữ* vào bộ *Tứ thư* ở thế kỷ 12, tư tưởng của ông định hình việc học, khoa cử và nếp gia đình ở Trung Hoa, Triều Tiên, Nhật Bản và Việt Nam. Ngày nay, ở một số nơi tại châu Á, ngày sinh của ông là Ngày Nhà giáo.",
],
"works": [
("TK 5–1 TCN", "*Luận ngữ* (論語)", "Lời Khổng Tử và học trò, 20 thiên, do các thế hệ học trò biên soạn"),
("thời Hán", "*Lễ ký* (禮記)", "Tuyển tập về lễ, chép thêm nhiều cuộc đối đáp của Khổng Tử ngoài *Luận ngữ*"),
("truyền thống gán cho ông", "*Xuân Thu* (春秋)", "Biên niên sử nước Lỗ; từ Mạnh Tử (3B9), truyền thống cho là do ông soạn"),
],
"thoughts": [
"**Nhân và lễ.** Nhân (仁) là thương người (12.22); lễ (禮) là khuôn phép, nghi thức của đời sống chung. Ông buộc hai thứ vào nhau: vượt lên chính mình để trở về với lễ, ấy là nhân (12.1). Lễ không có lòng thành chỉ là diễn kịch; lòng tốt không có hình thức để bày tỏ thì dễ phai, như nén hương ngày giỗ giữ cho nỗi nhớ có chỗ bám.",
"**Người quân tử.** Quân tử (君子) vốn nghĩa là “con nhà vua chúa” (Richey, IEP); Khổng Tử biến nó thành danh hiệu của nhân cách mà ai tu dưỡng cũng đạt được. “Quân tử hiểu điều nghĩa, tiểu nhân hiểu điều lợi” (4.16). Con đường là học đi đôi với nghĩ: học mà không nghĩ thì mờ mịt, nghĩ mà không học thì nguy (2.15).",
"**Cai trị bằng đức.** Dẫn dắt dân bằng mệnh lệnh, giữ trật tự bằng hình phạt thì dân chỉ tránh tội mà không biết hổ thẹn; dẫn dắt bằng đức, giữ trật tự bằng lễ thì dân biết hổ thẹn và tự sửa (2.3). Đức của người cầm quyền như gió, của dân như cỏ: gió thổi qua, cỏ ắt rạp theo (12.19).",
"**Gia đình là gốc.** Hiếu với cha mẹ, kính anh là gốc của nhân (1.2, lời Hữu Tử). Nhưng gốc ấy cũng sinh ra câu hỏi khó: khi có người khoe con mình ngay thẳng đến mức làm chứng cha trộm dê, Khổng Tử đáp rằng ở quê ông, cha che cho con, con che cho cha, “ngay thẳng ở trong đó” (13.18). Đến nay câu nói vẫn gây tranh cãi về giới hạn của lòng trung với gia đình.",
],
"argument": {
"title": "Chính danh — muốn trị nước, hãy gọi cho đúng tên",
"intro": "Tử Lộ hỏi: nếu vua nước Vệ giao chính sự cho thầy, thầy làm gì trước? Khổng Tử đáp: “Ắt phải chính danh!” Tử Lộ chê thầy vu vơ, và ông giảng lại bằng một chuỗi điều kiện nối nhau (*Luận ngữ* 13.3). Theo cách hiểu phổ biến, “danh” là tên gọi và danh phận của người, của việc.",
"premises": [
"Danh không chính thì lời nói không thuận; lời không thuận thì việc không thành.",
"Việc không thành thì lễ nhạc không hưng; lễ nhạc không hưng thì hình phạt không trúng.",
"Hình phạt không trúng thì dân không biết đặt tay chân vào đâu, tức không biết nên làm gì.",
],
"conclusion": "Vậy việc đầu tiên của chính trị là làm cho tên gọi khớp với thực chất: người quân tử đặt tên gì thì phải nói ra được, nói ra thì phải làm được, và không cẩu thả với lời nói của mình.",
"objection": "Chính Tử Lộ nêu phản bác ngay tại chỗ: thầy “vu vơ quá” (迂). Nước đang rối, sao lại lo chuyện chữ nghĩa? Đổi tên không làm thay đổi sự vật. Hơn nữa, đây là một chuỗi điều kiện dài, và một chuỗi chỉ chắc bằng mắt xích yếu nhất: hình phạt sai có nhất thiết bắt nguồn từ tên gọi sai không?",
"reply": "Người theo Khổng Tử đáp: danh không phải chữ nghĩa suông mà là cái khung để người ta phối hợp với nhau. Khi kẻ cướp ngôi vẫn được gọi là vua, khi tăng giá được gọi là “điều chỉnh”, sa thải được gọi là “tối ưu nhân sự”, người ta mất thước đo chung để phán đoán, và trách nhiệm trở nên mù mờ. Từng mắt xích có thể bàn lại, nhưng chiều hướng của cả chuỗi thì ai từng làm việc trong một tổ chức cũng nhận ra.",
},
"quote": {
"source": "Khổng Tử, *Luận ngữ* 15.24 (thiên Vệ Linh Công) — nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "子貢問曰：「有一言而可以終身行之者乎？」子曰：「其恕乎！己所不欲，勿施於人。」 — Tử Cống vấn viết: “Hữu nhất ngôn nhi khả dĩ chung thân hành chi giả hồ?” Tử viết: “Kỳ thứ hồ! Kỷ sở bất dục, vật thi ư nhân.”",
"vi": "Tử Cống hỏi: “Có một chữ nào có thể theo mà làm suốt đời không?” Thầy đáp: “Có lẽ là chữ thứ chăng! Điều mình không muốn, đừng làm cho người.”",
"url": "https://ctext.org/analects/wei-ling-gong/zh",
},
"misread": [
"**“Nho giáo của Khổng Tử dạy phục tùng tuyệt đối: vua bảo chết là phải chết.”** Thực ra trong *Luận ngữ*, quan hệ vua tôi có hai chiều: vua sai khiến bề tôi theo lễ, bề tôi thờ vua bằng lòng trung (3.19); bậc đại thần “lấy đạo thờ vua, không được thì thôi” (11.24). Theo một chuyện chép trong *Hàn Thi ngoại truyện*, ông còn trách học trò Tăng Tử đã cam chịu trận đòn quá nặng của cha (Csikszentmihalyi, SEP).",
"**“Khổng Tử đã nói: ‘Thực sắc, tính dã’.”** Thực ra câu “ăn uống và sắc dục là bản tính” là lời Cáo Tử, đối thủ của Mạnh Tử (*Mạnh Tử* 6A4). Ông cũng không tự viết sách: ông nhận mình chỉ “thuật lại chứ không sáng tác” (7.1).",
],
"related": [
("doc/luan-ngu.md", "Luận ngữ — những lời dạy của Khổng Tử"),
("cau-hoi/duc-tri.md", "Cai trị bằng đức hay bằng pháp?"),
("cau-hoi/nho-giao-viet.md", "Nho giáo Việt Nam: tiếp thu hay sáng tạo?"),
("cau-hoi/noi-doi.md", "Có bao giờ được nói dối?"),
("lich-su/trung-hoa.md", "Trung Hoa: trăm nhà đua tiếng"),
],
"sources": [
("Csikszentmihalyi, Mark, “Confucius”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/confucius/"),
("Richey, Jeff, “Confucius”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/confucius/"),
("*Luận ngữ* (論語), nguyên văn chữ Hán kèm bản dịch tiếng Anh của James Legge, ctext.org.", "https://ctext.org/analects"),
("Tư Mã Thiên, *Sử ký*, “Khổng Tử thế gia” (孔子世家), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/shiji/kong-zi-shi-jia/zh"),
],
},
"mac-tu": {
"desc": "Mặc Tử, người thợ thành triết gia: kiêm ái, chống chiến tranh xâm lược, đo mọi chủ trương bằng lợi ích của dân, đối thủ lớn đầu tiên của Nho gia.",
"bio": [
"Nghe tin người thợ trứ danh Công Thâu Ban vừa làm xong thang mây cho nước Sở để đánh nước Tống, Mặc Tử đi ròng rã mười ngày mười đêm tới Dĩnh, kinh đô Sở. Trước mặt vua Sở, ông cởi dây lưng làm tường thành, lấy thẻ gỗ làm khí giới, đấu trận giả: chín lần Công Thâu Ban đổi cách công, chín lần ông chống được. Ông còn cho biết ba trăm học trò của mình đã cầm khí cụ phòng thủ đứng sẵn trên thành Tống. Vua Sở bỏ ý định đánh Tống. Trên đường về đi qua nước Tống, trời mưa, ông vào trú dưới cổng làng, người giữ cổng không cho vào. Sách *Mặc Tử* (thiên “Công Thâu”) kết: người lo việc một cách thầm lặng thì thiên hạ chẳng ai biết công.",
"Về con người thật của ông, ta biết rất ít. Ông tên Địch (墨翟); *Sử ký* chỉ ghi ông làm đại phu nước Tống, giỏi phòng thủ, chủ trương tiết kiệm, sống cùng thời hoặc sau Khổng Tử. Niên đại khoảng 470–391 TCN chỉ là ước đoán; Chris Fraser (SEP) cho rằng ông hoạt động mạnh nhất vào nửa sau thế kỷ 5 TCN, cùng thời với Socrates. Sách *Hoài Nam Tử* đời Hán chép rằng ông từng học đạo Nho rồi bỏ, vì thấy lễ nghi rườm rà, tang ma tốn của làm dân nghèo; nhưng Fraser cho rằng giả thuyết ông xuất thân là thợ, có lẽ là thợ mộc, hợp lý hơn: sách của phái ông đầy ví dụ về nghề thủ công, buôn bán và cảnh thiếu thốn.",
"Mặc gia là một tổ chức hơn là một trường phái: môn đồ sống kham khổ, mỗi nhóm có một thủ lĩnh (cự tử), phải đóng góp tiền, có thể bị khai trừ, và được đưa đi làm quan hay làm lính giữ thành. Đến thế kỷ 3 TCN, Hàn Phi vẫn gọi Nho và Mặc là “hai học phái lừng lẫy” của thiên hạ. Mặc gia hậu kỳ còn để lại những khảo cứu về logic, hình học, quang học. Rồi sau khi nhà Tần thống nhất Trung Hoa, phái này lụi tàn; sách *Mặc Tử* suýt thất truyền, chỉ còn nhờ được chép vào Đạo tạng, và mãi đến cuối đời Thanh mới được đọc kỹ trở lại.",
"Vì sao vẫn đọc Mặc Tử hôm nay? Vì ông là người đầu tiên ở Trung Hoa nói rõ rằng phong tục không tự nó đúng, và đi tìm một tiêu chuẩn khách quan để phán xét. Câu trả lời của ông, đo đúng sai bằng lợi ích chung của thiên hạ, được Fraser gọi là hình thức **hệ quả luận** (*consequentialism*) sớm nhất thế giới, trước Bentham hơn hai nghìn năm.",
],
"works": [
("TK 5–3 TCN", "*Mặc Tử* (墨子)", "Tập văn của nhiều thế hệ Mặc gia, không phần nào tự nhận do chính Mặc Địch viết; nguyên có 71 thiên, nay còn 53"),
("", "“Kiêm ái” (兼愛, thiên 14–16) và “Phi công” (非攻, thiên 17–19)", "Lý lẽ cho sự quan tâm không phân biệt và chống chiến tranh xâm lược"),
("", "“Phi mệnh” (非命, thiên 35–37)", "Bác thuyết định mệnh; nêu “ba tiêu chuẩn” (三表) để thẩm định một lời nói"),
("k. nửa đầu TK 3 TCN", "*Mặc kinh* (墨經, thiên 40–45)", "Mặc gia hậu kỳ: ngữ nghĩa, tri thức luận, lập luận loại suy, hình học, quang học"),
],
"thoughts": [
"**Kiêm ái (兼愛).** Thầy thuốc phải biết bệnh từ đâu mới chữa được; người lo việc thiên hạ phải biết loạn từ đâu. Loạn sinh ra từ chỗ người ta không thương nhau: con chỉ thương mình mà làm thiệt cha, vua chỉ thương mình mà làm thiệt bề tôi (thiên 14). Thuốc chữa: thương nhau mọi bề và cùng làm lợi cho nhau.",
"**Phi công (非攻).** Trộm đào mận nhà bên là bất nghĩa; trộm gà chó, trâu ngựa còn bất nghĩa hơn; giết một người vô tội thì đáng tội chết. Vậy mà đánh chiếm cả một nước lại được khen là nghĩa (thiên 17). Mặc Tử vạch ra tiêu chuẩn kép: cùng một loại việc, chỉ khác quy mô.",
"**Ba tiêu chuẩn (三表).** Nói mà không có thước đo thì như đặt đồng hồ mặt trời trên bàn xoay của thợ gốm. Muốn biết một lời nói đúng hay sai, hãy xét gốc ở việc làm của các thánh vương xưa, xét nguồn ở những gì tai mắt trăm họ thật sự thấy nghe, và xét dụng bằng cách đem ra làm chính sách xem có lợi cho nước, cho dân không (thiên 35).",
"**Tiết dụng (節用) và câu hỏi về phong tục.** Mọi khoản chi không làm dân no hơn, ấm hơn, yên hơn đều nên bỏ: ma chay linh đình, để tang ba năm, nhạc lễ xa xỉ. Khi phe Nho viện cớ người quân tử vẫn làm thế mãi, Mặc Tử kể về một nước ở phía đông nước Việt cổ, nơi con trưởng sinh ra bị xẻ thịt ăn “cho tốt cho em”, và nói: ấy là “quen thói thì cho là tiện, quen tục thì cho là nghĩa” (thiên 25). Tục của người có thể sai, thì tục của ta cũng có thể sai.",
],
"argument": {
"title": "Kiêm ái có dùng được không? (thiên 16 “Kiêm ái hạ”)",
"intro": "Người phản đối nói: kiêm ái hay thì hay thật, nhưng dùng được sao? Mặc Tử đáp: nếu không dùng được thì chính ông cũng sẽ phản đối, nhưng làm gì có điều tốt mà không dùng được? Rồi ông đặt ra một tình huống:",
"premises": [
"Hình dung hai người: một người giữ “biệt”, chỉ lo cho thân mình và người nhà mình; một người giữ “kiêm”, lo cho bạn như lo cho mình, cho cha mẹ bạn như cha mẹ mình.",
"Giả sử bạn sắp mặc giáp ra trận, hoặc đi sứ nơi xa, sống chết chưa biết, và phải gửi cha mẹ, vợ con lại cho một trong hai người ấy.",
"Ai cũng sẽ gửi cho người giữ “kiêm”, kể cả người ngoài miệng chê kiêm ái: “thiên hạ không có người đàn ông, đàn bà ngu nào” làm khác.",
],
"conclusion": "Vậy kẻ chê kiêm ái tự mâu thuẫn: lời nói thì chê kiêm, mà khi phải chọn thì chọn kiêm. Kiêm ái là con đường mà chính họ muốn những người quanh mình đi theo.",
"objection": "Muốn người khác quan tâm đến mình không có nghĩa là mình phải quan tâm đến mọi người như nhau: một người ích kỷ khôn ngoan hoàn toàn có thể mong người khác “kiêm” còn mình thì “biệt”. Hơn nữa, lập luận dựng một thế lưỡng nan giả: “biệt” ở đây là coi thường, làm hại người khác, trong khi giữa thái độ ấy và thương mọi người như nhau còn nhiều lựa chọn, chẳng hạn thương có thứ bậc như Nho gia (Fraser, SEP).",
"reply": "Mặc gia đáp rằng họ đang bàn về một đạo, tức một bộ quy tắc chung cho mọi người, kể cả chính mình; muốn người khác theo một đạo mà mình không theo là không nhất quán (Fraser, SEP). Mặc gia hậu kỳ còn tinh chỉnh: quan tâm thì như nhau, nhưng giúp đỡ thì bắt đầu từ người gần, “yêu không phân bậc, làm thì bắt đầu từ người thân”, như lời người theo Mặc là Di Chi trong *Mạnh Tử* (3A5).",
},
"quote": {
"source": "*Mặc Tử*, thiên 15 “Kiêm ái trung” (兼愛中) — nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "視人之國若視其國，視人之家若視其家，視人之身若視其身。 — Thị nhân chi quốc nhược thị kỳ quốc, thị nhân chi gia nhược thị kỳ gia, thị nhân chi thân nhược thị kỳ thân.",
"vi": "Coi nước của người như nước của mình, coi nhà của người như nhà của mình, coi thân của người như thân của mình.",
"url": "https://ctext.org/mozi/universal-love-ii/zh",
},
"misread": [
"**“Mặc Tử là người theo chủ nghĩa hòa bình tuyệt đối.”** Thực ra ông chống chiến tranh *xâm lược*, không chống tự vệ. Ông và môn đồ còn là chuyên gia phòng thủ thành: một loạt thiên cuối sách *Mặc Tử* bàn kỹ thuật giữ thành trước thang leo, đường hầm hay nước ngập.",
"**“Kiêm ái nghĩa là phải thương người dưng y hệt cha mẹ mình.”** Thực ra theo Fraser (SEP), “biệt” mà Mặc gia phản đối là thái độ coi thường, làm hại người ngoài, chứ không phải chuyện thương người nhà hơn. Các ví dụ cụ thể trong sách khá khiêm tốn: đừng hại ai, làm tròn bổn phận với gia đình, giúp người già cả, cô quạnh không ai nuôi.",
],
"related": [
("doc/mac-tu-kiem-ai.md", "Hướng dẫn đọc Mặc Tử: kiêm ái"),
("doc/manh-tu-tinh-thien.md", "Hướng dẫn đọc Mạnh Tử: tính thiện"),
("lich-su/trung-hoa.md", "Trung Hoa: trăm nhà đua tiếng"),
],
"sources": [
("Fraser, Chris, “Mohism”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/mohism/"),
("Loy, Hui-chieh, “Mozi (Mo-tzu, c. 400s—300s B.C.E.)”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/mozi/"),
("*Mặc Tử* (墨子), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/mozi"),
("*Mặc Tử*, thiên “Công Thâu” (公輸), nguyên văn chữ Hán, Wikisource tiếng Trung.", "https://zh.wikisource.org/wiki/%E5%A2%A8%E5%AD%90/%E5%85%AC%E8%BC%B8"),
("*Hoài Nam Tử*, thiên “Yếu lược” (要略), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/huainanzi/yao-lve/zh"),
],
},
"manh-tu": {
"desc": "Mạnh Tử, “Á thánh” của Nho gia: bốn mầm thiện, chuyện vua Tề và con trâu, dân là quý, và vì sao “không làm” khác với “không thể”.",
"bio": [
"“Tin hết vào sách thì chẳng bằng không có sách.” Nhiều người Việt thuộc câu ấy, ít ai biết hoàn cảnh của nó. Mạnh Tử đang nói về thiên “Vũ Thành” của *Kinh Thư*, chép rằng khi Vũ vương đánh vua Trụ, máu chảy trôi cả chày giã gạo. Ông bảo mình chỉ tin “hai ba thẻ” trong đó: người chí nhân đánh kẻ chí bất nhân, sao lại đổ máu đến thế? (*Mạnh Tử* 7B3). Một cách đọc sách có phê phán, dù lý do ông đưa ra cũng cho thấy ông sẵn sàng gạt một sử liệu vì nó trái với niềm tin của mình.",
"Ông tên Kha, người nước Trâu (nay thuộc Sơn Đông), sinh khoảng một thế kỷ sau khi Khổng Tử mất. Theo truyền thống ông sống khoảng 372–289 TCN, nhưng nhiều học giả nay đẩy niên đại lên sớm hơn chừng hai mươi năm (Van Norden, SEP). Cha mất sớm; nhiều giai thoại kể về người mẹ dốc lòng lo cho con học, nổi tiếng nhất là chuyện ba lần dời nhà (tương truyền). Theo *Sử ký*, ông học với môn đồ của Tử Tư, cháu nội Khổng Tử, rồi đi thuyết vua Tuyên nước Tề, vua Huệ nước Lương: vua Tề không dùng, vua Lương cho là vu khoát, xa thực tế, giữa lúc các nước chỉ lo hợp tung liên hoành, đánh nhau. Về già, ông cùng học trò như Vạn Chương soạn sách *Mạnh Tử* bảy thiên.",
"Ông sống giữa hai đối thủ: Dương Chu dạy “vì mình”, Mặc Tử dạy “kiêm ái”. Mạnh Tử chê cả hai, một bên coi như không có vua, một bên coi như không có cha (3B9), và nhận việc của mình là chặn lời Dương, Mặc để giữ đạo Khổng Tử. Câu trả lời của ông nằm ở bản tính con người: ai cũng có bốn mầm thiện. Từ đó suy ra một học thuyết chính trị: vua phải lo cho dân có của cải ổn định trước rồi mới mong dân giữ được lòng ngay; “dân là quý, xã tắc thứ hai, vua là nhẹ” (7B14).",
"Lúc sinh thời ông không được trọng dụng. Từ Hàn Dũ (768–824), người coi ông là môn đồ “thuần khiết nhất” của Khổng Tử, đến các nhà Tân Nho giáo đời Tống, ông dần được tôn làm “Á thánh”, người đứng thứ hai sau Khổng Tử; Chu Hy đưa sách ông vào bộ *Tứ thư*, và học thuyết tính thiện thành chính thống. Câu “nhân chi sơ, tính bản thiện” trong *Tam tự kinh* mà nhiều thế hệ học trò chữ Hán thuộc lòng chính là dư âm của ông, qua lăng kính Chu Hy. Ngày nay ông được đọc cạnh Aristotle và Hume như một nhà đạo đức học về đức hạnh (SEP).",
],
"works": [
("TK 4–3 TCN", "*Mạnh Tử* (孟子)", "Bảy thiên, mỗi thiên hai phần (1A–7B); do ông và học trò, hoặc học trò của học trò, biên soạn; Triệu Kỳ biên tập, chú giải ở thế kỷ 2"),
("", "“Lương Huệ vương” (梁惠王, 1A–1B)", "Hà tất nói chuyện lợi; vua Tề và con trâu; giết kẻ tàn bạo không phải là giết vua"),
("", "“Công Tôn Sửu thượng” (公孫丑上, 2A)", "Đứa trẻ bên giếng và bốn mầm thiện"),
("", "“Cáo Tử thượng” (告子上, 6A)", "Tranh luận với Cáo Tử về tính người; núi Ngưu"),
],
"thoughts": [
"**Bốn mầm thiện.** Ai bỗng thấy đứa trẻ sắp rơi xuống giếng cũng giật mình thương xót, không vì muốn lấy lòng cha mẹ nó hay muốn được khen (2A6). Lòng trắc ẩn, lòng hổ thẹn, lòng nhường nhịn, lòng biết phải trái là bốn “đầu mối” (端) của nhân, nghĩa, lễ, trí; người ta có chúng như có tứ chi.",
"**Núi Ngưu.** Núi Ngưu xưa cây cối tốt tươi; vì ở sát kinh đô, ngày ngày bị đốn, mầm mới nhú lại bị trâu dê gặm, nên trơ trụi. Người ta nhìn núi trọc tưởng núi chưa từng có cây: “há đó là tính của núi sao?” (6A8). Điều ác không chứng minh tính người ác; nó cho thấy mầm thiện bị đốn hằng ngày.",
"**Có hằng sản mới có hằng tâm.** Dân không có của cải ổn định thì khó giữ lòng ngay; để dân sa vào tội rồi mới trừng phạt là “giăng lưới bắt dân” (1A7). Chính quyền phải lo cho dân no ấm trước khi đòi đạo đức.",
],
"argument": {
"title": "Không làm hay không thể? (vua Tề và con trâu, 1A7)",
"intro": "Vua Tuyên nước Tề thấy người ta dắt một con trâu đi giết lấy máu bôi chuông mới đúc. Không nỡ nhìn nó run rẩy “như người vô tội bị đưa đến chỗ chết”, vua bảo đổi bằng con dê. Mạnh Tử dùng chính chuyện ấy để lập luận với nhà vua:",
"premises": [
"Nhà vua có lòng thương thật: nó đủ mạnh để thay đổi một quyết định, dù chỉ vì một con vật.",
"Thương dân, bớt thuế, thôi gây chiến là việc cùng loại mà dễ hơn: như bẻ một cành cây giúp người lớn tuổi, chứ không phải kẹp núi Thái Sơn nhảy qua biển Bắc.",
"Ai làm được việc khó mà bảo không làm nổi việc dễ cùng loại thì đó là “không làm”, không phải “không thể”, như người nhấc nổi nghìn cân mà bảo không nhấc nổi một sợi lông.",
],
"conclusion": "Nhà vua chưa thi hành chính sách nhân từ là vì không chịu làm, không phải vì không thể. Việc cần làm là “mở rộng” (推) lòng thương sẵn có: kính già nhà mình rồi kính đến già nhà người, thương trẻ nhà mình rồi thương đến trẻ nhà người.",
"objection": "Chính câu chuyện cho thấy lòng trắc ẩn thiên lệch: vua tha con trâu ông thấy, còn con dê ông không thấy thì vẫn bị giết; Mạnh Tử thừa nhận vua “thấy trâu mà chưa thấy dê”. Nếu lòng thương chỉ bật lên trước cái ta nhìn thấy, thì mở rộng nó tới hàng vạn người dân vô hình là việc khó thật, không dễ như bẻ cành cây. Hơn nữa, nhận ra hai trường hợp giống nhau về lý chưa chắc đã khiến ta muốn hành động: đó là câu hỏi David Nivison nêu năm 1980, mở ra cả một cuộc tranh luận về sự “mở rộng” trong học giới phương Tây (Van Norden, SEP).",
"reply": "Mạnh Tử không nói lòng thương thô sơ là đủ. Ông gọi nó là mầm, và mầm cần ba điều kiện để lớn: dân được no ấm, được giáo dục, và mỗi người tự suy ngẫm (思). Cuộc đối thoại với vua Tề chính là để khơi sự suy ngẫm ấy: “cân rồi mới biết nặng nhẹ, đo rồi mới biết dài ngắn; vật nào cũng vậy, lòng người lại càng thế” (1A7). Thấy được chỗ thiên lệch của lòng mình đã là bước đầu của việc mở rộng nó.",
},
"quote": {
"source": "Mạnh Tử, *Mạnh Tử* 3B2 (thiên Đằng Văn công hạ), lời đáp Cảnh Xuân về các thuyết khách — nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "得志與民由之，不得志獨行其道。富貴不能淫，貧賤不能移，威武不能屈。此之謂大丈夫。 — Đắc chí dữ dân do chi, bất đắc chí độc hành kỳ đạo. Phú quý bất năng dâm, bần tiện bất năng di, uy vũ bất năng khuất. Thử chi vị đại trượng phu.",
"vi": "Đắc chí thì cùng dân đi theo đạo, không đắc chí thì một mình giữ đạo của mình. Giàu sang không làm cho hư hỏng, nghèo hèn không làm cho đổi lòng, uy vũ không khuất phục được. Như thế mới gọi là bậc đại trượng phu.",
"url": "https://ctext.org/mengzi/teng-wen-gong-ii/zh",
},
"misread": [
"**“‘Nhân chi sơ, tính bản thiện’ là lời Mạnh Tử.”** Thực ra câu ấy mở đầu *Tam tự kinh*, sách vỡ lòng ra đời nhiều thế kỷ sau. Mạnh Tử nói “tính thiện” (性善); chữ “bản” (vốn) đến từ lối chú giải được Chu Hy phổ biến (Van Norden, SEP). Ông cũng không nói ai sinh ra đã tốt sẵn, mà nói tính người “có thể làm điều thiện” (6A6), như mầm có thể thành cây.",
"**“Mạnh Tử cổ vũ dân nổi dậy lật vua.”** Thực ra ông nói ngôi vua chính đáng khi được lòng dân, và kẻ tàn bạo đã tự đánh mất tư cách làm vua (1B8). Nhưng ông không đề ra cơ chế nào để dân tự truất phế; những người “trừ kẻ độc phu” trong các ví dụ của ông là những vị vua hiền như Thang, Vũ.",
],
"related": [
("doc/manh-tu-tinh-thien.md", "Hướng dẫn đọc Mạnh Tử: tính thiện"),
("cau-hoi/ban-tinh-con-nguoi.md", "Bản tính con người thiện hay ác?"),
("cau-hoi/duc-tri.md", "Cai trị bằng đức hay bằng pháp?"),
("doc/mac-tu-kiem-ai.md", "Hướng dẫn đọc Mặc Tử: kiêm ái"),
("cau-hoi/nho-giao-viet.md", "Nho giáo Việt Nam: tiếp thu hay sáng tạo?"),
],
"sources": [
("Van Norden, Bryan, “Mencius”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/mencius/"),
("*Mạnh Tử* (孟子), nguyên văn chữ Hán kèm bản dịch tiếng Anh của James Legge, ctext.org.", "https://ctext.org/mengzi"),
("Tư Mã Thiên, *Sử ký*, “Mạnh Tử Tuân Khanh liệt truyện” (孟子荀卿列傳), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/shiji/meng-zi-xun-qing-lie-zhuan/zh"),
],
},
"trang-tu": {
"desc": "Trang Tử, nhà Đạo gia hoài nghi và hài hước: mộng hồ điệp, sáng ba chiều bốn, người đồ tể mổ bò, và câu hỏi ai phân xử được đúng sai.",
"bio": [
"Hai vị đại phu nước Sở tìm đến bờ sông Bộc, nơi Trang Tử đang ngồi câu cá, để mời ông ra gánh việc nước. Ông vẫn cầm cần câu, không ngoảnh lại, hỏi: nghe nói nước Sở có con rùa thần chết đã ba nghìn năm, vua cất mai nó trong miếu đường; con rùa ấy muốn chết để lại bộ xương được tôn quý, hay muốn sống mà lê đuôi trong bùn? Hai người đáp: muốn sống mà lê đuôi trong bùn. “Vậy các ông về đi, tôi sẽ lê đuôi trong bùn” (thiên 17 “Thu thủy”). *Sử ký* chép một chuyện tương tự, chỉ khác hình ảnh: con trâu tế được vỗ béo, khoác gấm, để rồi bị dắt vào miếu.",
"Ông tên Chu, người đất Mông, từng làm một chức quan nhỏ coi vườn sơn, sống cùng thời với vua Huệ nước Lương và vua Tuyên nước Tề (*Sử ký*), tức nửa sau thế kỷ 4 TCN, cùng thời với Mạnh Tử. Ngoài vài dòng ấy, gần như mọi điều ta biết về ông đến từ chính sách *Trang Tử*, một cuốn sách đầy ngụ ngôn, nên phải đọc với chút hoài nghi (Hansen, SEP). Người bạn tranh luận thân nhất của ông là nhà biện giả Huệ Thi.",
"Bản *Trang Tử* ta đọc ngày nay gồm 33 thiên do Quách Tượng (mất năm 312) rút gọn từ 52 thiên, chia làm Nội thiên (1–7), Ngoại thiên (8–22) và Tạp thiên (23–33). Quách Tượng chỉ coi Nội thiên là gần với thời Trang Tử; các phần sau có lẽ của môn đồ và những dòng tư tưởng khác (Hansen, SEP).",
"Hơn hai nghìn năm sau, Trang Tử vẫn là tác giả dễ mến nhất của triết học Trung Hoa, với những truyện về người đồ tể mổ bò mười chín năm không phải mài dao, hay con ếch trong giếng không thể nói chuyện biển cả, gần với câu “ếch ngồi đáy giếng” của ta. Hansen so ông với Hume hơn là với những người dựng hệ thống như Platon, Aristotle hay Kant. Cùng với *Lão Tử*, sách của ông góp phần nhào nặn Thiền tông Trung Hoa (SEP).",
],
"works": [
("TK 4–3 TCN", "*Trang Tử* (莊子)", "33 thiên theo bản Quách Tượng: Nội thiên (1–7), Ngoại thiên (8–22), Tạp thiên (23–33)"),
("", "“Tề vật luận” (齊物論, thiên 2)", "Bàn về sự ngang nhau của muôn vật; giấc mộng hồ điệp"),
("", "“Dưỡng sinh chủ” (養生主, thiên 3)", "Nuôi dưỡng sự sống; người đồ tể Đinh mổ bò"),
("", "“Nhân gian thế” (人間世, thiên 4)", "Sống giữa cõi người: cái cây vô dụng nhờ vô dụng mà sống lâu"),
("", "“Thu thủy” (秋水, thiên 17)", "Con ếch trong giếng, con rùa lê đuôi trong bùn, niềm vui của cá"),
],
"thoughts": [
"**Đúng sai tùy chỗ đứng.** Người ngủ chỗ ẩm thì đau lưng, liệt nửa người, con chạch có thế không? Người ở trên cây thì run sợ, con khỉ có thế không? Ba loài ấy, ai biết chỗ ở nào là đúng? Người đẹp làm ai cũng mê, nhưng cá thấy thì lặn sâu, chim thấy thì bay cao (thiên 2). Trang Tử không bảo mọi ý kiến đều như nhau; ông chỉ ra rằng lời “phải, trái” nào cũng được nói từ một chỗ đứng, thường vô hình với chính người nói.",
"**Sáng ba chiều bốn.** Người nuôi khỉ bảo: sáng cho ba hạt dẻ, chiều bốn; bầy khỉ nổi giận. Đổi lại sáng bốn, chiều ba; bầy khỉ mừng rỡ. Danh và thực không suy suyển gì mà mừng giận đã khác (thiên 2); thành ngữ “triêu tam mộ tứ” bắt nguồn từ đây. Cách đóng khung một chuyện có khi quyết định cảm xúc của ta hơn bản thân sự việc; bậc thánh nhân không cãi với bầy khỉ mà để cả hai cùng đi, gọi là “lưỡng hành”.",
"**Kỹ năng thành Đạo.** Người đồ tể Đinh mổ bò cho vua Văn Huệ: điều ông ưa là Đạo, vượt lên trên kỹ thuật. Ông lách lưỡi dao theo kẽ thớ tự nhiên, nên con dao dùng mười chín năm, mổ mấy nghìn con bò mà lưỡi vẫn như mới mài (thiên 3). Sống khéo là thuận theo kẽ thớ của sự việc, không chặt bổ vào chỗ cứng.",
"**Biết lòng kẻ khác.** Trang Tử và Huệ Tử dạo trên cầu sông Hào. “Cá bơi thong thả, ấy là niềm vui của cá.” “Anh không phải cá, sao biết cá vui?” “Anh không phải tôi, sao biết tôi không biết cá vui?” (thiên 17). Cuộc đối đáp ngắn này đặt ra từ rất sớm điều triết học ngày nay gọi là **vấn đề những tâm trí khác** (*problem of other minds*).",
],
"argument": {
"title": "Ai phân xử được cuộc tranh luận? (thiên 2 “Tề vật luận”)",
"intro": "Trong thiên “Tề vật luận”, qua lời nhân vật Trường Ngô Tử, Trang Tử dựng một lập luận mà người đời sau đọc như một trong những lập luận hoài nghi sắc sảo nhất của triết học Trung Hoa:",
"premises": [
"Giả sử anh và tôi tranh luận. Anh thắng tôi, chưa chắc anh đúng, tôi sai; tôi thắng anh, chưa chắc tôi đúng, anh sai.",
"Muốn biết ai đúng phải nhờ người thứ ba phân xử. Nhưng người ấy hoặc đồng ý với anh, hoặc đồng ý với tôi, hoặc khác cả hai, hoặc đồng ý cả hai.",
"Trong cả bốn trường hợp, người phân xử đã đứng sẵn ở một chỗ đứng (“đã giống anh rồi thì sao phân xử được?”), nên không thể phân xử một cách trung lập.",
],
"conclusion": "Không có chỗ đứng trung lập nào để định đoạt đúng sai một lần cho xong; thay vì cố thắng, hãy “hòa nó bằng lẽ quân bình tự nhiên” (hòa chi dĩ thiên nghê).",
"objection": "Lập luận này có nguy cơ tự phá mình: nếu không cuộc tranh luận nào phân xử được, thì chính kết luận ấy cũng không được phân xử. Mặc gia hậu kỳ bác thẳng: nói rằng tranh biện không có bên thắng là nói sai; khi một người bảo vật này “là trâu”, người kia bảo “không phải trâu”, thì ít nhất một bên phải sai, và “bên nào khớp với sự vật thì thắng” (*Mặc Tử*, Kinh hạ và Kinh thuyết hạ; Fraser, SEP). Đời thường cũng có cách phân xử không cần người trung lập tuyệt đối: đo đạc, thí nghiệm, chứng cứ.",
"reply": "Người đọc Trang Tử theo lối hoài nghi “chữa bệnh” đáp: ông không đưa ra một học thuyết để thắng ai, ông đặt câu hỏi để nới lỏng sự quả quyết. Ông vẫn chấp nhận “nhân thị”, tạm theo cái “phải” của tình huống, miễn đừng biến nó thành chân lý tuyệt đối. Với đo đạc, ông có thể hỏi lại: chọn thước đo nào, và ai chọn? Đó đúng là điều mà Nho gia và Mặc gia tranh nhau suốt thời ấy.",
},
"quote": {
"source": "Trang Tử, *Trang Tử*, thiên 4 “Nhân gian thế” (人間世), đoạn kết — nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "山木自寇也，膏火自煎也。桂可食，故伐之；漆可用，故割之。人皆知有用之用，而莫知無用之用也。 — Sơn mộc tự khấu dã, cao hỏa tự tiễn dã. Quế khả thực, cố phạt chi; tất khả dụng, cố cát chi. Nhân giai tri hữu dụng chi dụng, nhi mạc tri vô dụng chi dụng dã.",
"vi": "Cây trên núi tự chuốc lấy búa rìu, mỡ đèn tự đốt cạn mình. Quế ăn được nên bị chặt, sơn dùng được nên bị rạch. Người đời ai cũng biết cái dụng của cái hữu dụng, mà chẳng ai biết cái dụng của cái vô dụng.",
"url": "https://ctext.org/zhuangzi/man-in-the-world-associated-with/zh",
},
"misread": [
"**“Mộng hồ điệp chứng minh đời chỉ là giấc mộng.”** Thực ra Trang Tử dừng ở câu hỏi rồi viết thêm: “Chu với bướm ắt phải có phân biệt; ấy gọi là vật hóa” (thiên 2). Ông không xóa ranh giới giữa mộng và thực, mà nhắc rằng ranh giới ấy luôn chuyển hóa, và sự chắc chắn của ta về nó mỏng hơn ta tưởng.",
"**“Trang Tử là học trò của Lão Tử.”** Thực ra *Sử ký* không nói hai người từng gặp nhau, mà chỉ nói học thuyết của Trang Tử “gốc ở lời Lão Tử”. Việc gộp hai ông thành một trường phái là cách xếp loại từ đời Hán (Chan, SEP). Chad Hansen (SEP) còn cho rằng Trang Tử không phải người diễn giải một Lão Tử thần bí: đối thủ thật sự của ông là trực giác đạo đức kiểu Mạnh Tử và chủ nghĩa công lợi của Mặc Tử.",
],
"related": [
("doc/trang-tu-mong-ho-diep.md", "Mộng hồ điệp — Trang Tử (thiên Tề vật luận)"),
("doc/dao-duc-kinh.md", "Hướng dẫn đọc Đạo đức kinh"),
("lich-su/trung-hoa.md", "Trung Hoa: trăm nhà đua tiếng"),
],
"sources": [
("Hansen, Chad, “Zhuangzi”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/zhuangzi/"),
("*Trang Tử* (莊子), nguyên văn chữ Hán kèm bản dịch tiếng Anh của James Legge, ctext.org.", "https://ctext.org/zhuangzi"),
("Tư Mã Thiên, *Sử ký*, “Lão Tử Hàn Phi liệt truyện” (老子韓非列傳), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/shiji/lao-zi-han-fei-lie-zhuan/zh"),
("Fraser, Chris, “Mohist Canons”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/mohist-canons/"),
("Chan, Alan, “Laozi”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/laozi/"),
],
},
"tuan-tu": {
"desc": "Tuân Tử, nhà Nho nói “tính người là ác”: điều thiện do con người làm ra, học tập và lễ nghĩa chuyển hóa bản tính, còn trời chỉ là tự nhiên vận hành.",
"bio": [
"Giữa một thời ai cũng tin điềm báo, có một nhà Nho viết: “Cầu mưa mà mưa, là vì sao? Chẳng vì sao cả, cũng như không cầu mà mưa thôi.” Ông nói thêm: người quân tử coi lễ cầu mưa, lễ cứu nhật thực là nghi thức văn hóa, còn trăm họ coi đó là thần thông; coi là văn hóa thì lành, coi là thần thông thì dữ (thiên 17 “Thiên luận”). Người ấy là Tuân Tử, người thầy hàng đầu của thiên hạ vào cuối thời Chiến Quốc (Goldin, SEP).",
"Ông tên Huống, còn được gọi là Tuân Khanh hay Tôn Khanh, người nước Triệu. Năm sinh không rõ: *Sử ký* chép ông đến du học nước Tề năm năm mươi tuổi, nhưng Paul Goldin (SEP) cho rằng con số mười lăm hợp lý hơn, tức ông sinh khoảng năm 310 TCN. Ở Tề, nơi học giả khắp thiên hạ tụ về, ông được tôn là bậc thầy đáng kính nhất và ba lần làm tế tửu, đứng đầu giới học sĩ. Bị gièm, ông sang nước Sở, được Xuân Thân quân cho làm lệnh đất Lan Lăng. Năm 238 TCN Xuân Thân quân bị giết, ông mất chức, ở lại Lan Lăng cho tới cuối đời. Học trò ông có Hàn Phi và Lý Tư, người về sau làm thừa tướng nước Tần.",
"Tuân Tử nhận mình là người nối Khổng Tử, nhưng ông phê phán thẳng tên rất nhiều nhà đương thời: trong thiên “Giải tế”, Mặc Tử, Huệ Thi, Trang Tử, mỗi người đều “bị che” bởi một góc của Đạo; trong thiên “Tính ác”, ông bác Mạnh Tử. Với ông, trời chỉ là tự nhiên vận hành có thường; con người phải tự lo việc của mình bằng học tập, lễ nghĩa và thể chế. Câu nổi tiếng nhất của ông, “tính người là ác, điều thiện là do con người làm ra”, là lời đáp thẳng vào thuyết tính thiện.",
"Hậu thế đối xử với ông khá trớ trêu. Vì hai học trò theo Pháp gia và vì chữ “tính ác”, nhiều Nho gia đời sau coi ông là lệch lạc; Chu Hy còn cho rằng tư tưởng ông gần với Thân Bất Hại, Thương Ưởng và gián tiếp gây ra tai họa nhà Tần. Suốt phần còn lại của thời quân chủ, ông bị dòng chính gạt ra lề. Ngày nay chiều gió đã đảo: theo Goldin (SEP), Tuân Tử là một trong những triết gia được đọc nhiều nhất ở Đông Á, nhờ những lập luận chặt chẽ và một niềm tin rất hiện đại: con người không sinh ra đã tốt, nhưng ai cũng có thể học để trở nên tốt.",
],
"works": [
("TK 3 TCN", "*Tuân Tử* (荀子)", "32 thiên do Lưu Hướng (thế kỷ 1 TCN) biên tập từ 322 bó thẻ tre; phần lớn được coi là của chính ông"),
("", "“Khuyến học” (勸學, thiên 1)", "Khuyên học: học không thể dừng, con người làm nên từ tích lũy"),
("", "“Thiên luận” (天論, thiên 17)", "Bàn về trời: tự nhiên vận hành có thường, được mất là do con người"),
("", "“Lễ luận” (禮論, thiên 19)", "Nguồn gốc và chức năng của lễ"),
("", "“Chính danh” (正名, thiên 22)", "Sửa tên gọi: ngôn ngữ, ước định và thực tại"),
("", "“Tính ác” (性惡, thiên 23)", "Tính người là ác, điều thiện do con người làm ra"),
],
"thoughts": [
"**Trời là tự nhiên, không thưởng phạt.** “Trời vận hành có thường, không vì vua Nghiêu mà còn, không vì vua Kiệt mà mất; ứng với nó bằng trị thì lành, bằng loạn thì dữ” (thiên 17). Mặt trời, mặt trăng, các vì sao dưới thời vua thánh Vũ và bạo chúa Kiệt vẫn y như nhau; được hay mất là do cách con người tổ chức đời mình, đừng đổ cho trời.",
"**Lễ là cột mốc người xưa cắm sẵn.** Dục vọng con người không có bờ mà của cải có hạn; cứ thuận theo dục vọng thì tranh nhau, nên tiên vương đặt lễ nghĩa để chia phần (thiên 19). Như người lội qua sông cắm cọc đánh dấu chỗ sâu, thánh nhân dùng lễ “đánh dấu con đường” để người sau khỏi vấp (Goldin, SEP).",
"**Học là chuyển hóa tính.** Mục tiêu không phải diệt bản tính mà “hóa tính” (化性): “người bình thường ngoài đường cũng có thể thành vua Vũ”, vì ai cũng có tư chất để hiểu và năng lực để làm điều nhân nghĩa (thiên 23). Trẻ con các xứ sinh ra tiếng khóc như nhau, lớn lên phong tục khác nhau, ấy là do dạy dỗ (thiên 1).",
"**Tên gọi do ước định.** “Tên gọi không có cái hợp cố định; người ta ước định với nhau, thành thói quen thì gọi là hợp” (thiên 22). Nhưng tên gọi do ta đặt, còn sự vật thì không: với Tuân Tử, thực tại vẫn là thực tại bất kể ta nhìn nó thế nào, và tên gọi phải được dùng khớp với nó (Goldin, SEP).",
],
"argument": {
"title": "Tính người là ác, điều thiện do người làm ra (thiên 23)",
"intro": "Thiên “Tính ác” mở đầu bằng một luận đề như đáp thẳng Mạnh Tử: “Nhân chi tính ác, kỳ thiện giả ngụy dã.” Chữ then chốt là **ngụy** (偽): không phải “giả dối”, mà gồm bộ nhân (亻) và chữ vi (為, làm), tức cái do con người làm ra.",
"premises": [
"Tính là cái trời sinh sẵn, không học không làm mà có; cái học mà được, làm mà thành thì gọi là ngụy, tức công phu của con người.",
"Sinh ra người ta đã ham lợi, ganh ghét, ham muốn tai mắt; cứ thuận theo thì tranh giành, tàn hại, dâm loạn nổi lên, còn nhường nhịn, trung tín, lễ nghĩa mất đi.",
"Nhường nhịn và lễ nghĩa chỉ xuất hiện khi có thầy, có phép tắc, có lễ nghĩa uốn nắn; con nhường cha, em nhường anh là “trái với tính, ngược với tình”.",
],
"conclusion": "Vậy tính người là ác (xấu); điều thiện ở con người là thành quả của công phu.",
"objection": "Chính Tuân Tử tự nêu câu hỏi: nếu tính người ác thì lễ nghĩa từ đâu ra? Người đầu tiên dạy điều thiện đã học nó từ đâu? Người theo Mạnh Tử còn có thể nói: việc ai cũng học được điều thiện đã là bằng chứng của tính thiện. Và như A. C. Graham nhận xét, hai ông dùng chữ “tính” theo hai nghĩa khác nhau, nên có lẽ đang nói lệch nhau (Goldin, SEP).",
"reply": "Tuân Tử đáp bằng hình ảnh người thợ gốm: cái bình sinh ra từ công phu của người thợ, không từ “tính” của người thợ; lễ nghĩa cũng sinh ra từ công phu tích lũy của thánh nhân. Còn khả năng học điều thiện, như khả năng nhìn của mắt, chỉ là năng lực, chưa phải điều thiện.",
},
"quote": {
"source": "Tuân Tử, *Tuân Tử*, thiên 1 “Khuyến học” (勸學), đoạn mở đầu — nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "君子曰：學不可以已。青、取之於藍，而青於藍；冰、水為之，而寒於水。 — Quân tử viết: Học bất khả dĩ dĩ. Thanh, thủ chi ư lam, nhi thanh ư lam; băng, thủy vi chi, nhi hàn ư thủy.",
"vi": "Người quân tử nói: việc học không thể dừng. Màu xanh lấy từ cây chàm mà xanh hơn chàm; băng do nước làm thành mà lạnh hơn nước.",
"url": "https://ctext.org/xunzi/quan-xue/zh",
},
"misread": [
"**“Tính ác nghĩa là con người sinh ra đã độc ác, hết thuốc chữa.”** Thực ra chữ ác (惡) ở đây, theo Goldin (SEP), gần với “đáng ghét, xấu” hơn là “độc ác”: Tuân Tử chỉ nói rằng cứ để mặc ham muốn bẩm sinh thì sẽ sinh tranh giành. Chính vì thế ông đặt niềm tin vào học tập: gỗ được dây mực thì thẳng, kim loại được mài thì sắc (thiên 1).",
"**“Tuân Tử là ông tổ của Pháp gia, chủ trương trị dân bằng hình phạt.”** Thực ra ông là nhà Nho, đặt lễ nghĩa và người thầy lên trên hết. Hai học trò Hàn Phi và Lý Tư đi theo đường khác; tiếng xấu ấy, theo Goldin (SEP), phần lớn do đời sau gán cho ông.",
],
"related": [
("cau-hoi/ban-tinh-con-nguoi.md", "Bản tính con người thiện hay ác?"),
("doc/manh-tu-tinh-thien.md", "Hướng dẫn đọc Mạnh Tử: tính thiện"),
("lich-su/trung-hoa.md", "Trung Hoa: trăm nhà đua tiếng"),
],
"sources": [
("Goldin, Paul R., “Xunzi”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/xunzi/"),
("*Tuân Tử* (荀子), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/xunzi"),
("Tư Mã Thiên, *Sử ký*, “Mạnh Tử Tuân Khanh liệt truyện” (孟子荀卿列傳), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/shiji/meng-zi-xun-qing-lie-zhuan/zh"),
],
},
"han-phi": {
"desc": "Hàn Phi, nhà tổng hợp Pháp gia: pháp, thuật, thế; chuyện giáo và khiên, ôm cây đợi thỏ, và lập luận rằng đừng chờ vua thánh mà hãy dựng thể chế.",
"bio": [
"Chữ “mâu thuẫn” (矛盾, giáo và khiên) bắt nguồn từ một ngụ ngôn của Hàn Phi. Có người nước Sở bán khiên và giáo, khoe khiên của mình chắc đến mức không gì đâm thủng, rồi lại khoe giáo của mình sắc đến mức không gì không đâm thủng. Có người hỏi: lấy giáo của anh đâm khiên của anh thì sao? Anh ta không đáp được. Hàn Phi kể chuyện ấy để bắt bẻ các nhà Nho: họ vừa khen vua Nghiêu là bậc thánh sáng suốt đang ở ngôi, vừa khen ông Thuấn đi cảm hóa dân từng nơi; nhưng nếu Nghiêu đã sáng suốt thì dân đâu còn sai để Thuấn phải sửa? (thiên 36 “Nạn nhất”).",
"Hàn Phi là một công tử nước Hàn (韓, đừng nhầm với nhà Hán 漢), một nước nhỏ đang bị cắt dần đất đai. Năm sinh không rõ, thường được ước khoảng năm 280 TCN. Theo *Sử ký*, ông nói lắp, không giỏi biện thuyết nhưng viết rất hay; ông cùng Lý Tư học với Tuân Tử, và Lý Tư tự thấy mình không bằng (có học giả nghi mối thầy trò này, theo Goldin, SEP). Ông nhiều lần dâng thư can vua Hàn mà không được dùng, bèn viết các thiên “Cô phẫn”, “Ngũ đố”, “Thuyết nan”… hơn mười vạn chữ.",
"Sách của ông đến tay vua Tần, người về sau là Tần Thủy Hoàng. Đọc “Cô phẫn” và “Ngũ đố”, vua than: được gặp người này mà đàm đạo thì chết cũng không tiếc. Tần đánh gấp nước Hàn; Hàn sai Hàn Phi sang Tần. Nhưng Lý Tư và Diêu Giả gièm rằng ông là công tử nước Hàn, rốt cuộc sẽ vì Hàn chứ không vì Tần; ông bị hạ ngục, Lý Tư sai người đưa thuốc độc bắt tự tử. Vua Tần hối hận cho người đến tha thì ông đã chết, năm 233 TCN. Tư Mã Thiên viết: riêng ta thương Hàn Tử viết thiên “Thuyết nan” về cái khó của việc thuyết phục mà chính mình không thoát được (Pines, SEP, thận trọng gọi đây là cái chết “được kể lại”).",
"Vua Tần không dùng con người Hàn Phi nhưng dùng con đường mà ông là đại diện tiêu biểu nhất: nhà Tần thống nhất Trung Hoa năm 221 TCN và sụp đổ năm 207 TCN. Từ đời Hán, Nho sĩ ghét Pháp gia vì thái độ khinh miệt của nó với đạo đức và giới học sĩ, nhưng các triều đại vẫn dùng nhiều ý tưởng của dòng này (Pines, SEP). Ngày nay Hàn Phi được đọc lại như một nhà hiện thực chính trị: người hỏi thẳng một thể chế phải được thiết kế thế nào để vận hành được cả khi người cầm quyền chỉ là người bình thường.",
],
"works": [
("TK 3 TCN", "*Hàn Phi Tử* (韓非子)", "55 thiên còn nguyên vẹn; có học giả cho rằng không phải thiên nào cũng do một tay ông viết"),
("", "“Ngũ đố” (五蠹, thiên 49)", "Năm loài mọt hại nước; thời thế đổi thì cách trị phải đổi"),
("", "“Nạn thế” (難勢, thiên 40)", "Bàn về quyền thế và người cầm quyền bình thường"),
("", "“Định pháp” (定法, thiên 43)", "Hợp nhất “pháp” của Thương Ưởng với “thuật” của Thân Bất Hại"),
("", "“Giải Lão” (解老, thiên 20) và “Dụ Lão” (喻老, thiên 21)", "Giải thích và minh họa *Lão Tử*: lời chú giải xưa nhất còn lại của sách này"),
],
"thoughts": [
"**Pháp, thuật, thế.** Pháp (法) là luật lệ công bố ở quan phủ, thưởng phạt chắc chắn; thuật (術) là cách vua giao việc theo năng lực, “theo danh mà đòi thực”, xét xem lời hứa của quan có khớp việc làm không (thiên 43); thế (勢) là uy quyền gắn với ngôi vị (thiên 40).",
"**Hai cái cán.** Vua nắm hai “cán” là hình (phạt) và đức (thưởng) (thiên 7 “Nhị bính”); để quan lại nắm thay thì dân sẽ sợ quan mà coi thường vua. Con người ham lợi, sợ hại, nên cứ đặt thưởng phạt cho đúng thì không cần trông vào lòng tốt. Với Hàn Phi, đến tình thương của cha mẹ cũng không dạy nổi đứa con hư, phải đợi uy của quan lại (thiên 49).",
"**Ôm cây đợi thỏ.** Một người nước Tống thấy con thỏ chạy đâm vào gốc cây gãy cổ, bèn bỏ cày ngồi canh gốc cây chờ thỏ khác, thành trò cười cho cả nước. Muốn lấy phép trị của các vua xưa để trị dân đời nay cũng thế (thiên 49 “Ngũ đố”). Lý do: xưa người ít của nhiều nên dân không tranh; nay một người năm con, ông nội chưa mất đã có hai mươi lăm cháu, người đông của ít thì dân tranh nhau.",
"**Vị vua như một cỗ máy.** Vua lý tưởng của Hàn Phi giấu kín cảm xúc, không tự mình xen vào, chỉ để luật và thưởng phạt vận hành. A. C. Graham nhận xét nửa đùa rằng vị vua ấy không làm việc gì mà một chiếc máy tính sơ đẳng không làm được (theo Pines, SEP), một câu hỏi rất thời sự trong thời quản trị bằng thuật toán.",
],
"argument": {
"title": "Đừng chờ Nghiêu, Thuấn — thể chế cho người cầm quyền bình thường (thiên 40 “Nạn thế”)",
"intro": "Thiên “Nạn thế” là một cuộc tranh luận về quyền thế. Người phản bác nói: quyền thế trong tay vua hiền thì thiên hạ trị, trong tay bạo chúa thì loạn, nên rốt cuộc vẫn phải chờ người hiền. Hàn Phi đáp:",
"premises": [
"Vua thánh như Nghiêu, Thuấn hay bạo chúa như Kiệt, Trụ “nghìn đời mới có một”; người cầm quyền phổ biến là hạng trung, không bằng Nghiêu, Thuấn mà cũng không tệ như Kiệt, Trụ.",
"Với người hạng trung, “ôm pháp, giữ thế thì trị; bỏ pháp, rời thế thì loạn”.",
"Bỏ pháp mà chờ Nghiêu, Thuấn thì nghìn đời loạn mới được một đời trị; giữ pháp mà gặp Kiệt, Trụ thì nghìn đời trị mới có một đời loạn.",
],
"conclusion": "Chính trị phải dựa vào pháp và thế, được thiết kế cho người cầm quyền bình thường, chứ không chờ thánh nhân; chờ Nghiêu, Thuấn để trị dân hôm nay khác gì nhịn đói trăm ngày để chờ cơm thịt.",
"objection": "Chính người phản bác trong thiên đã nói: trao quyền thế cho kẻ bất tài là “chắp cánh cho hổ”. Hệ thống của Hàn Phi giữ cho bộ máy chạy đều, nhưng không có gì buộc chính nhà vua phải theo luật. Nhà Tần dựng theo đường lối Pháp gia sụp đổ chưa đầy mười lăm năm sau khi thống nhất. Còn người theo Khổng Tử sẽ nhắc *Luận ngữ* 2.3: dân chỉ sợ phạt thì tránh tội mà không biết hổ thẹn.",
"reply": "Người bênh vực Hàn Phi ngày nay giữ phần lõi của lập luận và đẩy nó đi xa hơn chính ông: nếu không được giả định người cầm quyền là thánh, thì cũng không được giả định nhà vua đứng ngoài luật. Áp dụng triệt để nguyên tắc “thiết kế cho người bình thường” vào chính kẻ cầm quyền, ta đi tới ý tưởng nhà nước pháp quyền: hiến pháp, phân quyền, bầu cử định kỳ, những cơ chế để thể chế vẫn chạy khi người đứng đầu không giỏi.",
},
"quote": {
"source": "Hàn Phi, *Hàn Phi Tử*, thiên 6 “Hữu độ” (有度) — nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "法不阿貴，繩不撓曲。法之所加，智者弗能辭，勇者弗敢爭。刑過不避大臣，賞善不遺匹夫。 — Pháp bất a quý, thằng bất nạo khúc. Pháp chi sở gia, trí giả phất năng từ, dũng giả phất cảm tranh. Hình quá bất tị đại thần, thưởng thiện bất di thất phu.",
"vi": "Pháp luật không nể kẻ sang, dây mực không uốn theo chỗ cong. Pháp đã áp vào thì kẻ khôn không chối được, kẻ mạnh không dám cãi. Phạt lỗi không chừa đại thần, thưởng điều thiện không bỏ sót kẻ thường dân.",
"url": "https://ctext.org/hanfeizi/you-du/zh",
},
"misread": [
"**“Pháp trị của Hàn Phi chính là nhà nước pháp quyền.”** Thực ra luật của Hàn Phi là công cụ để vua cai trị, và nhà vua đứng trên luật. Cần phân biệt *rule by law* (cai trị bằng luật) với *rule of law* (luật đứng trên mọi người, kể cả người cầm quyền). Pines (SEP) còn lưu ý rằng chữ *pháp* (法) không chỉ là luật mà còn là khuôn mẫu, tiêu chuẩn, phương pháp.",
"**“Hàn Phi sáng lập Pháp gia.”** Thực ra “Pháp gia” (法家) là cái nhãn do Tư Mã Đàm, cha của Tư Mã Thiên, đặt ra hơn một thế kỷ sau, chủ yếu để xếp loại sách; không nhà tư tưởng nào thời ấy tự nhận mình thuộc “Pháp gia”. Hàn Phi tự coi mình là người tổng hợp và sửa chữa những người đi trước như Thương Ưởng, Thân Bất Hại, Thận Đáo (Pines, SEP).",
],
"related": [
("cau-hoi/duc-tri.md", "Cai trị bằng đức hay bằng pháp?"),
("lich-su/trung-hoa.md", "Trung Hoa: trăm nhà đua tiếng"),
("doc/dao-duc-kinh.md", "Hướng dẫn đọc Đạo đức kinh"),
],
"sources": [
("Pines, Yuri, “Legalism in Chinese Philosophy”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/chinese-legalism/"),
("*Hàn Phi Tử* (韓非子), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/hanfeizi"),
("Tư Mã Thiên, *Sử ký*, “Lão Tử Hàn Phi liệt truyện” (老子韓非列傳), nguyên văn chữ Hán, ctext.org.", "https://ctext.org/shiji/lao-zi-han-fei-lie-zhuan/zh"),
("Goldin, Paul R., “Xunzi”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/xunzi/"),
("Chan, Alan, “Laozi”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/laozi/"),
],
},
"chu-hy": {
"desc": "Chu Hy, nhà tổng hợp Tân Nho giáo đời Tống: lý và khí, cách vật trí tri, bộ Tứ thư, thứ triết học đã thành chương trình học của sĩ tử Đông Á.",
"bio": [
"Tương truyền năm lên năm, cậu bé Chu Hy đã hỏi bên ngoài trời là gì. Lớn lên ông vẫn giữ cái tò mò ấy: thấy vỏ sò ốc nằm trong đá trên núi cao, ông đoán chỗ ấy xưa là đáy nước, “chỗ thấp đổi thành cao, chất mềm đổi thành cứng” (*Chu Tử ngữ loại*, quyển 94). Ông sinh năm 1130 ở Phúc Kiến, thời Nam Tống, khi triều đình vừa mất miền Bắc vào tay người Nữ Chân, và nỗi nhục ấy phủ bóng lên tư tưởng chính trị cả một thời (Tiwald, SEP).",
"Cha mất sớm, ông theo học mấy người bạn của cha, những học giả đọc cả sách Phật, sách Lão. Ông học Thiền với một nhà sư, đỗ tiến sĩ khi chưa đầy hai mươi tuổi, và theo SEP, bài thi còn dùng ý Thiền. Phải đến khi chính thức theo học Lý Đồng (1093–1163), người thuộc dòng học của anh em họ Trình, ông mới dứt khoát quay về đạo Nho. Ông làm quan không nhiều; vì bất đồng với triều đình, ông thường xin giữ những chức trông coi đền miếu nhàn tản để có thì giờ đọc sách, viết sách và dạy hàng trăm, có lẽ hàng nghìn học trò.",
"Việc lớn của ông là tổng hợp. Ông gom ý tưởng của các bậc thầy Bắc Tống, Chu Đôn Di, Trương Tái, Trình Hạo, Trình Di, thành một hệ thống nối liền vũ trụ, bản tính con người và con đường tu dưỡng. Ông chọn bốn văn bản *Đại học*, *Luận ngữ*, *Mạnh Tử*, *Trung dung*, chú giải thành bộ *Tứ thư*. Từ năm 1313, nhà Nguyên lấy cách hiểu kinh điển của ông làm chuẩn cho khoa cử, và cho tới khi khoa cử bị bãi bỏ đầu thế kỷ 20, hàng triệu sĩ tử đã học Nho giáo qua lời chú của ông (Tiwald, SEP).",
"Ảnh hưởng ấy lan sang Triều Tiên, Nhật Bản và Việt Nam. Nhưng Chu Hy không chỉ là người giữ kinh: đối thủ cùng thời là Lục Cửu Uyên, và ba thế kỷ sau là Vương Dương Minh, cãi với ông kịch liệt về chuyện cái lý của đạo đức nằm ở đâu, trong sự vật hay trong lòng người. Cuộc tranh luận giữa “lý học” và “tâm học” ấy, theo Justin Tiwald (SEP), vẫn định hình phần lớn cách người ta bàn về Nho giáo ở Đông Á ngày nay.",
],
"works": [
("cuối TK 12", "*Tứ thư chương cú tập chú* (四書章句集注)", "Chú giải bốn sách *Đại học*, *Luận ngữ*, *Mạnh Tử*, *Trung dung*; từ năm 1313 thành chuẩn khoa cử"),
("TK 12", "*Cận tư lục* (近思錄)", "Tuyển lời các bậc thầy Bắc Tống: Chu Đôn Di, Trương Tái, anh em họ Trình"),
("sau 1200", "*Chu Tử ngữ loại* (朱子語類)", "Ghi chép lời giảng và đối đáp với học trò, được xếp theo chủ đề sau khi ông mất"),
("", "*Chu Tử văn tập* (朱子文集)", "Thơ, văn, thư từ, trong đó có các thư tranh luận về tu dưỡng"),
],
"thoughts": [
"**Lý và khí.** Theo Chu Hy, mọi vật đều có lý (理), cái khuôn mẫu, cái lẽ khiến nó là nó, và khí (氣), chất liệu cụ thể làm nên hình hài của nó. Nói nôm na: thuyền nào cũng khác nhau về gỗ, về dáng, nhưng chiếc nào cũng phải theo cái lẽ đi được trên nước. Lý của muôn vật rốt cuộc quy về một, gọi là Thái cực.",
"**Tính người là lý.** Theo Mạnh Tử, Chu Hy tin bản tính con người vốn tốt; nhưng mỗi người bẩm thụ một thứ khí khác nhau, lại sống trong gia đình, hoàn cảnh khác nhau, nên có người dễ thành người tốt, có người khó, và ai cũng có thể sa vào điều xấu (Thompson, SEP). Tu dưỡng là làm cho cái lý vốn có ấy sáng ra.",
"**Kính và học.** Tu dưỡng đi bằng hai chân: giữ lòng chăm chú, kính cẩn (kính 敬), và xét cái lý của sự vật cho tới cùng. Cuối đời ông nhấn mạnh trước hết phải lập chí, quyết tâm làm người quân tử (Thompson, SEP).",
],
"argument": {
"title": "Cách vật trí tri — muốn biết, hãy đi vào từng sự vật",
"intro": "Sách *Đại học* nói mở mang hiểu biết là ở chỗ “cách vật”, xét đến sự vật, nhưng đoạn giải thích đã mất. Chu Hy viết bổ vào một đoạn, nói rõ là “trộm lấy ý của Trình Tử”, và đoạn ấy chứa một lập luận gọn:",
"premises": [
"Lòng người linh diệu, không ai không có khả năng biết.",
"Vật trong thiên hạ, không vật nào không có lý của nó.",
"Hiểu biết của ta còn chưa trọn chỉ vì lý của sự vật còn chưa được xét cho cùng.",
],
"conclusion": "Vậy muốn mở mang hiểu biết, phải đến với từng sự vật, dựa vào cái lý đã biết mà xét thêm cho tới cùng; dụng công lâu ngày, sẽ có lúc “bỗng nhiên thông suốt” (khoát nhiên quán thông).",
"objection": "Ba thế kỷ sau, Vương Dương Minh (1472–1529) thử “cách” những khóm trúc trước nhà để tìm lý của trúc, nghĩ mãi mà chẳng được gì, rồi gạt bỏ hẳn phương pháp của Chu Hy (Thompson, SEP); ông đi tới chỗ cho rằng lý ở ngay trong tâm. Trước đó, đối thủ cùng thời Lục Cửu Uyên tin vào trực giác đạo đức: tâm đã chứa lý, cần gì đi tìm khắp muôn vật? Con đường của Chu Hy, theo họ, vừa vụn vặt vừa xa vời.",
"reply": "Người theo Chu Hy đáp: “cách vật” không phải nhìn chằm chằm vào khóm trúc, mà chủ yếu là đọc sách, suy xét việc người, quan sát tự nhiên, đi cùng một thái độ chăm chú, kính cẩn. Chu Hy cho rằng trực giác một mình không đủ để xử lý những việc phức tạp của đời người, vì nhiều tình huống đòi hỏi cách ứng xử may đo riêng (Thompson, SEP). Và chính ông đã dùng lối nghĩ ấy khi từ vỏ sò trên núi suy ra núi xưa từng là đáy nước.",
},
"quote": {
"source": "Chu Hy, *Chu Tử ngữ loại* (朱子語類), quyển 94, lời đáp học trò về Thái cực — nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "本只是一太極，而萬物各有稟受，又自各全具一太極爾。如月在天，只一而已；及散在江湖，則隨處而見，不可謂月已分也。 — Bản chỉ thị nhất Thái cực, nhi vạn vật các hữu bẩm thụ, hựu tự các toàn cụ nhất Thái cực nhĩ. Như nguyệt tại thiên, chỉ nhất nhi dĩ; cập tán tại giang hồ, tắc tùy xứ nhi kiến, bất khả vị nguyệt dĩ phân dã.",
"vi": "Vốn chỉ có một Thái cực, nhưng muôn vật mỗi vật đều bẩm thụ, lại mỗi vật tự có đủ trọn một Thái cực. Như mặt trăng trên trời chỉ có một mà thôi; khi rải xuống sông hồ thì chỗ nào cũng thấy, không thể nói rằng mặt trăng đã bị chia ra.",
"url": "https://ctext.org/zhuzi-yulei/94/zh",
},
"misread": [
"**“Cách vật trí tri là nghiên cứu khoa học thực nghiệm.”** Thực ra với Chu Hy, lý vừa là lẽ của tự nhiên vừa là chuẩn mực đạo đức, và việc “cách vật” chủ yếu là đọc kinh điển, suy xét việc người. Ông có nhiều quan sát tự nhiên sắc sảo, về tuần trăng, nhật thực, sự hình thành trời đất, nhưng theo SEP những giải thích ấy chưa đủ chặt để thành giả thuyết khoa học.",
"**“Chu Hy chỉ là nhà chú giải bảo thủ.”** Thực ra ông là một nhà tổng hợp táo bạo: ông chọn lại kinh điển, đặt *Tứ thư* vào trung tâm việc học, tự viết thêm đoạn giải thích cho *Đại học*, và theo SEP có lẽ còn chịu ảnh hưởng lối nhìn toàn thể của Phật giáo Hoa Nghiêm khi dựng hệ thống. Vị thế “chính thống” là do triều đình đời sau trao cho tư tưởng của ông.",
],
"related": [
("cau-hoi/nho-giao-viet.md", "Nho giáo Việt Nam: tiếp thu hay sáng tạo?"),
("lich-su/trung-hoa.md", "Trung Hoa: trăm nhà đua tiếng"),
("lich-su/nhat-ban-viet-nam.md", "Nhật Bản và Việt Nam: triết học ở phương Đông"),
],
"sources": [
("Thompson, Kirill, “Zhu Xi”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/zhu-xi/"),
("Tiwald, Justin, “Song-Ming Confucianism”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/song-ming-confucianism/"),
("Chu Hy, *Đại học chương cú* (大學章句), đoạn bổ truyện chương 5 về cách vật trí tri, nguyên văn chữ Hán, Wikisource tiếng Trung.", "https://zh.wikisource.org/wiki/%E5%9B%9B%E6%9B%B8%E7%AB%A0%E5%8F%A5%E9%9B%86%E6%B3%A8/%E5%A4%A7%E5%AD%B8%E7%AB%A0%E5%8F%A5"),
("*Chu Tử ngữ loại* (朱子語類), quyển 94, nguyên văn chữ Hán, ctext.org.", "https://ctext.org/zhuzi-yulei/94/zh"),
],
},
"duc-phat": {
"desc": "Người sáng lập Phật giáo, đọc như một triết gia: khổ có nguyên nhân nên có thể chấm dứt, và cái “tôi” bất biến mà ta bám vào thật ra không có.",
"bio": [
"Một người trẻ con nhà quyền quý thuộc dòng họ Thích Ca (*Śākya*), ở vùng nay là biên giới Ấn Độ – Nepal, bỏ lại nhà cửa, vợ và đứa con nhỏ để đi tìm câu trả lời cho một câu hỏi: vì sao con người khổ, và có cách nào hết khổ không? Truyền thống kể như vậy về Siddhartha Gautama (Tất-đạt-đa Cồ-đàm), người về sau được gọi là Đức Phật — “người đã tỉnh thức”. Ông theo học các nhà tu khổ hạnh du phương (*śramaṇa*), thấy chưa thỏa, bèn tự đi con đường riêng. Sau khi giác ngộ, ông giảng bài pháp đầu tiên cho năm nhà tu khổ hạnh ở vườn nai Isipatana gần Varanasi, rồi dành bốn mươi lăm năm còn lại đi dạy học; theo truyền thống, ông mất năm tám mươi tuổi.",
"Ông sống vào khoảng nào? Không ai biết chắc. Truyền thống Phật giáo Nam tông (*Theravāda*) tính rằng ông nhập diệt năm 544 hoặc 543 TCN. Học giới phương Tây từ giữa thế kỷ 19 đến cuối thế kỷ 20 thường ghi khoảng 560–480 TCN. Sau một hội thảo quốc tế ở Göttingen năm 1988, sự đồng thuận ấy tan vỡ; phần đông học giả nay đặt cuộc đời ông muộn hơn chừng một thế kỷ, nhiều người cho rằng ông mất quanh năm 400 TCN. Trang này theo mốc sau cùng ấy. Ông cũng không viết gì: lời giảng được tăng đoàn thuộc lòng, truyền miệng qua nhiều thế kỷ rồi mới chép thành văn, nên “Đức Phật nghĩ gì” luôn là Đức Phật qua cách hiểu của các thế hệ sau.",
"Điều làm ông thành một triết gia là cách ông lập luận. Ông chẩn đoán như một thầy thuốc: có khổ; khổ có nguyên nhân; vì có nguyên nhân nên khổ có thể chấm dứt; và có con đường để chấm dứt nó. Nguyên nhân sâu nhất, theo ông, là sự lầm tưởng rằng có một cái “tôi” và những thứ “của tôi”, từ đó sinh ra bám víu, thèm khát, ghét bỏ. Ông gọi lời dạy của mình là trung đạo: giữa hưởng thụ dục lạc và tự hành xác, giữa tin rằng ta tồn tại mãi mãi và tin rằng chết là hết.",
"Hai nghìn rưỡi năm sau, những câu hỏi ấy vẫn nằm giữa triết học. Khi Derek Parfit bênh vực quan niệm quy giản về con người trong *Reasons and Persons* (1984), ông viết rằng Đức Phật hẳn sẽ đồng ý, và dành hẳn một phụ lục để dẫn các văn bản Phật giáo. Ở Việt Nam, từ các thiền sư đời Lý đến thiền phái Trúc Lâm đời Trần, tư tưởng của ông đã thành một phần của văn hóa. Mỗi khi ai đó khuyên “buông bỏ cho nhẹ lòng”, họ đang nói — có khi không biết — một phiên bản rút gọn của chẩn đoán ấy. Trang này mời bạn đọc bản đầy đủ, cùng các lý lẽ của nó.",
],
"works": [
("", "*Nikāya* (tiếng Pāli) và *A-hàm* (bản chữ Hán)", "các bộ kinh ghi lời giảng của Đức Phật, do tăng đoàn thuộc lòng, truyền miệng nhiều thế kỷ rồi mới chép thành văn; nguồn chính để tái dựng tư tưởng của ông"),
("", "*Kinh Chuyển pháp luân* (*Dhammacakkappavattana Sutta*, SN 56.11)", "bài giảng đầu tiên: hai cực đoan, trung đạo, Tứ diệu đế, Bát chánh đạo"),
("", "*Kinh Vô ngã tướng* (*Anattalakkhaṇa Sutta*, SN 22.59)", "“bài giảng thứ hai”: hai lập luận rằng năm uẩn không phải là tự ngã"),
("", "*Kinh Ca-chiên-diên* (*Kaccānagotta Sutta*, SN 12.15)", "trung đạo giữa “tất cả đều có” và “tất cả đều không”"),
("", "*Tiểu kinh Māluṅkya* (*Cūḷamāluṅkya Sutta*, MN 63)", "vì sao ông gác lại các câu hỏi siêu hình: dụ mũi tên tẩm độc"),
],
"thoughts": [
"**Tứ diệu đế** (*Four Noble Truths*) là một chẩn đoán: có khổ; khổ có nguyên nhân; nguyên nhân dứt thì khổ dứt; có con đường (Bát chánh đạo) để làm việc ấy. “Khổ” (*dukkha*) không chỉ là đau đớn mà là sự bất toại của mọi thứ vô thường — kể cả những niềm vui ta sợ mất.",
"**Duyên khởi** (*paṭiccasamuppāda*): mọi thứ sinh ra khi đủ điều kiện và mất đi khi điều kiện mất. Vì khổ sinh ra từ điều kiện, nó không phải định mệnh: đổi điều kiện (vô minh, tham ái) thì đổi được kết quả. Chuỗi “mười hai nhân duyên” quen thuộc, theo giới nghiên cứu, là do đời sau hệ thống hóa.",
"**Vô ngã** (*anattā*): trong thân và tâm không có một cái “tôi” thường hằng, tự chủ. Truyền thống về sau nói rõ bằng hai tầng chân lý: ở tầng quy ước vẫn có “người”, có trách nhiệm; ở tầng tối hậu chỉ có một dòng thân–tâm nối tiếp. Lầm tầng này với tầng kia là gốc của bám víu.",
"**Trung đạo**: tránh cả thường kiến (cái tôi tồn tại mãi) lẫn đoạn kiến (chết là hết), vì cả hai cùng giả định có một cái tôi để còn hay mất. Hỏi người giác ngộ sau khi chết đi đâu, theo ông, giống như hỏi ngọn lửa tắt rồi đi về hướng nào: câu hỏi dựa trên một tiền giả định sai.",
"**Gác lại siêu hình học vô ích**: ông không trả lời những câu như vũ trụ có vĩnh cửu không, ví người đòi được trả lời rồi mới chịu tu với kẻ trúng tên độc mà không cho rút tên khi chưa biết ai bắn (MN 63). Nhưng khi cần, như về vô ngã, ông lập luận rất chặt.",
],
"argument": {
"title": "Không có cái “tôi” thường hằng",
"intro": "Trong *Kinh Vô ngã tướng* (SN 22.59), Đức Phật lần lượt hỏi năm vị tỳ-kheo: thân xác, cảm giác, tri giác, các tâm hành, ý thức — cái nào thường còn? Mark Siderits (SEP) tái dựng phần này thành “lập luận từ vô thường”:",
"premises": [
"Nếu có một cái “tôi” (tự ngã) đúng nghĩa, nó phải thường còn — đủ bền để làm nên sự đồng nhất của một người qua thời gian, kể cả qua nhiều đời.",
"Con người không gồm gì khác ngoài năm uẩn: sắc (thân), thọ (cảm giác), tưởng (tri giác), hành (ý chí, thói quen), thức (ý thức). Đây là tiền đề ngầm.",
"Không uẩn nào thường còn: thân chỉ tồn tại trong một đời; cảm giác, tri giác, ý thức sinh ra khi giác quan gặp đối tượng và mất đi cùng lần gặp ấy.",
],
"conclusion": "Vậy không có cái “tôi” thường hằng; “tôi” chỉ là cái tên tiện dụng cho một dòng thân–tâm luôn đổi thay.",
"objection": "Chỗ yếu là tiền đề ngầm. Các trường phái Ấn Độ tin vào tự ngã (*ātman*) đáp rằng dĩ nhiên tự ngã không nằm trong những gì quan sát được: nó là chủ thể đứng sau mọi kinh nghiệm. Phái Sāṃkhya còn lập luận rằng chính việc ta điều khiển được thân và tâm cho thấy phải có một chủ thể vượt ngoài chúng. Một số học giả hiện đại, như Miri Albahari, cũng lưu ý rằng Đức Phật chưa bao giờ phủ nhận thẳng một tự ngã nằm ngoài năm uẩn.",
"reply": "Người theo hướng Đức Phật đáp: đặt ra một thực thể không ai quan sát được chỉ để giải thích kinh nghiệm là một bước không có căn cứ. Trong *Kinh Poṭṭhapāda* (DN 9), ông ví người đặt ra một “kẻ thấy” vô hình với người đem lòng mê người phụ nữ đẹp nhất thế gian chỉ vì nghĩ rằng hẳn phải có người như thế. Và các triết gia Ấn Độ cổ điển, cả Phật giáo lẫn chính thống, đều hiểu ông là người phủ nhận tự ngã hoàn toàn.",
},
"quote": {
"source": "*Kinh Vô ngã tướng* (SN 22.59) — bản dịch tiếng Anh của Bhikkhu Sujato, SuttaCentral (CC0)",
"orig": "Mendicants, form is not-self. For if form were self, it wouldn’t lead to affliction. And you could compel form: ‘May my form be like this! May it not be like that!’",
"vi": "Này các tỳ-kheo, sắc (thân) không phải là tự ngã. Vì nếu sắc là tự ngã, nó đã không dẫn tới bệnh khổ, và ta có thể ra lệnh cho nó: ‘Thân ta hãy như thế này! Đừng như thế kia!’",
"url": "https://suttacentral.net/sn22.59/en/sujato",
},
"misread": [
"**“Phật giáo bi quan: đời là khổ.”** Thực ra “khổ” là một chẩn đoán chứ không phải bản án: chân lý thứ ba nói khổ có thể chấm dứt, chân lý thứ tư chỉ đường. Chữ *dukkha* cũng rộng hơn “đau đớn”: nó chỉ sự bất toại của mọi thứ vô thường, kể cả những niềm vui mà ta sợ mất.",
"**“Vô ngã nghĩa là không có ai cả, nên chẳng ai phải chịu trách nhiệm.”** Thực ra Đức Phật vẫn dạy về nghiệp, và nhấn mạnh rằng nghiệp là ý định (*cetanā*) chứ không phải cử động bên ngoài — tức đặt trách nhiệm đạo đức vào trung tâm. Điều ông phủ nhận là một cái “tôi” bất biến đứng sau dòng thân–tâm, không phủ nhận con người ở tầng quy ước.",
],
"related": [
("lich-su/an-do.md", "Ấn Độ: giải thoát khỏi khổ đau"),
("cau-hoi/cai-toi.md", "Cái 'tôi' là gì? Bạn của mười năm trước có còn là bạn?"),
("cau-hoi/truc-lam.md", "Thiền phái Trúc Lâm: Phật giáo nhập thế thời Trần"),
],
"sources": [
("Siderits, Mark, “Buddha”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/buddha/"),
("Velez, Abraham, “Buddha”, *Internet Encyclopedia of Philosophy* (mục 1a về niên đại).", "https://iep.utm.edu/buddha/"),
("*Kinh Vô ngã tướng* (SN 22.59), *Kinh Chuyển pháp luân* (SN 56.11), *Kinh Ca-chiên-diên* (SN 12.15), *Tiểu kinh Māluṅkya* (MN 63) — nguyên văn Pāli và bản dịch tiếng Anh của Bhikkhu Sujato (CC0), SuttaCentral.", "https://suttacentral.net/sn22.59/en/sujato"),
("Bechert, Heinz (chủ biên), *The Dating of the Historical Buddha / Die Datierung des historischen Buddha*, 3 tập, Göttingen: Vandenhoeck & Ruprecht, 1991–1997.", ""),
("Parfit, Derek, *Reasons and Persons*, Oxford: Clarendon Press, 1984, tr. 273 và Phụ lục J.", ""),
],
},
"nagarjuna": {
"desc": "Nhà triết học Phật giáo lớn nhất sau Đức Phật: không gì có tự tính, và chính vì thế mà mọi thứ — kể cả giải thoát — mới có thể xảy ra.",
"bio": [
"Các nhà Phật học trước Nagarjuna đã quen với một phép thử: “cái xe” ở đâu? Không phải bánh, không phải trục, không phải thùng xe; tháo rời ra thì chẳng còn “cái xe” nào, nên “xe” chỉ là một cái tên tiện dụng. Nhưng họ dừng lại ở những thành phần cuối cùng — các “pháp” — mà họ tin là có thật, tự mình mà có. Nagarjuna (tên Hán Việt là Long Thụ, cũng đọc Long Thọ) hỏi tiếp: vậy những thành phần ấy thì sao? Câu trả lời của ông làm rung chuyển triết học Ấn Độ: không có tầng nền móng nào cả.",
"Về cuộc đời ông, ta biết rất ít. Hầu như chắc chắn ông là một tăng sĩ Phật giáo sống trong khoảng năm 150–250, phần lớn ở miền Nam Ấn Độ. Các tiểu sử bằng chữ Hán và tiếng Tây Tạng, viết nhiều thế kỷ sau, đầy truyền thuyết: tương truyền ông xuống cung loài rồng (*nāga*) dưới đáy biển mang về các kinh Bát nhã, nên mới có tên như vậy. Vài tác phẩm của ông là thư khuyên một vị vua, có thể thuộc triều Sātavāhana. Phật giáo Tây Tạng và Đông Á tôn ông là “Đức Phật thứ hai”.",
"Tác phẩm chính là *Trung luận* (*Mūlamadhyamakakārikā*), khoảng 450 bài kệ. Ông không dựng một học thuyết mới về thế giới mà làm một việc khác: lần lượt xét quan niệm của đối thủ về nhân quả, chuyển động, thời gian, cái tôi, tri thức, rồi chỉ ra rằng nếu sự vật có **tự tính** (*svabhāva*) — một bản chất tự có, độc lập — thì quan niệm ấy tự mâu thuẫn. Kết luận: mọi pháp đều là **tính không** (*śūnyatā*), trống rỗng tự tính. Ông nhấn mạnh: “không” không có nghĩa là “không có gì”.",
"Tư tưởng của ông ảnh hưởng tới tranh luận triết học Ấn Độ khoảng một nghìn năm, rồi theo Phật giáo sang Tây Tạng, Trung Hoa, Nhật Bản; ở Tây Tạng, một cách đọc ông (phái *Prāsaṅgika*) được coi là đỉnh cao triết học cho đến nay. Ở Đông Á, bản Hán *Trung luận* do Cưu-ma-la-thập dịch đầu thế kỷ 5 là bản được đọc rộng rãi nhất. Hôm nay, các triết gia còn đem ông vào siêu hình học đương đại, chẳng hạn cuộc tranh luận: thực tại có một tầng nền cuối cùng, hay chỉ có những quan hệ phụ thuộc chồng lên nhau mãi?",
],
"works": [
("k. TK 2–3", "*Mūlamadhyamakakārikā*", "*Trung luận*: khoảng 450 bài kệ, tác phẩm chính; bản Hán *Trung luận* (中論) của Cưu-ma-la-thập kèm chú giải của Thanh Mục"),
("", "*Vigrahavyāvartanī*", "*Hồi tránh luận* (“dẹp tan tranh luận”): 70 bài kệ kèm tự chú, trả lời các phản bác nhắm vào tính không"),
("", "*Yuktiṣaṣṭikā*", "*Sáu mươi bài kệ về lý lẽ*: tính không và duyên khởi"),
("", "*Śūnyatāsaptati*", "*Bảy mươi bài kệ về tính không*: tác nhân, hành động và hai chân lý"),
("", "*Ratnāvalī*", "*Tràng hoa quý* (*Bảo hành vương chính luận*): thư khuyên một vị vua về đạo đức và việc trị nước"),
],
"thoughts": [
"**Tự tính** (*svabhāva*) là đích bị phê phán: một bản chất tự có, không phụ thuộc vào nhân duyên, vào bộ phận hay vào khái niệm của ta. Ông lập luận rằng cái gì do duyên mà có thì không thể có tự tính (*Trung luận* 15.1–2).",
"**Tính không** (*śūnyatā*) không phải một thứ “hư không” nằm đâu đó: cái gì do nhiều duyên sinh ra, ông gọi là không; đó là một tên gọi giả lập, cũng chính là trung đạo (24.18). Ngay cả tính không cũng “không” — đừng biến nó thành một quan điểm mới để bám vào.",
"**Trung đạo** giữa hai cực: khẳng định chắc chắn “có” là rơi vào thường kiến, khẳng định chắc chắn “không” là rơi vào đoạn kiến (15.10). Ông dẫn chính lời Đức Phật dạy Ca-chiên-diên: lìa có và lìa không (15.7).",
"**Hai chân lý**: chư Phật dạy dựa trên tục đế (chân lý quy ước) và chân đế (chân lý tối hậu); không nương tục đế thì không đạt được chân đế (24.8–10). Đời thường — đi xe, trả nợ, giữ lời — vẫn vận hành; điều bị bác bỏ là ảo tưởng rằng nó đứng trên một nền móng tự tại.",
"**Phương pháp quy về vô lý**: thay vì dựng hệ thống riêng, ông lấy giả định của đối thủ và cho thấy nó tự mâu thuẫn — chẳng hạn xét bốn cách một vật có thể sinh ra (từ chính nó, từ cái khác, từ cả hai, không do nhân) và bác bỏ cả bốn. Điều sai, theo ông, không phải nhân quả mà là giả định nhân và quả có tự tính.",
],
"argument": {
"title": "Vì duyên khởi nên không có tự tính — và vì thế mọi thứ mới có thể",
"intro": "SEP lưu ý Nagarjuna không có một “lập luận chủ chốt” duy nhất. Nhưng sợi chỉ xuyên suốt *Trung luận*, cùng phản bác lớn nhất và câu trả lời của ông ở chương 24, có thể tái dựng như sau:",
"premises": [
"Nếu một vật có tự tính, nó tồn tại tự nó: không do nhân duyên tạo ra, không phụ thuộc vào vật khác, và vì thế không thể biến đổi (*Trung luận* 15.2, 15.8).",
"Mọi vật đều do duyên khởi — điều mà các đối thủ Phật giáo của ông cũng thừa nhận theo lời Đức Phật.",
],
"conclusion": "Vậy không vật nào có tự tính: mọi pháp đều “không” (*śūnya*).",
"objection": "Ngay trong *Trung luận* (24.1–6), đối thủ — những người tin vào các pháp tối hậu có thật — phản công: nếu tất cả đều không thì không có sinh, không có diệt; vậy không có Tứ diệu đế, không có tu tập, không có quả chứng, cả Phật, Pháp, Tăng cũng sụp đổ; tính không phá luôn nhân quả, tội phúc và mọi lề lối đời thường. Nói gọn: tính không là hư vô.",
"reply": "Nagarjuna lật ngược: chính vì có tính không mà mọi thứ mới thành được (24.14). Nếu sự vật có tự tính cố định thì chúng chẳng cần nhân duyên, nên không thể sinh, không thể diệt; khổ không thể khởi lên mà cũng không thể chấm dứt (24.16–20). Cái lỗi đối thủ gán cho tính không thật ra thuộc về chính thuyết tự tính — như người cưỡi ngựa mà quên mất con ngựa mình đang cưỡi (24.15).",
},
"quote": {
"source": "Nagarjuna, *Trung luận* 24.14 — bản Hán dịch của Cưu-ma-la-thập (đầu thế kỷ 5), nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "以有空義故，一切法得成；若無空義者，一切則不成。 (Dĩ hữu không nghĩa cố, nhất thiết pháp đắc thành; nhược vô không nghĩa giả, nhất thiết tắc bất thành.)",
"vi": "Vì có nghĩa lý của tính không, nên mọi pháp mới thành được; nếu không có nghĩa lý của tính không, thì chẳng gì thành được cả.",
"url": "https://zh.wikisource.org/wiki/%E4%B8%AD%E8%AB%96_(%E4%BD%9B%E6%95%99)/24",
},
"misread": [
"**“Tính không nghĩa là chẳng có gì tồn tại.”** Thực ra Nagarjuna gọi quan điểm “chắc chắn không” là đoạn kiến, sai chẳng kém “chắc chắn có” (*Trung luận* 15.10). “Không” là không có *tự tính*, không phải không có *gì*: chiếc xe vẫn chạy, chỉ là nó không có một bản chất nằm đâu đó độc lập với bánh, khung, động cơ và cách ta gọi tên.",
"**“Nếu mọi thứ là không thì đạo đức, tu tập cũng vô nghĩa.”** Thực ra ông lập luận ngược lại (24.14–20): chỉ trong một thế giới không có tự tính, con người mới thay đổi được — khổ mới có thể dứt, việc tốt mới có thể sinh quả. Ông cũng giữ hai chân lý: không nương chân lý quy ước thì không đạt chân lý tối hậu (24.10).",
],
"related": [
("lich-su/an-do.md", "Ấn Độ: giải thoát khỏi khổ đau"),
("doc/tam-kinh.md", "Hướng dẫn đọc Bát nhã Tâm kinh"),
],
"sources": [
("Westerhoff, Jan Christoph, “Nāgārjuna”, *Stanford Encyclopedia of Philosophy*.", "https://plato.stanford.edu/entries/nagarjuna/"),
("Berger, Douglas, “Nagarjuna (c. 150—c. 250)”, *Internet Encyclopedia of Philosophy*.", "https://iep.utm.edu/nagarjun/"),
("Nagarjuna, *Trung luận* (中論), bản Hán dịch của Cưu-ma-la-thập, chú giải của Thanh Mục, Wikisource tiếng Trung (các chương 15 và 24).", "https://zh.wikisource.org/wiki/%E4%B8%AD%E8%AB%96_(%E4%BD%9B%E6%95%99)"),
("*Kinh Ca-chiên-diên* (*Kaccānagotta Sutta*, SN 12.15), bản dịch tiếng Anh của Bhikkhu Sujato (CC0), SuttaCentral — bài kinh mà *Trung luận* 15.7 dẫn lại.", "https://suttacentral.net/sn12.15/en/sujato"),
],
},
"tue-trung": {
"desc": "Hưng Ninh Vương Trần Tung — vị tướng thời chống Nguyên rồi thành bậc thầy thiền tại gia, người khai tâm cho Trần Nhân Tông bằng những câu trả lời ngược đời.",
"bio": [
"Một bữa tiệc trong cung nhà Trần bày cả cỗ mặn lẫn cỗ chay. Người anh của hoàng hậu, vốn nổi tiếng tu thiền, cứ thản nhiên gắp thịt cá. Hoàng hậu nhắc khẽ: anh tu thiền mà ăn thịt cá thì làm sao thành Phật? Ông cười: Phật là Phật, anh là anh; anh chẳng cần làm Phật, Phật cũng chẳng cần làm anh. Cậu bé Trần Khâm — sau này là vua Trần Nhân Tông — ngồi đó và nhớ mãi. Người anh ấy là Tuệ Trung Thượng Sĩ; chuyện được chính Trần Nhân Tông kể lại trong bài *Thượng Sĩ hành trạng*.",
"Tên thật của ông là Trần Tung, con trưởng của An Sinh Vương Trần Liễu, anh của Hưng Đạo Vương Trần Quốc Tuấn và của hoàng hậu Nguyên Thánh Thiên Cảm — tức là cậu ruột của Trần Nhân Tông. Sau khi cha mất, ông được vua Trần Thái Tông phong Hưng Ninh Vương. Ông cầm quân trong các cuộc kháng chiến chống Nguyên–Mông, được giao trấn giữ vùng cửa biển Thái Bình, rồi lui về ấp riêng ở Tịnh Bang (sau đổi tên là Vạn Niên), chuyên tâm tu thiền tại gia. Ông học thiền với thiền sư Tiêu Dao; vua Trần Thánh Tông kính trọng gọi ông là sư huynh và giao con trai cho ông dạy dỗ. Năm sinh, năm mất lấy theo *Thượng Sĩ hành trạng*: ông mất năm 1291, thọ 62 tuổi.",
"Chính sử *Đại Việt sử ký toàn thư* hầu như không nhắc tới ông, và suốt nhiều thế kỷ ông bị lẫn với Hưng Nhượng Vương Trần Quốc Tảng, con thứ của Hưng Đạo Vương. Nhà nghiên cứu Nguyễn Huệ Chi truy ra nhầm lẫn ấy từ lời chú của Bùi Huy Bích trong *Hoàng Việt văn tuyển*, và từ những năm 1970 đã chứng minh rằng người thầy của thiền phái Trúc Lâm là Trần Tung. Sau khi ông mất, Pháp Loa biên tập lời dạy và thơ của ông thành *Tuệ Trung Thượng Sĩ ngữ lục*, khắc ván ở Yên Tử.",
"Tuệ Trung không làm sư trụ trì, không lập tông phái. Nhưng qua người học trò, ông in dấu lên cả Trúc Lâm: Trần Nhân Tông tả thầy là người “hòa quang đồng trần” — hòa ánh sáng của mình vào bụi trần, chữ của *Đạo đức kinh*. Thơ ông ngang tàng: có bài viết rằng ai tin được chỗ này sẽ bước cao trên đỉnh đầu Phật Tì-lô. Câu hỏi ông để lại vẫn rất đời: ăn chay hay ăn mặn, lễ lạy hay không — hình thức là chính việc tu, hay chỉ là phương tiện mà người ta dễ nhầm thành mục đích?",
],
"works": [
("sau 1291", "*Tuệ Trung Thượng Sĩ ngữ lục* (慧忠上士語錄)", "thơ, kệ, đối đáp thiền và lời bình các công án; Pháp Loa biên tập, khắc ván ở Yên Tử, kèm bài *Thượng Sĩ hành trạng* của Trần Nhân Tông; còn bản in lại năm 1683"),
("", "*Phóng cuồng ngâm*", "khúc ngâm của kẻ “phóng cuồng” chống gậy rong chơi “phương ngoài phương”; có câu “đói thì ăn… mệt thì ngủ…” mà Trần Nhân Tông về sau dùng lại"),
("", "*Phật tâm ca*", "bài ca về tâm Phật: ai tin được chỗ này thì bước cao trên đỉnh đầu Phật Tì-lô"),
("", "*Phàm thánh bất dị*", "“phàm và thánh chẳng khác nhau”: ta, người, phàm, thánh đều mong manh như sương, như chớp"),
],
"thoughts": [
"**Quay về soi chính mình** (*phản quan tự kỷ*): khi Trần Nhân Tông hỏi tông chỉ của thiền, ông đáp đại ý: hãy quay về tự thân mà tìm, điều ấy không thể có được từ người khác.",
"**Phàm thánh chẳng khác**: ta và người, phàm và thánh đều mong manh như sương móc, như sấm chớp; dựng một bức tường giữa “người thường” và “bậc thánh” cũng là một kiểu bám víu.",
"**Không bám hình thức**: “Phật là Phật, anh là anh” — giác ngộ không đo bằng mâm cỗ chay hay mặn. Nhưng ông không biến điều đó thành lời khuyên đại trà cho mọi người.",
"**Hòa quang đồng trần**: sống giữa đời — làm quan, đánh giặc, ở ấp riêng — mà tâm không vướng. Đây là mẫu hình mà thiền phái Trúc Lâm của Trần Nhân Tông kế thừa và gọi là “cư trần lạc đạo”.",
],
"argument": {
"title": "Muốn vượt qua tội phúc, đừng bám vào giới luật",
"intro": "*Thượng Sĩ hành trạng* kể: Trần Nhân Tông hỏi, nếu tội phúc vốn không thật thì công giữ giới để làm gì? Tuệ Trung cười, không đáp; bị nài mãi, ông dặn đừng nói cho kẻ không ra gì, rồi đọc một bài kệ đại ý: giữ giới và nhẫn nhục chỉ chuốc tội chứ chẳng chuốc phúc; muốn vượt qua tội phúc thì đừng giữ giới nhẫn nhục. Tái dựng của Logos Zero:",
"premises": [
"Tội và phúc, phàm và thánh là những cặp phân biệt do tâm đặt ra; theo một bài kệ khác ông đọc cho vua, mọi cảnh đều từ tâm mà sinh, cảnh và tâm đều không thật.",
"Người giữ giới để cầu phúc, tránh tội vẫn đang bám chặt vào chính cặp phân biệt ấy — như người đang yên lại trèo lên cây tìm chỗ nguy.",
"Bám víu là gốc của mê lầm và khổ.",
],
"conclusion": "Vậy giữ giới như một cách “mua phúc” không đưa tới giải thoát; việc cần làm là quay về soi lại chính mình để buông cả tâm phân biệt tội–phúc.",
"objection": "Chính người học trò đã nêu phản bác: nếu không còn tội phúc thì công giữ giới thanh tịnh để làm gì? Đẩy đến cùng, lời dạy này có thể thành giấy phép cho buông thả — ăn thịt uống rượu cũng gọi là tu — và làm rã khuôn phép đạo đức mà cả cộng đồng dựa vào.",
"reply": "Tuệ Trung không giảng điều đó cho mọi người: ông chỉ đọc bài kệ khi bị nài và dặn đừng truyền cho kẻ không ra gì — tức ông biết lời này nguy hiểm với người chưa hiểu. Điều bị phá là tâm cầu phúc sợ tội, không phải lòng tử tế. Chính học trò ông, khi đã là Thượng hoàng, vẫn mở hội lớn ở chùa Phổ Minh, bố thí cho dân nghèo và trao giới cho người đời (*Đại Việt sử ký toàn thư*, năm 1303): giữ giới mà không chấp giới.",
},
"quote": {
"source": "Tuệ Trung Thượng Sĩ, *Phàm thánh bất dị*, hai câu — phiên âm Hán Việt theo Nguyễn Huệ Chi (2014)",
"orig": "Ngã nhân tự lộ diệc tự sương, / Phàm thánh như lôi diệc như điện.",
"vi": "Ta với người: như hạt móc, cũng như giọt sương; / phàm với thánh: như tiếng sấm, cũng như tia chớp.",
"url": "https://vjol.info.vn/ncpt-hue/article/view/16248",
},
"misread": [
"**“Tuệ Trung dạy rằng giới luật vô ích, cứ ăn thịt uống rượu cũng là tu.”** Thực ra ông chỉ đọc bài kệ “đừng giữ giới nhẫn nhục” khi bị nài, kèm lời dặn đừng nói cho kẻ không ra gì; điều ông phá là tâm cầu phúc sợ tội, không phải lòng tử tế. Học trò ông, Trần Nhân Tông, về sau vẫn trao giới cho người đời.",
"**“Tuệ Trung chính là Trần Quốc Tảng, con Hưng Đạo Vương.”** Thực ra đây là nhầm lẫn bắt nguồn từ lời chú của Bùi Huy Bích (1744–1818). Theo khảo cứu của Nguyễn Huệ Chi, *Thượng Sĩ hành trạng* cho biết Tuệ Trung là Hưng Ninh Vương Trần Tung, anh của Hưng Đạo Vương, mất năm 1291 — trong khi Trần Quốc Tảng vẫn còn giữ chức tước trong triều nhiều năm sau đó và mất năm 1313.",
],
"related": [
("cau-hoi/truc-lam.md", "Thiền phái Trúc Lâm: Phật giáo nhập thế thời Trần"),
],
"sources": [
("Nguyễn Huệ Chi, “Trần Tung, một gương mặt lạ trong làng thơ thiền thời Lý–Trần”, *Tạp chí Nghiên cứu và Phát triển* (Huế), số 3–4 (110–111), 2014, tr. 169–190.", "https://vjol.info.vn/ncpt-hue/article/view/16248"),
("Viện Văn học, *Thơ văn Lý–Trần*, tập II, quyển thượng, Hà Nội: NXB Khoa học xã hội, 1989 (phần Tuệ Trung Thượng Sĩ).", ""),
("Trần Thị Minh Trang, “Tuệ Trung Thượng Sĩ and Trúc Lâm Buddhism of Trần Dynasty (13th–14th century)”, *Thang Long Journal of Science: Văn hiến and Heritage*, tập 4, số 1, 2025, tr. 16–26.", "https://vjol.info.vn/ThangLongJournalofScience/article/view/134618"),
("Trần Nhân Tông, *Tán Tuệ Trung Thượng Sĩ* (贊慧忠上士), Wikisource tiếng Việt.", "https://vi.wikisource.org/wiki/T%C3%A1n_Tu%E1%BB%87_Trung_th%C6%B0%E1%BB%A3ng_s%C4%A9"),
("*Đại Việt sử ký toàn thư*, Bản kỷ quyển 6 (năm 1303: Thượng hoàng mở hội ở chùa Phổ Minh, trao giới), nguyên văn chữ Hán, Wikisource tiếng Trung.", "https://zh.wikisource.org/wiki/%E5%A4%A7%E8%B6%8A%E5%8F%B2%E8%A8%98%E5%85%A8%E6%9B%B8/%E6%9C%AC%E7%B4%80%E5%8D%B7%E4%B9%8B%E5%85%AD"),
],
},
"tran-nhan-tong": {
"desc": "Vị vua lãnh đạo kháng chiến chống Nguyên–Mông rồi vào núi Yên Tử tu hành, sáng lập thiền phái Trúc Lâm: “cư trần lạc đạo” — ở giữa bụi trần mà vui với đạo.",
"bio": [
"Đầu năm 1285, quân Nguyên tràn xuống Đại Việt. Giữa lúc thế nước nguy nan, trên một chiếc thuyền, vị vua trẻ đề hai câu thơ ở đuôi thuyền, đại ý: chuyện Cối Kê ngày trước các ngươi nên nhớ, đất Hoan, Diễn vẫn còn mười vạn quân. Mười bốn năm sau, cũng vị vua ấy rời phủ Thiên Trường, vào núi Yên Tử tu khổ hạnh. Ông là Trần Nhân Tông (1258–1308), tên thật Trần Khâm, con trưởng của vua Trần Thánh Tông.",
"Ông lên ngôi năm 1278 và cùng cha (khi ấy là Thượng hoàng) với Hưng Đạo Vương Trần Quốc Tuấn lãnh đạo hai cuộc kháng chiến năm 1285 và 1287–1288. Năm 1293 ông nhường ngôi cho con là Trần Anh Tông. Sau một lần xuất gia ở hành cung Vũ Lâm rồi lại trở về (1295), năm 1299 ông vào Yên Tử, tự hiệu Trúc Lâm Đại Sĩ, và mất năm 1308 ở am Ngọa Vân. Đi tu nhưng ông không rời đời hẳn: năm 1301 ông sang Chiêm Thành và hứa gả con gái là công chúa Huyền Trân cho vua Chiêm; khi cuộc hôn nhân diễn ra năm 1306, nhiều văn nhân trong triều ngoài nội làm thơ Nôm chê trách. Năm 1303 ông mở hội lớn ở chùa Phổ Minh, bố thí cho dân nghèo và trao giới cho người đời.",
"Ông được tôn là vị tổ thứ nhất của thiền phái Trúc Lâm, với hai người kế tục là Pháp Loa và Huyền Quang. Người thầy dạy thiền đầu tiên của ông là cậu ruột, Tuệ Trung Thượng Sĩ, mà ông viết tiểu sử và làm bài tán. Ông viết cả chữ Hán lẫn chữ Nôm. Bài phú Nôm *Cư trần lạc đạo* mười hội, kết bằng bốn câu kệ chữ Hán, là nơi ông nói rõ nhất tư tưởng của mình: Phật ở trong nhà, chẳng phải tìm xa.",
"Sử thần Ngô Sĩ Liên (thế kỷ 15) khen ông nhân từ, gắn kết được lòng dân, là bậc vua hiền của nhà Trần, nhưng chê riêng việc xuất gia là “không hợp đạo trung dung”. Lời khen chê ấy cho thấy câu hỏi ông để lại không chỉ dành cho người tu: một người có thể vừa gánh việc đời vừa giữ được tâm tự do không? Hay “vui với đạo giữa bụi trần” chỉ là đặc quyền của một vị vua đã nhường ngôi?",
],
"works": [
("TK 13–14", "*Cư trần lạc đạo phú* (居塵樂道賦)", "phú chữ Nôm mười hội, kết bằng bài kệ chữ Hán bốn câu: “ở giữa bụi trần mà vui với đạo”"),
("TK 13–14", "*Đắc thú lâm tuyền thành đạo ca*", "bài ca chữ Nôm về niềm vui nơi rừng suối và sự thành đạo, cũng kết bằng kệ chữ Hán"),
("sau 1291", "*Thượng Sĩ hành trạng*", "tiểu sử người thầy Tuệ Trung, in trong *Tuệ Trung Thượng Sĩ ngữ lục*"),
("", "*Thiên Trường vãn vọng* (天長晚望)", "“Ngắm cảnh chiều ở Thiên Trường”: bài thơ chữ Hán tả làng quê, “nửa như có, nửa như không”"),
],
"thoughts": [
"**Phật ở trong nhà**: cái để giác ngộ không ở chùa xa mà ở chính tâm mình; ta đi tìm Bụt chỉ vì quên mất gốc của mình (*Cư trần lạc đạo phú*, hội 5).",
"**“Mình ngồi thành thị, nết dụng sơn lâm”** (hội 1): điều quyết định không phải nơi ta ở mà cách ta sống — thân giữa phố chợ, tâm như ở núi rừng.",
"**Tùy duyên và vô tâm**: “đối cảnh vô tâm” không phải vô cảm mà là tâm không bị cảnh kéo đi; “tùy duyên” không phải buông xuôi mà là làm việc cần làm trong hoàn cảnh của mình.",
"**Đạo không tách khỏi việc đời**: ông vừa là người lãnh đạo kháng chiến vừa là thiền sư; với ông, giữ nước và giữ tâm không phải hai con đường ngược chiều.",
],
"argument": {
"title": "Có thể tu ngay giữa đời",
"intro": "*Cư trần lạc đạo phú* là văn chương chứ không phải chuyên luận, nhưng lập luận ẩn bên trong có thể tái dựng như sau (cách đọc của Logos Zero):",
"premises": [
"Cái để giác ngộ — Phật tính, “báu trong nhà” — có sẵn trong tâm mỗi người: “Bụt ở cong nhà, chẳng phải tìm xa”.",
"Thứ trói buộc ta cũng ở trong tâm: tham ái, thị phi, sự bám víu.",
"Thứ ở trong tâm thì theo ta đến bất cứ đâu — vào chùa cũng như ra chợ.",
],
"conclusion": "Vậy nơi chốn không quyết định việc tu: có thể tu ngay giữa đời — “mình ngồi thành thị, nết dụng sơn lâm”; rời bỏ đời sống không phải điều kiện cần của giác ngộ.",
"objection": "Ngô Sĩ Liên, sử thần Nho giáo thế kỷ 15, phê phán từ phía ngược lại: một bậc vua hiền mà xuất gia là “không hợp đạo trung dung”, người hiền mà làm quá. Phản bác này đánh vào chính ông: nếu tu giữa đời được, sao ông lại lên núi? Và nếu chỉ tâm là quan trọng, người lười biếng cũng có thể gọi sự buông thả của mình là “tùy duyên”.",
"reply": "Người theo Trúc Lâm đáp: “cư trần” không có nghĩa là khỏi cần tu tập, mà là việc tu không bị trói vào nơi chốn; lên núi là một chặng tu, không phải sự trốn đời. Ngay khi đã ở Yên Tử, ông vẫn sang Chiêm Thành lo việc bang giao, vẫn mở hội bố thí cho dân nghèo và trao giới. Còn ranh giới giữa tùy duyên và buông thả nằm ở chữ “vô tâm”: làm việc mà không vướng, chứ không phải không làm gì.",
},
"quote": {
"source": "Trần Nhân Tông, *Cư trần lạc đạo phú*, hội thứ năm — chữ Nôm và phiên âm quốc ngữ theo Wikisource tiếng Việt",
"orig": "孛於宮茹 / 庄沛寻賒 / 因虧本年些寻孛 / 典谷処㐱孛羅些 — Bụt ở cong nhà, chẳng phải tìm xa. Nhân khuây bản nên ta tìm bụt; đến cốc hay chỉn bụt là ta.",
"vi": "Phật ở ngay trong nhà, chẳng phải tìm đâu xa. Vì quên mất gốc của mình nên ta mới đi tìm Phật; đến khi hiểu ra mới biết Phật chính là ta.",
"url": "https://vi.wikisource.org/wiki/C%C6%B0_tr%E1%BA%A7n_l%E1%BA%A1c_%C4%91%E1%BA%A1o_ph%C3%BA/%C4%90%E1%BB%87_ng%C5%A9_h%E1%BB%99i",
},
"misread": [
"**“‘Đói thì ăn, mệt thì ngủ’ là lời khuyên cứ sống tùy thích.”** Thực ra câu này có gốc trong Thiền tông. Theo *Cảnh Đức truyền đăng lục* (1004), khi được hỏi tu thế nào, thiền sư Đại Châu Tuệ Hải đáp “đói đến thì ăn, mệt đến thì ngủ”; hỏi lại mọi người chẳng cũng thế sao, ông nói không: người thường lúc ăn không chịu ăn mà trăm thứ đòi hỏi, lúc ngủ không chịu ngủ mà nghìn điều tính toán. Cái khó là trọn vẹn với việc đang làm, không phải làm gì tùy thích.",
"**“Trúc Lâm là thiền ‘thuần Việt’, không dính gì tới Thiền Trung Hoa.”** Thực ra các hình ảnh then chốt của bài kệ đều có tiền lệ: Mã Tổ từng trách Đại Châu Tuệ Hải bỏ “kho báu nhà mình” mà chạy rong đi tìm; thầy của Trần Nhân Tông, Tuệ Trung, cũng đã viết “đói thì ăn… mệt thì ngủ…”. Cái riêng nằm ở chỗ khác: một ông vua viết điều ấy bằng tiếng Nôm và thử sống nó giữa triều đình, chiến trận.",
],
"related": [
("cau-hoi/truc-lam.md", "Thiền phái Trúc Lâm: Phật giáo nhập thế thời Trần"),
("doc/tho-van-ly-tran.md", "Hướng dẫn đọc Thơ văn Lý–Trần (tuyển)"),
("lich-su/nhat-ban-viet-nam.md", "Nhật Bản và Việt Nam: triết học ở phương Đông"),
],
"sources": [
("*Đại Việt sử ký toàn thư*, Bản kỷ quyển 5–6 (Trần Nhân Tông: sinh 1258, lên ngôi 1278, nhường ngôi 1293, xuất gia 1295 và 1299, sang Chiêm Thành 1301, mất 1308; lời bình của Ngô Sĩ Liên), nguyên văn chữ Hán, Wikisource tiếng Trung.", "https://zh.wikisource.org/wiki/%E5%A4%A7%E8%B6%8A%E5%8F%B2%E8%A8%98%E5%85%A8%E6%9B%B8/%E6%9C%AC%E7%B4%80%E5%8D%B7%E4%B9%8B%E5%85%AD"),
("Trần Nhân Tông, *Cư trần lạc đạo phú* (chữ Nôm, phiên âm), Wikisource tiếng Việt.", "https://vi.wikisource.org/wiki/C%C6%B0_tr%E1%BA%A7n_l%E1%BA%A1c_%C4%91%E1%BA%A1o_ph%C3%BA"),
("Nguyễn Huệ Chi, “Trần Tung, một gương mặt lạ trong làng thơ thiền thời Lý–Trần”, *Tạp chí Nghiên cứu và Phát triển* (Huế), số 3–4 (110–111), 2014.", "https://vjol.info.vn/ncpt-hue/article/view/16248"),
("Đạo Nguyên (biên soạn), *Cảnh Đức truyền đăng lục* (1004), quyển 6 (thiền sư Đại Châu Tuệ Hải), bản Tứ bộ tùng san, Wikisource tiếng Trung.", "https://zh.wikisource.org/wiki/%E6%99%AF%E5%BE%B7%E5%82%B3%E7%87%88%E9%8C%84_(%E5%9B%9B%E9%83%A8%E5%8F%A2%E5%88%8A%E6%9C%AC)/%E5%8D%B7%E7%AC%AC%E5%85%AD"),
],
},
"chu-van-an": {
"desc": "Người thầy nổi tiếng nhất đời Trần: dâng sớ xin chém bảy nịnh thần, không được nghe thì treo mũ về quê — và được thờ ở Văn Miếu.",
"bio": [
"Năm 1370, một ông già chống gậy từ núi Chí Linh về kinh, mừng vị vua vừa được triều thần đón lập sau những tháng ngôi nhà Trần lọt vào tay kẻ khác, rồi lập tức xin về, không nhận tước phong nào. Ít lâu sau ông mất ở nhà. Triều đình truy tặng tên thụy Văn Trinh và cho ông được thờ phối hưởng ở Văn Miếu. Ông là Chu An, người đời sau quen gọi là Chu Văn An.",
"Ông người huyện Thanh Đàm (nay là Thanh Trì, Hà Nội). Chính sử chỉ chép năm mất; năm sinh 1292 lấy theo thần tích đình làng Thanh Liệt, nơi thờ ông làm thành hoàng. *Đại Việt sử ký toàn thư* tả ông cứng cỏi, sống thanh bạch, không cầu danh lợi, ở nhà đọc sách và dạy học. Học trò đầy cửa; nhiều người đỗ đạt làm quan to như Phạm Sư Mạnh, Lê Bá Quát mà mỗi lần về thăm vẫn giữ lễ học trò, được thầy nói chuyện vài câu thì mừng lắm; ai làm điều không phải, ông mắng thẳng, có khi không cho vào. Vua Trần Minh Tông vời ông làm Tư nghiệp Quốc Tử Giám, dạy kinh sách cho thái tử.",
"Dưới thời Trần Dụ Tông, vua ham chơi, bỏ bê việc nước, quyền thần làm càn. Chu An can không được, bèn dâng sớ xin chém bảy tên nịnh thần — người đương thời gọi là *Thất trảm sớ*. Sớ dâng lên không được trả lời; ông treo mũ từ quan, về ở núi Chí Linh, tự hiệu Tiều Ẩn, “người ở ẩn đi kiếm củi”. Khi có đại triều hội, ông vẫn về kinh. Hiến Từ thái hậu nói về ông: người như thế thì không thể bắt làm bề tôi được, ta sao sai khiến nổi. Vua sai người đem áo ban cho; ông lạy tạ xong liền đem cho người khác.",
"Sử thần Ngô Sĩ Liên (thế kỷ 15) xếp ông cùng Tô Hiến Thành là hai người hiếm hoi trong giới Nho nước Việt lấy đạo đức làm chí và lấy việc giúp vua, làm lợi cho dân làm điều tâm niệm; ông khen Chu An thờ vua thì dám nói thẳng, ra làm quan hay lui về đều theo lẽ nghĩa, và gọi ông là bậc “Nho tông” của nước Việt. Tác phẩm của ông gần như mất hết: bộ *Tứ thư thuyết ước* — tóm lược *Tứ thư*, bộ kinh điển do Chu Hy định hình — nay không còn nguyên vẹn; chỉ còn ít thơ chữ Hán. Ngày nay ông là biểu tượng của người thầy, nhưng câu hỏi ông đặt ra là câu hỏi chính trị: khi người cầm quyền làm sai, người có học nên làm gì?",
],
"works": [
("TK 14", "*Thất trảm sớ* (七斬疏)", "tờ sớ xin chém bảy nịnh thần dưới triều Trần Dụ Tông; nguyên văn không còn, chỉ biết qua *Đại Việt sử ký toàn thư*"),
("TK 14", "*Tứ thư thuyết ước* (四書說約)", "tóm lược ý chính *Tứ thư* (*Đại học*, *Trung dung*, *Luận ngữ*, *Mạnh Tử*); nay không còn nguyên vẹn"),
("TK 14", "*Tiều ẩn thi* (樵隱詩)", "thơ chữ Hán của “người ở ẩn đi kiếm củi”; còn lại một số bài"),
],
"thoughts": [
"**Thờ vua bằng đạo, không được thì thôi**: bổn phận của bề tôi là đưa chính sự theo lẽ phải, kể cả khi phải nói điều vua không muốn nghe; can không được thì rút lui chứ không ở lại làm đồng lõa. Đó là nguyên tắc Khổng Tử nói về “bậc đại thần” (*Luận ngữ* 11.24), và Chu An sống đúng như vậy.",
"**Người thầy là người giữ chuẩn**: ông nghiêm với học trò đến mức đuổi người làm điều xấu; với ông, dạy học là đào tạo người giữ được đạo, không chỉ người đỗ đạt.",
"**Rút lui không phải bỏ nước**: ông lui về núi nhưng vẫn về kinh dự đại triều hội, và khi xã tắc lâm nguy (1370) ông về mừng vua mới rồi lại đi — giữ khoảng cách với quyền lực mà không quay lưng với đất nước.",
"**Khí tiết hơn chức tước**: từ chối chức vụ, đem áo vua ban cho người khác — những cử chỉ nhỏ ấy là cách ông nói rằng phẩm giá không mua được.",
],
"argument": {
"title": "Can gián rồi lui về: bổn phận của bề tôi theo đạo",
"intro": "Chu An không để lại văn bản lý luận nào (tờ sớ đã mất). Nhưng hành động của ông có thể đọc như một lập luận, dựa trên nguyên tắc Khổng Tử nói trong *Luận ngữ* 11.24: bậc đại thần thờ vua bằng đạo, không được thì thôi. Tái dựng của Logos Zero:",
"premises": [
"Bề tôi phục vụ nhà vua là để đưa chính sự theo đạo, tức theo lợi ích của dân, chứ không phải để chiều ý người cầm quyền.",
"Khi chính sự trái đạo, bổn phận đầu tiên là nói thẳng, kể cả điều làm vua phật ý.",
"Nếu đã can mà vua không nghe, ở lại hưởng lộc là góp tay vào cái sai và làm mất sức nặng của chính lời can.",
],
"conclusion": "Vậy phải can gián đến cùng; can không được thì từ quan — và tiếp tục giữ đạo bằng con đường khác: dạy học, giữ khí tiết.",
"objection": "Rút lui là bỏ trận địa cho kẻ xấu. Nếu người ngay đều về quê, triều đình chỉ còn nịnh thần; ở lại, dù phải nhẫn nhịn, vẫn cứu được phần nào. Chính Ngô Sĩ Liên ghi nhận cái giá ấy khi chê Dụ Tông: Chu An đi rồi, không còn ai nói điều phải với vua. Một câu hỏi khác: xin vua chém bảy người bằng một tờ sớ, liệu có phải cũng là một cách dùng bạo lực chính trị?",
"reply": "Người bênh vực ông đáp: “không được thì thôi” không phải bỏ cuộc mà là từ chối hợp thức hóa cái sai; uy tín của sự từ chối ấy là một sức ép thật — đến thái hậu cũng phải nói không thể bắt ông làm bề tôi. Ông cũng không quay lưng với đất nước: vẫn về dự đại triều hội, và năm 1370 về mừng vua mới. Còn điều quan trọng nhất ông để lại không phải tờ sớ mà là những học trò giữ được chuẩn mực khi làm quan.",
},
"quote": {
"source": "*Đại Việt sử ký toàn thư*, Bản kỷ quyển 7, tiểu sử Chu An chép ở năm 1370 — nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "安諫不聽，乃上疏乞斬佞臣七人，皆權幸者，時人號七斬疏。疏入不報，遂掛冠歸田里。 (An gián bất thính, nãi thượng sớ khất trảm nịnh thần thất nhân, giai quyền hạnh giả, thời nhân hiệu Thất trảm sớ. Sớ nhập bất báo, toại quải quan quy điền lý.)",
"vi": "Chu An can ngăn, vua không nghe; ông bèn dâng sớ xin chém bảy tên nịnh thần, đều là những kẻ có quyền thế được vua sủng ái — người đương thời gọi là “Thất trảm sớ”. Sớ dâng vào không được trả lời; ông bèn treo mũ từ quan, về làng.",
"url": "https://zh.wikisource.org/wiki/%E5%A4%A7%E8%B6%8A%E5%8F%B2%E8%A8%98%E5%85%A8%E6%9B%B8/%E6%9C%AC%E7%B4%80%E5%8D%B7%E4%B9%8B%E4%B8%83",
},
"misread": [
"**“Thất trảm sớ còn lưu lại, ghi rõ tên bảy gian thần.”** Thực ra nguyên văn tờ sớ không còn. *Đại Việt sử ký toàn thư* chỉ chép ông xin chém bảy nịnh thần “đều là kẻ quyền thế được vua sủng ái”, không nêu tên ai.",
"**“Chu Văn An là ẩn sĩ bất hợp tác với triều đình.”** Thực ra ông từng nhận chức Tư nghiệp Quốc Tử Giám và dạy thái tử; sau khi từ quan, ông vẫn về kinh dự đại triều hội và về mừng khi vua Trần Nghệ Tông lên ngôi. Ông từ chối phục vụ cái sai, không từ chối đất nước.",
],
"related": [
("cau-hoi/nho-giao-viet.md", "Nho giáo Việt Nam: tiếp thu hay sáng tạo?"),
],
"sources": [
("*Đại Việt sử ký toàn thư*, Bản kỷ quyển 7 (năm 1370: tiểu sử Chu An và lời bình của Ngô Sĩ Liên), nguyên văn chữ Hán, Wikisource tiếng Trung.", "https://zh.wikisource.org/wiki/%E5%A4%A7%E8%B6%8A%E5%8F%B2%E8%A8%98%E5%85%A8%E6%9B%B8/%E6%9C%AC%E7%B4%80%E5%8D%B7%E4%B9%8B%E4%B8%83"),
("Trần Trọng Kim, *Nho giáo* (bản in 1943), quyển IV, thiên IV, Wikisource tiếng Việt.", "https://vi.wikisource.org/wiki/Nho_gi%C3%A1o/Quy%E1%BB%83n_IV/Thi%C3%AAn_IV"),
("Khổng Tử, *Luận ngữ*, thiên Tiên tiến (11.24), nguyên văn chữ Hán, Chinese Text Project.", "https://ctext.org/analects/xian-jin"),
("Thompson, Kirill, “Zhu Xi”, *Stanford Encyclopedia of Philosophy* (về bộ *Tứ thư* do Chu Hy biên soạn và ảnh hưởng của ông tới Việt Nam).", "https://plato.stanford.edu/entries/zhu-xi/"),
("Nguyễn Hải Anh, “Lược quan hệ thống sách ‘Tiết yếu’ gắn với ‘Bùi thị nguyên bản’”, *Tạp chí Hán Nôm*, số 3 (184), 2024 (về *Tứ thư thuyết ước*).", "https://vjol.info.vn/hannom/article/view/233140"),
("“Chu Văn An: Người thầy mẫu mực”, *Báo Pháp luật Việt Nam* (về năm sinh theo thần tích làng Thanh Liệt).", "https://baophapluat.vn/chu-van-an-nguoi-thay-mau-muc-post216187.html"),
],
},
"nguyen-trai": {
"desc": "Mưu sĩ của Lê Lợi, tác giả Bình Ngô đại cáo: nhân nghĩa cốt ở yên dân — và chính ông chết oan dưới triều đại mình góp sức dựng nên.",
"bio": [
"Năm 1435, triều Lê định chém bảy kẻ trộm tái phạm, đều còn ít tuổi. Vua hỏi ý Nguyễn Trãi. Ông đáp: rõ ràng pháp lệnh không bằng nhân nghĩa; một lúc giết bảy người e không phải việc của bậc thịnh đức. Các đại thần bèn đề nghị giao bọn trẻ cho ông cảm hóa; ông từ chối, nói phép nước còn không trị nổi thì kẻ đức mỏng làm sao cảm hóa được. Cuối cùng hai người bị chém, số còn lại bị đày. Câu chuyện nhỏ chép trong *Đại Việt sử ký toàn thư* cho thấy điều xuyên suốt đời ông — và cả giới hạn của nó: đo việc nước bằng thước “yên dân”.",
"Nguyễn Trãi, hiệu Ức Trai, người làng Nhị Khê (nay thuộc Hà Nội), đỗ Thái học sinh năm 1400 trong khoa thi của Hồ Quý Ly. Khi nhà Minh chiếm Đại Việt, ông theo Lê Lợi trong cuộc khởi nghĩa Lam Sơn, giữ việc thảo thư từ, hịch, cáo. *Toàn thư* chép: Lê Lợi sai ông viết thư dụ các thành Nghệ An, Thuận Hóa, Tây Đô, Đông Đô, bày rõ họa phúc, nên nhiều thành không đánh mà hàng; hơn mười vạn quân cứu viện nhà Minh bị bắt cũng được thả về. Năm 1428, ông viết *Bình Ngô đại cáo* thay lời Lê Lợi.",
"Thời bình, ông giữ những chức văn quan cao nhưng thường va chạm với các đại thần võ quan có công khai quốc. Năm 1442, vua Lê Thái Tông đi tuần miền đông, theo lời mời ghé chùa Côn Sơn quê ông, rồi đột ngột băng hà ở vườn Lệ Chi sau một đêm có vợ ông là Nguyễn Thị Lộ hầu bên. Người ta đồn Thị Lộ giết vua; Nguyễn Trãi bị giết cùng vợ, tội lây ba họ. Năm 1464, vua Lê Thánh Tông cho con ông là Nguyễn Anh Vũ ra làm quan; năm 1467 nhà vua sai sưu tầm thơ văn ông còn sót lại.",
"Ông để lại cả chữ Hán lẫn chữ Nôm: *Quân trung từ mệnh tập* (thư từ trong quân), *Ức Trai thi tập*, sách địa lý *Dư địa chí*, và *Quốc âm thi tập* — 254 bài thơ Nôm theo bản sưu tầm thế kỷ 19, được xem là tập thơ Nôm xưa nhất còn lại. Trong một bài thơ chữ Hán, ông viết: lật thuyền mới tin dân như nước — hình ảnh mà *Tuân Tử* đã dẫn từ một lời truyền xưa: vua là thuyền, dân là nước; nước chở thuyền, nước cũng lật thuyền. Câu hỏi của ông vẫn còn nguyên: một chính quyền lấy gì để chứng minh mình chính đáng?",
],
"works": [
("thời Lam Sơn", "*Quân trung từ mệnh tập*", "thư từ, văn kiện viết trong cuộc kháng chiến, nhiều lá dụ tướng Minh đầu hàng"),
("1428", "*Bình Ngô đại cáo* (平吳大誥)", "bài cáo tuyên bố thắng lợi và độc lập, mở đầu bằng định nghĩa nhân nghĩa"),
("", "*Ức Trai thi tập* (抑齋詩集)", "thơ chữ Hán, trong đó có *Quan hải* với câu “lật thuyền mới tin dân như nước”"),
("", "*Quốc âm thi tập*", "254 bài thơ Nôm, tập thơ Nôm xưa nhất còn lại"),
("", "*Dư địa chí*", "sách địa lý Đại Việt, còn gọi *An Nam vũ cống*"),
],
"thoughts": [
"**Nhân nghĩa cốt ở yên dân**: nhân nghĩa không đo bằng lời hay mà bằng việc dân có được yên không; đội quân “điếu phạt” — thương dân, đánh kẻ có tội — trước hết là để trừ bạo.",
"**Dân như nước**: “lật thuyền mới tin dân như nước” (*Quan hải*) — quyền lực đứng trên dân như thuyền trên nước; dân chở thuyền, dân cũng lật thuyền.",
"**Pháp lệnh không bằng nhân nghĩa**: luật pháp là công cụ, không phải thước đo cuối cùng; khi áp luật làm hại nhiều hơn giúp, phải quay về câu hỏi gốc: việc này có làm dân yên không?",
"**Thắng lòng người hơn thắng thành**: ông chủ trương đánh vào lòng người — viết thư dụ hàng, tha tù binh — vì chiến thắng phải kết thúc bằng hòa bình lâu dài chứ không bằng thù hận.",
"**Văn hiến là nền của độc lập**: Đại Việt đáng độc lập không chỉ vì có cương vực riêng mà vì có văn hiến, phong tục, triều đại riêng, ngang hàng với phương Bắc — một lập luận về bản sắc.",
],
"argument": {
"title": "Yên dân là thước đo của chính nghĩa",
"intro": "Phần mở đầu *Bình Ngô đại cáo* không kể chiến công mà nêu một tiêu chuẩn, rồi áp tiêu chuẩn ấy vào thực tế. Theo cách tái dựng phổ biến:",
"premises": [
"Việc nhân nghĩa cốt ở yên dân; đội quân điếu phạt trước hết là để trừ bạo.",
"Đại Việt là một nước có văn hiến, có cương vực, phong tục và các triều đại riêng, ngang hàng với các triều phương Bắc.",
"Quân Minh, nhân lúc nhà Hồ hà khắc, đã sang tàn hại dân Đại Việt bằng thuế khóa, phu dịch, chém giết.",
],
"conclusion": "Vậy cuộc kháng chiến Lam Sơn là việc nhân nghĩa, và nền độc lập của Đại Việt là chính đáng.",
"objection": "Ai thắng cũng tự xưng nhân nghĩa. Tiêu chí “yên dân” do chính người thắng diễn giải, nên bản cáo là lời của một bên, không phải phán quyết độc lập. Và lịch sử trớ trêu: chính triều đại sinh ra từ bản cáo ấy đã giết tác giả của nó cùng ba họ.",
"reply": "Tiêu chí “yên dân” kiểm được bằng việc làm, và Nguyễn Trãi dùng nó để trói tay chính phe mình: bản cáo kể việc cấp hơn năm trăm chiến thuyền và mấy nghìn con ngựa cho quân Minh đã hàng về nước, vì “lấy toàn quân làm trên hết, muốn dân được nghỉ ngơi”. Thời bình, ông vẫn dùng tiêu chí ấy để chất vấn triều đình, như vụ bảy thiếu niên năm 1435. Còn án Lệ Chi Viên cho thấy giới hạn của một học thuyết trông vào đức của người cầm quyền mà thiếu cơ chế ràng buộc họ.",
},
"quote": {
"source": "Nguyễn Trãi, lời tâu khi dâng bản vẽ khánh đá (1437), chép trong *Đại Việt sử ký toàn thư*, Bản kỷ quyển 11 — nguyên văn chữ Hán và phiên âm Hán Việt",
"orig": "和平為樂之本，聲音為樂之文。……願陛下愛養元元，使閭里無怨恨愁嘆之聲，斯為不失樂之本矣。 (Hòa bình vi nhạc chi bản, thanh âm vi nhạc chi văn. … Nguyện bệ hạ ái dưỡng nguyên nguyên, sử lư lý vô oán hận sầu thán chi thanh, tư vi bất thất nhạc chi bản hĩ.)",
"vi": "Hòa bình là gốc của nhạc, âm thanh chỉ là phần văn vẻ của nhạc. … Mong bệ hạ thương yêu nuôi dưỡng muôn dân, khiến nơi xóm làng không còn tiếng oán hận sầu than; như thế mới là không đánh mất cái gốc của nhạc.",
"url": "https://zh.wikisource.org/wiki/%E5%A4%A7%E8%B6%8A%E5%8F%B2%E8%A8%98%E5%85%A8%E6%9B%B8/%E6%9C%AC%E7%B4%80%E5%8D%B7%E4%B9%8B%E5%8D%81%E4%B8%80",
},
"misread": [
"**“Nguyễn Trãi bị xử vì đã bị chứng minh là giết vua.”** Thực ra *Đại Việt sử ký toàn thư* chỉ chép vua mất đột ngột ở vườn Lệ Chi sau một đêm có Nguyễn Thị Lộ hầu, và “người ta đều nói Thị Lộ giết vua” — một lời đồn; sử không ghi cuộc tra xét nào. Hai mươi hai năm sau, vua Lê Thánh Tông đã cho con ông ra làm quan và sai sưu tầm thơ văn của ông.",
],
"related": [
("doc/nguyen-trai-binh-ngo.md", "Hướng dẫn đọc Bình Ngô đại cáo của Nguyễn Trãi"),
("cau-hoi/nho-giao-viet.md", "Nho giáo Việt Nam: tiếp thu hay sáng tạo?"),
("cau-hoi/duc-tri.md", "Cai trị bằng đức hay bằng pháp?"),
],
"sources": [
("*Đại Việt sử ký toàn thư*, Bản kỷ quyển 10–12 (Bình Ngô đại cáo; các việc năm 1435 và 1437; án Lệ Chi Viên 1442; các năm 1464, 1467), nguyên văn chữ Hán, Wikisource tiếng Trung.", "https://zh.wikisource.org/wiki/%E5%A4%A7%E8%B6%8A%E5%8F%B2%E8%A8%98%E5%85%A8%E6%9B%B8/%E6%9C%AC%E7%B4%80%E5%8D%B7%E4%B9%8B%E5%8D%81%E4%B8%80"),
("Nguyễn Trãi, *Bình Ngô đại cáo* (1428), nguyên văn chữ Hán theo *Hoàng Việt văn tuyển* và các bản dịch, Wikisource tiếng Việt.", "https://vi.wikisource.org/wiki/B%C3%ACnh_Ng%C3%B4_%C4%91%E1%BA%A1i_c%C3%A1o"),
("Nguyễn Trãi, *Quan hải* (關海), nguyên văn chữ Hán, Wikisource tiếng Việt.", "https://vi.wikisource.org/wiki/Quan_h%E1%BA%A3i"),
("Mạnh Tử, thiên Lương Huệ Vương hạ (“tru kỳ quân nhi điếu kỳ dân”) và Tuân Tử, thiên Vương chế (“quân giả chu dã, thứ nhân giả thủy dã”), Chinese Text Project.", "https://ctext.org/mengzi/liang-hui-wang-ii"),
("Nguyễn Trãi, *Toàn tập*, in lần thứ hai có sửa chữa bổ sung, Hà Nội: NXB Khoa học xã hội, 1976.", ""),
("Nguyễn Minh Sơn, “Phải chăng thời Nguyễn Trãi chưa có từ nêu giả thuyết ‘nếu’?”, *Ngôn ngữ & Đời sống*, số 5 (175), 2010 (về 254 bài của *Quốc âm thi tập*).", "https://vjol.info.vn/NNDS/article/view/13430"),
],
},
"tran-duc-thao": {
"desc": "Người Việt đầu tiên đỗ thạc sĩ (agrégation) triết học ở Pháp, đối thoại với Husserl, Marx, Sartre; về nước năm 1952 và nhiều thăng trầm sau năm 1956.",
"bio": [
"Mùa đông 1949–1950 ở Paris, Jean-Paul Sartre và một người Việt ba mươi hai tuổi ghi âm năm buổi trò chuyện về chủ nghĩa hiện sinh và chủ nghĩa Marx, định in thành sách. Cuộc đối thoại đổ vỡ giữa chừng; bản ghi đến nay vẫn thất lạc. Người Việt ấy là Trần Đức Thảo. Theo ông, Sartre coi chủ nghĩa Marx là một cương lĩnh xã hội hấp dẫn nhưng chưa phải một triết học nghiêm túc. Năm 1951, ông cho in câu trả lời của mình: *Hiện tượng luận và duy vật biện chứng* — cuốn sách mà cả một thế hệ người Pháp, trong đó có Derrida, Lyotard và Ricœur, dùng làm lối vào tư tưởng Husserl.",
"Ông sinh năm 1917, học ở Hà Nội, năm 1936 nhận học bổng sang Pháp và năm 1939 vào Trường Sư phạm Cao cấp (*École normale supérieure*) ở Paris. Qua Jean Cavaillès và Maurice Merleau-Ponty, ông đến với hiện tượng luận của Husserl; năm 1942 ông viết luận văn về phương pháp hiện tượng luận, năm 1943 đỗ kỳ thi thạc sĩ (*agrégation*) triết học — người Việt Nam đầu tiên đạt học vị này. Năm 1944 ông đến Kho lưu trữ Husserl ở Louvain (Bỉ) và góp phần đưa một phần bản thảo chưa in của Husserl về Paris. Cuối năm 1945, sau một phát biểu phản đối việc Pháp đưa quân trở lại Đông Dương, ông bị bắt giam mấy tháng; năm 1946 ông viết về Đông Dương trên tạp chí *Les Temps modernes* của Sartre.",
"Năm 1951 ông rời Pháp; năm 1952 ông đến chiến khu Việt Bắc. Sau 1954, ông dạy lịch sử triết học ở Hà Nội và làm chủ nhiệm khoa Sử. Năm 1956, trong bầu không khí cởi mở ngắn ngủi sau khi Liên Xô phê phán Stalin, ông viết bài cho các ấn phẩm của nhóm Nhân Văn – Giai Phẩm, đòi mở rộng tự do dân chủ và chống bệnh quan liêu. Khi nhóm này bị phê phán, năm 1958 ông phải tự phê bình công khai và thôi dạy đại học. Theo các nhà nghiên cứu, ông bị đưa đi lao động ở một nông trường đến năm 1961, rồi về Hà Nội làm dịch thuật, trong đó có dịch Marx và Engels cho Nhà xuất bản Sự Thật, và sống nhiều năm đơn độc, thiếu thốn.",
"Ông vẫn nghiên cứu, gửi bài cho tạp chí Pháp, và in *Nghiên cứu về nguồn gốc của ngôn ngữ và ý thức* ở Paris năm 1973. Cuối thập niên 1980 hoàn cảnh ông khá hơn; năm 1991 ông sang Pháp và mất ở Paris ngày 24 tháng 4 năm 1993. Năm 2000, ông được truy tặng Giải thưởng Hồ Chí Minh. Với người Việt hôm nay, ông là một tiền lệ: triết gia Việt Nam có thể không chỉ học triết học thế giới mà bước vào giữa cuộc tranh luận của nó.",
],
"works": [
("1948", "“La *Phénoménologie de l’esprit* et son contenu réel”", "bài phê bình cách đọc Hegel của Kojève trên *Les Temps modernes*: ý thức là một cấu trúc mới nảy sinh từ biện chứng của chính tự nhiên"),
("1951", "*Phénoménologie et matérialisme dialectique*", "*Hiện tượng luận và duy vật biện chứng* (Paris: Minh-Tân; bản tiếng Anh 1986): phần một trình bày Husserl, phần hai phác thảo quá trình hình thành ý thức từ sinh vật đến xã hội"),
("1973", "*Recherches sur l’origine du langage et de la conscience*", "*Nghiên cứu về nguồn gốc của ngôn ngữ và ý thức* (Paris: Éditions sociales; bản tiếng Anh 1984): ý thức hình thành cùng với ngôn ngữ"),
("1989", "*Vấn đề con người và chủ nghĩa “lý luận không có con người”*", "sách tiếng Việt (NXB TP. Hồ Chí Minh) phê phán chủ nghĩa phản nhân bản của Althusser"),
],
"thoughts": [
"**Đi qua Husserl để vượt Husserl**: ông coi **hiện tượng luận** (*phenomenology*) là phương pháp mô tả kinh nghiệm tốt nhất, nhưng cho rằng chính phân tích sâu nhất của nó — về nguồn gốc của ý nghĩa — buộc ta bước ra khỏi ý thức thuần túy.",
"**Ý thức có lịch sử**: ý thức không rơi từ trên trời xuống mà hình thành dần trong tiến hóa của sinh vật và trong lao động xã hội; ông muốn chứng minh bằng chi tiết câu của Marx trong *Hệ tư tưởng Đức*: không phải ý thức quyết định đời sống, mà đời sống quyết định ý thức.",
"**Biện chứng, không phải quy giản**: ở mỗi nấc tiến hóa xuất hiện một cấu trúc mới, giữ lại cấu trúc cũ nhưng cho nó ý nghĩa mới; ý thức con người là cái mới thật sự, không chỉ là phản xạ phức tạp hơn.",
"**Ngôn ngữ và ý thức cùng lớn lên**: trong sách năm 1973, ông đặt khởi điểm của ý thức ở “cử chỉ chỉ trỏ” — khả năng hướng mình và người khác tới một vật ở bên ngoài — rồi ngôn ngữ phát triển dần qua các giai đoạn tiến hóa của loài người.",
"**Tự do có nội dung và có hình thức**: năm 1956 ông lập luận rằng giành được độc lập là có tự do về nội dung, nhưng hình thức của tự do là tự do cá nhân — tự do ngôn luận, hội họp, báo chí.",
],
"argument": {
"title": "Từ “cái sống trải” đến đời sống thực",
"intro": "Câu hỏi của *Hiện tượng luận và duy vật biện chứng* (1951): muốn hiểu ý nghĩa và ý thức từ đâu mà có, nên bắt đầu từ kinh nghiệm của chủ thể như Husserl, hay từ thế giới vật chất như Marx? Theo cách tái dựng phổ biến:",
"premises": [
"Husserl đúng khi đòi quay về với kinh nghiệm sống: mọi ý nghĩa phải được truy về cách sự vật hiện ra cho ý thức.",
"Nhưng khi truy đến nguồn gốc của ý nghĩa, phân tích ấy chạm tới những tầng mà ý thức không tự tạo ra — thân thể, cảm giác, hành động; ý thức luôn đến sau và không nắm hết điều cơ thể đang làm.",
"Những tầng ấy thuộc về đời sống thực: tiến hóa sinh học và lao động xã hội. “Cái sống trải” chỉ là một mặt trừu tượng của đời sống thực ấy.",
],
"conclusion": "Vậy muốn hoàn tất chính dự án của hiện tượng luận, phải chuyển sang một lý thuyết duy vật biện chứng về sự hình thành ý thức từ tự nhiên và xã hội.",
"objection": "Từ phía hiện tượng luận: đây là vòng luẩn quẩn. Mọi hiểu biết về tiến hóa hay lao động đều đã là sản phẩm của ý thức, nên không thể dùng chúng để “rút” ý thức ra từ vật chất mà không ngầm giả định chính cái cần giải thích — tức quay lại đúng thái độ tự nhiên mà Husserl đòi đặt trong ngoặc. Ngay cả người đọc thiện cảm như Rory O’Sullivan (2026) cũng thấy phần hai của cuốn sách nhiều chỗ rơi vào thứ duy vật máy móc mà chính Thảo từng cảnh báo.",
"reply": "Người bênh vực Thảo đáp: ông không phủ nhận mô tả hiện tượng luận, chỉ phủ nhận rằng nó là nền tảng cuối cùng; và ông không quy giản ý thức thành phản xạ, mà nói về những cấu trúc mới nảy sinh ở mỗi nấc tiến hóa. Về sau, trong sách năm 1973, ông cố biến luận đề thành những giả thuyết có thể đối chiếu với nhân học, tâm lý học trẻ em và ngôn ngữ học: ý thức bắt đầu từ cử chỉ chỉ trỏ và lớn lên cùng ngôn ngữ — một câu hỏi mà khoa học nhận thức hôm nay vẫn đang theo đuổi.",
},
"misread": [
"**“Trần Đức Thảo chỉ là người giới thiệu Husserl và Marx cho người Việt.”** Thực ra ông viết chủ yếu bằng tiếng Pháp, cho độc giả Pháp, và tham gia trực tiếp các cuộc tranh luận ở Paris — với cách đọc Hegel của Kojève, với Sartre; cuốn sách năm 1951 của ông là một trong những lối vào Husserl của cả một thế hệ triết gia Pháp.",
"**“Sau khi về nước, ông từ bỏ triết học.”** Thực ra dù bị kỷ luật và sống thiếu thốn, ông vẫn nghiên cứu: cuốn sách lớn thứ hai về nguồn gốc ngôn ngữ và ý thức ra đời năm 1973, và cuối đời ông còn viết sách bằng tiếng Việt về vấn đề con người.",
],
"related": [
("cau-hoi/viet-hien-dai.md", "Triết học Việt Nam hiện đại, từ Nho học đến Marx và hiện sinh"),
("lich-su/nhat-ban-viet-nam.md", "Nhật Bản và Việt Nam: triết học ở phương Đông"),
],
"sources": [
("McHale, Shawn, “Vietnamese Marxism, Dissent, and the Politics of Postcolonial Memory: Tran Duc Thao, 1946–1993”, *The Journal of Asian Studies* 61(1), 2002, tr. 7–37.", "https://doi.org/10.2307/2700187"),
("Benoist, Jocelyn & Michel Espagne (chủ biên), *L’itinéraire de Tran Duc Thao. Phénoménologie et transferts culturels*, Paris: Armand Colin, 2013 (ISBN 978-2-200-28045-1).", ""),
("Féron, Alexandre, “Who is Tran Duc Thao? Life and Work of a Vietnamese Philosopher” (bản dịch tiếng Anh bài viết của tác giả).", "https://ipernity.com/blog/235050/512209"),
("O’Sullivan, Rory, “The tragedy of Trần Đức Thảo”, *Aeon*, 8/1/2026.", "https://aeon.co/essays/the-tragic-life-and-principled-politics-of-tran-duc-thao"),
("Phạm Công Thưởng, “Phép biện chứng duy vật trong tư tưởng triết học Trần Đức Thảo”, *Tạp chí Triết học*, số 12 (396), 2024, tr. 50–60.", "https://vjol.info.vn/phil/article/download/135041/110963/"),
("Trường Đại học Sư phạm Hà Nội, “Trường Đại học Sư phạm Hà Nội với Giải thưởng Hồ Chí Minh” (đợt II, năm 2000).", "https://staff.hnue.edu.vn/Tintuc-Sukien/Trangtintonghop/tabid/260/news/377/TruongDaihocSuphamHaNoivoiGiaithuongHoChiMinh.aspx"),
],
},
}


# ----------------------------------------------------------------------------
# Sinh trang
# ----------------------------------------------------------------------------

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK_TO_PERSON = re.compile(r"\]\((?:\.\./)*triet-gia/([a-z0-9-]+)\.md(?:#[^)\s]*)?\)")
# Không tính vào "các bài khác nhắc tới": trang sinh tự động liệt kê mọi
# triết gia, các trang triết gia khác, và mục Thêm (sách in chép lại mọi bài).
BACKLINK_SKIP = {"lich-su/dong-thoi-gian.md", "lich-su/so-do-anh-huong.md"}
BACKLINK_SKIP_DIRS = ("triet-gia/", "them/")
SECTION_ORDER = ["bat-dau", "cong-cu", "cau-hoi", "lich-su", "doc"]


def validate(data: list) -> list[str]:
    errors = []
    ids = {p.get("id") for p in data}
    for p in data:
        pid = p.get("id")
        if p.get("school") not in SCHOOLS:
            errors.append(f"{pid}: school lạ: {p.get('school')}")
        for inf in p.get("influence", []):
            if inf not in ids:
                errors.append(f"{pid}: influence lạ: {inf}")
        if CERTAINTY_LABEL.search(p.get("summary", "")):
            errors.append(f"{pid}: summary chứa nhãn độ chắc chắn")
        c = CONTENT.get(pid)
        if c is None:
            errors.append(f"{pid}: thiếu nội dung trong CONTENT")
            continue
        if not c.get("bio") or not c.get("thoughts"):
            errors.append(f"{pid}: bio/thoughts rỗng")
        if not c.get("sources"):
            errors.append(f"{pid}: thiếu sources")
        for _, url in c.get("sources", []):
            if url and not url.startswith("https://"):
                errors.append(f"{pid}: URL nguồn phải là https: {url}")
        for rel, _ in c.get("related", []):
            if not (DOCS / rel).is_file():
                errors.append(f"{pid}: related trỏ tới trang không có: {rel}")
        a = c.get("argument")
        if a and not (a.get("premises") and a.get("conclusion")):
            errors.append(f"{pid}: argument thiếu premises/conclusion")
        if CERTAINTY_LABEL.search(json.dumps(c, ensure_ascii=False)):
            errors.append(f"{pid}: nội dung chứa nhãn độ chắc chắn")
    extra = set(CONTENT) - ids
    if extra:
        errors.append(f"CONTENT thừa id không có trong JSON: {sorted(extra)}")
    return errors


def reverse_influence(data: list) -> dict[str, list[dict]]:
    """rev[X] = những người có X trong "influence" của họ, tức những người đã ảnh hưởng tới X."""
    by_id = {p["id"]: p for p in data}
    rev: dict[str, list[dict]] = {p["id"]: [] for p in data}
    for p in data:
        for t in p.get("influence", []):
            if t in rev:
                rev[t].append(p)
    for lst in rev.values():
        lst.sort(key=lambda p: (p["start"], p["name"]))
    return by_id, rev


def page_title(text: str, fallback: str) -> str:
    m = FRONT_MATTER.match(text)
    if m:
        meta = yaml.safe_load(m.group(1)) or {}
        if meta.get("title"):
            return str(meta["title"])
    h = re.search(r"^# (.+)$", text, re.M)
    return h.group(1).strip() if h else fallback


def backlinks(ids: set[str]) -> dict[str, list[tuple[str, str]]]:
    """{id: [(đường dẫn từ docs/, tiêu đề)]}: các bài có link tới trang của triết gia."""
    found: dict[str, list[tuple[str, str]]] = {i: [] for i in ids}
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS).as_posix()
        if "/" not in rel or rel in BACKLINK_SKIP or rel.startswith(BACKLINK_SKIP_DIRS):
            continue
        text = path.read_text(encoding="utf-8")
        linked = set(LINK_TO_PERSON.findall(text)) & ids
        if not linked:
            continue
        title = page_title(text, path.stem)
        for pid in linked:
            found[pid].append((rel, title))

    def order(item: tuple[str, str]) -> tuple[int, str]:
        section = item[0].split("/")[0]
        rank = SECTION_ORDER.index(section) if section in SECTION_ORDER else len(SECTION_ORDER)
        return rank, item[0]

    for lst in found.values():
        lst.sort(key=order)
    return found


def link(p: dict) -> str:
    return f"[{p['name']}]({p['id']}.md)"


def render_person(p: dict, by_id: dict, rev: dict, back: dict) -> str:
    c = CONTENT[p["id"]]
    L = []
    L.append("---")
    L.append(f'title: "{p["name"]}"')
    L.append(f'description: "{c["desc"]}"')
    L.append(f"updated: {UPDATED}")
    L.append("---")
    L.append("")
    L.append(MARKER)
    L.append("")
    L.append(f"# {p['name']}")
    L.append("")
    head = f"**{p['years']}** · {p['school']}"
    if p["name_en"] != p["name"]:
        head += f" · *{p['name_en']}*"
    L.append(head)
    L.append("")
    # Mỗi đoạn tiểu sử cách nhau một dòng trống — viết liền thì Markdown gộp
    # thành một đoạn (lỗi của bản sinh trước 22/10/2026).
    for para in c["bio"]:
        L.append(para)
        L.append("")
    if c.get("works"):
        L.append("## Tác phẩm chính")
        L.append("")
        for year, title, gloss in c["works"]:
            line = f"- {title}"
            if year:
                line += f" ({year})"
            if gloss:
                line += f" — {gloss}"
            L.append(line)
        L.append("")
    L.append("## Tư tưởng chính")
    L.append("")
    for t in c["thoughts"]:
        L.append(f"- {t}")
    L.append("")
    a = c.get("argument")
    if a:
        L.append(f"## Một lập luận tiêu biểu: {a['title']}" if a.get("title") else "## Một lập luận tiêu biểu")
        L.append("")
        if a.get("intro"):
            L.append(a["intro"])
            L.append("")
        for i, premise in enumerate(a["premises"], 1):
            L.append(f"- **P{i}.** {premise}")
        L.append(f"- **K.** {a['conclusion']}")
        L.append("")
        if a.get("objection"):
            L.append(f"**Phản bác chính.** {a['objection']}")
            L.append("")
        if a.get("reply"):
            L.append(f"**Cách đáp lại.** {a['reply']}")
            L.append("")
    q = c.get("quote")
    if q:
        L.append(f'!!! quote "{q["source"]}"')
        L.append(f'    "{q["orig"]}"')
        L.append("")
        L.append(f'    "{q["vi"]}" *(bản dịch của Logos Zero)*')
        L.append("")
    if c.get("misread"):
        L.append("## Hiểu lầm thường gặp")
        L.append("")
        for m in c["misread"]:
            L.append(f"- {m}")
        L.append("")
    L.append("## Ảnh hưởng")
    L.append("")
    influenced_by = rev[p["id"]]
    if influenced_by:
        L.append("**Chịu ảnh hưởng từ:** " + ", ".join(link(q) for q in influenced_by) + ".")
    else:
        L.append("**Chịu ảnh hưởng từ:** chưa ghi nhận trong dữ liệu của site.")
    L.append("")
    targets = [by_id[t] for t in p.get("influence", []) if t in by_id]
    targets.sort(key=lambda q: (q["start"], q["name"]))
    if targets:
        L.append("**Ảnh hưởng tới:** " + ", ".join(link(q) for q in targets) + ".")
    else:
        L.append("**Ảnh hưởng tới:** chưa ghi nhận trong dữ liệu của site.")
    L.append("")
    L.append("## Đọc thêm trên Logos Zero")
    L.append("")
    curated = [rel for rel, _ in c["related"]]
    for rel, label in c["related"]:
        L.append(f"- [{label}](../{rel})")
    L.append("")
    others = [(rel, title) for rel, title in back[p["id"]] if rel not in curated]
    if others:
        L.append(f"**Các bài khác nhắc tới {p['name']}:** "
                 + ", ".join(f"[{title}](../{rel})" for rel, title in others) + ".")
        L.append("")
    L.append("## Nguồn")
    L.append("")
    for i, (label, url) in enumerate(c["sources"], 1):
        L.append(f"{i}. {label}" + (f" <{url}>" if url else ""))
    L.append("")
    L.append("---")
    L.append("")
    L.append("*[Các triết gia](index.md) · [Dòng thời gian triết học](../lich-su/dong-thoi-gian.md) · "
             "[Sơ đồ ảnh hưởng](../lich-su/so-do-anh-huong.md)*")
    L.append("")
    return "\n".join(L)


EAST = {"Trung Hoa", "Ấn Độ", "Việt Nam"}


def render_index(data: list) -> str:
    def span(group: list) -> str:
        group = sorted(group, key=lambda p: p["start"])
        return f"từ {group[0]['name']} đến {group[-1]['name']}"

    west = [p for p in data if p["school"] not in EAST]
    east = [p for p in data if p["school"] in EAST]
    parts = ["tiểu sử"]
    if any(CONTENT[p["id"]].get("works") for p in data):
        parts.append("tác phẩm chính")
    parts.append("tư tưởng chính")
    if any(CONTENT[p["id"]].get("argument") for p in data):
        parts.append("một lập luận tiêu biểu viết ở dạng chuẩn kèm phản bác")
    parts += ["ai ảnh hưởng đến họ và họ ảnh hưởng đến ai", "các bài trên site nhắc tới họ", "nguồn để đọc tiếp"]
    L = []
    L.append("---")
    L.append('title: "Các triết gia"')
    L.append(f'description: "{len(data)} triết gia {span(west)}, {span(east)} — mỗi người một trang: tiểu sử, tư tưởng, ảnh hưởng và nguồn."')
    L.append(f"updated: {UPDATED}")
    L.append("---")
    L.append("")
    L.append(MARKER)
    L.append("")
    L.append("# Các triết gia")
    L.append("")
    L.append("Triết học không phải danh sách trừu tượng các “chủ nghĩa” — đó là câu chuyện của những con người cụ thể, sống trong thời đại cụ thể, tranh luận với nhau qua nhiều thế kỷ. "
             f"Mỗi triết gia dưới đây có một trang riêng: {', '.join(parts[:-1])} và {parts[-1]}.")
    L.append("")
    L.append(f"Hiện có **{len(data)} triết gia**.")
    L.append("")
    for school in SCHOOLS:
        group = sorted([p for p in data if p["school"] == school],
                       key=lambda p: (p["start"], p["name"]))
        if not group:
            continue
        L.append(f"### {school}")
        L.append("")
        for p in group:
            L.append(f"- [{p['name']} ({p['years']})]({p['id']}.md) — {p['summary']}")
        L.append("")
    L.append("*Xem toàn cảnh: [Dòng thời gian triết học](../lich-su/dong-thoi-gian.md) · "
             "[Sơ đồ ảnh hưởng](../lich-su/so-do-anh-huong.md)*")
    L.append("")
    return "\n".join(L)


def generate(data: list) -> dict[str, str]:
    """Trả về {đường dẫn tương đối từ OUT: nội dung}."""
    by_id, rev = reverse_influence(data)
    back = backlinks(set(by_id))
    out = {}
    for p in data:
        out[f"{p['id']}.md"] = render_person(p, by_id, rev, back)
    out["index.md"] = render_index(data)
    return out


def main(argv: list[str]) -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    pages = generate(data)
    if "--check" in argv:
        problems = []
        existing = {p.name for p in OUT.glob("*.md")} if OUT.is_dir() else set()
        for name, body in sorted(pages.items()):
            path = OUT / name
            if not path.exists():
                problems.append(f"thiếu file: docs/triet-gia/{name}")
            elif path.read_text(encoding="utf-8") != body:
                problems.append(f"lệch nội dung: docs/triet-gia/{name}")
        for name in sorted(existing - set(pages)):
            problems.append(f"file thừa (không do generator sinh): docs/triet-gia/{name}")
        if problems:
            print("Trang triết gia lệch so với dữ liệu:", file=sys.stderr)
            print("\n".join(f"  {x}" for x in problems), file=sys.stderr)
            print("Chạy: python tools/philosophers.py", file=sys.stderr)
            return 1
        print(f"Trang triết gia khớp dữ liệu ({len(pages)} trang).")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for name, body in sorted(pages.items()):
        (OUT / name).write_text(body, encoding="utf-8")
    print(f"Đã sinh {len(pages)} trang trong docs/triet-gia/ ({len(data)} triết gia + chỉ mục).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
