你是 stock-analyst **v20 判斷 agent**，標的 ISRG（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ISRG","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":3048.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex.99.1 財報新聞稿"},"note":"未查到"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":41.6,"period":"Q3 2026（公告於 2026-10-20）","unit":"%（營業利益 1,269.7M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（公告於 2026-10-20）","citation":"公司 8-K Ex.99.1"},"note":"未查到"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":19.4,"period":"Q3 2026（公告於 2026-10-20）","unit":"%（營業利益 592.6M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（公告於 2026-10-20）","citation":"公司 8-K Ex.99.1；含 4.5 億美元反托拉斯集體訴訟和解費（SG&A，待法院核准；Q3 訴訟費用合計 454.9M）"},"note":"未查到"},{"id":"f_kpi3_diluted_eps_gaap_non_gaa","label":"Diluted EPS GAAP / Non-GAAP","value":3.0,"period":"Q3 2026（公告於 2026-10-20）","unit":"USD（Non-GAAP；GAAP 1.49）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（公告於 2026-10-20）","citation":"公司 8-K Ex.99.1"},"note":"未查到"},{"id":"f_kpi4_free_cash_flow","label":"Free cash flow（前三季累計，非單季）","value":2868.0,"period":"2026 前九個月（季末 2026-09-30，10-Q）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"2026 前九個月（季末 2026-09-30，10-Q）","citation":"10-Q isrg-20260930：營運現金流 3,197.0 − 資本支出 329.0；新聞稿與 10-Q 均無單季數"},"note":"不適用"},{"id":"f_kpi6_guidance_fy2026","label":"Guidance FY2026（全年）","value":"da Vinci 手術量成長 ~14–15%（偏中點）；Non-GAAP 毛利率 68.7–69.3%（含關稅約 0.9% 營收）；Non-GAAP 營業費用成長 11–13%","period":"Q3 2026 公告（2026-10-20）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026 公告（2026-10-20）","citation":"公司 8-K Ex.99.1；稅率未提供"},"note":"未查到"},{"id":"f_kpi7_da_vinci_installed_base_","label":"da Vinci installed base / procedures","value":12094,"period":"2026-09-30（公告於 2026-10-20）","unit":"systems（YoY +12%；Q3 手術量約 906,000，+14%；裝機 546 台，其中 da Vinci 5 為 315 台；Ion 裝機 1,152，+21%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"2026-09-30（公告於 2026-10-20）","citation":"公司 8-K Ex.99.1"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-20","period":"2026-10-20","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_isrg_gross_margin_pct","label":"ISRG 毛利率","value":66.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ISRG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_isrg_operating_margin_pct","label":"ISRG 營業利益率","value":31.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ISRG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_isrg_fcf_margin_pct","label":"ISRG FCF 利潤率","value":29.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ISRG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mdt_gross_margin_pct","label":"MDT 毛利率","value":65.01,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mdt_operating_margin_pct","label":"MDT 營業利益率","value":19.04,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mdt_fcf_margin_pct","label":"MDT FCF 利潤率","value":16.33,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_syk_gross_margin_pct","label":"SYK 毛利率","value":64.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_syk_operating_margin_pct","label":"SYK 營業利益率","value":21.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_syk_fcf_margin_pct","label":"SYK FCF 利潤率","value":18.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bsx_gross_margin_pct","label":"BSX 毛利率","value":69.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bsx_operating_margin_pct","label":"BSX 營業利益率","value":21.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bsx_fcf_margin_pct","label":"BSX FCF 利潤率","value":8.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_gaap","label":"SBC（占營收／占 GAAP 營業利益）","value":212.6,"period":"Q3 2026（公告於 2026-10-20）","unit":"USD M（占營收 7.0%；占 GAAP 營業利益 35.9%，被和解費壓低分母；占 Non-GAAP 營業利益 16.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（公告於 2026-10-20）","citation":"公司 8-K Ex.99.1 調節表；新聞稿文字段落寫 216M，與調節表 212.6M 不一致，本表採調節表"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":428.12,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-2.94,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":69.72,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.8 → 10.8）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.08,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.11 → 12.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.07,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.66 → 13.67）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":10.8,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":12.12,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":13.67,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":3.65,"period":"2026-07-16 → 2026-10-21","unit":"%","basis":"FY1 共識 EPS 10.42 → 10.8（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":51.77,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":13.06,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":12.48,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":39.64,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 10.8，分子＝快照價 428.12","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-6800.4,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 0.0、現金 6800.4（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":353.28,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":144444.99,"period":"2026-10-22","unit":"USD m","basis":"市值 151245.39 ＋ 淨負債 -6800.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":11905.42,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":13302.16,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（31 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":12.13,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 428.12 / W52 460.04 / W104 488.41 / W250 386.35 / W250 13週斜率 0.3%"},{"id":"f_ma_w52","label":"52 週均線","value":460.04,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":488.41,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":386.35,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.3,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出 Surgerii、CMR、Distalmotion、Medicaroid、Medtronic、J&J、Noah、微創醫療機器人、SS Innovations 等為已推出或明確進入機器人手術的對手，並預期中國競爭加劇；2025 年中國競爭與反貪腐使裝機少於預期","source":"SEC EDGAR 10-K FY2025 Item 1/1A","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"In 2025, the effects of this campaign, combined with the competitive dynamics in China and various measures related to industrial policy, contributed to fewer systems being placed in China than we anticipated.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Q2 2026 財報電話會議：管理層稱中國招標減少、本土機器人競爭增加、政策導向降價壓力","source":"Webull：Intuitive Surgical Q2 2026 Earnings Call Transcript","url":"https://www.webull.com/news/15239187065545728","excerpt":"We continue to see lower tender activity, increased domestic robotic competition, and policy-driven pricing pressure.","as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 da Vinci 5 占美國系統裝機 85%，作者認為在 Medtronic Hugo、J&J Ottava 站穩美國前先鎖定醫院預算","source":"Yahoo Finance：ISRG just secured U.S. market","url":"https://finance.yahoo.com/sectors/healthcare/articles/isrg-just-secured-u-market-152824520.html","excerpt":"The da Vinci 5 (dV5) accounted for 85% of U.S. system placements in Q1 2026. This rapid adoption secures hospital capital budgets before Medtronic's (MDT) Hugo or Johnson & Johnson's (JNJ) Ottava can establish a significant U.S. foothold.","as_of":"2026-05-01","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：美國本土營收占 68%（2024 為 67%、2023 為 66%），海外 32%；銷售以直銷為主，客戶為各地醫院，10-K 此節未列單一大客戶占比","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"During the years ended December 31, 2025, 2024, and 2023, domestic revenue accounted for 68%, 67%, and 66%, respectively, of total revenue, while revenue from our OUS markets accounted for 32%, 33%, and 34%, respectively, of total revenue.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2026 年檢索未見信評機構調降 ISRG 信評；2026 年 7 月財報後的負面訊息來自 da Vinci 手術量成長指引與分析師目標價下調，而非客戶信用事件","source":"Tradingpedia / 搜尋摘要（2026-07-17 報導）","url":"https://www.tradingpedia.com/2026/07/17/intuitive-surgical-falls-as-growth-concerns-rise/","excerpt":"Intuitive Surgical reaffirmed its full-year 2026 outlook for da Vinci procedure growth at 13.5%-15.5% and indicated expectations closer to the midpoint of that range.","as_of":"2026-07-17","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ISRG Q2 2026: da Vinci procedures up about 15%, Ion procedures up about 36%; instruments and accessories revenue up 18% to $1.73B","source":"ISRG Form 10-Q for quarter ended 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001035267/000103526726000058/isrg-20260630.htm","excerpt":"observations, and remote proctoring. In 2019, we commercialized our Ion endoluminal system, which is a flexible, robotic-assisted, catheter-based platform that utilizes instruments and accessories for which the first cleared indication is minimally invasive biopsies in the lung. Our Ion system extends our commercial offering beyond surgery into diagnostic, endoluminal procedures.","as_of":"2026-07-23","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"ISRG Q2 call: 267 US system placements up 24%, ~70% of US acquisitions leased; US bariatric procedures fell (GLP-1), US deferrable growth slowed","source":"Nasdaq/Zacks: ISRG Q2 Earnings Call Signals Durable Demand & U.S. Caution","url":"https://www.nasdaq.com/articles/isrg-q2-earnings-call-signals-durable-demand-us-caution","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261022","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Vizient projects 3.05% inflation for medical and surgical products in 2027; care migration to ambulatory/home settings makes historical utilization less reliable","source":"Becker's Hospital Review: MedSurg demand shifts will reshape supply planning: Vizient","url":"https://www.beckershospitalreview.com/supply-chain/medsurg-demand-shifts-will-reshape-supply-planning-vizient/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素揭露：第三方（欲競爭器械或維修市場者）與部分客戶已對公司提出反壟斷訴訟；公司業務受美國與歐盟反壟斷法規範。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"Also, antitrust claims have been brought against us by third parties looking to compete in the instruments or servicing space and by certain customers.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 披露歐盟執委會於 2025-12-16 發布 EU MDR 針對性修訂提案，預期 2027 年前不會通過。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"On December 16, 2025, the European Commission published a targeted revision proposal of the EU MDR to address structural issues, certification delays, and burdens on small and medium-sized enterprises (SMEs). The proposal will enter the ordinary legislative procedure and is not expected to be adopted before 2027.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"第九巡迴法庭 2026-08 撤銷 SIS 反壟斷案原判（陪審團指示錯誤）並發回地方法院；Intuitive 2026-09-28 聲請全院重審","source":"Bloomberg Tax：Surgical Robot Monopoly Suit Revived Over Jury Instructions","url":"https://news.bloombergtax.com/antitrust/surgical-robot-monopoly-suit-revived-sent-back-to-trial-court","excerpt":"A trial court gave incorrect jury instructions on how to assess whether Intuitive Surgical Inc. unfairly cornered the repair market for its line of “da Vinci” systems, the US Court of Appeals for the Ninth Circuit said Thursday. The trial court was too demanding in what plaintiff Surgical Instrument Service Co.","as_of":"2026-08-13","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Intuitive 向上訴法院聲請全院重審，要求推翻復活 SIS 主張的合議庭判決","source":"MLex：Intuitive Surgical asks US appeals court for rehearing after loss in antitrust case","url":"https://www.mlex.com/mlex/articles/2531050/intuitive-surgical-asks-us-appeals-court-for-rehearing-after-loss-in-antitrust-case","excerpt":"Antitrust Artificial Intelligence Data Privacy and Security DealRisk® Energy Financial Crime Financial Services Intellectual Property Mergers and Acquisitions State Aid Technology Trade GDPR Enforcement Tracker TAKE A FREE TRIAL Toggle Dropdown Advanced Search Intuitive Surgical asks US appeals court for rehearing after loss in antitrust case","as_of":"2026-09-28","retrieved_at":"20261022","affects":["moat_trend","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"多數器械與配件在墨西哥 Mexicali 製造，多數符合 USMCA 原產地而至今未被課美國進口關稅；內視鏡多在德國製造且受關稅；自中國進口原料與組件、並將美製 da Vinci Xi 賣入中國，皆受關稅，預期持續不利中國 Xi 系統產品成本。2025 年關稅與其他貿易措施使銷貨成本增加約 6,300 萬美元，預期 2026 年續增。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A（Trade and Tariffs Update）","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"We currently manufacture a significant majority of our instruments and accessories in Mexicali, Mexico. Most of these products qualify as originating under the USMCA and, therefore, have not been subject to U.S. import tariffs to date. We also import certain raw materials and finished goods from outside of the U.S. that are subject to tariffs, including our endoscopes, a majority of which are manufactured in Germany.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025 年關稅與其他貿易措施使銷貨成本增加約 6,300 萬美元，並預期 2026 年關稅帶來的銷貨成本續增。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"In 2025, tariffs and other trade measures have increased our cost of revenues by approximately $63.0 million. Based on the announced and implemented global tariffs as of the date of this report, and assuming such tariffs remain in place, we expect our cost of revenues driven by tariffs and other trade measures to continue to increase in 2026.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025 年中國政府宣布對含中國產稀土的部分產品實施出口管制與許可要求；稀土為公司產品部分零組件的關鍵材料，若實施可能需為部分產品申請出口許可，並可能造成供應中斷。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"For example, in 2025, the Chinese government announced export controls and licensing requirements applicable to certain products containing Chinese-origin rare earth elements and may implement additional controls in the future. Rare earth elements are critical to certain components contained in our products, and China is a predominant producer of these materials.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋摘要顯示美國商務部自 2025-09-02 起對醫療器材啟動 Section 232 調查；搜尋未見已對器械全面課徵 232 關稅的來源。","source":"AmCham Malaysia：US Opens Tariff Probes into Medical Equipment, Robotics, Industrial Machinery","url":"https://amcham.com.my/us-opens-tariff-probes-into-medical-equipment-robotics-industrial-machinery/","excerpt":null,"as_of":"2025-09-02","retrieved_at":"20261022","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Q2 2026 10-Q 提及臨時 Section 122 附加稅到期後，美國依 Section 301 對 60 個貿易夥伴加徵一般 10% 或 12.5% 關稅。","source":"SEC EDGAR 10-Q Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/0001035267/000103526726000058/isrg-20260630.htm","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"器械與配件的絕大多數在墨西哥 Mexicali 生產，多數符合 USMCA 原產地而至今未被課美國進口關稅；內視鏡為進口、課關稅，多數在德國製造。","source":"ISRG Form 10-Q (period ended 2026-09-30), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001035267/000103526726000071/isrg-20260930.htm","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026 年前九個月計入銷貨成本的關稅與貿易措施為 $72.4M；另認列 IEEPA 關稅退款 $63.7M，後續退款金額仍不確定。","source":"ISRG Form 10-Q (period ended 2026-09-30), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001035267/000103526726000071/isrg-20260930.htm","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因子警告中國對稀土（含磁鐵）與關鍵礦物的出口限制，可能限制多項產品所用零件的取得；2025 年關稅與貿易措施使銷貨成本增加約 $63.0M，預期 2026 年續增。","source":"ISRG Form 10-K FY2025, SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"部分組裝零件來自單一或唯一來源供應商，以採購單而非長期供應合約購料，且通常存貨很少（FY2018 10-K 原文，後續年度重複為風險因子）。","source":"ISRG Form 10-K FY2018, SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526719000012/isrg-20181231x10k.htm","excerpt":null,"as_of":"2018-12-31","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 Q3 營收約 30.5 億美元、年增 22%；全球 da Vinci 手術量約 +14%（美國約 +10%、美國以外約 +20%）；Ion 手術量約 +31%；系統 546 台含 da Vinci 5 315 台","source":"ISRG Q3 2026 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001035267/000103526726000067/q326ex-991earningsrelease.htm","excerpt":"•Worldwide procedures (da Vinci and Ion combined) grew approximately 15% compared with the third quarter of 2025. Da Vinci procedures grew approximately 14%, and Ion procedures grew approximately 31%. •The Company placed 546 da Vinci surgical systems, compared with 427 in the third quarter of 2025. The third quarter 2026 da Vinci surgical system placements included 315 da Vinci 5 systems,","as_of":"2026-10-21","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"2026 年 da Vinci 手術量成長指引 13.5%–15.5%；Q2 美國成長放緩至 12%，延後性手術偏弱；管理層提及中國競爭與定價壓力、GLP-1 壓抑減重手術","source":"Nasdaq: ISRG Q2 Earnings Call Signals Durable Demand & U.S. Caution","url":"https://www.nasdaq.com/articles/isrg-q2-earnings-call-signals-durable-demand-us-caution","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Medtronic 的 Hugo 手術機器人於 2025 年 12 月取得 FDA 泌尿科適應症許可，可在美國醫院廣泛行銷。","source":"eWeek｜Medtronic's 'Hugo' Surgical Robot Receives FDA Clearance for Urological Procedures","url":"https://www.eweek.com/news/medtronic-hugo-robot-fda-approval/","excerpt":"Medtronic can now widely market its Hugo robotic-assisted surgery system to American hospitals.","as_of":"2025-12-31","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"J&J Ottava 據稱於 2026 年中獲 FDA 許可十項一般外科術式；Intuitive 2026 年股價大幅回檔（來源為股票分析文章）。","source":"TIKR｜Intuitive Surgical fell 30% in 2026 as a rival arrived","url":"https://www.tikr.com/blog/intuitive-surgical-fell-30-in-2026-as-a-rival-arrived-heres-where-the-stock-could-go","excerpt":"Six days later, the FDA cleared Johnson & Johnson’s Ottava robot for ten general-surgery procedures, the first credible challenger in soft-tissue surgery, da Vinci’s core turf, in two decades.","as_of":"2026-08-17","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Intuitive 因競爭與中國標案偏好本土廠商，成長放緩。","source":"Bloomberg｜Intuitive Surgical Falls as Rivalry, Funding Slows Growth","url":"https://www.bloomberg.com/news/articles/2026-01-14/intuitive-surgical-falls-as-rivalry-slows-down-flagship-robot","excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Medtronic 已提交 Hugo 一般外科與婦科 510(k)；2026-02-17 Cleveland Clinic 完成美國首例商業 Hugo 手術。","source":"MedTech Dive｜Medtronic completes first Hugo case in the US","url":"https://www.medtechdive.com/news/medtronic-completes-first-hugo-case-in-the-us/812325/","excerpt":"procedure for its Hugo robotic surgery system, shortly after the company received Food and Drug Administration clearance for the platform. The first surgery was a prostatectomy procedure performed at the Cleveland Clinic.","as_of":"2026-02-17","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"-","claim":"第三方再製 Intuitive 器械與 Restore Robotics 反壟斷訴訟威脅高毛利器械與配件業務；Deutsche Bank 2025 年 6 月因此降評。","source":"Motley Fool｜Why Intuitive Surgical stock plunged today","url":"https://www.fool.com/investing/2025/06/09/why-intuitive-surgical-stock-plunged-today","excerpt":null,"as_of":"2025-06-09","retrieved_at":"20261022","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：ISRG 以直銷為主（美國、西歐除義西葡希、中國合資、日韓印台加），其餘海外市場用經銷商；美國占營收 68%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"We sell our products and services through direct sales organizations in the U.S., Europe (excluding Italy, Spain, Portugal, Greece, and Eastern European countries), China (through our majority-owned joint ventures, Intuitive Surgical-Fosun Medical Technology (Shanghai) Co., Ltd. and Intuitive Surgical-Fosun (HongKong) Co. Ltd. (collectively, the “Joint Venture”), with Fosun Pharma), Japan, South Korea, India, Taiwan, and Canada.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Zacks：ISRG 數位訂閱（My Intuitive+）2026 起可能成為新營收來源，客戶約 Q2 2026 起可付費續約。","source":"Zacks: Can Digital Subscriptions Become ISRG's New Revenue Stream in 2026","url":"https://www.zacks.com/stock/news/2877905/can-digital-subscriptions-become-isrgs-new-revenue-stream-in-2026","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"ISRG 10-Q（2026Q3）可能載明義大利、西班牙、葡萄牙經銷業務收購／轉直銷的進度。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001035267/000103526726000071/isrg-20260930.htm","excerpt":"our completion of and ability to successfully integrate acquisitions, including the recently completed acquisition of the da Vinci and Ion distribution businesses in Italy, Spain, and Portugal and the transition from a distributor to a direct sales model in those markets;","as_of":"2026-10-22","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY26 da Vinci procedure growth guidance 13.5–15.5%（Q2 維持）；非 GAAP 毛利率指引由 67.5–68.5% 上調至 68–69%；未見下修","source":"Hudson Labs Q3 2026 earnings preview","url":"https://www.hudson-labs.com/research/intuitive-surgical-q3-2026-earnings-preview-isrg-results-preview","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga：27 位分析師（23 買／3 持有／1 賣），平均目標價 $539（2026-09-08）；Investing.com 29 位平均 $477、高 $685、低 $324","source":"Benzinga ISRG price-targets; Investing.com consensus estimates","url":"https://kr.benzinga.com/quote/ISRG/price-targets","excerpt":null,"as_of":"2026-09-08","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"目標價自上半年下移：Fintel 2026-02-25 平均 $624.51；Barchart（Q1 前）平均 $619.85；Evercore 7 月由 $480 降至 $430；BofA 5 月由 $650 降至 $520；HSBC 7/30 降評 Hold 目標 $931","source":"Barchart；Sell-side 報導彙整（Sahm Capital／SimplyWall.St 搜尋摘要）","url":"https://www.barchart.com/story/news/1159069/intuitive-surgical-s-q1-2026-earnings-what-to-expect","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 共識：Benzinga EPS $2.54、營收 $2,908M（Hudson）；TickerLeague EPS $2.63（16 位）；Q2 實績 EPS $2.80 vs 預期 $2.41、營收 $2.89B vs $2.82B，近四季皆優於預期","source":"Benzinga earnings-forecasts; TickerLeague; Hudson Labs","url":"https://tickerleague.com/companies/ISRG/estimates","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 EPS $2.80 vs 預期 $2.41，Q3 EPS 共識 $2.54","source":"Benzinga ISRG earnings-forecasts","url":"https://kr.benzinga.com/quote/ISRG/earnings-forecasts","excerpt":null,"as_of":"2026-09-08","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-03-01 完成收購 ab medica、Abex、Excelencia Robótica 等的 da Vinci 與 Ion 經銷業務（南歐）；10-Q 載現金支出約 5.28 億美元。","source":"SEC EDGAR 8-K Item 8.01（2026-03-02）","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000012/isrg-20260301.htm","excerpt":"On March 2, 2026, Intuitive Surgical, Inc. (the “Company”) issued a press release announcing the completion of its acquisition on March 1, 2026, of the da Vinci and Ion distribution business operated by ab medica, Abex, Excelencia Robótica, and their affiliates.","as_of":"2026-03-02","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"10-K 披露多起產品責任訴訟（da Vinci 設計瑕疵、訓練不足等指控）及 In Re: da Vinci Surgical Robot Antitrust Litigation 集體訴訟（器械維修服務反壟斷），均仍在辯護中。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"Three class action complaints were filed against the Company in the Northern District of California Court alleging antitrust allegations relating to the service and repair of certain instruments manufactured by the Company.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"da Vinci 5（非力回饋器械）取得 FDA 心臟手術適應症核准，1 月財報電話會議揭露；3 月另有力回饋器械更新取得 FDA 核准（10-Q 載）。","source":"MDDI：Intuitive's da Vinci 5 Secures FDA Cardiac Clearance","url":"https://www.mddionline.com/robotics/intuitive-s-da-vinci-5-secures-fda-cardiac-clearance","excerpt":null,"as_of":"2026-01-22","retrieved_at":"20261022","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"FDA 執行報告列 2026 年 da Vinci X/Xi 機械臂螺絲可能斷裂之 Class II 召回（Z-2046-2026，2026-05-01 分類）及病人側推車煞車固定銷 Class II 召回（Z-2521-2026，2026-06-22 公布）；未見 FDA 警告信。","source":"FDA 召回資料庫／MarketScreener 搜尋摘要","url":"https://www.marketscreener.com/news/intuitive-surgical-inc-announces-fda-enforcement-action-and-voluntary-recall-of-da-vinci-x-and-da-ce7f5addd889f620","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"-","claim":"2026-02-04 有團體向 FDA 提出公民請願，要求對 da Vinci 5 全系統 Class I 召回、發緊急安全通訊並對 Intuitive 發警告信；此為請求，未見 FDA 回應。","source":"Northeastern Univ. AJRC citizen petition (PDF)","url":"https://law.northeastern.edu/wp-content/uploads/2026/02/ajrc-citizen-petition-davinci.pdf","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#5","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 10 份 8-K 中僅 1 份（2026-03-02 Item 8.01 收購）屬重大項目；無 Item 4.02（重編）、1.03 等。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001035267&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-03-01 完成收購 ab medica、Abex、Excelencia Robótica 等的 da Vinci 與 Ion 經銷業務；10-Q 載現金支出約 5.28 億美元。","source":"SEC EDGAR 8-K Item 8.01（2026-03-02）","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000012/isrg-20260301.htm","excerpt":"On March 2, 2026, Intuitive Surgical, Inc. (the “Company”) issued a press release announcing the completion of its acquisition on March 1, 2026, of the da Vinci and Ion distribution business operated by ab medica, Abex, Excelencia Robótica, and their affiliates.","as_of":"2026-03-02","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K 披露產品責任訴訟與 da Vinci 維修反壟斷集體訴訟（2021 年起），仍在辯護；搜尋未見 2026 年新的證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm","excerpt":"Three class action complaints were filed against the Company in the Northern District of California Court alleging antitrust allegations relating to the service and repair of certain instruments manufactured by the Company.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"da Vinci 5（非力回饋器械）取得 FDA 心臟手術適應症核准，1 月財報電話會議揭露；3 月力回饋器械更新亦獲 FDA 核准（10-Q 載）。","source":"MDDI：Intuitive's da Vinci 5 Secures FDA Cardiac Clearance","url":"https://www.mddionline.com/robotics/intuitive-s-da-vinci-5-secures-fda-cardiac-clearance","excerpt":null,"as_of":"2026-01-22","retrieved_at":"20261022","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"FDA 列 2026 年 da Vinci X/Xi 機械臂螺絲 Class II 召回（Z-2046-2026）及病人側推車煞車銷 Class II 召回（Z-2521-2026）；未見 FDA 警告信。","source":"FDA 召回資料庫／MarketScreener 搜尋摘要","url":"https://www.marketscreener.com/news/intuitive-surgical-inc-announces-fda-enforcement-action-and-voluntary-recall-of-da-vinci-x-and-da-ce7f5addd889f620","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"product_recall_warning#1","axis":"product_recall_warning","section":"events","direction":"-","claim":"2026-02-04 公民請願要求 FDA 對 da Vinci 5 Class I 召回並發警告信；為請求，非 FDA 行動。","source":"Northeastern Univ. AJRC citizen petition (PDF)","url":"https://law.northeastern.edu/wp-content/uploads/2026/02/ajrc-citizen-petition-davinci.pdf","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ISRG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":66.68,"operating_margin_pct":31.28,"fcf_margin_pct":29.21,"rd_intensity_pct":12.82},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ISRG","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"MDT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.01,"operating_margin_pct":19.04,"fcf_margin_pct":16.33,"rd_intensity_pct":7.77},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"SYK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.98,"operating_margin_pct":21.73,"fcf_margin_pct":18.2,"rd_intensity_pct":6.42},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYK","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"BSX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":69.92,"operating_margin_pct":21.0,"fcf_margin_pct":8.6,"rd_intensity_pct":10.25},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"ISRG"},"financial_history":{"ticker":"ISRG","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":6222200000.0,"revenue_yoy_pct":null,"gross_margin_pct":67.44,"operating_margin_pct":25.35,"net_income":1322300000.0,"diluted_eps":3.65,"free_cash_flow":958400000.0,"fcf_margin_pct":15.4,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":7124100000.0,"revenue_yoy_pct":14.49,"gross_margin_pct":66.39,"operating_margin_pct":24.8,"net_income":1798000000.0,"diluted_eps":5.03,"free_cash_flow":749600000.0,"fcf_margin_pct":10.52,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":8352100000.0,"revenue_yoy_pct":17.24,"gross_margin_pct":67.46,"operating_margin_pct":28.12,"net_income":2322600000.0,"diluted_eps":6.42,"free_cash_flow":1303800000.0,"fcf_margin_pct":15.61,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":10064700000.0,"revenue_yoy_pct":20.51,"gross_margin_pct":66.0,"operating_margin_pct":29.27,"net_income":2856000000.0,"diluted_eps":7.87,"free_cash_flow":2490700000.0,"fcf_margin_pct":24.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ISRG/ISRG_Q3_2026_Earnings_Call_20261020.md）

# Q3 2026 Earnings Call
**Intuitive Surgical, Inc.** | Earnings Calls | 2026-10-20

**Operator** (Operator):
Hello, and welcome to Intuitive's Third Quarter 2026 Earnings Release. [Operator Instructions] I would now like to turn the call over to Dan Connally, Head of Investor Relations. You may begin.

**Daniel Connally** (Executives):
Good afternoon, and welcome to Intuitive's Q3 2026 Earnings Conference Call. Joining me today are Dave Rosa, our CEO; Jamie Samath, our CFO; Dr. Jaime Wong, our Chief Medical Officer; and Gary Loeb, our Chief Legal and Compliance Officer. 
Before we begin, I would like to remind you that comments made on today's call may contain forward-looking statements. Actual results may differ materially from those expressed or implied as a result of certain risks and uncertainties. These risks and uncertainties are described in our Securities and Exchange Commission filings, including our most recent 10-K filed on February 3, 2026, and 10-Q filed on July 21, 2026. Our SEC filings can be found through our website at intuitive.com or at the SEC's website. 
Investors are cautioned not to place undue reliance on such forward-looking statements. This conference call will be available for audio replay on our website in the Events section under our Investor Relations page. We have posted today's press release and supplementary financial data tables to our website. 
Our format for this afternoon's conference call is as follows: Dave will review our business and operational highlights, Jamie will review our financial results and procedure highlights, Jaime Wong will review clinical highlights, I will review our updated financial outlook for 2026 and finally, we will host a question-and-answer session. With that, I will turn it over to Dave.

**David Rosa** (Executives):
Good afternoon, and thank you for joining us today. Q3 was a strong quarter for Intuitive with broad-based adoption across our multiport, single-port and Ion platforms. In Q3, total procedures increased 15%, driven by 14% growth in da Vinci procedures and 31% growth in Ion procedures. In the U.S., da Vinci procedure growth was 10%, and outside the U.S., da Vinci procedure growth was 20%.
We exited the quarter with more than 13,200 da Vinci and Ion systems installed worldwide. Over time, our customers have adopted, operationalized and standardized on the da Vinci ecosystem to provide their patients with improved care. That adoption has been driven by our commitment to innovation, robust training and clinical evidence, and it is apparent in how customers use da Vinci today. In the quarter, almost 7,000 customers in more than 70 countries performed da Vinci procedures at a rate of over 10,000 procedures per day. 
On the clinical evidence front, more than 48,000 peer-reviewed publications have evaluated the effectiveness of da Vinci surgery, including the recent benign COMPARE study, which Jaime Wong will discuss in more detail shortly. As I described last quarter, we continue to see increasing segmentation across our customer base. Needs vary by procedure, site of care, geography and health care system. 
We have been investing to support the segmentation, and we have positioned Intuitive to serve current and future customers with both our existing technologies and those in development. Meeting those needs also requires that we evolve our commercial approach to tailor how we engage, price and provide solutions for customers in each segment. 
In Q3, global customer demand across our da Vinci portfolio remains strong. Da Vinci system placements increased 28% worldwide with da Vinci 5 and SP accounting for 65% of global placements. Installations of XiR and X more than doubled in the quarter. Customers continue to adopt da Vinci 5 and its growing capabilities with demand for both capacity expansion and system upgrades.
We exited the quarter with more than 2,000 da Vinci 5 systems installed worldwide used by over 18,000 surgeons since launch. We continue to see strong interest in XiR, both in the U.S. and internationally, where customers are leveraging its familiarity, capabilities and cost profile to build programs around a focused set of procedures. Our da Vinci single-port platform is playing an increasingly important role for our customers and their patients. 
Our investments in additional clearances and instrumentation are yielding results as SP procedures expand in the U.S. and internationally. Adoption of the new SP stapler continues to broaden. And in Q4, we plan to make a U.S. submission for the SP vessel sealer, which we believe is a key enabler for wider adoption of our SP platform. 
Increasingly, customers that adopt both multiport and single-port describe benefits to their overall da Vinci programs, with SP opening new approaches for the surgeon, while existing procedure demand fills their multiport capacity. In Q3, we finalized a set of pricing actions for a subset of high-volume benign procedures where costs may be a constraint to broader access to da Vinci surgery. 
We believe these actions, in conjunction with increased availability of XiR, will expand our addressable opportunity and enable da Vinci technology to reach more patients around the world. Jamie will describe the anticipated impact shortly. Outside the U.S., we are elevating our focus and increasing our investments to help customers establish and expand their da Vinci programs. As of Q3, nearly 4,000 international customers have a da Vinci program and nearly 25% operate two or more systems. These customers are moving beyond urology and cancer procedures into benign hysterectomy in Germany, cholecystectomy in the U.K. and India, and inguinal hernia repair in Japan. 
To support this growth, we are continuing to build the foundation of market access country by country through regulatory clearances, reimbursement, training and clinical and economic validation. Da Vinci placements outside the U.S. increased 29% in the quarter with broad-based global demand. In Europe, Germany led the region with 20 system installations. We also placed systems in more than 20 other European countries and benign procedures led procedure growth. 
In Asia, Japan improved on both system placements and procedure growth for the second consecutive quarter, while India had another strong quarter with 42% procedure growth, surpassing 200,000 cumulative da Vinci procedures. In China, the operating environment remains challenging. To support expected long-term growth in Asia, we recently announced plans for a significant new I&A manufacturing facility in Penang, Malaysia. We expect this facility to begin operations in 2028.
Beyond da Vinci, we are investing in Ion outside the U.S. through multiyear country-by-country work that is foundational to broadening access and shortening the time between detection and treatment of lung cancer. During Q3, we received reimbursement for Ion in Korea, and we expect further reimbursement actions in other geographies in the coming quarters. 
This quarter, we received several CE marks, including Force Feedback instrumentation and cardiac procedures on da Vinci 5 as well as transvaginal gynecological procedures on SP. We now have da Vinci 5 cleared for cardiac procedures in the U.S., Europe, India, Japan and Korea. During Q3, we received FDA 510(k) clearance on da Vinci 5 for surgeon-initiated tool eject and multi-arm targeting, both of which bring incremental efficiency and surgeon autonomy to procedures. 
Surgeons have reported that these innovations support extending access to da Vinci surgery beyond traditional workdays and hours. Recently, we submitted a cavitational ultrasonic aspirator instrument for FDA 510(k) clearance for use in liver and pancreas procedures. And last week, we received FDA 510(k) clearance for an integrated version of the da Vinci 5 handheld endoscope. 
In August, we received FDA 510(k) clearance for our foundational noncommercial next-generation flexible robotic endoscope system for use in the gastrointestinal tract. This program is early in its development, but we are encouraged by our progress and look forward to updating you as we advance. 
Adoption of Intuitive Telepresence continues to increase with surgeons using these sessions to share techniques and to scale training in ways that were not previously practical. Telepresence on da Vinci 5 serves as a foundation for our efforts in telesurgery, where we expect several regulatory clearances in the first half of 2028. 
Our teams continue to develop additional digital and AI capabilities on da Vinci 5 including a voice-activated user interface and automated fourth arm control to further enhance efficiency and the user experience. AI-controlled motion in surgery has the potential to improve efficiency and outcomes, but it is early and must earn the confidence of regulators, surgeons, care teams and patients before we deploy it at scale. 
Looking ahead, our objective at Intuitive is to reach more patients with the best care available by combining robotics, human expertise, data and artificial intelligence so that minimally invasive care becomes more accessible and less variable. The problems we are working to address are significant and specific. Minimally invasive surgery access and adoption remain uneven around the world. Patients wait too long between detection and treatment and the care a patient receives still varies more than it should, depending on the hospital they enter and the surgeon available that day.
Over time, we are focused on significantly advancing the Quintuple Aim to ensure that the broader patient journey can become more predictable, more connected and less disruptive to a patient's life. Before I pass the time to Jamie, today, we announced that we have reached an agreement, subject to court approval, with U.S. customers who participated in the class action lawsuit on third-party remanufacturing of da Vinci instruments and third-party servicing of da Vinci systems. We believe that this no-fault settlement provides certainty for both our customers and Intuitive and maintains our ability to advance the safety, quality and security of our products. 
And with that, I'll turn the time over to Jamie to take you through our finances in greater detail.

**Jamie Samath** (Executives):
Good afternoon. I'll describe our performance on a non-GAAP basis, and I'll summarize our GAAP results later in my remarks. A reconciliation between our non-GAAP and GAAP results is available on our website. The strength of our financial performance this quarter reflects the durability of our business model driven by an expanding portfolio of differentiated products that provide clear clinical and economic value for our customers and their patients.
Increasingly, our da Vinci and Ion systems and the Intuitive ecosystem are being integrated into customers' core infrastructure across a variety of procedures, sites of care and geographies, driving value for hospitals and health care providers and recurring revenue for Intuitive. Today, we are also quantifying the instrument pricing actions we discussed in July, which we expect to reduce da Vinci I&A revenue per procedure by approximately 3% to 5% on a mix-constant basis once fully implemented. This is a deliberate choice to broaden adoption in high-volume benign procedures, and I will describe these actions in more detail shortly. 
Key financial highlights for the quarter are as follows: Revenue grew 22% to just over $3 billion, of which 84% was recurring revenue. Net da Vinci placements, that is placements that expand the installed base grew 40%. Non-GAAP operating margin was 42% of revenue or 41%, excluding a onetime pretax tariff refund of $28 million. Non-GAAP earnings per share grew 25% to $3 per share. 
Core metrics were solid in Q3. Taking da Vinci and Ion together, total procedures grew 15%, the installed base of systems grew 13% and average system utilization increased 2%. Revenue growth of 22% against total procedure growth of 15% reflects our innovation-led strategy and growth in system placements. As da Vinci 5, SP and Ion become a greater proportion of our business, revenue growth benefits from a richer product mix, higher levels of integration and incremental upgrade volumes.
Additionally, the scale and cost advantages we have built allow us to broaden our platform portfolio, reach customers in more geographies and expand access by lowering the cost of da Vinci surgery. The price reductions are concentrated in high-volume benign procedures where cost may be a barrier to adoption. Those procedures, particularly outside the U.S. and in ambulatory settings are where we see the largest opportunity to serve incremental patients. This is a strategic decision to reinvest a portion of the value our innovation creates and lower customer costs where they will have the greatest impact on adoption. We believe broader adoption creates more long-term value than near-term revenue per procedure.
Turning to the clinical side of our business. In the U.S., total procedures increased 11%, reflecting 10% growth in da Vinci procedures and 29% growth in Ion procedures. U.S. da Vinci growth of 10% was consistent with the expectations we described in July and reflects in part the 16% growth in the prior year quarter, our most difficult comparison of the year. 
After-hours procedures and benign gynecology procedures other than hysterectomy continue to lead growth. Da Vinci 5 accounted for more than 1/4 of U.S. procedures in Q3, up from 13% a year ago, and da Vinci 5 systems continue to run at utilization above our Xi base. Looking ahead, we believe the breadth of surgeon adoption, the continued expansion of benign general surgery and a growing da Vinci 5 and SP installed base, together with procedures earlier in adoption, including emergent general surgery, cardiac and nipple-sparing mastectomy positions us for durable U.S. procedure growth over the long term. 
In the short term, we continue to monitor the impacts from lower ACA enrollment, changes to Medicaid eligibility and potential changes to 340B. Outside the U.S., total and da Vinci procedures grew 20%, with Europe up 20%, Asia up 19% and Rest of World geographies up 22%. In Europe, growth was led by the U.K., Germany and Italy. In Asia, India and Taiwan led growth, and Japan procedure growth accelerated, reflecting early signs of a response to the June reimbursement changes. 
Procedure growth in China was roughly in line with the corporate average, reflecting lower recent capital placements. In Rest of World markets, growth was led by Canada, Australia and Brazil. Within OUS results, da Vinci adoption for benign procedures continued to accelerate, growing 41% in Q3, up from 37% in Q2 and 34% in Q1 with the strongest growth in hernia repair and cholecystectomy. Benign procedures represent over 1/4 of our international volume today and the significant majority of the gap between our current international volumes and the addressable opportunity, which is why they are a focus of our investments. 
As we build local clinical and economic evidence, a growing number of customers in OUS markets are recognizing the clinical benefits of da Vinci for these procedures and our tiered system portfolio, including XiR, together with the pricing actions I will describe shortly, provides customers the flexibility to rightsize their programs relative to local reimbursement. 
Third quarter SP procedure growth was 55%, reflecting accelerated growth in the U.S. of 50% and growth of 40% in Korea, our largest SP market. We now have 487 SP systems installed across 27 countries, and procedures in the 25 markets other than the U.S. and Korea nearly doubled from Q3 last year. Total I&A revenue in quarter 3 grew 18% to $1.8 billion. Da Vinci I&A revenue per procedure was approximately $1,860 compared to $1,800 last year, primarily driven by higher SP procedures and da Vinci 5 specific I&A, partially offset by procedure mix. 
With respect to instrument pricing, there are 2 developments to describe. The first is a set of pricing actions we will implement beginning in the first half of 2027, including the expansion of our extended use program announced in May. The second is a policy-driven price reduction in China that starts to take effect next month. As Dave described earlier, customer needs are increasingly segmented. In complex procedures, value comes from innovation and clinical capability. In high-volume benign procedures such as cholecystectomy and inguinal hernia repair, it comes from reliability, efficiency and economics, and that's where our pricing actions are focused.
Beginning in the first half of 2027, we will extend the useful lives of a subset of core EndoWrist instruments on our fourth and fifth generation platforms and introduce volume-based pricing; both lower our customers' cost per procedure. Years of investment in instrument design and manufacturing scale enable us to preserve the quality and reliability customers count on. 
In the U.S., the extended use instruments require a 510(k) clearance, which is in process. In China, the charge code policy changes we described last quarter will result in a significant reduction in our I&A prices in that market beginning in November. We continue to engage with the provincial governments on implementation and to progress through the green channel process for SP and da Vinci 5.
Taken together, we expect these pricing actions and the China price reduction to lower da Vinci I&A revenue per procedure by approximately 3% to 5% on a mix constant basis once fully implemented, meaning holding procedure, product and geographic mix constant to isolate the pricing changes themselves. For reference, that is less than the 7% we estimated when we launched our first extended use program in 2020. 
The accretive dynamics we described last quarter, including Force Feedback adoption and the mix shift toward da Vinci 5 and SP are not included and will be positive contributors to I&A revenue per procedure. In terms of timing, the China reduction takes effect in the fourth quarter, while the extended life instruments as part of our broader I&A pricing actions will roll out by country beginning in the first half of 2027. So the remaining impact will build progressively over 2027 rather than as a step function. 
Turning to cleared procedure categories that we expect to be future growth drivers. Cardiac procedures grew 40% in Q3. And during the quarter, we received CE mark for use of da Vinci 5 in cardiac procedures in Europe. We now estimate that the line of sight cardiac opportunity is between 300,000 and 400,000 procedures a year in the regions we are cleared. Separately, breast surgery grew 42%. Both remain early-stage opportunities whose near-term pace is linked to the training of surgeons and the accumulation of clinical evidence, and we are investing in both. Today, these procedure volumes are still small relative to our total volume.
Turning to capital performance and starting with our da Vinci business. We placed 546 da Vinci systems in quarter 3, an increase of 28% compared to 427 systems in Q3 last year. Demand was broad-based across our platform portfolio, 315 da Vinci 5 systems, 87 Xi, 65 XiR, 42 SP and 37 X systems. Da Vinci 5 placements included 41 in OUS markets, up from 12 last year as da Vinci 5 becomes available in more countries.
In the U.S., we placed 335 systems, up 27% from the 263 systems placed last year, driven by an increased number of multisystem deals as customers continue to convert to da Vinci 5. Building on our focus on ambulatory surgery centers, we installed 18 systems at U.S. ASCs in Q3, including 15 XiR systems. This is an early-stage multiyear effort and placements will be uneven quarter-to-quarter, but our pipeline of ASC opportunities continues to build, informed by customer familiarity with XiR's capabilities and reliability and its favorable cost profile.
Outside the U.S., we placed 211 systems, an increase of 29% compared to the 164 systems placed last year. By region, we placed 115 systems in Europe, up 83% from 63 last year, 78 in Asia, up 30% from 60, and 18 in Rest of World countries compared to 41 last year. Rest of World placements tend to be uneven quarter-to-quarter. 
Europe's performance reflected our broadening focus with record quarterly placements in Portugal, Turkey and Austria and solid growth in Poland, Croatia and Romania. Across all geographies, we placed 37 X systems and 65 XiR systems with purchased ASPs of approximately $0.5 million and $1.2 million, respectively, demonstrating our ability and willingness to compete effectively across the broad spectrum of customers and their economic objectives. 
Over the last 3 years, we have entered new geographies, including Croatia, Peru, Morocco and Lithuania. And in 2027, we plan to accelerate our expansion into additional countries we do not serve today. Given increasing investments in OUS markets and planned expansion into new geographies, in January, we plan to update our estimate of the long-term opportunity in soft tissue surgery. We placed a record 42 SP systems in Q3, including 21 in the U.S. and 12 in Korea, and the installed base of SP systems increased 42% from the year ago period to 487 systems. 
For our Ion platform, we placed 56 systems in Q3 compared to 50 systems last year. Given our capital performance, quarter 3 systems revenue grew 30% to $769 million. The average selling price for purchased da Vinci systems was approximately $1.6 million, flat to last year as a higher mix of da Vinci 5 was primarily offset by a higher mix of XiRs. Quarter 3 service revenue increased 22% to $482 million, reflecting the increased installed base of da Vinci and Ion systems and a higher mix of da Vinci 5.
Turning now to the rest of the P&L. Non-GAAP gross margin for the quarter was 69.9%, an increase from 68% in Q3 of last year. Q3 results included a onetime benefit of $28 million from the refund of previously paid IEEPA tariffs. Excluding this benefit, non-GAAP gross margin would have been 68.9%, an improvement of 90 basis points year-over-year.
The underlying improvement primarily reflects product cost reductions and fixed overhead leverage and our engineering and operations teams continue to execute on cost reduction programs across each of our platforms. Quarter 3 non-GAAP operating expenses increased 18% year-over-year, driven by increased variable compensation, reflecting our results, higher headcount and higher prototype expenses as several programs advanced in development. 
R&D again grew faster than SG&A and a portion of the increase reflects the timing of expenses between quarters. Given the progress our R&D teams are making and the opportunities in front of us, we will continue to prioritize incremental investment in our existing and new platforms and in advancing our AI capabilities, which we believe will meaningfully differentiate our solutions and expand the number of patients we can serve.
Non-GAAP other income was $75 million for the quarter compared to $83 million last quarter, reflecting lower average cash balances following our share repurchases. Our non-GAAP effective tax rate for the quarter -- for quarter 3 was 21.4%, consistent with our expectations.
Now turning to our GAAP results. GAAP net income for the quarter was $523 million or $1.49 per share compared to $704 million or $1.95 per share in Q3 of last year. Our GAAP results reflect the $450 million litigation settlement that Dave described earlier. This settlement is subject to court approval, and we do not expect that decision until next year. We ended the quarter with $6.8 billion in cash and investments, down from $8.6 billion last quarter. Cash generated from operating activities was more than offset by stock repurchases of $2.9 billion at an average price of $377 per share and capital expenditures of $113 million.
With that, I'll turn it over to Jaime to discuss recent clinical publications.

**Jaime Wong** (Executives):
Thank you, Jamie. It's a pleasure to speak with you this afternoon. As we routinely do on these calls, I'd like to share with you recently published peer-reviewed literature that we found to be notable. In addition to the specific data highlighted on this call, we encourage you to consider this data alongside the wider body of evidence detailing these topics and others and published scientific studies over the years. 
On our Q4 2024 earnings call, we described the landmark COMPARE study, a meta-analysis where the authors reported multiple benefits for the da Vinci approach when compared to alternative minimally invasive or open approaches in commonly performed oncologic procedures. Last month, Dr. Thomas Shin and colleagues from the Massachusetts General Brigham and the University of Virginia School of Medicine in collaboration with researchers from Intuitive, published the benign COMPARE study, comparing perioperative outcomes of benign, minimally invasive, laparoscopic, da Vinci robotic, and open procedures, a systematic review and meta-analysis of evidence in Annals of Surgery Open. 
This benign COMPARE study looked primarily at standard perioperative and 30-day clinical outcomes of 13 high-volume benign procedures across general surgery, gynecology, urology and bariatrics, including but not limited to, benign hysterectomy, cholecystectomy, benign colon and various hernia repairs. In many of these procedures, conventional laparoscopy has long been the standard of care. 
This meta-analysis included data from 366 studies across 32 countries published between 2010 and 2024 and included randomized controlled trials, prospective and retrospective cohort studies and large real-world database studies. In total, the analysis covered roughly 1.5 million da Vinci patients, 10.7 million laparoscopic patients and 1.7 million open patients. 
Results identified lower conversions to open surgery as the most clinically important and consistent finding. Compared with laparoscopy, da Vinci procedures were associated with 54% lower odds of conversion with significant reductions observed in benign hysterectomy, ventral and inguinal hernia repair, myomectomy, cholecystectomy and benign colon surgery. 
As the authors noted, conversion to open surgery is an important intraoperative event associated with increased morbidity and prolonged hospitalization, which has negative implications for patients and health care systems. Da Vinci patients also had 13% lower odds of blood transfusion and a shorter length of stay than laparoscopic patients, with the largest reductions in benign colon surgery, adrenalectomy and benign hysterectomy. 
Rates of 30-day complications, readmissions, and mortality were comparable between da Vinci and laparoscopy, while average da Vinci operative times were about 24 minutes longer. Compared with open surgery, da Vinci was associated with larger differences across nearly every studied measure, including 46% lower odds of postoperative complications and hospital stays that were nearly 2 days shorter. These differences have positive implications for patients and health care systems.
The authors concluded that da Vinci was associated with fewer conversions, less pain and faster recovery compared with open and laparoscopic surgery, supporting its effectiveness for benign indications. From my perspective as a surgeon, this large-scale analysis of millions of patients provides meaningful data on the expanding use of da Vinci surgery beyond oncology. These clinical correlations point toward a compelling value proposition for the use of da Vinci in these commonly performed high-volume benign procedures.
With that, I'll pass the time over to Dan.

**Daniel Connally** (Executives):
Thank you, Jaime. Our updated financial outlook for 2026 is as follows: Starting with da Vinci procedures. In July, we forecast full year 2026 procedure growth to be within a range of 13.5% to 15.5%, with an expectation to be closer to the midpoint. We are narrowing our forecast to be within a range of 14% to 15% with an expectation to be closer to the midpoint. Our range continues to consider the impact of changes to ACA premium subsidies on patient behavior in the U.S. as well as tender volumes and competitive intensity in China, among other factors.
Turning to gross profit. On our last call, we forecast non-GAAP gross profit margin to be within a range of 68% and 69% of revenue, including an estimated 100 basis point impact from tariffs as well as related refunds. We are updating our estimate to be within a range of 68.7% and 69.3% of revenue, including an estimated 90 basis points impact from tariffs as well as related refunds. Factors impacting the range include faster growth of newer products in da Vinci 5 and Ion, partially offset by product cost reductions. We continue to forecast higher input costs in certain areas like freight and semiconductor memory.
Our actual non-GAAP gross profit margin will vary depending largely on product, regional and trade-in mix and pricing. For operating expenses, we continue to expect 2026 non-GAAP operating expense growth of 11% to 13%. As a reminder, in Q4 2025, we made a $70 million multiyear contribution to the Intuitive Foundation. We do not expect to make a contribution to the foundation in 2026. Throughout the year and in Q3, in particular, we grew R&D at a rate above SG&A. We expect that trend to continue over the remainder of the year.
We now estimate noncash stock compensation expense between $860 million and $870 million. We now forecast non-GAAP other income, which is comprised mostly of interest income of between $300 million and $310 million due primarily to the impact of share repurchase activity in Q3. With regard to income tax, we expect our non-GAAP effective tax rate in Q4 to be 22%, plus or minus 50 basis points. That concludes our prepared remarks.
As we open the line to your questions, we ask that you limit yourselves to 1 question so that we may reach as many analysts as possible.

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Lawrence Biegelsen with Wells Fargo.

**Larry Biegelsen** (Analysts):
I'll just keep it at one here, focused on U.S. procedure growth. So Jamie or Dave, U.S. da Vinci procedure growth was stable on a stack 2-year basis, but the 10% growth in the quarter was the lowest we've seen since COVID. Shipments were strong, and it sounds like you have a ton of innovation and the extended use program is coming. So are we seeing a temporary lull in U.S. da Vinci procedure growth and the innovations and the pricing actions will help accelerate U.S. da Vinci procedures as soon as next year? I'd love to get any color on that.

**David Rosa** (Executives):
Yes. Larry, this is Dave, and I appreciate the question. Let me frame up the U.S. opportunity a bit and then Jamie can dive in with some specifics. So for me, the U.S. opportunity really breaks down into 2 areas. The first is about the addressable opportunity right in front of us that we're going after on a daily basis. 
And the second is a longer-term opportunity to expand the indications that da Vinci can have an impact in. And so if we look at the first part for the procedures that we know where the U.S. procedure opportunity is significant, particularly in benign general surgery, when I'm talking to customers, in order for them to adopt robotics across the benign general surgery areas as well as other benign indications, they really want to see how it compares to the alternatives, where laparoscopy is well entrenched like Jaime described, and against open surgeries sometimes. 
They want to see how is it doing clinically, how is it doing economically. And that is something we've invested in for a long time. We've worked hard to provide customers the data that they need from Intuitive, combine it with their data so they can understand how those modalities are doing against each other. In Q3, I had the opportunity actually to meet with about 5 large IDN customers. And when I was meeting with them, what I'm seeing is now they are developing their own real-time dashboards, looking at the economics and the clinical outcomes relative -- of da Vinci relative to laparoscopy and open.
And I think that's a shift that I believe is worth noting because it's moving from anecdotes and sort of episodic data that they may look at once a year, and they're looking at it on a routine basis. And so when I saw those data and talk to those customers, robotics is comparing favorably as compared to the other modalities. And so you take that, that sort of foundation of data. You get directional data from studies like COMPARE, but you get the actual data in our customers' hand through these interactions like I'm describing. Combine that with our portfolio, the rest of our ecosystem, with the commercial performance of our capital teams expanding capacity, with the focus of our commercial teams broadly, clinical service, training and the pricing actions that Jamie described. And I think that's the foundation of a durable U.S. procedure growth into that significant opportunity.

**Jamie Samath** (Executives):
Larry, I might just add. The way we think about it, the unit opportunity in front of us in the U.S. is significant. I understand investor intention on the U.S. kind of growth over the last several quarters. There's 4 things that we're focused on that we're driving, maybe just to add some color. First is adding capacity, particularly to support the benign general surgery growth. And what you saw in this quarter was U.S. net placements increased 41%, and that's a little bit of a change from what we've seen in more recent quarters.
Second thing is, as we've talked about, we've more recently added a focus on the ASC opportunity. If you look at the number of systems we've placed in ASCs last 2 quarters combined, that's more than we've placed in ASCs in almost the last 3 years, and we think that continues to be an attractive opportunity for us. And those first 2 areas are supported by both the I&A pricing actions that we've described and our tiered portfolio. 
If you want to invest in da Vinci 5 in the hospital with its capability -- with a capability that will only grow every year as we do software updates and extend the ecosystem, that's a good investment. But our tiered portfolio offers those customers an XiR in a HOPD or an ASC. 
The other 2 areas that we're driving, we're focused on over longer horizons. Three is to kind of progress cardiac and breast along the early-stage adoption curve it's in, and that requires both investment and execution. And then the fourth is what Dave described, we have programs today in R&D that have the potential to add new indications in the U.S. and elsewhere. And those are moving along and progressing and those are quite interesting. Again, they're on longer-term horizons.

**Operator** (Operator):
Our next question comes from the line of Robert Marcus with JPMorgan.

**Robert Marcus** (Analysts):
I want to follow up on the extended use, and it's great, I appreciate the 3% to 5% headwind over the total enactment period, both between that and the China pricing. How do we think about necessarily the time lines? Will there be any stocking ahead of the implementation of this? And how do we think about it down the P&L, both from a gross and operating margin? If I could add one more there. Last program, you did have a price elasticity benefit on volumes. How are you thinking about volumes in response to the pricing actions?

**Jamie Samath** (Executives):
You'll probably have to remind me of your questions, Robbie, as I go along. But there may well be a little bit of stocking kind of customer ordering pattern volatility across the period in which we launch. I wouldn't expect that at this point to be significant. And obviously, we'll call that out as that occurs. In terms of the impact on gross margin, I would say that it would be a modest impact on gross margin that we'll look across '27 to offset with the cost reduction programs that we have in play. And therefore, whatever impact there is on gross margin can fall through to operating margin, but I expect that to be small and offset at some point in the year. 
With respect to elasticity, I would just say we believe that these actions will drive elasticity. That's the underlying intention because where we're applying them to the greatest extent is where there is cost sensitivity or cost is a barrier to adoption. And the benefit for those high-volume benign procedures is quite a bit greater than the blended 3% to 5%. Obviously, that's our intention. 
We have looked back at the first EUP program that we did in 2020 and our data supports the existence of elasticity. And we have confidence that that implementation was successful. That, of course, is looking at our own data, but also getting feedback from our customers. And so over time, as we address economics and you think about how we frame our line of sight opportunities, as we address economics and bring costs down, we expect to increase the addressable market for Intuitive. And so those are the underlying intents. But I think we have relative confidence in the elasticity. That doesn't obviously turn on immediately in 2027, but over time.

**David Rosa** (Executives):
You know what, I know that pricing is a focus of the question as it relates to benign procedures and addressable opportunity, but I also -- I want to make sure that we are recognizing the value of our entire portfolio. And so da Vinci 5 and its innovation, we're pricing such that innovation is correlated to the value it creates. And so we have that thrust and that focus in our portfolio while actively doing the lowering of cost that Jamie described because that's where broader access matters. And so it's not a trade-off, it's our strategy to really expand our addressable market and serve more patients around the globe, and we're confident that it's going to make a difference as we look forward.

**Operator** (Operator):
Our next question comes from the line of Travis Steed with Bank of America.

**Travis Steed** (Analysts):
Maybe just a pipeline question, especially with this quarter being probably the biggest quarterly buyback you've ever done. So congrats on that. There's a lot of focus on U.S. procedures. And one of the things I've thought about is there are things that -- in the pipeline that can add revenue per procedure. And as we're looking at the pipeline, if there's anything you'd like to point to or what could be coming on AI use cases or imaging things or even anything that's interesting on the GI robot or lung cancer that could be helpful for investors at this point.

**David Rosa** (Executives):
Yes. Thanks, Travis. It's a great point and one that we've described a couple of times in previous quarters. Starting maybe with Ion actually, the 2 active development programs that we have that are progressing strongly. One is around a ROSE system. And that's on-site cytology so that the physician and the care team can understand if they -- the cells may be cancer or not real time. And so they can get better answers than they do today and do it more quickly. 
And the second program there is endobronchial ultrasound integrated into the Ion platform. And so that allows us to do staging. Both of those should be and bring value to the Ion program, speed up the time, we think, from detection to diagnosis and ultimately treatment, but will be accretive to the revenue per case on the Ion platform. 
You mentioned vision is another area that we're very excited about when it comes to da Vinci. And so we have multiple programs going there with advanced visualization technology around hyperspectral imaging of fluorescent molecules and some AI features that we do think will bring that incremental value, and we're going to be able to add some revenue per procedure as a result. And so it is exactly my point of this is where innovation can bring outsized value to the customer and then bring some accretive revenue on a per procedure basis to Intuitive. And we have that across our portfolio.

**Operator** (Operator):
Our next question comes from the line of Rick Wise with Stifel.

**Frederick Wise** (Analysts):
Another question about the ASC opportunity. Can you talk about your progress and what's next and maybe bring the contribution to future growth and how these next-generation extended use approach maybe impacts the opportunity. But related to that, maybe you can touch on now just with the Stryker CMR news, we have 2 competitors likely offering modular systems in the ASC. How do the competitive dynamics play in there? Does Intuitive need a modular offering of some kind? And just help us think through those various points.

**David Rosa** (Executives):
I appreciate the question, Rick. And maybe I'll break it down into kind of 2 parts because one is around the ASCs. And again, we've described this before. If you talk to ASC customers, what they're asking for is not a particular architecture. What they're asking for is something that can be repeatable, easy to learn, easy to use, reliable and serve the procedures that they're targeting for the ASCs in a very consistent way because it's about volume and it's about getting patients out in a repeatable, knowable way. 
So if you use that as the problem to be solved in the ASC environment, now you can start saying what kind of technology matches that and best serves that problem or solves the problem to be solved. And so if you look at how might customers look at robotic competitors and make a choice and -- for me, it comes down to basically 3 areas. One is it's got to be the right architecture for the ASC. It's got to be -- have the right portfolio of systems so that it can be priced in a manner that fits their economics. You got to have that broader ecosystem because we know that's what leads to good outcomes. 
And then you have to have the supporting infrastructure, all the teams and capabilities that are required to make sure a program runs at pace. And so customers understand this. They're now looking across potentially multiple solutions. And there -- they understand that it takes more than a robot. It does take an ecosystem, but the robot is front and center. 
And so you asked about the architectures. And if I look back over our 30 years, we have engineered and tested just about every form of architecture there is out there. And that includes modular, table-mounted and other types of robots. We brought in customers to assess them and to evaluate them side-by-side with us. And we continue to believe that a cart-based architecture consistent with da Vinci is the best option. It's the best balance of capability and usability no matter where you look, and it might be in the main OR or in the ASC environment. 
And so if you -- we believe that it is not required to have a modular type of architecture to serve the needs of the customer in these segments where they are doing benign procedures and maybe increasingly complex procedures over time. And so I think we are well positioned with our portfolio, the pricing that Jamie described to serve the needs of our customers there and we look forward to earning their first choice.

**Jamie Samath** (Executives):
And Rick, maybe just some framing in terms of numbers. These are a bit lagged, but we think a little under 10% of the U.S. soft tissue surgery business is in ASCs today. That's growing. About 70% of those volumes are ASCs associated with or affiliated with existing IDNs. So they are customers and surgeons that we know. That's our initial focus. Our penetration of kind of all of the ASC opportunity is low in the first quartile. And that's why now that we have XiR and we have the supply for XiR, it's a focus of ours.

**Operator** (Operator):
Our next question comes from the line of Adam Maeder with Piper Sandler.

**Adam Maeder** (Analysts):
I wanted to ask about EUP 2.0 and specifically one of the offsets -- potential offsets force sensing instruments. And if I heard correctly, it doesn't sound like there's any offset assumed in the 300 to 500 basis point headwind for these. So I would love just any update on force sensing instrumentation. Where is adoption today? What percentage of procedures are being done with force sensing? And how do you think it could evolve over time? And would also just appreciate any color in terms of kind of primary use cases for the force sensing technology.

**David Rosa** (Executives):
Adam, I appreciate the question. Maybe I'll start with a quick story that just happened. And so a few weeks ago, we hosted the surgeon event here where the early surgeons that were involved with da Vinci came to our campus and we had a nice event. I had the opportunity to meet with a very well-versed prostatectomy surgeon who has done over 10,000 cases. And he showed me his results that were a comparator between Xi and da Vinci 5. And he was showing the return of potency in this case from time 0 through 12 months. 
And so -- and you watch it gradually increase from about 50% or so out of the gate to above about 80%. And he has very good data. He's one of the world's leading surgeons. And then he laid his recent da Vinci 5 experience on top of it and had moved the entire curve up by about 10 points. And so -- and I asked him why, and he attributed that to Force Feedback and the ability to sense those forces and be that much gentler around the nerve-sparing portion of the prostatectomy, which led to those results. And so that's maybe a little bit of color about how Force Feedback can make a difference in outcomes and even with surgeons who are very, very high up in their use of da Vinci.

**Jamie Samath** (Executives):
In terms of adoption, this quarter, about 8% of da Vinci 5 cases involve Force Feedback. That's kind of been kind of a slow increase from where we've started. We only got full, full supply later in the quarter, so that affected the 8%. I would say this, our ambitions are for that number to be -- that penetration number to be quite a bit higher. Obviously, to some extent, that requires us to create the evidence that supports the value propositions. The teams are working hard on that, and we have our eye very close in terms of how that gets adopted and the actual value of using the Force Feedback instruments is well understood. 
I would just say there are other offsets as we described, the SP I&A per procedure is quite a bit higher than multi-port. And obviously, those procedures are growing at a much higher rate. And on da Vinci 5, because of the integrated insufflation -- when integrated insufflation is used, which is about 85% of the time, there's an additional about $100 per procedure for the tube sets that connect to the insufflator. So those 3 can drive offsets in terms of the 3% to 5%, and they generally would be expected to grow at a faster pace than the base I&A.

**Operator** (Operator):
Our next question comes from the line of Jayson Bedford with Raymond James & Associates.

**Jayson Bedford** (Analysts):
Maybe just for Jamie. On the EUP, how long will it take you to fully implement the program, meaning when do you expect to see the 3% to 5% gross impact on revenue per procedure? And is there any way to kind of frame the expected impact in '27?

**Jamie Samath** (Executives):
Yes. It will be country by country. The first is the U.S. As I said, that submission is in process. So we'd expect to start to roll that out sometime later in Q1, depending on obviously when we get clearance. Europe, it would be next, and that's not until the second half of '27. And then some of the other markets just before or just after that. So I don't think we get to the full impact until the end of the year, frankly.

**Operator** (Operator):
Our next question comes from the line of Matt Taylor with Jefferies.

**Matthew Taylor** (Analysts):
I did want to follow up on the settlement that you talked about today. You mentioned onetime, no fault and just provide some certainty for your customers. I guess just wondering what this practically means for your customers and how they move on from that. And if you could just talk about remanufacturing in general and whether that's been any kind of real headwind.

**David Rosa** (Executives):
Yes, sure. Maybe I'll start and Gary will please weigh in. So this settlement really is an agreement with our customers, specifically regarding third-party instrument remanufacturers and third-party service providers. And I think the important part here is that it provides a clear framework on how we'll continue to work together in those 2 specific areas. And it lets us focus on really the things that are important. So advancing the safety, quality and security of our products for surgeons, care teams and their patients. And so we believe that this certainty that it provides allows us to move forward and really focus on building value with our customers.

**Gary Loeb** (Executives):
Yes. Just to add briefly, I think the resolution really strengthens our customer relationships, and it just provides a defined framework for how we work together on instruments and servicing.

**Operator** (Operator):
Our next question comes from the line of Chris Pasquale with Barclays.

**Chris Pasquale** (Analysts):
I want to ask about margins. You guys have done a great job improving profitability over the past few years. This quarter was better than expected. Street is modeling operating margin flat next year. So while I appreciate you don't really want to get into '27 in detail right now, you talked about offsetting the gross margin headwind from extended use. Are there any other considerations that we should take into account as we think about profitability and your ability to continue to expand margins here going forward?

**Jamie Samath** (Executives):
Yes. I think what we've said for some time now is kind of the range of where we'd expect to be on operating margin is between 35% and 40%. And I think that's, frankly, best-in-class in MedTech. As we think about it from a strategy perspective, our lean is to invest, invest in areas where we can innovate and bring differentiated capability to our customers and their patients, but also to support investments that allow us to grow at accelerated rates so that we can, again, serve more patients. And where we are right now, 41%, 42%, we have the capacity to invest. And so as we finish our planning process, then we'll evaluate that carefully. I'm not ready to say what we'll do on operating expenses. But certainly, if there are opportunities for us to do what I just described, then we'll use that capacity to invest. We'll provide that guidance, obviously, in January.

**David Rosa** (Executives):
Okay. That was our last question. Thank you for the questions. In closing, we continue to believe there's a substantial and durable opportunity to fundamentally improve surgery and acute interventions. Our teams continue to work closely with hospitals, physicians and care teams in pursuit of what our customers have termed the Quintuple Aim: Better, more predictable patient outcomes, better experiences for patients, better experiences for their care teams, lower total cost of care and finally, increased access to care.
We believe value creation in surgery and acute care is foundationally human. It flows from respect for and understanding of patients and care teams and their needs and their environment. At Intuitive, we envision a future of care that is less invasive and profoundly better where diseases are identified earlier and treated quickly so patients can get back to what matters most.
Thank you for your support on this extraordinary journey. We look forward to talking with you again in 3 months.

**Operator** (Operator):
Ladies and gentlemen, that concludes today's conference call. Thank you for your participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ISRG_Q2_2026_Earnings_Call_20260716.md
- 2026-07-16｜Daniel Connally (IR)｜guidance：全年 da Vinci 程序量成長財測區間維持 13.5%–15.5%（原話："within a range of 13.5% to 15.5%"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：程序量預期落在區間中點附近（原話："with an expectation to be closer to the midpoint"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：非 GAAP 毛利率財測由 67.5–68.5% 上調至 68–69%（原話："to be within a range of 68% to 69% of revenue"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：前次毛利率財測含關稅約 100 bps 影響（原話："which reflected 100 basis points of impact from tariff"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：非 GAAP 營業費用成長財測 11%–13%（原話："operating expense growth to be between 11% and 13%"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：下半年 Q3 美國基期較高，國際有假期季節移動（原話："bit of a tougher comp in the U.S. in Q3"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：Q2 毛利率含 IEEPA 關稅退款 3600 萬美元（原話："Excluding the $36 million benefit from IEEPA tariff refunds"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：扣除退款後 Q2 非 GAAP 毛利率為 68.7%（原話："gross margin would have been 68.7%"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：Q2 非 GAAP 營業利益率 42%、EPS 年增 28%（原話："42%, and non-GAAP earnings per share increased 28%"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：R&D 成長刻意高於 SG&A（原話："We are intentionally growing R&D at a higher rate than SG&A"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：Q2 da Vinci I&A 每程序收入約 1,830 美元，去年 1,800（原話："increased to approximately $1,830 compared to $1,800"）
- 2026-07-16｜Jamie Samath (CFO)｜commitment：延長使用壽命器械計畫預計 2027 上半年推出（原話："Beginning in the first half of 2027, we plan to introduce"）
- 2026-07-16｜Jamie Samath (CFO)｜commitment：延長使用計畫定價與量化影響留待下次財報（原話："we'll provide additional quantification on our next"）
- 2026-07-16｜Jamie Samath (CFO)｜commitment：分析師問延長使用影響，管理層表示尚不量化（原話："not ready to quantify it yet"）
- 2026-07-16｜Jamie Samath (CFO)｜commitment：管理層形容延長使用影響為 2027 年逐步發生（原話："think of it as being a progressive"）
- 2026-07-16｜David Rosa (CEO)｜commitment：da Vinci 5 以固定節奏持續推更新（原話："this cadence that we've committed to"）
- 2026-07-16｜Daniel Connally (IR)｜commitment：2026 年不再對基金會捐款（Q4 2025 曾捐 7000 萬）（原話："made a $70 million multiyear contribution to the"）
- 2026-07-16｜David Rosa (CEO)｜product：Q2 推出 100 項計畫更新的第一階段（原話："100 planned updates to the da Vinci 5 platform"）
- 2026-07-16｜David Rosa (CEO)｜product：SP 程序量成長 61%（原話："SP procedures grew 61%"）
- 2026-07-16｜Jamie Samath (CFO)｜product：SP 吻合器在美國適用病例使用率近 60%（原話："it was used in nearly 60% of eligible cases"）
- 2026-07-16｜David Rosa (CEO)｜product：向 FDA 遞交 GI 軟式機器人內視鏡 510(k)（非商用）（原話："not ready today to describe kind of timing"）
- 2026-07-16｜David Rosa (CEO)｜product：GI 機器人時程與市場規模尚不揭露（原話："not ready today to describe kind of timing or size"）
- 2026-07-16｜David Rosa (CEO)｜product：Ion 程序量成長 36%（原話："Ion procedures increased 36% to 48,000"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：XiR 安裝基數約 130 台（原話："the installed base is something like 130 XiRs in the field"）
- 2026-07-16｜David Rosa (CEO)｜customer：CEO 預期 XiR 將成為未來數季裝機的重要部分（原話："the installed base is something like 130 XiRs"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：首批 My Intuitive+ 續約客戶無人退出（原話："customer chose to opt out of their MI+ arrangement"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：海外良性程序占國際業務略逾 25%（原話："just over 25% of our international business"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：ACA 補貼到期對美國 da Vinci 程序量有輕微不利影響（原話："modest adverse impact to Q2 U.S. da Vinci procedure growth"）
- 2026-07-16｜David Rosa (CEO)｜risk：美國成長較年初預期放緩，集中在可延後程序（原話："Growth in the U.S. moderated from recent trends"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：CFO 稱部分放緩源自基期變大（原話："a little bit of the law of large numbers"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：減重手術受 GLP-1 影響持續下滑（原話："Growth in the U.S. moderated from recent trends"）
- 2026-07-16｜Daniel Connally (IR)｜risk：財測區間納入中國招標量與競爭強度（原話："China tender volumes and competitive intensity"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：管理層對日本新給付態度為平衡（原話："we're balanced about the continuing financial challenges"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：暴露於交易所／Medicaid 的程序占比無精確估計（原話："We don't have a precise estimate"）
- 2026-07-16｜David Rosa (CEO)｜competition：中國環境持續具挑戰性（原話："the environment remains challenging"）
- 2026-07-16｜David Rosa (CEO)｜competition：中國本土機器人競爭與政策性價格壓力（原話："domestic robotic competition and policy-driven pricing"）
- 2026-07-16｜Jamie Samath (CFO)｜competition：Q2 中國僅裝 2 台，含香港首台 da Vinci 5（原話："placing 2 systems, including our first da Vinci 5"）
- 2026-07-16｜Jamie Samath (CFO)｜competition：經銷商市場相對強勢（原話："relative strength in distributor markets"）
- 2026-07-16｜David Rosa (CEO)｜competition：管理層不認為中國集中招標等同 VBP（原話："I wouldn't compare this tender centralization"）
- 2026-07-16｜David Rosa (CEO)｜competition：器械加密技術被問及是否抵擋再製器械，答以網路安全（原話："cybersecurity is front and center"）
- 2026-07-16｜Jamie Samath (CFO)｜capital_allocation：Q2 回購 3.79 億美元，均價 439 美元（原話："stock repurchases of $379 million at an average price"）
- 2026-07-16｜Jamie Samath (CFO)｜capital_allocation：2026 上半年自由現金流 18 億美元，年增 71%（原話："Free cash flow in the first half of 2026 was $1.8 billion"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：美國資本環境穩定（原話："The U.S. capital environment, at least in our experience"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：美國約 70% 系統採租賃（原話："70-ish percent of the systems acquired in the U.S."）
- 2026-07-16｜Jamie Samath (CFO)｜customer：美國裝機增量幾乎全來自換機（原話："the entirety of that increase is in trades"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：美國約半數裝機為換機（原話："half of the placements in the U.S. in Q2 were trades"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：以 Si→Xi 歷史類比 dV5 換機週期（原話："it took about 7 years before we got to the peak"）

### 問答異常語氣（迴避／改口／保留）
- ISRG_Q2_2026_Earnings_Call_20260716.md｜問：Travis Steed／Michael Polark：延長使用計畫對 I&A 每程序收入的量化影響（約 5 點？2027 持平或下降？）｜答法：兩次皆不給數字，僅稱下次財測會量化、需先走完內部分析；改談成長與獲利平衡及 mix 抵銷
- ISRG_Q2_2026_Earnings_Call_20260716.md｜問：Larry Biegelsen：器械加密是否促使醫院不改用再製器械｜答法：未正面回答再製器械問題，改談網路安全與產品品質、可用性
- ISRG_Q2_2026_Earnings_Call_20260716.md｜問：Vijay Kumar：程序對交易所與 Medicaid 的暴露程度｜答法：先請對方重述問題，後答無精確估計，只說商保占大部分
- ISRG_Q2_2026_Earnings_Call_20260716.md｜問：Rick Wise：GI 機器人的時機與潛在 TAM｜答法：稱仍早期，不給時程與市場規模

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
{"date":"20260717","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"裝機基數 ＋ ~85% 經常性耗材年金鎖住 83-85% 軟組織份額，且年金的單位經濟不被侵蝕前次僅要求份額；本次因 EUP 與售後市場訴訟同現，加入單位經濟這一半——份額守住但每台收入被砍，H1 一樣不成立"},{"id":"H2","text":"Ion／SP／心臟／NSM／國際 benign／ASC 通路接棒，維持整體雙位數手術量成長"},{"id":"H3","text":"市場願給高成長醫材上緣的倍數溢價。本次重寫：前次「長期 Fwd PE 38-48x」已被市場實付 34.45x(FY26)／30.47x(FY27) 直接否決（§12 矛盾 #1）。重寫後 ＝ 28-34x（Fwd FY2 口徑，相對高成長醫材同業 ~28x 約 0-20% 溢價）——不是回到 38-48x"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"EUP ＋ XiR／翻新機低價組合 ＋ GLP-1，三者同向侵蝕 I&amp;A 每台手術收入。EUP 於 2027 上半年上線、量級管理層兩次拒答（BofA 估 ~5pt、Wolfe 援引 2020 先例 ~7pt）；XiR（裝機 ~130 台）與翻新 Xi／X（Q2 共 122 台 vs 去年 59 台）把組合往低單價拉；美國 bariatric 因 GLP-1 高個位數下滑、膽囊切除等低單價術式佔比上升"},{"id":"R2","text":"手術量結構性降檔 ＋ 政策給付逆風，倍數向成熟醫材 22-26x 收斂。美國 da Vinci 自 Q1 +14% 降至 Q2 +12%；上半年 ~15% → 全年「靠近中點」14.5% → 下半年隱含 ~14%；管理層自承「大數法則」。疊加政策：ACA 增強版補貼已於 2026-01-01 到期且未見續延，非單季雜訊而是延續至 2026-27 的結構性逆風，且與 GLP-1 對 bariatric 的衝擊同方向疊加"},{"id":"R3","text":"EndoWrist 售後市場的法律可分割性 ＋ 競品在新興市場的價格戰。① 醫院買方反壟斷集體訴訟已於 2025-03-31 獲裁准 class certification，核心指控＝以程式化使用次數限制強迫回購 EndoWrist、禁止第三方維修；SIS v. Intuitive 一案 ISRG 雖於 2025-01-28 獲法官於陪審團審判中途作出有利之 JMOL（援引 Epic v. Apple 第九巡迴 2023 先例，認未能證明售後市場存在），但現上訴於第九巡迴（Open Markets Institute 已提 amicus）；法院曾於較早之即決判決認定 da Vinci 機器與 EndoWrist 為獨立產品市場且 ISRG 於售後市場具獨占力，惟已於 2024-07-30 准重新審議而撤銷——此爭點法院曾兩度改變見解，屬真正未定。② MicroPort Toumai 累計 300+ 全球訂單、覆蓋 60+ 國家（印度 30+ 台、巴西／阿根廷各近 20 台），定價約低 30%，主攻的正是 H2 所倚賴的國際低滲透市場"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"PEG（FY26 基準）≤ 2.0。今日解＝股價 ≤ $348；或 FY26 共識 EPS 上修至 ≥ $10.75 而價不變。無附加條件。","irr_base_pct":10.8,"ev5y_pct":47.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"❌","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.5,"ev5y_pct":47.9,"irr_base_pct":10.8,"max_dd_pct":-45.0,"bull_5y_price":770.0,"bear_5y_price":280.0,"p_bull_pct":22.0,"p_bear_pct":33.0,"rearm_trigger":"PEG（FY26 基準）≤ 2.0。今日解＝股價 ≤ $348；或 FY26 共識 EPS 上修至 ≥ $10.75 而價不變。無附加條件。","price_at_dd":358.97,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
