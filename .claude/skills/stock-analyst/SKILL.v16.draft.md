---
name: stock-analyst
version: v16.1-draft
released: 2026-09-04
description: "（WP2 draft，未接線、未取代現行 v15.2 SKILL.md）收到股票 ticker 後，以兩步制管線（Stage 0 sonnet 收資料，`validate_evidence.py --strict` 過才准開寫 → Writer Fable 一次寫完判斷＋呈現，機械閘全過即上站）產出單一 DD 報告（docs/dd/DD_{TICKER}_{YYYYMMDD}.html，dd-meta schema=v15.0，report-facing 版號凍結不變）。判斷機器（QC-1~QC-54 門檻、決策矩陣 rows 1-10、fail-safe 方向、dd-meta 契約）逐字未動，只重排『誰在什麼 context 做什麼、用什麼格式交接』。北極星、篇幅帶、E1-E12 表格收斂、統一裁決三詞頭銜、四值倉位角色等報告端規格與 v15.2 完全一致。觸發語與 v15.2 相同：『個股分析 {ticker}』『{ticker} DD』/ DD 報告 / 股票研究 / 估值分析 / 『{ticker} dca』『{ticker} 定見』『conviction analysis {ticker}』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』；裸 ticker 與『這檔如何/值不值得研究/先篩一下 {ticker}』不觸發本 skill，改走 stock-screen-v1。"
---

> **v16.1 兩步制（2026-09-04 持有人拍板：大道至簡）**：全鏈只剩兩步——**Stage 0（sonnet 收資料，`validate_evidence.py --strict` 過才准開寫）→ Writer（Fable，一個 context 判斷＋呈現＋交稿前自查一次寫完，機械閘全過即上站）**。**流程內沒有 critic、沒有 patch agent、沒有 re-gate、沒有輕 critic、沒有兩段式交接。** 原七軸 critic checklist（含覆蓋面掃描與量化模組抽查）改為 writer 的交稿前自查表；驗收改為前三份上站後的事後冷讀抽查（只計數不修補）。成因與退場訊號見設計稿 §13。判斷機器門檻、矩陣、dd-meta 語意零變動。
>
> **本檔狀態**：WP2（規則三分法拆分）交付物之一，**草稿**——尚未通過 WP1 回溯考卷（`dd_decision.py --check-all` 30/30、`gen_dd_tables.py` 反推比對）與 WP4 試點驗收，**不得取代 `.claude/skills/stock-analyst/SKILL.md`**（現行 v15.2，唯一生產版本）。ddreport v3（把本檔的鏈固化成一鍵指令）由 WP3 另寫，本檔只引用其名不重複內容。設計依據：`notes/site-internal/dd/_v16_design_spec_20260903.md`（下稱「設計稿」）。

---

## 北極星（v15.0 拍板，report-facing 語意零變更）

目標＝找到真值得長期投資的公司：獲利好且獲利品質好；ROIC 好且持續期長；產業結構與護城河都好——好價格是加分。生意決定買不買，價格決定何時買。完整文字見 `references/v16/judgment-rules.md` §0（Writer 唯一讀本，本檔不重複）。

---

## 一、兩步制流程總覽（v16.1）

```
第一步  Stage 0 證據包（sonnet fan-out，平行，零判斷）
  0a 數字包（沿用 data-collection.md 既有 spawn 模板，含財報時效閘）
     ＋ dd_numbers_extra.py 先產六個結構化欄位：numbers.latest_quarter_kpis／
       valuation_history／peer_financials／momentum_26w（含 rsi14_usable）／
       edgar_concentrations／consensus_revision（含 stale 旗標）
  0b 覆蓋矩陣：archetype 決定軸清單（references/v16/coverage-axes.md），
     每 3-5 軸一子 agent，回傳 sourced findings，orchestrator 只 merge 不讀內容
  0c 事件掃描：併入 0b 的 major_events 軸（QC-19 五組查詢已模板化在 coverage-axes.md）
  0d 前份 DD 三區塊＋知識帳本＋canonical ID 事實區塊：dd_prior.py（零 LLM 腳本擷取）
  0e 逐字稿：transcripts_for_dd.py 產路徑清單；讀取歸 Writer（親讀不外包）
  輸出：.dd_build/{T}_{D}.evidence.json
  **閘：validate_evidence.py --strict 過才准開寫**——FAIL 就回補該軸資料，不得帶缺口進第二步

第二步  Writer 判斷＋呈現＋自查（單一 agent、單一 context；--writer-model，預設 fable；不上網）
  讀：evidence.json ＋ 逐字稿 must_read[] ＋ judgment-rules.md ＋ archetype 對應 reference
      ＋ render-rules.md（動筆散文前才載入）
  ① 判斷物：judgment.json（一次 Write）、scenario.json（一次 Write）
     機械（一次複合 Bash）：dd_scenario.py → dd_decision.py run → validate_judgment.py
     --evidence；FAIL 只准改欄位重跑，≤3 輪
  ② 呈現（三支全過才開始）：gen_dd_tables.py 產表 → dd_prose_budget.py 算每段目標 bytes
     → 每段 .dd_build/{T}_{D}.prose/{sid}.html 一次 Write（禁 Edit，表格計入分子）
     → render_dd.py --assemble ... -o {OUT_HTML}
     → 六支驗證：validate_prose／dd_sections bytes／dd_sections leaks／qc.py／
       validate_dd_meta／verify_dd_math（HTML 版）；未過只重寫該段一次
  ③ 交稿前自查（取代原 critic）：QC-41 四軸＋覆蓋面掃描（缺軸即 🔴）＋量化模組完整性抽查
     ＋數字新鮮度＋散文一致性，逐條 🟢/🟡/🔴 打勾；🔴 先改該欄位或重寫該段一次再交稿，
     自查表為回報必要欄位

（流程外）事後抽查：前三份上站後 orchestrator 另 spawn 一次冷讀（模型與 writer 不同），
  只計判斷級 🔴 數、不修補，存 notes/site-internal/dd/_audit_{T}_{D}.md，只餵退場訊號
```

Orchestrator（opus）只做：spawn、傳檔名、讀 validator 輸出、commit。**不讀任何報告內容進自己的 context**（設計稿 §2 硬性原則）。

---

## 二、條件載入路由表

| 讀者 | 時點 | 必 Read | 說明 |
|---|---|---|---|
| Stage 0b 子 agent | 派工時 | `references/v16/evidence-pack.md`（spawn 模板＋規則五條）＋ `references/v16/coverage-axes.md`（軸清單 JSON，唯一權威） | 不讀 judgment-rules.md（不做判斷，只採集） |
| Writer | 一律 | `references/v16/judgment-rules.md`（always-on，≤40KB） | 唯一判斷規則檔，不重述 schema |
| Writer | archetype∈循環子型 | `references/cyclical-lens.md` | QC-42 全文＋附錄 B 位置錶族 |
| Writer | archetype∈{金融、未獲利、轉機、受監管公用} | `references/archetype-gatesets.md` | QC-44/45/46 全文 |
| Writer | 寫 §5.R 前 | `references/roic-durability.md` | 一律 |
| Writer | Part II 判斷前 | `references/judgment-playbook.md` | QC-53 觸發索引，命中逐條實答 |
| Writer | 填 appendix_a 四欄前 | `references/timing-appendix.md` | 未讀不得填 |
| Writer | 90 天內裁決翻面 | evidence.json.prior_dd.triggers（已含在 evidence 包，非另讀檔） | QC-49 |
| Writer | 交稿前自查 | 無須另讀檔——自查表 ①-⑧ 已逐條寫進 spawn prompt（`references/v16/agent-prompts.md` (b) 第三階段），條文語意沿 `critic-gates.md` QC-41 原文 | 流程內無獨立 critic；`critic-gates.md` 僅留作事後抽查與規則沿革參照 |
| Writer | 判斷四支全過、動筆散文前 | `references/v16/render-rules.md`（always-on，≤15KB） | 唯一呈現規則檔；§0 一次寫條款為硬規則 |
| Writer | 寫 prose 前 | `gen_dd_tables.py` 產出的 `TABLES_DIR/*.html` 清單＋`dd_prose_budget.py` 目標 bytes 表 | 機械先行，散文只讀產物不重算、不重寫表格 |
| orchestrator | 改規則前 | `references/changelog.md`＋`knowledge/rule_ledger.md` | 判斷類規則增刪同步 rule_ledger |
| orchestrator | delta 複審請求 | `references/delta-refresh.md`（**v16 delta 模式未定案**，見設計稿 §8 待決 4；命中時暫時回退 v15.2 全套或人工裁定） | 已知缺口，非本輪範圍 |

**不進 Writer context 的檔**：`decision-layer.md`（矩陣已由 `dd_decision.py` 機械翻譯，Writer 只填 `decision_inputs`）、`html-output.md`（v15.2 legacy BODY 契約，已被 `render-rules.md` 取代）、`dd-meta-schema.md`（權威已轉移 `judgment.schema.json`＋`judgment-to-ddmeta.md`）。

---

## 三、Stage 0／Writer／orchestrator 契約

> 完整 spawn prompt 全文（含逐字讀寫範圍、禁令、回報格式）已由 WP3 草擬於 `references/v16/agent-prompts.md`（(a) Stage 0b 子 agent／(b) Writer，含第三階段「交稿前自查」；(c) 是流程外事後抽查說明，不是派工模板。v16.1 起無 critic／patch／呈現模板）。本節只列**腳本名、CLI 旗標、驗證鏈順序**這個「契約骨架」，不重複 prompt 全文；`agent-prompts.md` 若與本節腳本旗標描述有出入，以腳本 `--help` 實際輸出為準。

### Stage 0
| 步驟 | 指令 |
|---|---|
| 0a 結構化數字欄位 | `python3 scripts/dd_numbers_extra.py {T} {D} --peers "{PEERS}" --out .dd_build/evidence_parts/numbers_extra.json`（零 LLM；產 `latest_quarter_kpis`／`valuation_history`／`peer_financials`／`momentum_26w`／`edgar_concentrations`／`consensus_revision`），再 spawn 採集 agent 補 KPI 缺項 |
| 0b 軸展開 | `python3 scripts/dd_evidence.py axes --archetype "{ARCHETYPE}" --ticker {T} --company "{C}" --industry "{I}" --customers "{CUST}" [--segments a,b,c] --json` |
| 0b 骨架初始化 | `python3 scripts/dd_evidence.py init {T} {D} --archetype "{ARCHETYPE}"` |
| 0b merge | `python3 scripts/dd_evidence.py merge .dd_build/{T}_{D}.evidence.json .dd_build/evidence_parts/{part}.json`（逐一） |
| **開寫前置閘** | `python3 scripts/validate_evidence.py .dd_build/{T}_{D}.evidence.json --strict --report`；**FAIL 就回補該軸資料（對該軸重 spawn），不得帶缺口進第二步**——兩步制下 Stage 0 是唯一的資料把關點 |
| 0d 前份/帳本/ID | `python3 scripts/dd_prior.py {T} --date {D} --out .dd_build/evidence_parts/prior.json`（零 LLM） |

### Writer（`--writer-model {fable|sonnet|opus}`，**預設 fable**）
判斷物寫完，一次複合 Bash：
```
python3 scripts/dd_scenario.py .dd_build/{T}_{D}.scenario.json --html .dd_build/{T}_{D}.tables/e11.html --meta .dd_build/{T}_{D}.scenario_meta.json
python3 scripts/dd_decision.py run .dd_build/{T}_{D}.judgment.json --html .dd_build/{T}_{D}.tables/audit.html --json .dd_build/{T}_{D}.judgment.json
python3 scripts/validate_judgment.py .dd_build/{T}_{D}.judgment.json --report --evidence .dd_build/{T}_{D}.evidence.json
```
FAIL 只准改 `judgment.json`／`scenario.json` 欄位重跑，≤3 輪。三支全過才進呈現：
```
python3 scripts/gen_dd_tables.py .dd_build/{T}_{D}.judgment.json --out .dd_build/{T}_{D}.tables --scenario-html .dd_build/{T}_{D}.tables/e11.html --scenario-meta .dd_build/{T}_{D}.scenario_meta.json
python3 scripts/dd_prose_budget.py .dd_build/{T}_{D}.judgment.json --tables .dd_build/{T}_{D}.tables
（Writer 依目標 bytes 表寫 .dd_build/{T}_{D}.prose/{sid}.html，每段一次 Write，禁 Edit）
python3 scripts/render_dd.py --assemble .dd_build/{T}_{D}.prose --tables .dd_build/{T}_{D}.tables --judgment .dd_build/{T}_{D}.judgment.json -o {OUT_HTML}
python3 scripts/validate_prose.py .dd_build/{T}_{D}.prose --judgment .dd_build/{T}_{D}.judgment.json --evidence .dd_build/{T}_{D}.evidence.json
python3 scripts/dd_sections.py bytes {OUT_HTML}
python3 scripts/dd_sections.py leaks {OUT_HTML}
python3 scripts/qc.py {OUT_HTML}
python3 scripts/validate_dd_meta.py {OUT_HTML} --report
python3 scripts/verify_dd_math.py {OUT_HTML}
```
`{OUT_HTML}`＝dry-run 時 `.dd_build/DD_{T}_{D}.v16dryrun.html`、正式時 `docs/dd/DD_{T}_{D}.html`。任一 FAIL：**只重寫命中的 `prose/{sid}.html`（整檔 Write）→ 重新組裝 → 重跑**，每段最多重寫一次，不動判斷物。六支閘全過後，writer 再跑第三階段「交稿前自查」（自查表 ①-⑧ 見 `agent-prompts.md` (b)），🔴 先修再交，自查表為回報必要欄位。

### Orchestrator（ddreport v3，WP3 另寫，本檔只引用鏈順序）
```
koyfin 增量下載（0e，沿用 v15.2）→ dd_numbers_extra → Stage 0 fan-out → validate_evidence --strict
→ Writer（判斷三支 → 產表／算預算 → 散文 → 組裝 → 六支閘 → 交稿前自查）
→ python scripts/update_dd_index.py → qc.py → commit
（流程外，前三份）事後冷讀抽查 → notes/site-internal/dd/_audit_{T}_{D}.md，只計數不修補
```
Orchestrator 全程只看 validator 輸出與 writer 的自查表，不讀報告內容、不讀 prose 段落。

---

## 四、Token 紀律（v16.1 兩步制）

**第一槓桿不變但機制改變**：v15.2 的槓桿是「writer 對輸出檔禁 Edit、驗證用腳本定位」；v16.1 把它推到極限——**每一次交接都要重付一次 context**，所以把交接次數壓到一次：
- **兩步而非五段**：Stage 0（sonnet fan-out）→ Writer（Fable，判斷＋呈現＋自查同一 context）。v16.0 兩段式的成本全在交接——呈現層得把整份判斷物重讀一次（DELL 71.9M／SNOW 40.6M），patch agent 兩輪再重付一次（20.4M／25.4M）；這兩筆在兩步制下歸零。
- 段落級修補仍在：機械閘 FAIL 只重寫命中的 `prose/{sid}.html`（單段幾 KB），不是 80KB 散文的 extract/replace。
- 規則不再每份重讀 225KB（v15.2 每份 writer 先讀 SKILL.md 125.8KB＋7-8 份 references）：Writer 只讀 `judgment-rules.md`（≤40KB）＋條件載入的 archetype reference＋動筆前的 `render-rules.md`（≤15KB）。

**Writer 端硬紀律**（寫進 spawn prompt，見 `agent-prompts.md` (b)）：①不重讀自己寫過的檔（judgment／scenario／prose／tables 一律以 context 內版本為準，要看結果就看腳本輸出）；②不 Read 任何 `docs/dd/`（前份三區塊已在 `evidence.json.prior_dd`）；③禁 WebSearch／WebFetch；④每檔一次 `Write`，prose 目錄一律禁 `Edit`；⑤散文動筆前先看 `dd_prose_budget.py` 的目標 bytes 表，不邊寫邊湊篇幅。

**外包界線不變**：有唯一正確答案、派工前就能定義清楚的查證＝Stage 0（採集/覆蓋矩陣）；需要先知道自己在找什麼才看得見答案的閱讀（逐字稿、前份 DD 假設觸發器、ID 事實區塊）與判斷端（archetype 換尺、moat_trend 方向、QC-39 兩閘裁定）一律 Writer 自讀自判，不外包。

**模型分工（v16.1 定版）**：

| 段 | 模型 | 說明 |
|---|---|---|
| Stage 0 收資料 | **sonnet** | fan-out 平行；`validate_evidence.py --strict` 過才准開寫 |
| Writer 判斷＋呈現＋自查 | **Fable** | `--writer-model`，預設 `fable`（可改 `sonnet`／`opus`） |
| 流程內 critic | **無** | 原七軸 checklist 改為 writer 交稿前自查；驗收改事後抽查 |
| 事後抽查（流程外，前三份） | 與 writer 不同模型（Fable writer → opus） | 只計判斷級 🔴 數，不修補、不阻斷發布 |

repo CLAUDE.md「writer 與 critic 永不同模型」的鐵律在 v16.1 試點期以**流程外抽查**的形式維持（跨模型的眼睛沒有消失，只是移到上站之後、且不再是 gate）——此為明文推翻既有拍板，理由與退場訊號見設計稿 §13。

**機械輪次批次化三條**（每個 spawn prompt 末尾附帶，逐字沿用 v15.2）：①定位先於動手，一輪複合 grep/查詢取齊；②同檔機械性修改 ≥5 處禁逐個修補；③Bash 驗證併成單條複合指令，驗證輪次 ≤3 輪。

**成本模型**：v15.2 同檔實測 SNOW 88M／DELL 138M；v16.0 兩段式實測 SNOW 112M／DELL 123M。v16.1 估計 **Stage 0 15-25M（sonnet）＋Writer（Fable）待實測**（前三份回填）。

**退場訊號（設計稿 §13，三條）**：
1. **覆蓋缺軸 0**（v16.0 兩份皆 0，此為不得倒退的底線）。
2. **前三份上站後事後冷讀抽查，判斷級 🔴 合計為 0 → 永久拿掉本驗收；出現 1 例 → Fable 驗收放回流程內**（恢復流程內 critic gate）。
3. **每份成本 ≤ v15.2 同檔**：SNOW ≤88M、DELL ≤138M。

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
**新增（v16.1）**：三段 token 用量拆解（Stage 0／Writer／事後抽查〔若有〕各自 cache_read，供成本模型回填）＋ `dd_decision.py --check` 與最終 HTML dd-meta 的 `dca_verdict` 是否一致（一致性自我檢查，理論上恆真，若不真代表 `gen_dd_tables.py` 或 `render_dd.py --assemble` 有 bug）。

**回報上限**：≤400 字＋INDEX 行，不複述報告內容，只給路徑／KB／Part I 佔比／§13 裁決與前份對比／3-5 條決策相關變化／自查表 🔴🟡 項／gate 狀態／`dd_sections.py bytes` 表原文。

---

## 六、不做的事（PREREG，同設計稿 §10）

不改任何門檻、機率防線、矩陣語意、dd-meta 欄位語意；不把逐字稿讀取外包成摘要（待決 1 未裁前）；不新建收斂面、不動下游聚合器（`update_dd_index.py`／dd-screener／picks 讀 dd-meta 不變）；不在本輪處理既有 DD 的未跳脫 `<`（另案 batch fix）；**本檔本身不生效**——取代 `SKILL.md` 需先過 WP1 回溯考卷與 WP4 試點驗收，由持有人裁定切換時點。
