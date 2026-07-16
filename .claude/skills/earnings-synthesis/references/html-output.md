# earnings-synthesis — html-output.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-16 v1.3 結構拆分，內容自 v1.2 原文搬移、語意零變更）。收錄 Step 5（HTML 輸出：head/CSS 模板 + 8 章節骨架 + TOC + 篇幅 sanity）、Step 6（index.html 整合）、以及 Bullet-First 條列化原則（write-time HTML 結構規則）。必讀時點見 SKILL.md 條件載入路由表。

## Step 5 — HTML output

輸出到 `docs/earnings/synthesis_YYYY-MM-DD.html`（檔名 = 跑 skill 當天的日期）。

### 5.A. `<head>` + `<style>` — 直接 reuse 日報模板

開 `docs/earnings/earnings_2026-05-21.html` 為模板，複製 lines 1-77（含 `<head>`、Google Fonts、embedded `<style>`），改：
- `<title>` → `美股財報統整 {window_start} → {window_end} · investMQuest`
- `<meta name="description">` → 一句敘述

額外**追加 CSS**（在現有 `<style>` 結尾前插入）：

```css
/* synthesis-specific */
.synthesis-tag{background:#ea580c;color:#fff;padding:.18rem .55rem;border-radius:4px;font-size:.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.source-local{color:#0369a1;font-size:.7rem;border:1px solid #bae6fd;padding:1px 6px;border-radius:3px;margin-left:4px}
.source-webfill{color:#9a3412;font-size:.7rem;border:1px solid #fed7aa;padding:1px 6px;border-radius:3px;margin-left:4px}
.trend-block{border-left:3px solid var(--accent);padding:14px 18px;background:var(--surface-2);border-radius:0 var(--radius) var(--radius) 0;margin-bottom:24px}
.trend-block h3{margin-top:0;font-size:1.05rem}
.imply-list{padding-left:0;list-style:none}
.imply-list li{padding:8px 0;border-bottom:1px solid var(--border)}
.imply-list li:last-child{border-bottom:none}
.confidence-note{font-size:.78rem;color:var(--text-muted);background:#fef3c7;border-left:3px solid #f59e0b;padding:10px 14px;border-radius:0 6px 6px 0;margin:18px 0}
```

### 5.B. `<header class="report-header">`

```html
<header class="report-header">
  <h1>美股財報統整：{window_start} → {window_end}</h1>
  <div class="report-meta">本地深度日報 {N} 份 · 缺失日 {M} 個（web 補 {K} 家公司）· {U} unique tickers · 生成於 {today}</div>
  <div class="report-lede">
    <strong>本期重點：</strong>{TL;DR 一段 4-6 句，列出 3-5 條最高 conviction 的產業 shift + 主要 ticker 標}
  </div>
</header>
```

### 5.C. 8 章節骨架（v1.1 從 9 章節縮成 8 章節：拿掉 §8 Methodology）

每章 H2 用 `<h2 id="secX">§X 章節名</h2>` 格式。`<div class="toc">` 列 9 章。

```
§0 TL;DR
  - 3-5 條最高 conviction 的產業 shift，一句一條 + 主要 ticker 標。
  - 用 <ol class="imply-list"> 呈現。
  - 例："AI capex 訊號分裂 — MSFT/GOOGL/AMZN 加碼 vs KLAC/TER 弱化 → 看好 power utility (NEE/CEG)、保留半導體設備曝險"

§1 Window 範圍與素材
  - 起迄日 / 本地深度日報 N 份 / 缺失日 M 個（web 補 K 家）/ unique ticker 數
  - **sector 分布小表**（5-6 行：sector → company count → reaction tilt）
  - **缺失日 fill-gap 表**：每個缺失日 → 補回 ticker 名單 → BEAT/MISS / surprise% / reaction% / source URL
  - 篇幅約 200-300 字 + 2 張表

§2 行業地圖
  - Sector × sub-industry 矩陣表（縱: 6-8 sector, 橫: 子產業, 格內: ticker count + ↑↓ reaction tilt）
  - 本地 vs web-filled 用 .source-local / .source-webfill 分色標
  - 篇幅約 300 字（解讀矩陣為主）+ 1 張大表

§3 跨產業大趨勢
  - 5-7 條 trend，每條 <div class="trend-block">：
    h3: trend name
    p: 主訊號（200 字）
    ul: confirm local + refute local + confirm webfill + cross-sector read-through
    p: web 外部 corroboration（120 字 + 2 source cite）
  - 篇幅約 300-500 字 / trend × 5-7 條 = 1800-3500 字。**本章是 prose 主體**

§4 各產業詳論
  - 6 個產業大段（Tech / Semi / Consumer / Financials / Industrial / Healthcare / Energy 視 window 而定）
  - 每產業 500-700 字：
    - 子產業 winners / losers（用 .source-local / .source-webfill 分色標）
    - 訊息 imply（這個產業 30 天內看到什麼 thesis、什麼證偽）
  - Financials / Industrials 中段斷檔多 → 特別仰賴 Step 0.5 補回的料 → 在這兩段標明信心度

§5 矛盾與弱訊號
  - Cross-industry contradictions：3-5 條
    - 例："hyperscaler capex 加碼 vs Teradyne 弱化 — 同主題下游分歧" 
    - 例："Beat-but-Sell 為何盛行 — 估值已 price in 還是 H2 guidance 被忽略"
    - 例："guidance vs reaction 背離 — 哪幾家 guide up 卻 -5%"
  - 篇幅約 600-900 字

§6 PM Implications（用戶最在意的章節）
  - 篇幅最大，~1000-1500 字
  - 三段：
    - **Sector tilt**：未來 30-90 天，超配 / 標配 / 低配哪幾個產業，理由
    - **Add/cut/hold ticker 名單**：每行 `TICKER | sector | action | rationale | confidence`
      - <ul class="imply-list">
      - Add: 5-10 檔具體 ticker（**只用本地深度日報的 conviction signal**）
      - Cut: 3-5 檔（同上）
      - Hold/Watch: 3-5 檔
    - **Web 補料公司**：另列 confirm-only 名單，**不單獨做主 add/cut**，只在 rationale 段引用為輔證
  - 用 .confidence-note 區塊明確說「web 補料公司不單獨入 add/cut 主名單」
  - **ID 機器欄交叉（v1.2 新增，動筆前必跑）**：§6 開寫前對每個涉及的產業跑 `python knowledge/q.py --theme {該節產業關鍵字}`，把 ID 機器欄（供需 / 時鐘 / priced-in）當交叉證據：
    - `priced_in=high` 的產業 → add 建議**必須逐條指明「哪個利多是市場尚未定價的」**；答不出來 → 該檔降為 hold。
    - `clock_phase=II`（熱產業）→ 依 QC-52 慣例對該產業 conviction 打折（熱產業時鐘系統性樂觀，見 calibration_id_20260707）。
    - 機器欄缺（legacy ID 無 machine columns）→ 照舊不阻斷，正常出建議。

§7 下 30 天 Watchlist
  - Catalysts ahead：
    - 即將 report 的重要公司（依當前已知 earnings 行事曆 — **必有 source URL，不可自由生成日期**；見 Step 4.5.B）
    - 即將公布的產業數據（CPI / PMI / FOMC / Powell speech）
    - 政策事件（tariff 期限、藥價、地緣政治）
  - 篇幅約 400-600 字 + 1 張 catalyst calendar 小表
  - **v1.1**：本章是 NVDA Q2 / AAPL Q3 等 mega-cap 下次 earnings 行事曆最容易出 hallucinate date 的地方，每個 date 必須在 Step 4.5.B fact-check 通過才能寫。如無法精確查證，用「Q2 FY27 預期 ~Aug」等含糊表述。

（v1.1 刪除原 §8 Methodology — source citations 改為各章 inline 引用 + §6 confidence-note。）
```

### 5.D. Toc 與導覽

```html
<div class="toc">
  <div class="toc-title">目錄</div>
  <ol>
    <li><a href="#sec0">§0 TL;DR</a></li>
    <li><a href="#sec1">§1 Window 範圍與素材</a></li>
    <li><a href="#sec2">§2 行業地圖</a></li>
    <li><a href="#sec3">§3 跨產業大趨勢</a></li>
    <li><a href="#sec4">§4 各產業詳論</a></li>
    <li><a href="#sec5">§5 矛盾與弱訊號</a></li>
    <li><a href="#sec6">§6 PM Implications</a></li>
    <li><a href="#sec7">§7 下 30 天 Watchlist</a></li>
  </ol>
</div>
```

### 5.E. 篇幅 + 比例 sanity

- 總篇幅 ≥ 60KB（typical 70-90KB）
- prose : table ≥ 7:3（敘事為主、表格為輔）
- §6 是篇幅最大章節（≥ 18% 內容）
- 每個 source citation 用 `<span class="source-local">`/`<span class="source-webfill">` tag 或括號引用

---

## Step 6 — Index 整合

在 `docs/earnings/index.html` 動 3 處：

### 6.A. CSS 新增 `.synthesis-tag` 與 `.synthesis-list`

在現有 `.reports .latest-tag{...}` 規則之後（約第 98 行）插入：

```css
/* Monthly synthesis section */
.synthesis-section{margin-top:0;margin-bottom:3rem}
.synthesis-list{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:.75rem}
.synthesis-list a{
  display:grid;grid-template-columns:1fr auto;gap:.85rem 1.5rem;
  padding:1.4rem 1.6rem;background:#fff;border:1px solid var(--border);
  border-left:4px solid #ea580c;border-radius:var(--radius);text-decoration:none;
  transition:box-shadow .15s,transform .15s
}
.synthesis-list a:hover{box-shadow:0 4px 14px rgba(0,0,0,.08);transform:translateY(-1px)}
.synthesis-list .date{font-family:'IBM Plex Mono',monospace;font-size:1.02rem;font-weight:600;color:var(--text-primary)}
.synthesis-list .takeaway{font-size:.87rem;color:var(--text-secondary);grid-column:1/-1;line-height:1.55}
.synthesis-tag{display:inline-block;padding:.14rem .5rem;border-radius:4px;
  font-size:.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  background:#ea580c;color:#fff}
```

### 6.B. 在 hero 之後（line ~209）插入新 section

在 `<div class="hero">...</div>` 結束之後、`<div class="section" id="earnings-reports">` 開始之前，插入：

```html
<div class="section synthesis-section" id="monthly-synthesis">
  <div class="container">
    <h2 class="section-title">📊 每月統整 · Industry Synthesis</h2>
    <ul class="synthesis-list">
      <li>
        <a href="synthesis_YYYY-MM-DD.html">
          <div class="date">Month DD, YYYY</div>
          <div class="meta">
            <span class="synthesis-tag">Synthesis</span>
            <span class="weekday">Day</span>
            <span class="companies">N reports · M companies</span>
          </div>
          <div class="takeaway">3 sentences capturing the 3-5 highest-conviction industry shifts · with primary tickers</div>
        </a>
      </li>
    </ul>
  </div>
</div>
```

新 synthesis 永遠**放最上面**；舊的往下 stack（複用同一 `<ul class="synthesis-list">`）。

### 6.C. 連結處理

`takeaway` 內容 = synthesis HTML §0 TL;DR 前 2-3 句的濃縮（≤ 35 中文字）。

---

## Bullet-First 條列化原則（v1.1 新增、強制）

**v1.0 翻車的另一條原因是「prose 太密、重點埋在長段落」**。v1.1 起，所有 §3/§4/§5/§6 內容**預設 bullet-first**，prose 退為輔助。

### 規則

1. **每個 §3 trend block** 的結構固定為：
   - `<p class="signal-row">` 1 句 anchor（≤ 30 字，講 trend 大方向）
   - `<h4>關鍵 data points</h4>` + `<ul class="bullets">`（4-6 條 bullets）
   - `<h4>Confirm 名單（本地）</h4>` + `<ul>` （按日期分行）
   - `<h4>Refute 名單（本地）</h4>` + `<ul>` （按日期分行）
   - `<h4>跨產業 read-through</h4>` + `<ul>` （2-3 條）
   - `<h4>外部 corroboration</h4>` + `<ul>` （3-4 條，每條 source + finding）
   - `<p class="caveat">` 1 段 caveat（≤ 80 字）

2. **每個 §4 industry block** 的結構固定為：
   - `<p class="lead-row">` 1 句 anchor
   - 2-4 個 `<h4>` 子段，每段 `<ul class="bullets">`（3-6 條）
   - `<p class="lead-row">` 1 句 implication（PM 行動結論）

3. **§5 contradiction** 的結構固定為：
   - `<h4>` 矛盾標題
   - `<ul>` 證據與暗示（3-5 條 bullets）
   - `<p class="pm-action">` 1 句 PM action

4. **§6 PM Implications** 已是 imply-list — **保持條列**。不要寫長段 prose。

### 禁止

- ❌ **任何段落 > 100 字**（除非是 disclaimer 或極特殊 caveat）
- ❌ **bullet 內套 bullet 超過 1 層**（保持平鋪）
- ❌ **用「然而」「另一方面」串接 4+ 個事實**（拆成 bullets）
- ❌ **數字混雜在敘述中**（用 `<strong>` 標出，或單獨成 bullet）

### CSS class 提示

- `signal-row` / `lead-row`：1 句 anchor，白底淺色 border
- `caveat`：黃底警告
- `pm-action`：白底 PM 行動結論
- `source-local` / `source-webfill`：inline tag
- `bullets`：bullet list（單層）
- `imply-list`：卡片式 list（用在 §6 add/cut/hold）
