你是 stock-analyst **v20 判斷 agent**，標的 FTNT（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"FTNT","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTNT_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTNT_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":2078.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"百萬美元；YoY +20.5%（Q3 2025：1,724.9）；QoQ +1.5%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"},"note":"consensus 約 $2.06B（Benzinga／Hudson Labs，聚合站，約略值）"},{"id":"f_kpi1_billings","label":"Billings","value":2336.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"百萬美元；YoY +29%（Q3 2025：1,807.7）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"},"note":"公司指引區間 $2.25–2.35B，落在高端"},{"id":"f_kpi2","label":"產品營收","value":765.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"百萬美元；YoY +37%（Q3 2025：559.3）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"}},{"id":"f_kpi3_non_gaap","label":"Non-GAAP 營業利益／利益率","value":38.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%（營業利益 793.8 百萬美元）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"}},{"id":"f_kpi4_gaap","label":"GAAP 營業利益／利益率","value":33.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%（營業利益 704.3 百萬美元）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"}},{"id":"f_kpi8_q4_2026","label":"管理層指引：Q4 2026","value":"見 unit","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"營收 $2.155–2.245B；billings $2.775–2.925B；Non-GAAP 營業利益率 35.5–37.5%；Non-GAAP EPS $0.93–0.95","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"}},{"id":"f_kpi9_fy2026","label":"管理層指引：FY2026（上調）","value":"見 unit","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"營收 $8.125–8.215B；billings $9.568–9.718B；Non-GAAP 營業利益率 36.5–37.5%；Non-GAAP EPS $3.54–3.58","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ftnt_gross_margin_pct","label":"FTNT 毛利率","value":80.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FTNT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ftnt_operating_margin_pct","label":"FTNT 營業利益率","value":32.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FTNT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ftnt_fcf_margin_pct","label":"FTNT FCF 利潤率","value":43.94,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FTNT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_panw_gross_margin_pct","label":"PANW 毛利率","value":70.36,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PANW.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_panw_operating_margin_pct","label":"PANW 營業利益率","value":6.05,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PANW.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_panw_fcf_margin_pct","label":"PANW FCF 利潤率","value":35.83,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PANW.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crwd_gross_margin_pct","label":"CRWD 毛利率","value":75.25,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWD.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crwd_operating_margin_pct","label":"CRWD 營業利益率","value":-2.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWD.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crwd_fcf_margin_pct","label":"CRWD FCF 利潤率","value":28.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWD.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_msft_gross_margin_pct","label":"MSFT 毛利率","value":67.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_operating_margin_pct","label":"MSFT 營業利益率","value":47.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_fcf_margin_pct","label":"MSFT FCF 利潤率","value":17.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_okta_gross_margin_pct","label":"OKTA 毛利率","value":78.13,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.OKTA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_okta_operating_margin_pct","label":"OKTA 營業利益率","value":7.68,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.OKTA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_okta_fcf_margin_pct","label":"OKTA FCF 利潤率","value":31.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.OKTA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_non_gaap_eps","label":"Non-GAAP 稀釋 EPS","value":0.91,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"美元（Q3 2025：0.74）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"},"note":"consensus 約 $0.84（Macau Business／Benzinga，聚合站，約略值）"},{"id":"f_kpi6_fcf","label":"自由現金流（FCF）","value":864.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"百萬美元；FCF 利益率 41.6%（營運現金流 946.0）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"}},{"id":"f_kpi7_sbc","label":"SBC","value":82.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"百萬美元；占營收 3.9%、占 GAAP 營業利益 11.6%（皆為本檔由新聞稿數字換算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（2026-10-28，IR：https://investor.fortinet.com；內文取自新聞稿 finviz 全文轉載 https://finviz.com/news/410526/fortinet-reports-strong-third-quarter-2026-financial-results）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":136.08,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":57.7,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":26.63,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.57 → 3.57）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.04,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.84 → 3.88）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":1.62,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.32 → 4.39）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.57,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.88,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":4.39,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":12.97,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 3.16 → 3.57（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":44.47,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝89.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":89.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":12.69,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":12.15,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝95.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":95.5,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":38.12,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.57，分子＝快照價 136.08","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-4238.5,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 560.5、現金 4799.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":734.71,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":95740.8,"period":"2026-11-02","unit":"USD m","basis":"市值 99979.3 ＋ 淨負債 -4238.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":8174.07,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（38 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":9115.19,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（41 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":11.71,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 136.08 / W52 118.41 / W104 106.87 / W250 80.39 / W250 13週斜率 2.1%"},{"id":"f_ma_w52","label":"52 週均線","value":118.41,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":106.87,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":80.39,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.1,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出主要對手（Check Point、Cisco、CrowdStrike、Palo Alto、Zscaler、Netskope、Microsoft 等），並稱競爭將持續加劇；較大對手可能以綑綁或把功能併入既有產品來阻礙客戶購買 FTNT 產品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"The market for network security products is intensely competitive and dynamic, and we expect competition to continue to intensify. We face many competitors across the different cybersecurity markets.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出部分對手專注雲端交付安全服務（CrowdStrike、Zscaler），且 FTNT 平台多數仍為地端部署，若轉型慢於對手可能流失客戶。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"For example, certain of our competitors are focusing on delivering security services from the cloud which include cloud-based security providers, such as CrowdStrike and Zscaler.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Zacks：FTNT 2026 Q2 SASE Firewall 業務（Secure Networking＋Unified SASE）成長 34% 至逾 20 億美元，FortiSASE billings 成長逾一倍；與 Zscaler、PANW 競爭。","source":"Zacks 'Can Fortinet's SASE Momentum Propel the Stock to New Highs'","url":"https://www.zacks.com/stock/news/3011142/can-fortinets-sase-momentum-propel-the-stock-to-new-highs","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：三家經銷商各占營收10%以上（Distributor A 28%、B 15%、C 12%），第三方摘要","source":"tldrfiling.com FTNT Key Financials","url":"https://tldrfiling.com/stocks/FTNT","excerpt":null,"as_of":"2026-02-27","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 三家經銷商各占營收 10% 以上：Distributor A 28%（2024: 29%）、B 15%（15%）、C 12%（13%），合計約 55%；應收帳款占比 A 32%、B 12%、C 9%","source":"SEC EDGAR 10-K FY2025 Note 15 Segment Information","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"The following distributor customers accounted for 10% or more of our revenue: Year Ended December 31, 2025 2024 2023 Distributor A 28 % 29 % 28 % Distributor B 15 % 15 % 15 % Distributor C 12 % 13 % 13 %","as_of":"2026-02-25","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"六家直接購買的經銷商占 2025 年底應收帳款 67%（2024: 69%）；公司風險因子自述最大經銷商可能遇財務困難而影響收款","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"Six distributor customers who purchase directly from us accounted for 67% and 69% of our total net accounts receivable in the aggregate as of December 31, 2025 and 2024, respectively.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"經搜尋未找到經銷商信用評等調降、破產或財務壓力的來源","source":"WebSearch（無相關結果）","url":null,"excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Fortinet 稱約65萬台防火牆2026年底到期、約35萬台低階機2027年到期；管理層稱換機週期延續至少4-6季；結構上2027批量較小且低價","source":"Nasdaq/Zacks: Will Fortinet's Firewall Upgrade Cycle Continue to Power Top-Line Growth?","url":"https://www.nasdaq.com/articles/will-fortinets-firewall-upgrade-cycle-continue-power-top-line-growth","excerpt":null,"as_of":"2025-11-15","retrieved_at":"20261102","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2 2026 財報會議：FY2026營收指引上調至80.2-81.8億美元，管理層稱出現更廣泛的基礎設施替換機會而非僅傳統換機","source":"Chartmill: FTNT Q2 Earnings Call Highlights SASE Firewall Growth","url":"https://www.chartmill.com/news/external/100472/ftnt-q2-earnings-call-highlights-sase-firewall-growth","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025 10-K：公司目前不預期關稅對原料與產品進口成本有重大影響，但若美國擴大關稅或他國報復，產品成本可能上升、需漲價。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"While we do not currently expect tariffs to have a significant effect on our raw material and product import costs, if the United States expands increased tariffs, changes in customs or tariffs classifications or modifications to tariff exemptions or if retaliatory trade measures are taken by other countries in response to the U.S. tariffs, the cost of our products could increase","as_of":"2026-02-25","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：產品含加密技術，受美國出口管制，部分產品需出口許可或可能被禁止出口至特定國家。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"Because we incorporate encryption technology into our products, certain of our products are subject to U.S. export controls and may be exported outside the United States only with the required export license or through an export license exception, or may be prohibited altogether from export to certain countries.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：中國政府近期指示國內特定產業企業不得使用包含公司在內的美國或以色列資安產品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"the Chinese government recently instructed domestic companies in certain industries not to use cybersecurity products manufactured by the companies 47 Table of Contents based in the United States or Israel, including us and certain of our competitors.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"路透報導北京要求中國企業停用包含 Fortinet 在內的十餘家美國／以色列資安廠商產品，限 2026 上半年前替換。","source":"Reuters 經 Algemeiner 轉載","url":"https://www.algemeiner.com/2026/01/14/beijing-tells-chinese-firms-stop-using-us-israeli-cybersecurity-software-sources-say/","excerpt":"The US companies whose cybersecurity software has been banned include Broadcom-owned VMware, Palo Alto Networks and Fortinet, while the Israeli companies include Check Point Software Technologies, the sources said.","as_of":"2026-01-14","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Fortinet 硬體高度集中台灣代工（歷年約85–95%），並警示中台緊張可能影響台灣製造；ASIC/零件無保證產能或價格的長約，部分零件為單一或有限來源","source":"Fortinet Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"(“Western Digital”), are available from limited or sole sources of supply. We have no long-term contracts related to the manufacturing of our ASICs or other components that guarantee any capacity or pricing terms.","as_of":"2026-02-27","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K 列出代工夥伴（Accton、IBASE、MSI、Senao、Wistron）且其使用台灣與日本的 TSMC 等晶圓廠","source":"Fortinet Form 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203925000011/ftnt-20241231.htm","excerpt":"Our current manufacturing partners include Accton Technology (“Accton”), IBASE Technology, Inc. (“IBASE”), Micro-Star International Co. (“Micro-Star”), Senao Networks, Inc. (“Senao”), Wistron Corporation (“Wistron”), and a number of other manufacturers.","as_of":"2025-02-28","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收年增 20% 至 $2.08B；產品營收年增 37% 至 $765M；服務營收年增 13% 至 $1.31B；billings 年增 29% 至 $2.34B","source":"Fortinet Q3 2026 8-K press release / mfn.se","url":"https://mfn.se/all/a/fortinet/fortinet-reports-strong-third-quarter-2026-financial-results-52fcf7f0","excerpt":"Product revenue increased 37% and 43% during the three and nine months ended September 30, 2026","as_of":"2026-10-28","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"10-Q 稱產品營收成長主因硬體平均售價提高，及高效能安全網路產品與 AI 基礎設施部署需求；總毛利率因產品占比上升下降 1.8pp（Q3）","source":"Fortinet 10-Q Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001262039/000126203926000027/ftnt-20260930.htm","excerpt":"Total gross margin decreased 1.8 and 1.0 percentage points during the three and nine months ended September 30, 2026","as_of":"2026-10-28","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"服務營收成長 13%，管理層稱受大型企業部署時點影響，大型協議可能合併既有服務安排","source":"Fortinet Q3 2026 earnings coverage (panabee)","url":"https://www.panabee.com/news/fortinet-earnings-q3-2026","excerpt":"While service revenue grew 13%, management said the result was affected by timing related to large enterprise deployments.","as_of":"2026-10-28","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 營收指引 $8.125B–$8.215B，billings 指引年內第三度上調","source":"Fortinet Q3 2026 press release","url":"https://mfn.se/all/a/fortinet/fortinet-reports-strong-third-quarter-2026-financial-results-52fcf7f0","excerpt":"Revenue in the range of $8.125 billion to $8.215 billion","as_of":"2026-10-28","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Gartner 2026 資安支出約 $246.2B、成長 12.2%（固定匯率）；網路安全設備 2026 預測上修 $1.7B（次級部落格轉述）","source":"Software Strategies Blog, Gartner 2026 forecast","url":"https://softwarestrategiesblog.com/2026/04/01/top-10-fastest-growing-security-categories-gartner-2026-forecast/","excerpt":"Gartner’s $246.2B Security Forecast shows 10 categories growing 2x to 3x the market","as_of":"2026-04-01","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 2025 call：防火牆單位市佔 55%；CFO 稱設備漲價 5%–20%，同業提前拉貨避免漲價","source":"Fortinet Q4 2025 earnings call transcript (AOL)","url":"https://www.aol.com/articles/fortinet-ftnt-q4-2025-earnings-011419957.html","excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"Accelerate 2026：FortiOS 8.0 與漲價發布","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/fortinet-reaffirms-convergence-strategy-at-accelerate-2026-unveils-fortios-80-and-price-hikes-2026-03-16/?.tsrc=rss","excerpt":null,"as_of":"2026-03-16","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FTNT 10-K 自述：替代技術的發展與市場接受度可能降低產品需求或使產品過時；競爭對手可能推出更便宜或效能更佳的產品。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"The development and market acceptance of alternative technologies could decrease the demand for our products or render them obsolete. Our competitors may introduce products that are less costly, provide superior performance, are better marketed, or achieve greater market acceptance than our products.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Zacks：Fortinet 的 SASE Firewall 業務 2026 Q2 成長 34% 超過 $2B，競爭對手為 Palo Alto Networks 與 Zscaler。","source":"Zacks: Can Fortinet's SASE Momentum Propel the Stock to New Highs","url":"https://www.zacks.com/stock/news/3011142/can-fortinets-sase-momentum-propel-the-stock-to-new-highs","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：Fortinet 仍主要經兩層經銷模式銷售（經銷商→轉售商／服務商／MSSP→終端客戶），僅在特定情況直銷大型客戶；雲端訂閱另透過自有資料中心與公有雲提供。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"We primarily sell our products and services through a two-tier distribution model. We sell to distributors that sell to resellers and to service providers and managed security service providers (“MSSPs”), who, in turn, sell products and/or services to end-customers. In certain cases, we sell directly to large service providers, major systems integrators and large end users.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：產品組合含硬體、軟體授權、SaaS 訂閱與雲端交付方案，並透過雲服務商平台銷售軟體授權與雲交付服務。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm","excerpt":"We also sell our software licenses and cloud delivered services via different cloud service provider platforms, both directly and through our channel partners.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"專業經銷商 Climb 自 2025-12 起銷售 Fortinet，2026 目標含 SMB/中型市場經合作夥伴成長（通路擴張而非縮減）。","source":"Channel Insider: Climb & Fortinet Execs on New US Partnership, 2026 Goals","url":"https://www.channelinsider.com/security/climb-fortinet-distribution-partnership/","excerpt":"Climb & Fortinet Execs on New US Partnership, 2026 Goals Specialty distributor Climb and security vendor Fortinet announced their partnership in December 2025. The agreement brings Fortinet’s vast portfolio into the Climb vendor linecard and follows years-long demand globally for security solutions available through","as_of":"2026-02-26","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"服務與支援營收約佔 2025 年營收 70%（自約 48%），訂閱化轉型；並開始揭露 SASE 與 SecOps ARR。","source":"Zacks/Nasdaq: FTNT's Subscription-Based Services Gain Steam","url":"https://www.nasdaq.com/articles/ftnts-subscription-based-services-gain-steam-sign-more-upside","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 財報（約 2026-10-28）公司再上調 FY2026 營收 guidance 至 $8.125–$8.215B（約 +20% YoY），並稱今年第三次上調 billings guidance","source":"ITWire: Fortinet reports strong third quarter 2026 financial results","url":"https://itwire.com/guest-articles/company-news/fortinet-reports-strong-third-quarter-2026-financial-results","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 財報後（2026-07-29）FY2026 EPS guidance 上調至 $3.41–$3.47、營收 $8.0–$8.2B，高於事前共識（EPS 約 $3.08、營收約 $7.8B）；前次 guidance 為 EPS $3.10–$3.16、營收 $7.71–$7.87B","source":"MarketBeat: Fortinet updates FY 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/fortinet-nasdaqftnt-updates-fy-2026-earnings-guidance-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師共識評級為 Hold；各聚合站平均目標價分歧：Investing.com 約 $119.92（11 Buy/27 Hold/6 Sell）、stockhub 2026-07-16 平均 $115（區間約 $70–$215）、Walnut Invest 2026-08 平均 $159.51（37 位、中位 $165、11 Buy/29 Hold/4 Sell）","source":"Investing.com / stockhub.kr / Walnut Invest 聚合頁","url":"https://walnutinvest.com/stocks/ftnt/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 後賣方上調目標價：Susquehanna $115→$160、Citigroup $165→$185、Piper Sandler $110→$175（2026-07-30～31）；Zacks 稱共識估值上修約 13.51%","source":"Walnut Invest 目標價追蹤頁","url":"https://walnutinvest.com/stocks/ftnt/forecast","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"Fortinet 面臨證券集體訴訟 In re Fortinet Securities Litigation（N.D. Cal., 3:25-cv-08037），class period 2024-11-08 至 2025-08-06，指控誇大防火牆換機週期；合併訴狀 2026-04-24 提出，Union Asset Management Holding AG 為 lead plaintiff。","source":"BLB&G / Levi & Korsinsky 公告及合併訴狀","url":"https://static.blbglaw.com/docs/2026-04-24%20_%20Consolidated%20Class%20Action%20Complaint.pdf","excerpt":null,"as_of":"2026-04-24","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Fortinet 於 2026-08-17 宣布收購 Virtue AI（AI 執行期防護），金額未揭露、公司稱對業務不重大。","source":"chartmill 新聞：Fortinet Expands AI Security With Virtue AI","url":"https://www.chartmill.com/news/external/126052/fortinet-expands-ai-security-with-virtue-ai-can-growth-accelerate","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"SEC EDGAR 近12個月 6 份 8-K，含重大項目者 0 份。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001262039&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-08-17 宣布收購 Virtue AI，金額未揭露、稱不重大。","source":"chartmill","url":"https://www.chartmill.com/news/external/126052/fortinet-expands-ai-security-with-virtue-ai-can-growth-accelerate","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"In re Fortinet Securities Litigation（N.D. Cal. 3:25-cv-08037-AMO），class period 2024-11-08～2025-08-06；合併訴狀 2026-04-24。","source":"BLB&G 合併訴狀","url":"https://static.blbglaw.com/docs/2026-04-24%20_%20Consolidated%20Class%20Action%20Complaint.pdf","excerpt":null,"as_of":"2026-04-24","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"無實體產品召回；2026 年多份政府資安通報（加拿大 AV26-812 2026-08-12 涉 FortiClientWindows；新加坡 CSA AL-2026-024 高風險漏洞）屬漏洞警告。","source":"Canadian Centre for Cyber Security / CSA Singapore","url":"https://www.csa.gov.sg/alerts-and-advisories/alerts/al-2026-024/","excerpt":null,"as_of":"2026-08-12","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"FTNT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":80.04,"operating_margin_pct":32.66,"fcf_margin_pct":43.94,"rd_intensity_pct":11.1},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FTNT","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"PANW","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":70.36,"operating_margin_pct":6.05,"fcf_margin_pct":35.83,"rd_intensity_pct":22.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PANW","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"CRWD","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":75.25,"operating_margin_pct":-2.21,"fcf_margin_pct":28.22,"rd_intensity_pct":28.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWD","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"MSFT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.66,"operating_margin_pct":47.1,"fcf_margin_pct":17.31,"rd_intensity_pct":10.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"OKTA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":78.13,"operating_margin_pct":7.68,"fcf_margin_pct":31.21,"rd_intensity_pct":21.18},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.OKTA","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"FTNT"},"financial_history":{"ticker":"FTNT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":4417400000.0,"revenue_yoy_pct":null,"gross_margin_pct":75.44,"operating_margin_pct":21.95,"net_income":857300000.0,"diluted_eps":1.06,"free_cash_flow":1449400000.0,"fcf_margin_pct":32.81,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":5304800000.0,"revenue_yoy_pct":20.09,"gross_margin_pct":76.68,"operating_margin_pct":23.4,"net_income":1147800000.0,"diluted_eps":1.46,"free_cash_flow":1731400000.0,"fcf_margin_pct":32.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":5955800000.0,"revenue_yoy_pct":12.27,"gross_margin_pct":80.56,"operating_margin_pct":30.28,"net_income":1745200000.0,"diluted_eps":2.26,"free_cash_flow":1879200000.0,"fcf_margin_pct":31.55,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":6799600000.0,"revenue_yoy_pct":14.17,"gross_margin_pct":80.46,"operating_margin_pct":30.66,"net_income":1853400000.0,"diluted_eps":2.42,"free_cash_flow":2225800000.0,"fcf_margin_pct":32.73,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/FTNT/FTNT_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**Fortinet, Inc.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Hello, and welcome to Fortinet's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please be advised that this call is being recorded.
I would now like to hand the call over to Anthony Luscri, Vice President of Investor Relations. Please go ahead.

**Anthony Luscri** (Executives):
Thank you. Good afternoon, and thank you for joining us on today's conference call to discuss Fortinet's third quarter 2026 financial results. Joining me on today's call are Ken Xie, Fortinet's Founder, Chairman and CEO; Christiane Ohlgart, our CFO; and John Whittle, our COO. Ken will begin our call today by providing a high-level perspective on our business. Christiane will then review our financial results for the third quarter of 2026 before providing guidance for the fourth quarter and updating the full year. We will then open the call for questions. During the Q&A session, we ask that you please limit yourself to one question and one follow-up question to allow others to participate.
Before we begin, I'd like to remind everyone that on today's call, we will be making forward-looking statements, and these forward-looking statements are subject to risks and uncertainties, which could cause actual results to differ materially from those projected. Please refer to our SEC filings, in particular, the risk factors in our most recent Form 10-K and Form 10-Q for more information. All forward-looking statements reflect our opinions only as of the date of this presentation, and we undertake no obligation and specifically disclaim any obligation to update forward-looking statements.
Also, all references to financial metrics that we make on today's call are non-GAAP unless stated otherwise. Our GAAP results and GAAP to non-GAAP reconciliations are located in our earnings press release and in the presentation that accompany today's remarks, both of which are posted on our Investor Relations website. As a reminder, this is a live call that will be available for replay via webcast on our Investor Relations website. The prepared remarks will also be posted on the quarterly earnings section of our Investor Relations website following today's call. Lastly, all references to growth are on a year-over-year basis unless noted otherwise. 
I will turn the call over to Ken.

**Ken Xie** (Executives):
Thank you, Anthony, and thank you, everyone, for joining our call. We are pleased with our excellent third quarter results, driven by strong execution and broad-based demand. Billing grew 29%, while total revenue increased 20%, led by 37% growth in product revenue. Based on our continued strong momentum, we have raised our 2026 billing guidance for the third time this year. With the rapid evolution of the AI landscape, Fortinet is leading the next frontier of cybersecurity by securing AI workflow and protecting against AI-discovered vulnerability in real time through our core strength in network security. We believe that network security is the most critical foundation of AI security with the firewall serving as a centralized point of in-line enforcement across enterprise, operation technology and hybrid cloud environment.
Fortinet's leadership in this space is driven by over 20 years of innovation, integration and improvement as shown on Slide 7, while continually expanding our AI capability and functions in FortiOS and FortiGuard services. Fortinet secured 4 critical areas of infrastructure and AI security as shown on Slide 9. First, at the network level, our SASE firewall natively protect against vulnerabilities and stop intrusions, supporting shadow AI monitoring and access control to data and applications. To address growing demand, the newly launched FortiGuard Inline AI Security Services this week transform every FortiGate into a real-time AI enforcement point.
Second, in the data center and AI factories, we offer FortiAIGate to secure GPU clusters and LLM infrastructure securing the massive growth in AI traffic that require high-performance protection across data center and hybrid cloud. Third, we extend AI security together with SASE to endpoint, defining, controlling and integrating agent identity directly into access and incident response life cycle. And fourth, our SOC FortiAgent deliver a highly automated solution to solve the industry active skill shortage and tools loading by enabling autonomous incident detection and response.
Our SASE firewall pillar billing grew 31%, and we are the fastest-growing SASE firewall vendor and scale, growing and nearly double the market growth rate, as shown on Slide 5. Our leadership stems from a fundamental architectural advantage as we are the only vendor in the industry to build all the key SASE Firewall and AI Security components into a single and unified operation system, FortiOS. This new SASE firewall pillar represents a large high-growth area driving long-term growth, combined with our differentiated FortiASIC technology and own global infrastructure, this allows Fortinet to deliver better performance and significantly lower total cost of ownership, as shown on Slide 14.
We are also the only vendor offering an easily deployable on-premise sovereign SASE solution alongside cloud SASE, which we believe give us an addressable market 2 to 3x larger than the cloud-only competitors. To further capitalize on our large installed base, we recently launched FortiLink SASE services. This positions our FortiAP and FortiSwitch as a SASE hardware agent, allowing customers to easily overlay FortiSASE on top of their existing hardware, driving recurring service revenue.
As we look ahead, Fortinet's strong momentum is a result of our vision of FortiAI era, our platform integration and a highly disciplined operation model. This combination positions Fortinet exceptionally well to drive strong cash generation, high recurring revenue and consistent GAAP profitability while executing our shareholder-focused capital allocation strategy. I would like to thank our employees, customers, partners, and suppliers worldwide for their continued support and hard work.
I will now turn the call over to Christiane.

**Christiane Ohlgart** (Executives):
Thank you, Ken, and good afternoon, everyone. We delivered another exceptional quarter, exceeding the midpoint of our guidance across our key growth and profitability metrics, including billings, revenue, operating margin and earnings per share. Based on our strong momentum, we've raised our 2026 billings and revenue guidance. Total billings grew 29% to $2.34 billion, reflecting broad-based demand and strong execution across customer segments, industry verticals, geographies, and our integrated and innovative portfolio of solutions, further validating the strength of our platform strategy. AI, SASE and network upgrades and expansions are key growth drivers as customers prepare for new threat environments. We saw strong demand in large enterprises with the total value of deals greater than $1 million, growing 51%, driven by an outsized contribution from our U.S. large enterprise business.
SASE firewall billings grew 31% as sustained FortiGate demand was driven by enterprise customers turning to our network security solutions to upgrade their infrastructure for the era of AI and expand their Fortinet security footprint into operational technology and AI data center use cases. Our OT billings grew nearly 40%, validating our leadership in protecting mission-critical infrastructure. These achievements highlight our focus on leading growth and innovation in the durable demand drivers as we capture long-term expansion opportunities across emerging high-value use cases. Billings from AI-driven security operations grew 15%, driven by strong upsell momentum as our installed base increasingly consolidates point solutions onto our broader platform. 
Turning to revenue. Total revenue grew 20% to $2.08 billion with product revenue increasing 37% to $765 million, even though we saw increasing lead times for certain components. Strong product demand persisted throughout the quarter. As in the prior quarter, our product revenue benefited from customers shifting towards higher-performing models lifting ASPs. Service revenue grew 13% to $1.31 billion and faced some headwinds from winning new large enterprise customers with ramp service activations and large new expansion deals that also consolidated various existing service arrangements into enterprise agreements. We continue to believe the first quarter of 2026 marked the trough for our services revenue growth rate.
As shown on Slide 19, we have key leading indicators supporting a continued positive trajectory, specifically robust 26% service billings growth, 19% total deferred revenue growth and a 14.5% increase in short-term deferred revenue, which represents our highest growth rate in 5 quarters. In addition, we continue to roll out new AI Security Services, including the FortiGuard Inline AI Security Service announced this week. To put our overall performance in perspective, our sustained growth is being propelled by several fundamental shifts in how enterprises approach cybersecurity. We are witnessing a transformed threat landscape where bad actors aggressively use artificial intelligence to orchestrate rapid, highly targeted attacks. This shift has elevated security from a back-office IT concern to a board-level enterprise risk management priority accelerating investments.
Our third quarter results highlight our continued momentum and how our portfolio evolves with accelerated market shifts. Specifically, we are winning because of the convergence of networking and security, the urgent push to safeguard AI use and get ahead of increased threats enabled by AI, the merging of IT and OT domains and the rising global demand for sovereign compliant architectures. Sovereignty is especially prominent throughout European enterprises and the global public sector, matching our long-standing market leadership in those markets. In this environment, as enterprises scale their AI projects and experience the increased threat environment, they face the massive challenge of safeguarding proprietary data sets. This transition requires high-capacity security architectures that can inspect vast amounts of data accelerating traffic flows without degrading performance.
Rather than deploying disconnected point products that add friction, IT and security teams are actively looking for integrated platforms that offer centralized visibility and accelerated automated responses. Fortinet is strongly positioned to capture this demand by securing the physical AI data center, protecting distributed AI applications and embedding AI directly into our security operations. For example, an AI company developing frontier models, selected Fortinet for a 7-figure expansion to secure its rapidly growing AI workloads. This strategic win builds on the successful deployment of the customer's first AI data center last year. Driven by that initial success, a deep trusted relationship and the strength of our technology, the customer has standardized on Fortinet, deploying our high-end data center firewalls across 5 additional data centers.
Our solution addresses the challenge of protecting high-value AI workloads while maintaining maximum performance, availability and scalability as the infrastructure expands. This deal exemplifies the leading throughput and resilience of our platform, positioning Fortinet as a foundational security partner for the world's most demanding next-generation AI environments. This fast-changing threat environment has turned high-performance security into a structural necessity. Because enterprises and governments are highly aware of AI-powered attack vectors and expanding regulatory oversight, they are directing investments towards SASE firewall that can defend complex, decentralized environments.
To address these distinct operational and regulatory environments, Fortinet provides significant flexibility. By natively converging firewall, SASE and Hybrid Mesh capabilities into a single OS, we deliver a seamless way to protect people, customers, applications and sensitive assets across physical sites, cloud environments and remote teams. This flexible deployment model is a significant competitive advantage, allowing customers to build a SASE posture that matches their specific enterprise risks and regulatory requirements.
Turning to operational technology. Safeguarding the edge and industrial networks has become one of the most urgent issues discussed at Board levels of our customers today. Security boundaries have blurred, exposing critical supply chains, utility grids and manufacturing systems to unprecedented risk. Manufacturing has been the single most targeted sector for 5 consecutive years. Combined with escalating attacks on regional critical infrastructure, it is clear that historically underfunded OT environments are highly vulnerable. To mitigate this, organizations are rushing to segment their networks, shield unpatchable legacy machinery and establish secure remote access. With AI now arming attackers, these security decisions are being fast-tracked directly by corporate boards and leaders.
Fortinet's FortiOS platform enhanced by FortiGuard security subscriptions gives enterprises complete unified visibility over both their corporate IT and OT domains and a way to control the new attack surfaces AI creates. This architectural advantage is driving sustained demand across our specialized industrial portfolio. To illustrate, a large transportation company selected Fortinet in an 8-figure competitive win to secure its mission-critical OT infrastructure. The win was driven by the customers' need to modernize and secure its distributed environments through Fortinet's converged networking and security capabilities.
By consolidating firewall, secure routing, 5G connectivity and deep OT inspection into a single platform on one unified appliance, the customer is simplifying its overall network design while significantly improving operational resilience. This significant deployment highlights our leading ability to protect highly specialized demanding OT environments while delivering an optimized total cost of ownership and streamlined operational efficiency. Further proving our architectural advantage at the edge, a large U.S. retailer selected Fortinet in an 8-figure deal to standardize and secure its footprint for 1,500 store locations. The strategic win was driven by the customers' need to enhance network performance and digital resilience while wanting to offer an improved in-store customer experience.
To support its distributed operations, the retailer required a simplified network design and architectural standardization that allowed them to scale seamlessly while dramatically reducing overall costs. Fortinet's ability to deliver a comprehensive unified security fabric managed centrally via FortiManager proved to be a key differentiator. The successful competitive win of this large rollout demonstrates also the invaluable role of Fortinet's highly trained and specialized partner network, whose deep technical expertise is essential in deploying complex enterprise-grade solutions. Our exceptional quarter highlights our relentless focus on the dynamic market themes shaping the cybersecurity industry. We believe Fortinet's integrated platform approach positions us well to capture share, deliver sustained growth and maximize long-term shareholder value.
Turning to margins and cash flow. Non-GAAP and GAAP gross margins were 79.6% and 79%, respectively, and were impacted by the continuously high contribution of product demand. Non-GAAP operating margin of 38.2% was a third quarter record, up 130 basis points. This performance exceeded the high end of our guidance, driven by stronger-than-expected revenue growth and disciplined cost management. Moreover, our GAAP operating margin of 33.9% continues to be one of the highest in the industry. This strong operating performance translated to the bottom line. Non-GAAP earnings per share increased 23% to $0.91, while GAAP earnings per share grew 39% to $0.86, outpacing our top line growth, reflecting high-quality earnings supported by our long-term focus on total shareholder returns.
Free cash flow grew 52% to $865 million in the third quarter and 74% year-to-date to $2.84 billion, driven by higher billings and operating margin strength. Adjusted free cash flow was $912 million, representing an exceptional margin of 44%. Our excellent execution and consistent cash generation continue to support our strong financial position. Reflecting the strength of our balance sheet and our ongoing commitment to delivering long-term shareholder value, our Board of Directors approved an approximately $1.2 billion increase to our authorized stock repurchase program. This brings our remaining share repurchase authorization to $2 billion, giving us flexibility to continue returning capital to our shareholders while investing in our key growth pillars.
Now moving on to guidance. As a reminder, our fourth quarter and full year outlooks, which are summarized on Slides 24 and 25 are subject to the disclaimers regarding forward-looking information that was provided at the beginning of the call. Consistent with our disciplined and prudent approach to guidance, our strong performance through the first 9 months support a higher full year outlook. We are raising our full year guidance for billings and revenue as well as operating margin and earnings per share.
For the fourth quarter, we expect the following: billings in the range of $2.775 billion to $2.925 billion, which at the midpoint represents growth of 20%. Revenue in the range of $2.155 billion to $2.245 billion, which at the midpoint represents growth of 15%. Non-GAAP gross margin of 78% to 80%, non-GAAP operating margin of 35.5% to 37.5%. Non-GAAP earnings per share of $0.93 to $0.95, which assumes a share count between 741 million and 745 million. Infrastructure investments of $180 million to $210 million, a non-GAAP tax rate of 18% and cash taxes of $80 million to $130 million.
For the full year, we expect billings in the range of $9.568 billion to $9.718 billion, which at the midpoint represents growth of 28%. Revenue in the range of $8.125 billion to $8.215 billion, which at the midpoint represents growth of 20%. Service revenue in the range of $5.15 billion to $5.17 billion, which at the midpoint represents growth of 13%. Non-GAAP gross margin of 79.7% to 80.3%. Non-GAAP operating margin of 36.5% to 37.5%. Non-GAAP earnings per share of $3.54 to $3.58, which assumes a share count of between 741 million and 743 million. Infrastructure investments of $390 million to $420 million, non-GAAP tax rate of 18% and cash taxes of $400 million to $450 million.
Our current 2026 fiscal year guidance represents an increase for billings and revenue guidance by $1.14 billion and $570 million, respectively, compared to our initial 2026 guide in February. As we look ahead to 2027, we expect our total billings and revenue growth to outpace the growth of our overall addressable market. Our 2027 service revenue is expected to grow at a higher rate compared to 2026 as we consider short-term deferred revenue growth as a good indicator for future service revenue growth. In addition, we see continued pipeline building for SASE firewall use cases and expect that the new FortiGuard services will be highly relevant for existing and new customers. 
I will now hand the call back over to Anthony to begin the Q&A session.

**Anthony Luscri** (Executives):
Thank you, Christiane. As a reminder, during the Q&A session, we ask you to please limit yourself to 1 question and 1 follow-up question to allow others to participate. Operator, please open the line for questions.

**Operator** (Operator):
[Operator Instructions]
Our first question is from Shaul Eyal from TD Cowen.

**Shaul Eyal** (Analysts):
Congrats on the solid results all around. One for Ken, one for Christiane. Ken, can you talk about the criticality of network security, SASE firewall, SecOps? Or in other words, the overall Fortinet platform in the age of AI specifically. Where does Fortinet address AI use cases? How does this opportunity impact your growth rate and sustainability of demand? And maybe for Christiane, can you maybe double-click on the service revenue? You're adding new services. You provided an early view on improved growth in 2027. Talk about it in the context of the third quarter. Is this more of a timing issue on revenue given the leading indicators, all in all, look absolutely solid?

**Ken Xie** (Executives):
Thank you, Shaul. It's a great question. I actually prepared slides for that, on Slide 4. You can see we started calling it a SASE firewall because we believe SASE is a function, it will integrate with the traditional firewall OS and the same for the AI security. And like in my script, we believe network security is the most important part of AI security because they are the inline enforcer to a lot of AI traffic and also provide better visibility. So with our kind of leadership in the global network security market, we have like over half of the global unit deployment. We believe we have a much better visibility, and that gives us a lot of data, can train and make a better kind of SASE firewall model and at the same time, kind of innovate, keep up all the technology plus investing like ASIC. That's where we have the confidence we can grow faster than the market.
So that's where combine all this AI security, all the SASE, all the traditional security, we believe the total addressable market will grow about 16% in the current market growth rate. and we continue to grow faster. And last quarter, actually, we doubled -- almost doubled the market growth rate. And we've already become the biggest SASE firewall player in the space, and we continue to grow faster than the market. We feel it's still pretty big market, and we're keeping growth for a long, long time, just like we did in the last 20, 30 years. I think it's network security in the market position to address the AI security concern.

**Christiane Ohlgart** (Executives):
And let me follow up on your second question regarding services. So as I mentioned in the prepared remarks that we see strong services biddings. And so many of the indicators for service revenue improved. It's really a timing issue. And the strength in our enterprise segment, I think, is part of the reason that we see some delays in the conversion because we sold a number of really nice big deals and they have some ramped service activation. So it's a lot of strength in the business, plus we continue to focus on services, and this is where the newer services and solutions play, of course, a critical role to continue to upsell our existing customers. They -- of course, all our existing FortiGuard services are evolving, but the new FortiGuard Inline AI Service addresses some specific risks that are new with AI and that require constant FortiGuard updates. So it's going to be highly relevant to our customers.

**Operator** (Operator):
Our next question is from Saket Kalia from Barclays.

**Saket Kalia** (Analysts):
Ken and Christiane, maybe for both of you. This has been a very strong year for the product line. And of course, that's sort of a combination of a variety of different things, whether it's pricing or mix shift or volume. Now I realize it's early to talk about 2027. But based on what we see here in Q4, how should we sort of think about product growth next year given what is a very tough compare here in '26?

**Ken Xie** (Executives):
I think probably we're still 3 months early to give the '27 guidance, but we do have a confidence we will grow faster than the market, right? So if you look at the SASE firewall market, current growth rate is 16%, and we do believe we're keeping gaining market share there. And plus, we have pretty strong operation model. We kind of -- with our own ASIC chip, with our kind of manufacturer managed by ourselves, plus operation directly, we feel we have more advantage in this supply chain issue compared to most other competitors. So that's where we have confidence we're keeping gaining market share in this space with better technology, with a better operation and execution.

**Christiane Ohlgart** (Executives):
Yes. Let me add to what Ken said. If you look at the demand environment, the demand environment is pretty solid. The AI attacks are happening, not only the deployment of AI, it's also the threat environment that has increased quite significantly. And so that really drives the requirement for customers to upgrade their network security and of course, new use cases as well. So we are confident that we are well positioned for 2027.

**Saket Kalia** (Analysts):
Got it. Maybe for my follow-up, again, for you, Ken. One of the building blocks there that we hit on was pricing. I was wondering if you could just talk about your latest thoughts on pricing, right? I mean you've passed through the cost increases from memory. But maybe the question is, where are we in that journey? And of course, it's tough to have a crystal ball going into next year, but how do you think about that as a lever in 2027?

**Ken Xie** (Executives):
I think the price so far has about 10% benefit on the top line. On the other side, you can look at the first half of the year, we do benefit from our kind of on-hand inventory which we keep saying in the normal year, we keep about 6 months on-hand inventory. So that's where in the early phase of the supply chain, we kind of have a buffer we can benefit from. But now starting from Q3, we see this become more normal. So that's where we have to continue to source like others. And at the same time, even we have a bigger quantity, we have more direct relation.
But we do see the lead time get longer. I'd say the price probably stabilized, but not improved yet. I think the price increase kind of slowed down compared to the first -- Q1, Q2, Q3 kind of stabilized, but kind of not improving yet, still kind of slowly increase, but it's difficult to forecast going forward. Our policy -- our strategy always we want to keep in the same gross margin. And if our costs go higher, will increase accordingly. If our costs get lower, we also will decrease accordingly. So that's why we want to maintain the same gross margin on the product side. So that's the company's strategy in the last 20 years, actually.

**Operator** (Operator):
Our next question is from Gray Powell from BTIG.

**Gray Powell** (Analysts):
Great. So maybe just a higher-level question. A lot of the investors that we speak with, they're just trying to compare the current spending environment that you're seeing this year to kind of the post-COVID period like in 2021 and 2022. If I had to guess, the current AI-driven cycle is probably bigger. But the question is just how does it feel on your side relative to post-COVID a few years back or even the post-target era spending cycle that we saw in 2014 and 2015? And do you think that this cycle is more durable than past cycles?

**Ken Xie** (Executives):
I personally agree with you. I do feel these times are bigger than like 5, 6 years ago. And also now times more kind of work from -- remotely from home drive to some kind of supply chain, but now it's kind of AI built a lot of infrastructure kind of things there. But it's -- on the other side, AI also drive up the demand because now most recently, the AI security become a bigger concern, especially a lot of enterprise, how they're using AI, and that's also drive up the demand. So that's where we have not seen demand slowdown. So demand is still very strong in the last few quarters. And even in Q3, we have not seen any slowdown in the demand.
But supply, we mentioned the lead time get longer and also the price kind of not grow as fast as Q1, Q2, but still kind of go up a little bit, but I would say it stabilized somehow, that's probably more become normal, but we believe we have pretty strong operation and a direct relation with all the component manufacturer, which we can negotiate kind of compared to some of our competitors, much small quantity. So that's where we feel we still have more advantage.

**John Whittle** (Executives):
I think your point is also good that our business follows the threat. You mentioned the target breach, COVID, et cetera. This AI threat, no one has a crystal ball as someone mentioned earlier, just seems a lot more durable and sustainable in some of those earlier kind of threat drivers. And so I think it feels like early days. And like you said, our business does follow that threat and that threat environment is elevated, and it seems like it's durable.

**Operator** (Operator):
Our next question is from Rob Owens from Piper Sandler.

**Robbie Owens** (Analysts):
Great. And maybe dovetailing that last answer around the threat environment. Obviously, headlines have been somewhat scary, I guess, for the month of October relative to agentic and what's going on. Would just love to understand, I realize we're only 1 month into your fourth quarter here, but just how things are trending? Have they picked up much over the last month? And are there any -- is there anything you can quantify for us relative to, I guess, how the start of fourth quarter has looked given what's going on from a vulnerability perspective?

**Ken Xie** (Executives):
Yes. The demand is still very strong, and we don't see any slowdown. And there's definitely AI discovering more vulnerability, like all the PHP, some other, and we do believe our firewall in the best position to stop some of these attack intrusion, and we do have the signatures that can block some of these vulnerability, which is a very effective way to help in a lot of enterprise to defend it. And also, we see kind of also accelerate some of the convergence. So we do see more high-end unit being deployed inside the company to do internal segmentation. And also, we mentioned the sovereign AI, also we see pretty strong growth. And that's where we do believe long term, the hybrid AI, both sovereign and also cloud combination will be the best solution for customers, which we feel we have a huge advantage. I say that the demand is still very, very strong and no sign of slowdown.

**Operator** (Operator):
Our next question is from Meta Marshall from Morgan Stanley.

**Meta Marshall** (Analysts):
Great. A couple of questions for me. Noticed kind of the strong OT billings or OT security billings. Just are you seeing a broadening customer base there? Any kind of contextualization of how you see of any major new customers there? And then a second question, just in terms of -- are you running into your customers kind of having any issues of having the services or even the staff to kind of install a lot of the equipment? And is there anything you can do with your own services organization to kind of help those customers out or align them better with additional services that can help them with the installation?

**Christiane Ohlgart** (Executives):
Meta, let me take your questions. So on the OT side, I would say we've been strong in certain geos, and we are expanding that strength into other regions just because we have more and more customer references. They see the benefits of our specialized devices that we have for that. So it's a broadening of the strength and continued expansion because it's also becoming more and more relevant with the tech surface expanding.
On the installation side, so typically, Fortinet services are more on the configuration side, not necessarily on the racking and stacking. That's why we have an extensive reseller and partner channel that we qualify to do these things locally with our customers. I've not really heard that there is a shortage in the ability to roll out. I think that's more -- it's not the channel capability or capacity. It's more so how quickly can the customers do that. And that's always, I think, depending on the business you're in, in Q4, probably a little bit more challenging because many get ready for year-end business and so on, yes. So if you're a calendar year company, you don't make major changes until the next year.

**Ken Xie** (Executives):
Yes. Also, Fortinet kind of uniquely, we built our own kind of a service infrastructure system, we call the FortiCare, which now like half of the FortiCare service kind of can use AI to handle, to help in improving there. So that's also we started more have the service personnel local to customer, which also will be helpful to customer to like understand the additional new service we are launching now. So that's also we feel -- that's what helping drive the additional service business going forward.

**John Whittle** (Executives):
And Meta, I think to your question, I just talked to a retailer who's considering rolling out our solution to 4,000 stores around the country. And we're going to engage in MSP, like Christiane mentioned. But at that scale, we are seeing demand where they want to work directly with us. And so our service team can augment their service team and the MSP as well. And so we are seeing large-scale rollouts where the customer wants to work directly with us in addition to working with a partner.

**Operator** (Operator):
Our next question is from Adam Borg from Stifel.

**Adam Borg** (Analysts):
So maybe just to take a step back, we just talked about the really strong demand environment, continued pricing tailwinds, albeit less than in the first half of the year. Any more color on just what led to the growth deceleration in 3Q relative to 2Q is incredibly strong, but any color just what led to the deceleration across a number of the metrics?

**Ken Xie** (Executives):
Yes. Like I said, Q3, we see demand continued strong, probably even stronger than the first half of the year. And -- but the first half year, we do benefit from some kind of inventory we usually keep for 6 months. So that's where you see some strong product growth benefit from some of the inventory we have on hand. I think starting from Q3, we more treated as a normal now. So the on-hand inventory advantage kind of starting to disappear. But that's -- and also some of the components, we see a little bit longer lead time. But it's -- the demand side is still keeping growing.

**Adam Borg** (Analysts):
And just to clarify, are you saying that you are somewhat supply constrained? Or are you saying that the new inventory is at higher prices and that added element?

**Ken Xie** (Executives):
I'd say a little bit both. And also the lead time kind of gets a little bit longer to get some of the components.

**Operator** (Operator):
Our next question is from Joe Gallo from Jefferies.

**Joseph Gallo** (Analysts):
I've got a 2-parter on services. First, I understand the delayed ramp with some of these large ELAs. But when you remove that cohort, are you seeing the same attach rates as historical? I mean you obviously have a ton of product success right now, but is it fair to say that some of the networking strength and AI data center strength may be hurting the attach rates? And is there any reason to expect that to change?

**Christiane Ohlgart** (Executives):
There -- of course, over the years, there has been a little bit of a product mix shift towards networking components that we've been very strong in and part of the consolidation play, which have fewer attach rates. I think that's something that hasn't changed from Q2 to Q3. What we've been seeing is really good FortiGate growth. So that will help us with attach rates. On the other hand, compared to, let's say, our success with sovereign deployment or sovereign solutions, they are a little bit more product heavy compared to cloud solutions. So that's impacting the overall kind of product service mix a little bit as well.
But yes, there is product mix. Sovereign has less services because we are delivering more product that the customer has versus cloud solutions. And we believe that this will be structurally helping us with product long term because it's definitely an important trend. And then it's on us to attach more relevant FortiGuard security subscriptions. That's why it's so critical to roll these out.

**Joseph Gallo** (Analysts):
That's really helpful. And then maybe just a follow-up. Is there a discrete subscription selling motion? Or is that entirely attached to hardware? The reason I ask is just as product is cyclical and decelerates, service is obviously more important. So I'm just curious if there's any other tailwinds to subscription as we go through the cycle.

**Christiane Ohlgart** (Executives):
There is a separate services motion. The initial -- I would say, the initial purchase always attaches certain services. Most of the time, it's FortiCare and smaller customers buy services in a bundle. With larger enterprise customers, it is more of an upsell motion to make sure they roll-out the hardware first and then we are upselling on relevant security subscriptions. And that's why the focus, I think, is also on the increased threat environment because IPS, virtual patching, certain OT subscriptions are really critical for our customers to have the right level of intelligence circulating through the FortiGate all the time to be protected. So I think the motion will pick up quite significantly.

**Operator** (Operator):
Our next question is from Gabriela Borges from Goldman Sachs.

**Gabriela Borges** (Analysts):
Christiane, I want to stay on this topic of large enterprise deals and the impact that they're having to services revenue. Maybe just relative to your expectations, was U.S. enterprise stronger than what you expected? And then did you go from expecting it not to be a ramp deal and then the customers ask for it to be a ramp deal? Maybe just explain to us the dynamic that happened in 2Q because I don't recall you talking about large enterprise has been a growth driver for Fortinet for quite some time now. I don't recall the specific ramp issue impacting services before. So I'm just trying to understand what's different this time.

**Christiane Ohlgart** (Executives):
So I think Q3, as we reported, had a lot of not only large enterprise deals, which we had in the past, it had a lot of newer customers that had truly expansion deals and not necessarily just refresh activity or also sometimes it's large customers might have big renewals. So this is where as customers roll-out their infrastructure, they may not want to pay services right away, and we had more of that in Q3 also consolidating different activities. That's why I addressed it specifically in my prepared remarks.

**Gabriela Borges** (Analysts):
And so as it pertains to the 4Q guide, is it fair to say that you're also expecting the trend to continue, meaning the pipeline -- give us some color on how the pipeline looks for those types of new customers in that type of cohort. Do you think the services ramp dynamic is going to impact 4Q and maybe longer term as well?

**Christiane Ohlgart** (Executives):
I mean, it definitely has some impact on Q4. This is why you see our revenue guidance and respective adjustment of the 2026 service revenue guide. But the good news is the customers are buying services, which you can see in deferred revenue, which you can see in service billings. And there are more services to come. So we are actually happy with the strength in the business. It's just a little bit of a delay from when it gets recognized.

**Operator** (Operator):
Our next question is from Fatima Boolani from Citi.

**Fatima Boolani** (Analysts):
Ken, one for you and one for Christiane, please. Ken, in your comments earlier in response to a question around the product growth trajectory and some of what appears to be some supply side constraints, some increasing supply side constraints, but also sort of different and changing levels of inventory management. I'm wondering if at a high level, you can comment on how customers are behaving with respect to asset sweating, so sweating their appliances for a little bit longer in response to this or in anticipation of this? And why you are protecting or defending the business against that potential risk as all of us think about what the 2027 product growth trajectory is going to look like in the face of these -- some of these bigger picture macro factors? And then a follow-up for Christiane, please.

**Ken Xie** (Executives):
Yes. I think for the new security functions, especially like AI security, they need kind of more high end, more computing power to run all this function there. That's where we do see the move more towards the high end and also more computing power of FortiGate system. And that's where the ASP also go higher. We see usually the stretching size sometimes come from some low end of certain vertical like retail which they also kind of balance try to see whether they want to move to some kind of SASE or some other ZTNA environment. We do see some retail actually leading the change, but some other probably still try to hang on some of the products for longer.
But they also start to realize it's a new threat environment, and there's a lot of attack or vulnerability exposed by the AI. So that's where we feel probably customers more try to concern of this new vulnerability instead of try to stretch in some of the current existing hardware because if you're keeping the hardware like 5, 7, 10 years longer, a lot of function kind of difficult to run, kind of no longer supporting some of the new function there. So that's where we don't feel this stretching will be a trend going forward and because it's a new threat and the new demand for this function what will drive the additional growth.
But right now, we do see that the first wave more come from the enterprise and also especially some internal segmentation and some of the data center, AI and -- but once more application -- I mean, once AI starting getting more application, we do see there's additional demand will keep in drive the growth.

**Fatima Boolani** (Analysts):
Christiane, I want to touch on the gross margin performance. That compression, how do we reconcile the ASP uplift commentary, the commentary of customers trading up to higher-end models with presumably higher ASPs. Why is that essentially not following through into at least stable gross margins, because compression on the product side in spite of those factors was still pretty high. So wondering if you can kind of reconcile those 2 dynamics for us and how this should trend over the next 2 to 4 quarters?

**Christiane Ohlgart** (Executives):
So on the product gross margin side, we definitely see the increase -- so we had the benefit in the first half year that we had inventory on-hand. And so we had lower cost while we had already increased the prices. So that benefited our gross margin. In the second half, you see that the costs are creeping up and then impacting the product gross margin. But on the other hand, our service gross margin is picking up nicely. So it's offsetting some of the impact. There are -- you can only increase the prices so much, right, for your customers. They also have limited budgets. So we are trading a balance between increase of price and gaining market share. And I think we've done this quite successfully this year. So our -- I mean, the guidance for the overall gross margin remains at 80% for the full year, right, which was what we said at the beginning of the year.

**Operator** (Operator):
Our next question is from Junaid Siddiqui from Truist.

**Junaid Siddiqui** (Analysts):
Just regarding open-weight models, does this shift towards open-weight models by enterprises structurally expand your opportunity by moving more AI security into customer controlled infrastructure? And are you seeing that translate into incremental security demand yet?

**Ken Xie** (Executives):
Yes, we do see more enterprise running whether it's an open-source, open-weight model internally. And that also drive some additional demand for how to monitor and manage all this kind of AI model within the enterprise. So that's where there's more demand for enterprise network security. Like I said, it's kind of accelerating all this convergence of network-network security. And with our high-performance ASIC advantage, definitely, we feel we're leading in this area for like internal high-speed network security deployment for a lot of internal segmentation within the data center.

**Junaid Siddiqui** (Analysts):
Great. And just regarding the SASE bundles that you've rolled out, what are you seeing in early adoption? And what kind of pricing uplift are you seeing as customers move on to the bundle?

**Christiane Ohlgart** (Executives):
So the pricing uplift, I think, is about maybe -- so the question is how you define the pricing uplift, right? So FortiCare and SD-WAN is priced as a percent of the hardware price. And so the question is how much more are they buying? We see some uptick, but some customers are still using SD-WAN just what is provided through FortiCare versus the incremental subscriptions that we're offering. So it's going to take a little bit longer to really get it adopted by all our SD-WAN customers. So you see it more on the customers.

**Operator** (Operator):
Our next question is from Adam Tindle from Raymond James.

**Adam Tindle** (Analysts):
Ken, I just wanted to ask a question thinking about the business bigger picture. You're getting bigger customers like sovereign and neocloud that you talked about. Those are growing very, very fast and driving a ton of product growth, but disconnecting some of the services that we're talking about and stocks down a lot on this. So a 2-parter for you. I wonder if you might just opine on the pros and cons of servicing that customer base in the first place. Is that a good customer set to be servicing? And secondly, have you contemplated maybe even a different business model, almost like how chip companies serve that cohort that might be just much higher volume product and lower focus on service?

**Ken Xie** (Executives):
Actually, a lot of this bigger enterprise and also neoclouds, even some service provider, they probably need a little bit different service. And sometimes they also like offer some of their own service using our technology. So we become the Tier 2, Tier 3 behind. So that's probably -- and also, there's a ramp-up, like Christiane mentioned, a lot of this -- they first get hardware deployed and then they gradually keep adding service because we have so many functions, so many service in the FortiOS, they can use, they can leverage. And they do take time to ramp up a different kind of service.
So that's where we see and that's what Christiane mentioned sometimes. The good news, we do get a lot of bigger customers, but the other side is really the service need sometimes to ramp up, and gradually enable more and more service. And then there's also a way how to recognize once we have the call enterprise agreement, sometimes a little bit slower to recognize some of the service. But we do see the trend is pretty healthy, whether from the billing from the short term and the deferred revenue. So that's where we have the confidence.
But it's -- this being a customer also kind of give us a very strong feedback and what's the latest new kind of AI security needed, and that's kind of keeping drive our innovation, keeping developing new technology, working closely to making the whole Internet more secure.

**Adam Tindle** (Analysts):
If I could just a quick follow-up, Christiane. I imagine this might be the last question, so I want to give you the floor. The key question tomorrow is going to be why go out with the services expectation in fiscal '27 on this call. We're going to get a lot of questions on that. People are going to say, you told us that it was going to accelerate in the second half of this year. And obviously, we have not seen that materialize. So you're going even further out and talking about acceleration there. People are going to say that there's structural differences with the service attach rate and the new customers that you're seeing, a higher bar for fiscal '27. So I just want to give you the chance to take the floor here and give us some details on what's giving you confidence to talk about services acceleration in fiscal '27.

**Christiane Ohlgart** (Executives):
I would say I haven't used the word acceleration. I've used the word improved growth rates. So I mean, I think we clearly see that the growth rates have bottomed in Q1. The question is how quickly can we convert some of our service billings into revenue, right? And that always takes a little bit of time, but we are -- we continue to be confident that we are selling relevant services to our customers and that they convert into revenue over the course of 2027 and continue to grow.

**Operator** (Operator):
Our final question is from Patrick Colville from Scotiabank.

**Patrick Edwin Colville** (Analysts):
So I guess I just want to tie some of the pieces together from the last hour. The points you made are that large new customers side mandated in 3Q to have service agreements prior. They turn on slowly than you would expect that they guided 3 months ago. And that's what has caused the revenue miss and the billings miss, but the confidence I have is they are going to tell me, and that's why you are good value for the clients in 2027. Is that the message kind of interpreted correctly, or is there something about it?

**Christiane Ohlgart** (Executives):
Patrick, you're a little bit hard to understand, but I think I got the question. So let me summarize what -- Q3 was a good quarter. We had large new customers. We had large new expansion deals that benefited us. But they also -- they came with some of delayed service activation, which is actually typical in -- or happens more often in large deals. So overall, that was one bigger factor that we may not have as anticipated. There are, of course -- there's, of course, a lot of different aspects that you see in the service line. With the increase in prices, you see a little bit more discounting between hardware and services. And then also in the U.S., you definitely see a push towards hardware because it's benefiting customers from the tax perspective to depreciate. So there are different components that are not as prevalent in what happened in Q3, but there are trends that we've been seeing as we analyze where it was coming from.

**Patrick Edwin Colville** (Analysts):
And if I may, just, I guess, a very tactical question about channel inventory and billings duration. Would you mind just commenting on those 2 pieces?

**Christiane Ohlgart** (Executives):
Duration is still around -- still pretty similar. It didn't increase significantly. And our channel inventory is flat in percent of -- or down in percent of billings, yes. So we continue to manage the inventory in a way that we want the channel to have enough for the run rate business, but we don't want to overallocate so we have dislocation of inventory when we need it in different places. So that's where we are extremely diligent in managing how much we have in the channel.

**Operator** (Operator):
That was our final question. I will now hand it back to Anthony Luscri for closing remarks.

**Anthony Luscri** (Executives):
Thank you. One clarification to an earlier statement. Our pricing increases had around a 10 percentage point impact to year-over-year billings growth, not top line. But other than that, I'd like to thank everyone for joining today's call. We will be attending investor conferences hosted by BMO, UBS, and Barclays during the fourth quarter. The fireside chat webcast links will be posted in the Events and Presentations section of our Investor Relations website. If you have any follow-up questions, please feel free to contact me or my team. Have a great rest of your day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FTNT_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：CFO 給 Q3 billings 區間 22.5–23.5 億美元（原話："billings in the range of $2.25 billion to $2.35 billion"）
- 2026-07-29｜CFO｜guidance：CFO 給 Q3 營收區間 20.1–21 億美元（原話："Revenue in the range of $2.01 billion to $2.1 billion"）
- 2026-07-29｜CFO｜guidance：CFO 給全年營收區間 80.2–81.8 億美元（原話："Revenue in the range of $8.02 billion to $8.18 billion"）
- 2026-07-29｜CFO｜guidance：CFO 給全年 non-GAAP EPS 區間 3.41–3.47 美元（原話："per share of $3.41 to $3.47"）
- 2026-07-29｜CFO｜guidance：CFO 表示下半年管理方式為逐季（原話："the remainder of the year on a quarter-by-quarter basis"）
- 2026-07-29｜CFO｜guidance：CFO 仍預期下半年服務營收成長加速（原話："continue to expect service revenue growth to pick up"）
- 2026-07-29｜CFO｜margin：CFO 指引 non-GAAP 營業利益率 35% 起（Q3 與全年同）（原話："non-GAAP operating margin of 35%"）
- 2026-07-29｜CFO｜margin：CFO 報告 Q2 non-GAAP 營業利益率 38%，Q2 紀錄（原話："a second quarter record, up 490 basis points."）
- 2026-07-29｜CFO｜margin：CFO 說明營業利益率優於預期的驅動因素（原話："disciplined cost management and growing"）
- 2026-07-29｜CFO｜margin：CFO 提到內部 AI 使支援部門人數成長放緩、部分職缺不補（原話："significantly slower head count"）
- 2026-07-29｜CEO｜margin：Ken 說明調價以維持相同毛利率為目的（原話："maintain the same gross margin"）
- 2026-07-29｜CEO｜margin：Ken 稱記憶體價格近期趨穩（原話："memory price kind of stabilized in the last few weeks"）
- 2026-07-29｜CFO｜margin：CFO 回答漲價影響：下半年 billings 假設內含高個位數影響（原話："high single-digit impact built into our billings"）
- 2026-07-29｜CEO｜commitment：Ken 稱維持毛利率是公司政策（原話："want to maintain the same gross margin. That's the policy."）
- 2026-07-29｜CFO｜commitment：CFO 表示 2027 年數字將於明年 1–2 月提供（原話："numbers in January or February."）
- 2026-07-29｜CFO｜commitment：CFO 稱 2026 Q1 為服務營收成長率谷底（原話："marked the trough for our service revenue growth rate"）
- 2026-07-29｜CEO｜commitment：Ken 稱無過量庫存或提前拉貨，並說明 90 天後才開始收服務費（原話："we don't see any like excess inventory or pull forward"）
- 2026-07-29｜CFO｜product：Q2 總 billings 成長 33%（原話："Total billings grew 33% to $2.37 billion"）
- 2026-07-29｜CFO｜product：產品營收成長 52% 的拆解：FortiGate 單位數與 ASP 上升（原話："increase in ASPs as customers shifted towards"）
- 2026-07-29｜CFO｜product：服務營收與服務 billings 成長數字（原話："Service billings growth increased 26%"）
- 2026-07-29｜CEO｜product：Ken 提出「SASE Firewall」新口徑，把 secure networking 與 Unified SASE 合併（原話："to create what we are calling the SASE Firewall"）
- 2026-07-29｜CEO｜product：Ken 給出 SASE Firewall 業務規模與成長（原話："Fortinet SASE Firewall business grew 34% to over $2 billion"）
- 2026-07-29｜CEO｜product：Ken 說明合併口徑的原因：同一 OS 下難以區分 SASE 與 secure networking（原話："difficult to categorize whether it's a SASE deal"）
- 2026-07-29｜CFO｜product：OT billings 成長（原話："OT billings increased over 55%"）
- 2026-07-29｜CFO｜product：FortiSASE billings 成長（原話："FortiSASE billings growing over 100%"）
- 2026-07-29｜CEO｜product：Ken 談與 Intel 的合作（原話："partnership with Intel also very, very significant"）
- 2026-07-29｜CEO｜product：Ken 稱 SASE Firewall 可能是未來 5–10 年成長趨勢（原話："we see that the SASE Firewall could be the new trend to"）
- 2026-07-29｜CEO｜competition：Ken 稱地端主權 SASE 的可及市場是純雲端 SASE 的 2–3 倍（原話："approximately 2 to 3x larger than the cloud-only"）
- 2026-07-29｜CEO｜competition：Ken 稱對各大 SASE 競爭者持續贏單（原話："win SASE deal versus all of the top SASE competitors"）
- 2026-07-29｜CFO｜customer：新雲端業者 8 位數美元 AI 資料中心訂單（原話："Fortinet to secure AI data centers in an 8-figure win"）
- 2026-07-29｜CFO｜customer：全球藥廠 7 位數 FortiSASE 競爭替換案（原話："global pharmaceutical company signed a 7-figure FortiSASE"）
- 2026-07-29｜CFO｜capital_allocation：年初至今回購均價約 78 美元（原話："average price for repurchases this year of around $78"）
- 2026-07-29｜CFO｜capital_allocation：剩餘回購授權額度（原話："authorization as of today is approximately $766 million"）
- 2026-07-29｜CFO｜capital_allocation：Q2 自由現金流（原話："Free cash flow more than tripled year-over-year to"）
- 2026-07-29｜CEO｜risk：Ken 對 2027 年被問及時表示難預測、現在給數字太早（原話："little bit too early to give any number on the 2027"）

### 問答異常語氣（迴避／改口／保留）
- FTNT_Q2_2026_Earnings_Call_20260729.md｜問：Gabriela Borges（Goldman Sachs）問 2027 上半年產品營收成長的管線能見度與建模方向｜答法：Ken 稱難預測、現在給 2027 數字太早；CFO 只談主題會延續，數字留到明年 1–2 月，未給任何數字
- FTNT_Q2_2026_Earnings_Call_20260729.md｜問：Joe Gallo（Jefferies）問是否還有更多漲價｜答法：Ken 未直接回答是否再漲價，改說每月依成本調整、維持相同毛利率，並轉談 SASE Firewall 與 OT 才是更大的成長驅動
- FTNT_Q2_2026_Earnings_Call_20260729.md｜問：Gray Powell（U.S. Bank）問 Unified SASE ARR 加速主要來自 SD-WAN 還是 SSE｜答法：Ken 只給 FortiSASE 翻倍等方向性描述；CFO 僅答 ARR 成長來自附加與非附加服務，未拆出各元件數字
- FTNT_Q2_2026_Earnings_Call_20260729.md｜問：Meta Marshall（Morgan Stanley）問每座資料中心的 OT 附加率或占比｜答法：CFO 答視產業而定，未給比例；Ken 改談 AI 基礎建設初期先從公用設施等 OT 開始

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
{"date":"20260730","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"SASE Firewall 是真實的載體轉移，而非既有營收的重新貼標——單一 FortiOS 上的防火牆＋SD-WAN＋SASE 融合，帶動的替換需求大於原案 650,000 台刷新的有限波"},{"id":"H2","text":"服務營收的加速是已經預售完成的機械結果，不需要新的產品訂單來實現——遞延收入 $7,675.7M（+17%）與服務 billings +26% 對服務營收 +14% 的缺口，將在 FY2027 收斂"},{"id":"H3","text":"ASIC 成本優勢 ＋ 全額成本轉嫁政策，使非 GAAP OM 守在 35-38%、調整後 FCF margin ≥ 40%，即使 DRAM 成本翻倍"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"倍數正常化：44.4x NTM 對 19.6% 三年 CAGR，而 2027 年的成長率無人（含公司）願意承諾。共識均值目標價 $136、中位 $125、評等 hold（n=37），現價高於均值約 25%；後續目標價修正呈雙峰（TD Cowen $215／BofA $200 vs Barclays $155／Morgan Stanley 升評後仍僅 $133）"},{"id":"R2","text":"刷新原案已近尾聲、可見度隨之消失。2025-08-06 法說自陳「2026 升級週期完成 40-50%」；原案 650,000 台／2025-26 合計約 $400-450M 產品營收，而本季單季產品營收 $773M 已達原案兩年估計的約 1.8 倍——強度不可能主要來自原案，也就是說原本可用來承保 2027 的台數日曆已經不適用；2027 只剩約 350,000 台低階（低 ASP、公司自陳影響「小得多」）"},{"id":"R3","text":"單一 FortiOS 的單一故障面 ＋ 訴訟與地緣的三重未定價尾部。① CVE-2026-24858（FortiOS／FortiCloud SSO 認證繞過，CVSS 9.4）自 2026-01-20 起在已完整修補的 FortiGate 上遭實際利用，公司於 2026-01-26 全面關閉 FortiCloud SSO、次日改版重啟，CISA 於 2026-01-27 列入 KEV——同一個「單一作業系統」設計既製造護城河也製造同時受害的安裝基數；② 證券集體訴訟（N.D. Cal.，2025-09-22 起訴，類別期間 2024-11-08 至 2025-08-06，含 Oklahoma Firefighters Pension 為原告）標的正是刷新週期揭露，且指控 Ken Xie 與 Michael Xie 於 2025 年 8 月法說前數日出售股票；③ 中國 2026-01-14 國產替代指令永久關閉該市場切入點"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價格路徑：FY+2 口徑 32x（約 $131）。事件路徑（不需更低價）：2027-01~02 之 FY2027 初始指引 billings ≥ +15% 且產品營收 ≥ 0%，屆時上限＝當時 FY+2 EPS 的 36x（約 $183，推導見 §14b）。","irr_base_pct":2.9,"ev5y_pct":7.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":1.0,"ev5y_pct":7.5,"irr_base_pct":2.9,"max_dd_pct":-52.0,"bull_5y_price":273.0,"bear_5y_price":88.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"價格路徑：FY+2 口徑 32x（約 $131）。事件路徑（不需更低價）：2027-01~02 之 FY2027 初始指引 billings ≥ +15% 且產品營收 ≥ 0%，屆時上限＝當時 FY+2 EPS 的 36x（約 $183，推導見 §14b）。","price_at_dd":169.85,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTNT_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
