你是 stock-analyst **v20 判斷 agent**，標的 SNPS（20261019）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SNPS","date":"2026-10-19","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNPS_20261019/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNPS_20261019/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":2476.8,"period":"Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）","citation":"公司新聞稿 news.synopsys.com Q3 FY26 results"},"note":"新聞稿稱高於財測區間上緣；共識數字未查"},{"id":"f_kpi1_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":41.6,"period":"Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）","citation":"公司新聞稿 news.synopsys.com Q3 FY26 results（adjusted segment operating income $1,030.4M）"},"note":"未查"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":14.4,"period":"Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）","citation":"公司新聞稿 news.synopsys.com Q3 FY26 results（營業利益 $357.5M）"},"note":"未查"},{"id":"f_kpi3_free_cash_flow_ytd_9","label":"Free cash flow (YTD 9個月，非單季)","value":2142.5,"period":"前三季累計至 2026-07-31，公告於 2026-08-26","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"前三季累計至 2026-07-31，公告於 2026-08-26","citation":"公司新聞稿現金流量表：營業現金流 $2,298.6M 減資本支出 $156.1M（FCF 為自算，新聞稿未直接列示）"},"note":"全年 FCF 指引約 $2,600M"},{"id":"f_kpi5_guidance_q4_fy2026","label":"Guidance Q4 FY2026","value":"營收 $2,530–2,580M；non-GAAP EPS $4.10–4.16；GAAP EPS $0.60–0.85","period":"公告於 2026-08-26","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"公告於 2026-08-26","citation":"公司新聞稿 news.synopsys.com Q3 FY26 results"},"note":"未查"},{"id":"f_kpi6_guidance_fy2026","label":"Guidance FY2026 全年","value":"營收 $9,690–9,740M；non-GAAP EPS $15.04–15.10；GAAP EPS $3.84–4.08；non-GAAP 營業利益率中點約 41.5%；GAAP 約 10.4%；FCF 約 $2,600M；capex 約 $225M","period":"公告於 2026-08-26","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"公告於 2026-08-26","citation":"公司新聞稿 news.synopsys.com Q3 FY26 results"},"note":"yfinance FY1 營收共識 $9,722M、EPS $15.14（見 capital_structure／consensus_revision）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-26","period":"2026-08-26","unit":"date","basis":"距今 38 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-26"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_snps_gross_margin_pct","label":"SNPS 毛利率","value":72.38,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_operating_margin_pct","label":"SNPS 營業利益率","value":11.03,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_fcf_margin_pct","label":"SNPS FCF 利潤率","value":29.18,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cdns_gross_margin_pct","label":"CDNS 毛利率","value":85.87,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cdns_operating_margin_pct","label":"CDNS 營業利益率","value":30.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cdns_fcf_margin_pct","label":"CDNS FCF 利潤率","value":28.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_arm_gross_margin_pct","label":"ARM 毛利率","value":97.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_arm_operating_margin_pct","label":"ARM 營業利益率","value":17.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_arm_fcf_margin_pct","label":"ARM FCF 利潤率","value":28.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_gross_margin_pct","label":"QCOM 毛利率","value":54.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_operating_margin_pct","label":"QCOM 營業利益率","value":23.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_fcf_margin_pct","label":"QCOM FCF 利潤率","value":23.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC 占營收","value":9.35,"period":"Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）","citation":"公司新聞稿：SBC $231.6M ÷ 營收 $2,476.8M（自算）；占 GAAP 營業利益約 64.8%"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":454.63,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":1.12,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":49.78,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":15.14,"period":"2026-10-19","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-19","citation":"yfinance earnings_estimate"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":18.67,"period":"2026-10-19","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-19","citation":"yfinance earnings_estimate"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":80.32,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":9.25,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.2,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":10.02,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝16.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":16.6,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":7234.12,"period":"2026-10-19","unit":"USD m","basis":"yfinance 最新一季：總債務 10841.79、現金 3607.67（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":191.64,"period":"2026-10-19","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":94357.88,"period":"2026-10-19","unit":"USD m","basis":"市值 87123.76 ＋ 淨負債 7234.12","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":9722.26,"period":"2026-10-19","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（22 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":11049.98,"period":"2026-10-19","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":9.71,"period":"2026-10-19","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"SemiAnalysis EDA market primer (paywalled; 2026-05 per search summary) 與轉述報告稱 Synopsys、Cadence、Siemens EDA 三家合計市占超過 85%；CY2025 營收 Synopsys 約 80 億美元（含 Ansys）、Cadence 53.0 億、Siemens EDA 估 22–25 億。","source":"SemiAnalysis, EDA market primer","url":"https://newsletter.semianalysis.com/p/eda-market-primer","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"DAC 2026 上 AI 原生新創（Bronco AI、ChipAgents.ai、Verkor.io）展示驗證／除錯與 agent 設計指標，均為廠商自述、未經獨立驗證；文中另述 Synopsys 與 OpenAI 合作 GPT-Synopsys。","source":"ecosistemastartup.com, OpenAI y Synopsys crean GPT-Synopsys para diseñar chips con IA","url":"https://ecosistemastartup.com/openai-y-synopsys-crean-gpt-synopsys-para-disenar-chips-con-ia/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261019","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"36Kr 報導 Kimi K3 模型在不使用 Cadence／Synopsys 商用授權軟體下，48 小時自主完成晶片設計實驗；同文稱要取代仍非常遙遠。","source":"36Kr, Kimi K3 chip design experiment","url":"https://eu.36kr.com/en/p/3938614896262280","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261019","affects":["decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Pitchgrade 研究筆記把熊市情境描述為晶片設計走向參數化 AI 原生流程、超大型雲端業者自建 EDA 能力而侵蝕 Synopsys 最高價值客戶的份額；定性為長期情境，非現況。","source":"Pitchgrade, synopsys ai margin pressure","url":"https://www.pitchgrade.com/research/synopsys-ai-margin-pressure","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261019","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"2026 年 4 月 TSMC 技術論壇：Cadence（N3/N2/A16/A14 AI 設計流程）與 Siemens EDA 皆宣布擴大與 TSMC 合作，三家同步對齊埃米世代路線；屬合作公告而非具名客戶搶單。搜尋未找到 2026 年客戶從 Cadence/Siemens 轉向 Synopsys 的具名案例。","source":"Futurum, EDA Vendors Race to Align With TSMC's Angstrom-Era Roadmap","url":"https://futurumgroup.com/insights/eda-vendors-race-to-align-with-tsmcs-angstrom-era-roadmap-at-technology-symposium/","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"投資人文章稱 Cadence 在數位實作（Innovus 對 Fusion Compiler）逐步取得進展，屬意見文章、非實測份額數據；同彙整稱美國出口管制限制兩家對中國先進節點工具銷售、中國本土對手成長但短期全球取代不太可能。","source":"inpractise.com, Synopsys vs Cadence digital design tool competition and market share","url":"https://inpractise.com/articles/synopsys-vs-cadence-digital-design-tool-competition-and-market-share","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2023 10-K：單一客戶（含子公司）占合併營收 12.4%（FY2023）、11.7%（FY2022）、10.6%（FY2021）；該客戶占 FY2023 應收帳款 10.9%。搜尋未取得 FY2024/FY2025 10-K 數字。","source":"SYNOPSYS INC Form 10-K FY2023 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/883241/000088324123000019/snps-20231031.htm","excerpt":"One customer, including its subsidiaries, accounted for 12.4%, 11.7%, and 10.6% of our consolidated revenue in fiscal 2023, 2022, and 2021, respectively.","as_of":"2023-12-01","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2015–FY2018 10-K 點名 Intel 為最大客戶：占營收 15.4%（FY2018）、17.9%（FY2017）、15.9%（FY2016）；無其他客戶超過 10%。","source":"SYNOPSYS INC Form 10-K FY2018 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000883241/000088324118000012/snps10311810-k.htm","excerpt":null,"as_of":"2018-12-01","retrieved_at":"20261019","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025 年 Q3 財報 Synopsys 因 Design IP 放緩與一家大型晶圓代工客戶困難而低於預期；執行長未點名，Yahoo/Reuters 報導推測為 Intel。2026 年 Q2 展望低於分析師預期（$2.23–2.28B），原因含中國出口管制與主要代工客戶需求較弱。","source":"Yahoo Finance: Synopsys set to wipe out 2025 gains as shares tank on China business woes","url":"https://finance.yahoo.com/news/synopsys-set-wipe-2025-gains-145824225.html","excerpt":null,"as_of":"2025-09-10","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"搜尋未發現 2026 年 Synopsys 或 Intel 的信用評等調降報導；所得結果僅有股票分析師評等（Piper Sandler 2026-06-23 升評至 Overweight，目標價 550 美元，提及 Intel 18A-P 需求前景較佳）。","source":"goldesel.de: Synopsys Aktie gewinnt: Piper Sandler stuft auf Overweight hoch","url":"https://goldesel.de/aktien/news/synopsys-aktie-gewinnt-piper-sandler-stuft-auf-overweight-hoch-und-setzt-550-dollar-kursziel","excerpt":null,"as_of":"2026-06-23","retrieved_at":"20261019","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Synopsys FY2026 Q3（8月底公布）上調全年營收指引約 $50M 至 $9.69–$9.74B；Design Automation 營收約 $2B、年增 53%，Design IP 年增 10.8% 至 $473.8M；管理層將需求歸因於 AI 提高晶片複雜度，並稱非 AI 設計活動已止穩。","source":"Futurum, Synopsys Q3 FY 2026: AI Design Demand Drives EDA Growth","url":"https://futurumgroup.com/insights/synopsys-q3-fy-2026-ai-design-demand-drives-eda-growth/","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261019","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Ansys 整合的 Multiphysics Fusion 目前處於早期部署，預期自 FY2027 起貢獻 EDA 成長；風險面提及中國出口限制與 Ansys 整合複雜度。","source":"Nasdaq, SNPS Q3 Earnings Call Highlights EDA Acceleration, Outlook Raised","url":"https://www.nasdaq.com/articles/snps-q3-earnings-call-highlights-eda-acceleration-outlook-raised","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 的 Jay Vleeschhouwer 預期 EDA 產業成長延續至 2027，但尚無全產業 2027 預測，只有 Cadence 與 Synopsys 個別預測（兩家合計近四分之三產業）。","source":"SEMI taxonomy page","url":"https://www.semi.org/en/taxonomy/term/73136","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261019","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FTC 對 Synopsys／Ansys 合併要求依同意令剝離資產（光學、光子、RTL 功耗分析三市場），資產交 Keysight；德文報導稱最終令於 2025-10-17 定案，FTC 頁面仍標 Pending","source":"FTC: synopsis inc ansys inc matter","url":"https://www.ftc.gov/legal-library/browse/cases-proceedings/synopsis-inc-ansys-inc-matter","excerpt":"The Federal Trade Commission will require Synopsys, Inc. and Ansys, Inc., under a proposed consent order, to divest certain assets to resolve antitrust concerns surrounding their $35 billion merger.","as_of":"2025-10-17","retrieved_at":"20261019","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"歐盟執委會 2025 年 1 月附剝離條件核准 Synopsys 收購 Ansys；英國 CMA 同樣以剝離方案達成結果","source":"TechCrunch: EU approves $35B Synopsys and Ansys merger subject to divestment conditions","url":"https://techcrunch.com/2025/01/10/eu-approves-35b-synopsys-and-ansys-merger-subject-to-divestment-conditions","excerpt":null,"as_of":"2025-01-10","retrieved_at":"20261019","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025-05-29 Synopsys received a BIS letter imposing a license requirement on certain EDA exports to China; it halted new China orders; restrictions were lifted in July 2025.","source":"Synopsys FY2025 ARS (SEC) / TrendForce / DCD search summaries","url":"https://www.sec.gov/Archives/edgar/data/883241/000088324126000010/snps-2026ars.pdf","excerpt":null,"as_of":"2025-05-29","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 annual report says Synopsys expects a challenging near-term environment, including in China, due to macroeconomic factors and Trade Restrictions.","source":"Synopsys Form ARS FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/883241/000088324126000010/snps-2026ars.pdf","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Feb 2026 (exact day not in snippet): Synopsys guided Q2 revenue $2.23-2.28B, below consensus $2.24B, citing China export restrictions preventing customers from starting new design projects; shares fell >5% after hours.","source":"Techleap feed / Yahoo Finance summary of Synopsys guidance","url":"https://finder.techleap.nl/news/feed/synopsys-shares-fall-5-as-china-export-curbs-dampen-q2-revenue-outlook","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261019","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"China customers were about 10% of quarterly revenue as of quarter ending April 2025 (third-party summary).","source":"Visible Alpha, Synopsys to see China revenue drop 16% YOY amid US export curbs","url":"https://visiblealpha.com/?p=36489","excerpt":null,"as_of":"2025-06-01","retrieved_at":"20261019","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K: 貿易政策／關稅變動至今未對業務、經營結果或財務狀況造成重大影響；FY2026 可能有新關稅或其他貿易政策變動","source":"Synopsys Form 10-K FY2025 (fiscal year ended 2025-10-31)","url":"https://www.sec.gov/Archives/edgar/data/883241/000088324125000028/snps-20251031.htm","excerpt":"These changes in global trade policy have not had a material impact on our business, operating results or financial condition to date.","as_of":"2025-10-31","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2023 10-K 風險因素列入中台關係變化，屬海外政經不確定性之一","source":"Synopsys Form 10-K FY2023","url":"https://www.sec.gov/Archives/edgar/data/883241/000088324123000019/snps-20231031.htm","excerpt":"changes in China-Taiwan relations","as_of":"2023-10-31","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K：受關稅／出口限制影響的客戶可能自行開發產品或替換 Synopsys 方案","source":"Synopsys Form 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/883241/000088324124000024/snps-20241031.htm","excerpt":"Current and potential customers who are concerned or affected by such tariffs or restrictions may respond by developing their own products or replacing our solutions","as_of":"2024-10-31","retrieved_at":"20261019","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"ZeBu Cloud 為 Synopsys 資料中心代管的模擬驗證服務（雲端服務集中於自家資料中心）","source":"Synopsys ZeBu Cloud 產品頁","url":"https://www.synopsys.com/verification/solutions/zebu-cloud-solution.html","excerpt":"hosts emulation capacity in the Synopsys data center","as_of":"2026-10-19","retrieved_at":"20261019","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 FY2026 營收 $2.477B（去年同期 $1.740B）；Design Automation 表現優於預期，Design IP 回到年增；全年營收指引中點上調至約 $9.715B，CFO 預期 EDA 雙位數成長","source":"Synopsys Q3 FY2026 earnings press release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0000883241/000119312526368620/d157153dex991.htm","excerpt":null,"as_of":"2026-08-26","retrieved_at":"20261019","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 FY2026 Design IP 營收 $454.2M，年減 5.8%；Q3 回到年增。全年指引上調 $50M 至 $9.69–9.74B，由 Design Automation（EDA）帶動；非 AI 設計活動近兩季趨穩","source":"Futurum Group, Synopsys Q3 FY 2026: AI Design Demand Drives EDA Growth","url":"https://futurumgroup.com/insights/synopsys-q3-fy-2026-ai-design-demand-drives-eda-growth/","excerpt":"Synopsys raised full-year revenue guidance by $50 million at the midpoint to $9.69 billion-$9.74 billion, driven by Design Automation strength led by EDA.","as_of":"2026-08-27","retrieved_at":"20261019","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"管理層表示 AI 變現、自主工作流、IP Factory Two、與 Ansys 聯合方案等新項目預期在 FY2027 貢獻較明顯；未找到 2027 正式量化需求預測","source":"Futurum Group, Synopsys Q3 FY 2026 / Q2 FY 2026 coverage","url":"https://futurumgroup.com/insights/synopsys-q3-fy-2026-ai-design-demand-drives-eda-growth/","excerpt":null,"as_of":"2026-08-27","retrieved_at":"20261019","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"SemiAnalysis EDA primer：CY2025 Synopsys（含 Ansys）營收約 $8B、Cadence $5.30B、Siemens EDA 約 $2.2–2.5B；三大廠合計市佔逾 85%；EDA 年複合成長 13% vs 半導體 R&D 7%","source":"SemiAnalysis, EDA Market Primer","url":"https://newsletter.semianalysis.com/p/eda-market-primer","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261019","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"Barchart 引述分析師估計 Cadence 與 Synopsys 各約 30% 市佔","source":"Barchart, Cadence spikes post earnings with strong interest in AI products","url":"https://www.barchart.com/story/news/349303/cadence-spikes-post-earnings-with-strong-interest-in-ai-products","excerpt":"Analysts estimate that Cadence and Synopsys (NASDAQ: SNPS) each hold around 30% market share in this space.","as_of":"2026-07-01","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Trefis 9月評論認為「AI 自行設計晶片而繞過 EDA 工具」的威脅可能存在但緩慢，已公布數字尚未證實；管理層仍在摸索 AI agent 以訂閱或用量計價。","source":"Trefis: What Happens To Synopsys Stock If AI Learns To Design Chips Without It?","url":"https://www.trefis.com/articles/616135/what-happens-to-synopsys-stock-if-ai-learns-to-design-chips-without-it/2026-09-22","excerpt":null,"as_of":"2026-09-22","retrieved_at":"20261019","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Synopsys 於 DAC 2026 與 NVIDIA 發布自主 agent 工作流；驗證 agent 宣稱達到可驗證 RTL 最高快 50 倍、覆蓋率再增 20%，除錯收斂流程縮短最多 40%（公司自述，無獨立基準），AMD 使用中。AI 由 Synopsys 自家嵌入工具。","source":"Synopsys press release 2026-07-26","url":"https://news.synopsys.com/2026-07-26-Synopsys-Showcases-Comprehensive-Autonomous-Engineering-Workflows-from-Silicon-to-Systems,-Developed-with-NVIDIA-Technology","excerpt":null,"as_of":"2026-07-26","retrieved_at":"20261019","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Pitchgrade 筆記指 AI 多半嵌入 EDA 工具而非取代；真正風險在設計服務與工具使用強度（每案工程師減少可能縮小授權池）。數字未對照一手來源。","source":"Pitchgrade: synopsys ai margin pressure","url":"https://www.pitchgrade.com/research/synopsys-ai-margin-pressure","excerpt":null,"as_of":"2026-09-22","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"管理層在 Q2 FY26 財報電話會議表示正探索在既有訂閱之上加收 AI agent 用量（consumption）費用，處於與客戶早期探索階段；Trefis 稱 8 月管理層列出三種付費方式：訂閱 agent、訂閱工作流程、按用量計費。","source":"Trefis, How Do OpenAI And AWS Deals Reshape Synopsys's Design Automation Outlook?","url":"https://www.trefis.com/articles/617384/how-do-openai-and-aws-deals-reshape-synopsyss-design-automation-outlook/2026-10-02","excerpt":"The current thinking, and we're in early exploration with customers, is how do we build from the subscription license to a subscription-plus-consumption model.","as_of":"2026-10-02","retrieved_at":"20261019","affects":["moat_trend","valuation","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Futurum 報導 2026-09-30 Investor Day：與 Amazon 簽署逾 10 億美元的應用最佳化 IP 協議、與 OpenAI 合作；新模式以訂閱、用量、成果分成變現。（次級來源，數字需對照公司原始資料）","source":"Futurum, Synopsys Investor Day 2026 Turns EDA Into a Royalty and AI Model Revenue Share Business","url":"https://futurumgroup.com/?p=96308","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261019","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 FY26 資料顯示 Ansys 通路營收改採總額（gross-basis）會計，FY26 營收指引橋中此項影響約 +6,000 萬美元；屬報表呈現效果，非通路夥伴流失證據。","source":"Synopsys Q2 FY2026 Financial Supplement / fn2.ai SNPS FY2026 Q2","url":"https://s201.q4cdn.com/778493406/files/doc_earnings/2026/q2/supplemental-info/Synopsys-Q2-FY2026-Financial-Supplement.pdf","excerpt":null,"as_of":"2026-05-31","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026 年 4–5 月 Synopsys 通知客戶其晶圓廠製程控制軟體已 end of life、僅維持維護，資源轉向 AI 驅動 EDA。","source":"Crypto Briefing, Synopsys exits chip fab software to go all-in on AI-driven design","url":"https://cryptobriefing.com/synopsys-exits-fab-software-ai-design/","excerpt":null,"as_of":"2026-05-31","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 彙整（2026 年 9 月初）：17 位分析師，15 買 2 賣，平均目標價 $569（聚合站引述價 $393.84，不作現價使用）","source":"Benzinga SNPS analyst consensus (via search summary)","url":"https://kr.benzinga.com/quote/SNPS/price-targets","excerpt":"Analyst Consensus — 17 Analysts 15Buy 2Sell Consensus RatingBuy# Analysts17Avg. Consensus PT$569","as_of":"2026-09-05","retrieved_at":"20261019","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 8 月 11 日快照：20 位分析師，平均目標價 $571，高 $675、低 $425","source":"Benzinga SNPS price targets (via search summary)","url":"https://kr.benzinga.com/quote/SNPS/price-targets","excerpt":"Analyst Consensus Buy Short Interest 2.9% short float","as_of":"2026-08-11","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Walnut Invest 2026 年 7 月：25 位分析師平均目標價 $564.43，區間 $414.77–$650，18 買 5 持有 1 賣","source":"Walnut Invest SNPS forecast","url":"https://walnutinvest.com/stocks/snps/forecast","excerpt":"25 analysts covering Synopsys (SNPS) carry an average price target of $564.43 as of July 2026","as_of":"2026-07-31","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-08-27 Mizuho 目標價由 $600 降至 $550；Baird 升至 Outperform、目標價 $560","source":"搜尋摘要彙整（Mizuho／Baird 個別調整）","url":"https://kr.benzinga.com/quote/SNPS/price-targets","excerpt":null,"as_of":"2026-08-27","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 FY26 財報後公司上調全年指引（營收 $9.625–9.705B）；處分處理器 IP 業務使營收中點減約 $40M；來源間 EPS 區間不一致","source":"TIKR／Nasdaq Q2 earnings call 摘要（搜尋結果）","url":"https://www.tikr.com/blog/synopsys-stock-q2-beat-full-year-raise-and-an-elliott-catalyst-the-street-calls-conservative","excerpt":null,"as_of":"2026-05-20","retrieved_at":"20261019","affects":["triggers","valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 FY26 再度上調全年指引：營收 $9.69–9.74B、non-GAAP EPS $15.04–15.10（次級來源 TIKR／Traders Union，未對照 8-K 原文）","source":"Traders Union: Synopsys reports strong Q3 results and raises 2026 guidance","url":"https://tradersunion.com/news/companies/show/3122068-synopsys-stock-edges-higher-to/","excerpt":null,"as_of":"2026-09-10","retrieved_at":"20261019","affects":["triggers","valuation"],"status":"ok"},{"id":"capital_markets_pricing#6","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 財報後股價下跌約 9.2%（量約 3 倍），理由為 IP 復甦、Ansys 成長持續性與中國出口限制疑慮（單一聚合來源）","source":"FN2 SNPS FY2026 Q2","url":"https://fn2.ai/earnings/snps/2026-q2","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"Kim v. Synopsys (No. 3:25-cv-09410, N.D. Cal.) 證券集體訴訟，class period 2024-12-04 至 2025-09-09，依 Exchange Act 10(b)/20(a)；起因為 FQ3 2025 財報後股價單日跌約 36%；另有 New England Teamsters Pension Fund v. Synopsys (No. 25-cv-10201) 於 2025-10-31 提起，後續修正訴狀增列與併購相關的 Securities Act 主張。原告律所指控未證實。","source":"Hagens Berman / Labaton / Levi Korsinsky 新聞稿（Barchart、hbsslaw.com）","url":"https://www.hbsslaw.com/press/synopsys-inc-snps-securities-class-action/synopsys-inc-snps-faces-securities-class-action-amid-q325-results-revealing-ip-business-problems-hagens-berman","excerpt":null,"as_of":"2025-10-31","retrieved_at":"20261019","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Synopsys 於 2025-07-17 宣布完成對 Ansys 的收購（約 $350 億；每股 Ansys 換 $199.91 現金＋0.3399 股 SNPS；部分以 $100 億債務融資；監管要求出售光學解決方案事業群予 Keysight 等）。完成日距今略超 12 個月，但為本輪核心 M&A 背景。搜尋未見 2026 年新的併購公告。","source":"Synopsys 新聞稿（Barchart）：Synopsys Completes Acquisition of Ansys","url":"https://www.barchart.com/story/news/33466864/synopsys-completes-acquisition-of-ansys","excerpt":null,"as_of":"2025-07-17","retrieved_at":"20261019","affects":["moat_trend","valuation","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Synopsys 於 2025-07-17 完成收購 Ansys（約 $350 億，現金＋股票，含約 $100 億債務融資；光學事業群出售予 Keysight）。搜尋未見 2026 年新併購。","source":"Synopsys 新聞稿（Barchart）","url":"https://www.barchart.com/story/news/33466864/synopsys-completes-acquisition-of-ansys","excerpt":null,"as_of":"2025-07-17","retrieved_at":"20261019","affects":["moat_trend","valuation","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Kim v. Synopsys (No. 3:25-cv-09410, N.D. Cal.)，class period 2024-12-04 至 2025-09-09，指控未揭露 AI 客製化侵蝕 Design IP 經濟性；股價 2025-09-10 單日跌 35.8%。另有 No. 25-cv-10201（2025-10-31）。尚無法院裁決資訊。","source":"Hagens Berman 新聞稿","url":"https://www.hbsslaw.com/press/synopsys-inc-snps-securities-class-action/synopsys-inc-snps-faces-securities-class-action-amid-q325-results-revealing-ip-business-problems-hagens-berman","excerpt":null,"as_of":"2025-10-31","retrieved_at":"20261019","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 8 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SNPS","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.38,"operating_margin_pct":11.03,"fcf_margin_pct":29.18,"rd_intensity_pct":30.6},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS","as_of":"TTM ending 2026-07-31（4季加總）"},"is_subject":true},{"name":"CDNS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":85.87,"operating_margin_pct":30.82,"fcf_margin_pct":28.64,"rd_intensity_pct":33.02},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ARM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":97.54,"operating_margin_pct":17.3,"fcf_margin_pct":28.55,"rd_intensity_pct":57.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"QCOM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":54.23,"operating_margin_pct":23.28,"fcf_margin_pct":23.64,"rd_intensity_pct":22.45},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"688521.SH","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688521.SH"},"note":"quarterly_income_stmt 無資料"}],"subject":"SNPS"},"financial_history":{"ticker":"SNPS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-10-31","revenue":4615714000.0,"revenue_yoy_pct":null,"gross_margin_pct":80.54,"operating_margin_pct":25.13,"net_income":984594000.0,"diluted_eps":6.29,"free_cash_flow":1599818000.0,"fcf_margin_pct":34.66,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-10-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-10-31","revenue":5318014000.0,"revenue_yoy_pct":15.22,"gross_margin_pct":80.62,"operating_margin_pct":24.94,"net_income":1229888000.0,"diluted_eps":7.92,"free_cash_flow":1511452000.0,"fcf_margin_pct":28.42,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-10-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-10-31","revenue":6127436000.0,"revenue_yoy_pct":15.22,"gross_margin_pct":79.68,"operating_margin_pct":22.13,"net_income":2263380000.0,"diluted_eps":14.51,"free_cash_flow":1267529000.0,"fcf_margin_pct":20.69,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-10-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-10-31","revenue":7054178000.0,"revenue_yoy_pct":15.12,"gross_margin_pct":76.98,"operating_margin_pct":12.97,"net_income":1332220000.0,"diluted_eps":8.04,"free_cash_flow":1349154000.0,"fcf_margin_pct":19.13,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-10-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SNPS/SNPS_Q3_2026_Earnings_Call_20260826.md）

# Q3 2026 Earnings Call
**Synopsys, Inc.** | Earnings Calls | 2026-08-26

**Operator** (Operator):
Ladies and gentlemen, welcome to the Synopsys earnings conference call for the third quarter fiscal year 2026. [Operator Instructions] As a reminder, today's call is being recorded. At this time, I would like to turn the conference over to Tushar Jain, Vice President. Please go ahead.

**Tushar Jain** (Executives):
Good afternoon, everyone. Welcome to Synopsys' Third Quarter Fiscal Year 2026 Earnings Call. With us today are Sassine Ghazi, President and CEO of Synopsys; and Shelagh Glaser, CFO.
Before we begin, I'd like to remind everyone that during the course of this conference call, Synopsys will discuss forecasts, targets and other forward-looking statements regarding the company and its financial results. While these statements represent our best current judgment about future results and performance as of today, our actual results are subject to many risks and uncertainties that could cause actual results to differ materially from what we expect. In addition to any risks that we highlight during this call, important factors that may affect our future results are described in our most recent SEC reports and today's earnings press release.
In addition, we will refer to certain non-GAAP financial measures during the discussion. Reconciliations to their most directly comparable GAAP financial measures and supplemental financial information can be found in the earnings press release, financial supplement and 8-K that we released earlier today. All of these items, plus the most recent investor presentation, prepared remarks and Investor Day information can be found on our website at www.synopsys.com.
With that, I'll turn the call over to Sassine Ghazi.

**Sassine Ghazi** (Executives):
Good afternoon. Synopsys delivered an outstanding third quarter with revenue, non-GAAP operating margin and EPS all exceeding the high end of guidance. These results reflect broad-based strength, including outperformance in EDA and Ansys and continued growth in IP. We are raising our full year revenue, non-GAAP operating margin and EPS guidance. In addition, we expect EDA growth to accelerate in Q4 and to deliver double-digit growth for the full year.
The key takeaway from Q3 is that the fundamentals across our portfolio are strengthening. EDA is accelerating. Design IP has returned to growth and Ansys is performing strongly while beginning to create new growth opportunities across the combined portfolio. This quarter marked 1 year since the Ansys acquisition close. And in Q3, we launched our first joint Synopsys and Ansys solutions, Multiphysics Fusion.
I want to recognize our global team for executing with focus and agility to integrate our world-class capabilities. The combination has strengthened our competitive position, expanded our opportunity and enabled us to deliver differentiated solutions addressing the physics challenges of modern chip design. Industry trends are aligned to our strategy and our strengths as the leading provider of engineering solutions from silicon to systems. Unprecedented design complexity driven by the demands of AI is fueling the need for the IP and design solutions necessary to deliver next-generation AI compute, infrastructure and physical AI systems. These trends are evident in our Q3 results. 
Starting with Design Automation, which achieved healthy growth in Q3, underpinned by strength in EDA, including record hardware revenue. We expect this momentum to continue with EDA growth accelerating to double digits in Q4 and for the full year.
Design activity is highest among AI and high-performance compute customers, developing increasingly specialized chips with multi-die architectures, more complex packaging and system requirements. These are all areas where Synopsys leads. AMD's recently launched Instinct MI455X GPU is a good example. To deliver this highly sophisticated new product series, AMD leveraged Synopsys' 3DIC Compiler, the industry's only exploration-to-sign-off platform for multi-die and advanced package co-design and optimization.
The complex software and system requirements of AI compute also drive demand for our hardware-assisted verification solutions. We secured 12 new and 66 repeat HAV customer wins in the quarter. 
As I mentioned, the launch of Multiphysics Fusion was a major EDA milestone in Q3 and creates a new growth opportunity for Synopsys. Multiphysics Fusion combines Synopsys and Ansys technology in the industry's only solution with thermal analysis fully integrated into the chip design flow. Customers, including NVIDIA, Cisco, MediaTek and Samsung Foundry have validated up to 10x faster design closure and 3x faster runtime. This drives greater value for our customers and also for our products. We expect these add-on capabilities to begin contributing to EDA growth in 2027.
Agentic AI is another growth vector for Synopsys, and we demonstrated strong progress in Q3. At the DAC conference, with NVIDIA, we showcased a fully autonomous long-running design verification agent that can orchestrate the entire chip verification cycle and deliver up to 50x faster time to validated RTL while achieving 20% additional coverage improvement. With Microsoft and AMD, we introduced the first autonomous EDA workflows on Microsoft Discovery that can automate debug, implementation and design closure. Early engagements show up to 40% reduction in debug cycle time, saving weeks of engineering effort while improving design quality.
We're seeing strong customer interest in our agentic AI platform with more than 30 active customer engagements underway. Early feedback has made clear that as these agents take on more engineering work, they orchestrate our underlying EDA tools at a significantly higher rate. That allows customers to run more design and verification workloads, creating an incremental growth opportunity for Synopsys as we capture our fair share of the value that these agentic workflows and foundational tools provide for our customers.
Turning to Ansys. One year into our integration, Ansys continues to see strong demand. From semis to aerospace to industrial and more, companies are embracing digital engineering. Across industries, Ansys simulation is accelerating innovation while reducing development risk and cost. For example, a leading automaker is using Ansys SimAI to achieve roughly 98% prediction accuracy and move crash analysis to near real time.
And a leading heavy equipment manufacturer achieved more than 10x faster motor design. We're applying AI to extend our S&A leadership and further automate the simulation of complex systems. This includes expanding our portfolio of GPU-accelerated Ansys applications. And in Q3, our largest Ansys deal was for GPU-accelerated Ansys CFD to support a company-wide digital twin at a multinational electronics component maker.
Turning to Design IP, which grew sequentially and year-over-year on broad AI infrastructure demand. As AI drives demand for higher bandwidth, faster connectivity and more complex system architectures, our interface, memory and die-to-die IP portfolio sits at the center of the stack. And our Q3 results showed it.
We won more than 95% of PCIe 7 opportunities, including a subsystem win at a marquee enterprise storage customer. In LPDDR6, silicon proven across multiple nodes and foundries, we've secured 25 design wins year-to-date. Our die-to-die business is on pace to double year-over-year, and we now have more than 100 cumulative design wins. The industry continues to rely on Synopsys for silicon-proven quality and unrivaled scale.
Our standards-based build once, sell many IP model remains foundational to our growth strategy. We'll continue to invest and grow this business, what I call Factory 1, which benefits from strong chip start activity and solid traction across industries. For example, in automotive, we've sustained a 90% plus design win rate for 3 consecutive quarters as ADAS platforms refresh on to 5- and 3-nanometer. In mobile, consumer and edge AI, our USB IP has now crossed $2 billion in lifetime bookings with Tier 1 design wins already moving to the leading-edge node. As AI expands beyond digital infrastructure into physical products, demand for silicon will continue to expand, providing a tailwind for our standards-based IP business. 
The higher growth opportunity in IP lies with a growing set of AI customers who are asking for deeper collaboration and IP solutions optimized to their specific workloads and architectures. To meet that demand, we are expanding into differentiated IP subsystems and enabling custom silicon solutions. Customers ranging from hyperscalers, ASIC vendors, foundries and classic semiconductors want to partner with Synopsys to accelerate their chip development efforts and leverage our IP and engineering expertise to build increasingly differentiated custom silicon.
This is our Factory 2 model for customized IP. It moves us up the value chain from licensing alone to licensing plus royalties and positions us to capture the fast-growing custom silicon opportunity. This is a large focus, and we are making strong progress. We are in active discussions with multiple Factory 2 customers, and I look forward to sharing more at Investor Day.
To summarize, I want to thank the entire Synopsys team for their continued focus, innovation and execution. Q3 reinforced the strength of our strategy and our confidence in a strong finish to the year. AI is driving demand for advanced silicon, system-level engineering and AI-powered design. Our leadership portfolio positions us to capture a greater share of R&D investment across industries. We remain focused on translating our technology leadership into sustainable growth and margin expansion.
Now over to Shelagh.

**Shelagh Glaser** (Executives):
Thank you, Sassine. We delivered an outstanding Q3, achieving revenue of $2.477 billion, non-GAAP operating margin of 41.6% and non-GAAP EPS of $3.91, all beating the high end of our guidance range. With broad-based strength across the business, the revenue outperformance was driven by EDA as well as strength in the Ansys business.
Backlog remains very strong at $10.9 billion, modestly down quarter-over-quarter due to the divestiture of the Processor IP Solutions business that closed in Q3. With the strength in Q3, strong cash flow generation and continued momentum into Q4, we are raising our full year revenue, non-GAAP operating margin, EPS and cash flow guidance.
I'll now review our third quarter results. All comparisons are year-over-year unless otherwise stated. We generated total revenue of $2.477 billion, up approximately 42%, including Ansys revenue of approximately $711 million.
As Sassine noted, 1 year into the combination, Ansys continues to perform strongly. We are also ahead of the schedule on the cost synergy commitments we made at close and have repaid the term loans earlier than planned.
Total GAAP costs and expenses were $2.119 billion with GAAP earnings per share of $2.84. Q3 GAAP EPS includes a gain associated with the sale of the Processor IP Solutions business that closed in the quarter. Total non-GAAP costs and expenses were $1.446 billion, on the lower end of our guided range, as we continue to improve operational efficiency and deliver Ansys cost synergies ahead of schedule, resulting in non-GAAP operating margin of 41.6%. Non-GAAP earnings per share were $3.91, ahead of our guidance, underscoring our strong operational execution in the quarter.
Now on to our segments. Design Automation segment revenue was approximately $2 billion. As a reminder, this excludes the Optical Solutions Group, which was divested in Q4 '25. Within the Design Automation segment, Q3 EDA revenue increased 8.5% year-over-year, reflecting robust EDA software performance and another record quarter for hardware-assisted verification solutions. Design Automation adjusted operating margin was 45.2%.
The Design IP segment returned to growth with revenue of $474 million, up approximately 11% year-on-year. Consistent with our outlook, this represents continued sequential growth in the IP segment as we've repositioned the portfolio to focus on the highest value opportunities. Design IP adjusted operating margin was 26.5%.
Turning to cash. Free cash flow was $746 million in Q3, and we ended the quarter with cash and short-term investments of $3.6 billion. Total debt at the end of Q3 was approximately $10 billion.
Now to guidance for the full year. We are raising our total revenue guidance by $50 million at the midpoint, driven by strength in Design Automation segment led by EDA. As Sassine stated, momentum in EDA remains strong, and we expect double-digit organic EDA revenue growth in Q4 and for the full year 2026. We continue to expect the IP business to grow sequentially in Q4. This results in a revenue range of $9.69 billion to $9.74 billion. Within that, Ansys revenue contribution is expected to be approximately $2.98 billion, up $20 million versus our prior guidance.
Next, expenses. Total GAAP costs and expenses are expected to be between $8.667 billion and $8.742 billion. This includes an increase in expected charges for fiscal year 2026 in relation to our previously announced restructuring program as we continue to accelerate our committed synergies.
Total non-GAAP costs and expenses are expected to be between $5.67 billion and $5.70 billion and non-GAAP operating margin of 41.5% at the midpoint, a 50 basis point raise to our previous guidance. GAAP earnings are expected to be between $3.84 to $4.08 per share. We expect non-GAAP earnings of $15.04 to $15.10 per share, a $0.31 increase at the midpoint from our prior guidance due to higher revenue and increased operational efficiency.
We are raising our cash flow from operations guidance by $500 million to approximately $2.8 billion on strong cash collections and reducing our CapEx guidance to approximately $225 million, resulting in free cash flow of approximately $2.6 billion, an increase of $600 million versus our previous guidance.
Now to targets for the fourth quarter: total revenue between $2.53 billion and $2.58 billion, total GAAP costs and expenses between $2.225 billion and $2.3 billion, total non-GAAP cost and expenses between $1.45 billion and $1.48 billion, GAAP earnings of $0.60 to $0.85 per share, and non-GAAP earnings of $4.10 to $4.16 per share. Our press release and financial supplement include additional targets and GAAP to non-GAAP reconciliations.
Thanks to our global Synopsys team for another strong quarter. These results reflect strong execution across the business, continued demand for our technology and disciplined operating performance as we build the foundation for the next phase of growth. We look forward to seeing many of you at our September Investor Day to discuss the compelling long-term opportunity we have as a mission-critical partner for our customers.
With that, I'll turn it over to the operator for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Jason Celino with KeyBanc Capital Markets.

**Jason Celino** (Analysts):
Really good results here. I think what really stuck out to me was the 8% EDA growth, which was stable with last quarter despite the harder comp. You mentioned it's supposed to accelerate to double digits in Q4 and the full year. I mean, how would you describe what's driving that incremental acceleration? Is it design start activity? Is it agentic? Is it just better monetization strategies? Just help us understand.

**Sassine Ghazi** (Executives):
Thanks, Jason, for the question. Yes, we are very excited about the overall performance in EDA and the acceleration to wrap up the year with double-digit growth, exactly what we have committed to in terms of our segment growth. What's driving the increase in confidence in our business in EDA is driven by multiple factors, the complexity of chip design, the move to advanced package 3DIC, the example I mentioned in my prepared remarks like an AMD expansion and use of 3DIC Compiler, and there are a number of other customers that are designing these advanced package are using our technology.
AI is definitely a tailwind. As customers are rethinking of how to reengineer their chip design engineering, it's requiring different methods for that engineering. So that's driving another tailwind for us. And hardware, we had a record revenue year on hardware. So all in all, that 8-plus percent is organic growth for EDA that we're fairly excited about.

**Shelagh Glaser** (Executives):
Yes. And I'd just point out, Jason, that the 8.5% Q3 EDA growth that you saw was against a really tough compare. Q3 '25 was 16%. And so as Sassine said, it really just shows the strength of the business to be able to perform against that tough compare and then have the full year continue to have double digit.

**Jason Celino** (Analysts):
Yes. And then, Sassine, you mentioned something. You talked about your customers having to reengineer their processes. We're seeing a lot of innovation happening. Everyone always talks about these new AI models. I think yesterday, there was an example. OpenAI talked about the development of their new chip. They talked about using their own AI models to accelerate the design process.
Maybe can you speak to when you hear examples like this, because a lot of your customers have used their own models in the past, what is involved in the reengineering of a design process? How much is supplemental or incremental or replacement of something that might be existing? I don't know if that makes sense but...

**Sassine Ghazi** (Executives):
Yes, of course, of course. Yes. Thank you for the question. For at least 1.5 years now to 2 years, we've been talking about how AI is reshaping how engineering is done. The investment that Synopsys has been making and leading in delivering agent engineers to our customers in rethinking the workflow, including AI models that will absolutely participate and contribute to that reengineering of engineering, in every case, the underlying requirement is more and more and more of our software. Because if you're using an AI model or agents that the customer is developing, it doesn't matter. You still need the ground truth physics in order to -- for that model to be able to operate with confidence and delivering to the best outcome.
So the example that you mentioned actually is a very good example and a great opportunity for Synopsys on the EDA front. Not to mention, it's a huge opportunity on the IP as well because that's rethinking the whole architecture as you customize the silicon.

**Operator** (Operator):
Your next question comes from the line of Joe Vruwink with Baird.

**Joseph Vruwink** (Analysts):
I wanted to go back a few years, but at your 2024 Investor Day, you shared an outlook back then around how 30% of EDA software demand might end up coming from multi-die efforts by next year. I'm curious how that figure might be tracking and maybe what you see after 2027. I think we all appreciate there's been quite a lot of recent attention even this week on HBM. How might EDA content change for you when thinking about DRAM processes moving to logic, that sort of thing? And is it actually strengthening maybe relative to what you thought a few years ago?

**Sassine Ghazi** (Executives):
Yes, Joe, actually, that forecast has accelerated. As I mentioned in the prepared remarks as well, the die-to-die wins that we've had in the last 12 months have doubled. And the reason for that is this whole advanced package and 3DIC architecture. That drives a significant opportunity in IP. Die to die is one example; then, of course, all the other interfaces that are required to stitch the system together as a final product at our customer.
And on the EDA side is 3DIC Compiler, and this is where the emphasis of the joint solution with Ansys is essential. You cannot build these systems without taking into account physics, thermal, structure, fluid into the chip design phase. So the 30% back then was the figure we thought was a stretch, but it absolutely accelerated given all the investments our customers are making to build these efficient custom silicon.

**Joseph Vruwink** (Analysts):
Okay. That's great. I wanted to ask, the double-digit organic growth in EDA, if you think about splitting that up between software and hardware, is the performance in your software business where you would like it to be here at year-end? It seems like hardware has remained a very large and strong driver. I'm more curious about the software performance.

**Sassine Ghazi** (Executives):
We're very happy with the software component actually. Very, very pleased. The part that actually I'm most excited about is the delivery of our joint solution with Ansys. And that gives us the platform to deliver to where the future of engineering challenges is heading. As we just talked about, the advanced package, the need for physics into electronics gives us even the confidence to look at the trajectory and continue on delivering these double-digit growth.

**Operator** (Operator):
Your next question comes from the line of Charles Shi with Needham & Company.

**Yu Shi** (Analysts):
First thing, Shelagh, I have -- maybe this is for Sassine. I have a high level -- maybe a long-term question. Sassine, we know that going back probably more than 10 years, you played a very pivotal role in terms of infusing AI. I know back then, it was not a large language model, probably more like reinforcement learning type of AI into the Synopsys tool flows, DSO.ai, all those great products.
But AI has advanced so much over the last 10 years, especially last 3. So the question I constantly hear from investors is about is there any risk for AI to actually disrupt the commercial EDA business. And I think one -- at least one school of thought we're thinking, could there be an end-to-end, what they call, AI-native chip design that bypasses all the commercial EDA tools, especially maybe with some AI models trained by the commercial EDA generated synthetic data. Is that a real threat, in your opinion, to the overall EDA industry at all? Or where do you see where AI can be more substitutive or complementary to the commercial EDA business?

**Sassine Ghazi** (Executives):
Yes. Thank you, Charles. I don't need to go back or go as far as 10 years ago. You're right. Around 2017, we introduced and invested and saw great results with DSO.ai centered around reinforcement learning. If you look at the last 3 years, the focus was around copilot, generative AI, move to agents. Right now, we're talking about autonomous designs. As you start looking at autonomous workflow, the most important thing is accuracy and determinism. Customers will not invest hundreds of millions of dollars in a product without having the confidence that it's going to work.
The portfolio we have with the sign-off leadership is essential to building these autonomous workflows. We are participating with our customers on how to achieve an autonomous workflow. It's not like it's happening without our participation. We're proactively engaged with them to reengineer how they're looking at the future of engineering with AI being the center of that evolution.
I am not worried at all that, at some point that, that model can do the end to end without our participation because you have to remember, these models are not static. They're constantly changing. They constantly need to learn. So the opportunity is the opposite. It's not a threat. It's a significant demand for our software to train, to inference, to constantly enable that faster design to deal with the complexity, and we're at the center of it.

**Yu Shi** (Analysts):
Maybe, Sassine, on the agentic AI agent opportunities, how should we think about any uplift to the overall revenue growth, especially EDA growth? And can you give us an update on the changing the business model more to the subscription plus consumption, at least for the agents? Any discussion with your customers so far?

**Sassine Ghazi** (Executives):
Yes, number of engagements. Actually, to the first question you had, as our customers are exploring whether to use an agent from Synopsys or an agent plus -- from Synopsys plus their own agents to keep their special sauce inside their workflow, the customer workflow or the customer agent, the need is for more licenses. We are defining with our customers multiple ways on how to engage from a subscription of our agents, subscription of our workflow as well as a consumption measure as these agents and the new workflow is consuming more software.
We'll highlight more of how we're thinking how to model the long-term growth with this context that I just described in a few weeks, September 30. But absolutely, we're in advanced discussions with number of customers with different flavors of using their agents, our agents, a hybrid of both and multiple model optionality that they're thinking about.

**Operator** (Operator):
Your next question comes from the line of Lee Simpson with Morgan Stanley.

**Lee Simpson** (Analysts):
Great. Maybe just a couple of quick ones on IP actually. Maybe just preempting the Analyst Day. I wondered, Sassine, if you can maybe just give us a little bit of outline on the speed of shift to the Factory 2 opportunity you outlined with licensing and royalties.
And then secondly, it's been about a year, I think, since we've seen the Intrinsic ID acquisition. And I think at the time, you talked about security IP as being a new vector of growth in IP. Just wanted to hear if you could maybe outline the size of that opportunity, how you've seen engagements go and where in particular you think deployments will happen.

**Sassine Ghazi** (Executives):
Thank you, Lee. On Factory 2, actually, all you need to look at is the momentum in every hyperscaler investing and are at various stages of delivering their own custom silicon. These chips will not happen without our interface IP. These customers need our interface IP in order to build their own chips and to connect to the ecosystem, be it the memory provider or if they're using -- if they are investing in their XPU, but they need a networking chip from their supplier, connecting them together come through our interface IP. So that's the opportunity.
What we could see as well and the reason we started talking about Factory 2 is the need to customize these standards and to accelerate the delivery of these customizations. Synopsys is in a unique position given our scale and the knowledge, the skills, the market position to deliver on that customization and acceleration. We are in advanced discussions with number of these customers to change the business model from the traditional IP license plus some NRE to a license plus a royalty.
I look forward in a few weeks to, again, help you model what does that look like. But I cannot be more excited about the investment that we've made and the agility in pivoting in that direction while absolutely continue on leading and investing in Factory 1 because that's another significant opportunity that will continue.
As for security, the reason we started looking at the portfolio and we divested the processor IP is to focus on the areas of growth. Security is one of them. As you said, we don't split it out as a separate item, but we have a great market position in security and will only continue on becoming more and more important given you need to secure the chip not only at the software level, as much as you can do at the hardware level, and that's where our security portfolio comes in.

**Operator** (Operator):
Your next question comes from the line of Josh Tilton with Wolfe Research.

**Arsenije Matovic** (Analysts):
This is Arsenije on for Josh. Just, Sassine, first, you talked about seeing strong early customer interest in Multiphysics Fusion following the launch. And just historically, chip design and simulation often were kind of handled by different engineering teams and different workflows and tools. I guess when you're bringing thermal analysis directly into the design flow, how are customers structurally, I guess, approaching that convergence? Are you seeing those teams start to work more closely together and consolidate around more common workflows? Or does adoption still kind of require navigating distinct engineering teams and maybe separate budgets?

**Sassine Ghazi** (Executives):
Yes, you're absolutely right. These teams or the skills and expertise of engineering were separate domains. They had a different handshake as the design steps are moving from the synthesis to the physical design to sign-off, et cetera. The requirements to have codesign is essential to reduce margin and deliver to these competitive products. So absolutely, leading customers are requiring to take thermal into account during the design implementation to take structure, stress as they're building these 3DIC into the architecture of the chip, not only the synthesis or the implementation of the multiple chiplets.
So yes, absolutely. And this is where we have invested, that the implementation engineer that's sitting in the upfront part of the design flow are able without too much effort to be able to bring in sign-off accuracy early in the design flow. And that's exactly where we see the opportunity of the combined portfolio and delivering to the fusion of physics with electronics.
From a budget point of view, by the way, the second part of your -- I'm sorry, from the second part of your question, from a budget point of view, as we have committed 1 plus 1 will be greater than 2. What it means even if it's coming from an EDA budget, the joint solution will capture an upside in revenue to the existing separate point tools.

**Arsenije Matovic** (Analysts):
Got it. That's helpful. And then just, Shelagh, just clarifying just 1 topic specifically on Ansys, the raise $20 million to the $2.98 billion. Last quarter, you helped us with $12.5 million contribution from that accounting dynamic and it was $60 million for the full year. Is it still $60 million for the full year and that raise on that $20 million increase in Ansys is just core upside from good execution there?

**Shelagh Glaser** (Executives):
Yes. So last quarter, we talked about the accounting change, and so we made that accounting change, and we'll be making that accounting change and in the guidance that we're giving incorporates that. So we're seeing strength in the Ansys business, including the channel business.

**Arsenije Matovic** (Analysts):
Got it. And what was it, I guess, in Q3, for Ansys' accounting change and it's still $60 million for the full year? Or is it a different number this time?

**Shelagh Glaser** (Executives):
It's still in that same range for the full year.

**Arsenije Matovic** (Analysts):
Got it. And the quarter, it was $12.5 million or...

**Shelagh Glaser** (Executives):
We didn't disclose the in-quarter.

**Operator** (Operator):
Your next question comes from the line of Joe Quatrochi with Wells Fargo.

**Joseph Quatrochi** (Analysts):
You talked about a tale of 2 markets with AI versus non-AI and EDA. I'm just wondering if the acceleration that you're seeing, is AI becoming a larger piece or in offsetting kind of the non-AI? Or have you started to see also some acceleration from the non-AI part of your business as well?

**Sassine Ghazi** (Executives):
Yes, Joe, the -- so the reason for our assertion to begin with, what we do on a quarterly basis, that these are internal measures that we have is we track chip starts. And the reason we have a good coverage on design starts is our IP portfolio. There is no customer that is planning a new chip start that we don't engage very early on through our IP portfolio. And of course, EDA will follow. 
The observation is on the non-AI, in the last 2 quarters, it has stabilized. What it means was we were observing a slowdown in design start in the non-AI segment. In the last couple of quarters, stabilization, so it's not declining anymore. Now on the flip side for AI, where we have been seeing and continue on seeing an acceleration in design start, which is a great balance for the opportunity that we have.

**Joseph Quatrochi** (Analysts):
That's helpful. And then maybe as a follow-up, just wondering if you could give any puts and takes on the RPO. It was down a touch this quarter. Was there any impact from the divestiture? And did it come in as expected with your plan?

**Shelagh Glaser** (Executives):
Yes, it came in as expected. And as I said in my prepared remarks, the modest change is really due to the divestiture of the processor IP business that happened inside the quarter. As you recall, we were close to closing the deal when we did last earnings. It closed a few days after we did the earnings. So that's why you're seeing it this quarter.

**Operator** (Operator):
Your next question comes from the line of Siti Panigrahi with Mizuho.

**Sitikantha Panigrahi** (Analysts):
Sassine, it's really a good quarter. Congratulations. Going back to the Ansys and Synopsys, the integrated products that you launched. I think you talked about that Multiphysics Fusion is not expected to contribute to EDA growth until 2027. So can you talk about the adoption of pipeline trajectory that we should expect from now and then? And is that '27 contribution more likely to show up as an incremental EDA growth? Or as share gains from your Ansys simulation base? Any color like what you are seeing in terms of pricing benefit, value to the customer on that? That will be great.

**Sassine Ghazi** (Executives):
Yes. So from a value to the customer, the 10x faster design closure or a 3x faster SPICE accurate multiphysics timing, that is a significant value to customers. What does it mean for the customer? Less iteration, better design, faster. So our customers in these early engagements have validated and they're in early stages of deployment. The moment we move to production, which those customers will move to production, we'll start seeing the revenue upside.
As we've said from the beginning, FY '26, we will not have much contribution in the joint solution. It was a year of execution, delivering to these products. As we look at FY '27, absolutely, it will contribute to our growth in EDA. We are absolutely committed as well to the $400 million synergy in year 4. So as we meet in September, we'll be able to start talking about '27 and the longer-term contribution of this differentiated solution.

**Sitikantha Panigrahi** (Analysts):
That's helpful. And then a quick follow-up. I know Mike Ellow has been there now a few quarters. How is he driving the sales organization? Any kind of specific changes he is contemplating or has been working towards as you roll out this integrated product?

**Sassine Ghazi** (Executives):
Yes. Mike has been doing a great job in leveraging what the organization does incredibly well and the areas that we need to increase our investment from portfolio, go-to-market point of view, et cetera, et cetera. The priority as we look at FY '27 and beyond is how to engage the customers in the areas of differentiation and ensure we have the right investment with the customer. We're enabling the customers successfully so we capture the monetization opportunity. So Mike has been spending a lot of energy internally with the team to prepare the organization for IP Factory 2, for the AI monetization, for the joint solutions. All this is a significant time where Mike is spending as we look at '27 and beyond.

**Sitikantha Panigrahi** (Analysts):
He's a great hire.

**Sassine Ghazi** (Executives):
He is. We're happy having him.

**Operator** (Operator):
Your next question comes from the line of Jay Vleeschhouwer with Griffin Securities.

**Jay Vleeschhouwer** (Analysts):
Sassine, for you first. This may be an imperfect analogy. But how would you compare the prospective migration or adoption benefit of the new multiphysics cohort and cohorts to follow, might compare with the ICC to Fusion Compiler transition? That obviously didn't include Ansys component at the time, but that was your last big architectural or generational change in your stack. So how would you think this one now that it's underway might compare to that? And then a follow-up.

**Sassine Ghazi** (Executives):
Yes. Jay, thank you. Actually, a very good question. What we've done with Fusion was bringing our sign-off capability and strength into the design physical implementation phase because the customers at the time were having to iterate late stage to correlate or to sign off the chip. It's exactly the same here, but you're including physics.
Now the RedHawk, the HFSS, the rest of the portfolio of Ansys, how do you bring not only approximation into the design phase, how do you bring the actual engines into the design phase so you reduce iteration, you have a convergent flow, et cetera? The investment we made in the Fusion platform, because remember, the Fusion platform is not about bringing tools together with a common interface or a user interface. We made a significant investment at the data model level. So we -- so our R&D team can write code, optimize on the same exact infrastructure and data model. And that's where Shankar and team have been investing quite heavily from day 1 of the integration start to deliver to exactly the same value that we were able to build on with Fusion.

**Jay Vleeschhouwer** (Analysts):
Okay. Secondly, the reengineering of engineering concept that you've talked about now since Converge last year remains a very interesting concept and prospect for you and your customers. The question is what are the ingredients that customers need to make that work. Is it a set of variables or changes they need to make? Is there a single magic bullet that they can implement to make that happen? The demos that you did jointly, for example, at DAC with AMD and Microsoft around Discovery seemed quite interesting as perhaps a catalyst for some of those changes. So maybe talk about what actually has to happen for the whole reengineering thing to really happen.

**Sassine Ghazi** (Executives):
Yes. We talked about Fusion as an essential part to have the entire complete set from a spec all the way to sign-off. So that's an essential component that Synopsys has that complete set of assets. Now from bringing together a workflow that can leverages the AI speed from a copilot, generative AI all the way to autonomy is where we're putting significant investment and racing. The 2 demos we've done -- and thank you for mentioning the Microsoft, AMD, which was a demonstration of a full autonomous EDA workflow on the Microsoft Discovery. Think how powerful that is, where you can start from a spec and you have a cognitive layer that can orchestrate multiple tasks agents in order to deliver to the outcome of the spec.
At the same time, what we've done at DAC actually is a demonstration with NVIDIA on an autonomous long-running agent capability. So that's part of -- essential part of reengineering the workflow. What I'm most excited about, as you double-click into what I just described, is not only the assets that we have, the consumption of these assets is exponential in order to allow for an autonomous flow to deliver to the promise that the customer is looking for, which is an efficient design, better power, better performance, better cost, and that's exactly what we're doing.

**Operator** (Operator):
Your next question comes from the line of Gary Mobley with StoneX.

**Gary Mobley** (Analysts):
Sassine, you mentioned in your prepared remarks, the largest deal in the quarter for Ansys was a GPU-based digital twin. Was that a large deal because it is accelerated compute, runs an accelerated compute versus CPU-based compute? I'm asking because I'm just trying to get a sense of whether the efficiency from an accelerated compute digital twin system accrues to NVIDIA or accrues to you as well.

**Sassine Ghazi** (Executives):
Thank you, Gary, for the question. So simulation is a perfect application for GPU acceleration because these are jobs you can, for the most part, not only [ parallelize ], you can achieve a significant speed up. So the speed up does not stop or has limitation at 10 or 15x. In CFD, we're seeing 40, 50, 60x speed up. The bottleneck for our customers is the time to results, the time to accurate results. And the investment actually started with the GPU acceleration even before the acquisition of Ansys by Synopsys. After the acquisition, we just accelerated even further the commitment, the investment and of course, the NVIDIA investment and alignment towards this opportunity only helped. 
In terms of who gets the value, we sell and we capture the entire value and uplift of the GPU. NVIDIA, of course, in the back end, they -- you need GPU to run from the traditional CPU to a GPU. They benefit that way. So the large deal is large because of the benefit to the customer and the speed up we were able to deliver to the customer.

**Gary Mobley** (Analysts):
And my follow-up, I wanted to ask about Korea. Revenue generated from Korea appears to be trending up, close to 20% this year. That's a standout for sure. Is that a reflection of the strength of the memory market? Is it a reflection of maybe, I guess, you retaining more market share at Samsung and what many have speculated? Maybe you can just give some color there.

**Sassine Ghazi** (Executives):
I'm not sure about the speculation. One thing I can tell you is our relationship with Samsung, with SK hynix, with the broad market in Korea has been a great collaboration in an area and a region that are leading with a very essential part of the AI infrastructure, and we are leading with those customers and not limited to those 2 in the broader region itself in -- across the portfolio. So you need to think of it from IP with our custom HBM and HBM engagements with the lead customers to EDA and to Ansys. So very pleased with the performance that we have.

**Operator** (Operator):
Your next question comes from the line of Kelsey Chia with Citi.

**Wei Chia** (Analysts):
Great to see the IP business getting back on track. I believe the team outlined a long-term growth of about mid-teens for IP business several years ago. I mean since then, we have seen significant acceleration in the chip design activity, particularly among hyperscalers. And it seems that the non-AI portion of the business is also stabilizing. Given that backdrop, is it unreasonable to think that IP business could achieve a much stronger growth than the mid-teens laid out over the next couple of quarters? And if so, are there any factors that could prevent that growth algorithm from being set higher?

**Sassine Ghazi** (Executives):
Kelsey, thank you for the question. Your assumptions are good ones, which is more chip start, a huge opportunity with custom chips, which I refer to as Factory 2, as Factory 1 continue on delivering and expanding. And for now, the mid-teens is our long-term guide. We look forward for September, where we can share more and provide any updates as necessary.

**Operator** (Operator):
We have reached the end of the Q&A session. I will now turn the call back to Sassine Ghazi for closing remarks.

**Sassine Ghazi** (Executives):
Thank you for all the questions. One year after the transformational acquisition of Ansys, we're executing with focus, gaining momentum and extending our leadership from silicon to systems. I look forward to seeing many of you at Investor Day in September. Thank you very much.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SNPS_Q2_2026_Earnings_Call_20260527.md
- 2026-05-27｜CFO｜guidance：全年營收財測區間更新，由三因素構成（上半年表現、Ansys 通路毛額認列、處分 Processor IP）（原話："updated revenue range of $9.625 billion to $9.705 billion"）
- 2026-05-27｜CFO｜guidance：全年 non-GAAP EPS 財測與較前次中點上調幅度（原話："non-GAAP earnings of $14.72 to $14.80 per share"）
- 2026-05-27｜CFO｜guidance：第三季營收目標區間（原話："Total revenue between $2.41 billion and $2.46 billion."）
- 2026-05-27｜CFO｜guidance：全年自由現金流財測上調 1 億美元至約 20 億（原話："free cash flow of approximately $2 billion"）
- 2026-05-27｜CFO｜margin：全年 non-GAAP 營業利益率財測中點 41%，較前次上調 50bp（原話："non-GAAP operating margin of 41% at the midpoint"）
- 2026-05-27｜CFO｜margin：第二季營收含 Ansys 通路改毛額認列的 1250 萬美元，費用等額增加，對 EPS 與現金流中性（原話："added $12.5 million to revenue and an equal amount to expense"）
- 2026-05-27｜CFO｜margin：全年通路會計影響 6000 萬美元營收，並預期逐季成長（原話："you can think about that growing through the year"）
- 2026-05-27｜CFO｜margin：第二季各部門數字：IP 營收年減約 6%、季增 12%，EDA 年增略高於 8%（原話："down approximately 6% year-over-year and up 12% sequentially"）
- 2026-05-27｜CEO｜margin：CEO 說明今年營業利益率較去年底提高逾 300bp（原話："we're raising our operating margin by more than 300 basis points"）
- 2026-05-27｜CFO｜margin：CFO 解釋 Ansys 季節性：Ansys 原 Q4 對應 SNPS 的 Q1，故 Q1 成長偏高（原話："their strongest quarter always being a Q1"）
- 2026-05-27｜CFO｜margin：CFO 說明積壓訂單降至 110 億符合預期，與續約時點有關（原話："We build and then we burn"）
- 2026-05-27｜CEO｜commitment：管理層承諾 IP 今年逐季成長，並稱 Q1 為谷底（原話："Q1, we hit the bottom."）
- 2026-05-27｜CEO｜commitment：預期 FY2026 IP 成長仍低迷，但下半年逐季改善（原話："we continue to expect muted IP growth for fiscal year 2026"）
- 2026-05-27｜CEO｜commitment：到本財年底將有少數客戶簽下新 IP 商業模式合約（原話："we will have few customers with signed agreements"）
- 2026-05-27｜CFO｜commitment：財年底前達成約一半承諾的成本綜效，其餘時程留待投資人日說明（原話："we will have achieved about half of our committed synergies"）
- 2026-05-27｜CFO｜commitment：人力縮減 10% 的承諾維持，多數已完成（原話："we are still committed to the 10%"）
- 2026-05-27｜CEO｜commitment：Synopsys-Ansys 聯合產品的營收綜效從 FY27 開始，4 億美元目標維持（原話："FY '27, because the -- we released to limited set of partners"）
- 2026-05-27｜CEO｜commitment：Multiphysics Fusion 預計 2026 下半年開始商業化放量（原話："will begin ramping into commercial availability in the second half of 2026"）
- 2026-05-27｜CEO｜commitment：管理層表示將改變變現與商業模式，細節留待 9 月 30 日投資人日（原話："we will capture different value and different business model"）
- 2026-05-27｜CFO｜capital_allocation：啟動 2.5 億美元加速股票回購，並另有 5000 萬美元公開市場回購（原話："we initiated a $250 million accelerated share repurchase in March"）
- 2026-05-27｜CFO｜capital_allocation：期末總債務約 100 億美元，並已提前償還部分定期貸款（原話："Total debt at the end of Q2 was approximately $10 billion."）
- 2026-05-27｜CEO｜capital_allocation：宣布與 Elliott 合作協議，Jesse Cohn 出任獨立董事（原話："a cooperation agreement with Elliott Management"）
- 2026-05-27｜CEO｜capital_allocation：Processor IP Solutions 處分預計很快完成，影響本財年營收約 4000 萬美元（原話："expect to close the pending sale of the Processor IP Solutions business shortly"）
- 2026-05-27｜CEO｜product：Multiphysics Fusion 早期結果：收斂速度最高 3 倍（原話："up to 3x faster design closure with higher ECO success rates"）
- 2026-05-27｜CEO｜product：GPU 加速 EDA 已出現早期變現跡象（原話："we're seeing early signs of monetization with GPU-accelerated EDA"）
- 2026-05-27｜CEO｜product：agentic EDA 有 20 家客戶評估，涵蓋逾 25 個專門 AI agent（原話："20 customers now evaluating solutions across more than 25 specialized AI agents"）
- 2026-05-27｜CEO｜product：agent 時代授權構想：由人類訂閱加上 agent 用量計費，仍在早期探索（原話："subscription plus consumption for the agents"）
- 2026-05-27｜CEO｜product：PCIe 7.0 IP 勝率逾 90%，新增 18 份授權（原話："PCIe 7.0 IP achieved a greater than 90% win rate"）
- 2026-05-27｜CEO｜product：發表業界首款 HBM4 IP 測試晶片（原話："we also delivered the industry's first HBM4 IP test chip"）
- 2026-05-27｜CEO｜product：硬體輔助驗證為 Design Automation 主要成長動能（原話："Hardware-assisted verification remained the key growth driver"）
- 2026-05-27｜CEO｜competition：CEO 稱所有自研晶片（COT）客戶都用到其 EDA、HAV、IP 與 S&A（原話："There are none of the COT that does not use the EDA, HAV, IP and S&A."）
- 2026-05-27｜CEO｜competition：先進節點完整流程技術勝利逾 30 件（原話："over 30 full-flow technical wins in the quarter"）
- 2026-05-27｜CEO｜risk：中國設計啟動環境仍受限，財測對中國維持務實（原話："the design start environment in China remains challenged"）
- 2026-05-27｜CEO｜risk：工業與車用領域設計啟動仍偏弱，與 AI 相關領域分化（原話："still fairly muted design start activity in that domain"）
- 2026-05-27｜CFO｜risk：GAAP 費用高於預期，主因重組成本提前認列，GAAP EPS 僅 0.09 美元（原話："primarily due to the accelerated timing of restructuring costs"）
- 2026-05-27｜CEO｜customer：英特爾 18A／14A 等新製程目前財測未計入任何上行，需待從評估轉量產才付費（原話："we're not accounting or taking into account in our guidance any upside"）
- 2026-05-27｜CEO｜customer：Multiphysics Fusion 客戶仍在評估階段，尚未變現（原話："the monetization of that is not happening yet"）
- 2026-05-27｜CEO｜customer：超大規模雲端客戶推動 HAV 與自研晶片需求，一家 HPC 業者已用其方案完成 AI 加速器 tape-out（原話："a leading HPC provider successfully taped out"）

### SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md
- 2026-09-30｜Shelagh Glaser｜guidance：CFO 給 FY27 營收財測：成長 15% 至 111.5 億美元（中點）（原話："We expect to grow revenue 15% to $11.15 billion"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY27 營業利益率擴張 250 bp 至 44%（中點）（原話："expand operating margin 250 basis points to 44%"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY27 EPS 財測 19.08 美元（中點）（原話："to grow EPS even faster at '27 to $19.08"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY27 自由現金流約 31 億美元（原話："free cash flow will be approximately $3.1 billion"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY26 營收預期 97 億美元（原話："for '26, we anticipate revenue of $9.7 billion"）
- 2026-09-30｜Sassine Ghazi｜guidance：長期成長展望：2030 前整體年複合成長率中高個位數（mid-teens），先前為雙位數（原話："the long-term growth outlook is mid-teens CAGR through 2030"）
- 2026-09-30｜Sassine Ghazi｜guidance：長期目標上調 IP 成長：由 mid-teens 到 high teens（原話："from the mid-teens to high teens for IP"）
- 2026-09-30｜Sassine Ghazi｜guidance：長期目標上調 EDA 成長：由雙位數到 mid-teens（原話："from double-digit to mid-teens growth"）
- 2026-09-30｜Shelagh Glaser｜guidance：各業務長期成長下限：EDA 13%（原話："mid-teens growth for EDA with a floor of 13%"）
- 2026-09-30｜Shelagh Glaser｜guidance：各業務長期成長下限：模擬與分析（S&A）10%（原話："double-digit S&A growth with a floor of 10%"）
- 2026-09-30｜Shelagh Glaser｜guidance：各業務長期成長下限：設計 IP 17%（原話："design IP with a floor of 17%"）
- 2026-09-30｜Sassine Ghazi｜guidance：S&A 長期雙位數成長為有機成長，高於 ANSYS 獨立時的有機表現（原話："the long-term double-digit growth, that's organic"）
- 2026-09-30｜Shelagh Glaser｜guidance：EPS 與自由現金流長期以 mid-20s 成長（原話："we will grow EPS and free cash in the mid-20s"）
- 2026-09-30｜Sassine Ghazi｜guidance：AoIP 2030 年營收目標 10 億美元，管理層稱以現有合約為依據（原話："The projected growth for AoIP by 2030 will be $1 billion"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY27 沒有版稅收入，版稅自 FY28 起才進入（原話："There's specifically no royalty in 2027"）
- 2026-09-30｜Sassine Ghazi｜guidance：FY27 營收財測在 9 月提前公布（原本 12 月）（原話："FY '27 outlook at 15% year-over-year growth"）
- 2026-09-30｜Shelagh Glaser｜margin：FY26 全年營業利益率預期 41.5%（原話："our expectation for full year '26 is 41.5%"）
- 2026-09-30｜Shelagh Glaser｜margin：FY26 較 FY25 營業利益率改善 420 bp（原話："420 basis points improvement from fiscal year 2025"）
- 2026-09-30｜Shelagh Glaser｜margin：長期營業利益率目標約 50%（FY2030）（原話："approximately 50% by fiscal year 2030"）
- 2026-09-30｜Shelagh Glaser｜margin：50% 目標高於先前的 mid-40s 預期（原話："That's up from our prior expectation of mid-40s"）
- 2026-09-30｜Shelagh Glaser｜margin：CFO 說明版稅被視為近乎全額利潤，是新的利潤率槓桿（原話："the royalty as being 100% pure margin over time"）
- 2026-09-30｜Shelagh Glaser｜margin：回答 AI 對毛利率影響：與客戶合作時成本不變（原話："our cost doesn't really change"）
- 2026-09-30｜Shelagh Glaser｜margin：營業利益率目標已含投入 AoIP 工廠的成本（原話："does include investing in AIOP (sic) [ AOIP ]"）
- 2026-09-30｜Sassine Ghazi｜margin：CEO 表示不會為了把利潤率從 44% 推到 45–46% 而犧牲成長機會（原話："We will not trade off growth opportunities"）
- 2026-09-30｜Shelagh Glaser｜margin：FY27 起報告口徑改變：半導體事業單位自 ANSYS 移入 EDA（約佔 ANSYS 營收 10%）（原話："move the semiconductor business unit from ANSYS"）
- 2026-09-30｜Sassine Ghazi｜margin：AoIP 三層收費：授權費、客製化費（非 NRE）、版稅（原話："you see here it's different than an NRE"）
- 2026-09-30｜Shelagh Glaser｜commitment：成本綜效 4 億美元提前一年於 FY27 完成（原話："$400 million run rate synergies in fiscal year 2027"）
- 2026-09-30｜Shelagh Glaser｜commitment：FY27 結束時營收綜效年化超過 1 億美元（原話："greater than $100 million run rate in revenue synergies"）
- 2026-09-30｜Shelagh Glaser｜commitment：維持營收綜效 2029 年達 4 億美元年化的承諾（原話："achieve the $400 million run rate synergies by 2029"）
- 2026-09-30｜Sassine Ghazi｜commitment：AoIP 目標為版稅營收大於授權營收（原話："royalty revenue is greater than the license revenue"）
- 2026-09-30｜Sassine Ghazi｜commitment：CEO 回應版稅爬坡期營收是否下滑：不會下滑（原話："there is no dip"）
- 2026-09-30｜Sassine Ghazi｜commitment：FY27 預期出現 AI 營收（原話："for FY '27, we will see revenue from AI"）
- 2026-09-30｜Sassine Ghazi｜commitment：2027 起 ANSYS 與 Synopsys 整合的多物理融合產品開始貢獻營收綜效（原話："In 2027, we will see revenue synergy from that first wave"）
- 2026-09-30｜Sassine Ghazi｜commitment：CEO 收尾承諾（原話："we do what we say and say what we do"）
- 2026-09-30｜Shelagh Glaser｜capital_allocation：股東回報框架：最多將自由現金流的 50% 還給股東（原話："return up to 50% of free cash flow to shareholders"）
- 2026-09-30｜Shelagh Glaser｜capital_allocation：宣布未來數月內回購 10 億美元股票（原話："intent to repurchase $1 billion in Synopsys shares"）
- 2026-09-30｜Shelagh Glaser｜capital_allocation：股權報酬（SBC）佔營收比目標 FY2030 降至 8%（原話："targeting 8% SBC as a percent of revenue by fiscal year 2030"）
- 2026-09-30｜Shelagh Glaser｜capital_allocation：優先順序之一：維持投資等級評等，已提前還清定期貸款（原話："pay off the term loans early"）
- 2026-09-30｜Sassine Ghazi｜product：AoIP（原稱 Factory 2）：與客戶早期共同定義系統並共同設計 IP；Factory 1 持續投資（原話："We'll continue investing in this factory"）
- 2026-09-30｜Sassine Ghazi｜product：亞馬遜協議的 10 億美元為授權費，涵蓋三款晶片的多世代（原話："The $1 billion is a license fee"）
- 2026-09-30｜Sassine Ghazi｜product：版稅時程：設計到量產約 14 個月後才開始放量（原話："14-ish months of design to tape out and production"）
- 2026-09-30｜Sassine Ghazi｜product：下一代 ZeBu 硬體系統代號 Artemis，預計 FY27 上半年（原話："first half of '27, the code name is Artemis"）
- 2026-09-30｜Sassine Ghazi｜product：宣布與 OpenAI 多年合作，推出以 Synopsys 工具後訓練的 GPT-Synopsys（原話："a partnership multiyear with Synopsys and OpenAI"）
- 2026-09-30｜Sassine Ghazi｜product：CEO 說明 GPT-Synopsys 後訓練成本由 OpenAI 負擔（原話："OpenAI will have to invest hundreds of millions of dollars"）
- 2026-09-30｜Sassine Ghazi｜product：第三種模式的營收與 OpenAI 分成，依成果計價（原話："revenue share split between us and OpenAI"）
- 2026-09-30｜Sassine Ghazi｜product：Agent 工程師平台使 VCS／Verdi 授權使用量增加的示例（原話："5 to 10x more VCS and Verdi licenses"）
- 2026-09-30｜Shankar Krishnamoorthy｜product：AI 代理工程師已與頂尖客戶展開 50 個以上合作（原話："Over 50 engagements with all the top customers"）
- 2026-09-30｜Sassine Ghazi｜product：目前客戶 AI 合作多落在第二種模式（客戶自建平台＋買 Synopsys 代理），其次全堆疊，再其次前沿模型（原話："most of our customer engagements are in 2, then 1, then 3"）
- 2026-09-30｜Sassine Ghazi｜competition：CEO 回應「AI 模型可取代 EDA」的外界推論（原話："extrapolation cannot be more far off than reality"）
- 2026-09-30｜Sassine Ghazi｜competition：回答 AI 是否能繞過 EDA：否（原話："not be a point where you can bypass EDA completely"）
- 2026-09-30｜Sassine Ghazi｜competition：客戶對 AI 的立場摘要語（原話："In AI, we believe, but in physics, we trust."）
- 2026-09-30｜Sassine Ghazi｜competition：CEO 提到投資人曾反覆詢問 Intel 流失問題，並回應 Synopsys 與 Intel 持續合作（原話："You've lost Intel. Are you at Intel?"）
- 2026-09-30｜Sassine Ghazi｜competition：CEO 論述 IP 在晶圓代工中的必要性（原話："be in the foundry business without having Synopsys IP"）
- 2026-09-30｜Sassine Ghazi｜risk：中國市場 IP 需求放緩，原因為先進製程受限（原話："the China opportunity as it relates to IP has slowed down"）
- 2026-09-30｜Sassine Ghazi｜risk：客戶在續約時不願簽 3 年固定容量，因為尚不知需多少容量（原話："not going to commit for 3 years at a certain level"）
- 2026-09-30｜Sassine Ghazi｜risk：現階段客戶仍偏好訂閱制而非用量計費（原話："primarily the customer comfort zone is subscription"）
- 2026-09-30｜Sassine Ghazi｜customer：ANSYS 併購使客戶基數擴大 10 倍（原話："expanded the Synopsys customer base by 10x"）

### 問答異常語氣（迴避／改口／保留）
- SNPS_Q2_2026_Earnings_Call_20260527.md｜問：Quatrochi 問 3,500 萬美元財測上調中 EDA 與 IP 各占多少｜答法：CEO 未拆分數字，改談 AI 半導體需求與全產品線強度
- SNPS_Q2_2026_Earnings_Call_20260527.md｜問：Panigrahi 問剩餘成本綜效的規模與時程｜答法：CFO 只重申年底達一半，剩餘綜效時程與規模推到投資人日再談，未給數字
- SNPS_Q2_2026_Earnings_Call_20260527.md｜問：Celino 問 Ansys 季增中段十幾 % 對比財測約 10% 的下半年減速原因｜答法：CEO 先談整合與需求，CFO 以 Ansys 會計年度重編的季節性機械因素回答，未直接量化下半年減速
- SNPS_Q2_2026_Earnings_Call_20260527.md｜問：Tilton 問成長率能否提升或僅是持久性，及成長形狀｜答法：CEO 未給成長率數字或形狀，強調變現模式轉變並推到投資人日
- SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md｜問：Jay Vleeschhouwer：核心 EDA 近年低至中個位數成長、甚至有季減，如何達到 mid-teens？｜答法：CEO 以續約洽談中客戶要更多 AI 容量與多物理融合為由，稱 FY27 為由下而上推估且信心高，未回應核心 EDA 單獨的成長數字或所需增量
- SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md｜問：Vivek Arya：請量化明年及 2030 模型中的版稅金額｜答法：CFO 稱 FY27 無版稅、AoIP 10 億含授權與版稅，並表示 We didn't give a split，未給比例
- SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md｜問：Jason Celino：若替代方案的成果比 GPT-Synopsys 更好，客戶仍會付費嗎？｜答法：CEO 轉談三種客戶選擇與工具需求，未直接回答成果較差時是否付費
- SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md｜問：Joshua Tilton：Factory 2 後續客戶管線為何；OpenAI 合作是否對 Synopsys 獨家｜答法：CEO 未給管線規模，稱對話進行中；獨家性問題回稱不偏袒、其他模型商是否跟進由對方決定

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
{"status":"no_prior_dd"}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNPS_20261019/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
