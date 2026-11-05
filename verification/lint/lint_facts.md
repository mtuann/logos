# Báo cáo linter dữ kiện

Sinh bằng `python tools/lint_facts.py --write`. Phạm vi: Lõi viết tay, bỏ mục Nguồn. So với `data/kb/works.yml` và `data/kb/people.yml`. Đây là báo cáo nền của đợt 2: chỉ ghi lại, sửa ở đợt 5.

**3 chỗ** ở **2 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `nam-tac-pham` | năm của tác phẩm khác năm đã chốt trong works.yml | 0 |
| `nam-chua-chot` | tác phẩm có nhiều năm khác nhau giữa các trang, works.yml chưa chốt | 3 |
| `nam-song` | năm sinh mất khác people.yml | 0 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `cau-hoi/dao-duc-hanh-dong.md:68` | `cau-hoi/dao-duc-hanh-dong.md#cac-lap-truong-chinh` | `nam-chua-chot` | *Utilitarianism* (1863) | `mill.utilitarianism` gặp với các năm 1861, 1863 |
| `cau-hoi/dao-duc-hanh-dong.md:141` | `cau-hoi/dao-duc-hanh-dong.md#doc-van-ban-goc` | `nam-chua-chot` | *Utilitarianism* (1863) | `mill.utilitarianism` gặp với các năm 1861, 1863 |
| `cau-hoi/noi-doi.md:144` | `cau-hoi/noi-doi.md#doc-van-ban-goc` | `nam-chua-chot` | *Utilitarianism* (1863) | `mill.utilitarianism` gặp với các năm 1861, 1863 |
