/* Logos Zero — công cụ "Luận cứ thép" (steelman).
 * Dẫn người dùng qua 4 bước dựng phiên bản mạnh nhất của lập trường đối lập,
 * rồi tổng hợp thành một bản "luận cứ thép" hoàn chỉnh.
 * KHÔNG chấm điểm, KHÔNG ghi nhận tiến độ — như thí nghiệm tư duy.
 * Cách dùng: <div class="oz-steelman"></div> */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.steelman = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* ================= Hàm thuần ================= */

  // Độ dài tối thiểu (ký tự, sau khi trim) cho từng bước. Ngắn hơn thì
  // chưa đủ chi tiết để gọi là "phiên bản mạnh nhất".
  var MIN_LEN = { 1: 30, 2: 15, 3: 20, 4: 20 };

  function nonEmpty(s) {
    return typeof s === "string" && s.trim().length > 0;
  }

  function longEnough(s, min) {
    return typeof s === "string" && s.trim().length >= min;
  }

  /* Kiểm tra một bước. d = { presetId, chuDeRieng, b1, b2a, b2b, b2c, b3, b4 }.
     Trả về null nếu đạt, chuỗi lỗi tiếng Việt nếu chưa. */
  function validateStep(step, d) {
    d = d || {};
    if (step === 0) {
      if (!d.presetId && !nonEmpty(d.chuDeRieng))
        return "Hãy chọn một chủ đề có sẵn, hoặc tự nhập chủ đề bạn đang tranh luận.";
      return null;
    }
    if (step === 1) {
      if (!longEnough(d.b1, MIN_LEN[1]))
        return "Bản phát biểu lại còn quá ngắn. Một “luận cứ thép” phải chi tiết đến mức chính phe đối lập đọc cũng phải gật đầu.";
      return null;
    }
    if (step === 2) {
      var thieu = ["b2a", "b2b", "b2c"].some(function (k) {
        return !longEnough(d[k], MIN_LEN[2]);
      });
      if (thieu)
        return (
          "Cần cả 3 luận cứ, mỗi luận cứ ít nhất " +
          MIN_LEN[2] +
          " ký tự — đừng để phe đối lập chỉ có một lý do duy nhất."
        );
      return null;
    }
    if (step === 3) {
      if (!longEnough(d.b3, MIN_LEN[3]))
        return "Hãy ghi cụ thể bằng chứng phe họ viện dẫn — càng cụ thể, bản “luận cứ thép” càng khó bị xem là người rơm.";
      return null;
    }
    if (step === 4) {
      if (!longEnough(d.b4, MIN_LEN[4]))
        return "Hãy viết rõ điều kiện làm bạn đổi ý. Nếu không có điều gì làm bạn đổi ý được, hãy ghi thẳng ra — khi đó bạn đang giữ một niềm tin, không phải một kết luận mở.";
      return null;
    }
    return "Bước không hợp lệ.";
  }

  /* ================= Dữ liệu thuần: chủ đề có sẵn =================
   * Mỗi preset: id, ten, bai (đường dẫn tính từ docs/), tinh_huong,
   * doi_lap (2–3 gợi ý phe đối lập mẫu), mau (ví dụ đã làm mẫu cho 4 bước;
   * mau[2] là bộ 3 luận cứ). Nội dung ví dụ bám theo các bài viết đã có. */
  var PRESETS = [
    {
      id: "pha-thai",
      ten: "Phá thai",
      bai: "cau-hoi/pha-thai.md",
      tinh_huong:
        "Bạn cho rằng phá thai nên được cho phép trong đa số trường hợp. Hãy dựng luận cứ thép cho phe phản đối.",
      doi_lap: [
        "Phe bảo vệ quyền sống: thai nhi là một con người từ thụ thai; phá thai về nguyên tắc không khác gì tước mạng sống của người vô tội.",
        "Phe bảo vệ quyền tự chủ (Thomson 1971): ngay cả khi thai nhi là người, người mẹ vẫn có quyền rút lại sự cho mượn thân thể — quyền sống không bao gồm quyền được nuôi bằng thân thể người khác.",
      ],
      mau: {
        1: "Phe phản đối, ở dạng mạnh nhất, không nói “thai nhi trông giống em bé”. Họ nói về ranh giới: mọi mốc ta vẽ — chào đời, khả năng sống độc lập, có ý thức — đều tùy tiện (trẻ sinh non tuần 24 sống được nhờ lồng ấp, nên “sống độc lập” phụ thuộc công nghệ; trẻ sơ sinh cũng chưa có ý thức đầy đủ). Chỉ có thụ thai là mốc sinh học không tùy tiện: từ đó một sinh thể người với đầy đủ mã di truyền tồn tại và phát triển liên tục. Và như Marquis (1989) lập luận: điều làm việc giết người trưởng thành là sai — tước đi một “tương lai đang chờ đợi” — cũng đúng với thai nhi.",
        2: [
          "Luận cứ từ nguyên tắc (ranh giới không tùy tiện): địa vị đạo đức phải dựa vào một mốc không do ta chọn bừa; chỉ có thụ thai đáp ứng được điều đó.",
          "Luận cứ từ hệ quả (tương lai bị tước): giết người sai vì tước tương lai của nạn nhân; phá thai tước đúng thứ tương lai đó của thai nhi.",
          "Luận cứ từ thực nghiệm (phát triển liên tục): y văn ghi nhận sự phát triển liên tục, không đứt đoạn, từ phôi đến trẻ sơ sinh; không có “khoảnh khắc hóa người” nào khác ngoài thụ thai.",
        ],
        3: "Bằng chứng họ viện dẫn: các mốc phát triển của phôi thai được ghi nhận trong y văn (tim thai, hoạt động não sớm); và thực tế pháp luật nhiều nước cho phép phá thai sớm dễ dàng hơn phá thai muộn — cho thấy trực giác “thai nhi càng phát triển càng có địa vị đạo đức cao hơn” là trực giác chung, không phải ý kiến riêng của phe nào.",
        4: "Tôi sẽ đổi ý nếu có một tiêu chí địa vị đạo đức vừa không tùy tiện, vừa không kéo theo hệ quả phi lý (chẳng hạn coi việc hủy phôi dư trong thụ tinh ống nghiệm là giết người hàng loạt) — hoặc nếu ai đó chỉ ra được vì sao “tương lai đang chờ đợi” áp dụng cho người trưởng thành mà lại không áp dụng cho thai nhi.",
      },
    },
    {
      id: "an-tu-hinh",
      ten: "Án tử hình",
      bai: "cau-hoi/an-tu-hinh.md",
      tinh_huong:
        "Bạn phản đối án tử hình. Hãy dựng luận cứ thép cho phe ủng hộ.",
      doi_lap: [
        "Phe ủng hộ: có những tội ác mà chỉ cái chết mới tương xứng; án tử hình còn có tác dụng răn đe kẻ khác.",
        "Phe phản đối: không hệ thống tư pháp nào đủ hoàn hảo — oan sai với án tử là không thể sửa chữa.",
      ],
      mau: {
        1: "Phe ủng hộ, ở dạng mạnh nhất, không nói “giết kẻ giết người cho hả giận”. Họ nói về công bằng: có những hành động mà không trừng phạt tương xứng thì chính là bất công — khi kẻ giết người hàng loạt chỉ ngồi tù vài chục năm trong khi nạn nhân mất tất cả, cán cân công lý chưa được lập lại. Họ cũng đảo gánh nặng chứng minh: nếu án tử hình cứu được dù chỉ một mạng người vô tội nhờ răn đe, thì bãi bỏ nó cũng là một lựa chọn có cái giá bằng sinh mạng — phe bãi bỏ không thể giả vờ rằng lựa chọn của họ không giết ai.",
        2: [
          "Luận cứ từ nguyên tắc (báo ứng tương xứng): công lý đòi hỏi hình phạt tương xứng với tội ác; với tội ác tước đi sinh mạng, chỉ cái chết mới tương xứng.",
          "Luận cứ từ hệ quả (răn đe): nếu án tử hình ngăn được kẻ khác giết người, bãi bỏ nó đồng nghĩa với hy sinh những nạn nhân tương lai.",
          "Luận cứ từ thực nghiệm (trực giác công bằng): trực giác “kẻ giết người hàng loạt xứng đáng chết” là dữ kiện đạo đức ổn định qua nhiều nền văn hóa, không phải ảo giác nhất thời.",
        ],
        3: "Bằng chứng họ viện dẫn: các nghiên cứu về hiệu quả răn đe — mà chính bài viết ghi nhận là còn tranh cãi, cho kết quả trái ngược nhau; và trực giác công bằng phổ biến: mỗi khi xảy ra một vụ án đặc biệt dã man, làn sóng dư luận đòi án tử hình cho thấy trực giác báo ứng không phải của riêng ai.",
        4: "Tôi sẽ đổi ý nếu có bằng chứng thuyết phục rằng án tử hình hoàn toàn không có tác dụng răn đe hơn tù chung thân trong mọi bối cảnh — hoặc nếu ai đó chỉ ra được một cách trừng phạt tội ác đặc biệt nghiêm trọng mà vẫn “tương xứng” nhưng không cần đến cái chết.",
      },
    },
    {
      id: "tu-do-y-chi",
      ten: "Tự do ý chí",
      bai: "cau-hoi/tu-do-y-chi.md",
      tinh_huong:
        "Bạn tin con người có tự do ý chí. Hãy dựng luận cứ thép cho phe tất định luận.",
      doi_lap: [
        "Phe bất tương thích (tất định luận cứng): mọi hành động đều có nguyên nhân đầy đủ từ trước khi ta sinh ra; “lựa chọn khác đi” chỉ là ảo tưởng.",
        "Phe tương thích luận: tự do là hành động theo ý muốn của chính mình — không cần phải thoát khỏi chuỗi nhân quả.",
      ],
      mau: {
        1: "Phe tất định, ở dạng mạnh nhất, không nói “con người như robot”. Họ đưa lập luận hệ quả của van Inwagen: nếu tất định luận đúng, mọi hành động của ta là hệ quả của các quy luật tự nhiên và những sự kiện quá khứ xa xôi; những gì xảy ra trước khi ta sinh ra không phụ thuộc vào ta; các quy luật tự nhiên cũng không phụ thuộc vào ta; vậy hành động hiện tại của ta cũng không phụ thuộc vào ta. Cảm giác “tôi có thể đã chọn khác” chỉ là cảm giác — như cảm giác mặt trời quay quanh trái đất.",
        2: [
          "Luận cứ từ nguyên tắc (lập luận hệ quả): không ai kiểm soát được quá khứ xa xôi và quy luật tự nhiên, nên không ai kiểm soát được hệ quả logic của chúng — bao gồm hành động của chính mình.",
          "Luận cứ từ thực nghiệm (thí nghiệm Libet): hoạt động não chuẩn bị cho hành động bắt đầu trước khi ý định có ý thức xuất hiện — cảm giác “tôi quyết định” có thể chỉ là một bản tường thuật muộn.",
          "Luận cứ từ hệ quả (trách nhiệm): nếu không ai thực sự “làm khác đi” được, thì khen–trách–trừng phạt theo nghĩa “đáng bị” mất nền tảng; pháp luật nên hướng về phòng ngừa và phục hồi — như cách ta cách ly người bệnh truyền nhiễm, không phải vì họ đáng bị nhốt.",
        ],
        3: "Bằng chứng họ viện dẫn: các thí nghiệm thần kinh học về thời điểm ý định có ý thức (Libet và các nghiên cứu nối tiếp — bài viết đã trình bày kèm những tranh cãi về phương pháp đo); và quan sát thường ngày: càng hiểu rõ nguyên nhân của một hành động (gen, cách nuôi dạy, hoàn cảnh), ta càng ít thấy chỗ cho một “cái tôi” đứng ngoài chuỗi nhân quả.",
        4: "Tôi sẽ đổi ý nếu vật lý chứng minh được rằng ở cấp độ não bộ có những sự kiện thực sự không bị quyết định bởi bất cứ gì trước đó, VÀ những sự kiện đó lại nằm dưới sự kiểm soát của “tôi” — chứ không phải chỉ là ngẫu nhiên (ngẫu nhiên cũng không cho ta tự do, như chính phe hoài nghi đã chỉ ra).",
      },
    },
    {
      id: "cai-chet",
      ten: "Cái chết có đáng sợ không?",
      bai: "cau-hoi/cai-chet.md",
      tinh_huong:
        "Bạn sợ chết và cho rằng nỗi sợ đó là hợp lý. Hãy dựng luận cứ thép cho phe “chết không đáng sợ”.",
      doi_lap: [
        "Phe Epicurus: “đã chết” không phải một trải nghiệm — khi ta còn thì nó chưa tới, khi nó tới thì ta không còn; sợ nó cũng như sợ “không có gì”.",
        "Phe Nagel: chết đáng sợ vì nó tước đi những điều tốt đẹp ta còn có thể trải qua trong đời.",
      ],
      mau: {
        1: "Phe Epicurus, ở dạng mạnh nhất, không nói “đừng nghĩ đến cái chết”. Họ hỏi: sợ hãi thường là sợ trải nghiệm điều gì đó (sợ đau, sợ nhục) — nhưng “đã chết” không phải một trải nghiệm, không có ai ở đó để mà sợ. Và họ đưa lập luận đối xứng: nếu bạn không thấy khoảng thời gian trước khi mình sinh ra có gì đáng sợ, bạn nợ một lời giải thích vì sao khoảng thời gian sau khi chết lại khác — hai khoảng “không tồn tại” ấy đối xứng nhau.",
        2: [
          "Luận cứ từ nguyên tắc (bản chất của sợ hãi): sợ hãi hợp lý phải gắn với một điều xấu có chủ thể trải nghiệm; cái chết không còn chủ thể nào để mà xấu.",
          "Luận cứ từ đối xứng (trước sinh / sau tử): không ai tiếc vì cha mẹ không sinh mình sớm hơn; nhất quán thì cũng không nên sợ khoảng không-tồn-tại sau khi chết.",
          "Luận cứ từ hệ quả (sống tốt hơn): người chấp nhận cái chết không đáng sợ sẽ bớt ám ảnh, sống trọn vẹn hơn — nỗi sợ chết, chứ không phải cái chết, mới là thứ làm hại đời sống.",
        ],
        3: "Bằng chứng họ viện dẫn: quan sát rằng nỗi sợ chết thường gắn với những điều cụ thể và giải quyết được (sợ đau lúc hấp hối — y học giảm đau giải quyết; sợ bỏ lại người thân — đó là nỗi buồn cho người ở lại, không phải cho “trạng thái đã chết”); và hiện tượng nhiều người sau khi đối mặt với bệnh hiểm nghèo lại sống thanh thản hơn — như thể nỗi sợ đã được “gọi tên” thì nhỏ lại.",
        4: "Tôi sẽ đổi ý nếu ai đó chỉ ra được một điều xấu của cái chết mà không cần đến một chủ thể trải nghiệm nó — tức là trả lời được câu hỏi của chính Epicurus: “bị tước đi” của ai, khi không còn ai cả — hoặc nếu có bằng chứng rằng nỗi sợ chết là cơ chế sinh tồn không thể “lý luận” cho tắt, và việc cố tắt nó gây hại nhiều hơn lợi.",
      },
    },
    {
      id: "cong-nghe-ai",
      ten: "AI và công nghệ",
      bai: "cau-hoi/cong-nghe-ai.md",
      tinh_huong:
        "Bạn lo ngại AI và thuật toán đang định hình lại con người. Hãy dựng luận cứ thép cho phe “công nghệ trung lập”.",
      doi_lap: [
        "Phe công nghệ trung lập: công cụ vô tội, lỗi ở người dùng — đổ lỗi cho thuật toán là trốn tránh trách nhiệm.",
        "Phe công nghệ định hình con người: ta không chỉ dùng công cụ; công cụ cũng đang “dùng” ta — viết lại cách ta nghĩ, nhớ, chọn lựa.",
      ],
      mau: {
        1: "Phe trung lập, ở dạng mạnh nhất, không nói “công nghệ chẳng ảnh hưởng gì”. Họ nói về trách nhiệm: đổ lỗi cho công nghệ là một cách trốn tránh — “tại thuật toán” thay vì “tại tôi đã thiết kế, bán, dùng nó như vậy”. Mỗi vụ bê bối công nghệ, câu hỏi đúng phải là: ai đã quyết định, ai hưởng lợi, ai chịu trách nhiệm — chứ không phải “công nghệ thật đáng sợ”. Và ví dụ cây cầu của Winner thực ra ủng hộ họ: vấn đề nằm ở Robert Moses — con người đã thiết kế cầu thấp để ngăn người nghèo ra biển — chứ không nằm ở “bản chất của cây cầu”.",
        2: [
          "Luận cứ từ nguyên tắc (trách nhiệm): chỉ con người mới là chủ thể đạo đức; gán lỗi cho công cụ làm mờ đi những con người cụ thể phải chịu trách nhiệm.",
          "Luận cứ từ thực nghiệm (lịch sử): cùng một công nghệ phục vụ mục đích trái ngược (internet vừa lan tỏa tri thức vừa lan tỏa tin giả) — nên “bản chất tốt/xấu” không nằm trong công nghệ.",
          "Luận cứ từ hệ quả (con người vẫn có lựa chọn): nhiều công nghệ từng bị từ chối, điều chỉnh, bị cấm (vũ khí hóa học, nhân bản người); EU áp GDPR lên các gã khổng lồ công nghệ — nếu công nghệ thực sự “tự trị”, những điều đó không thể xảy ra.",
        ],
        3: "Bằng chứng họ viện dẫn: lịch sử các công nghệ bị xã hội từ chối hoặc siết chặt (vũ khí hóa học, nhân bản người); các khung pháp lý như GDPR cho thấy con người vẫn đặt được ranh giới; và thực tế cùng một nền tảng có thể dùng để học tập lẫn để lan truyền tin giả — khác biệt nằm ở người dùng và thể chế, không ở “bản chất” nền tảng.",
        4: "Tôi sẽ đổi ý nếu có bằng chứng rằng một hệ thống AI cụ thể đã tự mình đặt ra mục tiêu trái với ý định của mọi con người liên quan mà không ai có thể can thiệp — tức là công nghệ không còn là “công cụ mang dấu ấn người thiết kế” mà đã thành một tác nhân độc lập thực sự.",
      },
    },
    {
      id: "khi-hau",
      ten: "Biến đổi khí hậu: ai chịu trách nhiệm?",
      bai: "cau-hoi/khi-hau-trach-nhiem.md",
      tinh_huong:
        "Bạn cho rằng trách nhiệm chính thuộc về cá nhân — mỗi người gánh phần của mình. Hãy dựng luận cứ thép cho phe trách nhiệm cấu trúc.",
      doi_lap: [
        "Phe trách nhiệm cá nhân: “mọi người đều có lỗi” trong thực tế thành “không ai có lỗi”; đại dương chính là tổng của các giọt nước.",
        "Phe trách nhiệm cấu trúc: đường cong phát thải chỉ uốn xuống khi hệ thống thay đổi — một nhà máy điện than đóng cửa bằng hàng triệu cá nhân tắt đèn.",
      ],
      mau: {
        1: "Phe cấu trúc, ở dạng mạnh nhất, không nói “cá nhân vô can”. Họ nói về tính thực tế nhân quả: một nhà máy điện than đóng cửa giảm phát thải bằng hàng triệu cá nhân tắt đèn cộng lại; tầng ozone được cứu không phải vì mỗi người tự nguyện bớt dùng bình xịt, mà vì Nghị định thư Montreal (1987) cấm CFC trên toàn cầu. Và họ chỉ ra sự đảo ngược đạo đức: dồn trách nhiệm lên vai người tiêu dùng — những người ít quyền lực nhất — trong khi tập đoàn và chính phủ đứng ngoài, là đổ lỗi sai địa chỉ; đáng ngờ hơn, chính chiến dịch của BP (một tập đoàn dầu khí) đã phổ biến khái niệm “dấu chân carbon” cá nhân vào đầu những năm 2000.",
        2: [
          "Luận cứ từ hệ quả (hiệu quả nhân quả): chỉ thay đổi cấp hệ thống mới uốn được đường cong phát thải toàn cầu; nỗ lực cá nhân đơn lẻ không cộng thành đủ.",
          "Luận cứ từ nguyên tắc (quyền lực đi với trách nhiệm): trách nhiệm phải tương xứng với khả năng gây ảnh hưởng — tập đoàn và chính phủ nắm đòn bẩy lớn nhất.",
          "Luận cứ từ thực nghiệm (tiền lệ lịch sử): những thắng lợi môi trường lớn (Montreal 1987) đều đến từ hành động tập thể có tính ràng buộc, không từ sự tự nguyện rời rạc.",
        ],
        3: "Bằng chứng họ viện dẫn: báo cáo Carbon Majors (2017) — chỉ 100 nhà sản xuất nhiên liệu hóa thạch gắn với 71% lượng phát thải công nghiệp toàn cầu kể từ năm 1988 (số liệu bài viết đã dẫn); tiền lệ Nghị định thư Montreal; và nguồn gốc của khái niệm “dấu chân carbon” từ chiến dịch quảng cáo của BP.",
        4: "Tôi sẽ đổi ý nếu có bằng chứng rằng tổng phát thải toàn cầu đã giảm đáng kể chỉ nhờ thay đổi hành vi tiêu dùng tự nguyện, trong khi chính sách và cơ cấu năng lượng không đổi — tức là nếu “các giọt nước” thực sự tự gom thành đại dương mà không cần ai đào kênh.",
      },
    },
    {
      id: "quyen-rieng-tu-so",
      ten: "Quyền riêng tư số",
      bai: "cau-hoi/quyen-rieng-tu-so.md",
      tinh_huong:
        "Bạn ủng hộ bảo vệ quyền riêng tư mạnh mẽ. Hãy dựng luận cứ thép cho phe “không có gì để giấu” (ưu tiên an ninh).",
      doi_lap: [
        "Phe an ninh: mạng người hay cảm giác riêng tư — đặt thứ tự ưu tiên nào lên trước? Trong thời đại số, “riêng tư tuyệt đối” đã là ảo tưởng.",
        "Phe tự chủ: riêng tư không phải che giấu tội lỗi mà là kiểm soát thông tin về mình — nó là điều kiện của tự do.",
      ],
      mau: {
        1: "Phe an ninh, ở dạng mạnh nhất, không nói “ai cũng nên bị đọc tin nhắn”. Họ đặt câu hỏi về thứ tự ưu tiên: khi một vụ tấn công có thể được ngăn bằng cách quét dữ liệu viễn thông, khăng khăng bảo vệ “quyền không bị đọc tin nhắn” nghe như đặt sự tiện nghi lên trên sinh mạng. Và họ chỉ ra sự thiếu nhất quán: mọi người tự nguyện nộp dữ liệu cho mạng xã hội, app giao hàng, bản đồ mỗi ngày — rồi lại phản đối nhà nước thu thập dữ liệu với lý do “riêng tư”. Nếu dữ liệu đã được cho đi tự nguyện, vì sao dùng nó để bảo vệ chính những người đó lại là sai?",
        2: [
          "Luận cứ từ nguyên tắc (thứ tự ưu tiên): sinh mạng con người nặng hơn cảm giác khó chịu vì bị giám sát; trong tình huống khẩn cấp, mọi quyền đều có thể bị hạn chế tạm thời (phong tỏa, trưng thu).",
          "Luận cứ từ hệ quả (an ninh thực tế): giám sát giúp ngăn chặn tội phạm và khủng bố; từ chối công cụ này đồng nghĩa với chấp nhận những vụ việc lẽ ra ngăn được.",
          "Luận cứ từ thực nghiệm (nhất quán hành vi): người dân đã tự nguyện đánh đổi dữ liệu lấy tiện ích mỗi ngày — “riêng tư tuyệt đối” không phải là chuẩn mực họ thực sự sống theo.",
        ],
        3: "Bằng chứng họ viện dẫn: các vụ phá án nhờ dữ liệu viễn thông mà báo chí từng đưa tin; và nghịch lý hành vi — cùng một người phản đối “nhà nước đọc tin nhắn” lại bấm “đồng ý” chia sẻ vị trí 24/7 cho ứng dụng giao đồ ăn.",
        4: "Tôi sẽ đổi ý nếu có bằng chứng thuyết phục rằng giám sát đại trà thực sự ngăn được nhiều vụ việc hơn hẳn giám sát có mục tiêu (có lệnh của tòa án) — chứ không chỉ “trông có vẻ quyết liệt hơn” — và nếu cơ chế kiểm soát lạm dụng (lệnh tòa, giám sát độc lập, giới hạn thời gian lưu trữ) được chứng minh là vận hành hiệu quả trong thực tế, không chỉ trên giấy.",
      },
    },
    {
      id: "cuu-giup-ngheo-doi",
      ten: "Cứu giúp người nghèo đói",
      bai: "cau-hoi/cuu-giup-ngheo-doi.md",
      tinh_huong:
        "Bạn cho rằng cứu giúp người nghèo là nghĩa vụ, không phải tùy lòng. Hãy dựng luận cứ thép cho phe “từ thiện tùy lòng”.",
      doi_lap: [
        "Phe Singer: khoảng cách không phải lý do đạo đức; nếu cứu được với chi phí nhỏ thì phải cứu — như cứu đứa trẻ đuối nước ngay trước mặt.",
        "Phe từ thiện tùy lòng: cứu giúp đáng khen nhưng không bắt buộc — đạo đức còn gồm những cam kết đặc biệt với người thân; Kant phân biệt nghĩa vụ hoàn hảo với nghĩa vụ bất hoàn hảo.",
      ],
      mau: {
        1: "Phe “tùy lòng”, ở dạng mạnh nhất, không nói “kệ người nghèo”. Họ nói về cấu trúc của đời sống đạo đức: đạo đức không chỉ gồm nghĩa vụ vô tư với toàn nhân loại, mà còn gồm những cam kết đặc biệt — với con cái, cha mẹ, cộng đồng — mà chính những cam kết đó làm cho cuộc đời đáng sống. Một lý thuyết biến mọi đồng tiền dư thừa thành “nợ” của người nghèo đã xóa nhòa ranh giới giữa “cuộc đời của tôi” và “dự án cứu thế giới”. Như Kant đã phân biệt: có nghĩa vụ hoàn hảo (không được giết — bắt buộc với mọi người) và nghĩa vụ bất hoàn hảo (giúp đỡ người khác — bắt buộc về nguyên tắc, nhưng ta được chọn khi nào, giúp ai, bao nhiêu); cứu trợ thuộc loại thứ hai.",
        2: [
          "Luận cứ từ nguyên tắc (“phải” kéo theo “có thể”): nghĩa vụ không thể đòi hỏi điều vượt quá khả năng hợp lý của con người; một “nghĩa vụ” mà tuân thủ nó đồng nghĩa với từ bỏ cuộc đời mình là sự hy sinh anh hùng — đáng ngưỡng mộ, không thể bắt buộc.",
          "Luận cứ từ hệ quả (đòi hỏi quá mức): nguyên tắc của Singer, nếu áp dụng nghiêm túc, sẽ phá hủy đời sống cá nhân — không còn tiền cho con cái học hành, sở thích, dự án riêng; một lý thuyết như vậy có gì đó sai với chính nó.",
          "Luận cứ từ thực nghiệm (khả năng kiểm chứng): cứu đứa trẻ trước mặt, bạn thấy kết quả chắc chắn; gửi tiền đi xa, bạn không biết tiền có đến tay người cần không, có bị tham nhũng nuốt mất không — đạo đức không thể đòi hỏi hành động trong mù mờ.",
        ],
        3: "Bằng chứng họ viện dẫn: thực tế tuân thủ — gần như không ai, kể cả những người tán thành Singer trên lý thuyết, sống theo nguyên tắc triệt để của ông (cho đi đến mức giới hạn); và những điều chính bài viết nêu: tiền cứu trợ có thể bị tham nhũng nuốt mất, hoặc gây hệ quả phụ như làm méo mó kinh tế địa phương.",
        4: "Tôi sẽ đổi ý nếu có một tiêu chí có nguyên tắc — không phải “tôi cho đến khi tôi thấy đủ” — để xác định chính xác nghĩa vụ cứu giúp dừng ở đâu; hoặc nếu ai đó chứng minh được rằng khoảng cách địa lý thực sự không tạo ra khác biệt nào về trách nhiệm vai trò và khả năng kiểm chứng hiệu quả.",
      },
    },
    {
      id: "binh-dang",
      ten: "Bình đẳng và bất bình đẳng",
      bai: "cau-hoi/binh-dang.md",
      tinh_huong:
        "Bạn ủng hộ bình đẳng kết quả — chênh lệch lớn tự nó đã là xấu. Hãy dựng luận cứ thép cho phe bình đẳng cơ hội.",
      doi_lap: [
        "Phe bình đẳng kết quả: chênh lệch quá lớn ăn mòn cộng đồng — người giàu sống trong một thế giới khác, “chúng ta” tan rã thành “họ” và “ta”.",
        "Phe bình đẳng cơ hội: cùng luật chơi công bằng là đủ; người chăm chỉ xứng đáng hơn người lười biếng — san bằng kết quả là trừng phạt sự cố gắng.",
      ],
      mau: {
        1: "Phe cơ hội, ở dạng mạnh nhất, không nói “nghèo là do lười”. Họ nói về trách nhiệm cá nhân: con người là những tác nhân có lựa chọn, không phải những cái bình giống hệt nhau cần đổ đầy ngang nhau. Một xã hội mà người chăm chỉ và người lười biếng hưởng như nhau là xã hội trừng phạt sự cố gắng — và về lâu dài, giết chết chính động lực tạo ra của cải để mà chia. Bình đẳng cơ hội nói: ta chịu trách nhiệm với lựa chọn của mình; xã hội chỉ nợ ta một sân chơi công bằng.",
        2: [
          "Luận cứ từ nguyên tắc (trách nhiệm): công bằng là đối xử với con người như tác nhân có lựa chọn — thưởng cho cố gắng, không san bằng bất kể lựa chọn.",
          "Luận cứ từ hệ quả (động lực): san bằng kết quả triệt tiêu động lực làm việc và sáng tạo; chiếc bánh nhỏ lại thì phần của người nghèo cũng nhỏ theo.",
          "Luận cứ từ thực nghiệm (phản ví dụ “hạ bằng”): hai xã hội — A: mọi người đều có 10 đồng; B: một nửa có 10, một nửa có 100, không ai khổ hơn ở A — trực giác của hầu hết chúng ta nói B tốt hơn; nếu bình đẳng đòi chọn A, thì bình đẳng đang đòi làm mọi người tệ đi nhân danh một con số đẹp.",
        ],
        3: "Bằng chứng họ viện dẫn: chủ yếu là thí nghiệm tư duy “hạ bằng” — một công cụ kiểm tra trực giác mà phe bình đẳng kết quả phải trả lời thay vì né tránh — cùng lập luận về động lực: xã hội trừng phạt sự cố gắng sẽ dần cạn kiệt chính nguồn lực để mà chia.",
        4: "Tôi sẽ đổi ý nếu ai đó chứng minh được rằng “cơ hội” có thể được làm cho thực chất (không chỉ hình thức) mà không cần can thiệp sâu đến mức xóa nhòa ranh giới với bình đẳng kết quả — tức là giải được bài toán mà chính bài viết đã đặt ra: cơ hội hình thức thì rỗng, cơ hội thực chất thì sụp đổ vào san bằng.",
      },
    },
    {
      id: "dan-chu",
      ten: "Dân chủ",
      bai: "cau-hoi/dan-chu.md",
      tinh_huong:
        "Bạn nghiêng về phe phê phán dân chủ — đa số cũng có thể thành chuyên chế. Hãy dựng luận cứ thép cho phe bênh vực dân chủ.",
      doi_lap: [
        "Phe dân chủ thủ tục (Schumpeter, Popper): giá trị của dân chủ không phải ở “ai nên cai trị”, mà ở chỗ ta có thể loại bỏ chính quyền tồi mà không đổ máu.",
        "Phe phê phán: đa số có thể sai và có thể ác — nếu dân chủ chỉ là “đa số thắng”, không có gì ngăn đa số chà đạp thiểu số.",
      ],
      mau: {
        1: "Phe bênh vực, ở dạng mạnh nhất, không nói “đa số luôn đúng”. Họ nói như Popper: đừng hỏi “ai nên cai trị” — hãy hỏi “làm sao loại bỏ chính quyền tồi mà không đổ máu”. Dân chủ thủ tục không hứa cho ra quyết định đúng; nó chỉ hứa một cơ chế thay người cầm quyền trong hòa bình — và trong lịch sử nhân loại, đó đã là một thành tựu phi thường. Còn “chuyên chế của đa số” mà phe phê phán lo sợ, thực ra là lập luận cho một phiên bản dân chủ tốt hơn — dân chủ hiến định, tức dân chủ cộng với những quyền mà ngay cả đa số cũng không được xâm phạm — chứ không phải lập luận chống dân chủ.",
        2: [
          "Luận cứ từ nguyên tắc (khả thi và trung thực): định nghĩa mỏng về dân chủ kiểm tra được bằng bầu cử, không hứa hão “quyết định đúng” — và chính vì mỏng nên khó bị lợi dụng để dán nhãn “dân chủ thật”.",
          "Luận cứ từ hệ quả (loại bỏ hòa bình): cơ chế thay chính quyền không đổ máu là điều mà mọi thể chế khác trong lịch sử đều thiếu.",
          "Luận cứ từ thực nghiệm (câu hỏi ngược): nếu không tin số đông, thì tin ai? “Vua triết gia” của Platon trong thực tế trông như thế nào — và ai sẽ canh chừng ông ta?",
        ],
        3: "Bằng chứng họ viện dẫn: lịch sử các cuộc chuyển giao quyền lực hòa bình qua bầu cử, đặt cạnh các cuộc đảo chính và nội chiến ở những nơi thiếu cơ chế đó; và thực tế rằng mọi chế độ phi dân chủ tự xưng “vì dân” đều né tránh chính phép thử bầu cử cạnh tranh tự do.",
        4: "Tôi sẽ đổi ý nếu có một thể chế được chứng minh trong thực tế — không chỉ trên lý thuyết — vừa bảo vệ được thiểu số khỏi đa số, vừa chọn được người cai trị có năng lực, vừa có cơ chế loại bỏ kẻ tồi mà không cần đến bầu cử cạnh tranh; nói cách khác, nếu “vua triết gia” bước ra khỏi sách và cai trị tốt hơn, lâu dài hơn, mà không cần ai canh chừng.",
      },
    },
  ];

  /* Ví dụ chung (không gắn bài viết nào): dùng khi người dùng tự nhập chủ đề,
   * và để nút "Xem ví dụ mẫu" có thể xoay vòng. */
  var GENERIC = [
    {
      chuDe: "Có nên cấm xe máy ở nội thành?",
      mau: {
        1: "Phe ủng hộ cấm, ở dạng mạnh nhất: xe máy là nguồn tai nạn và ô nhiễm chính ở nội thành; mọi thành phố văn minh đều phải trải qua giai đoạn “đau” khi chuyển sang giao thông công cộng; và “quyền đi xe máy” không phải quyền cơ bản — nó chỉ là thói quen được nâng lên thành quyền.",
        2: [
          "Luận cứ từ hệ quả: cấm xe máy giảm tai nạn và ô nhiễm — hai cái giá mà toàn xã hội đang trả mỗi ngày.",
          "Luận cứ từ nguyên tắc: đường phố là không gian chung; không ai có quyền biến nó thành nơi nguy hiểm cho người khác.",
          "Luận cứ từ thực nghiệm: các thành phố đã hạn chế xe cá nhân (kèm đầu tư giao thông công cộng) đều ghi nhận chất lượng sống tăng lên.",
        ],
        3: "Bằng chứng họ viện dẫn: số liệu tai nạn giao thông liên quan đến xe máy do cơ quan chức năng công bố; các nghiên cứu về ô nhiễm không khí đô thị; kinh nghiệm của các thành phố đã đi trước.",
        4: "Tôi sẽ đổi ý nếu có bằng chứng rằng có thể giữ nguyên xe máy mà vẫn đạt cùng mức an toàn và sạch — chẳng hạn xe máy điện 100% cộng với làn đường riêng tách biệt hoàn toàn — với chi phí thấp hơn cấm.",
      },
    },
    {
      chuDe: "Có nên cho trẻ nhỏ dùng điện thoại thông minh?",
      mau: {
        1: "Phe ủng hộ cho dùng sớm, ở dạng mạnh nhất: cấm đoán chỉ khiến trẻ tò mò hơn và tụt hậu kỹ năng số so với bạn bè; vấn đề không phải thiết bị mà là nội dung và thời gian — một đứa trẻ xem chương trình khoa học 30 phút/ngày khác hẳn đứa trẻ lướt video ngắn 4 tiếng; và cha mẹ thời nào cũng hoảng sợ trước công nghệ mới của con trẻ, từ truyện tranh đến TV.",
        2: [
          "Luận cứ từ hệ quả: trẻ được hướng dẫn dùng công nghệ sớm sẽ thành thạo công cụ của thời đại mình.",
          "Luận cứ từ nguyên tắc: cấm tuyệt đối là lười biếng trong giáo dục — dạy cách dùng đúng khó hơn nhưng đúng đắn hơn.",
          "Luận cứ từ thực nghiệm: mọi thế hệ đều từng bị cảnh báo về một loại hình giải trí mới, và nỗi hoảng sợ ấy thường bị thổi phồng.",
        ],
        3: "Bằng chứng họ viện dẫn: các nghiên cứu phân biệt “thời gian dùng màn hình” với “nội dung và cách dùng” — tác hại tập trung ở nhóm dùng thụ động, kéo dài, không kiểm soát; và quan sát rằng trẻ bị cấm hoàn toàn thường “bùng nổ” khi có cơ hội tiếp cận.",
        4: "Tôi sẽ đổi ý nếu có nghiên cứu dài hạn, có đối chứng tốt, cho thấy chỉ cần tiếp xúc sớm với smartphone — dù nội dung lành mạnh và có giới hạn thời gian — cũng gây hại đo được cho sự phát triển nhận thức của trẻ.",
      },
    },
  ];

  function presetById(id) {
    for (var i = 0; i < PRESETS.length; i++) if (PRESETS[i].id === id) return PRESETS[i];
    return null;
  }

  /* Tên chủ đề đã chốt: tên preset, hoặc chủ đề tự nhập. */
  function chuDeCua(d) {
    var p = d.presetId ? presetById(d.presetId) : null;
    if (p) return p.ten;
    return (d.chuDeRieng || "").trim();
  }

  /* Ví dụ cho một bước: [{ chuDe, noiDung }]. noiDung là chuỗi (bước 1, 3, 4)
     hoặc mảng 3 chuỗi (bước 2). Ví dụ của chủ đề đã chọn luôn đứng đầu tiên. */
  function examplesFor(presetId, step) {
    var out = [];
    var p = presetId ? presetById(presetId) : null;
    if (p && p.mau && p.mau[step] !== undefined) out.push({ chuDe: p.ten, noiDung: p.mau[step] });
    GENERIC.forEach(function (g) {
      if (g.mau[step] !== undefined) out.push({ chuDe: g.chuDe, noiDung: g.mau[step] });
    });
    return out;
  }

  var TIEU_DE_PHAN = [
    "Phe đối lập ở dạng mạnh nhất",
    "Ba luận cứ tốt nhất của họ",
    "Bằng chứng mạnh nhất họ viện dẫn",
    "Điều gì sẽ làm tôi đổi ý",
  ];

  /* Tổng hợp bản "luận cứ thép". Trả về { chuDe, phan, vanBan }. */
  function buildSummary(d) {
    d = d || {};
    var args = [d.b2a, d.b2b, d.b2c]
      .map(function (a) {
        return (a || "").trim();
      })
      .filter(nonEmpty);
    var phan = [
      { tieuDe: TIEU_DE_PHAN[0], noiDung: (d.b1 || "").trim() },
      {
        tieuDe: TIEU_DE_PHAN[1],
        noiDung: args.map(function (a, i) {
          return i + 1 + ". " + a;
        }),
      },
      { tieuDe: TIEU_DE_PHAN[2], noiDung: (d.b3 || "").trim() },
      { tieuDe: TIEU_DE_PHAN[3], noiDung: (d.b4 || "").trim() },
    ];
    var lines = ["LUẬN CỨ THÉP — " + chuDeCua(d).toUpperCase(), ""];
    phan.forEach(function (p, i) {
      lines.push(i + 1 + ". " + p.tieuDe);
      if (Array.isArray(p.noiDung)) lines = lines.concat(p.noiDung);
      else lines.push(p.noiDung);
      lines.push("");
    });
    return { chuDe: chuDeCua(d), phan: phan, vanBan: lines.join("\n").replace(/\n$/, "") };
  }

  /* ================= Giao diện ================= */

  var STEPS = [
    {
      tieuDe: "Bước 1 — Phe đối lập mạnh nhất",
      goiY: "Hãy phát biểu lại lập trường của phe đối lập ở dạng mạnh nhất có thể — mạnh đến mức chính họ đọc cũng phải nói: “Đúng, đó chính là điều tôi muốn nói.” Cấm dùng phiên bản yếu ớt, cực đoan hóa, hay gán động cơ xấu (“bọn họ chỉ vì tiền/quyền”).",
    },
    {
      tieuDe: "Bước 2 — Ba luận cứ tốt nhất của họ",
      goiY: "Nếu bạn là luật sư bào chữa cho phe đối lập, bạn sẽ đưa ra 3 lý do mạnh nhất nào? Gợi ý: một luận cứ từ hệ quả (nếu theo họ thì điều tốt gì xảy ra), một từ nguyên tắc (giá trị hay quyền nào đang được bảo vệ), một từ thực nghiệm (quan sát hay bằng chứng nào ủng hộ họ).",
    },
    {
      tieuDe: "Bước 3 — Bằng chứng mạnh nhất",
      goiY: "Phe họ viện dẫn bằng chứng, số liệu hay ví dụ cụ thể nào mà bạn thấy khó bác nhất? Ghi cụ thể — “có nghiên cứu nói vậy” không tính; “nghiên cứu nào, nói gì” mới tính.",
    },
    {
      tieuDe: "Bước 4 — Điều gì làm bạn đổi ý",
      goiY: "Điều kiện falsifiability: điều gì — bằng chứng nào, lập luận nào — sẽ khiến bạn đổi ý? Viết cụ thể. Nếu câu trả lời là “không có gì”, hãy thành thật ghi ra: khi đó bạn đang giữ một niềm tin, không phải một kết luận mở.",
    },
  ];

  function init(box) {
    var U = window.OZ.util;
    if (!U.claim(box)) return;
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Luận cứ thép");
    var say = U.live(box);

    var d = { presetId: null, chuDeRieng: "", b1: "", b2a: "", b2b: "", b2c: "", b3: "", b4: "" };
    var step = 0;
    var exIdx = { 1: 0, 2: 0, 3: 0, 4: 0 }; // vị trí xoay vòng ví dụ cho từng bước
    var stage = U.el("div", { class: "oz-steelman__stage" });
    box.appendChild(stage);

    function docDuLieu() {
      // Đọc giá trị các ô nhập hiện tại vào d (giữ lại khi qua lại giữa các bước).
      Array.prototype.forEach.call(stage.querySelectorAll("[data-k]"), function (n) {
        d[n.getAttribute("data-k")] = n.value;
      });
    }

    function loi(msg, focusEl) {
      var e = stage.querySelector(".oz-error");
      if (!e) {
        e = U.el("p", { class: "oz-error", role: "alert" });
        stage.insertBefore(e, stage.firstChild);
      }
      e.textContent = msg;
      say(msg);
      if (focusEl) focusEl.focus();
    }

    function xoaLoi() {
      var e = stage.querySelector(".oz-error");
      if (e) e.remove();
    }

    function nutViDu(stepNum) {
      var ex = examplesFor(d.presetId, stepNum);
      if (!ex.length) return null;
      var hop = U.el("div", { class: "oz-steelman__mau", hidden: true });
      var btn = U.el("button", {
        type: "button",
        class: "md-button",
        text: "Xem ví dụ mẫu",
        onclick: function () {
          var item = ex[exIdx[stepNum] % ex.length];
          exIdx[stepNum]++;
          hop.hidden = false;
          hop.textContent = "";
          hop.appendChild(U.el("p", { class: "oz-steelman__mau-nhan", text: "Ví dụ minh họa — chủ đề: " + item.chuDe }));
          if (Array.isArray(item.noiDung)) {
            var ol = U.el("ol");
            item.noiDung.forEach(function (t) {
              ol.appendChild(U.el("li", { text: t }));
            });
            hop.appendChild(ol);
          } else {
            hop.appendChild(U.el("p", { text: item.noiDung }));
          }
          hop.appendChild(
            U.el("p", { class: "oz-muted", text: "Đừng sao chép — hãy viết bằng lời của bạn. Chính việc viết mới luyện được tư duy." })
          );
          btn.textContent = "Xem ví dụ khác (" + (((exIdx[stepNum] - 1 + ex.length) % ex.length) + 1) + "/" + ex.length + ")";
          say("Đã hiện ví dụ mẫu.");
        },
      });
      return U.el("div", null, [btn, hop]);
    }

    function renderChonChuDe() {
      stage.textContent = "";
      stage.appendChild(U.el("h3", { text: "Chọn chủ đề tranh luận" }));
      stage.appendChild(
        U.el("p", { class: "oz-muted", text: "Chọn một chủ đề có sẵn (kèm bài viết để đọc lại lập trường các bên), hoặc tự nhập chủ đề của bạn." })
      );
      var group = U.el("div", { class: "oz-steelman__chude", role: "radiogroup", "aria-label": "Chủ đề có sẵn" });
      PRESETS.forEach(function (p) {
        var chon = U.el("button", {
          type: "button",
          role: "radio",
          "aria-checked": String(d.presetId === p.id),
          "data-id": p.id,
          text: p.ten,
          onclick: function () {
            d.presetId = p.id;
            custom.value = "";
            d.chuDeRieng = "";
            Array.prototype.forEach.call(group.querySelectorAll("button"), function (c) {
              c.setAttribute("aria-checked", String(c.getAttribute("data-id") === p.id));
            });
          },
        });
        var link = U.el("a", { href: "../" + p.bai.replace(/\.md$/, "/"), text: "Đọc bài viết" });
        group.appendChild(U.el("div", { class: "oz-steelman__chude-item" }, [chon, link]));
      });
      stage.appendChild(group);
      var custom = U.el("input", {
        type: "text",
        class: "oz-steelman__custom",
        "data-k": "chuDeRieng",
        placeholder: "Hoặc tự nhập chủ đề, ví dụ: Có nên bỏ bài tập về nhà?",
        "aria-label": "Tự nhập chủ đề",
        value: d.chuDeRieng,
        oninput: function () {
          if (custom.value.trim()) {
            d.presetId = null;
            Array.prototype.forEach.call(group.querySelectorAll("button"), function (c) {
              c.setAttribute("aria-checked", "false");
            });
          }
        },
      });
      stage.appendChild(custom);
      var hanhDong = U.el("div", { class: "oz-actions" });
      var batDau = U.el("button", {
        type: "button",
        class: "md-button md-button--primary",
        text: "Bắt đầu",
        onclick: function () {
          docDuLieu();
          var err = validateStep(0, d);
          if (err) return loi(err, custom);
          step = 1;
          render();
        },
      });
      hanhDong.appendChild(batDau);
      stage.appendChild(hanhDong);
      say("Chọn chủ đề tranh luận.");
    }

    function renderBuoc(n) {
      stage.textContent = "";
      var cfg = STEPS[n - 1];
      var p = d.presetId ? presetById(d.presetId) : null;
      stage.appendChild(U.el("p", { class: "oz-muted", text: "Chủ đề: " + chuDeCua(d) + " — Bước " + n + "/4" }));
      stage.appendChild(U.el("h3", { text: cfg.tieuDe }));
      if (p) stage.appendChild(U.el("p", { class: "oz-muted", text: p.tinh_huong }));
      stage.appendChild(U.el("p", { text: cfg.goiY }));

      // Gợi ý phe đối lập mẫu (bước 1, khi có preset).
      if (n === 1 && p && p.doi_lap && p.doi_lap.length) {
        stage.appendChild(
          U.el("p", { class: "oz-muted", text: "Chưa rõ phe đối lập nói gì? Gợi ý từ bài viết (bấm để đưa vào ô viết, rồi viết lại bằng lời của bạn):" })
        );
        var chips = U.el("div", { class: "oz-steelman__chips" });
        p.doi_lap.forEach(function (g) {
          chips.appendChild(
            U.el("button", {
              type: "button",
              class: "oz-steelman__chip",
              text: g,
              onclick: function () {
                var ta = stage.querySelector('textarea[data-k="b1"]');
                ta.value = ta.value.trim() ? ta.value.trim() + "\n" + g : g;
                ta.focus();
                say("Đã đưa gợi ý vào ô viết.");
              },
            })
          );
        });
        stage.appendChild(chips);
      }

      var vd = nutViDu(n);
      if (vd) stage.appendChild(vd);

      function oNhap(k, nhan, goiY) {
        var id = "oz-steelman-" + k;
        stage.appendChild(U.el("label", { for: id, text: nhan }));
        stage.appendChild(
          U.el("textarea", {
            id: id,
            "data-k": k,
            class: "oz-steelman__nhap",
            rows: n === 2 ? "3" : "5",
            placeholder: goiY,
            text: d[k],
          })
        );
      }

      if (n === 1) oNhap("b1", "Phát biểu lại lập trường đối lập ở dạng mạnh nhất:", "Viết ở đây — chi tiết đến mức chính phe đối lập cũng phải gật đầu…");
      if (n === 2) {
        oNhap("b2a", "Luận cứ 1 (gợi ý: từ hệ quả):", "Nếu theo phe họ thì điều tốt gì xảy ra?");
        oNhap("b2b", "Luận cứ 2 (gợi ý: từ nguyên tắc):", "Giá trị hay quyền nào đang được bảo vệ?");
        oNhap("b2c", "Luận cứ 3 (gợi ý: từ thực nghiệm):", "Quan sát hay bằng chứng nào ủng hộ họ?");
      }
      if (n === 3) oNhap("b3", "Bằng chứng mạnh nhất phe họ viện dẫn:", "Bằng chứng, số liệu hay ví dụ cụ thể nào khó bác nhất?");
      if (n === 4) oNhap("b4", "Điều gì sẽ làm bạn đổi ý:", "Bằng chứng hay lập luận nào, cụ thể, sẽ khiến bạn đổi ý?");

      var hanhDong = U.el("div", { class: "oz-actions" });
      hanhDong.appendChild(
        U.el("button", {
          type: "button",
          class: "md-button",
          text: "Quay lại",
          onclick: function () {
            docDuLieu();
            step = n - 1;
            render();
          },
        })
      );
      hanhDong.appendChild(
        U.el("button", {
          type: "button",
          class: "md-button md-button--primary",
          text: n === 4 ? "Xem bản tổng hợp" : "Tiếp tục",
          onclick: function () {
            docDuLieu();
            xoaLoi();
            var err = validateStep(n, d);
            if (err) {
              var first = stage.querySelector("textarea");
              return loi(err, first);
            }
            step = n === 4 ? 5 : n + 1;
            render();
          },
        })
      );
      stage.appendChild(hanhDong);
      var first = stage.querySelector("textarea");
      if (first) first.focus();
      say(cfg.tieuDe + ".");
    }

    function renderTongHop() {
      stage.textContent = "";
      var s = buildSummary(d);
      stage.appendChild(U.el("p", { class: "oz-muted", text: "Hoàn thành — đây là bản “luận cứ thép” của bạn." }));
      stage.appendChild(U.el("h3", { text: "Bản luận cứ thép: " + s.chuDe }));
      s.phan.forEach(function (p, i) {
        stage.appendChild(U.el("h4", { text: i + 1 + ". " + p.tieuDe }));
        if (Array.isArray(p.noiDung)) {
          var ol = U.el("ol");
          p.noiDung.forEach(function (t) {
            ol.appendChild(U.el("li", { text: t.replace(/^\d+\.\s*/, "") }));
          });
          stage.appendChild(ol);
        } else {
          stage.appendChild(U.el("p", { text: p.noiDung }));
        }
      });
      stage.appendChild(U.el("h4", { text: "Bản text để lưu hoặc chia sẻ" }));
      var ta = U.el("textarea", {
        class: "oz-steelman__nhap",
        rows: "10",
        readonly: true,
        "aria-label": "Bản text luận cứ thép",
        text: s.vanBan,
      });
      stage.appendChild(ta);
      var hanhDong = U.el("div", { class: "oz-actions" });
      var copyBtn = U.el("button", { type: "button", class: "md-button", text: "Sao chép" });
      copyBtn.addEventListener("click", function () {
        function baoXong() {
          copyBtn.textContent = "Đã sao chép";
          say("Đã sao chép bản luận cứ thép.");
          setTimeout(function () {
            copyBtn.textContent = "Sao chép";
          }, 2000);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(s.vanBan).then(baoXong, function () {
            ta.select();
            say("Không sao chép tự động được — hãy bấm Ctrl+C.");
          });
        } else {
          ta.select();
          try {
            document.execCommand("copy");
            baoXong();
          } catch (e) {
            say("Hãy bấm Ctrl+C để sao chép.");
          }
        }
      });
      hanhDong.appendChild(copyBtn);
      hanhDong.appendChild(
        U.el("button", {
          type: "button",
          class: "md-button md-button--primary",
          text: "Làm lại từ đầu",
          onclick: function () {
            d = { presetId: null, chuDeRieng: "", b1: "", b2a: "", b2b: "", b2c: "", b3: "", b4: "" };
            step = 0;
            exIdx = { 1: 0, 2: 0, 3: 0, 4: 0 };
            render();
          },
        })
      );
      stage.appendChild(hanhDong);
      stage.appendChild(
        U.el("p", { class: "oz-muted", text: "Công cụ này không lưu gì cả — bản viết của bạn chỉ tồn tại trên trang này, như một bài tập nháp." })
      );
      say("Hoàn thành bản luận cứ thép.");
    }

    function render() {
      xoaLoi();
      if (step === 0) renderChonChuDe();
      else if (step === 5) renderTongHop();
      else renderBuoc(step);
      if (box.scrollIntoView) {
        try {
          box.scrollIntoView({ block: "start", behavior: "smooth" });
        } catch (e) {}
      }
    }

    render();
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-steelman"), init);
  }

  return {
    MIN_LEN: MIN_LEN,
    STEPS: STEPS,
    PRESETS: PRESETS,
    GENERIC: GENERIC,
    presetById: presetById,
    chuDeCua: chuDeCua,
    examplesFor: examplesFor,
    validateStep: validateStep,
    buildSummary: buildSummary,
    initAll: initAll,
  };
});
