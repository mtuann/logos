# Nhật ký Đợt 1 — Công cụ nền

Mỗi dòng một việc đã xong hoặc đang dở. Phiên sau đọc từ đây và làm tiếp.

| Ngày | Việc | File | Trạng thái | Còn gì |
|---|---|---|---|---|
| 2026-11-05 | 1.1 Thư viện `tools/lz/` (registry, units, normalize, hashing) + kiểm thử | `tools/lz/*.py`, `tests/test_lz.py`, `README.md` | xong trên nhánh `dot-1-lz`: 35 kiểm thử; chuẩn hóa làm trên nguồn Markdown (không nạp thư viện render); ID dự phòng khớp anchor H2 của HTML đã build ở 178/180 trang (2 trang còn lại có H2 nằm trong khối sinh, không thành đơn vị); Lõi viết tay 887 đơn vị H2, khớp báo cáo nền | chủ biên duyệt, mở PR; việc tiếp: 1.2 `tools/parity.py` |
| 2026-11-05 | 1.1 merge vào `main` (chủ biên: merge thẳng, push một lần khi xong đợt 1) | — | xong | — |
| 2026-11-05 | 1.2 `tools/parity.py`: so văn bản hiển thị trong article, `<title>`, description, danh sách id; `--base REF` tự build qua git worktree | `tools/parity.py`, `tests/test_parity.py`, `README.md`, `AGENTS.md` | xong: `main` → cây làm việc giống 100% (181 trang); thử đổi một năm và một ID thì báo lệch đúng hai chỗ; 5 kiểm thử | việc tiếp: 1.3 |
