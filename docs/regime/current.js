/* 2026-09-13：共用市場發布包，避免六軸事實與已核准判讀各自停更。 */
(function () {
  'use strict';
  const axes = [
    ['利率與久期', '名目利率、實質利率與曲線', ['source:fred_treasury_10y', 'monitor:real10y', 'monitor:t10y2y']],
    ['美元與匯率', '美元指數與主要匯率', ['monitor:dxy', 'monitor:usdjpy', 'monitor:eurusd']],
    ['信用', '信用利差與債券相對價格', ['monitor:hy_oas', 'monitor:ccc_oas', 'monitor:hyg_lqd']],
    ['成長與防禦', '跨資產相對價格代理', ['monitor:copper_gold', 'monitor:iwm_spy', 'monitor:xly_xlp']],
    ['股票風險偏好', '指數、廣度與波動', ['monitor:sp500', 'internals:brd_above50', 'monitor:vix']],
    ['商品', '能源與金屬價格', ['monitor:wti', 'monitor:gold', 'monitor:copper']]
  ];
  const statuses = {ok: '判讀與資料同步', needs_review: '資料已更新，等待重評', current: '判讀與資料同步', fresh: '判讀與資料同步', degraded: '部分資料缺漏',
    pending: '等待重評', pending_analysis: '等待重評', stale: '判讀待更新', blocked: '更新受阻'};
  const esc = value => String(value == null ? '—' : value).replace(/[&<>"']/g,
    c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
  function age(day, now) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(day || '')) return null;
    const stamp = Date.parse(day + 'T00:00:00Z');
    return Number.isFinite(stamp) ? Math.floor((now - stamp) / 86400000) : null;
  }
  function quoteHTML(ref, quotes, now) {
    const q = quotes[ref] || {};
    const days = age(q.as_of, now);
    const usable = Number.isFinite(q.num) && days !== null && days >= 0;
    const state = !usable ? '缺少有效觀測' : days > 4 ? '資料較舊' : q.status && q.status !== 'ok' ? '來源待恢復' : '';
    let value = usable ? (q.val || String(q.num)) : '—';
    if (usable && q.unit === 'percent') value = q.num.toFixed(2) + '%';
    const link = /^https:\/\//.test(q.source_url || '') ? q.source_url : '/monitor/';
    return '<div class="rg-quote"><a href="' + esc(link) + '">' + esc(q.label || ref) + '</a>' +
      '<strong>' + esc(value) + '</strong><small>' + esc(q.as_of) + (state ? ' · ' + state : '') + '</small></div>';
  }
  function render(bundle, now) {
    const state = bundle.state || {}, refresh = bundle.refresh || {}, read = bundle.read || {};
    const quotes = (state.evidence || {}).quotes || {};
    const accepted = refresh.status !== 'blocked' && (read.review || {}).verdict === 'pass' && read.as_of && age(read.as_of, now) !== null && age(read.as_of, now) >= 0;
    const expired = accepted && Number.isFinite(read.valid_days) && age(read.as_of, now) > read.valid_days;
    let html = '<div class="rg-status">資料包日期 ' + esc(refresh.data_as_of || state.as_of) +
      ' · 判讀日期 ' + esc(accepted ? read.as_of : null) + ' · ' + esc(statuses[refresh.status] || refresh.status || '狀態未知') +
      (expired ? ' · 判讀已超過有效期' : '') + '</div>';
    html += '<h3>最新六軸觀測</h3><p class="rg-note">各筆日期以來源為準。觀測值用於檢查判讀，完整走勢與歷史比較見市場頁。</p><div class="rg-grid">';
    html += axes.map(([title, sub, refs]) => '<section class="rg-axis"><h4>' + title + '</h4><p>' + sub + '</p>' +
      refs.map(ref => quoteHTML(ref, quotes, now)).join('') + '</section>').join('');
    html += '</div><p class="rg-note">HYG／LQD 為 ETF 價格比，會同時受利差與久期影響；HY OAS 為高收益債信用利差。銅金比為不同報價單位的價格比，僅比較自身歷史。</p>';
    // 2026-09-13：保留前次研究供對照，並明示尚未依新版資料重評。
    const pending = refresh.status === 'needs_review';
    html += '<section class="rg-reading"><h3>' + (pending ? '上一份判讀（等待重評）' : '市場判讀與可能路徑') + '</h3>';
    if (pending && accepted) html += '<p class="rg-note">以下為上一份已審查判讀，尚未依本次新資料重評，請對照上述最新觀測。</p>';
    if (accepted) {
      html += '<p class="rg-note">共用市場頁已審查判讀 · ' + esc(read.as_of) + ' · 當時證據 ' + esc((read.snapshot_id || '').slice(0, 8)) + '</p>';
      html += '<p>' + esc(read.thesis_zh) + '</p><details><summary>推演路徑與跨資產影響</summary><p>' + esc(read.path_zh) + '</p>';
      html += (read.scenarios || []).map(s => '<section class="rg-scenario"><h4>' + esc(s.name_zh) + ' · ' + esc(s.horizon) + '</h4><p>' +
        esc(s.conditions_zh) + '</p><p>' + esc(s.asset_implications_zh) + '</p><p><b>推翻條件：</b>' + esc(s.falsifiers_zh) + '</p></section>').join('');
      html += '</details>';
    } else html += '<p>尚無可用的已審查判讀。觀測資料持續顯示。</p>';
    return html + '<p><a href="/market/">市場完整分析、歷史比較與命題對帳 →</a></p></section>';
  }
  async function load() {
    const weekly = document.getElementById('regime-weekly-status');
    if (weekly) {
      const days = age(weekly.dataset.asOf, Date.now());
      if (days === null || days < 0) weekly.textContent += ' · 週度資料不完整';
      else if (days > 10) weekly.textContent += ' · 週度資料逾期，等待來源更新';
    }
    const root = document.getElementById('regime-current');
    if (!root) return;
    try {
      const response = await fetch('/market/data/refresh.json', {cache: 'no-store'});
      if (!response.ok) throw new Error('refresh');
      const refresh = await response.json();
      if (!/^releases\/[a-f0-9]{64}\.json$/.test(refresh.bundle || '')) throw new Error('bundle path');
      const result = await fetch('/market/data/' + refresh.bundle);
      if (!result.ok) throw new Error('bundle');
      const bundle = await result.json();
      if (bundle.snapshot_id !== refresh.snapshot_id) throw new Error('snapshot mismatch');
      root.innerHTML = render(bundle, Date.now());
    } catch (_) {
      root.innerHTML = '<p>最新市場資料暫時無法載入。下方保留具日期的週度觀測；<a href="/market/">前往市場頁查看狀態</a>。</p>';
    }
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {render, quoteHTML, age};
  if (typeof document !== 'undefined') load();
}());
