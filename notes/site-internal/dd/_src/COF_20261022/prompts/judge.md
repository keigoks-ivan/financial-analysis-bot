你是 stock-analyst **v20 判斷 agent**，標的 COF（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"COF","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_net_revenue_gaap","label":"Total net revenue（GAAP）","value":16.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查到"},{"id":"f_kpi1_gaap_net_income_diluted_","label":"GAAP net income / diluted EPS","value":5.61,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD/share（淨利 $3.5bn）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查到（財報前 FY1 共識見 consensus_revision）"},{"id":"f_kpi2_adjusted_eps_non_gaap","label":"Adjusted EPS（non-GAAP，排除調整項）","value":6.69,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD/share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查到"},{"id":"f_kpi3_pre_provision_earnings_n","label":"Pre-provision earnings（non-GAAP）","value":7.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查到"},{"id":"f_kpi4_efficiency_ratio_gaap","label":"Efficiency ratio（GAAP／調整後）","value":54.19,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%（調整後 48.76%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查到"},{"id":"f_kpi5_provision_for_credit_los","label":"Provision for credit losses","value":2.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD bn（淨沖銷 $3.1bn；準備金釋出 $225m）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查到"},{"id":"f_kpi6_net_interest_margin","label":"Net interest margin","value":8.41,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查到"},{"id":"f_kpi7_cet1_ratio_basel_iii_sta","label":"CET1 ratio（Basel III Standardized，初步）","value":13.8,"period":"2026-09-30（Q3 2026 公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"2026-09-30（Q3 2026 公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"n/a"},{"id":"f_kpi8_period_end_loans_held_fo","label":"Period-end loans held for investment","value":462.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"n/a"},{"id":"f_kpi9_period_end_deposits","label":"Period-end deposits","value":480.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-20","period":"2026-10-20","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cof_fcf_margin_pct","label":"COF FCF 利潤率","value":47.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COF.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_axp_fcf_margin_pct","label":"AXP FCF 利潤率","value":19.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jpm_fcf_margin_pct","label":"JPM FCF 利潤率","value":-83.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JPM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_c_fcf_margin_pct","label":"C FCF 利潤率","value":-26.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.C.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_gross_margin_pct","label":"V 毛利率","value":80.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_operating_margin_pct","label":"V 營業利益率","value":65.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_fcf_margin_pct","label":"V FCF 利潤率","value":47.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":206.66,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":4.44,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":58.63,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.56 → 20.56）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（24.07 → 24.07）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（28.08 → 28.08）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":20.56,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":24.07,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":28.08,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.31,"period":"2026-07-16 → 2026-10-21","unit":"%","basis":"FY1 共識 EPS 19.71 → 20.56（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":13.27,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝14.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":14.7,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.59,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.61,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":10.05,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 20.56，分子＝快照價 206.66","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.548,"period":"2026-10-22","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-22"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":885.0,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 49774.0、現金 48889.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":613.48,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":127667.78,"period":"2026-10-22","unit":"USD m","basis":"市值 126782.78 ＋ 淨負債 885.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":64060.01,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（14 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":67545.92,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.99,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 206.66 / W52 206.2 / W104 199.27 / W250 149.35 / W250 13週斜率 0.7%"},{"id":"f_ma_w52","label":"52 週均線","value":206.2,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":199.27,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":149.35,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.7,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出收購 Global Payment Network 後，COF 與其他支付網路競爭 Network Partners，並與 Visa、Mastercard 的競爭可能影響既有合作；另面臨穩定幣、代幣化存款等新興替代支付業者。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"As a result of our recent acquisition of the Global Payment Network, we now face substantial and increasingly intense competition in the payments industry, both from traditional players and new, emerging alternative payment providers.","as_of":"2026-02-19","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出部分競爭者（含數位與行動支付、金融科技業者）不受同等監管，且部分對手規模遠大於 COF，可能在資金成本與通路上占優。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"Some of our competitors are substantially larger than we are, which may give those competitors advantages, including a more diversified product and customer base, the ability to reach more customers and potential customers, operational efficiencies, broad-based local distribution capabilities, lower-cost funding and larger existing branch networks.","as_of":"2026-02-19","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"2026 Q2 信用卡購買量約 2,538 億美元，年增 26%（含 Discover 併入效應）；舊 Discover 購買量年增不到 2%，舊 Capital One 業務約 14%；搜尋結果未見美國網路份額的 2026 數據。","source":"eMarketer：Capital One's Q2 earnings size up the new titan of the credit card industry","url":"https://www.emarketer.com/content/capital-one-s-q2-earnings-","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"COF 已完成簽帳卡轉到 Discover 網路，並測試信用卡轉移。","source":"PYMNTS：Capital One Tests Moving Credit Cards to Discover Network","url":"https://www.pymnts.com/dashboard-post/earnings/2026/capital-one-tests-moving-credit-cards-to-discover-network/","excerpt":"Capital One Tests Moving Credit Cards to Discover Network By PYMNTS | July 21, 2026 | Listen to Article Listen Highlights Capital One card purchase volume reached $253.8 billion, while legacy Discover purchase volume increased just under 2%. Capital One completed its debit conversion to the Discover network and is now testing Capital One credit","as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Capital One Q2 2026 財報後報導：約 2,500 萬張簽帳卡已轉至 Discover 網路；舊 Discover 購買量年增不到 2%，Capital One 其他業務（含 Brex）購買量約增 14%；舊 Discover 卡放款年減 1.5%（管理層稱為刻意收縮高餘額循環戶）。數字出自新聞報導，未核對公司原始財報。","source":"PaymentsJournal: After moving debit cards to Discover, Capital One turns to credit card migration","url":"https://www.paymentsjournal.com/after-moving-debit-cards-to-discover-capital-one-turns-to-credit-card-migration/","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"KPMG 2026 年 4 月發卡機構簡報：10% 信用卡利率上限法案（S.381／H.R.1944）尚未出委員會、聯邦利率上限未立法；KPMG 稱 10% 上限可能對發卡機構經濟性造成重大影響，包含收緊核貸標準、信用可得性下降。","source":"KPMG: Top of Mind – Credit Card Issuers, April 2026","url":"https://kpmg.com/kpmg-us/content/dam/kpmg/pdf/2026/top-of-mind-credit-card-issuers-april-2026.pdf","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261022","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Capital One 正測試將部分信用卡移至 Discover 網路，量與時程未揭露。","source":"PYMNTS: Capital One Tests Moving Credit Cards to Discover Network","url":"https://www.pymnts.com/dashboard-post/earnings/2026/capital-one-tests-moving-credit-cards-to-discover-network/","excerpt":"Capital One Tests Moving Credit Cards to Discover Network By PYMNTS | July 21, 2026 | Listen to Article Listen Highlights","as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 載明 Brex 收購的交割條件包含 Hart-Scott-Rodino 反壟斷申報許可。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"The completion of the Brex Transaction is subject to the satisfaction of customary closing conditions, including clearance under the Hart-Scott-Rodino Antitrust Improvements Act of 1976, as amended.","as_of":"2026-02-19","retrieved_at":"20261022","affects":["triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因子：監管機關可能限制公司的併購或擴張能力，且重疊調查、罰款、限制產品等可能損害業務。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"which could involve restrictions on our activities, or our ability to make acquisitions or otherwise expand our business, among other limitations that could adversely affect our business.","as_of":"2026-02-19","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 載明商家與商家團體對發卡銀行（含公司）提起多起反壟斷訴訟，主張交換費等做法違反聯邦反壟斷法；英國、加拿大等地對交換費設有上限或自願協議。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"Merchants and their trade groups have filed numerous lawsuits against payment card networks and banks that issue cards on those networks, claiming that their practices toward merchants, including interchange fees, violate federal antitrust laws.","as_of":"2026-02-19","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Law360 報導一群消費者請求加州聯邦法官阻止 Capital One 51.5 億美元收購 Brex，主張違反反壟斷法（付費牆，未見裁定結果）。","source":"Law360 'Capital One's $5B Brex Purchase Must Be Blocked, Judge Told'","url":"https://www.law360.com/articles/2453319","excerpt":null,"as_of":"2026-03-16","retrieved_at":"20261022","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#4","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Capital One 完成 Brex 收購，稱已取得所有必要監管核准與交割條件。","source":"Nasdaq 'Capital One Completes Brex Buyout, Boosts Digital Payments Strategy'","url":"https://www.nasdaq.com/articles/capital-one-completes-brex-buyout-boosts-digital-payments-strategy","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261022","affects":["triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"COF 10-K FY2025 風險因素把貿易戰、貿易壁壘、關稅、制裁與供應鏈中斷（含對汽車產業的影響）列為可能影響其業務的總體風險；非直接產品／供應鏈暴露。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"Trade wars, trade barriers, tariffs, economic sanctions, labor shortages and disruptions of global supply chains, including their impacts on the auto industry;","as_of":"2026-02-19","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"COF 10-K 說明須遵守 OFAC 等制裁法規（合規義務，非出口管制清單事件）。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"We are also required to comply with sanctions laws and regulations administered and imposed by the United States government, including the U.S. Treasury Department's Office of Foreign Assets Control (“OFAC”) and the Department of State","as_of":"2026-02-19","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：核心IT基礎設施與客戶應用已大部分遷至雲端，AWS為主要供應商；雲端供應商中斷可能造成服務中斷與非預期成本","source":"SEC EDGAR Capital One FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":null,"as_of":"2026-02-27","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 Q2 國內卡營收年增約 30%（多為併入 Discover 部分季度）；剔除 Discover 年增 9.5%。","source":"Nasdaq／MarketBeat：Capital One Financial Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/capital-one-financial-q2-earnings-call-highlights-2026-07-21/","excerpt":"Revenue was up 30% from the second quarter of 25, largely driven by the addition of a partial quarter of Discover revenue. Excluding Discover, year over year revenue growth was 9.5%","as_of":"2026-07-21","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"2026 Q2 國內卡期末貸款年增 2.6%，原 Discover 卡貸款年減 1.5%，管理層稱為預期中的暫時性「brownout」。","source":"Nasdaq／MarketBeat：Capital One Financial Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/capital-one-financial-q2-earnings-call-highlights-2026-07-21/","excerpt":"Ending domestic card loan balances increased 2.6% year over year. Legacy Discover card loans declined 1.5%, which Fairbank said was in line with management's expectations for a temporary \"brownout\" in Discover loan growth.","as_of":"2026-07-21","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 Q2 國內卡沖銷率 4.71%，較上季降 39bp、較去年同期降 54bp。","source":"Nasdaq／MarketBeat：Capital One Financial Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/capital-one-financial-q2-earnings-call-highlights-2026-07-21/","excerpt":"The domestic card charge-off rate was 4.71%, down 39 basis points from the first quarter and 54 basis points from a year earlier.","as_of":"2026-07-21","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"COF 10-K 風險因子列出「AI、機器人與加密貨幣推動的產業技術顛覆」為總體風險項目之一，未點名具體替代技術取代其信用卡產品","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"Technology-driven disruption of certain industries, such as those due to advances in AI, robotics and cryptocurrency;","as_of":"2026-02-19","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"BofA Global Research 2026-07 報告稱代理商務／穩定幣對卡網的擔憂較屬估值壓力而非基本面現實","source":"BofA, Will agentic commerce stay on the rails?","url":"https://business.bofa.com/en-us/content/agentic-commerce-and-stablecoin-payments.html","excerpt":"Will agentic commerce stay on the rails? Perspectives from BofA Global Research’s Leading Analysts July 22, 2026 Matthew O’Neill, Senior Research Analyst, Payments, Processors & IT Services, Consumer Finance Agentic & Stablecoin: Threat or Rail?","as_of":"2026-07-10","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"a16z crypto 論點：代理商務不會殺死信用卡，因卡提供信用、預授權與拒付保護","source":"a16z crypto, Agentic commerce won't kill cards, but it will open a gap","url":"https://a16zcrypto.substack.com/p/agentic-commerce-wont-kill-cards","excerpt":"The Citrini thesis rests on an assumption: that AI agents, freed from human habit, will optimize away interchange fees. But cards don’t just move money. They extend unsecured credit, pre-authorize uncertain transactions, and guarantee fraud protection with chargeback rights.","as_of":"2026-03-04","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"COF 已完成約 2,500 萬張簽帳卡轉至 Discover 網路並開始測試信用卡轉移","source":"PaymentsJournal, After moving debit cards to Discover, Capital One turns to credit card migration","url":"https://www.paymentsjournal.com/after-moving-debit-cards-to-discover-capital-one-turns-to-credit-card-migration/","excerpt":"Debit Digital Assets & Crypto Digital Banking Emerging Payments Fraud & Security Merchant Prepaid Commercial Credit Debit Digital Assets & Crypto Digital Banking Emerging Payments Fraud & Security Merchant Prepaid No Result View All Result No Result View All Result After Moving Debit Cards to Discover, Capital One Turns to Credit Card Migration","as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Capital One 已把約 2,500 萬張簽帳卡換到 Discover 網路；Q2 2026 財報會上表示開始測試把部分信用卡由 Visa 移到 Discover 網路（新發卡與既有帳戶轉換），尚未公布最終轉移量與時程。","source":"PaymentsJournal｜After moving debit cards to Discover, Capital One turns to credit card migration","url":"https://www.paymentsjournal.com/after-moving-debit-cards-to-discover-capital-one-turns-to-credit-card-migration/","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q1 2026 財報報導：新發行卡預計於 Q3 底前全數走 Discover 網路，全組合轉換至 2027 Q1；營收年減 2% 至 152 億美元，管理層歸因於 Discover 網路與 Brex 的轉換成本。","source":"eMarketer｜Capital One Q1 2026 earnings reflect tightened underwriting, groundwork for Discover transition","url":"https://www.emarketer.com/content/capital-one-q1-2026-earnings-reflect-tightened-underwriting--groundwork-discover-transition","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Capital One 宣布以 51.5 億美元收購企業費用管理平台 Brex（27.5 億現金加約 1,060 萬股），延伸至中小企業與商業客戶的平台化布局。","source":"PYMNTS｜Capital One Plans to Acquire Expense Management Platform Brex for $5.15 Billion","url":"https://www.pymnts.com/acquisitions/2026/capital-one-plans-to-acquire-expense-management-platform-brex-for-5-15-billion/","excerpt":null,"as_of":"2026-01-22","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Capital One 開始測試將信用卡移至 Discover 網路","source":"PYMNTS","url":"https://www.pymnts.com/dashboard-post/earnings/2026/capital-one-tests-moving-credit-cards-to-discover-network/","excerpt":"Legacy Discover card loans declined 1.5% from a year earlier, while ending loans excluding Discover increased about 5.3%. Chairman and CEO Richard Fairbank said Discover remains in what Capital One has called a “brownout” in loan growth during the integration.","as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat（2026-07-31 收盤時點）：24 位分析師 12 個月目標價均值約 $259，最高 $300、最低 $222；20 買進、4 持有，共識評等 Moderate Buy。","source":"MarketBeat COF forecast","url":"https://www.marketbeat.com/stocks/NASDAQ/COF/forecast/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 同期口徑較低：20 位分析師平均目標價約 $236（18 買、2 持有）；Citigroup 於 7/28 把目標價降到 $295，Evercore ISI 同日升到 $230。各聚合站樣本數與均值不一致。","source":"Benzinga COF price targets","url":"https://kr.benzinga.com/quote/COF/price-targets","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026 摘要：淨利 $3.0B、稀釋 EPS $4.73、調整後 EPS $5.81；管理層預期卡與個人貸款餘額縮減持續到 2026 Q4，Discover 綜效 $2.5B 預計 2027 年達成。","source":"Quartr Capital One Q2 2026 earnings summary","url":"https://quartr.com/events/capital-one-financial-corporation-cof-q2-2026_3Y1TBpuY","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Hudson Labs Q3 2026 預覽：公司沒有明確 EPS 或效率比 guidance，只說併購後獲利能力將符合交易時預期；Q3 市場共識營收 $16.3B、EPS $4.52；描述 Q3 為過渡季，行銷與科技支出仍高。","source":"Hudson Labs COF Q3 2026 earnings preview","url":"https://www.hudson-labs.com/research/capital-one-q3-2026-earnings-preview-cof-results-preview","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261022","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"TickerLeague（約 2026 年 7 月下旬）：6 位分析師目標價共識約 $253.82，區間 $229–$300；HSBC 7/13 由 Hold 升 Buy。修正趨勢資料不足。","source":"TickerLeague COF estimates","url":"https://tickerleague.com/companies/COF/estimates","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q1 2026 調整後 EPS $4.42 低於共識 $4.50，信用損失準備 $4.07B 高於預期（來源為低品質聚合站，待核）；BofA 維持 Buy、目標價 $234。","source":"accred.deac.org 聚合頁（Q1 2026 Earnings Miss）","url":"https://accred.deac.org/expert-time/Capital-One-Financial-Corporation-COF-Q1-2026-Earnings-Miss-Across-Three-Core-Metrics-Sparks-Consumer-Resilience-Concerns-10-6902","excerpt":null,"as_of":"2026-04-23","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"Discover 卡片產品誤分類：商家集體訴訟和解獲法院初步核准（2025-07-30），Discover 提列 12 億美元；股東集體訴訟 2025-03-31 被駁回（無損害駁回），原告 5-14 申請修訂；Discover 另受 SEC 調查，公司配合中。","source":"SEC EDGAR 10-K FY2025 Item 8 附註","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"Discover reserved $1.2 billion related to this matter and the class action settlement will be the primary means through which restitution will be paid to adversely affected merchants, merchant acquirers and other intermediaries.","as_of":"2026-02-19","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Discover 整合進行中：預計 2026-07-27 起分批把 Discover 帳戶遷移至 Capital One 系統；目標 2027 年中前至少 25 億美元綜效；2026 Q2 調整後 EPS 5.81、GAAP EPS 4.73（整合成本拉開差距）。","source":"Motley Fool／PaymentsJournal 搜尋摘要（2026-07）","url":"https://www.fool.com/investing/2026/07/25/what-the-capital-one-discover-tie-up-means-for-the/","excerpt":null,"as_of":"2026-07-25","retrieved_at":"20261022","affects":["thesis.H","thesis.R","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026-04-15 於維吉尼亞東區聯邦法院提起集體訴訟，指控單方關閉帳戶並取消已賺得信用卡回饋；2026-06-04 另案指控因錯誤「已故」註記關閉帳戶未依 ECOA 發出不利行動通知。","source":"Law360「Capital One Hit With Class Action Over Canceled Rewards」；Top Class Actions 2026-06-26","url":"https://law360.com/articles/2466514","excerpt":null,"as_of":"2026-06-26","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"360 Savings 利率集體訴訟 4.25 億美元和解於 2026-04-20 獲最終核准。","source":"Top Class Actions","url":"https://topclassactions.com/lawsuit-settlements/open-lawsuit-settlements/425m-capital-one-360-savings-account-class-action-settlement/","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"COF 2026 Q2 合併淨沖銷率 1.48%，較去年同期升 18bp；上半年 1.59%，升 14bp（搜尋摘要轉述，未讀原頁）","source":"Capital One Form 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000927628/000092762826000089/cof-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"+","claim":"COF 2026 Q2 釋放撥備 $662M，撥備餘額約 $230 億，總組合覆蓋率降 26bp 至 5.02%；信用撥備提列 $30 億，較前季減 27%；國內卡沖銷率 4.71%、逾期 3.39%（二手轉述，未核原文）","source":"vectorshift / roic.ai Q2 2026 earnings call summaries","url":"https://vectorshift.ai/research/companies/capital-one-financial/earnings/2026-q2","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"financial_capital_credit_cycle#2","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"Hudson Labs 預覽：沖銷與逾期率優於季節性，管理層仍提示總經不確定","source":"Hudson Labs COF Q3 2026 Earnings Preview","url":"https://www.hudson-labs.com/research/capital-one-q3-2026-earnings-preview-cof-results-preview","excerpt":"Credit quality: Charge-off and delinquency rates have been better than seasonality, but management continues to flag macro uncertainty (inflation, energy prices).","as_of":"2026-10-05","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#3","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"S&P Global：五大發卡行 2 月平均淨損失率 1.97%，低於 12 個月平均 2.02%；季調逾期自 2025 年 8 月後持平","source":"S&P Global Market Intelligence","url":"https://www.spglobal.com/market-intelligence/en/news-insights/articles/2026/3/average-delinquency-rates-at-top-credit-card-issuers-were-stable-in-february-99525369","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"financial_regulatory_capital_rules#0","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"Fed 於 2026-02-04 通知各銀行將 SCB 維持現水準（待壓力測試透明化提案公開徵詢）；COF 的 SCB 為 4.5%，10-Q 稱維持至 2027-09-30，CET1／Tier1／總資本最低要求為 9.0%／10.5%／12.5%，反景氣緩衝 0%。","source":"Capital One Form 10-Q Q2 2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000927628/000092762826000089/cof-20260630.htm","excerpt":"On February 4, 2026, the Federal Reserve notified all participating firms, including the Company, that because the Stress Testing Transparency Proposal remains subject to public comment, the Federal Reserve is maintaining stress capital buffer requirements for all such firms at their current levels.","as_of":"2026-06-30","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"financial_regulatory_capital_rules#1","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"Fed 2026 壓力測試結果（2026-06-24 公布）未改變 COF 的 SCB 要求；4.5% SCB 係在 Discover 併購完成前以 COF 單獨計算。","source":"Capital One Announces Stress Test Results (Business Wire, 2026-06-24)","url":"https://www.streetinsider.com/Business+Wire/Capital+One+Announces+Stress+Test+Results/26686276.html","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"financial_regulatory_capital_rules#2","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"三大銀行監管機關 2026-03-19 發布 Basel III endgame 再提案：強制 ERBA 僅適用 Category I、II；Category III、IV 須將 AOCI 計入監管資本；另有標準法修正提案。搜尋未見最終規則。","source":"Simpson Thacher, Basel III Endgame Evolution (2026-03-20)","url":"https://www.stblaw.com/about-us/publications/view/2026/03/20/basel-iii-endgame-evolution-banking-agencies-propose-major-capital-overhaul-again","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"financial_regulatory_capital_rules#3","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"Fed 2026 壓力測試結果：COF 嚴重不利情境下 CET1 最低預測 11.0%。","source":"Federal Reserve 2026 June DFAST results","url":"https://www.federalreserve.gov/publications/2026-june-dodd-frank-act-stress-test-results.htm","excerpt":"Projected minimum common equity tier 1 capital ratio under the severely adverse scenario, 2026:Q1–2028:Q132 banks Percent Bank Stressed ratios with supervisory stress testing capital action assumptions Ally 7.8 American Express 9.7 Bank of America 9.9 Bank of NY-Mellon 11.8 Barclays US 12.3 BMO 10.1 Capital One 11.0","as_of":"2026-06-24","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Discover 整合進行中：預計 2026-07-27 起分批遷移帳戶；綜效目標 2027 年中前至少 25 億美元。","source":"Motley Fool 搜尋摘要","url":"https://www.fool.com/investing/2026/07/25/what-the-capital-one-discover-tie-up-means-for-the/","excerpt":null,"as_of":"2026-07-25","retrieved_at":"20261022","affects":["thesis.H","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Discover 卡片產品誤分類商家集體訴訟和解，提列 12 億美元；股東集體訴訟曾被駁回後申請修訂。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"Discover reserved $1.2 billion related to this matter and the class action settlement will be the primary means through which restitution will be paid to adversely affected merchants, merchant acquirers and other intermediaries.","as_of":"2026-02-19","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-04-15 回饋取消集體訴訟（維吉尼亞東區）。","source":"Law360","url":"https://law360.com/articles/2466514","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"Discover 曾受 SEC 就卡片產品誤分類事件調查，公司配合中。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm","excerpt":"Discover was also subject to an SEC investigation into the Card Product Misclassification matter. We are cooperating with the investigation.","as_of":"2026-02-19","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#1","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 31 份 8-K 中無 4.02（財報不可信賴）項目。","source":"SEC EDGAR 8-K 清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000927628&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 31 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"COF","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":47.95,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COF","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AXP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":19.82,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXP","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"JPM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-83.39,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JPM","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"C","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-26.88,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.C","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"V","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":80.18,"operating_margin_pct":65.61,"fcf_margin_pct":47.23,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"COF"},"financial_history":{"ticker":"COF","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":34250000000.0,"revenue_yoy_pct":null,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":7360000000.0,"diluted_eps":17.91,"free_cash_flow":12875000000.0,"fcf_margin_pct":37.59,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":36787000000.0,"revenue_yoy_pct":7.41,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":4887000000.0,"diluted_eps":11.95,"free_cash_flow":19614000000.0,"fcf_margin_pct":53.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":39112000000.0,"revenue_yoy_pct":6.32,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":4750000000.0,"diluted_eps":11.59,"free_cash_flow":16955000000.0,"fcf_margin_pct":43.35,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":53434000000.0,"revenue_yoy_pct":36.62,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":2453000000.0,"diluted_eps":4.03,"free_cash_flow":26140000000.0,"fcf_margin_pct":48.92,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/COF/COF_Q3_2026_Earnings_Call_20261020.md）

# Q3 2026 Earnings Call
**Capital One Financial Corporation** | Earnings Calls | 2026-10-20

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to the Capital One Q3 2026 Earnings Call. Please be advised that today's conference is being recorded. [Operator Instructions] 
I would now like to hand the conference over to your speaker today, Jeff Norris, Senior Vice President of Finance. Please go ahead.

**Jeff Norris** (Executives):
Thanks very much, Josh, and welcome, everybody. To access the live webcast of this call, please go to the Investors section of Capital One's website, capitalone.com. A copy of the earnings presentation, press release and financial supplement can also be found in the Investors section of Capital One's website, capitalone.com, by selecting financials and then quarterly earnings releases.  
With me tonight are Mr. Richard Fairbank, Capital One's Chairman and Chief Executive Officer; and Mr. Andrew Young, Capital One's Chief Financial Officer. Rich and Andrew are going to walk you through the presentation summarizing our third quarter results for 2026.  
Please note that this presentation may contain forward-looking statements. Information regarding Capital One's financial performance and any forward-looking statements contained in today's discussion and the materials speak only as of the particular date or dates indicated in the materials. And Capital One does not undertake any obligation to update or revise any of this information whether as a result of new information, future events or otherwise. Numerous factors could cause our actual results to differ materially from those described in forward-looking statements. For more information on these factors, please see the section titled Forward-Looking Statements in the earnings release presentation and the Risk Factors section of our annual and quarterly reports accessible at Capital One's website and filed with the SEC.  
And now I'll turn the call over to Mr. Young. Andrew?

**Andrew Young** (Executives):
Thanks, Jeff, and good afternoon, everyone. I will start on Slide 3 of tonight's presentation. In the third quarter, Capital One earned $3.5 billion or $5.61 per diluted common share. The results for the quarter included several adjusting items related to the Discover and Brex acquisitions, which are outlined on the slide. Net of these adjusting items, third quarter earnings per share were $6.69.  
Relative to the prior quarter, both period end and average loans held for investment increased 1% while period end and average deposits decreased 1%. Linked quarter revenue increased 3% and noninterest expense declined 2%, resulting in preprovision earnings growth of 10%. On an adjusted basis, preprovision earnings grew 9% quarter-over-quarter. Our provision for credit losses decreased $73 million or 2% to $2.9 billion in the quarter. The provision reflects $3.1 billion of net charge-offs and an allowance release of $225 million.  
Turning to Slide 4. I'll cover the allowance in greater detail. The $225 million allowance release in the quarter brought the allowance balance to $22.7 billion. Our total portfolio coverage ratio decreased 10 basis points and now stands at 4.92%. I'll cover the drivers of the changes in allowance and coverage ratio by segment on Slide 5.  
In our Domestic Card business, we released $250 million of allowance. The allowance release was driven by continued favorable observed credit in the quarter, partially offset by greater consideration to downside economic scenarios related to geopolitical risks. The coverage ratio decreased by 13 basis points and now stands at 6.86%.  
In our Consumer Banking segment, we built $41 million of allowance. The allowance build was primarily driven by strong growth in the auto business, partially offset by an improved outlook for vehicle values. The coverage ratio ended the quarter at 2.34%, 5 basis points lower than the second quarter.  
And finally, in our Commercial Banking segment, the allowance balance was flat at about $1.5 billion, and the coverage ratio declined by 2 basis points to 1.6%.  
Turning to Page 6. I'll now discuss liquidity. Total liquidity reserves ended the second quarter at about $134 billion, down $10 billion from the prior quarter. Our ending cash position decreased by about $6 billion to approximately $49 billion. The market value of our investment securities decreased by about $3 billion. Our preliminary average liquidity coverage ratio in the quarter was 163%. 
Turning to Page 7, I'll cover our net interest margin. Our third quarter net interest margin was 8.41%, 40 basis points higher than the prior quarter. The increase was driven by higher yield in the Domestic Card business, a $13 billion decline in average cash balances and an additional day in the quarter.  
Turning to Slide 8. I will end by discussing our capital position. Our common equity Tier 1 capital ratio ended the quarter at 13.8%, roughly flat to the second quarter as net income in the quarter was largely offset by share repurchases of $2.6 billion, dividends and growth.  
With that, I will turn the call over to Rich. Rich?

**Richard Fairbank** (Executives):
Thanks, Andrew, and welcome, everyone, to our earnings call this evening. Slide 10 shows third quarter results in our Credit Card business. Credit Card segment results are largely a function of our Domestic Card results and trends, which are shown on Slide 11. The Domestic Card business posted another quarter of top line growth and strong credit results. Year-over-year trends in domestic card results now fully incorporate the impacts of the Discover acquisition. Year-over-year and quarterly comparisons continue to reflect the much smaller effect of adding Brex to the Domestic Card business and moving our small legacy corporate Credit Card business from the commercial bank to Domestic Card in the second quarter of this year.  
Third quarter purchase volume grew 11% year-over-year, primarily driven by growth in legacy Capital One purchase volume. The addition of Brex and the Corporate Card business in the second quarter was a modest tailwind to purchase volume growth, while legacy Discover purchase volume was a modest headwind. Because of the Discover loan growth brownout, legacy Discover purchase volume was essentially flat compared to the prior year quarter.  
Ending loan balances increased about 2% year-over-year. The legacy Discover card loans shrank about 3% from the prior year as the temporary brownout of Discover loan growth continued. Excluding Discover, ending loans grew about 6%. Revenue was up 5% from the third quarter of 2025, driven by growth in legacy Capital One purchase volume and loans. Revenue margin for the quarter was 17.8%. The Domestic Card charge-off rate for the third quarter was 3.98%, down 73 basis points from the prior quarter and down 65 basis points year-over-year. Our charge-offs are benefiting from the steady improvement in delinquencies that we observed in the first half of this year and from strong recoveries performance. The delinquency rate was 3.74% at quarter end, up 35 basis points from the linked quarter and down 15 basis points from a year ago. The linked quarter trend was in line with normal seasonality.  
Domestic Card noninterest expense was up 9% compared to the third quarter of 2025, driven by continuing technology investments, higher marketing and the addition of Brex. Our choices in Domestic Card are the biggest driver of total company marketing. Total company marketing expense in the quarter was about $1.6 billion, up 14% year-over-year, driven by higher direct marketing in our Domestic Card business, increased media spend and continuing investments in premium benefits. As we look ahead to the fourth quarter, we expect the Q3 to Q4 percentage growth in marketing to be similar to the Q3 to Q4 percentage growth we saw in 2025, primarily driven by seasonality.  
Slide 12 shows third quarter results in our Consumer Banking business. Global payment network transaction volume for the quarter was approximately $191 billion. Network transaction volume increased 25% compared to the third quarter of 2025, driven primarily by the successful conversion of Capital One debit customers to the Discover Network. Auto originations were up 22% from the prior year quarter. We continue to be in a strong position to pursue resilient growth in the current marketplace.  
Consumer Banking ending loan balances increased about $11 billion or about 13% year-over-year. Average loans were up 12%. Both ending and average deposit balances declined about 1% from the linked quarter, driven by volume impacts and choices related to the Discover integration including the sale of a small IRA portfolio we acquired from Discover. Legacy Capital One retail deposits continued to grow.  
Consumer Banking revenue for the quarter was up about 17% year-over-year, driven predominantly by Discover revenue synergies and growth in auto loans. Noninterest expense was up about 10% compared to the third quarter of 2025, driven by increased auto originations and continued technology investments. The auto charge-off rate for the quarter was 1.59%, up 5 basis points year-over-year and up 16 basis points from the sequential quarter. The year-over-year increase is largely the result of a gradual mix shift in new originations and loans as our subprime mix is returning to prepandemic levels. The auto delinquency rate was 4.64%, up 32 basis points from the linked quarter and down 35 basis points from the prior year.  
Slide 13 shows third quarter results for our Commercial Banking business. Compared to the linked quarter, both ending and average loan balances were up about 1%. Ending and average deposits were also up about 1% from the linked quarter. Revenue increased 6% from the linked quarter with strong growth in noninterest income. Noninterest expense was up about 1%. The Commercial Banking net charge-off rate for the second quarter was 0%. The commercial criticized performing loan rate was 4.4%, down 4 basis points compared to the linked quarter. The criticized nonperforming loan rate was down 10 basis points to 1.22%.  
In closing, third quarter results continued to reflect solid top line growth and strong credit performance. The third quarter is a seasonally strong quarter in most years with seasonal strength in margins and charge-offs. And this year, the quarterly results also benefited from an allowance release.  
Looking ahead, we expect to lean harder into marketing in 2027, driven by several factors. We're fully pursuing our origination opportunities and the window is open across our businesses. Our biggest competitors continue to invest heavily in marketing, and we need to be at the top of our game. Also, we plan to now lean back into Discover marketing. The trend of marketing increases is also powered by a gradual mix change, some of the biggest growth areas in the company are businesses where marketing is inherently a much larger component of the business model. That includes our quest at the top of the market with heavy spenders, Capital One Shopping, and our National Banking business. These businesses take a lot of marketing to build, but are great franchises with lower risk, lower capital and long-term revenue annuities.  
The Discover integration continues to go well, and we're making good progress on delivering the expected synergies. On a combined basis, we're achieving the expected synergies ahead of schedule. Our year-to-date results reflect about $1.8 billion of annualized combined synergies, primarily driven by the successful debit conversion early in 2026 and the pace of achieving expense synergies. We have talked for a while now about the earnings power on the other side of integration. You can squint your eyes and see it now in the first 3 quarters of 2026. You would need to normalize for sizable -- for the sizable allowance release we've had thus far this year. And to add, the increased marketing we expect in the fourth quarter.  
Looking forward, you would add in the remaining synergies we expect to get and probably deduct the lost interchange revenue that will likely come from the Visa-Mastercard settlement. Our current view is that the remaining synergies and the Visa-Mastercard settlement are roughly offsetting in magnitude. With those adjustments, that's a view into the run rate earnings power coming out of this deal, and it's consistent with what we expected at the time we announced the deal. Pulling way up, we've worked for years to put ourselves in a strong position to win in a rapidly changing marketplace. We continue to lean into investments in modern technology, data and AI. We continue to gain traction as we build enduring franchises with heavy spenders at the top of the credit card marketplace and with primary banking relationships in our national retail bank. And we're building momentum from the game-changing acquisition of Discover.  
And now we'll be happy to answer your questions. Jeff?

**Jeff Norris** (Executives):
Thank you, Rich. We'll now start Q&A session. [Operator Instructions] Josh, please start the Q&A.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Terry Ma with Barclays.

**Terry Ma** (Analysts):
I appreciate the color on the fourth quarter marketing and also the outlook for marketing in 2027. But as we kind of think about it, how do you measure the return on the investment for those marketing dollars? Maybe, for example, the dollars allocated to the Discover brownout since there is a lag between deployment of those dollars to account generation to balance growth, like should we expect you to keep leaning into marketing ahead of the loan growth materializing?

**Richard Fairbank** (Executives):
Thank you, Terry. So we built a company that was designed for organic growth, ironic that I say this at the time we're talking about having done the big acquisition of Discover. But marketing is right at the heart of this model. And as we've talked about many times, we run our company based on horizontal economics, where before an investment -- before, during and after an investment, we horizontally measure the performance and make adjustments if necessary. But the key thing is that methodology is really quite different from vertical accounting where one is trying to see how anything is doing based on vertical performance.  
Vertical-focus systematically underweights and underappreciates the value of investment over the longer term. So that's why if you pull way up on Capital One with our philosophy of horizontal accounting and building an organic growth company, we have, over the years, invested heavily to be where we are today. And over time, the vertical returns, in some sense, on a lag basis manifest that.  
Let's talk about marketing in particular. So for starters, the marketing machine of Capital One, much of it is a direct marketing machine that is pretty much stimulus response, measures things pretty quickly with respect to what are we -- what is -- what we're getting in terms of booking new accounts for an investment in marketing. But there's also a whole other component that doesn't lend itself as easily to stimulus response thing, and I put at the top of that list building a brand. And -- but also included in that is it's hard to measure the return on investments in some of the things we're doing at the very top of the market, the unique experiences, the lounges. So there are -- this will never lend itself to be all of it an exactly stimulus response measurable effect.  
But what we do is we pull up not only with respect to each choice that we make, but then pull up with respect to larger aggregations like our businesses themselves and look at their performance over time, and that's a very, very important part of our decision-making.  
The other thing I want to say -- but if we stand back, it is, to your point, Terry, it's striking to notice that the growth rate of marketing over the last number of years has been higher than the growth rate of revenue, the growth rate of other expenses. And so that -- of course, one can stand back and ask, but wait a minute, that's what exactly is going on. And that's why I wanted to make the point here in my earlier remarks that the businesses where we are really leaning in and growing the most are businesses that have a high marketing component to them. Obviously, winning at the top of the market with heavy spenders is a very sort of marketing intensive business, high cost of acquisition and high cost of things that the customers care a lot about, the building a brand, all of that.  
But I also want to point out on the National Bank. All the other major banks out there that the growth strategy they have is buying other banks. And that's not our growth strategy. We are organically building a national bank. And without a lot of branches on the corner, marketing is really the engine for that. So -- but my point was there is a gradual mix change going on where marketing is a higher component of our growth businesses and therefore, in some sense, becoming a higher component of our business. But through it all, we continue to be as bullish about marketing and our -- the return on our marketing as we have been really at any time in this journey.

**Terry Ma** (Analysts):
Got it. And I guess just as a follow-up, you called out the Visa and Mastercard settlement. Any way to kind of quantify the impact to Capital One? And I guess you kind of tied it to the synergies, is there any more color that you can kind of give?

**Richard Fairbank** (Executives):
So Terry, the revised settlement between merchants and Visa and Mastercard is going through the court approval process now. The hearing on final approval will take place in November. I know a lot of people in the investor marketplace or maybe even analysts are saying, "Well, we'll wait to see what happens and then sort of put it into our estimates." We put a pretty high likelihood on the final approval of this. And so in our planning, we have for some time been incorporating our best estimate that we can. This has a pretty wide error bar. We don't really have great insight into what that number is going to be. In many ways, we see the same information, the same analysis that you do.  
So my point was just that we are planning for this to happen, maybe it won't, but we're planning for it to happen. And then my point also was that in sort of rough ballpark, that is -- if we sort of stand from where we are today, looking at that impact on run rate is very -- it is in the ballpark of the impact of the extra synergies that are coming our way beyond the annualized number that we mentioned before. So those are in a nice way sort of offsetting, a nice way, meaning that for us to kind of give you a window to reach out and touch the earnings power. I think those things are generally offsetting.

**Operator** (Operator):
Our next question comes from Ryan Nash with Goldman Sachs.

**Ryan Nash** (Analysts):
So Rich, maybe to pick up on your ending statements. There were a lot of moving pieces, cost saves, network settlement, reserve normalization and elevated marketing, I think, were the 4 things you highlighted. I guess what are we supposed to take away from that statement? Are you saying that I tried to do math quickly, but return should be at 20% plus? Or is there something else underlying in the statement? And I guess given your response to Terry's question, should we expect that you'll be maintaining these returns? Or do you think marketing will eat into some of them? And I have a follow-up.

**Richard Fairbank** (Executives):
So thank you for your question, Ryan. So let's pull way up on the guidance that we've been giving over this since we brought Discover on because we don't generally guide on things like specific earnings power, things like that. But I think the question sort of on everybody's mind has been this kind of amazing deal with Discover. What's going to be the earnings power coming out the other side? And how will we -- when can we sort of validate that we see that? And so what we've been saying along the way is there are a number of things that have already sort of moved, but that we still believe that the earnings power coming out the other side of this integration is consistent with what we believed at the time that we made our announcement. And what has happened is along the way as we were getting ready for this earnings call and just savoring how much of the synergies have, in fact, been achieved that that's sort of the biggest thing that still has been waiting to happen as this deal is integrated.  
And so our point was, given that everyone wants to see what is the earnings power and how does Capital One view the earnings power coming out of this deal. My point was with a couple of approximate adjustments, we can actually just see it right now. We don't have to hold our breath and wait for it. It's really -- we can see it right now, and that's -- we don't -- we're not in the precise number business. This is -- as you know, in our business and earnings numbers involve the subtraction of very large numbers. They involve credit numbers that can move around and allowance numbers and things like that. But I think that what we have been saying for what we think will come out the other side of this deal is, in fact, manifest right now with a small number of basic adjustments. And that's really our point and we celebrate that it's there to be seen and that's really our -- the point that we wanted to make to investors.

**Ryan Nash** (Analysts):
Got it. And maybe, Rich, just as my follow-up. Obviously, there's a lot of macro noise out there, but the credit performance remains very strong. Just maybe unpack for us what's driving the improvement in card? And as you look forward, do you think that we can continue to see this type of improvement given the dynamics you're seeing in the portfolio?

**Richard Fairbank** (Executives):
Okay. So the -- let's just talk about our credit performance. I mean, we've got -- I think Capital One is performing very well in credit and there's kind of an industry effect there. And I think even on top of it, there's some Capital One very positive things going on. But the -- but if we pull up on credit for a long -- for quite a long time now that extends back into last year. Credit was -- has been improving relative -- a little bit kind of every month or every quarter to coming in just a little bit better than seasonality. So there's been this cumulatively very significant improvement that has happened. I'm talking about delinquencies now.  
In the last few months, I think what we see is more in line with seasonality rather than outperforming seasonality. But we're in a very good place with respect to credit. Now if you think about charge-offs, there are a couple of things to say there. First of all, charge-offs are lagged relative to delinquencies. The charge-offs continue to improve as the delinquencies have improved. And then we have the striking recoveries effect that I just want to sort of reflect on that. Recovery is, of course, an important factor in our overall credit performance. And our recovery rates have historically been at the high end of the industry, probably as a result of our business mix and our strategy. And during the period of postpandemic normalization, we noted that our recoveries were unusually low because of record low charge-offs during the preceding 3 years. And those low recoveries were a factor pushing up overall loss rates well above prepandemic levels.  
Today, we're seeing the opposite effect. Our recoveries inventories are higher than normal because of higher charge-offs in the rearview mirror. This is even more true at Discover, which had significantly higher charge-offs 2 years ago than they do today. But even when we adjust for this inventory effect, we see stronger recovery rates on recent charge-offs than what we've observed historically. And we think at least some of that is driven by sustainable improvements in our recovery strategies enabled by our transformation. So pulling way up on credit we think credit's in a solid -- in a very good place. We'll note that delinquencies have been kind of moving with seasonality for a few months now as opposed to beating it. But all told, we see it in a very good place.

**Operator** (Operator):
Our next question comes from Sanjay Sakhrani with KBW.

**Sanjay Sakhrani** (Analysts):
Quick question on expenses again, Rich. When we think about sort of the direction of travel on the efficiency ratio from here, how should we think about it? Should it be improving from here on out? And then just on the settlement, I guess, yes, we can -- it's a subjective thing. It may get appealed and delayed, and I get your point. But are there any offset to that interchange reduction that you could think of? Like would you pull down rewards to offset some of that impact? I'm just trying to think about the net effect of the decline in interchange part for the settlement.

**Richard Fairbank** (Executives):
Okay. Thank you, Sanjay. So let's talk about the efficiency ratio. There's a lot of variability quarter-to-quarter in efficiency ratio. So of course, I wouldn't anchor to any one quarter's results. And the efficiency ratio will continue to reflect the realization of synergies and our investment imperatives. And we continue to lean into our investment imperative, including foundational technology, AI, as well as important growth vectors like heavy spenders and our National Bank and our Global Network, and we will step up marketing investment.  
And as I mentioned also, our biggest growth areas are businesses where marketing costs are a bigger component of the business model and which have inherently higher efficiency ratios. But also, of course, they tend to bring lower risk, lower capital and long-lasting annuities. So there's a little bit of a geography change across a lot of the line items of Capital One, more gradual from quarter-to-quarter, but over the longer arc of time can be important. But also just we continue to lean in very hard to harvest meaningful efficiencies outside of our investment areas powered by our technology transformation. So there are a lot of moving pieces. Some of them are structural. We're not giving specific guidance on efficiency ratio, and we've been more focused in our dialogue on earnings power.  
And -- but we -- there really is the sort of continuing efficiency improvement underneath Capital One and so much of the business that we run while on the other hand, there's a mix change and a real leaning into investments that make the netting of these sometimes move in opposite directions. So -- or the netting of these 2 -- just to lead us not to give specific guidance on efficiency ratio.  
With respect to the settlement, so in some ways, the settlement is a couple of decades in the making. So I think folks could say, we've seen this extended so many times, like, why are we talking about it now? As I said earlier, from what we can gather, we give reasonably good odds that the settlement will happen. But the way we manage the company, when costs are likely to be coming, we put them into our numbers and manage accordingly. So we -- so from an expected value kind of point of view, that we're absolutely managing to that. 
The specific -- that specific change, I don't think is -- necessarily will catalyze any one specific change tactically in what we have because we've been incorporating the expectation of that for a long time in the strategy and the rewards that we set, et cetera.

**Operator** (Operator):
Our next question comes from Rick Shane with JPMorgan.

**Richard Shane** (Analysts):
Rich, I'm really curious about the Brex acquisition. When we think about Discover, you acquired a network, but I don't think you would argue that the technology there was cutting edge. Brex obviously has had a very different approach to market, brand-new platform. I'm curious how much of the technology from Brex, Capital One is actually integrating and adopting and changing your workflows. Is there learning from them?

**Richard Fairbank** (Executives):
So Brex is an amazing company. You -- I think you all saw my excitement at the day of the announcement and we have had it ever since. But I want to -- there are many things that are remarkable about Brex. But I do want to say that way up there, one of the most remarkable things is that this -- most founder companies these days are very tech forward. And just in terms of pure tech shops and innovation, they're way up there right at the top. But in addition, the choices that they made amaze me. And I have such reverence for it because I think we make a lot of similar choices in the building of Capital One, and that was choices to build for the long term, build from the bottom of the tech stack and be very reverential about things that will be profoundly helpful later, but that cost more money now. 
And so the fact that they have a full modern tech stack that they built themselves for their -- the age that, that company is, is breathtaking and it's really valuable to -- will be very valuable to Capital One over time. We have a great time hanging out with the Brex people comparing tech practices, learning, and there's so much to learn from them. And then I think that they've also seen a lot about how a company like Capital One, which has been built as a tech company has scaled technology and also taking on things like how do you create a scalable risk management in a highly regulated environment and things like that. So there is a lot of learning. 
I think one of the areas that Brex is, I think, most commonly struck by is where Capital One is on the data and analytics side of the business. Of course, we built the company on that. And so there's just so much I think that we are sharing, and we look forward to share. 
So let's talk about integration of technology. We are taking a -- we see great upside down the road to integrate a bunch of things, but we're also being very targeted and measured in our approach to integrating our technology with Brex, so we can be sure to allow them to focus on growing their business. And another striking indicator of the quality of what they've built is that we can let whole parts of Brex sort of operate independently and be confident about that because of their own reverence for risk management and how they build things. So as we've contemplated the broader integration, we will slope the work focusing it, and we already are doing this, focusing on the critical risk management requirements that come with being part of a regulated national bank. 
Now over time, Capital One can leverage Brex's spend management tools to broaden and enhance our offerings for our existing small business personal liability card customers, we are wildly excited about that opportunity. But that's not something we can sort of reach over and grab that. That's going to require more connection and more integration of certain tech and data aspects of this. So that one's down the road. We will also integrate Brex's spend management platform with the Capital One travel portal which will allow businesses to manage their corporate travel expenditures and policies, driving growth in business travel revenue. And as a side point there, we have really been leaning into our own travel business. I would encourage folks who are cardholders to check out our stand-alone travel app that we have and really quite a lot of great things there, and we're building many more things on that. 
But anyway, so we look forward to that synergy -- strategic synergy that will come there. 
And lastly, we will integrate Brex's banking services with ours, which will provide us capabilities to leverage Brex's business banking software with our payment capabilities. So this is -- so picture this sort of integration phase is the first phase is a little bit more, which I colloquially call adding water, that we try to do the things, the most important integrations and then add water to help grow their business. And Brex -- and just comment on that for a sec, Brex is already experiencing some of the early tailwinds that come with our brand, and we expect these to only grow stronger over the next few months. They're benefiting from the cost of funds, from moving to our balance sheet. We have already stood up a program to share high potential leads from across our businesses with Brex and are seeing very promising results at the outset, and we will scale into this approach more completely over time. 
We -- over the coming months, as we test and learn, we'll start leaning in with our marketing dollars. And what's also coming in this sort of add water phase but not yet at this moment is fully leveraging the marketing machine of Capital One, which requires a little more technical integration, setting up data pipelines, calibrating our models for Brex's customer base and so on. And for our travel business, we're going to be focused on the Hopper buildout through the balance of the year. So the travel portal -- bringing the travel portal to Brex is probably be a next year kind of thing. But anyway, that's a window into how we view this acquisition. 
But I just want to savor the -- that one of the power benefits of a deal like this is taking an absolutely leading technology company that is transforming a financial service marketplace and bring it on to Capital One with our modern tech stack and heritage of building a tech company. And I think that we're going to be able to create a lot of opportunity, and it's an opportunity that can uniquely be made possible by this combination.

**Operator** (Operator):
Our next question comes from John Pancari with Evercore.

**John Pancari** (Analysts):
Rich, I appreciate you walking through the process of how you got to the earnings power and how we should think about that. So given the way that you framed it and that earnings power is in sight, is it fair to say that based on that, we should not expect a meaningful incremental step-up in expenses from here as you continue with your business and network investments and that this ballpark of where we triangulate given the math you gave us that seems like it may be in that 20% ROTCE level that, that does not -- that we should not dial in an incremental step-up in expenses as we look forward?

**Richard Fairbank** (Executives):
Well, John, there are a lot of moving pieces in how we think about this company and where we go with our strategy. My real point was the earnings power that you can see out of this combination is now you can pretty much reach out and touch it. We have been saying along the way, we are leaning hard into investments. And a lot of that leaning is already in the numbers that we are printing these days. But there is important leaning that's coming going forward. And the -- and I commented things like the top of the market, I'm not going to run through the whole list necessarily again. 
But we will continue to lean into investments. And our belief is that we have the earnings power to be able to sustain pretty high levels of investment to help a really nice growth future and, at the same time, deliver strong earnings power, reflective of the kind of thing that you see.

**John Pancari** (Analysts):
Okay. Got it. And then separately, just around the network. Can you just update us on the progress of moving some of the Capital One Credit Card volumes onto the Discover Network and any of the pilots that you're running? How should we think about the pace of that migration and the time frame involved?

**Richard Fairbank** (Executives):
Okay. Thank you, John. So as I often say, the Discover Network is a rare and valuable asset and the crown jewel of the acquisition. Discover built an amazing network. To this day, the deeper I dive into networks it still amazes me how far they came with building out a global network with the scale that they had. They were benefited by being an early player going back decades and -- but I give so much credit to them, but they didn't have the scale to fully complete and sort of turn the flywheel. So they were trapped in a subscale situation doing an amazing job with what they had. 
The Capital One brings the opportunity to build more scale in a very scale-sensitive business. I don't know if I've seen a more scale-sensitive business than this one. So earlier this year, of course, we completed the conversion of our Debit Card business to the Discover Network. And we are very pleased with how the conversion went from a customer experience standpoint, the volume retention and the growth that we're driving on the other side. We're also looking forward to growing credit card volume on the Discover Network in several ways. So we will, of course, continue to lean in to grow Discover-branded cards, which have always been on the Discover Network and will continue to be. 
We will also build network volume by originating Capital One cards on the Discover Network and by converting Capital One customers from their existing network to the Discover Network. And we've been conducting tests to help inform our strategy regarding which customers and products we target for moving to the Discover Network and the timing of those moves. In parallel, we will lean hard into enhancing global network acceptance and building the Discover brand. And along the way, we will slope the work as we drive acceptance and slope the work in selecting which products and customers are moved onto the network. 
So this will be a -- this is not going to be a big bang thing like you saw on the debit side. But this is -- we want to make very clear, this is what we're working backwards from and picture us leaning in, really giving it the best opportunity it can, investing to be able to get there and then sloping the work on the acceptance and the conversion side along the way.

**Operator** (Operator):
Our next question comes from Andrew Bauch with BMO Capital Markets.

**Conan Leon** (Analysts):
This is Conan on for Andrew. My question is on the premium card space and Venture X specifically. I was wondering if you can talk about the competitive landscape and how you view the lifetime value of an incremental premium card user over time, just given the increase in rewards and marketing spending.

**Richard Fairbank** (Executives):
So thank you. So the launch of Venture X is a continuation of our journey over many years to win at the top of the market. And it really started back in 2010 when we launched our Venture Card, and we have continued, it's another one of these things at Capital One, where we declare where we're going and patiently build something over an extended period of time, which can span -- in this case, we're well into our second decade of this quest. 
But included in this has been the launch of our Capital One travel portal, the opening of Capital One lounges and investments in sort of groundbreaking customer experiences and exclusive services. We have been very pleased with the customer engagement and the traction that we're getting. And we have with each -- every year or 2, we just keep moving a little bit higher in the marketplace, stretch higher toward the heaviest spenders. And over this period of time, we continue to see that the fastest growing part of our card business is with the heavier spenders. And I think there's so much growth opportunity left there. 
But first -- but the thing we note is the very positive growth trajectory that we get and the very positive customer validation that we get. 
When we think about economics, we -- let's go back to our journey from 2010. We set out on this quest, this battle cry, we're going to win at the top of the market. And we had Venture and VentureOne, our first 2 products, and we lean into those, build them to scale, look at the very impressive horizontal returns coming from that franchise. We lean up. We go into Venture X and we watch how that thing is going and the power of -- the earnings power of those annuities. Meanwhile, on the small business side, we have had a parallel quest going on with our Venture X business card. We're very pleased with those results. 
So we -- I guess with -- so we validate along the way with our horizontal economics, the customer -- the traction with customers, the growth rate, the annuities, the attrition rates, the charge-off rates that all collectively add up to the overall economics. But what we continue to see is a very strong validation of this quest. And -- but included in it, we know that it involves continuing to invest grow not only more customers, but to keep growing higher in that marketplace. So we're pretty excited about where we are. 
Just a comment, you asked about the competitive -- maybe just a comment about the competitive position of, for example, Venture X. We feel we're in a great place with Venture X's competitive positioning as a straightforward high-value product. And we see our competitors doing -- leaning in very hard. And I think everyone is staking out a bit of a special place in that market at the top of the market. But I think the power metrics that we're seeing from our quest are very impressive.

**Operator** (Operator):
Our next question comes from Erika Najarian with UBS.

**L. Erika Penala** (Analysts):
Just my first question, Andrew, on the net interest margin trajectory from the 8.41%. Obviously, the revenue suppression being lower helped the earning asset yields. Lower deposit balances help with deposit costs. As we think about sort of growth in balances in the fourth quarter and maybe the puts and takes of how to think about the forward curve, can you sort of help us think about the path of net interest margin at least in the fourth quarter?

**Andrew Young** (Executives):
Sure, Erika. Thanks for the question. The one thing I would add is just the benefit in the third quarter, too, is just the ending cash balances coming down in the quarter -- or sorry, the average coming down in the quarter was beneficial this quarter as well. 
Looking ahead, something I noted last quarter is that all of the structural impacts from the Discover acquisition have largely played out at this point in our NIM. And so from a rate perspective, our NII is relatively neutral to rates, the pace and timing of rate hikes could impact NIM in any given quarter, just given the timing of asset repricing and deposit repricing decisions. But over, call it, a handful of quarters, the changes in short-term rates should have a largely neutral impact. 
And so I would say longer term, the changes to NIM will be driven by 2 things. The first is the seasonality that happens by quarter, things like day count, revolve rates, you brought up the fourth quarter holiday spending impacting the denominator. Those are things that are going to impact quarterly NIM, but they're just not going to impact the ambient level. 
The other thing ultimately that will impact NIM over time is just the relative growth rates of specific assets and liabilities that will be driven by business choices, by the competitive environment, by customer behavior. But at this point, the thing I would reinforce is the structural impacts to NIM have run their course. So it's more going to be about seasonality and the effects that I just described.

**Operator** (Operator):
Our next question comes from Don Fandetti with Wells Fargo.

**Donald Fandetti** (Analysts):
Rich, recently Capital One ranked pretty well on an AI industry report. I guess I have 2 questions. One, are you seeing specific like revenue benefits, market share type gains from these investments? And number two, do you plan to quantify these benefits?

**Richard Fairbank** (Executives):
So Don, the -- we certainly do not intend to quantify the benefits. But I want to stand back and just talk a little bit about AI and how we think about it and how central it is to who we are and what we're building. So the pace of advancement in AI is just breathtaking. The world has really, I think, never seen anything like the rate of innovation and change we're now seeing in the world of AI. The AI itself and then generative AI in 2022, agentic AI over the last year, it's just unbelievable and the pace of change it is accelerating. And it is as clear as could be possible, at least in our mind, that everything is going to change and our lives are going to change. And in business across the business world and in banking, it's never going to be the same. But those changes also aren't going to happen overnight. 
But let me talk about that. We've talked for a long time about our technology transformation. And you all know that in 2013, we pulled our company together and said, look, we built -- we set out to build a tech company and a data company, and I'm proud of what we built. But we're on the wrong side of history with respect to the technology that was modern in the past, but it's not modern now. And we set out to rebuild our technology from the bottom of the tech stack up. But I want to savor what the objective function of that rebuild was. Back then, we're talking more than a decade ago. 
The objective function was not so that we could be modern. The objective function of the rebuild was AI and envisioning how the whole world was hurtling toward a world where everything was going to be about AI in real time, bringing instant solutions entirely customized to consumers and businesses and also creating the opportunity to transform how companies work on the inside. So that's what we set out in 2013. It's been the objective function ever since. 
Now note, we didn't predict generative AI, and we did not predict agentic AI, but yet AI was the objective function of this transformation. And as I look at the amazing advancements in generative AI and agentic AI, they are part of a continuous curve of that is -- and the tech stack that it needs, we often say, well, if we had known about generative AI or agentic AI, what would we have done differently with what we built? And the answer is we would have built exactly what we built because we were working backwards from having a modern tech company where -- powered by AI. 
So let's talk about the AI that's coming to the world, I think AI is -- everybody all over the place in business is talking about AI as they should be. And I think companies will adopt AI and get a lot of benefits. This includes banks and as well as other companies. But I think there will be the degree of benefit and the extent to which this is adopted will be across a really wide spectrum. And that spectrum relates to whether AI is -- we bring -- whether companies bring AI to improve work as it is done today or whether companies reinvent how work is done with AI, and I think everybody is going to do the former and get a lot of benefits. In order to do the latter to reinvent how work is done with AI, it's -- I think it's going to need modern tech stack. It's going to need an organization that can work backwards from transformations that transcend business units and sort of collide with a lot of things about how companies are built and organized today. 
So -- but we are bullish about these opportunities. And we -- when we think about -- so the customer experience, well, certainly, I think AI will be transformative for the customer experience because customized solutions in real time are going to be coming out the other side. But when you think about inside a bank, the opportunity with modern technology, data and AI to transform the entire data ecosystem, how software is developed, credit, marketing, risk management, fraud, operations, servicing, cybersecurity, pretty much, I think, across the board. 
And so these will be things that will -- and I think investors will often ask, well, where do I see AI? I want to see the app. I want to see it in the app or what's the manifestation and I appreciate those will be questions people ask but it's a little bit like asking the question, "Well, Capital One, you set out to build an information-based strategy 3.5 decades ago, where do I see it?" And my answer is it's all around us. It's everywhere, but I can't point at an app where you see it. It's just really in the business model, in the choices, in the way risk is managed, customer experiences, marketing and everything. 
And I think AI will be experienced by our investors in exactly the same way. And we are really bullish about the opportunity. But it also ties back to the question often investors are asking, why do we keep talking about -- why do we talk about investment? Can't we just settle back and just stay where we are with respect to our investment levels? You should all know -- I mean, my view is we are experiencing something basically like fire and electricity itself, except experiencing it, not in the long period of time that those innovations came but in an incredibly short period of time. And we believe we're very well positioned, but we know there is a big investment imperative to take advantage of this. And it would be, I think, really a disservice to our investors if on the shoulders of what we have built, we held back in terms of investing in this extraordinary humanity-changing thing that's happening.

**Operator** (Operator):
Our next question comes from Bill Carcache with Piper Sandler.

**Bill Carcache** (Analysts):
As investors debate where we are in the cycle and how much growth runway is left, many believe the Capital One franchise today is structurally more resilient given the Discover combination and the meaningful investments you've made in the digitization of the business and this quarter's results certainly support that. So while the Capital One in the past has historically gotten down to tangible book value in downturns, it would be helpful to hear how you think the resilience of the business has changed and whether you believe it's -- the business is in a superior position today to weather the next turn in credit, whenever that comes, of course, it's very favorable today, but it would be great to get your thoughts.

**Richard Fairbank** (Executives):
Well, Bill, thank you so much for that question. Wow, there's a lot packed into this that you know from the founding of this company and maybe it's because I spent too many years consulting to companies that didn't -- that were living the consequences of not doing what I'm about to say. But from the founding of this company, we have been just very focused on building something great for the long term. And that means something that not only has nice horizontal economics like we talk about, but something that has resiliency to weather the extraordinary storms that hit companies over time. And so we built our company with that philosophy and with respect to resilience, let's talk about what we've done. Always in our underwriting, we don't underwrite to how things like the test cells are performing. We underwrite to a worsening scenario and assume the worsening is business as usual that we try to bake resilience into our very choices. And we have various resilience metrics we do. 
We also take every program that we have at Capital One and evaluate it as part of this horizontal evaluation but evaluate the resilience of all the different parts of our business. And so it doesn't mean there's a guarantee of being resilient, but to bake worsening into the business model at all times is, I think, a really important thing. We also have a conservative capital philosophy. We've talked about that. And I think that we've been well served by that. But I believe that Capital carries -- Capital has very asymmetric risks and benefits associated with it, and we take a pretty conservative philosophy there. 
Let's talk, Bill, about what has changed since the global financial crisis. Certainly, Capital One's business mix, we have just a lower-risk business mix in terms of the sort of credit content of the company way more spender-led portfolio, lots of business at the top of the market with heavy spenders, and I think that will serve us well. 
We also, over the years, you may remember, Bill, I'm sure you do. We were vocal for years about managing to avoid the best we could, what we call high balance revolvers that we said they performed incredibly well in the good times, but the issue is resilience. And so we -- at the expense of growth over the years, really managed to do the best we could to minimize high-balance revolvers. By the way, Discover has got more of those than we do. And that's part of the trimming around the edges we've done there that has contributed to the brownout, but they have a great franchise. 
So we -- those are some of the -- then along the way, also the technology of Capital One that we have built allows us to measure things so much better, to monitor things in real time, to monitor with even in some of our areas, you use AI-based monitoring that is full file instead of sample based, it's full file. And instead of batch, it's real time. Instead of manual, it's automated. And instead of just flagging something, it's flagging things with root cause diagnosis and suggested solution. So the early days still on some of that AI monitoring, but that's just an example of where the technology that we have built at Capital One because from its founding day, we built basically a credit-based company. At the top of our list of what we build is to build the technology that can enhance our resilience. And so those are some examples. 
I do want to say that one thing that was very wind-aided in the global financial crisis that we should point out, and that is that we had a significant amount of our balance sheet -- of our loans off balance sheet. And so -- and also, it was not a CECL regime. So we when the sort of the bad times came, our allowance build was way less than it would be pound for pound now with everything on balance sheet and everything with CECL and all that. 
So -- but -- so I think there are some things a little bit on the other side that we should keep in mind. But one of the very strong motivators of the strategic journey of Capital One in the last 1.5 decades has been the diversification of our business model and moving into businesses that have a lower credit risk, higher expense bases, lower capital requirements and that migration will continue.

**Operator** (Operator):
Our next question comes from Darrin Peller with Wolfe Research.

**Darrin Peller** (Analysts):
Can we just -- I'd love to hear your opinion on the potential just given the political and the upcoming elections for CCCA and how you believe you could fare just given the obvious the Discover Network now, what that can mean for the business, both ways, whether it's gaining share or obviously, pricing dynamics of keeping things in-house? 
And then just also on the topic of Discover, just as you were restarting marketing and originations around it, do you have a sense on the timing before we can see Discover return to positive loan growth? Any way to think about the economics of new balances there versus prior?

**Richard Fairbank** (Executives):
Yes. So let's talk about CCCA. So interchange has been around for a long time because it's part of a well-established payments ecosystem in the United States that benefits both retailers and consumers alike. And we believe that there is substantial competition in the payments industry already with banks like Capital One taking a big portion of its interchange revenue and giving it to the consumer in the form of rewards. And in fact, if you -- when we have looked at the evolution of the international credit-based marketplaces, we find an observation is the banks in those markets probably passed a significantly lower proportion of their interchange to consumers. 
I'm not faulting them, it's a choice that was made. The banks -- the leading banks in the United States, one of them being Capital One, but others as well have really leaned into taking such -- a big part of the interchange revenue and giving it to the consumer in the form of rewards. And lots of important things happen. First of all, obviously, it's a big win for consumers. It stimulates consumer spending, merchant sales, it helps the ecosystem thrive. And it also creates an important, in a sense, political constituency that appreciates the power of what's happening there with consumers across the credit spectrum being able to enjoy their rewards. 
So I think whether I speak from the legacy Capital One perspective or the Discover perspective, I think the ecosystem works very well now and a change that would inevitably alter credit card rewards would be undesirable for consumers, merchants and the economy. And so we -- that's a view that we have had, and it's a view that we still have even as we own this network. The brownout, excuse me. I get so excited about the other topic. Yes, let me just talk about the brownout for a second. 
So as we've talked about for a whole bunch of quarters now, the Discover Card portfolio is going through a bit of a loan growth, and I colloquially created the phrase brownout just -- so it would have a branded term there. As several factors combined to pressure loan growth in the near term, following Discover's credit expansion in their card business in '22 and '23, they dialed back their origination programs and credit line management by a fair amount toward the end of 2023, and they largely sustained those dial-backs. Since we took over, we've been trimming on the margins of Discover's credit policies in areas where we are less comfortable with the resiliency of the underlying customers like high balance revolvers. 
As a result of these pullbacks, the portfolio has been contracting and continues to face some headwinds to growth as these more recent smaller vintages mature. In the third quarter, Discover Card outstandings were down 2.9% year-over-year. By the way, it's worth noting the flip side of these pullbacks and the brownout has been strong credit performance. Now this brownout will not last forever since we will bring to bear a number of capabilities as we move Discover originations and existing customers to Capital One's technology. And that whole movement is way underway. 
Getting Discover on to Capital One's technology will allow us to unleash our models, full spectrum underwriting and spender capability to power more originations, higher spend volume and ultimately, higher loan volume over time. As of the end of September, 100% of Discover Card originations are on our tech stack. We are in the middle of our conversion of the back book, and we'll complete that in the first quarter. We are just -- one of our waves, we have several waves of conversion, but one wave happened over the weekend. You might want to peek at the App Store any of these days. I won't give it away, but check out the free apps on the App Store. And you'll see the evidence of droves of people moving to the Capital One mobile app. 
So anyway, all these moves will bring octane back to the portfolio. This quarter, new originations were up year-over-year for the first time since the deal closed. As the back book converts, we are resuming and leaning into customer management programs, which have been limited during the conversion. All these moves, of course, take time to turn into loans. We expect continued contraction over the next several quarters and then for loan growth to turn positive after that. 
And just one -- I'm sorry, one other note, just the other area of brownout has been personal loans, and that's going through its own sort of magnified brownout because the -- those loans have shorter duration to them. And so the dial-backs have been more dramatic. But over time, we have the same views for that one, and we look forward to leaning back into that.

**Operator** (Operator):
Our next question comes from Rob Wildhack with Autonomous Research.

**Robert Wildhack** (Analysts):
Just a quick follow-up on the NIM commentary. Andrew, you teased it a little bit, but end-of-period cash was much lower than average cash in the quarter. So I'm wondering if there's any structural or longer-term opportunity to continue mixing away from cash? Or is this kind of it? And then just quickly, how about your thoughts on deposit growth in betas and deposit competition through the hiking cycle? There have been some mixed messages so far from some of the other players in that market. So just checking if there's any color you want to share there.

**Andrew Young** (Executives):
Yes, sure, Rob. We ended the quarter with just under $50 billion of cash. The third quarter average was about $55 billion, which is in line with where we ended the second quarter. Cash levels can move up and down due to the timing of deposit and loan growth, has a little bit of seasonality in it and also need to keep an eye on the timing of maturities and wholesale funding issuances. But I don't want to give a specific target given the fluctuation. But I would say the range of this quarter sort of average and ending probably gives you a reasonable benchmark of what will be typical levels. 
In terms of deposits, what we saw this quarter, as Rich noted in his talking points, was deposits were down about 1%. We sold a small IRA portfolio as part of the Discover integration, that drove a majority of the decline this quarter. If you take a longer kind of aperture even with that decline, our book has grown something like 3.5% over the course of the last year. So we feel really good about the business we've built and the ability that it creates for us to have resilient, high insurance percentage with deep customer relationship business.
So with respect then to beta, I would say the recent falling cycle had a lot of noise given we acquired Discover, which drove some mix change. So I don't believe that that's particularly useful from an informational value perspective. But if you look at the last rising rate cycle, that's probably a better neighborhood of what we could expect with this cycle's beta, but it's important to note that each rate cycle is different. I think the ultimate beta is going to be driven by our product mix, by the opportunities that we see to build those lasting customer relationships, the magnitude and pace of Fed funds move, but as you said, also the competitive landscape. And so keeping a close eye on that competitive landscape and how it potentially impacts pricing choices and beta, but we're starting from a place of believing that the last cycle is probably a reasonable starting point, at least for our assumptions, and we'll keep a close eye as this cycle plays out.

**Operator** (Operator):
And our final question comes from Mihir Bhatia with Bank of America.

**Mihir Bhatia** (Analysts):
I just have one quick one. I just wanted to clarify the comments on earnings power in 2027 investments. I think Rich, you said the deal model earnings power is visible today, making a couple of adjustments from today's results. But then you also, I think, in the Q&A have talked about a lot of important investment that's still to come and that holding it back would be a disservice to investors and we totally understand you want to invest for the long term. 
But I just want to be clear about the earnings power as we think about 2027, 2028. When you talk about the earnings power that you have projected at the deal, does that include those step-ups in marketing, technology, spending? Or does that spending power come on top of the model, if you will, right? Like it's -- just trying to understand if the earnings power already incorporates some of this investment spending you're talking about.

**Richard Fairbank** (Executives):
So the -- thank you for that question. The investments, we have already been leaning into investments significantly in our company. We've talked a lot about that. And so the -- a lot is already in the numbers that you see and we are continuing to lean in as well, some things that are probably going to see more in the future than they have are investment in the Discover Network, which is really just kind of getting underway. We talked about the growth in marketing, of course. But -- and the investment in AI and capitalizing on this opportunity. 
So I -- we aren't generally going to be in the business of being in the year after year giving guidance on the earnings power of the company. I think our -- really, our point has been we wanted to show the earnings power that's on the other side of this deal, and we have -- and I think you can -- our point is you don't have to hold your breath, you can reach out and touch it here. We will continue to lean into investments as we do at Capital One, and there's quite a bit that we are pursuing, but it's also the case that we are very focused on the earnings power in this company and generating quite a few savings on the -- on one minus those investments. 
So we just wanted you to be able to reach out and see the earnings power as the dust settles from the integration. And we continue to be bullish about the earnings power going forward as well as leaning into important investment opportunities. And that's a little bit of a window into who we are. 
And I want to reflect on that because from the founding of the company, we didn't build -- we didn't just say we're going to go do what all the other banks did. We very carefully chose businesses that had inherently high earnings power that enabled the delivery of strong earnings power and at the same time, investing to build a great company for the long term. And I think you're seeing it today and so I think it's simultaneously the case that we're -- we have a lot of earnings power on display, and we will continue to lean into very high-value investment opportunities. And always with -- and that I think that's going to be a key formula for driving great earnings power for years.

**Jeff Norris** (Executives):
Thanks, Rich, and thanks, everybody, for joining us on the conference call this evening. Thank you for your interest in Capital One. Have a great night.

**Operator** (Operator):
Thank you. This concludes today's conference call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### COF_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO｜margin：Q2 淨利差 8.01%，較上季高 14bp（原話："Our second quarter net interest margin was 8.01%,"）
- 2026-07-21｜CFO｜margin：下季淨利差預期因平均現金追上期末現金而回補（原話："there should be a bit of a NIM catch-up"）
- 2026-07-21｜CFO｜margin：下半年每季多一天，帶來 9bp 淨利差順風（原話："So that adds a 9 basis point tailwind to NIM."）
- 2026-07-21｜CFO｜margin：結構性淨利差參考去年下半年水準（原話："the back half of last year as a pretty decent proxy for a"）
- 2026-07-21｜CFO｜margin：NII 對利率近乎中性，但 Fed 動作短期可能影響 NIM（原話："neutral to rates over time, but if and when the Fed moves"）
- 2026-07-21｜CFO｜capital_allocation：CET1 13.7%，較上季低 70bp（含回購、Brex、風險加權資產增加）（原話："ended the quarter at 13.7%, 70 basis points lower"）
- 2026-07-21｜CFO｜capital_allocation：11% 是長期資本『需求』而非目標（原話："long-term capital need as opposed to a target"）
- 2026-07-21｜CFO｜capital_allocation：不急著把資本比率壓到特定數字（原話："we are not in a race to drive it down as quickly as"）
- 2026-07-21｜CFO｜risk：卡業務備抵釋出 7.05 億美元（原話："we released $705 million of allowance."）
- 2026-07-21｜CEO｜risk：國內卡淨沖銷率 4.71%，較上季降 39bp（原話："was 4.71%, down 39 basis points from the prior quarter"）
- 2026-07-21｜CEO｜risk：國內卡逾期率 3.39%（原話："delinquency rate was 3.39% at quarter end"）
- 2026-07-21｜CEO｜risk：6 月逾期是今年第一個沒有優於季節性的月份（原話："it's the first month that didn't actually"）
- 2026-07-21｜CEO｜risk：回收庫存預期未來一年左右趨緩（原話："our recoveries inventory should taper off a bit"）
- 2026-07-21｜CEO｜risk：2024、2025 年新增帳戶表現優於 2022、2023（原話："2024 and 2025 originations coming in better than"）
- 2026-07-21｜CEO｜risk：支付率明顯高於疫情前（原話："meaningfully above prepandemic levels across all of our"）
- 2026-07-21｜CEO｜risk：管理層稱其客戶數據未見 K 型分化（原話："We don't, in our own numbers, see this K-shaped economy"）
- 2026-07-21｜CEO｜risk：車貸淨沖銷率 1.43%（原話："The auto charge-off rate for the quarter was 1.43%"）
- 2026-07-21｜CEO｜customer：消費者表現良好（原話："the consumer continues to perform remarkably well"）
- 2026-07-21｜CEO｜guidance：Discover 卡貸款預期短期續縮，谷底約在第四季（原話："we expect continued contraction in the near term"）
- 2026-07-21｜CEO｜guidance：Discover 貸款收縮谷底時點（原話："sort of the bottom of the brownout will be somewhere around"）
- 2026-07-21｜CEO｜product：Discover 卡貸款年減 1.5%（原話："The legacy Discover card loans shrank 1.5% from"）
- 2026-07-21｜CEO｜product：Discover 新發卡約一半已上 Capital One 技術平台（原話："50% of Discover originations are now on Capital One's tech"）
- 2026-07-21｜CEO｜commitment：Discover 舊帳戶要到明年第一季才完全轉入（原話："until the first quarter of next year"）
- 2026-07-21｜CEO｜product：遷移分批進行（7 月、10 月、1 月）（原話："A wave in July, a wave in October, a wave in January."）
- 2026-07-21｜CEO｜product：Legacy Capital One 購買量（含 Brex 與公司卡）年增約 14%（原話："grew about 14% year-over-year"）
- 2026-07-21｜CEO｜product：全球支付網路交易量約 1,900 億美元（原話："was approximately $190 billion"）
- 2026-07-21｜CEO｜product：金融卡轉 Discover 網路已完成，管理層形容成功（原話："I would call it a smashing success"）
- 2026-07-21｜CEO｜product：信用卡轉網路仍在測試，之後才定最終遷移量與時程（原話："we will then make our final choices about how"）
- 2026-07-21｜CEO｜capital_allocation：行銷費用約 17 億美元，年增 23%（原話："marketing expense in the quarter was about $1.7 billion"）
- 2026-07-21｜CFO｜capital_allocation：行銷費用下半年通常較高（原話："upward slope and particularly in the back half of the year"）
- 2026-07-21｜CEO｜capital_allocation：網路投資只是眾多投資之一，技術與 AI 花費更多（原話："upward slope and particularly in the back half"）
- 2026-07-21｜CEO｜commitment：Discover 完整 25 億美元綜效維持不變（原話："spending a lot more money than that on Capital One"）
- 2026-07-21｜CEO｜commitment：剩餘營運費用綜效預計 2027 下半年達成（原話："remain on track to deliver the full $2.5 billion"）
- 2026-07-21｜CEO｜guidance：整合後盈餘能力與併購宣布時預期一致（原話："to be consistent with what we expected at the time"）
- 2026-07-21｜CEO｜margin：不就效率比率給具體指引（原話："But we're not specifically guiding on that."）
- 2026-07-21｜CEO｜margin：效率比率隨營收、費用、投資與綜效而變（原話："The efficiency ratio will continue to reflect our revenue"）
- 2026-07-21｜CEO｜guidance：盈餘能力不給精確數字（回應 20% 報酬問題）（原話："We're not branding a precise number"）
- 2026-07-21｜CFO｜margin：盈餘能力以 ROTCE 衡量，分母採 12.5% CET1 僅為可比性（原話："the weighted average consensus for CET1 was 12.5%."）
- 2026-07-21｜CEO｜capital_allocation：近期最大化 ROTCE 不是公司整體目標函數（原話："isn't the maximization of ROTCE in the near term"）
- 2026-07-21｜CEO｜product：Brex：先前未說過從第一天就能加速成長（原話："I don't believe we said this from the second"）
- 2026-07-21｜CEO｜product：Brex 行銷整合需資料管線，較晚才會到（原話："So that will come a little further down the road."）
- 2026-07-21｜CEO｜product：旅遊入口併入 Brex 待 Hopper 建置完成（原話："we will be focused on the Hopper build-out"）
- 2026-07-21｜CEO｜commitment：Brex 投資將嚴格衡量價值（原話："we're going to very rigorously measure to be sure"）
- 2026-07-21｜CFO｜product：不拆分披露 Brex 損益（原話："we're going to very rigorously measure to be sure"）
- 2026-07-21｜CEO｜competition：管理層認為市場對公司估值未充分認可（原話："I believe that we probably don't get appropriate recognition"）

### 問答異常語氣（迴避／改口／保留）
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Darrin Peller 問 Brex 與公司卡的備考購買量成長｜答法：CFO 稱 Brex 占比小、不拆分 P&L；Norris 重述已給的 14% 數字
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Ryan Nash 問是否至少 20% 報酬｜答法：CEO 不給精確數字，只說與當初預期一致
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Erika Najarian 問盈餘能力基準（2027 EPS 約 24.5、ROTCE 中 20 幾）算法錯在哪｜答法：CFO 只說假設不符、股價等變數已動，未確認或否定其數字，回到 ROTCE 定義
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Sanjay Sakhrani 問 Brex 與行銷投資對效率比率的邊際影響｜答法：CEO 稱不就效率比率給指引，改談盈餘能力
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Mihir Bhatia 問 6 月沖銷率大降｜答法：CEO 稱手邊無 6 月數字，主動指出 6 月逾期未優於季節性

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

## ⑥ 條件附卡（archetype_hint='金融' 命中）：judge_addendum_archetype.md

<!-- source: .claude/skills/stock-analyst/references/archetype-gatesets.md sha256:d173785f92087f36 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary ∈ {金融，未獲利高成長，轉機/特殊情境，受監管公用/穩定內需} -->

# archetype 換尺 gate-set 附卡（QC-44/45/46）

## QC-44 金融（bank／insurer／broker）
archetype=金融時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：ROTCE(替FCF Margin) >15%穿越循環｜ROE且>COE~10%(替ROIC) ROE>12-15%｜跨信用循環ROTCE穩定含2008/2020壓力年(替10Y ROIC穩定) 壓力年仍正/不破底｜NIM趨勢+效率比cost/income(替毛利率定價) 效率比<~60%｜Capex/Rev不適用→operating leverage/效率比改善｜EPS+TBVPS複合+股息總回報(替EPS CAGR>20%) ~10-12%即優｜P/TBV vs ROTCE(替PEG)：Warranted P/TBV=(ROTCE−g)/(COE−g)，實際P/TBV≤warranted｜CET1 ratio(替D/E<0.7) >監管要求+緩衝(~11-13%)｜NPL/NCO趨勢+撥備覆蓋+CET1緩衝(替負債安全性)：信用品質穩、撥備足。[§QC-44]
§10估值主錨：P/TBV分位+P/E，用Warranted P/TBV判貴賤；EV/EBITDA拿掉。QC-31 signal：X改ROTCE跨循環<COE／CET1跌破監管／NPL·NCO結構惡化／重大舞弊，移除FCF·NI、EV-EBITDA、Capex觸發。§6跑道：放款·存款·AUM成長+費收業務+市佔，非TAM滲透。[§QC-44]
子型：bank＝CET1/NIM/效率比/NPL·NCO/ROTCE/P-TBV｜insurer(注意US掛牌ALV=Autoliv汽車安全件循環工業，非保險，勿誤歸)＝combined ratio<100%/float/Solvency II ratio/book value/ROE，不看NIM/CET1｜broker·交易所＝ARPU/AUC/take rate/活躍戶，常與未獲利高成長blend｜支付網絡不歸金融，走品質複利。[§子型]
batch補搜：`[ticker] CET1 ratio NIM efficiency ratio ROTCE`(bank)／`[ticker] combined ratio Solvency II book value`(insurer)；yfinance .info 給不出 CET1/NIM/效率比/NPL/ROTCE/TBV。[§batch]

## QC-45 未獲利高成長
archetype=未獲利高成長時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：Rule-of-40(營收成長%+FCF margin%，替EPS CAGR>20%) ≥40｜EV/S÷營收成長growth-adjusted或EV/gross-profit(替PEG<2)｜NRR+毛利率+增量OI margin改善軌跡(替ROIC>15%，GAAP負無意義) NRR>110%/GM>65-70%｜FCF margin+轉正軌跡(替FCF Margin>15%；已正看margin升，未正看跑道+轉正路徑)｜NI負時FCF/NI比無意義→改看FCF margin絕對值+淨現金+跑道，FCF正或跑道>12個月。[§QC-45]
§10估值主錨：EV/S(+EV/gross-profit)+Rule-of-40-adjusted，轉正後接forward P/E；trailing PE/PEG拿掉。**情境樹同步改走EV/S（2026-10-12）**：FY1共識EPS≤0時程式自動切`valuation_basis=sales_multiple`，`scenario_inputs`填營收路徑×終端EV/S×終端淨負債×終端股數（形狀見尾段），不再用EPS×本益比；負債重者(淨負債/EV>30%)Bear的`net_debt_y5`須如實反映融資缺口，股權價值為負即歸零。QC-31 signal：不因GAAP NI負觸發X；X改NRR跌破100%／Rule-of-40<20連2季／毛利結構崩／現金跑道<12個月無轉正路徑／SBC稀釋失控(股數>10%/yr無營收槓桿)。§6跑道：NRR+淨增客戶+TAM滲透+SBC-adjusted轉正時程。blend：fintech broker常＝金融×未獲利，兩套都跑、標背離。[§QC-45]

## QC-46 轉機／受監管公用（輕量尺，不展開大表）
轉機/特殊情境：§4/§10主錨→資產重估/SOTP/normalized earning power/P-TBV，非成長外推；EPS-CAGR/PEG不適用。Single Thing→轉機觸發(債務重組完成/出售虧損部門/新管理層/catalyst里程碑)，非「moat擴張」。§6/§5→「為何現在會轉」catalyst+下行保護(資產底/清算價值)。QC-31 X→流動性危機(跑道<12個月+無再融資)/重整失敗/治理舞弊。[§QC-46轉機]
受監管公用/穩定內需：§4/§10主錨→DDM/殖利率+股息成長/regulated ROE(rate base×allowed ROE)/P/B；PEG/高成長門檻不適用。§6成長→rate base成長+費率案(rate case)+准許ROE，非TAM滲透。§5護城河→監管特許/天然獨佔(single-axis)。QC-31 X→准許ROE結構下調/費率案連敗/監管轉敵/過度槓桿(利率敏感)。[§QC-46受監管]
此兩類不強制長表，但換尺與catalyst/下行保護須sourced。[§QC-46]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260722","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Discover synergy 兌現至 $2.5B 年化（2H2027）：cost + network economics（debit 已繞過 Durbin 完成、卡量遷移待測），驅動 EPS 從 2025 CECL 低點正常化至 FY26 $19.71 / FY28 $28.44"},{"id":"H2","text":"信用週期維持「正常化」（國內卡 NCO 4.5-6% 區間、不結構性反轉）至 FY27：失業率不破 5.5% + subprime 損失回歸 through-cycle 中樞"},{"id":"H3","text":"估值修復：市場把 COF 從「受監管 subprime lender」8x 重估回「正常化優質銀行」10-11x + P/TBV 向 warranted ~2.6x 靠攏"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"信用週期反轉 + 失業率破 5.5% → subprime 卡 NCO 升向 8-9%（COF ~26% subprime 曝險為結構性 binary risk）；疊加 macro overlay 已部分釋出 + recoveries 順風將退坡（管理層自認「未來一年左右」）＝改善引擎熄火，若此時週期轉向損失反彈更陡"},{"id":"R2","text":"Discover synergy 大幅 miss（大型銀行併購典型 30-40% miss）→ re-rate 動能消失；back book 轉換（Jul/Oct/Jan 波次）造成客戶流失加劇、brownout 未如期 Q4 觸底"},{"id":"R3","text":"監管尾部（三面夾）：① 聯邦 10% 信用卡利率上限提案（2026-01 Trump 於 Davos 重申支持一年期 10% 上限；2026-04/05 Warren 續質詢執行進度、至今未決）——若成真將直接摧毀 COF 8% NIM 的 near/subprime 卡經濟，是對 thesis 最大的單一尾部風險（雖低機率）；② CCCA（2026-01 重提，2026-03 未成功附掛住房法案）——雙向：若強制 routing 競爭可能壓 interchange 池（利空），亦可能把量導向 COF 自有 Discover 網絡（對沖）；③ CFPB late-fee RFI（2026-07 送審，現規則已於 2025-04 遭 N.D. Texas vacate）→ subprime 費收"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼：國內卡 NCO 連 2 季 ≤5% 且 Discover 年化 synergy ≥$2.0B（FY26 末）；或回檔 $180-190（P/TBV ~1.7x）分批加","irr_base_pct":12.0,"ev5y_pct":54.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":4.1,"ev5y_pct":54.0,"irr_base_pct":12.0,"max_dd_pct":-52.0,"bull_5y_price":433.0,"bear_5y_price":150.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"加碼：國內卡 NCO 連 2 季 ≤5% 且 Discover 年化 synergy ≥$2.0B（FY26 末）；或回檔 $180-190（P/TBV ~1.7x）分批加","price_at_dd":206.22,"archetype":"金融","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
