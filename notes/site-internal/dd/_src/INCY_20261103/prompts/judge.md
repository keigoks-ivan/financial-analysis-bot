你是 stock-analyst **v20 判斷 agent**，標的 INCY（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"INCY","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenue_gaap","label":"Total revenue (GAAP)","value":1557.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income","value":-629.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":-708.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_kpi3_gaap_eps_diluted","label":"GAAP EPS (diluted)","value":-3.86,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation","value":69.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_kpi5_cash_equivalents_marketa","label":"Cash, equivalents & marketable securities","value":3854.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_kpi6_fy2026_guidance_total_ne","label":"FY2026 guidance: total net sales","value":"5,210–5,300","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_kpi7_fy2026_guidance_opzelura","label":"FY2026 guidance: Opzelura net sales","value":"1,100–1,120","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_kpi8_fy2026_guidance_hematolo","label":"FY2026 guidance: Hematology & Oncology net sales","value":"890–910","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_kpi9_fy2026_guidance_non_gaap","label":"FY2026 guidance: non-GAAP R&D+SG&A opex","value":"4,625–4,695","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_incy_gross_margin_pct","label":"INCY 毛利率","value":92.69,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INCY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_incy_operating_margin_pct","label":"INCY 營業利益率","value":11.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INCY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_incy_fcf_margin_pct","label":"INCY FCF 利潤率","value":11.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INCY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_vrtx_gross_margin_pct","label":"VRTX 毛利率","value":86.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRTX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vrtx_operating_margin_pct","label":"VRTX 營業利益率","value":37.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRTX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vrtx_fcf_margin_pct","label":"VRTX FCF 利潤率","value":30.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRTX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_regn_gross_margin_pct","label":"REGN 毛利率","value":84.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.REGN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_regn_operating_margin_pct","label":"REGN 營業利益率","value":26.87,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.REGN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_regn_fcf_margin_pct","label":"REGN FCF 利潤率","value":23.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.REGN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bmrn_gross_margin_pct","label":"BMRN 毛利率","value":76.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMRN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bmrn_operating_margin_pct","label":"BMRN 營業利益率","value":4.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMRN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bmrn_fcf_margin_pct","label":"BMRN FCF 利潤率","value":21.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMRN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_exel_gross_margin_pct","label":"EXEL 毛利率","value":96.26,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXEL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_exel_operating_margin_pct","label":"EXEL 營業利益率","value":40.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXEL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_exel_fcf_margin_pct","label":"EXEL FCF 利潤率","value":45.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXEL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":118.97,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":22.48,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":54.28,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":15.48,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.1 → 3.58）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.34,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.71 → 8.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.06 → 9.06）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.58,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":8.74,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":9.06,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":60.7,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝10.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":10.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.03,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝30.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":30.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝23.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":23.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":33.23,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.58，分子＝快照價 118.97","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-3817.16,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 37.41、現金 3854.57（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":203.83,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":20433.26,"period":"2026-11-03","unit":"USD m","basis":"市值 24250.42 ＋ 淨負債 -3817.16","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6036.48,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6277.74,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.38,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 119.21 / W52 107.24 / W104 90.26 / W250 77.06 / W250 13週斜率 0.9%"},{"id":"f_ma_w52","label":"52 週均線","value":107.24,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":90.26,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":77.06,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.9,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 披露：已收到 Apotex、Hikma、Sun、Granules 等多家學名藥廠對 JAKAFI 的 ANDA/NDA 通知函，Jakafi 面臨學名藥競爭風險","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm","excerpt":"We have received a notice letter from each of Apotex, Inc., Hikma Pharmaceuticals USA Inc., Sun Pharmaceutical Industries Inc., Granules India Ltd., Dr.…","as_of":"2026-02-10","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出競爭對手包含大型藥廠與小型生技，資源多於 Incyte，可能開發出使其產品過時的藥物","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm","excerpt":"our competitors, which include large global pharmaceutical and biopharmaceutical companies and smaller research-based biotechnology companies, may succeed in developing products that render our products obsolete or noncompetitive.","as_of":"2026-02-10","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Fierce Pharma：Incyte 面對新競爭者並準備 Jakafi 專利懸崖（GSK Ojjaara 等）","source":"Fierce Pharma","url":"https://www.fiercepharma.com/pharma/competitor-rollouts-and-patent-cliff-incyte-banks-jakafi-resilience-new-disease-and","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Fierce Pharma：Jakafi 趨近學名藥競爭，Incyte 更依賴 Opzelura","source":"Fierce Pharma","url":"https://www.fiercepharma.com/pharma/jakafi-approaches-loe-incyte-counting-more-opzelura","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Incyte 10-Q 揭露其對多數商品（含 Jakafi）無自有製造設施，且各原料/API/成品通常單一或少數合格供應商，並維持至少 24 個月 ruxolitinib phosphate API 庫存","source":"Incyte Form 10-Q for period ended 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000066/incy-20260930.htm","excerpt":"While our strategy is to maintain at a minimum 24 months stock of ruxolitinib phosphate API, inclusive of finished product, ruxolitinib phosphate might be used by us either to make JAKAFI or OPZELURA or for ruxolitinib drug candidates in clinical trials.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：Jakafi/Opzelura 產品營收五大客戶占比 A 13%、B 9%、C 21%、D 18%、E 11%（合計約72%）；五大客戶占2025年底應收帳款54%（2024年底49%）。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm","excerpt":"Customer A 13 % 15 % 17 % Customer B 9 % 10 % 10 % Customer C 21 % 19 % 18 % Customer D 18 % 17 % 17 % Customer E 11 % 10 % 10 % We are exposed to risks associated with extending credit to customers related to the sale of products. Customers A, B, C, D and E comprised, in the aggregate, 54% and 49% of the accounts receivable balance as of December 31, 2025 and 2024, respectively.","as_of":"2026-02-10","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q2 2026 Jakafi/Jakafi XR sales $817M, +7% YoY; FY Jakafi guidance unchanged at $3.22-3.27B; Jakafi XR approved May 2026 for MF, PV, GVHD.","source":"Incyte Q2 2026 earnings release (BusinessWire/BioSpace)","url":"https://secure.businesswire.com/news/home/20260728733422/en/Incyte-Reports-Second-Quarter-2026-Financial-Results-and-Provides-Business-Updates","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2 2026 Opzelura sales excluding one-time accrual reversal were $204M, +24% YoY; FY2026 total net sales guidance raised to $5.13-5.26B, largely from a one-time non-cash CMS-settlement accrual reversal (~$300-310M FY).","source":"Incyte Q2 2026 earnings release / SEC 8-K","url":"https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000053/incy-q22026xexx991.htm","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因子僅以一般性文字提及製藥業曾成為反壟斷等訴訟與調查對象，並提到公司過去曾受講者計畫與病患援助計畫的查詢；未指出現行針對 Incyte 的反壟斷調查。三次搜尋亦未發現 2026 年 DOJ／FTC／EU 對 Incyte 的反壟斷行動。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm","excerpt":"pharmaceutical and biotechnology companies have been the target of lawsuits and investigations alleging violations of government regulations, including claims asserting submission of incorrect pricing information, improper promotion of pharmaceutical products, payments intended to influence the referral of federal or state healthcare business, submission of false claims for government reimbursement, antitrust violations","as_of":"2026-02-10","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因子指出併購交易可能受反壟斷審查拖延或附帶剝離條件（一般性風險，非針對特定案件）。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm","excerpt":"antitrust scrutiny by regulatory agencies and changes to regulatory approval processes in the U.S. and foreign jurisdictions may cause approvals to take longer than anticipated to obtain, or may not be obtained at all, or contain burdensome conditions such as required divestitures","as_of":"2026-02-10","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FDA 對 Zynyz NSCLC sBLA 發出 Complete Response Letter，唯一理由為 Catalent Indiana 充填廠合規，非療效或安全性。","source":"Incyte 8-K 2026-03-06 (Boardroom Alpha)","url":"https://www.boardroomalpha.com/sec/incy-8-k-2026-03-06-0000879169-26-000013","excerpt":"FDA CRL for Zynyz NSCLC sBLA due to facility inspection findings; efficacy unaffected; Incyte pursuing resubmission with Catalent. About Incyte Corp Market cap","as_of":"2026-03-06","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Incyte FY2025 10-K 風險因子揭露：營運及其CRO、供應商可能受國際貿易政策（關稅與貿易爭端、制裁、進出口許可要求）造成的業務中斷與不確定性影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm","excerpt":"as well as other business uncertainties as a result of international trade policies, including tariff and trade disputes, trade sanctions and import and export licensing requirements.","as_of":"2026-02-10","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-04-02 總統公告依 Section 232 對專利藥及其原料課徵關稅（Annex I 產品 100%；歐盟/日/韓/瑞士 15%；英國 10%）；與HHS簽署在地化及最惠國定價協議者適用 0%。搜尋結果未提及 Incyte 是否被列入或有協議。","source":"Baker McKenzie Global Import Blog 2026-04-08","url":"https://globalimportblog.bakermckenzie.com/2026/04/08/united-states-president-trump-tariffs-on-patented-pharmaceuticals-under-section-232/","excerpt":null,"as_of":"2026-04-08","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Incyte 10-Q 風險揭露：ruxolitinib phosphate（Jakafi/Opzelura 活性成分）原料來自中國供應商，中美貿易爭端可能影響供應。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000066/incy-20260930.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Incyte 10-K 揭露 Jakafi 原料僅單一來源，並依賴單一或少數合格供應商（原料、API、成品）","source":"Incyte Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm","excerpt":"We generally have a single source or a limited number of suppliers that are qualified to supply each of the API and finished product of our drug products and our other drug candidates. For ruxolitinib phosphate, the API for JAKAFI and OPZELURA, we have three qualified third-party contract manufacturers from","as_of":"2026-02-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Incyte 10-Q 風險因子提到關稅、制裁及俄烏與中東衝突可能干擾營運與供應商","source":"Incyte Form 10-Q Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000066/incy-20260930.htm","excerpt":"business uncertainties as a result of international trade policies, including tariff and trade disputes, trade sanctions and import and export licensing requirements. In addition, geopolitical and other events, such as the Russian invasion of Ukraine or the conflicts in the Middle East, could lead to sanctions, embargoes, supply shortages, regional instability, geopolitical shifts, cyberattacks","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026：總營收年增14%；Jakafi淨銷售+4%至$827M（付費需求+12%）；Opzelura +36%至$255M（含與CMS和解後淨價改善，pro forma約+21%）；血液腫瘤合計+38%至$235M；Niktimvo $67.4M vs $45.8M","source":"Incyte Q3 2026 8-K / 10-Q (SEC); BioPharmaWatch; Panabee","url":"https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026上調全年指引：總淨銷售$5,130–5,260M、Opzelura $1,050–1,100M（原$750–790M）、Jakafi維持$3,220–3,270M；Opzelura上調與CMS不將其視為Jakafi line extension的和解（返利）有關","source":"Incyte Q2 2026 8-K (SEC); Fierce Pharma","url":"https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000053/incy-q22026xexx991.htm","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Jakafi美國專利到期（LOE）約2028年12月，之後預期學名藥ruxolitinib侵蝕；公司目標2030年非Jakafi產品淨銷售$3–4B；ER劑型轉換目標3–5%","source":"Fierce Pharma 'As Jakafi approaches generic competition, Incyte counts more on Opzelura'","url":"https://www.fiercepharma.com/pharma/jakafi-approaches-loe-incyte-counting-more-opzelura","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Opzelura在美國品牌外用藥新患者份額46%；美國以外Q2銷售$43M，年增34%","source":"Fierce Pharma 'Boosted by CMS settlement, Incyte expects Opzelura to cross $1B in 2026'","url":"https://www.fiercepharma.com/pharma/boosted-cms-settlement-incyte-expects-opzelura-cross-1b-2026","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 稱生技製藥業競爭激烈且技術變化快速；合作夥伴可能追求替代技術或替代產品，而與公司產生衝突。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm","excerpt":"The biotechnology and pharmaceutical industries are intensely competitive and subject to rapid and significant technological change.","as_of":"2026-02-10","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Incyte 自家 INCA033989（突變 CALR 抗體）在 EHA 2026 的 MF 數據：第24週 27%（17/62）達 SVR35；公司為其自我迭代的新機轉，非外部替代。","source":"Incyte 新聞稿 EHA 2026 (BioSpace/BusinessWire)","url":"https://www.biospace.com/press-releases/incyte-announces-new-positive-data-at-eha-2026-showed-inca033989-achieved-rapid-robust-and-sustained-clinical-and-molecular-responses-and-was-well-tolerated-in-patients-with-myelofibrosis-and-essential-thrombocythemia","excerpt":"27% (17/62) patients achieved SVR35","as_of":"2026-06-13","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 描述 Incyte 產品仍經專業與零售藥局、專業經銷商及批發商（美國）和零售/醫院藥局、經銷商及獨家批發商（美國以外）銷售；文件未見訂閱化、D2C 或平台化的通路轉型描述。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm","excerpt":"These commercialized products are sold to specialty and retail pharmacies, specialty distributors and wholesalers in the United States in addition to retail pharmacies, hospital pharmacies, distributors and an exclusive wholesaler outside of the United States.","as_of":"2026-02-10","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 結果（2026-10-29）公司再上調 2026 全年總淨銷售 guidance 至 $5.21–5.30B（前值 $5.13–5.26B）；Opzelura 與 Hematology/Oncology guidance 亦上調。Q3 營收 $1.56B、年增 14%；GAAP 虧損含 Vega Therapeutics 收購的一次性 $1.23B IPR&D 費用。","source":"Incyte 8-K Q3 2026 press release (SEC) / Quiver Quant","url":"https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026（2026-07-28）營收 $1.67B、調整後 EPS $3.09，高於共識約 $1.50B／$2.20；公司將全年總淨銷售 guidance 由 $4.77–4.94B 上調至 $5.13–5.26B，其中 Opzelura 含 $246M CMS 和解的一次性非現金利益。","source":"MarketBeat / Barchart 搜尋摘要","url":"https://www.marketbeat.com/instant-alerts/incyte-nasdaqincy-price-target-raised-to-15000-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026 年 2 月初始 guidance 低於當時共識（約 $5.52B；Opzelura 指引 $750–790M vs 共識 $801.5M）；Q2 後一來源稱 guidance 低於 $5.6B 共識，但該共識可能為上調前舊值，來源間不一致。","source":"TIKR / 搜尋彙整","url":"https://www.tikr.com/blog/incyte-shares-drop-8-post-earnings-analysts-target-104-amid-2026-guidance-concerns","excerpt":null,"as_of":"2026-02-15","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Investing.com 美國頁：12 個月平均目標價 128.48，共識 Buy（23 位分析師；12 買/15 持有/1 賣），最新項為 JPMorgan Hold 目標 $123（2026-09-28）。","source":"Investing.com INCY consensus estimates","url":"https://www.investing.com/equities/incyte-corp-consensus-estimates","excerpt":null,"as_of":"2026-09-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布隨來源與日期差異大：MarketBeat 7/29 共識目標約 $113.60（8 買/14 持有，共識 Hold）；Barchart 平均 $127.09、最高 $155；Benzinga 8 月中平均 $110、最高 $155；HC Wainwright 升至 $150、BMO 升至 $130（7 月底）。","source":"MarketBeat / Barchart / Benzinga 搜尋摘要","url":"https://www.barchart.com/story/news/3905499/incyte-stock-is-wall-street-bullish-or-bearish","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 全年營收 guidance 中點相對分析師估計落差的報導","source":"Panabee Incyte Q3 2026","url":"https://www.panabee.com/news/incyte-earnings-q3-2026","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Incyte 於 2026-07-06 完成收購 Vega Therapeutics（2026-06-08 宣布，前期 $12.5 億美元，另有最多 $7.5 億銷售里程碑）。","source":"SEC EDGAR 8-K 2026-07-06 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000048/incy-20260706.htm","excerpt":"On July 6, 2026, Incyte Corporation (the “Company”) issued a press release announcing it has completed its previously announced acquisition of Vega Therapeutics, Inc., a wholly owned subsidiary of Star Therapeutics LLC (“Vega Therapeutics”).","as_of":"2026-07-06","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"Incyte 與 CMS 就 Opzelura Medicaid 回扣規則訴訟達成和解，預計第二季認列約 $2.46 億美元一次性非現金利益。","source":"SEC EDGAR 8-K 2026-06-22 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000046/incy-20260622.htm","excerpt":"The Company expects to record a one-time, non-cash benefit of approximately $246 million in the second quarter ending June 30, 2026, associated with the reversal of previously established accrual balances through March 31, 2026","as_of":"2026-06-22","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Incyte 與 CMS 簽協議，Jakafi 對州 Medicaid 採國際參考價，預期不受 GUARD/GLOBE 等未來定價授權影響，公司稱不影響 2026 指引。","source":"SEC EDGAR 8-K 2026-08-31 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000058/incy-20260831.htm","excerpt":"The Company does not expect the agreement to affect its 2026 financial guidance or have a material impact on its future financial outlook.","as_of":"2026-08-31","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"+","claim":"Jakafi XR 獲 FDA 核准（2026-05 初，先前曾收 CRL）；povorcitinib（HS）申請已受理，預期 1Q27 核准。","source":"搜尋摘要：Incyte Q1 2026 業績新聞稿","url":"https://www.businesswire.com/news/home/20260210471010/en/Incyte-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-07-06 完成收購 Vega Therapeutics（前期 $12.5 億美元）。","source":"SEC EDGAR 8-K 2026-07-06","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000048/incy-20260706.htm","excerpt":"On July 6, 2026, Incyte Corporation (the “Company”) issued a press release announcing it has completed its previously announced acquisition of Vega Therapeutics, Inc.","as_of":"2026-07-06","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"+","claim":"與 CMS 的 Opzelura Medicaid 回扣訴訟於 2026-06 和解、公司撤訴；搜尋未見近12個月證券集體訴訟。","source":"SEC EDGAR 8-K 2026-06-22","url":"https://www.sec.gov/Archives/edgar/data/879169/000087916926000046/incy-20260622.htm","excerpt":"the Company has withdrawn its lawsuit challenging the regulations.","as_of":"2026-06-22","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"Jakafi XR 於 2026-05 初獲 FDA 核准；povorcitinib HS 申請受理，預期 1Q27 核准。","source":"搜尋摘要：Incyte Q1 2026 業績新聞稿","url":"https://incytecorp.gcs-web.com/news-releases/news-release-details/incyte-reports-first-quarter-2026-financial-results-and-provides","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"INCY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":92.69,"operating_margin_pct":11.66,"fcf_margin_pct":11.31,"rd_intensity_pct":57.16},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INCY","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"VRTX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":86.0,"operating_margin_pct":37.95,"fcf_margin_pct":30.16,"rd_intensity_pct":32.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRTX","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"REGN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":84.86,"operating_margin_pct":26.87,"fcf_margin_pct":23.01,"rd_intensity_pct":40.4},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.REGN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"BMRN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.12,"operating_margin_pct":4.38,"fcf_margin_pct":21.28,"rd_intensity_pct":28.99},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMRN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"EXEL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":96.26,"operating_margin_pct":40.21,"fcf_margin_pct":45.84,"rd_intensity_pct":33.43},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXEL","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"INCY"},"financial_history":{"ticker":"INCY","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":3394635000.0,"revenue_yoy_pct":null,"gross_margin_pct":93.9,"operating_margin_pct":17.43,"net_income":340660000.0,"diluted_eps":1.52,"free_cash_flow":892108000.0,"fcf_margin_pct":26.28,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":3695649000.0,"revenue_yoy_pct":8.87,"gross_margin_pct":93.1,"operating_margin_pct":17.73,"net_income":597599000.0,"diluted_eps":2.65,"free_cash_flow":449001000.0,"fcf_margin_pct":12.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":4241217000.0,"revenue_yoy_pct":14.76,"gross_margin_pct":92.64,"operating_margin_pct":2.39,"net_income":32615000.0,"diluted_eps":0.15,"free_cash_flow":235174000.0,"fcf_margin_pct":5.54,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5141242000.0,"revenue_yoy_pct":21.22,"gross_margin_pct":92.76,"operating_margin_pct":26.12,"net_income":1286650000.0,"diluted_eps":6.41,"free_cash_flow":1329631000.0,"fcf_margin_pct":25.86,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/INCY/INCY_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Incyte Corporation** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Greetings, and welcome to the Incyte Third Quarter 2026 Earnings Call. [Operator Instructions] As a reminder, this conference is being recorded. [Operator Instructions] 
It's now my pleasure to turn the call over to Alexis Smith, Vice President and Head of Investor Relations. Please go ahead, Alexis.

**Alexis Smith** (Executives):
Thank you. Good morning, and welcome to Incyte's Third Quarter 2026 Earnings Conference Call. Before we begin, I encourage everyone to go to the Investors section of our website to find the press release, related financial tables and slides that follow today's discussion.
On today's call, I'm joined by Bill, Pablo and Suky, who will deliver our prepared remarks. Steven, Dave and Mohamed will also be available for Q&A. I would like to point out that we will be making forward-looking statements, which are based on our current expectations and beliefs. These statements are subject to certain risks and uncertainties, and our actual results may differ materially. I encourage you to consult the risk factors discussed in our SEC filings for additional detail. 
I'll now hand the call over to Bill.

**William Meury** (Executives):
Thanks, Alexis, and good morning, everyone. As we look at the first 9 months of the year, we've made meaningful progress against the strategy we laid out for Incyte. That strategy has 2 fundamental components: scaling the core business beyond Jakafi; and advancing our late-stage pipeline to drive the next phase of growth. The core business is the foundation. It gives us a scale to navigate the '29 transition and fund R&D. Layering the pipeline on top of that gives us the opportunity to build a significantly larger company over the next decade.
We now have several compounds in Phase III development, including a mutant CALR antibody for MPNs, a protein S modulator for von Willebrand disease, a G12D inhibitor for pancreatic cancer, a TGF-beta by PD-1 bispecific antibody in colorectal cancer, a CDK2 inhibitor for ovarian cancer and a JAK inhibitor currently under regulatory review in HS.
We have increasing confidence in the biology behind these programs and believe we've taken meaningful risks out of them as they've advanced. That does not mean the risk is zero, but increasingly, the risk we are managing is execution risk, running high-quality Phase III programs, enrolling them on time and achieving the regulatory milestones in front of us. Those are things we directly control, and that is our focus today.
We are fully funding and resourcing these opportunities, leaving nothing to chance. And if we deliver against them, we believe the value creation potential is substantial and that is how we should ultimately be judged.
Now we'll frame the quarter around 3 themes. First, key business performance. Every product grew year-over-year. Jakafi had another strong quarter with growth across all indications, and sales from our core business, excluding Jakafi, increased 37% from prior year. Second, we achieved important regulatory milestones, including the approval and launch of Opzelura for moderate AD in the EU in the third quarter. In parallel, the NDA reviews for Monjuvi and frontline DLBCL and povorcitinib in moderate-to-severe HS are well underway. Third, we continue to advance our late-stage pipeline, including trial initiations and expansion efforts for key programs like G12D, TGF-beta by PD-1 and 989. 
I'll now cover the quarter in more detail and then hand it to Pablo to expand on the progress across our pipeline. Total revenue for the quarter was $1.56 billion, representing growth of 14% year-over-year. Total net sales in the quarter were $1.32 billion, up 14% versus the prior year. Growth was broad-based and led by Opzelura and our Hematology and Oncology franchise while Jakafi remained a significant contributor.
Jakafi franchise net sales in the third quarter were $827 million, up 4% year-over-year. Underlying demand remained strong, increasing 12% with growth across all indications led by PV. Net sales growth reflects expected pricing dynamics during the quarter, including the impact of the CMS generous model. Jakafi XR net sales for the third quarter were $15 million. XR share of the franchise increased by approximately 100 basis points in September to approximately 3%. This was driven by both new and existing patients. Formulary coverage is expected to exceed 80% by year-end. The combination of increasing uptake here and expanding market access keeps us on track to achieve our full year-end target of roughly $50 million in XR net sales and supports our goal of retaining 10% to 30% of the Jakafi business by 2029.
Now to our core business ex Jakafi, which is one of the clearest indicators of transitioning the company. Net sales from our core business, excluding Jakafi were $490 million, representing a 30% increase versus prior year, reflecting contributions from key growth brands, namely Opzelura, Niktimvo, Zynyz and Monjuvi. The growth across brands and geographies strengthens the outlook for the company as we see this business growing to $3 billion to $4 billion by 2030.
Opzelura net sales were $255 million in the quarter, an increase of 36% over prior year. Net sales were driven by increased demand across geographies and favorable U.S. pricing dynamics resulting from the agreement with CMS related to the Opzelura line extension. On a pro forma basis, which adjusts the third quarter of '25 for the favorable impact of the Medicaid line extension settlement, total Opzelura net sales increased 21% over the prior year period.
Now I'll break down the U.S. and international performance. U.S. net sales in the third quarter were $208 million, up 45% year-over-year and 25% on a pro forma basis. Importantly, prescription demand increased 24% across both atopic dermatitis and vitiligo. New patient starts, an important leading indicator, increased 26%.
The strong third quarter results reflect the strategy we outlined at the beginning of the year, which include expanding the sales force, taking a more targeted approach with nurse practitioners and physician assistants and improving access quality. We're seeing progress across all 3 of those areas. Internationally, Opzelura net sales were $47 million in the third quarter, up 5% year-over-year. Excluding the benefit from a prior year reversal related to a government rebate program, underlying sales increased approximately 20% year-over-year.
Now vitiligo has been the foundation of our international business to date. Looking ahead, the approval of Opzelura for moderate atopic dermatitis in Europe represents the next phase of growth for the franchise. As the first JAK inhibitor approved for moderate AD in Europe, we expect adoption to build over time as reimbursement expands across Germany and additional European markets in mid-2027. Excluding the onetime U.S. CMS impact, we continue to expect the international business to represent approximately 20% of total Opzelura net sales for the full year. 
Finally, our Hematology and Oncology portfolio delivered net sales of $235 million, an increase of 38% versus the prior year. Niktimvo net sales were $67 million, an increase of 47% versus prior year and approximately 10% sequentially. We expect full year sales to approach $250 million. Zynyz net sales were $58 million, an increase of 157% year-over-year. Uptake in the U.S. and international markets remain strong, and Zynyz is the leading first-line treatment option and only FDA-approved first-line treatment and SCAC.
Monjuvi net sales were $55 million, up 30% year-over-year, driven by follicular lymphoma uptake in the United States and the launch of Monjuvi in Europe and Japan following approvals in follicular lymphoma during the first half of the year. This performance reinforces our belief that we can build a substantial Hematology and Oncology business beyond Jakafi.
With that, I'll turn the call over to Pablo to review our R&D progress.

**Pablo Cagnoni** (Executives):
Thank you, Bill, and good morning, everyone. We're making meaningful progress across our pipeline. Programs that were in early clinical development last year are now in Phase III registrational studies. Today, more than 10 pivotal trials are underway across hematology, oncology and inflammation and autoimmunity, including several programs with the potential to be first-in-class medicines. It is important to highlight how we got here. Each decision has been driven by data. We advance programs where the evidence is clear and focus on the treatment settings that can offer the greatest opportunity for patients and physicians. This discipline built into our discovery and clinical organization gives us confidence that we can continue to deliver. 
Today, I will cover the progress we have made year-to-date and during the quarter and highlight what lies ahead. Starting with myeloproliferative neoplasms, or MPNs. Our ambition is to develop molecularly targeted treatments for every patient with an MPN by the beginning of the next decade. These efforts are anchored by 989, our mutant CALR monoclonal antibody and the first mutation-specific therapy in late-stage development for CALR-mutated MPNs.
Last year, we presented the first clinical data in patients with CALR-mutated essential thrombocythemia and myelofibrosis, which established the foundation for our development strategy. Our registrational program in second-line ET is underway with site activation ongoing and the first patient treated during the third quarter. In second-line MF, we have had productive conversations with the FDA, including alignment on the Phase III EXCALIBUR-MF2 study. We expect to initiate the study by year-end.
The Phase III randomized study will evaluate 989 against best available therapy in patients with CALR-mutated myelofibrosis who have previously received a JAK inhibitor. The study will enroll patients with both type 1 and non-type 1 CALR mutations with mutation-specific dosing informed by our Phase I experience. The co-primary endpoints are spleen volume reduction of at least 35%, or SVR35, and total symptom score reduction of at least 50% or TSS50 at week 36.
The week 36 assessment allows additional time to capture the full magnitude and durability of treatment benefit, consistent with the targeted treatment approach that we believe has the potential to address underlying disease biology. These are established endpoints consistent with those used for current approved therapies in MF. Notably, we're also evaluating a composite endpoint as a key secondary endpoint. The composite endpoint is designed to capture the benefits we have observed beyond spleen and symptoms, including improvements in hemoglobin, platelet counts and blasts in peripheral blood. This allows us to further characterize the potential benefit of a disease-modifying therapy on key manifestations of MF.
The study is powered to evaluate efficacy in patients with type 1 mutations, who represent more than 70% of the CALR-mutated MF population and have experienced the most robust clinical responses to date. We will also continue to generate data in patients with non-type 1 mutations to further characterize the potential of 989 across the broader CALR-mutated population.
Looking ahead, we expect to share the first clinical data for 989 in first-line MF by year-end, both as monotherapy and in combination with ruxolitinib. This data will help define the role of 989 in an early treatment setting and inform our development plans in 2027. Additionally, we plan to share preclinical data on our next-generation mutant-CALR antibody, which we will be progressing into the clinic in early 2027. Together, these efforts reflect our strategy to build a broader portfolio of mutation-directed therapies with the potential to meaningfully change the treatment paradigm for patients with MPNs.
Beyond MPNs, we continue to advance important programs across our hematology pipeline. The FDA's review of tafasitamab in first-line diffuse large B-cell lymphoma, or DLBCL, is ongoing with approval expected in the first quarter of next year. In chronic graft-versus-host disease, we are evaluating axatilimab in early lines of therapy. This includes a Phase II study of axatilimab in combination with ruxolitinib with results expected at a medical meeting early next year and a Phase III study evaluating axatilimab in combination with steroids with top line results anticipated in 2028.
We also expanded our hematology pipeline this quarter with the acquisition of Vega Therapeutics and its lead therapy, latarcibart. This novel proteinase modulator has the potential to be a transformative nonfactor replacement treatment for von Willebrand disease. The pivotal Phase III study is underway with top line data expected in early 2029. We also plan to share additional data from the Phase I open-label extension later this year.
Turning to oncology. We have advanced our solid tumor programs from early clinical development to a growing late-stage pipeline. A year ago, we established clinical proof of concept across several novel mechanisms and tumor types. Today, we have pivotal programs underway for our KRAS G12D inhibitor, our TGF-beta receptor 2 by PD-1 bispecific antibody and our CDK2 inhibitor with expansion efforts planned for next year.
As we reviewed at ESMO earlier this week, our strategy is to advance novel mechanisms in high incidence cancers where outcomes remain poor with a particular emphasis on building a leading gastrointestinal franchise anchored by 734 and 890. Starting with 734, our G12D inhibitor, our conviction in this program continues to grow, and we are rapidly expanding its development across tumor types, treatment settings and novel combinations. At ESMO, we presented Phase I data evaluating 734 in combination with standard of care chemotherapy in first-line pancreatic ductal adenocarcinoma, or PDAC, and in combination with cetuximab in heavily pretreated patients with colorectal cancer.
In PDAC, 734 showed encouraging activity in combination with both standard of care chemotherapies with a safety and tolerability profile consistent with this established regimens. Objective response rates confirmed and pending were 58% for 734 plus gemcitabine and nab-paclitaxel and 81% for 734 plus modified FOLFIRINOX. We also see promising signals of durability with 6-month landmark PFS of 80% and 90%, respectively.
The depth of response, early signs of durability and consistent tolerability across both chemotherapy backbones reinforce our confidence in the ongoing Phase III DAWN-303 study in first-line PDAC, and support moving 734 into early stage of disease with a Phase III study in adjuvant PDAC planned to start in 2027.
Turning to colorectal cancer. 734 in combination with cetuximab produced a 36% objective response rate in heavily pretreated patients. This is notable because anti-EGFR therapy alone has historically produced response rates below 5% in late-line colorectal cancer, which suggests a synergistic combination. This data informed the design of our Phase III DAWN-302 study in previously treated colorectal cancer. We reached alignment with the FDA on the design this quarter and plan to initiate the study in the first half of next year.
Beyond these registrational programs, we recently announced clinical collaborations, enabling evaluation of 734 with novel combinations. This include petosemtamab and EGFR by LGR5 bispecific antibody in first-line colorectal cancer; navlimetostat, a PRMT5 inhibitor and PDAC, and SNV1521, a PARP1 inhibitor in solid tumors. These Phase I studies will begin next year.
Turning to 890, our TGF-beta receptor 2 by PD-1 bispecific antibody. We believe 890 has the potential to serve as an immunotherapy backbone, starting in microsatellite stable colorectal cancer, or MSS CRC, a disease that has historically been resistant to immunotherapy. At ESMO, we presented Phase I data evaluating 890 in combination with standard of care chemotherapy in first-line MSS CRC. 890 in combination with FOLFOX and bevacizumab showed encouraging antitumor activity with an objective response rate of 71%.
Importantly, responses were observed across patient subgroups, including an objective response rate of 83% in patients with liver metastases, a population historically associated with poor outcomes and reduced responsiveness to immunotherapy. We also see early signals of durability with a 6-month landmark progression-free survival of 81%. We look forward to sharing more mature progression-free survival data next year. This data support our ongoing Phase III NEXERA-303 study in first-line metastatic MSS colorectal cancer, which is well underway with top line data expected in 2029. We're also moving 890 into earlier treatment settings, including a proof-of-concept study in patients with circulating tumor DNA-positive disease following surgery and adjuvant chemotherapy.
Finally, turning to 667, our CDK2 inhibitor. Based on the evolving treatment landscape, we are focusing our development on first-line maintenance in cyclin E1 overexpressing ovarian cancer, where we believe the opportunity for 667 is greatest to offer a more meaningful treatment option for patients and physicians. As a result, we are deprioritizing development efforts in platinum-resistant ovarian cancer. The open-label Phase II MAESTRA-1 trial remains ongoing. However, we have made the decision to stop additional site activation and discontinue future enrollment in the randomized Phase III MAESTRA-2 study. This was not an easy decision, and we're grateful to the investigators and patients who participated in this study.
Stepping back, in a short period, we have moved from established proof of concept to advancing multiple registrational programs in oncology. We have done so by following the data, and we will continue to deliberate about where we invest. With that approach, we believe we're well positioned to build multiple oncology franchises over time.
Turning to IAI, where we continue to build on our leadership in dermatology across topical and systemic therapies. In July, the European Commission approved Opzelura for adults with moderate atopic dermatitis, or AD. This approval makes Opzelura the first steroid-free topical JAK inhibitor available in Europe for this population and expands its EU label into a second indication.
Povorcitinib, our oral JAK inhibitor, received a positive CHMP opinion for the treatment of moderate-to-severe HS in adults who have had an inadequate response to anti-TNF therapy. We anticipate a potential approval in Europe by year-end. In the U.S., the NDA is under review with an anticipated approval in the first quarter of 2027.
We also expect several important Phase III readouts by year-end, including top line results from ruxolitinib cream in mild-to-moderate HS and povorcitinib in prurigo nodularis. Together, these programs position povorcitinib for potential approval in multiple indications, including HS, PN and vitiligo, building on the foundation Opzelura has established in dermatology.
To close, the pipeline we have today looks very different from a year ago. We have moved multiple novel programs into registrational development, and we have done so deliberately, guided at each step by the data. With a more mature and diversified late-stage pipeline, supported by the discovery and clinical engine behind it, we're well positioned to deliver meaningful innovation for patients and support sustainable top line growth heading into the 2030s.
With that, I will turn it over to Suky for a financial update on the quarter.

**Suketu Upadhyay** (Executives):
Thank you, Pablo, and good morning. I'll begin with comments on our third quarter results and then turn to our updated full year outlook. As Bill mentioned earlier, we delivered strong net sales, managed expenses well and executed across all areas of the company.
Total revenue for the quarter was $1.56 billion, an increase of 14%. Total net sales were $1.32 billion, reflecting 14% growth versus the prior year, driven by strong product demand. Total GAAP expenses for the quarter were $2.27 billion, an increase of 146% compared to the prior year. This includes a $1.23 billion IP R&D expense related to the closing of the Vega acquisition. Total cash consideration for the transaction was approximately $1.27 billion, including [ $1.25 billion ] for the upfront. When we exclude the Vega-related IP R&D expense, total operating expenses for the quarter grew 12%.
GAAP cost of goods sold was $109 million, representing approximately 8% of total net sales. This is in line with our expectations, and we expect COGS to be approximately 8% for the full year. Our GAAP R&D expenses were $1.79 billion for the quarter, an increase of 254% versus the prior year, driven by the Vega acquisition and continued investment in our late-stage development assets across Hematology and Oncology. Excluding the Vega acquisition, GAAP R&D expenses increased 11% for the quarter.
Moving to SG&A. GAAP SG&A expenses were $364 million for the quarter, increasing 11% year-over-year, driven by prelaunch activities for povorcitinib. And lastly, we ended the quarter with $3.9 billion in cash and cash equivalents.
Now turning to our outlook for the remainder of the year. We are maintaining our full year guidance for the Jakafi franchise of $3.220 billion to $3.270 billion. Demand and pricing performed in line with our expectations, and we successfully absorbed the impact of the CMS generous model, which on an annualized basis will be roughly 1% of Jakafi gross sales.
We are raising our full year guidance for Opzelura, Hematology and Oncology and total net sales based on the strong performance delivered through the first 9 months of the year. For Opzelura, we are raising full year 2026 net sales guidance to $1.100 billion to $1.120 billion, reflecting continued growth in both the U.S. and international markets.
For Hematology and Oncology, we are raising full year guidance to $890 million to $910 million, reflecting the performance across key growth brands. As a result, we are increasing total net sales guidance to $5.210 billion to $5.300 billion.
We are also maintaining our full year operating expense guidance. While unchanged, based on our year-to-date R&D investment and expected spend in the fourth quarter, we expect total R&D and SG&A expenses to be towards the middle of our full year range, reflecting investments in our late-stage development pipeline and pre-commercialization efforts. To close, we are pleased with our performance for the quarter and the first 9 months of the year, and we remain confident in our outlook.
With that, I'll turn the call back over to the operator and open it up for Q&A.

**Operator** (Operator):
[Operator Instructions] Our first question is coming from Tazeen Ahmad from Bank of America.

**Tazeen Ahmad** (Analysts):
So I just wanted to ask you, what are the key items we should be focusing on for the update for 989 mCALR in the frontline MF study coming up this quarter?

**William Meury** (Executives):
Thanks, Tazeen. Pablo will take the question.

**Pablo Cagnoni** (Executives):
Tazeen, thank you for the question. So at ASH, we're going to present, as promised, an update on the first-line data. Now just as on the side, you remember that at EHA, we presented data in patients that were ineligible for Jakafi. And the data looked quite good in our opinion, both on SVR35 and TSS50 as well, the anemia improvement that we've become accustomed to see in patients treated with 989. 
So to complement that or to expand on that at ASH, we're going to have about a total of 55 patients in frontline. Of those, about 20 are in that group of ineligible and the other 40 or so are in true first-line patients that would have been eligible for Jakafi. There's a split between single agent and combination with ruxolitinib, about 2/3, 1/3 approximately.
And importantly, we have quite a bit of follow-up in those patients at this point. In fact, one of the things that I think is important to highlight is the data in the abstract are much more immature than the data in the presentation. In fact, the data cut in the presentation about 4 months later than the date in the abstract. So I would ask you when the abstracts come out, which is in the relatively near term, that we wait for the data in the presentation because that's a truly relevant data. So I think it's a pretty comprehensive update. I think it will give a clear idea of the role of 989 potential in frontline MF, and we look forward to sharing the data with you.

**Operator** (Operator):
Your next question today is coming from Etzer Darout from Barclays.

**Gustave Diep** (Analysts):
This is Gustave, on for Etzer. My question is on the second line MS pivotal for 989. How will prior JAK inhibitor treatment be defined? Would the patients need to be resistance, refractory or intolerant? And is there a minimum duration of treatment or dose for those?

**William Meury** (Executives):
Go ahead, Pablo.

**Pablo Cagnoni** (Executives):
I mean the definition is pretty standard in the fact that patients don't achieve ideal SVR35 or ideal -- spleen or symptom response to Jakafi or usually, the reason for intolerance is either thrombocytopenia or anemia in most patients. So the physicians make that determination. There's a language in the protocol, but the physicians will make that determination. And there's no minimum duration. I don't believe -- I would have to confirm with the product. I don't believe there's any minimum duration of treatment or dose of Jakafi. The dose of Jakafi prior to entering a second-line study is not predetermined in the second-line study at all.

**Operator** (Operator):
Our next question today is coming from Jessica Fye from JPMorgan.

**Silvia Luo** (Analysts):
This is Silvia, on for Jess Fye. Can you elaborate on the strength that you are seeing in Opzelura? And are you able to quantify the gross to net you saw this quarter and how that differed from third quarter '25?

**William Meury** (Executives):
It's a good question. I'll make a few comments and then Pablo -- I mean, Mohamed can expand on them. At the start of the year, we made a very deliberate strategic decision to expand the sales force, increase promotion to NPs and PAs, and to improve access quality, which required an investment. And if you look at the results this quarter, you focus on 2 key metrics: underlying prescription demand, and new patient starts. And it's been strong now for several months. I think it's an important indicator of the strength of the business, not just to finish the year, but in 2027.
Opzelura has a very large prescriber base of 20,000 physicians. We have extensive formulary coverage. And we have probably north of 0.25 million people receiving Opzelura today. And so that is a moat around the business. And our job right now is really simple, keep the pressure on keep our foot on the gas pedal and this business could represent over 1/3 of our core business ex Jakafi when we hit the transition in 2029. And Mohamed and his team has done an excellent job managing this product for the past several quarters.
Mohamed, do you want to add anything?

**Mohamed Issa** (Executives):
Yes. Maybe just to quantify a few of the points that you mentioned, Bill, thank you. Just to reiterate, in the U.S., we grew net sales 25% on a pro forma basis, which basically accounts for the GTN benefit that you would have seen from the line extension settlement that we declared. And on top of that, right, that 25% was driven by a 24% overall demand growth year-over-year. So the majority of the pro forma growth was driven by demand. And actually, there was a little bit of a price downside on that when you look at it on a pro forma basis.
So the growth of the business is really, really healthy. And a lot of the growth, as you can see, is coming from the brands underlying health of the business, which is demand. And like Bill mentioned, new patient volume, which is really the best measure of competitiveness, grew 2x market when you think about AD and vitiligo. So not only are we growing, but we're growing and we're outpacing the market, which is a really good indicator of not only the health of the business, but our competitiveness overall.

**William Meury** (Executives):
And Silvia, just to add one thing to what Mohamed just said. When you think about price for Opzelura, 2026 was a year of investment to improve the quality of formulary coverage. When we look out '27 and beyond, think about price as a maintenance strategy. there's a cost to maintaining coverage, but we don't expect significant headwinds as it relates to average selling price for Opzelura.

**Operator** (Operator):
Next question today is coming from Salim Syed from Mizuho.

**Erik Lavington** (Analysts):
This is Erik, on for Salim. Congrats on the quarter. One on axatilimab in GVHD. It looks like the first-line axa plus rux readout got pushed out from 4Q '26 to 1Q '27. Just curious about the puts and takes on that and how are you thinking about the overall time line on that at this point if that's different?

**William Meury** (Executives):
Thanks for the question, Erik. Pablo will take it.

**Pablo Cagnoni** (Executives):
So the reason for that is simply to present the data -- to present a comprehensive data set at the most relevant meeting, which is in the first quarter of 2027. The data wasn't ready for submission to an earlier meeting. We don't want to just show the primary endpoint. We want to show you durability of the response. We want to show you subsequent therapy, a comprehensive review of the safety profile. So we want to present that at a meeting and a scientific meeting and the most appropriate one is in the first quarter of 2027. That's the only reason for shifting the time line a little bit.

**Operator** (Operator):
Your next question today is coming from Brian Abrahams from RBC Capital Markets.

**Brian Abrahams** (Analysts):
Congrats on the continued progress. Maybe one on 989. I guess I'm curious what monotherapy or combo activity do you think you would need to see and KOLs would want to see to warrant development of 989 as a frontline alternative or add-on for treatment-naive CALR mutated patients, just given the known benefits of Jakafi, but also the known AEs?

**William Meury** (Executives):
Great. Go ahead, Pablo.

**Pablo Cagnoni** (Executives):
Thank you for the question. Let me give you a little bit of a more comprehensive answer here because I think it's important. I know it's in everybody's mind. So we need two pieces of data to finalize the design of a frontline study in MF. First of all, let's go back to the comment I made a few minutes ago. We know from the EHA data in ineligible patients that the efficacy in 989 untreated, rux untreated patients with MF is substantial.
You all remember the SVR35 and TSS50 data, we showed and the really striking effect on anemia improvement. So what we need now is a more comprehensive data set with longer follow-up, which we will have at ASH, including single agent and combination with Jakafi, as you pointed out. We need to see that data in order to decide the final decision on the design of the frontline study.
The other event that needs to happen is, we will have a meeting with the FDA, a type C meeting with the surrogate endpoints team to discuss -- continue the conversation that we've had on the use of a composite endpoint to try to shift away from SVR35 or TSS50 because we believe disease-modifying therapies, like 989, need to be looked at differently. We need to address the fact that this medicine basically shifts hematopoiesis back to normal, and that is represented by improvement in anemia, reduction in fibrosis, reduction of mutated megakaryocyte in the bone marrow, et cetera, that needs to be addressed. So once we complete those conversations with the FDA and once we have the full data set, we will make the decision on the frontline study. 
Going directly to your question, we do know that Jakafi produces rapid improvement in symptoms, and in SVR35 and CALR-mutated patients in frontline of approximately 20% to 22%. We think there's a lot of room for improvement there. Whether we need a combination arm in the study or not, we'll decide based on the points that I just made. We do think there might be a role in which case, we'll launch a 3-arm study, which would be rux versus rux plus 989 versus 989 alone. That's a perfect legitimate study. Patients and physicians will have two options to treat their MF, either single-agent 989 or combination with rux and all that will be decided in the next few months, and we'll update you early in 2027.

**Operator** (Operator):
Next question today is coming from Evan Seigerman from BMO Capital Markets.

**Evan Seigerman** (Analysts):
So just taking a step back, the pipeline progress that Incyte has accomplished over the past year has been impressive. Can you just level set kind of remind us what you've accomplished over the past year? And then looking forward, aside from mCALR at ASH, what are some things that we should be focused on over the next year so that when we get to the 3Q call we can discuss those as well?

**William Meury** (Executives):
Thanks for the question, Evan. I agree with you. I think the shape and maturity of the pipeline has changed over the past 12 months. I also believe it is the right balance of risk and reward. In other words, the pipeline is not consumed on one hand by moonshots, and on the other hand, by safe, low-return bets. We sort of have a combination of products that can deliver, what I would describe as, outsized returns potentially with products that can deliver incremental but reliable growth over time.
More specifically, we have 6 assets right now in Phase III. They're not all equal when you think about them on a sort of risk-adjusted value basis. Povacitinib, 989, 12D and latarcibart are comparatively higher PTRS projects. TGF-beta by PD-1, the fifth asset, is different, significant potential value, but more biology risk. So in our strat plan, it has the widest range of possible outcomes, whereas the other 3 or 4 anchor franchises for us. CDK2, the last one, I would describe as an incremental opportunity. That's how we view it.
I don't think the pipeline thesis for Incyte is trading on any one opportunity. And I do believe that the pipeline we have right now has the potential to support our target growth rate post 2029. Now is it enough? If we execute, then the answer is yes. But as you know, these are probabilistic opportunities, and attrition is a fact of life. And our job is to sort of keep this product line moving. We can't declare victory yet.
Over the next 12 to 18 months, you will receive updates on many of these programs, at least Phase I updates, as we're running the Phase III programs, and you will receive updates on how we are expanding each program, the initiation of studies, and Pablo talked a great deal about our GI oncology program at ESMO. And we'll provide you and everyone else with visibility into how we are advancing this pipeline so that there's more clarity on the growth potential of Incyte post '29 on top of the core business.

**Operator** (Operator):
Our next question today is coming from Andrew Berens from Leerink Partners.

**Andrew Berens** (Analysts):
Congrats on all the progress. It's great seeing you guys in Madrid. I don't know about you, but I'm practicing by Spanish as an insurance policy against next week. Maybe a bit of color on the decision to deprioritize PROC for the CDK2. We noticed there wasn't a focus at your event on Monday, but we thought it really looked pretty good relative to some of the other oral programs in the same setting. Was it the trial wasn't enrolling well or something else that you saw?
And then if I could just sneak in a little more on the MF program and the endpoints. I know you did give some color. But what's your sense of the regulatory buy-in for the potential to get a biomarker-driven endpoint eventually in the frontline setting?

**William Meury** (Executives):
Pablo will take the question.

**Pablo Cagnoni** (Executives):
Thank you, Andy. Good to see you earlier this week. So it's the competitive landscape mainly. So look, we like 667. The data in combination with bev, as you saw and you pointed out, we thought looks pretty strong, 48% response rate in the late-line population. But the data that has continued to accumulate in platinum-resistant ovarian cancer with ADCs convinces that, number one, the study will be very challenging to accrue; and number two, the commercial prospects in that indication were limited.
Now we continue to believe that there will be a role for an oral option for these patients, particularly in molecular targeted population. The maintenance study continues. And we do have a large data set in platinum-resistant disease that we'll discuss with FDA. Now I think the probability of accelerated approval on that basis is very, very small because there's very clear evidence that, A, randomized trials can be run in that disease; and B, the efficacy has been superior to what we've shown with 667 to be very frank. So that's kind of the basis for discontinuing that one study.
On MF, look, a surrogate biomarker endpoint would be ideal. I don't think we're there. And I don't think we're there mainly because I'm not sure what that endpoint would be today. We talked about VAF and VAF is an interesting way to monitor to some extent, the progress, but it's far from an ideal endpoint because, as you know, VAF and peripheral blood measures a lot of cells that are not relevant to the treatment effect of 989 or any CALR antibody.
What we do believe, however, is that it's time in MF to consider alternative endpoints to SVR35 and TSS50. And that is incorporating different measures of normal hematopoiesis, hemoglobin platelets as well as blasts in peripheral blood as well as spleen volume, quite honestly. That is a better way to characterize a treatment response to a drug like 989. And also those factors are better predictors of long-term survival in MF patients that's simply using SVR35 and TSS50. And that's why we want to continue that conversation with FDA.

**Operator** (Operator):
Our next question is coming from Salveen Richter from Goldman Sachs.

**Salveen Richter** (Analysts):
Could you speak to what you'll share with regard to preclinical data for your next-generation antibody at ASH? And how we should think about the profile of this asset versus 989 in competitors? And then also how you would position your bispecific, given the similar pathway?

**William Meury** (Executives):
Thanks for the question, Salveen. Go ahead, Pablo.

**Pablo Cagnoni** (Executives):
Thank you, Salveen. Good to see you early this week. Let me make 2 points that I think are really important. Based on the preclinical data that has been disclosed by our competitors and the preclinical data that we have on hand, I think our next-generation CALR antibody is the best-in-class CALR antibody out there. The reason for that is we've optimized every property that we thought we had to optimize on 989.
This novel medicine is 70x more potent against non-type 1 mutations, and it has a much longer half-life. You'll see the details at ASH, but it will allow at least for monthly subcu injection, maybe even less frequent depending on what we see in patients. It will be subcu, obviously, from day 1. We expect that the dose that's going to be required is going to fit in a pen. So we really believe that this will address some of the limitations that 989 has. And as excited as we're getting 989 approved for patients with ET and MF, we think that this next gen will be very helpful in the longer run.
Just, I know you didn't ask about that one, but we're also going to present data on the next-gen V617F inhibitor. We think this drug addresses a lot of limitations that we had with our previous entry in this space. So we look forward to sharing that data with you.
Regarding the bispecific, as we've discussed a couple of times over the past year, I need to see more data to understand exactly where the bispecific will be positioned in patients with MF. Efficacy and safety will determine what kind of a role this medicine potentially can play in this disease, I think possibly in patients with more accelerated MF that need a more rapid tumor reduction. But if the data with 989 continues to look better and better, one could argue that the space for the bispecific could become a little bit more limited.

**Operator** (Operator):
Next question today is coming from Jay Olson from Oppenheimer.

**Jay Olson** (Analysts):
Congrats on all the progress. For 734, what are your plans for combination strategies in PDAC and CRC, especially with the positive news from petosemtamab, how are you thinking about moving 734 into earlier lines in combination with petosemtamab?

**Pablo Cagnoni** (Executives):
So the combination that we announced is, in fact, to study 734 in combination with petosemtamab and FOLFOX in patients with colorectal cancer. Obviously, you need to do a Phase I study first, but the idea is to move to frontline therapy as quickly as possible. We reviewed the landscape of novel EGFR inhibitors. We decided, and I think the data that was released yesterday confirmed that, that was the right choice. We believe that petosemtamab is the best next-generation EGFR inhibitor, and that's why we put that collaboration in place.

**Operator** (Operator):
Our next question is coming from Ash Verma from UBS.

**Unknown Analyst** (Analysts):
This is [indiscernible] on for Ash. So I have one on the G12D program. Can you talk about your enrollment strategy for Phase III and fourth line PDAC? It seems like some of the other competitors are flagging the need to enroll from ex U.S. sites given increased new agents use in the front line. So what percent of patients do you intend to enroll from U.S. as well as ex U.S.? And do you have agreement with the FDA on the enrollment mix?

**Pablo Cagnoni** (Executives):
So it's an important question, and we looked at it in a couple of different ways. First of all, in terms of enrollment itself, it's going extremely well. So we have no concerns at this point. We're not going to yet provide an exact timing for completion of enrollment. But based on our initial projections, it's on track, if not a little bit ahead of schedule. So that's going very well. No concerns there.
Now the question, it's important to answer what happens if a lot of daraxonrasib gets used in patients that progress and whether that treatment effect of daraxonrasib post progression is different in the 2 arms of the study. We've done extensive statistical modeling. We're going to track that in the study and we can potentially shift to countries where daraxonrasib is not approved if we see that that's happening in a lot of patients. 
I would say at this point, we already have more than enough patients enrolled in the U.S. to be sufficient for an FDA submission. So I have no concerns about not having enough U.S. patients. What we will monitor though is post progression daraxonrasib use to make sure that, that does an impact the post progression of PFS2 in a way in one or more than the other. And if there is a need for intervention, we will shift to countries with daraxonrasib is not approved.

**Operator** (Operator):
Our next question today is coming from Gavin Clark-Gartner from Evercore ISI.

**Gavin Clark-Gartner** (Analysts):
I just wanted to ask on the second-line MF mCALR study. Are there any limitations on the percent of patients that can receive a JAK inhibitor in the best available therapy arm? And what are your expectations for what that number will be? And just to clarify on the primary endpoint. So that's type 1 only. When you do hierarchical testing, do you go look in the ITT population? Or do you specifically then look in the nontype 1 population?

**Pablo Cagnoni** (Executives):
No, there's no other mutation in the percentage of patients that can receive a JAK inhibitor. As you know, if you look at the data, one has to be careful to looking at studies that allow versus did not allow washout after prior line first-line therapy, the prior line therapy prior to entering a second line study. So the SVR35 is as low as 8% in patients depending on whether they did or did not have washout. Our data that we presented at ASH, which is close to 40% SVR35 and about 40%, 45% TSS50, it's in patients with no washout that obviously are expected to do worse. So that's important to remember. So we feel very confident that all the approved therapies in second line are substantially inferior to what we've seen with 989 so far. 
The only other comment I'm going to make about the statistical testing is that the primary endpoint is in type 1 patients. We thought that was the right way to run the study to ensure success and to get this medicine approved for these patients, which are about 2/3, if not a little bit higher of the patients with CALR mutations. We will collect the data in nontype 1 patients. Obviously, we'll have it available, but the primary analysis of the study is in type 1 disease.

**Operator** (Operator):
Your next question today is coming from John Newman from Canaccord Genuity.

**John Newman** (Analysts):
Congrats on all the progress. You previously stated that at least at this point in time, you probably won't pursue combinations with your G12D and a pan-RAS inhibitor. I'm just wondering, outside of the work that you're doing with your G12D, have you considered at all licensing G12D as a vector, it seems like an area where there are a few competitors with maybe not quite as many yet as G12D?

**Pablo Cagnoni** (Executives):
Great question. On the pan-RAS, we don't rule out doing a combination with the pan-RAS. We are continuing to scan the landscape to see if there is an option that is suitable for us. So we're not ruling it out. I mean we're very clear. We've done preclinical work, and we think there's value in the combination. In terms of G12D, we are interested in expanding our KRAS franchise. So also, we would not rule out, at some point, addressing patients with G12D mutations.

**Operator** (Operator):
Next question today is coming from Michael Schmidt from Guggenheim Securities.

**Michael Schmidt** (Analysts):
I just had another follow-up on 989. So thinking about the possible registration strategy in frontline MF patients, will the focus there also primarily be on type 1 patients with a 36-month endpoint? Or would that include a broader opportunity? And how will you position the next-gen CALR antibody relative to 989 in that context?

**Pablo Cagnoni** (Executives):
Michael, on the first part, we'll see where the data takes us. Right now, we continue to develop 989 to try to address the needs of all patients with CALR mutations. We made a decision in second line as we just discussed. In frontline, the data will guide that decision. So let's talk after ASH, and then we can -- once we both have the data in front of us, we can see what that looks like. Now remember, a potential path in first line, as I discussed a few minutes ago, is a 3-arm study with Jakafi in combination with 989. In that case, that calculation might change a little bit. So let's keep that in mind as we review the data at ASH. 
On the next gen, right now, the positioning is getting to the clinic as fast as possible, getting to pivotal trials as fast as possible. We think that if we reach an agreement with FDA on the starting dose, our current understanding of this target will allow us to have a very short dose escalation period. If you remember, 989, we had to start at 50 to 70 milligrams, and we had to escalate all the way to 2,500 milligrams. That took a long time. It is not going to be the case with the next generation program. We think we can get to the recommend the Phase II dose much faster. And our goal is to start pivotal trials with next gen in 2028.

**Operator** (Operator):
The next question is coming from Mitchell Kapoor from H.C. Wainwright.

**Amit Dayal** (Analysts):
This is Amit, on for Mitchell. I guess looking at 734 and DAWN-302, what supports 34 and cetuximab combo replacing second-line chemo? And will DAWN-302 second-line cohort be large enough to establish benefit independently of third-line results?

**Pablo Cagnoni** (Executives):
Let me see if I understand the question. So you're asking about the design of the 302 of the colorectal trial?

**Amit Dayal** (Analysts):
Yes. I was just wondering if you will be able to distinguish the benefit in second line versus third line patients?

**Pablo Cagnoni** (Executives):
It's a good question. In general, I expect -- let me put it this way. I expect that the study will enroll predominantly third-line patients because the control arm will allow LONSURF bev, which was the winning arm of the SUNLIGHT study as well as regorafenib and fruquintinib. And when you put those options in the control arm, you're more likely to end up with a third-line shifted population. So whether the data at the end are sufficient for a broad label, time will tell. It depends on the population we enroll, depending on the results of the study. So based on the control arms, that's what we expect.
Now I wanted to use this question to address one point also, which I think is very important about the DAWN-302 study just to make sure we're all clear on what the expectations are of the control arm. The SUNLIGHT study had a PFS of about 5.6 months, and that was cited by several as the benchmark. Importantly, in the SUNLIGHT study, bev-exposed patients had a PFS of 4.5 months, which is substantially lower. And DAWN-302 will be in bev-exposed patients. So we expect the control arm overall will underperform the overall SUNLIGHT study.
The other point that's important is we run a real-world analysis with Tempus showing that the SUNLIGHT study population and patients with KRAS mutations do worse on LONSURF bev than patients that are wild type. So based on that, we think that reassured us that the probability of success of DAWN-302 is quite high considering the expectations for the control arm.

**Operator** (Operator):
Next question today is coming from Derek Archila from Wells Fargo.

**Jacob Goell** (Analysts):
This is Jacob, on for Derek. Can you just provide us some of your thoughts on label scenarios for Povo and HS? And what analogs do you could point to there for the launch?

**William Meury** (Executives):
I think there are basic label scenarios. We studied both a pre- and post-biologic population. And so that would be clearly the preferred label scenario. The other is just simply a post-biologic population, and there are JAK inhibitors, for example, an AD that have an indication, different data set, different indication post biologics. I think that they're both workable paths.
I think the biggest opportunity for povacitinib is it can be used at both inflection points, a moderate-to-severe patient diagnosed with HS who has been only receiving antibiotics and steroids, which are imperfect solutions. That's a large pool of patients. And then after a biologic for patients who have active disease aren't achieving consistent pain relief or a loss of response, which has been well documented, especially with TNF alpha.
We're in discussions right now with the FDA. And as part of planning for this launch, we plan for both plausible outcomes. We've not seen the label. We expect that the data will support a broad label, but I'm laying out the range of possibilities. 
And I'll let Mohamed comment on how to think about analogs?

**Mohamed Issa** (Executives):
I think Bill, really not much to add. I mean the analogs that we've seen so far will really dictate based on the data. And we believe we have a broad label that supports a broad indication and different analogs, I think, in the marketplace today, so just the same based on the data sets that were submitted in their pivotal program. So we'll wait and see. But like Bill said, I think the most important point is that both scenarios are very workable, and we're very optimistic about the opportunity.

**Operator** (Operator):
Your next question is coming from Eric Schmidt from Cantor Fitzgerald.

**Imogen Mansfield** (Analysts):
This is Imogen, on for Eric. Does the trial on clinicaltrials.gov for an antibody in MPNs INCA036978 that started enrolling earlier this year as monotherapy and in combo with standard disease directed therapy. Could you just tell us a little bit about that program? And is it targeting CALR or something else?
And then one question on povo. In the mild-to-moderate HS population, we've heard very encouraging feedback from KOLs here if this ends up being a positive set of Phase III studies. Why do you think that peak sales could get to for Opzelura -- sorry, not for povo, but for Opzelura in HS?

**William Meury** (Executives):
Great. I'll turn over the first part of your question, Imogen, to Pablo?

**Pablo Cagnoni** (Executives):
Thank you for the question. At this point, we're not going to disclose the target. All I would say is that, that antibody is mutation-agnostic antibody for patients with MPN, so you can potentially target CALR as well as 617F as well as MPPA mutations, and we'll disclose the actual target at the right time, Imogen. I'm sure you'll understand.

**William Meury** (Executives):
And Imogen, I think your question was about Opzelura and HS. And I think the backdrop here is really important. There is no FDA-approved oral anti-inflammatory and there's no FDA-approved topical. Now the study we did was in mild-to-moderate HS, and so there's some overlap with POVO, but not a lot. Our math is, there's a couple of hundred thousand patients, roughly maybe 300,000 in that mild-to-moderate segment.
And if you picked up 10%, 15% of that or more, it could be a 5% to 10% lift on Opzelura. We have to wait for the data in the fourth quarter but it could produce $50 million, $100 million in incremental sales, I think, is not a heroic assumption. We'll wait and see what the data looks like, and it will be a part of the growth story. It's not necessarily built into our models right now. We're just waiting for the data.

**Operator** (Operator):
Our final question today is coming from Tara Bancroft from TD Cowen.

**Tara Bancroft** (Analysts):
So I was hoping maybe you could tell us the time line to the clinic for 954, the V617F, and what we should focus on in the preclinical data that's most indicative of potentially improved clinical profile versus 958?

**Pablo Cagnoni** (Executives):
Certainly. So the entry into clinic for next gen V617F, 954, will be early 2027. We never disclose the exact date, but it's going to be in the early part of 2027. The main thing that we wanted to address here compared with our previous entry was improving the selectivity and important in this case to always remind ourselves that what matters is selectivity between wild-type and V617F mutated cells. This is not a JAK1/JAK2 selectivity question. It's wild-type versus mutated cells. And we've run extensive preclinical studies that you'll see at ASH. And we think the selectivity of this molecule is substantially better than our previous V617F inhibitor. So we feel much better about that.
The second is, we worked the formulation ahead of time. If you remember, we had to do a lot of work on the formulation of 054. Now the formulation that we're going into the clinic, we feel much better about. So both the formulation side and the selectivity of the molecule and the margin in preclinical tox studies are much better than 054. So we're really excited about moving this program forward.

**Operator** (Operator):
We've reached the end of our question-and-answer session. And ladies and gentlemen, that does conclude today's teleconference and webcast. You may disconnect your lines at this time, and have a wonderful day. We thank you for your participation today.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### INCY_Q1_2009_Earnings_Call_20090507.md
- 2009-05-07｜CFO｜guidance：全年現金使用財測維持122–128百萬美元，不含潛在合作夥伴付款（原話："cash use guidance for the year remain unchanged"）
- 2009-05-07｜CFO｜margin：Q1期末現金與投資175.6百萬、當季現金使用42.2百萬，CFO稱符合計畫（原話："our cash use this quarter was 42.2 million"）
- 2009-05-07｜CFO｜margin：Q1 R&D費用29.6百萬，低於2008年Q1，聚焦近期價值程式（原話："R&D expense totaled 29.6 million"）
- 2009-05-07｜CFO｜guidance：CFO回答R&D費用走勢今年將相當平穩（原話："It should look pretty flat this year, Tom."）
- 2009-05-07｜CFO｜margin：CFO解釋Q1為現金消耗季節性最高季，因付息與營運資金支出（原話："So Q1 is seasonally the highest quarter for our burn."）
- 2009-05-07｜CFO｜risk：CFO承認可轉債餘額構成重大財務overhang（原話："represents a significant financial overhang"）
- 2009-05-07｜CFO｜capital_allocation：管理層稱有多種重組或減少可轉債的選項，處理債務將以股東價值最大化為焦點，但不公開討論（原話："will be focused on maximizing shareholder value"）
- 2009-05-07｜CEO｜guidance：已重新提交SPA，若FDA同意，預計上半年啟動myelofibrosis樞紐性Phase III（原話："we remain in a position to start our pivotal Phase III"）
- 2009-05-07｜CEO｜guidance：預期歐洲註冊試驗將於一個月左右內開始，每項試驗約需六個月收案（原話："take about six months to enroll each of these studies"）
- 2009-05-07｜CEO｜guidance：仍預期於2010年底或2011年初完成試驗並申報NDA（原話："filing the NDA in late 2010 or early 2011"）
- 2009-05-07｜CEO｜product：INCB28050口服JAK抑制劑類風濕關節炎六個月Phase II，預期2010上半年出結果（原話："results of the trial in the first half of 2010"）
- 2009-05-07｜CEO｜product：INCB13739糖尿病試驗中期分析摘要獲ADA晚期海報接受，最終數據預計6月初（原話："we expect to have the final data in early June"）
- 2009-05-07｜CEO｜product：424於PV與ET的Phase II已完成收案，預計ASH發表，管理層稱安全性與療效結果令人鼓舞（原話："This study is fully enrolled"）
- 2009-05-07｜CEO｜product：外用424乾癬Phase IIb結果預計夏末（原話："we look forward to having results late this summer"）
- 2009-05-07｜CEO｜commitment：JAK腫瘤計畫意圖保留北美權利，但若條件有吸引力會考慮美國以外合作（原話："It remains our intent to keep North American rights"）
- 2009-05-07｜CEO｜commitment：JAK發炎計畫可做全球授權，或保留部分適應症／分享下游經濟利益（原話："we could do a broad global licensing deal"）
- 2009-05-07｜CEO｜commitment：CEO結語列出最高優先：開始MF註冊試驗，並以合作改善財務狀況（原話："improve our financial position by partnering"）
- 2009-05-07｜CEO｜commitment：被問若無法與FDA達成SPA是否仍進行，CEO稱想要SPA但不拘泥（原話："We very much like to have the SPA. We are not wedded to it."）
- 2009-05-07｜CEO｜capital_allocation：c-MET前臨床資產合作為相當高優先，但對改善資產負債表的幫助不如發炎或MPD交易（原話："it doesn't move the needle as a pre-clinical entity"）
- 2009-05-07｜CEO｜capital_allocation：sheddase需待與Herceptin合用於轉移性乳癌的試驗完成後才較易取得價值；IDO尚未嘗試合作（原話："we've not attempted to partner at this point in time"）
- 2009-05-07｜CMO｜competition：CMO說明外用乾癬藥療效門檻：維他命D/A類似物約20%達clear或almost clear，近期核准藥約23%（原話："you get responses in the 20% range"）
- 2009-05-07｜CEO｜competition：CEO稱其c-MET分子是c-MET抑制劑中最佳（原話："we think we have the best molecule of the c-MET inhibitors"）
- 2009-05-07｜CEO｜risk：CEO說明13739中期分析僅涵蓋約35%最終收案病人，提醒勿先下假設（原話："interim analysis was done on about 35% of the patients"）
- 2009-05-07｜CMO｜risk：CMO稱FDA對SPA並非全有全無，其樂觀認為可核准或小幅修改（原話："we're pretty optimistic that we either get approval"）
- 2009-05-07｜CEO｜customer：13739夥伴洽談：因最終數據只需再七週，決定等到6月初再重新接觸對象（原話："We started to wait until early June"）
- 2009-05-07｜CEO｜customer：CEO稱JAK發炎計畫興趣濃厚（原話："There is a lot of interest in that program."）

### 問答異常語氣（迴避／改口／保留）
- INCY_Q1_2009_Earnings_Call_20090507.md｜問：第二版SPA的試驗設計與原先構想相比變動多少？｜答法：拒絕說明設計，稱待FDA同意後再提供清楚描述，僅重申NDA時程
- INCY_Q1_2009_Earnings_Call_20090507.md｜問：是否嘗試以有利條件回購可轉債，若無原因為何？｜答法：未回答是否嘗試回購，僅稱不願透露策略細節、以股東價值最大化為準
- INCY_Q1_2009_Earnings_Call_20090507.md｜問：JAK按適應症拆分授權是否被合作方視為問題？｜答法：稱難以深入，僅表示分子不同已將問題降到最低，不再進一步評論

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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
