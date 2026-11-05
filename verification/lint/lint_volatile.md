# Báo cáo linter nội dung có hạn dùng

Sinh bằng `python tools/lint_volatile.py --write`. Phạm vi: Lõi viết tay, bỏ mục Nguồn và đích link. Đây là báo cáo nền của đợt 1 (so với `verification/bao-cao-nen.md` mục 2); đợt 3 dời các chỗ này vào khối thời sự, đích là 0.

**90 chỗ** ở **50 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `nam` | năm 2022 trở đi trong thân bài Lõi | 19 |
| `cum-thoi-gian` | cụm chỉ thời điểm (hiện nay, gần đây, tính đến…) | 58 |
| `van-ban-luat` | nhắc tới văn bản luật cụ thể | 13 |
| `thoi-su-qua-han` | khối thời sự quá hạn rà soát (`review_by`) | 0 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `cau-hoi/an-tu-hinh.md:64` | `cau-hoi/an-tu-hinh.md#cac-lap-truong-chinh` | `nam` | 2024 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/an-tu-hinh.md:64` | `cau-hoi/an-tu-hinh.md#cac-lap-truong-chinh` | `nam` | 2026 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/an-tu-hinh.md:97` | `cau-hoi/an-tu-hinh.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/ban-tinh-con-nguoi.md:115` | `cau-hoi/ban-tinh-con-nguoi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `nam` | 2025 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/ban-tinh-con-nguoi.md:115` | `cau-hoi/ban-tinh-con-nguoi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `nam` | 2025 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/bat-dong-tri-thuc.md:47` | `cau-hoi/bat-dong-tri-thuc.md#cau-hoi-that-su-la-gi` | `cum-thoi-gian` | tính đến | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/bien-gioi-di-cu.md:55` | `cau-hoi/bien-gioi-di-cu.md#cac-lap-truong-chinh` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/binh-dang.md:83` | `cau-hoi/binh-dang.md#cac-lap-truong-chinh` | `cum-thoi-gian` | tính đến | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/chan-ly.md:126` | `cau-hoi/chan-ly.md#lien-he-doi-song` | `nam` | 2025 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/chan-ly.md:128` | `cau-hoi/chan-ly.md#lien-he-doi-song` | `van-ban-luat` | Bộ luật | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/chien-tranh-chinh-dang.md:87` | `cau-hoi/chien-tranh-chinh-dang.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/chien-tranh-chinh-dang.md:89` | `cau-hoi/chien-tranh-chinh-dang.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `van-ban-luat` | Nghị định | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/cong-ly.md:152` | `cau-hoi/cong-ly.md#lien-he-doi-song` | `cum-thoi-gian` | tính đến | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/cong-nghe-ai.md:149` | `cau-hoi/cong-nghe-ai.md#tu-kiem-tra` | `cum-thoi-gian` | mới nhất | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/cong-nghe-ai.md:151` | `cau-hoi/cong-nghe-ai.md#tu-kiem-tra` | `nam` | 2026 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dan-chu.md:110` | `cau-hoi/dan-chu.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dao-duc-hanh-dong.md:74` | `cau-hoi/dao-duc-hanh-dong.md#cac-lap-truong-chinh` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dao-duc-moi-truong.md:13` | `cau-hoi/dao-duc-moi-truong.md#_dau` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dao-duc-moi-truong.md:59` | `cau-hoi/dao-duc-moi-truong.md#cac-lap-truong-chinh` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dao-duc-moi-truong.md:120` | `cau-hoi/dao-duc-moi-truong.md#lien-he-doi-song` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dao-duc-ung-dung.md:170` | `cau-hoi/dao-duc-ung-dung.md#tu-kiem-tra` | `cum-thoi-gian` | tính đến | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dinh-menh.md:18` | `cau-hoi/dinh-menh.md#_dau` | `cum-thoi-gian` | năm nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dinh-menh.md:87` | `cau-hoi/dinh-menh.md#cac-lap-truong-chinh` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dinh-menh.md:120` | `cau-hoi/dinh-menh.md#cac-lap-truong-chinh` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/dinh-menh.md:158` | `cau-hoi/dinh-menh.md#lien-he-doi-song` | `cum-thoi-gian` | năm nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/hien-tang.md:93` | `cau-hoi/hien-tang.md#lien-he-doi-song` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/hien-tang.md:176` | `cau-hoi/hien-tang.md#tu-viet` | `cum-thoi-gian` | tính đến | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/khe-uoc-xa-hoi.md:110` | `cau-hoi/khe-uoc-xa-hoi.md#cac-lap-truong-chinh` | `cum-thoi-gian` | mới nhất | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/khi-hau-trach-nhiem.md:15` | `cau-hoi/khi-hau-trach-nhiem.md#_dau` | `van-ban-luat` | Nghị định | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/khi-hau-trach-nhiem.md:64` | `cau-hoi/khi-hau-trach-nhiem.md#cac-lap-truong-chinh` | `van-ban-luat` | Nghị định | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/khi-hau-trach-nhiem.md:96` | `cau-hoi/khi-hau-trach-nhiem.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/khi-hau-trach-nhiem.md:104` | `cau-hoi/khi-hau-trach-nhiem.md#lien-he-doi-song` | `nam` | 2080 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/khoa-hoc.md:140` | `cau-hoi/khoa-hoc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/linh-hon.md:198` | `cau-hoi/linh-hon.md#tu-viet` | `nam` | 2040 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/loi-chung.md:29` | `cau-hoi/loi-chung.md#thi-nghiem-tu-duy` | `cum-thoi-gian` | gần đây | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/luan-chung-ton-giao.md:14` | `cau-hoi/luan-chung-ton-giao.md#_dau` | `cum-thoi-gian` | năm nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/luan-chung-ton-giao.md:19` | `cau-hoi/luan-chung-ton-giao.md#_dau` | `cum-thoi-gian` | năm nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/luan-chung-ton-giao.md:73` | `cau-hoi/luan-chung-ton-giao.md#cac-lap-truong-chinh` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/luan-chung-ton-giao.md:75` | `cau-hoi/luan-chung-ton-giao.md#cac-lap-truong-chinh` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/mo-phong.md:78` | `cau-hoi/mo-phong.md#cac-lap-truong-chinh` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/nghe-thuat.md:77` | `cau-hoi/nghe-thuat.md#cac-lap-truong-chinh` | `nam` | 2026 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/nghe-thuat.md:136` | `cau-hoi/nghe-thuat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `nam` | 2022 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/nghe-thuat.md:138` | `cau-hoi/nghe-thuat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/nghe-thuat.md:148` | `cau-hoi/nghe-thuat.md#lien-he-doi-song` | `nam` | 2022 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/ngon-ngu.md:42` | `cau-hoi/ngon-ngu.md#cau-hoi-that-su-la-gi` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/ngon-ngu.md:73` | `cau-hoi/ngon-ngu.md#cac-lap-truong-chinh` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/nho-giao-viet.md:126` | `cau-hoi/nho-giao-viet.md#lien-he-doi-song` | `cum-thoi-gian` | gần đây | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/noi-doi.md:133` | `cau-hoi/noi-doi.md#lien-he-doi-song` | `nam` | 2024 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/noi-doi.md:168` | `cau-hoi/noi-doi.md#tu-kiem-tra` | `nam` | 2024 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/nu-quyen.md:106` | `cau-hoi/nu-quyen.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/quyen-rieng-tu-so.md:94` | `cau-hoi/quyen-rieng-tu-so.md#lien-he-doi-song` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/quyen-rieng-tu-so.md:94` | `cau-hoi/quyen-rieng-tu-so.md#lien-he-doi-song` | `van-ban-luat` | Luật | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/quyen-rieng-tu-so.md:94` | `cau-hoi/quyen-rieng-tu-so.md#lien-he-doi-song` | `van-ban-luat` | Luật | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/quyen-rieng-tu-so.md:94` | `cau-hoi/quyen-rieng-tu-so.md#lien-he-doi-song` | `van-ban-luat` | Nghị định | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/quyen-rieng-tu-so.md:94` | `cau-hoi/quyen-rieng-tu-so.md#lien-he-doi-song` | `van-ban-luat` | Nghị định | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/quyen-rieng-tu-so.md:94` | `cau-hoi/quyen-rieng-tu-so.md#lien-he-doi-song` | `van-ban-luat` | Nghị định | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/quyen-rieng-tu-so.md:94` | `cau-hoi/quyen-rieng-tu-so.md#lien-he-doi-song` | `van-ban-luat` | Nghị định | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/sieu-dao-duc.md:60` | `cau-hoi/sieu-dao-duc.md#cac-lap-truong-chinh` | `cum-thoi-gian` | gần đây | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/tam-tri-va-ai.md:83` | `cau-hoi/tam-tri-va-ai.md#cac-lap-truong-chinh` | `nam` | 2023 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/tam-tri-va-ai.md:85` | `cau-hoi/tam-tri-va-ai.md#cac-lap-truong-chinh` | `nam` | 2025 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/tam-tri-va-ai.md:87` | `cau-hoi/tam-tri-va-ai.md#cac-lap-truong-chinh` | `nam` | 2023 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/tam-tri-va-ai.md:130` | `cau-hoi/tam-tri-va-ai.md#lien-he-doi-song` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/tinh-yeu.md:90` | `cau-hoi/tinh-yeu.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/truc-lam.md:41` | `cau-hoi/truc-lam.md#cau-hoi-that-su-la-gi` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/tu-do-y-chi.md:23` | `cau-hoi/tu-do-y-chi.md#thi-nghiem-tu-duy` | `nam` | 2045 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/tu-do-y-chi.md:171` | `cau-hoi/tu-do-y-chi.md#lien-he-doi-song` | `van-ban-luat` | Bộ luật | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/tu-do-y-chi.md:186` | `cau-hoi/tu-do-y-chi.md#doc-van-ban-goc` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/tu-do-y-chi.md:207` | `cau-hoi/tu-do-y-chi.md#tu-kiem-tra` | `van-ban-luat` | Bộ luật | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/van-de-su-du.md:59` | `cau-hoi/van-de-su-du.md#cau-hoi-that-su-la-gi` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/van-de-su-du.md:123` | `cau-hoi/van-de-su-du.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/van-de-tam-tri.md:16` | `cau-hoi/van-de-tam-tri.md#_dau` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/van-de-tam-tri.md:22` | `cau-hoi/van-de-tam-tri.md#_dau` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/van-de-tam-tri.md:108` | `cau-hoi/van-de-tam-tri.md#cac-lap-truong-chinh` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/viet-hien-dai.md:109` | `cau-hoi/viet-hien-dai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | gần đây | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cau-hoi/y-nghia-song.md:146` | `cau-hoi/y-nghia-song.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cong-cu/bien-chung-socrates.md:48` | `cong-cu/bien-chung-socrates.md#vi-du-kinh-dien-euthyphro` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cong-cu/gia-dinh-ngam.md:153` | `cong-cu/gia-dinh-ngam.md#vi-du-2-mot-binh-luan-tren-mang-xa-hoi` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cong-cu/logic-menh-de.md:226` | `cong-cu/logic-menh-de.md#tu-kiem-tra` | `van-ban-luat` | Luật | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cong-cu/quy-nap.md:101` | `cong-cu/quy-nap.md#mot-cau-hoi-khong-de-chiu-vi-sao-tin-quy-nap` | `cum-thoi-gian` | Đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cong-cu/so-do-hoa-lap-luan.md:108` | `cong-cu/so-do-hoa-lap-luan.md#mot-bai-ve-hoan-chinh` | `nam` | 2030 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cong-cu/so-do-hoa-lap-luan.md:115` | `cong-cu/so-do-hoa-lap-luan.md#mot-bai-ve-hoan-chinh` | `nam` | 2030 | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `cong-cu/so-do-hoa-lap-luan.md:167` | `cong-cu/so-do-hoa-lap-luan.md#bai-tap` | `cum-thoi-gian` | gần đây | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `doc/aurelius-suy-tuong.md:128` | `doc/aurelius-suy-tuong.md#hieu-lam-thuong-gap` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `doc/luan-ngu.md:17` | `doc/luan-ngu.md#_dau` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `doc/platon-hang-dong.md:93` | `doc/platon-hang-dong.md#phan-bac` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `doc/russell-gia-tri.md:35` | `doc/russell-gia-tri.md#doc-tung-doan` | `cum-thoi-gian` | hiện nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `doc/tam-kinh.md:16` | `doc/tam-kinh.md#_dau` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `lich-su/nhat-ban-viet-nam.md:27` | `lich-su/nhat-ban-viet-nam.md#nhat-ban-tu-phat-giao-den-truong-phai-kyoto` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `lich-su/the-ky-20.md:17` | `lich-su/the-ky-20.md#nga-thu-nhat-phan-tich-ngon-ngu-va-logic` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
| `lich-su/trung-hoa.md:50` | `lich-su/trung-hoa.md#manh-tu-vs-tuan-tu-ban-tinh-thien-hay-ac` | `cum-thoi-gian` | đến nay | dời vào khối thời sự (data/thoi-su/, đợt 3) hoặc viết lại không phụ thuộc thời gian (đợt 5) |
