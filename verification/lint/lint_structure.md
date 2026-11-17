# Báo cáo linter cấu trúc

Sinh bằng `python tools/lint_structure.py --write`. Phạm vi: Lõi viết tay và dữ liệu Lõi có văn xuôi. Đây là báo cáo nền của đợt 1: chỉ ghi lại; bổ sung mục hay ghi ngoại lệ là quyết định của chủ biên.

**2 chỗ** ở **1 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `thieu-muc` | thiếu mục H2 bắt buộc theo loại trang (KE-HOACH.md mục 5.1) | 2 |
| `thieu-tom-tat` | bài cau-hoi thiếu hộp "Tóm tắt 5 phút" | 0 |
| `nhan-chac-chan` | nhãn độ chắc chắn ngoài bài có chú giải, hoặc trong front matter/dữ liệu | 0 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `cong-cu/luan-cu-thep.md` | — | `thieu-muc` | Bài tập | thêm mục, hoặc ghi ngoại lệ (quyết định của chủ biên) |
| `cong-cu/luan-cu-thep.md` | — | `thieu-muc` | Tự kiểm tra | thêm mục, hoặc ghi ngoại lệ (quyết định của chủ biên) |
