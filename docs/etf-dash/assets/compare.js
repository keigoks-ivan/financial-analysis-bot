/* 兩檔配法比較器（etf-dash 與 active-etf 共用）。
 * 資料：compare_series.json（兩支 build_compare_data.py 產生）。全部在瀏覽器端計算，含息。
 * 頁面用 window.COMPARE_CONFIG 指定資料檔、預設兩檔、視窗清單。
 * 核心函式（parseData、resolveWindow、comboSeries、metrics…）不碰 DOM，Node 可直接 require 測試。
 * 算法與 2026-10-28 深度檢驗一致：
 *   幾何超額 (1+r)/(1+b)-1；年化用 252 個交易日；週報酬用週五收盤（沒有週五 bar 的週併入下一週）；
 *   上下捕捉用日曆月（首尾月不完整也算）；不再平衡＝兩條指數依權重加總；
 *   每月／每季再平衡＝在該期最後一個交易日收盤回到權重。
 */
(function (root) {
  'use strict';

  /* ───────── 日期工具 ───────── */
  function dow(iso) { return new Date(iso + 'T00:00:00Z').getUTCDay(); }
  function shiftDate(iso, years, months) {
    var d = new Date(iso + 'T00:00:00Z');
    if (years) d.setUTCFullYear(d.getUTCFullYear() - years);
    if (months) d.setUTCMonth(d.getUTCMonth() - months);
    return d.toISOString().slice(0, 10);
  }
  // 最後一個 <= iso 的位置，沒有回 -1
  function lastIdxLE(dates, iso) {
    var lo = 0, hi = dates.length - 1, ans = -1;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1;
      if (dates[mid] <= iso) { ans = mid; lo = mid + 1; } else { hi = mid - 1; }
    }
    return ans;
  }

  /* ───────── 資料 ───────── */
  function parseData(raw) {
    var n = raw.dates.length, scale = raw.scale || 1, funds = {};
    Object.keys(raw.funds).forEach(function (k) {
      var f = raw.funds[k], v = new Float64Array(n);
      v.fill(NaN);
      for (var j = 0; j < f.q.length; j++) v[f.i0 + j] = f.q[j] / scale;
      funds[k] = {
        key: k, label: f.label || k, ticker: f.ticker, currency: f.currency, start: f.start,
        first: f.i0, lastReal: f.last_real, totalReturn: f.total_return !== false, v: v
      };
    });
    return {
      dates: raw.dates, n: n, funds: funds, bench: raw.benchmark, episodes: raw.episodes || [],
      overlap: raw.overlap || {}, overlapAsOf: raw.overlap_as_of, notes: raw.notes || [],
      asOf: raw.as_of, currency: raw.currency, generatedAt: raw.generated_at
    };
  }

  /* 視窗：spec = {kind:'years'|'months', n} | {kind:'all'} | {kind:'custom', from, to}
   * 起點＝要求起日當天或之前最後一個交易日（與深度檢驗相同）；兩檔（加基準）共同起日較晚時縮到共同起日。 */
  function resolveWindow(data, spec, keys) {
    var dates = data.dates, end = data.n - 1, req;
    if (spec.kind === 'custom') {
      if (spec.to) end = Math.max(0, lastIdxLE(dates, spec.to));
      req = spec.from || dates[0];
    } else if (spec.kind === 'years') { req = shiftDate(dates[end], spec.n, 0); }
    else if (spec.kind === 'months') { req = shiftDate(dates[end], 0, spec.n); }
    else { req = dates[0]; }
    var common = 0, limiting = [];
    keys.forEach(function (k) { common = Math.max(common, data.funds[k].first); });
    keys.forEach(function (k) { if (data.funds[k].first === common && common > 0 && limiting.indexOf(k) < 0) limiting.push(k); });
    var base = lastIdxLE(dates, req);
    var shrunk = spec.kind !== 'all' && base < common;
    var i0 = spec.kind === 'all' ? common : (shrunk ? common : base);
    return {
      i0: i0, i1: end, shrunk: shrunk, reqStart: req, commonStart: dates[common],
      limiting: limiting, valid: end - i0 >= 20, kind: spec.kind
    };
  }

  function isPeriodEnd(d0, d1, reb) {
    var m0 = d0.slice(0, 7), m1 = d1.slice(0, 7);
    if (m0 === m1) return false;
    if (reb === 'M') return true;
    var m = d0.slice(5, 7);
    return m === '03' || m === '06' || m === '09' || m === '12';
  }

  /* 配法指數：視窗起日＝1。reb：'none'｜'M'｜'Q'。wa 是 A 的權重（0～1）。 */
  function comboSeries(a, b, wa, reb, dates, i0, i1) {
    var n = i1 - i0 + 1, V = new Float64Array(n), wb = 1 - wa;
    var ua = wa / a[i0], ub = wb / b[i0];
    V[0] = 1;
    for (var t = 1; t < n; t++) {
      var i = i0 + t;
      V[t] = ua * a[i] + ub * b[i];
      if (reb !== 'none' && t < n - 1 && isPeriodEnd(dates[i], dates[i + 1], reb)) {
        ua = V[t] * wa / a[i]; ub = V[t] * wb / b[i];
      }
    }
    return V;
  }

  function slice(v, i0, i1) {
    var out = new Float64Array(i1 - i0 + 1);
    for (var i = i0; i <= i1; i++) out[i - i0] = v[i] / v[i0];
    return out;
  }

  /* ───────── 統計 ───────── */
  function pctRets(v) {
    var r = new Float64Array(v.length - 1);
    for (var i = 1; i < v.length; i++) r[i - 1] = v[i] / v[i - 1] - 1;
    return r;
  }
  function mean(x) { var s = 0; for (var i = 0; i < x.length; i++) s += x[i]; return s / x.length; }
  function cov(x, y) {
    var mx = mean(x), my = mean(y), s = 0;
    for (var i = 0; i < x.length; i++) s += (x[i] - mx) * (y[i] - my);
    return s / (x.length - 1);
  }
  function std(x) { return Math.sqrt(cov(x, x)); }
  function corr(x, y) {
    if (x.length < 3) return NaN;
    var sx = std(x), sy = std(y);
    if (!(sx > 1e-12) || !(sy > 1e-12)) return NaN;
    return cov(x, y) / (sx * sy);
  }
  function sub(x, y) { var o = new Float64Array(x.length); for (var i = 0; i < x.length; i++) o[i] = x[i] - y[i]; return o; }

  // 視窗內的週五收盤位置（含起點與終點）
  function weeklyIdx(dates) {
    var n = dates.length, idx = [0];
    for (var i = 1; i < n - 1; i++) if (dow(dates[i]) === 5) idx.push(i);
    if (idx[idx.length - 1] !== n - 1) idx.push(n - 1);
    return idx;
  }
  function weeklyRets(v, idx) {
    var o = new Float64Array(idx.length - 1);
    for (var k = 1; k < idx.length; k++) o[k - 1] = v[idx[k]] / v[idx[k - 1]] - 1;
    return o;
  }
  function monthlyRets(v, dates) {
    var keys = [], vals = [], cur = null, acc = 1;
    for (var i = 1; i < v.length; i++) {
      var m = dates[i].slice(0, 7);
      if (m !== cur) { if (cur !== null) { keys.push(cur); vals.push(acc - 1); } cur = m; acc = 1; }
      acc *= v[i] / v[i - 1];
    }
    if (cur !== null) { keys.push(cur); vals.push(acc - 1); }
    return vals;
  }
  function capture(fm, bm) {
    var su = 0, bu = 0, sd = 0, bd = 0, nu = 0, nd = 0;
    for (var i = 0; i < bm.length; i++) {
      if (bm[i] > 0) { su += fm[i]; bu += bm[i]; nu++; } else { sd += fm[i]; bd += bm[i]; nd++; }
    }
    return { up: nu && bu ? su / bu : NaN, down: nd && bd ? sd / bd : NaN, nUp: nu, nDown: nd };
  }
  function maxDrawdown(v) {
    var pk = 0, best = 0, bp = 0, bt = 0;
    for (var i = 1; i < v.length; i++) {
      if (v[i] > v[pk]) pk = i;
      var dd = v[i] / v[pk] - 1;
      if (dd < best) { best = dd; bp = pk; bt = i; }
    }
    var rec = -1;
    if (best < 0) for (var j = bt + 1; j < v.length; j++) if (v[j] >= v[bp]) { rec = j; break; }
    return { dd: best, peak: bp, trough: bt, recovery: rec };
  }

  /* 一條序列（視窗起點＝1）的整組指標。b 是基準同視窗序列，dates 是視窗日期。 */
  function metrics(v, b, dates, isBench) {
    var n = v.length, r = pctRets(v), rb = pctRets(b), act = sub(r, rb);
    var cum = v[n - 1] / v[0] - 1, cumB = b[n - 1] / b[0] - 1;
    var wi = weeklyIdx(dates), w = weeklyRets(v, wi), wb = weeklyRets(b, wi);
    var te = std(act) * Math.sqrt(252);
    var cap = capture(monthlyRets(v, dates), monthlyRets(b, dates));
    var dd = maxDrawdown(v);
    return {
      cum: cum,
      excess: isBench ? NaN : (1 + cum) / (1 + cumB) - 1,
      vol: std(r) * Math.sqrt(252),
      betaD: isBench ? 1 : cov(r, rb) / cov(rb, rb),
      betaW: isBench ? 1 : cov(w, wb) / cov(wb, wb),
      te: isBench ? NaN : te,
      ir: isBench || !(te > 1e-9) ? NaN : mean(act) * 252 / te,
      mdd: dd.dd, mddPeak: dd.peak, mddTrough: dd.trough, mddRecovery: dd.recovery,
      up: isBench ? NaN : cap.up, down: isBench ? NaN : cap.down, nUp: cap.nUp, nDown: cap.nDown
    };
  }

  /* 兩檔的相關：主動報酬（扣基準）與原始報酬，日與週 */
  function correlations(a, b, bench, dates) {
    var ra = pctRets(a), rb = pctRets(b), rm = pctRets(bench);
    var wi = weeklyIdx(dates);
    var wa = weeklyRets(a, wi), wbb = weeklyRets(b, wi), wm = weeklyRets(bench, wi);
    return {
      activeD: corr(sub(ra, rm), sub(rb, rm)), activeW: corr(sub(wa, wm), sub(wbb, wm)),
      rawD: corr(ra, rb), rawW: corr(wa, wbb), nDays: ra.length, nWeeks: wa.length
    };
  }

  function overlapOf(data, ka, kb) {
    if (ka === kb) return null;
    var v = data.overlap[ka + '|' + kb];
    if (v === undefined) v = data.overlap[kb + '|' + ka];
    return v === undefined ? null : v;
  }

  /* 基準回檔 ≥10% 的區段（峰日在視窗內者）：每條序列的跌幅與谷後反彈 */
  function episodeRows(data, win, series) {
    var dates = data.dates, rows = [];
    data.episodes.forEach(function (e) {
      var ip = lastIdxLE(dates, e.peak), it = lastIdxLE(dates, e.trough);
      if (ip < win.i0 || it > win.i1) return;
      var ir = e.recovery ? lastIdxLE(dates, e.recovery) : -1;
      var recovered = ir >= 0 && ir <= win.i1;
      var ie = recovered ? ir : win.i1;
      var row = { peak: e.peak, trough: e.trough, recovery: recovered ? e.recovery : null, vals: {} };
      Object.keys(series).forEach(function (k) {
        var s = series[k]; // s 以視窗起點為 0
        var p = s[ip - win.i0], t = s[it - win.i0], x = s[ie - win.i0];
        row.vals[k] = { dd: t / p - 1, rebound: x / t - 1 };
      });
      rows.push(row);
    });
    return rows;
  }

  /* 逐年：年初用上一年最後一個交易日（視窗起點之前沒有就用起點），年末用該年最後一個交易日 */
  function yearlyRows(dates, series, benchKey) {
    var n = dates.length, years = [], lastOf = {};
    for (var i = 0; i < n; i++) { var y = dates[i].slice(0, 4); if (lastOf[y] === undefined) years.push(y); lastOf[y] = i; }
    var rows = [];
    years.forEach(function (y, yi) {
      var startIdx = yi === 0 ? 0 : lastOf[years[yi - 1]];
      var endIdx = lastOf[y];
      if (endIdx <= startIdx) return;
      var partialStart = yi === 0 && dates[0].slice(5) !== '12-31' && !(dates[0] > y + '-12-24');
      var partialEnd = yi === years.length - 1 && dates[endIdx] < y + '-12-24';
      var vals = {};
      Object.keys(series).forEach(function (k) {
        vals[k] = series[k][endIdx] / series[k][startIdx] - 1;
      });
      rows.push({ year: y, vals: vals, partial: partialStart || partialEnd, from: dates[startIdx], to: dates[endIdx] });
    });
    return rows;
  }

  /* 整組計算：回傳畫面要的全部數字 */
  function compute(data, st) {
    var ka = st.a, kb = st.b, bk = data.bench;
    var keys = [ka, kb, bk];
    var win = resolveWindow(data, st.win, keys);
    if (!win.valid) return { win: win, error: '視窗內交易日不足 20 天，請放寬起訖。' };
    var dates = data.dates.slice(win.i0, win.i1 + 1);
    var A = slice(data.funds[ka].v, win.i0, win.i1);
    var B = slice(data.funds[kb].v, win.i0, win.i1);
    var M = slice(data.funds[bk].v, win.i0, win.i1);
    var wa = st.wa;
    var C = comboSeries(data.funds[ka].v, data.funds[kb].v, wa, st.reb, data.dates, win.i0, win.i1);
    var out = { win: win, dates: dates, A: A, B: B, C: C, M: M, st: st };
    out.mA = metrics(A, M, dates, ka === bk);
    out.mB = metrics(B, M, dates, kb === bk);
    out.mC = metrics(C, M, dates, false);
    out.mM = metrics(M, M, dates, true);
    out.corr = correlations(A, B, M, dates);
    out.overlap = overlapOf(data, ka, kb);
    // 回檔區段、逐年：序列以視窗起點為 0（episodeRows 用絕對位置換算）
    out.episodes = episodeRows(data, win, { A: A, B: B, C: C, M: M });
    out.yearly = yearlyRows(dates, { A: A, B: B, C: C, M: M });
    return out;
  }

  /* ───────── 文字 ───────── */
  function fmtNum(x, d) {
    if (x === null || x === undefined || !isFinite(x)) return '—';
    var s = Math.abs(x).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
    var zero = Number(s.replace(/,/g, '')) === 0;
    return (x < 0 && !zero ? '−' : '') + s;
  }
  function fmtPct(x, d, sign) {
    if (x === null || x === undefined || !isFinite(x)) return '—';
    var v = x * 100, s = fmtNum(v, d === undefined ? 1 : d);
    if (sign && v > 0 && s !== '0.0' && s.charAt(0) !== '−') s = '+' + s;
    return s + '%';
  }
  function cmpWord(x, y, hi, lo, eq) {
    if (Math.abs(x - y) < 0.0005) return eq;
    return x > y ? hi : lo;
  }
  function shortName(key) { return key.replace('_', ' '); }

  function winLabel(cfg, st, c) {
    if (c.win.shrunk) return '共同起日 ' + c.dates[0] + ' 起';
    if (st.winId === 'custom') return '自訂（' + c.dates[0] + '～' + c.dates[c.dates.length - 1] + '）';
    if (c.win.kind === 'all') return '全期（' + c.dates[0] + ' 起）';
    var w = (cfg.windows || []).filter(function (x) { return x.id === st.winId; })[0];
    return w ? w.label.replace(/（.*$/, '') : '';
  }

  function summaryText(data, cfg, c) {
    var st = c.st, ka = st.a, kb = st.b, bk = data.bench;
    var A = shortName(ka), B = shortName(kb), BK = shortName(bk);
    var wa = Math.round(st.wa * 1000) / 10, wb = Math.round((1 - st.wa) * 1000) / 10;
    var mix = ka === kb ? A + ' 重複選了兩次' : (wa === 50 ? A + ' 與 ' + B + ' 各半' : A + ' ' + wa + '%、' + B + ' ' + wb + '%');
    var reb = { none: '不再平衡', M: '每月再平衡', Q: '每季再平衡' }[st.reb];
    var win = winLabel(cfg, st, c);
    var s1 = win + ' ' + mix + '（' + reb + '）累計 ' + fmtPct(c.mC.cum, 1);
    var cl = [];
    if (ka !== kb || true) {
      cl.push(cmpWord(c.mC.cum, c.mA.cum, '高於', '低於', '約等於') + ' ' + A + ' 單檔（' + fmtPct(c.mA.cum, 1) + '）');
      if (kb !== ka) cl.push(cmpWord(c.mC.cum, c.mB.cum, '高於', '低於', '約等於') + ' ' + B + ' 單檔（' + fmtPct(c.mB.cum, 1) + '）');
      if (ka !== bk && kb !== bk) cl.push(cmpWord(c.mC.cum, c.mM.cum, '高於', '低於', '約等於') + '基準 ' + BK + '（' + fmtPct(c.mM.cum, 1) + '）');
    }
    s1 += '，' + cl.join('，') + '。';
    var s2 = '最大回檔 ' + fmtPct(c.mC.mdd, 1) + '（' + c.dates[c.mC.mddPeak] + ' 至 ' + c.dates[c.mC.mddTrough] + '），' +
      cmpWord(c.mC.mdd, c.mA.mdd, '淺於', '深於', '約等於') + ' ' + A + ' 單檔（' + fmtPct(c.mA.mdd, 1) + '）';
    if (kb !== ka) s2 += '，' + cmpWord(c.mC.mdd, c.mB.mdd, '淺於', '深於', '約等於') + ' ' + B + ' 單檔（' + fmtPct(c.mB.mdd, 1) + '）';
    s2 += '。對基準的幾何超額 ' + fmtPct(c.mC.excess, 1, true) + '，追蹤誤差 ' + fmtPct(c.mC.te, 1) + '。';
    var s3 = '';
    if (ka !== kb && isFinite(c.corr.activeW)) {
      s3 = A + ' 與 ' + B + ' 的主動報酬相關，週 ' + fmtNum(c.corr.activeW, 2) + '，日 ' + fmtNum(c.corr.activeD, 2) + '。';
    }
    return [s1, s2, s3].filter(Boolean);
  }

  var core = {
    dow: dow, shiftDate: shiftDate, lastIdxLE: lastIdxLE, parseData: parseData, resolveWindow: resolveWindow,
    comboSeries: comboSeries, slice: slice, pctRets: pctRets, weeklyIdx: weeklyIdx, weeklyRets: weeklyRets,
    monthlyRets: monthlyRets, capture: capture, maxDrawdown: maxDrawdown, metrics: metrics,
    correlations: correlations, overlapOf: overlapOf, episodeRows: episodeRows, yearlyRows: yearlyRows,
    compute: compute, fmtNum: fmtNum, fmtPct: fmtPct, summaryText: summaryText, mean: mean, std: std, corr: corr
  };

  /* ───────── 圖：inline SVG ───────── */
  var COLORS = { A: '#173564', B: '#b8924a', C: '#1f7a5a', M: '#7a8190' };

  function niceTicks(lo, hi, want) {
    var raw = (hi - lo) / want, mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), nrm = raw / mag;
    var step = (nrm < 1.5 ? 1 : nrm < 3.5 ? 2 : nrm < 7.5 ? 5 : 10) * mag, out = [];
    for (var v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(v);
    return out;
  }
  function logTicks(lo, hi) {
    var out = [], p = Math.floor(Math.log(lo) / Math.LN10) - 1;
    for (; p <= Math.ceil(Math.log(hi) / Math.LN10); p++) [1, 2, 5].forEach(function (m) {
      var v = m * Math.pow(10, p); if (v >= lo && v <= hi) out.push(v);
    });
    return out;
  }
  function timeTicks(dates) {
    var t0 = Date.parse(dates[0]), t1 = Date.parse(dates[dates.length - 1]);
    var months = (t1 - t0) / (30.4375 * 86400000), step = 1;
    [1, 3, 6, 12, 24, 60].some(function (s) { step = s; return months / s <= 8; });
    var d = new Date(t0), out = [];
    d = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 1));
    if (step >= 12) d = new Date(Date.UTC(d.getUTCFullYear() + (d.getUTCMonth() === 0 ? 0 : 1), 0, 1));
    while (d.getTime() <= t1) {
      var m = d.getUTCMonth() + 1;
      if (step < 12 ? ((m - 1) % step === 0) : ((d.getUTCFullYear()) % (step / 12) === 0)) {
        out.push({ t: d.getTime(), label: step >= 12 ? String(d.getUTCFullYear()) : d.getUTCFullYear() + '-' + (m < 10 ? '0' : '') + m });
      }
      d = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + (step >= 12 ? 12 : 1), 1));
    }
    return out;
  }

  function chartSvg(dates, lines, log) {
    var W = 880, H = 360, ml = 54, mr = 14, mt = 12, mb = 26, pw = W - ml - mr, ph = H - mt - mb;
    var t = dates.map(function (d) { return Date.parse(d); }), t0 = t[0], t1 = t[t.length - 1];
    var lo = Infinity, hi = -Infinity;
    lines.forEach(function (l) { for (var i = 0; i < l.v.length; i++) { var x = l.v[i] * 100; if (x < lo) lo = x; if (x > hi) hi = x; } });
    var f, ticks;
    if (log) {
      var L0 = Math.log(lo * 0.97), L1 = Math.log(hi * 1.03);
      f = function (v) { return mt + (L1 - Math.log(v)) / (L1 - L0) * ph; };
      ticks = logTicks(Math.exp(L0), Math.exp(L1));
    } else {
      var pad = (hi - lo) * 0.05; lo = lo - pad; hi = hi + pad;
      f = function (v) { return mt + (hi - v) / (hi - lo) * ph; };
      ticks = niceTicks(lo, hi, 5);
    }
    var X = function (tm) { return ml + (tm - t0) / (t1 - t0) * pw; };
    var out = ['<svg class="cmp-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="累計報酬走勢圖" preserveAspectRatio="xMidYMid meet">'];
    ticks.forEach(function (v) {
      var y = f(v).toFixed(1);
      out.push('<line x1="' + ml + '" x2="' + (W - mr) + '" y1="' + y + '" y2="' + y + '" class="cmp-grid"/>');
      out.push('<text x="' + (ml - 6) + '" y="' + (+y + 3.5) + '" class="cmp-axis" text-anchor="end">' + fmtNum(v, v < 10 ? 1 : 0) + '</text>');
    });
    timeTicks(dates).forEach(function (tk) {
      var x = X(tk.t).toFixed(1);
      out.push('<line x1="' + x + '" x2="' + x + '" y1="' + (H - mb) + '" y2="' + (H - mb + 4) + '" class="cmp-grid"/>');
      out.push('<text x="' + x + '" y="' + (H - 8) + '" class="cmp-axis" text-anchor="middle">' + tk.label + '</text>');
    });
    var stride = Math.max(1, Math.floor(t.length / 1400));
    lines.forEach(function (l) {
      var d = [];
      for (var i = 0; i < t.length; i += stride) d.push((d.length ? 'L' : 'M') + X(t[i]).toFixed(1) + ' ' + f(l.v[i] * 100).toFixed(1));
      if ((t.length - 1) % stride !== 0) d.push('L' + X(t1).toFixed(1) + ' ' + f(l.v[t.length - 1] * 100).toFixed(1));
      out.push('<path d="' + d.join('') + '" fill="none" stroke="' + l.color + '" stroke-width="' + (l.w || 1.6) + '"' +
        (l.dash ? ' stroke-dasharray="' + l.dash + '"' : '') + ' stroke-linejoin="round"/>');
    });
    out.push('<line id="cmpCross" x1="0" x2="0" y1="' + mt + '" y2="' + (H - mb) + '" class="cmp-cross" visibility="hidden"/>');
    out.push('</svg>');
    return { svg: out.join(''), geom: { W: W, ml: ml, pw: pw, t: t, t0: t0, t1: t1 } };
  }

  /* ───────── 畫面 ───────── */
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function sgn(x) { return x > 0 ? 'pos' : x < 0 ? 'neg' : ''; }
  function td(txt, cls) { return '<td class="num' + (cls ? ' ' + cls : '') + '">' + txt + '</td>'; }

  function renderAll(data, cfg, c, els) {
    var st = c.st, bk = data.bench;
    var nameA = shortName(st.a), nameB = shortName(st.b), nameBK = shortName(bk);
    var comboName = st.a === st.b ? '配法' : '配法 ' + Math.round(st.wa * 100) + '／' + Math.round((1 - st.wa) * 100);
    var cols = [['A', nameA, c.mA], ['B', nameB, c.mB], ['C', comboName, c.mC], ['M', '基準 ' + nameBK, c.mM]];

    // 視窗說明
    var wl = [];
    wl.push('比較期間 ' + c.dates[0] + ' 至 ' + c.dates[c.dates.length - 1] + '（' + (c.dates.length - 1) + ' 個交易日）。');
    if (c.win.shrunk) {
      wl.push('原視窗起日 ' + c.win.reqStart + '，' + c.win.limiting.map(shortName).join('、') + ' 的資料較晚開始，視窗縮到共同起日 ' + c.win.commonStart + '。');
    } else if (c.win.kind === 'all') {
      wl.push('全期＝A、B 與基準的共同起日 ' + c.win.commonStart + ' 起。');
    }
    var stale = [st.a, st.b, bk].filter(function (k, i, arr) { return arr.indexOf(k) === i; }).filter(function (k) {
      var lr = data.funds[k].lastReal; return lr && lr < data.dates[c.win.i1] && (Date.parse(data.dates[c.win.i1]) - Date.parse(lr)) / 86400000 > 3;
    });
    if (stale.length) wl.push(stale.map(function (k) { return shortName(k) + ' 最後一筆資料是 ' + data.funds[k].lastReal + '，之後以持平處理'; }).join('；') + '。');
    els.winNote.innerHTML = wl.map(function (x) { return '<div>' + esc(x) + '</div>'; }).join('');

    // 摘要
    els.summary.innerHTML = summaryText(data, cfg, c).map(function (x) { return '<p>' + esc(x) + '</p>'; }).join('');

    // 圖
    var lines = [{ v: c.A, color: COLORS.A, name: nameA }, { v: c.B, color: COLORS.B, name: nameB },
      { v: c.C, color: COLORS.C, name: comboName, w: 2.4 }, { v: c.M, color: COLORS.M, name: '基準 ' + nameBK, dash: '5 4', w: 1.4 }];
    var ch = chartSvg(c.dates, lines, !!st.log);
    els.chart.innerHTML = ch.svg;
    els.legend.innerHTML = lines.map(function (l) {
      return '<span class="cmp-lg"><i style="background:' + l.color + '"></i>' + esc(l.name) + ' <b class="num">' + fmtNum(l.v[l.v.length - 1] * 100, 0) + '</b></span>';
    }).join('');
    els.tip.textContent = '起點 ＝ 100，滑過圖面可看當日數值。';
    attachHover(els, ch.geom, c.dates, lines);

    // 指標表
    var rows = [
      ['累計報酬', function (m) { return fmtPct(m.cum, 1); }, function (m) { return sgn(m.cum); }],
      ['對基準幾何超額', function (m) { return fmtPct(m.excess, 1, true); }, function (m) { return sgn(m.excess); }],
      ['年化波動', function (m) { return fmtPct(m.vol, 1); }],
      ['對基準 beta（日）', function (m) { return fmtNum(m.betaD, 2); }],
      ['對基準 beta（週）', function (m) { return fmtNum(m.betaW, 2); }],
      ['追蹤誤差（年化）', function (m) { return fmtPct(m.te, 1); }],
      ['資訊比率', function (m) { return fmtNum(m.ir, 2); }],
      ['最大回檔', function (m) { return fmtPct(m.mdd, 1); }, function () { return 'neg'; }],
      ['最大回檔區間', function (m) {
        if (!(m.mdd < 0)) return '—';
        var rec = m.mddRecovery >= 0 ? '，' + c.dates[m.mddRecovery] + ' 回前高' : '，未回前高';
        return c.dates[m.mddPeak] + ' → ' + c.dates[m.mddTrough] + rec;
      }, null, true],
      ['上漲月捕捉', function (m) { return fmtPct(m.up, 0); }],
      ['下跌月捕捉', function (m) { return fmtPct(m.down, 0); }]
    ];
    var h = '<table class="t"><thead><tr><th>指標</th>' + cols.map(function (x) { return '<th class="num">' + esc(x[1]) + '</th>'; }).join('') + '</tr></thead><tbody>';
    rows.forEach(function (r) {
      h += '<tr><td>' + r[0] + '</td>' + cols.map(function (x) {
        var m = x[2];
        return r[3] ? '<td class="num small">' + r[1](m) + '</td>' : td(r[1](m), r[2] ? r[2](m) : '');
      }).join('') + '</tr>';
    });
    h += '</tbody></table>';
    els.metrics.innerHTML = h;
    var nUp = c.mM.nUp, nDn = c.mM.nDown;
    var tz = (cfg.tzFunds || []).filter(function (k) { return k === st.a || k === st.b; });
    els.metricsNote.innerHTML = '上下月捕捉用日曆月，視窗首尾月不完整也算；基準上漲 ' + nUp + ' 個月、下跌 ' + nDn + ' 個月' +
      (Math.min(nUp, nDn) < 12 ? '，月數少，數字雜訊大' : '') + '。' +
      (tz.length ? ' ' + tz.map(shortName).join('、') + ' 在亞洲時段收盤，日 beta 被時差壓低，看週 beta。' : '');

    // 相關
    var cr = c.corr, same = st.a === st.b;
    var ov = c.overlap;
    var h3 = '<table class="t"><thead><tr><th>' + esc(nameA) + ' 與 ' + esc(nameB) + '</th><th class="num">日</th><th class="num">週</th></tr></thead><tbody>' +
      '<tr><td>主動報酬相關（各自扣基準）</td>' + td(same ? '—' : fmtNum(cr.activeD, 2)) + td(same ? '—' : fmtNum(cr.activeW, 2)) + '</tr>' +
      '<tr><td>原始報酬相關</td>' + td(same ? '—' : fmtNum(cr.rawD, 2)) + td(same ? '—' : fmtNum(cr.rawW, 2)) + '</tr>' +
      '<tr><td>持股重疊（加權，兩檔相同持股各取較小權重相加）</td>' + td(ov === null ? '—' : fmtNum(ov, 1) + '%') + '<td class="num"></td></tr>' +
      '</tbody></table>';
    els.corr.innerHTML = h3;
    els.corrNote.textContent = '樣本 ' + cr.nDays + ' 個日報酬、' + cr.nWeeks + ' 個週報酬。持股重疊取自 ' + (data.overlapAsOf || '最近一次') + ' 的持股快照' +
      (ov === null ? '，這一組沒有重疊數字（同一檔、指數或沒有持股資料）' : '') + '。主動報酬相關是兩檔各自扣掉基準後的報酬相關，數字越高，兩檔贏輸基準的時間越一致，分散效果越小。';

    // 回檔區段
    if (!c.episodes.length) {
      els.episodes.innerHTML = '<p class="muted">視窗內基準沒有 10% 以上的回檔區段。</p>';
    } else {
      var h4 = '<table class="t"><thead><tr><th>峰日</th><th>谷日</th><th>回前高日</th><th class="num">' + esc(nameA) + ' 跌</th><th class="num">' + esc(nameB) + ' 跌</th><th class="num">配法跌</th><th class="num">基準跌</th>' +
        '<th class="num">' + esc(nameA) + ' 反彈</th><th class="num">' + esc(nameB) + ' 反彈</th><th class="num">配法反彈</th><th class="num">基準反彈</th></tr></thead><tbody>';
      c.episodes.forEach(function (e) {
        var v = e.vals;
        h4 += '<tr><td>' + e.peak + '</td><td>' + e.trough + '</td><td>' + (e.recovery || '未回前高') + '</td>' +
          td(fmtPct(v.A.dd, 1), 'neg') + td(fmtPct(v.B.dd, 1), 'neg') + td(fmtPct(v.C.dd, 1), 'neg') + td(fmtPct(v.M.dd, 1), 'neg') +
          td(fmtPct(v.A.rebound, 1, true)) + td(fmtPct(v.B.rebound, 1, true)) + td(fmtPct(v.C.rebound, 1, true)) + td(fmtPct(v.M.rebound, 1, true)) + '</tr>';
      });
      h4 += '</tbody></table>';
      els.episodes.innerHTML = h4;
    }
    els.episodesNote.textContent = '區段以基準（' + nameBK + '）從前高回檔 10% 以上定義，跌幅是峰日到谷日，反彈是谷日到回前高日（未回前高則到視窗最後一日）；只列峰日在視窗內的區段。';

    // 逐年
    var h5 = '<table class="t"><thead><tr><th>年度</th><th class="num">' + esc(nameA) + ' 超額</th><th class="num">' + esc(nameB) + ' 超額</th><th class="num">配法超額</th><th class="num">基準報酬</th></tr></thead><tbody>';
    var anyPartial = false;
    c.yearly.forEach(function (r) {
      var v = r.vals, ex = function (k) { return (1 + v[k]) / (1 + v.M) - 1; };
      if (r.partial) anyPartial = true;
      h5 += '<tr><td>' + r.year + (r.partial ? '*' : '') + '</td>' +
        td(fmtPct(ex('A'), 1, true), sgn(ex('A'))) + td(fmtPct(ex('B'), 1, true), sgn(ex('B'))) + td(fmtPct(ex('C'), 1, true), sgn(ex('C'))) + td(fmtPct(v.M, 1)) + '</tr>';
    });
    h5 += '</tbody></table>';
    els.yearly.innerHTML = h5;
    els.yearlyNote.textContent = '超額是幾何超額 (1+報酬)/(1+基準報酬)−1。' + (anyPartial ? '* 為不足完整年度（視窗起日或資料最後一日在年度中間）。' : '');
  }

  function attachHover(els, g, dates, lines) {
    var svg = els.chart;
    if (!svg.addEventListener) return;
    var cross = els.chart.querySelector ? els.chart.querySelector('#cmpCross') : null;
    var onMove = function (ev) {
      var rect = svg.getBoundingClientRect(), cx = (ev.clientX !== undefined ? ev.clientX : (ev.touches && ev.touches[0].clientX));
      if (!rect.width || cx === undefined) return;
      var x = (cx - rect.left) / rect.width * g.W;
      var tm = g.t0 + (x - g.ml) / g.pw * (g.t1 - g.t0);
      if (tm < g.t0 || tm > g.t1) return;
      var lo = 0, hi = g.t.length - 1;
      while (lo < hi) { var mid = (lo + hi) >> 1; if (g.t[mid] < tm) lo = mid + 1; else hi = mid; }
      var i = lo;
      if (cross) { var px = g.ml + (g.t[i] - g.t0) / (g.t1 - g.t0) * g.pw; cross.setAttribute('x1', px); cross.setAttribute('x2', px); cross.setAttribute('visibility', 'visible'); }
      els.tip.textContent = dates[i] + '　' + lines.map(function (l) { return l.name + ' ' + fmtNum(l.v[i] * 100, 1); }).join('　');
    };
    svg.onpointermove = onMove;
    svg.onpointerdown = onMove;
  }

  /* ───────── 啟動 ───────── */
  function init() {
    var cfg = root.COMPARE_CONFIG;
    var $ = function (id) { return document.getElementById(id); };
    var els = {
      status: $('cmpStatus'), winNote: $('cmpWinNote'), summary: $('cmpSummary'), chart: $('cmpChart'), legend: $('cmpLegend'),
      tip: $('cmpTip'), metrics: $('cmpMetrics'), metricsNote: $('cmpMetricsNote'), corr: $('cmpCorr'), corrNote: $('cmpCorrNote'),
      episodes: $('cmpEpisodes'), episodesNote: $('cmpEpisodesNote'), yearly: $('cmpYearly'), yearlyNote: $('cmpYearlyNote'),
      selA: $('cmpA'), selB: $('cmpB'), num: $('cmpW'), range: $('cmpWR'), wbLabel: $('cmpWB'), selWin: $('cmpWin'),
      custom: $('cmpCustom'), from: $('cmpFrom'), to: $('cmpTo'), selReb: $('cmpReb'), log: $('cmpLog'), notes: $('cmpDataNotes'),
      asof: $('cmpAsOf')
    };
    var data = null, state = null;

    function readQuery() {
      var q = {};
      try { (location.search || '').replace(/^\?/, '').split('&').forEach(function (p) { if (!p) return; var kv = p.split('='); q[decodeURIComponent(kv[0])] = decodeURIComponent(kv[1] || ''); }); } catch (e) { /* 忽略 */ }
      return q;
    }
    function winSpec(id) {
      if (id === 'custom') return { kind: 'custom', from: els.from.value || null, to: els.to.value || null };
      var w = cfg.windows.filter(function (x) { return x.id === id; })[0] || cfg.windows[0];
      return w.kind === 'all' ? { kind: 'all' } : { kind: w.kind, n: w.n };
    }
    function pull() {
      var wa = parseFloat(els.num.value);
      if (!isFinite(wa)) wa = 50;
      wa = Math.max(0, Math.min(100, wa));
      var winId = els.selWin.value;
      return { a: els.selA.value, b: els.selB.value, wa: wa / 100, reb: els.selReb.value, winId: winId, win: winSpec(winId), log: !!els.log.checked };
    }
    function pushQuery(s) {
      try {
        var q = 'a=' + encodeURIComponent(s.a) + '&b=' + encodeURIComponent(s.b) + '&w=' + Math.round(s.wa * 100) + '&win=' + s.winId + '&reb=' + s.reb +
          (s.winId === 'custom' ? '&from=' + (els.from.value || '') + '&to=' + (els.to.value || '') : '') + (s.log ? '&log=1' : '');
        history.replaceState(null, '', '?' + q);
      } catch (e) { /* 預覽或封閉環境不給改網址，略過 */ }
    }
    function update() {
      var s = pull();
      els.wbLabel.textContent = 'B 檔 ' + (Math.round((1 - s.wa) * 1000) / 10) + '%';
      els.range.value = Math.round(s.wa * 100);
      els.custom.hidden = s.winId !== 'custom';
      var c;
      try { c = compute(data, s); } catch (e) { els.status.textContent = '計算失敗：' + e.message; return; }
      if (c.error) {
        els.status.textContent = c.error;
        els.status.hidden = false;
        return;
      }
      els.status.hidden = true;
      renderAll(data, cfg, c, els);
      pushQuery(s);
    }

    function fill() {
      var keys = Object.keys(data.funds).sort();
      var opt = function (k) {
        var f = data.funds[k], tag = (k === data.bench ? '（基準）' : '') + (f.totalReturn ? '' : '（指數，不含息，對照用）');
        return '<option value="' + k + '">' + esc(f.label) + tag + '</option>';
      };
      var html = keys.map(opt).join('');
      els.selA.innerHTML = html; els.selB.innerHTML = html;
      els.selWin.innerHTML = cfg.windows.map(function (w) { return '<option value="' + w.id + '">' + esc(w.label) + '</option>'; }).join('') + '<option value="custom">自訂起訖</option>';
      var q = readQuery();
      var pick = function (v, d) { return v && data.funds[v] ? v : d; };
      els.selA.value = pick(q.a, cfg.defaultA);
      els.selB.value = pick(q.b, cfg.defaultB);
      var w = parseFloat(q.w); if (isFinite(w) && w >= 0 && w <= 100) { els.num.value = w; }
      if (q.reb && ['none', 'M', 'Q'].indexOf(q.reb) >= 0) els.selReb.value = q.reb;
      var wid = q.win && (q.win === 'custom' || cfg.windows.some(function (x) { return x.id === q.win; })) ? q.win : cfg.defaultWindow;
      els.selWin.value = wid;
      els.from.min = els.to.min = data.dates[0]; els.from.max = els.to.max = data.dates[data.n - 1];
      els.from.value = q.from || data.dates[Math.max(0, lastIdxLE(data.dates, shiftDate(data.dates[data.n - 1], 3, 0)))];
      els.to.value = q.to || data.dates[data.n - 1];
      if (q.log === '1') els.log.checked = true;
      if (els.asof) els.asof.textContent = data.asOf;
      els.notes.innerHTML = data.notes.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
    }

    function bind() {
      [els.selA, els.selB, els.selWin, els.selReb, els.log, els.from, els.to].forEach(function (e) { e.addEventListener('change', update); });
      els.num.addEventListener('input', function () { els.range.value = els.num.value; update(); });
      els.range.addEventListener('input', function () { els.num.value = els.range.value; update(); });
    }

    els.status.textContent = '資料載入中…';
    fetch(cfg.dataUrl, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (raw) {
      data = parseData(raw);
      fill(); bind(); update();
    }).catch(function (e) {
      els.status.hidden = false;
      els.status.textContent = '資料載入失敗：' + e.message;
    });
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = core;
    core.init = init;
    core.chartSvg = chartSvg;
    core.renderAll = renderAll;
  } else {
    root.CompareCore = core;
    if (root.document && root.COMPARE_CONFIG) {
      if (root.document.readyState === 'loading') root.document.addEventListener('DOMContentLoaded', init);
      else init();
    }
  }
})(typeof window !== 'undefined' ? window : globalThis);
