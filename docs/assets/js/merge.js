/* Logos Zero — gộp bản sao lưu dữ liệu (merge-restore).
 * Mọi hàm đều thuần (không đụng localStorage/DOM), xuất qua module.exports để kiểm thử.
 * Mô hình dữ liệu: state của progress.js là các bộ đếm tổng hợp (aggregate),
 * nên gộp theo NGỮ NGHĨA từng mục (xem quy tắc trong mergeStates), không phải
 * gộp bản ghi có timestamp. */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.OZ = root.OZ || {};
    root.OZ.merge = api;
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  function isObj(x) {
    return x !== null && typeof x === "object" && !Array.isArray(x);
  }

  function clone(x) {
    return JSON.parse(JSON.stringify(x));
  }

  function uuid() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
      var r = Math.floor(Math.random() * 16);
      var v = c === "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  /* Id máy: sinh một lần, lưu ở localStorage. Ngoài trình duyệt trả về dự phòng. */
  function deviceId() {
    try {
      if (typeof window === "undefined" || !window.localStorage) return "unknown-device";
      var KEY = "lz:device-id";
      var id = window.localStorage.getItem(KEY);
      if (!id) {
        id = uuid();
        window.localStorage.setItem(KEY, id);
      }
      return id;
    } catch (e) {
      return "unknown-device";
    }
  }

  /* Ngày YYYY-MM-DD so sánh chuỗi là đúng thứ tự thời gian. */
  function maxDate(a, b) {
    if (!a) return b || null;
    if (!b) return a || null;
    return a >= b ? a : b;
  }

  function minDate(a, b) {
    if (!a) return b || null;
    if (!b) return a || null;
    return a <= b ? a : b;
  }

  /* {k: {n, c[, last]}} — cộng dồn n, c; last (nếu có) lấy lớn nhất. */
  function sumCounters(a, b) {
    var out = {};
    function add(src) {
      Object.keys(src || {}).forEach(function (k) {
        var e = src[k] || {};
        var cur = out[k] || { n: 0, c: 0 };
        var merged = { n: cur.n + (e.n || 0), c: cur.c + (e.c || 0) };
        if (e.last !== undefined || cur.last !== undefined) merged.last = maxDate(cur.last, e.last);
        out[k] = merged;
      });
    }
    add(a);
    add(b);
    return out;
  }

  function mergeSkills(a, b) {
    var out = {};
    var keys = {};
    Object.keys(a || {}).forEach(function (k) { keys[k] = true; });
    Object.keys(b || {}).forEach(function (k) { keys[k] = true; });
    Object.keys(keys).forEach(function (k) {
      var x = (a || {})[k], y = (b || {})[k];
      if (!x) { out[k] = clone(y); return; }
      if (!y) { out[k] = clone(x); return; }
      var nx = x.n || 0, ny = y.n || 0, n = nx + ny;
      var ex = x.ema === null || x.ema === undefined ? null : x.ema;
      var ey = y.ema === null || y.ema === undefined ? null : y.ema;
      var ema = null;
      if (n > 0) {
        if (ex === null && ey === null) ema = null;
        else if (ex === null) ema = ey;
        else if (ey === null) ema = ex;
        else ema = Math.round(((ex * nx + ey * ny) / n) * 1000) / 1000;
      }
      out[k] = { ema: ema, n: n, last: maxDate(x.last, y.last), days: sumCounters(x.days, y.days) };
    });
    return out;
  }

  function mergeQuizzes(a, b) {
    var out = {};
    var keys = {};
    Object.keys(a || {}).forEach(function (k) { keys[k] = true; });
    Object.keys(b || {}).forEach(function (k) { keys[k] = true; });
    Object.keys(keys).forEach(function (k) {
      var x = (a || {})[k], y = (b || {})[k];
      if (!x) { out[k] = clone(y); return; }
      if (!y) { out[k] = clone(x); return; }
      // total khác nhau: giữ bản có last mới hơn; bằng nhau → total lớn hơn.
      var pick = x;
      if ((y.total || 0) !== (x.total || 0)) {
        var ly = y.last || "", lx = x.last || "";
        if (ly > lx) pick = y;
        else if (ly === lx && (y.total || 0) > (x.total || 0)) pick = y;
      }
      out[k] = {
        best: Math.max(x.best || 0, y.best || 0),
        total: pick.total,
        tries: (x.tries || 0) + (y.tries || 0),
        last: maxDate(x.last, y.last),
      };
    });
    return out;
  }

  /* Hợp nhất bài đã đọc: giữ ngày đọc SỚM nhất. */
  function mergeRead(a, b) {
    var out = {};
    Object.keys(a || {}).forEach(function (k) { out[k] = a[k]; });
    Object.keys(b || {}).forEach(function (k) {
      out[k] = out[k] ? minDate(out[k], b[k]) : b[k];
    });
    return out;
  }

  /* Thẻ nào "thắng": last mới hơn → box lớn hơn → so JSON (deterministic). */
  function betterCard(x, y) {
    var lx = x.last || "", ly = y.last || "";
    if (lx !== ly) return lx > ly;
    if ((x.box || 0) !== (y.box || 0)) return (x.box || 0) > (y.box || 0);
    return JSON.stringify(x) >= JSON.stringify(y);
  }

  function mergeCards(a, b) {
    var out = {};
    var keys = {};
    Object.keys(a || {}).forEach(function (k) { keys[k] = true; });
    Object.keys(b || {}).forEach(function (k) { keys[k] = true; });
    Object.keys(keys).forEach(function (k) {
      var x = (a || {})[k], y = (b || {})[k];
      if (!x) { out[k] = clone(y); return; }
      if (!y) { out[k] = clone(x); return; }
      out[k] = clone(betterCard(x, y) ? x : y);
    });
    return out;
  }

  /* Journal: hợp nhất theo entry. Mỗi entry {t, text}; identity = t + "\n" + text.
   * Cùng khóa ngày ở 2 máy → union + dedupe (không mất entry nào), sắp xếp theo giờ. */
  function journalKey(e) {
    return (e && e.t ? e.t : "") + "\n" + (e && e.text ? e.text : "");
  }

  function mergeJournal(a, b) {
    var out = {};
    function addAll(src) {
      Object.keys(src || {}).forEach(function (k) {
        var list = Array.isArray(src[k]) ? src[k] : [];
        var seen = {};
        (out[k] || []).forEach(function (e) { seen[journalKey(e)] = true; });
        var merged = (out[k] || []).slice();
        list.forEach(function (e) {
          var key = journalKey(e);
          if (!seen[key]) { seen[key] = true; merged.push(clone(e)); }
        });
        merged.sort(function (x, y) {
          return (x.t || "") < (y.t || "") ? -1 : (x.t || "") > (y.t || "") ? 1 : 0;
        });
        out[k] = merged;
      });
    }
    addAll(a);
    addAll(b);
    return out;
  }

  function alreadyImported(local, meta) {
    if (!meta || !meta.deviceId || !meta.exportedAt) return false;
    var log = (local && local.imports) || [];
    return log.some(function (m) {
      return m.deviceId === meta.deviceId && m.exportedAt === meta.exportedAt;
    });
  }

  /* Gộp hai state. meta = { deviceId, exportedAt } của file được nhập;
   * nhập lại cùng file → trả về local nguyên vẹn (không nhân đôi). */
  function mergeStates(local, imported, meta) {
    var L = clone(local || {});
    var I = clone(imported || {});
    if (alreadyImported(L, meta)) return L;
    var imports = Array.isArray(L.imports) ? L.imports.slice() : [];
    if (meta && meta.deviceId && meta.exportedAt) {
      imports.push({ deviceId: meta.deviceId, exportedAt: meta.exportedAt });
    }
    return {
      v: Math.max(L.v || 1, I.v || 1),
      skills: mergeSkills(L.skills, I.skills),
      days: sumCounters(L.days, I.days),
      quizzes: mergeQuizzes(L.quizzes, I.quizzes),
      read: mergeRead(L.read, I.read),
      cards: mergeCards(L.cards, I.cards),
      items: sumCounters(L.items, I.items),
      journal: mergeJournal(L.journal, I.journal),
      imports: imports,
    };
  }

  /* Kiểm tra file sao lưu do người dùng chọn. */
  function validateBackup(data) {
    if (!isObj(data)) return { ok: false, error: "File không phải là JSON object." };
    // Nhận cả bản sao lưu xuất từ logos-zero, để người đọc mang tiến độ sang site mới.
    if (data.app !== "logos" && data.app !== "logos-zero") return { ok: false, error: "Đây không phải bản sao lưu của Logos Zero." };
    if (!isObj(data.state)) return { ok: false, error: "Bản sao lưu thiếu trường state." };
    return {
      ok: true,
      meta: { deviceId: data.deviceId || null, exportedAt: data.exported || null },
      state: data.state,
    };
  }

  /* Tóm tắt thay đổi để hiện preview trước khi gộp. */
  function previewMerge(local, imported, meta) {
    var L = clone(local || {});
    var I = imported || {};
    var done = alreadyImported(L, meta);
    var merged = done ? L : mergeStates(L, I, meta);
    var summary = [];
    function countBoth(a, b) {
      var aKeys = Object.keys(a || {}), bKeys = Object.keys(b || {});
      var inA = {};
      aKeys.forEach(function (k) { inA[k] = true; });
      var added = 0, updated = 0;
      bKeys.forEach(function (k) { if (inA[k]) updated++; else added++; });
      return { added: added, updated: updated };
    }
    function row(section, c) {
      if (c.added || c.updated) summary.push({ section: section, added: c.added, updated: c.updated });
    }
    row("Kỹ năng", countBoth(L.skills, I.skills));
    row("Ngày luyện tập", countBoth(L.days, I.days));
    row("Bài quiz", countBoth(L.quizzes, I.quizzes));
    row("Bài đã đọc", countBoth(L.read, I.read));
    row("Thẻ ghi nhớ", countBoth(L.cards, I.cards));
    row("Câu hỏi đã làm", countBoth(L.items, I.items));
    row("Nhật ký", countBoth(L.journal, I.journal));

    var conflicts = [];
    Object.keys(I.quizzes || {}).forEach(function (k) {
      var x = (L.quizzes || {})[k];
      if (x && (x.total || 0) !== ((I.quizzes[k] || {}).total || 0)) {
        conflicts.push(
          "Quiz '" + k + "': tổng số câu khác nhau (" + x.total + " và " + I.quizzes[k].total + ") — giữ bản mới hơn."
        );
      }
    });
    Object.keys(I.cards || {}).forEach(function (k) {
      var x = (L.cards || {})[k], y = I.cards[k];
      if (x && JSON.stringify(x) !== JSON.stringify(y)) {
        conflicts.push(
          "Thẻ '" + k + "': hai bên khác nhau — giữ bản ôn gần nhất (" + (betterCard(x, y) ? "trên máy này" : "trong file") + ")."
        );
      }
    });

    return {
      alreadyImported: done,
      summary: summary,
      conflicts: conflicts,
      emaNote: "Độ chính xác theo kỹ năng (EMA) được gộp xấp xỉ theo số câu đã làm mỗi bên.",
      merged: merged,
    };
  }

  return {
    deviceId: deviceId,
    mergeStates: mergeStates,
    validateBackup: validateBackup,
    previewMerge: previewMerge,
    alreadyImported: alreadyImported,
    // xuất thêm để kiểm thử:
    _mergeSkills: mergeSkills,
    _mergeQuizzes: mergeQuizzes,
    _mergeCards: mergeCards,
    _mergeJournal: mergeJournal,
    _sumCounters: sumCounters,
  };
});
