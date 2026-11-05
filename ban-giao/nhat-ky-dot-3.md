# Nhật ký Đợt 3 — Tách thời sự và số đếm

Mỗi dòng một việc đã xong hoặc đang dở. Phiên sau đọc từ đây và làm tiếp.

| Ngày | Việc | File | Trạng thái | Còn gì |
|---|---|---|---|---|
| 2026-11-05 | Brief đợt 3 theo `ban-giao/mau-dot.md`; khảo sát: 90 chỗ `lint_volatile` (lọc theo nghĩa còn 7 đoạn cần dời ở 7 trang), 44 bảng PhilPapers ở 42 trang (135 ô khớp JSON từng chữ khi ghép thô), số đếm nội dung site ở 7 trang hệ thống; quyết định 20 (chủ biên chọn Đề xuất) | `ban-giao/dot-3.md`, `KE-HOACH.md` | xong | việc tiếp: 3.1 |
| 2026-11-05 | 3.1 Khung khối thời sự: shortcode `[[thoi-su:id]]` trong `hooks/kb.py` (mở trước shortcode khác; khối nhiều dòng nhận thụt lề của dòng chứa shortcode; khóa sai trang thì build dừng), `load_context` thay `load_registry` cho handler; `schema/thoi-su.schema.json`; `tools/thoi_su_check.py --check` vào CI; `book.py` mở khối thời sự trước khi viết lại link. Mục `data/thoi-su/` trong `content.yml` thêm ở 3.3 (khi thư mục có file) | `hooks/kb.py`, `schema/thoi-su.schema.json`, `tools/thoi_su_check.py`, `tools/book.py`, tests, CI, `AGENTS.md`, `README.md` | xong: 11 kiểm thử mới; parity 100% | việc tiếp: 3.2 |
