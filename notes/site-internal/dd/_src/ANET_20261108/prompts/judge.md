你是 stock-analyst **v20 判斷 agent**，標的 ANET（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ANET","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":3657.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"},"note":"consensus 約 $3.31B（來源：web_search／earningswhispers，次級來源）；公司 Q3 指引 $3.3B"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":1795.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD million；margin 49.1%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":1642.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD million；margin 44.9%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_kpi3_gaap_gross_margin","label":"GAAP gross margin","value":63.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_kpi4_non_gaap_diluted_eps","label":"Non-GAAP diluted EPS","value":1.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"},"note":"consensus 約 $1.08（web_search 次級來源）"},{"id":"f_kpi5_gaap_diluted_eps","label":"GAAP diluted EPS","value":1.22,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_kpi6_stock_based_compensation","label":"Stock-based compensation（占 GAAP 營業利益 8.4%；占營收 3.8%）","value":138.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_kpi7_free_cash_flow","label":"Free cash flow（僅有前九月，單季未揭露）","value":3792.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD million（9M 2026：營業現金流 3,977.4 − 資本支出 184.9）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_kpi8_deferred_revenue","label":"Deferred revenue（流動＋非流動）","value":6839.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD million（流動 5,102.2；非流動 1,737.3）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_kpi9_q4_fy2026_guidance_reven","label":"Q4 FY2026 guidance：revenue","value":"3900～4000","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_kpi10_q4_fy2026_guidance_non_g","label":"Q4 FY2026 guidance：non-GAAP operating margin","value":"48～49","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_kpi11_q4_fy2026_guidance_non_g","label":"Q4 FY2026 guidance：non-GAAP diluted EPS","value":"1.26～1.3","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-03","period":"2026-11-03","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_anet_gross_margin_pct","label":"ANET 毛利率","value":62.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ANET.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_anet_operating_margin_pct","label":"ANET 營業利益率","value":43.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ANET.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_anet_fcf_margin_pct","label":"ANET FCF 利潤率","value":42.2,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ANET.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_csco_gross_margin_pct","label":"CSCO 毛利率","value":64.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSCO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_csco_operating_margin_pct","label":"CSCO 營業利益率","value":25.36,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSCO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_csco_fcf_margin_pct","label":"CSCO FCF 利潤率","value":20.16,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSCO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_hpe_gross_margin_pct","label":"HPE 毛利率","value":36.73,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HPE.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_hpe_operating_margin_pct","label":"HPE 營業利益率","value":7.84,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HPE.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_hpe_fcf_margin_pct","label":"HPE FCF 利潤率","value":9.93,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HPE.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cien_gross_margin_pct","label":"CIEN 毛利率","value":44.07,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cien_operating_margin_pct","label":"CIEN 營業利益率","value":14.12,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cien_fcf_margin_pct","label":"CIEN FCF 利潤率","value":13.53,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cls_gross_margin_pct","label":"CLS 毛利率","value":11.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cls_operating_margin_pct","label":"CLS 營業利益率","value":8.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cls_fcf_margin_pct","label":"CLS FCF 利潤率","value":2.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":170.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":20.48,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":43.36,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-1.38,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.34 → 4.28）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":4.44,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.4 → 5.64）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":4.33,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.7 → 6.99）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":4.28,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":5.64,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":6.99,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.14,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 4.11 → 4.28（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":45.79,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝76.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":76.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":18.15,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝77.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":77.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":16.94,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝70.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":70.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":39.91,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 4.28，分子＝快照價 170.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-14359.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 0.0、現金 14359.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1263.4,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":201430.13,"period":"2026-11-08","unit":"USD m","basis":"市值 215789.13 ＋ 淨負債 -14359.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":13383.87,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":18699.44,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":15.05,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 170.8 / W52 157.84 / W104 134.3 / W250 84.89 / W250 13週斜率 2.7%"},{"id":"f_ma_w52","label":"52 週均線","value":157.84,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":134.3,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":84.89,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.7,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 列出競爭對手：Cisco 長期主導，另有 Dell/EMC、Extreme、HPE（已收購 Juniper）、Huawei、Nvidia 與白牌廠商；並指新進入者與替代技術可能造成降價壓力。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"The arrival of new market entrants and the rapid adoption of alternative technologies may create downward pricing pressure. Such shifts could result in lost sales and materially harm our operating results and financial condition.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：競爭已造成降價壓力、可能損失份額；AI Ethernet 產品需與較成熟的 InfiniBand 及他廠 AI Ethernet 競爭，品牌認知尚未廣泛建立。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"In addition, we have not established broad market awareness or acceptance of our AI Ethernet products that will compete against more established InfiniBand products or against the AI Ethernet products of other competitors.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"IDC：1Q26 Nvidia 成為資料中心乙太網路交換器營收第一，Arista 資料中心份額 20.7%","source":"IDC Markets and Trends 2026-06-17","url":"https://www.idc.com/resource-center/blog/nvidia-becomes-1-in-datacenter-ethernet-switching-as-1q26-market-surges-39-8-to-15-4-billion/","excerpt":"NVIDIA’s Spectrum-X platform, an end-to-end AI networking solution that integrates Spectrum Ethernet switches with BlueField DPUs and NVIDIA LinkX cables, purpose-built for large-scale GPU clusters, has emerged as the preferred network interconnect for large-scale AI training, winning significant traction with hyperscalers and AI-native cloud providers building AI factories. Arista","as_of":"2026-06-17","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"IDC：2Q26 Arista 資料中心份額 18.7%、整體 13.4%；Nvidia 20.4%","source":"IDC Markets and Trends 2026-09-11","url":"https://www.idc.com/?p=120278","excerpt":"Arista Networks: Arista’s revenues grew 37.6% YoY in 2Q26 to $2.5B, per IDC, with the company holding a 13.4% share of the total Ethernet switch market and 18.7% in the datacenter segment.","as_of":"2026-09-11","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Meta 與 Nvidia 簽多年 Spectrum-X 乙太網路部署合約，Arista 股價下跌","source":"rallies.ai","url":"https://rallies.ai/news/arista-shares-drop-29-after-meta-nvidia-multi-year-spectrum-x-networking-deal","excerpt":"Arista Shares Drop 2.9% After Meta-Nvidia Multi-Year Spectrum-X Networking Deal - ANET News | Rallies","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：大型系統廠商越來越多提供垂直整合的雲端網路方案，作為 Arista 產品的替代；white box 網路廠商（開源 OS）列為競爭者。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"Moreover, large system vendors are increasingly seeking to deliver vertically integrated cloud networking solutions to customers that combine cloud-focused hardware and software solutions as an alternative to our products.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Next Platform 報導：Microsoft 與 Meta 並非獨家向 Arista 採購交換器，並促使 Arista 支援其 SONiC 與 FBOSS 網路作業系統（多供應商）。","source":"The Next Platform, The current AI networking wave will be a tsunami of money by 2027","url":"https://www.nextplatform.com/2026/02/13/the-current-ai-networking-wave-will-be-a-tsunami-of-money-by-2027/","excerpt":null,"as_of":"2026-02-13","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 兩大終端客戶占營收 26% 與 16%（合計 42%）；FY2024 為 20%／15%，FY2023 為 18%／21%。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"Sales to one end customer represented 16%, 15% and 21% of our total revenue, and sales to the other end customer represented 26%, 20% and 18% of our total revenue for the years ended December 31, 2025, 2024 and 2023, respectively.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"公司自述客戶集中度與下單時點每季/每年會波動；前兩大經銷商占 2025 年底應收帳款 52%（2024 年底 50%）。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"As of December 31, 2025, and 2024, our top two resellers accounted for 52% and 50% of total accounts receivable, respectively.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"S&P 2026-10-30 將 Meta 評等展望調為負面（AA- 維持），理由為資本支出與租賃推升槓桿。","source":"ppc.land: Meta faces S&P downgrade as 2027 AI capex forecast tops 225bn","url":"https://ppc.land/meta-faces-s-p-downgrade-as-2027-ai-capex-forecast-tops-225bn/","excerpt":"What: S&P revised Meta's outlook to negative from stable and affirmed its AA- rating. It now forecasts capital expenditure of more than $225 billion in 2027 and $252 billion in 2028, free operating cash flow deficits of $22 billion, $71 billion and $39 billion in 2026 to 2028, and adjusted leverage of 1.1x in 2027 and 1.3x in 2028, above its 1.0x downgrade threshold, driven mainly by data","as_of":"2026-10-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Arista 2027 AI networking target約 7 十億美元（約為 2026 的兩倍）；Q3 2026 財報後發布","source":"247wallst: Arista Says Its AI Business Will Double to $7 Billion","url":"https://247wallst.com/investing/2026/11/04/arista-says-its-ai-business-will-double-to-7-billion/","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q2 call 上 CFO 稱客戶需求能見度約兩季，預測以有把握取得的供給為基礎","source":"MarketBeat Arista Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/arista-networks-q2-earnings-call-highlights-2026-08-04/","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"業界分析稱記憶體供需缺口為結構性，2027 可能惡化並延續至 2028；製造商優先供應 AI 基建而非傳統網通硬體","source":"Alpha-Sense: AI memory super cycle; telecomcauliffe: chip shortages expected through 2027","url":"https://www.alpha-sense.com/resources/research-articles/ai-memory-super-cycle/","excerpt":"The current supply-demand gap is structural rather than cyclical, and shortages are not approaching near-term resolution.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Arista 2027 outlook 約 18.5B（單一 SEC 分析站）","source":"sec-api.io Q3 2026 earnings and FY2027 outlook","url":"https://sec-api.io/insights/arista-networks-anet-q3-2026-earnings-and-fy2027-outlook-sec-filing-analysis","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K FY2025 風險因素僅泛稱可能收到政府機關詢問並導致正式調查，未點名任何針對 Arista 的反壟斷調查；搜尋亦未見 2026 年 DOJ／FTC／EU 對 ANET 的調查。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"From time to time, we may receive inquiries from governmental agencies, or we may make voluntary disclosures regarding our compliance with applicable governmental regulations or requirements relating to various matters, including import/export controls, federal securities laws and tax laws and regulations which could lead to formal investigations.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 揭露：美國自2025年2月起依IEEPA及Section 232等授權加徵關稅，另有對中國的Section 301關稅；關稅成本可能無法完全轉嫁，供應鏈調整未必成功。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"Since February 2025, the U.S. has also imposed additional country-specific tariffs on most trading partners, including China, as well as additional commodity-specific tariffs on certain imported items, in both instances pursuant to executive orders issued under various trade authorities, including the International Emergency Economic Powers Act and Section 232 of the Trade Expansion Act of 1962.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 揭露：產品含加密技術，出口須政府授權；中國對鍺、鎵等材料實施出口管制（2025年5月起部分放寬），可能影響元件採購與成本。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"Our products are subject to various export controls and because we incorporate encryption technology into certain of our products, certain of our products may be exported from various countries only with government authorization.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"最新10-Q（2026Q3）稱若關稅或非關稅措施升級，毛利率可能進一步受影響；產品營業成本含運費與關稅。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000254/anet-20260930.htm","excerpt":"If tariff or non-tariff measures escalate,","as_of":"2026-10-30","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Arista 製造全數外包，合約製造夥伴在馬來西亞、越南、墨西哥生產；關稅與非關稅貿易措施涉及美、墨、中等可能影響零件供應","source":"Arista 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653225000028/anet-20241231.htm","excerpt":"We subcontract the manufacturing of the majority of our products to various contract manufacturers. Our primary manufacturing partners are Jabil Inc., Sanmina Corporation, Flex Ltd. and Foxconn Hon Hai. These partners manufacture our products internationally in Malaysia, Vietnam, Mexico and other countries.","as_of":"2025-02-20","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Arista 對 Broadcom 交換晶片高度依賴，且與零件供應商通常無書面供貨保證、無關鍵零件獨家權","source":"Arista 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653225000028/anet-20241231.htm","excerpt":"In particular, we are primarily reliant upon our predominant merchant silicon vendor, 9 Table of Contents Broadcom, for our switching chips. Generally, neither we nor our contract manufacturers have a written agreement with these component providers to guarantee the supply of the key components used in our products, nor do we have exclusive rights to such key","as_of":"2025-02-20","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q3 2026 10-Q 列台灣為可能對通訊設備加徵關稅/非關稅壁壘的政府之一","source":"Arista 10-Q Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000254/anet-20260930.htm","excerpt":"to significant uncertainty about the future relationship between the U.S., and other countries, with respect to tariffs and trade policies. The U.S., China, Malaysia, Vietnam, Mexico, Taiwan, Thailand, the Philippines and other governments may place additional tariffs and non-tariff trade barriers on communication equipment products, our products and services, our inputs, or other items, which","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收約 $3.66B，年增 58.5%、季增 20.5%；Q4 指引 $3.9–4.0B","source":"Arista Q3 2026 earnings release (SEC 8-K ex99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 AI 目標 $3.5B+、campus $1.25B+（Q3 前指引）；2027 指引成長 38–40%（中點約 $18.5B），AI 預期約倍增至 $7B、campus 約 $2B，高於 Street 約 $16.15–16.75B","source":"TIKR / 247WallSt / Finviz 報導 Q3 2026 財報","url":"https://www.tikr.com/blog/arista-soars-6-on-18-5-billion-2027-outlook-after-quarter-surpassing-even-my-high-expectations","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"IDC：2Q26 Arista 資料中心乙太網交換器份額 18.7%（1Q26 為 20.7%），營收約 $2.5B、年增 37.6%；NVIDIA 同季 20.4%，1Q26 起居資料中心乙太網交換器營收第一","source":"IDC Worldwide Ethernet Switch tracker 部落格/新聞稿","url":"https://www.idc.com/resource-center/blog/nvidia-becomes-1-in-datacenter-ethernet-switching-as-1q26-market-surges-39-8-to-15-4-billion/","excerpt":null,"as_of":"2026-09-11","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 自述：新進者與客戶正開發基於開源 NOS 的白盒網通產品，或採拆解式採購搭配自有軟體，替代技術快速被採用可能造成降價壓力、流失銷售。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"Some of these entities are developing white box networking products based on open-source network operating systems that may be provided for free using off-the-shelf or commoditized hardware technology","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：若無法預期技術變化並及時推出新產品，產品可能過時；800GbE AI 乙太網產品能否維持競爭力取決於交付時程與客戶接受度。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"If we are unable to anticipate technological changes in our industry by introducing new, enhanced or expanded products and services in a timely and cost-effective manner or if we fail to introduce products and services that meet market demand or gain market share, we may lose our competitive position, our products may become obsolete","as_of":"2026-02-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Fierce Network：Arista 居資料中心交換第一，但 Nvidia 以 Spectrum-X 逼近。","source":"Fierce Network 'AI tailwind keeps Arista at No. 1 spot in data center switching — now Nvidia looms'","url":"https://www.fierce-network.com/cloud/arista-rides-ai-past-cisco-now-nvidia-looms","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025：Arista 以直銷團隊加通路夥伴（經銷商、VAR、系統整合商、OEM）銷售；夥伴通常先收到終端客戶訂單才向 Arista 下單，且一般不持有庫存。未見通路結構性改制的揭露。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm","excerpt":"We market and sell our products through our direct sales force and in partnership with our channel partners, including distributors, value-added resellers, systems integrators and original equipment manufacturer (\"OEM\") partners.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q4 2025 財報電話會議：訂閱型網路服務與軟體（A-Care、CloudVision 等）約占營收 17%，仍為少數；第三方整理稱 CloudVision Lite as-a-Service SKU 於 2026-03-02 停售。","source":"Arista Q4 2025 earnings call transcript (equibles.com 轉錄)","url":"https://equibles.com/stocks/anet/documents/1a44e419-f6ae-43d4-920d-6b6a5cf96df7","excerpt":"Arista's subscription-based network services and software revenue contributed approximately 17%.","as_of":"2026-02-17","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"第三方評論稱 Arista 推進園區／分支（含 VeloCloud SD-WAN）需強化通路策略，COO Todd Nightingale 負責擴大通路；此為評論而非公司披露。","source":"thestrategystory.com Arista Networks SWOT analysis 2026","url":"https://thestrategystory.com/blog/arista-networks-swot-analysis-2026/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 財報（2026-08）營收略高於 30 億美元，高於公司先前指引 28 億；2026 全年營收成長指引上調至約 40%（約 126 億美元），Q3 指引營收約 33 億、稀釋 EPS 1.06–1.08 美元。搜尋摘要未見下修。","source":"GuruFocus: Arista Networks Q2 2026 earnings call highlights (raised 2026 guidance)","url":"https://www.gurufocus.com/news/9004375/arista-networks-inc-anet-q2-2026-earnings-call-highlights-record-3-billion-quarter-and-raised-2026-guidance-signal-strong-ai-momentum","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 2026（2026-05）營收 27.1 億美元（共識 26.2 億）、EPS 0.87（共識 0.81），全年指引上調至約 115 億（成長約 28%）；Q2 指引營收約 28 億、EPS 0.88（MarketBeat 稱共識 0.84）。各來源對 Q2 營收指引相對共識（持平或低於約 28.5 億）說法不一。","source":"TIKR Q1 beat article; MarketBeat Q2 2026 guidance update 2026-05-05; 247wallst live blog","url":"https://www.tikr.com/blog/arista-networks-stock-beats-q1-revenue-estimates-with-2-71b-and-raises-full-year-outlook","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"管理層表示能見度約兩季，指引取決於供給可得性，供給釋出才有上檔空間（供應限制為風險）。","source":"搜尋摘要彙整（Hudson Labs／TIKR 等），非單一原文","url":"https://www.hudson-labs.com/research/arista-networks-q3-2026-earnings-preview-anet-results-preview","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Citi 於 2026-08-07 維持買進並將目標價由 173 上調至 215；Barchart 引述平均目標價約 238.34、街頭最高 289。Benzinga 韓文頁（8 月底）顯示共識目標價約 226（18 位分析師）。各聚合站數字與分析師家數差異大（Tickflow 185.45／26 位；VCP 區間 164–200／52 位）。","source":"Barchart: Arista Networks stock analyst estimates & ratings; Benzinga KR price targets","url":"https://www.barchart.com/story/news/3755970/arista-networks-stock-analyst-estimates-ratings","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"較新的目標價：Bernstein 250（2026-09-30）、Jefferies 250（2026-08-05），高於各聚合站共識均值；共識評等 Buy。","source":"StockAnalysis ANET forecast page（搜尋摘要）","url":"https://stockanalysis.com/stocks/anet/forecast/","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"EPS 預估上修：Zacks 稱 60 日內 2026 EPS 預估升約 7% 至 3.53、2027 升約 6.6% 至 4.19（文章日期未顯示）；MarketBeat 2026-04-29 當時 FY2026 共識 3.17。兩者口徑不同。","source":"Zacks: Should You Bet on ANET Stock Amid an Estimate Revision Uptrend?; MarketBeat 2026-04-29","url":"https://www.zacks.com/stock/news/2896323/should-you-bet-on-anet-stock-amid-an-estimate-revision-uptrend","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月（2025-11-08至2026-11-08）共5份8-K，皆為財報(2.02)或股東會(5.07)，無併購、重大協議、重編(4.02)等重大項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001596532&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 5 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單中無含2.01等重大項目者，搜尋亦未見2026年新併購（VeloCloud於2025-06-30完成，在窗口外）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001596532&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 5 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單無Item 4.02（財報不可信賴）等項目；搜尋僅見2015年舊重編與創辦人Bechtolsheim個人內線交易和解，均非近12個月公司事件。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001596532&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 5 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ANET","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":62.88,"operating_margin_pct":43.83,"fcf_margin_pct":42.2,"rd_intensity_pct":12.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ANET","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"CSCO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.52,"operating_margin_pct":25.36,"fcf_margin_pct":20.16,"rd_intensity_pct":15.1},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSCO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"HPE","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.73,"operating_margin_pct":7.84,"fcf_margin_pct":9.93,"rd_intensity_pct":8.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HPE","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"CIEN","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.07,"operating_margin_pct":14.12,"fcf_margin_pct":13.53,"rd_intensity_pct":15.36},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"CLS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.46,"operating_margin_pct":8.29,"fcf_margin_pct":2.99,"rd_intensity_pct":0.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"ANET"},"financial_history":{"ticker":"ANET","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":4381310000.0,"revenue_yoy_pct":null,"gross_margin_pct":61.07,"operating_margin_pct":34.86,"net_income":1352446000.0,"diluted_eps":1.0675,"free_cash_flow":448169000.0,"fcf_margin_pct":10.23,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":5860200000.0,"revenue_yoy_pct":33.75,"gross_margin_pct":61.95,"operating_margin_pct":38.52,"net_income":2087300000.0,"diluted_eps":1.645,"free_cash_flow":1999600000.0,"fcf_margin_pct":34.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":7003100000.0,"revenue_yoy_pct":19.5,"gross_margin_pct":64.13,"operating_margin_pct":42.05,"net_income":2852100000.0,"diluted_eps":2.23,"free_cash_flow":3676200000.0,"fcf_margin_pct":52.49,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":9005700000.0,"revenue_yoy_pct":28.6,"gross_margin_pct":64.06,"operating_margin_pct":42.82,"net_income":3511400000.0,"diluted_eps":2.75,"free_cash_flow":4252400000.0,"fcf_margin_pct":47.22,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ANET/ANET_Q3_2026_Earnings_Call_20261103.md）

# Q3 2026 Earnings Call
**Arista Networks, Inc.** | Earnings Calls | 2026-11-03

**Operator** (Operator):
Welcome to the Third Quarter 2026 Arista Networks Financial Results Earnings Conference Call. [Operator Instructions] As a reminder, this conference is being recorded and will be available for replay from the Investor Relations section on the Arista website following this call. Mr. Rudolph Araujo, Arista's Head of Investor Advocacy, you may begin.

**Rudolph Araujo** (Executives):
Thank you, Regina. Good afternoon, everyone, and thank you for joining us. With me on today's call are Jayshree Ullal, Arista Networks' Chairperson and Chief Executive Officer; and Chantelle Breithaupt, Arista's Chief Financial Officer. This afternoon, Arista Networks issued a press release announcing its fiscal third quarter results for the period ending September 30, 2026. If you want a copy of this release, you can find it on our website. 
During the course of this conference call, Arista Networks management will make forward-looking statements, including those relating to our financial outlook for the fourth quarter of the 2026 fiscal year, longer-term business model and financial outlook for 2027 and beyond. 
Our total addressable market and strategy for accessing those market opportunities across AI, campus, data center and other segments, inventory levels and management, lead times, purchase commitments, component supply and product innovation, which are subject to the risks and uncertainties that we discuss in detail in our documents filed with the SEC, specifically in our most recent Form 10-Q and Form 10-K and which could cause actual results to differ materially from those anticipated by these statements. 
These forward-looking statements apply as of today, and you should not rely on them as representing our views in the future. We undertake no obligation to update these statements after this call. This analysis of our Q3 results and our guidance for Q4 2026 and FY 2027 is based on non-GAAP financial measures and excludes stock-based compensation expense, intangible asset amortization and other nonrecurring items as well as the income tax effect of these non-GAAP exclusions, including the recognition of direct access tax benefits associated with stock-based awards. 
A full reconciliation of our selected GAAP to non-GAAP historical results is provided in our earnings release. A reconciliation of our FY '27 non-GAAP guidance to the most directly comparable GAAP measures is not available without unreasonable effort. With that, I will turn the call over to Jayshree.

**Jayshree Ullal** (Executives):
Thank you, Rudy, and welcome, everyone, to our third quarter 2026 earnings call. Arista just delivered a standout quarter of $3.66 billion in revenue, which is translating to our annual growth of 58.5%. This marks our largest ever year-over-year revenue growth in the history of being a public company.
Before we dive into the financial specifics, I would like to emphasize our rapid Arista 2.0 success, a strategy we embarked upon just 3 years ago. It has generated meaningful customer outcomes to become the central network nervous system for us. In the 2000 era, the industry had accepted a status quo, plagued by fragile, overly complex, disparate and vulnerable operating systems. Arista pioneered the universal cloud network and the AI leaf-spine architecture based upon our rock-solid, high-quality foundation of our differentiated EOS. 
That one network operating system with a publish-subscribe state and data-driven foundation has governed us with 5 As: agile security, automation, availability, analytics, and AI principles. By extending our single EOS operating system from the data center all the way from the universal spine to many forms of edge leaf functions, we deliver structural and secure network harmony. Our Arista 2.0 transformation from data centers to centers of data can be characterized as the age of network intelligence, learning from vast repositories of streamed data. 
It has driven our strategy across locations, be it client to branch, to campus, to data, to cloud and AI centers for our customers. Based on our network data lake architecture, we offer our customers automated and conversational troubleshooting agentic companions. Devoid of manual hunting through text-heavy logs, our systems proactively begin identifying and isolating issues for network workloads, workflows and work streams. 
In 2026, the network-centric acceleration is well underway. Our customers have increasingly coalesced the back end and the front end of AI and data centers. Arista has long championed standards-based Ethernet. Customers have welcomed our open approach to modernizing cloud, campus, data centers, WAN centers and now AI centers with a lower total cost of ownership.
Recently, we were recognized with the leader status from Forrester for the highest strength of innovation and data center portfolio. We were also recognized by Gartner Magic Quadrant Leadership for campus, wired and wireless, and data center segments. As agentic AI models increase in parallelism, compute diversity and density, we have the choice of many more training and inference accelerators. The industry, we believe, is shifting from compute-centric vertical stack to a holistic network-centric approach. 
Arista is committed to unleashing and breaking down the barriers between compute and networking. Arista customers can now construct an open network platform capable of handling heterogeneous models and diverse accelerators at scale. Our Etherlink portfolio of at least 25 switches for scale-up, scale-out and scale-across is optimally designed to improve XPU utilization, job completion time and token latency for these intense training and inference workloads.
In October of 2026, at the Open Compute Project conference, Arista showcased our rack scale-up designs, partnering closely with several AI accelerators infused with our Arista network diagnostics layer. Based on ESUN, Ethernet for scale-up, rack options, these include orthogonal designs, cable-intensive backplanes and heterogeneous cross-rack designs co-designed with many of our partners, including Arm, Microsoft Maia, AMD's Helios, Qualcomm, Meta's MTIA and many more ahead. We expect scale-up trials to begin in 2027, driving Ethernet to larger radix of 126 to 144 within a rack and across 1,000 across racks, with production expected for scale-up in 2028. 
We are witnessing the migration from highly centralized training compute to disaggregated and distributed inference, prefill and decode, demanding much more intelligent networking and colocation of compute, storage and KV cache resources rather than simply focusing on raw feeds and speeds and flops of compute. A well-designed network is becoming a foundational cornerstone for optimal token efficiency.
Arista's decades of EOS engineering in both multiplanar and distributed models routing at scale, be it ARP, address resolution protocols, or FIB tables, forwarding information base, or access list with rapid reconvergence comes to the rescue. Our Etherlink products are inherently designed to actively understand parameters at a deep level, including latency and bandwidth profiles of multitenancy to intelligently steer workloads for optimal placement between local and remote domains. 
The need for visibility into ports, packet queues, flows, buffer utilization and path latency across the entire scale-out and scale-across fabric validates [ real-time ] AI system level performance to avoid idling of precious compute cycles. It assures immediate and network-wide insight to the root cause as well as rapid recovery of the AI system with smart system upgrades across millions of accelerators. 
When we initially began this transformational AI journey, we spoke about 4 or 5 AI customers with approximately 50,000 to 100,000 NVIDIA GPUs. And in fact, we were largely staring at a proprietary network cycle such as InfiniBand. In 2026, we are in a super cycle of AI, having already surpassed 100 Etherlink customers. By the end of '27, we are forecasting greater than 10 gigawatts of deployment across 10 or more different types of compute accelerators. What a stark inflection in just 3 years. 
Central to this AI super cycle is also the expansion of Arista AVA, our Autonomous Virtual Assist, to support efficient AI in the enterprise. By providing that open programmable interface within EOS and utilizing the Model Context Protocol, MCP, AVA allows emerging AI agents to reason, to interact with the network stack and perform advanced multidomain event correlation across the entire enterprise. With exponential rise of generative AI attacks and the ever-increasing cyber threats, securing the network is key and integral and our responsibility. 
I would like to invite Ken Duda, our Founder, President and CTO, to shed some light on this problem. Ken?

**Kenneth Duda** (Executives):
Thanks, Jayshree. It's hard to overstate the impact of AI on networking. First, the good news, AVA, which is Arista's Autonomous Virtual Assistant, fueled by real-time data, AVA is incredibly powerful. It seamlessly navigates networking and security infrastructure from campus to WAN, to data center, to cloud, continuously monitoring and troubleshooting, isolating root causes without manual labor-intensive tasks. Having seen what AVA can do, I can't imagine managing my own infrastructure without it, and I expect many of our customers will feel the same way. 
The bad news, of course, is the massive challenge AI poses for us and our customers by discovering and exploiting security vulnerabilities. This threat landscape demands secure and robust networking. Over the past few months, we've been collaborating with Anthropic, Google, OpenAI and many others to integrate new AI-enabled security capabilities from frontier models into our existing software security pipeline. 
We are being invited early as a key infrastructure provider into partnerships like Project Glasswing, building AI-driven vulnerability discovery and assessment into our established security vulnerability management process. True network security has become a must-have, not a nice-to-have, and Arista's EOS operating system is the ideal architectural foundation based on 4 key principles.
First, a single high-quality operating system. Arista has maintained one of the lowest CVE counts, less than 100 in the industry over the last 2 decades, while others are rising exponentially due in part to the simple fact that multiple networking operating systems tend to have more vulnerabilities than just one. Second, limiting vulnerability impact through process isolation. 
EOS keeps each software agent, management plane or control plane, architecturally separate from each other and also from hardware forwarding, so traffic keeps moving even if there is a defect in one component. EOS's state-sharing architecture also resists lateral movement. So a defect in one component typically cannot be exploited to attack other agents within the switch. 
Third, we provide a seamless upgrade process. Process isolation also means that we can ship a targeted fix to the affected component and install the fix without a maintenance window or network disruption. And fourth, delivering a compliance dashboard to stay current. When a security advisory lands, Arista CloudVision brings real-time visibility that turns a stressful advisory day into a manageable one. 
In addition to providing secure switches, we also provide Zero Trust Networking, or ZTN technology, to help our customers build secure infrastructure. I'd especially like to highlight Macro Segmentation Services, or MSS, a ZTN feature allowing for dynamic security enforcement, preventing undesired interactions among users, devices and applications.
Second, we provide Network Detection and Response, or NDR services, that profile, analyze and proactively detect sophisticated security threats. And finally, once workload traffic leaves the confines of the local data center, it becomes even more vulnerable to malicious actors. So we offer protection with wire speed ubiquitous link and tunnel encryption native in every port with 0 performance degradation. 
I hope this was a helpful summary of how Arista is helping customers take advantage of AI while improving security to meet the new challenges. Back over to you, Jayshree.

**Jayshree Ullal** (Executives):
Thank you, Ken. It was useful for me, too. With Arista's uncompromised ZTN approach, we can systematically address the security hazards and parabolic attacks. Our CVE count, our vulnerability count is often 10 to 50x better than alternatives. Our customer momentum this year has been significant to the enterprise in the providers across data center, campus and AI because we are addressing security proactively. 
I would like to invite Todd Nightingale, our President and Chief Operating Officer, to describe more about this. Over to you, Todd.

**Todd Nightingale** (Executives):
Thanks, Jayshree. We're seeing phenomenal growth across our enterprise business, driven by customers building mission-critical networks, which benefit from Arista's industry-leading quality and reliability. As the entire industry responds to AI-powered attack exposure, customers are motivated by the fact that keeping their infrastructure current with security updates will protect, segment and defend against vulnerabilities beyond the network. 
Arista won a strategic deal at an Asian web services company as they shifted their focus strategically on the speed, scale and resilience in the new AI era. Reliability was the key to the engagement as their teams are frustrated by long-standing quality issues with their existing vendor. Arista was able to demonstrate reliability and scalability while leveraging standards-based technology and a powerful EVPN-VXLAN architecture on our 100- and 400-gig platforms. This deployment will operate as the front end for their AI deployments moving forward. 
In the health care sector, leading hospitals are selecting Arista for strategic data center deployment. One important hospital group chose Arista following an exhaustive Zero Trust Networking evaluation. Their primary business goal was to protect sensitive patient data through advanced network segmentation while enabling seamless integration to cloud environments. Arista secured this win by delivering an automated high-performance fabric that perfectly aligned with their trust nothing, verify everything security mandate.
By centralizing routing on Arista's R3 spines, we provided a powerful streamlined layer for traffic management tailored to modern health care workloads with a robust leaf-spine topology. We deployed CloudVision-as-a-Service alongside the Arista AVD framework for cloud-based automation and deep visibility. And by integrating Arista's segmentation service, MSS, the customer can now dynamically automate the entire system.
In the hospitality sector, an award-winning regional resort and casino selected Arista to modernize its expanding operations. Realizing their legacy network was a bottleneck for innovation, they architected a truly unified standards-based architecture across their data center and campus environments to support new guest experiences and rapidly scale their services. 
Arista's routing and switching platforms alongside campus access switches are delivering quality and reliability key to performing in mission-critical applications like their demanding casino gaming floor network. They utilize CloudVision and AVD to automate device provisioning and gain the deep real-time visibility required to optimize network performance. In all 3 of these examples, Arista's differentiated EOS provided unmatched quality and reliability and integrated seamlessly with their overarching security ecosystem partners. Additionally, our TAC delivered the flawless experience and peace of mind to derisk these modern enterprise migrations to Arista. 2026 has really been an exciting year building momentum across our entire enterprise business around the world in data center, campus and AI build-outs. Thank you, Jayshree.

**Jayshree Ullal** (Executives):
Thank you, Todd. Wow, that momentum is indeed unprecedented. I haven't experienced anything like this until you arrived. We are pleased with Arista's accelerated networking progress across all our sectors. Our commitment to fulfilling this accelerated demand in the second half of 2026 is really playing out well with our improved execution in supply chain, partnering closely with our vendors.
I want to give a special kudos to you and your entire manufacturing team led by Eugenia for the tireless work and progress despite the widespread industry-wide supply chain constraints and shortages. With this backdrop, we are now increasing our annual guidance for the fourth time in 2026 to $13.3 billion, which represents a 48% annual growth. 
At Arista, we find ourselves in a position to address this ever-increasing total accessible market, not just available market, which now stands at north of $200 billion in 2030, therefore, representing a multiyear growth opportunity for us. Our first look at 2027 guidance range puts us in the 38% to 40% range for growth annually to approximately $18.5 billion. Within this envelope, we expect our AI fabrics target to be the fastest-growing segment and to double to approximately $7 billion, while our cognitive campus represents a healthy growth of 60%, much faster than the market to approximately $2 billion in 2027.
We do live in exciting times as we harness the power of cloud and AI revolution. It has certainly surpassed my expectations as we exceeded our original $10 billion goal this year to enter revenue dollars in the teens for both 2026 and 2027. We do so in the typical Arista way, bringing our unique combination of innovations, quality, profitability, efficiency and 0 debt, making our financials very pristine. 
Our results would not be possible without the cohesive Aristan leadership and team, our elite customers and partners and, of course, our supportive shareholders. And with that, over to you, Chantelle, to shed more light on our impressive financials.

**Chantelle Breithaupt** (Executives):
Thank you, Jayshree. This quarter, we delivered record high revenue growth since our IPO at 58.5%, partnered with robust operating margin above 49%. At the same time, we invested ahead of demand in R&D, inventory and supply commitments to support the AI opportunity in front of us. Congratulations to the Arista team for being named to the S&P 100 in September, a great achievement within a short time frame.
Let's dive into the financial details. To start off, total revenues in Q3 were approximately $3.66 billion, up 58.5% year-over-year and above our guidance of $3.3 billion. This significant growth was driven by our continued strength in both AI and enterprise customers. International revenues for the quarter came in at $682.5 million, or 18.6% of total revenue, down from 23% last quarter. 
This quarter-over-quarter change was primarily influenced by a shift in the geographic mix of sales to our large global customers. Year-over-year double-digit growth was achieved in all 3 geographic segments. The overall gross margin in Q3 was 64%, down from 65.2% in the prior year, with supply chain efficiency working to partially offset product cost inflation, and up from 63.4% in the prior quarter, driven by end customer mix. 
Operating expenses for the quarter were $545.3 million, or 14.9% of revenue, up from the last quarter of $411 million. Our R&D spending came in at $408.5 million, or 11.2% of revenue, up from the last quarter at $278.1 million. Arista continues to demonstrate its commitment and focus on network innovation with additional investment in liquid cooling, high-radix switching and leading AI software. 
Sales and marketing expense was $110.9 million, or 3% of revenue, down slightly from 3.6% of revenue last quarter, representative of the highly efficient Arista go-to-market methodology. Our G&A costs came in at $25.9 million, or 0.7% of revenue, up slightly from $23.1 million last quarter as we continue to focus on our critical corporate systems and processes. Our operating income for the quarter was $1.8 billion, or 49.1% of revenue, demonstrating our ability to invest in innovation while expanding profitability. 
Other income and expense for the quarter was a favorable $138.6 million, and our effective tax rate was 20.9%. Overall, this resulted in net income for the quarter of $1.53 billion, or 41.9% of revenue. Our diluted share number was 1.278 billion shares, resulting in a diluted earnings per share for the quarter of $1.20, up significantly with a growth of 55.8% from $0.77 in the prior year period. 
Now turning to the balance sheet. Cash, cash equivalents and marketable securities ended the quarter at approximately $14.4 billion, up from $13.3 billion at the end of Q2. Of the $1.5 billion stock repurchase program approved in May of 2025, $817.9 million remain available for repurchase in future quarters. The actual timing and amount of future repurchases will be dependent on market and business conditions, stock price and other factors.
Now turning to operating cash performance for the third quarter. We generated approximately $1.2 billion of cash from operations. This was driven by a robust earnings performance, coupled with an intentional inventory build to meet our growing customer demand. DSOs came in at 59 days, down from 68 days in Q2 due to the timing of customer shipments and invoicing. 
Our inventory turns dropped slightly from 1.7 in Q2 to 1.6 for the quarter. We ended the quarter with $3.2 billion in inventory, up from $2.5 billion last quarter. Inventory level fluctuations are expected to continue as we work through the balancing of component timing and availability. This could result in quarters of elevated inventory balances affecting the timing of cash flow from operations ahead of customer deployments. 
Our purchase commitments at the end of the quarter were $11.4 billion, up from $9.7 billion at the end of Q2. As mentioned in prior quarters, this expected activity mostly represents purchases for chips related to new products and AI deployments. Our total deferred revenue balance was approximately $6.8 billion, down from $6.9 billion in the prior quarter. The majority of the deferred revenue balance is product related. Our product deferred revenue decreased $86 million sequentially versus last quarter. 
We remain in a period of ramping our new products, winning new customers and expanding new use cases, including AI. These trends have resulted in increased customer-specific acceptance clauses and an increase in the volatility of our product deferred revenue balances. 
As mentioned in prior quarters, the deferred balance can move significantly on a quarterly basis, independent of underlying business drivers. Accounts payable days were 48 days, down from 57 days in Q2, reflecting the timing of inventory receipts and payments. Capital expenditures for the quarter were $100.7 million. Our construction work to build expanded facilities in Santa Clara remains on track, and we expect construction to be completed in the coming months. 
As we look ahead, the momentum is strong. We are grateful to our customers and proud of our team's continuous ability to rise to meet the demands of the networking industry. For the fourth quarter, we are forecasting a range of revenue between $3.9 billion and $4 billion. This positions fiscal year 2026 revenue just over $13.3 billion at the midpoint. 
Our fourth quarter gross margin outlook is 63% to 64% and operating margin is between 48% and 49%. Diluted EPS is forecasted to be between $1.26 and $1.30 with approximately 1.28 billion diluted shares, and the effective tax rate is expected to be approximately 21%.
Looking further ahead to 2027, the momentum continues. For fiscal year 2027, the revenue growth outlook is between 38% and 40%, equating to approximately $18.5 billion at the midpoint. Gross margin continues to be in the range of 62% to 64% and an operating margin of approximately 49%. Our effective tax rate is expected to be approximately 21%. 
In closing, there is a lot to be excited about here at Arista. We will continue to be focused on our innovation, execution and delighting customers in the Arista way. Now back to you, Rudy, for Q&A.

**Rudolph Araujo** (Executives):
Thank you, Chantelle. We will now move to the Q&A portion of the Arista earnings call. [Operator Instructions] Regina, please take it away.

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Michael Ng with Goldman Sachs.

**Michael Ng** (Analysts):
I wanted to ask about your comment around the greater than 10 gigawatts of deployments across 10-plus compute accelerators for next year. Could you just talk a little bit about whether that is an industry number or an Arista-specific number in terms of those deployments? And how does the diversification of compute potentially create more opportunities for Arista networking relative to just having a handful of compute suppliers?

**Jayshree Ullal** (Executives):
Thanks, Michael. As you know, I think much of AI, even in our world started initially being compute-centric, and we're seeing that change to network-centric. And so as part of the accelerated networking strategy, we are supporting 3 types of AI fabrics, scale-up, scale-out and scale-across. So our guess is by the end of '27, we will deploy largely in '26 and '27, is where the exponential ramp happened, across or greater than 10 gigawatts. 
Now some of that -- much of that gigawatt may be new. But remember, in scale-across, we can also have existing gigawatts being deployed. So we're talking about new distributed 10 gigawatts, but there may already be multiple gigawatts deployed across. 
So the rationale here is while we are new to scale-up, we are touching a variety of XPUs and scale-out and scale-across, across the rack and across data centers. And we already know with our scale-across, we are touching multiple XPUs, 4 or 5 of them. With the advent of scale-up, we will add another 5 in 2027.

**Operator** (Operator):
Our next question will come from the line of Meta Marshall with Morgan Stanley.

**Meta Marshall** (Analysts):
Congrats on the quarter. I guess just, Jayshree, if you could give an update just on how you see that mix of scale-across and scale-out and scale-up just as a mix of your business. Clearly, scale-up nothing today. I think last quarter, you had said you expected 1/3 of the demand this year to be from scale-across. Just as you've continued to increase your guidance and as you look into '27, just what do you see those mixes being?

**Jayshree Ullal** (Executives):
I think in '27 -- Meta, thank you for the kind wishes. We've been working hard for this day. The scale-up will still be in early trials. So I don't think there's a material number associated with scale-up in '27. I do think it could contribute in '28. So then that -- if scale-up is virtually 0, then we're basically left with most of the use case being scale-out and scale-across. 
And as you've heard us say in the past, scale-across, we think, will be at least 1/3. It will probably go higher in '27. And so the split this year is roughly 70-30. The split next year may be -- I can't venture to guess, but I think the 70 may come down and the 30 would go up when it comes to scale-across because it's a very strong use case for us. Arista is highly differentiated with our 7800 scale-across platform. 
And unsurprisingly, the word scale means a lot to us there and our customers, scale for security, scale for performance, scale for reliability, and there's just no room for error when you're connecting millions of XPUs. So we feel very comfortable that these are our 2 strongest use cases. 
I also think it will fuel -- I mean, a lot of this is back-end AI fabric. We will come back to revisit a question of front end as well as we move to more inference and the line between back and front becomes thinner.

**Operator** (Operator):
Our next question will come from the line of Ben Reitzes with Melius Research.

**Benjamin Reitzes** (Analysts):
Jayshree, pretty good quarter guide there. So I just want -- you've previously referred to potentially 2 10%-plus customers into the fourth quarter. Do you mind talking about whether they're landing in that range and what the use cases are for and if you're excited about those customers still and into '27?

**Jayshree Ullal** (Executives):
Yes. Yes, yes. So I guess diversity is the name of the game and the theme today, right, Chantelle?

**Chantelle Breithaupt** (Executives):
That's right.

**Jayshree Ullal** (Executives):
We have diverse accelerators. We have diverse models. We want to have diverse 10% customers, too. So as we said before, our dearest ones are M&M. We fully expect our top prior 10%-plus customers to continue to be with us in '26, and we hope beyond. 
And we expect to add at least 1, maybe 2. And a lot of that depends on whether Todd and Eugenia can ship enough product. So we'll let them decide, and we'll give them all the way into December 31.

**Todd Nightingale** (Executives):
We'll take every day.

**Jayshree Ullal** (Executives):
So we're feeling pretty good about at least 3 and maybe 4.

**Operator** (Operator):
Our next question will come from the line of George Notter with Wolfe Research.

**George Notter** (Analysts):
I was just curious about the big sequential jump in R&D. It was really, really significant. I'm just wondering if that included some onetime items. Also, is this the new run rate in R&D going forward? Any perspective there would be great.

**Jayshree Ullal** (Executives):
Okay. So over to you, Ken. Why did you spend so much money this year?

**Kenneth Duda** (Executives):
We're building so much new stuff. The opportunity is humongous in AI, these AI accelerating systems are -- we are -- our success with the hyperscaler AI companies depends on our ability to partner. Our ability to partner is based on our understanding of each of their unique requirements and constraints.
And also, there's a new technology introduction around liquid cooling. This requires major infrastructure upgrades and technology upgrades on our part. So I think that's what's really driving the expansion in spending there.

**Chantelle Breithaupt** (Executives):
Sorry, George, just in your comment, is this new run rate, I'll still put the framework at anywhere between 9% and 11% as we work through. So some quarters like we've talked about, we'll hit this range as we have specific investments. And so I would still keep it in that 9% to 11%. More to come as we guide next year in more detail.

**Jayshree Ullal** (Executives):
But I noticed the prototype bill was very high this quarter, Ken.

**Kenneth Duda** (Executives):
That's right, because of all the opportunities in the hyperscaler AI space.

**Operator** (Operator):
Our next question will come from the line of Amit Daryanani with Evercore ISI.

**Amit Daryanani** (Analysts):
Congrats on a really good set of numbers over here. Jayshree, you talked initially about the industry moving towards a more network-centric architecture. As customers deploy different type of accelerators, does Arista become involved earlier in designing the overall systems rather than connecting them afterwards? 
And as you have to work with a more distributed disaggregated compute network, does that change your networking content per deployment? I know you talked about 10 gigawatts, I'm just sort of wondering, does the network intensity start to change as well? 
And then maybe for Chantelle, as you think about this 38%, 40% guide for '27, which is extremely impressive, can you just touch on your confidence around the supply chain execution to meet this demand? What's in the bag versus what still needs to be closed?

**Jayshree Ullal** (Executives):
Amit, this is a very good question. I think until now, we've enforced our architecture mostly on scale-out and scale-across. And a lot of that had to do with distributed power, location, moving to regional edges, a very software-defined type of network with the intensity, like I described, of package, flows, performance, predictable latency, et cetera. 
As we start participating with new accelerators, we get a greater chance early in the cycle to see the behavior of these accelerators. Two or 3 examples I'd like to highlight is our close work with Cerebras, our work with Microsoft and Maia. These have been going on the last couple of years and has allowed us to tune our buffers, tune our software performance and maximize the I/O throughput, if you will. 
The recognition of those scale-up designs are still in the works, but they're already manifesting itself in scale-out and scale-across. So you bring up a very good point, not only in the actual work we're doing with these accelerators, but the aggregate impact it has on our network design in terms of scale, performance and reliability.

**Chantelle Breithaupt** (Executives):
And then I think to part two of your question, Amit, and thank you for the kind words at the beginning, I think -- so I am confident in the guide, and I am confident in the supply chain. What makes me confident in the supply chain is internally, Todd and Eugenia and the team doing a fantastic job every day, being scrappy to make sure we can do what we need to do to deliver to our customers. 
And I also have confidence in a lot of great conversations and agreements with some of our key suppliers, and that's why you see our purchase commitments increasing because we have that confidence. So internally, externally confident. As far as visibility, I think we have 2 quarters of visibility as we always have, and we lean into the other 2. But given our highly fungible portfolio, we're pretty clear where to make that bet. So we're pretty excited about next year.

**Operator** (Operator):
Our next question will come from the line of Tim Long with Barclays.

**Timothy Long** (Analysts):
Maybe if we could shift a little bit and talk about the campus and branch, pretty good year this year and guiding it to 60% next year. Could you talk a little bit about kind of what's enabling you to grow so much faster than the industry? And is this something that you see as a multiyear type of dynamic? Obviously, you got strength in enterprise data centers. But curious what else is helping this much higher than industry growth?

**Todd Nightingale** (Executives):
Thanks for the question. In a lot of ways, I think the enterprise campus market is coming to us. Arista has always led the way in quality and reliability. And over the past few years, just practically every significant enterprise has shifted gears and really considered their campus networks, their branch networks mission-critical, with the highest need for reliability. 
This has only accelerated because of the Glasswing and Mythos effect where people are really focused deeply not only on providing the highest level of reliability, but being able to do that as they rapidly patch and adjust their infrastructure over time. And the differentiation with EOS and the ability for Arista software to be able to do this with practically no downtime with extremely, extremely high uptime, it's highly differentiated in the market. And I really think that's the core of what's driving market share gains here.

**Kenneth Duda** (Executives):
I think the other thing that makes this an incremental process is that campus refresh cycles are pretty long. So even customers that understand the Arista advantage may take some time to adopt us simply because of the schedule on which they depreciate and upgrade their gear. So I think we can expect this to be a multiyear cycle.

**Operator** (Operator):
Our next question will come from the line of David Vogt with UBS.

**David Vogt** (Analysts):
So maybe, Chantelle, one for you, and I'll wrap 2 together in 1 question. Can you kind of help us understand sort of your purchase commitment dynamic and your deferred revenue dynamic against the strong revenue guide that you provided for 2027? So obviously, we recognize that you're confident in the number. But deferred revenue, I understand that it's volatile and it varies quarter-to-quarter. 
But just help us understand how to think about that metric in the context of a 38% to 40% guide, particularly also with purchase commitments going up a couple of billion dollars sequentially.

**Chantelle Breithaupt** (Executives):
Thanks, David. I think there's a few things. I don't know if they correlate directly, but they're all in purpose and designed to serve the customers as we need to exiting Q4 and into 2027. Purchase commitments from that perspective, there are some things additionally we added and now we have memory in there, a memory agreement, which has done that. So that's a multiyear agreement that you'll see as the Q comes out. 
And I think on the purchase commitment side, you can probably expect that to go up a little bit more as we exit Q4, as we get ready for this 2027 guide we have. As far as the deferred revenue, deferred revenue actually had the largest churn in and out and still remained flat and still delivered a 58.5% revenue growth quarter, which I think is a fantastic outcome.
So there, you're seeing things exit again, released, and things to get booked back to the deferred balance, which I think is a really healthy sign of the demand that's fueling that 38% to 40% revenue growth next year. So I think they're all related. Purchase commitments grow to serve that demand and the deferred staying flat to deliver that outcome to the P&L. And we're pretty excited to see how that continues through 2027.

**Operator** (Operator):
Our next question will come from the line of Simon Leopold with Raymond James.

**Simon Leopold** (Analysts):
Appreciate that. I wanted to get one quick clarification. You gave us targets for 2027 for campus and AI. Just wanted to check on what the baselines are for 2026. And the question was really on a topic that I think Andy has been vocal about, but your thoughts about the evolution of switching with the inclusion of either CPO or NPO, what does that mean to Arista?

**Jayshree Ullal** (Executives):
Okay. Just to clarify, the baseline upon our 38% to 40% is the '26 guide we gave of...

**Chantelle Breithaupt** (Executives):
Yes, $13.3 billion.

**Jayshree Ullal** (Executives):
$13.3 billion.

**Chantelle Breithaupt** (Executives):
Yes. And within that, AI is $3.5 billion and campus is $1.25 billion.

**Jayshree Ullal** (Executives):
Yes. We're staying with the target numbers because we only know actuals after we ship everything end of the year. And to your second question on optics, optics is very integral to Arista's strategy. Andy Bechtolsheim, our Chief Architect, lives and breathes this. It doesn't mean we build everything, but we actually systematically put it together. 
We, first of all, strongly believe in copper when you can and optics if you must, because the minute you go beyond the 1- or 2-meter radius, the flexibility of pluggable optics and lasers is probably the most widely deployed and accepted. Andy was a pioneer of OSFP that gave us a very wide density of thermal limits and widely used. And now our new coherent optics, LPO modules is something that goes long distance without requiring DSP. 
And then to meet higher front panel density, we're very excited about extra-dense pluggable optics that can -- that is being supported by over 150 vendors. So we think the world is going to remain in a very majority fashion on pluggable optics. 
Having said that, I think there's always room for complementing the pluggables with a strong adoption at higher speeds to what we call near-packaged optics or open CPO. We don't want to build proprietary co-packaged optics. And to solve these constraints, Arista has been pioneering this open CPO that instead of soldering components, we can use socketed optical engines and pigtail fibers to allow these modules to be pretested, et cetera.
So we are big fans of these. We think they'll come on to the market in the '28 to '30 time frame. It's not imminent, but meanwhile, long live pluggable optics.

**Operator** (Operator):
Our next question will come from the line of Joseph Cardoso with JPMorgan.

**Joseph Cardoso** (Analysts):
Congrats on the results as well. Maybe the question that I wanted to touch on and maybe it kind of dovetails off of the clarification on the last one. When we take a look at the initial full year guide for 2027, particularly as it relates to maybe the non-AI noncampus business, I think growth is being implied to moderate from the strong 2026 levels. 
I was just wondering if you can kind of touch on the underlying assumptions or factors that's maybe driving a little bit more moderation here into 2027 and whether that's maybe just tough compares or conservatism in terms of supply, et cetera. Just trying to understand directionally what's the drivers of the 2027 forecast as it relates to the maybe core business.

**Jayshree Ullal** (Executives):
Thank you, Joe. Well, listen, when some things are growing 60% and 100%, and then you say the overall growth is 38% to 40%, then obviously, some of the things are not growing as fast, right? We're very comfortable that everything is going to grow double digits, some more, some less. And we're also very comfortable that given our first guide literally over a year before that all sectors are doing well for us, AI, enterprise, specialty cloud providers, front-end networks. So we started out 2026 wondering if front end would grow. So it's a cyclical thing. 
When the back end grows, the front end may grow a little slower. When the back end slows down, the front end may grow a little faster. So I wouldn't read any conservatism into these numbers. These are wildly higher and optimistic than we had once projected. So enjoy them for a moment, and hopefully, they'll get better.

**Operator** (Operator):
Our next question will come from the line of James Fish with Piper Sandler.

**James Fish** (Analysts):
Fantastic quarter and guide here to start for '27, ladies, and Ken, of course.

**Jayshree Ullal** (Executives):
We have 2 gentlemen and 2 ladies.

**James Fish** (Analysts):
And Todd, I don't -- I didn't forget about you, Todd. But look, I appreciate the early outlook, but you guys always talk about 1 to 2 quarters of visibility. You tend to be a very prudent team. And so maybe going back to, I think it was Amit's question, I guess, the confidence in providing the durability at this scale this early and why we're going to see this kind of strength persist, why Arista for scale-up in 2028?

**Chantelle Breithaupt** (Executives):
Well, I'll just go back, and thank you for the kind words...

**Jayshree Ullal** (Executives):
The kind words to the ladies and gentlemen.

**Chantelle Breithaupt** (Executives):
That's right, to all of us. I think that -- so I'll just go back and reiterate the confidence level. There was a lot of thought, obviously, put into a guide this strong, this early. So there's a lot of attention paid with Todd and Ken and Jayshree and myself and team. So we had to get comfortable first, and we're very comfortable with all the things we've done to secure what we need to go ahead. 
And again, the 2 quarters visibility, 2 years of relationship and technical conversations, so somewhere between the second half lands, and it's the usual kind of cadence we have. So nothing's changed there. I think from -- and then the second part of your question was about scale-up going into 2027, 2028. Jayshree?

**Jayshree Ullal** (Executives):
Yes. So listen, I think scale-up has been a tough market for us because it doesn't have all the software advantages that we bring, but it absolutely has the hardware skills and all the non-NVIDIA accelerators that Arista is in the best position to connect to. So this movement from stand-alone basic switches to rack scale is something that Andy, Alex, Hugh Holbrook, the entire team has been working on and co-developing for a couple of years. It's hard work. 
Just as we were staring at InfiniBand and now we can go, of course, it's going to be Ethernet. We're looking forward to a time where we were staring at proprietary UALink or NVLink, and we're going to go, of course, it's going to be ESUN. But these type of migrations are multiyear. And so we're very confident not only in our '27 guide, but a promising '28 ahead as well. And the reason we are is because even though we have 2 quarters of visibility, we have 2 years of work behind it.

**Operator** (Operator):
Our next question will come from the line of Tal Liani with Bank of America.

**Tal Liani** (Analysts):
I missed the call last time, and you raised the guidance substantially, and now you're doing it again. And on the other hand, I heard Chantelle's explanation about deferred revenues, but the sequentials are slowing down, if I look at total deferred and current deferred, are slowing down. But you are feeling more comfortable with next year and you're guiding well, well above the street. 
So the question is, when you look at orders versus recognizing from deferred because of availability of components, because of releasing kind of deferred revenues, because of completion of build-out, et cetera, so what are the drivers for -- like same question, but from different angles. 
What are the drivers for the growth? Is it orders? Or is there some part there of recognition of historical orders? And then is deferred revenue actually losing some of its predicting ability just because I see some decoupling between the deferred revenue trends and revenue growth trends?

**Jayshree Ullal** (Executives):
Okay. Let me start and then Lady Chantelle, will you take over? So I think, first, Tal, we missed you last quarter because we don't get this level of detail from anyone else on exactly what are the puts and takes. I just broadly look at you and say, hey, it's great demand. And if you want to dissect demand into how much is sitting into deferred, how much is sitting into our orders, how much is getting shipped into revenue, you're turning demand into a physics problem that I don't have the answer for because I don't predict or forecast deferred. 
Deferred is a strong function of a new use case or a new product that eventually is not a new use case or a new product. So we had millions of dollars come out of deferred because the use case is satisfied. We had millions of dollars go in as deferred. And generally, that number, if you look at it over the last few quarters or if you look at it over the entire year, is trending up. 
But deferred is never going to be infinite. It is going to come out and other new deferred will go in, or the product becomes familiar and less new, right? So it's important to just look at this big picture and say, we got demand. We got demand in AI, in enterprise, in campus, in data centers, and we're just in the best position we've been in a long, long time in my 18-year career at Arista. Over to you, Chantelle.

**Chantelle Breithaupt** (Executives):
The only thing -- I think it's very well said, and I think that's the right perspective to take on this, so we don't get too lost in the weeds on a quarter-to-quarter basis. We're very confident in the demand and the guide. Deferred is a balance sheet account that will reflect whatever happens in the quarter. So that is what it is. 
The only thing I'd add, like I said before, Tal, we did miss you last quarter, was that we anticipate the end of this year from a deferred balance to be higher than we ended last year, which shows that the P&L did what the P&L needed to do without deferred. And so if that helps you feel more comfortable with that, then that's the only thing I would leave you with.

**Operator** (Operator):
Our next question will come from the line of Ryan Koontz with Needham & Company.

**Ryan Koontz** (Analysts):
I wanted to follow up on some of your scale-up commentary and ask about some of the technical design changes a little bit here with obviously including more optics and including liquid cooling. And how will that change your fulfillment model? What things are you including in your sale versus partner to reference third parties? And maybe you can expand a little bit on your product plans around scale-up and how we should think about the product changes.

**Jayshree Ullal** (Executives):
Actually, that's a really good question, Ryan. We're still figuring it out ourselves because Arista's value in the rack scale is still the switch. But however, we have to design the whole rack and then work with different partners differently on whether they want the whole rack from us or the rack gets shipped through our manufacturing partners while we basically ascertain the switch. 
So different strokes for different folks, because you've got 3 different designs going on with the orthogonal, the cabled backplane and the cross-rack designs, each one is a little bit different. Give us a chance in the next few quarters to share with you what's going on with each one. There isn't one answer to your question. But one last thing I do want to add to that is that what's very clear is there's a lot of switches swimming in water. A lot of it's liquid-cooled.

**Operator** (Operator):
Our next question will come from the line of Karl Ackerman with BNP Paribas.

**Karl Ackerman** (Analysts):
Chantelle or Jayshree, I'd like to ask a question that was similar to peers, but in a slightly different way. In the context of your 2027 revenue outlook, can you speak to whether your revenue outlook is predicated on new permitting or financing of power shell infrastructure to achieve these forecasts? And as you address that, can you speak to whether you require an aggressive drawdown of your deferred revenue balance to achieve your outlook? I think I know the answer, but I would love your view.

**Jayshree Ullal** (Executives):
What do you think our answer is? It's so nice to sometimes ask a question ourselves.

**Karl Ackerman** (Analysts):
I don't think you need to, but I would love clarification.

**Jayshree Ullal** (Executives):
Okay. Go for it, Chantelle.

**Chantelle Breithaupt** (Executives):
Yes, we're not -- we don't guide deferred. So I think that was the answer you were expecting to the second hand. I would say from the perspective of the guide next year, we are looking at what we know ahead of us, 2 quarters visibility, taking a lean on the second half of the next year in the sense of what we've had conversations with some of our largest customers, the run rate we have in Todd's business in the sense of enterprise. And all that comes together, but we don't guide deferred.

**Jayshree Ullal** (Executives):
His question was, are we counting on data center?

**Chantelle Breithaupt** (Executives):
The first part. The second part was are we preparing to draw down deferred to hit the number? So we don't guide deferred, but I would say that we see a very strong demand signal and demand environment back to the momentum theme. But Jayshree, if you want to comment on...

**Jayshree Ullal** (Executives):
Right, exactly. So I think while we don't guide deferred, let me be clear, that we do see plenty of new use cases and new products. 2027, like '26, is going to be filled with lots of new products.

**Operator** (Operator):
Our next question will come from the line of Gianmarco Conti with Deutsche Bank.

**Gianmarco Conti** (Analysts):
Congrats on the quarter, great numbers. As SU-144 moves towards production in '28, how should we think about gross margin economics relative to your existing switching portfolio? And how much customer commits do you already have behind those programs?

**Jayshree Ullal** (Executives):
You're talking about '27 or '28?

**Gianmarco Conti** (Analysts):
'27 and '28.

**Jayshree Ullal** (Executives):
What's your question?

**Gianmarco Conti** (Analysts):
It's about gross margin for SU-144.

**Jayshree Ullal** (Executives):
Look, since we went public, our long-term gross margin has always been in the 60% to 65%. I think we've tightened the range now to more like 62% to 64%. We don't see any change.

**Operator** (Operator):
Our next question will come from the line of Daniel Zhu with Bernstein.

**Daniel Zhu** (Analysts):
Congrats on a great quarter. I just want to ask how concentrated is the customer base for scale-across? Should we think about this as really being driven by the cloud titans for synchronous training? Or are we also seeing scale-across deployments even among smaller customers or for inference use cases?

**Jayshree Ullal** (Executives):
Yes. No, I think they are both small use cases and colos for scale-across, which would be a smaller footprint switching and routing platforms like the 7280. But the concentration of our large customers also is high with our larger customers opting for the very large AI spines across data centers and requiring that kind of 576-port density and terabit scale and multi-gigawatt deployments for security and performance. So we do see both, but I think the revenue concentration favors the 7800. The location concentration of multiple sites favors the 7280.

**Operator** (Operator):
Our next question will come from the line of Sean O'Loughlin with TD Cowen.

**Sean O'Loughlin** (Analysts):
Congrats on the fantastic results, ladies and gentlemen. I want to just check in broadly on where we are actually in the front-end cycle. I think we've spent so much time talking about scale-out, scale-across, back-end deployments and the focus on 800 gig and above in those deployments that maybe we collectively have lost track of where we are in the sort of more traditional front-end compute. I'm just wondering if you could comment on that and what you see in terms of market trends on the front end specifically.

**Jayshree Ullal** (Executives):
Yes. No, Sean, it's a very good question. I think the -- it's like a sine wave. When everybody is focused on the back end, then there's -- in those customers, they're thinking less about the front end. And then sometimes when they're focusing a lot on the front end, they're not worrying as much about the back.
If you look at it over a period of time, like 6 quarters to 2 years, you can capture both. But in a given year, we had one 10% customer, for example, put a lot of thought into the multihundred gig refresh of their front end before enhancing their back end. And so that particular year, their front end was very high, but their back end was low. The following year, maybe the reverse. 
So if you tend to look at it over multiple quarters and years, they even out. But if you tend to look at it in a concentrated period of time, you'll usually see more of one than the other. Right now, in general, we're seeing more back end and AI fabrics, and I think the front end will catch up later.

**Operator** (Operator):
Our next question will come from the line of Antoine Chkaiban with New Street Research.

**Antoine Chkaiban** (Analysts):
Congratulations on the very strong set of results. Ken, maybe one for you. I want to ask about AVA. With all the recent high-profile infrastructure security breaches we've been hearing about, it looks like the technology can address a very large opportunity. So how should we think about sizing it? How do you plan to monetize AVA? And is that going to fall into products? Or could this drive actually a meaningful acceleration in your services revenue?

**Kenneth Duda** (Executives):
We are early days in understanding all of that. We have just turned the AVA on as an alpha feature for customer trial within our CloudVision service, and we are currently working on pricing models. I don't think I have any forecast or data to share with you at this time on that.

**Jayshree Ullal** (Executives):
But I think it's very promising, Antoine, because back again to Ken's point that he repeatedly makes with me is the architecture of EOS is so sound that adding AVA or CloudVision as capability to look at deeper details and get more analysis starts with the foundation, right? So we feel very privileged that we can sit here and we can talk about, oh my God, our vulnerabilities doubled from 30 to 67, and we fixed them. And therefore, we can go apply AVA. 
Everybody else is dealing with a game of whack-a-mole where they've got thousands of vulnerabilities and no AVA can possibly keep track of it. So I think we feel in a very good position to monetize AVA in the next few years.

**Operator** (Operator):
Our next question will come from the line of Ben Bollin with Cleveland Research.

**Benjamin Bollin** (Analysts):
Jayshree and Todd, I suppose, I'm interested in your thoughts on where lead times are across the portfolio if we kind of carve it up into enterprise-centric and hyperscale-centric, just what those look like today? And I was hoping Todd could talk maybe a little bit more big picture about the go-to-market effort, the execution within enterprise share capture, and how that's building and where that goes from here.

**Todd Nightingale** (Executives):
On the lead times, and it goes both for the component lead times and the finished good lead times. In the enterprise side of our business, we tend to have shorter lead times, somewhat shorter. And that's driven by the fact that those switches are not always in the absolute cutting edge. They're not leaving brand-new technologies requiring the highest process silicon, et cetera. 
And we're able to -- they also tend to be at a lower price point, we're able to hold a little bit more buffered inventory there. So we tend to have lower component lead times there and lower lead times to our customers on the AI side, on the ultra-advanced hyperscale data center lead times tend to be a little bit longer. 
As far as the build-out on the go-to-market side, we were really -- we have been just really pleased with the momentum we've seen this year and the maturity that's being built into the whole go-to-market on the kind of thought leadership side and the awareness side, we saw great momentum on the -- from webinars and from events. In fact, we have our largest customer event coming up in December, which we're very excited about. 
And on the sales execution side, it's been just phenomenal efficiency from that team, and we're looking forward to continuing to build out next year.

**Jayshree Ullal** (Executives):
I just want to add, Todd, also, I see that you and Chris Schmidt, Chris Bellmare, you've really heightened the investment not only in the United States, but with key verticals and international as well. So I think all of the go-to-market investments we've been making over the last year and in fact, the last 3 years, is really paying off.

**Operator** (Operator):
Our final question will come from the line of Mehdi Hosseini with Susquehanna.

**Mehdi Hosseini** (Analysts):
I have 2 quick follow-ups. Going back to your revenue guide for '27, $18.5 billion, should we assume that all the silicon have been planned for? And then the second question, if you could elaborate on the mix between cloud and enterprise. I just want to get a better understanding how enterprises are investing as it relates to hyperscalers.

**Todd Nightingale** (Executives):
Sorry, you asked is all the silicon planned for already in the $18.5 billion?

**Mehdi Hosseini** (Analysts):
Should we -- since you are providing an initial assessment on 2027 revenue target, should we assume that you have already planned with your suppliers and silicon is secured for both compute and memory? And there are some that argue that tightness is going to get worse in '27. I just want to make sure that there is no downside risk to this target as it relates to inventory management and supply.

**Todd Nightingale** (Executives):
Understand, understand. We work very, very closely. We're sort of proud of our strategic partnerships, and we've been investing heavily in long-term strategic agreements in order to secure supply, not just in silicon, but PCB capacity memory, which Chantelle mentioned earlier. So we're incredibly -- we have very high confidence in the ability to deliver supply to the forecast. We -- of course, we would not want to place everything to 5 quarters lead time for all of next year. So not every order is placed.

**Rudolph Araujo** (Executives):
This concludes Arista Networks' Third Quarter 2026 Earnings Call. We have posted presentations that provide additional information on our results, which you can access in the Investors section of our website. Thank you for joining us today and for your interest in Arista.

**Operator** (Operator):
Thank you for joining, ladies and gentlemen. This concludes today's call, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ANET_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CEO｜guidance：CEO 說這是今年第三次上調財測（2026 營收約 126 億美元、年增 40%）（原話："we are excited to increase our guidance for the third time"）
- 2026-08-04｜CFO｜guidance：CFO 給 Q3 毛利率與營業利益率指引（原話："operating margin between 48% and 49%"）
- 2026-08-04｜CFO｜guidance：CFO 給全年校園營收目標（原話："our 2026 campus revenue goal is at least $1.25 billion"）
- 2026-08-04｜CFO｜guidance：CFO 給全年 AI fabrics 目標（至少 35 億美元；CEO 另處講 AI target 至少 36 億）（原話："is at least $3.5 billion."）
- 2026-08-04｜CEO｜guidance：CEO 提到 AI 目標至少 36 億美元，其中 scale-across 約占 30%（原話："30% of our overall AI target of at least $3.6 billion"）
- 2026-08-04｜CFO｜margin：CFO 維持全年毛利率區間 62%–64%，含供應鏈成本上升（原話："maintaining the range for the fiscal year of 62% to 64%"）
- 2026-08-04｜CFO｜margin：CFO 上調全年營業利益率目標至 48%–49%（原話："operating margin target now at a range of 48% to 49%"）
- 2026-08-04｜CFO｜margin：CFO 拆解 Q2 毛利率對比指引：關稅退款 20–30 bps，其餘為客戶組合（原話："20 to 30 bps of tariff refund and the remainder more of a"）
- 2026-08-04｜CFO｜margin：CFO 表示毛利率目前尚未計入漲價效果（原話："I wouldn't put anything in there yet due to a price increase"）
- 2026-08-04｜CEO｜margin：CEO 說漲價效果要到年底或明年才反映，因仍在消化積壓訂單（原話："price increases will really help or affect us only towards"）
- 2026-08-04｜CFO｜margin：CFO 說明 Q2 毛利率 63.4%，年減因客戶組合（原話："gross margin in Q2 was 63.4%, down from 65.6% in the prior"）
- 2026-08-04｜CFO｜margin：CFO 報 Q2 營業利益率（原話："operating income for the quarter was $1.5 billion or 49.9%"）
- 2026-08-04｜CFO｜guidance：CFO 報 Q2 營收約 30 億美元，年增 37.7%（原話："revenues in Q2 were just over $3 billion, up 37.7%"）
- 2026-08-04｜CEO｜commitment：CEO 說明多年期採購承諾由 36 億增至約 97 億（原話："now almost tripling from a year ago at $3.6 billion"）
- 2026-08-04｜CFO｜commitment：CFO 報 Q2 末採購承諾 97 億美元，上季 89 億（原話："commitments at the end of the quarter were $9.7 billion"）
- 2026-08-04｜CEO｜commitment：CEO 對全年各項數字的口徑：不給 AI/校園新數字，但稱都會上調（原話："we can most certainly say all numbers are"）
- 2026-08-04｜CEO｜commitment：CEO 表示預期 1 到 2 個 10% 以上客戶（原話："I fully expect there to be 1, maybe 2 10%"）
- 2026-08-04｜CEO｜customer：CEO 說全年增幅 10 億美元以上，微軟與 Meta 仍為最長期夥伴（原話："we're going to increase the number by $1 billion or more"）
- 2026-08-04｜CEO｜customer：CEO 提到 Etherlink AI 客戶累計數（原話："now exceeds 100 cumulative customers"）
- 2026-08-04｜CEO｜customer：CEO 說 scale-across 已延伸至數家 Neocloud（原話："we're already seeing it apply to several Neoclouds"）
- 2026-08-04｜CEO｜customer：CEO 對核心資料中心前端的說法：不會持平（原話："it isn't going to be flat"）
- 2026-08-04｜CEO｜risk：CEO 稱供應鏈問題是產業性的兩年問題（原話："The industry is going to have a 2-year problem."）
- 2026-08-04｜CFO｜risk：CFO 說庫存可能出現高檔季度，影響營運現金流時點（原話："could result in quarters of elevated inventory balances"）
- 2026-08-04｜CFO｜risk：CFO 說明遞延收入波動來自客戶特定驗收條款增加（原話："increased customer-specific acceptance clauses"）
- 2026-08-04｜CFO｜risk：CFO 說指引依有把握取得供應的量來訂（原話："guiding based on what we're confident we can get the supply"）
- 2026-08-04｜CFO｜risk：CFO 說客戶能見度仍維持約兩季（原話："we still have the same kind of 2 quarters of"）
- 2026-08-04｜COO｜product：COO 說記憶體 2026 年供應已確保（原話："Our memory supply has been secured for 2026"）
- 2026-08-04｜COO｜product：COO 說已建立液冷供應鏈（原話："we've now established a liquid cooling supply chain"）
- 2026-08-04｜CEO｜product：CEO 說 1.6T 將於下半年試用，2027 才量產（原話："we will be in trials in the second half of this year"）
- 2026-08-04｜CEO｜product：CEO 說 1.6T 量產在 2027（原話："the real production will still be in 2027"）
- 2026-08-04｜CEO｜product：CEO 預估 2026 scale-across 市場規模約 30–40 億美元，將快速成長（原話："still maybe $3 billion to $4 billion"）
- 2026-08-04｜CEO｜competition：CEO 說白盒是戰術性方案，用於簡單情境（原話："white box is certainly a tactical solution"）
- 2026-08-04｜CEO｜competition：CEO 說在供應與人力稀缺下 Arista 系統級方案勝出（原話："Arista is really winning out with the system-wide approach"）
- 2026-08-04｜CEO｜competition：CEO 說 NVIDIA 場景（NVLink scale-up）轉換需要較長時間（原話："In the NVIDIA cases, it's going to take a bit longer."）
- 2026-08-04｜CEO｜competition：CEO 說 CPO 方面多數仍為可插拔光學與銅線（原話："will still remain pluggable optics and copper"）
- 2026-08-04｜CFO｜capital_allocation：CFO 說本季未回購股票（原話："repurchase our common stock."）
- 2026-08-04｜CFO｜capital_allocation：CFO 說 Santa Clara 擴建預計 2026 年底完工（原話："we expect construction to be completed by the"）

### 問答異常語氣（迴避／改口／保留）
- ANET_Q2_2026_Earnings_Call_20260804.md｜問：UBS Vogt：為何全年財測大幅上調但 AI 目標沒變、僅動校園｜答法：CEO 稱數字都會上調，但拒絕給具體數字，理由是看出貨組合
- ANET_Q2_2026_Earnings_Call_20260804.md｜問：Melius Reitzes：AI 實驗室客戶進展與第四季潛在 10% 客戶｜答法：CEO 改談安全網路研討會與模型多元，未直接回答客戶進展與 10% 客戶
- ANET_Q2_2026_Earnings_Call_20260804.md｜問：Wells Fargo Rakers：是否新增 10% 客戶、微軟與 Meta 是否仍為 10% 以上｜答法：CEO 只說預期 1 到 2 個 10% 客戶，並稱要保留彈性，未指名
- ANET_Q2_2026_Earnings_Call_20260804.md｜問：Raymond James Leopold：增加的 10 億美元來源組成｜答法：CEO 稱涵蓋所有產品線，出貨後才知道確切組成，未給拆分

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
{"date":"20260805","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 基建超級週期持續，且 Arista 可服務的 scale-out／scale-across 段不被 scale-up 邊緣化"},{"id":"H2","text":"系統層贏單守得住 — Arista 在超大規模客戶的份額不被 NVIDIA 矽晶片、白牌 ODM 與客戶自有 NOS 結構性侵蝕"},{"id":"H3","text":"市場維持對 Arista 的成長溢價倍數 — 不 de-rate 至硬體同業區間"}],"extra_text":"假設 | vs Inception（2026-05-06，$146.65）累積漂移\nH1 | 🟢 兌現。Inception 時 FY26 指引 $10.5B、AI 目標 $3.25B→$3.5B；今日指引 $12.6B、AI $3.5B。總營收路徑大幅超前（+20%），但 AI 分項零漂移 — 累積漂移的方向是「總量超交付、AI 分項原地」。\nH2 | 🟡 削弱。Inception 時的疑慮是 Spectrum-X 已贏 Meta＋Oracle；今日 IDC 確認 NVIDIA 已取走資料中心乙太網第一，且 Meta 的 Minipack3N 白牌交換機直接建在 NVIDIA Spectrum-4 ASIC 上（Meta Engineering，2025-10-13）。份額壓力自「訂單層」下沉到「客戶內部矽來源層」。惟 Meta 同時仍在 DSF 架構中部署 Arista 7700R4，未見主體切換。\nH3 | 🔴 反向漂移（對持有人不利方向）。Inception 時 Fwd PE（FY+2）約 32x；今日 42.1x。股價 +43.5%，倍數擴張貢獻約三分之二。H3 從「假設」變成「已經被市場超額給付」 — 這正是本份裁決留在觀望的原因。"},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"大客戶內部矽來源替代：NVIDIA Spectrum ASIC 滲透進客戶自研白牌（Meta Minipack3N＝Spectrum-4 ASIC＋Accton 代工）、Microsoft 以自有 SONiC 取代 EOS 差異化（Azure 近七成 aggregation 交換機）。這比「訂單份額」更結構 — 即使營收金額仍成長，差異化正被壓回硬體層"},{"id":"R2","text":"AI 資本支出進入消化期 → 42x 倍數快速 de-rate。此風險的形狀是「基本面還好、股價先崩」，因為 H3 是三個假設中證據等級最低的一個"},{"id":"R3","text":"垂直整合參考系統繞過系統 OEM 層（本次新增）：Broadcom Tomahawk 6-Davisson（102.4Tbps CPO 交換器，自有 ASIC＋自有光引擎）自 2025-10-08 起已出貨。管理層在法說談的是「開放 CPO 2028-2029」，但非開放的垂直整合 CPO 整機今天就可以買 — 若超大規模業者願意直接採購晶片商參考系統，擠壓時點遠早於 2028"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE(NTM) ≤ 35x（以現行 NTM EPS $4.61 計約 $161，隨共識上修同步上移）；週線布林中軌現位 $160.55 同區","irr_base_pct":3.9,"ev5y_pct":12.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":1.1,"ev5y_pct":12.0,"irr_base_pct":3.9,"max_dd_pct":-65.0,"bull_5y_price":421.0,"bear_5y_price":81.0,"p_bull_pct":22.0,"p_bear_pct":32.0,"rearm_trigger":"Fwd PE(NTM) ≤ 35x（以現行 NTM EPS $4.61 計約 $161，隨共識上修同步上移）；週線布林中軌現位 $160.55 同區","price_at_dd":210.51,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
