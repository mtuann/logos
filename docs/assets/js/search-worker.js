/* Worker tìm kiếm của site (đợt 4.5, quyết định 22): chạy chính worker của Material 9.8.0 (bản cuối, giao thức tin
 * nhắn không đổi) và thêm một bước vào pipeline dựng chỉ mục của lunr: mỗi từ có dấu được ghi thêm dạng không dấu
 * (gồm đ → d), cùng vị trí. Gõ "dao duc" khớp dạng không dấu; gõ "đạo đức" khớp đúng dạng có dấu như trước.
 * Nhờ vậy search_index.json không cần bản sao không dấu (hooks/search_vi.py): bản sao chỉ nằm trong bộ nhớ worker.
 * Câu truy vấn giữ nguyên như người đọc gõ (không đưa bước này vào searchPipeline).
 * Đổi phiên bản Material thì sửa tên file bên dưới (tests/test_hooks.py kiểm file có thật). */
importScripts("../javascripts/workers/search.a7633da7.min.js");

(function () {
  function boDau(s) {
    return s.replace(/đ/g, "d").replace(/Đ/g, "D").normalize("NFD").replace(/[̀-ͯ]/g, "").normalize("NFC");
  }
  function ozBoDau(token) {
    var s = token.toString();
    var b = boDau(s);
    return b === s ? token : [token, token.clone(function () { return b; })];
  }
  lunr.Pipeline.registerFunction(ozBoDau, "ozBoDau");
  var Base = lunr.Builder;
  function Builder() {
    Base.call(this);
    this.pipeline.add(ozBoDau);
  }
  Builder.prototype = Object.create(Base.prototype);
  Builder.prototype.constructor = Builder;
  /* Đợt 7.1.3: mục đại diện cả trang (location không có #) được thêm chữ của địa chỉ trang vào tiêu đề
   * ("cau-hoi/tri-thuc/" → "tri thuc"), vì tiêu đề bài thường là một câu hỏi không chứa tên chủ đề
   * ("Biết một điều nghĩa là gì?"). Chỉ trong bộ nhớ worker; search_index.json không đổi. */
  Builder.prototype.add = function (doc, attrs) {
    var loc = doc && typeof doc.location === "string" ? doc.location : null;
    if (loc !== null && loc.indexOf("#") < 0) {
      var m = loc.match(/([^\/]+)\/$/);
      if (m) doc = Object.assign({}, doc, { title: (doc.title || "") + " " + m[1].replace(/-/g, " ") });
    }
    return Base.prototype.add.call(this, doc, attrs);
  };
  lunr.Builder = Builder;
  /* Đợt 6.1 (quyết định 38): Material thêm `*` vào cuối mọi từ của câu truy vấn. Với từ ≤ 2 chữ cái ("tu", "do",
   * "y") đuôi `*` khớp quá rộng nên bài chính tụt hạng. Từ ngắn như vậy khớp nguyên từ (bỏ wildcard cuối). */
  function ozTuNgan(clause) {
    var W = lunr.Query.wildcard;
    /* Đợt 7.1.3: Material để mọi từ là tùy chọn (OPTIONAL), nên một từ ngắn ("y", "do") kéo vào cả trăm mục. Mọi
     * từ không mang dấu + hay - thì thành bắt buộc: kết quả phải chứa đủ các từ đã gõ. */
    if (clause.presence === undefined || clause.presence === lunr.Query.presence.OPTIONAL) {
      clause.presence = lunr.Query.presence.REQUIRED;
    }
    if (clause.wildcard & W.TRAILING) {
      var t = String(clause.term).replace(/\*$/, "");
      if (t.length <= 2) {
        clause.wildcard &= ~W.TRAILING;
        clause.term = t;
      }
    }
    return clause;
  }
  var baseClause = lunr.Query.prototype.clause;
  lunr.Query.prototype.clause = function (clause) {
    return baseClause.call(this, ozTuNgan(clause));
  };
})();
