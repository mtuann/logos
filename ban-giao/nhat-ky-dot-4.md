# Nhật ký Đợt 4 — Giao diện tối thiểu

Mỗi dòng một việc đã xong hoặc đang dở. Phiên sau đọc từ đây và làm tiếp.

| Ngày | Việc | File | Trạng thái | Còn gì |
|---|---|---|---|---|
| 2026-11-05 | Chủ biên duyệt danh sách miễn của `lint_volatile` (61 mục) | `KE-HOACH.md` (quyết định 20), `data/style/volatile-allow.yml` | xong | — |
| 2026-11-05 | Brief đợt 4 theo `ban-giao/mau-dot.md`; quyết định 21–24 (font tự host, tìm kiếm bỏ dấu ở trình duyệt, một trang chỉ mục tác phẩm, trang chủ sắp xếp lại; chủ biên chọn Đề xuất) | `ban-giao/dot-4.md`, `KE-HOACH.md` | xong | việc tiếp: 4.1 |
| 2026-11-05 | 4.1 Thêm `playwright@1.64.1` (devDependency, ghim; axe nạp từ `axe-core` 4.13.0 có sẵn, không thêm `@axe-core/playwright`); `tests/real/` (máy chủ tĩnh, 10 trang mẫu), `npm run test:real` quét axe WCAG 2.2 AA cả trang trên Chromium: 40 lần quét; `npm run anh` chụp 40 ảnh vào `site-anh/` (gitignore). Báo cáo nền `verification/giao-dien/axe-nen.md`: 1.430 phần tử vi phạm, 4 luật (link-in-text-block 1.320, color-contrast 58, aria-progressbar-name 40, target-size 12), khớp điểm đo ngày 3/11. CI: cài Chromium (cache), đo axe (chưa chặn), tải ảnh lên artifact `anh-trang-mau`. Ghi nhận: `npm audit` báo 1 lỗ hổng cao ở `undici` (qua jsdom, có từ trước, chỉ dùng khi kiểm thử) — không sửa trong đợt này | `package.json`, `package-lock.json`, `tests/real/`, `verification/giao-dien/`, CI, `.gitignore`, `AGENTS.md`, `README.md` | xong | việc tiếp: 4.2 |
