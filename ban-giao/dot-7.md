# Đợt 7: Vận hành Mở rộng

- **Thời gian**: kế hoạch ghi từ 26/4/2027; chủ biên mở sớm ngày 20/11/2026. Đợt này không có ngày đóng mà chạy liên tục, mỗi đợt sóng gắn một tag `v1.7.N`.
- **Luật 7 hết hiệu lực**: từ đợt 7 được thêm nội dung mới. Nội dung mới vào tầng **Mở rộng** (`tier: mo-rong`) theo năm ngăn: khối thời sự, bài chuyên đề, hồ sơ triết gia mới, hướng dẫn đọc mới, ngân hàng luyện tập.
- **Lõi không đổi**:
  - Sửa đơn vị Lõi vẫn chỉ qua `[doi-loi]`, kèm bằng chứng mới.
  - Mở rộng được link vào Lõi; Lõi không phụ thuộc Mở rộng.
- **Nhánh**: `dot-7-<ten-ngan>`, mỗi nhánh tối đa 3 đơn vị nội dung, merge `--no-ff` trên máy. Push khi xong một đợt sóng.
- **Tiến độ**: `ban-giao/nhat-ky-dot-7.md`.

## Việc thường kỳ

| Việc | Nhịp | Cách làm |
|---|---|---|
| Rà khối thời sự đến hạn | khi `thoi_su_check` báo (hạn sớm nhất hiện nay: 22/10/2027) | mở lại nguồn, cập nhật `updated_to`, `review_by`; khối là Mở rộng nên không cần `[doi-loi]` |
| Báo lỗi từ người đọc (nhãn `bao-loi`) | trong 7 ngày | khoanh tới đơn vị hoặc bản ghi; Lõi thì `[doi-loi]` kèm bằng chứng |
| Thăng hạng Mở rộng → Lõi | mỗi quý | đơn vị Mở rộng đã ổn định qua một quý, kiểm như đợt 5 (lượt 1, mẫu 10%), rồi đổi `tier` và đóng băng |
| Rà định kỳ mô tả front matter (quyết định 15) | mỗi quý | kiểm `description` của các trang đã đổi trong quý |
| Kiểm link hằng tuần (quyết định 34) | hằng tuần (CI) | cần GitHub Actions chạy được |

## Đợt sóng 7.1: dọn tồn của đợt 5–6

| # | Việc | Loại | Kết quả kiểm được |
|---|---|---|---|
| 7.1.1 | Quy ước ghi sách in (quyết định 36): cùng một sách ghi một kiểu ở mọi mục Nguồn và hồ sơ; gộp bản ghi `sources/sach.*` trùng | cơ học, `[doi-loi]` | `kb_sources`: không còn hai bản ghi cùng tác giả, năm, tên; parity chỉ lệch ở dòng Nguồn đã khai báo; sổ khớp |
| 7.1.2 | Link cho mục Nguồn: 44 tác phẩm trước 1927 thêm Gutenberg, Wikisource hoặc Internet Archive; sách hiện đại thêm DOI hoặc trang nhà xuất bản khi có | nội dung, `[doi-loi]` | mỗi link mới có bằng chứng; số mục không link giảm |
| 7.1.3 | Tìm kiếm xếp theo trang (`viec-cho` 20/11): "tri thuc" đưa `cau-hoi/tri-thuc` vào 5 kết quả đầu | giao diện | kiểm thử mô hình Material |
| 7.1.4 | `cau-hoi/dao-duc-ung-dung.md`: bỏ phần nghèo đói trùng `cuu-giup-ngheo-doi`, bài chỉ bàn động vật (quyết định 32) | nội dung, `[doi-loi]` | kiểm lượt 1 và mẫu cho các đơn vị đổi |

## Danh sách chờ chủ biên xếp ưu tiên (nội dung mới, Mở rộng)

Rút từ `ban-giao/viec-cho.md`. Chủ biên chọn thứ tự; mỗi mục là một hay vài nhánh, kiểm như đợt 5 trước khi merge.

- **Hồ sơ triết gia mới:**
  - Wollstonecraft, Camus, Vương Dương Minh, Lê Quý Đôn, Phan Châu Trinh;
  - theo số lần được nhắc: Gettier, Mackie, J. J. Thomson, Kuhn, Plantinga, Putnam, Ockham, Ayer, Broad…;
  - người còn sống theo quyết định 33: Singer, Chalmers, Nussbaum.
- **Hướng dẫn đọc mới:** Locke (*Khảo luận thứ hai*), Hobbes (*Leviathan* ch. 13), Tuân Tử ("Tính ác"), Trần Thái Tông (*Khóa hư lục*).
- **Bài mới:**
  - Nghịch lý (Zeno, kẻ nói dối, đống cát);
  - Vì sao phải sống có đạo đức? (chiếc nhẫn Gyges);
  - triết học Hồi giáo; tách "Việt Nam" khỏi "Nhật Bản và Việt Nam";
  - các chủ đề PhilPapers chưa có bài: ngôn ngữ, logic và nghịch lý, động cơ đạo đức…
- **Bổ sung cho bài sẵn có:**
  - mục "Đọc văn bản gốc" cho 18 bài Câu hỏi lớn;
  - quiz 5 câu cho 8 hướng dẫn đọc chỉ có 3 câu;
  - trích dẫn tiêu biểu cho 11 hồ sơ chưa có;
  - 11 thuật ngữ mới cho từ điển.
- **Nguồn:** thay nguồn yếu tiếng Việt bằng ấn phẩm Viện Hán Nôm, Viện Văn học (quyết định 31).
- **Công cụ:** Sơ đồ lập luận vẽ được tiền đề liên kết hay độc lập.
