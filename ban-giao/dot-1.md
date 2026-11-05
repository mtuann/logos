# Đợt 1 — Công cụ nền

- **Thời gian dự kiến**: 9/11–22/11/2026 (lùi một tuần theo đợt 0). **Điều kiện bắt đầu**: đợt 0 đã đóng.
- **Mục tiêu**: dựng máy móc cho kiểm chứng (đơn vị, chuẩn hóa, băm, sổ, linter, báo cáo PR) và gắn ID cố định cho mọi mục H2. **Không đổi chữ hiển thị nào.**
- **Nhánh**: `dot-1-cong-cu`, mỗi việc một PR.

## Việc

| # | Việc | Kết quả kiểm được |
|---|---|---|
| 1.1 | `tools/lz/`: `registry.py` (đọc `content.yml`), `units.py` (tách đơn vị theo H2; khóa `path#id`; phần trước H2 đầu tiên là `#_dau`), `normalize.py` và `hashing.py` theo `KE-HOACH.md` mục 5.6. Kiểm thử `tests/test_lz.py` chứng minh từng hệ quả ở mục 5.6 | thư viện có kiểm thử |
| 1.2 | `tools/parity.py`: build hai bản (trước và sau), trích văn bản hiển thị của từng trang (bỏ thanh điều hướng, chân trang, script), so từng trang | "giống 100%" hoặc danh sách trang lệch |
| 1.3 | `tools/add_heading_ids.py`: thêm `{#id}` cho mọi H2 chưa có ID. ID lấy đúng anchor đang có trong HTML đã build, theo thứ tự, kể cả hậu tố `_1`, `_2` của tiêu đề trùng | 888 mục có ID; link nội bộ không đổi; parity 100% |
| 1.4 | Thêm `tier` và `block` vào front matter từ `content.yml` bằng script; mở rộng `content_registry.py --check` để so khớp hai bên | front matter khớp sổ; parity 100% |
| 1.5 | `verification/ledger.json` rỗng, `schema/ledger.schema.json`, `tools/check_ledger.py`: `--check` báo lỗi khi đơn vị `frozen` lệch mã băm, trừ khi biến môi trường `LZ_ALLOW_CORE_CHANGE=1` (CI đặt khi PR có nhãn `doi-loi`); `--status` in tiến độ theo khối | CI có bước sổ kiểm chứng |
| 1.6 | `tools/changed_units.py` (so base…head, liệt kê đơn vị đổi, tầng, checklist cần làm) và bước GitHub Actions đăng kết quả thành bình luận PR; `.github/pull_request_template.md` | mỗi PR có báo cáo đơn vị |
| 1.7 | `data/style/terms-policy.yml` (sinh từ bảng ở `HUONG-DAN-VIET.md` mục 3, có danh sách ngoại lệ: trích nguyên văn, từ điển, tên riêng); `tools/lint_terms.py`, `tools/lint_volatile.py`, `tools/lint_structure.py` chạy chế độ cảnh báo, ghi báo cáo vào `verification/lint/` | báo cáo nền của ba linter |
| 1.8 | `hooks/kb.py`: khung shortcode. Chốt cú pháp ở PR này (gợi ý `[[count:cau-hoi]]`); làm trước loại `count` (đọc `content.yml`); khóa không tồn tại thì build dừng; kiểm thử trong `tests/test_hooks.py` | sẵn sàng cho đợt 3 |

## Lưu ý kỹ thuật

- So tương đương: `uv run properdocs build --strict -f mkdocs.yml -d <thư-mục-tạm>/truoc` trên commit gốc và `-d <thư-mục-tạm>/sau` trên nhánh, rồi chạy `tools/parity.py` trên hai thư mục.
- Anchor hiện tại do `hooks/slugs.py` và phần mở rộng `toc` sinh ra. Đừng tự tính lại slug: đọc ID từ HTML đã build, để khớp cả cách `toc` đánh số tiêu đề trùng.
- Chuẩn hóa bỏ `updated` và các khối gen/fig, để chạy lại generator không mở khóa đơn vị.
- Ưu tiên thư viện chuẩn. Cần thư viện mới thì ghim phiên bản trong `requirements.txt` và nêu trong báo cáo.
- Mỗi tool có `--help`, chạy được từ thư mục gốc repo, thoát mã 1 khi lỗi (giống các tool hiện có).

## Cổng

- [x] `tools/parity.py` báo giống 100% sau việc 1.3 và 1.4. (Từng việc so với `main`; cả đợt `73378c0` → `main`: 181 trang + `search_index.json` giống 100%; `changed_units.py`: không đơn vị nào đổi mã băm.)
- [x] `tests/test_lz.py` chứng minh các hệ quả ở `KE-HOACH.md` mục 5.6.
- [x] CI có thêm: `content_registry`, `check_ledger`, ba linter (cảnh báo), `changed_units`. (Thêm cả `add_heading_ids --check`, `terms_policy --check`.)
- [x] `verification/lint/` có báo cáo nền của ba linter.
- [x] `AGENTS.md` mục 4 và `README.md` có lệnh mới.
- [x] CI xanh (5/11/2026: trên máy 110 unittest, 122 + 250 kiểm thử JS; GitHub Actions run 41988926748 trên `main`: build và deploy xanh).

## Không làm

Sửa chữ trong bài; sửa lỗi mà linter tìm ra (chỉ ghi lại); tạo kho dữ kiện; đổi giao diện.

## Đầu vào từ đợt 0

`content.yml`, `tools/content_registry.py`, `verification/bao-cao-nen.md`, bảng Quyết định đã điền.
