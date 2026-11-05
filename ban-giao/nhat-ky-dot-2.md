# Nhật ký Đợt 2 — Kho dữ kiện

Mỗi dòng một việc đã xong hoặc đang dở. Phiên sau đọc từ đây và làm tiếp.

| Ngày | Việc | File | Trạng thái | Còn gì |
|---|---|---|---|---|
| 2026-11-05 | Luật git mới (chủ biên): merge vào `main` trên máy sau mỗi việc, push khi xong đợt, không PR | `AGENTS.md`, `KE-HOACH.md`, `ban-giao/README.md`, `ban-giao/mau-dot.md` | xong, merge vào `main` | — |
| 2026-11-05 | Brief đợt 2 theo `ban-giao/mau-dot.md`; thêm quyết định 13–19 (chờ, có Đề xuất) | `ban-giao/dot-2.md`, `KE-HOACH.md` | xong | chủ biên duyệt brief, chọn quyết định 13–14 trước việc 2.1 và 2.4 |
| 2026-11-05 | Quyết định 13, 14 theo Đề xuất (chủ biên chọn) | `KE-HOACH.md` | xong | — |
| 2026-11-05 | 2.1 Thêm `jsonschema==4.26.0` (uv.lock, requirements.txt; bản xuất của uv 0.11.32 trong CI giống hệt); 7 schema `schema/kb/` (thêm `person-profile` cho `data/people/<id>.yml`); `tools/kb_check.py --check` (schema, khóa trùng YAML, tham chiếu chéo, `used_in`) vào CI | `pyproject.toml`, `uv.lock`, `requirements.txt`, `schema/kb/*.json`, `tools/kb_check.py`, `tests/test_kb_check.py`, CI, `AGENTS.md`, `README.md` | xong: 8 kiểm thử | việc tiếp: 2.2 |
