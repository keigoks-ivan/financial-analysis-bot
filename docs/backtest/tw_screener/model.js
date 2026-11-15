/* 台股選股回測器：介面設定與引擎設定的轉換。純函式，不碰 DOM，瀏覽器與 Node 共用。
   介面用自然單位（ROE 10 ＝ 10%、市值 100 ＝ 100 億元），這裡換算成 engine.js 的單位；網址 hash 的編碼與解碼也在這裡。
   engine.js 不動：計算口徑、因子定義、預設組合都在 engine.js。 */
(function (root) {
  'use strict';
  var TW = root.TWS || (typeof require !== 'undefined' ? require('./engine.js') : null);
  var FACTORS = TW.FACTORS, FIDX = TW.FIDX, PRE = TW.PRESETS;

  /* ---------------- 分類（「＋加條件」選單） ---------------- */
  var CATS = [
    ['價值', ['pb', 'pe', 'dy']],
    ['獲利與體質', ['roe', 'debt']],
    ['成長', ['yoy1', 'yoy3']],
    ['動能', ['m20', 'm60', 'm120', 'm12_1', 'm120_20', 'dist52', 'ma200']],
    ['風險', ['vol60', 'vol120']],
    ['籌碼', ['trust']],
    ['規模與流動性', ['mcap', 'amt60']]
  ];
  // 介面上的名稱（沒列的用 engine.js 的 name）；th：加門檻時的起始方向與數值（介面單位）
  var NAME = { ma200: '站上 200 日線（距 200 日均線）', yoy3: '近 3 個月營收年增', yoy1: '月營收年增（最近 1 個月）' };
  var TH = {
    roe: ['>', 0], yoy1: ['>', 0], yoy3: ['>', 0], m20: ['>', 0], m60: ['>', 0], m120: ['>', 0], m12_1: ['>', 0], m120_20: ['>', 0],
    dist52: ['>', -20], ma200: ['>', 0], vol60: ['<', 3], vol120: ['<', 3], pb: ['<', 3], pe: ['<', 20], dy: ['>', 3], trust: ['>', 0],
    debt: ['<', 60], mcap: ['>', 100], amt60: ['>', 1]
  };

  function clean(x) { return +(+x).toPrecision(12); }
  // 介面單位 → 引擎單位；mul < 1 的（市值、成交額，引擎用元）乘上 1/mul，其餘（百分比）除以 mul
  function toRaw(f, ui) { var m = f.mul; return clean(m < 1 ? ui * Math.round(1 / m) : ui / m); }
  function fromRaw(f, raw) { var m = f.mul; return clean(m < 1 ? raw / Math.round(1 / m) : raw * m); }
  function nameOf(k) { return NAME[k] || FIDX[k].name; }

  /* ---------------- 介面設定 U ---------------- */
  function defU() {
    return { conds: [], n: 20, freq: 'M', liq: 50, market: 'all', mrank: 0, mmin: 0, basis: 'pool', missing: 'drop', wp: 0, keep: 0,
      timing: 'me', fee: 0.1425, tax: 0.3, start: '2014-01-02', end: '', draws: 200 };
  }
  function copyU(U) { return JSON.parse(JSON.stringify(U)); }
  function findC(U, k) { for (var i = 0; i < U.conds.length; i++) if (U.conds[i].k === k) return U.conds[i]; return null; }

  function num(x, d) { x = parseFloat(x); return isFinite(x) ? x : d; }

  // 介面設定 → 引擎設定。conds 一律照 FACTORS 的順序放（分數相加的順序固定，結果不隨加條件的先後改變）。
  function toSettings(U) {
    var S = { conds: {} };
    S.liq = Math.min(100, Math.max(1, num(U.liq, 50) || 50));
    S.mcapRank = Math.max(0, num(U.mrank, 0) || 0);
    S.mcapMin = Math.max(0, num(U.mmin, 0) || 0);
    S.market = U.market; S.pctBasis = U.basis; S.missing = U.missing;
    S.n = Math.max(1, Math.round(num(U.n, 20) || 20)); S.wtPow = +U.wp; S.keep = Math.max(0, Math.round(num(U.keep, 0) || 0));
    S.freq = U.freq; S.timing = U.timing;
    S.fee = clean(Math.max(0, num(U.fee, 0)) / 100); S.tax = clean(Math.max(0, num(U.tax, 0)) / 100);
    S.start = U.start || '2014-01-02'; S.end = U.end || null;
    FACTORS.forEach(function (f) {
      var u = findC(U, f.k); if (!u) return;
      var c = {};
      if (u.filter) { var v = parseFloat(u.filter.val); if (isFinite(v)) c.filter = { op: u.filter.op, val: toRaw(f, v) }; }
      if (u.rank) c.rank = { dir: u.rank.dir, w: Math.max(0, parseFloat(u.rank.w) || 0) };
      if (c.filter || c.rank) S.conds[f.k] = c;
    });
    return S;
  }

  // 引擎設定（例如 PRESETS 的 s）→ 介面設定
  function fromSettings(S, start) {
    var U = defU(), k;
    ['n', 'freq', 'liq', 'market', 'keep', 'timing', 'missing'].forEach(function (a) { if (S[a] != null) U[a] = S[a]; });
    if (S.mcapRank != null) U.mrank = S.mcapRank;
    if (S.mcapMin != null) U.mmin = S.mcapMin;
    if (S.pctBasis != null) U.basis = S.pctBasis;
    if (S.wtPow != null) U.wp = S.wtPow;
    if (S.fee != null) U.fee = clean(S.fee * 100);
    if (S.tax != null) U.tax = clean(S.tax * 100);
    U.start = start || S.start || U.start; U.end = S.end || '';
    for (k in (S.conds || {})) {
      var f = FIDX[k], c = S.conds[k], u = { k: k, filter: null, rank: null };
      if (c.filter) u.filter = { op: c.filter.op, val: fromRaw(f, c.filter.val) };
      if (c.rank) u.rank = { dir: c.rank.dir, w: c.rank.w };
      U.conds.push(u);
    }
    return U;
  }

  /* ---------------- 起點按鈕 ---------------- */
  var PRESET_BTNS = [['comp', 'FinLab 四因子'], ['val', '價值＋品質＋股息'], ['chips', '籌碼'], ['mom', '動能輪動'], ['zero', '從零開始']];
  var PRESET_NOTE = {
    comp: '成交額前 50% 的股票，用 ROE、120 日漲幅、120 日波動（低的好、權重 2）、月營收年增四項，跟全市場比排名後加權，取前 25 檔，分數越高分越多（三次方），每月 15 日左右決定並買。',
    val: '成交額前 50% 的股票，先留下股價淨值比大於 0 而且 120 日漲幅大於 0 的，再用股價淨值比（低的好）、ROE、殖利率三項排名，取前 20 檔，照分數比例分配，每季換股（3、6、9、12 月底）。缺資料的那一項給 0 分。',
    chips: '成交額前 50%、全市場市值前 600 名、投信買超強度大於 0 的股票，用投信買超強度與 60 日漲幅兩項排名，取前 15 檔，照分數比例分配，每月月底決定、隔天買。上櫃的投信資料 2014-12 才有，所以從 2015-02 起算。',
    mom: '全市場市值前 200 名、ROE 大於 0、月營收年增大於 0 的股票，用 60 日漲幅、120 日漲幅扣最近 20 日、60 日波動（低的好）、ROE 四項排名，取前 20 檔，分數的平方比例分配，每月月底決定、15 日左右才買。',
    zero: '全部條件清空。請至少加一項排名條件，否則名單只是池子裡的隨便幾檔。'
  };
  function presetU(k) {
    if (k === 'zero') return defU();
    var P = PRE[k];
    return fromSettings(P.s, P.start < '2014-01-02' ? '2014-01-02' : P.start);
  }
  // 兩組設定的「選股與時點」是否相同（不比成本、訖日、隨機次數）
  function canon(U) { var S = toSettings(U); delete S.fee; delete S.tax; delete S.end; return JSON.stringify(S); }
  var PC = null;
  function whichPreset(U) {
    if (!PC) { PC = {}; PRESET_BTNS.forEach(function (b) { PC[b[0]] = canon(presetU(b[0])); }); }
    var c = canon(U);
    for (var i = 0; i < PRESET_BTNS.length; i++) if (PC[PRESET_BTNS[i][0]] === c) return PRESET_BTNS[i][0];
    return null;
  }

  /* ---------------- 網址 hash ---------------- */
  var MK = { all: 'a', TWSE: 's', TPEX: 'o' }, MKR = { a: 'all', s: 'TWSE', o: 'TPEX' };
  var BS = { pool: 'p', all: 'a' }, BSR = { p: 'pool', a: 'all' };
  var MS = { drop: 'd', zero: 'z' }, MSR = { d: 'drop', z: 'zero' };
  var TM = { me: 'm', off14: 'o', off14frozen: 'f' }, TMR = { m: 'me', o: 'off14', f: 'off14frozen' };
  function ns(x) { return String(clean(x)); }
  function encode(U) {
    var D = defU(), o = [];
    o.push('c=' + U.conds.map(function (u) {
      var s = u.k + ':';
      if (u.rank) s += (u.rank.dir === 'hi' ? 'H' : 'L') + ns(isFinite(u.rank.w) ? Math.max(0, u.rank.w) : 0);
      if (u.filter && isFinite(u.filter.val)) s += (u.filter.op === '>' ? 'g' : 'l') + ns(u.filter.val);
      return s;
    }).filter(function (s) { return !/:$/.test(s); }).join(','));
    function add(code, v, d, f) { if (String(v) !== String(d)) o.push(code + '=' + (f ? f(v) : v)); }
    add('n', U.n, D.n); add('f', U.freq, D.freq); add('l', U.liq, D.liq); add('mk', U.market, D.market, function (v) { return MK[v]; });
    add('mr', U.mrank, D.mrank); add('mm', U.mmin, D.mmin); add('b', U.basis, D.basis, function (v) { return BS[v]; });
    add('ms', U.missing, D.missing, function (v) { return MS[v]; }); add('w', U.wp, D.wp); add('k', U.keep, D.keep);
    add('t', U.timing, D.timing, function (v) { return TM[v]; }); add('s', U.start, D.start); add('e', U.end, D.end);
    add('fe', U.fee, D.fee); add('tx', U.tax, D.tax); add('d', U.draws, D.draws);
    return o.join('&');
  }
  var DATE = /^\d{4}-\d{2}-\d{2}$/;
  // 解不出來回 null；有 c= 這個欄位才算「帶設定的網址」
  function decode(str) {
    str = String(str || '').replace(/^#/, '');
    if (str.indexOf('c=') !== 0 && str.indexOf('&c=') < 0) return null;
    var P = {}, U = defU();
    str.split('&').forEach(function (kv) { var i = kv.indexOf('='); if (i > 0) P[kv.slice(0, i)] = kv.slice(i + 1); });
    var seen = {};
    (P.c || '').split(',').forEach(function (tok) {
      var m = /^([a-z0-9_]+):(?:([HL])(\d+(?:\.\d+)?(?:e[+-]?\d+)?))?(?:([gl])(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?))?$/.exec(tok);
      if (!m || !FIDX[m[1]] || seen[m[1]] || (!m[2] && !m[4])) return;
      seen[m[1]] = 1;
      U.conds.push({ k: m[1], filter: m[4] ? { op: m[4] === 'g' ? '>' : '<', val: +m[5] } : null, rank: m[2] ? { dir: m[2] === 'H' ? 'hi' : 'lo', w: +m[3] } : null });
    });
    function pick(code, map, key) { if (P[code] != null && map[P[code]]) U[key] = map[P[code]]; }
    function numeric(code, key, lo, hi, int) { if (P[code] != null) { var v = parseFloat(P[code]); if (isFinite(v)) { v = Math.min(hi, Math.max(lo, v)); U[key] = int ? Math.round(v) : v; } } }
    numeric('n', 'n', 1, 100, true); numeric('l', 'liq', 1, 100); numeric('mr', 'mrank', 0, 5000, true); numeric('mm', 'mmin', 0, 1e6);
    numeric('w', 'wp', 0, 3, true); numeric('k', 'keep', 0, 500, true); numeric('fe', 'fee', 0, 5); numeric('tx', 'tax', 0, 5); numeric('d', 'draws', 200, 1000, true);
    if (P.f === 'M' || P.f === 'Q') U.freq = P.f;
    pick('mk', MKR, 'market'); pick('b', BSR, 'basis'); pick('ms', MSR, 'missing'); pick('t', TMR, 'timing');
    if (P.s && DATE.test(P.s)) U.start = P.s;
    if (P.e && DATE.test(P.e)) U.end = P.e;
    if ([200, 500, 1000].indexOf(U.draws) < 0) U.draws = 200;
    return U;
  }

  /* ---------------- 一句話描述目前設定 ---------------- */
  function describe(U) {
    var S = toSettings(U), rk = [], ft = [];
    FACTORS.forEach(function (f) { var c = S.conds[f.k]; if (c && c.rank) rk.push(f.k); if (c && c.filter) ft.push(f.k); });
    var pool = (S.market === 'all' ? '上市與上櫃' : S.market === 'TWSE' ? '上市' : '上櫃') + '股票裡，' + (S.liq < 100 ? '60 日均成交額前 ' + S.liq + '%' : '成交額不設限');
    if (S.mcapRank > 0) pool += '、全市場市值前 ' + S.mcapRank + ' 名';
    if (S.mcapMin > 0) pool += '、市值至少 ' + S.mcapMin + ' 億';
    if (ft.length) pool += '、另有 ' + ft.length + ' 項門檻';
    var pick = rk.length ? '依 ' + rk.length + ' 項排名取前 ' + S.n + ' 檔' : '還沒有排名條件';
    var wt = ['每檔一樣多', '照分數比例分配', '分數的平方比例分配', '分數的三次方比例分配'][S.wtPow];
    var when = { me: '月底決定、隔天買', off14: '15 日左右決定並買', off14frozen: '月底決定、15 日左右才買' }[S.timing];
    return pool + '。' + pick + '，' + wt + '，' + (S.freq === 'M' ? '每月' : '每季') + (S.timing === 'off14' ? ' ' : '') + when + '。';
  }

  var api = { CATS: CATS, TH: TH, nameOf: nameOf, toRaw: toRaw, fromRaw: fromRaw, clean: clean, defU: defU, copyU: copyU, findC: findC, toSettings: toSettings, fromSettings: fromSettings,
    PRESET_BTNS: PRESET_BTNS, PRESET_NOTE: PRESET_NOTE, presetU: presetU, whichPreset: whichPreset, canon: canon, encode: encode, decode: decode, describe: describe };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.TWSUI = api;
})(typeof self !== 'undefined' ? self : this);
