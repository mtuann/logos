# Nhật ký Đợt 0 — Chốt mốc

Mỗi dòng một việc đã xong hoặc đang dở. Phiên sau đọc từ đây và làm tiếp.

| Ngày | Việc | File | Trạng thái | Còn gì |
|---|---|---|---|---|
| 2026-11-03 | 0.1 Nhập nguyên trạng `logos-zero@ecb2bb8` vào `main` (commit `ee3a2f9`), tag `v1.0-moc` | toàn repo | xong: mã tree `9e3893c7` trùng commit nguồn, 290 file | chủ biên push `main` và tag |
| 2026-11-03 | 0.10 Kiểm thử Kế hoạch học hết phụ thuộc ngày chạy | `tests/browser/ke-hoach.test.js` | xong: trước 249/250, sau 250/250 | — |
| 2026-11-03 | 0.8 ProperDocs 1.6.7 + Material 9.8.0, uv | `pyproject.toml`, `uv.lock`, `.python-version`, `requirements.txt`, `.github/workflows/*`, `README.md` | xong: 181/181 trang HTML giống bản nhập (bỏ dòng generator và mã băm tên file CSS/JS), `search_index.json` giống hệt | — |
| 2026-11-03 | 0.9 Cấu hình site song song | `mkdocs.yml`, `overrides/main.html`, `docs/robots.txt`, `docs/sw.js`, `docs/assets/js/{progress,mydata,merge}.js`, `package*.json`, `tests/**` | xong: `search_index.json` giống hệt; HTML chỉ khác URL gốc, dòng generator, thẻ robots | — |
| 2026-11-03 | 0.3 Bộ bàn giao cho repo logos | `AGENTS.md`, `CLAUDE.md`, `KE-HOACH.md`, `ban-giao/*` | xong: thêm quyết định 9–12, viết lại mục 11 và 12, việc chờ đo ngày 3/11 | chủ biên chọn quyết định (0.2) |
| 2026-11-03 | 0.4–0.5 Sổ đăng ký nội dung | `content.yml`, `schema/content.schema.json`, `tools/content_registry.py`, `tests/test_content_registry.py`, `.github/workflows/deploy.yml`, `AGENTS.md`, `README.md` | xong: sinh từ nav, 180 trang (loi 161, he-thong 19) + 9 file dữ liệu; `--check` xanh, trong CI; 8 kiểm thử | chủ biên duyệt cột `tier`, `block` |
| 2026-11-03 | 0.6 Báo cáo nền | `tools/baseline_report.py`, `verification/bao-cao-nen.md` | xong: chạy lại giống hệt; so với số 23/10: 6/7 chỉ số lệch dưới 10% ở phạm vi khớp, PhilPapers +11,4% có giải thích trong báo cáo | — |
| 2026-11-03 | 0.7 Script tạo nhãn GitHub | `tools/github_labels.sh` | xong phần agent | chủ biên chạy sau khi tạo repo GitHub |
| 2026-11-04 | 0.1 Đẩy `main`, nhánh `dot-0-chot-moc` và tag `v1.0-moc` lên GitHub | — | xong (chủ biên) | — |
| 2026-11-04 | 0.7 Tạo 12 nhãn bằng `tools/github_labels.sh` | — | xong (chủ biên) | — |
| 2026-11-04 | Mở PR #1 `dot-0-chot-moc` → `main` | — | xong | chờ CI xanh, merge, bật Pages |
| 2026-11-04 | 0.2 Chốt 11 quyết định theo Đề xuất; duyệt `content.yml` | `KE-HOACH.md`, `ban-giao/dot-0.md` | xong (chủ biên chọn) | — |
| 2026-11-04 | Merge PR #1 vào `main`; CI xanh trên `main`; bật GitHub Pages | — | xong (chủ biên) | — |
| 2026-11-05 | Đóng đợt 0: kiểm cổng (Pages trả 200), cập nhật bảng Trạng thái | `KE-HOACH.md`, `ban-giao/dot-0.md` | xong | — |
