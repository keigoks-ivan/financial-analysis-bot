---
name: crowding-monitor
description: 產出新一期「跨資產擁擠交易監測」HTML（docs/crowding/CROWDING_YYYYMMDD.html）並在期刊列表插卡。消費端 skill——假設 docs/crowding/data/latest.json 由週更 pipeline（build_crowding.py）維護（COT 15 市場＋64+ 主題擁擠分數＋15 檔跨資產 ETF＋gaps）。skill 職責＝把最新資料層＋情緒/資金流 web 掃描（BofA FMS／Flow Show／GS Prime positioning／AAII／VIX-SKEW，每主題 3-5 輪 WebSearch，每個數字帶來源日期與信心）收斂成三層代理三角測量：Exhibit 編號制的 named trades（含 unwind 觸發器與狀態）、COT positioning 儀表、主題擁擠熱力圖、機構 vs 散戶分岔、對本站組合的 read-through（GRP／三軌語言，禁 IRR 排序、禁買賣指令）、反向掃描、方法論血統與 gaps 誠實列出。定位＝描述器非擇時訊號，與首頁風險儀表同家族。觸發：用戶說「跑擁擠交易監測」「crowding monitor」「擁擠交易月報」「新一期 crowding」「positioning monitor」。
version: v1.0
date: 2026-07-05
changelog:
  - v1.0 (2026-07-05)：initial release。報告規格固化自創刊號 docs/crowding/CROWDING_20260705.html（三層代理三角、Exhibit 編號制、8 筆 named trades、§7 GRP／三軌 read-through）。
---

# Workflow: crowding-monitor（跨資產擁擠交易監測 · 月度敘事）v1.0

> **定位**：消費端 / 綜合層 skill。資料層（COT 15 市場、64+ 主題擁擠分數、15 檔跨資產 ETF、資料 gaps）由**週更 pipeline** `scripts/build_crowding.py` 產出至 `docs/crowding/data/latest.json`——**本 skill 不重算擁擠引擎、不抓 COT、不動 pipeline**。skill 的價值＝把 latest.json 的資料層，疊上**情緒/資金流的 web 掃描**與**對本站組合的 read-through**，收斂成一期可讀的敘事。
>
> **與首頁風險儀表同家族**：本監測是**描述器（describer），不是擇時訊號（timing signal）**。擁擠度衡量部位集中與下方緩衝，放大回撤幅度與相關性，**不預測轉折時點**。這是本站對風險儀表的既定裁決語言。

---

## 環境常數（已鎖定）

- **輸入資料層**：`docs/crowding/data/latest.json`（週更 pipeline 維護；schema 含 COT 15 市場 net %OI 與 5y/3y 百分位＋Δ4w/Δ13w、64+ 主題 A/B/C/E 維度分數與覆蓋、15 檔 ETF 自身百分位、gaps 清單、各層 as-of）。**pipeline 是另一個 owner——本 skill 唯讀 latest.json，絕不改 build_crowding.py／data/／workflow。**
- **輸出報告**：`docs/crowding/CROWDING_{YYYYMMDD}.html`（noindex；視覺規格見下方「報告規格」，對齊創刊號 `CROWDING_20260705.html`）。
- **期刊索引**：`docs/crowding/index.html`——在 `<ul class="reports">` **最上方** insert 新一期 `<li>` 卡片（三行 lede：本期主軸 · 跨資產極端 · 情緒結構）；把前一期的 `<span class="vol-tag">最新</span>` 拿掉。**不要動** `<!-- CROWDING_AUTO_DASH_START -->`／`<!-- CROWDING_AUTO_DASH_END -->` 之間的內容（那是 pipeline 管的即時儀表區）。
- **決策時 critic**（repo 規則）：§7 對本站組合下判讀前，spawn `industry-thesis-critic` 對重疊的擁擠 cluster 對應 ID 冷讀，存 `notes/site-internal/id/_critic_Crowding_{YYYYMMDD}.md`（repo-root notes/，不進 published docs/）。
- **git flow**：**預設停下複審**——寫完、self-review gate 通過後**不自動 commit**；把本地路徑給持有人看，待持有人說 push 才走 commit flow（比照 expectations-synthesis 政策）。push 前 `git pull --rebase`；只 `git add` 本期真正要動的三個檔（新報告 HTML＋`docs/crowding/index.html`＋critic md），**不盲 `git add -A`**。

---

## 觸發

- 「跑擁擠交易監測」「crowding monitor」「擁擠交易月報」「新一期 crowding」「positioning monitor」

**不觸發**：純資訊查詢（「擁擠交易是什麼」「creowding 怎麼算」——直接解釋）；要單檔 DD（→ stock-analyst）；要產業深度（→ industry-analyst）。

---

## Pipeline（六步）

### Step 0 — 載入資料層 + 確認時效
1. 讀 `docs/crowding/data/latest.json`。抽出三個資料塊：COT 15 市場、主題擁擠分數（可評分數 / 覆蓋標記）、15 檔 ETF 自身百分位；並記下 `gaps[]` 與**各層 as-of**（COT as-of、主題引擎 as-of、ETF as-of）。
2. **時效硬規則**：COT 常因假期順延（如 6/30 期因 7/4 順延）。以 latest.json 提供的 as-of 為準，**報告開頭與各表 tbl-src 必標 as-of**；若 COT 已非本週，明說「最新讀數已是 N 天前，短期翻轉可能未反映」。
3. 若 latest.json 缺失或 pipeline 尚未跑，**停下並回報**（不要自己捏資料層）。

### Step 1 — 情緒／資金流 web 掃描（層三）
對下列每個主題跑 **3-5 輪 WebSearch/WebFetch**，抽數字時**每個數字帶來源＋as-of 日期＋信心分級**（high＝原文/多源一致；med＝單一二手源或稍舊；low＝方向性推論）：
- **BofA FMS**（最新月）：最擁擠交易排名、現金水位、股票 overweight、尾部風險排序、Bull & Bear Indicator。
- **BofA Flow Show**（最新週）：科技/美股/債券/現金週度資金流、record 級進出、比特幣 ETF 流向。
- **GS Prime**（最新月）：對沖基金總槓桿、板塊淨曝險（半導體等）、downside protection 語言、crowding/concentration 面板。
- **散戶端**：AAII bull/bear spread（連續數週偏空與否）、CNN Fear & Greed、NAAIM 曝險、equity put/call。
- **尾部定價**：VIX 收盤、SKEW、VIX/VXV 期限結構。
- 對每個**未取得**的官方數值（如 FMS equity allocation z-score、GS crowding index 單一讀數），列入 §9 gaps 誠實清單，**不要硬編**。

### Step 2 — 組合 recon（供 §7 read-through）
1. 讀 `docs/picks/candidates.json`（正式榜長熬／爆發席次）＋ stock sleeve handoff（三軌：核心複利／衛星結構／衛星循環）。
2. 對每個持倉，用 latest.json 的主題引擎排名，標出**所屬主題（排名／分數／覆蓋）**與**擁擠讀數**（分數＋覆蓋信心的定性合成）。
3. 對重疊最深的擁擠 cluster 對應 ID，spawn `industry-thesis-critic` 冷讀（見環境常數）。

### Step 3 — 合成報告（填規格，見下方「報告規格」）
把三層收斂。核心敘事＝**三角測量**：三層同向時讀數 robust；三層分歧時（如黃金 COT 偏多 vs ETF 動能鈍化）**誠實標記為不明，不硬給結論**。

### Step 4 — 期刊索引插卡
`docs/crowding/index.html` 的 `<ul class="reports">` 最上方 insert 新 `<li>`；前一期移除 `最新` tag。

### Step 5 — self-review gate（發布前三重檢查，比照 earnings-synthesis v1.1）
**寫稿後、給持有人前**逐項過（任一不過就回頭改，不放行）：
1. **時效與來源**：每個數字都有來源＋as-of？COT as-of 與各層時效在報告開頭與各表都標了？低信心數據都掛了 lo 標記？未取得的數值都進了 §9 gaps 而非被捏造？
2. **口吻與定位**：全報告零「應買入／應賣出／加碼／減碼」指令句？§7 用 GRP／三軌語言、無 IRR 排序語言？描述器定位在 mandate 與各章重申？無鷹架語言（「本版補齊」「先前漏掉」「更新」「changelog」等）？
3. **一致性**：Exhibit 1 named trades 的狀態與 Exhibit 2/3 的數字互相對得上？§7 持倉的主題歸屬與 Exhibit 3 排名一致？中文字後標點全形？

### Step 6 — 停下複審 / git flow
預設**停下**，把本地路徑給持有人。持有人說 push 才 `git pull --rebase` → `git add` 三檔 → commit（訊息格式 `Add crowding monitor: Vol.N YYYY-MM-DD`）→ push main。

---

## 報告規格（固化自創刊號，對齊 `CROWDING_20260705.html`）

視覺與 CSS 直接沿用創刊號（深色主題為主＋light media query；`.exec`／`.tbl-wrap`／`.bar`／`.status`／`.callout`／`.src` 等 class）。結構固定如下：

1. **報告頭**：kicker（`Cross-Asset Crowding Monitor · 第 N 期`）＋ h1「跨資產擁擠交易監測」＋ report-meta（發布日＋**COT as-of＋主題引擎 as-of＋情緒/資金流截止日**，三層時效並列）＋ **mandate 段**（描述器非擇時的既定裁決語言）。
2. **執行摘要**：`.exec` 有序清單，本期 3-5 條判讀，首條 `.hero`。每條數字內嵌 `.src` 來源＋信心。
3. **Exhibit 1｜named trades**：把三層收斂成 6-8 筆**具名交易**，每筆欄位＝交易／方向／擁擠證據（跨源引用）／5y 百分位·主導維度／**unwind 觸發器（具體事件或數字）**／狀態。狀態詞彙固定：`building`（部位仍累積）／`peak`（已極端）／`unwinding`（去化中）／`extreme-contra`（極端但方向為空）／`structural`（結構長存）。附「如何讀這張表」callout：擁擠 ≠ 錯，擁擠告訴你下方緩衝多薄、什麼事件抽掉緩衝。
4. **Exhibit 2｜COT positioning 儀表**：15 市場 net %OI ＋方向＋5y/3y 百分位（bar 顏色＝擁擠熱度）＋Δ4w/Δ13w；極端旗標於 5y ≥90 或 ≤10。附「儀表判讀」與「延伸：15 檔跨資產 ETF 自身百分位」子表。tbl-src 必標 COT as-of 與假期順延情形。
5. **Exhibit 3｜主題擁擠熱力圖**：latest.json 的 64+ 主題（依綜合分數排序）＋A 動能／B 相關／C 上修／E 共識四維＋覆蓋率＋主導維度。**覆蓋薄弱（cov≤5 或 <40%）標 ⚠ 並註明「僅方向性」**；D 量能維度若 NULL 要在方法論說明。附 Top/Bottom 深讀（高信心 vs 低覆蓋分流）。
6. **§情緒與資金流：機構 vs 散戶分岔**：機構端（擁擠且高槓桿）vs 散戶端（AAII/CNN/put-call）雙卡＋尾部定價背離（VIX 低 vs SKEW 高）＋資金流急轉 callout＋**跨源張力誠實標記**（訊號不一致處攤開，不強行調和）。
7. **§對本站組合的 read-through**（最需誠實的一章）：(a) 持倉 × 擁擠 cluster 重疊表；(b) 擁擠對持倉的具體後果（回撤放大／相關上升同跌／天然低擁擠對沖）；(c) 哪些 unwind 觸發器是 DD §13 級證偽、哪些只是波動。**硬規則見下。**
8. **§反向掃描**：投機與動能雙低的資產＋「若要反向需先看到什麼」（描述器，非進場建議；低擁擠 ≠ 該買）。
9. **§方法論附錄與資料血統**：逐層列 as-of／侷限／已知缺口；三角測量邏輯（同向 robust、分歧標不明）；**gaps 誠實清單**（未取得的官方數值逐項列）。收尾 disclaimer＋footer（`描述器非擇時`）。

---

## 硬規則（寫進每一期）

- **中文標點全形**：中文字之後一律全形（，。：；「」）；數字/英文與單位之間照原樣。發布前跑一次標點正規化檢查。
- **描述器非擇時**：全報告零買賣指令句（「應買入／賣出／加碼／減碼／進場／清倉」皆禁）。只描述**擁擠度、脆弱性、unwind 觸發器**。mandate 與各章重申此定位。
- **§7 語言鐵律**：對本站組合的 read-through **只用 GRP／三軌語言**（高成長×EPS 上修×股價位置三閘、核心複利／衛星結構／衛星循環）。**禁 IRR 排序語言、禁買賣指令**。本站賣出紀律是 thesis 級（DD §13/§14 證偽），擁擠度**不是**那個扳機——明說「擁擠告訴持有人回撤會更深、成員會同跌，唯一該重審的是 thesis 級破裂，不是任何一次 positioning 洗盤」。
- **時效必標**：COT as-of 與各層資料時效在報告開頭與各表 tbl-src 都要標；COT 若非本週，明說落後天數與「短期翻轉可能未反映」。
- **信心分級必標**：每個 web 數字掛 high／med／lo；未取得的官方數值進 §9 gaps，**不捏造**。
- **覆蓋率誠實**：主題引擎覆蓋薄者標 ⚠「僅方向性」；區分「相對排名」與「絕對水位」（45 分不代表市場不擁擠，只代表比此宇宙的 AI cluster 不擠）。
- **無鷹架語言**：不出現「本版補齊／先前漏掉／更新／changelog」等 stingtao 殘留；報告是獨立成期的一份判讀。
- **不動 pipeline 疆界**：唯讀 latest.json；不改 build_crowding.py、data/、`docs/crowding/data/`、workflow，也不改 index.html 的 AUTO_DASH 標記間內容。
