你是 stock-analyst **v20 判斷 agent**，標的 GM（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GM","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_net_sales_and_reve","label":"Total net sales and revenue (GAAP)","value":50015,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"GM Q3 2026 press release (SEC 8-K Ex.99)"},"note":"未查得"},{"id":"f_kpi1_ebit_adjusted_non_gaap_o","label":"EBIT-adjusted (non-GAAP operating profit proxy)","value":4106,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"GM Q3 2026 press release (SEC 8-K Ex.99)"},"note":"未查得"},{"id":"f_kpi2_ebit_adjusted_margin","label":"EBIT-adjusted margin","value":8.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"GM Q3 2026 press release (SEC 8-K Ex.99)"},"note":"未查得"},{"id":"f_kpi3_gaap_operating_income_co","label":"GAAP operating income (combined)","value":3598,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"GM Q3 2026 press release (SEC 8-K Ex.99)"},"note":"未查得"},{"id":"f_kpi4_adjusted_automotive_free","label":"Adjusted automotive free cash flow","value":5882,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"GM Q3 2026 press release (SEC 8-K Ex.99)"},"note":"未查得"},{"id":"f_kpi5_eps_diluted_adjusted","label":"EPS-diluted-adjusted","value":3.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"GM Q3 2026 press release (SEC 8-K Ex.99)"},"note":"未查得"},{"id":"f_kpi6_gmna_ebit_adjusted_margi","label":"GMNA EBIT-adjusted margin","value":8.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"GM Q3 2026 press release (SEC 8-K Ex.99)"},"note":"未查得"},{"id":"f_kpi7_wholesale_volume_total","label":"Wholesale volume (total)","value":1028,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"thousand vehicles","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"GM Q3 2026 press release (SEC 8-K Ex.99)"},"note":"未查得"},{"id":"f_kpi8_fy2026_guidance","label":"FY2026 guidance（更新後）","value":"EBIT-adj $14.5–15.5B；adj. auto FCF $11.5–12.5B；EPS-diluted-adj $12.75–13.75","period":"Q3 2026（公告於 2026-10-20）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（公告於 2026-10-20）","citation":"GM Q3 2026 press release (SEC 8-K Ex.99)"},"note":"共識 FY1 EPS 13.37（財報後 10-21 快照，見 consensus_revision）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-20","period":"2026-10-20","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_gm_gross_margin_pct","label":"GM 毛利率","value":5.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gm_operating_margin_pct","label":"GM 營業利益率","value":0.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gm_fcf_margin_pct","label":"GM FCF 利潤率","value":0.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tsla_gross_margin_pct","label":"TSLA 毛利率","value":18.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSLA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsla_operating_margin_pct","label":"TSLA 營業利益率","value":4.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSLA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsla_fcf_margin_pct","label":"TSLA FCF 利潤率","value":5.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSLA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amzn_gross_margin_pct","label":"AMZN 毛利率","value":50.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_operating_margin_pct","label":"AMZN 營業利益率","value":11.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_fcf_margin_pct","label":"AMZN FCF 利潤率","value":-0.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":76.11,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-3.25,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":35.5,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.37,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.42 → 13.37）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.2,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.11 → 15.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.82 → 16.82）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":13.37,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":15.14,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":16.82,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.53,"period":"2026-07-16 → 2026-10-21","unit":"%","basis":"FY1 共識 EPS 12.79 → 13.37（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":16.65,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝59.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":59.9,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.36,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝57.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":57.1,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.92,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝29.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":29.1,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":5.69,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 13.37，分子＝快照價 76.11","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.907,"period":"2026-10-22","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-22"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":104053.0,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 128772.0、現金 24719.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":877.45,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":170835.83,"period":"2026-10-22","unit":"USD m","basis":"市值 66782.83 ＋ 淨負債 104053.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":186269.54,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":189497.13,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.92,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 76.11 / W52 79.18 / W104 65.36 / W250 49.32 / W250 13週斜率 0.8%"},{"id":"f_ma_w52","label":"52 週均線","value":79.18,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":65.36,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":49.32,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.8,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"GM 2025 中國總銷量 1.9 百萬輛，市占 7.1%，較 2024 年增 0.1 個百分點","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"Our total vehicle sales in China were 1.9 million units resulting in a market share of 7.1% in the year ended December 31, 2025, representing an increase of 0.1 percentage points compared to the corresponding period in 2024.","as_of":"2026-01-27","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：中國、印度等低成本製造商已在新興市場成為競爭者並進入成熟市場，對 GM 定價、份額造成並預期持續造成顯著負面影響；另有科技公司支持的新創與非傳統競爭者進入","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"Manufacturers in countries that have lower production costs, such as China and India, have become competitors in key emerging markets and have begun offering their products in established markets, as well as low-cost alternatives to established entry-level automobiles. These actions have had, and are expected to continue to have, a significant negative effect on our vehicle pricing, market share, and results of operations in these markets.","as_of":"2026-01-27","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"GM 2025 全球批發量 3,799 千輛，較 2024 的 4,010 千輛減少；GMI 由 547 降至 503 千輛","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"GMNA 3,296 86.8 % 3,464 86.4 % 3,147 83.5 % GMI 503 13.2 % 547 13.6 % 621 16.5 % Total 3,799 100.0 % 4,010 100.0 % 3,768 100.0 %","as_of":"2026-01-27","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"GM 2026 Q3 美國銷量 670,974 輛，年減 5.5%；Cox 預估 GM 年初至今份額 16.7%，去年 17.4%；底特律三強 Q3 份額創紀錄低點","source":"DBusiness／GM Authority 2026 Q3 銷量報導","url":"https://www.dbusiness.com/daily-news/stellantis-sales-tick-up-3-in-q3-gm-sales-down-6-ford-sales-slip-6-6/","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"CPCA：2026 H1 三家中國車廠進入全球前十，BYD 全球份額 4.8%","source":"CarNewsChina 2026-08-05","url":"https://carnewschina.com/2026/08/05/three-chinese-companies-entered-top-10-global-automakers-by-market-share-in-h1-2026/","excerpt":"6 BYD 4.8% 7 Geely 4.6% 8 General Motors 4.5% 9 Chery 4.1% 10 Ford 4.1% 11 SAIC 3.7% 12 Suzuki 3.7% 13 Honda 3.4% 14 BMW 2.4% 15 Mercedes-Benz 2.3% 16 Tesla 2.1%","as_of":"2026-08-05","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"GM 10-Q（2026-06-30 期）稱四家信評機構目前皆給予投資等級企業信用評等；截至 2026-07-15 自 2025-12-31 起評等未變。","source":"General Motors Co Form 10-Q, period ending 2026-06-30 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0001467858/000146785826000051/gm-20260630.htm","excerpt":"all four credit rating agencies currently rate our corporate credit at investment grade","as_of":"2026-07-15","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"BCG 白皮書指歐洲汽車產能結構性過剩：以 80% 稼動率為基準，過剩逾 20%（約 540 萬輛/年）；此為歐洲，非美國。","source":"BCG white paper: Europe's automotive overcapacity imperative 2026","url":"https://www.bcg.com/assets/2026/white-paper-europes-automotive-overcapacity-imperative-2026.pdf","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"GM 2026 Q3 美國交車約 670,974 輛，年減約 5.5%（前年同期 710,347）；GM 歸因於 EV 市場縮小與停產車款，並稱最大量車款需求仍穩。","source":"General Motors Q3 2026 Earnings Preview (INDmoney)","url":"https://www.indmoney.com/blog/us-stocks/general-motors-q3-earnings-preview","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Barra 預期 2027 年表現更佳，來自熱銷 SUV 供給增加與次世代卡車平台定價能力提升。","source":"General Motors lifts 2026 outlook despite hit from electric retreat (Ground News)","url":"https://ground.news/article/general-motors-lifts-2026-outlook-despite-hit-from-electric-retreat","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Cox Automotive 預估 2026 年 8 月美國新車 SAAR 約 1,630 萬，7 月約 1,670 萬為年內最強；2027–2028 預測未查到。","source":"Cox Automotive Forecast August 2026 US Auto Sales Forecast","url":"https://www.coxautoinc.com/insights/cox-automotive-forecast-august-2026-us-auto-sales-forecast/","excerpt":null,"as_of":"2026-08-26","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"GM 10-K（FY2025）Item 3 揭露：與 Ultium Cells 合資廠有關的 TSCA 進口違規已於 2023-11 與 EPA 以同意協議和解，截至 2025-12-31 GM 已累計估計 $18.2 million 民事罰款，EPA 發出 TSCA 5(e) 命令前罰款將持續增加，由 GM 與 Ultium Cells LLC 連帶負責。","source":"SEC EDGAR｜GM 10-K FY2025 Item 3. Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"As of December 31, 2025, GM has incurred an estimated $18.2 million in civil penalties. These penalties, which will continue to grow until the EPA issues a TSCA 5(e) order, are assessed jointly and severally to GM and Ultium Cells LLC.","as_of":"2026-01-27","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"GM 2026 Q1 10-Q 提到 EPA 最終規則（生效 2026-04-20）廢除溫室氣體 endangerment finding 及相關車輛 GHG 標準；GM 預期部分美國排放標準因銷售組合可能不達標。","source":"SEC EDGAR｜GM 10-Q FY2026 Q1","url":"https://www.sec.gov/Archives/edgar/data/0001467858/000146785826000035/gm-20260331.htm","excerpt":"The Environmental Protection Agency (EPA) also finalized a rule (effective April 20, 2026) repealing its \"endangerment finding\" and removing greenhouse gas (GHG) regulations for light-, medium-, and heavy-duty on-highway vehicles on a retrospective and prospective basis.","as_of":"2026-04-30","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"GM 2025 年關稅對 EBIT-adjusted 衝擊 31 億美元；公司預估 2026 年衝擊 30–40 億美元。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"In 2025, impacts to earnings before interest and taxes (EBIT)-adjusted from tariffs were $3.1 billion. Based on the current tariff environment, we estimate that impacts to EBIT-adjusted could range from $3.0 billion to $4.0 billion for the year ending December 31, 2026.","as_of":"2026-01-27","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：關稅可能超出公司現有估計，減緩措施（調整美國生產計畫、減少或暫停部分進口）短期內無法完全抵銷；USMCA 檢討與部分關稅法律挑戰待決。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"We cannot predict with complete precision the breadth of tariffs and related costs that will impact GM in the future. As a result, the ultimate impact of tariffs on our business could exceed our current estimates","as_of":"2026-01-27","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 載明電動車電池原料加工與萃取集中於中國，可能受進出口限制或關稅影響；中美貿易緊張亦是中國業務風險。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"Processing and extraction of certain EV battery raw materials is currently concentrated in China and may be subject to import or export restrictions, and/or tariffs.","as_of":"2026-01-27","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"GM 預期取回約 5 億美元關稅退款（最高法院推翻 IEEPA 關稅），但 232 鋼鋁關稅仍適用；Q1 關稅成本約 2 億美元。","source":"Supply Chain Dive：GM forecasts $500M tariff refund, plans further mitigation efforts","url":"https://www.supplychaindive.com/news/gm-forecasts-500m-tariff-refund-plans-further-mitigation-efforts/818752/","excerpt":"Court invalidated IEEPA duties earlier this year, GM is still subject to Section 232 levies on steel and aluminum imports, which make up the bulk of its projected tariff impact, according to Jacobson. In Q1 alone, the company incurred a $200 million tariff bill, and that’s including the assumed $500 million in refunds, he added.","as_of":"2026-04-28","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"GM 2026 Q1 10-Q 新增中東衝突風險因子（涉及伊朗及鄰國），列出供應鏈與物流中斷、制裁限制交易、原料與能源成本上升等潛在影響。","source":"GM Form 10-Q for quarter ended 2026-03-31 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001467858/000146785826000035/gm-20260331.htm","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Reuters 報導（2025-11）：GM 要求數千家供應商把中國零件移出供應鏈，部分供應商期限為 2027 年；GM 於 2024 年底已提出類似要求。為匿名消息來源報導，非 GM 官方公告。","source":"Bloomberg Law / Reuters: GM Asks Suppliers to Pull Supply Chains From China","url":"https://news.bloomberglaw.com/international-trade/gm-asks-suppliers-to-pull-supply-chains-from-china-reuters-says","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261022","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"GM 與 Procura Auto Parts 的約 45 億美元安排：預先買入並融資關鍵零件庫存，使單一供應商中斷較不易停產；末期還款期限至 2029 年中。來源為二手摘要，發布日未明。","source":"CBT News: Inside GM's $4.5B strategy to supply chain","url":"https://www.cbtnews.com/inside-gms-4-5b-strategy-to-supply-chain/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"GM 2026 年關稅毛成本預估約 30–40 億美元；2025 年透過定價、產線調整與降本抵銷逾 40%。","source":"Nasdaq/Zacks: Will Tariffs Remain a Major Headwind for General Motors in 2026?","url":"https://www.nasdaq.com/articles/will-tariffs-remain-major-headwind-general-motors-2026","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"GM 將 Equinox 自墨西哥移至 Kansas City（2027）、Blazer 移至 Spring Hill（2027）；Buick Envision 下一代自中國移至美國（2028）；Ramos Arizpe 自 2027 起組裝 Aveo、Groove 取代中國進口，因墨西哥自 2026-01-01 對非 FTA 車輛課新關稅。","source":"Automotive Logistics / Investment Monitor","url":"https://www.automotivelogistics.media/nearshoring/gm-to-localise-chinabuilt-models-at-ramos-arizpe-as-tariffs-reshape-mexico-footprint/2671047","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"GMNA 2026Q3 營收約 414 億美元，年增 2.1%（前年同期 405.5 億）；增長來自全尺寸皮卡與跨界車批發量增加，中型皮卡與廂型車下滑；調整後 EBIT 率 8.7% vs 6.2%。","source":"GM Form 10-Q (period ending 2026-09-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001467858/000146785826000059/gm-20260930.htm","excerpt":"Total net sales and revenue $41,419 $40,551 $868 2.1%","as_of":"2026-10-21","retrieved_at":"20261022","affects":["valuation","moat_trend"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Cox Automotive 預測 GM 2026 年迄今美國市佔 16.7%（去年同期 17.4%），銷量約降 6%；Detroit 三大 Q3 市佔約 36% 創新低，亞系品牌過半，主因油電混合需求。","source":"GM Authority: GM 2026 calendar year sales expected to drop by 6 percent","url":"https://gmauthority.com/blog/2026/09/gm-2026-calendar-year-sales-expected-to-drop-by-6-percent/","excerpt":null,"as_of":"2026-09-25","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 3 月 GM 四品牌平均成交價 $53,474，年增 3.8%（GMC 單獨 -1.3%）。","source":"GM Authority: GMC average transaction price dips in March 2026","url":"https://gmauthority.com/blog/2026/04/gmc-average-transaction-price-dips-in-march-2026/","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"GM 10-K 風險因子：產業正經歷重大變動，除傳統對手外，另須因應新創與大型科技公司支持的軟體、叫車服務等非傳統競爭者，這些新進者以新技術、產品、直銷通路、交通方式與車輛所有權模式衝擊產業舊商業模式。","source":"SEC EDGAR GM 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"In addition to our traditional competitors, we must also be responsive to the entrance of start-ups and other non-traditional competitors in the automotive industry, such as software and ridesharing services supported by large technology companies. These new competitors, as well as established industry participants, are disrupting the historic business model of our industry through the introduction of new technologies, products, services, direct-to-consumer sales channels, methods of transportation, and vehicle ownership.","as_of":"2026-01-27","retrieved_at":"20261022","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"AlixPartners 全球汽車展望：中國車廠在智慧連網車的優勢來自速度、成本競爭力與組織敏捷度，並預期從軟體定義車走向 AI 定義車","source":"AlixPartners 23rd Annual Global Automotive Outlook (China)","url":"https://www.alixpartners.com/newsroom/press-release-the-23rd-annual-alixpartners-global-automotive-outlook-china/","excerpt":"organizational agility, particularly in the development of intelligent connected vehicles. These strengths position them well to compete globally, even as EV growth overseas becomes more measured.” Looking ahead, the Outlook highlights the industry’s next major technological shift—from software-defined vehicles (SDVs) to AI-defined vehicles (AI-DVs).","as_of":"2026-01-15","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"GM 10-K FY2025：車輛仍主要透過獨立授權經銷商網路銷售（GMNA 4,566、GMI 6,276 家），未見直銷轉型披露","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"We market vehicles and automotive parts primarily through a network of independent authorized retail dealers.","as_of":"2026-01-27","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"GM 訂閱／軟體收入：2025 年實現訂閱收入 $2.7B、遞延 $5.4B；2026 預期 $3.1B／$7.5B；Super Cruise $39.99/月（次級來源，未核原文）","source":"Automotive Addicts: GM's software and subscription business becoming new profit engine","url":"https://www.automotiveaddicts.com/119626/gms-software-and-subscription-business-becoming-new-profit-engine","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"GM 於 2026-07-21 發布 Q2 財報，第二度上調全年指引：EBIT-adjusted $14.0–16.0B（原 $13.5–15.5B）、調整後汽車自由現金流 $9.5–11.5B、調整後稀釋 EPS $12.00–14.00","source":"SEC 8-K GM Q2 2026 press release","url":"https://www.sec.gov/Archives/edgar/data/0001467858/000146785826000049/gmq22026pressreleaseandfin.htm","excerpt":"$14.0 billion - $16.0 billion $13.5 billion - $15.5 billion Adjusted automotive free cash flow $9.5 billion - $11.5 billion $9.0 billion - $11.0 billion EPS-diluted-adjusted $12.00 - $14.00","as_of":"2026-07-21","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師共識評級 Moderate Buy（28 位：17 Strong Buy、3 Moderate Buy、6 Hold、2 Strong Sell）；平均目標價約 $98.46，最高 $132（Barchart，日期為 Q1 後，約 2026 上半年）","source":"Barchart: General Motors stock analyst estimates ratings","url":"https://www.barchart.com/story/news/1606502/general-motors-stock-analyst-estimates-ratings","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Tigress Financial 於 2026-07-28 將目標價自 $92 上調至 $130（Strong Buy）；MarketBeat 引共識目標價 $101.41","source":"MarketBeat: General Motors price target raised at Tigress Financial","url":"https://www.marketbeat.com/instant-alerts/general-motors-nysegm-price-target-raised-to-13000-at-tigress-financial-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"JPMorgan 將 GM 目標價自 $110 上調至 $120；Wells Fargo 維持 Underweight、目標價 $61（MarketBeat 2026-07-22）","source":"MarketBeat: GM stock price expected to rise, JPMorgan analyst says","url":"https://www.marketbeat.com/instant-alerts/general-motors-nysegm-stock-price-expected-to-rise-jpmorgan-chase-co-analyst-says-2026-07-22/","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露多起集體訴訟仍在進行：Duramax 柴油排放集體訴訟（第六巡迴法院 2025-06 部分維持／部分撤銷並發回）及 8 速變速箱集體訴訟（2025-06 第六巡迴法院撤銷 26 個州子集團認證並發回）；公司無法估計可能損失。","source":"SEC EDGAR 10-K FY2025 Item 8 Note 16","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"In June 2025, the Sixth Circuit decertified all 26 state subclasses and remanded to the district court for further proceedings.","as_of":"2026-01-27","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-01-08 8-K：因消費者稅務優惠終止與排放法規放寬，北美 EV 需求 2025 年放緩；GM 主動縮減 EV 產能，Orion 廠轉產內燃機大型 SUV／皮卡，並把 Ultium Cells Lansing 廠權益賣給 LG Energy Solution。","source":"SEC EDGAR 8-K Item 8.01 (2026-01-08)","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000005/gm-20260108.htm","excerpt":"GM proactively reduced EV capacity, including by pivoting the Company’s assembly plant in Orion, MI from EV production to the production of full-size SUVs and full-size pickups powered by internal combustion engines","as_of":"2026-01-08","retrieved_at":"20261022","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"NHTSA 於 2026-08 對約 997,743 輛 GM 皮卡與 SUV（2021–2026 年式、L87 6.2L V8）展開工程分析，評估 2025 年召回修復是否有效。","source":"ARY News／Reuters 轉載：US opens probe into 1 million GM pickups, SUVs","url":"https://arynews.tv/us-opens-probe-into-1-million-gm-pickups-suvs-over-concerns","excerpt":null,"as_of":"2026-08-21","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"+","claim":"Cruise 相關證券詐欺集體訴訟（City of Hollywood Police Officers' Retirement System v. GM）：2026-02 E.D. Mich. 准許 GM 重新考慮動議，全數駁回對 GM 被告的剩餘主張。","source":"Paul Weiss：GM wins motion for reconsideration securing full dismissal of securities class action","url":"https://www.paulweiss.com/insights/client-news/gm-wins-motion-for-reconsideration-securing-full-dismissal-of-securities-class-action","excerpt":null,"as_of":"2026-02-11","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"經查近12個月（2025-10-22至2026-10-22）9份8-K，無 Item 2.01 併購交割；唯一資產處分為 Ultium Cells Lansing 廠權益售予 LG Energy Solution（2026-01-08 8-K 披露）。","source":"SEC EDGAR 8-K 申報清單／8-K 2026-01-08","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000005/gm-20260108.htm","excerpt":"we proactively reduced battery cell capacity, including by selling our interest in Ultium Cells LLC’s Lansing, MI facility to LG Energy Solution.","as_of":"2026-01-08","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K 載明 8 速變速箱集體訴訟於 2025-06 被第六巡迴法院撤銷 26 個州子集團認證並發回。","source":"SEC EDGAR 10-K FY2025 Item 8 Note 16","url":"https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm","excerpt":"In June 2025, the Sixth Circuit decertified all 26 state subclasses and remanded to the district court for further proceedings.","as_of":"2026-01-27","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"+","claim":"Cruise 證券集體訴訟於 2026-02 獲全數駁回（重新考慮動議）。","source":"Paul Weiss 客戶新聞","url":"https://www.paulweiss.com/insights/client-news/gm-wins-motion-for-reconsideration-securing-full-dismissal-of-securities-class-action","excerpt":null,"as_of":"2026-02-11","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"NHTSA 2026-08 對約 997,743 輛 L87 6.2L V8 車款展開調查，評估2025年召回修復成效。","source":"ARY News／Reuters 轉載","url":"https://arynews.tv/us-opens-probe-into-1-million-gm-pickups-suvs-over-concerns","excerpt":null,"as_of":"2026-08-21","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":5.74,"operating_margin_pct":0.98,"fcf_margin_pct":0.33,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TSLA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":18.85,"operating_margin_pct":4.61,"fcf_margin_pct":5.55,"rd_intensity_pct":7.46},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSLA","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AMZN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.25,"operating_margin_pct":11.52,"fcf_margin_pct":-0.49,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"GM"},"financial_history":{"ticker":"GM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":156735000000.0,"revenue_yoy_pct":null,"gross_margin_pct":13.39,"operating_margin_pct":6.58,"net_income":9934000000.0,"diluted_eps":6.13,"free_cash_flow":-5144000000.0,"fcf_margin_pct":-3.28,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":171842000000.0,"revenue_yoy_pct":9.64,"gross_margin_pct":11.14,"operating_margin_pct":5.41,"net_income":10127000000.0,"diluted_eps":7.32,"free_cash_flow":-3680000000.0,"fcf_margin_pct":-2.14,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":187442000000.0,"revenue_yoy_pct":9.08,"gross_margin_pct":12.49,"operating_margin_pct":6.82,"net_income":6008000000.0,"diluted_eps":6.37,"free_cash_flow":-5980000000.0,"fcf_margin_pct":-3.19,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":185019000000.0,"revenue_yoy_pct":-1.29,"gross_margin_pct":6.27,"operating_margin_pct":1.57,"net_income":2697000000.0,"diluted_eps":3.27,"free_cash_flow":1771000000.0,"fcf_margin_pct":0.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GM/GM_Q3_2026_Earnings_Call_20261020.md）

# Q3 2026 Earnings Call
**General Motors Company** | Earnings Calls | 2026-10-20

**Operator** (Operator):
Good morning, and welcome to the General Motors Company Third Quarter 2026 Earnings Conference Call. [Operator Instructions] As a reminder, this conference call is being recorded Tuesday, October 20, 2026. I would now like to turn the conference over to Ashish Kohli, GM's Vice President of Investor Relations.

**Ashish Kohli** (Executives):
Thanks, Amanda, and good morning, everyone. We appreciate you joining us as we review GM's financial results for the third quarter of 2026. Our conference call materials were issued this morning and are available on GM's Investor Relations website. We are also broadcasting this call via webcast. Joining us today are Mary Barra, GM's Chair and CEO, along with Paul Jacobson, GM's Executive Vice President and CFO. Susan Sheffield, President and CEO of GM Financial, will also be joining us for the Q&A portion. 
On today's call, management will make forward-looking statements about our expectations. These statements are subject to risks and uncertainties that could cause our actual results to differ materially. These risks and uncertainties include the factors identified in our filings with the SEC. Please review the safe harbor statement on the first page of our presentation as the content of our call will be governed by this language. And with that, I'm delighted to turn the call over to Mary.

**Mary Barra** (Executives):
Thanks, Ashish, and good morning, everyone. I want to begin by recognizing our employees, dealers and suppliers. It takes commitment, focus and resilience to deliver solid results quarter after quarter and year after year in this industry. The agility, teamwork and commitment have been exceptional, and I'm very appreciative. This year, through the third quarter, we have delivered $12.3 billion in EBIT adjusted, $12.2 billion in adjusted automotive free cash flow and $10.97 in EPS diluted adjusted, which is up more than 35% year-over-year. 
During the third quarter, our margins in North America were 8.7%, up 2.5 points year-over-year. The compelling products, technology and services we're delivering for customers around the world makes us confident in the consistent long-term growth of our earnings and cash generation as well as our ability to return capital to shareholders. 
Our track record of improved cash flow generation began 5 years ago, and we have responded by increasing our investment in the business and continually strengthen our balance sheet. Then, in 2023, we began using surplus cash to repurchase shares given our low valuation. Since that time, we have reduced our fully diluted shares by 37%. The new $20 billion multiyear authorization we announced today further demonstrates our Board's commitment. 
As this quarter's results and our revised guidance show, our business is performing well, even with a major launch underway and the inflationary pressures we're experiencing in areas like logistics, commodities and memory. That's because we've spent years making the business more resilient by strengthening our vehicle portfolio, developing new high-margin revenue streams and operating with strong discipline around production, pricing and incentives. Looking ahead, there are clear external headwinds, and in some cases, they are intensifying. 
While the path forward is more challenging, we continue to believe that 2027 will be another strong year and better than 2026, assuming customer demand remains strong and commodity, logistics and other recent cost pressures moderate. On the plus side, we expect incremental benefits from warranty expense improvements, lower EV losses, growth in software and services revenue and the launches of our next-generation Chevrolet Silverado and GMC Sierra light-duty pickups. The performance of today's Silverado and Sierra has been consistently strong because of their design, capability, technology and innovative features. 
We have now achieved 19 consecutive quarters of sales leadership in the U.S. and grown our market share by 10 full points since the current generation went on sale in 2018. And now in their final year of production, we're seeing robust sales, share and financial results. This speaks directly to the value we offer customers. Our new trucks build on this foundation. Their interior and exterior designs are high watermarks for refinement and precision. 
Our trim series strategy allows us to meet customers at different price points while creating a clearer path to the higher value configurations. For example, High Country, Chevrolet's premium sub-brand, has become more premium, modern and athletic, with materials, features and technology closer to a luxury SUV experience. Sierra Denali remains the core premium capable truck, and the Denali Ultimate is moving further into halo territory. We've also made powertrain choice a critical part of the value ladder and a mix lever. 
We will offer the TurboMax 4-cylinder with best-in-class standard torque, our segment-exclusive Duramax inline six turbo diesel and all-new 5.7-liter and 6.6-liter V8s. Each engine is tuned to distinct performance and lifestyle needs, and we will focus on the things truck customers desire most: usable torque, smooth and predictable power delivery, fuel economy under real-world use, trailering confidence, durability under load and refinement. 
To ensure quality and durability, we have put our new V8 through more than 100,000 hours of dynamometer testing, and we have completed more than 1.6 million miles of real-world on-road validation before the truck reaches customers. Production has begun at Silao, and customers should see the first trucks arrive in dealerships later in the year. Fort Wayne will follow in Q1, and we will launch the trucks at Orion in Q2. We expect to build roughly the same number of trucks in '27 as in '26. And then in '28, we will have incremental capacity to support segment and market share growth. 
Trucks will also be a big driver of incremental Super Cruise adoption and digital revenue as we make the technology standard on high-end Silverado and Sierra LD trims and offer on most others. We expect full-size truck Super Cruise penetration to grow 4 to 5x next year, reflecting strong customer demand and our ability to scale the technology across critical customer segments. The base is already strong and growing rapidly. Year-over-year, deferred revenue from software and services is up 40%. 
For the full year, we're on pace to approach $7.5 billion in deferred revenue, driven by 1 million new OnStar subscriptions and a 1 million strong Super Cruise-equipped car parc. The quality of the Super Cruise driving experience and frequent customer engagement with the technology underscores why it is so successful with customers. Our Super Cruise-equipped vehicles travel well over a cumulative million miles hands-free each day. Nearly 70% of our customers use it at least once a month, and I'm confident we can grow our Super Cruise installed base by close to 50% next year. 
I'll close by recognizing the tremendous progress GM Defense has made since our last call, including several new multiyear contract awards that will help us drive annual top line growth of more than 30% with double-digit margins. During the quarter, the Pentagon announced increased production volumes for the ISV, including a contract for the ISV-Utility variant. These are part of a more than $1 billion potential ISV award based on the U.S. Army's procurement objectives, subject to congressional appropriation. The Army has contracted with us to deliver Silverado HD-derived tactical vehicle prototypes for its ISV heavy competition. We have signed contracts with 4 customers since June for our factory-armored Suburban Shield VIP transport. 
Our EPIQ mobile energy system is now certified and ready for sale to customers, and we delivered our first component set to Lockheed Martin for the Patriot PAC-3 less than a month after we signed a formal contract. As Lockheed said at the time, our ability to deliver components that can traditionally take months to years to produce underscores the effectiveness of defense and commercial partnerships and our own capabilities. These are all very positive developments for our country, our partners, taxpayers and our business. Thank you, and I'll now turn the call over to Paul.

**Paul Jacobson** (Executives):
Thank you, Mary, and good morning, everyone. Thank you for joining us. I want to begin by recognizing the entire GM team. Their hard work and consistent execution are showing up in both our operating performance and consistently in our financial results. Revenue for the quarter was a record $50 billion, up 3% year-over-year. EBIT adjusted was $4.1 billion, up 22% year-over-year, and EPS diluted adjusted was up more than 30% year-over-year to $3.70. 
The industry backdrop remains healthy, with a total industry SAAR in the upper 16 million unit range in the third quarter, with resilient demand across trucks, SUVs and fleet. Our U.S. sales totaled more than 670,000 vehicles in the quarter. ICE sales of 645,000 were up slightly year-over-year, despite the impact of discontinued models. And our light-duty full-size pickups continue to perform exceptionally well in the final year of their product cycle, with sales up 9% year-over-year. This leaves us on track to lead the industry in full-size pickup sales in 2026 for the seventh consecutive year. And with deliveries of our all-new light-duty trucks expected to begin in the late fourth quarter, we plan to carry this momentum into 2027. 
In terms of the changeover, we have already completed 4 down weeks at Silao Assembly ahead of starting production of the new truck last week. To ensure a high-quality launch, production will start at measured pace and ramp up over the coming months and quarters to more normalized levels. At Fort Wayne, we are planning 4 down weeks beginning in mid-December, with production scheduled to restart in January. In preparation for the downtime, the sell-down of the existing truck is on track, with inventories at planned levels and incentives as a percentage of MSRP that are several hundred basis points lower than prior truck changeovers. 
This is part of the broader discipline with which GM has been operating over the past 5 years. With that in mind, we expect to finish the year with overall inventory in our 50- to 60-day target range. On the cash side, continued strong cash generation supports both our growth-focused investments and ongoing share repurchases, which combine nicely to drive continued EPS growth. In the third quarter, we repurchased $2.5 billion worth of shares. That reduced our diluted share count by approximately 27 million shares to around 866 million or 9% below the third quarter 2025 level. 
So far in October, we have already repurchased another $1 billion. That brings our year-to-date buybacks to $6.3 billion and completes the prior Board authorization. This morning, we announced a new $20 billion multiyear share repurchase authorization, representing more than 25% of our current market capitalization. The size and duration of this authorization are a meaningful statement of the Board's confidence that our cash generation is sufficient to continue investing in the future of the company and returning capital to shareholders. 
Now let's turn to more details on our third quarter performance. Total company revenue of $50 billion was up $1.4 billion year-over-year. ICE volumes were up 8% year-over-year, while EV volumes declined as we lapped the expiration of the consumer purchase incentive in the third quarter of 2025 and aligned EV production with demand. EBIT adjusted was $4.1 billion, up $700 million year-over-year. The improvement was driven by core business performance, including a higher mix of full-size pickups and lower warranty expense, partially offset by higher commodity and onshoring costs. 
Adjusted automotive free cash flow was $5.9 billion, up $1.7 billion year-over-year. The improvement was driven by higher earnings and tariff timing. Regarding EV charges, as I mentioned last quarter, we moved quickly with our suppliers and partners and have substantially completed the material cash charges we expect to incur as we align our EV capacity and manufacturing footprint with changes in regulatory policy. We incurred an additional $0.2 billion of cash charges in the third quarter, bringing total cash charges incurred since the end of the first half of 2025 to $7.4 billion. 
To date, $4.6 billion of this has been paid, of which $4.2 billion was paid in 2026 to date. We expect to pay another roughly $1 billion in the fourth quarter and the remainder in calendar year 2027. As a result, free cash flow available to be returned to shareholders next year should benefit from a significant year-over-year step down in supplier EV settlement payments. 
Now let's move to our regional results for the third quarter. North America continued its strong performance, delivering EBIT adjusted of $3.6 billion, up $1.1 billion or 43% year-over-year. Margin was 8.7%, an improvement of 2.5 points from a year ago when tariffs were first put into place. Having worked through much of that pressure, we are solidly back within our 8% to 10% margin target, a clear marker of the progress the team has made. The improvement was broad based but included a higher mix of full-size pickups, lower EV losses from rightsizing our capacity and continued warranty expense reductions. 
These gains were partially offset by commodity inflation, including logistics and higher DRAM costs, along with higher manufacturing costs related to onshoring production to the U.S. OnStar Digital and Super Cruise delivered recognized revenue of over $800 million in the third quarter, up 15% year-over-year. We are on track for more than $3 billion in realized revenue for calendar year 2026 and expect to approach $7.5 billion in deferred revenue by year-end. Looking forward to 2027, we anticipate another year of double-digit growth in realized revenue. 
GM International EBIT adjusted, excluding China equity income, was breakeven in the third quarter, down $200 million year-over-year, driven by a negative $100 million mark-to-market adjustment for an investment in Momenta, along with higher manufacturing and logistics costs, partially offset by higher volume in South America and foreign exchange. China equity income was $32 million, recording its eighth consecutive quarter of profitability, a trend we expect to continue in the fourth quarter. 
New energy vehicles accounted for more than 60% of GM China's third quarter sales, and the team remains focused on execution, cost efficiencies and mix optimization to deliver ongoing profitability. GM Financial delivered EBT adjusted of $700 million and paid $250 million in dividends to GM in the quarter. Consumer credit performance remained resilient and consistent with our expectations. The business remains on track with its full year EBT adjusted guidance range of $2.5 billion to $3 billion and to pay full year dividends to GM at a level similar to last year, reinforcing its strategic value within the enterprise. 
Let's turn now to our calendar year 2026 guidance. Following another strong quarter, we're updating our full year outlook as follows. We now expect EBIT adjusted of $14.5 billion to $15.5 billion compared with our previous range of $14 billion to $16 billion. EPS diluted adjusted narrowed to a range of $12.75 to $13.75 from $12 to $14, reflecting the benefit of our share buybacks to date. Capital expenditures at the lower half of the $10 billion to $12 billion range and adjusted automotive free cash flow in the $11.5 billion to $12.5 billion range, up from $9.5 billion to $11.5 billion. This improvement is being driven by operational excellence, lower-than-projected capital expenditures and tariff timing. 
Now let me update you on a few key assumptions underlying our updated guidance. Let's start with the industry backdrop. The U.S. market remains resilient. We expect total SAAR to be in the mid-16 million unit range for the full year, which implies approximately 16 million for the rest of the year, consistent with what we are seeing in October. In North America, we expect fourth quarter ICE volumes to be lower than usual, primarily due to the launch of our new full-size trucks. We anticipate a year-over-year volume headwind of approximately 35,000 full-size pickups. 
Headwinds from lower truck volumes in the fourth quarter are expected to be largely offset by tailwinds from price in North America, including benefits from the new truck launch. Year-to-date, North American pricing is up $400 million. We continue to expect a full year pricing tailwind of 0.5% in North America, with the remainder of the benefit expected to be realized in the fourth quarter. 
Turning to EVs. We remain on track to reduce losses by $1 billion to $1.5 billion for the full year, driven by rightsizing our EV capacity and significantly lower volumes. We expect modest additional loss reduction in the fourth quarter as we lap the expiration of the consumer purchase incentive last year. 
On warranty, following our $600 million third quarter performance, our year-to-date improvement is approximately $1.1 billion on a year-over-year basis. For the full year, we now expect warranty to be closer to the high end of our $1 billion to $1.5 billion in full year improvement. Emissions-related regulatory savings are around $500 million year-to-date, and we expect a minimal benefit in the fourth quarter as we lap savings from last year. 
With respect to tariffs, we have incurred approximately $1.8 billion of tariff costs year-to-date, net of IEEPA reversal benefits. And we now expect gross tariff costs to come in at the low end of our $2.5 billion to $3.5 billion range for the full year. And finally, on the tax line, we continue to expect a 20% to 21% effective tax rate for the full year. This includes a higher tax rate in the fourth quarter, which is expected to be in the 25% to 27% range, driven by a mix of onetime discrete items affecting timing. 
Now let's turn to the headwinds. As the conflict in the Middle East has continued, commodity and logistics costs have intensified since our second quarter earnings update. Copper prices are at record levels, while HRC steel prices are at 4-year highs. Spot prices for HRC steel and copper are each up 10% to 15% since July and approximately 50% versus last year's average. Collectively, inflation is adding approximately $400 million in incremental costs for the calendar year, with the majority of that impacting the fourth quarter. 
As a result, we now expect a headwind from commodity inflation, logistics and DRAM costs to be around $2 billion for the full year. In the third quarter, we incurred approximately $700 million primarily related to commodity costs year-over-year, bringing the calendar year-to-date headwind to approximately $1.3 billion. 
Separately, we are investing approximately $1 billion to $1.5 billion this year to onshore production to the U.S., strengthen our supply chain and expand our software capabilities. We expect these costs to continue to ramp in the fourth quarter ahead of additional U.S. capacity additions in 2027. Finally, turning to our international operations. We expect continued ongoing softness in GM International, reflecting headwinds from the dynamic environment in the Middle East. 
Let's turn next to 2027. Assuming market conditions and the tariff environment remain broadly similar to 2026 and recent commodity pressures moderate, we continue to believe we can grow revenue, margins and EBIT adjusted next year. It's too early to try to predict where commodity prices will land in 2027. However, if we were to simply annualize the recent incremental commodity inflation since July, it would translate into an additional $1 billion to $1.5 billion of EBIT-adjusted headwind for 2027, which would result in a total headwind for 2027 of roughly $2 billion. 
Our growth plan is supported by our product cycle and the ongoing operational discipline that investors have come to expect from General Motors. The opportunity is centered on 4 key GM-specific drivers. First, launching our new truck flawlessly and capturing a rich mix in its first year. Second, unlocking additional capacity in full-size SUVs and high-volume crossovers. Third, growing our adjacencies in OnStar, Super Cruise and Defense. And fourth, managing costs across warranty, EVs, fixed costs and onshoring. 
The bottom line is that we have demonstrated time and again our ability to roll up our sleeves and execute. We have set a high bar for ourselves, and the team is working to deliver another year of growth for our shareholders. We have a great product portfolio that is only going to get better in 2027 and beyond. Thank you. And now we'll move to the Q&A portion of the call.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Mark Delaney with Goldman Sachs.

**Mark Delaney** (Analysts):
I understand the change in the cost environment that GM is seeing heading into 2027. I'm hoping you can talk a little bit more on some of the tools GM may have at its disposal in order to try and manage that. And to what extent GM could potentially utilize net pricing to help offset what's a higher cost environment, especially given your expectation for a measured ramp of the full-size pickup trucks?

**Mary Barra** (Executives):
Mark, well, when you look at the increases, as Paul mentioned, we saw it happen in just the last couple of months, and so we really haven't had time as a team to go work to find the offsets. We do have significant tailwinds next year when we look at continued warranty improvement. We're seeing it this year. We believe we'll continue it into next year. And as we've said, although volume will remain roughly flat from a new truck perspective, we do think there is some price and mix opportunity there. 
We also see growth opportunities in OnStar and Super Cruise. We see continued improvements in EV profitability. And then we are going to continue to work at fixed costs. There's a lot of opportunity, we believe, especially as we continue to implement and leverage AI to improve the business and make it more efficient. So like this team always does, we just -- because this has happened so recently, we're going to go to work, and we'll have more to say when we give full year '27 guidance at the end of the fourth quarter. But we obviously have work to do and we plan to do it.

**Mark Delaney** (Analysts):
That makes sense. And my follow-up is just a clarification on what GM is currently assuming. So you said the assumption that '27 is a better year than '26 does assume that cost pressures tied to commodities, logistics and memory moderate. When you talk about moderation, do you mean that the spot prices just need to level off from current levels? Or would you actually need to see spot prices decline?

**Paul Jacobson** (Executives):
Yes, Mark, it's a little bit too early to call commodity prices in '27. So what we're really trying to do here, as we said in July where we highlighted the tailwinds, and we said assuming the environment remains consistent. We have seen a significant amount of inflation, as I called out in the prepared remarks, really just in the last, call it, 8 to 10 weeks. And should we see prices at this level, it makes that more challenging heading into next year. So we're really looking for a little bit of moderation from the most recent increase that we've seen. But as Mary said, we're continuing to work through our budget process. 
So we won't give any definitive guidance on the year and where it's going to come out. But obviously, it's gotten a little bit more challenging with this additional inflation that we've seen since that disclosure. So I don't think anything has changed. The tailwinds are the tailwinds. We have a lot of mix benefits coming in with the first year of the truck, but we'll continue to watch it and hopefully become what we're known for. But the goal remains to grow next year as it does every year.

**Operator** (Operator):
Our next question comes from Itay Michaeli with TD Cowen.

**Itay Michaeli** (Analysts):
Maybe first question just on the higher free cash flow guidance for the year. Paul, maybe talk a little bit more about what are kind of the drivers there. I think you mentioned maybe kind of lower end of the CapEx outlook as well. And how much of the strength that you're seeing this year may be sustainable into next year?

**Paul Jacobson** (Executives):
Itay, thanks for the question. A couple of things. One, we are coming in probably at the lower end of our capital. We're certainly seeing a little bit of a reduction in capital spend as everything comes online in that $10 billion to $12 billion range. So that unlocks some free cash flow. Also, if you recall, earlier this year when we talked about the IEEPA refunds, we brought the EBIT guidance up, but we didn't bring the cash flow guide up because we were uncertain. We've seen some success in getting IEEPA refunds, both in terms of our own as well as the second order from our supply base that's contributed to some of that benefit. 
As we look forward into 2027, I mean, should we have a year where we can grow earnings, we would expect that free cash flow would be pretty consistent, if not a little bit higher. But remember, our GAAP cash flow, so our actual sort of cash available for investment, should be significantly higher as we lap the bulk of the cash restructuring work that we did on the EV side. So we're looking for a bullish year on cash generation overall in 2027, irrespective of what we've seen with the commodity inflation recently.

**Itay Michaeli** (Analysts):
That's very helpful. As a quick follow-up, as you lap the EV restructuring and as you have a number of updates coming in 2028, curious if you could kind of share how we should think about kind of GM's breakeven EV volume, let's say, in the 2029 time frame and kind of latest thoughts on the path to EV profitability would be helpful.

**Paul Jacobson** (Executives):
Yes. I think it's a little bit too soon to tell. As we've said, we've had a good year of EV profitability improvement, primarily from lower volumes as we've adjusted and also the fixed costs coming out of the system as we restructure. So that's a big benefit in '26. We've said that '27 will be a year of probably lower benefit, but still maybe improvement versus '26 and then '28 and '29, as we get into LMR and the next-generation battery cells and packs, we should see another step function improvement in profitability. 
We're going to continue to watch volumes. We think with these oil prices and these fuel prices, that EV penetration may continue to go up. And we want to make sure we're ready for that. We're the #2 producer of EVs in the U.S., and we've got a strong portfolio and one in which we're committed to improving the profitability of it.

**Operator** (Operator):
Our next question comes from Dan Levy with Barclays.

**Dan Levy** (Analysts):
So one of the points in your commentary on 2027 is it talks about customer demand remaining strong. And I know this has been a constant debate in the industry. I think people just amazed by how resilient the auto industry has been. But we're getting the latest round of questions of health to the quality of consumer with rising rates. So can you just talk about, given the latest backdrop, what your view is on the ability of the market to absorb these continued very high trim products and potentially incremental volume on your trucks as you expand capacity? Maybe just help disaggregate what we're seeing from the consumer as a whole versus the average consumer of your products.

**Paul Jacobson** (Executives):
Yes, Dan, I'll give it a shot, and Mary can help if I miss anything here. I think as we've said now for a number of years, when you look at a lot of the consumer sentiment surveys, they really have become disaggregated from consumer behavior on the ground, and that's evident in our average transaction price. It's evident in our trim mix. It's even evident in what we see in GMF, where no noticeable shifts in delinquencies, defaults, et cetera. 
So I think the consumer has held up remarkably well. That being said, we know from that sentiment. And historically, we should continue to watch it. So it's not necessarily pessimism. It's really more an abundance of caution, of making sure that we're setting expectations against that backdrop, that we're basing that forward projection on consumer stability, and we think that's going to continue to be the case because we haven't seen anything that indicates any weakness right now.

**Dan Levy** (Analysts):
Okay. Great. Second question is about the dynamic in China. And obviously, we've seen this sharp rise in exports from China. Maybe you can just talk about the extent to which you are participating in this sharp rise of exports. Is there any benefit to you on the cost side? And then I know you're talking about GMI ex China moderating. How much of that is sort of the pressure of competition from Chinese OEMs in some of these other regions? What's your ability to offset that?

**Mary Barra** (Executives):
Well, I think when we look at some of the markets where China is working, specifically from a South America perspective, we're still holding share. And we are -- there are some of our product portfolio we are exporting from China. Once the market has allowed the Chinese competition to come in, we're well positioned to participate with that with Chevrolet products that are true to the Chevrolet brand but have that price point. So we're holding our own in South America. Actually, remain strong based on the portfolio. And in South America, Chevrolet is considered a premium brand. 
So I think that's an opportunity for us in some other markets as well. So again, from a China perspective, we -- I would say in country, we're really not seeing that much benefit. I mean from our China business, we are very proud of the fact that we got to the restructuring early in China, and our business is profitable even in the depressed economy that they're seeing from an overall industry perspective. So there may be a little bit of benefit because of the opportunity from an export perspective. But bottom line, we're seeing that market tougher because of the challenges, but we are participating in the export market and maintaining share through the strength of our product portfolio.

**Operator** (Operator):
Our next question comes from Joe Spak with UBS.

**Joseph Spak** (Analysts):
Paul, I just want to go back to one of your answers, I think earlier, maybe to Itay's question. I think you said when you were talking about '27, I know it's early and there's still a lot to be determined, but you said -- I think you said that if there's a year where you grow earnings, you'd expect free cash flow to be consistent, if not higher. And I guess I'm just a little bit curious. I know distributable free cash should be higher because of EV payments, but is there something else we're not considering with -- in sort of the free cash flow factors? Like if it's -- if earnings would grow, like why wouldn't the free cash flow also be higher?

**Paul Jacobson** (Executives):
Yes, Joe. So yes, sorry if my answer was confusing. There's a couple of reasons why. Number one, if we go into 2027 with the same CapEx guided range of $10 billion to $12 billion, but we come in at the high end versus the low end, obviously that's going to be a case where EBIT growth and free cash flow would become a little bit disconnected based on timing. Second, we do have the added benefit this year of the IEEPA tariff refunds that have come in. That's not expected to repeat. 
So on a like-for-like basis on tariff flows, there's some upside that we got in '26 that wouldn't repeat in 2027. And generally, you see some small working capital nuances from year-to-year. But other than that, it should be fairly linear as cash flow from earnings is -- the connection between cash flow and earnings is pretty constant.

**Joseph Spak** (Analysts):
Okay. Second question is just, Mary, I think in the past you've said you would study hybrids and plug-ins. And I think earlier this month, Mike Anderson said you'll listen to customers and they're part of the plan. I know you don't give sort of product announcements away on these calls for competitive reasons. But can you let us know if some of that investment and spending is already occurring? Does that require an additional investment? I mean I know you have a lot of these technologies internationally, so maybe you could just tell us how you're sort of thinking about leveraging that and bringing it to scale in the U.S.

**Mary Barra** (Executives):
Sure. From a hybrid perspective, we will have hybrids in our portfolio in multiple segments, the key segments that we participate. If you look at right now, a lot of where the hybrid activity is, it's in compact car, midsize car and minivans, which are 3 segments we're not a part of right now. So you have to look -- and that's why I think our sales continue to be so strong. In many cases, we're building everything we can. I mean for the Equinox compact SUV, it's fully maxed out even without a hybrid. 
So I think we're still taking advantage. As Paul said earlier, we're well positioned from an EV perspective as this continues, but we will have hybrids. They've already been added. It's not going to be additional CapEx in engineering, and we'll talk more about them as we get closer to the launch.

**Operator** (Operator):
Our next question comes from James Picariello with BNP Paribas.

**James Picariello** (Analysts):
Just on the Q1 pickup volumes, the expectation is for the volumes to trend flat next year. Is the expected downtime impact slated for the first quarter at the similar 35,000 unit reduction to the fourth quarter? And then can you share any dimensioning of what the targeted incremental full-size SUV capacity might look like for 2027?

**Mary Barra** (Executives):
Well, as we said, if you look at the full-size truck, we have 3 assembly plants. We also have 3 engine plants that we're launching, and we're focused on a flawless launch. It's on track right now. As we've said, we'll have the first trucks rolling out of the first plant yet this year at the very end of the year. And then we do have some downtime. We haven't specified it to the exact number of units, but we do have some downtime coming as we get the other 2 plants going. And so that's why we're saying really the volume is going to be flat from '26 truck volumes to '27 because we're in the middle of that launch of these 6 plants. 
So as we get into '28, that's where there's an opportunity for plus side. We won't have any of the changeover downtime, and we'll also have the benefit of the Orion plant. So '28 is an opportunity for growing market share in the truck, not only in the U.S., but globally.

**James Picariello** (Analysts):
Got it. And then as a follow-up for GMI, excluding China, what's the embedded expectation for the fourth quarter regarding the Middle East challenges? Should we anticipate another quarter of EBIT loss? And I know it's early, but how should we be thinking about this business for next year with respect to the puts and takes?

**Paul Jacobson** (Executives):
Yes, James. So what I would say with respect to the Middle East, it's largely a wash at the enterprise level because we're selling a lot of vehicles there that with the right notice and with the right preparation, we can actually redirect many of those vehicles into the U.S., which we have. The team has done a really good job of managing that, so we're not losing volume at the enterprise level. So as long as that persists in the Middle East with that tension, I would expect that you'll see a little bit more of a lean to North America than you will international, particularly the Middle East. 
And then I think we're continuing to work with the team to try to mitigate as much of the international competition and deliver value in the pockets where we can and where we're really competitive. And I think the team is doing a good job everywhere else in the world being able to do that. Keep in mind that our international results were also impacted this quarter by about $100 million negative mark-to-market adjustment on Momenta. So if you actually look at the underlying business, it performed marginally better than what the results indicated.

**Mary Barra** (Executives):
And James, just to be clear, we're building the trucks in the first plant right now. They'll be in showrooms by the end of the year.

**Operator** (Operator):
Our next question comes from Andrew Percoco with Morgan Stanley.

**Andrew Percoco** (Analysts):
I do want to come back to the 2027 bridge. And obviously, mix and pricing are clearly working in your favor with the new truck. But is there a way to also think about corporate or fixed cost savings as we get into 2027? I think this is an area where you guys have obviously been very focused. And I'm just curious to the extent we could get more clarity in terms of what that could look like into next year. I think, Paul, you've talked about AI integration within the organization, and just curious if some of those investments could start bearing some fruit on the cost side.

**Mary Barra** (Executives):
Andrew, absolutely. And like I said, with the increase that we saw just in the last 8 to 10 weeks, we're even doubling down. But there's active work going on across the company to really not only make sure everybody is using AI efficiently, but to be able to make their job more efficient and make our design processes more efficient, our manufacturing more efficient, with really every single function is leveraging AI. It's how do we harness that savings from a fixed cost perspective. 
I'm not going to quantify it right now. We can do that when we get to the end of fourth quarter and when we announce -- officially announce guidance for 2027, but trust that there will be significant work in the fixed cost arena as we move forward. It's happening today.

**Andrew Percoco** (Analysts):
Okay. That's super helpful color. And I guess, just on the buyback announcement, curious if there's anything you can provide in terms of how we should be thinking about the cadence there. Obviously, you guys have talked about the lack of supplier payments that you have to make next year. Is that a reasonable way to think about potentially the step-up in buyback cadence in 2027 relative to 2026?

**Paul Jacobson** (Executives):
Yes. Andrew, it's Paul. First of all, you're going to make me lose a bet because I thought for sure you were going to ask about digital revenues. I'll take the question. On the buyback side, we don't give any forward commentary on what we're going to do on buyback for obvious reasons. But as we've talked about, we expect the actual cash flow, the GAAP cash flow, to be significantly bigger year-over-year. And I think, hopefully, you look at, and the market sees what we did this year because I know there was a lot of skepticism on our ability to return capital back to shareholders given the EV restructuring, and we completed that authorization ahead of all expectations. 
So the Board has demonstrated a commitment to continuing to drive shareholder value this way. We continue to believe that with a double-digit free cash flow yield, we're compounding the EPS growth of the company. And that's no shortage of commitment as what you've seen for the last several years and expect that to continue going forward as long as the valuation remains depressed.

**Andrew Percoco** (Analysts):
Okay, that makes a ton of sense. And I'll take that digital services question offline.

**Operator** (Operator):
Our next question comes from Emmanuel Rosner with Wolfe Research.

**Emmanuel Rosner** (Analysts):
I appreciate all the color on the commodities and some of the assumptions. So I think you said, around current prices, if things stay at current level, it would probably be a $2 billion additional headwind to 2027. In order for your expectation to grow EBIT in '27 to be realized, are you assuming this $2 billion? Or should it be less than that? And then I understand it's early to identify the offsets that are in your control to sort of offset some of these increased commodities. But in the past, you've built a very, very strong track record around, call it, a downturn playbook, right? The discretionary spending cuts, things that are in your control, restructuring, et cetera. Can you maybe just remind us historically, what are those things that you could have as levers? And to what extent this could be applicable in the current environment?

**Paul Jacobson** (Executives):
Yes. So Emmanuel, thanks for the question. On the commodities, as we clearly stated, we would need prices to come off of these levels a little bit to have the confidence to be able to grow at this point. But we're in the middle of the budgeting process, and we'll continue to work through that. So nothing specific on the headwinds or tailwinds because we don't want to get ahead of expectations and where the market is as we continue to develop that. As we've talked publicly, we approve our budget with the Board in December, and we give guidance in January, and that's going to continue to be the case for 2027. 
If you look at past years, I think we've proven adept at getting costs out. These things take time. Some of them can pivot quickly, but other larger initiatives like, for example, several years ago, we did a $2 billion fixed cost reduction program that was very successful over that time period, too. So we're continuing to go to work. We're looking at those plans. And as we've said repeatedly, we're committed to grow earnings every year, and that's what we're going to be working towards the best we can.

**Emmanuel Rosner** (Analysts):
Okay. That's helpful. And then one quick follow-up on the improvement in this year's free cash flow guidance. I appreciate the buckets that make this up. Any way to quantify for us the piece around the IEEPA refund that's now in the -- assumed in the full year free cash flow?

**Paul Jacobson** (Executives):
Well, so we announced there's a $500 million credit that we took to earnings. We've gotten probably about 60% of that back to date. And then I would say roughly a similar amount from the supply base that we expect to get before the end of the year as well. So call it, $600 million to $800 million this year, but that'll continue to come in as we go through the remainder of this year.

**Operator** (Operator):
Our next question comes from Michael Ward with Citigroup.

**Michael Ward** (Analysts):
Just to follow-up on the $20 billion share repurchase. Is that -- it looks like that's what you spent the last 3 years, $20 billion in share repurchase. Is that number more of a timing or just an opportunistic to give you the flexibility to be more optimistic, I mean, at current trading levels and those sorts of things?

**Mary Barra** (Executives):
Mike, we're going to follow our capital allocation framework of bringing the -- reinvesting in the business to generate a 20% return on invested capital, maintaining an investment-grade balance sheet. And as we've done now for several years, return the rest to our owners, our shareholders. And so I think this is -- what we're really trying to signal is we believe the company is undervalued. And so we think this is the best way to provide value for our shareholders because of it. And we're not -- as Paul already indicated, we're not going to put a specific time line on it. We'll be opportunistic as we've been over the last several years. But I think a signal you should take from the size of it is that it reflects our Board's commitment to return cash to shareholders when we believe the shares are undervalued.

**Michael Ward** (Analysts):
Okay. And then on the financing front, you've stepped back leasing over the last few years. Is that a lever you're looking to pull? Or is subsidized interest rates? What are some of the things that you can pull on GMF as far as trying to make vehicles a little more affordable if that's something that's needed in the marketplace? Will you push back leasing more? Or what are your long-term goals with GM Financial and what they can do?

**Paul Jacobson** (Executives):
Yes. Mike, and Susan's on the line, too. I can start and turn it over to her. But we've obviously seen over the last few years, a lot of EV leasing, and there was a lot of investment made there to help socialize that, help drive demand, and also it was structurally superior with the consumer tax credits in a lot of cases. 
So I think the organization is pivoting. We're still very much committed to GMF. And when you look at loyalty, when you look at availability for financing options for the customer, it's a great way to serve that. And as we continue to look for ways to grow GMF with GM Insurance and there's really interesting ties that we can do with the GM Rewards program. It's obviously a big lever in terms of helping to create value for consumers in different ways than just producing vehicles. Susan, happy to let you add.

**Susan Sheffield** (Executives):
Yes. I mean I think you addressed it. We're here to support GM in moving vehicles, and it's about discipline on incentive spend. And yes, really don't have anything else to add.

**Michael Ward** (Analysts):
Okay. Is it a concerted effort to scale back leasing? Or is that something a lever you can pull as you go forward?

**Paul Jacobson** (Executives):
I would say, Mike, it's a balance between -- it certainly is a lever, and I would like to see us probably do more leasing, but it's also a lever against the incentive environment that we're in and how do we use our incentive dollars. I think our go-to-market strategy has evolved over the last several years, and it's clearly been a competitive advantage for us. And we've got to use those dollars where we can. And sometimes that changes from time to time as consumer needs change, and we'll be responsive to where the customer is.

**Operator** (Operator):
Our next question comes from Alex Perry with Bank of America.

**Alexander Perry** (Analysts):
I just wanted to follow up with -- on price. So I guess how should we think about the pricing -- potential pricing benefit next year compared to the last major redesign of the full-size trucks? I think in 2019 you saw a very strong price realization. What are the puts and takes of sort of using that as a case study for thinking about some of the pricing benefits next year?

**Paul Jacobson** (Executives):
Yes. Alex, thanks for the call. We've been cautious to make sure that we're not using historical heuristic models on pricing for this generation of trucks. And the main difference is the current generation, the model year '26s, are performing better than any trucks, really any vehicle program has in its last year of production. So the historical step function improvements that you've seen aren't going to be there as pronounced. That being said, we should benefit from a mix benefit, as we tend to produce a bit of a rich mix out of the gate, as we're scaling up. And that should ultimately average out over time. But just caution you against using some of the 2018, 2019 data because the current pricing environment is very different than what it was back then.

**Alexander Perry** (Analysts):
Really helpful. And then my follow-up question was just on input costs. I guess, as we think about the impact of higher fuel prices, I guess, what specific impact is higher diesel having on the supply chain with some of the fuel surcharges we've been hearing about? And I guess also on end customer demand for some of your heavy-duty platforms.

**Mary Barra** (Executives):
Yes. I would say it's early with the spike that's just happened in diesel, and we'll see what happens to it. But throughout the year, our diesels are so efficient that, even with the higher prices before this last spike, they were more fuel efficient, so cost of ownership was lower than buying a hybrid truck.
So I think we've seen demand. We're watching it closely. I think a lot is going to happen of how long people perceive that the prices are going to be there. I think I'm excited about the new engines that we have coming because not only are they going to improve performance across the board, they also are going to drive efficiency. So again, it's too soon to tell if the diesel prices remain at this high level. But up until a month or 2 ago, we weren't really seeing an impact, and we were still seeing strong demand.

**Paul Jacobson** (Executives):
And Alex, on the logistics front, it comes in pretty quickly, as you've seen, maybe a 2- to 4-week lag, but we see it hit pretty quickly, and that's been a sizable component of the $400 million of pressure that we called out in the prepared remarks.

**Operator** (Operator):
Our next question comes from Tom Narayan with RBC Capital Markets.

**Gautam Narayan** (Analysts):
The first one is on the competitive pressures into 2027 and the potential impacts on volume and pricing. You have a Detroit 3 peer with elevated dealer inventories, especially at its pickup truck, and we're seeing incentives pick up there. We saw Japanese OEMs to be taking up share, especially with hybrids. I know you just said that's not really where you play, but you also have European OEMs getting squeezed out in Europe and China because of competition from Chinese OEMs, and they're talking about coming into the U.S. aggressively at their investor events. I mean is this all just kind of par for the course or something you're concerned about?

**Mary Barra** (Executives):
Well, if you think about when we saw the semiconductor shortage a few years back, we saw -- and everyone was limited of how many vehicles they could build because of the allocations of semiconductors. We saw everybody pushing that limited supply to the United States because of the profitability of this market. So I don't think it's anything new. I think we're well positioned because of the overall strength of our portfolio and the fact that we've got a new truck coming out that takes performance across all aspects to the next level. 
Right now, in most of the products we build, we're capacity constrained. We're building as many as we can from a truck, SUV. I mentioned earlier, the Equinox, we can't build enough of them. We'll be relieving that as we launch the opportunity to build that in the United States. But I think that kind of competition is going to be here to stay. Specifically from a truck perspective, we've seen one of our competitors tend to have higher incentives for quite some time now. It goes up and down, but it's been years. And we're still -- we grew share with this truck, and we think we have a huge opportunity to -- as we launch -- get past the launch, continue to grow share based on the strength of our product. 
And when we do that, it also gives us the opportunity to continue to grow the OnStar and Super Cruise revenue. So again, I think you're accurate in what you're seeing. I think we're well positioned because of the strength of our portfolio, and we've seen it before and have the proof points that we continue to do well.

**Gautam Narayan** (Analysts):
Got it. It's a good segue on the Super Cruise to my next question. You guys are confident on Level 3 for 2028. There's a couple of German OEMs who tried Level 3, and it kind of didn't go as well. I think they had some limited consumer demand. Part of that was just their ODDs were limited. I suspect you guys are different. And so just curious to hear kind of why -- how you're able to just get a better service than maybe what they have had on their Level 3, and what makes you more confident in achieving the consumer demand there?

**Mary Barra** (Executives):
Well, I think when we get to, in '28, when we launch the Escalade IQ, it will be the first, and we'll talk more about that tomorrow in the GM Forward event that we have. Our highway autonomous driving will be for highways, and it won't have limited ODDs. It will also carry with it the same focus we have on safety that I think everyone and customers have seen and trust, and therefore use from a Super Cruise perspective. So I think they will see a very capable product. I was just in the vehicle within the last month. And from a couple of months ago, when I was in, it was dramatic how confident the vehicle is on-highway, highway speeds, et cetera. So I feel very good about the product that we're going to be launching. We'll have more to talk about it tomorrow. And I think it will -- customers will use it and want to pay for it because it will definitely improve their lives and the amount that they're going to be able to use it.

**Operator** (Operator):
And at this time, I'd like to turn the call back to Mary Barra for her closing comments.

**Mary Barra** (Executives):
Great. Well, thank you, and thanks, everybody, for your questions. As we discussed today, GM is performing very well. That hasn't changed. While inflation continues to be uncertain, we are working hard to continue our momentum and generate significant cash returns for our shareholders. We are making the core business stronger with strategic investments in new products, new technologies and through improved quality and operating efficiency. And we have raised our full year guidance twice this year while offsetting higher commodities, logistics and other costs outside of our control. 
As we move forward over the next several years, our product portfolio will only get stronger as we complete the launches of the Silverado and Sierra light-duty pickups and then follow them with our next-generation heavy-duty pickups and our next-generation full-size SUVs, all-new Cadillac sedans and crossovers and more. So I think you can see we've got a lot coming. 
At the same time, we'll be expanding our capabilities in autonomous technology for highway, starting with the Cadillac Escalade IQ in '28, as I just discussed, developing cutting-edge battery technology like LMR that will help improve our EV profitability and building even stronger relationships with customers through our digital experience. We think this is a proven strategy for creating even greater shareholder value as we move forward, and we look forward to delivering. So thank you for joining us today, and I hope everyone has a great day.

**Operator** (Operator):
That concludes the conference call for today. Thank you for joining.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GM_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO｜guidance：CFO 上調全年 EBIT adjusted 指引至 $14–16B（前 $13.5–15.5B）（原話："We now expect EBIT adjusted of $14 billion to $16 billion"）
- 2026-07-21｜CFO｜guidance：全年 EPS diluted adjusted 指引上調至 $12–14（原話："EPS diluted adjusted of $12 to $14, up from $11.50 to $13.50"）
- 2026-07-21｜CFO｜guidance：全年 adjusted automotive FCF 指引上調至 $9.5–11.5B（原話："free cash flow of $9.5 billion to $11.5 billion, up from $9"）
- 2026-07-21｜CFO｜guidance：指引前提：中東不明顯升級、大宗商品與通膨壓力不顯著增加（原話："assumes no material escalation in the Middle East and no"）
- 2026-07-21｜CFO｜guidance：北美全年定價預期約 +0.5%，位於先前指引高端（原話："year North America pricing to be up around 0.5%, which is at"）
- 2026-07-21｜CFO｜guidance：下半年定價效益較小，因為對上年度 2026 車型年漲價（原話："The pricing benefit is expected to be smaller in the second"）
- 2026-07-21｜CFO｜guidance：EV 虧損全年改善 $1–1.5B 維持不變（原話："We continue to expect losses to improve by $1 billion to"）
- 2026-07-21｜CFO｜guidance：保固全年改善上調為 $1–1.5B（前為 $1B）（原話："Warranty is tracking to a $1 billion to $1.5 billion"）
- 2026-07-21｜CFO｜guidance：排放法規節省全年 $500–750M 維持（原話："full year benefit of $500 million to $750 million, primarily"）
- 2026-07-21｜CFO｜guidance：全年毛關稅成本 $2.5–3.5B 維持（原話："We continue to expect gross tariff costs of $2.5 billion to"）
- 2026-07-21｜CFO｜guidance：大宗商品／物流／DRAM 逆風全年 $1.5–2B 維持（原話："DRAM costs to be a headwind of $1.5 billion to $2 billion"）
- 2026-07-21｜CFO｜guidance：今年投入 $1–1.5B 於回美國生產、供應鏈與軟體（原話："we're also investing approximately $1 billion to $1.5"）
- 2026-07-21｜CFO｜guidance：Q4 預期較季節性模式偏弱（新卡車投產、回美國成本）（原話："we expect the fourth quarter to be somewhat weaker than"）
- 2026-07-21｜CFO｜guidance：Q4 新卡車造成約 35,000 輛年減量逆風（原話："anticipated year-over-year volume headwind of approximately"）
- 2026-07-21｜CFO｜guidance：管理層對 2027 的初步看法：營收、利潤率、EBIT、FCF 皆可成長（原話："based on what we know today, we believe we can grow revenue"）
- 2026-07-21｜CFO｜margin：北美 Q2 EBIT 利潤率回到 8–10% 目標區間（原話："solidly back within our 8% to 10% margin target"）
- 2026-07-21｜CFO｜margin：新卡車變動利潤與定價的效益預期落在 2027 年後而非今年（原話："potentially more of a '27 and beyond tailwind than anything"）
- 2026-07-21｜CFO｜margin：回美國生產成本 2027 年相抵，整體大致平衡（原話："it's a little bit balanced into 2027"）
- 2026-07-21｜CFO｜margin：大宗商品：不預期下半年價格低於上半年（原話："I don't think we are projecting lower commodity prices for"）
- 2026-07-21｜CFO｜margin：保固被描述為多年期順風（原話："we think that this is part of the multiyear"）
- 2026-07-21｜CFO｜margin：OnStar 軟體營收遞延收入 $6.3B，年增近 50%（原話："Subscriber growth drove deferred revenue to $6.3 billion, up"）
- 2026-07-21｜CFO｜margin：2027 年已實現數位營收預計雙位數成長（原話："existing deferred and subscriber growth is expected to drive"）
- 2026-07-21｜CFO｜margin：車隊銷售成長未稀釋利潤（原話："Importantly, the growth in fleet comes without diluting"）
- 2026-07-21｜CFO｜margin：車隊定位轉變：不再是過剩產能出口（原話："fleet historically, I think, was an outlet for excess"）
- 2026-07-21｜CEO｜commitment：承諾持續擴張利潤率（原話："all of this supports our commitment to ongoing margin"）
- 2026-07-21｜CFO｜commitment：EV 重整現金費用大致完成，但保留補提空間（原話："While circumstances may change in the future and we may have"）
- 2026-07-21｜CFO｜commitment：預計持續穩定回購，剩餘授權 $3.5B（原話："We have $3.5 billion remaining under our current repurchase"）
- 2026-07-21｜CEO｜commitment：預計 2028 推出 eyes-off 系統，進度無變化（原話："the program overall is on track"）
- 2026-07-21｜CEO｜commitment：預計 2027–28 於電池研發中心建置經驗證的鈉離子電芯（原話："we believe that we'll be building production validated cells"）
- 2026-07-21｜CFO｜capital_allocation：Q2 公開市場買回 $2B（原話："In the second quarter, we made $2 billion in"）
- 2026-07-21｜CFO｜capital_allocation：對 EV 工廠資本投入持保守，拒絕多十億美元投資（原話："we turned down opportunities to put billions of dollars of"）
- 2026-07-21｜CEO｜customer：北美全尺寸皮卡市佔逾 42%（原話："our share of the U.S. full-size pickup market stands at more"）
- 2026-07-21｜CFO｜customer：整體市佔年減約 60 bps，管理層歸因於停產車型等三因素（原話："share was down by about 60 basis points versus the first"）
- 2026-07-21｜CEO｜customer：CEO 稱負擔能力疑慮尚未轉為對大型車需求的影響（原話："that's been predicted for several months now, and it's just"）
- 2026-07-21｜CEO｜product：新一代 Silverado／Sierra 輕型皮卡 12 月進展示間（原話："will further separate us from key competitors when they"）
- 2026-07-21｜CEO｜product：2027 因 Super Cruise 策略估計增加 160,000 套（原話："We're estimating 160,000 incremental Super Cruise units from"）
- 2026-07-21｜CFO｜product：Super Cruise 附加率約 30–40%（原話："we're seeing really encouraging attachment rates in the 30%"）
- 2026-07-21｜CEO｜product：新卡車量的真正成長在 2027 年底至 2028（原話："The real volume opportunity comes in the very late '27 or"）
- 2026-07-21｜CEO｜product：GM Defense 2026 營收預計近 $700M（原話："GM Defense expects 2026 revenue to grow to almost $700"）
- 2026-07-21｜CEO｜product：GM Defense 預期營收 CAGR 逾 30%（原話："We are expecting a top-line revenue CAGR for GM Defense of"）
- 2026-07-21｜CEO｜product：美國陸軍 ISV 採購可能超過 10,000 輛（待撥款）（原話："plans to procure more than 10,000 if the appropriation is"）
- 2026-07-21｜CEO｜product：GM Insurance 從 3 州擴至 21 州（原話："scaled from 3 states in early 2024 to 21 states today"）
- 2026-07-21｜CEO｜competition：CEO 形容中國智駕定價競爭不可持續（原話："there's intense pricing competition that, frankly, is"）
- 2026-07-21｜CFO｜risk：DRAM 供應：與 Micron 擴大合作（原話："On DRAM, specifically, our expanded collaboration with"）

### 問答異常語氣（迴避／改口／保留）
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Spak：Super Cruise 普及後是否調整價格結構（前期成本／月費）｜答法：未給具體答覆，稱「沒有具體要宣布的」，改談成長機會與附加率
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Rosner：2027 是否有逆風（大宗商品、DRAM）可一併說明｜答法：稱尚未量化，只說會有通膨壓力，轉回講多年期順風
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Narayan：現有回美國生產是否足以符合 50% 美國含量提案｜答法：未直接回答是否足夠，改談供應鏈韌性與美墨加談判
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Delaney：Micron 記憶體協議對 2027 成本能見度的影響｜答法：未揭露定價，只談關係與技術路線圖
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Levy：定價、保固、批發、商品皆較佳但指引上調幅度偏小，抵銷項目為何｜答法：未列出具體抵銷項，強調不預期商品價格下降並「謹慎」

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
{"date":"20260524","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Capital allocation 持續主動（buyback + 分紅 + 紀律）","columns":{"2Y":"2026-27 EBIT $13-15B/yr + $6B buyback 完成","5Y":"累計回購 ≥ 50% shares outstanding","10Y":"EPS CAGR 包含 buyback +7-10%/yr","具體門檻":"buyback / 分紅每季 announcement","來源":"Q1 26 法說會 + Feb 2026 board approval"}},{"id":"H2","text":"EV 段虧損穩定漸縮 / 不再 impairment","columns":{"2Y":"FY26-27 EV 段虧損","5Y":"EV 段損平 2028","10Y":"EV 占比 30%+ 且 margin 平","具體門檻":"季度 EV 段 EBIT、Equinox EV 銷量","來源":"Q1 26 已 $1.1B 額外調整，需觀察是否最後一輪"}},{"id":"H3","text":"OEM 估值 mean revert（mid-cycle PE 8x+）","columns":{"2Y":"Fwd PE 7x+ → 股價 +12%","5Y":"同業中位 8x+ 確認","10Y":"—","具體門檻":"同業中位 Fwd PE","來源":"StockAnalysis / Macrotrends 5Y 歷史"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"✅","trap":"🟡","moat_trend":"穩定","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":78.79,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
