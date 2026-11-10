# Báo cáo linter trích dẫn

Sinh bằng `python tools/lint_quotes.py --write`. So khối `!!! quote` của Lõi viết tay với `data/kb/quotes.yml`. Đây là báo cáo nền của đợt 2: chỉ ghi lại, bổ sung ở đợt 5.

**0 chỗ** ở **0 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `khong-khop` | khối trích trong trang không khớp bản ghi nào trong quotes.yml | 0 |
| `mo-coi` | bản ghi trỏ tới đơn vị không còn chứa khối trích | 0 |
| `chua-ghep-tac-pham` | bản ghi chưa ghép với tác phẩm trong works.yml và chưa có lý do (work_note) | 0 |
| `chua-co-vi-tri` | bản ghi chưa có vị trí trích (locator) | 0 |
