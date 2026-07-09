---
name: earnings-synthesis
description: 把過去 30 天 docs/earnings/earnings_YYYY-MM-DD.html 的所有日報串成一份產業/子產業 trend + investment implication 的統整 HTML。輕掃 per-company 重點，心力放產業 read-through。**缺失交易日自動 web fill-gap 補回重要公司精簡結果**（不另存日報檔，融入趨勢章節）+ 中量 web augmentation（3-5 輪/主題）+ **8 章節**敘事為主表格為輔（v1.1 拿掉 §8 Methodology，source citations 改為 inline）。**v1.1 強制 Step 4.5 self-review gate + Step 5.5 post-write sanity check + Step 8.5 reflective review 反思**：寫稿前/後對 ticker completeness、未來日期 fact-check、本地/web 標籤、跨章節一致進行三重檢查。觸發：用戶說「跑最近財報的統整」/「earnings 統整」/「30 天財報統整」/「月度財報統整」/「財報季統整」/「過去 30 天財報重點」/「earnings synthesis」/「earnings monthly recap」/「earnings 30-day recap」/「monthly earnings rollup」。
version: v1.2
date: 2026-07-09
changelog:
  - v1.2 (2026-07-09)：§6 PM Implications 動筆前新增 ID 機器欄交叉（`python knowledge/q.py --theme`）— priced_in=high 的產業 add 建議須逐條指明未定價利多否則降 hold；clock_phase=II 熱產業依 QC-52 打折（calibration_id_20260707）；機器欄缺（legacy）不阻斷。
  - v1.1 (2026-05-22)：拿掉 §8 Methodology 章節；新增 Step 4.5 self-review、Step 5.5 post-write sanity、Step 8.5 reflective review；明確要求 ticker completeness sweep（top-20 mkt cap 個別 confirm 是否覆蓋）；明確要求未來日期必有 source URL（防 hallucinate dates）；明確要求本地 day-內盲點處理（earnings_YYYY-MM-DD.html 存在但漏該日重要 ticker 時，當作 in-day webfill 補回）。
  - v1.0 (2026-05-22)：initial release.
---

# Workflow: earnings-synthesis / 30 天財報統整

當用戶以上方任一觸發句要求「最近財報的統整」時，照下方 9 個 step 從頭做到尾，**不要先問**。素材已存在 `docs/earnings/`，補資料走 web。

## 0. 定位與不做什麼

**做的事**：把日報 vertical 視角串成 sector-level horizontal 敘事 + investment implication。重點在「**產業 / 子產業 trend** + **PM imply（具體 add/cut/hold）**」，不是 rehash 每家公司。

**不做的事**：
- 不重做 per-company 深度分析（那是現有 `earnings_YYYY-MM-DD.html` 日報的工作）
- 不替缺失日另存一份日報 HTML 檔（補回的料只當 in-memory 原料）
- 不寫 validator / meta JSON / pre-commit hook 鎖規則（mirror push-earnings 政策）
- 不跑強制 critic gate（v1 手動 review；用戶可在發布後說「review 一下這份 synthesis」）

---

## Step 0 — Window 決定 + Universe 盤點

1. **預設 window**：`today − 30d` → `today`。用戶可指定「過去 N 天」/「上個月」/「Q1 earnings 季」等覆蓋。
2. **列出 expected trading days**：window 內所有 US 交易日（排除週六/日 + 下表硬編 US holidays）：

   | 2026 US holidays（NYSE/NASDAQ closed） |
   |---|
   | New Year 1/1, MLK Day 1/19, Presidents Day 2/16, Good Friday 4/3, Memorial Day 5/25, Juneteenth 6/19, Independence Day 7/3, Labor Day 9/7, Thanksgiving 11/26, Christmas 12/25 |

3. **掃本地深度日報**：`docs/earnings/earnings_YYYY-MM-DD.html`，date in [window_start, window_end]，記下 covered_dates。
4. **算缺失日**：`missing = expected_trading_days − covered_dates`。
5. 輸出：`{window: [start, end], expected: N, local: M, missing: [...dates]}`

---

## Step 0.5 — 缺失日 web fill-gap + 本地 day-內盲點掃描

對 Step 0 算出的每個 `missing_date`，跑 light 補資料流程；**同時對本地已覆蓋日做 day-內盲點掃描**（local-but-incomplete check）：

1. **掃當日 reporting universe**：
   - `WebSearch "earnings reports {Month} {Day} {Year} large cap"`
   - 補一次 `WebSearch "S&P 500 companies reporting {YYYY-MM-DD} pre-market post-market"`
   - 解析回傳，列出當天有 report 的 ticker。
2. **篩重要公司**：mkt cap ≥ **$50B**（沿用本地日報 threshold），取前 **5-10 家**最重要（mkt cap × abs(surprise%) × abs(reaction%) 綜合排序；無法判斷 surprise 時 fallback 純 mkt cap）。
2.5. **本地 day-內盲點掃描（v1.1 新增）**：對每份本地日報 `earnings_YYYY-MM-DD.html`，掃 WebSearch 確認當日**所有 ≥$200B 公司**是否都被本地覆蓋。若有遺漏（例如本地 5/20 報告 9 家但漏 NVDA AMC），則對該漏掉的 ticker 用相同 Step 0.5 流程做 light webfetch，並在 §1 fill-gap 表標為「day-內盲點」。**這條最重要 — top-20 mkt cap 級別的個股 earnings 不能因為本地編輯失誤而消失於 synthesis**。常需檢查的 top-20 名單：NVDA, MSFT, AAPL, AMZN, GOOGL, META, TSLA, BRK.B, JPM, V, MA, LLY, ORCL, UNH, XOM, JNJ, WMT, PG, HD, BAC。
3. **Light WebFetch per ticker**（每家 1-2 輪，不要超過）：
   - 目標 source：Seeking Alpha headline、Zacks earnings call、Reuters/Bloomberg/CNBC earnings recap、公司 IR press release。
   - 抽取：`{eps_actual, eps_estimate, eps_surprise_pct, revenue_actual, revenue_estimate, guidance_tilt: "raise/maintain/cut/no-guide", reaction_pct, one_line_thesis}`
4. **整理 in-memory** `web_filled_companies[]`，schema：
   ```
   {
     date: "YYYY-MM-DD",
     ticker: "XYZ",
     mkt_cap: "$80B",
     sector: "Financials",
     sub_industry: "Regional Banks",
     beat_miss: "BEAT" | "MISS" | "MIXED",
     eps_surprise_pct: +5.2,
     revenue_surprise_pct: +1.3,
     guidance_tilt: "raise",
     reaction_pct: +3.4,
     thesis_one_liner: "Loan loss reserve normalized; net interest margin reached cycle peak.",
     sources: ["url1", "url2"]
   }
   ```
5. **不寫檔**。這份結構直接餵 Step 3/4/6 使用。

**重要原則**：
- web 補料的權重低於本地深度日報。**只當趨勢輔證、不當主錨點**。
- §6 PM Implications 的 add/cut/hold 建議**優先用本地深度日報的 conviction signal**；web 補料的公司只作為 confirm，不單獨做主 add/cut 建議。
- §1 / §8 必須**透明列出**哪些 ticker 來自 web 補料 + source URLs。

---

## Step 1 — 本地素材 ingest

對每份 `docs/earnings/earnings_YYYY-MM-DD.html`，parse：

1. **report-meta**：`<div class="report-meta">N companies analyzed · TICKER1 $XXb · TICKER2 $YYB · ... · YYYY-MM-DD</div>`
   → 抽 tickers + mkt cap
2. **report-lede**：`<div class="report-lede">` 內 `<strong>核心發現：</strong>` 之後的 prose → 取為當日 headline 主題詞料
3. **company-cards**：`grep -c '<div class="company-card">'` → company count
4. **§2/§3/§4/§5 章節**：找 `<h2 id="sec2">` 到 `<h2 id="sec3">` 之間（與 sec3→sec4、sec4→sec5、sec5→footer）整段 plain text。這四章已經做了 cross-cutting 工作，是 synthesis 主要原料：
   - §2 跨公司比較與趨勢 → 主要 trend signal
   - §3 贏家輸家 → reaction 資料
   - §4 矛盾與風險訊號 → §5 synthesis 反例料
   - §5 總結 → highlight 萃取

整理成 `local_reports[]`，每份一個 dict：`{date, tickers, lede, sections: {sec2, sec3, sec4, sec5}}`

---

## Step 2 — Ticker → 子產業 mapping

三路 fallback 建表：

1. **`docs/id/ID_*.html`**：每份 ID 報告的 `<script id="id-meta">` JSON 有 `related_tickers[]`。一個 ticker 出現在 ID_HBM_*.html 的 related_tickers，就 mapping `(ticker → "Semiconductors" → "HBM supply chain")`。
2. **`docs/dd/*.html`**：找 `<script id="dd-meta">` JSON 的 `industry` 欄（覆蓋率低，但能補一些）。
3. **Inline 硬表**（fallback；只覆蓋 30 天 window 出現的 ~100 ticker；不夠時用 WebSearch 1 輪查 sector）：
   ```
   Mag7 / Hyperscaler: MSFT GOOGL AMZN META APPL NVDA TSLA
   Semi 上游 (Fab/Tools): TSM AMAT LRCX KLAC ASML
   Semi 下游 (Design): NVDA AMD AVGO QCOM ADI MRVL
   Consumer Discretionary: AMZN HD LOW TJX ROST WMT TGT COST
   Financials: JPM BAC GS MS WFC BLK SCHW V MA AXP
   Industrial / Aerospace: BA LMT RTX GD CAT DE UPS FDX
   Energy: XOM CVX COP EOG SLB
   Healthcare / Pharma: LLY UNH JNJ PFE MRK ABBV REGN GSK AZN
   Software / SaaS: CRM ORCL NOW ADBE INTU WDAY
   ```
   覆蓋本地 + Step 0.5 web-filled tickers。

輸出 `ticker_map = {ticker: (sector, sub_industry)}`。

---

## Step 3 — 趨勢 surface

從三路素材萃出 **5-7 條跨產業 trend**：

1. **詞頻 / 主題重複度**：跨 30 份 lede + §2/§3 整段，找重複出現 ≥ 3 次的主題（如 "AI capex"、"tariff"、"MFN drug pricing"、"住房底部"、"K-shaped 消費"、"Beat-but-Sell"、"datacenter power"）。
2. **跨產業共振**：一個主題只出現在 1 個產業 → 是 vertical 故事、不是 cross-cutting trend，**淘汰**；至少橫跨 2+ sector 才入選。
3. **每條 trend 結構**：
   ```
   trend_name: "AI capex 訊號分裂"
   main_signal: "Hyperscaler trio capex 全面再加速 vs 半導體設備商指引疲弱"
   confirm_local: ["MSFT 4/29 報告", "GOOGL 4/29 報告", "AMZN 4/30 報告"]
   refute_local: ["KLAC 5/06", "Teradyne 4/28"]
   confirm_webfill: ["AMAT 5/15 補回 BEAT"] (if any)
   cross_sector_readthrough: "AI capex 加碼 → power utility 受惠 (NextEra defense AI thesis)"
   ```
4. 一定要**明確標**「來自本地深度日報」vs「來自缺失日 web 補資料」。

---

## Step 4 — Web augmentation（趨勢深掘）

對每條 Step 3 萃出的 trend，再跑 **3-5 輪 WebSearch / WebFetch**：

1. **外部 corroboration**：搜「{trend keyword} 2026 Q1 earnings sell-side consensus」「{trend} sector report May 2026」找券商 / 主流財經媒體有沒有同主題覆蓋
2. **跨產業 read-through**：搜「{primary sector} {downstream sector} read-through 2026」找上下游受影響的子產業
3. **數字 sanity check**：搜「{trend} TAM market size 2026」「{trend} adoption rate」確認數字 / 規模

**Source 限制**：
- T1（最高優先）：公司 IR / press release、SEC filings
- T2（次優）：Bloomberg / Reuters / WSJ / FT / CNBC / Barron's / Forbes
- T3（補強）：Seeking Alpha analyst notes、Zacks、券商 PDF outlook
- **拒收**：Twitter / Reddit / 個人 blog / SeekingAlpha 純 retail opinion

每條 trend ≥ 2 source citations。引用格式 `(Source: Bloomberg 2026-05-18, "AI capex outlook by hyperscaler")`

**與 Step 0.5 區分**：0.5 是「補資料點」（per ticker, light fetch），4 是「趨勢深掘」（per theme, multi-round）。兩者不要混。

---

## Step 4.5 — Self-Review Gate（反思 / write-time critic）

**v1.1 新增、強制執行**。Step 4 完成 web augmentation 之後、Step 5 開寫 HTML 之前，必須對手上的 in-memory 數據做 5 軸 sanity check。**這個 step 沒過就不准開寫**。

### 4.5.A. Ticker Completeness Sweep（重點）

對本期 window 內 US top-20 mkt cap 公司逐一 confirm 是否覆蓋：

```
top_20_mkt_cap = [NVDA, MSFT, AAPL, AMZN, GOOGL, META, TSLA, BRK.B, 
                  JPM, V, MA, LLY, ORCL, UNH, XOM, JNJ, WMT, PG, HD, BAC]
```

對每一檔：
1. 確認該公司 earnings date 是否落在 window 內
2. 如是，確認是否在 `local_reports[]` 任一份的 tickers 名單中
3. 如不在，且不在 `web_filled_companies[]`，則**必須補回**（走 Step 0.5.2.5 day-內盲點流程，light webfetch）

**這條最容易漏的是 day-內盲點**：本地某日報告涵蓋了 N 家，但**該日另有 mega-cap 報 earnings 沒被收進去**（典型例：NVDA AMC 在當日本地報告主場已存其他 retail 公司時被遺漏）。Top-20 級別的 ticker 必須補回。

### 4.5.B. 未來日期 Fact-Check（防 hallucinate）

掃過 `web_filled_companies[]` 與你在 Step 4 抓到的 catalyst / event dates，並準備寫進 §7 Watchlist 的「earnings ahead」名單前：

- **任何「earnings ahead」日期都必須有對應的 source URL**（earnings whisper / company IR / WallStreetHorizon / TipRanks earning calendar 等）。
- 不可由模型自由生成 date（例如「~5/30 NVDA Q2」這種就是 hallucinate — NVDA Q2 FY27 真實日期是 8/26，模型不應自由填空）。
- **NVDA 行事曆**：Feb / May / Aug / Nov（fiscal quarter ends April/Jul/Oct/Jan）。若不確定，WebSearch `"NVDA next earnings date"` 確認。
- 其他常被誤判的：AAPL（Jan/Apr/Jul/Oct）、AMZN（Jan/Apr/Jul/Oct/月底）、MSFT（Jan/Apr/Jul/Oct/月底）。
- 如連 WebSearch 都查不到精確日期，就**用含糊但安全的表述**（如「Q2 FY27 預期 ~8 月底」）而非具體編日期。

### 4.5.C. Source Provenance Check

對每條 §3 trend 主訊號裡會出現的數字（%, $, +XX% YoY），確認該數字能在：
1. 本地 `local_reports[].sections.sec2-sec5` 找到原始引用，或
2. `web_filled_companies[]` 的 `thesis_one_liner` / 對應 source URL 找到，或
3. Step 4 web augmentation 抓回的 source quote 裡找到

如有任何數字「印象記憶」但找不到 source，**移除或改成定性敘述**（如「+8x 訂單」→「訂單顯著加速」），不可保留精確數字。

### 4.5.D. 本地 vs Web 標籤完整性

確認 in-memory 結構裡每個 ticker 都有正確 provenance flag：
- 本地深度料 → `<span class="source-local">` 將在 HTML 出現
- Web 補料（缺失日 + day-內盲點）→ `<span class="source-webfill">` 將在 HTML 出現

§6 ADD/CUT 名單原則上**只用本地深度料**。Web 補料公司原則上在 §6 confidence-note 提及為 confirm-only — 但**唯一例外是 top-5 mkt cap 的 day-內盲點 webfill**（例：NVDA / MSFT / AAPL 等級），可破例入主 ADD/CUT 但必須在 confidence 欄標「業務 High / 短期 entry Medium」並附 caveat 段。

### 4.5.E. 跨章節一致性 Plan

寫 HTML 之前，先草擬：
- §0 TL;DR 5 條 → 每條必須在 §3 對應 trend block 展開
- §6 ADD/CUT/HOLD 每個 ticker → 必須在 §4 對應產業段有業務敘述背景
- §7 Watchlist catalysts → 必須與 §3 trends 有 logical link（不可空降不相關的 event）

如發現任一條 violate，回 Step 3-4 補資料，不要硬寫。

---

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

## Step 5.5 — Post-Write Sanity Check（v1.1 新增）

HTML 寫完、commit 前，跑下列 grep 自我驗證。任一條 fail 就回頭修。

### 5.5.A. 結構基本盤

```bash
python3 -c "
import re
with open('docs/earnings/synthesis_{YYYY-MM-DD}.html') as f: s = f.read()
print('size:', len(s), 'chars')
print('sections H2:', len(re.findall(r'<h2 id=\"sec', s)))   # 應為 8
print('trend blocks:', len(re.findall(r'class=\"trend-block\"', s)))   # 應 5-7
print('source-local refs:', len(re.findall(r'class=\"source-local\"', s)))   # 應 ≥ 50
print('source-webfill refs:', len(re.findall(r'class=\"source-webfill\"', s)))   # 應 ≥ web-fill ticker 數 × 2
print('add/cut/hold tags:', len(re.findall(r'class=\"tag-(add|cut|hold)\"', s)))
print('external URLs:', len(re.findall(r'href=\"https?://', s)))   # 應 ≥ 12 (2 per trend × 6 trends)
"
```

Gate：size ≥ 60KB；H2 = 8；trends 5-7；external URLs ≥ 12。

### 5.5.B. 未來日期反查

對 §7 watchlist 表格的每個 `<td>` 含日期，grep 確認該日期出自 Step 4.5.B 通過過的 source URL。**任何 `YYYY-MM-DD` 或 `M/DD` 格式的具體日期，如不能對應到一個 source URL，必須改為含糊表述**。

特別檢查：
- `~5/30` / `5月底` 這類「month-end」guess → 必須 source confirm
- 「NVDA Q2 / AAPL Q3」這類 fiscal quarter → 必須對應到真實財報日（NVDA fiscal Q2 = 8/26、Q3 = 11月底 等）

### 5.5.C. Top-20 mkt cap 覆蓋反查

```bash
for t in NVDA MSFT AAPL AMZN GOOGL META TSLA JPM V MA LLY ORCL UNH XOM JNJ WMT PG HD BAC; do
  if grep -q "$t" docs/earnings/synthesis_{YYYY-MM-DD}.html; then
    echo "$t ✓"
  else
    echo "$t ✗ MISSING"
  fi
done
```

如該公司有在 window 內 report earnings 但 grep 不到 → 回 Step 4.5.A 補回。
如該公司沒在 window 內 report（如 LLY 4 月已報過、AAPL 4/30 已在 4/30 local） → 確認本身 ticker 至少在 §2 行業地圖或 §6 holdwatch 中出現一次。

### 5.5.D. 本地 / Web 分色標籤一致

確認每個 web-filled ticker 的所有出現都帶 `<span class="source-webfill">`。

```bash
# webfill ticker 應該出現在以下 3 個地方都有 webfill tag：
# §1 fill-gap table, §2 industry map, §3 trend block (confirm webfill list), §6 confidence-note
```

### 5.5.E. 跨章節一致 final check

讀 §0 TL;DR 5 條，對每條找 §3 對應 trend block 確認 narrative 一致。讀 §6 ADD 名單，對每個 ticker 找 §4 對應產業段確認業務敘述背景。讀 §7 watchlist，對每個 catalyst 找 §3 對應 trend 確認 logical link。

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

## Step 7 — Commit & push

```bash
git add docs/earnings/synthesis_YYYY-MM-DD.html docs/earnings/index.html
git commit -m "Add earnings synthesis: window YYYY-MM-DD → YYYY-MM-DD

本地深度日報 N 份 + 缺失日 M 個 (web 補 K 家) → 萃 T 條跨產業 trend，
PM imply 含 X 檔 add / Y 檔 cut / Z 檔 hold-watch。

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
git push origin main
```

如果 push 被 reject → `git pull --rebase origin main && git push`（mirror 其他 skill push 慣例）。

---

## Step 8 — Report back

跑完 skill，給用戶簡短回報：

```
✅ Earnings synthesis 發布完成

Window: YYYY-MM-DD → YYYY-MM-DD ({N} days)
本地深度日報: {M} 份
缺失日: {K} 個 → 補回 {L} 家公司（mkt cap ≥ $50B）
Unique tickers: {U}
萃出 trend: {T} 條
Web sources: {S}
Add/cut/hold: {X}/{Y}/{Z} 檔

Live: https://research.investmquest.com/earnings/synthesis_YYYY-MM-DD.html
Index: https://research.investmquest.com/earnings/
```

---

## Step 8.5 — Reflective Review（反思 / post-publish critic, v1.1 新增）

commit & push 之後、Step 8 回報用戶之前，跑 **inline 自我反思**。讀自己剛寫的 HTML 全文，對下列五題用 contrarian 角度回答：

### 8.5.A. 「如果這次 synthesis 有大錯，最可能錯在哪？」

從用戶角度想：「我點開這份 HTML，第一個會挑剔的是什麼？」常見錯誤類型：
- **遺漏關鍵 ticker**：top-20 mkt cap 公司在 window 內報了 earnings 但沒被覆蓋（NVDA day-內盲點是 v1.0 翻車的真實案例）
- **虛構未來日期**：§7 catalyst calendar 寫了「~5/30 NVDA Q2」這類 hallucinate
- **Trend 主訊號數字找不到 source**：印象記憶寫的 +XX% 但 grep 不到原始引用
- **§6 add 名單沒有業務背景**：§4 對應產業段找不到敘述支撐
- **§0 TL;DR 與 §3 trends 編號不一致**

### 8.5.B. 「我的 ADD 名單反向想：如果其中 3 檔是錯的，可能的理由是什麼？」

對 §6 ADD 名單每檔，問自己：
- 業務動能是否真的可持續 4-8 季？還是只是 cyclical bounce？
- 估值（NTM P/E vs 5Y avg）已經 priced in 多少 thesis？
- 同產業同主題的其他名稱有沒有可能反而是更乾淨的 add？

如有任一檔通不過這個反向 test，移到 HOLD/WATCH。

### 8.5.C. 「Web 補料公司的 confidence flag 是否誠實？」

對每個 web-filled ticker，確認：
- §1 fill-gap 表 source URL 真的能驗證關鍵數字（不是泛泛 calendar 頁）
- §3 trend confirm list 有明確區分本地 vs webfill
- §6 confidence-note 真的有點明「web 補料不入主 add/cut」

### 8.5.D. 「§7 Watchlist 的每個 catalyst 都有真實 source 嗎？」

特別檢查日期 — 用 contrarian 心態假設「這個日期是我亂編的」，去找 source 反證。如找不到精確 source，立即改為含糊表述。

### 8.5.E. 「最重要：我有沒有過度自信？」

讀 §0 TL;DR — 5 條 conviction shift 是否有任何一條是「我覺得這樣比較簡潔好讀」而非「實際 trend 浮現」？如有，改寫成更謙遜的措辭（如「初步觀察」「需 H2 驗證」）。

**如 8.5.A-E 任一條發現問題**：
- 小錯（cosmetic / 措辭）→ 直接 patch HTML，commit 一次 `fix(synthesis): self-review 反思 patch`
- 大錯（漏 ticker / 虛構日期 / trend 無證據）→ 必須通知用戶承認失誤 + 給修補 plan，**不可悄悄改**

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

---

## Anti-laziness 規則（mini）

寫 HTML 時：
- §3 trend block **不可空話** — 每條 trend 必須有「主訊號 1 句 + ≥ 2 confirm ticker + ≥ 1 refute ticker（如有）+ web corroboration ≥ 2 source」
- §4 每產業段 **不可只列名單** — 必須有「子產業 imply 結論」段（80-150 字）
- §6 add/cut/hold **不可只寫 ticker** — 每行必須有 rationale ≥ 1 句 + confidence tag
- 數字必引 source — `(EPS $X.XX vs est $Y.YY)` 或 `(reaction +Z.Z% 收於 $W)`
- web-filled 公司在 §3/§4/§6 出現時 **必須加 `<span class="source-webfill">web-filled</span>` 標**

## Edge cases

- **缺失日 0 個**（本地完整覆蓋）→ Step 0.5 skip；§1 缺失日表標 "全期完整覆蓋"
- **某缺失日無重要公司 report**（如 OPEX 後 Friday，全 sector 低活躍）→ §1 fill-gap 表標「{date}: 無 ≥$50B earnings」，Step 0.5 此日 skip
- **本地日報 < 5 份**（window 太短或新建系統）→ 不要硬跑；回用戶「本地深度料不足，建議 window 拉長或先補日報」並停在 Step 0
- **window 跨季**（如 4/1 ~ 5/30 含 Q1/Q2 兩季）→ §3 trend block 須額外標「Q1 main」vs「Q2 early read」
- **同 ticker 在 window 內被分析多次**（如 NVDA 出現在 4/22 + 5/21）→ 取**最近一次**為主、舊次當 contradiction signal 對比

## 不要做的事

- ❌ 不要 rehash per-company details — 那是日報的工作
- ❌ 不要把 web 補料公司放進 §6 主 add/cut 名單
- ❌ 不要 invent 沒在 source 出現的 trend — 寧可萃 5 條真的比 7 條湊的好
- ❌ 不要動 `docs/research/`、`docs/dd/`、`update_dd_index.py`
- ❌ 不要寫 INDEX.md（earnings 目錄沒這檔）
- ❌ 不要動其他日報 HTML 內容

## 未來 Phase 2 候選

- **id-review --mode synthesis**：新增 critic 模式，檢查 §6 imply 與 §3 trend 一致性、source citation 充分度
- **自動 cron**：每月 1 號自動跑上個月 synthesis（GitHub Actions）
- **Cross-window 比較**：本期 vs 上期 trend shift（哪些主題上升、哪些消失）
- **DD universe 對齊**：synthesis 萃出的 add 名單 vs `docs/research/index.html` 現有 DD universe overlap 檢查
