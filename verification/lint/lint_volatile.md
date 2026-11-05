# Báo cáo linter nội dung có hạn dùng

Sinh bằng `python tools/lint_volatile.py --write`. Phạm vi: Lõi viết tay, bỏ mục Nguồn, đích link, khối trích. Đầu đợt 1: 90 chỗ (luật cũ, `verification/bao-cao-nen.md` mục 2). Đợt 3 dời chỗ có hạn dùng vào khối thời sự (`data/thoi-su/`), chỗ còn lại vào danh sách miễn có lý do; đích là 0.

**0 chỗ** ở **0 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `nam` | năm 2022 trở đi trong thân bài Lõi | 0 |
| `cum-thoi-gian` | cụm chỉ thời điểm (hiện nay, gần đây, tính đến…) | 0 |
| `van-ban-luat` | nhắc tới văn bản luật cụ thể | 0 |
| `thoi-su-qua-han` | khối thời sự quá hạn rà soát (`review_by`) | 0 |
| `mien-thua` | mục trong danh sách miễn không còn khớp chỗ nào | 0 |

## Chỗ được miễn (61)

Theo `data/style/volatile-allow.yml` (quyết định 20). Mục miễn hết hiệu lực khi ngữ cảnh đổi chữ.

| Lý do | Nghĩa | Số chỗ |
|---|---|---:|
| `co-moc-thoi-gian` | câu đã gắn mốc ngày, nên đúng mãi | 8 |
| `vi-du-gia-dinh` | năm hoặc "năm nay" trong ví dụ, thí nghiệm tư duy, bài tập | 10 |
| `trang-thai-hoc-thuat` | "đến nay/hiện nay" nói về một tranh luận hay giới nghiên cứu, đổi theo thập kỷ | 35 |
| `chung-chung` | "hiện nay" nghĩa chung, không nêu dữ kiện kiểm được | 5 |
| `su-kien-lich-su` | văn bản pháp lý lịch sử có năm | 3 |

| Vị trí | Đơn vị | Tìm thấy | Lý do |
|---|---|---|---|
| `cau-hoi/an-tu-hinh.md:97` | `cau-hoi/an-tu-hinh.md#gioi-triet-hoc-ngay-nay-nghi-gi` | hiện nay | `chung-chung` |
| `cau-hoi/ban-tinh-con-nguoi.md:115` | `cau-hoi/ban-tinh-con-nguoi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | 2025 | `co-moc-thoi-gian` |
| `cau-hoi/bien-gioi-di-cu.md:55` | `cau-hoi/bien-gioi-di-cu.md#cac-lap-truong-chinh` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/chien-tranh-chinh-dang.md:87` | `cau-hoi/chien-tranh-chinh-dang.md#gioi-triet-hoc-ngay-nay-nghi-gi` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/chien-tranh-chinh-dang.md:89` | `cau-hoi/chien-tranh-chinh-dang.md#gioi-triet-hoc-ngay-nay-nghi-gi` | Nghị định | `su-kien-lich-su` |
| `cau-hoi/cong-nghe-ai.md:149` | `cau-hoi/cong-nghe-ai.md#tu-kiem-tra` | mới nhất | `chung-chung` |
| `cau-hoi/cong-nghe-ai.md:151` | `cau-hoi/cong-nghe-ai.md#tu-kiem-tra` | 2026 | `co-moc-thoi-gian` |
| `cau-hoi/dan-chu.md:110` | `cau-hoi/dan-chu.md#gioi-triet-hoc-ngay-nay-nghi-gi` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/dao-duc-hanh-dong.md:74` | `cau-hoi/dao-duc-hanh-dong.md#cac-lap-truong-chinh` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/dao-duc-moi-truong.md:13` | `cau-hoi/dao-duc-moi-truong.md#_dau` | hiện nay | `chung-chung` |
| `cau-hoi/dao-duc-moi-truong.md:59` | `cau-hoi/dao-duc-moi-truong.md#cac-lap-truong-chinh` | hiện nay | `chung-chung` |
| `cau-hoi/dao-duc-moi-truong.md:120` | `cau-hoi/dao-duc-moi-truong.md#lien-he-doi-song` | hiện nay | `chung-chung` |
| `cau-hoi/dinh-menh.md:18` | `cau-hoi/dinh-menh.md#_dau` | năm nay | `vi-du-gia-dinh` |
| `cau-hoi/dinh-menh.md:87` | `cau-hoi/dinh-menh.md#cac-lap-truong-chinh` | hiện nay | `trang-thai-hoc-thuat` |
| `cau-hoi/dinh-menh.md:120` | `cau-hoi/dinh-menh.md#cac-lap-truong-chinh` | hiện nay | `trang-thai-hoc-thuat` |
| `cau-hoi/dinh-menh.md:158` | `cau-hoi/dinh-menh.md#lien-he-doi-song` | năm nay | `vi-du-gia-dinh` |
| `cau-hoi/khe-uoc-xa-hoi.md:110` | `cau-hoi/khe-uoc-xa-hoi.md#cac-lap-truong-chinh` | mới nhất | `trang-thai-hoc-thuat` |
| `cau-hoi/khi-hau-trach-nhiem.md:15` | `cau-hoi/khi-hau-trach-nhiem.md#_dau` | Nghị định | `su-kien-lich-su` |
| `cau-hoi/khi-hau-trach-nhiem.md:64` | `cau-hoi/khi-hau-trach-nhiem.md#cac-lap-truong-chinh` | Nghị định | `su-kien-lich-su` |
| `cau-hoi/khi-hau-trach-nhiem.md:96` | `cau-hoi/khi-hau-trach-nhiem.md#gioi-triet-hoc-ngay-nay-nghi-gi` | hiện nay | `trang-thai-hoc-thuat` |
| `cau-hoi/khi-hau-trach-nhiem.md:104` | `cau-hoi/khi-hau-trach-nhiem.md#lien-he-doi-song` | 2080 | `vi-du-gia-dinh` |
| `cau-hoi/khoa-hoc.md:140` | `cau-hoi/khoa-hoc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | hiện nay | `trang-thai-hoc-thuat` |
| `cau-hoi/linh-hon.md:198` | `cau-hoi/linh-hon.md#tu-viet` | 2040 | `vi-du-gia-dinh` |
| `cau-hoi/loi-chung.md:29` | `cau-hoi/loi-chung.md#thi-nghiem-tu-duy` | gần đây | `vi-du-gia-dinh` |
| `cau-hoi/luan-chung-ton-giao.md:73` | `cau-hoi/luan-chung-ton-giao.md#cac-lap-truong-chinh` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/luan-chung-ton-giao.md:75` | `cau-hoi/luan-chung-ton-giao.md#cac-lap-truong-chinh` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/mo-phong.md:78` | `cau-hoi/mo-phong.md#cac-lap-truong-chinh` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/nghe-thuat.md:77` | `cau-hoi/nghe-thuat.md#cac-lap-truong-chinh` | 2026 | `vi-du-gia-dinh` |
| `cau-hoi/nghe-thuat.md:136` | `cau-hoi/nghe-thuat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | 2022 | `co-moc-thoi-gian` |
| `cau-hoi/nghe-thuat.md:138` | `cau-hoi/nghe-thuat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/nghe-thuat.md:148` | `cau-hoi/nghe-thuat.md#lien-he-doi-song` | 2022 | `co-moc-thoi-gian` |
| `cau-hoi/ngon-ngu.md:42` | `cau-hoi/ngon-ngu.md#cau-hoi-that-su-la-gi` | hiện nay | `trang-thai-hoc-thuat` |
| `cau-hoi/ngon-ngu.md:73` | `cau-hoi/ngon-ngu.md#cac-lap-truong-chinh` | hiện nay | `trang-thai-hoc-thuat` |
| `cau-hoi/nu-quyen.md:106` | `cau-hoi/nu-quyen.md#gioi-triet-hoc-ngay-nay-nghi-gi` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/sieu-dao-duc.md:60` | `cau-hoi/sieu-dao-duc.md#cac-lap-truong-chinh` | gần đây | `trang-thai-hoc-thuat` |
| `cau-hoi/tam-tri-va-ai.md:83` | `cau-hoi/tam-tri-va-ai.md#cac-lap-truong-chinh` | 2023 | `co-moc-thoi-gian` |
| `cau-hoi/tam-tri-va-ai.md:85` | `cau-hoi/tam-tri-va-ai.md#cac-lap-truong-chinh` | 2025 | `co-moc-thoi-gian` |
| `cau-hoi/tam-tri-va-ai.md:130` | `cau-hoi/tam-tri-va-ai.md#lien-he-doi-song` | hiện nay | `co-moc-thoi-gian` |
| `cau-hoi/tinh-yeu.md:90` | `cau-hoi/tinh-yeu.md#gioi-triet-hoc-ngay-nay-nghi-gi` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/truc-lam.md:41` | `cau-hoi/truc-lam.md#cau-hoi-that-su-la-gi` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/tu-do-y-chi.md:23` | `cau-hoi/tu-do-y-chi.md#thi-nghiem-tu-duy` | 2045 | `vi-du-gia-dinh` |
| `cau-hoi/tu-do-y-chi.md:207` | `cau-hoi/tu-do-y-chi.md#tu-kiem-tra` | Bộ luật | `co-moc-thoi-gian` |
| `cau-hoi/van-de-su-du.md:59` | `cau-hoi/van-de-su-du.md#cau-hoi-that-su-la-gi` | hiện nay | `trang-thai-hoc-thuat` |
| `cau-hoi/van-de-su-du.md:123` | `cau-hoi/van-de-su-du.md#gioi-triet-hoc-ngay-nay-nghi-gi` | hiện nay | `trang-thai-hoc-thuat` |
| `cau-hoi/van-de-tam-tri.md:16` | `cau-hoi/van-de-tam-tri.md#_dau` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/van-de-tam-tri.md:22` | `cau-hoi/van-de-tam-tri.md#_dau` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/van-de-tam-tri.md:108` | `cau-hoi/van-de-tam-tri.md#cac-lap-truong-chinh` | đến nay | `trang-thai-hoc-thuat` |
| `cau-hoi/viet-hien-dai.md:109` | `cau-hoi/viet-hien-dai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | gần đây | `trang-thai-hoc-thuat` |
| `cau-hoi/y-nghia-song.md:146` | `cau-hoi/y-nghia-song.md#gioi-triet-hoc-ngay-nay-nghi-gi` | hiện nay | `trang-thai-hoc-thuat` |
| `cong-cu/bien-chung-socrates.md:48` | `cong-cu/bien-chung-socrates.md#vi-du-kinh-dien-euthyphro` | đến nay | `trang-thai-hoc-thuat` |
| `cong-cu/gia-dinh-ngam.md:153` | `cong-cu/gia-dinh-ngam.md#vi-du-2-mot-binh-luan-tren-mang-xa-hoi` | hiện nay | `vi-du-gia-dinh` |
| `cong-cu/quy-nap.md:101` | `cong-cu/quy-nap.md#mot-cau-hoi-khong-de-chiu-vi-sao-tin-quy-nap` | Đến nay | `trang-thai-hoc-thuat` |
| `cong-cu/so-do-hoa-lap-luan.md:115` | `cong-cu/so-do-hoa-lap-luan.md#mot-bai-ve-hoan-chinh` | 2030 | `vi-du-gia-dinh` |
| `cong-cu/so-do-hoa-lap-luan.md:167` | `cong-cu/so-do-hoa-lap-luan.md#bai-tap` | gần đây | `vi-du-gia-dinh` |
| `doc/aurelius-suy-tuong.md:128` | `doc/aurelius-suy-tuong.md#hieu-lam-thuong-gap` | hiện nay | `trang-thai-hoc-thuat` |
| `doc/luan-ngu.md:17` | `doc/luan-ngu.md#_dau` | hiện nay | `trang-thai-hoc-thuat` |
| `doc/platon-hang-dong.md:93` | `doc/platon-hang-dong.md#phan-bac` | đến nay | `trang-thai-hoc-thuat` |
| `doc/tam-kinh.md:16` | `doc/tam-kinh.md#_dau` | đến nay | `trang-thai-hoc-thuat` |
| `lich-su/nhat-ban-viet-nam.md:27` | `lich-su/nhat-ban-viet-nam.md#nhat-ban-tu-phat-giao-den-truong-phai-kyoto` | đến nay | `trang-thai-hoc-thuat` |
| `lich-su/the-ky-20.md:17` | `lich-su/the-ky-20.md#nga-thu-nhat-phan-tich-ngon-ngu-va-logic` | đến nay | `trang-thai-hoc-thuat` |
| `lich-su/trung-hoa.md:50` | `lich-su/trung-hoa.md#manh-tu-vs-tuan-tu-ban-tinh-thien-hay-ac` | đến nay | `trang-thai-hoc-thuat` |
