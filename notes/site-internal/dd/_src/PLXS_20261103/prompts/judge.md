你是 stock-analyst **v20 判斷 agent**，標的 PLXS（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
  valuation_basis: str|null enum[eps_pe｜sales_multiple｜None]
  rev
    bull[]: arr ≥1 num
    base[]: arr ≥1 num
    bear[]: arr ≥1 num
  ev_s
    bull: num|null
    base: num|null
    bear: num|null
  net_debt_y5
    bull: num|null
    base: num|null
    bear: num|null
  shares_y5
    bull: num|null
    base: num|null
    bear: num|null
  eps
    *bull[]: arr ≥1 num
    *base[]: arr ≥1 num
    *bear[]: arr ≥1 num
  pe
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
- `scenario_inputs.valuation_basis`：eps_pe｜sales_multiple
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
{"meta":{"ticker":"PLXS","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":1426.6,"period":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","unit":"USD M；YoY +34.8%（Q4 FY25 1,058.4）、QoQ +9.3%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","citation":"公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm"},"note":"查無共識數字"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":95.8,"period":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","unit":"USD M；margin 6.7%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","citation":"公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm"},"note":"查無共識數字"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":86.3,"period":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","unit":"USD M；margin 6.0%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","citation":"公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm"},"note":"查無共識數字"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":6.4,"period":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","unit":"USD M（OCF 29.2 − capex 22.8）；FY26 全年 −28.9","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","citation":"公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm"},"note":"查無共識數字"},{"id":"f_kpi5_guidance_q1_fy2027_2027_","label":"Guidance Q1 FY2027（季末 2027-01-02）","value":"營收 1,410–1,460","period":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","unit":"USD M；GAAP op margin 5.5–5.9%、non-GAAP 6.0–6.4%；GAAP EPS 2.16–2.32、non-GAAP EPS 2.46–2.62；FY27 營收成長中高個位至高十位數（mid-to-upper teens）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","citation":"公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm"},"note":"查無共識數字"},{"id":"f_kpi6_inventory_days","label":"Inventory days","value":119,"period":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","unit":"天；cash cycle 62 天","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","citation":"公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm"},"note":"查無共識數字"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_plxs_gross_margin_pct","label":"PLXS 毛利率","value":10.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLXS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_plxs_operating_margin_pct","label":"PLXS 營業利益率","value":5.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLXS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_plxs_fcf_margin_pct","label":"PLXS FCF 利潤率","value":-1.0,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLXS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sanm_gross_margin_pct","label":"SANM 毛利率","value":9.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_operating_margin_pct","label":"SANM 營業利益率","value":5.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_fcf_margin_pct","label":"SANM FCF 利潤率","value":4.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bhe_gross_margin_pct","label":"BHE 毛利率","value":10.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BHE.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bhe_operating_margin_pct","label":"BHE 營業利益率","value":4.25,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BHE.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bhe_fcf_margin_pct","label":"BHE FCF 利潤率","value":4.61,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BHE.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_flex_gross_margin_pct","label":"FLEX 毛利率","value":9.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_flex_operating_margin_pct","label":"FLEX 營業利益率","value":5.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_flex_fcf_margin_pct","label":"FLEX FCF 利潤率","value":3.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jbl_gross_margin_pct","label":"JBL 毛利率","value":9.23,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_jbl_operating_margin_pct","label":"JBL 營業利益率","value":5.11,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_jbl_fcf_margin_pct","label":"JBL FCF 利潤率","value":3.82,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_gaap","label":"SBC（占 GAAP 營業利益／占營收）","value":9.6,"period":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","unit":"USD M；占 GAAP 營業利益 11.1%、占營收 0.67%（含 1.1 高階主管退休加速認列）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）","citation":"公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm"},"note":"查無共識數字"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":214.32,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-18.37,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":37.11,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":2.08,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.12 → 10.33）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":3.42,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.4 → 11.79）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":10.33,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":11.79,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":25.52,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 8.23 → 10.33（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":28.92,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝66.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":66.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.15,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.15,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":20.75,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 10.33，分子＝快照價 214.32","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":10.81,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 291.99、現金 281.18（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":26.65,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":5723.02,"period":"2026-11-03","unit":"USD m","basis":"市值 5712.21 ＋ 淨負債 10.81","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5872.32,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（5 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6423.12,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（5 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.97,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 211.96 / W52 223.15 / W104 181.11 / W250 133.19 / W250 13週斜率 1.54%"},{"id":"f_ma_w52","label":"52 週均線","value":223.15,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":181.11,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":133.19,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.54,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"公司在 FY2026 Q3 財報稿稱，因新專案導入與市占率提升，上調 FY2026 營收成長預期至逾 20%（公司自述，非第三方份額數據）。","source":"Barchart／Plexus 新聞稿 Plexus Announces Fiscal Third Quarter Financial Results","url":"https://www.barchart.com/story/news/3534466/plexus-announces-fiscal-third-quarter-financial-results","excerpt":"For fiscal 2026, we now anticipate generating in excess of 20% revenue growth due to Plexus' success in launching numerous new programs and our market share gains combined with improved end market demand.","as_of":"2026-07-29","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：製造流程缺乏重大專利保護，資源更大的公司可能進入市場；客戶亦可能自製；競爭加劇可能導致降價或失去客戶／份額。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"Our manufacturing processes are generally not subject to significant proprietary protection, and companies with greater resources or a greater market presence may enter our market or otherwise become increasingly competitive. Increased competition could result in significant price reductions, reduced sales and margins, or loss of customers or market share.","as_of":"2025-11-14","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K Item 1：競爭者可能提供類似服務、部分在特定產業更成熟或資源更大；Plexus 亦與客戶自有產能競爭。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"A number of competitors may provide services similar to Plexus. Others may be more established in certain industry sectors, or have greater financial, manufacturing or marketing resources.","as_of":"2025-11-14","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K FY2025 揭露 Plexus 亦與現有及潛在客戶的 in-house 能力競爭（一般性競爭風險，未指名特定客戶自製）","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"Plexus also competes with in-house capabilities of current and potential customers.","as_of":"2025-11-14","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Q2 FY2026 前十大客戶占營收54%（FY2025為49%），客戶集中度上升","source":"SEC 8-K Q2 FY2026 earnings exhibit","url":"https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000028/plxsf26q2er-ex991.htm","excerpt":"Top 10 customers comprised 54% of revenue during the second quarter of fiscal 2026.","as_of":"2026-04-29","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：無單一客戶占營收逾10%（FY2025、FY2024皆然）；前10大客戶占營收49.1%（FY2024為47.8%）。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"As a percentage of consolidated net sales, no customer accounted for over 10.0% or more of consolidated net sales in fiscal 2025 or 2024. Our 10 largest customers accounted for 49.1% and 47.8% of our net sales in fiscal 2025 and 2024, respectively.","as_of":"2025-11-14","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：FY2023 GE Healthcare 占營收10.3%，FY2024、FY2025無客戶達10%。","source":"SEC EDGAR 10-K FY2025 Item 8 Note","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"As a percentage of consolidated net sales, there were no customers representing 10.0% or more of consolidated net sales for fiscal 2025 or 2024. As a percentage of consolidated net sales, GE Healthcare Technologies, Inc. (\"GEHC\") represented 10.3% of consolidated net sales for fiscal 2023.","as_of":"2025-11-14","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 Q2財報稿稱前10大客戶占該季營收54%（搜尋摘要轉述）。","source":"Plexus 8-K Q2 FY2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000028/plxsf26q2er-ex991.htm","excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 Q4財報稿：FY2026前10大客戶占營收54%，較FY2025上升。","source":"Plexus 8-K Q4 FY2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm","excerpt":"Top 10 customers comprised 56% of revenue during the fourth quarter of fiscal 2026. This is up 1 percentage point from the third quarter of fiscal 2026 and up 7 percentage points from the fourth quarter of fiscal 2025. For fiscal 2026, top 10 customers comprised 54% of revenue, up 5 percentage points from fiscal 2025.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Plexus Q3 FY26 call (2026-07-30): management said FY2027 growth could exceed long-term 9–12% goal on demand visibility; healthcare/life sciences expected to moderate to at least mid-single digits in FY27 after high-teens FY26 (digestion); A&D preliminary at least mid-single digit. (搜尋摘要轉述，未取得逐字原文)","source":"MarketBeat, Plexus Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/plexus-q3-earnings-call-highlights-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Per Earnings Whispers on FQ4 report (single secondary source): FY27 growth raised to mid-to-upper teens, A&D and Industrial each expected >20% growth, new 6.5–7.0% operating margin goal. Unverified against company release.","source":"Earnings Whispers PLXS","url":"https://www.earningswhispers.com/article/PLXS/20977","excerpt":null,"as_of":"2026-11-01","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"EMS industry demand strong; capacity and lead time, not demand, are primary constraint (Global Electronics Association, June 2026 N.A. EMS results, book-to-bill 1.33, shipments +6.7%).","source":"Global Electronics Association news release","url":"https://www.electronics.org/news-release/north-american-ems-shipments-rise-67-june-book-bill-reaches-133","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"European EMS: defence expected to remain strongest structural growth driver; consolidation accelerating.","source":"Evertiq, 2026-03-17","url":"https://evertiq.com/news/2026-03-17-european-ems-consolidation-accelerates-as-defence-demand-reshapes-the-market","excerpt":null,"as_of":"2026-03-17","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lincoln International Q2 2026 EMS review: A&D, data center/AI, critical power remained areas of strength; margins vary more with mix, execution, utilization than size.","source":"Lincoln International EMS Quarterly Review Q2 2026","url":"https://www.lincolninternational.com/publications/ems-quarterly-review-q2-2026/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 揭露：墨西哥廠在 IMMEX 保稅計畫下營運（降低關稅），計畫變動或不合規會造成不利影響；關稅、出口管制與貿易保護措施可能影響成本、零組件供應與需求。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"Our current facilities in Mexico operate under the Mexican Maquiladora (“IMMEX”) program. This program provides for reduced tariffs and eased import regulations. We could be adversely affected by changes in the IMMEX program or our failure to comply with its requirements.","as_of":"2025-11-14","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 揭露：出口規範與制裁可能限制在中國使用或生產特定技術／產品，或銷售最終運往中國的零組件；貿易法規涉及先進半導體，可能限制對中國客戶出貨、支援中國營運專案與採購零組件。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"Changing export regulations, increasing sanctions or other trade barriers may limit our ability to use or produce certain technologies or products in China or sell certain components or products that are ultimately destined to China.","as_of":"2025-11-14","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 揭露：客戶合約多允許季度性價格調整，但公司過去及未來可能承擔調價之間的零組件漲價風險，回收調價對營業利益率有稀釋效果。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"While many of our customers permit quarterly or other periodic adjustments to pricing based on changes in component prices and other factors, we have in the past and may continue to bear the risk of price increases that occur between any such repricing or, if such repricing is not permitted, during the balance of the term of the particular customer contract.","as_of":"2025-11-14","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K：美國以外營運占淨銷售與營業利益多數，且特別集中在馬來西亞；墨西哥廠在 IMMEX 計畫下營運，貿易政策／關稅變動為風險。","source":"Plexus Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"Operations outside of the U.S. in the aggregate represent a majority of our net sales and operating income, with a particular concentration in Malaysia.","as_of":"2025-11-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 提及中美關稅與出口管制可能影響中國採購零組件的成本與可得性。","source":"Plexus Form 10-K FY2022","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578622000085/plxs-20221001.htm","excerpt":"These actions could also affect the cost and/or availability of components that we procure from suppliers in China, as well as create disruptions, delays, shortages or increased costs within our global supply chain.","as_of":"2022-11-15","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 分段營收：A&D $847M(17%)、Healthcare/Life Sciences $1,933M(39%)、Industrial $2,185M(44%)，總 $4,965M，前一年 $4,033M；Q4 Industrial $691M(48%) 對 Q3 $589M、去年同期 $461M。","source":"Plexus 8-K FY2026 Q4 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm","excerpt":"Industrial 2,185 44 % 1,715 43 %","as_of":"2026-10-28","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q4 FY2026 A&D $224M 較 Q3 $233M 下滑；Healthcare $512M 對 Q3 $483M。","source":"Plexus 8-K FY2026 Q4 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm","excerpt":"Aerospace/Defense $ 224 16 % $ 233 18 % $ 173 16 %","as_of":"2026-10-28","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"公司指引 FY2027 營收中到高十位數成長；Q1 FY2027 營收 $1.410–1.460B。","source":"Plexus 8-K FY2026 Q4 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm","excerpt":"We now expect mid- to upper-teens revenue growth with increasing operating margin and sustained working capital efficiency.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"FY2027 初步展望：A&D 至少中個位數成長、Healthcare/Life Sciences 放緩至至少中個位數(消化期)，Industrial 受半導體設備需求帶動；top-10 客戶占 56%。","source":"MarketBeat Plexus Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/plexus-q3-earnings-call-highlights-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 風險因素僅提到客戶終端市場的新進入者可能影響業務，未點名任何取代 Plexus EMS 服務的替代技術。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"Any weakness in our customers’ end markets, or new entrants in those markets that compete with our customers, could affect our business and results of operations.","as_of":"2025-11-14","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 描述 Plexus 依三大市場板塊（航太國防、醫療生技、工業）做業務開發，除特定 go-to-market 團隊外不為特定板塊專設資源；原料向製造商及授權經銷商採購，屬 B2B 合約製造模式，一手文件未顯示通路或商業模式轉移。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm","excerpt":"Although our current business development focus is based on our targeted market sectors of Aerospace/Defense, Healthcare/Life Sciences, and Industrial, we evaluate our financial performance and allocate our resources geographically","as_of":"2025-11-14","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ3 2026 (2026-07-29)營收 $1.305B，高於原指引 $1.200–1.250B；FQ4 營收指引 $1.330–1.380B。","source":"Plexus IR press release: Plexus Announces Fiscal Third Quarter Financial Results","url":"https://investor.plexus.com/news/news-details/2026/Plexus-Announces-Fiscal-Third-Quarter-Financial-Results/default.aspx","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ4 非GAAP EPS 指引 $2.47–2.63，Benzinga 列示當時共識 $2.09（指引高於共識）；Benzinga 另列 FQ3 實績對照預估 $1.96，各站預估數字不一致。","source":"Benzinga earnings-forecasts (kr)","url":"https://kr.benzinga.com/quote/PLXS/earnings-forecasts","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"LSEG 對 FQ4 EPS 平均預估 $2.56，位於指引區間 $2.47–2.63 中段附近。","source":"Capital.com: Plexus Corp expected to post earnings of $2.56 a share","url":"https://capital.com/en-au/news/plexus-corp-plxs-oq-expected-to-post-earnings-of-2-56-a","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill：FY2026 EPS 共識 8.87（9 位分析師，截至 2026-10-18）；FQ4 EPS 共識 $2.61、營收 $1.386B，略高於指引上緣；預計 10-28 公布（結果未確認）。","source":"Chartmill PLXS estimates","url":"https://www.chartmill.com/stock/quote/PLXS/estimates","excerpt":null,"as_of":"2026-10-18","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價分布（2026-08 前後）：Benzinga 平均 $254（7 位，高 $330/低 $150，截至 8/7）；Tickflow 共識 $277.50（6 位）；MarketBeat $246.67 Moderate Buy；Investing.com 7月底平均約 $305.75（4 Buy 1 Hold）；Sidoti 7/31 升評 Buy 目標 $308。來源間差異大，均非 11 月最新。","source":"Benzinga / Tickflow / MarketBeat / Investing.com 彙整（搜尋摘要）","url":"https://www.benzinga.com/quote/PLXS/analyst-ratings","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 統計 2022-10 至 2026-07 共 18 次指引更新，8 次上調、5 次下調。","source":"Benzinga earnings-forecasts","url":"https://www.benzinga.com/quote/PLXS/earnings-forecasts","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月7份8-K中僅2份含重大項目：2026-06-08 新信貸協議（Item 1.01，循環額度5億美元，到期2031-06-05）與2026-08-24 新增1億美元庫藏股授權（Item 8.01）；無併購（2.01）、重編（4.02）等項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000785786&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-05 簽署第二次修訂重述信貸協議，取代2022年協議，到期日2031-06-05，循環額度5億美元（可增至7.5億）。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/785786/000078578626000038/plxs-20260605.htm","excerpt":"The Second Amended and Restated Credit Agreement has a maturity date of June 5, 2031. The Second Amended and Restated Credit Agreement is comprised of a revolving credit facility under which the maximum commitment is $500 million","as_of":"2026-06-08","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"ems_utilization_capex_cycle#0","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"+","claim":"管理層稱現有廠區可支撐約 $6B 營收，各區域有閒置產能（未披露稼動率%；來源為第三方 AI 摘要，FQ1 2026 法說）","source":"Fintool PLXS Q1 2026 earnings summary","url":"https://fintool.com/app/research/companies/PLXS/earnings/Q1 2026","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ems_utilization_capex_cycle#1","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"FY26 capex 指引上修至 $100–120M（約營收 2.5%），後續由新增廠區轉向自動化投資；Q2 重申","source":"VectorShift Plexus 2026 Q1/Q2 summary","url":"https://vectorshift.ai/research/companies/plexus/earnings/2026-q2-summary","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ems_utilization_capex_cycle#2","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"-","claim":"Penang 馬來西亞第六廠：Q2 FY26 略低於損益兩平，預期財年末轉盈；Q3 摘要稱新增逾 $500M 產能（新產能稀釋 ROIC 風險點）","source":"MarketBeat Plexus Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/plexus-q3-earnings-call-highlights-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"ems_utilization_capex_cycle#3","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"+","claim":"FQ3 2026 營收 $1.305B，FQ4 指引 $1.330–1.380B（現有產能利用提升中）","source":"Plexus IR FQ3 results release","url":"https://investor.plexus.com/news/news-details/2026/Plexus-Announces-Fiscal-Third-Quarter-Financial-Results/default.aspx","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#0","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"OpenCapital 列 ROIC：Plexus Q1 2026 為 18.7%（去年同期 14.9%）；同業 Celestica 39.5%、Jabil 29.8%、Flex 19.2%、Sanmina 11.3%。聚合站口徑，非公司自報。","source":"OpenCapital PLXS ROIC metrics page","url":"https://www.opencapital.sh/stocks/plxs/metrics/roic","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#1","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"OpenCapital 列資產週轉：Plexus 1.3x、Jabil 1.6x、Sanmina 1.5x、Flex 1.4x（Celestica 缺）；Value Research 另列 Plexus 資產週轉 0.90（銷售/平均總資產），稱高於同業中位數，兩者口徑不同不可直接比。","source":"OpenCapital PLXS asset turnover page; Value Research PLXS key ratios","url":"https://www.opencapital.sh/stocks/plxs/metrics/asset_turnover","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#2","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"+","claim":"Plexus 自報 FY2026 ROIC 15.8%，高於 9.0% WACC 680bps；現金循環天數 62 天；FY2027 目標低至中 60 天、FCF 至少 1 億美元。季度 ROIC：Q1 13.2%、Q2 13.8%、Q3 14.9%；現金循環 69→64→62 天。","source":"Plexus Form 8-K FY2026 Q4 earnings release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["moat_trend","valuation","triggers"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#3","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"Lincoln International 2026 Q2 EMS 季報列營業利益率：Celestica 8.9%、Jabil 5.1%、Sanmina 5.5%、Flex 5.4%、Benchmark 3.7%、Plexus 5.2%（非 ROIC，僅供結構參考）。","source":"Lincoln International 2026 Q2 EMS Quarterly Review","url":"https://www.lincolninternational.com/publications/ems-quarterly-review-q2-2026/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單中無併購相關項目（2.01）；僅信貸協議與庫藏股。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000785786&type=8-K","excerpt":"2026-06-08 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"-","claim":"2025-01-22 有FDA 483檢查紀錄（第三方彙整站），涉及心臟監測Class II器材的陶瓷電容破裂調查與客訴紀錄風險評估缺漏；為檢查缺失，非警告信。","source":"globalkeysolutions.net FDA 483 - Plexus Corp.","url":"https://www.globalkeysolutions.net/records/483/plexus-corp/f2d74b19-0144-402c-b9e6-58c93ea0dc0a","excerpt":null,"as_of":"2025-01-22","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單無 Item 4.02（財報不可信賴）申報。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000785786&type=8-K","excerpt":"共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 1 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"PLXS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":10.08,"operating_margin_pct":5.02,"fcf_margin_pct":-1.0,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLXS","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SANM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.01,"operating_margin_pct":5.49,"fcf_margin_pct":4.66,"rd_intensity_pct":0.26},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"BHE","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":10.38,"operating_margin_pct":4.25,"fcf_margin_pct":4.61,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BHE","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"FLEX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.5,"operating_margin_pct":5.44,"fcf_margin_pct":3.32,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"JBL","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.23,"operating_margin_pct":5.11,"fcf_margin_pct":3.82,"rd_intensity_pct":0.08},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL","as_of":"TTM ending 2026-08-31（4季加總）"}}],"subject":"PLXS"},"financial_history":{"ticker":"PLXS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-09-30","revenue":3811368000.0,"revenue_yoy_pct":null,"gross_margin_pct":9.11,"operating_margin_pct":4.73,"net_income":138243000.0,"diluted_eps":null,"free_cash_flow":-127852000.0,"fcf_margin_pct":-3.35,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-09-30","revenue":4210305000.0,"revenue_yoy_pct":10.47,"gross_margin_pct":9.37,"operating_margin_pct":5.2,"net_income":139094000.0,"diluted_eps":4.95,"free_cash_flow":61773000.0,"fcf_margin_pct":1.47,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":3960827000.0,"revenue_yoy_pct":-5.93,"gross_margin_pct":9.56,"operating_margin_pct":4.75,"net_income":111815000.0,"diluted_eps":4.01,"free_cash_flow":341320000.0,"fcf_margin_pct":8.62,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":4032966000.0,"revenue_yoy_pct":1.82,"gross_margin_pct":10.08,"operating_margin_pct":5.13,"net_income":172885000.0,"diluted_eps":6.26,"free_cash_flow":153967000.0,"fcf_margin_pct":3.82,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/PLXS/PLXS_Q4_2026_Earnings_Call_20261029.md）

# Q4 2026 Earnings Call
**Plexus Corp.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to the Plexus Fourth Quarter 2026 and Fiscal 2026 Earnings Conference Call. [Operator Instructions]
On the call today to answer your questions after the presentation are Todd Kelsey, President and CEO; David Abuhl, CFO and Senior Vice President; and Oliver Mihm, Executive Vice President and COO. I will now hand the conference over to Shawn Harrison, VP of Investor Relations. Shawn, please go ahead.

**Shawn Harrison** (Executives):
Good morning, and thank you for joining us today. Some of the statements made and information provided during our call today will be forward-looking statements including, without limitation, those regarding revenue, gross margin, selling and administrative expense, operating margin, other income and expense, taxes, cash cycle, capital allocation and future business outlook. 
Forward-looking statements are not guarantees since there are inherent difficulties in predicting future results, and actual results could differ materially from those expressed or implied in the forward-looking statements. For a list of factors that could cause actual results to differ materially from those discussed, please refer to the company's periodic SEC filings, particularly the risk factors in our Form 10-K filing for the fiscal year ended September 27, 2025, and the safe harbor and fair disclosure statement in our press release. 
We encourage participants on the call this morning to access the live webcast and supporting materials on Plexus' website at www.plexus.com, clicking on Investors at the top of that page. Joining me today are Todd Kelsey, President and Chief Executive Officer; Oliver Mihm, Executive Vice President and Chief Operating Officer; and David Abuhl, Senior Vice President and Chief Financial Officer. 
With today's earnings call, Todd will provide summary comments before turning the call over to Oliver and David for further details. Before turning the call over to Todd, please note that Plexus will attend Baird's Global Industrial Conference in Chicago on November 11 and Raymond James' TMT and Consumer Conference in New York City on December 7.
 
 With that, let me now turn the call over to Todd.

**Todd Kelsey** (Executives):
Thank you, Shawn. Good morning, everyone. Please advance to Slide 3. Plexus delivered an outstanding fiscal 2026 that exceeded expectations. Our differentiated value proposition anchored by unmatched quality and delivery creates significant opportunities for new and expanded customer relationships, positioning Plexus to generate robust financial returns and shareholder value. 
Plexus generated record fiscal fourth quarter revenue of $1.43 billion. This resulted in fiscal 2026 revenue increasing 23% year-over-year to approximately $5 billion. We are now forecasting fiscal 2027 revenue growth in the mid- to upper teens. Our wins performance remains strong, while our funnel of qualified manufacturing opportunities reached another record level, expanding $1.2 billion year-over-year to nearly $5 billion, supporting our diversified and accelerating revenue growth momentum. 
We delivered fantastic operating performance that exceeded our guidance. Fiscal fourth quarter non-GAAP operating margin of 6.7% increased 40 basis points sequentially and nearly 100 basis points year-over-year. Plexus exceeded its 6% non-GAAP operating margin goal for fiscal 2026, expanding non-GAAP operating margin 30 basis points to 6.2%. We're introducing a new non-GAAP operating margin goal of 6.5% to 7%, given our expectation of continued revenue growth and ongoing dividends from efficiency investments and our continuous improvement culture. 
Finally, fiscal 2026 ROIC exceeded our 15% enduring goal, supported by continued robust working capital efficiency and disciplined capital investment. We anticipate another strong ROIC result for fiscal 2027 and, at the anticipated revenue growth rate, continue to forecast free cash flow for fiscal 2027 exceeding $100 million. 
Please advance to Slide 4. Record revenue in the fiscal fourth quarter of $1.43 billion substantially exceeded our guidance range and increased 9% sequentially and 35% year-over-year. Excellent performance by our supply chain and operations teams helped our customers gain market share and Plexus capture stronger-than-anticipated end-market demand. In addition, non-GAAP operating margin of 6.7% and non-GAAP EPS of $2.84 substantially exceeded our guidance ranges on strong operating leverage from the revenue upside and continued efficiency gains. 
Please advance to Slide 5. Our go-to-market team secured 36 fiscal fourth quarter new manufacturing wins worth $290 million in annualized revenue when fully ramped into production. Each market sector delivered strong performance and secured exciting new customer programs and relationships that Oliver will discuss in more detail. With the strong fiscal fourth quarter performance, Plexus captured new manufacturing wins for fiscal 2026 worth nearly $1.2 billion in annualized revenue when fully ramped into production. 
This outstanding result reflected share gains with long-standing customers, the addition of exciting new customers that support growth technologies and continued expansion into attractive secular growth markets such as aerospace and defense, where we generated fiscal 2026 manufacturing wins of nearly $0.5 billion. 
The team generated these very strong wins while also expanding Plexus' funnel of qualified manufacturing opportunities by an exceptional $1.2 billion, or 33% year-over-year, to reach another record of $4.9 billion. The combination of our strong manufacturing wins performance and significantly expanded funnel of qualified manufacturing opportunities positions Plexus to sustain our diversified and accelerating revenue growth momentum. 
Please advance to Slide 6. Plexus' culture is foundational to our success and embodied by our team as they live our vision to help create the products that build a better world. Supporting our customers as the most trusted partner is central to our strategy. During the fiscal fourth quarter, Eaton recognized our team for operational excellence and honored Plexus with the Supplier Excellence Award at its Global Supplier Conference, a distinction granted to only 30 of Eaton's 30,000 global suppliers. 
And early in fiscal 2027, GE Vernova's Power Conversion and Storage business honored Plexus with its Lean Manufacturing Excellence Award. GE Vernova recognized the strong execution, continuous improvement culture and exceptional delivery performance by our sites in Oradea, Romania and Xiamen, China. 
I'm also incredibly proud to share that our Kelso, Scotland operations were named Manufacturing Business of the Year at the 2026 Scottish Borders Business Excellence Awards, while also earning high commendations for both Innovation in Business and Large Business of the Year. These recognitions celebrate our Kelso team's operational leadership, technological innovation and role as an employer and partner of choice in the EMEA region. Our team members' dedication also extends deeply into our communities. 
For fiscal 2026, our global team shared its time and talents with various local causes, donating approximately 35,000 hours of paid volunteer time off. Further, the Plexus Community Foundation granted $1.5 million in charitable donations to nonprofits globally, expanding our community impact and demonstrating how we actively live our vision of building a better world. 
Finally, we continue to take proactive steps to reduce our environmental impact. In fiscal 2026, we generated an incredible result and reduced our absolute Scope 1 and Scope 2 greenhouse gas emissions by more than 50% across our global manufacturing sites compared to our fiscal 2023 baseline. I continue to be immensely proud of our global team members as we deliver excellence, live our values and create a lasting positive impact for our customers, our communities and the world.
Please advance to Slide 7. For our fiscal first quarter, we are guiding revenue of $1.41 billion to $1.46 billion, representing 1% sequential and 34% year-over-year growth at the midpoint. We anticipate strong year-over-year revenue growth from each of our market sectors with sequential revenue expansion in aerospace and defense and Healthcare/Life Sciences market sectors, balancing a demand normalization in our industrial market sector. 
We are also guiding non-GAAP operating margin of 6.0% to 6.4%, an increase of 40 basis points year-over-year at the midpoint and non-GAAP EPS of $2.46 to $2.62. We remain focused on expanding operating margin and delivering robust returns even as we are increasing our investments in our people and technology to support stronger-than-anticipated revenue growth.
For fiscal 2027, we are increasing our revenue growth forecast to reflect our robust fiscal 2026 finish, stronger end-market demand and continued program ramps. We now anticipate delivering mid- to upper teens revenue growth with expansion in operating margin and sustained working capital efficiency. 
We continue to see exceptionally strong growth from our aerospace and defense and industrial market sectors, including semiconductor capital equipment associated with our support of growth technologies and the benefit of ongoing market share gains. In addition, we now anticipate stronger growth from our Healthcare/Life Sciences market sector associated with increased end-market demand, particularly from new programs we launched during fiscal 2026. 
Finally, through our aligned focus on innovation and continuous improvement culture, Plexus is creating customer success, scaling the company for the future and developing substantial long-term efficiencies that will generate robust financial returns and shareholder value. 
I will now turn the call over to Oliver for additional analysis of the performance of our market sectors. Oliver?

**Oliver Mihm** (Executives):
Thank you, Todd. Good morning. For each of our market sectors, I will discuss our fiscal fourth quarter and fiscal year performance, our expectations for our fiscal first quarter, review the annualized revenue contribution of our quarterly wins performance and offer growth commentary for fiscal 2027. I will also provide an overview of our record funnel of qualified manufacturing opportunities. 
Beginning with our Aerospace and Defense sector on Slide 8. Fiscal fourth quarter revenue decreased 4% sequentially compared to our expectation of approximately flat performance as timing dynamics with materials more than offset strength in new program ramps and customer demand pull-ins. We anticipate capturing any deferred demand during our fiscal first quarter. 
Fiscal 2026 saw the aerospace and defense sector revenue grow 23%. Growth was driven by remarkable strength in the defense and unmanned subsectors, a return to growth in commercial aerospace and new program ramps in the security and space subsectors. For our fiscal first quarter, we expect revenue to be up high single digits sequentially on strength in the defense and space subsectors. Fiscal fourth quarter wins for the aerospace and defense sector were strong at $90 million.
This quarterly result reflects a 67% year-over-year increase and brings the total fiscal year wins for the sector to an extraordinary $490 million. For comparison, this fiscal year's aerospace and defense sector wins performance exceeds the combined wins in this sector for fiscal years 2023, 2024 and 2025. Our team in Neenah, Wisconsin is excited to welcome a new customer to Plexus with a win of a product that supports defense pilot combat training. 
The partnership our teams developed over the past 18 months as they worked together to ensure a smooth product launch supported the win. In addition, our historically strong execution and depth of knowledge contributed to the award of a flight refueling system from an existing customer for our team in Kelso, Scotland. Looking ahead to fiscal 2027, we continue to see the potential for another year of robust revenue growth for our aerospace and defense sector. 
We expect revenue growth to exceed 20% with exceptional growth from our defense, unmanned, security and space subsectors associated with program ramps, market share gains and robust end-market demand as well as continued commercial aerospace demand improvement.
Please advance to Slide 9. Healthcare/Life Sciences market sector revenue increased 6% sequentially for our fiscal fourth quarter. The result exceeded our expectation of approximately flat revenue due to improved demand from our customers and our team's ability to pull in the required materials to support the growth. 
Our Healthcare/Life Sciences market sector grew a robust 19% for fiscal 2026, well ahead of our estimate of a mid-single-digit market growth rate. The therapeutics and imaging subsectors drove the strong performance. For our fiscal first quarter, we expect revenue growth to be up low single digits on strength in the therapeutics and monitoring subsectors from demand increases and program wins. Healthcare/Life Sciences sector wins for the fiscal fourth quarter were $74 million, representing a 35% year-over-year increase. 
Our wins for the fiscal fourth quarter included the addition of 3 new customers to Plexus. Our team in Chicago, Illinois welcomes one of these new customers, and we'll be building a light imaging product that supports robotic surgical procedures. Our proactive engagement and our ability to support the customer with product design, manufacturing production and aftermarket sustaining services contributed to the win. 
Another of the new customers will be supported by our team in Bangkok, Thailand as they were awarded the production of a Class III registered FDA device for cardiac defibrillation. The customer noted that Plexus' medical device and regulatory competence as well as our regionalization expertise drove the award. 
Looking ahead to fiscal 2027 for our Healthcare/Life Sciences sector, we now see the potential to grow revenue high single digits, exceeding market growth, which we estimate to be mid-single digits. Our updated outlook is supported by existing and new program ramps and general demand increases, led by the strength in the therapeutics and monitoring subsectors. 
Advancing to the industrial sector on Slide 10. Fiscal fourth quarter revenue increased 17% sequentially, well ahead of our forecast for high single-digit to low double-digit growth. Driving the upside was the ability of our supply chain and operations teams to quickly react and support semi-cap, industrial equipment and communications customers in capturing stronger demand and market share gain opportunities. 
Our industrial sector grew 27% in fiscal 2026. This extraordinary result was driven substantially by our semi-cap subsector where revenue increased 50% year-over-year as well as growth in our industrial equipment subsector. Market share gains, new program ramps and customer demand increases all contributed to the outstanding result. 
For the fiscal first quarter, we expect revenue for the industrial sector to be down low single digits. Semi-cap subsector revenue increases are being offset by customer program timing dynamics and demand normalization in our communications subsector following fiscal fourth quarter upside. Wins for the industrial market sector were strong for the fiscal fourth quarter at $126 million. 
Our team in Boise, Idaho won a substantial award from a new customer for the production of a clean tech battery energy storage system supporting smart grid applications. The customer noted the strength of our collaboration and our cultural alignment as contributing to the award. In addition, our team in Penang, Malaysia won a substantial follow-on award from an existing semi-cap customer based on the strength of our historical execution. 
We continue to see the potential for a very strong fiscal 2027 for our industrial market sector. We expect revenue growth to exceed 20%, supported by continued robust growth from our semi-cap subsector as well as growth from our test and measurement, robotics and automation and energy subsectors. 
Please advance to Slide 11 for a review of our funnel of qualified manufacturing opportunities. The funnel reached another record this quarter. The strength of our funnel is positively influenced by a number of factors, including the breadth of our service offering, our commitment to creating strong partnerships with our customers and our relentless focus on providing unmatched quality and delivery. 
At $4.9 billion, the funnel reflects a 33% year-over-year and 10% sequential increase, driven by record contributions from our aerospace and defense and industrial market sectors. The funnel growth is remarkable, considering the strong fiscal 2026 wins performance of $1.2 billion. 
 I will now turn the call over to David. David?

**David Abuhl** (Executives):
Thank you, Oliver, and good morning, everyone. Our fiscal fourth quarter results are summarized on Slide 12. Gross margin of 10.2% met our guidance, benefiting from leverage on higher revenue and continued operational efficiency gains. Selling and administrative expense of $59.7 million included typical stock-based compensation as well as expenses related to executive retirement. 
Excluding these expenses, we gained 30 basis points of sequential leverage. Our fiscal fourth quarter non-GAAP operating margin of 6.7% exceeded our guidance, benefiting from end-of-year fixed cost leverage on the stronger-than-anticipated customer demand, operational efficiencies and continued cost discipline. 
Non-GAAP diluted earnings per share of $2.84 exceeded the top end of our guidance due to higher revenue and the other items mentioned, partially offset by a tax rate at the upper end of guidance. Turning to our cash flow and balance sheet on Slide 13. For the fiscal fourth quarter, we delivered better-than-expected free cash flow of $6 million, reflecting $29 million in cash from operations and $23 million in capital expenditures. 
We repurchased approximately $21 million of our stock in the quarter, completing the expanded 2026 share repurchase program. The 2027 share repurchase program was approved by our Board in August for $100 million, all of which is available for fiscal 2027 and our repurchases are underway. We ended the fourth quarter in a net cash position, and we had $159 million outstanding under our revolving credit facility with over $340 million available to borrow. 
Return on invested capital was 15.8% in the fiscal fourth quarter, 680 basis points above our weighted average cost of capital. Our fiscal fourth quarter result was the highest in nearly a decade and above our enduring goal of 15%. While continuing to increase invested capital to support our robust revenue growth, we anticipate continuing to generate healthy ROIC for fiscal 2027 from our expanding margins and working capital efficiency. 
Now turning to working capital trends on Slide 14. We ended fiscal 2026 at a 62-day cash cycle, our best performance on record and down 1 day compared to the prior year. I'm very pleased with how our teams are partnering closely with our customers and suppliers and driving improvements across all areas of working capital while continuing to make the investments needed to fuel our robust revenue growth.
Please advance to Slide 15. I would like to take a moment to commend our teams on delivering a really great year, and I'm especially pleased to see the progress on expanding our margins. For fiscal 2026, we delivered non-GAAP operating margins of 6.2%, a 30 basis point increase from the prior year, including a tremendous result in the fourth quarter. 
Going forward, having consistently exceeded our previous 6% goal, we are introducing a new non-GAAP operating margin goal of 6.5% to 7%. This new goal will be supported by our strong operational momentum, continued anticipated revenue leverage and a balanced ongoing approach to our investments in growth, people and technology. We take a methodical approach to setting our financial goals, and our expectation is to consistently meet and then progress through the goal. 
We expect to deliver on our 6.5% to 7% non-GAAP operating margin goal from continued revenue leverage and operational efficiencies, while we expect a fairly muted impact from price and mix. We will balance these benefits with continued investments in our people, technology, capacity and capabilities. This new target represents a larger step-up than we have historically provided as we have growing confidence in the dividends from our efficiency and automation initiatives and our continuous improvement culture. 
Over the past 2 years, our team's efforts have driven a greater than 10% gain in our equipment efficiency, allowing our operations to generate greater revenue and profitability without significantly expanding capital spending. We've also seen revenue per team member expand by approximately 20% over the same time period. And while the revenue outlook is an important backdrop for our new margin goal, we are seeing dividends from our investments in operational efficiency, and we expect to continue to accrue benefits. 
Now let me turn to our fiscal first quarter guidance summarized on Slide 16. As Todd has already provided the revenue and EPS guidance, I will review some additional details. Fiscal first quarter gross margin is expected to be in the range of 9.7% to 10%, including expansion of investments in people and technology. 
For fiscal 2027, we expect gross margins to remain at approximately 10%. Our outlook for selling and administrative expense for the fiscal first quarter is in the range of $61 million to $62 million, including stock-based compensation. Excluding these expenses, we expect the percent of revenue to be flat compared to the prior quarter, while for fiscal 2027, we expect to gain leverage on higher revenue and continued cost discipline. 
Fiscal first quarter non-GAAP operating margin is expected to be in the range of 6% to 6.4%, exclusive of stock-based compensation. At the midpoint, this would represent a sequential decline compared to the fiscal fourth quarter as we expand investments in people and technology given the improved fiscal year revenue outlook. 
Given the timing of the investments in our revenue momentum, we currently anticipate minimal to no decline in our fiscal second quarter operating margins from typical seasonal cost increases. And finally, for fiscal year 2027, we continue to expect our ongoing investments will result in operating flow-through at the low end of our 8% to 12% target range, driving expansion in non-GAAP operating margin compared to the prior year. 
We're estimating a non-GAAP effective tax rate of between 16% and 18% for the fiscal first quarter and a similar range for fiscal 2027. In support of our accelerating revenue momentum, we continue to strategically increase our working capital investments and expect our fiscal first quarter cash cycle to be in the range of 66 to 70 days. 
We typically experience around a 6-day sequential increase in our fiscal first quarter cash cycle days associated with the end of many of our customers' fiscal years. For fiscal 2027, we continue to expect cash cycle days to be in the low to mid-60s. Turning to capital expenditures. Long term, we continue to target spending in the range of 2% to 3% of revenue. Given our robust revenue growth trends, capital expenditures for fiscal 2027 will likely fall toward the upper end of that range. 
We remain committed to deploying capital diligently and are pleased with the very strong returns our investments in capabilities, capacity and technology are generating. As a result of these factors and the timing of our working capital investments, we are forecasting a use of free cash flow in the fiscal first quarter, including the annual payments for our incentive compensation program. For fiscal 2027, we still expect to generate in excess of $100 million of free cash flow, benefiting from our sustained robust profitability and our focus on working capital efficiency. 
With that, Jen, let's open the call for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of David Williams with Needham & Co.

**John Patrick Malloy** (Analysts):
This is Patrick Malloy on for David Williams at Needham. Congrats on the quarter. To jump right into it, how much of the demand acceleration reflects customer forecast increases versus pulling orders forward to secure that capacity or components? And are you guys seeing forecasts revised upwards that may give you more confidence in the durability of demand?

**Oliver Mihm** (Executives):
Yes. I would say that customer demand increases are forming a substantial part of our outlook and the increase that you saw in outlook relative to last quarter. And then relative to our ability to pull in materials, you saw the results from Q4. Certainly, from a materials perspective, we consider the environment to be challenged. 
We're always working the angle here to help support our customers, close partnership with our customers, a number of tools we have in place to help ensure that we can capture those materials. I can go into more detail there, if you'd like. But in general, I think our assessment of risk associated with materials is already contemplated in the forecast.

**John Patrick Malloy** (Analysts):
Okay. Great. And then maybe quickly as a follow-up in semi cap, how much of that growth is driven by increases in demand on existing programs versus new customer programs? Or is that also coming from share gains? And if the demand in the wafer fabrication equipment environment moderates, how quickly will that flow through to your business? Congrats again.

**Todd Kelsey** (Executives):
Yes. Thanks again, Patrick. This is Todd this time. Within semi cap, there are a number of factors that are driving our revenue growth there. There certainly is increasing end-market demand, but we took a significant amount of share, particularly through the last downturn within the semi-cap market, and that's coming to bear right now. 
We also continue to take some additional share as we're going through this upcycle because of our ability to outperform. And if you take a look at our results, as Oliver mentioned, for the fiscal year, we're up about 50% within the semi-cap space, way above WFE, and we expect we'll continue to do that as we go through fiscal 2027.

**Shawn Harrison** (Executives):
I think for the downturn question, Patrick, this is Shawn Harrison. The surprising thing is typically, we take more share during the downturn, as Todd mentioned, and you see less share gains during an upturn as customers are just looking to secure demand and fulfill demand. And so the fact that we're taking share during an upturn is a positive sign. And we would expect, as we've seen in past cycles, to be able to outperform the market because of the share capture we generate.

**Operator** (Operator):
Your next question comes from the line of Steve Barger with KeyBanc Capital Markets.

**Steve Barger** (Analysts):
I wanted to start with free cash flow. You expect $100 million in FY '27 despite raising revenue to the upper -- mid- to upper teens. If demand exceeds that outlook again, does free cash flow necessarily decline because of working cap? Or are you seeing customer funding and operating efficiency that kind of changes that relationship and you can maintain that level on revenue upside?

**David Abuhl** (Executives):
Steve, this is David. Yes, we're pleased with the outlook at the moment. And if you looked at the delivery on cash cycle days, and we ended at a record low, our teams are really performing well in terms of the efficiency of the capital investments we're making in working capital. And we usually say we need about $0.15 to $0.20 of working capital for revenue growth. And that's -- we're right in that maybe 17% range. 
 
In fact, we've added nearly $1.5 billion of revenue growth in the last year on an annualized basis, but we've added $250 million of working capital to support that. And so as we go through the year, we're confident in generating that $100 million of free cash flow, and let's see how we do as we rate the year. But so far, so good, and I think we're pretty confident in this business generating great free cash flow this year.

**Shawn Harrison** (Executives):
And Steve, it's Shawn. Just to follow up on that, we and the team are very diligent in trying to offset investments in working capital with corresponding commensurate investments by our customers in that inventory to make sure that we're continuing to hit these record low cash cycle days, which, as David said, is the best we've seen on record. So it was a fantastic result.

**Steve Barger** (Analysts):
Yes. That's a good outcome. And just thinking about the operating margin goal of 6.5% to 7%, can you frame up what brings you to the low versus the high end? Is it mix versus leverage or Penang maturation? Or just what are the swing factors that you see in that range?

**David Abuhl** (Executives):
Yes, Steve, on these targets, we like to consistently exceed but then progress through these targets. We have a track record of doing that with the last couple that we've set. And in the moment, you'll see our flow-through rate, we stay at 8% to 12% flow-through on revenue growth. And at the moment, we're tracking toward the lower end of that, given the investments we're making -- to support accelerating revenue momentum. 
 
And so as you model in that flow-through rate, I think that will get you a pretty good balance of what we think margins will look like for the quarter, for the year, et cetera. But our teams are really working hard to consistently meet this next target and then progress through it. But I'd say that the growth elements are there. The up elevators, as I like to call them, on margin are strong in terms of leverage on revenue growth. 
 
The operational efficiency gains are really coming through strong as well. And we just need to balance that with the investments needed for kind of the next chapter of growth that's ahead of us. But overall, it's upward momentum for us, and we'd like to progress through this target. So I'd say the answer to that is watch that 8% to 12% kind of closely, as the investments are the balancing factor there.

**Operator** (Operator):
Your next question comes from the line of Melissa Fairbanks with Raymond James.

**Melissa Dailey Fairbanks** (Analysts):
I would wish you congratulations on the Brewers win last night, but I'm still a little bit sore as a Rays fan. So anyway, congratulations on a great quarter. I have a question probably for Oliver. Looking into aerospace and defense, some of these new wins, I think a quarter or a couple of quarters ago, some of the commentary had been that you haven't yet seen an uptick in NATO spending. Wondering what some of the dynamics are there, if these are new spending -- understanding that these are very long term, but if these are new spending programs or if this is just an extension of newer technologies that are moving into this space?

**Oliver Mihm** (Executives):
Yes, I'll say it's a bit of both. So we do see that defense spending flowing through to an extent. But then, as we noted, some of the technology wins here that we had recently in this past quarter, also seeing new technology, new entrants. One of the things that we like is our engagement with non-primes, I'll say, within this space. 
 
We think that's a really good fit and a tailwind as we look forward here. And then I'll flip that also over to Europe and say from an EU side, still early days and still seeing a potential tailwind as we look forward from an EU perspective, and we think we're well positioned there as well.

**Melissa Dailey Fairbanks** (Analysts):
Okay. Perfect. And maybe I'll kind of stretch that same question into the Healthcare/Life Sciences business. We know that historically, you guys have had really strong engagements on the imaging and the diagnostics and surgical side. It sounds as though you may be extending into newer types of engagements. Wondering if you could comment there.

**Oliver Mihm** (Executives):
Yes. A couple of things there. I think our optimism, our confidence in our growth outlook here certainly stems from coming off a really strong '26 at 19%, well ahead of market, which we think is mid-single digits. As you noted, the strength in therapeutics and monitoring underscores that, right? And so that's kind of maybe your point about what we've historically seen. 
 
Certainly seeing new -- our engagement with secular growth technologies, like robotic surgery, like pulsed field ablation, I think those things give us further optimism here as we look forward into the coming year. Yes. And one other comment I'll make, which isn't directly related to your question, but I think provides us some optimism on future tailwinds, is historically, our engineering development work has been a bit of a leading indicator for us. And our funnel inside engineering for Healthcare/Life Sciences took a marked uptick in Q4. So that gives us also some optimism here in terms of future outlook.

**Operator** (Operator):
Your next question comes from the line of Anja Soderstrom with Sidoti.

**Anja Soderstrom** (Analysts):
Congratulations on the great quarter here. Just curious in the aerospace and defense, first of all, the commercial air, what are you seeing there?

**Todd Kelsey** (Executives):
Yes. We're seeing slightly incremental demand improvements in commercial aerospace. I think it still hasn't hit the levels that we think it's capable of once we see the Boeing demand flow all the way through to us.

**Anja Soderstrom** (Analysts):
And is that included in your guidance now or the more meaningful comeback there or.

**Todd Kelsey** (Executives):
No. No, it's not. We're still taking a conservative approach on when that happens and to what level it happens.

**Anja Soderstrom** (Analysts):
Okay. And then within space, are you -- do you have any exposure to the LEOs at all or...

**Shawn Harrison** (Executives):
Yes. So Anja, it's Shawn. In space, we -- as we like to say, have more electronics on orbit than any other EMS provider and probably by a considerable amount. We play strongly in LEO satellites and communication systems. And so unmatched quality and delivery is paramount in generating success in that market. And so very strong position and would anticipate to see strong growth as that market continues to expand.

**Anja Soderstrom** (Analysts):
Okay. And then within semi cap, where do you think we are there now in the cycle? What do you see? What kind of visibility do you have in the coming quarters or years?

**Oliver Mihm** (Executives):
Yes. I guess I'll start by saying we talked on the call in our prepared remarks about our growth here in the past fiscal year being 50%. As we contemplate the calendar year, which will be coming up here at the end of this quarter, we expect that growth rate to be even stronger. And so our demand continues to show improvement. I mentioned that here for the current quarter outlook, we continue to see strength of demand. So generally, I would say, still strong and still growing.

**Todd Kelsey** (Executives):
Yes, we probably have -- I mean, I would say we have reasonable visibility for the next year or so within the pipeline of our customers.

**Shawn Harrison** (Executives):
And Anja, I would say that visibility came into view probably a little bit earlier than normal. We talked about that last quarter, which gave us some of the confidence in providing an early fiscal year view back in July. I know some of the industry forecasts are strengthening for out years. Being conservative as we are, we also understand that semi cap is cyclical. And so just taking a cautious approach of how that market will sustain the growth, but also very focused in on capturing the market share, which drives our outgrowth.

**Anja Soderstrom** (Analysts):
Okay. And then have you seen any changes to the competitive environment at all?

**Todd Kelsey** (Executives):
Not really. No. It's pretty similar.

**Operator** (Operator):
Your next question comes from the line of David Williams with Needham.

**David Williams** (Analysts):
Congrats on the really solid results. Just quickly, I wanted to ask maybe on the semi-cap visibility, and I think you touched on this a bit earlier, but one of your competitors or maybe peers had mentioned that the demand forecasts are certainly firming and they're seeing forecasts out to 2029 and 2030. Do you think that -- I mean, is it fair to say you're probably seeing the same things and that, that demand is fairly sustainable? And it's always cyclical, and I think, Shawn, you had talked about that earlier. But just kind of curious what you're seeing from that demand environment. It feels like those elongated forecasts are getting maybe more prevalent.

**Todd Kelsey** (Executives):
Yes. The demand environment is good, but I think to project out several years would probably be a little bit too far at this point. I would say we feel comfortable with fiscal '27, but I wouldn't want to look out any further than that.

**Shawn Harrison** (Executives):
We've seen the industry forecasts strengthen as everybody has in terms of the third-party forecasters. I would just go back to the earlier statement that we take a conservative approach in understanding a market that historically has had some cyclicality.

**David Williams** (Analysts):
Sure. That makes sense, and that's very fair. Then maybe secondly, just maybe across the customer base, is there a way to maybe disaggregate the revenue by maybe customers that are increasing their demand forecast or existing programs versus maybe how much of the demand or the growth that you're seeing is coming from new programs?

**Oliver Mihm** (Executives):
Yes, I'll give that a shot, David. Broadly, I mean, especially given the strength of our outlook here on the fiscal year, customers are strengthening their forecasts. We gave some specific commentary that we're seeing uplift there in the Healthcare/Life Sciences sector. That was a bit of a turning of a corner for us or seeing an improvement, maybe is a better word choice. And then within industrial and aerospace, that's generally been strong. Obviously, there's always puts and takes. But I would say that net-net, quite strong in terms of supporting our outlook here for fiscal '27.

**Operator** (Operator):
Our next question comes from the line of Steve Barger with KeyBanc Capital Markets.

**Steve Barger** (Analysts):
Just wanted to ask about the top 10 customers. I think that increased from 49% in fiscal '25 to 56% in fiscal 4Q '26. And I get it, like you're seeing some really significant ramps from large programs. But when you look at the funnel, are you becoming structurally more concentrated as you scale? Or how should we think about that?

**Todd Kelsey** (Executives):
I would say, in general, Steve, the answer is no. The 56% is kind of a historical number that we've had if you go back over time and 49% is a little bit on the low side. But we did get some pretty good growth from our top 10 customers this year. So we're certainly aware of that and appreciative of that from our customers.

**Steve Barger** (Analysts):
Got it. Okay. And then last one. Can you give us an update on some of the AI investments or the productivity initiatives and how you're thinking about increasing revenue per square foot in North America versus Europe versus Asia? Just any update operationally on how you're getting more throughput through the plants?

**Oliver Mihm** (Executives):
Yes, sure. Happy to handle that or talk to that. So I'd like to provide a couple of examples because I think it makes it very poignant for folks, right? So just as an example, one of the tools that we have internally that we call Excellence Guide is a tool that enables operator efficiency, agility and quality and enables us to turn over the line quickly as we move from one assembly to the next. And our deployment on that front saw 110% pickup year-over-year. 
 
And so those are the kinds of things that we're doing to drive efficiency. We talk about specific outcomes to that. For instance, revenue per employee up 25% if you compare Q4 of fiscal '24 to Q4 of fiscal '26. And so those are the types of activities we're driving both to improve our labor efficiency, our labor output as well as driving improvement from an, I'll say, asset utilization perspective, whether that's bricks and mortar or machine capacity. 
 
We've talked historically about, from a machine capacity perspective, over that same time period, a 12% increase in how we're utilizing those machines and getting more efficiency out of the capital.

**Steve Barger** (Analysts):
Is that -- are those initiatives kind of uniformly spread across the footprint? Or do you expect to see some pretty -- are there still sizable levers to pull in terms of driving incremental efficiency from here?

**Oliver Mihm** (Executives):
Well, there's certainly still sizable opportunity in front of us. So we continue to focus on it. This isn't a thing that we did last year and we're done. I would say that it's fairly consistent across the organization. But as you can imagine, there are things that we pilot in one organization and then we propagate more globally. And so by way of an example there, we use AI to automate the procurement of low-dollar POs to our suppliers. 
 
We're currently handling about 80% of our receipts through that AI agent that started in the AMER region and is now deploying out into our Asia Pacific and EMEA regions. And what that enables us to do, it enables our procurement folks to instead work on closing the gaps, finding the miracle, securing the parts for challenging dynamics and hitting the upside for our customers and potentially helping them to capture share gain. Does that help answer that?

**Operator** (Operator):
There are no further questions at this time. I will now turn the call back to Todd Kelsey for closing remarks.

**Todd Kelsey** (Executives):
Thank you, Jen. In closing, thank you to our Plexus global team for their passion and leadership in delivering a fantastic fiscal 2026. Additionally, thank you to our customers for their partnership as we help create the products that build a better world. I'm excited for fiscal 2027 and the positive momentum created by our team. I expect they'll generate a fantastic performance in fiscal 2027, and I look forward to speaking with everyone early next year. Thank you to all who joined our call today. Have a nice day.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### PLXS_Q3_2026_Earnings_Call_20260730.md
- 2026-07-30｜CEO｜guidance：FQ4 營收財測區間（原話："We are guiding revenue of $1.33 billion to $1.38 billion"）
- 2026-07-30｜CEO｜guidance：FQ4 非GAAP營益率與EPS財測（原話："non-GAAP EPS of $2.47 to $2.63."）
- 2026-07-30｜CEO｜guidance：FY2026 營收成長預期（原話："deliver more than 20% revenue growth for fiscal 2026"）
- 2026-07-30｜CEO｜guidance：FY2027 營收成長潛力高於長期目標（原話："generate revenue growth in excess of our 9% to 12% goal"）
- 2026-07-30｜CFO｜guidance：FQ4 毛利率財測區間（原話："range of 10% to 10.3%. At the midpoint, gross margin will"）
- 2026-07-30｜CFO｜guidance：FY2027 非GAAP稅率初步看法（原話："between 16% and 18%"）
- 2026-07-30｜CFO｜guidance：FY2026 資本支出預期不變（原話："forecast is unchanged at $100 million to $120 million"）
- 2026-07-30｜CFO｜guidance：FQ4 自由現金流預期（原話："breakeven or a slight usage of cash"）
- 2026-07-30｜IR VP｜guidance：A&D 本季預期持平（原話："approximately flat versus our fiscal third quarter"）
- 2026-07-30｜IR VP｜guidance：A&D FY2027 成長高於長期目標（原話："should well exceed our 9% to 12% goal"）
- 2026-07-30｜IR VP｜guidance：HLS FY2026 成長預期（原話："we now anticipate revenue to increase in the high teens"）
- 2026-07-30｜CFO｜margin：S&A 槓桿口徑：扣除股權報酬與高管退休費用後的槓桿（原話："gained nearly 50 basis points of leverage compared to our"）
- 2026-07-30｜CFO｜margin：管理層對營益率目標的表述（原話："delivering non-GAAP operating margin at or above 6%"）
- 2026-07-30｜CFO｜margin：FY2027 營益率擴張，細節留待下季說明（原話："including future expectations for operating margin"）
- 2026-07-30｜CEO｜margin：新增產能預期對毛利影響（原話："we wouldn't expect it to have a meaningful impact"）
- 2026-07-30｜CFO｜margin：現金循環天數成果（原話："We delivered a 62-day cash cycle in the fiscal third"）
- 2026-07-30｜CFO｜margin：年底現金循環天數預期（原話："cash cycle days in the low to mid-60s"）
- 2026-07-30｜CEO｜commitment：FY2027 營益率擴張承諾（原話："we anticipate delivering operating margin expansion"）
- 2026-07-30｜CFO｜commitment：FY2027 自由現金流承諾（原話："free cash flow generation in excess of $100 million"）
- 2026-07-30｜CFO｜commitment：FY2027 資本支出維持營收2–3%（原話："range of 2% to 3% of revenue."）
- 2026-07-30｜CFO｜capital_allocation：FQ3 股票回購金額（原話："We repurchased $20.6 million of our stock"）
- 2026-07-30｜CFO｜capital_allocation：八月與董事會討論新回購授權（原話："We will discuss our next share repurchase authorization"）
- 2026-07-30｜CFO｜capital_allocation：馬來西亞擴產決定（原話："we've made the decision to expand"）
- 2026-07-30｜CEO｜capital_allocation：新增產能規模（原話："somewhere north of $0.5 billion of"）
- 2026-07-30｜IR VP｜capital_allocation：現有產能可支撐營收規模（原話："close to $6 billion of revenue"）
- 2026-07-30｜IR VP｜competition：半導體設備營收預期優於WFE（原話："we would expect to outgrow WFE again next year"）
- 2026-07-30｜CEO｜competition：份額成長與新專案為成長來源（原話："market share gains and support of disruptive"）
- 2026-07-30｜CFO｜risk：管理層承認供應鏈有吃緊點（原話："But there are tight spots. We're not going to gloss"）
- 2026-07-30｜CEO｜risk：預置庫存由客戶資金支應（原話："typically funding those replacements."）
- 2026-07-30｜IR VP｜product：HLS FY2027 短期成長趨緩（原話："we expect short-term growth moderation as activity"）
- 2026-07-30｜CEO｜product：資料中心策略funnel規模（原話："funnel that's conservatively somewhere around $0.5 billion"）
- 2026-07-30｜CEO｜customer：本季新專案贏單（原話："we secured 31 new manufacturing programs with $255 million"）
- 2026-07-30｜CEO｜customer：合格機會funnel創高（原話："opportunities expanded to a record $4.5 billion"）
- 2026-07-30｜IR VP｜customer：工業部門本季季增（原話："revenue increased 23% sequentially"）

### 問答異常語氣（迴避／改口／保留）
- PLXS_Q3_2026_Earnings_Call_20260730.md｜問：Ruben Roy 追問 A&D 與工業要達到強勁雙位數所需的成長與市場/份額拆分｜答法：Shawn Harrison 未給 A&D FY2027 成長百分比，回「I'll let you do the math to back into what the percentage must be」

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

`scenario_inputs`（EPS路徑五年、終端倍數、機率、yield、second_stage、Max DD範圍與依據）——你不寫`scenario.json`，那份由程式跑`dd_scenario.py`產生。**估值口徑由程式決定（2026-10-12）**：事實表`f_consensus_eps_fy1`≤0（虧損）→尾段給`sales_multiple`形狀，情境樹改填營收路徑×終端EV/S：`start`={`rev`=`f_rev_consensus_fy1_m`、`ev_s`=`f_ev_s_fwd`、`basis`}，`rev`五年路徑(百萬)、`ev_s`終端EV/S、`net_debt_y5`/`shares_y5`(終端淨負債/稀釋股數，須反映該情境的現金燒耗、再融資與增資稀釋；null=沿用目前`f_net_debt_m`/`f_shares_diluted_m`)；終端每股價=max(0,(營收×EV/S−淨負債)÷股數)，Bear債務吃光股權就讓它歸零。此模式不填`eps`/`pe`/`second_stage`；Bear/Base/Bull散布、機率、Max DD、年期規則照舊，「EPS分母同源」改為「EV/S分母(FY+1或終端年營收)與現價EV/S同源」，三分量拆解改看「每股營收複利/EV/S變動」，倍數貢獻≥Base合計IRR的40%同樣標「估值依賴型」。Bear機率5Y不應<20%(多數25-30%；極強護城河+短期已兌現才壓15-20%)；Bull/Bear散布5Y應比1Y/2Y寬≥50%；Base機率不應>50%；bear機率須註明依據，sourced結構性durability仍硬套bear需說明「為何不採信」否則不得高於base [§3]。
- 內生天花板sanity check：Base情境EPS CAGR貢獻vs§5.R內生天花板(同組數字不重算)→天花板內✅/超出⚠(⚠→Bear機率強制≥30%)。成長熄火：3年後成長率降至15%/10%/5%三情境×Forward P/E壓縮→估值跌幅，作Bear PE錨。三分量拆解(≤80字，Base IRR多少來自EPS複利/re-rate/股息淨回購)：re-rate貢獻≥Base合計IRR的40%→標記「估值依賴型」(`decision_inputs.valuation_dependent=true`) [§3]。
- IRR落點：<8%/yr弱、8-12%中、>12%強、>15%罕見，不作跨檔排序依據。AR=`(P_bull×|Bull5Y%|)÷(P_bear×|Bear5Y%|)`，<2平庸/2-4偏正/≥4顯著，非放鬆機率防線理由。年期硬規則：①表頭終端年=主時距終端年②終端倍數EPS分母年期與現價倍數同源③終端倍數必附≥1個同業現值comp對照 [§3]。10Y二段延伸(`runway_post_y5`=🟢且終端倍數承重，或Base IRR實質來自Y5後)：Y5→Y10 EPS CAGR/10Y累積倍數/IRR。R:R數學假象：下行>15%正常使用；5-15%警示「已接近定價」；<5%失效標「數學假象」禁引用進場判定，改極端Bear(Bear PE×0.8+Bear EPS×0.85)重算(Bear EPS=FY+1 EPS×0.9；Bear PE=成長熄火「降至10%」情境) [§3]。

**Max DD**(`premortem.max_dd`)：填範圍`lo`/`hi`(禁單點，寬度≥10pp)+`path_risk`(🟢0～−30%/🟡−30～−50%/🔴<−50%)；推導依據須寫`reasoning.premortem`。硬接線：🔴且thesis脆弱(`moat.trend`↓或`runway_post_y5`🔴或估值依賴型)→倉位上限下修(6%→≤3%)；🔴但thesis完整→不因波動砍倉，註記「深回撤心理準備」[§2問六]。

**必答項**：`scenario_inputs`三支EPS路徑、終端倍數、Bear/Base/Bull機率、`premortem.max_dd.lo/hi`、`path_risk`（sales_multiple模式：三支營收路徑、終端EV/S、淨負債、股數，其餘同）。

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

## ⑥ 條件附卡（archetype_hint='EMS/ODM' 命中）：judge_addendum_cyclical.md

<!-- source: .claude/skills/stock-analyst/references/cyclical-lens.md sha256:b13d95972edd47ea git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary 或 secondary ∈ {循環/商品，EMS/ODM}（QC-43 判定，含 capex 建設循環／需求量循環子型） -->

# QC-42 循環交易讀數（附錄 B）附卡

循環股的錢在 Game 2（投降買、延伸賣）。本附卡是平行、明標投機的交易讀數，不改長抱裁決。[§WHY]

## 一、觸發與子型判定
無循環 sleeve（純成長 mis-route）→ 整段省略。[§①]
商品子型（下列≥2命中→用商品 through-cycle 錶）：近5-7年≥1個GAAP虧損年｜peak-to-trough毛利率擺動>~20pp｜營收主由商品ASP驅動(price-taker)｜產業∈{記憶體/DRAM/NAND、礦業/材料/稀土、化工、航運、鋼鐵、太陽能、油氣E&P、部分晶圓/設備}｜capex/rev結構性>15%且ROIC高度擺動。未達≥2仍判循環→依驅動來源選capex建設循環錶或需求量循環錶。[§商品子型]

## 二、循環位置錶族（三選一，錨自身 through-cycle 區間非動能；位置落 深谷投降/早循環/中循環/晚循環/過熱頂部，多數決+sourced 裁決）
商品 through-cycle（MU 型，6 訊號）：P/B vs 自身區間(近1x/下緣=買，>中位2x/上緣=賣)｜量 vs 價(量增領先=買，ASP-only量平降=賣)｜GM vs自身區間(近谷/負=買，近峰=賣)｜供給紀律(減產=買，新產能洪水=賣)｜庫存(去化乾淨=買，通路+公司堆積=賣)｜情緒/部位(投降PT>價=買，狂熱PT<價=賣)。[§B.1商品]
capex 建設循環（ORCL 型，6 訊號）：capex/折舊比(低/正常化=買，遠高於1=賣)｜產能利用率爬坡(低基期回升=買，滿載見頂=賣)｜RPO(backlog)vs capex覆蓋(backlog領先=買，capex超前需求=賣)｜交易對手信用(客戶分散信用強=買，集中燒錢客戶=賣)｜情緒/部位(同上)｜量vs價(量增領先=買，ASP承壓量見頂=賣)。[§B.1capex]
需求量循環（EMS/ODM，JBL 型，5 訊號）：book-to-bill/需求量拐點(>1拐點向上=買，<1量見頂=賣)｜客戶庫存去化(去化乾淨=買，通路+客戶堆積=賣)｜倍數vs自身歷史re-rate均值回歸(近下緣=買，>5Y中位×1.5/貼峰=賣)｜終端·hyperscaler capex週期位置(早週期=買，晚週期見頂=賣)｜情緒/部位(同上)。[§B.1需求量]

## 三、交易姿態 + 反動能硬閘（跨子型通用，逐條檢查，觸發即 override 向保守）
位置→姿態：深谷投降→積極分批建立｜早→分批建立｜中→持有不加｜晚→分批了結｜頂→清光不碰。[§B.2]
閘1 位置=晚/頂→姿態不得為任何「建立」。閘2 成長=ASP-only+量持平/降→最多「持有」。閘3 P/B>自身中位2x→禁新建立。閘4 訊號矛盾→標「位置不明，觀望」不硬給姿態。閘5 TTM/Fwd本益比或EV倍數>自身歷史高區(>5Y中位×1.5、或貼/破歷史峰)→禁新建立。[§閘1-5]

## 四、落欄與 §13 row 8b 接線
`cycle_position`(深谷投降｜早循環｜中循環｜晚循環｜過熱頂部)＋`cycle_verdict`(右側可追蹤｜等回踩｜頂部觀望｜未觸發)；非循環 archetype 不填，整欄省略。[§落欄]
接 §13 row 8b：位置∈{深谷投降，早循環}+五閘全過+moat底線+獨立critic冷讀通過→落「進場・條件式(循環衛星)」(倉位上限3%)；任一不成立→只落研究提名，§13維持觀望。驗證失敗不得升級，只能降回觀望。`trade_stance`僅進HTML不入dd-meta。[§row8b]

## 五、雙制度與兩軌背離
有 secular sleeve + commodity sleeve → 循環鏡頭只套 commodity sleeve，secular sleeve 一句話另計(不隨循環賣)。[§⑤]
投資軌(§13長抱視角) vs 交易軌(本鏡頭位置)：底部背離(長抱視角迴避 + 循環位置深谷投降/早循環)是本鏡頭獨門訊號；頂部多收斂(皆遠離)。[§B.3]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260524","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"FCF margin 從 FY26 1.5% 改善至 FY28+ 4%+（working capital 正常化）","columns":{"2Y 驗證點":"FY26 H2 FCF $50M+","5Y 驗證點":"FY28 FCF $300M+（margin 5%）","10Y 驗證點":"FY30 FCF $400M+","具體門檻":"FY26 全年 FCF","來源":"公司 quarterly FCF 揭露","漂移觸發":"連 2 季 FCF margin"}},{"id":"H2","text":"Non-GAAP OpMargin 維持在 6%+ 並向 7% 進階","columns":{"2Y 驗證點":"FY26 全年 6.0-6.5%","5Y 驗證點":"FY28 6.5-7.0%","10Y 驗證點":"FY30 7.0%+","具體門檻":"連 2 季","來源":"quarterly earnings","漂移觸發":"連 2 季 Non-GAAP OpMargin"}},{"id":"H3","text":"healthcare/Life Sciences 段 YoY 維持 +12%+ 為 group 主成長引擎","columns":{"2Y 驗證點":"FY26-27 平均 +12%+","5Y 驗證點":"FY28-29 +10%+","10Y 驗證點":"FY30 +8%+","具體門檻":"連 2 季 YoY","來源":"segment quarterly disclosure","漂移觸發":"連 2 季 healthcare YoY"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"FCF margin 持續無法改善（working capital 結構性問題）","columns":{"時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 FCF margin","警戒閾值":"FY26 全年 FCF"}},{"id":"R2","text":"healthcare 段成長率 mean revert 至 mid-single-digit（COVID 後特殊週期結束）","columns":{"時間尺度":"🔥 中期","監測指標":"healthcare segment YoY","警戒閾值":"連 2 季"}},{"id":"R3","text":"EMS sector valuation mean reversion（CLS sentiment peak 退潮）","columns":{"時間尺度":"🐢 長期（2+ 年）","監測指標":"CLS / JBL / SANM Fwd PE 倍數","警戒閾值":"CLS Fwd PE 跌至"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":265.72,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
