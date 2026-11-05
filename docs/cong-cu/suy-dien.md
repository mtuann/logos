---
title: Khi nào kết luận buộc phải đúng?
description: Lập luận suy diễn hứa hẹn sự chắc chắn. Bài này phân biệt hợp lệ với vững chắc, giới thiệu modus ponens, modus tollens, tam đoạn luận, hai ngụy biện hình thức và phương pháp phản ví dụ.
skill: deduction
updated: 2026-10-13
---

# Khi nào kết luận buộc phải đúng?

Sáng thứ Hai, chị Thu mở cửa nhà và thấy sân ướt. Chị nghĩ ngay: "Đêm qua mưa rồi." Rồi chị nhìn sang sân nhà hàng xóm: khô ráo. Hóa ra con trai chị vừa rửa xe.

Chị Thu không ngốc. Chị dựa vào một điều đúng: *nếu trời mưa thì sân ướt*. Và sân đúng là ướt. Hai điều đúng, vậy mà kết luận vẫn sai. Có gì đó trục trặc không nằm ở thông tin, mà nằm ở *cách* chị đi từ thông tin đến kết luận.

Bài này nói về chính cái "cách" ấy: khi nào những gì ta biết *buộc* một kết luận phải đúng, và khi nào nó chỉ trông có vẻ như vậy.

## Hợp lệ: một lời hứa về hình thức {#hop-le-mot-loi-hua-ve-hinh-thuc}

Một lập luận **suy diễn** (*deductive*) là lập luận nhắm đến sự chắc chắn: nếu tiền đề đúng thì kết luận *không thể* sai.

Một lập luận suy diễn là **hợp lệ** (*valid*) khi nó giữ được lời hứa đó: *không thể* có chuyện mọi tiền đề đều đúng mà kết luận lại sai. Nói cách khác, tiền đề đúng thì kết luận đúng, bất kể thế giới ra sao.

Điều quan trọng nhất cần nắm: **hợp lệ không nói gì về việc tiền đề có thật sự đúng hay không.** Nó chỉ nói về mối nối. Hãy xem lập luận này:

```text
P1. Mọi loài cá đều là động vật có vú.
P2. Cá voi là một loài cá.
--------------------------------------
K.  Cá voi là động vật có vú.
```

Cả hai tiền đề đều sai. Kết luận lại đúng. Và lập luận này *hợp lệ*: nếu P1 và P2 đúng thì K không thể sai. Lập luận hợp lệ, nhưng không cho ta lý do tốt nào để tin K.

Vì vậy cần thêm một khái niệm. Một lập luận là **vững chắc** (*sound*) khi nó vừa hợp lệ, vừa có mọi tiền đề đúng. Một lập luận vững chắc thì kết luận chắc chắn đúng.

## Bảng bốn trường hợp {#bang-bon-truong-hop}

| | **Mọi tiền đề đều đúng** | **Có ít nhất một tiền đề sai** |
|---|---|---|
| **Hợp lệ** | Kết luận *chắc chắn* đúng. Đây là lập luận vững chắc. *Mọi người đều phải chết; mọi nhà thơ đều là người; vậy mọi nhà thơ đều phải chết.* | Kết luận có thể đúng hoặc sai. *Mọi loài chim đều biết bay; chim cánh cụt là chim; vậy chim cánh cụt biết bay* (kết luận sai). Ví dụ cá voi ở trên (kết luận đúng). |
| **Không hợp lệ** | Kết luận có thể đúng hoặc sai. *Nếu Hà Nội là thủ đô Việt Nam thì Hà Nội ở Việt Nam; Hà Nội ở Việt Nam; vậy Hà Nội là thủ đô Việt Nam* (kết luận đúng, nhưng chỉ do may mắn). | Kết luận có thể đúng hoặc sai. |

Chỉ có *một* tổ hợp không bao giờ xảy ra: **hợp lệ, mọi tiền đề đúng, kết luận sai.** Đó chính là định nghĩa của hợp lệ.

Hãy để ý ô dưới bên trái. Lập luận về Hà Nội có tiền đề đúng, kết luận đúng, mà vẫn không hợp lệ. Thay "Hà Nội" bằng "Huế":

```text
P1. Nếu Huế là thủ đô Việt Nam thì Huế ở Việt Nam.   (đúng)
P2. Huế ở Việt Nam.                                 (đúng)
---------------------------------------------------
K.  Huế là thủ đô Việt Nam.                         (sai)
```

Cùng một khuôn, tiền đề vẫn đúng, kết luận thì sai. Vậy cái khuôn ấy không bảo đảm gì cả. Kết luận về Hà Nội đúng là nhờ thế giới tình cờ như vậy, không phải nhờ lập luận. Đây cũng chính là lỗi của chị Thu.

## Những khuôn đáng tin {#nhung-khuon-dang-tin}

Tính hợp lệ phụ thuộc vào **hình thức** của lập luận, không phụ thuộc vào nội dung. Vì vậy, quen mặt vài khuôn hợp lệ là có thể nhận ra chúng ở bất cứ đâu. Trong các sơ đồ dưới đây, P, Q, R là những khẳng định bất kỳ.

### Modus ponens (khẳng định tiền kiện)

Trong câu "nếu P thì Q", P gọi là **tiền kiện**, Q gọi là **hậu kiện**.

```text
Nếu P thì Q.          Nếu điện thoại hết pin thì nó tắt nguồn.
P.                    Điện thoại hết pin.
-----------           ----------------------------------------
Q.                    Nó tắt nguồn.
```

### Modus tollens (phủ định hậu kiện)

```text
Nếu P thì Q.          Nếu có trộm vào nhà thì con chó đã sủa.
Không Q.              Con chó không sủa.
-----------           ----------------------------------------
Không P.              Không có trộm vào nhà.
```

Modus tollens là công cụ của nhà khoa học và của người bác bỏ: nếu một giả thuyết dự đoán Q mà Q không xảy ra, giả thuyết có vấn đề. (Lập luận về con chó hợp lệ; còn có vững chắc hay không thì tùy P1. Trộm quen mặt chó thì sao?)

### Tam đoạn luận nhất quyết

Một **tam đoạn luận** (*syllogism*) nhất quyết có hai tiền đề và một kết luận, nói về quan hệ giữa các nhóm sự vật. Khuôn nổi tiếng nhất, được các nhà logic thời Trung cổ đặt tên là *Barbara*:

```text
Mọi M là P.           Mọi người đều phải chết.
Mọi S là M.           Mọi nhà thơ đều là người.
-----------           -------------------------
Mọi S là P.           Mọi nhà thơ đều phải chết.
```

Ví dụ kinh điển "Mọi người đều phải chết; Socrates là người; vậy Socrates phải chết" là người anh em gần của Barbara, với một cá nhân thay cho một nhóm. Nó cũng hợp lệ.

Hãy hình dung các vòng tròn: vòng "nhà thơ" nằm trong vòng "người", vòng "người" nằm trong vòng "phải chết". Vậy vòng "nhà thơ" nằm trong vòng "phải chết".

### Tam đoạn luận giả định

```text
Nếu P thì Q.          Nếu mất điện thì máy bơm ngừng.
Nếu Q thì R.          Nếu máy bơm ngừng thì bể nước cạn.
-----------           -----------------------------------
Nếu P thì R.          Nếu mất điện thì bể nước cạn.
```

### Tam đoạn luận lựa chọn

```text
P hoặc Q.             Chìa khóa ở trong cặp hoặc ở trên bàn.
Không P.              Không có trong cặp.
-----------           ----------------------------------------
Q.                    Nó ở trên bàn.
```

Cẩn thận với chiều ngược lại: "P hoặc Q; P; vậy không Q" *không* hợp lệ, vì "hoặc" thường để ngỏ khả năng cả hai cùng đúng. "Anh ấy giỏi tiếng Anh hoặc giỏi tiếng Pháp. Anh ấy giỏi tiếng Anh. Vậy anh ấy không giỏi tiếng Pháp" là một bước nhảy. Chỉ khi tiền đề nói rõ "chỉ một trong hai" thì bước đó mới hợp lệ.

## Hai cái bẫy đối xứng {#hai-cai-bay-doi-xung}

Hai khuôn hợp lệ đầu tiên có hai "người anh em sinh đôi" không hợp lệ. Chúng trông giống đến mức rất dễ nhầm.

**Khẳng định hậu kiện** (*affirming the consequent*): đó là lỗi của chị Thu.

```text
Nếu P thì Q.          Nếu trời mưa thì sân ướt.
Q.                    Sân ướt.
-----------           -------------------------
P.          ✗         Trời mưa.
```

Sân có thể ướt vì rửa xe, vì vỡ ống nước, vì sương đêm.

**Phủ định tiền kiện** (*denying the antecedent*):

```text
Nếu P thì Q.          Nếu trời mưa thì sân ướt.
Không P.              Trời không mưa.
-----------           -------------------------
Không Q.    ✗         Sân không ướt.
```

Lý do hệt như trên: mưa không phải con đường duy nhất làm sân ướt. Câu "nếu P thì Q" chỉ nói P là **điều kiện đủ** cho Q, không nói P là **điều kiện cần**.

Mẹo nhớ: với "nếu P thì Q", *khẳng định cái đầu* (P) hoặc *phủ định cái đuôi* (không Q) thì an toàn. *Khẳng định cái đuôi* hoặc *phủ định cái đầu* thì không.

## Phương pháp phản ví dụ {#phuong-phap-phan-vi-du}

Làm sao chứng minh một lập luận *không* hợp lệ? Nói "tôi thấy nó không thuyết phục" chưa đủ. Có một cách gọn gàng và dứt khoát, gọi là phương pháp **phản ví dụ** (*counterexample*):

1. Rút ra hình thức của lập luận (thay nội dung bằng chữ cái).
2. Điền vào hình thức đó một nội dung mới, sao cho mọi tiền đề *rõ ràng đúng* và kết luận *rõ ràng sai*.
3. Nếu làm được, hình thức đó không hợp lệ: nó không bảo đảm kết luận, nên lập luận ban đầu không thể dựa vào nó để buộc kết luận phải đúng.

Ví dụ, có người nói: "Mọi người ăn chay đều không ăn thịt bò. Lan không ăn thịt bò. Vậy Lan ăn chay."

```text
Hình thức:  Mọi A là B.  x là B.  Vậy x là A.

Phản ví dụ: Mọi con chó đều là động vật.          (đúng)
            Con mèo nhà tôi là động vật.          (đúng)
            Vậy con mèo nhà tôi là con chó.       (sai)
```

Phản ví dụ không chứng minh Lan *không* ăn chay. Có thể cô ấy ăn chay thật. Nó chỉ chứng minh rằng *lý do được đưa ra* không đủ để buộc kết luận phải đúng. Đó là hai chuyện khác nhau, và phân biệt được chúng là một nửa của tư duy phản biện.

!!! warning "Tiền đề phải thật sự đúng"
    Phản ví dụ chỉ có tác dụng khi tiền đề đúng một cách không thể bàn cãi và kết luận sai một cách không thể bàn cãi. "Mọi con cá đều là chim; mọi con mèo đều là chim; vậy mọi con cá đều là mèo" có kết luận sai, nhưng tiền đề cũng sai, nên nó không chứng minh được gì.

## Mẫu nhận diện {#mau-nhan-dien}

**Dấu hiệu của lập luận suy diễn:** từ chỉ báo kiểu "tất yếu", "nhất định", "chắc chắn suy ra", "không thể khác"; các từ "mọi", "tất cả", "không ai", "nếu… thì…", "hoặc… hoặc…".

**Bảng tra nhanh với "nếu P thì Q":**

```text
Có thêm          Rút ra          Tên gọi                     Hợp lệ?
P                Q               modus ponens                CÓ
không Q          không P         modus tollens               CÓ
Q                P               khẳng định hậu kiện         KHÔNG
không P          không Q         phủ định tiền kiện          KHÔNG
```

**Ba câu hỏi đánh giá:**

1. Hình thức của lập luận là gì? Có khớp với khuôn hợp lệ nào không?
2. Nếu không chắc, có tìm được phản ví dụ không?
3. Nếu hợp lệ: các tiền đề có thật sự đúng không? (Vững chắc hay không.)

## Bài tập {#bai-tap}

**Bài 1.** Hợp lệ hay không? Nếu không, gọi tên lỗi.

> "Nếu Nam đỗ đại học thì bố mẹ sẽ mua cho Nam xe máy. Bố mẹ vừa mua cho Nam xe máy. Vậy Nam đã đỗ đại học."

??? success "Xem gợi ý đáp án"
    Không hợp lệ: khẳng định hậu kiện (nếu P thì Q; Q; vậy P). Bố mẹ có thể mua xe vì lý do khác, chẳng hạn Nam đi làm thêm xa nhà.

**Bài 2.** Hợp lệ hay không? Có vững chắc không?

> "Nếu tài khoản của tôi bị xâm nhập thì tôi sẽ nhận được email cảnh báo đăng nhập lạ. Tôi không nhận được email cảnh báo nào. Vậy tài khoản của tôi không bị xâm nhập."

??? success "Xem gợi ý đáp án"
    Hợp lệ: đây là modus tollens (nếu P thì Q; không Q; vậy không P). Nhưng có vững chắc hay không thì đáng ngờ. Tiền đề thứ nhất có thể sai: kẻ xâm nhập tinh vi có thể xóa email cảnh báo, hoặc hệ thống không phát hiện được lần đăng nhập đó. Hợp lệ không cứu được một tiền đề sai.

**Bài 3.** Dùng phương pháp phản ví dụ để chứng minh lập luận sau không hợp lệ.

> "Tất cả nhân viên công ty X đều có bảo hiểm y tế. Chị Hoa có bảo hiểm y tế. Vậy chị Hoa là nhân viên công ty X."

??? success "Xem gợi ý đáp án"
    Hình thức: Mọi A là B; x là B; vậy x là A. Phản ví dụ: "Mọi con chim sẻ đều có lông vũ. Con đại bàng này có lông vũ. Vậy con đại bàng này là chim sẻ." Tiền đề đúng, kết luận sai, nên hình thức không hợp lệ.

**Bài 4.** Hợp lệ hay không?

> "Máy tính không lên là do hỏng phần cứng hoặc do lỗi phần mềm. Kỹ thuật viên đã kiểm tra: phần cứng không hỏng. Vậy là lỗi phần mềm."

??? success "Xem gợi ý đáp án"
    Hợp lệ: tam đoạn luận lựa chọn (P hoặc Q; không P; vậy Q). Câu hỏi còn lại là tiền đề thứ nhất có đúng không: có thật chỉ có hai khả năng đó? Có thể là do mất điện, do dây sạc. Nếu tiền đề lựa chọn bỏ sót khả năng, ta có một **lưỡng nan giả**, xem bài [Ngụy biện](nguy-bien.md#false-dilemma).

**Bài 5.** Lập luận sau mắc lỗi gì? Tìm một phản ví dụ.

> "Nếu một người là bác sĩ thì người đó đã tốt nghiệp đại học. Chị Mai không phải bác sĩ. Vậy chị Mai chưa tốt nghiệp đại học."

??? success "Xem gợi ý đáp án"
    Phủ định tiền kiện (nếu P thì Q; không P; vậy không Q). Phản ví dụ: "Nếu một con vật là con chó thì nó là động vật có vú. Con mèo không phải con chó. Vậy con mèo không phải động vật có vú." Tiền đề đúng, kết luận sai.

## Tự kiểm tra {#tu-kiem-tra}

Thử xem bạn nắm được đến đâu.

<div class="oz-quiz" data-id="deduction-1" data-skill="deduction" markdown="0">
<script type="application/json">
[
 {"q": "Khẳng định nào đúng?", "options": ["Một lập luận hợp lệ luôn có kết luận đúng", "Một lập luận hợp lệ có thể có kết luận sai, nếu có ít nhất một tiền đề sai", "Một lập luận có tiền đề đúng và kết luận đúng thì chắc chắn hợp lệ", "Một lập luận không hợp lệ luôn có kết luận sai"], "answer": 1, "explain": "Hợp lệ chỉ bảo đảm: tiền đề đúng thì kết luận đúng. Nếu có tiền đề sai, kết luận có thể sai (ví dụ chim cánh cụt biết bay). Lập luận về Hà Nội cho thấy tiền đề đúng, kết luận đúng mà vẫn không hợp lệ; và lập luận không hợp lệ vẫn có thể tình cờ có kết luận đúng."},
 {"q": "“Nếu giả thuyết đúng thì nước sẽ sôi ở 80 độ. Nước không sôi ở 80 độ. Vậy giả thuyết sai.” Đây là khuôn nào?", "options": ["Modus ponens", "Modus tollens", "Khẳng định hậu kiện", "Phủ định tiền kiện"], "answer": 1, "explain": "Nếu P thì Q; không Q; vậy không P: phủ định hậu kiện, tức modus tollens. Đây là khuôn hợp lệ."},
 {"q": "“Nếu tôi uống cà phê sau 4 giờ chiều thì tôi mất ngủ. Đêm qua tôi mất ngủ. Vậy chiều qua tôi đã uống cà phê sau 4 giờ.” Lập luận này thế nào?", "options": ["Hợp lệ, vì là modus ponens", "Hợp lệ, vì là modus tollens", "Không hợp lệ: khẳng định hậu kiện", "Không hợp lệ: phủ định tiền kiện"], "answer": 2, "explain": "Nếu P thì Q; Q; vậy P. Mất ngủ có thể do nhiều nguyên nhân khác, nên Q đúng không buộc P đúng."},
 {"q": "Một lập luận vững chắc là lập luận…", "options": ["có kết luận mà mọi người đồng ý", "hợp lệ và có mọi tiền đề đúng", "có tiền đề đúng, bất kể hình thức", "hợp lệ, bất kể tiền đề"], "answer": 1, "explain": "Vững chắc = hợp lệ + mọi tiền đề đúng. Chỉ khi có cả hai điều này, kết luận mới chắc chắn đúng."},
 {"q": "Cần chứng minh hình thức “Mọi A là B; mọi C là B; vậy mọi A là C” không hợp lệ. Phản ví dụ nào làm được việc đó?", "options": ["Mọi con chó là động vật; mọi con mèo là động vật; vậy mọi con chó là mèo", "Mọi con chó là động vật; mọi động vật là sinh vật; vậy mọi con chó là sinh vật", "Mọi con cá là chim; mọi con mèo là chim; vậy mọi con cá là mèo", "Mọi con chó là động vật; mọi con chó là sinh vật; vậy mọi động vật là sinh vật"], "answer": 0, "explain": "Lựa chọn A có cùng hình thức, tiền đề đúng, kết luận sai, nên nó là phản ví dụ. B và D có hình thức khác. C có cùng hình thức nhưng tiền đề sai, nên không chứng minh được gì."}
]
</script>
</div>

## Đi tiếp {#di-tiep}

Suy diễn cho ta sự chắc chắn, nhưng với một cái giá: kết luận không bao giờ đi xa hơn những gì đã nằm sẵn trong tiền đề. Phần lớn đời sống, từ chẩn đoán bệnh đến dự báo thời tiết, đòi hỏi ta đi xa hơn thế. Mời đọc [Khi bằng chứng chỉ làm cho có lẽ đúng](quy-nap.md).

## Nguồn {#nguon}

1. Jc Beall, Greg Restall và Gil Sagi, "Logical Consequence", *Stanford Encyclopedia of Philosophy*. <https://plato.stanford.edu/entries/logical-consequence/>
2. Timothy Shanahan, "Deductive and Inductive Arguments", *Internet Encyclopedia of Philosophy*. <https://iep.utm.edu/deductive-inductive-arguments/>
3. Bradley Dowden, "Fallacies", *Internet Encyclopedia of Philosophy* (các mục "Affirming the Consequent" và "Denying the Antecedent"). <https://iep.utm.edu/fallacy/>
