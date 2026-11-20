# Hướng dẫn kiểm 5.8: Câu hỏi lớn II (`docs/cau-hoi/*.md`)

Repo: `/Users/mitu/Desktop/work/projects/logos`. Bạn là **agent kiểm**, không phải người viết bài.

- **Chỉ ghi** file `verification/evidence/cau-hoi__<trang>.md__*.json` của các trang được giao. Không sửa bài, không commit, không đổi nhánh git.
- File tạm (HTML tải về, script) đặt trong thư mục riêng `${TMPDIR:-/tmp}/logos-5.8/<mã của bạn>/`.

## Đọc trước

1. `ban-giao/kiem-chung.md`: quy trình, checklist ngữ nghĩa, mức lỗi, định dạng file bằng chứng. Đây là luật chính.
2. `schema/evidence.schema.json`: schema mà CI kiểm.
3. Bảng thuật ngữ bắt buộc trong `HUONG-DAN-VIET.md`: chỉ khi cần đối chiếu thuật ngữ.

Không mở `verification/evidence/` của trang khác, `verification/mau/` hay nhật ký. Bạn kiểm độc lập.

## Đơn vị

Mỗi trang có 9–10 đơn vị: `_dau` (phần trước H2 đầu tiên, gồm hộp "Tóm tắt 5 phút") và mỗi mục H2 (id là phần `{#…}` của tiêu đề). Xem danh sách khóa:

    uv run python tools/verify.py --pham-vi 5.8 | grep <tên-trang>

Lấy mã băm hiện tại:

    uv run python tools/check_ledger.py --hash "cau-hoi/<trang>.md#<id>"

Đơn vị là một mục H2, gồm cả các mục H3 bên trong. Quiz trong "Tự kiểm tra" được kiểm cùng đơn vị đó: kiểm đáp án đúng có thật sự đúng, các phương án sai có thật sự sai, lời giải có khớp bài không.

## Cái gì cần kiểm ở bài Câu hỏi lớn

- **Tóm tắt 5 phút** (`_dau`): mỗi ý phải khớp đúng điều thân bài nói, không thêm dữ kiện mà thân bài không có.
- **Dữ kiện** (`du-kien`): năm, tên người, tên tác phẩm, tên thí nghiệm, số liệu.
  - Phần lớn đã có trong kho đóng băng: dùng `kb` (xem mục dưới).
  - Số liệu PhilPapers viết bằng shortcode `[[pp:…]]` lấy từ kho `philpapers/*` đã đóng băng. Chỉ kiểm câu văn có diễn đạt đúng con số không (câu chính hay câu bổ sung, "chấp nhận hoặc nghiêng về", đúng lựa chọn). Đối chiếu với `tools/philpapers-2020.md`.
- **Khối thời sự** `[[thoi-su:…]]` (nội dung ở `data/thoi-su/`): **không kiểm** ở đây, vì nó có quy trình rà soát riêng. Chỉ kiểm câu bao quanh nó.
- **Thí nghiệm tư duy**: kể đúng phiên bản của tác giả gốc chưa (tên, năm, chi tiết then chốt)? Phiên bản do bài tự chế thì có ghi rõ không?
- **Các lập trường chính**: mỗi lập trường có đủ ba nhãn **Lập luận mạnh nhất**, **Phản bác chính**, **Cách đáp lại** không. Thiếu nhãn thì ghi `sai`, mức `vua`, kèm `fix` gợi ý câu.
  - Lập luận có được trình bày ở dạng mạnh nhất, không thành người rơm không?
  - Phản bác và cách đáp lại có thật trong văn liệu (SEP, IEP) không?
  - Nếu gắn với một tác giả, tác giả đó có nói vậy không?
- **Khái quát** (`dien-giai`): "phần lớn triết gia cho rằng…", "lập luận nổi tiếng nhất…", "đầu tiên…". Không có nguồn thì `sai`, mức `vua` (dữ kiện trình bày như chắc chắn) hoặc `nhe`, với `fix` làm câu chặt lại.
- **Giới triết học ngày nay nghĩ gì**: số liệu đúng câu khảo sát; nhận định đi kèm không vượt quá số liệu.
- **Liên hệ đời sống**: dữ kiện Việt Nam (luật, sự kiện, tục lệ) cần nguồn. Nguồn tiếng Việt yếu (báo, trang tin) chấp nhận được nếu ghi `"where": "nguồn yếu: …"` (quyết định 31).
- **Đọc văn bản gốc**: trích nguyên văn (Hy Lạp, Latin, Anh, Pháp, Đức, chữ Hán). Mở văn bản gốc (Gutenberg, Perseus, Wikisource, ctext, marxists.org, Internet Archive) và so từng chữ, ghi đúng vị trí.
  - Bản dịch của site ("bản dịch của Logos"): dịch sai nghĩa là `sai`, mức `nghiem-trong`; chỉ vụng là `nhe`.
  - Văn bản còn bản quyền: mỗi trích dẫn tối đa 1–2 câu. Trích dài hơn thì `sai`, mức `vua`.
- **Tự viết**: thường không có dữ kiện. Một claim `dien-giai` cho thấy câu hỏi bám đúng bài.
- **Mọi link nội bộ có mô tả** (Đọc tiếp, "xem bài…", "Đọc thêm"):
  - Mở trang đích trên site đã deploy `https://mtuann.github.io/logos/<đường dẫn không .md>/`.
  - Kiểm nhãn khớp tên trang, và mô tả đúng điều trang đích thật sự có (lượt trước nhiều lỗi ở đây).
  - Trang mới viết hôm nay có thể chưa lên site: khi đó đọc file `docs/…` trong repo và ghi `where`.
- **Nguồn**: URL mở được không; tác giả, tên bài, năm có khớp không. SEP ưu tiên bản lưu `plato.stanford.edu/archives/fall2026/entries/<mục>/`. Dòng trùng bản ghi `sources/*` đóng băng thì dùng `kb`.
- **Không dùng Wikipedia làm nguồn** (chỉ dùng để tìm nguồn).

## Việc riêng của 5.8

- **Ba bài Tư tưởng Việt Nam** (`truc-lam`, `nho-giao-viet`, `viet-hien-dai`) dùng nhãn độ chắc chắn **[chắc chắn]** / **[có cơ sở]** / **[suy đoán]** (quyết định 6; chú giải "Cách đọc nhãn độ chắc chắn" trong bài).
  - Mỗi nhận định lịch sử hoặc diễn giải quan trọng phải có nhãn. Nhận định quan trọng thiếu nhãn: `sai`, mức `vua`, `fix` là câu có nhãn.
  - Nhãn phải khớp nguồn: **[chắc chắn]** chỉ khi có văn bản gốc hoặc nguồn học thuật nói thẳng; **[có cơ sở]** khi có nguồn học thuật nhưng còn tranh luận; **[suy đoán]** khi chỉ là cách đọc. Nhãn mạnh hơn nguồn: `sai`, mức `vua`.
  - Ở đây nguồn tiếng Việt (sách, tạp chí, trang các viện, đại học) là chính. Nguồn yếu chấp nhận nếu ghi `"where": "nguồn yếu: …"` (quyết định 31).
- **Việc đã ghi sẵn từ trước** (`ban-giao/viec-cho.md`). Kiểm kỹ và ghi claim riêng cho từng việc:
  - `viet-hien-dai`, lập trường 2 "con đường của Trần Đình Hượu": thuận/nghịch, "Tây hóa toàn diện", so sánh Nhật Bản, "dành cả sự nghiệp", cùng câu hỏi dẫn dắt, quiz và Tự viết dựa trên các ý ấy. Bài tự ghi "chưa đối chiếu được nguyên bản". Nguồn hiện có chỉ là trang tin ĐHQG Hà Nội và ĐH KHXH&NV. Tìm sách hoặc bài nghiên cứu mở được. Ý nào không có nguồn: `sai` kèm `fix` bỏ hoặc làm dè dặt.
  - `nho-giao-viet`, lập trường 2: ai theo lập trường "Việt hóa"? Cần nguồn; không có thì `fix` bỏ phần gán tên.
  - `duc-tin-ly-tri`, lập trường 1 và Tóm tắt: "bước nhảy (đức tin)" được dùng như thuật ngữ của Kierkegaard. Theo SEP (*Søren Kierkegaard*), "leap" gắn với hành động tự do trong *Khái niệm lo âu*; chuyển nấc là biến đổi các "đam mê"; chuyện Abraham là câu hỏi diễn giải ("đình chỉ đạo đức vì một mục đích cao hơn"). Kiểm và ghi `fix` cho đúng SEP.
  - `mo-phong`: "ác quỷ" (Descartes). Các trang khác dùng "ác thần" (`grep -rn "ác thần\|ác quỷ" docs/`). Không thống nhất: `sai`, mức `nhe`, `fix` dùng "ác thần".
- **`thoi-gian`, lập trường 3 "Khối đang lớn"**: vừa viết thêm ba nhãn (nguồn: SEP *Charlie Dunbar Broad*, SEP *Presentism*, IEP *Time*). Kiểm như mọi lập trường khác.

## Kho dữ kiện đã đóng băng

Nếu một dữ kiện của bài **trùng đúng** một bản ghi, ghi claim `dung` với `"kb": "<khóa>"` thay cho `sources`:

- `people/<id>`: `data/kb/people.yml`
- `works/<id>`: `data/kb/works.yml`
- `quotes/<id>`: `data/kb/quotes.yml`
- `sources/<id>`: `data/kb/sources.yml`
- `events/<id>`: `data/kb/events.yml`
- `philpapers/<id>`: `data/kb/philpapers-2020.json`
- `ho-so/<id>`: `data/people/<id>.yml`
- `terms/<id>`: thuật ngữ

Chỉ dùng khóa có `"status": "frozen"` trong `verification/ledger.json`. Nếu bài **khác** bản ghi, đó là một claim cần kiểm bằng nguồn: ghi `sai` nếu nguồn ủng hộ bản ghi.

## Trích nguồn: phải là nguyên văn

Lượt kiểm 5.5 có 163 `quote` hóa ra là câu tóm tắt của công cụ đọc web, không phải chữ trên trang. Vì vậy:

- `sources[].quote` phải là **chuỗi có thật, từng chữ**, trên trang bạn mở **trong phiên này**.
- Cách chắc nhất: tải trang bằng `curl -sL <url>` (không giả User-Agent), bỏ thẻ HTML, rồi chép đúng đoạn chữ. Sau khi ghi file, script của người duyệt sẽ so mọi `quote` với trang tải về.
- Không dùng trí nhớ. Không viết lại cho gọn. Có thể cắt bớt, nhưng phần giữ lại phải đúng chữ.
- Trang chặn công cụ (ctext.org, cbetaonline, trang có kiểm tra chống bot): theo quyết định 34 (KE-HOACH.md), claim "URL đúng" ghi `dung` khi nội dung đã đối chiếu ở bản khác và URL đúng mẫu đường dẫn. Không vượt kiểm tra chống bot.
- Gutenberg bảo trì thì dùng mirror `gutenberg.pglaf.org`. Thử bản khác: Wikisource, Internet Archive (`_djvu.txt`), `web.archive.org/web/2026/<url>`, Crossref API cho DOI.
- Không mở được thì ghi `chua-kiem-duoc`, kèm `notes` ghi rõ đã thử những URL nào. Không đoán.

## Mỗi claim

- `text`: chép nguyên câu (hoặc cụm) của bài.
- Claim `sai` cần `severity` (`nghiem-trong`, `vua`, `nhe`), `sources`, và `fix`.
  - `fix` là **câu thay thế cụ thể**, viết bằng tiếng Việt theo văn phong bài (đọc `HUONG-DAN-VIET.md`), chỉ đổi đúng chỗ sai.
  - `fix` phải dán thẳng được vào bài. Không viết "nên sửa thành…" hay "cân nhắc…".
- Câu vụng, chính tả: `nhe`. Không đề xuất viết lại vì văn phong.

## File bằng chứng

`verification/evidence/cau-hoi__<trang>.md__<id>.json`, ví dụ `verification/evidence/cau-hoi__tri-thuc.md___dau.json`.

- `unit`: khóa đầy đủ.
- `hash`: mã băm hiện tại.
- `checked_on`: ngày kiểm (YYYY-MM-DD).
- `checker`: mã được giao.
- `checklist`: bắt buộc, đủ 5 khóa (`true`, `false` hoặc `null`).
- `result`:
  - `dat` nếu không có claim `sai` mức `nghiem-trong` hay `vua`, và không có claim `chua-kiem-duoc`;
  - `sua` nếu có lỗi;
  - `chua-kiem-duoc` nếu còn claim chưa kiểm được.
- **Ghi file ngay sau mỗi đơn vị.** Phiên có thể bị ngắt.
- Sau mỗi file, kiểm schema:

      uv run python -c "import json,jsonschema,sys;s=json.load(open('schema/evidence.schema.json'));jsonschema.validate(json.load(open(sys.argv[1])),s);print('ok')" verification/evidence/<file>.json

## Báo cáo cuối

Trả về ngắn gọn:

- số đơn vị đã ghi, số `dat`/`sua`/`chua-kiem-duoc`;
- danh sách claim `sai`: khóa, mức, một dòng mô tả;
- claim `chua-kiem-duoc`: khóa, một dòng lý do.

Không chép lại toàn bộ bằng chứng.
