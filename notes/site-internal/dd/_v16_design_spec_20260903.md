# stock-analyst v16 設計規格草案（流程重建：證據 → 判斷 → 呈現三段式；判斷機器仍凍結）

> 狀態：**草案，待持有人裁定**（2026-09-03）。前身：`_v15_2_design_spec_20260903.md`（v15.2 只改流程與機械閘，writer 仍是單一巨石 agent）。本稿把 writer 拆成三段、中間用結構化資料接，讓修補不再重付整個 context，並把「覆蓋面」從 writer 自覺變成 validator 輸入。
> 硬邊界：判斷機器（QC 門檻、決策矩陣 rows 1–10、fail-safe 方向、dd-meta 契約、critic 觸發條件）**一字不動**，PREREG 凍結至 2026-10 校準輪；本稿只重排「誰在什麼 context 裡做什麼、用什麼格式交接」。

---

## 0. 證據摘要（WHY）

三份 v15.2 實跑（2026-09-03，session jsonl 逐輪加總 cache_read）：

| | AVGO | SNOW | DELL |
|---|---|---|---|
| writer（sonnet） | 48M／151 輪 | 61M／199 輪（Edit 9） | **107M／309 輪（Edit 30、Read 15）** |
| critic（opus，兩輪） | 6.3M | 5.3M | 7.0M |
| patch（sonnet，兩輪） | **150M**（同 agent 跨兩輪） | 21M | 15M＋R2 |
| critic 首輪 🔴 | 8 | 7 | 5 |
| 整軸覆蓋缺口 | 1（Apple） | 1（法規／資料主權） | 2（客戶集中度、關稅 §232） |

四個結構性結論：
1. **修補成本＝context 大小 × 修補輪數**。DELL writer 107M 中 64M 發生在 part 檔寫完之後（30 次 Edit＋去讀 render_dd.py／dd_sections.py 原始碼）。單一巨石 agent 的任何一處小修都重付 500k context。
2. **規則佔 context 大頭**。writer 每份先讀 SKILL.md（125.8KB）＋7–8 份 references（約 100KB），cache 建立 1.2–1.5M；這些文字絕大多數是「檢查」（三處同源、表格上限、跳脫、bytes、leaks），不是「判斷」。
3. **整軸缺口三份三中**。QC-39 三軸與 critic ⑤ 覆蓋面掃描都寫在規則裡，但「哪些軸必須查」從未成為 writer 的**輸入**；critic 抓到後 patch 再補，等於每份都付一次「先漏再補」。
4. **critic 便宜且有效**（每份 5–7M、$3 上下），抓到的 🔴 中約半數是 writer 自己看不見的（財報前價格、Databricks 數字、`<` 截斷、觸發器棘輪）；三個純機械項已於今日轉成閘（財報時效、Bull 退化、未跳脫 `<`）。剩下的 🔴 類型＝覆蓋缺口、sourced 數字錯、決策層自洽（rearm 互斥／棘輪）。

## 1. 總則

- **判斷機器零變動**：QC-1～QC-54 的門檻、決策矩陣、archetype 路由、critic gate 觸發條件、dd-meta `schema:"v15.0"` 全部凍結。本稿把它們**搬家**（散文 → validator／腳本／JSON 欄位），不改語意。搬家後必過「回溯考卷」（§9）。
- **三段一契約**：證據包（evidence pack）→ 判斷物（judgment）→ 呈現（render）。每段的輸出是**可驗證的檔案**，下一段只讀檔案，不讀上一段的 context。
- **數字只有一個居所**：任何進裁決的數字只存在於判斷物 JSON，表格與 dd-meta 由腳本生成。「三處一致」從規則變成結構。
- **模型鐵律不變**：判斷層與冷讀 critic 永不同模型；呈現層可與判斷層同模型（它不做判斷）。
- **可 A/B**：判斷層模型（sonnet／opus／Fable）是一個旗標，因為它的輸入輸出都小，換模型的成本可量。

## 2. 架構

```
Stage 0  證據包（sonnet fan-out，平行）
  ├─ 0a 數字包（現有 data-collection.md 採集 agent，含財報時效閘）
  ├─ 0b 覆蓋矩陣（新）：依 archetype 固定軸清單，每軸一個搜尋子任務 → sourced 發現 或 明確「查無」
  ├─ 0c 事件掃描（QC-19 五組查詢，現有，併入 0b 的「事件」軸）
  ├─ 0d 前份 DD 三區塊（QC-17/18 grep 擷取，腳本化）＋ 知識帳本 q.py ＋ canonical ID 事實區塊（QC-52 Stage 1）
  └─ 0e 逐字稿：路徑清單（transcripts_for_dd.py）；**讀取歸判斷層**（見 §8 待決 1）
  輸出：.dd_build/{T}_{D}.evidence.json（validator：validate_evidence.py）

Stage 1  判斷物（單一 agent；模型旗標；不上網、不寫 HTML）
  輸入：evidence.json ＋ 逐字稿 .md ＋ 判斷規則精簡版（judgment-rules.md，目標 ≤35KB）
  輸出：.dd_build/{T}_{D}.judgment.json（validator：validate_judgment.py）
        ＋ .dd_build/{T}_{D}.scenario.json（現有 dd_scenario.py 契約）
  機械：dd_scenario.py → dd_decision.py（矩陣路由腳本化，輸出 dca_verdict／role／命中 row／執行語骨架）
        → verify_dd_math.py（改讀 judgment.json）
  critic（跨模型冷讀）：讀 evidence.json ＋ judgment.json（合計約 40–60KB），FINDINGS 對準 JSON 欄位；
        patch＝改欄位 → 重跑三支腳本。**不再對 80KB 散文做 extract/replace。**

Stage 2  呈現（sonnet；讀 evidence.json ＋ judgment.json；只鋪陳不判斷）
  機械先行：gen_dd_tables.py 由 judgment.json 生成 dashboard／E1／E2／E11／E12／dd-meta／appA 表／情境欄
  agent：寫 §1–§14 散文段落到 .dd_build/{T}_{D}.prose/{sid}.html（每段一檔、一次 Write）
  組裝：render_dd.py（擴充：吃 prose/ 目錄＋生成表格 → 單一 HTML）
  閘：dd_sections.py bytes／leaks（含未跳脫 <）、qc.py、validate_dd_meta.py
  修補：只重寫超標或命中的那一段檔（prose 段落級，不動判斷物）
  輕 critic（可選）：只核白話開場與敘事是否與判斷物一致（QC-54 ⑦ 軸），不重審判斷
```

Orchestrator（opus）只做：spawn、傳檔名、讀 validator 結果、決定是否 re-gate、commit。**不讀任何報告內容進自己的 context。**

## 3. 交接物 schema（草案，validator 為權威；欄名待 WP1 定稿）

### 3.1 `evidence.json`
```
{ "ticker","date","archetype_hint","earnings_recency",
  "numbers": {…數字包全部欄位，含 price_at_dd 與 as-of、共識三年＋快照日、週線狀態機旗標…},
  "coverage": {                       ← 覆蓋矩陣，軸清單由 archetype 決定（見 3.3）
     "<axis_id>": {"status":"found|none|not_applicable",
                   "findings":[{"claim","source","as_of","direction":"+|0|-","affects":["H1","moat","bear",…]}],
                   "queries_run":[…], "note"} },
  "events": {…QC-19 五組結果…},
  "prior_dd": {"path","schema","verdict","role","H":[…],"R":[…],"triggers":[{"id","text","status_now"}]},
  "ledger": {…q.py 輸出的機器欄…},
  "canonical_id": {"theme","as_of","facts":[…只有事實區塊…]},
  "transcripts": {"must_read":[paths],"optional":[paths]}
}
```
**validator 規則**：每個 `coverage.<axis>` 的 `status` 必填；`found` 至少一條帶 `source`＋`as_of` 的 finding；`none` 必附 `queries_run`（≥2 條）；`not_applicable` 必附一句理由。**任一軸缺 key＝FAIL**。這就是 critic ⑤ 覆蓋面掃描的機械版。

### 3.2 `judgment.json`
```
{ "archetype":{"primary","secondary","confidence","fingerprint"},
  "thesis":{"holding_period","H":[{"id","text","2y","5y","10y","threshold","source","drift_rule"}×3],
            "R":[{"id","text","H_ref","clock":"⚡|🔥|🐢","threshold"}×3],
            "single_thing":{…五格…}},
  "industry":{"clock_phase","sd_verdict_source","bargaining":{"up","down","geo"},"profit_pool_dir","tam_table":[…E3 列…]},
  "moat":{"execution","pricing","combined","grade","trend","trend_evidence","spread_table":[…],"threats":[{"level","text","p"}],
          "roic_durability":{"quadrant","checkpoints":[…4…],"roiic","reinvest_rate","endo_ceiling","formula_note"}},
  "growth":{"runway_years","runway_post_y5","seven_questions":[…],"segments":[…E8 列…],"decay_signals":[…10 列…],"trap_rating"},
  "quality":{"three_year":[…],"dupont":[…],"ccc":[…],"buyback":{…},"lumpiness":{…}},
  "governance":{"capalloc_grade","scorecard":[…],"sbc":{…}},
  "valuation":{"tier","peers":[…],"fwd_pe","peg","percentile_5y","val_light","val_light_derivation","targets":{…}},
  "scenario_ref":"{T}_{D}.scenario.json",
  "decision_inputs":{"signal","trap","val","ma","runway_post_y5","moat_trend","moat_grade","capalloc_grade",
                     "valuation_dependent","week26_return","ar","hard_veto_reasons":[…],"soft_veto_reasons":[…]},
  "decision_out": {…由 dd_decision.py 寫入：verdict, role, row_hit, exec_line 骨架, audit_rows…},
  "triggers":[{"n","text","type","maps_to","metric","threshold","action","source_freq","date"}],   ← E12 唯一居所
  "contradictions":[{"axis","side_a","side_b","ruling","evidence_level","settle_metric","if_then":[…]}],
  "premortem":{"blind_spots":[…],"failure_story","second_failure","max_dd":{"lo","hi","path_risk","trigger_time"}},
  "reasoning":{"<module>":"≤3 行推導"}   ← 每個承重數字的 QC-33 三段推導，呈現層原樣鋪進 <div class="reasoning">
}
```
**規則**：所有進裁決的數字只在這裡；dd-meta 由 `gen_dd_tables.py` 從此生成（`kill_metrics`＝triggers 的減碼／清倉／風險列，`rearm_trigger`＝估值 rearm／進場首倉列，`catalysts`＝有 date 列）。

### 3.3 覆蓋矩陣軸清單（依 archetype，WP1 定稿；先列通用＋兩個 archetype 範例）

通用（全 archetype）：競爭份額／新進入者、客戶 second-source 與 in-house、客戶集中度與客戶信用、供需 durability、法規／反壟斷、關稅／出口管制、地緣（生產地與供應鏈單點）、各主要終端市場（依 §3 營收段逐一列）、替代技術、通路／商業模式轉移、資本市場定價（共識 vs guide、目標價 as-of）、重大事件（QC-19）。
循環／商品加：供給紀律與新產能時程、庫存與價格週期位置、上一輪下行的實際價格行為。
未獲利高成長加：NRR／Rule of 40 同業帶、稀釋軌跡、轉正路徑。
金融加：資本／信用週期、監管資本規則變動。

軸清單放 `references/coverage-axes.md`（機器可讀表），由 0b 的 fan-out 直接展開成子任務；`not_applicable` 需理由，避免 agent 用它逃避。

## 4. 新增／改動腳本（WP1）

| 腳本 | 職責 | 取代的散文規則 |
|---|---|---|
| `scripts/validate_evidence.py` | evidence.json schema＋覆蓋矩陣完整性＋as-of 時效（>180 天標記） | critic ⑤、QC-15、QC-39 ①「≥3 query」 |
| `scripts/validate_judgment.py` | judgment.json schema、enum、必填模組（五模組七表的資料是否齊）、內部恆等式（H↔R↔triggers 對映、moat 閘 A、runway↔row 7、QC-49 翻面須引前份觸發器） | QC-7、QC-14、QC-36、QC-37、QC-38 模組閘、QC-49 |
| `scripts/dd_decision.py` | 決策矩陣 rows 1–10 機械路由（max-severity wins）＋ row 4/5 節奏修飾＋ 8a/8b 資格檢核；輸出 verdict／role／row_hit／audit 表；`--check DD.html` 從既有 dd-meta 重算比對 | decision-layer.md 矩陣散文（**語意不動，只是腳本化**） |
| `scripts/gen_dd_tables.py` | 由 judgment.json＋scenario 產物生成 dashboard／E1／E2／E3／E5／E6／E7／E8／E9／E10／E11／E12／dd-meta／appA 表／appB 表 | QC-7 三處同源、E12 同源、html-output.md 模板段 |
| `scripts/render_dd.py`（擴充） | 吃 `prose/` 目錄＋生成表格，依 canonical 順序組裝；表格位置由 section 模板固定 | 現有 render 邏輯不變 |
| `scripts/verify_dd_math.py`（改讀 judgment.json） | 檢查 A–E 不變；新增「judgment ↔ 產出 HTML dd-meta 一致」 | — |
| `scripts/dd_sections.py`／`qc.py` | 不動（bytes／leaks／未跳脫 `<` 已在） | — |

回溯考卷：`dd_decision.py --check` 對現行 30 份 v15 DD 重算 `dca_verdict`／`dca_role`，**必須 30/30 相同**（差異＝腳本翻譯錯，非規則變動）才准上線。

## 5. Agent 契約

### 5.1 Stage 0 採集（sonnet，fan-out）
- 0a 沿用 data-collection.md 模板（含 v15.2.4 財報時效閘）。
- 0b 覆蓋矩陣：orchestrator 依 archetype_hint（前份 DD 或 q.py 給；無則通用清單）展開軸清單，**每軸一個子 agent 或一個 agent 批次跑 3–5 軸**，每軸 ≤3 輪搜尋，回傳該軸 JSON 片段；orchestrator 只 merge 檔案不讀內容。
- 0d 腳本化：`scripts/dd_prior.py` 擷取前份三區塊＋q.py＋ID 事實區塊，寫進 evidence.json（零 LLM）。
- 預算：0a 約 2M、0b 約 8–15 軸 × 1–2M、0d 0。合計 ≤ 25M sonnet。

### 5.2 Stage 1 判斷（模型旗標，預設 sonnet；A/B 用 Fable／opus）
- 讀：evidence.json、逐字稿必讀清單（最近四季法說＋高訊號會議稿）、`judgment-rules.md`（由 SKILL.md 抽出**只保留判斷類**：archetype 判定、Munger 門檻、護城河二維與 §5.R、成長七問與 runway、trap 四層、QC-39 三軸裁決句、QC-45/44/46 換尺、情境樹機率防線、QC-53 觸發式手冊、§11–§12 判斷句式；目標 ≤35KB）＋ archetype 對應 reference（條件載入不變）。
- 寫：judgment.json（一次 Write）、scenario.json（一次 Write）→ 跑 dd_scenario.py／dd_decision.py／validate_judgment.py／verify_dd_math.py → FAIL 只准改欄位重跑，≤3 輪。
- 禁：WebSearch（證據不足→在該軸 `note` 標「證據包未涵蓋」，不得自搜補洞；orchestrator 可決定回 Stage 0 補一軸）、寫 HTML、Read 任何 docs/dd。
- 回報：≤300 字＋validator 輸出原文。

### 5.3 Critic（跨模型冷讀；判斷層為 sonnet 時 critic＝opus，判斷層為 opus／Fable 時 critic＝sonnet）
- 讀：evidence.json＋judgment.json＋scenario 產物（合計 40–60KB），**不讀散文**。
- 七軸 checklist 不變，但 ⑤ 覆蓋面改為「validator 已擋缺軸，critic 只審 `none`／`not_applicable` 的理由是否成立」；⑥ 量化模組改為對 judgment 欄位驗算；⑦ 白話呈現移到 Stage 2 輕 critic。
- 輸出：FINDINGS 表的「段落 id」欄改為 **JSON 路徑**（如 `moat.roic_durability.reinvest_rate`）；GATE 判準不變。
- 查證預算不變（≤10／合併 ≤14）。

### 5.4 Patch（sonnet，乾淨 context）
- 輸入：FINDINGS＋受影響的 JSON 子樹（orchestrator 用 `jq`／小腳本抽出）＋證據補件。
- 動作：改子樹 → merge → 重跑三支腳本。一輪 ≤10 輪。**不碰散文。**
- re-gate 規則沿用 v15.2.1（GATE=FAIL 才 re-gate；第二輪另 spawn）。

### 5.5 Stage 2 呈現（sonnet）
- 讀：evidence.json＋judgment.json（含 reasoning 段）＋`render-rules.md`（由 html-output.md＋QC-40／QC-54＋分章 byte 預算抽出，≤15KB）＋ `gen_dd_tables.py` 已產出的表格片段清單。
- 寫：`prose/{sid}.html` 每段一次 Write（s1…s14、appA 敘述、revlog）；**段內不得出現判斷物沒有的數字**（validator：正文數字集合 ⊆ judgment 數字集合，容忍格式差）。
- 機械：render_dd.py 組裝 → bytes／leaks／qc.py／validate_dd_meta.py；超標或命中只重寫該段檔。
- 輕 critic（可選，sonnet 或 opus 皆可，因為不涉裁決）：QC-54 ⑦ 三問＋「散文有無與判斷物矛盾」；PASS-with-fixes 直接段落重寫。

### 5.6 Orchestrator／ddreport v3
`koyfin 增量下載（sonnet 0e）→ Stage 0 fan-out → validate_evidence → Stage 1 → 三支腳本 → critic → patch → [re-gate] → gen_dd_tables → Stage 2 → 閘 → [輕 critic] → INDEX／update_dd_index → commit`。orchestrator 全程只看 validator 輸出與 FINDINGS 表。

## 6. 規則遷移地圖（QC-1～QC-54 三分法；WP2 定稿逐條表）

| 去向 | 條文（例） | 落點 |
|---|---|---|
| **validator／腳本**（不再要 LLM 記得） | QC-2/10/24/25（採集旗標）、QC-4（分位公式）、QC-7/14/36/37（同源）、QC-15（時效）、QC-17/18（前份擷取）、QC-21（R:R 假象）、QC-22（漂移）、QC-32（schema）、QC-34/35（漂移門檻）、QC-38（模組／表格／bytes）、QC-40（leaks）、QC-49（翻面須引觸發器）、決策矩陣、E12 同源、財報時效、Bull 退化、未跳脫 `<` | Stage 0/1/2 validators、dd_decision.py、gen_dd_tables.py |
| **判斷規則**（留給 Stage 1 agent） | QC-1/3/5/6/9/11/13/16/19（深查）/20/23/26/27/28/30/31/33/39（三軸裁決）/42–47/50–53、§2–§12 各模組的判準句式、機率防線、archetype 換尺 | `judgment-rules.md`（≤35KB）＋條件載入 references |
| **呈現規則**（留給 Stage 2 agent） | QC-40 文字面、QC-54、html-output 模板、分章預算、白話對照表 | `render-rules.md`（≤15KB） |
| **退役候選**（本稿只提名，2026-10 審計裁） | QC-8（不中斷——由流程保證）、QC-29（已退役）、QC-12（併 QC-39）、附錄 A 品質分六步表中純機械部分（改腳本） | rule_ledger 審計欄 |

## 7. 成本模型（牌價；cache read 為主量，sonnet $0.20/M、opus $0.50/M、Fable $0.25/M；cache 建立 sonnet $2.5/M、Fable $12.5/M；輸出 sonnet $10/M、Fable $50/M）

| 段 | v15.2 實測（SNOW／DELL） | v16 估計（sonnet 判斷層） | v16 估計（Fable 判斷層） |
|---|---|---|---|
| Stage 0 | 2M（併在 writer 內） | 15–25M sonnet ≈ $4 | 同左 |
| Stage 1 判斷 | （writer 61／107M ≈ $12–21＋建立 $4） | 讀 ≈150k、寫 30KB、≤3 輪修：**10–20M** ≈ $3＋建立 $0.5 | 10–20M ≈ $4＋建立 $2＋輸出 $2 |
| critic | 5–7M opus ≈ $3 | 讀 60KB：3–5M opus ≈ $2 | 3–5M sonnet ≈ $1 |
| patch | 15–21M sonnet ≈ $3–4 | 改 JSON：2–5M ≈ $1 | 同左 |
| Stage 2 呈現 | （併在 writer） | 讀 80KB＋寫 80KB 散文、段落級修：**15–25M** ≈ $4 | 同左 |
| **合計** | **$23–32** | **≈ $14–16** | **≈ $17–20** |

省的不是單價，是**修補不再重付整個 context**與**規則不再每份重讀 225KB**。判斷層換 Fable 只多 $3–4，A/B 變得可負擔。

## 8. 待決（持有人裁定，影響 WP 切法）

1. **逐字稿讀法**：現行鐵律「逐字稿由分析 agent 親讀」。v16 判斷層親讀四季法說（約 50k tokens）仍可行，成本進 Stage 1；替代方案是 Stage 0 產「結構化摘錄」（guidance 數字、被迴避的問題、語氣句），判斷層只讀摘錄。**建議維持親讀**（摘錄會丟掉「需要先知道自己在找什麼才看得見」的訊號），僅 optional 會議稿改摘錄。
2. **散文與推理脫節風險**：Stage 2 若只鋪陳，§5／§6 的「產品是推理本身」會變套話。解法＝judgment.json `reasoning` 段強制每模組 ≥3 行，且呈現層對 §5／§6／§11 可「擴寫推理但不得新增數字」。是否接受這個折衷？
3. **判斷層預設模型**：sonnet（延續 2026-08-08 拍板）或藉重建之機直接 A/B。建議：WP 完成後前兩份用 sonnet、第三份用 Fable，比 critic 首輪 🔴 數與整軸缺口（v16 下缺軸應為 0，比較的是 sourced 數字錯與決策自洽）。
4. **delta 複審**：v16 下 delta＝只重跑 Stage 0（證據更新）＋ Stage 1 的 diff 模式（判斷物欄位級比對，翻面仍禁）；是否納入本輪或留 v16.1。
5. **critic 是否保留兩層**：判斷層 critic（必要）＋呈現層輕 critic（可選）。建議輕 critic 先做旗標，預設關，前三份開著量。

## 9. 工作包與驗收

| WP | 內容 | 驗收 |
|---|---|---|
| WP1 腳本 | validate_evidence／validate_judgment／dd_decision／gen_dd_tables／render_dd 擴充／dd_prior／coverage-axes.md | **回溯考卷**：dd_decision --check 30/30 現行 v15 DD 裁決相同；gen_dd_tables 對 DELL／SNOW／AVGO 的 judgment（由現行 dd-meta 反推）生成的 dd-meta 與原檔逐欄相同 |
| WP2 規則拆分 | SKILL.md → judgment-rules.md（≤35KB）＋render-rules.md（≤15KB）＋validators；SKILL.md 本體降為路由表＋三段契約（目標 ≤30KB）；rule_ledger 登記遷移（判斷類規則搬家不算新增，不觸發「加一提刪一」，但退役候選要提名） | 三檔合計 <90KB；每條 QC 有去向 |
| WP3 agent 契約與 ddreport v3 | 5.1–5.6 寫進 SKILL.md／critic-gates.md／ddreport | 一份 dry-run（不上站）跑通全鏈 |
| WP4 試點 | 三份實跑（兩份 sonnet 判斷層、一份 Fable），量 Stage 0/1/2/critic/patch 五端 cache_read | 退場訊號：合計未較 v15.2（88–130M）降 ≥40%、或 critic 首輪 🔴 未較 5–8 降 ≥50% → 回 v15.2 檢討 |

**試點順序建議（投報率）**：先做 WP1 的 `coverage-axes.md`＋`validate_evidence.py`＋0b fan-out（可獨立掛到 v15.2 現行鏈上，直接消掉最常見的 🔴），再做 `dd_decision.py`＋`gen_dd_tables.py`（消同源類錯誤），最後才拆 writer。這樣每一步都能單獨上線、單獨量效果。

## 10. 不做的事

- 不改任何門檻、機率防線、矩陣語意、dd-meta 欄位語意（PREREG）。
- 不把逐字稿讀取外包成摘要（待決 1 未裁前）。
- 不新建收斂面、不動下游聚合器（update_dd_index／screener／picks 讀 dd-meta 不變）。
- 不在本輪處理 8 份既有 DD 的未跳脫 `<`（另案 batch fix）。

---

## 11. 首次 dry-run 實測（DELL，2026-09-04，不上站）

| 段 | 輪數 | cache_read | 備註 |
|---|---|---|---|
| Stage 0（數字包＋4 組覆蓋軸） | 159 | 11.8M | 17 軸全填；validator 只卡 as_of 格式（已放寬）與 `numbers.segments` 型別 |
| Stage 1 判斷（sonnet） | 53 | 9.8M | 一輪過；transcripts 因前份已 mark 為 no-new 未讀 |
| critic 兩輪（opus） | 65 | 9.1M | 首輪 **3🔴＋7🟡**（v15.2 三份 8／7／5），**覆蓋缺軸 0**；🔴 全是判斷層一天內放寬 Bear／無交叉矛盾歸因 |
| patch 兩輪（sonnet，只改 JSON） | 150 | 20.4M | 兩輪各一次過，裁決不翻 |
| Stage 2 呈現（sonnet） | **286** | **71.9M** | 87.5KB 全閘過；validate_prose 抓到 3 個捏造數字；但 12 輪都在一分一分湊「商業本質 ≥45%」與補七表缺口 |
| **合計** | | **≈123M** | v15.2 DELL 138M（−11%），**未達 −40% 退場訊號**；判斷側（0+1+critic+patch）51M 達標，成本被呈現層吃掉 |

**結論**：證據→判斷→critic→patch 這一半已證明有效（🔴 8→3、缺軸 0、判斷層 9.8M）。呈現層失敗原因與修法：
1. `gen_dd_tables.py` 只產 dashboard／E2／E11／E12／appA／audit，**七表（E3/E5/E6/E7/E8/E9/E10）未從 judgment 生成**，散文只好硬撐篇幅與模組關鍵字（verify_dd_math 的模組偵測是關鍵字式，被「改標題」繞過——要改成檢查表格 id）。→ WP1c 補：從 `industry.tam_table`／`moat.spread_table`／`moat.roic_durability.checkpoints`／`growth.segments`／`quality.dupont`／`quality.ccc`／`governance.scorecard` 生成七表，並在 judgment schema 標必填。
2. 呈現 agent 為湊「商業本質 ≥45%」逐輪加字（43 次 Edit）。→ render-rules 改：先算好每段目標 bytes 再一次寫；生成表格計入分子；**禁 Edit prose，一段最多重寫一次**。
3. 機械表內容也會 leak（`judgment.triggers[].action` 含「row8a/8b」）與半形標點。→ `validate_judgment.py` 加 leaks 詞表掃描與 CJK 標點檢查（判斷層就攔）。
4. `dd_decision.py run` 會覆蓋掉手填的 `rearm_trigger`／`exec_line`／row 8 `requires_critic`。→ run 改為只寫 decision_out 的機械欄，保留其餘。
5. 判斷層一天內把 Bear 放寬且無歸因（critic 3🔴 的根因）。→ judgment-rules 加「與前份 dd-meta 逐欄 diff 必列於 contradictions（腳本先算 diff 餵進 evidence.prior_dd）」；`dd_prior.py` 輸出 `prior_meta_diff_targets`。

修完 1–5 再跑第二份 dry-run；預期 Stage 2 降到 20–30M、合計 70–80M。

## 12. 第二次 dry-run 實測（SNOW，2026-09-04，修法 A＋B 後，不上站）

| 段 | 輪數 | cache_read | 備註 |
|---|---|---|---|
| Stage 0 | 149 | 10.7M | 16 軸全 found（法規／資料主權軸一開始就在）；財報時效閘用 9/3 盤後價 |
| Stage 1（sonnet） | 125 | 28.4M | 七表必填＋親讀 Q2 法說；矩陣機械輸出 row 9b，agent 依 QC-49 承繼觀望 |
| critic 三輪（opus） | 59 | 6.8M | 首輪 **6🔴＋8🟡**（DELL v16 3🔴）；核心裁定：GAAP 為準→EV/S 主錨對規則，val 🟡／9b 成立，承繼合規 |
| patch 兩輪＋補漂移 | 197 | 25.4M | R1 引入 momentum 誤判→R2 修回；漂移機械檢查抓到 3 欄無 prior_field |
| Stage 2（sonnet） | 177 | 40.6M | 91KB 全閘過；重寫 7 段各一次＋decision 二次；validate_prose 11 個未覆蓋（多為「負38.6%」vs「−38.6%」符號差） |
| **合計** | | **≈112M** | v15.2 SNOW 88M（＋27%）；v15.2 DELL 138M（−19%）。**未達 −40%** |

**讀數**：①判斷品質：覆蓋缺軸 0（兩份 v16 皆 0）、裁決與 v15.2 同向；critic 🔴 未降（6），且多為判斷層資料新鮮度（733→828）與口徑一致性，非覆蓋缺口——這類要靠 Stage 0 把「最新一季官方數字」結構化進數字包（`numbers.latest_quarter_kpis`），判斷層不得引用比它舊的數字。②成本：呈現層仍是最大項（40.6M），其中 validate_prose 的符號正規化（負／−／-）可省一輪；Stage 1 因七表必填由 9.8M 升至 28.4M；patch 兩輪 25M 是 critic 首輪 6🔴 的直接後果。③兩個新機械閘實測有效：漂移歸因檢查（3 欄）、Soft Veto 與無 Veto 路徑互斥（critic 抓到，**尚未機械化**→ dd_decision 應自檢 audit_rows 互斥）。

**下一輪修法（第三份 dry-run 前）**：(a) validate_prose 符號／全半形正規化；(b) numbers 包加 `latest_quarter_kpis`（customers ≥$1M、NRR、RPO vs 共識、product GM、SBC vs OI）並在 judgment-rules 加「引用數字以此為準」；(c) dd_decision run 自檢互斥（Soft Veto hit ⇒ baseline 行不得 hit）；(d) decision 段預算下界在 v16 改 2KB（audit 已排除）；(e) 判斷層 A/B：第三份用 Fable 判斷層，比較 critic 首輪 🔴 數與 Stage 1 成本。

---

## 13. v16.1 兩步制（2026-09-04 持有人拍板：大道至簡）

**新鏈**：**第一步 sonnet 收資料**（`dd_numbers_extra.py` 六個結構化欄位＋0b 覆蓋矩陣 fan-out＋`dd_prior.py`；`validate_evidence.py --strict` 過才准開寫）→ **第二步 Fable 一次寫完**（判斷物→產表→算段落預算→散文→組裝→六支機械閘→交稿前自查），閘全過即上站。**流程內沒有 critic、沒有修補、沒有 re-gate。**

**明文推翻的兩條既有拍板**（不是繞過，是覆蓋）：
1. **「DD 寫稿後必掛獨立 critic gate」**（repo CLAUDE.md 模型路由表＋QC-41/48/50/row 8b）——v16.1 流程內取消，改為 writer 交稿前自查表（QC-41 四軸＋覆蓋面掃描＋量化模組抽查＋數字新鮮度＋散文一致性，條文語意逐字沿用，只換執行者）。
2. **「writer 與 critic 永不同模型」**——流程內已無 critic，鐵律以**流程外事後抽查**維持：前三份上站後另 spawn 一次與 writer 不同模型的冷讀，只計數不修補。

**砍掉了什麼**：獨立 patch agent、re-gate、輕 critic、Stage 1↔Stage 2 兩段式交接、`--judge-model`／`--light-critic`／`--writer-model` 的 A/B 分歧（writer 固定 Fable，旗標保留但不預期切換）。

**理由**：兩次 dry-run（§11 DELL／§12 SNOW）的 critic 首輪 🔴 **全為資料級**——資料新鮮度（733→828）、口徑一致（GAAP vs non-GAAP）、漂移未歸因——沒有一條是「另一個模型看出不同的產業判斷」。資料級問題的正確解法是把資料在 Stage 0 結構化（`latest_quarter_kpis`／`valuation_history`／`consensus_revision`／`edgar_concentrations`／`peer_financials`／`momentum_26w`）＋`--strict` 前置閘＋機械閘，不是在下游多養一個 agent 重讀 80KB 去抓。成本面同向：v16.0 的錢全花在交接（呈現層重讀 71.9M／40.6M、patch 兩輪 20.4M／25.4M），兩步制把交接次數壓到一次。

**代價（明寫，不粉飾）**：失去「不同模型的眼睛」當作發布前的 gate。writer 的自查與自己的盲點共享同一個模型——覆蓋面掃描與量化模組抽查原本正是為了對付這件事（PLTR A/B 教訓）。v16.1 只剩兩道防線：機械閘（結構、數字集合、bytes、leaks、dd-meta）＋writer 自查表。這是刻意接受的風險，用下面第 2 條退場訊號限期驗證。

**退場訊號（三條，任一未達即回退）**：
1. **覆蓋缺軸 0**（v16.0 兩份皆 0，此為不得倒退的底線；`--strict` 前置閘是主要保證）。
2. **前三份上站後事後冷讀抽查，判斷級 🔴 合計為 0 → 永久拿掉本驗收；出現 1 例 → 把 Fable 驗收放回流程內**（恢復流程內 critic gate）。
3. **每份成本 ≤ v15.2 同檔**：SNOW ≤88M、DELL ≤138M。

登記：`knowledge/rule_ledger.md`「v16.1 移除流程內 critic gate」條（kill condition 同上第 2 條）。

## 14. 第三次 dry-run 實測（SNOW，2026-09-04，v16.1 兩步制，不上站）

| 段 | 輪數 | cache_read | cache_create | output | 備註 |
|---|---|---|---|---|---|
| Stage 0（sonnet ×6：4 批覆蓋軸＋數字包／KPI＋Koyfin） | 214 | 16.9M | 1.16M | 25K | 16 軸全 found；KPI 17 項（Q2 FY2027）；`--strict` 首輪 FAIL 兩類：頂層 `events` 五組沒人寫（由 major_events 軸機械分組補）、8 條歷史事實 as_of >180 天（改為 info，strict 不升級） |
| Writer（Fable，單一 context：判斷→散文→自查） | 70 | 18.7M | 3.11M | 143K | 44 分；判斷 3 輪（首輪 4 FAIL 皆字串含 QC 代號）；verify_dd_math 首輪 FAIL（Max DD 下界 vs Bear 終點）判斷側修正；整檔重寫 3 段（s11／s12／revlog，同一根因）；99.4KB 全閘過 |
| **合計** | | **35.5M** | 4.27M | 168K | v15.2 SNOW 88M（**−60%**）；v16.0 SNOW 112M（−68%） |

**讀數**：①裁決 觀望｜追蹤（row 8）與 v15.2／v16.0 同向；覆蓋缺軸 0；數字新鮮度以 KPI 段為準，未再出現前兩輪的「舊季數字」問題。②自查表 6🟢 2🟡（③結構變數：EU AI Act／CLOUD Act 只入盲點未成觸發器，因地區營收占比證據包未涵蓋；④priced-in：方向與前份同向，邊際資訊在倍數 regime 與價格錨）。③牌價換算（§7 單價）：Stage 0 ≈ $6.5、Writer ≈ $51（cache_create 3.11M × $12.5 佔 $39——Fable 的 cache 建立單價是主因，token 量降 60% 但美元成本高於 v15.2 sonnet writer 的 $23–32）。④欄位級缺口清單（地區營收占比、Databricks 財務、管理層薪酬與內部人交易、可轉債條款、AI 收入金額）應回 Stage 0 補為結構化欄位。⑤機械小修：`render_dd --assemble` 的 site_nav 後處理在非 docs/ 路徑拋 ValueError（dry-run 限制，檔已寫）；dd_decision 條件文字（深谷投降／早循環）內含半形逗號觸發 qc 警告。

**退場訊號對照**：覆蓋缺軸 0 ✓；成本 ≤ v15.2 同檔 ✓（token 口徑）；事後抽查待前三份上站後執行。**待持有人裁定**：美元成本口徑是否納入退場訊號。

**§14 補：流程外冷讀抽查（opus，2026-09-04，`notes/site-internal/dd/_audit_SNOW_20260904.md`）**：判斷級 🔴 2／資料級 🔴 2／🟡 11，裁決方向同意觀望｜追蹤。orchestrator 對質兩個判斷級：①「Databricks 相對速度差連 4 季 >2 倍才升趨勢↓，現計 1 季」——證據包自述 2025-10 季度超車且差距逐季拉大，計數是否該為 3–4 季屬真實判斷分歧，且落在 row 8（觀望）↔ row 3（迴避）分界，**成立**；②「GAAP 轉盈利 Q4 FY28 承諾無據」——Investor Day 2026-06-02 逐字稿第 590 行明寫，writer 親讀逐字稿正確，冷讀者只拿證據包未拿逐字稿，**不成立**（改列 Stage 0 資料級缺口：網搜漏掉該公告；抽查輸入須加 must_read 逐字稿）。**依 rule_ledger kill condition（判斷級 🔴 ≥1 例）觸發：Fable 驗收應放回流程內，待持有人裁定形式。**
