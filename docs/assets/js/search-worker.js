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
  var doDaiTieuDe = {};   // location → độ dài tiêu đề gốc, để bỏ vị trí khớp nằm trong phần chữ thêm (xem ozCatViTri)
  Builder.prototype.add = function (doc, attrs) {
    var loc = doc && typeof doc.location === "string" ? doc.location : null;
    if (loc !== null && loc.indexOf("#") < 0) {
      var m = loc.match(/([^\/]+)\/$/);
      if (m) {
        doDaiTieuDe[loc] = (doc.title || "").length;
        doc = Object.assign({}, doc, { title: (doc.title || "") + " " + m[1].replace(/-/g, " ") });
      }
    }
    return Base.prototype.add.call(this, doc, attrs);
  };
  lunr.Builder = Builder;
  /* Đợt 7.1.3: Material để mọi từ là tùy chọn (OPTIONAL), nên một từ ngắn ("y", "do") kéo vào cả trăm mục. Mọi từ
   * không mang dấu + hay - thì thành bắt buộc: kết quả phải chứa đủ các từ đã gõ. */
  function ozBatBuoc(clause) {
    if (clause.presence === undefined || clause.presence === lunr.Query.presence.OPTIONAL) {
      clause.presence = lunr.Query.presence.REQUIRED;
    }
    return clause;
  }
  /* Material thêm `*` vào cuối mọi từ của câu truy vấn, và lunr giữ dấu `*` ngay trong chữ của từ (cờ wildcard vẫn là
   * 0; bước của đợt 6.1 xét cờ nên chưa từng có tác dụng). Đợt 7.1.3 (lượt 2), xét chữ của từ sau khi lunr phân tích:
   * - từ không phải từ cuối: người đọc đã gõ xong, khớp nguyên từ ("tri*" từng khớp cả "triết", "triển", nên
   *   "tri thuc" kéo về 160 mục với bài Phá thai đứng đầu);
   * - từ cuối (có thể đang gõ dở) giữ `*`, trừ khi chỉ có ≤ 2 chữ cái (quyết định 38: "y*", "do*" khớp quá rộng).
   * Dấu + / - và field: của người đọc vẫn giữ, vì chỉ bỏ dấu `*` cuối. */
  function ozBoSao(clauses) {
    for (var i = 0; i < clauses.length; i++) {
      var c = clauses[i], t = String(c.term);
      if (!/\*$/.test(t)) continue;
      var goc = t.replace(/\*+$/, "");
      if (i < clauses.length - 1 || goc.length <= 2) {
        c.term = goc;
        c.wildcard &= ~lunr.Query.wildcard.TRAILING;
      }
    }
  }
  /* Từ cuối giữ `*` vẫn khớp cả từ dài hơn ("chi*" khớp "chiến"). Thêm một mệnh đề tùy chọn cho đúng từ ấy, trọng số
   * cao: mục chứa nguyên từ xếp trên mục chỉ khớp tiền tố. Mệnh đề tùy chọn đi cùng mệnh đề bắt buộc chỉ đổi điểm,
   * không thêm hay bớt kết quả. */
  function ozNguyenTu(query) {
    var cl = query.clauses, c = cl[cl.length - 1];
    if (!c || !/\*$/.test(String(c.term)) || c.presence === lunr.Query.presence.PROHIBITED) return;
    query.clause({ term: String(c.term).replace(/\*+$/, ""), fields: c.fields, boost: 10, usePipeline: true,
                   wildcard: lunr.Query.wildcard.NONE, presence: lunr.Query.presence.OPTIONAL });
  }
  /* Dọn vị trí khớp trước khi trả kết quả cho Material (Material tô sáng theo vị trí; điểm và thứ hạng không đổi):
   * - vị trí nằm trong phần chữ của địa chỉ trang gắn thêm vào tiêu đề (ở trên) vượt quá tiêu đề gốc, nên kết quả
   *   hiện mẩu thẻ vỡ ("tri thứcrk>", "<mark></mark>"): bỏ;
   * - một từ có dấu và bản không dấu của nó (ozBoDau) cùng vị trí, nên "chi*" khớp cả "chiến" lẫn "chien" và Material
   *   chèn hai thẻ chồng nhau ("gây >chiến"): trong mỗi trường, mỗi vị trí chỉ giữ một lần. */
  function ozCatViTri(results) {
    results.forEach(function (r) {
      var n = doDaiTieuDe[r.ref];
      var md = r.matchData.metadata, daCo = {};
      Object.keys(md).forEach(function (term) {
        Object.keys(md[term]).forEach(function (field) {
          var f = md[term][field];
          if (!f || !f.position) return;
          var seen = daCo[field] || (daCo[field] = {});
          f.position = f.position.filter(function (p) {
            if (field === "title" && n !== undefined && p[0] + p[1] > n) return false;
            var k = p[0] + "," + p[1];
            if (seen[k]) return false;
            seen[k] = true;
            return true;
          });
        });
      });
    });
    return results;
  }
  lunr.Index.prototype.search = function (queryString) {
    return ozCatViTri(this.query(function (query) {
      new lunr.QueryParser(queryString, query).parse();
      ozBoSao(query.clauses);
      ozNguyenTu(query);
    }));
  };
  var baseClause = lunr.Query.prototype.clause;
  lunr.Query.prototype.clause = function (clause) {
    return baseClause.call(this, ozBatBuoc(clause));
  };
})();
