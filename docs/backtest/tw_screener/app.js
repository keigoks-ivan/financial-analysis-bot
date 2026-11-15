/* 台股互動選股回測器：頁面介面。回測在 worker.js，設定與引擎單位的換算在 model.js，這裡只管輸入與顯示。 */

/* 頁首的「其他回測頁」：把注入的 pill-bar 收成一行，點了才展開。
   只靠本頁自己的 CSS（html.tws-js .bt-subnav 預設隱藏）與這段 JS，不改注入的內容，之後重跑注入也不會被洗掉。 */
(function () {
  var nav = document.querySelector('.bt-subnav');
  if (!nav) return;
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'tws-navbtn'; btn.setAttribute('aria-expanded', 'false'); btn.textContent = '其他回測頁 ▾';
  nav.parentNode.insertBefore(btn, nav);
  btn.addEventListener('click', function () {
    var o = nav.classList.toggle('tws-open');
    btn.setAttribute('aria-expanded', String(o)); btn.textContent = o ? '其他回測頁 ▴' : '其他回測頁 ▾';
  });
})();

(function () {
  'use strict';
  var TW = window.TWS, UI = window.TWSUI, $ = function (s, r) { return (r || document).querySelector(s); }, $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var root = $('#tws-app');
  if (!root || !TW || !UI) return;
  var FIDX = TW.FIDX;
  var worker, runId = 0, timer = null, ready = false, info = {}, stats = null, U = UI.defU();
  var cur = null, prev = null, keyById = {}, showPrev = true, lastHash = null, logScale = true;
  var COLORS = ['#2a78d6', '#eb6834'], PREVC = '#a9c3ea';

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function mi(s) { return s.replace('-', '−'); }
  function pct(x, n) { return isFinite(x) ? mi((x * 100).toFixed(n == null ? 1 : n)) + '%' : '—'; }
  function sg(x, n) { return (x >= 0 ? '+' : '−') + Math.abs(x * 100).toFixed(n == null ? 1 : n); }
  function ab(x, n) { return Math.abs(x * 100).toFixed(n == null ? 1 : n); }
  function hasRank(S) { return Object.keys(S.conds).some(function (k) { return S.conds[k].rank; }); }

  /* ---------------- 試驗次數（只存在這位讀者的瀏覽器） ---------------- */
  var TKEY = 'twscreener_trials_v1', mem = {};
  function tload() { try { var s = localStorage.getItem(TKEY); if (s) return JSON.parse(s); } catch (e) { } return Object.keys(mem); }
  function tsave(arr) { try { localStorage.setItem(TKEY, JSON.stringify(arr)); } catch (e) { } arr.forEach(function (k) { mem[k] = 1; }); }
  function hash(s) { var h = 5381; for (var i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0; return (h >>> 0).toString(36); }
  function countTrial(S) {
    var key = hash(JSON.stringify(S)), arr = tload();
    if (arr.indexOf(key) < 0) { arr.push(key); tsave(arr); }
    $('#tws-trials').innerHTML = '你在這個瀏覽器裡已經試過 <b>' + arr.length + '</b> 組不同設定。試越多組，越容易挑到碰巧好看的結果，最後那組的績效不能直接當成預期。';
  }

  /* ---------------- 左欄：設定 ---------------- */
  var TIPS = {
    n: '每次換股時持有幾檔，等分或照分數配權（見進階設定的「資金怎麼分」）。',
    freq: '每月＝每個月換一次；每季＝只在 3、6、9、12 月換。',
    liq: '先把全市場股票依最近 60 日平均成交額由大到小排，只留前面這個比例。100 ＝不限。比例越小，池子裡的股票越好買賣。',
    mkt: '池子只放上市、只放上櫃，或兩邊都放。',
    basis: '排名時拿誰來比。「在池子裡比」：只跟通過上面池子與門檻的股票比，最好的得 1 分。「在全市場比」：跟當天全部有這項資料的股票比，池子裡的股票不一定拿得到高分。FinLab 四因子複合用全市場。',
    missing: '某檔股票缺少某個排名項目的資料（例如剛上市沒有 120 日漲幅、虧損的沒有本益比）。「不選」：這檔直接不入選。「這項給 0 分」：這一項當最差，其他項照算。門檻條件缺資料的一律不選。',
    wp: '選出來的股票各買多少。平均分：每檔一樣多。其餘三種：權重跟總分成正比，分數越高買越多；平方與三次方會讓高分的比重更大。總分是各項排名分數（最好 1、最差接近 0）依權重平均，介於 0 到 1。',
    keep: '每次換股時，原本持有的股票只要總分排名還在前這個名次內就繼續抱，空出來的名額才由排名最前面的新股補上。這個數字要比持股檔數大才有緩衝。0 ＝每次都全部重選。',
    timing: '「月底決定、隔天買」：月底最後一個交易日收盤後決定名單，下一個交易日收盤價買。「每月 15 日左右決定並買」：月底之後第 14 天（含）以前的最後一個交易日決定名單，下一個交易日收盤價買，這時上個月營收已經公布（FinLab 的 offset 14D）。「月底決定、15 日左右才買」：月底最後一個交易日決定名單，等到月底後第 14 天才買，中間維持原本的持股。換股頻率選每季時，這裡的「月底」指 3、6、9、12 月底。',
    mrank: '只留當天全市場市值排名在前面這個名次內的股票，排名用全市場，不是池子內。0 ＝不限。',
    mmin: '市值低於這個數字的不選，單位是億元。0 ＝不限。',
    fee: '手續費買進與賣出各收一次。預設 0.1425% 是法定費率，沒有打折。',
    tax: '證交稅只有賣出時收。預設 0.3%。',
    start: '預設從資料起點 2014-01-02 起算，第一次成交在之後。用到「投信買超強度」會自動從 2015-02 起。',
    end: '留空＝算到資料截止日。',
    draws: '隨機對照：每期從同一個池子隨機抽同樣檔數、等權，重複這麼多次。次數越多，範圍越穩，也越慢。'
  };
  var MODES_HELP = '排名：把池子裡的股票依這一項由好到壞排隊，最好的得 1 分、最差的接近 0 分；有好幾項排名時，依權重平均成總分，總分最高的前幾檔入選。門檻：不符合就不進池子。同一項可以兩個都用。';

  function opt(v, t) { return '<option value="' + v + '">' + t + '</option>'; }
  function fld(id, label, ctl, tip) {
    return '<div class="tws-f"><div class="tws-fl"><label for="' + id + '">' + label + '</label><button type="button" class="tws-i" data-tip="tip-' + id + '" aria-label="說明">ⓘ</button></div><div class="tws-fc">' + ctl + '</div>' +
      '<div class="tws-tipbox" id="tip-' + id + '" hidden>' + esc(tip) + '</div></div>';
  }

  function buildLeft() {
    var P = UI.PRESET_BTNS.map(function (b) { return '<button type="button" class="tws-btn" data-preset="' + b[0] + '">' + esc(b[1]) + '</button>'; }).join('');
    var common =
      fld('c-n', '持股檔數', '<input id="c-n" type="number" min="1" max="100" step="1"> 檔', TIPS.n) +
      fld('c-freq', '換股頻率', '<select id="c-freq">' + opt('M', '每月') + opt('Q', '每季（3、6、9、12 月）') + '</select>', TIPS.freq) +
      fld('c-liq', '池子：成交額前', '<input id="c-liq" type="number" min="5" max="100" step="5"> %<span class="tws-hint">100 ＝不限</span>', TIPS.liq) +
      fld('c-mkt', '池子：市場', '<select id="c-mkt">' + opt('all', '上市＋上櫃') + opt('TWSE', '只上市') + opt('TPEX', '只上櫃') + '</select>', TIPS.mkt);
    var adv =
      fld('c-basis', '排名在哪裡比', '<select id="c-basis">' + opt('pool', '在池子裡比') + opt('all', '在全市場比') + '</select>', TIPS.basis) +
      fld('c-miss', '缺資料的股票', '<select id="c-miss">' + opt('drop', '不選') + opt('zero', '這項給 0 分') + '</select>', TIPS.missing) +
      fld('c-wp', '資金怎麼分', '<select id="c-wp">' + opt('0', '平均分') + opt('1', '分數高的多分') + opt('2', '分數高的多分很多（平方）') + opt('3', '分數高的多分更多（三次方）') + '</select>', TIPS.wp) +
      fld('c-keep', '原本的持股掉出前幾名才賣', '<input id="c-keep" type="number" min="0" max="500" step="5"> 名<span class="tws-hint">0 ＝每次全換</span>', TIPS.keep) +
      fld('c-timing', '換股時間點', '<select id="c-timing">' + opt('me', '月底決定、隔天買') + opt('off14', '每月 15 日左右決定並買（營收公布後）') + opt('off14frozen', '月底決定、15 日左右才買') + '</select>', TIPS.timing) +
      fld('c-mrank', '全市場市值排名前', '<input id="c-mrank" type="number" min="0" step="50"> 名<span class="tws-hint">0 ＝不限</span>', TIPS.mrank) +
      fld('c-mmin', '市值下限', '<input id="c-mmin" type="number" min="0" step="10"> 億元<span class="tws-hint">0 ＝不限</span>', TIPS.mmin) +
      fld('c-fee', '手續費（買賣各一次）', '<input id="c-fee" type="number" min="0" step="0.005"> %', TIPS.fee) +
      fld('c-tax', '證交稅（只有賣出）', '<input id="c-tax" type="number" min="0" step="0.05"> %', TIPS.tax) +
      fld('c-start', '起日', '<input id="c-start" type="date" min="2014-01-01">', TIPS.start) +
      fld('c-end', '訖日', '<input id="c-end" type="date" min="2014-02-01">', TIPS.end) +
      fld('c-draws', '隨機對照次數', '<select id="c-draws">' + opt('200', '200') + opt('500', '500') + opt('1000', '1000') + '</select>', TIPS.draws);
    $('#tws-left').innerHTML =
      '<div class="tws-sec"><div class="tws-h">起點</div><div class="tws-row" id="tws-presets">' + P + '</div>' +
      '<div class="tws-row"><button type="button" class="tws-btn tws-ghost" id="tws-copy">複製連結</button><span class="tws-muted" id="tws-copied" aria-live="polite"></span></div>' +
      '<p class="tws-note" id="tws-pnote"></p></div>' +
      '<div class="tws-sec"><div class="tws-h">條件<span class="tws-hn" id="tws-cn"></span><button type="button" class="tws-i" data-tip="tip-conds" aria-label="說明">ⓘ</button></div>' +
      '<div class="tws-tipbox" id="tip-conds" hidden>' + esc(MODES_HELP) + '</div>' +
      '<div id="tws-conds"></div><div class="tws-empty" id="tws-cempty">還沒有條件。按下面的「＋加條件」，至少加一項排名。</div>' +
      '<div class="tws-addrow"><button type="button" class="tws-btn tws-add" id="tws-addbtn" aria-expanded="false">＋加條件</button></div><div class="tws-menu" id="tws-menu" hidden></div></div>' +
      '<div class="tws-sec"><div class="tws-h">常用設定</div><div class="tws-fs">' + common + '</div><p class="tws-desc" id="tws-desc"></p></div>' +
      '<details class="tws-adv" id="tws-adv"><summary>進階設定<span class="tws-hn" id="tws-advn"></span></summary><div class="tws-fs">' + adv + '</div></details>' +
      '<div class="tws-muted" id="tws-load"></div><div id="tws-trials"></div>';
  }

  function rowHtml(u) {
    var f = FIDX[u.k], tag = '';
    var tipTxt = '<p>' + esc(f.def) + '</p><p class="tws-muted">資料從 ' + esc(f.start) + ' 起。' + (f.supp ? '這項用財報、營收、股利或成交資料自己算，哪一天起算「已公布」照上面的定義，跟官方或其他網站的數字可能有小差異。' : '') + '</p>';
    var h = '<div class="tws-cr" data-k="' + u.k + '"><div class="tws-crh"><b>' + esc(UI.nameOf(u.k)) + '</b>' + tag +
      '<span class="tws-sp"></span><button type="button" class="tws-i" data-tip="tip-r-' + u.k + '" aria-label="定義">ⓘ</button><button type="button" class="tws-x" data-del="' + u.k + '" aria-label="移除這項條件">✕</button></div><div class="tws-crb">';
    if (u.rank) h += '<span class="tws-ch" data-m="rank"><em>排名</em><select class="dir"><option value="hi">高的好</option><option value="lo">低的好</option></select><span class="tws-pl">權重</span><input class="w" type="number" min="0" step="0.5"><button type="button" class="tws-cx" data-off="rank" aria-label="不用排名">×</button></span>';
    if (u.filter) h += '<span class="tws-ch" data-m="filter"><em>門檻</em><select class="op"><option value="&gt;">高於</option><option value="&lt;">低於</option></select><input class="val" type="number" step="any"><span class="tws-u">' + esc(f.unit) + '</span><button type="button" class="tws-cx" data-off="filter" aria-label="不用門檻">×</button></span>';
    if (!u.rank) h += '<button type="button" class="tws-lnk" data-on="rank" data-k="' + u.k + '">＋排名</button>';
    if (!u.filter) h += '<button type="button" class="tws-lnk" data-on="filter" data-k="' + u.k + '">＋門檻</button>';
    h += '</div>' + (u.filter ? '<div class="tws-stat" data-st="' + u.k + '"></div>' : '') + '<div class="tws-tipbox" id="tip-r-' + u.k + '" hidden>' + tipTxt + '</div></div>';
    return h;
  }
  function renderConds() {
    var box = $('#tws-conds'), openTips = $$('.tws-tipbox:not([hidden])', box).map(function (x) { return x.id; });
    box.innerHTML = U.conds.map(rowHtml).join('');
    $$('.tws-cr', box).forEach(function (row) {
      var u = UI.findC(U, row.getAttribute('data-k'));
      if (u.rank) { $('.dir', row).value = u.rank.dir; $('.w', row).value = u.rank.w; }
      if (u.filter) { $('.op', row).value = u.filter.op; $('.val', row).value = isFinite(u.filter.val) ? u.filter.val : ''; }
    });
    openTips.forEach(function (id) { var el = document.getElementById(id); if (el) el.hidden = false; });
    $('#tws-cempty').hidden = U.conds.length > 0;
    $('#tws-cn').textContent = U.conds.length ? '（' + U.conds.length + ' 項）' : '';
    fillStats(); if (!$('#tws-menu').hidden) renderMenu();
  }
  function nf(v) { var a = Math.abs(v), s = a >= 1000 ? Math.round(v).toLocaleString('en-US') : a >= 100 ? v.toFixed(0) : a >= 10 ? v.toFixed(1) : v.toFixed(2); return mi(s); }
  function fu(f, v) { return f.unit === '%' ? nf(v) + '%' : f.unit === '倍' ? nf(v) + ' 倍' : nf(v) + ' 億'; }
  function fillStats() {
    $$('.tws-stat').forEach(function (el) {
      var k = el.getAttribute('data-st'), f = FIDX[k], q = stats && stats.q[k];
      el.textContent = q ? '最新一期（' + stats.date + '）全市場：中位數 ' + fu(f, q[1]) + '、中間一半 ' + nf(q[0]) + '～' + fu(f, q[2]) + '。' : (stats ? '' : '資料載入完成後，這裡會顯示全市場的數字範圍。');
    });
  }
  function renderMenu() {
    var h = '';
    UI.CATS.forEach(function (c) {
      h += '<div class="tws-mc"><div class="tws-mt">' + esc(c[0]) + '</div>';
      c[1].forEach(function (k) {
        var u = UI.findC(U, k);
        h += '<div class="tws-mi"><span>' + esc(UI.nameOf(k)) + '</span><span class="tws-mb"><button type="button" data-add="' + k + '" data-m="rank"' + (u && u.rank ? ' disabled' : '') + '>排名</button><button type="button" data-add="' + k + '" data-m="filter"' + (u && u.filter ? ' disabled' : '') + '>門檻</button></span></div>';
      });
      h += '</div>';
    });
    $('#tws-menu').innerHTML = h;
  }
  function addCond(k, mode) {
    var f = FIDX[k], u = UI.findC(U, k);
    if (!u) { u = { k: k, filter: null, rank: null }; U.conds.push(u); }
    if (mode === 'rank' && !u.rank) u.rank = { dir: f.dir, w: 1 };
    if (mode === 'filter' && !u.filter) { var t = UI.TH[k]; u.filter = { op: t[0], val: t[1] }; }
    renderConds(); after(true);
  }
  function offCond(k, mode) {
    var u = UI.findC(U, k); if (!u) return;
    u[mode] = null;
    if (!u.rank && !u.filter) U.conds = U.conds.filter(function (x) { return x !== u; });
    renderConds(); after(true);
  }

  function writeCommon() {
    var set = function (id, v) { $('#' + id).value = v; };
    set('c-n', U.n); set('c-freq', U.freq); set('c-liq', U.liq); set('c-mkt', U.market); set('c-basis', U.basis); set('c-miss', U.missing); set('c-wp', U.wp);
    set('c-keep', U.keep); set('c-timing', U.timing); set('c-mrank', U.mrank); set('c-mmin', U.mmin); set('c-fee', U.fee); set('c-tax', U.tax);
    set('c-start', U.start); set('c-end', U.end); set('c-draws', U.draws);
  }
  function readCommon() {
    var D = UI.defU(), nv = function (id, d) { var v = parseFloat($('#' + id).value); return isFinite(v) ? v : d; };
    U.n = nv('c-n', D.n); U.freq = $('#c-freq').value; U.liq = nv('c-liq', D.liq); U.market = $('#c-mkt').value; U.basis = $('#c-basis').value; U.missing = $('#c-miss').value;
    U.wp = +$('#c-wp').value; U.keep = nv('c-keep', 0); U.timing = $('#c-timing').value; U.mrank = nv('c-mrank', 0); U.mmin = nv('c-mmin', 0);
    U.fee = nv('c-fee', D.fee); U.tax = nv('c-tax', D.tax); U.start = $('#c-start').value || D.start; U.end = $('#c-end').value || ''; U.draws = +$('#c-draws').value || 200;
  }
  function readRow(row) {
    var u = UI.findC(U, row.getAttribute('data-k')); if (!u) return;
    if (u.rank) { var w = parseFloat($('.w', row).value); u.rank = { dir: $('.dir', row).value, w: isFinite(w) ? w : 0 }; }
    if (u.filter) u.filter = { op: $('.op', row).value, val: parseFloat($('.val', row).value) };
  }

  /* 設定改了之後：更新起點按鈕、說明、網址，並排程重算 */
  function after(run) {
    var wp = UI.whichPreset(U), D = UI.defU(), n = 0;
    $$('#tws-presets .tws-btn').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-preset') === wp); });
    var note = $('#tws-pnote'); note.textContent = wp ? UI.PRESET_NOTE[wp] : ''; note.hidden = !wp;
    ['basis', 'missing', 'wp', 'keep', 'timing', 'mrank', 'mmin', 'fee', 'tax', 'start', 'end', 'draws'].forEach(function (a) { if (String(U[a]) !== String(D[a])) n++; });
    $('#tws-advn').textContent = n ? '（已改 ' + n + ' 項）' : '';
    var ds = $('#tws-desc'); ds.textContent = wp ? '' : UI.describe(U); ds.hidden = !!wp;
    syncHash();
    if (run) schedule();
  }
  function syncHash() {
    var h = '#' + UI.encode(U);
    if (h === lastHash) return;
    lastHash = h;
    try { history.replaceState(null, '', h); } catch (e) { }
  }
  function applyU(next) { U = next; writeCommon(); renderConds(); after(true); }

  /* ---------------- 執行 ---------------- */
  function schedule() { clearTimeout(timer); timer = setTimeout(go, 450); }
  function go() {
    var S = UI.toSettings(U);
    runId++;
    if (!hasRank(S)) { cur = null; renderConcl(); $('#tws-res').hidden = true; $('#tws-right').classList.remove('stale'); return; }
    countTrial(S);
    keyById[runId] = JSON.stringify(S);
    $('#tws-right').classList.add('stale');
    if (!cur) renderConcl();
    worker.postMessage({ type: 'run', id: runId, S: S, draws: +U.draws });
  }

  function onMsg(e) {
    var m = e.data;
    if (m.type === 'meta') { info = m; }
    else if (m.type === 'progress') {
      $('#tws-load').innerHTML = (m.stage === 'f' ? '載入因子資料' : '背景載入每日報酬') + '：' + m.done + ' / ' + m.total + '（已傳輸 ' + (m.bytes / 1048576).toFixed(1) + ' MB）';
    }
    else if (m.type === 'factors-ready') { info.factorsMs = m.ms; }
    else if (m.type === 'ready') {
      ready = true; info.loadMs = m.ms; info.bytes = m.bytes;
      $('#tws-load').innerHTML = '資料已載入：' + (m.bytes / 1048576).toFixed(1) + ' MB，' + (m.ms / 1000).toFixed(1) + ' 秒。';
    }
    else if (m.type === 'stats') { stats = m; fillStats(); }
    else if (m.type === 'result' && m.id === runId) {
      $('#tws-right').classList.remove('stale');
      if (m.empty) { cur = null; renderConcl('empty'); $('#tws-res').hidden = true; return; }
      var key = keyById[m.id];
      if (cur && cur.key !== key) prev = { key: cur.key, r: cur.r };
      cur = { key: key, r: m.r, rc: null };
      render(m.r); renderConcl();
    }
    else if (m.type === 'rc' && m.id === runId) { if (cur) { cur.rc = m; renderConcl(); } }
    else if (m.type === 'error') { $('#tws-concl').innerHTML = '<div class="tws-cc"><span class="tws-warn">錯誤：' + esc(m.msg) + '</span></div>'; }
  }

  /* ---------------- 結論卡 ---------------- */
  function verdict(rc) {
    if (!rc || !rc.done) return { k: 'calc', short: '計算中', html: '<b>計算中</b>' + (rc ? '（已抽 ' + rc.n + ' ／ ' + rc.total + ' 次）' : '') };
    var q = rc.summ.nocost, rg = '（範圍 ' + sg(q.lo) + ' 到 ' + sg(q.hi) + '）';
    if (q.lo > 0) return { k: 'good', short: '有', html: '<b class="ok">有</b>：比同一池隨機挑多 ' + ab(q.med) + ' 個百分點' + rg };
    if (q.hi < 0) return { k: 'bad', short: '比隨機差', html: '<b class="no">比隨機挑還差</b>：少 ' + ab(q.med) + ' 個百分點' + rg };
    return { k: 'none', short: '看不出來', html: '<b class="mid">看不出來</b>：範圍含 0' + rg };
  }
  function kpiRow(name, m) {
    return '<tr><td class="lbl">' + name + '</td><td class="num">' + pct(m.ann) + '</td><td class="num">' + (isFinite(m.sharpe) ? m.sharpe.toFixed(2) : '—') + '</td><td class="num ng">' + pct(m.mdd) + '</td><td class="num">' + m.uwYears.toFixed(1) + ' 年</td><td class="num">' + m.total.toFixed(2) + ' 倍</td></tr>';
  }
  function rcTable(m) {
    var s = m.summ, f = function (x) { return (x >= 0 ? '+' : '−') + Math.abs(x * 100).toFixed(1); };
    var row = function (name, q) { return '<tr><td class="lbl">' + name + '</td><td class="num">' + f(q.med) + '</td><td class="num">' + f(q.lo) + ' 到 ' + f(q.hi) + '</td><td class="num">' + (q.lo > 0 ? '不含 0，策略較好' : q.hi < 0 ? '不含 0，策略較差' : '含 0') + '</td></tr>'; };
    return '<p class="tws-muted">' + (m.done ? '已抽 ' + m.total + ' 次' : '已抽 ' + m.n + ' ／ ' + m.total + ' 次，還在跑') + '。每一期從同一個池子隨機抽同樣檔數、等權，換股日與成本一樣。下表是「這組設定的年化減隨機組的年化」，單位是個百分點。</p>' +
      '<div class="scroll"><table><thead><tr><th></th><th class="num">差的中位數</th><th class="num">2.5% 到 97.5% 範圍</th><th class="num">範圍有沒有 0</th></tr></thead><tbody>' +
      row('不扣成本（結論用這個）', s.nocost) + row('扣成本', s.cost) + '</tbody></table></div>' +
      '<p class="table-note">隨機組每期整批換股，換手比多數策略高，扣成本版的差距會偏大。</p>';
  }
  function tipI(id) { return ' <button type="button" class="tws-i" data-tip="' + id + '" aria-label="說明">ⓘ</button>'; }
  function prevOk() { return !!(prev && cur && prev.key !== cur.key); }
  function renderConcl(state) {
    var box = $('#tws-concl'), bar = $('#tws-bar');
    if (!cur) {
      var noRank = !hasRank(UI.toSettings(U));
      var msg = state === 'empty' ? '這組條件在這段期間每一期的池子都是空的，沒有名單。放寬門檻，或把池子的成交額比例調高。' :
        noRank ? '還沒有排名條件。到左邊按「＋加條件」，至少加一項排名，或按上面的起點按鈕。' : ready ? '計算中…' : '資料載入中，載完會自動計算。第一次要下載約 11 MB，之後瀏覽器會快取。';
      var warn = state === 'empty' || noRank;
      box.innerHTML = '<div class="tws-cc"><div class="tws-cc-h">結論</div><p class="tws-cc-w' + (warn ? ' tws-warn' : '') + '">' + msg + '</p></div>';
      bar.innerHTML = '<span class="tws-bm' + (warn ? ' tws-warn' : '') + '">' + msg + '</span>'; bar.classList.add('warm');
      return;
    }
    var r = cur.r, v = verdict(cur.rc), sc = r.scale, d50 = r.m.ann - r.mb.ann;
    var h = '<div class="tws-cc"><div class="tws-cc-h">結論</div><ul class="tws-cc-l">' +
      '<li class="big">年化 <b>' + pct(r.m.ann) + '</b>（0050：' + pct(r.mb.ann) + '）；最大跌幅 <b>' + pct(r.m.mdd) + '</b>（0050：' + pct(r.mb.mdd) + '）</li>' +
      '<li>排序有沒有用：' + v.html + tipI('tip-c-rc') + '</li>' +
      '<li>跌幅壓到 −20% 後：年化 <b>' + pct(sc.ann) + '</b>，0050 為 ' + pct(sc.ann50) + tipI('tip-c-sc') + '</li>';
    if (prevOk()) {
      var pa = prev.r.m.ann, pm = prev.r.m.mdd, dA = r.m.ann - pa, dM = r.m.mdd - pm;
      h += '<li>跟上一組比：年化' + (dA >= 0 ? '高 ' : '低 ') + ab(dA) + ' 個百分點（上一組 ' + pct(pa) + '），最大跌幅' + (dM >= 0 ? '淺 ' : '深 ') + ab(dM) + ' 個百分點（上一組 ' + pct(pm) + '）</li>';
    }
    h += '</ul>' +
      '<div class="tws-tipbox" id="tip-c-rc" hidden>每期從同一個池子隨機抽同樣檔數、等權，換股日與成本一樣，重複幾百次。用「不扣成本」的年化比：這組設定減隨機組，取 2.5% 到 97.5% 的範圍。整段大於 0，代表排序方式有加分；整段小於 0，代表比隨機挑還差；含 0，代表看不出比在同一個池子裡隨便挑好。</div>' +
      '<div class="tws-tipbox" id="tip-c-sc" hidden>每天的報酬乘一個固定倍數（這組 ' + sc.m.toFixed(2) + ' 倍、0050 ' + sc.m50.toFixed(2) + ' 倍），其餘放現金不計息，讓最大跌幅剛好 −20%。多數選股策略的最大跌幅在 −30% 到 −45%，這樣處理之後才能跟 0050 在同樣的跌幅下比年化。</div>' +
      '<div class="tws-cc-s">期間 ' + r.firstTrade + '（第一次成交）到 ' + r.endDay + '，共 ' + r.periods + ' 次換股，平均池子 ' + Math.round(r.poolAvg) + ' 檔。' +
      (r.S.conds.trust ? '用到投信買超強度，判斷日自動從 2015-01-30 起。' : '') + (r.tieShort ? '有 ' + r.tieShort + ' 期因為並列在邊界，入選檔數少於設定值。' : '') + '</div>' +
      '<details class="tws-more"><summary>更多數字：夏普、最長水下、不扣成本、隨機對照明細</summary>' +
      '<div class="scroll"><table><thead><tr><th></th><th class="num">年化（日曆年）</th><th class="num">日夏普</th><th class="num">最大跌幅</th><th class="num">最長水下</th><th class="num">累積</th></tr></thead><tbody>' +
      kpiRow('這組設定（扣成本）', r.m) + kpiRow('同一組、不扣成本', r.m0) + kpiRow('0050 含息', r.mb) + '</tbody></table></div>' +
      (cur.rc ? rcTable(cur.rc) : '<p class="tws-muted">同池隨機對照計算中…</p>') + '</details></div>';
    var more = $('.tws-more', box), open = more && more.open, openTips = $$('.tws-tipbox:not([hidden])', box).map(function (x) { return x.id; });
    box.innerHTML = h;
    if (open) $('.tws-more', box).open = true;
    openTips.forEach(function (id) { var el = document.getElementById(id); if (el) el.hidden = false; });
    bar.classList.remove('warm');
    bar.innerHTML = '<span class="tws-bc"><i>年化</i><b>' + pct(r.m.ann) + '</b></span><span class="tws-bc"><i>最大跌幅</i><b>' + pct(r.m.mdd) + '</b></span>' +
      '<span class="tws-bc"><i>對 0050</i><b>' + sg(d50) + ' 點</b></span><span class="tws-bc"><i>排序有沒有用</i><b class="v-' + v.k + '">' + v.short + '</b></span>';
  }

  /* ---------------- 右欄：圖表與名單 ---------------- */
  function render(r) {
    $('#tws-res').hidden = false;
    drawCharts(r);
    var rows = '', by50 = {}; r.yearly50.forEach(function (y) { by50[y.y] = y.ret; });
    r.yearly.forEach(function (y) {
      var d = y.ret - by50[y.y];
      rows += '<tr><td class="lbl">' + y.y + (y.partial ? '（部分年度）' : '') + '</td><td class="num ' + (y.ret < 0 ? 'ng' : '') + '">' + pct(y.ret) + '</td><td class="num ' + (by50[y.y] < 0 ? 'ng' : '') + '">' + pct(by50[y.y]) + '</td><td class="num ' + (d < 0 ? 'ng' : '') + '">' + (d >= 0 ? '+' : '') + mi((d * 100).toFixed(1)) + '</td></tr>';
    });
    $('#tws-yearly').innerHTML = '<table class="narrow"><thead><tr><th>年</th><th class="num">這組設定</th><th class="num">0050 含息</th><th class="num">差（點）</th></tr></thead><tbody>' + rows + '</tbody></table>';
    renderPicks(r);
    $('#tws-turn').innerHTML = '年換手率 <b>' + (r.turnover * 100).toFixed(0) + '%</b>；成本（手續費與證交稅）每年吃掉 <b>' + (r.costPP * 100).toFixed(1) + ' 個百分點</b>的年化。';
    $('#tws-cap').innerHTML = '假設帳戶 1,000 萬元，' + r.capacity.n + ' 筆買進裡有 ' + r.capacity.hit + ' 筆（' + (r.capacity.share * 100).toFixed(1) + '%）超過該股 60 日均成交額的 5%。這裡用判斷日的 60 日均額代替成交日當天成交額。';
  }

  function renderPicks(r) {
    var ps = r.picks, lp = ps[ps.length - 1];
    function tbl(p) {
      return '<div class="scroll"><table class="narrow"><thead><tr><th>代號</th><th>名稱</th><th class="num">權重</th><th class="num">分數</th><th class="num">市值（億）</th></tr></thead><tbody>' +
        p.rows.map(function (x) { return '<tr><td>' + x[0] + '</td><td>' + esc(x[1]) + '</td><td class="num">' + (x[2] * 100).toFixed(1) + '%</td><td class="num">' + x[3].toFixed(3) + '</td><td class="num">' + (isFinite(x[4]) ? Math.round(x[4]).toLocaleString() : '—') + '</td></tr>'; }).join('') + '</tbody></table></div>';
    }
    $('#tws-latest').innerHTML = '<div class="tws-latest"><b>最新一期</b>：依 ' + lp.jd + ' 的資料判斷、' + lp.tr + ' 收盤成交，池子 ' + lp.poolN + ' 檔、選 ' + lp.rows.length + ' 檔。這是資料截止日（' + (info.dataEnd || '') + '）前最後一次換股，不是今天的建議。' + tbl(lp) + '</div>';
    var html = '';
    for (var i = ps.length - 2; i >= 0; i--) html += '<details data-i="' + i + '"><summary>' + ps[i].jd + ' 判斷，' + ps[i].tr + ' 成交（' + ps[i].rows.length + ' 檔）</summary><div class="tws-ph"></div></details>';
    $('#tws-hist').innerHTML = html;
    $('#tws-hist').onclick = function (e) {
      var d = e.target.closest ? e.target.closest('summary') : null; if (!d) return;
      var det = d.parentNode, ph = det.querySelector('.tws-ph');
      if (ph && !ph.innerHTML) ph.innerHTML = tbl(ps[+det.getAttribute('data-i')]);
    };
  }

  /* ---------------- 圖（每條線可以有自己的日期軸，上一組的起點可能不同） ---------------- */
  function lineChart(el, cfg) {
    var box = el.querySelector('.vch-plot'), tip = el.querySelector('.vch-tip'), ML = cfg.kind === 'nav' ? 44 : 50, MR = 12, MT = 8, MB = 22, LOG = cfg.kind === 'nav' && cfg.log, cv = null;
    function xsOf(se) { return se.x || cfg.x; }
    function tk(lo, hi, n) { var rg = (hi - lo) || 1, s = Math.pow(10, Math.floor(Math.log10(rg / n))), e = rg / n / s; s *= e < 1.5 ? 1 : e < 3 ? 2 : e < 7 ? 5 : 10; var t = []; for (var v = Math.ceil(lo / s) * s; v <= hi + 1e-9; v += s) t.push(+v.toFixed(6)); return t; }
    function fm(v) { if (v == null) return '—'; return cfg.kind === 'nav' ? (v >= 100 ? v.toFixed(0) : v >= 10 ? v.toFixed(1) : v.toFixed(2)) + ' 倍' : mi(v.toFixed(1)) + '%'; }
    function draw() {
      var w = box.clientWidth; if (!w) return; var hh = w < 520 ? 210 : 260, all = [], x0 = Infinity, x1 = -Infinity;
      cfg.s.forEach(function (s) { var xs = xsOf(s); x0 = Math.min(x0, xs[0]); x1 = Math.max(x1, xs[xs.length - 1]); for (var i = 0; i < s.y.length; i += 1) { var v = s.y[i]; if (v != null) all.push(LOG ? Math.log10(v) : v); } });
      var lo = Math.min.apply(null, all), hi = Math.max.apply(null, all), t;
      if (cfg.kind === 'dd') hi = Math.max(hi, 0);
      if (LOG) { t = []; [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500].forEach(function (m) { var v = Math.log10(m); if (v >= lo - .001 && v <= hi + .001) t.push(v); }); if (!t.length) t = [0]; lo = Math.min(lo, t[0]); hi = Math.max(hi, t[t.length - 1]); }
      else { t = tk(lo, hi, 4); lo = Math.min(lo, t[0]); hi = Math.max(hi, t[t.length - 1]); }
      if (hi === lo) hi = lo + 1;
      var X = function (v) { return ML + (v - x0) / (x1 - x0) * (w - ML - MR); }, Y = function (v) { return MT + (hi - v) / (hi - lo) * (hh - MT - MB); }, s = '';
      t.forEach(function (v) { var lab = LOG ? fm(Math.pow(10, v)).replace(' 倍', '×') : fm(v); s += '<line x1="' + ML + '" x2="' + (w - MR) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" stroke="#e5e7eb"/><text x="' + (ML - 6) + '" y="' + (Y(v) + 4) + '" text-anchor="end">' + lab + '</text>'; });
      var y0 = new Date(x0 * 864e5).getUTCFullYear(), y1 = new Date(x1 * 864e5).getUTCFullYear(), step = Math.max(1, Math.ceil((y1 - y0 + 1) * 46 / (w - ML - MR)));
      for (var y = y0 + 1; y <= y1; y++) { if ((y - y0 - 1) % step) continue; var px = X(Date.UTC(y, 0, 1) / 864e5); s += '<line x1="' + px + '" x2="' + px + '" y1="' + (hh - MB) + '" y2="' + (hh - MB + 4) + '" stroke="#9ca3af"/><text x="' + px + '" y="' + (hh - 6) + '" text-anchor="middle">' + y + '</text>'; }
      cfg.s.slice().reverse().forEach(function (se, ri) {
        var i = cfg.s.length - 1 - ri, xs = xsOf(se), d = '', on = false, stp = Math.max(1, Math.floor(xs.length / (w * 1.5)));
        for (var k = 0; k < xs.length; k += stp) { var v = se.y[k]; if (v == null) { on = false; continue; } d += (on ? 'L' : 'M') + X(xs[k]).toFixed(1) + ' ' + Y(LOG ? Math.log10(v) : v).toFixed(1); on = true; }
        if (cfg.kind === 'dd' && i === 0) s += '<path d="' + d + 'L' + X(xs[xs.length - 1]) + ' ' + Y(0) + 'L' + X(xs[0]) + ' ' + Y(0) + 'Z" fill="' + se.c + '" fill-opacity=".12" stroke="none"/>';
        s += '<path d="' + d + '" fill="none" stroke="' + se.c + '" stroke-width="' + (i === 0 ? 1.9 : se.faint ? 1.6 : 1.4) + '" stroke-linejoin="round"/>';
      });
      box.innerHTML = '<svg height="' + hh + '" viewBox="0 0 ' + w + ' ' + hh + '" role="img" aria-label="' + esc(cfg.title) + '">' + s + '<line class="ch" y1="' + MT + '" y2="' + (hh - MB) + '" stroke="#6b7280" visibility="hidden"/></svg>';
      cv = { X: X, w: w, x0: x0, x1: x1 };
    }
    function at(xs, xv) { if (xv < xs[0] || xv > xs[xs.length - 1]) return -1; var lo = 0, hi = xs.length - 1; while (lo < hi) { var mid = (lo + hi + 1) >> 1; if (xs[mid] <= xv) lo = mid; else hi = mid - 1; } return lo; }
    box.onpointermove = function (e) {
      if (!cv) return; var rc = box.getBoundingClientRect(), px = e.clientX - rc.left; if (px < ML || px > cv.w - MR) { tip.style.display = 'none'; return; }
      var xv = cv.x0 + (px - ML) / (cv.w - ML - MR) * (cv.x1 - cv.x0), sx = cv.X(xv);
      var ch = box.querySelector('.ch'); ch.setAttribute('x1', sx); ch.setAttribute('x2', sx); ch.setAttribute('visibility', 'visible');
      var t = '<b>' + new Date(Math.round(xv) * 864e5).toISOString().slice(0, 10) + '</b>';
      cfg.s.forEach(function (se) { var j = at(xsOf(se), xv); t += '<br><span style="color:' + se.c + '">●</span> ' + se.n + ' ' + (j < 0 ? '—' : fm(se.y[j])); });
      tip.innerHTML = t; tip.style.display = 'block'; var tw = tip.offsetWidth, W = el.clientWidth; tip.style.left = (sx + 14 + tw > W ? Math.max(0, sx - tw - 14) : sx + 14) + 'px'; tip.style.top = (box.offsetTop + 10) + 'px';
    };
    box.onpointerleave = function () { tip.style.display = 'none'; var ch = box.querySelector('.ch'); if (ch) ch.setAttribute('visibility', 'hidden'); };
    el._redraw = draw; draw();
  }
  function drawCharts(r) {
    if (!r) return;
    var x = r.baseNum, nav = Array.prototype.slice.call(r.nav), b50 = Array.prototype.slice.call(r.b50);
    var dd = Array.prototype.map.call(r.dd, function (v) { return v * 100; }), dd50 = Array.prototype.map.call(r.dd50, function (v) { return v * 100; });
    var s1 = [{ n: '這組設定', y: nav, c: COLORS[0] }, { n: '0050 含息', y: b50, c: COLORS[1] }];
    $('#tws-prevleg').hidden = !prevOk();
    if (prevOk() && showPrev) s1.push({ n: '上一組', y: Array.prototype.slice.call(prev.r.nav), x: prev.r.baseNum, c: PREVC, faint: true });
    lineChart($('#tws-ch1'), { kind: 'nav', x: x, log: logScale, title: '淨值', s: s1 });
    lineChart($('#tws-ch2'), { kind: 'dd', x: x, title: '跌幅', s: [{ n: '這組設定', y: dd, c: COLORS[0] }, { n: '0050 含息', y: dd50, c: COLORS[1] }] });
  }

  /* ---------------- 複製連結、說明、事件 ---------------- */
  function copyLink() {
    syncHash();
    var url = location.href, ok = function () { var c = $('#tws-copied'); c.textContent = '已複製'; setTimeout(function () { c.textContent = ''; }, 1800); };
    function fallback() {
      var ta = document.createElement('textarea'); ta.value = url; ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.appendChild(ta); ta.select();
      var done = false; try { done = document.execCommand('copy'); } catch (e) { } document.body.removeChild(ta);
      if (done) ok(); else { var c = $('#tws-copied'); c.innerHTML = '請手動複製：<input type="text" readonly value="' + esc(url) + '" size="28">'; var inp = $('input', c); inp.focus(); inp.select(); }
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(ok, fallback); else fallback();
  }

  function init() {
    buildLeft();
    var left = $('#tws-left');
    function edited(e) {
      var t = e.target, row = t.closest('.tws-cr');
      if (row) readRow(row); else readCommon();
      after(true);
    }
    left.addEventListener('input', function (e) { var t = e.target; if (t.type === 'number' || t.type === 'date') edited(e); });
    left.addEventListener('change', function (e) { var t = e.target; if (t.tagName === 'SELECT') edited(e); });
    document.addEventListener('click', function (e) {
      var t = e.target, b;
      if ((b = t.closest('.tws-i'))) { var box = document.getElementById(b.getAttribute('data-tip')); if (box) box.hidden = !box.hidden; return; }
      if ((b = t.closest('[data-preset]'))) { applyU(UI.presetU(b.getAttribute('data-preset'))); return; }
      if ((b = t.closest('[data-del]'))) { var k = b.getAttribute('data-del'); U.conds = U.conds.filter(function (u) { return u.k !== k; }); renderConds(); after(true); return; }
      if ((b = t.closest('[data-off]'))) { offCond(b.closest('.tws-cr').getAttribute('data-k'), b.getAttribute('data-off')); return; }
      if ((b = t.closest('[data-on]'))) { addCond(b.getAttribute('data-k'), b.getAttribute('data-on')); return; }
      if ((b = t.closest('[data-add]'))) { addCond(b.getAttribute('data-add'), b.getAttribute('data-m')); return; }
      if (t.closest('#tws-addbtn')) { var mn = $('#tws-menu'); mn.hidden = !mn.hidden; $('#tws-addbtn').setAttribute('aria-expanded', String(!mn.hidden)); if (!mn.hidden) renderMenu(); return; }
      if (t.closest('#tws-copy')) { copyLink(); return; }
      if (t.closest('#tws-bar')) { var c = $('#tws-concl'); if (c.scrollIntoView) c.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
    });
    $('#tws-prevchk').addEventListener('change', function () { showPrev = this.checked; if (cur) drawCharts(cur.r); });
    $$('.vch-sw button', $('#tws-ch1')).forEach(function (b) {
      b.onclick = function () { logScale = b.getAttribute('data-s') === 'log'; $$('.vch-sw button', $('#tws-ch1')).forEach(function (z) { z.className = z === b ? 'on' : ''; }); if (cur) drawCharts(cur.r); };
    });
    var rz; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { ['#tws-ch1', '#tws-ch2'].forEach(function (s) { var el = $(s); if (el._redraw) el._redraw(); }); }, 150); });
    window.addEventListener('hashchange', function () {
      if (location.hash === lastHash) return;
      var d = UI.decode(location.hash); if (d) { lastHash = null; applyU(d); }
    });
    try { worker = new Worker('worker.js'); } catch (e) { $('#tws-concl').innerHTML = '<div class="tws-cc"><span class="tws-warn">這個瀏覽器無法啟動背景運算（Web Worker），請改用較新版的 Chrome、Safari 或 Firefox。</span></div>'; return; }
    worker.onmessage = onMsg;
    worker.onerror = function (e) { $('#tws-concl').innerHTML = '<div class="tws-cc"><span class="tws-warn">背景運算出錯：' + esc(e.message || '') + '</span></div>'; };
    worker.postMessage({ type: 'init', base: location.href.replace(/[#?].*$/, '').replace(/[^\/]*$/, '') });
    applyU(UI.decode(location.hash) || UI.presetU('comp'));
    renderConcl();
  }
  init();
})();
