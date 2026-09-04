---
name: ddreport
version: v3.1-draft
released: 2026-09-04
description: "v16.1 草案：thin orchestrator，把 stock-analyst v16.1 的兩步鏈（sonnet 收資料 → Fable 一次寫完，機械閘全過即上站；流程內無 critic、無修補、無 re-gate）（設計稿 notes/site-internal/dd/_v16_design_spec_20260903.md）固化成一鍵。與現行 v2.3（單一巨石 writer→critic→patch）並存——本鏈由 `ddreport --v16 {ticker}` 觸發，預設仍走 v2.3。orchestrator（opus）全程只 spawn、傳檔名、讀 validator 輸出、決定是否 re-gate、commit，**不讀任何報告內容或 evidence/judgment JSON 進自己的 context**。"
---

# DD Report Pipeline v3.1（draft，v16.1 兩步制 orchestrator）

```
git hygiene → Stage0 證據包（sonnet fan-out；dd_numbers_extra 先行）→ validate_evidence --strict
  → Writer（Fable，單一 context）：judgment/scenario → dd_scenario/dd_decision/validate_judgment
      → gen_dd_tables → dd_prose_budget → prose/{sid}.html 逐段一次 Write
      → render_dd --assemble → validate_prose/dd_sections bytes/leaks/qc.py/validate_dd_meta/verify_dd_math
      → 交稿前自查表 ①-⑧
  → INDEX/update_dd_index.py → size gate → commit/push
（流程外，前三份）事後冷讀抽查 → notes/site-internal/dd/_audit_{T}_{D}.md，只計數不修補
```


**判斷機器零變動**：QC-1～QC-54 門檻、決策矩陣、dd-meta schema 全部凍結（見設計稿 §1）。本鏈只是把散文規則搬進 validator／腳本／JSON 欄位。**與 v15.2 並存**：v16.1 兩步鏈以 `ddreport --v16 {ticker}` 觸發，未帶旗標一律走現行 v2.3（`.claude/skills/ddreport/SKILL.md`）。WP4 三份試點（皆 Fable writer；上站後各跑一次 opus 事後抽查）通過退場訊號（設計稿 §13：①覆蓋缺軸 0 ②前三份上站後事後冷讀抽查判斷級 🔴 合計為 0 ③每份成本 ≤ v15.2 同檔 SNOW 88M／DELL 138M）後才切預設；抽查出現 1 例判斷級 🔴 即把 Fable 驗收放回流程內，本檔停留草案不轉正。

**旗標**：`--writer-model {fable|sonnet|opus}`（**預設 `fable`**）。`--dry-run`＝組裝輸出到 `.dd_build/DD_{T}_{D}.v16dryrun.html`（不寫 `docs/dd/`）、**不跑 `update_dd_index.py`、不 commit、不 push**，其餘鏈（含 critic／patch／六支閘）照跑；用於流程試點與成本回量。

## Steps

1. **解析 ticker + git hygiene**（沿用 v2.3 步驟 1）：模糊 ticker 先問用戶；開始前 `git log --oneline -5` + `git status` 排除並行 session 的 orphan 檔。決策意圖（要不要加倉/新進/退出）先按 repo CLAUDE.md「Decision-time critic」規則 spawn `industry-thesis-critic`，純研究不觸發。

2. **Stage 0：證據包（writer-free）**。orchestrator 依序：
   - **0d 零 LLM**：`python3 scripts/dd_prior.py {TICKER} --date {DATE} --out .dd_build/parts/prior.json`（前份 DD 三區塊＋q.py 帳本＋canonical ID 事實＋逐字稿路徑清單，一次到位）。
   - `python3 scripts/dd_evidence.py init {TICKER} {DATE} --archetype "{archetype_hint}" [--segments "..."]` 建 `.dd_build/{T}_{D}.evidence.json` 骨架；`dd_evidence.py merge` 併入 0d 片段。
   - **0a 數字包**：先跑零 LLM 的 `python3 scripts/dd_numbers_extra.py {TICKER} {DATE} --peers "{PEER1,PEER2,...}" --out .dd_build/evidence_parts/numbers_extra.json`（**`--peers` 規則**：有前份 DD → 沿用其 `peer_valuation` 名單；無前份 DD → orchestrator 依產業指定 3-5 檔，且**必須與交給採集 agent 的 `peer_valuation` 同一份名單**，兩處不得各挑各的）（產 `numbers.latest_quarter_kpis`／`valuation_history`／`peer_financials`／`momentum_26w`〔含 `rsi14_usable`〕／`edgar_concentrations`／`consensus_revision`〔含 `stale` 旗標〕），`merge` 進 evidence.json；**再** spawn sonnet 採集 agent 沿用 `references/data-collection.md` 模板（含財報時效閘）補齊 `latest_quarter_kpis.items[]` 缺項與其餘數字欄（採集端鐵律：同一指標只准引最新一季官方值，每項帶 `as_of`＋`source`），輸出片段 `merge` 進 evidence.json。
   - **0b 覆蓋矩陣 fan-out**：依 `references/evidence-pack.md` §1-§2——`dd_evidence.py axes --archetype ... --json` 展開軸清單（約 14-17 軸），每 3-5 軸一個 sonnet 子 agent（模板見 `references/v16/agent-prompts.md` (a)），每軸 ≤3 輪搜尋；orchestrator 逐一 `dd_evidence.py merge` 併回，**不讀子 agent 回傳內容**。0c（QC-19 事件五組）併入 0b 的「事件」軸，同一批派工。
   - **Koyfin 增量下載**：spawn 一個獨立 sonnet 子任務（沿 v15.2.3 步驟 0：`koyfin_downloader.py --tickers {T}` → `transcripts_for_dd.py {T}`），輸出必讀/可略讀逐字稿路徑清單寫回 evidence.json 的 `transcripts` 區塊；session 過期只標記不阻塞。
   - **開寫前置閘**：`python3 scripts/validate_evidence.py .dd_build/{T}_{D}.evidence.json --strict --report`。**FAIL 就回補資料**（對缺軸／不合格軸重 spawn 該子任務，≤2 次重試），**不得帶缺口開寫**——兩步制下 Stage 0 是唯一的資料把關點，缺口帶進第二步就沒有 critic 會攔。`--strict` PASS 才進 Writer。

3. **Writer：判斷＋呈現＋自查**（單一 agent、單一 context，`--writer-model fable|sonnet|opus`，**預設 `fable`**）：
   - spawn 模板見 `references/v16/agent-prompts.md` (b)。輸入＝`evidence.json` 路徑＋逐字稿 `must_read` 清單（親讀，不摘錄）＋`references/v16/judgment-rules.md`＋archetype 對應 reference（同 v15.2 條件載入路由表）＋`references/v16/render-rules.md`（動筆散文前才載入）。
   - **① 判斷物**：`.dd_build/{T}_{D}.judgment.json`＋`.dd_build/{T}_{D}.scenario.json`，各一次 Write。writer 自己一次複合 Bash 跑：`dd_scenario.py .dd_build/{T}_{D}.scenario.json --html .dd_build/{T}_{D}.tables/e11.html --meta .dd_build/{T}_{D}.scenario_meta.json` → `dd_decision.py run .dd_build/{T}_{D}.judgment.json --html .dd_build/{T}_{D}.tables/audit.html --json .dd_build/{T}_{D}.judgment.json`（欄位契約見 `scripts/dd_schema/decision_inputs.md`；`run` 只覆寫機械欄，不清空手填欄）→ `validate_judgment.py ... --report --evidence .dd_build/{T}_{D}.evidence.json`。任一 FAIL → **只准改欄位**重跑這三支，≤3 輪。
   - **② 呈現**（三支全過才開始）：`gen_dd_tables.py .dd_build/{T}_{D}.judgment.json --out .dd_build/{T}_{D}.tables --scenario-html .dd_build/{T}_{D}.tables/e11.html --scenario-meta .dd_build/{T}_{D}.scenario_meta.json`（dashboard／E2／E3／E5-E10／E11／E12／dd-meta／appA 表；audit 表視 `decision_out.audit_rows` 非空）→ `dd_prose_budget.py .dd_build/{T}_{D}.judgment.json --tables .dd_build/{T}_{D}.tables` 得各段散文目標 bytes（表格計入分子）→ 依表逐段**一次 `Write`** `.dd_build/{T}_{D}.prose/{sid}.html`（**禁 `Edit`**，render-rules §0 一次寫條款）。
   - **③ 組裝與六支閘**：`render_dd.py --assemble .dd_build/{T}_{D}.prose --tables .dd_build/{T}_{D}.tables --judgment .dd_build/{T}_{D}.judgment.json -o {OUT_HTML}` → `validate_prose.py`（正文數字 ⊆ 判斷物數字集合）／`dd_sections.py bytes`／`dd_sections.py leaks`／`qc.py`／`validate_dd_meta.py --report`／`verify_dd_math.py`（HTML 版）。`{OUT_HTML}`＝`--dry-run` 時 `.dd_build/DD_{T}_{D}.v16dryrun.html`，否則 `docs/dd/DD_{T}_{D}.html`。超標或命中**只重寫該段 prose 檔**（整檔 Write）、重新組裝、重跑；每段最多重寫一次，不動 judgment.json。
   - **④ 交稿前自查**（取代原獨立 critic）：writer 依模板 (b) 第三階段的自查表 ①-⑧（QC-41 四軸＋覆蓋面掃描〔缺軸即 🔴〕＋量化模組完整性抽查＋數字新鮮度＋散文一致性）逐條 🟢/🟡/🔴 作答，🔴 先改該欄位或整檔重寫該段一次再交稿；**自查表是回報的必要欄位，缺表視為未交稿**。
   - **禁**：WebSearch/WebFetch（證據不足在該軸 `note` 標「證據包未涵蓋」，不得自搜）、Read 任何 `docs/dd/`、重讀自己寫過的產物、prose 目錄用 `Edit`。

4. **INDEX／同步／size gate／commit**（沿用 v2.3 步驟 4.5-7）：INDEX.md 登錄 → `python scripts/update_dd_index.py`（同步 research 頁＋dd-screener＋picks）→ size-budget gate（`dd_sections.py bytes`，70KB 下界／75-105KB 目標／115KB 上界警告）→ `docs/dd/DD_*`、`docs/research/_body.html`、`docs/dd-screener/latest.json`、`docs/picks/candidates.json` 併入同一 commit → push main。commit 訊息附註 `[v16-draft]` 供試點回溯量測。**`--dry-run` 時整個步驟 4 跳過**（不寫 `docs/dd/`、不跑 `update_dd_index.py`、不 commit／push），只回報六支閘輸出、自查表與兩段 token 用量。

   **（流程外）事後抽查**：前三份上站後，orchestrator 另 spawn 一次冷讀（模型與 writer 不同；Fable writer → opus），只計判斷級 🔴 數、不修補、不重跑腳本，輸出存 `notes/site-internal/dd/_audit_{T}_{D}.md`。抽查只餵設計稿 §13 退場訊號，永不阻斷發布。

## 邊界

- `--dry-run`（組裝到 `.dd_build/`、不上站、不 commit）供流程試點與 A/B writer 模型用；跑完仍要回報六支閘輸出、自查表與成本，才算一份有效試點。
- 不新增判斷語意、不動決策矩陣／dd-meta schema／QC-41 checklist 條文本身（只改由誰執行——v16.1 由 writer 自查，見 `references/v16/agent-prompts.md`）。
- `.dd_build/` 下所有中間檔案皆非最終產物，不進 commit（只有步驟 4 列的四類進 commit；事後抽查的 `_audit_*.md` 於抽查完成後另行 commit）。
- 本檔為草案，**不覆蓋、不取代** `.claude/skills/ddreport/SKILL.md`（v2.3 仍是預設鏈）；WP4 驗收通過前，任何非明確帶 `--v16` 的請求一律照舊走 v2.3。
