# 產業深度報告 HTML Template v2.0 — 敘事為骨、表格為窗

**此檔是「完整考證版」（`_full.html`）的 template**。視覺走精煉版編輯風（暖紙 + 襯線 + 鏽金，見 §共用 CSS）。每次跑 skill 同時產**兩份**：canonical 精煉版（決策卡，帶 id-meta，見 `lean_template.md`）+ 本完整版（9 章 + 一手 source，無 id-meta，`_full.html`）。dual-output 規則見 SKILL.md。

## 檔名規則

`docs/id/ID_{Theme_CamelCase}_{YYYYMMDD}.html`

- Theme_CamelCase 範例：GlassSubstrate / HBM_Supercycle / AIASIC_vs_GPU / GLP1_Landscape / EUV_NextGen

---

## 基本骨架（§0-§9）

```html
<!DOCTYPE html>
<html lang="zh-Hant"><head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<!-- ⚠ dual-output 規則：完整考證版（_full.html）是 companion，「不放任何 id-meta」——
     ❌ 不要 <meta name="id-skill-version | id-theme | id-publish-date"> 三標
     ❌ 不要 <script id="id-meta"> JSON block
     id-meta 的 SSOT 只放在 canonical 精煉版（lean_template.md → ID_{Theme}_{YYYYMMDD}.html）。
     原因：validate_id_meta.py 以 <meta name="id-*"> / id-meta script 判定「此檔是 ID 檔」；
     _full 只要殘留任一個，就會被誤判成「缺 id-meta block 的 ID 檔」而 FAIL（CI strict gate 整 push 連坐）。
     ∴ _full 的 <head> 只保留 robots / charset / viewport + <title> + <style>。 -->
<title>產業深度（完整考證版）— {THEME}（{YYYY-MM-DD}）</title>
<style>{SHARED_STYLES}</style>
</head><body>
<!-- ▼▼ canonical site header — 全站統一，由 scripts/site_nav.py full_nav_block('research','id') 生成。
     不要手改；site_nav.py 變更時重算貼回（python3 -c "import sys; sys.path.insert(0,'scripts'); import site_nav; print(site_nav.full_nav_block('research','id'))"）。 ▼▼ -->
<style id="imq-nav-style">
.imq-nav-root{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:.7rem 20px;font-size:13px;box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:1000;font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.imq-nav-inner{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.imq-logo{font-weight:700;color:#fff !important;text-decoration:none !important;font-size:15px;letter-spacing:-.02em;flex-shrink:0;background:none !important;padding:0 !important}
.imq-logo:hover{color:#fff !important;text-decoration:none !important}
.imq-logo span{color:#3b82f6}
.imq-menu{display:flex;align-items:center;gap:.15rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}
.imq-menu > a,.imq-dd-btn{color:rgba(255,255,255,.7) !important;font-size:.8rem;font-weight:500;padding:.42rem .72rem;border-radius:6px;transition:all .15s;background:none;border:0;font-family:inherit;cursor:pointer;text-decoration:none !important;display:inline-flex;align-items:center;gap:.28rem;line-height:1.2;letter-spacing:0}
.imq-menu > a:hover,.imq-dd-btn:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-menu > a.active,.imq-dd.active > .imq-dd-btn{color:#fff !important;background:rgba(59,130,246,.22);font-weight:600}
.imq-dd{position:relative;display:inline-block}
.imq-dd-menu{display:none;position:absolute;top:100%;left:0;background:#1e293b;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{display:block}
.imq-dd-menu a{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}
.imq-dd-menu a:hover{color:#fff !important;background:rgba(59,130,246,.18)}
.imq-dd-menu a.active{color:#fff !important;background:rgba(59,130,246,.22);font-weight:600}
.imq-caret{font-size:.6rem;opacity:.7;margin-top:1px}
.imq-subnav{background:#0f172a;padding:.45rem 20px;font-family:'Inter','Noto Sans TC',-apple-system,sans-serif}
.imq-subnav-inner{max-width:1140px;margin:0 auto;display:flex;gap:.3rem;flex-wrap:wrap}
.imq-subnav a{color:rgba(255,255,255,.55) !important;font-size:.74rem;font-weight:500;padding:.28rem .6rem;border-radius:5px;text-decoration:none !important}
.imq-subnav a:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-subnav a.active{color:#fff !important;background:rgba(59,130,246,.28);font-weight:600}
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
      <div class="imq-dd active">
        <button type="button" class="imq-dd-btn">研究<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/research/">個股 DD</a>
          <a href="/id/" class="active">產業深度 ID</a>
          <a href="/ds/">產業敘述 DS</a>
          <a href="/comparisons/">多股對比</a>
          <a href="/supply-chain/">供應鏈地圖</a>
          <a href="/id/tier_matrix.html">🎯 Tier Matrix</a>
        </div>
      </div>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">市場<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/briefing/">每日簡報</a>
          <a href="/weekly/">週報</a>
          <a href="/earnings/">財報分析</a>
          <a href="/markets.html">Markets</a>
          <a href="/sectors.html">Sectors</a>
          <a href="/six-state/">六狀態機</a>
        </div>
      </div>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">工具<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/backtest/">量化回測</a>
          <a href="/dd-screener/">DD Screener</a>
          <a href="/qgm/">QGM 美股</a>
          <a href="/qgm-tw/">QGM 台股</a>
          <a href="/screener.html">Screener 美股</a>
          <a href="/screener-tw.html">Screener 台股</a>
          <a href="/screener-jp.html">Screener 日股</a>
          <a href="/screener-my.html">Screener 馬股</a>
          <a href="/cache/">🗄 Data Cache</a>
          <a href="/tools/">期貨部位計算機</a>
        </div>
      </div>
      <a href="/mental-models/">🧠 心智模型</a>
      <a href="/how-to.html">📘 使用說明</a>
    </nav>
  </div>
</header>
<script>(function(){document.querySelectorAll('.imq-dd-btn').forEach(function(btn){btn.addEventListener('click',function(e){e.preventDefault();var dd=btn.closest('.imq-dd');document.querySelectorAll('.imq-dd.open').forEach(function(d){if(d!==dd)d.classList.remove('open')});dd.classList.toggle('open')})});document.addEventListener('click',function(e){if(!e.target.closest('.imq-dd'))document.querySelectorAll('.imq-dd.open').forEach(function(d){d.classList.remove('open')})});})();</script>
<!-- ▲▲ canonical site header 結束 ▲▲ -->

<header class="id-head">
  <div class="id-badge"><span>產業深度研究 · INDUSTRY EQUITY RESEARCH · {SECTOR}</span><span class="v2-pill">{DD MON YYYY}</span></div>
  <h1>{THEME}</h1>
  <!-- stance band：等同個股 rating+TP。stance NEUTRAL→.rate 琥珀；Overweight→改 #15803D；Underweight→改 #B42318 -->
  <div class="mh-stance">
    <span><span class="k">Sector stance</span>　<span class="rate">{NEUTRAL / OVERWEIGHT / UNDERWEIGHT}</span></span>
    <span><span class="k">供需裁決</span>　<span class="vv">{過剩 / 平衡 / 短缺（含時間範圍）}</span></span>
    <span><span class="k">Conviction</span>　<span class="vv">{High / Mid / Low}</span></span>
    <span><span class="k">Top picks</span>　<span class="vv">{TICKER1, TICKER2}</span></span>
  </div>
  <p class="id-meta">發布日 {YYYY-MM-DD} ｜ 涵蓋股票 {N} ｜ AI 占比 {PCT}% ｜ 文字比 {RATIO}% ｜ v2.2</p>
</header>

<!-- Claim Taxonomy reader banner（v2 必加） -->
<div class="claim-banner">
  <strong>CLAIM TAXONOMY v1（v2.0 敘事版）</strong>：本 ID 在 §0/§5/§7/§8 使用 4 類 inline tag 揭露 claim 性質：
  <strong>[F:]</strong> 事實（有 source）｜<strong>[I:]</strong> 推論（A→B 揭露）｜
  <strong>[X:]</strong> 情境預測（base/bull/bear 三情境，詞彙級機率）｜<strong>[A:]</strong> 顯式假設。
  數字以 range / ~xxx 呈現（除非 T1 公告精準值）；機率用「很可能 / 可能 / 不太可能」非百分比。來源收在每節末「本節參考來源」區塊。
</div>

<!-- Unit glossary（QC-19；§0 前後）：ASP 單位 / Revenue 口徑 / 營收 scope -->
<div class="unit-glossary">
  <strong>單位與口徑</strong>：ASP = {$/wafer | $/stack | $/GB | $/unit}；Revenue = {全年 | 季度 | annualized run-rate}；營收 scope = {segment | AI-only | total company}。
</div>

<!-- sticky section nav（頁內錨點；class 不可叫 imq-nav-root，會被 canonical site header 樣式覆蓋） -->
<nav class="id-secnav">
  <a href="#s0">§0 決策</a><a href="#s1">§1 歷史</a><a href="#s2">§2 技術</a>
  <a href="#s3">§3 供給</a><a href="#s4">§4 需求</a><a href="#s5">§5 裁決</a>
  <a href="#s6">§6 估值</a><a href="#s7">§7 分歧</a><a href="#s8">§8 Catalyst</a><a href="#s9">§9 個股</a>
</nav>

<section id="s0" class="id-body"> ... 決策摘要層 ... </section>
<section id="s1" class="id-body"> ... 白話定義 + 歷史脈絡 ... </section>
<section id="s2" class="id-body"> ... 技術成熟度 + S 曲線 ... </section>
<section id="s3" class="id-body"> ... 供給側 + 利潤池 ... </section>
<section id="s4" class="id-body"> ... 需求側 + 三角驗證 ... </section>
<section id="s5" class="id-body"> ... 供需裁決 + 推估 + 投資時鐘 ... </section>
<section id="s6" class="id-body"> ... 產業經濟學 + 估值傳導 ... </section>
<section id="s7" class="id-body"> ... Non-Consensus + Priced-in + Kill ... </section>
<section id="s8" class="id-body"> ... Catalyst Timeline + 證偽表 ... </section>
<section id="s9" class="id-body"> ... 關聯個股 ... </section>

<!-- Disclosures（IB 免責頁尾，v2.2 必加） -->
<div class="id-disclosures">
  <div class="dh">DISCLOSURES &amp; IMPORTANT INFORMATION</div>
  本報告由 InvestMQuest Research 內部買方研究流程產生，僅供研究與投資決策參考，不構成要約、招攬或個別投資建議。資料來源含公司公告（8-K / 10-Q / 法說 transcript）與第三方研究機構，已力求準確但不保證完整或無誤；前瞻性陳述（base / bull / bear 情境）含不確定性，實際結果可能重大不同。估值與目標倍數隨價格與盈餘修正而變動。持倉揭露：本研究流程關聯帳戶可能持有文中標的部位。Past performance is not indicative of future results. © {YYYY} InvestMQuest Research.
</div>

<footer class="id-foot">
  <p>產業深度報告 · industry-analyst v2.2（敘事版） · 主題：{THEME} · 發布日：{YYYY-MM-DD} · AI 占比 {PCT}% · 文字比 {RATIO}%</p>
  <p><a href="/research/">← 回研究首頁</a> · <a href="/id/">所有產業報告</a></p>
</footer>
</body></html>
```

---

## 共用 CSS（貼到 `<style>`）

**精煉版編輯風（Editorial · v2.3）**：暖紙底 `--paper:#faf7f2` + 墨黑 `--ink:#1c1916` + 鏽金 accent `--accent:#7a3d1c` / `--gold:#b08840`，功能語意色 `--green/--red/--amber`。body 用 Noto Serif TC + Crimson Pro **襯線**，標籤/數字用 IBM Plex Mono（需在 `<head>` 引 Google Fonts：Crimson Pro + IBM Plex Mono + Noto Serif TC）。每張表自動 `Exhibit N ·`（CSS counter）+ mono 表頭；§0 含 masthead（desk 抬頭 + stance band）+ INVESTMENT SUMMARY 三欄 dsum（綠/金/紅）+ KEY CALL 深墨金字框；頁尾 Disclosures。`.ds-refs` / `.tier` / `.source-warning` 沿用。**統一精煉版風，完整版與精煉版同皮**；禁回紫色 / 海軍藍 IB。

```css
:root{--ink:#1c1916;--ink-soft:#3d3833;--paper:#faf7f2;--paper-deep:#f0ebe1;--paper-card:#f5f1e8;--accent:#7a3d1c;--accent-deep:#4a2410;--gold:#b08840;--gold-soft:#d4b572;--muted:#6e665a;--green:#2a5040;--red:#8a3424;--amber:#8a6420}
html{background:var(--paper-deep)}
body{font-family:'Noto Serif TC','Crimson Pro',serif;background:var(--paper);color:var(--ink);margin:0 auto;padding:30px 46px 90px;max-width:940px;font-size:15px;line-height:1.78;counter-reset:exhibit;-webkit-font-smoothing:antialiased}
.id-head{position:relative;border-bottom:3px double var(--ink);padding-bottom:22px;margin-bottom:16px}
.id-badge{display:flex;justify-content:space-between;align-items:baseline;gap:12px;font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;color:var(--muted);font-weight:500;text-transform:uppercase;margin-bottom:18px}
.v2-pill{color:var(--accent);font-weight:600;letter-spacing:.1em;font-size:10px;flex:0 0 auto;text-transform:none}
h1{font-family:'Crimson Pro','Noto Serif TC',serif;color:var(--ink);font-size:33px;margin:6px 0 10px;line-height:1.2;font-weight:700;letter-spacing:-.005em}
h1 em{color:var(--accent);font-style:italic}
.id-meta{font-family:'IBM Plex Mono',monospace;color:var(--muted);font-size:10px;letter-spacing:.07em;text-transform:uppercase;margin:16px 0 0;border-top:1px solid var(--paper-deep);padding-top:12px}
.mh-stance{display:flex;gap:0;flex-wrap:wrap;border:1px solid var(--ink);margin:22px 0 0;font-family:'IBM Plex Mono',monospace;font-size:12px}
.mh-stance>span{flex:1 1 150px;padding:13px 16px;border-right:1px solid var(--ink)}
.mh-stance>span:last-child{border-right:none}
.mh-stance .k{display:block;font-size:9.5px;letter-spacing:.16em;color:var(--muted);text-transform:uppercase;margin-bottom:6px}
.mh-stance .vv{font-family:'Crimson Pro',serif;color:var(--ink);font-weight:600;font-size:16px}
.mh-stance .rate{font-family:'Crimson Pro',serif;background:var(--amber);color:var(--paper);padding:1px 10px;font-weight:600;letter-spacing:.04em;font-size:15px}
h2{font-family:'Crimson Pro','Noto Serif TC',serif;color:var(--ink);border-bottom:2px solid var(--ink);padding:0 0 12px;margin:56px 0 18px;font-size:27px;font-weight:700;line-height:1.2}
h2 em{color:var(--accent);font-style:italic}
h3{font-family:'Crimson Pro','Noto Serif TC',serif;color:var(--accent-deep);margin:28px 0 8px;font-size:19px;font-weight:600;font-style:italic}
p{margin:0 0 16px;line-height:1.8}
.id-body p{text-align:justify;hyphens:auto;font-size:16px}
.id-body ul,.id-body ol{margin:12px 0 18px;padding-left:24px;line-height:1.72}
.id-body li{margin:7px 0}
.id-body li strong,strong{color:var(--ink);font-weight:600}
em{color:var(--accent);font-style:italic;font-weight:400}
.id-lede{font-style:italic;color:var(--ink-soft);font-size:17px;line-height:1.62;margin:16px 0 22px;border-left:3px solid var(--gold);padding:4px 0 4px 18px;background:none}
.claim-banner{font-family:'IBM Plex Mono',monospace;background:var(--paper-card);border-left:3px solid var(--muted);padding:11px 16px;margin:14px 0;font-size:11.5px;line-height:1.6;color:var(--ink-soft)}
.claim-banner strong{color:var(--accent-deep)}
.unit-glossary{background:var(--paper-card);border-left:3px solid var(--gold);padding:10px 16px;margin:10px 0 16px;font-size:12px;color:var(--ink-soft);line-height:1.6}
table{width:100%;border-collapse:collapse;margin:14px 0 6px;background:var(--paper)}
th{font-family:'IBM Plex Mono',monospace;background:none;color:var(--muted);padding:9px 14px;text-align:left;font-weight:600;font-size:10px;letter-spacing:.06em;text-transform:uppercase;border-bottom:1.5px solid var(--ink)}
td{padding:10px 14px;border-bottom:1px solid var(--paper-deep);vertical-align:top;font-size:14px;line-height:1.5}
tbody tr:last-child td{border-bottom:1px solid var(--ink)}
tbody tr:hover td{background:var(--paper-card)}
caption{caption-side:top;font-family:'IBM Plex Mono',monospace;color:var(--accent);font-size:11px;letter-spacing:.06em;text-transform:uppercase;text-align:left;padding:8px 0;font-weight:600}
caption::before{counter-increment:exhibit;content:"Exhibit " counter(exhibit) " · ";color:var(--gold);font-weight:600}
.tbl-why{font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;margin:16px 0 0}
.tbl-read{font-size:14px;color:var(--ink-soft);font-style:italic;line-height:1.66;margin:12px 0 18px}
.tldr-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;margin:24px 0;border:1px solid var(--ink)}
.tldr-card{background:var(--paper);border-right:1px solid var(--ink);border-bottom:1px solid var(--ink);padding:15px 17px}
.tldr-card h4{font-family:'IBM Plex Mono',monospace;margin:0 0 7px;color:var(--muted);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:500}
.tldr-card .v{font-family:'Crimson Pro','Noto Serif TC',serif;font-size:20px;font-weight:600;color:var(--ink);line-height:1.15}
.id-thesis{background:var(--paper-card);border-left:4px solid var(--accent);padding:22px 26px;margin:24px 0;font-size:16px;color:var(--ink);line-height:1.72}
.id-thesis .label{font-family:'IBM Plex Mono',monospace;display:inline-block;background:var(--accent);color:var(--paper);padding:3px 11px;font-size:10px;letter-spacing:.22em;font-weight:600;text-transform:uppercase;margin-bottom:12px}
.id-crosslink{background:var(--paper-card);border:1px solid var(--paper-deep);padding:14px 18px;margin:18px 0;font-size:13.5px;color:var(--ink-soft);line-height:1.7}
.id-crosslink a{color:var(--accent);font-weight:600;text-decoration:none}
.judgment-banner{background:var(--paper-card);border-left:4px solid var(--gold);padding:12px 16px;margin:10px 0 16px;color:var(--ink-soft);font-size:14px}
.judgment-card{background:var(--paper-card);border:1px solid var(--gold-soft);border-left:4px solid var(--gold);padding:20px 24px;margin:24px 0}
.judgment-card .j-head{font-family:'IBM Plex Mono',monospace;display:flex;align-items:center;gap:10px;font-weight:600;color:var(--accent-deep);margin-bottom:12px;flex-wrap:wrap;font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.j-conf{font-family:'IBM Plex Mono',monospace;display:inline-block;font-size:10px;padding:2px 9px;font-weight:600;letter-spacing:.08em;color:var(--paper)}
.j-conf.high{background:var(--green)}
.j-conf.mid{background:var(--gold)}
.j-conf.low{background:var(--red)}
.j-facts{font-size:14.5px;color:var(--ink-soft);margin:8px 0;padding-left:20px;line-height:1.66}
.j-logic{font-size:13.5px;color:var(--ink);margin-top:12px;padding:12px 16px;background:rgba(28,25,22,.05);line-height:1.6}
.id-implication{background:rgba(42,80,64,.06);border-left:4px solid var(--green);padding:18px 22px;margin:24px 0 14px;font-size:15px;color:var(--ink);line-height:1.7}
.id-implication::before{font-family:'IBM Plex Mono',monospace;content:"對投資的意義 · INVESTMENT IMPLICATION";display:block;font-weight:600;color:var(--green);font-size:10px;letter-spacing:.18em;text-transform:uppercase;margin-bottom:10px}
.id-bridge{background:rgba(176,136,64,.07);border-left:4px solid var(--gold);padding:18px 22px;margin:26px 0;font-size:15px;color:var(--ink);line-height:1.7}
.id-bridge .label{font-family:'IBM Plex Mono',monospace;display:inline-block;color:var(--accent);font-size:10px;letter-spacing:.18em;font-weight:600;text-transform:uppercase;margin-bottom:10px}
.tier-pill{font-family:'IBM Plex Mono',monospace;display:inline-block;padding:2px 8px;font-size:10px;font-weight:600;color:var(--paper)}
.tier-red{background:var(--red)}
.tier-yellow{background:var(--gold)}
.tier-green{background:var(--green)}
.scurve-ascii{background:var(--paper-card);color:var(--accent-deep);padding:14px 16px;font-family:'IBM Plex Mono',monospace;font-size:12px;white-space:pre;line-height:1.45;overflow-x:auto;border:1px solid var(--paper-deep)}
.vc-svg{display:block;max-width:100%;margin:16px auto}
time,strong.id-time{display:inline;background:rgba(122,61,28,.08);color:var(--accent-deep);padding:1px 7px;font-family:'IBM Plex Mono',monospace;font-size:12.5px;font-weight:600;white-space:nowrap}
.ds-path-positive{color:var(--green);font-weight:600}
.ds-path-negative{color:var(--red);font-weight:600}
.id-tickers{font-size:13px}
.id-tickers .depth-red{color:var(--red);font-weight:700}
.id-tickers .depth-yellow{color:var(--amber);font-weight:700}
.id-tickers .depth-green{color:var(--green);font-weight:700}
.ds-refs{margin:30px 0 8px;padding:16px 0 0;background:none;border-top:1px solid var(--paper-deep);font-size:12px;color:var(--muted);line-height:1.6}
.ds-refs .ds-refs-label{font-family:'IBM Plex Mono',monospace;color:var(--muted);font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;display:block;margin-bottom:8px;font-weight:600}
.ds-refs ol{margin:0;padding-left:20px}
.ds-refs li{margin:4px 0}
.ds-refs a{color:var(--accent);text-decoration:none}
.ds-refs a:hover{text-decoration:underline}
.ds-refs .tier{font-family:'IBM Plex Mono',monospace;display:inline-block;color:var(--gold);font-weight:600;margin-right:6px;font-size:10px}
.source-warning{background:rgba(138,100,32,.07);border-left:3px solid var(--amber);padding:12px 18px;margin:16px 0;font-size:12.5px;color:var(--accent-deep);line-height:1.62}
.id-secnav{position:sticky;top:0;z-index:20;background:rgba(250,247,242,.96);backdrop-filter:blur(5px);border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);padding:8px 0;margin:0 0 24px;display:flex;flex-wrap:wrap;gap:2px;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.03em}
.id-secnav a{color:var(--accent);text-decoration:none;padding:3px 9px;font-weight:500}
.id-secnav a:hover{background:var(--accent);color:var(--paper)}
.inv-summary{display:grid;grid-template-columns:repeat(3,1fr);border:2px solid var(--ink);margin:24px 0;padding:0}
.inv-summary .inv-hd{grid-column:1/-1;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--paper);background:var(--ink);font-weight:600;padding:9px 16px;margin:0;border:none}
.inv-row{display:block;margin:0;padding:20px 22px;border-right:1px solid var(--ink);line-height:1.62}
.inv-row:last-child{border-right:none}
.inv-row:nth-child(2){background:rgba(42,80,64,.05)}
.inv-row:nth-child(3){background:rgba(176,136,64,.06)}
.inv-row:nth-child(4){background:rgba(138,52,36,.05)}
.inv-row .inv-lab{display:block;flex:none;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;padding:0;margin-bottom:11px;border:none}
.inv-row:nth-child(2) .inv-lab{color:var(--green)}
.inv-row:nth-child(3) .inv-lab{color:var(--gold)}
.inv-row:nth-child(4) .inv-lab{color:var(--red)}
.inv-row .inv-txt{font-size:14px}
.key-judgment{background:var(--ink);color:var(--paper);padding:28px 32px;margin:26px 0;line-height:1.7;position:relative}
.key-judgment .kj-hd{font-family:'IBM Plex Mono',monospace;color:var(--gold-soft);font-size:10px;letter-spacing:.28em;text-transform:uppercase;font-weight:600;margin-bottom:14px}
.key-judgment p{color:var(--paper);font-size:16px}
.key-judgment strong{color:var(--gold-soft)}
.key-judgment em{color:var(--gold-soft)}
.id-foot{margin-top:42px;padding-top:16px;border-top:3px double var(--ink);color:var(--muted);font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;text-align:center;line-height:1.9}
.id-foot a{color:var(--accent);text-decoration:none}
.id-disclosures{margin-top:36px;padding-top:16px;border-top:1px solid var(--paper-deep);color:var(--muted);font-size:11px;line-height:1.62}
.id-disclosures .dh{font-family:'IBM Plex Mono',monospace;color:var(--accent);font-weight:600;letter-spacing:.18em;font-size:10px;text-transform:uppercase;margin-bottom:6px}
@media (max-width:720px){body{padding:20px 18px 60px}h1{font-size:27px}h2{font-size:22px}.id-secnav{font-size:10px}.mh-stance{flex-direction:column}.mh-stance>span{border-right:none;border-bottom:1px solid var(--ink)}.mh-stance>span:last-child{border-bottom:none}.inv-summary{grid-template-columns:1fr}.inv-row{border-right:none;border-bottom:1px solid var(--ink)}}
@media print{body{padding:12px;max-width:none;font-size:11pt;line-height:1.6;background:#fff}.id-thesis,.id-implication,.id-bridge,.judgment-card,.key-judgment{break-inside:avoid}.id-secnav{display:none}}
```

---

## §0 決策摘要層（三句話 + KEY CALL + 6-box + thesis + PM 綠卡 + cross-link）

`§0 內順序`：**INVESTMENT SUMMARY 三句話看完（現在/未來/行動，v2.2 第一個內容塊）→ KEY CALL 最重要的一個判斷** → 6-box TL;DR → 一句話 thesis box（帶 [I:]/[X:]）→ legacy cross-link callout（若有）→ PM 綠卡。

```html
<section id="s0" class="id-body">
<h2>§0 決策摘要層</h2>

<!-- 1. INVESTMENT SUMMARY — 三句話看完（v2.2，§0 第一個內容塊；同步寫進 id-meta now_state/future_state/action） -->
<div class="inv-summary">
  <div class="inv-hd">INVESTMENT SUMMARY — 三句話看完</div>
  <div class="inv-row"><div class="inv-lab">現在 / NOW</div><div class="inv-txt">{產業現況裁決（過剩/平衡/短缺）+ 最硬證據錨點}</div></div>
  <div class="inv-row"><div class="inv-lab">未來 / NEXT</div><div class="inv-txt">{3-5 年走向 + 最大結構裂縫}</div></div>
  <div class="inv-row"><div class="inv-lab">行動 / ACTION</div><div class="inv-txt">{標的層級 + 動作；允許「都不買 / 現價非進場點 / 等回調 X%」}</div></div>
</div>

<!-- 2. 6-box TL;DR -->
<div class="tldr-grid">
  <div class="tldr-card"><h4>TAM（2030）</h4><div class="v">USD {X} B</div></div>
  <div class="tldr-card"><h4>5Y CAGR</h4><div class="v">~{Y}%</div></div>
  <div class="tldr-card"><h4>投資時鐘 Phase</h4><div class="v">Phase {I/II/III/IV}</div></div>
  <div class="tldr-card"><h4>供需裁決</h4><div class="v">{過剩 / 平衡 / 短缺}</div></div>
  <div class="tldr-card"><h4>Conviction</h4><div class="v">{high / mid / low}</div></div>
  <div class="tldr-card"><h4>Top Picks</h4><div class="v">{TICKER1 / TICKER2}</div></div>
</div>

<!-- 2. 一句話 thesis box（必帶 [I:] 或 [X:] tag；同步寫入 id-meta oneliner） -->
<div class="id-thesis">
  <div class="label">核心 Thesis</div>
  <strong>{≤200 字非共識核心觀點}</strong> 🟡 [I: {事實鏈} → {結論}] 或 🔵 [X: base 很可能 / bull 可能 / bear 不太可能]
</div>

<!-- 3. KEY CALL — 本報告最重要的一個判斷（放三句話濃縮不下的深層非共識洞見，勿重述裁決字句） -->
<div class="key-judgment">
  <div class="kj-hd">KEY CALL — 本報告最重要的一個判斷</div>
  <p><strong>{那一條最反直覺、三句話容不下的深層判斷}</strong>{講清因果機制、市場為何看錯、訊號該盯哪裡}。</p>
</div>

<!-- 4. legacy cross-link callout（若同 theme 有 legacy ID/DS） -->
<div class="id-crosslink">
  本主題已有 legacy 報告：<a href="ID_{Theme}_{舊日期}.html"><strong>ID_{Theme}_{舊日期}</strong></a>（v1.x 表格 dashboard）／
  <a href="../ds/DS_{Theme}_{舊日期}.html"><strong>DS_{Theme}_{舊日期}</strong></a>（敘述版）。本份為 <strong>v2 敘事版</strong>，整合兩者。
</div>

<!-- 5. PM Implication 綠卡（必填，缺即 Gate 5 阻斷）；§7/§8/§9 完成後才寫 -->
<div class="judgment-card">
  <div class="j-head"><strong>Portfolio Implication（PM 級行動結論）</strong> <span class="j-conf high">conviction：{high/mid/low}</span></div>
  <!-- conviction：high = §9 ≥2 🔴 + §8 falsification 距離 >2 sigma；mid = ≥1 🔴 + ≥1 kill 未排除；low = thesis AT_RISK/BROKEN -->
  <ul class="j-facts" style="color:#14532D">
    <li><strong>thesis 方向</strong>：{保持 / 強化 / 降級 — 引用 §7 哪條 NC thesis 的 INTACT/AT_RISK 判斷}</li>
    <li><strong>個股 conviction tier 變化</strong>：{ticker A 從 X → Y；含 cross-ID sync 註記（cross-ID: ID_X）— 必須點名 ticker}</li>
    <li><strong>關鍵新監測點</strong>：{≤3 條可量化 metric，引 §8 證偽 row / catalyst；格式「metric ≥/≤ threshold by YYYY-QX」}</li>
    <li><strong>multiple / 估值 / 週期定位風險</strong>：{§6 de-rating window + §5 現 Phase + 下個 Phase 轉換條件 + 現價 vs entry 區間}</li>
    <li><strong>Entry 時機</strong>：{現在追高 OK / 等 catalyst [事件+日期] / 等 sector correction [X%]}</li>
  </ul>
  <div class="j-logic" style="background:rgba(22,163,74,.1);color:#14532D">→ PM 級行動：① {動詞+ticker+條件}；② {action 2}；③ {action 3}；④ {action 4}</div>
</div>
</section>
```

---

## §1 白話定義 + 歷史脈絡（含 cycle 統計表）

```html
<section id="s1" class="id-body">
<h2>§1 產業白話定義 + 歷史脈絡</h2>

<div class="id-lede">{2-3 句人話導讀：這產業賣什麼、誰付錢、為何現在重要 — 不假設讀者懂行話}</div>

<p><strong>白話開場</strong>：{第一段不准出現未解釋行話。術語首現括號內或破折號後一行白話}。</p>
<p><strong>邊界界定</strong>：{in-scope vs out-of-scope 收斂為敘事一段；為何這樣切、灰色地帶在哪}。</p>

<!-- 歷史敘事 2-3 個轉折點，每個強制：具體日期（YYYY/YYYY-MM）+ ≥1 量化錨點（Gate 9） -->
<p>第一次轉折：<strong>{YYYY-MM}</strong> {事件}，{量化錨點：% / $ / TFLOPS / GB / MAU / capacity}…</p>
<p>第二次轉折：<strong>{YYYY-MM}</strong> {事件}，{量化錨點}…</p>

<!-- 1-2 歷史類比（QC-16）：年份 + 主角 + 當年關鍵數據 + 多頭/空頭錯在哪 + 本次量化差異 -->
<p><strong>歷史類比</strong>：{YYYY} 的 {主角}，當年 {關鍵數據}。多頭錯在 {…}、空頭錯在 {…}；本次量化差異：{具體數字對照，非「這次不一樣」}。</p>

<!-- 模組 §1：歷史 cycle 統計表（≥2 輪 cycle 強制；無 cycle 註明） -->
<p class="tbl-why">把敘事歷史升級成可用於 timing 的統計量 — 看股價領先/落後基本面幾個月。</p>
<table>
  <caption>歷史 cycle 統計（過去 N 輪）</caption>
  <thead><tr><th>Cycle</th><th>起訖</th><th>長度（月）</th><th>ASP peak-to-trough</th><th>股價領先/落後基本面（月）</th></tr></thead>
  <tbody>
    <tr><td>Cycle 1</td><td>{YYYY–YYYY}</td><td>~{n}</td><td>−{XX}%</td><td>領先 ~{m}</td></tr>
    <tr><td>Cycle 2</td><td>{YYYY–YYYY}</td><td>~{n}</td><td>−{XX}%</td><td>領先 ~{m}</td></tr>
  </tbody>
</table>
<p class="tbl-read">怎麼讀：{第 1 句 — 過去 cycle 平均長度 / 振幅}；{第 2 句 — 股價領先 N 個月對今天 timing 的意義}。（無 ≥2 輪 cycle 的產業：刪表並註明「本產業尚無可統計的完整 cycle」。）</p>

<div class="id-implication">{這段歷史對今天意味著什麼 — 非顯而易見 + 可行動}</div>

<aside class="ds-refs">
  <span class="ds-refs-label">本節參考來源</span>
  <ol>
    <li><span class="tier">[T1]</span><a href="URL">Source title — claim/page</a></li>
    <li><span class="tier">[T2]</span><a href="URL">產業協會 cycle 時序 — claim</a></li>
  </ol>
</aside>
</section>
```

---

## §2 技術成熟度 + S 曲線（強制保留 S 曲線）

```html
<section id="s2" class="id-body">
<h2>§2 技術成熟度 + S 曲線</h2>

<div class="id-lede">{2-3 句：為什麼是現在，不是三年前、也不是三年後}</div>

<p>{敘事講「為什麼是現在」：哪個 bottleneck 剛被解、哪個成本曲線剛跨拐點}</p>

<!-- S-curve 強制（QC-4）：優先官方 roadmap；ASCII 為主，複雜情境改 inline SVG -->
<pre class="scurve-ascii">
採用率 / 成熟度
   │
100%│                                         ●━━━━━━━
   │                                     ╱
75%│                               ●━━━╱   ← 成熟期
   │                          ╱
50%│                     ●━━╱           ← 成長期（現在）
   │                ╱
25%│           ●━━╱                      ← 早期
   │     ╱
 0 │──●─────────────────────────────────────────────→ 時間
    {過去}   {現在}   {近未來}  {遠未來}
</pre>

<!-- 技術棧 kingmaker 小表（只放最關鍵 3-5 子技術） -->
<p class="tbl-why">點出哪個子技術成為 kingmaker — 良率卡點 × 專利持有者決定誰技術領導。</p>
<table>
  <caption>技術棧 kingmaker（關鍵 3-5 子技術）</caption>
  <thead><tr><th>子技術</th><th>良率卡點</th><th>專利/領導者</th><th>kingmaker?</th></tr></thead>
  <tbody><tr><td>{子技術}</td><td>{卡點}</td><td>{持有者}</td><td>{是/否 + 一句}</td></tr></tbody>
</table>
<p class="tbl-read">怎麼讀：{第 1 句}；{第 2 句}。</p>

<div class="id-implication">{技術成熟度對 entry timing / 哪家技術領導的含義}</div>

<aside class="ds-refs"><span class="ds-refs-label">本節參考來源</span><ol>
  <li><span class="tier">[T1]</span><a href="URL">官方 roadmap keynote slide — S 曲線數據</a></li>
</ol></aside>
</section>
```

---

## §3 供給側 + 利潤池（玩家矩陣三時間欄 / 利潤池表 / 成本曲線）

```html
<section id="s3" class="id-body">
<h2>§3 供給側：現在與未來 + 利潤池</h2>

<div class="id-lede">{2-3 句：誰在供給、瓶頸在哪、利潤被誰賺走}</div>

<!-- 玩家矩陣：T-2 / 現在 / T+1 三時間欄（看加速/穩定/衰退） -->
<p class="tbl-why">三時間欄讓你看出 share 在加速還是衰退，不只是 snapshot。</p>
<table>
  <caption>玩家矩陣（top players × share 三時間欄）</caption>
  <thead><tr><th>玩家</th><th>share T-2</th><th>現在</th><th>T+1（預估）</th><th>角色 / 護城河</th></tr></thead>
  <tbody>
    <tr><td>{玩家 A}</td><td>~{XX}%</td><td>~{XX}%</td><td>~{XX}%</td><td>{角色}</td></tr>
  </tbody>
</table>
<p class="tbl-read">怎麼讀：{誰在搶 share}；{議價權往哪段集中}。（新興供給 <3 年 → 改 T-1/當年/T+1 並 footnote 註數據起始限制。QC-17：禁 Q×4 推估。）</p>

<!-- 模組 §3-1：利潤池遷移表（強制；取代靜態毛利率表） -->
<p class="tbl-why">看整條鏈的利潤「總額」分布在哪、往哪遷、誰搶誰的池子。</p>
<table>
  <caption>利潤池遷移分析</caption>
  <thead><tr><th>環節</th><th>利潤池占比 T-2</th><th>現在</th><th>遷移方向</th><th>搶 / 被搶</th></tr></thead>
  <tbody>
    <tr><td>{上游}</td><td>~{XX}%</td><td>~{XX}%</td><td>↑/↓/→</td><td>{誰搶誰}</td></tr>
    <tr><td>{中游}</td><td>~{XX}%</td><td>~{XX}%</td><td>↑/↓/→</td><td>{}</td></tr>
    <tr><td>{下游}</td><td>~{XX}%</td><td>~{XX}%</td><td>↑/↓/→</td><td>{}</td></tr>
  </tbody>
</table>
<p class="tbl-read">怎麼讀：{利潤往哪段集中}；{遷移含義}。（QC-18：% 無 source → 改定性「主導/均勢/次要」。利潤池 value chain SVG 見 value_chain_svg.md。）</p>

<!-- 模組 §3-2：成本曲線（週期/大宗強制；結構成長型可省，須註明理由 QC-M4） -->
<p>{成本曲線敘事：主要廠商在 cost curve 位置 → 價格跌到哪 level 誰先停產（marginal producer）→ 價格戰終局。結構成長型一句註明省略理由，如「設計服務無實體產能成本曲線，價格戰由 IP 護城河而非邊際成本決定」。}</p>

<!-- 未供敘事 + 因果閉合（DS-2：§1 結構變數須在此或 §4 ≥50 字回應是否仍 binding） -->
<p><strong>未來供給</strong>：capex pipeline（誰擴 capacity、何時完成）/ 新進入者門檻 / 地緣政策 / 供給彈性（價格漲多快能擴）。</p>
<p><strong>因果閉合</strong>：{§1 提出的結構變數（某代際技術 / 護城河 / 製程獨家性）在未來 3-5 年是否仍 binding — ≥50 字直接回應，不准推到 §7}。</p>

<div class="id-implication">{12-36M 內供給能否回應需求、議價權往哪段集中}</div>

<aside class="ds-refs"><span class="ds-refs-label">本節參考來源</span><ol>
  <li><span class="tier">[T1]</span><a href="URL">玩家 IR deck — share / capacity</a></li>
  <li><span class="tier">[T2]</span><a href="URL">Yole/IC Insights — 利潤池 / 成本曲線</a></li>
</ol></aside>
</section>
```

---

## §4 需求側 + 三角驗證（TAM 三情境含推導 / 三角對帳）

```html
<section id="s4" class="id-body">
<h2>§4 需求側：現在與未來 + 三角驗證</h2>

<div class="id-lede">{2-3 句：誰在買、為何買、哪塊需求最不可替代}</div>

<p><strong>現需</strong>：end-market mix / 地域 / 客戶集中度 / pricing power（哪段需求最 price inelastic）。</p>

<!-- TAM 三情境表含推導鏈（每個數字「推導：A×B→C」可回溯，Gate 7） -->
<p class="tbl-why">base/bull/bear 三情境，每個數字都能回溯到「假設改了什麼」。</p>
<table>
  <caption>TAM 三情境（含推導鏈）</caption>
  <thead><tr><th>情境</th><th>{YYYY}E TAM</th><th>核心假設</th><th>推導</th></tr></thead>
  <tbody>
    <tr><td><strong>Base</strong></td><td>~${X}B</td><td>{兌現度 100%}</td><td>推導：capex ${A}B × workload {B}% × accel ratio {C} → ${X}B</td></tr>
    <tr><td>Bull</td><td>~${X+}B</td><td>{兌現度 120%}</td><td>推導：base × 1.2（FOMO 加碼）→ ${X+}B</td></tr>
    <tr><td>Bear</td><td>~${X-}B</td><td>{兌現度 75%}</td><td>推導：base × 0.75（衰退）→ ${X-}B</td></tr>
  </tbody>
</table>
<p class="tbl-read">怎麼讀：{bull/bear 偏離 base 來自哪個 input}；{對 TAM 的信心}。</p>

<!-- 模組 §4：需求三角驗證（硬規則；差 >20% 必解釋缺口 QC-M2） -->
<p><strong>三角驗證</strong>：top-down TAM ${X}B vs bottom-up（下游客戶 capex/採購 guidance 加總 ${P}B vs 上游廠商營收 consensus 加總 ${Q}B）。{兩邊差 {Δ}%；若 >20% → 缺口在哪（重複計算 / 樂觀滲透率 / 口徑不同）+ 採信哪邊、為什麼}。</p>

<!-- 因果閉合：§1 需求驅動（生成式 AI / 生育率 / 老化）在 §4 回應 5-10Y 走向 / 拐點 -->
<p><strong>因果閉合</strong>：{§1 提及的需求驅動未來 5-10 年走向 / 是否拐點}。</p>

<div class="id-implication">{哪塊需求最有定價權、TAM forecast 史上偏差、需求拐點}</div>

<aside class="ds-refs"><span class="ds-refs-label">本節參考來源</span><ol>
  <li><span class="tier">[T1]</span><a href="URL">下游客戶法說 — capex guidance（bottom-up）</a></li>
  <li><span class="tier">[T2]</span><a href="URL">市場研究機構 — top-down TAM</a></li>
</ol></aside>
</section>
```

---

## §5 供需裁決 + 推估 + 投資時鐘（資本週期 / 三視野×三情境 / 庫存指標）

```html
<section id="s5" class="id-body">
<h2>§5 供需裁決 + 短中長期推估 + 投資時鐘</h2>
<div class="judgment-banner">⚠️ 本章含 judgment：🟡 bullet 代表推論，附事實鏈與信心度 + ⚠ 證偽條件</div>

<div class="id-lede">{2-3 句先給結論方向：綜合 §3 §4，本產業未來 X 年是過剩/平衡/短缺}</div>

<!-- 模組 §5-1：資本週期證據（裁決至少引 2 項 QC-M1） -->
<p><strong>資本週期證據</strong>：① capex/折舊比趨勢 {…}；② 產業 ROIC {…} vs WACC {…}（[A:] 假設註明）；③ 新產能 lead time {…}。「高報酬引資本→過剩→均值回歸」機制檢查 — 至少引其中 2 項。</p>

<!-- 強制裁決（三選一不准騎牆，DS bridge） -->
<div class="id-bridge">
  <div class="label">§3 + §4 → 供需裁決</div>
  <p>依本章 §3 與 §4 的推導，未來 X 年產業供需狀態是 <strong>{過剩 / 平衡 / 短缺}</strong>，因為 {具體原因}。{允許「短期 X 中長期 Y」分時間段，但每段明確}。</p>
</div>

<!-- 三視野 × 三情境表（每 cell 可量化 trigger + 推導，Gate 7） -->
<p class="tbl-why">12M / 3Y / 5Y+ 各 base/bull/bear，trigger 必須可量化、可回溯。</p>
<table>
  <caption>三視野 × 三情境推估</caption>
  <thead><tr><th>Horizon</th><th>Base</th><th>Bull</th><th>Bear</th><th>Trigger metric（推導）</th></tr></thead>
  <tbody>
    <tr><td><strong>12M</strong></td><td>{量化}</td><td>{量化}</td><td>{量化}</td><td>{e.g. NVDA inference run-rate ≥ $80B annualized（推導：DC rev $130B × 60% inference）}</td></tr>
    <tr><td><strong>3Y</strong></td><td>…</td><td>…</td><td>…</td><td>{trigger 推導}</td></tr>
    <tr><td><strong>5Y+</strong></td><td>…</td><td>…</td><td>…</td><td>{trigger 推導}</td></tr>
  </tbody>
</table>
<p class="tbl-read">怎麼讀：{每 horizon 邏輯}；{trigger 禁「demand booms」這種模糊詞}。</p>

<!-- 投資時鐘 phase 判定 + 必要∩充分條件 -->
<p><strong>投資時鐘</strong>：當前 Phase {I/II/III/IV} + 各 phase 贏家切換 + 換 phase 的必要 ∩ 充分條件。</p>

<!-- 模組 §5-2：庫存/訂單指標（產業適用時強制；軟體服務改 NRR/RPO QC-M6） -->
<p><strong>庫存/訂單指標</strong>：channel inventory {n} 週 / book-to-bill {x} / backlog {m} 月。{軟體服務類改 NRR / backlog / RPO / billings 並說明用了哪個替代指標及理由}。</p>

<div class="id-implication">{本產業現在處於 cycle 哪段、下個 phase 觸發條件、現在 act 還是等}</div>

<aside class="ds-refs"><span class="ds-refs-label">本節參考來源</span><ol>
  <li><span class="tier">[T1]</span><a href="URL">財報 — capex/折舊、ROIC</a></li>
  <li><span class="tier">[T2]</span><a href="URL">SEMI book-to-bill / 庫存週數</a></li>
</ol></aside>
</section>
```

---

## §6 產業經濟學 + 估值傳導

```html
<section id="s6" class="id-body">
<h2>§6 產業經濟學與估值傳導</h2>

<div class="id-lede">{2-3 句：這產業的錢怎麼賺、估值跟著什麼變數動}</div>

<!-- unit economics / ASP 表（1 表） -->
<p class="tbl-why">看 unit economics 與 ASP 動態 + 抗 commoditization 能力。</p>
<table>
  <caption>unit economics / ASP 動態</caption>
  <thead><tr><th>指標</th><th>過去 5Y</th><th>未來 2Y</th><th>抗 commoditization</th></tr></thead>
  <tbody>
    <tr><td>ROIC / Gross / Capex cycle</td><td>{}</td><td>{}</td><td>{}</td></tr>
    <tr><td>ASP（{單位}）</td><td>{}</td><td>{}</td><td>{}</td></tr>
  </tbody>
</table>
<p class="tbl-read">怎麼讀：{ASP 趨勢}；{抗價格戰能力}。</p>

<!-- 估值傳導（敘事 + 敏感度錨點） -->
<p><strong>估值傳導</strong>：產業變數 → 公司 Fwd PE/PEG 怎麼 pass-through。敏感度錨點：{+1pp 毛利 ⇒ ~? 倍數擴張}。</p>

<div class="id-implication">{估值現在 price 了什麼、哪個變數動會 re-rate / de-rating}</div>

<aside class="ds-refs"><span class="ds-refs-label">本節參考來源</span><ol>
  <li><span class="tier">[T1]</span><a href="URL">財報 — ROIC / ASP</a></li>
</ol></aside>
</section>
```

---

## §7 Non-Consensus + Priced-in + Kill Scenario

```html
<section id="s7" class="id-body">
<h2>§7 Non-Consensus + Priced-in 檢驗 + Kill Scenario</h2>
<div class="judgment-banner">⚠️ 本章含 judgment：每條分歧附 [F:] cornerstone + [X:] 三情境 + priced-in</div>

<div class="id-lede">{2-3 句：市場主流怎麼看、我們哪裡不同、為何這分歧還能賺錢}</div>

<!-- 3 個分歧（bullet 並列）；每條：共識 X（引 T3）/ 我們 Y / 證據 Z（§1-§6）/ 市場 price 多少 -->
<div class="judgment-card">
  <div class="j-head"><span>🟡</span><span>分歧 1：{標題}</span><span class="j-conf high">信心：高</span></div>
  <ul class="j-facts">
    <li>共識說 X：{引 ≥1 主流券商/媒體 T3} 🟢 [F: T3-A: …]</li>
    <li>我們說 Y：{§1-§6 某處事實 Z 支撐} 🔵 [X: base 很可能 / bull 可能 / bear 不太可能]</li>
    <li><strong>Priced-in</strong>：sector 估值歷史分位 {現在 EV/Sales 在過去兩輪 cycle 第 {p} 百分位}；現價隱含 {reverse 推回市場隱含 CAGR / margin}（推導：…）。{分歧對但已 priced → 標「不可操作」}</li>
  </ul>
  <div class="j-logic">→ 推論邏輯：{為何 Y 對且未 priced}　⚠ 證偽：{什麼發生就推翻}</div>
</div>
<!-- 分歧 2 / 分歧 3 同結構 -->

<!-- 3 個 steel-man 反方（QC-11）：具體路徑 + 當前證據 + 證偽窗口 -->
<h3>Steel-man 反方（最有力的 3 條）</h3>
<ul>
  <li>反方 1：{具體路徑} + {當前證據} + {證偽窗口}</li>
  <li>反方 2：…</li>
  <li>反方 3：…</li>
</ul>

<!-- 風險矩陣降級為敘事素材 -->
<p>{技術/需求/替代 + 政策補貼管制 融入敘事；點名「市場最低估的風險」}。</p>

<div class="id-implication">{這三條分歧裡哪條最可操作（對 + 未 priced）}</div>

<aside class="ds-refs"><span class="ds-refs-label">本節參考來源</span><ol>
  <li><span class="tier">[T3-A]</span><a href="URL">券商 primer p.XX — 共識 / 估值分位</a></li>
</ol></aside>
</section>
```

---

## §8 Catalyst Timeline + 證偽表

```html
<section id="s8" class="id-body">
<h2>§8 Catalyst Timeline + 證偽表</h2>
<div class="judgment-banner">⚠️ 本章含 judgment：每條 metric ≥1 [X:] 三情境閾值</div>

<div class="id-lede">{2-3 句：未來 18 個月盯哪些節點、哪些數字一破就要砍}</div>

<!-- Catalyst（18M 內 5-8 個，bullet 並列）：日期 + 類別 + 指標 + 雙路徑（QC-12） -->
<p>未來 18 個月最關鍵的 5-8 個節點：</p>
<p><strong class="id-time">{YYYY-MM-DD}</strong> {事件}。檢視 {指標}。<span class="ds-path-positive">若達成（{閾值}）</span> → {動作}。<span class="ds-path-negative">若落空（{閾值}）</span> → {觸發 §7 哪條反方 / 重檢哪檔}。</p>
<p><strong class="id-time">{YYYY-Q4}</strong> {事件}。<span class="ds-path-positive">若達成</span> → … <span class="ds-path-negative">若落空</span> → …</p>

<!-- 證偽表（position-thesis-monitor 的輸入；QC-13 真 falsification）-->
<p class="tbl-why">3-5 個 kill metric + base/bull/bear 閾值 + 時間窗。bear 閾值即 thesis 作廢點。</p>
<table>
  <caption>證偽表（kill metrics）</caption>
  <thead><tr><th>Metric</th><th>Base</th><th>Bull</th><th>Bear（thesis 作廢）</th><th>時間窗</th></tr></thead>
  <tbody>
    <tr><td>{metric 1}</td><td>{range}</td><td>{range}</td><td>{真 falsification range}</td><td>{by YYYY-QX}</td></tr>
  </tbody>
</table>
<p class="tbl-read">怎麼讀：{bear 觸發點對應哪條反方}；{數字用 range，非 strawman}。</p>

<div class="id-implication">{最該盯的 1-2 個 leading indicator}</div>

<aside class="ds-refs"><span class="ds-refs-label">本節參考來源</span><ol>
  <li><span class="tier">[T1]</span><a href="URL">財報 / 法說 — catalyst 指標基準</a></li>
</ol></aside>
</section>
```

---

## §9 關聯個股（🔴🟡🟢 表 ≤16 行 + caption 時間限定 + non-obvious）

```html
<section id="s9" class="id-body">
<h2>§9 關聯個股</h2>

<div class="id-lede">{2-3 句：誰是純度玩家、誰是市場沒注意到的二次受益者}</div>

<p>本 ID 對應個股、角色與深度（stock-analyst 自動讀取本表 + id-meta related_tickers）：</p>

<table class="id-tickers">
  <caption>🔴 核心（營收 >40% 依賴 OR 技術領導）｜🟡 次要（10-40%）｜🟢 邊緣（<10% 但被連動）。閾值為 {current 2026-Q1 actual / forward-looking by 2028}（Gate 10-2 時間限定）。</caption>
  <thead><tr><th>Ticker</th><th>深度</th><th>受益/受害</th><th>營收曝險（current actual）</th><th>角色</th><th>DD 連結</th></tr></thead>
  <tbody>
    <tr>
      <td><strong>NVDA</strong></td>
      <td><span class="tier-pill tier-red">🔴 核心</span></td>
      <td>受益</td>
      <td>~60%（2026-Q1 actual）</td>
      <td>AI GPU 設計與封裝 driver</td>
      <td><a href="../dd/DD_NVDA_20260418.html">DD</a></td>
    </tr>
    <!-- forward-looking 範例：AMD 雖 current ~8%，但 projected 45% by 2028 → 標 🔴；表內列 current actual 對照 -->
  </tbody>
</table>

<!-- 1-2 個非顯而易見受益者（強制） -->
<p><strong>非顯而易見受益者</strong>：{e.g. 本產業需某設備 → 該設備的乾燥爐供應商 {ticker}；理由}。</p>

<div class="id-implication">{哪檔是最高純度 play、哪檔被低估其曝險}</div>

<aside class="ds-refs"><span class="ds-refs-label">本節參考來源</span><ol>
  <li><span class="tier">[T1]</span><a href="URL">{ticker} 營收 breakdown — 曝險 %</a></li>
</ol></aside>
</section>
```

---

## 新模組表格骨架速查

| 模組 | 落點 | 表頭 |
|:---|:---|:---|
| cycle 統計 | §1 | `Cycle｜起訖｜長度(月)｜ASP peak-to-trough｜股價領先/落後(月)` |
| 玩家矩陣 | §3 | `玩家｜share T-2｜現在｜T+1｜角色/護城河`（三時間欄） |
| 利潤池 | §3 | `環節｜利潤池占比 T-2｜現在｜遷移方向｜搶/被搶` |
| TAM 三情境 | §4 | `情境｜TAM｜核心假設｜推導`（含推導行） |
| 三視野×三情境 | §5 | `Horizon｜Base｜Bull｜Bear｜Trigger metric（推導）` |
| 證偽表 | §8 | `Metric｜Base｜Bull｜Bear（作廢）｜時間窗` |
| ticker 表 | §9 | `Ticker｜深度｜受益/受害｜營收曝險(current actual)｜角色｜DD`（caption 時間限定） |

S 曲線見上方 §2 樣板（`scurve_ascii.md` 樣式）；利潤池 value chain SVG 見 `value_chain_svg.md`。
