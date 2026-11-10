# Báo cáo linter số liệu khảo sát

Sinh bằng `python tools/lint_so_lieu.py --write`. Phạm vi: Lõi viết tay, `thi-nghiem.json`, chữ trong `tools/figures.py`. Số liệu PhilPapers chỉ lấy từ `data/kb/philpapers-2020.json` (quyết định 3); số gõ tay trùng kho đổi thành `[[pp:…]]` sau khi `philpapers/*` đóng băng (ban-giao/dot-5.md 5.2).

**0 chỗ** ở **0 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `go-tay` | % khảo sát gõ tay trùng số trong kho: đổi thành `[[pp:…]]%` | 0 |
| `ngoai-kho` | % trong ngữ cảnh khảo sát mà kho không có: đối chiếu số liệu chính thức | 0 |
| `quiz` | % trong câu hỏi, đáp án đúng hoặc lời giải của quiz mà kho không có | 0 |
| `du-lieu` | % khảo sát gõ tay trong dữ liệu luyện tập hoặc trong chữ của hình | 0 |
| `mien-thua` | mục miễn không còn khớp chỗ nào | 0 |
