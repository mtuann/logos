# Báo cáo linter thuật ngữ

Sinh bằng `python tools/lint_terms.py --write`. Phạm vi: Lõi viết tay. Luật: `data/style/terms-policy.yml` (từ `HUONG-DAN-VIET.md` mục 3). Đây là báo cáo nền của đợt 1: chỉ ghi lại, sửa ở đợt 5.

**134 chỗ** ở **52 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `thuat-ngu` | dùng cách dịch khác thay cho thuật ngữ bắt buộc | 7 |
| `thuat-ngu-mo-ho` | cách dịch khác trùng một từ thường hay thuật ngữ khác: người đọc xem lại, thường là đúng | 127 |
| `ten-rieng` | tên riêng không theo cách phiên quy định (ví dụ Plato → Platon) | 0 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `bat-dau/lo-trinh.md:39` | `bat-dau/lo-trinh.md#2-nhung-cau-hoi-lon` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:10` | `cau-hoi/ai-nen-cai-tri.md#_dau` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:22` | `cau-hoi/ai-nen-cai-tri.md#_dau` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:22` | `cau-hoi/ai-nen-cai-tri.md#_dau` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:50` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:54` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:61` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:65` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:76` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/ai-nen-cai-tri.md:86` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:88` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:92` | `cau-hoi/ai-nen-cai-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:110` | `cau-hoi/ai-nen-cai-tri.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:118` | `cau-hoi/ai-nen-cai-tri.md#doc-van-ban-goc` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/ai-nen-cai-tri.md:196` | `cau-hoi/ai-nen-cai-tri.md#tu-viet` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/ban-nga-thoi-gian.md:59` | `cau-hoi/ban-nga-thoi-gian.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cau-hoi/cai-ac.md:69` | `cau-hoi/cai-ac.md#cac-lap-truong-chinh` | `thuat-ngu` | ý chí tự do | dùng "tự do ý chí" (free will) |
| `cau-hoi/chan-ly.md:73` | `cau-hoi/chan-ly.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/chan-ly.md:79` | `cau-hoi/chan-ly.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/chien-tranh-chinh-dang.md:14` | `cau-hoi/chien-tranh-chinh-dang.md#_dau` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cau-hoi/chien-tranh-chinh-dang.md:61` | `cau-hoi/chien-tranh-chinh-dang.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cau-hoi/chien-tranh-chinh-dang.md:190` | `cau-hoi/chien-tranh-chinh-dang.md#tu-viet` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cau-hoi/cong-nghe-ai.md:57` | `cau-hoi/cong-nghe-ai.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cau-hoi/dan-chu.md:41` | `cau-hoi/dan-chu.md#cau-hoi-that-su-la-gi` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cau-hoi/dao-duc-ung-dung.md:98` | `cau-hoi/dao-duc-ung-dung.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cau-hoi/dinh-menh.md:13` | `cau-hoi/dinh-menh.md#_dau` | `thuat-ngu-mo-ho` | thuyết định mệnh | dùng "tất định luận" (determinism); đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism |
| `cau-hoi/dinh-menh.md:16` | `cau-hoi/dinh-menh.md#_dau` | `thuat-ngu-mo-ho` | thuyết định mệnh | dùng "tất định luận" (determinism); đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism |
| `cau-hoi/dinh-menh.md:41` | `cau-hoi/dinh-menh.md#cau-hoi-that-su-la-gi` | `thuat-ngu-mo-ho` | Thuyết định mệnh | dùng "tất định luận" (determinism); đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism |
| `cau-hoi/dinh-menh.md:73` | `cau-hoi/dinh-menh.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | thuyết định mệnh | dùng "tất định luận" (determinism); đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism |
| `cau-hoi/dinh-menh.md:88` | `cau-hoi/dinh-menh.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | thuyết định mệnh | dùng "tất định luận" (determinism); đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism |
| `cau-hoi/dinh-menh.md:128` | `cau-hoi/dinh-menh.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `thuat-ngu-mo-ho` | thuyết định mệnh | dùng "tất định luận" (determinism); đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism |
| `cau-hoi/dinh-menh.md:151` | `cau-hoi/dinh-menh.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `thuat-ngu-mo-ho` | thuyết định mệnh | dùng "tất định luận" (determinism); đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism |
| `cau-hoi/dinh-menh.md:162` | `cau-hoi/dinh-menh.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | thuyết định mệnh | dùng "tất định luận" (determinism); đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism |
| `cau-hoi/dinh-menh.md:164` | `cau-hoi/dinh-menh.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | thuyết định mệnh | dùng "tất định luận" (determinism); đúng khi nói về fatalism; chỉ sai khi dùng để dịch determinism |
| `cau-hoi/duc-tri.md:76` | `cau-hoi/duc-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/hanh-phuc.md:75` | `cau-hoi/hanh-phuc.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/hanh-phuc.md:79` | `cau-hoi/hanh-phuc.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/hanh-phuc.md:85` | `cau-hoi/hanh-phuc.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/khoa-hoc.md:71` | `cau-hoi/khoa-hoc.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/khoa-hoc.md:148` | `cau-hoi/khoa-hoc.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/luan-chung-ton-giao.md:135` | `cau-hoi/luan-chung-ton-giao.md#lien-he-doi-song` | `thuat-ngu` | tiền đề ẩn | dùng "giả định ngầm" (hidden assumption / unstated premise) |
| `cau-hoi/mo-phong.md:52` | `cau-hoi/mo-phong.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cau-hoi/mo-phong.md:54` | `cau-hoi/mo-phong.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cau-hoi/mo-phong.md:60` | `cau-hoi/mo-phong.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cau-hoi/mo-phong.md:62` | `cau-hoi/mo-phong.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cau-hoi/ngon-ngu.md:39` | `cau-hoi/ngon-ngu.md#cau-hoi-that-su-la-gi` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/ngon-ngu.md:137` | `cau-hoi/ngon-ngu.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/ngon-ngu.md:141` | `cau-hoi/ngon-ngu.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/nho-giao-viet.md:85` | `cau-hoi/nho-giao-viet.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/nu-quyen.md:80` | `cau-hoi/nu-quyen.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cau-hoi/pho-quat.md:134` | `cau-hoi/pho-quat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cau-hoi/sieu-dao-duc.md:84` | `cau-hoi/sieu-dao-duc.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cau-hoi/tai-san-rieng.md:213` | `cau-hoi/tai-san-rieng.md#tu-viet` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/thoi-gian.md:138` | `cau-hoi/thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/tinh-yeu.md:60` | `cau-hoi/tinh-yeu.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cau-hoi/truc-lam.md:102` | `cau-hoi/truc-lam.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/truc-lam.md:119` | `cau-hoi/truc-lam.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/truc-lam.md:121` | `cau-hoi/truc-lam.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/truc-lam.md:125` | `cau-hoi/truc-lam.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/truc-lam.md:165` | `cau-hoi/truc-lam.md#tu-viet` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/tu-do-ngon-luan.md:79` | `cau-hoi/tu-do-ngon-luan.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/tu-do-y-chi.md:99` | `cau-hoi/tu-do-y-chi.md#cac-lap-truong-chinh` | `thuat-ngu` | ý chí tự do | dùng "tự do ý chí" (free will) |
| `cau-hoi/van-de-su-du.md:59` | `cau-hoi/van-de-su-du.md#cau-hoi-that-su-la-gi` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cau-hoi/van-de-su-du.md:135` | `cau-hoi/van-de-su-du.md#lien-he-doi-song` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/van-de-tam-tri.md:81` | `cau-hoi/van-de-tam-tri.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cau-hoi/viet-hien-dai.md:15` | `cau-hoi/viet-hien-dai.md#_dau` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/viet-hien-dai.md:15` | `cau-hoi/viet-hien-dai.md#_dau` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/viet-hien-dai.md:69` | `cau-hoi/viet-hien-dai.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/viet-hien-dai.md:79` | `cau-hoi/viet-hien-dai.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/viet-hien-dai.md:79` | `cau-hoi/viet-hien-dai.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cau-hoi/viet-hien-dai.md:87` | `cau-hoi/viet-hien-dai.md#cac-lap-truong-chinh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cong-cu/doc-van-ban-kho.md:83` | `cong-cu/doc-van-ban-kho.md#thuc-hanh-tren-mot-doan-van-mau` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cong-cu/gia-dinh-ngam.md:74` | `cong-cu/gia-dinh-ngam.md#quy-trinh-nam-buoc` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `cong-cu/gia-dinh-ngam.md:209` | `cong-cu/gia-dinh-ngam.md#bai-tap` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cong-cu/logic-menh-de.md:3` | `cong-cu/logic-menh-de.md#nguon` | `thuat-ngu-mo-ho` | Mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:3` | `cong-cu/logic-menh-de.md#nguon` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:18` | `cong-cu/logic-menh-de.md#menh-de-cau-co-chan-tri` | `thuat-ngu-mo-ho` | Mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:20` | `cong-cu/logic-menh-de.md#menh-de-cau-co-chan-tri` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:20` | `cong-cu/logic-menh-de.md#menh-de-cau-co-chan-tri` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:20` | `cong-cu/logic-menh-de.md#menh-de-cau-co-chan-tri` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:20` | `cong-cu/logic-menh-de.md#menh-de-cau-co-chan-tri` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:22` | `cong-cu/logic-menh-de.md#menh-de-cau-co-chan-tri` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:29` | `cong-cu/logic-menh-de.md#menh-de-cau-co-chan-tri` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:29` | `cong-cu/logic-menh-de.md#menh-de-cau-co-chan-tri` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:29` | `cong-cu/logic-menh-de.md#menh-de-cau-co-chan-tri` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:121` | `cong-cu/logic-menh-de.md#doc-bang-chan-tri-cua-cong-thuc-phuc` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:121` | `cong-cu/logic-menh-de.md#doc-bang-chan-tri-cua-cong-thuc-phuc` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:168` | `cong-cu/logic-menh-de.md#gioi-han-nhung-gi-bang-chan-tri-khong-thay` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:168` | `cong-cu/logic-menh-de.md#gioi-han-nhung-gi-bang-chan-tri-khong-thay` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:179` | `cong-cu/logic-menh-de.md#gioi-han-nhung-gi-bang-chan-tri-khong-thay` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:179` | `cong-cu/logic-menh-de.md#gioi-han-nhung-gi-bang-chan-tri-khong-thay` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/logic-menh-de.md:212` | `cong-cu/logic-menh-de.md#bai-tap` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/luan-cu-thep.md:18` | `cong-cu/luan-cu-thep.md#_dau` | `thuat-ngu` | luận cứ | dùng "lập luận" (argument) |
| `cong-cu/nguy-bien-hinh-thuc.md:65` | `cong-cu/nguy-bien-hinh-thuc.md#bon-cai-bay` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/nguy-bien-hinh-thuc.md:109` | `cong-cu/nguy-bien-hinh-thuc.md#bang-tra-nhanh` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `cong-cu/nguy-bien.md:101` | `cong-cu/nguy-bien.md#nhom-1-sai-lien-quan` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `cong-cu/nguy-bien.md:157` | `cong-cu/nguy-bien.md#nhom-2-gia-dinh-sai` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cong-cu/quy-nap.md:117` | `cong-cu/quy-nap.md#suy-luan-den-loi-giai-thich-tot-nhat` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `cong-cu/quy-nap.md:183` | `cong-cu/quy-nap.md#bai-tap` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/aristotle-dao-duc.md:88` | `doc/aristotle-dao-duc.md#phan-bac` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/aristotle-dao-duc.md:104` | `doc/aristotle-dao-duc.md#cau-hoi-de-tu-viet` | `thuat-ngu` | luận cứ | dùng "lập luận" (argument) |
| `doc/aurelius-suy-tuong.md:30` | `doc/aurelius-suy-tuong.md#doc-tung-doan` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `doc/hume-nhan-qua.md:83` | `doc/hume-nhan-qua.md#tai-dung-lap-luan` | `thuat-ngu-mo-ho` | Hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/luan-ngu.md:53` | `doc/luan-ngu.md#doc-tung-doan` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/platon-bien-ho.md:97` | `doc/platon-bien-ho.md#phan-bac` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/platon-hang-dong.md:79` | `doc/platon-hang-dong.md#tai-dung-lap-luan` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/platon-hang-dong.md:82` | `doc/platon-hang-dong.md#tai-dung-lap-luan` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/platon-hang-dong.md:84` | `doc/platon-hang-dong.md#tai-dung-lap-luan` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/platon-hang-dong.md:84` | `doc/platon-hang-dong.md#tai-dung-lap-luan` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/platon-hang-dong.md:87` | `doc/platon-hang-dong.md#tai-dung-lap-luan` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/platon-hang-dong.md:97` | `doc/platon-hang-dong.md#phan-bac` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/platon-hang-dong.md:105` | `doc/platon-hang-dong.md#hieu-lam-thuong-gap` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/platon-hang-dong.md:134` | `doc/platon-hang-dong.md#doc-tiep` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `doc/russell-gia-tri.md:82` | `doc/russell-gia-tri.md#phan-bac` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `doc/tam-kinh.md:12` | `doc/tam-kinh.md#_dau` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `doc/tam-kinh.md:76` | `doc/tam-kinh.md#doc-tung-doan` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `doc/tam-kinh.md:133` | `doc/tam-kinh.md#doc-tiep` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `doc/tho-van-ly-tran.md:22` | `doc/tho-van-ly-tran.md#boi-canh` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `lich-su/an-do.md:108` | `lich-su/an-do.md#sau-truong-phai-chinh-thong-tong-quan-ngan` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `lich-su/can-dai.md:13` | `lich-su/can-dai.md#_dau` | `thuat-ngu-mo-ho` | đúng đắn | dùng "vững chắc" (sound); cũng là từ thường |
| `lich-su/can-dai.md:19` | `lich-su/can-dai.md#descartes-khoi-dau-bang-su-hoai-nghi` | `thuat-ngu-mo-ho` | mệnh đề | dùng "khẳng định" (claim / assertion); cũng là thuật ngữ đúng cho proposition (logic mệnh đề) |
| `lich-su/can-dai.md:31` | `lich-su/can-dai.md#cac-nha-duy-ly-spinoza-va-leibniz` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `lich-su/hy-lap-co-dai.md:33` | `lich-su/hy-lap-co-dai.md#socrates-nguoi-chi-biet-dat-cau-hoi` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `lich-su/nhat-ban-viet-nam.md:19` | `lich-su/nhat-ban-viet-nam.md#nhat-ban-tu-phat-giao-den-truong-phai-kyoto` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `lich-su/nhat-ban-viet-nam.md:25` | `lich-su/nhat-ban-viet-nam.md#nhat-ban-tu-phat-giao-den-truong-phai-kyoto` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `lich-su/nhat-ban-viet-nam.md:25` | `lich-su/nhat-ban-viet-nam.md#nhat-ban-tu-phat-giao-den-truong-phai-kyoto` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `lich-su/nhat-ban-viet-nam.md:35` | `lich-su/nhat-ban-viet-nam.md#viet-nam-thien-truc-lam-va-nho-hoc` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `lich-su/the-ky-19.md:19` | `lich-su/the-ky-19.md#hegel-moi-thu-deu-van-dong-theo-bien-chung` | `thuat-ngu-mo-ho` | Tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `lich-su/the-ky-19.md:33` | `lich-su/the-ky-19.md#marx-lat-nguoc-hegel` | `thuat-ngu` | luận cứ | dùng "lập luận" (argument) |
| `lich-su/the-ky-19.md:75` | `lich-su/the-ky-19.md#tom-tat-dong-thoi-gian` | `thuat-ngu-mo-ho` | Tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `lich-su/trung-co.md:21` | `lich-su/trung-co.md#augustine-noi-tam-va-thanh-pho-cua-chua` | `thuat-ngu` | ý chí tự do | dùng "tự do ý chí" (free will) |
| `lich-su/trung-co.md:25` | `lich-su/trung-co.md#anselm-duc-tin-di-tim-hieu-biet` | `thuat-ngu-mo-ho` | hiểu biết | dùng "tri thức" (knowledge); cũng là từ thường |
| `lich-su/trung-co.md:27` | `lich-su/trung-co.md#anselm-duc-tin-di-tim-hieu-biet` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
| `lich-su/trung-hoa.md:94` | `lich-su/trung-hoa.md#tan-nho-giao-va-thien-tong-quan-ngan` | `thuat-ngu-mo-ho` | tinh thần | dùng "tâm trí" (mind); cũng là từ thường (tinh thần, tâm lý; spirit) |
