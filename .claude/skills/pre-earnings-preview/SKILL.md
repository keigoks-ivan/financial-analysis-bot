---
name: pre-earnings-preview
description: "收到一個 ticker（或「本週財報 preview」）後，先用 scripts/snapshot_consensus.py 把財報前的市場期望凍結成不可變的錨（共識 EPS/營收、現價、ATM straddle 隱含波動、base_eps_path 承保錨），再讀該檔既有 DD 的 §3.B 核心假設 / §6.I 分部 build / §11.5 三情境 / §1 監測指標，合成一份一頁式財報前瞻 HTML（docs/earnings/preview_{TICKER}_{YYYYMMDD}.html）：凍結快照塊 + 三情境 × 管理層 commentary 聽點 + ranked catalyst checklist + implied move 錯價判讀 + 複盤掛鉤草稿。是消費端 skill（假設 DD 已存在、只讀不改；不重做基本面、不抓 filing）。觸發：『{ticker} 財報前瞻 / preview {ticker} / {ticker} earnings preview / 財報 setup {ticker} / 本週財報 preview』。"
---

# pre-earnings-preview（財報前瞻 · 賽前錨 × 三情境 × 錯價判讀）v1

> **定位**：消費端 skill。假設目標 ticker 的 DD（`docs/dd/DD_{TICKER}_*.html`，含
> §3.B / §6.I / §11.5 / §1）已存在；**本 skill 不重做基本面、不抓 filing、不改任何 DD**。
> 它把「財報前市場對這一季的期望」定格成不可變的錨（`snapshot_consensus.py`），再把
> DD 承保時的假設攤成三情境，問一個窄而具體的問題：**「這一季市場 price 的是哪個情境？
> implied move 相對三情境的幅度是貴還是便宜？財報當下要聽管理層講什麼才知道走哪條路？」**
>
> **與 expectations-synthesis 的差別**：後者問「市場對『未來數年 EPS』的預估是否錯」（跨季、
> 跨賣方）；本 skill 只鎖「**這一次財報這一季**」的賽前 setup，時間尺度是單一事件。
>
> **與 stock-analyst 的差別**：stock-analyst 問「這公司好不好、裁決是什麼」（重做研究）；
> 本 skill 只消費既有 DD + 凍結快照 + 輕量 web，不產生新裁決、不改 dd-meta。

---

## 環境常數（已鎖定）

- 凍結錨工具：`scripts/snapshot_consensus.py`（deterministic；**永不覆寫**，賽前錨一旦寫下即凍結）
- 快照檔：`docs/catalyst/snapshots/preview_{TICKER}_{YYYYMMDD}.json`（YYYYMMDD = 財報日）
- 前瞻報告：`docs/earnings/preview_{TICKER}_{YYYYMMDD}.html`（`preview_` 前綴，push-earnings 的
  `earnings_YYYY-MM-DD.html` regex 不會誤抓——同 `synthesis_` 前例）
- 索引：`docs/earnings/index.html` 的 `<ul class="reports">`，最上方 insert 一張帶「財報前瞻」tag 的卡片
- 日曆錨：`docs/catalyst/calendar.json`（財報日）、`docs/catalyst/variance.json`（承保 vs 共識漂移）
- 預設**停下複審**：寫完、驗證通過後**不自動 commit**；把本地路徑給用戶看，待用戶說 push 才走 commit flow

---

## 觸發

- 「{ticker} 財報前瞻」「preview {ticker}」「{ticker} earnings preview」「財報 setup {ticker}」
- 「本週財報 preview」→ **不指定單一 ticker**：讀 `calendar.json`，列出「7 天內、且 positioning.dca_verdict
  相關（進場 / 持倉）」的財報事件，回問用戶「這幾檔要跑哪一檔（或全部）」，得到答案後逐檔走下面流程。

**不觸發**：純資訊查詢（「{ticker} 何時財報」→ 直接查 calendar.json 回答）、要單檔 DD（→ stock-analyst）、
要跨季期望落差綜合（→ expectations-synthesis）、財報**後**複盤（本 skill 只做賽前；賽後回填見 §尾段）。

---

## 資格閘（Eligibility gate）

跑之前先讀該 ticker 最新 v13/v14 dd-meta（`scripts/dd_meta_reader.py`）：

1. `dca_verdict == 進場` → **正常跑**。
2. `dca_verdict ∈ {觀望, 迴避}` 但**用戶明確點名**要跑 → **照跑不擋**，但報告頂部與 §0 明確標註
   「**本標的現行裁決＝{觀望/迴避}，非進場部位；本前瞻僅為事件觀察，不構成建倉訊號**」。
3. **完全沒有 DD**（`docs/dd/` 無此 ticker 任何 v13/v14 檔）→ **拒絕**，回一句：「{ticker} 尚無 DD，
   財報前瞻需要 §3.B/§6.I/§11.5/§1 當骨架——請先跑 stock-analyst（`跑 {ticker} DD`）。」不硬湊。

---

## Pipeline

### Step 0 — 凍結錨先落盤（**FIRST，賽前錨優先**）

```
python3 scripts/snapshot_consensus.py {TICKER}
# 財報日若 calendar.json / yfinance 都給不出，或要覆寫既定日 → 加 --earnings-date YYYY-MM-DD
```

- **成功寫檔** → 記下 `docs/catalyst/snapshots/preview_{TICKER}_{YYYYMMDD}.json` 路徑，Step 4 直讀它渲染。
- **回報「已凍結、拒絕覆寫」（exit 3）** → **不是錯誤**：代表今天已對這場財報凍過錨。**直接複用既有 JSON**
  重新渲染 HTML（idempotent re-render 允許；錨不可變，但報告可重生）。**絕不**為了重抓數字而刪檔重跑——
  刪掉賽前錨＝改寫事後複盤的基準，違反本 skill 前提。
- **exit 2（財報日無法解析）** → 回用戶要 `--earnings-date`，別瞎猜日期。
- 快照裡任何 `null` 欄位（honest-fail）→ 在報告對應處誠實標「共識/現價/隱含波動：yfinance 當日未取得」，
  **不要**用記憶或估值回填凍結區。

### Step 1 — 讀既有 DD（只讀不改）+ 日曆/漂移錨

從最新 `docs/dd/DD_{TICKER}_{YYYYMMDD}.html` 抽（用 grep/Read 定位錨點，不重算）：
- **§3.B**：三個核心假設（每個帶 sourced floor / 編號）——這是三情境的**營運驅動骨架**。
- **§6.I**：三年分部前瞻 build 的數字（分部營收/利潤率/EPS 橋）——情境的**量化刻度**。
- **§11.5**：Bull / Base / Bear 5Y 端點 + 機率——本 skill 把它**降維到「這一季」**的方向讀法。
- **§1**：最關鍵監測指標表（含閾值）——ranked catalyst checklist 第一條**必須**來自這裡。
- **variance.json**：該 ticker 的 `drift_pct` / `flag`（承保 Base vs 當下共識已漂移多少）——餵 §4 錯價判讀。

### Step 2 — 輕量 web（**hard cap ≤ 4 searches**）

只查兩類、且**只為賽前 context**，不做基本面研究：
1. **近 4 季財報日次日股價反應**（beat/miss + 隔日 %）——**必 WebSearch 查證，禁用記憶**（見硬規則）。
2. **最新共識 / whisper 語境**（街頭對這季的關注點、buy-side whisper 高於或低於 sell-side 共識的定性說法）。

**禁止**：抓 10-Q/10-K/8-K、重建競爭分析、重算估值、開新 IRR。若查到的資訊顯示 **DD 假設已明顯過時**
（如 §3.B 某假設的前提已被推翻）→ 在報告 §2 對應列標一句「**⚠ 此假設可能已過時，建議重跑 DD**」，
**而非**自行補研究把它救回來。

### Step 3 — 合成 HTML

- **樣式沿用 `docs/earnings/` 既有慣例**：先 `Read` 一份近期 `docs/earnings/earnings_*.html`（如最新那份）
  複用其 `<head>` / CSS / 字體 / 色票 / `<meta name="robots" content="noindex">`。**一頁式，目標 ~15–25KB**。
- 章節（見下方「報告結構」五節）。
- 中文全形標點；凍結區數字**直讀 JSON**，禁止與快照不一致。

### Step 4 — 驗證閘（commit 前 hard gate，跑 bash 自檢）

- **凍結區一致性**：報告裡渲染的共識 EPS / 營收 / 現價 / implied move / frozen_at **逐字等於** JSON
  對應欄位（grep 比對；不一致＝違規）。
- `div` open/close 平衡；`<meta name="robots" content="noindex">` 在。
- DD 下鑽連結（`/dd/DD_{TICKER}_*.html#s3` 等）目標檔存在（`[ -f ]`）。
- **無 slang**（`梭哈|踏空|嚇人|硬幣|死等|打臉|空手|滿倉追`）、**無自我對話**（`我[^們]|你`，管理層引號內例外）。
- **無跨檔對照**：報告只講本 ticker（除非同業對照是 DD §11.5 明列的、且只作情境刻度引用）。
- HTML 檔大小落在 ~15–25KB。

### Step 5 — 複審 → commit（停下，待用戶 go）

- 預設**把本地檔路徑 + 裁決/edge 摘要給用戶看**，**不自動 commit**。
- 用戶說 push 後，`git add` **只加三檔**（先 `git status` 看 `??` 沒 orphan，**不要 `git add -A`**）：
  - `docs/earnings/preview_{TICKER}_{YYYYMMDD}.html`
  - `docs/catalyst/snapshots/preview_{TICKER}_{YYYYMMDD}.json`
  - `docs/earnings/index.html`（新增的財報前瞻卡片）
- commit 訊息：`Add {TICKER} 財報前瞻 (pre-earnings preview) + frozen consensus snapshot`，
  結尾 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`。
- **push 前先 `git pull --rebase origin main`**（並行 cron 常推），rebase 後重查卡片 + snapshot 都在，再 push。

---

## 報告結構（五節，一頁式）

**1. 凍結快照塊**（rendered **FROM the snapshot JSON verbatim**）
- 共識 EPS / 共識營收 / 現價 / implied move %（含 straddle 到期日；若 `implied_move_proxy` 非 null，
  標明「以 {proxy} 代理」）/ `frozen_at` 時戳。
- 醒目標語：**「賽前錨 · 事後不改（frozen at {frozen_at}）」**。任何 null 欄位誠實標「當日未取得」。

**2. 三情境表 Bull / Base / Bear**（每列三欄 + 一欄股價）
- **營運驅動**：引 DD §3.B 假設**編號** + §6.I build **數字**（如「假設②資料中心營收 QoQ +X%，對應 §6.I 分部橋 EPS $Y」）。
- **管理層 commentary 聽什麼**：具體訊號**詞句**（如「毛利率 guidance 是否守住 5X%」「capex 全年上修 vs 維持」「某產品 ramp 用『on track』還是『ahead』」）——要可聽、可證。
- **若出現 → 股價含義**：該情境成立時的方向與量級判讀。
- 末欄：**情境股價區間 vs implied move 併排**（讓讀者一眼看到市場定價的隱含幅度落在三情境的哪一段）。

**3. Ranked catalyst checklist（3–5 條）**：格式 `[指標] vs [共識/DD 閾值]`
- **第一條必是 DD §1 帶閾值的監測指標**（本 skill 的 anchor catalyst）。
- 其餘按「對裁決的影響力」排序，各條標「達標/破線各代表什麼」。

**4. 錯價判讀（implied move vs 三情境）**
- implied move 對比 Bull/Bear 幅度：市場 price 的是哪個情境？隱含波動買貴了還是便宜了？
- 併入 `variance.json` 的承保 drift（共識已比 DD Base 漂移多少）——賽前市場期望相對我們承保錨的位置。

**5. 尾段「複盤掛鉤」**
- 一段預填的 **event_outcome ledger 草稿**（放 code block 的 JSON；`kind` = `event_outcome`、
  帶 `snapshot` 路徑、`expected` = 共識 + base 情境一句話；`actual` / `verdict` **留空待人工**）：

  ```json
  {"kind":"event_outcome","ticker":"{TICKER}","earnings_date":"{YYYY-MM-DD}","snapshot":"docs/catalyst/snapshots/preview_{TICKER}_{YYYYMMDD}.json","expected":"共識 EPS ${eps} / 營收 ${rev}；Base 情境＝{一句話}","actual":"","verdict":""}
  ```

- 一句提示：**財報後回填 `docs/catalyst/archive.json` 對應事件的 `outcome` 欄**（人工所有欄位），
  完成賽前→賽後閉環。

---

## 硬規則（實戰約束，不可省）

1. **凍結錨優先且不可變**：Step 0 一定先跑 `snapshot_consensus.py`。回報已凍結＝複用既有 JSON 重渲染，
   **絕不刪檔重跑**。凍結區數字**直讀 JSON**，渲染值與 JSON 不一致＝違規（Step 4 grep 攔）。
2. **反範圍蔓延（anti-scope-creep）**：本 skill 只讀 DD §3.B/§6.I/§11.5/§1 + calendar/variance/snapshot JSON
   + ≤4 次輕量 WebSearch。**不重做基本面、不抓 filing、不改任何 DD、不動 dd-meta、不開新 IRR/估值**。
   DD 假設疑似過時 → 一句「建議重跑 DD」標註，**不自行補研究救回**。
3. **歷史股價反應必 WebSearch 查證**（近 4 季 beat/miss + 次日 %）——**禁用記憶**。反直覺數字先查證
   （見 repo memory：曾對 SNDK/MU 憑記憶斷言、方向全錯）。
4. **資格閘**：非進場部位照跑但全篇標「非進場、僅事件觀察」；無 DD 直接拒絕導去 stock-analyst。
5. **「No findings is a finding」**：若共識 EPS 與 DD base 情境**一致、implied move 不偏、drift 貼合**——
   **明說「市場與底稿無分歧，本次 preview 無 edge，維持 §1 監測、不加碼不預判」**，不要硬擠出假 edge。
6. **中文全形標點**（中文字後用 `，。：；「」`）；數字/英文與單位照原樣。
7. **專業賣方口吻**：無 slang、無「我/你」自我對話、不渲染分析流程鷹架（Step 代號 / QC / critic 握手）。
8. **noindex**：報告 `<meta name="robots" content="noindex">`（內部研究）。
9. **一頁式 ~15–25KB**：這是賽前 setup 便條、不是第二份 DD——競爭/估值深度住 DD，本頁只連出不複製。
10. **git 衛生**：`git add` 只加三檔、不 `-A`；commit 前 `git status` 看 `??`；push 前 `git pull --rebase`。

---

## 反模式（別做）

- ❌ Step 0 之前先寫 HTML（錨沒落盤就渲染，數字無所本）。
- ❌ 快照回報已凍結時刪檔重抓（改寫事後複盤基準）。
- ❌ 凍結區用記憶/估值回填 null 欄位，或渲染值與 JSON 不一致。
- ❌ 把報告寫成第二份 DD（重做基本面 / 抓 filing / 開新 IRR / 改 dd-meta）。
- ❌ 歷史股價反應憑記憶寫、不 WebSearch。
- ❌ 共識與底稿一致卻硬擠 edge（該說「無分歧、無 edge」）。
- ❌ 半形標點跟在中文字後；slang；「我/你」自我對話。
- ❌ `git add -A`（掃並行 session 的 orphan）；commit 前不 `pull --rebase`；自動 commit。

---

## Plumbing 摘要

- **凍結錨工具**：`scripts/snapshot_consensus.py`（deterministic、永不覆寫、honest-fail）。
- **無 pre-commit validator**（同 comparisons / synthesis 政策）；索引卡片走 skill-append（同 push-earnings 模式）。
- **size-floor gate 不適用**（非 `docs/dd|dca` 檔）。
- **3 檔 commit**：preview HTML + snapshot JSON + earnings/index.html。
- **前綴不撞**：`preview_` 不被 push-earnings 的 `earnings_YYYY-MM-DD.html` regex 誤抓（synthesis_ 前例）。
- 賽後閉環：財報後人工回填 `docs/catalyst/archive.json` 的 `outcome`（cron 永不覆寫人工欄位）。
