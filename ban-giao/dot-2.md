# Đợt 2 — Kho dữ kiện

- **Thời gian dự kiến**: 23/11–6/12/2026 (đợt 1 đóng sớm ngày 5/11/2026, nên có thể bắt đầu ngay). **Điều kiện bắt đầu**: đợt 1 đã đóng (tag `v1.1`, CI xanh).
- **Mục tiêu**: rút dữ kiện (người, tác phẩm, trích dẫn, sự kiện, nguồn, số liệu PhilPapers) từ trang và từ `tools/philosophers.py` vào kho `data/kb/` bằng script, kèm schema. Chuyển 59 hồ sơ triết gia sang `data/people/<id>.yml`. **Loại thay đổi: dữ liệu.** Chưa sửa dữ kiện sai: chỉ ghi danh sách lệch cho đợt 5.
- **Nhánh**: mỗi việc một nhánh `dot-2-<ten-ngan>`, merge vào `main` trên máy khi xong; push khi xong cả đợt (AGENTS.md luật 6).
- **Tiến độ**: `ban-giao/nhat-ky-dot-2.md`.

## Việc

| # | Việc | Loại | Kết quả kiểm được |
|---|---|---|---|
| 2.1 | Schema cho sáu loại bản ghi `schema/kb/{people,works,quotes,events,sources,philpapers}.schema.json` (đặc tả dưới); `tools/kb_check.py --check` kiểm mọi file trong `data/kb/` và `data/people/` theo schema, khóa trùng, tham chiếu chéo (`works.author` → `people`, `quotes.work` → `works`, `evidence`/`source` → `sources`); thêm vào CI và `AGENTS.md` mục 4 | công cụ | `kb_check --check` đỏ khi bản ghi sai; kiểm thử cho từng loại lỗi |
| 2.2 | `data/kb/people.yml` (59 người, từ `philosophers.json`) và `data/people/<id>.yml` (phần văn của 59 hồ sơ, từ `CONTENT` trong `tools/philosophers.py`, quyết định 7) bằng script một–một. `philosophers.py` đọc YAML thay cho `CONTENT`; `philosophers.json` thành file sinh từ `people.yml` (cập nhật `content.yml`: `generated: true`; `tools/philosophers.py` không còn là file dữ liệu) | cơ học | 59 trang `triet-gia/*.md` và `index.md` **giống từng byte**; `philosophers.json`, dòng thời gian, sơ đồ ảnh hưởng giống từng byte; parity 100% |
| 2.3 | `data/kb/sources.yml` (`tools/kb_sources.py`, có `--check`; mỗi mục Nguồn một bản ghi khóa theo URL đầu, URL phụ ở `also`): gộp mọi mục Nguồn (628 trong Lõi viết tay, 898 khi tính cả hồ sơ) và `sources` của hồ sơ, khử trùng theo URL; phân loại (`sep`, `iep`, `gutenberg`, `wikisource`, `ctext`, `cbeta`, `doi`, `sach`, `khac`); ghi danh sách trang dùng mỗi nguồn | dữ liệu | mỗi URL một bản ghi; mọi mục Nguồn ánh xạ được tới một bản ghi, hoặc nằm trong danh sách lệch |
| 2.4 | Link SEP sang bản lưu theo quý (quyết định 14): script đổi `plato.stanford.edu/entries/<mục>/` → `plato.stanford.edu/archives/<quý>/entries/<mục>/` ở trang viết tay và hồ sơ, **chỉ** khi bản lưu trả 200 (script mở thử từng mục: 186 mục dạng `entries/`, cộng 1 link đã là bản lưu fall2024); mục không có bản lưu thì giữ link cũ và ghi danh sách lệch. Ghi `archive` và `accessed` vào `sources.yml` | cơ học (chỉ đổi URL) | parity: chỉ lệch ở chữ URL SEP (script so lệch với bảng ánh xạ cũ → mới, ngoài ra 0); `build --strict` xanh |
| 2.5 | `data/kb/works.yml`: gom tác phẩm từ các chỗ "*Tác phẩm* (năm)" (159 trong Lõi viết tay, 415 khi tính cả hồ sơ) và danh sách `works` của hồ sơ; khóa `<tác giả>.<slug tên>`; ghi mọi cách viết tên và mọi năm gặp được; năm khác nhau giữa các trang thì vào danh sách lệch | dữ liệu | `verification/lech/works.md` liệt kê mọi tác phẩm có hơn một năm hoặc hơn một cách viết |
| 2.6 | `data/kb/quotes.yml`: tách 156 khối trích dẫn (108 `!!! quote` trong Lõi viết tay, 48 `quote` của hồ sơ; số ngày 23/10 là 157) giữ nguyên chữ: tiêu đề khối, nguyên văn, bản dịch, ghi chú "(bản dịch của Logos Zero)", URL. Khóa theo `<tác giả>.<tác phẩm>.<vị trí>` khi rút được, không thì `<trang>.<số thứ tự>` và vào danh sách lệch. Trang **chưa** đổi sang shortcode (quyết định 3: trích dẫn đối chiếu bằng linter) | dữ liệu | mỗi khối có đúng một bản ghi; ghép ngược bản ghi ra khối cho cùng chữ (kiểm thử) |
| 2.7 | `data/kb/philpapers-2020.json` từ `tools/philpapers-2020.md` (87 câu, câu chính/bổ sung, % bao gồm, % loại trừ khi có, n); `.md` sinh lại từ JSON, giống từng byte. 13 câu còn thiếu: chỉ bổ sung nếu mở được Bảng 1–2 của bài báo (DOI `10.3998/phimp.2109`) hoặc trang kết quả chính thức trong phiên; không mở được thì ghi "Câu hỏi mở" | dữ liệu | `.md` sinh lại giống từng byte; 87 (hoặc 100) câu qua schema |
| 2.8 | `data/kb/events.yml`: rút ứng viên sự kiện (năm + câu chứa nó) từ các bài khối `lich-su` và `viet-nam`, và mọi câu có nhãn độ chắc chắn; mỗi ứng viên một bản ghi `verified: null`, ghi trang và đơn vị nguồn. Đợt con 5.2 lọc và kiểm | dữ liệu | mọi năm trong các bài đó có bản ghi hoặc nằm trong danh sách bỏ qua có lý do |
| 2.9 | `tools/lint_facts.py` (năm và tên tác phẩm trong văn xuôi lệch `works.yml`) và `tools/lint_quotes.py` (khối trích không khớp `quotes.yml`), chế độ cảnh báo, báo cáo nền vào `verification/lint/`; `check_ledger.py` nhận khóa bản ghi (`people/kant`, `quotes/…`), mã băm bằng `lz.hashing.record_hash` | công cụ | CI chạy hai linter; `check_ledger --hash people/kant` in mã băm |

Thứ tự đề xuất: 2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6 → 2.7 → 2.8 → 2.9. Việc 2.4 là thay đổi duy nhất đụng chữ hiển thị (URL trong mục Nguồn); việc 2.2 đụng `tools/philosophers.py` nhưng không đổi trang sinh ra.

## Đặc tả

Mọi bản ghi có `evidence` (danh sách khóa trong `sources.yml` hoặc URL đã mở; được rỗng khi mới rút) và `verified` (`null`, hoặc `{date: YYYY-MM-DD, by: <người/phiên>}`; chỉ đợt 5 điền). Khóa: chữ thường, không dấu, `[a-z0-9.-]`. YAML: một file một loại, dạng ánh xạ `khóa: bản ghi`, sắp theo khóa (để diff gọn); riêng `people.yml` giữ thứ tự của `philosophers.json` (thứ tự biên tập, hiện ở trang chỉ mục, không theo năm).

```yaml
# data/kb/people.yml
kant:
  name: Immanuel Kant            # tên dùng trên site (giữ đúng philosophers.json: "name")
  name_en: Immanuel Kant
  born: {year: 1724}             # {year, approx: true} cho "k."; năm TCN là số âm
  died: {year: 1804}
  years_label: "1724–1804"       # chuỗi đang hiện trên site, giữ nguyên để trang giống từng byte
  school: Cận đại
  summary: "…"
  influence: [hume, leibniz]
  evidence: []
  verified: null

# data/kb/works.yml
kant.phe-phan-ly-tinh-thuan-tuy:
  author: kant
  titles: ["Phê phán lý tính thuần túy"]       # mọi cách viết gặp trong trang; cái đầu là cách chuẩn
  title_orig: "Kritik der reinen Vernunft"
  year: 1781                                    # null khi các trang lệch nhau (xem verification/lech/works.md)
  years_seen: {1781: ["cau-hoi/tri-thuc.md#…"]}
  evidence: []
  verified: null

# data/kb/quotes.yml
platon.bien-ho.38a:
  work: platon.bien-ho           # null khi chưa ghép được
  locator: "38a"
  title: "…"                     # tiêu đề khối !!! quote, nguyên văn
  original: "…"                  # đoạn nguyên văn (có thể rỗng)
  translation: "…"               # bản dịch tiếng Việt như trên trang
  translator: logos-zero         # logos-zero | <tên người dịch> | null
  license: public-domain         # public-domain | fair-use-short | unknown
  url: https://www.gutenberg.org/ebooks/1656
  used_in: ["index.md#_dau"]
  evidence: []
  verified: null

# data/kb/sources.yml
sep.knowledge-analysis:
  type: sep
  author: "Ichikawa, Jonathan Jenkins & Matthias Steup"
  title: "The Analysis of Knowledge"
  url: https://plato.stanford.edu/entries/knowledge-analysis/
  archive: https://plato.stanford.edu/archives/fall2026/entries/knowledge-analysis/
  accessed: 2026-11-05
  used_in: ["cau-hoi/tri-thuc.md#nguon"]

# data/kb/events.yml
dai-viet.khoa-thi-1075:
  year: 1075
  text: "khoa thi Nho học đầu tiên"      # câu gốc (rút gọn) trong trang
  certainty: chac-chan                    # theo nhãn trong bài, nếu có
  used_in: ["lich-su/nhat-ban-viet-nam.md#…"]
  evidence: []
  verified: null
```

`philpapers-2020.json`: `{"source": {...}, "questions": [{"id": "free-will", "title_vi": "...", "table": 1|2, "n": 1770, "options": [{"id": "compatibilism", "label_vi": "...", "pct": 59.2, "pct_exclusive": null}]}]}`; khóa số liệu dạng `free-will.compatibilism` (KE-HOACH.md mục 5.4).

Danh sách lệch: `verification/lech/<loại>.md`, sinh bằng script, chạy lại cho cùng kết quả. Đây là đầu vào của đợt 5, không sửa trong đợt 2.

## Lưu ý kỹ thuật

- **Byte-identical**: trước việc 2.2, chép `docs/triet-gia/` và `docs/assets/data/philosophers.json` ra thư mục tạm; sau khi đổi `philosophers.py`, chạy lại `philosophers.py`, `timeline.py`, `influence.py` và `diff -r`. Chú ý thứ tự khóa, dấu ngoặc kép cong, dòng trống cuối file khi dump YAML (dùng `allow_unicode=True`, `sort_keys=False`, `width` lớn; kiểm thử đọc lại).
- Tuple trong `CONTENT` (`works`, `related`, `sources`) thành ánh xạ có tên trường (`year`, `title`, `note`; `path`, `title`; `text`, `url`) trong `data/people/<id>.yml`.
- Năm "k. 624–546 TCN": `born: {year: -624, approx: true}`; giữ `years_label` để không phải tái tạo chuỗi.
- Việc 2.4 mở mạng: mỗi URL một lần, có `--cache` (file JSON trong thư mục tạm) để chạy lại không gọi lại; ghi kết quả HTTP vào danh sách lệch. Không đổi link nào chưa mở được.
- Rút dữ kiện bằng regex từ nguồn Markdown, dùng `lz.units` để ghi đơn vị (`used_in`); dùng `lz.lint.masked_lines` khi cần bỏ code, khối sinh.
- Không có thư viện JSON Schema trong môi trường: theo quyết định 13.
- Chạy kiểm tra tương đương sau 2.2 và 2.4 (`tools/parity.py --base main`), và `tools/changed_units.py --base main` để xác nhận đơn vị đổi chỉ là các mục Nguồn có link SEP.

## Cổng

- [ ] 100% bản ghi qua schema (`kb_check --check` xanh, trong CI).
- [ ] 59 trang triết gia (và `index.md`, `philosophers.json`, dòng thời gian, sơ đồ ảnh hưởng) giống từng byte sau việc 2.2.
- [ ] Link SEP dùng bản lưu theo quý; parity chỉ lệch ở URL SEP.
- [ ] Danh sách lệch lưu ở `verification/lech/` cho đợt 5.
- [ ] `lint_facts`, `lint_quotes` chạy trong CI (cảnh báo), có báo cáo nền.
- [ ] `AGENTS.md` mục 4, `README.md` có lệnh mới.
- [ ] CI xanh.

## Không làm

Sửa năm, tên, trích dẫn sai (chỉ ghi lệch, đợt 5); thay chữ trong bài bằng shortcode (đợt 3); tách khối thời sự (đợt 3); thêm triết gia hay bài mới (đợt 7); đổi giao diện.

## Đầu vào từ đợt 1

`tools/lz/` (units, normalize, hashing, lint), `tools/parity.py`, `tools/changed_units.py`, `tools/check_ledger.py`, ID cố định của mục H2 (dùng cho `used_in`), báo cáo nền `verification/bao-cao-nen.md` mục 4 (số chỗ "*Tác phẩm* (năm)", khối trích, mục Nguồn), `verification/lint/`.
