你是 stock-analyst **v20 判斷 agent**，標的 DDOG（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"DDOG","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":1121.454,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；YoY +35.6%（去年同期 826.760）、QoQ +11.4%（+115.0M，公司稱為史上最大單季增量）"},"note":"Zacks 共識約 1.08B，超出約 3.8%（來源：Yahoo Finance／Zacks 轉載）；也高於公司自家 Q2 指引上緣 1.08B（指引 1.07–1.08B）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income／margin","value":257.031,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（利益率 22.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；含 DASH 年會成本約 15M（CFO 電話會）"},"note":"高於公司自家指引 225–235M（利益率 21–22%）；分析師共識未查得"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income／margin","value":5.455,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（利益率 0.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）"},"note":"未查得共識（GAAP 端與 non-GAAP 差 251.6M，主要是股權激勵）"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":278.704,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（FCF 利益率 24.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；營業現金流 315.872M，扣 capex 與資本化軟體後（Q2 單季由上半年累計減 Q1 推得約 9.9M + 27.3M）"},"note":"未查得共識"},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation（占營收／占 non-GAAP 營業利益）","value":220.251,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（占營收 19.6%；占 non-GAAP 營業利益 85.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；分項：營收成本 9.256M、R&D 131.682M、S&M 47.098M、G&A 32.215M。GAAP 營業利益僅 5.5M，故不以 GAAP 為分母"},"note":"不適用"},{"id":"f_kpi5_guidance_q3_fy2026_reven","label":"Guidance: Q3 FY2026 revenue","value":"1135–1145","period":"Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026","unit":"USD M（YoY +28–29%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；CFO 稱指引已計入最大客戶用量下降（該客戶已續約）"},"note":"Q3 營收共識未查得"},{"id":"f_kpi6_guidance_q3_fy2026_non_g","label":"Guidance: Q3 FY2026 non-GAAP operating income／EPS","value":"營業利益 260–270M（利益率 23–24%）；non-GAAP EPS 0.63–0.65（約 378M 稀釋股數）","period":"Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026","unit":"USD M／USD per share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）"},"note":"未查得 Q3 共識"},{"id":"f_kpi7_guidance_fy2026_revenue_","label":"Guidance: FY2026 revenue／non-GAAP operating income／EPS","value":"營收 4450–4470M（YoY +30%）；non-GAAP 營業利益 1010–1030M（利益率 23%）；non-GAAP EPS 2.50–2.54（約 376M 稀釋股數）","period":"Q2 FY2026 財報公告於 2026-08-06，指引期間 FY2026","unit":"USD M／USD per share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2026 財報公告於 2026-08-06，指引期間 FY2026","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；CFO 另給：淨利息及其他收入約 180M、現金稅 30–40M、non-GAAP 稅率 21%、capex＋資本化軟體占營收 4–5%"},"note":"FY1 EPS 共識 2.53（2026-09-19 快照，來源：dd_numbers_extra.py consensus_revision），落在指引 2.50–2.54 內"},{"id":"f_kpi8_non_gaap_gross_margin_pr","label":"Non-GAAP gross margin（公司未單獨揭露 product gross margin）","value":79.6,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）：non-GAAP 毛利 892M；GAAP 毛利 881.341M（78.6%）出自 8-K Ex-99.1"},"note":"未查得共識；管理層稱毛利率長期在 80% 上下波動"},{"id":"f_kpi9_customers_with_arr_100k","label":"Customers with ARR ≥ $100k","value":4720,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"家（占 ARR 約 91%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release；占 ARR 比率出自 Q2 財報電話會"},"note":"不適用"},{"id":"f_kpi10_total_customers","label":"Total customers","value":33400,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"家","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CEO 準備稿（2026-08-06）"},"note":"不適用"},{"id":"f_kpi11_ai_native_1m_1m_arr_ai","label":"AI-native 客戶群：年支出 ≥$1M 家數（公司未揭露全公司 ≥$1M ARR 家數，此為 AI 群組口徑）","value":31,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"家（其中年支出 ≥$10M 為 8 家；AI 客戶群共約 750 家）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）"},"note":"不適用"},{"id":"f_kpi12_net_revenue_retention_tr","label":"Net revenue retention（trailing 12 個月）／gross revenue retention","value":"NRR 低 120%（low 120s）；GRR 中後段 90%（mid- to high 90s）","period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"%（公司只給區間，未給精確值）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）"},"note":"不適用"},{"id":"f_kpi13_rpo_current_rpo","label":"RPO／current RPO","value":3470,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（YoY +43%；cRPO YoY 約 +40%，RPO 期間拉長）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[13]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）；公司稱營收比 billings／RPO 更能反映業務趨勢"},"note":"未查得 RPO 共識"},{"id":"f_kpi14_billings","label":"Billings","value":1180,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（YoY +38%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[14]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）"},"note":"未查得共識"},{"id":"f_kpi15_ai_yoy","label":"非 AI 客戶營收 YoY 成長","value":"高 20%（high 20s）","period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"%（公司只給區間）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[15]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CEO／CFO 準備稿（2026-08-06）"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ddog_gross_margin_pct","label":"DDOG 毛利率","value":79.58,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ddog_operating_margin_pct","label":"DDOG 營業利益率","value":2.3,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ddog_fcf_margin_pct","label":"DDOG FCF 利潤率","value":25.93,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_snow_gross_margin_pct","label":"SNOW 毛利率","value":67.03,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNOW.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snow_operating_margin_pct","label":"SNOW 營業利益率","value":-22.76,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNOW.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snow_fcf_margin_pct","label":"SNOW FCF 利潤率","value":21.96,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNOW.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_dt_gross_margin_pct","label":"DT 毛利率","value":81.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dt_operating_margin_pct","label":"DT 營業利益率","value":13.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dt_fcf_margin_pct","label":"DT FCF 利潤率","value":26.53,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_estc_gross_margin_pct","label":"ESTC 毛利率","value":75.5,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ESTC.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_estc_operating_margin_pct","label":"ESTC 營業利益率","value":-1.54,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ESTC.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_estc_fcf_margin_pct","label":"ESTC FCF 利潤率","value":19.37,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ESTC.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_now_gross_margin_pct","label":"NOW 毛利率","value":73.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_now_operating_margin_pct","label":"NOW 營業利益率","value":9.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_now_fcf_margin_pct","label":"NOW FCF 利潤率","value":30.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":179.04,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-10.55,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":28.28,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.79,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.53 → 2.55）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.98 → 2.98）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.76 → 3.76）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.55,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.98,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.76,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.79,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 2.53 → 2.55（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":248.67,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":15.11,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝41.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":41.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":14.19,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝25.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":25.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":70.21,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 2.55，分子＝快照價 179.04","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-3926.36,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 1307.23、現金 5233.59（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":361.04,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":60714.7,"period":"2026-11-08","unit":"USD m","basis":"市值 64641.06 ＋ 淨負債 -3926.36","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":4521.48,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（46 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":5530.37,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（46 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":13.43,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 179.04 / W52 188.17 / W104 160.4 / W250 128.27 / W250 13週斜率 1.09%"},{"id":"f_ma_w52","label":"52 週均線","value":188.17,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":160.4,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":128.27,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.09,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Ramp 供應商頁：截至 2026 年 9 月，在有採用可觀測性(Observability)類供應商的組織中，34% 使用 Datadog，較去年同期持平（頁面寫 0% YoY、up <1 percentage point）；Datadog 在該類別排名第 2，月對月維持排名。搜尋摘要另出現 8 月版本文字為 down <1pp，方向皆為約持平。頁面未載明樣本口徑。","source":"https://ramp.com/vendors/datadog (Ramp「Datadog Ramp Rate: A Data-Backed Look」)","url":null,"excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Gartner 2026 Magic Quadrant for Observability Platforms：Datadog 連續第 6 年入選 Leader，並在 Ability to Execute 軸位置最高（Datadog 新聞稿自述）。","source":"GlobeNewswire：Datadog Named a Leader in the 2026 Gartner Magic Quadrant For Observability Platforms For Sixth Consecutive Year — https://www.globenewswire.com/news-release/2026/07/15/3328024/0/en/datadog-named-a-leader-in-the-2026-gartner-magic-quadrant-for-observability-platforms-for-sixth-consecutive-year.html","url":null,"excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"FinancialContent 評論文章稱：Palo Alto Networks 收購 Chronosphere、Snowflake 收購 Observe，是把資料儲存、資安與監控合併成單一平台的趨勢，文章形容為對 Datadog 的「Pincer」夾擊威脅；並稱 Dynatrace 是企業市場「chief rival」（Davis AI 歷來被視為較成熟，但 Bits AI 推出後差距縮小），Cisco 正把 Splunk 的日誌優勢與網通硬體整合、主攻傳統企業。此為第三方評論文章的描述，非份額數據。","source":"FinancialContent：Datadog (DDOG) and the 2026 Observability Frontier: Navigating the AI Re-Architecting Phase — https://www.financialcontent.com/article/finterra-2026-1-27-datadog-ddog-and-the-2026-observability-frontier-navigating-the-ai-re-architecting-phase","url":null,"excerpt":null,"as_of":"2026-01-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Datadog's largest customer renewed a nine-figure agreement but reduced its usage; per the search summary of the TheStreet article, this affected the company's Q3 and full-year 2026 forecasts. Article body not retrieved (WebFetch returned 403), so the exact contract figures and whether the usage cut involved in-house or a second vendor are not confirmed.","source":"TheStreet, 'Datadog's largest customer renews deal but cuts usage' https://www.thestreet.com/investing/stocks/datadogs-largest-customer-renews-deal-but-cuts-usage","url":null,"excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"SaaStr states 'OpenAI is Datadog's biggest single customer' (analyst assessment, not a company-named disclosure), and that the AI-native cohort including it grew only 'high single digits' in Q1 2026.","source":"SaaStr, 'Datadog Stock Is Up +66%. Here Are 5 Reasons Why...' https://www.saastr.com/datadogup/","url":null,"excerpt":null,"as_of":"2026-05-25","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"+","claim":"SaaStr reports the largest new logo in Datadog's history was consolidating onto Datadog from 'more than five open-source, commercial, hyperscaler, and in-house' tools, and states 'the AI labs themselves are now choosing Datadog over building in-house'. SaaStr's read is that the new logo is most likely Anthropic; this identity is the outlet's inference, not a company disclosure.","source":"SaaStr, 'Datadog Stock Is Up +66%. Here Are 5 Reasons Why...' https://www.saastr.com/datadogup/","url":null,"excerpt":null,"as_of":"2026-05-25","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Per a secondary summary of the FY2025 10-K, Datadog identified an 'AI-native cohort' that 'includes our largest customer', and quantified the cohort's contribution at about seven percentage points of YoY revenue growth for the quarter ended 2025-12-31.","source":"Mungomash, 'Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail' https://mungomash.com/orgs/datadog/financials/ (summarising Datadog FY2025 10-K)","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#4","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Per the same secondary source, one large AI-native customer's decision in early 2024 to scale down and partially re-platform its observability stack onto internal tooling drove the public growth deceleration that began with the Q1 2024 print.","source":"Mungomash, 'Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail' https://mungomash.com/orgs/datadog/financials/","url":null,"excerpt":null,"as_of":"2024-05-07","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Q2 2026 法說會：管理層不點名最大客戶，只說是「一家領先的 AI 公司」，使用 17 項 Datadog 產品，剛完成一筆「九位數美元」的續約。續約後用量有下降（usage reduction），已納入 Q3 與 FY2026 財測；CEO Pomel 稱今年剩餘時間的財測已「fully derisked」。","source":"The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","url":null,"excerpt":null,"as_of":"2026-08-13","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q2 2026 法說會：管理層表示剔除最大客戶後，其餘業務的成長率與整體「幾乎相同」（pretty much the same growth rate as the rest of the business）。","source":"The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","url":null,"excerpt":null,"as_of":"2026-08-13","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q2 2026：AI 原生客群超過 750 家，其中 31 家年支出逾 100 萬美元、8 家逾 1,000 萬美元；管理層稱前 10 大 AI 公司「全數」是客戶。公司未在此次法說會把 AI 原生客群量化為占營收的百分比。","source":"The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","url":null,"excerpt":null,"as_of":"2026-08-13","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q2 2026：非 AI 客戶營收年增加速至 20% 後段（high 20s%），Q1 為 20% 中段（mid-20s），去年同期為 18%。","source":"GuruFocus, Datadog Inc (DDOG) Q2 2026 Earnings Call Highlights: Revenue Surges 36% to $1.12B, https://www.gurufocus.com/news/9014386/datadog-inc-ddog-q2-2026-earnings-call-highlights-revenue-surges-36-to-112b-aidriven-growth-accelerates","url":null,"excerpt":null,"as_of":"2026-08-13","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#4","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q2 2026：過去 12 個月淨營收留存率（NRR）為 120% 出頭（low 120s），毛營收留存率（GRR）為 90% 中後段（mid- to high 90s），管理層稱流失（churn）維持低檔。","source":"The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","url":null,"excerpt":null,"as_of":"2026-08-13","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#5","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K（2026-02-18 提交）有「AI-native cohort」一詞，並註明該客群「包含我們最大的客戶」；該客群對 2025 年 12 月底當季營收年增的貢獻約 7 個百分點。（二手來源轉述，未讀到 10-K 原文；未查到 10-K 是否列出單一客戶占營收 ≥10% 的具體百分比。）","source":"mungomash.com「Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail」（搜尋摘要轉述 FY2025 10-K；頁面 WebFetch 回 404，未能直接驗證）","url":null,"excerpt":null,"as_of":"2026-02-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#6","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Q1 2026 10-Q（2026-05-07 提交）沿用「AI-native cohort 包含最大客戶」的措辭，並把該客群對 2026 年 3 月底當季營收年增的貢獻改寫為「high single digits」（個位數高段）。（二手來源轉述，未讀到 10-Q 原文。）","source":"mungomash.com「Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail」（搜尋摘要轉述 Q1 2026 10-Q；頁面 WebFetch 回 404，未能直接驗證）","url":null,"excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#7","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"外部資料點（Datadog 本身未點名最大客戶是誰，此處的對應是分析師/媒體推測，未經公司確認）：OpenAI 於 2026-03-31 完成 1,220 億美元募資，募後估值 8,520 億美元，同時把循環信貸額度擴大到約 47 億美元，交割時未動用。另有報導稱 OpenAI 帳上無負債，但 2026 年 Q1 燒錢約 37 億美元。","source":"搜尋摘要轉述 Sacra「OpenAI revenue, valuation & funding」(https://sacra.com/c/openai/) 與 The Next Web「OpenAI's suspiciously clean balance sheet is about to get a hard look」(https://thenextweb.com/news/openai-light-balance-sheet-ipo-scrutiny)；各事實對應哪一篇未逐條核對","url":null,"excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner projects the observability platform market will reach $14.2 billion by 2028, driven by complexity in hybrid and cloud-native environments.","source":"Network World, 'In crowded observability market, Gartner calls out AI capabilities, cost optimization, DevOps integration' https://www.networkworld.com/article/4032218/in-crowded-observability-market-gartner-calls-out-ai-capabilities-cost-optimization-devops-integration.html","url":null,"excerpt":null,"as_of":"2025-08-06","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Gartner's observability report says more than 40 vendors compete in the space (20 evaluated in the Magic Quadrant), that 'questions about total cost of ownership are now standard', and that leading platforms must offer granular data retention controls, tiered storage and usage-based pricing.","source":"Network World, 'In crowded observability market, Gartner calls out AI capabilities, cost optimization, DevOps integration' https://www.networkworld.com/article/4032218/in-crowded-observability-market-gartner-calls-out-ai-capabilities-cost-optimization-devops-integration.html","url":null,"excerpt":null,"as_of":"2025-08-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Datadog Q1 2026 revenue was about $1.01B, up 32% YoY (vs 29% in Q4 2025 and 25% in Q1 2025); sequential growth of 6% was the strongest since 2022.","source":"BigGo Finance, '[DDOG Q1 2026 Earnings Call] Datadog Surpasses $1B in Quarterly Revenue as AI Workloads Fuel 32% Growth' https://finance.biggo.com/news/US_DDOG_2026-05-07","url":null,"excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Per the Q1 2026 call as reported, trailing-12-month net revenue retention improved to the low 120% range and gross retention stayed in the mid-to-high 90s.","source":"BigGo Finance, '[DDOG Q1 2026 Earnings Call] Datadog Surpasses $1B in Quarterly Revenue as AI Workloads Fuel 32% Growth' https://finance.biggo.com/news/US_DDOG_2026-05-07","url":null,"excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Datadog guided Q2 2026 revenue to $1.07B-$1.08B (29-31% YoY) and full-year 2026 revenue to $4.30B-$4.34B (25-27% YoY), as reported in the Q1 2026 call summary.","source":"BigGo Finance, '[DDOG Q1 2026 Earnings Call] Datadog Surpasses $1B in Quarterly Revenue as AI Workloads Fuel 32% Growth' https://finance.biggo.com/news/US_DDOG_2026-05-07","url":null,"excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q1 2026 call summary: 22 customers spend over $1M a year on Datadog's AI products (5 above $10M); two hyperscale labs signed seven- and eight-figure annualized deals for training-workload monitoring; 6,500 customers (20% of total, 80% of ARR) use AI integrations.","source":"BigGo Finance, '[DDOG Q1 2026 Earnings Call] Datadog Surpasses $1B in Quarterly Revenue as AI Workloads Fuel 32% Growth' https://finance.biggo.com/news/US_DDOG_2026-05-07","url":null,"excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.H","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner predicts 40% of organizations deploying AI will use AI observability to monitor model performance by 2028.","source":"Gartner press release 'Gartner Predicts 40% of Organizations Deploying AI Will Use AI Observability to Monitor Model Performance by 2028' https://www.gartner.com/en/newsroom/press-releases/2026-05-12-gartner-predicts-40-percent-of-organizations-deploying-ai-will-use-ai-observability-to-monitor-model-performance-by-2028","url":null,"excerpt":null,"as_of":"2026-05-12","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#7","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Grafana Labs reached $400M+ ARR with 7,000 customers as of September 2025 (competitor scale figure cited in a vendor comparison blog; blog publish date not shown, as_of day set to the first of the stated month).","source":"OpenObserve blog, '10 Best Datadog Competitors & Alternatives in 2026' https://openobserve.ai/blog/datadog-competitors/","url":null,"excerpt":null,"as_of":"2025-09-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因子指出歐盟 AI Act（2024-08 生效）及美國各州隱私／AI 法規為一般性監管風險；未見針對 Datadog 的反壟斷調查或拆分事項。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm","excerpt":"For example, the European Union's Artificial Intelligence Act, which would apply beyond the European Union’s borders, came into effect in August 2024. It contains numerous requirements regarding the development and use of AI and imposes significant monetary fines.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Datadog's own export control page (effective 2026-05-05) classifies its observability and security services as ECCN 5D002.c.1 under license exception ENC/740.17(b)(1); automation, incident management and AI products (e.g. Bits AI) as 5D992.c.1 under ENC/740.17(b)(1); and the Datadog Agent and other downloadable products (SDKs, IDE plugins) as EAR99 / NLR (no license required).","source":"Datadog, 'Export Control Information' https://www.datadoghq.com/legal/export-control-information/2026-05-05/","url":null,"excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K（截至 2025-12-31，2026-02-05 提交）把「political turmoil, natural catastrophes, outbreaks of contagious diseases, warfare and terrorist attacks ... such as the conflicts in Ukraine and the Middle East」列為國際營運風險，並提到對俄制裁可能加劇相關趨勢。","source":"Datadog, Inc. Form 10-K FY2025, SEC EDGAR https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm","url":null,"excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K 經 WebFetch 抽取，全文未出現 China、Taiwan、半導體供應鏈或製造依賴的字樣（純 SaaS，10-K 未揭露實體製造環節）。此為抽取結果，非逐頁人工確認。","source":"Datadog, Inc. Form 10-K FY2025, SEC EDGAR https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm","url":null,"excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K 載明約 44% 全職員工位於美國以外，其中 34% 在法國。","source":"Datadog, Inc. Form 10-K FY2025, SEC EDGAR https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm","url":null,"excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Datadog 官方部落格稱：「Following a March 2023 outage of our own, Datadog launched a company-wide initiative to improve regional isolation across Datadog sites」，並推出 Disaster Recovery 產品，讓客戶在雲端供應商中斷時維持可觀測性。","source":"Datadog Blog, 'Maintain observability during cloud outages with Datadog Disaster Recovery' https://datadoghq.com/blog/ddr-mitigates-cloud-provider-outages","url":null,"excerpt":null,"as_of":"2026-06-09","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"產業層面：雲端集中風險來自過多關鍵流程依賴單一供應商、單一區域或中央服務；AWS us-east-1 是最老、最大的區域，並承載其他區域所依賴的全域控制功能（如 IAM 更新、DynamoDB Global Tables），該區失效會擴散到區域之外。此文為通論，未指名 Datadog 受影響。","source":"cloudmagazin.com, 'One Region Fails, Half of the Supply Chain Grinds to a Halt' https://www.cloudmagazin.com/en/2026/07/12/one-region-fails-half-of-the-supply-chain-grinds-to-a-halt","url":null,"excerpt":null,"as_of":"2026-07-12","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 Q2 營收約 $1.12B，年增 36%；上半年營收約 $2.1B，年增 34%（Q1 為 $1,006M、年增 32%）。","source":"Datadog 8-K ex-99.1 (period ended 2026-06-30) https://www.sec.gov/Archives/edgar/data/0001561550/000162828026053829/ex-991x20260630x8k.htm ；GuruFocus「Datadog Q2 2026 Earnings Call Highlights」","url":null,"excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"AI 原生客戶群超過 750 家，其中 31 家年支出逾 $1M、8 家逾 $10M；全球前 10 大 AI 公司皆為客戶。非 AI 營收年增加速至 20% 後段（Q1 為 20% 中段，去年同期 18%）。","source":"Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/ ；GuruFocus Q2 2026 highlights","url":null,"excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"最大客戶出現用量下滑（同時簽了九位數美元續約）；管理層稱已把此影響完整反映在 Q3 與全年 2026 指引，並稱排除該客戶後整體趨勢與加速一致。","source":"Motley Fool, Datadog Q2 2026 Earnings Call Transcript（WebFetch 摘要）https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/ ；GuruFocus Q2 2026 highlights","url":null,"excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"指引：Q3 營收 $1.135B–$1.145B（年增 28%–29%，低於 Q2 的 36%）；全年 2026 營收 $4.45B–$4.47B（年增約 30%）。","source":"GuruFocus, Datadog Q2 2026 Earnings Call Highlights https://www.gurufocus.com/news/9014386/datadog-inc-ddog-q2-2026-earnings-call-highlights-revenue-surges-36-to-112b-aidriven-growth-accelerates","url":null,"excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"客戶結構：總客戶約 33,400（年增約 2,000）；年 ARR≥$100k 客戶約 4,720（去年同期約 3,850，年增 23%），占總 ARR 91%；新客戶貢獻年增量的 30%（Q1 為 25%）；過去 12 個月淨留存率在 120% 出頭，毛留存率在 90% 中後段。","source":"Motley Fool, Datadog Q2 2026 Earnings Call Transcript https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/ ；Datadog 8-K 2026-06-30","url":null,"excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"產品線 ARR（截至 2025 年底、2026-02 報導）：基礎設施監控 ARR 逾 $1.6B；日誌管理與 APM 各自突破 $1B ARR，兩者年增皆在 30% 中段。這是 Q4 2025 資料，非 Q2 2026 最新值。","source":"Yahoo Finance/Zacks, Will Datadog Stock Sustain Growth on Rising AI Cloud Monitoring Spend? https://finance.yahoo.com/news/datadog-stock-sustain-growth-rising-144300289.html","url":null,"excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"RUM（真實使用者監控）ARR 超過 $200M，年增逾 50%。","source":"Motley Fool, Datadog Q2 2026 Earnings Call Transcript https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","url":null,"excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"0","claim":"外部分析師共識（Zacks）2026 全年營收預估 $4.08B（年增 19.17%），為 2026-02 舊值，已低於公司 2026-08 指引 $4.45–4.47B；文中無 2027 共識。","source":"Yahoo Finance/Zacks https://finance.yahoo.com/news/datadog-stock-sustain-growth-rising-144300289.html ；GuruFocus Q2 2026 highlights（指引）","url":null,"excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"0","claim":"定價結構：APM Pro 約 $23/host/月、APM Enterprise 約 $34/host/月（2026 年牌價），日誌、基礎設施、RUM、Synthetics、SIEM 另計；同類報告稱 New Relic、Dynatrace、Splunk 成本與 Datadog 相近而非大幅便宜，企業議價可壓 35%–55% 牌價。Datadog 與 Dynatrace 投入 OpenTelemetry 相容以維持定價能力。來源為第三方部落格比較，非公司揭露。","source":"Uptrace, Top 10 Observability Tools in 2026 https://uptrace.dev/tools/top-observability-tools ；VendorBenchmark, Observability Platform Pricing Benchmarks 2026 https://vendorbenchmark.com/blog/observability-platform-pricing-benchmark-comparison","url":null,"excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#9","axis":"end_markets","section":"coverage","direction":"0","claim":"市佔（僅為網站偵測指標，非營收佔比）：2026 年 8 月偵測到 Datadog 在 APM 與錯誤追蹤類別占 5.78%，排在 Sentry、New Relic 之後第三；Dynatrace 3.38%、Grafana 2.43%。該指標反映瀏覽器代理程式部署，非客戶數或營收。","source":"Uptrace, Top 10 Observability Tools in 2026 https://uptrace.dev/tools/top-observability-tools","url":null,"excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#10","axis":"end_markets","section":"coverage","direction":"0","claim":"可觀測性市場規模第三方估計落差極大：2026 年 Mordor Intelligence $3.35B（2031 年 $6.93B，CAGR 15.62%）、Coherent $3.40B（CAGR 11.1%）、Business Research Insights $4.35B、MarketsandMarkets $11.91B（CAGR 14.1%）、Research Nester $34.1B。各家 CAGR 在 11%–16%。","source":"Mordor Intelligence https://www.mordorintelligence.com/industry-reports/observability-market ；MarketsandMarkets https://www.marketsandmarkets.com/Market-Reports/observability-tools-and-platforms-market-69804486.html ；Research Nester https://www.researchnester.com/reports/observability-tools-and-platforms-market/8139","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"groundcover（Datadog 競品廠商）2026-07-29 的指南結論稱：2026 年可觀測性品類的轉變是架構面的——以 eBPF 取代語言 agent、以 BYOC（資料留在客戶自己的 VPC）取代純 SaaS、以「依基礎設施計價」取代「依用量計價」。此為競品自家行銷文章的說法，非中立第三方量測。","source":"groundcover, 'Datadog Alternatives for Full-Stack Observability in 2026', https://www.groundcover.com/guides/datadog-alternatives-for-full-stack-observability","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"IT Connection（Currentanalysis）2026 年觀測性預測稱：應用開發工具類新創將透過在自家產品組合內增加可觀測性功能，對整個可觀測性市場產生破壞性影響（標題：Makers of Dev Tools to Disrupt Space）。搜尋摘要只取得此論點，未取得內文細節與具體廠商名單。","source":"IT Connection / Currentanalysis, 'Observability Predictions 2026: Makers of Dev Tools to Disrupt Space', https://itcblogs.currentanalysis.com/2026/01/29/observability-predictions-2026-makers-of-dev-tools-to-disrupt-space/","url":null,"excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Splunk 官方部落格 2026-03-24 載明：2025 年底至 2026 年初，Palo Alto Networks 收購 Chronosphere、LogicMonitor 收購 Catchpoint、Snowflake 宣布擬收購 Observe Inc.。該文未提及 Datadog、eBPF、OpenTelemetry 或 AI SRE agent 為競爭威脅。","source":"Splunk, 'Ahead of the Curve: How Recent M&A Forecasts New Observability Trends for 2026', https://www.splunk.com/en_us/blog/observability/new-observability-trends-for-2026.html","url":null,"excerpt":null,"as_of":"2026-03-24","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"As of Q1 2026, Datadog had over 26 products, of which 5 had crossed $100M ARR and 3 were between $50M and $100M ARR; 18 products were still early in their lifecycle. (Secondary-source figure from a search-result summary; not checked against the primary earnings release.)","source":"Capital Blueprint (Substack), 'Datadog, Inc. (NASDAQ: DDOG) — Deep Investment Analysis', https://capitalblueprint.substack.com/p/datadog-inc-nasdaq-ddog-deep-investment","url":null,"excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-06 公司給 FY2026 EPS 指引 2.50–2.54、營收約 45 億美元，高於當時共識 EPS 2.07、營收 43 億美元（MarketBeat 彙整）","source":"MarketBeat: Datadog updates FY 2026 earnings guidance 2026-08-06","url":"https://www.marketbeat.com/instant-alerts/datadog-nasdaqddog-updates-fy-2026-earnings-guidance-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 指引 EPS 0.63–0.65、營收約 11 億美元，MarketBeat 引共識 EPS 0.52；Chartmill 另列 EPS 0.67／營收 11.69 億美元，兩家口徑不一","source":"MarketBeat: Datadog releases Q3 2026 earnings guidance 2026-08-06; Chartmill DDOG estimates","url":"https://www.marketbeat.com/instant-alerts/datadog-nasdaqddog-releases-q3-2026-earnings-guidance-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 共識評級 Moderate Buy，共識目標價 $271.57（另一則引 $272.48）；7 月曾為 $253.36；Canaccord 8/4 目標價 $295、Oppenheimer 7/20 目標價 $300，個別目標價有分布但聚合站數字彼此不一","source":"MarketBeat instant alerts（Canaccord 2026-08-04、Oppenheimer 2026-07-20）","url":"https://www.marketbeat.com/instant-alerts/datadog-nasdaqddog-stock-price-expected-to-rise-canaccord-genuity-group-analyst-says-2026-08-04/","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill：FY2026 EPS 共識 2.60（51 位分析師，2026-10-24 記錄），下一季營收預估近 3 個月上修 3.63%","source":"Chartmill DDOG estimates","url":"https://www.chartmill.com/stock/quote/DDOG/estimates","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Barchart：Datadog 連續超越共識與客戶集中度風險","source":"Barchart","url":"https://www.barchart.com/story/news/3675897/datadog-s-consensus-beat-streak-what-happens-when-customer-concentration-finally-matters","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Datadog 於 2026-06-30 宣布收購 Adaptive ML，併入 Datadog AI Research；價格未查到。","source":"ChartMill：Datadog Acquires Adaptive ML to Pioneer RLOps","url":"https://www.chartmill.com/news/external/63300/datadog-acquires-adaptive-ml-to-pioneer-rlops-what-s-ahead","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 8-K 共 7 份，僅 1 份含重大項目（2026-04-22 Item 8.01，為改在內華達州註冊的法律意見附件）；無訴訟、SEC 調查、重編（Item 4.02）類 8-K。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001561550&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Datadog 於 2026-06-30 宣布收購 Adaptive ML，併入 Datadog AI Research；價格未查到。","source":"ChartMill：Datadog Acquires Adaptive ML to Pioneer RLOps","url":"https://www.chartmill.com/news/external/63300/datadog-acquires-adaptive-ml-to-pioneer-rlops-what-s-ahead","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 中無 Item 4.02（非可靠財報）項目，搜尋亦無 SEC 傳票或重編紀錄。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001561550&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 13 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"DDOG","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.58,"operating_margin_pct":2.3,"fcf_margin_pct":25.93,"rd_intensity_pct":42.61},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"SNOW","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.03,"operating_margin_pct":-22.76,"fcf_margin_pct":21.96,"rd_intensity_pct":38.78},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNOW","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"DT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.05,"operating_margin_pct":13.55,"fcf_margin_pct":26.53,"rd_intensity_pct":23.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ESTC","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":75.5,"operating_margin_pct":-1.54,"fcf_margin_pct":19.37,"rd_intensity_pct":25.26},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ESTC","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"NOW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":73.08,"operating_margin_pct":9.68,"fcf_margin_pct":30.78,"rd_intensity_pct":22.47},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"DDOG"},"financial_history":{"ticker":"DDOG","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":1675100000.0,"revenue_yoy_pct":null,"gross_margin_pct":79.3,"operating_margin_pct":-3.5,"net_income":-50160000.0,"diluted_eps":-0.16,"free_cash_flow":353518000.0,"fcf_margin_pct":21.1,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2128359000.0,"revenue_yoy_pct":27.06,"gross_margin_pct":80.74,"operating_margin_pct":-1.57,"net_income":48568000.0,"diluted_eps":0.14,"free_cash_flow":597548000.0,"fcf_margin_pct":28.08,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2684275000.0,"revenue_yoy_pct":26.12,"gross_margin_pct":80.79,"operating_margin_pct":2.02,"net_income":183746000.0,"diluted_eps":0.52,"free_cash_flow":775103000.0,"fcf_margin_pct":28.88,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3427158000.0,"revenue_yoy_pct":27.68,"gross_margin_pct":79.96,"operating_margin_pct":-1.29,"net_income":107741000.0,"diluted_eps":0.31,"free_cash_flow":914717000.0,"fcf_margin_pct":26.69,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/DDOG/DDOG_Q3_2026_Earnings_Call_20261104.md）

# Q3 2026 Earnings Call
**Datadog, Inc.** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to the Third Quarter 2026 Datadog Earnings Conference Call. [Operator Instructions] Please be advised that today's call is being recorded. I will now hand it over to our first speaker, AJ Ljubich, Senior Vice President, Strategic Finance and Investor Relations. Please go ahead.

**Alexander Joseph Ljubich** (Executives):
Thank you, Victor. Good morning, and thank you for joining us to review Datadog's Third Quarter 2026 Financial Results, which we announced in our press release issued this morning. Joining me on the call today are Olivier Pomel, Datadog's Co-Founder and CEO; and David Obstler, Datadog's CFO. First, I'd like to thank Yuka Broderick for her excellent work leading our IR function over the last 5.5 years as she takes on a new role within Datadog. 
I'm excited to step back into the IR function after having worked with many of you through the company's 2019 IPO. During this call, we will make forward-looking statements, including statements related to our future financial performance, our outlook for the fourth quarter and for the fiscal year of 2026 and related notes and assumptions, our product capabilities and our ability to capitalize on market opportunities. 
The words anticipate, believe, continue, estimate, expect, intend, and will and similar expressions are intended to identify forward-looking statements or similar indications of future expectations. These statements reflect our views as of today and are subject to a variety of risks and uncertainties that could cause actual results to differ materially. For a discussion of the material risks and other important factors that could affect our actual results, please refer to our Form 10-Q for the quarter ended June 30, 2026. 
Additional information will be made available in our upcoming Form 10-Q for the fiscal quarter ended September 30, 2026, and other filings with the SEC. This information is also available on the Investor Relations section of our website, along with a replay of this call. We will discuss non-GAAP financial measures, which are reconciled to the most directly comparable GAAP financial measures in our earnings release, which are available at investors.datadoghq.com. With that, I'd like to turn the call over to Olivier.

**Olivier Pomel** (Executives):
Thanks, AJ, and thank you all for joining us today to go over our Q3 results. Let me begin with this quarter's business drivers. I am pleased to say that we executed a strong Q3. We saw strength across our business, including across our product lines and across our diverse customer base. Revenue growth from our non-AI customers accelerated for the fifth straight quarter and was in the high 20s percent year-over-year, up about 1 percentage point from last quarter and up from about 20% in the year ago quarter. 
Additionally, our AI customer cohort remains a strong growth driver. This cohort continued to grow and diversify, both in the number of customers we serve and in the scale of those customers. Overall, we continue to see healthy demand as customers from the most tech-forward startups to the largest enterprises in the world are building with AI and with modern technologies, which we believe is fueling expanded adoption of the cloud and of the Datadog platform. 
Regarding our Q3 financial performance and key metrics. Revenue was $1.2 billion, an increase of 35% year-over-year and above the high end of our guidance range. We ended Q3 with about 33,500 customers, up from about 32,000 a year ago. We also ended with about 4,860 customers with an ARR of $100,000 or more, up from about 4,060 a year ago. These customers generated about 91% of our ARR. 
And we generated free cash flow of $251 million with a free cash flow margin of 21%. Turning to product adoption. Our platform strategy continues to resonate in the market. 61% of our customers now use 4 or more products, up from 54% a year ago. 41% of our customers use 6 or more products, up from 31% a year ago and 16% of our customers use 10 or more products, up from 8% a year ago. So we're landing more customers and delivering value across more products through our unified platform. One milestone we are very proud of, our Infrastructure Monitoring suite of products now exceeds $2 billion in ARR, growing in the mid-30s percent year-over-year. 
Infrastructure Monitoring was the first product we brought to market more than 10 years ago. Today, our customers rely on Datadog for visibility across their environments, including cloud infrastructure, on-prem servers, containers, serverless applications and GPU fleets. And while we're thrilled to reach this milestone, we still feel that we're just getting started. According to industry analysts, we are the market share leader in global observability, but with a percentage market share still in the teens. 
Moving on to R&D. As AI changes how our customers build and run software, we've been investing and executing on 2 fronts: AI for Datadog and Datadog for AI. First, AI for Datadog. These are AI products and capabilities that make the Datadog platform more useful and increasingly automated for our customers. First off, our flagship agent, Bits AI, is off to a very strong start. Since we launched Bits, it has become the fastest adopted product in our history. And in October, Bits Testing became generally available. 
With a single click, it discovers the critical user flow in an application and generates tests to cover them. Meanwhile, our AI research team is hard at work pushing the boundaries of what Bits and our platform can do. Last month, we introduced Scout, our own reasoning model specifically optimized for SRE tasks. 
Scout was built using our in-house distributed reinforcement learning infrastructure and now powers our Bits Investigations. This is exciting for 2 reasons. First, it performs on par or even better than frontier models on alert investigations at a fraction of the inference cost. 
This is valuable as it allows Bits to investigate many more alerts, start earlier and go deeper on incidents as an always-on first responder for our customers. Second, this is also exciting as a demonstration of what we can achieve when we train models with our own production data, critical user workflows and internal tooling. Scout is only the beginning. With the Adaptive ML team, which joined us in June, we are broadly accelerating our work on reinforcement learning and model post-training.
Over time, we expect our research efforts to drive a step change in capabilities across our platform and move us closer to our goal of autonomous operations. Moving on next to Datadog for AI. These are the products that deliver end-to-end observability and security across the new AI stack. As AI moves from experimentation into production, customers today need to answer 3 key questions, how is it performing? Is it secure? And what's the ROI or is it worth the spend? 
And because AI doesn't run in isolation, they want these answers on the same platform as the rest of their tech stack. On performance, we covered the whole AI stack from compute all the way to agents. GPU monitoring now goes beyond hardware reliability with new capabilities that help customers maximize fleet utilization, increase training throughput and serve inference at a lower cost per request. The number of GPU devices we monitor is up by a factor of 8 so far this year, and some of our frontier lab customers are working with us as design partners on these capabilities. 
Going up the stack, Agent Observability helps teams monitor and evaluate their agents in production, including the quality of their responses, latency and token usage. The number of spans sent to Agent Observability is now up by a factor of 9 this year. We've also made Agent Observability available in the Anthropic marketplace, and we are a launch partner to OpenAI's new enterprise marketplace as well. So now customers can buy our products directly through the frontier labs they already work with. 
On the security side, our AI Guard product discovers the custom agents running across an organization and protects them at runtime against prompt injection and data exfiltration, drawing on the same real-time data we collect to observe them. And on the cost side, companies everywhere are grappling with a very fast growth in token and AI spend. Beyond the 3 major clouds, AI providers are now the largest category of spend our customers monitor in Datadog Cloud Cost Management, or CCM. 
Now with AI cost in CCM, customers can see which teams, models and agents drive their AI spend, can govern that spend with budgets, forecasts and anomaly alerts. More than 1/3 of our CCM customers now track AI costs. The number of customers doing so is up more than 11x. Moving up the stack again. Our agent console adds to our CCM data and shows exactly which agents are actually used by whom, for what tasks, at what cost and most importantly, with what outcomes. 
As we continue to innovate across AI for Datadog and Datadog for AI, independent research is taking note. Forrester named Datadog a leader in its 2026 Forrester Wave for AIOps Platforms. And Gartner's August 2026 AI Vendor Race report called Datadog the company to beat for observability platform. We believe this validates our leadership in observability as well as our ability to help customers manage complexity in the edge of AI. 
Let's move on to sales and marketing and look at a few of the deals our go-to-market teams have closed in what has been a very strong quarter. First, we signed a 7-figure annualized expansion with a leading software company, more than doubling their annual commitment. This customer is moving AI agents into production and will replace a stand-alone commercial tool with Datadog Agent Observability to monitor their cost and quality. And by using Flex Logs, they can gather and correlate larger log volumes at a lower cost. 
In total, they will consolidate 3 tools on to Datadog and grow to 20 Datadog products, including On-Call and Bits AI. Next, we landed a 5-year 7-figure annualized deal with the U.S. Federal Defense Agency. This customer runs thousands of cloud accounts across hundreds of mission owners. And as they've modernized, their manual tooling left them with fragmented visibility and security blind spots. They chose Datadog as their Enterprise Observability and Security platform and we'll start with 9 products, including Infrastructure Monitoring and Cloud Security. 
I want to congratulate our public sector team on this milestone win, which was a direct result of our investment in government and the FedRAMP High certification we secured earlier in the year. And we are actively expanding our government platform to support workloads up to Impact Level 5 or IL5, the highest level of accreditation for unclassified data, which is part of our long-term investment in the U.S. public sector. Next, we landed a 7-figure annualized deal with a leading home healthcare software company. 
As this customer has grown, fragmented tools have slowed incident response and hurt customer experience. They will consolidate 4 tools into Datadog, replacing their legacy log and security vendor with Flex Logs and Cloud SIEM and relying on our sensitive data scanner to help them stay HIPAA compliant. This customer will start with 9 Datadog products, including Incident Management and Bits AI for faster resolution. 
Next, we signed a 7-figure annualized expansion with a leading online entertainment company. This customer is seeing a surge in traffic with their peak season and is scaling effectively with Datadog. Their own AI agents already use our MCP server, and today, they are also adding Bits AI. This customer will grow to 23 Datadog products, including Agent Observability and Cloud Cost Management. Next, we landed a 7-figure annualized deals with 2 of Japan's most important banks. As they modernize their core financial systems, both banks are standardizing on Datadog for unified visibility across cloud and on-prem environments. 
Both customers are adopting the full Datadog platform, including all 3 pillars: Digital Experience, Security, Software Delivery, Service Management and Bits AI as they move towards AI-driven operations. Next, we landed a 6-figure annualized deal with a top European AI lab. These customers' developers were losing valuable time to slow builds and flaky tests with delayed releases in a highly competitive market. 
They chose Datadog CI Visibility and Test Optimization, replacing a commercial tool and freeing their own engineers to focus on shipping products. Their engineers also use Bits AI to quickly build monitors and custom analytics. Next, we signed a 7-figure annualized expansion for an 8-figure annualized deal with a leading AI coding company. This customer is growing rapidly and renewed early to keep pace with their expanding footprint. 
With this expansion, they will adopt Flex Logs and our new Infinite Cardinality Metrics to scale cost effectively with volume. And they are also one of the largest users of our MCP server. This customer will grow to 13 Datadog products. Finally, we signed an 8-figure annualized expansion with the AI division of one of the world's largest technology companies, which nearly tripled their annual commitment. Just 2 quarters after we landed them, they are scaling Datadog across a large number of AI training workloads. They are also adopting APM and Bits AI to further reduce engineering friction. 
Alongside these wins, on the other side of the customer spectrum, we are leaning into the large number of new AI native companies we see created every day by investing in our Datadog for startups program. We are broadening its reach to a larger number of start-ups that are earlier in their life cycle and offering deeper engineering collaboration with the ones that are seeing explosive growth. This is a truly exciting time to partner with start-ups. Now before I turn it over to David for a financial review, I'd like to say a few words on the longer-term outlook. 
There is no change to our overall view that digital transformation and cloud migration are long-term growth drivers for our business. And AI is another large growth driver for us today as AI workloads move into production to drive more cloud consumption and more usage of the Datadog platform, and we see that today across our business. All 15 of the top 15 AI leaders are our customers. And more broadly, we now serve over 850 AI customers, up from about 750 last quarter. And across our broader customer base, we also see AI activity growing substantially. 
About 1/3 of our customers now use one or more of our AI products, including 3/4 of our $100,000-plus customers with many of these customers still just getting started with these products, leaving a large opportunity for future expansion. And we continue to see rapid growth in agentic activity with a number of MCP tool calls up by a factor of 50 so far this year. We are tremendously excited about where this is going. As AI writes and runs more of our customers' software, they're shipping more code faster across a growing mix of models, agents and infrastructure. 
Of course, this generates complexity that is very quickly outpacing what even the best engineering teams can track on their own. And that's exactly the problem we're investing to solve. AI for Datadog takes on more of that work for them. Datadog for AI help them run their AI with confidence and our AI research turns our data into models that will deliver more autonomy over time. Because of that, now more than ever, we feel ideally positioned to help customers of every size and every industry as well as every type of user, whether humans or AI agents, so they can transform, innovate and drive value through AI and cloud adoption. And with that, I will turn it over to our CFO. David?

**David Obstler** (Executives):
Thanks, Olivier, and good morning to everybody. Our Q3 revenue was $1.197 billion, up 35% year-over-year. We continue to see robust usage growth from existing customers as well as a strong ramp in our new customers. Revenue growth accelerated within our broad base of customers, excluding AI customers, to the high 20s percent year-over-year, up about 1 percentage point from last quarter and up from about 20% in the year ago quarter. 
And we saw robust growth with broad-based strength across customer segments, spending bands and industries. And excluding our largest customer, revenue growth accelerated again. As we communicated in August, our largest customer reduced their usage in the third quarter, while their usage remained above their minimum commitment. Meanwhile, our AI customers growth continues to significantly outpace the rest of the business. This over 850 strong group continues to diversify and grow, including 39 customers spending more than $1 million annually with us. And we continue to land larger and grow faster with new logos, contributing more to revenue growth. 
The portion of our year-over-year revenue growth that relates to new customers was about 30% in Q3, up from 25% in the year ago quarter. And now regarding our retention metrics. Our trailing 12-month net revenue retention percentage was in the low 120s percent similar to last quarter, and churn remains low, with gross retention stable -- gross revenue retention stable in the mid- to high 90s. We believe this metric highlights the mission-critical nature of our platform for our customers. 
And now moving on to our financial results. Billings in the quarter were $1.16 billion, up 30% year-over-year. Remaining performance obligations, or RPO, was $3.85 billion, up 38% year-over-year. And current RPO grew in the mid-30s percent year-over-year. RPO duration increased slightly year-over-year. As a reminder, we continue to believe revenue is a better indication of our business trends than billings or RPO. Let's review some of the key income statement results. Unless otherwise noted, all metrics are non-GAAP. 
We have provided a reconciliation of GAAP to non-GAAP financials in our earnings release. For Q3, our gross profit was $972 million, and the gross margin was 81.2%. This compares to a gross margin of 79.6% last quarter and 81.2% in the year ago quarter. Q3 OpEx grew 25% year-over-year versus 26% last quarter and 32% in the year ago quarter. And Q3 operating income was $334 million or 28% operating margin compared to 23% last quarter and 23% in the year ago quarter. 
And now turning to the balance sheet and cash flow statements. We ended the quarter with $5.2 billion in cash, cash equivalents and marketable securities. Cash flow from operations was $290 million in the quarter. After taking into consideration capital expenditures and capitalized software, free cash flow was $251 million with a free cash flow margin of 21%. Quarterly, the timing of collections and payments vary and on a 12 -- trailing 12-month basis, free cash flow margin was 26%. And now for our outlook for the fourth quarter and for fiscal year 2026. First, our guidance philosophy overall remains unchanged. 
As a reminder, we base our guidance on trends observed in recent months and apply conservatism on these growth trends. Regarding our largest customer, our Q4 guidance contemplates their revenue at their minimum commitment. Now for the fourth quarter, we expect revenue to be in the range of $1.19 billion to $1.2 billion, which represents a 25% to 26% year-over-year growth. Excluding our largest customer, Q4 revenue growth implied in our guidance is in the low to mid-30s percent range. 
Non-GAAP operating income is expected to be in the range of $280 million to $290 million, which implies an operating margin of 24%. The fourth quarter includes large marketing investments, including AWS re:Invent. Our non-GAAP net income per share is expected to be in the $0.69 to $0.71 per share range based on approximately 379 million weighted average diluted shares outstanding. For the fiscal year 2026, we expect revenue to be in the range of $4.515 billion to $4.525 billion, which represents approximately 32% year-over-year growth. 
And non-GAAP operating income is expected to be in the range of $1.095 billion to $1.105 billion, which implies an operating margin of 24%. Finally, non-GAAP net income per share is expected to be in the range of $2.73 to $2.75 per share based on approximately 375 million weighted average diluted shares outstanding. Now some additional notes on our guidance. We expect net interest and other income for the fiscal year 2026 to be approximately $200 million. 
We expect cash taxes to be about $30 million to $40 million, and we continue to apply a 21% non-GAAP tax rate for 2026 and going forward. And finally, we expect capital expenditures and capitalized software together to be in the 3% to 4% of revenue range in fiscal year 2026. 
To summarize, we are pleased with our execution in Q3, which combines strong growth with strong profitability. We continue to invest to capture our long-term opportunity in the cloud and in AI. And I want to thank Datadogs worldwide for their efforts. Now with that, we will open the call for questions. Operator, let's begin the Q&A.

**Operator** (Operator):
[Operator Instructions] Our first question will come from the line of Sanjit Singh from Morgan Stanley.

**Sanjit Singh** (Analysts):
Congrats on the strong results on Q3. David, I want to start with the Q4 guide. If we wind back 90 days ago, has anything changed with respect to your underlying assumptions between the different cohorts, so between the core business and the sort of largest customers versus 90 days ago? Or is this outlook just sort of a reflection of that sort of minimum commitment methodology that you're applying in Q4? Just want to get a sense of has anything changed with respect to the outlook...

**David Obstler** (Executives):
Yes, there are a couple -- yes, thank you, Sanjit. There are a couple of things to talk about. First of all, I think we said versus our largest customer that they renewed and they were spending above the minimum commit, and that happened in Q3. We said that in our guidance, we were going to only include the minimum commit despite the fact that in Q3, they were spending above the minimum commit. The -- as we've talked about, we've accelerated in Q3, excluding the largest customer. 
So I would say the only thing that has changed was in sort of Q3, we did some renewals extensions with some large and large AI customers where as normal, we essentially extend and increase the commit, but do better pricing for that. And that happened in a number of large customers. It's a normal behavior, and that's really the only thing that changed since our last communication. Oli, do you want to add anything?

**Olivier Pomel** (Executives):
Yes. There's a few -- we discussed on the call, I could bring up a few of those large customers where we saw renewals way earlier than we thought we would. There's another one that happened in October that we're not discussing. So these are all good news, but they do create like headwind into the short term into the revenue, and that's one change from last quarter. Other than that, like everything has played out pretty much the way we were expecting with some happy surprises increasing, in particular, the continued acceleration of the non-AI customer, which has been very good overall.

**Sanjit Singh** (Analysts):
Understood. And if we think about the ex-AI native customer growth, that's been on an accelerating trend for several quarters now. As we think about this core non-AI native business, you obviously have a lot of tailwinds on the AI portfolio. It seems like the $100,000 customer quarter is more of the AI product. Do you feel that, that can continue to drive sort of sustained trajectory? Or are we -- after multiple quarters of acceleration, do you sort of see a leveling off in that ex-AI native cohort?

**Olivier Pomel** (Executives):
I mean, look, in the [indiscernible] that all of these customers are adopting AI and they are continuing more cloud and they're building more software and they are changing the way they work. So we expect a long period of growth for these customers. Now with the overall growth rate is, does it keep going up a lot, does it stay stable? It's a very high growth rate already, and we feel pretty good about it. It's hard to tell where it's going to go. But we're very confident in the broader trend that is underpinning that.

**Operator** (Operator):
Next question will come from the line of Gabriela Borges from Goldman Sachs.

**Gabriela Borges** (Analysts):
David, I want to stay on this point on the AI native cohort because I think you've been very transparent in how you talk about your largest customers versus the rest of the cohort. And my question for you is you have these funky sequentials because you have had this incredible growth rate in this cohort over the last 12 months. And now you've got this renewal dynamic with your largest customer, you're also talking about the renewal dynamics on the early renewals. 
So my question for you is, what can you tell us about how to think about modeling the sequentials in this business? Is it that we get through the next, call it, 2 quarters and then we're back to steady state? Is it that maybe we see another step function down every year in the sequential because you have this early renewal dynamic, which again, is a really good place to be because you're getting these really large deals but the only way you get better pricing is because the dollar volume is going up. So maybe just the puts and takes to how we think about the sequentials for the AI native cohort and when we will be back to something that looks like normal, which I get is a tricky definition of the word normal anyway.

**David Obstler** (Executives):
Yes. So good question. So in terms of the largest customer, I think as we said, the customer renewed -- the customer -- we decided to put only the commitment, the minimum commitment. So the customer in Q3 spent substantially above the minimum commitment. So one thing that is very important in the sequentials is what happens there. We don't control that. The customer can't go below the minimum commitment, but can be various degrees above the minimum commitment. So that is one factor that we -- so essentially, one thing that will create less of a sequential guidance or actual would be that, that number stabilizes and isn't running above the minimum commitment. So that's one.

**Olivier Pomel** (Executives):
I would say and I will broaden it, I mean, the point here is there's one part that is very usual, which is that we have all these customers that are expanding and they're growing and they're renewing. And then when they renew, they get better deals and they also adjust their traffic over time with an underpinning of growth, which is what we've seen since the beginning of the company. There's something that is new that we have, some of these companies are scaling incredibly fast to a level that we've never seen in the industry or any industry really before, which creates new dynamics. 
This is why we can be a bit surprised when we see customers renew early just a few quarters into there -- starting to add up the product. In general, though, we're getting a larger number of these customers like the AI native cohort is broadening. We have many more customers, many more large customers into that cohort. We called out a few wins that we landed another AI lab, for example, this quarter that's in the note. 
So we -- the long term, this is going to broaden. This is going to represent a much larger fraction of our customer base. And as a result, there will be more stability over time. I still don't think it's a very unstable business. I mean we're talking about a change of a few percentage quarter-to-quarter in terms of where we end up versus where we think we're going to be. But we think at the end of the day, this is a usage-based model, and we get more visibility into the mid- to long term than we do into the very short term.

**David Obstler** (Executives):
I do want to remind everybody that all things being equal, the sequential between Q3 and Q4 tends to be less because of the late December effect when our usage-based products and vacations, so -- and some code freezes. So that can be transparent based on the other factors or it might be underneath of that, but we do have that effect in Q4, which we don't have in the other quarters.

**Operator** (Operator):
Our next question will come from the line of Raimo Lenschow from Barclays.

**Raimo Lenschow** (Analysts):
Can I stay on one last time -- one last question on this one. So if I think about the customers renewed early. So they get better pricing. But obviously, the volume is going -- kind of going crazy there, but it kind of creates a short-term headwind because the same volume is now on a lower price, but then the volume grows and from then on in a couple of quarters, we should see like the normal progression. Is that kind of the right thing to think about? I think we have that in the past, but I just wanted to clarify that. And then I have one follow-up.

**Olivier Pomel** (Executives):
Yes, that's broadly what happened. There's a few other things that typically happen in those situations, which is they try to understand what is that going to need. So they look at what they're using and they think, okay, this part, maybe we don't need that much of -- this part, we're probably more of or maybe in some situations, we tell them, hey, maybe you should use this different tier of retention for this type of data because of the way you're using it. 
So there's a bit of account optimization there when we work with them. But the -- that this is on the background of growth. These customers are growing and they're deploying much larger workloads, and they're looking at doubling, tripling, [ quadrupling ] their footprint with us over time, and this is basically we're working on with them.

**Raimo Lenschow** (Analysts):
Okay. Perfect. And then the main question for me was on the ex-AI part, like historically, we would think about that growth coming from cloud migration, people modernize and doing more stuff. You mentioned another aspect, which is kind of because of AI, et cetera, we can code more, there's more application modernization, all these stuff happening. So is this kind of changing the way it's kind of evolving for you from classically with people modernize, you have to go to Datadog. Thank you very much. Well, now actually the companies are working differently, and that's also starting to drive the [ ex-AI ] business. Can you speak to that, please?

**Olivier Pomel** (Executives):
Yes. I mean -- well, the one thing I didn't mention on the call, that's always true. We also do more things for our customers. We have consolidated a lot of what they were using. We have more products to cover more of the surface area. As it comes to customers building more with AI, like it also brings some of our other products more into the front and center. So one example is customers are building a lot more software. So they're putting a lot more pressure on their CI and deployment and testing. And so they're trying also to adopt more of our CI products. I think we called out a few wins around that too in the call. So that opens the door for more products beyond core observability for us.

**Operator** (Operator):
Our next question will come from the line of Samik Chatterjee from JPMorgan.

**Samik Chatterjee** (Analysts):
I had a couple. Maybe for the first one, I know you mentioned your largest customer did spend above their commit in Q3. Is there any way to tell us how much of the beat relative to your guidance in Q3 was because of the large customer spending above the commit relative to the rest of the business, right? Depending on how you forecasted them in Q3? And I have a quick follow-up.

**David Obstler** (Executives):
Yes. We're not answering -- we're not being specific, but it is true. It just -- it is true that if you're basically guiding like in below there -- we said we'd be conservative. In Q3, we said conservative relative to what they were spending. And in Q4, we've been explicit and said minimum commitment. It is true that if they spend more than that, that would be implicit beat mathematically, yes, yes.

**Olivier Pomel** (Executives):
Again, we didn't change the assumption there over time. So we get everything unchanged. I think the one difference -- we brought up earlier, the one difference since the last quarter is some positive trends on the overall customer growth, but also some early renewals of larger customers, which includes some other AI customers. That's the one thing we should remember as being the difference.

**Samik Chatterjee** (Analysts):
Yes, sure. And for my follow-up, I mean, the contribution of revenue from new customers continues to ramp up steadily. Can you just talk about sort of what is the average land size that you're seeing now with new customers and how that's changed? And what sort of behavior you're seeing on that front? How you're thinking about it as you sort of move into next year in terms of how much new customers contribute to your overall growth?

**David Obstler** (Executives):
We haven't provided guidance on -- we said over time, we've seen an increase of average land size due to the increase of the platform and as we give the metrics on the adoption of products, the adoption of more parts of the platform. Oli, do you want to...

**Olivier Pomel** (Executives):
Yes. I think -- look, this is something we see in the customer base that we see that one is -- one, with the new and the AI native companies, some of them start with more scale earlier, like we've discussed it before, but we see companies scaling faster than used to. So they have -- they represent more of the revenue faster. But we also are developing new segments and landing large customers from day 1. 
So we called out a few on the script today. We mentioned, I think, a defense agency in the U.S. government. We mentioned Japanese banks, like 2 of the 3 largest Japanese banks in the same quarters. Those are all sizable low land deals. And if you compare the business to what it was, say, 5 years ago, like this is definitely a new side of business that we didn't necessarily have before. And by the way, those wins I mentioned, they don't even register into the revenue yet because these are lands but these are not customers that have ramped usage yet. So...

**Operator** (Operator):
Our next question comes from the line of Matt Hedberg from RBC.

**Matthew Hedberg** (Analysts):
I wanted to start with training. You noted in your script, you had an 8-figure, I think, annualized expansion with an AI division of a large software company. It sounds like they're using you guys for AI training workloads. I guess this is -- to us, it seems like a really interesting growth opportunity. Can you step back and kind of talk about what that training opportunity is? And what could it mean for your growth?

**Olivier Pomel** (Executives):
I mean it's been evolving positively. If you look a year or 2 years ago, basically nobody was doing training. It was only a few frontier labs who were doing their own training and nobody else was. Now we see an order of magnitude more large-ish labs or new labs that are doing training at a large scale. And then there's another whole category of companies below that, that are starting to do their own, including us. We started doing training at a pretty decent scale, and we showed some of the results, we showed some of the results on the call as well. 
So I think there's some interesting potential development there where training becomes a part of everybody's business and everybody's customizing model in building their own. And so we are investing. I would say it's still early to call it as a mass market. Right now, we see some interesting indications of it. We also see that we can be extremely useful to some very large customers. But I think we still have to invest. We have to build. We have to see how that market develops.

**Matthew Hedberg** (Analysts):
Got it. And actually, David, if I could just have one more follow-up. On your largest customer, you used the word substantially above their minimums, which I find interesting. And I know you're assuming only the minimums for 4Q, but philosophically, looking at this customer and their recent consumption patterns, does this perhaps change your opinion about how they might use Datadog longer term, maybe new use cases above and beyond what they're using today that could make that growth opportunity really interesting for this customer?

**David Obstler** (Executives):
I think that's true for any customer that there are many different use cases. For that, in particular, we -- as we've said all along for many quarters, we don't control. We have the contract, the renewal, and we're not in the business of projecting that. But it is true from -- across our customer base that there are many use cases in a company, whether it be division and end user, et cetera. Oli, you want to...

**Operator** (Operator):
Our next question will come from the line of Karl Keirstead from UBS.

**Karl Keirstead** (Analysts):
Okay. Great. Maybe, Olivier, for you. You mentioned in your comments that a lot of customers are grappling with higher token costs, higher AI spend and are trying to get it under control. I'm just wondering, based on all your customer interactions, how enterprise spending behavior is changing in light of the fact that they're trying to get their token costs under control. And to the extent that any of the customers that early renewed to try to get price discounts were not AI natives. They were traditional enterprises. Do you think that might be because they're trying to grapple with budget pressure?

**Olivier Pomel** (Executives):
Yes. So I think, look, this is a very widespread problem. I think what we've seen is there's been an explosion of adoption of AI, in particular, coding agents. And that was not planned largely. A year ago, nobody had the amount they spend in their budget on AI. So they really had to try and figure out [ what ] that works and what part of that they actually need and what they get from that. So there's a strong need for tooling, which is something we provide. 
It's a great opportunity for us, and we see great growth and adoption of our Cloud Cost Management products on that or Agent Console that is our products that -- now in terms of the early renewals that we see, they're not directly related to that. I think they come from large customers that are either AI labs or that are focused on -- that are tech companies in general, I would say. And they -- and that doesn't really have anything to do with their own -- they think something has more to do with their own growth as a business.

**Operator** (Operator):
Next question will come from the line of Fatima Boolani from Citi.

**Joel Omino** (Analysts):
This is Joel on for Fatima. I'll maybe just ask 2 real quick. So firstly, just on margins and operating and gross income leverage, maybe for you, David. Strong results this quarter, at least relative to our expectations, but we do know there's also certain areas that you are investing fairly heavily in. So just curious what some of the drivers of the performance were specifically this quarter? And then what your updated or what your latest investment posture is? And then just the quick second question, I'll just throw it in now is any data points on Bits AI penetration specifically in the customer base?

**Olivier Pomel** (Executives):
Do you want to go on margins first?

**David Obstler** (Executives):
Yes, I'll go with margins first, yes. Yes, it's very similar to what we said. We are investing aggressively in the go-to-market, we continue to have white space uncovered, both from a geographical or an end market, for instance, Fed. And we are continuing to be successful in scaling our quota capacity and you see that in the growth. 
In addition, we're continuing to invest in R&D. In this case, it's a combination of AI, of investments in a combination of AI and people. We see lots of opportunities. I think Oli will now go -- talk about the products, but we continue to see a lot of opportunity for us to get market share, get platform penetration and increase our feet on the street or on a global basis. Want to go over the Bits?

**Olivier Pomel** (Executives):
Yes. And on Bits, I think we've mentioned on the call, we see amazing adoption of it, like this is -- when you look at the number of individual customers or users that are using it, this has been the strongest launch we've ever had as a product. So we feel very good about it. We've also revamped the way we package it over the past quarter. So we used to charge specifically for investigations. 
Now we have a model of AI credits that cover a whole different set of use cases that involve Bits as our agent and we've seen great results. Thanks to that. So it's super encouraging. I would say it's still early because there's still so much that we were building into this. So many things our customers want us to do for them, so many opportunities to automate their workflows. But we are -- we feel very, very good about the current status.

**David Obstler** (Executives):
Let me just circle back on one thing. I think I neglected to go over gross margin, as you mentioned. I think it's very similar to what we said before that through a combination of the penetration of our platform as well as our engineering, we have been plus or minus in this 80% range. I think you see in this quarter, we ended up around 81%. And so this is common practice for us. We invest, optimize, do engineering projects and what was communicating gross margin indicates stability there, which we've evidenced in previous quarters.

**Operator** (Operator):
Our next question will come from the line of Kirk Materne from Evercore ISI.

**S. Kirk Materne** (Analysts):
I guess, David, on -- or Oli, on this native AI cohort that's renewing a little bit early. Obviously, they're coming back because they're spending so much with you all and obviously want to get better economics. I'm just curious, what's the sort of attach rate on some of those newer renewals? When they come back and renew early, do you still have time to sort of cross-sell them some of the other products? I guess what are you seeing in that dynamic? I realize it creates some near-term headwinds from a revenue perspective, but it would also, I think, open up the opportunity to have a discussion about you expanding their usage across multiple products.

**Olivier Pomel** (Executives):
Yes. I mean, look, if you look at these cohorts, and if you compare them in particular to the non-native cohorts we might have had like 5 or 6 years ago, like these are adopting many more products. So we see much broader product adoption and platform adoption with those customers than we saw 5, 6 years ago. So that's definitely something that is happening. Some of that is happening at renewal time, sometimes just happening organically as new needs emerge and all we spread to more teams inside those companies.

**David Obstler** (Executives):
But I think it's important to clarify, these are renewals, but they are at higher levels than their previous commit, which is how they're getting the volume discounts. But we are renewing these customers at higher commits.

**S. Kirk Materne** (Analysts):
Okay. And David, I guess just for you, I mean, this would seem this cohort coming up for renewal earlier is all good over the long term. I'd imagine just visibility is a little bit harder from a sequential perspective. Is that sort of -- to Oli's comments on the long term, I'd imagine it's all good from a longer-term perspective, but it just creates a little more volatility for you on a sort of quarter out guidance perspective. Is that fair?

**David Obstler** (Executives):
I would say it has a small amount of variation in the timing of the revenue path of these customers. The sequential here was really 3 things. It was really, one, that factor. Two, I think we mentioned the largest customer in the guide, which we're not predicting what they're going to do. And three, is we know about the small amount of seasonality. So it's one of the factors. We try to get a good sense of that. But of course, as our RPO and as our contract, as we extend, it does create some volatility around the edges in the sequential nature.

**Olivier Pomel** (Executives):
But again, it's all good news. Look, we are a usage-based model and when we deal with fast-growth customers, these customers themselves don't know exactly how they're going to grow over the next few months and what part of their business and how their consumption is going to change. So we happily work with them and make sure that we support their growth and we do everything that's right. The only time we think about it in difficult terms is when we prepare for these calls, we have to figure out, okay, so what part can we communicate, what part do we know, what part do we not know. But overall, these are all great news, great customers, great growth, a great adoption, amazing trends that are underpinning the industry as a whole. So we feel very good about it.

**David Obstler** (Executives):
Yes. And this is similar to what we -- in the company's existence that you talked about. I mean our motion is to increase the commitment of customers, broaden the platform and extend the contract. So that's what we do all the time. It has some variability, but it's very similar to what we've been doing in the company throughout its history, and it's a good thing.

**Operator** (Operator):
And our next question will come from the line of Peter Weed from Bernstein Research.

**Peter Weed** (Analysts):
You talked about it a little bit, but it's really exciting to hear about the release of the Bits AI, Scout and the strong early adoption. Could you help enumerate that a little bit? And maybe remind us how the pricing works there? Is it kind of directly monetized? Or does it really drive the adoption or use of Bits AI overall? It would be really exciting to kind of appreciate how broad this AI adoption is now and how it might move the needle on overall growth and perhaps become another major pillar for the business.

**Olivier Pomel** (Executives):
Yes. So it's actually a bit of both. So look, it largely sits on the -- all of the data we acquire and the way we can process it and all the various products we have. So that's the core. But we also have a model where we charge for AI creative specifically for what Bits does on top of that. And the model we've chosen is a model where we stay fairly close to inference costs there so that we can pass on the savings as the models become more efficient to our customers, and so we can run many more investigations. 
And the reason we've done that is the field is changing so fast, and we're improving the efficiency of those models so fast that it's not very productive to have a fixed price on say everything you do as you expect the volume of things you do to increase by orders of magnitude while the price goes down by orders of magnitude as well. 
And so we are working on that model for that, which works really well. So long term, we expect both to monetize Bit directly as we do today and to drive broader adoption of the platform and deliver more value to our customers. In terms of what becomes the dominant monetization, it's hard to tell, and we don't really care. Again, we're fully usage-based. So as long as we get more usage, deliver more value, we'll be fine.

**Operator** (Operator):
Our next question will come from the line of Koji Ikeda from Bank of America.

**Koji Ikeda** (Analysts):
I wanted to ask a question on Infrastructure Monitoring. So you guys disclosed it's now exceeding $2 billion in ARR and growing in the mid-30s. Could you quantify how different that growth rate is from when you last disclosed the scale of this business at $1.5 billion earlier this year. How much of that growth is coming from AI infrastructure? And how sustainable is that growth rate as GPU efficiency improves?

**Olivier Pomel** (Executives):
So -- I mean, look, we've seen an acceleration of the business in general. And not just thanks to AI native, but also thanks to the rest of the customer base, so we have mentioned that, and that applies to Infrastructure Monitoring also. Today, that growth is not actually related directly to GPUs. GPUs are still largely on -- we see them for our customers on training. We have products there, but we don't monetize those products widely yet. And so for us, that's an opportunity we have in front of us. That's not something that's baked into the current growth and the current numbers.

**Operator** (Operator):
Our next question will come from the line of Patrick Colville from Scotiabank.

**Patrick Edwin Colville** (Analysts):
To me, one of the most interesting points in the prepared remarks is about Datadog training, your own frontier models. And then Olivier, your comments around this behavior is not mass market, but seeing how the market develops. I guess I want to ask you because you're at the forefront of how things are changing. How does this affect Datadog's use of proprietary tokens internally or for customers versus open weight tokens? And then I guess, David, if this shift that Olivier is describing picks up steam, what might that mean for Datadog profitability that it nicely increased this quarter, but is there a potential that this might help the bottom line as well?

**Olivier Pomel** (Executives):
So look, what we see internally and what we see with customers is -- there's a mix of models that are being used. So I mean I can say we include both customers and us into that collective we because the behaviors are fairly similar. We are big consumers of the top labs, top models, but we also consume open weight models, a growing amount of open weight models, and we train our own, post-train our own.
And I think it's probably representative of where the industry as a whole is going. We do that because there are certain things you can only get from the top-of-the-line models that are being generally trained by others. And there's a number of things that are good enough and very cost efficient with open weight models, you can just pick up and run. And there's finally a number of other things that you can make way more efficient with your own data, your own workflow and your own post-training, which is what we've done with some of the models we announced. 
So I expect that mix to remain about the same. In terms of the impact on margin, look, at the end of the day, you get some control on what you spend your money on. If it's very proprietary to you and you can deliver superior economy, you should absolutely do so. If not, like if it's very undifferentiated and applies broadly in some parts of your business that are the same to millions of other businesses, then it's fine probably to use off-the-shelf models and keep consuming those.

**Operator** (Operator):
Our next question will come from the line of Alex Zukin from Wolfe Research.

**Aleksandr Zukin** (Analysts):
Oli, maybe a quick one for you and David, a follow-up. Just to what extent are you seeing the demand for Agent Observability from both AI natives and the core driving demand for offerings like your Traces product? And what is the -- like what has changed here longer term just given the kind of elevated adoption levels? And maybe also any comments on cybersecurity and the plans there?

**Olivier Pomel** (Executives):
Yes. So we see growing demand for Agent Observability. And what -- so there was always interesting demand from the AI natives et cetera. But what's most interesting here is the non-AI natives are consuming more and more. And -- because they're getting deeper into AI, we see real demand, real volumes and really exciting -- really exciting pipeline for products actually. So we think that this is not crossing the chasm, so to speak, and that's exciting for this product, even though we didn't mention any hard numbers today on that. 
On cybersecurity, look, there's so many new opportunities with AI. We're very happy to see that we can land the full platform with large customers. We mentioned that for a defense agency. We mentioned that also for a couple of other wins when we landed not just observability, but our security platform at the same time. So we feel good about the market fit there, and we feel good about the way the whole retooling and rebuild that is taking place with AI is playing in our favor.

**Aleksandr Zukin** (Analysts):
Perfect. And David, maybe for you, just a clarification. If we think about -- first of all, it's great to hear about the renewal with your largest customer. And I think we totally understand the guiding for the minimum for Q4. Any pearls of wisdom on how to think about modeling that for '27? Because presumably, that's a 1-year contract. And should -- is that something we should think about kind of maintaining at some level? 
Is that something that you guys are going to take out of the model? And then if I think about how you're guiding with respect to some of those other early renewals for the AI natives that got renewed, are those also at the minimum commitment level? Are those slightly above? Just any help on those 2 items, I think, would be helpful for.

**David Obstler** (Executives):
Yes, reminding everybody -- yes, yes, sorry -- yes, on the -- we'll give guidance for 2027 on our year-end call. I think we've said in the last couple of quarters that we're guiding at whatever the contractual minimums, and we've repeated that this quarter. We'll give some more flavor on that when we do '27. 
And in terms of the rest of the business, what we've been -- what we do is, and we've said this over the many years, is we take the growth rate of those customers and we discount that. So that would be how we apply it across the customer base in taking the most recent organic growth and then discount it. And we would certainly be doing that for both the early renewal customers and our broader customer base.

**Olivier Pomel** (Executives):
All right. And I think that's it for our questions today. So thank you all for listening. I also want to thank everybody at Datadog for a great Q3. I know we are right in the middle of an even greater Q4. We're all very, very busy. We're meeting -- I'm going to meet a lot of our customers at the largest AWS conference in a few weeks. And we hope to have many more exciting product announcement to share soon. So thank you very much all, and see you next quarter.

**Operator** (Operator):
Thank you for your participation in today's conference. This does conclude the program. You may now disconnect. Everyone, have a great day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DDOG_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：Q3 營收財測 11.35–11.45 億美元，年增 28–29%（原話："to be in the range of $1.135 billion to $1.145 billion"）
- 2026-08-06｜CFO｜guidance：全年營收財測 44.5–44.7 億美元，年增約 30%（原話："to be in the range of $4.45 billion to $4.47 billion"）
- 2026-08-06｜CFO｜margin：全年 non-GAAP 營業利益財測 10.1–10.3 億美元，營業利益率約 23%（原話："which implies an operating margin of 23%"）
- 2026-08-06｜CFO｜guidance：最大客戶用量下降，已納入 Q3 與全年財測（原話："we have seen a usage reduction,"）
- 2026-08-06｜CEO｜customer：CEO 披露與領先 AI 公司簽 9 位數續約，但 Q3 起用量下降（原話："albeit with a user reduction starting in Q3"）
- 2026-08-06｜CEO｜guidance：管理層說明對最大客戶採完全去風險的財測處理方式（原話："fully derisk the guidance for the rest of the year"）
- 2026-08-06｜CEO｜guidance：CEO 說明這次對最大客戶的權重與平常不同，其餘保守度不變（原話："we also weighted this one"）
- 2026-08-06｜CFO｜guidance：CFO 稱財測方法論不變，以近幾個月趨勢為基礎並隱含保守（原話："we base our guidance on trends observed in recent months"）
- 2026-08-06｜CEO｜customer：CEO 稱剔除最大客戶後成長率與其餘業務相同，其餘業務已連續 5 季加速（原話："5 quarters of continuous acceleration"）
- 2026-08-06｜CEO｜customer：非 AI 客戶營收成長加速至高 20% 區間，前季為 20% 中段，去年同期 18%（原話："to the high 20s percent year-over-"）
- 2026-08-06｜CFO｜customer：Q2 營收 11.2 億美元年增 36%，單季新增營收 1.15 億美元為紀錄（原話："added of $115 million is a record by a significant margin"）
- 2026-08-06｜CFO｜margin：毛利率 79.6%，前季 80.2%、去年同期 80.9%，管理層稱預期不變（原話："There's no change in our expectations for"）
- 2026-08-06｜CFO｜margin：Q2 營業費用年增 26%，DASH 大會成本約 1,500 萬美元（原話："the event cost about $15 million"）
- 2026-08-06｜CFO｜margin：Q2 自由現金流 2.79 億美元，利潤率 25%（原話："$279 million for a free cash flow margin of 25%"）
- 2026-08-06｜CFO｜capital_allocation：全年資本支出加資本化軟體占營收 4–5%；現金部位 50 億美元（原話："in the 4% to 5% of revenue range in fiscal 2026"）
- 2026-08-06｜CEO｜capital_allocation：宣布收購 Adaptive ML 以加速 AI 研究，預計 6 月完成（原話："acquisitions of Adaptive ML, which will close"）
- 2026-08-06｜CFO｜customer：淨營收留存率低 120%，總營收留存中高 90%（原話："net revenue retention percentage was in the low 120s"）
- 2026-08-06｜CFO｜customer：新客戶貢獻的年增營收占比由 Q1 25% 升至 Q2 約 30%（原話："was about 30% in Q2, up from 25% in Q1"）
- 2026-08-06｜CFO｜customer：AI 客戶群 750 家，含 31 家年支出逾 100 萬美元、其中 8 家逾 1,000 萬美元，並納入超大規模雲端業者內部 AI 實驗室（原話："hyperscalers using Datadog for in-house AI labs"）
- 2026-08-06｜CFO｜customer：CFO 稱 RPO 與帳單不如營收能反映業務趨勢；RPO 34.7 億美元年增 43%（原話："revenue is a better indication of our business trends"）
- 2026-08-06｜CFO｜customer：客戶總數約 33,400，新增客戶數被分析師指為歷來最弱；CFO 稱毛新增穩定，差異來自免費與合約邊界的低端（原話："customer additions continue to be strong and on trend line"）
- 2026-08-06｜CEO｜product：RUM 年化營收超過 2 億美元，成長加速至逾 50%（原話："now exceeds $200 million in ARR"）
- 2026-08-06｜CEO｜product：多產品採用率上升：使用 4 款以上產品的客戶 58%，去年同期 52%（原話："58% of our customers now use 4 or more products"）
- 2026-08-06｜CEO｜product：Bits AI 擴大接觸面，並改採 AI credits 新計價包裝模式（原話："we have a new model with AI credits that we're rolling"）
- 2026-08-06｜CEO｜product：Infinite Cardinality Metrics 以不同的指標包裝方式解決基數導致帳單不可預測的問題，仍屬早期（原話："by packaging our metrics a little bit differently"）
- 2026-08-06｜CEO｜product：MCP 工具呼叫次數季增四倍，較 2025 Q4 成長逾 22 倍（原話："MCP tool calls quadrupling again quarter-over-quarter"）
- 2026-08-06｜CEO｜product：將 Bits Security Analyst 從自家 SIEM 分離，可搭配其他 SIEM，朝 AI SOC 方向（原話："separated the agent from our SIEM"）
- 2026-08-06｜CEO｜competition：資安產品需整合重做，CEO 稱整合式平台符合其做法（原話："So it's a complete rebuild for most of the industry."）
- 2026-08-06｜CEO｜competition：Fortune 100 健保客戶案，管理層稱 HIPAA 合規與 PII 處理使其勝出競爭方案（原話："differentiate and win over competitive solutions."）
- 2026-08-06｜CEO｜customer：逾 3,000 萬美元 TCV 的多年約，取代 4 套商業與內部工具，含迄今最大 BYOC 案（原話："displacing 4 commercial and internal tools"）
- 2026-08-06｜CEO｜risk：客戶關注點由驗證正確性轉向 AI 成本控制；分析師提出 CFO 對 Datadog 帳單的抱怨（原話："the focus has moved quite a bit towards cost."）
- 2026-08-06｜CEO｜risk：分析師問 Bits AI 自動化是否減少消耗量；CEO 稱不是零和（原話："it's not a zero-sum game."）
- 2026-08-06｜CEO｜commitment：管理層稱持續投資研發與業務團隊，因尚未達理想的涵蓋規模（原話："still not at the scale we want to be"）
- 2026-08-06｜CFO｜commitment：管理層稱非 AI 成長可持續，並將部分成長歸因於擴編業務配額（原話："We've successfully expanded quota capacity, the"）

### DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md
- 2026-02-12｜David Obstler (CFO)｜guidance：毛利率規劃維持在正負 80% 左右，並保留彈性投資平台、資料中心與產品（原話："planning our gross margins plus or minus 80%"）
- 2026-02-12｜David Obstler (CFO)｜commitment：重申長期營業利益率目標 25% 以上，並稱與上一次投資人日所說相同（原話："long-term target of an operating margin at 25% plus"）
- 2026-02-12｜David Obstler (CFO)｜margin：R&D 占營收比重的目標約 30%，並稱有波動（原話："this has been our target around 30%"）
- 2026-02-12｜David Obstler (CFO)｜margin：稱 AI 的使用可能成為 R&D 占比的槓桿之一，未量化（原話："some things about the use of AI that might be levers here"）
- 2026-02-12｜David Obstler (CFO)｜margin：銷售與行銷費用占營收比重，原文下一行接「roughly the mid-20s range」（原話："keep that sales and marketing as a percentage of revenues"）
- 2026-02-12｜David Obstler (CFO)｜margin：G&A 占營收約 5%（原話："Thank you for all the hard work you do there at around 5%"）
- 2026-02-12｜David Obstler (CFO)｜margin：去年 non-GAAP 營業利益率 22%；前一句稱現金流利潤率 27%（原話："So, it's all non-GAAP, and it was 22%"）
- 2026-02-12｜David Obstler (CFO)｜margin：解釋營業利益率有波動：消費型模式的變動快過招聘速度（原話："that changes faster than we can hire people"）
- 2026-02-12｜Unknown Executive｜margin：答覆 $10M 客戶與 $10 萬客戶的獲利結構差異時，改談加權平均後毛利率大致不變（原話："maintain our margins the same at the gross"）
- 2026-02-12｜David Obstler (CFO)｜capital_allocation：淨股數稀釋目標為 2.5% 至 3%（原話："our target in net share dilution, which is 2.5% to 3%"）
- 2026-02-12｜David Obstler (CFO)｜capital_allocation：併購策略強調審慎，過去聚焦補技術能力（前後文提到 Eppo、Metaplane）（原話："a thoughtful and disciplined acquisition strategy"）
- 2026-02-12｜Olivier Pomel (CEO)｜capital_allocation：長期以約 30% 營收投入 R&D，2025 年超過 $10 億、約 4,000 名工程師（原話："we've invested about 30% of revenues into R&D"）
- 2026-02-12｜Sean Walters (CRO)｜capital_allocation：宣布開始試行資安專屬銷售團隊（原話："we decided to start a pilot of security-focused sales teams"）
- 2026-02-12｜Adam Blitzer (COO)｜competition：稱 R&D 支出約為最接近同業的 3 倍（原話："about 3x the R&D spend of our next closest peer"）
- 2026-02-12｜Sean Walters (CRO)｜competition：稱資安市場的競爭對手正在整併（原話："competitors in this space consolidating"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：承認事後排查類需求用 Claude Code 這類工具也能得到不錯結果（逐字稿拼作 Cloud Code）（原話："you can get a pretty good result if you ask Cloud Code"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱預防性、主動式場景無法靠通用 coding agent 完成，因資料不會流經它們（原話："that just doesn't work at all because the data doesn't flow"）
- 2026-02-12｜Michael Whetten｜competition：回應通用 LLM 的程式碼資安能力：稱自家優勢是看得到程式碼在正式環境的部署狀況（原話："we can see how that code is deployed in production"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱 coding agent 會持續存在且做更多，公司定位是補充而非取代（原話："the agents are here to stay and they're going to do more"）
- 2026-02-12｜Alexis Le-Quoc (CTO)｜competition：被問進入門檻時，承認小模型沒有明確的資金門檻，護城河放在資料品質（原話："don't think there's a clear financial barrier of entry"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：回應 OpenTelemetry：稱資料收集從來不是護城河（原話："The collection has never been the moat"）
- 2026-02-12｜Adam Blitzer (COO)｜competition：自我定位為觀測市場中的高價位產品（原話："Datadog is a premium product"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱觀測市場占有率仍只在十幾個百分點中段（原話："our market share is still only in the mid-teens"）
- 2026-02-12｜David Obstler (CFO)｜competition：觀測市場規模 $300 億以上；擴大到資安、軟體交付等後 TAM 稱超過 $1,000 億（原話："a $30 billion-plus market"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：基礎設施監控 ARR 達 $16 億，日誌與 APM 各超過 $10 億（原話："$1.6 billion of ARR in infrastructure monitoring"）
- 2026-02-12｜Tim Knudsen｜product：資安產品 ARR 已超過 $1 億（原話："we've now surpassed $100 million in ARR"）
- 2026-02-12｜Tim Knudsen｜product：百萬美元客戶中 70% 用至少一項資安產品，但資安只占其 Datadog 支出 2%（原話："together is only 2% of their Datadog spend"）
- 2026-02-12｜Yrieix Garnier｜product：Flex Logs 的 ARR 接近 $1 億且快速成長（原話："approaching $100 million ARR and growing very rapidly"）
- 2026-02-12｜Yrieix Garnier｜product：BYOC（自帶雲）已有大型公司在預覽，並預期打開更多機會（原話："engaged with very large companies and previewing BYOC"）
- 2026-02-12｜Yanbing Li (CPO)｜product：Bits AI SRE 一月單月就有超過 2,000 家客戶跑調查（原話："more than 2,000 customers run investigation with Bits AI"）
- 2026-02-12｜Yuka Broderick｜product：Bits AI SRE 公開定價為每 20 次調查 $500（原話："Bits AI SRE $500 per 20 investigations"）
- 2026-02-12｜Yanbing Li (CPO)｜product：MCP server 自推出後用量呈指數式成長（原話："we've seen also exponential adoption and growth"）
- 2026-02-12｜David Obstler (CFO)｜product：LLM Observability 的 span 量一年增加 10 倍（原話："the last year, that has increased 10x"）
- 2026-02-12｜Alexis Le-Quoc (CTO)｜product：訓練時序模型 Toto 2025 年花費約 $75 萬（原話："We spent about $750,000 to train this"）
- 2026-02-12｜David Obstler (CFO)｜product：數位體驗監控（DEM）已大到公司也稱之為第四支柱（原話："we are also calling that a fourth pillar"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：承認對功能旗標與實驗平台的看法改變（過去視為商品化）（原話："we've changed our minds quite a bit on the topic"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：資料可觀測性過去被視為周邊市場，現在升到優先清單前列（原話："We thought also this was an interesting market"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：被問自主營運何時到來，稱無法判斷是一年或三年（原話："hard to tell whether we get there in a year or in 3 years"）
- 2026-02-12｜Unknown Executive｜product：被問自主營運的計價模式時，稱距離談定價還太遠（原話："too far away to be talking about pricing models"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：預期今年會有相當多公司把 AI 寫程式的轉換推進（原話："I would expect quite a bit of that to happen this year"）
- 2026-02-12｜Unknown Executive｜guidance：把財測保守度歸因於用量計價模式（原話："some of the conservatism we put in guidance"）
- 2026-02-12｜Unknown Executive｜commitment：稱對中期走勢很有信心，短期用量則不確定（原話："we're very confident about where we'll be in the midterm"）
- 2026-02-12｜Sean Walters (CRO)｜commitment：銷售團隊剛開完年度啟動會，稱全面投入 AI 銷售並已訓練每位業務（原話："we are going all in on AI"）
- 2026-02-12｜Unknown Executive｜risk：承認短期用量走勢無法確知（原話："how the usage is going to trend in 1 month from now"）
- 2026-02-12｜Unknown Executive｜risk：承認客戶會定期做用量優化，有時是公司主動建議（原話："we do see optimization on a regular basis"）
- 2026-02-12｜Olivier Pomel (CEO)｜risk：稱多數公司仍處於 AI 寫程式轉換的早期（原話："most companies are still early in the transition there"）
- 2026-02-12｜David Obstler (CFO)｜customer：新增客戶貢獻每年 ARR 成長約四分之一（原話："about 1/4 of that ARR growth each"）
- 2026-02-12｜David Obstler (CFO)｜customer：ARR 成長其餘約四分之三來自既有客戶多用產品與交叉銷售（原話："the remaining approximately 3/4 comes from"）
- 2026-02-12｜David Obstler (CFO)｜customer：客戶數超過 32,000，占約 50 萬目標客戶的邏輯數僅 7%（原話："that's a penetration in logos of only 7%"）
- 2026-02-12｜David Obstler (CFO)｜customer：百萬美元客戶今年成長到超過 600 家（原話："our $1 million customers, which this year grew to over 600"）
- 2026-02-12｜David Obstler (CFO)｜customer：首度揭露年花費超過 $1,000 萬的客戶指標；逐字稿數字為「over 60% growth, and that's now 34%」，未給明確客戶數，原文口徑不清（原話："growing quite rapidly, over 60% growth, and that's now 34%"）
- 2026-02-12｜David Obstler (CFO)｜customer：AI 原生客戶去年底占營收約 11%（原話："at the end of last year was about 11% of revenues"）
- 2026-02-12｜Adam Blitzer (COO)｜customer：前 20 大 AI 原生公司中有 14 家用 Datadog，AI 原生客戶群超過 650 家（原話："14 of the top 20 AI native companies are using Datadog"）
- 2026-02-12｜David Obstler (CFO)｜customer：整體毛留存率 97% 以上（企業 98% 以上，中小與中型 96% 以上）（原話："retention percentage. It's 97% plus in the company"）
- 2026-02-12｜David Obstler (CFO)｜customer：只有約一半客戶同時使用三大支柱（原話："only about half of our customers use all three pillars"）
- 2026-02-12｜David Obstler (CFO)｜customer：三大支柱都用的客戶，花費是其他客戶的 15 倍（原話："In fact, they spend 15x more"）
- 2026-02-12｜David Obstler (CFO)｜customer：一半客戶用 4 項以上產品，用 10 項以上的僅 9%（原話："half of our customers have 4-plus products"）
- 2026-02-12｜Sean Walters (CRO)｜customer：Key accounts 業務第二年的目標從開會數轉向營收與成交（原話："goals are shifted much more to revenue and closing deals"）
- 2026-02-12｜Sean Walters (CRO)｜customer：Key accounts 2025 年有比預期快的成交，且正快速擴張（原話："wins that are already expanding very rapidly"）
- 2026-02-12｜Sean Walters (CRO)｜customer：財星 500 大客戶的花費中位數不到 $50 萬（原話："is still modest at less than $0.5 million per customer"）
- 2026-02-12｜Sean Walters (CRO)｜customer：拉美約占營收 5%，成長遠快於整體（原話："they're growing far faster than our overall revenue"）
- 2026-02-12｜Sean Walters (CRO)｜customer：只稱 2025 訂單表現「stellar」，未給金額（原話："shows our bookings by year, including a stellar 2025"）
- 2026-02-12｜Adam Blitzer (COO)｜customer：計價為用量基礎並有量、承諾、多產品、期限等折扣，稱客戶越成長曲線越彎（原話："We have volume-based pricing"）
- 2026-02-12｜Unknown Executive｜customer：解釋客戶 ARR 出現短期下滑：簽更長期承諾換折扣時可能暫時下降（原話："it might drop you temporarily from where you were"）
- 2026-02-12｜Unknown Executive｜customer：承認過去幾年偏重從既有大客戶擴張，較少花力氣從零開發新客戶（原話："bit victims of our own success"）

### 問答異常語氣（迴避／改口／保留）
- DDOG_Q2_2026_Earnings_Call_20260806.md｜問：Sanjit Singh：最大客戶新合約的期限是否相近？用量下降是單價降低還是流失／降級，且是否延續至全年？｜答法：CEO 稱不評論個別客戶、「there's not a lot more we can share」；CFO 只談財測方法，未回答合約期限與降量原因
- DDOG_Q2_2026_Earnings_Call_20260806.md｜問：Alex Zukin：最大客戶續約的期限、折扣費率卡或產品數是否讓合約更黏？｜答法：CFO 稱「I won't comment on this」，改談一般企業客戶的年約加承諾加用量模式；CEO 僅說續約「a lot of continuity」
- DDOG_Q2_2026_Earnings_Call_20260806.md｜問：Brad Reback：剔除最大客戶的季減後，核心財測是否會高 300–400 bp？｜答法：CEO 稱「I can't speculate」，改談剔除該客戶後成長率相同與整體加速，未給數字
- DDOG_Q2_2026_Earnings_Call_20260806.md｜問：KeyBanc：Q3 財測的季增幅低於過去 Q3 的指引水準，趨勢與假設為何？｜答法：CFO 回答重複財測方法論與保守原則及最大客戶下降，未提供具體假設數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Sanjit Singh (Morgan Stanley)：自主營運一年後、三年後長什麼樣？是否需要自己掌握軟體交付管線（build vs buy）？｜答法：Olivier Pomel 稱時程 'hard to tell whether we get there in a year or in 3 years'，未給具體里程碑；build vs buy 只點名功能旗標與資料可觀測性兩個已改變看法的領域，並稱 'a few other areas... I'm not going to tell you about it'
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Fatima Boolani (Citi)：自主營運商業化後，計價模式是否會根本改變（結果導向計價）？｜答法：回答 'too far away to be talking about pricing models'、'It doesn't mean we have a pricing packaging in mind just yet'，未給計價方向，改談用量計價較容易適應
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Fatima Boolani (Citi)：$1,000 萬客戶與 $10 萬客戶的增量獲利／單位經濟是否有實質差異？｜答法：Unknown Executive 只答量折扣與加權平均後毛利率大致不變，未直接拆解大客戶的獲利結構差異
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Andrew Sherman (TD Cowen)：三大支柱使用率 53% 通常缺哪一塊產品？未來幾年會到多少？｜答法：Sean Walters 稱每個客戶情境不同、不強推三支柱，Yuka Broderick 補 'I wouldn't think of it as one particular pillar that's missing'；兩人都沒給未來使用率數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Keith Bachman (BMO)：資安產品組合的邊界在哪、哪些領域不打？｜答法：Tim Knudsen 談既有成熟預算與統一平台優勢、AI 帶來新領域，未指出任何不打的領域
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Ittai Kidron (Oppenheimer)：小模型成本只要 $75 萬，第三方進入門檻多高？AI 對公司業務的風險是什麼？｜答法：Alexis Le-Quoc 談資料與評測集的護城河、並承認沒有明確的資金門檻；Olivier Pomel 補 R&D 投入金額；兩人都沒列出 AI 對業務的具體風險
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Koji Ikeda (BofA)：財星 500 大客戶如何把花費中位數拉高？2025 年 TCV 訂單（分析師稱 $45 億以上）中大客戶與中型客戶各占多少？｜答法：Unknown Executive 談長銷售週期、工具整併與 key accounts，未拆分 TCV 訂單的客群貢獻，也未確認分析師提出的 $45 億數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Eric Heath (KeyBanc)：BYOC 的可服務客群、何時廣泛推出、進入市場策略？｜答法：Yrieix Garnier 稱已在預覽並有付費客戶，客群點名資料在地化與合規產業、超大規模客戶；未給一般上市時程
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Arti Vula (JPMorgan)：目前 AI 產生的程式碼量能否量化、是否已進到正式環境並帶動用量？｜答法：Unknown Executive 只做定性回答（訊號與開源都顯示程式碼變多），稱多數公司仍在早期，未給量化數字；改以 'we should see where we are at the end of the year' 收尾

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
{"date":"20260924","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","irr_base_pct":1.4,"ev5y_pct":4.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":1.1,"ev5y_pct":4.3,"irr_base_pct":1.4,"max_dd_pct":-70,"bull_5y_price":450.0,"bear_5y_price":94.4,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","price_at_dd":251.49,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
