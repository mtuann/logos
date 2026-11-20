# Đợt 6: Thiết kế lại giao diện

- **Thời gian**: kế hoạch ghi 15/3–25/4/2027; chủ biên mở sớm ngày 20/11/2026.
- **Điều kiện bắt đầu**: đợt 5 đã đóng. Hiện còn treo: CI chưa chạy được vì tài khoản GitHub lỗi thanh toán, nên chưa có tag `v1.5`.
- **Hướng (quyết định 37)**: chỉnh trên nền thiết kế hiện có.
  - Giữ bảng màu (mực `#26324a`, đất nung `#a3401c`, giấy `#fbfaf7`) và hai font tự host (Be Vietnam Pro, Noto Serif).
  - Giữ Material 9.8.0 + ProperDocs 1.6.7. Không đổi trình render, vì chưa có điều kiện kích hoạt nào ở `KE-HOACH.md` mục 11.
- **Loại thay đổi: giao diện.**
  - Chữ trong bài không đổi. Chỉ đổi CSS, override, hook hiển thị, JS và trang chủ.
  - Không đơn vị Lõi nào bị mở khóa: `check_ledger --check` vẫn khớp.
- **Nhánh**: mỗi việc một nhánh `dot-6-<ten-ngan>`, merge `--no-ff` vào `main` trên máy. Push khi xong cả đợt (AGENTS.md luật 6), rồi gắn tag `v1.6`.
- **Tiến độ**: `ban-giao/nhat-ky-dot-6.md`.

## Việc

| # | Việc | Loại | Kết quả kiểm được |
|---|---|---|---|
| 6.1 | Tìm kiếm (quyết định 38): trong `docs/assets/js/search-worker.js`, từ ≤ 2 chữ cái của câu truy vấn không thêm `*` (khớp nguyên từ), để "tu do y chi" và "tri thuc" đưa bài chính lên đầu (`viec-cho` 5/11) | giao diện | kiểm thử `tests/browser/search.test.js`: "tu do y chi" → `cau-hoi/tu-do-y-chi`, "tri thuc" → `cau-hoi/tri-thuc` ở kết quả đầu; các ca cũ không đổi |
| 6.2 | Ngoặc kép hiển thị (quyết định 26, 39): hook `hooks/ngoac.py` đổi `"…"` thành `“…”` trong chữ của bài lúc build. Bỏ qua `code`, `pre`, `script`, `style`, `kbd`, thuộc tính HTML. Nguồn Markdown không đổi | giao diện | kiểm thử hook; `parity.py --expect-sub` chỉ lệch ở ngoặc; mã băm và sổ không đổi |
| 6.3 | Bố cục bài: nhịp chữ (cỡ, giãn dòng, khoảng cách tiêu đề) theo một thang; hộp Tóm tắt 5 phút, ba nhãn lập trường (**Lập luận mạnh nhất / Phản bác chính / Cách đáp lại**), bảng PhilPapers, quiz, khối thời sự cùng một hệ khung và màu; chế độ tối và bản in kiểm lại | giao diện | parity 100%; axe 0 lỗi ở 10 trang mẫu, hai cỡ màn hình, sáng và tối (`npm run test:real`); `contrast.test.js` có các cặp màu mới |
| 6.4 | Trang chủ: giữ chữ đang có (quyết định 24); bố cục lại các cửa vào thành lưới thẻ, nút "Bắt đầu ở đây" nổi bật, dải "Lõi đã kiểm chứng" dẫn tới trang Kiểm chứng (chữ sinh mang `data-oz-sinh`) | giao diện | parity 100% (phần sinh bỏ qua); ảnh chụp 1280 px và 390 px |
| 6.5 | Đóng đợt: ảnh chụp 10 trang mẫu trước và sau; `AGENTS.md`, `README.md`, `KE-HOACH.md`; push, CI, tag `v1.6` | — | cổng đạt |

**10 trang mẫu**: như đợt 4 (`ban-giao/dot-4.md`).

## Cổng

- Kiểm tra tương đương: văn bản hiển thị giống 100%. Ngoại lệ duy nhất là ngoặc kép, được khai báo bằng `--expect-sub`.
- Mọi URL còn mở được: sitemap giữ nguyên, mọi `id` tiêu đề giữ nguyên.
- Tiến độ người đọc giữ nguyên: khóa `localStorage` `logos` và mọi `data-id` không đổi.
- Không đơn vị nào bị mở khóa: `check_ledger --check` khớp, không commit `[doi-loi]` nào trong đợt.
- Bộ kiểm tra đầy đủ xanh (gồm `npm run test:real`); CI xanh sau khi push.

## Ngoài phạm vi

- Đổi màu hay font, đổi trình render, Pagefind (quyết định 38 chọn sửa worker).
- Sửa chữ trong bài.
- Công cụ Sơ đồ lập luận chưa thể hiện tiền đề liên kết hay độc lập (`viec-cho` 17/11): việc riêng, để đợt 7.
