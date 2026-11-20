# Kiểm mẫu 5.8 (agent kiểm thứ hai)

Làm đúng như hướng dẫn kiểm lượt 1: `/Users/mitu/Desktop/work/projects/logos/ban-giao/dot-5.8/huong-dan/HUONG-DAN-KIEM-5.8.md`. Có các điểm khác sau.

- **Độc lập.** KHÔNG mở `verification/evidence/`, `verification/mau/5.8/` của agent khác, nhật ký hay git log. Bạn kiểm như thể chưa ai kiểm đơn vị này.
- **Nơi ghi.** Ghi bằng chứng vào `verification/mau/5.8/<khóa, thay "/" và "#" bằng "__">.json`, ví dụ `verification/mau/5.8/cau-hoi__tri-thuc.md__nguon.json`. Cùng schema, `checked_on` là ngày kiểm, `checker` là mã của bạn. `hash` là mã băm hiện tại.
- **Kỹ.** Mở nguồn thật cho mọi dữ kiện: văn bản gốc, SEP bản lưu fall2026, IEP, Wikisource, Perseus, Gutenberg qua mirror `gutenberg.pglaf.org`, Internet Archive, Crossref…
  - ctext.org chặn bot: theo quyết định 34 trong KE-HOACH.md, claim "URL đúng" được ghi `dung` khi nội dung đã đối chiếu ở bản khác và URL đúng mẫu. Không vượt kiểm tra chống bot.
  - Kho đã đóng băng (`kb`) được dùng như hướng dẫn lượt 1.
  - Link nội bộ: mở trang trên `https://mtuann.github.io/logos/...`.
  - Không dùng Wikipedia làm nguồn. Không dùng trí nhớ.
- **Mức lỗi** đúng như `ban-giao/kiem-chung.md`. Mục tiêu của mẫu là tìm lỗi `nghiem-trong` mà lượt kiểm đầu bỏ sót, nên đừng bỏ qua dữ kiện nào.
- **Thư mục tạm.** Dùng `${TMPDIR:-/tmp}/logos-5.8/<mã của bạn>/`.
- **Phạm vi.** Không sửa file nào khác, không commit.

Báo cáo cuối gồm:
- mỗi khóa: `result`;
- mọi claim `sai`: khóa, mức, mô tả một dòng, `fix`;
- mọi claim `chua-kiem-duoc` kèm lý do.

Thêm cho 5.8:
- Mọi `quote` phải là nguyên văn trên trang bạn tải trong phiên này (curl, không giả User-Agent). Tự so bằng script trước khi ghi file.
- Khối thời sự `[[thoi-su:…]]` không kiểm ở đây, chỉ kiểm câu bao quanh nó.
- Trang đã sửa trong hôm nay có thể chưa lên site đã deploy. Khi đó đọc file `docs/…` trong repo.
