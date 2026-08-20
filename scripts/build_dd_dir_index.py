#!/usr/bin/env python3
"""build_dd_dir_index.py — 產生 docs/dd/index.html 與 docs/dca/index.html。

這兩個目錄過去沒有目錄頁（直接訪問 /dd/ 或 /dca/ 是 404）。本腳本直接掃描
目錄下的檔名（DD_{TICKER}_{YYYYMMDD}[.html] / DCA_{TICKER}_{YYYYMMDD}.html），
不依賴 INDEX.md 的 markdown 表格解析（欄位內容含大量 markdown/HTML 特殊字元，
直接掃檔名更穩定），產生「原始檔案目錄」清單頁：

- docs/dd/index.html：說明本頁是原始檔案目錄，主要瀏覽入口是 /research/（DD 主表）
  與 /t/（個股總覽），下方按日期新到舊列出全部報告。
- docs/dca/index.html：同上，但頁首標示 DCA 體系已於 2026-06-22 凍結封存，
  深度定見層併入 DD v13+（見 /research/）。

可重複執行（idempotent）：直接覆寫兩個 index.html。
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DD_DIR = REPO_ROOT / "docs" / "dd"
DCA_DIR = REPO_ROOT / "docs" / "dca"

FILENAME_RE = re.compile(r"^(?P<prefix>DD|DCA)_(?P<rest>.+)\.html$")
DATE_RE = re.compile(r"^\d{8}$")


def parse_reports(directory: Path, prefix: str) -> list[dict]:
    """掃描 directory 下 {prefix}_*.html，回傳 [{ticker, date, filename}, ...]。

    檔名格式主體為 {PREFIX}_{TICKER}_{YYYYMMDD}.html，但存在版本後綴變體，例如
    DD_2383TW_v10_20260415.html（版本字串夾在 ticker 與日期之間）或
    DD_2383TW_20260414_v3.html（版本字串在日期之後）。統一規則：
    ticker = 第一個 '_' 之前的片段；date = 其餘片段中第一個符合 8 碼數字者。
    """
    out = []
    for f in sorted(directory.glob(f"{prefix}_*.html")):
        m = FILENAME_RE.match(f.name)
        if not m:
            continue
        parts = m.group("rest").split("_")
        if len(parts) < 2:
            continue
        ticker = parts[0]
        date = next((p for p in parts[1:] if DATE_RE.match(p)), None)
        if date is None:
            continue
        out.append({"ticker": ticker, "date": date, "filename": f.name})
    return out


def fmt_date(d: str) -> str:
    return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"


NAV_HTML = """<style id="imq-nav-style">
.imq-nav-root{background:linear-gradient(135deg,#081832 0%,#173564 100%);padding:.7rem 20px;font-size:13px;box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:1000;font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.imq-nav-inner{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.imq-logo{font-weight:700;color:#fff !important;text-decoration:none !important;font-size:15px;letter-spacing:-.02em;flex-shrink:0;background:none !important;padding:0 !important}
.imq-logo:hover{color:#fff !important;text-decoration:none !important}
.imq-logo span{color:#d4b576}
.imq-menu{display:flex;align-items:center;gap:.15rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}
.imq-menu > a,.imq-dd-btn{color:rgba(255,255,255,.7) !important;font-size:.8rem;font-weight:500;padding:.42rem .72rem;border-radius:6px;transition:all .15s;background:none;border:0;font-family:inherit;cursor:pointer;text-decoration:none !important;display:inline-flex;align-items:center;gap:.28rem;line-height:1.2;letter-spacing:0}
.imq-menu > a:hover,.imq-dd-btn:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-menu > a.active,.imq-dd.active > .imq-dd-btn{color:#fff !important;background:rgba(184,146,74,.26);font-weight:600}
.imq-dd{position:relative;display:inline-block}
.imq-dd-menu{display:none;position:absolute;top:100%;left:0;background:#0d2244;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{display:block}
.imq-dd-menu a{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}
.imq-dd-menu a:hover{color:#fff !important;background:rgba(184,146,74,.20)}
.imq-dd-menu a.active{color:#fff !important;background:rgba(184,146,74,.26);font-weight:600}
.imq-caret{font-size:.6rem;opacity:.7;margin-top:1px}
.imq-subnav{background:#081832;padding:.45rem 20px;font-family:'Inter','Noto Sans TC',-apple-system,sans-serif}
.imq-subnav-inner{max-width:1140px;margin:0 auto;display:flex;gap:.3rem;flex-wrap:wrap}
.imq-subnav a{color:rgba(255,255,255,.55) !important;font-size:.74rem;font-weight:500;padding:.28rem .6rem;border-radius:5px;text-decoration:none !important}
.imq-subnav a:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-subnav a.active{color:#fff !important;background:rgba(184,146,74,.30);font-weight:600}
@media(max-width:768px){
  .imq-nav-root{padding:.55rem 12px}
  .imq-nav-inner{gap:.4rem}
  .imq-menu{width:100%;justify-content:flex-start;gap:.1rem}
  .imq-menu > a,.imq-dd-btn{font-size:.74rem;padding:.32rem .5rem}
  .imq-dd-menu{position:static;display:none;min-width:auto;box-shadow:none;background:rgba(255,255,255,.04);border:none;padding:.1rem 0 .3rem 1rem;margin:.1rem 0}
  .imq-dd.open .imq-dd-menu{display:block}
}
</style>
<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/">首頁</a>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">市場<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/intel/">情報監視器</a>
          <a href="/briefing/">每日簡報</a>
          <a href="/rotation/radar.html">資產輪動雷達</a>
          <a href="/macro/">總經深度報告</a>
          <a href="/earnings/">財報分析</a>
          <a href="/markets.html">Markets</a>
          <a href="/sectors.html">Sectors</a>
        </div>
      </div>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">選股<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/cockpit/">選股主控台</a>
          <a href="/dd-screener/">DD Screener</a>
          <a href="/research/momentum-5/">Momentum-5</a>
          <a href="/qgm/">QGM 美股</a>
          <a href="/qgm-tw/">QGM 台股</a>
          <a href="/screeners.html">RS+VCP Screener</a>
        </div>
      </div>
      <div class="imq-dd active">
        <button type="button" class="imq-dd-btn">研究<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/t/">個股總覽</a>
          <a href="/research/">個股 DD</a>
          <a href="/id/">產業深度 ID</a>
          <a href="/id/tier_matrix.html">Tier Matrix</a>
          <a href="/supply-chain/">供應鏈地圖</a>
          <a href="/comparisons/">多股對比</a>
          <a href="/research/synthesis/">期望落差綜合研判</a>
        </div>
      </div>
      <a href="/mental-models/">心智模型</a>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">系統<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/track-record/">裁決實績</a>
          <a href="/pm/">持倉週掃</a>
          <a href="/long-track-w52-adaptive/">實單主系統</a>
          <a href="/long-track/">追蹤總覽</a>
          <a href="/backtest/">量化回測</a>
          <a href="/tools/">期貨部位計算機</a>
          <a href="/data.html">公開資料</a>
        </div>
      </div>
      <a href="/flow/">投資流程</a>
      <a href="/how-to.html">使用指南</a>
      <a href="/search.html">搜尋</a>
    </nav>
  </div>
</header>
<script>(function(){document.querySelectorAll('.imq-dd-btn').forEach(function(btn){btn.addEventListener('click',function(e){e.preventDefault();var dd=btn.closest('.imq-dd');document.querySelectorAll('.imq-dd.open').forEach(function(d){if(d!==dd)d.classList.remove('open')});dd.classList.toggle('open')})});document.addEventListener('click',function(e){if(!e.target.closest('.imq-dd'))document.querySelectorAll('.imq-dd.open').forEach(function(d){d.classList.remove('open')})});})();</script>
"""

FOOT_HTML = """<footer class="imq-foot">
  <div class="container">
    <div>&copy; 2026 InvestMQuest Research</div>
    <div><a href="/disclosures.html">方法論與揭露</a> &middot; 本站內容僅供研究參考，不構成投資建議</div>
  </div>
</footer>
"""

STYLE_TEMPLATE = """<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);background:var(--paper);color:var(--body);line-height:1.65;font-size:14px;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none;transition:color .15s}
a:hover{color:var(--accent-ink)}
.container{max-width:1000px;margin:0 auto;padding:0 1.5rem}
.hero{padding:2.6rem 0 2rem;border-bottom:1px solid var(--line-soft)}
.hero .eyebrow{font-family:var(--mono);font-size:.66rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-deep);display:block;margin-bottom:.9rem}
.hero h1{font-family:var(--serif);font-size:1.6rem;font-weight:700;letter-spacing:-.01em;color:var(--ink)}
.hero .sub{color:var(--sec);font-size:.9rem;margin-top:.5rem;max-width:700px;line-height:1.7}
.crumb{font-size:.78rem;color:var(--muted);margin-bottom:.6rem;font-family:var(--mono)}
.crumb a{color:var(--muted)}
.crumb a:hover{color:var(--accent)}
.frozen-banner{margin-top:1.1rem;padding:.9rem 1.15rem;background:var(--gold-bg);border:1px solid var(--gold-line,var(--line));border-radius:var(--r);color:var(--gold-deep);font-size:.86rem;font-weight:600;line-height:1.6}
.entry-links{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.1rem}
.entry-links a{display:inline-flex;align-items:center;gap:.4rem;background:var(--accent);color:#fff;padding:.55rem 1rem;border-radius:8px;font-size:.84rem;font-weight:700;text-decoration:none}
.entry-links a:hover{background:var(--accent-ink);color:#fff}
.entry-links a.secondary{background:var(--card);color:var(--accent);border:1px solid var(--line)}
.entry-links a.secondary:hover{border-color:var(--accent)}
.section{padding:1.8rem 0 3rem}
.toolbar{display:flex;align-items:center;gap:.7rem;flex-wrap:wrap;margin-bottom:1rem}
.toolbar input{flex:1 1 240px;min-width:0;border:1px solid var(--line);border-radius:8px;padding:.55rem .8rem;font:inherit;font-size:13px;background:var(--card);color:var(--body);outline:none}
.toolbar input:focus{border-color:var(--accent)}
.toolbar .count{font-size:.76rem;color:var(--muted);font-family:var(--mono);white-space:nowrap}
.dir-table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh-1)}
.dir-table thead th{text-align:left;font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600;padding:.6rem .9rem;border-bottom:1px solid var(--line);background:var(--line-soft)}
.dir-table tbody td{padding:.5rem .9rem;border-bottom:1px solid var(--line-soft);font-size:.85rem;vertical-align:top}
.dir-table tbody tr:last-child td{border-bottom:none}
.dir-table tbody tr:hover{background:var(--line-soft)}
.dir-table .c-date{font-family:var(--mono);color:var(--sec);white-space:nowrap;width:6.5rem}
.dir-table .c-ticker{font-family:var(--mono);font-weight:700;color:var(--ink);white-space:nowrap}
.dir-table .c-file a{color:var(--accent)}
.dir-table tbody tr.is-hidden{display:none}
.empty-row td{text-align:center;color:var(--muted);padding:2rem}
@media(max-width:768px){
  .hero h1{font-size:1.3rem}
  .dir-table .c-file{word-break:break-all}
}
</style>"""


def render_page(*, title: str, description: str, eyebrow: str, h1: str, sub_html: str,
                 frozen_banner_html: str, reports: list[dict]) -> str:
    rows_html = []
    for r in reports:
        rows_html.append(
            f'      <tr data-search="{r["date"]} {r["ticker"].lower()} {r["filename"].lower()}">'
            f'<td class="c-date">{fmt_date(r["date"])}</td>'
            f'<td class="c-ticker">{r["ticker"]}</td>'
            f'<td class="c-file"><a href="{r["filename"]}">{r["filename"]}</a></td></tr>'
        )
    rows_joined = "\n".join(rows_html)
    n = len(reports)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta property="og:title" content="{title}">
  <meta property="og:site_name" content="InvestMQuest Research">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/imq-base.css">
  {STYLE_TEMPLATE}
</head>
<body>
{NAV_HTML}
<div class="hero">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> &rsaquo; {h1}</div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="sub">{sub_html}</p>
    {frozen_banner_html}
    <div class="entry-links">
      <a href="/research/">→ /research/ 個股 DD 主表（篩選 · 裁決 · 護城河總覽）</a>
      <a href="/t/" class="secondary">→ /t/ 個股總覽（單一 ticker 全歷史）</a>
    </div>
  </div>
</div>
<div class="section">
  <div class="container">
    <div class="toolbar">
      <input type="text" id="filter-input" placeholder="搜尋 ticker 或日期（例：2330 或 2026-05）" autocomplete="off">
      <span class="count"><span id="visible-count">{n}</span> / {n} 筆</span>
    </div>
    <table class="dir-table">
      <thead><tr><th>日期</th><th>Ticker</th><th>檔案</th></tr></thead>
      <tbody id="dir-tbody">
{rows_joined}
      </tbody>
    </table>
  </div>
</div>
{FOOT_HTML}
<script>
(function(){{
  var input = document.getElementById('filter-input');
  var rows = Array.prototype.slice.call(document.querySelectorAll('#dir-tbody tr'));
  var counter = document.getElementById('visible-count');
  input.addEventListener('input', function(){{
    var q = input.value.trim().toLowerCase();
    var visible = 0;
    rows.forEach(function(tr){{
      var hit = !q || (tr.getAttribute('data-search') || '').indexOf(q) !== -1;
      tr.classList.toggle('is-hidden', !hit);
      if(hit) visible++;
    }});
    counter.textContent = visible;
  }});
}})();
</script>
</body>
</html>
"""


def main() -> None:
    dd_reports = parse_reports(DD_DIR, "DD")
    dd_reports.sort(key=lambda r: (r["date"], r["ticker"]), reverse=True)

    dca_reports = parse_reports(DCA_DIR, "DCA")
    dca_reports.sort(key=lambda r: (r["date"], r["ticker"]), reverse=True)

    dd_html = render_page(
        title="DD 報告原始檔案目錄 — InvestMQuest Research",
        description=f"個股深度研究（DD）原始 HTML 檔案目錄，共 {len(dd_reports)} 份，按日期新到舊排列。主要瀏覽入口請見 /research/ 與 /t/。",
        eyebrow="Raw File Directory",
        h1="DD 報告原始檔案目錄",
        sub_html=(
            "這裡是個股深度研究（Due Diligence）報告的<b>原始檔案存放目錄</b>，"
            f"目前共 {len(dd_reports)} 份，按產出日期新到舊排列——單純列出檔名，不做篩選、"
            "不看裁決分布。<b>多數情況你要找的其實是下面兩個聚合頁</b>：/research/ 的 DD 主表"
            "可依裁決、護城河、估值燈篩選全部個股；/t/ 的個股總覽可直接看單一 ticker 的完整歷史。"
            "本頁僅供需要直接定位某一份特定檔案時使用。"
        ),
        frozen_banner_html="",
        reports=dd_reports,
    )
    (DD_DIR / "index.html").write_text(dd_html, encoding="utf-8")
    print(f"wrote docs/dd/index.html ({len(dd_reports)} reports)")

    dca_frozen = (
        '<div class="frozen-banner">⚠ 本體系已於 2026-06-22 凍結封存——'
        '深度定見層已併入 DD v13+（見 <a href="/research/">/research/</a>）。'
        '以下清單為既有存量報告的原始檔案存檔，不再新增。</div>'
    )
    dca_html = render_page(
        title="DCA 報告原始檔案目錄（已凍結） — InvestMQuest Research",
        description=f"投資決策層（DCA）原始 HTML 檔案目錄，共 {len(dca_reports)} 份；體系已於 2026-06-22 凍結封存，深度定見層併入 DD v13+。",
        eyebrow="Raw File Directory · Frozen",
        h1="DCA 報告原始檔案目錄",
        sub_html=(
            "這裡是投資決策層（Deep Conviction Analysis）報告的<b>原始檔案存放目錄</b>，"
            f"目前共 {len(dca_reports)} 份既有存量報告，按產出日期新到舊排列。"
        ),
        frozen_banner_html=dca_frozen,
        reports=dca_reports,
    )
    (DCA_DIR / "index.html").write_text(dca_html, encoding="utf-8")
    print(f"wrote docs/dca/index.html ({len(dca_reports)} reports)")


if __name__ == "__main__":
    main()
