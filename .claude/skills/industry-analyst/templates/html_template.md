# 產業 DD HTML Template v1.0

## 檔名規則

`docs/id/ID_{Theme_CamelCase}_{YYYYMMDD}.html`

- Theme_CamelCase 範例：GlassSubstrate / HBM_Supercycle / AIASIC_vs_GPU / GLP1_Landscape / EUV_NextGen

## 基本骨架

```html
<!DOCTYPE html>
<html lang="zh-Hant"><head>
<meta charset="UTF-8">
<meta name="id-skill-version" content="v1.0">
<meta name="id-theme" content="{THEME}">
<meta name="id-publish-date" content="{YYYY-MM-DD}">
<title>產業深度 — {THEME}（{YYYY-MM-DD}）</title>
<script id="id-meta" type="application/json">
{
  "theme": "{THEME}",
  "skill_version": "v1.0",
  "id_version": "v1.0",
  "publish_date": "{YYYY-MM-DD}",
  "thesis_type": "structural",
  "ai_exposure": "🟡",
  "oneliner": "{≤200 字，本 ID 核心 thesis 一句話 — 不可截斷}",
  "related_tickers": [
    {"ticker": "{TICKER}", "role": "{角色描述}", "depth": "🔴", "beneficiary": true}
  ]
}
</script>
<style>{SHARED_STYLES}</style>
</head><body>

<header class="id-head">
  <div class="id-badge">產業深度 · Industry DD</div>
  <h1>{THEME}</h1>
  <p class="id-meta">發布日：{YYYY-MM-DD} ｜ 涵蓋股票：{N} ｜ 🟡 占比：{PCT}% ｜ v1.0</p>
</header>

<section id="s0"> ... TL;DR ... </section>
<section id="s1"> ... 定義 ... </section>
...
<section id="s11"> ... 關聯個股 ... </section>

<footer class="id-foot">
  <p>產業深度報告 · industry-analyst v1.0 · {THEME} · {YYYY-MM-DD} · 🟡 占比：{PCT}%</p>
  <p><a href="/research/">← 回研究首頁</a> · <a href="/id/">所有產業報告</a></p>
</footer>
</body></html>
```

## 共用 CSS（貼到 `<style>`）

```css
body{font-family:-apple-system,'Noto Sans TC',sans-serif;background:#FAFAF9;color:#1E1B4B;margin:0;padding:24px;max-width:1040px;margin:0 auto;font-size:14px;line-height:1.65}
.id-head{border-bottom:3px solid #7C3AED;padding-bottom:12px;margin-bottom:24px}
.id-badge{display:inline-block;background:#7C3AED;color:#fff;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600;letter-spacing:.5px;margin-bottom:6px}
h1{color:#4C1D95;font-size:24px;margin:4px 0}
.id-meta{color:#6B7280;font-size:12px;margin:4px 0}
h2{color:#4C1D95;border-left:4px solid #7C3AED;padding-left:10px;margin:30px 0 10px;font-size:17px}
h3{color:#5B21B6;margin:16px 0 6px;font-size:14px}
table{width:100%;border-collapse:collapse;margin:8px 0 14px;font-size:13px;background:#fff;box-shadow:0 1px 3px rgba(76,29,149,.08)}
th{background:#4C1D95;color:#fff;padding:8px;text-align:left;font-weight:500}
td{padding:7px 8px;border-bottom:1px solid #E5E7EB;vertical-align:top}
tr:hover td{background:#FAF5FF}

.judgment-banner{background:#FEF9C3;border-left:4px solid #EAB308;padding:10px 14px;margin:8px 0 14px;border-radius:4px;color:#713F12;font-size:13px}
.judgment-card{background:#FEF9C3;border-left:4px solid #EAB308;border-radius:4px;padding:12px 14px;margin:10px 0}
.judgment-card .j-head{display:flex;align-items:center;gap:8px;font-weight:600;color:#713F12;margin-bottom:6px}
.j-conf{display:inline-block;font-size:11px;padding:1px 8px;border-radius:10px;font-weight:600}
.j-conf.high{background:#DCFCE7;color:#166534}
.j-conf.mid{background:#FEF3C7;color:#92400E}
.j-conf.low{background:#FEE2E2;color:#991B1B}
.j-facts{font-size:12.5px;color:#713F12;margin:6px 0;padding-left:20px}
.j-logic{font-size:12.5px;color:#713F12;margin-top:6px;padding:6px 10px;background:rgba(234,179,8,.08);border-radius:3px}

.tier-pill{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11px;font-weight:600}
.tier-red{background:#FEE2E2;color:#991B1B}
.tier-yellow{background:#FEF3C7;color:#92400E}
.tier-green{background:#DCFCE7;color:#166534}

.scurve-ascii{background:#F5F3FF;color:#4C1D95;padding:12px 14px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-size:12px;white-space:pre;line-height:1.4;overflow-x:auto;border:1px solid #DDD6FE}

.vc-svg{display:block;max-width:100%;margin:12px auto}

.source-tag{color:#6B7280;font-size:11px}
.source-tag a{color:#7C3AED}

.tldr-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:10px 0 20px}
.tldr-card{background:#fff;border:1px solid #E5E7EB;border-radius:6px;padding:12px;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.tldr-card h4{margin:0 0 6px;color:#6B21A8;font-size:11px;letter-spacing:.5px;text-transform:uppercase;font-weight:600}
.tldr-card .v{font-size:15px;font-weight:600;color:#1E1B4B;line-height:1.35}

.foot{margin-top:32px;padding-top:16px;border-top:1px solid #E5E7EB;color:#6B7280;font-size:11px;text-align:center}
```

## §0 TL;DR 卡片 區塊範例

```html
<section id="s0">
<h2>§0 TL;DR</h2>
<div class="tldr-grid">
  <div class="tldr-card"><h4>主題</h4><div class="v">{主題一句話}</div></div>
  <div class="tldr-card"><h4>時長</h4><div class="v">{短期/中期/長期 主軸}</div></div>
  <div class="tldr-card"><h4>2030 規模</h4><div class="v">USD {X} B</div></div>
  <div class="tldr-card"><h4>關鍵玩家</h4><div class="v">{A / B / C}</div></div>
  <div class="tldr-card"><h4>關鍵風險</h4><div class="v">{一句話}</div></div>
  <div class="tldr-card"><h4>今日 Phase</h4><div class="v">Phase {I/II/III}</div></div>
</div>
</section>
```

## §2 S 曲線（ASCII 樣板）

```html
<section id="s2">
<h2>§2 技術演進史 + S 曲線</h2>
<table>
  <tr><th>階段</th><th>時間</th><th>技術代表</th><th>瓶頸</th></tr>
  <tr><td>過去</td><td>{年份}</td><td>{技術}</td><td>{瓶頸}</td></tr>
  <tr><td>現在</td><td>{年份}</td><td>{技術}</td><td>{瓶頸}</td></tr>
  <tr><td>未來</td><td>{年份}</td><td>{技術}</td><td>{瓶頸}</td></tr>
</table>
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
    2020   2023   2026   2029   2032
          {過去}  {現在} {近未來} {遠未來}
</pre>
</section>
```

## §5 Value Chain inline SVG 樣板

```html
<section id="s5">
<h2>§5 供應鏈 Value Chain</h2>
<svg class="vc-svg" viewBox="0 0 900 220" xmlns="http://www.w3.org/2000/svg">
  <!-- 上游 -->
  <rect x="20"  y="40" width="240" height="140" rx="8" fill="#EDE9FE" stroke="#7C3AED" stroke-width="2"/>
  <text x="140" y="72" text-anchor="middle" font-size="14" font-weight="700" fill="#4C1D95">上游</text>
  <text x="140" y="98" text-anchor="middle" font-size="12" fill="#5B21B6">{子類別}</text>
  <text x="140" y="120" text-anchor="middle" font-size="11" fill="#1E1B4B">毛利 {XX%}</text>
  <text x="140" y="140" text-anchor="middle" font-size="11" fill="#1E1B4B">代表 {公司}</text>
  <!-- 中游 -->
  <rect x="330" y="40" width="240" height="140" rx="8" fill="#DDD6FE" stroke="#7C3AED" stroke-width="2"/>
  <text x="450" y="72" text-anchor="middle" font-size="14" font-weight="700" fill="#4C1D95">中游</text>
  <text x="450" y="98" text-anchor="middle" font-size="12" fill="#5B21B6">{子類別}</text>
  <text x="450" y="120" text-anchor="middle" font-size="11" fill="#1E1B4B">毛利 {XX%}</text>
  <text x="450" y="140" text-anchor="middle" font-size="11" fill="#1E1B4B">代表 {公司}</text>
  <!-- 下游 -->
  <rect x="640" y="40" width="240" height="140" rx="8" fill="#C4B5FD" stroke="#7C3AED" stroke-width="2"/>
  <text x="760" y="72" text-anchor="middle" font-size="14" font-weight="700" fill="#4C1D95">下游</text>
  <text x="760" y="98" text-anchor="middle" font-size="12" fill="#5B21B6">{子類別}</text>
  <text x="760" y="120" text-anchor="middle" font-size="11" fill="#1E1B4B">毛利 {XX%}</text>
  <text x="760" y="140" text-anchor="middle" font-size="11" fill="#1E1B4B">代表 {公司}</text>
  <!-- 箭頭 -->
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7C3AED"/>
    </marker>
  </defs>
  <line x1="260" y1="110" x2="330" y2="110" stroke="#7C3AED" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="570" y1="110" x2="640" y2="110" stroke="#7C3AED" stroke-width="2" marker-end="url(#arrow)"/>
</svg>
</section>
```

## §8-§10 🟡 判斷卡片樣板

```html
<div class="judgment-banner">⚠️ 本章含 judgment：🟡 bullet 代表推論，附事實鍊與信心度</div>

<div class="judgment-card">
  <div class="j-head">
    <span>🟡</span>
    <span>{推論結論標題}</span>
    <span class="j-conf high">信心：高</span>
  </div>
  <ul class="j-facts">
    <li>事實 1：{可驗證事實} <span class="source-tag">[source: <a href="URL">URL</a>]</span></li>
    <li>事實 2：{可驗證事實} <span class="source-tag">[source: ...]</span></li>
  </ul>
  <div class="j-logic">→ 推論邏輯：{為何從事實得出結論}</div>
</div>
```

## §11 關聯個股清單

```html
<section id="s11">
<h2>§11 關聯個股清單</h2>
<table>
  <tr><th>Ticker</th><th>深度</th><th>受益 / 受害</th><th>營收曝險</th><th>角色</th><th>DD 連結</th></tr>
  <tr>
    <td>NVDA</td>
    <td><span class="tier-pill tier-red">🔴 核心</span></td>
    <td>受益</td>
    <td>~60%</td>
    <td>AI GPU 設計與封裝 driver</td>
    <td><a href="/dd/DD_NVDA_20260418.html">DD</a></td>
  </tr>
  <!-- ... -->
</table>
</section>
```

## 頁尾 footer 固定樣式

```html
<footer class="foot">
  產業深度報告 · industry-analyst v1.0 · {THEME} · 發布日 {YYYY-MM-DD} · 🟡 占比 {PCT}%<br>
  <a href="/research/">回研究首頁</a> · <a href="/id/">所有產業報告</a>
</footer>
```
