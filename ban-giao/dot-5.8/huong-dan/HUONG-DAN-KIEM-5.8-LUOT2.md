# Hướng dẫn kiểm 5.8, lượt 2: kiểm lại đơn vị đổi chữ và claim còn mở

Repo: `/Users/mitu/Desktop/work/projects/logos`. Bạn là **agent kiểm**.

- Chỉ sửa file `verification/evidence/cau-hoi__<trang>.md__*.json` của các đơn vị được giao.
- Không sửa bài, không commit, không đổi nhánh git.
- File tạm đặt trong thư mục riêng `${TMPDIR:-/tmp}/logos-5.8/<mã của bạn>/`.

Đọc trước:

- `ban-giao/kiem-chung.md`;
- `schema/evidence.schema.json`;
- hướng dẫn lượt 1 `/Users/mitu/Desktop/work/projects/logos/ban-giao/dot-5.8/huong-dan/HUONG-DAN-KIEM-5.8.md`, nhất là mục "Trích nguồn: phải là nguyên văn".

## Danh sách đơn vị

- `changed.json`: các đơn vị đã đổi chữ sau lượt 1.
- `open.json`: các đơn vị còn claim `chua-kiem-duoc`.

Cả hai file nằm trong `ban-giao/dot-5.8/` (người điều phối sinh trước lượt 2, xem README). Bạn chỉ làm các đơn vị thuộc trang được giao, có trong ít nhất một trong hai danh sách.

## Việc cho mỗi đơn vị

1. **Đọc bài hiện tại** (`docs/cau-hoi/<trang>.md`, phần của đơn vị) và đối chiếu từng claim cũ trong file bằng chứng.
   - Claim `sai` có `fixed: true`: kiểm câu mới trong bài có đúng ý `fix` và khớp `sources` không. Đúng thì giữ `fixed: true`. Nếu câu mới lại sai, hoặc thêm điều không có nguồn, thì đặt `fixed: false` và ghi một claim `sai` mới kèm `fix`.
   - Claim `dung`: nếu câu bài đã đổi, cập nhật `text` cho khớp chữ mới. Nếu ý mới cần nguồn khác thì kiểm lại.
   - **Chữ mới không ứng với claim cũ nào** (người sửa có thể đã đổi thêm, ví dụ đồng bộ thuật ngữ, quiz, Tóm tắt): ghi claim mới và kiểm như lượt 1.
   - Khối thời sự `[[thoi-su:…]]` (ví dụ con số GiveWell ở `cuu-giup-ngheo-doi`) không kiểm ở đây, chỉ kiểm câu bao quanh.
2. **Claim `chua-kiem-duoc`**: tìm nguồn khác và mở được.
   - Ưu tiên văn bản gốc, SEP và IEP (bản lưu fall2026), bản số hóa hợp lệ (Internet Archive `_djvu.txt` của bản không khóa, Wikisource, Gutenberg qua mirror `gutenberg.pglaf.org`), Crossref, Europe PMC, PhilArchive, trang tác giả.
   - Theo quyết định 34 (KE-HOACH.md): không vượt kiểm tra chống bot, không giả User-Agent.
   - Nếu chỉ có nguồn thứ cấp đáng tin (SEP, IEP, sách học thuật có trích) nói đúng ý, ghi `dung` và ghi rõ nguồn thứ cấp trong `where`.
   - Nếu sau khi thử kỹ mà vẫn không có nguồn nào, chuyển claim thành `sai`:
     - mức `nhe` nếu chi tiết phụ, mức `vua` nếu là ý chính;
     - `fix` là câu dán thẳng được: bỏ chi tiết, chuyển trích dẫn thành diễn ý không gán nguyên văn, hoặc ghi "theo một cách đọc".
     - Không để lại `chua-kiem-duoc` trừ khi thật sự không thể quyết.
3. **Cập nhật file**:
   - `hash`: mã băm **hiện tại** (`uv run python tools/check_ledger.py --hash "<khóa>"`).
   - `checked_on`: ngày kiểm (YYYY-MM-DD).
   - `checker`: giữ mã cũ, thêm ` + <mã của bạn>`.
   - Cập nhật `checklist`.
   - `result`:
     - `dat` nếu không còn claim `chua-kiem-duoc`, và mọi claim `sai` có mức `nhe` hoặc `fixed: true`;
     - `sua` nếu còn lỗi `vua` hoặc `nghiem-trong` chưa sửa;
     - `chua-kiem-duoc` nếu còn claim chưa kiểm được.
   - Thêm một dòng "Lượt 2: …" vào `notes`.
4. Kiểm schema sau mỗi file:

       uv run python -c "import json,jsonschema,sys;s=json.load(open('schema/evidence.schema.json'));jsonschema.validate(json.load(open(sys.argv[1])),s);print('ok')" <file>

   Mọi `quote` mới phải là nguyên văn trên trang bạn tải trong phiên này; tự so bằng script trước khi ghi.


## Chỗ còn sót, người soạn bảng sửa ghi lại

Các chỗ dưới đây chưa bị chấm ở lượt 1 nhưng cùng loại với lỗi đã sửa, hoặc lệch với phần đã sửa. Với chỗ thuộc trang của bạn, nếu thấy đúng là lỗi thì ghi claim `sai` kèm `fix` dán thẳng được, đặt vào đúng đơn vị (đơn vị đó vào danh sách của bạn dù không có trong `changed.json` hay `open.json`):

- nho-giao-viet: Tóm tắt ý 2, lập trường 2 (dòng ~82 "trừ bạo là bổn phận"), quiz câu 1 phương án 1 vẫn gộp "trừ bạo" vào định nghĩa nhân nghĩa (去暴 thuộc vế 吊伐之師). Thân bài dòng ~63 "tam cương ngũ thường [chắc chắn]".
- truc-lam: đoạn mới nhắc Cảnh Đức truyền đăng lục (1004) nhưng Nguồn chưa có.
- tu-do-ngon-luan: Tóm tắt (dòng ~15) và Đọc văn bản gốc (~117) vẫn tóm Popper "bar rất cao", chưa có ý chú thích 4 ch.7.
- hanh-phuc: thân bài dòng ~83 "Nguy cơ lớn nhất… gia trưởng".
- duc-tri: lời giải quiz "kẻ cầm quyền đứng ngoài luật" (câu điều kiện, để nguyên?).
- khe-uoc-xa-hoi: hình fig:khe-uoc "ai cũng chống ai" → "chưa có quyền lực chung" (tools/figures.py) — CHƯA áp, làm riêng. Anderson Private Government (2017) chưa có ở Nguồn.
- bien-gioi-di-cu: "Carens (1987; 2013)" nhưng Nguồn chỉ có 1987.
- cong-ly: dòng ~62 "sinh ra ngẫu nhiên" (Harsanyi).
- thoi-gian nguon#7 thêm IEP Time → bản ghi nguồn mới (cần accessed? ghi sổ + bằng chứng, đóng băng 5.2).
- mo-phong: quiz meta-c4 câu 5 số % gõ tay 27,5/54,2; Tóm tắt và quiz câu 4 vẫn xếp Putnam dưới "phản bác tính khoa học".
- nghe-thuat: hình fig:ho-khai-niem "Tương tự họ" → "tương đồng gia đình" (tools/figures.py) — làm cùng nhánh hình khe-uoc.
- cai-dep: Tóm tắt dòng ~13 "người phê bình lý tưởng".
- duc-tin-ly-tri: hình fig:pascal-wager "Mất mát vô hạn / hình phạt đời đời" (tools/figures.py). Front matter description, H3 "Kierkegaard: đức tin là bước nhảy vượt lên trên lý trí", Phản bác chính lập trường 1, mở bài vẫn dùng "bước nhảy" — việc viec-cho, phải sửa hết.
- luan-chung-ton-giao: quiz giải thích "nhiều triết gia vô thần vẫn coi…"; H3 "mọi sự đều có nguyên nhân" và dòng ~42.
- van-de-su-du: "biện hộ" còn dùng cho theodicy ở Tóm tắt, mô tả, Hick ("biện hộ linh hồn-tôi luyện").
- viet-hien-dai: nguồn mới Gadkar-Wilcox 2014 (DOI 10.1017/S0021911813002349) → bản ghi nguồn mới. Hình fig:vietnam-timeline "Trần Đình Hượu (1996)". Lập trường 1 Phản bác chính "Trần Đình Hượu sẽ nói: không…" (gán lời). Có thể thêm phản bác Nguyễn Kiến Giang ("có phần cường điệu").

Hình trong khối `<!-- fig:… -->` (khe-uoc, ho-khai-niem, pascal-wager) người áp đã sửa ở `tools/figures.py`: chỉ kiểm chữ mới.

## Báo cáo cuối

Trả về ngắn gọn:

- số đơn vị theo `result`;
- claim `sai` mới, hoặc claim `fixed` bị bác (khóa, mức, một dòng, `fix`);
- claim còn `chua-kiem-duoc` (khóa, lý do).
