---
name: stock-analyst
version: v16.0-draft
released: 2026-09-03
description: "（WP2 draft，未接線、未取代現行 v15.2 SKILL.md）收到股票 ticker 後，以三段式管線（Stage 0 證據包 fan-out → Stage 1 判斷層 → Stage 2 呈現層）產出單一 DD 報告（docs/dd/DD_{TICKER}_{YYYYMMDD}.html，dd-meta schema=v15.0，report-facing 版號凍結不變）。判斷機器（QC-1~QC-54 門檻、決策矩陣 rows 1-10、fail-safe 方向、dd-meta 契約）逐字未動，只重排『誰在什麼 context 做什麼、用什麼格式交接』。北極星、篇幅帶、E1-E12 表格收斂、統一裁決三詞頭銜、四值倉位角色等報告端規格與 v15.2 完全一致。觸發語與 v15.2 相同：『個股分析 {ticker}』『{ticker} DD』/ DD 報告 / 股票研究 / 估值分析 / 『{ticker} dca』『{ticker} 定見』『conviction analysis {ticker}』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』；裸 ticker 與『這檔如何/值不值得研究/先篩一下 {ticker}』不觸發本 skill，改走 stock-screen-v1。"
---

> **本檔狀態**：WP2（規則三分法拆分）交付物之一，**草稿**——尚未通過 WP1 回溯考卷（`dd_decision.py --check-all` 30/30、`gen_dd_tables.py` 反推比對）與 WP4 試點驗收，**不得取代 `.claude/skills/stock-analyst/SKILL.md`**（現行 v15.2，唯一生產版本）。ddreport v3（把本檔的鏈固化成一鍵指令）由 WP3 另寫，本檔只引用其名不重複內容。設計依據：`notes/site-internal/dd/_v16_design_spec_20260903.md`（下稱「設計稿」）。

---

## 北極星（v15.0 拍板，report-facing 語意零變更）

目標＝找到真值得長期投資的公司：獲利好且獲利品質好；ROIC 好且持續期長；產業結構與護城河都好——好價格是加分。生意決定買不買，價格決定何時買。完整文字見 `references/v16/judgment-rules.md` §0（Stage 1 唯一讀本，本檔不重複）。

---

## 一、三段式流程總覽

```
Stage 0  證據包（sonnet fan-out，平行，零判斷）
  0a 數字包（沿用 data-collection.md 既有 spawn 模板，含財報時效閘）
  0b 覆蓋矩陣（新）：archetype 決定軸清單（references/v16/coverage-axes.md），
     每 3-5 軸一子 agent，回傳 sourced findings，orchestrator 只 merge 不讀內容
  0c 事件掃描：併入 0b 的 major_events 軸（QC-19 五組查詢已模板化在 coverage-axes.md）
  0d 前份 DD 三區塊＋知識帳本＋canonical ID 事實區塊：dd_prior.py（零 LLM 腳本擷取）
  0e 逐字稿：transcripts_for_dd.py 產路徑清單；讀取歸 Stage 1（親讀不外包，見待決 1）
  輸出：.dd_build/{T}_{D}.evidence.json（validator：validate_evidence.py）

Stage 1  判斷（單一 agent；模型旗標 --judge-model，預設 sonnet；不上網、不寫 HTML）
  讀：evidence.json ＋ 逐字稿 must_read[] ＋ references/v16/judgment-rules.md（always-on，
      唯一判斷規則檔）＋ archetype 對應 reference（條件載入，見下方路由表）
  寫：judgment.json（一次 Write）、scenario.json（一次 Write）
  機械：dd_scenario.py → dd_decision.py → validate_judgment.py → verify_dd_math.py
        FAIL 只准改欄位重跑，≤3 輪
  critic（跨模型冷讀，orchestrator spawn，非 Stage 1 自己 spawn）：
      讀 evidence.json＋judgment.json（不讀散文），觸發條件見 judgment-rules.md §16

Stage 2  呈現（sonnet；讀 evidence.json＋judgment.json，只鋪陳不判斷）
  機械先行：gen_dd_tables.py 由 judgment.json 生成 dashboard/E2/E11/E12/dd-meta/appA 表
  agent：寫 §1-§14 散文到 .dd_build/{T}_{D}.prose/{sid}.html（每段一次 Write）
  組裝：render_dd.py --assemble PROSE_DIR --tables TABLES_DIR -o docs/dd/DD_{T}_{D}.html
  閘：dd_sections.py leaks → validate_prose.py → dd_sections.py bytes →
      verify_dd_math.py → validate_dd_meta.py --report → qc.py
  輕 critic（可選旗標，預設關）：只核 QC-54 白話開場一致性
```

Orchestrator（opus）只做：spawn、傳檔名、讀 validator 輸出、決定是否 re-gate、commit。**不讀任何報告內容進自己的 context**（設計稿 §2 硬性原則）。

---

## 二、條件載入路由表

| 讀者 | 時點 | 必 Read | 說明 |
|---|---|---|---|
| Stage 0b 子 agent | 派工時 | `references/v16/evidence-pack.md`（spawn 模板＋規則五條）＋ `references/v16/coverage-axes.md`（軸清單 JSON，唯一權威） | 不讀 judgment-rules.md（不做判斷，只採集） |
| Stage 1 | 一律 | `references/v16/judgment-rules.md`（always-on，≤40KB） | 唯一判斷規則檔，不重述 schema |
| Stage 1 | archetype∈循環子型 | `references/cyclical-lens.md` | QC-42 全文＋附錄 B 位置錶族 |
| Stage 1 | archetype∈{金融、未獲利、轉機、受監管公用} | `references/archetype-gatesets.md` | QC-44/45/46 全文 |
| Stage 1 | 寫 §5.R 前 | `references/roic-durability.md` | 一律 |
| Stage 1 | Part II 判斷前 | `references/judgment-playbook.md` | QC-53 觸發索引，命中逐條實答 |
| Stage 1 | 填 appendix_a 四欄前 | `references/timing-appendix.md` | 未讀不得填 |
| Stage 1 | 90 天內裁決翻面 | evidence.json.prior_dd.triggers（已含在 evidence 包，非另讀檔） | QC-49 |
| critic（QC-41/48/50/51 任一觸發） | orchestrator spawn 時 | `references/critic-gates.md`（**已知落差**：文字仍寫「讀 dd_sections.py text」，v16 應改讀 evidence.json+judgment.json——WP3 更新前先照 spawn prompt 實際指示為準，見 `references/v16/agent-prompts.md`） | 查證預算 ≤10／合併 ≤14 輪不變 |
| Stage 2 | 一律 | `references/v16/render-rules.md`（always-on，≤15KB） | 唯一呈現規則檔 |
| Stage 2 | 產表格前 | `gen_dd_tables.py` 已產出的 `TABLES_DIR/*.html` 清單 | 機械先行，Stage 2 只讀產物不重算 |
| orchestrator | 改規則前 | `references/changelog.md`＋`knowledge/rule_ledger.md` | 判斷類規則增刪同步 rule_ledger |
| orchestrator | delta 複審請求 | `references/delta-refresh.md`（**v16 delta 模式未定案**，見設計稿 §8 待決 4；命中時暫時回退 v15.2 全套或人工裁定） | 已知缺口，非本輪範圍 |

**不進 Stage 1/2 context 的檔**：`decision-layer.md`（矩陣已由 `dd_decision.py` 機械翻譯，Stage 1 只填 `decision_inputs`）、`html-output.md`（v15.2 legacy BODY 契約，已被 `render-rules.md` 取代）、`dd-meta-schema.md`（權威已轉移 `judgment.schema.json`＋`judgment-to-ddmeta.md`）。

---

## 三、Stage 0/1/2 與 critic／patch／orchestrator 契約

> 完整 spawn prompt 全文（含逐字讀寫範圍、禁令、回報格式）已由 WP3 草擬於 `references/v16/agent-prompts.md`（(a) Stage 0b 子 agent／(b) Stage 1／(c) Stage 1 critic／(d) patch agent／(e) Stage 2）。本節只列**腳本名、CLI 旗標、驗證鏈順序**這個「契約骨架」，不重複 prompt 全文；`agent-prompts.md` 若與本節腳本旗標描述有出入，以腳本 `--help` 實際輸出為準。

### Stage 0
| 步驟 | 指令 |
|---|---|
| 0b 軸展開 | `python3 scripts/dd_evidence.py axes --archetype "{ARCHETYPE}" --ticker {T} --company "{C}" --industry "{I}" --customers "{CUST}" [--segments a,b,c] --json` |
| 0b 骨架初始化 | `python3 scripts/dd_evidence.py init {T} {D} --archetype "{ARCHETYPE}"` |
| 0b merge | `python3 scripts/dd_evidence.py merge .dd_build/{T}_{D}.evidence.json .dd_build/evidence_parts/{part}.json`（逐一） |
| 0b 驗證 | `python3 scripts/validate_evidence.py .dd_build/{T}_{D}.evidence.json --report`；FAIL 缺軸→對該軸重 spawn（≤2 次，同 QC-41 fail-safe 精神） |
| 0d 前份/帳本/ID | `python3 scripts/dd_prior.py {T} --date {D} --out .dd_build/evidence_parts/prior.json`（零 LLM） |

### Stage 1
`--judge-model {sonnet|opus|fable}` 旗標（設計稿待決 3：前兩份 sonnet、第三份 A/B 測 Fable）。輸出後跑：
```
python3 scripts/dd_scenario.py .dd_build/{T}_{D}.scenario.json --html .dd_build/{T}_{D}.tables/e11.html --meta .dd_build/{T}_{D}.scenario_meta.json
python3 scripts/dd_decision.py run .dd_build/{T}_{D}.judgment.json --html .dd_build/{T}_{D}.tables/audit.html --json .dd_build/{T}_{D}.decision_out.json
python3 scripts/validate_judgment.py .dd_build/{T}_{D}.judgment.json --report
python3 scripts/verify_dd_math.py .dd_build/{T}_{D}.judgment.json
```
FAIL 只准改 `judgment.json`／`scenario.json` 欄位重跑，≤3 輪。

### Critic（跨模型冷讀，orchestrator spawn；模型鐵律：Stage 1 為 sonnet 時 critic 必為 opus）
輸入＝evidence.json＋judgment.json（合計約 40-60KB，不讀散文）。觸發條件、七軸 checklist、查證預算見 `judgment-rules.md` §16＋`critic-gates.md`。輸出 FINDINGS 表的段落 id 改用 **JSON 路徑**（如 `moat.roic_durability.reinvest_rate`），供 patch agent `jq` 直接定位。

### Patch（sonnet，乾淨 context）
輸入＝FINDINGS＋受影響 JSON 子樹（orchestrator 用 `jq` 抽出，不整份貼）。動作＝改子樹→merge→重跑 Stage 1 的四支驗證腳本。**不碰散文**（若 FINDINGS 涉及呈現層措辭，走 Stage 2 段落級重寫，不算 patch 範圍）。一輪 ≤10 輪；re-gate 另 spawn 乾淨 agent。

### Stage 2
```
python3 scripts/gen_dd_tables.py .dd_build/{T}_{D}.judgment.json --out .dd_build/{T}_{D}.tables --scenario-html .dd_build/{T}_{D}.tables/e11.html --scenario-meta .dd_build/{T}_{D}.scenario_meta.json
（Stage 2 agent 寫 .dd_build/{T}_{D}.prose/{sid}.html，每段一次 Write）
python3 scripts/render_dd.py --assemble .dd_build/{T}_{D}.prose --tables .dd_build/{T}_{D}.tables --judgment .dd_build/{T}_{D}.judgment.json -o docs/dd/DD_{T}_{D}.html
python3 scripts/dd_sections.py leaks docs/dd/DD_{T}_{D}.html
python3 scripts/validate_prose.py .dd_build/{T}_{D}.prose --judgment .dd_build/{T}_{D}.judgment.json
python3 scripts/dd_sections.py bytes docs/dd/DD_{T}_{D}.html
python3 scripts/verify_dd_math.py docs/dd/DD_{T}_{D}.html
python3 scripts/validate_dd_meta.py --report
python3 scripts/qc.py docs/dd/DD_{T}_{D}.html
```
任一 FAIL：`dd_sections.py extract FILE ID` 取段→重寫該 `prose/{sid}.html`→重新組裝→重跑；只重寫命中的段落，不動判斷物。驗證輪次 ≤3。

### Orchestrator（ddreport v3，WP3 另寫，本檔只引用鏈順序）
```
koyfin 增量下載（0e，沿用 v15.2）→ Stage 0 fan-out → validate_evidence
→ Stage 1 → 四支驗證 → critic → patch → [re-gate]
→ gen_dd_tables → Stage 2 → 閘 → [輕 critic]
→ python scripts/update_dd_index.py → qc.py → commit
```
Orchestrator 全程只看 validator 輸出與 FINDINGS 表，不讀報告內容、不讀 prose 段落。

---

## 四、Token 紀律（v16 版）

**第一槓桿不變但機制改變**：v15.2 的槓桿是「writer 對輸出檔禁 Edit、驗證用腳本定位」；v16 把這個原則往前推一層——**修補成本從來源就等於 context 大小 × 修補輪數**，而 v16 讓每個修補動作的「context 大小」結構性變小：
- Stage 1 修補只改 JSON 子樹（幾 KB），不是 80KB 散文的 extract/replace。
- Stage 2 修補只重寫命中的 `prose/{sid}.html`（單段幾 KB），不動判斷物、不動其餘段落。
- 規則不再每份重讀 225KB（v15.2 每份 writer 先讀 SKILL.md 125.8KB＋7-8 份 references）：Stage 1 只讀 `judgment-rules.md`（≤40KB）＋條件載入的 archetype reference；Stage 2 只讀 `render-rules.md`（≤15KB）。

**外包界線不變**：有唯一正確答案、派工前就能定義清楚的查證＝Stage 0（採集/覆蓋矩陣）；需要先知道自己在找什麼才看得見答案的閱讀（逐字稿、前份 DD 假設觸發器、ID 事實區塊）與判斷端（archetype 換尺、moat_trend 方向、QC-39 兩閘裁定）一律 Stage 1 自讀自判，不外包。

**模型鐵律不變**：判斷層與冷讀 critic 永不同模型；呈現層可與判斷層同模型（它不做判斷）。

**機械輪次批次化三條**（每個 spawn prompt 末尾附帶，逐字沿用 v15.2）：①定位先於動手，一輪複合 grep/查詢取齊；②同檔機械性修改 ≥5 處禁逐個修補；③Bash 驗證併成單條複合指令，驗證輪次 ≤3 輪。

**成本模型**（牌價估計，設計稿 §7；WP4 試點需回填實測）：v15.2 三份實測合計 88-130M token；v16 估計（sonnet 判斷層）Stage 0 15-25M＋Stage 1 10-20M＋critic 3-5M＋patch 2-5M＋Stage 2 15-25M ≈ 合計 45-80M，**退場訊號＝合計未較 v15.2 降 ≥40%、或 critic 首輪 🔴 未較 5-8 降 ≥50% → 回 v15.2 檢討**（WP4 驗收條件，設計稿 §9）。

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
**新增（v16）**：五段 token 用量拆解（Stage 0／Stage 1／critic／patch／Stage 2 各自 cache_read，供 WP4 成本模型回填）＋ `dd_decision.py --check` 與最終 HTML dd-meta 的 `dca_verdict` 是否一致（一致性自我檢查，理論上恆真，若不真代表 `gen_dd_tables.py` 或 `render_dd.py --assemble` 有 bug）。

**回報上限**：≤400 字＋INDEX 行，不複述報告內容，只給路徑／KB／Part I 佔比／§13 裁決與前份對比／3-5 條決策相關變化／未解 critic 項／gate 狀態／`dd_sections.py bytes` 表原文。

---

## 六、不做的事（PREREG，同設計稿 §10）

不改任何門檻、機率防線、矩陣語意、dd-meta 欄位語意；不把逐字稿讀取外包成摘要（待決 1 未裁前）；不新建收斂面、不動下游聚合器（`update_dd_index.py`／dd-screener／picks 讀 dd-meta 不變）；不在本輪處理既有 DD 的未跳脫 `<`（另案 batch fix）；**本檔本身不生效**——取代 `SKILL.md` 需先過 WP1 回溯考卷與 WP4 試點驗收，由持有人裁定切換時點。
