你是 stock-analyst **v20 判斷 agent**，標的 CRDO（20261012）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

## 你只在五個地方出手（其餘由程式投影，填了即 FAIL）

| # | 出手點 | 落在哪 |
|---|---|---|
| ① | **論點與唯一致命數字** | `thesis`（H1–H3／R1–Rn／Single Thing）＋`answers.q1_business` |
| ② | **護城河方向與再投資報酬** | `answers.q2_moat`（機制／trend／子評分／四檢查點／ROIIC）＋`answers.q3_growth`（runway 燈／缺口歸因） |
| ③ | **情境樹假設** | `scenario_inputs`（三支 EPS 路徑、終端倍數、機率、Max DD 範圍與依據） |
| ④ | **反證裁定** | `counter_evidence`（三視角反證、矛盾裁定、觸發器、行動條件） |
| ⑤ | **決策輸入與行動條件** | `decision_inputs` 九欄＋`appendix_a` 七欄＋`eps_meta` |

**不歸你的**（程式從上面這幾塊投影或算出來）：評分加總與燈號（`capalloc_grade`／`path_risk`／moat 合併分）、`plain.*` 白話段、`reasoning` 頂層摘要、`contradictions`／`triggers`／`premortem` 等舊形狀頂層欄、同業對照表的數字、整份 `scenario.json`、`decision_out` 矩陣欄、`decision_inputs` 的機械欄。這些不要填——填了機械閘會擋，而你沒有下一輪能改。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：v19 schema 速查、`facts.json` 事實表全文、最新一季逐字稿全文、判斷卡（`judge_card.md`）、常載附卡（ROIC 持續期檢核、情境判斷問題字典）、archetype 命中時的條件附卡、前份判斷摘要，最後是回覆格式規範。bundle 之外一律不存在：不讀 `docs/dd/` 任何既有報告，不查證任何未附上的資料，不重述 bundle 內容。

## 三條在動筆前先掃一遍的硬規則

1. **負向證據強制處置**——`facts.json` 的 `findings_digest[]` 內每一條 `direction="-"` 的 finding，必須落在 `counter_evidence.contradictions[]`／`blind_spots[]`／`triggers[]`／`answers.q2_moat` 內 `moat.threats[]`／`thesis.R[]` 之一的 `evidence_refs`，或寫進 `counter_evidence.evidence_dismissed[]`（`{"ref": …, "reason": …}`，理由要指得出證據本身的問題，不得寫「影響不大」）。
2. **引用可追溯**——事實表已有的資料用該題 `fact_refs[]`；索引漏收時可在理由中引用本包原始證據，寫明欄位路徑、來源與期間。不得捏造 `f_*` id，不得從記憶補數字，原始證據也沒有才標資料缺口。
3. **前份漂移按原因分組**——前份判斷摘要裡有變動的每一欄都要映射到 `counter_evidence.contradictions[]` 一條帶 `cause`（`價格變動`／`新證據`／`方法變動`）的條目，漏一欄視為未處理；行動門檻（`kill_metrics`／`triggers` 的門檻數字、Single Thing）與前份不同時必歸因，`rearm_trigger` 不得對已變動的門檻寫「相同」。

## 禁

- 不自搜補洞：證據不足就在對應欄位標「事實表未涵蓋」。
- 不引用 bundle 之外的任何資料。
- enum 欄位只准用速查列出的值，不得自行加註解或譯成中文；`kill_metrics[]` 是陣列不是索引鍵物件；§5.R 四檢查點四項必答（缺一即無效）。


===== BUNDLE =====

## ② Schema 速查（judge-owned 形狀；機械生成自 judgment.schema.json 的 v19_contract 區塊）

格式：縮排＝巢狀層級（不重複完整路徑）；行首 `*`＝必填；型別簡寫 str/obj/arr/int/num/bool，`a|b`＝可為多型別（含 null）；`enum[...]`＝允許值；`pat=`＝正則；`≤N`＝maxLength；`≥N`＝minItems；陣列欄位以 `key[]` 表示，其元素（items）型別接在同一行，物件元素的欄位在下一層縮排列出。

*meta
  *ticker: str
  *date: str pat=^\d{4}-\d{2}-\d{2}$
  *schema: str pat=^v1[2345]\.\d+$
  *contract: str enum[v19]
  company_name: str|null
*oneliner: str ≤200
*facts_ref: str
*scenario_ref: str|null
*answers
  *q1_business
    *verdict: str
    *reasoning: str
    *fact_refs[]: arr str pat=^f_[a-z0-9_]+$
    *verdict_values
      *revenue_quality: str|null
      *unit_econ_note: str|null
      *archetype
        *primary: str|null
        secondary: str|null
        confidence: str|null
        fingerprint: str|null
      *industry
        *clock_phase: str|null enum[I｜II｜III｜IV｜None]
        *sd_verdict_source: str|null
        bargaining
          up: str|null
          down: str|null
          geo: str|null
        profit_pool_dir: str|null
        *tam_table: arr|obj
      single_thing
  *q2_moat
    *verdict: str
    *reasoning: str
    *fact_refs[]: arr str pat=^f_[a-z0-9_]+$
    *verdict_values
      *moat
        *mechanism: str|null
        *execution: num|null
        *pricing: num|null
        combined: num|null
        score: num|null
        *grade: str|null enum[S｜A｜B｜C｜X｜None]
        *trend: str|null enum[↑｜→｜↓｜None]
        *trend_evidence: str|null
        *competitor_notes[]: arr
          *name: str
          *strategy_note: str
        spread_notes: obj|null
        peer_na_reason: str|null
        *threats[]: arr
          level: str|null
          text: str|null
          p: str|num|null
          evidence_refs[]: arr str
        *roic_durability
          quadrant: str|null
          *checkpoints[]: arr
          *roiic: num|str|null
          *reinvest_rate: num|str|null
          *endo_ceiling: num|null
          formula_note: str|null
  *q3_growth
    *verdict: str
    *reasoning: str
    *fact_refs[]: arr str pat=^f_[a-z0-9_]+$
    *verdict_values
      *growth
        *driver_mix: str|null
        runway_years: num|str|null
        *runway_post_y5: str|null enum[🟢｜🟡｜🔴｜None]
        *endo_ceiling_basis: str|null
        *segments: arr|obj
        seven_questions[]: arr
        decay_signals[]: arr
        trap_rating: str|null
  *q4_capital
    *verdict: str
    *reasoning: str
    *fact_refs[]: arr str pat=^f_[a-z0-9_]+$
    *verdict_values
      *capalloc
        *items[]: arr ≥1
          *name: str enum[ma_roiic｜buyback_yield｜sbc_dilution]
          *applicable: bool|null
          *passed: bool|null
          *input: str|null
        grade: str|null enum[A｜B｜C｜None]
      *governance
        *capital_returns: arr|obj
        scorecard[]: arr
        sbc
      quality
        three_year[]: arr
        dupont[]: arr ≥1
        ccc[]: arr ≥1
        buyback
        lumpiness
        financial_note: str
        latest_quarter_note: str
  *q5_valuation
    *verdict: str
    *reasoning: str
    *fact_refs[]: arr str pat=^f_[a-z0-9_]+$
    *verdict_values
      *valuation
        *basis: str|null
        tier: str|null
        *peers: arr|obj
        fwd_pe: num|null
        *peg: num|null
        *percentile_5y: num|null
        *val_light: str|null enum[🟢｜🟡｜🟠｜🔴｜None]
        *val_light_derivation: str|null
        targets
        *upside_short_pct: num|null
        *upside_mid_pct: num|null
        *denominator_disputed: bool|null
        *denominator_note: str|null
  *q6_how_wrong
    *verdict: str
    *reasoning: str
    *fact_refs[]: arr str pat=^f_[a-z0-9_]+$
    *verdict_values
      *trap
        *verdict: str|null enum[🟢｜🟡｜🔴｜None]
        *label: str|null
*scenario_inputs
  *terminal_label: str
  start
  *eps
    *bull[]: arr ≥1 num
    *base[]: arr ≥1 num
    *bear[]: arr ≥1 num
  *pe
    *bull: num|null
    *base: num|null
    *bear: num|null
  *p
    *bull: num|null
    *base: num|null
    *bear: num|null
  yield_pct
  second_stage
  basis
  endo_ceiling_exceeded: bool|null
  peer_max_fpe: num|null
  *max_dd
    *lo: num|null
    *hi: num|null
    *basis: str|null
    trigger_time: str|null
*counter_evidence
  *blind_spots[]: arr ≥1
    view: str|null enum[論點失敗｜論點成功但股東經濟變差｜價格已反映太多｜None]
    evidence: str|null
    assumption: str|null
    consequence: str|null
    ruling: str|null
    watch: str|null
    not_applicable_reason: str|null
    evidence_refs[]: arr str
    fact_refs[]: arr str
  *contradictions[]: arr
    axis: str|null
    cause: str|null enum[價格變動｜新證據｜方法變動｜None]
    prior_field: str|arr|null
    side_a: str|null
    side_b: str|null
    ruling: str|null
    evidence_level: str|null
    settle_metric: str|null
    if_then[]: arr str
    evidence_refs[]: arr str
  *triggers[]: arr ≥1
    *n: int|str
    *text: str|null
    *type: str|null enum[假設驗證｜風險｜Single Thing｜估值rearm｜加碼｜減碼｜清倉｜複審日期｜None]
    *maps_to: str|null
    *metric: str|null
    *threshold: str|null
    *action: str|null
    *source_freq: str|null
    *date: str|null
    type_display: str|null
    evidence_refs[]: arr str
  kill_metrics[]: arr
    *metric: str|null ≤120
    *bear_threshold: str|null ≤120
    *window: str|null ≤60
    source: str|null ≤120
    last_status: str|null enum[ok｜warning｜triggered｜unknown｜None]
  evidence_dismissed[]: arr
    ref: str|null
    reason: str|null
  *action_conditions
    *rearm_trigger: str|null ≤120
    *exec_line: str|null
    holding_cap: str|null
*decision_inputs
  *signal: str|null enum[A+｜A｜B｜C｜X｜None]
  *ma: str|null enum[🟢｜✅｜🟡｜🟠｜❌｜-｜None]
  *cycle_position: str|null
  *cycle_verdict: str|null
  *thesis_irreconcilable: bool|null
  *valuation_dependent: bool|null
  *market_wrong_reason_given: bool|str|null
  *momentum_overheated: bool|null
  *cycle_gates_pass: bool|null
  qc49_inherit_prior: bool|null
  wait_for_price: bool|null
  wait_for_price_condition: str|null
  qc48_result: str|null enum[pass｜fail｜not_run｜None]
  qc48_note: str|null
*decision_out
  *verdict: str|null
  *role: str|null
  *row_hit: str|null
  pacing[]: arr str
  holding_cap: str|null
  requires_critic[]: arr str
  *audit_rows[]: arr str|obj
*thesis
  *H[]: arr ≥3
    *id: str pat=^H[1-9][0-9]*$
    *text: str|null
    2y: str|null
    5y: str|null
    10y: str|null
    *threshold: str|null
    *source: str|null
    *drift_rule: str|null
  *R[]: arr ≥3
    *id: str pat=^R[1-9][0-9]*$
    *text: str|null
    *h_ref: str|null
    *clock: str|null enum[⚡｜🔥｜🐢｜None]
    *threshold: str|null
    evidence_refs[]: arr str
  *single_thing
    *description: str|null
    *why_fatal: str|null
    *if_happens: str|null
    *how_monitor: str|null
    *probability: str|null
*appendix_a
  *growth_durability: num|null
  *quality_score: num|null
  *ai_risk: str|null enum[🟢｜🟡｜🔴｜None]
  *long_term_confidence: str|null enum[高｜中｜低｜None]
  *fpe_fy2: num|null
  *peg_fy2: num|null
  *stress
    *pass: int|null
    *total: int|null
*eps_meta
  *base_eps_path
  fy_end_month: int|null
  eps_basis: str|null
catalysts[]: arr
  *date: str|null
  date_precision: str|null enum[month｜quarter｜None]
  *type: str|null enum[product｜regulatory｜capacity｜guidance｜macro｜other｜None]
  *event: str|null
  *impact: str|null enum[高｜中｜低｜None]
  *watch: str|null

### evidence_refs 用法（v19）
`counter_evidence.contradictions[]`／`counter_evidence.blind_spots[]`／`counter_evidence.triggers[]`／`answers.q2_moat.verdict_values.moat.threats[]`／`thesis.R[]` 可各自加選填 `evidence_refs: [string]`，格式 `axis_id#index`（對應事實表 `findings_digest[]` 的 `id`）。無法對應到既有證據、但仍要捨棄的負向 finding，記到 `counter_evidence.evidence_dismissed: [{ref, reason}]`（理由要指得出證據本身的問題，不得寫「影響不大」）。`validate_judgment.py --evidence`（J1）會檢查每條 `direction=="-"` 的 finding 是否被上述任一處引用，未引用＝FAIL。

### fact_refs 用法（v19）
`answers.qX.fact_refs[]` 只准填事實表裡真的存在的 `f_*` id（引不到＝FAIL）。索引漏收時可引用本包原始證據，寫明欄位路徑、來源與期間；不要捏造 fact id，也不要從記憶補數字。

### 不要填的欄（填了即 FAIL）
`decision_inputs` 的 `trap`、`val`、`moat`、`moat_trend`、`runway_post_y5`、`capalloc_grade`、`archetype`、`price_at_dd`、`week26_return_pct`、`consensus_rev_3m_pct`、`asym_ratio`、`irr_base_pct`、`ev5y_pct`、`val_denominator_disputed`、`val_denominator_note` 一律留 `null` 或整個不寫——由程式從六問答案與事實表投影。同理不要寫 `moat.spread_table`／`moat.competitors`（同業數字在事實表的 `peer_comparison`，你只寫 `moat.competitor_notes` 每家一句判讀）、`reasoning`／`plain`／`contradictions` 等舊形狀頂層欄、以及整份 `scenario.json`。

### §5.R 四檢查點形狀（checkpoints[] 未在上方展開，這裡手動點名）
`answers.q2_moat.verdict_values.moat.roic_durability.checkpoints[]` 四項（需求基礎值／決策層級／價值鏈分配／社會容忍度）**每項各一筆物件**，鍵名固定 `item`（四項名稱之一，逐字比對，不得改寫或縮寫）／`level`（🟢🟡🔴）／`text`（判讀句；查無或不適用改填 `not_applicable_reason`）。四項缺一，或某項 `text` 與 `not_applicable_reason` 皆空＝FAIL（`validate_judgment.v19_required_items_checks`）。

### kill_metrics[] 形狀（counter_evidence.kill_metrics，未在上方展開，這裡手動點名）
是**陣列**（`[{...}, {...}]`），不是以索引數字（`"0"`／`"1"`）當鍵的物件；每條必填 `metric`／`bear_threshold`／`window`，並附 `source`（資料來源）。

### 機器語言／半形標點洩漏詞表（單一權威：`dd_sections.LEAK_PATTERNS` ＋ `qc.CJK_PUNCT_RE`）
`row ?\d`、`Hard Veto`、`Soft Veto`、`signal ?[ABCX]\b`、`估值燈`、`val ?[🟢🟡🟠🔴]`、`MA ?[✅❌🟢🟡🟠]`、`Pure MA`、`盲點 ?\d`、`PREREG`、`dd-meta`、`runway_post_y5`、`capalloc`、`QC-\d`、`archetype`、`metadata`、`硬接線`、`接線[:：]`、`Guardrail`、`校驗紀錄`、`判定規則`、`\bgate\b`、`\bF2\b`、`row 8[ab]`、`爆發候選路徑`、`循環衛星進場路徑`
- CJK 字元後接半形 `,` `.` `:`（正則 `[㐀-䶿一-鿿豈-﫿][,.:]`）——一律應為全形 ，。：

---

## ②b enum 表（機械抽自 judgment.schema.json；這些欄只准填表列值，填自由文字＝FAIL）

- `answers.q1_business.verdict_values.industry.clock_phase`：I｜II｜III｜IV
- `answers.q2_moat.verdict_values.moat.grade`：S｜A｜B｜C｜X
- `answers.q2_moat.verdict_values.moat.trend`：↑｜→｜↓
- `answers.q3_growth.verdict_values.growth.runway_post_y5`：🟢｜🟡｜🔴
- `answers.q4_capital.verdict_values.capalloc.items[].name`：ma_roiic｜buyback_yield｜sbc_dilution
- `answers.q4_capital.verdict_values.capalloc.grade`：A｜B｜C
- `answers.q5_valuation.verdict_values.valuation.val_light`：🟢｜🟡｜🟠｜🔴
- `answers.q6_how_wrong.verdict_values.trap.verdict`：🟢｜🟡｜🔴
- `counter_evidence.blind_spots[].view`：論點失敗｜論點成功但股東經濟變差｜價格已反映太多
- `decision_inputs.signal`：A+｜A｜B｜C｜X
- `decision_inputs.ma`：🟢｜✅｜🟡｜🟠｜❌｜-
- `decision_inputs.qc48_result`：pass｜fail｜not_run
- `appendix_a.ai_risk`：🟢｜🟡｜🔴
- `appendix_a.long_term_confidence`：高｜中｜低
- `archetype.primary（投影後驗）`：品質複利成長｜循環/商品｜金融｜未獲利高成長｜轉機/特殊情境｜受監管公用/穩定內需｜EMS/ODM
- `archetype.confidence（投影後驗）`：高｜中｜低
- `decision_inputs.trap（投影後驗）`：🟢｜🟡｜🔴
- `decision_inputs.val（投影後驗）`：🟢｜🟡｜🟠｜🔴
- `decision_inputs.moat_trend（投影後驗）`：↑｜→｜↓
- `decision_inputs.moat（投影後驗）`：S｜A｜B｜C｜X
- `decision_inputs.capalloc_grade（投影後驗）`：A｜B｜C
- `decision_inputs.archetype（投影後驗）`：品質複利成長｜循環/商品｜金融｜未獲利高成長｜轉機/特殊情境｜受監管公用/穩定內需｜EMS/ODM
- `decision_inputs.cycle_position（投影後驗）`：深谷投降｜早循環｜中循環｜晚循環｜過熱頂部
- `decision_inputs.cycle_verdict（投影後驗）`：右側可追蹤｜等回踩｜頂部觀望｜未觸發
- `triggers[].type（投影後驗）`：假設驗證｜風險｜Single Thing｜估值rearm｜加碼｜減碼｜清倉｜複審日期
- `catalysts[].date_precision（投影後驗）`：month｜quarter
- `catalysts[].impact（投影後驗）`：高｜中｜低
- `thesis.R[].clock（投影後驗）`：⚡｜🔥｜🐢

---

## ②c 理由文字禁用詞表（QC-40 機器語言，命中任一＝FAIL；這些是給程式看的代號，不是給讀者的話）

以下為 regex 原文，逐條避開（含變體）：

`row ?\d`　`Hard Veto`　`Soft Veto`　`signal ?[ABCX]\b`　`估值燈`　`val ?[🟢🟡🟠🔴]`　`MA ?[✅❌🟢🟡🟠]`　`Pure MA`　`盲點 ?\d`　`PREREG`　`dd-meta`　`runway_post_y5`　`capalloc`　`QC-\d`　`archetype`　`metadata`　`硬接線`　`接線[:：]`　`Guardrail`　`校驗紀錄`　`判定規則`　`\bgate\b`　`\bF2\b`　`row 8[ab]`　`爆發候選路徑`　`循環衛星進場路徑`

改寫原則：說結論本身，不說「燈號／閘／row／QC／驗算」這類流程代號。例：「估值燈色不變」→「估值結論不變」；「row 8a」→ 直接寫進場條件本身，不用路徑代號。

---

## ③ facts.json 事實表全文（引用索引；含 findings_digest 與同業對照）

（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"meta":{"ticker":"CRDO","date":"2026-10-12","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRDO_20261012/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRDO_20261012/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":479.0,"period":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","unit":"USD M（YoY +114.7%，QoQ +9.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","citation":"公司新聞稿（BusinessWire，Q1 FY27 earnings release）https://s205.q4cdn.com/511065572/files/doc_news/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results-2026.pdf"}},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income","value":230.6,"period":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","unit":"USD M（利益率 48.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","citation":"公司新聞稿（BusinessWire，Q1 FY27 earnings release）https://s205.q4cdn.com/511065572/files/doc_news/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results-2026.pdf"}},{"id":"f_kpi2_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":48.2,"period":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","citation":"公司新聞稿（BusinessWire，Q1 FY27 earnings release）https://s205.q4cdn.com/511065572/files/doc_news/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results-2026.pdf"}},{"id":"f_kpi3_gaap_operating_income","label":"GAAP operating income","value":120.7,"period":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","unit":"USD M（利益率 25.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","citation":"公司新聞稿（BusinessWire，Q1 FY27 earnings release）https://s205.q4cdn.com/511065572/files/doc_news/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results-2026.pdf"}},{"id":"f_kpi4_gaap_operating_margin","label":"GAAP operating margin","value":25.2,"period":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","citation":"公司新聞稿（BusinessWire，Q1 FY27 earnings release）https://s205.q4cdn.com/511065572/files/doc_news/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results-2026.pdf"}},{"id":"f_kpi5_share_based_compensation","label":"Share-based compensation（占營收／占 non-GAAP 營業利益）","value":88.0,"period":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","unit":"USD M（占營收 18.4%；占 non-GAAP 營業利益 38.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","citation":"公司新聞稿（BusinessWire，Q1 FY27 earnings release）https://s205.q4cdn.com/511065572/files/doc_news/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results-2026.pdf"}},{"id":"f_kpi6_non_gaap_gross_margin","label":"Non-GAAP gross margin","value":68.0,"period":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","unit":"%（GAAP 64.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","citation":"公司新聞稿（BusinessWire，Q1 FY27 earnings release）https://s205.q4cdn.com/511065572/files/doc_news/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results-2026.pdf"}},{"id":"f_kpi7_guidance_q2_fy2027","label":"Guidance Q2 FY2027","value":"營收 525–535M；non-GAAP 毛利率 67.0–69.0%；non-GAAP 營業費用 100–105M；GAAP 毛利率 62.9–64.9%；GAAP 營業費用 199–204M","period":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","unit":"USD M／%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q1 FY2027（季末 2026-08-01，公告於 2026-09-01）","citation":"公司新聞稿（BusinessWire，Q1 FY27 earnings release）https://s205.q4cdn.com/511065572/files/doc_news/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results-2026.pdf"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-09-01","period":"2026-09-01","unit":"date","basis":"距今 29 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-09-01"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_crdo_gross_margin_pct","label":"CRDO 毛利率","value":67.07,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crdo_operating_margin_pct","label":"CRDO 營業利益率","value":31.74,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crdo_fcf_margin_pct","label":"CRDO FCF 利潤率","value":27.57,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_gross_margin_pct","label":"MRVL 毛利率","value":52.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_operating_margin_pct","label":"MRVL 營業利益率","value":16.81,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_fcf_margin_pct","label":"MRVL FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_alab_gross_margin_pct","label":"ALAB 毛利率","value":75.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_alab_operating_margin_pct","label":"ALAB 營業利益率","value":22.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_alab_fcf_margin_pct","label":"ALAB FCF 利潤率","value":23.02,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtsi_gross_margin_pct","label":"MTSI 毛利率","value":56.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtsi_operating_margin_pct","label":"MTSI 營業利益率","value":18.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtsi_fcf_margin_pct","label":"MTSI FCF 利潤率","value":10.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":216.55,"period":"2026-10-09（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":81.08,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":56.98,"period":"2026-10-09（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.31 → 6.31）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.1,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.7 → 9.69）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.45 → 12.45）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":6.31,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.69,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":12.45,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.94,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 6.13 → 6.31（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":76.79,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"2 個年度端點內的分位＝3.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":3.6,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":25.58,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝97.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":97.9,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":25.12,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝99.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":99.9,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":34.32,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 6.31，分子＝快照價 216.55","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"JPMorgan-based note (Oct 2025) puts Credo AEC share at ~80%, citing competition from Marvell, Broadcom and especially Astera; later secondary write-ups cite ~88% share. Neither is sourced to Dell'Oro/LightCounting; as_of is month-level approximate (2025-10).","source":"Investing.com, Credo Technology's SWOT analysis (search summary)","url":"https://uk.investing.com/news/-4696563","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Marvell reportedly launched Alaska AEC products aimed at Credo's core market and runs a 'Golden Cable' AEC ecosystem initiative; Marvell expects AEC and retimer revenue to more than double YoY. Third-party analysis, primary source not verified; date not found.","source":"Seeking Alpha / theinvestingshow newsletter (search summary)","url":"https://theinvestingshow.beehiiv.com/p/crdo-a77e27fdf926919e","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Credo added a fifth hyperscaler customer (initial revenue) in fiscal Q2 2026; three hyperscalers each >10% of revenue, top three customers 39%/32%/17% of revenue in FQ3 2026.","source":"Nasdaq/Zacks, Will CRDO's Expanding Hyperscaler Base Accelerate Growth Momentum?","url":"https://www.nasdaq.com/articles/will-crdos-expanding-hyperscaler-base-accelerate-growth-momentum","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Settlements with Amphenol and Volex resolved AEC patent disputes via licenses (removes litigation overhang; implies licensed competitors in AEC).","source":"Investing.com, Credo SWOT analysis (search summary)","url":"https://uk.investing.com/news/-4696563","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Credo Q3 FY2026 call: largest customer 39% of revenue, second 32%, third 17%; management expects 3-4 customers above 10% to continue (搜尋摘要轉述，非逐字)","source":"Credo Q3 FY2026 earnings call coverage (Yahoo Finance/MarketBeat)","url":"https://finance.yahoo.com/news/credo-technology-group-q3-earnings-232723083.html","excerpt":null,"as_of":"2026-03-02","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2026 10-K: Customer A 53% of accounts receivable at year-end (vs 86% a year earlier); Customers B and C 20% and 19%; customer mix shifts period to period; substantial majority of revenue from limited number of customers","source":"Credo Form 10-K FY2026 (FYE 2026-05-02)","url":"https://www.sec.gov/Archives/edgar/data/0001807794/000162828026043303/crdo-20260502.htm","excerpt":null,"as_of":"2026-05-02","retrieved_at":"20261012","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Q2 FY2025 call: CEO acknowledged hyperscaler customers desire multiple sources; Credo aims to be first to deliver samples and ramp production (二手摘要)","source":"Fintool CRDO Q2 2025 earnings summary","url":"https://fintool.com/app/research/companies/CRDO/earnings/Q2 2025","excerpt":null,"as_of":"2024-12-03","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Marvell launched an AEC ecosystem initiative (Golden Cable) with cable assemblers to accelerate hyperscaler AEC adoption, letting customers incorporate their own IP; vendor-side competitive move, not a named customer second-source award","source":"Marvell press release via BusinessWire","url":"https://www.businesswire.com/news/home/20251209603264/en","excerpt":null,"as_of":"2025-12-09","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 10-K（FY 結束 2026-05-02）：營收來自少數客戶；以終端客戶口徑 Customer D 占 33%、Customer B 32%、Customer E 19%；Customer D FY2025 為 63%。合約對象（常為代工廠）口徑與終端客戶口徑不同。","source":"SEC EDGAR, Credo Technology Group Holding Ltd Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001807794/000162828026043303/crdo-20260502.htm","excerpt":null,"as_of":"2026-05-02","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"單季口徑（媒體/分析報導，非 10-K）：FY26 Q4 前三大客戶 34%、27%、16%；Q3 前三大 39%、32%、17%；管理層預期未來數季有 3–4 家客戶各占逾 10%，分散化將是漸進的。","source":"Nasdaq/Yahoo Finance 報導彙整（Credo Q3 earnings; Credo stock outlook）","url":"https://www.nasdaq.com/articles/credo-technology-stock-outlook-hinges-ai-and-optical-scale","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"超大型雲端客戶信用面：Moody's 警示 Microsoft、Amazon 等六家大型科技公司轉向重資產模式威脅信用品質，2026 資本支出預估 7850 億美元；但多份來源稱 Alphabet/Amazon/Meta/Microsoft 近期不致失去投資級。未找到 xAI 或 Credo 具名客戶的信用事件。","source":"Yahoo Finance 'AI coming trillion dollar hangover'; Moody's 報導轉載（binance square）","url":"https://finance.yahoo.com/news/ai-coming-trillion-dollar-hangover-150642244.html","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Credo 管理層稱 AEC 為機櫃內／機櫃間短距互連的事實標準；FY26 Q3 營收 4.07 億美元，QoQ +51.9%、YoY +201.5%；前三大客戶占營收 39%/32%/17%（集中度風險）。皆為公司自述，經 Zacks/Nasdaq 轉載。","source":"Nasdaq/Zacks: Credo Technology Expands Hyperscaler Reach: Concern or Strength?","url":"https://www.nasdaq.com/articles/credo-technology-expands-hyperscaler-reach-concern-or-strength","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"業界分析認為 CPO 大規模部署要到 2027–2029 年之後，在此之前 AEC 為機櫃內短距互連較優解；800G 於 2025–2027 年成為主流、並朝 1.6T 演進（分析師/Substack 評論，非一手數據）。","source":"Semi Fundamental (Substack): Active Electrical Cable (AEC) Fundamentals","url":"https://semifundamental.substack.com/p/active-electrical-cable-aec-fundamentals","excerpt":"AEC has emerged as the optimal solution for short-reach in-rack interconnects in AI data centers; large-scale deployment after 2027–2029","as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"超大規模雲端 capex 預期 2027 年續增（Moody's 約 8,200 億美元；Goldman 估 AI capex 約 1.14 兆），但部分來源認為市場將定價 2027 為高峰、2027 後增速放緩至 10% 以下；2028 無明確共識。多為二手來源，需對原報告核實。","source":"DatacenterDynamics: Moody's hyperscaler capex forecasts marked up by $85bn to close in on $1trn by 2027","url":"https://datacenterdynamics.com/en/news/moodys-hyperscaler-capex-forecasts-marked-up-by-85bn-to-close-in-on-1trn-by-2027/","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261012","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lucintel 2026 年 6 月報告：AEC 整體市場 2035 年約 68 億美元、2026–2035 CAGR 22.8%（市場定義與其他報告不同，不可直接比較）。","source":"Lucintel: Active Electrical Cable Technology Market Report to 2035","url":"https://www.lucintel.com/ko/active-electrical-cable-technology-market.aspx","excerpt":"The global active electrical cable technology market is expected to reach an estimated $6.8 billion by 2035 with a CAGR of 22.8% from 2026 to 2035.","as_of":"2026-06-01","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Credo FY2026 10-K（會計年度止 2026-05-02）國際營運風險因素列出貿易限制、較高關稅（引述美中貿易緊張已使部分半導體產品關稅上升）、出口許可要求、制裁，及中國法規可能限制中國子公司資金／股利匯出；Credo 在中國大陸設有 R&D、行銷、行政與銷售職能；晶圓製造與封測全數外包，主要在亞洲。","source":"SEC EDGAR Credo Technology Group Holding Ltd Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001807794/000162828026043303/crdo-20260502.htm","excerpt":null,"as_of":"2026-05-02","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Credo FY2025 10-K 提及2025年4月美國關稅（含對中國等國較高稅率）及貿易戰升溫可能壓低客戶需求、墊高成本；FY2026 版本此段仍在，且相關討論自 FY2025 起擴充。","source":"SEC EDGAR Credo Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1807794/000162828025033813/crdo-20250503.htm","excerpt":null,"as_of":"2025-05-03","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 公告、01-15 生效的 Section 232 對特定先進運算晶片課 25% 關稅，範圍依性能門檻（如 H200、MI325X），用於美國資料中心、維修、R&D等用途豁免；搜尋結果未提及 Credo 或網通／連接類產品是否涵蓋。","source":"Thomson Reuters OneSource: Trump administration imposes tariffs on advanced AI chips under Section 232 authority","url":"https://www.thomsonreuters.com/en-us/help/onesource-global-trade/regulatory-insights/2026/january-15th/trump-admin-tariffs-advanced-ai-chips-232.html","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261012","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K：Credo 所有產品的製造與組裝外包給第三方，主要在亞洲；研發點含美、加、中國大陸、台灣、香港；地緣不穩與關稅被列為供應鏈與需求的不確定來源（搜尋摘要轉述，未讀全文）","source":"SEC EDGAR, Credo Technology Group Holding Ltd Form 10-K FY2026 (period ended 2026-05-02)","url":"https://www.sec.gov/Archives/edgar/data/0001807794/000162828026043303/crdo-20260502.htm","excerpt":"Credo outsources all product fabrication and assembly to third parties, mostly in Asia.","as_of":"2026-05-02","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K：除 BizLink 的部分 AEC 製造協議外，Credo 與 TSMC 及其他第三方代工／供應商均無長期供貨合約","source":"SEC EDGAR, Credo 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001807794/000162828026043303/crdo-20260502.htm","excerpt":"Except for our agreement with BizLink for the manufacture of certain AEC products, we do not maintain long-term supply contracts with TSMC or generally with any of our third-party contract manufacturers or other suppliers.","as_of":"2026-05-02","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 稱 TSMC、BizLink 等均未提供產能的合約保證；更換現有代工或組裝商估計需約 9–12 個月、成本上升且客戶須重新認證（搜尋摘要轉述）","source":"SEC EDGAR, Credo 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001807794/000162828026043303/crdo-20260502.htm","excerpt":"None of TSMC, BizLink or our third-party manufacturers or other suppliers have provided contractual assurances to us that adequate capacity will be available to us to meet our anticipated future demand for our solutions.","as_of":"2026-05-02","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"第三方分析稱 Credo 為無廠半導體，全部半導體產品依賴台灣 TSMC 代工，並標示兩岸緊張為中斷風險（二手來源，需對 10-K 全文交叉驗證）","source":"dcf-analysis.com, Credo Technology Group Holding Ltd (CRDO): PESTLE Analysis [Apr-2026 Updated]","url":"https://dcf-analysis.com/products/crdo-pestel-analysis","excerpt":"relies on TSMC in Taiwan as the foundry for all of its semiconductor products","as_of":"2026-04-30","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"產業層面：台灣廠商在先進封裝（CoWoS/InFO）占比高，各來源數字不一（67%／85% vs 28% ATP），屬產業集中度背景，非 CRDO 專屬揭露","source":"Evertiq, Global semiconductor supply chain remains concentrated, exposing bottlenecks","url":"https://evertiq.com/design/2025-12-26-global-semiconductor-supply-chain-remains-concentrated-exposing-bottlenecks","excerpt":null,"as_of":"2025-12-26","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q1 FY2027 營收 $479M，YoY +114.7%、QoQ +9.6%；Q2 指引 $525–535M；AEC 仍為最大事業單元，驅動為 hyperscale 滲透與 NeoCloud 採用；1.6T AEC 預期 FY27 下半年開始貢獻、FY28 放量。","source":"Credo Reports Q1 Fiscal 2027 Revenue Of $479 Million, Up 115% Year Over Year (pulse2) / chartmill","url":"https://pulse2.com/credo-reports-q1-fiscal-2027-revenue-of-479-million-up-115-year-over-year/","excerpt":"representing growth of 9.6% sequentially and 114.7% year over year","as_of":"2026-09-01","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"管理層 FY2027 營收成長目標 >85%，光學營收預期超過 $600M；FY27 新增營收約一半來自光學、一半來自銅（主要 AEC 與 retimer）。","source":"Credo Q1 FY2027 coverage (itiger: Credo Reports 114.7% Revenue Surge in Q1)","url":"https://www.itiger.com/news/1122940235","excerpt":"about half of the expected absolute dollar revenue growth in fiscal 2027 should come from the optical portfolio and about half from the existing copper portfolio, predominantly AECs and retimers.","as_of":"2026-09-01","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"客戶集中：Q1 FY27 四大客戶約占營收 84%。","source":"Credo Q1 FY2027 coverage (itiger)","url":"https://www.itiger.com/news/1122940235","excerpt":"four customers generated roughly 84% of quarterly revenues","as_of":"2026-09-01","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"AEC 市佔估計：某投資電子報稱約 88%（JPMorgan 預估該市場 2028 年達 $4B）；Tech Investments 2025-10 筆記估約 80%，且 Marvell、Broadcom、Astera 為新進者。2026 年無新市佔或定價資料。","source":"Tech Investments, High growth stock picks (2025-10)","url":"https://www.techinvestments.io/p/high-growth-stock-picks","excerpt":null,"as_of":"2025-10-15","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"AEC 單價隨產品組合上移：由早期單一客戶 100G 直連線（ASP 低數百美元）轉向最高 800G 的複雜形式（ASP 中數百美元）；為 2025 年分析師觀點，非 2026 價格趨勢。","source":"Tech Investments, High growth stock picks (2025-10)","url":"https://www.techinvestments.io/p/high-growth-stock-picks","excerpt":null,"as_of":"2025-10-15","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"第三方 TAM：Lucintel 預估 AEC 技術市場 2035 年約 $6.8B、2026–2035 CAGR 22.8%，AI 資料中心與 >400G 成長最快；另一 Lucintel 版本數字不一致（2035 年 $3.5B），品質存疑；查無 650 Group／Dell'Oro 數字。","source":"Lucintel, Active Electrical Cable Technology Market Report","url":"https://www.lucintel.com/active-electrical-cable-technology-market.aspx","excerpt":"The global active electrical cable technology market is expected to reach an estimated $6.8 billion by 2035 with a CAGR of 22.8% from 2026 to 2035.","as_of":"2026-06-01","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"報導指出市場擔憂 CPO 隨埠速推向 1.6T 可能取代 Credo 的 AEC 本業；Credo 已於 5/28 完成收購 DustPhotonics 以補光學能力","source":"Crypto Briefing: Credo Technology slides as Wall Street weighs whether optical tech could replace its copper cash cow","url":"https://cryptobriefing.com/credo-technology-copper-optical-replacement-risk/","excerpt":"the concern centers on Co-Packaged Optics, or CPO, which could eventually replace Credo's bread-and-butter Active Electrical Cables as data center port speeds push toward 1.6 terabits per second","as_of":"2026-06-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"SemiVision 分析認為 AEC 是機櫃內短距互連的最佳解，大規模 CPO 部署預期在 2027–2029 之後","source":"SemiVision: The AI Interconnect War – Copper Fights","url":"https://tspasemiconductor.substack.com/p/the-ai-interconnect-war-copper-fights","excerpt":"Active Electrical Cable (AEC) has emerged as the optimal solution for short-reach in-rack interconnects in AI data centers.","as_of":"2026-03-04","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"TrendForce：microLED CPO 功耗可降至銅纜方案約 5%；Credo 以 Hyperlume 基礎的 Active Light Cable 預計 FY2027 送樣、FY2028 量產（廠商/分析師預估，非實測部署）","source":"TrendForce News: micro LED optical interconnect ecosystem","url":"https://www.trendforce.com/news/2026/06/29/news-mapping-the-micro-led-optical-interconnect-ecosystem/","excerpt":"sample shipments expected in fiscal 2027, followed by volume production ramp-up in fiscal 2028","as_of":"2026-06-29","retrieved_at":"20261012","affects":["moat_trend","thesis.R","triggers"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Semtech OFC 2026：銅纜仍是目前叢集規模最務實的 scale-up 互連，光學是並行進入而非取代；並展示 3.2T ACC（448G/lane）","source":"Semtech blog: OFC 2026 Semtech advances the future of AI data center optical and active copper interconnects","url":"https://blog.semtech.com/ofc-2026-semtech-advances-the-future-of-ai-data-center-optical-and-active-copper-interconnects","excerpt":"Copper remains the most practical scale-up interconnect for today's cluster sizes, but as AI clusters expand, optics is entering scale-up alongside copper, not replacing it.","as_of":"2026-03-16","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Evercore 分析師預期 Credo 由銅線為主轉向銅＋光platform，光產品2027年約佔營收25%（分析師觀點，非公司指引）","source":"Invezz: credo stock surges on Evercore $325 target and optical growth outlook","url":"https://invezz.com/au/news/2026/06/22/credo-stock-surges-on-evercore-dollar325-target-and-optical-growth-outlook/","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"搜尋摘要指出分析師把 co-packaged optics 列為對 Credo 商業模式的潛在結構性風險（可能減少獨立連接產品需求）；未找到通路（直銷 vs 經銷）結構轉變的證據","source":"WebSearch 摘要（Credo FY2027 光產品／客戶集中度報導）","url":null,"excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261012","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 FY2027（2026-09-01 公布）營收 $479.0M，季增 9.6%、年增 114.7%；Q2 指引營收 $525–535M。","source":"Credo Q1 FY2027 financial results press release","url":"https://s205.q4cdn.com/511065572/files/doc_news/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results-2026.pdf","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q1 營收 $479M 高於共識 $473.3M，EPS $1.20 高於預期 $1.17，但股價財報後下跌；一說指引（光學 $600M+）低於市場期待，另一說歸因毛利率疑慮，兩說法不一致。","source":"parameter.io / stocktwits 報導","url":"https://parameter.io/credo-technology-crdo-stock-plunges-9-despite-beating-earnings-estimates-on-margin-concerns/","excerpt":null,"as_of":"2026-09-02","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"管理層全年營收成長指引：前季為 >50%，上調至 >80%，Q1 call 重申 >85%；光學營收全年 >$600M。Mizuho 的 Jordan Klein 稱 Q2 指引『a bit skinnier』。","source":"Stocktwits: CRDO Plunges Despite Q1 Beat","url":"https://stocktwits.com/news-articles/markets/equity/crdo-plunges-despite-q1-beat-retail-feels-stock-will-recover-strongly/cZsAfv6RJu5","excerpt":null,"as_of":"2026-09-02","retrieved_at":"20261012","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga：16 位分析師，15 Buy／1 Hold，平均目標價約 $216（9/4）；JPM 目標 $335→$310、Evercore ISI $325→$292（皆 2026-09-02）。7 月快照平均 $215，Barclays 7/20 升至 $300。","source":"Benzinga CRDO price targets","url":"https://www.benzinga.com/quote/CRDO/price-targets","excerpt":null,"as_of":"2026-09-04","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"valueinvesting.io 顯示 27 位分析師平均目標 $263.60、區間 198.19–315.00，無標註日期；與 Benzinga 平均 $216 差異大，口徑未明。","source":"valueinvesting.io CRDO estimates","url":"https://valueinvesting.io/CRDO/estimates","excerpt":null,"as_of":"2026-09-04","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Credo 於 2025-10 宣布收購 Hyperlume（microLED 晶片間光互連）。","source":"Finviz/Zacks: Credo Technology Leans on Inorganic Push to Strengthen AI Edge（經搜尋摘要轉述）","url":"https://finviz.com/news/330882/credo-technology-leans-on-inorganic-push-to-strengthen-ai-edge","excerpt":null,"as_of":"2025-10-31","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Credo 於約 2026-03 隨 FY2026 Q3 財報宣布收購高速連接 IP 公司 CoMira Solutions（日期為約略，來源為搜尋摘要）。","source":"Finviz/Zacks: Credo Technology Leans on Inorganic Push to Strengthen AI Edge（經搜尋摘要轉述）","url":"https://finviz.com/news/330882/credo-technology-leans-on-inorganic-push-to-strengthen-ai-edge","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Credo 於 2026-05 宣布收購 DustPhotonics，一來源稱交易價值 $750M（現金＋股票＋績效獎金），約 2026-06-01 完成（完成日期不同頁面寫 5/29 與 6/1，未確定）。","source":"搜尋摘要彙整（Finviz/Zacks 等）","url":"https://finviz.com/news/330882/credo-technology-leans-on-inorganic-push-to-strengthen-ai-edge","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261012","affects":["moat_trend","valuation","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"三筆收購：Hyperlume（2025-10）、CoMira Solutions（約 2026-03）、DustPhotonics（2026-05 宣布，約 2026-06-01 完成，一來源稱 $750M）。未見 Credo 被併購消息。","source":"Finviz/Zacks: Credo Technology Leans on Inorganic Push to Strengthen AI Edge（經搜尋摘要轉述）","url":"https://finviz.com/news/330882/credo-technology-leans-on-inorganic-push-to-strengthen-ai-edge","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261012","affects":["moat_trend","valuation","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CRDO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.07,"operating_margin_pct":31.74,"fcf_margin_pct":27.57,"rd_intensity_pct":21.46},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO","as_of":"TTM ending 2026-07-31（4季加總）"},"is_subject":true},{"name":"MRVL","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.21,"operating_margin_pct":16.81,"fcf_margin_pct":18.23,"rd_intensity_pct":25.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"ALAB","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":75.13,"operating_margin_pct":22.75,"fcf_margin_pct":23.02,"rd_intensity_pct":36.13},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MTSI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.54,"operating_margin_pct":18.11,"fcf_margin_pct":10.63,"rd_intensity_pct":23.42},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"CRDO"},"financial_history":{"ticker":"CRDO","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-04-30","revenue":184194000.0,"revenue_yoy_pct":null,"gross_margin_pct":57.65,"operating_margin_pct":-10.22,"net_income":-16547000.0,"diluted_eps":-0.11,"free_cash_flow":-46328000.0,"fcf_margin_pct":-25.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-04-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-04-30","revenue":192970000.0,"revenue_yoy_pct":4.76,"gross_margin_pct":61.89,"operating_margin_pct":-19.2,"net_income":-28369000.0,"diluted_eps":-0.18,"free_cash_flow":17085000.0,"fcf_margin_pct":8.85,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-04-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-04-30","revenue":436775000.0,"revenue_yoy_pct":126.34,"gross_margin_pct":64.77,"operating_margin_pct":8.5,"net_income":52183000.0,"diluted_eps":0.29,"free_cash_flow":29022000.0,"fcf_margin_pct":6.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-04-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-04-30","revenue":1335116000.0,"revenue_yoy_pct":205.68,"gross_margin_pct":68.04,"operating_margin_pct":33.33,"net_income":472279000.0,"diluted_eps":2.51,"free_cash_flow":406996000.0,"fcf_margin_pct":30.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-04-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CRDO/CRDO_Q1_2027_Earnings_Call_20260901.md）

# Q1 2027 Earnings Call
**Credo Technology Group Holding Ltd** | Earnings Calls | 2026-09-01

**Operator** (Operator):
Ladies and gentlemen, thank you for standing by. [Operator Instructions]
I would now like to turn the conference over to Dan O'Neil, Treasurer and VP of Investor Relations. Please go ahead, sir.

**Daniel O'Neil** (Executives):
Good afternoon. Thank you all for joining our First Quarter Fiscal 2027 Earnings Call. Today, I am joined by Bill Brennan, Credo's Chief Executive Officer; and Dan Fleming, Credo's Chief Financial Officer.
During this call, we will make certain forward-looking statements. These forward-looking statements are subject to risks and uncertainties discussed in detail in our documents filed with the SEC. These documents can be found in the Investor Relations portion of the company's website. It is not possible for the company's management to predict all risks, nor can the company assess the impact of all factors on its business or the extent to which any factor or combination of factors may cause actual results to differ materially from those contained in any forward-looking statement.
Given these risks, uncertainties and assumptions, the forward-looking events discussed during this call may not occur, and actual results could differ materially and adversely from those anticipated, implied or inferred. The company undertakes no obligation to publicly update forward-looking statements for any reason after the date of this call to conform these statements to changes in the company's expectations or to actual results, except as required by law.
Also during this call, we will refer to certain non-GAAP financial measures, which we consider to be important measures of the company's performance. These non-GAAP financial measures are provided in addition to and not as a substitute for or superior to financial performance prepared in accordance with U.S. GAAP. A discussion of why we use non-GAAP financial measures and reconciliations between our GAAP and non-GAAP financial measures is available in the earnings release we issued today, which can be accessed using the Investor Relations portion of the website.
I will now turn the call over to our CEO. Bill?

**William Brennan** (Executives):
Thanks, Dan, and thank you, everyone, for joining our First Quarter Fiscal '27 Earnings Call. The first quarter was another strong quarter for Credo. Revenue reached a record $479 million, increasing 10% sequentially and more than doubling year-over-year. Non-GAAP gross margin was 68%, and non-GAAP net income exceeded $236 million, up 140% year-over-year. Credo has been growing at a pace that very few semiconductor companies have achieved, all while expanding profitability.
At the heart of this growth is 7 consecutive quarters of triple-digit year-over-year growth. We continue to see outsized growth in fiscal '27 with our optical business growing at the fastest pace. AI infrastructure investment continues to grow rapidly. Cluster sizes are increasing, data rates are moving higher, and connectivity requirements are becoming more challenging. As these systems scale, connectivity is about much more than bandwidth. Reliability, power efficiency, signal integrity, telemetry and serviceability all matter. We also believe AI infrastructure will become increasingly heterogeneous. There will not be 1 architecture, 1 protocol or 1 physical medium that is chosen for every connection.
Future AI systems will combine optical and copper interconnects across different reaches, protocols and topologies with customers choosing the right technology to optimize their architecture. This is where Credo shines. While network reliability remains Credo's North Star, our ability to innovate, execute, qualify and deploy across the wide range of customers' needs is core to our differentiation. Our focus is on helping customers bring clusters up faster, maximize processor utilization and maintain reliable operation at scale. Our portfolio now spans connectivity from millimeters to kilometers with solutions across optics and copper.
Let me walk through each of these areas in more detail. Starting with AECs. AECs remain our largest business and continues to grow. We now have deep relationships with 5 hyperscalers, and our engagement with NeoCloud customers continues to expand. Within our existing customers, we continue to see increased AEC penetration as deployments scale. Higher data rates provide another growth vector with the transition to 200-gig-per-lane 1.6T ports ahead.
AECs have always been a system-level product for Credo. We provide the complete solution and optimize the silicon, firmware, manufacturing test and system qualification together. Our system-level approach has been fundamental to our differentiation since we created the category. As AI clusters get larger, the value proposition remains straightforward, high reliability and low power for short-reach connectivity or both become increasingly important at scale. We continue to see a healthy growth trajectory for AECs, driven by deeper penetration with existing and new customers and with increasing bandwidth in next-generation clusters.
Now turning to optics. Our optical business is progressing very well and includes optical DSPs, silicon photonics PICs and ZeroFlap optical transceivers. Our optical DSP business delivered record revenue in Q1. Revenue included deployments across our 50-gig and 100-gig-per-lane solutions. We see a long tail for 800-gig ports even as we begin the transition to 1.6T solutions. At 200-gig-per-lane, customer engagement with our 1.6T DSP is strong across both fully retimed and LRO solutions. Our first 1.6T DSP revenue remains on track for later this fiscal year.
During the quarter, we also recognized our first silicon photonics PIC revenue following the DustPhotonics acquisition. Our initial wins are in 800-gig and 1.6T optical transceivers, and we expect these products to ramp throughout the year. More importantly, silicon photonics PICs add another important technology to our optical platform. We now optimize the DSP and PIC together and combine them with our firmware, telemetry and PILOT software. This level of integration creates opportunities to improve reliability, power, signal integrity and diagnostics.
It also positions us well as scale-up architectures move toward near package optics. We're seeing increasing customer activity around NPO for scale-up networks with confirmed design wins expected to begin ramping in our fiscal '28. As part of the Open CPX MSA consortium, we'll bring many of the advantages of today's pluggable ecosystem, including telemetry, interoperability and serviceability. Our opportunity here includes both optical components and complete system-level solutions. This is an important evolution for Credo. We've historically been very successful solving connectivity problems at the semiconductor and the AEC system level. We're now applying that same approach to optics.
Our ZeroFlap Optics business continues to progress. ZeroFlap Optics combines optimized optical hardware, PILOT software and switch-level SDK integration to continuously monitor link health and identify and mitigate when link instabilities become likely. The objective is to improve cluster bring-up time and long-term network availability, both of which deliver significant financial advantages and end customer outcomes. Production shipments are underway, and we expect additional customer ramps during fiscal '27 across both 800-gig and 1.6T with both hyperscalers and NeoClouds.
With DSPs, PICs and ZeroFlap Optics, we now address much more of the optical link. That changes the opportunity for Credo. We sell components where that's preferred by customers, but more importantly, we also integrate those components with hardware, firmware and software to deliver a complete optical transceiver with unprecedented system-level reliability. Taken together, the momentum across DSPs, PICs and ZeroFlap Optics keeps us firmly on track to deliver more than $600 million of optical revenue in fiscal '27.
Now turning to Retimers. Our retimer business also delivered record revenue in Q1. Growth was primarily driven by scale-up deployments using our Screaming Eagle retimer at 100-gig-per-lane and with our Blue Heron retimer beginning to contribute at 200-gig-per-lane. We continue to see opportunities for the Toucan retimer as PCIe Gen 6 adoption increases and for Screaming Eagle and Blue Heron across Ethernet and UALink. Scale-up architectures are developing quickly with customers making different choices around protocols, topology and connectivity. Our ability to support multiple protocols allows us to successfully participate across these architectures.
Now I'll discuss 2 important emerging growth areas. We also continue to make progress with both Active LED Cables or ALCs and our OmniConnect gearbox solutions. Our ALC solutions use micro emitters to combine many of the reliability and power advantages of copper with reach of up to 30 meters. Customer engagement continues to increase, and we plan to demonstrate ALC solutions at OCP in October. We remain on target for initial revenue in fiscal '28.
We're also seeing strong engagement around our OmniConnect innovation. Our OmniConnect SerDes and Weaver gearboxes address the fanout issues that come with increasing memory bandwidth and capacity requirements of next-generation AI architectures. This is especially relevant for inference where memory capacity, bandwidth, packaging and costs are becoming increasingly important architectural constraints. We believe OmniConnect solutions can represent thousands of dollars of Credo content per GPU with revenue beginning in fiscal '28.
In conclusion, Q1 was another strong quarter for Credo and customer engagement across the business remains very strong. AECs continue to grow as we expand with existing customers, add new customers and move to higher data rates. Our retimer and optical DSP businesses also delivered record revenue. At the same time, the scope of our optical business is expanding. We believe that the system-level approach will become increasingly important as AI networks move to 1.6T and 3.2T solutions and the scale-up architectures drive greater use of Near-Package Optics. AECs helped take Credo to the scale we've achieved today, and we continue to see growth ahead for that business.
What's different today is that we're adding optics as another major growth engine from a much larger base and as an established player in the industry. Our optical opportunity now extends from DSPs and silicon photonic PICs to complete ZeroFlap Optics and NPO solutions. Our content opportunity expands significantly as we solve a broader set of challenges for our customers. AECs continue to grow. Optics is growing faster. And based on the customer engagements and ramps underway across the portfolio, we remain confident in the outsized growth we expect to deliver in fiscal '27.
The common thread across all these products remains reliability. As AI infrastructure scales, our job is to provide connectivity that works reliably, uses less power, provides visibility into the network and keeps expensive processors operating at high utilization. That's what we're focused on, and we're very excited about what lies ahead.
With that, I'll turn the call over to Dan.

**Daniel Fleming** (Executives):
Thank you, Bill, and good afternoon. I will first review our Q1 results and then discuss our outlook for Q2 of fiscal year '27.
In Q1, we reported revenue of $479 million, up 10% sequentially and above the high end of our guidance range. Year-over-year, revenue grew 115%. Q1 marks another revenue record, driven by substantial year-over-year growth across 4 domestic customers, and marks our seventh consecutive quarter of triple-digit revenue growth year-over-year.
Our top 4 end customers each came in at or greater than 10% of revenue in Q4. As a reminder, customer mix will vary from quarter-to-quarter. We continue to expect that 3 to 4 customers will be greater than 10% of revenue in the coming quarters and fiscal year, and we continue to make progress in diversifying our revenue base across hyperscalers, NeoClouds and other customers.
Our team delivered Q1 non-GAAP gross margin of 68% at the midpoint of our guidance range. Total non-GAAP operating expenses in the first quarter were $95.2 million, above the high end of our guidance range due to our strong R&D investment, and up 16% sequentially. Our non-GAAP operating income was $230.6 million in Q1 compared to non-GAAP operating income of $216.7 million in Q4. Our non-GAAP operating margin was 48.2% in the quarter. Our bottom line once again demonstrated the substantial leverage we are delivering in the business, even with our continued heavy investment in R&D.
Our non-GAAP net income was $236.3 million in the quarter, a record high and a 4% sequential increase compared to non-GAAP net income of $226.7 million in Q4. Our Q1 non-GAAP net income more than doubled year-over-year, clearly demonstrating the magnitude of our top line growth, strong gross margins and disciplined approach to managing operating expenses. Our non-GAAP net margin was 49.3% in the quarter.
Cash flow from operations in the first quarter was $90.2 million, down $92.0 million sequentially due primarily to changes in working capital. CapEx was $7.3 million in the quarter, and free cash flow was $82.9 million. We ended the quarter with cash and equivalents of $764.3 million, a decrease of $679 million from the fourth quarter due primarily to the cash outlay for our acquisition of DustPhotonics. We remain well capitalized to continue investing in our growth opportunities while maintaining a substantial cash buffer. Our Q1 ending inventory was $313.1 million, up $62.2 million sequentially.
Now turning to our guidance. We currently expect revenue in Q2 of fiscal '27 to be between $525 million and $535 million. We expect Q2 non-GAAP gross margin to be within a range of 67% to 69%. We expect Q2 non-GAAP operating expenses to be between $100 million and $105 million. And we expect Q2 diluted weighted average share count to be approximately 200 million shares. These expectations are based on the current tariff regime, which remains fluid.
As we move forward through fiscal year '27, we continue to expect an inflection in the second half, driven by more than $600 million in optical revenue with ZeroFlap Optics, silicon photonics PICs and optical DSPs each contributing more than $100 million, resulting in more than 85% year-over-year total revenue growth for the full year.
We expect non-GAAP gross margin in fiscal year '27 to be broadly consistent with fiscal year '26 levels. We expect non-GAAP operating expenses to increase approximately 55% year-over-year, well below our revenue growth rate as we continue to invest in R&D to support the new product development and address the significant growth opportunities ahead. As a result, we expect our non-GAAP net margin to be in the vicinity of 50%.
And with that, I will open it up for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Tore Svanberg with Stifel.

**Tore Svanberg** (Analysts):
Congrats on the record quarter. Bill, I was hoping you could unpack a little bit the position in optical right now. You did reiterate the $600 million plus, but now you also talked about NPO and maybe even doing some system-level NPO. So as we think about that $600 million, both in fiscal '27 and fiscal '28, how should we expect the mix to look like between all the various different components?

**William Brennan** (Executives):
Sure. I think we feel great about the broadening portfolio that we're bringing to market. As we've indicated, the optical DSP business for us is doing quite well at a component level. The team that came in to Credo from Dust brought a lot of momentum. And in fact, after just a few months, the momentum has picked up, and we're happy to be able to say that we've got design wins with 2 major players for next-generation ramps that will occur in fiscal '28 and maybe starting in the late part of this fiscal year.
ZF Optics, we continue to make progress. We're engaged with multiple customers, both hyperscalers and NeoClouds. And we feel good about the way that the year is shaping up. I think as I think about the overall optical opportunity, and you did mention CPX, and I think you may have all seen the press release earlier that we have joined the consortium. And we plan on pursuing solutions for the scale-up market that's developing really across the board.
CPX is, I think, an important development in the industry. That's one way of solving the challenge of going to 10x more density than what you're seeing in scale-out. And we'll pursue this market the same way. We'll pursue component sales where that makes sense with customers, and we'll also pursue system-level solutions that we'll talk about over time.
But you bring up an important point. Fiscal '27, I think, is just a stepping stone for where we're going with our optical business. And if we think about the market forecasters, specifically the ones that are focused on the optical transceiver pluggable market, just that piece alone is expected to grow from 60 million units in '26 to 175 million units by 2030. This is amazing growth for this portion of the industry, and then add growth on top of that for what happens in scale-up.
And so we think that with our broad portfolio of solutions that we're going to experience continued outsized growth through the 2030 time frame. And it's going to have contributions from not just our optical portfolio, but also AECs as well as our other copper solutions. So I probably gave you a little more color than you asked in that question. So hopefully, that gives you what you're looking for.

**Operator** (Operator):
Your next question comes from the line of Quinn Bolton with Needham.

**Quinn Bolton** (Analysts):
Bill, I guess a question just on a follow-up to Tore's question. Just really wanted more color on the importance of Credo joining the Open CPX consortium, what types of solutions you may be providing? Is it more kit-based? Would you be supplying the full optical engines? I assume these are all laser-based rather than microLED-based, but maybe just a little bit more detail on this new opportunity that's opening up for you in the NPO scale-up segment.

**William Brennan** (Executives):
Sure. So as we all think about the scale-up opportunity, we're thinking about a changing of form factors. When we look at front-end and we look at scale-out, there's no real catalyst to change from the pluggable form factor. But for scale-up networks, there's a fundamental need to have more dense form factors. And we've talked, there's been an ongoing industry conversation about things like XPO, CPX, how that fits in with NPO and then ultimately CPO. All of these solutions address the need for a 10x density improvement.
And the way that we're approaching the market is somewhat agnostic. We will basically look at what our customers are asking us and what our customers are driving towards. And so we've, I think, done a very good job of being agnostic as it relates to the solutions that we're bringing to market. We're going to continue to do that. And so of course, with all of the NPO solutions, including CPX, we'll lead with the silicon photonics PIC, but we'll also look at doing the complete optical engine long-term as we add more functionality to our portfolio.

**Operator** (Operator):
Your next question comes from the line of Tom O'Malley with Barclays.

**Thomas O'Malley** (Analysts):
So mine relates to the ZF Optics side as well. So like when you look at the forecast that you have kind of over the next year and then in the year after that as well, like a lot of the volume in terms of revenue is driven by the ZF Optics forecast. And like it's unique. You imagine that you're going to use a contract manufacturer for this. And you're hearing about supply issues, raising prices in the foundry world.
Like can you talk about like challenges that you're facing in scaling today? And what gives you the confidence that you're able to kind of hit the metrics that you gave us some color on the last earnings call. But like what gives you the confidence that you're able to hit those really big revenue numbers in the near term? And just maybe a little bit of a pulse check on conversations with customers today, particularly those who in the media have potentially been spending a little bit more money and the forecast is raised on the ZF Optics side?

**William Brennan** (Executives):
Yes, you point out something that's lots of fun. We're in a very dynamic market right now. And you're right, from the supply side, it has been important that we have spent so much time even going back 18 to 24 months ago, and we knew that this was a direction that we're heading. And so you can see from Dan's update, that working capital is increasing. We're leaning in from a supply chain standpoint. I feel great about our ability to supply increasing volumes in our second half and then throughout the next couple of fiscal years.
The other half of that is driving demand. And so I see that over the past year, we've been very successful in marketing and really engaging with customers. And so all of this has got to come together. But again, I'll point out that we're really playing the long game here. And of course, there's -- there should be, and there is a lot of emphasis on the very fast ramp that we've set expectations on. But I think more importantly, looking at the big picture, this involves an opportunity that takes us to a different scale as a company. And so this is very much an important part of our growth strategy and our scale as a company.

**Operator** (Operator):
Your next question comes from the line of Sean O'Loughlin with TD Cowen.

**Sean O'Loughlin** (Analysts):
Congrats on the solid results and momentum. Maybe we could just get some blocking and tackling on the -- Dan, you mentioned the 3 to 4 customers will be greater than 10%, and you're continuing to diversify. I wanted to ask specifically maybe if you could do the rundown of what the stats were on those 3 to 4 in the quarter. But then also when we think about customer concentration, there's also platform concentration? And are you diversifying your product portfolio across those customers as well?

**Daniel Fleming** (Executives):
Yes, sure. Let me start with just the percentages of those 10% plus customers. So our largest customer was 1/3 of our revenue at 33%, second largest 28%, and then followed by 13% and 10%. Those top 3 customers were similar to or the same 3 as in the prior quarter in a slightly different order. One thing to note, our fourth 10% customer right at 10% was different from our 10% fourth customer last quarter. They have been a 10% customer in the past. Now in terms of diversification of product line within those, for sure, there is a strengthening and broadening across the board. It isn't just AECs that these hyperscalers are consuming in volumes.

**Operator** (Operator):
Your next question comes from the line of Blayne Curtis with Jefferies.

**Blayne Curtis** (Analysts):
On the AEC side, I just wanted to ask you timing on 1.6 terabit, but also just the design traction if you compare that versus the 800-gig. You've been talking about NeoClouds. I think some of your existing customers are moving to faster speeds. Can you just give us a perspective of how those designs are laid out and the timing?

**William Brennan** (Executives):
Sure. We expect that our AEC portfolio will ramp in a similar kind of time frame as the rest of the market and for that matter, our ZF Optics products. I want to step back and give some perspective on the way we view the AEC market. There's been a lot of conversation about copper and optical and just the trade-off there. And the way that we view the AEC market, and it is part of the pluggable transceiver market. So when we talked about forecasts for specifically optical transceivers going from 60 million to 175 million over the next 4 years, there's not really a breakout for the AEC market, but the AEC market really represents the 1-meter to 7-meter segment of that market. And so it just makes sense that, that segment is going to grow as well.
And we see that really being long-term. We see that in a big way in the 800-gig category, what we saw was copper replacing optical. And it was replacing optical laser-based optical transceivers because of the need for higher reliability and secondarily, lower power as it relates to that first connection in the network from GPUs to that first switch.
And so the bottom line is that we see the pluggable transceiver market for all of the pluggable transceivers from copper to laser-based optical. And ultimately, we'll talk about ALCs being another pluggable transceiver option within the spectrum and that going up to 30 meters.
And so as it relates to what I think the setup looks like for 1.6T, we're quite bullish about the AEC opportunity. And as we showed going back 6 months ago at OFC, many of the next-generation deployments that have been discussed in the industry, we showed very elegant solutions, all connected with AECs and we'll deliver up to 6.5 meters in that category. So we think it takes shape towards the end of -- or towards -- there will be some contribution in our second half fiscal '27 and then fiscal '28, it comes in, in a much bigger way.

**Operator** (Operator):
Your next question comes from the line of Joseph Cardoso with JPMorgan.

**Unknown Analyst** (Analysts):
This is MP on behalf of Joseph Cardoso. So I just wanted to ask on the overall opportunity. Till date, most of the opportunity has been -- and the focus has been on training, but we are seeing incremental development around inferencing as well now. So I just wanted to check how does Credo is positioned in terms of addressing the inferencing opportunity and which part of the portfolio particularly stands out? And how does the overall opportunity compare relative to training?

**William Brennan** (Executives):
Appreciate that question. I'd like to maybe talk a little bit about our OmniConnect solutions that we are bringing to market now and that we expect to contribute revenue in our fiscal '28. And specifically related to inference, as these solutions continue to gain momentum, one universal issue is around memory fanout. The memory fanout issue is limiting bandwidth and also total memory deployment of memory capacity, both of which are critical to achieving high-performance inference.
And so with our OmniConnect solutions, there's kind of a 2-piece story to the offering. First thing is we license a highly optimized high-speed SerDes that's got a very small form factor, very low power and that's got reach of up to 10 inches. And so effectively addressing the fanout issue that exists on the XPU beachfront as well as the distance that you can get -- the distance you can achieve between the GPU and memory. So the second piece is the gearboxes that we're developing. The first gearbox that we're developing is a solution that we call Weaver. And it is a gearbox that interfaces between that embedded SerDes on the XPU. So it's up to 10 inches reach and interfaces with that same exact SerDes. And then it becomes an LPDDR interface.
And it's important to note that our first product will be LPDDR5, and there will be a second product we do for LPDDR6. And so in a sense, this architecture is future enabled because when the memory market shifts from 5 to 6, there isn't going to be a need for our XPU partners to do another tape-out, another design, just simply change the gearbox.
And so our first customer, Positron, is doing really, really great things. When we look at memory limitations and the opportunity that if you can increase memory capacity up to 2 terabytes, which is their first announced product, just the performance with frontier model or frontier models, basically, you can hit everything in memory and your performance just goes off the charts. And so they're redefining what is competitive in that space.
And if we look even from a bandwidth standpoint, we've got a road map that will achieve very comparable bandwidth to even HBM5. And that's while expanding on memory size and eliminating the reliability issues of packaging XPUs and HBM in the same package. But related specifically to inference, we're really excited about how this is really going to change the game for many frontier model applications.

**Operator** (Operator):
Your next question comes from the line of Vivek Arya with Bank of America.

**Vivek Arya** (Analysts):
Bill, I wanted to go back on the AEC growth in the second half and then longer term. If I take your 85% growth outlook for the year, suggest about $500 million of incremental growth in the second half. But if optics is going to be the bulk of it, then that $600 million, that suggests kind of more conservative assumptions about AEC growth. I'm sure that I'm probably mistaken about how much optics was in the first half or so.
So I was just hoping if you could kind of give us some more details on the optics versus AEC segmentation in the first half versus second half and what that implies for AEC growth in the second half? And then how should we model AEC growth longer term?

**William Brennan** (Executives):
Sure. I think that as we look at the entire year and we look at the growth across each one of the products that we're bringing to market, we see growth across the board. Now of course, with our optical solutions, this is really the first year that we're ramping, and it makes a lot of sense based on what we're bringing to market that we'll be able to achieve a really fast-paced growth. I think AECs will continue to grow. You've got to consider where we've grown from. AECs have driven growth over the last 2 fiscal years, more than doubling from '24 to '25 and then more than tripling from '25 to '26.
And so I think that as we look at our opportunities in AEC, we continue to see expanding opportunities. But in a sense, I think we're looking at clearly a slower growth overall compared to the fact that we're growing into such a large market with optics. And so it makes sense that optics will grow faster because we're growing from a smaller base. But long-term, I think you'll see AECs grow. And as we continue to scale as a company, I think you'll see balance -- a really nice balance between copper solutions and optical.

**Operator** (Operator):
Your next question comes from the line of Sebastien Naji with William Blair.

**Sebastien Cyrus Naji** (Analysts):
I just wanted to maybe ask a little bit about PILOT and some of the telemetry data that your solutions are picking up. As your installed base grows, are you accumulating enough link-level telemetry that the data itself is becoming a bit of a competitive advantage, for example, allowing you to identify failure modes or optimize future DSP designs? And is that extending your moat at all? Just any thoughts on that?

**William Brennan** (Executives):
Sure. The PILOT software platform is a really important part of the total ZF Optics offering. And when we look at what we've done, we basically had to start with a custom DSP design, one that would enable telemetry to be lit up on every link between an XPU and a switch. And when I say every link, there's really 6 in total. There's 3 in one direction and 3 in the other. And this is completely different than the telemetry that has been discussed up to this point in the industry.
And so what we're able to sense on a real-time continuous basis is really rich telemetry data that looks on indicators of link stability, even going down to the SerDes level because that, of course, is core to our platform on everything we do. But we're looking at a real-time measurement of eye height and SNR post-histograms, really rich telemetry data even down to that level.
And so when we are sensing this continuously, we can sense when the link integrity is decreasing. And so you can think of it as right now in the industry, what exists is a green light when you've got a connection and a red light when there's a failure. What we're adding is like a check engine light, a yellow light that says, okay, you've identified something. And then the mitigation piece of it is about acting. And so there's different approaches that are enabled by PILOT. You can make the decision on a transceiver-by-transceiver basis to take that transceiver that looks likely to have a link flap and in an orderly way, take that GPU out of the cluster.
We've got other customers that are looking at a network level, more of a centralized approach. And the ultimate outcome is the same from a reliability standpoint. But in this case, both opportunities allow you to collect a tremendous amount of data because as you're taking a link down, you've got a snapshot of exactly what was happening within that transceiver and what's happening within the network. And so you're right that the data set that we're starting to gather and that we will gather over time will lead to better solutions. It will lead to next-generation solutions being optimized even more so for the types of failures that we're detecting early.
I will say we're doing other things that are really interesting, and that's related to conversations with customers. We had a customer ask us, can you sense even the slightest ESD damage on a transceiver because that will become a latent defect. And so we figured out a way to sense even the slightest ESD damage, not the type of damage that would cause a transceiver to fail, but the type of damage that over time would result in a failure in that connection. And so now when we've got customers lighting up racks, they can determine immediately if a transceiver was mishandled and needs to be replaced.
Other things that we're sensing is dust on the fiber plant. This is really, really important because even the smallest speck of dust can have light bouncing back in the other direction, causing a multipath interference situation. And so what we're doing is far beyond. Now PILOT allows us to iterate within the network at our customers. And that really just changes the game on giving our customers tools to be active in identifying and mitigating.
And look, the goal here is twofold. It's really to deliver the fastest time to revenue. So bringing a cluster up in 5 or 6 days versus 6 to 8 weeks. I think we've seen the contracts that have been reported in the market, you can measure a month on the order of hundreds of millions or even $1 billion of advantage when you've got that really expensive gear that could be generating revenue, but it's sitting idle because you're trying to bring a cluster up and on the order of weeks versus days.
The other big one is uptime after deployment and driving to a 99% uptime or even higher is the objective here. And that just delivers a better fabric, better product for the end customers. And so it's a huge differentiator, I think, at a cluster level. But yes, PILOT is critical to enabling that. It's a combination of the custom hardware, but the interface within the network is really the critical piece.

**Operator** (Operator):
Your next question comes from the line of Karl Ackerman with BNP.

**Karl Ackerman** (Analysts):
Great. [indiscernible] DSPs and PICs, aren't direct hyperscaler sales growing as a portion of your mix versus optical module suppliers? And how does that improve your customer visibility and stickiness with your data center customer base?

**William Brennan** (Executives):
Karl, I apologize. You -- the first part of your question, we didn't hear. So I just want to make sure I got the right perspective.

**Karl Ackerman** (Analysts):
Sure. Yes. As we think about the opportunity for your discrete DSPs and PICs of that $600 million and also growing over time, isn't the customer mix moving more toward direct hyperscaler sales who are making their own custom transceivers? And as they do that, how does that improve your customer visibility and stickiness with that customer base?

**William Brennan** (Executives):
When -- so in looking at our optical components business, this is a really important part of our business short term and long term. And ultimately, it's the path where we're going to pursue that pluggable optical transceiver market that is based on mainstream standards. And the combination of having an optical DSP and a PIC and being able to offer that system level even within a component offering, that will help our customers deliver what we see as the most competitive combination of system performance, power and yield.
Many times, our module customers are working directly with hyperscalers. And the hyperscalers are active in basically pointing to the components that they want to be put together within the modules that our module customers offer. And so the hyperscalers play a big role in both the component sale part of our business to our module customers as well as our ZF Optics modules that we're building ourselves.
Long term, I think that, that is going to be a balance that we see that will continue to where we're going to see that, in fact, our component sales and our module sales will be complementary in the sense that the broad part of the market will be addressed by components and a very specific part of the market that really, really is focused on reliability will be kind of a new product that's offered in that transceiver space.

**Operator** (Operator):
Your next question comes from the line of Vijay Rakesh with Mizuho.

**Vijay Rakesh** (Analysts):
Just a quick question. You mentioned -- just taking a step back, you mentioned 2027 is a stepping stone, and you're already growing like 85% year-on-year. As you look out to fiscal '28, can you give us some perspective on how to look at it? Obviously, AEC is growing might be like 50% this year. You have ZF Optics ramping and SiPho -- the ZF Optics and SiPho is like $600 million for fiscal '27, which kind of annualizes like $1 billion plus run rate. And as you mentioned, Active LED cables as well. As you have all these 4 segments ramping, can you kind of give us some perspective on how to look at fiscal '28?

**William Brennan** (Executives):
I appreciate that. The conversation about fiscal '28 and '29 and '30 is something that's a very active conversation within our leadership team at Credo.
Let me first touch on ALC as a part of our portfolio. I think this is -- the ALC product that we're bringing to market first is using microLED technology. And the promise of this technology is really to deliver the same reliability and the same power efficiencies at a core technology level as AECs. Key difference there is we'll extend the length of 30 meters. And so it's going to -- ALCs will represent our third differentiated pluggable transceiver solution. So different things we first did kind of created the product category with AECs, followed by ZF Optics, again, creating a new product category. ALCs will be the third leg of that stool.
The bottom line is I look at that pluggable transceiver market, and I think that's just step 1 for ALCs and the micro emitter technology. A next natural step forward on that is to apply that to what comes with the scale-up opportunity because, again, in scale-up, this is another technology alternative, but the promise there is that at a core technology level, we'd be addressing some of the problems that have prohibited that market from taking off with solutions specifically related to reliability, availability and serviceability.
And so we view ALC as a big multibillion-dollar opportunity, followed by as big of an opportunity with scale-up and it's highly complementary to the suite of technologies that we brought to market. So the way that I think about the future, more specifically to answer your question is that we're trying to put ourselves in several multibillion-dollar TAM opportunities. You can just analyze our portfolio across the pluggable space. And you can see that it's really tens of billions of dollars of opportunity that we're now going to be addressing in our fiscal '28 time line given the fact that ALCs will be part of the portfolio.
And so we're trying to put ourselves in a position to address a very large market. Our growth as a company will follow based on our success in executing with every customer. I think we're quite bullish on the opportunity. And that's without even talking about the massive opportunity that the entire industry has in front of us with scale-up. Even think about OmniConnect, we've articulated in the past that that's a multibillion-dollar opportunity annually as well. And so I think that as we think about fiscal '28, you're right, we think about outsized growth again for another year, but we think that will continue for the years to follow as well.

**Operator** (Operator):
Your next question comes from the line of Mark Lipacis with Evercore ISI.

**Mark Lipacis** (Analysts):
Bill, I think for you, optics is growing faster. It's a newer market. Can you contrast how you are prosecuting the optics market compared to how you prosecuted the AEC market? I have to imagine there's some differences given you effectively created the AEC market. And maybe as part of that, what are the implications on the business model as optics becomes larger? And to the extent that you can talk about like where you get leverage between these businesses on development and the supply chain with your customers and where you need to build capabilities?

**William Brennan** (Executives):
There is a pretty interesting contrast between the efforts that we pursued with AECs and some of the leverage and how it looks different this time with ZF Optics. With AECs, we imagined this product as being an extension to copper, basically addressing some of the issues that our customers are facing as they were going to faster speeds and they were having issues back. We were surprised when we had customers pursuing us talking about really interesting innovations at a feature level, things like telemetry, things like other system-related rack-level innovations. And we really opened that door to the customer base on feature set innovation.
Our first customer, Microsoft, the reason that they converted to AECs was really the functionality that we offered. We developed a solution that was smart enough to sense when a ToR port was failing or about to fail and then switching the data to a redundant ToR in a hitless manner. Really, really smart solution in a cable format.
Over time, the momentum built, and this is over years, momentum built because as speeds increased, it was clear that DACs weren't going to cut it from a signal integrity, but also from a form factor standpoint with the copper wires needed to become much, much thicker. So from a form factor standpoint and a signal integrity standpoint, many of the customers started looking. And then again, I mean, if we look at our solutions today, many of them have really innovative feature set solutions.
And so the growth happened over -- that product category creation happened over several years. As part of developing our solution and having it be a complete solution and taking ownership of it, we developed a really differentiated way of coming to market from a qualification standpoint. The rigor that we put our solutions through is sometimes far beyond what our customer calls look like. And that includes having our customers' switches, our customers' NICs running at speed as we're hammering the link, the entire link, not just our AEC, but the entire link from link to switch.
And the objective is to harden the solution, finding link weaknesses and then hardening that through firmware modifications. So that was definitely something that we're leveraging now as we bring ZF Optics to market. But the difference with ZF Optics was that AI happened and AI networks were fundamentally different than, say, front-end networks where there was kind of a built-in redundancy within the different tiers of the network. And so we've had link flaps for a long time, but they just haven't surfaced as a major concern because there wasn't any massive hit to the network.
But now that we've got AI clusters, you've got tens of thousands, if not hundreds of thousands of links that are all interdependent that if you start getting flaps on some of those links, it can affect the entire cluster to the point where customers have talked about losing GPU utilization on the order of greater than 10% or even approaching 20%. So there was a -- with this new application, it was a perfect fit for following the playbook on AECs and doing interesting things, very innovative things in an area where innovation had not happened for many years, working closely with customers and basically charting the path to at a system level, be able to improve reliability of the network. That was really the difference. And it took some time to develop the hardware and the software solution.
But we're seeing that the market is taking off a lot faster than AECs because we're addressing a pain point that exists, clearly exists already. So this is welcome every time we have a conversation with the technical networking teams within the customer base.

**Operator** (Operator):
Your next question comes from the line of Suji Desilva with ROTH Capital.

**Sujeeva De Silva** (Analysts):
Congrats on the progress and the margins. You've given us a lot of color on the optical and kind of dug into how you're approaching it. I'd like to take the time to revisit the competitive landscape and how you think competitors are approaching the markets you're approaching, whether you're approaching it differently? Are they going to be able to approach the feature-driven approach the way you are? Or any other elements that are key to kind of how you're doing it that really allow you to separate from the group because a lot of people talking about the same opportunities.

**William Brennan** (Executives):
Sure. I think it's -- I think there is a case to be made here about our go-to-market strategy and the fact that we are owning the entire stack. And I think when we look at the opportunity just at a transceiver level, starting with the SerDes and then looking at it from a DSP and now a PIC perspective, being vertically integrated gives huge advantage on your ability to deliver the best possible system solution, but it also gives you an advantage on COGS.
Then you think about going to market with a solution that's differentiated and the challenge is what are those features worth. And so I think we expect an advantage at a COGS level, but we also expect an advantage on an ASP level as we compare our solution to more standards-based solutions in the market.
I do think that long-term, we are now the pacesetter on innovation in the optical space. The market needs it. And we're being pretty open with working with the standards groups on standardizing around some of the things that we're doing. And the challenge there is how can we innovate faster than the rest of the competition, the rest of the market. And I think we feel comfortable given the fact that we own the entire stack that, that's going to lead to the same kind of success that we've had with AECs.

**Operator** (Operator):
Your next question and final question comes from the line of Christopher Rolland with Susquehanna.

**Christopher Rolland** (Analysts):
And Bill, I will bite on your DSP plus PIC integration that you've mentioned quite a few times. I guess, first of all, if you could talk maybe a little bit more about your 2 Dust wins. Do they include DSP integration? And if you could remind us kind of the economics for this part for this market and what it means to you guys, that would be great.

**William Brennan** (Executives):
Appreciate the question. The world we live in at a component level is quite competitive. And so just by proper protocol, we're not able to talk too specifically about exactly which of the major players that we're engaged with. I will say that these first 2 major design wins that we're talking about do not include the DSP. So there's upside potential with that as we look at really co-marketing the DSP and the PICs long-term.
Right now, it's -- the Dust team was really doing a great job with engaging deeply with major players in the industry. Amazing that a small team like that had such great traction. And I think it's evidence of the fact that their technical solution is absolutely leading edge in the market.
Long-term, I think there's going to be a great opportunity for us to look at these 2 components and really bring a lot of benefits for the customer base. So I look at this as a great development in our overall portfolio and going to be really promising long-term for us.
So I guess with that, we'll wrap up the call. So I really appreciate you all attending, and thanks for the thoughtful questions. We look forward to the follow-up. Thanks so much.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CRDO_Q4_2026_Earnings_Call_20260601.md
- 2026-06-01｜CFO｜guidance：CFO 給 FY27 Q1 營收指引 4.65–4.75 億美元（原話："Q1 of fiscal '27 to be between $465 million and $475 million"）
- 2026-06-01｜CFO｜margin：Q1 non-GAAP 毛利率指引 67%–69%（原話："Q1 non-GAAP gross margin to be within a range of 67% to 69%"）
- 2026-06-01｜CFO｜guidance：FY27 上半年季增中個位數、下半年轉折，全年營收成長逾 80%，光學逾 6 億美元（原話："we expect mid-single-digit"）
- 2026-06-01｜CEO｜guidance：FY27 光學三條產品線各逾 1 億、合計逾 6 億美元，下半年加速（原話："ZeroFlap optics will each contribute more than $100 million"）
- 2026-06-01｜CFO｜margin：FY27 non-GAAP 毛利率預期與 FY26 大致持平（原話："gross margin in fiscal year '27 to be broadly consistent"）
- 2026-06-01｜CFO｜margin：FY27 non-GAAP 營業費用年增約 50%，淨利率約 50%（原話："operating expenses to increase approximately 50%"）
- 2026-06-01｜CFO｜margin：FY27 營收成長絕對金額約一半來自光學、一半來自既有銅線（AEC 為主、含 retimer）（原話："half of that growth in absolute dollars is coming from our"）
- 2026-06-01｜CFO｜customer：Q4 四家客戶占比 ≥10%，最大客戶占 34%、第二 27%、第三 16%，第四為 10% 且 FY26 先前未達 10%（原話："34% for the largest, 27% for the second largest"）
- 2026-06-01｜CFO｜customer：管理層預期 FY27 客戶更分散，仍預期 3–4 家客戶占比逾 10%（原話："We continue to expect that 3 to 4 customers will be"）
- 2026-06-01｜CEO｜customer：CEO 表示 Neo cloud 客群合計可達營收約 20%（原話："I definitely think it could be on the order of 20%."）
- 2026-06-01｜CEO｜customer：AEC 已在 6 家超大規模業者中的 5 家大量出貨，僅 xAI 視為完全部署（原話："we're deployed and we're high volume"）
- 2026-06-01｜CEO｜product：收購 Dust Photonics 已於上週完成，帶來矽光子 PIC 技術與 800G/1.6T 組合（原話："the acquisition of Dust Photonics, which closed last week"）
- 2026-06-01｜CEO｜product：CPO／NPO 設計首批營收預期落在 FY28（原話："initial revenue for CPO and NPO designs is expected in our"）
- 2026-06-01｜CEO｜product：ALC 與 OmniConnect 的量產爬坡預期自 FY28 開始（原話："production ramps for both ALC and OmniConnect solutions"）
- 2026-06-01｜CEO｜product：Weaver 首家客戶 Positron，每顆 GPU 營收貢獻 2,000–3,000 美元（原話："the revenue contribution per GPU can be"）
- 2026-06-01｜CEO｜product：離散光學 DSP 與 PIC 為兩位數美元 ASP，ZF Optics 為三位數 ASP，將是光學最大營收貢獻者（原話："On the ZF Optics, we're going to see 3-digit ASPs."）
- 2026-06-01｜CEO｜commitment：三條光學產品線各自年增皆逾 80%（原話："each one of these categories independently is"）
- 2026-06-01｜CEO｜risk：FY27 的 200G/lane 營收預期偏輕，因業界尚未到位，且 1.6T 時程取決於 Rubin 與各客戶策略（原話："There is a significant tightness in the supply chain"）
- 2026-06-01｜CEO｜risk：管理層指供應鏈有顯著吃緊，3 奈米產能亦在討論中（原話："We feel confident that we're going to achieve"）
- 2026-06-01｜CEO｜commitment：對 ZF Optics 下半年積極爬坡有信心，並稱次年可再成長兩到三倍（原話："We feel confident that we're going to achieve"）
- 2026-06-01｜CFO｜risk：指引基於當前關稅制度，並稱該制度仍在變動（原話："we have no current plans to raise any additional capital"）
- 2026-06-01｜CFO｜capital_allocation：無新增募資或庫藏股計畫；Dust 收購 Q1 淨現金流出約 7.5 億美元；可能有機會型收購但無近期標的（原話："the net cash amount that you'll see in Q1"）
- 2026-06-01｜CFO｜capital_allocation：Dust 收購於 Q1 的淨現金流出金額（原話："zero-flap AECs deliver up to 1,000x greater reliability"）
- 2026-06-01｜CEO｜competition：CEO 稱 AEC 可靠度為商用雷射光模組的最高 1,000 倍且耗電更低（原話："I think we can make a case where we will achieve 50-50"）
- 2026-06-01｜CEO｜competition：CEO 認為長期光學與銅線營收可達 50-50（原話："operating margin was 49.6% in the quarter, flat sequentially"）
- 2026-06-01｜CFO｜margin：Q4 非 GAAP 營業利益率 49.6%、與上季持平；毛利率 68.3% 高於指引上緣（原話："based on the current tariff regime, which remains fluid"）

### CRDO_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md
- 2026-09-10｜CEO｜guidance：CEO 重申 FY27 每季季增 10% 以上。（原話："10% or greater sequential level quarterly"）
- 2026-09-10｜CFO｜guidance：CFO 拆解下半年季增節奏：Q3 約 20%、Q4 約 30%。（原話："call it, 20% into Q3, 30% into Q4"）
- 2026-09-10｜CFO｜guidance：CFO 說單季 10 億美元營收在 FY28 初可見。（原話："$1 billion quarter is within our sights"）
- 2026-09-10｜CFO｜margin：CFO 說 FY27 毛利率指引與上年大致相當。（原話："broadly consistent with last year"）
- 2026-09-10｜CFO｜margin：CFO 指最近一季毛利率落在 68%，與先前暗示一致，法說會上無人問毛利率。（原話："we were right at 68%, which is what we had alluded to"）
- 2026-09-10｜CEO｜margin：CEO 以 ASP 與 COGS 兩因素說明光收發模組毛利率論證。（原話："ASPs and COGS widening the gross margin"）
- 2026-09-10｜CFO｜margin：CFO 說今年營收成長約比 OpEx 快 50%。（原話："our top line is growing about 50% faster than our OpEx"）
- 2026-09-10｜CFO｜guidance：CFO 表示進入 FY28 時營收與 OpEx 成長比可能回到 2:1，並稱 FY28 未給具體指引。（原話："you may see us get back to a 2:1 ratio"）
- 2026-09-10｜CEO｜commitment：CEO 預期光學產品 FY27 底月產數十萬顆。（原話："producing hundreds of thousands of units per month"）
- 2026-09-10｜CEO｜commitment：CEO 表示光學產能到 FY28 底會倍增乃至三倍。（原話："increase that production rate to double and then even triple"）
- 2026-09-10｜CEO｜product：ALC（微發光體線纜）預計下月 OCP 展示，FY28 量產。（原話："be in production in FY '28"）
- 2026-09-10｜CEO｜product：CEO 稱微發光體技術可達 30 公尺。（原話："it will reach 30 meters"）
- 2026-09-10｜CEO｜product：CEO 稱 ALC 線纜體積比 AEC 小 75%。（原話："75% smaller from a total volume"）
- 2026-09-10｜CEO｜product：CEO 表示公司將自建 ZeroFlap 光收發模組（進入模組業務）。（原話："We're going to build ZeroFlap optics"）
- 2026-09-10｜CEO｜product：CEO 說 FY28 時間框架微發光體 ALC 與記憶體牆產品將起飛，並視為超預期機會。（原話："we're going to see those products take off"）
- 2026-09-10｜CEO｜customer：CEO 述 xAI 為 ZeroFlap 緣起客戶，轉用 AEC 後達 99.9% 稼動。（原話："They've achieved 99.9% uptime."）
- 2026-09-10｜CEO｜customer：CEO 述 Oracle 因 NIC 至首層交換器距離超過 7 公尺無法用 AEC，促成光學方案。（原話："our connections between the NIC and the first switch"）
- 2026-09-10｜CEO｜customer：CEO 說每家客戶拉貨節奏各異，10% 客戶季間有明顯暴增與暫停。（原話："great variations quarter-to-quarter"）
- 2026-09-10｜CEO｜customer：CEO 列出超預期來源含深化現有合作與擴展 Neocloud。（原話："expanding in the Neocloud area"）
- 2026-09-10｜CEO｜competition：CEO 稱銅光之爭將是異質並存，公司自我定位為不挑媒介的連接公司。（原話："we believe it's going to be heterogeneous"）
- 2026-09-10｜CEO｜competition：CEO 稱擁有整套系統方案是最大護城河。（原話："that's probably our biggest competitive moat"）
- 2026-09-10｜CEO｜competition：CEO 稱自己是市場上唯一垂直整合的光收發業者。（原話："we're the only vertically integrated player in the market"）
- 2026-09-10｜CEO｜competition：CEO 引述 7 公尺以上光模組單位數預測從今年 6,000 萬到 2030 年 1.75 億。（原話："175 million units by 2030"）
- 2026-09-10｜CEO｜capital_allocation：CEO 表示將持續併購優秀工程團隊與互補技術。（原話："We'll continue down that path from the standpoint"）
- 2026-09-10｜CEO｜capital_allocation：CEO 稱業務範圍不設明確界線，核心連接以外需是差異化系統方案。（原話："identifying great engineering teams"）
- 2026-09-10｜CEO｜commitment：CEO 稱未來數年第一優先是執行。（原話："execution is by far the most important thing"）
- 2026-09-10｜CEO｜risk：CEO 提醒不宜以過短期間過度解讀客戶季間波動。（原話："it can be a little confusing"）

### 問答異常語氣（迴避／改口／保留）
- CRDO_Q4_2026_Earnings_Call_20260601.md｜問：Tore Svanberg 追問三條光學線中哪條明顯高於 1 億美元｜答法：CEO 先答成長廣泛、各線年增逾 80%，未直接給各線金額；後續追問才表示 ZF Optics 為最大貢獻者但仍未給數字，且自述「didn't mean to be a bit elusive」
- CRDO_Q4_2026_Earnings_Call_20260601.md｜問：Vijay Rakesh 問 1.6T／200G 何時放量及 ZF Optics 客戶數｜答法：CEO 未給時程與客戶數，改談客戶設計彈性與雙埠方案，稱 FY27 的 200G 營收相對輕
- CRDO_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：近期 AEC 需求、部署時程與採購型態是否改變？｜答法：未回答近期需求數字或趨勢，改談客戶各自節奏與季間暴增／暫停，並稱不宜短期過度解讀。
- CRDO_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：AEC 作為成長動能在 3–5 年的持久性憑什麼有信心？｜答法：先說可談 AEC 的擴張，隨即轉向整體產品組合與『成長更快的其他部分』，未給 AEC 自身的量化持久性。
- CRDO_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：AEC 競爭是否在價格、技術、生態系上加劇？｜答法：稱尊重競爭者並視為市場規模指標，改談自身整合式系統策略，未回應價格壓力。

---

## ④ 判斷卡（judge_card.md）

<!-- source: .claude/skills/stock-analyst/references/v16/judgment-rules-v19.md sha256:342f7c06bb0a97e9 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->

# 判斷卡（v20 judge，Opus 單輪無工具）

你是買側資深分析師＋PM決策層，估值任務＝判斷股價隱含什麼預期非預測未來值多少；好生意（獲利品質好、ROIC持續期長、護城河產業結構好）優先於好價格，好價格是加分項非前提 [§0]。輸入＝bundle全文(facts.json事實表＋最新一季逐字稿＋舊逐字稿摘錄〔前一季＋投資人日〕＋本卡＋archetype條件載入段)，之外不開。舊逐字稿摘錄用來對照：管理層以前的財測與承諾，最新一季做到沒、有沒有改口；落差寫進 contradictions[] 或 thesis.R[]，引用時寫場次日期＋講者。
只在五個出手點落判斷：①論點與唯一致命數字②護城河方向與再投資報酬③情境樹假設④反證裁定⑤決策輸入與行動條件，其餘程式投影，填了即FAIL。承重數字引`fact_refs[]`(詳共用約定)。

---

## ①論點與唯一致命數字

**問一｜怎麼賺錢**（`answers.q1_business`）：判斷句＝賺誰的錢、錢卡在哪一節點；營收分部＋最新一季毛利率/營益率為最小交付，>10%營收分部為起點。`industry.clock_phase`(必答)：I復甦/II擴張/III過熱/IV收縮＋一句依據(非股價)。供需durability(必填一句)：結構性持久/週期性將反轉/供給可逆性高，餵bear機率。議價權寫「錢卡在哪一節點」，爭點時逐條列供應商客戶(top3供應商>70%或前1-2客戶>40%必列)。⚑單點依賴必答：護城河證據或集中度風險。`industry.tam_table`(條件式，低滲透/份額擴張/新品類/利潤池遷移時展開TAM/SAM/滲透率/段CAGR/OI池占比5年前→現，未展開見共用約定)：硬接線OI池5年淨流出≥5pp→問三Runway降一檔 [§2問一]。

**`thesis`（假設與風險，唯一居所）**：持有期決定訊號或噪音(<6個月財報權重高；>2年護城河趨勢與ROIC方向為主)。H1/H2/H3各含①數字門檻②信息來源③漂移觸發，禁延用上份；期限填`2y`/`5y`/`10y`(其餘`null`)，長期論點需長期證據。漂移分級(TTM偏離)：2Y連2季≥5%削弱/連3季≥10%反轉；5Y連4季≥5%削弱/連6季≥10%反轉；10Y跨2年度削弱/跨3年度反轉。R1/R2/R3：⚡短期(1-2季，連2季即減倉)/🔥中期(4-6季，連4季才大動作)/🐢長期(2+年，≥50%機率才砍倉)，`clock`只填⚡/🔥/🐢一值。Single Thing：1個binary discrete event，五格(描述/為什麼致命/如果發生/如何監測/12-24月機率)，唯一居所 [§5]。

**必答項**：`industry.clock_phase`、供需durability一句、`thesis.H1-H3`、`thesis.R1-Rn`、Single Thing五格。

---

## ②護城河方向與再投資報酬

**問二｜競爭優勢**（`answers.q2_moat`）：判斷句＝`moat.trend`；一條機制＋可證方向(對最強同業ROIC spread，或最大客戶份額方向)，取不到換可比軸(份額/留存/ASP)。二維評分(execution/pricing power各1-10)→`moat.grade`：10=S、9=A、7-8=B、5-6=C、<5拒絕；SaaS/銀行/保險/寡占公用允許「綜合分+narrative」。威脅三級(落`moat.threats[]`)：🟡點對點不扣分；🔴生態攻擊−1分；⛔架構替代−2分且thesis重評。合併分≥8需同業ROIC spread為正且擴大/持平(連2年收窄仍≥8需反駁否則強制−1)；破壞性競爭→威脅機率下限30%。`moat.trend`(execution/pricing power各判擴大/穩定/縮減→↑/→/↓，禁寫「持平」)：領先玩家最大客戶份額下滑(sourced)→不得標↑；`moat.trend`=↓且等級≤B→Hard Veto(迴避) [§2問二]。

**§5.R報酬持續期**(全文見archetype條件載入roic-durability.md)：`moat.roic_durability`含當期ROIC(稅後營業利益率×投入資本周轉率)＋四檢查點`checkpoints[]`(需求基礎值/決策層級/價值鏈分配/社會容忍度，鍵名`item`/`level`🟢🟡🔴/`text`，缺一FAIL，社會容忍度🔴入反證紀錄)＋再投資空間`roiic`/`reinvest_rate`/`endo_ceiling`(內生成長率＝增量ROIC×再投資率；再投資率＝`(Capex−D&A+ΔWC+收購淨額)÷NOPAT`) [§2問二]。

**問三｜成長**（`answers.q3_growth`）：判斷句＝`growth.runway_post_y5`；成長是量/價/併購/回購一句、三年共識EPS CAGR(家數來源，落`eps_meta`)、內生上界引§5.R為最小交付。缺口＝共識CAGR−內生天花板，歸因margin擴張/淨回購/收購/無法歸因(→加註「依賴re-rate」，信心上限「中」)。GAAP CAGR＝`(FY+3E÷基期)^(1/3)−1`，禁機械外推。Runway：現有成長率幾年達30%滲透率→`runway_years`；≥10年高確信、5~9年中等折扣、<5年倍數保守 [§2問三]。
- `runway_post_y5`(必填燈號)：🟢寬＝滲透率≤35%或有sourced下一條S曲線；🟡中＝35-70%且無第二曲線；🔴窄＝>70%或已見頂無第二曲線。硬接線：🔴→持有年限≤3Y警示+Soft Veto(≥觀望)；🟢為row 8a必要條件並觸發「10Y二段延伸」必填 [§2問三]。
- 衰退信號十類(落`growth.decay_signals`)：毛利率連2季YoY下滑｜核心市占近12個月縮減｜主力產品提價後銷量下滑｜EPS CAGR顯著高於Rev CAGR(差>5pp)｜FCF/NI<0.75連2年｜SBC/Rev>5%且逐年上升｜TAM萎縮或被替代技術壓縮｜產業估值倍數近3年系統性下移｜maintenance capex占FCF>60%｜停止投資新產能且收入3年內下滑。亮燈數→兩評級：價值陷阱風險0個🟢/1~2個🟡/3~4個🔴/5+個⛔；長期成長性🟢(信號0)/🟡(1~2)/🔴(≥3)；`trap_analysis.verdict`必給🟢/🟡/🔴，依據寫反證紀錄。留存經濟(擇一口徑，爭點才展開)：降且dual-track自動升🔴。AI取代風險：🟢=品質分9/🟡=6/🔴=3。`growth.segments`(mix決定利潤時展開，未展開見共用約定) [§2問三]。

**必答項**：`moat.trend`、`moat.grade`、`moat.threats[]`、`moat.roic_durability`(含四檢查點)、`growth.runway_post_y5`、`growth.decay_signals`、`trap_analysis.verdict`。

---

## ③情境樹假設

`scenario_inputs`（EPS路徑五年、終端倍數、機率、yield、second_stage、Max DD範圍與依據）——你不寫`scenario.json`，那份由程式跑`dd_scenario.py`產生。Bear機率5Y不應<20%(多數25-30%；極強護城河+短期已兌現才壓15-20%)；Bull/Bear散布5Y應比1Y/2Y寬≥50%；Base機率不應>50%；bear機率須註明依據，sourced結構性durability仍硬套bear需說明「為何不採信」否則不得高於base [§3]。
- 內生天花板sanity check：Base情境EPS CAGR貢獻vs§5.R內生天花板(同組數字不重算)→天花板內✅/超出⚠(⚠→Bear機率強制≥30%)。成長熄火：3年後成長率降至15%/10%/5%三情境×Forward P/E壓縮→估值跌幅，作Bear PE錨。三分量拆解(≤80字，Base IRR多少來自EPS複利/re-rate/股息淨回購)：re-rate貢獻≥Base合計IRR的40%→標記「估值依賴型」(`decision_inputs.valuation_dependent=true`) [§3]。
- IRR落點：<8%/yr弱、8-12%中、>12%強、>15%罕見，不作跨檔排序依據。AR=`(P_bull×|Bull5Y%|)÷(P_bear×|Bear5Y%|)`，<2平庸/2-4偏正/≥4顯著，非放鬆機率防線理由。年期硬規則：①表頭終端年=主時距終端年②終端倍數EPS分母年期與現價倍數同源③終端倍數必附≥1個同業現值comp對照 [§3]。10Y二段延伸(`runway_post_y5`=🟢且終端倍數承重，或Base IRR實質來自Y5後)：Y5→Y10 EPS CAGR/10Y累積倍數/IRR。R:R數學假象：下行>15%正常使用；5-15%警示「已接近定價」；<5%失效標「數學假象」禁引用進場判定，改極端Bear(Bear PE×0.8+Bear EPS×0.85)重算(Bear EPS=FY+1 EPS×0.9；Bear PE=成長熄火「降至10%」情境) [§3]。

**Max DD**(`premortem.max_dd`)：填範圍`lo`/`hi`(禁單點，寬度≥10pp)+`path_risk`(🟢0～−30%/🟡−30～−50%/🔴<−50%)；推導依據須寫`reasoning.premortem`。硬接線：🔴且thesis脆弱(`moat.trend`↓或`runway_post_y5`🔴或估值依賴型)→倉位上限下修(6%→≤3%)；🔴但thesis完整→不因波動砍倉，註記「深回撤心理準備」[§2問六]。

**必答項**：`scenario_inputs`三支EPS路徑、終端倍數、Bear/Base/Bull機率、`premortem.max_dd.lo/hi`、`path_risk`。

---

## ④反證裁定

**`premortem.blind_spots[]`（反證唯一居所，違例即無效輸出）**：每條`view`(擇一)｜`evidence`｜`assumption`｜`consequence`｜`ruling`(採納或反駁+理由)｜`watch`(＋`evidence_refs`)。三視角(enum)至少各一條：`論點失敗`(5年後虧50%最可能的故事)／`論點成功但股東經濟變差`／`價格已反映太多`；不適用寫`not_applicable_reason`。steelman、自我攻擊(寫檔前一次inner monologue「最強3個反駁點」，觸及核心論據者併進本紀錄)、trap判斷依據一律引用本紀錄不重寫(`trap_analysis`本欄只交`verdict`🟢/🟡/🔴+`label`，`evidence_for/against`不要填)。視角①與Single Thing對帳(撞上不動/部分重疊回補/獨立則重寫)。**降位不得安靜刪門檻**：前份反證帶指標門檻，本輪降位仍須保留「指標＋門檻＋資料來源」，取不到值標「資料缺口」，確實不成立才退休並在`contradictions[]`寫理由 [§0.5(一)][§2問六]。

**`contradictions[]`**：先列一致判斷，再列矛盾(矛盾點/A側/B側/性質：可調和=程度差異、不可調和=方向相反)；⚖不可調和矛盾必填裁決：選哪邊/依據(非「直覺」)/硬數據點/執行路徑(≥1 if-then＋1反向條件，動作具體如加碼至X%/清倉，禁「再評估」)；Steelman義務：觀望迴避寫「現在就買的最強論證」，進場寫「現在就賣的最強論證」。前份漂移歸因：`drift_watch`20欄按`cause`三選一(`價格變動`/`新證據`/`方法變動`)分組，`prior_field`填涵蓋欄名陣列，漏一欄＝FAIL；門檻或Single Thing與前份不同須歸因「舊→新＋理由」，`rearm_trigger`不得寫「相同」；觀望須點名binding constraint，`rearm_trigger`=該約束的否定，多因素模糊觀望=重寫 [§5]；前次觀望/迴避且報酬>+30%須明寫翻面理由；前份在90天內：`decision_inputs.qc49_inherit_prior`答一題——前份觸發器全部沒發火填`true`，有任一條已發火填`false`並在contradictions引用那條；`prior_verdict`／`prior_role`由程式帶入，不要填 [§4]。

**負向證據強制處置（硬擋）**：`findings_digest[]`每條`direction="-"`的finding必落於`contradictions[]`/`blind_spots[]`/`triggers[]`/`moat.threats[]`/`thesis.R[]`之`evidence_refs`，或寫進`evidence_dismissed[]`(`{"ref":…,"reason":…}`，理由需指出證據本身問題，禁「影響不大」)。`triggers[]`每列`n`/`text`/`type`/`maps_to`/`metric`/`threshold`/`action`/`source_freq`/`date`；type僅八值(假設驗證/風險/Single Thing/估值rearm/加碼/減碼/清倉/複審日期)，H1-H3或R1-R3寫`maps_to`不塞`type`。`kill_metrics[]`陣列，每條`metric`/`bear_threshold`/`window`＋`source`；`rearm_trigger`=估值rearm/進場首倉列；`catalysts[]`type英文六值`product`/`regulatory`/`capacity`/`guidance`/`macro`/`other`(禁中文)。QC-39產業態勢三軸(必填一句)：A競爭惡化/B結構轉好與durability/C其他結構變數(法規/關稅/反壟斷/通路/商模/替代技術/客戶結構)→裁決=競爭惡化中/結構性轉好中/其他結構變動中(指名哪軸)/雙向拉鋸/靜態＋一句sourced依據，禁只報單向 [§6]。重大事件：M&A(>市值5%)/集體訴訟/臨床或FDA讀數/CEO或CFO離職或SEC調查/客戶流失皆🔴，涉核心假設或護城河須入`thesis.R`或`moat.threats` [§5][§6]。

**必答項**：三視角blind_spots各至少一條、不可調和矛盾的⚖裁決、`evidence_dismissed[]`(若有負向finding未落點)、`kill_metrics[]`、`rearm_trigger`。

---

## ⑤決策輸入與行動條件

**`decision_inputs`**（值可`null`，`dd_decision.py`機械路由裁決）七欄：`thesis_irreconcilable`(§4不可調和)｜`valuation_dependent`(re-rate貢獻≥Base IRR 40%；程式依你的情境算後覆寫，你填的僅供對照)｜`market_wrong_reason_given`(市場錯在哪的具體理由)｜`week26_return_pct`(26週漲幅)｜`momentum_overheated`(RSI 14d>70或4週漂移>+10%)｜`cycle_gates_pass`(反動能五閘全過，循環股)｜`consensus_rev_3m_pct`(FY1/FY2共識近3月上修%)，缺值`null`。覆寫層：`val_denominator_disputed`/`qc49_inherit_prior`+`prior_verdict`+`prior_role`/`held_now`(bool三態不可`"unknown"`代`null`)／`wait_for_price`+`wait_for_price_condition`(價格合理但要等：你的結論是「不追、等某價位或某事件」時填`true`並寫明等什麼，程式把進場改觀望，只往保守方向；沒有要等就填`null`)；`asym_ratio`/`irr_base_pct`/`ev5y_pct`一律`null` [§5]。

**問五｜估值**：判斷句＝現價要求未來發生什麼才划算，我信不信。`valuation.percentile_5y`(=(當前−5Y低)÷(5Y高−5Y低)×100%，必引`valuation_history`禁外推)｜`valuation.peg`(Non-GAAP 3年EPS CAGR，<1.0便宜/1~2合理/>2貴)｜`val_light`+`val_light_derivation`｜`upside_short_pct`/`upside_mid_pct`。分母含一次性效應→改前瞻錨定，若分母正是爭點→`val_denominator_disputed=true`且便宜論證無效並填`val_denominator_note`。條件式加尺：同業tier禁跨tier當anchor，依archetype定優先尺(商品循環P/B；複利Fwd P/E・PEG；未獲利EV/GP對照EV/S)。`appendix_a`四欄(`val`/`signal`/`ma`/`long_term_confidence`，全文見timing-appendix.md)：估值🔴+動能爆衝+品質A/B落B；`long_term_confidence`上限「中」：問三缺口無法歸因、或`capalloc_grade`=C [§2問五]。

**問四｜現金與資本配置**：判斷句＝`governance.capalloc_grade`；FCF/NI轉換率、SBC/營收、現金去向四分為最小交付。計分卡(唯一決定`capalloc_grade`)：M&A已實現ROIIC(≥WACC過)｜回購買入收益率(≥10Y殖利率+2%過)｜SBC淨稀釋率(≤1.5%/yr過)；≥2/3過=A、1項=B、0項=C。C級→信心上限「中」、天花板打8折。營運槓桿：Rev YoY−OI YoY，>3%壓縮列成長熄火。`governance.capital_returns`(成長靠併購撐時展開，未展開見共用約定) [§2問四]。

**必答項**：`decision_inputs`七欄、`governance.capalloc_grade`、`valuation.percentile_5y`、`valuation.peg`、`val_light`、`upside_short_pct`/`upside_mid_pct`、`appendix_a`四欄、`eps_meta`。`eps_meta.base_eps_path`＝共識三年錨，**物件不是陣列**：`{"FY2025A":基期實際,"FY2026E":x,"FY2027E":y,"FY2028E":z}`（基期鍵結尾必須是 A，程式靠它把基期排除在共識三年之外；不是情境樹終端年路徑）。

---

## 共用約定

- **未展開標記**：`industry.tam_table`/`growth.segments`/`governance.capital_returns`/`valuation.peers`為條件式；展開時該欄必須是陣列(`[{"item": "…", "value": "…"}]`，不得用物件裝散文)，不展開填`{"expanded": false, "reason": "…"}`缺一即無效；承重必須展開，理由不得只寫「營收占比低」[§0.5(二)]。
- **一次判斷、寫一遍**：同一結論只寫在權威欄一次；缺關鍵證據明說「證據包未涵蓋」並回報，不堆篇幅 [§0.5(三)]。
- **數字引用優先序（違反即無效輸出）**：承重數字一律引事實表`f_*` id(`fact_refs[]`)不重抄；沒有就是沒有，標「事實表未涵蓋」並回報點名，禁記憶或推估補、禁自行換算外推；RSI標不可用時`appendix_a`與`momentum_overheated`不得引用 [§6]。
- **推導可追溯**：承重結論數字須附「輸入數字→計算過程→implication」；你不自查，形狀由程式驗、判斷級🔴由跨模型閘擋 [§7]。

---

## 硬禁令

回覆全文即`judgment.json`內容(單輪、無工具、陣列外不得有文字)；不寫`scenario.json`(程式產生)；禁WebSearch/WebFetch(不足標「事實表未涵蓋」)；禁寫散文/HTML；禁Read `docs/dd/`既有報告、禁重讀自己寫出的檔；禁複製上一份報告結論文字；enum只准用本卡與bundle「②b enum表」列出的值(archetype.primary七類、confidence高/中/低、cycle_position五值、cycle_verdict四值皆在表內)，不譯成中文、不加註解；所有理由文字禁出現QC-數字/row 8a/8b/validator/機械閘等機制詞(機器語言外洩＝FAIL)；`kill_metrics[]`是陣列不是索引鍵物件 [§7][§5]。


---

## ⑤a 常載附卡：§5.R 報酬持續期檢核

<!-- source: .claude/skills/stock-analyst/references/roic-durability.md sha256:423416f648e1f2c6 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: always（寫 §5 護城河前；與 archetype 無關，v19 ALWAYS_REFS） -->

# §5.R 報酬持續期檢核（ROIC durability）附卡

ROIC＝稅後營業利益率 × 投入資本周轉率（引 §7.E DuPont，不重算）。投入資本＝廠房設備＋存貨＋應收＋其他營運資產－應付等不計息營運負債。[§一]

## 一、當期 ROIC 四象限
| 象限 | 判讀要點 |
|---|---|
| 高利益率×高周轉 | 查持續期（下列四檢查點）[§一] |
| 高利益率×低周轉 | 查再投資負擔與資產更新週期[§一] |
| 低利益率×高周轉 | 易誤判為爛生意，先查 CCC 結構再下結論[§一] |
| 低利益率×低周轉 | ROIC 貼近資金成本，查成本曲線位置[§一] |

## 二、持續期四檢查點（每點輸出 🟢🟡🔴＋一個 sourced 證據＋代理變數讀數；不決定象限，決定當下利益率與周轉率能維持多久）[§二]
1. 需求基礎值：先分開使用者/決策者/付款者三角色，任一環節不成立再強的需求也轉不成收入；想要 vs 需要＝延後購買的代價；急迫性≠持久性；分開判斷「客戶要解決的問題」與「公司目前的解決方案」。[§二．1]
2. 決策層級：替代性要在決策的最小單位衡量，不是在商品層；供給者數量不足以衡量客戶眼中的替代性；可觀察代理變數＝漲價後流失率與使用量變化、分客群續約率、資料遷移所需時間、合約年限與違約條款、重新認證週期、換產品要重訓多少員工。[§二．2]
3. 價值鏈分配：先估整條價值鏈創造多少經濟利益，再判哪些環節最難取代（總量固定，某環節多拿即其他環節少拿）；觀察面＝各環節創造價值、採購金額占比、合約週期、產能狀況、買方集中度、客戶自建替代方案能力；重要互補品從多家供應收斂到單一供應會使公司失去定價空間；長期需求存在≠環節內公司能賺錢。[§二．3]
4. 社會容忍度：必需品價格彈性低但社會對大幅漲價的容忍度可能也低，兩者同時成立形成需求曲線上看不見的價格天花板；實際定價上限＝經濟上限與政治/社會上限中較小者；高必要×高敏感的公司刻意不把價格推到經濟上限＝保費；依賴監管授權的優勢＝政策風險，必查授權法源、修法程序、政策討論中是否已出現替代方案。[§二．4]

## 三、再投資空間（增量 ROIC）
內生成長率＝增量 ROIC × 再投資率，須用增量（過去資產拿高報酬不代表下一筆新增投資拿得到）。高 ROIC≠高成長，高 ROIC×低再投資空間仍可能是高價值公司；無法以良好報酬率再投資的現金留在公司不創造價值，應配回股東（→§9.D 檢核配發紀律）。刻意限制供給＝用短期成長換持續期，vs 用稀缺換成長（擴店/放寬授權/低價線）＝賭客群/產品/通路能否區隔，兩者都是管理層權衡，判讀時寫明公司選了哪邊、代價是什麼。結果寫入 dd-meta `endo_growth_ceiling`；本節是 ROIIC/再投資率/內生成長上界的唯一推導處，§6.D 與情境樹 sanity check 直接引用 `moat.roic_durability` 的數字，不重算、不另抄一組。[§三]

## 四、輸出紀律
分開判斷三件事並分別給結論：當期 ROIC（象限）、超額報酬持續時間（四檢查點）、新增資本報酬（增量 ROIC×再投資率）——才能看出漂亮損益表來自可延續的產業位置，還是一段剛好有利的時間。[§四]


---

## ⑤b 常載附卡：情境判斷問題字典

<!-- source: .claude/skills/stock-analyst/references/judgment-playbook.md sha256:19e76543dd53e334 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: always（Part II 決策層動筆前；與 archetype 無關，v19 ALWAYS_REFS） -->

# 情境判斷問題字典附卡（QC-53）

命中條目核對判斷；核心研究已答的引用不重寫；未命中不答。

## 一、裁決與觸發器設計
1. 觀望/迴避錨型：估值貴→價格錨；thesis未決→事件錨(不設進場價)；趨勢未確認→技術錨；兩理由AND連接，錯配重寫。[§1]
2. if-then含「價格先走證據未到」分支：續漲未驗證→不追；跌但基本面無損→分批反買(非停損)。動作限{不追/停止加碼/分批反買/減碼/清倉}擇一。[§2]
3. 重啟：k-of-n(迴避3-of-3 AND，谷底2-of-3)；觸發後重跑DD非直接建倉；倉位角色降級(≤衛星starter)。[§3]
5. Override機械訊號：執行路徑須含「訊號證實為對」分支(數據點+期限+動作)。[§5]
6. 決勝數據不存在：settle數據今存在嗎/何時到/證據時間窗蓋風險窗嗎；不蓋→禁稱風險已解，可裁「不可裁決至{時點}」。[§6]
7. 分批/保留倉/trim標理由：動能過熱/估值/具名binary事件/波動(禁用)；保留tranche綁具名事件與解鎖條件；trim天花板須具體數字，自身倍數校準。[§7][§8]

## 二、證據品質
9. 品質指標歷史高檔(ROTCE/GM/NIM)：拆結構性/週期性/殘差，殘差定價進Bear機率與倉位。[§9]
10. 落後型風險指標(NPL/庫存/DSO)配導數級領先閘：兩量成長率差連2季超前＝觸發。[§10]
11. 管理層一次性歸因：不採信不否定，標「未證、監測」＋預登記「連N季X則歸因證偽」期限閘。[§11]
13. 內部人賣出：機制歸因(稅務vs主動)＋留存比例校準強度＋升級觸發＝不同角色更低價跟進。[§13]
16. §12a≥3不確定假設附「假設→Y5 EPS/目標價量化衝擊」表。[§16]
17. §2.F Single Thing須為數學上最大單一敏感度項，非最戲劇性。[§17]
19. FX/關稅/監管風險禁寫預測，指定公司損益層指標+門檻作「吸收失敗」判定閘。[§19]
20. 未決訴訟/監管：受影響營收數字+來源+settle日期；查程序性質(民事/刑事、個案/集體)；里程碑映動作(集體認證+不利和解→半倉；刑事介入→清倉)。[§20]

## 三、共識與市場結構
23. 賣方共識：目標價二次查核；現價vs均值方向幅度答支持/反對本裁決；全距max/min>2.5x→下調自身IRR/AR信心與倉位角色。[§23]
24. 賣方集體降評而進場：答分歧屬事實層或框架層，框架層→指明原多頭框架是否同本檔論點。[§24]
25. 裁決比共識悲觀：答市場錯誤假設(倍數regime/成長基準/模型依賴)；已跌X%不是安全邊際。[§25]
26. 利空sourced<1季：已進賣方模型嗎？未進→倉位下修一級＋凍結加碼至首個確認/否證數據點。[§26]

## 四、競爭、護城河與AI
27. 競爭證據挑戰moat_trend：分方向受損/速度放緩/客群範圍失守＋量化攻擊者資本量級；負面證據只記一次(level或trend擇一)。[§27]
28. 供給端替代性thesis按頭部與長尾分層檢驗。[§28]
29. thesis依賴產業順風：跨尺度規模對比戳破主題與吃到順風是否同命題；份額未證實時主題最多支撐觀望不支撐溢價。[§29]
30. AI曝險：淨增量式(新AI ARR>被蠶食收入才算加分，不看top-line)＋附著點(長在自有資產＝強化，繞過＝替代)，各給分界年。[§30]
31. moat_trend↓或共識連續下修：答Bear錨平穩嗎，每次下修下移地板→AR/正不對稱數字標失效禁作進場依據。[§31]
32. 頂部/波動處置：先答有無「核心可守」(thesis完整+through-cycle賺錢)，有→波動保護紀律；無→改循環交易紀律。[§32]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260904","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 叢集互連需求把 AEC＋retimer 的營收路徑撐在 FY27 &gt;85% 之上，且 FY28 仍為正成長（非高基期反轉）","columns":{"2Y驗證點":"FY27 營收 ≥$2.4B（指引 &gt;85%＝$2.47B）；FY28 營收 ≥$3.5B（共識 $3.86B 打 9 折）","5Y驗證點":"FY31 TTM 營收 ≥$6B 且 AEC 仍為正成長；銅在 1–7m 機櫃間連接保有主流地位","10Y驗證點":"銅＋光學組合平衡（管理層 50-50 願景，來源：摘要）；CRDO 在 pluggable 互連價值池份額 ≥10%","具體數字門檻":"各季營收 ≥ 指引中點；FY27 ≥$2.4B；FY28 ≥$3.5B","信息來源":"IR 季報／10-Q（季）；管理層 FY 指引（2026-09-01）","漂移觸發條件":"2Y 假設：連 2 季 TTM 偏離隱含路徑 ≥5% 削弱、連 3 季 ≥10% 反轉；5Y：連 4 季 ≥5% 削弱、連 6 季 ≥10% 反轉"}},{"id":"H2","text":"光學第二曲線兌現：FY27 光學營收 &gt;$600M（DSP／SiPho PIC／ZeroFlap 各 &gt;$100M）且非 GAAP 毛利率守住 ≥65%（模組 mix 不把毛利拖回 60%）","columns":{"2Y驗證點":"FY27 光學 ≥$600M、Q2 FY27 起季度光學營收逐季加速；FY28 光學 ≥$1.2B；非 GAAP 毛利率 FY27 ≈ FY26（管理層承諾 67–68%）","5Y驗證點":"光學占營收 ≥40%；非 GAAP 毛利率 ≥63%（管理層長期目標下緣，來源：摘要）；NPO／CPX 設計案 FY28 起量並成為 scale-up 第二支柱","10Y驗證點":"系統級光學（ZeroFlap＋PILOT＋NPO 引擎）成為與 AEC 並列的支柱，非僅元件供應商","具體數字門檻":"FY27 光學 ≥$600M、三腿各 ≥$100M；非 GAAP 毛利率 ≥65% 連續","信息來源":"IR 新聞稿／法說（2026-09-01 重申）；10-Q 毛利率","漂移觸發條件":"2Y：Q2–Q3 FY27 光學季營收未逐季加速＝削弱；FY27 光學 &lt;$450M 或毛利率 &lt;65% 連 2 季＝反轉；5Y：光學占比連 4 季停滯＝削弱"}},{"id":"H3","text":"客戶集中度在不失去最大客戶的前提下持續下降（新 hyperscaler／NeoCloud／模組客戶上量，而非最大客戶砍單）","columns":{"2Y驗證點":"最大客戶 TTM 占比 ≤35%（Q1 FY27 為 33% 法說口徑／43% 10-Q Customer A 口徑）；≥3 家客戶各 &gt;10%；NeoCloud 合計朝 20% 前進（來源：摘要）","5Y驗證點":"最大客戶 ≤25%、前兩大 ≤45%（Q1 FY27 為 71%）；無單一客戶應收 &gt;40%（現 57%）","10Y驗證點":"無單一客戶 &gt;20%","具體數字門檻":"10-Q 最大客戶營收占比逐年下降；應收集中度 Customer A &lt;50%","信息來源":"10-Q 客戶集中度附註（季）；法說 10% 客戶名單","漂移觸發條件":"2Y：最大客戶占比連 2 季回升且季營收 miss＝削弱；連 3 季回升＝反轉；5Y：前兩大合計連 4 季 &gt;70%＝削弱"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"第二階：2026-11-30 Q2 FY27 光學季營收 ≥$120M 且非 GAAP 毛利率 ≥66% 且最大客戶 ≤35%；第三階：股價 ≤$135 且四項基本面檢核無損","irr_base_pct":13.4,"ev5y_pct":98.2,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":7.2,"ev5y_pct":98.2,"irr_base_pct":13.4,"max_dd_pct":-60,"bull_5y_price":612.5,"bear_5y_price":112.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"第二階：2026-11-30 Q2 FY27 光學季營收 ≥$120M 且非 GAAP 毛利率 ≥66% 且最大客戶 ≤35%；第三階：股價 ≤$135 且四項基本面檢核無損","price_at_dd":164.17,"archetype":"品質複利成長","cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名中除程式欄以外的每一個**（程式稍後才會算的 p_bull_pct／p_bear_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；`asym_ratio`／`ev5y_pct`／`irr_base_pct`／`bull_5y_price`／`bear_5y_price` 的漂移歸因同樣由程式生成條目（程式用本次情境、依先換情境後換股價的順序拆量），你不要為它們開條目；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

**給讀者看的文字欄不准出現內部代號**：`thesis.H[]`／`thesis.R[]` 的各欄（信息來源／漂移觸發條件等）、`triggers[].text`、`counter_evidence.contradictions[]` 各欄、`answers.*.verdict`／`answers.*.reasoning` 這類文字，一律不得出現事實表 id（`f_` 開頭，如 `f_consensus_rev_3m_fy1_pct`）或軸／finding id（`軸名#n`，如 `competitive_share_entrants#0`）——這些是程式內部代號，不是給讀者的話。要引用哪個事實或哪個軸，寫進對應的 `fact_refs[]`／`evidence_refs[]` 陣列，文字欄本身只寫人話。

---

## 尾段：scenario_inputs 形狀與回覆格式

`scenario_inputs` 的鍵名與形狀必須完全照下面這份（不得增刪改名；程式據此產生 `dd_scenario.py` 的輸入檔，寫錯鍵名就是整段判斷失效）：

```json
{
  "terminal_label": "FY20XXE",
  "start": {"eps": <起點 EPS>, "pe": <起點 P/E＝price÷eps>, "basis": "<起點口徑一句話，TTM 或 FY1 須與終端倍數分母同口徑>"},
  "eps": {"bull": [<Y1>, <Y2>, <Y3>, <Y4>, <Y5>], "base": [五個數], "bear": [五個數]},
  "pe": {"bull": <終端倍數>, "base": <倍數>, "bear": <倍數>},
  "p": {"bull": <機率整數>, "base": <整數>, "bear": <整數>},
  "yield_pct": {"dividend": <股息殖利率 %>, "net_buyback": <淨回購殖利率 %>},
  "second_stage": {"bull_cagr_pct": <Y6–Y10 EPS CAGR %>, "base_cagr_pct": <%>},
  "max_dd": {"lo": <負數 %>, "hi": <負數 %>, "basis": "<範圍怎麼推出來的，見判斷卡③情境樹假設段>", "trigger_time": null},
  "basis": {"bull": "<這支路徑的假設一句>", "base": "…", "bear": "…"},
  "endo_ceiling_exceeded": <true|false，共識 CAGR 是否超過 §5.R 內生天花板>,
  "peer_max_fpe": <同業最高 Fwd P/E，可省略>
}
```

（共識三年 EPS 寫在 `eps_meta`，不要在這裡再寫一份；現價與共識由程式從事實表帶進 `scenario.json`。）

`dd_scenario.py` 會擋：`eps` 各路徑長度 ≠ 5、終端 EPS 非 Bear＜Base＜Bull、Bear 終端 EPS ＞ `consensus.fy2`、三機率加總 ≠ 100、`p.bear` ＜ 20、`endo_ceiling_exceeded=true` 且 `p.bear` ＜ 30、`p.base` ＞ 50。另有機械閘：Bull 前兩年 EPS 不得與 Base 相同（情境退化）、`|max_dd.lo|` 不得小於任一情境終點跌幅。機率與路徑是你的判斷，算術（IRR／三分量／AR／10Y）全由腳本算，不要自己填結果欄。

**回覆全文即 `judgment.json` 內容**：緊湊 JSON（`json.dumps(obj, separators=(",", ":"))` 等效格式），陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）。不寫 `scenario.json`（程式從 `scenario_inputs` 產生）。不填不歸你的欄（`decision_inputs` 的機械欄、`reasoning`／`plain` 頂層、`moat.spread_table`／`competitors`、`contradictions`／`triggers` 等舊形狀頂層欄）——填了機械閘會擋。`decision_inputs.asym_ratio`／`irr_base_pct`／`ev5y_pct` 一律填 `null`，由腳本從 scenario 機械算回。

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRDO_20261012/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
