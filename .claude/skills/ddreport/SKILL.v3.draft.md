---
name: ddreport
version: v3.0-draft
released: 2026-09-03
description: "v16 草案：thin orchestrator，把 stock-analyst v16 的證據→判斷→呈現三段鏈（設計稿 notes/site-internal/dd/_v16_design_spec_20260903.md）固化成一鍵。與現行 v2.3（單一巨石 writer→critic→patch）並存——本鏈由 `ddreport --v16 {ticker}` 觸發，預設仍走 v2.3。orchestrator（opus）全程只 spawn、傳檔名、讀 validator 輸出、決定是否 re-gate、commit，**不讀任何報告內容或 evidence/judgment JSON 進自己的 context**。"
---

# DD Report Pipeline v3（draft，v16 三段鏈 orchestrator）

```
git hygiene → Stage0 證據包（writer-free，fan-out）→ validate_evidence
  → Stage1 判斷物（單一 agent，模型旗標）→ dd_scenario/dd_decision/validate_judgment/verify_dd_math
  → critic（跨模型冷讀 evidence+judgment）→ patch（改 JSON 子樹）→ [需要時 re-gate]
  → Stage2 呈現（gen_dd_tables 先行 → prose agent → render_dd --assemble）
  → validate_prose/dd_sections bytes/leaks/qc.py/validate_dd_meta → [輕 critic]
  → INDEX/update_dd_index.py → size gate → commit/push
```

**判斷機器零變動**：QC-1～QC-54 門檻、決策矩陣、dd-meta schema 全部凍結（見設計稿 §1）。本鏈只是把散文規則搬進 validator／腳本／JSON 欄位。**與 v15.2 並存**：v16 鏈以 `ddreport --v16 {ticker}` 觸發，未帶旗標一律走現行 v2.3（`.claude/skills/ddreport/SKILL.md`）。WP4 三份試點（兩份 sonnet 判斷層、一份 Fable）通過退場訊號（合計 cache_read 較 v15.2 降 ≥40%、critic 首輪 🔴 降 ≥50%）後才切預設；未過則回 v15.2 檢討，本檔停留草案不轉正。

## Steps

1. **解析 ticker + git hygiene**（沿用 v2.3 步驟 1）：模糊 ticker 先問用戶；開始前 `git log --oneline -5` + `git status` 排除並行 session 的 orphan 檔。決策意圖（要不要加倉/新進/退出）先按 repo CLAUDE.md「Decision-time critic」規則 spawn `industry-thesis-critic`，純研究不觸發。

2. **Stage 0：證據包（writer-free）**。orchestrator 依序：
   - **0d 零 LLM**：`python3 scripts/dd_prior.py {TICKER} --date {DATE} --out .dd_build/parts/prior.json`（前份 DD 三區塊＋q.py 帳本＋canonical ID 事實＋逐字稿路徑清單，一次到位）。
   - `python3 scripts/dd_evidence.py init {TICKER} {DATE} --archetype "{archetype_hint}" [--segments "..."]` 建 `.dd_build/{T}_{D}.evidence.json` 骨架；`dd_evidence.py merge` 併入 0d 片段。
   - **0a 數字包**：spawn sonnet 採集 agent，沿用 `references/data-collection.md` 模板（含財報時效閘），輸出片段 `merge` 進 evidence.json。
   - **0b 覆蓋矩陣 fan-out**：依 `references/evidence-pack.md` §1-§2——`dd_evidence.py axes --archetype ... --json` 展開軸清單（約 14-17 軸），每 3-5 軸一個 sonnet 子 agent（模板見 `references/v16/agent-prompts.md` (a)），每軸 ≤3 輪搜尋；orchestrator 逐一 `dd_evidence.py merge` 併回，**不讀子 agent 回傳內容**。0c（QC-19 事件五組）併入 0b 的「事件」軸，同一批派工。
   - **Koyfin 增量下載**：spawn 一個獨立 sonnet 子任務（沿 v15.2.3 步驟 0：`koyfin_downloader.py --tickers {T}` → `transcripts_for_dd.py {T}`），輸出必讀/可略讀逐字稿路徑清單寫回 evidence.json 的 `transcripts` 區塊；session 過期只標記不阻塞。
   - **驗證**：`python3 scripts/validate_evidence.py .dd_build/{T}_{D}.evidence.json --report`。FAIL → 只對缺軸/不合格軸重 spawn 該子任務（≤2 次重試；2 次仍失敗，該軸標「證據包未涵蓋」放行，交 Stage 1 決定是否回補）。PASS → 進 Stage 1。

3. **Stage 1：判斷物**（單一 agent，模型旗標 `--judge-model sonnet|opus|fable`，預設 `sonnet`）：
   - spawn 模板見 `references/v16/agent-prompts.md` (b)。輸入＝`evidence.json` 路徑＋逐字稿 `must_read` 清單（親讀，不摘錄）＋`references/v16/judgment-rules.md`＋archetype 對應 reference（同 v15.2 條件載入路由表）。
   - 輸出：`.dd_build/{T}_{D}.judgment.json`＋`.dd_build/{T}_{D}.scenario.json`，各一次 Write。
   - orchestrator 機械鏈：`dd_scenario.py .dd_build/{T}_{D}.scenario.json --html .dd_build/{T}_{D}.tables/e11.html --meta .dd_build/{T}_{D}.scenario_meta.json` → `dd_decision.py run` 吃 judgment.json 的 `decision_inputs`（欄位契約見 `scripts/dd_schema/decision_inputs.md`），把 `decision_out` 寫回 judgment.json → `validate_judgment.py .dd_build/{T}_{D}.judgment.json --report` → `verify_dd_math.py`（讀 judgment.json 版本，若尚未支援則暫用既有 HTML 版跳過，記 gap）。
   - 任一 FAIL → 回同一 agent，**只准改欄位**重跑上述三支腳本，≤3 輪。
   - **禁**：WebSearch/WebFetch（證據不足在該軸 `note` 標「證據包未涵蓋」，不得自搜）、寫 HTML、Read 任何 `docs/dd/`。

4. **Critic（跨模型冷讀）**：orchestrator 讀 `judgment.json.decision_out.requires_critic[]`（`dd_decision.py` 已依矩陣寫入該份 DD 命中哪些 gate 名稱）與 QC-41 觸發條件（強方向裁決／moat_trend 方向性／archetype 屬競爭動態·循環商品·法規敏感·B2B 客戶集中），決定要 spawn 哪些 gate；**同時觸發 ≥2 個走合併載具（單一冷讀 critic）**。模型鐵律：判斷層 sonnet → critic **opus**；判斷層 opus/fable → critic **sonnet**（永不同模型）。
   - spawn 模板見 `references/v16/agent-prompts.md` (c)。輸入＝`evidence.json`＋`judgment.json`＋scenario 產物（合計約 40-60KB），**不讀散文**。
   - 輸出：`notes/site-internal/dd/_critic_{T}_{D}.md`，檔頭固定 FINDINGS 表（段落 id 欄改為 **JSON 路徑**，如 `moat.roic_durability.reinvest_rate`）＋ GATE 行。

5. **Patch（sonnet，乾淨 context）**：
   - orchestrator 用 `jq`／小腳本從 judgment.json 抽出 FINDINGS 涉及的 JSON 子樹，連同 FINDINGS 摘錄與證據補件交乾淨 sonnet patch agent（模板見 `references/v16/agent-prompts.md` (d)）。
   - 四步：① `cat` 讀入子樹（不讀 critic md、不讀 skill/reference 檔，規則由 orchestrator 摘進 prompt）；② 改好子樹，一次 Write 到 `.dd_build/{T}_{D}.patch_out/{path}.json`；③ orchestrator 用 merge 腳本把子樹寫回 judgment.json（原子性，全部命中恰 1 才寫）；④ 一次複合 Bash 重跑 `dd_scenario.py`／`dd_decision.py run`／`validate_judgment.py`（三支驗證）。禁 WebSearch/WebFetch、禁改散文。驗證 FAIL 只准再一輪 ②③④，≤10 輪。
   - **GATE=FAIL 才 re-gate**（PASS-with-fixes → patch 完驗證即收工）；re-gate 用同一 critic agent（SendMessage）重驗；仍有 findings → **另 spawn 乾淨的 sonnet patch agent** 只餵 R2 findings（不沿用第一輪 agent，同 v15.2.1/2 教訓）。

6. **Stage 2：呈現**（sonnet）：
   - 機械先行：`python3 scripts/gen_dd_tables.py .dd_build/{T}_{D}.judgment.json --out .dd_build/{T}_{D}.tables/ --scenario-meta .dd_build/{T}_{D}.scenario_meta.json --scenario-html .dd_build/{T}_{D}.tables/e11.html`（產 dashboard／E2／E12／dd-meta／appA 表；audit 表視 `decision_out.audit_rows` 是否非空）。
   - spawn 呈現 agent（模板見 `references/v16/agent-prompts.md` (e)）。輸入＝`evidence.json`＋`judgment.json`（含 `reasoning` 段）＋`references/v16/render-rules.md`＋`gen_dd_tables.py` 已產出的表格片段清單。輸出：`.dd_build/{T}_{D}.prose/{sid}.html` 每段一次 Write（s1…s14、appA 敘述、revlog）。
   - 組裝：`python3 scripts/render_dd.py --assemble .dd_build/{T}_{D}.prose/ --tables .dd_build/{T}_{D}.tables/ --judgment .dd_build/{T}_{D}.judgment.json -o docs/dd/DD_{T}_{D}.html`。
   - 閘：`validate_prose.py .dd_build/{T}_{D}.prose/ --judgment .dd_build/{T}_{D}.judgment.json --evidence .dd_build/{T}_{D}.evidence.json`（正文數字 ⊆ 判斷物數字集合）／`dd_sections.py bytes`／`dd_sections.py leaks`／`qc.py`／`validate_dd_meta.py --report`。超標或命中**只重寫該段 prose 檔**，重跑組裝與該項驗證，不動 judgment.json。
   - **輕 critic**（旗標 `--light-critic`，預設關；前三份試點開著量）：只核 QC-54 ⑦ 白話開場三問＋「散文有無與判斷物矛盾」，同模型或跨模型皆可（不涉裁決）；PASS-with-fixes 直接段落重寫。

7. **INDEX／同步／size gate／commit**（沿用 v2.3 步驟 4.5-7）：INDEX.md 登錄 → `python scripts/update_dd_index.py`（同步 research 頁＋dd-screener＋picks）→ size-budget gate（`dd_sections.py bytes`，70KB 下界／75-105KB 目標／115KB 上界警告）→ `docs/dd/DD_*`、`docs/research/_body.html`、`docs/dd-screener/latest.json`、`docs/picks/candidates.json`、critic 報告併入同一 commit → push main。commit 訊息附註 `[v16-draft]` 供 WP4 試點回溯量測。

## 邊界

- 只跑到 Stage 1（不呈現、不 commit）→ 供 A/B 判斷層模型用，不觸發本鏈其餘步驟。
- 不新增判斷語意、不動決策矩陣／dd-meta schema／critic checklist 條文本身（只改讀法，見 `references/v16/agent-prompts.md`）。
- `.dd_build/` 下所有 Stage 0-2 中間檔案皆非最終產物，不進 commit（只有 §7 列的四類 + critic 報告進 commit）。
- 本檔為草案，**不覆蓋、不取代** `.claude/skills/ddreport/SKILL.md`（v2.3 仍是預設鏈）；WP4 驗收通過前，任何非明確帶 `--v16` 的請求一律照舊走 v2.3。
