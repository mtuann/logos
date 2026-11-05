# AGENTS.md — Hướng dẫn cho agent và người mới

Đọc file này trước mọi việc trong repo. Nó áp dụng cho mọi agent (Claude Code, Codex, Cursor…) và cho người mới tham gia.
Không xuất bản lên site.

## 1. Dự án trong năm dòng

- **Logos** (repo `mtuann/logos`): làm lại Logos Zero, website triết học tiếng Việt cho người bắt đầu từ con số 0 — <https://mtuann.github.io/logos/>. Logos Zero (<https://mtuann.github.io/logos-zero/>, repo `mtuann/logos-zero`) chạy song song, độc lập; từ repo này không sửa logos-zero.
- Site tĩnh ProperDocs 1.6.7 (bản kế tục MkDocs 1.x) + Material for MkDocs 9.8.0, phiên bản ghim trong `uv.lock`. Push lên `main` là GitHub Actions build và deploy ngay.
- Nội dung hiện có: 57 bài Câu hỏi lớn, 15 bài Công cụ tư duy, 8 bài Lịch sử, 19 hướng dẫn Đọc văn bản, 59 trang triết gia (sinh tự động), 249 thuật ngữ, ngân hàng luyện tập (428 câu quiz, 100 đoạn ngụy biện…).
- Đang làm lại site theo kế hoạch **Lõi đã kiểm chứng + Mở rộng**, chia thành 8 đợt có cổng: xem `KE-HOACH.md`. Mốc xuất phát: tag `v1.0-moc` = commit nhập nguyên trạng từ `logos-zero@ecb2bb8` (cùng mã tree).
- **Chủ biên** (mtuann) chọn quyết định và duyệt. Agent được merge vào `main` trên máy sau mỗi việc, và được push `main` khi xong cả một đợt (luật 6; chủ biên cho quyền ngày 5/11/2026).

## 2. Đọc theo thứ tự

1. `KE-HOACH.md` — kế hoạch, bảng quyết định, các đợt, cổng; mục "Đợt đang mở".
2. `ban-giao/dot-N.md` — việc của đợt bạn được giao (N = số đợt).
3. `ban-giao/nhat-ky-dot-N.md` — tiến độ các phiên trước của đợt đó (nếu có). Làm tiếp từ đây, đừng làm lại.
4. `HUONG-DAN-VIET.md` — văn phong, bảng thuật ngữ bắt buộc, cú pháp Markdown. **Bắt buộc đọc trước khi sửa bất kỳ chữ nào trong nội dung.**
5. `README.md` — cấu trúc repo, lệnh, cách thêm nội dung, cách thêm công cụ.
6. `tools/philpapers-2020.md` — nguồn số liệu khảo sát duy nhất được dùng (sinh từ `data/kb/philpapers-2020.json`; sửa số ở JSON).

## 3. Luật cứng

Vi phạm một luật dưới đây thì dừng lại và hỏi chủ biên, không tự xoay xở.

1. **Không bịa.** Mọi năm, tên người, tên tác phẩm, trích dẫn, số liệu phải có nguồn bạn đã thực sự mở được (SEP — ưu tiên link bản lưu theo quý dạng `plato.stanford.edu/archives/fall2026/entries/<mục>/`, IEP, Project Gutenberg, Wikisource, ctext.org, bài báo gốc qua DOI). Không chắc thì không viết; ghi vào "Câu hỏi mở" trong báo cáo.
2. **Không tự chế câu nói.** Trích nguyên văn chỉ từ văn bản đã mở. Văn bản còn bản quyền: tối đa 1–2 câu. Bản dịch của site ghi "(bản dịch của Logos)".
3. **Một nhánh (một việc), một loại thay đổi, đúng đợt đang mở.** Không "tiện tay" sửa chỗ khác. Thấy lỗi ngoài phạm vi: ghi vào `ban-giao/viec-cho.md`.
4. **Không sửa tay file sinh tự động**: `docs/triet-gia/*.md`, `docs/assets/data/philosophers.json` (sinh từ `data/kb/people.yml`), `docs/them/sach.md`, `docs/them/tu-dien.md`, `docs/tac-pham/index.md`, `docs/them/kiem-chung.md`, `docs/assets/data/quiz-bank.json`, phần giữa `<!-- gen:… -->`…`<!-- /gen:… -->` và `<!-- fig:… -->`…`<!-- /fig:… -->`. Sửa nguồn rồi chạy tool tương ứng trong `tools/`.
5. **Không phá người đọc.** Không đổi URL trang (đường dẫn giữ như logos-zero), khóa `localStorage` `logos`, `data-id` của quiz, `id` của thuật ngữ và của bản ghi luyện tập.
6. **Git an toàn.** Mỗi việc làm trên nhánh `dot-N-<ten-ngan>`; xong việc và bộ kiểm tra đầy đủ xanh thì `git merge --no-ff` vào `main` **trên máy**. Không mở PR. **Chỉ push `main` khi xong cả một đợt** (mọi việc đã merge, cổng đạt trừ mục CI, bộ kiểm tra xanh), vì push là deploy ngay; sau khi push, chờ CI xanh rồi gắn tag đóng đợt. Không force-push, không xóa file, không viết lại lịch sử.
7. **Không thêm nội dung mới** (bài, triết gia, hướng dẫn đọc) trước đợt 7, trừ khi chủ biên mở rõ trong `KE-HOACH.md`.
8. **Đơn vị Lõi đã đóng băng** (có trạng thái `frozen` trong `verification/ledger.json`) chỉ được sửa trong PR mang nhãn `doi-loi` (hoặc commit có `[doi-loi]` trong message khi merge thẳng), kèm bằng chứng mới. Xem tiến độ: `uv run python tools/check_ledger.py --status`.

## 4. Lệnh

Cần [uv](https://docs.astral.sh/uv/) (tự cài Python 3.13 theo `.python-version` và đúng phiên bản trong `uv.lock`) và Node 24.15+.

```bash
uv sync --frozen
npm ci

# Bộ kiểm tra đầy đủ, giống CI. Chạy trước mọi báo cáo.
for t in gen_glossary figures review_check timeline influence philosophers book frontmatter_check quiz_bank terms_policy kb_sources kb_works kb_quotes kb_philpapers kb_events works_page verification_page nav_gen; do
  uv run python tools/$t.py --check || break
done
uv run python tools/content_registry.py --check
uv run python tools/add_heading_ids.py --check
uv run python tools/check_ledger.py --check
uv run python tools/kb_check.py --check
uv run python tools/thoi_su_check.py --check
uv run python tools/lint_volatile.py --strict -q   # chặn: nội dung có hạn dùng phải ở data/thoi-su/ hoặc trong danh sách miễn
for l in lint_terms lint_structure lint_facts lint_quotes; do uv run python tools/$l.py -q; done   # cảnh báo, chưa chặn
uv run properdocs build --strict -f mkdocs.yml
uv run python -m unittest discover -s tests
npm test        # cần thư mục site/ đã build
npm run test:real   # axe trên Chromium thật (lần đầu: npx playwright install chromium); AXE_REPORT=1 để chỉ đo
```

Không có uv: tạo virtualenv Python 3.11+, `pip install -r requirements.txt` (sinh từ `uv.lock`), rồi chạy các lệnh trên không kèm `uv run`. Không sửa tay `uv.lock`, `requirements.txt`; nâng phiên bản là việc phải hỏi (mục 6).

Xem đơn vị nào đổi chữ so với `main` (gồm tầng, trạng thái sổ, việc cần làm): `uv run python tools/changed_units.py --base main`.

Kiểm chứng một đợt con của đợt 5 (quy trình: `ban-giao/dot-5.md` mục Đặc tả; bằng chứng: `ban-giao/kiem-chung.md`):

```bash
uv run python tools/verify.py --pham-vi 5.1     # khóa của đợt con
uv run python tools/verify.py --ghi-so 5.1      # ghi vào sổ, trạng thái chua-kiem
uv run python tools/verify.py --ghi-dot 5.1     # bằng chứng đạt → da-kiem
uv run python tools/verify.py --tien-do 5.1
uv run python tools/verify.py --mau 5.1         # rồi agent kiểm thứ hai làm verification/mau/5.1/*.json
uv run python tools/verify.py --so-mau 5.1      # tỉ lệ lỗi nghiêm trọng bị bỏ sót ≤ 2%
uv run python tools/verify.py --dong-bang 5.1 --chu-bien-duyet YYYY-MM-DD
```

Thay đổi cơ học (mục 5, bước 3) chứng minh "không đổi chữ" bằng:

```bash
uv run python tools/parity.py --base main   # so văn bản hiển thị, <title>, description, id của mọi trang
```

Sửa nguồn của một trang sinh tự động thì chạy lại tool đó **không** kèm `--check` (ví dụ `uv run python tools/philosophers.py`), rồi mới chạy bộ kiểm tra. Các tool mới của kế hoạch (registry, sổ kiểm chứng, linter) được thêm vào danh sách này khi đợt tương ứng xong; `KE-HOACH.md` ghi danh sách hiện hành.

## 5. Một phiên làm việc

1. Đọc mục 2. Xác định phần việc nhỏ của phiên: tối đa 3 đơn vị nội dung, hoặc đúng một thay đổi cơ học (do script).
2. Làm. **Sau mỗi đơn vị**, thêm một dòng vào `ban-giao/nhat-ky-dot-N.md`: ngày, việc, file, trạng thái, còn gì. Phiên có thể bị ngắt bất cứ lúc nào; nhật ký là thứ giữ lại công việc.
3. Thay đổi cơ học phải chứng minh "không đổi chữ" bằng kiểm tra tương đương: `tools/parity.py --base main` (mục 4).
4. Chạy bộ kiểm tra đầy đủ. Đỏ thì sửa; không sửa được trong phạm vi đợt thì dừng và báo.
5. Commit trên nhánh, message dạng `Đợt N: <việc>`. Agent thêm dòng `Co-Authored-By` của mình. Xong việc: merge `--no-ff` vào `main` trên máy (luật 6), ghi dòng "merge vào `main`" trong nhật ký. Chưa push nếu đợt chưa xong.
6. Kết thúc bằng báo cáo theo mẫu ở mục 7.

## 6. Khi nào dừng và hỏi chủ biên

- Việc cần một quyết định chưa có trong bảng Quyết định của `KE-HOACH.md`. (Quyết định còn "chờ" thì dùng phương án Đề xuất và ghi rõ trong báo cáo.)
- Cổng của đợt không đạt, và cách sửa đụng tới phạm vi của đợt khác.
- Thấy lỗi nội dung khi đang làm một đợt không phải đợt 5: ghi vào `ban-giao/viec-cho.md`, không sửa.
- Các nguồn mâu thuẫn nhau về cùng một dữ kiện.
- Cần xóa file, đổi URL, đổi cấu trúc thư mục, nâng phiên bản thư viện, hoặc đụng tới repo logos-zero.

## 7. Mẫu báo cáo cuối phiên

```markdown
## Báo cáo — Đợt N, phiên <YYYY-MM-DD>
- Đã làm: …
- File thay đổi: …
- Kiểm tra: generator --check ✓/✗ · content_registry --check ✓/✗ · build --strict ✓/✗ · unittest ✓/✗ · npm test ✓/✗ (số test pass)
- Cổng của đợt: đạt / chưa đạt — còn thiếu: …
- Bằng chứng (nếu có): verification/evidence/…
- Quyết định đã dùng theo Đề xuất (nếu có): …
- Câu hỏi mở cho chủ biên: …
- Việc tiếp theo đề xuất: …
```

## 8. Từ vựng của kế hoạch

| Từ | Nghĩa |
|---|---|
| Lõi | kiến thức kinh điển, kiểm chứng một lần rồi đóng băng |
| Mở rộng | mọi thứ thêm sau; mỗi lần chỉ kiểm phần thêm |
| Đơn vị | một mục H2 của trang (`trang.md#id-muc`) hoặc một bản ghi dữ liệu (`people/kant`) |
| Kho dữ kiện | `data/kb/`: người, tác phẩm, trích dẫn, sự kiện, nguồn, số liệu PhilPapers |
| Sổ kiểm chứng | `verification/ledger.json`: mỗi đơn vị một dòng, có mã băm và bằng chứng |
| Khối thời sự | đoạn có hạn dùng (luật, số liệu, AI hiện nay), tách ra `data/thoi-su/`, có hạn rà soát |
| Kiểm tra tương đương | so văn bản hiển thị của mọi trang trước và sau một thay đổi cơ học |
| Cổng | điều kiện bắt buộc để đóng một đợt |
