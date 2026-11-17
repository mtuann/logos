# Báo cáo linter link triết gia

Sinh bằng `python tools/lint_lien_ket.py --write`. Phạm vi: Lõi viết tay. Lần đầu nhắc một triết gia đã có hồ sơ thì đặt link tới trang hồ sơ (README, "Thêm nội dung"); sửa trong đợt con của trang (ban-giao/dot-5.md).

**15 chỗ** ở **14 trang/file**. Chế độ cảnh báo: chưa chặn CI.

| Luật | Nghĩa | Số chỗ |
|---|---|---:|
| `thieu-link` | bài nhắc triết gia đã có hồ sơ mà không link tới trang hồ sơ | 15 |
| `mien-thua` | mục miễn không còn khớp chỗ nào | 0 |

## Chi tiết

| Vị trí | Đơn vị | Luật | Tìm thấy | Ghi chú |
|---|---|---|---|---|
| `bat-dau/lo-trinh.md:30` | `bat-dau/lo-trinh.md#1-tu-duy-ro-rang` | `thieu-link` | Socrates (socrates) | đặt link ở lần nhắc đầu: [Socrates](../triet-gia/socrates.md) |
| `cau-hoi/cai-chet.md:168` | `cau-hoi/cai-chet.md#doc-van-ban-goc` | `thieu-link` | Marcus Aurelius (marcus-aurelius) | đặt link ở lần nhắc đầu: [Marcus Aurelius](../triet-gia/marcus-aurelius.md) |
| `cau-hoi/cai-chet.md:168` | `cau-hoi/cai-chet.md#doc-van-ban-goc` | `thieu-link` | Socrates (socrates) | đặt link ở lần nhắc đầu: [Socrates](../triet-gia/socrates.md) |
| `cau-hoi/chien-tranh-chinh-dang.md:115` | `cau-hoi/chien-tranh-chinh-dang.md#doc-van-ban-goc` | `thieu-link` | Mặc Tử (mac-tu) | đặt link ở lần nhắc đầu: [Mặc Tử](../triet-gia/mac-tu.md) |
| `cau-hoi/dan-chu.md:145` | `cau-hoi/dan-chu.md#doc-van-ban-goc` | `thieu-link` | Kant (kant) | đặt link ở lần nhắc đầu: [Immanuel Kant](../triet-gia/kant.md) |
| `cau-hoi/hanh-phuc.md:121` | `cau-hoi/hanh-phuc.md#lien-he-doi-song` | `thieu-link` | Epictetus (epictetus) | đặt link ở lần nhắc đầu: [Epictetus](../triet-gia/epictetus.md) |
| `cau-hoi/khoa-hoc.md:166` | `cau-hoi/khoa-hoc.md#doc-van-ban-goc` | `thieu-link` | Hume (hume) | đặt link ở lần nhắc đầu: [David Hume](../triet-gia/hume.md) |
| `cau-hoi/mo-phong.md:106` | `cau-hoi/mo-phong.md#lien-he-doi-song` | `thieu-link` | Trang Tử (trang-tu) | đặt link ở lần nhắc đầu: [Trang Tử](../triet-gia/trang-tu.md) |
| `cau-hoi/tu-do-ngon-luan.md:125` | `cau-hoi/tu-do-ngon-luan.md#doc-van-ban-goc` | `thieu-link` | Kant (kant) | đặt link ở lần nhắc đầu: [Immanuel Kant](../triet-gia/kant.md) |
| `cau-hoi/tu-do-y-chi.md:194` | `cau-hoi/tu-do-y-chi.md#doc-van-ban-goc` | `thieu-link` | Sartre (sartre) | đặt link ở lần nhắc đầu: [Sartre](../triet-gia/sartre.md) |
| `cau-hoi/y-nghia-song.md:170` | `cau-hoi/y-nghia-song.md#doc-van-ban-goc` | `thieu-link` | Sartre (sartre) | đặt link ở lần nhắc đầu: [Sartre](../triet-gia/sartre.md) |
| `cong-cu/suy-dien.md:94` | `cong-cu/suy-dien.md#nhung-khuon-dang-tin` | `thieu-link` | Socrates (socrates) | đặt link ở lần nhắc đầu: [Socrates](../triet-gia/socrates.md) |
| `doc/aurelius-suy-tuong.md:156` | `doc/aurelius-suy-tuong.md#doc-tiep` | `thieu-link` | Heidegger (heidegger) | đặt link ở lần nhắc đầu: [Heidegger](../triet-gia/heidegger.md) |
| `doc/luan-ngu.md:154` | `doc/luan-ngu.md#doc-tiep` | `thieu-link` | Kant (kant) | đặt link ở lần nhắc đầu: [Immanuel Kant](../triet-gia/kant.md) |
| `lich-su/trung-hoa.md:53` | `lich-su/trung-hoa.md#lao-tu-va-trang-tu-dao-khong-noi-duoc` | `thieu-link` | Lão Tử (lao-tu) | đặt link ở lần nhắc đầu: [Lão Tử](../triet-gia/lao-tu.md) |
