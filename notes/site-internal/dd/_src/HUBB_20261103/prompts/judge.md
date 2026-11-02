你是 stock-analyst **v20 判斷 agent**，標的 HUBB（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"HUBB","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBB_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBB_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":1872.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M（YoY +24.6%，其中 organic +11.3%、併購約 +13pp；QoQ +9.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）"},"note":"未取得"},{"id":"f_kpi1_adjusted_non_gaap_operat","label":"Adjusted (Non-GAAP) operating income / margin","value":25.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%（調整後營業利益 476.8 USD M；上年同期 23.9%，+160bps）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）；分部：Utility 26.0%（+30bps）、Electrical 24.8%（+400bps）"},"note":"未取得"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":21.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%（營業利益 408.7 USD M；上年同期 22.0%，-20bps）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）"},"note":"未取得"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":280.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M（營運現金流 322.6、資本支出 42.2；上年同期 253.8，YoY +10%；前九個月 539.2 vs 485.9）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）"},"note":"未取得"},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation（前九個月累計）","value":30.0,"period":"前九個月 FY2026（截至 2026-09-30，公告於 2026-10-27）","unit":"USD M（9M 累計；上年同期 27.0）。新聞稿未揭露單季 SBC 及九個月營業利益，故無法精確算占營業利益 %","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"前九個月 FY2026（截至 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）現金流量表"},"note":"不適用"},{"id":"f_kpi5_guidance_fy2026","label":"Guidance FY2026（本次上調）","value":"Adj. diluted EPS $20.40–$20.60；GAAP EPS $17.30–$17.50；總營收成長 18–19%；organic 10–11%","period":"Q3 FY2026（公告於 2026-10-27）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）；另載 adjusted tax rate 22.0–22.5%、FCF 約為 adj. 淨利 90%、重組約 $20M；未提供 Q4 單季指引與全年利益率目標"},"note":"媒體稱上調後僅與市場預期相當（TIKR，未驗證，不採為數字）；本站快照 FY1 EPS 共識 20.59（consensus_revision），落在區間內"},{"id":"f_kpi6_backlog_archetype","label":"Backlog（硬體/設備 archetype，僅定性）","value":"未揭露金額；管理層稱 orders 強勁、backlog 續增（continued backlog build）","period":"Q3 FY2026（公告於 2026-10-27）","unit":"定性","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 CEO 引言"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_hubb_gross_margin_pct","label":"HUBB 毛利率","value":35.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBB.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hubb_operating_margin_pct","label":"HUBB 營業利益率","value":20.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBB.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hubb_fcf_margin_pct","label":"HUBB FCF 利潤率","value":14.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBB.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_etn_gross_margin_pct","label":"ETN 毛利率","value":35.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_operating_margin_pct","label":"ETN 營業利益率","value":17.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_fcf_margin_pct","label":"ETN FCF 利潤率","value":13.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvt_gross_margin_pct","label":"NVT 毛利率","value":36.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvt_operating_margin_pct","label":"NVT 營業利益率","value":17.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvt_fcf_margin_pct","label":"NVT FCF 利潤率","value":11.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ayi_gross_margin_pct","label":"AYI 毛利率","value":50.64,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AYI.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ayi_operating_margin_pct","label":"AYI 營業利益率","value":15.89,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AYI.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ayi_fcf_margin_pct","label":"AYI FCF 利潤率","value":16.11,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AYI.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_abbn_sw_gross_margin_pct","label":"ABBN.SW 毛利率","value":40.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abbn_sw_operating_margin_pct","label":"ABBN.SW 營業利益率","value":17.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abbn_sw_fcf_margin_pct","label":"ABBN.SW FCF 利潤率","value":13.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":429.56,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-16.24,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":36.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.59 → 20.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.05 → 23.05）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（25.49 → 25.49）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":20.59,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":23.05,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":25.49,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.73,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 20.44 → 20.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":25.19,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝44.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":44.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.44,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝58.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":58.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.19,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝82.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":82.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":20.86,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 20.59，分子＝快照價 429.55","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.322,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":4951.6,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 5306.6、現金 355.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":52.84,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":27647.15,"period":"2026-11-03","unit":"USD m","basis":"市值 22695.55 ＋ 淨負債 4951.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6920.26,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":7682.7,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.0,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 432.91 / W52 476.49 / W104 438.92 / W250 345.74 / W250 13週斜率 1.19%"},{"id":"f_ma_w52","label":"52 週均線","value":476.49,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":438.92,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":345.74,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.19,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 稱 Hubbell 無法精確指出各產品類別的競爭者數量與相對市占，部分對手規模更大、資源更多；未點名新進入者。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":"Hubbell cannot specify with precision the number of competitors in each product category or their relative market position. However, some of its competitors are larger companies with substantial financial and other resources.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：競爭者行為與價格壓力可能使漲價無法完全抵銷成本；AI 等技術採用可能造成長期競爭劣勢。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":"Competitive pricing pressures may not allow us to offset some or all of our increased costs through pricing actions.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q2 2026 銷售約 +15%、有機約 +10%，管理層稱聚焦交叉銷售與新品搶份額。","source":"Webull/StockStory HUBB Q2 Deep Dive","url":"https://www.webull.com/news/15309608306697216","excerpt":"Management remains focused on capturing additional market share through cross-selling, new product development, and strategic vertical integration, stating, “We are confident in our ability to execute over the second half to deliver on a strong 2026 financial outlook.”","as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Hubbell 2026 SEC prospectus: Utility Solutions sales not believed materially dependent on any customer or group of customers, though substantial variability in utility purchases would affect the segment. No second-source/in-house event found.","source":"SEC Form 424B2 Hubbell 2026","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000119312526252576/d146732d424b2.htm","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Top ten customers account for approximately 42% of net sales (secondary source)","source":"Porter's Five Forces blog on Hubbell","url":"https://portersfiveforce.com/blogs/competitors/hubbell","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-K FY2025 揭露前十大客戶約占淨銷售 42%，不依賴單一客戶；風險因子提及客戶信用惡化、流失或降價壓力可能影響業績。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":"We are not dependent on a single customer, however, our top ten customers account for approximately 42% of our Net sales. Deterioration in the credit quality of, loss of, significant decline in business with, or pricing pressure from, one or more of our major customers could adversely affect our results of operations, financial condition and cash flows.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"財報附註 14：公司監控客戶信用，壞帳沖銷歷來極少。","source":"SEC EDGAR 10-K FY2025 Note 14","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":"As part of its ongoing procedures, the Company monitors the credit worthiness of its customers. Bad debt write-offs have historically been minimal.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Rystad 2026年5月底白皮書：北美與歐洲製造商的變壓器與高壓斷路器交期仍至少2~3年，預期價格與交期短期內維持高檔（二手摘要，非原文）","source":"pv magazine USA / Rystad Energy via search summary","url":"https://pv-magazine-usa.com/2026/05/11/u-s-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/","excerpt":null,"as_of":"2026-05-11","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"William Blair 2026-07-21 文章把電氣化描述為多年投資循環（搜尋摘要轉述）；多家來源稱變壓器短缺為多年結構性問題，成因含取向矽鋼、銅與產線排程","source":"William Blair, 3 forces powering the electrification opportunity","url":"https://im.williamblair.com/insights/articles/3-forces-powering-the-electrification-opportunity","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Eaton 投資3.4億美元於南卡羅來納變壓器廠，預計2027年投產；Wood Mackenzie 來源稱製造商擴產整體審慎（二手摘要）。Hitachi Energy 追加15億美元全球變壓器產能計畫目標2027年","source":"search summary; Manufacturing Dive (Hitachi Energy)","url":"https://www.manufacturingdive.com/news/hitachi-energy-expands-transformer-factories-pennsylvania-virginia-mexico/728188/","excerpt":null,"as_of":"2024-09-30","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Hubbell 2026Q2：銷售+15%至17.12億美元，調整後EPS+12%至5.52美元；資料中心銷售約+65%，全年預期約+50%；部分輸變電訂單已排入2027；管理層稱公用事業T&D處於多年投資循環早期；分析師質疑資料中心成長為週期或結構、及對聯邦基建支出的依賴","source":"MarketBeat / Nasdaq Hubbell Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/hubbell-q2-earnings-call-highlights-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"NEMA 2026年7月電氣產業信心指數六個月展望73.9，自76.3下滑但仍遠高於50榮枯線","source":"inside.lighting, survey industry confidence remains firm","url":"https://inside.lighting/news/26-08/survey-industry-confidence-remains-firm-july","excerpt":null,"as_of":"2026-08-11","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"GE Vernova高層稱需求「強勁且持久」，未履約訂單可能2027年初達2000億美元","source":"TechNews 科技新報","url":"https://finance.technews.tw/2026/09/17/ge-vernova-could-reach-200-billion-backlog-in-early-2027/","excerpt":null,"as_of":"2026-09-17","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Hubbell 於 2026-05-01 簽署以 30 億美元現金收購 NSI Industries 的股權購買協議，交割條件含 HSR 反壟斷等待期屆滿或終止；若因未取得反壟斷核准而終止須付終止費。","source":"SEC EDGAR 8-K（2026-05）NSI Industries 收購","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000119312526204099/d133302d8k.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"經查搜尋結果，未見 2026 年 DOJ／FTC 對 Hubbell 的反壟斷調查，亦未見 NSI 交易第二次要求（second request）的報導。","source":"WebSearch 結果彙總","url":null,"excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-Q 列示關稅、IEEPA 關稅退款、Pillar Two 為風險因素；無產業特定監管調查。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000162828026050405/hubb-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 風險因子：Hubbell 使用的鋼、鋁、銅及零組件、成品來自加拿大、中國、墨西哥與歐洲；進口關稅已或可能推高成本，並可能引發他國報復性關稅，影響需求與利潤。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":"We utilize materials (such as steel, aluminum and copper), components and finished goods that are sourced from or manufactured in foreign countries, including Canada, China, Mexico and countries in Europe. Import tariffs and potential additional import tariffs have resulted or may result in increased prices for these imported goods and materials","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 MD&A：2025 年毛利率擴張中，材料與其他成本通膨（含關稅費用）造成約三個百分點的收縮，被價格與生產力抵銷。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":"The increase in gross profit margin includes approximately four percentage points of margin expansion driven by favorable price realization, improved operational productivity, and lower acquisition-related intangible amortization expense, which was partially offset by three points of margin contraction due to material and other cost inflation, including tariff expense.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K FY2025 風險因子：出口管制與制裁法規可能限制出口或需出口許可，違規有罰則；一手文件未點名具體管制清單事件。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":"Moreover, any changes in export control or sanctions regulations may further restrict the export of our products or services, and the possibility of such changes requires constant monitoring to ensure we remain compliant.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Q3 2026 10-Q：當季營益率提升驅動因素包含淨關稅效益（net tariff benefit）。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000162828026067729/hubb-20260930.htm","excerpt":"impact of acquisitions and a net tariff benefit. The effect of those items was partially offset by margin contraction from material and other cost inflation. See the further discussion within Segment Results below. Global Trade Policy On February 20, 2026, the U.S. Supreme Court ruled that tariffs imposed under the International Emergency Economic Power Act (\"IEEPA\") exceeded presidential","as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Q3 2026 新聞稿前瞻聲明列示 IEEPA 關稅退款的時點與資格為不確定因素。","source":"SEC EDGAR 8-K Ex.99.1 2026-10-27","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000162828026067421/exhibit991_10272026.htm","excerpt":"the timing of and eligibility for anticipated additional International Emergency Economic Power Act (IEEPA) tariff refunds;","as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Hubbell 10-K FY2025 揭露：部分電子元件（螺線管、印刷電路板、IC 晶片、電源線組）來自數量有限的供應商；公司在多國製造與採購，供應中斷會影響營運結果（搜尋摘要為轉述，未取得逐字原文）","source":"Hubbell 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Hubbell 2026 年 10-Q 風險因素列出美國、中國、墨西哥間關稅與貿易措施不確定性，並提及 IEEPA 關稅退款時程","source":"Hubbell 10-Q Q3 2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000162828026067729/hubb-20260930.htm","excerpt":"International Emergency Economic Powers Act (\"IEEPA\") Tariffs On February 20, 2026, the U.S. Supreme Court issued a ruling in Learning Resources, Inc.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026: Electrical Solutions sales +51% to ~$845M (organic +22%, acquisitions ~29pts); data-center sales up >80% organically. FY2026 Electrical Solutions organic growth guided 17-18%.","source":"Hubbell 8-K Q3 2026 earnings release (Exhibit 99.1)","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000162828026067421/exhibit991_10272026.htm","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026: Utility Solutions sales +9% to $1,028M (organic ~5%); Grid Infrastructure ~+13%, Grid Automation ~-4%; ~$15M meter-component shortage shifted revenue to Q4. FY2026 Utility organic guide 6-7% (cut from 7-9% per one analysis).","source":"Hubbell 8-K Q3 2026 earnings release; MarketBeat Q3 call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-hubbell-q3-earnings-call-highlights-2026-10-27/","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Management expects data-center, electric T&D and renewable markets to remain strong in 2027; Utility backlog up >$500M YTD; heavy industrial markets relatively soft.","source":"MarketBeat Q3 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-hubbell-q3-earnings-call-highlights-2026-10-27/","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 call: recent price increases expected to add ~3-4% price realization for the year to offset input costs; no market share data found.","source":"Stock Taper HUBB Q2 2026 earnings call summary / Barchart","url":"https://stocktaper.com/earningsCallSummary/HUBB/2026/Q2","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"MIT Technology Review 報導 NYPA/EPRI 於 2026-08 測試 1MW 固態變壓器，開發商目前主攻資料中心，較高電壓應用仍需工程工作","source":"MIT Technology Review - solid state transformers","url":"https://technologyreview.com/2026/10/27/1147684/solid-state-transformers","excerpt":"But solid-state transformers can do much more. They absorb the jobs of devices like rectifiers and inverters (which convert AC to DC power and vice versa), shrinking the total footprint of the electrical equipment and potentially cutting the amount of power lost in the system. In August, the New York Power Authority and the Electric Power Research Institute (EPRI) tested a","as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 載明 Utility Solutions 產品主要經經銷商或直售公用事業；Electrical Solutions 主要經電氣／工業經銷商、家居賣場、零售五金及住宅導向網站銷售；十大客戶約占淨銷售 42%。未見通路結構轉變的陳述。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":"The products are sold into these markets primarily through distributors, or directly to utilities.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026 年 10-Q 載明 H1 2026 完成約 30 億美元收購 NSI Industries（電氣配件、連接器、線材管理），併入 Electrical Solutions；搜尋未見訂閱化或 D2C 等商業模式轉變的來源。","source":"SEC EDGAR 10-Q (period 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000162828026050405/hubb-20260630.htm","excerpt":"we completed the acquisition of NSI Industries for approximately $3.0 billion, net of cash acquired, subject to customary purchase price adjustments.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026（10/27）Hubbell 把 FY2026 調整後 EPS 指引由 20.25–20.55 上調至 20.40–20.60；中點僅升約 $0.10，而當季 beat $0.16，新中點與市場共識大致相當，股價當日跌約 6%","source":"TIKR: Hubbell Sinks 6% Despite Q3 Beat as Raised Outlook Only Matches Wall Street","url":"https://www.tikr.com/blog/hubbell-sinks-6-despite-q3-beat-as-raised-outlook-only-matches-wall-street","excerpt":"Hubbell beat the quarter by $0.16 a share but raised its full-year midpoint by just $0.10.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 公司上調全年展望，主因 Electrical Solutions 成長（資料中心）；NSI 併購整合優於原預期","source":"Hubbell 8-K Exhibit 99.1 (2026-10-27)","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000162828026067421/exhibit991_10272026.htm","excerpt":"We are raising our full year 2026 outlook, primarily driven by stronger anticipated Electrical Solutions growth.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2（7/28）指引 EPS 20.25–20.55 高於當時共識 19.98；營收指引 $6.8–6.9B 高於共識 $6.6B","source":"MarketBeat / aggregator via search: Hubbell updates FY2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/hubbell-nysehubb-updates-fy-2026-earnings-guidance-2026-07-28/","excerpt":"The company provided EPS guidance of 20.250-20.550 for the period, compared to the consensus estimate of 19.980.","as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill 顯示 FY2026 共識 EPS 20.88（19 位分析師，2026-10-17），近三個月 FY EPS 預估上修約 4%","source":"Chartmill HUBB estimates","url":"https://www.chartmill.com/stock/quote/HUBB/estimates","excerpt":"Latest recorded estimate: 20.88 USD · Oct 17, 2026 · 19 analysts","as_of":"2026-10-17","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布：Benzinga 14 位分析師均值 $504、高 $600、低 $325；另 Benzinga 價格頁 11 位 8 Buy/3 Hold 均值 $502；MarketBeat 共識 $554.38；各聚合站數字不一（FN2 均值約 $443）","source":"Benzinga HUBB sentiment / price-targets; MarketBeat","url":"https://www.benzinga.com/quote/HUBB/sentiment","excerpt":null,"as_of":"2026-09-02","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Morgan Stanley 2026-09-02 目標價調至 $575（Equal-Weight）；Baird 2026-08-21 以 Outperform、目標價 $550 啟動coverage","source":"Benzinga HUBB price targets (via search summary)","url":"https://www.benzinga.com/quote/HUBB/price-targets","excerpt":null,"as_of":"2026-09-02","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-05-01 簽訂股票購買協議，以 30 億美元現金收購 NSI Industries（電氣配件、連接器、線材管理產品），以現金加債務融資","source":"SEC EDGAR 8-K Item 1.01（2026-05-04）","url":"https://www.sec.gov/Archives/edgar/data/48898/000119312526204099/d133302d8k.htm","excerpt":"Hubbell agreed to pay an aggregate purchase price of $3.0 billion in cash, subject to customary adjustments related to cash, indebtedness, working capital and transaction expenses, as set forth in the Agreement. Hubbell anticipates that the Transaction will be financed with a combination of cash-on-hand and debt.","as_of":"2026-05-04","retrieved_at":"20261103","affects":["valuation","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-06-02 為併購融資發行三檔共 19 億美元優先債（5 億 2031、7 億 2033、7 億 2036），另有 9 億美元定期貸款協議","source":"SEC EDGAR 8-K Item 1.01（2026-06-08）","url":"https://www.sec.gov/Archives/edgar/data/48898/000119312526261758/d103727d8k.htm","excerpt":"relating to Hubbell’s public offering of $500,000,000 aggregate principal amount of its 4.650% Senior Notes due 2031 (the “2031 Notes”), $700,000,000 aggregate principal amount of its 4.900% Senior Notes due 2033 (the “2033 Notes”) and $700,000,000 aggregate principal amount of its 5.150% Senior Notes due 2036","as_of":"2026-06-08","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"NSI 收購於 2026-06-09 完成（搜尋摘要轉述 8-K 與 10-Q）","source":"SEC EDGAR 10-Q（2026-09-30）","url":"https://www.sec.gov/Archives/edgar/data/0000048898/000162828026067729/hubb-20260930.htm","excerpt":null,"as_of":"2026-06-09","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共 11 份，重大項目 6 份，皆與 NSI 收購及融資、債券發行相關；未見 4.02（財報不可信賴）或訴訟項目","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000048898&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 6 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-05-01 簽約以 30 億美元現金收購 NSI Industries","source":"SEC EDGAR 8-K Item 1.01（2026-05-04）","url":"https://www.sec.gov/Archives/edgar/data/48898/000119312526204099/d133302d8k.htm","excerpt":"Hubbell agreed to pay an aggregate purchase price of $3.0 billion in cash, subject to customary adjustments related to cash, indebtedness, working capital and transaction expenses, as set forth in the Agreement.","as_of":"2026-05-04","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"-","claim":"9 億美元無擔保定期貸款用於 NSI 收購融資","source":"SEC EDGAR 8-K Item 1.01（2026-05-15）","url":"https://www.sec.gov/Archives/edgar/data/48898/000119312526227142/d147999d8k.htm","excerpt":"The Term Loan Agreement provides Hubbell with the ability to borrow up to $900 million on an unsecured basis to finance the NSI Acquisition, repay certain existing indebtedness of NSI and pay fees, costs and expenses in connection with the foregoing.","as_of":"2026-05-15","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K 風險因子稱公司涉多項法律程序（產品責任、智財、環境），無法預測結果；搜尋未見 2024–2026 對 Hubbell 的證券集體訴訟","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm","excerpt":"We are a party to a number of legal proceedings and claims, including those involving product liability, intellectual property and environmental matters, which could be significant.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單未見 Item 4.02 或調查相關項目；搜尋僅見 2004–2005 舊 CFO 個人案件，與公司無關","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000048898&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 6 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"HUBB","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.36,"operating_margin_pct":20.21,"fcf_margin_pct":14.07,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBB","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ETN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.9,"operating_margin_pct":17.71,"fcf_margin_pct":13.1,"rd_intensity_pct":2.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"NVT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.97,"operating_margin_pct":17.1,"fcf_margin_pct":11.95,"rd_intensity_pct":1.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVT","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AYI","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.64,"operating_margin_pct":15.89,"fcf_margin_pct":16.11,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AYI","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ABBN.SW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":40.12,"operating_margin_pct":17.6,"fcf_margin_pct":13.29,"rd_intensity_pct":3.86},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"HUBB"},"financial_history":{"ticker":"HUBB","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":4947900000.0,"revenue_yoy_pct":null,"gross_margin_pct":29.74,"operating_margin_pct":14.33,"net_income":545900000.0,"diluted_eps":9.43,"free_cash_flow":453900000.0,"fcf_margin_pct":9.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":5372900000.0,"revenue_yoy_pct":8.59,"gross_margin_pct":34.93,"operating_margin_pct":19.12,"net_income":751400000.0,"diluted_eps":14.05,"free_cash_flow":715100000.0,"fcf_margin_pct":13.31,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":5628500000.0,"revenue_yoy_pct":4.76,"gross_margin_pct":33.86,"operating_margin_pct":19.42,"net_income":779000000.0,"diluted_eps":14.37,"free_cash_flow":810800000.0,"fcf_margin_pct":14.41,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5844600000.0,"revenue_yoy_pct":3.84,"gross_margin_pct":35.32,"operating_margin_pct":20.68,"net_income":887100000.0,"diluted_eps":16.54,"free_cash_flow":874700000.0,"fcf_margin_pct":14.97,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HUBB/HUBB_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**Hubbell Incorporated** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Thank you for standing by, and welcome to Hubbell's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] 
I would now like to hand the call over to Dan Innamorato, Investor Relations. Please go ahead.

**Daniel Innamorato** (Executives):
Thanks, operator. Good morning, everyone, and thank you for joining us. Earlier this morning, we issued a press release announcing our results for the third quarter of 2026. The press release and slides are posted to the Investors section of our website at Hubbell.com. I'm joined today by our Chairman, President and CEO, Gerben Bakker; and our CFO, Joe Capozzoli.  
Please note our comments this morning may include statements related to the expected future results of our company. These forward-looking statements as defined by the Private Securities Litigation Reform Act of 1995.
Please note the discussion of forward-looking statements in our press release and considered incorporated by reference into this call. Additionally, comments may also include non-GAAP financial measures. Those measures are reconciled to the comparable GAAP measures, which are included in the press release and slides.
Now let me turn the call over to Gerben.

**Gerben Bakker** (Executives):
Good morning, and thank you for joining us to discuss Hubbell's third quarter 2026 results. I will start my comments by summarizing 3 main themes we are seeing across the business in 2026. The first is that demand for Hubbell's critical infrastructure solutions remains strong. We see this clearly in our order book, year-to-date backlog build and in long-term planning discussions with our utility and electrical end customers. Second, we are proactively investing to serve this strong demand.
These investments have varying profiles across businesses, product lines and factory footprint. Some areas such as data center balance of system, electrical components and certain transmission and substation product categories are coming online quickly and are driving outperformance in 2026, while some investment in these same high-growth markets will enable us to serve longer-term visible project demand in 2027 and beyond. What is consistent across the capital investment program as a whole is a highly attractive return profile accretive to our overall ROIC which will enable us to grow our leading position in our core end markets over the next several years.
And finally, we are managing effectively through a dynamic supply chain and inflationary environment. While broad-based inflation persists, we continue to aggressively drive price and productivity actions across our portfolio. Our recent track record, our unique positions in our end markets and our visibility on actions taken and in progress give us confidence in our ability to continue to manage the price/cost productivity equation to neutral or better through the cycle.
Looking more specifically at the third quarter, Hubbell delivered strong financial performance with double-digit growth in sales, adjusted operating profit, adjusted earnings per share and free cash flow in the quarter as well as on a year-to-date basis. Third quarter performance was highlighted by 22% organic growth in Electrical Solutions, driven by data center sales increasing more than 80% in the quarter on an organic basis as well as continued progress on our segment unification efforts and vertical market strategy. The NSI acquisition is off to a strong start with performance and integration efforts trending ahead of our initial expectations. Utility Solutions results were solid in the quarter with strong core T&D performance offsetting a temporary component availability headwind in our meters business.
We are raising our full year 2026 outlook this morning, primarily driven by stronger growth outlook in the Electrical Solutions. As we look ahead to 2027, we see an attractive growth outlook across our largest, highest margin end markets, and I'll talk further about our preliminary views on next year at the end of this call. But now, let me turn the call over to Joe to provide some details on the third quarter.

**Joseph Capozzoli** (Executives):
Thank you, Gerben, and good morning, everyone. I am going to start my comments on Slide 4. Hubbell's overall financial performance was strong with double-digit growth across sales, adjusted operating profit, adjusted earnings per share and free cash flow, both in the quarter and on a year-to-date basis.
Net sales of $1.873 billion in the quarter increased by 25% as compared to the prior year. Organic growth of 11% was driven by robust 22% organic growth in Electrical Solutions and solid 5% organic growth in Utility Solutions. Acquisitions contributed 13% to growth in the quarter with NSI off to a strong start in the Electrical segment, as Gerben indicated, and DMC Power contributing nicely to our Utility segment.
From an operational standpoint, Hubbell generated $477 million of adjusted operating profit in the third quarter, representing 33% growth versus the prior year and delivered adjusted operating margins of 25.5%, representing 160 basis points of year-over-year expansion. Growth in adjusted operating profit was primarily driven by strong volume in high-margin businesses as well as the impact of acquisitions, which were accretive to adjusted operating margins.
Price/cost productivity was approximately neutral on a dollar basis in the third quarter, including the net impact of IEEPA tariff refunds. While broad-based cost inflation has persisted as 2026 has progressed, we have driven strong price and productivity realization over the last several quarters, and we are executing additional actions as we exit the year, which we are confident will position us well for 2027.
Adjusted earnings per diluted share were $5.91 in the third quarter. This represented a 14% increase versus the prior year, driven by adjusted operating profit growth and a modestly lower share count as a result of prior share repurchase activity, partially offset by higher interest expense associated with the NSI and DMC Power acquisitions and a higher year-over-year tax rate.
Free cash flow of $280 million was up 10% relative to the prior year. We continue to anticipate approximately 90% conversion of free cash flow to adjusted net income on a full year basis, which absorbs the impact from increased capital expenditures, acquisition costs and working capital investments to serve strong current and future sales growth.
Our balance sheet remains healthy, and we remain committed to deleveraging over the next 2 years, which will drive incremental adjusted EPS accretion in 2027 and position our strong balance sheet for further accretive M&A investment over the next few years.
Turning to Page 5 to review our performance by segment. Utility Solutions delivered 10% adjusted operating profit growth in the quarter and 9% sales growth, which was comprised of 5% organic growth and 4 points of contribution from the DMC Power acquisition. DMC Power's performance will be reflected in organic growth starting in the fourth quarter of 2026, which we anticipate will be accretive to the segment's organic growth rate.
Grid Infrastructure grew 8% organically in the third quarter, led by strong growth in distribution and transmission markets. Substation sales also grew strongly in the quarter, but modestly below our prior expectation, driven by timing of capacity expansion in our substation control house business. From a demand perspective, we continue to see broad-based order strength across substation, transmission and distribution markets, leading to further backlog build in the quarter as utility customers plan new projects supporting load growth and continue to invest in hardening and resiliency initiatives.
Grid Automation declined 4% organically in the third quarter, driven by a temporary component availability headwind in our meters business, which we anticipate will be resolved by the end of the fourth quarter and results in a shift of approximately $15 million in revenue from the third quarter into the fourth quarter. Protection & controls delivered strong double-digit growth in the quarter, led by continued strength in substation switching products where project interconnecting, load growth and recent capacity expansion investments are bolstering our performance.
Operationally, Utility Solutions delivered $267 million of adjusted operating profit in the third quarter, representing 10% growth versus the prior year, with adjusted operating margins up 30 basis points year-over-year. Adjusted operating profit growth was primarily driven by strong volume growth in high-margin businesses and acquisitions, while higher cost inflation and raw material costs were largely offset by price realization, productivity and a net tariff benefit in the quarter.
We also remain focused on executing and investing in capacity expansion initiatives to serve customer demand in high-growth areas of our Utility business, which we are confident will drive strong organic growth and deliver attractive returns on shareholder capital, both in the near term and over the next several years.
Moving to Page 6. Electrical Solutions results were very strong in the quarter. On the top line, Electrical Solutions generated net sales of $845 million, which represented growth of 51% versus the prior year and ahead of our prior expectation, driven by outperformance in both our organic business and in NSI. Starting with NSI, as we highlighted at the time of the acquisition, this business is a strong strategic fit with our portfolio and enables us to double down on our attractive core of critical infrastructure components with complementary products and brands, similar channels to market and clear opportunities for revenue and cost synergies. We are encouraged by the early integration efforts and strong performance with NSI contributing 29 points to the Electrical Solutions segment revenue growth in the third quarter at accretive adjusted operating margins.
From an organic revenue standpoint, 22% organic revenue growth was again highlighted by strength in data center and light industrial markets. Data center sales increased over 80% on an organic basis in the third quarter as content gains, new product introductions and capacity additions drove outgrowth in a strong underlying market. Most notably, our wiring device and Pin & Sleeve product lines have driven accelerated data center penetration through our vertical market strategy and recent product innovations and recent capacity investments in these areas are enabling us to capitalize on strong customer demand.
Outside of data center, light industrial markets remain strong, bolstered by U.S. manufacturing activity and electric T&D and renewables markets also grew strongly in the quarter. Nonresidential markets were solid in the quarter, while heavy industrial markets remained relatively soft. Across our HES portfolio, our initiatives around cross-selling and channel conversions have driven broad-based commercial success, and we see further opportunities to accelerate this strategy through the integration of NSI.
Operationally, Electrical Solutions delivered $210 million of adjusted operating profit in the third quarter, representing 80% growth versus the prior year and adjusted operating margins of 24.8% expanded 400 basis points year-over-year. Adjusted operating profit growth was driven by strong volume growth and the NSI acquisition, while higher cost inflation and raw material costs were largely offset by price realization, productivity and a net tariff benefit in the quarter.
Turning to Page 7 to discuss our full year outlook. We are raising our 2026 outlook this morning, driven by stronger sales growth and adjusted operating profit growth. On sales, we are raising our growth outlook to plus 18% to 19%, reflecting an increase in organic growth expectations to 10% to 11% and stronger NSI contribution now expected to contribute approximately 7.5% to full year sales growth.
Our increased organic growth expectations are driven by a stronger outlook in Electrical Solutions, which we now expect to grow 17% to 18% organically in 2026, while we have slightly lowered our outlook in Utility Solutions to plus 6% to 7% on a full year basis. Broadly, orders and end market demand have exceeded our expectations across our largest end markets in both segments as 2026 has progressed. The timing of project deployments and internal capacity expansions is driving stronger relative growth within Electrical Solutions segment near term.
Operationally, we anticipate over 20% year-over-year growth in adjusted operating profit on a full year basis at the midpoint of our outlook range, an increase versus our prior expectation driven largely by stronger volume growth, while the impact of incremental cost inflation, price and productivity actions results in an anticipated adjusted operating margin range of 23.0% to 23.2% for the full year.
Our expectations for below-the-line items remain unchanged and we continue to anticipate approximately 90% free cash flow conversion on adjusted net income on a full year basis, which includes the impact of elevated levels of inflation, increased year-over-year capital investment and NSI acquisition costs. We are raising our full year outlook for adjusted earnings per share to a range of $20.40 to $20.60. We are confident in our ability to deliver on this increased outlook in 2026, which represents year-over-year earnings growth of 12% to 13%.
Now let me turn the call back over to Gerben to give some preliminary views on our attractive 2027 setup.

**Gerben Bakker** (Executives):
Thanks, Joe. We see an attractive end market setup for Hubbell in 2027. Our standing long-term outlook targets mid-single-digit organic growth through the cycle. And as we have indicated throughout this year, everything we see in our end markets, order trends and conversations with customers has given us incremental confidence in the strength and duration of the long-term investment cycle ahead of us. Given the shorter cycle nature of many of our products, we intend to remain conservative as we update both our annual and long-term growth targets next year, but we will be exiting 2026 with stronger than typical backlog visibility, and we are confident in our ability to deliver an attractive year of organic growth in 2027.
In Utility Solutions, we continue to see broad-based strength across distribution, substation and transmission markets. Orders throughout 2026 have continued to exceed our initial expectations with particular strength in transmission and substation project activity driving backlog build in excess of $500 million year-to-date. We continue to believe utility T&D markets are in the early stages of an attractive multiyear investment cycle, driven by aging infrastructure and bolstered by load growth and data center interconnections. We have strong specified positions with our end customers, along with leading brands and installed base. And our primary focus as a management team is on executing the capacity expansion required to serve this broad-based demand for our utility customers. In our smaller end markets, we anticipate more modest growth in the approximately 20% of our portfolio exposed to gas, telecoms and meters and AMI.
In Electrical Solutions, we expect data center markets to remain strong in 2027, and we are confident in our ability to continue to drive outperformance through content gains, capacity initiatives and our vertical market strategy to capture more of our available balance of systems component opportunity. More broadly, conversations with distributor partners on large project activities have been constructive as electrification, U.S. reshoring and data center build-outs drive tailwinds across the broader industrial economy. We also anticipate continued strength in electric T&D and renewable markets in 2027, while our expectations for nonresidential and heavy industrial remain more modest.
Finally, I'll highlight that we expect the addition of NSI to further accelerate our strategy to compete collectively in HES with a broad portfolio of leading brands and critical infrastructure solutions, driving continued commercial success across our portfolio.
With that, we will turn the call over to Q&A.

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Steve Tusa with Wells Fargo.

**Charles Stephen Tusa** (Analysts):
Can you just provide a little bit of color, I guess, on just the '27 bridge dynamics? I know you guys gave the usual slide talking about the year forward, which looks like it implies something above your long-term algo, first of all. But then anything that you'd want to highlight moving forward on the bridge outside of obviously the tariff stuff?

**Joseph Capozzoli** (Executives):
Sure. Steve. So just a little more color on '27 bridge. So certainly, we'll provide a little more color as we get out into January on '27. But at this point, we've got a little more visibility than we typically would heading into '27 just given the incoming order rate, the backlog build. So we like the visibility into '27 at this point. And we're confident that '27 sees organic of at least our mid-single-digit standing long-term framework. So we feel really good about that. We're anticipating PCP to be in the neutral to dollar positive next year with incrementals in line with our long-term algo at 25% to 30%. So I'd say that's probably the anchor of the construct, Steve, for '27.

**Charles Stephen Tusa** (Analysts):
And do you have to go get more price between now and then to make that happen? Or are you pretty comfortable with the way things stand today?

**Joseph Capozzoli** (Executives):
So we are pricing -- accelerating price for '27 on the electrical side, pulling that forward into the fourth quarter here in November, and we'll be out at the end of the year or the beginning of the year with utility price. And that's generally for 2 key purposes. One is to address the cost inflation, the higher levels of inflation we've been seeing come through the last couple of months and also in line with our normal annual price increase cycle.

**Operator** (Operator):
Our next question comes from the line of Chad Dillard of Bernstein.

**Charles Albert Dillard** (Analysts):
I was hoping you could dig more into the guidance cut on utility. Can you talk through like what some of the sub segments drove the more conservative outlook?

**Gerben Bakker** (Executives):
Yes. I think 2 main things that are driving slightly below what we're expecting here in the third quarter. And as we look for the balance of this year. The first one is, as we highlighted, a component shortage that we had in our meters business. And this is a very discrete and unforeseen situation, and it has to do with our contract manufacturer of meters who was unable to source a component from a supplier that led to a production slowdown. And this took several weeks to resolve.
The good news is we're back in full production right now and looking to start that recovery -- have that recovery here in the first -- in the fourth quarter. So that was one.
The second one has to do with our substation and particularly the control houses in our substation market. This is our Systems Controls business. And if you look at this market in total, it represents about 20% of the HUS segment with about half being the components and half being this modular control house. And as a whole, this portfolio grew very attractively, I would say, in line with what transmission and distribution in the high single, low double digit.
And if you break that down, the components actually grew even better. This is stuff like connectors and bushings and arresters and switches, and that was in excess of 20% growth. And it's also areas where we've been successfully adding capacity here this year. We were expecting stronger growth in those control houses going from the first half to the second half. And this is a business that's grown very attractively over the last couple of years. We've been adding capacity and continue to add capacity, and that just proved a little harder here in the third quarter to continue to ramp that up. So as a result of continued growth, we were actually flat sequentially from the second quarter to the third quarter.
There's actions in place to continue to grow that, but it's just taken us a little bit longer. So I would expect this part to ramp up as we go into next year, but just at a little bit slow pace. So if you look at those 2 events, it's really what caused us to pull back a little bit on the organic growth this year. But I would say it's a really, really solid setup for next year as we continue to add capacity to our portfolio.

**Charles Albert Dillard** (Analysts):
Got you. That's super helpful. And maybe just on that capacity ramp point, can you give more detail in terms of just broadly across the whole business, the product lines? Any way to frame just like the revenue unlock as you go into '27? And then just timing and how much here you're investing to unlock that revenue?

**Gerben Bakker** (Executives):
Yes. Yes. And if you look at capacity broadly, I would put it in a few buckets. The primary bucket and where we're most adding capacity is what we've been talking about. It's adding the next machine, adding the next assembly line. We're a very SKU-broad company and portfolio. So generally, our capacity adds take that form. And if you think about Burndy connectors, if you think about the Pin & Sleeve where we've been able to grow 80%, it's adding more machines under existing roof line, similar to those components in the substation that I talked about. And that's the primary way that we add capacity still today.
The next level of capacity add is extending roof lines. And you can only keep adding so many machines before you run out of roof line. And so adding more roof line, adding more square footage around those existing factories is the next level, and we're seeing areas where we're doing that right now. Our Systems Control business is one of those that we're doing that as well.
So those are primarily the areas how we're adding capacity into our business. What we talked about this year is about $25 million a quarter of that additional capacity coming online, and that's to serve the growth that we're seeing in these markets. And as we look into next year, we anticipate that to about double to about $50 million per quarter as we go into next year.
So I would say our capacity adds have been very successful. The return on these projects, it's the highest returns we get of our investment. So we feel generally really, really good. And it's an area where we're focused as a management team to execute to serve this visible demand that we're seeing in our markets.

**Joseph Capozzoli** (Executives):
And Chad, I might just add a lot of that capacity going into key markets where we see durable, high growth, high margin, and that continues to be in transmission, substation and data center markets. So certain areas we've been adding as we go along, we were doing it last year, we're doing it this year, and you see that coming through in the data center growth rate in particular, but also happening in transmission, substation as well. So long term, a lot going on there, but really excited about the opportunities.

**Operator** (Operator):
Next question comes from the line of Julian Mitchell of JPMorgan.

**Chigusa Katoku** (Analysts):
This is Chigusa Katoku on for Julian. My first question is on the Q4 operating margins. I think they're implied down year-over-year in the guide. So is this at both segments? And can you just provide some color on what's the big headwind here?

**Joseph Capozzoli** (Executives):
Sure. So the margin impact is primarily you're seeing in Utility. And that is a couple of things, and we'll touch on each of these. First, we're seeing and anticipating price/cost productivity neutral in the fourth quarter in Utility. We are seeing higher levels of inflation come through in the back half year. We are seeing higher levels of price realization. The Utility business implemented price in July. And as they work their way through the backlog, that price realization is ramping up as the back half is progressing, and that is serving to offset that cost inflation that we're seeing. But it does have price -- it has an impact on the margin, just trading price cost dollars there.
Number two is we've got some investments. As Gerben was just talking about capacity expansion in key areas. Some of that is CapEx dollars. Some of it shows up in OpEx dollars, but really important that we're investing for our future in these growth initiatives. Some of that is also beyond CapEx and capacity is also targeted at new product introductions, and those new products are serving things like 765 and data center products and things of that nature. So investments are also included in there.
And then we also have some spillover. We talked about our expectations of IEEPA refunds coming through in the third quarter of about $30 million of refunds with about $10 million of partial offsets of customer considerations. And this kind of straddles 3Q. We did receive the $30 million of IEEPA refunds in the quarter as anticipated. And while we were expecting about $10 million of customer considerations and other, we realized about $5 million of that in 3Q and about $5 million of that is going to spill over into 4Q. So that's also part and parcel to that margin dynamic that you're seeing in Utility in the fourth quarter.

**Chigusa Katoku** (Analysts):
Okay. Just to be clear, Electrical is, you're expecting it to be up year-over-year or it's also down?

**Daniel Innamorato** (Executives):
Yes. I would say we haven't given by segment margin, but I think Electrical's got tailwinds from obviously, the NSI acquisition and then a lot of the same dynamics that Joe just outlined.

**Operator** (Operator):
Our next question comes from the line of Chris Glynn of Oppenheimer.

**Christopher Glynn** (Analysts):
A little bit on HUS. Curious on the $500 million or more of year-to-date backlog build, if that's pretty much all Grid Infrastructure. Curious if there's any kind of advance or green shoots at the Grid Automation besides the P&C. And also if there's any update on the high-voltage transmission sort of next-gen architectures.

**Gerben Bakker** (Executives):
Yes, Chris, it's in both areas of both Grid Infrastructure and Grid Automation that we're seeing that. And to give maybe some context to that, it's about up 30% from where we were at the beginning of the year, and this is what gives us more confidence as we go into 2027 with just higher visibility to some of that demand.
As far as the 765, it's an area that so far, we've been successful at. It's actually what we do for a living is the products that go into the transmission and substation for 765. We've been continuing to build that up to higher voltages over the years. So 765 is just a natural progression for us. We talked about in the past, having one project that will start shipping here as we go to the end of the year and into next year.
I'd say the pipeline for that is growing, and we have products that we're working with our customers with to specify. These are all specified products. So we feel really good. It does require investment, and Joe talked a little bit here in the fourth quarter. So before you can get these products up on the line, you're doing a lot of design testing on it. We have some of those capabilities in-house, but some also go to third parties. So there's an investment that's required to get these products specified and ready to go on the lines. But I would say that's progressing very well, and we believe over the next years, we'll benefit from those voltages coming online.

**Christopher Glynn** (Analysts):
Yes. Is that something that pulls your share even higher, or at least nominally, directionally?

**Gerben Bakker** (Executives):
Yes. I mean I don't know that it would be materially higher. I mean we're clearly very well positioned for it. I think if we look generally in these kind of materials, we're a leading supplier to the market in them and I would expect that to be similar here.

**Christopher Glynn** (Analysts):
Yes, makes sense. And then last one, just comments, latest thoughts on the fit for the Aclara portion of Grid Automation?

**Gerben Bakker** (Executives):
Yes. I would say, as we've talked in the past, this is a business that we've changed the direction in a little bit, focused on electric meters, muni, co-ops on the AMI side and the installed base of TWACS. We've taken structural cost out of this business. And from here, our expectations of it is to have more modest growth and improve the margins. And just as a reminder, this is less than 10% of HUS revenue exiting this year and well below that on an OP basis. So we would expect it to stabilize and drive less volatility going forward.

**Operator** (Operator):
Our next question comes from the line of Tommy Moll of Stephens.

**Thomas Moll** (Analysts):
Gerben, I wanted to start with a question on your Electrical Solutions margin approaching 25% for the quarter. You did call out NSI integration is ahead of plan, so that's got to be part of it. But if you pull that away, what other factors were favorable this quarter? And as we think toward next year, before we all put 25% in our model for 2027, is there any temporary benefit you had this quarter that we should be mindful may fall away going forward?

**Joseph Capozzoli** (Executives):
Tommy, so I would say the anchor of that margin performance in the quarter was strong organic volume contribution. And that strong volume is coming in key product lines, high-margin product lines that are serving data center in addition to the contribution, the nice contribution we were anticipating from NSI.
So certainly, third quarter is seasonally the strongest revenue and margin performance quarter of the year for us. We're very pleased with the margin performance of Electrical in the quarter. But certainly, this isn't the ongoing run rate performance. It certainly is the seasonal performance. But we do continue to see a strong margin in Electrical.
And Tommy, we've talked about this long-term margin expansion program that Mark Mikes and the Electrical segment team have been driving, which is really multifaceted and includes the segment unification strategy, our go-to-market strategy with our broad Electrical Solutions focused commercial team.
We've talked about portfolio management. We've talked about business simplification and management delayering and consolidation, new product intros in key areas. So a lot of variables driving this long-term margin expansion program through Electrical. And we really see us in the middle innings and continuing that margin expansion program. So while you are seeing a real strong third quarter margin, we think about it more broadly that the Electrical Solutions segment will continue to drive margin expansion in 2027 and beyond for all those reasons.

**Thomas Moll** (Analysts):
And as a follow-up, I wanted to ask about the capacity adds, particularly in your transmission and substation businesses. You noted that it should unlock some revenue for you into next year. But assuming that occurs, are you in that case, fully meeting the demand? Or should we still think of this as a capacity-constrained market?

**Gerben Bakker** (Executives):
Yes. I would say this -- I mean, this is not taken the form of you add a huge plant, you have an incremental step and then you're done or you're planning for multiyears out. I mean some areas of this market, if you think about some of the other equipment, that's exactly how you have to plan capacity add. For us, still the capacity adds are incremental even when we do roof line extensions. So it's a question of staying ahead of it.
So certainly, the capacity that we're adding next year isn't to solve for multiyear. We're going to have to continue to add capacity in '27 for '28, in '28 for '29. And we view that actually as a good thing because it limits you a little bit from getting too far ahead of yourself. But I would see it in that kind of construct of how we're thinking about capacity adds, multiyear.

**Operator** (Operator):
[Operator Instructions] Our next question comes from the line of Alexander Virgo of Evercore ISI.

**Alexander Virgo** (Analysts):
I wondered if you could just talk a little bit about 2 things for me. The first one, the $15 million in Grid Automation, if I adjust that back, it looks like automation was kind of flat year-on-year instead of building on something of the momentum that you saw in Q2 against an easier comp. So I'm just wondering why we should be feeling better about that as we go forward into next year.
And then secondly, the data center business, you obviously very strong and your comments on backlog are helpful and the ''27 sort of initial view is helpful. But obviously, a dark green arrow masks a lot of potential growth next year. So I wondered if you could just give us a little bit of a hand on what that might end up looking like in HES, again, in the interest of putting a sensible sort of number into the model to start with.

**Joseph Capozzoli** (Executives):
So yes, I'll start with your first question. That's a $15 million flip in Grid Automation and normalizing 3Q, 4Q, you're thinking about that the right way. And that $15 million flip would have been very consistent with our expectation for the back half 90 days ago. So just that movement from 3Q to 4Q normalizes the expectation of Grid Auto that would have been positive in the third quarter. And we're anticipating now with that $15 million falling into the fourth quarter that we see double-digit growth in Grid Auto in the fourth quarter because of it.
The second question on the data center business and the backlog. Certainly, data center has been really strong for our Electrical business. And we're anticipating that we exit the year with about 30 -- sorry, 15% of our Electrical segment revenues tied to data center. And we will provide more color and insight on our 2027 guidance on data center come January. But at this point, we're anticipating that data center continues to grow at very attractive levels in 2027 off of a higher base for us as we exit this year.

**Operator** (Operator):
I would now like to turn the conference back to Dan Innamorato for closing remarks. Sir?

**Daniel Innamorato** (Executives):
Great. Thanks, everybody, for joining us. I'll be around all day for follow-up calls.

**Operator** (Operator):
This concludes today's conference call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HUBB_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CEO Gerben Bakker｜guidance：CEO 宣布上調 2026 全年財測（原話："We are raising our full year 2026 guidance this morning"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年調整後 EPS 財測由 19.30–19.85 上調至 20.25–20.55（原話："from a range of $19.30 to $19.85 to a range of $20.25"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年調整後營業利益率財測 23.1%–23.4%（原話："we anticipate adjusted operating margins of 23.1% to 23.4%"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年銷售成長財測由 +8–11% 上調至 +16–18%（含 NSI 5 點）（原話："plus 8% to 11% to plus 16% to 18%"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Utility Solutions 有機成長財測上調至 +7–9%（原話："Utility Solutions organic growth outlook to plus 7% to 9%"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Electrical Solutions 有機成長財測上調至 +12–14%（原話："growth outlook to plus 12% to 14%, driven by our increased"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年資料中心成長預期約 50%（原話："approximately 50% for the full year"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：財測含 $20M 價格成本淨效益，主要來自 IEEPA 退款（原話："net benefit of $20 million"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年淨利息費用 $1.7 億，來自 NSI 借款（原話："increased net interest expense of $170 million"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Q3 調整後稅率預期較高約 24%（原話："rate of approximately 24% in the third quarter"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：FCF 轉換率未來幾年約維持 90%（原話："pacing around 90% for the next couple of years"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Grid Infrastructure 全年營收約雙位數成長，Q4 基期較高（原話："Grid Infrastructure revenue pacing around double digits"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Utility 下半年有機成長預期較上半年小幅改善（原話："where we expect organic growth to improve"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：Q2 Electrical 調整後營業利益率 21.2%，年減 130bps（原話："operating margins of 21.2% were down 130 basis points"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：Q2 Electrical 利潤率受約 60bps 較高重組投資影響（原話："60 basis points of higher restructuring investment"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：利潤率橋：淨關稅 30bps、NSI 40bps（原話："30 bps from net tariff, the 40 bps on NSI squares up"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：下半年利潤率擴張預期偏 Q3 較集中（關稅退款）（原話："it is going to be a little more front-loaded"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：關稅效益約一半一半分攤 Electrical 與 Utility（原話："we would split that roughly half and half between electrical"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：IEEPA 退款全數預期落在 Q3（原話："the refund we're anticipating in the guide is all in the"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：Q2 價格/生產力與成本通膨（原話："productivity actions are keeping pace"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：重組：下半年仍偏重（原話："pretty heavily loaded with restructuring-related"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：全年重組約 $2,000 萬，上半年已花過半（原話："million of restructuring related in the full year"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：價格：4 月調價後 7 月再度追加，全年約 3–4 點（原話："3 to 4 points for the full year"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：管理層稱關稅變動影響小、環境仍通膨（原話："nothing of any substance one way or another"）
- 2026-07-28｜CEO Gerben Bakker｜risk：管理層稱環境仍屬高通膨（原話："it's still a very inflationary environment"）
- 2026-07-28｜CEO Gerben Bakker｜risk：Transmission/substation Q2 偏低歸因專案時點（原話："there's really nothing to read into this beyond"）
- 2026-07-28｜CFO Joe Capozzoli｜risk：非住宅市場：不確定是否持續加速（原話："We're a little cautious to say that that's going to"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：Electrical 下半年（Q3、Q4）利潤率回到擴張（原話："we do see electrical margin returning to expansion"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：未來 24–30 個月降槓桿還債（原話："pay down significant portions of debt and deleverage"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：資本配置：股利成長與小額回購（原話："dividend growth and modest share repurchases"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：NSI 預期 2026 EPS 增益約 $0.20（原話："adjusted earnings accretion of approximately $0.20 in 2026"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：NSI 銷售協同 2–3%（原話："2% to 3% sales synergies from increased channel"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：NSI 成本協同 3–5%（原話："approximately 3% to 5% cost synergies from leveraging"）
- 2026-07-28｜CEO Gerben Bakker｜commitment：預告投資人日時間地點（原話："Centralia, Missouri, on March 4, 2027"）
- 2026-07-28｜CFO Joe Capozzoli｜capital_allocation：NSI 收購後預估槓桿約 2.9x（原話："leverage moves to approximately 2.9x net debt to EBITDA"）
- 2026-07-28｜CFO Joe Capozzoli｜capital_allocation：2026 CapEx 預估 $175–190M（原話："roughly $175 million to $190 million of CapEx"）
- 2026-07-28｜CFO Joe Capozzoli｜capital_allocation：CapEx 占營收提高至 2.5–3%（原話："we're now pacing at 2.5% to 3% of sales"）
- 2026-07-28｜CFO Joe Capozzoli｜capital_allocation：每季新增約 $25M 產能（原話："bringing on roughly $25 million of new capacity-ish"）
- 2026-07-28｜CFO Joe Capozzoli｜customer：Utility 上半年 book-to-bill 約 1.2x（原話："first half book-to-bill ratio of approximately 1.2x"）
- 2026-07-28｜CEO Gerben Bakker｜customer：訂單開始排入 2027（輸配電）（原話："We are seeing orders starting to be booked into 2027"）
- 2026-07-28｜CFO Joe Capozzoli｜customer：Q2 資料中心銷售約 +65%（原話："Data center sales were up approximately 65%"）
- 2026-07-28｜CEO Gerben Bakker｜customer：配電成長部分反映去庫存後低基期（原話："the comps are still somewhat easy to lap"）
- 2026-07-28｜CEO Gerben Bakker｜customer：配電長期預期為中個位數以上市場（原話："for this to be a mid-single-digit plus market"）
- 2026-07-28｜CEO Gerben Bakker｜customer：Aclara 於 muni/co-op 專案流改善（原話："particularly in the muni and co-op space"）
- 2026-07-28｜CFO Joe Capozzoli｜customer：資料中心 content 增加稱「more of the same」（原話："I would call it more of the same"）
- 2026-07-28｜CEO Gerben Bakker｜product：高壓：首個 765kV 訂單 2027 開始出貨（原話："will start shipping in '27"）
- 2026-07-28｜CEO Gerben Bakker｜product：高壓傳輸機會約 $15 億/10 年（原話："about $1.5 billion opportunity over the next 10 years"）
- 2026-07-28｜CEO Gerben Bakker｜product：該機會約帶來 1 點額外成長（原話："it's about 1 point of additional growth"）
- 2026-07-28｜CEO Gerben Bakker｜product：新 Pin & Sleeve 產品面向 800V 基礎設施（原話："our new Pin & Sleeve devices"）
- 2026-07-28｜CFO Joe Capozzoli｜product：Grid Automation 回到年增（原話："we were pleased to return to year-over-year growth"）
- 2026-07-28｜CEO Gerben Bakker｜competition：報價量約兩年前兩倍（原話："about doubled in the last couple of years"）
- 2026-07-28｜CEO Gerben Bakker｜competition：大型專案勝率與過往相近（原話："similar to what we've seen traditionally"）
- 2026-07-28｜CEO Gerben Bakker｜competition：管理層稱在輸配電市場為領導地位（原話："leading position with the installed base, with spec position"）
- 2026-07-28｜CEO Gerben Bakker｜competition：模組化/捆綁趨勢（原話："absolutely a trend going on where you're bundling more"）

### 問答異常語氣（迴避／改口／保留）
- HUBB_Q2_2026_Earnings_Call_20260728.md｜問：Nigel Coe：扣除 Q3 關稅退款後 Electrical 利潤率是否仍擴張｜答法：IR 回覆「hard to reconcile right now」並請會後再談，未給答案
- HUBB_Q2_2026_Earnings_Call_20260728.md｜問：Alexander Virgo：1.2x book-to-bill 約 $2.4B 中多少會在下半年交貨｜答法：CEO 稱「hard to exactly do all the math」，只給定性說法（短週期、部分排入 2027），未給拆分數字

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
{"date":"20260518","verdict":"A（核心候選進場，Fwd PE 22x 5Y 分位 0% + post-earnings -13% drop 創 5 年難得 entry，是 PWR 同 thesis 便宜替代品）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Utility Solutions（特別是 Grid Infrastructure）持續 mid-to-high single-digit 組織成長","columns":{"2Y 驗證點":"Q2-Q4 26：Grid Infrastructure YoY ≥ 10%","5Y 驗證點":"2027-30：Utility Solutions 段營收從 FY25 $3.7B 至 $5.5-6.0B（mgmt 7-9% 組織 CAGR + bolt-on）","10Y 驗證點":"2030-34：765kV ultra-HV 顯著貢獻（mgmt $1.5B 10Y opportunity 兌現 50%+）","數字門檻":"Grid Infrastructure YoY ≥ 8%（2Y）","來源":"Q1 26 法說 4/30/26 + StockStory 整理","漂移觸發":"連 2 季 YoY &lt; 5% → 削弱；連 3 季 &lt; 2% → 反轉"}},{"id":"H2","text":"Adj OPM 維持並擴張至 FY26 22.7%+ → FY28-30 23-24%","columns":{"2Y 驗證點":"FY26 Adj OPM ≥ 22.7%（mgmt 大約 +20bps 中位）","5Y 驗證點":"FY28 Adj OPM ≥ 23%；FY30 Adj OPM 23.5-24%","10Y 驗證點":"長期 24% 區間穩定","數字門檻":"Adj OPM 連 4 季 ≥ 22.5%（2Y）","來源":"FY25 法說 + Q1 26 法說","漂移觸發":"連 4 季 TTM Adj OPM &lt; 21.5% → 削弱；連 6 季 &lt; 20.5% → 反轉"}},{"id":"H3","text":"Data center 段（Electrical Solutions 內）持續 20%+ YoY 成長","columns":{"2Y 驗證點":"FY26 data center growth 25%+（mgmt 已上修）；連 4 季 ≥ 20%","5Y 驗證點":"FY28-30：data center 段年化 15-20% 成長","10Y 驗證點":"長期 data center segment 占 Electrical Solutions 50%+","數字門檻":"Data center QoQ growth ≥ 5% 連 4 季","來源":"Q1 26 mgmt 法說、Hubbell investor presentation 2026","漂移觸發":"連 2 季 data center YoY &lt; 15% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"大型 utility 客戶 capex 推遲 1-2 季","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"季度 Grid Infrastructure 揭露 + utility capex commentary","警戒閾值":"Grid Infrastructure YoY 連 2 季 &lt; 5%"}},{"id":"R2","text":"Systems Control 整合 margin 拖累 — Aclara 2018-20 重演 dilutive period","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Utility Solutions 段 Adj OPM TTM trend / Systems Control segment 貢獻揭露","警戒閾值":"Utility Solutions Adj OPM 連 4 季 &lt; 20%"}},{"id":"R3","text":"Data center 段 cycle peak / hyperscaler capex 結構性 plateau","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"每季 data center growth 揭露 / hyperscaler combined capex consensus","警戒閾值":"Data center YoY 連 2 季 &lt; 20%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":479.97,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBB_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
