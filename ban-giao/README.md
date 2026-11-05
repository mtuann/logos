# Bàn giao: giao việc cho agent, LLM hay người mới

Thư mục này chứa mọi thứ cần đưa cho người nhận việc, kèm prompt dán sẵn. Không xuất bản lên site.

## Bộ file cần đưa

| File | Dùng để | Ai cần |
|---|---|---|
| `AGENTS.md` | luật cứng, lệnh, cách làm một phiên, mẫu báo cáo | mọi người nhận việc (agent tự đọc) |
| `CLAUDE.md` | để Claude Code tự nạp `AGENTS.md` | Claude Code |
| `KE-HOACH.md` | kế hoạch, bảng quyết định, các đợt, cổng, đặc tả | mọi người |
| `ban-giao/dot-N.md` | việc cụ thể của đợt N | người làm đợt N |
| `ban-giao/kiem-chung.md` | quy trình và định dạng bằng chứng cho người kiểm | agent kiểm, LLM chat |
| `ban-giao/mau-dot.md` | khuôn viết brief cho đợt mới | chủ biên |
| `ban-giao/viec-cho.md` | lỗi và ý tưởng ngoài phạm vi, chờ đợt phù hợp | mọi người |
| `ban-giao/nhat-ky-dot-N.md` | tiến độ từng phiên (người làm tự tạo) | người làm, chủ biên |
| `HUONG-DAN-VIET.md`, `README.md`, `tools/philpapers-2020.md` | văn phong và thuật ngữ; lệnh và cấu trúc; số liệu khảo sát | mọi người |

Agent có quyền vào repo chỉ cần repo: nó tự đọc các file trên. Chỉ LLM chat (không vào được repo) mới cần đính kèm file.

## Giao cho ai, giao thế nào

1. **Agent có quyền vào repo và chạy lệnh** (Claude Code, Codex CLI, Cursor…): dùng cho mọi đợt. Mở repo, dán **Prompt A**. Claude Code nạp `AGENTS.md` qua `CLAUDE.md`; Codex và nhiều công cụ khác đọc `AGENTS.md` trực tiếp.
2. **Agent kiểm** (đợt 5 và mọi PR Mở rộng): mở một phiên mới, tách biệt với phiên của agent làm, dán **Prompt B**.
3. **LLM chat không chạy được lệnh** (ChatGPT, Claude trên web…): chỉ giao việc kiểm chứng từng đơn vị. Đính kèm `ban-giao/kiem-chung.md` và `HUONG-DAN-VIET.md`, dán **Prompt C** cùng nội dung đơn vị. Không giao việc sửa repo.
4. **Người mới**: làm "Bài nhận việc" ở cuối file này trước khi nhận đợt.

## Prompt A — agent làm

```text
Bạn đang làm việc trên repo Logos (làm lại website triết học tiếng Việt Logos Zero; ProperDocs + Material, quản lý bằng uv).
1. Đọc AGENTS.md và tuân theo toàn bộ, nhất là mục 3 (luật cứng) và mục 6 (khi nào dừng và hỏi).
2. Việc của phiên này: Đợt {N} — {tên đợt}, phần: {phạm vi cụ thể, ví dụ "việc 0.4 và 0.5"}. Chi tiết ở ban-giao/dot-{N}.md.
3. Nếu có ban-giao/nhat-ky-dot-{N}.md thì đọc và làm tiếp từ đó, không làm lại.
4. Mỗi việc một nhánh dot-{N}-{tên-ngắn}; xong việc, bộ kiểm tra xanh thì merge --no-ff vào main trên máy. Chỉ push main khi xong cả đợt (AGENTS.md luật 6). Không xóa file.
5. Sau mỗi đơn vị việc, ghi một dòng vào ban-giao/nhat-ky-dot-{N}.md.
6. Trước khi báo cáo, chạy bộ kiểm tra đầy đủ ở AGENTS.md mục 4.
Kết thúc bằng báo cáo theo mẫu AGENTS.md mục 7.
```

## Prompt B — agent kiểm

```text
Bạn là người kiểm chứng độc lập cho Logos Zero. Bạn không viết các đơn vị dưới đây và không sửa nội dung bài.
1. Đọc ban-giao/kiem-chung.md và HUONG-DAN-VIET.md.
2. Kiểm các đơn vị: {danh sách khóa, ví dụ cau-hoi/tri-thuc.md#cac-lap-truong-chinh}.
3. Kiểm xong đơn vị nào thì ghi ngay file bằng chứng của đơn vị đó vào verification/evidence/ theo đúng schema trong kiem-chung.md.
4. Mọi phán đoán phải có link nguồn bạn đã thực sự mở trong phiên này và vài chữ trích từ trang đó. Không mở được nguồn thì ghi "chua-kiem-duoc", không đoán.
Kết thúc bằng bảng: đơn vị · kết luận (dat / sua / chua-kiem-duoc) · số lỗi theo mức.
```

## Prompt C — LLM chat, không có repo

```text
Bạn là người kiểm chứng cho một website triết học tiếng Việt.
Tài liệu đính kèm: kiem-chung.md (quy trình, nguồn được dùng, định dạng kết quả) và HUONG-DAN-VIET.md (văn phong, thuật ngữ bắt buộc).
Hãy kiểm đơn vị dưới đây theo kiem-chung.md. Dùng công cụ duyệt web để mở nguồn; chỉ dẫn nguồn bạn đã thực sự mở.
Trả lời đúng một khối JSON theo schema trong kiem-chung.md, không thêm lời bình ngoài JSON.
Đơn vị: {khóa}
---
{dán nguyên văn nội dung đơn vị}
---
```

## Mẹo để việc giao ra đúng ý

- Một phiên, một phần việc nhỏ. Phạm vi càng cụ thể, kết quả càng sát.
- Agent kiểm luôn là một phiên mới, không thấy cuộc trò chuyện của agent làm.
- Không cho hai agent cùng sửa một file.
- Khi trả lời câu hỏi của agent về một quyết định, ghi câu trả lời vào bảng Quyết định trong `KE-HOACH.md`. Trả lời trong chat thì phiên sau không biết.
- Cuối mỗi phiên, đọc báo cáo, nhật ký và kết quả CI; không cần đọc lại từng trang. Việc đọc kỹ dành cho mẫu 10% ở đợt 5.
- Khi đổi lịch hay cổng, sửa `KE-HOACH.md` trước rồi mới giao việc.

## Bài nhận việc cho người mới (khoảng 2 giờ)

1. Đọc `AGENTS.md`, `KE-HOACH.md` mục 1–3, `HUONG-DAN-VIET.md`.
2. Cài đặt và chạy bộ kiểm tra đầy đủ ở `AGENTS.md` mục 4; ghi lại số kiểm thử pass.
3. Đọc `docs/cau-hoi/tri-thuc.md` và `docs/triet-gia/kant.md`. Đánh dấu đâu là dữ kiện (năm, tác phẩm, trích dẫn, số liệu) và đâu là diễn giải.
4. Kiểm một đơn vị theo `ban-giao/kiem-chung.md` rồi đưa chủ biên xem file bằng chứng.
