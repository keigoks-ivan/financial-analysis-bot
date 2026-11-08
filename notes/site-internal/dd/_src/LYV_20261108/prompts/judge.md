你是 stock-analyst **v20 判斷 agent**，標的 LYV（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"LYV","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":10105.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results"},"note":"查無（新聞稿未列；未另抓第二來源）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income (AOI)","value":1179.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results"},"note":"查無（新聞稿未列；未另抓第二來源）"},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":892.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results"},"note":"查無（新聞稿未列；未另抓第二來源）"},{"id":"f_kpi3_free_cash_flow_adjusted","label":"Free cash flow—adjusted","value":934.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results"},"note":"查無（新聞稿未列；未另抓第二來源）"},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation","value":47.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results"},"note":"查無（新聞稿未列；未另抓第二來源）"},{"id":"f_kpi5_management_guidance_fy20","label":"Management guidance FY2026","value":"fan attendance approach 180M; Concerts & Sponsorship AOI double-digit growth; Ticketing AOI up high single-digits","period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results"},"note":"查無（新聞稿未列；未另抓第二來源）"},{"id":"f_kpi6_event_related_deferred_r","label":"Event-related deferred revenue","value":3818.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results"},"note":"查無（新聞稿未列；未另抓第二來源）"},{"id":"f_kpi7_diluted_eps","label":"Diluted EPS","value":1.69,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results"},"note":"查無（新聞稿未列；未另抓第二來源）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_lyv_gross_margin_pct","label":"LYV 毛利率","value":25.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LYV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lyv_operating_margin_pct","label":"LYV 營業利益率","value":2.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LYV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lyv_fcf_margin_pct","label":"LYV FCF 利潤率","value":5.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LYV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_msge_gross_margin_pct","label":"MSGE 毛利率","value":45.82,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSGE.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_msge_operating_margin_pct","label":"MSGE 營業利益率","value":17.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSGE.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_msge_fcf_margin_pct","label":"MSGE FCF 利潤率","value":24.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSGE.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sphr_gross_margin_pct","label":"SPHR 毛利率","value":55.77,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPHR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sphr_operating_margin_pct","label":"SPHR 營業利益率","value":-1.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPHR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sphr_fcf_margin_pct","label":"SPHR FCF 利潤率","value":22.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPHR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tko_gross_margin_pct","label":"TKO 毛利率","value":60.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TKO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tko_operating_margin_pct","label":"TKO 營業利益率","value":21.71,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TKO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tko_fcf_margin_pct","label":"TKO FCF 利潤率","value":31.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TKO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmg_gross_margin_pct","label":"WMG 毛利率","value":45.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmg_operating_margin_pct","label":"WMG 營業利益率","value":16.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmg_fcf_margin_pct","label":"WMG FCF 利潤率","value":3.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":175.25,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":7.33,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":50.69,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-0.46 → -0.46）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.9 → 1.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.9 → 2.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":-0.46,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.9,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":2.9,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.55,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS -0.44 → -0.46（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.48,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":3647.71,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 11905.18、現金 8257.47（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":235.7,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":44953.53,"period":"2026-11-08","unit":"USD m","basis":"市值 41305.82 ＋ 淨負債 3647.71","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":28534.92,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":30976.6,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.58,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 175.25 / W52 161.72 / W104 152.64 / W250 116.07 / W250 13週斜率 0.82%"},{"id":"f_ma_w52","label":"52 週均線","value":161.72,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":152.64,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":116.07,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.82,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 指出自助售票系統與場館自行售票的競爭「顯著且增加」，並列出 SeatGeek、Fever、CTS Eventim 等票務對手，且大型科技／電商公司可能進入。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":"We also face significant and increasing competition from companies that sell self-ticketing systems, as well as from venues that choose to integrate self-ticketing systems into their existing operations or acquire primary ticketing service providers.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素：自助售票與客戶自售可能使票務量下降。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":"The intense competition that we face in the ticketing industry could cause the volume of our ticketing services business to decline.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"美國司法部反壟斷陪審團審判於2026年3月開始；政府主張5至7年長約使場館無法選擇對手。","source":"ABC7 News 報導 Antitrust trial begins","url":"https://abc7news.com/post/antitrust-trial-begins-could-lead-breakup-ticketmasters-parent-company-live-nation/18675403/","excerpt":null,"as_of":"2026-03-09","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"2026年分析稱 Eventim 積極擴張美國業務挑戰 Live Nation","source":"Mammoth Times / Finterra","url":"https://business.mammothtimes.com/mammothtimes/article/finterra-2026-3-9-live-nation-lyv-navigating-the-experience-economy-amidst-a-landmark-regulatory-shift","excerpt":null,"as_of":"2026-03-09","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K FY2025 檔案存在，客戶集中度揭露段落待核（搜尋摘要未顯示）","source":"SEC EDGAR LYV 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 揭露：無任何單一客戶占合併營收超過 10%（任何年度）","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":"There were no customers that individually accounted for more than 10% of our consolidated revenue in any year.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Moody's 2025-06 將 Live Nation CFR 升至 Ba2，展望穩定；未見 2026 年評等行動","source":"Moody's via researchpool","url":"https://app.researchpool.com/provider/moodys-investors-service/lyv-moodys-ratings-upgrades-live-nations-cfr-to-ba2-outlook-is-stable-l8xfrF7mSk","excerpt":null,"as_of":"2025-06-01","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Live Nation Q2 2026 新場館管線：2027 年底前預計開出 25 座以上大型場館（>3,000 席），run-rate 可增加約 1,500 萬人次容量（供給端擴張）","source":"Live Nation Q2 2026 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001335258/000133525826000034/lyv-2026q2xex991er.htm","excerpt":"Current pipeline of more than 25 large (over 3,000 seats) venues expected to open through the end of 2027, adding capacity for an incremental 15 million fans on a run rate basis","as_of":"2026-07-31","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q1 2026 電話會議：管理層預期場館開幕在 2027、2028 加速，未給確切時程","source":"MarketBeat, Live Nation Q1 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/live-nation-entertainment-q1-earnings-call-highlights-2026-05-11/","excerpt":"Berchtold said the company expects venue openings to accelerate in 2027 and 2028, though he declined to provide exact timing by year.","as_of":"2026-05-11","retrieved_at":"20261108","affects":["moat_trend","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026：2026 年演出票房預售 +13%、事件遞延收入 Q3 歷史最高、年增 8%；Q3 營收 $101 億 +19%","source":"Live Nation Q3 2026 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001335258/000133525826000052/lyv-2026q3xex991er.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2 2026：事件遞延收入 $64 億、年增 25%；CEO 稱未見消費者縮手，取消率 1.1% 低於歷史均值 1.6%","source":"MarketBeat, Live Nation Q2 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/live-nation-entertainment-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Goldman Sachs 2026 音樂報告：live 需求結構性上升、較一般可選消費不循環","source":"IQ Magazine, Goldman Sachs hails 'insatiable demand' for live","url":"https://www.iqmagazine.com/?p=378324","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 揭露：2024-05 DOJ 與州政府提告反壟斷，求償含剝離 Ticketmaster、取消部分票務合約、禁止反競爭行為與金錢賠償；原定 2026-03-02 開審。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":"In May 2024, we were sued by the United States Department of Justice and state authorities for alleged violations of various laws pertaining to antitrust, competition, unlawful or unfair business practices, restraint of trade, and other causes of action, with various forms of relief requested for the alleged violations, including without limitation the divestiture of Ticketmaster by the Company","as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"搜尋摘要：DOJ 於 2026-03-09 開審後與 Live Nation 和解（2.8 億美元基金、剝離至多 13 座圓形劇場、費用上限 15%，不要求剝離 Ticketmaster，待 Tunney Act 法院核准）；拒絕和解的各州續訴，2026-04-15 陪審團認定 Live Nation 在主要票務市場違反反壟斷法。Live Nation 稱將重提 JMOL 並上訴，結構性救濟待法院裁定；估計州方三倍賠償可達 4.5 億美元。資料只到約 2026-05，後續狀態未確認。","source":"WebSearch 摘要（Thompson Coburn、The Ticketing Business 等）","url":"https://www.thompsoncoburn.com/insights/live-nation-and-ticketmaster-found-liable-for-antitrust-violations-by-federal-jury/","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"陪審團認定 Live Nation／Ticketmaster 違反反壟斷法","source":"The Ticketing Business","url":"https://www.theticketingbusiness.com/2026/04/jury-rules-live-nation-ticketmaster-held-monopoly-in-landmark-case/","excerpt":null,"as_of":"2026-04-16","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#none","axis":"reg_tariff_export","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2020 10-K 風險因子列出國際營運面臨政治不穩、外交關係惡化與不利經濟環境，尤其是新興市場；搜尋結果未見實體製造或供應鏈單點的揭露（僅此一次搜尋，且只取得舊年度 10-K）。","source":"Live Nation Entertainment, Inc. Form 10-K FY2020","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525821000009/lyv-20201231.htm","excerpt":"political instability, adverse changes in diplomatic relations and unfavorable economic and business conditions in the markets in which we currently have international operations or into which we may expand, particularly in the case of emerging markets","as_of":"2021-02-26","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Ticketing 營收 +9%（+$72.7M），AOI 由 $285.9M 增至 $315.7M，fee-bearing ticket sales 98.3M（vs 89.1M）","source":"Live Nation Form 10-Q / 8-K Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001335258/000133525826000053/lyv-20260930.htm","excerpt":"Our Ticketing segment's revenue for the quarter increased by $72.7 million, or 9%","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Sponsorship & Advertising 營收 $442.7M→$505.7M（+14%），AOI +12% 至 $350.2M，國際市場占成長 65%","source":"Live Nation Q3 2026 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001335258/000133525826000052/lyv-2026q3xex991er.htm","excerpt":"from $442.7 million in the third quarter of 2025 to $505.7 million in the third quarter of 2026","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 事件相關遞延收入創高 $3.8B（+8%）；2027 預付廣告為雙位數成長；全年出席人數預期近 1.8 億；北美 +13%、體育場與露天劇場占成長 90%；2026 年每月至 10 月售票均高於去年（摘要整理，未逐字核對）","source":"Live Nation Q3 2026 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001335258/000133525826000052/lyv-2026q3xex991er.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","valuation","triggers"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"2026 年 3 月起 DOJ 與各州反壟斷審判；紐約州律師稱 Ticketmaster 每張票平均留 $7.58；法官 2 月駁回部分壟斷主張（含票價推高論）；結果報導互相矛盾，未確認；FTC 另有轉售訴訟","source":"NPR/TPR 2026-03-03 'The Live Nation trial could reshape the music industry'","url":"https://www.tpr.org/2026-03-03/the-live-nation-trial-could-reshape-the-music-industry-heres-what-you-need-to-know","excerpt":null,"as_of":"2026-03-03","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 財報電話會議：遞延收入給管理層信心；上半年美國受體育場檔期影響；2026–2027 透過併購與興建新增約 1,500 萬人容量","source":"MarketBeat Q2 2026 call highlights","url":"https://www.marketbeat.com/instant-alerts/live-nation-entertainment-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子提及來自自助票務系統業者及大型科技/電商公司進入票務市場的競爭","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"報導稱 DOJ 和解要求 Ticketmaster 開放第三方使用其技術系統售票（二手報導，需 Tunney Act 核准）","source":"tdp-frontend.pages.dev 轉載文章 2026-03-09","url":"https://tdp-frontend.pages.dev/article/2026-03-09-live-nation-keeps-ticketmaster-but-faces-sweeping-concert-industry-reforms-f2b9c3bb","excerpt":"Ticketmaster will be required to enable third parties to use its technology system to offer tickets.","as_of":"2026-03-09","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"同報導稱和解將 Live Nation 長期獨家合約上限訂為四年","source":"tdp-frontend.pages.dev 轉載文章 2026-03-09","url":"https://tdp-frontend.pages.dev/article/2026-03-09-live-nation-keeps-ticketmaster-but-faces-sweeping-concert-industry-reforms-f2b9c3bb","excerpt":"The agreement caps Live Nation's long-term exclusivity contracts at four years","as_of":"2026-03-09","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 2026 財報新聞稿列出與 Spotify Reserved 的售票合作，利用 Ticketmaster 平台","source":"Live Nation 8-K Q2 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001335258/000133525826000034/lyv-2026q2xex991er.htm","excerpt":"New ticket access partnership with Spotify's Reserved leverages Ticketmaster's platform to help more fans access tickets","as_of":"2026-07-30","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 稱 Ticketmaster 2025 年經多通路（行動、線上、聯盟夥伴）配售 6.46 億張票，並以擴大非服務費收入為方向","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":"We are focused on selling tickets through a wide set of sales channels including mobile, online and affiliate partners while continuing to broaden our digital rollout.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 10-Q：管理層因 Ticketing 上半年表現，預期該分部全年 AOI 中個位數成長（僅分部層級定性 guidance，未見全公司量化 guidance）","source":"Live Nation 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001335258/000133525826000035/lyv-20260630.htm","excerpt":"we are anticipating mid-single digit AOI growth for the segment for the full year","as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q1 2026 後 Zacks 稱共識 EPS 估計一個月內下修 36.01%；Q1 調整後每股虧損 32 美分，劣於共識虧損 27 美分","source":"Zacks（經搜尋摘要）Q1 2026 earnings 報導","url":"https://shop.atlasrr.com/first-dry/LYV-Q1-2026-Earnings-Staggering-EPS-Miss-Amid-Seasonally-Weak-Quarter-30-1494","excerpt":"The consensus estimate has shifted -36.01% due to these changes.","as_of":"2026-05-29","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Walnut Invest（第三方聚合站，2026年10月）：24位分析師預期 FY2026 EPS -$0.46、營收 $28.1B；FY2027 EPS $1.93、營收 $30.7B；目標價均值 $202.17、中位 $209；評級 20 buy/3 hold/2 sell","source":"Walnut Invest LYV forecast","url":"https://walnutinvest.com/stocks/lyv/forecast","excerpt":null,"as_of":"2026-10-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga（約2026年9月）：26位分析師共識 Buy，平均目標價 $191，區間最高 $222、最低 $145；Citi 目標價由 $181 升至 $212，Bernstein 由 $200 升至 $215","source":"Benzinga LYV price targets","url":"https://www.benzinga.com/quote/LYV/price-targets","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026 10-Q 九個月營業利益減少 $350.5M，歸因主要為 Governmental Investigations and Litigation（非 guidance 變動）","source":"Live Nation 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001335258/000133525826000053/lyv-20260930.htm","excerpt":null,"as_of":"2026-11-01","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q4 2025 財報 8-K：2026 資本支出預期 $1.1–1.2B、股數大致不變","source":"Live Nation 8-K Q4 2025 earnings release","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000007/lyv-2025q4xex991er.htm","excerpt":"•2026 capital expenditures expected to be $1.1 to $1.2 billion ◦Approximately $800 to $850 million of total capex is for venue expansion and enhancement projects","as_of":"2026-02-19","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-04-15 紐約聯邦陪審團認定 Live Nation／Ticketmaster 違反聯邦與州反壟斷法（33 州＋DC 起訴，DOJ 審理中途和解）；救濟與損害賠償由法官另行決定，states 要求最高約 7 億美元並求分拆 Ticketmaster，Live Nation 表示將上訴。","source":"Axios／Music Business Worldwide 等報導（搜尋摘要）","url":"https://www.axios.com/2026/04/15/live-nation-ticketmaster-lose-antitrust-case","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R","moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FTC 與七州 2025 年 9 月對 Live Nation／Ticketmaster 提起消費者保護訴訟（價格欺騙、購票限制、經紀商轉售），公司 2026 年 1 月提出駁回動議。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":"In September 2025, the United States Federal Trade Commission (the “FTC”), joined by the attorneys general of seven states, filed a lawsuit against Live Nation Entertainment, Inc. and Ticketmaster L.L.C. in the Central District of California.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026 年多筆中小型併購：義大利 ForumNet（預計 2026-04 交割）、阿根廷 Movistar Arena／Dale Play Live 多數股權；未見大型合併。","source":"搜尋摘要（pulse.bot／rallies.ai 等，部分為聚合站）","url":"https://www.pulse.bot/ma/deals/live-nation-acquires-majority-stake-in-argentinas-movistar-arena-buenos-aires-a5bf86da-5471-4b35-b233-fd57f9f263a3/","excerpt":null,"as_of":"2026-06-15","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"Astroworld 相關訴訟自 2025 年初起已全數和解，公司損失超過保險回收。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":"All lawsuits relating to Astroworld have been resolved since early 2025. We incurred losses in excess of our insurance recovery in connection with those lawsuits.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026 年多筆中小型收購（ForumNet 義大利、Movistar Arena／Dale Play Live 阿根廷、Balada 巴西 60%），金額未揭露，無大型合併。","source":"搜尋摘要（pulse.bot／mergerlinks 等）","url":"https://www.pulse.bot/ma/deals/live-nation-acquires-majority-stake-in-argentinas-movistar-arena-buenos-aires-a5bf86da-5471-4b35-b233-fd57f9f263a3/","excerpt":null,"as_of":"2026-06-15","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-04-15 陪審團認定違反反壟斷法，損害賠償與救濟待法官裁定，公司將上訴。","source":"Axios","url":"https://www.axios.com/2026/04/15/live-nation-ticketmaster-lose-antitrust-case","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R","valuation"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"FTC＋七州 2025-09 消費者保護訴訟，公司 2026-01 提駁回動議。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm","excerpt":"The Company filed a motion to dismiss the complaint in January 2026.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#2","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"證券集體訴訟（C.D. Cal.，涵蓋 2022-02-23 至 2023-11-20 買入者）為既有案件，搜尋未見近12個月新結果。","source":"Robbins LLP／law-firm 公告（搜尋摘要）","url":"https://www.businesswire.com/news/home/20230804293319/en/Shareholder-Alert-Robbins-LLP-Informs-Shareholders-of-Class-Action-Filed-Against-Live-Nation-Entertainment-Inc.-LYV","excerpt":null,"as_of":"2023-08-04","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"LYV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.78,"operating_margin_pct":2.94,"fcf_margin_pct":5.23,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LYV","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MSGE","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.82,"operating_margin_pct":17.31,"fcf_margin_pct":24.21,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSGE","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SPHR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.77,"operating_margin_pct":-1.68,"fcf_margin_pct":22.68,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPHR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TKO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.32,"operating_margin_pct":21.71,"fcf_margin_pct":31.1,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TKO","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WMG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.77,"operating_margin_pct":16.11,"fcf_margin_pct":3.94,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMG","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"LYV"},"financial_history":{"ticker":"LYV","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":16681254000.0,"revenue_yoy_pct":null,"gross_margin_pct":25.98,"operating_margin_pct":4.14,"net_income":266440000.0,"diluted_eps":0.64,"free_cash_flow":1481761000.0,"fcf_margin_pct":8.88,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":22726317000.0,"revenue_yoy_pct":36.24,"gross_margin_pct":23.92,"operating_margin_pct":4.71,"net_income":556893000.0,"diluted_eps":1.34,"free_cash_flow":887717000.0,"fcf_margin_pct":3.91,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":23155625000.0,"revenue_yoy_pct":1.89,"gross_margin_pct":24.94,"operating_margin_pct":3.51,"net_income":896287000.0,"diluted_eps":2.74,"free_cash_flow":1050019000.0,"fcf_margin_pct":4.53,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":25201406000.0,"revenue_yoy_pct":8.83,"gross_margin_pct":25.55,"operating_margin_pct":4.89,"net_income":495972000.0,"diluted_eps":-0.24,"free_cash_flow":304979000.0,"fcf_margin_pct":1.21,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/LYV/LYV_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Live Nation Entertainment, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Good afternoon. My name is John, and I will be your conference operator today. At this time, I would like to welcome everyone to Live Nation's Third Quarter 2026 Earnings Call.
I would now like to turn the call over to Ms. Yong. Thank you, Ms. Yong. You may begin your conference.

**Amy Yong** (Executives):
Good afternoon, and welcome to the Live Nation Third Quarter 2026 Earnings Conference Call. Joining us today is our President and CEO, Michael Rapino; and our President and CFO, Joe Berchtold.
We would like to remind you that this afternoon's call will contain certain forward-looking statements that are subject to risks and uncertainties that could cause actual results to differ, including statements related to the company's anticipated financial performance, business prospects, new developments and similar matters. Please refer to Live Nation's SEC filings, including the risk factors and cautionary statements included in the company's most recent filings on Forms 10-K, 10-Q and 8-K for a description of risks and uncertainties that could impact the actual results.
Live Nation will also refer to some non-GAAP measures on this call. In accordance with the SEC Regulation G, Live Nation has provided definitions of these measures and a full reconciliation to the most comparable GAAP measures in our earnings release. The release reconciliation can be found under the Financial Information section on Live Nation's website.
With that, we will now take your questions. Operator?

**Operator** (Operator):
[Operator Instructions] And the first question comes from the line of David Karnovsky with JPMorgan.

**David Karnovsky** (Analysts):
Joe, I wanted to see if you could unpack the Q3 result a bit. It looks like fan count came in even higher than expected. So can you give some color on where you saw that added growth and how it flowed to concerts and ticketing AOI? And can you also just remind us of any preopening expense growth in the quarter?

**Joe Berchtold** (Executives):
Thanks, David. Yes, great quarter for concerts with attendance of over 60 million. I think the first time we've had that level of attendance, up almost 20%. Both North America and international doing well. International, in particular, was up 29% in every one of the regions. So Latin America, Europe, Asia, all up at least 15%. So we're seeing consistently strong performance globally. In North America, we had a very good amphitheater, including September being our largest amphitheater month overall.
And then globally, it was a very big stadium quarter. Stadiums drove over half of the global fan growth, up measurably in both North America and internationally. North America, a chunk of that being the timing that we've talked about before, where the stadium timing this year was a bit later than it was in previous years, just given how we had to manage the logistics around the World Cup. So overall, excellent, and that obviously flowed through to the ticketing business. Ticketing business, 95% of their growth was from concerts. So certainly benefited from the great attendance that we had at our shows.

**Operator** (Operator):
And the next question comes from the line of Stephen Laszczyk with Goldman Sachs.

**Stephen Laszczyk** (Analysts):
Joe and Michael, maybe just digging a bit deeper into the growth at Ticketmaster. It's come in a bit better than expectations over the course of this year. I think you're now calling out high single-digit AOI growth for the full year. Just would be curious if you could talk more about the strength you're seeing play out this year, the durability of those trends and then ultimately, how you would expect to close out the year for Ticketmaster.

**Joe Berchtold** (Executives):
Sure. I'll get that started. So first of all, better than expected even in terms of the fan growth in our concert business, which we've now guided towards close to 180 million. So that obviously supports the Ticketmaster business. Ticketmaster has also continued to add a number of clients, particularly internationally, with over 20 million net new tickets so far this year. So that continues to perform well.
We had flagged a year or so ago that we thought that there was likely to be some headwinds on the secondary side as we really continue to increase the enforcement on the concert secondary, which we expected to reduce that business. And as we noted, we have some offsets with increased performance on the sports side. So we're not seeing that headwind for the year.
So with that, we took up our guidance to now expect high single-digit AOI growth for the year. It's been great year-to-date. Q3 was very strong in part because we had a number of substantial onsales for shows next year, Harry Styles, Bruno Mars, Oasis, Metallica, all being substantial onsales in the third quarter. So that's already set us up now with some nice momentum heading into next year.

**Operator** (Operator):
And the next question comes from the line of Brandon Ross with LightShed Partners.

**Brandon Ross** (Analysts):
First, I just wanted to get a clarification or follow-up on David's question and wanted to hone in on the impact of Venue Nation specifically on your concert numbers. There's a lot of moving pieces there. You're acquiring venues, preopening in others, but the O&O fans should be more profitable. How should investors think about how that all nets out at this point in time?

**Joe Berchtold** (Executives):
Yes. As you said, Venue Nation is having a great year. We expect to have about 75 million fans attend our venues worldwide. So we're seeing solid growth from that, continued solid growth as well from third-party fans as we're looking at roughly 20 million fan growth overall. So I would say pretty comparable contribution to our overall fan growth from the year from both operated and non-operated fans. Clearly, the operated fans are higher profitability per fan, higher margin per fan. When you look at the overall numbers, the couple of pieces you need to take into account with your math are one is the stadium fans because those are the highest-priced tickets will tend to be a lower margin.
And then preopening costs that we've talked about, which is just as we're ramping up the venue side, these early years, this year and for the next couple of years, we're also ramping up preopening costs. So that's -- that all just needs to get put into the math. And as we get into next week in our Investor Day, we'll lay out more for you guys, the ramp of what we expect in terms of the venue fans as well as the investment overall, including the preopening costs over the next few years.

**Operator** (Operator):
And the next question comes from the line of Cameron Mansson-Perrone with Morgan Stanley.

**Cameron Mansson-Perrone** (Analysts):
To follow up on Venue Nation, you've acquired a handful of venues this year. Some of those like Milan, I believe, have closed. But could you give us an update on what's closed and what you're expecting in terms of the timing of acquisition closes across some of these markets like Prague, Paris, Santiago, Copenhagen, for example?

**Michael Rapino** (Executives):
I think you all know we have an Investor Day next week. We're trying to get today to anything that you want kind of specific around the quarter. But we're going to take you through a great presentation next week and give you much more detail around Venue Nation, what rolls out, AI impact, all the good things you want to know about the next few years on what we're rolling out to build your model. So we'll see you there next week and give you those details.

**Operator** (Operator):
And the next question comes from the line of Ian Moore with Bernstein Research.

**Ian Moore** (Analysts):
Just to hone in again on kind of the Venue Nation openings this year in the quarter. You've acquired and obviously opened organically a number of venues. I guess of the ones that are joined this year, still ramping, what's kind of been the biggest, I guess, surprise versus your expectations? And what's driving that? Is it more shows, more spend per fan, maybe sponsorship?

**Joe Berchtold** (Executives):
I think the main thing that we've seen this year, both of our operated and third-party, is just the strength of the consumer, right? All year, we've been reading in the press about all the concerns about consumer spending, are they going to keep going to shows? Are they going to keep spending at shows? Will shows close? Will they go on sale well? And we are absolutely seeing continued strong consumer demand globally in all these venues.
And you look at some of the amphitheaters we opened here in the U.S., had just about a full slate of shows, performed very well. Premium did well, continue to see strength there. The few arenas we've acquired in Europe, all of them doing well. Sponsorship sales on the B2B side continuing to do well. So I wouldn't call out any one of them as being particular, but I would just note the continued strong dynamics on all of the venues.

**Operator** (Operator):
And the next question comes from the line of Kutgun Maral with Evercore ISI.

**Kutgun Maral** (Analysts):
I had a follow-up on concerts where you had a really strong quarter. If I look at the first 9 months of the year, concerts AOI is up about 4%. So your outlook for double-digit growth implies that the fourth quarter loss narrows by at least $30 million or so versus last year, and I imagine it will narrow meaningfully more than that. I guess with fans now approaching 180 million for the year, that implies about 12% fan growth in Q4. Can you help unpack the main drivers of the implied AOI improvement a bit more for next quarter?

**Joe Berchtold** (Executives):
Yes. I think we've said a number of things over the course of the year. I think we got into pretty good detail over the first couple of quarters explaining what was going on with the results for each of those quarters and how we saw the full year playing out. I think we've been consistent that we expected to see AOI growth for the full year in concerts hitting double digits, and we reiterated that today.
So no change in that overall expectation. I laid out earlier some of the puts and takes that we have, very strong overall fan growth, strong in both venues we operate as well as third-party venues. The margin and per fan economics can get impacted by what type of venue it is sometimes, but I think we've given you the pieces there. And then we've also given you the preopening costs.
The last piece that I would note as being an impact is the marketing expense that gets written off for prepaid advertising at the end of the year. We noted here that through the third quarter, that was up double digits. So you can assume the very good news that our fourth quarter gets impacted by prepaid advertising for tours that are on sale and performing well for next year. So that's the best problem in the world to have.

**Operator** (Operator):
And our final question comes from the line of Steven Cahall with Wells Fargo.

**Steven Cahall** (Analysts):
So just wanted to understand the upgrade to fan count growth. I think it's about 3% above what you'd guided to before. Is that upside from your expectation that you're all seeing in the second half? Or is it more that as you've gotten visibility into the year, you're more comfortable upgrading that? Just trying to understand how the business is performing versus your expectation as we roll into next year and if you feel like you have incremental momentum. And then just a housekeeping one. How do we think about the partner share of venue CapEx flowing through the cash flow statement in 2026?

**Joe Berchtold** (Executives):
So on the upgrade to the expected attendance, I think it's -- number one thing is the shows are just consistently doing well. So our sell-through rate is higher this year than it was last year. Our cancellation rate is lower. At the start of the year, we probably would have been planning for those to be in line. So for those to outperform and at -- and our business, that can account for millions of incremental fans.
I think we've ended up stronger on our stadium volume than we thought early in the year, given what we had to manage through with the World Cup here in the U.S. Those would be your 2 largest factors that would have driven the increase. In terms of how we're managing all of the economics, why don't we save that one for Investor Day, so we can go through in more detail and make sure we're answering all of the questions on how the capital is being deployed, what pieces of it are ours versus partners, and what the implications that has for IRRs and rates that we're seeing every year.

**Operator** (Operator):
Thank you. And that concludes the question-and-answer session, and that also concludes today's teleconference. We thank you for your participation. You may disconnect your lines at this time.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LYV_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Joe Berchtold｜guidance：CFO 說全年演唱會財測上調，預期全年粉絲數雙位數成長，帶動營收與 AOI 雙位數成長及利潤率擴張（原話："I think we've stepped up our expectation now"）
- 2026-07-30｜Joe Berchtold｜guidance：CFO 說美國粉絲成長全部落在下半年（上半年受體育場檔期影響）（原話："all the fan growth in the U.S. will be in the second half"）
- 2026-07-30｜Joe Berchtold｜guidance：CFO 說 Ticketmaster 全年 AOI 成長預期上調至中個位數（原話："increased our expectation for AOI growth for the full year"）
- 2026-07-30｜Joe Berchtold｜guidance：CFO 說露天劇場約 70% 的全年成長集中在下半年（原話："mainly back half, 70% focused in terms of the"）
- 2026-07-30｜Michael Rapino｜guidance：CEO 說 2027 年預訂量已有大比例到位，各場館類型看來仍強（原話："We already have a big percentage of our bookings in"）
- 2026-07-30｜Joe Berchtold｜margin：CFO 解釋利潤率擴張的基礎：自營場館粉絲數成長快於第三方場館（原話："the foundation of what sets us up for margin expansion."）
- 2026-07-30｜Joe Berchtold｜margin：CFO 對自營場館成長較快的口徑：Live Nation 只經營少數場館，自營端有更多可著力的環節（原話："We run a small minority of venues."）
- 2026-07-30｜Joe Berchtold｜margin：CFO 提供 Ticketmaster 收費票數成長口徑（高個位數）（原話："fee-bearing ticket count by high single digits"）
- 2026-07-30｜Joe Berchtold｜margin：CFO 說現場人均消費全面上升（原話："per caps on-site spending is up."）
- 2026-07-30｜Michael Rapino｜customer：CEO 說至今未見消費者購買端問題（原話："we've seen no consumer issues to date in terms"）
- 2026-07-30｜Michael Rapino｜customer：CEO 說取消率 1.1%，低於歷史平均 1.6%（原話："at 1.1% cancellations versus 1.6% average."）
- 2026-07-30｜Michael Rapino｜customer：CEO 說酒類消費年增，未見消費者減少飲酒（原話："Liquor is up year-over-year"）
- 2026-07-30｜Michael Rapino｜competition：CEO 說不把 Spotify 視為票務競爭者，Spotify Reserved 為付費取得預售票額的傳統合作（原話："we don't look at Spotify as a ticketing"）
- 2026-07-30｜Michael Rapino｜competition：CEO 說 Spotify 配額在全球規模上很小（原話："small allocation on a global basis"）
- 2026-07-30｜Joe Berchtold｜competition：CFO 說二級市場票務占全球 GTV 低雙位數（原話："Secondary now on a global GTV basis is below teens."）
- 2026-07-30｜Joe Berchtold｜competition：CFO 說演唱會二級市場票約占全球 GTV 5%（原話："probably 5% of our global GTV."）
- 2026-07-30｜Michael Rapino｜competition：CEO 說日本市場自家占有率很小，90% 為本地業務（原話："We have a very small market share today."）
- 2026-07-30｜Joe Berchtold｜product：CFO 說 Ticketmaster 已進入 6 個拉美與 6 個亞太市場（原話："now in 6 Latin America markets, 6 Asia Pacific markets"）
- 2026-07-30｜Joe Berchtold｜product：CFO 說用 AI 輔助 Ticketmaster 的程式開發（原話："we're using AI to help power our coding and"）
- 2026-07-30｜Michael Rapino｜product：CEO 說 Spotify Reserved 於 5 月以 Role Model 巡演首度上線（原話："We launched Spotify in May with Role Model"）
- 2026-07-30｜Joe Berchtold｜capital_allocation：CFO 說今年已完成 3 座場館收購（原話："we've completed the acquisition of 3 arenas so far"）
- 2026-07-30｜Joe Berchtold｜capital_allocation：CFO 說 2027 年底前預計再有 4 至 5 座收購（原話："probably 4 or 5 in that period"）
- 2026-07-30｜Joe Berchtold｜capital_allocation：CFO 說資本支出增加的效益要到 2028 年才明顯（原話："probably '28 before we really start seeing the impact"）
- 2026-07-30｜Joe Berchtold｜commitment：CFO 說明年資本支出為漸進增加，不會倍增（原話："we're not doubling, tripling. We're not leaping."）
- 2026-07-30｜Joe Berchtold｜commitment：CFO 說會繼續淘汰報酬不達標的專案（原話："turning down a lot of projects that don't."）
- 2026-07-30｜Michael Rapino｜risk：CEO 說拉美仍在早期，巴西等大型場館尚未營運（原話："we're in the second kind of inning of the 9-inning game"）
- 2026-07-30｜Michael Rapino｜risk：CEO 說約九成演出不會完售，需靠分銷夥伴協助（原話："90% of shows don't sell out"）

### 問答異常語氣（迴避／改口／保留）
- LYV_Q2_2026_Earnings_Call_20260730.md｜問：Steven Cahall 問新增 1,500 萬粉絲產能是否意味 2027 年再度雙位數粉絲成長｜答法：CFO 未回答是否雙位數，表示現在談明年與 1,500 萬運行速率如何流入「還太早」（原文 'premature to talk specifically about next year'）
- LYV_Q2_2026_Earnings_Call_20260730.md｜問：Peter Henderson 問 2027 早期巡演管線與 2026 相比如何｜答法：CEO 未給比較數字，改談一貫的全球擴張策略，僅說「已有大比例預訂」「仍早但令人鼓舞」
- LYV_Q2_2026_Earnings_Call_20260730.md｜問：Robert Fishman 問 2027 年資本支出更新｜答法：CFO 稱規劃仍在早期不給具體數字，只說會是漸進增加

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
{"date":"20260518","verdict":"觀望 — thesis 完整（Concerts +11%、Sponsorship +21%）但估值🔴過熱（PEG 2.6 + 5Y 80% 分位）+ Subramanian remedy 二元未明。等 5 或裁決明朗化","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"監管衝擊有限：DOJ remedy phase 不強制 Ticketmaster + Concerts 結構性分拆，僅 behavioral remedy（15% fee cap、開放 SeatGeek/StubHub），對集團 AOI 影響 &lt; 5%。","columns":{"2Y 驗證點（至 2028）":"2027 Judge Subramanian remedy 公布；若 behavioral-only → H1 ✓；若 structural break-up → H1 ✗。Ticketmaster Q AOI margin 維持 ≥ 32%。","5Y 驗證點（至 2031）":"上訴階段（若有）2030 結案，遠端 Ticketmaster 護城河仍在；fee cap 後 Ticketmaster Revenue 仍 +6-8% 年成長。","10Y 驗證點（至 2036）":"監管常態化後 Ticketmaster ARR 仍佔集團 25-30% AOI，垂直整合 synergies 保留。","驗證指標":"(1) Judge Subramanian 裁決文本；(2) Ticketmaster AOI margin（門檻 ≥ 32%）；(3) 集團 AOI YoY ≥ +8%"}},{"id":"H2","text":"Concerts 結構性需求延續：Gen Z + Millennial 體驗消費偏好不變，Stadium 大型 show 需求 5 年內維持雙位數成長，Concerts AOI 累積至 ~.5B（5Y CAGR +18%）。","columns":{"2Y 驗證點（至 2028）":"FY 2027-2028 Concerts attendance ≥ 175M（vs 2025 159M），AOI ≥ 0M（vs 2025 7M）。","5Y 驗證點（至 2031）":"FY 2031 Concerts attendance ≥ 220M，AOI ≥ B（margin 升至 4.5%）。","10Y 驗證點（至 2036）":"FY 2036 Concerts revenue ≥ B（vs 2025 B），全球 Stadium tier penetration 30%+。","驗證指標":"(1) 年度 fan attendance；(2) Concerts AOI margin（門檻 ≥ 3.5%）；(3) 大型 show pipeline YoY"}},{"id":"H3","text":"Sponsorship + Ticketing 高毛利雙引擎延續：Sponsorship AOI 5 年 CAGR ≥ +12%、Ticketing AOI 即使受 fee cap 影響仍 ≥ +5% 年成長。","columns":{"2Y 驗證點（至 2028）":"FY 2027 Sponsorship AOI ≥ B（vs 2025 5M），Ticketing AOI ≥ .15B。","5Y 驗證點（至 2031）":"FY 2031 Sponsorship AOI ≥ .5B，Ticketing AOI ≥ .3B（已吸收 fee cap 衝擊）。","10Y 驗證點（至 2036）":"FY 2036 高毛利兩段合計 AOI 占集團 75%+。","驗證指標":"(1) Sponsorship YoY；(2) Ticketing 138M fee-bearing tix 是否續成長；(3) take rate after fee cap"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Judge Subramanian remedy 強制結構性分拆（拆分 Ticketmaster / Concerts，或剝離 venue 業務）","columns":{"對應假設":"H1","時間尺度":"🐢 中期（18-24 個月，2027-2028 期）","監測指標":"(1) Subramanian 公開裁決，(2) DOJ 補充 motion，(3) 26 states+DC 立場","警戒閾值":"若 remedy 包含「強制業務分拆」或「強制資產出售」中任一 → R1 觸發 → 立即減倉 2/3"}},{"id":"R2","text":"Concerts artist take rate 失控（大牌 artist 拿走 95%+ 收入，Concerts AOI margin 跌穿 2.5%）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（4-8 季）","監測指標":"(1) 季度 Concerts AOI margin；(2) 大型 show（Stadium tour）占比變化；(3) 法律 fees 是否擠壓 margin","警戒閾值":"連 2 季 Concerts AOI margin &lt; 2.5% → R2 觸發 → 重評 H2"}},{"id":"R3","text":"估值倍數均值回歸（市場開始用 30-40x PE 而非 78x 定價 LYV，無外部催化也能下行 -40%）","columns":{"對應假設":"H1/H3","時間尺度":"🔥 中短期（6-18 個月）","監測指標":"(1) 5Y NTM PE 分位；(2) 同業 EV/EBITDA 趨勢；(3) CTS Eventim relative valuation","警戒閾值":"5Y NTM PE 分位 &gt; 90% 持續 4 週 或 同業 PE 收斂 +20% → R3 已實現"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":168.87,"archetype":null,"cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名中除程式欄以外的每一個**（程式稍後才會算的 p_bull_pct／p_bear_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；`asym_ratio`／`ev5y_pct`／`irr_base_pct`／`bull_5y_price`／`bear_5y_price` 的漂移歸因同樣由程式生成條目（程式用本次情境、依先換情境後換股價的順序拆量），你不要為它們開條目；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

**給讀者看的文字欄不准出現內部代號**：`thesis.H[]`／`thesis.R[]` 的各欄（信息來源／漂移觸發條件等）、`triggers[].text`、`counter_evidence.contradictions[]` 各欄、`answers.*.verdict`／`answers.*.reasoning` 這類文字，一律不得出現事實表 id（`f_` 開頭，如 `f_consensus_rev_3m_fy1_pct`）或軸／finding id（`軸名#n`，如 `competitive_share_entrants#0`）——這些是程式內部代號，不是給讀者的話。要引用哪個事實或哪個軸，寫進對應的 `fact_refs[]`／`evidence_refs[]` 陣列，文字欄本身只寫人話。

---

## 尾段：scenario_inputs 形狀與回覆格式

**本檔 FY1 共識 EPS ≤ 0（虧損），程式已把估值口徑定為 `sales_multiple`：情境樹用營收路徑 × 終端 EV/S，不用 EPS × 本益比。** 口徑由程式決定，你填什麼 `valuation_basis` 都會被覆寫。`scenario_inputs` 的鍵名與形狀必須完全照下面這份（不得增刪改名；程式據此產生 `dd_scenario.py` 的輸入檔，寫錯鍵名就是整段判斷失效）：

```json
{
  "valuation_basis": "sales_multiple",
  "terminal_label": "FY20XXE",
  "start": {"rev": <FY+1 共識營收，百萬，報告幣別；抄事實表 f_rev_consensus_fy1_m>, "ev_s": <目前 EV/S（EV÷FY+1 共識營收）；抄事實表 f_ev_s_fwd>, "basis": "<起點口徑一句話：營收取哪一年、EV/S 的分母是哪一年，須與終端 EV/S 分母同口徑>"},
  "rev": {"bull": [<Y1>, <Y2>, <Y3>, <Y4>, <Y5>], "base": [五個數], "bear": [五個數]},
  "ev_s": {"bull": <終端 EV/S>, "base": <倍數>, "bear": <倍數>},
  "net_debt_y5": {"bull": <終端年淨負債，百萬，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "shares_y5": {"bull": <終端年稀釋股數，百萬股，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "p": {"bull": <機率整數>, "base": <整數>, "bear": <整數>},
  "yield_pct": {"dividend": <股息殖利率 %>, "net_buyback": <淨回購殖利率 %>},
  "max_dd": {"lo": <負數 %>, "hi": <負數 %>, "basis": "<範圍怎麼推出來的，見判斷卡③情境樹假設段>", "trigger_time": null},
  "basis": {"bull": "<這支路徑的假設一句>", "base": "…", "bear": "…"},
  "endo_ceiling_exceeded": <true|false，共識 CAGR 是否超過 §5.R 內生天花板>
}
```

（**不要**填 `eps`、`pe`、`second_stage`、`peer_max_fpe`；`eps_meta` 仍照常寫共識三年 EPS。現價、目前淨負債（`f_net_debt_m`）、目前股數（`f_shares_diluted_m`）由程式從事實表帶進 `scenario.json`。）

**終端每股價＝max(0, (終端營收 × 終端 EV/S − 終端淨負債) ÷ 終端股數)**，股權價值為負就是 0（Bear 情境債務吃光股權時，要如實寫出讓它歸零，不要為了好看調高倍數）。`net_debt_y5` 要反映該情境下的現金流與融資（虧損公司的淨負債通常會變大，不是沿用目前值）；`shares_y5` 要反映該情境下的增資與稀釋；兩者填 null 才是沿用目前值，不是預設答案。`ev_s` 是終端年 EV ÷ 終端年營收，須與 `start.ev_s` 同口徑（前瞻 vs trailing 不可混）。

`dd_scenario.py` 會擋：`rev` 各路徑長度 ≠ 5、終端營收非 Bear＜Base＜Bull、三機率加總 ≠ 100、`p.bear` ＜ 20、`endo_ceiling_exceeded=true` 且 `p.bear` ＜ 30、`p.base` ＞ 50。另有機械閘：Bull 前兩年營收不得與 Base 相同（情境退化）、`|max_dd.lo|` 不得小於任一情境終點跌幅。機率與路徑是你的判斷，算術（IRR／倍數貢獻／AR）全由腳本算，不要自己填結果欄。

**回覆全文即 `judgment.json` 內容**：緊湊 JSON（`json.dumps(obj, separators=(",", ":"))` 等效格式），陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）。不寫 `scenario.json`（程式從 `scenario_inputs` 產生）。不填不歸你的欄（`decision_inputs` 的機械欄、`reasoning`／`plain` 頂層、`moat.spread_table`／`competitors`、`contradictions`／`triggers` 等舊形狀頂層欄）——填了機械閘會擋。`decision_inputs.asym_ratio`／`irr_base_pct`／`ev5y_pct` 一律填 `null`，由腳本從 scenario 機械算回。

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
