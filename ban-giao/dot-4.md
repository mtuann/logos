# Đợt 4 — Giao diện tối thiểu

- **Thời gian dự kiến**: 14/12–20/12/2026, phần còn lại sang tuần 4/1/2027 (đợt 3 đóng sớm ngày 5/11/2026, nên có thể bắt đầu ngay). **Điều kiện bắt đầu**: đợt 3 đã đóng (tag `v1.3`, CI xanh).
- **Mục tiêu**: thêm phần giao diện sinh từ dữ liệu (dải thông tin, hộp thời sự, nhãn Mới, thẻ di chuột, trang tác phẩm, trang Tình trạng kiểm chứng, nav sinh từ `content.yml`), sửa các điểm đo ngày 3/11/2026 (khả năng tiếp cận, điện thoại, font, tìm kiếm), dựng lại trang chủ. **Loại thay đổi: giao diện.** Chữ trong bài không đổi; chỉ thêm phần sinh (override, CSS, JS, trang sinh), bằng Material 9.8.0 như cũ (không đổi theme).
- **Nhánh**: mỗi việc một nhánh `dot-4-<ten-ngan>`, merge vào `main` trên máy khi xong; push khi xong cả đợt (AGENTS.md luật 6).
- **Tiến độ**: `ban-giao/nhat-ky-dot-4.md`.

## Việc

| # | Việc | Loại | Kết quả kiểm được |
|---|---|---|---|
| 4.1 | Kiểm thử trên trình duyệt thật: thêm `playwright` và `@axe-core/playwright` (ghim trong `package.json`/`package-lock.json`); `tests/real/*.test.js` (`npm run test:real`) mở `site/` qua máy chủ tĩnh, quét axe **cả trang** (gồm tương phản) cho 10 trang mẫu ở hai cỡ màn hình (1280 px, 390 px); chụp ảnh 10 trang mẫu vào `site-anh/` (không commit; CI tải lên làm artifact). Báo cáo nền `verification/giao-dien/axe-nen.md` | công cụ | báo cáo nền liệt kê đúng các lỗi đã đo ngày 3/11 (`ban-giao/viec-cho.md`); CI chạy được Chromium |
| 4.2 | Parity cho giao diện: `tools/parity.py` bỏ qua phần tử có thuộc tính `data-oz-sinh` (phần giao diện sinh thêm); `--ngoai-le TRANG` cho trang được phép đổi chữ (trang chủ, việc 4.9), in khác biệt nhưng không tính lệch | công cụ | kiểm thử: phần tử `data-oz-sinh` không làm lệch; trang ngoại lệ được báo riêng |
| 4.3 | Khả năng tiếp cận: link trong bài có gạch chân (hoặc tương phản ≥ 3:1 với chữ thường); chữ xám nhỏ ≥ 4,5:1; vùng chạm ≥ 24 px (menu trái, điện thoại); `aria-label` cho `.md-progress`; axe trên trình duyệt thật 0 lỗi ở 10 trang mẫu, hai chế độ sáng/tối | giao diện | `npm run test:real` 0 vi phạm axe; `tests/unit/contrast.test.js` có cặp màu mới |
| 4.4 | Font tự host (quyết định 21): Be Vietnam Pro (400, 600, 700) và Noto Serif (400, 700, nghiêng 400), woff2, tập Latin + tiếng Việt, `font-display: swap`, kèm file giấy phép OFL; preload font thân bài; service worker cache font | giao diện | trình duyệt thật dùng đúng font (kiểm thử `document.fonts`); tổng dung lượng font ghi trong nhật ký |
| 4.5 | Tìm kiếm (quyết định 22): `hooks/search_vi.py` thôi thêm bản sao không dấu; bỏ dấu (gồm đ → d) ở trình duyệt, khi dựng chỉ mục và khi gõ, bằng worker tìm kiếm của site thay cho worker của Material (cùng giao thức tin nhắn của Material 9.8.0, bản cuối nên không đổi); chỉ tải chỉ mục khi mở ô tìm; trang Dòng thời gian không còn đoạn trích dính chữ | giao diện | `search_index.json` giảm ≥ 45%; `tests/browser/search.test.js` cho cùng kết quả (chạy với bỏ dấu phía trình duyệt); kiểm thử trên trình duyệt thật: gõ "dao duc" ra "Đạo đức…" |
| 4.6 | Dải thông tin đầu trang và hộp thời sự: dải dưới tiêu đề (tầng, khối, ngày cập nhật, trạng thái kiểm chứng theo sổ: "chưa kiểm" / "đã kiểm N/M mục"); khối thời sự hiện trong hộp có "Thông tin đúng tới …, rà lại trước …" (khối nhiều dòng) hoặc dấu nhỏ có chú thích (khối một dòng, giữa câu). Phần chữ thêm mang `data-oz-sinh` | giao diện | parity 100% (bỏ `data-oz-sinh`); kiểm thử JS/hook cho dải và hộp |
| 4.7 | Nhãn Mới và thẻ di chuột: nhãn "Mới" cho trang `mo-rong` có `added` trong 60 ngày (cơ chế; hiện chưa có trang nào); thẻ di chuột (và chạm giữ trên điện thoại) cho link tới trang triết gia (tên, năm, một dòng tóm tắt từ `philosophers.json`) và thuật ngữ (`terms.json`), truy cập được bằng bàn phím | giao diện | kiểm thử jsdom + trình duyệt thật; axe 0 lỗi |
| 4.8 | Trang sinh mới (quyết định 23): `docs/tac-pham/index.md` (tác phẩm đã biết tác giả, theo tác giả, kèm bài nhắc tới, ghi "chưa kiểm chứng") bằng `tools/works_page.py`; `docs/them/kiem-chung.md` (Tình trạng kiểm chứng: số đơn vị theo tầng, khối, trạng thái sổ) bằng `tools/verification_page.py`; cả hai có `--check`, đăng ký `content.yml` (`he-thong`, `generated: true`), vào nav | giao diện | `--check` trong CI; trang có trong sitemap; parity các trang cũ 100% |
| 4.9 | Nav sinh từ `content.yml` và trang chủ mới (quyết định 24): `content.yml` thêm mục `nav` (cây nhóm và đường dẫn, tiêu đề nav khi khác tiêu đề trang); `tools/nav_gen.py` ghi phần `nav:` của `mkdocs.yml` (`--check` trong CI). Trang chủ: nút chính "Bắt đầu ở đây" → `bat-dau/`, xếp 6 cửa vào thành chính/phụ, dùng lại chữ đang có | cơ học (nav) + giao diện (trang chủ) | nav sinh ra giống hệt nav hiện tại (so cấu trúc); parity 100% trừ `index.md` (ngoại lệ, khác biệt ghi nhật ký) |
| 4.10 | Điện thoại và in: khối "Tóm tắt 5 phút" gọn trên màn hẹp (thu gọn được, mặc định mở trên máy tính); nút "In bài này" không chiếm màn hình đầu; cột chữ khoảng 65–75 ký tự; `description` chạy được shortcode (hook mở shortcode trong `page.meta.description`), rồi thay "57 câu hỏi…", "19 hướng dẫn…" ở `cau-hoi/index.md`, `doc/index.md` | giao diện + cơ học | ảnh chụp 390 px; parity 100% (gồm `description`) |
| 4.11 | Đóng đợt: ảnh chụp 10 trang mẫu (máy tính và điện thoại, sáng và tối) đăng thành một trang để chủ biên duyệt; `AGENTS.md`, `README.md`, `KE-HOACH.md` | — | cổng đạt |

Thứ tự đề xuất: 4.1 → 4.2 → 4.3 → 4.4 → 4.5 → 4.6 → 4.7 → 4.8 → 4.9 → 4.10 → 4.11. Việc 4.1–4.2 là công cụ đo, làm trước để mọi việc sau có số đo trước/sau.

**10 trang mẫu**: `index.md`, `bat-dau/index.md`, `cau-hoi/tri-thuc.md` (bài dài, bảng PhilPapers, hình), `cau-hoi/tu-do-y-chi.md` (khối thời sự, quiz), `cong-cu/lap-luan.md`, `lich-su/dong-thoi-gian.md`, `doc/platon-bien-ho.md`, `triet-gia/kant.md`, `them/tu-dien.md`, `luyen-tap/nguy-bien.md`.

## Đặc tả

### Phần sinh và parity

Mọi chữ do giao diện thêm vào trong `<article>` (dải thông tin, nhãn hộp thời sự, nhãn Mới) nằm trong phần tử có `data-oz-sinh`; `parity.py` bỏ các phần tử đó ở cả hai bên. Thẻ di chuột được dựng bằng JS lúc chạy, không có trong HTML. Chữ của bài, kể cả thân khối thời sự, không được nằm trong `data-oz-sinh`.

### Dải thông tin

`<div class="oz-info" data-oz-sinh>`: tầng (Lõi / Mở rộng), khối (tên đọc được, từ `content.yml`), "Cập nhật lần cuối" (chuyển từ cuối trang lên, cuối trang giữ nguyên), trạng thái kiểm chứng từ `verification/ledger.json` (đợt 4: mọi đơn vị "chưa kiểm"). Không hiện ở trang `he-thong`. Dữ liệu được hook đọc lúc build (không gọi mạng).

### Hộp thời sự

Hook `kb.py` bọc thân khối nhiều dòng trong `<div class="oz-thoi-su" markdown>` có tiêu đề `data-oz-sinh` ("Thông tin có hạn dùng · đúng tới 22/10/2026 · rà lại trước 22/10/2027"); khối một dòng trong `<span class="oz-thoi-su-dong">` kèm dấu `data-oz-sinh` có `title`/`aria-label` cùng nội dung. Khối quá hạn: thêm lớp `oz-thoi-su--qua-han` (CI đã chặn deploy khi quá hạn, nên chỉ thấy ở bản build trên máy).

### Nav trong `content.yml`

```yaml
nav:
  - Trang chủ: index.md
  - Bắt đầu:
      - bat-dau/index.md
      - Ba con đường đọc: bat-dau/lo-trinh.md   # tiêu đề nav khi khác title của trang
```

Giữ đúng cú pháp nav của MkDocs để chép thẳng. `nav_gen.py` ghi vào `mkdocs.yml` giữa `# gen:nav` và `# /gen:nav`; `content_registry --check` kiểm mọi trang trong nav có trong `pages` và ngược lại (trừ trang ẩn khai báo rõ).

## Lưu ý kỹ thuật

- Playwright cần trình duyệt: trên máy `npx playwright install chromium`; trong CI `npx playwright install --with-deps chromium` (có cache). `npm test` giữ nguyên (jsdom, 122 + 250); `npm run test:real` là bộ mới, chạy riêng một bước trong CI.
- Material 9.8.0 là bản cuối: override bằng `overrides/` (block, partial), không vá file trong gói.
- Worker tìm kiếm (4.5): nếu không giữ được giao thức của Material mà không vá gói, dừng ở mức "bỏ bản sao + tải chậm" là không được (mất tìm không dấu), nên khi đó giữ bản sao, chỉ làm tải chậm, và báo chủ biên.
- Font: lấy file từ kho chính thức của Google Fonts (GitHub `google/fonts`, giấy phép OFL), cắt tập ký tự bằng `fonttools` chạy một lần (không thêm vào phụ thuộc của dự án); ghi nguồn và mã băm file vào `docs/assets/fonts/NGUON.md`.
- Mỗi việc chạm giao diện: chạy `npm run test:real` và parity trước khi merge.

## Cổng

- [ ] 250 kiểm thử trình duyệt (jsdom) và 122 kiểm thử đơn vị xanh; axe trên trình duyệt thật 0 vi phạm ở 10 trang mẫu, hai cỡ màn hình, sáng và tối (CI).
- [ ] Parity 100% cả đợt (`tools/parity.py --base v1.3`, bỏ `data-oz-sinh`), trừ `index.md` (ngoại lệ có ghi khác biệt).
- [ ] `search_index.json` giảm ≥ 45% mà tìm không dấu vẫn đúng (kiểm thử).
- [ ] Trang tác phẩm và trang Tình trạng kiểm chứng sinh từ dữ liệu, có `--check`; nav sinh từ `content.yml`.
- [ ] Chủ biên duyệt ảnh chụp 10 trang mẫu.
- [ ] `AGENTS.md` mục 4 có lệnh mới.
- [ ] CI xanh.

## Không làm

Đổi chữ trong bài, kể cả bài có điểm đo xấu (đợt 5); chọn kiểu ngoặc kép (việc chờ ngày 3/11: là đổi chữ, để đợt 5 quyết trước khi đóng băng); đổi theme hay trình render (đợt 6); trang riêng cho từng tác phẩm (sau đợt 5, quyết định 23); Pagefind (đợt 6).

## Đầu vào từ đợt trước

`ban-giao/viec-cho.md` (điểm đo ngày 3/11/2026: axe, điện thoại, font, tìm kiếm), `data/thoi-su/` và shortcode `[[thoi-su:…]]` (đợt 3), `data/kb/works.yml`, `verification/ledger.json`, `content.yml`, `tools/parity.py`, `tests/browser/` (250 kiểm thử jsdom), `tests/unit/contrast.test.js`.
