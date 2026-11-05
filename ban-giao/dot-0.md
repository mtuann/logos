# Đợt 0 — Chốt mốc

- **Thời gian**: 3/11–8/11/2026 (dự kiến ban đầu 26/10–1/11/2026).
- **Mục tiêu**: lập repo `logos` từ bản nhập nguyên trạng của logos-zero, chốt điểm xuất phát và lập sổ đăng ký nội dung, để mọi đợt sau làm việc trên cùng một danh sách. **Không đổi chữ nào trong nội dung.**
- **Nhánh**: `dot-0-chot-moc`. Mỗi commit một loại thay đổi; chủ biên duyệt theo từng commit (hoặc tách PR theo commit).
- **Tiến độ**: `ban-giao/nhat-ky-dot-0.md`.

## Việc

| # | Việc | Ai | Kết quả kiểm được |
|---|---|---|---|
| 0.1 | Nhập nguyên trạng `logos-zero@ecb2bb8` vào `main` (cùng mã tree `9e3893c7`), gắn tag `v1.0-moc` | agent | tag có trên GitHub sau khi chủ biên push |
| 0.2 | Chọn quyết định ở `KE-HOACH.md` mục 3 (12 dòng; dòng 9 đã chốt) | chủ biên | không còn dòng "chờ", hoặc ghi rõ "theo Đề xuất" |
| 0.3 | Commit bộ bàn giao (`AGENTS.md`, `CLAUDE.md`, `KE-HOACH.md`, `ban-giao/`) | agent | có trong nhánh |
| 0.4 | `content.yml` + `schema/content.schema.json` (đặc tả dưới) | agent | sổ phủ mọi trang và file dữ liệu |
| 0.5 | `tools/content_registry.py`: `--init` (sinh lần đầu từ `nav`) và `--check`; thêm vào CI và `AGENTS.md` mục 4 | agent | CI đỏ khi trang và sổ lệch nhau |
| 0.6 | `tools/baseline_report.py` sinh `verification/bao-cao-nen.md` (đặc tả dưới) | agent | số liệu nền để đo đợt 1–3 |
| 0.7 | Tạo nhãn GitHub: chạy `tools/github_labels.sh` | chủ biên | nhãn có trên repo |
| 0.8 | Chuyển sang ProperDocs 1.6.7 + Material 9.8.0, ghim bằng `uv.lock`; CI cài bằng uv | agent | HTML giống bản nhập, trừ file CSS/JS của theme |
| 0.9 | Cấu hình site song song (quyết định 9): `site_url`, khóa `localStorage` `logos`, cache service worker `logos-v1`, `noindex` (quyết định 12) | agent | `search_index.json` giống hệt bản nhập |
| 0.10 | Sửa kiểm thử phụ thuộc ngày chạy (`tests/browser/ke-hoach.test.js`) | agent | 250/250 kiểm thử trình duyệt xanh |

## Đặc tả `content.yml`

```yaml
version: 1
pages:      # đường dẫn tính từ docs/, theo thứ tự nav
  - {path: cau-hoi/tri-thuc.md, type: cau-hoi, tier: loi, block: tri-thuc, generated: false}
data:       # đường dẫn tính từ gốc repo
  - {path: docs/assets/data/terms.json, kind: thuat-ngu, tier: loi, block: thuat-ngu, generated: false}
```

- Giá trị cho phép nằm một chỗ: `schema/content.schema.json` (JSON Schema). Tool đọc danh sách từ đó; kiểm thử đòi danh sách `block` khớp `KE-HOACH.md` mục 5.3.
- `type`: `cau-hoi` | `cong-cu` | `lich-su` | `doc` | `bat-dau` | `triet-gia` | `he-thong`. Trang chủ, mọi `index.md`, `them/`, `luyen-tap/` là `he-thong`.
- `tier`: `loi` | `mo-rong` | `he-thong`. Trang `he-thong` có `tier: he-thong`, `block: null`.
- `block` của bài `cau-hoi` lấy theo nhóm trong `nav` (11 chủ đề); các loại khác theo thư mục (`cong-cu`, `lich-su`, `van-ban`, `bat-dau`, `triet-gia`). Dữ liệu cũng có `block` (`thuat-ngu`, `triet-gia`, `luyen-tap`) hoặc `null`.
- `kind` của dữ liệu: `thuat-ngu` | `triet-gia` | `ho-so-triet-gia` | `luyen-tap` | `quiz` | `philpapers`.
- `generated: true` cho trang và file sinh tự động: `triet-gia/*.md` (cả `index.md`), `them/sach.md`, `them/tu-dien.md`, `lich-su/dong-thoi-gian.md`, `lich-su/so-do-anh-huong.md`, `docs/assets/data/quiz-bank.json`. Trang chỉ có một khối sinh (như `them/cap-nhat.md`) vẫn là `false`.
- Sinh lần đầu bằng `uv run python tools/content_registry.py --init`, rồi chủ biên duyệt. Không gõ tay danh sách. `--init` không ghi đè `content.yml` đã có (thêm `--force` nếu thật sự muốn sinh lại).
- Quyết định 1 và 6 ở `KE-HOACH.md` mục 3 quyết định `tier` của 11 bài luân lý ứng dụng và thời sự, và của 3 bài Tư tưởng Việt Nam. Còn "chờ" thì dùng Đề xuất (cả hai nhóm là `loi`).
- Chưa thêm `tier`/`block` vào front matter ở đợt này; đợt 1 làm cùng lúc với ID mục. Front matter nào đã có hai trường này thì phải khớp `content.yml`.

`content_registry.py --check` báo lỗi khi: một file `.md` trong `docs/` không có trong `pages`; một mục trong `pages` không còn file; một file trong `docs/assets/data/` không có trong `data`; đường dẫn trùng; thiếu trường hoặc thừa trường; giá trị ngoài danh sách cho phép; `type` không khớp thư mục; `generated` không khớp danh sách trang sinh; trang `he-thong` có `block` khác `null`; front matter lệch sổ.

## Đặc tả báo cáo nền

`verification/bao-cao-nen.md`, sinh bằng `uv run python tools/baseline_report.py`, chạy lại cho cùng kết quả (không ghi ngày giờ). Không chạy lại ở các đợt sau: đây là số nền để so. Gồm:

1. Theo khu vực: số trang, số mục H2, dung lượng chữ (bỏ SVG).
2. Dấu thời gian theo trang, đếm sau khi bỏ front matter và mục Nguồn: năm 2022–2026; "hiện nay", "gần đây", "tính đến", "đến nay", "mới nhất", "năm nay"; "Luật …", "Nghị định", "Bộ luật".
3. Số đếm gõ tay trong văn xuôi ("57 bài", "19 hướng dẫn", "100 đoạn hội thoại"…).
4. Dữ kiện gõ tay: số chỗ dạng "*Tác phẩm* (năm)", số khối `!!! quote`, số mục trong các danh sách Nguồn, số bài có bảng PhilPapers.
5. Trang thiếu mục bắt buộc theo loại (KE-HOACH.md mục 5.1).

Phạm vi đếm: trang viết tay (`generated: false` trong `content.yml`). Hồ sơ triết gia (văn nằm trong `tools/philosophers.py`) đếm riêng trên trang sinh `triet-gia/*.md`.

Số đo ngày 23/10/2026 để đối chiếu: 139 dấu thời gian ở 66 trang; 394 chỗ "*Tác phẩm* (năm)"; 157 khối trích dẫn; 628 mục Nguồn; 35 bài có bảng PhilPapers; 888 mục H2. Cách đếm có thể làm số hơi khác; lệch trên 10% thì giải thích trong báo cáo.

## Nhãn GitHub

`tools/github_labels.sh` tạo (hoặc cập nhật) các nhãn: `cho` (việc chờ), `doi-loi` (PR được sửa đơn vị Lõi đã đóng băng), `bao-loi` (báo lỗi của người đọc, mẫu issue dùng nhãn này), `link-hong` (issue do kiểm tra link hằng tuần tự mở), `dot-0` … `dot-7`. Cần `gh` đã đăng nhập và repo `mtuann/logos` đã có trên GitHub.

## Cổng

- [x] Repo GitHub `mtuann/logos` có `main`, nhánh `dot-0-chot-moc`, tag `v1.0-moc`.
- [x] Bảng Quyết định đã điền (11 dòng theo Đề xuất, 4/11/2026).
- [x] `content.yml` phủ 100% trang; `content_registry.py --check` chạy trong CI.
- [x] Chủ biên đã duyệt `content.yml`, nhất là hai cột `tier` và `block` (chấp nhận như sinh từ nav, 4/11/2026).
- [x] `verification/bao-cao-nen.md` đã commit.
- [x] CI xanh trên PR. Sau khi merge: bật GitHub Pages (Settings → Pages → Source: GitHub Actions) để site lên ở <https://mtuann.github.io/logos/>. (CI xanh trên PR #1 và trên `main` sau merge 4/11/2026; Pages chạy, trang chủ trả 200 ngày 5/11/2026.)

## Không làm trong đợt này

Sửa chữ trong bài; thêm ID mục; tạo kho dữ kiện; đổi giao diện; thêm bài; sửa repo logos-zero.
