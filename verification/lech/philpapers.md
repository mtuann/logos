# Danh sách lệch: số liệu PhilPapers 2020

Sinh bằng `python tools/kb_philpapers.py --import-md` (đợt 2); cập nhật tay ở đợt con 5.2 (9/11/2026) sau khi kiểm
với Bảng 1–2 của bài báo, đọc ở PhilArchive (`https://philarchive.org/archive/BOUPOP-3`; trang nhà xuất bản chặn công cụ tải).

- 100 câu (câu chính 40, câu bổ sung 60), đủ số câu của khảo sát. 13 câu bổ sung còn thiếu được thêm ở 5.2 từ Bảng 2,
  nhãn tiếng Việt do Claude dịch (chủ biên duyệt lại cùng mẫu 5.2): Giả thuyết continuum, Nền tảng của toán học, Nền tảng
  của ý hướng tính, Siêu hình học liên tầng, Siêu bản thể học, Phương pháp nghiên cứu lịch sử triết học, Khái niệm chuẩn
  tắc, Thái độ mệnh đề, Mệnh đề, Nội dung ngữ nghĩa, Người đẹp ngủ, Không–thời gian, Đơn vị chọn lọc.
- id câu và lựa chọn là slug của nhãn tiếng Việt (file gốc không có nhãn tiếng Anh); hai id mới rút gọn tay:
  `khong-thoi-gian`, `nguoi-dep-ngu-sleeping-beauty`.

## Ô không theo quy ước một chữ số thập phân (0)

Đã xử lý ở 5.2: bài báo in đủ một chữ số thập phân ("9.0", "58.0", "48.0", "45.0", "16.0", "35.0"); trường `raw` của
năm ô dưới đây bị bỏ, trang in "9,0", "58,0"… như mọi ô khác.

- `phai-keo-theo-co-the-ought-implies-can.khac`: pct = "9" → 9,0
- `phuong-phap-triet-hoc-chinh-tri.ly-thuyet-phi-ly-tuong`: pct = "58", pct_exclusive = "48" → 58,0; 48,0
- `luat-phap.phi-thuc-chung-luan-phap-ly`: pct = "45" → 45,0
- `luat-phap.khac`: pct = "16" → 16,0
- `cau-thanh-vat-chat-khi-nao-nhieu-vat-hop-thanh-mot-vat.doi-khi-han-che-luan`: pct = "35" → 35,0

## Sửa khác theo bằng chứng 5.2

- `ban-chat-cua-dao-duc`: n ≈ 1030 → 1020 (trang kết quả: N = 1024).
- `phan-doan-dao-duc`: n ≈ 1630 → 1640 (N = 1636).
- `platon-quan-diem-cua-ong-la-gi`: nhãn "Chỉ có tri thức về các Form" → "Chỉ có tri thức về các Ý niệm (*Form*)" (thuật ngữ
  "Ý niệm (thuyết Platon)" của từ điển).
