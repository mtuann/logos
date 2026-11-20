# Nhật ký đợt 6

| Ngày | Việc | Trạng thái, còn gì |
|---|---|---|
| 2026-11-20 | Mở đợt 6 (chủ biên yêu cầu): đặc tả `ban-giao/dot-6.md`; quyết định 37 (chỉnh trên nền hiện có), 38 (sửa worker tìm kiếm), 39 (ngoặc cong khi hiển thị) | còn 6.1–6.5 |
| 2026-11-20 | 6.1 tìm kiếm: `search-worker.js` vá `lunr.Query.prototype.clause` — từ ≤ 2 chữ cái bỏ wildcard cuối mà Material thêm; kiểm thử mô hình Material: 0 ca tụt hạng, "tự do ý chí" 8 → 2, "tu do y chi" 59 → 8, "tu do ngon luan" 3 → 1; "tri thuc" không đổi → viec-cho | xong |
| 2026-11-20 | 6.2 ngoặc cong: `hooks/ngoac.py` (on_page_content) đổi "…" → “…” trong nút chữ, bỏ qua code/pre/script/style/kbd/svg/textarea và thuộc tính; `tools/parity.py --bo-kieu-ngoac` (chuẩn hóa cả hai bản); `parity --base main --bo-kieu-ngoac`: giống 100%, 183 trang; không còn ngoặc thẳng trong chữ bài ở site đã build; sổ không đổi | xong |
