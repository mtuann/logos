# Bàn giao đợt con 5.8: Câu hỏi lớn II

**Đã xong (2026-11-20): 299 khóa đóng băng, mẫu 30/30, 0% lỗi nghiêm trọng bị bỏ sót.** Phần dưới giữ lại để tra cứu cách đã làm; xem dòng 2026-11-20 cuối trong `ban-giao/nhat-ky-dot-5.md`.

Đọc trước theo thứ tự `AGENTS.md`, rồi tới mục 5.8 trong `ban-giao/dot-5.md` và dòng 2026-11-20 trong `ban-giao/nhat-ky-dot-5.md`.

Thư mục này giữ kế hoạch và công cụ dở dang của 5.8, để agent khác làm tiếp. Không xuất bản lên site.

## Trạng thái (2026-11-20, sau lô `r-6`)

| Bước | Trạng thái |
|---|---|
| Cổng nội dung (`thoi-gian` "Khối đang lớn" đủ ba nhãn; ba bài Việt Nam có nhãn độ chắc chắn) | xong, đã merge |
| Ghi sổ 299 khóa `cau-hoi/*` | xong (`chua-kiem`) |
| Kiểm lượt 1 (`agent-kiem-5.8-k01…k17`) | xong: 251 dat, 38 sua, 10 chua-kiem-duoc; 217 claim sai (63 vừa, 154 nhẹ); 12 claim chưa kiểm được |
| Bảng sửa (`agent-sua-5.8-s1…s9`) | xong cho cả 31 trang: `sua/<trang>.json` và `sua/<trang>.map.json` |
| Áp bảng sửa theo lô | **dở**: đã merge 6 lô `sua-s8-*` (`lots-s8.json`, xong hết) và 7 lô `sua-r-0…6` (`lots-rest.json`). **Còn lô 7–38 của `lots-rest.json`** |
| Làm tay: `thoi-gian`, `viet-hien-dai`, ba hình | chưa |
| Lượt 2, mẫu, đóng băng | chưa |

Kiểm lại số lô đã merge: `git log --oneline main | grep -c "sua-r-"` (đúng bằng chỉ số lô tiếp theo).

## Nội dung thư mục

- `huong-dan/`: hướng dẫn cho từng loại agent: kiểm lượt 1, kiểm lượt 2, soạn bảng sửa, kiểm mẫu.
- `con-sot.md`: những chỗ người soạn bảng sửa thấy còn sót (cùng loại lỗi nhưng chưa bị chấm). Hướng dẫn lượt 2 đã chép lại danh sách này, và lượt 2 phải xử lý hết.
- `sua/`:
  - `sai-5.8.json`: mọi claim sai sau lượt 1, gom theo trang.
  - `<trang>.json`: bảng `[path, old, new]` của trang; `<trang>.map.json`: claim ↔ dòng của bảng.
  - `lots-s8.json`, `lots-rest.json`: lô ≤ 3 đơn vị (luật cứng).
- `tools/`:
  - `run_lots.sh START END TAG`: mỗi lô tạo nhánh `dot-5-5-8-sua-TAG-N`, áp, ghi lại mã băm (`--ghi-so 5.8`), sinh lại `kb_*`, chạy bộ kiểm tra đầy đủ (`fin.sh` → `run_all.sh`), commit rồi merge `--no-ff` vào `main`. Bộ kiểm tra đỏ thì dừng.
  - `apply.py N`: áp lô N, đặt `fixed: true` cho claim tương ứng. File lô lấy từ biến môi trường `LOTS`.
  - `plan.py`: chia bảng thành lô.
  - `check_rep.py`: kiểm thử bảng (không ghi).
  - `prune_allow.py`: dọn `volatile-allow.yml` khi ngữ cảnh đổi.
  - `rep.py`: áp một bảng `[path, old, new]` tùy ý.
  - `mk.py`: dựng bảng từ spec.

## Làm tiếp

Chỉ một agent được chạy lô trong thư mục repo chính, vì `run_lots.sh` liên tục `git checkout`. Muốn làm song song thì dùng worktree riêng, và chỉ chạm vào trang không nằm trong lô còn lại.

### 1. Áp lô 7–38

```bash
rm -f "${TMPDIR:-/tmp}/logos-5.8-STOP"
LOTS=lots-rest.json zsh ban-giao/dot-5.8/tools/run_lots.sh 7 38 r
```

- **Dừng sạch giữa chừng:** `touch "${TMPDIR:-/tmp}/logos-5.8-STOP"`. Lô đang chạy vẫn merge xong; lô sau thoát ngay khi vừa tạo nhánh. Khi đó `git checkout main`, rồi `git branch -d` nhánh rỗng ấy.
- **Bộ kiểm tra đỏ:** đọc `${TMPDIR:-/tmp}/logos-5.8-last.out` và sửa trên chính nhánh đó.
  - Bản ghi nguồn mới thiếu `accessed`: thêm ngày mở vào `data/kb/sources.yml`.
  - Test đếm tác phẩm `tests/test_kb_works.py` đổi số: cập nhật số đếm và ghi lý do.
  - `lint_volatile`: thêm mục `data/style/volatile-allow.yml` có lý do, hoặc tách khối thời sự.

  Sửa xong thì chạy `zsh ban-giao/dot-5.8/tools/fin.sh "<message>"`, rồi chạy tiếp từ lô kế.

### 2. Làm tay (nhánh riêng, mỗi nhánh tối đa 3 đơn vị)

- **`thoi-gian`**:
  - Áp `sua/thoi-gian.json` bằng `uv run python ban-giao/dot-5.8/tools/rep.py ban-giao/dot-5.8/sua/thoi-gian.json`. Sau đó đặt `fixed: true` cho các claim có trong `sua/thoi-gian.map.json`.
  - Bảng thêm Nguồn mục 7: IEP "Time" của Bradley Dowden, <https://iep.utm.edu/time/>. Chạy `tools/kb_sources.py` để sinh bản ghi nguồn mới, thêm `accessed`, rồi viết bằng chứng `verification/evidence/sources__<khóa>.json` và dòng sổ `frozen`. Làm như `sources/sep.broad`: commit "5.8 cổng nội dung", bằng chứng `verification/evidence/sources__sep.broad.json`.
  - Trang IEP ghi "Author Information Bradley Dowden", và có câu "one second per second".
- **`viet-hien-dai`**:
  - Làm như trên với `sua/viet-hien-dai.json`. Bảng viết lại lập trường 2 (Trần Đình Hượu) theo bằng chứng.
  - Nguồn mới: Wynn Gadkar-Wilcox, "Existentialism and Intellectual Culture in South Vietnam", *The Journal of Asian Studies* 73(2), 2014, tr. 377–395, DOI 10.1017/S0021911813002349. Crossref xác nhận tên, số, trang.
  - Nếu `kb_sources` tách dòng Nguồn gộp thành nhiều bản ghi, mỗi bản ghi mới đều cần bằng chứng và dòng sổ.
- **Ba hình** trong `tools/figures.py`. Sửa xong chạy `uv run python tools/figures.py`; không sửa tay khối `fig` trong `docs/`.
  - `fig_khe_uoc` (`khe-uoc-xa-hoi`): "ai cũng chống ai" → "chưa có quyền lực chung". Đây là claim lượt 1 chưa áp.
  - `ho-khai-niem` (`nghe-thuat`): tiêu đề và caption "Tương tự họ" → "Tương đồng gia đình", thuật ngữ đã đóng băng `terms/tuong-dong-gia-dinh`.
  - `pascal-wager` (`duc-tin-ly-tri`, `luan-chung-ton-giao`): ô "Mất mát vô hạn / hình phạt đời đời" phải khớp câu đã sửa trong thân bài ("khốn khổ" (*misery*), mà nhiều người đọc là hình phạt đời đời), theo SEP *Pascal's Wager*.

  Sau khi sửa, ghi `fixed: true` cho claim tương ứng: `khe-uoc-xa-hoi.md#cau-hoi-that-su-la-gi` claim 2, cùng các claim thuật ngữ "tương tự gia đình" ở `nghe-thuat`.

### 3. Lượt 2

Sinh danh sách đơn vị cho lượt 2:

- `changed.json`: khóa 5.8 có mã băm hiện tại khác `hash` trong bằng chứng.
- `open.json`: khóa còn claim `chua-kiem-duoc`.

Đặt hai file vào thư mục này. Rồi giao agent theo `huong-dan/HUONG-DAN-KIEM-5.8-LUOT2.md`, mỗi agent 2–4 trang, mã `agent-kiem-5.8-rNN`.

Lượt 2 sẽ sinh claim sai mới, từ chỗ còn sót và từ claim chưa kiểm được không tìm ra nguồn. Soạn bảng sửa cho các claim đó (theo `huong-dan/HUONG-DAN-BANG-SUA.md`), áp theo lô như bước 1, rồi kiểm lại đến khi không còn claim mở. Đây là cách đã làm ở 5.7: lô `sua-C-*`.

### 4. Ghi đạt, mẫu, đóng băng

```bash
uv run python tools/verify.py --ghi-dot 5.8      # bằng chứng đạt → da-kiem
uv run python tools/verify.py --tien-do 5.8      # phải 299/299 da-kiem
uv run python tools/verify.py --mau 5.8          # chọn mẫu 10%
```

- **Mẫu:** giao agent kiểm thứ hai theo `huong-dan/HUONG-DAN-MAU-5.8.md` (ghi vào `verification/mau/5.8/`). Agent mẫu không được xem bằng chứng gốc.
- **Đếm lỗi bỏ sót:** `--so-mau 5.8` đếm lỗi nghiêm trọng bị bỏ sót, phải ≤ 2%. Lỗi mẫu tìm ra thì sửa (ở 5.7 là lô `sua-mau-*`), cập nhật cả bằng chứng gốc và bằng chứng mẫu.
- **Đóng băng:** `uv run python tools/verify.py --dong-bang 5.8 --chu-bien-duyet YYYY-MM-DD`. Các đợt trước ghi "(Claude duyệt tạm)" trong nhật ký; chủ biên duyệt lại sau.
- **Ghi lại:** cập nhật `ban-giao/nhat-ky-dot-5.md` (một dòng cho các lô sửa, một dòng cho lượt 2 và mẫu, một dòng cho đóng băng). Ghi `ban-giao/viec-cho.md` cho các việc dưới đây.

## Việc ngoài 5.8 đã phát hiện (ghi vào `viec-cho.md`)

- **Câu "câu bổ sung chỉ hỏi những người chọn trả lời thêm"** còn ở các trang đã đóng băng: `chan-ly`, `tu-do-y-chi`, `trach-nhiem`. Cách viết đúng như ở `sieu-dao-duc`: mỗi câu bổ sung được hỏi một phần sáu số người tham gia, chọn ngẫu nhiên, cộng với những người tự chọn. Sửa cần `[doi-loi]`.
- **Số trang bài McTaggart 1908:** Wikisource ghi 456–473, kho đã đóng băng ghi 457–474. Cần đối chiếu.
- **`lint_lien_ket` còn 1 chỗ** (`cong-cu/suy-dien`, Socrates): để cho 5.9.
