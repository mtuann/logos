# Báo cáo linter số liệu khảo sát

Sinh bằng `python tools/lint_so_lieu.py --write`. Phạm vi: Lõi viết tay, `thi-nghiem.json`, chữ trong `tools/figures.py`. Số liệu PhilPapers chỉ lấy từ `data/kb/philpapers-2020.json` (quyết định 3); số gõ tay trùng kho đổi thành `[[pp:…]]` sau khi `philpapers/*` đóng băng (ban-giao/dot-5.md 5.2).

**223 chỗ** ở **43 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `go-tay` | % khảo sát gõ tay trùng số trong kho: đổi thành `[[pp:…]]%` | 192 |
| `ngoai-kho` | % trong ngữ cảnh khảo sát mà kho không có: đối chiếu số liệu chính thức | 12 |
| `quiz` | % trong câu hỏi, đáp án đúng hoặc lời giải của quiz mà kho không có | 6 |
| `du-lieu` | % khảo sát gõ tay trong dữ liệu luyện tập hoặc trong chữ của hình | 13 |
| `mien-thua` | mục miễn không còn khớp chỗ nào | 0 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `cau-hoi/an-tu-hinh.md:16` | `cau-hoi/an-tu-hinh.md#_dau` | `go-tay` | 17,7% | đổi thành `[[pp:an-tu-hinh.duoc-phep]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/an-tu-hinh.md:16` | `cau-hoi/an-tu-hinh.md#_dau` | `go-tay` | 75,1% | đổi thành `[[pp:an-tu-hinh.khong-duoc-phep]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:14` | `cau-hoi/ban-nga-thoi-gian.md#_dau` | `go-tay` | 14,9% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-su-kien-bo-sung]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/ban-nga-thoi-gian.md:14` | `cau-hoi/ban-nga-thoi-gian.md#_dau` | `go-tay` | 19,1% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-sinh-hoc]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/ban-nga-thoi-gian.md:14` | `cau-hoi/ban-nga-thoi-gian.md#_dau` | `go-tay` | 35,2% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.song-sot]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:14` | `cau-hoi/ban-nga-thoi-gian.md#_dau` | `go-tay` | 40,1% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.chet]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:14` | `cau-hoi/ban-nga-thoi-gian.md#_dau` | `go-tay` | 43,7% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-tam-ly]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:97` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 14,9% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-su-kien-bo-sung]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/ban-nga-thoi-gian.md:97` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 19,1% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-sinh-hoc]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/ban-nga-thoi-gian.md:97` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 26,6% | đổi thành `[[pp:ban-sac-ca-nhan.khac]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/ban-nga-thoi-gian.md:97` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 43,7% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-tam-ly]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:99` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 35,2% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.song-sot]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:99` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 35,2% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.song-sot]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:99` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 40,1% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.chet]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:101` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 35,2% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.song-sot]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:101` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 40,1% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.chet]]%` |
| `cau-hoi/ban-nga-thoi-gian.md:101` | `cau-hoi/ban-nga-thoi-gian.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 43,7% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-tam-ly]]%` |
| `cau-hoi/ban-tinh-con-nguoi.md:115` | `cau-hoi/ban-tinh-con-nguoi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 49,34% | kho không có số này: đối chiếu tools/philpapers-2020.md |
| `cau-hoi/bat-dong-tri-thuc.md:16` | `cau-hoi/bat-dong-tri-thuc.md#_dau` | `go-tay` | 19,4% | đổi thành `[[pp:bat-dong-hop-ly-hai-nguoi-cung-bang-chung-co-the-bat-dong-ma.khong-the-non-permissivism]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/bat-dong-tri-thuc.md:16` | `cau-hoi/bat-dong-tri-thuc.md#_dau` | `go-tay` | 70,2% | đổi thành `[[pp:bat-dong-hop-ly-hai-nguoi-cung-bang-chung-co-the-bat-dong-ma.co-the-permissivism]]%` |
| `cau-hoi/bat-dong-tri-thuc.md:135` | `cau-hoi/bat-dong-tri-thuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 70,2% | đổi thành `[[pp:bat-dong-hop-ly-hai-nguoi-cung-bang-chung-co-the-bat-dong-ma.co-the-permissivism]]%` |
| `cau-hoi/binh-dang.md:15` | `cau-hoi/binh-dang.md#_dau` | `go-tay` | 44,0% | đổi thành `[[pp:triet-hoc-chinh-tri.chu-nghia-binh-dang-egalitarianism]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/binh-dang.md:98` | `cau-hoi/binh-dang.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 44,0% | đổi thành `[[pp:triet-hoc-chinh-tri.chu-nghia-binh-dang-egalitarianism]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/binh-dang.md:100` | `cau-hoi/binh-dang.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 44,0% | đổi thành `[[pp:triet-hoc-chinh-tri.chu-nghia-binh-dang-egalitarianism]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/cai-chet.md:131` | `cau-hoi/cai-chet.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 41,3% | đổi thành `[[pp:bat-tu-ban-co-chon-khong.khong]]%` |
| `cau-hoi/cai-chet.md:131` | `cau-hoi/cai-chet.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 44,9% | đổi thành `[[pp:bat-tu-ban-co-chon-khong.co]]%` |
| `cau-hoi/cai-dep.md:15` | `cau-hoi/cai-dep.md#_dau` | `go-tay` | 40,6% | đổi thành `[[pp:gia-tri-tham-my.chu-quan]]%` |
| `cau-hoi/cai-dep.md:15` | `cau-hoi/cai-dep.md#_dau` | `go-tay` | 43,5% | đổi thành `[[pp:gia-tri-tham-my.khach-quan]]%` |
| `cau-hoi/cai-dep.md:130` | `cau-hoi/cai-dep.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 37,2% | đổi thành `[[pp:gia-tri-tham-my.chu-quan/loai-tru]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:16` | `cau-hoi/cai-gi-ton-tai.md#_dau` | `go-tay` | 11,5% | đổi thành `[[pp:tinh-chat-properties.lop-tap-hop]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:16` | `cau-hoi/cai-gi-ton-tai.md#_dau` | `go-tay` | 15,3% | đổi thành `[[pp:tinh-chat-properties.trope-tinh-chat-ca-biet]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:16` | `cau-hoi/cai-gi-ton-tai.md#_dau` | `go-tay` | 19,8% | đổi thành `[[pp:tinh-chat-properties.pho-quat-sieu-viet-kieu-platon]]%` |
| `cau-hoi/cai-gi-ton-tai.md:16` | `cau-hoi/cai-gi-ton-tai.md#_dau` | `go-tay` | 20,6% | đổi thành `[[pp:tinh-chat-properties.pho-quat-noi-tai-kieu-aristotle]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:16` | `cau-hoi/cai-gi-ton-tai.md#_dau` | `go-tay` | 38,4% | đổi thành `[[pp:doi-tuong-truu-tuong.thuyet-platon-platonism]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:16` | `cau-hoi/cai-gi-ton-tai.md#_dau` | `go-tay` | 41,9% | đổi thành `[[pp:doi-tuong-truu-tuong.duy-danh-luan-nominalism]]%` |
| `cau-hoi/cai-gi-ton-tai.md:16` | `cau-hoi/cai-gi-ton-tai.md#_dau` | `go-tay` | 79,5% | đổi thành `[[pp:the-gioi-ben-ngoai.thuc-tai-luan-phi-hoai-nghi]]%` |
| `cau-hoi/cai-gi-ton-tai.md:16` | `cau-hoi/cai-gi-ton-tai.md#_dau` | `go-tay` | 8,1% | đổi thành `[[pp:tinh-chat-properties.khong-ton-tai]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:104` | `cau-hoi/cai-gi-ton-tai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 11,5% | đổi thành `[[pp:tinh-chat-properties.lop-tap-hop]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:104` | `cau-hoi/cai-gi-ton-tai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 15,3% | đổi thành `[[pp:tinh-chat-properties.trope-tinh-chat-ca-biet]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:104` | `cau-hoi/cai-gi-ton-tai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 29,1% | đổi thành `[[pp:tinh-chat-properties.khac]]%` |
| `cau-hoi/cai-gi-ton-tai.md:104` | `cau-hoi/cai-gi-ton-tai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 8,1% | đổi thành `[[pp:tinh-chat-properties.khong-ton-tai]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:104` | `cau-hoi/cai-gi-ton-tai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 40% | kho không có số này: đối chiếu tools/philpapers-2020.md |
| `cau-hoi/cai-gi-ton-tai.md:106` | `cau-hoi/cai-gi-ton-tai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 79,5% | đổi thành `[[pp:the-gioi-ben-ngoai.thuc-tai-luan-phi-hoai-nghi]]%` |
| `cau-hoi/cai-gi-ton-tai.md:122` | `cau-hoi/cai-gi-ton-tai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 8,2% | đổi thành `[[pp:cau-thanh-vat-chat-khi-nao-nhieu-vat-hop-thanh-mot-vat.khong-bao-gio-hu-vo-luan]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/cai-gi-ton-tai.md:136` | `cau-hoi/cai-gi-ton-tai.md#tu-kiem-tra` | `quiz` | câu 5: 21% | số không có trong kho: đối chiếu tools/philpapers-2020.md; gần `[[pp:tinh-chat-properties.pho-quat-noi-tai-kieu-aristotle]]` (20,6) |
| `cau-hoi/cai-toi.md:16` | `cau-hoi/cai-toi.md#_dau` | `go-tay` | 14,9% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-su-kien-bo-sung]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/cai-toi.md:16` | `cau-hoi/cai-toi.md#_dau` | `go-tay` | 19,1% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-sinh-hoc]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/cai-toi.md:16` | `cau-hoi/cai-toi.md#_dau` | `go-tay` | 35,2% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.song-sot]]%` |
| `cau-hoi/cai-toi.md:16` | `cau-hoi/cai-toi.md#_dau` | `go-tay` | 40,1% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.chet]]%` |
| `cau-hoi/cai-toi.md:16` | `cau-hoi/cai-toi.md#_dau` | `go-tay` | 43,7% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-tam-ly]]%` |
| `cau-hoi/cai-toi.md:118` | `cau-hoi/cai-toi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 43,7% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-tam-ly]]%` |
| `cau-hoi/cai-toi.md:119` | `cau-hoi/cai-toi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 35,2% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.song-sot]]%` |
| `cau-hoi/cai-toi.md:119` | `cau-hoi/cai-toi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 40,1% | đổi thành `[[pp:may-dich-chuyen-vat-chat-moi.chet]]%` |
| `cau-hoi/chan-ly.md:17` | `cau-hoi/chan-ly.md#_dau` | `go-tay` | 10,2% | đổi thành `[[pp:chan-ly.thuyet-tri-thuc-epistemic]]%` |
| `cau-hoi/chan-ly.md:17` | `cau-hoi/chan-ly.md#_dau` | `go-tay` | 24,5% | đổi thành `[[pp:chan-ly.thuyet-giam-phat-deflationary]]%` |
| `cau-hoi/chan-ly.md:17` | `cau-hoi/chan-ly.md#_dau` | `go-tay` | 51,4% | đổi thành `[[pp:chan-ly.thuyet-tuong-ung-correspondence]]%` |
| `cau-hoi/chan-ly.md:117` | `cau-hoi/chan-ly.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 48,3% | đổi thành `[[pp:chan-ly.thuyet-tuong-ung-correspondence/loai-tru]]%` |
| `cau-hoi/chan-ly.md:117` | `cau-hoi/chan-ly.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 51,4% | đổi thành `[[pp:chan-ly.thuyet-tuong-ung-correspondence]]%` |
| `cau-hoi/chan-ly.md:118` | `cau-hoi/chan-ly.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 12,4% | đổi thành `[[pp:mau-thuan-dung.co-that]]%` |
| `cau-hoi/chan-ly.md:118` | `cau-hoi/chan-ly.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 71,4% | đổi thành `[[pp:mau-thuan-dung.bat-kha]]%` |
| `cau-hoi/cong-ly.md:16` | `cau-hoi/cong-ly.md#_dau` | `go-tay` | 13,4% | đổi thành `[[pp:triet-hoc-chinh-tri.chu-nghia-tu-do-ca-nhan-libertarianism]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/cong-ly.md:16` | `cau-hoi/cong-ly.md#_dau` | `go-tay` | 27,3% | đổi thành `[[pp:triet-hoc-chinh-tri.cong-dong-luan]]%` |
| `cau-hoi/cong-ly.md:16` | `cau-hoi/cong-ly.md#_dau` | `go-tay` | 44,0% | đổi thành `[[pp:triet-hoc-chinh-tri.chu-nghia-binh-dang-egalitarianism]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/cong-nghe-ai.md:16` | `cau-hoi/cong-nghe-ai.md#_dau` | `go-tay` | 3,4% | đổi thành `[[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-hien-tai-nam-2020]]%` |
| `cau-hoi/cong-nghe-ai.md:16` | `cau-hoi/cong-nghe-ai.md#_dau` | `go-tay` | 39,2% | đổi thành `[[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-tuong-lai]]%` |
| `cau-hoi/cong-nghe-ai.md:16` | `cau-hoi/cong-nghe-ai.md#_dau` | `go-tay` | 76,9% | đổi thành `[[pp:may-trai-nghiem-co-vao-khong.khong]]%` |
| `cau-hoi/cong-nghe-ai.md:16` | `cau-hoi/cong-nghe-ai.md#_dau` | `go-tay` | 82,4% | đổi thành `[[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-hien-tai-nam-2020/bac-bo]]%` |
| `cau-hoi/cong-nghe-ai.md:113` | `cau-hoi/cong-nghe-ai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 3,4% | đổi thành `[[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-hien-tai-nam-2020]]%` |
| `cau-hoi/cong-nghe-ai.md:113` | `cau-hoi/cong-nghe-ai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 39% | đổi thành `[[pp:bai-toan-newcomb.lay-hai-hop]]%` |
| `cau-hoi/cong-nghe-ai.md:113` | `cau-hoi/cong-nghe-ai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 27% | kho không có số này: đối chiếu tools/philpapers-2020.md; gần `[[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-tuong-lai/bac-bo]]` (26,8) |
| `cau-hoi/cong-nghe-ai.md:113` | `cau-hoi/cong-nghe-ai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 82% | kho không có số này: đối chiếu tools/philpapers-2020.md; gần `[[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-hien-tai-nam-2020/bac-bo]]` (82,4) |
| `cau-hoi/cong-nghe-ai.md:114` | `cau-hoi/cong-nghe-ai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 13% | kho không có số này: đối chiếu tools/philpapers-2020.md; gần `[[pp:may-trai-nghiem-co-vao-khong.co]]` (13,3) |
| `cau-hoi/cong-nghe-ai.md:114` | `cau-hoi/cong-nghe-ai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 77% | kho không có số này: đối chiếu tools/philpapers-2020.md; gần `[[pp:may-trai-nghiem-co-vao-khong.khong]]` (76,9) |
| `cau-hoi/cong-nghe-ai.md:115` | `cau-hoi/cong-nghe-ai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 52% | kho không có số này: đối chiếu tools/philpapers-2020.md; gần `[[pp:tam-tri.vat-ly-luan]]` (51,9) |
| `cau-hoi/cong-nghe-ai.md:153` | `cau-hoi/cong-nghe-ai.md#tu-kiem-tra` | `quiz` | câu 1: 77% | số không có trong kho: đối chiếu tools/philpapers-2020.md; gần `[[pp:may-trai-nghiem-co-vao-khong.khong]]` (76,9) |
| `cau-hoi/cuu-giup-ngheo-doi.md:15` | `cau-hoi/cuu-giup-ngheo-doi.md#_dau` | `go-tay` | 62,9% | đổi thành `[[pp:phai-keo-theo-co-the-ought-implies-can.co]]%` |
| `cau-hoi/cuu-giup-ngheo-doi.md:101` | `cau-hoi/cuu-giup-ngheo-doi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 22,0% | đổi thành `[[pp:cay-cau-day-nguoi.day]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/cuu-giup-ngheo-doi.md:101` | `cau-hoi/cuu-giup-ngheo-doi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 63,4% | đổi thành `[[pp:bai-toan-xe-dien-be-ghi.be-ghi]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/cuu-giup-ngheo-doi.md:103` | `cau-hoi/cuu-giup-ngheo-doi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 62,9% | đổi thành `[[pp:phai-keo-theo-co-the-ought-implies-can.co]]%` |
| `cau-hoi/dan-chu.md:108` | `cau-hoi/dan-chu.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 13,4% | đổi thành `[[pp:ban-sac-ca-nhan.quan-diem-su-kien-bo-sung/loai-tru]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/dan-chu.md:108` | `cau-hoi/dan-chu.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 27,3% | đổi thành `[[pp:triet-hoc-chinh-tri.cong-dong-luan]]%` |
| `cau-hoi/dan-chu.md:108` | `cau-hoi/dan-chu.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 44,0% | đổi thành `[[pp:gia-tri-trong-khoa-hoc.nhat-thiet-mang-gia-tri]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/dao-duc-hanh-dong.md:16` | `cau-hoi/dao-duc-hanh-dong.md#_dau` | `go-tay` | 30,6% | đổi thành `[[pp:dao-duc-hoc-chuan-tac.he-qua-luan]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/dao-duc-hanh-dong.md:16` | `cau-hoi/dao-duc-hanh-dong.md#_dau` | `go-tay` | 32,1% | đổi thành `[[pp:dao-duc-hoc-chuan-tac.nghia-vu-luan]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/dao-duc-hanh-dong.md:16` | `cau-hoi/dao-duc-hanh-dong.md#_dau` | `go-tay` | 37,0% | đổi thành `[[pp:dao-duc-hoc-chuan-tac.dao-duc-hoc-duc-hanh]]%` |
| `cau-hoi/dao-duc-hanh-dong.md:16` | `cau-hoi/dao-duc-hanh-dong.md#_dau` | `go-tay` | 56% | đổi thành `[[pp:cay-cau-day-nguoi.khong-day]]%` |
| `cau-hoi/dao-duc-hanh-dong.md:16` | `cau-hoi/dao-duc-hanh-dong.md#_dau` | `go-tay` | 63,4% | đổi thành `[[pp:bai-toan-xe-dien-be-ghi.be-ghi]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/dao-duc-hanh-dong.md:124` | `cau-hoi/dao-duc-hanh-dong.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 40% | kho không có số này: đối chiếu tools/philpapers-2020.md |
| `cau-hoi/dao-duc-hanh-dong.md:125` | `cau-hoi/dao-duc-hanh-dong.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 56% | đổi thành `[[pp:cay-cau-day-nguoi.khong-day]]%` |
| `cau-hoi/dao-duc-hanh-dong.md:125` | `cau-hoi/dao-duc-hanh-dong.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 63,4% | đổi thành `[[pp:bai-toan-xe-dien-be-ghi.be-ghi]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/dao-duc-moi-truong.md:15` | `cau-hoi/dao-duc-moi-truong.md#_dau` | `go-tay` | 42,2% | đổi thành `[[pp:dao-duc-moi-truong.lay-con-nguoi-lam-trung-tam]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/dao-duc-moi-truong.md:15` | `cau-hoi/dao-duc-moi-truong.md#_dau` | `go-tay` | 50,7% | đổi thành `[[pp:dao-duc-moi-truong.khong-lay-con-nguoi-lam-trung-tam]]%` |
| `cau-hoi/dao-duc-ung-dung.md:16` | `cau-hoi/dao-duc-ung-dung.md#_dau` | `go-tay` | 18,4% | đổi thành `[[pp:an-dong-vat-va-san-pham-dong-vat-trong-hoan-canh-binh-thuong.thuan-chay-khong-ca-hai]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/dao-duc-ung-dung.md:16` | `cau-hoi/dao-duc-ung-dung.md#_dau` | `go-tay` | 26,5% | đổi thành `[[pp:an-dong-vat-va-san-pham-dong-vat-trong-hoan-canh-binh-thuong.an-chay-khong-an-thit-van-dung-san-pham-dong-vat]]%` |
| `cau-hoi/dao-duc-ung-dung.md:16` | `cau-hoi/dao-duc-ung-dung.md#_dau` | `go-tay` | 48,0% | đổi thành `[[pp:an-dong-vat-va-san-pham-dong-vat-trong-hoan-canh-binh-thuong.an-tap-duoc-an-ca-thit-lan-san-pham-dong-vat]]%` |
| `cau-hoi/dao-duc-ung-dung.md:126` | `cau-hoi/dao-duc-ung-dung.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 45% | đổi thành `[[pp:luat-phap.phi-thuc-chung-luan-phap-ly]]%` |
| `cau-hoi/dao-duc-ung-dung.md:126` | `cau-hoi/dao-duc-ung-dung.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 48,0% | đổi thành `[[pp:an-dong-vat-va-san-pham-dong-vat-trong-hoan-canh-binh-thuong.an-tap-duoc-an-ca-thit-lan-san-pham-dong-vat]]%` |
| `cau-hoi/dinh-menh.md:16` | `cau-hoi/dinh-menh.md#_dau` | `go-tay` | 22% | đổi thành `[[pp:cay-cau-day-nguoi.day]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/dinh-menh.md:16` | `cau-hoi/dinh-menh.md#_dau` | `go-tay` | 39,9% | đổi thành `[[pp:ban-the-luan-thoi-gian.vinh-cuu-luan]]%` |
| `cau-hoi/dinh-menh.md:128` | `cau-hoi/dinh-menh.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 11,2% | đổi thành `[[pp:tu-do-y-chi.khong-co-tu-do-y-chi]]%` |
| `cau-hoi/dinh-menh.md:128` | `cau-hoi/dinh-menh.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 18,8% | đổi thành `[[pp:phuong-phap-triet-hoc-chinh-tri.khac]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/dinh-menh.md:128` | `cau-hoi/dinh-menh.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 59,2% | đổi thành `[[pp:tu-do-y-chi.tuong-thich-luan]]%` |
| `cau-hoi/dinh-menh.md:150` | `cau-hoi/dinh-menh.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 22% | đổi thành `[[pp:cay-cau-day-nguoi.day]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/dinh-menh.md:150` | `cau-hoi/dinh-menh.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 32,0% | đổi thành `[[pp:co-hoc-luong-tu-dien-giai.khac]]%` |
| `cau-hoi/duc-tin-ly-tri.md:16` | `cau-hoi/duc-tin-ly-tri.md#_dau` | `go-tay` | 14,2% | đổi thành `[[pp:luan-chung-cho-su-ton-tai-cua-thuong-de-manh-nhat.thuc-dung]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/duc-tin-ly-tri.md:16` | `cau-hoi/duc-tin-ly-tri.md#_dau` | `go-tay` | 18,9% | đổi thành `[[pp:thuong-de.huu-than]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/duc-tin-ly-tri.md:16` | `cau-hoi/duc-tin-ly-tri.md#_dau` | `go-tay` | 66,9% | đổi thành `[[pp:thuong-de.vo-than]]%` |
| `cau-hoi/duc-tin-ly-tri.md:113` | `cau-hoi/duc-tin-ly-tri.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 14,2% | đổi thành `[[pp:luan-chung-cho-su-ton-tai-cua-thuong-de-manh-nhat.thuc-dung]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/duc-tin-ly-tri.md:113` | `cau-hoi/duc-tin-ly-tri.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 19,4% | đổi thành `[[pp:bat-dong-hop-ly-hai-nguoi-cung-bang-chung-co-the-bat-dong-ma.khong-the-non-permissivism]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/duc-tin-ly-tri.md:113` | `cau-hoi/duc-tin-ly-tri.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 70,2% | đổi thành `[[pp:bat-dong-hop-ly-hai-nguoi-cung-bang-chung-co-the-bat-dong-ma.co-the-permissivism]]%` |
| `cau-hoi/duc-tin-ly-tri.md:115` | `cau-hoi/duc-tin-ly-tri.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 18,9% | đổi thành `[[pp:thuong-de.huu-than]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/duc-tin-ly-tri.md:115` | `cau-hoi/duc-tin-ly-tri.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 66,9% | đổi thành `[[pp:thuong-de.vo-than]]%` |
| `cau-hoi/hanh-phuc.md:16` | `cau-hoi/hanh-phuc.md#_dau` | `go-tay` | 12,7% | đổi thành `[[pp:phuc-loi-well-being.khoai-lac-trai-nghiem]]%` |
| `cau-hoi/hanh-phuc.md:16` | `cau-hoi/hanh-phuc.md#_dau` | `go-tay` | 13,3% | đổi thành `[[pp:may-trai-nghiem-co-vao-khong.co]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/hanh-phuc.md:16` | `cau-hoi/hanh-phuc.md#_dau` | `go-tay` | 18,6% | đổi thành `[[pp:phuc-loi-well-being.thoa-man-uoc-muon]]%` |
| `cau-hoi/hanh-phuc.md:16` | `cau-hoi/hanh-phuc.md#_dau` | `go-tay` | 53,2% | đổi thành `[[pp:phuc-loi-well-being.danh-sach-khach-quan]]%` |
| `cau-hoi/hanh-phuc.md:16` | `cau-hoi/hanh-phuc.md#_dau` | `go-tay` | 76,9% | đổi thành `[[pp:may-trai-nghiem-co-vao-khong.khong]]%` |
| `cau-hoi/hanh-phuc.md:103` | `cau-hoi/hanh-phuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 13,3% | đổi thành `[[pp:may-trai-nghiem-co-vao-khong.co]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/hanh-phuc.md:103` | `cau-hoi/hanh-phuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 76,9% | đổi thành `[[pp:may-trai-nghiem-co-vao-khong.khong]]%` |
| `cau-hoi/hanh-phuc.md:107` | `cau-hoi/hanh-phuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 12,7% | đổi thành `[[pp:phuc-loi-well-being.khoai-lac-trai-nghiem]]%` |
| `cau-hoi/hanh-phuc.md:107` | `cau-hoi/hanh-phuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 18,6% | đổi thành `[[pp:phuc-loi-well-being.thoa-man-uoc-muon]]%` |
| `cau-hoi/hanh-phuc.md:107` | `cau-hoi/hanh-phuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 20,1% | đổi thành `[[pp:phuc-loi-well-being.khac]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/hanh-phuc.md:107` | `cau-hoi/hanh-phuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 53,2% | đổi thành `[[pp:phuc-loi-well-being.danh-sach-khach-quan]]%` |
| `cau-hoi/hanh-phuc.md:109` | `cau-hoi/hanh-phuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 12,7% | đổi thành `[[pp:phuc-loi-well-being.khoai-lac-trai-nghiem]]%` |
| `cau-hoi/hanh-phuc.md:109` | `cau-hoi/hanh-phuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 13,3% | đổi thành `[[pp:may-trai-nghiem-co-vao-khong.co]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/khi-hau-trach-nhiem.md:15` | `cau-hoi/khi-hau-trach-nhiem.md#_dau` | `ngoai-kho` | 71% | kho không có số này: đối chiếu tools/philpapers-2020.md |
| `cau-hoi/khi-hau-trach-nhiem.md:16` | `cau-hoi/khi-hau-trach-nhiem.md#_dau` | `go-tay` | 42,2% | đổi thành `[[pp:dao-duc-moi-truong.lay-con-nguoi-lam-trung-tam]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/khi-hau-trach-nhiem.md:16` | `cau-hoi/khi-hau-trach-nhiem.md#_dau` | `go-tay` | 50,7% | đổi thành `[[pp:dao-duc-moi-truong.khong-lay-con-nguoi-lam-trung-tam]]%` |
| `cau-hoi/khi-hau-trach-nhiem.md:112` | `cau-hoi/khi-hau-trach-nhiem.md#tu-kiem-tra` | `quiz` | câu 2: 71% | số không có trong kho: đối chiếu tools/philpapers-2020.md |
| `cau-hoi/khoa-hoc.md:16` | `cau-hoi/khoa-hoc.md#_dau` | `go-tay` | 72,4% | đổi thành `[[pp:khoa-hoc.hien-thuc-luan-khoa-hoc]]%` |
| `cau-hoi/khoa-hoc.md:130` | `cau-hoi/khoa-hoc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 17,7% | đổi thành `[[pp:gia-tri-trong-khoa-hoc.nhat-thiet-trung-lap-gia-tri]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/khoa-hoc.md:130` | `cau-hoi/khoa-hoc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 72,4% | đổi thành `[[pp:khoa-hoc.hien-thuc-luan-khoa-hoc]]%` |
| `cau-hoi/linh-hon.md:15` | `cau-hoi/linh-hon.md#_dau` | `go-tay` | 51,9% | đổi thành `[[pp:tam-tri.vat-ly-luan]]%` |
| `cau-hoi/linh-hon.md:17` | `cau-hoi/linh-hon.md#_dau` | `go-tay` | 62,4% | đổi thành `[[pp:van-de-kho-cua-y-thuc-co-ton-tai-khong.co]]%` |
| `cau-hoi/linh-hon.md:112` | `cau-hoi/linh-hon.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 32,1% | đổi thành `[[pp:tam-tri.phi-vat-ly-luan]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/linh-hon.md:112` | `cau-hoi/linh-hon.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 51,9% | đổi thành `[[pp:tam-tri.vat-ly-luan]]%` |
| `cau-hoi/linh-hon.md:114` | `cau-hoi/linh-hon.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 29,8% | đổi thành `[[pp:van-de-kho-cua-y-thuc-co-ton-tai-khong.khong]]%` |
| `cau-hoi/linh-hon.md:114` | `cau-hoi/linh-hon.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 62,4% | đổi thành `[[pp:van-de-kho-cua-y-thuc-co-ton-tai-khong.co]]%` |
| `cau-hoi/linh-hon.md:116` | `cau-hoi/linh-hon.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 22,0% | đổi thành `[[pp:y-thuc-ly-thuyet.nhi-nguyen-luan]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/linh-hon.md:116` | `cau-hoi/linh-hon.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 7,5% | đổi thành `[[pp:y-thuc-ly-thuyet.toan-tam-luan-panpsychism]]%` |
| `cau-hoi/linh-hon.md:118` | `cau-hoi/linh-hon.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 62,4% | đổi thành `[[pp:van-de-kho-cua-y-thuc-co-ton-tai-khong.co]]%` |
| `cau-hoi/luan-chung-ton-giao.md:17` | `cau-hoi/luan-chung-ton-giao.md#_dau` | `go-tay` | 18,9% | đổi thành `[[pp:thuong-de.huu-than]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/luan-chung-ton-giao.md:17` | `cau-hoi/luan-chung-ton-giao.md#_dau` | `go-tay` | 20,9% | đổi thành `[[pp:luan-chung-cho-su-ton-tai-cua-thuong-de-manh-nhat.vu-tru-luan]]%` |
| `cau-hoi/luan-chung-ton-giao.md:17` | `cau-hoi/luan-chung-ton-giao.md#_dau` | `go-tay` | 66,9% | đổi thành `[[pp:thuong-de.vo-than]]%` |
| `cau-hoi/luan-chung-ton-giao.md:17` | `cau-hoi/luan-chung-ton-giao.md#_dau` | `go-tay` | 8,9% | đổi thành `[[pp:luan-chung-cho-su-ton-tai-cua-thuong-de-manh-nhat.ban-the-luan]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/luan-chung-ton-giao.md:127` | `cau-hoi/luan-chung-ton-giao.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 25,2% | đổi thành `[[pp:luan-chung-cho-su-ton-tai-cua-thuong-de-manh-nhat.khac]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/luan-chung-ton-giao.md:127` | `cau-hoi/luan-chung-ton-giao.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 8,9% | đổi thành `[[pp:luan-chung-cho-su-ton-tai-cua-thuong-de-manh-nhat.ban-the-luan]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/mo-phong.md:94` | `cau-hoi/mo-phong.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 27,5% | đổi thành `[[pp:tai-tam-tri-len-may-nao-duoc-thay-bang-ban-mo-phong-so.song-sot]]%` |
| `cau-hoi/mo-phong.md:94` | `cau-hoi/mo-phong.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 54,2% | đổi thành `[[pp:tai-tam-tri-len-may-nao-duoc-thay-bang-ban-mo-phong-so.chet]]%` |
| `cau-hoi/nghe-thuat.md:135` | `cau-hoi/nghe-thuat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 37,2% | đổi thành `[[pp:gia-tri-tham-my.chu-quan/loai-tru]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/nghe-thuat.md:135` | `cau-hoi/nghe-thuat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 37,2% | đổi thành `[[pp:gia-tri-tham-my.chu-quan/loai-tru]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/nhan-qua-ban-chat.md:105` | `cau-hoi/nhan-qua-ban-chat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 37,2% | đổi thành `[[pp:nhan-qua.phan-thuc-tao-khac-biet]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/nhan-qua-ban-chat.md:105` | `cau-hoi/nhan-qua-ban-chat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 4,1% | đổi thành `[[pp:nhan-qua.khong-ton-tai]]%` |
| `cau-hoi/nhan-qua-ban-chat.md:107` | `cau-hoi/nhan-qua-ban-chat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 31,3% | đổi thành `[[pp:quy-luat-tu-nhien.kieu-hume-quy-luat-chi-tom-tat-cac-khuon-mau-deu-dan]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/nhan-qua-ban-chat.md:107` | `cau-hoi/nhan-qua-ban-chat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 54,3% | đổi thành `[[pp:quy-luat-tu-nhien.phi-hume]]%` |
| `cau-hoi/noi-doi.md:17` | `cau-hoi/noi-doi.md#_dau` | `go-tay` | 30,6% | đổi thành `[[pp:dao-duc-hoc-chuan-tac.he-qua-luan]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/noi-doi.md:17` | `cau-hoi/noi-doi.md#_dau` | `go-tay` | 32,1% | đổi thành `[[pp:dao-duc-hoc-chuan-tac.nghia-vu-luan]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/noi-doi.md:17` | `cau-hoi/noi-doi.md#_dau` | `go-tay` | 37,0% | đổi thành `[[pp:dao-duc-hoc-chuan-tac.dao-duc-hoc-duc-hanh]]%` |
| `cau-hoi/noi-doi.md:121` | `cau-hoi/noi-doi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 54,6% | đổi thành `[[pp:nguyen-tac-dao-duc.pho-quat-luan-dao-duc-generalism]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/noi-doi.md:121` | `cau-hoi/noi-doi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 54,6% | đổi thành `[[pp:nguyen-tac-dao-duc.pho-quat-luan-dao-duc-generalism]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/nu-quyen.md:16` | `cau-hoi/nu-quyen.md#_dau` | `go-tay` | 63,1% | đổi thành `[[pp:gioi-gender-thuoc-loai-gi.xa-hoi]]%` |
| `cau-hoi/nu-quyen.md:104` | `cau-hoi/nu-quyen.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 43,0% | đổi thành `[[pp:gioi-gender-thuoc-loai-gi.xa-hoi/loai-tru]]%` |
| `cau-hoi/pho-quat.md:16` | `cau-hoi/pho-quat.md#_dau` | `go-tay` | 11,5% | đổi thành `[[pp:tinh-chat-properties.lop-tap-hop]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/pho-quat.md:16` | `cau-hoi/pho-quat.md#_dau` | `go-tay` | 15,3% | đổi thành `[[pp:tinh-chat-properties.trope-tinh-chat-ca-biet]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/pho-quat.md:16` | `cau-hoi/pho-quat.md#_dau` | `go-tay` | 19,8% | đổi thành `[[pp:tinh-chat-properties.pho-quat-sieu-viet-kieu-platon]]%` |
| `cau-hoi/pho-quat.md:16` | `cau-hoi/pho-quat.md#_dau` | `go-tay` | 20,6% | đổi thành `[[pp:tinh-chat-properties.pho-quat-noi-tai-kieu-aristotle]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/pho-quat.md:134` | `cau-hoi/pho-quat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 11,5% | đổi thành `[[pp:tinh-chat-properties.lop-tap-hop]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/pho-quat.md:134` | `cau-hoi/pho-quat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 15,3% | đổi thành `[[pp:tinh-chat-properties.trope-tinh-chat-ca-biet]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/pho-quat.md:134` | `cau-hoi/pho-quat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 29,1% | đổi thành `[[pp:tinh-chat-properties.khac]]%` |
| `cau-hoi/pho-quat.md:134` | `cau-hoi/pho-quat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 8,1% | đổi thành `[[pp:tinh-chat-properties.khong-ton-tai]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/pho-quat.md:134` | `cau-hoi/pho-quat.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 40% | kho không có số này: đối chiếu tools/philpapers-2020.md |
| `cau-hoi/sieu-dao-duc.md:16` | `cau-hoi/sieu-dao-duc.md#_dau` | `go-tay` | 26,1% | đổi thành `[[pp:sieu-dao-duc-hoc-meta-ethics.phan-hien-thuc-luan-dao-duc]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/sieu-dao-duc.md:16` | `cau-hoi/sieu-dao-duc.md#_dau` | `go-tay` | 62,1% | đổi thành `[[pp:sieu-dao-duc-hoc-meta-ethics.hien-thuc-luan-dao-duc-moral-realism]]%` |
| `cau-hoi/sieu-dao-duc.md:133` | `cau-hoi/sieu-dao-duc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 62,1% | đổi thành `[[pp:sieu-dao-duc-hoc-meta-ethics.hien-thuc-luan-dao-duc-moral-realism]]%` |
| `cau-hoi/sieu-dao-duc.md:133` | `cau-hoi/sieu-dao-duc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 69,3% | đổi thành `[[pp:phan-doan-dao-duc.thuyet-nhan-thuc-cognitivism]]%` |
| `cau-hoi/tai-san-rieng.md:16` | `cau-hoi/tai-san-rieng.md#_dau` | `go-tay` | 13,4% | đổi thành `[[pp:triet-hoc-chinh-tri.chu-nghia-tu-do-ca-nhan-libertarianism]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/tai-san-rieng.md:16` | `cau-hoi/tai-san-rieng.md#_dau` | `go-tay` | 29,5% | đổi thành `[[pp:chinh-tri-kinh-te.chu-nghia-tu-ban]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/tai-san-rieng.md:16` | `cau-hoi/tai-san-rieng.md#_dau` | `go-tay` | 53,0% | đổi thành `[[pp:chinh-tri-kinh-te.chu-nghia-xa-hoi]]%` |
| `cau-hoi/tai-san-rieng.md:109` | `cau-hoi/tai-san-rieng.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 13,4% | đổi thành `[[pp:triet-hoc-chinh-tri.chu-nghia-tu-do-ca-nhan-libertarianism]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/tam-tri-va-ai.md:121` | `cau-hoi/tam-tri-va-ai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 39% | đổi thành `[[pp:bai-toan-newcomb.lay-hai-hop]]%` |
| `cau-hoi/tam-tri-va-ai.md:121` | `cau-hoi/tam-tri-va-ai.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 27% | kho không có số này: đối chiếu tools/philpapers-2020.md; gần `[[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-tuong-lai/bac-bo]]` (26,8) |
| `cau-hoi/tam-tri-va-ai.md:154` | `cau-hoi/tam-tri-va-ai.md#tu-kiem-tra` | `quiz` | câu 5: 52% | số không có trong kho: đối chiếu tools/philpapers-2020.md; gần `[[pp:tam-tri.vat-ly-luan]]` (51,9) |
| `cau-hoi/tam-tri-va-ai.md:154` | `cau-hoi/tam-tri-va-ai.md#tu-kiem-tra` | `quiz` | câu 5: 62% | số không có trong kho: đối chiếu tools/philpapers-2020.md; gần `[[pp:van-de-kho-cua-y-thuc-co-ton-tai-khong.co]]` (62,4) |
| `cau-hoi/tam-tri-va-ai.md:154` | `cau-hoi/tam-tri-va-ai.md#tu-kiem-tra` | `quiz` | câu 5: 67% | số không có trong kho: đối chiếu tools/philpapers-2020.md; gần `[[pp:can-phong-tieng-trung.khong-hieu]]` (67,1) |
| `cau-hoi/thoi-gian.md:16` | `cau-hoi/thoi-gian.md#_dau` | `go-tay` | 17,0% | đổi thành `[[pp:ban-the-luan-thoi-gian.thuyet-khoi-dang-lon]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/thoi-gian.md:16` | `cau-hoi/thoi-gian.md#_dau` | `go-tay` | 18,4% | đổi thành `[[pp:ban-the-luan-thoi-gian.hien-tai-luan]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/thoi-gian.md:16` | `cau-hoi/thoi-gian.md#_dau` | `go-tay` | 27,2% | đổi thành `[[pp:thoi-gian.thuyet-a]]%` |
| `cau-hoi/thoi-gian.md:16` | `cau-hoi/thoi-gian.md#_dau` | `go-tay` | 38,2% | đổi thành `[[pp:thoi-gian.thuyet-b]]%` |
| `cau-hoi/thoi-gian.md:16` | `cau-hoi/thoi-gian.md#_dau` | `go-tay` | 39,9% | đổi thành `[[pp:ban-the-luan-thoi-gian.vinh-cuu-luan]]%` |
| `cau-hoi/trach-nhiem.md:142` | `cau-hoi/trach-nhiem.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 11,2% | đổi thành `[[pp:tu-do-y-chi.khong-co-tu-do-y-chi]]%` |
| `cau-hoi/trach-nhiem.md:142` | `cau-hoi/trach-nhiem.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 18,8% | đổi thành `[[pp:phuong-phap-triet-hoc-chinh-tri.khac]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/trach-nhiem.md:142` | `cau-hoi/trach-nhiem.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 59,2% | đổi thành `[[pp:tu-do-y-chi.tuong-thich-luan]]%` |
| `cau-hoi/tri-thuc.md:165` | `cau-hoi/tri-thuc.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 5% | đổi thành `[[pp:trai-nghiem-tri-giac.thuyet-du-lieu-giac-quan]]%` |
| `cau-hoi/tu-do-y-chi.md:165` | `cau-hoi/tu-do-y-chi.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `ngoai-kho` | 63% | kho không có số này: đối chiếu tools/philpapers-2020.md; gần `[[pp:phai-keo-theo-co-the-ought-implies-can.co]]` (62,9) |
| `cau-hoi/van-de-su-du.md:121` | `cau-hoi/van-de-su-du.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 18,9% | đổi thành `[[pp:dap-lai-hoai-nghi-ve-the-gioi-ben-ngoai-manh-nhat.ngoai-tai-luan-tri-thuc]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/van-de-su-du.md:121` | `cau-hoi/van-de-su-du.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 66,9% | đổi thành `[[pp:thuong-de.vo-than]]%` |
| `cau-hoi/van-de-tam-tri.md:106` | `cau-hoi/van-de-tam-tri.md#cac-lap-truong-chinh` | `go-tay` | 16,4% | đổi thành `[[pp:zombie-triet-hoc.khong-the-hinh-dung]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/van-de-tam-tri.md:106` | `cau-hoi/van-de-tam-tri.md#cac-lap-truong-chinh` | `go-tay` | 36,5% | đổi thành `[[pp:zombie-triet-hoc.hinh-dung-duoc-nhung-khong-kha-huu-ve-sieu-hinh]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/vu-tru-khoi-dau.md:16` | `cau-hoi/vu-tru-khoi-dau.md#_dau` | `go-tay` | 20,9% | đổi thành `[[pp:luan-chung-cho-su-ton-tai-cua-thuong-de-manh-nhat.vu-tru-luan]]%` |
| `cau-hoi/vu-tru-khoi-dau.md:16` | `cau-hoi/vu-tru-khoi-dau.md#_dau` | `go-tay` | 32,1% | đổi thành `[[pp:tinh-chinh-vu-tru-giai-thich-bang-gi.su-that-tran-trui-khong-can-giai-thich]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/vu-tru-khoi-dau.md:114` | `cau-hoi/vu-tru-khoi-dau.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 20,9% | đổi thành `[[pp:luan-chung-cho-su-ton-tai-cua-thuong-de-manh-nhat.vu-tru-luan]]%` |
| `cau-hoi/vu-tru-khoi-dau.md:116` | `cau-hoi/vu-tru-khoi-dau.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 15,1% | đổi thành `[[pp:tinh-chinh-vu-tru-giai-thich-bang-gi.da-vu-tru]]%` (hoặc 4 khóa khác cùng giá trị) |
| `cau-hoi/vu-tru-khoi-dau.md:116` | `cau-hoi/vu-tru-khoi-dau.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 17,3% | đổi thành `[[pp:tinh-chinh-vu-tru-giai-thich-bang-gi.thiet-ke]]%` |
| `cau-hoi/vu-tru-khoi-dau.md:116` | `cau-hoi/vu-tru-khoi-dau.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 21,7% | đổi thành `[[pp:tinh-chinh-vu-tru-giai-thich-bang-gi.khong-co-tinh-chinh]]%` |
| `cau-hoi/vu-tru-khoi-dau.md:116` | `cau-hoi/vu-tru-khoi-dau.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 32,1% | đổi thành `[[pp:tinh-chinh-vu-tru-giai-thich-bang-gi.su-that-tran-trui-khong-can-giai-thich]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/vu-tru-khoi-dau.md:116` | `cau-hoi/vu-tru-khoi-dau.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 35,9% | đổi thành `[[pp:nguyen-ly-ly-do-day-du.dung]]%` (hoặc 1 khóa khác cùng giá trị) |
| `cau-hoi/vu-tru-khoi-dau.md:116` | `cau-hoi/vu-tru-khoi-dau.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 45,7% | đổi thành `[[pp:nguyen-ly-ly-do-day-du.sai]]%` |
| `cau-hoi/y-nghia-song.md:141` | `cau-hoi/y-nghia-song.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 16,1% | đổi thành `[[pp:y-nghia-cuoc-song.khong-ton-tai]]%` (hoặc 2 khóa khác cùng giá trị) |
| `cau-hoi/y-nghia-song.md:141` | `cau-hoi/y-nghia-song.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 32,1% | đổi thành `[[pp:y-nghia-cuoc-song.khach-quan]]%` (hoặc 3 khóa khác cùng giá trị) |
| `cau-hoi/y-nghia-song.md:141` | `cau-hoi/y-nghia-song.md#gioi-triet-hoc-ngay-nay-nghi-gi` | `go-tay` | 33,0% | đổi thành `[[pp:y-nghia-cuoc-song.chu-quan]]%` (hoặc 1 khóa khác cùng giá trị) |
| `docs/assets/data/thi-nghiem.json` | `thi-nghiem/tau-theseus` | `du-lieu` | 30,1% | nên đọc từ kho (đổi thành `[[pp:buc-tuong-va-khoi-dat-set.mot-vat]]%` (hoặc 1 khóa khác cùng giá trị)) |
| `docs/assets/data/thi-nghiem.json` | `thi-nghiem/tau-theseus` | `du-lieu` | 41,8% | nên đọc từ kho (đổi thành `[[pp:buc-tuong-va-khoi-dat-set.hai-vat]]%`) |
| `tools/figures.py:877` | — | `du-lieu` | 76,9% | nên đọc từ kho (đổi thành `[[pp:may-trai-nghiem-co-vao-khong.khong]]%`) |
| `tools/figures.py:947` | — | `du-lieu` | 30,6% | nên đọc từ kho (đổi thành `[[pp:dao-duc-hoc-chuan-tac.he-qua-luan]]%` (hoặc 3 khóa khác cùng giá trị)) |
| `tools/figures.py:947` | — | `du-lieu` | 32,1% | nên đọc từ kho (đổi thành `[[pp:dao-duc-hoc-chuan-tac.nghia-vu-luan]]%` (hoặc 3 khóa khác cùng giá trị)) |
| `tools/figures.py:947` | — | `du-lieu` | 37,0% | nên đọc từ kho (đổi thành `[[pp:dao-duc-hoc-chuan-tac.dao-duc-hoc-duc-hanh]]%`) |
| `tools/figures.py:952` | — | `du-lieu` | 11,2% | nên đọc từ kho (đổi thành `[[pp:tu-do-y-chi.khong-co-tu-do-y-chi]]%`) |
| `tools/figures.py:952` | — | `du-lieu` | 18,8% | nên đọc từ kho (đổi thành `[[pp:phuong-phap-triet-hoc-chinh-tri.khac]]%` (hoặc 1 khóa khác cùng giá trị)) |
| `tools/figures.py:952` | — | `du-lieu` | 59,2% | nên đọc từ kho (đổi thành `[[pp:tu-do-y-chi.tuong-thich-luan]]%`) |
| `tools/figures.py:957` | — | `du-lieu` | 23,6% | nên đọc từ kho (đổi thành `[[pp:phan-tich-khai-niem-tri-thuc.niem-tin-dung-duoc-bien-minh-jtb]]%` (hoặc 1 khóa khác cùng giá trị)) |
| `tools/figures.py:957` | — | `du-lieu` | 30,6% | nên đọc từ kho (đổi thành `[[pp:dao-duc-hoc-chuan-tac.he-qua-luan]]%` (hoặc 3 khóa khác cùng giá trị)) |
| `tools/figures.py:957` | — | `du-lieu` | 32,2% | nên đọc từ kho (đổi thành `[[pp:phan-tich-khai-niem-tri-thuc.mot-phan-tich-khac]]%`) |
| `tools/figures.py:1058` | — | `du-lieu` | 76,9% | nên đọc từ kho (đổi thành `[[pp:may-trai-nghiem-co-vao-khong.khong]]%`) |
