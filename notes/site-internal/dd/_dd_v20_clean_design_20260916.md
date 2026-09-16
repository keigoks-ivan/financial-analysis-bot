# DD 管線 v20 設計稿：從零重練

日期：2026-09-16
狀態：§13 四題已於 2026-09-16 拍板，可進原型
範圍：`ddreport` skill 背後的生產管線。skill 本身維持一個、一條指令。

## 0｜結論

LLM 只做四件事：查、判、審、寫。每件事一通，打完就掛。其餘全部交給程式。
判斷只在五個點出手，單輪、無修補輪。沒有修補輪。證據按軸過期，不按 run 過期。
估計全新一檔從 $17 到 $22 降到 $10 到 $14，重跑一檔從 $16 降到 $5 到 $8（2026-09-16 量測後修正）。時間從約 60 分降到約 25 分。以上是估計，驗收見 §10。

## 1｜為什麼要打掉

現行 `scripts/ddreport.py` 有 6,288 行，`dd_*.py` 合計 19,028 行。功能沒有問題，問題是錢和時間花在修正 LLM 輸出的形狀。

TXN 2026-09-07 全套實際帳單（manifest 各段加總）：

| 段 | 模型 | 通數 | 花費 | 占比 |
|---|---|---|---|---|
| 收證據 | sonnet | 3（11 軸沿用前一天） | $1.25 | 8% |
| 判斷 | Fable | 2 | $9.88 | 62% |
| 閘 | opus | 2 | $3.16 | 20% |
| 散文 | sonnet | 1 | $1.70 | 11% |
| 合計 | | 8 | $16 | |

三個結構性浪費：

1. 判斷的錢花在輸出。Fable 一通吐 55K 到 93K 個 token，`judgment.json` 有 62KB。v19 契約說判斷只出手五個點，其餘由 `dd_project.py` 投影，但實際輸出量沒有降下來。
2. 修補輪。判斷 JSON 形狀不對就再開一通 Fable 修。每通 $0.8 到 $1.5，快取命中為零（`cache_read=0`，整包重送）。TXN 2026-09-10 修了 3 通，$2.6。修的是機械欄位形狀（checkpoints、capital_returns），本該由程式處理。
3. 輸入包重複。判斷 bundle 有 270KB，同時放 facts.json（100KB，evidence 的整理版）和 evidence.json 原文（187KB）。閘 bundle 有 125 到 220KB，放 judgment 全文。

第二個問題長出一整套周邊：replay、delta 路由、short 與 loop 雙模式、patch map、JSON repair。這些加起來占 `ddreport.py` 超過一半。修補輪拿掉，它們都不需要了。

## 2｜設計原則

1. 一通一事。每通 LLM 有固定的輸入契約、固定的輸出 schema、固定的模型。不給工具的通一律單輪。
2. 形狀由程式管。LLM 的輸出先過 schema 驗證。能機械修的修，不能修的直接 FAIL 停下來。不開第二通 LLM 修形狀。
3. 事實只查一次。證據庫按軸存，每軸自帶保存期限。重跑只查過期的軸。
4. 判斷寫小、程式算大。判斷只給假設和裁定，EV、IRR、燈號、表格全由程式算。

## 3｜架構

```
證據庫 facts/{T}/          （程式，零 LLM，跨 run 累積）
   │
   ├─ 查   sonnet × N 並行   只查過期的軸，每軸一通，有 WebSearch
   │
   ▼
事實表 facts.json          （程式合併，帶 fact id）
   │
   ├─ 判   Fable × 1 單輪    輸入：事實表 + 規則卡。輸出：judgment.json（5 到 8KB）
   │
   ├─ 算   程式              scenario / decision / 燈號 / 表格 / dd-meta JSON
   │
   ├─ 審   opus × 1 單輪     輸入：judgment + 事實表 + 閘卡。輸出：紅黃燈清單
   │        紅燈 → FAIL 停下來，回報持有人。不自動修。
   │
   ├─ 寫   sonnet × 1        輸入：judgment + 程式算好的表。輸出：HTML 散文段
   │
   └─ 發   程式              組頁、verify_dd_math、update_dd_index、commit、push
```

通數：全新一檔 4 + N（N 為過期軸數，最多 12）。重跑一檔常見為 3 到 5 通。

## 4｜每一通的契約

### 4.1 查（coverage agent）

| 項目 | 規格 |
|---|---|
| 模型 | sonnet |
| 工具 | WebSearch、WebFetch、Write |
| 輪數上限 | 8。分段軸（end_markets）12 |
| 並行 | 8 |
| 輸入 | 一軸的題目與查詢詞（≤ 5KB）。不附任何規則檔 |
| 輸出 | `facts/{T}/axes/{axis}.json`，每條 finding 帶 source、as_of、direction |
| 失敗 | 超輪數視為該軸 `status=incomplete`，寫進事實表的 gaps。不重試 |

跟現在的差別：現在每批 2 軸一通，改成每軸一通。理由是 TSM 2026-09-11 實測每軸 $0.3 到 $0.5，合併兩軸並沒有省，反而撞輪數。

### 4.2 判（judge）

| 項目 | 規格 |
|---|---|
| 模型 | Fable（持有人 2026-09-06 拍板） |
| 工具 | 無。單輪。回覆全文即 JSON |
| 輸入 | 事實表 facts.json（目標 ≤ 60KB）+ 最新一季逐字稿（原文）+ 判斷卡（≤ 16KB）+ 兩張常載附卡（ROIC 持續期、判斷手冊，各 ≤ 4KB）+ 條件附卡（循環股、特殊 archetype，命中才載，各 ≤ 4KB）+ 前份判斷摘要（≤ 5KB） |
| 輸出 | judgment.json，形狀＝v19 契約（judge-owned 欄）。實測 v19 判斷物 33K 到 40K 字，這是六問的結論與理由，不是灌水。目標 ≤ 30K 字 |
| 預算 | 思考上限 32K token（`MAX_THINKING_TOKENS`，待驗證生效）；輸出 JSON ≤ 30K 字。2026-09-16 實測 TXN judge_1：輸出 55K token，其中思考 30K、JSON 約 25K |

不再附 evidence.json 原文和前三季 digest。理由：事實表就是它們的整理版，兩份都放讓 Fable 每通多讀 190KB，且 2026-09-11 之後沒有證據顯示原文有被引用到事實表以外的內容。若驗收發現判斷品質掉，回補的順序是「先補事實表的涵蓋」，不是把原文塞回去。

規則卡是新東西。從 `references/v16/judgment-rules-v19.md`（45KB）抽出判斷五個點真正需要看的判準，壓到 16KB 以內。卡是人工濃縮（sonnet 抽、人審），存 `scripts/dd2/cards/`，檔頭記來源 sha256；`cards.py check` 在來源變動時報 STALE，不自動重生。references 仍是權威，規則卡是它的投影。2026-09-16 實作發現：roic-durability 與 judgment-playbook 在現行路由是每次都載，不是 archetype 條件式，故判斷通規則總量約 24KB。

### 4.3 審（gate）

| 項目 | 規格 |
|---|---|
| 模型 | opus（writer 與 critic 永不同模型） |
| 工具 | 無。單輪 |
| 輸入 | judgment.json + 事實表 + 閘卡（`gate_contract.md` 的精簡版，≤ 8KB） |
| 輸出 | 固定 schema 的清單：`[{item, light, judgment_path, reason}]` |
| 處置 | 紅燈 ≥ 1 → 管線停在 `gated_fail`，印清單，不發布。黃燈只記錄 |

不再有閘後修補。紅燈是「判斷級」的錯，該由持有人決定重跑還是改規則，不該由程式再開一通 Fable 修改。閘的覆蓋面掃描與量化模組抽查兩項職責保留（2026-08-06 拍板）。

### 4.4 寫（prose）

| 項目 | 規格 |
|---|---|
| 模型 | sonnet |
| 工具 | Write |
| 輪數上限 | 6 |
| 輸入 | judgment.json + 程式算好的表格 HTML + 呈現規則卡（從 render-rules.md 抽，≤ 10KB） |
| 輸出 | 各章散文 HTML 片段，程式組頁 |
| 失敗 | 篇幅低於 `DD_FULL_FLOOR_BYTES` 直接 FAIL。不補寫輪 |

### 4.5 統一的 spawn 層

一個 `spawn(prompt, model, tools, max_turns, schema)` 函式。回傳原始 JSON 與 usage。所有通都走它。沒有 oneshot、short、loop 三套。現行 `dd_headless.py`（346 行）可直接沿用。

## 5｜證據庫與過期規則

`facts/{T}/` 跨 run 累積，不放在 `.dd_build/runs/` 裡。每軸一個檔，檔頭有 `fetched_at`。

| 軸類 | 保存期限 | 強制刷新條件 |
|---|---|---|
| 財報數字（Koyfin） | 到下一次財報 | 新一季逐字稿出現 |
| 競爭、客戶、供需、終端市場 | 90 天 | 新一季逐字稿出現 |
| 法規、關稅、地緣、替代技術 | 180 天 | 無 |
| 資本市場定價 | 30 天 | 股價變動 > 20% |
| 重大事件 | 14 天 | 無 |

現行 `_axis_reuse_decision` 和 `dd_delta.py` 的判斷邏輯可以抽進來，但只保留「這軸要不要重查」一個問題。delta 判斷路由（Fable 只補部分欄位）不做。判斷永遠整份重做，因為判斷通已經很小。

## 6｜程式做的事

全部零 LLM，多數已存在，直接沿用：

| 事 | 現有腳本 | 動作 |
|---|---|---|
| 抓數字 | `dd_numbers_extra.py`、Koyfin 下載 | 沿用 |
| 前份判斷 | `dd_prior.py` | 沿用 |
| 事實表初稿 | `dd_facts.py extract` | 沿用，去掉 sonnet 補題那段 |
| 情境樹算術 | `dd_scenario.py` | 沿用 |
| 決策矩陣 | `dd_decision.py` | 沿用 |
| 投影燈號與 dd-meta | `dd_project.py` | 沿用 normalize 與 project，去掉 patch 路徑 |
| 驗算 | `verify_dd_math.py` | 沿用 |
| 發布同步 | `update_dd_index.py` | 沿用，一字不改 |

新寫的只有三個：`facts_store.py`（證據庫與過期）、`cards.py`（從 references 生成規則卡、閘卡、呈現卡）、`run.py`（主流程，目標 ≤ 800 行）。

## 7｜失敗處理

每通只有三種結果：PASS、FAIL、INCOMPLETE。

- 查：INCOMPLETE 記進 gaps，管線繼續。
- 判：schema 驗證失敗先跑 `dd_project.py normalize`（只修路徑、欄名、單物件包陣列）。仍失敗 → FAIL 停下。
- 審：紅燈 → FAIL 停下。
- 寫：篇幅不足 → FAIL 停下。

FAIL 的回報固定格式：哪一通、哪個欄位、原始輸出存在哪。持有人看完決定重跑或改規則。管線不自己再開 LLM 修。

## 8｜不變的東西

- skill 一個、指令一條：`python3 scripts/dd2/run.py {T}`。
- `references/` 是判斷與呈現規則的權威。規則卡是投影，不是取代。
- dd-meta JSON 的欄位與形狀不變。15 支下游腳本在吃（`build_dd_screener.py`、`build_picks.py`、`build_cyclical_track.py` 等），任何一欄變動都要先過 `update_dd_index.py`。
- writer 與 critic 永不同模型。判斷 Fable、閘 opus、其餘 sonnet。
- 快速版 `docs/dd/brief/` 照產，等持有人拍板停產。
- 發布前 `verify_dd_math.py` pre-commit 閘不動。

## 9｜估計的帳單與時間

| | 現在（實測） | v20（估計） |
|---|---|---|
| 全新一檔 | $17 到 $22 | $10 到 $14 |
| 重跑一檔 | $16 | $5 到 $8 |
| 牆鐘時間 | 約 60 分 | 約 25 分 |
| LLM 通數 | 8 到 17 | 4 到 16，重跑常見 3 到 5 |
| 主流程行數 | 6,288 | ≤ 800 |

估計依據（2026-09-16 量測後修正）：判斷通省的是單輪（不再 4 輪重讀 640K cache）、零修補輪（每輪 $0.8 到 $1.5，快取零命中）、思考上限；JSON 本體 33K 到 40K 字不變。判斷通估從 $7 到 $10 降到 $3 到 $5。閘二輪歸零省 $1.3。另每個 `claude -p` 子程序夾一筆 haiku 約 100K input（$0.10），17 通就 $1.7，待查能否關。原稿寫的「判斷輸出砍到十分之一」不成立，已撤回。

## 10｜驗收

拿三檔對照跑：TXN（有前份、可重跑）、TSM（全新、12 軸）、一檔循環股（換尺路由）。舊鏈與 v20 各跑一次，同一天。

過關條件：

1. 三檔裁決方向（進場、觀望、迴避）與倉位角色跟舊鏈一致。
2. 三個數字（5Y EV%、IRR base%、Max DD%）差異在 ±3 個百分點內。
3. 閘紅燈 0。
4. 帳單低於舊鏈 40% 以上。
5. 篇幅在 70KB 到 115KB 帶內。

任一不過，v20 不上線，列出原因回到本稿修。

Kill condition（登記 `knowledge/rule_ledger.md`）：上線後 90 天內，v20 判斷因「事實表漏收、原文有的證據」被翻面 ≥ 1 例，判斷輸入回補 evidence 原文。

## 11｜檔案清單

```
scripts/dd2/
  run.py            主流程，plan → gather → facts → judge → project → gate → prose → publish
  facts_store.py    證據庫，每軸保存期限，過期判斷
  cards.py          從 references/ 生成三張卡：judge_card.md、gate_card.md、prose_card.md
  spawn.py          包一層 dd_headless.spawn，統一 schema 驗證與 usage 記帳
  schemas/
    judgment.v20.json
    gate_result.v20.json
  prompts/
    coverage.md.tmpl
    judge.md.tmpl
    gate.md.tmpl
    prose.md.tmpl
facts/{T}/
  axes/{axis}.json
  numbers.json
  transcripts.json
```

舊鏈 `scripts/ddreport.py` 與 `dd_*.py` 原地不動，直到 §10 驗收通過。切換用 skill 的指令行一處改。回退：改回原指令。

## 12｜不做的事

- 不拆多個 skill。
- 不做 replay、delta 判斷路由、short 與 loop 雙模式、patch map、JSON repair agent。
- 不動 references 的門檻與矩陣。
- 不動 update_dd_index.py 與下游 15 支腳本。
- 不做閃判（`dd_flash.py`）的整合，另案。

## 13｜持有人拍板（2026-09-16）

1. 判斷輸入拿掉 evidence.json 原文與前三季 digest（§4.2）。拍板：拿掉。事實表即其整理版，重複輸入無證據顯示有用。以 §10 kill condition 保底。
2. 閘紅燈不自動修（§4.3）。拍板：不自動修。紅燈是判斷級的錯，同一模型再修等於自審。停下來給人看。
3. 證據庫保存期限（§5）。拍板：照表，重大事件由 30 天改 14 天。該軸最常突變，多查一軸僅多約 $0.3。
4. 判斷輸出 token 上限（§4.2）。拍板：15K。**2026-09-16 量測後修正**：v19 判斷物 JSON 本體就有 25K token，15K 做不到；改為思考上限 32K、JSON ≤ 30K 字，總輸出預期 45K 上下。撞上限先查多寫了什麼，不先調高。
