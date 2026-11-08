你是 stock-analyst **v20 判斷 agent**，標的 FICO（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"FICO","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FICO_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FICO_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":657.0,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（8-K Exhibit 99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000037/exhibit991erq42026.htm"}},{"id":"f_kpi1_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":null,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（8-K Exhibit 99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000037/exhibit991erq42026.htm"},"needs_sonnet":true},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":266.6,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（8-K Exhibit 99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000037/exhibit991erq42026.htm"}},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":284.3,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（8-K Exhibit 99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000037/exhibit991erq42026.htm"}},{"id":"f_kpi5_guidance","label":"Guidance","value":null,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（8-K Exhibit 99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000037/exhibit991erq42026.htm"},"needs_sonnet":true},{"id":"f_kpi6_software_arr_growth","label":"Software ARR growth","value":14,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"% YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（8-K Exhibit 99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000037/exhibit991erq42026.htm"}},{"id":"f_kpi7_dollar_based_net_retenti","label":"Dollar-based net retention rate (Software)","value":112,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（8-K Exhibit 99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000037/exhibit991erq42026.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_fico_gross_margin_pct","label":"FICO 毛利率","value":85.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FICO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_fico_operating_margin_pct","label":"FICO 營業利益率","value":53.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FICO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_fico_fcf_margin_pct","label":"FICO FCF 利潤率","value":39.94,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FICO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_efx_gross_margin_pct","label":"EFX 毛利率","value":55.18,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EFX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_efx_operating_margin_pct","label":"EFX 營業利益率","value":18.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EFX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_efx_fcf_margin_pct","label":"EFX FCF 利潤率","value":16.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EFX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tru_gross_margin_pct","label":"TRU 毛利率","value":58.82,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TRU.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tru_operating_margin_pct","label":"TRU 營業利益率","value":19.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TRU.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tru_fcf_margin_pct","label":"TRU FCF 利潤率","value":18.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TRU.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrsk_gross_margin_pct","label":"VRSK 毛利率","value":70.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRSK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrsk_operating_margin_pct","label":"VRSK 營業利益率","value":43.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRSK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrsk_fcf_margin_pct","label":"VRSK FCF 利潤率","value":34.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRSK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mco_gross_margin_pct","label":"MCO 毛利率","value":74.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mco_operating_margin_pct","label":"MCO 營業利益率","value":45.94,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mco_fcf_margin_pct","label":"MCO FCF 利潤率","value":36.41,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC","value":43.5,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（8-K Exhibit 99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000037/exhibit991erq42026.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":704.55,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-37.43,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":40.67,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（46.28 → 46.28）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（52.77 → 52.77）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（59.35 → 59.35）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":46.28,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":52.77,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":59.35,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":7.35,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 43.11 → 46.28（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":19.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.94,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":7.94,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.22,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 46.28，分子＝快照價 704.55","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":5072.4,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 5290.0、現金 217.6（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":21.38,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":20136.33,"period":"2026-11-08","unit":"USD m","basis":"市值 15063.93 ＋ 淨負債 5072.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":2595.26,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（19 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":2769.62,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.76,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 704.55 / W52 1224.94 / W104 1514.28 / W250 1164.01 / W250 13週斜率 0.44%"},{"id":"f_ma_w52","label":"52 週均線","value":1224.94,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":1514.28,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":1164.01,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.44,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出 Scores 段主要對手為三大徵信機構與其合資的 VantageScore，後者在美國房貸市場的監管接受度提高。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"VantageScore (a joint venture entity established by the three major U.S. consumer reporting agencies), which is selling a credit scoring product competitive with our products and which has experienced increased regulatory acceptance in the U.S. mortgage market.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：客戶可能以 AI 自建評分模型，且分析與決策產品愈來愈與大型語言模型開發商的產品競爭。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"our analytics and decisioning products increasingly compete against products from large language model developers.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Motley Fool 報導 2026-09-29 FICO 股價單日跌 25.4%，文章稱政府與房貸業界正在扶植新競爭者 VantageScore。","source":"Motley Fool: Why Fair Isaac Corporation plunged today","url":"https://www.fool.com/investing/2026/09/29/why-fair-isaac-corporation-plunged-today/","excerpt":"Needless to say, when a company with a monopoly sees that monopoly erode, the stock can undergo a big rerating.","as_of":"2026-09-29","retrieved_at":"20261108","affects":["moat_trend","valuation","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素：客戶可能自行開發評分模型或其他產品（含以 AI 方案），可能減少或取消對 FICO 產品的採購；Scores 部門面對 VantageScore（三大徵信局合資），該分數在美國房貸市場獲更多監管認可。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"This competition may include our customers developing their own scoring models or other products, including through the use of AI-based offerings, which could eliminate or reduce their purchases of our products and services. For example, our Scores segment faces competition from other credit score models, including VantageScore, which has experienced increased regulatory acceptance in the U.S. mortgage market.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 競爭清單把「in-house data science and systems developers」列為競爭來源之一。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"We encounter competition from several sources, including: •in-house data science and systems developers; •developers and providers of large language models, machine learning, and AI systems;","as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2026 營收來自 Experian、TransUnion、Equifax 協議合計占總營收 60%（FY2025 51%、FY2024 45%）。","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000042/fico-20260930.htm","excerpt":"During fiscal 2026, 2025 and 2024, revenues generated from our agreements with Experian, TransUnion and Equifax collectively accounted for 60%, 51% and 45% of our total revenues, respectively.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FHFA/Pulte 結束試行，指示 Fannie/Freddie 核准所有貸方使用 VantageScore。","source":"The Mortgage Reports: vantagescore fannie freddie all lenders","url":"https://themortgagereports.com/134153/vantagescore-fannie-freddie-all-lenders","excerpt":"Mortgage News, roughly 50 lenders delivered loans under that pilot, and VantageScore 4.0 was used on more than 9% of mortgages Fannie and Freddie securitized between May 1 and August 31. On September 3, Pulte ended the pilot phase, posting: “So, EFFECTIVE IMMEDIATELY, I’m instructing Fannie and Freddie to approve ALL lenders to use VantageScore.”","as_of":"2026-09-09","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Experian、TransUnion、Equifax 三家合計占 FICO 營收 FY2026 60%、FY2025 51%、FY2024 45%。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"During fiscal 2026, 2025 and 2024, revenues generated from our agreements with Experian, TransUnion and Equifax collectively accounted for 60%, 51% and 45% of our total revenues, respectively.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"三家 CRA 各自占營收超過 10%；2026-09-30 有三個客戶各占應收帳款 10% 以上（前一年為兩個）。","source":"SEC EDGAR 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"with all three consumer reporting agencies each contributing more than 10% of our total revenues in each of fiscal 2026, 2025 and 2024. At September 30, 2026 and September 30, 2025, three customers and two customers, respectively, accounted for 10% or more of total consolidated receivables.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 風險因素揭露依賴少數客戶（含三大 CRA），客戶規模較大、議價力強，條款可能被重談或終止。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"We rely on relatively few customers, including our contracts with the three major consumer reporting agencies, for a significant portion of our revenues and profits. Many of our customers are significantly larger than we are and may have greater bargaining power, which could negatively impact the terms of our commercial agreements.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未見三大 CRA 遭信用評等調降；僅見 Equifax 下調 2026 營收指引（美國房貸業務疲弱）及券商調降評等（Oppenheimer、RBC），為股票評等非信用評等。","source":"WebSearch 彙整結果（Equifax FY26 guidance cut 等聚合報導）","url":"https://scanx.trade/stock-market-news/companies/equifax-fy26-results-sales-guidance-cut-6-646b-6-676b/54038439","excerpt":"Equifax FY26 Results: Sales guidance cut to $6.646B-$6.676B","as_of":"2026-10-22","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"FICO 以維持批發抵押貸款分數 $10 換取貸款機構承諾；Equifax 稱 FICO 2026 價格由 $4.95 翻倍至 $10，Equifax VantageScore 4.0 定價 $4.50 至 2027 年底，TransUnion 99 美分 VantageScore 4.0 延長至 2028 年底；FHFA 擬將 VantageScore 納入同一定價表，無開始日期。","source":"TIKR: FICO Sinks 16% as It Holds Mortgage Score Price at $10 (搜尋摘要彙整)","url":"https://www.tikr.com/blog/fico-sinks-16-as-it-holds-mortgage-score-price-at-10-with-flat-year-over-year-pricing","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Scores 占 FICO 2025 財年營收約 59%；6 月分析稱空頭論點取決於抵押貸款量激增中有多少為週期性而非結構性","source":"Walnut Invest / TIKR","url":"https://walnutinvest.com/stocks/fico/is-it-a-buy-or-sell","excerpt":"mortgage-scoring monopoly and inviting pricing pressure. FICO's own move to a roughly $0.99-per-score-plus-fee mortgage model sharply cut average per-score fees, and investors are debating whether that defends share or signals eroding pricing power. The relationship with the FHFA has become adversarial, and a regulator-led move to a two-bureau mortgage model would hand VantageScore a structural","as_of":"2026-06-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FICO 為伊利諾州北區聯邦法院反壟斷集體訴訟被告；2026-09-29 簽訂和解條款書，擬付 6,500 萬美元並附合規承諾，不承認不當行為，仍待法院最終核准。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"On September 29, 2026, FICO and the plaintiffs entered into a term sheet memorializing the material terms of a proposed settlement of the lawsuits. In consideration of a cash payment by FICO to the plaintiffs of $65.0 million and certain compliance undertakings, the settlement would fully resolve all remaining claims asserted against FICO in the lawsuits.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"法院 2024-11-24 駁回除 Sherman Act 第 2 條及相關州法請求以外的所有主張，剩餘主張對 FICO 進入證據開示階段。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"The court dismissed with prejudice all claims in the lawsuit other than a Sherman Act Section 2 claim and accompanying state law claims against FICO, which were allowed to proceed through the discovery stage of the litigation.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2026 第四季已認列 6,500 萬美元和解負債，計入 SG&A 的外部服務費增加。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"a $65.0 million liability recorded in the fourth quarter of fiscal 2026 for a proposed settlement of the antitrust class action lawsuits","as_of":"2026-11-06","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Florida 檢察長 Uthmeier 於 2026-07-01 對 FICO 發出民事調查要求（CID），調查是否違反 Florida Antitrust Act（綑綁、掠奪性定價、與信用局限制性協議）。","source":"PYMNTS/CPI：Florida opens antitrust probe into FICO","url":"https://www.pymnts.com/cpi-posts/florida-opens-antitrust-probe-into-fico-over-credit-scoring-market-practices/","excerpt":"a Civil Investigative Demand to FICO on July 1, seeking records related to pricing, licensing agreements, communications about competitors, exclusionary contracts, market-share analyses and documents produced in existing federal antitrust litigation. The probe is examining whether FICO violated the Florida Antitrust Act through alleged monopolistic conduct, including product bundling,","as_of":"2026-07-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#4","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Sen. Hawley 於 2026-03-23 通知 FICO 國會調查其房貸信用分數漲價，並去函 FTC 要求平行調查。","source":"Ballard Spahr via Mondaq","url":"https://www.mondaq.com/unitedstates/financial-services/1765928/senator-hawley-investigating-fico-credit-score-pricing-practices-and-urging-ftc-to-investigate-as-well","excerpt":"Senator Hawley Investigating FICO Credit Score Pricing Practices And Urging FTC To Investigate As Well Ballard Spahr LLP More Contributor Ballard Spahr LLP","as_of":"2026-03-30","retrieved_at":"20261108","affects":["thesis.R","moat_trend","valuation"],"status":"ok"},{"id":"regulatory_antitrust#5","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FHFA 指示 Fannie/Freddie 開放所有貸款人使用 VantageScore，報導稱 FICO 股價單日大跌約 15–18%（二手來源）。","source":"TIKR：Fair Isaac stock drops after federal regulator vows to end credit bureau overcharging","url":"https://www.tikr.com/blog/fair-isaac-stock-drops-fhfa-vantagescore-directive","excerpt":"Federal Housing Finance Agency Director Bill Pulte ordered Fannie Mae and Freddie Mac to immediately let all mortgage lenders use VantageScore, FICO’s main rival in credit scoring.","as_of":"2026-09-05","retrieved_at":"20261108","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FICO 10-K 列出出口管制與制裁法規（OFAC、EAR）適用於其在非美國地區交付的產品；風險因素亦提及關稅變動與貿易壁壘為國際業務風險，FY2026 營收 20% 來自美國以外。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"Laws and regulations restricting transactions with sanctioned parties and regarding export controls as they apply to FICO products delivered in non-U.S. countries or to foreign nationals (e.g., Office of Foreign Asset Control sanctions and Export Administration Regulations)","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"風險因素將關稅與報復性關稅、貿易緊張列為可能壓抑客戶（銀行業占營收 92%）支出與延長銷售週期的總經因素；未見 FICO 特定關稅或出口管制事件。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"During fiscal 2026, 92% of our revenues were derived from sales of products and services to the banking industry.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 稱約三分之一員工位於印度，可能受印巴緊張局勢影響","source":"FAIR ISAAC CORP Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454725000030/fico-20250930.htm","excerpt":"For example, approximately one-third of our workforce is located in India, which could be negatively impacted by heightened tensions between India and Pakistan.","as_of":"2025-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 稱服務可靠度依賴自有及外部供應商資料中心與IT系統，風險清單含戰爭","source":"FAIR ISAAC CORP Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454725000030/fico-20250930.htm","excerpt":"of our and our external service providers’ data centers, information technology and communication systems. Any disruption of or interference with our use of data centers, information technology or communication systems of our external service providers would adversely affect our operations and our business. As we continue to grow our Software segment’s business, our dependency on the","as_of":"2025-11-05","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q4 Scores 營收約 $414M，年增 33%，主因房貸 origination 分數單價上調（量下降）；全年 Scores $1.652B，年增 41%","source":"FICO FY2026 Q4 earnings call transcript (Earnings Whispers)","url":"https://www.earningswhispers.com/transcript/FICO/Q42026","excerpt":"scores revenues in our fourth quarter were $414 million, up 33% versus the prior year","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q4 Software 營收 $243M，年增 19%；平台營收 +84%、非平台 -12%；Software ARR $851M，+14%","source":"FICO FY2026 Q4 earnings call transcript (Earnings Whispers)","url":"https://www.earningswhispers.com/transcript/FICO/Q42026","excerpt":"In our software segment, we delivered $243 million in Q4 revenues, up 19% year over year.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"FICO 不提供 FY27 財測，因正與客戶洽談涵蓋 2027 曆年的客製化房貸定價安排","source":"Zacks, Fair Isaac Q4 earnings top estimates","url":"https://www.zacks.com/stock/news/2787140/fair-isaac-q4-earnings-top-estimates-strong-scores-drive-up-sales-y-y","excerpt":"would not provide its fiscal 2027 guidance while negotiating customized mortgage pricing arrangements covering calendar 2027","as_of":"2026-11-04","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"RBC 降評至 Sector Perform，指房貸定價不確定與 VantageScore 份額風險","source":"Goldesel: Fair Isaac Aktie RBC stuft auf Sector Perform ab","url":"https://goldesel.de/aktien/news/fair-isaac-aktie-rbc-stuft-auf-sector-perform-ab-und-senkt-kursziel","excerpt":"November von Outperform auf Sector Perform herab. 02 Das Kursziel sinkt von 1.045 auf 770 US-Dollar. 03 FICO übertrifft im vierten Quartal des Geschäftsjahres 2026 die Erwartungen beim bereinigten Gewinn je Aktie.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FICO 10-K 自列風險：AI（含生成式與代理式 AI）快速變動，若產品跟不上技術變化可能迅速失去競爭力或過時；並列示AI造成的市場擾動、競爭信用評分模型的可得性與使用增加、含AI技術的免費或廉價消費者信用資訊增加為產品接受度風險。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"changes in technology, including increased use of artificial intelligence (“AI”) and market disruption caused by AI-based offerings;","as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 明列「競爭信用評分模型的可得性、接受度與使用增加」為產品市場接受度風險因素。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"the availability, acceptance and increased use of competing credit score models;","as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Equifax 針對 FICO 房貸分數漲價，以較 FICO 2026 價格低逾 50% 的價格（$4.50，至 2027 年底）提供 VantageScore 4.0 房貸信用分數。","source":"TipRanks/The Fly: Equifax cuts mortgage credit scores price","url":"https://www.tipranks.com/news/the-fly/equifax-cuts-mortgage-credit-scores-price-by-50-in-response-to-fico-thefly","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261108","affects":["moat_trend","valuation","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FICO 2025年10月宣布房貸直接授權計畫，tri-merge 轉售商等可不經三大信用局直接計算並分銷 FICO 分數；2026年4月 FICO Score 10T 也納入；信用局相關營收占總營收 FY2026/2025/2024 為 60%/51%/45%。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"In October 2025, we announced a significant change in the delivery of FICO® Scores to the U.S. mortgage industry. With the announcement of the FICO® Mortgage Direct License Program, tri-merge resellers, platform providers, and other third-party distributors will have the option to calculate and distribute FICO Scores directly to their customers (e.g., mortgage originators), without relying on a consumer reporting agency as an intermediary.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FICO 預期隨 FICO Platform 能力增加，間接通路（聯盟夥伴、轉售商、系統整合商）銷售將成長，並投入大量資源發展。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"As more capabilities are made available on FICO® Platform, we expect our sales through indirect channels to grow. We are investing significant resources to develop our indirect channel relationships.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"直接授權計畫提供 tri-merge 轉售商兩種定價：每分 $4.95 權利金（較平均降約50%）或維持每分 $10；Cotality、Ascend、Xactus、CIC Credit 已加入；Equifax、TransUnion 公告後股價下跌。","source":"MarketChameleon／搜尋摘要彙整（2025-10）","url":"https://marketchameleon.com/articles/b/2025/10/2/fico-direct-licensing-cuts-mortgage-score-costs","excerpt":null,"as_of":"2025-10-02","retrieved_at":"20261108","affects":["valuation","moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"FICO 2026-11-04 公布財報，公司暫不提供 FY2027 財測；調整後 EPS 11.10 美元高於市場預期 10.71 美元","source":"goldesel.de 《Fair Isaac Aktie: Quartalsgewinn übertrifft Erwartungen, FY27-Ausblick bleibt aus》","url":"https://goldesel.de/aktien/news/fair-isaac-aktie-quartalsgewinn-ubertrifft-erwartungen-fy27-ausblick-bleibt-aus","excerpt":"verzichtet das Unternehmen vorerst auf eine Prognose für das Geschäftsjahr 2027.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","triggers","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"RBC Capital 於 2026-11-05 將 FICO 由 Outperform 降至 Sector Perform，目標價由 1,045 降至 770 美元","source":"goldesel.de 《Fair Isaac Aktie: RBC stuft auf Sector Perform ab und senkt Kursziel》","url":"https://goldesel.de/aktien/news/fair-isaac-aktie-rbc-stuft-auf-sector-perform-ab-und-senkt-kursziel","excerpt":"RBC Capital stuft Fair Isaac am 5. November von Outperform auf Sector Perform herab. Das Kursziel sinkt von 1.045 auf 770 US-Dollar.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-07-28：15 位分析師、10 買 5 持有，平均目標價約 1,628 美元（財報前、已較年初下修；此為財測撤回前的舊共識）","source":"MarketBeat 2026-07-28 consensus recommendation 'Moderate Buy'","url":"https://www.marketbeat.com/instant-alerts/fair-isaac-corporation-nysefico-receives-consensus-recommendation-of-moderate-buy-from-analysts-2026-07-28/","excerpt":"The average 12-month price target is approximately $1,627.93.","as_of":"2026-07-28","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"FICO 與原告於 2026-09-29 簽訂和解條款書：就 FICO Scores 反壟斷集體訴訟，支付 6,500 萬美元現金並附合規承諾，不承認不當行為；仍待法院最終核准","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"On September 29, 2026, FICO and the plaintiffs entered into a term sheet memorializing the material terms of a proposed settlement of the lawsuits. In consideration of a cash payment by FICO to the plaintiffs of $65.0 million and certain compliance undertakings, the settlement would fully resolve all remaining claims asserted against FICO in the lawsuits.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-01 公司承諾裁員約 15% 職位，預計 FY2026 Q4 認列約 2,700 萬美元稅前費用","source":"SEC EDGAR 8-K Item 2.05","url":"https://www.sec.gov/Archives/edgar/data/814547/000119312526415732/d127042d8k.htm","excerpt":"This plan involves the elimination of approximately 15% of positions across the Company.","as_of":"2026-10-06","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-05 增設 15 億美元無擔保定期貸款，所得用於加速股票回購（ASR）","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/814547/000119312526260817/d140061d8k.htm","excerpt":"The Company borrowed the full amount of the Incremental Term Loan on June 5, 2026, and will use these proceeds pursuant to the accelerated share repurchase program described in Item 8.01 below.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"FICO 完成收購 nextmv.io（決策營運開發公司），2026-05 交割；屬小型收購，搜尋未見 FICO 被併或大型併購","source":"Faegre Drinker 交易經驗頁：Fair Isaac Corporation completes acquisition of nextmv.io Inc.","url":"https://www.faegredrinker.com/en/services/experience/2026/6/fair-isaac-corporation-completes-acquisition-of-nextmvio-inc","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"FICO Scores 反壟斷集體訴訟（伊利諾州北區）以 6,500 萬美元和解條款書了結，待法院核准；公司稱預期 FY2027 Q1 簽正式協議","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm","excerpt":"We anticipate the parties will enter into definitive settlement agreements in the first quarter of fiscal 2027 reflecting the terms of the settlement as set forth in the term sheet.","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"FICO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":85.86,"operating_margin_pct":53.21,"fcf_margin_pct":39.94,"rd_intensity_pct":8.39},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FICO","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"EFX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.18,"operating_margin_pct":18.83,"fcf_margin_pct":16.75,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EFX","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TRU","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":58.82,"operating_margin_pct":19.35,"fcf_margin_pct":18.06,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TRU","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"VRSK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":70.17,"operating_margin_pct":43.91,"fcf_margin_pct":34.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRSK","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MCO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.63,"operating_margin_pct":45.94,"fcf_margin_pct":36.41,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"FICO"},"financial_history":{"ticker":"FICO","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-09-30","revenue":1377270000.0,"revenue_yoy_pct":null,"gross_margin_pct":78.06,"operating_margin_pct":39.38,"net_income":373541000.0,"diluted_eps":14.18,"free_cash_flow":503421000.0,"fcf_margin_pct":36.55,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-09-30","revenue":1513557000.0,"revenue_yoy_pct":9.9,"gross_margin_pct":79.45,"operating_margin_pct":42.34,"net_income":429375000.0,"diluted_eps":16.93,"free_cash_flow":464678000.0,"fcf_margin_pct":30.7,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":1717526000.0,"revenue_yoy_pct":13.48,"gross_margin_pct":79.73,"operating_margin_pct":42.71,"net_income":512811000.0,"diluted_eps":20.45,"free_cash_flow":607413000.0,"fcf_margin_pct":35.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":1990869000.0,"revenue_yoy_pct":15.91,"gross_margin_pct":82.23,"operating_margin_pct":47.0,"net_income":651946000.0,"diluted_eps":26.54,"free_cash_flow":739400000.0,"fcf_margin_pct":37.14,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/FICO/FICO_Q4_2026_Earnings_Call_20261104.md）

# Q4 2026 Earnings Call
**Fair Isaac Corporation** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Thank you for standing by, and welcome to FICO's Fourth Quarter 2026 Earnings Conference Call. [Operator Instructions]
I would now like to hand the call over to Dave Singleton, Head of IR. Please go ahead.

**Dave Singleton** (Executives):
Good afternoon, and thank you for attending FICO's fourth quarter earnings call. I'm Dave Singleton, Vice President of Investor Relations, and I'm joined today by our CEO, Will Lansing; and our CFO, Steve Weber.
Today, we issued a press release that describes financial results compared to the prior year. On this call, management will also discuss results in comparison with the prior quarter to facilitate an understanding of the run rate of the business. Certain statements made in this presentation are forward-looking under the Private Securities Litigation Reform Act of 1995. Those statements involve many risks and uncertainties that could cause actual results to differ materially. Information concerning these risks and uncertainties is contained in the company's filings with the SEC, particularly in the risk factors and forward-looking statements portions of such filings. Copies are available from the SEC, from FICO's website or from our Investor Relations team.
This call will also include statements regarding certain non-GAAP financial measures. Please refer to the company's earnings release and Reg G schedule issued today for a reconciliation of these non-GAAP financial measures to the most comparable GAAP measure. The earnings release and Regulation G schedule are available on the Investor Relations page of the company's website at fico.com or on the SEC's website at sec.gov. A replay of this webcast will be available through November 4, 2027. Our quarterly investor presentation is available on the Investor Relations section of our website, and we will refer to this presentation during today's earnings announcement.
I will now turn the call over to our CEO, Will Lansing.

**William Lansing** (Executives):
Thanks, Dave, and thank you, everyone, for joining us for our fourth quarter earnings call. With another strong quarter, we closed fiscal 2026 as the most successful financial year in FICO's history. 
We reported Q4 revenues of $657 million, up 27% over last year, as you can see on Page 5 of our investor presentation. For the full fiscal year, we delivered revenues of $2.535 billion, up 27% versus the prior year. 
For the quarter, we reported GAAP net income of $175 million, up 13% and GAAP earnings of $8.12 per share, up 26% from the prior year. GAAP net income included three significant items, which Steve will discuss later, that had a combined net charge of $44 million pretax, $33 million after tax. Excluding these items only, adjusted net income would have been $208 million, up 27%, and adjusted earnings per share would have been $9.64, up 43% on a comparable basis to the prior year. These items are excluded from our non-GAAP results, along with other adjustments consistent with prior periods. With all these adjustments for the quarter, our non-GAAP net income was $239 million, up 28%, and non-GAAP earnings per share were $11.10, up 43% from the prior year.
For the fiscal year, GAAP net income was $835 million, up 28% from fiscal 2025, and GAAP earnings per share were $36.32, up 37% over the same period. For the fiscal year, non-GAAP net income was $988 million, up 35% from fiscal 2025, and non-GAAP earnings per share were $42.99, up 44% over the same period.
We delivered free cash flow of $284 million in our fourth quarter. For the full fiscal year, we delivered $1.034 billion in free cash flow, an increase of 40% over fiscal 2025.
In fiscal 2026, we repurchased a record $3.028 billion of stock or 2.514 million shares at an average price of $1,204 per share. This represents about 10% of shares outstanding from the end of fiscal 2025.
Now in Q4, we paused repurchases and directed free cash flow to repaying the term loan that funded the Q3 accelerated share repurchase, bringing leverage to 3.29x net debt to EBITDA. Going forward, our philosophy has not changed. We continue to view share repurchases as an attractive use of cash.
At the segment level, shown on Page 6, Scores revenues in our fourth quarter were $414 million, up 33% versus the prior year. While B2B Scores were the key driver of growth, we also experienced continued growth in B2C Scores. For the full year, we delivered $1.652 billion in Scores revenues, up 41% from the prior year.
In our Software segment, we delivered $243 million in Q4 revenues, up 19% year-over-year. Results included 84% platform revenue growth and a 12% decline in non-platform revenue. For the full year, we delivered $883 million in Software segment revenues, up 7% from the prior year. Steve will provide additional segment level details later.
This year, our Scores business advanced our strategic priorities in a challenging environment, and I'm really proud of our accomplishments. We laid the groundwork for broader distribution by signing direct license agreements with reseller partners representing about 73% of mortgage reseller volume, including the current quarter agreement with Informative Research.
We also brought new IP into the market with next-generation UltraFICO Score, and we grew adoption of both our FICO Score Mortgage Simulator and FICO Score 10T. This quarter, the FHA announced FICO Score 10T, which is the most predictive modern credit score, will be available for approved lenders beginning Jan 1, 2027. The availability of FICO Score 10T will enable lenders to make more accurate lending decisions, while helping consumers gain access to more favorable mortgage terms and sustainable homeownership. FICO Score 10T outperforms competing models by more than 10% on FHA first-time home buyer mortgages. A clear predictive advantage in a segment where accurate risk assessment is paramount.
Our FICO Score 10T Adopter Program, which you can see on Page 9, has grown to 84 lenders, spanning both conforming and non-conforming mortgage markets. The program now represents over 60% of the volume generated by the top 50 mortgage originators for originated FHA units, over 50% for originated first-lien units purchased by the GSEs. Based on 2025 HMDA data, participating lenders account for $684 billion in eligible annual originations and more than $2.65 trillion in eligible annual servicing.
In October, we launched the FICO Preferred Program distributed by our participating tri-merge resellers. Enrolled lenders and brokers that commit to the program will have no 2027 wholesale mortgage price increase for the FICO score and will receive a bundled classic FICO Score and FICO Score 10T. With this program, we're ensuring lenders have access to the trusted and predictive tools they need to assess risk with confidence. Better risk decisions strengthen the mortgage market and help lenders responsibly expand access to credit, helping more Americans achieve the dream of homeownership.
To date, as shown on Page 11, we've demonstrated demand for this program by several announcements. We expect resellers to continue signing participants. And although we don't anticipate announcing all participants, we do expect to provide periodic updates on program uptake and demand.
We've also made significant strides with our software innovation. Early in October, we achieved 2 key milestones in our software business: First, general availability of the next-generation FICO platform and the launch of Enterprise Fraud Solution, which we call EFS; and second, FICO-focused sequence model together on the FICO platform.
With the next-generation FICO platform customers gained 3 connected capabilities on a single platform: First, the platform provides an always-on real-time view of their own customers. Second, the platform gives business teams greater agency while reducing dependence on traditional IT release cycles. Third, the platform provides a closed feedback loop giving customers the evidence needed to improve decision quality over time rather than relying on systems to flag issues and hand them off. 
The launch of Enterprise Fraud Solution and FICO Focused Sequence Model together on FICO platform gives financial institutions connected and comprehensive fraud protection across the entire customer life cycle. The solution is designed to protect financial institutions globally from fraud losses, customer impact and regulatory liability. This is critical at a time where losses are escalating from scams and authorized push payment fraud, money mules, first-party fraud and card and real-time payments fraud.
Our solution is also designed to deal with the threats and challenges faced by agentic commerce and agentic attacks and threats. It allows banks to integrate data and orchestrate decisions in real time more precisely than ever before. It unifies transaction behavior across every channel into one real-time profile that follows customers throughout their journey. The result is proactive protection, fewer false positives and less friction for genuine customers.
I'm proud of these accomplishments and industry analysts recognize them as well. In September, FICO was named Leader in the IDC MarketScape: Worldwide Decision Intelligence Platforms 2026 Vendor Assessment. FICO was recognized for its strength in dynamic profiling and expanding ecosystem and marketplace and agentic policy offering. 
In fiscal '27, we plan to advance our direct and indirect distribution and invest to capture market opportunities emerging from these innovations, both in our software and scoring business.
I'll now hand it over to Steve to provide further financial details.

**Steven Weber** (Executives):
Thanks, Will, and good afternoon, everyone. As Will mentioned, our software -- our Scores segment revenues for the quarter were $414 million, up 33% from the prior year. As shown on Page 17 of our presentation, B2B revenues were up 39%, primarily attributable to higher mortgage origination scores unit price, partially offset by a decline in mortgage originations volumes. Our B2C revenues were up 3% versus the prior year, primarily due to growth in our indirect channel.
Turning to B2B origination Scores revenues. Our fourth quarter mortgage originations revenue was up 72%. Volumes in Q4 declined by high single digits versus the prior year, driven by elevated interest rates. In the quarter, we saw no meaningful loss of volume to competition. In addition, we observed a mix shift from first-lien mortgages to HELOC as Q4 HELOC volume growth accelerated from Q3 level. Because the average price for HELOC is lower than first-lien mortgages, our total mortgage origination scores average price declined sequentially from Q3 to Q4.
Refer to Page 18 to see a comparison to the prior quarter mortgage originations revenue growth. Mortgage originations revenue accounted for 67% of B2B revenues and 58% of total Scores revenues in Q4. Auto originations revenue was up 11% and credit card, personal loan and other originations revenue was up 12% versus the prior year. For your reference, Page 19 of our presentation provides quarterly trending for Scores segment metrics.
Turning to our Software segment. Our software ACV bookings for the quarter were $45 million, as shown on Page 20 of our presentation. On a trailing 12-month basis, ACV bookings reached $140 million this quarter, an increase of 36% from the same period last year. This is the strongest annual performance in FICO history, and we continue to see strength in our sales pipeline. 
Our total software ARR, shown on Page 21, was $851 million, a 14% increase over the prior year. Platform ARR grew 72% versus the prior year to $453 million and now represents 53% of our total Q4 '26 ARR, while non-platform declined 18% to $398 million this quarter.
Excluding migrations, platform ARR growth was in the mid-40% range, reflecting strong execution and new customer wins as well as expanded use cases and volumes from existing customers. In our non-platform business, ARR declined year-over-year, driven mostly by migrations and to a lesser extent, end-of-life products. Our dollar-based net retention rate in the quarter was 112%. Platform NRR was 156%, while our non-platform NRR was 82%. Platform NRR was driven by a combination of new use cases, increased usage of existing cases and some migrations.
Fourth quarter Software revenues, detailed on Page 22, were $243 million, up 19% versus the prior year. Within the segment, our SaaS revenues grew 29%, driven by continued strength in FICO platform with a smaller contribution from CCS. On-premises revenue grew 13%, driven by higher point-in-time revenues compared to the prior year quarter. Platform revenues grew 84%, driven by success in our land and expand strategy and by migrations. Excluding migrations, platform revenues grew in the low 50% range. Non-platform revenues declined 12%, driven mainly by migrations, offset partially by higher point-in-time revenue. As a reminder, platform and non-platform revenues exclude professional services revenues.
From a regional perspective, 89% of total company revenues this quarter were derived from our Americas region, which is a combination of our North America and Latin American regions. Our EMEA region generated 7% of revenues and the Asia Pacific region delivered 4%. Operating expense was $390 million, up 25% from the third quarter. That includes a $65 million accrual for the proposed settlement of the antitrust class action lawsuit related to our Scores business and a $27 million restructuring charge for our workforce reduction. Both are excluded from the non-GAAP results and are shown on Pages 23 and 24.
Operating expense, excluding these items, was $298 million for the quarter, down 4% sequentially on lower personnel costs. Excluding these items for the full year, expense grew 12% to $1.177 billion. Through strategic partnerships with third parties and AI-driven efficiencies within our FICO platform, we anticipate a significant decline in professional services revenue for FY '27. And as such, professional services roles were impacted as part of the recent restructuring.
In FY '27, we plan to continue to shape our workforce around the skills our strategy requires, hiring for the capabilities we need and investing in AI tools that make our teams more productive. Other income and expense for Q4 was a net expense of $29 million. This included an interest expense of $78 million, up from the prior quarter reflecting a full quarter of interest on the June 2026 term loan that funded our accelerated share repurchase. It also included a $48 million non-operating gain on the sale of a minority equity investment, which is excluded from our non-GAAP results. 
Our non-GAAP operating margin, as shown on Page 25, was 61% for the quarter compared with 54% in the same quarter last year. Our full year non-GAAP operating margin was 61% compared to 55% in the prior year, an improvement of approximately 600 basis points. 
The effective tax rate for the quarter was 26.3%. Our full year net effective tax rate was 24.1%, while the operating tax rate was 26%. As a reminder, the key differences between the operating tax rate and net effective tax rate was a $17 million excess tax benefit. In FY '27, we expect a full year operating tax rate of 26%. 
At the end of the quarter, we had $269 million in cash and marketable investments. Our total debt at quarter end was $5.26 billion with a weighted average interest rate of 5.64%. As of September 30, 2026, 64% of our debt was held in senior notes, while 36% of our debt was held in term loans or a balance on a revolving line of credit, both of which are repayable at any time. 
We repurchased $3.028 billion of stock in FY '26, which represented approximately 10% of shares outstanding from the end of fiscal '25. And as Will highlighted, although we continue to pay down debt, we continue to view share repurchases as an attractive use of cash.
And with that, I'll turn it back to Will for comments.

**William Lansing** (Executives):
Thanks, Steve. We are transitioning to custom mortgage originations pricing tailored to the individual needs of our customers. One bespoke pricing program, the FICO preferred program, has had several deals already announced, and we continue to work with others on programs that will cover calendar year 2027. At the same time, elevated interest rates and ongoing affordability challenges continue to weigh on the mortgage market, keeping loan originations below historical norms. We are in the middle of this pricing transition where programs and agreements are still being finalized, and the outcomes of mortgage market challenges are uncertain. Because of these factors, we are not providing fiscal year 2027 guidance at this time.
I recognize that this is not what you were expecting to hear from us today. And I want to emphasize that it does not reflect a change in our long-term confidence in our business. FICO closed fiscal 2026 as the most successful year in our history, and the foundation behind those results is durable. For more than 70 years, FICO has been the trusted backbone of high-stakes decision-making, and we expect to remain the industry standard in credit scoring and a leader in AI decisioning intelligence platforms for financial services. We feel positive about the long-term outlook for our business, and we remain focused on executing our strategy with discipline.
With that, I'll turn the call back to Dave, and we'll open up the Q&A session.

**Dave Singleton** (Executives):
Thanks, Will. This concludes our prepared remarks. We're now ready to take questions. Operator, you can please open the line.

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Manav Patnaik of Barclays.

**Manav Patnaik** (Analysts):
Will, I was just hoping in terms of the custom pricing program you're referring to. I know you mentioned preferred a few times. I'm just wondering, looking into next year, how many different programs do you think you're going to have there? And if you can give us a little bit of color, and how we should think about that?

**William Lansing** (Executives):
Well, there are a number of different programs, some of which we've announced and some of which we're still working on. And we will make additional announcements as appropriate. But there are multiple programs.

**Manav Patnaik** (Analysts):
Okay. Any just, I guess, broad color on how the -- like it sounds like preferred program is your preferred target, though?

**William Lansing** (Executives):
Manav, I -- for some reason, the questions are coming through very muffled. Could you just repeat that, please?

**Manav Patnaik** (Analysts):
Just a question around the preferred program being your preferred program as well or not necessarily?

**William Lansing** (Executives):
Can you understand him?

**Dave Singleton** (Executives):
I think he's just asking a question about pricing and he wants to know about the preferred program is something we think that most customers will take.

**William Lansing** (Executives):
So the preferred program, okay, yes, I'm sorry, I couldn't really hear your question, Manav. The preferred program is enjoying popularity and we're in conversations with many lenders and originators about the preferred program and other options. We've had some uptake, as you've seen in our recent announcements. We anticipate additional uptake. So yes, I would say that the preferred program is a popular one, though not the only one.

**Operator** (Operator):
Our next question comes from the line of Simon Clinch of Rothschild & Co Redburn.

**Simon Alistair Clinch** (Analysts):
I wanted to just follow up on Manav's line of question there, Will. I mean, if -- maybe you could talk about the kind of pain points that you're trying to solve with the various number of different programs that you're exploring. And I was wondering in these discussions, whether or not your lender partners or lender customers actually sort of raising the -- are using, say, VantageScore, as a point of negotiation or anything like that? I was just curious about that kind of color.

**William Lansing** (Executives):
Well, I'm not sure I would describe anything we're doing is responding to pain points. I think that the way to think about this is, historically, we've had a one-size-fits-all, and it's been -- here's the score price, and here you go. And pretty much everybody had the same program. And we're in a very different kind of a mindset now. 
I think we're trying to be more responsive to our customers, to our customers' needs, give them more options, more flexibility, let them do more of what they want to do. And as long as we can accommodate that, we're really flexible about how we take our IP to market. And as you know, just from -- over the last year or 2, we've talked about a lot of alternative models for bringing our IP to market. And so this is the beginning of some of that. I think that if you look at the construct of the preferred program, which we've announced, I think it's pretty obvious why it's appealing to the customers who signed up for it. And I think that some of the other programs are designed to appeal to other needs.

**Simon Alistair Clinch** (Analysts):
Just a follow up, Will. On the preferred program. Is there like a contracted period, which -- like do you have to sign up for a year? Is it 3 years? Or is it various depending on the customer?

**William Lansing** (Executives):
The term varies depending on the customer and the specific arrangement. As I said, these things are really bespoke, they're very customized. There are some annual arrangements, and then there are other arrangements. So yes, I would say that it's not one size fits all. It's very custom and tailored to each customer's needs.

**Operator** (Operator):
Our next question comes from the line of Jason Haas of Wells Fargo.

**Jason Haas** (Analysts):
I'm curious if you're seeing any issues that lenders are having in terms of like downstream uses of VantageScore, which would cause them to need to use FICO, whether it's the MBS market or anything else? Anything that you could point to there?

**William Lansing** (Executives):
Well, all this data is public and available, and I'd encourage you to go and look at it yourselves. Near as we can tell, FICO is used in most cases in the secondary market. And so any kind of problems with Vantage there, I think you got a consult with Vantage.

**Jason Haas** (Analysts):
Got it. Okay. We'll take a look there. And then can you just give us an update on time line for implementation of the direct licensing program? And also any expectation for 10T approval by the FHFA?

**William Lansing** (Executives):
Sure. I appreciate those questions. So I'll take them one at a time. So direct license program, the preferred program that we announced recently is a direct license program. It's done through direct license, through the tri-merge resellers. So that is an example of the direct license program up and running.
The only thing that's not happening in that from a direct license standpoint that we've talked about previously is the computation of the score by the tri-merge resellers, that's still pending approval from the GSEs. But in all other respects, the direct license program is live. We -- and we're really excited and pleased with this. I mean our goal was to develop an alternate channel for bringing our IP to market to be able to work with the tri-merge resellers. And that's exactly what's occurring now. 
And it's -- obviously, it's terrific for bringing mortgage scores to market, and that's their primary business. But it's also an opportunity for us to bring other kinds of IP to market. And we have -- in the tri-merge resellers, we have very willing and enthusiastic channel partners. So the direct license program is live. It's just not live in all the incarnations we've talked about. 
In terms of 10T, is still under review by the GSEs. It was approved in 2022. And now it's going through another cycle of evaluation with the GSEs. You have access to the third-party studies and data that have been made public. You know that 10T is the most predictive score out there. It is a modern credit score. It does incorporate rental data. It is most predictive on credit default risk. It's most predictive on prepayment risk. So we're very excited about the value proposition represented by 10T. 
It's being used in some parts of the market, but not all. So in the non-conforming market, we have over 80 lenders who've now taken it, are using it. It's either from an evaluation standpoint or some of them are making credit decisions with it. You know that the FHA has decided to use 10T starting January 1, 2027, and that's in their total credit decisioning. So we are still waiting for GSE approval and, I guess, implementation because theoretically, it's been approved. It's just not implemented. But we have a lot of optimism about the future of 10T.

**Operator** (Operator):
Our next question comes from the line of Jeff Meuler of Baird.

**Jeffrey Meuler** (Analysts):
Is anything resembling the prior performance model still on the list of program options for calendar year '27 pricing?

**William Lansing** (Executives):
Yes. We have not withdrawn that model. That model we described it last year, and we're excited about getting it to market. And it's still pending certification and approval from the GSEs, but we have not, in any way, formally withdrawn that model. Now whether that model is superseded by other models that we're working with right now, that's for the market to decide. But the performance model is still an option.

**Jeffrey Meuler** (Analysts):
Got it. And do any of the new programs changed the client use or reuse rights of FICO scores? And as a part of that, do you tap into any new payer types beyond the underwriting lender?

**William Lansing** (Executives):
The short answer to that is not at this time.

**Operator** (Operator):
Our next question comes from the line of Surinder Thind of Jefferies.

**Surinder Thind** (Analysts):
Will, earlier you mentioned just the 10T going live with FHFA at the beginning of the new year in '27. Can you maybe help us understand how the FHA uses the credit scores or how many pulls? Because at the same time, my understanding is that VS4 will also go live on January 1. And now you have a situation where there's multiple scores available to the FHA.

**William Lansing** (Executives):
The FHA uses 10T as part of a broader credit evaluation. So it's part of the total credit evaluation.

**Surinder Thind** (Analysts):
Got it. I guess is the implication that they're going to pull both scores. Is that -- I'm just trying to understand how the total credit evaluation works. I guess that was...

**William Lansing** (Executives):
I can't tell you exactly how that's going to work. A lot of that is their secret sauce.

**Surinder Thind** (Analysts):
Got it. Okay. That's helpful or understood. And then I guess in terms of just any update in terms of conversations with the regulators at this point, whether it's, I guess, the approval for 10T or the implementation, I guess, technically or the tri-merge to bi-merge. Just any other topics that are that are up in the air or just what may be going on behind the scenes, if there's anything to note or highlight there?

**William Lansing** (Executives):
I wish there were things to note and highlight there. We continue to have conversations with them, and there is progress being made and they're working through their own process. And I'm confident that we'll get to where we need to get to, but I don't really have an update for you right now.

**Operator** (Operator):
Our next question comes from the line of Ashish Sabadra of RBC Capital Markets.

**Ashish Sabadra** (Analysts):
Another question on pricing. As you think about all these different pricing strategies, net-net, even on a blended basis, would pricing be flat, up or down next year depending on different adoption profiles for different strategies?

**William Lansing** (Executives):
Ashish, I guess I can't blame you for asking the question, but maybe it's time for me just to explain a little bit of a change in philosophy, and how we talk about our pricing and our programs and so on. 
I know -- I think you all know. It is no secret that transparency and detail on our programs and pricing have not been particularly helpful for FICO. We were of a view for many years that because the FICO score at $10 or $4.95 or whatever we were charging, was such a tiny fraction of overall closing costs. We really didn't think that the price was a very big deal. We thought that the value so far exceeded the price that why not share details around the pricing, just so that everyone understands how little it is in the scheme of things. 
And as you all know from watching events over the last several years, we've really been attacked for what we consider to be not very good reasons. We're attacked because we're transparent and clear about our score price. And as you all know, the credit files costs a lot more, credit evaluation costs are much more. In fact, every other element of the closing is a lot more than what FICO charges. And yet somehow FICO has become the poster child for affordability in housing, which is just a crazy thing.
So internally, we've had a lot of conversations about, has this transparency been helpful? And the conclusion is, no. It has not been helpful. And I think you guys know that we've probably been in the top decile of open transparent, help everyone outside understand what we're doing inside. But it hasn't really worked very well for us. And so on a go-forward basis, our intention is to not share every detail. We're not going to share every pricing program. We're not going to share what the prices are. We're not going to share all the terms. They're going to be customized by customer to meet customer needs. And we're just not going to provide all that kind of information. 
So to your very specific question, as the average price of FICO going up, down or sideways, we're not going to answer that. And you guys who have been watching us and watching the industry can understand exactly why we're not going to answer that.

**Ashish Sabadra** (Analysts):
That's very helpful color. Maybe just, again, on the EPS, we appreciate the current environment makes formal guidance challenging. But just Wondering if you could provide some high-level goalpost around EPS expectations. Is that -- can you continue to drive earnings growth in '27 with all these moving pieces?

**William Lansing** (Executives):
We're not going to provide guidance at this time. Now as things come into more focus as we work through the different programs and pricing and terms and watch industry volumes and so on, we'll be in a better position to share guidance with you, but we're not ready to do that at this time.

**Operator** (Operator):
Our next question comes from the line of Faiza Alwy of Deutsche Bank.

**Faiza Alwy** (Analysts):
Okay. I'm going to try and ask the same question in a different way. I guess, Will, you said in response to a prior question that it's obvious that the preferred program is appealing to customers, and it does seem appealing. And I'm just curious as we're thinking about the model and about 2027, like what are some of the reasons that you might be hearing why someone might not want to sign up for the preferred program, and you said there may be other programs that are designed to appeal to those other needs. 
So maybe talk about some of those other needs and give us some perspective on what you're seeing? And I guess, is the worst-case scenario essentially that there is no pricing and everyone goes with the preferred program in addition to just lower volumes due to mortgage rates?

**William Lansing** (Executives):
Well, so I can't tell you what the uptake rate will be on the preferred program. Yes, it is popular. And we're happy that it is and for some of the major lenders who are signing up, we're sharing that with you all. So you have a sense for the popularity of it. But we're not going to go into details on the other programs. And for the reasons that we just explained, we're just -- I'm sorry, that we're not going to be in a position to give you that detail.

**Faiza Alwy** (Analysts):
Okay. Okay. Understood. Let me ask you then, obviously, you've had this restructuring program. Maybe you can talk about the level of savings that we should expect from the restructuring program in 2027? Maybe as we think about just the actual reported savings versus what the run rate savings might be exiting the year? And how we should think about -- will those flow through to the bottom line? Or should we expect those to be reinvested?

**Steven Weber** (Executives):
Yes. I mean, I think you can expect a lot of it we invested. As you saw over the course of the year, we had -- our expenses ramped up throughout the year. We bought a couple of smaller companies and absorb those expenses. We've seen some expenses in AI. So a lot of this is reallocating our resources. And as we go live with Northstar project, there's things that we were done with, right? 
And we talked a little bit about professional services. We don't need as much implementation. So this is a great opportunity to reallocate some resources into distribution and other things. So when I'm going to talk about specific dollar amounts at this point, we'll discuss that more as we move through the year. But that's a lot of -- it's just a general reevaluation of our needs and reallocating the resources accordingly.

**Operator** (Operator):
Our next question comes from the line of Alexander Hess of JPMorgan.

**Alexander EM Hess** (Analysts):
I wanted to just start with the preferred program. I know there's been a lot of questions on it. But my understanding, and correct me if this is wrong, guys, is that the preferred program involves you guys holding price at $10, but -- and giving the client both a classic FICO and a FICO 10T inquiry score for the price of one. But the existence of carrot, if you'll excuse the metaphor, sort of implies the existence of a stick. And I think that's sort of what people are trying to get at. Again, sorry for the metaphor, but how to think about why somebody would choose this versus another program at a high level? Or anything you can provide there would be great.

**William Lansing** (Executives):
Yes. I guess I don't really see the stick. There's nothing exclusive about the preferred program. I mean you can participate in the preferred program and still buy, VantageScore, you can still do all the gaming that has been talked about in the industry, which I think is a real thing. But there's -- so I don't really see a stick.
And -- so I think there's a lot of popularity there because it looks a lot like business as usual. It looks a lot like what our customers have been doing. And it does provide a level of price certainty and price stability for customers. So that part that you mentioned is absolutely accurate. But I think that's why they're going for it.

**Alexander EM Hess** (Analysts):
Understood. Maybe just to reframe my question a little bit. I think, well, what I was trying to get at was, the customer is being asked to give up something of value, which is committing to FICO for every pull. So that was sort of what I thought was the carrot was flat pricing in exchange for that, but maybe there was -- that implies something else about the -- what other programs are available. 
I hope you -- that's where my thinking was. But maybe to switch gears and ask Steve a question. Steve, I know you're not providing guidance at this time, but just any dimensions, any color you can share about what you expect ex mortgage for the business in the fiscal year ahead. Just some thoughts there? I know we're not talking specifically on mortgage loan guide...

**Steven Weber** (Executives):
Yes, we don't. Frankly, it's -- as you're familiar with us from following us for several years. With the way we guide is we guide the whole company. So to parse the piece of that out, we were able to guide the whole company because we have 2 different pieces, and we can kind of balance puts and takes on both sides. So it's pretty difficult to guide half of it, and we're not going to do that at this point.

**Operator** (Operator):
Our next question comes from the line of George Tong of Goldman Sachs.

**Keen Fai Tong** (Analysts):
You're using several bespoke programs to secure mortgage volumes under various different pricing arrangements. Across those programs, what portion of 2027 mortgage originations do you expect to have under committed agreements?

**William Lansing** (Executives):
George, I guess, I would just go back to the comments I made earlier about how we're not going to break out all this kind of detail. We're not going to provide details on these other programs or the pricing on the other programs or the percent that goes into one program versus another. It's just something we're not prepared to do. Hasn't helped us in the past. We don't believe it's helpful in the future. So I'm sorry, I can't answer that question for you.

**Keen Fai Tong** (Analysts):
Understood. And then with respect to guidance, what specifically needs to fall into place for you to provide fiscal 2027 guidance? And is it possible you won't provide guidance at any point this year?

**William Lansing** (Executives):
I think it's likely that we will be providing guidance as we have more of the pricing out. I mean, remember, our fiscal starts 10/1, and our pricing happens Jan 1. And so we're right now in the middle of negotiations, discussions on different kinds of arrangements with a whole bunch of different lenders and originators. And so now is not a good time for us to be -- especially given all the fact that there are multiple programs, not a good time for us to be trying to put a lot of fine points on it. I think as we progress through the year, we'll be in a much better position to do that.

**Operator** (Operator):
Our next question comes from the line of Ryan Griffin of BMO Capital Markets.

**Ryan Griffin** (Analysts):
Just wondering if we should be thinking about 2027 as a year for 10T adoption in the markets where it's available? And then what are you hearing from the lenders ahead of the January 1 date on the preference versus 10T and VantageScore.

**William Lansing** (Executives):
I think 10T will -- 10T is the best score available. I mean it is far and away the best score available, and it's making inroads a bit here, a bit there, a bit here, a bit there. And yes, everyone is waiting for GSEs to sign off finally so that the conforming market can use it. But all the trend and momentum is in the direction of 10T adoption, and I think 2027 will be a big year for 10T.

**Ryan Griffin** (Analysts):
And then can you provide any updated thoughts on just score gaming and the unified LLPA grids?

**William Lansing** (Executives):
Yes. A couple of comments. We said before and we continue to believe that gaming is real. I think when you have a 2 score system, one score or the other score is inevitably going to provide -- sometimes it's a tie, but sometimes one score provides a better price than the other score. So the gaming is real. And I think that it would be naive to expect it to go away under today's environment. In terms of a unified LLPA grid, I think if you talk to anyone in the industry, with kind of a data and science background, they would tell you that a unified grid doesn't make a lot of sense. The combination of 2 very different scores in a single grid means that you're going to be underpricing one or the other of them. 
And in this case, Vantage is not being priced properly for risk. It's being underpriced. That's just a reality. I think we all know why that's happening. And I assume also that sooner or later, adjustments will be made because it's not very good for the GSEs. There's a subsidy involved when you underprice risk. So we will see how this all unfolds. But the gaming is real, absolutely.

**Operator** (Operator):
Our next question comes from the line of Owen Lau of Clear Street.

**Owen Lau** (Analysts):
It doesn't look like people are interested in software, but platform ARR grew 72% year-over-year. Could you please talk about the traction there? What are the use cases that resonate with clients driving this strength? It doesn't look like AI has been impacting this business.

**Nikhil Behl** (Executives):
Owen. This is Nikhil Behl. I run the software business here at FICO. Thanks for your question. So Owen, we are predominantly on the retail banking side of most financial institutions globally. And we provide intelligent solutions that they can implement across the entire consumer life cycle. And we see fairly good adoption of the FICO platform across multi segments of that life cycle. So whether it's in originations or in customer management or in fraud protection or in compliance or in credit collections, we go across the life cycle. And we've seen really good adoption for the platform across those use cases, particularly because they are starting to find real benefit in the platform as they expand from their original land use case. 
The more use cases they put on the platform, the better each and every platform use case gets both the initial solutions as well as the incremental solutions that they're adding on top of it. And as our customers start to see the benefit of that strategy and that investment, their uptake from an expand perspective continues to get better. And we're seeing that strategy work, which is why you're actually seeing our numbers perform the way in which they're performing.

**Owen Lau** (Analysts):
Got it. Just a quick follow up, Will. Does your custom pricing strategy only applies to mortgage or it also includes like card, auto and others?

**William Lansing** (Executives):
It's primarily mortgage, but we are exploring all options. I think that we want to be responsive to the market. We want to be responsive to our customers. And we have, over the years, tried different kinds of things on a kind of a one-off basis with different customers. But I think there's a real value for us in customizing the delivery of our IP to meet the needs of individual customers. And so I think you'll see more and more of that. But the programs we've been talking about today are primarily mortgage.

**Operator** (Operator):
Our next question comes from the line of Patrick O'Shaughnessy of Raymond James.

**Patrick O'Shaughnessy** (Analysts):
To the best that you can gather, how is your market share trending in non-conforming mortgages, auto and credit card? Is VantageScore's introduction into the conforming mortgage ecosystem impacted other parts of the Scores business?

**William Lansing** (Executives):
We have not seen any, no.

**Patrick O'Shaughnessy** (Analysts):
All right. I appreciate that. And then a question on software and your restructuring efforts there. Do you have like a targeted margin profile that you want to end up with on the other side of the restructuring effort?

**William Lansing** (Executives):
We do, although I wouldn't say that we've been public about it. We don't publish a target. I think we've always said and we continue to say that our goal is to balance growth with margin expansion. And right now, we're achieving both. So it's kind of a two-pronged effort where we want to see the revenue growth rates continue at the very high. They may not stay at the high levels that they're at right now. I mean they're quite high. For a software company, our size to be growing at our speed is fairly remarkable. But as we scale our margins improve, and so we anticipate both improvement in margin and improvement in growth rate.

**Steven Weber** (Executives):
Just to add to that, the restructuring was not done with a specific margin target in mind. It really was done serve the needs of the business and to reallocate resources, like I said before. It's an evolution of that business. And as it evolves, we allocate resources in different ways. It wasn't like we were trying to take a certain amount of expense to hit a certain margin number.

**William Lansing** (Executives):
I mean I would say we invite you to evaluate us by the Rule of 40.

**Operator** (Operator):
Our next question comes from the line of Kyle Peterson of Needham.

**Kyle Peterson** (Analysts):
I wanted to stay on the software theme here. Obviously, in FY '26, the platform ARR, even kind of ex-migration seem to accelerate year-on-year as the year progressed, I guess. Is the 4Q kind of that mid-40s year-on-year growth rate? Is that a reasonable baseline to expect from here given the good things you guys have going on there? Or how should we kind of think of the platform ARR growth ex-migrations?

**Steven Weber** (Executives):
Well, we don't -- we're not giving forward-looking views on the platform growth. Frankly, we've got some projections for it, but it's difficult to know exactly what quarters the numbers are going to be. But we do expect very high platform growth rates going forward into '27?

**Nikhil Behl** (Executives):
Our demand continues to remain strong, and our pipeline is strong as well, and we continue to expect to see good product market fit with our platform. And as Will mentioned earlier, we just launched our next-generation FICO platform, and we expect to see good uptake of that over the coming quarters.

**Steven Weber** (Executives):
And you see there's the high ACV bookings. Obviously, that leads to higher ARR next year.

**Kyle Peterson** (Analysts):
Okay. Okay. And then I guess switching over to capital deployment. Obviously, you guys made a good dent in the term loan this quarter. Is there a -- whether it's a particular leverage ratio or kind of share price versus interest? Like how are you guys kind of thinking about what you're going to evaluate and when you guys might step back into the market for buybacks?

**William Lansing** (Executives):
We certainly believe that our stock is quite a great value at these levels. We're -- because of the ASR, we're paying down some debt to get to a leverage ratio that's a little bit more comfortable. But you can absolutely expect us to be back in the market and using our free cash flow to retire shares. And we're as committed as we've ever been and the opportunity, the margin for our stock is as great as it's ever been. And so you can count on us to be back in. But as we said before, this is a 1- or 2-quarter thing while we bring down our leverage.

**Steven Weber** (Executives):
Yes. And we were able to bring it down quite a bit just this last quarter. Obviously, we're driving a lot of free cash flow and our EBITDA is growing so that we delever pretty quickly. But we don't put a time line on that, but we're -- in the meantime, we're trying to pay down as much as we can as quickly as we can.

**Operator** (Operator):
Our next question comes from the line of Curtis Nagle of BofA.

**Curtis Nagle** (Analysts):
Maybe I'll just start with the mortgage question and ask a question that's been asked maybe a bit differently. But on this transaction or transition, I should say, the bespoke pricing by customer, I suppose philosophically for FICO is the goal to optimize for pricing for volume? How should we think about that?

**William Lansing** (Executives):
Well, I think we take it all into account. Obviously, we want to retain as much volume as we possibly can in the face of competition from Vantage. And the price is something that varies by program and is also designed around that. I mean, we certainly have profit, EPS commitments to our shareholders. And so that also is taken into account. And we try to optimize around both of those factors.

**Curtis Nagle** (Analysts):
Okay. Fair enough. And then maybe somewhat of a mechanical question, but as we kind of talked about the software growth rates are impressive. What drove, I guess, just such a sharp and material acceleration in both the ARR and maybe more specifically the converted revenue in the fourth quarter?

**Nikhil Behl** (Executives):
ACV bookings.

**Steven Weber** (Executives):
Yes. I mean you've seen the bookings we've had for the last 1.5 years have been pretty grown pretty remarkably. And those things come on, you start to see an acceleration in ARR. And then we've had the migrations from off the platform onto the platform. And at the same time, there's some point in time revenue that can add to some lumpiness. So if you take a look at all the different pieces, you can kind of parse us apart and see what's actually happening there.
But we were really focused on the recurring revenue piece and the ARR growth that happens is that recurring revenue piece. So we have a -- maybe Nikhil, you want to jump in on this, but we have a really good sales team that's taken the really good products we brought to market, and there's just a lot of demand in that space.

**Nikhil Behl** (Executives):
Yes, I would just go back to what I said earlier. I think we're seeing really good product market fit, and we're seeing our customers find value in the investments that they're making with FICO platform. In fact, I would say that it's -- we are recognized as the market leader. 
If you look at Gartner, Forrester or IDC, in all 3 of their AI decisioning platform studies, we are the market leader. And our customers are seeing the same thing. And the more they invest in the platform, the more return they get from the investment that they're putting on platform. So we've been seeing this momentum building over the course of the last 6 quarters or so, and we continue to see strong momentum in the future.

**Operator** (Operator):
Our next question comes from the line of Scott Wurtzel of Wolfe Research.

**Scott Wurtzel** (Analysts):
Just on sort of the outlook here and I understand the uncertainty right now around how pricing is going to shake out. But just wondering if you can kind of help give us any directional guidance on what you're assuming for volumes on the mortgage side for this year?

**William Lansing** (Executives):
No. We never have given that our kind of internal estimates on that out, and we're not going to start now. I think that you should do your own assessment of where you think industry volumes will be and you can take it from there. But no, we don't share our internal estimates.

**Operator** (Operator):
Our next question comes from the line of Kevin McVeigh of UBS.

**Kevin McVeigh** (Analysts):
I guess, Will, you mentioned pricing with clients this year. Has that exercise change relative to prior years, just given the shift in delivery to DLP as opposed to historically through the credit bureaus. And any puts and takes around those conversations, or is it pretty much the same cadence?

**William Lansing** (Executives):
Yes. Thank you for the question. It has changed quite a bit. So if you go back in time, say, 5 years ago, we did not have a dedicated score sales force. We didn't have direct relationships with the end customers who are consuming our scores. We essentially went to market, dragged along by the bureaus, along with their credit data sales force. And so they would sell the credit file and the score for us. But we really had no efforts whatsoever of our own. 
And several years ago, we came to a view that, that really didn't make a lot of sense given the importance of the business, given the importance of the IP to those who consume it. We didn't think that we're getting the full benefit of what our IP might do for end customers because it really wasn't being communicated as well as we would have liked. 
And with all due respect to the bureaus, our channel partners, that wasn't their priority. I mean their priority is to sell their data and not to move FICO IP. And so we have very much changed the way we think about this over the last several years. We now have a dedicated software sales force. We now have direct relationships with the major customers for our Scores' IP. We are bringing to them all kinds of innovation that they never saw before. We are constructing much more complex arrangements that include IP across different software, different scores verticals, so beyond mortgage and into other scores vertical, but also leveraging other IP that we have. 
And so all of that has changed. And I would say for the better, very much for the better. Our customers are grateful for the attention they're getting from us. They're grateful for the opportunity to have input into our R&D and our IP development process. We have Scores Customer Advisory Board now where major players give us very, very direct feedback on the product, and what they'd like to see in future generations of it. So all that has changed dramatically in the last three years. So, yes, I would say -- and I would say the relationships are very strong, and we're happy.

**Kevin McVeigh** (Analysts):
Got it. And then just with some of the obviously pretty dramatic shift today post election, anything you'd expect on the regulatory side?

**William Lansing** (Executives):
I think your speculation is as good as ours. We're not in the business of speculating on political outcomes. Here's what I would say. I would say that the mortgage industry, multitrillion dollar industry, very, very important, relies on quality IP. All the models are built on quality IP, our IP. 
All of the industry would like to see the IP strengthened. And so there's a lot of pent-up demand for 10T. I believe that this year 2027 and in future years, demand for our IP to help lenders make better credit decisions to help investors evaluate the quality of the paper that they're buying. All that is -- it only becomes more pronounced in the future than it is today. 
And the tools that we're providing as a company to the industry, just keep getting sharper. We're getting better and better and better. Some of it is from leveraging incremental data sets, rental data is the example everyone talks about. But obviously, UltraFICO and the cash flow data we have there has a lot of signal in it. And I think that the appetite for what we do for using our IP to help with credit decisions is just getting stronger and stronger and stronger. And again, because of the cost of the IP relative to the value of not making a bad decision in a loan, it's just huge. And so that's how I look at it is I think there's just continued appetite for advances in the technology, and we are at the forefront of that.

**Operator** (Operator):
Thank you. Ladies and gentlemen, we have reached the end of our time. This does conclude today's conference call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FICO_Q3_2026_Earnings_Call_20260729.md
- 2026-07-29｜CEO｜guidance：FY2026營收財測上調至25.3億美元（原話："revenue guidance is now $2.53 billion, an increase of 20%"）
- 2026-07-29｜CEO｜guidance：非GAAP淨利財測上調至9.79億美元（原話："Non-GAAP net income guidance is now $979"）
- 2026-07-29｜CFO｜guidance：Q4營運費用預期略高於Q3（原話："modestly higher than in our third quarter"）
- 2026-07-29｜CFO｜guidance：Q4費用含一次性重組費用（原話："onetime restructuring charges"）
- 2026-07-29｜CFO｜guidance：Q4利息費用預期高於Q3（原話："we expect fourth quarter interest expense to be higher"）
- 2026-07-29｜CFO｜guidance：全年有效稅率預期約24%（原話："an effective tax rate of around 24%"）
- 2026-07-29｜CFO｜guidance：財測上調原因：DLP未上線而未遞延營收（原話："we would push some revenues out, more revenues out"）
- 2026-07-29｜CEO｜guidance：軟體訂單持續加速（原話："bookings, yes, we see continued acceleration"）
- 2026-07-29｜CFO｜margin：非GAAP營業利益率62%對去年57%（原話："was 62% for the quarter compared with 57%"）
- 2026-07-29｜CEO｜margin：長期焦點為利益率擴張（原話："our long-term focus is on driving margin expansion"）
- 2026-07-29｜CFO｜margin：軟體成本成長快於營收，預期明年利益率改善（原話："you're going to see the margin growth"）
- 2026-07-29｜CEO｜margin：平台開發資本支出需求有限（原話："This requires limited CapEx as we leverage"）
- 2026-07-29｜CFO｜margin：B2B成長主因抵押貸款原始評分單價提高（原話："a higher mortgage origination score unit price"）
- 2026-07-29｜CFO｜margin：抵押貸款原始評分占B2B營收71%（原話："accounted for 71% of B2B revenues"）
- 2026-07-29｜CFO｜margin：抵押貸款量年增低個位數（原話："third quarter volumes grew low single digit versus the"）
- 2026-07-29｜CFO｜margin：抵押貸款營收成長放緩歸因利率上升（原話："As rates tick up, the volumes do slow down."）
- 2026-07-29｜CFO｜margin：管理層稱上季127%成長屬時點異常（原話："you see anomalies like last quarter"）
- 2026-07-29｜CFO｜margin：平台ARR首度超過非平台（原話："platform ARR dollars exceed non-platform ARR dollars"）
- 2026-07-29｜CFO｜margin：扣除遷移後平台ARR成長中30%（原話："platform ARR growth was in the mid-30% range"）
- 2026-07-29｜CFO｜margin：平台NRR 148%、非平台82%（原話："Platform NRR was 148%, while our non-platform NRR was 82%."）
- 2026-07-29｜CEO｜risk：利率與負擔能力壓抑抵押貸款量（原話："Elevated interest rates and ongoing affordability challenges"）
- 2026-07-29｜CEO｜risk：Lender Choice被視為壞政策（原話："We think it's bad policy because it encourages gaming"）
- 2026-07-29｜CEO｜risk：目前未見FICO查詢量流失（原話："No, we are not, which suggests that they're pulling both"）
- 2026-07-29｜CEO｜risk：管理層對監測量流失承認不易（原話："honestly, it's not that easy"）
- 2026-07-29｜CEO｜risk：trigger lead立法影響輕微（原話："we noticed a bit but I wouldn't say anything dramatic"）
- 2026-07-29｜CEO｜risk：管理層預期Vantage占比上限在20幾%（原話："we don't anticipate more than the 20s for Vantage share"）
- 2026-07-29｜CEO｜competition：與信用局互為夥伴亦在抵押貸款評分競爭（原話："we're now competing in mortgage scores"）
- 2026-07-29｜CEO｜competition：估計Vantage抵押債券溢價約30基點（原話："the theory behind the 30 basis points"）
- 2026-07-29｜CEO｜competition：10T預期與classic及Vantage並存（原話："you'll have classic and Vantage and 10T"）
- 2026-07-29｜CEO｜product：Milliman分析稱10T預測力優於Vantage 4（原話："10T delivers more than a 10% predictive advantage"）
- 2026-07-29｜CEO｜product：10T採用者計畫達70家貸款機構（原話："The program has grown to 70 lenders"）
- 2026-07-29｜CEO｜product：採用者計畫占前50大貸款機構量約55%（原話："represents about 55% of the volume generated"）
- 2026-07-29｜CEO｜product：UltraFICO處於採用早期（原話："we're still in the early days of"）
- 2026-07-29｜CEO｜product：新一代FICO平台預計年內GA（原話："we anticipate the general availability"）
- 2026-07-29｜CEO｜product：AI功能尚未驅動目前平台成長（原話："it's not yet because of AI"）
- 2026-07-29｜CEO｜product：10T目前與classic捆綁免費（原話："if you pay for classic, you get 10T free"）
- 2026-07-29｜CEO｜product：10T定價尚未定案（原話："we have not made final pricing decisions"）
- 2026-07-29｜CEO｜product：10T單獨收費可帶來營收跳升但非現行計畫（原話："One could easily imagine a revenue jump at FICO"）
- 2026-07-29｜CEO｜customer：DLP等待其中一家GSE認證（原話："We're literally waiting on certification from one"）
- 2026-07-29｜CEO｜customer：DLP原預期數月前上線（原話："we thought it would be live months ago but it's not"）
- 2026-07-29｜CEO｜customer：已簽經銷商涵蓋約60%量，談成後近90%（原話："bring us closer to 90% of mortgage volume once finalized"）
- 2026-07-29｜CEO｜customer：GSE何時接受10T由其自行決定（原話："That's on them and that's their schedule"）
- 2026-07-29｜CEO｜customer：績效模式並非人人喜歡（原話："is it for everyone? No, it's not"）
- 2026-07-29｜CEO｜customer：Accenture合作補足分銷弱點（原話："We're IP-rich and distribution poor"）
- 2026-07-29｜CEO｜customer：非平台遷移與終止銷售（原話："we have some products that are old in the tooth"）
- 2026-07-29｜CEO｜customer：不強迫遷移之舊說法（原話："we're not forcing migration"）
- 2026-07-29｜CEO｜customer：部分平台成長現來自遷移（原話："some amount of the platform growth is coming from migration"）
- 2026-07-29｜CEO｜customer：平台與非平台分歧將持續（原話："you will continue to see the divergence"）
- 2026-07-29｜CEO｜capital_allocation：Q3回購金額超過歷史單季紀錄三倍（原話："spending exceeding 3x the historical record quarter"）
- 2026-07-29｜CFO｜capital_allocation：近期以現金償債（原話："In the near term, we will be using cash to pay down debt."）
- 2026-07-29｜CFO｜capital_allocation：除ASR外近期不太可能再買股（原話："probably not likely we're going to buy any shares"）
- 2026-07-29｜CEO｜commitment：2027定價尚無可分享（原話："really nothing to share with you right now"）
- 2026-07-29｜CEO｜commitment：對Vantage占比保有多種回應空間（原話："we have lots of degrees of freedom in how to respond"）

### 問答異常語氣（迴避／改口／保留）
- FICO_Q3_2026_Earnings_Call_20260729.md｜問：Meuler：上季127%成長是否有時點因素｜答法：稱可能有時點與季結算差異，但表示無法取得信用局數據，未給具體解釋
- FICO_Q3_2026_Earnings_Call_20260729.md｜問：Clinch/Ashish：2027定價與對Vantage的因應｜答法：稱現在言之過早、無可分享，不給任何方向
- FICO_Q3_2026_Earnings_Call_20260729.md｜問：Craig Huber：DLP何時可上線｜答法：不給時點，僅稱在等GSE認證
- FICO_Q3_2026_Earnings_Call_20260729.md｜問：Kyle Peterson：回購暫停多久｜答法：稱下季再更新，僅說除ASR外不太可能再買

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
{"date":"20260710","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"VantageScore 4.0 在 GSE 房貸的實際「取量」5 年內受限，FICO 靠 90% 份額 + tri-merge 慣性 + FICO 10T 雙軌保住多數 Scores 量","columns":{"2Y 驗證點":"Scores 房貸量 YoY（剔價）≥ 0；tri-merge 要求未廢除","5Y 驗證點":"房貸 Scores 份額 ≥ 70%（vs 現 ~90%）","10Y 驗證點":"Scores 仍為結構性現金引擎、非萎縮","數字門檻 + 來源":"門檻：Scores 量 YoY ≥ 0 且 LLPA 對 VantageScore 折讓 ≤ 5bps。來源：FICO 10-K FY2025、Q2 FY26 8-K、FHFA/FHA tri-merge 立場（S1/S2）","漂移觸發":"連 2 季 Scores 量 YoY 10bps → H1 削弱、降 C（單季不觸發）"}},{"id":"H2","text":"Software Platform 成為第二成長曲線，Platform ARR 維持 +40%+ YoY，抵銷非平台 legacy 衰退","columns":{"2Y 驗證點":"Platform ARR YoY ≥ +40%；Software 整體 YoY 轉正加速","5Y 驗證點":"Platform ARR 佔 Software > 55%（現 44%）","10Y 驗證點":"Software 成為與 Scores 並列的第二引擎","數字門檻 + 來源":"門檻：Platform ARR YoY ≥ +40%（Q2 FY26 實際 +49%）；非平台 ARR 衰退 ≤ −10%/yr。來源：Q2 FY26 法說（S1）","漂移觸發":"連 2 季 Platform ARR YoY"}},{"id":"H3","text":"監管明朗化後估值自 Fwd PE 23.5x（FY27）re-rate 至資料壟斷同業區間 26–33x（非返回歷史 50–60x 溢價）","columns":{"2Y 驗證點":"FY+2 Fwd PE ≥ 26x；分析師中位目標價站回 $1,700+","5Y 驗證點":"穩定於 26–33x（SPGI 20–22x／MSCI 30–31x 之間偏上）","10Y 驗證點":"倍數不再受監管折價壓抑","數字門檻 + 來源":"門檻：re-rate 基準＝資料壟斷同業 26–33x（明確非歷史峰值）。來源：SPGI/MSCI 現 Fwd PE、FICO 歷史區間（S3）","漂移觸發":"監管利空落地 6 個月後 Fwd PE 仍"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"監管限價：Hawley→FTC/DOJ + 佛州 AG CID（2026-07-01 發出，8/5 回覆） + 潛在多州聯合，以「score 價 5 年漲 16 倍」為訴因促成 price cap／和解限價","columns":{"對應假設":"H1/H3","時間尺度":"⚡ 短期（8/5 CID 回覆即可觸發）","監測指標":"佛州 CID 是否升級為訴訟；FTC/CFPB 是否進入 NPRM；多州跟進","警戒閾值":"任一升級為正式訴訟或限價立法 → 連動減碼（見 §14b）"}},{"id":"R2","text":"VantageScore 取量 + MBA 遊說廢除 tri-merge（若成功直接拆掉三局捆綁的分銷慣性）；Equifax 主動價格戰（$4.50 + 免費贈送）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4–6 季）","監測指標":"Scores 房貸量 YoY（剔價）；MBA tri-merge 廢除倡議進度；前 20 大銀行切換數","警戒閾值":"連 4 季量 YoY 轉負，或 tri-merge 要求被鬆動 → 大動作"}},{"id":"R3","text":"卡貸/消費金融端 FICO 依賴度下降既成事實（JPM/BofA/Capital One 內部評分）擴散至更多場景；AI/ML 替代模型長期化","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"非房貸 B2B Scores 佔比趨勢；GSE 是否認可另類承保資料商取代 bureau score","警戒閾值":"非房貸 Scores 結構性萎縮 + ML 模型獲 GSE 認可（≥ 50% 機率）→ 砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"佛州AG CID（8/5）與Hawley/FTC調查未致限價、2026Q4 LLPA對VantageScore折讓≤5bps且tri-merge保留→加碼至核心；深回檔~$1,050亦為加碼窗","irr_base_pct":13.3,"ev5y_pct":81.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":5.9,"ev5y_pct":81.8,"irr_base_pct":13.3,"max_dd_pct":-52.0,"bull_5y_price":3630.0,"bear_5y_price":884.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"佛州AG CID（8/5）與Hawley/FTC調查未致限價、2026Q4 LLPA對VantageScore折讓≤5bps且tri-merge保留→加碼至核心；深回檔~$1,050亦為加碼窗","price_at_dd":1279.41,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FICO_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
