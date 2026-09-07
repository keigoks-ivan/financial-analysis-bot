# 委託書：DD 管線大改（給 Codex）

> 用法：在 Codex 開 `~/financial-analysis-bot` 專案，第一句「先讀 AGENTS.md 最後一節，再讀本檔全文」。本檔是唯一任務來源；有衝突以本檔為準，仍不確定就停下來問，不要猜。
> 日期：2026-09-06。委託人：持有人。管線現況見 `notes/site-internal/dd/_dd_pipeline_redesign_spec_20260905.md`（v17 設計稿）與 `git log --oneline -20 -- scripts/ddreport.py`。

## 一、為什麼改（目標，可量測）

一份快速版 DD 現在約 20 到 40 分鐘、$18 到 21（列表價）。持有人的用法有兩種：批次補到期隊列（睡前排、早上讀）與「我現在想知道這檔」。批次那種已有 `ddreport.py batch`；即時那種已有 `scripts/dd_flash.py`（5 分、$2，無閘）。本次大改的目標是**正式快速版本身**：

| 指標 | 現況 | 目標 |
|---|---|---|
| 一檔快速版牆鐘時間（首次跑） | 20 到 40 分 | ≤ 20 分 |
| 一檔快速版牆鐘時間（90 天內重跑） | 同上 | ≤ 12 分 |
| 一檔列表價 | $18 到 21 | ≤ $12 |
| 裁決一致性（回溯考卷，見第五節） | — | 17 份全同向 |

時間花在哪（TXN 2026-09-06 實跑）：證據段 12 到 19 分（13 到 17 個 sonnet agent 分波跑、等最慢的、重試）、判斷段 13 分（Fable 寫 25K token 判斷加 20K 思考，**這段是生成速度的物理下限，不在本次範圍**）、閘 5 分、finish 3 到 4 分（每檔重跑全站同步）。

## 二、絕對不能動的（動了整份工作作廢）

1. **判斷規則的語意**：`.claude/skills/stock-analyst/references/v16/judgment-rules.md`、`decision-layer.md`、`timing-appendix.md`、`roic-durability.md`、`judgment-playbook.md`、`archetype-gatesets.md`、`cyclical-lens.md`。一字不改。要改判斷規則是另一種委託，要走 `knowledge/rule_ledger.md` 的 kill condition 程序。
2. **決策矩陣**：`scripts/dd_decision.py` 與 `scripts/dd_schema/decision_inputs.md`。裁決必須仍由它機械算出。
3. **判斷物 schema**：`scripts/dd_schema/judgment.schema.json` 的欄位名、型別、enum、required。可以加選填欄，不可刪、不可改名。理由：驗證器、閘、快速版渲染、下游聚合全部讀它。
4. **dd-meta 契約**：`docs/dd/brief/BRIEF_*.html` 與 `docs/dd/DD_*.html` 內嵌的 dd-meta JSON 欄位（`.claude/skills/stock-analyst/references/dd-meta-schema.md`、`scripts/validate_dd_meta.py`）。下游讀者：`scripts/update_dd_index.py`、`build_dd_screener.py`、`build_picks.py`、`build_ticker_hubs.py`、`engine/`、`build_quality_entry.py`、`build_catalyst_*.py`、`aggregate_dca_stats.py` 等十幾支。
5. **模型路由**：證據 sonnet、判斷 Fable、閘 opus、渲染零 LLM。這是 2026-09-06 拍板（有 opus A/B 數據），不在本次範圍。
6. **跨模型閘不可拿掉、不可改成同模型**。
7. **不得新增任何「收斂面」**：不新增名單、不讓任何新產物進 picks／GRP／三軌／dd-screener／cockpit。
8. `.claude/skills/` 目錄任何檔不動（含 SKILL.md）；改了 CLI 介面要回報，由持有人另行更新 skill 說明。

## 三、隨你改的（機械層，這是大改的空間）

以下每一項都是「換做法、不換語意」。優先序由上到下，做一項驗一項、commit 一項（由持有人 commit，你只交 diff）。

### 3.1 證據段增量化（最大的一刀）
到期隊列全是重跑；前一份的證據包還在 `notes/site-internal/dd/_src/{T}_{D}/`（`*.evidence.json`、`parts/`、`*.transcript_digest.json`）。設計一個「證據沿用政策」：
- 逐軸判斷是否過期：數字類（numbers／events／latest_quarter_kpis／consensus）每次重抓；結構類（護城河、監管、地緣、供應鏈、替代技術、通路、資本市場定價）在 N 天內（預設 30，CLI 可調）沿用舊 findings，並在 finding 上加 `reused_from` 與 `age_days`；最新一季逐字稿有新檔才重跑 digest，其餘季沿用。
- Stage 0 只派「過期或缺」的軸的 agent。判斷 bundle 標明哪些軸是沿用的，讓 Fable 與閘看得到年齡。
- 驗收：對 `_src` 內任一檔用 `--reuse-days 3650` 跑 plan，應 0 個證據 agent；`--reuse-days 0` 應與現在相同數量。

### 3.2 平行度與批次結構
- 現在 `STAGE0_MAX_PARALLEL` 預設 6、每批 2 軸。研究「一軸一 agent、平行 8 到 10、輪數上限依軸型別」是否更快且不更貴；用 `_src` 的 manifest（agent_usage）估。
- 事件與 numbers 的 agent 最慢（13 到 15 輪），看能否把 numbers 改成全零 LLM（`dd_numbers_extra.py` 已做一半）。

### 3.3 finish 批次化
- `_do_finish` 每檔跑 `update_dd_index.py`（含 screener 重建、yfinance）。改成：單檔 finish 只做 commit＋push 該檔與 brief；研究頁與 screener 同步改由 `batch` 結尾做一次，或加 `--sync-later`。單跑 `run` 仍預設同步（持有人習慣），但要能關。

### 3.4 閘與修補
- 閘現在 2 到 7 輪；看 gate bundle 能否只帶 judgment＋evidence 摘要而不帶全部逐字稿。
- 🔴 修補後**不 re-gate**（設計稿 §3.4 已定：除非裁決翻面），確認程式真的沒有多跑一次閘。

### 3.5 觀測與帳
- 每段印開始／結束時間、牆鐘、cache_read／output／cost；`token.json` 與 batch 摘要含各段時間。持有人要一眼看到「錢與時間花在哪」。

### 3.6（選配，先問再做）判斷物分層
把 judgment.json 分成「核心裁決物」（決策矩陣輸入、情境樹、plain、觸發器、矛盾裁決；約 8K token）與「延伸物」（其餘敘述欄）兩次呼叫，判斷段從 13 分降到 5 到 6 分。**這會動到判斷 agent 的 prompt 與 schema 的 required 集合，屬第二節第 3 條的邊界**，要先寫設計（一頁）給持有人核可才做。

## 四、工作方式

- Python 3.9 相容、中文全形標點、每處改動附「2026-09-XX：為什麼」。
- **改程式期間不 spawn 模型**（`claude -p`）、不跑 `ddreport.py run／finish／batch`（會上站）。用 `--dry-run`、`--replay-from`（`scripts/tests/fake_claude.py` 有假的 claude）與單元測試驗證。持有人另外明說「跑 X 的 DD」時，照 AGENTS.md「跑 DD 的規矩」執行，且只在 `scripts/` 沒有你未交付的改動時跑。
- 不 commit、不 push、不 `git add -A`、不 stash。這個 working tree 有別的 session 在動，`git status` 裡大量修改檔不是你的。
- 大改拆成可獨立 review 的小步：每步一份 diff、一段說明、驗證輸出。一次交一整包 3,000 行的 diff 會被退回。
- 卡住就停下來問，不要繞路硬做。

## 五、驗收（全部通過才算完成）

1. **回溯考卷**：`notes/site-internal/dd/_src/` 現有 17 份（AVGO／BE／BWXT／CAMT／CDNS／CIEN／CRDO／ETN／FIX／FN／GRAB／HPE／PANW／SNOW dryrun／STRL／TXN／WDAY）。用 `--replay-from` 走新管線，`decision_out.verdict`／`role`／`row_hit` 與歸檔的 judgment.json **全部相同**；情境數字允許差異（那是判斷變異，不是管線變異），但 `dd_scenario.py` 驗證全過。
2. `python3 -m pytest scripts/tests -q` 全過（現 112），新功能有新測試。
3. `python3 scripts/qc.py` 對所有改到的檔 0 errors。
4. 用 `_src` 的 manifest 估算新舊時間與 cost，交一張表對照第一節目標；估不到的欄寫「需實跑」。
5. 一份「改了什麼、沒改什麼、哪裡不確定」的說明，不超過兩頁。

實跑（真的 spawn 模型）由持有人在 Claude Code 這邊做，不在你的範圍。
