/* 回測在 Worker 裡跑，頁面不會卡住。先載因子資料，再載每日報酬；載完才算得出結果。 */
importScripts('engine.js');
var store = null, latest = 0, ready = false, pending = null, base = '';

function isGzip(buf) { var u = new Uint8Array(buf, 0, 2); return u[0] === 0x1f && u[1] === 0x8b; }
async function getBin(name) {
  var r = await fetch(base + 'data/' + name);
  if (!r.ok) throw new Error(name + ' ' + r.status);
  var buf = await r.arrayBuffer(), bytes = buf.byteLength;
  if (isGzip(buf)) {
    var ds = new Response(new Blob([buf]).stream().pipeThrough(new DecompressionStream('gzip')));
    buf = await ds.arrayBuffer();
  }
  return { buf: buf, bytes: bytes };
}

async function init(b) {
  base = b;
  try {
    if (typeof DecompressionStream === 'undefined') throw new Error('這個瀏覽器不支援 DecompressionStream，請改用較新版的 Chrome、Safari 或 Firefox');
    var t0 = Date.now(), mr = await fetch(base + 'data/meta.json');
    var meta = await mr.json();
    store = new TWS.Store(meta);
    var years = meta.years, total = years.length * 2, done = 0, bytes = 0;
    postMessage({ type: 'meta', built: meta.built, dataEnd: meta.data_end, firstDay: meta.first_day });
    // 因子檔先（小），每日報酬檔接著
    for (var i = 0; i < years.length; i++) {
      try { var f = await getBin('f_' + years[i] + '.bin.gz'); bytes += f.bytes; store.addF(TWS.parseF(f.buf)); } catch (e) { /* 該年沒有快照檔 */ }
      postMessage({ type: 'progress', stage: 'f', done: ++done, total: total, bytes: bytes, ms: Date.now() - t0 });
    }
    postMessage({ type: 'factors-ready', ms: Date.now() - t0 });
    for (i = 0; i < years.length; i++) {
      var r = await getBin('r_' + years[i] + '.bin.gz'); bytes += r.bytes; store.addR(TWS.parseR(r.buf));
      postMessage({ type: 'progress', stage: 'r', done: ++done, total: total, bytes: bytes, ms: Date.now() - t0 });
    }
    store.finishReturns();
    ready = true;
    postMessage({ type: 'ready', ms: Date.now() - t0, bytes: bytes });
    if (pending) { var m = pending; pending = null; doRun(m); }
  } catch (e) { postMessage({ type: 'error', msg: String(e && e.message || e) }); }
}

function plain(res) {
  var st = store;
  return {
    S: res.S, base: res.base, baseNum: Array.from(res.baseNum), nav: res.nav, nav0: res.nav0, b50: res.b50, dd: res.dd, dd50: res.dd50,
    m: res.m, m0: res.m0, mb: res.mb, scale: res.scale, yearly: res.yearly, yearly50: res.yearly50, turnover: res.turnover, costPP: res.costPP,
    capacity: res.capacity, periods: res.periods, firstTrade: res.firstTrade, endDay: res.endDay, latestPick: res.latestPick, poolAvg: res.poolAvg, tieShort: res.tieShort,
    picks: res.picks.map(function (p) {
      return { jd: st.ymd[p.jd], tr: st.ymd[p.tr], poolN: p.poolN, rows: p.ids.map(function (id, j) { var s = st.meta.stocks[id]; return [s.c, s.n, p.w[j], p.score[j], p.mcap[j] / 1e8]; }) };
    })
  };
}

async function doRun(m) {
  latest = m.id;
  if (!ready) { pending = m; return; }
  try {
    var t0 = Date.now(), res = store.run(m.S);
    if (res.empty) { postMessage({ type: 'result', id: m.id, empty: true, S: res.S }); return; }
    var out = plain(res);
    out.ms = Date.now() - t0;
    postMessage({ type: 'result', id: m.id, r: out });
    var id = m.id;
    var sum = await store.randomControl(res, m.draws, 20261115, async function (d, s) {
      postMessage({ type: 'rc', id: id, n: d, total: m.draws, summ: s });
      await new Promise(function (r) { setTimeout(r, 0); });
      return latest !== id;
    });
    if (sum) postMessage({ type: 'rc', id: id, n: m.draws, total: m.draws, summ: sum, done: true });
  } catch (e) { postMessage({ type: 'error', id: m.id, msg: String(e && e.message || e) }); }
}

onmessage = function (e) {
  var m = e.data;
  if (m.type === 'init') init(m.base);
  else if (m.type === 'run') doRun(m);
};
