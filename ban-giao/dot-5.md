# Đợt 5 — Kiểm chứng và đóng băng Lõi

- **Thời gian dự kiến**: 4/1–14/3/2027 (đợt 4 đóng sớm ngày 5/11/2026, nên có thể bắt đầu ngay). **Điều kiện bắt đầu**: đợt 4 đã đóng (tag `v1.4`, CI xanh).
- **Mục tiêu**: kiểm từng đơn vị Lõi và từng bản ghi kho theo `ban-giao/kiem-chung.md`, sửa đúng chỗ sai (mỗi chỗ có bằng chứng), kiểm mẫu 10%, rồi đóng băng. **Loại thay đổi: nội dung.** Đây là đợt duy nhất được sửa chữ trong bài (AGENTS.md mục 6).
- **Nhánh**: mỗi việc một nhánh `dot-5-<ten-ngan>`, merge vào `main` trên máy khi xong. **Push `main` một lần khi xong cả đợt 5** (luật 6; quyết định 25). Từng đợt con không push và không gắn tag.
- **Tiến độ**: `ban-giao/nhat-ky-dot-5.md`; tình trạng sổ: `uv run python tools/check_ledger.py --status`.

## Quy mô (đo ngày 5/11/2026)

| Phạm vi | Số lượng |
|---|---:|
| Đơn vị Lõi trong trang (mục H2 và `#_dau`) | 987: Câu hỏi lớn 552, Văn bản gốc 190, Công cụ 171, Lịch sử 68, Bắt đầu 6 |
| Bản ghi kho `data/kb/` | people 59, works 337, quotes 155, events 128, sources 681, philpapers 87 câu |
| Hồ sơ triết gia `data/people/` | 59 |
| Dữ liệu luyện tập và từ điển `docs/assets/data/` | terms 249, fallacy-types 20, fallacies 100, lap-luan 30, logic 20, thi-nghiem 8 |

## Việc

| # | Việc | Loại | Kết quả kiểm được |
|---|---|---|---|
| 5.0a | Mã băm bỏ qua kiểu ngoặc (quyết định 26): `tools/lz/normalize.py` coi `“ ”` như `"` và `‘ ’` như `'` ở bước 4 của chuẩn hóa (KE-HOACH.md 5.6) | công cụ | kiểm thử: đổi kiểu ngoặc thì mã băm không đổi, đổi chữ trong ngoặc thì đổi; sổ còn rỗng nên không đơn vị nào bị mở khóa |
| 5.0b | Sổ ghi được dữ liệu JSON: `check_ledger.py` thêm loại `terms/<id>`, `fallacy-types/<id>` (20 loại ngụy biện), `fallacies/<id>` (100 đoạn luyện), `lap-luan/<id>`, `logic/<id>`, `thi-nghiem/<id>` (đọc `docs/assets/data/*.json`); `--status` đếm cả các loại này | công cụ | kiểm thử: khóa sai báo lỗi; mã băm đổi khi bản ghi đổi |
| 5.0c | Công cụ đợt con `tools/verify.py` (đặc tả dưới) và `schema/evidence.schema.json`; `check_ledger --check` kiểm mọi file bằng chứng theo schema | công cụ | kiểm thử cho từng lệnh; bằng chứng sai schema thì CI đỏ |
| 5.0d | Đổi tên "Logos Zero" thành "Logos" (quyết định 27) bằng `tools/migrate/dot5_ten.py`: tên site, manifest, chân trang, nhãn "(bản dịch của Logos Zero)" và mọi chỗ trong bài, dữ liệu (`data/kb/quotes.yml`, `data/people/*.yml`), tool và kiểm thử đọc nhãn đó, `AGENTS.md` luật 2, `HUONG-DAN-VIET.md`. **Giữ** chỗ nói tới site song song `logos-zero` (trang Dữ liệu của tôi, nhập bản sao lưu, `KE-HOACH.md`, nhật ký) | cơ học | parity: mọi khác biệt chỉ là "Logos Zero" → "Logos" (script in bảng chỗ đổi và chỗ giữ, chủ biên xem); làm **trước** khi ghi sổ chỗ nào |
| 5.1 | Kho: người và tác phẩm | nội dung | mọi bản ghi `people/*` và `works/*` đóng băng; `verification/lech/works.md` hết mục mở (117 tác phẩm chưa rõ tác giả được gán hoặc ghi lý do; 3 tác phẩm nhiều năm được chốt) |
| 5.2 | Kho: trích dẫn, sự kiện, nguồn, PhilPapers | nội dung | `quotes/*`, `events/*`, `sources/*`, `philpapers/*` đóng băng; `lint_quotes` = 0 trong Lõi; `verification/lech/{quotes,events,sources,sep,philpapers,philpapers-bang}.md` hết mục mở |
| 5.3 | Hồ sơ triết gia và thuật ngữ | nội dung | `ho-so/*` (59), `terms/*` (249) đóng băng; quyết định 18 vào `HUONG-DAN-VIET.md`; `lint_terms` = 0 trong Lõi |
| 5.4 | Văn bản gốc: 19 hướng dẫn | nội dung | 190 đơn vị `doc/*` đóng băng; `doc/sartre-hien-sinh.md` có mục "Đọc từng đoạn" (quyết định 19) |
| 5.5 | Công cụ tư duy và dữ liệu luyện tập | nội dung | 171 đơn vị `cong-cu/*`, `fallacy-types/*`, `fallacies/*`, `lap-luan/*`, `logic/*`, `thi-nghiem/*` đóng băng; `cong-cu/luan-cu-thep.md` có "Bài tập", "Tự kiểm tra" (quyết định 19) |
| 5.6 | Lịch sử và Bắt đầu | nội dung | 74 đơn vị `lich-su/*`, `bat-dau/lo-trinh.md` đóng băng |
| 5.7 | Câu hỏi lớn I: Tri thức, Tâm trí, Tự do, Đạo đức, Luân lý ứng dụng | nội dung | 253 đơn vị đóng băng |
| 5.8 | Câu hỏi lớn II: Chính trị, Mỹ học, Tôn giáo, Siêu hình, Ý nghĩa, Việt Nam | nội dung | 299 đơn vị đóng băng; ba bài Tư tưởng Việt Nam có nhãn độ chắc chắn (quyết định 6) |
| 5.9 | Đóng đợt: `lint_structure`, `lint_terms`, `lint_facts`, `lint_quotes` chuyển sang chặn trong CI (0 trong Lõi); `AGENTS.md`, `README.md`, `KE-HOACH.md`; push, CI, tag `v1.5` | — | cổng đạt |

Thứ tự: 5.0a → 5.0b → 5.0c → 5.0d → 5.1 → … → 5.8 → 5.9. Kho trước (5.1–5.3) để các bài sau chỉ còn kiểm phần diễn giải: dữ kiện trong bài khớp bản ghi đã đóng băng thì ghi `dung` kèm khóa bản ghi, không phải mở lại nguồn.

## Đặc tả

### Quy trình một đợt con

1. **Phạm vi**: `uv run python tools/verify.py --pham-vi 5.N` in danh sách đơn vị và bản ghi; `--ghi-so 5.N` ghi chúng vào sổ ở trạng thái `chua-kiem` kèm mã băm hiện tại.
2. **Kiểm**: agent kiểm là một phiên riêng (subagent), chỉ nhận `ban-giao/kiem-chung.md`, khóa đơn vị và văn bản của đơn vị; không nhận ý kiến của agent làm. Agent kiểm mở nguồn, ghi `verification/evidence/<khóa>.json`. Mỗi lượt giao tối đa một trang (hoặc 20 bản ghi kho) để bằng chứng không bị dồn ẩu.
3. **Sửa**: agent làm đọc các claim `sai`, sửa đúng câu đó trong bài hoặc bản ghi, mỗi nhánh tối đa 3 đơn vị nội dung (AGENTS.md mục 5). Commit ghi khóa đơn vị và file bằng chứng. Sửa bản ghi kho thì chạy lại generator dùng nó. Không sửa ngoài claim; thấy lỗi khác thì ghi vào bằng chứng của đơn vị đó để agent kiểm xét.
4. **Kiểm lại**: đơn vị đã sửa có mã băm mới; agent kiểm xét lại riêng các claim đã sửa, cập nhật bằng chứng (`hash` mới, `result: dat`).
5. **Ghi sổ**: `verify.py --ghi <khóa>…` kiểm bằng chứng (schema, `unit`, `hash` trùng mã băm hiện tại, `result: dat`), rồi đặt `da-kiem` với `verified_on`, `checker`, `evidence`.
6. **Kiểm mẫu**: `verify.py --mau 5.N` chọn 10% (làm tròn lên, ít nhất 3) đơn vị `da-kiem` của đợt con, theo hạt giống cố định là tên đợt con, nên ai chạy cũng ra cùng mẫu; ghi `verification/mau/5.N.md`. Agent kiểm thứ hai (phiên khác, không thấy bằng chứng cũ) kiểm lại mẫu vào `verification/mau/5.N/<khóa>.json`; `verify.py --so-mau 5.N` so hai bộ và tính tỉ lệ lỗi nghiêm trọng mà bộ đầu bỏ sót. Trên 2% thì kiểm lại cả đợt con. Chủ biên đọc trang mẫu (quyết định 5).
7. **Đóng băng**: `verify.py --dong-bang 5.N` chuyển `da-kiem` → `frozen` khi mẫu đạt và chủ biên đã duyệt (cờ `--chu-bien-duyet YYYY-MM-DD`, ghi vào `verification/mau/5.N.md`).

Nhánh chỉ thêm bằng chứng và sổ (không đổi chữ bài) có thể gom cả một trang hoặc một loại bản ghi; nhánh đổi chữ thì tối đa 3 đơn vị.

### `tools/verify.py`

| Lệnh | Việc |
|---|---|
| `--pham-vi 5.N` | in khóa đơn vị và bản ghi của đợt con (theo bảng Việc; khối của `content.yml`) |
| `--ghi-so 5.N` | thêm khóa chưa có vào sổ, trạng thái `chua-kiem` |
| `--ghi KHOA…` | bằng chứng hợp lệ và `result: dat` → `da-kiem` |
| `--mau 5.N` | chọn mẫu 10% cố định, ghi `verification/mau/5.N.md` |
| `--so-mau 5.N` | so bằng chứng mẫu với bằng chứng gốc, in tỉ lệ lỗi nghiêm trọng bị bỏ sót |
| `--dong-bang 5.N --chu-bien-duyet NGÀY` | `da-kiem` → `frozen` cho đợt con đã đạt mẫu |
| `--tien-do 5.N` | đếm theo trạng thái, liệt kê đơn vị `sua` chưa xong |

### File bằng chứng

Theo `ban-giao/kiem-chung.md`, kiểm bằng `schema/evidence.schema.json`. Thêm cho bản ghi kho: claim có thể dẫn khóa bản ghi đã đóng băng (`"kb": "works/kant.critique-of-pure-reason"`) thay cho `sources`. Mỗi `sources[].quote` là chữ thật trên trang đã mở trong phiên đó; agent kiểm không dùng trí nhớ.

## Lưu ý kỹ thuật

- Mọi lần đổi chữ phải dùng đúng bảng thuật ngữ và văn phong của `HUONG-DAN-VIET.md`; đọc nó trước mỗi phiên sửa.
- Đổi một bản ghi kho làm đổi mọi trang sinh từ nó (`philosophers.py`, `gen_glossary.py`, `works_page.py`…): chạy lại generator và để parity trong commit đó chỉ ra các trang bị ảnh hưởng.
- Sổ chặn ngay khi một đơn vị đã đóng băng bị đổi (quyết định 4). Sửa lại một đơn vị `frozen` trong đợt 5 cũng phải có `[doi-loi]` trong message và bằng chứng mới (luật 8).
- Quiz nằm trong trang nên được kiểm cùng đơn vị chứa nó; `data-id` không đổi.
- Số liệu PhilPapers chỉ lấy từ `data/kb/philpapers-2020.json`. JSON hiện có 87/100 câu; 13 câu còn thiếu chỉ thêm khi mở được trang kết quả chính thức (5.2), không thì ghi lý do.
- Mạng: agent kiểm mở nguồn bằng trình duyệt hoặc web fetch. Nguồn không mở được thì `chua-kiem-duoc`, không suy ra từ trí nhớ.

## Cổng

- [ ] 100% đơn vị Lõi (987) và mọi bản ghi trong phạm vi đóng băng (`check_ledger --status`).
- [ ] Mỗi đợt con: lỗi nghiêm trọng bị bỏ sót trong mẫu ≤ 2%; chủ biên đã duyệt mẫu (`verification/mau/5.N.md`).
- [ ] Mọi danh sách lệch ở `verification/lech/` hết mục mở; `lint_structure`, `lint_terms`, `lint_facts`, `lint_quotes` = 0 trong Lõi và chặn trong CI.
- [ ] Không còn "Logos Zero" trong bài và giao diện, trừ chỗ nói tới site song song (quyết định 27).
- [ ] `AGENTS.md` mục 4 có lệnh mới (`verify.py`).
- [ ] CI xanh.

## Không làm

Thêm bài, triết gia, hướng dẫn đọc mới (đợt 7; luật 7). Thiết kế lại giao diện, chọn kiểu ngoặc hiển thị (đợt 6). Viết lại một mục vì văn phong khi không có claim sai hay lỗi `vua` (người kiểm ghi `nhe`, gom lại cho sau). Sửa logos-zero.

## Đầu vào từ đợt trước

`verification/lech/*.md` (đợt 2–3), `verification/lint/*.md` (báo cáo nền của linter), `ban-giao/viec-cho.md` (các dòng loại "lỗi nghi ngờ" và "quyết định" dành cho đợt 5), `data/kb/*`, `data/people/*`, `data/thoi-su/*` (đợt 5 bổ sung nguồn còn thiếu), quyết định 15–19 (còn "chờ": dùng Đề xuất).
