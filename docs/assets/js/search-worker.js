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
  Builder.prototype = Base.prototype;
  lunr.Builder = Builder;
})();
