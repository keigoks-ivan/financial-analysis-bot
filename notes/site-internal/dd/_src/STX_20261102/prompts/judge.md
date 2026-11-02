你是 stock-analyst **v20 判斷 agent**，標的 STX（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"STX","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":3629,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"$M（YoY +48.5%，QoQ +16.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 investors.seagate.com Q4 FY26 press release（表格對照 SEC 8-K 附件 stxq42026pressreleasefinan.htm）"},"note":"共識約 $3.48–3.50B（媒體彙整兩個版本 $3.48B／$3.50B，非單一權威來源）；亦高於公司 Q4 指引上緣 $3.55B（$3.45B ±$0.1B）"},{"id":"f_kpi1_non_gaap_gross_margin","label":"Non-GAAP gross margin","value":52.7,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）"},"note":"未取得共識"},{"id":"f_kpi2_non_gaap_operating_incom","label":"Non-GAAP operating income／margin","value":44.6,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%（營業利益 $1,619M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks（QoQ +710 bps，non-GAAP opex $293M＝營收 8%）"},"note":"未取得共識（僅查到營收與 EPS）"},{"id":"f_kpi3_gaap_operating_income_ma","label":"GAAP operating income／margin","value":43.0,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%（營業利益 $1,559M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release（表格對照 SEC 8-K 附件）"},"note":"未取得共識"},{"id":"f_kpi4_non_gaap_diluted_eps","label":"Non-GAAP diluted EPS","value":5.71,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"$（GAAP $5.58；QoQ +39%，YoY +121%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks"},"note":"共識約 $5.09–5.10（媒體彙整兩個版本）；亦高於公司 Q4 指引上緣 $5.20（$5.00 ±$0.20）"},{"id":"f_kpi5_free_cash_flow","label":"Free cash flow","value":1118,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"$M（FCF margin 約 31%；營運現金流 $1,305M − capex $187M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release（表格對照 SEC 8-K 附件）；FY2026 全年 FCF $3,105M"},"note":"未取得共識"},{"id":"f_kpi7_guidance_q1_fy2027_reven","label":"Guidance — Q1 FY2027 revenue","value":4100,"period":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027（2026 年 9 月季）的指引","unit":"$M（區間 $4,000–4,200M；中點 YoY +56%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027（2026 年 9 月季）的指引","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks"},"note":"未取得 Q1 FY27 共識"},{"id":"f_kpi8_guidance_q1_fy2027_non_g","label":"Guidance — Q1 FY2027 non-GAAP operating margin（營收中點）","value":50,"period":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引","unit":"%（約；non-GAAP opex 約 $300M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引","citation":"CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）"},"note":"未取得 Q1 FY27 共識"},{"id":"f_kpi9_guidance_q1_fy2027_non_g","label":"Guidance — Q1 FY2027 non-GAAP diluted EPS","value":7.3,"period":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引","unit":"$（區間 $7.10–7.50；稅率約 16%、稀釋股數 231M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks"},"note":"未取得 Q1 FY27 共識"},{"id":"f_kpi10_guidance_fy2027","label":"Guidance — FY2027 全年營收成長（定性，無數字區間）","value":"> 34","period":"Q4 FY2026 公告（2026-07-28）","unit":"%（管理層僅稱 FY27 營收成長將高於 FY26 的 34%；capex 維持 4–6% 營收目標區間）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q4 FY2026 公告（2026-07-28）","citation":"CEO／CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）"},"note":"未取得"},{"id":"f_kpi11_exabytes_shipped","label":"Exabytes shipped（總出貨）","value":218,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"EB（YoY +34%，QoQ +9.5%；其中資料中心 195 EB，占 89%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）"},"note":"未取得"},{"id":"f_kpi12_revenue_per_exabyte_asp","label":"Revenue per exabyte（ASP 替代指標，自算）","value":16.6,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"$M／EB（營收 $3,629M ÷ 218 EB；QoQ +6.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"自算：IR 新聞稿營收 ÷ 法說逐字稿總出貨 EB；公司未揭露單價（ASP）"},"note":"不適用"},{"id":"f_kpi13_price_per_exabyte_yoy","label":"Price per exabyte（YoY）","value":10,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%（6 月季；9 月季指引隱含約 20% 以上，為 Morgan Stanley 分析師推算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[13]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"Q4 FY26 法說 Q&A（Morgan Stanley 分析師引述公司數字，CFO 答覆確認供需缺口擴大、定價較佳；Koyfin 逐字稿）"},"note":"不適用"},{"id":"f_kpi14_inventory_days","label":"Inventory days（期末庫存天數，自算）","value":82.6,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"天（期末庫存 $1,571M ÷ 單季銷貨成本 $1,731M × 91 天）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[14]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"自算：IR 新聞稿資產負債表與損益表（SEC 8-K 附件 stxq42026pressreleasefinan.htm）；公司未揭露 DIO"},"note":"不適用"},{"id":"f_kpi15_nearline_exabyte_lta_bac","label":"Nearline exabyte 長約（LTA）覆蓋（backlog 替代；公司未揭露數字 backlog／book-to-bill／產能利用率）","value":"vast majority 已配置至 CY2028","period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"定性；HAMR 占 nearline exabyte 出貨run rate 約 40%（6 月）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[15]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"CEO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）；訂單須先簽約定義規格與價格才開始生產，涵蓋整個 CY2027"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_stx_gross_margin_pct","label":"STX 毛利率","value":50.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_stx_operating_margin_pct","label":"STX 營業利益率","value":40.49,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_stx_fcf_margin_pct","label":"STX FCF 利潤率","value":30.13,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mu_gross_margin_pct","label":"MU 毛利率","value":80.72,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_mu_operating_margin_pct","label":"MU 營業利益率","value":74.59,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_mu_fcf_margin_pct","label":"MU FCF 利潤率","value":44.27,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_000660_ks_gross_margin_pct","label":"000660.KS 毛利率","value":76.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_operating_margin_pct","label":"000660.KS 營業利益率","value":68.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_fcf_margin_pct","label":"000660.KS FCF 利潤率","value":47.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_gross_margin_pct","label":"005930.KS 毛利率","value":57.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_operating_margin_pct","label":"005930.KS 營業利益率","value":36.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_fcf_margin_pct","label":"005930.KS FCF 利潤率","value":28.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_285a_t_gross_margin_pct","label":"285A.T 毛利率","value":61.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.285A.T.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_285a_t_operating_margin_pct","label":"285A.T 營業利益率","value":55.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.285A.T.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_285a_t_fcf_margin_pct","label":"285A.T FCF 利潤率","value":30.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.285A.T.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi6_sbc_non_gaap","label":"SBC 占 non-GAAP 營業利益","value":3.3,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%（SBC $54M；占營收 1.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release non-GAAP 調節表（FY2026 全年 SBC $213M − 前三季 $159M＝Q4 $54M，與新聞稿單季數相符）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":644.58,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-11.19,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":37.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.62,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（40.6 → 40.35）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.7,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（64.62 → 65.07）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.03,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（87.31 → 87.28）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":40.35,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":65.07,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":87.28,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":12.08,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 36.0 → 40.35（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":33.8,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝29.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":29.5,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":10.72,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝66.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":66.2,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":10.83,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝64.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":64.5,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.97,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 40.35，分子＝快照價 644.58","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.459,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1414.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 2672.0、現金 1258.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":229.56,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":149384.51,"period":"2026-11-02","unit":"USD m","basis":"市值 147970.51 ＋ 淨負債 1414.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":20305.82,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":27968.47,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.36,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 644.58 / W52 606.35 / W104 367.09 / W250 195.08 / W250 13週斜率 4.97%"},{"id":"f_ma_w52","label":"52 週均線","value":606.35,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":367.09,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":195.08,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":4.97,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Tom Coughlin 估 2025 全年 HDD 三家出貨份額：以台數計 WDC 42.3%、STX 40.8%、Toshiba 17%；以容量（EB）計 WDC 約 47%、STX 約 42%、Toshiba 約 11%。","source":"Forbes (Tom Coughlin), 'C4Q 2025 And 2025 Hard Disk Drive Industry Update' https://www.forbes.com/sites/tomcoughlin/2026/02/02/c4q-2025-and-2025-hard-disk-drive-industry-update/ （數字取自搜尋摘要，WebFetch 未能讀全文）","url":null,"excerpt":null,"as_of":"2026-02-02","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026 年第二季全球 HDD 出貨 504.3EB，季增 5.6%；估計營收 85 億美元，季增 14.9%；上半年 HDD 產業營收逾 150 億美元，全年有機會超過 300 億美元。","source":"Forbes (Tom Coughlin), 'HDD Industry Revenue Could Top $30B In 2026' https://www.forbes.com/sites/tomcoughlin/2026/08/09/hdd-industry-revenue-could-top-30b-in-2026/ （數字取自搜尋摘要，WebFetch 遇 403）","url":null,"excerpt":null,"as_of":"2026-08-09","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"STX 10-Q（期間結束 2026-04-03）披露 nearline 容量出貨由 497EB 增至 695EB，成長 39.8%。此為 STX 自身絕對出貨量，非份額數字。","source":"SEC EDGAR, Seagate Form 10-Q https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000088/stx-20260403.htm （數字取自搜尋摘要；as_of 取財報期間結束日，實際比較期間未核）","url":null,"excerpt":null,"as_of":"2026-04-03","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Blocks & Files 報導 Toshiba 推出 11 碟 34TB SMR 硬碟（僅據文章標題「Toshiba goes glassy-eyed with 11-platter 34TB SMR drive」，內文未讀）。","source":"Blocks & Files https://www.blocksandfiles.com/disk/2026/03/31/toshiba-goes-glassy-eyed-with-11-platter-34tb-smr-drive/5213568","url":null,"excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Seagate FY2026 10-K (fiscal year ended 2026-07-03) states that one customer accounted for about 14% of consolidated revenue; the excerpt retrieved does not name the customer and does not list other customers above 10%.","source":"Seagate FY2026 Form 10-K (SEC accepted 2026-08-04), via StockTitan: https://www.stocktitan.net/sec-filings/STX/10-k-seagate-technology-holdings-plc-files-annual-report-6e534d62e382.html","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261102","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"Forbes (Tom Coughlin) headline reports Seagate qualified its 40TB-class HAMR (Mozaic) HDDs at two leading data center companies and ships them to those customers; this is a qualification/ramp fact, not a second-source or in-house disclosure.","source":"Forbes, Tom Coughlin, 'Seagate Ships Highest Capacity Hard Drives To Leading Data Center Companies': https://www.forbes.com/sites/tomcoughlin/2026/03/03/seagate-qualifies-40tb-hamr-hdds-at-two-leading-data-center-companies/","url":null,"excerpt":null,"as_of":"2026-03-03","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 10-K (fiscal year ended 2026-07-03): one customer accounted for approximately 14% of Seagate's consolidated revenue. Two secondary sources (Stock Titan 10-K summary and GuruFocus SWOT) give the same figure.","source":"Stock Titan, 'Seagate outlines data storage strategy and risks | STX Annual Report (10-K)' https://www.stocktitan.net/sec-filings/STX/10-k-seagate-technology-holdings-plc-files-annual-report-6e534d62e382.html ; GuruFocus, 'STX SWOT Analysis: Financial Strength and Market Challenges Revealed in 10-K Filing' https://www.gurufocus.com/news/9004434/stx-swot-analysis-financial-strength-and-market-challenges-revealed-in-10k-filing","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Trefis reports Seagate management said nearline capacity is almost fully allocated through calendar 2027 (headline: 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand'), following the Q3 FY2026 earnings call of 2026-04-28.","source":"Trefis, 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand' https://www.trefis.com/stock/stx/articles/597921/seagate-is-sold-out-through-2027-as-ai-reshapes-hard-drive-demand/2026-04-30","url":null,"excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"The Register 標題稱硬碟（HDD）2026 年已售罄，並把原因歸給 AI 需求（僅據標題；內文未取得）。","source":"The Register, 'AI blamed again as hard drives are sold out for this year', https://www.theregister.com/on-prem/2026/02/20/ai-blamed-again-as-hard-drives-are-sold-out-for-this-year/4285453","url":null,"excerpt":null,"as_of":"2026-02-20","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"24/7 Wall St. 標題稱 Seagate 與 Western Digital 的 AI 儲存需求『已反映在定價權上』（僅據標題；內文未取得）。","source":"24/7 Wall St., 'Seagate and Western Digital: AI Storage Demand Is Now Showing Up in Pricing Power', https://247wallst.com/investing/2026/05/16/seagate-and-western-digital-ai-storage-demand-is-now-showing-up-in-pricing-power/","url":null,"excerpt":null,"as_of":"2026-05-16","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Morgan Stanley 研究被轉載為：預期 HDD 出現『更嚴重的缺貨』，至少持續到 2028 年，供應商報價將明顯高於現況，並大幅調升儲存類公司目標價。","source":"P Equity Research (X 貼文) 轉述 Morgan Stanley 研究，https://x.com/pequityresearch/status/2068189826310930478；同文另見 Futu News, https://news.futunn.com/en/post/74636545/morgan-stanley-research-forecasts-a-more-severe-shortage-of-hard","url":null,"excerpt":null,"as_of":"2026-06-20","retrieved_at":"20261102","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Forbes（Tom Coughlin）標題主張：儲存與記憶體的價格飆升支撐 AI 需求，但『可能是暫時的』（僅據標題；內文未取得）。屬週期性論點，與『結構性缺貨』說法相反。","source":"Forbes, Tom Coughlin, 'Storage And Memory Price Surges Supporting AI Demand Likely Temporary', https://www.forbes.com/sites/tomcoughlin/2025/10/10/storage-and-memory-price-surges-supporting-ai-demand-likely-temporary/","url":null,"excerpt":null,"as_of":"2025-10-10","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"2026-01-08 美國第九巡迴上訴法院撤銷地方法院判決並發回重審，讓 Seagate 對日本 NHK Spring 的懸吊組件（suspension assemblies，硬碟零件）價格壟斷民事求償得以繼續。NHK 已就此向美國最高法院申請調卷（cert）。Seagate 在此案是原告（求償方），不是被調查方。","source":"US Court of Appeals for the Ninth Circuit, No. 24-4470, opinion filed 2026-01-08 (https://cdn.ca9.uscourts.gov/datastore/opinions/2026/01/08/24-4470.pdf); Reuters via TradingView 'US appeals court revives Seagate antitrust claims against Japan's NHK Spring'; Law360 'NHK Says Seagate Antitrust Revival Cries Out For Justices'","url":null,"excerpt":null,"as_of":"2026-01-08","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2023-04-18 Seagate 與美國商務部工業安全局（BIS）達成和解：因 2020 年 8 月至 2021 年 9 月向被列入實體清單的華為出貨逾 740 萬顆硬碟，被處 3 億美元民事罰款；另有暫緩執行的拒絕出口令，在令發出滿五年且付款與稽核義務履行後豁免。","source":"CNBC 'Seagate hit with $300 million penalty for continuing $1 billion relationship with blacklisted firm Huawei' (2023-04-20); Paul, Weiss 'BIS Imposes $300 Million Penalty Against Seagate for Export Control Violations'; BIS order e2836.pdf","url":null,"excerpt":null,"as_of":"2023-04-20","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2026 10-K（會計年度止於 2026-07-03，簽署日 2026-08-04）前瞻聲明仍提到「按時支付與 BIS 和解協議的每季款項」的預期；風險因素寫明部分產品與服務受出口管制法規約束，法規變動或違反可能對業務、營運結果、財務狀況與現金流造成重大不利影響；製造據點含中國、馬來西亞、北愛爾蘭、新加坡、泰國與美國。10-K 法律程序段擷取內容僅見智慧財產權與環境事項，未見對 Seagate 的反壟斷或競爭主管機關調查。","source":"Seagate Technology Holdings plc Form 10-K FY2026 (https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm)","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Seagate FY2026 10-K risk factors state that changes in U.S. trade policy, including the imposition of sanctions or tariffs and the resulting consequences, may have a material and adverse impact on its business and results of operations; the 10-K also lists the impact of trade policy (including tariffs) and FX on the cost of producing its products and the effective price to customers as a factor.","source":"Seagate Technology Holdings plc Form 10-K, fiscal year ended 2026-07-03, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Seagate FY2026 10-K states that component manufacturing, subassembly and final test and assembly are performed at facilities in China, Malaysia, Northern Ireland, Singapore, Thailand and the United States.","source":"Seagate Technology Holdings plc Form 10-K, fiscal year ended 2026-07-03, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Seagate FY2026 10-K states that some of its products and services are subject to export control laws, that changes to or violation of these laws could have a material and adverse effect on the business, and that if it were prohibited from selling to key customers for any reason, such as export regulations, revenues and results could be materially and adversely affected.","source":"Seagate Technology Holdings plc Form 10-K, fiscal year ended 2026-07-03, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"In April 2023 the U.S. Commerce Department's BIS imposed a $300 million civil penalty on Seagate Technology LLC and Seagate Singapore for selling over 7.4 million HDDs to Huawei (added to the Entity List in May 2019) in violation of the Foreign Direct Product Rule; BIS also imposed a multi-year audit requirement and a five-year suspended Denial Order. This is the largest standalone administrative penalty in BIS history.","source":"CNBC, 'Seagate hit with $300 million penalty for continuing $1 billion relationship with blacklisted firm Huawei, despite U.S. export controls', https://www.cnbc.com/2023/04/20/seagate-to-pay-300-million-penalty-over-billion-dollar-deal-with-huawei.html ; Orrick, 'Seagate Export Control Penalty Shows New, Aggressive China-Trade Enforcement'; Arnold & Porter Enforcement Edge blog (2023-04)","url":null,"excerpt":null,"as_of":"2023-04-20","retrieved_at":"20261102","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"The Section 232 proclamation imposing a 25% U.S. tariff on certain semiconductors took effect 2026-01-15; per search-result descriptions it covers a narrow range of advanced computing chips (above TPP and DRAM-bandwidth thresholds, e.g. NVIDIA H200, AMD MI325X) and their derivative assemblies. The search results did not show hard disk drives as covered.","source":"EY Global Tax News, 'US Section 232 proclamation imposes 25% tariff on certain semiconductors', https://globaltaxnews.ey.com/news/2026-0209-us-section-232-proclamation-imposes-25-percent-tariff-on-certain-semiconductors ; C.H. Robinson client advisory 2026-01-15, 'Guidance on Section 232 Semiconductor Import Duties for 2026'","url":null,"excerpt":null,"as_of":"2026-02-09","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#5","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"A Yahoo Finance article on Western Digital (HDD peer) states that the proposed tariffs focus on a wider set of chip-related products, including hardware used in data center servers and storage, and that this could influence WDC's component and system costs and where it sources and assembles drives for hyperscale and AI customers. The article is about WDC, not STX, and does not name Section 232 or Seagate.","source":"Yahoo Finance, 'How Exposed Is Western Digital (WDC) To New Semiconductor Tariffs?', https://finance.yahoo.com/technology/articles/exposed-western-digital-wdc-semiconductor-021558493.html","url":null,"excerpt":null,"as_of":"2026-08-30","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#6","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Bloomberg reported that the U.S. and China are discussing tariff concessions to extend their trade truce; search-result text says both sides are eyeing tariff cuts on goods including American energy and agricultural products ahead of the leaders' summit.","source":"Bloomberg newsletter, 'China, US Discuss Tariff Concessions to Extend Trade Truce', https://www.bloomberg.com/news/newsletters/2026-09-16/us-and-china-trade-truce-and-tariffs","url":null,"excerpt":null,"as_of":"2026-09-16","retrieved_at":"20261102","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#7","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Fortune headline reports that Trump is readying a new tariff to punish China for its flood of cheap exports, structured so as not to endanger the trade truce or the summit with Xi Jinping (only the headline/summary was read; details not fetched).","source":"Fortune, 'Trump readies a new tariff to punish China for its flood of cheap exports—without endangering his trade truce or his summit with Xi Jinping', https://fortune.com/2026/08/24/trump-new-tariff-china-cheap-exports-trade-war-truce-summit-xi-jinping/","url":null,"excerpt":null,"as_of":"2026-08-24","retrieved_at":"20261102","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Seagate 10-K (FY ended 2026-07-03) states: 'Component manufacturing, subassembly and final test and assembly operations are performed at facilities in China, Malaysia, Northern Ireland, Singapore, Thailand and the United States.' The excerpt read gives no per-site percentage split.","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Seagate 10-K risk-factor language: 'Shortages or delays in the receipt of, or cost increases in, critical components, equipment or raw materials necessary to manufacture our products, as well as reliance on single-source suppliers, have in the past and may in the future affect our production.' Also: 'Certain components and raw materials are available from a limited number of suppliers.'","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Seagate 10-K states production requires 'commodities and specialty materials, including certain rare earth elements, precious metals and specialized alloys, which may be subject to supply constraints or price volatility.'","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Seagate 10-K states: 'Changes in U.S. trade policy, including the imposition of sanctions or tariffs and the resulting consequences, may have a material and adverse impact on our business and results of operations.' It also says some products are subject to export control laws. The excerpt read has no explicit Taiwan-specific or Middle East/Iran language.","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Third-party supply-chain mapping (Gillware, estimate) says Seagate's Springtown, Northern Ireland wafer fab is long reported to produce on the order of one third of all HDD read/write heads globally. It names TDK (Japan) as the merchant head supplier.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","url":null,"excerpt":null,"as_of":"2026-07-06","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#5","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Third-party mapping (Gillware, estimate) says Japan's Nidec makes on the order of 80% of the world's HDD spindle motors. MinebeaMitsumi is a second source with Thailand manufacturing.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","url":null,"excerpt":null,"as_of":"2026-07-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#6","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Third-party mapping (Gillware) says China accounted for roughly 60% of world mined rare-earth supply and around 90% of refining of magnet-grade material used in HDD magnets. Japan produces the finished magnets.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","url":null,"excerpt":null,"as_of":"2026-07-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#7","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Third-party mapping (Gillware) says HDD controller silicon is designed by Broadcom and Marvell and manufactured by TSMC (Taiwan), with OSAT assembly in Taiwan and elsewhere in Asia. This is an industry-level map; it does not name Seagate's own controller vendors.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","url":null,"excerpt":null,"as_of":"2026-07-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#8","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Third-party mapping (Gillware) says HDD final assembly is centered in a Thailand cluster (primary), with Malaysia and China also involved. It says the 2011 Thailand floods eliminated up to half of global HDD manufacturing capacity within weeks and roughly doubled drive prices.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","url":null,"excerpt":null,"as_of":"2026-07-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center／nearline] FQ4 FY2026（截至 2026-07-03）總營收 $3.629B，YoY +48%；FY2026 營收 $12.2B，YoY +34%（FY2025 為 $9.097B）；FQ1 FY2027 指引營收 $4.1B ±$0.1B、non-GAAP EPS $7.30 ±$0.20。","source":"Seagate IR press release「Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2026 Financial Results」https://investors.seagate.com/news/news-details/2026/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2026-Financial-Results/default.aspx","url":null,"excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center] FQ4 FY2026 Data Center 營收 $2.9B，YoY +57%，占總營收 81%（去年同期 76%）；nearline 出貨 195 EB，YoY +43%，占出貨容量 89.4%；總出貨 218 EB，YoY +34%。","source":"Blocks & Files「Seagate HAMRing customers - generating more and more $/TB」https://www.blocksandfiles.com/disk/2026/07/30/seagate-hamring-customers-generating-more-and-more-/tb/5281058","url":null,"excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center／價格] 報導稱上季每 TB 均價 YoY +10%；分析師在電話會議上談到 9 月季指引的價格成長「closer to maybe 20 percent year-over-year or even above」。Seagate FQ4 non-GAAP 毛利率 52.7%（紀錄新高）。","source":"Blocks & Files 2026-07-30（同上）；毛利率取自 Investing.com「Earnings call transcript: Seagate beats Q4 2026 forecasts」https://www.investing.com/news/transcripts/earnings-call-transcript-seagate-beats-q4-2026-forecasts-as-shares-rebound-after-hours-93CH-4818284","url":null,"excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H","valuation","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center／需求能見度] 管理層稱大部分 nearline 出貨 EB 已配置到 2028 曆年，且不少客戶正尋求把規劃期延長到 2029 年以後；FQ4 結束時 HAMR 產品約占 nearline EB 出貨 run rate 的 40%；長期 EB 成長目標為 mid-20%。","source":"Investing.com「Earnings call transcript: Seagate beats Q4 2026 forecasts as shares rebound after hours」https://www.investing.com/news/transcripts/earnings-call-transcript-seagate-beats-q4-2026-forecasts-as-shares-rebound-after-hours-93CH-4818284；配置到 2028／2029 引述另見 Blocks & Files 2026-07-30","url":null,"excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["thesis.H","moat_trend","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"[Edge IoT／legacy] FQ4 FY2026 Edge IoT 營收 $697M，YoY +20%、QoQ +14%，占總營收 19%；同季非 nearline 出貨 23 EB，YoY -10%。","source":"Blocks & Files 2026-07-30（Edge IoT $697M／+20%／19%、非 nearline 23 EB／-10%）；QoQ +14% 取自 Yahoo Finance「Can Seagate Extend the Growth Momentum in Its Edge IoT Business?」https://finance.yahoo.com/markets/stocks/articles/seagate-extend-growth-momentum-edge-131300564.html","url":null,"excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center／產業供需] 搜尋摘要引述 X 帳號 pequityresearch 一則標題為「Morgan Stanley research forecasts a 'more severe ...'」的貼文，內容稱：2026 年 nearline HDD 供給缺口約 300 EB（10%–15%），2027、2028 年擴大到約 400 EB；未來 2–3 年 nearline EB 供給受限，CAGR 約 30%–35%，需求成長 40%–50%。","source":"X post by pequityresearch（轉述 Morgan Stanley 研究）https://x.com/pequityresearch/status/2068189826310930478","url":null,"excerpt":null,"as_of":"2026-06-20","retrieved_at":"20261102","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"TrendForce 稱 AI 推論需求使 nearline HDD 交期由數週拉長到 52 週以上；高容量 QLC SSD 出貨 2026 年『可能爆發式成長』；與 nearline HDD 相比，QLC SSD 效能較高、功耗約低 30%。該文未給 QLC 出貨量或每 TB 成本的數字。","source":"TrendForce Press Center, 'Soaring Inference AI Demand Triggers Severe Nearline HDD Shortages; QLC SSD Shipments Poised for Breakout in 2026' https://www.trendforce.com/presscenter/news/20250915-12714.html","url":null,"excerpt":null,"as_of":"2025-09-15","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"TrendForce 報導標題指 Seagate 財測優於預期，且 nearline HDD 產能到 2026 年已全數被訂走（fully booked through 2026）。內文細節未逐字核對。","source":"TrendForce News, '[News] Seagate Q3 Guidance Tops Estimates, Nearline HDD Capacity Fully Booked Through 2026' https://www.trendforce.com/news/2026/01/28/news-seagate-q3-guidance-tops-estimates-nearline-hdd-capacity-fully-booked-through-2026/","url":null,"excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Seagate Mozaic 4+ HAMR 平台已通過兩家頂級超大規模雲端業者資格認證並進入量產，支援單碟／整機容量最高 44TB，並提到未來朝單碟 10TB、整機 100TB 擴展。","source":"Yahoo Finance, 'Seagate (STX) Expands HAMR With Hyperscalers: Is Mozaic 4+ the Margin Story Investors Missed?' https://finance.yahoo.com/news/seagate-stx-expands-hamr-hyperscalers-043020641.html","url":null,"excerpt":null,"as_of":"2026-03-05","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"同一篇文章列出的風險：若需求或價格轉弱，Seagate 的負債與資本密集度是否可控；並提到謹慎的分析師擔心能源效率需求上升，可能限縮 Mozaic 4+ 的上行空間。文章未量化 SSD 替代幅度，也未寫 WD 的 HAMR 時程。","source":"Yahoo Finance, 'Seagate (STX) Expands HAMR With Hyperscalers: Is Mozaic 4+ the Margin Story Investors Missed?' https://finance.yahoo.com/news/seagate-stx-expands-hamr-hyperscalers-043020641.html","url":null,"excerpt":null,"as_of":"2026-03-05","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Western Digital 公布路線：40TB UltraSMR（ePMR 為基礎）預計 2026 下半年推出，已在兩家超大規模客戶認證中；HAMR 預計 2027 完成客戶認證並量產；目標 2029 年推出 100TB HAMR。另據報導 WD 計畫將 ePMR 延伸到 60TB 級。這是 HDD 同業路線，非 SSD 替代，但顯示 HAMR 第二供應商預計 2027 進場。","source":"Western Digital press release 'Western Digital Accelerates Storage Innovation for AI Era' https://www.westerndigital.com/company/newsroom/press-releases/2026/2026-02-03-western-digital-accelerates-storage-innovation-for-ai-era（細節同見 Tom's Hardware / Guru3D 報導）","url":null,"excerpt":null,"as_of":"2026-02-03","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#5","axis":"substitute_technology","section":"coverage","direction":"+","claim":"搜尋到 Seagate FY2026 10-K（期間止於 2026-07-03）的摘要指出：財年末 HAMR 產品約占 nearline 每季出貨 exabyte 執行率的 40%；Mozaic 3 已在所有主要雲端客戶通過認證；Mozaic 4（最高 44TB）正與兩大雲端業者放量。此條摘自搜尋結果摘要，未開 10-K 逐字核對。","source":"Seagate Technology Holdings plc Form 10-K FY2026 https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Seagate FY2026 營收通路占比：OEM 81%、經銷商 13%、零售 6%；對比前一年 OEM 80%、經銷商 12%、零售 8%（零售降 2 個百分點）。","source":"Seagate FY2026 10-K / ARS（SEC EDGAR，stx-20260703.htm；stxq426filingx2026x08x31x1.pdf）；百分比取自搜尋結果摘要，WebFetch 只抓到 10-K 部分段落，未能親眼對到該表","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Seagate 10-K 寫明：主要客戶（含 OEM 與超大型雲端業者）依主採購協議（master purchase agreements）購買，依客戶採購單與需求預測出貨；針對高容量 nearline 硬碟，與關鍵客戶建立較長期的需求預測與供應承諾，並在特定情況下設有取消費用條款。","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"DIGITIMES 報導標題與開頭：Seagate 正走向以合約為主的商業模式，因雲端與超大型客戶更重視供應可預期性，勝過短期採購彈性。（全文付費牆，僅確認標題與開頭一句。）","source":"DIGITIMES Asia, Sherri Wang, 'Seagate leans on long-term contracts as storage demand stabilizes', https://www.digitimes.com/news/a20260429VL218/seagate-demand-business-capacity-hdd.html","url":null,"excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FQ3 2026 法說（搜尋摘要轉述）：Seagate 已與幾乎所有主要雲端／超大型客戶簽有 exabyte 規模供應協議，nearline 產能到 2027 日曆年幾乎全數配置；正在敲定涵蓋到 FY2027 年底的 build-to-order 合約（定義規格與價格）；規劃討論已延伸到 2028 年以後，多年期客戶協議延伸至 2028–2029。細節取自搜尋摘要，未逐字對到逐字稿。","source":"Seagate Q3 FY2026 earnings call（Alpha Spread 逐字稿頁 https://www.alphaspread.com/security/xber/847/investor-relations/earnings-call/q3-2026；Seagate 8-K stx-20260428.htm）","url":null,"excerpt":null,"as_of":"2026-04-28","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#4","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Seagate 32TB 容量硬碟開始向通路（channel）與零售夥伴全球出貨。","source":"Business Wire, 'Seagate 32TB Capacities Now Shipping to Channel and Retail Partners Globally', https://www.businesswire.com/news/home/20260112624971/en/Seagate-32TB-Capacities-Now-Shipping-to-Channel-and-Retail-Partners-Globally","url":null,"excerpt":null,"as_of":"2026-01-12","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#5","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"同業對照（非 STX）：Western Digital 與前七大客戶有確定採購單，其中兩家簽有 2027 日曆年長約、一家簽有 2028 日曆年長約（搜尋摘要轉述）。","source":"Blocks & Files, 'Western Digital blows hard disk drive future wide open', https://www.blocksandfiles.com/ai-ml/2026/02/03/western-digital-blows-hard-disk-drive-future-wide-open/4090494","url":null,"excerpt":null,"as_of":"2026-02-03","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ1 2027 指引（2026-07-28）高於分析師預期","source":"MarketBeat: Seagate releases Q1 2027 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/seagate-technology-nasdaqstx-releases-q1-2027-earnings-guidance-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"共識目標價 $898.52、22 位分析師 Buy（7/24）","source":"MarketBeat: STX stock price down 6.8%","url":"https://www.marketbeat.com/instant-alerts/seagate-technology-nasdaqstx-stock-price-down-68-whats-next-2026-07-24/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ1 實績 EPS $7.68、營收 $4.23B 超預期；FQ2 指引營收 $4.80B、EPS $9.20","source":"24/7 Wall St: Seagate Tops Q1 2027 Estimates but Guides to $4.8B Next Quarter","url":"https://247wallst.com/cards/seagate-technology-q1-2027-earnings-stx-01m5zg90mk29dvmt5zgqe2kcj1","excerpt":"$7.68 est $7.40 +3.7% Revenue $4.23B est $4.14B +2.2% Guidance is the reason to stay interested: management sees $4.8 billion in revenue next quarter as HAMR drives record profitability.","as_of":"2026-10-27","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"StockAnalysis 共識目標價 $829.05，低 $545、高 $1,140","source":"StockAnalysis STX forecast","url":"https://www.stockanalysis.com/stocks/stx/forecast/","excerpt":null,"as_of":"2026-05-29","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"In re Seagate Technology Holdings plc Securities Litigation（Huawei 銷售相關）：2026-04-03 達成和解原則，總額 1.75 億美元，保險公司約負擔 7,000 萬，公司認列 1.05 億美元費用；2026-07-07 法院初步核准，最終核准聽證 2026-11-17。","source":"SEC EDGAR 10-K FY2026 Note 12","url":"https://www.sec.gov/Archives/edgar/data/1137789/000113778926000159/stx-20260703.htm","excerpt":"On April 3, 2026, the parties agreed to a settlement in principle to resolve the matter for a total amount of $175 million, approximately $70 million of which will be paid by the Company’s insurers. The parties have since executed a stipulation of settlement. The Company recorded a charge of $105 million which was included in Legal settlement in its Consolidated Statements of Operations and Comprehensive Income. On July 7, 2026, the court granted preliminary approval of the settlement, and a final approval hearing will be held on November 17, 2026.","as_of":"2026-08-04","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 8-K 共 15 份，其中含重大項目者 8 份；內容為可交換票據贖回／交換發股（Item 3.02／8.01）與董事／高管異動（5.02），清單中無 1.01／2.01／4.02 等併購或重編項目。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001137789&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 15 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 8 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Seagate is expanding its HDD head facility in Bloomington, MN by almost 3X, from 11,000 sq ft of clean room space to 19,000 sq ft. The article says the added capacity is expected 12-18 months out, i.e. later 2027 or 2028.","source":"Yahoo Finance (Forbes/Tom Coughlin syndication), 'Hard Disk Drive Unit Shipments Could Grow To Support AI Workloads', https://finance.yahoo.com/technology/articles/hard-disk-drive-unit-shipments-031628090.html","url":null,"excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261102","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"TDK announced increased HDD head production capacity in April 2026, to support demand from Toshiba and possibly other HDD makers.","source":"Yahoo Finance (Forbes/Tom Coughlin syndication), 'Hard Disk Drive Unit Shipments Could Grow To Support AI Workloads', https://finance.yahoo.com/technology/articles/hard-disk-drive-unit-shipments-031628090.html","url":null,"excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Seagate and Western Digital both prioritize raising storage capacity (exabyte) shipments over raising HDD unit volume. The article's unit-shipment scenarios: +1.2% from 2025 to 2026; about +11% over 2026-2030 (median); up to +30% over 2026-2030 (high case, tied to capacity expansion announcements).","source":"Yahoo Finance (Forbes/Tom Coughlin syndication), 'Hard Disk Drive Unit Shipments Could Grow To Support AI Workloads', https://finance.yahoo.com/technology/articles/hard-disk-drive-unit-shipments-031628090.html","url":null,"excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261102","affects":["moat_trend","thesis.H","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Seagate FY2026 capex was $569M, up from $265M the prior year, about 4.7% of revenue. The article gives no FY2027 capex guidance.","source":"XenoSpectrum, 'Seagate's Gross Margin Hits 52.7%, HDDs in the AI Era Earn Through Density, Not Unit Volume', https://xenospectrum.com/en/seagate-fy2026-hamr-margin/","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Seagate nearline HDD supply allocations are largely filled through 2028, and customers are already discussing 2029 and later procurement. Cloud providers want to lock in capacity over several years rather than buy spot. The article says Seagate must meet demand through areal density rather than unit volume growth.","source":"XenoSpectrum, 'Seagate's Gross Margin Hits 52.7%, HDDs in the AI Era Earn Through Density, Not Unit Volume', https://xenospectrum.com/en/seagate-fy2026-hamr-margin/","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Trefis 引述 Seagate 管理層：nearline 產能『almost fully allocated through calendar 2027』（已被預訂到 2027 年底）。","source":"Trefis, 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand', https://www.trefis.com/stock/stx/articles/597921/seagate-is-sold-out-through-2027-as-ai-reshapes-hard-drive-demand/2026-04-30","url":null,"excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"同篇 Trefis 文章寫：Seagate 現在是『setting terms with customers rather than reacting to market fluctuations』，走多年期 build-to-order 合約；並稱傳統的庫存過剩風險『no longer a near-term concern』（此為 Trefis 的描述，非公司財報數字）。","source":"Trefis, 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand', https://www.trefis.com/stock/stx/articles/597921/seagate-is-sold-out-through-2027-as-ai-reshapes-hard-drive-demand/2026-04-30","url":null,"excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"同篇 Trefis 文章引述：非 GAAP 毛利率 Q3 達『all-time high of 47.0%』，去年同期為 36.2%。","source":"Trefis, 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand', https://www.trefis.com/stock/stx/articles/597921/seagate-is-sold-out-through-2027-as-ai-reshapes-hard-drive-demand/2026-04-30","url":null,"excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261102","affects":["valuation","moat_trend"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2023（截至 2023-06）營收 $7.384B，FY2022 為 $11.661B；GAAP 毛利率 18.3%（FY2022 為 29.7%）、non-GAAP 毛利率 21.1%（FY2022 為 30.1%）；GAAP 淨損 $529M（FY2022 為淨利 $1.649B）；營運現金流 $942M（FY2022 為 $1.657B）。","source":"Seagate IR — Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2023 Financial Results, https://investors.seagate.com/news/news-details/2023/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2023-Financial-Results/default.aspx","url":null,"excerpt":null,"as_of":"2023-07-26","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2023 第四季（2023-06 季）營收 $1.602B，去年同期 $2.628B；GAAP 毛利率 19.0%（去年同期 28.9%）、non-GAAP 毛利率 19.5%（去年同期 29.3%）；GAAP 淨損 $92M。","source":"Seagate IR — Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2023 Financial Results, https://investors.seagate.com/news/news-details/2023/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2023-Financial-Results/default.aspx","url":null,"excerpt":null,"as_of":"2023-07-26","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"過去十二個月（至 FY2023 結束）產能閒置費用（扣除折舊攤銷後）合計 $171M，公司揭露原因含無錫廠疫情封控與生產計畫調整。","source":"Seagate IR — Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2023 Financial Results, https://investors.seagate.com/news/news-details/2023/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2023-Financial-Results/default.aspx","url":null,"excerpt":null,"as_of":"2023-07-26","retrieved_at":"20261102","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2023 第三季（2023-03 季）營收約 $1.9B、毛利率 17%，為搜尋摘要所見 FY2023 各季中最低的一季（搜尋摘要轉述 10-Q 與 Seagate IR 第三季新聞稿；未抓全文核對，as_of 取季末日）。","source":"SEC Form 10-Q for quarter ended 2023-03-31, https://www.sec.gov/Archives/edgar/data/1137789/000113778923000029/stx-20230331.htm","url":null,"excerpt":null,"as_of":"2023-03-31","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#4","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Blocks and Files 報導：FY2023 營收較前一年下滑 37%，為 17 年來最低年度營收，也是 13 年以上來首次全年虧損；CEO Mosley 稱「a profound downturn in demand」，原因包含中國復甦不均、雲端庫存消化、企業支出謹慎；最大買家超大規模雲端業者的 nearline 硬碟採購大減。","source":"Blocks and Files — Seagate cites 'profound downturn in demand' as revenues dip... and it won't get better soon, https://www.blocksandfiles.com/disk/2023/07/27/seagate-cites-profound-downturn-in-demand-as-revenues-dip-and-it-wont-get-better-soon/1613546","url":null,"excerpt":null,"as_of":"2023-07-27","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#5","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Tom Coughlin（Forbes）：2023 年第二季全產業硬碟出貨總容量（EB）較第一季下降約 19.3%；2023 全年出貨容量估約 875EB，較前一年下降約 29%（搜尋摘要彙整自 Coughlin 系列文章，全年數字對應文章為 2023-12-10 的 2024 年預測，未抓全文核對）。","source":"Forbes / Tom Coughlin — C2Q 2023 Hard Disk Drive Industry Update, https://www.forbes.com/sites/tomcoughlin/2023/08/14/c2q-2023-hard-disk-drive-industry-update/ ；Digital Storage And Memory Projections For 2024, Part 1, https://www.forbes.com/sites/tomcoughlin/2023/12/10/digital-storage-and-memory-projections-for-2024-part-1/","url":null,"excerpt":null,"as_of":"2023-08-14","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#6","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"Coughlin 硬碟產業歷史文章：硬碟營收自 1956 年起長期成長至 2012 年見頂（該年因前一年泰國水災造成硬碟短缺而墊高），出貨顆數高點在 2010 年（6.51 億顆）；此後營收與顆數均下滑（搜尋摘要轉述，未抓全文）。","source":"Forbes / Tom Coughlin — Hard Disk Drive Revenue History From 1957 To Today, https://www.forbes.com/sites/tomcoughlin/2024/01/02/hard-disk-drive-revenue-history-from-1957-to-today/","url":null,"excerpt":null,"as_of":"2024-01-02","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#7","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"+","claim":"對照點：Seagate FY2026 第三季 non-GAAP 毛利率為創紀錄的 47%，較上季增 480 bps、較去年同期增約 1,080 bps。","source":"Yahoo Finance — Can Seagate Sustain Its Gross Margin Expansion Momentum?, https://finance.yahoo.com/markets/stocks/articles/seagate-sustain-gross-margin-expansion-135900141.html","url":null,"excerpt":null,"as_of":"2026-05-22","retrieved_at":"20261102","affects":["valuation","moat_trend"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"證券集體訴訟（class period 2020-09-14 至 2023-04-19）以 1.75 億美元和解，公司認列 1.05 億美元費用；2026-07-07 初步核准，2026-11-17 最終核准聽證。","source":"SEC EDGAR 10-K FY2026 Note 12","url":"https://www.sec.gov/Archives/edgar/data/1137789/000113778926000159/stx-20260703.htm","excerpt":"On April 3, 2026, the parties agreed to a settlement in principle to resolve the matter for a total amount of $175 million, approximately $70 million of which will be paid by the Company’s insurers. The parties have since executed a stipulation of settlement. The Company recorded a charge of $105 million which was included in Legal settlement in its Consolidated Statements of Operations and Comprehensive Income. On July 7, 2026, the court granted preliminary approval of the settlement, and a final approval hearing will be held on November 17, 2026.","as_of":"2026-08-04","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"STX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.35,"operating_margin_pct":40.49,"fcf_margin_pct":30.13,"rd_intensity_pct":5.57},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STX","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"MU","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":80.72,"operating_margin_pct":74.59,"fcf_margin_pct":44.27,"rd_intensity_pct":4.24},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU","as_of":"TTM ending 2026-08-31（4季加總）"}},{"name":"000660.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.27,"operating_margin_pct":68.04,"fcf_margin_pct":47.8,"rd_intensity_pct":4.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"005930.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.48,"operating_margin_pct":36.88,"fcf_margin_pct":28.95,"rd_intensity_pct":9.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"285A.T","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":61.72,"operating_margin_pct":55.7,"fcf_margin_pct":30.28,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.285A.T","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"STX"},"financial_history":{"ticker":"STX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":7384000000.0,"revenue_yoy_pct":null,"gross_margin_pct":18.3,"operating_margin_pct":0.81,"net_income":-529000000.0,"diluted_eps":-2.560115,"free_cash_flow":626000000.0,"fcf_margin_pct":8.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":6551000000.0,"revenue_yoy_pct":-11.28,"gross_margin_pct":23.45,"operating_margin_pct":6.44,"net_income":335000000.0,"diluted_eps":1.580071,"free_cash_flow":664000000.0,"fcf_margin_pct":10.14,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":9097000000.0,"revenue_yoy_pct":38.86,"gross_margin_pct":35.18,"operating_margin_pct":21.05,"net_income":1469000000.0,"diluted_eps":6.770305,"free_cash_flow":818000000.0,"fcf_margin_pct":8.99,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":12195000000.0,"revenue_yoy_pct":34.06,"gross_margin_pct":45.58,"operating_margin_pct":34.65,"net_income":3184000000.0,"diluted_eps":13.900626,"free_cash_flow":3105000000.0,"fcf_margin_pct":25.46,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STX/STX_Q1_2027_Earnings_Call_20261027.md）

# Q1 2027 Earnings Call
**Seagate Technology Holdings plc** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Welcome to the Seagate Technology Fiscal First Quarter 2027 Conference Call. [Operator Instructions] Please note, this event is being recorded.
I would now like to turn the conference over to Shanye Hudson, Senior Vice President, Investor Relations. Please go ahead.

**Shanye Hudson** (Executives):
Thank you. Hello, everyone, and welcome to today's call. Joining me are Dave Mosley, Seagate's Chair and Chief Executive Officer; and Gianluca Romano, our Chief Financial Officer. We've posted our earnings press release and detailed supplemental information for our September quarter results on the Investors section of our website.
During today's call, we'll refer to GAAP and non-GAAP measures. Non-GAAP figures are reconciled to GAAP figures in the earnings press release posted on our website and included on our Form 8-K. We've not reconciled certain non-GAAP outlook measures because material items that may impact these measures are out of our control and/or cannot be reasonably predicted. Therefore, a reconciliation to the corresponding GAAP measures is not available without unreasonable effort.
Before we begin, I'd like to remind you that today's call contains forward-looking statements that reflect management's current views and assumptions based on information available to us as of today and should not be relied upon as of any subsequent date. Actual results may differ materially from those contained in or implied by these forward-looking statements as they are subject to risks and uncertainties associated with our business.
To learn more about the risks, uncertainties and other factors that may affect future business results, please refer to the press release issued today and our SEC filings, including our most recent annual report on Form 10-K and quarterly report on Form 10-Q as well as the supplemental information, all of which may be found on the Investors section of our website.
Following our prepared remarks, we'll open the call up for questions. [Operator Instructions]
With that, I'll hand the call over to you, Dave.

**William Mosley** (Executives):
Thank you, Shanye, and hello, everyone. Fiscal '27 is off to an outstanding start. September quarter revenue grew by more than 60% year-over-year and non-GAAP EPS expanded by nearly 3x to a record $7.68. We also achieved record gross and operating margins, demonstrating the earnings power of our business and ongoing demand strength for data storage. Both the data center and edge IoT markets delivered double-digit sequential revenue growth, up 18% and 13%, respectively, reflecting ongoing demand and pricing strength. These trends support our expectation to deliver strong sequential revenue growth and gross margin expansion throughout fiscal 2027. Our confidence is supported by an extremely strong demand environment with visibility extending beyond 2030 and an areal density-driven technology road map poised to capture this growth.
In the September quarter, we shipped a record 198 exabytes nearline capacity into data center customers, and we expect a meaningful step-up in the December quarter, supported by the continued ramp of Mozaic 4. As we stage new generations of Mozaic products and ship to a broader customer base, quarterly exabyte growth may vary. At the same time, we expect our technology road map to support nearline exabyte supply growth in the mid-20% range on a compound basis.
Overall, we delivered another very strong quarter, including record free cash flow generation of nearly $1.5 billion, driven by durable demand, our continued technology innovation and disciplined operational execution.
Additionally, we significantly strengthened the balance sheet, achieved our primary debt reduction objectives and regained investment-grade status. With those goals largely achieved, we are shifting our focus towards capital returns with share repurchases serving as our primary vehicle complemented by dividends. This month, our Board approved an increase in the quarterly dividend to $0.76 per share.
Importantly, this capital allocation strategy reflects our confidence in the cash flow potential of the business as well as the multiyear demand visibility afforded by our customer agreements. Demand strength continues to be driven by data center customers, which accounted for 90% of our shipped capacity. Within data center, Cloud nearline products achieved a 12th consecutive quarter of revenue growth, while enterprise OEM revenue reached its second highest quarterly level in over a decade. Data growth is profound across a wide variety of applications.
Behind these trends is a growing recognition that the value of data extends well beyond its original use. In a recent discussion with Seagate, a leading hyperscale customer observed that their customers are increasingly discovering new ways to extract value from data long after it's initially stored, strengthening the incentive to retain it and AI innovations are amplifying this dynamic.
As AI adoption expands beyond model training and toward inference and agentic applications, persistent data becomes increasingly important. These systems rely on vast amounts of historical data to make informed decisions and take effective actions while constantly generating new output that must be governed, retained and reused.
Estimates suggest that billions of AI agents will be deployed worldwide over the next decade, executing hundreds of billions of actions daily. At that scale, agents will continuously consume, generate and reuse data. We believe future storage demand will increasingly be tied to this new data life cycle and compound again as physical AI applications proliferate.
As the volume of persistent data grows, storage demand can extend well beyond the initial infrastructure buildout. These positive demand dynamics play directly into the strength of hard drives, which deliver the scalable, reliable and cost-efficient foundation for data retention. Hyperscale customers have long recognized these benefits and continue to pursue higher capacity storage architectures.
Our engineering teams work closely with leading cloud providers to align our product road map with future data storage requirements and simplify the adoption of higher capacity drives. A recent example is Microsoft's qualification of a joint Seagate and Broadcom solution that combines our HAMR-based Mozaic drives configured with SMR technology and Broadcom's connectivity infrastructure.
Microsoft already deploys HAMR drives, and this recent qualification validates the SMR-enabled solution at hyperscale. Customers can benefit from additional capacity gains that SMR provides. However, broad adoption at higher drive capacities has been limited given the meaningful architectural and software changes required. This joint solution provides a blueprint for implementing SMR storage to unlock additional capacity gains on top of our HAMR-based Mozaic platform.
Beyond hyperscalers and CSPs, demand is expanding among a broader set of enterprise OEM customers that are managing increasingly large data sets. We are engaging more directly with many of these customers and developing reference architectures that pair proven compute and storage hardware with flexible customer selected software. These solutions offer a path to scale persistent data capacity, improve storage economics and drive platform efficiencies. The strengthening demand environment is extending our customers' planning horizons, which is reflected in the supply agreements we now have in place. The vast majority of our nearline exabyte supply is now allocated under long-term supply agreements through calendar 2028 with some cloud customer agreements extending through calendar 2030.
Our strategic planning discussions extend even further. We are working closely with customers to address their growing storage needs across this time horizon by executing our Mozaic product road map. As we transition to HAMR-based Mozaic products, we are investing in additional tools and technologies necessary to offset longer manufacturing cycle times and maintain stable unit production.
For Seagate, increasing capacity per disk is driving exabyte growth. Our build-to-order contracts establish specific configuration and pricing terms for nearline shipments through calendar 2027. As we move through the next few quarters, we expect to begin finalizing configuration and pricing terms with customers for the exabyte supply that we've allocated to them for calendar 2028.
Pricing continues to improve, reflecting both the execution of our value-based pricing framework and higher external component costs. We expect a stronger demand environment evident in customers' multiyear commitments to continue to support these healthy pricing dynamics. Taken together, these agreements provide customers with greater supply assurance while increasing visibility for both parties. They also reflect customer confidence in long-term demand growth and the increasingly strategic role that hard drive storage plays in the modern data ecosystem.
Supporting this demand growth requires storage solutions to deliver scale, efficiency and economics. These very attributes serve as the foundation for our technology strategy. Increasing storage density within the same data center footprint is the most cost-efficient way to maximize bytes per square foot, as one large hyperscale customer put it, and our HAMR-enabled road map is designed to deliver on that objective.
Advancing areal density is our North Star. We are scaling drive capacity through areal density rather than relying on higher drive unit production. We believe that this is the most efficient way to help customers manage their extreme data growth and retention needs. The same approach supports profitable exabyte growth for Seagate.
We are executing well on the product road map milestones that we've outlined. We continue to expect HAMR to represent roughly 50% of our nearline exabyte shipment run rate exiting calendar 2026, with Mozaic 4 representing roughly half of those HAMR shipments. Mozaic 4, which offers up to 44 terabytes of capacity, is continuing to ramp with 2 leading CSPs. We are on track for additional qualifications to complete over the next couple of months across multiple global CSPs and OEM enterprise customers.
Product development for our third generation Mozaic 5 product remains on track. These drives can deliver upwards of 50 terabytes of capacity and leverage our highly efficient 10-disk platform. We continue to expect customer qualification shipments to begin towards the end of calendar 2027.
Reflecting on our ongoing advancements in photonics, we recently demonstrated 8 terabytes per disk in the lab, providing further evidence that HAMR and the Mozaic platform can deliver on customers' growing capacity needs and reinforces our conviction that increasing exabyte supply through areal density growth is the right long-term strategy for both our customers and for Seagate.
Wrapping up, our results demonstrate both the durability of demand and the effectiveness of our strategy. Data creation, retention and reuse are compounding demand for mass capacity storage. And based on the long-term visibility we have with customers, we believe we're still in the early days of a multiyear growth phase.
Our technology road map, combined with disciplined supply management and a value-based pricing strategy and the operational leverage in the business, gives us confidence in our ability to deliver strong profitability, cash generation and shareholder returns.
I'd like to recognize our global team for their execution in delivering a record quarter and a strong start to fiscal '27. I'd also like to thank our customers, suppliers and shareholders for their continued trust and support.
Now I'll turn the call over to Gianluca.

**Gianluca Romano** (Executives):
Thank you, Dave. Seagate posted very strong results for the September quarter, exceeding the high end of our guidance range for both revenue and earnings per share, while continuing to establish new profitability records that translated into our highest ever free cash flow generation.
September quarter revenue was $4.2 billion, up 17% sequentially and up 61% year-over-year. Non-GAAP gross margin came in at 57.8%, up 510 basis points sequentially. Non-GAAP operating margin increased 610 basis points sequentially to 50.7%. And non-GAAP EPS was $7.68, up 35% quarter-over-quarter and 194% year-over-year.
Sustained data center demand continues to drive strong company performance. In the September quarter, we shipped a total of 220 exabytes, up 21% year-over-year, with data center representing 90% of that total. Data center revenue was $3.4 billion, up 18% sequentially and 63% year-over-year, and representing 81% of total revenue.
Data center shipments totaled 198 exabytes, up 24% year-over-year, and represented 90% of the company's overall exabyte volume. As Dave noted, we are staging Mozaic 4 products ahead of anticipated customer qualification and we expect capacity shipments to meaningfully step up in the December quarter.
Global cloud customers accounted for the vast majority of data center revenue and exabyte demand, a trend that we expect to continue as we ramp Mozaic 4 volume. At the same time, demand across the enterprise OEM data center market has continued to strengthen.
As AI applications transition more toward inference and agent-based workloads, customers are seeking scalable, high-capacity storage solutions across hybrid cloud data center environments. In the September quarter, revenue from these markets increased for the sixth consecutive quarter with double-digit growth both sequentially and year-over-year.
Complementing the strength in our data center business, our edge IoT markets also delivered solid revenue growth. Revenue totaled $784 million representing 19% of total revenue. This was an increase of 13% sequentially and 52% year-over-year.
Moving on to the rest of the income statement. Non-GAAP gross profit increased significantly to $2.4 billion, up 28% quarter-over-quarter and more than doubling from $1.1 billion in the year ago period.
Non-GAAP gross margin expanded to 57.8%, up from 52.7% in the prior period, reflecting favorable pricing execution and an improving product mix as we ramp Mozaic 4 products. These factors more than offset cost headwinds associated with certain externally-sourced components. Looking ahead, we expect continued benefit from our value-based pricing strategy and product mix to support quarterly margin expansion for the rest of fiscal 2027.
Non-GAAP operating expenses were $300 million or about 7% of revenue. The strong demand environment, combined with disciplined expense management, drove substantial operating leverage with non-GAAP operating profit up 33% sequentially to $2.1 billion, representing 50.7% of revenue.
Other income and expenses totaled $38 million in the September quarter. Following the debt reduction we completed early in October, we anticipate other income and expenses to decrease further in the December quarter to approximately $25 million, benefiting from the lower interest expense. Non-GAAP net income grew to $1.8 billion with corresponding non-GAAP EPS of $7.68 per share based on tax expense of $328 million and a diluted share count of approximately 232 million shares.
Turning now to cash flow and the balance sheet. Operating cash flow was $1.7 billion, and capital expenditures were $211 million for the September quarter, or 5% of revenue. For fiscal 2027, we continue to expect CapEx investment will remain within our target range of 4% to 6% of revenue, as we support the ongoing transition to HAMR technology.
Higher profitability and in-line CapEx resulted in free cash flow generation of $1.5 billion, up 32% from the prior quarter and more than tripling year-over-year. We expect cash generation to further improve throughout fiscal 2027, supported by sustained demand, operational efficiencies and CapEx discipline.
During the September quarter, we retired $1.2 billion in debt, including the remaining convertible notes and approximately $1 billion in high-yield debt. We exited the quarter with gross debt of approximately $2.4 billion and a net leverage ratio of 0.2x.
Following the close of the September quarter, we retired an additional $750 million of high-yield senior notes reducing principal debt to approximately $1.6 billion. As a result of our actions, we expect to be net cash positive exiting this calendar year.
We have now delivered on our goal of strengthening the balance sheet and are now focused on returning more of our free cash flow generation to our shareholders. During the September quarter, we returned $568 million to shareholders through dividends and share repurchases, roughly 2x the amount returned in the June quarter. We are also increasing our quarterly dividend by approximately 3% to $0.76 per share, reflecting our confidence that strong cash generation is sustainable.
We exited the September quarter with $4.4 billion remaining on our existing share repurchase authorization and expect to significantly increase share repurchases starting calendar 2027. We ended the September quarter with cash and cash equivalents of $1.3 billion and total liquidity of $2.6 billion, including our undrawn revolving credit facility.
Turning now to the December quarter outlook. We expect another quarter of strong sequential growth, underpinned by continued demand momentum, a significant increase in exabyte shipments and ongoing execution of our value-based pricing strategy. We expect December quarter revenue to be in a range of $4.8 billion, plus or minus $100 million, which represents a 70% year-over-year improvement at the midpoint. Non-GAAP operating expenses are expected to remain flat at approximately $300 million. Based on the midpoint of our revenue guidance, non-GAAP operating margin is expected to expand towards the mid-50% range. Non-GAAP EPS is expected to be $9.20 plus or minus $0.20 based on a tax rate of about 16% and non-GAAP diluted share count of 233 million shares.
Our September quarter results and December quarter outlook reinforce our expectation for annual revenue growth to meaningfully outpace fiscal 2026. Durable demand, increasing Mozaic adoption and healthy operating leverage are supporting ongoing revenue growth, margin expansion and strong cash generation. Together with our increasing focus on capital returns, we are well positioned to increase long-term shareholder value.
Operator, let's open the call up for questions.

**Operator** (Operator):
[Operator Instructions] The first question today is from C.J. Muse with Cantor Fitzgerald.

**Christopher Muse** (Analysts):
I guess first question regarding exabyte deceleration in the September quarter. I'm curious, given your inventory days moved up to 97 from 83, was there kind of staging involved prebuilding that's supporting your outlook for the accelerated exabytes into December? And then maybe as you think about calendar '27, you were kind of in the mid-30s range. You're reiterating kind of the mid-20s long term.
Curious, given the ramp of Mozaic, whether we should be kind of in that 30%-plus range? Or do you think we will revert to that compounded number at some point in calendar '27?

**William Mosley** (Executives):
C.J., thanks for the question. Yes. If you think back to the June quarter, we had a pretty appreciable step-up. In the September quarter, we were relatively flat, to your point. And the quarter we're in now, the December quarter, we'll step up again. So we are on a trajectory and I think 25% is a really good number for that.
We're driving product transitions, and we have to stage them quite a ways out in time. We make sure that we lock in with our customers on what they need to when those things have to hit their dock and sync up with all the other parts that they need to build the data center. So pretty happy with the progress and still staging very aggressive areal density and product transition technologies so that we can get to those higher exabyte levels.

**Gianluca Romano** (Executives):
Yes, C.J., we have a few customers that will qualify Mozaic 4 in the next quarter. And therefore, we are preparing manufacturing for those quals and the volume that we can ship to them in the December quarter and later.

**Christopher Muse** (Analysts):
Perfect. And as a quick follow-up, Gianluca, on the operating margin guidance in the slide deck approaching or towards the mid-50s, should we be modeling 50%? Or are you suggesting something else?

**Gianluca Romano** (Executives):
No, I think that's...

**Christopher Muse** (Analysts):
55%, sorry. 55%, sorry...

**Gianluca Romano** (Executives):
Well, we are suggesting something that is between 50% and 55%. So of course, it's another improvement compared to what we have done this quarter that was already above the 50%. So we are very happy on how we are managing the operating margin in particular. We have seen continuous improvement in revenue, in gross margin, very stable OpEx.
So this is resulting in sequential strong improvement in operating margin, and we are approaching even higher results that we have guided for this December quarter. And as we said in prior calls, we expect to improve even more in the rest of the fiscal year.

**Operator** (Operator):
Next question is from Erik Woodring with Morgan Stanley.

**Erik Woodring** (Analysts):
Really strong pricing, obviously, in the quarter. I'd love any commentary that you could provide there just on how to look forward on that price per terabyte metric, but separately, also, just to address the cost per terabyte declines. Over the last 4 quarters, you've done something like 15% annual cost declines or year-over-year cost declines. You just did kind of mid-single digits. So can you maybe help us understand any temporary factors that are impacting that related to the Mozaic transition? Or when we should expect that metric to accelerate? And then a quick follow-up, please.

**William Mosley** (Executives):
Yes. Thanks, Erik. It's a complicated question. So on the pricing side, I continue to believe that, that's very dependent upon demand and demand continues to be very strong, not just in quarter, but you look 2, 3, 4 quarters out, people are demanding that we go higher in exabytes as well.
So it's a great long-term relationship that we have with the customers. And we're able to predictably go through these product transitions and accelerate our technology the way we talked about. So -- and I don't see that changing. The past years ago, we would see product swaps and things like that, people saying, "I don't need product in quarter." We're seeing none of that right now. Absolutely, everything we can make above and beyond our plans is being spoken for.
On the cost side, you know that we control our manufacturing efficiency of our critical technologies. And that's the largest driver of our costs. We get a lot of efficiency, especially in cost per terabyte if that's a metric, as we transition platforms. But during some of the transitions, we get early cost, things like scrap that go up. It doesn't dissuade us from driving the transitions. We continue to drive them very hard and then we go work those things down. Right now, I see more opportunity because the future transitions look even brighter than I would have said 90 days ago. So I'm pretty excited about that.

**Gianluca Romano** (Executives):
Yes. Erik, I would say, our cost declined for what we produce. So heads and media is continuing to be very, very strong. So we are happy with that. The cost of the external component, as you know, compared to a year ago, is now much higher. And therefore, there is at least a partial offset of our internal cost reduction from a higher external component cost. So we have to see where the external component costs will go in the future. But what we can control is actually performing very well.
Now when we have enough visibility and we have the time to include that cost increase for the external component into our pricing, of course, we do it. And this is also why you're seeing a little bit higher cost increase -- sorry, price increase to our customers in the current quarter. But sometimes it's not so predictable. So we need a little bit of time to adjust.

**Erik Woodring** (Analysts):
Okay. Dave, maybe just going back to C.J.'s question at the top of Q&A. I just want to make sure I understand the kind of product staging dynamics in the September quarter. I just want to make sure there's no kind of right tail risk here in terms of any yield issues that we need to be thinking about, anything in terms of data center readiness. I just want to make sure there's none of those that are impacting and this was generally just product transition, leading to the slower sequential exabyte growth as opposed to anything maybe that would be a little more concerning.

**William Mosley** (Executives):
Yes, there's none. The big step up in the June quarter, it tapered off a little bit in the September quarter, just timing and then it will be another big step-up in the December quarter. And then as we get through these product transitions, we'll see exabyte growth.

**Operator** (Operator):
The next question is from Amit Daryanani with Evercore.

**Amit Daryanani** (Analysts):
I guess the first one was really, you folks reiterated the 4% to 6% of revenue for CapEx in fiscal '27. Is that a sustainable framework to support mid-20% exabyte growth longer term beyond fiscal '27 as well, especially given the fact that you need -- you talked about longer tooling needed to offset the longer HAMR manufacturing cycles. Could you just talk about like what the right framework would be longer term? And to the extent you need additional heads or media capacity, how do you kind of weigh between building it organically versus acquiring it?

**William Mosley** (Executives):
So first order, there is no way we can acquire the HAMR technology, the leading-edge technology. So we have to do that ourselves, exactly to your point. Yes, we see that 4% to 6% model being plenty for us to continue to grow according to our plans.
Actually, the latest acquisition of new tools is really helping us drive areal density because we get to buy remarkable new tools that are maybe more capable than what we're replacing in the factory. So that's cause for optimism.
We are using some legacy technology from outside as on a case-by-case basis that will help us through some -- help us pivot some of our manufacturing technology to HAMR. But I definitely think that 25% is the target for our exabyte growth. We can do that predominantly through the areal density transitions that we're driving. Some of those components get -- we've talked about this in the last couple of quarters. Some of those components get a little bit longer time in the factory. And so therefore, we have to adjust our output and -- accordingly, but we can do that all within the 4% to 6% window.

**Amit Daryanani** (Analysts):
Got it. That's helpful. And then as HAMR ramps up, especially with Mozaic 4 becoming a bigger percent of exabyte for you folks, what's the right way to think about cost per bit declines as you get through that transition? I get that the 4% to 6% range right now isn't the optimal one. But I'm just curious as HAMR ramps up for you, what's the right cost per bit decline longer term?

**Gianluca Romano** (Executives):
Yes. As I said before, the cost that -- for the components that we produce, of course, is continuing to decline. And when you go from 3 terabyte per disk to 4 terabyte per disk, you have major impact in terms of cost per terabyte decline.
As I said before, right now, there is also an impact from external components. So you need to separate the 2 between internal efficiency and technology improvement that is driving cost reduction and the overall cost per terabyte that is, of course, also impacted by the external supply chain and external component costs.
So we have seen a very good decline in the prior quarter, a little bit less in the September quarter. I would say we need to understand the various drivers for the different components because we buy a lot of different components externally. But overall, when you go even longer term, the technology is what is driving cost per terabyte and having a technology that continues to generate more terabyte per disk is exactly the way that we want to follow in order to reduce the cost per terabyte and improve our profitability.

**Operator** (Operator):
The next question is from Krish Sankar with TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
Dave or Gianluca, I just want to follow up on an earlier question. I understand the dynamics of the cost with the product transition. But if we just look at it from a high level, 50% of the exabytes exiting the sales is going to be HAMR, which is gross margin accretive. Unlike your peer, you're sticking to 10 platters, not going to 12 or 14, which, in theory, I think you said increases cost. So I'm just wondering why wouldn't the cost downs be even better going forward, or would you consider moving beyond the 10 platters? Was there any technical reason for not doing it? And then I have a follow-up.

**William Mosley** (Executives):
I'll start at the end. There's no technical reason for not moving beyond 10 platters. I mean I think we like the platform and we get leverage, cost leverage, to your point. Going from product generation to product generation, we don't have to transition the mechanical piece parts and pay for new tooling and things like that. So we know the platform, we like it. We're going to stay on it. But there's no technical reason why we can't start adding platters.
Actually, from a qualification perspective, it's much simpler, especially with our customers, to just qualify one thing that they don't have to go through any new risks on except for just the technology transition. They don't have to change the dynamics of how many heads and disks are in the drive.
From my perspective, I probably should have said this on one of the earlier comments as well, there's not a significant cost increase in the HAMR technology from one generation to the other. So the cost per terabyte takedown, you can pretty much calculate it, if you go from 4 to 5, for example. And we are driving 5 very, very hard right now.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got it. Got it. And then as a quick follow-up, I understand you're maintaining your capital intensity 4% to 6%. Obviously, your peers spoke about going into like 8% in the next couple of years. So obviously, the distant third player talking about adding capacity in Japan. So I'm just wondering, is the 4% to 6% still a good bogey to use for the next few years? Or should we worry about any potential share loss? Or is the demand so much greater than supply that it should not matter?

**William Mosley** (Executives):
Well, I don't really speculate on what our competitors' plans are. I'd just say relative to ours, I think 4% to 6% is just fine. I have a lot of respect for everybody in the industry that their technology solutions may differ from ours. And you may see that over the next few years. From our perspective, demand remains really strong. And from a supply side, we continue to believe that bringing meaningful HDD capacity to market is a really complex process that requires substantial investment in R&D and technology.
It's an intricate supply chain balance. And the idea of just plugging in a few machines, I mean it's orders of magnitude more difficult than that. It really requires tight coordination throughout our supply chain. So most of our -- as I said in the prepared remarks, our nearline exabyte supply is already allocated through calendar year 2028, and we're having conversations much further out than that.
So we have very -- a lot of confidence that our customers are going to be there, and we believe supply will remain fairly tight for our products over that period. So we're just going to keep focusing on our technology road map and try to get the products out and up and meet exactly what the customers need when they do, and I'm not really worried about anything else.

**Operator** (Operator):
The next question is from Asiya Merchant with Citi.

**Asiya Merchant** (Analysts):
Great. You mentioned a lot about KV cache adoption contributing to demand. So given that, how should we think about unconstrained demand and the impact to exabyte demand given just the trend that you're seeing on KV caching?

**William Mosley** (Executives):
Yes. Thanks. I do think we are watching a lot of new technologies come out that are increasing the value of data very quickly. And I know a lot of people toss around the letters AI. It gets really confusing. What I would say is the data sphere is growing leaps and bounds anyway. Just look at video on the Internet or video analytics, for example, in places like our factory, it's growing very quickly.
And then AI is an accelerator of that dynamic. The ability to take data from the application layer and move it down to the storage layer and then promote data from the storage layer back up, we've never seen the systems be as efficient as they are right now with software not in the way, with compute technologies that are much faster than they were in the past. And architecturally, things like the KV cache plug between those 2 layers only accelerates it even faster.
So very excited about that. I don't think any of us has ever lived in a world where things are this efficient above the storage layers, and I do think that will drive a lot of future demand for us.

**Gianluca Romano** (Executives):
Yes. We are seeing demand for storage in the different parts of the cloud growing very rapidly, even a little bit faster than what we were expecting. So as we were discussing before, our demand is stronger and stronger. I would say the supply-demand gap is probably growing at this point. But as we said, we are really focused on our technology transition and we will ramp more of our 40 terabyte drive in the next few quarters, and this is how we want to address demand.

**Asiya Merchant** (Analysts):
Okay. And just as a follow-up, could I just even ask about physical AI? I know that's probably a little bit longer term. But are you seeing any of that demand currently translate into meaningful inflections for your exabyte?

**William Mosley** (Executives):
I would say not yet directly, but we're hopeful. I mean we've had conversations for a long time with autonomous vehicles companies and people that are moving data around in the world. The interesting thing to us about physical AI is not only the need to store the data for training, but it's also the need to store the data to make sure we made the right decision. And that storage will probably be closer to where the data is actually created, which is the edge.
So there's maybe new products that are coming on the horizon. It's still very early days in this, but I think there's a lot of innovative companies out there driving for value-add solutions out at the edge, and we're watching them carefully. I think this could be a further driver of storage that we haven't really contemplated yet.

**Operator** (Operator):
The next question is from Mark Newman with Bernstein.

**Mark Newman** (Analysts):
Congrats on the numbers. I just want to look a little bit deeper at this price and cost to gross margin. I mean you've had another very, very strong quarter of gross margin appreciation and it's obviously baked into the guidance as well. But when I look at the price, it seems to be accelerating significantly from what was something like mid-single digits Q-on-Q to something like mid-teens Q-on-Q in the September quarter?
And meanwhile, your cost, still slightly confused about that, appears to be actually up Q-on-Q. You did point out about some of the component costs coming up. I understand that could be part of it. But is there anything else that we should be aware of, perhaps on the mix or something else that may have changed things, that may have boosted the price or the cost temporarily that we should be aware of? And I have one follow-up.

**William Mosley** (Executives):
No. Thanks, Mark. So the first thing I would always say is that I'm really happy with the bottom line. We continue to drive the operating income really well, the free cash flow really well. As you get up into things like gross margin and then above it to prices, there could be some in-quarter dynamics going on about our product transitions. I mentioned scrap already.
As we drive these hard product transitions, we have to incur some of that scrap. And we actually incur a little bit of manufacturing, I'll call it, lossiness when that happens as well. The yields on the product transition may not be where we want. We go take a quarter or 2, and we go beat those back into what the old yields were. From -- so there's a little lost capacity in that. From my perspective, the pricing dynamic is really still about the long-term demand. It's not about in-quarter demand. It's about long-term demand.
And we're having great conversations with our customers about staging these technologies, making sure that we get through the product transition and that their systems are ready for that product transition as well because they have to make sure their architecture is ready for the higher capacity drives, and we do that very carefully. And making sure we don't build too early for those transitions, making sure we just time it right.
It's very important because the size of the supply chains that we have out in the world are enormous. And in order to make sure you're doing what the customers want today, tomorrow and next year and the following year, you have to make sure you sync up the number of [ squared sets that you will ] -- with those customers. We were working all of that very hard. And I think that all plays into the pricing and the cost dynamics that you talked about.

**Gianluca Romano** (Executives):
Yes. No, that's correct. I think pricing and cost dynamics are always somehow correlated. And when we have visibility on some external cost increase, we try to pass that to customers, including that in our pricing. Sometimes, the timing is not immediate because we have contracts in place and we have commitments, but over time, that additional cost from the supply chain, if any, is going to be passed to customers, which is why pricing now is increasing a little bit faster than what we have seen in the past is also to cover that additional cost.
As I said before, there is nothing unusual internally, and our cost for producing heads and media is declining as we were expecting, but there are additional costs from external components. And as we have said before, gross margin is actually -- the improvement of gross margin is actually accelerating because pricing more than offset that increase in cost. So I think we are managing this external component cost increase in the right way, in a way that is actually accelerating the profitability of the company.

**Mark Newman** (Analysts):
Really appreciate that. And a follow-up on price. Given all that and the huge price increase you've been getting recently, I mean should we expect this type of quarterly ASP growth to continue in the mid-teens range? Or is that more of a one-off? And -- I mean I appreciate strong pricing will continue, but that was extremely strong pricing you just printed. So I'm just curious if that's realistic to consider that to continue at that rate.

**William Mosley** (Executives):
As we talked about on supply, there will be step-ups as new contracts come up all the time. I said in the prepared remarks that we don't see any demand destruction at all. If anything, we see a lot more demand creation kind of quarter-over-quarter. And we're projecting where this is going to be 3 or 4 quarters from now. Then we get into the negotiations with the customers on the exabytes that we've kind of allocated for them. We locked down the configuration and then locked down the pricing. And I don't see the trend changing too much right now.

**Gianluca Romano** (Executives):
Yes, every quarter is a bit different. Of course, everything is included in our guidance. So you see a strong revenue upside. Part of that is coming from exabyte, as Dave said before, part is coming from pricing, and I think you can model another step-up in gross margin. And of course, that is coming, at this point, mainly from pricing because we discussed about the cost and the offset from the external component cost increase.

**Operator** (Operator):
The next question is from Wamsi Mohan with Bank of America.

**Wamsi Mohan** (Analysts):
I wanted to touch on pricing as well. Maybe if you could just double click a little bit on the pricing. How much of this would you say was achieved with already contracted pricing versus what's floating, any relative percentages on there? Or hyperscaler versus OEM versus edge or by capacity tranches? Like any color incrementally just given the sheer magnitude of what we just saw? And I have a quick follow-up.

**William Mosley** (Executives):
Yes. I think most of it is on the, I'll call it, the rolling re-upping of the contracts, Wamsi. It's not because we're getting more exabytes out or we're pushing more exabytes out. We're running the business very predictably on that front. So usually, when we see a pricing upside, it will be 2 or 3 quarters away because we'll be able to find a way to get a few more exabytes out, then we'll say who wants them? That comes because we are working operations really hard and just trying to get a little bit more efficiency out of our factory.

**Gianluca Romano** (Executives):
Yes, we have not changed our pricing strategy. No, the strategy is the same. But as we said before, when we have visibility for some of the external cost increase, we have to pass that through and include in our new pricing. So when we negotiate a new contract, of course, we also consider the current situation for the external supply chain costs and adjust the pricing according to that. But apart from the change, the strategy is exactly the same that we have followed for the last 3 years at this point.

**Wamsi Mohan** (Analysts):
Right. Okay. And then just as a follow-up, on the exabyte growth, I understand that you're calling for an acceleration, a meaningful step-up again next quarter. As we think through the fiscal year, is it right to think that we should be seeing sort of improving exabyte growth trajectory as we go through the course of the year given that all this product transition issues would be behind you and you're still saying that you're meaningfully undershipping demand?

**William Mosley** (Executives):
Yes. I don't think we had any issues with product transitions. I think it's all been planned. I mean to your point, wafer cycle time is quite long. So we've known exactly what our exabyte output is going to be. Yes, you will see continued acceleration in Mozaic 4, and then we're going to start leaning into Mozaic 5 as well. So I'm very happy with the 25% number. We're going to keep driving it as hard as we can.

**Operator** (Operator):
The next question is from Ben Reitzes with Melius.

**Benjamin Reitzes** (Analysts):
Dave and Gianluca, I want to talk about the buyback and the cash return pace because you say you're going to start in the March quarter. You actually don't have any debt that comes due, I believe, until June of 2029. So you probably start with like free cash flow of around a couple of billion, maybe $2 billion at the start of this period. What does it imply for buybacks? Are you going to do 100% of the free cash flow that we start with in that March quarter of '27, and can that continue up until you have to pay down that debt? What kind of percentages of the free cash flow are we looking at here? And then I have a follow-up.

**William Mosley** (Executives):
Yes, we're -- thanks, Ben. We're very happy to be through the period where we dealt with the debt, like you said, and we're back to being ourselves, our model is 75%, and we should be able to get back to that model over some period of time. So that's great. Beyond that, it's opportunistic. When we can, when we don't think we have any other needs for the free cash flow that we're generating above and beyond that 75%, we'll look at it.

**Gianluca Romano** (Executives):
Yes, I think that's correct. No, we had the last debt repurchase earlier this month, but we are also active in the market in terms of share buyback this quarter. But we said starting next quarter because we don't have any other debt activity planned. We will step up the share buyback program. So you will see much more happening on that side starting the March quarter.

**Benjamin Reitzes** (Analysts):
Okay. Your customers, especially for most of your business, are the big hyperscalers. Are you hearing anything about in terms of their ability to purchase on time? Are you hearing anything about land, power, shell delays? Or is it more -- are you hostage to their timing of when they get chips or land, power, shell? And how are you managing that? And how would you characterize that?

**William Mosley** (Executives):
Yes, Ben, that's an interesting question. The answer to your question is no. But there -- we are very mindful of the fact that we don't want any of our products sitting anywhere. And so it's very important that we don't overbuild and we build exactly to what we think the demand is. The demand for exabytes will strengthen. The more exabytes in the box makes the data center much more efficient. The customers know that. They want that.
In general, the storage layer doesn't use a whole lot of power compared to the compute layer. It doesn't use a whole lot of space and it doesn't use a whole lot of money either. So we can calculate all those things, but we just do not want to -- we don't want to overship into a channel that necessarily doesn't have the components elsewhere, right?
We want to make sure we spread out as much as we possibly can. And I think we're doing a good job of that, giving our customers that predictability not just for next quarter, but for the next few years now, so that they know exactly what they're going to have to acquire, and they know what their footprint is, they know what their data requirements are, but also their data center capabilities are, and we try to time all that together.

**Operator** (Operator):
The next question is from Karl Ackerman with BNP Paribas.

**Karl Ackerman** (Analysts):
Obviously, hyperscale demand is robust, but you spoke about near record sales from on-prem enterprise. I'm cognizant that CPU providers have said traditional server demand supports 25% of the agentic CPU opportunity. So my question is, frankly, have you seen it yet? And as more of the CPU racks become deployed over the next 12 months across both hyperscale and on-prem, how is your penetration rate of high-capacity hard drives changing due to this agentic CPU demand build?

**William Mosley** (Executives):
Yes, it's an interesting question. I would say, typically, those enterprise and OEM customers lagged quite a bit, the highest capacity points, and they're starting to not lag as much. I mean -- so the storage layers are much more data rich, and the products are higher capacity drives than they ever have been before. I think maybe inside of your question, there's some of this -- is it truly just an on-prem instance where you may only have 1 petabyte? Or is it -- are we talking about people that may be serviced through these channels that may grow to a larger scale?
I think we're seeing both. And there's demand for both types of products. So there may be just on-prem meaning a small office or a small enterprise, and then there may be some of these channels that are actually servicing people who are doing software cloud instances and things like that.

**Operator** (Operator):
The next question is from Joe Quatrochi with Wells Fargo.

**Joseph Quatrochi** (Analysts):
I was wondering if you could just quantify what was the external component impact on gross margin? And then is that expected to be completely offset and embedded in the December quarter guide?

**Gianluca Romano** (Executives):
Yes, it is included in the December guidance. As I said before, there is the cost related to what we produce, and that is declining as rapidly as we said in the past. And then there is the cost of what we buy externally. And if you compare to the cost of the same component a year ago, today that cost is higher. And so it's partially offsetting the cost decline that we generate internally. But everything is included in the guidance, and the guidance is showing an improvement, not only -- strong improvement, not only in revenue, but also in gross margin, in operating margin and, of course, EPS.
So I think the trend of improvement is the same that you have seen in the past. And of course, we are managing these additional external costs as well as we can and still generating strong improvements.

**Joseph Quatrochi** (Analysts):
And then maybe as a follow-up, apologies for another question coming about ASPs. But just thinking about just the increase in dollar per terabyte, can you help us understand like how much of that was maybe mix driven by higher HAMR contributions relative to, like, like-for-like price uplift?

**William Mosley** (Executives):
Yes. Let's see. The product is going to, say, hyperscalers, they are pulling really hard on new capacity points that are much more efficient, better TCO proposition for their data centers. So we get the benefit from that. Relative to price per terabyte, that's fairly well blended across the entire portfolio. So some of those contracts with the hyperscalers are more 4 quarters. Think of it as 4 quarters rolling, if you will. And some of the other stuff is a little less than that.
So I don't know that you can really look at it different markets. But I think that relative to our ability to actually predict, we're going after the highest capacity points to make sure that we keep those big chunks of demand kind of predictable for us so we can run our factories.

**Operator** (Operator):
The next question is from Joseph Cardoso with JPMorgan.

**Joseph Cardoso** (Analysts):
Maybe just wanted to follow up. I think in the past, you kind of hinted at maybe an outlook around HAMR exiting your fiscal '27. So just curious if there's any update there on how we should be thinking about HAMR share of nearline as we track through the fiscal year, just given any shifts in thoughts around constraints on getting there faster, like customer quals, head wafer cycle times or any other variables? And then I do have a quick follow-up.

**William Mosley** (Executives):
Thanks, Joseph. Everything on the 4 terabyte per platter is on track. So we're happy with the qualification progress. We're happy with the initial units we've shipped to the field and how they're doing in the field. Everything is on track there. The 5-terabyte is that we're actually more optimistic than we were last quarter, I'd say.
We see the ability to make this transition a little bit faster than what we had originally planned, and we'll get to talking to that when we get into fiscal '28. We're going to stage that and go as hard as we possibly can because that's yet another improvement for us. And I also see the 5 terabyte per platter extending fairly rapidly into 6 terabyte per platter.
So love this platform. The technology development is going quite well, and we're pretty optimistic about it. We'll keep driving it.

**Gianluca Romano** (Executives):
Yes. So I'll say there are no changes on our targets that we discussed in the prior quarter in terms of HAMR as a percentage of total nearline exabyte for end of calendar '26 and then for fiscal '27.

**Joseph Cardoso** (Analysts):
Got it. Makes sense. And then just wanted to touch on some of the comments in the prepared remarks that you guys had around agreement extending through calendar '30, if I heard correctly. Maybe just touch on like -- is there any changes or differences between the agreements going out all the way through calendar '30 versus maybe the ones that are more near term in terms of calendar '28? Just curious in terms of how you guys are thinking about or like what's -- how we should be thinking about, maybe more importantly, around those agreements relative to locking in exabyte pricing, et cetera? And maybe how these agreements are influencing your capacity plans?

**William Mosley** (Executives):
Our process hasn't changed. So we're giving visibility to people about how -- what our exabyte growth will be and then we're saying, basically, when you get within, say, 12 months, we lock in the configuration that we're going to be building in our factories, and then we lock in pricing, and that's what I would call the build-to-order process that we have.
As things roll forward, if demand stays strong, as strong as it is, we may see that some of those contracts start, we lock in at higher prices, that's fine. We also would understand very quickly if somebody wasn't pulling according to the plan, we could pull back. We don't see any evidence of that right now.
I think we're in the -- in a multiyear growth phase for data. And the reason I say that is just go back 5 years ago, the data storage products were roughly shipping half the exabytes on a quarterly basis of where we are today. And then we had this big downturn. So the world is making up for a lot of lost time and there's growth -- extreme growth in data everywhere.
So I think the next 5 years will be very strong from that perspective. And the value of that data with some of these accelerated applications is -- it's becoming much more valuable. So I'm very excited about this. I think the customers are as well. So they know what they're planning for, what they're going to install capacity for, and we'll work together with them on that.

**Operator** (Operator):
This concludes our question-and-answer session. I would like to turn the conference back over to Dave Mosley for any closing remarks.

**William Mosley** (Executives):
Thanks, Gary, and thanks again to everyone for joining us. Look, we're entering fiscal 2027 with really strong momentum ahead of what we believe is a multiyear growth phase for mass capacity storage.
We're executing our strategy that positions Seagate to capture that opportunity through continued technology innovation and disciplined execution with a relentless focus on driving profitable growth and creating value for our customers and shareholders. Thank you, and we'll talk to you next quarter.

**Operator** (Operator):
The conference has now concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### STX_Q4_2026_Earnings_Call_20260728.md
- 2026-07-28｜CFO｜guidance：CFO 給 9 月季營收指引 41 億美元 ±1 億（原話："to be in the range of $4.1 billion, plus"）
- 2026-07-28｜CFO｜guidance：9 月季 non-GAAP EPS 指引 7.30 ±0.20（原話："expected to be $7.30, plus or minus $0.20,"）
- 2026-07-28｜CEO｜guidance：CEO 預期 FY2027 營收成長高於 FY2026（原話："we expect fiscal 2027 revenue growth to outpace our"）
- 2026-07-28｜CFO｜guidance：CFO 預期 FY2027 資本支出落在營收 4%–6% 目標區間（原話："will remain well within our target range of 4% to 6% of"）
- 2026-07-28｜CFO｜margin：CFO 稱 6 月季 non-GAAP 毛利率 52.7%，季增 570bp（原話："Non-GAAP gross margin came in at 52.7%, up 570 basis points"）
- 2026-07-28｜CFO｜margin：CFO 將毛利率改善歸因於長期定價策略與產品組合（原話："This improvement reflects continued execution of"）
- 2026-07-28｜CFO｜margin：CFO 被問 80% 毛利率時稱沒有具體目標（原話："we don't have a specific"）
- 2026-07-28｜CFO｜margin：CFO 稱增量毛利率遠高於分析師所提的 60%，但不給未來指引（原話："Our incremental gross margin is well above the 60%"）
- 2026-07-28｜CFO｜margin：CFO 說明價格上行主因是供需缺口擴大、需求強，不是策略改變（原話："the gap between supply and demand is now a little bit"）
- 2026-07-28｜CFO｜margin：CFO 稱特定早期 HAMR 客戶優惠價在 9 月季不再出現，但非價格改善主因（原話："it's not the major reason why pricing"）
- 2026-07-28｜CFO｜commitment：CFO 承諾 FY2027 全年營收續增、毛利率擴張（原話："We remain confident in delivering sequential"）
- 2026-07-28｜CEO｜commitment：CEO 稱 FY2027 預期毛利率與現金創造逐季成長（原話："deliver sequential margin and cash generation growth"）
- 2026-07-28｜CEO｜commitment：CEO 稱長期供貨協議下，絕大部分 nearline 容量已配置到 2028 年（原話："the vast majority of our nearline exabytes are now"）
- 2026-07-28｜CEO｜commitment：CEO 稱公司先取得訂單才開始生產，合約約定 2027 全年規格與價格（原話："We remain disciplined in securing orders from these"）
- 2026-07-28｜CEO｜commitment：CEO 重申 nearline 出貨量(EB)年增中段 20% 目標（原話："support our mid-20% exabyte growth target"）
- 2026-07-28｜CEO｜commitment：CEO 稱策略是硬碟機數量維持持平，靠磁頭與碟片提升容量（原話："keep the number of drives flat"）
- 2026-07-28｜CEO｜product：CEO 稱 HAMR 產品占 nearline 出貨量(EB)約 40%（原話："HAMR-based products represented approximately 40%"）
- 2026-07-28｜CEO｜product：CEO 預期 2026 年底 HAMR 出貨量中 50% 在 Mozaic 4 平台（原話："exiting calendar '26 with 50% of our HAMR exabytes on our"）
- 2026-07-28｜CEO｜product：CEO 稱 Mozaic 5 預計 2027 年底送樣驗證（原話："Mozaic 5, our 5-plus terabyte per disk platform,"）
- 2026-07-28｜CEO｜product：CEO 稱有意放慢 Mozaic 4 放量節奏，因客戶驗證週期（原話："We intentionally have maybe throttled the Mozaic 4 ramp"）
- 2026-07-28｜CFO｜product：CFO 稱 Mozaic 4 自 3 月開始出貨，6 月季明顯放量（原話："we started shipping Mozaic 4 in March."）
- 2026-07-28｜CFO｜product：CFO 提及公司正投資更多工具與技術支援 HAMR 製造（原話："strategically investing in additional tools and technology"）
- 2026-07-28｜CEO｜product：CEO 稱 KV cache 與 agentic 應用仍屬極早期（原話："Both very, very early days."）
- 2026-07-28｜CEO｜customer：CEO 稱資料中心占出貨量(EB)約 90%（原話："Data center demand now represents"）
- 2026-07-28｜CEO｜customer：CEO 稱客戶沒有縮短規劃期，且有意延長至 2029 年以後（原話："are not seeing customers pull back on planning horizons."）
- 2026-07-28｜CEO｜customer：CEO 稱企業 nearline 營收連續第五季成長，且與 neocloud 接觸增加（原話："Enterprise nearline revenue increased for a fifth"）
- 2026-07-28｜CEO｜customer：CEO 稱 neocloud 過去偏運算，現開始需要資料與近端儲存（原話："I would have said neocloud is probably largely compute-based"）
- 2026-07-28｜CFO｜customer：CFO 稱 6 月季資料中心營收 29 億美元，季增 17%、年增 57%（原話："with data center revenue coming in at $2.9 billion, up 17%"）
- 2026-07-28｜CEO｜competition：CEO 稱 HAMR 最終將完全取代產品組合，並提到 PMR 比預期推得更久（原話："we have pushed maybe PMR a little bit harder than we"）
- 2026-07-28｜CFO｜capital_allocation：CFO 稱年底總債務約 36 億美元，預期 FY2027 Q1 底降至 24 億（原話："probably end fiscal Q1 at $2.4 billion in debt."）
- 2026-07-28｜CFO｜capital_allocation：CFO 稱本季庫藏股執行額高於上季，且會持續數季（原話："we are executing a higher level of share buyback"）
- 2026-07-28｜CFO｜capital_allocation：CFO 稱 9 月季再償還 12 億美元債務，7 月已清償 10 億高收益債（原話："we are retiring an additional $1.2 billion in debt"）
- 2026-07-28｜CFO｜capital_allocation：CFO 稱 6 月季自由現金流超過 11 億美元，為十年來最佳（原話："we generated free cash flow of more than $1.1 billion"）
- 2026-07-28｜CEO｜risk：CEO 稱新應用的需求預測相對更難（原話："is relatively harder"）
- 2026-07-28｜CEO｜risk：CEO 稱製程轉換期間工廠會有些許效率損失（原話："there's a little bit of inefficiency in your factories."）
- 2026-07-28｜CEO｜risk：CEO 稱面密度轉換可能不足以滿足全部需求（原話："I do not think that probably our areal"）

### 問答異常語氣（迴避／改口／保留）
- STX_Q4_2026_Earnings_Call_20260728.md｜問：Aaron Rakers 問 9 月季指引是否隱含約 57% 毛利率，及每年每 TB 約 15% 的成本下降是否可持續｜答法：CEO 轉給 CFO 量化；CFO 談定價策略與產品組合延續，未確認 57% 也未回答每 TB 成本降幅是否可持續
- STX_Q4_2026_Earnings_Call_20260728.md｜問：Erik Woodring 問每 EB 價格年增已從 10% 加速至 20% 以上，之後是否持續｜答法：CFO 承認缺口擴大、定價優勢更大，但未給後續幅度，稱要看接下來幾季
- STX_Q4_2026_Earnings_Call_20260728.md｜問：Wamsi Mohan 問 FY27/FY28 EB 有多少已由 BTO 鎖定，及價格動能幅度｜答法：CEO 未給鎖定比例，改談 FY27 可預測性與良率增產；CFO 只談特定客戶優惠價影響，未回答後續漲幅
- STX_Q4_2026_Earnings_Call_20260728.md｜問：Joseph Cardoso 問不增加硬碟機數量是否涵蓋 2028 配置與 2029 規劃，及遠期價格能見度｜答法：CEO 重述硬碟機數量持平與磁頭磁碟片製程複雜度，未回答遠期價格能見度
- STX_Q4_2026_Earnings_Call_20260728.md｜問：Tom O'Malley 問 2027 年 6 月 HAMR 占 nearline EB 70% 的目標追蹤進度｜答法：CEO 稱 HAMR 如預期但提到 PMR 推得比預期久；CFO 只確認 40% 里程碑達成及「on track」，未重申 70% 數字
- STX_Q4_2026_Earnings_Call_20260728.md｜問：Vijay Rakesh 問毛利率是否達 60% 以上及 HAMR 4 的增量毛利｜答法：CFO 稱「I'm not guiding for the future」，僅說增量毛利率遠高於 60%，未給 HAMR 4 增量數字

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

## ⑥ 條件附卡（archetype_hint='循環/商品' 命中）：judge_addendum_cyclical.md

<!-- source: .claude/skills/stock-analyst/references/cyclical-lens.md sha256:b13d95972edd47ea git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary 或 secondary ∈ {循環/商品，EMS/ODM}（QC-43 判定，含 capex 建設循環／需求量循環子型） -->

# QC-42 循環交易讀數（附錄 B）附卡

循環股的錢在 Game 2（投降買、延伸賣）。本附卡是平行、明標投機的交易讀數，不改長抱裁決。[§WHY]

## 一、觸發與子型判定
無循環 sleeve（純成長 mis-route）→ 整段省略。[§①]
商品子型（下列≥2命中→用商品 through-cycle 錶）：近5-7年≥1個GAAP虧損年｜peak-to-trough毛利率擺動>~20pp｜營收主由商品ASP驅動(price-taker)｜產業∈{記憶體/DRAM/NAND、礦業/材料/稀土、化工、航運、鋼鐵、太陽能、油氣E&P、部分晶圓/設備}｜capex/rev結構性>15%且ROIC高度擺動。未達≥2仍判循環→依驅動來源選capex建設循環錶或需求量循環錶。[§商品子型]

## 二、循環位置錶族（三選一，錨自身 through-cycle 區間非動能；位置落 深谷投降/早循環/中循環/晚循環/過熱頂部，多數決+sourced 裁決）
商品 through-cycle（MU 型，6 訊號）：P/B vs 自身區間(近1x/下緣=買，>中位2x/上緣=賣)｜量 vs 價(量增領先=買，ASP-only量平降=賣)｜GM vs自身區間(近谷/負=買，近峰=賣)｜供給紀律(減產=買，新產能洪水=賣)｜庫存(去化乾淨=買，通路+公司堆積=賣)｜情緒/部位(投降PT>價=買，狂熱PT<價=賣)。[§B.1商品]
capex 建設循環（ORCL 型，6 訊號）：capex/折舊比(低/正常化=買，遠高於1=賣)｜產能利用率爬坡(低基期回升=買，滿載見頂=賣)｜RPO(backlog)vs capex覆蓋(backlog領先=買，capex超前需求=賣)｜交易對手信用(客戶分散信用強=買，集中燒錢客戶=賣)｜情緒/部位(同上)｜量vs價(量增領先=買，ASP承壓量見頂=賣)。[§B.1capex]
需求量循環（EMS/ODM，JBL 型，5 訊號）：book-to-bill/需求量拐點(>1拐點向上=買，<1量見頂=賣)｜客戶庫存去化(去化乾淨=買，通路+客戶堆積=賣)｜倍數vs自身歷史re-rate均值回歸(近下緣=買，>5Y中位×1.5/貼峰=賣)｜終端·hyperscaler capex週期位置(早週期=買，晚週期見頂=賣)｜情緒/部位(同上)。[§B.1需求量]

## 三、交易姿態 + 反動能硬閘（跨子型通用，逐條檢查，觸發即 override 向保守）
位置→姿態：深谷投降→積極分批建立｜早→分批建立｜中→持有不加｜晚→分批了結｜頂→清光不碰。[§B.2]
閘1 位置=晚/頂→姿態不得為任何「建立」。閘2 成長=ASP-only+量持平/降→最多「持有」。閘3 P/B>自身中位2x→禁新建立。閘4 訊號矛盾→標「位置不明，觀望」不硬給姿態。閘5 TTM/Fwd本益比或EV倍數>自身歷史高區(>5Y中位×1.5、或貼/破歷史峰)→禁新建立。[§閘1-5]

## 四、落欄與 §13 row 8b 接線
`cycle_position`(深谷投降｜早循環｜中循環｜晚循環｜過熱頂部)＋`cycle_verdict`(右側可追蹤｜等回踩｜頂部觀望｜未觸發)；非循環 archetype 不填，整欄省略。[§落欄]
接 §13 row 8b：位置∈{深谷投降，早循環}+五閘全過+moat底線+獨立critic冷讀通過→落「進場・條件式(循環衛星)」(倉位上限3%)；任一不成立→只落研究提名，§13維持觀望。驗證失敗不得升級，只能降回觀望。`trade_stance`僅進HTML不入dd-meta。[§row8b]

## 五、雙制度與兩軌背離
有 secular sleeve + commodity sleeve → 循環鏡頭只套 commodity sleeve，secular sleeve 一句話另計(不隨循環賣)。[§⑤]
投資軌(§13長抱視角) vs 交易軌(本鏡頭位置)：底部背離(長抱視角迴避 + 循環位置深谷投降/早循環)是本鏡頭獨門訊號；頂部多收斂(皆遠離)。[§B.3]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260923","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回到 $572–644（FY2027E 共識 35.78 的 16–18 倍）即重跑研究；此價位之前不建倉","irr_base_pct":-4.8,"ev5y_pct":-5.8,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.1,"ev5y_pct":-5.8,"irr_base_pct":-4.8,"max_dd_pct":-75,"bull_5y_price":1620.0,"bear_5y_price":300.0,"p_bull_pct":30,"p_bear_pct":30,"rearm_trigger":"股價回到 $572–644（FY2027E 共識 35.78 的 16–18 倍）即重跑研究；此價位之前不建倉","price_at_dd":914.72,"archetype":"循環/商品","cycle_position":"晚循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
