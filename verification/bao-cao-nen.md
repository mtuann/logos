# Báo cáo nền

Sinh bằng `tools/baseline_report.py` trên commit đầu của đợt 0 (nội dung nguyên trạng từ `logos-zero@ecb2bb8`).
Chạy lại cho cùng kết quả. Không sửa tay; không chạy lại ở các đợt sau: đây là số nền để so.

Phạm vi chính: **Lõi viết tay** (`tier: loi`, `generated: false` trong `content.yml`): 100 bài cần kiểm bằng tay. Trang sinh tự động chỉ được đếm số trang, số mục H2 và dung lượng; hồ sơ triết gia (văn nằm trong `tools/philosophers.py`) có cột riêng ở mục 4. Số đếm gõ tay (mục 3) quét mọi trang viết tay.

## Đối chiếu với số đo ngày 23/10/2026

| Chỉ số | 23/10/2026 | Lõi viết tay | Lõi viết tay + trang triết gia | Lệch (cột khớp) | Ghi chú |
|---|---:|---:|---:|---:|---|
| dấu thời gian | 139 | 128 | — | -7,9% |  |
| trang có dấu thời gian | 66 | 67 | — | +1,5% |  |
| chỗ “*Tác phẩm* (năm)” | 394 | 159 | 415 | +5,3% | số ngày 23/10 tính cả trang triết gia |
| khối `!!! quote` | 157 | 108 | 156 | -0,6% | số ngày 23/10 tính cả trang triết gia |
| mục trong danh sách Nguồn | 628 | 628 | 898 | +0,0% |  |
| bài có bảng PhilPapers | 35 | 39 | — | +11,4% | 4 bài ghi số kèm dấu % và thêm cột “Chỉ chọn lựa chọn này” (`cau-hoi/binh-dang.md`, `cong-ly.md`, `nu-quyen.md`, `tai-san-rieng.md`); số ngày 23/10 chỉ tính bảng theo mẫu chuẩn |
| mục H2 | 888 | 887 | — | -0,1% |  |

## 1. Theo khu vực

| Khu vực | Trang | Trong đó sinh tự động | Mục H2 (viết tay) | Mục H2 (trang sinh) | Dung lượng (nghìn ký tự, bỏ SVG) |
|---|---:|---:|---:|---:|---:|
| `(trang chủ)` | 1 | 0 | 3 | 0 | 6 |
| `bat-dau` | 2 | 0 | 14 | 0 | 26 |
| `cau-hoi` | 58 | 0 | 507 | 0 | 1429 |
| `cong-cu` | 16 | 0 | 156 | 0 | 203 |
| `doc` | 20 | 0 | 178 | 0 | 269 |
| `lich-su` | 11 | 2 | 60 | 1 | 100 |
| `luyen-tap` | 5 | 0 | 2 | 0 | 3 |
| `them` | 7 | 2 | 10 | 890 | 2120 |
| `triet-gia` | 60 | 60 | 0 | 413 | 468 |
| **Tổng** | **180** | **64** | **930** | **1304** | **4623** |

## 2. Dấu thời gian

Trong Lõi viết tay, sau khi bỏ front matter, khối code, khối sinh, mục Nguồn và địa chỉ link. Tổng **128** dấu ở **67** trang.
Cột: năm 2022–2026; cụm “hiện nay”, “gần đây”, “tính đến”, “đến nay”, “mới nhất”, “năm nay”; văn bản luật (“Luật …”, “Nghị định”, “Bộ luật”).

| Trang | Năm | Cụm thời gian | Luật | Tổng |
|---|---:|---:|---:|---:|
| `cau-hoi/quyen-rieng-tu-so.md` | 0 | 1 | 6 | 7 |
| `cau-hoi/tam-tri-va-ai.md` | 6 | 1 | 0 | 7 |
| `cau-hoi/dinh-menh.md` | 1 | 4 | 0 | 5 |
| `cau-hoi/luan-chung-ton-giao.md` | 1 | 4 | 0 | 5 |
| `cau-hoi/nghe-thuat.md` | 4 | 1 | 0 | 5 |
| `cau-hoi/an-tu-hinh.md` | 3 | 1 | 0 | 4 |
| `cau-hoi/dao-duc-moi-truong.md` | 1 | 3 | 0 | 4 |
| `cau-hoi/khi-hau-trach-nhiem.md` | 1 | 1 | 2 | 4 |
| `cau-hoi/tu-do-y-chi.md` | 1 | 1 | 2 | 4 |
| `cau-hoi/van-de-tam-tri.md` | 1 | 3 | 0 | 4 |
| `cau-hoi/chan-ly.md` | 2 | 0 | 1 | 3 |
| `cau-hoi/cong-nghe-ai.md` | 2 | 1 | 0 | 3 |
| `cau-hoi/ngon-ngu.md` | 1 | 2 | 0 | 3 |
| `cau-hoi/noi-doi.md` | 3 | 0 | 0 | 3 |
| `cau-hoi/ban-tinh-con-nguoi.md` | 2 | 0 | 0 | 2 |
| `cau-hoi/bat-dong-tri-thuc.md` | 1 | 1 | 0 | 2 |
| `cau-hoi/binh-dang.md` | 1 | 1 | 0 | 2 |
| `cau-hoi/chien-tranh-chinh-dang.md` | 0 | 1 | 1 | 2 |
| `cau-hoi/cong-ly.md` | 1 | 1 | 0 | 2 |
| `cau-hoi/dao-duc-hanh-dong.md` | 1 | 1 | 0 | 2 |
| `cau-hoi/dao-duc-ung-dung.md` | 1 | 1 | 0 | 2 |
| `cau-hoi/hien-tang.md` | 0 | 2 | 0 | 2 |
| `cau-hoi/khoa-hoc.md` | 1 | 1 | 0 | 2 |
| `cau-hoi/nu-quyen.md` | 1 | 1 | 0 | 2 |
| `cau-hoi/sieu-dao-duc.md` | 1 | 1 | 0 | 2 |
| `cau-hoi/van-de-su-du.md` | 0 | 2 | 0 | 2 |
| `cau-hoi/y-nghia-song.md` | 1 | 1 | 0 | 2 |
| `doc/russell-gia-tri.md` | 1 | 1 | 0 | 2 |
| `cau-hoi/ban-nga-thoi-gian.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/bien-gioi-di-cu.md` | 0 | 1 | 0 | 1 |
| `cau-hoi/cai-chet.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/cai-dep.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/cai-gi-ton-tai.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/cai-toi.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/cuu-giup-ngheo-doi.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/dan-chu.md` | 0 | 1 | 0 | 1 |
| `cau-hoi/duc-tin-ly-tri.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/hanh-phuc.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/khe-uoc-xa-hoi.md` | 0 | 1 | 0 | 1 |
| `cau-hoi/linh-hon.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/loi-chung.md` | 0 | 1 | 0 | 1 |
| `cau-hoi/mo-phong.md` | 0 | 1 | 0 | 1 |
| `cau-hoi/nhan-qua-ban-chat.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/nho-giao-viet.md` | 0 | 1 | 0 | 1 |
| `cau-hoi/pha-thai.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/pho-quat.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/tai-san-rieng.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/thoi-gian.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/tinh-yeu.md` | 0 | 1 | 0 | 1 |
| `cau-hoi/trach-nhiem.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/tri-thuc.md` | 1 | 0 | 0 | 1 |
| `cau-hoi/truc-lam.md` | 0 | 1 | 0 | 1 |
| `cau-hoi/viet-hien-dai.md` | 0 | 1 | 0 | 1 |
| `cau-hoi/vu-tru-khoi-dau.md` | 1 | 0 | 0 | 1 |
| `cong-cu/bien-chung-socrates.md` | 0 | 1 | 0 | 1 |
| `cong-cu/gia-dinh-ngam.md` | 0 | 1 | 0 | 1 |
| `cong-cu/logic-menh-de.md` | 0 | 0 | 1 | 1 |
| `cong-cu/quy-nap.md` | 0 | 1 | 0 | 1 |
| `cong-cu/so-do-hoa-lap-luan.md` | 0 | 1 | 0 | 1 |
| `doc/aurelius-suy-tuong.md` | 0 | 1 | 0 | 1 |
| `doc/hume-nhan-qua.md` | 1 | 0 | 0 | 1 |
| `doc/luan-ngu.md` | 0 | 1 | 0 | 1 |
| `doc/platon-hang-dong.md` | 0 | 1 | 0 | 1 |
| `doc/tam-kinh.md` | 0 | 1 | 0 | 1 |
| `lich-su/nhat-ban-viet-nam.md` | 0 | 1 | 0 | 1 |
| `lich-su/the-ky-20.md` | 0 | 1 | 0 | 1 |
| `lich-su/trung-hoa.md` | 0 | 1 | 0 | 1 |

## 3. Số đếm gõ tay trong văn xuôi

Số đi trước danh từ chỉ nội dung của site (bài, hướng dẫn, câu hỏi, thuật ngữ, triết gia…). Tổng **98** chỗ ở **41** trang. Không phải chỗ nào cũng là số đếm của site (ví dụ “2 bài tập” trong một bài); đợt 3 lọc lại khi thay bằng shortcode.

| Trang | Chỗ |
|---|---|
| `bat-dau/index.md` | 1.785 triết gia; 100 câu hỏi; 40 câu; 60 câu |
| `bat-dau/lo-trinh.md` | 15 bài; 57 bài; 8 bài; 19 hướng dẫn; 100 đoạn hội thoại; 57 bài; 8 bài; 19 hướng dẫn |
| `cau-hoi/ai-nen-cai-tri.md` | 100 câu hỏi |
| `cau-hoi/bien-gioi-di-cu.md` | 100 câu hỏi; 100 câu hỏi |
| `cau-hoi/binh-dang.md` | 1.540 triết gia |
| `cau-hoi/cai-ac.md` | 100 câu hỏi |
| `cau-hoi/cai-chet.md` | 1.110 triết gia |
| `cau-hoi/cai-dep.md` | 40 câu; 1.785 triết gia |
| `cau-hoi/chien-tranh-chinh-dang.md` | 100 câu hỏi; 100 câu hỏi |
| `cau-hoi/cong-ly.md` | 1.540 triết gia |
| `cau-hoi/dan-chu.md` | 100 câu hỏi |
| `cau-hoi/dao-duc-hanh-dong.md` | 1.785 triết gia |
| `cau-hoi/dinh-menh.md` | 560 triết gia |
| `cau-hoi/duc-tri.md` | 100 câu hỏi |
| `cau-hoi/hien-tang.md` | 100 câu hỏi |
| `cau-hoi/index.md` | 57 bài; 40 câu; 60 câu; 10 câu |
| `cau-hoi/khi-hau-trach-nhiem.md` | 100 câu hỏi; 890 triết gia |
| `cau-hoi/mo-phong.md` | 100 câu hỏi |
| `cau-hoi/nghe-thuat.md` | 1.785 triết gia |
| `cau-hoi/nu-quyen.md` | 1.650 triết gia; 100 câu hỏi |
| `cau-hoi/quyen-rieng-tu-so.md` | 50 trang; 100 câu hỏi |
| `cau-hoi/tai-san-rieng.md` | 1.540 triết gia |
| `cau-hoi/thoi-gian.md` | 1.120 câu |
| `cau-hoi/tinh-yeu.md` | 100 câu hỏi |
| `cau-hoi/tri-thuc.md` | 1.785 triết gia |
| `cau-hoi/tu-do-ngon-luan.md` | 100 câu hỏi |
| `cau-hoi/van-de-tam-tri.md` | 1.785 triết gia |
| `cau-hoi/y-nghia-song.md` | 1.730 triết gia |
| `cong-cu/index.md` | 100 đoạn hội thoại |
| `doc/aristotle-dao-duc.md` | 16 trang |
| `doc/descartes-suy-niem.md` | 17 trang |
| `doc/hume-nhan-qua.md` | 30 đoạn |
| `doc/mill-tu-do.md` | 44 đoạn |
| `doc/platon-bien-ho.md` | 25 trang |
| `doc/russell-gia-tri.md` | 13 đoạn |
| `index.md` | 15 bài; 57 câu hỏi; 19 hướng dẫn; 100 đoạn hội thoại; 1.785 triết gia |
| `lich-su/index.md` | 59 triết gia |
| `luyen-tap/index.md` | 100 đoạn hội thoại |
| `luyen-tap/nguy-bien.md` | 10 đoạn |
| `luyen-tap/the-ghi-nho.md` | 5 thuật ngữ |
| `them/cap-nhat.md` | 19 hướng dẫn; 11 bài; 59 trang; 19 hướng dẫn; 38 trang; 57 bài; 249 thuật ngữ; 428 câu; 53 bài; 15 bài; 8 bài; 100 câu hỏi; 17 thuật ngữ; 55 bài; 11 chủ đề; 35 bài; 19 hướng dẫn; 83 bài; 26 bài; 8 trang; 8 bài; 19 hướng dẫn; 11 bài; 24 bài; 38 trang; 150 thuật ngữ; 9 bài; 3 công cụ; 26 bài; 5 bài; 3 bài; 80 thuật ngữ; 100 đoạn hội thoại; 12 đoạn; 100 câu |

## 4. Dữ kiện gõ tay

| Chỉ số | Lõi viết tay | Trang triết gia (sinh) |
|---|---:|---:|
| Chỗ dạng “*Tác phẩm* (năm)” | 159 | 256 |
| Khối `!!! quote` | 108 | 48 |
| Mục trong danh sách Nguồn | 628 | 270 |
| Bài có bảng PhilPapers (trong mục “Giới triết học ngày nay nghĩ gì”) | 39 | — |

Trang triết gia đếm: 59 (không tính `triet-gia/index.md`).

## 5. Trang thiếu mục bắt buộc (KE-HOACH.md mục 5.1)

2 trang.

| Trang | Thiếu |
|---|---|
| `cong-cu/luan-cu-thep.md` | Bài tập · Tự kiểm tra |
| `doc/sartre-hien-sinh.md` | Đọc từng đoạn |

## Cách đếm

- Mục H2: dòng bắt đầu bằng `## ` ngoài khối code và ngoài khối sinh.
- Năm: số 2022–2026 đứng riêng (không nằm trong số khác, ngày dạng 2026-10-12 vẫn tính một lần).
- “*Tác phẩm* (năm)”: chữ in nghiêng ngay trước ngoặc đơn mở đầu bằng năm 3–4 chữ số (cho phép “khoảng”, “k.”, “năm” đứng trước), ví dụ “*Cộng hòa* (khoảng 375 TCN)”.
- Mục Nguồn: dòng danh sách (`1.`, `-`, `*`) thụt không quá 3 dấu cách trong mục `## Nguồn`.
- Mục bắt buộc: so tiêu đề H2 không phân biệt hoa thường, bỏ dấu `?`, `.`, `:` ở cuối và thuộc tính `{…}`.
