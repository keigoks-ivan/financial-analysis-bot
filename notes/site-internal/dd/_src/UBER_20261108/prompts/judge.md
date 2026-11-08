你是 stock-analyst **v20 判斷 agent**，標的 UBER（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"UBER","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UBER_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UBER_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":14766,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）"},"note":"未查得共識營收，省略"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income","value":2304,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m（占 Gross Bookings 3.9%；占營收約 15.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）"},"note":"未查得，省略"},{"id":"f_kpi2_gaap_income_from_operati","label":"GAAP income from operations","value":1447,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m（占營收 9.8%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）"},"note":"未查得，省略"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":2535,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m（營運現金流 2,639；FCF 占營收約 17.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）；TTM FCF 約 10.4B 取自 Quartr 摘要"},"note":"未查得，省略"},{"id":"f_kpi5_gross_bookings","label":"Gross Bookings","value":59819,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m（YoY +20% 固定匯率；Mobility 29,512 +18%、Delivery 28,539 +22%、Freight 1,768 +35%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）"},"note":"未查得，省略"},{"id":"f_kpi6_adjusted_ebitda","label":"Adjusted EBITDA","value":2963,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m（占 GB 5.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）"},"note":"未查得，省略"},{"id":"f_kpi7_mapcs_trips_archetype","label":"MAPCs／Trips（平台 archetype）","value":215,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"M MAPCs（YoY +14%）；Trips 4,061M（YoY +16%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）"},"note":"未查得，省略"},{"id":"f_kpi8_non_gaap_eps","label":"Non-GAAP EPS","value":0.88,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD（YoY +35%；GAAP 稀釋 EPS 0.25，含權益投資重估稅前虧損 476m）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（Business Wire／Finviz 轉載確認）"},"note":"前季給的 Q3 指引為 0.84–0.88，實際落在區間上緣；市場共識值未查得"},{"id":"f_kpi9_guidance_q4_2026","label":"Guidance：Q4 2026 展望","value":"Gross Bookings 63.25–65.25B（固定匯率 +18% 至 +22%，匯率約 1 個百分點逆風）；Adjusted EBITDA 3.13–3.23B；Non-GAAP EPS 0.95–0.99（YoY +34% 至 +39%）","period":"Q3 FY2026（公告於 2026-11-04）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）；另提及年底約 700 輛全無人駕駛車上線、2027 年超過 2,000 輛"},"note":"未查得，省略；公司未提供全年指引"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_uber_gross_margin_pct","label":"UBER 毛利率","value":43.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_uber_operating_margin_pct","label":"UBER 營業利益率","value":12.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_uber_fcf_margin_pct","label":"UBER FCF 利潤率","value":18.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dash_gross_margin_pct","label":"DASH 毛利率","value":51.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dash_operating_margin_pct","label":"DASH 營業利益率","value":5.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dash_fcf_margin_pct","label":"DASH FCF 利潤率","value":12.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lyft_gross_margin_pct","label":"LYFT 毛利率","value":45.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LYFT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lyft_operating_margin_pct","label":"LYFT 營業利益率","value":-1.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LYFT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lyft_fcf_margin_pct","label":"LYFT FCF 利潤率","value":16.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LYFT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_grab_gross_margin_pct","label":"GRAB 毛利率","value":44.45,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GRAB.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_grab_operating_margin_pct","label":"GRAB 營業利益率","value":10.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GRAB.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_grab_fcf_margin_pct","label":"GRAB FCF 利潤率","value":-0.45,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GRAB.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bkng_operating_margin_pct","label":"BKNG 營業利益率","value":32.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BKNG.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bkng_fcf_margin_pct","label":"BKNG FCF 利潤率","value":32.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BKNG.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":40.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%（SBC 591m ÷ GAAP 營業利益 1,447m；占營收 4.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"SBC 591m 取自新聞稿現金流量表；比率為本 agent 計算。Adjusted EBITDA 調節表口徑為 529m（不含併購、重組、舊獎勵結算相關 SBC），若用此口徑為 36.6%"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":68.59,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-9.09,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":50.31,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.36 → 3.36）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.41 → 4.41）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.5 → 5.5）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.36,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":4.41,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":5.5,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 3.36 → 3.36（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":40.35,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝50.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.48,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝48.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":48.1,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝47.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":47.1,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":20.41,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 3.36，分子＝快照價 68.59","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":7669.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 17737.0、現金 10068.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":2041.9,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":147722.79,"period":"2026-11-08","unit":"USD m","basis":"市值 140053.79 ＋ 淨負債 7669.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":57814.28,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（46 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":67017.55,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（48 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.56,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 68.59 / W52 75.29 / W104 78.49 / W250 59.83 / W250 13週斜率 0.74%"},{"id":"f_ma_w52","label":"52 週均線","value":75.29,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":78.49,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":59.83,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.74,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：Uber 稱 mobility／delivery／logistics 低進入門檻、低轉換成本，預期未來有新進入者；AV 對手含 Alphabet(Waymo)、Amazon(Zoox)、Tesla。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"We also compete with other ridesharing companies, including certain of our minority-owned entities, for Drivers and riders, including Bolt, Didi, Lyft, and Ola. There are also a number of companies developing and introducing autonomous vehicles and technologies 12 that either are competing with us or may compete with us in the future, including Alphabet (Waymo), Amazon (Zoox), and Tesla.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 自述負面媒體報導使競爭對手募資、加碼投入並提升品類地位與市占。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"As a result, our competitors raised additional capital, increased their investments in certain markets, and improved their category positions and market shares, and may continue to do so.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K：Delivery 對手含 DoorDash、Instacart、Gopuff、Rappi、Delivery Hero、Just Eat Takeaway、Amazon。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"Our Delivery offering competes with numerous companies in the meal, grocery and other delivery space in various regions for Drivers, consumers, and merchants, including DoorDash, Instacart, Gopuff, Rappi, Delivery Hero, Just Eat Takeaway, and Amazon.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Schwab Network 影片摘要：UBER 面臨 DASH、LYFT、Waymo 加速搶市占的逆風。","source":"Schwab Network","url":"https://schwabnetwork.com/video/uber-rally-faces-headwinds-as-dash-lyft-waymo-accelerate-market-share","excerpt":"Faces Headwinds as DASH, LYFT, Waymo Accelerate Market Share UBER Rally Faces Headwinds as DASH, LYFT, Waymo Accelerate Market Share The 2025 rally in Uber Technologies (UBER) was a \"move we've been expecting for quite a while,\" says LikeFolio's Andy Swan. However, he argues its moat is now being threatened. App usage data shows competitors like DoorDash (DASH), Lyft Inc.","as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Uber 10-K(FY2025)揭露 2023、2024、2025 年皆無任何客戶占營收 10% 以上；收款依賴信用品質高的支付服務商。","source":"SEC EDGAR 10-K FY2025 Item 8 Financial Statements","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"No customers accounted for 10% or more of revenue for the years ended December 31, 2023, 2024, and 2025.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026 Gross Bookings $59.8B, +20% constant currency (fifth straight quarter >20% per search summary); Mobility +17%, Delivery +23%; Q4 guide $63.25–65.25B (+18–22% cc).","source":"Uber Q3 2026 8-K earnings press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001543151/000154315126000039/uberq326earningspressrelea.htm","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Mobility growth ran 1–2 points below management expectations due to elevated fuel prices and tighter driver supply in some international markets (supply-side constraint); trends improved in October.","source":"Uber Q3 26 Prepared Remarks","url":"https://s23.q4cdn.com/407969754/files/doc_earnings/2026/q3/transcript/Uber-Q3-26-Prepared-Remarks.pdf","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Uber One passed 50M members, generating about half of Mobility and Delivery Gross Bookings; agreed to acquire Delivery Hero, expected to close 2H 2027.","source":"Uber Q3 26 Prepared Remarks","url":"https://s23.q4cdn.com/407969754/files/doc_earnings/2026/q3/transcript/Uber-Q3-26-Prepared-Remarks.pdf","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"About 700 fully driverless vehicles expected on Uber by year-end 2026 and over 2,000 in 2027; $239M loss on Aurora stake in Q3.","source":"24/7 Wall St., Uber Q3 2026 earnings","url":"https://247wallst.com/cards/uber-q3-2026-earnings-uber-01m6k6trxhjn4rq4qdym9215wx","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素：Uber 目前受 DOJ、FTC 及其他聯邦、州、地方與外國政府機關多項詢問、調查與資料要求，不利結果可能傷害業務；反壟斷申訴已在美國與巴西等地提出。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"We currently are subject to a number of inquiries, investigations, and requests for information from the DOJ, FTC, other federal, state and local government agencies and other foreign government agencies, the adverse outcomes of which could harm our business.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 列示：歐盟、美國、巴西、印度等主要市場競爭法執法趨嚴，焦點含定價平價、操縱價格與濫用市場力；主管機關可罰款、強制剝離資產或限制定價模式。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"Competition authorities closely scrutinize us under U.S. and foreign antitrust and competition laws.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FTC 於 2025-04 起訴 Uber One 訂閱做法（ROSCA），21 州加 DC 於 2025-12 加入；搜尋結果顯示 Uber 否認並主張為 first-party biller。","source":"CBT News / SAN 等（搜尋摘要）","url":"https://www.cbtnews.com/ftc-files-suit-against-uber-for-deceptive-practices/","excerpt":null,"as_of":"2025-04-22","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Uber 10-K 風險因子指出，近期關稅推高新舊車零件價格，增加司機與貨運業者成本，可能使其減少在平台上的工時或另尋收入來源；未見自身產品出口管制或直接進口關稅暴露的記載。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"Factors such as inflation, increased fuel prices, and increased vehicle purchase, rental, insurance, or maintenance costs, including increased prices of new and used vehicle parts as a result of recent tariffs, global supply chain challenges","as_of":"2026-02-13","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MarketBeat 分析：Uber 司機自備並維修車輛，汽車零件關稅可能推高其維修成本。","source":"MarketBeat","url":"https://www.marketbeat.com/originals/why-ubers-stock-could-soar-on-av-growth-and-tariff-resilience","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素提及中東與俄烏衝突，可能涉及制裁與區域不穩，影響無法預測，可能對業務、營運結果與股價造成重大損害（搜尋摘要轉述，未讀原文）。","source":"Uber Technologies Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026年5月報導：Uber 預期Q2訂單穩健，但受中東衝突、燃料成本與地緣緊張壓力（搜尋摘要轉述）。","source":"Boursorama (Reuters 法文轉載)：Uber prévoit des réservations solides au T2 malgré le conflit au Moyen-Orient","url":"https://www.boursorama.com/bourse/actualites-amp/uber-prevoit-des-reservations-solides-au-t2-malgre-le-conflit-au-moyen-orient-31e30ed6ea3cc3a63deac4249ad74e0d","excerpt":null,"as_of":"2026-05-06","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"自駕供應集中度：Uber 持有 Lucid 約11% 股權，訂購至少3.5萬輛搭載 Nuro 系統的 robotaxi 車輛；Waymo 計畫2028年1月起在奧斯汀與亞特蘭大自營，現有合約至少到2028年5月（二手整理，未核原文）。","source":"letsdatascience：Uber Reengages Partnerships To Rebuild Autonomy","url":"https://letsdatascience.com/news/uber-reengages-partnerships-to-rebuild-autonomy-75896a14","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 Mobility Gross Bookings +17% cc (~$29.5B reported); Mobility revenue -2% to $7.5B; management cited international driver supply constraints for growth short of expectations (搜尋摘要彙整，未逐字核原文)","source":"Uber Announces Results for Third Quarter 2026 / Uber Q3 26 Prepared Remarks","url":"https://s23.q4cdn.com/407969754/files/doc_earnings/2026/q3/transcript/Uber-Q3-26-Prepared-Remarks.pdf","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Delivery Gross Bookings +23% cc (~$28.5B), Delivery revenue +23% to $5.5B; Freight Gross Bookings +35% to $1.77B, third straight quarter of acceleration; total GB $59.8B +20% cc","source":"Uber Announces Results for Third Quarter 2026","url":"https://seekingalpha.com/pr/20712391","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 2026 guidance: Gross Bookings $63.25B–$65.25B, +18% to +22% YoY cc","source":"Uber Q3 2026 results (summary)","url":"https://finviz.com/news/415280/uber-announces-results-for-third-quarter-2026","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Food delivery share end-2024 (US): DoorDash 60.7%, Uber Eats 26.1%, Grubhub 6.3% (2024 data, not 2026)","source":"Earnest Analytics","url":"https://www.earnestanalytics.com/insights/doordash-leads-us-delivery-share-but-some-cities-still-competitive","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 Mobility/Delivery/Freight segment figures","source":"Uber Q3 2026 10-Q","url":"https://www.sec.gov/Archives/edgar/data/0001543151/000154315126000041/uber-20260930.htm","excerpt":"Mobility Gross Bookings grew 17% year-over-year, on a constant currency basis, primarily due to an increase in Mobility Trip volumes. Delivery Gross Bookings grew 23% year-over-year, on a constant currency basis, primarily driven by an increase in Delivery Trip volumes. Freight Gross Bookings grew 35% year-over-year, on a constant","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 列出自駕車業者 Alphabet(Waymo)、Amazon(Zoox)、Tesla 為正在或可能與 Uber Mobility 競爭的對手","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"There are also a number of companies developing and introducing autonomous vehicles and technologies 12 that either are competing with us or may compete with us in the future, including Alphabet (Waymo), Amazon (Zoox), and Tesla.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：AI 助理等新技術可能使 Uber 與消費者的關係被中介化，需求轉向競爭者","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"shifts in consumer behavior, including the use of new or emerging technologies, such as AI-enabled platforms and digital assistants, may disintermediate our relationship with consumers by controlling how our products are accessed, presented or selected, which could redirect demand to competitors and adversely affect our demand and growth.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K：大眾運輸與私家車為 Mobility 替代品，私家車占多數乘客里程","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"Our Mobility offering competes with personal vehicle ownership and usage, which accounts for the majority of passenger miles in the markets that we serve","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"10-K FY2025 describes Delivery expanding beyond Uber Eats to Uber Direct (white-label Delivery-as-a-Service for retailers and restaurants) and advertising.","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"Over the last several years, our Delivery business has expanded to include Uber Direct, our white-label Delivery-as-a-Service offering to retailers and restaurants around the world, as well as advertising.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Uber One reached about 50 million members, roughly half of Mobility and Delivery Gross Bookings; Q1 2026 reported revenue growth was negatively impacted by business model changes.","source":"Uber Q1 2026 earnings press release 8-K","url":"https://www.sec.gov/Archives/edgar/data/0001543151/000154315126000019/uberq126earningspressrelea.htm","excerpt":"“Reaching 50 million Uber One members is an exciting milestone as we execute against our platform strategy, with members now driving half of our Gross Bookings across Mobility and Delivery.”","as_of":"2026-05-06","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q1 2026 call: AV trips up >10x YoY, partnerships with 20+ AV companies, AV not profitable for a few years.","source":"Motley Fool Q1 2026 earnings call transcript","url":"https://www.fool.com/earnings/call-transcripts/2026/05/06/uber-uber-q1-2026-earnings-call-transcript/","excerpt":"Uber One Membership -- Surpassed 50 million members, growing 50% year over year, now accounting for over 50% of bookings. Driver and Courier Base -- Exceeded 10 million globally, marking an expansion of platform earner opportunities. Autonomous Partnerships -- Now over 30 global partners;","as_of":"2026-05-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Uber 2026-11-04 發布 Q3 2026 結果；Q4 guidance：Gross Bookings $63.25–65.25B（constant currency +18–22% YoY）、Adjusted EBITDA $3.13–3.23B、non-GAAP EPS $0.95–0.99。","source":"Uber Q3 2026 earnings press release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001543151/000154315126000039/uberq326earningspressrelea.htm","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026 non-GAAP EPS $0.88 低於共識 $0.90（差 2.54%），營收 $14.77B 高於預期 0.63%；EPS 落差與股權投資重估虧損 $476M 有關。","source":"Zacks: Uber Q3 earnings miss estimates on investment loss, revenue beat","url":"https://www.zacks.com/stock/news/3023392/uber-q3-earnings-miss-estimates-on-investment-loss-revenue-beat","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價共識（2026-09 中快照）：MarketBeat 平均 $103.03、Moderate Buy；Financhill $101.11（54 位）；MarketScreener $101.21。Stockanalysis 較早快照 $107.79（33 位），區間 $75–$150。未找到 Q3 後（11 月）更新的共識目標價；各來源 as-of 與分析師家數不一致。","source":"MarketBeat / Financhill / MarketScreener / Stockanalysis 聚合（經搜尋彙整）","url":"https://stockanalysis.com/stocks/uber/forecast/","excerpt":null,"as_of":"2026-09-15","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 earnings summary 與 Q4 guidance 對照","source":"Quartr Q3 2026 summary","url":"https://quartr.com/events/uber-technologies-inc-uber-q3-2026_3PkH0eTw","excerpt":"Q4 Gross Bookings guidance is $63.25B–$65.25B, up 18%–22% YoY in constant currency, including an ~1-point currency headwind to reported growth. Q4 Adjusted EBITDA guidance is $3.13B–$3.23B;","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 共識評等 Moderate Buy 與平均目標價","source":"MarketBeat consensus rating","url":"https://www.marketbeat.com/instant-alerts/uber-technologies-inc-nyseuber-receives-consensus-rating-of-moderate-buy-from-analysts-2026-05-16/","excerpt":null,"as_of":"2026-05-16","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-07-16 Uber 與 Delivery Hero 簽 Business Combination Agreement，以每股 €41.50 現金公開收購 Delivery Hero 全部股份；Delivery Hero 董事會一致通過。","source":"SEC EDGAR 8-K Item 1.01（2026-07-16）","url":"https://www.sec.gov/Archives/edgar/data/1543151/000155278126000382/e26302_uber-8k.htm","excerpt":"On July 16, 2026, Uber Technologies, Inc. (the “Company” or “Uber”) entered into a Business Combination Agreement (the “BCA”), by and among, the Company, Uber International Technologies II Corporation, a Delaware corporation and a wholly-owned subsidiary of the Company (the “Bidder”), and Delivery Hero SE","as_of":"2026-07-16","retrieved_at":"20261108","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-08-06 Uber 簽 Term Loan Credit Agreement 為 Delivery Hero 收購融資，並將 Bridge Credit Agreement 承諾額度減少 €4,000,000,000。","source":"SEC EDGAR 8-K Item 1.01（2026-08-07）","url":"https://www.sec.gov/Archives/edgar/data/1543151/000155278126000414/e26328_uber-8k.htm","excerpt":"The entry into the Term Loan Credit Agreement reduced the commitments under the Bridge Credit Agreement (as defined below) by €4,000,000,000.","as_of":"2026-08-07","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-09-15 Uber 完成 €4.5 億級以上歐元優先無擔保票據公開發行（五檔合計 €4,500,000,000）。","source":"SEC EDGAR 8-K Item 8.01（2026-09-15）","url":"https://www.sec.gov/Archives/edgar/data/1543151/000155278126000486/e26383_uber-8k.htm","excerpt":"On September 15, 2026, Uber Technologies, Inc. (the “Company”) completed a registered public offering of €750,000,000 aggregate principal amount of the Company’s 3.750% Senior Notes due 2029","as_of":"2026-09-15","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露公司涉多項訴訟與政府調查，含集體訴訟（如澳洲計程車業集體訴訟已和解、無承認責任）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"These include individual, multiple plaintiff, and putative class and class action claims for alleged violation of laws related to, among other things, transportation, competition, advertising, consumer protection, fee calculations, personal injuries, privacy, intellectual property, product liability, discrimination, safety, and employment.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-07-16 Uber 簽 BCA，以每股 €41.50 現金公開收購 Delivery Hero 全部股份。","source":"SEC EDGAR 8-K Item 1.01（2026-07-16）","url":"https://www.sec.gov/Archives/edgar/data/1543151/000155278126000382/e26302_uber-8k.htm","excerpt":"for cash consideration per Delivery Hero Share of €41.50 (the “Offer”).","as_of":"2026-07-16","retrieved_at":"20261108","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"搜尋摘要稱預計交割在 2027 下半年，需反壟斷核准；Delivery Hero 同意把 14 市場業務售予 SSW Partners 約 €1.4 億級（摘要數字不一致）。","source":"WebSearch 彙整（Inside Retail / Khaleej Times 等，2026-07）","url":"https://insideretail.asia/2026/07/17/what-will-uber-gain-from-buying-delivery-hero/","excerpt":null,"as_of":"2026-07-17","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K FY2025 揭露多項個人、多原告及集體訴訟；Item 3 稱除 Note 14 所述外，預期無重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm","excerpt":"We are a party to various legal actions and government investigations, and similar or other actions could be brought against us in the future.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"FTC 2025-04 起訴 Uber One 訂閱計費與取消做法，2025-12 修正起訴有 21 州＋DC 加入；搜尋未見 2026 已提起的證券集體訴訟，僅有原告律所調查公告（Portnoy，2026-03-03）。","source":"WebSearch（FTC Release 轉載、Portnoy Law Firm 公告）","url":"https://www.itiger.com/news/2601395368","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"搜尋未見 Uber 自身 2026 產品召回；NHTSA 於 2026-05-08 調查 Uber 自駕夥伴 Avride（Dallas 16 起 robotaxi 事故），屬調查而非召回。","source":"WebSearch 結果摘要（NHTSA / Avride）","url":null,"excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"UBER","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.21,"operating_margin_pct":12.44,"fcf_margin_pct":18.44,"rd_intensity_pct":7.35},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"DASH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":51.91,"operating_margin_pct":5.55,"fcf_margin_pct":12.91,"rd_intensity_pct":10.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"LYFT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.52,"operating_margin_pct":-1.77,"fcf_margin_pct":16.43,"rd_intensity_pct":6.98},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LYFT","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"GRAB","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.45,"operating_margin_pct":10.95,"fcf_margin_pct":-0.45,"rd_intensity_pct":10.4},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GRAB","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"BKNG","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":32.78,"fcf_margin_pct":32.84,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BKNG","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"UBER"},"financial_history":{"ticker":"UBER","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":31877000000.0,"revenue_yoy_pct":null,"gross_margin_pct":38.33,"operating_margin_pct":-5.75,"net_income":-9141000000.0,"diluted_eps":-4.65,"free_cash_flow":390000000.0,"fcf_margin_pct":1.22,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":37281000000.0,"revenue_yoy_pct":16.95,"gross_margin_pct":39.76,"operating_margin_pct":2.98,"net_income":1887000000.0,"diluted_eps":0.87,"free_cash_flow":3362000000.0,"fcf_margin_pct":9.02,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":43978000000.0,"revenue_yoy_pct":17.96,"gross_margin_pct":39.4,"operating_margin_pct":6.36,"net_income":9856000000.0,"diluted_eps":4.56,"free_cash_flow":6895000000.0,"fcf_margin_pct":15.68,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":52017000000.0,"revenue_yoy_pct":18.28,"gross_margin_pct":39.75,"operating_margin_pct":10.7,"net_income":10053000000.0,"diluted_eps":4.73,"free_cash_flow":9763000000.0,"fcf_margin_pct":18.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/UBER/UBER_Q3_2026_Earnings_Call_20261104.md）

# Q3 2026 Earnings Call
**Uber Technologies, Inc.** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Hello, and welcome to Uber's Q3 2026 Earnings Conference Call. [Operator Instructions] I would now like to turn the conference over to Alax Wang, Head of Investor Relations. You may begin.

**Alaxandar Wang** (Executives):
Thank you, Sarah. Thank you for joining us today, and welcome to Uber's Third Quarter 2026 Earnings Presentation. On the call today, we have Uber's CEO, Dara Khosrowshahi; and CFO, Balaji Krishnamurthy.
During today's call, we'll present both GAAP and non-GAAP financial measures. Additional disclosures regarding these non-GAAP measures, including a reconciliation of GAAP to non-GAAP measures, are included in the press release, supplemental slides and our filings with the SEC, each of which is posted to investor.uber.com. Certain statements in this presentation and on this call are forward-looking statements. You should not place undue reliance on forward-looking statements. Actual results may differ materially from these forward-looking statements, and we do not undertake any obligation to update any forward-looking statements we make today, except as required by law.
For more information about factors that may cause actual results to differ materially from forward-looking statements, please refer to the press release we issued today, as well as risks and uncertainties described in our most recent Form 10-K and in other filings made with the SEC. We published our quarterly earnings press release, prepared remarks and supplemental slides to our Investor Relations website earlier today, and we ask you to review those documents if you haven't already. We will open up the call to questions following brief opening remarks from Dara. With that, let me hand it over to Dara.

**Dara Khosrowshahi** (Executives):
Thanks, Alax. Q3 was another strong quarter of growth and expanding profitability for Uber, with record audience and engagement across our platform. We reached 215 million monthly active platform consumers who are using Uber more frequently than ever. That helped us deliver our fifth consecutive quarter of 20-plus percent year-over-year gross bookings growth, alongside 35% growth in non-GAAP EPS and record trailing 12-month free cash flow of $10.4 billion.
Mobility continued to see healthy growth but came in below our expectations as a result of driver supply not keeping pace with strong consumer demand in several international markets. We're responding with targeted investments to improve driver availability and marketplace balance, and we saw encouraging improvement in October. Our focus is on driving consistent growth while maintaining strong profitability of the business.
Delivery had another excellent quarter, with gross bookings up 23% year-over-year and organic growth accelerating. Our investments in selection, affordability and reliability are making Uber Eats even more useful for everyday occasions, from restaurant meals to weekly groceries and last-minute essentials. And with approximately 55 million Uber One members, we're deepening consumer relationships across both Mobility and Delivery. Those direct consumer relationships are central to our approach to AI. We're using AI to make everyday transactions simpler and discovery more personalized while selectively exploring new distribution channels that can bring incremental demand.
In AVs, our focus is shifting from partnerships and testing to driverless commercial service. We're excited for Zoox to launch on Uber in Las Vegas later this month, with Motional moving up to fully driverless operations soon thereafter. We expect approximately 700 fully driverless vehicles on Uber by year-end and more than 2,000 by the end of 2027. Just as importantly, we're focused on demonstrating utilization and economics that are needed to scale. As we enter Q4, our priorities are clear: improve Mobility supply, build on Delivery's momentum and deliver against our AV milestones, all while continuing to grow profitably.
Before I hand it off to the operator, I did also want to offer a special thanks to Jill Hazelbaker, our President and Chief Corporate Affairs Officer. After 10 years here at Uber, she's moving on to OpenAI. It's a big win for them. It's a loss for us to lose someone like Jill. She's been such a big part of our culture, our company. But fortunately, she has built a great team who get to step up to more senior positions, many of them working with me directly.
So I want to personally thank Jill for her 10 years here. She's helped me in innumerable ways, both professionally and personally as well. She's been a great adviser. It's a big win for OpenAI. And I'm really glad that the team that she built is ready to step up to bigger positions, which they fully deserve at the company. So big thank you to Jill. And with that, I will turn it over to the operator for questions.

**Operator** (Operator):
Your first question comes from the line of Eric Sheridan with Goldman Sachs.

**Eric Sheridan** (Analysts):
I want to come back to the parts of the letter and prepared remarks around AV fleet financing. Can you go a little bit deeper in terms of how we should be thinking about the balance sheet and incremental free cash flows that you want to put behind these efforts? And how should we be thinking about rates of return or aligning the economics with the commercial opportunity?

**Balaji Krishnamurthy** (Executives):
Thanks, Eric. I can take this. So I think we aren't ready to say a lot on the structures that we are working on just yet. But what I would point you to is the $1 billion financing arrangement that we had set up with Santander earlier in the year that was focused on our traditional fleet partners. That is a template for what we could be doing with our AV fleets as we go through the next few months. We are actively working on these kinds of setups. And specifically, you should expect that we will have announcements to make both on infrastructure financing, but also on vehicle financing as we go forward.
So our long-run expectation is that this should be financed by third-party capital, not by Uber's balance sheet. And in the near term, as you've seen with the announcement that we had in the release that we will have about 700 driverless vehicles on our network this year, 2,000 by the end of next year, the capital deployment against those is fairly limited. But as we start scaling out into the 10,000-plus territory in 2028 and beyond, we want to bring in third-party capital against that, and we feel good about the ROI that the third parties can get there.

**Dara Khosrowshahi** (Executives):
And Eric, just a little bit more from me, which is, we do think that fleet financing for these cars is going to be somewhat unusual in that if you look at like fleet financing for rental car fleets, et cetera, they're all based on residual value of vehicles. And I think the residual value of AV vehicles isn't established yet. And so as a result, in the early days, we're going to take these vehicles on our balance sheet. We have a very strong balance sheet, are capable of doing so.
And I think a lot of the fleet financing is going to be based on revenue -- kind of revenue potential of these fleets. And what we're able to demonstrate is that cars on our network get very, very high utilization, and actually higher utilization [ on ] cars that aren't on our network. We show a 30% kind of utilization premium on our network, and we're able to do so very flexibly. So if there's a fleet that, for some reason, fails in terms of their operations, we can take that AV vehicle and put it under separate ownership, and it will still earn on the Uber network, so to speak.
So we think that the financing on the Uber network can have a real advantage in terms of cost of capital versus alternatives, and it is kind of a business model that we're working with to establish with partners. The reaction has been, actually, they're quite interested. They want to diversify away from data centers, so to speak. So we're quite optimistic on it, but we do have to establish kind of the business model, the utilization advantages, demonstrate that to the banks and then go from there.

**Operator** (Operator):
Your next question comes from Nikhil Devnani with Bernstein.

**Nikhil Devnani** (Analysts):
I wanted to follow up on the international supply dynamic you called out. Just want to make sure, did something sort of change through the quarter? I think last time we had talked about Brazil, but it seems like there's a few more markets that are now reflecting this. So if you could just elaborate on what you saw through the quarter, that would be helpful.
And then also, as we look forward, how should we be thinking about the supply side investments required? Because some of the variables called out, like immigration, feel a little bit more persistent. So it would be helpful to understand just the degree and persistence of these investments as you try and reaccelerate the business.

**Balaji Krishnamurthy** (Executives):
Yes. Thank you, Nikhil. So I think what I would say is, a lot of this is a continuation of the dynamics that we have seen through the year. And if you zoom out and look at the macro environment, with the escalation in the war in the Middle East, fuel cost impacts have been felt globally. Where it shows up most materially for us is in emerging markets, where there is a level of price sensitivity on both the consumer and the driver side. And what we talked about last quarter in Brazil was specifically focused on Moto supply from delivery competition in the market. But through the last quarter, we have seen the elevated fuel price impact in markets like Brazil and India, in particular, quite meaningfully impacting the supply situation.
Similarly, the immigration dynamics have been in place through the year. But as we go through the back half of the year and we see elevated demand from the holiday season that you have coming through right now, which, again, the demand picture is pretty strong, we see an elevated impact on the supply -- on the marketplace when the supply is short. So that's kind of what we're calling out in Canada as well.
Now this is a good problem, where we are at the scale that we are operating at, and we still are running into supply constraints rather than demand constraints. And we know exactly how to address those kinds of challenges with the history that we have demonstrated. We're making targeted supply investments, so this is focused on driver acquisition, retention and engagement. And as we go through that kind of investment, we are already encouraged with the early signs of supply improvement we saw in October and supply hours growth globally accelerated in October, including notable improvements in Brazil and India.
So I think with all of that, you see our outlook, which is steady at the 18% to 22% growth range, which is steady from the last couple of quarters. So we feel good about where we are, and the growth runway in front of us is extremely long. Over the last 5 years, we have doubled our eligible population penetration in our top 10 markets, but it's still at only 10%, right? So we feel really good about where we can go from here.

**Dara Khosrowshahi** (Executives):
I think just the additional factor that we are dealing with is that we obviously have a year-over-year pressure on supply, but then we also have seasonal pressure on supply as well, which is, September, October, November, December are kind of peak season for us, both in Mobility and Delivery. And in some markets like Brazil, Mobility and Delivery depend on 2-wheel supply, which for us is, for example, one of the examples of supply that we need to add. So those kind of intermingle. So it's a seasonal issue and it's a year-on-year issue that are hitting together. But we've got a good handle on it. We're very optimistic about the trends as we see them in October and going into Q4. And again, this is not the first time we have dealt with this kind of situation.

**Operator** (Operator):
Your next question comes from Brian Nowak with Morgan Stanley.

**Brian Nowak** (Analysts):
Maybe one on grocery. Just talk to us a little bit philosophically about the investments you need to make in grocery and retail to sort of further accelerate and compete in that business in the U.S., and how do you think about the need to have a larger 1P presence, so your own dark stores or your own sort of fulfillment operation?

**Dara Khosrowshahi** (Executives):
Yes, absolutely, Brian. So we're very excited about the progress of our grocery and retail business. We're -- run rate now at a $15 billion run rate, growing 40% on a year-on-year basis. We think this is like a $10 trillion TAM, so it's an enormous market for us. And what we see from consumers is, over and over, is they want more stuff faster. They want everything faster. I think when Amazon brought overnight shipping, it was magic. And now next hour shipping is magic, and pretty soon people are going to expect everything in 15 minutes. And we play right into that area.
The areas of investment for us are really about selection, they're about affordability and they're about kind of consumer experience. On the selection side, we're very excited to expand to Costco nationwide. We also have added a number of international players, Target, Decathlon, Priceline in Australia, Tesco in the U.K., REWE in Germany as well. So we continue to invest in selection. And as we add selection, we have more consumers coming online as well and also conversion rates improve. We continue to invest in affordability, whether it's Fresh Tuesdays or, for example, members not having any fees above $60 that our members are loving as well.
And then we continue to invest in product innovation as well to make sure that our pick, pack is as accurate as it can be. Shopper -- we're investing in shopper quality, so we are paying high-quality shoppers more. And we're also introducing technology, for example, where our shoppers will take a photo of an empty shelf to verify that the item that you're looking for isn't there. It also helps our consumers too, because when they see the empty shelf, they don't get upset. It's not the shopper's fault. It's just what they want wasn't there. And so it helps establish trust between both sides of the marketplace. So for us, it's just all about execution.
As it relates to dark stores, our #1 priority has been to work with our partners and to help them grow their businesses. Now we're very excited, as it relates to Delivery Hero, they have built a substantial quick commerce and dark store business. And the benefit of dark stores is that you have a much better handle on inventory. Usually, your pick and pack success percentages, your found rates are much higher. So quality goes up as a result of the vertical integration. And this is a part of the Delivery Hero hopeful potential acquisition that we're very excited about. That team has been building their quick commerce business for well over 7, 8 years. It is -- it hit breakeven. It is growing at very attractive rates, and we're very excited to add that as part of our portfolio once we close on Delivery Hero.

**Balaji Krishnamurthy** (Executives):
And just one additional comment on the dark store question. This is, for us, a fit-for-purpose sort of solution, right? We will not -- we don't want to get into this business everywhere, but there are markets where it makes sense. As Dara mentioned, Delivery Hero has done a really good job with their dark store footprint in the Middle East. We are also in a position where we would be able to look at that business in Türkiye, both with our existing presence in the market, but also with the Getir transaction that we have done. 
And that business, again, is running near profitability, and then we have organically experimented with this in Taiwan as well. So ultimately, it needs to be a business that can be run well, has to meet the market conditions and has to have a good return on assets when you go into that sort of a field. So we'll be selective in where we engage with this. Otherwise, we will work with our grocery partners who are experts at doing that in their own space.

**Operator** (Operator):
Your next question comes from Ron Josey of Citi.

**Ronald Josey** (Analysts):
I want to ask a little bit more about the fully driverless rollout from 700 this year to 2,000 next year. Just help us understand a little bit on the geography pace of rollout. I think you said 50-50 in the U.S. and international, and how you're thinking about that.

**Dara Khosrowshahi** (Executives):
Yes, absolutely. So we're very excited. I mean we've got launches. Obviously, we're in market with Waymo already in the U.S. We're in market with WeRide and Baidu with no drivers in a number of international markets. We expect to launch Zoox and Motional, as we mentioned, in Vegas this year. And then next year, we expect to add Nuro in California and then in Houston as well in Texas, at least early on in 2027. These are fully driverless commercial rides, and Avride middle of the year in Texas as well. And internationally, we expect to add Pony and Momenta to our no vehicle operator kind of inventory.
In late '27, I do think we are going to be doing kind of testing rides -- vehicle operator testing rides with NVIDIA, with Rivian, hopefully with Waabi as well, and also Wayve outside of the U.S. So there's going to -- the partner strategy and the panoply of all these partners are really going to start adding up, and we're quite confident of getting to the 2,000 vehicles in 2027. But the real goal is to get to tens of thousand vehicles -- tens of thousands of vehicles in '28 and beyond, and really scaling the ecosystem.
And we are in market in these markets. We have relationships with the cities. We have operations in those markets. We don't have to build demand. The demand is already there. So we think we can launch very quickly at very high utilizations for our partners, which makes us even more optimistic about the opportunity here.

**Operator** (Operator):
Your next question comes from Shweta Khajuria with Wolfe Research.

**Shweta Khajuria** (Analysts):
Can you hear me?

**Dara Khosrowshahi** (Executives):
We can.

**Shweta Khajuria** (Analysts):
Let me try 2, please. The first is on AV unit economics. So in the illustrative example that you gave, 30% increase in paid trips with a 23% decrease in fixed costs. And even if partners were to pay the transaction fee or take rate to Uber, that would still be additive to them. So my question is, how durable is that 30% increase in paid trips that you would add? How durable is that advantage as you think long term in AV?
And then the second question I have is on just your capital allocation strategy. You talked about that in your letter. There's no change there in terms of your priorities, and you don't expect M&A -- further M&A until the year-end or after. But I guess, how are you -- what was the rationale for ezCater? How are you thinking about capital allocation in general when you think about Mobility and Delivery as well as AV going forward?

**Balaji Krishnamurthy** (Executives):
Sure. Thanks, Shweta. I'll take the first one. Dara is going to jump in on the second one. So on the utilization lift, I would start by saying we believe it's a very durable advantage for Uber. And maybe just for context, when we are talking about the 30% lift here, we are comparing Uber's deployments on a hybrid basis in the U.S. with mature 1P deployments, right? And these mature 1P deployments have the advantage of mix in that they include San Francisco, which is a uniquely favorable market for AV deployments today.
As that deployment scale broadens out, we expect that 1P deployments will likely have utilization that will be worse than what they're seeing in San Francisco. And in fact, what you're seeing on the ground today is exactly that. Both for Waymo and Tesla, their trips per vehicle per day in the new markets that they have launched this year is in the low teens versus high 20s that we are seeing on our network in these hybrid markets. And effectively, you're looking at 100% plus utilization for us in those markets.
I think the other part of this is we are also going to likely have advantages on additional pieces of the unit economics pie. First, the vehicle costs over time are going to come down, and that will be true for many players. But in general, what we are trying to ensure here is that as we work with OEMs, we want to ensure that we have line of sight to advantaged pricing that we can deliver because we have scale.
Second piece that we will have advantage on also is on shared charging, maintenance and fleet infrastructure, since that can be shared across multiple AV partners. And I would think about this as the hyperscalers getting advantage versus on-prem data centers that were serving one corporate. So I think those 2 pieces, in addition to the utilization, will support long-term economics. Our goal is for AV trips to deliver margins comparable to human-driven trips over time. And as we get beyond that kind of point, we can share savings with consumers and truly expand TAM beyond what we are already seeing on the ground.

**Dara Khosrowshahi** (Executives):
Great. And in terms of capital allocation, et cetera, our priorities haven't changed. Obviously, our #1 priority is to drive organic growth. Investment in the AV ecosystem, we talked about a $10 billion commitment based on certain deliverables, both an investment in partners and/or AV fleets, et cetera. That's another priority. And then there's M&A and buybacks as well, and we have plenty of capital for both. We are going to shift to, I would say, more of the top 2, and we're going to pull back on M&A chiefly because we're really focused on integration of the deals that we've already announced. Generally, they're performing great, but we want to make sure we get the right cost of capital as it relates to M&A.
And if you look at kind of our M&A philosophy historically and going forward, it's really in a couple categories. One, you'll see deals that expand our geographies, right? They allow us to offer our services in more countries. Delivery Hero is an example of that. Trendyol Go is an example of that. And not only do we get into new geographies that are growing very, very fast, but it allows us to offer the platform advantage, the power of the platform, which is Mobility and Delivery cross-promoting each other, membership programs cross-promoting each other in more countries. So we're in many, many of the Delivery Hero markets, we're in many, many of the Delivery Hero markets, and it's just the extension of our platform geographically.
The second area we look at are, what are capabilities that we can build that are specialized and we think really profitable? We talked about our premium business growing. And we've talked, for example, it's grown 35% year-on-year, and our U4B business grew almost 50% year-on-year. So premium as a theme for us and corporate business as a theme for us is something that we want to kind of double down on. And those, for example, are the acquisitions of Blacklane and ezCater that you asked about.
Blacklane gives us more specialty, very high quality inventory, and ezCater have specialized capabilities. They only work with merchant partners who focus on catering. A lot of times, the delivery partner has to come into the office, set things up. It's a different level of service, and there's a huge advantage in being able to offer both Blacklane and ezCater to our U4B audience, which I think now we've got like half of Fortune 500 companies now as well. So those are established businesses, different capabilities that we can introduce our U4B audience and really embed with them even more.
And then third is kind of new products that can grow with our audience. So SpotHero is an example of that. We want our product to be more relevant, for example, to commuters. Commute is one of our largest categories. And to be able to offer commuters an Uber to work, a path to avoid surge and parking if they want it when they want to drive is a great, for example, example for us building out our inventory of services to the commuter, who is a top customer for us. So those are the themes that we're going after. We're really excited about the acquisitions that we have on our books. We're very excited about ezCater. And generally, as standalones, they are operating at higher levels than our deal cases. And now we just want to make sure that the integration is right, the teams are treated well, and everything goes well, which is why next year, I think the focus is going to be more on organic, autonomous, and then, of course, buying back stock opportunistically.

**Balaji Krishnamurthy** (Executives):
I'd just add that from a process standpoint, for any deal that you see us do, we are always evaluating the build versus buy case, and we are looking at the accretion math relative to what it would look like if we just bought back our own stock. In this specific case, since you asked specifically about ezCater, the build versus buy math could not be more obvious. We are talking about acquiring a business that is profitable right now. We have more synergies coming, and relative to building this business, we expect that you would see a few hundred million dollars of profit swing in the build case versus buy. So I think we feel very good about the deal logic, and we now are focused on executing against it.

**Operator** (Operator):
Your next question comes from Michael Morton with MoffettNathanson.

**Michael Morton** (Analysts):
I wanted to maybe talk about the potential combination of DoorDash and Instacart. Uber has talked a lot about the cross-platform success you've experienced from your Eats to your Mobility business. So I was wondering if you could talk about the potential opportunity and/or risk that you see created by this combination.

**Dara Khosrowshahi** (Executives):
Yes, absolutely. So I don't think, honestly, Michael, it's going to affect us too much. Our grocery and retail business is growing. It's a $15 billion run rate, growing 40%. Our focus really is to continue to improve the product, and the product still has a lot of improvement ahead of it in terms of selection, in terms of quality, in terms of on-time rate, in terms of fill rates, et cetera. When we talk to our merchant partners, they want choice. They want to develop direct channels. They want plenty of partners, including us and DoorDash and Instacart, to work with. So this potential deal takes one of those partners off the table, and we've already had kind of reach outs from our partners, both who are very worried about the potential transaction and asking us, "What do you think?"
And then two, wanting to actually work with us more, wanting to build their business with us so that they are not overly dependent on a single platform if DoorDash and Instacart happens, which will be a very, very large percentage of the online market. But from our standpoint, the promise of this market, it's a $10 trillion market. This would create a competitor that has a big share of certainly the online portion of that market. But we think for us, we're going to continue to invest in. And these acquisitions create a lot of distractions. And at this point, the reach outs we've gotten from merchants are merchants who want to embed with us more deeply and want to build their business with us so that they have alternatives. And it's going to be up to the government to decide whether 3 alternatives or 2 alternatives is better.

**Operator** (Operator):
Your next question comes from Ken Gawrelski with Wells Fargo.

**Kenneth Gawrelski** (Analysts):
Two, if I may, please. First, could you talk about domestic or U.S. Mobility trends? Maybe what you saw in 3Q and into 4Q. You talked about improving Mobility growth, but I want to see if we can touch a little bit upon what you're seeing in the U.S. versus some of the international markets you've talked about. And in particular, I think there's a market focus on -- continued on California, but maybe even in some markets in Texas where there's been heavier AV penetration.
And the second question is, you talked about organic Delivery acceleration. Could you talk about the drivers between kind of restaurants and grocery? Are you seeing core restaurant acceleration as part of that overall organic acceleration?

**Balaji Krishnamurthy** (Executives):
Yes. Thanks, Ken. On the U.S. for Mobility, we are seeing a relatively resilient growth in the U.S. versus the international trends we talked about earlier in the call. Growth moderated a bit in Q3, but not as much as in the international markets. Elevated gas prices are an issue globally, and there is some level of supply pressure that we're seeing in the U.S. as well, but we are responding with the targeted investment -- supply investments that we talked about earlier. I think beyond the supply question, what we are seeing in the U.S. that continues to be true is the insurance tailwinds continue to build. We talked about the meaningful acceleration in California trip growth. They continue to outperform relative to the rest of the country.
Two, our barbell strategy on the product side continues to be really, really healthy in the U.S. U.S. barbell products grew at 3x the rate of the overall business in Q3, and it's driven by strong innovation in our Growth Bets portfolio, including Wait & Save, Comfort, Reserve Black, but then also expanding to new demographics with teens and women preferences that are targeting just new cohorts of consumers and creating more options for our consumer base.
And then finally, from a sparse market standpoint, we just see so much runway in the U.S. Less than 10% of eligible consumers in sparse markets have used Uber in the last 12 months. That number in dense markets is 50% of consumers. So we continue to make improvements on supply and reliability in these markets, and that should have long-term impacts that are very favorable. Dara, do you want to take the second one?

**Dara Khosrowshahi** (Executives):
Yes. And we're quite pleased in terms of U.S. Delivery, which accelerated nicely. It's the second quarter in a row that organic growth in Delivery, in U.S. Delivery accelerated. And really, it's for a number of factors. One is mathematically, our grocery and retail business and direct business, which are growing faster than our OFD business, are becoming a higher percentage of the portfolio, so to speak. So you just have kind of a bigger, faster-growing part of the business getting even larger. Our core restaurant business is also accelerating, and that is because of really merchant selection. The number of merchants that we added in the U.S. was up nicely, about 12% on a year-on-year basis. So as we add more selection, everything helps, conversion improves, we get new customers on the platform as well.
Membership is definitely a tailwind for us. So members are now 70% of Delivery gross bookings. So membership is deepening in engagement with our consumers as well. And then, of course, sparse markets. As Balaji said, sparse markets is a play that we're running globally, but it's absolutely a play that we're running in the U.S. as well for Delivery. That helps.
And then last but not least is really deals. We are focused on kind of merchant-funded promotions in addition to the membership discounts that we give to our consumers. If you look at our ad business and merchant-funded promotions, they grew to over $10 billion on a year-on-year basis. And these are dollars that we're giving to our consumers, and the return for merchants is new consumers and kind of higher penetration in the marketplace. So all of it is working at this point. 
If there's one issue, it runs with Mobility in that we continue to invest in Delivery, in couriers, to make sure that kind of our courier growth keeps up with the consumer demand that we're seeing on the food side. That is right now the biggest challenge that we've got, but the team, we think, is more than up for it.

**Operator** (Operator):
Your next question comes from Mark Mahaney with Evercore.

**Mark Stephen Mahaney** (Analysts):
I just want to ask one question on the profitability of the Mobility segment, these 8% margins you had this last quarter. With the supply initiatives that you're introducing in international markets, does that -- can you maintain the profitability performance that you've had? Or is it -- do we have a detour? Is it structural? Or is it a temporary detour? Or is there any detour just in those profit margins?

**Balaji Krishnamurthy** (Executives):
Yes, Mark, I think I would just take you back to our philosophy as always, which is that we want to drive margin expansion for the total company on a year-on-year basis. And ideally, we want to do the same for the segments as well. But on a quarterly basis, there is some variability in the business, both from just the investments we typically make in supply in holiday season, et cetera. So I don't -- I wouldn't call out any kind of meaningful changes in the margin trajectory for the business. 
And we would have some color on just the Q4 supply investments for Mobility that would have an impact on take rate, but not necessarily from a margin standpoint, anything meaningful. Look, I think the final point I'd make here is on profitability we are -- if you look at our outlook, we delivered a quarter of mid-30% EPS growth. The Q4 outlook that we just provided at the midpoint is a 37% year-on-year growth on our non-GAAP EPS. So if anything, you're seeing the profit ramp expand, and that puts us in a pretty good spot for 2027.

**Dara Khosrowshahi** (Executives):
And Mark, just a little bit more so you understand the picture in terms of supply and demand. We have base pricing for both kind of our consumer pricing and then base pricing for driver, courier pay, et cetera. Then we have incentives, and there are kind of, call it, rider side incentives, driver side incentives, eater side incentives and then kind of courier incentives as well. These are more flexible dollars that we target times, like Halloween, make sure drivers show up, et cetera, or we'll target places. If we think that there's a ball game going on, we'll put incentives for drivers to show up to the ball game at the right time. But the cool thing is that we just rebalance incentives between riders and drivers, for example, in this case. And so whereas last year, more of the incentives went to riders to reduce price.
Now this year, we're taking down rider incentives, and we're using those dollars to fund driver incentives. Now that does mean sometimes higher prices for riders, which is something that we watch out for. We will do trade-offs against profitability, but that's something that we handle. But there is a flexible incentive pool that we allocate to supply or demand based on the balance of the marketplace, and that's part of kind of the art that we've got and then there's a lot of science, algorithmic science that goes into, hey, if you have a dollar, what is the maximum predicted return for that dollar? And should I invest that dollar in a driver in Brazil? Or should I invest that dollar in a rider in India, for example? And the algorithms are making these choices, and they structurally can make these choices based on training on billions of trips, and they can allocate these investments in a way that humans just can't.

**Operator** (Operator):
Your last question will come from Doug Anmuth with JPMorgan.

**Douglas Anmuth** (Analysts):
Dara, I was hoping to get your latest thoughts on AI agents. Can you just talk about some of the goals and differentiation that you can provide by building agentic directly into the Uber platform? And then also how you're thinking about the opportunities on third-party platforms like Muse and others?

**Dara Khosrowshahi** (Executives):
Yes, definitely. So Doug, I think our focus is making sure that we invest for the best possible experience if you come direct. It's price, your delivery time, reliability, selection. Obviously, we have membership benefits, and members now account for more than 50% of our bookings. It just builds the best experience when you come direct. And we're really focused on making sure that the direct app experience is already frictionless, right?
So like the mean ride time booking is less than a minute. It's actually 50 seconds. That's how much time people spend on our app, and 75% of our rides are a single tap based on personalizing your destination based on the data that we have on you. Our mean -- if you look at the median time for an eater to reorder their favorite food, it's only 90 seconds. So we make sure that kind of coming to Uber doesn't require a bunch of toil. You can get in, you can get out. And because of the data that we have, where you're going, when you're going there, et cetera, we think we're going to have a ton of people come direct to our site.
And listen, I used to work in the travel business where we were dependent on the Googles of the world. I don't want to go back there. So really kind of the best-in-class marketplace technology that we're building, operational execution, I think is going to have more and more people coming direct to us. And we are building our own AI experiences. For example, we have a Cart Assistant, which we're very excited about, and early signal shows that baskets that you build with a Cart Assistant are roughly twice the average of the average basket as well, and we're working on kind of Eats Assistant, Driver Assistant, et cetera, to make sure that AI -- kind of we have the best AI assistant that can get you in and out of our services very, very quickly.
That said, we will have discussions with kind of third-party AI agents. We think that it's another opportunity to reach our platform. We think it'll be a net positive in terms of demand into the ecosystem. And you can guess based on kind of our services, there are a lot of -- every single AI assistant company is talking to us, and we're really now negotiating the terms of trade. And the good news here is, in most markets, you have 2 Mobility -- big Mobility providers, 2 big Delivery providers. I think I've counted now there are 8 different assistants, and I think there'll be more than 10 assistants.
So I think the content players in our space, in the physical space, where kind of the fulfillment, the demands on the services that we build are very large. I think the demands on our services are going to be very, very high. So something we're really excited about now, it's pretty small. Balaji, I think you were telling me AI, what are the transaction volumes at this point?

**Balaji Krishnamurthy** (Executives):
Yes. So I think just to put numbers to it, we had our -- one of our largest weeks last week because it was Halloween. So we did just around 320 million trips on Uber and Uber Eats. The volumes coming from AI agents for Uber Eats were around 500 orders total. And for our rides business, it was a grand total of 4 trips that we fulfilled from agents. So it's very, very early and very limited traction that we've seen so far.

**Dara Khosrowshahi** (Executives):
Yes. Listen, we hope that there will be more traction. Like we do think that we want to make services that are available to consumers in a delightful, easy way. We think our direct services are going to be the most delightful and easy, but we will work with these third parties. It's just very, very early. And we want to make sure we're not dependent on any one player. And I think we're very well positioned to -- in this environment going forward.
All right. Well, I think that's it. Thank you, everyone, for joining. Thank you, Uber team, for everything that you've done to deliver a great quarter. We're excited to close out the year, hopefully with a really, really strong quarter. And a big thank you to our investors and our owners who put their dollars and faith in us as a company. More to come. Thank you.

**Operator** (Operator):
This concludes today's conference call. Thank you for joining. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### UBER_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜Balaji Krishnamurthy｜guidance：CFO重申美國全年逐季加速的預期（原話："we expect the U.S. to accelerate through this year."）
- 2026-08-05｜Balaji Krishnamurthy｜guidance：CFO稱對下半年維持原預期（原話："We continue to hold our expectation for the remainder"）
- 2026-08-05｜Dara Khosrowshahi｜guidance：CEO給AV上線城市目標：年底15個市場（原話："We'll be in 15 markets by the end of the year."）
- 2026-08-05｜Balaji Krishnamurthy｜guidance：CFO談Q3外送：Turkey併購交接對報告成長為淨逆風（原話："it is a headwind to Delivery reported growth"）
- 2026-08-05｜Balaji Krishnamurthy｜guidance：CFO稱Q3外送有機成長加速（原話："our organic Delivery business is accelerating quite nicely"）
- 2026-08-05｜Dara Khosrowshahi｜margin：CEO報Q2總預訂量成長與規模（原話："bookings grew 22% year-on-year to more than $58 billion"）
- 2026-08-05｜Dara Khosrowshahi｜margin：CEO報TTM自由現金流首度超過100億美元（原話："trailing 12-month free cash flow exceeding $10 billion"）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO拆解Mobility收入take rate降幅（原話："nearly 500 basis points decline year-on-year"）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO稱其中約400bp為英國商業模式變更的帳面影響（原話："it's an optical impact."）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO報Mobility營業利益率（原話："operating income margin remains very strong at 7.6% as well"）
- 2026-08-05｜Dara Khosrowshahi｜margin：CEO稱巴西二輪車業務利潤低、未衝擊獲利但影響趟次（原話："it's certainly not hitting the bottom line"）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO稱AI與組織精簡使人力增速放緩，部分組織減編10-20%（原話："headcount by about 10% to 20%"）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO稱工程師程式產出倍增（原話："a doubling in the code output per engineer"）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO稱巴西外送競爭（DiDi Food、Meituan）新增（原話："DiDi has introduced DiDi Food."）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO稱巴西份額持平、流量由Mobility移向Delivery（原話："we continue to hold our share in Brazil"）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO談Waymo：不想依賴單一夥伴（原話："we're not dependent on one partner."）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO稱Austin與Atlanta明年續營運（原話："We believe we'll continue to operate next year"）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO稱AV目前占總趟次比重（原話："even less than 0.5% of our overall trip volume"）
- 2026-08-05｜Balaji Krishnamurthy｜competition：CFO稱美國AV運營城市外仍是主要成長與獲利來源（原話："Only 30% of our U.S. gross bookings and 25% of our profits"）
- 2026-08-05｜Dara Khosrowshahi｜product：CEO談AV單車使用率（原話："often mid- to high 20s, low 30s in terms"）
- 2026-08-05｜Dara Khosrowshahi｜product：CEO談AV Labs：自建數百輛蒐集資料（原話："we're building out hundreds of cars"）
- 2026-08-05｜Dara Khosrowshahi｜product：CEO談AI預期：許多小改善而非單一大突破（原話："I wouldn't look for like one giant hit from AI."）
- 2026-08-05｜Balaji Krishnamurthy｜product：CFO談B2B產品U4B成長（原話："U4B, in particular, we saw 40% year-on-year growth"）
- 2026-08-05｜Dara Khosrowshahi｜risk：CEO談AV監管，主張放慢以換取可持續法規（原話："We're very much pro AV"）
- 2026-08-05｜Dara Khosrowshahi｜risk：CEO談Lucid新CEO與合作訂單（原話："it's a big order with kind of guaranteed volume"）
- 2026-08-05｜Balaji Krishnamurthy｜customer：CFO稱美國稀疏市場滲透率低（原話："eligible consumers in our sparse markets have used Uber"）
- 2026-08-05｜Dara Khosrowshahi｜customer：CEO稱跨平台用戶占比（原話："only 20% of our consumers at this point use both Rides and"）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO說明AV投資規模（原話："the $10 billion of AV investments we're talking about here"）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO稱夥伴每1美元獲Uber投資後另募2.5美元（原話："raise an additional $2.50 from other investors."）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO稱Q2因買進Delivery Hero股票轉向併購（原話："We deployed about $4 billion of capital in the second"）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO重申自由現金流約50%用於回購（原話："deploying about 50% of our free cash flows"）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO稱今年已回購約35億美元（原話："bought back about $3.5 billion of our stock this year."）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO給回購恢復時程（原話："I don't think this is a year away."）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO說明Delivery Hero整合時程假設（原話："assuming we close in the second half of 2027"）
- 2026-08-05｜Balaji Krishnamurthy｜commitment：CFO承諾Delivery Hero綜效（原話："we remain committed to delivering the synergies"）
- 2026-08-05｜Balaji Krishnamurthy｜commitment：CFO稱12萬輛車承諾（原話："120,000 vehicle commitments that we are looking to deliver"）
- 2026-08-05｜Balaji Krishnamurthy｜commitment：CFO稱AV投資損益影響之後再揭露（原話："we will give you more visibility into that as"）

### 問答異常語氣（迴避／改口／保留）
- UBER_Q2_2026_Earnings_Call_20260805.md｜問：Justin Post：AV百億美元投資如何流入損益表、對利潤率的影響｜答法：未給數字，稱隨部署逐步提供損益影響的可視度
- UBER_Q2_2026_Earnings_Call_20260805.md｜問：Doug Anmuth：媒體報導Uber與Waymo關係，請釐清｜答法：稱Waymo是重要夥伴、Austin/Atlanta續營運，但未直接回應報導內容，轉談不依賴單一夥伴
- UBER_Q2_2026_Earnings_Call_20260805.md｜問：Mark Mahaney：能否量化AI對消費者轉換與支出的提升｜答法：未給整體量化，只舉cart builder購物車約兩倍與3/4目的地建議等例子，稱不要期待單一大突破

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
{"date":"20260808","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"N/A（裁決為進場，非觀望）","irr_base_pct":16.6,"ev5y_pct":94.3,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"🟠","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.65,"ev5y_pct":94.3,"irr_base_pct":16.6,"max_dd_pct":-58.0,"bull_5y_price":264.0,"bear_5y_price":55.0,"p_bull_pct":20.0,"p_bear_pct":35.0,"rearm_trigger":"N/A（裁決為進場，非觀望）","price_at_dd":74.21,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UBER_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
