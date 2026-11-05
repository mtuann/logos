# Đợt 3 — Tách thời sự và số đếm

- **Thời gian dự kiến**: 7/12–13/12/2026 (đợt 2 đóng sớm ngày 5/11/2026, nên có thể bắt đầu ngay). **Điều kiện bắt đầu**: đợt 2 đã đóng (tag `v1.2`, CI xanh).
- **Mục tiêu**: dời đoạn có hạn dùng ra khối thời sự `data/thoi-su/*.md`, thay số đếm và số liệu PhilPapers gõ tay bằng shortcode đọc từ dữ liệu. **Loại thay đổi: cơ học.** Câu chữ hiển thị giữ nguyên, chỉ dời chỗ; mọi việc chạm trang phải qua kiểm tra tương đương 100%.
- **Nhánh**: mỗi việc một nhánh `dot-3-<ten-ngan>`, merge vào `main` trên máy khi xong; push khi xong cả đợt (AGENTS.md luật 6).
- **Tiến độ**: `ban-giao/nhat-ky-dot-3.md`.

## Việc

| # | Việc | Loại | Kết quả kiểm được |
|---|---|---|---|
| 3.1 | Khung khối thời sự: định dạng `data/thoi-su/<id>.md` và `schema/thoi-su.schema.json` (đặc tả dưới); shortcode `[[thoi-su:<id>]]` trong `hooks/kb.py` chèn nguyên văn thân khối; `tools/thoi_su_check.py --check` (mỗi khối được đúng trang `page` dùng đúng một lần, mọi shortcode có khối, khối nhiều dòng thì shortcode đứng riêng một dòng); `tools/book.py` mở shortcode thời sự trước khi viết lại link; `content.yml` đăng ký `data/thoi-su/` (`kind: thoi-su`, `tier: mo-rong`) | công cụ | kiểm thử: chèn đúng chữ, giữ thụt lề trong danh sách và admonition, khối thiếu hoặc thừa thì build và `--check` đỏ |
| 3.2 | `lint_volatile`: sửa luật bắt nhầm về ngôn ngữ ("tính đến" nghĩa "xét đến", "hai nghìn năm nay", "Luật De Morgan", trích dẫn tác giả–năm có ngoặc "Hicks, Humphries và Slater (2024)", văn bản cổ trong khối `!!! quote`); danh sách miễn `data/style/volatile-allow.yml` (quyết định 20), mỗi mục có đơn vị, chữ tìm thấy, đoạn ngữ cảnh nguyên văn, loại lý do; báo cáo liệt kê riêng các chỗ được miễn | công cụ | mỗi luật sửa có kiểm thử; mục miễn hết hiệu lực khi ngữ cảnh đổi chữ (kiểm thử) |
| 3.3 | Dời 7 đoạn có hạn dùng ở 7 trang ra `data/thoi-su/` bằng script `tools/migrate/dot3_thoi_su.py` (bảng ánh xạ: trang, đoạn nguyên văn, id, nguồn); mọi chỗ còn lại vào danh sách miễn với lý do. `lint_volatile --strict` vào CI | cơ học | parity 100%; `lint_volatile --strict` = 0 trong Lõi; `thoi_su_check --check` xanh |
| 3.4 | Số đếm: shortcode `[[count:…]]` thêm loại dữ liệu (`nguy-bien` → `fallacies.json`, `thuat-ngu` → `terms.json`, `quiz` → `quiz-bank.json`); script thay số đếm nội dung site gõ tay ở các trang hệ thống và trang chủ (`index.md`, `bat-dau/lo-trinh.md`, `cau-hoi/index.md`, `doc/index.md`, `lich-su/index.md`, `cong-cu/index.md`, `luyen-tap/index.md`) | cơ học | parity 100%; mỗi chỗ thay có số in ra bằng đúng số cũ |
| 3.5 | Số liệu PhilPapers: shortcode `[[pp:…]]` đọc `data/kb/philpapers-2020.json` (đặc tả dưới); script `tools/migrate/dot3_philpapers.py` thay **chỉ** ô số khớp JSON từng chữ, trong các bảng PhilPapers của Lõi (44 bảng ở 42 trang), cùng `n ≈ …` của từng câu và số tổng của khảo sát trong văn xuôi (1.785 triết gia, 100 câu hỏi, 40 câu chính, 60 câu bổ sung). Ô không khớp, câu chưa ghép được thì giữ nguyên, ghi `verification/lech/philpapers-bang.md`. Ba hình `philpapers-*` của `tools/figures.py` đọc số từ JSON | cơ học | parity 100%; hình sinh lại giống từng byte; danh sách lệch liệt kê mọi ô số còn gõ tay trong bảng PhilPapers |
| 3.6 | Đóng đợt: `AGENTS.md` mục 4, `README.md`, `KE-HOACH.md` (Trạng thái, danh sách lệnh), parity cả đợt `v1.2` → `main`, `changed_units` cả đợt | — | cổng đạt |

Thứ tự đề xuất: 3.1 → 3.2 → 3.3 → 3.4 → 3.5 → 3.6. Mọi việc chạm trang (3.3–3.5) đổi mã băm của đơn vị chứa chỗ thay (chữ được thay bằng shortcode); sổ kiểm chứng còn rỗng nên không đơn vị nào bị mở khóa.

## Đặc tả

### Khối thời sự

```markdown
---
page: cau-hoi/tu-do-y-chi.md          # trang dùng khối (đường dẫn trong docs/); một khối, một trang
updated_to: 2026-10-22                # nội dung đúng tới ngày này (đợt 3: lấy `updated` của trang)
review_by: 2027-10-22                 # hạn rà soát; đợt 3: updated_to + 1 năm
sources:                              # link trong thân khối (đợt 5 bổ sung nguồn còn thiếu)
  - https://…
---
**Pháp luật hình sự.** Pháp luật Việt Nam, …
```

- Id: `<trang không đuôi .md, "/" thành ".">.<tên ngắn>`, ví dụ `cau-hoi.tu-do-y-chi.bo-luat-hinh-su`.
- Thân khối là đúng phần Markdown đã cắt khỏi trang, không thêm, không bớt (không có dòng trống cuối). Khối một dòng có thể đứng giữa câu (chèn tại chỗ); khối nhiều dòng thì shortcode đứng riêng một dòng, và các dòng sau dòng đầu được thêm đúng thụt lề của dòng chứa shortcode.
- Link trong thân khối viết tương đối với trang `page` (như trước khi cắt), nên chỉ trang đó được dùng khối.
- Đợt 3 không có giao diện riêng cho khối thời sự (hộp, ngày cập nhật): đó là việc của đợt 4. Văn bản hiển thị phải giống hệt trước khi dời.

### Tiêu chí dời (quyết định 20)

Dời khi điều đoạn nói **đúng hay sai tùy lúc đọc** và phải rà lại định kỳ: văn bản pháp luật đang hiệu lực, số liệu đang thay đổi (số người được minh oan, nguồn tạng, số du học sinh), mô tả tình trạng hiện tại của AI không gắn mốc ngày. Không dời, mà ghi vào danh sách miễn với một trong các lý do:

| Lý do | Nghĩa | Ví dụ |
|---|---|---|
| `co-moc-thoi-gian` | câu đã gắn mốc ngày, nên đúng mãi | "Năm 2023, một nhóm 19 nhà nghiên cứu… công bố" |
| `vi-du-gia-dinh` | năm hoặc "năm nay" trong ví dụ, thí nghiệm tư duy, bài tập | "cấm xe xăng từ năm 2030", "Năm 2045, … Máy Tiên Tri" |
| `trang-thai-hoc-thuat` | "đến nay/hiện nay" nói về một tranh luận hay giới nghiên cứu, đổi theo thập kỷ chứ không theo năm | "Đến nay các nhà triết học vẫn chưa thống nhất" |
| `chung-chung` | "hiện nay" nghĩa chung, không nêu dữ kiện kiểm được | "với hệ thống tư pháp như hiện nay" |
| `su-kien-lich-su` | văn bản pháp lý lịch sử có năm | "Nghị định thư Montreal (1987)" |

`data/style/volatile-allow.yml`: danh sách `{unit, found, context, reason}`; `context` là một đoạn nguyên văn (≥ 20 ký tự) của dòng chứa chỗ bị bắt. Mục miễn chỉ có hiệu lực khi đơn vị còn chứa đúng `context` đó: sửa chữ ở đợt 5 thì linter bắt lại. Mục miễn không khớp chỗ nào thì `lint_volatile --strict` cũng đỏ (để danh sách không mục dần).

### Shortcode số liệu PhilPapers

| Cú pháp | In ra | Ví dụ |
|---|---|---|
| `[[pp:<câu>.<lựa chọn>]]` | `pct`, một chữ số thập phân, dấu phẩy (ô `raw` thì in chữ gốc) | `[[pp:tu-do-y-chi.tuong-thich-luan]]` → 59,2 |
| `[[pp:<câu>.<lựa chọn>/bac-bo]]`, `/loai-tru` | `pct_reject`, `pct_exclusive` | |
| `[[pp:<câu>/n]]` | `n` kiểu Việt Nam | `[[pp:tu-do-y-chi/n]]` → 1.760 |
| `[[pp:khao-sat/<trường>]]` | số tổng của khảo sát: `nguoi-tra-loi` (1.785), `so-cau` (100), `cau-chinh` (40), `cau-bo-sung` (60) | |

Số tổng thêm vào `philpapers-2020.json` ở `source.survey`, chép từ chính phần mở đầu của file (đã có các số này); `tools/philpapers-2020.md` vẫn sinh lại giống từng byte. Khóa sai thì build dừng.

Ô chỉ được thay khi chữ trong ô **bằng đúng** chữ shortcode in ra ("9" ≠ "9,0"): đợt 3 không đổi cách ghi số.

## Lưu ý kỹ thuật

- Parity trước và sau mỗi việc chạm trang: `uv run python tools/parity.py --base main`. Không có phép thay nào được chờ đợi (`--expect-sub` không dùng ở đợt này).
- `lz.normalize` giữ shortcode nguyên dạng, nên đơn vị đã thay số bằng shortcode không đổi mã băm khi số trong dữ liệu đổi; ngược lại, việc dời đoạn làm mã băm đơn vị đổi một lần (ghi trong nhật ký).
- Các tool rút dữ kiện (`kb_works`, `kb_quotes`, `kb_events`, `kb_sources`) và linter đọc nguồn Markdown của trang: chạy lại sau 3.3 và xem bản ghi nào mất `used_in`; khối thời sự là Mở rộng, nên dữ kiện trong đó không còn tính là của Lõi.
- `them/cap-nhat.md` là nhật ký thay đổi: số trong đó là số của từng thời điểm, **không** thay bằng shortcode. Số theo phiên luyện tập ("10 đoạn", "5 thuật ngữ") cũng không phải số đếm nội dung.
- `docs/them/sach.md` sinh từ các trang: chạy lại `tools/book.py` sau mỗi việc chạm trang.

## Cổng

- [ ] `lint_volatile --strict` = 0 trong Lõi, chạy chặn trong CI; mọi mục miễn có lý do.
- [ ] Đoạn có hạn dùng nằm trong `data/thoi-su/`, qua schema và `thoi_su_check --check`.
- [ ] Số đếm nội dung site trong trang hệ thống và trang chủ là shortcode.
- [ ] Ô số PhilPapers khớp JSON là shortcode; ô còn lại có trong danh sách lệch.
- [ ] Tương đương 100% cả đợt (`tools/parity.py --base v1.2`).
- [ ] `AGENTS.md` mục 4 cập nhật nếu có lệnh mới.
- [ ] CI xanh.

## Không làm

Viết lại câu cho hết phụ thuộc thời gian, sửa số liệu lệch, đổi "9" thành "9,0" (đợt 5); giao diện hộp thời sự, ngày cập nhật hiện trên trang (đợt 4); thêm nguồn cho khối thời sự (đợt 5); thay số trong `them/cap-nhat.md`.

## Đầu vào từ đợt trước

`hooks/kb.py` (shortcode `count`), `tools/lint_volatile.py` và báo cáo nền `verification/lint/lint_volatile.md` (90 chỗ ở 50 trang), `data/kb/philpapers-2020.json` (87 câu), `verification/bao-cao-nen.md` mục 2–4 (139 dấu thời gian, 98 số đếm gõ tay, 39 bài có bảng PhilPapers: số đếm thô ngày 23/10, đợt 3 lọc lại), `tools/parity.py`, `tools/changed_units.py`.
