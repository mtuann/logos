<!-- Một PR, một loại thay đổi, đúng đợt đang mở (AGENTS.md mục 3). CI tự đăng danh sách đơn vị đổi bên dưới. -->

## Đợt và việc

Đợt N, việc N.x: …

## Loại thay đổi

- [ ] Cơ học (script, không đổi chữ): `uv run python tools/parity.py --base main` giống 100%
- [ ] Nội dung Lõi (chỉ đợt 5): mỗi chỗ sửa có bằng chứng trong `verification/evidence/`
- [ ] Mở rộng (từ đợt 7): không sửa file Lõi
- [ ] Công cụ, kiểm thử, tài liệu (không đụng `docs/`)
- [ ] Sửa đơn vị đã đóng băng: PR mang nhãn `doi-loi`, có bằng chứng mới, sổ kiểm chứng đã cập nhật

## Kiểm tra (AGENTS.md mục 4)

generator --check ✓/✗ · content_registry ✓/✗ · add_heading_ids ✓/✗ · check_ledger ✓/✗ · build --strict ✓/✗ · unittest ✓/✗ · npm test ✓/✗

## Câu hỏi mở cho chủ biên

…
