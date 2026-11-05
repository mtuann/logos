# Nhật ký Đợt 5 — Kiểm chứng và đóng băng Lõi

Mỗi dòng một việc đã xong hoặc đang dở. Phiên sau đọc từ đây và làm tiếp.

| Ngày | Việc | File | Trạng thái | Còn gì |
|---|---|---|---|---|
| 2026-11-05 | Brief đợt 5 theo `ban-giao/mau-dot.md`; quyết định 25 (push khi xong cả đợt 5), 26 (mã băm bỏ qua kiểu ngoặc), 27 (đổi hết "Logos Zero" thành "Logos") | `ban-giao/dot-5.md`, `KE-HOACH.md` | xong | việc tiếp: 5.0a |
| 2026-11-05 | 5.0a Mã băm bỏ qua kiểu ngoặc (quyết định 26): `tools/lz/hashing.py` gộp `“ ”` → `"`, `‘ ’` → `'` khi băm đơn vị và bản ghi (cả chuỗi lồng trong bản ghi); `normalize()` giữ nguyên ngoặc; KE-HOACH.md 5.6 bước 4. Tiêu đề admonition ngoặc cong không phải cú pháp nên vẫn đổi mã băm | `tools/lz/hashing.py`, `tests/test_lz.py`, `KE-HOACH.md` | xong; sổ rỗng nên không đơn vị nào mở khóa | việc tiếp: 5.0b |
| 2026-11-05 | 5.0a merge vào `main` | — | xong | — |
| 2026-11-05 | 5.0b Sổ ghi được dữ liệu JSON: `check_ledger.py` thêm `JSON_RECORDS` (`terms`, `fallacy-types`, `fallacies`, `lap-luan`, `logic`, `thi-nghiem`; theo `id` trong `docs/assets/data/*.json`); `--status` và trang Tình trạng kiểm chứng đếm cả các loại này (sinh lại `docs/them/kiem-chung.md`); `changed_units` báo bản ghi JSON đổi | `tools/check_ledger.py`, `tools/changed_units.py`, `tools/verification_page.py`, `schema/ledger.schema.json`, `docs/them/kiem-chung.md`, tests | xong | việc tiếp: 5.0c |
