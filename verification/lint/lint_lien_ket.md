# Báo cáo linter link triết gia

Sinh bằng `python tools/lint_lien_ket.py --write`. Phạm vi: Lõi viết tay. Lần đầu nhắc một triết gia đã có hồ sơ thì đặt link tới trang hồ sơ (README, "Thêm nội dung"); sửa trong đợt con của trang (ban-giao/dot-5.md).

**1 chỗ** ở **1 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `thieu-link` | bài nhắc triết gia đã có hồ sơ mà không link tới trang hồ sơ | 1 |
| `mien-thua` | mục miễn không còn khớp chỗ nào | 0 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `cong-cu/suy-dien.md:94` | `cong-cu/suy-dien.md#nhung-khuon-dang-tin` | `thieu-link` | Socrates (socrates) | đặt link ở lần nhắc đầu: [Socrates](../triet-gia/socrates.md) |
