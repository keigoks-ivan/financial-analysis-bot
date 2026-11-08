你是 stock-analyst **v20 判斷 agent**，標的 ARM（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ARM","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenue_gaap","label":"Total revenue (GAAP)","value":1443,"period":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","citation":"Arm 新聞稿 newsroom.arm.com/news/arm-q2-fye27-results；Exhibit 99.2 股東信"}},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":638,"period":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M（利益率 44.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","citation":"Arm 新聞稿；Exhibit 99.2 股東信"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":201,"period":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M（利益率 13.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","citation":"Arm 新聞稿；Exhibit 99.2 股東信"}},{"id":"f_kpi3_non_gaap_free_cash_flow","label":"Non-GAAP free cash flow","value":110,"period":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","citation":"Exhibit 99.2 股東信"}},{"id":"f_kpi5_guidance_q3_fye27","label":"Guidance Q3 FYE27","value":"營收 1.54bn ± 50M；non-GAAP 營業費用約 825M；non-GAAP EPS 0.56 ± 0.04","period":"Q2 FYE27 公告日 2026-11-04","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FYE27 公告日 2026-11-04","citation":"Exhibit 99.2 股東信"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_arm_gross_margin_pct","label":"ARM 毛利率","value":97.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_arm_operating_margin_pct","label":"ARM 營業利益率","value":17.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_arm_fcf_margin_pct","label":"ARM FCF 利潤率","value":21.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_snps_gross_margin_pct","label":"SNPS 毛利率","value":72.38,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_operating_margin_pct","label":"SNPS 營業利益率","value":11.03,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_fcf_margin_pct","label":"SNPS FCF 利潤率","value":29.18,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cdns_gross_margin_pct","label":"CDNS 毛利率","value":85.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cdns_operating_margin_pct","label":"CDNS 營業利益率","value":29.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cdns_fcf_margin_pct","label":"CDNS FCF 利潤率","value":28.65,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_qcom_gross_margin_pct","label":"QCOM 毛利率","value":53.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_qcom_operating_margin_pct","label":"QCOM 營業利益率","value":20.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_qcom_fcf_margin_pct","label":"QCOM FCF 利潤率","value":20.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_non_gaap","label":"SBC（含雇主稅）占 non-GAAP 營業利益","value":66.6,"period":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）","citation":"Exhibit 99.2 股東信：SBC 377＋雇主稅 48＝425（US$M）；425÷638 本表自算；占營收 29.5%"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":174.62,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-18.12,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":31.08,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.23 → 2.23）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.06 → 3.06）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.05 → 4.05）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.23,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.06,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":4.05,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 2.23 → 2.23（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":200.71,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝26.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":26.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":34.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝64.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":64.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":33.62,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝63.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":63.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":78.3,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 2.23，分子＝快照價 174.62","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-3121.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 500.0、現金 3621.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1070.0,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":183722.4,"period":"2026-11-08","unit":"USD m","basis":"市值 186843.4 ＋ 淨負債 -3121.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6092.14,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（39 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":8381.79,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（40 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":30.16,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 174.62 / W52 209.64 / W104 174.4 / W250 None / W250 13週斜率 None%"},{"id":"f_ma_w52","label":"52 週均線","value":209.64,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":174.4,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"20-F 自述：雲端運算市場中 Arm 架構晶片因 CSP 自研晶片與其他 CSP 採用授權客戶晶片而持續拿下份額。","source":"SEC EDGAR 20-F FY2026 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"Arm-based chips have been gaining market share as CSPs have started to deploy Arm products in their own in-house designed chips used in their data centers, and as other CSPs start to deploy chips designed by Arm licensees.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F 風險因子：x86 與免費開源 RISC-V 為競爭者，許多客戶同時是 RISC-V 支持者，客戶可能改用 RISC-V。","source":"SEC EDGAR 20-F FY2026 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"Many of our customers are also major supporters of the RISC-V architecture and related technologies. If RISC-V-related technology continues to be developed and market support for RISC-V increases, our customers may choose to utilize this free, open-source architecture instead of our products.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F 風險因子：多家客戶自建 AI 加速器，若工作負載由 CPU 移向加速器，CPU 市場規模與授權費／權利金可能下降。","source":"SEC EDGAR 20-F FY2026 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"Further, several of our customers are creating their own bespoke accelerators for artificial intelligence (“AI”) workloads that are intended to sit alongside the Arm core. If, over time, more of the workloads move to accelerators away from the CPU, the CPU market size may decrease, resulting in a decrease of our license fees and royalties.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F：Arm 自推 Arm AGI CPU 等量產矽產品，部分授權客戶將面臨與 Arm 直接競爭。","source":"SEC EDGAR 20-F FY2026 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"Furthermore, many of our customers who have historically licensed our IP may face direct competition from us in certain market segments, which could impact our existing commercial relationships. For example, some of our customers may face direct competition from us in silicon production products, such as with the Arm AGI CPU.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"TrendForce 預估 Arm 架構 CPU 2026 年占伺服器 CPU 出貨超過 20%、2027 年約 30%，AMD 2026 年約 27%。","source":"TrendForce Press Center","url":"https://www.trendforce.com/presscenter/news/20261022-13279.html","excerpt":"capacity at TSMC limiting AMD’s ability to accommodate additional orders, TrendForce estimates that the company’s share of the server CPU market will increase significantly to approximately 27% in 2026. In the Arm-based CPU segment, AWS continues to deploy its internally developed Graviton processors, while demand for NVIDIA’s Grace CPUs continues to expand.","as_of":"2026-10-22","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Mercury Research 認為即使 AGI CPU 賣到約 20 億美元，Arm 整體 CPU 市占仍處低個位數。","source":"Tom's Hardware","url":"https://www.tomshardware.com/pc-components/cpus/arms-usd2-billion-in-agi-cpu-sales-are-still-not-enough-to-penetrate-5-percent-of-overall-market-share-analyst-reveals-at-least-usd90-million-worth-of-cpus-to-be-shipped-before-fy2027","excerpt":"less than two months, the company attained around $2 billion in commitments for its AGI CPU over the next several years, smashing the company's expectations two-fold. But despite this heightened interest, Arm's market share will remain in the low single digits even if it manages to ship $2 billion worth of CPUs in two years, Mercury Research told Tom's Hardware.","as_of":"2026-05-11","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"20-F 風險因素：客戶可能授權 ISA 自行開發處理器而非採用 Arm 預開發產品；最大客戶 Arm China 占 FY2026 營收約 16%（FY2025 17%、FY2024 21%），前五大客戶占約 57%。","source":"SEC EDGAR 20-F FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"Customers may choose to develop their own processors if they believe they can do so more effectively than us or if supply and capacity constraints within the semiconductor industry further incentivize vertical integration in an effort to secure additional control over their supply chains.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"20-F：Arm 進入自有量產晶片（Arm AGI CPU）可能使傳統授權客戶視為利益衝突，客戶可能改用替代架構或自研架構。","source":"SEC EDGAR 20-F FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"As a result, these customers or partners may terminate or materially reduce their relationship with us, seek alternative architectures or products, develop their own proprietary architectures, withhold sensitive roadmap information, reduce collaboration on product development, challenge our pricing models or demand more favorable commercial terms, or pursue legal action.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"20-F：中國自給政策可能使陸系客戶自研 IP 或改用競爭對手技術。","source":"SEC EDGAR 20-F FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"PRC semiconductor companies and OEMs may increasingly develop their own technology and use such technology in their devices, or use our competitors’ technology in their devices.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"0","claim":"20-F：Arm 稱客戶並非獨家授權，部分客戶同時設計基於非 Arm 架構的處理器。","source":"SEC EDGAR 20-F FY2026 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"our partners and customers do not license our products exclusively; rather, several of our partners and customers also design, develop, manufacture and market processors based on non-Arm based architectures as well as develop their own Physical IP in-house.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026（截至2026-03-31）前五大客戶（含 Arm China、SoftBank）合計約占營收57%（FY25 56%、FY24 54%）；最大客戶 Arm China 約16%（FY25 17%、FY24 21%）；部分近期營收依賴與 SoftBank 的商業安排。","source":"SEC EDGAR 20-F FY2026 Item 3 風險因子","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"our top five customers (including Arm China and SoftBank Group) collectively accounted for approximately 57%, 56% and 54% of our total revenue for the fiscal years ended March 31, 2026, 2025 and 2024, respectively, and our largest customer individually, Arm China, accounted for approximately 16%, 17% and 21% of our total revenue, respectively, during those fiscal years.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 有三家客戶合計占營收42%（16%／14%／12%）；FY2025 為四家合計49%。應收帳款最大客戶占22%；信用損失歷年不重大。","source":"SEC EDGAR 20-F FY2026 Item 8 信用風險集中","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"For the fiscal year ended March 31, 2026, the Company had three customers that collectively represented 42% of total revenue, with the single largest customer accounting for 16% of total revenue, the second largest customer accounting for 14% of total revenue, and the third largest customer accounting for 12% of total revenue.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Qualcomm 為主要客戶，占 FY2026 營收9%，且與 Arm 有訴訟。","source":"SEC EDGAR 20-F FY2026 Item 3 風險因子","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"Qualcomm, which is currently a major customer of ours and accounted for 9% of our total revenue for the fiscal year ended March 31, 2026.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"S&P 2026-03 將 SoftBank 展望由穩定降為負面、維持 BB+，因加碼 OpenAI；Arm 持股為其評等支撐。","source":"pulse.bot Finance News: SoftBank's $30 Billion OpenAI Bet Spurs S&P Credit Outlook Cut","url":"https://www.pulse.bot/finance/news/softbanks-30-billion-openai-bet-spurs-sp-credit-outlook-cut-8f2dde86-c46f-42a6-8bc3-51e0e6901bfd","excerpt":null,"as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#4","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Barron's：SoftBank 持有 Arm 約90%，為設計授權業務基石客戶，9月當季占設計授權業務35%。","source":"Barron's: Arm Stock Is Falling. Its Biggest Customer Might Be Masking Larger Problems","url":"https://www.itiger.com/news/2603635316","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce 報導：Micron 評論顯示 2028 年的供給緩解可能不如預期；Samsung 與 SK hynix 下一波產能多自 2028 年起；SK hynix CEO 稱短缺可能延續至 2030（搜尋摘要轉述，未讀原頁）","source":"TrendForce News","url":"https://www.trendforce.com/news/?p=64868","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Astute Group：先進製程供給緊俏至少到 2027，晶圓供給受限直到後續新廠投產；封測緊張預期 2026 年底前緩解（搜尋摘要轉述）","source":"Astute Group, 05 May 2026","url":"https://www.astutegroup.com/?p=59281","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Arm 6-K（FY2026）稱預期長期半導體需求持續上升，但營收仍隨週期性晶片市場出貨量（版稅）波動（搜尋摘要轉述）","source":"SEC Form 6-K, Arm Holdings, period 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001973239/000197323926000142/arm-20260930.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Sherwood News 報導：Arm 對 AGI CPU 在 FY2027-2028 有逾 $2B 客戶需求能見度，高層稱尚未確保供給；TIKR 文則稱 CEO 提及逾 $20B 需求、僅確保首 $1B 製造，兩者數字衝突未核對","source":"Sherwood News / TIKR","url":"https://www.sherwood.news/markets/arm-holdings-q4-earnings-report-q1-guidance-cpu-data-center-ai-boom/","excerpt":null,"as_of":"2026-05-06","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"產業需求端：Gartner 稱記憶體有意義的價格緩解不早於 2027 年底；ASML 稱產能實質上 2027 年售罄且訂單延伸至 2028；JPMorgan 稱 2028 年初前無顯著新產能（二手彙整，來源為 Zacks 等文）","source":"Zacks, Will chip boom last through 2027","url":"https://www.zacks.com/stock/news/3012503/will-chip-boom-last-through-2027","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"風險面：中國記憶體產能擴張引發過剩疑慮；Deloitte 警告 2027-2028 可能與目前預期大幅偏離；Digitimes 稱若 AI 資本支出放緩可能出現庫存修正（二手摘要）","source":"Deloitte 2026 global semiconductor industry outlook (DQ India)","url":"https://www.dqindia.com/esdm/delloite-presents-2026-global-semiconductor-industry-outlook-11121381","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Intel CEO 稱記憶體短缺可能延續至 2028（次級站來源）","source":"excesschip.com","url":"https://www.excesschip.com/article/details/intel_warns_global_memory_chip_shortage_could_last_until_2028_amid_ai_boom","excerpt":null,"as_of":"2026-02-15","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"20-F 風險因子載明：Arm 受多司法管轄區反壟斷法規約束，過去曾遭反壟斷主管機關調查；Qualcomm 訴訟進行中，Qualcomm 占 FY2026 營收 9%。","source":"SEC EDGAR 20-F FY2026 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"Further, we are subject to antitrust laws and regulations in multiple jurisdictions, which could and has from time to time subjected us to investigations by antitrust regulators.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Bloomberg 報導 FTC 調查 Arm 授權行為是否試圖壟斷部分晶片市場，並要求 Arm 保存文件；Arm 否認反競爭指控，尚無正式指控。","source":"Bloomberg Law: Arm Is Said to Face US Antitrust Probe Over Chip Technology","url":"https://news.bloomberglaw.com/antitrust/arm-holdings-said-to-face-us-antitrust-probe-over-chip-tech","excerpt":"investigation by the US Federal Trade Commission over the UK company’s licensing of its semiconductor technology, part of ongoing global scrutiny of the business, people familiar with the matter said. The US competition and consumer protection regulator is probing whether Arm is trying to illegally monopolize parts of the semiconductor market, according to the people, who were granted","as_of":"2026-05-15","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Arm 20-F：Neoverse V 系列效能達美英出口管制門檻，對中國出貨需出口許可，且難取得；公司改授權未超門檻的其他 CPU 核心以滿足客戶需求。","source":"SEC EDGAR 20-F FY2026 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"For example, our Neoverse V series processors meet or exceed performance thresholds under U.S. and U.K. export control regimes and thereby trigger U.S. and U.K. export license requirements prior to export and delivery to customers in the PRC.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"20-F：2025 年美國發布先進運算晶片、HBM、GAAFET 等出口管制規則並增列實體清單；公司稱不太可能取得部分高效能 Neoverse 核心的美英出口許可，可能降低營收並使產品路線圖不確定。","source":"SEC EDGAR 20-F FY2026 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"it is unlikely that we would be able to obtain a U.S. or U.K. export license for certain high performance compute cores in the Neoverse series processor family. This and any similar limitations could also reduce our revenues and cause significant uncertainty in our products roadmap","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"20-F：2026-02-20 最高法院推翻部分 IEEPA 關稅；2025 年關稅曾對半導體與電子等策略產業給予豁免；Section 232 半導體調查於 2026-01-15 起對 NVIDIA H200、AMD MI325X 課關稅；2026 年啟動 Section 301 半導體調查。","source":"SEC EDGAR 20-F FY2026 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"The investigation resulted in an announcement of tariffs, effective January 15, 2026, applicable to NVIDIA H200 and AMD MI325X chips and systems incorporating such chips.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Arm FY2026 20-F 稱進入量產晶片使其依賴第三方晶圓代工與委外製造商，供應鏈中斷可能對業務造成重大不利影響，另提及記憶體與封裝供應商依賴。","source":"Arm Holdings Form 20-F FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001973239/000197323926000097/arm-20260331.htm","excerpt":null,"as_of":"2026-05-20","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Arm 3nm 資料中心 CPU 由台積電代工，並稱僅取得首批約 10 億美元需求的產能；多家券商點出台積電先進製程晶圓供給為近期瓶頸（二手報導）。","source":"City AM, Arm's AI ambitions hit supply chain reality despite record revenues","url":"https://www.cityam.com/?p=2422458","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國約占 Arm 營收 18%（FY2026 摘要），經由 Arm China（Arm 不控制營運）；IPO 文件稱 Arm China 為最大客戶；出口管制限制中國成長。","source":"SCMP / Panabee Arm Q1 2026 summary","url":"https://www.scmp.com/tech/big-tech/article/3232051/softbank-backed-arm-warns-significant-china-risk-mentioning-country-350-times-its-ipo-prospectus","excerpt":null,"as_of":"2023-09-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"FQ2 FY27（2026-11-04 公布）營收約 $1.443B、年增 27%；授權及其他 $773M 年增 50%（含 SoftBank 技術授權 $209M）；權利金 $670M 僅年增 8%；資料中心權利金年增約一倍，edge AI 權利金大致持平，記憶體漲價壓抑手機出貨；下季營收指引 $1.54B±$50M。","source":"搜尋摘要彙整（cryptobriefing／finviz／valueaddvc／xenospectrum 等，Arm FQ2 FY27 報導）","url":"https://valueaddvc.com/pulse/arm-q2-revenue-1-44b-27pct-data-center-royalties-2026","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FQ3 FY26（2025-12 季）權利金年增 27% 至 $737M，授權 $505M 年增 25%；FQ4 FY26 指引權利金低十位數成長、授權高十位數成長。","source":"SEC 6-K FY2026 Q3 exhibit 99.2／Quartr","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000005/exhibit992fye26q331-decx25.htm","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"資料中心：管理層稱資料中心業務數年內將大於行動業務；Morningstar 稱手機份額約 99%、手機約占營收 40–45%，手機成長主要靠權利金費率上調（CSS 轉換）；Mercury Research 估 Arm 伺服器 CPU 出貨份額 13.6%（Q2 2026），Arm 自稱頂級超大規模業者份額將達 50%。","source":"Morningstar「Arm Earnings: Data Centers Becoming Increasingly Important for the Growth Story」；Arm FQ3 FY26 法說逐字稿（finviz）","url":"https://global.morningstar.com/en-gb/stocks/arm-earnings-data-centers-becoming-increasingly-important-growth-story","excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"WSTS 2026 年春季預測：全球半導體 2026 年成長 89.9% 至 $1.51 兆，2027 年再成長 27% 至約 $1.9 兆；記憶體 2026 年 $803.9B，為主要驅動。","source":"WSTS Spring 2026 forecast release／TelecomLead","url":"https://telecomlead.com/semiconductor/wsts-raises-semiconductor-forecast-market-to-reach-1-51-trillion-in-2026-grow-to-1-9-trillion-in-2027-126102?noamp=mobile","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"FQ2 FY27 權利金 +8%、資料中心權利金翻倍、edge AI 持平","source":"xenospectrum","url":"https://xenospectrum.com/en/arm-q2-fye27-license-royalty/","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Arm 20-F 列明競爭來自 x86 與免費開源的 RISC-V，且部分客戶同時是 RISC-V 的主要支持者。","source":"SEC EDGAR 20-F FY2026 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"We face significant competition from established technologies such as the x86 architecture, as well as from free, open-source technologies, including the RISC-V architecture. Some of our customers are also major supporters of the RISC-V architecture and related technologies.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Arm 20-F 風險因素：客戶無義務獨家使用 Arm 產品，部分客戶已用含自家設計在內的競爭技術，且多數安排無最低採購義務。","source":"SEC EDGAR 20-F FY2026 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"However, our customers are not contractually obligated to design, manufacture, sell or deploy chips using our products on an exclusive basis or at all. Some of our existing customers design, manufacture, sell and deploy chips based on competing technology, including their own, and other existing or potential customers may do so in the future.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"SHD Group 估 RISC-V 晶片 2024 年市場 520 億美元、滲透率 10.4%，2030 年可能超過 2600 億美元。","source":"Simply Wall St 轉述 SHD Group","url":"https://simplywall.st/stocks/us/semiconductors/nasdaq-arm/arm-holdings/news/is-rising-competition-from-risc-v-challenging-the-investment/amp","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Arm 於 2026 年 3 月起商業模式由純 IP 授權擴展到自家設計的矽產品（Arm AGI CPU），預計 2026 年底前量產。","source":"SEC EDGAR 20-F FY2026, Item 4","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"As of March 2026, we also expanded our offerings to include Arm-designed silicon products with the introduction of the Arm AGI CPU, with production expected by the end of calendar year 2026.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"Arm 自有晶片與授權客戶（AWS、Google、Microsoft、NVIDIA 等）存在通路衝突疑慮；Meta 為首發客戶。","source":"eWeek: Arm Enters the AI Chip Market With New AGI Processor","url":"https://www.eweek.com/news/arm-agi-cpu-ai-chip-market-entry/","excerpt":"Meta Platforms is Arm’s first official customer for the AGI CPU, with early customers including OpenAI, Cloudflare, SAP, SK Telecom, and Cerebras.","as_of":"2026-03-25","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Tickflow 彙整（資料截至 2026-08-01）：47 位分析師共識 Buy，平均目標價 $271；StockAnalysis 列區間低 $125、高 $500、平均 $257.3；各聚合站平均目標價 $213～$272 不一，as-of 不同。","source":"Tickflow ARM forecast / StockAnalysis ARM forecast","url":"https://tickflow.io/stock/ARM/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill：FY2027 EPS 共識 2.25 美元（2026-10-17、44 位分析師）；下季（FQ2 2027，預計 11/5 公布）EPS 預估 0.48、營收 13.89 億；近 3 個月下季營收預估上修約 2.66%、FY2027 EPS 上修約 2.13%。","source":"Chartmill ARM estimates","url":"https://www.chartmill.com/stock/quote/ARM/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 指引頁：公司最近一次指引為 2026-07-29，營收 $1.33B～$1.43B，自前一區間上調；頁面表格內部不一致，季別待核。","source":"Benzinga ARM guidance / earnings-forecasts","url":"https://www.benzinga.com/quote/ARM/earnings-forecasts","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-02 第三季財報：FY2026 成長指引由至少 20% 上修至約 22%；FY2027 無正式全年指引，管理層稱維持 20% 成長「合理」；2026-03 CFO 重申第四季指引。","source":"SEC Form 6-K 2026-03-24 / Benzinga","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000052/arm-20260324.htm","excerpt":null,"as_of":"2026-03-24","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 2026-05-28：目標價上調至 $360（單一券商），共識 Moderate Buy、平均目標價 $213.17。","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/arm-nasdaqarm-price-target-raised-to-36000-2026-05-28/","excerpt":null,"as_of":"2026-05-28","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"TIKR：Street 平均目標價 $245 低於當時股價，ARM 2026 年內大漲約 240%。","source":"TIKR","url":"https://www.tikr.com/blog/arm-stock-is-up-240-in-2026-but-the-street-mean-target-sits-38-below-today","excerpt":"ARM Stock Is Up 240% in 2026 but the Street Mean Target Sits 38% Below Today Gian Estrada • 10 minute read Reviewed by: David Hanson Last updated Jun 5, 2026 TIKR Key Stats for Arm Stock 52-Week Range: $100 to $428 Current Price: $393 Street Mean Target: $245","as_of":"2026-06-05","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Arm 於 2026-07-01 以約 2.65 億美元現金完成收購 DreamBig Semiconductor 100% 股權（2025-10 簽約）。","source":"SEC EDGAR 6-K（季度財務資料）","url":"https://www.sec.gov/Archives/edgar/data/0001973239/000197323926000114/arm-20260630.htm","excerpt":"On July 1, 2026, the Company completed the acquisition of DreamBig, acquiring 100% of the outstanding equity interests of DreamBig in an all-cash transaction for approximately $ 265.0million.","as_of":"2026-07-29","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"Arm 與 Qualcomm/Nuvia 訴訟仍在進行，預計 2026 年第四季開庭；Qualcomm 於 2026-03-30 提出修正訴狀新增一項違約主張。","source":"SEC EDGAR 20-F FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"The case is expected to go to trial in the fourth calendar quarter of 2026.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026-05-15 Bloomberg 報導 FTC 調查 Arm 是否試圖非法壟斷部分半導體市場，股價當日跌 8.5% 至 209.16 美元；多家原告律所隨後宣布證券詐欺調查（非已提起之集體訴訟）。","source":"Business Wire：Law Offices of Frank R. Cruz 公告","url":"https://www.businesswire.com/news/home/20260518851582/en/Securities-Fraud-Investigation-Into-Arm-Holdings-plc-ARM-Announced-%E2%80%93-Shareholders-Who-Lost-Money-Urged-To-Contact-The-Law-Offices-of-Frank-R.-Cruz/","excerpt":null,"as_of":"2026-05-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Arm 於 2026-07-01 以約 2.65 億美元現金完成收購 DreamBig Semiconductor。","source":"SEC EDGAR 6-K（季度財務資料）","url":"https://www.sec.gov/Archives/edgar/data/0001973239/000197323926000114/arm-20260630.htm","excerpt":"On July 1, 2026, the Company completed the acquisition of DreamBig, acquiring 100% of the outstanding equity interests of DreamBig in an all-cash transaction for approximately $ 265.0million.","as_of":"2026-07-29","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Qualcomm/Nuvia 訴訟進行中，預計 2026 Q4 開庭。","source":"SEC EDGAR 20-F FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm","excerpt":"The case is expected to go to trial in the fourth calendar quarter of 2026.","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-05 起多家原告律所宣布證券詐欺調查（因 FTC 調查報導後股價跌 8.5%），搜尋結果未見已提起之集體訴訟。","source":"Business Wire：Law Offices of Frank R. Cruz 公告","url":"https://www.businesswire.com/news/home/20260518851582/en/Securities-Fraud-Investigation-Into-Arm-Holdings-plc-ARM-Announced-%E2%80%93-Shareholders-Who-Lost-Money-Urged-To-Contact-The-Law-Offices-of-Frank-R.-Cruz/","excerpt":null,"as_of":"2026-05-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ARM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":97.44,"operating_margin_pct":17.02,"fcf_margin_pct":21.5,"rd_intensity_pct":57.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"SNPS","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.38,"operating_margin_pct":11.03,"fcf_margin_pct":29.18,"rd_intensity_pct":30.6},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"CDNS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":85.68,"operating_margin_pct":29.64,"fcf_margin_pct":28.65,"rd_intensity_pct":33.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"QCOM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.1,"operating_margin_pct":20.08,"fcf_margin_pct":20.06,"rd_intensity_pct":23.67},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"ARM"},"financial_history":{"ticker":"ARM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-03-31","revenue":2679000000.0,"revenue_yoy_pct":null,"gross_margin_pct":96.04,"operating_margin_pct":25.31,"net_income":524000000.0,"diluted_eps":0.510694,"free_cash_flow":646000000.0,"fcf_margin_pct":24.11,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-03-31","revenue":3233000000.0,"revenue_yoy_pct":20.68,"gross_margin_pct":95.24,"operating_margin_pct":3.62,"net_income":306000000.0,"diluted_eps":0.29,"free_cash_flow":947000000.0,"fcf_margin_pct":29.29,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-03-31","revenue":4007000000.0,"revenue_yoy_pct":23.94,"gross_margin_pct":96.98,"operating_margin_pct":20.74,"net_income":792000000.0,"diluted_eps":0.75,"free_cash_flow":158000000.0,"fcf_margin_pct":3.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-03-31","revenue":4920000000.0,"revenue_yoy_pct":22.79,"gross_margin_pct":97.54,"operating_margin_pct":18.46,"net_income":904000000.0,"diluted_eps":0.85,"free_cash_flow":949000000.0,"fcf_margin_pct":19.29,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ARM/ARM_Q2_2027_Earnings_Call_20261104.md）

# Q2 2027 Earnings Call
**Arm Holdings plc** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to the ARM's Second Quarter Fiscal Year 2027 Webcast and Conference Call. [Operator Instructions] Please be advised that today's conference is being recorded. 
I would now like to hand the conference over to your first speaker today, Ian Thornton, Vice President of Investor Relations. Please go ahead.

**Ian Thornton** (Executives):
Thank you very much, and welcome to our second quarter fiscal '27 earnings call. On the call are Rene Haas, Arm's Chief Executive Officer; and Jason Child, Arm's Chief Financial Officer. 
Today's call contains forward-looking information about the company and its financial results. While these statements represent our best current judgment, our business is subjected to many risks and uncertainties that could cause actual results to differ materially. Important risk factors that may affect our business and future financial results are described in our annual report on Form 20-F filed with the SEC. Arm assumes no obligation to update any forward-looking statements. 
We will also refer to non-GAAP financial measures. Reconciliations of these non-GAAP financial measures to the most directly comparable GAAP measures can be found in our shareholder letter as can the discussion of certain projected non-GAAP financial measures that we're not able to reconcile without unreasonable efforts and supplemental financial information. Our earnings materials are available at investors.arm.com. 
And with that, I'll turn the call over to Rene.

**Rene Haas** (Executives):
Thank you, Ian, and good afternoon, everyone. Arm delivered a record second quarter. Revenue reached $1.44 billion, up 27% year-over-year, marking our fifth straight quarter of growth above 20%. License and other revenue grew 50% to $773 million, driven by our partners increasing their investment in the Arm compute platform. This strong licensing momentum is an important leading indicator of future royalties, which we expect to accelerate as these new designs enter production. 
Second quarter royalty revenue grew 8% to $670 million, with data center royalties doubling year-over-year. And non-GAAP earnings per share increased 33% to $0.52, while we continue to increase our investment in R&D. AI is driving unprecedented demand for compute across the cloud, devices and autonomous systems, with Arm being the compute platform of choice. 
Today, our business is now driven by 2 rapidly growing areas: the IP business, where partners are increasing investment in the Arm compute platform and deploying record numbers of Arm-based chips and our new silicon business, where demand for the Arm AGI CPU is extremely strong, both leverage the same Arm compute platform and software ecosystem. We are seeing these 2 growth vectors play out clearly in the data center, where our partners are expanding their deployment of Arm-based infrastructure alongside strong demand for Arm-designed silicon. 
Oracle Cloud Infrastructure, OCI, is a key example of how these 2 businesses reinforce one another. Today, OCI offers NVIDIA Vera CPUs built on Arm, and in addition, plans to offer Arm AGI CPU instances in 2027. Since launching the Arm AGI CPU in March, customer demand has continued to strengthen. We have secured purchase orders from multiple customers extending through calendar 2027 and first commercial deliveries remain on track for fiscal Q4 '27. Our confidence in achieving up to $2 billion of revenue in Arm AGI CPU across fiscal 2027 and 2028 has increased over the last 90 days, supported by additional supply and customer mix. 
We remain focused on expanding capacity to meet growing customer demand. Power availability makes performance and efficiency even more important. Morgan Stanley projects a 38 gigawatt global data center power shortfall through 2028. Arm is helping customers address this constraint by delivering more useful compute from the power already available. At OCP, independent testing by Signal65 showed the Arm AGI CPU delivering approximately twice the performance per rack versus the AMD EPYC 9755. This type of improvement could reduce the projected global power shortfall by half. 
Our data center royalties doubled year-over-year, and Arm-based server market share at the top hyperscalers has more than tripled from 15% in calendar 2024 to more than 50% in calendar 2025. Based upon expected ramps across Google Axion, AWS Graviton, Microsoft Cobalt and NVIDIA platforms, we now expect that share to exceed 60% by the end of calendar 2026. Beyond the data center, Arm's role in edge AI increases as AI agents become more capable and persistent. 
Arm-based PCs have now reached 20% of global shipments. Google recently announced Googlebook, a new category of AI-native laptops built for Gemini Intelligence with Arm serving as the primary compute platform for many models. NVIDIA's RTX Spark systems, which are now available, further expand Arm into local AI, content creation and gaming. In smartphones, Arm recently announced CSS for Mobile 2, which improves the performance of agentic AI workloads by up to 70% through SME2. 
Our first AI-native Mali GPU delivers up to 4x the frame rate at the same sustained power. These capabilities allow more AI and richer experiences to run directly on the device without compromising battery life. Arm is the platform of choice for physical AI. Royalty revenue grew 50% year-over-year, driven by advanced driver assistance and in-vehicle infotainment. We also launched Arm Total Design for physical AI, bringing together more than 80 companies to accelerate the development and deployment of complete physical AI systems. 
For the first time, our partners reported more than 10 billion Arm-based chips shipped in a single quarter, an increase of 1.5 billion year-on-year, supported by a software ecosystem of more than 30 million developers. Demand for Arm technology has never been stronger as AI is driving more complex designs and greater demand for power-efficient compute. Our IP business generates licensing revenue as those designs begin and royalties as they enter production. And now Arm AGI CPU as a new direct silicon business built on the same compute platform and software ecosystem. That gives Arm 2 powerful growth engines, which we expect to accelerate revenue at a faster pace in the future. 
And with that, I'll turn it over to Jason.

**Jason Child** (Executives):
Thank you, Rene. We delivered another strong quarter with total revenue growing 27% year-on-year to $1.44 billion. This was a record for our second quarter and our second highest quarterly revenue ever, reflecting continued strength in our business. License and other revenue was $773 million, up 50% year-on-year, also a record for the second quarter and our second highest quarter ever. License revenue was around $100 million higher than we had anticipated due to an acceleration of interest from customers wanting to sign long-term commitments to access Arm technology. 
During the quarter, we signed 3 new Arm Total Access agreements, bringing the number -- total number of active ATA subscriptions to more than 60. This included one of our major customers signing their first ATA license. We also signed 4 additional compute subsystem licenses, 2 for data center chips and 2 for smartphones. For established customers, these agreements broaden and deepen access to our future technology road map and provide an important foundation for Arm's future royalty growth. 
In addition, we are seeing ATA and CSS as a way for newer customers who have previously made only limited use of Arm technology to accelerate their adoption with several signing ATA or CSS licenses during the quarter. Of the $773 million in license revenue, our agreement with SoftBank for technology licensing and design services contributed $209 million, up 17% year-on-year. 
We expect the quarterly run rate for the rest of the year to remain around this level. Annualized contract value grew 12% year-on-year. As we have discussed before, license revenue can vary significantly from quarter-to-quarter based on the timing and accounting treatment of large agreements. So ACV remains a useful measure of the underlying licensing trend. 
Turning now to royalty. Royalty revenue was $670 million, up 8% year-on-year, also our highest ever figure for Q2. Cloud AI remained the largest growth driver. Once again, data center royalty doubled year-on-year as Arm-based CPUs ramp across AI infrastructure and general-purpose cloud workloads. Physical AI royalty revenue grew 50% year-on-year, driven by increasing adoption of Arm technology in automotive and robotics. 
In edge AI, royalty revenue was roughly flat year-on-year. Higher memory prices continue to pressure smartphone unit sales, particularly in the mid- and lower-tier segments. That headwind was offset by the benefit we continue to see from higher royalty rates as our latest Armv9 and CSS technologies are adopted. As smartphone market conditions normalize, we expect edge AI royalty revenue to reaccelerate. As Rene discussed, customer demand for the Arm AGI CPU remains very strong. 
Last quarter, we said that we increased confidence -- we had increased confidence in achieving more than $1 billion across fiscal year '27 and '28. In the past 90 days, we have signed purchase orders from multiple customers and signed supply agreements with companies in our supply chain, giving us increased confidence in achieving up to $2 billion across fiscal '27 and '28. We will provide another update at our Q3 results, which is when we'll have better visibility. 
Turning to operating expenses and profits. Non-GAAP operating expense was $774 million, up 19% year-on-year as we continue to expand our engineering capacity and invest in next-generation platforms, compute subsystems and our Arm AGI CPU product family. Non-GAAP operating income was $638 million, up 37% year-on-year. Non-GAAP operating margin was 44.2%, up 300 basis points from a year ago as revenue outpaced operating expense growth. Non-GAAP EPS was $0.52, up 33% year-on-year. Importantly, even at these elevated levels of investment, we generate free cash flow of $1.1 billion over the trailing 12 months, giving us the flexibility to continue to invest for long-term growth. 
Turning now to guidance. For Q3, we expect revenue of $1.54 billion, plus or minus $50 million. At the midpoint, this represents growth of approximately 24% year-on-year. We expect continued strong growth in license and other revenue, up a little over 50% year-on-year, supported by strong customer demand and our visibility into the licensing pipeline. In royalties, we expect continued strength in cloud AI and physical AI, offset by ongoing pressure in edge AI from weaker smartphone demand, and we have a tough year-on-year comp. 
As a result, we expect royalty revenue to grow low teens sequentially and low single digits year-on-year. We expect non-GAAP operating expenses of approximately $825 million and non-GAAP EPS of $0.56, plus or minus $0.04. Looking further ahead, we continue to see strong customer demand across our business. Combined with the expansion of our technology portfolio and deepening strategic customer relationships, this gives us confidence in our long-term growth outlook. 
With that, I'll turn the call back to the operator for Q&A.

**Operator** (Operator):
[Operator Instructions] And your first question today comes from the line of Gary Mobley from StoneX Group.

**Gary Mobley** (Analysts):
I think on the top of the mind for everybody is Arm AGI CPU, and you're obviously signaling something closer to $2 billion in revenue over the 5-quarter period up to the end of fiscal year '28. So I'm wondering what's driving your confidence in that with respect to securing more supply with your different partners? And I would assume most of the revenue initially goes to supporting Meta, but maybe if you can talk about whether or not you've signed and committed contractually with additional customers?

**Rene Haas** (Executives):
Yes. Thanks, Gary. I'll take that question, and Jason can add if I've missed anything. Each one of the quarters, as we talk about the ramp of the product, we've been careful to make sure that we manage the expectations of supply and demand. I think there's no secret that in general, demand is incredibly strong for the Arm AGI CPU, really driven by everything we see with agentic workloads and the CPU being central to that. 
Demand is stronger today than we talked about when we did the Arm Everywhere event in March. And subsequently, demand for multiple customers, Meta being the chief customer has also been beyond what we've expected. That being said, we've been working very hard over the last few quarters on securing what's necessary in the supply chain to address that demand. There's multiple components to it. There is wafer supply, there are substrates, there are testers, there's memory, et cetera. We have wanted to be confident when we signal our ability to achieve this extra demand with supply in the ongoing quarters. 
So at Arm Everywhere Day, we talked about visibility of $1 billion. And quickly, we have seen that to about a $2 billion number. I can tell you today that the confidence is the strongest it's been to date, and it's definitely stronger than it was 90 days ago in terms of securing that supply. And as I said, it's across all of those independent areas. But we didn't start working on it yesterday or the previous quarter. We've been working on it actually for the last number of quarters. We've got great partners who are supporting us here. And as you mentioned, Meta is a chief customer, but there will be multiple customers beyond Meta. 
Jason, I don't know if there's anything you want to add. So if not, thanks, Gary, for the question.

**Gary Mobley** (Analysts):
If I could ask...

**Operator** (Operator):
Please continue, Gary.

**Gary Mobley** (Analysts):
My apologies. I was just hoping to ask a follow-up question briefly. You've given us enough information in the shareholder letter to calculate your royalty rate per unit on a year-over-year basis, and it looks like it's trending up at least mid-single-digit percent. So I'm wondering if that's just sort of an anomaly with respect to mix or if that should be how we view the royalty rate per unit growth over the long term?

**Jason Child** (Executives):
Yes. It's -- I mean, it's mix, but it's also, I think we said, what, 10 billion chips shipped in the quarter. And so it's going to bounce around based on any particular quarter. I would say, certainly, mobile on average is probably a little lower than certainly server and physical AI given the size and value of the chips. And so that probably had some impact. So I don't know that I would take the overall average across 10 billion chips and use that as the best way to forecast going forward. 
I do think if you break it out by the 3 different business units, as we said, pretty flattish growth in the mobile business, very strong double-digit growth in server, where we're also seeing increasing core counts and more CSS revenue flowing through this quarter, but we're going to continue seeing that going forward. That's why we have high confidence that we're going to have triple-digit growth for the next few years. 
And then on physical AI, that one is also -- we said growing 50% year-on-year. That's also going to, I'd say, be a bit of a tailwind to overall royalty rates and overall royalty growth. But again, I would probably break it into those 3 categories as opposed to just looking at it all combined together.

**Rene Haas** (Executives):
Yes. Maybe, Gary, just a finer point on the data center growth. I think there's 2 vectors independent of the Arm AGI CPU on the royalty. One is Arm taking market share, which I mentioned before. Now we think it's going to be 60% by the end of the year. That market share gain is driven both in terms of units going up at agentic AI driving increased design starts for Graviton, Cobalt, Axion, et cetera. 
But in addition, we are seeing a transition away from x86 to Arm for the head node CPU that connect to accelerators. We already know about Vera Rubin, but Google has already announced the conversion of x86 to Axion connecting to TPU version 8. So to Jason's point, this is why we have a high degree of confidence on data center royalties growing triple digits over the next number of years.

**Operator** (Operator):
[Operator Instructions] And our next question comes from the line of Sebastien Naji from William Blair.

**Sebastien Cyrus Naji** (Analysts):
I want to ask about how Arm wins versus x86 in the AI data center. At OCP, you introduced agentic AI benchmarks that showed your AGI CPU can deliver twice the performance per rack versus a competing x86 solution. But then last night on its earnings call, AMD said that its Venice CPU offers the best performance per watt. So maybe, Rene, could you talk about where you see the most meaningful opportunity for the Arm CPU to win in the data center versus x86?

**Rene Haas** (Executives):
Yes. Sure. I'll take the question kind of from 2 angles. One is looking at it in the eyes of a Amazon or Google or Microsoft who are building custom CPUs for their own implementations and their own racks and their own systems. In those designs, particularly when an end customer is designing an SoC, the degree and flexibility that they have to innovate around their own system is extremely high. Trade-offs that they can make in terms of what goes inside the SoC for data movement versus what takes place inside of DPU, which is what takes place inside of storage. 
At that level, you almost have to look at it in terms of performance per rack versus the chip basis. But at a chip level, Arm not only gives them the most efficient core on the planet, but allows them to design the most efficient SoC and subsequently, the ultimate system. So -- and we've seen that just in terms of how quickly these customers have been converting designs away from standard x86 to Arm. Now the Arm AGI CPU benchmark that we ran, that was done through  Signal65 at OCP, was looking at the previous generation to Venice. And we are very confident in those numbers, and we're very, very confident in terms of the choices that customers make vis-a-vis head-to-head against that design. 
Venice is a great product, but we're very confident in terms of the demand we have for our product, Arm AGI CPU, and the road map going forward. But I would say 2 vectors to look at it. One is just efficiency, cost per -- performance per dollar and performance per watt with AGI CPU. And then on the custom level, there are just simply things that end customers can do that a standard product is never going to be able to touch. And that's kind of the beauty of our business model.

**Operator** (Operator):
Our next question today comes from the line of Krish Sankar from TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
Rene or Jason, at OCP, you introduced your AGI CPU reference server design. I'm just wondering, are you working with ODMs or server manufacturers? Are you targeting the enterprise private cloud? And along the same path on FY '31, $15 billion in AGI CPU revenues, which is the biggest factor? Is it core count increase? Or is it ASP increasing from the current version 1?

**Rene Haas** (Executives):
Yes. No, thank you for the question. When I think about the partners that we're working with, it's Supermicro, Lenovo and ASRock. They are building the racks for us, and then are basically standing those up for deployment at data centers such as OCI. So they are the partners that we build with. As far as the revenue outlook, and Jason can speak to the specifics of where we think and when we think those numbers are going to land. There is clearly going to be an acceleration of number of cores inside these SoCs. 
And that is largely driven by agentic workloads and specifically the fact that each one of these agents, when you think of Muse agent that's running a specific job, typically runs as a virtual machine on one CPU core. The software is rather complex to manage that across a single core or multiple cores, if you will. So if you can run that on a single core, it's a better thing. So do I see CPUs going from 128 cores to 256 cores to 500-plus cores? Absolutely. You can imagine that the average selling price of the chips with more cores will be higher, certainly. But I think what we will see is probably a more rapid acceleration to that, which will help grow the top line. 
And Jason, anything you want to add on to that numbers-wise?

**Jason Child** (Executives):
Yes. No, I mean, we said back at the Arm Everywhere event last March that we had the line of sight to $1 billion for this kind of end of '27 and fiscal '28. And of course, now we're increasing our confidence to deliver $2 billion. And then the following year, we haven't made any updates, but I think the original plan was that we were going to get to about $2 billion a year after that, and then we're going to go up to about $5 billion a year after that. And so to the extent that we're successful in delivering over $2 billion, you should expect that we'll probably have some upsides after that. 
That's something that we'll plan on providing in terms of updated possible targets when we have the next Arm Everywhere event. We're still working on timing, but likely probably in, say, spring or first half of next year is probably when we'll provide that update.

**Rene Haas** (Executives):
Yes. I think what we can say is when we did the Arm Everywhere Day in March, the conventional wisdom was the market was a $60 billion market and wasn't going to be growing all that much. When we did our calculations, we felt differently, and we talked about a number that day of $100 billion by 2030. I think that number has been increased by various folks. I think Lisa may have even said $200 billion or more. I think that's about right and maybe even could be undercalling it, who knows? 
What is obvious is that the agentic demands on AI jobs are CPU bound. And the more agentic workloads that run, that's going to need more CPUs. So I think that's what's going to end up driving these higher core count devices, which I think is very -- will be very good for us because what's going to matter there is performance per watt at the core level, having the most efficient core on the planet, which is what we're very good at.

**Operator** (Operator):
Your next question today comes from the line of Mehdi Hosseini from Susquehanna.

**Mehdi Hosseini** (Analysts):
Yes. Two follow-ups. Going back to the new updated AGI silicon revenue target of $2 billion, should we assume any revenue contribution in September or December quarter of this year? FY '27?

**Jason Child** (Executives):
Assume that our shipments will start in Q4. If we have something in Q3, we'll let you know. It wouldn't be a lot. We're really targeting Q4.

**Mehdi Hosseini** (Analysts):
Okay. And then just a quick follow-up. Would it be fair to say that data center mix of the royalty revenue is tracking to 1/3 or 30% to 35%? And for next fiscal year, FY '28, it could go up towards mid-40%?

**Rene Haas** (Executives):
I'm sorry, the -- are you asking...

**Jason Child** (Executives):
Mix of total royalties?

**Rene Haas** (Executives):
Percentage of total royalties that are data center. Is that the question?

**Mehdi Hosseini** (Analysts):
Yes. Would it be fair to assume that it's tracking to like 1/3 in FY '27 and it would step up again in '28, moving towards 45%?

**Jason Child** (Executives):
Yes. I don't -- yes, I mean, we look at them independently. So I would assume that royalties for edge are going to be pretty flattish this quarter. And I think we said we'll start to see some recovery in Q4. But if you have that in the kind of high single digits and then you have data center growing at double digits. I think we said last year, we were kind of approaching 20-ish percent of total royalties. 
And then you have physical AI growing somewhere probably in the -- somewhere between 20%, 30-ish percent range, then that's how you should build your model. I haven't done the math to look at the percentage. I don't think data center will get quite to 1/3, but it will sometime soon. I just don't know if it's going to get there by the end of this year.

**Operator** (Operator):
Your next question comes from the line of Simon Leopold from Raymond James.

**Simon Leopold** (Analysts):
I wanted to ask about the -- basically the cloud and AI group of products and how you might frame the customer concentration there to help us give us a better appreciation? For example, could we guess that maybe 60% of these royalties are coming from 3 customers? Any kind of quantification would be helpful to understand that.

**Rene Haas** (Executives):
I think we can say, and Jason, chime in on this thing, Amazon, Google and Microsoft are the largest contributors, and then you've now got NVIDIA ramping up quickly. They are the 4 guys inside the data center that command the majority of the royalties.

**Operator** (Operator):
Our next question today comes from the line of Harlan Sur from JPMorgan.

**Harlan Sur** (Analysts):
With the strong success of your first-generation AGI CPU, I'm sure your customers are already looking towards your next-generation platform, right? Can you just give us an update on second-gen AGI? I think the plan was for the team to tape out either end of this year, beginning of next year for ramp in calendar '28. And then maybe just as importantly, as you continue to add more capabilities to your compute silicon portfolio, does it actually make sense to add more networking and high-performance I/O capabilities as well? 
More and more, we're seeing that compute and networking are very closely coupled to determine very good systems performance. So does the team -- is the team going to add more networking and capabilities to the portfolio?

**Rene Haas** (Executives):
Yes. Thank you, Harlan. Those are great questions. Without disclosing the precise schedule on the follow-on chip, you can think about this market goes at about an 18- to 24-month cadence in terms of production ramps. So as we are ramping into production now on the first one, you can kind of do the math and when the second one would be available. Regarding other things that you can add to the toolbox to improve performance, whether that's around connectivity, broadly speaking, whether that's around specific I/O and/or networking and/or other aspects of the system, we are absolutely looking at all of that. 
When we think about developing these products, we're thinking about rack system performance. The chip, the CPU is a big part of it, but how you move data in and out of the system, to your question, is as large an area as any. And we have a lot of activity underway in all these areas. Nothing that we can announce here on this call, but completely cognizant of that being an area that we could have even larger differentiation.

**Operator** (Operator):
Your next question comes from the line of Lee Simpson from Morgan Stanley.

**Lee Simpson** (Analysts):
Maybe just 2 quick ones, if I could. Maybe first one for Jason. $773 million for licensing really stands out. Congratulations to everyone there. You did talk about Total Access. You did talk about CSS deals, particularly smartphones and I think data center, you mentioned. But do we have any sort of architecture license agreements in there? And could we look at 770 plus as a new level, a structural level? 
And maybe for follow-on for Rene, maybe in line with some of the earlier questions, it's interesting that as we look to higher ASP CPUs in the future with higher core count, could it be that we see a higher per core dollar equivalence in that pricing? In other words, playing off this capability that are associated capabilities, perhaps networking and I/O as mentioned in the last question, that drives that per core dollar value up?

**Jason Child** (Executives):
Okay. Thanks, Lee. On your first question around license, yes, we didn't -- we talk about ATA and CSS, which is the vast majority of everything that we're selling going forward. Architecture licenses are very, very few and far between. And so I would think of it as really being ATA and CSS. That is the bulk of most everything we're selling going forward. In terms of absolute magnitude of dollars, yes, $773 million is -- was a great quarter. But if you -- I think kind of work out the details, I said it was going to be increasing and going up from there in this next quarter.  And even in Q4, it's going to step up again. 
So we're not -- we haven't talked about next year, whether or not that's the new the new number every quarter. I don't know if I would say that. But I will say the pipeline has been surprisingly strong, stronger than we expected when we started the year. And a little bit like the last couple of years where we've had maybe deals that weren't initially -- they were in the pipeline, but they weren't -- they were not renewals. They were -- these were incremental and new deals that are kind of hard to forecast. We're in that same situation again. 
And so what's interesting is when we started this year, we thought it was going to be much more around royalties and that a lot of the license growth related to all the AI investments, we thought maybe we kind of had passed a lot of that. Well, what's interesting is it seems to be that with AI and the consistent variability and now everyone's trying to address all the agentic workloads we're seeing that the need for additional license and additional product variations and different technologies is not slowing down at all. 
And so that's particularly exciting. As you know, any license beats, especially with ATAs and CSSs, that will -- is very highly likely to turn into design wins and very likely to turn into even more royalties probably 12, 18 months, 24 months down the road. So that's a really good setup for next year and after. And so -- but we'll have to, I guess, get through the next couple of quarters before I can talk about next year. But the pipelines do look strong. 
And even with the memory issues that we've seen really kind of making for some tough comps in the mobile business, which really that does end mostly in this quarter that we're now in Q3. We start lapping those headwinds that really started in January, February of next year. So the comps also get easier. But overall, we think it's a really good setup for the balance of this year and likely going into next year as well.

**Rene Haas** (Executives):
Yes. On pricing, it's a tricky one from the perspective of memory pricing has obviously increased a lot since we announced the Arm AGI CPU. Data centers are getting more and more complicated to build, whether it's through just, again, memory pricing/finding laborers, et cetera, et cetera. So while we want to be cognizant of not pushing the pricing piece too hard given all these other factors, I think it is fair to say that there's probably some pricing elasticity that we could potentially exercise on these larger chips and the chips that have higher core counts. We'll look at all of it, obviously. But I think it's fair to say that there probably is some headroom there.

**Operator** (Operator):
Your next question today comes from the line of Vivek Arya from Bank of America Securities.

**Vivek Arya** (Analysts):
One for each. Jason, let's say, smartphone units are down again double digit next year. Do you think royalties will kind of be similarly profiled to what we saw this year? Or are there other dynamics at play? And then, Rene, on the AGI platform, let's assume we believe in the technical merits. My question is, does Arm have the scale in the ecosystem to secure supply? Because, for example, yesterday, when AMD reported they raised their server CPU business, right? By several billions of dollars. 
So that tells me that they have the scale to go and get incremental supply, right? So how are you dealing with that question about does Arm have enough scale to go and get the supply to be a meaningful player in the CPU markets, right? Given your belief in the technical merits of the product?

**Rene Haas** (Executives):
Yes. Thank you, Vivek. I'll start, take your second part of your question first, and then Jason will talk about the smartphone scenario that you had described. Your question is a valid one. The way I think about it is that the Arm AGI CPU is our first product. AMD has been at it for a long time. They've got a lot of SKUs. They buy a lot of capacity from TSMC. They have a lot of relationships that they've built over decades. This is our first product. That said, it's not our first relationship with folks like TSMC. 
It's not our first relationship with memory vendors such as Micron, Samsung and SK. They've known us for years and decades, and we've been working pretty diligently to share with them our long-term plans. I think supply for the industry is going to be tight. And as Jason mentioned, we'll talk a bit more about our future outlook in upcoming quarters. But we are going to be working very, very hard to secure the supply that we need for the expanded demand because we think it's very, very, very large. 
And our partners know that. And we've been talking to them not for weeks, not for months, but probably a year plus as we've talked about doing this platform. So we've looked at this as a long-term endeavor. It's not a 1-year single project. It's a 5- to 10-year endeavor that's going to require relationships across all the supply chain, and we're very, very serious about making sure we get all that done.

**Jason Child** (Executives):
Thanks, Vivek. So regarding the mobile business, when we look at some of the external forecasts, I think IDC has units in mobile growing basically flat. I think it's minus 1% next year. As we talk to partners, that's -- I'd say, flat is generally what folks are expecting. We -- there's already been kind of the hit and the reduction due to the memory constraints. And I think the expectations are those constraints stay relatively consistent, which basically means flat growth, not further deterioration. And then because we have -- we continue to have more v9 adoption, it's -- we're now getting over 50%. So it's a little less of a tailwind. 
But CSS adoption continues to grow. We also have multiple partners on next generations of CSS, which are at slightly higher royalty rates with -- and higher chip prices. So all that means that we will grow the overall business much faster than the market. So think of it at least being in the kind of double digits plus in growth rate for next year. That's our best guess right now. If we see anything that changes, of course, we'll let you guys know. But that's what industry as well as our partners all seem to think at this point.

**Operator** (Operator):
We will now take our final question for today. And the final question comes from the line of Joe Quatrochi from Wells Fargo.

**Joseph Quatrochi** (Analysts):
You talked about securing more supply on AGI, and I assume that comes at a higher cost. So can you just kind of talk us through the ability to offset that and how we should think about just the gross margin puts and takes as you start to ship?

**Rene Haas** (Executives):
Yes, I'm sorry. Could you repeat that one more time?

**Joseph Quatrochi** (Analysts):
Yes. Just -- I assume that the increased supply that you're getting for AGI is coming at a higher cost. So can you just talk about your ability to offset those higher costs, pass that through to customers in terms of pricing and then the puts and takes on gross margin?

**Rene Haas** (Executives):
Yes. No, thank you. As I mentioned earlier, the overall cost of the systems, memory being probably the single largest contributor to all that. And then you've got kind of downstream other impacts to your point, on different parts of the supply chain, definitely put margin pressure. That being said, we do have some elasticity on pricing and the ability to increase it, which I think we've already demonstrated an ability to do that as we've gotten started with the program. 
So I'm actually not as worried on that point relative to offsetting any constraints on supply and cost and managing it downstream. You've seen public comments from everybody else who's in this business that that's what we're doing. We'll be following where the market goes and making sure that we're not trailing common sense, but at the same time, not trying to cause too much pain on the end customers. It's our first product. We want to make sure everybody wins with it, but I'm not as worried about that piece impacting gross margins.

**Jason Child** (Executives):
Yes. Maybe just to reiterate, what we said was for this first version, we're expecting to be somewhere in the high 30s to low 40% gross margin. And for the first version, we expect it to be probably a little lower. And then as we develop more expertise, probably rely on doing a little more work ourselves and maybe less from partners over time, which others in the market do over time, we'll get ourselves to more of the market standard of 50% plus. 
But I don't expect that to happen on the first version. That's probably going to happen more on the next version. So for this version, I would stick to the kind of 30% to 40% range. And then we'll obviously give you updates on a quarterly basis as we start shipping in Q4.

**Operator** (Operator):
That was our final question for today. I will now hand the call back to Rene for closing remarks.

**Rene Haas** (Executives):
Thank you, and thank you for all the questions. They were very, very timely and excellent questions. Just to summarize, this was a great quarter for the company. 50% licensing growth means a lot of growth coming in the future in royalties, which we feel great about. We also feel very, very good about the fact that our data center business continues to flourish. We had talked for many, many years about Arm getting to 20% in data centers. The fact that we are 50% in the last year and will be 60% by the end of this year is also something we're very, very proud of. 
But most importantly, I think what we're now starting to see is what was one great business is now turning into 2 great businesses. The IP business continues to do very, very well. We're very confident in this growth going forward. But now with our new AGI CPU ramping into production, increased confidence to achieve the $2 billion number that we've been talking about, it just thrills me to be able to talk about 2 businesses now rather than 1 that are both going to be on amazing growth paths and could not be prouder of what the company has achieved, thanking our employees, our partners and customers who helped make it happen. So thank you again for all the questions and comments, and congratulations to the Arm team for a great quarter.

**Operator** (Operator):
Thank you. This concludes today's conference call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ARM_Q1_2027_Earnings_Call_20260729.md
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 FY27 營收財測（原話："expect revenue of $1.38 billion, plus or minus $50 million"）
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 授權年增約 30%、權利金年增低十幾%（原話："royalty revenue to be up in the low teens year-on-year."）
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 non-GAAP 營業費用約 7.8 億美元（原話："non-GAAP operating expense to be approximately $780 million"）
- 2026-07-29｜Jason Child (CFO)｜guidance：其餘季度營業費用預期逐季成長幅度（原話："mid-single-digit percentage quarter-on-quarter"）
- 2026-07-29｜Jason Child (CFO)｜guidance：全年權利金成長預期由約 20% 下修為接近高十幾%（原話："that's probably somewhere closer to the high teens right now"）
- 2026-07-29｜Jason Child (CFO)｜guidance：先前說法：未來數年（含本年）權利金年增約 20%（原話："around 20% year-on-year for the next few years in royalties"）
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 權利金口徑：此處說低到中十幾%，與 prepared remarks 的 low teens、後段 13% 並陳（原話："we guided to kind of the low to mid-teens for Q2"）
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 權利金 13%，同時調高授權成長（原話："We're now guiding to 13% royalty growth in Q2."）
- 2026-07-29｜Jason Child (CFO)｜guidance：FY28、FY29 權利金 20%+ 成長維持（原話："I think that's very much still intact."）
- 2026-07-29｜Jason Child (CFO)｜guidance：AGI CPU 超過 10 億美元的更新時點在 Q3 財報（原話："provide an update at our Q3 results"）
- 2026-07-29｜Jason Child (CFO)｜guidance：SoftBank 授權／設計服務季度運行率約 2 億美元（原話："quarterly run rate for the rest of the year to be around"）
- 2026-07-29｜Jason Child (CFO)｜margin：Q1 非 GAAP 營業利益（原話："Non-GAAP operating income was $531 million"）
- 2026-07-29｜Jason Child (CFO)｜margin：Q1 非 GAAP 營業利益率及年增（原話："41%, up 200 basis points year-on-year."）
- 2026-07-29｜Jason Child (CFO)｜margin：Q1 營業費用低於財測約 2,700 萬，歸因時點（原話："This was about $27 million below our guidance due"）
- 2026-07-29｜Jason Child (CFO)｜margin：營業費用差異來自工具（模擬、雲端支出）而非人力（原話："it was really more on kind of the tools that were utilized"）
- 2026-07-29｜Jason Child (CFO)｜margin：Q1 自由現金流（原話："generated free cash flow of $665 million for the quarter"）
- 2026-07-29｜Jason Child (CFO)｜margin：AGI CPU 首代毛利率區間（高 30% 到低 40%）（原話："somewhere in the high 30% range, maybe low 40s percent"）
- 2026-07-29｜Jason Child (CFO)｜margin：AGI CPU 毛利率數年內目標 50%（原話："we do expect to get to 50%, but"）
- 2026-07-29｜Jason Child (CFO)｜margin：授權 ACV 作為底層授權趨勢指標（口徑）（原話："ACV grew 13% year-on-year, maintaining strong momentum."）
- 2026-07-29｜Jason Child (CFO)｜commitment：AGI CPU 營收滿 10% 後獨立列示為第三條線（原話："at least 10% of revenue, we'll break it out"）
- 2026-07-29｜Rene Haas (CEO)｜commitment：AGI CPU 需求超過 20 億美元（原話："Demand now exceeds $2 billion as we continue to add"）
- 2026-07-29｜Jason Child (CFO)｜commitment：對 AGI CPU 超過 10 億美元的信心上升（原話："confidence in achieving more than $1 billion has increased"）
- 2026-07-29｜Jason Child (CFO)｜commitment：內部目標高於對外數字（原話："internally, we do have higher targets"）
- 2026-07-29｜Rene Haas (CEO)｜commitment：TAM 不調整、但認為先前可能保守（原話："we're not changing the numbers at all"）
- 2026-07-29｜Rene Haas (CEO)｜product：AGI CPU 初期產品已交付多家客戶（原話："Initial product has now been delivered to"）
- 2026-07-29｜Rene Haas (CEO)｜product：AGI CPU 目前為 128 核；方向為更多核，路線圖無可說（原話："the direction of travel is more cores"）
- 2026-07-29｜Rene Haas (CEO)｜product：AGI CPU 可連接客製加速器（含 NVLink Fusion）（原話："paths for Arm to connect to custom accelerators"）
- 2026-07-29｜Rene Haas (CEO)｜product：AGI CPU 適用三類應用（傳統伺服器、head node、agentic）（原話："we had folks like Cerebras and OpenAI, which were"）
- 2026-07-29｜Rene Haas (CEO)｜product：Neoverse 出貨累計核數（原話："Neoverse shipments have now surpassed 1.5 billion cores"）
- 2026-07-29｜Rene Haas (CEO)｜customer：資料中心權利金年增超過一倍（原話："Data center royalties more than doubled year-over-year"）
- 2026-07-29｜Rene Haas (CEO)｜customer：NVIDIA Vera 量產（原話："brought Vera into production."）
- 2026-07-29｜Rene Haas (CEO)｜customer：IDC：Arm 加速伺服器平台支出近兩季近倍增（原話："has nearly doubled in the past 2 quarters"）
- 2026-07-29｜Rene Haas (CEO)｜customer：V9／CSS 使 Arm 相對隔離於手機市場衰退（原話："we have moved the vast majority of the customers to V9"）
- 2026-07-29｜Jason Child (CFO)｜customer：記憶體漲價下手機銷量下滑，被較高權利金率抵銷（原話："more than offset the decline in smartphone sales"）
- 2026-07-29｜Jason Child (CFO)｜risk：手機疲弱擴及中高階市場（原話："even some upper and mid-tier being affected"）
- 2026-07-29｜Jason Child (CFO)｜risk：供應鏈未來兩年相當緊（原話："supply chain is pretty tight"）
- 2026-07-29｜Jason Child (CFO)｜risk：供應鏈於日曆 2028–29 放寬（原話："supply chain is going to loosen or at least expand"）
- 2026-07-29｜Rene Haas (CEO)｜risk：回應單一元件缺口風險：無單點失敗（原話："there isn't one single point of failure"）
- 2026-07-29｜Rene Haas (CEO)｜competition：Qualcomm 宣布進入 AI 資料中心 CPU 市場（原話："Qualcomm has also announced plans to enter the AI data"）
- 2026-07-29｜Jason Child (CFO)｜competition：CPU TAM 最新估計 2,200 億美元（先前 1,000 億+）（原話："recent estimate is $220 billion sitting on"）
- 2026-07-29｜Rene Haas (CEO)｜competition：開源模型對 Arm 中性到正面（原話："between a net neutral to a net positive"）
- 2026-07-29｜Rene Haas (CEO)｜capital_allocation：管理層對供給端比 90 天前更樂觀（原話："we are more optimistic than we were 90 days ago"）

### ARM_Shareholder_Analyst_Call_Arm_Holdings_plc_20260324.md
- 2026-03-24｜Rene Haas｜product：CEO 表示 Arm 開始以晶片形式直接供貨，進入新業務（原話："Arm, and we are supplying CPUs as chips."）
- 2026-03-24｜Rene Haas｜customer：CEO 稱做自家晶片的首要原因是夥伴提出需求（原話："reason 0 is our partners have asked us for it."）
- 2026-03-24｜Rene Haas｜product：CEO 給出 CSS 占權利金比重的口徑（原話："represents almost 20% of our royalties and growing."）
- 2026-03-24｜Rene Haas｜product：CEO 估算 agentic AI 下每 GW 所需 CPU 核心數增為 4 倍（原話："120 million CPU cores for that same gigawatt"）
- 2026-03-24｜Rene Haas｜risk：CEO 承認 AI 投資可能放緩、估值可能變動，但主張 AI 不會消失（原話："it may be a financial bubble in the case of investment"）
- 2026-03-24｜Mohamed Awad｜product：產品主管說明 AGI CPU 已可供貨（原話："Arm AGI CPU is available now, and we're so proud of that."）
- 2026-03-24｜Mohamed Awad｜customer：客戶正在評估 AGI CPU（原話："Customers are actually evaluating it as we speak."）
- 2026-03-24｜Mohamed Awad｜commitment：管理層給出 AGI CPU 量產時點（原話："by the end of the year, and we are excited to share"）
- 2026-03-24｜Mohamed Awad｜product：AGI CPU 規格：Neoverse V3 核心數（原話："We pack in 136 of those cores"）
- 2026-03-24｜Mohamed Awad｜product：管理層給出已出貨至資料中心的 Neoverse 核心累計數（原話："over 1.25 billion Arm Neoverse cores"）
- 2026-03-24｜Mohamed Awad｜competition：管理層指稱 x86 業者需過度配置資料中心（原話："data center operators have to overprovision"）
- 2026-03-24｜Rene Haas｜competition：CEO 與 x86 同等結構比較的效能主張（原話："36 kilowatts, 2x the performance in the same power."）
- 2026-03-24｜Rene Haas｜competition：CEO 量化每 GW 額外電力對應的資本支出（原話："it's up to $10 billion of"）
- 2026-03-24｜Rene Haas｜commitment：CEO 承諾 AGI CPU 後續世代產品線（原話："So we are committing to future generations of this product."）
- 2026-03-24｜Santosh Janardhan｜commitment：Meta 方面稱為多世代合作（原話："multigenerational partnership. I just want to emphasize"）
- 2026-03-24｜Santosh Janardhan｜product：Meta 說明首顆合作 CPU 的設計取向（原話："something to minimize risk for this iteration."）
- 2026-03-24｜Rene Haas｜customer：CEO 列出已承諾購買 AGI CPU 的客戶（原話："we have committed customers, Meta, OpenAI, Cloudflare, SAP"）
- 2026-03-24｜Rene Haas｜guidance：CEO 給出 AI 資料中心權利金 TAM 現況口徑（原話："that represents today about a $3 billion TAM."）
- 2026-03-24｜Rene Haas｜guidance：CEO 稱雲端 AI 業務數年內將成最大業務（原話："probably be our largest business in a few years."）
- 2026-03-24｜Rene Haas｜guidance：CEO 給出晶片業務未來 TAM 估計（原話："we think this represents about $100 billion TAM for us"）
- 2026-03-24｜Rene Haas｜guidance：CEO 給出 2030 年前整體可觸及 TAM（原話："greater than a $1 trillion TAM by the end of the decade."）
- 2026-03-24｜Rene Haas｜commitment：CEO 稱 IP／CSS 業務表現優於 IPO 路演時對投資人所說（原話："we're actually ahead of that."）
- 2026-03-24｜Rene Haas｜product：CEO 重申 Arm 現在提供三種型態：IP、CSS、晶片（原話："IP, CSS and chips. IP, CSS and chips."）

### 問答異常語氣（迴避／改口／保留）
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Quatrochi：10億美元以上上調信心的具體來源（晶圓、記憶體？）｜答法：Rene 答「all of the above」，未指出單一項目，也未給數量
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Quatrochi：超過10億美元部分的毛利率結構｜答法：Jason 稱無變化，沿用上季區間，並說漲價仍在消化、定價待定，詳細更新留到 Q3 末
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Mobley：150億美元（FY31）AGI 營收是否已含供應限制｜答法：Rene 未直接回答是／否，轉談 TAM 上調；Jason 談供應鏈放寬時程，未對 FY29–31 需求給數字
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Arya：為何無法再多確保10億美元供給｜答法：Rene 以整體供應吃緊回應，未說明 Arm 具體卡在哪一環，亦未給額外產能數字
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Naji：手機單位需求與全年權利金展望｜答法：Rene 把數字交給 Jason；Jason 稱全年「if I had to guess」接近高十幾%，Q2 權利金表述在不同段落為 low teens／low to mid-teens／13%，且說下季再更新

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

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260730","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"每顆晶片權利金費率的階梯（v8 2.5-3.5% → v9 ~5% → CSS ~10%）持續往上爬，資料中心的量補上行動段的飽和"},{"id":"H2","text":"自製 AGI CPU 兌現訂單，且不嚴重疏離授權客戶，也不把混合毛利率壓到讓估值框架切換"},{"id":"H3","text":"市場願意繼續用「IP 授權年金」的倍數為 Arm 定價，而不是用「半導體公司」的倍數"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"三法域反壟斷同案，攻擊「中立 IP 商」身分。Qualcomm 於 2025-03 同時向美國 FTC、歐盟執委會與南韓 KFTC 遞交反壟斷投訴，指 Arm 在數十年開放授權後開始限制設計取用。三者皆已動作：FTC 於 2026-05-15 開查（Bloomberg 首報，調查焦點是 Arm 是否在自售競品的同時 degrade/deny 對 Apple／Qualcomm／Nvidia 等數百家授權客戶的架構授權；截至 7 月底仍在文件保全／證據蒐集階段，未提訴）；歐盟執委會已開啟自己的調查（cms.law）；KFTC 於 2025-11-19 突襲 Arm 首爾辦公室。若任一法域強制中立授權，CSS 的 ~10% ASP 溢價失去依據——這正是 H1 費率階梯的心臟。歷史罰則對照：歐盟曾對 Qualcomm 支配地位濫用開罰 €997M。"},{"id":"R2","text":"授權客戶一手保住 Arm 授權、一手出資繞開 Arm。Qualcomm 於 2024-12 陪審團與 2025-09-30 法院裁定中勝訴（法院駁回 Arm 剩餘違約主張並否決重審動議），確立其 Nuvia 血統的 Oryon 核心在既有架構授權下合法——Arm 以併購為由終止架構授權的槓桿在司法上被削弱。同時 Qualcomm 2025-12-10 完成收購 Ventana（RISC-V 伺服器 CPU）、2025-12-18 完成收購 Alphawave（$2.3-2.4B，連結 IP），並於 2026-06-24 發表基於 Oryon 的 250 核 Dragonfly C1000（5GHz、2028 商用），首發部署客戶是 Meta——而 Meta 正是 Arm 自製 AGI CPU 的共同開發客戶。Qualcomm 首席工程師稱 Oryon 核心「僅 1% 或更少源自 Arm 原始技術」，意即高階核心上客戶付的是 ISA 相容性、不是 Arm 的設計。"},{"id":"R3","text":"估值框架由「IP 授權年金」切換為「半導體公司」。機制是 Arm 自己的計畫：FY2031 目標 $25B 營收中 $15B 為自製矽晶片（毛利率 35-42%），混合毛利率將由 97.5% 壓向 63%。第一個財報級顯影是合併毛利率單季跌破 90%，預估最早出現於 Q4 FY27。可比組一旦由 CDNS（34.9x／毛利 85.9%）移向 AVGO（19.0x／毛利 76.3%）與半導體中位（28.19x），倍數壓縮 40-60%。此風險不需要任何競爭者出現，也不需要任何假設失敗——它在 thesis 成功的路徑上。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"FY+2 forward PE ≤ 35x（約 $108）→ 重跑完整 DD；≤ 30x（約 $92）Base 5Y IRR 才過 9%/yr。重啟後角色上限衛星 starter、倉位帽 3%","irr_base_pct":-8.2,"ev5y_pct":-36.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":0.18,"ev5y_pct":-36.5,"irr_base_pct":-8.2,"max_dd_pct":-75.0,"bull_5y_price":288.0,"bear_5y_price":56.0,"p_bull_pct":17.0,"p_bear_pct":35.0,"rearm_trigger":"FY+2 forward PE ≤ 35x（約 $108）→ 重跑完整 DD；≤ 30x（約 $92）Base 5Y IRR 才過 9%/yr。重啟後角色上限衛星 starter、倉位帽 3%","price_at_dd":224.89,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
