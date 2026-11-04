/* Logos Zero — lưu trữ và tiến độ.
 * Một khóa localStorage duy nhất, có phiên bản. Các hàm thuần (không đụng localStorage)
 * được xuất ra để kiểm thử: emptyState, migrate, applyAnswer, applyQuiz, markRead,
 * addJournalEntry, today. */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.progress = api;
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  // Khóa riêng của logos. logos-zero dùng khóa "logos-zero" trên cùng origin mtuann.github.io,
  // nên hai site không được dùng chung khóa (KE-HOACH.md, quyết định 9).
  var KEY = "logos";
  var VERSION = 1;
  var ALPHA = 0.3; // hệ số làm trơn EMA cho độ chính xác
  var HISTORY_DAYS = 400;

  function today(d) {
    d = d || new Date();
    var m = d.getMonth() + 1;
    var day = d.getDate();
    return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (day < 10 ? "0" : "") + day;
  }

  function emptyState() {
    // imports: nhật ký các file đã gộp {deviceId, exportedAt} — chống nhập trùng.
    // journal: ghi chép của người dùng {date: [{t: "HH:MM", text}]}.
    return { v: VERSION, skills: {}, days: {}, quizzes: {}, read: {}, cards: {}, items: {}, journal: {}, imports: [] };
  }

  function isObj(x) {
    return x !== null && typeof x === "object" && !Array.isArray(x);
  }

  // Đưa dữ liệu bất kỳ (cũ, hỏng, null) về đúng cấu trúc hiện hành.
  function migrate(raw) {
    var s = emptyState();
    if (!isObj(raw)) return s;
    Object.keys(s).forEach(function (k) {
      if (k === "v") return;
      // imports là mảng (nhật ký file đã gộp) — giữ lại, các khóa khác vẫn chỉ nhận object.
      if (k === "imports") {
        if (Array.isArray(raw[k])) s[k] = raw[k];
        return;
      }
      if (isObj(raw[k])) s[k] = raw[k];
    });
    return s;
  }

  function clone(x) {
    return JSON.parse(JSON.stringify(x));
  }

  function bump(dayMap, date, correct) {
    var d = dayMap[date] || { n: 0, c: 0 };
    dayMap[date] = { n: d.n + 1, c: d.c + (correct ? 1 : 0) };
  }

  function trimDays(dayMap) {
    var keys = Object.keys(dayMap).sort();
    while (keys.length > HISTORY_DAYS) delete dayMap[keys.shift()];
  }

  /* Ghi một câu trả lời cho một kỹ năng. itemId (tùy chọn) dùng để theo dõi từng câu hỏi.
   * Trả về trạng thái mới; không sửa trạng thái cũ. */
  function applyAnswer(state, skill, correct, date, itemId) {
    var s = clone(migrate(state));
    date = date || today();
    var sk = s.skills[skill] || { ema: null, n: 0, last: null, days: {} };
    var x = correct ? 1 : 0;
    sk.ema = sk.ema === null || sk.ema === undefined ? x : Math.round((ALPHA * x + (1 - ALPHA) * sk.ema) * 1000) / 1000;
    sk.n += 1;
    sk.last = date;
    sk.days = sk.days || {};
    bump(sk.days, date, correct);
    trimDays(sk.days);
    s.skills[skill] = sk;
    bump(s.days, date, correct);
    trimDays(s.days);
    if (itemId) {
      var it = s.items[itemId] || { n: 0, c: 0, last: null };
      s.items[itemId] = { n: it.n + 1, c: it.c + (correct ? 1 : 0), last: date };
    }
    return s;
  }

  function applyQuiz(state, quizId, score, total, date) {
    var s = clone(migrate(state));
    date = date || today();
    var q = s.quizzes[quizId] || { best: 0, total: total, tries: 0, last: null };
    s.quizzes[quizId] = {
      best: Math.max(q.best, score),
      total: total,
      tries: q.tries + 1,
      last: date,
    };
    return s;
  }

  function markRead(state, path, date) {
    var s = clone(migrate(state));
    if (!s.read[path]) s.read[path] = date || today();
    return s;
  }

  var JOURNAL_MAX = 2000;
  var JOURNAL_DAYS = 365; // giữ tối đa 365 ngày gần nhất (tránh đầy localStorage)

  /* Ghi một mục nhật ký vào ngày cho trước. text được trim và cắt ở 2000 ký tự.
   * Tự trim journal về JOURNAL_DAYS ngày gần nhất. Trả về trạng thái mới. */
  function addJournalEntry(state, date, time, text) {
    var s = clone(migrate(state));
    var d = String(date == null ? "" : date);
    var entry = {
      t: String(time == null ? "" : time),
      text: String(text == null ? "" : text)
        .trim()
        .slice(0, JOURNAL_MAX),
    };
    var arr = Array.isArray(s.journal[d]) ? s.journal[d] : [];
    s.journal[d] = arr.concat([entry]);
    var keys = Object.keys(s.journal).sort();
    while (keys.length > JOURNAL_DAYS) delete s.journal[keys.shift()];
    return s;
  }

  /* Số ngày liên tiếp có hoạt động, tính lùi từ hôm nay (hoặc hôm qua nếu hôm nay chưa học). */
  function streak(state, date) {
    var s = migrate(state);
    var active = {};
    Object.keys(s.days).forEach(function (k) {
      active[k] = true;
    });
    Object.keys(s.read).forEach(function (k) {
      active[s.read[k]] = true;
    });
    Object.keys(s.journal).forEach(function (k) {
      active[k] = true;
    });
    var d = date ? new Date(date + "T12:00:00") : new Date();
    if (!active[today(d)]) d.setDate(d.getDate() - 1);
    var n = 0;
    while (active[today(d)]) {
      n++;
      d.setDate(d.getDate() - 1);
    }
    return n;
  }

  /* ---- Lớp localStorage (bọc try/catch: chế độ riêng tư có thể chặn) ---- */
  var memory = null;

  function load() {
    if (memory) return memory;
    var raw = null;
    try {
      raw = JSON.parse(window.localStorage.getItem(KEY));
    } catch (e) {
      raw = null;
    }
    memory = migrate(raw);
    return memory;
  }

  function save(state) {
    memory = migrate(state);
    try {
      window.localStorage.setItem(KEY, JSON.stringify(memory));
      return true;
    } catch (e) {
      return false;
    }
  }

  function update(fn) {
    return save(fn(load()));
  }

  function clear() {
    memory = emptyState();
    try {
      window.localStorage.removeItem(KEY);
    } catch (e) {}
  }

  return {
    KEY: KEY,
    VERSION: VERSION,
    today: today,
    emptyState: emptyState,
    migrate: migrate,
    applyAnswer: applyAnswer,
    applyQuiz: applyQuiz,
    markRead: markRead,
    addJournalEntry: addJournalEntry,
    streak: streak,
    load: load,
    save: save,
    update: update,
    clear: clear,
    record: function (skill, correct, itemId) {
      return update(function (s) {
        return applyAnswer(s, skill, correct, today(), itemId);
      });
    },
    _reset: function () {
      memory = null;
    },
  };
});
