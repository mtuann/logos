# Đo axe trên trình duyệt thật

Sinh bằng `AXE_REPORT=1 npm run test:real` (Chromium qua Playwright, axe-core 4.13.0, WCAG 2.2 AA, cả trang).
10 trang mẫu × 2 cỡ màn hình × 2 chế độ màu = 40 lần quét.

**1430 phần tử vi phạm**, 4 luật.

| Luật | Mức | Nghĩa | Phần tử (cộng mọi lần quét) | Trang |
|---|---|---|---:|---|
| `link-in-text-block` | serious | Links must be distinguishable without relying on color | 1320 | /logos/, /logos/bat-dau/, /logos/cau-hoi/tri-thuc/, /logos/cau-hoi/tu-do-y-chi/, /logos/cong-cu/lap-luan-la-gi/, /logos/doc/platon-bien-ho/, /logos/luyen-tap/nguy-bien/, /logos/them/tu-dien/, /logos/triet-gia/kant/ |
| `color-contrast` | serious | Elements must meet minimum color contrast ratio thresholds | 58 | /logos/, /logos/bat-dau/, /logos/cau-hoi/tri-thuc/, /logos/cau-hoi/tu-do-y-chi/, /logos/cong-cu/lap-luan-la-gi/, /logos/doc/platon-bien-ho/, /logos/lich-su/dong-thoi-gian/, /logos/luyen-tap/nguy-bien/, /logos/them/tu-dien/, /logos/triet-gia/kant/ |
| `aria-progressbar-name` | serious | ARIA progressbar nodes must have an accessible name | 40 | /logos/, /logos/bat-dau/, /logos/cau-hoi/tri-thuc/, /logos/cau-hoi/tu-do-y-chi/, /logos/cong-cu/lap-luan-la-gi/, /logos/doc/platon-bien-ho/, /logos/lich-su/dong-thoi-gian/, /logos/luyen-tap/nguy-bien/, /logos/them/tu-dien/, /logos/triet-gia/kant/ |
| `target-size` | serious | All touch targets must be 24px large, or leave sufficient space | 12 | /logos/cau-hoi/tu-do-y-chi/, /logos/triet-gia/kant/ |

## Từng lần quét

| Trang | Màn hình | Màu | Vi phạm (luật: số phần tử) |
|---|---|---|---|
| /logos/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 1, `link-in-text-block`: 5 |
| /logos/ | may-tinh | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 5 |
| /logos/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 1, `link-in-text-block`: 5 |
| /logos/ | dien-thoai | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 5 |
| /logos/bat-dau/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 13 |
| /logos/bat-dau/ | may-tinh | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 13 |
| /logos/bat-dau/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 13 |
| /logos/bat-dau/ | dien-thoai | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 13 |
| /logos/cau-hoi/tri-thuc/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 25 |
| /logos/cau-hoi/tri-thuc/ | may-tinh | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 25 |
| /logos/cau-hoi/tri-thuc/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 25 |
| /logos/cau-hoi/tri-thuc/ | dien-thoai | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 25 |
| /logos/cau-hoi/tu-do-y-chi/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 20, `target-size`: 2 |
| /logos/cau-hoi/tu-do-y-chi/ | may-tinh | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 20, `target-size`: 2 |
| /logos/cau-hoi/tu-do-y-chi/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 20 |
| /logos/cau-hoi/tu-do-y-chi/ | dien-thoai | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 20 |
| /logos/cong-cu/lap-luan-la-gi/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 8 |
| /logos/cong-cu/lap-luan-la-gi/ | may-tinh | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 8 |
| /logos/cong-cu/lap-luan-la-gi/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 8 |
| /logos/cong-cu/lap-luan-la-gi/ | dien-thoai | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 8 |
| /logos/lich-su/dong-thoi-gian/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 3 |
| /logos/lich-su/dong-thoi-gian/ | may-tinh | dark | `aria-progressbar-name`: 1 |
| /logos/lich-su/dong-thoi-gian/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 3 |
| /logos/lich-su/dong-thoi-gian/ | dien-thoai | dark | `aria-progressbar-name`: 1 |
| /logos/doc/platon-bien-ho/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 14 |
| /logos/doc/platon-bien-ho/ | may-tinh | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 14 |
| /logos/doc/platon-bien-ho/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 14 |
| /logos/doc/platon-bien-ho/ | dien-thoai | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 14 |
| /logos/triet-gia/kant/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 6, `target-size`: 4 |
| /logos/triet-gia/kant/ | may-tinh | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 6, `target-size`: 4 |
| /logos/triet-gia/kant/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 6 |
| /logos/triet-gia/kant/ | dien-thoai | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 6 |
| /logos/them/tu-dien/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 238 |
| /logos/them/tu-dien/ | may-tinh | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 238 |
| /logos/them/tu-dien/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 3, `link-in-text-block`: 238 |
| /logos/them/tu-dien/ | dien-thoai | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 238 |
| /logos/luyen-tap/nguy-bien/ | may-tinh | light | `aria-progressbar-name`: 1, `color-contrast`: 4, `link-in-text-block`: 1 |
| /logos/luyen-tap/nguy-bien/ | may-tinh | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 1 |
| /logos/luyen-tap/nguy-bien/ | dien-thoai | light | `aria-progressbar-name`: 1, `color-contrast`: 4, `link-in-text-block`: 1 |
| /logos/luyen-tap/nguy-bien/ | dien-thoai | dark | `aria-progressbar-name`: 1, `link-in-text-block`: 1 |
