---
name: stock-analyst
version: v16.2-draft
released: 2026-09-04
description: "（WP2 draft，未接線、未取代現行 v15.2 SKILL.md）收到股票 ticker 後，以三步制管線（Stage 0＋0e sonnet 收資料與逐字稿摘要，`validate_evidence.py --strict` 過才准開寫 → 判斷 agent（Fable）只寫 judgment.json／scenario.json → 散文 agent（sonnet）讀 judgment.json 鋪陳，機械閘全過即上站）產出單一 DD 報告（docs/dd/DD_{TICKER}_{YYYYMMDD}.html，dd-meta schema=v15.0，report-facing 版號凍結不變）。判斷機器（QC-1~QC-54 門檻、決策矩陣 rows 1-10、fail-safe 方向、dd-meta 契約）逐字未動，只重排『誰在什麼 context 做什麼、用什麼格式交接』。目標＝每份報告 Fable 用量最小、整週用量最小、品質不掉。北極星、篇幅帶、E1-E12 表格收斂、統一裁決三詞頭銜、四值倉位角色等報告端規格與 v15.2 完全一致。觸發語與 v15.2 相同：『個股分析 {ticker}』『{ticker} DD』/ DD 報告 / 股票研究 / 估值分析 / 『{ticker} dca』『{ticker} 定見』『conviction analysis {ticker}』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』；裸 ticker 與『這檔如何/值不值得研究/先篩一下 {ticker}』不觸發本 skill，改走 stock-screen-v1。"
---

> **v16.2（2026-09-04，接續 v16.1 兩步制「大道至簡」拍板）**：全鏈四段——**Stage 0（sonnet 收資料）＋0e（sonnet 逐字稿摘要，除最新一季外）→ `validate_evidence.py --strict` 過才准開寫 → 判斷 agent（Fable，只寫 judgment.json／scenario.json，不碰散文）→ 散文 agent（sonnet，讀 judgment.json 鋪陳，不重讀 evidence.json 全文），機械閘全過即上站**。**流程內沒有 critic、沒有 patch agent、沒有 re-gate、沒有輕 critic。** 原七軸 critic checklist 拆進判斷／散文兩個agent 各自的交稿前自查表（①-⑦判斷層歸判斷 agent，⑧散文一致性歸散文 agent）；驗收改為前三份上站後的事後冷讀抽查（只計數不修補）。**成因**：v16.1 單一 Fable context 同時判斷＋呈現，PANW 實測 Fable cache_creation 單價（$12.5/M）吃掉美元成本大頭；v16.2 把判斷與呈現拆開，讓 Fable 只做最需要它的判斷部分，呈現交回便宜的 sonnet。成因與退場訊號見設計稿 §13、§16。判斷機器門檻、矩陣、dd-meta 語意零變動。
>
> **本檔狀態**：WP2（規則三分法拆分）交付物之一，**草稿**——尚未通過 WP1 回溯考卷（`dd_decision.py --check-all` 30/30、`gen_dd_tables.py` 反推比對）與 WP4 試點驗收，**不得取代 `.claude/skills/stock-analyst/SKILL.md`**（現行 v15.2，唯一生產版本）。ddreport v3（把本檔的鏈固化成一鍵指令）由 WP3 另寫，本檔只引用其名不重複內容。設計依據：`notes/site-internal/dd/_v16_design_spec_20260903.md`（下稱「設計稿」）。

---

## 北極星（v15.0 拍板，report-facing 語意零變更）

目標＝找到真值得長期投資的公司：獲利好且獲利品質好；ROIC 好且持續期長；產業結構與護城河都好——好價格是加分。生意決定買不買，價格決定何時買。完整文字見 `references/v16/judgment-rules.md` §0（判斷 agent 唯一讀本，本檔不重複）。

---

## 一、四段制流程總覽（v16.2）

```
Stage 0＋0e  證據包＋逐字稿摘要（sonnet fan-out，平行，零判斷）
  0a 數字包（沿用 data-collection.md 既有 spawn 模板，含財報時效閘）
     ＋ dd_numbers_extra.py 先產扁平三欄 numbers.price_at_dd／price_as_of／
       earnings_recency（v16.2 新增，validate_evidence 必填）＋ 五個結構化欄位：
       numbers.latest_quarter_kpis／valuation_history／peer_financials／
       momentum_26w（含 rsi14_usable）／edgar_concentrations／consensus_revision
       （含 stale 旗標）
  0b 覆蓋矩陣：archetype 決定軸清單（references/coverage-axes.md），
     每 3-5 軸一子 agent，回傳 sourced findings，orchestrator 只 merge 不讀內容；
     負責 major_events 軸的那批同時交付頂層 events 五組（QC-19，v16.2 明文接線）
  0c 事件掃描：併入 0b 的 major_events 軸（QC-19 五組查詢已模板化在 coverage-axes.md）
  0d 前份 DD 三區塊＋知識帳本＋canonical ID 事實區塊：dd_prior.py（零 LLM 腳本擷取）
  0e 逐字稿摘要（v16.2 新增，sonnet）：把 transcripts.must_read_all 中除最新一季外
     的三篇（＋optional 的 Investor Day 若有）逐篇讀成 transcript_digest.json
     （每篇 ≥12 條逐字 quote＋qa_flags）；`validate_digest.py` 驗證每條 quote
     皆能在原文逐字找到；merge 回 evidence.json 的 transcripts.digest_path。
     最新一季全文留給判斷 agent 親讀，不進 0e 範圍。
  輸出：.dd_build/{T}_{D}.evidence.json（＋ transcript_digest.json）
  **閘：validate_evidence.py --strict 過才准開寫**——FAIL 就回補該軸資料或摘要，
  不得帶缺口進下一段

判斷 agent（Fable，`--judgment-model`，預設 fable；不上網；只寫 JSON，不碰散文）
  讀：evidence.json ＋ 最新一季逐字稿全文（親讀）＋ digest.json（其餘三季摘要，
      引用時標「來源：摘要」）＋ judgment-rules.md ＋ archetype 對應 reference
      （不讀 render-rules.md，不讀任何 prose/tables 目錄）
  寫：judgment.json（一次 Write）、scenario.json（一次 Write）
  機械（一次複合 Bash）：dd_scenario.py → dd_decision.py run → validate_judgment.py
     --evidence；FAIL 只准改欄位重跑，≤3 輪
  交稿前自查（取代原 critic①-⑦）：QC-41 四軸＋覆蓋面掃描（缺軸即 🔴）＋量化模組
     完整性抽查＋數字新鮮度，逐條 🟢/🟡/🔴 打勾；🔴 先改該欄位再交稿，自查表為回報必要欄位

散文 agent（sonnet，固定；不上網；只讀 judgment.json 鋪陳，不改判斷）
  讀：judgment.json（含 reasoning 段，承重數字唯一來源）＋ render-rules.md
      ＋ gen_dd_tables.py／dd_prose_budget.py 產物（**不讀 evidence.json 全文**）
  呈現：gen_dd_tables.py 產表 → dd_prose_budget.py 算每段目標 bytes
     → 每段 .dd_build/{T}_{D}.prose/{sid}.html 一次 Write（禁 Edit，表格計入分子）
     → render_dd.py --assemble ... -o {OUT_HTML}
     → 六支驗證：validate_prose／dd_sections bytes／dd_sections leaks／qc.py／
       validate_dd_meta／verify_dd_math（HTML 版）；未過只重寫該段一次
  交稿前自查（取代原 critic⑧）：散文一致性＋QC-54 白話開場，🔴 先重寫該段再交稿

（流程外）事後抽查：前三份上站後 orchestrator 另 spawn 一次冷讀（模型與判斷 agent 不同），
  輸入含 evidence.json＋judgment.json＋transcript_digest.json（SNOW 教訓：冷讀者缺逐字稿
  摘要會誤判 writer 親讀得到的正確判斷為無據），只計判斷級 🔴 數、不修補，
  存 notes/site-internal/dd/_audit_{T}_{D}.md，只餵退場訊號
```

Orchestrator（opus）只做：spawn、傳檔名、讀 validator 輸出、commit。**不讀任何報告內容進自己的 context**（設計稿 §2 硬性原則）。

---

## 二、條件載入路由表

| 讀者 | 時點 | 必 Read | 說明 |
|---|---|---|---|
| Stage 0b 子 agent | 派工時 | `references/evidence-pack.md`（spawn 模板＋規則五條，含 v16.2 major_events→events 頂層交付規則）＋ `references/coverage-axes.md`（軸清單 JSON，唯一權威） | 不讀 judgment-rules.md（不做判斷，只採集） |
| Stage 0e 摘要 agent | 派工時 | `references/v16/agent-prompts.md` (a2)（spawn 模板）＋逐字稿原文路徑清單 | 不讀 judgment-rules.md／render-rules.md，禁推論裁決 |
| 判斷 agent | 一律 | `references/v16/judgment-rules.md`（always-on，≤40KB） | 唯一判斷規則檔，不重述 schema；不讀 render-rules.md |
| 判斷 agent | archetype∈循環子型 | `references/cyclical-lens.md` | QC-42 全文＋附錄 B 位置錶族 |
| 判斷 agent | archetype∈{金融、未獲利、轉機、受監管公用} | `references/archetype-gatesets.md` | QC-44/45/46 全文 |
| 判斷 agent | 寫 §5.R 前 | `references/roic-durability.md` | 一律 |
| 判斷 agent | Part II 判斷前 | `references/judgment-playbook.md` | QC-53 觸發索引，命中逐條實答 |
| 判斷 agent | 填 appendix_a 四欄前 | `references/timing-appendix.md` | 未讀不得填 |
| 判斷 agent | 90 天內裁決翻面 | evidence.json.prior_dd.triggers（已含在 evidence 包，非另讀檔） | QC-49 |
| 判斷 agent | 交稿前自查 | 無須另讀檔——自查表 ①-⑦ 已逐條寫進 spawn prompt（`references/v16/agent-prompts.md` (b1)），條文語意沿 `critic-gates.md` QC-41 原文 | 流程內無獨立 critic；`critic-gates.md` 僅留作事後抽查與規則沿革參照 |
| 散文 agent | 一律 | `references/v16/render-rules.md`（always-on，≤15KB） | 唯一呈現規則檔；§0 一次寫條款為硬規則；不讀 judgment-rules.md |
| 散文 agent | 寫 prose 前 | `gen_dd_tables.py` 產出的 `TABLES_DIR/*.html` 清單＋`dd_prose_budget.py` 目標 bytes 表 | 機械先行，散文只讀產物不重算、不重寫表格；**不讀 evidence.json 全文** |
| 散文 agent | 交稿前自查 | 自查表 ⑧＋QC-54 已寫進 `agent-prompts.md` (b2) | 判斷層①-⑦已由判斷 agent 做過，不重複 |
| orchestrator | 改規則前 | `references/changelog.md`＋`knowledge/rule_ledger.md` | 判斷類規則增刪同步 rule_ledger |
| orchestrator | delta 複審請求 | `scripts/dd_delta.py`（另案，草案中，見 ddreport v3.1 邊界一句） | 已知缺口，非本輪範圍 |

**不進判斷 agent context 的檔**：`decision-layer.md`（矩陣已由 `dd_decision.py` 機械翻譯，只填 `decision_inputs`）、`html-output.md`／`render-rules.md`（呈現規則，歸散文 agent）、`dd-meta-schema.md`（權威已轉移 `judgment.schema.json`＋`judgment-to-ddmeta.md`）。**不進散文 agent context 的檔**：`judgment-rules.md`（判斷規則，已由判斷 agent 定案）、`evidence.json` 全文。

---

## 三、Stage 0／判斷 agent／散文 agent／orchestrator 契約

> 完整 spawn prompt 全文（含逐字讀寫範圍、禁令、回報格式）已由 WP3 草擬於 `references/v16/agent-prompts.md`（(a) Stage 0b 子 agent／(a2) Stage 0e 逐字稿摘要子 agent／(b1) 判斷 agent／(b2) 散文 agent；(c) 是流程外事後抽查說明，不是派工模板。v16.2 起無 critic／patch 模板）。本節只列**腳本名、CLI 旗標、驗證鏈順序**這個「契約骨架」，不重複 prompt 全文；`agent-prompts.md` 若與本節腳本旗標描述有出入，以腳本 `--help` 實際輸出為準。

### Stage 0＋0e
| 步驟 | 指令 |
|---|---|
| 0a 結構化數字欄位 | `python3 scripts/dd_numbers_extra.py {T} {D} --peers "{PEERS}" --out .dd_build/evidence_parts/numbers_extra.json`（零 LLM；產扁平三欄 `price_at_dd`／`price_as_of`／`earnings_recency`＋五個結構化欄位 `latest_quarter_kpis`／`valuation_history`／`peer_financials`／`momentum_26w`／`edgar_concentrations`／`consensus_revision`），再 spawn 採集 agent 補 KPI 缺項（**只能在既有鍵原地補值，不得改鍵名或另包一層**） |
| 0b 軸展開 | `python3 scripts/dd_evidence.py axes --archetype "{ARCHETYPE}" --ticker {T} --company "{C}" --industry "{I}" --customers "{CUST}" [--segments a,b,c] --json` |
| 0b 骨架初始化 | `python3 scripts/dd_evidence.py init {T} {D} --archetype "{ARCHETYPE}"` |
| 0b merge | `python3 scripts/dd_evidence.py merge .dd_build/{T}_{D}.evidence.json .dd_build/evidence_parts/{part}.json`（逐一；major_events 批次的 part 檔含頂層 `coverage`＋`events` 兩鍵，同一次 merge 即可） |
| 0d 前份/帳本/ID | `python3 scripts/dd_prior.py {T} --date {D} --out .dd_build/evidence_parts/prior.json`（零 LLM） |
| **0e 逐字稿摘要** | spawn (a2) 子 agent 寫 `.dd_build/{T}_{D}.transcript_digest.json` → `python3 scripts/validate_digest.py .dd_build/{T}_{D}.transcript_digest.json --transcripts {DIR}`（FAIL 找出幻覺 quote 重寫，≤2 輪）→ merge `{"transcripts":{"digest_path":"..."}}` 回 evidence.json |
| **開寫前置閘** | `python3 scripts/validate_evidence.py .dd_build/{T}_{D}.evidence.json --strict --report`；**FAIL 就回補該軸資料或摘要（對該軸/0e 重 spawn），不得帶缺口進下一段**——Stage 0 是唯一的資料把關點 |

### 判斷 agent（`--judgment-model {fable|sonnet|opus}`，**預設 fable**）
判斷物寫完，一次複合 Bash：
```
python3 scripts/dd_scenario.py .dd_build/{T}_{D}.scenario.json --html .dd_build/{T}_{D}.tables/e11.html --meta .dd_build/{T}_{D}.scenario_meta.json
python3 scripts/dd_decision.py run .dd_build/{T}_{D}.judgment.json --html .dd_build/{T}_{D}.tables/audit.html --json .dd_build/{T}_{D}.judgment.json
python3 scripts/validate_judgment.py .dd_build/{T}_{D}.judgment.json --report --evidence .dd_build/{T}_{D}.evidence.json
```
FAIL 只准改 `judgment.json`／`scenario.json` 欄位重跑，≤3 輪。三支全過、交稿前自查①-⑦過關即交棒散文 agent——**判斷 agent 到此結束，不接著寫散文**。

### 散文 agent（sonnet，固定，另 spawn）
```
python3 scripts/gen_dd_tables.py .dd_build/{T}_{D}.judgment.json --out .dd_build/{T}_{D}.tables --scenario-html .dd_build/{T}_{D}.tables/e11.html --scenario-meta .dd_build/{T}_{D}.scenario_meta.json
python3 scripts/dd_prose_budget.py .dd_build/{T}_{D}.judgment.json --tables .dd_build/{T}_{D}.tables
（散文 agent 依目標 bytes 表寫 .dd_build/{T}_{D}.prose/{sid}.html，每段一次 Write，禁 Edit）
python3 scripts/render_dd.py --assemble .dd_build/{T}_{D}.prose --tables .dd_build/{T}_{D}.tables --judgment .dd_build/{T}_{D}.judgment.json -o {OUT_HTML}
python3 scripts/validate_prose.py .dd_build/{T}_{D}.prose --judgment .dd_build/{T}_{D}.judgment.json --evidence .dd_build/{T}_{D}.evidence.json
python3 scripts/dd_sections.py bytes {OUT_HTML}
python3 scripts/dd_sections.py leaks {OUT_HTML}
python3 scripts/qc.py {OUT_HTML}
python3 scripts/validate_dd_meta.py {OUT_HTML} --report
python3 scripts/verify_dd_math.py {OUT_HTML}
```
`{OUT_HTML}`＝dry-run 時 `.dd_build/DD_{T}_{D}.v16dryrun.html`、正式時 `docs/dd/DD_{T}_{D}.html`。任一 FAIL：**只重寫命中的 `prose/{sid}.html`（整檔 Write）→ 重新組裝 → 重跑**，每段最多重寫一次，不動判斷物。六支閘全過後，散文 agent 跑交稿前自查（⑧散文一致性＋QC-54，見 `agent-prompts.md` (b2)），🔴 先修再交，自查表為回報必要欄位。

### Orchestrator（ddreport v3.1，WP3 另寫，本檔只引用鏈順序）
```
koyfin 增量下載（沿用 v15.2）→ dd_numbers_extra → Stage 0 fan-out → Stage 0e 摘要 → validate_evidence --strict
→ 判斷 agent（Fable，判斷三支＋自查①-⑦）
→ 散文 agent（sonnet，產表／算預算 → 散文 → 組裝 → 六支閘 → 自查⑧＋QC-54）
→ INDEX.md 登錄 → python scripts/update_dd_index.py → qc.py → commit
（流程外，前三份）事後冷讀抽查 → notes/site-internal/dd/_audit_{T}_{D}.md，只計數不修補
```
Orchestrator 全程只看 validator 輸出與兩個 agent 的自查表，不讀報告內容、不讀 prose 段落。

---

## 四、Token 紀律（v16.2 三步制）

**第一槓桿不變但機制再進一步**：v15.2 的槓桿是「writer 對輸出檔禁 Edit、驗證用腳本定位」；v16.1 把交接次數壓到一次（Stage0 → 單一 Fable writer）；v16.2 在此基礎上**把判斷與呈現拆回兩個 agent，但拆分邊界刻意選在「便宜」那一側**——呈現不需要 Fable 的判斷力，讀 judgment.json 鋪陳是 sonnet 就能做好的機械翻譯工作，讓 Fable 只做真正需要它的判斷：
- **判斷 agent（Fable）只寫 JSON**：不產表、不寫散文、不讀 render-rules.md，讀取範圍收斂到 evidence.json＋最新一季逐字稿＋digest.json＋judgment-rules.md。v16.1 PANW 實測 Fable 一個 context 走完判斷＋呈現，cache_read 7.7M（去重尺）＋cache_creation 2.01M（單價 $12.5/M，佔美元成本大頭）；拆開後判斷 agent 的讀寫量大幅縮小，目標 cache_read ≤3M。
- **散文 agent（sonnet）不重讀 evidence.json 全文**：只讀 judgment.json（已收斂的判斷結果，含 reasoning）＋表格產物，比讀 80KB+ 的 evidence.json 便宜得多；且 sonnet 的 cache_creation 單價（$2.5/M）遠低於 Fable。
- **0e 逐字稿摘要（sonnet）分攤親讀成本**：除最新一季外的三篇法說稿改由 sonnet 讀成結構化摘要，判斷 agent（Fable）只需親讀最新一季，摘要真實性由 `validate_digest.py` 逐字引句驗證把關（不是省去查證，是把查證換成便宜的機械比對）。
- 段落級修補仍在：機械閘 FAIL 只重寫命中的 `prose/{sid}.html`（單段幾 KB），不是 80KB 散文的 extract/replace。
- 規則不再每份重讀 225KB（v15.2 每份 writer 先讀 SKILL.md 125.8KB＋7-8 份 references）：判斷 agent 只讀 `judgment-rules.md`（≤40KB）＋條件載入的 archetype reference；散文 agent 只讀 `render-rules.md`（≤15KB）。

**判斷 agent 端硬紀律**（見 `agent-prompts.md` (b1)）：①不重讀自己寫過的檔；②不 Read 任何 `docs/dd/`；③禁 WebSearch／WebFetch；④每檔一次 `Write`；⑤不寫 prose、不跑 `gen_dd_tables.py`／`render_dd.py`。
**散文 agent 端硬紀律**（見 `agent-prompts.md` (b2)）：①不讀 evidence.json 全文；②不改 `judgment.json` 任何欄位；③每檔一次 `Write`，prose 目錄禁 `Edit`；④動筆前先看 `dd_prose_budget.py` 目標 bytes 表，不邊寫邊湊篇幅。

**外包界線不變**：有唯一正確答案、派工前就能定義清楚的查證＝Stage 0（採集/覆蓋矩陣/逐字稿摘要）；需要先知道自己在找什麼才看得見答案的閱讀（最新一季逐字稿、前份 DD 假設觸發器、ID 事實區塊）與判斷端（archetype 換尺、moat_trend 方向、QC-39 兩閘裁定）一律判斷 agent 自讀自判，不外包。

**模型分工（v16.2 定版）**：

| 段 | 模型 | 說明 |
|---|---|---|
| Stage 0 收資料 | **sonnet** | fan-out 平行；`validate_evidence.py --strict` 過才准開寫 |
| Stage 0e 逐字稿摘要 | **sonnet** | 除最新一季外三篇＋optional；`validate_digest.py` 逐字引句驗證 |
| 判斷 agent | **Fable** | `--judgment-model`，預設 `fable`（可改 `sonnet`／`opus`）；只寫 judgment.json／scenario.json |
| 散文 agent | **sonnet** | 固定；讀 judgment.json 鋪陳，不判斷 |
| 流程內 critic | **無** | 原七軸 checklist 拆給兩個 agent 各自的交稿前自查（①-⑦判斷／⑧＋QC-54 散文）；驗收改事後抽查 |
| 事後抽查（流程外，前三份） | 與判斷 agent 不同模型（Fable 判斷 → opus） | 只計判斷級 🔴 數，不修補、不阻斷發布 |

repo CLAUDE.md「writer 與 critic 永不同模型」的鐵律在 v16.2 試點期以**流程外抽查**的形式維持（跨模型的眼睛沒有消失，只是移到上站之後、且不再是 gate）——此為明文推翻既有拍板，理由與退場訊號見設計稿 §13、§16。

**機械輪次批次化三條**（每個 spawn prompt 末尾附帶，逐字沿用 v15.2）：①定位先於動手，一輪複合 grep/查詢取齊；②同檔機械性修改 ≥5 處禁逐個修補；③Bash 驗證併成單條複合指令，驗證輪次 ≤3 輪。

**成本模型**（三個數字：Fable／opus／sonnet；**2026-09-04 起一律用 `scripts/dd_token_report.py` 按 message.id 去重的 cache_read 尺**，舊尺把同一則訊息的多個 tool_use 行重複加總，高估 2–3 倍）：v15.2 同檔實測 SNOW ≈49M（writer 34.1／critic 2.4／patch 12.1）、DELL ≈78M（writer 59.7／critic 3.2／patch 14.7）；v16.0 兩段式實測 SNOW ≈60M（Stage 0 4.8／判斷 16.3／critic 3.0／patch 13.7／呈現 21.7）、DELL ≈68M（5.5／5.2／4.8／12.0／40.2）；v16.1 兩步制實測 SNOW dry-run ≈14.9M（Stage 0 sonnet 7.5／Fable writer 7.5）、PANW ≈14.8M（Stage 0 sonnet 7.1／Fable writer 7.7）——單一 Fable context 同時判斷＋呈現，cache_creation（PANW 2.01M，單價 $12.5/M）是美元成本主因。**v16.2 目標**：拆開判斷／呈現後，**Fable 每份 ≤3M（cache_read；判斷只讀約 85K token context、≤15 輪）、sonnet 散文 ≤4M、每份合計 ≤15M**——目標不是壓總 token，是把貴的 Fable 用量壓到最小，讓整週美元成本下降。前三份試點回填實測值。

**散文 agent ≤4M 目標的達成手段（2026-09-04，CRDO 實測 6.8M 超標後補課）**：CRDO 首份散文 agent 54 次工具呼叫燒 6.8M——13 次讀規則/表格、3 次讀 `render_dd.py` 原始碼、18 次段落 Write、19 次驗證/修補（3 輪 render+validate、3 次誤用 `Edit` 局部補符號違反 §0 一次寫條款、1 次 grep `validate_prose.py` 原始碼、2 次 grep 定位字串）。五項修法：①`validate_prose.py --dump-numbers` 產逐字數字白名單（含 −/%/$ 符號慣例），(b2) 動筆前先讀、逐字複製，避免符號漏帶（如「年減 2.9%」漏負號）多跑一輪；②`dd_sections.py leaks` 詞表與 `validate_prose.py` 符號正規化規則抽成 11 行摘要內嵌 `agent-prompts.md` (b2) 模板，動筆前對照，不必 grep 原始碼；③六支機械閘合成 `scripts/dd_gates.sh {T} {D} {OUT_HTML}`（順序執行＋彙總輸出＋任一真正擋下的閘 exit 1），(b2) 只呼叫這一支，驗證輪次上限由 3 降 2；④「prose 目錄任何 `Edit` 視為無效輸出」改模板層明文強調（放棄 mtime 機械偵測——跨 session/跨工具寫入序號比對成本高於效益，本輪刻意選擇模板強調而非機制擋）；⑤`render-rules.md` 由 18.4KB 砍歷史/沿革敘述與冗餘表格欄壓縮至 15.9KB，(b2) 讀取量同步下降。下一份看散文 cache_read 能否落回 ≤4M。

**退場訊號（設計稿 §13、§16，四條，任一未達即回退）**：
1. **覆蓋缺軸 0**（v16.0/v16.1 皆 0，此為不得倒退的底線；`--strict` 前置閘是主要保證）。
2. **前三份上站後事後冷讀抽查，判斷級 🔴 合計為 0 → 永久拿掉本驗收；出現 1 例 → 判斷層驗收放回流程內**（恢復流程內 critic gate）。
3. **機械閘全過、裁決與前份同向或有歸因**（judgment-rules §12 item 3b 的漂移歸因檢查）。
4. **Fable 每份 ≤3M、sonnet 散文 ≤4M、每份合計 ≤15M**（cache_read，去重尺；v16.2 新增，取代 v16.1「每份成本 ≤ v15.2 同檔」與舊目標「Fable ≤8M」——v16.1 已證明總 token 量可以低於 v15.2，但美元成本因 Fable 單價（cache_creation $12.5/M）反而更高；v16.2 直接把北極星換成「Fable 用量」這個真正要壓的量）。

---

## 五、最終回報格式（orchestrator 對用戶）

沿用 v15.2 既有格式，欄位對映到 v16 產物：
```
✅ v15.0 DD 報告完成：[TICKER]
📄 檔案：docs/dd/DD_TICKER_YYYYMMDD.html
💰 最新股價：$__（來源：evidence.json.numbers）
🎯 統一裁決：[進場 / 觀望 / 迴避]（倉位角色：__；row_hit：__，來自 dd_decision.py 輸出）
📊 基本面評級：[A+/A/B/C/X]（metadata）｜陷阱定性：[🟢/🟡/🔴]
🛡️ 護城河趨勢：[↑/→/↓]（權威）｜Y5 後跑道：[🟢/🟡/🔴]｜Max DD：[−__%]
📈 5Y EV：[+__%]／Base IRR：[__%/yr]（三分量：EPS __ / re-rate __ / 股息回購 __）
💡 opportunity cost：__
🔗 首頁同步：[✅ 成功 / ❌ 失敗，需手動 python scripts/update_dd_index.py]
```
**新增（v16.2）**：分模型三欄 token 用量（`python3 scripts/dd_token_report.py {SESSION_ID}`，Stage 0＋0e＝sonnet／判斷 agent＝Fable 或旗標指定模型／散文 agent＝sonnet，各自 cache_read／cache_creation）＋ `dd_decision.py --check` 與最終 HTML dd-meta 的 `dca_verdict` 是否一致（一致性自我檢查，理論上恆真，若不真代表 `gen_dd_tables.py` 或 `render_dd.py --assemble` 有 bug）。

**回報上限**：≤400 字＋INDEX 行，不複述報告內容，只給路徑／KB／Part I 佔比／§13 裁決與前份對比／3-5 條決策相關變化／自查表 🔴🟡 項／gate 狀態／`dd_sections.py bytes` 表原文。

---

## 六、不做的事（PREREG，同設計稿 §10）

不改任何門檻、機率防線、矩陣語意、dd-meta 欄位語意；**最新一季逐字稿仍強制親讀，不外包**（v16.2 只把「除最新一季外」的三篇改成 sonnet 摘要＋`validate_digest.py` 逐字引句驗證，設計稿 §8 待決 1 的「維持親讀」原則對最新一季不變）；不新建收斂面、不動下游聚合器（`update_dd_index.py`／dd-screener／picks 讀 dd-meta 不變）；不在本輪處理既有 DD 的未跳脫 `<`（另案 batch fix）；不動 `scripts/dd_delta.py`（另一 WP 進行中的差異模式腳本）；**本檔本身不生效**——取代 `SKILL.md` 需先過 WP1 回溯考卷與 WP4 試點驗收，由持有人裁定切換時點。
