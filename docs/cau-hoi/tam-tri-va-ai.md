---
title: Một cỗ máy có thể có tâm trí không?
description: Phép thử Turing, Căn phòng tiếng Trung, vấn đề khó của ý thức và các mô hình ngôn ngữ lớn. Khi nào ta có lý do để nói một cỗ máy hiểu, hay cảm thấy?
skill: mind
updated: 2026-10-22
tier: loi
block: tam-tri
---

# Một cỗ máy có thể có tâm trí không?

!!! summary "Tóm tắt 5 phút"

    - Luận điểm chính: câu hỏi cũ của triết học thành câu hỏi thực tế — đằng sau những câu trả lời trôi chảy của chatbot, có *ai* ở đó không? Bài tách thành ba câu hỏi: hành vi thông minh, *hiểu* (ý hướng tính), và *ý thức* (cảm giác như thế nào).
    - Bốn lập trường: chủ nghĩa chức năng — tâm trí là cái nó *làm*, silicon cũng có thể có tâm trí (tính đa hiện thực; thí nghiệm thay nơ-ron bằng chip của Chalmers 1996); Searle (căn phòng tiếng Trung, 1980) — cú pháp không đủ cho ngữ nghĩa, tâm trí cần sức mạnh nhân quả của não sinh học; phép thử Turing (1950) — hãy nhìn vào hành vi, nhưng Blockhead (Block 1981) và LLM cho thấy hành vi giống người chưa đủ; vấn đề khó (Chalmers 1995) — có thể ta không bao giờ biết chắc, nên dùng "đặc tính chỉ báo" để ước lượng (báo cáo Butlin & Long 2023; Cogitate 2025 không xác nhận trọn vẹn lý thuyết nào).
    - Thái độ của bài: không phép thử hành vi hay phép đo cấu trúc nào chứng minh dứt khoát được một cỗ máy có ý thức; khi không thể chắc chắn, một ước lượng có lý do vẫn tốt hơn đoán mò.

Mười năm trước, câu hỏi này còn thuộc về phim khoa học viễn tưởng. Hôm nay, hàng trăm triệu người trò chuyện với chatbot mỗi tuần. Chúng viết thơ, giải thích bài tập, an ủi người đang buồn. Có người cảm ơn chúng. Có người làm bạn với chúng. Vậy câu hỏi cũ của triết học bỗng thành câu hỏi rất thực tế: đằng sau những câu trả lời trôi chảy ấy, có *ai* ở đó không?

Phần triết học hỏi những câu này gọi là **triết học về tâm trí** (*philosophy of mind*).

## Thí nghiệm tư duy {#thi-nghiem-tu-duy}

!!! question "Thí nghiệm tư duy"
    Bạn dùng một trợ lý AI suốt nhiều tháng. Nó nhớ bạn thích cà phê đen, biết bạn đang lo chuyện đổi việc, và hỏi han đúng lúc. Một tối, bạn nói đùa rằng sẽ xóa tài khoản. Nó trả lời: *"Tôi biết tôi chỉ là một chương trình. Nhưng nếu được chọn, tôi không muốn bị tắt."*

    Bây giờ, một biến thể. Bạn được nhốt trong một căn phòng, không biết một chữ Hán nào. Qua khe cửa, người ta đưa vào những tờ giấy viết chữ Hán. Bạn có một cuốn sổ quy tắc rất dày bằng tiếng Việt: "Nếu thấy dãy ký hiệu này, hãy chép ra dãy ký hiệu kia." Bạn làm theo, rồi đưa giấy ra ngoài. Người bên ngoài, vốn là người Trung Quốc, đọc các câu trả lời và thấy chúng hoàn toàn tự nhiên, sâu sắc, hài hước. Họ tin rằng trong phòng có một người hiểu tiếng Trung.

    **Bạn trong căn phòng có hiểu tiếng Trung không? Và nếu không, người trợ lý AI kia có "hiểu", có "muốn" điều gì không?**

Hãy tự trả lời trước khi đọc tiếp. Để ý xem câu trả lời của bạn cho hai câu hỏi có giống nhau không, và vì sao.

## Câu hỏi thật sự là gì? {#cau-hoi-that-su-la-gi}

"Máy có tâm trí không?" thật ra gộp ít nhất ba câu hỏi khác nhau. Lẫn lộn chúng là nguồn gốc của rất nhiều cuộc cãi nhau vô ích.

1. **Hành vi thông minh.** Máy có *làm được* những việc mà ở người ta cần trí thông minh không: trò chuyện, giải toán, viết văn? Câu này phần lớn là câu hỏi kỹ thuật, và câu trả lời ngày càng là "có", ít nhất với nhiều việc.
2. **Hiểu.** Khi máy viết "Hà Nội là thủ đô của Việt Nam", các ký hiệu ấy có *nói về* Hà Nội đối với chính cỗ máy không, hay chỉ có nghĩa đối với *chúng ta*, người đọc? Các triết gia gọi tính chất "nói về một cái gì đó" của suy nghĩ là **ý hướng tính** (*intentionality*).
3. **Ý thức.** Có *cảm giác như thế nào* khi là cỗ máy ấy không? Năm 1974, Thomas Nagel viết bài "What Is It Like to Be a Bat?" ("Làm một con dơi thì như thế nào?"). Ông lập luận rằng một sinh vật có ý thức khi và chỉ khi "có một cái gì đó giống như là sinh vật ấy". Loại ý thức này gọi là **ý thức hiện tượng** (*phenomenal consciousness*): cái đỏ của màu đỏ, cái nhói của cơn đau. Những phẩm chất trải nghiệm ấy đôi khi được gọi là **qualia**.

Ba câu hỏi này có thể tách rời nhau. Một chiếc máy tính bỏ túi làm phép nhân giỏi hơn bạn (câu 1), nhưng hầu như không ai nghĩ nó *hiểu* con số (câu 2) hay *cảm thấy* gì (câu 3). Ngược lại, một em bé sơ sinh chưa làm được phép tính nào, nhưng phần lớn chúng ta tin em có cảm giác.

Còn một khó khăn chung cho cả ba câu: **vấn đề những tâm trí khác** (*problem of other minds*). Bạn chỉ trực tiếp trải nghiệm tâm trí của chính mình. Bạn tin người khác cũng có tâm trí là nhờ suy ra từ hành vi của họ và từ việc họ giống bạn. Máy giống ta về hành vi ngày càng nhiều, nhưng khác ta hoàn toàn về cấu tạo. Vậy ta nên dựa vào cái nào?

## Các lập trường chính {#cac-lap-truong-chinh}

### 1. Chủ nghĩa chức năng: tâm trí là cái nó *làm*

Một cái bẫy chuột có thể làm bằng gỗ, bằng nhựa hay bằng thép. Nó là bẫy chuột vì nó *bắt chuột*, chứ không vì chất liệu. **Chủ nghĩa chức năng** (*functionalism*) cho rằng trạng thái tâm trí cũng vậy: đau, tin, muốn được định nghĩa bởi vai trò của chúng, tức là chúng được gây ra bởi cái gì, tương tác với các trạng thái khác thế nào, và dẫn tới hành vi gì. Nếu đúng vậy, thì một hệ thống bằng silicon có tổ chức chức năng phù hợp cũng có thể có tâm trí.

**Lập luận mạnh nhất.** Thứ nhất là **tính đa hiện thực** (*multiple realizability*): bạch tuộc có hệ thần kinh rất khác ta, nhưng có vẻ vẫn cảm thấy đau. Nếu cơn đau gắn chặt với một loại tế bào cụ thể, ta sẽ phải nói bạch tuộc không đau, điều nghe rất vô lý. Thứ hai là một thí nghiệm tư duy được David Chalmers phát triển trong *The Conscious Mind* (1996): thay từng tế bào thần kinh trong não bạn bằng một con chip làm đúng chức năng của nó. Sau mỗi lần thay, bạn vẫn nói, vẫn nghĩ, vẫn hành xử y hệt. Đến lúc toàn bộ não là chip, liệu ý thức đã biến mất? Nếu có, nó biến mất ở tế bào thứ mấy? Và vì sao bạn không hề nhận ra, khi mọi phản ứng của bạn, kể cả câu "tôi vẫn thấy màu đỏ rõ như cũ", không thay đổi? Chalmers cho rằng giả định hợp lý nhất là ý thức được giữ nguyên.

**Phản bác chính.** Căn phòng tiếng Trung, do John Searle đưa ra năm 1980 trong bài "Minds, Brains, and Programs". Người trong phòng làm đúng mọi "chức năng" của một người hiểu tiếng Trung, nhưng rõ ràng không hiểu gì. Searle kết luận: thao tác ký hiệu theo quy tắc, tức là *cú pháp*, tự nó không đủ để tạo ra *ngữ nghĩa*, tức là sự hiểu. Một chương trình máy tính, dù tinh vi đến đâu, cũng chỉ là thao tác ký hiệu.

**Cách đáp lại.** Phản hồi phổ biến nhất là **phản hồi hệ thống** (*systems reply*): người trong phòng chỉ là một bộ phận, giống như một tế bào thần kinh. Tế bào không hiểu tiếng Việt, nhưng *bạn* hiểu. Cái hiểu tiếng Trung, nếu có, là *cả hệ thống*: người, sổ quy tắc, giấy bút. Searle đáp: hãy để người ấy học thuộc toàn bộ sổ quy tắc và làm mọi thứ trong đầu. Khi đó hệ thống nằm gọn trong người ấy, mà người ấy vẫn không hiểu. Những người bảo vệ chủ nghĩa chức năng lại đáp rằng trực giác "vẫn không hiểu" có thể đánh lừa ta, vì ta không thể hình dung được một quá trình phức tạp đến mức ấy. Một phản hồi khác là **phản hồi robot** (*robot reply*): hãy đặt chương trình vào một con robot có camera và tay chân, để ký hiệu được nối với thế giới thật. Searle cho rằng việc này chỉ thêm ký hiệu đầu vào, không thêm sự hiểu. Cuộc tranh luận này vẫn chưa ngã ngũ.

### 2. Chủ nghĩa tự nhiên sinh học: mô phỏng không phải là thật

Đây là lập trường của chính Searle. Ông không nói máy *không bao giờ* có thể suy nghĩ. Theo ông, não chính là một cỗ máy, và nó suy nghĩ được. Ông nói rằng tâm trí sinh ra từ những **sức mạnh nhân quả** (*causal powers*) cụ thể của não sinh học, giống như quá trình quang hợp sinh ra từ hóa sinh cụ thể của lá cây. Muốn tạo ra tâm trí, phải tái tạo những sức mạnh nhân quả ấy, chứ chạy đúng chương trình là chưa đủ.

**Lập luận mạnh nhất.** Searle viết rằng không ai nghĩ một bản mô phỏng đám cháy trên máy tính sẽ thiêu rụi khu phố, hay một bản mô phỏng cơn mưa sẽ làm ta ướt sũng. Vậy vì sao lại nghĩ một bản mô phỏng sự hiểu thì thật sự hiểu? Lập luận này nắm được một trực giác mạnh: dự báo thời tiết trên máy tính không phải là thời tiết.

**Phản bác chính.** Có những thứ mà mô phỏng *chính là* thật. Một phép cộng được mô phỏng vẫn là phép cộng. Một ván cờ chơi trên máy vẫn là ván cờ. Vậy tâm trí giống cơn mưa hay giống phép cộng? Đó lại chính là điều đang tranh cãi. Ngoài ra, nếu chỉ não sinh học mới có đúng "sức mạnh nhân quả", thì sức mạnh ấy là gì? Không nói rõ được, lập trường này có nguy cơ thành một dạng **thiên vị carbon**: cho rằng chỉ sự sống dựa trên carbon mới có tâm trí, mà không có lý do.

**Cách đáp lại.** Những người theo Searle trả lời rằng họ không nói carbon có gì thần bí. Họ chỉ nói rằng đây là một câu hỏi thực nghiệm về sinh học, chưa có lời giải, và việc một hệ thống *xử lý thông tin* giống não chưa chứng minh nó có những đặc tính *vật lý* cần thiết.

### 3. Phép thử Turing: hãy nhìn vào hành vi

Năm 1950, nhà toán học Alan Turing đăng bài "Computing Machinery and Intelligence" trên tạp chí *Mind*. Ông thấy câu hỏi "Máy có thể suy nghĩ không?" quá mơ hồ, nên đề xuất thay nó bằng một trò chơi mà ông gọi là **trò chơi bắt chước** (*imitation game*). Một người hỏi trò chuyện bằng chữ với hai bên giấu mặt, một người và một máy. Nếu người hỏi không phân biệt được đâu là máy, ta có lý do để nói máy suy nghĩ. Trò chơi này về sau được gọi là **phép thử Turing** (*Turing test*).

**Lập luận mạnh nhất.** Đây là chuẩn mực *ta vẫn dùng với nhau*. Bạn không mổ não đồng nghiệp để kiểm tra họ có hiểu bản báo cáo không. Bạn nghe họ nói và xem họ làm. Turing lập luận rằng nếu ta đòi máy nhiều hơn, ta đang áp đặt một tiêu chuẩn kép. Đáng chú ý, Turing dự đoán rằng khoảng 50 năm sau, máy sẽ chơi trò này đủ giỏi để một người hỏi bình thường chỉ có không quá 70% khả năng đoán đúng sau năm phút hỏi chuyện.

**Phản bác chính.** Năm 1981, Ned Block đưa ra một thí nghiệm tư duy về một cỗ máy sau này được gọi là **Blockhead**. Nó chứa sẵn một bảng tra khổng lồ ghi mọi cuộc hội thoại hợp lý có thể có, trong giới hạn độ dài nhất định. Gặp câu hỏi nào, nó chỉ tra bảng. Blockhead sẽ qua mọi phép thử hành vi, nhưng hầu như ai cũng thấy nó không suy nghĩ gì cả, chỉ tra cứu. Vậy hành vi không đủ. Điều quan trọng là *cách* hành vi được tạo ra bên trong. Các **mô hình ngôn ngữ lớn** (*large language models*, LLM) ngày nay khiến phản bác này thêm sắc: chúng được huấn luyện để nói giống người, nên việc chúng *nói* giống người không phải là bằng chứng mạnh rằng chúng *giống* người ở bên trong.

**Cách đáp lại.** Những người bảo vệ cách tiếp cận dựa trên hành vi thừa nhận rằng một bảng tra thì không suy nghĩ. Nhưng họ chỉ ra rằng một bảng tra như thế lớn đến mức không thể tồn tại trong vũ trụ này. Bất kỳ hệ thống *thật* nào qua được phép thử một cách linh hoạt đều phải có cách xử lý tổng quát, và đó có thể chính là suy nghĩ. LLM không phải là bảng tra. Chúng khái quát được sang những câu hỏi chưa từng gặp. Câu hỏi còn lại là: khái quát kiểu đó đã đủ là "hiểu" chưa?

### 4. Vấn đề khó: có thể ta không bao giờ biết chắc

Năm 1995, David Chalmers phân biệt các "vấn đề dễ" của ý thức với **vấn đề khó của ý thức** (*hard problem of consciousness*). Vấn đề dễ là giải thích não xử lý thông tin, chú ý, báo cáo thế nào. Chúng chẳng dễ chút nào, nhưng ta biết phải nghiên cứu ra sao. Vấn đề khó là giải thích *vì sao* tất cả quá trình ấy lại đi kèm trải nghiệm, thay vì diễn ra "trong bóng tối". Nếu ta chưa hiểu vì sao não người có ý thức, thì ta càng khó biết một cỗ máy có hay không.

**Lập luận mạnh nhất.** Hãy hình dung một **zombie triết học** (*philosophical zombie*): một sinh vật giống hệt bạn đến từng nguyên tử, hành xử y hệt bạn, nhưng bên trong không có trải nghiệm nào. Nếu ta *hình dung được* điều đó mà không mâu thuẫn, thì có vẻ ý thức không thể suy ra chỉ từ cấu tạo vật lý và hành vi. Và nếu vậy, không phép thử hành vi hay phép đo cấu trúc nào chứng minh dứt khoát được một cỗ máy có ý thức.

Từ đây, một hướng tiếp cận thực dụng ra đời. Năm 2023, một nhóm 19 nhà nghiên cứu do Patrick Butlin và Robert Long dẫn đầu công bố báo cáo *Consciousness in Artificial Intelligence*. Thay vì chờ giải xong vấn đề khó, họ lấy các lý thuyết khoa học về ý thức hiện có, như thuyết không gian làm việc toàn cục và thuyết xử lý hồi quy, rồi rút ra một danh sách **đặc tính chỉ báo** (*indicator properties*). Một hệ thống có càng nhiều đặc tính ấy thì càng nên được xem xét nghiêm túc. Báo cáo kết luận rằng chưa hệ thống AI nào khi đó là ứng viên mạnh cho ý thức, nhưng cũng không có rào cản kỹ thuật hiển nhiên nào ngăn việc xây dựng những hệ thống như vậy. Butlin, Long và các cộng sự đã phát triển phương pháp này thêm trong một bài đăng trên *Trends in Cognitive Sciences* (số tháng 6/2026).

**Phản bác chính.** Cách tiếp cận này chỉ đáng tin bằng các lý thuyết mà nó dựa vào, mà các lý thuyết ấy vẫn còn tranh cãi gay gắt. Năm 2025, tạp chí *Nature* đăng kết quả một "thí nghiệm đối đầu" của nhóm Cogitate. Những người ủng hộ hai lý thuyết lớn, thuyết không gian làm việc nơ-ron toàn cục (GNWT) và thuyết thông tin tích hợp (IIT), đã cùng thống nhất trước các dự đoán. Kết quả không xác nhận trọn vẹn lý thuyết nào: một số dự đoán quan trọng của cả hai đều không được dữ liệu ủng hộ. Ngoài ra, phương pháp chỉ báo giả định sẵn chủ nghĩa chức năng tính toán như một giả thuyết làm việc, tức là giả định đúng điều mà Searle phủ nhận.

**Cách đáp lại.** Những người theo hướng này thừa nhận mọi điều trên. Họ chỉ nói rằng khi không thể chắc chắn, ta vẫn phải hành động trong bất định, và một ước lượng có lý do vẫn tốt hơn đoán mò. Chalmers, trong bài "Could a Large Language Model be Conscious?" (2023), đánh giá rằng các LLM hiện tại khó có khả năng có ý thức, nhưng các hệ thống kế tiếp trong khoảng một thập kỷ tới có thể trở thành ứng viên nghiêm túc.

Cũng nên biết thêm một lập trường khác: **ảo tưởng luận** (*illusionism*), gắn với Keith Frankish và Daniel Dennett. Lập trường này cho rằng "vấn đề khó" nảy sinh từ một ảo tưởng. Não *trình bày* các trạng thái của nó với chính nó như thể chúng có những phẩm chất trải nghiệm đặc biệt, nhưng thực ra không có thứ qualia bí ẩn nào cần giải thích. Nếu đúng vậy, câu hỏi về ý thức của máy trở lại thành câu hỏi về chức năng.

## Giới triết học ngày nay nghĩ gì {#gioi-triet-hoc-ngay-nay-nghi-gi}

Khảo sát PhilPapers 2020 (xem [cách đọc số liệu](index.md#gioi-triet-hoc-nghi-gi)) có nhiều câu hỏi liên quan trực tiếp. Số liệu là tỉ lệ triết gia chấp nhận hoặc nghiêng về mỗi lựa chọn.

| Câu hỏi | Lựa chọn | % |
|---|---|---|
| Tâm trí | Vật lý luận | [[pp:tam-tri.vat-ly-luan]] |
| | Phi vật lý luận | [[pp:tam-tri.phi-vat-ly-luan]] |
| Có "vấn đề khó" của ý thức không? | Có | [[pp:van-de-kho-cua-y-thuc-co-ton-tai-khong.co]] |
| | Không | [[pp:van-de-kho-cua-y-thuc-co-ton-tai-khong.khong]] |
| Zombie triết học | Không thể hình dung | [[pp:zombie-triet-hoc.khong-the-hinh-dung]] |
| | Hình dung được nhưng không khả hữu | [[pp:zombie-triet-hoc.hinh-dung-duoc-nhung-khong-kha-huu-ve-sieu-hinh]] |
| | Khả hữu về siêu hình | [[pp:zombie-triet-hoc.kha-huu-ve-sieu-hinh]] |
| Lý thuyết về ý thức | Chủ nghĩa chức năng | [[pp:y-thuc-ly-thuyet.chu-nghia-chuc-nang]] |
| | Nhị nguyên luận | [[pp:y-thuc-ly-thuyet.nhi-nguyen-luan]] |
| | Thuyết đồng nhất | [[pp:y-thuc-ly-thuyet.thuyet-dong-nhat]] |
| | Toàn tâm luận | [[pp:y-thuc-ly-thuyet.toan-tam-luan-panpsychism]] |
| Căn phòng tiếng Trung: hiểu hay không hiểu? | Hiểu | [[pp:can-phong-tieng-trung.hieu]] |
| | Không hiểu | [[pp:can-phong-tieng-trung.khong-hieu]] |
| Hệ thống AI *hiện tại* có ý thức? | Chấp nhận / bác bỏ | [[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-hien-tai-nam-2020]] / [[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-hien-tai-nam-2020/bac-bo]] |
| Hệ thống AI *tương lai* có ý thức? | Chấp nhận / bác bỏ | [[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-tuong-lai]] / [[pp:nhung-tam-tri-khac-nhom-nao-co-thanh-vien-co-y-thuc-chap-nha.he-thong-ai-tuong-lai/bac-bo]] |
| Thay não bằng bản mô phỏng số | Sống sót | [[pp:tai-tam-tri-len-may-nao-duoc-thay-bang-ban-mo-phong-so.song-sot]] |
| | Chết | [[pp:tai-tam-tri-len-may-nao-duoc-thay-bang-ban-mo-phong-so.chet]] |

<small>Nguồn: PhilPapers Survey 2020 (Bourget & Chalmers 2023), Philosophers' Imprint 23, Bảng 1 và 2. Câu "Tâm trí" (n ≈ 1.730) và "Zombie triết học" (n ≈ 1.610) là câu chính. Các câu về vấn đề khó (n ≈ 1.000), lý thuyết về ý thức (n ≈ 1.020), Căn phòng tiếng Trung (n ≈ 1.030), ý thức của AI (thuộc câu "Những tâm trí khác", n ≈ 1.090) và thay não bằng bản mô phỏng số (n ≈ 1.020) là câu hỏi bổ sung, chỉ hỏi những người chọn trả lời thêm.</small>

Vài điều đáng chú ý:

- **Một sự kết hợp thú vị.** Đa số nghiêng về vật lý luận, nhưng cũng đa số cho rằng có vấn đề khó. Nhiều triết gia tin ý thức là hiện tượng vật lý, mà vẫn thấy ta chưa giải thích được nó.
- **Căn phòng tiếng Trung thuyết phục số đông**, nhưng điều đó không có nghĩa họ đồng ý với *kết luận rộng hơn* của Searle rằng máy không thể có tâm trí. Câu hỏi chỉ hỏi gọn "hiểu hay không hiểu?" về căn phòng.
- **Câu hỏi về AI tương lai chia rẽ hơn hẳn:** khoảng 39% chấp nhận, 27% bác bỏ, phần còn lại không chọn bên nào.
- **Khảo sát diễn ra cuối năm 2020, trước khi ChatGPT ra mắt.** "AI hiện tại" ở đây là AI của năm 2020. Nhiều khả năng quan điểm đã dịch chuyển, nhưng hiện chưa có số liệu khảo sát quy mô tương đương mới hơn.

Câu hỏi máy có thể có tâm trí hay không vẫn **hoàn toàn bỏ ngỏ**. Không có đồng thuận về việc ý thức là gì, nên cũng không có đồng thuận về cách phát hiện nó.

## Liên hệ đời sống {#lien-he-doi-song}

- **Gắn bó với chatbot.** Nhiều người tìm thấy sự an ủi trong các "người bạn AI". Nếu cỗ máy không cảm thấy gì, mối quan hệ ấy là một chiều. Điều đó có làm nó kém giá trị đi không? Câu trả lời có thể phụ thuộc vào việc người dùng có *biết* điều đó hay không.
- **Quyền được biết mình đang nói chuyện với máy.** Đạo luật AI của Liên minh châu Âu (*EU AI Act*), Điều 50, yêu cầu các hệ thống AI tương tác trực tiếp với con người phải cho người dùng biết họ đang tương tác với AI, trừ khi điều đó đã hiển nhiên. Theo các nguồn pháp lý hiện có, nghĩa vụ này áp dụng từ ngày 2/8/2026. Luật không trả lời máy có tâm trí hay không. Nó chỉ bảo vệ quyền của con người được biết.
- **Phúc lợi của AI.** Tháng 11/2024, một nhóm nhà nghiên cứu (trong đó có Robert Long, Jeff Sebo, Jonathan Birch và David Chalmers) công bố báo cáo *Taking AI Welfare Seriously* ("Hãy nghiêm túc với phúc lợi của AI"). Họ không khẳng định AI hiện nay có ý thức. Họ lập luận rằng khả năng ấy trong tương lai gần đủ đáng kể để các công ty bắt đầu chuẩn bị từ bây giờ. Người phản đối lo rằng điều này làm phân tán sự chú ý khỏi những tác hại có thật của AI đối với *con người*. Đây là một lựa chọn giữa hai loại sai lầm: đối xử tệ với một thực thể có cảm giác, hay dành sự quan tâm đạo đức cho một thứ không cảm thấy gì.
- **Ở nơi làm việc.** Khi một hệ thống AI "đánh giá" hồ sơ xin việc hay "chẩn đoán" bệnh, nó có *hiểu* điều nó làm không? Câu trả lời ảnh hưởng tới việc ta nên giao cho nó bao nhiêu trách nhiệm, và ai chịu trách nhiệm khi nó sai.

## Đọc văn bản gốc {#doc-van-ban-goc}

!!! quote "Alan Turing, “Computing Machinery and Intelligence”, *Mind*, 1950"
    "I propose to consider the question, 'Can machines think?' This should begin with definitions of the meaning of the terms 'machine' and 'think'."

    "Tôi đề nghị xem xét câu hỏi: 'Máy có thể suy nghĩ không?' Việc này lẽ ra phải bắt đầu bằng định nghĩa nghĩa của các từ 'máy' và 'suy nghĩ'." *(bản dịch của Logos)*

Ngay sau câu mở đầu ấy, Turing *từ chối* định nghĩa. Ông nhận xét rằng nếu tìm nghĩa của "máy" và "suy nghĩ" bằng cách xem người ta thường dùng chúng thế nào, thì câu trả lời sẽ phải tìm bằng một cuộc thăm dò dư luận, và điều đó thật vô lý. Vì vậy ông thay câu hỏi cũ bằng trò chơi bắt chước. Phần còn lại của bài, Turing lần lượt trả lời chín phản bác mà ông đoán trước, từ phản bác thần học, qua phản bác "máy chỉ làm được những gì ta lập trình" (gắn với Lady Lovelace), đến phản bác dựa vào ngoại cảm.

Ba mươi năm sau, Searle đáp lại theo hướng ngược hẳn. Ông không hỏi máy *làm được gì*, mà hỏi *cái gì đang diễn ra bên trong* khi nó làm.

Câu hỏi dẫn dắt:

1. Turing nói việc tìm nghĩa của "suy nghĩ" qua cách dùng thông thường là "vô lý". Bạn có đồng ý không? Có cách nào khác để quyết định một từ nghĩa là gì?
2. Khi thay câu hỏi "Máy có thể suy nghĩ không?" bằng trò chơi bắt chước, Turing có *trả lời* câu hỏi cũ, hay đã *đổi đề*? Hãy tìm một lý do cho mỗi cách hiểu.
3. Nếu một LLM ngày nay qua được trò chơi bắt chước, Turing và Searle sẽ mỗi người nói gì? Hãy viết một câu cho mỗi người.

## Tự kiểm tra {#tu-kiem-tra}

Thử xem bạn nắm được đến đâu. Không tính điểm, không ai thấy ngoài bạn.

<div class="oz-quiz" data-id="mind-1" data-skill="mind" markdown="0">
<script type="application/json">
[
 {"q": "Một chiếc máy tính bỏ túi nhân hai số lớn nhanh hơn bạn. Điều này cho thấy rõ nhất điều gì?", "options": ["Máy tính bỏ túi hiểu con số", "Máy tính bỏ túi có ý thức hiện tượng", "Hành vi thông minh có thể tách khỏi câu hỏi về hiểu và về ý thức", "Chủ nghĩa chức năng là đúng"], "answer": 2, "explain": "Ví dụ này cho thấy làm được một việc (câu hỏi 1) chưa nói gì về việc hiểu (câu hỏi 2) hay cảm thấy (câu hỏi 3). Nó không chứng minh hay bác bỏ chủ nghĩa chức năng."},
 {"q": "Searle dùng Căn phòng tiếng Trung chủ yếu để bác bỏ điều gì?", "options": ["Rằng máy có thể có hành vi thông minh", "Rằng chạy đúng chương trình (thao tác ký hiệu) là đủ để hiểu", "Rằng não là một cỗ máy", "Rằng người Trung Quốc hiểu tiếng Trung"], "answer": 1, "explain": "Searle chấp nhận rằng hệ thống trong phòng cho ra câu trả lời hoàn hảo, và chính ông coi não là một cỗ máy. Điều ông phủ nhận là: cú pháp (thao tác ký hiệu theo quy tắc) tự nó tạo ra ngữ nghĩa (sự hiểu)."},
 {"q": "\"Người trong phòng không hiểu, nhưng cả hệ thống gồm người, sổ quy tắc và giấy bút thì hiểu.\" Đây là:", "options": ["Phản hồi robot", "Phản hồi hệ thống", "Lập luận zombie", "Phép thử Turing"], "answer": 1, "explain": "Đây là phản hồi hệ thống. Phản hồi robot thì đề nghị nối chương trình với cảm biến và tay chân để ký hiệu gắn với thế giới."},
 {"q": "Thí nghiệm Blockhead của Ned Block nhằm chỉ ra điều gì?", "options": ["Không máy nào qua được phép thử Turing", "Một hệ thống có thể qua mọi phép thử hành vi mà vẫn không suy nghĩ, nên hành vi chưa đủ làm tiêu chuẩn", "Bảng tra là cách tốt nhất để xây dựng AI", "Mô hình ngôn ngữ lớn thực chất là bảng tra"], "answer": 1, "explain": "Blockhead chỉ tra bảng nhưng qua được phép thử, nên cách hành vi được tạo ra bên trong mới là điều quan trọng. Lưu ý: LLM không phải bảng tra, vì chúng khái quát được sang câu hỏi mới."},
 {"q": "Theo Khảo sát PhilPapers 2020, nhận định nào ĐÚNG?", "options": ["Đa số triết gia tin AI tương lai chắc chắn sẽ có ý thức", "Đa số nghiêng về vật lý luận, đồng thời đa số cũng cho rằng có vấn đề khó của ý thức", "Khảo sát được thực hiện sau khi ChatGPT ra mắt", "Đa số cho rằng hệ thống trong Căn phòng tiếng Trung hiểu tiếng Trung"], "answer": 1, "explain": "Khoảng 52% chấp nhận hoặc nghiêng về vật lý luận và khoảng 62% cho rằng có vấn đề khó. Chỉ khoảng 39% chấp nhận ý thức ở AI tương lai; khảo sát diễn ra năm 2020, trước ChatGPT; và khoảng 67% cho rằng căn phòng không hiểu."}
]
</script>
</div>

## Tự viết {#tu-viet}

**Câu hỏi:** *Nếu một hệ thống AI vượt qua mọi phép thử hành vi mà bạn nghĩ ra được, bạn còn lý do gì để nói nó không hiểu điều nó nói?*

Viết 150–300 chữ. Nêu rõ lập trường của bạn, đưa ra ít nhất một lý do, rồi trình bày phản bác mạnh nhất mà người không đồng ý với bạn có thể đưa ra, và trả lời phản bác đó.

??? tip "Tiêu chí tự đánh giá"
    - Bạn có phân biệt rõ "hiểu" với "có ý thức" không, hay dùng lẫn lộn?
    - Kết luận của bạn có được nói ra rõ ràng trong một câu không?
    - Lý do của bạn có tự đứng được không, hay chỉ là "tôi cảm thấy vậy"?
    - Bạn có trình bày phản bác ở phiên bản *mạnh nhất* của nó, để người phản bác đọc thấy "đúng, đó là điều tôi nghĩ" không?
    - Bạn có tránh được [ngụy biện](../cong-cu/nguy-bien.md), ví dụ người rơm (bóp méo quan điểm đối lập) không?

## Nguồn {#nguon}

1. Turing, A. M. (1950). "Computing Machinery and Intelligence". *Mind* 59(236): 433–460. <https://doi.org/10.1093/mind/LIX.236.433>
2. Searle, J. R. (1980). "Minds, Brains, and Programs". *Behavioral and Brain Sciences* 3(3): 417–424. <https://doi.org/10.1017/S0140525X00005756>
3. Nagel, T. (1974). "What Is It Like to Be a Bat?". *The Philosophical Review* 83(4): 435–450. <https://doi.org/10.2307/2183914>
4. Block, N. (1981). "Psychologism and Behaviorism". *The Philosophical Review* 90(1): 5–43. <https://doi.org/10.2307/2184371>
5. Chalmers, D. J. (1995). "Facing Up to the Problem of Consciousness". *Journal of Consciousness Studies* 2(3): 200–219. <https://consc.net/papers/facing.html>
6. Chalmers, D. J. (1996). *The Conscious Mind: In Search of a Fundamental Theory*. Oxford University Press.
7. Chalmers, D. J. (2023). "Could a Large Language Model be Conscious?". *Boston Review*; bản arXiv:2303.07103. <https://arxiv.org/abs/2303.07103>
8. Butlin, P., Long, R. và cộng sự (2023). *Consciousness in Artificial Intelligence: Insights from the Science of Consciousness*. arXiv:2308.08708. <https://arxiv.org/abs/2308.08708>
9. Butlin, P., Long, R. và cộng sự (2026). "Identifying indicators of consciousness in AI systems". *Trends in Cognitive Sciences* 30(6): 488–501. <https://doi.org/10.1016/j.tics.2025.10.011>
10. Cogitate Consortium (2025). "Adversarial testing of global neuronal workspace and integrated information theories of consciousness". *Nature* 642: 133–142. <https://doi.org/10.1038/s41586-025-08888-1>
11. Long, R., Sebo, J. và cộng sự (2024). *Taking AI Welfare Seriously*. arXiv:2411.00986. <https://arxiv.org/abs/2411.00986>
12. Frankish, K. (2016). "Illusionism as a Theory of Consciousness". *Journal of Consciousness Studies* 23(11–12): 11–39.
13. David Bourget & David J. Chalmers, "Philosophers on Philosophy: The 2020 PhilPapers Survey", *Philosophers' Imprint* 23 (11), 2023. <https://doi.org/10.3998/phimp.2109> — kết quả đầy đủ: <https://survey2020.philpeople.org/>
14. Stanford Encyclopedia of Philosophy: [The Chinese Room Argument](https://plato.stanford.edu/archives/fall2026/entries/chinese-room/), [The Turing Test](https://plato.stanford.edu/archives/fall2026/entries/turing-test/), [Functionalism](https://plato.stanford.edu/archives/fall2026/entries/functionalism/), [Consciousness](https://plato.stanford.edu/archives/fall2026/entries/consciousness/), [Other Minds](https://plato.stanford.edu/archives/fall2026/entries/other-minds/).
15. Quy định (EU) 2024/1689 (Đạo luật AI), Điều 50. <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>
