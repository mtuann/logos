/* Logos Zero — kế hoạch học thích ứng.
 * <div class="oz-ke-hoach"></div>
 * Gợi ý bài học tiếp theo dựa trên tiến độ đã lưu (EMA từng kỹ năng + bài đã đọc).
 * CHỈ gợi ý, KHÔNG chấm điểm, KHÔNG gọi P.record.
 * Mẫu UMD của repo: hàm thuần xuất qua module.exports; trình duyệt dùng OZReady(initAll). */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.kehoach = api;
    if (root.OZReady) root.OZReady(api.initAll);
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* Tên hiển thị của 17 kỹ năng (đồng bộ với SKILL_NAMES trong mydata.js). */
  var SKILL_NAMES = {
    intro: "Nhập môn",
    argument: "Nhận ra lập luận",
    deduction: "Suy diễn",
    induction: "Quy nạp",
    assumption: "Giả định ngầm",
    fallacy: "Nhận ra ngụy biện",
    logic: "Logic mệnh đề",
    knowledge: "Tri thức",
    mind: "Tâm trí và AI",
    freewill: "Tự do ý chí",
    vietnam: "Triết học Việt Nam",
    ethics: "Đạo đức học",
    politics: "Triết học chính trị",
    aesthetics: "Mỹ học",
    religion: "Triết học tôn giáo",
    metaphysics: "Siêu hình học",
    meaning: "Ý nghĩa cuộc sống",
    terms: "Thuật ngữ",
  };

  var LEVEL_TITLES = {
    "nhap-mon": "Bắt đầu từ đây",
    "on-tap": "Đến hạn ôn tập",
    "cung-co": "Cần củng cố",
    "thu-suc": "Thử sức mới",
    vung: "Đã vững — đi tiếp",
  };

  var LEVEL_DESCS = {
    "nhap-mon": "Bạn chưa có dữ liệu học tập nào trên máy này. Ba mục dưới đây là điểm khởi đầu tốt.",
    "on-tap": "Thuật ngữ và câu hỏi trắc nghiệm đến hạn theo phương pháp ngắt quãng — ôn càng đúng hẹn càng nhớ lâu.",
    "cung-co": "Tỉ lệ đúng còn thấp — ôn lại từ đầu sẽ hiệu quả hơn học bài mới.",
    "thu-suc": "Những kỹ năng bạn chưa từng thử. Mỗi mục chỉ mất vài phút.",
    vung: "Bạn đã nắm chắc — thử bài chưa đọc để mở rộng.",
  };

  /* Danh mục gợi ý: {skill, title, path, kind: 'bai'|'tool'}.
   * path là đường dẫn tuyệt đối dạng /muc/bai/ (khớp với khóa state.read của loader). */
  var CATALOG = [
    { skill: "intro", title: "Triết học là gì, và không phải là gì?", path: "/bat-dau/", kind: "bai" },
    { skill: "intro", title: "Ba con đường đọc", path: "/bat-dau/lo-trinh/", kind: "bai" },
    { skill: "intro", title: "Cách đọc một văn bản triết học khó", path: "/cong-cu/doc-van-ban-kho/", kind: "bai" },
    { skill: "intro", title: "Đọc “Biện hộ của Socrates”", path: "/doc/platon-bien-ho/", kind: "bai" },
    { skill: "intro", title: "Đọc Russell: “Giá trị của triết học”", path: "/doc/russell-gia-tri/", kind: "bai" },
    { skill: "argument", title: "Lập luận là gì?", path: "/cong-cu/lap-luan-la-gi/", kind: "bai" },
    { skill: "argument", title: "Sơ đồ hóa lập luận (công cụ)", path: "/cong-cu/so-do-hoa-lap-luan/", kind: "tool" },
    { skill: "argument", title: "Thế nào là một định nghĩa tốt?", path: "/cong-cu/dinh-nghia-phan-vi-du/", kind: "bai" },
    { skill: "argument", title: "Cách viết một đoạn lập luận", path: "/cong-cu/viet-doan-lap-luan/", kind: "bai" },
    { skill: "argument", title: "Thí nghiệm tư duy", path: "/cong-cu/thi-nghiem-tu-duy/", kind: "bai" },
    { skill: "argument", title: "Phép biện chứng Socrates", path: "/cong-cu/bien-chung-socrates/", kind: "bai" },
    { skill: "argument", title: "Luận cứ thép (công cụ)", path: "/cong-cu/luan-cu-thep/", kind: "tool" },
    { skill: "deduction", title: "Khi nào kết luận buộc phải đúng?", path: "/cong-cu/suy-dien/", kind: "bai" },
    { skill: "deduction", title: "Cần khác đủ như thế nào?", path: "/cong-cu/dieu-kien-can-du/", kind: "bai" },
    { skill: "induction", title: "Khi bằng chứng chỉ làm cho “có lẽ đúng”", path: "/cong-cu/quy-nap/", kind: "bai" },
    { skill: "assumption", title: "Điều không được nói ra", path: "/cong-cu/gia-dinh-ngam/", kind: "bai" },
    { skill: "fallacy", title: "Ngụy biện", path: "/cong-cu/nguy-bien/", kind: "bai" },
    { skill: "fallacy", title: "Nhận ra ngụy biện (luyện tập)", path: "/luyen-tap/nguy-bien/", kind: "tool" },
    { skill: "fallacy", title: "Ngụy biện hình thức", path: "/cong-cu/nguy-bien-hinh-thuc/", kind: "bai" },
    { skill: "logic", title: "Bảng chân trị: khi lập luận thành phép tính", path: "/cong-cu/logic-menh-de/", kind: "tool" },
    { skill: "knowledge", title: "Biết một điều nghĩa là gì?", path: "/cau-hoi/tri-thuc/", kind: "bai" },
    { skill: "knowledge", title: "Tin vào lời người khác?", path: "/cau-hoi/loi-chung/", kind: "bai" },
    { skill: "knowledge", title: "Khi người giỏi cãi nhau?", path: "/cau-hoi/bat-dong-tri-thuc/", kind: "bai" },
    { skill: "knowledge", title: "Sự thật là gì?", path: "/cau-hoi/chan-ly/", kind: "bai" },
    { skill: "knowledge", title: "Khoa học khác gì phi khoa học?", path: "/cau-hoi/khoa-hoc/", kind: "bai" },
    { skill: "knowledge", title: "Ngôn từ có định hình tư duy?", path: "/cau-hoi/ngon-ngu/", kind: "bai" },
    { skill: "knowledge", title: "Đọc Hume về nhân quả", path: "/doc/hume-nhan-qua/", kind: "bai" },
    { skill: "knowledge", title: "Đọc “Suy niệm” của Descartes", path: "/doc/descartes-suy-niem/", kind: "bai" },
    { skill: "knowledge", title: "Đọc ẩn dụ hang động của Platon", path: "/doc/platon-hang-dong/", kind: "bai" },
    { skill: "knowledge", title: "Đọc Trang Tử: mộng hồ điệp", path: "/doc/trang-tu-mong-ho-diep/", kind: "bai" },
    { skill: "mind", title: "Một cỗ máy có thể có tâm trí không?", path: "/cau-hoi/tam-tri-va-ai/", kind: "bai" },
    { skill: "mind", title: "Thân xác và tâm trí?", path: "/cau-hoi/van-de-tam-tri/", kind: "bai" },
    { skill: "mind", title: "Cái “tôi” là gì?", path: "/cau-hoi/cai-toi/", kind: "bai" },
    { skill: "mind", title: "AI thay đổi con người thế nào?", path: "/cau-hoi/cong-nghe-ai/", kind: "bai" },
    { skill: "freewill", title: "Ta có thật sự tự do lựa chọn?", path: "/cau-hoi/tu-do-y-chi/", kind: "bai" },
    { skill: "freewill", title: "Ta có đáng bị trách?", path: "/cau-hoi/trach-nhiem/", kind: "bai" },
    { skill: "freewill", title: "Mọi thứ đã được viết sẵn?", path: "/cau-hoi/dinh-menh/", kind: "bai" },
    { skill: "freewill", title: "Đọc Sartre: “Thuyết hiện sinh là một thuyết nhân bản”", path: "/doc/sartre-hien-sinh/", kind: "bai" },
    { skill: "vietnam", title: "Thiền phái Trúc Lâm", path: "/cau-hoi/truc-lam/", kind: "bai" },
    { skill: "vietnam", title: "Nho giáo Việt Nam", path: "/cau-hoi/nho-giao-viet/", kind: "bai" },
    { skill: "vietnam", title: "Triết học Việt Nam hiện đại", path: "/cau-hoi/viet-hien-dai/", kind: "bai" },
    { skill: "vietnam", title: "Đọc “Bình Ngô đại cáo”", path: "/doc/nguyen-trai-binh-ngo/", kind: "bai" },
    { skill: "vietnam", title: "Đọc Thơ văn Lý–Trần", path: "/doc/tho-van-ly-tran/", kind: "bai" },
    { skill: "ethics", title: "Hành động đúng là gì?", path: "/cau-hoi/dao-duc-hanh-dong/", kind: "bai" },
    { skill: "ethics", title: "Đúng sai có khách quan không?", path: "/cau-hoi/sieu-dao-duc/", kind: "bai" },
    { skill: "ethics", title: "Có bao giờ được nói dối?", path: "/cau-hoi/noi-doi/", kind: "bai" },
    { skill: "ethics", title: "Bản tính con người thiện hay ác?", path: "/cau-hoi/ban-tinh-con-nguoi/", kind: "bai" },
    { skill: "ethics", title: "Ăn thịt có sai không?", path: "/cau-hoi/dao-duc-ung-dung/", kind: "bai" },
    { skill: "ethics", title: "Có nghĩa vụ cứu người nghèo đói?", path: "/cau-hoi/cuu-giup-ngheo-doi/", kind: "bai" },
    { skill: "ethics", title: "Thiên nhiên có giá trị tự thân?", path: "/cau-hoi/dao-duc-moi-truong/", kind: "bai" },
    { skill: "ethics", title: "Ai chịu trách nhiệm cho khí hậu?", path: "/cau-hoi/khi-hau-trach-nhiem/", kind: "bai" },
    { skill: "ethics", title: "Phá thai có sai không?", path: "/cau-hoi/pha-thai/", kind: "bai" },
    { skill: "ethics", title: "Án tử hình có chính đáng?", path: "/cau-hoi/an-tu-hinh/", kind: "bai" },
    { skill: "ethics", title: "Hiến tạng: ai quyết định?", path: "/cau-hoi/hien-tang/", kind: "bai" },
    { skill: "ethics", title: "Quyền riêng tư thời đại số", path: "/cau-hoi/quyen-rieng-tu-so/", kind: "bai" },
    { skill: "ethics", title: "Cái ác là gì?", path: "/cau-hoi/cai-ac/", kind: "bai" },
    { skill: "ethics", title: "Đọc “Đạo đức Nicomachus”", path: "/doc/aristotle-dao-duc/", kind: "bai" },
    { skill: "ethics", title: "Đọc “Luận ngữ” của Khổng Tử", path: "/doc/luan-ngu/", kind: "bai" },
    { skill: "ethics", title: "Đọc Mạnh Tử: tính thiện", path: "/doc/manh-tu-tinh-thien/", kind: "bai" },
    { skill: "ethics", title: "Đọc Mặc Tử: kiêm ái", path: "/doc/mac-tu-kiem-ai/", kind: "bai" },
    { skill: "politics", title: "Vì sao phải vâng lời nhà nước?", path: "/cau-hoi/khe-uoc-xa-hoi/", kind: "bai" },
    { skill: "politics", title: "Công lý là gì?", path: "/cau-hoi/cong-ly/", kind: "bai" },
    { skill: "politics", title: "Dân chủ là gì?", path: "/cau-hoi/dan-chu/", kind: "bai" },
    { skill: "politics", title: "Cai trị bằng đức hay bằng pháp?", path: "/cau-hoi/duc-tri/", kind: "bai" },
    { skill: "politics", title: "Bình đẳng là gì?", path: "/cau-hoi/binh-dang/", kind: "bai" },
    { skill: "politics", title: "Triết học nữ quyền là gì?", path: "/cau-hoi/nu-quyen/", kind: "bai" },
    { skill: "politics", title: "Tài sản riêng có chính đáng?", path: "/cau-hoi/tai-san-rieng/", kind: "bai" },
    { skill: "politics", title: "Tự do ngôn luận đến đâu?", path: "/cau-hoi/tu-do-ngon-luan/", kind: "bai" },
    { skill: "politics", title: "Chiến tranh có bao giờ chính đáng?", path: "/cau-hoi/chien-tranh-chinh-dang/", kind: "bai" },
    { skill: "politics", title: "Biên giới và di cư", path: "/cau-hoi/bien-gioi-di-cu/", kind: "bai" },
    { skill: "politics", title: "Ai nên cai trị?", path: "/cau-hoi/ai-nen-cai-tri/", kind: "bai" },
    { skill: "politics", title: "Đọc Mill: “Bàn về tự do”", path: "/doc/mill-tu-do/", kind: "bai" },
    { skill: "politics", title: "Đọc Kant: “Khai sáng là gì?”", path: "/doc/kant-khai-sang/", kind: "bai" },
    { skill: "aesthetics", title: "Cái đẹp ở trong mắt người nhìn?", path: "/cau-hoi/cai-dep/", kind: "bai" },
    { skill: "aesthetics", title: "Cái gì làm nên nghệ thuật?", path: "/cau-hoi/nghe-thuat/", kind: "bai" },
    { skill: "religion", title: "Có thể chứng minh Chúa tồn tại?", path: "/cau-hoi/luan-chung-ton-giao/", kind: "bai" },
    { skill: "religion", title: "Có nên tin mà không cần bằng chứng?", path: "/cau-hoi/duc-tin-ly-tri/", kind: "bai" },
    { skill: "religion", title: "Vì sao có đau khổ?", path: "/cau-hoi/van-de-su-du/", kind: "bai" },
    { skill: "metaphysics", title: "Cái gì thực sự tồn tại?", path: "/cau-hoi/cai-gi-ton-tai/", kind: "bai" },
    { skill: "metaphysics", title: "Phổ quát có thật không?", path: "/cau-hoi/pho-quat/", kind: "bai" },
    { skill: "metaphysics", title: "Thời gian có trôi không?", path: "/cau-hoi/thoi-gian/", kind: "bai" },
    { skill: "metaphysics", title: "Nhân quả là gì?", path: "/cau-hoi/nhan-qua-ban-chat/", kind: "bai" },
    { skill: "metaphysics", title: "Vũ trụ có khởi đầu?", path: "/cau-hoi/vu-tru-khoi-dau/", kind: "bai" },
    { skill: "metaphysics", title: "Con người có linh hồn?", path: "/cau-hoi/linh-hon/", kind: "bai" },
    { skill: "metaphysics", title: "Ta có đang sống trong mô phỏng?", path: "/cau-hoi/mo-phong/", kind: "bai" },
    { skill: "metaphysics", title: "Cái tôi qua thời gian", path: "/cau-hoi/ban-nga-thoi-gian/", kind: "bai" },
    { skill: "metaphysics", title: "Đọc “Đạo đức kinh”", path: "/doc/dao-duc-kinh/", kind: "bai" },
    { skill: "metaphysics", title: "Đọc “Bát nhã Tâm kinh”", path: "/doc/tam-kinh/", kind: "bai" },
    { skill: "meaning", title: "Cuộc sống có ý nghĩa không?", path: "/cau-hoi/y-nghia-song/", kind: "bai" },
    { skill: "meaning", title: "Hạnh phúc là gì?", path: "/cau-hoi/hanh-phuc/", kind: "bai" },
    { skill: "meaning", title: "Tình yêu là gì?", path: "/cau-hoi/tinh-yeu/", kind: "bai" },
    { skill: "meaning", title: "Chết có đáng sợ không?", path: "/cau-hoi/cai-chet/", kind: "bai" },
    { skill: "meaning", title: "Đọc “Suy tưởng” của Marcus Aurelius", path: "/doc/aurelius-suy-tuong/", kind: "bai" },
    { skill: "meaning", title: "Đọc “Cẩm nang” của Epictetus", path: "/doc/epictetus-cam-nang/", kind: "bai" },
    { skill: "terms", title: "Thẻ ghi nhớ thuật ngữ", path: "/luyen-tap/the-ghi-nho/", kind: "tool" },
    { skill: "terms", title: "Ôn tập thông minh", path: "/luyen-tap/on-tap/", kind: "tool" },
  ];

  function normPath(p) {
    return String(p || "").replace(/\/+$/, "");
  }

  /* Hàm thuần: từ state (đã migrate hoặc thô) + catalog → các nhóm gợi ý.
   * Trả về [{level, skill, skillName, items:[{title, path, kind}]}].
   * level: 'nhap-mon' | 'on-tap' | 'cung-co' | 'thu-suc' | 'vung'.
   * review (tùy chọn): {dueTerms, dueQuestions} hoặc {terms, questions} — số mục ôn tập đến hạn; nếu > 0
   * thêm nhóm "Ôn tập" lên đầu danh sách. */
  function recommend(state, catalog, review) {
    catalog = catalog || CATALOG;
    var skills = (state && state.skills) || {};
    var read = (state && state.read) || {};
    var groups = [];

    var dueT = (review && (review.dueTerms || review.terms)) || 0;
    var dueQ = (review && (review.dueQuestions || review.questions)) || 0;
    if (dueT + dueQ > 0) {
      groups.push({
        level: "on-tap",
        skill: "review",
        skillName: "Ôn tập thông minh",
        items: [
          {
            title: "Ôn tập: " + dueT + " thuật ngữ, " + dueQ + " câu hỏi đến hạn",
            path: "/luyen-tap/on-tap/",
            kind: "tool",
          },
        ],
      });
    }

    function isRead(path) {
      var want = normPath(path);
      return Object.keys(read).some(function (k) {
        return normPath(k) === want;
      });
    }

    function itemsFor(skill, preferUnread, count) {
      var items = catalog.filter(function (c) {
        return c.skill === skill;
      });
      var unread = items.filter(function (c) {
        return !isRead(c.path);
      });
      var pool = preferUnread && unread.length ? unread : items;
      return pool.slice(0, count).map(function (c) {
        return { title: c.title, path: c.path, kind: c.kind };
      });
    }

    function firstOf(skill) {
      var items = itemsFor(skill, true, 1);
      return items.length ? items[0] : null;
    }

    var hasData = Object.keys(skills).some(function (k) {
      return skills[k] && (skills[k].n || 0) > 0;
    });

    /* Chưa có dữ liệu gì: gợi 3 mục nhập môn (giữ nhóm ôn tập ở đầu nếu có). */
    if (!hasData) {
      var intro = [firstOf("intro"), firstOf("argument"), firstOf("logic")].filter(Boolean);
      return groups.concat([{ level: "nhap-mon", skill: null, skillName: null, items: intro }]);
    }

    var buckets = { "cung-co": [], "thu-suc": [], vung: [] };
    var seen = {};
    catalog.forEach(function (c) {
      if (seen[c.skill]) return;
      seen[c.skill] = true;
      var sk = skills[c.skill] || {};
      var n = sk.n || 0;
      var ema = sk.ema;
      if (n > 0 && ema !== null && ema !== undefined && ema < 0.6) buckets["cung-co"].push(c.skill);
      else if (n === 0) buckets["thu-suc"].push(c.skill);
      else if (ema !== null && ema !== undefined && ema >= 0.8 && n >= 5) buckets.vung.push(c.skill);
    });

    buckets["cung-co"].forEach(function (skill) {
      var items = itemsFor(skill, true, 2);
      if (items.length) groups.push({ level: "cung-co", skill: skill, skillName: SKILL_NAMES[skill] || skill, items: items });
    });
    buckets["thu-suc"].forEach(function (skill) {
      var items = itemsFor(skill, true, 1);
      if (items.length) groups.push({ level: "thu-suc", skill: skill, skillName: SKILL_NAMES[skill] || skill, items: items });
    });
    buckets.vung.forEach(function (skill) {
      var items = itemsFor(skill, true, 2);
      if (items.length) groups.push({ level: "vung", skill: skill, skillName: SKILL_NAMES[skill] || skill, items: items });
    });
    return groups;
  }

  var KIND_LABELS = { bai: "Bài đọc", tool: "Công cụ" };

  function render(box, review) {
    var U = window.OZ.util;
    var P = window.OZ.progress;
    box.textContent = "";
    var say = U.live(box);
    var groups = recommend(P.load(), CATALOG, review);
    if (!groups.length) {
      box.appendChild(U.el("p", { class: "oz-muted", text: "Bạn đã đọc hết các gợi ý. Hãy quay lại khi có bài mới." }));
      return;
    }
    groups.forEach(function (g) {
      var sec = U.el("section", { class: "oz-ke-hoach__nhom" });
      sec.appendChild(U.el("h3", { text: (g.skillName ? g.skillName + " — " : "") + LEVEL_TITLES[g.level] }));
      sec.appendChild(U.el("p", { class: "oz-muted", text: LEVEL_DESCS[g.level] }));
      var ul = U.el("ul", { class: "oz-ke-hoach__ds" });
      g.items.forEach(function (it) {
        var a = U.el("a", { href: it.path, text: it.title });
        ul.appendChild(
          U.el("li", null, [a, U.el("span", { class: "oz-ke-hoach__kind", text: " · " + (KIND_LABELS[it.kind] || it.kind) })])
        );
      });
      sec.appendChild(ul);
      box.appendChild(sec);
    });
    var refresh = U.el("button", {
      type: "button",
      class: "md-button",
      text: "Làm mới gợi ý",
      onclick: function () {
        refreshAll(box);
        say("Đã cập nhật gợi ý theo tiến độ mới nhất.");
      },
    });
    box.appendChild(U.el("div", { class: "oz-actions" }, [refresh]));
  }

  /* Tải dữ liệu ôn tập rồi render; lỗi tải thì render không có nhóm ôn tập. */
  function refreshAll(box) {
    var U = window.OZ.util;
    var P = window.OZ.progress;
    var OT = window.OZ.onTap;
    if (!OT) {
      render(box, null);
      return;
    }
    Promise.all([U.fetchJSON("assets/data/terms.json"), U.fetchJSON("assets/data/quiz-bank.json")])
      .then(function (res) {
        var st = P ? P.load() : { cards: {} };
        var today = P ? P.today() : new Date().toISOString().slice(0, 10);
        render(box, OT.dueCounts(res[0].terms || [], res[1].items || [], st.cards || {}, today));
      })
      .catch(function () {
        render(box, null);
      });
  }

  function initAll(doc) {
    Array.prototype.forEach.call((doc || document).querySelectorAll(".oz-ke-hoach"), function (box) {
      var U = window.OZ.util;
      if (!U.claim(box)) return;
      box.appendChild(U.el("p", { class: "oz-muted", text: "Đang tải gợi ý…" }));
      refreshAll(box);
    });
  }

  return { SKILL_NAMES: SKILL_NAMES, CATALOG: CATALOG, recommend: recommend, initAll: initAll };
});
