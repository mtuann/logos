# Báo cáo linter thuật ngữ

Sinh bằng `python tools/lint_terms.py --write`. Phạm vi: Lõi viết tay. Luật: `data/style/terms-policy.yml` (từ `HUONG-DAN-VIET.md` mục 3). Đây là báo cáo nền của đợt 1: chỉ ghi lại, sửa ở đợt 5.

**3 chỗ** ở **2 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `thuat-ngu` | dùng cách dịch khác thay cho thuật ngữ bắt buộc | 0 |
| `thuat-ngu-mo-ho` | cách dịch khác trùng một từ thường hay thuật ngữ khác: người đọc xem lại, thường là đúng | 3 |
| `ten-rieng` | tên riêng không theo cách phiên quy định (ví dụ Plato → Platon) | 0 |
| `mien-lech` | số chỗ của một mục miễn đã đổi: xem lại các chỗ, rồi sửa `count` hoặc sửa chữ | 0 |
| `mien-thua` | mục miễn không còn khớp chỗ nào (xóa mục) | 0 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `cau-hoi/duc-tin-ly-tri.md:58` | `cau-hoi/duc-tin-ly-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/duc-tin-ly-tri.md:58` | `cau-hoi/duc-tin-ly-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/loi-chung.md:119` | `cau-hoi/loi-chung.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
