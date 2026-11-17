---
title: "Bảng chân trị: khi lập luận thành phép tính"
description: Mệnh đề là gì, sáu phép nối với bảng chân trị của từng phép, cách đọc bảng của công thức phức, và cách kiểm tra một lập luận hợp lệ bằng bảng chân trị — cùng giới hạn của logic mệnh đề.
skill: logic
updated: 2026-10-22
tier: loi
block: cong-cu
---

# Bảng chân trị: khi lập luận thành phép tính

Bố hứa với cu Tí: "Nếu con được 10 điểm toán thì bố mua xe đạp." Cuối kỳ, Tí được 9,5. Bố không mua xe. Tí phụng phịu: "Bố nuốt lời!"

Bố có nuốt lời không? Lời hứa "nếu P thì Q" chỉ bị phá vỡ trong đúng một trường hợp: P xảy ra mà Q không xảy ra — được 10 điểm mà không có xe. Tí được 9,5: lời hứa không nói gì về trường hợp này cả. Bố không nuốt lời; Tí giận cũng dễ hiểu, nhưng giận sai chỗ.

Câu chuyện nhỏ này chứa toàn bộ ý tưởng của bài: chân trị **đúng** hay **sai** của một câu "nếu… thì…" được quyết định máy móc bởi chân trị của hai vế, theo một bảng tra cứu cố định. Bài này dựng bảng tra cứu ấy cho mọi phép nối, rồi dùng nó như một cái máy: bỏ lập luận vào, quay tay, biết ngay hợp lệ hay không.

## Mệnh đề: câu có chân trị {#menh-de-cau-co-chan-tri}

Một **mệnh đề** là một câu khẳng định mà ta có thể nói nó **đúng** hay **sai** — người ta gọi đó là **chân trị** (*truth value*) của câu. "Hà Nội là thủ đô của Việt Nam" là một mệnh đề (chân trị: đúng). "2 + 2 = 5" cũng là một mệnh đề (chân trị: sai). Sai vẫn là mệnh đề, miễn là ta xác định được nó sai.

Những câu sau *không* là mệnh đề:

- Câu hỏi: "Mấy giờ rồi?"
- Mệnh lệnh: "Đóng cửa lại!"
- Câu cảm thán: "Trời ơi!"
- Câu mơ hồ, không xác định được đúng sai: "Phở ngon." (Phở nào? Ngon với ai?)

**Logic mệnh đề** (*propositional logic*) chỉ làm việc với mệnh đề, và coi mỗi mệnh đề đơn giản là một khối không thể chia nhỏ: đúng hoặc sai, không có thứ ba. Phần còn lại của bài là: từ những khối ấy, ta lắp ghép câu phức bằng các **phép nối**, và chân trị của câu phức được tính *máy móc* từ chân trị của các khối thành phần. Bảng ghi lại cách tính ấy gọi là **bảng chân trị** (*truth table*) — ý tưởng đã ngầm có trong công trình của Peirce, Jevons, Venn ở thế kỷ XIX và xuất hiện tường minh từ năm 1909, nhưng chỉ trở nên phổ biến từ đầu thập niên 1920, nhờ Emil Post (1921) và [Wittgenstein](../triet-gia/wittgenstein.md) (*Tractatus*, 1921).

Trong các bảng dưới đây, Đ = đúng, S = sai.

## Sáu phép nối {#sau-phep-noi}

### Phủ định: ¬

"Không P", ký hiệu ¬P. Đảo chân trị.

| P | ¬P |
|---|----|
| Đ | S |
| S | Đ |

"Trời không mưa" đúng chính khi "trời mưa" sai.

### Hội: ∧ ("và")

P ∧ Q đúng khi *cả hai* cùng đúng.

| P | Q | P ∧ Q |
|---|---|-------|
| Đ | Đ | Đ |
| Đ | S | S |
| S | Đ | S |
| S | S | S |

"Lan được 10 điểm toán và được 10 điểm văn" — chỉ cần một môn không được 10 là cả câu sai.

### Tuyển: ∨ ("hoặc", bao hàm)

P ∨ Q sai *chỉ khi* cả hai cùng sai; còn lại đúng.

| P | Q | P ∨ Q |
|---|---|-------|
| Đ | Đ | Đ |
| Đ | S | Đ |
| S | Đ | Đ |
| S | S | S |

Chú ý: "hoặc" ở đây là **bao hàm** — cả hai cùng đúng vẫn được. "Ai nộp bài trước 5 giờ hoặc có giấy phép thì được dự thi": người vừa nộp sớm vừa có giấy phép vẫn được dự thi. Trong đời thường, "hoặc" đôi khi mang nghĩa loại trừ ("hoặc trà hoặc cà phê, chọn một thôi"), nhưng trong logic, ∨ luôn bao hàm trừ khi nói rõ.

### Kéo theo: → ("nếu… thì…")

Đây là phép quan trọng nhất — và dễ gây hiểu lầm nhất. P → Q **sai trong đúng một trường hợp**: P đúng mà Q sai. Đó chính là bài học từ lời hứa của bố Tí.

| P | Q | P → Q |
|---|---|-------|
| Đ | Đ | Đ |
| Đ | S | S |
| S | Đ | Đ |
| S | S | Đ |

Hai dòng cuối gây ngạc nhiên: "nếu 2 + 2 = 5 thì Hà Nội là thủ đô" được tính là đúng, vì tiền kiện sai. Trong logic, → không đòi hỏi quan hệ nhân quả giữa hai vế; nó chỉ là một cách tính chân trị. "Nếu… thì…" trong đời thường giàu hơn thế (nó gợi ý nguyên nhân, lời hứa, quy luật), nhưng khi kiểm tra *hình thức* của lập luận, ta chỉ dùng bảng này.

### Tương đương: ↔ ("khi và chỉ khi")

P ↔ Q đúng khi hai vế *cùng* chân trị.

| P | Q | P ↔ Q |
|---|---|-------|
| Đ | Đ | Đ |
| Đ | S | S |
| S | Đ | S |
| S | S | Đ |

"Bạn được vào vòng trong khi và chỉ khi bạn qua vòng loại": qua vòng loại mà không được vào, hoặc được vào mà chưa qua vòng loại — cả hai đều phá vỡ câu này.

### Tuyển loại trừ: ⊕ ("hoặc… hoặc…", chọn một)

P ⊕ Q đúng khi *đúng một* trong hai đúng.

| P | Q | P ⊕ Q |
|---|---|-------|
| Đ | Đ | S |
| Đ | S | Đ |
| S | Đ | Đ |
| S | S | S |

"Hoặc đi xe buýt hoặc đi xe ôm, chọn một phương tiện thôi": đi cả hai hoặc chẳng đi cái nào đều sai với câu này.

## Độ ưu tiên: ai tính trước {#do-uu-tien-ai-tinh-truoc}

Khi một công thức có nhiều phép nối, thứ tự tính là: **¬ trước, rồi ∧, rồi ∨, rồi →, cuối cùng ↔**. Ngoặc luôn được ưu tiên cao nhất; với ⊕, cứ viết ngoặc cho rõ.

Ví dụ: ¬P ∨ Q → R được đọc là ((¬P) ∨ Q) → R.

Quy tắc này giống "nhân trước cộng sau" trong số học: một ước lệ để khỏi phải viết ngoặc khắp nơi. Khi không chắc, cứ thêm ngoặc — rõ ràng hơn là tiếc mực.

## Đọc bảng chân trị của công thức phức {#doc-bang-chan-tri-cua-cong-thuc-phuc}

Muốn biết chân trị của một công thức phức, ta lập bảng liệt kê *mọi* khả năng chân trị của các mệnh đề thành phần, rồi tính từng cột từ trong ra ngoài. Với n mệnh đề khác nhau, bảng có 2ⁿ dòng.

Ví dụ: kiểm tra xem ¬(P ∧ Q) có tương đương ¬P ∨ ¬Q không (luật De Morgan):

| P | Q | P ∧ Q | ¬(P ∧ Q) | ¬P | ¬Q | ¬P ∨ ¬Q |
|---|---|-------|----------|----|----|---------|
| Đ | Đ | Đ | S | S | S | S |
| Đ | S | S | Đ | S | Đ | Đ |
| S | Đ | S | Đ | Đ | S | Đ |
| S | S | S | Đ | Đ | Đ | Đ |

Hai cột ¬(P ∧ Q) và ¬P ∨ ¬Q giống hệt nhau trên mọi dòng: hai công thức **tương đương logic**. Nói bằng lời: "không phải (vừa P vừa Q)" cũng như "hoặc không P hoặc không Q". "Không phải vừa mưa vừa nắng" nghĩa là "hoặc không mưa hoặc không nắng" — nghe rất tự nhiên, và bảng chân trị chứng minh nó đúng một cách máy móc.

Một công thức đúng trên *mọi* dòng gọi là **hằng đúng** (*tautology*), ví dụ P ∨ ¬P ("hoặc P hoặc không P"). Một công thức sai trên mọi dòng gọi là **hằng sai** (*contradiction*), ví dụ P ∧ ¬P.

## Kiểm tra hợp lệ bằng bảng chân trị {#kiem-tra-hop-le-bang-bang-chan-tri}

Bài [Suy diễn](suy-dien.md) định nghĩa: một lập luận **hợp lệ** (*valid*) khi không thể có chuyện mọi tiền đề đúng mà kết luận sai. Bảng chân trị biến định nghĩa ấy thành một thủ tục: **lập luận hợp lệ khi và chỉ khi mọi dòng làm mọi tiền đề đúng đều làm kết luận đúng.**

Kiểm tra modus ponens (nếu P thì Q; P; vậy Q):

| P | Q | P → Q | P | Q |
|---|---|-------|---|---|
| Đ | Đ | Đ | Đ | Đ |
| Đ | S | S | Đ | S |
| S | Đ | Đ | S | Đ |
| S | S | Đ | S | S |

Tiền đề là hai cột "P → Q" và "P". Chỉ có dòng 1 làm cả hai cùng đúng — và ở dòng đó, kết luận Q cũng đúng. Không có dòng nào "tiền đề đúng, kết luận sai". Vậy modus ponens hợp lệ — ta vừa *chứng minh* điều bài Suy diễn đã giới thiệu.

Giờ kiểm tra khẳng định hậu kiện (nếu P thì Q; Q; vậy P) — lỗi của chị Thu:

| P | Q | P → Q | Q | P |
|---|---|-------|---|---|
| Đ | Đ | Đ | Đ | Đ |
| Đ | S | S | S | Đ |
| S | Đ | Đ | Đ | S |
| S | S | Đ | S | S |

Dòng 3: cả hai tiền đề đúng (P → Q đúng, Q đúng) mà kết luận P sai. Dòng này chính là một **phản ví dụ** (*counterexample*): sân ướt (Q đúng) nhưng trời không mưa (P sai) — vì có người rửa xe. Lập luận không hợp lệ.

Công cụ dưới đây làm đúng việc này: bạn nhập tiền đề và kết luận, nó dựng bảng chân trị và chỉ ra dòng phản ví dụ nếu có.

<div class="oz-logic"></div>

## Giới hạn: những gì bảng chân trị không thấy {#gioi-han-nhung-gi-bang-chan-tri-khong-thay}

Logic mệnh đề rất mạnh trong phạm vi của nó, nhưng phạm vi ấy có biên. Nó coi mỗi mệnh đề là một khối không chia được, nên nó **không xử lý được lượng từ** ("mọi", "tồn tại") và **vị từ** (tính chất, quan hệ bên trong câu).

Ví dụ kinh điển:

```text
P1. Mọi người đều phải chết.
P2. Socrates là người.
-------------------------
K.  Socrates phải chết.
```

Với logic mệnh đề, P1 và P2 chỉ là hai khối A, B chẳng liên quan gì nhau; từ A, B không thể suy ra K. Muốn "nhìn vào bên trong" các câu — thấy được "mọi", thấy được "là người" — cần **logic vị từ**, một hệ mạnh hơn. Tương tự, "An cao hơn Bình" chứa một *quan hệ* giữa hai người mà mệnh đề nguyên tử không diễn tả được.

Quy tắc thực hành: khi một lập luận dùng các từ "mọi", "có", "tồn tại", hoặc nói về quan hệ giữa các đối tượng, bảng chân trị không phải công cụ phù hợp. Nó không sai — nó chỉ không đủ.

## Bài tập {#bai-tap}

**Bài 1.** Viết bảng chân trị của ¬P ∨ Q rồi so sánh với bảng của P → Q. Kết luận gì?

??? success "Xem gợi ý đáp án"
    | P | Q | ¬P | ¬P ∨ Q |
    |---|---|----|--------|
    | Đ | Đ | S | Đ |
    | Đ | S | S | S |
    | S | Đ | Đ | Đ |
    | S | S | Đ | Đ |

    Cột ¬P ∨ Q trùng hệt cột P → Q: hai công thức tương đương logic. "Nếu P thì Q" cũng như "hoặc không P hoặc Q".

**Bài 2.** Công thức (P → Q) ∧ P → Q có phải hằng đúng không? Vì sao điều đó liên quan đến modus ponens?

??? success "Xem gợi ý đáp án"
    Có. Viết bảng 4 dòng: cột (P → Q) ∧ P chỉ đúng ở dòng P đúng, Q đúng; ở dòng đó Q cũng đúng, nên cả công thức → Q luôn đúng. Một lập luận hợp lệ chính là một công thức "các tiền đề kéo theo kết luận" là hằng đúng.

**Bài 3.** Dùng bảng chân trị kiểm tra: "Nếu P thì Q; không Q; vậy không P" (modus tollens) có hợp lệ không?

??? success "Xem gợi ý đáp án"
    Hợp lệ. Các dòng làm cả hai tiền đề (P → Q và ¬Q) cùng đúng: chỉ có dòng P sai, Q sai. Ở dòng đó kết luận ¬P đúng. Không có dòng phản ví dụ.

**Bài 4.** "Hoặc An hoặc Bình trực nhật (chỉ một người). An không trực nhật. Vậy Bình trực nhật." Dùng phép nối nào để mô hình hóa? Lập luận có hợp lệ không?

??? success "Xem gợi ý đáp án"
    Dùng ⊕ (tuyển loại trừ): P ⊕ Q; ¬P; vậy Q. Bảng chân trị: dòng duy nhất làm cả hai tiền đề đúng là P sai, Q đúng; kết luận Q đúng ở dòng đó. Hợp lệ. Chú ý: nếu "hoặc" ở đây là ∨ bao hàm thì lập luận vẫn hợp lệ (tam đoạn luận lựa chọn). Khác biệt giữa ⊕ và ∨ chỉ lộ ra ở chiều ngược lại: biết *An có trực*, thì với ⊕ suy ra được Bình không trực, còn với ∨ thì không.

**Bài 5.** Tìm một công thức là hằng sai (sai trên mọi dòng) với hai mệnh đề P, Q.

??? success "Xem gợi ý đáp án"
    Ví dụ: (P ∨ Q) ∧ ¬P ∧ ¬Q, hay đơn giản P ∧ ¬P (không cần Q). Kiểm tra: P ∧ ¬P không bao giờ cùng đúng nên cả hội luôn sai.

## Tự kiểm tra {#tu-kiem-tra}

Thử xem bạn nắm được đến đâu.

<div class="oz-quiz" data-id="logic-1" data-skill="logic" markdown="0">
<script type="application/json">
[
 {"q": "Câu nào sau đây là một mệnh đề?", "options": ["Mấy giờ rồi?", "Đóng cửa lại!", "Hà Nội là thủ đô của Việt Nam", "Trời ơi!"], "answer": 2, "explain": "Mệnh đề là câu khẳng định có chân trị đúng/sai. Câu hỏi, mệnh lệnh, cảm thán không có chân trị nên không phải mệnh đề."},
 {"q": "P → Q sai trong trường hợp duy nhất nào?", "options": ["P đúng, Q đúng", "P đúng, Q sai", "P sai, Q đúng", "P sai, Q sai"], "answer": 1, "explain": "Kéo theo chỉ sai khi tiền kiện đúng mà hậu kiện sai — như lời hứa bị phá vỡ: được 10 điểm mà không có xe đạp."},
 {"q": "Công thức nào tương đương logic với ¬(P ∧ Q)?", "options": ["¬P ∧ ¬Q", "¬P ∨ ¬Q", "P ∨ ¬Q", "¬P → ¬Q"], "answer": 1, "explain": "Luật De Morgan: phủ định của hội bằng tuyển của các phủ định. Kiểm tra bằng bảng chân trị 4 dòng, hai cột trùng nhau hoàn toàn."},
 {"q": "Xét lập luận: “Nếu P thì Q; Q; vậy P”. Dòng nào của bảng chân trị là phản ví dụ chứng tỏ nó không hợp lệ?", "options": ["P đúng, Q đúng", "P đúng, Q sai", "P sai, Q đúng", "P sai, Q sai"], "answer": 2, "explain": "Ở dòng P sai, Q đúng: P → Q đúng, Q đúng (mọi tiền đề đúng) mà P sai (kết luận sai). Đây chính là trường hợp sân ướt nhưng trời không mưa."},
 {"q": "Logic mệnh đề KHÔNG xử lý được loại câu nào sau đây?", "options": ["Câu có phép nối “và”", "Câu có “nếu… thì…”", "Câu có lượng từ “mọi” / “tồn tại”", "Câu phủ định"], "answer": 2, "explain": "Logic mệnh đề coi mỗi mệnh đề là khối không chia được, nên không “nhìn vào trong” để xử lý lượng từ hay vị từ. Muốn vậy cần logic vị từ."}
]
</script>
</div>

## Đi tiếp {#di-tiep}

"Nếu P thì Q" nói P là điều kiện **đủ** cho Q — nhưng nó có nói P là điều kiện **cần** không? Hai khái niệm này dễ bị đánh tráo cho nhau, và đó là nguồn gốc của nhiều lập luận hỏng. Mời đọc [Cần khác đủ như thế nào?](dieu-kien-can-du.md).

Bảng chân trị coi "đúng" và "sai" là những giá trị có sẵn. [Sự thật là gì?](../cau-hoi/chan-ly.md) hỏi có chân trị nghĩa là gì, và vì sao câu "câu này sai" làm logic lúng túng.

## Nguồn {#nguon}

1. Kevin C. Klement, "Propositional Logic", *Internet Encyclopedia of Philosophy* (mục lịch sử: bảng chân trị trước Post và Wittgenstein). <https://iep.utm.edu/prop-log/>
2. Jc Beall, Greg Restall và Gil Sagi, "Logical Consequence", *Stanford Encyclopedia of Philosophy*. <https://plato.stanford.edu/archives/fall2026/entries/logical-consequence/>
