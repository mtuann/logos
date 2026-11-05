# Kiểm chứng một đơn vị: quy trình và định dạng

Dùng cho agent kiểm (đợt 5, mọi PR Mở rộng) và cho LLM chat được giao kiểm. Người kiểm không sửa nội dung bài; chỉ ghi bằng chứng.

## Việc phải làm

1. Đọc đơn vị. Liệt kê mọi khẳng định kiểm được, chia hai loại:
    - `du-kien`: năm, tên người, tên tác phẩm, trích dẫn nguyên văn, số liệu, sự kiện.
    - `dien-giai`: "X lập luận rằng…", "lập trường Y cho rằng…", tóm tắt một thí nghiệm tư duy.
2. Với mỗi khẳng định: mở nguồn, so sánh, kết luận `dung`, `sai` hoặc `chua-kiem-duoc`. Nếu `sai`, đề xuất câu sửa và mức lỗi.
3. Chấm checklist ngữ nghĩa năm câu cho cả đơn vị.
4. Ghi file bằng chứng ngay sau khi xong đơn vị.

## Nguồn được dùng, theo thứ tự ưu tiên

1. **SEP, bản lưu theo quý**: `https://plato.stanford.edu/archives/<mùa><năm>/entries/<mục>/`, mùa là `win`, `spr`, `sum`, `fall`. Bản lưu là bản cố định, tạo mỗi ba tháng (ngày 21 các tháng 3, 6, 9, 12), nên trích dẫn không bị đổi về sau.
2. **IEP** (`iep.utm.edu`).
3. **Văn bản gốc**: Project Gutenberg (ghi số ebook), Wikisource, ctext.org (ghi chương), CBETA (kinh Phật).
4. **Bài báo gốc qua DOI**; sách học thuật (ghi trang).
5. **Số liệu PhilPapers 2020**: chỉ `tools/philpapers-2020.md` — % "chấp nhận hoặc nghiêng về", một chữ số thập phân, dấu phẩy; phân biệt câu chính (Bảng 1) và câu bổ sung (Bảng 2).
6. **Lịch sử Việt Nam**: *Đại Việt sử ký toàn thư* (ghi quyển, đối chiếu chữ Hán khi có), công trình của Viện Hán Nôm và Viện Văn học. Wikipedia chỉ để tìm nguồn, không phải nguồn.

Không dùng: blog không rõ tác giả, trang tổng hợp, trang "danh ngôn", câu trả lời của AI.

## Checklist ngữ nghĩa

| Khóa | Câu hỏi |
|---|---|
| `dung-nguon` | Mỗi lập trường được trình bày đúng như nguồn nói? |
| `manh-nhat` | Lập trường ở dạng mạnh nhất, không phải người rơm? |
| `phan-bac` | Có phản bác chính và cách lập trường đáp lại? |
| `trung-lap` | Bài không kết luận thay người đọc ở câu hỏi còn mở? |
| `thuat-ngu` | Dùng đúng bảng thuật ngữ bắt buộc; lần đầu có *English term*? |

## Mức lỗi

- `nghiem-trong`: sai năm, sai người, sai trích dẫn, sai số liệu, quiz sai đáp án, trình bày sai một lập trường.
- `vua`: đơn giản hóa gây hiểu lầm, sai thuật ngữ bắt buộc, rủi ro bản quyền, nội dung có hạn dùng nằm trong thân bài Lõi.
- `nhe`: chính tả, câu vụng.

## File bằng chứng

Đường dẫn: `verification/evidence/<khóa đơn vị, thay "/" và "#" bằng "__">.json`, ví dụ `verification/evidence/cau-hoi__tri-thuc.md__cac-lap-truong-chinh.json`.

```json
{
  "unit": "cau-hoi/tri-thuc.md#cac-lap-truong-chinh",
  "hash": null,
  "checked_on": "2027-01-12",
  "checker": "tên người hoặc mã phiên agent",
  "claims": [
    {
      "text": "Gettier đăng bài trên Analysis năm 1963",
      "kind": "du-kien",
      "verdict": "dung",
      "sources": [{"url": "https://doi.org/10.1093/analys/23.6.121", "quote": "Analysis, Volume 23, Issue 6, June 1963"}]
    },
    {
      "text": "câu bị sai, chép nguyên văn",
      "kind": "dien-giai",
      "verdict": "sai",
      "severity": "nghiem-trong",
      "fix": "câu sửa đề xuất",
      "sources": [{"url": "https://…", "quote": "vài chữ trên trang nguồn"}]
    }
  ],
  "checklist": {"dung-nguon": true, "manh-nhat": true, "phan-bac": true, "trung-lap": true, "thuat-ngu": false},
  "result": "sua",
  "notes": ""
}
```

- `hash`: mã băm của đơn vị lúc kiểm: `uv run python tools/check_ledger.py --hash <khóa đơn vị>`. Phải trùng mã băm ghi trong `verification/ledger.json`.
- `result`: `dat` = không còn lỗi nghiêm trọng hay vừa; `sua` = có lỗi cần sửa, liệt kê trong `claims`; `chua-kiem-duoc` = còn khẳng định không mở được nguồn.

## Quy tắc trung thực

- Chỉ ghi URL đã mở trong phiên này. `quote` là chữ thật trên trang đó.
- Không biến trí nhớ thành `dung`. Không chắc thì ghi `chua-kiem-duoc`.
- Không sửa bài, kể cả khi lỗi rõ ràng: người làm sửa, người kiểm ghi.
