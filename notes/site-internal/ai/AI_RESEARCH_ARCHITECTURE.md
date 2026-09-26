# AI Research Architecture：現況分析與地端模型定位

> 2026-09-26 初稿。只做分析，沒有改任何生產程式。
> 位置說明：原本指定放 `docs/`，但本 repo 的 `docs/` 就是公開網站根目錄（GitHub Pages 直接發布），而且並行 session 的廣域 `git add` 會把未追蹤檔掃上線。所以放在 `notes/site-internal/ai/`。

---

> **結論框**
> 你現在用 LLM 的方式，**九成以上是判斷與研究型工作，不適合地端模型**。真正適合地端的只有三塊：每日情報分類、券商 PDF／逐字稿抽取、研究庫語意檢索。
> 這三塊加起來，佔你 LLM 工作量的比例不高，而且目前都跑在訂閱額度內、邊際成本接近零。
> 所以 **Mac mini 64GB 現在不值得「為了這個專案」買**。先用手上的 M5 16GB 跑一輪真實任務基準測試，過了再說。

---

## 1. 現況：repo 實際長什麼樣（不是假設）

### 1.1 網站怎麼產生

- `docs/` ＝整個網站。`deploy-pages.yml` 在 push `docs/**` 時發布，另有每 6 小時補發、`pages-auto-heal.yml` 每 15 分鐘自癒。
- 58 支 GitHub Actions：抓價、抓基本面、跑 screener、建頁面、寄信。**只有 2 支會叫 LLM**（`intel-2-daily.yml`，以及已停用的 `daily_analysis.yml`）。
- 資料全是 JSON／JSONL 檔。唯一資料庫是 `knowledge/brain.db`（SQLite FTS5 全文索引，567MB，gitignored，不在網站上）。
- 沒有 API server。唯一的 server 是本機 `knowledge/brain_server.py`（127.0.0.1:8873）。

### 1.2 LLM 現在怎麼被呼叫

**關鍵事實：不走 API，全部走 Claude 訂閱。** 程式用 `claude -p` 無頭模式，並刻意清掉 `ANTHROPIC_API_KEY`，避免被 API 計費。

| 呼叫點 | 模型 | 做什麼 | 地端可行性 |
|---|---|---|---|
| `scripts/dd2/run.py` stage0 | sonnet，每軸一通 | 上網採證（agentic，帶工具） | 低：需要多步網搜＋判斷相關性 |
| `scripts/dd2/run.py` judged | opus 單輪 | DD 判斷：情境樹、H/R 假說、裁決 | **不可** |
| `scripts/dd2/decide.py`＋gate | opus／sonnet 交叉 | 冷讀閘門 | **不可**（跨模型獨立性是品質前提） |
| `scripts/dd2/run.py` prose | sonnet ×2 並行 | 寫公開散文 | 低：對外文字品質門檻高 |
| `scripts/intel/classify.py` | haiku，日上限 440 張 | 新聞卡分類 | **高** |
| `scripts/intel/summarize.py`／`deepread.py` | sonnet，日上限 80／12 | 摘要、深讀 | 中：摘要可，深讀不可 |
| `scripts/intel/theme_weekly.py` | sonnet | 週主題彙整 | 中低 |
| 雲端 routine：`idea-watch-auto`、`market-read-auto`、`horizon-memo-auto` | session 模型 | 查核點判定、市況判讀、備忘 | **不可**：都是判斷 |
| 互動 skill：industry-analyst、macro-analyst、id-review、critic | opus／sonnet | 產業研究與冷讀 | **不可** |
| `scripts/dd_codex.py` | GPT 系列 | 第三方判斷模型選項 | — |

**已經存在的「路由」**：沒有通用 router，只有幾張寫死的對照表——`ddreport.GATE_MODEL_FOR`（判斷↔閘門交叉配對）、`dd_simple.REVIEW_MODEL_FOR`、`intel/llm.py` 的每日上限。CLAUDE.md 的模型路由表是給人看的散文。

**成本量級**（`scripts/dd2/README.md` §8）：一份 v20 DD 約 $9 等值（舊鏈 $16）；判斷一步約 $3.5–5、11–17 分鐘。這些是 API 等值金額，實際走訂閱額度。

### 1.3 研究記憶已經有什麼

你已經有一套相當完整、但分散的「研究物件」：

| 需求欄位 | 現在放在哪 |
|---|---|
| hypotheses[] | `scripts/dd_schema/judgment.schema.json` 的 `thesis{H[≥3], R[≥3], single_thing}` |
| contradictory_evidence[] | judgment 的 `counter_evidence{blind_spots, contradictions, triggers}`、`evidence_dismissed` |
| evidence[]／sources[] | `facts/{T}/axes/*.json`（findings：claim／source／as_of／direction）＋`facts.json`（含 `quote`） |
| invalidation_conditions[] | dd-meta／id-meta 的 `kill_metrics[]`；`docs/ideas/ideas.json` 的 `refutes_if` |
| monitoring_variables[] | `kill_registry.json`（1017 條）→ `kill_watch.json`（12 條機器可監測） |
| conclusion／confidence | dd-meta `verdict`／`dca_verdict`／`p_bull_pct`；id-meta `conviction` |
| status | ideas 查核點 `supports/shaky`；rule_ledger `KEEP/KILL`；沒有統一的研究生命週期狀態 |
| 決策與事後對帳 | `knowledge/decisions.jsonl`＋`settlement.json`＋`forecasts.jsonl`（1283 筆，Brier＋SPRT） |
| 回測紀律 | v7-backtest 各 `*_Spec.md` 的「預註冊」、`rule_ledger.md` kill condition、track JSON 的 PREREG 區塊 |

**結論：不要重寫 schema。** 缺的是兩件小事：

1. **證據來源欄位不完整**。`facts/{T}/axes` 的 findings 沒有 URL 欄位（`source` 是自由文字）、沒有原文摘錄；抓取日期只在軸層級。`ideas/data/research.json` 的 `summary` 把原文與解讀混在一起，也沒有來源發布日。
2. **物件之間沒有連線**。例：AMD 案裡，ideas 查核點 cp7／cp9 跟 DD 的 `kill_metrics` 互不知道對方。

### 1.4 回測

- 主 repo 沒有共用回測框架，每支腳本獨立。v7-backtest 是正式回測場（成本 14bp 來回、調整後股價、t+1 執行、預註冊文件）。
- 紀律面已經比多數機構好：預註冊、凍結門檻、kill condition、跨標的樣本外、bootstrap、影子軌。
- 真正的缺口（機械可補，不需要 LLM）：
  - **沒有「試過幾個變體」的計數**，所以做不了 deflated Sharpe（對多重測試打折的 Sharpe）。
  - 主 repo 多支回測用「今天的成分股」＝存活者偏差（`sop_funnel/backtest*.py`、`backtest_entry_state.py`），且多數不扣成本。
  - 基本面不是 point-in-time（QGM、GRP、sop 品質閘）。
  - 本機 v7-backtest checkout 落後 origin 197 個 commit。

---

## 2. 兩個真實研究案例

### 案例 A（基本面／產業）：代理人 AI → 伺服器 CPU 需求 → AMD

資料最完整的真實鏈：

- 想法：`docs/ideas/ai-scissors.html`、`docs/ideas/consumer-agents.html`
- 查核點：`ideas.json` ai-scissors cp7「伺服器 CPU 供不應求」、consumer-agents cp9「伺服器 CPU：代理人的錢流向誰」（refutes_if：x86 供給追上，或工作負載搬到自研 Arm）
- 監測狀態：`docs/ideas/data/research.json` cp7／cp9 皆 supports（9/24、9/25 起）
- DD：`docs/dd/DD_AMD_20260923.html`（v20；H2＝伺服器 CPU 份額續升）
- 供應鏈：`docs/supply-chain/data/server.json` CPU 節點
- 帳本：`decisions.jsonl` 6 筆、`forecasts.jsonl` 12 筆、`kill_registry.json`

**缺口**：沒有伺服器 CPU 的 ID；沒有「CPU 需求」本身的可結算預測；沒有 `facts/AMD/`；查核點與 kill_metrics 沒連線。

### 案例 B（量化）：W52 × 自適應波動率（實盤主系統）

- 規格：v7-backtest `docs/Adaptive_Sigma_Spec.md`、`W52_Adaptive_OOS_Spec.md`（只在 origin/main）
- 帳本：`knowledge/rule_ledger.md` W52 列（含 2026-09-15 修訂）
- 假說：週線收盤 > 52 週均線才持有，曝險＝clip(σ_t / RV20, 1.5)，σ_t＝RV20 近 756 日中位數
- 樣本內：美 Calmar 0.573 對舊版 0.524；台 1.048 對 0.995
- **預註冊樣本外（34 檔沒看過的標的，2026-09-05）：通過率 20.6%；三個 kill 觸發兩個。** 10 月由你複審。

這個案例本身就證明一件事：**你的量化瓶頸不是智力，是樣本與多重測試。** 這兩件事都該交給程式，不該交給任何 LLM。

---

## 3. Atomic tasks 分類

代碼：**A**＝前緣模型、**B**＝地端模型可勝任、**C**＝確定性程式、**D**＝人。

### 3.1 案例 A：代理人 AI → 伺服器 CPU → AMD

| # | 任務 | 分類 | 為什麼 |
|---|---|---|---|
| A01 | 提出想法「代理人會拉高 CPU 需求」 | D | 你的原創判斷 |
| A02 | 把想法拆成可證偽的因果鏈（每任務推論次數 → CPU 時間 → 伺服器數 → TAM → AMD 份額） | A | 要找出哪一環最弱，需要跨領域推理 |
| A03 | 為每一環寫出 supports_if／refutes_if | A | 寫錯就變成永遠證實不了、也推翻不了的套套邏輯 |
| A04 | 找原始來源（KeyBanc「CPU 賣完」、AMD／Intel 法說、Mercury Research 份額） | A | 分辨一手與轉述、找到原始出處，是多步網搜加判斷 |
| A05 | 驗證來源是一手還是轉述 | A | 地端小模型很難分辨「媒體引述分析師」和「公司親口說」 |
| A06 | 從法說逐字稿抽出 CPU 相關段落 | **B** | 範圍明確的抽取 |
| A07 | 從 10-Q／新聞稿抽資料中心營收、季增率 | **B**＋C 驗算 | 抽取可交地端；數字必須跟 Koyfin／EDGAR 對帳 |
| A08 | 抽出的引文逐字存在於原文 | C | 字串比對，零 LLM |
| A09 | 計算 CPU TAM 情境（推論次數 × CPU 秒數 × 單價） | C | 純算術 |
| A10 | 歷史對照：過去的「CPU 賣完」後來怎麼了（2018、2021） | A | 要判斷類比是否成立、哪裡不同 |
| A11 | 替代解釋：CPU 缺貨是因為 Intel 18A 良率，不是需求 | A | **地端最容易漏的一步**：它會順著你的假說找證據 |
| A12 | 反向證據：Arm 自研晶片（Graviton／Axion）吃掉增量 | A | 同上 |
| A13 | 判斷證據是否真的支持因果，而非只是相關 | A | 核心推理 |
| A14 | 每日新聞卡分類到 cp7／cp9 | **B** | 高量、低風險、可抽查 |
| A15 | 新聞卡是否「推翻」keystone 查核點 | A | 推翻 keystone 會觸發整個想法重評，錯判代價高 |
| A16 | 把 kill_metrics 寫成機器可監測的門檻 | A→C | 前緣寫定義，程式執行 |
| A17 | 門檻監測（資料中心季增 <10%） | C | 已有 `kill_watch.json` |
| A18 | 門檻觸發後解讀「為什麼」 | A | 要分辨一次性因素還是趨勢反轉 |
| A19 | 存證據、打標籤、建連線 | **B**／C | 格式化工作 |
| A20 | 語意檢索：「以前哪份報告談過 CPU／GPU 比例」 | **B**（embedding） | 小型 embedding 模型即可 |
| A21 | 決定倉位 | D | 你 |

### 3.2 案例 B：W52 × 自適應波動率

| # | 任務 | 分類 | 為什麼 |
|---|---|---|---|
| B01 | 假說：長趨勢閘門＋波動率目標能改善 Calmar | D | 你的經濟邏輯 |
| B02 | 寫預註冊規格：參數、樣本外定義、kill 門檻 | A＋D | 前緣找漏洞，你拍板 |
| B03 | 審查規格的前視偏差、存活者偏差、樣本期代表性 | **A** | 例：美股樣本內只有一次深熊，這種洞地端很難主動指出 |
| B04 | 抓調整後股價、修 0050 假分割 | C | 程式 |
| B05 | 寫回測程式初稿 | A（Claude Code） | 你已經用 Claude Code；地端寫的程式要花更多時間驗 |
| B06 | 跑回測、算 Calmar／MDD／CAGR | C | 程式 |
| B07 | 自動記錄實驗編號、參數、變動理由 | C | 目前缺，應補 |
| B08 | 計算累計試過的變體數、deflated Sharpe | C | 目前缺，應補 |
| B09 | 樣本外、bootstrap | C | 已有 |
| B10 | 解讀樣本外 20.6% 通過率代表什麼 | A | 要分辨「規則沒用」、「標的不適用」、「樣本太短」 |
| B11 | 提議要不要改規則 | A（只提）＋D（決定） | **任何 LLM 都不准看完結果就自動改參數** |
| B12 | 實盤每日訊號與寄信 | C | 已有 |
| B13 | 批次跑 34 檔、整理結果表 | C | 不需要 LLM |

### 3.3 地端模型的智力不足，會在哪裡真的出事

1. **確認偏誤**（A11、A12）：小模型會順著提問方向找證據，很少主動說「你的假說可能錯在這裡」。
2. **來源階層**（A04、A05）：分不清一手、轉述、二手推測。在你的系統裡，這會直接污染 `facts/`。
3. **數字自信地錯**（A07）：抽對格式、抽錯期別（季對年、GAAP 對 non-GAAP）。靠 C 類對帳可以攔。
4. **方法論盲點**（B03、B10）：不會主動指出「樣本內只有一次深熊」。
5. **長上下文退化**：一份 DD 判斷的證據包動輒幾萬 token；地端 30B 級模型在長上下文後段的注意力明顯下降。

第 1、2、4 點**沒有程式能攔**，所以這些一律前緣。第 3 點可以攔，所以可以交給地端。

---

## 4. Model Router 設計

### 4.1 原則

不是看 token 數，而是依序問六個問題，第一個「是」就定案：

```
1. 能用程式確定算出來嗎？（公式、門檻、查詢、格式轉換）         → CODE
2. 會直接改變部位或資金嗎？                                      → HUMAN
3. 錯了會污染判斷層，而且程式攔不到嗎？                          → FRONTIER
   （因果判斷、反向證據、來源真偽、方法論審查、推翻 keystone）
4. 是全新問題、沒有前例模板嗎？                                  → FRONTIER
5. 輸出能被程式逐條驗證嗎？（引文逐字比對、數字對帳、分類抽查）  → LOCAL（＋CODE 驗證）
6. 其他                                                          → FRONTIER
```

第 5 題是地端能不能用的**唯一入口**：地端的輸出一定要有程式能驗。驗不了，就不准進 `facts/`。

### 4.2 評分欄位（給 classifier 用）

| 欄位 | 值 | 意義 |
|---|---|---|
| `deterministic` | bool | 有公式可算 |
| `capital_impact` | none／indirect／direct | 是否直接動部位 |
| `verifiable_by_code` | bool | 輸出能被程式驗證 |
| `judgment_layer` | bool | 是否進入 DD 判斷或 critic |
| `novelty` | template／variant／novel | 有無前例 |
| `volume_per_day` | int | 高量才值得在地端 |
| `context_tokens` | int | >32K 時地端品質打折 |

### 4.3 實作形態

- 第一版就是一張 YAML 規則表＋一支 Python 函式，**分類本身不用 LLM**（任務類型是有限集合）。
- 只有「把研究問題拆成任務」這一步要前緣模型；拆完之後，每個任務的路由由規則表決定。

---

## 5. Research Object：擴充，不重寫

不新增真相檔。做一個**衍生索引** `knowledge/research_objects.jsonl`（由 `build_knowledge.py` 從既有檔重建，gitignored），把散在各處的東西串起來：

```json
{
  "research_id": "agentic-cpu",
  "title": "代理人 AI 拉高伺服器 CPU 需求",
  "type": "industry_thesis",
  "status": "MONITORING",
  "tickers": ["AMD", "INTC", "ARM"],
  "links": {
    "ideas": ["ai-scissors#cp7", "consumer-agents#cp9"],
    "dd": ["docs/dd/DD_AMD_20260923.html#H2"],
    "supply_chain": ["server.json#cpu"],
    "kill_metrics": ["dd:DD_AMD_20260923:0"],
    "forecasts": [],
    "experiments": []
  },
  "status_history": [{"date": "2026-09-24", "from": "RESEARCHING", "to": "MONITORING", "by": "human"}]
}
```

`status` 用你列的七個狀態。**只有人能改狀態**；程式只能提議。

**證據欄位補強**（additive，舊檔不動）：`facts/{T}/axes` 的 finding 新增 `url`、`retrieved_at`、`excerpt`（原文），把 `claim` 定義為解讀。對應 `validate_evidence.py` 放寬為選填，新 run 必填。

---

## 6. 回測：補兩個機械欄位就好

不蓋新框架。在 v7-backtest 加一個只能追加的 `experiments.jsonl`：

```json
{"exp_id": "W52-017", "parent": "W52-016", "prereg_ref": "docs/W52_Adaptive_OOS_Spec.md",
 "hypothesis": "...", "params": {...}, "changed": {"cap": [1.0, 1.5]}, "reason": "...",
 "who_proposed": "human|frontier", "is": {...}, "oos": {...}, "ts": "..."}
```

加上一支程式：從 `experiments.jsonl` 算「同一假說家族試過幾次」→ deflated Sharpe。這兩件事就能擋住「AI 一直改到 Sharpe 最高」。

---

## 7. 前緣與地端的合作方式

```
你（PM）── 提想法、拍板狀態、決定部位
  │
前緣（Claude opus／sonnet）── 拆假說、找一手來源、反向證據、因果判斷、方法論審查、冷讀
  │        ▲
  │        │ 只讀「程式驗過」的證據包
  ▼        │
程式（Python）── 引文逐字比對、數字對帳、算指標、回測、門檻監測、實驗記帳
  ▲
  │ 抽取結果先過程式驗證
地端（Mac）── PDF／逐字稿抽取、新聞卡分類、embedding 語意檢索、批次格式化
```

一句話：**地端是資料實習生，前緣是資深分析師，程式是稽核，你是 PM。** 實習生的產出不經稽核，不准送到分析師桌上。

---

## 8. 對現有系統的建議優先序

1. ~~補證據來源欄位~~（2026-09-26 完成）：採證 prompt 要求 url／excerpt／excerpt_from，`facts_store.put_axis` 逐條補 retrieved_at，`dd_facts` 帶進 findings_digest，`validate_evidence` 只做形狀檢查不擋舊檔。
2. **地端基準測試**（見 `LOCAL_MODEL_EVALUATION.md`，1–2 天）：用現有 `facts/MU|TSM|TXN` 的 144 條 findings 當標準答案，在手上的 M5 16GB 先跑。
3. **Research Task Router 原型**（1 天）：規則表＋拆題，只輸出任務清單，不執行。
4. ~~experiments.jsonl＋deflated Sharpe~~（2026-09-26 完成）：v7-backtest `src/experiment_ledger.py`＋`experiments/ledger.jsonl`，已開立 W52-ADAPTIVE 家族。
5. 基準測試過關後，才考慮把 `intel/classify.py` 切到地端。
