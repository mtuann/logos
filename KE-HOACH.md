# KE-HOACH.md — Kế hoạch làm lại Logos Zero trong repo logos (bản cho agent)

Bản gốc là tài liệu "Logos Zero — Kế hoạch phát triển bền vững" của chủ biên (hai tab: *Kế hoạch* và *Triển khai từng đợt*), ngày 23/10/2026.
File này là nguồn chính cho agent và người mới. Khi chủ biên đổi một quyết định, một ngày hay một cổng, sửa file này trong cùng PR.
Không xuất bản lên site.

Repo `logos` bắt đầu ngày 3/11/2026 từ bản nhập nguyên trạng `logos-zero@ecb2bb8` (tag `v1.0-moc`, cùng mã tree). Logos Zero chạy song song, độc lập (quyết định 9); kế hoạch này chỉ áp dụng cho repo `logos`.

## Trạng thái

| Đợt | Tên | Dự kiến | Trạng thái |
|---|---|---|---|
| 0 | Chốt mốc | 3/11–8/11/2026 | **Xong** 4/11/2026 (PR #1) — `ban-giao/dot-0.md`, nhật ký `ban-giao/nhat-ky-dot-0.md` |
| 1 | Công cụ nền | 9/11–22/11/2026 | **Xong** 5/11/2026 (tag `v1.1`) — `ban-giao/dot-1.md`, nhật ký `ban-giao/nhat-ky-dot-1.md` |
| 2 | Kho dữ kiện | 23/11–6/12/2026 | **Xong** 5/11/2026 (tag `v1.2`) — `ban-giao/dot-2.md`, nhật ký `ban-giao/nhat-ky-dot-2.md` |
| 3 | Tách thời sự và số đếm | 7/12–13/12/2026 | **Xong** 5/11/2026 (tag `v1.3`) — `ban-giao/dot-3.md`, nhật ký `ban-giao/nhat-ky-dot-3.md` |
| 4 | Giao diện tối thiểu | 14/12–20/12/2026 | **Xong** 5/11/2026 (tag `v1.4`) — `ban-giao/dot-4.md`, nhật ký `ban-giao/nhat-ky-dot-4.md` |
| — | Nghỉ cuối năm | 21/12/2026–3/1/2027 | — |
| 5 | Kiểm chứng và đóng băng Lõi | 4/1–14/3/2027 | **Xong** 20/11/2026 (chờ CI để gắn tag `v1.5`; đóng băng 5.1–5.8 chủ biên duyệt 20/11/2026) — `ban-giao/dot-5.md`, nhật ký `ban-giao/nhat-ky-dot-5.md` |
| 6 | Thiết kế lại giao diện | 15/3–25/4/2027 | **Xong** 20/11/2026 (chờ CI để gắn tag `v1.6`) — `ban-giao/dot-6.md`, nhật ký `ban-giao/nhat-ky-dot-6.md` |
| 7 | Vận hành Mở rộng | từ 26/4/2027 | **Đang làm** từ 20/11/2026 (chủ biên mở sớm) — `ban-giao/dot-7.md`, nhật ký `ban-giao/nhat-ky-dot-7.md` |

Đợt 0 bắt đầu muộn một tuần (3/11 thay vì 26/10), nên đợt 1–3 lùi một tuần và đợt 4 rút còn một tuần để giữ kỳ nghỉ cuối năm. Không đủ thì phần còn lại của đợt 4 sang tuần 4/1/2027 và đợt 5 lùi theo. Đây là đề xuất; chủ biên chỉnh nếu cần.
Material for MkDocs hết vòng đời ngày **5/5/2027**; bản đã ghim vẫn build được sau ngày đó (mục 11). Rà soát nền tảng hằng năm vào tháng 2, lần đầu **1/2/2027**.
Brief cho các đợt 2–7 viết theo `ban-giao/mau-dot.md` khi đợt trước đóng.

## 1. Mục tiêu

- **Lõi**: kiến thức kinh điển (công cụ tư duy, câu hỏi kinh điển, lịch sử, triết gia, văn bản gốc, thuật ngữ) được kiểm chứng một lần theo từng đơn vị, rồi đóng băng bằng mã băm. Chỉ đơn vị nào thay đổi mới phải kiểm lại.
- **Mở rộng**: mọi thứ thêm sau, đi vào năm ngăn (khối thời sự, bài chuyên đề, hồ sơ triết gia mới, hướng dẫn đọc mới, ngân hàng luyện tập). Mỗi lần chỉ kiểm phần thêm. Mở rộng được link vào Lõi; Lõi không phụ thuộc Mở rộng.
- **Một dữ kiện, một chỗ**: năm sinh mất, tên và năm tác phẩm, trích dẫn nguyên văn, số liệu PhilPapers, sự kiện lịch sử nằm trong kho dữ kiện có bằng chứng; trang gọi tới dữ kiện hoặc được máy đối chiếu với kho.
- **Thời gian hiện rõ**: luật, số liệu thời sự, "AI hiện nay" nằm trong khối thời sự có ngày cập nhật và hạn rà soát; thân bài Lõi không phụ thuộc thời gian.
- **Máy kiểm phần máy kiểm được** (nhất quán, số liệu, thuật ngữ, cấu trúc, link, số đếm); người hoặc agent chỉ kiểm phần ngữ nghĩa.

## 2. Nguyên tắc triển khai (bắt buộc)

1. **Mỗi đợt một loại thay đổi.** Không vừa chuyển công nghệ vừa sửa nội dung; không vừa sửa nội dung vừa đổi giao diện.
2. **Cơ học trước, ngữ nghĩa sau.** Thay đổi do script phải qua kiểm tra tương đương (văn bản hiển thị của mọi trang trước và sau giống nhau). Chỉ đợt 5 được sửa chữ trong nội dung.
3. **Site đang chạy luôn chạy.** Merge vào `main` chỉ khi CI xanh. Nếu phải đổi trình render (mục 11), dựng song song trên nhánh riêng và chỉ merge khi tương đương 100%. Không sửa repo logos-zero từ kế hoạch này.
4. **Không phá người đọc.** Giữ URL (đường dẫn trang như logos-zero, hoặc chuyển hướng), khóa `localStorage` `logos`, ID quiz, ID thuật ngữ.
5. **Mã băm tính trên nội dung chuẩn hóa** (mục 5.6), nên đổi định dạng hay đổi nền tảng không mở khóa Lõi.
6. **Không thêm nội dung mới trước khi Lõi đóng băng.** Ý tưởng vào issue nhãn `cho`, làm từ đợt 7.

## 3. Quyết định

Quyết định còn "chờ" thì agent dùng phương án **Đề xuất** và ghi rõ trong báo cáo. Chủ biên đổi cột Trạng thái khi chọn.

| # | Quyết định | Đề xuất | Phương án khác | Trạng thái |
|---|---|---|---|---|
| 1 | Kích thước Lõi | Toàn bộ nội dung hiện có, sau khi tách khối thời sự | Chỉ phần nhập môn; 11 bài luân lý ứng dụng và thời sự sang Mở rộng | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 2 | Đơn vị đóng băng | Mục H2 | Cả trang | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 3 | Dữ kiện trong văn xuôi | Shortcode cho số liệu PhilPapers và số đếm; linter đối chiếu năm và tên tác phẩm | Shortcode cho mọi dữ kiện | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 4 | Mức chặt của sổ kiểm chứng | CI chặn khi Lõi đổi mà sổ chưa cập nhật | Chỉ cảnh báo | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 5 | Ai xác nhận "đã kiểm" | Agent kiểm theo checklist; chủ biên duyệt mẫu 10% | Chủ biên duyệt toàn bộ, hoặc chỉ agent | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 6 | Ba bài Tư tưởng Việt Nam | Lõi, bắt buộc nhãn độ chắc chắn | Ngăn chuyên đề cho tới khi có thêm nguồn học thuật | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 7 | Nơi lưu hồ sơ triết gia | `data/people/<id>.yml`, mỗi người một file | Giữ trong `tools/philosophers.py` | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 8 | Thêm bài trong lúc làm đợt 0–5 | Tạm dừng; ý tưởng ghi vào danh sách chờ | Thêm song song trên nhánh riêng | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 9 | Quan hệ với logos-zero | — | — | **đã chốt 3/11/2026**: hai site song song, độc lập; logos-zero giữ nguyên, không chuyển hướng. Hệ quả (đợt 0): khóa `localStorage` riêng `logos`, cache service worker riêng `logos-v1`; trang Dữ liệu của tôi nhận bản sao lưu của logos-zero |
| 10 | Nền tảng | ProperDocs 1.6.7 + Material 9.8.0, ghim bằng `uv.lock`; lối ra là bộ build Python tự viết (mục 11) | Zensical khi có bản 1.0; Astro + Starlight | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 11 | Tên site | Giữ "Logos Zero" tới đợt 5 (chữ trong bài chỉ sửa ở đợt 5) | Đổi ngay thành "Logos" ở tên site và manifest | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 12 | Cho Google lập chỉ mục logos | `noindex` (`extra.noindex: true`) tới khi logos khác logos-zero rõ rệt | Mở ngay | theo Đề xuất (chủ biên chốt 4/11/2026) |
| 13 | Kiểm schema của kho dữ kiện (đợt 2) | Thêm `jsonschema` (ghim trong `pyproject.toml`/`uv.lock`), vì schema kho có tham chiếu và điều kiện | Tự viết bộ kiểm cho tập con JSON Schema như `check_ledger.py`, không thêm gói | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 14 | Quý của bản lưu SEP (đợt 2) | `fall2026` (bản lưu mới nhất lúc làm đợt 2; đã mở thử được 5/11/2026); đổi quý chỉ khi kiểm lại nguồn ở đợt 5 hoặc Mở rộng | Luôn dùng quý mới nhất | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 15 | `description` trong front matter có vào mã băm không | Không, đúng đặc tả 5.6 (mã băm bỏ front matter); tiêu đề vẫn được băm qua dòng `# …` | Băm thêm `title`, `description` vào đơn vị `#_dau` | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 16 | Quy tắc đếm của `[[count:…]]` | Không đếm trang `he-thong` và trang sinh tự động, trừ trang triết gia (`lich-su` → 8, `triet-gia` → 59) | Đếm mọi trang theo `type` | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 17 | Năm trong trích dẫn tác giả–năm ("Bourget & Chalmers 2023") ở `lint_volatile` | Không tính: là năm xuất bản, không có hạn dùng | Tính, như báo cáo nền | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 18 | "thuyết định mệnh" trong bảng thuật ngữ | Ghi rõ trong `HUONG-DAN-VIET.md`: chỉ sai khi dịch *determinism*; đúng cho *fatalism* | Giữ "(sai)" chung | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 19 | Hai trang thiếu mục bắt buộc (`cong-cu/luan-cu-thep.md`: Bài tập, Tự kiểm tra; `doc/sartre-hien-sinh.md`: Đọc từng đoạn) | Bổ sung ở đợt 5 | Ghi ngoại lệ cho `lint_structure` | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 20 | Tiêu chí dời vào khối thời sự (đợt 3) | Chỉ dời đoạn đúng hay sai tùy lúc đọc (luật đang hiệu lực, số liệu đang đổi, AI hiện tại không gắn mốc); chỗ còn lại vào `data/style/volatile-allow.yml` có lý do (`co-moc-thoi-gian`, `vi-du-gia-dinh`, `trang-thai-hoc-thuat`, `chung-chung`, `su-kien-lich-su`), hết hiệu lực khi đổi chữ | Dời mọi chỗ `lint_volatile` bắt | theo Đề xuất (chủ biên chốt 5/11/2026; duyệt danh sách miễn 61 mục cùng ngày) |
| 21 | Font chữ (đợt 4) | Tự host Be Vietnam Pro và Noto Serif (woff2, OFL, tập Latin + tiếng Việt) trong `docs/assets/fonts/`; không gọi Google Fonts | Font hệ thống | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 22 | Chỉ mục tìm kiếm (đợt 4) | Bỏ bản sao không dấu khỏi `search_index.json`; bỏ dấu ở trình duyệt khi dựng chỉ mục và khi gõ; chỉ tải chỉ mục khi mở ô tìm | Pagefind (đợt 6); giữ nguyên | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 23 | Trang tác phẩm (đợt 4) | Một trang chỉ mục `tac-pham/index.md` sinh từ `works.yml` (tác phẩm đã biết tác giả, ghi "chưa kiểm chứng"); chưa có URL riêng cho từng tác phẩm tới sau đợt 5 | Mỗi tác phẩm một trang; dời sau đợt 5 | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 24 | Trang chủ mới (đợt 4) | Sắp xếp lại khối đang có thành cửa chính/phụ, thêm nút "Bắt đầu ở đây"; chữ mới chỉ là nhãn nút; chủ biên duyệt bằng ảnh chụp | Viết lại trang chủ; không đổi | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 25 | Nhịp push trong đợt 5 | Push mỗi đợt con, tag `v1.5.N` | Push một lần khi xong cả đợt 5 (luật 6) | **Push khi xong cả đợt 5** (chủ biên chọn 5/11/2026) |
| 26 | Kiểu ngoặc kép và mã băm | Mã băm bỏ qua kiểu ngoặc (`“ ”` như `"`, `‘ ’` như `'`); kiểu hiển thị chốt ở đợt 6, đổi không mở khóa | Thống nhất ngoặc cong hoặc ngoặc thẳng bằng script trước 5.1 | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 27 | Tên site (theo quyết định 11) | Đổi tên site thành "Logos", giữ nhãn "(bản dịch của Logos Zero)" | Đổi hết "Logos Zero" thành "Logos", kể cả nhãn bản dịch, bằng script trước 5.1; giữ chỗ nói tới site song song logos-zero | **Đổi hết thành "Logos"** (chủ biên chọn 5/11/2026) |
| 28 | Năm của tác phẩm (đợt 5.1) | Năm công bố lần đầu; tác phẩm cổ hoặc di cảo chưa rõ năm in thì năm soạn; khác biệt (năm soạn, bản sửa, bản dịch) ghi `year_note`; văn xuôi nói rõ đang dẫn một bản cụ thể thì giữ năm bản đó, còn lại sửa theo năm công bố | Năm soạn; giữ năm như bài | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 29 | Nghĩa của cạnh `influence` (đợt 5.1) | Người sau đọc và đáp lại người trước, tiếp thu hoặc phản bác; ghi định nghĩa ở Sơ đồ ảnh hưởng và schema | Chỉ tiếp thu; tách hai loại cạnh (đợt 6) | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 30 | Năm sinh mất cổ đại không có trong nguồn (đợt 5.1) | `years_label` theo nguồn ("hoạt động k. 500 TCN"); `born`/`died` giữ làm số ước lượng chỉ để xếp trục thời gian, có trường ghi rõ, không hiện như dữ kiện | Giữ nguyên, ghi nguồn yếu | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 31 | Nguồn Việt Nam yếu (đợt 5.1) | Bỏ khẳng định không tìm được nguồn nào; nhận báo chí, bảo tàng, tạp chí Việt Nam, ghi "nguồn yếu" trong bằng chứng để thay bằng ấn phẩm Viện Hán Nôm/Viện Văn học ở đợt 7 | Chờ nguồn sách, chưa đóng băng | theo Đề xuất (chủ biên chốt 5/11/2026) |
| 32 | Bài "Ăn thịt có sai không?" (`cau-hoi/dao-duc-ung-dung.md`): hai lập trường đều của Singer (động vật; nghèo đói), phần nghèo đói trùng ý với `cau-hoi/cuu-giup-ngheo-doi.md` | Ở 5.7 thêm một lập trường phản bác Singer về động vật ở dạng mạnh nhất (đủ ba nhãn Lập luận mạnh nhất, Phản bác chính, Cách đáp lại; có nguồn đã mở), thêm link sang `cuu-giup-ngheo-doi`; không bỏ chữ, không đổi `data-id` quiz. Tách hoặc viết lại bài để đợt 7 | Giữ nguyên tới đợt 7 | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 33 | Hồ sơ triết gia còn sống (đợt 7) | Được thêm khi người đó có tư tưởng được SEP hoặc IEP trình bày (vd. Singer, Chalmers, Nussbaum); hồ sơ chỉ nói tư tưởng và tác phẩm, năm sinh theo nguồn, không đời tư; trang hồ sơ ghi "người đang sống"; hồ sơ người còn sống có ngày cập nhật và hạn rà lại như khối thời sự (chủ biên thêm 20/11/2026) | Chỉ người đã mất | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 34 | Nguồn ở trang chặn công cụ kiểm (đợt 5.2): `ctext.org`, `cbetaonline`, trang có kiểm tra chống bot (DASH Harvard, thuvienphapluat, SSRN…) | Claim "URL mở được" coi là đạt khi nội dung đã đối chiếu ở một bản khác (Wikisource, CBETA cbdata, Crossref, bản ghi thư viện) và URL đúng mẫu đường dẫn của site; link hỏng do kiểm link hằng tuần (`links.yml`) phát hiện. Không vượt kiểm tra chống bot. Điều kiện (chủ biên thêm 20/11/2026): bằng chứng của mỗi URL như vậy có một URL dự phòng mở được; kiểm link hằng tuần phải chạy được | Thay mọi URL như thế bằng nguồn mở được; để `chua-kiem-duoc` | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 35 | Chi tiết phụ của dòng nguồn không kiểm được (đợt 5.2): số liên tục của tạp chí, trang cuối, trang trong sách, nhãn "phạm vi công cộng", "phụ lục", cơ quan chủ quản | Bỏ chi tiết đó khỏi dòng nguồn (giữ tác giả, tên, năm, nơi in, link đã kiểm); nhận định của bài mà không nguồn nào nói thì viết lại cho khớp nguồn | Giữ và để `chua-kiem-duoc` tới khi có bản in | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 36 | Mục Nguồn gộp nhiều tác phẩm, cùng một nguồn ghi khác nhau ở các trang (đợt 5.2, `verification/lech/sources.md`) | Mỗi mục Nguồn một tác phẩm: mục gộp tác phẩm khác nhau thì tách; nhiều URL của cùng một tác phẩm (bản điện tử khác, bản dịch, nguyên văn, các chương/thiên) giữ trong một mục và ghi vào `NHIEU_URL_DUYET` của `tools/kb_sources.py`. Cùng một nguồn ghi giống nhau ở mọi trang và hồ sơ; vị trí và chú thích riêng của trang đặt ở câu ngắn trước danh sách Nguồn (hồ sơ: bỏ). Link http:// đổi sang https:// khi site chạy https; còn lại ghi vào `HTTP_DUYET` kèm lý do. Sách in cùng tên nhưng khác quy ước ghi giữa trang và hồ sơ (năm sau tên tác giả hay ở cuối) để 5.9 | Giữ mục gộp, ghi mỗi trang một kiểu | theo Đề xuất (Claude chọn tạm, **chủ biên duyệt 20/11/2026**) |
| 37 | Hướng thiết kế đợt 6 | Chỉnh trên nền hiện có: giữ màu, font, Material; làm lại nhịp chữ, bố cục bài, trang chủ | Nhận diện mới hoàn toàn; chỉ việc kỹ thuật | **Chỉnh trên nền hiện có** (chủ biên chọn 20/11/2026) |
| 38 | Tìm kiếm tiếng Việt (đợt 6) | Sửa worker của site: từ ≤ 2 chữ cái không thêm `*` | Pagefind | **Sửa worker** (chủ biên chọn 20/11/2026) |
| 39 | Kiểu ngoặc kép hiển thị (quyết định 26) | Ngoặc cong `“ ”` khi hiển thị, đổi lúc build bằng hook; nguồn không đổi | Giữ như bài | **Ngoặc cong** (chủ biên chọn 20/11/2026) |

## 4. Kiến trúc

Kho dữ kiện cấp dữ kiện cho cả Lõi lẫn Mở rộng; Mở rộng chỉ link vào Lõi; sổ kiểm chứng và CI canh để Lõi không đổi ngoài ý muốn. Tầng là thuộc tính (front matter và `content.yml`), không phải thư mục: URL giữ nguyên.

| Thành phần | Vị trí | Nội dung | Đợt tạo |
|---|---|---|---|
| Sổ đăng ký nội dung | `content.yml` + `schema/content.schema.json` | mọi trang và file dữ liệu: loại, tầng, khối; nguồn sinh nav, chỉ mục, số đếm | 0 |
| Thư viện công cụ | `tools/lz/` | đọc `content.yml`, tách đơn vị, chuẩn hóa, băm | 1 |
| Sổ kiểm chứng | `verification/ledger.json` + `verification/evidence/` | mỗi đơn vị một dòng: mã băm, trạng thái, ngày, người kiểm, file bằng chứng | 1 |
| Hook shortcode | `hooks/kb.py` | in số đếm, số liệu, dữ kiện từ dữ liệu lúc build; khóa sai thì build dừng | 1 (khung), 2 (dữ liệu) |
| Kho dữ kiện | `data/kb/people.yml`, `works.yml`, `quotes.yml`, `events.yml`, `sources.yml`, `philpapers-2020.json` | bản ghi có `evidence` và `verified` | 2 |
| Hồ sơ triết gia | `data/people/<id>.yml` | phần văn của 59 hồ sơ, chuyển khỏi `tools/philosophers.py` | 2 |
| Khối thời sự | `data/thoi-su/<id>.md` | `page`, `updated_to`, `review_by`, `sources`; chèn vào trang bằng dấu giữ chỗ | 3 |
| Chính sách thuật ngữ | `data/style/terms-policy.yml` | bảng thuật ngữ bắt buộc của `HUONG-DAN-VIET.md` ở dạng máy đọc | 1 |

## 5. Mô hình nội dung

### 5.1 Loại trang và mục bắt buộc

Các mục bắt buộc lấy đúng cấu trúc đang có, nên không phải viết lại bài nào.

| Loại (`type`) | Thư mục | Mục H2 bắt buộc |
|---|---|---|
| `cau-hoi` | `docs/cau-hoi/` | Thí nghiệm tư duy · Câu hỏi thật sự là gì? · Các lập trường chính · Giới triết học ngày nay nghĩ gì · Liên hệ đời sống · Tự kiểm tra · Tự viết · Nguồn; thêm hộp `!!! summary "Tóm tắt 5 phút"`. "Đọc văn bản gốc" tùy chọn (39/57 bài có) |
| `cong-cu` | `docs/cong-cu/` | Bài tập · Tự kiểm tra · Đi tiếp · Nguồn |
| `lich-su` | `docs/lich-su/` | Đọc tiếp · Nguồn |
| `doc` | `docs/doc/` | Bối cảnh · Đọc từng đoạn · Tái dựng lập luận · Phản bác · Hiểu lầm thường gặp · Tự kiểm tra · Câu hỏi để tự viết · Đọc tiếp · Nguồn |
| `triet-gia` | `docs/triet-gia/` (sinh) | sinh từ dữ liệu |
| `tac-pham` (mới, đợt 4) | `docs/tac-pham/` (sinh) | sinh từ kho |
| `he-thong` | `docs/them/`, `docs/luyen-tap/`, các `index.md`, trang chủ | không bắt buộc |

### 5.2 Front matter mới

Giữ `title`, `description`, `skill`, `updated` (nghĩa: lần sửa cuối, không phải trạng thái kiểm chứng). Thêm:

- `tier`: `loi` | `mo-rong` | `he-thong`
- `block`: khóa khối (5.3)
- `work`: khóa tác phẩm trong kho (chỉ trang `doc`, từ đợt 2)
- `added`, `related`: chỉ bài `mo-rong`

`content.yml` là nơi khai báo chính; front matter được kiểm cho khớp với nó.

### 5.3 Khóa khối (`block`)

`bat-dau`, `cong-cu`, `tri-thuc`, `tam-tri`, `tu-do`, `dao-duc`, `luan-ly-ung-dung`, `chinh-tri`, `my-hoc`, `ton-giao`, `sieu-hinh`, `y-nghia`, `viet-nam`, `lich-su`, `triet-gia`, `van-ban`, `thuat-ngu`, `luyen-tap`.
Bài `cau-hoi` lấy khối theo nhóm trong `nav` của `mkdocs.yml` (11 chủ đề).

### 5.4 Bản ghi kho dữ kiện

Mọi bản ghi có thêm `evidence` (danh sách link đã mở) và `verified` (`{date, by}` hoặc `null`). Schema viết bằng JSON Schema trong `schema/`.

| Bản ghi | File | Trường chính | Ví dụ khóa |
|---|---|---|---|
| Người | `data/kb/people.yml` | tên Việt, tên gốc, sinh, mất (kèm độ chính xác "k."), trường phái, tóm tắt một dòng | `kant` |
| Tác phẩm | `data/kb/works.yml` | tác giả, tên Việt, tên gốc, năm và ghi chú bản in, bản quyền, link văn bản | `kant.phe-phan-ly-tinh-thuan-tuy` |
| Trích dẫn | `data/kb/quotes.yml` | tác phẩm, vị trí (38a, §IV, 2A6), nguyên văn, bản dịch nguồn, bản dịch của Logos Zero, giấy phép | `platon.bien-ho.38a` |
| Sự kiện | `data/kb/events.yml` | ngày hoặc năm, mô tả ngắn | `dai-viet.nguyen-mong-1258` |
| Số liệu PhilPapers | `data/kb/philpapers-2020.json` | câu hỏi, lựa chọn, % bao gồm, n, câu chính hay bổ sung | `free-will.compatibilism` |
| Nguồn | `data/kb/sources.yml` | loại (SEP, IEP, sách, DOI), tác giả, tiêu đề, link bản lưu, ngày truy cập | `sep.kant.fall2026` |
| Thuật ngữ | `docs/assets/data/terms.json` (giữ chỗ cũ) | như hiện tại | `tri-thuc-luan` |

### 5.5 Đơn vị và ID

- Mỗi mục H2 mang ID cố định viết tay: `## Các lập trường chính {#cac-lap-truong-chinh}`. ID lấy đúng anchor đang được build ra hôm nay, để link cũ không gãy; sau đó đổi tiêu đề không đổi ID.
- Khóa đơn vị: `<đường dẫn trong docs>#<id>`, ví dụ `cau-hoi/tri-thuc.md#cac-lap-truong-chinh`. Phần trước H2 đầu tiên là đơn vị `#_dau`.
- Bản ghi dữ liệu: `<loại>/<khóa>`, ví dụ `people/kant`, `quotes/platon.bien-ho.38a`, `quiz/knowledge-1`.

### 5.6 Chuẩn hóa và băm

1. Lấy văn bản nguồn của đơn vị (từ dòng H2 tới trước H2 kế tiếp).
2. Bỏ: front matter; khối giữa `<!-- gen:… -->` và `<!-- /gen:… -->`, giữa `<!-- fig:… -->` và `<!-- /fig:… -->`; thuộc tính `{#…}` và `{: …}`; comment HTML.
3. Chuyển Markdown thành chuỗi: giữ chữ hiển thị (cả tiêu đề admonition trong ngoặc kép); giữ đích link ở dạng `⟨đích⟩` ngay sau chữ của link; giữ shortcode nguyên dạng; bỏ dấu nhấn, ký hiệu đầu dòng, tên loại admonition; ô bảng giữ nội dung, ngăn bằng ` | `. JSON của quiz được parse rồi in lại có sắp xếp khóa.
4. Unicode NFC; mọi chuỗi khoảng trắng thành một dấu cách; cắt hai đầu. Khi băm, ngoặc cong `“ ”` `‘ ’` được coi như ngoặc thẳng `"` `'` (quyết định 26).
5. `sha256` của chuỗi UTF-8, ghi `sha256:<hex>`.

Hệ quả cần có (viết kiểm thử cho từng điều): đổi `*nhấn*` thành `**nhấn**`, đổi `"…"` thành `“…”`, đổi `!!! note` thành `!!! tip`, đổi nền tảng render → mã băm không đổi; sửa một chữ, một năm, một link → mã băm đổi.

## 6. Các đợt

Ngày là đề xuất; thứ tự và cổng thì giữ.

| Đợt | Việc chính | Nội dung cũ | Cổng hoàn thành |
|---|---|---|---|
| 0 · Chốt mốc | Nhập nguyên trạng logos-zero, tag `v1.0-moc`; ProperDocs + Material 9.8.0 + uv; cấu hình site song song; chốt quyết định; `content.yml` + kiểm tra đăng ký; báo cáo nền | Không đổi chữ nào | Chủ biên duyệt `content.yml`; CI xanh |
| 1 · Công cụ nền | `tools/lz/`; ID cố định cho 888 mục H2; sổ kiểm chứng rỗng + `check_ledger.py`; `changed_units.py` + mẫu PR; linter ở chế độ cảnh báo; khung hook shortcode; công cụ kiểm tra tương đương | Chỉ thêm `{#id}` | Tương đương 100%; linter in báo cáo nền; CI xanh |
| 2 · Kho dữ kiện | `data/kb/*`; 59 hồ sơ sang `data/people/*.yml`; generator đọc YAML; link SEP sang bản lưu theo quý | Rút dữ kiện bằng script; chưa sửa chỗ sai, chỉ ghi danh sách lệch | 100% bản ghi qua schema; 59 trang triết gia giống từng byte; danh sách lệch lưu cho đợt 5 |
| 3 · Tách thời sự và số đếm | 139 chỗ có hạn dùng ở 66 trang thành `data/thoi-su/*.md`; số đếm gõ tay thành shortcode; bảng PhilPapers ở 35 bài sinh từ JSON | Câu chữ giữ nguyên, chỉ dời chỗ | `lint_volatile` = 0 trong Lõi; tương đương 100% |
| 4 · Giao diện tối thiểu | Dải thông tin đầu trang, hộp thời sự, nhãn Mới, thẻ di chuột, trang tác phẩm, trang Tình trạng kiểm chứng, nav sinh từ `content.yml`, trang chủ mới (override + CSS, không đổi theme). Sửa các điểm đo ngày 3/11/2026 (`ban-giao/viec-cho.md`): khả năng tiếp cận, khối Tóm tắt 5 phút trên điện thoại, nút In, chỉ mục tìm kiếm, font; thêm kiểm thử axe bằng Playwright trên trình duyệt thật | Không đổi; chỉ thêm phần sinh | 250 kiểm thử trình duyệt + axe (jsdom và trình duyệt thật) xanh; chủ biên duyệt ảnh chụp 10 trang mẫu |
| 5 · Kiểm chứng và đóng băng Lõi | 8 đợt con (6.1); mỗi đợt con: kiểm, ghi bằng chứng, kiểm mẫu 10%, đóng băng | Sửa đúng chỗ sai, mỗi chỗ có bằng chứng | 100% đơn vị Lõi đóng băng; lỗi nghiêm trọng trong mẫu ≤ 2% mỗi đợt con |
| 6 · Thiết kế lại giao diện | Thiết kế lại trên nền hiện tại (CSS, override, trang chủ, hình). Chỉ đổi trình render khi một điều kiện kích hoạt ở mục 11 xảy ra: dựng trên nhánh riêng, chuyển cú pháp bằng script, nhúng 18 file JavaScript, chuyển kiểm thử | Giữ nguyên | Tương đương 100%; mọi URL còn mở được; tiến độ người đọc giữ nguyên; không đơn vị nào bị mở khóa |
| 7 · Vận hành Mở rộng | PR nhỏ theo 5 ngăn; rà khối thời sự đến hạn; thăng hạng mỗi quý; báo lỗi xử lý trong 7 ngày | — | Mỗi PR CI xanh; không PR Mở rộng nào sửa file Lõi |

### 6.1 Các đợt con của đợt 5

Kiểm kho trước, để các bài sau chỉ còn phải kiểm phần diễn giải.

| Đợt con | Phạm vi | Quy mô | Thời gian |
|---|---|---|---|
| 5.1 | Kho: người và tác phẩm | 59 người có hồ sơ và người khác được nhắc; khoảng 250 tác phẩm có năm | 4–10/1 |
| 5.2 | Kho: trích dẫn, sự kiện, PhilPapers | 157 khối trích dẫn; số liệu ở 35 bài | 11–17/1 |
| 5.3 | Hồ sơ triết gia và thuật ngữ | 59 hồ sơ, 249 thuật ngữ | 18–24/1 |
| 5.4 | Văn bản gốc | 19 hướng dẫn, 171 mục | 25–31/1 |
| — | Tết, dự phòng; rà soát nền tảng 1/2 (mục 11) | — | 1–7/2 |
| 5.5 | Công cụ tư duy + dữ liệu luyện tập | 15 bài (156 mục); 100 ngụy biện, 30 đoạn lập luận, 20 bài logic, 8 thí nghiệm | 8–14/2 |
| 5.6 | Lịch sử và Bắt đầu | 10 bài, khoảng 70 mục | 15–21/2 |
| 5.7 | Câu hỏi lớn I: Tri thức, Tâm trí, Tự do, Đạo đức, Luân lý ứng dụng | 26 bài, khoảng 225 mục | 22/2–3/3 |
| 5.8 | Câu hỏi lớn II: Chính trị, Mỹ học, Tôn giáo, Siêu hình, Ý nghĩa, Việt Nam | 31 bài, khoảng 270 mục | 4–14/3 |

## 7. Kiểm chứng (đợt 5 và mọi phần Mở rộng)

1. **Trích dữ kiện** từ đơn vị, đối chiếu kho; dữ kiện chưa có thành bản ghi chờ kiểm.
2. **Kiểm kho** một lần cho cả site: mỗi bản ghi có ít nhất một nguồn ổn định (SEP bản lưu theo quý, IEP, Gutenberg/Wikisource có số hiệu, DOI). Trích dẫn so từng chữ và ghi vị trí.
3. **Kiểm ngữ nghĩa theo mục**, checklist năm câu: đúng nguồn? phiên bản mạnh nhất? có phản bác và cách đáp lại? trung lập? đúng thuật ngữ? Mỗi phán đoán có bằng chứng (link + vài chữ trích). Agent kiểm độc lập với agent làm: `ban-giao/kiem-chung.md`.
4. **Kiểm mẫu**: mỗi đợt con lấy ngẫu nhiên 10% đơn vị đã kiểm cho người hoặc agent thứ hai. Lỗi nghiêm trọng trên 2% mẫu thì kiểm lại cả đợt con.
5. **Đóng băng**: ghi vào sổ (mã băm theo 5.6, ngày, người kiểm, file bằng chứng). Mã băm bỏ qua `updated` và các khối sinh.
6. **Mở lại có kiểm soát**: lệch mã băm thì CI báo; PR phải có nhãn `doi-loi` (merge thẳng thì commit có `[doi-loi]` trong message) và bằng chứng mới; chỉ đơn vị đó được kiểm lại.
7. **Báo lỗi từ người đọc** (nút "Báo lỗi trang này", nhãn `bao-loi`): khoanh tới đơn vị hoặc bản ghi, sửa, cập nhật sổ. Lỗi ở một bản ghi kho thì mọi trang dùng nó đúng theo.

"Lỗi nghiêm trọng" = sai năm, sai người, sai trích dẫn, sai số liệu, quiz sai đáp án, hoặc trình bày sai một lập trường.

## 8. Kiểm tra tự động (đích đến)

| Công cụ | Chặn điều gì | Đợt |
|---|---|---|
| `tools/content_registry.py --check` | trang có trong `docs/` mà thiếu trong `content.yml`, hoặc ngược lại; front matter lệch sổ đăng ký | 0 |
| `tools/check_ledger.py --check` | đơn vị `frozen` đổi mã băm mà PR không có nhãn `doi-loi` | 1 |
| `tools/lint_terms.py` | sai thuật ngữ bắt buộc; "Plato" trong văn xuôi | 1 (cảnh báo), 5.9 (chặn) |
| `tools/lint_volatile.py` | năm 2022+, văn bản luật, "hiện nay/gần đây/tính đến" trong Lõi ngoài khối thời sự; khối thời sự quá hạn | 1 (cảnh báo), 3 (chặn) |
| `tools/lint_structure.py` | thiếu mục bắt buộc theo loại trang (5.1); nhãn độ chắc chắn ngoài bài có chú giải | 1 (cảnh báo), 5.9 (chặn) |
| `tools/changed_units.py` | không chặn: bình luận PR liệt kê đơn vị đổi và checklist | 1 |
| `tools/parity.py` | văn bản hiển thị lệch sau thay đổi cơ học | 1 |
| `tools/lint_facts.py` | năm và tên tác phẩm trong văn xuôi lệch kho | 2 (cảnh báo), 5.9 (chặn) |
| `tools/lint_quotes.py` | khối trích không khớp bản ghi trích dẫn | 2 (cảnh báo), 5.9 (chặn) |
| `tools/lint_so_lieu.py` | số % PhilPapers gõ tay ngoài `[[pp:…]]`; số trong quiz và dữ liệu lệch kho (rà soát 9/11) | 5 (cảnh báo), 5.9 (chặn) |
| `tools/lint_lien_ket.py` | bài nhắc triết gia đã có hồ sơ mà không link (rà soát 9/11) | 5 (cảnh báo), 5.9 (chặn) |
| `hooks/kb.py` | shortcode trỏ tới khóa không tồn tại (build dừng) | 1–3 |
| kiểm thử axe trên trình duyệt thật (Playwright) | lỗi tiếp cận mà jsdom không thấy: tương phản, link chỉ khác bằng màu, vùng chạm | 4 |

Linter mới chạy ở chế độ cảnh báo hai tuần rồi mới chuyển sang chặn.

## 9. Quy trình PR và vai trò

1. Issue "Đợt N" ghi phạm vi, cổng, danh sách việc.
2. Nhánh `dot-N-<ten>`; mỗi nhánh tối đa 3 đơn vị nội dung, hoặc đúng một thay đổi cơ học. Không mở PR: xong việc thì merge vào `main` trên máy; push `main` khi xong cả đợt (chủ biên chốt 5/11/2026).
3. CI: schema → generator `--check` → linter → sổ kiểm chứng → `properdocs build --strict` → kiểm thử; `changed_units.py` bình luận PR.
4. Kiểm: cơ học thì kiểm tra tương đương; nội dung thì agent kiểm độc lập, bằng chứng vào `verification/evidence/`.
5. Agent merge vào `main` trên máy; chủ biên đọc báo cáo cuối phiên, nhật ký và mẫu 10%.
6. Đóng đợt: tag (`v1.1`, `v1.2`…), mục Cập nhật sinh từ các PR, cập nhật bảng Trạng thái ở đầu file này.

| Vai trò | Ai | Việc |
|---|---|---|
| Chủ biên | mtuann | chọn quyết định, duyệt cổng và mẫu |
| Agent làm | một phiên agent | script, chuyển nội dung, sửa theo báo cáo; merge vào `main` trên máy sau mỗi việc, push khi xong đợt |
| Agent kiểm | phiên agent khác | tra nguồn, ghi bằng chứng; không tự sửa bài |
| CI | GitHub Actions | mọi thứ máy kiểm được; chặn merge khi đỏ |

## 10. Tái sử dụng nội dung cũ

| Hiện có | Đích đến | Cách chuyển | Kiểm |
|---|---|---|---|
| 57 Câu hỏi lớn, 15 Công cụ, 8 Lịch sử, 19 hướng dẫn đọc, 2 bài Bắt đầu | giữ đường dẫn trong `docs/` | script thêm ID mục, dời khối thời sự, thay số gõ tay bằng shortcode | tương đương văn bản |
| `philosophers.json` + `CONTENT` trong `tools/philosophers.py` | `data/kb/people.yml` + `data/people/<id>.yml` | script một–một | 59 trang giống từng byte |
| `tools/philpapers-2020.md` (87/100 câu) | `data/kb/philpapers-2020.json`; `.md` sinh lại cho người đọc | script; bổ sung 13 câu còn thiếu | đối chiếu 100 câu với trang kết quả chính thức |
| 157 khối `!!! quote` | `data/kb/quotes.yml` + shortcode | script tách, giữ nguyên chữ | `lint_quotes` |
| 628 mục Nguồn | `data/kb/sources.yml` + danh sách Nguồn sinh lại | script gộp trùng; SEP sang bản lưu theo quý | kiểm tra link |
| 394 chỗ "*Tác phẩm* (năm)" | `data/kb/works.yml` | script gom theo tên, báo chỗ lệch năm | `lint_facts` |
| `terms.json` (249) | giữ nguyên | thêm `verified` | đợt con 5.3 |
| 428 câu quiz trong trang | giữ trong trang, giữ `data-id` | — | đợt 5, theo trang |
| `fallacies.json`, `thi-nghiem.json`, `lap-luan.json`, `logic.json` | giữ đường dẫn | thêm schema | kiểm thử JS, đợt con 5.5 |
| Bảng thuật ngữ trong `HUONG-DAN-VIET.md` | `data/style/terms-policy.yml` | script | `lint_terms` chạy được |
| 18 file JavaScript, `oz.css`, 9 generator, kiểm thử | giữ; chỉ chuyển khi kích hoạt lối ra (mục 11) | — | 250 kiểm thử trình duyệt |

## 11. Công nghệ

Nguyên tắc: phần có giá trị (nội dung, kho dữ kiện, sổ kiểm chứng) nằm trên lớp ít thay đổi nhất: Markdown theo cú pháp Python-Markdown, YAML/JSON, Python, JavaScript thuần, HTML tĩnh. Trình render là lớp vỏ mỏng, thay được trong một đợt mà không mở khóa Lõi, vì mã băm tính trên văn bản chuẩn hóa (5.6) và kiểm tra tương đương bảo đảm chữ không đổi.

- **Đang dùng (từ đợt 0, quyết định 10)**: ProperDocs 1.6.7 (bản kế tục MkDocs 1.x, do người bảo trì cuối của MkDocs lập 3/2026) + Material for MkDocs 9.8.0 (bản cuối, hết vòng đời 5/5/2027), Markdown 3.11, pymdown-extensions 12.2, Python 3.13; ghim bằng `pyproject.toml` + `uv.lock`. Đo ngày 3/11/2026: HTML giống hệt bản MkDocs 1.6.1 + Material 9.7.7, chỉ khác tên file CSS/JS của theme.
- **Không nâng phiên bản ngoài kế hoạch.** Mỗi lần nâng là một PR riêng, qua kiểm tra tương đương.
- **Lối ra chính**: bộ build nhỏ tự viết trên Python-Markdown + Jinja2 (5 gói; không bản nào phá vỡ tương thích trong 4 năm tính đến 11/2026). Giữ nguyên cú pháp nội dung; dùng lại `hooks/slugs.py`, `hooks/search_vi.py`, `content.yml` làm nav, 18 file JavaScript. Chỉ kích hoạt khi: (a) bản ghim không cài được nữa, hoặc có lỗi bảo mật không vá được; (b) cần tính năng bản ghim không làm được; (c) ProperDocs ngừng bảo trì và `mkdocs==1.6.1` cũng không chạy được.
- **Rà soát hằng năm (tháng 2)**: chạy lại bộ thử ngày 3/11/2026 với Zensical (anchor không dấu, tìm kiếm không dấu, tương đương văn bản). Kết quả với Zensical 0.0.74: build được 181 trang nhưng hai hook không chạy; 1.030/3.146 anchor đổi vì mất chữ "đ"; tìm "dao duc" ra 0 kết quả. Khi Zensical có bản 1.0 và module API Python đủ chạy hai hook, đó là đường chuyển rẻ nhất vì đọc thẳng `mkdocs.yml`.
- **Astro + Starlight**: không chọn. Astro ra 6 bản major trong 4 năm, Starlight còn 0.x (42 bản 0.x), 278 gói npm, và phải chuyển cú pháp 180 trang. Chỉ xem lại nếu muốn giao diện tương tác phong phú và chấp nhận 1–2 đợt nâng cấp mỗi năm.
- **Tìm kiếm**: Pagefind 1.x (ổn định từ 9/2023) dùng được với mọi trình render và chỉ tải phần chỉ mục cần cho mỗi truy vấn; nó tự bỏ dấu thanh nhưng không đổi "đ" thành "d", cần vá (đã thử ngày 3/11/2026).

## 12. Rủi ro

| Rủi ro | Dấu hiệu | Cách giảm |
|---|---|---|
| Phạm vi phình ra | issue nhãn `cho` tăng nhanh; PR có trang mới trước đợt 7 | CI từ chối trang mới khi chưa mở đợt 7 |
| Script làm sai nội dung | kiểm tra tương đương báo lệch | không merge khi lệch; script có kiểm thử, chạy thử 3 trang trước |
| Mã băm báo động giả | nhiều đơn vị mở khóa sau đổi định dạng | băm trên nội dung chuẩn hóa (5.6) |
| Agent kiểm sai hoặc bịa nguồn | mẫu 10% lỗi > 2% | agent kiểm độc lập; bắt buộc link + trích; chủ biên xem mẫu |
| Material hết vòng đời (5/5/2027) | công bố lỗi bảo mật ở JS của Material; bản ghim không cài được trên Python mới | site tĩnh nên rủi ro thấp; ghim Python và `uv.lock`; kích hoạt lối ra (mục 11) |
| ProperDocs ngừng bảo trì | lỗi chặn không có bản sửa | quay về `mkdocs==1.6.1` (HTML giống hệt) hoặc kích hoạt lối ra |
| Hai site cùng origin đè dữ liệu của nhau | — | khóa `localStorage` và tiền tố cache riêng (đợt 0). Còn lại: service worker của logos-zero xóa mọi cache khác `oz-v1` mỗi khi nó cập nhật, kể cả cache của logos; chỉ mất bản đọc ngoại tuyến, sửa một dòng ở logos-zero nếu chủ biên muốn |
| Kiểm thử phụ thuộc ngày chạy | CI đỏ dù không ai sửa gì | dữ liệu mẫu tính theo ngày chạy (đã sửa `ke-hoach.test.js` ở đợt 0) |
| Phiên bị ngắt giữa chừng | agent dừng không ghi kết quả | nhật ký sau từng đơn vị; đợt con nhỏ |
