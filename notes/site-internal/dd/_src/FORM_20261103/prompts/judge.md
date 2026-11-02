你是 stock-analyst **v20 判斷 agent**，標的 FORM（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"FORM","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":280.5,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm"},"note":"高於公司自家指引上緣：Q3 指引 260–280（逐字稿）；外部共識未取得"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":94.1,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","unit":"USD million（margin 33.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":81.6,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","unit":"USD million（margin 29.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm"}},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":64.8,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","unit":"USD million（占營收 23.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm"}},{"id":"f_kpi5_guidance_q4_fy2026_reven","label":"Guidance Q4 FY2026 revenue","value":285,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","unit":"USD million（±10，區間 275–295）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm"}},{"id":"f_kpi6_non_gaap_gross_margin","label":"Non-GAAP gross margin","value":56.5,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm；基線說明見 Q3 法說會逐字稿"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_form_gross_margin_pct","label":"FORM 毛利率","value":44.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FORM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_form_operating_margin_pct","label":"FORM 營業利益率","value":15.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FORM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_form_fcf_margin_pct","label":"FORM FCF 利潤率","value":16.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FORM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ter_gross_margin_pct","label":"TER 毛利率","value":59.41,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TER.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ter_operating_margin_pct","label":"TER 營業利益率","value":33.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TER.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ter_fcf_margin_pct","label":"TER FCF 利潤率","value":21.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TER.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_6857_t_gross_margin_pct","label":"6857.T 毛利率","value":65.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6857.T.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6857_t_operating_margin_pct","label":"6857.T 營業利益率","value":45.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6857.T.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6857_t_fcf_margin_pct","label":"6857.T FCF 利潤率","value":31.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6857.T.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6223_two_gross_margin_pct","label":"6223.TWO 毛利率","value":56.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6223.TWO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6223_two_operating_margin_pct","label":"6223.TWO 營業利益率","value":30.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6223.TWO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6223_two_fcf_margin_pct","label":"6223.TWO FCF 利潤率","value":-11.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6223.TWO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohu_gross_margin_pct","label":"COHU 毛利率","value":43.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHU.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohu_operating_margin_pct","label":"COHU 營業利益率","value":-6.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHU.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohu_fcf_margin_pct","label":"COHU FCF 利潤率","value":6.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHU.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_stock_based_compensa","label":"SBC (stock-based compensation)","value":8.8,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","unit":"USD million（占 GAAP 營業利益 10.8%；占營收 3.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":90.01,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-33.01,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":35.46,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":9.84,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.05 → 3.35）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":9.84,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.86 → 4.24）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":4.07,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.65 → 5.88）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.35,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":4.24,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":5.88,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":37.3,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 2.44 → 3.35（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":41.29,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝10.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":10.9,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":7.17,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":26.87,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.35，分子＝快照價 90.01","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-367.65,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 27.76、現金 395.41（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":78.12,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":6664.0,"period":"2026-11-03","unit":"USD m","basis":"市值 7031.65 ＋ 淨負債 -367.65","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":1047.97,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（10 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":1301.29,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.36,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 89.7 / W52 103.01 / W104 69.3 / W250 50.58 / W250 13週斜率 1.67%"},{"id":"f_ma_w52","label":"52 週均線","value":103.01,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":69.3,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":50.58,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.67,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出探針卡主要對手含 Technoprobe、JEM、MPI、MJC 等；探針卡市場歷來分散；公司承認競爭加劇已導致或可能導致降價、毛利下降或失去市占。","source":"SEC EDGAR 10-K FY2025 Item 1 / 1A","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"We have experienced increased competition in the markets in which we operate, and we expect competition to intensify in the future. Increased competition has resulted in, and in the future may result in, price reductions, reduced gross margins or loss of market share.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 點名探針卡主要競爭者名單（含 Technoprobe S.p.A、MPI、STAr 等）。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"Our primary competitors are Japan Electronic Materials Corporation, Korea Instrument Co., Ltd., Micronics Japan Co., Ltd., MPI Corporation, STAr Technologies, Inc., Max One, Technoprobe S.p.A, TSE Co., Ltd., among others.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"TrendForce 2026-06 報告：Technoprobe 有望超越 FormFactor 成為全球探針卡第一供應商。","source":"TrendForce, Probe Card Tech Upgrade & Market Reshaped by AI Packaging-Part 2","url":"https://www.trendforce.com/research/download/RP260626XO3","excerpt":"Market Outlook: Total revenue is forecast to surge sharply in 2026, with Technoprobe poised to overtake FormFactor as the top global supplier. Table of Contents","as_of":"2026-06-26","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Deutsche Bank 首度納入研究，稱 FORM 為 Nvidia 關鍵供應商，Technoprobe 亦為 Nvidia 測試供應商。","source":"TechNews 2026-10-01","url":"https://finance.technews.tw/2026/10/01/deutsche-bank-bullish-on-formfactor-shares-surge/","excerpt":"已躍居輝達（NVIDIA）關鍵供應商，未來可望搶下更多晶片測試市場。 綜合外媒報導，德銀分析師布朗（George Brown）在最新報告中給予 FormFactor 買進評等，目標價設定為200美元，看好該公司已鞏固做為輝達GPU探針卡第二大供應商的地位；輝達GPU是由台積電製造。 布朗看好，與輝達的合作可望讓FormFactor接觸規模達5億美元的潛在市場，相當於該公司目前整體晶片測試設備業務的全年營收。 布朗指出，FormFactor對輝達的相關銷售預料於今年7月至12月間開始，至2028年可望取得最高20%的晶片測試市場，額外創造2億美元年營收。 FormFactor股價9月30日大漲9.59%，收149.31美元，年初迄今已大漲167%。 德銀並未在報告中說明目前排名第一的供應商；高盛先前曾指出，FormFactor主要競爭對手、義大利探針卡巨頭特諾本（Technoprobe）也是","as_of":"2026-10-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 財報電話會議：CEO 稱已獲第二個設計案，延續先前合格認證與首個設計勝出。","source":"MarketBeat FormFactor Q1 2026 Earnings Call Transcript","url":"https://www.marketbeat.com/earnings/reports/2026-4-29-formfactor-inc-stock/","excerpt":"Specifically, we've now been awarded a second design, building off our successful qualification and initial design win.","as_of":"2026-04-29","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Q2 2026 前三大客戶占營收35%，其中 SK Hynix 24%；去年同期為48%","source":"panabee FormFactor Q2 2026 摘要 / FormFactor 10-Q","url":"https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000033/form-20260627.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"SK hynix 占 FormFactor FY2025 營收 22.9%（FY2024 為 18.9%）；FY2024 兩大客戶合計 33.5%、FY2023 單一客戶 17.1%。","source":"SEC EDGAR 10-K FY2025 Item 1A/財報附註","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"A relatively small number of customers account for a significant portion of our revenues. One customer represented 22.9% of total revenues in fiscal 2025, two customers represented a combined 33.5% of total revenues in fiscal 2024 and one customer represented 17.1% of total revenues in fiscal 2023.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"SK hynix 單季占比 FY2025 Q1–Q4 為 23.3%、25.0%、24.5%、19.2%；期末應收帳款 FY2025 兩家客戶占 15.8% 與 10.8%，公司通常不要求擔保品。","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"At December 27, 2025, two customers accounted for 15.8% and 10.8% of gross accounts receivable. At December 28, 2024, one customer accounted for 22.0% of gross accounts receivable.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"客戶自身信用：Moody's 於 2026-08-03 將 SK hynix 由 Baa1 升至 A3（展望穩定）；Fitch 2026-04-30 升至 BBB+；S&P 2026-02-05 升至 BBB+（展望正向），另有報導稱 S&P 後續升至 A-（日期未證實）。未見信用惡化。","source":"WebSearch 彙整（Moody's/S&P/Fitch 升評報導，如 smarttoday、newsquawk、asiae）","url":"https://www.smarttoday.co.kr/ko-kr/articles/110067","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"第三方報導稱 Q1 2026 SK hynix 占 FormFactor 營收 29.5%（去年同期 23.3%），NVIDIA 首次列為 10%+ 客戶（10.2%）；未經一手文件核實。","source":"PhotonCap「formfactors july 29th」","url":"https://photoncap.net/p/formfactors-july-29th","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 2026年中預測：全球半導體設備銷售2026年1659億美元，2028年達2295億美元，連續第五年成長；測試設備2027年+18.1%、2028年+13.6%至1047億美元；DRAM設備2027年+27.4%、2028年+15.0%。","source":"SEMI press release: Global Semiconductor Equipment Sales Forecast to Reach a Record $229 Billion in 2028","url":"https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-dollars-in-2028-semi-reports","excerpt":null,"as_of":"2026-07-14","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TrendForce報導：美光認為記憶體供給緊到FY28，新產能約2028年才開出，2028為新產能轉折點但釋放將漸進；ASML低NA EUV 2027產能幾乎訂滿，計畫增產約30%。","source":"TrendForce News 2026-08-19 chip equipment crunch lead times 24 months","url":"https://www.trendforce.com/news/2026/08/19/news-chip-equipment-crunch-reportedly-pushes-lead-times-to-24-months-giving-chinas-toolmakers-a-boost/","excerpt":null,"as_of":"2026-08-19","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FormFactor 2026Q1創連續第二季營收歷史新高，DRAM/HBM與foundry/logic探針卡成長；Q2指引2.40億美元±500萬。","source":"FormFactor, Inc. Reports 2026 First Quarter Results","url":"https://investors.formfactor.com/news-releases/news-release-details/formfactor-inc-reports-2026-first-quarter-results","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"評論指測試需求具週期性，當前強勢集中在AI/HBM與CPO，業績對產品組合變化敏感；另有出口管制、關稅、AI支出持續性不確定。","source":"Barchart: FormFactor's Semiconductor Test Business Confronts the Post-Boom Reality Tomorrow","url":"https://www.barchart.com/story/news/3511514/formfactor-s-semiconductor-test-business-confronts-the-post-boom-reality-tomorrow","excerpt":null,"as_of":"2026-04-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 對中國客戶銷售占營收 7%（FY2024 為 14%），中國為受美國擴大出口許可要求影響的地區之一。","source":"SEC EDGAR 10-K FY2025, Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"approximately 7% of our fiscal 2025 revenue and 14% of our fiscal 2024 revenue was derived from sales to customers in China, which was one of the regions subject to the expanded export license requirements imposed by the United States government.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 關稅成本使毛利率受 1.4 個百分點衝擊，探針卡毛利率下降部分因關稅成本增加；下半年毛利率較上半年明顯改善。","source":"SEC EDGAR 10-K FY2025, Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"gross margins decreased as a result of greater revenues and a favorable product mix, that was offset by higher manufacturing costs, which included a 1.4% gross margin impact from increased costs for tariffs. Despite the impact of tariffs, third and fourth quarters of fiscal 2025 have shown meaningful improvement in gross margins compared to the first half of fiscal 2025 and second half of fiscal 2024.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：部分零組件來自單一或有限供應商，加徵關稅與貿易壁壘可能加劇供應風險；並提及美中出口管制與貿易緊張可能影響中國市場業務。","source":"SEC EDGAR 10-K FY2025, Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"escalating trade tensions and policy divergence between the U.S. and China, including restrictions on technology transfers, cross-border data transfers, export controls, and investment limitations, could impact our ability to conduct business, access critical technologies, or operate effectively in the Chinese market.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋 Section 232 半導體關稅與 2026 年中美實體清單新聞，結果均未提及 FormFactor；Section 232 25% 關稅僅針對窄範圍先進晶片，2026-01-15 生效。","source":"White & Case / Thomson Reuters 搜尋摘要（未見 FormFactor 專屬內容）","url":"https://www.whitecase.com/insight-alert/president-trump-orders-narrowly-targeted-25-section-232-tariff-certain-advanced","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FormFactor 10-K 風險因素：依賴單一或有限來源供應商，多數供應商僅採採購單而非長約，單一來源供應商可能漲價拖累毛利","source":"FormFactor 10-K FY2022 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939923000010/form-20221231.htm","excerpt":"Because we rely on purchase orders rather than long-term contracts with the majority of our suppliers, we cannot guarantee our ability to obtain components and materials in the long term. A sole or limited source supplier could increase prices, which could lead to a decline in our gross profit.","as_of":"2023-02-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"某第三方 PESTLE 分析稱 FormFactor 於 2025 年 11 月宣布在德州 Farmers Branch 投資新先進製造廠，定位為回岸（二手聚合來源，未核公司揭露）","source":"dcf-analysis.com FORM PESTLE","url":"https://dcf-analysis.com/products/form-pestel-analysis","excerpt":"FormFactor is aligning its growth with this federal push by investing in a new advanced manufacturing facility in Farmers Branch, Texas. This project, announced in November 2025, is a strategic bet on reshoring.","as_of":"2026-04-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 將供應商中斷連結到關稅與貿易壁壘、區域緊張","source":"FormFactor 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"This could be exacerbated by certain events outside the control of either the supplier or us, such as global, regional or national health crises, armed conflicts, increased tariffs and trade barriers, regional tensions or other adverse global, regional and national events.","as_of":"2026-02-25","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FormFactor Q2 2026 DRAM probe card revenue was a record, HBM about two-thirds of DRAM; management guided Q3 DRAM revenue roughly comparable to Q2 record with mix shifting materially toward DDR.","source":"MarketBeat, FormFactor Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/formfactor-q2-earnings-call-highlights-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q1 2026 call: management expected continued growth in foundry & logic probe card revenue, driven mainly by data center CPU, plus strong networking and steady PC/mobile; Q2 2026 summary describes continued foundry & logic growth from broad incremental demand.","source":"MarketBeat, FormFactor Q1 2026 Earnings Call Transcript","url":"https://www.marketbeat.com/earnings/reports/2026-4-29-formfactor-inc-stock/","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"TrendForce June 2026 report: FormFactor, Technoprobe and MJC dominate probe cards; Taiwan's CHPT, MPI and WinWay gaining share on AI wave; Technoprobe could overtake FormFactor as top global supplier in 2026.","source":"TrendForce, Probe Card Tech Upgrade & Market Reshaped by AI Packaging-Part 2","url":"https://www.trendforce.com/research/download/RP260626XO3","excerpt":null,"as_of":"2026-06-26","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Systems segment revenue reached a record $48.5M, up 74% from Q1 (per aggregator; period label unclear, likely Q2 2026).","source":"Aggregator snippet via search (unverified period)","url":"https://www.marketbeat.com/instant-alerts/formfactor-q2-earnings-call-highlights-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"SEMI Mid-Year 2026 forecast: total equipment sales $165.9B in 2026 (+23.2%), WFE $143.9B (+23.1%), record $229.5B by 2028.","source":"SEMI press release / Communications Today","url":"https://www.communicationstoday.co.in/global-chip-equipment-market-to-hit-165-9b-in-2026-semi/","excerpt":"manufacturers (OEMs) are forecast to reach a record high of $165.9 billion in 2026, increasing 23.2% year-on-year, SEMI announced today in its Mid-Year Total Semiconductor Equipment Forecast – OEM Perspective. Growth momentum is expected to continue through 2028, with total equipment sales forecast to reach a record $229.5 billion, marking five consecutive years of growth as AI-driven","as_of":"2026-07-15","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"SEMI Dec 2025 year-end forecast (superseded): $145B in 2026, $156B in 2027.","source":"SEMI press release","url":"https://semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports","excerpt":null,"as_of":"2025-12-16","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 列出的探針卡競爭者皆為同類探針卡廠（JEM、Korea Instrument、MJC、MPI、STAr、Max One、Technoprobe、TSE 等），未在競爭段列出非探針卡的替代技術","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"Our primary competitors are Japan Electronic Materials Corporation, Korea Instrument Co., Ltd., Micronics Japan Co., Ltd., MPI Corporation, STAr Technologies, Inc., Max One, Technoprobe S.p.A, TSE Co., Ltd., among others.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子承認客戶需求隨 AI 相關產品快速變化、技術變遷快，且他人可能獨立開發類似或競爭技術或繞過專利設計","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"Others might independently develop similar or competing technologies or methods or design around our patents.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"TrendForce 2026-06 報告：MEMS 已成探針卡主流製程，專有針尖合金為關鍵差異化；Advantest、Teradyne 入股 Technoprobe、FormFactor、MJC","source":"TrendForce Probe Card Tech Upgrade & Market Reshaped by AI Packaging-Part 1","url":"https://www.trendforce.com/research/download/RP260623JC3","excerpt":"Market Consolidation: Advantest and Teradyne have taken stakes in Technoprobe, FormFactor, and MJC, signaling accelerated vertical integration ahead. Table of Contents Introduction MEMS Processes Take Center Stage: Probe Tip Material Compositions Become the Core Technology","as_of":"2026-06-23","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"+","claim":"FormFactor 稱 HBM 由 1,024 增至 4,096 I/O、16-Hi/20-Hi 堆疊、>10 Gbps，晶圓測試複雜度大增，以 SmartMatrix 與垂直 MEMS 測試卡因應","source":"Silicon Saxony: FormFactor Beyond Bandwidth","url":"https://silicon-saxony.de/en/formfactor-beyond-bandwidth-how-genai-is-reshaping-hbm-architecture-and-semiconductor-testing/","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 描述通路為全球直銷團隊加上製造商代表與經銷商；經銷商用於特定地區因當地法規或商業慣例，未見通路結構性轉變的記載。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm","excerpt":"We sell our products worldwide through a global direct sales force and through a combination of manufacturers’ representatives and distributors.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-29 公司將 Q3 2026 guidance 上調：EPS $0.77–$0.95、營收 $260–$280M，高於當時分析師預期 EPS $0.60、營收 $246.2M（guidance 高於共識）。","source":"MarketBeat / Northland estimate article via search summary","url":"https://www.marketbeat.com/instant-alerts/formfactor-nasdaqform-updates-q3-2026-earnings-guidance-2026-07-29/","excerpt":"FormFactor raised its Q3 2026 guidance to EPS of $0.77–$0.95 and revenue of $260 million–$280 million, both above analysts' estimates of $0.60 EPS and $246.2 million in revenue.","as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Northland 於 2026-07-30 前後把 Q3 2026 EPS 預估由 $0.55 上修至 $0.78（高於 guidance 中點），FY2026 EPS $2.70、FY2027 $2.76。","source":"MarketBeat: Northland Securities estimates FormFactor Q3 earnings","url":"https://www.marketbeat.com/instant-alerts/northland-securities-estimates-formfactor-q3-earnings-2026-08-05/","excerpt":"Northland Securities raised FormFactor's Q3 2026 earnings estimate to $0.78 per share from $0.55, above the company's guidance range midpoint. The firm projects $2.70 EPS for fiscal 2026 and $2.76 for fiscal 2027.","as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill 顯示 FY2026 EPS 共識最新紀錄 3.12（13 位分析師，2026-10-18）；Q3 預估 EPS 0.88、營收約 275.9M，Q3 財報預定 10/28。","source":"Chartmill FORM estimates page","url":"https://www.chartmill.com/stock/quote/FORM/estimates","excerpt":"Latest recorded estimate: 3.12 USD · Oct 18, 2026 · 13 analysts","as_of":"2026-10-18","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Fintel 最新紀錄（2026-10-02）一年期平均目標價 $145.55，區間 64.64–210.00，中位數 160.65；Investing.com 平均 144.67、高 175、低 64。","source":"Fintel FORM page; Investing.com FormFactor","url":"https://fintel.io/s/us/FORM","excerpt":null,"as_of":"2026-10-02","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 2026-07 下旬：11 家券商共識 Moderate Buy（6 買 5 持有），12 個月平均目標價 $132.45；3 月時平均為 $80.91、2 月 TIKR 為約 $71，目標價年內大幅上移。","source":"MarketBeat consensus rating article 2026-07-27","url":"https://www.marketbeat.com/instant-alerts/formfactor-inc-nasdaqform-receives-consensus-rating-of-moderate-buy-from-brokerages-2026-07-27/","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Seeking Alpha 修正頁：EPS 下修 0 次、營收上修 9 次、下修 0 次（上修趨勢）。","source":"Seeking Alpha FORM earnings revisions","url":"https://seekingalpha.com/symbol/FORM/earnings/revisions","excerpt":"Revenue # of Up Revisions 9 Revenue # of Down Revisions 0","as_of":"2026-10-18","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#6","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 2026-10-28 發布 Q3 2026 結果，CEO 稱營收、毛利率、EPS 成長超出 guidance 高標；搜尋未取得 Q4 outlook 數字。","source":"FormFactor, Inc. Reports 2026 Third Quarter Results (Seeking Alpha PR)","url":"https://seekingalpha.com/pr/20704290","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-01-09 8-K 揭露重整計畫（Item 2.05）與重大減損（Item 2.06）；搜尋摘要稱預計重整費用約 $30–40M，整併 Carlsbad 與 Baldwin Park 製造廠，多數費用落在 FY2026。","source":"SEC EDGAR 8-K（2026-01-09）Item 2.06","url":"https://www.sec.gov/Archives/edgar/data/1039399/000103939926000002/form-20260105.htm","excerpt":"Item 2.06. Material Impairments.\nThe disclosure under Item 2.05 is incorporated by reference into this Item 2.06.","as_of":"2026-01-09","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共 8 份，僅 1 份含重大項目（2026-01-09 的 2.05/2.06），其餘為財報、董事異動、股東會等。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001039399&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單中無 Item 4.02（財報不可依賴）；僅 1 份重大項目為 2.05/2.06。搜尋未見 SEC 調查，重編僅見 2004、2007 年舊案。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001039399&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"FORM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.1,"operating_margin_pct":15.95,"fcf_margin_pct":16.67,"rd_intensity_pct":13.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FORM","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"TER","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":59.41,"operating_margin_pct":33.17,"fcf_margin_pct":21.59,"rd_intensity_pct":11.78},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TER","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"6857.T","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.73,"operating_margin_pct":45.86,"fcf_margin_pct":31.21,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6857.T","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"6223.TWO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.52,"operating_margin_pct":30.26,"fcf_margin_pct":-11.23,"rd_intensity_pct":8.45},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6223.TWO","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"COHU","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.95,"operating_margin_pct":-6.19,"fcf_margin_pct":6.68,"rd_intensity_pct":18.6},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHU","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"FORM"},"financial_history":{"ticker":"FORM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":747937000.0,"revenue_yoy_pct":null,"gross_margin_pct":39.58,"operating_margin_pct":7.34,"net_income":50738000.0,"diluted_eps":0.65,"free_cash_flow":66532000.0,"fcf_margin_pct":8.9,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":663102000.0,"revenue_yoy_pct":-11.34,"gross_margin_pct":39.0,"operating_margin_pct":1.48,"net_income":82387000.0,"diluted_eps":1.05,"free_cash_flow":8575000.0,"fcf_margin_pct":1.29,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":763599000.0,"revenue_yoy_pct":15.16,"gross_margin_pct":40.33,"operating_margin_pct":5.79,"net_income":69614000.0,"diluted_eps":0.89,"free_cash_flow":79098000.0,"fcf_margin_pct":10.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":784993000.0,"revenue_yoy_pct":2.8,"gross_margin_pct":39.34,"operating_margin_pct":7.66,"net_income":54361000.0,"diluted_eps":0.69,"free_cash_flow":11740000.0,"fcf_margin_pct":1.5,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/FORM/FORM_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**FormFactor, Inc.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Thank you, and welcome, everyone, to FormFactor's Third Quarter 2026 Earnings Conference Call. On today's call are Chief Executive Officer, Mike Slessor, and Chief Financial Officer, Aric McKinnis. Before we begin, Stan Finkelstein, the company's VP of Investor Relations, will remind you of some important information.

**Stan Finkelstein** (Executives):
Thank you. Today, the company will be discussing GAAP P&L results and some important non-GAAP results intended to supplement your understanding of the company's financials. Reconciliations of GAAP to non-GAAP measures and other financial information are available in the press release issued today by the company and on the Investor Relations section of our website. Today's discussion contains forward-looking statements within the meaning of the federal securities laws.
Examples of such forward-looking statements include those with respect to the projections of financial and business performance, future macroeconomic and geopolitical conditions; the benefits of acquisitions and investments, including the ramp-up of manufacturing facilities, anticipated industry trends, potential disruptions in our supply chain; the impacts of regulatory changes, including tariffs and changes in export controls, the anticipated volatility in demand for products, our ability to develop, produce and sell products and the assumptions upon which such statements are based. 
These statements are subject to known and unknown risks and uncertainties that could cause actual results to differ materially from those expressed during this call. Information on risk factors and uncertainties is contained in our most recent filing on Form 10-K with the SEC for the fiscal year ended December 27, 2025, and in our other SEC filings, which are available on the SEC's website at www.sec.gov and in our press release issued today. Forward-looking statements are made as of today, October 28, 2026, and we assume no obligation to update them. With that, we will now turn the call over to FormFactor's CEO, Mike Slessor.

**Mike Slessor** (Executives):
Thanks for joining us today. During the third quarter, FormFactor again grew revenue, gross margin and earnings per share, with each metric exceeding the high end of our outlook range. These results continue a theme you've seen from us for the past year, namely broad-based growth in demand from our diversified leadership position at the intersection of high-performance compute and advanced packaging and our ability to serve this demand by producing more output from our existing manufacturing footprint. On a year-over-year basis, we grew quarterly revenue close to 40% within essentially the same manufacturing footprint.
Our fourth quarter outlook extends this trend. Although we are now reaching the limits of our ability to extract more output from our existing manufacturing footprint, we're also bringing our new Farmers Branch factory online. We recently qualified the assembly and test portion of this new facility and, only a few days ago, shipped the first production unit to a leading customer. We celebrated these milestones last week together with almost 200 customers, suppliers, partners, employees and government officials at a ribbon-cutting event that formally launched our nearly 300,000-square-foot facility.
Over the course of 2027, our top priority is the ramp-up of Farmers Branch. We'll ramp as quickly as we can while ensuring we both sustain the efficiency improvements we've demonstrated in the last year and maintain the market-leading product quality that is one of FormFactor's foundational competitive advantages. Aric will provide more details on the status and plans for Farmers Branch later in the call. Earlier this month, we announced the expansion of our long-standing partnership with Teradyne, one of the world's leading automated test equipment or ATE, suppliers. 
Together with our multiyear partnership with Advantest, this announcement formalizes the collaboration and partnership between FormFactor and both market-leading ATE suppliers. The goal of these collaborations is to speed up the development, validation and high-volume production of next-generation semiconductor applications, enabling high-performance compute like high-bandwidth memory and co-packaged optics. These partnerships also reinforce and solidify the open ecosystem market structure that provides our mutual customers with full probe card ATE interoperability, enabling customers to select the optimum probe card and ATE combination for their specific chip architectures and designs.
Turning now to segment and market details. Foundry and Logic was one of the key drivers of our third quarter growth, increasing 10% sequentially on the expected broad-based strength across multiple applications. We expect continued demand growth and breadth in the current fourth quarter. In this market, we're building on our established positions in PCs, mobile, data center CPUs and networking while adding new growth vectors like GPUs and hyperscaler custom ASICs. 
Specifically, during the third quarter, we shipped probe cards to the world's leading foundry for 1 single GPU design in multimillion-dollar volumes. Building on this successful qualification and initial ramp, we're well positioned to meaningfully grow share in this important part of the foundry and logic market in 2027, with Farmers Branch providing the required capacity. Looking ahead in foundry and logic, the accelerating trends of higher speed interfaces, greater power density and increasingly complex advanced packaging chiplet architectures for next-generation GPUs and custom ASICs are increasing probe card performance requirements. 
These higher performance requirements make FormFactor's advanced MEMS probe technology a requirement for cost-effective production test, and we're building the foundation to achieve share gains in 2027 across a diverse set of GPU and custom ASIC designs. Our exposure to multiple customers and applications provides us with several ways to participate in the growth of high-performance compute and shows the benefits of our diversification strategy, reducing reliance on any single customer, program or architecture to drive our revenue and growth.
Turning to DRAM probe cards. Third quarter revenue was, as expected, essentially unchanged from the record levels of the second quarter, but the mix shifted significantly. This mix shift was also expected with HBM revenue declining and DDR5 revenue increasing as our customers move their wafer start mix to more DDR designs to capture the profit opportunity provided by significant DDR market price increases. Since probe cards are specific to each customer chip design, our DRAM probe card mix tracks these dynamic customer product shifts, and we expect these quarter-to-quarter shifts between DDR and HBM to continue so long as the current bit-constrained DRAM market conditions persist.
Another important point related to this mix shift is that at the same time we achieved record DRAM probe card revenues with a DDR5 heavy and HBM light product mix, we delivered record gross margin performance. Compared to the FormFactor of years past, this is evidence of a very different profitability profile, demonstrating the impact of the successful execution of several DRAM probe card manufacturing cost reduction programs. The net result is improved DRAM probe card gross margins, which in turn lessen the dependence of our company level gross margins on product mix.
Turning now to our Systems segment. Systems delivered a record quarter, growing 20% sequentially on accelerating demand for our TRITON system for co-packaged optics or CPO, applications. This accelerating demand has been evident in the steady increase in our expectations for this business in 2026. We started the year expecting between $10 million and $20 million of TRITON revenue and now expect upwards of $30 million in 2026. In tandem with this growing CPO business, we're also serving demand for additional photonics applications such as CPO's close cousin near package optics or NPO as well as pluggable devices.
This beyond CPO application coverage is the result of our intentional focus on developing the world's leading optical probing technologies applicable across a wide range of photonics applications. In this case, we've prioritized building leadership in Test Insertion One, which ensures known good die or KGD, of the photonic integrated circuit or PIC. Both CPO and NPO architectures require KGD PICs before they are combined with the electronic ICs to form the optical module and scale up and scale out network switches. As a result, FormFactor benefits from broader photonics adoption, whether it be CPO or NPO.
Part of our leadership position in photonics probing stems from the acquisition of Keystone Photonics a year ago. As we've discussed, Keystone's innovative and differentiated optical probe technology enables high-efficiency optical coupling to our customers' photonic devices in much the same way our advanced MEMS probes provide best-in-class electrical connectivity to our customers' chips. To maximize our competitive advantage from this acquisition, we've made the decision to more tightly integrate the Keystone team and technologies into FormFactor with an exclusive focus on enhancing FormFactor's development and delivery of the world's leading photonics probing solutions.
We believe the exciting growth in CPO, NPO and pluggables represents the very early stages of widespread adoption of photonics in the broader semiconductor industry. Traditional copper interconnect is reaching physical limits in speed, heat and energy consumption and photonics provides a fundamentally more efficient way to transmit data within and between data centers using light instead of electricity. FormFactor's ideally positioned to help lead test for this new area as our lab-to-fab strategy has produced a decade-long first-mover advantage paired with key customer and partner relationships.
Before turning the call over to Aric, I want to once again thank the global FormFactor team for continuing to demonstrate remarkable agility and perseverance in navigating the current challenging supply environment, quickly resolving internal and external constraints to again grow in the third quarter. 
With our recent qualifications and Farmers Branch coming online, we're well positioned to accelerate our growth as test intensity and complexity continue to rise at the intersection of high-performance compute and advanced packaging. The midpoint of our fourth quarter outlook puts us on track to exceed $1 billion of revenue in 2026, and we're excited to cross this important milestone for FormFactor on the way to the $1.6 billion revenue level and $5 of non-GAAP earnings per share of our target model. Aric, you're up.

**Aric McKinnis** (Executives):
Thank you, Mike, and good afternoon. Q3 was another strong quarter for FormFactor. We delivered non-GAAP gross margin of 56.5% and non-GAAP earnings per fully diluted share of $1.04 on our fourth consecutive quarter of record revenues, revenue levels close to 40% higher than the same quarter a year ago. These results continue the operating story we discussed last quarter, addressing broad-based demand by driving higher output from our existing manufacturing footprint through improved cycle times, yields and operating efficiency. Revenue increased 9% sequentially, while non-GAAP operating expenses fell by approximately 250 basis points as a percentage of revenue. 
Combined with record revenue, these improvements produced strong operating leverage across the P&L. Non-GAAP gross margin increased 320 basis points sequentially to 56.5%. Approximately $10.5 million or about 380 basis points, of benefit resulted primarily from tariff refunds and favorable subcomponent costs in our Quantum business that are not expected to recur. Excluding these items, non-GAAP gross margins would have been between 52.5% and 53%, about 150 basis points above the baseline described last quarter. This durable improvement in baseline non-GAAP gross margins is the result of continued improvements in labor performance, manufacturing spending, yields and other production costs. 
We now view around 53% as the gross margin baseline at Q3 volumes. Over the course of the Farmers Branch ramp in 2027, we expect leverage from higher volumes and increased operational efficiency to effectively offset the temporary inefficiencies typically associated with new factory ramps. Accordingly, we expect 2027 gross margins to continue at levels similar to the current baseline. Stepping through our results in a bit more detail. Q3 revenues of $280.5 million came in $10.5 million above the midpoint of our Q3 outlook range of $260 million to $280 million and were up $22.3 million, or 9%, from Q2. 
Systems segment revenues grew on higher TRITON Photonics system revenues, reaching a new record of $59.5 million in Q3, up $11 million or 23%, from Q2. GAAP gross margin for the third quarter was 54.7%, up from 50.7% in Q2. Cost of revenues included $5.1 million of GAAP to non-GAAP reconciling items, primarily related to stock-based compensation, amortization of intangibles and restructuring charges. Details of the GAAP to non-GAAP reconciling items are outlined in our press release issued today and in the reconciliation table available on the Investor Relations section of our website.
On a non-GAAP basis, third quarter gross margin was 56.5%, 320 basis points higher than Q2 and 100 basis points above the high end of our outlook range. The favorable impact of tariff refunds on gross margins in the third quarter was about 300 basis points, or $8.6 million. In Q4, we expect to receive back the remaining roughly $2 million of tariffs paid under IEEPA, or around 70 basis points at the midpoint of the outlook range. Once these refunds are received, we do not expect any ongoing benefit to baseline gross margins from tariff refunds. 
Probe card gross margin increased by about 90 basis points to 55.3% as higher utilization, improved yields, manufacturing spending discipline and tariff benefits more than offset the less favorable mix in DRAM. System gross margin increased by more than 10 percentage points to 61% about half of the system gross margin improvement from Q2 was driven by record revenue volumes that created significant operating leverage on fixed costs, primarily due to increased sales of our TRITON Photonics systems. The remaining improvement came from items we don't expect to recur as described earlier.
Our GAAP operating expenses were $71.8 million for the third quarter, down from Q2 and down as a percentage of revenue. On a non-GAAP basis, operating expenses were $64.4 million or 23% of revenue and also down from the second quarter at $65.7 million or 25.4% of revenue. This approximately 250 basis point sequential improvement in non-GAAP operating expenses demonstrates continued operating leverage despite including increased Farmers Branch ramp costs. Included in Q3 operating expenses were $6.4 million of preproduction ramp costs. 
We expect these expenses to transition to the cost of revenues as capacity expansion phases are released to production. GAAP net income for the third quarter was $73.8 million or $0.93 per fully diluted share, up from GAAP net income of $56.2 million or $0.71 per fully diluted share in the previous quarter. The increase was driven primarily by higher revenue, higher gross margin and lower restructuring-related costs. Third quarter non-GAAP net income was $82.3 million or $1.04 per fully diluted share, up from $65 million or $0.82 per fully diluted share in Q2. About $0.09 of EPS was attributable to tariff refunds in the third quarter. 
The GAAP effective tax rate for the third quarter was 15.5% and the non-GAAP effective tax rate for the third quarter was 17.6%. Moving to the balance sheet and cash flows. We delivered free cash flow in the third quarter of $64.8 million compared to $52.6 million in Q2. This increase in free cash flow was driven primarily by higher cash flows from operations, partially offset by higher cash spent on CapEx for Farmers Branch. Cash flows from operations were $104.3 million in Q3, up $42.5 million from Q2, driven primarily by higher net income, partially offset by working capital investments to support the higher operating levels. At quarter end, cash -- total cash and investments were up $50 million to $399 million. 
Our capital allocation framework remains unchanged. Cash will be used to reinvest in the business, pursue targeted acquisitions to expand our served markets and to execute share repurchases with the objective of offsetting dilution from stock-based compensation. During the third quarter, we did not repurchase any shares. And at quarter end, $70.9 million remained available under the $75 million repurchase program authorized in April 2025. As Mike mentioned, at the beginning of the current fourth quarter, we announced a collaboration with Teradyne. This included a $300 million investment in FormFactor in order to formalize our partnership and reinforce the open ecosystem for probe card and ATE solutions. 
The areas of partnership closely align with the growth areas in our target model and are intended to accelerate development of solutions for our mutual customers. This investment strengthens our balance sheet, but does not change our capital allocation priorities. With respect to investing in the business, the Farmers Branch ramp to initial target capacity remains on track, if not slightly ahead of our original schedule. Due primarily to optimization of timing of capital spending and favorable payment terms, we now expect 2026 cash capital expenditures for Farmers Branch to be between $100 million and $110 million, below our prior estimate of $140 million to $170 million.
Importantly, this simply reflects changes in timing of cash rather than a change in scope or velocity of the ramp as project commitments and total project costs associated with the initial target capacity remained aligned with our original plans. We expect the associated cash spending to shift into 2027 as we continue executing the ramp and the expansion of the site. and we expect capital investment in Farmers Branch to remain at similar levels in the next year. 
Exiting 2027, we expect Farmers Branch will have the capability to produce about $400 million in annual probe card revenue, and we expect that capability to ramp over the course of 2027. Preproduction ramp costs are currently recorded as a component of G&A, and we continue to expect $25 million to $30 million of Farmers Branch preproduction expense in 2026. As we begin production, costs will move from operating expenses into cost of revenues. We expect to see this begin in Q4 with about $5 million of start-up costs planned to move from OpEx to cost of revenues in the quarter and another $5 million remaining in OpEx, the latter related to capacity expansion phases not yet released to production.
Turning to the fourth quarter non-GAAP outlook. We expect revenue of approximately $285 million, plus or minus $10 million. At the midpoint, we expect non-GAAP gross margin of 54%, plus or minus 150 basis points. The expected Q4 non-GAAP gross margins are better than the baseline gross margin of 53% described earlier, primarily on tariff refunds, better mix and higher volumes. At the midpoint, we expect Q4 non-GAAP operating expense of approximately $69 million, plus or minus $2 million, including Farmers Branch ramp costs. 
Our Q4 non-GAAP effective tax rate is expected to be within the range of 15% to 19% -- non-GAAP earnings per fully diluted share for Q4 are expected to be $0.95, plus or minus $0.09. A reconciliation of our GAAP to non-GAAP Q4 outlook is available on the Investor Relations section of the website and in our press release issued today. Q3's results and our Q4 outlook demonstrate the operating leverage available when strong demand is combined with an efficient cost structure and disciplined spending. We are continuing to produce more from our existing footprint through better cycle times, higher yields and improved resource efficiency, even while investing in Farmers Branch to create the capacity and structural economics required for the next phase of growth. 
Our position at the intersection of high-performance compute and advanced packaging provides broad exposure across the AI compute architecture from HBM paired with advanced GPUs, CPUs and custom ASICs to emerging co-packaged optics and other photonics applications. As we have demonstrated, the underlying operating model is substantially stronger than it was 1.5 years ago and positions us well to deliver against our target model of $1.6 billion in revenues at 55% gross margins and $5 of EPS. With that, let's open the call for questions. Operator?

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Krish Sankar of TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
I have 2 of them, Mike or Aric. First one, I think, Mike, you mentioned that calendar '27 gross margin is similar to the current baseline, which is 53%. I'm just wondering, I understand you have Farmers Branch ramping up. Are there any other headwinds to think about? Or why wouldn't margins get better as volumes ramp next year?

**Aric McKinnis** (Executives):
Yes. Thanks for your question, Krish. I'll take this one. This is Aric. So, we stated that we expect at current operating levels that our baseline gross margins are now at 53%, and that's up from the 51% to 51.5% we discussed last quarter. Of course, with any ramp of a production facility, you're going to have some inefficiencies, and that's associated with headcount additions and other spending that's required to support the ramp as you're ramping up capacity. 
What we expect to be able to do and one of the planned potential successes of our strategy is that we expect to be able to effectively offset that investment with associated increase in volume as well as efficiencies similar to the ones that we've been driving over the last 1.5 years. So, while you would typically see a degradation in gross margins as a result of a ramp, we think we can largely offset those potential inefficiencies that are temporary in nature and sustain the current operating levels.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got it. And then a quick follow-up for Mike. Mike, I think you had like pretty good traction in the past on HBM. Just kind of 2-part question on it. One is, how do you think about like all the chatter about HBM de-specing? How would that impact you? And the part 2 version of that is if we do more lower the signal requirements or the pin speed requirements for HBM, how would it impact probe card intensity?

**Mike Slessor** (Executives):
Yes. So, as you said, Krish, 2 parts to that, that HBM continues to be a major driver for our business. both here through 2026 and into 2027. On the de-spec, we're really not seeing any significant impact. To orient everybody, we do see third quarter HBM revenue down, but that's primarily a result of customers shifting mix. And with the HBM4E and HBM5 design funnel we have and the forecast we have from customers, we expect continued strong growth in HBM. I'll remind people that one of the places where we're really strongly differentiated is in the final stack test.
And of course, this HBM de-spec involves more completed stacks with fewer die in each stack. We're moving from, for example, 12-high to 8-high. And so this potentially hard to account for all the moving parts, but we don't see any significant headwinds associated with HBM growth associated with the de-spec. On the speed question, if you look at the road map, the move from HBM4 to, as I said, we're working right now on initial designs for 4E and 5. That continues to be an advancing road map with higher speeds. 
And that's also been a place where FormFactor provides strong differentiation for our customers, high-speed test performance, so they're guaranteeing to their customers, they're meeting their test specs with high productivity and high parallelism from our SmartMatrix DRAM architecture.

**Operator** (Operator):
Our next question comes from the line of Craig Ellis of B. Riley.

**Craig Ellis** (Analysts):
Mike, I wanted to follow up on some of the comments around foundry/logic given the strength we saw in the business. First, can you go into a little bit more detail on some of the things that were driving the sequential growth in the quarter? And I think you indicated that you expected the business to grow again in the fourth quarter. Is it similar drivers? Is it new drivers? And as you comment, can you help us understand the degree to which traditional x86 server strength is benefiting the business in light of the fact that Micron was out there less than 1 month ago talking about high teens growth this year and next?

**Mike Slessor** (Executives):
Yes. So, foundry/logic, as you know, up in Q3, right around 10% -- and as I said in my prepared remarks, we expect Foundry and Logic to grow again in Q4. One of the key features of this growth, key drivers of this growth is CPUs for presumably Agentic AI use cases, right? This has been an interesting development in 2026. And it's an example where we have really strong exposure, right, both through historical long-term customer relationship where we have high native share. 
That customer almost a 10% customer in Q3 based on this data center CPU strength, and we would expect them probably to appear as a 10% customer in Q4, but also exposure with x86 fabless and ARM CPU features. So, as that business continues to grow, nice exposure, it is one of the key drivers for Foundry and Logic right now.

**Craig Ellis** (Analysts):
That's really helpful. And then the follow-up is on the systems business. You've been real clear this year, we should expect strength in TRITON. It seems like it's coming in even stronger than we expected 6 months ago, maybe even 3 months ago. As you talk to customers, what are they signaling about the durability of the strength we're seeing today as we look through the fourth quarter of this year and into 2027?

**Mike Slessor** (Executives):
Yes. TRITON and Photonics has been one of the real highlights for us in 2026. It's been a set of investments we've been making for the better part of a decade. And as you noted, we've accelerated our expectations now to north of $30 million in TRITON revenue for 2026 after starting the year at between $10 million and $20 million Customers continue to be very bullish. It's still really dominated by 1 ecosystem, at least on the CPO side. But as I mentioned in the prepared remarks, one of the other things we're seeing is some diversification where we're seeing adoption in NPO applications and some pluggables applications as well.
In pluggables, not necessarily the TRITON system, but a derivative technology. There's a focus area where we expect continued growth, right? Photonics is such a compelling solution for the power and energy challenges that the industry face. It's really a question of when and not if, and we're seeing the early innings of that when really take place here in '26 into '27.

**Operator** (Operator):
Our next question comes from the line of George Brown of Deutsche Bank.

**George Brown** (Analysts):
Just 2 from my side. So, just firstly, on the GPUs and maybe the ASIC side, I think you said in your statements that you shipped products for the GPU in this quarter. But I think most of the step-up in your sales to TSMC, which is again a sort of over 10% customer. It sounds like it's mainly from TRITON or the CPU stuff rather than maybe less so the GPU. So, how should we think about the GPU sort of contribution in Q3 and into Q4 and also as we go into 2027 with more capacity coming online? 
And I guess, in a similar vein on the ASIC side, -- sort of are there any updates here in terms of qualifications? I know last quarter, you talked about the Google TPU likely requiring advanced MEMS at some point. So, any update there as well? And then I have a second.

**Mike Slessor** (Executives):
Okay. Let me see if I could parse -- there was a lot in that question. Let's start with the GPU. We did say in the prepared remarks that we shipped probe cards for 1 single GPU design to the world-leading foundry in multimillion-dollar quantities. And this is the very early part of us becoming a key part of those projects annually. We're well positioned to grow that business and start to take significant share in 2027, and that's a key feature of our growth.
Similar for custom ASICs, right, where we've qualified, shipped multiple units, but we're really constrained essentially by our ability to produce in volume. And that's why Farmers Branch getting that ramped up, as Aric described, is the #1 priority for the company. We ourselves very well positioned, whether it be GPUs, x86 fabless CPUs, custom ASICs, customers need our technology. This advanced MEMS technology is a key enabler for high-performance compute, getting the capacity online to go deliver that top priority for the company, and we're executing really well on that as fast as we can.

**George Brown** (Analysts):
Perfect. And then just following on from what you said in terms of capacity, we're hearing more from your peers about accelerating capacity additions, really sort of doubling down here to ramp as fast as possible. I think Advantest said this morning, they're accelerating their plans to double their capacity on the logic test equipment side and hinted at doubling again over the midterm. So, just wondering how much flexibility here you guys have in terms of accelerating the ramp at Farmers Branch into '27, maybe into '28 because I think there's multiple phases you have, I think, Phase 1 to Phase 2. And obviously, the injection from cash from Teradyne. I wonder if that helps, I guess, is my question.

**Aric McKinnis** (Executives):
Yes. I think -- as Mike shared, this is our #1 priority as a company right now is making sure that we bring up the capacity at Farmers Branch as fast as possible, but within the context of making sure we preserve our quality and we do it the right way. I provided an expectation of where we think we'd be able to exit 2027 at about $400 million of capability. That's framed on a variety of potential scenarios, and that's one that we think balances the risks with our execution ability.
We feel really good about the team that we have working on this. It's a team that has done this before. They've demonstrated their ability to deliver over the past 1.5 years on the cost improvements that we've been working on. So, we feel really good about where we're at. Maybe the additional point I'll add here is that Farmers Branch is really a platform for us to build on going forward. And so by definition, it is flexible. 
That's one of the basic tenets around that site is we want to make sure that we can add capacity in a modular fashion as we move forward and as the demand environment dictates. In the ramp phase, there's -- we've got plenty to do over the next 12 months. So, I think it's a good balanced view of what we put out there in terms of our potential exiting the year and then moving beyond that into coming years.

**Operator** (Operator):
Our next question comes from the line of Matt Prisco of Cantor.

**Matthew Prisco** (Analysts):
I guess to start off, just a follow-up on Farmers Branch there. How should we think about the linearity of that ramp throughout 2027? And do you expect to have the demand to fill that fab completely as it kind of ramps to that $400 million annual run rate capability exiting '27?

**Aric McKinnis** (Executives):
Yes. I think -- so I'll just reiterate, we expect to be able to exit the year at this $400 million annual run rate capability. That's a capability exit. not necessarily the revenue. The revenue is going to be dictated by the timing of demand as you state. Now the current demand environment is clearly very strong. So, I think our thinking right now is that capacity is the limiting factor, and that is why it's the #1 company priority that we're focused on.

**Matthew Prisco** (Analysts):
And then that linearity through the year, should we expect that to be even better?

**Aric McKinnis** (Executives):
Yes, sorry. And then yes, I think linearity is -- it's a fair assumption to assume it roughly linear. Now there could be puts and takes as things kind of shift around in the schedule. But I think as a mental model, that's a fair way to think about it, starting at something close to 0 and ramping up over the course of 2027 to the $400 million worth of annual capacity.

**Matthew Prisco** (Analysts):
Got you. And then as my follow-up, just going back to gross margins, can you give a little more color on what's driving that 2-point increase in the baseline? And then maybe the headwind that Farmers Branch that early ramp you expect, can you quantify that headwind at all through '27, so we can start thinking through once we're at that full run rate, what kind of tailwind we can expect from that facility?

**Aric McKinnis** (Executives):
Yes. So, the increase in the baseline gross margins is driven really by the same things that we've been seeing over the past 1.5 years. It's cycle times, it's yield, just improving our efficiency in our existing footprint. We're getting more out with the same amount of resources, and that's driving up our gross margins because it's driving down our unit cost. That's really what's driving that once we exclude those nonrecurring items. As it relates to 2027, we haven't quantified the pluses and minuses over that time frame, mainly because it's a false sense of precision. But we are committed to when we exit the year after we have completed that initial ramp that it will be accretive to the gross margin levels we see today once we're at that initial capacity.

**Operator** (Operator):
Our next question comes from the line of [ Elizabeth Sun ] of Citi.

**Yiling Sun** (Analysts):
I guess my first question is also on the Farmers Branch. I understand you are trying to ramp as fast as possible throughout next year. I'm just curious, for the near term, it seems like capacity is becoming more of a constraint on the growth. And it seems like Q4 is kind of constrained on that as well. So, I was just curious, as we go into Q1 next year, how much longer does farmers -- does the capacity continue to be a headwind or constraints? And it's just how fast you can ramp in Q1 so that it doesn't -- for Farmers Branch so that it doesn't become a constraint?

**Aric McKinnis** (Executives):
Yes. I agree that we're starting to see more and more tightness in our ability to produce. We're operating kind of at the limits of what our current footprint can do. And as you correctly noted, and maybe just we've managed to squeeze out significantly more production over the course of this year from the beginning of this year to the end of this year, and that's driven through these process improvements, these efficiencies that we've driven, really the same footprint. We've squeezed that orange multiple times now, and it's getting harder and harder to get more out of that. 
You can see that in our outlook for Q4, where our incremental guide up a little bit less than maybe the prior quarter, what we were able to achieve. So, you're correct in your statement that we are starting to see those limits. Farmers Branch is, of course, the relief valve for that. And I'll just go back to kind of what I said previously is that we expect that capacity to come online effectively linearly over the year to that $400 million ending exiting capability.

**Yiling Sun** (Analysts):
Okay. Got it. And then on the gross margin side, I think Aric talked about or Mike talked about like there is structurally increasing gross margin in DRAM side. There is like cost programs you are executing. So, I'm just curious right now how -- is there any pricing element in that gross margin improvement for DRAM overall? And also, how far is DRAM gross margin away from foundry logic right now?

**Mike Slessor** (Executives):
Yes. Elizabeth, it's Mike. I'll take that. What we did note and just to orient everyone, we delivered again record DRAM revenue and at the same time, delivered record or near record company gross margins. That's something you would have not seen from the FormFactor of the past. And it goes to these DRAM cost reductions. If I look at the DRAM gross margins and parse them, there's very little contribution from price increases. 
As we've shared with people in the past, our business model is really about delivering value to our customers and then getting compensated for that value. So, we're not running a commodity business here. There are situations where an expedited delivery or a capacity reservation is valuable for our customers, and they are compensating for that. But it's not the prominent theme associated with DRAM gross margin improvement.

**Operator** (Operator):
[Operator Instructions] Our next question comes from the line of Charles Shi of Needham.

**Yu Shi** (Analysts):
Maybe I want to push you guys a little bit more on the Farmers Branch gross margin. I understand that during the ramp, there's always offsetting factors. But in a steady state, let's say, once Farmers Branch is fully ramped, you're in a steady state. There's no ramp cost-related headwinds left. I'm sure you know the cost structure of that new facility. And what would be the steady state gross margin accretion to the overall FormFactor. If you can shed some light into that, that would be great.

**Aric McKinnis** (Executives):
Yes. I think over the longer term, what we're seeing in terms of what we've been able to achieve so far this year as an example and as we head into the ramp of Farmers Branch is very close alignment to the target model that we communicated earlier this year in terms of operating leverage and the sort of gains that we're able to drive as volumes increase. I think that continues to hold as we exit the Farmers Branch ramp. And the target model did include the investments required to build out effectively the capacity to support the $1.6 billion revenue level. So, I think looking at the target model profitability is a good guide for you beyond next year.

**Yu Shi** (Analysts):
Okay. Maybe a question for Mike. Mike, the TRITON system revenue, if I understand correctly, from last year to this year, based on what you just said, north of $30 million it's approximately 4x of last year's level. Obviously, this is probably still a small part of the FormFactor business, 3% or 4% of the total. But let's say, you've had franchises in the past that it can grow multiple times in a short amount of time like HBM franchise, right? So, do you have the capacity in place, let's say, that the TRITON system demand can do another 3x or 4x or even higher going into next year? And with all the attention on Farmers Branch, that seems like a probe card facility, anything you're doing on the system side?

**Mike Slessor** (Executives):
Yes. So, TRITON really has been a great growth story for us in 2026. But as I mentioned earlier, really the result of many, many years of investment and partnership with some of the driver customers. In 2025, it was 0 revenue. So, it's gone from 0 to $30-plus million here in 2026. And when you look at how we manufacture the TRITON system, it's a little less internally focused and more externally focused on different subcomponents. We're basically integrating and assembling some subcomponents. 
And so it's not quite the capacity constraints that we have in what's a pretty vertically integrated business in probe cards. All of our growth forecasts, even at the high end, remember, we talked about this being a $400 million served market in 2030, showing good progress this year to start to move on the way there. We expect the same in 2027, and we do not expect capacity to be a constraint on the growth of that business.

**Operator** (Operator):
Our next question comes from the line of Brian Chin of Stifel.

**Brian Chin** (Analysts):
Mike, so in the past, when TSMC has bobbed its head over 10%, now that's, I think, 2 quarters in a row, maybe the business was $100 million below the run rate you're at now, so call it a $190 million or $180 million versus like a $280 million now. And historically, it's the composition of that business, there's been certainly a bias towards things like mobile processors, et cetera. Is that kind of historic larger part of the TSMC foundry business, is that kind of a similar size and kind of all the incremental growth from 10% at $180 million versus 10% at $280 million. Is that all coming mainly from like custom ASICs? Or how would you describe how the composition of that TSMC business has evolved?

**Mike Slessor** (Executives):
Yes. It's actually a microcosm of how we've driven our larger growth strategy at the company. There is multiple components to it. As you note, historically, that business was anchored in essentially mobile application processor ramps, broadened out a little bit as high-performance compute started, broadened out a lot this year with some more high-performance compute and different projects. And we've also got the TRITON system there now as well. 
So, a broader-based set of opportunities with that customer, again, an almost perfect parallel to the way we're driving growth and diversification for the overall company, where we've got exposure to multiple different opportunities, making sure that when those opportunities hit, we've got exposure to them. I think the business with that customer, again, a perfect microcosm of how we approach driving the overall growth strategy for FormFactor.

**Brian Chin** (Analysts):
Okay. That's helpful. And then in terms of the initial waves or batches of products that you start to bring up in Texas and the new probe card facility, is there a bias towards just new customer designs straight into Texas? Or is there some sort of balance there between products and maybe you're transferring out of Livermore and moving there? What's kind of the thought process on what kind of batch lead offs?

**Mike Slessor** (Executives):
Yes. So, that gets pretty in the weeds, but -- let me try and give you some of the themes for it. We are initially ramping assembly and test for our foundry and logic products, and we'll be adding the MEMS front end for foundry and logic products in 2027. That frees up DRAM capacity in Livermore. And so the set of customers served out of Farmers Branch primarily -- well, not primarily, exclusively foundry and logic customers. Within that set, we're obviously optimizing things for speed to ramp. If customers want a lengthy detailed qualification process, well, maybe they're going to be closer to the end. 
We want to make sure we're utilizing that capacity as aggressively as we possibly can. One of the earlier questions about us being capacity constrained, we don't want that capacity sitting idle while customers decide whether they're going to qual or not. So, there's very much a bias, whether it be new customers or existing customers who have a practical but aggressive qual plan to get them into Farmers Branch first.

**Brian Chin** (Analysts):
Okay. That's pretty helpful. And then maybe in terms of the comment that things are going a little bit ahead of plan, is that in terms of your initial view of how that engagement is going with your customers? Is that kind of the learning curve on training new employees and hiring them? Is that the availability of the equipment sets?

**Aric McKinnis** (Executives):
Yes. It's really a reflection on the expected revenue shipment timing. So, we initially expected the first revenue out to either be at the very, very end of this year to the beginning of 2027. And as Mike mentioned in his prepared remarks, we shipped our first card in the last couple of weeks. So, that's the acceleration that we're seeing. That said, the other areas that you mentioned, such as workforce, et cetera, also seem to be going well. Again, we've got a really good team working on this. I think we're continuing to tick through the milestones at a good pace.

**Brian Chin** (Analysts):
Good. Just be careful lifting those cards in the factory.

**Operator** (Operator):
I would now like to turn the conference back to Mike Slessor for closing remarks.

**Mike Slessor** (Executives):
Thanks, everybody, for joining us today. An exciting time for FormFactor. As I said in the prepared remarks, our guidance implies going through $1 billion of revenue this year for the first time in company history. We've got a bright future in front of us with Farmers Branch coming online. Thanks for joining.

**Operator** (Operator):
This concludes today's conference call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FORM_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO Aric McKinnis｜guidance：Q3 營收指引 2.7 億美元 ±1,000 萬。（原話："We expect Q3 revenues of $270 million, plus or minus"）
- 2026-07-29｜CFO Aric McKinnis｜guidance：Q3 非 GAAP EPS 指引 0.86 美元 ±0.09。（原話："for Q3 is expected to be $0.86, plus or minus $0.09."）
- 2026-07-29｜CEO Mike Slessor｜guidance：Q3 DRAM 營收與 Q2 相當，但 HBM 轉向 DDR 的結構明顯變動。（原話："but with a significant underlying shift from HBM to DDR."）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q2 非 GAAP 毛利率 53.3% 的改善拆成三分之一持久成本降低、三分之一營收增加、三分之一不會重複的項目。（原話："Approximately 1/3 of the improvement is from baseline cost"）
- 2026-07-29｜CFO Aric McKinnis｜margin：排除一次性項目與產品組合有利後，基準毛利率約 51%。（原話："improved to around 51% at Q2 volumes."）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q3 毛利率指引 54% 的中點高於 51% 基準，主因是 IEEPA 關稅退款（約 300bp，不會重複）。（原話："300 basis points in IEEPA tariff refunds"）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q3 非 GAAP 毛利率指引中點 54%，±150bp。（原話："gross margin of 54%, plus or minus 150 basis points."）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q3 較高營收量的好處預期被 DRAM 較不利的產品組合抵銷。（原話："The benefits of marginally higher Q3 revenue volumes are"）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q2 探針卡部門毛利率 54.4%，歸因於稼動率、支出紀律與良率。（原話："increased to 54.4%, driven primarily by higher factory"）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q2 非 GAAP 營業費用 6,570 萬美元，占營收 25.4%，Q1 為 27.4%。（原話："operating expenses were $65.7 million or 25.4% of revenue"）
- 2026-07-29｜CFO Aric McKinnis｜guidance：Q3 非 GAAP 營業費用指引 7,000 萬 ±200 萬，含約 700 萬 Farmers Branch 預生產租金。（原話："about $7 million in preproduction rent costs"）
- 2026-07-29｜CFO Aric McKinnis｜guidance：2026 年 Farmers Branch 與產能擴充現金資本支出預期 1.4 億至 1.7 億美元，維持不變。（原話："capacity additions will be between $140 million"）
- 2026-07-29｜CFO Aric McKinnis｜guidance：2026 年預生產爬坡成本預期調整為 2,500 萬至 3,000 萬美元。（原話："between $25 million and $30 million in total in 2026."）
- 2026-07-29｜CFO Aric McKinnis｜guidance：Q3 非 GAAP 有效稅率預期 15% 至 19%。（原話："expected to be between the range of 15% to 19%."）
- 2026-07-29｜CEO Mike Slessor｜commitment：Farmers Branch 預計 Q4 上線、2027 年全年爬坡。（原話："site is on track to come online in the fourth quarter"）
- 2026-07-29｜CFO Aric McKinnis｜commitment：2030 目標模型：營收倍增至 16 億、非 GAAP 毛利率 55%、EPS 5 美元。（原話："achieving 55% non-GAAP gross margin and more than doubling"）
- 2026-07-29｜CFO Aric McKinnis｜commitment：Farmers Branch 達初期目標產能（預計 2028 初）後預期對毛利率有增益。（原話："we expect Farmers Branch to be accretive to gross margin."）
- 2026-07-29｜CFO Aric McKinnis｜commitment：管理層表示毛利率增益主要在 2028 年才完整體現，2027 年爬坡有無效率。（原話："primarily counting on matching that sort of improvement"）
- 2026-07-29｜CFO Aric McKinnis｜capital_allocation：Q2 未回購股票，短期現金優先用於 Farmers Branch 爬坡。（原話："During the second quarter, we did not repurchase any shares."）
- 2026-07-29｜CFO Aric McKinnis｜capital_allocation：Farmers Branch 投資主要由獲利與營運現金流自行資助，另有德州 2,420 萬美元補助。（原話："largely self-funding the investment in Farmers Branch"）
- 2026-07-29｜CEO Mike Slessor｜product：CPO 營收原預期達年初 1,000 萬至 2,000 萬區間高端，現預期 Q3 底超越該區間、全年顯著超過 2,000 萬。（原話："We now expect to exceed that range by the end"）
- 2026-07-29｜CEO Mike Slessor｜product：CPO 全年超過 2,000 萬確定，但幅度難以判斷，新技術有加速與消化階段。（原話："The magnitude of that is a little tricky to judge"）
- 2026-07-29｜CEO Mike Slessor｜product：管理層表示 CPO 無顯著提前或改變看法，2027 逐季預測過細。（原話："wouldn't say there's a significant pull in or change in our"）
- 2026-07-29｜CEO Mike Slessor｜product：Q2 HBM 約占 DRAM 營收三分之二，來自兩家客戶採用 SmartMatrix。（原話："HBM comprised approximately 2/3 of our overall DRAM revenue"）
- 2026-07-29｜CEO Mike Slessor｜product：Systems 營收 Q2 季增近一倍，來自工程探針台復甦與 CPO 加速。（原話："Systems revenue nearly doubled sequentially"）
- 2026-07-29｜CEO Mike Slessor｜product：下一代自訂 ASIC（如 Google TPU）預期需要先進 MEMS 探針卡；2026 年無顯著營收貢獻，2027 起放量。（原話："significant revenue contributions here in 2026."）
- 2026-07-29｜CEO Mike Slessor｜customer：Q2 台灣營收季增逾 30%，全球領先晶圓代工廠再度為 10% 客戶。（原話："revenue from Taiwan grew sequentially by more than 30%"）
- 2026-07-29｜CEO Mike Slessor｜customer：Q2 10% 客戶中無 GPU 業務；GPU 預期為下半年事件，已通過認證並於 Q3 出貨量產品。（原話："There really is no component of GPU business in the second"）
- 2026-07-29｜CEO Mike Slessor｜customer：CPU 需求增加來自三組客戶關係：既有 CPU 龍頭、HPC 龍頭擴張、大型無晶圓 XPU 客戶多個設計案。（原話："successful qualification and subsequent multiple design wins"）
- 2026-07-29｜CEO Mike Slessor｜customer：無晶圓 CPU 客戶市占為低個位數，產能受限成為市占成長的限制因素，直到 Farmers Branch 上線。（原話："single-digit market share at this point"）
- 2026-07-29｜CEO Mike Slessor｜competition：HBM 的強勢市占集中在高速堆疊晶粒最終測試，核心晶粒等插入點競爭多。（原話："lots of competition for example, in the core die insertions"）
- 2026-07-29｜CEO Mike Slessor｜competition：第三大 HBM 客戶的市占不如前兩家強。（原話："although our share is stronger at two of them right now."）
- 2026-07-29｜CEO Mike Slessor｜competition：GPU 先進 MEMS 探針卡目前主要是競爭對手的生意，公司剛通過認證。（原話："Right now, it's primarily"）
- 2026-07-29｜CEO Mike Slessor｜risk：DRAM 客戶因 DDR5 價格轉向 DDR，探針卡為裝置專用耗材，公司 DRAM 組合隨之變動。（原話："probe cards are a device-specific consumables"）
- 2026-07-29｜CFO Aric McKinnis｜risk：供應鏈限制在目前生產水準下增加。（原話："we see more constraints across the supply chain"）

### FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md
- 2026-05-11｜CFO Aric McKinnis｜guidance：2030 目標：市場成長至 $4.5B，FormFactor 營收翻倍至 $1.6B（原話："we're expecting the market to grow to $4.5 billion."）
- 2026-05-11｜CFO Aric McKinnis｜guidance：2030 目標毛利率 55%（原話："55% gross margins at these revenue levels"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：2030 目標非 GAAP EPS $5（原話："a non-GAAP EPS of $5 per share"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：2030 營業費用占營收 23%（原話："operating expense as a percent of revenues of 23%"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：EPS 由 2025 年 $1.27 增至 $5（原話："$1.27 in the baseline year of 2025 to $5 a share"）
- 2026-05-11｜Sudhakar Raman｜guidance：探針卡業務 2030 年營收翻倍（原話："double the probes business revenue by 2030"）
- 2026-05-11｜Jens Klattenhoff｜guidance：Systems 部門 2030 年營收翻倍（原話："planning to double our revenue within the Systems segment"）
- 2026-05-11｜CEO Mike Slessor｜guidance：CPO 2026 營收原預期 $10–20M，上季財報更新至區間高端（原話："we updated that to the high end of that range"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：晶圓級 CPO 測試 2030 年 SAM 約 $300–400M（原話："SAM by 2030, around about $300 million to $400 million"）
- 2026-05-11｜Jens Klattenhoff｜guidance：Jens 稱矽光與 CPO 2030 年對公司為數億美元機會（原話："a multi-hundred million dollar opportunity by 2030"）
- 2026-05-11｜Sudhakar Raman｜guidance：Sudhakar 稱先進探針卡市場至 2030 年成長口徑為 $2.8B 至 $4B（與 CFO 的 TAM $3.1B→$4.5B 口徑不同）（原話："growth of about $2.8 billion to $4 billion by 2030"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：市場 CAGR 約 8%，公司計畫成長速度為其兩倍（原話："about 8% CAGR over this time frame"）
- 2026-05-11｜CFO Aric McKinnis｜margin：2020 年舊目標模型：營收約 $850M、毛利率 47%（原話："targeting around $850 million in revenue, 47% gross margins"）
- 2026-05-11｜CFO Aric McKinnis｜margin：毛利率改善拆解：量能約 600bp（原話："about 600 basis points from volume as we double revenues"）
- 2026-05-11｜CFO Aric McKinnis｜margin：毛利率改善拆解：營運卓越約 500bp（原話："about 500 basis points from operational excellence"）
- 2026-05-11｜CFO Aric McKinnis｜margin：毛利率改善拆解：創新約 400bp（原話："about 400 basis points from innovation"）
- 2026-05-11｜CFO Aric McKinnis｜margin：管理層稱毛利率改善不靠產品組合（原話："we aren't relying on luck"）
- 2026-05-11｜CFO Aric McKinnis｜margin：管理層稱後續改善會比前面困難（原話："Now it's going to get harder as we move"）
- 2026-05-11｜CFO Aric McKinnis｜margin：最近一季毛利率 49%，指引高 50bp；部分因素為暫時性（原話："we guided 50 basis points up from that level"）
- 2026-05-11｜CFO Aric McKinnis｜margin：最近一季探針卡毛利率超過 50%，兩部門毛利率趨同（原話："we exceeded 50% gross margin in the probe card business"）
- 2026-05-11｜CFO Aric McKinnis｜margin：毛利率單期波動正常範圍約正負數百 bp（原話："plus or minus a couple of hundred basis points"）
- 2026-05-11｜CFO Aric McKinnis｜margin：2025 年起至今已有 1,100bp 改善，三大支柱皆有貢獻（原話："the 1,100 basis point improvement that we've generated"）
- 2026-05-11｜CFO Aric McKinnis｜margin：舊目標模型因產品組合轉變對毛利率不利（原話："it was not favorable to our gross margins"）
- 2026-05-11｜CFO Aric McKinnis｜margin：Farmers Branch 爬坡期預期有毛利率逆風，由效率改善抵銷（原話："to be offset by the efficiencies that we're driving"）
- 2026-05-11｜CFO Aric McKinnis｜margin：德州製造成本較加州低（原話："in Texas, a little bit cheaper to manufacture there"）
- 2026-05-11｜Missy Figueroa｜commitment：Farmers Branch 兩條線預計年底前完成驗證，2027 年開始量產爬坡（原話："with initial production ramp starting in 2027"）
- 2026-05-11｜Missy Figueroa｜commitment：Farmers Branch 採模組化擴充，資本投入對應需求（原話："There will be no speculative capacity and no excess volume."）
- 2026-05-11｜CFO Aric McKinnis｜commitment：管理層稱 Farmers Branch 是未來約 1.5 年最優先事項（原話："probably the single most important short-term priority"）
- 2026-05-11｜CFO Aric McKinnis｜commitment：目標模型自我融資（原話："importantly, it's self-funding"）
- 2026-05-11｜CFO Aric McKinnis｜commitment：CFO 稱目標模型已含 Farmers Branch 所需投資（原話："it includes the required investment"）
- 2026-05-11｜CEO Mike Slessor｜capital_allocation：併購以補強型為主，Keystone 為例（原話："It is more tilted towards the tuck-in."）
- 2026-05-11｜CEO Mike Slessor｜capital_allocation：CEO 重申測試與封裝供應鏈需整併（原話："needs to consolidate in the supply chain"）
- 2026-05-11｜CFO Aric McKinnis｜capital_allocation：庫藏股目的為抵銷股權激勵稀釋（原話："The main purpose of that program is to buy back shares"）
- 2026-05-11｜CFO Aric McKinnis｜capital_allocation：長期維持性資本支出約占營收 4–5%（原話："around 4% to 5% of revenues in sustaining capital"）
- 2026-05-11｜Missy Figueroa｜capital_allocation：宣布關閉 Carlsbad A&T 並併入 Farmers Branch（原話："we also announced the site closure of our Carlsbad A&T."）
- 2026-05-11｜CFO Aric McKinnis｜capital_allocation：R&D 優先順序：縮小焦點、避免同時做太多事（原話："You try to do too many things at once"）
- 2026-05-11｜Sudhakar Raman｜competition：客製 ASIC 長期預期為先進 MEMS 且兩家供應商市場（原話："a 2-supplier market in the long term"）
- 2026-05-11｜CEO Mike Slessor｜competition：探針卡供給吃緊，管理層稱各家處境相同（原話："Everybody is in the same constrained situation."）
- 2026-05-11｜CFO Aric McKinnis｜competition：GPU 測試公司過去未參與，預期 2026 下半年起放量（原話："we didn't participate historically in GPU tests."）
- 2026-05-11｜CFO Aric McKinnis｜competition：CPU 部分大廠份額低到幾乎沒有，預期滲透（原話："we have low to nonexistent share"）
- 2026-05-11｜CEO Mike Slessor｜competition：公司稱自己是唯一同時有邏輯與 DRAM 探針卡規模的供應商（原話："We're the only supplier of scale in both foundry and logic"）
- 2026-05-11｜Sudhakar Raman｜product：HBM 世代演進使測試強度提高約 25–30%（原話："increases the test intensity by about 25% to 30%"）
- 2026-05-11｜Sudhakar Raman｜product：客製 HBM 新架構預期 2028 年後實現（原話："coming to fruition more in the 2028 and beyond time frame"）
- 2026-05-11｜Sudhakar Raman｜product：Sudhakar 稱現有產品跟不上下一代 GPU 熱需求，已與客戶共同開發（原話："the current set of products are not able to keep up"）
- 2026-05-11｜Jens Klattenhoff｜product：Jens 稱 2026 為 CPO 轉入量產的轉折年（原話："2026 is an inflection year"）
- 2026-05-11｜Jens Klattenhoff｜product：CPO 第一測試站可降低良品晶粒成本最多 5 倍（原話："reduces cost of good die by up to 5x"）
- 2026-05-11｜CEO Mike Slessor｜product：長期預期 CPO 測試走向拆分的開放生態（原話："we expect CPO as a team to broaden out"）
- 2026-05-11｜CEO Mike Slessor｜customer：HBM 首張探針卡出貨給現第一大客戶（2012）（原話："who's now our #1 customer"）
- 2026-05-11｜CEO Mike Slessor｜customer：客戶對 6 個月預測更投入，產能協議／付費保產能在討論（原話："capacity agreements, paying for capacity"）
- 2026-05-11｜CEO Mike Slessor｜customer：客戶提供超過一季的需求能見度（原話："not visibility, on what customers think they need from us"）
- 2026-05-11｜CFO Aric McKinnis｜customer：商務長稱公司定位已是共同開發夥伴（原話："we are no longer just a supplier"）
- 2026-05-11｜CEO Mike Slessor｜risk：管理層稱產業屬週期性，成長路徑不會線性（原話："I don't expect it to be linear"）
- 2026-05-11｜CEO Mike Slessor｜risk：管理層稱供給吃緊情況將持續一段時間（原話："in an undersupply condition for a while"）
- 2026-05-11｜CFO Aric McKinnis｜risk：管理層稱市場有過熱氛圍，自稱務實（原話："a lot of bubbliness out there in the market right now"）
- 2026-05-11｜CEO Mike Slessor｜risk：DRAM 漲價推升產業金額，探針卡金額強度預期與之脫鉤（原話："going to see a decoupling between the classic probe card"）
- 2026-05-11｜CEO Mike Slessor｜risk：人才招募有挑戰但目前順利（原話："are there challenges with talent? Sure, right?"）
- 2026-05-11｜Missy Figueroa｜risk：營運改善來源為良率與週期時間（原話："squeezing more out of the juice"）

### 問答異常語氣（迴避／改口／保留）
- FORM_Q2_2026_Earnings_Call_20260729.md｜問：Duley 詢問週期時間與良率已改善多少的具體指標（是否已達 60% 週期時間改善的一半）。｜答法：CFO 表示通常不分享這類指標，改以「on track」、Q3 營收年化近 1.1B、毛利率 49%→51% 回應，未給數字。
- FORM_Q2_2026_Earnings_Call_20260729.md｜問：Prisco 詢問 Farmers Branch 營收貢獻時間點與可觀程度。｜答法：CFO 談現有廠區效率與初始產能約等同加州探針卡廠，「to the extent the demand is there」，未給營收貢獻時點或金額。
- FORM_Q2_2026_Earnings_Call_20260729.md｜問：Needham 詢問 CPO 時程是否從 2028 提前、2027 是否放量。｜答法：CEO 稱無顯著提前或改變，但承認短期加速；表示 2027 逐季預測 a bridge too far，未給 2027 數字。
- FORM_Q2_2026_Earnings_Call_20260729.md｜問：Citi 詢問 CPO 全年可做多少營收。｜答法：CEO 稱 Q4 與全年幅度 open question、tricky to judge，只確認高於 2,000 萬。
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Craig Ellis 問營運改善是否為近期提前拉貨、Farmers Branch 前還能撐多久｜答法：CEO 轉述 Farmers Branch 不到一年內爬坡，Missy 答「confident」並談良率與週期時間，未給量化產能數字
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Matt Prisco 問明年 Q1 德州啟用折舊對毛利率影響｜答法：CEO 只答第二題（份額），Aric 稱爬坡期有逆風但會被效率抵銷，未給 Q1 數字
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Yu Shi 問 CPO 量產時點（財報會議提到 2028）是否更新｜答法：CEO 改談 2026 年營收預期更新與 Triton 裝機，未回應 2028 時點
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Stifel 分析師問 Farmers Branch 12 個月最大增量營收｜答法：Missy 轉交 Aric，Aric 稱目標模型已含投資，未給增量營收數字
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Matt Prisco 問 2030 目標是否錨定半導體營收、預測上修時如何轉換｜答法：CEO 改談 DRAM ASP 上漲與探針卡金額強度脫鉤，Aric 談務實與彈性，未說明目標模型錨定基準

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
{"date":"20260629","verdict":"觀望","role":"條件式衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"HBM4 結構性 replacement-cycle 驅動 GM/EPS 維持高檔（margin 拐點可持續）","columns":{"2Y 驗證點":"non-GAAP GM 維持 ≥ 46%、DRAM/HBM 段 YoY 雙位數","5Y 驗證點":"HBM4→HBM5 接棒不斷層、GM 站穩 45%+","10Y 驗證點":"探針卡仍是高層數記憶體測試必經環節","具體數字門檻":"non-GAAP GM ≥ 46%；DRAM/HBM 段營收 YoY ≥ +15%","信息來源":"FORM Q1 FY26 法說、8-K（2026-04-29）；probe card 市調（Mordor）","漂移觸發":"連 2 季 GM TTM 偏離 ≥ 5%（"}},{"id":"H2","text":"FORM 守住 HBM probe 領先（sole/primary），並在 F&L networking（Nvidia/AMD）拿份額補 2nm 流失","columns":{"2Y 驗證點":"HBM 維持 sole/primary、F&L networking 段成長 > F&L 整體","5Y 驗證點":"探針卡份額 ≥ 25%、HBM 段無量產 second-source","10Y 驗證點":"SmartMatrix 世代延續領先、IP 護城河擴大","具體數字門檻":"整體探針卡份額 ≥ 25%；HBM 大廠無量產 second-source","信息來源":"市調份額（FORM 26% / TPRO 16.5% / Micronics 10.2%, 2025）；各 HBM 廠認證新聞","漂移觸發":"任一 HBM 廠量產導入 second-source → 反轉"}},{"id":"H3","text":"估值（~50x forward PE）能被 EPS 成長與倍數維持消化，不大幅 de-rate","columns":{"2Y 驗證點":"forward PE 維持 ~45–55x 區間、不破 ~35x","5Y 驗證點":"5Y end PE ≥ ~28x（成熟仍享結構溢價）","10Y 驗證點":"市場持續給予 AI 測試結構溢價","具體數字門檻":"FY27 forward PE 維持 > 35x；5Y end PE ≥ 28x","信息來源":"yfinance/GuruFocus forward PE；§11.1 5Y 分位","漂移觸發":"forward PE 連 2 季"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"HBM4 ramp 時序後移 + 循環峰值 margin 回吐：SK Hynix（最大客戶 22.9%）2026-06 放慢 HBM4 + F&L（PC/server）續軟 → 近端探針卡訂單後移、GM 從 49% 回落","columns":{"對應假設":"H1","時間尺度":"⚡🔥 短中期（已部分觸發，2026H2 顯現）","監測指標":"SK Hynix HBM4 量產進度、non-GAAP GM（季）、F&L probe 訂單 YoY","警戒閾值":"GM 連 2 季"}},{"id":"R2","text":"foundry/HBM 份額流失：Technoprobe（已贏 30% TSMC 2nm）/Micronics（升 primary）擴大，並威脅切入 HBM 量產","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4–6 季）","監測指標":"各 HBM 廠/TSMC 認證新聞、FORM 份額市調","警戒閾值":"任一 HBM 廠量產 second-source → 重評 §6/§7"}},{"id":"R3","text":"估值倍數系統性下移：AI 測試溢價收斂、probe-card tier 整體 de-rate（TPRO 121x PE/FORM 56x 皆為極端）","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"forward PE 5Y 分位、同 tier（TPRO）倍數","警戒閾值":"forward PE 連 2 季"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":3.3,"ev5y_pct":13.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式衛星持倉","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":null,"ev5y_pct":13.0,"irr_base_pct":3.3,"max_dd_pct":-60.0,"bull_5y_price":245.36,"bear_5y_price":60.65,"p_bull_pct":28.0,"p_bear_pct":30.0,"rearm_trigger":null,"price_at_dd":137.84,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
