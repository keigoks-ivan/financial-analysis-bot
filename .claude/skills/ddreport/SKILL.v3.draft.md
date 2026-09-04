---
name: ddreport
version: v3.1-draft
released: 2026-09-04
description: "v16.2 草案：thin orchestrator，把 stock-analyst v16.2 的四段鏈（sonnet 收資料＋0e 逐字稿摘要 → Fable 只寫判斷 → sonnet 只寫散文，機械閘全過即上站；流程內無 critic、無修補、無 re-gate）（設計稿 notes/site-internal/dd/_v16_design_spec_20260903.md §13-§16）固化成一鍵。與現行 v2.3（單一巨石 writer→critic→patch）並存——本鏈由 `ddreport --v16 {ticker}` 觸發，預設仍走 v2.3。orchestrator（opus）全程只 spawn、傳檔名、讀 validator 輸出、決定是否 re-gate、commit，**不讀任何報告內容或 evidence/judgment JSON 進自己的 context**。"
---

# DD Report Pipeline v3.1（draft，v16.2 三步制 orchestrator）

```
1 git hygiene
  → 2 Stage 0（sonnet fan-out；dd_numbers_extra 先行）＋0e 逐字稿摘要（sonnet）→ validate_evidence --strict
  → 3 判斷（Fable，只寫 judgment.json／scenario.json）：dd_scenario/dd_decision/validate_judgment →自查①-⑦
  → 4 散文（sonnet，只讀 judgment.json）：gen_dd_tables → dd_prose_budget → prose/{sid}.html 逐段一次 Write
      → render_dd --assemble → validate_prose/dd_sections bytes/leaks/qc.py/validate_dd_meta/verify_dd_math
      → 自查⑧＋QC-54
  → 5 INDEX.md 登錄
  → 6 update_dd_index.py → size gate → commit/push
  → 7 來源檔存 notes/site-internal/dd/_src/{T}_{D}/
  → 8（已含在 6-7，列出僅供對照）commit
（流程外，前三份）事後冷讀抽查 → notes/site-internal/dd/_audit_{T}_{D}.md，只計數不修補
```

**判斷機器零變動**：QC-1～QC-54 門檻、決策矩陣、dd-meta schema 全部凍結（見設計稿 §1）。本鏈只是把散文規則搬進 validator／腳本／JSON 欄位。**與 v15.2 並存**：v16.2 三步鏈以 `ddreport --v16 {ticker}` 觸發，未帶旗標一律走現行 v2.3（`.claude/skills/ddreport/SKILL.md`）。WP4 三份試點（皆 Fable 判斷 agent；上站後各跑一次 opus 事後抽查）通過退場訊號（設計稿 §13、§16：①覆蓋缺軸 0 ②前三份上站後事後冷讀抽查判斷級 🔴 合計為 0 ③機械閘全過、裁決與前份同向或有歸因 ④Fable 每份 cache_read ≤3M、sonnet 散文 ≤4M、每份合計 ≤15M，去重尺）後才切預設；抽查出現 1 例判斷級 🔴 即把判斷層驗收放回流程內，本檔停留草案不轉正。

**旗標**：`--judgment-model {fable|sonnet|opus}`（**預設 `fable`**，v16.1 的 `--writer-model` 更名——語意收斂為「只管判斷層模型」，散文 agent 固定 sonnet 不受此旗標影響）。`--dry-run`＝組裝輸出到 `.dd_build/DD_{T}_{D}.v16dryrun.html`（不寫 `docs/dd/`）、**不跑 `update_dd_index.py`、不寫 INDEX.md、不 commit、不 push**，其餘鏈（含機械閘與兩個 agent 的自查）照跑；用於流程試點與成本回量。`--delta`＝同檔重跑走差異模式（`scripts/dd_delta.py`，**草案中，模板待補**——本輪不納入，見「邊界」段）。

## Steps

1. **解析 ticker + git hygiene**（沿用 v2.3 步驟 1）：模糊 ticker 先問用戶；開始前 `git log --oneline -5` + `git status` 排除並行 session 的 orphan 檔。決策意圖（要不要加倉/新進/退出）先按 repo CLAUDE.md「Decision-time critic」規則 spawn `industry-thesis-critic`，純研究不觸發。同檔重跑（`docs/dd/DD_{TICKER}_*.html` 已存在）提示可用 `--delta`（模板待補，本輪先走全套）。

2. **Stage 0：證據包＋0e 逐字稿摘要（無判斷 agent 介入）**。orchestrator 依序：
   - **0d 零 LLM**：`python3 scripts/dd_prior.py {TICKER} --date {DATE} --out .dd_build/parts/prior.json`（前份 DD 三區塊＋q.py 帳本＋canonical ID 事實＋逐字稿路徑清單，一次到位；輸出含 `transcripts.selected.recent_four_quarters[]`／`transcripts.selected.high_signal_optional[]`）。
   - `python3 scripts/dd_evidence.py init {TICKER} {DATE} --archetype "{archetype_hint}" [--segments "..."]` 建 `.dd_build/{T}_{D}.evidence.json` 骨架；`dd_evidence.py merge` 併入 0d 片段。
   - **0a 數字包**：先跑零 LLM 的 `python3 scripts/dd_numbers_extra.py {TICKER} {DATE} --peers "{PEER1,PEER2,...}" --out .dd_build/evidence_parts/numbers_extra.json`（**`--peers` 規則**：有前份 DD → 沿用其 `peer_valuation` 名單；無前份 DD → orchestrator 依產業指定 3-5 檔，且**必須與交給採集 agent 的 `peer_valuation` 同一份名單**）（v16.2 起產扁平三欄 `numbers.price_at_dd`／`numbers.price_as_of`／`numbers.earnings_recency`＋五個結構化欄位 `latest_quarter_kpis`／`valuation_history`／`peer_financials`／`momentum_26w`〔含 `rsi14_usable`〕／`edgar_concentrations`／`consensus_revision`〔含 `stale` 旗標〕），`merge` 進 evidence.json；**再** spawn sonnet 採集 agent 沿用 `references/data-collection.md` 模板（含財報時效閘＋v16.2 新增的財報日「唯一來源＝公司 IR 新聞稿」規則）補齊 `latest_quarter_kpis.items[]` 缺項與其餘數字欄，**採集端只能在既有扁平鍵原地補值，不得改鍵名或另包一層**（PANW 教訓）。
   - **0b 覆蓋矩陣 fan-out**：依 `references/evidence-pack.md` §1-§2——`dd_evidence.py axes --archetype ... --json` 展開軸清單（約 14-17 軸），每 3-5 軸一個 sonnet 子 agent（模板見 `references/v16/agent-prompts.md` (a)），每軸 ≤3 輪搜尋；orchestrator 逐一 `dd_evidence.py merge` 併回，**不讀子 agent 回傳內容**。0c（QC-19 事件五組）併入 0b 的「事件」軸，同一批派工；**負責 `major_events` 軸的那批子 agent 需同時交付頂層 `events` 五組**（見 `evidence-pack.md` §2 v16.2 新增段），不得只填 `coverage.major_events`。
   - **0e 逐字稿摘要（新，sonnet）**：spawn (a2) 子 agent（模板見 `agent-prompts.md` (a2)），輸入＝`transcripts.selected.recent_four_quarters[]` 去掉最新一季的三篇＋`transcripts.selected.high_signal_optional[]`（若有），輸出 `.dd_build/{T}_{D}.transcript_digest.json`（每篇 ≥12 條逐字 quote＋qa_flags）。跑 `python3 scripts/validate_digest.py .dd_build/{T}_{D}.transcript_digest.json --transcripts {逐字稿所在目錄}`，FAIL 則回去原文重寫（≤2 輪）。PASS 後 `dd_evidence.py merge` 把 `{"transcripts":{"digest_path":"..."}}` 併入 evidence.json。**最新一季全文不進本步驟**，留給判斷 agent 親讀。0e 與 0a／0b 可平行跑。
   - **Koyfin 增量下載**：spawn 一個獨立 sonnet 子任務（沿 v15.2.3 步驟 0：`koyfin_downloader.py --tickers {T}` → `transcripts_for_dd.py {T}`），輸出必讀/可略讀逐字稿路徑清單寫回 evidence.json 的 `transcripts` 區塊；session 過期只標記不阻塞。此步驟須先於 0e，0e 依賴其輸出的路徑清單。
   - **開寫前置閘**：`python3 scripts/validate_evidence.py .dd_build/{T}_{D}.evidence.json --strict --report`。**FAIL 就回補資料**（對缺軸／不合格軸重 spawn 該子任務，缺 `transcripts.digest_path` 就重跑 0e，≤2 次重試），**不得帶缺口開寫**——Stage 0 是唯一的資料把關點，缺口帶進下一段就沒有 critic 會攔。`--strict` PASS 才進判斷 agent。

3. **判斷 agent：只寫 judgment.json／scenario.json**（單一 agent、單一 context，`--judgment-model fable|sonnet|opus`，**預設 `fable`**）：
   - spawn 模板見 `references/v16/agent-prompts.md` (b1)。輸入＝`evidence.json` 路徑＋`transcripts.selected.recent_four_quarters[]` 中**最新一季**全文（親讀，不摘錄）＋`transcript_digest.json`（其餘三季摘要，引用時標「來源：摘要」）＋`references/v16/judgment-rules.md`＋archetype 對應 reference（同 v15.2 條件載入路由表）。**不讀** `render-rules.md`、不產表、不寫 prose。
   - **判斷物**：`.dd_build/{T}_{D}.judgment.json`＋`.dd_build/{T}_{D}.scenario.json`，各一次 Write。判斷 agent 自己一次複合 Bash 跑：`dd_scenario.py .dd_build/{T}_{D}.scenario.json --html .dd_build/{T}_{D}.tables/e11.html --meta .dd_build/{T}_{D}.scenario_meta.json` → `dd_decision.py run .dd_build/{T}_{D}.judgment.json --html .dd_build/{T}_{D}.tables/audit.html --json .dd_build/{T}_{D}.judgment.json`（欄位契約見 `scripts/dd_schema/decision_inputs.md`；`run` 只覆寫機械欄，不清空手填欄）→ `validate_judgment.py ... --report --evidence .dd_build/{T}_{D}.evidence.json`。任一 FAIL → **只准改欄位**重跑這三支，≤3 輪。
   - **交稿前自查①-⑦**（取代原獨立 critic 的判斷層部分）：QC-41 四軸（競爭惡化／供需 durability／其他結構變數／priced-in）＋覆蓋面掃描（缺軸即 🔴）＋量化模組完整性抽查＋數字新鮮度，逐條 🟢/🟡/🔴 作答，🔴 先改該欄位再交稿；自查表為回報必要欄位，缺表視為未交稿。**判斷 agent 到此結束**，不接著寫散文。
   - **禁**：WebSearch/WebFetch（證據不足在該軸 `note` 標「證據包未涵蓋」，不得自搜）、Read 任何 `docs/dd/`、重讀自己寫過的產物、寫 `prose/` 或跑 `gen_dd_tables.py`／`render_dd.py`。

4. **散文 agent：只讀 judgment.json 鋪陳**（另 spawn，sonnet，固定，不受 `--judgment-model` 影響）：
   - spawn 模板見 `references/v16/agent-prompts.md` (b2)。輸入＝`judgment.json`（含 `reasoning` 段，承重數字唯一來源）＋`references/v16/render-rules.md`。**不讀 evidence.json 全文**——`validate_prose.py` 以 judgment 為主要比對集合。
   - **產表與算預算**：`gen_dd_tables.py {JUDGMENT} --out .dd_build/{T}_{D}.tables --scenario-html .dd_build/{T}_{D}.tables/e11.html --scenario-meta .dd_build/{T}_{D}.scenario_meta.json`（dashboard／E2／E3／E5-E10／E11／E12／dd-meta／appA 表；audit 表視 `decision_out.audit_rows` 非空）→ `dd_prose_budget.py {JUDGMENT} --tables .dd_build/{T}_{D}.tables` 得各段散文目標 bytes（表格計入分子）→ 依表逐段**一次 `Write`** `.dd_build/{T}_{D}.prose/{sid}.html`（**禁 `Edit`**，render-rules §0 一次寫條款）。
   - **組裝與六支閘**：`render_dd.py --assemble .dd_build/{T}_{D}.prose --tables .dd_build/{T}_{D}.tables --judgment {JUDGMENT} -o {OUT_HTML}` → `validate_prose.py`（正文數字 ⊆ 判斷物數字集合）／`dd_sections.py bytes`／`dd_sections.py leaks`／`qc.py`／`validate_dd_meta.py --report`／`verify_dd_math.py`（HTML 版）。`{OUT_HTML}`＝`--dry-run` 時 `.dd_build/DD_{T}_{D}.v16dryrun.html`，否則 `docs/dd/DD_{T}_{D}.html`。超標或命中**只重寫該段 prose 檔**（整檔 Write）、重新組裝、重跑；每段最多重寫一次，不動 judgment.json。
   - **交稿前自查⑧＋QC-54**（取代原獨立 critic 的呈現層部分）：散文一致性（有沒有與 judgment.json 矛盾／出現判斷物沒有的數字）＋白話開場，逐條 🟢/🟡/🔴 作答，🔴 先重寫該段一次再交稿；自查表為回報必要欄位。
   - **禁**：WebSearch/WebFetch、Read 任何 `docs/dd/`、重讀自己寫過的 prose/tables 檔、改 `judgment.json` 任何欄位。

5. **INDEX.md 登錄**（`docs/dd/INDEX.md`，明列，取代原「沿用 v2.3」的含糊帶過——**研究頁只收 INDEX.md 有的 DD**，漏此步等於報告上站但不進站內導覽）：照既有列格式（`| 日期 | Ticker | Schema | 裁決 | 陷阱定性 | R:R (60/200/104w) | 檔案 | 備註 |`，見既有 `docs/dd/INDEX.md` 逐行範例）append 一行，欄位取自最終 HTML 的 dd-meta：

   | 欄位 | 取值 |
   |---|---|
   | 日期 | `{DATE}`（YYYY-MM-DD） |
   | Ticker | `{TICKER}` |
   | Schema | dd-meta `schema`（現行 `v15.0`） |
   | 裁決 | dd-meta `dca_verdict`＋`dca_role`＋`rearm_trigger`（同既有格式「進場｜衛星·xxx」／「觀望｜追蹤·xxx」） |
   | 陷阱定性 | dd-meta `trap_label`（🟢/🟡/🔴＋一句定性） |
   | 第 6 欄 | dd-meta `moat_grade`＋`moat_trend`／`val_light`／`trap`（同既有 `B↑/🔴/🟡` 格式，非真的 R:R——欄名沿用歷史命名，語意見 INDEX.md 頂部欄位說明） |
   | 檔案 | `DD_{TICKER}_{DATE}.html` |
   | 備註 | 一句摘要（3-5 個決策相關數字／變化，含「v16.2 三步制」字樣供試點回溯辨識） |

   `--dry-run` 時跳過本步驟。

6. **同步／size gate／commit**（沿用 v2.3 步驟 4.5-7）：`python scripts/update_dd_index.py`（同步 research 頁＋dd-screener＋picks）→ size-budget gate（`dd_sections.py bytes`，70KB 下界／75-105KB 目標／115KB 上界警告）→ `docs/dd/DD_*`、`docs/dd/INDEX.md`、`docs/research/_body.html`、`docs/dd-screener/latest.json`、`docs/picks/candidates.json` 併入同一 commit → push main。commit 訊息附註 `[v16.2-draft]` 供試點回溯量測。**`--dry-run` 時整個步驟 5-6 跳過**（不寫 `docs/dd/`、不寫 INDEX.md、不跑 `update_dd_index.py`、不 commit／push），只回報六支閘輸出、兩份自查表與分模型 token 用量。

7. **來源檔存查**（新，明列）：把本次產物存進 `notes/site-internal/dd/_src/{T}_{D}/`（供下一輪 `--delta` 差異模式當基底，也供事後抽查與人工複查）：
   - `{T}_{D}.judgment.json`
   - `{T}_{D}.scenario.json`
   - `{T}_{D}.scenario_meta.json`
   - `{T}_{D}.evidence.json`
   - `{T}_{D}.transcript_digest.json`（v16.2 新增）
   - `prose/`（整個目錄）

   這些檔案本身不進 `docs/` 的 commit（步驟 6 已列的四類才進），另外 add 進同一個或緊接的 commit。

8. **分模型計量**（新，`python3 scripts/dd_token_report.py {SESSION_ID}` — 你要新寫的腳本，參考
   `~/.claude/projects/-Users-ivanchang-financial-analysis-bot/{SESSION_ID}/subagents/agent-*.meta.json`
   的 `model` 欄位）：讀本次 session 的 `subagents/*.jsonl`，按每個 sub-agent 的 `model` 分三欄
   （fable／opus／sonnet）加總 cache_read／cache_creation／output，可用 `--filter {TICKER}` 只挑本次
   相關的 sub-agent。回報格式見 `SKILL.v16.draft.md` §五「新增（v16.2）」段；用於前三份試點回填成本
   模型與比對退場訊號④（Fable 每份 cache_read ≤3M、sonnet 散文 ≤4M、每份合計 ≤15M，去重尺；`dd_token_report.py` 依 message.id 去重才是正確尺度，舊尺重複加總同一則訊息高估 2–3 倍）。

   **（流程外）事後抽查**：前三份上站後，orchestrator 另 spawn 一次冷讀（模型與判斷 agent 不同；Fable
   判斷 agent → opus），輸入含 `judgment.json`＋`evidence.json`＋`transcript_digest.json`（SNOW 教訓：
   冷讀者缺逐字稿/摘要會誤判 writer 親讀得到的正確判斷為無據），只計判斷級 🔴 數、不修補、不重跑腳本，
   輸出存 `notes/site-internal/dd/_audit_{T}_{D}.md`。抽查只餵設計稿 §13、§16 退場訊號，永不阻斷發布。

## 邊界

- `--dry-run`（組裝到 `.dd_build/`、不上站、不 commit）供流程試點與 A/B 判斷層模型用；跑完仍要回報六支閘輸出、兩份自查表與分模型 token 用量，才算一份有效試點。
- 不新增判斷語意、不動決策矩陣／dd-meta schema／QC-41 checklist 條文本身（只改由誰執行——v16.2 由判斷 agent 自查①-⑦、散文 agent 自查⑧＋QC-54，見 `references/v16/agent-prompts.md`）。
- `.dd_build/` 下所有中間檔案皆非最終產物，不進 commit（只有步驟 6 列的四類進 commit；步驟 7 的來源檔存進 `notes/site-internal/dd/_src/`，非 `docs/`；事後抽查的 `_audit_*.md` 於抽查完成後另行 commit）。
- **同檔重跑（delta）本輪不納入**：`scripts/dd_delta.py` 是另一個 agent 正在寫的差異模式腳本，本檔不碰、不搶著設計其模板——同檔重跑一律走本檔全套鏈（步驟 1-8），`--delta` 旗標與其模板留給下一輪補上。
- 本檔為草案，**不覆蓋、不取代** `.claude/skills/ddreport/SKILL.md`（v2.3 仍是預設鏈）；WP4 驗收通過前，任何非明確帶 `--v16` 的請求一律照舊走 v2.3。
