---
title: Khi bằng chứng chỉ làm cho có lẽ đúng
description: Phần lớn những gì ta tin đến từ quy nạp, không phải suy diễn. Bài này bàn về quy nạp khái quát, thống kê, loại suy, nhân quả, suy luận đến lời giải thích tốt nhất, và vì sao tương quan không phải nhân quả.
skill: induction
updated: 2026-10-22
tier: loi
block: cong-cu
---

# Khi bằng chứng chỉ làm cho có lẽ đúng

Ở chợ Bến Thành, chị bán xoài bổ cho bạn nếm một miếng. Ngọt. Bạn chọn thêm một quả khác, nhờ chị bổ thử. Cũng ngọt. Bạn mua năm cân.

Về nhà, bạn chưa ăn quả nào trong năm cân ấy. Vậy mà bạn khá chắc chúng ngọt. Bạn không *chứng minh* được điều đó. Có thể chị bán hàng đã đưa hai quả ngon nhất cho bạn thử. Nhưng bạn có lý do, và lý do ấy không phải là không có gì.

Đây là kiểu suy nghĩ ta dùng nhiều nhất trong đời: đi từ những gì đã thấy đến những gì chưa thấy. Triết học gọi nó là **quy nạp** (*inductive*).

## Quy nạp là gì? {#quy-nap-la-gi}

Ở bài [suy diễn](suy-dien.md), một lập luận tốt *bảo đảm* kết luận: tiền đề đúng thì kết luận không thể sai. Một lập luận quy nạp không hứa hẹn nhiều như vậy. Nó chỉ nói: nếu tiền đề đúng thì kết luận *có lẽ* đúng.

Đổi lại, quy nạp làm được điều suy diễn không làm được: kết luận của nó **đi xa hơn** tiền đề. Hai quả xoài nói cho bạn về hai quả xoài; kết luận của bạn lại nói về năm cân.

Vì vậy, ta không đánh giá lập luận quy nạp bằng "hợp lệ hay không", mà bằng **mạnh hay yếu** (*strong*). Một lập luận quy nạp mạnh mà các tiền đề lại đúng thì được gọi là **thuyết phục** (*cogent*).

Hai điểm khác biệt quan trọng:

- Hợp lệ là chuyện có hoặc không. Mạnh là chuyện *mức độ*: lập luận này mạnh hơn lập luận kia.
- Thêm tiền đề không bao giờ làm một lập luận hợp lệ trở thành không hợp lệ. Nhưng thêm thông tin có thể làm một lập luận quy nạp yếu đi rất nhiều. Biết thêm "chị bán xoài để riêng hai quả thử ở một rổ khác" là đủ để niềm tin của bạn lung lay.

## Bốn dạng quy nạp thường gặp {#bon-dang-quy-nap-thuong-gap}

### Quy nạp khái quát

Từ một mẫu, rút ra kết luận về cả tổng thể.

```text
Những con thiên nga ta đã quan sát đều màu trắng.
------------------------------------------------- (có lẽ)
Mọi con thiên nga đều màu trắng.
```

Người châu Âu từng có rất nhiều quan sát như thế, cho đến khi gặp thiên nga đen ở Úc. Quy nạp mạnh vẫn có thể sai.

### Quy nạp thống kê

Từ một tỉ lệ trong một nhóm, rút ra kết luận về một cá thể trong nhóm ấy.

```text
90% sinh viên trường X đi học bằng xe buýt.
An là sinh viên trường X.
------------------------------------------------- (có lẽ)
An đi học bằng xe buýt.
```

Tỉ lệ càng cao, lập luận càng mạnh. Nhưng nếu biết thêm "An ở ký túc xá ngay trong trường", lập luận yếu đi hẳn: bây giờ nhóm liên quan không còn là "sinh viên trường X" nữa mà là "sinh viên ở ký túc xá".

### Loại suy

Hai thứ giống nhau ở nhiều điểm, nên có lẽ giống nhau ở điểm đang xét.

```text
Thuốc A và thuốc B có cùng hoạt chất, cùng liều lượng.
Thuốc A trị được bệnh này.
------------------------------------------------- (có lẽ)
Thuốc B cũng trị được bệnh này.
```

Loại suy mạnh khi các điểm giống nhau *liên quan* đến điểm đang xét (cùng hoạt chất thì liên quan đến tác dụng), và yếu khi chỉ giống bề ngoài (cùng màu vỏ hộp thì không).

### Quy nạp nhân quả

Từ những quan sát về sự đi kèm, rút ra kết luận rằng cái này gây ra cái kia.

```text
Mỗi lần tôi ăn tôm, tôi bị ngứa.
Những lần không ăn tôm, tôi không bị ngứa.
------------------------------------------------- (có lẽ)
Tôm gây ngứa cho tôi.
```

Dạng này đặc biệt dễ trượt, ta sẽ quay lại ở cuối bài.

## Mạnh hay yếu: cỡ mẫu và tính đại diện {#manh-hay-yeu-co-mau-va-tinh-dai-dien}

Một khảo sát đăng trong nhóm Facebook của một phòng gym hỏi: "Bạn có tập thể dục ít nhất ba buổi mỗi tuần không?" Kết quả: 92% trả lời có. Một trang tin giật tít: "Phần lớn người Việt tập thể dục đều đặn."

Mẫu này hỏng ở hai chỗ:

- **Cỡ mẫu**: nếu chỉ 50 người trả lời, ngẫu nhiên thôi cũng đủ làm con số lệch đi nhiều.
- **Tính đại diện**: người trong nhóm gym không giống người Việt nói chung. Thêm nữa, ai chịu trả lời một khảo sát tự nguyện cũng đã là một nhóm chọn lọc.

Một mẫu nhỏ nhưng chọn ngẫu nhiên tử tế có thể đáng tin hơn một mẫu khổng lồ nhưng lệch. Khi rút ra một kết luận khái quát từ quá ít trường hợp hoặc từ những trường hợp không đại diện, ta mắc lỗi **khái quát vội vàng**, được bàn ở bài [Ngụy biện](nguy-bien.md#hasty-generalization).

## Một câu hỏi không dễ chịu: vì sao tin quy nạp? {#mot-cau-hoi-khong-de-chiu-vi-sao-tin-quy-nap}

Mọi lập luận quy nạp đều ngầm dựa vào một giả định: tương lai (hoặc phần chưa quan sát) sẽ giống quá khứ (hoặc phần đã quan sát). Mặt trời đã mọc mỗi sáng, nên mai nó sẽ mọc.

Nhưng ta lấy gì để tin giả định ấy? Không phải suy diễn: "tương lai khác quá khứ" không hề tự mâu thuẫn. Nếu là quy nạp ("trước giờ tương lai luôn giống quá khứ, nên sau này cũng vậy"), thì ta đang dùng chính quy nạp để biện minh cho quy nạp, tức là đi vòng tròn.

Đây là **vấn đề quy nạp**, gắn với tên [David Hume](../triet-gia/hume.md), người trình bày nó trong *A Treatise of Human Nature* (1739–40) và *An Enquiry concerning Human Understanding* (1748). Đến nay các nhà triết học vẫn chưa thống nhất cách giải quyết. Lập luận của Hume được đọc chậm, từng đoạn, trong bài [Đọc Hume về nhân quả](../doc/hume-nhan-qua.md).

Ở đây chỉ cần một ghi chú thực dụng: vấn đề của Hume không cho phép ta coi mọi lập luận quy nạp là ngang nhau. Dù chưa có lời biện minh triệt để cho quy nạp, nếm hai quả xoài vẫn tốt hơn không nếm quả nào.

## Suy luận đến lời giải thích tốt nhất {#suy-luan-den-loi-giai-thich-tot-nhat}

Bác sĩ ở một phòng khám tại Hà Nội, giữa mùa mưa, gặp một bệnh nhân: sốt cao đột ngột ba ngày, đau nhức cơ khớp, đau sau hốc mắt, nổi ban đỏ, xét nghiệm thấy tiểu cầu giảm. Bác sĩ nghĩ đến **sốt xuất huyết**.

Bác sĩ không suy diễn ra điều đó, cũng không khái quát từ một mẫu. Bác sĩ đặt ra vài giả thuyết (cúm, sốt xuất huyết, sốt phát ban do virus khác…) rồi chọn giả thuyết *giải thích tốt nhất* toàn bộ những gì đang thấy. Kiểu suy luận này gọi là **suy luận đến lời giải thích tốt nhất** (*inference to the best explanation*), còn được gọi là *abduction*.

Thám tử cũng làm vậy. Két sắt mất tiền, cửa không bị phá, camera tắt đúng mười phút, chú chó bảo vệ không sủa. Giả thuyết "kẻ trộm là người lạ" phải thêm nhiều chi tiết gượng ép (biết mật khẩu camera, quen với chó…). Giả thuyết "người trong nhà" giải thích được mọi chi tiết mà không cần thêm gì.

Thế nào là một lời giải thích "tốt"? Không có công thức chung, nhưng người ta thường dùng các tiêu chí sau:

1. **Giải thích được nhiều**: bao quát được càng nhiều dữ kiện càng tốt, kể cả dữ kiện lạ (đau sau hốc mắt, tiểu cầu giảm).
2. **Đơn giản**: không đặt ra nhiều thực thể hay cơ chế hơn mức cần thiết.
3. **Nhất quán với điều đã biết**: phù hợp với tri thức nền (đang mùa mưa, đang có dịch sốt xuất huyết ở địa phương).
4. **Ít giả định ad hoc**: không phải vá víu thêm những giả định chỉ được tạo ra để cứu giả thuyết.

!!! warning "Tốt nhất chưa chắc là đúng"
    Lời giải thích tốt nhất trong số những lời giải thích *ta nghĩ ra được* vẫn có thể sai, nếu ta chưa nghĩ đến lời giải thích đúng. Vì vậy bác sĩ giỏi vẫn làm xét nghiệm xác nhận, và thám tử giỏi vẫn tìm thêm bằng chứng.

## Tương quan không phải nhân quả {#tuong-quan-khong-phai-nhan-qua}

Một bài báo đưa tin: "Ở các thành phố bán nhiều kem, số vụ đuối nước cũng cao hơn." Kem gây đuối nước?

Khi hai thứ hay đi cùng nhau (**tương quan**), có ít nhất bốn khả năng:

```text
1. A gây ra B.                 Kem gây đuối nước? (khó tin)
2. B gây ra A.                 Đuối nước làm người ta mua kem? (vô lý)
3. C gây ra cả A và B.         Trời nóng → nhiều người ăn kem
                                         → nhiều người đi bơi → nhiều vụ đuối nước
4. Trùng hợp.                  Với đủ nhiều dữ liệu, sẽ có những cặp số
                               đi cùng nhau chỉ do tình cờ.
```

Khả năng 3 (một **yếu tố gây nhiễu** chung) là thủ phạm phổ biến nhất. Trước khi kết luận A gây ra B, hãy hỏi: có yếu tố nào khác có thể gây ra cả hai không? Có thể nào chiều nhân quả ngược lại không?

Một lỗi họ hàng là chỉ vì B xảy ra *sau* A mà cho rằng A gây ra B, gọi là [Sau nó nên do nó](nguy-bien.md#post-hoc).

## Mẫu nhận diện {#mau-nhan-dien}

**Dấu hiệu của lập luận quy nạp:** từ chỉ báo kiểu "có lẽ", "nhiều khả năng", "hầu hết", "thường thì", "chắc là", "theo khảo sát", "từ kinh nghiệm", "giống như"; kết luận nói về nhiều hơn những gì đã quan sát.

**Câu hỏi kiểm tra theo dạng:**

```text
Khái quát   → Mẫu bao lớn? Chọn thế nào? Có đại diện không?
Thống kê    → Tỉ lệ cao đến đâu? Cá thể có thuộc nhóm hẹp hơn nào khác không?
Loại suy    → Những điểm giống nhau có LIÊN QUAN tới điểm đang xét không?
              Có điểm khác nhau quan trọng nào không?
Nhân quả    → Có yếu tố gây nhiễu không? Có thể ngược chiều không? Trùng hợp?
Giải thích  → Đã xét đủ các giả thuyết khác chưa? Giả thuyết nào giải thích
              nhiều hơn, đơn giản hơn, ít vá víu hơn?
```

## Bài tập {#bai-tap}

**Bài 1.** Một ứng dụng học tiếng Anh khảo sát 2.000 người dùng của chính ứng dụng và kết luận: "85% người Việt muốn học tiếng Anh mỗi ngày." Lập luận này mạnh hay yếu? Vì sao?

??? success "Xem gợi ý đáp án"
    Yếu, dù cỡ mẫu không nhỏ. Mẫu không đại diện: người dùng một ứng dụng học tiếng Anh vốn đã là những người muốn học tiếng Anh. Kết luận về "người Việt" nói chung đi quá xa so với mẫu.

**Bài 2.** "Hãng bay X có 95% chuyến đúng giờ trong năm qua. Chuyến bay của tôi chiều nay thuộc hãng X. Vậy chuyến của tôi có lẽ sẽ đúng giờ." Thông tin nào sau đây làm lập luận yếu đi: (a) hãng X vừa được giải thưởng dịch vụ; (b) chiều nay có bão đổ bộ vào sân bay đến?

??? success "Xem gợi ý đáp án"
    (b). Bây giờ nhóm liên quan không còn là "mọi chuyến bay của hãng X" mà là "chuyến bay vào sân bay đang có bão", và tỉ lệ đúng giờ của nhóm này chắc chắn thấp hơn nhiều. Điều này cho thấy lập luận quy nạp có thể yếu đi khi biết thêm thông tin, điều không bao giờ xảy ra với tính hợp lệ của suy diễn.

**Bài 3.** Đánh giá lập luận loại suy: "Bộ não xử lý thông tin giống như máy tính. Máy tính không có cảm xúc. Vậy bộ não cũng không thực sự có cảm xúc."

??? success "Xem gợi ý đáp án"
    Yếu. Điểm giống nhau (xử lý thông tin) chưa chắc liên quan đến điểm đang xét (có cảm xúc hay không), và ta có bằng chứng trực tiếp mạnh hơn nhiều về cảm xúc của con người. Lập luận cũng có thể bị lật ngược: "bộ não giống máy tính, bộ não có cảm xúc, vậy máy tính có thể có cảm xúc", cũng yếu ngang vậy. Câu hỏi này được bàn kỹ ở [bài về tâm trí và AI](../cau-hoi/tam-tri-va-ai.md).

**Bài 4.** Một nghiên cứu thấy học sinh có điện thoại thông minh riêng từ năm lớp 6 có điểm trung bình thấp hơn các bạn không có. Hãy nêu ít nhất hai cách giải thích khác ngoài "điện thoại làm điểm thấp".

??? success "Xem gợi ý đáp án"
    Một vài khả năng: (1) yếu tố gây nhiễu: hoàn cảnh gia đình (ví dụ bố mẹ đi làm xa, ít thời gian kèm con) vừa khiến con được cho điện thoại sớm để liên lạc, vừa ảnh hưởng đến kết quả học; (2) ngược chiều: học sinh học kém hơn có thể được bố mẹ cho điện thoại để dùng ứng dụng học thêm; (3) trùng hợp, nếu mẫu nhỏ. Điều này không có nghĩa điện thoại *không* ảnh hưởng, chỉ có nghĩa tương quan một mình chưa đủ để kết luận.

**Bài 5.** Chiếc bánh bông lan trên bàn biến mất. Có vụn bánh trên áo em trai bạn; con mèo đang ngủ trên ghế sofa; cửa sổ mở. Ba giả thuyết: (a) em trai ăn; (b) mèo ăn; (c) kẻ trộm trèo cửa sổ vào lấy. Giả thuyết nào là lời giải thích tốt nhất? Theo tiêu chí nào?

??? success "Xem gợi ý đáp án"
    (a). Nó giải thích được dữ kiện lạ nhất (vụn bánh trên áo em), đơn giản, nhất quán với tri thức nền (trẻ con thích bánh). Giả thuyết (b) không giải thích vụn bánh trên áo và cần thêm giả định (mèo ăn hết cả chiếc bánh mà không để lại dấu vết). Giả thuyết (c) cần nhiều giả định ad hoc (trộm chỉ lấy bánh?). Nhưng (a) vẫn có thể sai; có thể em chỉ ăn một miếng.

## Tự kiểm tra {#tu-kiem-tra}

Thử xem bạn nắm được đến đâu.

<div class="oz-quiz" data-id="induction-1" data-skill="induction" markdown="0">
<script type="application/json">
[
 {"q": "Điểm khác biệt cốt lõi giữa lập luận quy nạp mạnh và lập luận suy diễn hợp lệ là gì?", "options": ["Quy nạp luôn có tiền đề sai", "Với quy nạp mạnh, tiền đề đúng làm kết luận có lẽ đúng nhưng không bảo đảm nó đúng", "Quy nạp chỉ dùng trong khoa học tự nhiên", "Suy diễn luôn cho kết luận mới mà tiền đề chưa chứa"], "answer": 1, "explain": "Suy diễn hợp lệ bảo đảm kết luận khi tiền đề đúng; quy nạp mạnh chỉ làm kết luận có khả năng cao. Đổi lại, quy nạp cho phép kết luận đi xa hơn tiền đề."},
 {"q": "Một khảo sát về thói quen đọc sách được thực hiện tại hội sách và kết luận “người Việt đọc trung bình 10 cuốn mỗi năm”. Vấn đề lớn nhất là gì?", "options": ["Mẫu không đại diện", "Lập luận không hợp lệ về hình thức", "Đây là loại suy", "Không có vấn đề gì nếu cỡ mẫu đủ lớn"], "answer": 0, "explain": "Người đến hội sách là nhóm thích đọc sách hơn mức trung bình. Mẫu lệch thì cỡ mẫu lớn đến đâu cũng không sửa được."},
 {"q": "Số người đi biển và số người bị cháy nắng cùng tăng vào tháng 6. Cách giải thích nào hợp lý nhất?", "options": ["Đi biển gây ra cháy nắng, chắc chắn", "Cháy nắng khiến người ta đi biển", "Nắng hè là yếu tố chung góp phần gây ra cả hai, nên chỉ riêng tương quan này chưa đủ để kết luận nhân quả", "Đây chỉ là trùng hợp"], "answer": 2, "explain": "Mùa hè nắng nóng làm cả hai cùng tăng. Có thể đi biển cũng góp phần gây cháy nắng, nhưng tương quan theo mùa một mình không đủ để tách các yếu tố."},
 {"q": "Tiêu chí nào KHÔNG thuộc nhóm tiêu chí thường dùng để chọn lời giải thích tốt nhất?", "options": ["Giải thích được nhiều dữ kiện", "Đơn giản", "Nhất quán với điều đã biết", "Được nhiều người tin nhất"], "answer": 3, "explain": "Số người tin không phải tiêu chí của một lời giải thích tốt. Ba tiêu chí kia, cùng với việc ít giả định ad hoc, là những tiêu chí thường được nêu."},
 {"q": "Vấn đề quy nạp của Hume chỉ ra điều gì?", "options": ["Mọi lập luận quy nạp đều yếu như nhau", "Khó biện minh cho giả định “tương lai sẽ giống quá khứ” mà không đi vòng tròn", "Quy nạp thực chất là suy diễn", "Khoa học không dùng quy nạp"], "answer": 1, "explain": "Hume cho thấy giả định ấy không chứng minh được bằng suy diễn, còn dùng quy nạp để biện minh cho nó thì vòng tròn. Điều này không có nghĩa mọi lập luận quy nạp đều ngang nhau."}
]
</script>
</div>

## Đi tiếp {#di-tiep}

Trong nhiều lập luận ở trên, có những điều người nói không nói ra mà vẫn ngầm dựa vào: "người dùng ứng dụng giống người Việt nói chung", "chỉ có hai khả năng". Làm sao lôi chúng ra ánh sáng? Mời đọc [Điều không được nói ra](gia-dinh-ngam.md).

## Nguồn {#nguon}

1. Leah Henderson, "The Problem of Induction", *Stanford Encyclopedia of Philosophy*. <https://plato.stanford.edu/archives/fall2026/entries/induction-problem/>
2. Igor Douven, "Abduction", *Stanford Encyclopedia of Philosophy*. <https://plato.stanford.edu/archives/fall2026/entries/abduction/>
3. Timothy Shanahan, "Deductive and Inductive Arguments", *Internet Encyclopedia of Philosophy*. <https://iep.utm.edu/deductive-inductive-arguments/>
4. Qu, Hsueh & Elizabeth S. Radcliffe, "David Hume", *Stanford Encyclopedia of Philosophy* (2026). <https://plato.stanford.edu/archives/fall2026/entries/hume/>
5. David Hume, *An Enquiry concerning Human Understanding* (1748), bản phạm vi công cộng trên Project Gutenberg. <https://www.gutenberg.org/ebooks/9662>
6. Peter Lipton, *Inference to the Best Explanation*, ấn bản 2, Routledge, 2004.
