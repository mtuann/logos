# Danh sách lệch: nguồn

Sinh bằng `python tools/kb_sources.py`. Đầu vào cho đợt 5: không sửa trong đợt 2.

- 960 mục Nguồn (trang viết tay + hồ sơ) → 684 bản ghi.
- Theo loại: cbeta 3, ctext 24, doi 59, gutenberg 61, iep 37, khac 87, sach 182, sep 187, wikisource 44.
- 221 mục không có URL (sách in, hoặc thiếu link).

## Cùng một nguồn, chữ khác nhau (0)

Cùng URL đầu nhưng các trang ghi tác giả, tiêu đề, năm khác nhau: thống nhất ở đợt 5 (cách ghi giống nhau ở mọi trang và hồ sơ; vị trí và chú thích riêng của trang đặt ở câu trước danh sách Nguồn, quyết định 36).

Không còn mục mở.

## Sách có thể trùng (0)

Sách in không có URL, ghi gần giống nhau ở các trang (khác chương, trang, nhà xuất bản): xem có phải một nguồn.

Không còn mục mở.

## Mục có nhiều URL, chưa duyệt (0)

Bản ghi lấy URL đầu; các URL sau ghi ở `also`. Mục gộp nhiều tác phẩm thì tách mỗi tác phẩm một mục; mục mà mọi URL thuộc cùng một tác phẩm thì ghi vào `NHIEU_URL_DUYET` trong `tools/kb_sources.py` (quyết định 36).

Không còn mục mở.

## Mục có nhiều URL, đã duyệt: cùng một tác phẩm (67 mục, 12 bản ghi)

- `ctext.mengzi-gong-sun-chou-i`: *Mạnh Tử*: ba thiên 2A, 3B, 6A (dùng ở `cau-hoi/ban-tinh-con-nguoi.md#nguon`, `doc/manh-tu-tinh-thien.md#nguon`)
- `ctext.mengzi-teng-wen-gong-i`: *Mạnh Tử*: hai thiên 3A, 3B (dùng ở `doc/mac-tu-kiem-ai.md#nguon`)
- `ctext.mozi-universal-love-i`: *Mặc Tử*: năm thiên (dùng ở `doc/mac-tu-kiem-ai.md#nguon`)
- `doi.10-3998-phimp-2109`: bài báo khảo sát PhilPapers 2020 và trang kết quả của chính khảo sát (dùng ở `bat-dau/index.md#nguon`, `cau-hoi/ai-nen-cai-tri.md#nguon`, `cau-hoi/an-tu-hinh.md#nguon`, `cau-hoi/ban-nga-thoi-gian.md#nguon`, `cau-hoi/ban-tinh-con-nguoi.md#nguon`, `cau-hoi/bat-dong-tri-thuc.md#nguon`, `cau-hoi/bien-gioi-di-cu.md#nguon`, `cau-hoi/binh-dang.md#nguon`, `cau-hoi/cai-ac.md#nguon`, `cau-hoi/cai-chet.md#nguon`, `cau-hoi/cai-dep.md#nguon`, `cau-hoi/cai-gi-ton-tai.md#nguon`, `cau-hoi/cai-toi.md#nguon`, `cau-hoi/chan-ly.md#nguon`, `cau-hoi/chien-tranh-chinh-dang.md#nguon`, `cau-hoi/cong-ly.md#nguon`, `cau-hoi/cong-nghe-ai.md#nguon`, `cau-hoi/cuu-giup-ngheo-doi.md#nguon`, `cau-hoi/dan-chu.md#nguon`, `cau-hoi/dao-duc-hanh-dong.md#nguon`, `cau-hoi/dao-duc-moi-truong.md#nguon`, `cau-hoi/dao-duc-ung-dung.md#nguon`, `cau-hoi/dinh-menh.md#nguon`, `cau-hoi/duc-tin-ly-tri.md#nguon`, `cau-hoi/duc-tri.md#nguon`, `cau-hoi/hanh-phuc.md#nguon`, `cau-hoi/hien-tang.md#nguon`, `cau-hoi/khi-hau-trach-nhiem.md#nguon`, `cau-hoi/linh-hon.md#nguon`, `cau-hoi/luan-chung-ton-giao.md#nguon`, `cau-hoi/mo-phong.md#nguon`, `cau-hoi/nghe-thuat.md#nguon`, `cau-hoi/nhan-qua-ban-chat.md#nguon`, `cau-hoi/noi-doi.md#nguon`, `cau-hoi/nu-quyen.md#nguon`, `cau-hoi/pha-thai.md#nguon`, `cau-hoi/pho-quat.md#nguon`, `cau-hoi/quyen-rieng-tu-so.md#nguon`, `cau-hoi/sieu-dao-duc.md#nguon`, `cau-hoi/tai-san-rieng.md#nguon`, `cau-hoi/tam-tri-va-ai.md#nguon`, `cau-hoi/thoi-gian.md#nguon`, `cau-hoi/tinh-yeu.md#nguon`, `cau-hoi/trach-nhiem.md#nguon`, `cau-hoi/tri-thuc.md#nguon`, `cau-hoi/tu-do-ngon-luan.md#nguon`, `cau-hoi/tu-do-y-chi.md#nguon`, `cau-hoi/van-de-tam-tri.md#nguon`, `cau-hoi/viet-hien-dai.md#nguon`, `cau-hoi/vu-tru-khoi-dau.md#nguon`, `cau-hoi/y-nghia-song.md#nguon`, `doc/hume-nhan-qua.md#nguon`, `doc/russell-gia-tri.md#nguon`)
- `web.archive-org.details-bim-eighteenth-century-a-treatise-of-human`: *A Treatise of Human Nature* của Hume: ba quyển của ấn bản đầu (dùng ở `cau-hoi/cai-toi.md#nguon`, `cau-hoi/nhan-qua-ban-chat.md#nguon`)
- `web.archive-org.details-cu31924029021612`: bài của Kant (1797): bản dịch Abbott và nguyên văn Akademie-Ausgabe (dùng ở `cau-hoi/noi-doi.md#nguon`)
- `wikisource.de.beantwortung-der-frage-was-ist-aufklarung`: bài của Kant (1784): bản in gốc và Akademie-Ausgabe (dùng ở `doc/kant-khai-sang.md#nguon`)
- `wikisource.en.meditations-on-first-philosophy-meditation-i`: *Meditations* của Descartes: bản dịch Veitch và Molyneux (dùng ở `cau-hoi/tri-thuc.md#nguon`)
- `wikisource.en.the-problems-of-philosophy-chapter-15`: *The Problems of Philosophy*: Wikisource và Gutenberg (dùng ở `doc/russell-gia-tri.md#nguon`)
- `wikisource.vi.binh-ngo-dai-cao-tran-trong-kim-dich`: *Bình Ngô đại cáo*: hai bản dịch (Trần Trọng Kim; Mạc Bảo Thần) (dùng ở `cau-hoi/nho-giao-viet.md#nguon`, `doc/nguyen-trai-binh-ngo.md#nguon`)
- `wikisource.vi.cu-tran-lac-dao-phu-de-ngu-hoi`: *Cư trần lạc đạo phú*: hội 5 và bài kệ kết (dùng ở `doc/tho-van-ly-tran.md#nguon`)
- `wikisource.zh.d8922572ee`: *Đại Việt sử ký toàn thư*: Bản kỷ quyển 10 và 11 (dùng ở `doc/nguyen-trai-binh-ngo.md#nguon`)

## Link http:// (0)

Không còn mục mở.

## Link http:// đã duyệt (1)

- `cau-hoi/nghe-thuat.md#nguon`: <http://news.bbc.co.uk/2/hi/entertainment/4059997.stm> — trang lưu của BBC News chỉ chạy http (mở bằng https bị chuyển về http)
