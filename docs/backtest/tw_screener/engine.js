/* 台股互動選股回測器：純 JS 引擎（瀏覽器 Worker 與 Node 共用）。
   口徑沿用 v7-backtest src/finlab_repro 的 pt_core／ss_core：成交日收盤成交、含息日報酬、下市股用最後成交日賣出、
   手續費買賣各一次、賣出證交稅。資料檔由 v7 src/tw_screener/build.py 產生。 */
(function (root) {
  'use strict';

  /* ---------------- 因子清單（白話定義、起始日、是否補的） ---------------- */
  // mul：頁面上顯示值＝原始值×mul；unit：單位；dir：預設排名方向（hi＝高好）；src：stored（快照內存）或 price（由每日報酬算）
  var FACTORS = [
    { k: 'roe', name: '單季 ROE', mul: 100, unit: '%', dir: 'hi', start: '2014-01', supp: true,
      def: '最近一季稅後淨利（含非控制權益）除以該季末權益總額，不年化。財報在法定期限（5/15、8/14、11/14、隔年 3/31）之後才算已公布。' },
    { k: 'yoy1', name: '月營收年增（最近 1 個月）', mul: 100, unit: '%', dir: 'hi', start: '2014-02', supp: true,
      def: '最近一個月營收除以去年同月營收減 1。營收在次月 10 日（遇休市順延）的下一個交易日起算已公布，這個公布日是補的。2013 年以前營收口徑不同，只用 2014 年起。' },
    { k: 'yoy3', name: '近 3 個月營收年增', mul: 100, unit: '%', dir: 'hi', start: '2014-04', supp: true,
      def: '最近三個月營收合計除以去年同期三個月合計減 1，公布日規則同上。' },
    { k: 'm20', name: '20 日漲幅', mul: 100, unit: '%', dir: 'hi', start: '2014-01', supp: false,
      def: '今天的未還原收盤價除以 20 個交易日前的收盤價減 1。除權息日的價格下跌也算在內，這跟 FinLab 原文一樣。' },
    { k: 'm60', name: '60 日漲幅', mul: 100, unit: '%', dir: 'hi', start: '2014-01', supp: false,
      def: '同上，往前 60 個交易日。' },
    { k: 'm120', name: '120 日漲幅', mul: 100, unit: '%', dir: 'hi', start: '2014-01', supp: false,
      def: '同上，往前 120 個交易日。' },
    { k: 'm12_1', name: '12-1 動能', mul: 100, unit: '%', dir: 'hi', start: '2014-01', supp: false,
      def: '12 個月（252 個交易日）前到 1 個月（21 個交易日）前之間的漲幅，扣掉最近一個月，避開短線反轉。' },
    { k: 'm120_20', name: '120 日漲幅扣最近 20 日', mul: 100, unit: '%', dir: 'hi', start: '2014-01', supp: true,
      def: '140 個交易日前到 20 個交易日前之間的漲幅。FinLab 動能輪動用這一項，所以另外列出，不在原本的 15 項內。' },
    { k: 'vol60', name: '60 日波動', mul: 100, unit: '%', dir: 'lo', start: '2014-01', supp: false,
      def: '最近 60 個交易日「日報酬」的標準差（用未還原收盤價），越小代表走勢越平穩。' },
    { k: 'vol120', name: '120 日波動', mul: 100, unit: '%', dir: 'lo', start: '2014-01', supp: false,
      def: '同上，最近 120 個交易日。' },
    { k: 'pb', name: '股價淨值比（PB）', mul: 1, unit: '倍', dir: 'lo', start: '2014-01', supp: true,
      def: '市值除以最近一季歸屬母公司權益（沒有就用總權益）。權益為負的算不出。這是我們自己算的，不是交易所公布的數字。' },
    { k: 'pe', name: '本益比（近四季）', mul: 1, unit: '倍', dir: 'lo', start: '2014-01', supp: true,
      def: '市值除以近四個連續季度的單季稅後淨利合計（含非控制權益）。淨利合計小於等於 0、或不滿四季的算不出，留空。' },
    { k: 'dy', name: '殖利率', mul: 1, unit: '%', dir: 'hi', start: '2014-01', supp: true,
      def: '近 365 天已除息的現金股利合計除以收盤價。上市公司「權息並發」的現金部分是用當年上櫃公司的比例估的，所以有誤差。沒有除息記錄的算 0。' },
    { k: 'trust', name: '投信買超強度（20 日）', mul: 100, unit: '%', dir: 'hi', start: '2015-02', supp: true,
      def: '近 20 日投信買賣超股數合計，除以近 20 日平均成交股數。成交股數用「成交金額除以收盤價」估算。上櫃投信資料 2014-12 才有，所以用到這一項會自動從 2015-02 起算。' },
    { k: 'debt', name: '負債比', mul: 100, unit: '%', dir: 'lo', start: '2014-01', supp: true,
      def: '最近一季負債總額除以資產總額，公布日規則同 ROE。' },
    { k: 'mcap', name: '市值', mul: 1e-8, unit: '億元', dir: 'hi', start: '2014-01', supp: true,
      def: '股數乘未還原收盤價。股數＝普通股股本除以 10 元面額（一律當 10 元）；外幣申報的 KY 公司與少數改面額的公司會算錯。' },
    { k: 'amt60', name: '60 日均成交額', mul: 1e-8, unit: '億元', dir: 'hi', start: '2014-01', supp: true,
      def: '最近 60 個交易日成交金額的平均（交易所公布的成交金額，不是收盤價乘成交股數）。' },
    { k: 'dist52', name: '距 52 週高點', mul: 100, unit: '%', dir: 'hi', start: '2014-01', supp: false,
      def: '收盤價除以近 252 個交易日最高收盤價減 1，永遠是 0 或負數，0 代表正在創高。' },
    { k: 'ma200', name: '站上 200 日線（距 200 日均線）', mul: 100, unit: '%', dir: 'hi', start: '2014-01', supp: false,
      def: '收盤價除以 200 日均線減 1。大於 0 就是站上 200 日線。' }
  ];
  var FIDX = {}; FACTORS.forEach(function (f, i) { f.i = i; FIDX[f.k] = f; });

  /* ---------------- 預設組合（定義照 FinLab_PT_1114／FinLab_SS_1114 登記稿） ---------------- */
  var PRESETS = {
    comp: { name: 'FinLab 四因子複合', note: '流動性前 50%，品質（ROE）、動能（120 日漲幅）、低波動（120 日，權重 2）、營收（月營收年增）四項「全市場」百分位加權平均，取前 25 檔，分數三次方配權，每月、月底加 14 天後成交。',
      start: '2014-02-14', s: {
        liq: 50, mcapRank: 0, mcapMin: 0, market: 'all', n: 25, wtPow: 3, keep: 0, freq: 'M', timing: 'off14', pctBasis: 'all', missing: 'drop',
        conds: { roe: { rank: { dir: 'hi', w: 1 } }, m120: { rank: { dir: 'hi', w: 1 } }, vol120: { rank: { dir: 'lo', w: 2 } }, yoy1: { rank: { dir: 'hi', w: 1 } } } } },
    val: { name: '價值＋品質＋股息', note: '流動性前 50%，PB 大於 0 且 120 日漲幅大於 0；PB（低好）、ROE、殖利率三項「池內」百分位相加，取前 20 檔，分數線性配權，每季（3、6、9、12 月底）換股。',
      start: '2013-09-30', s: {
        liq: 50, mcapRank: 0, mcapMin: 0, market: 'all', n: 20, wtPow: 1, keep: 0, freq: 'Q', timing: 'me', pctBasis: 'pool', missing: 'zero',
        conds: { pb: { filter: { op: '>', val: 0 }, rank: { dir: 'lo', w: 1 } }, m120: { filter: { op: '>', val: 0 } }, roe: { rank: { dir: 'hi', w: 1 } }, dy: { rank: { dir: 'hi', w: 1 } } } } },
    chips: { name: '籌碼（投信買超＋動能）', note: '流動性前 50%、市值全市場前 600、投信買超強度大於 0；投信買超強度與 60 日漲幅兩項「池內」百分位相加，取前 15 檔，分數線性配權，每月月底判斷、次日成交。上櫃投信資料 2014-12 才有，所以從 2015-02 起。',
      start: '2015-01-30', s: {
        liq: 50, mcapRank: 600, mcapMin: 0, market: 'all', n: 15, wtPow: 1, keep: 0, freq: 'M', timing: 'me', pctBasis: 'pool', missing: 'zero',
        conds: { trust: { filter: { op: '>', val: 0 }, rank: { dir: 'hi', w: 1 } }, m60: { rank: { dir: 'hi', w: 1 } } } } },
    mom: { name: '動能輪動', note: '市值前 200、ROE 大於 0、月營收年增大於 0；60 日漲幅、120 日漲幅扣最近 20 日、60 日波動（低好）、ROE 四項「池內」百分位相加，取前 20 檔，分數平方配權，每月。名單凍結在月底，下個月 14 日之後才成交（照 FinLab 腳本字面）。',
      start: '2014-02-27', s: {
        liq: 100, mcapRank: 200, mcapMin: 0, market: 'all', n: 20, wtPow: 2, keep: 0, freq: 'M', timing: 'off14frozen', pctBasis: 'pool', missing: 'zero',
        conds: { roe: { filter: { op: '>', val: 0 }, rank: { dir: 'hi', w: 1 } }, yoy1: { filter: { op: '>', val: 0 } }, m60: { rank: { dir: 'hi', w: 1 } },
          m120_20: { rank: { dir: 'hi', w: 1 } }, vol60: { rank: { dir: 'lo', w: 1 } } } } }
  };

  var DEFAULTS = {
    liq: 50, mcapRank: 0, mcapMin: 0, market: 'all', n: 20, wtPow: 0, keep: 0, freq: 'M', timing: 'me', pctBasis: 'pool', missing: 'drop',
    conds: {}, fee: 0.001425, tax: 0.003, start: '2014-01-02', end: null
  };

  /* ---------------- 二進位解析 ---------------- */
  function readHeader(buf) {
    var dv = new DataView(buf), H = dv.getUint32(0, true);
    var hdr = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 4, H)));
    return { hdr: hdr, off: 4 + H };
  }
  function unplane(buf, off, n) {          // 低位元組 n 個、高位元組 n 個 → Int16Array(n)
    var u = new Uint8Array(buf, off, 2 * n), out = new Int16Array(n);
    for (var i = 0; i < n; i++) out[i] = u[i] | (u[n + i] << 8);
    return out;
  }
  function parseF(buf) {
    var r = readHeader(buf), hdr = r.hdr, off = r.off, tot = 0;
    hdr.snaps.forEach(function (s) { tot += s.n; });
    var ids = unplane(buf, off, tot); off += 2 * tot;
    var vals = {};
    hdr.factors.forEach(function (k) { vals[k] = unplane(buf, off, tot); off += 2 * tot; });
    var out = [], p = 0;
    hdr.snaps.forEach(function (s) {
      var id = new Uint16Array(s.n), o = { d: s.d, n: s.n, ids: id, raw: {} };
      for (var i = 0; i < s.n; i++) id[i] = ids[p + i] & 0xffff;
      hdr.factors.forEach(function (k) { o.raw[k] = vals[k].subarray(p, p + s.n); });
      p += s.n; out.push(o);
    });
    return out;
  }
  function parseR(buf) {
    var r = readHeader(buf), hdr = r.hdr;
    return { hdr: hdr, data: unplane(buf, r.off, hdr.ns * hdr.nd) };
  }

  /* ---------------- 資料倉 ---------------- */
  function Store(meta) {
    var T = meta.dates.length, NS = meta.stocks.length;
    this.meta = meta; this.T = T; this.NS = NS;
    this.R = new Int16Array(NS * T);
    this.excR = new Map(); this.uov = [];
    this.snapByDay = new Map();
    this.cache = new Map();
    this.ymd = meta.dates.map(function (s) { return '20' + s.slice(0, 2) + '-' + s.slice(2, 4) + '-' + s.slice(4, 6); });
    this.dnum = this.ymd.map(function (s) { return Date.UTC(+s.slice(0, 4), +s.slice(5, 7) - 1, +s.slice(8, 10)) / 864e5; });
    this.fdef = {}; meta.factors.forEach(function (f) { this.fdef[f.k] = f; }, this);
    this.rLoaded = 0; this.PL = null; this.priceReady = false;
    this.sellday = meta.stocks.map(function (s) { return s.s; });
    this.v0 = Int32Array.from(meta.stocks.map(function (s) { return s.v0; }));
    this.e = Int32Array.from(meta.stocks.map(function (s) { return s.e; }));
    this.p0 = Float64Array.from(meta.stocks.map(function (s) { return s.p0; }));
    this.market = meta.stocks.map(function (s) { return s.m; });
    this.rYears = {};
  }
  Store.prototype.addF = function (arr) {
    for (var i = 0; i < arr.length; i++) this.snapByDay.set(arr[i].d, arr[i]);
  };
  Store.prototype.addR = function (p) {
    var h = p.hdr, T = this.T, R = this.R, nd = h.nd, d0 = h.d0;
    for (var s = 0; s < h.ns; s++) {
      R.set(p.data.subarray(s * nd, (s + 1) * nd), s * T + d0);
    }
    for (var i = 0; i < h.exc.length; i++) this.excR.set(h.exc[i][1] * T + h.exc[i][0], h.exc[i][2]);
    for (i = 0; i < h.ev.length; i++) this.uov.push(h.ev[i]);
    this.rYears[h.year] = 1;
  };
  // 臺股升降單位：價格 < 10 為 0.01，< 50 為 0.05，< 100 為 0.1，< 500 為 0.5，< 1000 為 1，其餘 5。
  function tickOf(p) { return p < 10 ? 0.01 : p < 50 ? 0.05 : p < 100 ? 0.1 : p < 500 ? 0.5 : p < 1000 ? 1 : 5; }
  Store.prototype.finishReturns = function () {
    // 未還原收盤價 PL[s*T+t]（元）。每天用「前一天價格 × (1+報酬)」推出，再對齊到升降單位；
    // 報酬只存到 0.01%，誤差遠小於半個升降單位，所以每天都能還原成真正的收盤價，誤差不會累積。
    var T = this.T, NS = this.NS, R = this.R, PL = new Float32Array(NS * T);
    var ov = new Map();
    this.uov.forEach(function (x) { ov.set(x[1] * T + x[0], x[2]); });
    for (var s = 0; s < NS; s++) {
      var v0 = this.v0[s], e = this.e[s];
      if (v0 < 0) continue;
      var base = s * T, px = this.p0[s];
      PL[base + v0] = px;
      for (var t = v0 + 1; t <= e; t++) {
        var k = base + t, u = ov.has(k) ? ov.get(k) : R[k];
        if (this.excR.has(k) && !ov.has(k)) u = this.excR.get(k);
        var est = px * (1 + u / 1e4), tk = tickOf(est);
        px = Math.round(Math.round(est / tk) * tk * 100) / 100;
        PL[k] = px;
      }
    }
    this.PL = PL; this.priceReady = true; this.cache = new Map();
  };
  Store.prototype.ret = function (s, t) {
    var k = s * this.T + t;
    if (this.excR.size && this.excR.has(k)) return this.excR.get(k);
    return this.R[k];
  };

  function dec(a, f) {
    var NA = -32768, n = a.length, out = new Float64Array(n), k = f.s, o = f.o, i, x;
    for (i = 0; i < n; i++) {
      x = a[i];
      if (x === NA) { out[i] = NaN; continue; }
      if (f.t === 'slog') out[i] = (x < 0 ? -1 : x > 0 ? 1 : 0) * (Math.exp(Math.abs(x) / k) - 1) * o;
      else if (f.t === 'log') out[i] = Math.exp((x + 32767) / k + o);
      else if (f.t === 'log1p') out[i] = Math.exp((x + 32767) / k) - 1;
      else out[i] = x / k;
    }
    return out;
  }

  /* 某個判斷日（交易日序號 t）全部因子（實值）。回傳 {n, ids, v:{key:Float64Array}} */
  Store.prototype.factors = function (t) {
    if (this.cache.has(t)) return this.cache.get(t);
    var sn = this.snapByDay.get(t);
    if (!sn) return null;
    var n = sn.n, T = this.T, PL = this.PL, ids = sn.ids, st = {}, v = {}, i, j;
    ['roe', 'yoy1', 'yoy3', 'debt', 'amt60', 'trust'].forEach(function (k) { v[k] = dec(sn.raw[k], this.fdef[k]); }, this);
    var sh = dec(sn.raw.sh, this.fdef.sh), eq = dec(sn.raw.eq, this.fdef.eq), ttm = dec(sn.raw.ttm, this.fdef.ttm), dv = dec(sn.raw.div, this.fdef.div);
    var keys = ['m20', 'm60', 'm120', 'm12_1', 'm120_20', 'vol60', 'vol120', 'dist52', 'ma200', 'mcap', 'pb', 'pe', 'dy'];
    keys.forEach(function (k) { v[k] = new Float64Array(n).fill(NaN); });
    var valid = new Uint8Array(n);
    for (i = 0; i < n; i++) {
      var s = ids[i], v0 = this.v0[s], e = this.e[s];
      if (v0 < 0 || t < v0 || t > e) continue;
      valid[i] = 1;
      var b = s * T, pt = PL[b + t];
      if (t - 20 >= v0) v.m20[i] = pt / PL[b + t - 20] - 1;
      if (t - 60 >= v0) v.m60[i] = pt / PL[b + t - 60] - 1;
      if (t - 120 >= v0) v.m120[i] = pt / PL[b + t - 120] - 1;
      if (t - 252 >= v0) v.m12_1[i] = PL[b + t - 21] / PL[b + t - 252] - 1;
      if (t - 140 >= v0) v.m120_20[i] = PL[b + t - 20] / PL[b + t - 140] - 1;
      var w, sum, sq, u, prev, mx, mean;
      if (t - 60 >= v0) {
        sum = 0; sq = 0; prev = PL[b + t - 60];
        for (j = t - 59; j <= t; j++) { u = PL[b + j] / prev - 1; prev = PL[b + j]; sum += u; sq += u * u; }
        v.vol60[i] = Math.sqrt(Math.max(0, (sq - sum * sum / 60) / 59));
      }
      if (t - 120 >= v0) {
        sum = 0; sq = 0; prev = PL[b + t - 120];
        for (j = t - 119; j <= t; j++) { u = PL[b + j] / prev - 1; prev = PL[b + j]; sum += u; sq += u * u; }
        v.vol120[i] = Math.sqrt(Math.max(0, (sq - sum * sum / 120) / 119));
      }
      if (t - 251 >= v0) {
        mx = 0; for (j = t - 251; j <= t; j++) if (PL[b + j] > mx) mx = PL[b + j];
        v.dist52[i] = pt / mx - 1;
      }
      if (t - 199 >= v0) {
        sum = 0; for (j = t - 199; j <= t; j++) sum += PL[b + j];
        v.ma200[i] = pt / (sum / 200) - 1;
      }
      var px = pt;
      var mc = isFinite(sh[i]) ? Math.round(px * sh[i]) : NaN;
      v.mcap[i] = mc;
      if (isFinite(mc) && isFinite(eq[i]) && eq[i] > 0) v.pb[i] = mc / eq[i];
      if (isFinite(mc) && isFinite(ttm[i]) && ttm[i] > 0) v.pe[i] = mc / ttm[i];
      if (isFinite(dv[i])) v.dy[i] = dv[i] / px * 100;
    }
    var o = { n: n, ids: ids, v: v, valid: valid };
    this.cache.set(t, o);
    return o;
  };

  /* ---------------- 百分位與排名 ---------------- */
  // 平均名次（並列取平均），只算 mask 內且有值的；回傳 {rank: Float64Array(NaN 為無), cnt}
  function avgRank(vals, mask, desc) {
    var n = vals.length, idx = [], i;
    for (i = 0; i < n; i++) if ((!mask || mask[i]) && !isNaN(vals[i])) idx.push(i);
    idx.sort(function (a, b) { return desc ? vals[b] - vals[a] : vals[a] - vals[b]; });
    var rk = new Float64Array(n).fill(NaN), m = idx.length, p = 0;
    while (p < m) {
      var q = p;
      while (q + 1 < m && vals[idx[q + 1]] === vals[idx[p]]) q++;
      var r = (p + q) / 2 + 1;
      for (var z = p; z <= q; z++) rk[idx[z]] = r;
      p = q + 1;
    }
    return { rank: rk, cnt: m };
  }

  /* ---------------- 選股 ---------------- */
  function normCond(c) {
    var out = {};
    for (var k in (c || {})) {
      if (!FIDX[k]) continue;
      var x = c[k], o = {};
      if (x.filter && x.filter.op && isFinite(x.filter.val)) o.filter = { op: x.filter.op, val: +x.filter.val };
      if (x.rank && x.rank.w > 0) o.rank = { dir: x.rank.dir || FIDX[k].dir, w: +x.rank.w };
      if (o.filter || o.rank) out[k] = o;
    }
    return out;
  }

  // 回傳 {ids, w, score, mcap, amt60, pool(int 索引陣列), poolN, rankInfo}
  Store.prototype.pick = function (t, S, prevIds) {
    var F = this.factors(t);
    if (!F) return null;
    var n = F.n, v = F.v, i, keep = new Uint8Array(n).fill(1), conds = S.conds;
    // 池子
    if (S.liq < 100) {
      var rl = avgRank(v.amt60, null, false), thr = 1 - S.liq / 100;
      for (i = 0; i < n; i++) if (!(rl.rank[i] / rl.cnt > thr)) keep[i] = 0;
    }
    if (S.mcapRank > 0) {
      var rm = avgRank(v.mcap, null, true);
      for (i = 0; i < n; i++) if (!(rm.rank[i] <= S.mcapRank)) keep[i] = 0;
    }
    if (S.mcapMin > 0) for (i = 0; i < n; i++) if (!(v.mcap[i] >= S.mcapMin * 1e8)) keep[i] = 0;
    if (S.market !== 'all') for (i = 0; i < n; i++) if (this.market[F.ids[i]] !== S.market) keep[i] = 0;
    // 沒有價格（不在市）的一律不進池
    for (i = 0; i < n; i++) if (!F.valid[i]) keep[i] = 0;
    var rankKeys = [], k;
    for (k in conds) {
      var c = conds[k];
      if (c.filter) {
        var op = c.filter.op, th = c.filter.val, arr = v[k], mul = 1;
        for (i = 0; i < n; i++) {
          if (!keep[i]) continue;
          var x = arr[i];
          if (isNaN(x) || !(op === '>' ? x > th : x < th)) keep[i] = 0;
        }
      }
      if (c.rank) rankKeys.push(k);
    }
    // 排名項目缺值
    if (S.missing === 'drop') for (i = 0; i < n; i++) if (keep[i]) for (var q = 0; q < rankKeys.length; q++) if (isNaN(v[rankKeys[q]][i])) { keep[i] = 0; break; }
    var poolN = 0; for (i = 0; i < n; i++) poolN += keep[i];
    // 分數
    var score = new Float64Array(n).fill(NaN), wsum = 0;
    rankKeys.forEach(function (kk) { wsum += conds[kk].rank.w; });
    if (rankKeys.length === 0) {
      for (i = 0; i < n; i++) if (keep[i]) score[i] = 1;
    } else {
      for (i = 0; i < n; i++) if (keep[i]) score[i] = 0;
      rankKeys.forEach(function (kk) {
        var c = conds[kk].rank, mask = S.pctBasis === 'pool' ? keep : null, desc = c.dir === 'hi';
        var ra = avgRank(v[kk], mask, false);
        for (var j = 0; j < n; j++) {
          if (!keep[j]) continue;
          var p = isNaN(ra.rank[j]) ? 0 : (desc ? ra.rank[j] / ra.cnt : (ra.cnt + 1 - ra.rank[j]) / ra.cnt);
          score[j] += c.w * p;
        }
      });
      for (i = 0; i < n; i++) if (keep[i]) score[i] /= wsum;
    }
    // 名次（分數大者在前）
    var rs = avgRank(score, null, true);
    var sel = [];
    var N = S.n;
    if (S.keep > 0 && prevIds && prevIds.length) {
      var prevSet = {}; prevIds.forEach(function (id) { prevSet[id] = 1; });
      for (i = 0; i < n; i++) if (!isNaN(rs.rank[i]) && rs.rank[i] <= S.keep && prevSet[F.ids[i]]) sel.push(i);
      if (sel.length > N) { sel.sort(function (a, b) { return rs.rank[a] - rs.rank[b]; }); sel = sel.slice(0, N); }
    }
    var chosen = {}; sel.forEach(function (i) { chosen[i] = 1; });
    var tops = [];
    for (i = 0; i < n; i++) if (!isNaN(rs.rank[i]) && !chosen[i] && (S.keep > 0 ? true : rs.rank[i] <= N)) tops.push(i);
    tops.sort(function (a, b) { return rs.rank[a] - rs.rank[b]; });
    if (S.keep > 0) { for (i = 0; i < tops.length && sel.length < N; i++) sel.push(tops[i]); }
    else sel = tops;
    var pw = S.wtPow, w = sel.map(function (i) { return pw === 0 ? 1 : Math.pow(score[i], pw); });
    var tot = 0; w.forEach(function (x) { tot += x; });
    if (!(tot > 0)) { sel = []; w = []; tot = 1; }
    var poolIdx = []; for (i = 0; i < n; i++) if (keep[i]) poolIdx.push(i);
    return {
      t: t, ids: sel.map(function (i) { return F.ids[i]; }), w: w.map(function (x) { return x / tot; }),
      score: sel.map(function (i) { return score[i]; }), mcap: sel.map(function (i) { return v.mcap[i]; }), amt60: sel.map(function (i) { return v.amt60[i]; }),
      pool: poolIdx.map(function (i) { return F.ids[i]; }), poolN: poolN, tieShort: (poolN >= N && sel.length < N)
    };
  };

  /* ---------------- 日程 ---------------- */
  function lastLE(dnum, x) { // 最後一個 dnum <= x 的序號，沒有回 -1
    var lo = 0, hi = dnum.length - 1, r = -1;
    while (lo <= hi) { var m = (lo + hi) >> 1; if (dnum[m] <= x) { r = m; lo = m + 1; } else hi = m - 1; }
    return r;
  }
  Store.prototype.schedule = function (S) {
    var dn = this.dnum, T = this.T, out = [], first = this.snapByDay, startNum = Date.parse(S.start) / 864e5;
    var y0 = +this.ymd[0].slice(0, 4), y1 = +this.ymd[T - 1].slice(0, 4);
    for (var y = y0; y <= y1; y++) for (var m = 1; m <= 12; m++) {
      if (S.freq === 'Q' && m % 3 !== 0) continue;
      var cal = Date.UTC(y, m, 0) / 864e5;                 // 月底日曆日
      var lab = cal + (S.timing === 'me' ? 0 : 14);
      var tr = lastLE(dn, lab) + 1;                        // 標籤日之後第一個交易日
      if (tr >= T) break;
      var fr = lastLE(dn, cal);
      var jd = (S.timing === 'off14') ? lastLE(dn, lab) : fr;
      if (jd < 0 || !first.has(jd)) continue;
      if (dn[jd] < startNum) continue;
      out.push({ jd: jd, tr: tr });
    }
    return out;
  };

  /* ---------------- 模擬（單一路徑，逐日） ---------------- */
  // periods: [{tr, ids, w}]；回傳 {nav, base, turn, buys}
  Store.prototype.simulate = function (periods, fee, tax, endIdx, wantBuys) {
    var T = this.T, R = this.R, excR = this.excR, hasExc = excR.size > 0, sell = this.sellday;
    var t0 = periods[0].tr, tEnd = Math.min(endIdx == null ? T - 1 : endIdx, T - 1);
    var nav = new Float64Array(tEnd - t0 + 2); nav[0] = 1;
    var idx = [], P = [], cash = 1, turn = 0, pi = 0, buys = [];
    for (var t = t0; t <= tEnd; t++) {
      var j, sumP = 0;
      for (j = 0; j < idx.length; j++) {
        var s = idx[j]; if (s < 0) continue;
        var k = s * T + t, r = R[k];
        if (hasExc && excR.has(k)) r = excR.get(k);
        P[j] *= 1 + r / 1e4;
        if (sell[s] >= 0 && t === sell[s]) { cash += P[j] * (1 - fee - tax); turn += P[j]; P[j] = 0; idx[j] = -1; }
      }
      if (pi < periods.length && periods[pi].tr === t) {
        var pr = periods[pi++], V = cash, i2;
        for (j = 0; j < idx.length; j++) if (idx[j] >= 0) V += P[j];
        var newIdx = [], newW = [];
        for (i2 = 0; i2 < pr.ids.length; i2++) {
          var sd = sell[pr.ids[i2]];
          if (sd !== -1 && sd <= t) continue;              // 已下市或當天賣出日：不買（權重留在現金）
          newIdx.push(pr.ids[i2]); newW.push(pr.w[i2]);
        }
        var oldMap = new Map();
        for (j = 0; j < idx.length; j++) if (idx[j] >= 0) oldMap.set(idx[j], P[j]);
        var buy = 0, sellv = 0, tg = 0, nP = [], matched = new Set(), bl = [];
        for (i2 = 0; i2 < newIdx.length; i2++) {
          var T_ = newW[i2] * V, cur = oldMap.has(newIdx[i2]) ? oldMap.get(newIdx[i2]) : 0;
          if (oldMap.has(newIdx[i2])) matched.add(newIdx[i2]);
          if (T_ > cur) { buy += T_ - cur; if (wantBuys) bl.push([newIdx[i2], (T_ - cur) / V]); }
          else sellv += cur - T_;
          nP.push(T_); tg += T_;
        }
        oldMap.forEach(function (val, key) { if (!matched.has(key)) sellv += val; });
        var cost = buy * fee + sellv * (fee + tax), sc = (V - cost) / V;
        for (i2 = 0; i2 < nP.length; i2++) nP[i2] *= sc;
        cash = (V - tg) * sc; turn += buy + sellv;
        idx = newIdx; P = nP;
        if (wantBuys) buys.push({ tr: t, list: bl });
      }
      var tv = cash;
      for (j = 0; j < idx.length; j++) if (idx[j] >= 0) tv += P[j];
      nav[t - t0 + 1] = tv;
    }
    return { nav: nav, t0: t0, tEnd: tEnd, turn: turn, buys: buys };
  };

  /* ---------------- 指標 ---------------- */
  function metrics(nav, dnumBase) {   // dnumBase: 長度同 nav 的日曆日序號
    var n = nav.length - 1, i, sum = 0, sq = 0, peak = nav[0], mdd = 0, uwBest = 0, uwStart = -1;
    var r = new Float64Array(n);
    for (i = 1; i <= n; i++) { r[i - 1] = nav[i] / nav[i - 1] - 1; sum += r[i - 1]; }
    var mean = sum / n; for (i = 0; i < n; i++) sq += (r[i] - mean) * (r[i] - mean);
    var sd = Math.sqrt(sq / (n - 1)), yrs = (dnumBase[n] - dnumBase[0]) / 365.25;
    for (i = 0; i <= n; i++) {
      if (nav[i] >= peak) { peak = nav[i]; if (uwStart >= 0) { uwBest = Math.max(uwBest, dnumBase[i] - dnumBase[uwStart]); uwStart = -1; } }
      else { if (uwStart < 0) uwStart = i; var d = nav[i] / peak - 1; if (d < mdd) mdd = d; }
    }
    if (uwStart >= 0) uwBest = Math.max(uwBest, dnumBase[n] - dnumBase[uwStart]);
    // 新增欄位（不動上面的計算）：Calmar＝年化 ÷ |最大跌幅|；Sortino＝日報酬平均 × 252 ÷（下行標準差 × √252），
    // 下行標準差＝sqrt(mean(min(r,0)²))，對全部交易日取平均，目標報酬 0，不扣無風險利率（跟日夏普同口徑）
    var annV = Math.pow(nav[n] / nav[0], 1 / yrs) - 1, dsq = 0;
    for (i = 0; i < n; i++) if (r[i] < 0) dsq += r[i] * r[i];
    var dsd = Math.sqrt(dsq / n);
    return { ann: Math.pow(nav[n] / nav[0], 1 / yrs) - 1, sharpe: sd > 0 ? mean / sd * Math.sqrt(252) : NaN, mdd: mdd, uwYears: uwBest / 365.25, total: nav[n] / nav[0], days: n, yrs: yrs, r: r,
             calmar: mdd < 0 ? annV / Math.abs(mdd) : NaN, sortino: dsd > 0 ? mean * 252 / (dsd * Math.sqrt(252)) : NaN };
  }
  function mddOf(nav) { var pk = nav[0], m = 0; for (var i = 0; i < nav.length; i++) { if (nav[i] > pk) pk = nav[i]; var d = nav[i] / pk - 1; if (d < m) m = d; } return m; }
  // 每日報酬乘固定倍數 m（≤1，其餘放現金不計息），二分法找最大倍數使最大跌幅不超過 target
  function scaleTo(r, target) {
    function nv(m) { var a = new Float64Array(r.length + 1); a[0] = 1; for (var i = 0; i < r.length; i++) a[i + 1] = a[i] * (1 + m * r[i]); return a; }
    if (mddOf(nv(1)) >= target) return { m: 1, nav: nv(1) };
    var lo = 0, hi = 1;
    for (var it = 0; it < 40; it++) { var mid = (lo + hi) / 2; if (mddOf(nv(mid)) >= target) lo = mid; else hi = mid; }
    return { m: lo, nav: nv(lo) };
  }
  function yearly(nav, ymdBase) {   // ymdBase: 每個 nav 點對應日期字串
    var out = [], last = 0;
    for (var i = 1; i < nav.length; i++) {
      var y = ymdBase[i].slice(0, 4), ny = i + 1 < nav.length ? ymdBase[i + 1].slice(0, 4) : null;
      if (ny !== y) { out.push({ y: +y, ret: nav[i] / nav[last] - 1, partial: (last === 0 && ymdBase[0].slice(5) !== '12-31' && y === ymdBase[0].slice(0, 4)) || ny === null && ymdBase[i].slice(5) < '12-25' }); last = i; }
    }
    return out;
  }

  /* ---------------- 回測總流程 ---------------- */
  function mergeSettings(S) {
    var o = {}, k;
    for (k in DEFAULTS) o[k] = DEFAULTS[k];
    for (k in S) o[k] = S[k];
    o.conds = normCond(S.conds);
    return o;
  }

  Store.prototype.run = function (S0, opts) {
    opts = opts || {};
    var S = mergeSettings(S0), T = this.T;
    if (!this.priceReady) throw new Error('每日報酬尚未載入');
    // 籌碼條件自動從 2015-01-30 判斷日（2015-02 第一次成交）起
    var floor = Date.parse(S.start) / 864e5;
    if (S.conds.trust && floor < Date.parse('2015-01-30') / 864e5) floor = Date.parse('2015-01-30') / 864e5;
    var S2 = {}; for (var kk in S) S2[kk] = S[kk]; S2.start = new Date(floor * 864e5).toISOString().slice(0, 10);
    var sched = this.schedule(S2), picks = [], prev = null, i;
    var endIdx = S.end ? lastLE(this.dnum, Date.parse(S.end) / 864e5) : T - 1;
    sched = sched.filter(function (x) { return x.tr <= endIdx; });
    for (i = 0; i < sched.length; i++) {
      var p = this.pick(sched[i].jd, S2, prev);
      if (!p) { sched.splice(i, 1); i--; continue; }
      p.tr = sched[i].tr; p.jd = sched[i].jd; prev = p.ids; picks.push(p);
    }
    if (!picks.length) return { empty: true, S: S2 };
    var sim = this.simulate(picks, S.fee, S.tax, endIdx, true);
    var sim0 = this.simulate(picks, 0, 0, endIdx, false);
    var t0 = sim.t0, n = sim.nav.length;
    var base = new Array(n), baseNum = new Float64Array(n);
    for (i = 0; i < n; i++) { var di = t0 - 1 + i; base[i] = this.ymd[di]; baseNum[i] = this.dnum[di]; }
    var b50 = new Float64Array(n); b50[0] = 1;
    for (i = 1; i < n; i++) b50[i] = b50[i - 1] * (1 + this.meta.r50[t0 - 1 + i] / 1e4);
    var m = metrics(sim.nav, baseNum), m0 = metrics(sim0.nav, baseNum), mb = metrics(b50, baseNum);
    var sc = scaleTo(m.r, -0.2), mcs = metrics(sc.nav, baseNum), sc50 = scaleTo(mb.r, -0.2), m50s = metrics(sc50.nav, baseNum);
    var meanNav = 0; for (i = 0; i < n; i++) meanNav += sim.nav[i]; meanNav /= n;
    var turn = sim.turn / 2 / meanNav / m.yrs;
    // 容量：1,000 萬元帳戶，每筆買進金額超過該股 60 日均成交額（判斷日）的 5%
    var cap = 0, capN = 0, byTr = {};
    picks.forEach(function (p) { var o = {}; p.ids.forEach(function (id, j) { o[id] = p.amt60[j]; }); byTr[p.tr] = o; });
    sim.buys.forEach(function (b) { b.list.forEach(function (x) { capN++; var a = byTr[b.tr][x[0]]; if (x[1] * 1e7 > 0.05 * a) cap++; }); });
    var dd = new Float64Array(n), pk = 0; for (i = 0; i < n; i++) { if (sim.nav[i] > pk) pk = sim.nav[i]; dd[i] = sim.nav[i] / pk - 1; }
    var dd50 = new Float64Array(n); pk = 0; for (i = 0; i < n; i++) { if (b50[i] > pk) pk = b50[i]; dd50[i] = b50[i] / pk - 1; }
    var lastP = picks[picks.length - 1];
    return {
      S: S2, base: base, baseNum: baseNum, nav: sim.nav, nav0: sim0.nav, b50: b50, dd: dd, dd50: dd50,
      m: strip(m), m0: strip(m0), mb: strip(mb), scale: { m: sc.m, ann: mcs.ann, mdd: mcs.mdd, ann50: m50s.ann, m50: sc50.m },
      yearly: yearly(sim.nav, base), yearly50: yearly(b50, base), turnover: turn, costPP: m0.ann - m.ann,
      capacity: { share: capN ? cap / capN : 0, n: capN, hit: cap },
      picks: picks, periods: picks.length, firstTrade: this.ymd[t0], endDay: this.ymd[sim.tEnd], latestPick: this.ymd[lastP.jd],
      poolAvg: picks.reduce(function (a, p) { return a + p.poolN; }, 0) / picks.length, tieShort: picks.filter(function (p) { return p.tieShort; }).length,
      endIdx: endIdx
    };
  };
  function strip(m) { var o = {}; for (var k in m) if (k !== 'r') o[k] = m[k]; return o; }

  /* ---------------- 同池隨機對照 ---------------- */
  // 每期從同一個池子隨機抽同樣檔數、等權。回傳 {costDiff[], nocostDiff[]}（年化差：策略減隨機）
  function mulberry(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  Store.prototype.randomControl = function (res, draws, seed, yieldFn) {
    var self = this, S = res.S, rng = mulberry(seed || 20261115), picks = res.picks, n = S.n;
    var cost = [], nocost = [], d = 0, endIdx = res.endIdx;
    var annS = res.m.ann, annS0 = res.m0.ann;
    function one() {
      var per = picks.map(function (p) {
        var m = p.pool.length, k = Math.min(n, m), arr = p.pool.slice(), ids = [], w = [];
        for (var i = 0; i < k; i++) { var j = i + Math.floor(rng() * (m - i)); var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp; ids.push(arr[i]); w.push(1 / k); }
        return { tr: p.tr, ids: ids, w: w };
      });
      var a = self.simulate(per, S.fee, S.tax, endIdx, false), b = self.simulate(per, 0, 0, endIdx, false);
      cost.push(annS - metrics(a.nav, res.baseNum).ann); nocost.push(annS0 - metrics(b.nav, res.baseNum).ann);
    }
    function q(a, p) { var s = a.slice().sort(function (x, y) { return x - y; }), h = (s.length - 1) * p, lo = Math.floor(h), hi = Math.ceil(h); return s[lo] + (s[hi] - s[lo]) * (h - lo); }
    function summ() {
      return { n: cost.length, cost: { med: q(cost, .5), lo: q(cost, .025), hi: q(cost, .975) }, nocost: { med: q(nocost, .5), lo: q(nocost, .025), hi: q(nocost, .975) } };
    }
    if (yieldFn) {   // 非同步：每批之後讓出，讓 Worker 能收新訊息
      return (async function () {
        while (d < draws) {
          var stop = Math.min(draws, d + 10);
          for (; d < stop; d++) one();
          if (await yieldFn(d, summ())) return null;
        }
        return summ();
      })();
    }
    for (; d < draws; d++) one();
    return summ();
  };

  var api = { FACTORS: FACTORS, FIDX: FIDX, PRESETS: PRESETS, DEFAULTS: DEFAULTS, Store: Store, parseF: parseF, parseR: parseR, metrics: metrics, scaleTo: scaleTo, mergeSettings: mergeSettings, avgRank: avgRank };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.TWS = api;
})(typeof self !== 'undefined' ? self : this);
