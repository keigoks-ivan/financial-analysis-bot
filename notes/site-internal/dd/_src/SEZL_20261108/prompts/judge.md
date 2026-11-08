你是 stock-analyst **v20 判斷 agent**，標的 SEZL（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SEZL","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenue_gaap","label":"Total revenue (GAAP)","value":149.7,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"市場彙整稿稱優於預期約 $14.6M（預期約 $135.1M；二手來源，未經 IR 稿驗證）"},{"id":"f_kpi1_gaap_operating_income","label":"GAAP operating income","value":55.0,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi2_net_income_gaap","label":"Net income (GAAP)","value":40.8,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi3_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未揭露 Non-GAAP 營業利益，以此代替）","value":58.0,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi4_free_cash_flow","label":"Free cash flow（僅上半年累計，無單季）","value":140.4,"period":"H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi5_stock_based_compensation","label":"Stock-based compensation（僅上半年累計）","value":3.4,"period":"H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi6_full_year_2026_guidance","label":"Full-year 2026 guidance（上調）","value":185.0,"period":"Q2 FY2026（公告於 2026-08-06）","unit":"USD million（Adjusted net income）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"Adjusted EPS 指引 $5.25 vs 站內共識 FY1 EPS $5.26（consensus_revision，口徑未必相同）"},{"id":"f_kpi7_active_subscribers","label":"Active subscribers","value":854000,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"人","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi8_gross_merchandise_volume","label":"Gross merchandise volume (GMV)","value":1.3,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_sezl_gross_margin_pct","label":"SEZL 毛利率","value":74.33,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SEZL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sezl_operating_margin_pct","label":"SEZL 營業利益率","value":39.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SEZL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sezl_fcf_margin_pct","label":"SEZL FCF 利潤率","value":65.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SEZL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_afrm_gross_margin_pct","label":"AFRM 毛利率","value":68.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_afrm_operating_margin_pct","label":"AFRM 營業利益率","value":20.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_afrm_fcf_margin_pct","label":"AFRM FCF 利潤率","value":23.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pypl_gross_margin_pct","label":"PYPL 毛利率","value":45.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pypl_operating_margin_pct","label":"PYPL 營業利益率","value":18.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pypl_fcf_margin_pct","label":"PYPL FCF 利潤率","value":18.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":149.43,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":55.11,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":63.18,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.26 → 5.26）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.65 → 6.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.95 → 7.95）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.26,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.65,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.95,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 5.26 → 5.26（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":28.79,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":8.68,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":8.74,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":28.41,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 5.26，分子＝快照價 149.43","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":32.62,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 102.76、現金 70.14（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":33.78,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":5080.87,"period":"2026-11-08","unit":"USD m","basis":"市值 5048.25 ＋ 淨負債 32.62","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":641.14,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（5 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":796.9,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（7 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.92,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 149.43 / W52 101.5 / W104 89.82 / W250 None / W250 13週斜率 None%"},{"id":"f_ma_w52","label":"52 週均線","value":101.5,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":89.82,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Sezzle CEO 稱 BNPL 份額主要來自區域銀行而非 BNPL 同業；Sezzle 短天期放款模型營業利益率 61%、ROE 91.9%，高於較長天期的 Affirm、Klarna（搜尋摘要轉述）","source":"24/7 Wall St.: Sezzle CEO Says BNPL Market Share Is Coming From Regional Banks, Not Rivals, as Stock Soars 150% YTD","url":"https://247wallst.com/investing/2026/06/26/sezzle-ceo-says-bnpl-market-share-is-coming-from-regional-banks-not-rivals-as-stock-soars-150-ytd/","excerpt":"Sezzle CEO Says BNPL Market Share Is Coming From Regional Banks, Not Rivals, as Stock Soars 150% YTD","as_of":"2026-06-26","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Fed 資料：2025 年美國六大 BNPL 業者發放信貸 $156.7B；Afterpay/Block $53.7B、Affirm $41.3B、PayPal $26.5B、Klarna $23.9B、Sezzle $3.9B（Sezzle 約 2.5%，為六家中規模最小之一；彙總站轉述，非 Fed 原頁）","source":"Chargeflow 彙整 Federal Reserve 2025 credit issuance 數據；Fed FEDS Note 2026-06-05","url":"https://www.federalreserve.gov/econres/notes/feds-notes/buy-now-pay-later-beyond-pay-in-4-a-comprehensive-product-overview-20260605.html","excerpt":"Sezzle reported 3.05 million active consumers and $3.94 billion in gross merchandise volume for 2025.","as_of":"2026-06-05","retrieved_at":"2026-10-05","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 Sezzle 營收 +29%、淨利 +42%；訂閱戶 +76.4%、交易筆數 +32%、季 GMV +38% YoY（搜尋摘要轉述）","source":"搜尋彙整（Yahoo Finance／StockStory 等）","url":"https://finance.yahoo.com/markets/stocks/articles/sezzle-shares-tumble-despite-strong-123845759.html","excerpt":"Sezzle Shares Tumble Despite Strong Quarter as Growth Outlook Disappoints","as_of":"2026-08-01","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"2026 Q2 財報優於預期但警告下半年營收成長放緩，盤前股價跌 23%（as_of 為約略月份，確切日期未讀到）","source":"Yahoo Finance: Sezzle Shares Tumble Despite Strong Quarter as Growth Outlook Disappoints","url":"https://finance.yahoo.com/markets/stocks/articles/sezzle-shares-tumble-despite-strong-123845759.html","excerpt":"Sezzle Shares Tumble Despite Strong Quarter as Growth Outlook Disappoints","as_of":"2026-08-01","retrieved_at":"2026-10-05","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"競爭威脅：搜尋摘要指 Chase、Citi 等銀行發展 BNPL 產品（信用卡額度轉分期、固定手續費），以及 Apple、PayPal 等大型科技整合先買後付；Affirm、Klarna、Afterpay 規模與零售整合較深（二手彙整，未見具名 2026 新進入者）","source":"搜尋彙整（businessmodelcanvastemplate 等）","url":"https://businessmodelcanvastemplate.com/blogs/competitors/sezzle-competitive-landscape","excerpt":"What is Competitive Landscape of Sezzle Company?","as_of":"2026-08-01","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Sezzle 8-K（2026-05）披露的融資concentration limit：單一商家（Target Corporation 除外）上限 15.0%，Target 上限 35.0%，顯示 Target 為最大商家集中點。","source":"Sezzle Inc. Form 8-K FY2026 (ex10.1, 2026-05-07)","url":"https://www.sec.gov/Archives/edgar/data/0001662991/000166299126000071/sezl-20260507ex1001.htm","excerpt":null,"as_of":"2026-05-07","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"搜尋未找到 Target 與 Sezzle 協議續約、導入第二 BNPL 供應商或 Target 自建 BNPL 的任何報導。","source":"WebSearch 結果（無相關條目）","url":null,"excerpt":null,"as_of":"2026-10-05","retrieved_at":"2026-10-05","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 披露：2025 與 2024 年度無任何外部單一對象占總營收達 10% 以上。","source":"Sezzle 10-K FY2025（經 StockTitan 摘要頁讀取）","url":"https://www.stocktitan.net/sec-filings/SEZL/10-k-sezzle-inc-files-annual-report-701e205530f4.html","excerpt":"For the years ended December 31, 2025 and 2024, no external party amounted to ten percent or more of our total revenue.","as_of":"2026-02-26","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"對照：FY2022 有單一商家約占總收入 14%；FY2021 無商家超過 10%。（歷史資料，非現況）","source":"Sezzle 10-K FY2022 / FY2023 S-1 披露（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000121390023022123/ea175545-s1_sezzleinc.htm","excerpt":null,"as_of":"2023-03-01","retrieved_at":"2026-10-05","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"美國 BNPL 市場預測 2026 年 $111.6B（+14.7%）、2027 年 $124.8B（+11.9%），成長率自 2025 年 20.4% 逐年放緩；來源敘述放緩反映市場成熟而非景氣疲弱。","source":"SaleHoo / eMarketer 彙整：US Buy Now, Pay Later Market Size (2023-2027)；BNPL growth is slowing as the industry matures","url":"https://www.salehoo.com/learn/us-bnpl-market-size","excerpt":"In 2026, the US BNPL market is projected at $111.6 billion (+14.7%), and $124.8 billion in 2027 (+11.9%).","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Sezzle 2026 Q1：活躍訂閱用戶 714,000（+48.4% YoY）、活躍消費者 3.1M（+13.6%）、交易筆數 9.9M（+35.8%）；季均購買頻率 7.1 次（去年同期 6.1）。","source":"Sezzle Reports First Quarter 2026 Results（Seeking Alpha PR／Nasdaq 彙整）","url":"https://seekingalpha.com/pr/20504067","excerpt":"In the first quarter of 2026, active subscribers rose 48.4% year over year to 714,000, while the combined total of monthly on-demand users and subscribers reached 887,000, up 34.8%.","as_of":"2026-05-01","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Sezzle 面臨企業級商家費率的顯著競爭壓力；2025-03 Klarna 取代 Affirm 成為 Walmart 獨家 BNPL 供應商，顯示供給端競爭仍在重分配。","source":"CSIMarket SEZL Competitors／Business Strategy Hub 彙整搜尋摘要","url":"https://csimarket.com/stocks/SEZL-Competitors","excerpt":"Sezzle faces significant competitive pressure on merchant fees, particularly from enterprise merchants","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"Sezzle 是原告：其對 Shopify 的反壟斷訴訟（明尼蘇達聯邦地方法院）2026-05 裁定部分駁回 Shopify 的駁回動議，Sherman Act 核心主張續行，不當搭售（tying）主張被無偏見駁回。","source":"GlobeNewswire: Sezzle Provides Update on Antitrust Case Against Shopify","url":"https://www.globenewswire.com/news-release/2026/05/12/3293417/0/en/sezzle-provides-update-on-antitrust-case-against-shopify.html","excerpt":"Sezzle's core antitrust claims against Shopify under the Sherman Act will proceed, while an unlawful tying claim was dismissed without prejudice.","as_of":"2026-05-12","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"CFPB 利用監理與資料蒐集權限，向包含 Sezzle 在內的六家 BNPL 業者取得 pay-in-four 貸款資料；另有說法稱 CFPB 已撤回先前對 BNPL 的限制性規則，監管壓力暫時緩和。","source":"Richmond Fed Economic Brief: Buy Now, Pay Later: Recent Developments and Implications（搜尋摘要）","url":"https://www.richmondfed.org/publications/research/economic_brief/2026/eb_26-05","excerpt":"The CFPB used its supervisory and data-collection authority to obtain detailed pay-in-four loan data from six leading BNPL providers: Affirm, Afterpay, Klarna, PayPal, Sezzle and Zip.","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"有律所公告調查 Sezzle 等 BNPL 業者是否就逾期費、付款時點、透支風險或分期真實成本誤導消費者（非政府機關調查）。","source":"Migliaccio & Rathod LLP: Sezzle Buy Now Pay Later Investigation","url":"https://classlawdc.com/2026/07/07/sezzle-buy-now-pay-later-investigation/","excerpt":"A law firm is investigating whether Sezzle and similar Buy Now, Pay Later companies mislead consumers about late fees, payment timing, overdraft risks, or the true cost of installment purchases.","as_of":"2026-07-07","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"多家律所2026-05公告調查 Sezzle 及部分高管／董事是否涉證券詐欺或其他不當行為（證券訴訟調查，非反壟斷）。","source":"Pomerantz Law Firm via Morningstar/PR Newswire","url":"https://www.morningstar.com/news/pr-newswire/20260514dc60536/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-sezzle-inc-sezl","excerpt":null,"as_of":"2026-05-14","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素把關稅與國際貿易規範列為影響消費者支出與信貸可得性的總經因子之一（間接暴露，非供應鏈直接暴露）","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":"consumer spending and consumer credit are affected by economic conditions such as unemployment, consumer confidence, actual or anticipated economic recessions, consumer debt, inflation and deflation, currency exchange rates, tariffs and international trade regulations, taxation, fuel and energy prices and interest rates","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 只提及適用 OFAC 與加拿大制裁計畫，未見出口管制或實體清單相關揭露","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":"We are also subject to certain economic and trade sanctions programs including Canadian sanctions laws and the sanctions programs administered by the U.S. Department of the Treasury’s Office of Foreign Assets Control (“OFAC”), which prohibit or restrict transactions or dealings with specified countries, individuals, and entities.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"SEZL 10-K 風險因子：與發卡銀行夥伴的協議為非獨家，且在特定事件發生時發卡夥伴可終止（融資/發卡環節的單點依賴）。","source":"Sezzle Inc. Form 10-K FY2025（SEC EDGAR）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"SEZL 10-K 風險因子：重要供應商含雲端資料儲存、IT 方案與支付處理；服務中斷或供應商錯誤可能使其無法處理交易或入帳。","source":"Sezzle Inc. Form 10-K FY2025（SEC EDGAR）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"SEZL 10-K 風險因子：相當比重的業務與交易量集中在少數大型電商平台，任一平台不再合作或轉投競爭者會不成比例地衝擊公司。","source":"Sezzle Inc. Form 10-K FY2025（SEC EDGAR）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Sezzle CEO 稱 BNPL 市佔主要來自區域銀行與信用合作社，而非其他 BNPL 業者","source":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/06/26/sezzle-ceo-says-bnpl-market-share-is-coming-from-regional-banks-not-rivals-as-stock-soars-150-ytd/","excerpt":"Sezzle CEO Says BNPL Market Share Is Coming From Regional Banks, Not Rivals, as Stock Soars 150% YTD","as_of":"2026-06-26","retrieved_at":"2026-10-05","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Sezzle 風險揭露稱 BNPL 與其他替代支付產品的採用增加，可能吸引大型金融機構、卡網與科技公司進入，對方規模與品牌較強，可能迫使 Sezzle 降低商家費率或加碼誘因。","source":"gloom.sh Sezzle 2026 risk factors（搜尋摘要，轉述 Sezzle 風險因子）","url":"https://gloom.sh/stocks/sezl/risk-factors/2026","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Sezzle 以產品擴張回應：6 月推出 SezzleCash、8 月推出 Sezzle Send，並於 2026 推出內嵌 AT&T 網路的 Sezzle Mobile 手機方案。","source":"Sezzle Inc. Form 8-K Ex.99.1（2026 Q2 業績新聞稿）","url":"https://www.sec.gov/Archives/edgar/data/0001662991/000166299126000124/sezl-20260806ex9901.htm","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q1 2026 活躍訂閱用戶 714,000，年增 48.4%；訂閱＋隨選月付用戶合計 887,000，年增 34.8%；季均購買頻率 7.1 次（前年 6.1 次）。搜尋摘要稱此為由單次 BNPL 交易轉向訂閱式經常性收費關係，並以 Sezzle Anywhere 虛擬卡擴大可用商家範圍。","source":"Yahoo Finance / Zacks 摘要：Sezzle Recasts BNPL Model With Subscriptions Sezzle Anywhere And Eased Rules","url":"https://finance.yahoo.com/news/sezzle-recasts-bnpl-model-subscriptions-132212461.html","excerpt":null,"as_of":"2026-05-01","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"搜尋摘要稱 Sezzle 商家開發由量取向轉為優先大型企業商家；Q2 2026 新增企業商家含 Poshmark、Gymshark、Debenhams、Brookshire's、RockAuto。","source":"TradingView/Zacks：SEZL's Merchant Acquisition Strategy Vital for Its Growth Trajectory；Investing.com：Sezzle Q2 2026 slides","url":"https://www.tradingview.com/news/zacks:523b0aa6b094b:0-sezl-s-merchant-acquisition-strategy-vital-for-its-growth-trajectory/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FY2025 Q4 財報（發布日 2026-02-25）：新增 134,000 名隨選月付與訂閱用戶，總數 918,000；2026 計畫包含更高信用額度的長期借貸與更廣商家接受度。","source":"PYMNTS：Sezzle GMV Surges as Super App Plans Advance","url":"https://www.pymnts.com/earnings/2026/sezzle-gmv-surges-as-super-app-plans-advance/","excerpt":"Sezzle also added 134,000 new Monthly On-Demand and Subscribers during the quarter, bringing the total to 918,000.","as_of":"2026-02-25","retrieved_at":"2026-10-05","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-11-04 Q3 業績公布，公司把 FY2026 營收成長指引上調至約 42.5%（8 月為 35%），調整後稀釋 EPS 指引 $5.45–$5.50（8 月 $5.25）；全年指引自 2 月 25–30% 起連續四次上調","source":"Sezzle Reports Third Quarter 2026 Results (GlobeNewswire via mfn.se)","url":"https://mfn.se/all/a/sezzle/sezzle-reports-third-quarter-2026-results-421784fd","excerpt":"Raised FY2026 guidance to approximately 42.5% Total Revenue growth.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"賣方目標價共識依來源 $137–$168 不等（MarketBeat $151.33 Moderate Buy、Benzinga $152.88/8 位、Tickflow $137.33、Investing.com $168 區間 $150–$196），資料多停在 2026-07/08，早於 Q3 公布，未見 Q3 後更新；8 月 KBW 目標價由 $190 降至 $155 並降評為 Market Perform，Needham 由 $166 升至 $172 Buy","source":"MarketBeat / Tickflow / Investing.com / Benzinga（搜尋摘要）","url":"https://www.marketbeat.com/instant-alerts/sezzle-nasdaqsezl-shares-gap-down-on-analyst-downgrade-2026-08-07/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-02-25 8-K Item 4.02：公司認定 2024 年現金流量表中票據應收款的購入／還款分類錯誤（應歸投資活動），2024 全年及 2024/2025 各季現金流量表不應再依賴；資產負債表、損益表無影響。","source":"SEC EDGAR 8-K Item 4.02","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000014/sezl-20260219.htm","excerpt":"the Company concluded that it had not appropriately classified purchases and originations of notes receivable, and proceeds from repayments thereof, as “investing activities” within its Consolidated Statements of Cash Flows for the year ended December 31, 2024.","as_of":"2026-02-25","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2025-06-09 Sezzle 在明尼蘇達聯邦地院對 Shopify 提起反壟斷訴訟（公司為原告）；Shopify 聲請駁回，2025-12-08 聽證，截至 10-K 申報日法院尚未裁決。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":"On June 9, 2025, we filed a lawsuit against Shopify, Inc., in the U.S. District Court for the District of Minnesota asserting federal and state antitrust violations.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"2026-08-12 與 WebBank 簽第二次修訂銀行計畫協議，擴及 SezzleCash（預借現金）與 Sezzle Send 兩項新產品。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000144/sezl-20260812.htm","excerpt":"The Second Amended Bank Program Agreements expand the Program to support two additional Company products: SezzleCash, a cash advance product, and Sezzle Send, a payments product","as_of":"2026-08-18","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"10-K 法律程序章節除 Shopify 訴訟外，無其他重大法律程序；經查近 12 個月 8-K 清單未見併購（2.01）項目。","source":"SEC EDGAR 10-K Item 3；8-K 清單","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":"Except as set forth below, we are not currently involved in any material legal proceedings, other than ordinary routine litigation incidental to the business","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"-","claim":"2026-04-09 董事 Karen Webster 請辭並以信函指與管理層方向／治理分歧；之後多家原告律所（Pomerantz、Lowey Dannenberg、Glancy 等）宣布調查，皆為律所新聞稿，未見已提起之集體訴訟。","source":"Pomerantz 新聞稿／搜尋摘要彙整","url":"https://www.placera.se/pressmeddelanden/sezzle-investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-sezzle-inc-sezl-20260521","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"公司為原告對 Shopify 提反壟斷訴訟，聽證 2025-12-08，尚無裁決；公司稱無重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":"Shopify has denied the allegations and filed a motion to dismiss the complaint. A hearing on such motion was held on December 8, 2025.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","triggers"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-05 起多家原告律所公告調查 Sezzle 是否違反證券法，為徵求投資人公告，未見已提起之集體訴訟。","source":"Pomerantz 新聞稿","url":"https://www.placera.se/pressmeddelanden/sezzle-investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-sezzle-inc-sezl-20260521","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"2026-02-25 8-K Item 4.02 非依賴通知：2024 年現金流量表重編（票據應收款改列投資活動），不影響資產負債表與損益表。","source":"SEC EDGAR 8-K Item 4.02","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000014/sezl-20260219.htm","excerpt":"had no impact on the Consolidated Balance Sheets, Consolidated Statements of Operations and Comprehensive Income, Consolidated Statements of Stockholders’ Equity, or the Notes to the Consolidated Financial Statements.","as_of":"2026-02-25","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SEZL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.33,"operating_margin_pct":39.68,"fcf_margin_pct":65.06,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SEZL","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AFRM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.07,"operating_margin_pct":20.44,"fcf_margin_pct":23.3,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PYPL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.76,"operating_margin_pct":18.52,"fcf_margin_pct":18.37,"rd_intensity_pct":9.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"SEZL"},"financial_history":{"ticker":"SEZL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":125570441.0,"revenue_yoy_pct":null,"gross_margin_pct":19.89,"operating_margin_pct":-38.25,"net_income":-38093756.0,"diluted_eps":-1.14,"free_cash_flow":7503771.0,"fcf_margin_pct":5.98,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":159356772.0,"revenue_yoy_pct":26.91,"gross_margin_pct":46.3,"operating_margin_pct":13.93,"net_income":7098022.0,"diluted_eps":0.208333,"free_cash_flow":-27056025.0,"fcf_margin_pct":-16.98,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":271128000.0,"revenue_yoy_pct":70.14,"gross_margin_pct":56.89,"operating_margin_pct":25.26,"net_income":78522000.0,"diluted_eps":2.188333,"free_cash_flow":129184000.0,"fcf_margin_pct":47.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":450279000.0,"revenue_yoy_pct":66.08,"gross_margin_pct":70.06,"operating_margin_pct":36.15,"net_income":133130000.0,"diluted_eps":3.72,"free_cash_flow":207212000.0,"fcf_margin_pct":46.02,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SEZL/SEZL_Q3_2026_Earnings_Call_20261104.md）

# Q3 2026 Earnings Call
**Sezzle Inc.** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Good day, and welcome to the Sezzle Inc. Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please note that today's event is being recorded.
I would now like to turn the conference over to Charlie Youakim, Executive Chairman and CEO. Please go ahead, sir.

**Charles Youakim** (Executives):
Thank you, and good afternoon, everyone, and welcome to Sezzle's third quarter 2026 earnings call. I'm Charlie Youakim, CEO and Executive Chairman of Sezzle. I'm joined today by our CFO, Lee Brading, my Co-Founder and Company President, Paul Paradis; and Head of IR and Corp Dev, Jack Fagan.
In conjunction with this conference call, we filed our earnings announcement with the SEC and posted it along with our earnings presentation on our investor website at sezzle.com. To retrieve the documents, please go to the Investor Relations section of the website. Please be advised of the cautionary note on forward-looking statements and the reconciliation of GAAP to non-GAAP measures included in the presentation, which also covers our statements on today's call.
Before getting into the results, I want to talk about how I'm looking at the third quarter. We spent a good part of this year building and launching new products. I'm incredibly proud of what our teams have accomplished this year. We spent a good deal of time researching which products made sense with strategy sessions and customer surveys and panels, but the real test is whether consumers actually use the product after we launch it and whether it adds value to their relationship with Sezzle and ultimately, whether it helps us build a better business.
We saw one of our early product launches this year do just that. Pay-in-5 was a home run product launch for us. The results match the research. It's become a much-used and much-loved variant of our core BNPL product. And this quarter, we're starting to get some more answers. SezzleCash looks like it's going to be another great product for us, but it's still not putting up significant numbers just because it's starting from scratch. And Sezzle Send, our P2P product, that one looks like it still needs some fine-tuning to make a significant impact in future years. But again, really small volumes, but we just wanted to give you the early reads. All of this activity is helping though. It adds up.
We're seeing purchase frequency continue to increase, and we're seeing stronger monetization as consumers engage more deeply with the platform. We're still in the learning and improvement phase with some of these offerings like Send and Cash, and their volumes are so small relative to our base product that it will take many months for them to catch up and have truly measurable numbers relative to the existing products.
But what is encouraging is that we're beginning to see the different pieces of our strategy work together. And we're doing that while maintaining the financial discipline that's been so important to our success. We continue to keep our OpEx growth in check while we grow the team and launch new offerings for our consumers. That's how I want to frame today's results. It's not just about how much we've built, it's about what those investments are starting to deliver.
With that, let's turn to Slide 3. Total transaction volume, which expands our traditional GMV measure to include SezzleCash and Sezzle Send, grew 34.9% year-over-year, while total revenue increased 42.6%. We generated $47.8 million of net income and $70.2 million of adjusted EBITDA. And total revenue less transaction-related costs came in at 64.7% of revenue, near the upper end of the range we've consistently targeted.
Those are strong results, but I think the more important story is what's happening with our consumers. We ended the quarter with 955,000 active subscribers, up 68.1% year-over-year, putting us within reach of 1 million subscribers.
And average quarterly transaction frequency reached 7.8x compared to 6.5x a year ago. Importantly, that now includes not only purchases but also SezzleCash advances and Sezzle Send payments. That's an important distinction because we're giving consumers more reasons to use Sezzle beyond shopping. And to me, that's exactly what we've been working toward.
Given the strength of the business, we're also raising our full year outlook. We now expect revenue growth of approximately 42.5%, adjusted net income of $190 million and adjusted net income per diluted share of $5.45 to $5.50. We've also introduced a preliminary adjusted net income per diluted share outlook of $7.20 for 2027. Lee will walk through the financial details and outlook later in the call.
But before we get there, I want to spend some time talking about what's driving these results and why we believe the consumer relationship continues to strengthen. Let's start with subscriptions.
On Slide 4, you can see the continued progress we're making with subscriptions. We added another 101,000 net new subscribers in the third quarter, following the record 140,000 we added in Q2. That brings us to 955,000 active subscribers, and it puts us within reach of 1 million.
One thing I want to call out is our marketing spend because we spent quite a bit of time talking about it last quarter. In Q2, we deliberately pushed spending higher to see how far we could go while staying within our 6-month marketing payback threshold. We also said at the time that it was a test, not necessarily a new run rate.
In the third quarter, we brought marketing spend down to $15.9 million from $19.4 million, while continuing to grow our subscriber base. Our philosophy hasn't changed. If we find opportunities to acquire high-value consumers at attractive returns, we're going to pursue them. But we're not interested in growing subscribers just for the sake of growing subscribers. Based on this test, we like the lower marketing run rate spend level. We think it gives us a nice margin of safety while still delivering long-term results.
And I think that's where the engagement metrics on this slide become particularly important. On average, our subscribers are making 9 more transactions per quarter than nonsubscribers. And importantly, that now includes not just traditional purchases, but also SezzleCash advances and Sezzle Send payments. So we're getting a more complete picture of how consumers are engaging with Sezzle across different financial needs, not just when they're shopping.
To me, that's really what we're trying to accomplish. We want to keep giving consumers reasons to come back and use Sezzle more often. And we're continuing to add to that value proposition. More recently, we introduced Subscription Saver, which helps anywhere subscribers identify, manage and cancel recurring subscriptions they no longer need. It's one more practical way we can deliver value to our consumers.
And that same thinking is driving our broader product strategy. Whether consumers are shopping, converting a short-term cash need or sending money to someone else, we're finding new ways to make Sezzle more useful in their everyday lives. We've made a lot of progress on that front this year. Part of what gives me confidence in the direction is the pace at which our teams have continued to deliver new products. And when you look at what we've accomplished throughout 2026 on Slide 5, it's not just one big product launch. It's a series of additions that we are making to make Sezzle more useful for our consumers.
We started the year with Pay-in-5, added the virtual card offering in Canada, expanded our long-term lending capabilities and introduced Sezzle Mobile. Then we launched SezzleCash, giving eligible anywhere consumers access to funds for short-term cash needs without having to make a purchase. And we also introduced Sezzle Send, which remained in beta throughout the third quarter before we opened it up more broadly to Sezzle users at the beginning of October.
This brings the flexibility of installment payments to everyday money transfers. Now each of these products serves a different purpose, but the strategy behind them is the same. We're giving consumers more reasons to choose Sezzle and more reasons to keep coming back.
We also did an updated study earlier this year on Sezzle Up, our pro bono credit builder. It turns out that for our on-time subprime customers, they are lifting their credit score an average of 17 points in 4 months. That's an amazing result for a group of consumers that can benefit greatly from a credit score lift like that. And it's there in the product set and has been there for years.
Importantly, not every new product needs to be a significant stand-alone revenue driver. Look at Sezzle Up. It's free for our consumers to join. Some products are designed to attract new consumers, others to improve engagement and retention and others, like Up, to do the right thing for our consumers. In the end, what matters is the value they all create in the overall platform.
Looking ahead, we've also soft launched Sezzle Anywhere in Canada at the start of the fourth quarter. This brings our subscription model and open-loop virtual card capabilities to the Canadian customer, allowing them to use Sezzle wherever Visa is accepted in Canada. But launching new products is really only the first step. The more important question is what consumers actually do with them once they're available.
And with SezzleCash, we're starting to see some encouraging results that I think are worth spending a little more time on. We rolled out SezzleCash in June. So the third quarter was our first full quarter of seeing how consumers use the product, and the early results are encouraging. As a reminder, SezzleCash allows eligible anywhere subscribers to access funds for short-term cash needs without having to make a purchase. So whether it's paying a bill, covering an unexpected expense or something that simply doesn't accept a card, we're giving consumers another way to manage their everyday finances.
One of the clearest signals we're seeing is how consumers are getting started. In the third quarter, more than 15% of eligible new Anywhere subscribers made their very first transaction with SezzleCash. That's a meaningful number. We're seeing consumers sign up for Sezzle Anywhere, a product that has historically been centered around shopping and their first transaction isn't the purchase. It's a cash advance.
That suggests SezzleCash may be attracting consumers who wouldn't have necessarily considered an anywhere subscription for BNPL alone, and that potentially opens up an entirely new avenue for subscriber acquisition. But there's another part of the story. More than 60% of new Anywhere subscribers who started with SezzleCash also went on to make a BNPL purchase. And when we look at all SezzleCash users during the third quarter, more than 90% also use Sezzle for BNPL purchases.
We're also seeing repeat engagement with the product itself with more than 60% of SezzleCash users taking multiple advances during the quarter. Now we're still early, and we're continuing to be thoughtful about how we grow and manage the product, but the opportunity is becoming clearer. SezzleCash may be bringing consumers into our subscription offering who wouldn't have used us or reached us otherwise. And we're seeing many of those consumers go on to use our traditional BNPL products.
With Sezzle Send, we're exploring another avenue for reaching consumers, but this time through something entirely different, sending money to another person. Sezzle Send is a different kind of product for us. It was in beta throughout the third quarter, and we opened it up more broadly to Sezzle users at the beginning of October. So we're still at an early stage of understanding how consumers will use it, and we're still actively working on tweaking the offering to make it a hit.
The concept displayed on Slide 7 is straightforward. You can send money to someone using their phone number, either paying in full or splitting the payment into 5 installments. And regardless of how the sender chooses to pay, the recipient receives the full amount upfront. Where this becomes a new avenue for Sezzle is in how it can introduce people to the platform. When one of our consumers sends money to somebody who doesn't use Sezzle, that recipient has a reason to sign up and experience our product for the first time. Instead of coming to us through a merchant or an advertisement, they're being introduced through someone they know.
So we're creating a potential acquisition channel that's built directly into how consumers use the product. But to be clear, this is a new behavior for consumers within the Sezzle app. Spending money is different from shopping and for someone receiving their first transfer, there's an onboarding experience involved. So broader adoption may take some time.
SezzleCash addresses a more immediate financial need for eligible Anywhere subscribers. Sezzle Send involves getting consumers comfortable using Sezzle in a new way, including people who may never have interacted with our platform before. We like the potential here, but we're going to be thoughtful about building it out and learning from how consumers actually use it.
And while we're exploring new offerings like Sezzle Send, we're also continuing to invest in the products we've already built. Slide 8 is a good example. We originally launched Sezzle Up back in 2021, becoming the first BNPL platform in North America to give consumers the option to report their short-term installment payments to the credit bureaus.
More recently, we've focused on making that experience easier and more accessible. We've expanded eligibility, simplified enrollment and refreshed the design. We're also working on adding features like in-app credit scores, credit monitoring and alerts. And we're already seeing some encouraging results from those changes. Following our September enhancements, enrollment conversion increased 18% and average weekly enrollments nearly doubled.
So this isn't about introducing something new. It's about continuing to improve a product we've had for years and making it more useful for more consumers.
And beyond helping consumers build their credit, we've also been investing in financial education and finding better ways to learn directly from our users as seen on Slide 9. Money IQ is one part of that effort. Through the program, more than 338,000 consumers have completed over 2 million financial education modules, representing more than 68,000 hours of learning. And in our March survey, 91% of respondents said Money IQ was helpful in making financial decisions. But we're also learning from our consumers.
Our Gen Z Advisory Council gives younger consumers a direct way to tell us what they like, what they change and what they'd like to see next. And we're putting that feedback to work across products like Sezzle Send, Sezzle Up and our rewards offerings. It's a 2-way relationship. We're helping consumers become more informed about their finances while they're helping us build better products.
And as we continue to improve these products, AI is playing an increasingly important role in how quickly and efficiently we can deliver. AI continues to be a major focus across Sezzle, and Slide 10 shows some meaningful progress since our last update. We've talked before about embedding AI throughout our organization. What I want to highlight this quarter is the impact we're seeing from those efforts.
On the consumer side, 40% of support contacts now end with our AI agent without requiring any human involvement. And we're seeing strong consumer satisfaction from those interactions as well. Based on our post-contact surveys, AI interactions are 1.4x as likely to receive a top satisfaction score compared to human handled tickets.
Internally, we're seeing similar progress. More than 90% of our engineering merges in the third quarter involved AI, and we're seeing a 43% year-over-year increase in code changes merged per engineer. We're also getting more efficient in how we use these tools with AI costs per unit of work declining 27% sequentially.
These are the great results we're looking for, more consumer support handled without human intervention, greater output from our engineering teams and improving cost efficiency. It's one thing to adopt AI across an organization. It's another to see that adoption translate into measurable improvement in how the business operates.
And while a lot of this work happens behind the scenes, the ultimate measure of our progress is how consumers are engaging with Sezzle. The metrics on Slide 11 give you a good picture of how this is all coming together.
First, we're continuing to see strong engagement in our core shopping business. Average quarterly frequency reached 7.8x, up from 6.5x a year ago. That now includes BNPL purchases along with SezzleCash and Sezzle Send payments, giving us a broader view of how consumers are using the platform. Across the platform, total transactions increased 30.1% year-over-year to 12.4 million. Repeat usage also remained strong at 97.4% of total transactions, up 80 basis points year-over-year. But the number I'd like to leave you with is average quarterly revenue per monetized user, which increased 28.1% year-over-year to $41.
We spent a lot of time today talking about our investments in subscriptions, new products and the consumer experience. These are the measures that help us evaluate whether those investments are paying off. Consumers are shopping with us more frequently. They're engaging with a broader range of subtle products, and we're generating more revenue per monetized user. There's still plenty of work ahead of us, but we're encouraged by the progress we're making and confident in the direction of the business.
With that, I'll turn it over to Lee to walk through the financial results in more detail.

**Lee Brading** (Executives):
Thanks, Charlie. I'll start on Slide 12. Total revenue increased 42.6% year-over-year to $166.5 million. Net income rose 79.3% to $47.8 million and adjusted net income grew 89.9% to $47.7 million.
As you can see, it was a solid quarter of growth coupled with margin expansion, driven by margin improvements, profit grew roughly twice as fast as revenue as we more than doubled the threshold for the Rule of 40.
Total revenue less transaction-related costs rose 10.5 points to 64.7% of total revenue at the top of our 55% to 65% target range. Non-transaction-related operating expenses were 27.8% of revenue, up 0.7 points year-over-year, but down 1.2 points from Q2.
On Slide 13, you'll notice a change in how we measure volume. Starting this quarter, total transaction volume, or TTV, is our primary measure of overall volume. Our products now go beyond the checkout. So TTV includes volume from SezzleCash and Sezzle Send, which GMV did not capture. We recast prior periods to the TTV definition, so every comparison on these slides is apples-to-apples. Q3 TTV grew 34.9% year-over-year to a new company high of $1.4 billion, an 11.6% sequential increase.
Growth was driven by our Sezzle Anywhere and Sezzle Premium subscribers plus the launch of SezzleCash in June. Total revenue grew faster than volume at 42.6%. Revenue as a percentage of TTV was 11.9%, up 60 basis points year-over-year and flat with Q2. As a reminder of seasonality, revenue yield is usually highest in Q1 and lowest in Q4. So we expect it to step down in the fourth quarter.
Turning to the unit economics on Slide 14 through 16. As a reminder, transaction-related cost is a non-GAAP measure that combines transaction expense, provision for credit losses and net interest expense. Revenue less transaction-related costs is what we also refer to as net transaction margin.
On Slide 14, transaction-related costs for Q3 were $58.8 million or 4.2% of TTV, down from 5.2% a year ago. As a percentage of revenue, they fell more than 10 points to 35.3%.
Slide 15 breaks out the 3 main components of transaction-related costs, transaction expense, provision for credit losses and net interest expense. Most of the decrease in transaction expense as a percentage of TTV is attributed to us signing an exclusive arrangement with Visa for our U.S. credit products. During the quarter, we recognized a $3.7 million benefit from the arrangement. Excluding this benefit, transaction expense would have been about 1.6% of TTV, still an improvement on the 1.7% we've run for the past several quarters.
The provision for credit losses was 2.7% of TTV, down from 3.1% a year ago. The step-up from Q2 is the normal seasonal pattern from Q1 as the low point because of tax refunds and the provision climbing through the year from there. Year-to-date, the provision is about 2.2% of TTV. With the move to TTV, we're updating full year guidance to approximately 2.5% of TTV from 2.5% to 3% of GMV, which still allows for the usual seasonal rise in Q4.
Net interest expense fell 29% year-over-year to $2.8 million or 0.2% of TTV. That reflects the new $300 million credit facility we entered into in May at a lower rate, plus SezzleCash and Sezzle Send now being handled through our loan facility with WebBank.
That brings us to Slide 16. Net transaction margin was $107.7 million, up 70% year-over-year and 64.7% of total revenue. Even without the payment network benefit, we would have been around 62.5%, comfortably in the upper half of our 55% to 65% target range.
Our focus on costs extends to non-transaction-related operating expenses on Slide 17. These costs were $46.2 million or 27.8% of revenue, down from 29% in Q2. Marketing came in at $15.9 million, down from $19.4 million in Q2 and consistent with what we talked about in Q2. As Charlie noted earlier, Q2 was a deliberate test of higher spend, not a new run rate.
Marketing is still up 81% year-over-year, and we'll keep putting dollars to work wherever the math supports a payback of less than 6 months. The investments we made in Q2 are already showing up with active subscribers reaching 955,000.
We're also gaining operating leverage in other areas. Personnel expense grew 17% against revenue growth of 43%, helped by the AI productivity gains Charlie described. Third-party technology and data grew faster as we scaled cloud infrastructure for higher volume and 3 new products.
Corporate strategic project costs were $2.4 million this quarter for 2 projects. First, our antitrust case remains in discovery, which we expect to continue through 2027. Second, we submitted our application for a national bank charter in October. Both are long-term investments in Sezzle, and we add these costs back in our adjusted figures.
On Slide 18, net income was $47.8 million, a 28.7% margin. That's up 79% year-over-year, even though our effective tax rate rose 22.1% from 15.7% a year ago. Adjusted EBITDA was $70.2 million, up 77% year-over-year with a 42.1% margin.
We continue to keep our adjustments to a minimum. Adjusted net income was $47.7 million. The relatively minor difference with GAAP net income is attributed to the difference of discrete tax benefit offset against the after-tax add-back of corporate strategic project costs. You can also see our seasonality here. Q1 and Q4 are typically our strongest quarters for bottom line performance.
Slide 19 shows we remain well capitalized with plenty of liquidity and low leverage. At quarter end, we had about $239 million in liquidity, made up of $70.1 million of unrestricted cash and $169.3 million of availability in our $300 million line of credit. We had $104 million drawn on the line, down from $118 million a year ago, even as notes receivable grew 72% to $315.9 million. Total debt is about 0.4x trailing 12-month adjusted EBITDA and 0.4x equity.
The business continues to fund itself. Year-to-date, cash from operations was $227.9 million, up 64%. Stockholders' equity grew 79% year-over-year to $277.7 million. Year-to-date, we have also returned capital as we have repurchased $28 million of stock under our $100 million program this year, which brings me to Slide 20.
We first guided to $4.35 of adjusted EPS for 2026 a year ago, and this is our fourth raise since. We now expect total revenue growth of approximately 42.5% for 2026, up from 35%. We're also raising adjusted net income guidance to $190 million from $185 million and adjusted net income per diluted share to $5.45 to $5.50, up from $5.25.
We are also introducing preliminary 2027 guidance for adjusted net income per diluted share of $7.20. That's a growth rate of 31% to 32% over our updated 2026 range. Our outlook includes a measured view of our newest products. SezzleCash is off to a strong start, and Sezzle Send just rolled out more broadly in October. As with any new lending product, we're managing both carefully on risk and marketing, and we'll update you as they mature.
With that, I'll turn the call over to the operator for Q&A.

**Operator** (Operator):
[Operator Instructions] And today's first question comes from Mike Grondahl with Northland.

**Mike Grondahl** (Analysts):
A nice quarter. Charlie, you guys are clearly product innovation and kind of riding a new product wave here, Pay-in-5, SezzleCash, Sezzle Send. Can you talk about what inning you think we're in, in some of these newer products? And any other to call out other than those 3?

**Charles Youakim** (Executives):
Well, good question, and thanks, Mike. Pay-in-5 is pretty much rolled out at this point. So I think that's a ball game for Pay-in-5 in terms of rolling out within our business. But our view on Pay-in-5 is maybe it's not ball game in terms of acquiring consumers and retaining consumers. That's all point is we saw such good feedback from consumers using our product that they love it so much that our view is that it incrementally helps us win consumers and keep consumers from competition.
SezzleCash and Sezzle Send, super early. I mean they're just getting started. So I think that's probably the layout. We're excited about all of them. But really Pay-in-5 has just been -- I mean, it rolled out earlier this year. So it's had a lot of time to make hay for us. And so that is the winner of the 3 right now.

**Mike Grondahl** (Analysts):
Got it. And maybe just 2 more questions. One quick on Pay-in-5. What percent of the business, and I think it's a big number, has transitioned to Pay-in-5? And then secondly, could you just cover again how SezzleCash and how Sezzle Send you think that's going to help with customer acquisition kind of bringing in new customers?

**Charles Youakim** (Executives):
Yes. I'll pass off the first part to Lee because he might have more detail on that. But on SezzleCash, Sezzle Send, actually even Pay-in-5, they all help us acquire new customers because they're basically differentiated offerings from, I think, some of the competitive base that our consumers may be compare us against. So we have differentiated or totally different products from some of our competitors that allow us to acquire new consumers.
I would say Sezzle Send has launched the entire -- I would say the majority of the design was around helping us acquire new consumers because the thesis is that consumers will send other money to their friends and family, contact, et cetera. And if you're already a Sezzle user, it's likely that you -- in your nexus, you have other potential Sezzle users just because people tend to hang out with people like them. There's a little bit of that. So our view is that, that would be a user-generated acquisition channel. And we still believe it is. But they're all helping us acquire users. I don't know, Lee, anything to add on the first part of the question?

**Lee Brading** (Executives):
Yes, on the percent of Pay-in-5. Yes, if you look at our kind of core BNPL product, yes, it's about -- it's the majority, and I think we've alluded to it before around 70%. And like Charlie said, yes, it's past the ninth inning, I guess.

**Mike Grondahl** (Analysts):
Got it. Yes, I mean that turned out to be pretty popular.

**Operator** (Operator):
And the next question is from Ross Cole with Needham & Company.

**Ross Cole** (Analysts):
Congratulations on the great quarter. My first question here is for FY '27, the $7.20 guide, can you provide any color into what's driving this? And then also, is this including an impact from SezzleCash and Send? Or would you consider like that growth to be upside here?

**Charles Youakim** (Executives):
Lee, do you want to take that one?

**Lee Brading** (Executives):
Yes, I can pop in here. I guess what I'll give you just a little more on the history of how we've given guidance. We did similarly in Q3 last year. We gave that $4.35 EPS for 2026. And it's inclusive of what we have opened like, what we've already launched in terms of products. So -- but we don't give much more than that at this point in time. As we come out in Q4, we'll break out more in terms of revenue and margin expectations. But at this point, it's just more of an EPS estimate for you guys.

**Ross Cole** (Analysts):
Great. And then I was wondering as well, it's great to see the subscribers approaching 1 million. Can you maybe talk a bit about how chartering conversions from on-demand are trending?

**Charles Youakim** (Executives):
Well, on-demand has been shrinking as a percentage of our business, mainly because we realized -- we talked about this earlier in the year as we started to transition more to subscribers as the focus. When we first launched on-demand, we had the theory in our mind, and we've been wrong before. The theory was that we were basically building like a bridge like almost like -- I know it's not free, but it's like a freemium bridge into our subscription product where it's like try before you buy, before you commit. And what we realized is a lot of those customers, they just like gating us like just dabbling, and they never made commitment. And when we converted, we did get on-demand consumers to convert in, but it wasn't like what we imagined it would be.
And so we decided, let's just lead with subscription. We've talked about this a bit externally, a bit internally. It's almost like the view is, do you want to be like a target or do you want to be like a Costco model? And what we started to realize is just we really like the kind of the Costco model instead, just a subscription-based product allows us to deliver lower-cost financial services products to our subscriber base, the ones that commit to us and want to be a part of our system.
And so we're really viewing as leading with subscription as the primary solution. And on-demand is still there. But now it's not used as much as a tool with the direct-to-consumer type of relationship with consumers. It's used more as a tool to help our sales and partnerships teams to work and deliver solutions to merchants that might be less comfortable with the merchant fees required to support BNPL. And if we can pass on some of the fees to the consumer directly in the merchant checkout, now the merchants much more comfortable with adding Sezzle into their checkout. So it's become more of a merchant acquisition tool than a consumer tool.

**Operator** (Operator):
And our next question is from Ryan Tomasello with KBW.

**Huan Chong** (Analysts):
This is Huan Chong on for Ryan. Congrats on a great quarter. Could you just help frame for us what the monthly spending is like for your average subscriber and how you're thinking about your current wallet share of either credit or spending within the current user base? Just trying to get a sense of how much room there could be for like a TTV per user growth, especially given the expanded product suite.

**Charles Youakim** (Executives):
Yes. We plan to keep on pushing forward with more and more products in our future. Some of those products are waiting for our national bank charter completion, like checking accounts, savings account products and potentially more in the financial services area or arena. So we think there's more wallet share with these consumers and more frequency. We know they love our product, but we just think there's probably a lot more there in terms of making these consumers -- having these consumers that are in love with us, do more with us.
But Lee, I don't know if you have any additional color on the first part of the question?

**Lee Brading** (Executives):
Yes, I'll follow up on a couple of items there. Yes, we haven't -- we're not disclosing the CAC, what we do from a subscription cost because we do a net number, and we have subscribers move in and out, and it's very easy to cancel and move in and out. So we just don't get into those numbers. But also add on to Charlie's comment on the wallet shares. We've looked at some others -- other companies out there and people are transacting with them 15-plus times a month, the consumers are. And we disclosed consumers using us what, 7 to 8 times a quarter. So we definitely think there's a lot of upside.

**Huan Chong** (Analysts):
Okay. Got it. That's helpful. And just in the most recent 10-Q, you broke out your new revenue disaggregation, which was helpful in getting a sense of that with the different moving pieces of take rate. Can you just help us understand the outlook for take rate? And do you see that roughly 11.8% rate in 3Q as something that's sustainable?

**Charles Youakim** (Executives):
Lee, do you want to take that?

**Lee Brading** (Executives):
Yes. We -- sorry, yes, I'll take that. The seasonality of our business, we definitely expect it to come down in Q4. And -- but we do -- I think last quarter, we did give guidance out there. At least on the call, we talked about seeing the take rate flat year-over-year, meaning '26 versus '25. But we had a strong quarter here in Q3, particularly driven by the subscriber side, if you look at take rate. And so we'd expect that probably up a little bit year-over-year on the take rate versus -- '26 versus '25.

**Operator** (Operator):
And the next question is from Rayna Kumar with Oppenheimer.

**Anthony Cyganovich** (Analysts):
This is Anthony Cyganovich filling in for Rayna. With AI-driven shopping assistance and agentic commerce becoming more prevalent, can you talk about how Sezzle is positioning itself to remain relevant at the checkout layer? Are there opportunities for Sezzle to become a preferred payment or financing option within AI-powered purchasing workflows?

**Charles Youakim** (Executives):
We're definitely thinking about a lot. I mean you hear us talk about AI a ton, I'm sure, and we really lean into it heavily. So we also think about it with our products and services to the consumer as well. I think it is a big win for our partnerships team right now because our partnerships team is looking at where are the big AI partnerships, where are the potentials, where can we get plugged in, where can we watch for fast risers and latch on quickly to become the partners of the winners of the future in AI. And we think it does matter.
But I think we're also helped a bit is that we have our Anywhere card where just like -- I'm not sure -- I asked this question to a bunch of investors about a year ago and asked who's using AI shopping assistant and it was still pretty low. But I even find myself using them now. And I'm probably a super early adopter because I try to adopt products and I like to. But I'm starting to use shopping assistants.
And basically, what I find is that when you connect into them, it's all about loading your card into the product -- and we have that card. We have a credit card for our consumers that's used as a payment vehicle. And so for our Anywhere customers, I think we're already kind of on that front, our Anywhere customers can load those cards into these virtual shopping assistants and then just be prompted to use us or to confirm the purchase.
So I think we already have an avenue that's helping us with the virtual card and our Anywhere subscription as a leading front, but we're also actively thinking about how else to get in there deeper because we really believe in it.

**Anthony Cyganovich** (Analysts):
That's helpful. Just as my follow-up, I mean, your profitability and cash generation has been improving a lot over the last year. Can you talk about how you're prioritizing capital allocation among buybacks, product investment, geographic expansion or potential M&A?

**Charles Youakim** (Executives):
It always starts with product and delivering to the consumer. That's the first thought whenever we're talking about capital allocation. But because we're such an efficient company with how we do things, it tends not to be a big usage of cash. To give you an idea like when we launch new products, it's basically bringing 3 or 4 new team members, especially now with AI.
I mean it's -- we've even started to discuss testing single-person teams, single-person teams bring things end-to-end more and more rather than multifaceted or multifunctional teams. So we're bringing on team members to launch and support products that doesn't tend to be a big use of funds. And then so that tends to lead to cash coming out of the balance sheet. And then we have decision-making there. Do we sit and wait? Do we do buybacks? Do we do dividends?
But we also have right in front of us our national bank charter application process. And that process also -- there's a bit of a lean towards putting on cash during that process because you want to show safety and soundness, too. So we have that in kind of the back of our heads as well.
I don't know, Lee, anything to add to that?

**Lee Brading** (Executives):
No, you're spot on hit on all the items. And I'd say we're constantly looking at all of those. And number one, as you mentioned, is organic investment back in the business. But with the excess, we're always looking for the best opportunity, best return.

**Operator** (Operator):
The next question comes from Hoang Nguyen with TD Cowen.

**Hoang Nguyen** (Analysts):
Congrats on the quarter. I wanted to start first with maybe on the gross margin. So over the past 4 quarters, it looks like you guys have been, again, at the high end, 65% or even exceed that, right? Do you think we're at the stage where the business is at a consistently higher level of profitability and maybe the high end is what we should think about the business going forward? And I have a follow-up.

**Charles Youakim** (Executives):
Yes, I'll let Lee give more detail on this. But I think it's hard for us to say just because we're learning about the product mix as the products get out into the market. And we think about gross margin as we launch products, but each one has like puts and takes on gross margin and what we are okay with. Like for instance, I'll give a more obvious caveat to gross margin. Sezzle Send is a product that we're okay with lower financial metrics on because we view it as a product that can help us acquire consumers. That's more of the focus. So it's a give and take. That product would have a lower gross margin. So it depends on that product grows in terms of like the next 12, 24 months on what happens to gross margin. But that kind of gives you the idea of like why it's hard to predict where it might be in 12 months, 24 months because we have some -- our own gives and takes of how we want to guide things.
But Lee, anything to add?

**Lee Brading** (Executives):
Yes. No, that's spot on. Yes, as we launch these new products, particularly Cash and Send, as you noted, lower margin. And typically, when you start off on the product too, you're going to have a higher provision or higher loss rate with that. So that type of -- that takes time to play out. And as Charlie mentioned earlier, we're just getting started with these products.

**Hoang Nguyen** (Analysts):
Got it. And maybe on the marketing, it looks like, I mean, marketing has gone up, but that also happened to your net subscriber adds, right? So net-net, I mean, how do we think about the efficiency of your marketing over the past year and coming into the holiday season, I mean, how should we think about the net subscriber add as we are about to enter the holiday?

**Charles Youakim** (Executives):
Well, we feel good about our efficiencies. We're always focused on efficiency. We always try to explain also marketing, just so people are aware, there's some fixed elements in marketing with our Timberwolves partnership, just quarter-to-quarter-to-quarter. We have some parts of marketing that are just the more people use our app, the more -- some of the marketing cost components just rise from consumer usage. And then some of it is discretionary. So it's kind of a mixed bag on the total marketing spend we get every quarter. But on the discretionary part, I feel like we've been even more deliberate, more conservative maybe or more -- wanting even more return from what we're spending over the last quarter-on-quarter.
But Lee, anything to add to that or clear up?

**Lee Brading** (Executives):
No, that was spot on.

**Operator** (Operator):
And at this time, there are no further questioners in the queue, and this does conclude our question-and-answer session. I would now like to turn the conference back over to Charlie Youakim for any closing remarks.

**Charles Youakim** (Executives):
Thank you. I usually close with a Buffett or Munger quote, but tonight, I wanted to share something JPMorgan said to Congress in 1912. During the Pujo hearings, he was asked whether commercial credit is based primarily on money or property. His answer, "No, sir, the first thing is character." Asked whether that came before money or property said, "Before money or anything else, money cannot buy it."
A few weeks ago, we filed our application to become a national bank. It's a long process and the outcome isn't guaranteed, but it made us take a hard look at what we've built, a model where customers stay current to keep using Sezzle, where we adjust spend limits so customers don't overextend and where customers who pay on time can build their credit history through Sezzle Up. We think that's what character looks like in the lending business. The numbers we shared to that matter, but what we're more focused on building is trust with our consumers, our merchants, our regulators and all of you.
And before we close, as always, a big thank you to the Sezzle team who accomplishes far more than you can believe and to our investors for your continued support. We'll talk to you again next quarter. Thanks.

**Operator** (Operator):
The conference has now concluded. Thank you for attending today's presentation, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SEZL_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Charles Youakim (CEO)｜guidance：全年營收成長財測上調至35%，指向原30%–35%區間上緣（原話："targeting the upper bound of our prior 30% to 35% range"）
- 2026-08-06｜Charles Youakim (CEO)｜guidance：調升全年調整後淨利財測至1.85億美元（原1.8億）（原話："guidance to $185 million from $180 million"）
- 2026-08-06｜Lee Brading (CFO)｜guidance：H1營收年增約40%，下半年營收財測約年增30%（原話："guiding kind of 30% up here in revenue for the top line"）
- 2026-08-06｜Lee Brading (CFO)｜guidance：2026全年營收收益率預期與2025年的11.4%相近（原話："will be similar to 2025's yield of 11.4%"）
- 2026-08-06｜Lee Brading (CFO)｜guidance：營收收益率其餘季度逐季下滑，Q4為季節低點（原話："step down sequentially for the remainder of 2026"）
- 2026-08-06｜Lee Brading (CFO)｜guidance：全年信用損失撥備預期落在GMV的2.5%–3%（原話："provision for credit losses will be in the 2.5% to 3% range"）
- 2026-08-06｜Charles Youakim (CEO)｜guidance：Q3核心行銷支出預期低於Q2（其他條件不變）（原話："You can expect a lower level of spend in Q3"）
- 2026-08-06｜Lee Brading (CFO)｜guidance：財測不含Sezzle Send貢獻（原話："Our guidance does not take into consideration Sezzle Send"）
- 2026-08-06｜Charles Youakim (CEO)｜guidance：財測未假設SezzleCash有重大上行（原話："guidance does not assume material upside from SezzleCash"）
- 2026-08-06｜Lee Brading (CFO)｜margin：Q2淨交易利潤率63.5%，位於55%–65%目標區間高端（原話："net transaction margin of 63.5%, which is at the high end"）
- 2026-08-06｜Lee Brading (CFO)｜margin：Q2營收收益率較去年同期擴張110bp至11.7%（原話："yield expanded 110 basis points year-over-year to 11.7%"）
- 2026-08-06｜Lee Brading (CFO)｜margin：Rule of 40分數91（營收成長加EBITDA利潤率）（原話："puts us right at a score of 91 for the Rule of 40"）
- 2026-08-06｜Lee Brading (CFO)｜margin：撥備上升歸因季節性與新用戶增加（原話："with new users comes higher provisioning"）
- 2026-08-06｜Lee Brading (CFO)｜margin：Q2營收收益率受去年低基期影響（易比較基期）（原話："we had an easy comp on the revenue yield in Q2"）
- 2026-08-06｜Lee Brading (CFO)｜margin：Pagaya等新產品入帳方式使take rate較低（原話："be not accretive to the take rate"）
- 2026-08-06｜Lee Brading (CFO)｜margin：SezzleCash/Pagaya類產品take rate較低但利潤率類似（原話："the take rates on those can be a little lower"）
- 2026-08-06｜Lee Brading (CFO)｜commitment：行銷支出只要回收期短於6個月就會持續投入（原話："as long as the math works for a less than 6-month payback"）
- 2026-08-06｜Charles Youakim (CEO)｜commitment：管理層稱Q2行銷是刻意測試較高支出，非新常態（原話："this was a deliberate step-up to test out higher levels"）
- 2026-08-06｜Charles Youakim (CEO)｜commitment：CEO稱6個月是回收期的邊界（原話："The 6 months is our edge."）
- 2026-08-06｜Charles Youakim (CEO)｜commitment：CEO表示不想太靠近6個月回收期邊緣，故略為收斂行銷（原話："a little bit more comfortable not going near the 6 months"）
- 2026-08-06｜Charles Youakim (CEO)｜commitment：預期銀行執照總時程12–18個月（原話："our expectations are 12 to 18 months in total"）
- 2026-08-06｜Lee Brading (CFO)｜capital_allocation：本季預計提交國家銀行執照申請（原話："planning to submit our application"）
- 2026-08-06｜Lee Brading (CFO)｜capital_allocation：流動性逾2.05億美元（原話："we had over $205 million in liquidity"）
- 2026-08-06｜Lee Brading (CFO)｜capital_allocation：總負債對股東權益僅0.5倍（原話："total debt to equity is also only 0.5x"）
- 2026-08-06｜Charles Youakim (CEO)｜product：SezzleCash平均預支金額約165美元，近10%符合資格新訂閱者首筆交易即預支（原話："approximately $165, and nearly 10% of eligible new"）
- 2026-08-06｜Charles Youakim (CEO)｜product：SezzleCash尚未對外行銷，僅對現有客群內部推廣（原話："we haven't even started marketing externally yet"）
- 2026-08-06｜Charles Youakim (CEO)｜product：Sezzle Send預計8月推出（原話："And coming in August, we plan to"）
- 2026-08-06｜Charles Youakim (CEO)｜product：Sezzle Send候補名單約10萬人（原話："we've already got about 100,000 users on the wait list"）
- 2026-08-06｜Charles Youakim (CEO)｜product：Sezzle Send非訂閱者手續費約每100美元3美元（原話："around $3 for $100 spend"）
- 2026-08-06｜Charles Youakim (CEO)｜product：Sezzle Send是首個大部分由AI建置的產品（原話："first product we produced where the vast majority of the"）
- 2026-08-06｜Charles Youakim (CEO)｜product：AI客服機器人分流68%的消費者來電（原話："AI support chatbot is deflecting 68% of consumer inbounds"）
- 2026-08-06｜Charles Youakim (CEO)｜product：On-Demand不再是主推產品，主推為訂閱方案（原話："The lead is join our subscription program"）
- 2026-08-06｜Charles Youakim (CEO)｜customer：活躍訂閱者達85.4萬，年增76.4%（原話："reached 854,000, up an incredible 76.4% year-over-year"）
- 2026-08-06｜Charles Youakim (CEO)｜customer：本季淨增14萬訂閱者，為訂閱方案推出以來單季最大（原話："We added 140,000 net new subscribers in the quarter."）
- 2026-08-06｜Charles Youakim (CEO)｜customer：管理層稱消費者信用表現正常（原話："everything seems just normal"）
- 2026-08-06｜Charles Youakim (CEO)｜risk：新用戶虧損率較高，新用戶成長超預期會使撥備高於模型（原話："new users have higher loss rates"）
- 2026-08-06｜Lee Brading (CFO)｜risk：反壟斷訴訟部分駁回被告撤案動議（原話："granted in part and denied in part the defendant's motion"）
- 2026-08-06｜Lee Brading (CFO)｜risk：反壟斷訴訟進入證據開示階段，預計延續至2027年（原話："entering the discovery phase, which is expected to go"）
- 2026-08-06｜Charles Youakim (CEO)｜competition：近期企業客戶新增Poshmark、Gymshark、Debenhams等（原話："include Poshmark, Gymshark, Debenhams, and several others"）
- 2026-08-06｜Paul Paradis (President)｜competition：早期商家傾向只選一家BNPL（獨家）（原話："Early days, a merchant would commit to one exclusively."）
- 2026-08-06｜Paul Paradis (President)｜competition：第二、第三家BNPL帶來增量銷售的案例加速企業銷售漏斗（原話："adding a second or third brings incremental sales"）

### 問答異常語氣（迴避／改口／保留）
- SEZL_Q2_2026_Earnings_Call_20260806.md｜問：Tomasello：下半年營收成長為何較Q2減速？Kumar同樣追問2H減速驅動因素｜答法：CFO以H1對H2的「基本算術」與財測保守（部分產品未計入）回應，未拆解減速成因；Kumar一題則轉談收益率低基期
- SEZL_Q2_2026_Earnings_Call_20260806.md｜問：Goetsch：行銷支出是否持續或加碼？｜答法：CEO答「I think it depends」，以開油門比喻、「all things being equal」及新產品可能抵銷作答，未給支出水準
- SEZL_Q2_2026_Earnings_Call_20260806.md｜問：Tomasello：回收期這麼好為何收斂行銷、是否有回收期承壓訊號｜答法：CEO以「comfort／edge」風險偏好回答，未直接說明有無回收期壓力的數據
- SEZL_Q2_2026_Earnings_Call_20260806.md｜問：Tomasello：營收成長約2/3來自用戶、1/3來自ARPU，後續是否維持此組合｜答法：CEO稱不看此拆分，改談產品成功率與SezzleCash/Send，未回答組合走向

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
{"date":"20261005","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"第三季財報提列／GMV 守在全年 2.5–3% 指引內且淨交易利潤率 ≥55% 即進場首倉；股價先跌破 95 美元而信用未惡化則分批反買","irr_base_pct":7.1,"ev5y_pct":40.2,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.4,"ev5y_pct":40.2,"irr_base_pct":7.1,"max_dd_pct":-70,"bull_5y_price":276.0,"bear_5y_price":54.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"第三季財報提列／GMV 守在全年 2.5–3% 指引內且淨交易利潤率 ≥55% 即進場首倉；股價先跌破 95 美元而信用未惡化則分批反買","price_at_dd":110.85,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
