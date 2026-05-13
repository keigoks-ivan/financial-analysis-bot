# 產業敘述（DS）HTML Template v1.2

## 檔名規則

`docs/ds/DS_{Theme_CamelCase}_{YYYYMMDD}.html`

範例：
- `DS_AIAcceleratorDemand_20260512.html`
- `DS_GlobalShippingCycle_20260601.html`
- `DS_HBMSupplyDemand_20260520.html`

## 基本骨架

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="ds-skill-version" content="v1.2">
<meta name="ds-theme" content="{THEME_CAMELCASE}">
<meta name="ds-publish-date" content="{YYYY-MM-DD}">
<title>產業敘述 — {THEME 中文}（{YYYY-MM-DD}）</title>
<script id="ds-meta" type="application/json">
{
  "theme": "{THEME 敘述}",
  "skill_version": "v1.2",
  "ds_version": "v1.0",
  "publish_date": "{YYYY-MM-DD}",
  "thesis_type": "mixed",
  "ai_exposure": "🟡",
  "mega": "{semi | bio | ...}",
  "sub_group": "{對應子群組}",
  "quality_tier": "Q1",
  "oneliner": "{≤ 200 字一句話 thesis}",
  "history_window_years": 25,
  "forecast_horizon_years": 5,
  "related_tickers": [
    {"ticker": "{TICKER}", "role": "{角色}", "depth": "🔴", "beneficiary": true}
  ],
  "related_ids": ["ID_{Theme}_{YYYYMMDD}"],
  "sections_refreshed": {
    "history": "{YYYY-MM-DD}",
    "supply_demand": "{YYYY-MM-DD}",
    "forecast": "{YYYY-MM-DD}"
  }
}
</script>
<style>{DS_STYLES}</style>
</head>
<body>

<header class="ds-head">
  <div class="ds-badge">產業敘述 · Industry Discourse</div>
  <h1>{THEME 中文}</h1>
  <p class="ds-meta">發布日：{YYYY-MM-DD} ｜ 涵蓋股票：{N} ｜ 歷史窗口：{H} 年 ｜ 預測範圍：{F} 年 ｜ v1.2</p>
</header>

<section id="s0"> ... TL;DR + cross-link callout ... </section>
<section id="s1"> ... 產業歷史脈絡 ... </section>
<section id="s2"> ... 現在供給結構 ... </section>
<section id="s3"> ... 未來供給趨勢 ... </section>
<section id="s4"> ... 現在需求結構 ... </section>
<section id="s5"> ... 未來需求趨勢（含 TAM）... </section>
<section id="s6"> ... 短 / 中 / 長期推估 ... </section>
<section id="s7"> ... 投資時鐘 + Phase 轉換 ... </section>
<section id="s8"> ... Non-Consensus View ... </section>
<section id="s9"> ... 風險與 Kill Scenario ... </section>
<section id="s10"> ... Catalyst Timeline ... </section>
<section id="s11"> ... 關聯個股清單 ... </section>

<footer class="ds-foot">
  <p>產業敘述報告 · industry-ds v1.2 · {THEME} · {YYYY-MM-DD}</p>
  <p><a href="/research/">← 回研究首頁</a> · <a href="/ds/">所有產業 DS 報告</a> · <a href="/id/">產業 ID 報告</a></p>
</footer>
</body></html>
```

## 共用 CSS（貼到 `<style>`）

```css
body{font-family:-apple-system,'Noto Sans TC','Noto Serif TC',sans-serif;background:#FAFAF9;color:#1E1B4B;margin:0;padding:24px;max-width:880px;margin:0 auto;font-size:15px;line-height:1.85}
.ds-head{border-bottom:3px solid #7C3AED;padding-bottom:14px;margin-bottom:28px}
.ds-badge{display:inline-block;background:#7C3AED;color:#fff;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600;letter-spacing:.5px;margin-bottom:6px}
h1{color:#4C1D95;font-size:26px;margin:4px 0;letter-spacing:-.02em;line-height:1.3}
.ds-meta{color:#6B7280;font-size:12.5px;margin:6px 0}

/* DS 的核心是文字：把段落間距、字體大小、行高都調整到適合長文閱讀 */
h2{color:#4C1D95;border-left:4px solid #7C3AED;padding-left:12px;margin:36px 0 14px;font-size:19px;font-weight:700;letter-spacing:-.01em}
h3{color:#5B21B6;margin:22px 0 8px;font-size:15px;font-weight:600}
p{margin:12px 0;line-height:1.85}
.ds-body p{text-align:justify;text-justify:inter-character;hyphens:auto}
strong{color:#4C1D95;font-weight:700}
em{color:#5B21B6;font-style:normal;font-weight:600}

/* 表格樣式 — DS 用得少，刻意小巧 */
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:13px;background:#fff;box-shadow:0 1px 3px rgba(76,29,149,.06)}
th{background:#4C1D95;color:#fff;padding:8px 10px;text-align:left;font-weight:500;font-size:12.5px}
td{padding:8px 10px;border-bottom:1px solid #E5E7EB;vertical-align:top;font-size:13px}
tr:hover td{background:#FAF5FF}
caption{caption-side:top;color:#6B7280;font-size:11.5px;text-align:left;padding:4px 0 8px;font-style:normal}

/* TL;DR thesis box（§0 唯一允許的 callout 容器） */
.ds-thesis{background:linear-gradient(135deg,#F5F3FF 0%,#EDE9FE 100%);border-left:4px solid #7C3AED;padding:16px 20px;margin:18px 0 24px;border-radius:6px;font-size:14.5px;color:#1E1B4B;line-height:1.75}
.ds-thesis .label{display:inline-block;background:#7C3AED;color:#fff;padding:2px 9px;border-radius:3px;font-size:10.5px;letter-spacing:.5px;font-weight:600;text-transform:uppercase;margin-bottom:8px}
.ds-thesis strong{color:#4C1D95}

/* Cross-link callout (§0 if related_ids exists) */
.ds-crosslink{background:#F5F3FF;border-left:4px solid #7C3AED;padding:10px 14px;margin:8px 0 18px;border-radius:4px;font-size:13px;color:#4C1D95;line-height:1.7}
.ds-crosslink a{color:#7C3AED;font-weight:600}
.ds-crosslink a:hover{text-decoration:underline}

/* 章末「💡 對投資的意義」段落 */
.ds-implication{background:#FFFBEB;border-left:3px solid #F59E0B;padding:12px 16px;margin:18px 0 12px;border-radius:4px;font-size:14px;color:#78350F;line-height:1.75}
.ds-implication::before{content:"💡 對投資的意義";display:block;font-weight:700;color:#92400E;font-size:11.5px;letter-spacing:.5px;text-transform:uppercase;margin-bottom:6px}

/* 因果橋（§5 → §6 銜接，明確標出供需平衡結論） */
.ds-bridge{background:#ECFEFF;border-left:4px solid #0891B2;padding:14px 18px;margin:20px 0;border-radius:4px;font-size:14.5px;color:#164E63;line-height:1.8}
.ds-bridge .label{display:inline-block;background:#0891B2;color:#fff;padding:2px 9px;border-radius:3px;font-size:10.5px;letter-spacing:.5px;font-weight:600;text-transform:uppercase;margin-bottom:8px}
.ds-bridge strong{color:#155E75}

/* Catalyst 時間錨點（§10 用） */
time, strong.ds-time{display:inline;background:#EDE9FE;color:#5B21B6;padding:1px 6px;border-radius:3px;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:13px;font-weight:600;letter-spacing:.5px;white-space:nowrap}
time:hover, strong.ds-time:hover{background:#DDD6FE}

/* §10 雙路徑（若達成 / 若落空） */
.ds-path-positive{color:#166534;font-weight:600}
.ds-path-negative{color:#991B1B;font-weight:600}

/* §11 ticker table — 緊湊一些 */
.ds-tickers{font-size:12.5px}
.ds-tickers .depth-red{color:#DC2626;font-weight:700}
.ds-tickers .depth-yellow{color:#D97706;font-weight:700}
.ds-tickers .depth-green{color:#059669;font-weight:700}

/* §末 references aside（v1.2：取代 inline source-tag） */
.ds-refs{margin:28px 0 8px;padding:10px 14px;background:#FAFAF9;border-left:2px solid #D1D5DB;border-radius:3px;font-size:12px;color:#6B7280;line-height:1.7}
.ds-refs .ds-refs-label{color:#4B5563;font-size:10.5px;letter-spacing:.5px;text-transform:uppercase;display:block;margin-bottom:6px;font-weight:700}
.ds-refs ol{margin:0;padding-left:20px}
.ds-refs li{margin:3px 0}
.ds-refs a{color:#7C3AED;text-decoration:none}
.ds-refs a:hover{text-decoration:underline}
.ds-refs .tier{display:inline-block;color:#4B5563;font-weight:600;margin-right:6px;font-size:11px}

/* T3-only section warning */
.source-warning{background:#FEF3C7;border-left:3px solid #F59E0B;padding:10px 14px;margin:14px 0;font-size:12px;color:#78350F;border-radius:3px}

/* Footer */
.ds-foot{margin-top:48px;padding-top:18px;border-top:1px solid #E5E7EB;color:#6B7280;font-size:12px;text-align:center;line-height:1.8}
.ds-foot a{color:#7C3AED;text-decoration:none}
.ds-foot a:hover{text-decoration:underline}

@media (max-width:720px){
  body{padding:18px}
  h1{font-size:22px}
  h2{font-size:17px}
  p{font-size:14.5px}
}

@media print{
  body{padding:12px;max-width:none;font-size:11pt;line-height:1.6}
  .ds-thesis,.ds-implication,.ds-bridge{break-inside:avoid}
}
```

## §0 TL;DR 段落範例

**§0 內順序固定**：thesis box → cross-link callout（若有同 theme ID） → intro paragraph → 編輯記錄 details（若有 critic patch；預設 collapsed）。

```html
<section id="s0" class="ds-body">
<h2>§0 TL;DR</h2>

<!-- 1. Thesis box — §0 必填、放最前面（讀者第一眼看到核心 thesis） -->
<div class="ds-thesis">
  <div class="label">核心 Thesis</div>
  <strong>AI 加速器需求進入「推論主導 + 結構性電力瓶頸 + 客製化 ASIC 蠶食」三軌混合期</strong>：訓練週期 2024-2025 高峰已過、推論 run-rate 2026-2027 取代訓練成 demand 主軸；供給端電力 lead time（2-3 年）已超過晶片 lead time，重新定義成本曲線；hyperscaler ASIC 2028 將佔加速器 capex 35-45%（共識 20-25%）。
</div>

<!-- 2. Cross-link callout — 若同 theme 有 ID 則必填 -->
<div class="ds-crosslink">
  📊 本主題已有 ID 報告：<a href="../id/ID_AIAcceleratorDemand_20260419.html"><strong>ID_AIAcceleratorDemand_20260419</strong></a> — 表格 dashboard 視角，建議與本 DS 互補閱讀。
</div>

<!-- 3. Intro paragraph — 展開 thesis 的 narrative bridge -->
<p>本 DS 以 25 年產業史為起點，回顧 GPU 從遊戲卡到 AI 訓練工具、再到推論基建的三次轉折，據此推演未來 5 年供需平衡：現在供給以 NVDA / AMD / 自研 ASIC 三軌共存，但電力（不是晶片）才是未來 24-36 個月的硬限制；未來需求轉軸於 2026 H2 從訓練讓位給推論，TAM 由 $300B 擴至 $700B 但增速由 +60% YoY 降至 +25-30%；短中長期推估收斂於「base case 推論超越訓練成 demand 主軸 + ASIC 滲透 +15pp + 電力定 ASP 上限」。</p>

<!-- 4. 編輯記錄（critic patch banner）— 若有 patch 則放 §0 末尾、預設 collapsed -->
<details style="margin:18px 0 6px;font-size:12.5px;color:#6B7280">
  <summary style="cursor:pointer;color:#7C3AED;font-weight:600;list-style:none">📌 編輯記錄（v1.1 critic patch）— 點開展開</summary>
  <div style="margin-top:8px;padding:10px 14px;background:#FEF9C3;border-left:3px solid #F59E0B;border-radius:3px;color:#78350F;line-height:1.65">
    <strong>v1.1（YYYY-MM-DD）</strong>：🟡 / 🔴 / 🟢 — {patch summary} → 影響章節：§{X}。critic report：<a href="_critic_{Theme}_{YYYYMMDD}.md" style="color:#7C3AED">_critic_{Theme}_{YYYYMMDD}.md</a>
  </div>
</details>
</section>
```

## §1 歷史脈絡段落範例（純敘述）

```html
<section id="s1" class="ds-body">
<h2>§1 產業歷史脈絡</h2>

<p>AI 加速器這個產業從來不是線性演進。從 1999 年 NVDA 發布 GeForce 256 把「GPU」這個詞推進大眾語言開始，到 2026 年的今天，這個產業經歷了至少三次明確的代際轉折，而每一次轉折都重新洗牌「誰是 capex 受益者」這個問題的答案。</p>

<p>第一次轉折發生在 2010-2012 年。在這之前，GPU 是遊戲卡，是消費電子，是顯示器旁邊的東西。但 2010 年起，Hinton 在 Toronto 用 GTX 580 跑 AlexNet、2012 年 ImageNet 突破 → GPU 一夜之間從遊戲變成科研工具。NVDA 那時的 CEO Jensen Huang 並未錯過這個訊號，2012 年底 Tesla 系列推出、CUDA 開始成為非選不可的開發平台。這段歷史的關鍵不在「GPU 變強了」，而在「CUDA 軟體棧把 NVDA 從硬體公司變成平台公司」— 這個身分轉換，是後面 14 年 NVDA moat 的根。</p>

<p>...（更多歷史段落，2-3 個歷史轉折點 + 1-2 個歷史類比）...</p>

<div class="ds-implication">
GPU 的三次轉折暗示了第四次：從遊戲卡 → 訓練工具 → 推論基建。每次轉折都重洗 capex 受益者排序。本 DS §3-§6 將推估第四次轉折下，誰被擠出、誰擠進來。歷史告訴我們，每次轉折的核心都不是晶片本身，而是「軟體 + 規模 + 供應鏈整合」三者誰先建立。
</div>

<!-- v1.2: 節末 aside 列本節所有引用來源（deduped by URL） -->
<aside class="ds-refs">
  <span class="ds-refs-label">本節參考來源</span>
  <ol>
    <li><span class="tier">[T1]</span><a href="https://developer.nvidia.com/cuda-toolkit-archive">NVIDIA CUDA Toolkit Archive — v1.0 release 2006-11</a></li>
    <li><span class="tier">[T1]</span><a href="https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks">Krizhevsky et al., NIPS 2012 — AlexNet 15.3% top-5 error</a></li>
    <li><span class="tier">[T1]</span><a href="https://blogs.nvidia.com/blog/openai-deep-learning-dgx-1/">NVIDIA Blog — DGX-1 delivered to OpenAI 2016-08-15</a></li>
  </ol>
</aside>
</section>
```

## §5 → §6 因果橋範例（DS 特色）

§5 結尾必須有明確的「供需平衡結論」橋接到 §6：

```html
<div class="ds-bridge">
  <div class="label">§5 → §6 供需平衡結論</div>
  <p>合 §3（未來供給）與 §5（未來需求）兩章：晶片供給端 NVDA Blackwell + AMD MI400 + 自研 ASIC 三軌 2026-2027 capacity 可承載 demand +30-35% YoY；但<strong>電力供給</strong>受限於變壓器 lead time（3-5 年）與 grid interconnection queue（5-10 年），這是真正的 binding constraint。因此未來 24-36 個月產業狀態判定為 <strong>「晶片端平衡偏寬鬆 + 電力端結構性短缺」</strong>，這個非對稱結論是 §6 三情境推估的起點。</p>
</div>
```

## §6 短中長期推估表格範例

```html
<section id="s6" class="ds-body">
<h2>§6 短 / 中 / 長期推估</h2>

<p>{200-300 字敘述：本章如何推估、為何短中長期會出現分歧、三情境的核心變數是什麼}</p>

<table>
  <caption>三 horizon × 三情境推估</caption>
  <thead>
    <tr><th>Horizon</th><th>Base</th><th>Bull</th><th>Bear</th><th>Trigger metric</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>短期（12M）</strong></td>
      <td>Total accelerator capex YoY +28%；NVDA Q4 26 GM 70%；ASIC 占新 capex 22%</td>
      <td>+45%；GM 72%；ASIC 25%</td>
      <td>+15%；GM 65%；ASIC 18%</td>
      <td>hyperscaler 2026 capex guidance（Q2 26 earnings season）</td>
    </tr>
    <tr>
      <td><strong>中期（3Y）</strong></td>
      <td>...</td><td>...</td><td>...</td><td>...</td>
    </tr>
    <tr>
      <td><strong>長期（5Y+）</strong></td>
      <td>...</td><td>...</td><td>...</td><td>...</td>
    </tr>
  </tbody>
</table>

<p>{200-400 字敘述：每個 horizon 的邏輯依據}</p>

<div class="ds-implication">
{對投資的意義}
</div>
</section>
```

## §10 Catalyst Timeline（敘述 + 內聯 time）

```html
<section id="s10" class="ds-body">
<h2>§10 Catalyst Timeline</h2>

<p>未來 18 個月對 AI 加速器需求 thesis 最關鍵的五個節點：</p>

<p><strong class="ds-time">2026-08-27</strong> NVDA Q2 FY27 earnings。觀察 inference revenue run-rate（管理層 commentary）。<span class="ds-path-positive">若達成（≥ $80B annualized）</span> → 確認推論週期延長 → 進入 bull case，下一個窗口看 ASIC mix。<span class="ds-path-negative">若落空（≤ $50B 或 management 提及 inference 增速放緩）</span> → 觸發 §9 thesis #2 反方（推論泡沫提前破裂）→ 對 NVDA / TSMC 重新檢視。</p>

<p><strong class="ds-time">2026-Q4</strong> AMD MI400 出貨節奏。<span class="ds-path-positive">若 H2 26 量產順利 + 拿到 Meta/MSFT 大單</span> → AMD 訓練側 share 由 8% 衝 15-18%。<span class="ds-path-negative">若 yield 問題 / 客戶推遲</span> → NVDA 訓練端 lock-in 延長。</p>

<p>...（其餘 catalyst）...</p>
</section>
```

## §11 ticker table 範例

```html
<section id="s11" class="ds-body">
<h2>§11 關聯個股清單</h2>

<p>本 DS 對應的個股、角色與深度（stock-analyst 自動讀取本表）：</p>

<table class="ds-tickers">
  <thead>
    <tr><th>Ticker</th><th>角色</th><th>深度</th><th>受益方向</th><th>對應 DD</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>NVDA</strong></td>
      <td>訓練 + 推論加速器主導者</td>
      <td><span class="depth-red">🔴</span></td>
      <td>長期受益（短中期單元獲利分歧）</td>
      <td><a href="../dd/DD_NVDA_20260419.html">DD_NVDA_20260419</a></td>
    </tr>
    <tr>
      <td><strong>AVGO</strong></td>
      <td>ASIC 設計服務龍頭</td>
      <td><span class="depth-red">🔴</span></td>
      <td>結構性受益</td>
      <td><a href="../dd/DD_AVGO_20260420.html">DD_AVGO_20260420</a></td>
    </tr>
    <!-- ... -->
  </tbody>
</table>

<p style="font-size:12px;color:#6B7280">深度說明：🔴 核心（營收 > 40% 受該 theme 影響）｜ 🟡 次要（10-40%）｜ 🟢 邊緣（< 10%）</p>

<aside class="ds-refs">
  <span class="ds-refs-label">本節參考來源</span>
  <ol>
    <li><span class="tier">[T1]</span><a href="URL">Source title — {ticker} AI revenue breakdown</a></li>
  </ol>
</aside>
</section>
```
