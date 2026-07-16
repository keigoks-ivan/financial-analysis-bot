---
name: earnings-synthesis
description: 把過去 30 天 docs/earnings/earnings_YYYY-MM-DD.html 的所有日報串成一份產業/子產業 trend + investment implication 的統整 HTML。輕掃 per-company 重點，心力放產業 read-through。**缺失交易日自動 web fill-gap 補回重要公司精簡結果**（不另存日報檔，融入趨勢章節）+ 中量 web augmentation（3-5 輪/主題）+ **8 章節**敘事為主表格為輔（v1.1 拿掉 §8 Methodology，source citations 改為 inline）。**v1.1 強制 Step 4.5 self-review gate + Step 5.5 post-write sanity check + Step 8.5 reflective review 反思**：寫稿前/後對 ticker completeness、未來日期 fact-check、本地/web 標籤、跨章節一致進行三重檢查。觸發：用戶說「跑最近財報的統整」/「earnings 統整」/「30 天財報統整」/「月度財報統整」/「財報季統整」/「過去 30 天財報重點」/「earnings synthesis」/「earnings monthly recap」/「earnings 30-day recap」/「monthly earnings rollup」。
version: v1.3
date: 2026-07-16
---

# Workflow: earnings-synthesis / 30 天財報統整

當用戶以上方任一觸發句要求「最近財報的統整」時，照下方 9 個 step 從頭做到尾，**不要先問**。素材已存在 `docs/earnings/`，補資料走 web。

## 條件載入路由表（v1.3 結構拆分：核心 = always-on，references/ = 按需載入）

> v1.3 把 HTML 輸出模板、index 整合、Bullet-First 結構規則、三道 review gate 的逐條 checklist、版本沿革搬到 `references/`（內容自 v1.2 原文零語意變更搬移）。核心保留定位 / 觸發 / Step 0-4 + Step 7-8 工作流骨架 / anti-laziness 與 edge-case 紀律。載入時點如下：

| 時點 | 條件 | 必 Read |
|---|---|---|
| Step 4.5（web augmentation 完成、開寫 HTML 之前） | 一律 | `references/review-gates.md`（Step 4.5 self-review gate 5 軸 checklist） |
| Step 5（開寫 HTML 之前） | 一律 | `references/html-output.md`（head/CSS 模板 + 8 章節骨架 + TOC + 篇幅 sanity + Bullet-First 原則） |
| Step 5.5（HTML 寫完、commit 之前） | 一律 | `references/review-gates.md`（同檔，Step 5.5 post-write grep sanity） |
| Step 6（index.html 整合） | 一律 | `references/html-output.md`（同檔，Step 6 三處編輯） |
| Step 8.5（push 後、回報用戶之前） | 一律 | `references/review-gates.md`（同檔，Step 8.5 反思五題） |
| 修改本 skill 規則 / 查版本沿革時 | — | `references/changelog.md`（v1.0→v1.3 版本歷史） |

---

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

**v1.1 新增、強制執行**。Step 4 完成 web augmentation 之後、Step 5 開寫 HTML 之前，必須對手上的 in-memory 數據做 5 軸 sanity check（Ticker Completeness Sweep / 未來日期 Fact-Check / Source Provenance / 本地 vs Web 標籤 / 跨章節一致性 Plan）。**這個 step 沒過就不准開寫**。

→ 5 軸 checklist 全文（4.5.A–4.5.E）：**開跑本 step 前必 Read `references/review-gates.md`**（Step 4.5 段）。

---

## Step 5 — HTML output

輸出到 `docs/earnings/synthesis_YYYY-MM-DD.html`（檔名 = 跑 skill 當天的日期）。head/CSS 直接 reuse 日報模板 + 追加 synthesis CSS、8 章節骨架（§0 TL;DR / §1 Window / §2 行業地圖 / §3 跨產業大趨勢 / §4 各產業詳論 / §5 矛盾與弱訊號 / §6 PM Implications / §7 下 30 天 Watchlist）、TOC、篇幅 sanity（≥60KB、prose:table ≥7:3），以及 Bullet-First 條列化結構規則（§3/§4/§5/§6 預設 bullet-first、段落 >100 字禁令等）。

→ 完整模板與骨架（5.A–5.E + Bullet-First 原則）：**開寫 HTML 前必 Read `references/html-output.md`**。

---

## Step 5.5 — Post-Write Sanity Check（v1.1 新增）

HTML 寫完、commit 前，跑一組 grep 自我驗證（結構基本盤 / 未來日期反查 / Top-20 mkt cap 覆蓋反查 / 本地-Web 分色標籤一致 / 跨章節一致 final check）。任一條 fail 就回頭修。

→ 各條 grep 腳本與 gate 門檻（5.5.A–5.5.E）：**commit 前必 Read `references/review-gates.md`**（Step 5.5 段）。

---

## Step 6 — Index 整合

在 `docs/earnings/index.html` 動 3 處：6.A CSS 新增 `.synthesis-tag` / `.synthesis-list`、6.B hero 之後插入 `#monthly-synthesis` section（新 synthesis 永遠放最上面）、6.C takeaway 連結處理（= §0 TL;DR 前 2-3 句濃縮 ≤35 中文字）。

→ 三處編輯的完整 CSS / HTML 片段：**Read `references/html-output.md`**（Step 6 段）。

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

commit & push 之後、Step 8 回報用戶之前，跑 **inline 自我反思**。讀自己剛寫的 HTML 全文，對五題用 contrarian 角度回答（最可能的大錯在哪 / ADD 名單反向想 / web 補料 confidence flag 是否誠實 / §7 catalyst 日期是否都有真實 source / 是否過度自信）。小錯直接 patch，大錯必須通知用戶承認失誤 + 給修補 plan，**不可悄悄改**。

→ 反思五題全文（8.5.A–8.5.E）與大/小錯處置協議：**回報用戶前必 Read `references/review-gates.md`**（Step 8.5 段）。

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
