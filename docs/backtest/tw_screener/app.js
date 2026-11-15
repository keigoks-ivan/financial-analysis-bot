/* 台股互動選股回測器：頁面介面。回測在 worker.js，這裡只管輸入與顯示。 */
(function () {
  'use strict';
  var TW = window.TWS, $ = function (s, r) { return (r || document).querySelector(s); };
  var root = $('#tws-app');
  if (!root || !TW) return;
  var FAC = TW.FACTORS, PRE = TW.PRESETS;
  var worker, runId = 0, timer = null, last = null, ready = false, info = {}, state = { conds: {} };
  var COLORS = ['#2a78d6', '#eb6834', '#1baf7a', '#7c5cbf'];

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function mi(s) { return s.replace('-', '−'); }
  function pct(x, n) { return isFinite(x) ? mi((x * 100).toFixed(n == null ? 1 : n)) + '%' : '—'; }
  function ppt(x, n) { return isFinite(x) ? (x >= 0 ? '+' : '−') + Math.abs(x * 100).toFixed(n == null ? 1 : n) + ' 個百分點' : '—'; }

  /* ---------------- 試驗次數（只存在這位讀者的瀏覽器） ---------------- */
  var TKEY = 'twscreener_trials_v1', mem = {};
  function tload() { try { var s = localStorage.getItem(TKEY); if (s) return JSON.parse(s); } catch (e) { } return Object.keys(mem); }
  function tsave(arr) { try { localStorage.setItem(TKEY, JSON.stringify(arr)); } catch (e) { } arr.forEach(function (k) { mem[k] = 1; }); }
  function hash(s) { var h = 5381; for (var i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0; return (h >>> 0).toString(36); }
  function countTrial(S) {
    var key = hash(JSON.stringify(S, Object.keys(S).sort())), arr = tload();
    if (arr.indexOf(key) < 0) { arr.push(key); tsave(arr); }
    $('#tws-trials').innerHTML = '你在這個瀏覽器裡已經試過 <b>' + arr.length + '</b> 組不同設定。試越多組，越容易挑到碰巧好看的結果，最後那組的績效不能直接當成預期。';
  }

  /* ---------------- 控制項 ---------------- */
  function h(html) { var d = document.createElement('div'); d.innerHTML = html; return d.firstElementChild; }
  var MODES = [['off', '不用'], ['filter', '門檻'], ['rank', '排名'], ['both', '門檻＋排名']];

  function buildControls() {
    var presets = Object.keys(PRE).map(function (k) { return '<button type="button" class="tws-btn" data-preset="' + k + '">' + esc(PRE[k].name) + '</button>'; }).join('');
    var facs = FAC.map(function (f) {
      var tag = (f.supp ? '<span class="tws-tag">補的</span>' : '') + '<span class="tws-tag tws-tag2">' + esc(f.start) + ' 起</span>';
      return '<div class="tws-fr" data-k="' + f.k + '"><div class="tws-fn"><b>' + esc(f.name) + '</b>' + tag + '<div class="tws-fd">' + esc(f.def) + '</div></div>' +
        '<div class="tws-ff"><label>用法<select class="m">' + MODES.map(function (m) { return '<option value="' + m[0] + '">' + m[1] + '</option>'; }).join('') + '</select></label>' +
        '<label class="t">門檻<select class="op"><option value="&gt;">大於</option><option value="&lt;">小於</option></select><input class="val" type="number" step="any" value="0"><span class="u">' + esc(f.unit) + '</span></label>' +
        '<label class="r">排名<select class="dir"><option value="hi">高好</option><option value="lo">低好</option></select>權重<input class="w" type="number" min="0" step="0.5" value="1"></label></div></div>';
    }).join('');
    root.querySelector('#tws-controls').innerHTML =
      '<div class="tws-row"><span class="tws-lb">一鍵帶入</span>' + presets + '<button type="button" class="tws-btn tws-ghost" data-preset="clear">全部清除</button></div>' +
      '<p class="tws-note" id="tws-pnote"></p>' +
      '<h3 class="sub-title">一、池子</h3><div class="tws-grid">' +
      '<label>流動性前 <input id="c-liq" type="number" min="5" max="100" step="5" value="50"> %<small>60 日均成交額排名，100 ＝不限</small></label>' +
      '<label>市值排名前 <input id="c-mrank" type="number" min="0" step="50" value="0"> 名<small>0 ＝不限</small></label>' +
      '<label>市值下限 <input id="c-mmin" type="number" min="0" step="10" value="0"> 億元<small>0 ＝不限</small></label>' +
      '<label>市場 <select id="c-mkt"><option value="all">上市＋上櫃</option><option value="TWSE">只上市</option><option value="TPEX">只上櫃</option></select></label></div>' +
      '<h3 class="sub-title">二、條件（19 項）</h3><p class="tws-note">「門檻」是不符合就不進池子；「排名」是在池子裡換成 0 到 1 的百分位，再依權重加權平均成分數。同一項可以兩個都用。</p>' +
      '<div class="tws-facs">' + facs + '</div>' +
      '<h3 class="sub-title">三、合成與持股</h3><div class="tws-grid">' +
      '<label>百分位的母體 <select id="c-basis"><option value="pool">池子內</option><option value="all">全市場</option></select><small>FinLab 四因子複合用全市場</small></label>' +
      '<label>排名項目缺值 <select id="c-miss"><option value="drop">該檔不入選</option><option value="zero">該項記 0 分</option></select></label>' +
      '<label>持股檔數 <input id="c-n" type="number" min="1" max="100" step="1" value="20"></label>' +
      '<label>權重 <select id="c-wp"><option value="0">等權</option><option value="1">按分數</option><option value="2">分數的平方</option><option value="3">分數的三次方</option></select></label>' +
      '<label>續抱名次 <input id="c-keep" type="number" min="0" max="200" step="5" value="0"><small>0 ＝不用；原持股仍在前 K 名就不換</small></label>' +
      '<label>換股頻率 <select id="c-freq"><option value="M">每月</option><option value="Q">每季（3、6、9、12 月）</option></select></label>' +
      '<label>換股日 <select id="c-timing"><option value="me">月底判斷，下一個交易日收盤成交</option><option value="off14">月底加 14 天後才判斷與成交（FinLab 的 offset 14D）</option><option value="off14frozen">月底判斷，月底加 14 天後才成交（動能輪動的讀法）</option></select></label></div>' +
      '<h3 class="sub-title">四、成本與期間</h3><div class="tws-grid">' +
      '<label>手續費（買賣各一次） <input id="c-fee" type="number" min="0" step="0.005" value="0.1425"> %</label>' +
      '<label>證交稅（只有賣出） <input id="c-tax" type="number" min="0" step="0.05" value="0.3"> %</label>' +
      '<label>起日 <input id="c-start" type="date" min="2014-01-01" value="2014-01-02"><small>用到投信買超強度會自動從 2015-02 起</small></label>' +
      '<label>訖日 <input id="c-end" type="date" min="2014-02-01"></label>' +
      '<label>隨機對照次數 <select id="c-draws"><option>200</option><option>500</option><option>1000</option></select></label></div>';
  }

  function readUI() {
    var S = { conds: {} }, num = function (id) { return +$('#' + id).value; };
    S.liq = Math.min(100, Math.max(1, num('c-liq') || 50)); S.mcapRank = Math.max(0, num('c-mrank') || 0); S.mcapMin = Math.max(0, num('c-mmin') || 0);
    S.market = $('#c-mkt').value; S.pctBasis = $('#c-basis').value; S.missing = $('#c-miss').value;
    S.n = Math.max(1, Math.round(num('c-n') || 20)); S.wtPow = +$('#c-wp').value; S.keep = Math.max(0, Math.round(num('c-keep') || 0));
    S.freq = $('#c-freq').value; S.timing = $('#c-timing').value;
    S.fee = Math.max(0, num('c-fee')) / 100; S.tax = Math.max(0, num('c-tax')) / 100;
    S.start = $('#c-start').value || '2014-01-02'; S.end = $('#c-end').value || null;
    FAC.forEach(function (f) {
      var row = $('.tws-fr[data-k="' + f.k + '"]'), m = $('.m', row).value, c = {};
      if (m === 'filter' || m === 'both') { var v = parseFloat($('.val', row).value); if (isFinite(v)) c.filter = { op: $('.op', row).value, val: v / f.mul }; }
      if (m === 'rank' || m === 'both') c.rank = { dir: $('.dir', row).value, w: Math.max(0, parseFloat($('.w', row).value) || 0) };
      if (c.filter || c.rank) S.conds[f.k] = c;
    });
    return S;
  }
  function applyPreset(k) {
    FAC.forEach(function (f) { var row = $('.tws-fr[data-k="' + f.k + '"]'); $('.m', row).value = 'off'; $('.dir', row).value = f.dir; $('.w', row).value = 1; $('.val', row).value = 0; $('.op', row).value = '>'; row.className = 'tws-fr'; });
    var note = $('#tws-pnote');
    if (k === 'clear') {
      var d = TW.DEFAULTS, set = function (id, v) { $('#' + id).value = v; };
      set('c-liq', 50); set('c-mrank', 0); set('c-mmin', 0); set('c-mkt', 'all'); set('c-basis', 'pool'); set('c-miss', 'drop'); set('c-n', 20); set('c-wp', 0); set('c-keep', 0);
      set('c-freq', 'M'); set('c-timing', 'me'); set('c-start', '2014-01-02'); set('c-end', '');
      note.textContent = '已清除全部條件。至少選一項排名條件，否則名單等於池子裡隨便選。'; syncRows(); schedule(); return;
    }
    var P = PRE[k], s = P.s, set2 = function (id, v) { $('#' + id).value = v; };
    set2('c-liq', s.liq); set2('c-mrank', s.mcapRank); set2('c-mmin', s.mcapMin); set2('c-mkt', s.market); set2('c-basis', s.pctBasis); set2('c-miss', s.missing);
    set2('c-n', s.n); set2('c-wp', s.wtPow); set2('c-keep', s.keep); set2('c-freq', s.freq); set2('c-timing', s.timing);
    var st = P.start < '2014-01-02' ? '2014-01-02' : P.start;
    set2('c-start', st); set2('c-end', '');
    for (var key in s.conds) {
      var f = TW.FIDX[key], row = $('.tws-fr[data-k="' + key + '"]'), c = s.conds[key];
      $('.m', row).value = c.filter && c.rank ? 'both' : c.filter ? 'filter' : 'rank';
      if (c.filter) { $('.op', row).value = c.filter.op; $('.val', row).value = +(c.filter.val * f.mul).toPrecision(6); }
      if (c.rank) { $('.dir', row).value = c.rank.dir; $('.w', row).value = c.rank.w; }
    }
    note.textContent = P.note;
    syncRows(); schedule();
  }
  function syncRows() {
    FAC.forEach(function (f) {
      var row = $('.tws-fr[data-k="' + f.k + '"]'), m = $('.m', row).value;
      row.classList.toggle('on', m !== 'off'); row.classList.toggle('has-t', m === 'filter' || m === 'both'); row.classList.toggle('has-r', m === 'rank' || m === 'both');
    });
  }

  /* ---------------- 執行 ---------------- */
  function schedule() { clearTimeout(timer); timer = setTimeout(go, 450); }
  function go() {
    var S = readUI();
    if (!Object.keys(S.conds).some(function (k) { return S.conds[k].rank; })) {
      $('#tws-status').innerHTML = '<span class="tws-warn">還沒選排名條件。請至少把一項條件的用法設成「排名」或「門檻＋排名」，或按上面的預設組合。</span>';
    }
    countTrial(S);
    runId++;
    $('#tws-out').classList.add('stale');
    if (!ready) { $('#tws-status').innerHTML += ' 資料載入完成後會自動計算。'; }
    worker.postMessage({ type: 'run', id: runId, S: S, draws: +$('#c-draws').value });
  }

  function onMsg(e) {
    var m = e.data;
    if (m.type === 'meta') { info = m; }
    else if (m.type === 'progress') {
      var pr = $('#tws-load'); pr.hidden = false;
      pr.innerHTML = (m.stage === 'f' ? '載入因子資料' : '背景載入每日報酬') + '：' + m.done + ' / ' + m.total + '（已傳輸 ' + (m.bytes / 1048576).toFixed(1) + ' MB）';
    }
    else if (m.type === 'factors-ready') { info.factorsMs = m.ms; }
    else if (m.type === 'ready') {
      ready = true; info.loadMs = m.ms; info.bytes = m.bytes;
      $('#tws-load').innerHTML = '資料已載入：' + (m.bytes / 1048576).toFixed(1) + ' MB，' + (m.ms / 1000).toFixed(1) + ' 秒。';
    }
    else if (m.type === 'result' && m.id === runId) {
      $('#tws-out').classList.remove('stale');
      if (m.empty) { $('#tws-status').innerHTML = '<span class="tws-warn">這組條件在這段期間每一期的池子都是空的，沒有名單。放寬門檻或把流動性比例調高。</span>'; $('#tws-res').hidden = true; return; }
      last = m.r; render(m.r);
    }
    else if (m.type === 'rc' && m.id === runId) renderRC(m);
    else if (m.type === 'error') { $('#tws-status').innerHTML = '<span class="tws-warn">錯誤：' + esc(m.msg) + '</span>'; }
  }

  /* ---------------- 顯示 ---------------- */
  function kpiRow(name, m, extra) {
    return '<tr><td class="lbl">' + name + '</td><td class="num">' + pct(m.ann) + '</td><td class="num">' + (isFinite(m.sharpe) ? m.sharpe.toFixed(2) : '—') + '</td><td class="num ng">' + pct(m.mdd) + '</td><td class="num">' + m.uwYears.toFixed(1) + ' 年</td><td class="num">' + m.total.toFixed(2) + ' 倍</td></tr>';
  }
  function render(r) {
    $('#tws-res').hidden = false;
    var s = r.S, tr = [];
    $('#tws-status').innerHTML = '期間 <b>' + r.firstTrade + '</b>（第一次成交）到 <b>' + r.endDay + '</b>，共 ' + r.periods + ' 次換股，平均池子 ' + Math.round(r.poolAvg) + ' 檔；計算 ' + r.ms + ' 毫秒。' +
      (s.conds.trust ? ' 用到投信買超強度，判斷日自動從 2015-01-30 起。' : '') + (r.tieShort ? ' 有 ' + r.tieShort + ' 期因為並列在邊界，入選檔數少於設定值。' : '');
    $('#tws-kpi').innerHTML = '<table><thead><tr><th></th><th class="num">年化（日曆年）</th><th class="num">日夏普</th><th class="num">最大跌幅</th><th class="num">最長水下</th><th class="num">累積</th></tr></thead><tbody>' +
      kpiRow('這組設定（扣成本）', r.m) + kpiRow('同一組、不扣成本', r.m0) + kpiRow('0050 含息', r.mb) + '</tbody></table>';
    var sc = r.scale;
    $('#tws-extra').innerHTML = '<ul class="bul">' +
      '<li><b>跌幅縮到 −20% 之後</b>：每日報酬乘 ' + sc.m.toFixed(2) + ' 倍，其餘放現金不計息，年化 <b>' + pct(sc.ann) + '</b>，最大跌幅 ' + pct(sc.mdd) + '。同樣處理 0050 含息（乘 ' + sc.m50.toFixed(2) + ' 倍）：年化 ' + pct(sc.ann50) + '。</li>' +
      '<li><b>年換手率</b> ' + (r.turnover * 100).toFixed(0) + '%；成本（手續費與證交稅）每年吃掉 <b>' + (r.costPP * 100).toFixed(1) + ' 個百分點</b>的年化。</li>' +
      '<li><b>容量</b>：假設帳戶 1,000 萬元，' + r.capacity.n + ' 筆買進裡有 ' + r.capacity.hit + ' 筆（' + (r.capacity.share * 100).toFixed(1) + '%）超過該股 60 日均成交額的 5%。這裡用判斷日的 60 日均額代替成交日當天成交額。</li></ul>';
    drawCharts(r);
    // 逐年
    var rows = '', by50 = {}; r.yearly50.forEach(function (y) { by50[y.y] = y.ret; });
    r.yearly.forEach(function (y) {
      var d = y.ret - by50[y.y];
      rows += '<tr><td class="lbl">' + y.y + (y.partial ? '（部分年度）' : '') + '</td><td class="num ' + (y.ret < 0 ? 'ng' : '') + '">' + pct(y.ret) + '</td><td class="num ' + (by50[y.y] < 0 ? 'ng' : '') + '">' + pct(by50[y.y]) + '</td><td class="num ' + (d < 0 ? 'ng' : '') + '">' + (d >= 0 ? '+' : '') + mi((d * 100).toFixed(1)) + '</td></tr>';
    });
    $('#tws-yearly').innerHTML = '<table class="narrow"><thead><tr><th>年</th><th class="num">這組設定</th><th class="num">0050 含息</th><th class="num">差（點）</th></tr></thead><tbody>' + rows + '</tbody></table>';
    renderPicks(r);
    $('#tws-rc').innerHTML = '<span class="tws-muted">同池隨機對照計算中…</span>';
  }

  function renderRC(m) {
    var s = m.summ, f = function (x) { return (x >= 0 ? '+' : '−') + Math.abs(x * 100).toFixed(1); };
    var row = function (name, q) { return '<tr><td class="lbl">' + name + '</td><td class="num">' + f(q.med) + '</td><td class="num">' + f(q.lo) + ' 到 ' + f(q.hi) + '</td><td class="num">' + (q.lo > 0 ? '不含 0，策略較好' : q.hi < 0 ? '不含 0，策略較差' : '含 0') + '</td></tr>'; };
    $('#tws-rc').innerHTML = '<p class="tws-muted">' + (m.done ? '已抽 ' + m.total + ' 次' : '已抽 ' + m.n + ' / ' + m.total + ' 次，還在跑') + '。每一期從同一個池子隨機抽同樣檔數、等權，其餘（換股日、成本）一樣。下表是「這組設定的年化減隨機組的年化」，單位是個百分點。</p>' +
      '<table><thead><tr><th></th><th class="num">差的中位數</th><th class="num">2.5% 到 97.5% 範圍</th><th class="num">範圍有沒有 0</th></tr></thead><tbody>' +
      row('不扣成本（主要看這個）', s.nocost) + row('扣成本', s.cost) + '</tbody></table>' +
      '<p class="table-note">隨機組每期整批換股，換手比多數策略高，扣成本版的差距會偏大。範圍含 0，代表這組排序方式沒有比在同一個池子裡隨便挑好。</p>';
  }

  function renderPicks(r) {
    var ps = r.picks, lp = ps[ps.length - 1];
    function tbl(p) {
      return '<div class="scroll"><table class="narrow"><thead><tr><th>代號</th><th>名稱</th><th class="num">權重</th><th class="num">分數</th><th class="num">市值（億）</th></tr></thead><tbody>' +
        p.rows.map(function (x) { return '<tr><td>' + x[0] + '</td><td>' + esc(x[1]) + '</td><td class="num">' + (x[2] * 100).toFixed(1) + '%</td><td class="num">' + x[3].toFixed(3) + '</td><td class="num">' + (isFinite(x[4]) ? Math.round(x[4]).toLocaleString() : '—') + '</td></tr>'; }).join('') + '</tbody></table></div>';
    }
    var html = '<div class="tws-latest"><b>最新一期</b>：依 ' + lp.jd + ' 的資料判斷、' + lp.tr + ' 收盤成交，池子 ' + lp.poolN + ' 檔、選 ' + lp.rows.length + ' 檔。這是資料截止日（' + (info.dataEnd || '') + '）前最後一次換股，不是今天的建議。' + tbl(lp) + '</div>';
    html += '<div class="tws-hist">';
    for (var i = ps.length - 2; i >= 0; i--) html += '<details data-i="' + i + '"><summary>' + ps[i].jd + ' 判斷，' + ps[i].tr + ' 成交（' + ps[i].rows.length + ' 檔）</summary><div class="tws-ph"></div></details>';
    html += '</div>';
    $('#tws-picks').innerHTML = html;
    $('#tws-picks').onclick = function (e) {
      var d = e.target.closest ? e.target.closest('summary') : null; if (!d) return;
      var det = d.parentNode, ph = det.querySelector('.tws-ph');
      if (ph && !ph.innerHTML) ph.innerHTML = tbl(ps[+det.getAttribute('data-i')]);
    };
  }

  /* ---------------- 圖 ---------------- */
  function lineChart(el, cfg) {
    var box = el.querySelector('.vch-plot'), tip = el.querySelector('.vch-tip'), x = cfg.x, ML = cfg.kind === 'nav' ? 44 : 50, MR = 12, MT = 8, MB = 22, LOG = cfg.kind === 'nav' && cfg.log, cur = null;
    function tk(lo, hi, n) { var rg = (hi - lo) || 1, s = Math.pow(10, Math.floor(Math.log10(rg / n))), e = rg / n / s; s *= e < 1.5 ? 1 : e < 3 ? 2 : e < 7 ? 5 : 10; var t = []; for (var v = Math.ceil(lo / s) * s; v <= hi + 1e-9; v += s) t.push(+v.toFixed(6)); return t; }
    function fm(v) { if (v == null) return '—'; return cfg.kind === 'nav' ? (v >= 100 ? v.toFixed(0) : v >= 10 ? v.toFixed(1) : v.toFixed(2)) + ' 倍' : mi(v.toFixed(1)) + '%'; }
    function draw() {
      var w = box.clientWidth; if (!w) return; var hh = w < 520 ? 210 : 260, all = [];
      cfg.s.forEach(function (s) { for (var i = 0; i < s.y.length; i += 1) { var v = s.y[i]; if (v != null) all.push(LOG ? Math.log10(v) : v); } });
      var lo = Math.min.apply(null, all), hi = Math.max.apply(null, all), t;
      if (cfg.kind === 'dd') hi = Math.max(hi, 0);
      if (LOG) { t = []; [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500].forEach(function (m) { var v = Math.log10(m); if (v >= lo - .001 && v <= hi + .001) t.push(v); }); if (!t.length) t = [0]; lo = Math.min(lo, t[0]); hi = Math.max(hi, t[t.length - 1]); }
      else { t = tk(lo, hi, 4); lo = Math.min(lo, t[0]); hi = Math.max(hi, t[t.length - 1]); }
      if (hi === lo) hi = lo + 1;
      var x0 = x[0], x1 = x[x.length - 1], X = function (v) { return ML + (v - x0) / (x1 - x0) * (w - ML - MR); }, Y = function (v) { return MT + (hi - v) / (hi - lo) * (hh - MT - MB); }, s = '';
      t.forEach(function (v) { var lab = LOG ? fm(Math.pow(10, v)).replace(' 倍', '×') : fm(v); s += '<line x1="' + ML + '" x2="' + (w - MR) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" stroke="#e5e7eb"/><text x="' + (ML - 6) + '" y="' + (Y(v) + 4) + '" text-anchor="end">' + lab + '</text>'; });
      var y0 = new Date(x0 * 864e5).getUTCFullYear(), y1 = new Date(x1 * 864e5).getUTCFullYear(), step = Math.max(1, Math.ceil((y1 - y0 + 1) * 46 / (w - ML - MR)));
      for (var y = y0 + 1; y <= y1; y++) { if ((y - y0 - 1) % step) continue; var px = X(Date.UTC(y, 0, 1) / 864e5); s += '<line x1="' + px + '" x2="' + px + '" y1="' + (hh - MB) + '" y2="' + (hh - MB + 4) + '" stroke="#9ca3af"/><text x="' + px + '" y="' + (hh - 6) + '" text-anchor="middle">' + y + '</text>'; }
      cfg.s.slice().reverse().forEach(function (se, ri) {
        var i = cfg.s.length - 1 - ri, d = '', on = false, stp = Math.max(1, Math.floor(x.length / (w * 1.5)));
        for (var k = 0; k < x.length; k += stp) { var v = se.y[k]; if (v == null) { on = false; continue; } d += (on ? 'L' : 'M') + X(x[k]).toFixed(1) + ' ' + Y(LOG ? Math.log10(v) : v).toFixed(1); on = true; }
        if (cfg.kind === 'dd' && i === 0) s += '<path d="' + d + 'L' + X(x1) + ' ' + Y(0) + 'L' + X(x0) + ' ' + Y(0) + 'Z" fill="' + COLORS[0] + '" fill-opacity=".12" stroke="none"/>';
        s += '<path d="' + d + '" fill="none" stroke="' + COLORS[i] + '" stroke-width="' + (i ? 1.4 : 1.9) + '" stroke-linejoin="round"/>';
      });
      box.innerHTML = '<svg height="' + hh + '" viewBox="0 0 ' + w + ' ' + hh + '" role="img" aria-label="' + esc(cfg.title) + '">' + s + '<line class="ch" y1="' + MT + '" y2="' + (hh - MB) + '" stroke="#6b7280" visibility="hidden"/></svg>';
      cur = { X: X, w: w };
    }
    box.onpointermove = function (e) {
      if (!cur) return; var rc = box.getBoundingClientRect(), px = e.clientX - rc.left; if (px < ML || px > cur.w - MR) { tip.style.display = 'none'; return; }
      var xv = x[0] + (px - ML) / (cur.w - ML - MR) * (x[x.length - 1] - x[0]), lo = 0, hi = x.length - 1; while (lo < hi) { var mid = (lo + hi + 1) >> 1; if (x[mid] <= xv) lo = mid; else hi = mid - 1; }
      var ch = box.querySelector('.ch'), sx = cur.X(x[lo]); ch.setAttribute('x1', sx); ch.setAttribute('x2', sx); ch.setAttribute('visibility', 'visible');
      var t = '<b>' + new Date(x[lo] * 864e5).toISOString().slice(0, 10) + '</b>'; cfg.s.forEach(function (se, k) { t += '<br><span style="color:' + COLORS[k] + '">●</span> ' + se.n + ' ' + fm(se.y[lo]); });
      tip.innerHTML = t; tip.style.display = 'block'; var tw = tip.offsetWidth, W = el.clientWidth; tip.style.left = (sx + 14 + tw > W ? Math.max(0, sx - tw - 14) : sx + 14) + 'px'; tip.style.top = (box.offsetTop + 10) + 'px';
    };
    box.onpointerleave = function () { tip.style.display = 'none'; var ch = box.querySelector('.ch'); if (ch) ch.setAttribute('visibility', 'hidden'); };
    el._redraw = draw; draw();
  }
  function drawCharts(r) {
    var x = r.baseNum, nav = Array.prototype.slice.call(r.nav), b50 = Array.prototype.slice.call(r.b50);
    var dd = Array.prototype.map.call(r.dd, function (v) { return v * 100; }), dd50 = Array.prototype.map.call(r.dd50, function (v) { return v * 100; });
    var c1 = $('#tws-ch1'), c2 = $('#tws-ch2');
    var log = c1._log !== false; c1._log = log;
    lineChart(c1, { kind: 'nav', x: x, log: log, title: '淨值', s: [{ n: '這組設定', y: nav }, { n: '0050 含息', y: b50 }] });
    lineChart(c2, { kind: 'dd', x: x, title: '跌幅', s: [{ n: '這組設定', y: dd }, { n: '0050 含息', y: dd50 }] });
    c1._cfg = null;
  }
  function wireToggle() {
    var c1 = $('#tws-ch1');
    c1.querySelectorAll('.vch-sw button').forEach(function (b) {
      b.onclick = function () { c1._log = b.getAttribute('data-s') === 'log'; c1.querySelectorAll('.vch-sw button').forEach(function (z) { z.className = z === b ? 'on' : ''; }); if (last) drawCharts(last); };
    });
  }

  /* ---------------- 啟動 ---------------- */
  function init() {
    buildControls();
    root.querySelector('#tws-controls').addEventListener('change', function (e) { if (e.target.closest && e.target.closest('.tws-fr')) syncRows(); schedule(); });
    root.querySelector('#tws-controls').addEventListener('input', function (e) { if (e.target.type === 'number') schedule(); });
    root.querySelector('#tws-controls').addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('button[data-preset]'); if (b) applyPreset(b.getAttribute('data-preset')); });
    var rz; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { ['#tws-ch1', '#tws-ch2'].forEach(function (s) { var el = $(s); if (el._redraw) el._redraw(); }); }, 150); });
    wireToggle();
    var base = location.pathname.replace(/[^\/]*$/, '');
    try { worker = new Worker('worker.js'); } catch (e) { $('#tws-status').innerHTML = '<span class="tws-warn">這個瀏覽器無法啟動背景運算（Web Worker），請改用較新版的 Chrome、Safari 或 Firefox。</span>'; return; }
    worker.onmessage = onMsg;
    worker.onerror = function (e) { $('#tws-status').innerHTML = '<span class="tws-warn">背景運算出錯：' + esc(e.message || '') + '</span>'; };
    worker.postMessage({ type: 'init', base: location.href.replace(/[^\/]*$/, '') });
    applyPreset('comp');
  }
  init();
})();
