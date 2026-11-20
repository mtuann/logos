# Soạn bảng thay chữ theo bằng chứng 5.8

Repo: `/Users/mitu/Desktop/work/projects/logos`. Bạn là **người soạn bảng sửa**. Bạn **không sửa file nào trong repo** và không commit. Bạn chỉ ghi file trong thư mục `/Users/mitu/Desktop/work/projects/logos/ban-giao/dot-5.8/sua/`.

## Đầu vào

`sai-5.8.json` (cùng thư mục) gom theo trang mọi claim `sai` chưa sửa: `unit`, `severity`, `text` (câu của bài), `fix` (câu thay thế người kiểm đề xuất) và `evidence_file` (file bằng chứng đầy đủ, có `sources` và `notes`).

Đọc trước:

- `HUONG-DAN-VIET.md`: văn phong, bảng thuật ngữ bắt buộc, cú pháp Markdown.
- `AGENTS.md` mục 3, các luật cứng.

## Việc

Với **mỗi trang được giao**, ghi file `sua/<tên-trang>.json`. File là danh sách các mục `[path, old, new]`:

- `path`: ví dụ `"docs/cau-hoi/khoa-hoc.md"`.
- `old`: chuỗi **có thật, đúng từng ký tự**, trong file hiện tại, và chỉ xuất hiện **một lần**. Lấy đủ dài để không trùng chỗ khác.
- `new`: chuỗi thay thế, áp đúng ý của `fix`.

Cách làm cho từng claim:

1. Mở file bằng chứng và đọc `fix`, `sources`, `notes`. Rồi tìm đúng chỗ trong bài. Một claim có thể chạm nhiều chỗ (ví dụ Tóm tắt, thân bài, lời giải quiz cùng một lỗi); sửa đủ các chỗ người kiểm chỉ ra.
2. `fix` thường đã là câu dán thẳng được. Nếu `fix` chỉ mô tả cách sửa, hoặc viết chưa hợp văn phong, hãy viết câu thay thế:
   - đúng ý `fix`;
   - không thêm dữ kiện mà `sources` của bằng chứng không ủng hộ;
   - chỉ đổi đúng chỗ sai.
3. Giữ nguyên:
   - id tiêu đề `{#…}`;
   - `data-id` và thứ tự phương án của quiz, chỉ số `answer`;
   - shortcode `[[pp:…]]`, `[[thoi-su:…]]`;
   - link không bị chỉ ra là sai.

   Dòng quiz là JSON nằm trong Markdown. Chuỗi mới phải giữ JSON hợp lệ: dùng ngoặc kép cong “ ” bên trong chuỗi, như bài đang dùng.
4. Thuật ngữ: làm theo bảng bắt buộc. Nếu một `fix` về thuật ngữ mâu thuẫn với bảng hoặc với cách dùng thống nhất ở các trang khác (dùng `grep` trong `docs/`), đừng áp; ghi vào báo cáo.
5. Không áp một `fix` khi:
   - nó cần dữ kiện mới chưa có nguồn đã mở;
   - nó đổi cấu trúc lớn, như thêm hay bỏ cả một lập trường;
   - nó mâu thuẫn với claim khác.

   Ghi những trường hợp đó vào báo cáo kèm lý do. Riêng claim thiếu nhãn ba phần ("Lập luận mạnh nhất / Phản bác chính / Cách đáp lại") thì áp nếu `fix` có sẵn đoạn văn dựa trên nguồn đã mở.
6. Mỗi file `sua/<trang>.json` đặt các mục theo đúng thứ tự xuất hiện. Kiểm bằng:

       cd /Users/mitu/Desktop/work/projects/logos && uv run python /Users/mitu/Desktop/work/projects/logos/ban-giao/dot-5.8/tools/check_rep.py <file>

   Lệnh phải in `ok`.
7. Ghi kèm `sua/<trang>.map.json`: danh sách `{"unit": …, "claim_index": …, "rows": [chỉ số các mục trong bảng], "applied": true/false, "why": "…"}`. Người áp dùng file này để đặt `fixed: true` cho claim.

## Báo cáo cuối

Ngắn gọn:

- số claim đã áp / không áp cho mỗi trang;
- danh sách claim không áp, mỗi claim một dòng lý do;
- các câu thay thế mà bạn viết khác hẳn `fix` gốc, kèm lý do.

## Riêng 5.8

- **Câu bổ sung PhilPapers.** Nhiều trang viết câu bổ sung "chỉ hỏi những người chọn trả lời thêm". Thống nhất theo cách các trang đã đóng băng đang viết: "(mỗi câu bổ sung được hỏi một phần sáu số người tham gia, chọn ngẫu nhiên, cộng với những người tự chọn trả lời thêm)", hoặc dạng ngắn hơn cùng ý nếu câu đã dài.
- **"Không lựa chọn nào vượt quá…"** mâu thuẫn với "Khác": đổi thành "không lập trường cụ thể nào…".
- **Nhãn độ chắc chắn** ở `truc-lam`, `nho-giao-viet`, `viet-hien-dai`: giữ đúng dạng `**[chắc chắn]**`, `**[có cơ sở]**`, `**[suy đoán]**`. Không đưa nhãn vào Tóm tắt nếu Tóm tắt hiện chưa có.
- **`viet-hien-dai`, lập trường 2 (Trần Đình Hượu)**: đây là việc đã giao từ trước (`ban-giao/viec-cho.md`, dòng 10/11). Được phép viết lại cả đoạn, kể cả mục Đọc văn bản gốc, quiz `vietnam-3` (giữ `data-id`, giữ số phương án và chỉ số `answer`, nếu cần thì đổi chữ của phương án) và Tự viết, miễn mọi câu mới chỉ dùng ý có nguồn trong bằng chứng. Ngoại lệ với mục 5 về "đổi cấu trúc lớn" chỉ áp cho trang này.
- **Thuật ngữ**: "ác thần" (không dùng "ác quỷ"); *epistemology* là "tri thức luận"; *theodicy* là "biện thần luận"; "tương đồng gia đình" (thuật ngữ đã đóng băng).
- **Khối sinh tự động** (`<!-- fig:… -->`, hình trong `tools/figures.py`): không sửa; ghi vào báo cáo.
