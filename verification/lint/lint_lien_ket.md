# Báo cáo linter link triết gia

Sinh bằng `python tools/lint_lien_ket.py --write`. Phạm vi: Lõi viết tay. Lần đầu nhắc một triết gia đã có hồ sơ thì đặt link tới trang hồ sơ (README, "Thêm nội dung"); sửa trong đợt con của trang (ban-giao/dot-5.md).

**3 chỗ** ở **2 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `thieu-link` | bài nhắc triết gia đã có hồ sơ mà không link tới trang hồ sơ | 3 |
| `mien-thua` | mục miễn không còn khớp chỗ nào | 0 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `cau-hoi/bien-gioi-di-cu.md:49` | `cau-hoi/bien-gioi-di-cu.md#cac-lap-truong-chinh` | `thieu-link` | Nozick (nozick) | đặt link ở lần nhắc đầu: [Robert Nozick](../triet-gia/nozick.md) |
| `cau-hoi/bien-gioi-di-cu.md:49` | `cau-hoi/bien-gioi-di-cu.md#cac-lap-truong-chinh` | `thieu-link` | Rawls (rawls) | đặt link ở lần nhắc đầu: [John Rawls](../triet-gia/rawls.md) |
| `cong-cu/suy-dien.md:94` | `cong-cu/suy-dien.md#nhung-khuon-dang-tin` | `thieu-link` | Socrates (socrates) | đặt link ở lần nhắc đầu: [Socrates](../triet-gia/socrates.md) |
