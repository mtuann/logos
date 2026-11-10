# Báo cáo linter dữ kiện

Sinh bằng `python tools/lint_facts.py --write`. Phạm vi: Lõi viết tay, bỏ mục Nguồn. So với `data/kb/works.yml` và `data/kb/people.yml`. Đây là báo cáo nền của đợt 2: chỉ ghi lại, sửa ở đợt 5.

**0 chỗ** ở **0 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `nam-tac-pham` | năm của tác phẩm khác năm đã chốt trong works.yml | 0 |
| `nam-chua-chot` | tác phẩm có nhiều năm khác nhau giữa các trang, works.yml chưa chốt | 0 |
| `nam-song` | năm sinh mất khác people.yml | 0 |
