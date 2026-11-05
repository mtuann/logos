# Nhật ký Đợt 2 — Kho dữ kiện

Mỗi dòng một việc đã xong hoặc đang dở. Phiên sau đọc từ đây và làm tiếp.

| Ngày | Việc | File | Trạng thái | Còn gì |
|---|---|---|---|---|
| 2026-11-05 | Luật git mới (chủ biên): merge vào `main` trên máy sau mỗi việc, push khi xong đợt, không PR | `AGENTS.md`, `KE-HOACH.md`, `ban-giao/README.md`, `ban-giao/mau-dot.md` | xong, merge vào `main` | — |
| 2026-11-05 | Brief đợt 2 theo `ban-giao/mau-dot.md`; thêm quyết định 13–19 (chờ, có Đề xuất) | `ban-giao/dot-2.md`, `KE-HOACH.md` | xong | chủ biên duyệt brief, chọn quyết định 13–14 trước việc 2.1 và 2.4 |
| 2026-11-05 | Quyết định 13, 14 theo Đề xuất (chủ biên chọn) | `KE-HOACH.md` | xong | — |
| 2026-11-05 | 2.1 Thêm `jsonschema==4.26.0` (uv.lock, requirements.txt; bản xuất của uv 0.11.32 trong CI giống hệt); 7 schema `schema/kb/` (thêm `person-profile` cho `data/people/<id>.yml`); `tools/kb_check.py --check` (schema, khóa trùng YAML, tham chiếu chéo, `used_in`) vào CI | `pyproject.toml`, `uv.lock`, `requirements.txt`, `schema/kb/*.json`, `tools/kb_check.py`, `tests/test_kb_check.py`, CI, `AGENTS.md`, `README.md` | xong: 8 kiểm thử | việc tiếp: 2.2 |
| 2026-11-05 | 2.1 merge vào `main` | — | xong | — |
| 2026-11-05 | 2.2 `data/kb/people.yml` (59, giữ thứ tự của philosophers.json) + 59 hồ sơ `data/people/<id>.yml` bằng `tools/migrate/dot2_people.py` (đọc nguồn từ git, tự kiểm đọc ngược); `philosophers.py` đọc YAML (bỏ 3.190 dòng CONTENT), sinh cả `philosophers.json`; `content.yml`: `philosophers.json` thành file sinh, thêm mục thư mục `data/people/`; schema hồ sơ cho phép `url` rỗng (14 nguồn là sách in) | `data/kb/people.yml`, `data/people/*.yml`, `tools/philosophers.py`, `tools/migrate/dot2_people.py`, `tools/content_registry.py`, `content.yml`, `tools/lint_structure.py`, `schema/kb/person-profile.schema.json`, tests, `README.md`, `AGENTS.md` | xong: 60 trang triết gia, philosophers.json, dòng thời gian, sơ đồ ảnh hưởng giống từng byte; `kb_check`: people 59, hồ sơ 59 | việc tiếp: 2.3 |
