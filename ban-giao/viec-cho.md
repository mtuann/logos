# Việc chờ

Lỗi và ý tưởng phát hiện ngoài phạm vi đợt đang làm. Không sửa ngay: chủ biên xếp vào đợt phù hợp (thường đợt 5 cho lỗi trong Lõi, đợt 7 cho nội dung mới). Mỗi dòng nên có issue GitHub nhãn `cho` tương ứng.

| Ngày | Người ghi | Trang hoặc đơn vị | Mô tả | Loại | Đợt dự kiến |
|---|---|---|---|---|---|
| 2026-10-23 | Claude | `cau-hoi/*` | 18/57 bài không có mục "Đọc văn bản gốc": chốt mục này là bắt buộc hay tùy chọn trong mẫu | quyết định | 1 |
| 2026-10-23 | Claude | `cong-cu/` | Bài mới: Nghịch lý (Zeno, kẻ nói dối, đống cát) | ý tưởng | 7 |
| 2026-10-23 | Claude | `cau-hoi/` | Bài mới: Vì sao phải sống có đạo đức? (chiếc nhẫn Gyges) | ý tưởng | 7 |
| 2026-10-23 | Claude | `lich-su/` | Tách "Việt Nam" khỏi "Nhật Bản và Việt Nam"; thêm bài triết học Hồi giáo | ý tưởng | 7 |
| 2026-10-23 | Claude | `triet-gia/` | Hồ sơ mới: Wollstonecraft, Camus, Vương Dương Minh, Lê Quý Đôn, Phan Châu Trinh | ý tưởng | 7 |
| 2026-10-23 | Claude | `doc/` | Hướng dẫn đọc mới: Locke (*Khảo luận thứ hai về chính quyền*), Hobbes (*Leviathan* ch. 13), Tuân Tử ("Tính ác"), Trần Thái Tông (*Khóa hư lục*) | ý tưởng | 7 |
| 2026-11-03 | Claude | `docs/**` | Chọn kiểu ngoặc kép hiển thị (thẳng "…" hay cong “…”) trước khi đóng băng: đổi sau đợt 5 sẽ mở khóa mọi đơn vị có ngoặc | quyết định | 1–4 |
| 2026-11-03 | Claude | giao diện | Đo bằng axe trên Chromium: link trong bài chỉ khác chữ thường bằng màu (tương phản 2,53:1, cần 3:1 hoặc gạch chân; 26 chỗ ở `cau-hoi/tri-thuc`); chữ xám nhỏ "Cập nhật lần cuối", "Báo lỗi trang này" 2,87:1 (cần 4,5:1); mục menu trái cao 18 px (cần ≥ 24 px), khoảng 14 vùng chạm nhỏ hơn 24 px trên điện thoại; `.md-progress` thiếu `aria-label`. Kiểm thử hiện tại không thấy vì chạy axe trong jsdom, tắt tương phản, chỉ quét `article` | giao diện | 4 |
| 2026-11-03 | Claude | giao diện | Trên điện thoại, màn hình đầu bài chỉ có tiêu đề, nút "In bài này" và khối Tóm tắt 5 phút dày đặc; trang chủ có 6 cửa vào ngang nhau, thiếu một nút "Bắt đầu ở đây"; CSS gọi Be Vietnam Pro và Noto Serif nhưng không tải font nên mỗi máy một kiểu chữ; cột chữ khoảng 83 ký tự mỗi dòng | giao diện | 4 |
| 2026-11-03 | Claude | tìm kiếm | `search_index.json` 5,4 MB (1,6 MB nén) được tải ngay lần mở trang đầu tiên, 52% là bản sao không dấu của `hooks/search_vi.py`; trang Dòng thời gian cho đoạn trích dính chữ trong kết quả tìm | giao diện | 4 |
| 2026-11-03 | Claude | logos-zero (ngoài repo) | `tests/browser/ke-hoach.test.js` hỏng theo ngày từ 27/10/2026 (đã sửa ở logos); `docs/sw.js` xóa mọi cache khác `oz-v1`, kể cả cache của logos. Chỉ ghi nhận: không sửa logos-zero từ repo này | ghi nhận | — |
| 2026-11-03 | Claude | `cau-hoi/cong-ly.md` | Bảng PhilPapers câu bổ sung (phương pháp triết học chính trị) ghi “58%”, “48%”, không có chữ số thập phân như quy ước; đối chiếu lại với kết quả chính thức | lỗi nghi ngờ | 3 hoặc 5 |
| 2026-11-03 | Claude | `cau-hoi/{binh-dang,cong-ly,nu-quyen,tai-san-rieng}.md` | Bảng PhilPapers theo mẫu khác (số kèm dấu %, thêm cột “Chỉ chọn lựa chọn này”). Đợt 3 sinh bảng từ JSON: chốt một mẫu hay hỗ trợ cả hai | quyết định | 3 |
| 2026-11-03 | Claude | `cong-cu/luan-cu-thep.md`, `doc/sartre-hien-sinh.md` | Thiếu mục bắt buộc theo KE-HOACH.md mục 5.1: “Bài tập”, “Tự kiểm tra” (luan-cu-thep); “Đọc từng đoạn” (sartre-hien-sinh). Bổ sung ở đợt 5 hay ghi ngoại lệ cho `lint_structure` | quyết định | 1 hoặc 5 |
| 2026-11-05 | Claude | tìm kiếm | Xếp hạng kém với câu nhiều từ ngắn: "tu do y chi", "tri thuc" không đưa bài chính lên đầu (cả trước và sau đợt 4.5), vì Material thêm `*` vào mọi từ của câu truy vấn nên "y*", "tu*" khớp quá rộng. Cách sửa có thể: bỏ `*` cho từ ≤ 2 chữ cái trong worker, hoặc Pagefind (đợt 6) | giao diện | 6 |
