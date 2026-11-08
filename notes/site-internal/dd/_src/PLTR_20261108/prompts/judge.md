你是 stock-analyst **v20 判斷 agent**，標的 PLTR（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"PLTR","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLTR_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLTR_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":2313.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司新聞稿 8-K Ex.99.1（SEC 存檔）"},"note":"未查得營收共識"},{"id":"f_kpi1_non_gaap_adjusted_operat","label":"Non-GAAP (adjusted) operating income / margin","value":1426.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD million（利益率 62%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查得共識"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":1084.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD million（利益率 47%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查得共識"},{"id":"f_kpi3_adjusted_free_cash_flow","label":"Adjusted free cash flow","value":1216.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD million（FCF 利益率 53%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查得共識"},{"id":"f_kpi5_guidance_q4_fy2026_fy202","label":"Guidance: Q4 FY2026 與 FY2026","value":"Q4 營收 $2,649–2,653M、Q4 adj. 營業利益 $1,640–1,644M；FY26 營收 $8,530–8,534M、FY26 adj. 營業利益 $5,245–5,249M、FY26 adj. FCF $4.8–5.0B","period":"Q3 FY2026 公告（2026-11-02）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026 公告（2026-11-02）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查得共識"},{"id":"f_kpi6_total_contract_value_tcv","label":"Total contract value (TCV) closed","value":2918,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD million（YoY +6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"不適用"},{"id":"f_kpi7_u_s_commercial_remaining","label":"U.S. commercial remaining deal value","value":6517,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD million（YoY +79%、QoQ +4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-02","period":"2026-11-02","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-02"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_pltr_gross_margin_pct","label":"PLTR 毛利率","value":84.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pltr_operating_margin_pct","label":"PLTR 營業利益率","value":45.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pltr_fcf_margin_pct","label":"PLTR FCF 利潤率","value":55.62,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_snow_gross_margin_pct","label":"SNOW 毛利率","value":67.03,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNOW.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snow_operating_margin_pct","label":"SNOW 營業利益率","value":-22.76,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNOW.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snow_fcf_margin_pct","label":"SNOW FCF 利潤率","value":21.96,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNOW.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_now_gross_margin_pct","label":"NOW 毛利率","value":73.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_now_operating_margin_pct","label":"NOW 營業利益率","value":9.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_now_fcf_margin_pct","label":"NOW FCF 利潤率","value":30.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_crm_gross_margin_pct","label":"CRM 毛利率","value":77.28,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_operating_margin_pct","label":"CRM 營業利益率","value":21.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_fcf_margin_pct","label":"CRM FCF 利潤率","value":34.49,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_ddog_gross_margin_pct","label":"DDOG 毛利率","value":79.58,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ddog_operating_margin_pct","label":"DDOG 營業利益率","value":2.3,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ddog_fcf_margin_pct","label":"DDOG FCF 利潤率","value":25.93,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_gaap","label":"SBC 占營收 / 占 GAAP 營業利益","value":13.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"% of revenue（占 GAAP 營業利益 29.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"新聞稿 SBC $318.889M ÷ 營收 $2,313.411M／GAAP 營業利益 $1,084.845M，自行換算"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":160.38,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":16.39,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":31.17,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.7 → 1.7）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.4,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.48 → 2.49）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.43 → 3.43）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.7,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.49,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.43,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":6.25,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.6 → 1.7（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":112.94,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":53.02,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝51.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":51.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":51.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝50.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":50.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":94.34,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.7，分子＝快照價 160.38","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-10336.26,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 225.27、現金 10561.53（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":2409.5,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":376098.99,"period":"2026-11-08","unit":"USD m","basis":"市值 386435.25 ＋ 淨負債 -10336.26","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":8550.52,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（27 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":13112.15,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（30 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":43.99,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 160.38 / W52 157.3 / W104 139.99 / W250 67.82 / W250 13週斜率 4.07%"},{"id":"f_ma_w52","label":"52 週均線","value":157.3,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":139.99,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":67.82,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":4.07,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 載明公司主要與客戶內部自研軟體競爭，對手包括大型企業軟體商、政府承包商與系統整合商，並有新進與既有公司持續進入此市場。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"We are fundamentally competing with the internal software development efforts of our potential customers.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子警告大型對手可能以搭售、零或負毛利等方式競爭，並可能導致訂單減少、毛利下降與市占流失。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"Increased competition could result in fewer customer orders, price reductions, reduced margins, and loss of market share, any of which could harm our business and results of operations.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Trefis：AI 模型實驗室也想要同樣的企業客戶，既是供應商也是對手；Q2 客戶數字未見影響。","source":"Trefis What Are Palantir Stock Bulls Not Worried About?","url":"https://www.trefis.com/stock/pltr/articles2/617673/what-are-palantir-stock-bulls-not-worried-about/2026-10-06","excerpt":"Those companies want Anthropic and OpenAI to guarantee that the companies’ intellectual property will not be misused. How Much Of Palantir’s Revenue Comes From Companies?","as_of":"2026-10-06","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Barchart：Alphabet 與美國國防部簽署機密協議，對 Palantir 等既有承包商形成競爭壓力。","source":"Barchart Why Palantir suddenly looks vulnerable after Google's move","url":"https://www.barchart.com/story/news/1625210/why-palantir-suddenly-looks-vulnerable-after-googles-move","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K風險因子載明：公司可能無法說服潛在客戶採用其平台而非現有軟體或內部IT部門偏好的自研軟體專案（一般性競爭風險，未指名最大客戶）","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"We may not be successful in convincing the management teams of our potential customers to deploy our platforms in lieu of existing software solutions or in-house software development projects often favored by internal IT departments or other competitive products and services.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"聚合站轉述：英國政府以自建系統取代Palantir於難民案件管理系統的軟體，稱省下數百萬英鎊（未核實原始來源）","source":"聚合站(轉述BBC，未證實)","url":"https://durslt.du.ac.in/first-dry/UK-Government-Saves-Millions-by-Replacing-Palantir-Technology-in-Refugee-Case-Management-System-12-8658","excerpt":null,"as_of":"2026-05-18","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 前三大客戶合計占營收 16%（FY2024 為 17%），前三大平均合作 10 年；曾有大客戶縮減支出或終止合約並需退還部分款項。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"Our top three customers together accounted for 16% and 17% of our revenue for the years ended December 31, 2025 and 2024, respectively. Our top three customers by revenue for the year ended December 31, 2025, have been with us for an average of ten years as of December 31, 2025.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2023–2025 無任何單一客戶占營收 10% 以上；應收帳款中 Customer I 占 25%（2024 年底 26%），無其他客戶超過 10%，應收總額 $1.0B。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"Customer I represented 25% and 26% of total accounts receivable as of December 31, 2025 and 2024, respectively, and no other customer represented more than 10% of total accounts receivable as of December 31, 2025 or 2024.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2026-09-30 10-Q：Customer I 占應收帳款 27%（2025 年底 25%），應收總額約 $1.9B；搜尋未見信用評等調降、破產或下修財測事件。","source":"SEC EDGAR 10-Q Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001321655/000132165526000048/pltr-20260930.htm","excerpt":"The Company’s accounts receivable balances as of September 30, 2026 and December 31, 2025 were $1.9 billion and $1.0 billion, respectively. Customer I represented 27% and 25% of total accounts receivable as of September 30, 2026 and December 31, 2025, respectively.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"PLTR Q3 2026 beat estimates and raised FY2026 revenue outlook to about $8.5B, above ~$8.21B consensus; Q4 guide ~8% above consensus (搜尋摘要，未讀原頁)","source":"investinglive: Palantir beats Q3 estimates, lifts 2026 revenue outlook to around $8.5 billion","url":"https://investinglive.com/stocks/palantir-beats-q3-estimates-lifts-2026-revenue-outlook-to-around-8-5-billion/","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"IDC: AI risk is capacity shortage not demand; memory shortage called structural, persisting through 2027, tight into 2028 (產業層，非軟體專屬)","source":"IDC blog: AI is short of capacity, not demand","url":"https://www.idc.com/resource-center/blog/ai-is-short-of-capacity-not-demand/","excerpt":null,"as_of":"2026-10-22","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Creative Strategies: 2027 為AI基礎設施限制高峰年，2028初緩解","source":"The Diligence Stack","url":"https://www.thediligencestack.com/p/2027-peak-year-of-constraint","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 稱無預期會對業績造成重大不利影響的法律程序；訴訟細節見 Note 8，未在 Item 3 點名反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"Based on our current knowledge, we believe that the amount or range of reasonably possible losses will not, either individually or in the aggregate, have a material adverse effect on our business, results of operations, or financial condition.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素：公司目前涉及並可能持續涉及監管或政府調查／訴訟，類型含反壟斷；政府正考慮進一步監管 AI，可能影響產品開發使用。為一般性風險揭露，未指名具體反壟斷案。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"governmental bodies have implemented laws and are considering further regulation of AI (including machine learning), which could negatively impact our ability to use and develop platforms and products incorporating these technologies.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"三次搜尋均未發現 DOJ／FTC／歐盟執委會對 PLTR 的反壟斷調查或拆分報導；唯一相關為與前員工新創 Percepta 的私人競業訴訟（非監管行動）。","source":"WebSearch 搜尋結果摘要（rallies.ai: Palantir Sues Startup Percepta）","url":"https://rallies.ai/news/palantir-sues-percepta-claims-two-ex-employees-misused-proprietary-code","excerpt":null,"as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"英國金融行為監理局（FCA）讓 Palantir 做三個月試用，分析其金融犯罪資料，引發對其觸及英國政府資料的疑慮。","source":"aitopics.org（轉載 Guardian）","url":"https://aitopics.org/doc/news:F5D39B40","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K FY2025 風險因子：產品受美國出口管制；多數產品（含核心軟體平台）歸類於 EAR，憑加密軟體例外通常無需特定許可；若被歸類 ITAR 或不符例外則需出口許可。新增出口限制或制裁變動可能降低海外客戶使用、減少營收。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"Most of our products, including our core software platforms, have been classified under the EAR and are generally exportable without needing a specific license, under an EAR exception for encrypted software.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 將關稅或貿易關係變動列為影響企業客戶採購決策的宏觀不確定因素之一。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"uncertainty about macroeconomic conditions (including as a result of the ongoing Russia-Ukraine conflict and related economic sanctions, the conflict resulting from Hamas’ attack on Israel and the ongoing conflict in the Middle East, fluctuating interest rates, monetary policy changes, foreign currency fluctuations, or the potential or actual imposition of tariffs or other impacts on trade relations)","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 揭露 Palantir 依賴 AWS、Microsoft 等第三方運算基礎設施支撐部分客戶，且不控制第三方設施營運；雲端供應商中斷或政策變動屬單點風險","source":"Palantir Form 10-K FY2023","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165524000022/pltr-20231231.htm","excerpt":null,"as_of":"2024-02-20","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K 稱在衝突地區營運使公司與供應商更易遭國家級網路攻擊，可能干擾供應鏈；未見台灣／中國製造集中揭露","source":"Palantir Form 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165525000022/pltr-20241231.htm","excerpt":null,"as_of":"2025-02-18","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"歐洲主權疑慮：法國 DGSI 轉用本地 ChapsVision、西班牙 SEPI 建議關係企業避免新合約（媒體報導，二手來源）","source":"Börse Express: Palantir Aktie: DGSI wechselt zu ChapsVision","url":"https://www.boerse-express.com/news/articles/palantir-aktie-dgsi-wechselt-zu-chapsvision-921538","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Iran IRGC 將 Palantir 列入其認定可攻擊的西亞美企設施名單","source":"TIKR: Palantir Stock Fell 7% as France Drops Its Software","url":"https://www.tikr.com/blog/palantir-stock-fell-7-as-france-drops-its-software-is-the-sovereignty-threat-real-or-a-buying-opportunity","excerpt":null,"as_of":"2026-06-23","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026：美國商業營收 $984M，年增 148%；美國政府 $953M，年增 96%；美國商業首度超過美國政府；全公司 $2.31B，年增 96%","source":"Palantir Form 8-K Q3 2026 press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001321655/000132165526000045/a2026q3ex991pressrelease.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"全年 2026 營收指引上調至 $8.530–8.534B（約年增 91%）；美國商業全年指引 >$3.559B（至少年增 143%）","source":"aiweekly.co / Futurum Group Q3 FY2026 earnings","url":"https://aiweekly.co/alerts/palantir-q3-revenue-nearly-doubles-to-231b-guides-to-853b","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 總合約價值（TCV）僅年增 6%，Q2 為 49%（分析師標示預訂成長放緩）","source":"sec-api.io Palantir Q3 2026 earnings analysis","url":"https://sec-api.io/insights/palantir-pltr-q3-2026-earnings-us-commercial-overtakes-us-government-sec-filing-analysis","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"競爭面：2026 年 1 月分析師預覽指超大型雲端與 AI 實驗室競爭升溫、AI 模型商品化可能稀釋錢包占有率；亦有看多觀點認為中期競爭有限。未找到可靠的定價或市占資料","source":"fundaai substack 'PLTR 4Q25 preview'; Freedom Broker note","url":"https://fundaai.substack.com/p/previewpltr-4q25-continue-to-accelerate","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：公司自述市場快速演變，成長取決於競爭產品進入、既有競爭產品成功與否，以及客戶是否願意採用替代做法。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"The market for our platforms is rapidly evolving. Our future success will depend in large part on the growth and expansion of this market, which is difficult to predict and relies on a number of factors, including customer adoption, customer demand, changing customer needs, the entry of competitive products, the success of existing competitive products","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"報導稱 Anthropic、OpenAI 等前沿 AI 實驗室可能把資料整合／工作流程功能產品化，成為 Palantir 替代方案；OpenAI 被報導在建資料連接平台，且複製 forward deployed engineer 模式；Karp 斥為 farce。","source":"MetaTrader news: Palantir Faces a Bigger Threat Than Valuation: AI Labs Like Anthropic and OpenAI","url":"https://www.metatrader.com/zh/news/1656682-palantir-faces-a-bigger-threat-than-valuation-ai-labs-like","excerpt":"Palantir Faces a Bigger Threat Than Valuation: AI Labs Like Anthropic and OpenAI Are Disrupting the PLTR Stock Story Barchart 2026.05.19 14:10 (GMT+0)","as_of":"2026-05-19","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"10-K FY2025 describes channel sales via cloud-provider partnerships, which give access to their large customer bases and expand distribution capabilities.","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"The existing footprint of these providers provides us with access to their large customer base and expands our distribution capabilities.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Palantir announced a multi-tiered partnership with Google Cloud making Palantir available on Google Cloud Marketplace.","source":"MarketBeat: Why Palantir's Google Cloud Deal Could Change the Debate","url":"https://www.marketbeat.com/articles/why-palantirs-google-cloud-deal-could-change-the-debate/","excerpt":"The multi-tiered partnership makes Palantir available on Google Cloud Marketplace and establishes two-way data federation between BigQuery and Foundry, as well as deeper connectivity between Gemini and Palantir AIP.","as_of":"2026-06-19","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 財報（2026-11-02）公司把全年營收 guidance 上調至 $8.530–8.534B，前次約 $8.15–8.16B（中點上調約 $378M）；Q4 營收 guidance $2.649–2.653B。","source":"Palantir Form 8-K Q3 2026 press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001321655/000132165526000045/a2026q3ex991pressrelease.htm","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q4 營收 guidance 約高於市場共識 8%；財報後盤後股價下跌約 3%。","source":"aiweekly.co: Palantir Q3 Revenue Nearly Doubles to $2.31B, Guides to $8.53B","url":"https://aiweekly.co/alerts/palantir-q3-revenue-nearly-doubles-to-231b-guides-to-853b","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"財報前（約 2026-10-30 收盤）分析師平均目標價約 $218.95，最高 $265（Barclays）；財報後 Mizuho 目標價 $205 維持 Hold、Jefferies $70 維持 Sell，目標價分布極寬。","source":"TIKR / TipRanks（Mizuho stays cautious…; Barclays $265 target）","url":"https://www.tipranks.com/news/mizuho-stays-cautious-on-palantir-stock-pltr-despite-q3-beat-jefferies-remains-bearish","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Palantir 上調 2026 營收展望至約 $85 億，Q3 優於預期","source":"investinglive","url":"https://investinglive.com/stocks/palantir-beats-q3-estimates-lifts-2026-revenue-outlook-to-around-8-5-billion/","excerpt":"beats Q3 estimates, lifts 2026 revenue outlook to around $8.5 billion Stocks Eamonn Sheridan 02/11/2026 | 21:15 GMT, published 02/11/2026 at 09:15 PM Tags Stock Earnings Summary Palantir beat Q3 forecasts with revenue of about $2.31bn and adjusted EPS of $0.44, then guided Q4 revenue to roughly $2.65bn, near 8% above the consensus, and lifted its full-year revenue outlook to about $8.53bn","as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 5 份 8-K 皆為財報/FD/股東會，無重大項目（1.01/1.02/2.01/4.02 等）","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001321655&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 5 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2022 年證券集體訴訟（Cupat v. Palantir）仍為 10-K 揭露的既有訴訟；搜尋摘要稱 2025-04-04 以 with prejudice 駁回、原告上訴第十巡迴法院、2026-03-16 言詞辯論，未見裁決；搜尋未見 2026 新增集體訴訟","source":"SEC EDGAR 10-K FY2025 Note 8；WebSearch 摘要","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"On March 31, 2024, the Court dismissed the Cupat matter without prejudice. On May 24, 2024, plaintiffs filed a second amended complaint.…","as_of":"2026-02-17","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"搜尋未見 Palantir 2026 年併購；僅見 2025-05 與 TWG Global 合資及 2026-02 DHS 最高 10 億美元合約（非併購）","source":"WebSearch 摘要（mergerlinks、SiliconANGLE）","url":null,"excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"搜尋未見 SEC 調查或重編財報；僅見 2025-10 起律所『調查』公告（Army NGC2 備忘錄報導後股價跌 7.5%），非 SEC 行動","source":"WebSearch 摘要（Business Wire、Portnoy Law Firm）","url":"https://www.businesswire.com/news/home/20251008536763/en","excerpt":null,"as_of":"2025-10-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2022 年證券集體訴訟（Cupat）列於 10-K FY2025 訴訟段，仍在上訴；未見 2026 新增集體訴訟","source":"SEC EDGAR 10-K FY2025 Note 8","url":"https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm","excerpt":"On March 31, 2024, the Court dismissed the Cupat matter without prejudice. On May 24, 2024, plaintiffs filed a second amended complaint.…","as_of":"2026-02-17","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 1 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"PLTR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":84.74,"operating_margin_pct":45.64,"fcf_margin_pct":55.62,"rd_intensity_pct":9.83},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"SNOW","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.03,"operating_margin_pct":-22.76,"fcf_margin_pct":21.96,"rd_intensity_pct":38.78},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNOW","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"NOW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":73.08,"operating_margin_pct":9.68,"fcf_margin_pct":30.78,"rd_intensity_pct":22.47},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"CRM","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":77.28,"operating_margin_pct":21.52,"fcf_margin_pct":34.49,"rd_intensity_pct":14.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"DDOG","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.58,"operating_margin_pct":2.3,"fcf_margin_pct":25.93,"rd_intensity_pct":42.61},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"PLTR"},"financial_history":{"ticker":"PLTR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":1905871000.0,"revenue_yoy_pct":null,"gross_margin_pct":78.56,"operating_margin_pct":-8.46,"net_income":-373705000.0,"diluted_eps":-0.180263,"free_cash_flow":183710000.0,"fcf_margin_pct":9.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2225012000.0,"revenue_yoy_pct":16.75,"gross_margin_pct":80.62,"operating_margin_pct":5.39,"net_income":209825000.0,"diluted_eps":0.090131,"free_cash_flow":697069000.0,"fcf_margin_pct":31.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2865507000.0,"revenue_yoy_pct":28.79,"gross_margin_pct":80.25,"operating_margin_pct":10.83,"net_income":462190000.0,"diluted_eps":0.190277,"free_cash_flow":1141231000.0,"fcf_margin_pct":39.83,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":4475446000.0,"revenue_yoy_pct":56.18,"gross_margin_pct":82.37,"operating_margin_pct":31.59,"net_income":1625033000.0,"diluted_eps":0.63,"free_cash_flow":2100591000.0,"fcf_margin_pct":46.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/PLTR/PLTR_Q3_2026_Earnings_Call_20261102.md）

# Q3 2026 Earnings Call
**Palantir Technologies Inc.** | Earnings Calls | 2026-11-02

**Ana Soro** (Executives):
Good afternoon. I'm Ana Soro from Palantir's finance team, and I'd like to welcome you to our third quarter 2026 earnings call. We'll be discussing the results announced in our press release issued after the market closed and posted on our Investor Relations website.
During the call, we will make statements regarding our business that may be considered forward-looking within applicable securities laws, including statements regarding our fourth quarter and fiscal 2026 results, management's expectations for our future financial and operational performance, which does not constitute formal guidance unless indicated as such in the accompanying written materials and other statements regarding our plans, prospects, expectations, goals and aspirations. These statements are not promises or guarantees and are subject to risks and uncertainties, which could cause them to differ materially from actual results. Information concerning those risks is available in our earnings press release distributed after the market closed today and in our SEC filings. We undertake no obligation to update forward-looking statements, except as required by law.
Further, during the course of today's call, we will refer to certain adjusted financial measures. These non-GAAP financial measures should be considered in addition to, not as a substitute for or in isolation from GAAP measures. Additional information about these non-GAAP measures, including reconciliation of non-GAAP to comparable GAAP measures, is included in our press release and investor presentation provided today. Our press release, investor presentation and other earnings materials are available on our Investor Relations website at investors.palantir.com. Over the course of the call, we will refer to various growth rates when discussing our business, these rates reflect year-over-year comparisons unless otherwise stated.
Joining me on today's call are Alex Karp, Chief Executive Officer; Shyam Sankar, Chief Technology Officer; Dave Glazer, Chief Financial Officer; and Ryan Taylor, Chief Revenue Officer and Chief Legal Officer.
I'll now turn it over to Ryan to start the call.

**Ryan Taylor** (Executives):
Humanity is facing world historic crossroads in how it chooses to deal with AI. And through it all, our genre-defining technology has led the way, redefining the industry. We've been shaping the AI revolution from its start. And despite being only at the very beginning of the sovereign AI revolution, we already see how it is transforming the size of the market.
We achieved revenue growth of 96% year-over-year and 20% sequentially, the highest growth rates we've ever delivered as a public company. These results are the continued financial expression of the transformational impact we're delivering for our customers, which is also evident in the depth of our customer relationships. The third quarter average trailing 12-month revenue from our top 20 customers increased 76% year-over-year to $146 million per customer.
Our U.S. business is in overdrive. We brought in $1.9 billion in U.S. revenue, which grew 119% year-over-year and 23% sequentially, representing 84% of our total revenue. This is led by our U.S. commercial business, which grew 148% year-over-year and 29% sequentially, and surpassed our U.S. government business revenue in quarter for the first time. In U.S. commercial, the average trailing 12-month revenue per customer grew 88% year-over-year and 20% sequentially. The U.S. continues to be the epicenter of the AI revolution.
I won't repeat what I said last quarter because it has become self-evident in our unparalleled results. Two years ago, we led the way with our commoditized cognition thesis. And today, the market is only beginning to recognize the full force of sovereign AI. It's pervasive in the conversations I'm having with customers and undeniable in the results they've shared.
The COO of Optum Serve highlighted, "Sovereignty doesn't mean that we have to build everything ourselves. What it does mean, though, is protecting what differentiates us while retaining the ability to evolve, to adapt and to scale our solutions as our customers' needs change, and they change often. It means knowing where the right partner can help us move faster." L3Harris noted that by fine-tuning open source models on its own data, a sovereign model outperformed the frontier model it had been using in less than 48 hours and cut costs by 95% in preliminary results.
NVIDIA reported that by evaluating and posttraining its open models, it was able to get its smallest, most efficient model to outperform its largest model by a large gap, and can now retrain that model on just a single GPU in a couple of hours, enabling them to retrain any time they have data to improve the decision intelligence. They stated, "We captured our alpha and we trained it into a model. We couldn't have started this process until we built the workflows in Palantir."
And our customers are choosing Palantir and our sovereign AI to transform their organizations at a furious pace. An industrial materials company piloted a nearly $3 million engagement in Q2 2026 before converting to a $29 million ACV deal last quarter. A global athletic company converted a $1.6 million pilot that began in Q1 2026 into an approximately $21 million ACV deal last quarter. A global home appliance company converted a $1 million pilot that began in Q2 2026 into a $3 million ACV deal within the same quarter, then expanded nearly fivefold to a $15 million ACV deal in Q3 across commercial, finance and supply chain workflows. After an AgentCamp in Q2 2026, an apparel company signed a $2.5 million pilot, then last quarter, they converted to an $11.5 million ACV deal.
These commitments are downstream of the measurable impact we're delivering with our customers. With Palantir Sovereign AI, McCarthy Building Companies will save 30,000 hours annually by using posttrain Nemotron to help turn complex project requirements into contract language that allocates risk and clearly define subcontractor obligations. Tampa General is deploying sovereign AI to keep sensitive data and model processing local while enforcing its own risk and privacy standards for LLM traffic, and supporting the granular controls Tampa General wants to define for itself. Using fine-tuned and posttrained Nemotron to achieve this outcome, together, we also improved model performance by 7% and reduced latency by 22x.
Turning to our U.S. government business. Revenue grew 96% year-over-year and 18% sequentially, demonstrating continued extraordinary impact across civil and defense, with Maven as our foundational work. In Q3, the Army awarded Palantir a prime agreement to produce 8 TITAN systems. And last quarter, FAA highlighted the impact of our work together, stating, "That shift from scattered data to an embedded Ontology is what changes the game. This is a modernization in operational form changing how safety work gets done." And noted that the work they can do now would require hundreds of analysts without Palantir.
As I reflect on our results, I see the furious pace continuing unabated. I'm invigorated unlike ever before by the ambition I'm hearing from our customers and their demand for sovereign AI, a revolution we should remember is barely 1 quarter old. As extraordinary as these results are, they are only the opening chapter of sovereign AI.
I'll now turn it over to Shyam.

**Shyam Sankar** (Executives):
Thanks, Ryan. Palantir is obsessed with turning tokens into economic value. It's clear that the vast majority of economically valuable problems that LLMs can solve can be solved with intelligence at or below the frontier. So what's preventing this from happening? On one end, you have the model makers who can't conceive of solving any problem except through model improvement. So they aren't even trying. And on the other end, you have the hard work of diffusion, which sounds passive, but is anything but. All the value comes from the elegant integration of AI, software and humans. And this requires not a harness for the model, but something closer to a harness for the enterprise, which is exactly what AIP is.
Most profoundly, the conceit that the labs have wrong is the belief that the atomic unit of the enterprise is the individual knowledge worker. It is not. The fundamental unit of the enterprise is the workflow. You can make any set of workers more productive and generate no actual ROI. For some things like coding, the knowledge worker is the workflow. So there's perfect product market fit. But for the vast majority of the enterprise, it is not. Given this, it is incredibly valuable that AIP implements enterprise workflows and is able to bring AI to it in a way that generates objective, quantifiable value.
For example, Page 209 of Anthropic's S-1 talks about AIG's automation of insurance underwriting processes for complex commercial lines of business. That entire workflow and the elegant application of AI, software and humans runs in AIP and was implemented by Palantir and AIG. We are the diffusion layer, not just of choice, but of necessity.
There's a clear pattern emerging amongst our customers who are most successful at getting value from AI. They have enormous ambition. Their goal is not something lame like OpEx reduction. It's market domination. And the opposite is true. Customers that struggle the most are narrowly focused on reducing cost. AI is a new type of intelligence. Simply trying to shoehorn it to replacing the human misses the moment completely. The error of conflating human and machine intelligence locks you into a poorly chosen goal, one that limits your ambition and still remains out of reach.
Instead, we're attacking all the work the enterprise knows it should be doing, but historically lack the economic resources or capabilities to take on. An agent swarm watching each patient in the ICU ward to help clinicians avoid potential signs of sepsis earlier and improve patient outcomes, an agent swarm per wellhead in the Permian Basin to maximize production, an agent swarm for every customer of our customer to drive growth. This is not about doing the same thing cheaper. It's about defining the productive work that goes beyond yesterday's frontier, and capturing and compounding the new economic value it creates, and doing so with sovereign AI.
The examples are everywhere now. It's clear that posttraining on your specific operational data in Ontology enables better than frontier performance on weights you control, protecting your alpha. Yes, it's cheaper, but the dominant variable is that more use cases can actually get to the threshold of viability for machine intelligence to generate economic value when elegantly integrated into your enterprise. And our product investments in AIP to create a closed-loop model factory are making this easy and fast.
The specific posttrained model is a commodity item. The compounding value is in the posttraining pipeline that is constantly fed from your operational exhaust captured in the Ontology that drives automated posttraining runs, model checkpoints, evaluations and deployment across yesterday's, today's and tomorrow's open-weight ecosystem. Our new feature of AutoResearch and continued investment in AIP Evolve, push us closer and closer to an automated loop to build, deploy and evaluate intelligence continuously against ROI. In AIP and sovereign AI, the Pareto optimal frontier is no longer an unachievable academic aspiration. It is a simple function call and one we can invoke automatically on your behalf.
At a recent PACOM exercise, we deployed a 30 billion parameter posttrain model into space, weight, power, cooling constrained compute, ready for the disconnected fight, with superior task-specific performance than GPT 5.6 Sol, a 3 trillion parameter model. L3Harris realized 95% cost reduction with sovereign AI. McCarthy will save 30,000 hours a year on subcontractor drafting, achieving better than frontier performance for RFI classification and subcontractor drafting on a posttrain Nemotron 4 billion parameter model, where, again, the real value is the substantially greater number of demand events they can process now.
Maven continues to deliver for the joint force, exceeding 100,000 users. Maven is now available to all of the services beyond just the combatant commands and many combat support agencies. We just concluded a Maven hackathon, 46 teams across the joint force participated. Many amazing projects were built by our 25,000-strong builder community. The winning 2 teams were both Army teams, one building an edge planning and simulation capability for force protection and a second place, an incredible platform to analyze drone incursions to drive force protection insights.
And we continue to feel demand for Maven down to the tactical edge in disconnected environments, ashore and afloat. We have seen incredible success with DORA, Disconnected Ontology Resilient Architecture, including in the Army's jailbreak effort. DORA is an embedded compute device that brings Maven's capabilities to disconnected operations. Using AI FDE, service members can build read-write integrations with legacy sensors and effectors and bring them online in hours, entirely unassisted.
With that, I'll turn it over to Dave.

**David Glazer** (Executives):
Thanks, Shyam. We had an outstanding third quarter. We delivered our highest ever reported year-over-year revenue growth rate of 96% and our highest ever reported sequential revenue growth rate of 20%. Quarterly revenue crossed the $2 billion mark for the first time, and we surpassed additional $1 billion milestones in commercial revenue, government revenue and GAAP operating income.
Revenue in our U.S. business accelerated yet again, growing 119% year-over-year and 23% sequentially. Our U.S. commercial business grew 148% year-over-year and accelerated to 29% growth sequentially, and our U.S. government business grew 96% year-over-year and 18% sequentially. Demand for our sovereign AI offering is accelerating our U.S. commercial momentum, helping to make this our first ever quarter that U.S. commercial revenue eclipsed U.S. government revenue, a critical milestone in the history of our company.
On top of this, we are raising our full year U.S. commercial revenue guidance to in excess of $3.559 billion, representing a growth rate of at least 143%. We are also raising our full year 2026 revenue guidance midpoint to $8.532 billion, representing 91% growth year-over-year, a 9-point increase over our full year 2026 revenue guidance from last quarter.
Turning to our global top line results. Third quarter revenue grew 96% year-over-year and 20% sequentially to $2.313 billion. Third quarter U.S. revenue grew 119% year-over-year and 23% sequentially to $1.937 billion. Revenue from our largest customers continues to expand. Third quarter trailing 12-month revenue from our top 20 customers increased 76% year-over-year to $146 million per customer.
Now moving to our commercial segment. Third quarter commercial revenue grew 113% year-over-year and 24% sequentially to $1.168 billion, crossing the $1 billion mark for the first time. We closed $1.652 billion in commercial TCV bookings in the third quarter, representing 17% growth year-over-year. Our AI platform continues to dominate the U.S. markets as the only real choice for operationalizing LLMs while still giving customers full control over the data, logic, actions and security of their enterprise.
Third quarter U.S. commercial revenue grew 148% year-over-year and accelerated sequentially to 29% quarter-over-quarter, totaling $984 million. U.S. commercial revenue was $397 million in the third quarter of 2025, meaning it increased by $587 million in just 1 year. We closed $1.463 billion of U.S. commercial TCV bookings, representing growth of 11% year-over-year. Over the past 12 months, we closed $6.114 billion of U.S. commercial TCV bookings, a 62% increase from the prior 12 months, highlighting the accelerating demand for AI that creates real operational value while also moving power away from the labs and back into your enterprise. Total remaining deal value in our U.S. commercial business grew 79% year-over-year and 4% sequentially.
We believe sovereign AI is the latest and largest tech revolution of our generation. We signed multiple 8-figure deals in the quarter that were shorter in duration than usual, as customers rapidly adopted initial sovereign AI capabilities in their enterprise. It is important to remember that the sovereign AI revolution is only 1 quarter old. As we continue to deliver value with sovereign AI, over time, we expect both the duration and size of these contracts to increase.
Our U.S. commercial customer count grew to 686 customers, reflecting growth of 29% year-over-year and 5% sequentially. Third quarter international commercial revenue grew 21% year-over-year and 1% sequentially to $184 million. Revenue from strategic commercial contracts was approximately $400,000 for the quarter, representing less than 0.02% of overall revenue. We continue to expect revenue from these contracts to be less than $500,000 in the fourth quarter, and we anticipate no further revenue from these contracts beyond the fourth quarter of this year.
Shifting to our government segment. Third quarter government revenue grew 81% year-over-year and 16% sequentially to $1.146 billion, crossing the $1 billion mark for the first time. Third quarter U.S. government revenue grew 96% year-over-year and 18% sequentially to $953 million. This growth was driven by continued execution in the existing programs and new awards reflecting the growing demand for our AI platform and government.
Third quarter international government revenue grew 31% year-over-year and 6% sequentially to $192 million. We closed $2.918 billion of TCV bookings, up 6% year-over-year. Net dollar retention was 165%, an increase of 800 basis points from last quarter. We ended the third quarter with $13.4 billion in total remaining deal value, an increase of 55% year-over-year and 2% sequentially, and $4.9 billion in remaining performance obligations, an increase of 88% year-over-year and flat sequentially. As a reminder, RPO is primarily comprised of our commercial business as it does not take into account contracts with an initial term of less than 12 months and contractual obligations that fall beyond termination for convenience clauses, both of which are common in most of our government business.
Turning to margin and expense. Adjusted gross margin, which excludes stock-based compensation expense, was 85% for the quarter. Adjusted income from operations, which excludes stock-based compensation expense and related employer payroll taxes, was $1.427 billion in the third quarter, representing adjusted operating margin of 62%. Q3 adjusted expense was $887 million, up 20% sequentially and 53% year-over-year, primarily driven by the continued investment in our AI platform and technical hiring as we welcomed our latest class of new grad hires. We remain committed to investing in the most elite technical talent as well as R&D for our product pipeline and sovereign AI efforts, all while delivering on our goals of sustained GAAP profitability.
Third quarter GAAP operating income was $1.085 billion, representing a 47% margin and surpassing the $1 billion mark for the first time. Third quarter GAAP net income was $1.128 billion, representing a 49% margin. Net income has increased nearly eightfold over the last 24 months from $144 million in the third quarter of 2024.
Third quarter stock-based compensation expense was $319 million and equity-related employer payroll tax expense was $23 million. Third quarter GAAP earnings per share was $0.44. Third quarter adjusted earnings per share was $0.44. Additionally, our combined revenue growth and adjusted operating margin accelerated to 158% in the third quarter, a 3-point increase to our Rule of 40 score from the prior quarter and our 13th consecutive quarter of an expanding Rule of 40 score.
Turning to our cash flow. In the third quarter, we generated $1.205 billion in cash from operations and $1.216 billion in adjusted free cash flow, representing margins of 52% and 53%, respectively. We ended the quarter with $10.4 billion in cash, cash equivalents and U.S. Treasury securities.
Now turning to our outlook. For Q4 2026, we expect revenue of between $2.649 billion and $2.653 billion, and adjusted income from operations of between $1.640 billion and $1.644 billion. For full year 2026, we are raising our revenue guidance to between $8.530 billion and $8.534 billion. We're raising our U.S. commercial revenue guidance to in excess of $3.559 billion, representing a growth rate of at least 143%. We are raising our adjusted income from operations guidance to between $5.245 billion and $5.249 billion. We are raising our adjusted free cash flow guidance to between $4.8 billion and $5 billion, and we continue to expect GAAP operating income and net income in each quarter of this year.
With that, I'll turn it over to Alex for a few remarks, and then Ana will kick off the Q&A.

**Alexander Karp** (Executives):
Welcome to our earnings call. And I think for many, many years, our earnings calls were really about our earnings. Now it is the focal point of tech, society and general trends. And I think many, if not most people who are watching this, and it is by far the most watched earnings call in the world. It's the one where people come to figure out what's going on, on the ground floor. And given that AI and sovereign AI is changing the universe, in our case, for tremendous good and is showing up in our numbers, people really want to have a sense of, well, what is actually happening in the world, politically, sociologically, anthropologically and, of course, financially.
So given that demand and interest in Palantir and the reality that this moment has become a real focal point of understanding. And quite frankly, many investors watching this are watching it to figure out what's going on with their investments and not even primarily Palantir. And so there's this larger question of what does it mean to have a business that was built around what we believed and believe now is the most important mission in the world, supporting our war fighters, bringing them home, where even as much -- even a year ago, 2 years ago, that people, even involved inside Palantir, viewed the core value of our business economically as Glazer would look at it. And quite frankly, in a very helpful way, he's the force of greed. Glazer's view of our business was, could you talk a little more about commercial over the past year -- past couple years.
And in this quarter, our commercial business eclipsed our government business. And in fact, the market value of that is probably justifies our current valuation, given we're growing at 90% -- our aggregate business growing at 96%. The juggernaut of U.S. commercial. I mean these numbers are so far outside the bounds of what you could -- I mean, outside the bounds of what even the most optimistic people could think a business like ours could do, while maintaining a way of going to market that is completely sui generis.
We have products that are unique. We have ways of going to the market that are unique. We were the leader of a revolution that was in front of us but none of us really were able to put our name on the sovereign revolution, meaning people need to understand how AI can create value, how you can create value out of tokens, how you can keep the value of your own alpha, how is it not transferred to anyone else, and how can you expand it. That revolution, of course, is happening in America.
And then these out-of-bounds results, of which were a metaphor really show you the future is becoming the present and the present is now. You see it in Europe, which I spent half of my life in. At this point, we should kind of avoid talking about it because of what's going on, and it doesn't help to just stamp on them. But you see it across America, you see the reaction to AI, you see the polarization politically. It's because all the value in the market is actually moving to the vehicles, in this case, Palantir and really very few others, Anthropic, OpenAI, us, others, that where you can actually make a claim that there is some value creation.
Again, it's so extreme that a business that was viewed as a nice-to-have part of our business as late as 3 years ago is now the dominant part of our business. That business grew 29% quarter-on-quarter. It's almost at 150% growth. And it's dragging our U.S. growth number over 100%. These are just -- and we did this while attacking the market the way we attack it, very few salespeople. Very -- an impossible way to understand how we are capturing this juggernaut unless you view it as a completely new and different moment.
And so when people are watching this, they're like, what is happening in the market? What is happening in our society? It really is the case that the playbook, the products, the way of going to market do not work in most cases, but the things that do just spring alive. And our somewhat crazy aspiration to take the whole market doesn't look that crazy right now.
And we believe at this company and many of the people watching it, we do not only have a financial reason for taking the whole market, which Glazer is salivating at. We, on the mission side, we believe we have a mission reason for taking the market. And that mission reason is we support your alpha, we support your sovereignty. We've done this for over 20 years. We support the war fighter. We are delighted that we can support the war fighter even more because we're making so much money. But we believe we have a moral imperative to be the dominant player in our industry, broadly defined, including all AI applications and the use of model, open and closed, especially training open-weight models. And that moral imperative drives every part of our business.
The interesting thing about the internal dynamic of our business, it's not only that the sum of the parts in our business is stronger. That's obvious, 96% growth. Look at our Rule of 40, it's 158%. It's almost, like, jaw dropping. But we -- the parts of our business, the individual parts, the parts that the people at this company are running, those parts are stronger than they were before, every part. And that's what you're seeing in these numbers. And arguably for most people watching that, that's what you're seeing in broader society.
And this move to the -- from the future to the present is the reason why many of the classical approaches to business, there was an idea they were going to fail in 5 years. That doesn't work. You have to execute now and in the present. And this company, Palantir, and everyone involved and all of the people watching this who are on our side, of which there are many, many people, are part of that movement. And that's why we're so really happy, and honestly, quite optimistic about the future, especially in the U.S.

**Ana Soro** (Executives):
Thanks, Alex. Our first question is from Dan with Yorkville Ives.

**Daniel Ives** (Analysts):
Obviously, just another phenomenal quarter. So my question is, with the sovereignty AI bootcamps, I mean, I've been to a few. It seems like they're really becoming huge for converting customers. Can you just walk through, like, Alex, like you talk to so many of these customers. Like do they come into a bootcamp, just they're not -- they're trying to understand their AI path and then they leave and they're actually a customer? Like can you just walk through, like, just from your perspective?

**Alexander Karp** (Executives):
Well, I mean what's really shifted on the front line is, like, there used to be this long walk-up to people, like, talking to us and then you do a pilot and then you try to get a long pilot, and then you kind of lock that in because the same way you lock in, like, hire all these salespeople so that the market believes you're going to have sales kind of thing. Now it's much more -- people are -- it's super heterogeneous. So some people -- everybody basically comes in on the spectrum of what I have doesn't work now, and I've heard what you have does work. That's usually where it starts.
They also strongly believe and are quite tired of what they believe the reality is, my IP is in danger, and I'm getting no value. It's like -- and this is -- when we started talking about sovereignty, this was kind of -- this was something that was being expressed, they felt, but they didn't know how to articulate. Now it's something they articulated and they've gone from anger to action. It's like they've gone from thinking, hey, I'm not in a great marriage, to I'm at the divorce. And like they come. And then what's very special now is they're surrounded by people who've had the same journey, and the time line from interaction to them buying pilots or going into production is completely shifted.
And so what, like, Ryan and I are seeing on the front line in commercial is this much quicker interaction, much quicker to deployment, shorter duration of the contract, but then an ability to expand that contract dramatically. Because as soon as you go in there and you show them that you can, for example, train open-weight models in our Ontology, those models are valuable and you have beyond frontier capacity without losing the alpha, you just are hooked. What we have to do internally is figure out how to re-resource our company to focus exclusively on those people because we don't have even the bandwidth to do that.
So -- but that's because, like, every single time we go into the conference, like in the past, you would be -- we go into a conference and people are like warm leads turn into hot leads. This is like first date into bed kind of thing. Maybe that's not the right metaphor for this, but it's like -- it's a very different jam. It's like we've -- put this way, we've gone from being the most attractive person in the physics department to being the captain of the football team kind of thing. I mean not that I did that. But this is like a completely different jam of, like, what's going on.
And then it's also different on our end because we know we can deliver on use cases no one else can deliver on. So like even today, we're going over a use case after use case with like a super -- like, one of the most important companies, and I'm going to go see them. And basically, it's like I'm going to -- instead of saying, hey, which is like, let's just get started. You have this crucial problem for your business. We know we can deliver on this in weeks. This will change the trajectory of your business. And it's, in a weird way, it's much, much closer to what we were doing in the beginning in the U.S. government, where we're like, hey, we're just going to get started. We knew we could prove it with PG and then we -- but it's like at a much more massive scale. So instead of being, like, $250,000, it's like $25 million to start.
And honestly, the general vibe is if this actually works, it's worth of infinite value, and it will work. And quite frankly, I do not see how other offerings are going to work because this is both product and artistry. It's not -- that's why these numbers are so bombastic. It's not like some static, like when Shyam's on the front line doing implementations or Ryan is structuring these -- I mean, Ryan was so busy in the last couple days of last quarter, he couldn't get out of his car. We were like -- I was about to send over a bottle, so he could, like, take care of nature. It was like -- it's like that on the front line. Like, I'm not even -- I'm not exaggerating. It's like -- I'm like, Ryan was on his way to work and, like, he had to pull over. He drives a fancy car. I mean look at that. It's -- but he literally had to pull over. And that's just what's going on.
And -- but again, I know like the primary focus of your interest here is financial, but there's the flip side. The other stuff is not working. That's part of -- it's not just that our thing is unique. It's -- there's a very strong sense in the market that these other approaches, fake deploy codes, token, raw usage, lightweight companies reselling tokens, software companies that are reselling tokens and accounts as revenue, people are just tired of it.
And I'll tell you, last not least, the taste of the market is shifting. Like, people really do grow to like what works. I mean, look at the success in the Department of War. It's like, that was -- we shifted the taste. That's what's happening in U.S. comm. That's what's explaining the numbers. And that's what -- if you like people watching this, you should come to one of our AIP Sovereign. It's a little bit like a rock concert.

**Ana Soro** (Executives):
Our next question is from Gil with D.A. Davidson.

**Gil Luria** (Analysts):
I want to build on that conversation you had with Dan. You talked to him about one type of CEO, the one that comes to you with an urgency around sovereignty. But as reading the Anthropic S-1 will tell us about half of their customers work directly with Anthropic. So when you have a -- which means there's a lot of CEOs that haven't gotten the message. To your point, you're in the first inning of this conversation.
When you get a CEO that's still unconvinced, what kind of analogies and metaphors can you use to help them understand the importance of this diffusion layer, orchestration harnesses coming from you and not directly from the lab? What kind of examples do you have to provide them to understand the risk?

**Alexander Karp** (Executives):
There's 2 parts to your question, which is, like, the person who's not convinced or not yet convinced, and then what do we do? The weird thing here, though, is we really cannot satiate demand. So this is a market that is growing so rapidly. We don't need the people who aren't convinced. We really don't. And by the way, and again, I say this every time, Dario is someone I get along very well with. I think he's one of the most important business people of my generation, if not multiple generations. They are also selling our product because people interact with them.
And again, some people want that approach. But a lot of people are super concerned about their alpha being transferred to them. And the results -- even the results they talk about are often already in our application layer. We work very effectively with Anthropic and the Department of War and at AIG and all over the place. But again, the primary -- what they are doing is increasing the size of the market. What we're doing is servicing the market that's gotten real.
And we are actually in a symbiotic relationship with them commercially because they're growing a market that's probably much, much bigger than it will be -- than it is today. And we're taking advantage of the market where you really need delivery, where delivery also includes. Now if there is somebody -- we don't -- we really do convincing in the government space, like, we've been on the front line, like, certain agencies didn't want to adopt, and we knew the war fighters would die if they didn't adopt. So we went to convince them.
In commercial, our real approach is, hey, enjoy the one you're with until you just -- you find out it's not the one you want. There are very, very, very few times where we're trying to go and compete and take their customer away. It really is not happening. And conversely, once you go Palantir, you don't go back. And that's just -- that's how it is. And you see it in our numbers, which is -- so it's -- this is a very different thing. I don't know at what point we become competitive with each other. But at this point in the U.S., the market for us is insatiable. And it's insatiable and growing and growing and growing.
There's 2 ways to look at our numbers. One is to say we are just sublime at what we do. Another way is to say we're very unique and the market is exploding around us. I'm much more in the latter camp. Like, I don't -- we are a creative colony, we're not perfect. But the market is exploding around us, and they are helping it explode. And the only area where we do anything that looks competitive is we are spending a lot of time educating clients, partners that may -- that are nonpartners around the risks of using closed models without an application layer. That's the one thing we do, do actively.
So -- but we're not really saying, hey, you're going to -- the value creation, people know we own. It's certainly an industry, I think less on Wall Street. Actually, honestly, I think on Wall Street, I don't mean you, but I think really what happened on Wall Street is everybody invested in these firms early, bless you guys. It's hard to see the reality when you're getting rich on something that's not actually working the way you think it is. And the reality is, though, in industry, people realize when it gets real, you need us. And that market is much larger than we can service.

**Ana Soro** (Executives):
Our last question is from Brad with Deutsche Bank.

**Brad Zelnick** (Analysts):
Congrats on another rocket ship quarter. Alex, in your shareholder letter, you said that you see Palantir as the pioneers of a genuine and viable anti-war movement. Can you expand on what that means and what it might mean for your government business?

**Alexander Karp** (Executives):
Well, one of -- and I'll let Shyam talk about this. I'll go back to the beginning of our Palantir PG. And we built products that would protect civil liberties and stop terrorism for the very simple reason that you don't want to do one or the other. If you don't stop terrorism, you're going to get a radical fringe on the right. If you stop terrorism without rights, none of us want that.
Okay. You could say it's an anti-terror product or you could say it's a product for social cohesion. It's this product for -- our products are built to avoid war, meaning the adversary knows that they will have such pain inflicted upon them that, in fact, it's not worth going to war and also to create social cohesion because we're going to bring back our troops healthier, safer, nondamaged and that makes our society much more effective.
And I would say as a person, not as, like, Palantir, I grew up as a lefty. I don't actually like war. I want to avoid war. I do not support wars. Sometimes they are necessary. And when they are necessary, America and its allies need the very, very, very best tools. And we have competitors, adversaries and enemies out there. They need to know our stuff works. The way to stop a war is for them to know these things work.
And also, part of the problem that we've had in an AI discussion in this country is we do have a rival and adversary on the battlefield. I happen to respect their culture quite a bit, China, but it is us or them. And they have a dynamic, interesting super high IQ scaled culture that is doing exceedingly well at AI. And we've got to make sure we're the leaders.
And somehow, we have to drag our European and other allies with us, which is going to be hard because they're going to have to also learn how these things work, and that probably means a real interaction with the leader of the sovereign movement, not some fake bureaucratic thing made up by people who have no idea what they're talking about and think you can regulate these things like a telecom industry when, in fact, this is galvanizing a new transformative technology that is transforming every part of society and transforming our numbers and everything it touches.

**Ana Soro** (Executives):
Thank you. Alex, as always, we have a lot of individual investors online.

**Alexander Karp** (Executives):
Somebody else has got to talk.

**Ana Soro** (Executives):
Is there anything anyone would like to say before I end the call?

**Alexander Karp** (Executives):
Maybe you guys can say a couple words. Shyam, would you like to say?

**Shyam Sankar** (Executives):
Well, I mean, you spoke about deterrence really well. I guess I would just add that, of course, the objective is to deter conflict. Deterrence is not something you accomplish by hope. You actually have to build it brick by brick. And so on one end, in the foxhole, that's about having a capability that's 10x, 100x better than your adversary. Should they choose to fight, they're going to lose, and therefore, they should not choose to fight. And on the other end, it comes down to the factory floor. A deterring conflict, as we've seen with Russia and Ukraine, is really about your ability to produce the materiel.
And we are in a period where we need to reinvent how we do production. We've gone through 30, 40 years of essentially deindustrialization in the nation beyond just our defense industrial base. And the work that we're doing with war machine and working with commercial and private and public sector companies in order to enable production using a modern American manufacturing stack. These are 2 parts of the same coin here. And I think it comes down to, yes, freedom driven through the foxhole, but also prosperity, the growth of the American economy on the back of that.

**Alexander Karp** (Executives):
Do you want to say something? Would you like to talk about your greed afterwards?

**Ryan Taylor** (Executives):
I'll just add, the sovereign AI revolution, we launched this last quarter and the felt version on the ground is -- and what we're seeing at sovereign AI bootcamps when we actually show and don't tell is the momentum and the urgency of customers that get it and see it, adopting quickly, moving quickly, moving with urgency because they realize how much it matters. And we're feeling that on the ground, and we're at the very beginning of this, and we only see that continuing and expanding from here.

**Shyam Sankar** (Executives):
And because I can't help myself, I'll say one more thing, going back to Gil's question. I mentioned this earlier in my comments, but it really is the case that I think one of the conceits that the labs don't have right and that perhaps the customers who don't quite yet realize that the return is not there, is that the atomic unit of the enterprise is not the knowledge worker. You can make people more productive and generate no actual return on investment. If you're measuring the inputs, it can feel really good to see that productivity of the person. You actually -- the atomic unit is the workflow.
And having a platform like AIP, where you're already managing your supply chain or your S&OP or your key enterprise processes, the exhaust of those processes then enable you to go through the posttraining loop to have a model that's better than frontier at that. We give you the tools to elegantly integrate your people, your AI and the software to actually drive objective, quantifiable value against the workflow.
This is the compounding loop that the customers who are coming to us in the sovereign bootcamps really understand. Just at our most recent DevCon down in Miami, we had a customer who, on their stack in production as a hack week project, built a production-ready model that's better than frontier for their use case in the 48 hours. Single person, in the 48 hours that was DevCon. So the proof is everywhere on this.

**David Glazer** (Executives):
And I guess to add 2 financial metrics to leave you with, I'd say, 2 years ago on net income and to today, we've 8x-ed our net income over the last 2 years, which I am incredibly proud of as well as everything else that was said. And also, as we look at sort of this year to basically guide to almost $5 billion in cash flow for the full year is, I think, something we all can be excited about.

**Alexander Karp** (Executives):
And to close, I just -- the people who invested in us early, many of them were investing their own money and would otherwise be called retail, and many now and recently have reinvested in us. The sovereign revolution is a metaphor for your interaction with Palantir. And the fact that we've been able to help you and you've been able to help us in your own wealth creation and in our journey and that you've defended us against what obviously now look like ridiculously stupid and malicious, incredibly hard-to-understand attacks is something that we will never forget.
And part of the delivery here, part of what motivates me is helping to make sure we are fighting for you and, quite frankly, making sure that the people that made fun of you and made fun of us are suffering. And I'm very proud of that, and I'm very proud to have all of you along with us, and thank you for that support.

**Ana Soro** (Executives):
Thank you. That concludes today's call.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### PLTR_Q2_2026_Earnings_Call_20260803.md
- 2026-08-03｜CFO｜guidance：CFO 上調全年美國商業營收財測至至少 3.424 億美元以上的口徑：超過 $3.424 billion、成長至少 134%（原話："$3.424 billion, representing a growth rate of at least 134%"）
- 2026-08-03｜CFO｜guidance：CFO 上調 2026 全年營收財測中點至 81.54 億美元、成長 82%（原話："midpoint to $8.154 billion, representing 82% growth"）
- 2026-08-03｜CFO｜guidance：CFO 給 Q3 營收財測區間 21.6 億至 21.64 億美元（原話："we expect revenue of between $2.16 billion and $2.164"）
- 2026-08-03｜CFO｜guidance：CFO 上調全年調整後營業利益財測（區間 48.89 億至 48.97 億美元）（原話："adjusted income from operations guidance to between"）
- 2026-08-03｜CFO｜guidance：CFO 上調全年調整後自由現金流財測至 45 億至 47 億美元（原話："free cash flow guidance to between $4.5 billion and"）
- 2026-08-03｜CFO｜guidance：策略性商業合約營收預期剩餘每季低於 50 萬美元（原話："these contracts to be less than $500,000 in each"）
- 2026-08-03｜CFO｜commitment：CFO 重申今年每一季都預期 GAAP 營業利益與淨利為正（原話："we continue to expect GAAP operating income and net income"）
- 2026-08-03｜CEO｜commitment：CEO 表示在推動整體業務未來 18 個月成長率不低於美國商業的成長率（原話："to what we have in U.S. commercial for the next 18 months"）
- 2026-08-03｜CFO｜margin：CFO 預告 Q3 費用將明顯增加（新進員工到職季節性）（原話："we expect a significant ramp in expense in the third quarter"）
- 2026-08-03｜CFO｜margin：CFO 說明調整後毛利率 86% 反映為某政府客戶承接雲端代管的成本增加（原話："an increase in costs associated with taking on cloud"）
- 2026-08-03｜CFO｜margin：CFO 給 Q2 調整後費用金額與季增、年增幅度（原話："Q2 adjusted expense was $741 million, up 14% sequentially"）
- 2026-08-03｜CFO｜margin：CFO 拆出 SpaceX 持股未實現利益對 GAAP EPS 與調整後 EPS 的貢獻（原話："RPO is primarily comprised of our commercial business"）
- 2026-08-03｜CFO｜margin：CFO 說明 RPO 的口徑：主要由商業業務組成，政府業務多不計入（原話："RPO is primarily comprised of our commercial business"）
- 2026-08-03｜CFO｜customer：CFO 報 Q2 淨美元留存率（原話："Net dollar retention was 157%"）
- 2026-08-03｜CFO｜customer：CFO 報美國商業 TCV 簽約額創紀錄（原話："record-setting $2.132 billion of U.S. commercial TCV"）
- 2026-08-03｜CFO｜customer：CFO 報美國商業客戶數（原話："Our U.S. commercial customer count grew to 653 customers"）
- 2026-08-03｜CFO｜customer：CFO 報國際商業營收成長率（對照美國商業 149%）（原話："international commercial revenue grew 26% year-over-year"）
- 2026-08-03｜CFO｜customer：CFO 報前 20 大客戶 TTM 營收成長（原話："top 20 customers increased 67% year-over-year"）
- 2026-08-03｜CRO｜customer：CRO 報百萬美元以上大單筆數創新高（原話："We closed 220 deals worth $1 million or more"）
- 2026-08-03｜CRO｜customer：CRO 舉一家跨國科技公司由單一營運公司擴展為約 3.7 億美元三年期合約（原話："converting to a 3-year nearly $370 million"）
- 2026-08-03｜CTO｜customer：CTO 指出美國國防部 TTM 營收占五角大廈預算比例仍低（原話："trailing 12-month revenue is still less than 25 basis points"）
- 2026-08-03｜CEO｜customer：CEO 稱舊客戶（原只用 Foundry）正轉向 Ontology，NDR 預期還會更好（原話："become even more positive"）
- 2026-08-03｜CTO｜product：CTO 稱首個政府 program of record 選擇 Maven 作為營運平台（原話："government program of record chose Maven as the platform"）
- 2026-08-03｜CTO｜product：CTO 報 Maven 平台上的建構者人數（原話："25,000 builders. Uniform service members, civilians"）
- 2026-08-03｜CTO｜product：CTO 描述 AIP 加入客戶安全邊界內的自動化模型工廠（後訓練）（原話："accumulates intelligence in weights they control"）
- 2026-08-03｜CTO｜product：CTO 舉例：未經後訓練的 Nemotron Ultra 在 5 項生產任務勝過前沿模型（原話："Within 24 hours of bringing Nemotron Ultra into our"）
- 2026-08-03｜CTO｜competition：CTO 描述與前沿實驗室的 bake-off：對手未交付價值（原話："failed to deliver anything of value against it"）
- 2026-08-03｜CRO｜competition：CRO 開場以 token 計費模式批評非 Palantir 的企業做法（原話："enterprises that are not using Palantir are seeing their"）
- 2026-08-03｜CTO｜competition：CTO 回答為何市場近一兩季才警覺：合作夥伴開始做出競爭性產品（原話："some of the people who were partners out there were"）
- 2026-08-03｜CEO｜competition：CEO 提及與 NVIDIA 建立合作夥伴關係，並說夥伴有時會與 Palantir 競爭（原話："we built a partnership with NVIDIA"）
- 2026-08-03｜CEO｜competition：CEO 談尋找夥伴的新方向：夥伴可偶爾與 Palantir 競爭（原話："They can occasionally compete against us."）
- 2026-08-03｜CEO｜risk：CEO 承認歐洲機構業務為出於信念而做、經濟面成長不佳（原話："supporting lots of institutions in Europe, the growth sucks"）
- 2026-08-03｜CFO｜capital_allocation：CFO 報期末現金與短期美國公債部位（原話："$9.2 billion in cash, cash equivalents and short-term"）
- 2026-08-03｜CFO｜capital_allocation：CFO 說明持續投入技術人才與研發（含主權 AI）（原話："supporting lots of institutions in Europe, the growth sucks"）

### 問答異常語氣（迴避／改口／保留）
- PLTR_Q2_2026_Earnings_Call_20260803.md｜問：Gil Luria（D.A. Davidson）問若客戶綁定單一實驗室模型、模型被下架時 Palantir 是否能換模型｜答法：CEO 先答 No，提到政府端已有可換模型的產品，隨後轉向壟斷資本主義、鎖定與企業憤怒等論述，未給客戶數或量化資訊；Ryan Taylor 與 Shyam 接續以合約結構與基準測試作答

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
{"date":"20260805","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Ontology＋FDE 是代理人時代的控制平面，模型商品化反而強化它","columns":{"2Y 驗證點":"US 商業 YoY &gt; 60%、NDR &gt; 130%","5Y 驗證點":"US 商業營收 &gt; 政府營收且 &gt; $8B","10Y 驗證點":"AIP 成跨產業事實標準（類比 ERP 之於 SAP）","具體數字門檻":"Q2 實績：US 商業 +149%、NDR 157%、TCV/營收比 2.79x","信息來源":"Q2 FY26 法說（08-03）＋該場的 bake-off 案例","漂移觸發":"連 2 季 US 商業 YoY &lt; 60% → 削弱"}},{"id":"H2","text":"成長的約束是部署人力而非需求或資本，故營收可在高基期續高速","columns":{"2Y 驗證點":"FY2027 營收 &gt; $11.5B（+41% 以上）","5Y 驗證點":"FY2031 營收 &gt; $28B、調整後營益率 &gt; 63%","10Y 驗證點":"單位部署成本隨模型代際下降，FDE 產能非線性放大","具體數字門檻":"FY26 guide $8.154B（+82%）；調整後費用 +37% vs 營收 +93%","信息來源":"公司 FY26 guide（08-03）＋費用揭露","漂移觸發":"連 4 季營收成長低於當期 guide 隱含值 → 削弱"}},{"id":"H3","text":"倍數正常化的速度慢於 EPS 複利速度，故長期報酬為正","columns":{"2Y 驗證點":"NTM 本益比不破 45x，且 FY+2 共識續上修","5Y 驗證點":"FY2031 本益比 ≥ 40x 且 EPS ≥ $5.6","10Y 驗證點":"EPS 複利吃掉倍數壓縮，10Y 累積 ≥ 2.4x","具體數字門檻":"NTM 82.2x、PEG 1.36；FY2027 共識 3 個月 +3.2%（$2.025→$2.09，stockanalysis／MarketBeat 08-06 雙源；yfinance eps_trend 曾示 $2.264 為單源離群值）","信息來源":"stockanalysis.com＋MarketBeat（08-06）＋賣方目標中位 $200（n=32）","漂移觸發":"跨 2 年度本益比持續 &lt; 40x 而 EPS 照長 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"US 商業飛輪由「加速」轉「高速但減速」——高基期算術必然發生，問題是斜率。若 QoQ 由 +28% 掉到 +12% 以內，市場將重定價成長性質","columns":{"對應假設":"H1／H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"US 商業 QoQ、NDR 變化率、TCV/營收領先比","警戒閾值":"QoQ 連 2 季 &lt; +15%，或 TCV/營收比 &lt; 1.8x"}},{"id":"R2","text":"歐洲主權 AI 的系統性排除（非單一國家個案）：歐盟執委會 2026-06-03 發布「歐洲技術主權套案」，對美國軟體建立對等程序性限制；德國聯邦國防軍 2026-04-28 公開排除並測試三家歐洲替代（年底前決標）；法國 DGSI 與德國 BfV 已轉向 ChapsVision 的 ArgonOS；西班牙指示各州機構排除 Palantir 採購；比利時／荷蘭／盧森堡／羅馬尼亞正評估法國 Artemis；法德 2026-07-17 聯合聲明以 Arcadia 平台對標 Maven。抵銷因子：NATO 本身作戰系統仍以 Palantir 為主力、無替代計畫。另美國陸軍 NGC2 共同資料層主導權 2026-06-22 由 Anduril 取得，Palantir 降為夥伴","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"國際政府與國際商業 QoQ（Q2 僅 +5%／+2%）、德國決標結果、歐盟套案實施細則、英國 FDP break clause","警戒閾值":"國際段任一季 QoQ 轉負，或英國動用 break clause"}},{"id":"R3","text":"Frontier lab 全棧複製：OpenAI Presence（2026-07-22）＋ DeployCo 自建 FDE（2026-05，收購 Tomoro 約 150 人）；Microsoft Agent 365（2026-05-01 GA）＋ Fabric IQ Ontology。攻擊者資本規模約為 Palantir 的 100 倍","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"frontier lab 企業部署具名客戶、Palantir top-10 商業客戶留存、AIP 相關續約折讓","警戒閾值":"任一 top-10 商業客戶遷出（＝§2.F 觸發），或 NDR 因價格競爭跌破 130%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔 $130-140（NTM ~68x、布林中軌）或 Q3 US 商業 QoQ ≥ +18% 且 NDR 未下滑","irr_base_pct":9.3,"ev5y_pct":54.4,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.7,"ev5y_pct":54.4,"irr_base_pct":9.3,"max_dd_pct":-65.0,"bull_5y_price":446.0,"bear_5y_price":60.0,"p_bull_pct":27.0,"p_bear_pct":28.0,"rearm_trigger":"回檔 $130-140（NTM ~68x、布林中軌）或 Q3 US 商業 QoQ ≥ +18% 且 NDR 未下滑","price_at_dd":162.66,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLTR_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
