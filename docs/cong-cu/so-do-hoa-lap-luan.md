---
title: "Sơ đồ hóa lập luận"
description: "Vẽ lập luận thành sơ đồ hộp-mũi tên: tiền đề nào đỡ kết luận, giả định ngầm nằm ở đâu, tiền đề nào phải đi cùng nhau. Bài này hướng dẫn vẽ tay trong năm phút."
skill: argument
updated: 2026-10-13
tier: loi
block: cong-cu
---

# Sơ đồ hóa lập luận

Bạn đọc một bài báo hai nghìn chữ phản đối dạy thêm. Đọc xong, bạn thấy "có gì đó sai sai" mà không chỉ ra được chỗ nào. Vấn đề không phải bạn kém — mà là lập luận nằm rải rác trong hai nghìn chữ, còn bộ nhớ của ta thì không giữ nổi ngần ấy thứ cùng lúc.

Cách đơn giản nhất để *thấy* một lập luận: vẽ nó ra.

## Hộp và mũi tên {#hop-va-mui-ten}

Một sơ đồ lập luận chỉ có hai thứ:

- **Hộp**: mỗi hộp là một khẳng định. Một hộp, một ý — đừng nhét hai ý vào một hộp.
- **Mũi tên**: đi từ lý do đến điều được lý do đó nâng đỡ. Đọc là: "vì hộp này, nên hộp kia".

Lấy một đoạn văn ngắn:

> Trường nên cấm điện thoại trong giờ học. Điện thoại làm học sinh mất tập trung, mà mất tập trung thì học kém đi.

Tách thành ba hộp:

- P1. Điện thoại làm học sinh mất tập trung.
- P2. Mất tập trung thì học kém đi.
- K. Nên cấm điện thoại trong giờ học.

```text
P1 ──┐
     ├─→ K
P2 ──┘
```

Hai mũi tên chập làm một: P1 và P2 phải *đi cùng nhau* mới đỡ nổi K. Một mình P1 ("điện thoại làm mất tập trung") thì chưa đủ để kết luận "nên cấm" — mất tập trung thì sao? Một mình P2 cũng vậy. Cặp tiền đề như thế gọi là **tiền đề liên kết** (*linked premises*).

Ngược lại, có những tiền đề mỗi cái tự đứng được:

> Nên đọc sách mỗi ngày. Đọc sách mở rộng vốn từ. Đọc sách còn giúp dễ ngủ.

```text
P1 ──→ K
P2 ──→ K
```

Mỗi mũi tên đứng một mình. Gãy một cái, kết luận vẫn còn cái kia đỡ. Đây là **tiền đề độc lập** (*independent premises*).

## Vì sao phải phân biệt liên kết với độc lập {#vi-sao-phai-phan-biet-lien-ket-voi-doc-lap}

Vì cách phản biện hai loại này khác nhau hoàn toàn.

Với tiền đề liên kết, chỉ cần bẻ *một* mắt xích là cả cụm sập. Trong ví dụ điện thoại: nếu chứng minh được "mất tập trung không nhất thiết làm học kém" (có người vừa nghe nhạc vừa học vẫn giỏi), mũi tên gãy — dù P1 có đúng đi nữa.

Với tiền đề độc lập, bẻ một cái chưa đủ. Bạn chứng minh "đọc sách không giúp dễ ngủ" thì kết luận "nên đọc sách" vẫn còn P1 đỡ. Phải bẻ từng cái một.

Lỗi phổ biến: hạ được một tiền đề độc lập rồi tưởng mình đã hạ được kết luận — trong khi kết luận vẫn đứng vững trên những chân còn lại.

## Đánh dấu mũi tên gãy {#danh-dau-mui-ten-gay}

Sơ đồ không chỉ để vẽ lúc yên bình — nó còn là chiến trường. Khi bạn bẻ được một mắt xích, đánh dấu ngay trên sơ đồ:

```text
P1 ──✗──→ K        (mũi tên bị đánh gãy: lý do này không đỡ nổi nữa)
```

Và khi bạn có lý do phản bác, vẽ thêm hộp "phản biện" với mũi tên đâm ngược vào hộp tiền đề:

```text
┌──────────────┐      ┌───────────────────┐
│ P1. Điện     │◀──── │ Phản biện: có     │
│ thoại gây    │      │ người vừa nghe    │
│ mất tập      │      │ nhạc vừa học vẫn  │
│ trung        │      │ giỏi               │
└──────────────┘      └───────────────────┘
```

Một sơ đồ đầy đủ sau trận chiến sẽ có: hộp, mũi tên, hộp đứt nét (giả định ngầm), dấu ✗ (mũi tên gãy), và hộp phản biện. Nhìn vào đó, ai cũng thấy ngay lập luận còn đứng được hay đã sập.

## Giả định ngầm: hộp đứt nét {#gia-dinh-ngam-hop-dut-net}

Quay lại ví dụ điện thoại. Nhìn kỹ sơ đồ, bạn có thấy thiếu gì không? Từ "mất tập trung thì học kém" nhảy đến "nên cấm" còn một bước nữa mà tác giả không nói ra:

```text
P1 ──┐
     ├─→ K
P2 ──┘

+ - - - - - - - - - - - - -+
: Giả định ngầm:           : ──→ K
: "không có cách nào khác  :
: giảm mất tập trung       :
: ngoài cấm"               :
+ - - - - - - - - - - - - -+
```

Quy ước: **giả định ngầm** (*hidden assumption*) vẽ bằng hộp đứt nét — để nhắc rằng nó có mặt trong lập luận dù tác giả không nói ra.

Và đây mới là chỗ đáng đánh nhất: cấm có phải cách duy nhất không? Thu điện thoại đầu giờ, dùng app khóa máy trong giờ học — đều giảm mất tập trung mà không cần cấm. Tác giả lẳng lặng giả định "ngoài cấm ra không còn cách nào" mà không hề bảo vệ giả định đó. Trong hầu hết lập luận thực tế, giả định ngầm chính là mắt xích yếu nhất — vẽ nó ra là đã thắng một nửa. (Xem thêm [Giả định ngầm](gia-dinh-ngam.md).)

## Một bài vẽ hoàn chỉnh {#mot-bai-ve-hoan-chinh}

Ghép mọi thứ lại trong một đoạn văn:

> "Thành phố nên cấm xe xăng trong nội đô từ năm 2030. Xe xăng là nguồn ô nhiễm không khí chính trong thành phố, mà ô nhiễm không khí làm tăng bệnh hô hấp. Hơn nữa, các thành phố lớn trên thế giới đều đã làm vậy."

Tách hộp:

- P1. Xe xăng là nguồn ô nhiễm không khí chính trong nội đô.
- P2. Ô nhiễm không khí làm tăng bệnh hô hấp.
- P3. Các thành phố lớn trên thế giới đều đã làm vậy.
- K. Nên cấm xe xăng trong nội đô từ năm 2030.

Vẽ:

```text
P1 ──┐
     ├─→ K          (P1 + P2 liên kết)
P2 ──┘

P3 ──→ K            (P3 độc lập)

+ - - - - - - - - - - - - -+
: Giả định ngầm:           : ──→ K
: "lợi ích sức khỏe đáng   :
: đánh đổi sự bất tiện     :
: và chi phí chuyển đổi"   :
+ - - - - - - - - - - - - -+
```

Giờ thì cả lập luận nằm gọn trong một hình. Muốn phản biện, bạn có sẵn bản đồ: bẻ P1 (xe xăng có thật là nguồn *chính* không, hay còn bụi xây dựng, nhà máy?), bẻ P2, bẻ P3 ("ai cũng làm" — xem câu 5 phần Tự kiểm tra), hay đánh vào giả định ngầm (người nghèo đi xe xăng cũ lấy gì đi làm?). Không còn cảnh "sai sai mà không biết sai ở đâu".

## Khi nào nên vẽ {#khi-nao-nen-ve}

- **Bài viết dài, lập luận rải rác.** Vẽ ra, bạn sẽ thấy có những mũi tên trơ trọi không hộp nào đỡ — đó chính là chỗ "sai sai".
- **Tranh luận rối.** Hai người cãi nhau nảy lửa, vẽ ra mới thấy họ đang bảo vệ hai kết luận *khác nhau*. Bao nhiêu cuộc cãi vã thực chất chỉ là hiểu lầm về "ta đang tranh luận điều gì".
- **Khi bạn là người viết.** Trước khi đăng một bài phản biện, vẽ sơ đồ lập luận của chính mình trước: mũi tên nào yếu, tự mình thấy trước khi người khác thấy.

Không cần vẽ mọi thứ. Lập luận nào đã ngắn gọn, rõ ràng thì vẽ thêm chỉ tốn giấy. Sơ đồ là kính lúp, không phải kính râm — chỉ đeo khi cần soi.

## Bài tập {#bai-tap}

**Bài 1.** Vẽ sơ đồ cho đoạn văn sau. Các tiền đề liên kết hay độc lập?

> Nên uống cà phê buổi sáng. Cà phê giúp tỉnh táo, mà tỉnh táo thì làm việc hiệu quả.

??? success "Xem gợi ý đáp án"
    Ba hộp: P1 "Cà phê giúp tỉnh táo", P2 "Tỉnh táo thì làm việc hiệu quả", K "Nên uống cà phê buổi sáng". P1 và P2 liên kết: một mình "cà phê giúp tỉnh táo" chưa đủ để kết luận "nên uống" (tỉnh táo thì sao?). Giả định ngầm (hộp đứt nét): "làm việc hiệu quả là điều đáng theo đuổi" và "cà phê buổi sáng không hại sức khỏe đến mức át đi lợi ích".

**Bài 2.** Vẽ sơ đồ cho đoạn văn sau. Mũi tên nào gãy thì kết luận vẫn đứng?

> Bạn nên tập thể dục. Tập thể dục giúp tim khỏe. Tập thể dục còn giúp ngủ ngon. Tập thể dục cũng làm quen được nhiều bạn mới.

??? success "Xem gợi ý đáp án"
    Ba tiền đề độc lập, mỗi cái một mũi tên riêng đến K "Bạn nên tập thể dục". Bẻ một cái (ví dụ: "tập thể dục không giúp ngủ ngon với người mất ngủ kinh niên") thì K vẫn còn hai chân kia đỡ. Muốn hạ K phải bẻ cả ba — hoặc tấn công thẳng vào giả định ngầm: "khỏe, ngủ ngon, nhiều bạn thì đã sao?"

**Bài 3.** Tìm giả định ngầm trong lập luận quảng cáo sau và vẽ nó bằng hộp đứt nét:

> "99% nha sĩ được hỏi khuyên dùng kem đánh răng X. Vì vậy bạn nên dùng X."

??? success "Xem gợi ý đáp án"
    Ít nhất ba giả định ngầm: (1) các nha sĩ được hỏi không bị hãng X trả tiền; (2) "nha sĩ khuyên dùng" đồng nghĩa với "tốt cho bạn" (có thể họ khuyên vì hoa hồng); (3) điều đúng với đa số thì đúng với bạn (răng bạn có vấn đề riêng thì sao?). Quảng cáo cố tình để những hộp này "tàng hình" — vẽ ra là thấy ngay.

**Bài 4.** Lấy một bài báo hoặc một topic tranh luận bạn đọc gần đây. Vẽ sơ đồ đầy đủ: hộp, mũi tên, đánh dấu liên kết/độc lập, ít nhất một hộp đứt nét cho giả định ngầm. Giữ tờ giấy lại — một tuần sau nhìn lại, bạn còn đồng ý với sơ đồ của mình không?

??? success "Xem gợi ý đáp án"
    Không có đáp án mẫu. Dấu hiệu làm tốt: sơ đồ của bạn có ít nhất một hộp đứt nét mà lúc đọc bài bạn không để ý; và ít nhất một mũi tên bạn phải phân vân "liên kết hay độc lập". Dấu hiệu làm chưa tới: mọi thứ đều trơn tru, không có chỗ nào khiến bạn khựng lại — thường nghĩa là bạn mới vẽ lại những gì tác giả *nói*, chưa vẽ những gì tác giả *giấu*.

## Tự kiểm tra {#tu-kiem-tra}

<div class="oz-quiz" data-id="argument-4" data-skill="argument" markdown="0">
<script type="application/json">
[
 {"q": "Trong sơ đồ lập luận, mũi tên có nghĩa là gì?", "options": ["Hai hộp mâu thuẫn nhau", "Hộp này nâng đỡ hộp kia (lý do đỡ kết luận)", "Hai hộp nói về cùng một chủ đề", "Hộp này xảy ra trước hộp kia về thời gian"], "answer": 1, "explain": "Mũi tên đi từ lý do đến điều được lý do đó nâng đỡ. Đọc là: 'vì hộp này, nên hộp kia'."},
 {"q": "Tiền đề liên kết khác tiền đề độc lập ở điểm nào?", "options": ["Tiền đề liên kết luôn đúng, độc lập luôn sai", "Liên kết: phải đi cùng nhau mới đỡ nổi kết luận; độc lập: mỗi cái tự đứng được", "Liên kết thì không cần vẽ, độc lập thì phải vẽ", "Không có điểm nào khác nhau"], "answer": 1, "explain": "Với tiền đề liên kết, thiếu một mắt xích là cả cụm sập. Với tiền đề độc lập, gãy một cái thì kết luận vẫn còn những cái kia đỡ."},
 {"q": "Giả định ngầm được vẽ thế nào trong sơ đồ?", "options": ["Hộp đứt nét", "Mũi tên hai chiều", "Hộp tô đậm", "Không vẽ, vì đã gọi là 'ngầm'"], "answer": 0, "explain": "Quy ước của bài này: giả định ngầm vẽ bằng hộp đứt nét — để nhắc rằng nó có mặt trong lập luận dù tác giả không nói ra."},
 {"q": "Muốn phản bác một kết luận được đỡ bởi hai tiền đề độc lập, bạn phải làm gì?", "options": ["Bẻ một trong hai là đủ", "Bẻ từng cái một, hoặc tấn công thẳng vào kết luận hay giả định ngầm", "Vẽ lại sơ đồ cho đẹp hơn", "Hỏi tác giả học trường nào"], "answer": 1, "explain": "Mỗi tiền đề độc lập tự đỡ kết luận một mình, nên bẻ một cái chưa hạ được kết luận. Phải bẻ cả hai, hoặc đánh vào chỗ khác."},
 {"q": "Cho sơ đồ: P1 'Học thêm giúp điểm cao' ──→ K 'Nên cho con đi học thêm'; P2 'Bạn bè trong lớp đều đi học thêm' ──→ K. Mắt xích nào yếu nhất?", "options": ["P1, vì điểm cao chưa chắc do học thêm", "P2, vì 'ai cũng làm' không phải lý do", "K, vì kết luận luôn sai", "Không có mắt xích nào yếu"], "answer": 1, "explain": "P2 là kiểu 'ai cũng làm thì mình cũng nên làm' — số đông không biến một việc thành đúng. Ngoài ra còn giả định ngầm: 'điểm cao đáng để đánh đổi thời gian tuổi thơ'."}
]
</script>
</div>

## Thử với công cụ {#thu-voi-cong-cu}

Kéo từng câu vào đúng vai trò — tiền đề, kết luận, hay không liên quan — rồi xem sơ đồ hiện ra trước mắt bạn.

<div class="oz-so-do"></div>

## Đi tiếp {#di-tiep}

Sơ đồ cho thấy cấu trúc của lập luận. Câu hỏi tiếp theo: các mũi tên có thật sự *buộc* kết luận phải đúng không? Mời đọc [Khi nào kết luận buộc phải đúng?](suy-dien.md).

## Nguồn {#nguon}

1. Leo Groarke, "Informal Logic", *Stanford Encyclopedia of Philosophy*. <https://plato.stanford.edu/archives/fall2026/entries/logic-informal/>
