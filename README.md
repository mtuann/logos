# Logos

Website triết học bằng tiếng Việt, cho người bắt đầu từ con số 0: bản làm lại của Logos Zero theo `KE-HOACH.md`.
Địa chỉ: <https://mtuann.github.io/logos/>. Logos Zero (<https://mtuann.github.io/logos-zero/>, repo `mtuann/logos-zero`) vẫn chạy song song, độc lập; repo này bắt đầu từ bản nhập nguyên trạng `logos-zero@ecb2bb8` (tag `v1.0-moc`).

Site tĩnh (ProperDocs 1.6.7, bản kế tục MkDocs 1.x, + Material for MkDocs 9.8.0; phiên bản ghim trong `uv.lock`), không có máy chủ. Các công cụ tương tác viết bằng JavaScript thuần, dữ liệu người học chỉ lưu trong `localStorage` của trình duyệt.

## Cấu trúc repo

```
docs/                     nội dung Markdown
  bat-dau/                Bài 0, ba con đường đọc
  cong-cu/                trục kỹ năng: Công cụ tư duy (15 bài)
  cau-hoi/                trục chủ đề: Những câu hỏi lớn (57 bài, 11 chủ đề)
  lich-su/                lịch sử tư tưởng (8 bài), dòng thời gian, sơ đồ ảnh hưởng (sinh tự động)
  doc/                    hướng dẫn đọc văn bản gốc (19 bài)
  triet-gia/              trang triết gia (sinh tự động, KHÔNG sửa tay)
  luyen-tap/              trang công cụ: nhận ra ngụy biện, thẻ ghi nhớ, ôn tập, kế hoạch học
  them/                   từ điển (sinh tự động), dữ liệu của tôi, nhật ký, tham khảo, cập nhật, sách in (sinh tự động)
  assets/js/              mỗi công cụ một file (xem dưới)
  assets/css/oz.css       CSS chung (màu, công cụ, in)
  assets/data/            fallacies.json (ngụy biện), terms.json (thuật ngữ), philosophers.json (triết gia, sinh từ data/kb/people.yml),
                          quiz-bank.json (sinh từ quiz trong bài)
  manifest.webmanifest    PWA
  sw.js                   service worker (đọc ngoại tuyến trang đã mở)
hooks/
  slugs.py                anchor tiếng Việt không dấu ("Đọc văn bản" → doc-van-ban)
  search_vi.py            bỏ box Tóm tắt 5 phút khỏi chỉ mục tìm kiếm (bỏ dấu: docs/assets/js/search-worker.js, đợt 4.5)
  kb.py                   shortcode: [[count:…]] số đếm (content.yml, file dữ liệu), [[pp:…]] số liệu PhilPapers,
                          [[thoi-su:…]] khối thời sự data/thoi-su/; khóa sai thì build dừng
tools/                    mọi tool sinh trang đều có --check (CI chạy hết)
  gen_glossary.py         docs/them/tu-dien.md từ terms.json
  philosophers.py         docs/triet-gia/*.md và philosophers.json từ data/kb/people.yml + data/people/<id>.yml; tự tính
                          "chịu ảnh hưởng từ" và danh sách bài có link tới từng triết gia
  timeline.py             dòng thời gian (SVG) từ philosophers.json
  influence.py            sơ đồ ảnh hưởng (SVG) từ trường "influence"
  figures.py              hình minh họa SVG chèn giữa <!-- fig:TÊN --> … <!-- /fig:TÊN -->
  quiz_bank.py            docs/assets/data/quiz-bank.json từ quiz trong các bài
  book.py                 sách in docs/them/sach.md theo thứ tự nav
  review_check.py         mục "Tình trạng rà soát" ở trang Cập nhật
  frontmatter_check.py    front matter YAML hợp lệ
  content_registry.py     sổ đăng ký content.yml: --init (sinh lần đầu từ nav), --check (CI),
                          --sync-frontmatter (ghi tier, block vào front matter trang viết tay)
  baseline_report.py      báo cáo nền verification/bao-cao-nen.md (số đo trước khi làm lại; không chạy lại)
  github_labels.sh        tạo nhãn GitHub của kế hoạch (cần gh)
  add_heading_ids.py      gắn ID cố định {#id} cho mục H2 của Lõi, lấy đúng anchor đang build ra; --check (CI)
  kb_sources.py           data/kb/sources.yml từ mọi mục Nguồn và sources của hồ sơ (giữ archive, accessed, verified);
                          danh sách lệch verification/lech/sources.md; --check (CI)
  kb_works.py             data/kb/works.yml từ "*Tên* (năm)" và danh sách tác phẩm của hồ sơ; lệch: verification/lech/works.md
  kb_quotes.py            data/kb/quotes.yml từ khối !!! quote (thân nguyên văn) và quote của hồ sơ; lệch: verification/lech/quotes.md
  kb_events.py            data/kb/events.yml: ứng viên sự kiện (năm + câu) ở khối lich-su, viet-nam và câu có nhãn độ chắc chắn
  sep_archive.py          đổi link SEP sang bản lưu fall2026 (quyết định 14) sau khi mở thử từng mục; --dry-run, --cache
  kb_check.py             kho dữ kiện: schema (jsonschema), khóa trùng, tham chiếu chéo, used_in còn tồn tại
  nav_gen.py              nav của mkdocs.yml sinh từ mục nav của content.yml (đợt 4.9); --check
  works_page.py           trang chỉ mục tác phẩm docs/tac-pham/index.md từ data/kb/works.yml (quyết định 23); --check
  verification_page.py    trang Tình trạng kiểm chứng docs/them/kiem-chung.md từ sổ kiểm chứng; --check
  thoi_su_check.py        khối thời sự data/thoi-su/*.md: schema, id, mỗi khối được đúng trang của nó dùng một lần
  migrate/                script chuyển đổi một lần, giữ lại để đọc và chạy lại (chạy lại không đổi gì):
                          dot2_people.py (hồ sơ → YAML), dot3_thoi_su.py (dời đoạn có hạn dùng),
                          dot3_so_dem.py (số đếm → [[count:…]]), dot3_philpapers.py (ô PhilPapers → [[pp:…]];
                          lệch: verification/lech/philpapers-bang.md); thay_shortcode.py (thay có kiểm, dùng chung)
  check_ledger.py         sổ kiểm chứng verification/ledger.json: --check (CI), --status (tiến độ theo khối),
                          --hash KHÓA (mã băm hiện tại của đơn vị hoặc bản ghi: people/kant, ho-so/kant…)
  changed_units.py        báo cáo đơn vị đổi chữ giữa hai phiên bản (tầng, khối, trạng thái sổ, việc cần làm);
                          CI đăng thành bình luận PR, hoặc vào job summary khi push
  terms_policy.py         data/style/terms-policy.yml từ bảng thuật ngữ ở HUONG-DAN-VIET.md mục 3; --check (CI)
  lint_terms.py           cách dịch bị tránh, tên riêng sai (Plato → Platon) trong Lõi viết tay
  lint_volatile.py        nội dung có hạn dùng: năm 2022+, "hiện nay"…, văn bản luật; khối thời sự quá hạn;
                          danh sách miễn data/style/volatile-allow.yml (quyết định 20); CHẶN trong CI từ đợt 3
  lint_structure.py       thiếu mục bắt buộc theo loại trang; nhãn độ chắc chắn đặt sai chỗ
  lint_facts.py           năm tác phẩm, năm sinh mất trong văn xuôi so với works.yml, people.yml
  lint_quotes.py          khối !!! quote so với quotes.yml; trích dẫn chưa ghép tác phẩm, chưa có vị trí
                          (ba linter: chế độ cảnh báo; --write ghi verification/lint/, --strict để chặn)
  parity.py               kiểm tra tương đương: so văn bản hiển thị, <title>, description, id của mọi trang
                          giữa hai bản build (--base REF: tự build commit REF và cây làm việc;
                          --expect-sub REGEX THAY: thay đổi có chủ đích, áp lên bản trước rồi mới so)
  lz/                     thư viện dùng chung cho công cụ kiểm chứng (KE-HOACH.md mục 5.5–5.6):
                          registry (đọc content.yml), units (tách đơn vị theo H2, khóa trang.md#id),
                          normalize (chuẩn hóa trên nguồn Markdown), hashing (sha256:…)
  philpapers-2020.md      số liệu PhilPapers 2020 (bản đọc), sinh từ data/kb/philpapers-2020.json bằng kb_philpapers.py
  kb_philpapers.py        philpapers-2020.md từ JSON; --check (CI); --import-md (chuyển một lần, đợt 2)
tests/
  unit/                   kiểm thử hàm thuần + tương phản màu WCAG
  browser/                jsdom: mở mọi trang đã build qua bộ tải thật; axe-core; tìm kiếm
  test_hooks.py           kiểm thử hook Python và script sinh trang
  test_kb_sources.py       tools/kb_sources.py: phân loại, khóa, mọi mục Nguồn có bản ghi
  test_kb_works.py        tools/kb_works.py: mẫu năm, gán tác giả, 159 chỗ như báo cáo nền
  test_kb_quotes.py       tools/kb_quotes.py: tách khối, ghép ngược đúng từng chữ
  test_kb_philpapers.py   JSON ↔ philpapers-2020.md giống từng byte
  test_kb_events.py       tools/kb_events.py: mẫu năm, bỏ năm tác phẩm và năm sinh mất
  test_kb_check.py         tools/kb_check.py: bản ghi mẫu mỗi loại và từng loại lỗi
  test_thoi_su.py         tools/thoi_su_check.py: khối thiếu, thừa, dùng sai trang, sai schema
  test_dot3.py            script đợt 3: không còn ô PhilPapers khớp JSON mà còn gõ tay; số đếm, khối thời sự đã thay
  test_ledger.py          tools/check_ledger.py: schema, đơn vị đóng băng, bằng chứng
  test_changed_units.py   tools/changed_units.py trên một repo git tạm
  test_linters.py         terms_policy và ba linter
  test_parity.py          tools/parity.py: trích văn bản hiển thị, phát hiện lệch
  test_lz.py              thư viện tools/lz: mọi hệ quả của chuẩn hóa và băm (KE-HOACH.md mục 5.6)
  test_indexes.py         chỉ mục mỗi mục liệt kê đủ bài; Kế hoạch học trỏ tới trang có thật;
                          không có văn xuôi lọt vào khối code
content.yml               sổ đăng ký: mỗi trang, mỗi file dữ liệu một dòng (loại, tầng, khối, sinh tự động?)
schema/content.schema.json  giá trị cho phép của content.yml
schema/kb/                schema của kho dữ kiện (người, hồ sơ, tác phẩm, trích dẫn, sự kiện, nguồn, PhilPapers)
data/kb/, data/people/    kho dữ kiện và hồ sơ triết gia (đợt 2)
verification/             báo cáo nền; sổ kiểm chứng ledger.json (schema/ledger.schema.json); evidence/ bằng chứng
AGENTS.md, KE-HOACH.md, ban-giao/  luật cho agent, kế hoạch làm lại, việc từng đợt (không xuất bản)
overrides/main.html       tùy biến Material (manifest, "cập nhật lần cuối", link "Báo lỗi trang này")
HUONG-DAN-VIET.md         hướng dẫn văn phong, thuật ngữ thống nhất, cú pháp Markdown
```

### JavaScript

| File | Vai trò |
|---|---|
| `core.js` | `window.OZReady(init)`: chạy `init` mỗi lần trang hiển thị (kể cả instant navigation); `OZ.base`; nút "In bài này"; đăng ký service worker |
| `progress.js` | một khóa `localStorage` (`logos`, khác khóa `logos-zero` của site cũ vì hai site cùng origin), có phiên bản; độ chính xác EMA theo kỹ năng, lịch sử theo ngày, quiz, bài đã đọc, thẻ |
| `loader.js` | quét trang, chỉ nạp script công cụ cần thiết, đúng thứ tự (`async = false`) |
| `util.js` | tiện ích chung: tạo DOM, xáo trộn có hạt giống, tải JSON, vùng `aria-live` |
| `quiz.js`, `fallacy.js`, `flashcards.js`, `daily.js`, `mydata.js` | các công cụ |

`mkdocs.yml` chỉ nạp `core.js`, `progress.js`, `loader.js`. Trang chỉ có chữ không tải thêm gì.

## Chạy trên máy

Cần [uv](https://docs.astral.sh/uv/). uv tự cài Python 3.13 theo `.python-version` và đúng các phiên bản trong `uv.lock`.

```bash
uv sync --frozen
uv run properdocs serve -f mkdocs.yml   # http://127.0.0.1:8000/logos/
```

Không dùng uv: tạo virtualenv với Python 3.11+, `pip install -r requirements.txt` (sinh từ `uv.lock`, có hash), rồi chạy các lệnh dưới đây không kèm `uv run`. Sau khi sửa `pyproject.toml`: `uv lock`, rồi `uv export --frozen --format requirements-txt --no-emit-project -o requirements.txt`.

## Kiểm thử

Cần uv (hoặc Python 3.11+) và Node 24.15+.

```bash
npm ci
for t in gen_glossary figures review_check timeline influence philosophers book frontmatter_check quiz_bank terms_policy kb_sources kb_works kb_quotes kb_philpapers kb_events works_page verification_page nav_gen; do
  uv run python tools/$t.py --check || break  # trang/dữ liệu sinh tự động khớp nguồn
done
uv run python tools/content_registry.py --check  # content.yml khớp trang và dữ liệu
uv run python tools/add_heading_ids.py --check   # mọi mục H2 của Lõi có ID cố định {#id}
uv run python tools/check_ledger.py --check      # sổ kiểm chứng đúng dạng; đơn vị đóng băng không đổi mã băm
uv run python tools/kb_check.py --check          # kho dữ kiện data/kb/, data/people/ khớp schema/kb/ và tham chiếu chéo
uv run python tools/thoi_su_check.py --check     # khối thời sự data/thoi-su/ khớp schema, mỗi khối dùng đúng một lần
uv run python tools/lint_volatile.py --strict -q  # chặn từ đợt 3: có hạn dùng thì ở data/thoi-su/ hoặc data/style/volatile-allow.yml
for l in lint_terms lint_structure lint_facts lint_quotes; do uv run python tools/$l.py -q; done  # linter, chế độ cảnh báo
uv run properdocs build --strict -f mkdocs.yml  # build sạch, kiểm tra link và anchor
uv run python -m unittest discover -s tests     # hook, tool Python, chỉ mục
npm test                                        # hàm thuần, màu, trình duyệt (jsdom), axe-core, tìm kiếm
npm run test:real                               # axe trên Chromium thật, 10 trang mẫu × 2 cỡ × sáng/tối (Playwright)
npm run anh                                     # ảnh chụp 10 trang mẫu vào site-anh/ (không commit; CI tải lên artifact)
```

Thay đổi cơ học (do script, không được đổi chữ) phải qua kiểm tra tương đương trước khi merge:

```bash
uv run python tools/parity.py --base main      # build main và cây làm việc, so từng trang; mã thoát 1 khi lệch
```

`npm test` và một phần `tests/test_indexes.py` cần thư mục `site/` đã build. CI (`.github/workflows/deploy.yml`) chạy tất cả các bước trên trước mỗi lần deploy lên GitHub Pages. `links.yml` kiểm tra link web mỗi tuần bằng lychee (chấp nhận 403 và 202 vì nhiều trang chặn bot); khi có link hỏng thì mở hoặc cập nhật một issue nhãn `link-hong`, khi hết lỗi thì tự đóng issue.

Người đọc báo lỗi qua link "Báo lỗi trang này" cuối mỗi trang: link mở mẫu `.github/ISSUE_TEMPLATE/bao-loi.yml` (nhãn `bao-loi`), điền sẵn tên và đường dẫn trang. Địa chỉ đặt ở `extra.report_issue_url` trong `mkdocs.yml`.

## Thêm một công cụ mới

1. Viết `docs/assets/js/ten-cong-cu.js` theo mẫu UMD của các file có sẵn: xuất các hàm thuần qua `module.exports` (để kiểm thử), và trong trình duyệt gọi `OZReady(initAll)`. `init` phải idempotent: dùng `OZ.util.claim(node)`.
2. Thêm một dòng vào bảng `TOOLS` trong `loader.js`: `{ sel: ".oz-ten-cong-cu", js: ["util.js", "ten-cong-cu.js"] }`.
3. Nhúng vào trang Markdown: `<div class="oz-ten-cong-cu"></div>`.
4. Thêm kiểm thử đơn vị trong `tests/unit/`, và bộ chọn vào `TOOL_SELECTORS` trong `tests/browser/site.test.js`.

## Thêm nội dung

Đọc `HUONG-DAN-VIET.md` trước: văn phong, bảng thuật ngữ bắt buộc, cú pháp quiz và admonition. Mỗi bài có front matter `title`, `description`, `skill`, `updated`, và mục `## Nguồn` ở cuối.

Thêm một bài mới:

1. Viết bài trong thư mục của mục (ví dụ `docs/cau-hoi/`), thêm vào `content.yml` (cả `pages` lẫn `nav`; rồi chạy `python tools/nav_gen.py` để chép nav vào `mkdocs.yml`) **và** vào trang `index.md` của mục (kiểm thử `tests/test_indexes.py` sẽ báo nếu quên); nếu hợp, thêm vào `CATALOG` của `docs/assets/js/ke-hoach.js`.
2. Lần đầu nhắc tới một triết gia đã có trang, đặt link `[Tên](../triet-gia/<id>.md)`.
3. Chạy lại các tool sinh trang bị ảnh hưởng: `python tools/quiz_bank.py` (nếu có quiz), `python tools/philosophers.py` (nếu có link tới triết gia), `python tools/book.py` (luôn luôn — sách in gộp mọi bài), `python tools/review_check.py`.

Thuật ngữ mới: thêm vào `docs/assets/data/terms.json`, rồi chạy `python tools/gen_glossary.py`.

Đoạn có hạn dùng (luật đang hiệu lực, số liệu đang đổi, tình trạng AI hiện tại; quyết định 20) không viết thẳng vào bài Lõi: đặt vào khối thời sự `data/thoi-su/<trang>.<tên-ngắn>.md` (front matter `page`, `updated_to`, `review_by`, `sources`; schema `schema/thoi-su.schema.json`) và gọi trong bài bằng `[[thoi-su:<id>]]`. Rà khối khi tới `review_by`: sửa thân khối, cập nhật hai ngày; mã băm của bài Lõi không đổi. Chỗ `lint_volatile` bắt mà không có hạn dùng: thêm vào `data/style/volatile-allow.yml` kèm lý do.

Thêm một triết gia (từ đợt 7): thêm bản ghi vào `data/kb/people.yml` và hồ sơ `data/people/<id>.yml` (bắt buộc có `sources`; schema ở `schema/kb/`), thêm vào `nav`, rồi chạy `python tools/kb_check.py --check` và `philosophers.py`, `timeline.py`, `influence.py`.

## Thêm hình minh họa

Hình được sinh từ mã nguồn bằng `tools/figures.py` (SVG inline dùng biến màu của site và `currentColor`, nên tự theo chế độ sáng/tối/in), chèn giữa các dấu `<!-- fig:TÊN -->` … `<!-- /fig:TÊN -->`, và có chế độ `--check` trong CI.
