你是 stock-analyst **v20 判斷 agent**，標的 NVMI（20261012）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
  *eps
    *bull[]: arr ≥1 num
    *base[]: arr ≥1 num
    *bear[]: arr ≥1 num
  *pe
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
{"meta":{"ticker":"NVMI","date":"2026-10-12","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261012/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261012/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":254.96,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）"},"note":"未取得共識對照"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income","value":85.25,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）"},"note":"未取得共識對照"},{"id":"f_kpi2_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":33,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）"},"note":"未取得共識對照"},{"id":"f_kpi3_gaap_operating_income","label":"GAAP operating income","value":76.19,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）"},"note":"未取得共識對照"},{"id":"f_kpi4_gaap_operating_margin","label":"GAAP operating margin","value":30,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）"},"note":"未取得共識對照"},{"id":"f_kpi7_guidance_q3_2026","label":"Guidance Q3 2026 營收","value":"277～287","period":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）"},"note":"未取得共識對照"},{"id":"f_kpi8_guidance_q3_2026_non_gaa","label":"Guidance Q3 2026 non-GAAP diluted EPS","value":"2.7～2.85","period":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）"},"note":"未取得共識對照"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-06","period":"2026-08-06","unit":"date","basis":"距今 47 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-06"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_nvmi_gross_margin_pct","label":"NVMI 毛利率","value":57.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVMI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvmi_operating_margin_pct","label":"NVMI 營業利益率","value":28.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVMI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvmi_fcf_margin_pct","label":"NVMI FCF 利潤率","value":20.24,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVMI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_klac_gross_margin_pct","label":"KLAC 毛利率","value":61.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_klac_operating_margin_pct","label":"KLAC 營業利益率","value":41.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_klac_fcf_margin_pct","label":"KLAC FCF 利潤率","value":27.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_onto_gross_margin_pct","label":"ONTO 毛利率","value":50.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_onto_operating_margin_pct","label":"ONTO 營業利益率","value":13.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_onto_fcf_margin_pct","label":"ONTO FCF 利潤率","value":22.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_camt_gross_margin_pct","label":"CAMT 毛利率","value":50.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAMT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_camt_operating_margin_pct","label":"CAMT 營業利益率","value":23.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAMT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_free_cash_flow_40_92_cap","label":"Free cash flow（推算＝營運現金流 40.92 − capex 2.49；公司未揭露 FCF）","value":38.42,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）；FCF 為依新聞稿現金流量表推算"},"note":"未取得共識對照"},{"id":"f_kpi6_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":8.9,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）"},"note":"未取得共識對照"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":353.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-28.84,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":40.13,"period":"2026-10-09（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.67 → 10.67）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.66 → 13.66）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.59 → 16.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":10.67,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":13.66,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":16.59,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.72,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 10.49 → 10.67（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":44.12,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":11.98,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝88.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":88.1,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":11.74,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝78.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":78.2,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":33.08,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 10.67，分子＝快照價 353.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"管理層引述 Gartner 最新報告：Nova 在薄膜、SIMS 與關鍵尺寸量測再增約 400bp 份額，連續第二年顯著成長，為該細分市場第二大供應商（子市場數字，非整體份額；為管理層轉述）。","source":"Nasdaq: Nova Q1 earnings call highlights","url":"https://www.nasdaq.com/articles/nova-q1-earnings-call-highlights","excerpt":"Waisman highlighted a recent Gartner market share report showing Nova gained an additional 400 basis points of share in film SIMS and critical dimension metrology, marking the second consecutive year of significant share growth. He said the gains strengthened Nova's position as the second-largest vendor in that market.","as_of":"2026-05-14","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Onto Innovation FY2025 10-K 將 KLA 與 Nova 列為薄膜與 OCD 量測的主要競爭對手；Nova 為其整合式量測的主要對手（as_of 為 10-K 提交時間，約略值）。","source":"Onto Innovation Form 10-K (FY ended 2026-01-03)","url":"https://www.sec.gov/Archives/edgar/data/704532/000119312526066937/onto-20260103.htm","excerpt":"KLA Corporation and Nova Ltd. are its principal competitors for thin film and critical dimension OCD metrology.","as_of":"2026-02-25","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"第三方估計 Nova 在製程控制約 18% 份額、KLA 為領導者；該數字無法交叉驗證（getquin 貼文）。","source":"getquin post KPnxoSUSpw","url":"https://app.getquin.com/de/post/KPnxoSUSpw","excerpt":"Nova is positioning itself as a key challenger with an estimated 18 percent market share in the process control segment.","as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2025 20-F 客戶表（搜尋摘要轉述）：Customer B 占 2025 營收 10%、2024 為 14%；Customer A 2024 為 18%，2025 的 Customer A 數字未取得。客戶未具名。","source":"Nova Ltd Form 20-F FY2025 (SEC EDGAR, via search summary)","url":"https://www.sec.gov/Archives/edgar/data/0001109345/000117891326000504/zk2634307.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"20-F 風險因素指向 Note 16 揭露主要客戶占營收比重；WebFetch 只讀到前 100000 字，未讀到 Note 16 數值，故最大客戶 2025 占比與前五大合計未驗證。","source":"Nova Ltd Form 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/0001109345/000117891326000504/zk2634307.htm","excerpt":"For more information regarding our sales by major customers as percentage of our total sales, see Note 16","as_of":"2025-12-31","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"歷史趨勢（搜尋摘要轉述）：Customer A 2021 31%、2022 23%、2023 19%；Customer B 2021 21%、2022 12%、2023 18%，集中度呈下降趨勢。","source":"Nova Ltd 20-F financial reports FY2021-FY2023 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1109345/000117891324000649/Financial_Report.xlsx","excerpt":null,"as_of":"2023-12-31","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"客戶信用：搜尋僅得 Intel（客戶身分推測未經 Nova 確認，客戶未具名）2025 年遭 Fitch 降至 BBB 負向展望、S&P 降至 BBB；未找到 2026 年評等動作。Nova 客戶實際身分未於本軸證實。","source":"Fitch/S&P Intel downgrade coverage (bondblox, tweaktown)","url":"https://bondblox.com/news/intel-downgraded-to-bbb-by-fitch","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Citi 2026 TMT 會議摘要：2026 WFE 共識成長 >20%（AI 驅動），部分分析師至 38%；DRAM 的量測強度低於邏輯，故 Nova 2026 對 WFE 超額表現較少；預期 2027 因 2nm／GAA 轉換量測強度上升；新五年計畫將於 2027 初 Investor Day 公布。","source":"Quartr — Nova (NVMI) Citi's 2026 Global TMT Conference summary","url":"https://quartr.com/events/nova-ltd-nvmi-citi-s-2026-global-tmt-conference_FG2AxEM9","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Nova Q2 2026 營收 $255M（年增 16%），Q3 指引 $277–287M；先進邏輯（GAA）與先進封裝創紀錄，先進封裝占營收約 25%，中國約 30%、預期長期穩定在 25–30%。","source":"Nasdaq／搜尋摘要 — Nova Q1 earnings call highlights 及相關法說摘要","url":"https://www.nasdaq.com/articles/nova-q1-earnings-call-highlights","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261012","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 中期 2026 預測（二手報導）：WFE 2026 為 $143.9B（+23.1%），2027 +21.8%，2028 +14.1%，約 $200B；為相對年底預測的大幅上修。","source":"iconnect007 — Global Semiconductor Equipment Sales Forecast to Reach a Record $229 Billion in 2028","url":"https://iconnect007.com/article/150797/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-in-2028/150794/ein","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Yole：量測與檢測設備市場 2025 年成長 15% 至逾 $180 億，約占 WFE 14%；成長兼具週期復甦與先進架構、AI、先進封裝帶來的製程控制強度結構性提升。","source":"Yole Group press release — 15% in 2025: metrology & inspection accelerate semiconductor innovation","url":"https://www.yolegroup.com/press-release/15-in-2025-metrology-inspection-accelerate-semiconductor-innovation/","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"風險面：分析師指出若先進封裝投資放緩，WMC／Prism 等工具可能利用率不足；另有先進節點大客戶撤單的集中度風險；NAND 仍處長期下行。","source":"Quartr — Nova Citi 2026 TMT summary／搜尋摘要","url":"https://quartr.com/events/nova-ltd-nvmi-citi-s-2026-global-tmt-conference_FG2AxEM9","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Nova FY2025 20-F 風險因素：貿易限制、關稅變動與進出口許可可能使受影響國家的銷售大幅減少；主要客戶位於台灣、日本、南韓、中國與美國。","source":"NOVA LTD. Form 20-F FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001109345/000117891326000504/zk2634307.htm","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國占 Nova 營收約 35%（2025 上半年），2024 年為 39%；管理層預期中國占比下降。來源為第三方 PESTLE 分析（2026-04 更新），非公司文件。","source":"dcf-analysis.com Nova Ltd. (NVMI) PESTLE Analysis [Apr-2026 Updated]","url":"https://dcf-analysis.com/products/nvmi-pestel-analysis","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Q3 2025 電話會議上 CFO 稱中國限制尚無顯著影響，毛利變化主要來自產品組合（第三方轉述）；Q1 2025 指引為關稅壓低毛利率 30–50bps（Fintool 摘要）。","source":"Fintool / PESTLE 摘要 (NVMI Q1 2025, Q3 2025 call)","url":"https://fintool.com/app/research/companies/NVMI/earnings/Q1 2025","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261012","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國 Section 232 公告自 2026-01-15 生效，對特定先進運算晶片課 25% 關稅並附終端用途豁免；公告涵蓋範圍提及半導體製造設備及衍生品，但搜尋結果未見設備本身的具體稅率，也未見 Nova 被點名。","source":"Thomson Reuters / EY / White & Case 摘要 Section 232 semiconductors","url":"https://taxnews.ey.com/news/2026-0209-us-section-232-proclamation-imposes-25-percent-tariff-on-certain-semiconductors","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Section 122 全球替代關稅 10%、後升至 15%，自 2026-02-24 生效，可能波及半導體供應鏈（出自 SEALSQ 424B5，非 Nova 專屬）。","source":"SEALSQ Corp Form 424B5 FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1951222/000110465926029206/tm268871-1_424b5.htm","excerpt":null,"as_of":"2026-02-24","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Nova 2025 20-F 摘要列出營運集中於以色列、美國、德國的製造設施，並提及對中國晶片廠銷售受出口管制與關稅影響。","source":"StockTitan, Nova Ltd 20-F annual report summary","url":"https://www.stocktitan.net/sec-filings/NVMI/20-f-nova-ltd-files-annual-report-foreign-issuer-a6f4cb93a5ef.html","excerpt":"operational concentration in manufacturing facilities in Israel, the U.S. and Germany","as_of":"2026-03-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Nova 2026年8月（Q2 2026）投資人簡報風險項列有依賴有限數量供應商，以及每條產品線依賴單一製造設施；FY2024 20-F 亦稱對有限供應商、部分情況為唯一供應商。","source":"Nova investor presentation Q2 2026 / Nova 20-F FY2024 (SEC)","url":"https://www.novami.com/wp-content/uploads/2026/08/nova-investor-presenation-q22026.pdf","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國占 Nova 營收：2024年約39%（分析師於法說會提問）；第三方稱2025上半年約35%，預期占比下降但名目仍小幅成長（二手來源）。","source":"fintool.com NVMI research; dcf-model.com PESTLE","url":"https://fintool.com/app/research/companies/NVMI","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261012","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Nova Q1 2026 前瞻聲明列示外國政治經濟風險，含供應鏈困難及可能限制營運的制裁與出口限制。","source":"Nova Q1 2026 call date PDF / VCP Scanner NVMI","url":"https://www.novami.com/wp-content/uploads/2026/04/nova-q1-2026-call-date.pdf","excerpt":"foreign political and economic risks including supply-chain difficulties","as_of":"2026-04-01","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 營收 $255.0M，季增 8%、年增 16%；先進邏輯（GAA 轉換）與先進封裝（邏輯／記憶體擴產）皆創單季紀錄。","source":"Nova Reports Record Second Quarter 2026 Financial Results (2026-08-06)","url":"https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html","excerpt":"Revenue hit $255.0 million, up 8% from the first quarter of 2026 and 16% higher than the second quarter of 2025.","as_of":"2026-08-06","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q2 2026 產品營收 $201.5M、服務營收 $53.5M；產品中邏輯／晶圓代工 73%、記憶體及其他 27%。","source":"Nova Q2 2026 results (2026-08-06), 搜尋彙整","url":"https://www.sec.gov/Archives/edgar/data/0001109345/000117891326003892/zk2635873.htm","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261012","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Q2 2026 毛利率 56.5%，低於 Q1 2026 的 57.7% 與 Q2 2025 的 57.8%。","source":"Nova Q2 2026 results (2026-08-06), 搜尋彙整","url":"https://www.barchart.com/story/news/3688856/nova-reports-record-second-quarter-2026-financial-results","excerpt":"Gross margin in the second quarter of 2026 was 56.5%, compared with 57.7%, in the first quarter of 2026 and 57.8% in the second quarter of 2025.","as_of":"2026-08-06","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收指引 $277M–$287M，中點約高於分析師預期 1.8%。","source":"Nova Q2 2026 results / Barchart (2026-08)","url":"https://www.barchart.com/story/news/3693558/novas-nasdaqnvmi-q2-sales-top-estimates-inventory-levels-improve","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261012","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"先進封裝約占 2025 產品營收 20%、年增逾 60%；Citi 研討會摘要（2026 年 9 月）稱現占營收約 25%；混合鍵合為未來機會，目前以認證為主。","source":"Quartr: Nova Citi 2026 Global TMT Conference summary / Q2 2026 summary","url":"https://quartr.com/events/nova-ltd-nvmi-citi-s-2026-global-tmt-conference_FG2AxEM9","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"管理層稱 GAA 業務於 2026 年貢獻顯著營收，涵蓋主要客戶；ELIPSON 平台被一家頂級晶圓代工廠選為 tool of record。","source":"Nova Q1/Q2 2026 earnings call highlights (搜尋彙整)","url":"https://www.nasdaq.com/articles/nova-q1-earnings-call-highlights","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"0","claim":"Citi 摘要預期 2027 年隨 2nm／GAA 轉換量測密度提高，但警示 2026 年因投資組合與較低量測密度，相對 WFE 的超額表現較少。","source":"Quartr: Nova Citi 2026 Global TMT Conference summary","url":"https://quartr.com/events/nova-ltd-nvmi-citi-s-2026-global-tmt-conference_FG2AxEM9","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261012","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"0","claim":"市占：單一聚合貼文估 Nova 約占製程控制 18%、KLA 約 55%（無方法論）；Walnut Invest（2026 年 7 月更新）稱 Nova 為光學 CD 量測第二名，管理層自稱 CD 量測市占增約 400bp（公司自述）。","source":"getquin 貼文；Walnut Invest NVMI buy/sell 頁","url":"https://walnutinvest.com/stocks/nvmi/is-it-a-buy-or-sell","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"+","claim":"Yole 2026 Q2 更新：2026 WFE 預測上修至約 $162B，2031 前 CAGR 約 9%；AI 投資拉動含量測與檢測在內的設備需求，未來兩年預期續為成長年。","source":"Yole Group WFE Market Monitor / Metrology & Inspection Equipment 2026","url":"https://www.yolegroup.com/product/report/metrology--inspection-equipment-2026/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#9","axis":"end_markets","section":"coverage","direction":"0","claim":"半導體製程控制設備 TAM：GMI 估 2025 年 $12.6B、2026 年 $13.5B（CAGR 8.1%）；TBRC 估 2025 年 $8.29B→2026 年 $8.82B（CAGR 6.4%）；定義不同不可直接比較。","source":"Global Market Insights (2026-04); The Business Research Company via GII Korea","url":"https://www.gminsights.com/industry-analysis/semiconductor-process-control-equipment-market","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Onto Innovation（Nova 同業）2026-04 宣布與 Rigaku 合作，把 OCD 與 X-ray 結合；X-ray 被定位為 OCD 的互補而非取代。","source":"Silicon Saxony 轉載 Onto Innovation 新聞稿：Onto Innovation announces strategic partnership with Rigaku","url":"https://silicon-saxony.de/en/onto-innovation-onto-innovation-announces-strategic-partnership-with-leading-x-ray-provider-rigaku-to-advance-next-generation-process-control-solutions/","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Onto 的 Atlas G6 OCD 系統（2025-09 發表）瞄準第二代 GAA 邏輯與 HBM 用垂直閘 DRAM，已取得多家邏輯與記憶體廠量產訂單；光學量測仍是主流路線，同業在同一賽道推新平台。","source":"Business Wire：Onto Innovation Launches Next Generation OCD Metrology Platform to Enable Process Control for Advanced AI Devices","url":"https://www.businesswire.com/news/home/20250909090035/en/Onto-Innovation-Launches-Next-Generation-OCD-Metrology-Platform-to-Enable-Process-Control-for-Advanced-AI-Devices/","excerpt":null,"as_of":"2025-09-09","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Yole 報告：2025 年量測與檢測設備市場成長 15%、超過 180 億美元，製程控制正擴展到軟體、分析、整合方案與混合量測。","source":"Yole Group press release：15% in 2025, metrology & inspection accelerate semiconductor innovation","url":"https://www.yolegroup.com/press-release/15-in-2025-metrology-inspection-accelerate-semiconductor-innovation/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"聚合站風險清單籠統列出技術過時風險，未指明 Nova 哪項產品受威脅；搜尋未找到 2026–2027 年有具體替代技術取代 OCD/X-ray 的證據。","source":"explore.nemo.money NVMI 頁","url":"https://explore.nemo.money/en/stocks/NVMI","excerpt":"Investors should note concentration risks, technology obsolescence and geopolitical or supply-chain disruptions can affect results.","as_of":"2026-06-01","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Nova 於 2026-08-06 給 Q3 指引：EPS 2.70–2.85、營收 277–287M，高於當時共識 EPS 2.64、營收 276.7M","source":"MarketBeat - Nova releases Q3 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/nova-nasdaqnvmi-releases-q3-2026-earnings-guidance-2026-08-06/","excerpt":"The company provided earnings per share guidance of 2.700-2.850 for the period, compared to the consensus estimate of 2.640.","as_of":"2026-08-06","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 彙整（2026-08-04）：11 位分析師，8 買 3 持有，平均目標價 556.67，區間 345–640","source":"MarketBeat NVMI price target","url":"https://www.marketbeat.com/stocks/NASDAQ/NVMI/price-target/","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Benzinga 2026-09-03 快照：10 位分析師平均目標價約 491，高 640、低 240（Jefferies）；Citigroup 8/10 由 595 降至 550，Needham 8/7 由 640 降至 570","source":"Benzinga NVMI sentiment page","url":"https://kr.benzinga.com/quote/NVMI/sentiment","excerpt":null,"as_of":"2026-09-03","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 共識表：Q3'26E EPS 2.74／營收 282.2M，Q4'26E EPS 3.01／營收 305.4M；不同頁面數字互相衝突，且有 17 次指引更新中 12 升 2 降的紀錄","source":"Benzinga NVMI earnings forecasts","url":"https://jp.benzinga.com/quote/NVMI/earnings-forecasts","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#none","axis":"major_events","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"NVMI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.12,"operating_margin_pct":28.97,"fcf_margin_pct":20.24,"rd_intensity_pct":16.11},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVMI","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"KLAC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":61.3,"operating_margin_pct":41.69,"fcf_margin_pct":27.74,"rd_intensity_pct":11.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ONTO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.36,"operating_margin_pct":13.81,"fcf_margin_pct":22.54,"rd_intensity_pct":12.73},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"CAMT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.05,"operating_margin_pct":23.19,"fcf_margin_pct":null,"rd_intensity_pct":11.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAMT","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"NVMI"},"financial_history":{"ticker":"NVMI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":570729000.0,"revenue_yoy_pct":null,"gross_margin_pct":55.54,"operating_margin_pct":26.27,"net_income":140213000.0,"diluted_eps":4.4,"free_cash_flow":98225000.0,"fcf_margin_pct":17.21,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":517922000.0,"revenue_yoy_pct":-9.25,"gross_margin_pct":56.61,"operating_margin_pct":25.54,"net_income":136310000.0,"diluted_eps":4.28,"free_cash_flow":106343000.0,"fcf_margin_pct":20.53,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":672396000.0,"revenue_yoy_pct":29.83,"gross_margin_pct":57.57,"operating_margin_pct":27.89,"net_income":183762000.0,"diluted_eps":5.75,"free_cash_flow":218051000.0,"fcf_margin_pct":32.43,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":880577000.0,"revenue_yoy_pct":30.96,"gross_margin_pct":57.37,"operating_margin_pct":28.78,"net_income":259223000.0,"diluted_eps":7.96,"free_cash_flow":217915000.0,"fcf_margin_pct":24.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/NVMI/NVMI_Q2_2026_Earnings_Call_20260806.md）

# Q2 2026 Earnings Call
2026-08-06

Q2 2026 Earnings Call
Nova Ltd. | Earnings Calls | 2026-08-06
Operator (Operator)
Good day, and welcome to the Nova Ltd. Second Quarter 2026 Results Conference Call. [Operator
Instructions] Please note today's event is being recorded. I would now like to turn the conference over
to Ms. Miri Segal, CEO of MS-IR. Please go ahead.
Miri Segal-Scharia (Attendees)
Thank you, operator, and good day, everyone. I would like to welcome all of you to Nova's Second
Quarter 2026 Financial Results Conference Call. With us on the line today are Gaby Waisman,
President and CEO; and Guy Kizner, CFO. Before we begin, I would like to remind our listeners that
certain information provided on this call may contain forward-looking statements and the safe harbor
statement outlined in today's earnings release also pertains to this call. If you have not received a copy
of the release, please view it in the Investor Relations section of the company's website. Gaby will begin
the call with a business update, followed by Guy with an overview of the financials. We will then open
the call for the question-and-answer session.
I will now turn the call over to Gaby Waisman, Nova’s President and CEO. Gaby, please go ahead.
Gabriel Waisman (Executives)
Thank you, Miri, and thank you all for joining us today. I will start the call by summarizing our second
quarter performance highlights. Following my commentary, Guy will review the quarterly financial
results in detail. We delivered an exceptional quarter, achieving record revenue of $255 million at the
top end of our guidance and record profitability. This performance marks a significant milestone for
Nova with quarterly revenue surpassing $250 million and non-GAAP earnings per share exceeding
$2.50, demonstrating the scale and earning power envisioned in our long-term strategic plan. Looking
ahead, we expect to deliver another year of double-digit growth, supported by sustained customer
investment, broader adoption of our solution and continued market share gains. We are now working
on the next phase of our long-term growth strategic planning, and we will share more about this in our
upcoming Investor Day during the first quarter of 2027.
Our results reflect strong execution amid a favorable industry backdrop, characterized by accelerating
technology transitions and capacity investments. Demand was broad-based across our portfolio,
driving record sales in multiple product lines and services, led by advanced logic and advanced
packaging applications. With enhanced visibility and a robust pipeline of opportunities, we are well
positioned to extend this momentum and deliver another year of profitable growth. We continue to see
strong AI-driven demand across the semiconductor industry, supported by ongoing investments in
infrastructure and the emergence of agentic AI. The need for related leading -edge silicon, including
CPUs, memory and storage is robust, supporting continued investments in manufacturing capacity and
the process control solutions required to enable it. Sustained investment in innovation remains central
to our strategy.

We invest approximately 15% of revenue in research and development to ensure that our technology
road map remains aligned with the industry's most advanced manufacturing challenges. As device
architecture becomes more complex and customers pursue new approaches in advanced logic, memory
and packaging, the need for new metrology capabilities, higher levels of automation and greater
software intelligence continue to increase. Recent product introductions demonstrate the breadth of
our innovation. These include a new generation of Prism targeted for advanced memory structures, a
new generation of VeraFlex for materials metrology and a new configuration of Nova WMC that
extends our dimensional metrology capabilities to panel-level packaging.
In software, we introduced Nova Hub, a scalable platform for fleet and AI-driven analytics that enable
advanced applications and supports the efficient operation of large metrology fleets. Together, these
solutions and additional technological innovations still in the pipeline expand our serviceable market
while enabling customers to achieve higher performance, greater productivity and address critical
applications across future technology generations.
Now let me turn to some business highlights for this quarter. Revenue associated with advanced logic
more than doubled sequentially as customers expanded production capacity. Demand stretched across
product lines and divisions reflecting the range of process control solutions required in leading-edge
logic manufacturing. This quarter, 2 areas in particular, benefited from advanced logic. In materials
metrology, the VeraFlex XPS platform continued to gain traction, driven by proliferation in gate-all-
around manufacturers as customers continue to increase the number of VeraFlex tools per fab. This
traction was one of the factors driving our recent clean room expansion in California, which doubles
our manufacturing capacity in the U.S.
Another highlight was the increasing need for more powerful capabilities in our dimensional metrology
platforms to further increase performance while reducing time to solution. Our AI-enabling modeling
solution, which combines physics-based and machine learning algorithms help customers address
multiple challenges associated with complex 3D device structures. These capabilities play an
increasingly important role in managing the expanding Nova's installed base in gate-all-around
manufacturing. Another highlight was the record sales of our front-end chemical metrology solution,
Nova ancosys, supported by both advanced memory and mature logic applications, reflecting
increasing adoption, deeper engagement with existing customers and continued market share gains at
the front end of the line.
Ancosys strong performance demonstrates its growing role as an important revenue driver and further
reinforces our leadership in chemical metrology. Advanced packaging was another area of strength
during this quarter with record sales contributing nearly 1/4 of our overall product revenue, driven by
our dimensional metrology portfolio. This performance was fueled by our customers' continued
investment in advanced packaging and high-bandwidth memory capacity to support growing demand
for AI-related devices.
An important growth driver was the Nova WMC platform, which continued to gain traction across
advanced packaging applications, including a recent tool of record selection by a leading foundry
customer for multiple layers measurement in advanced packaging production flows. We also saw
accelerating adoption of the Nova WMC across memory and foundry customers, positioning us to
benefit from further investments in advanced packaging and high-bandwidth memory manufacturing.
Service revenue reached another record level in the quarter, augmented by value-added services. This

included customer investments in upgrading existing tools to address new process requirements such
as tool upgrades, coupled with enhancements to our chemical metrology fleet.
These enable customers to address new applications, materials and chemistry. The strength and
breadth of demand we see across our end markets provide us with increased visibility into the
remainder of the year and into 2027. Customer road maps and planned capacity investments continue
to support a favorable outlook. Importantly, the drivers behind this demand appear increasingly
durable in nature. Given these trends, we believe we are on a path to reaching our organic growth
objectives sooner than originally planned, reinforcing our confidence in Nova's long-term growth.
Now for some more details on our financials, let me hand over the call to Guy.
Guy Kizner (Executives)
Thanks, Gaby. Good day, everyone. I will begin by reviewing our quarter financial achievements and
then provide guidance for the third quarter. Total revenues in the second quarter of 2026 reached a
record level of $255 million, at the high end of our guidance. This performance reflects growth of 8%
quarter-over-quarter and 16% year-over-year, driven by continued strength across our customer base
and solid demand for our differentiated process control solutions.
Product revenue distribution was approximately 73% from logic and foundry and 27% from memory
and others. Product revenues included two customers and four territories, which contributed each 10%
or more to product revenues. In the second quarter, blended gross margins were 57% on a GAAP basis
and 58% on a non-GAAP basis. Gross margins remained healthy and supported our record revenue and
strong profitability performance. As expected, operating expenses increased to $68 million on a GAAP
basis and $62.9 million on a non-GAAP basis. This increase reflects our disciplined approach to
reinvesting growth into product development and road map expansion, positioning the company for
continued long-term success.
Operating margins in the second quarter reached 30% on a GAAP basis and 33% on a non-GAAP basis,
on the upper range of our target model of 28% to 33%. This excellent result was driven by the revenue
growth and the company robust operational model. The effective tax rate in the second quarter was
approximately 16%. Earnings per share in the second quarter on a GAAP basis were $2.20 per diluted
share, and earnings per share on a non-GAAP basis were $2.51 per diluted share, exceeding the high
end of our second quarter guidance.
Next, I would like to outline our guidance for the third quarter of 2026. We currently expect revenues
for the quarter to be between $277 million and $287 million. GAAP earnings per diluted share to range
from $2.46 to $2.61. Non-GAAP earnings per diluted share to range from $2.70 to $2.85. At the
midpoint of our third quarter 2026 estimates, we anticipate the following: gross margins of
approximately 57% on a GAAP basis and approximately 59% on a non-GAAP basis. Operating expenses
on a GAAP basis to increase to approximately $74 million. Operating expenses on a non-GAAP basis to
increase to approximately $68 million; financial income on a non-GAAP basis to remain similar to that
of the second quarter.
Effective tax rate is expected to be approximately 17%, looking back at the first half of 2026, we are
pleased with the strong momentum across the business. We achieved record revenues, delivered
operating margins at the upper end of our target model and generated earnings above the high end of
our guidance. These results highlight both the demand of our solutions and the leverage inherent in our

operating model. Our financial position remains strong with more than $1.7 billion in cash and
investments, providing substantial flexibility to continue investing in R&D, support strategic growth
initiatives and pursue selective M&A opportunities that align with our long-term objectives. Combined
with our positive third quarter outlook, we believe we are well positioned to continue driving profitable
growth throughout 2026.
With that, we will be pleased to take your questions. Operator?
Operator (Operator)
[Operator Instructions] First question is from Tom O'Malley, Barclays
Robert Smith (Analysts)
This is Trip Smith on for Tom O'Malley. Nice results today. I was just a little curious about what's going
on in the split between logic/foundry and memory. Just based on the numbers you guys gave, the 73-27
split, it implies nice sequential growth for logic/foundry, but a step down in memory, down 14%
quarter-over-quarter. I was just wondering what the puts and takes were there.
Gabriel Waisman (Executives)
Thank you, Trip, for the question, and thank you for the kind comments. We are projecting memory to
be about 30% for us this year. Obviously, the intensity in logic is higher, and our long-term model calls
for about 60-40 in favor of logic. But we do see strong demand from DRAM, somehow muted demand
from 3D NAND still this year, which may change. But we see growth in both logic and memory, whereas
the intensity and growth on the advanced nodes in logic is obviously higher.
Robert Smith (Analysts)
And then just as a quick follow-up. We've heard buy side, sell side talking about potentially 40% growth
next year for WFE. That implies something closer to like $210 billion, $215 billion. I was just
wondering if you could support those levels today or what you might need to do to support those levels.
Gabriel Waisman (Executives)
Sure. So we do have visibility into 2027 where our customers are planning further ahead. And
obviously, we're working closely with them to plot capacity and inventory levels. In some cases, we're
already receiving orders and planning the 2027 deliveries. We did see some pull-ins by the way, that
drove both the first half and are obviously driving the second half of the year.
But obviously, in overall customers are planning further ahead, and we do work closely with them on
their capacity planning. It's too early to say whether 2027 will grow 40%. We do anticipate it to be a
growth year for us. And therefore, we are working to ensure that our supply chain can provide us with
the needed capacity. They are stretched, but we are managing production as well as the supply chain to
ensure that we are meeting the lead times and the increased demand from our customers.
Operator (Operator)
Next question is from Atif Malik, Citi.
Atif Malik (Analysts)

Gaby, you used the word enhanced visibility in your prepared remarks. And I was curious if you can
compare or contrast this cycle, particularly on the DRAM side to any prior memory cycles, maybe
perhaps the NAND cycle in 2001 to 2007, which was a fairly long investment cycle. But any kind of
qualitative commentary you can provide around your customers' behavior? Are they giving -- putting
more down payments or any backlog and RPO that can help us understand how far is your visibility
extending?
Gabriel Waisman (Executives)
Yes. Thank you for the question, Atif. I think that it's not really comparable to the previous cycles
because we are seeing demand from both logic and memory and customers understand that in order to
provide the product in the lead times that suppliers, including Nova are committed to, they should
work closely or closer with us on giving us long-term or longer-term visibility into next year. That didn't
happen in previous cycles, long or short ones. And we are encouraged by that because it does give us
the ability to work with our supply chain and making sure that we have the right planning in terms of
capacity in order to address the needs of next year.
So I would say that comparably, it's an unprecedented cycle in terms of the visibility and also customer
intimacy that allows us to have better planning for both the second half of this year as well as into next
one.
Atif Malik (Analysts)
Great. And a follow-up for Guy. Guy, can you talk about any impact from higher component costs,
particularly memory to your gross margins? And if you can share your philosophy or strategy around
pricing? Are there any knobs for you to take your target gross margin model higher in this environment
of supply constraints?
Guy Kizner (Executives)
Yes. So thank you, Atif. I would say that we do see some impact on the -- on our BOM costs related to
memory. Our proportion of memory portion of our BOM is not significant. So we don't see any major
change to our gross margin profile due to that. So I would say the margin profile and the margin range,
the gross margin range that we have in our target model of 57% to 60% is well intact.
Gabriel Waisman (Executives)
Yes. I would add to that, if I understood correctly, also from the ASP side. Obviously, there is a balance
and, let's say, an effort on all sides to ensure that pricing continues to support both the down side and
COGS that Guy mentioned as well as customer expectations -- we are looking at the long term in that
respect and the customers are long-term partners of ours. So we continue to support in the best
possible way while considering the different changes on the BOM and COGS. But overall, as Guy said,
we are maintaining our gross margin model, and we are confident that we will continue to do so
through this year and the next one.
Operator (Operator)
Next question is from Shane Brett, Morgan Stanley.
Shane Brett (Analysts)

So my first question is, if I take your guidance, you're growing products in the low to mid-20s, which is
a bit below WFE this year, but I think that's more so due to process control intensity being quite a bit
lower this year and nothing idiosyncratic. So a bit of a 2-part question. Firstly, what is Nova's view on
process control intensity recovering into 2027?
And my second question is just do we have levers to outgrow process control growth next year?
Gabriel Waisman (Executives)
Thank you very much, Shane. I would say that in terms of process control intensity, we need to break
down the process control into end markets because they behave differently. Logic process control
intensity is higher than memory, while advanced packaging is, of course, rapidly growing. Process is
also tapping on other growth engines such as 3D NAND, which is investing in upgrades, but it's
currently muted in process control. And that, of course, may change in the future.
More importantly, the structural drivers that propel our business are still in place. We have increasing
complexity in architectures and materials that are driving the need for process control. And from our
perspective, the most important indicators are customer adoption, market share gains and technology
wins. And we see continuous strength across these areas and remain confident that those long-term
drivers of Nova's growth and outperformance remain firmly intact.
Shane Brett (Analysts)
Got it. And for my follow-up, you previously published a tech blog focusing on your talks at VLSI 2025
on hybrid bonding and Nova solutions for it. Just can you talk about hybrid bonding is impacting your
SAM? And if there's just an update you can give on your advanced packaging growth for this year as
well, that would be very helpful.
Gabriel Waisman (Executives)
Sure. So we mentioned in the call that advanced packaging is nearing 25% of our product revenue in the
second quarter of the year. And we see advanced packaging evolving from essentially no revenue
several years ago into a meaningful and growing contributor to our business. We view this advanced
packaging as a multiyear structural growth opportunity for Nova and opportunities are now spanning
both optical, chemical and materials metrology. So it's across the board. It's becoming increasingly
similar to front-end manufacturing in terms of complexity, and I'm talking about both logic and
memory, of course, and technologies such as chiplets, hybrid bonding, panel level packaging that I also
mentioned the 2.5D integration are all increasing the number of measurements required as well as the
criticality of those measurements.
So overall, advanced packaging is benefiting our business. We see the hybrid bonding as an additional
layer that will accelerate this growth for Nova. So it's a positive momentum and trajectory for us.
Operator (Operator)
Next question is from Vedvati Shrotre, Evercore.
Vedvati Shrotre (Analysts)
The first one I wanted to understand is you talked about lead times increasing. Could you compare
where the lead times are today versus where they were in the past 3 months and how they have

changed?
Gabriel Waisman (Executives)
Thank you, Vedvati. I mentioned the fact that even though the supply chain is stretched, we are
managing production to ensure that we are improving the lead times as and while the demand from
customers, and we continue to basically provide almost similar lead times. So we make a tremendous
effort to maintain lead times to customers. I think that we are best-in-class in lead times in the
industry. The specific lead times vary from product to product. Overall, I would say that it's been
between 4 to 12 months at the latest depending on the product line.
Vedvati Shrotre (Analysts)
Understood. And for my follow-up question, I know you talked about advanced packaging being 25% of
your product revenues in 2Q. Maybe how do you see the year end up in terms of contribution from
advanced packaging? Do we -- does it stay at the 25% for the whole year in the second half?
Gabriel Waisman (Executives)
I believe it will be -- we projected it initially to be between 20% and 25%. I think inching towards 25%
for the year.
Operator (Operator)
Next question is from Denis Pyatchanin, Needham.
Denis Pyatchanin (Analysts)
So I just wanted to follow up about the end market outlook. So if I understood correctly, you're
expecting memory for you to be down this year. If so, maybe could you talk about what you're maybe
seeing in more detail in DRAM versus NAND in the second half? And perhaps given your visibility, if
you're expecting to see any changes in the memory demand for you entering into first half of '27.
Gabriel Waisman (Executives)
Sure. So first of all, our long-term model is based on a ratio of 60-40, 60 logic/foundry versus 40
memory, and that's because of the higher process control intensity in logic. In 2025, our ratio was 70-
30. And this year's memory share is expected to grow slightly, whereas the majority of our memory
exposure is DRAM. On the metrology side, intensity between DRAM and NAND is more or less similar.
But NAND at this point is a bit muted for us because growth is driven by upgrades rather than capacity
and process control intensity or expansion.
Looking ahead, we believe that the technology transitions such as 4F square, 6F square advanced
DRAM architecture and eventually the 3D DRAM all increase the process complexity and metrology
requirements. Now in terms of positioning, we sell -- if you look at the NAND specifically, which is
relatively muted this year, we sell to all the top players in the NAND market and different -- naturally,
we have different positions, of course, depending on the product line. But once capacity is back, and the
reason I'm saying that is because I'm hoping that capacity is back sometime next year, we are expected
to benefit from it.
Denis Pyatchanin (Analysts)

Excellent. And for a quick follow-up for Guy regarding the gross margin. So it looks like the gross
margin is in with your long-term range, but maybe about 90 basis points below the guidance. Maybe
you can tell us about what drove this unexpected change? Was it mix in the quarter or some sort of
unforeseen costs?
Guy Kizner (Executives)
Yes. So the main reason is product mix. And as we say in every quarter, the estimate that we're giving
can fluctuate plus/minus 1% -- and as I mentioned earlier, this quarter, the gross margins were 58%,
which is a healthy level and well within our target model. And as we discussed previously, gross margin
can fluctuate from quarter-to-quarter depending on product mix.
Looking on the first half of 2026, gross margin was approximately 59%. Our third quarter outlook is
59%, and we expect full year gross margin to be approximately 59%. And overall, it reflects the normal
dynamic of the business.
Operator (Operator)
Next question is from Crawford Clarke, Jefferies.
Crawford Clarke (Analysts)
You've talked about having a position across all 4 of the gate-all-around players. One of those
customers, I know, has joined with the [ Terafab ] project. I was hoping you could help us unpack
maybe without divulging any specific information, how does a greenfield project like [ Terafab ] with a
new fab operator at a leading-edge node compared to a more typical brownfield expansion in terms of
metrology intensity and what your opportunity might look like there?
Gabriel Waisman (Executives)
So I am a bit reluctant to relate to specific customers, as you know. So I will not relate to [ Terafab ]
specifically. Generally speaking, and that's not a comment related to [ Terafab ]. It's a general comment
related to greenfield operation, which happened a couple of years ago, for example, in Rapidus, it
happens in other territories, of course. What we see is the higher metrology intensity as the fab is being
built out as a result of the need to improve time to market and getting to the yield threshold required
for such a new operation.
So the general generic answer I have, which is that we see process control intensity at the initial stages
of greenfield fabs is higher than ongoing operations of more mature ones.
Crawford Clarke (Analysts)
Super helpful. And then just as a follow-up, in the release, I know you guys called out records in the
ancosys front-end chemical metrology business and in Sentronics. I was hoping maybe we could get an
update on where Metrion and Elipson sit on the adoption curve exiting Q2.
Gabriel Waisman (Executives)
Sure. So we did speak of the Metrion accelerated adoption in the first quarter of the year, and we
continue to see demand for Metrion going forward in terms of both the number of customers, both
across logic and memory as well as the utilization and qualifications that we received for this product.
We also indicated the fact that we moved into high-volume manufacturing proliferation, which is true

both for the Metrion and Elipson and the effort that we're investing right now for both those lab-to-fab
concept products is to increase the utilization of the tools, introduce new applications and gain
adoption by more customers so that we will replicate the model that we had with XPS in the past, and
we're currently working on having multiple tools per fab. I also indicated the fact that on the XPS, we
are increasing adoption in logic, the advanced nodes right now. And I think that we are in a positive
trajectory generally with this strategy and in particular, with the Metrion, as I mentioned before.
Operator (Operator)
This concludes our question-and-answer session. I would like to turn the conference back to Mr. Gaby
Waisman, Nova's President and CEO, for any closing remarks.
Gabriel Waisman (Executives)
Thank you, operator, and thank you all for joining our call today.
Operator (Operator)
The conference has now concluded. Thank you for attending today's presentation. You may now
disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NVMI_Q1_2026_Earnings_Call_20260514.md
- 2026-05-14｜CFO｜guidance：CFO 給 Q2 營收指引區間 2.45–2.55 億美元（原話："between $245 million and $255 million."）
- 2026-05-14｜CFO｜guidance：CFO 給 Q2 non-GAAP EPS 指引 2.34–2.48 美元（原話："Non-GAAP earnings per diluted share to range from $2.34 to"）
- 2026-05-14｜CEO｜guidance：CEO 表示客戶排程考量使上半年偏高、下半年預期更高（原話："we expect the second half to run higher"）
- 2026-05-14｜CEO｜guidance：CEO 讀 WFE 今年中十位數成長，高於 2 月看法，預期 Nova 表現優於此數（原話："we expect WFE to reach mid-teens growth"）
- 2026-05-14｜CFO｜margin：CFO 說明 Q1 毛利率與其驅動因素（產品組合與服務成長）（原話："blended gross margins were 57.7% on a GAAP basis"）
- 2026-05-14｜CFO｜margin：CFO 稱 Q1 營業利益率超過目標模型上緣 28%–33%（原話："reached 30% on a GAAP basis and 34% on a non-GAAP basis"）
- 2026-05-14｜CFO｜margin：CFO 答全年毛利率會落在與上半年指引相同的區間、可持續（原話："we see gross margins for 2026 will be within the same rate"）
- 2026-05-14｜CFO｜margin：CFO 解釋 Q2 毛利率指引 59% 較 Q1 低的口徑：指引通常上下 1%（原話："guiding, it's plus/minus 1%. So it's within the same"）
- 2026-05-14｜CFO｜margin：CFO 給 Q2 費用與稅率指引：non-GAAP 營業費用增至約 6,600 萬美元、稅率約 15%（原話："Effective tax rate is expected to be approximately 15%."）
- 2026-05-14｜CEO｜commitment：CEO 重申 2027 年營收 10 億美元的策略目標仍在軌道上，且不提供更遠指引（原話："we are on track, of course, to reach this"）
- 2026-05-14｜CEO｜commitment：CEO 重申 GAA 累計 5 億美元營收目標在軌道上，並稱 2027 年 GAA 投資較今年成長（原話："we're on track for the forecasted $500 million cumulative"）
- 2026-05-14｜CEO｜customer：CEO 稱客戶更早規劃，部分已下單並規劃 2027 年交貨，能見度提高（原話："we do have improved visibility towards next year"）
- 2026-05-14｜CEO｜customer：CEO 稱有拉貨使上半年高於原預期，交貨時點由客戶需求結構決定（原話："We do see some pull-ins, by the way, driving the first half"）
- 2026-05-14｜CFO｜customer：CFO 揭露 Q1 營收組合 Logic/Foundry 約 66%、Memory 約 34%（原話："Revenue mix was approximately 66% from Logic and Foundry"）
- 2026-05-14｜CEO｜customer：CEO 預期今年 Memory 占比較去年更高，由先進 DRAM 投資帶動（原話："I expect Memory to become more dominant this year"）
- 2026-05-14｜CEO｜customer：CEO 稱中國占營收比重預期下降，長期穩定在 25%–30%，今年較上季有正向動能（原話："we expect China to stabilize in the range of 25% to 30%"）
- 2026-05-14｜CEO｜customer：CEO 稱 Nova 獲 Intel EPIC 供應商獎（原話："Nova was awarded the Intel EPIC"）
- 2026-05-14｜CFO｜customer：CFO 稱有 4 家客戶與 5 個地區各占產品營收逾 10%（原話："4 customers and 5 geographic regions, each"）
- 2026-05-14｜CEO｜competition：CEO 引 Gartner 報告稱膜厚與 CD 量測市占再增 400 bp，為第二大供應商（原話："an additional 400 basis points share gain"）
- 2026-05-14｜CEO｜competition：CEO 承認 XPS 與材料量測出現競爭，含中國本土廠商與其他潛在新進者（原話："We are also seeing emerging XPS and material metrology"）
- 2026-05-14｜CEO｜competition：CEO 稱中國市場競爭激烈，Nova 以產品與擁有成本作為差異化（原話："China is also a very competitive market, as you know."）
- 2026-05-14｜CEO｜competition：CEO 稱交期仍短於部分同業（原話："Our lead times are still shorter than some of our peers"）
- 2026-05-14｜CEO｜product：CEO 稱先進封裝已接近產品營收的 20% 中段，多數來自 Logic（原話："advanced packaging for Nova is edging towards the mid-20s"）
- 2026-05-14｜CEO｜product：CEO 稱先進 DRAM 約占 Memory 業務 2/3，Metrion 平台創紀錄（原話："approximately 2/3 of our memory business"）
- 2026-05-14｜CEO｜product：CEO 稱混合鍵合採用速度快於預期，量測密集度高（原話："Adoption is progressing faster than expected"）
- 2026-05-14｜CEO｜product：CEO 稱部分客戶（尤其 Memory）對混合鍵合有拉貨（原話："We do see some pull-ins for hybrid bonding"）
- 2026-05-14｜CEO｜product：CEO 稱服務營收創紀錄，連續第 13 季季增（原話："marking the 13th consecutive"）
- 2026-05-14｜CEO｜capital_allocation：CEO 稱亞洲新廠預計 2026 年底前後投產，目標擴產、優化成本、區域負載平衡（原話："The new facility is expected to become operational"）
- 2026-05-14｜CEO｜risk：CEO 承認供應鏈有壓力並正與數家供應商協調（原話："We see, I would say, some pressure on the"）
- 2026-05-14｜CEO｜risk：CEO 稱供應商端出現成本壓力，主因晶片價格上漲，以成本管理因應（原話："some cost pressure at the supplier level, mainly tied to the"）
- 2026-05-14｜CEO｜risk：CEO 答分析師質疑製程管制強度時稱今年製程管制表現尚難判斷（原話："it's too early to say how process control looks like"）
- 2026-05-14｜CFO｜risk：CFO 稱 Q1 稅率約 17%，略高於指引，預期正常化（原話："We expect this dynamic to normalize as the year"）

### NVMI_Citi_s_2026_Global_TMT_Conference_20260908.md
- 2026-09-08｜Guy Kizner (CFO)｜guidance：CFO 稱 WFE 數字依賴外部共識，2026 年 WFE 成長將高於 20%，無法給確切數字（原話："when we're looking on the WFE, it will be above 20%."）
- 2026-09-08｜Guy Kizner (CFO)｜competition：管理層說明 2026 年未見慣常的優於 WFE 表現（敘事與先前「2x WFE」框架相比有變）（原話："we don't see the same outperformance that we usually used"）
- 2026-09-08｜Guy Kizner (CFO)｜product：NAND 因多為升級而非新增產能，Nova 尚未受惠，希望 2027 出現（原話："Hopefully, we will see some of it happening in 2027."）
- 2026-09-08｜Guy Kizner (CFO)｜margin：DRAM 的量測密集度低於邏輯，長期模型為邏輯 60／其餘 40（原話："metrology intensity in DRAM is lower compared to the logic"）
- 2026-09-08｜Guy Kizner (CFO)｜risk：AI 客戶仍用 3nm／5nm（N-1）並大舉擴充產能，未轉 GAA，使 2026 量測密集度下降（原話："the metrology intensity went down because of the spending"）
- 2026-09-08｜Guy Kizner (CFO)｜guidance：管理層預期 2027 邏輯端組合偏向 2nm 與 GAA，量測密集度回升（原話："we will see much more metrology intensity going up"）
- 2026-09-08｜Guy Kizner (CFO)｜guidance：DRAM 2027 預期不會有量測密集度顯著提升，要到 4F square 的 2028 年之後（原話："it will happen in '28 and going forward"）
- 2026-09-08｜Guy Kizner (CFO)｜customer：管理層描述訂單能見度優於過往上行週期：積存訂單較高、客戶遵守交期、提前給預測（原話："it's higher versus the previous up cycles"）
- 2026-09-08｜Guy Kizner (CFO)｜customer：客戶提供約一年以上的預測（原話："they are giving you a forecast, say, 1 year ahead"）
- 2026-09-08｜Guy Kizner (CFO)｜customer：被問訂金時，管理層稱交期與條款未改變（原話："we are not changing the terms and conditions"）
- 2026-09-08｜Guy Kizner (CFO)｜product：ELIPSON／METRION 現階段重點是增加應用與搭載率，客戶回購但屬漸進過程（原話："we see repeat buys from leading customers"）
- 2026-09-08｜Guy Kizner (CFO)｜product：WMC 平台一年前推出，近期再宣布一項客戶採用（原話："just recently, we announced another win with this platform"）
- 2026-09-08｜Guy Kizner (CFO)｜product：先進封裝占比由 2025 年約 20% 升至第二季 25%；材料量測尚未切入封裝，被視為下一個成長引擎（原話："we reached a level of 25% of contribution"）
- 2026-09-08｜Guy Kizner (CFO)｜product：混合鍵合 2027 年並非量產大題，目前重點是驗證（原話："the capacity is not a big story in 2027"）
- 2026-09-08｜Guy Kizner (CFO)｜margin：上半年毛利率 59%，第三季財測亦為 59%，管理層稱已處於目標模型高端（原話："In the third quarter guidance, we also guided at 59%."）
- 2026-09-08｜Guy Kizner (CFO)｜margin：毛利率驅動因素：規模經濟、技術進步帶動 ASP；客戶規模越大折扣越高；成本面有材料與人力上升（原話："the bigger customer, the higher discounts"）
- 2026-09-08｜Guy Kizner (CFO)｜margin：產品毛利率高於服務；服務屬人力密集，但隨裝機規模有槓桿（原話："So the gross margins on the service side are lower."）
- 2026-09-08｜Guy Kizner (CFO)｜commitment：新目標模型將於 2027 年初投資人日公布，涵蓋未來五年市場、技術與財務模型（原話："planning to do an Investor Day in the beginning of 2027"）
- 2026-09-08｜Guy Kizner (CFO)｜guidance：第二季達到 2022 年目標模型的營收run rate，比預定時程早約一年；預期營運槓桿持續增加（原話："we should expect operation leverage keep increasing."）
- 2026-09-08｜Guy Kizner (CFO)｜capital_allocation：現金逾 17 億美元，首要優先仍為併購，並維持紀律（增益、符合財務模型、明確綜效）（原話："top priority for us is inorganic growth"）
- 2026-09-08｜Guy Kizner (CFO)｜capital_allocation：先前 1 億美元回購已完成，新增最多 2 億美元授權，視市場條件與估值執行（原話："an additional authorization up to $200 million"）
- 2026-09-08｜Guy Kizner (CFO)｜capital_allocation：併購目標領域不限於封裝或光子，核心篩選是綜效（原話："If we have not identified synergies"）
- 2026-09-08｜Guy Kizner (CFO)｜commitment：擴產：美國產線加倍、德國新無塵室、年底首度在亞洲開無塵室；2027 年 CapEx 仍聚焦基礎設施（原話："by the end of this year for the first time in Asia"）
- 2026-09-08｜Guy Kizner (CFO)｜risk：供應鏈瓶頸被視為關注點，管理層讓供應商看到需求並尋找備援供應商（原話："if there is a bottleneck in specific vendor"）
- 2026-09-08｜Guy Kizner (CFO)｜guidance：中國營收占約 30%；今年原預期持平至略降，現預期名目金額仍成長，占比續降（原話："another growth year for China for us on a nominal basis"）
- 2026-09-08｜Guy Kizner (CFO)｜competition：中國本土廠商正在追趕；管理層視為風險，目前仍有技術差距，策略是加大 R&D（原話："We are not dismissing any competition"）
- 2026-09-08｜Guy Kizner (CFO)｜commitment：對中國本土競爭的策略承諾：持續以高比例營收投入研發（原話："Our goal is to run faster."）

### 問答異常語氣（迴避／改口／保留）
- NVMI_Q1_2026_Earnings_Call_20260514.md｜問：Needham 問中國今年預期（前次為持平到小增）是否改變｜答法：未直接回答是否調整先前說法，也未給數字，改談中國占比下降、長期 25–30%、封裝新客戶及「some potential growth」
- NVMI_Q1_2026_Earnings_Call_20260514.md｜問：Morgan Stanley 問今年製程管制強度偏低下如何優於 WFE｜答法：稱「too early to call」，未給優於 WFE 的幅度，改談製程與製程管制兩條成長線
- NVMI_Q1_2026_Earnings_Call_20260514.md｜問：Barclays 問 Q2 毛利率指引較 Q1 下降的原因｜答法：未說明驅動因素，僅稱指引通常上下 1%、屬同一量級
- NVMI_Q1_2026_Earnings_Call_20260514.md｜問：BofA 問全年成長相對 WFE 與 Memory/Logic 組合｜答法：未給全年成長數字，僅稱預期優於 WFE 並重申 2027 年 10 億美元目標
- NVMI_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問 2026／2027 WFE 規模與五月「中位數十幾%」框架如何演變｜答法：稱自己無內部 WFE 預測、只引用共識，僅說高於 20%，明說很難給確切數字
- NVMI_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問是否仍對「2x WFE」的優於大盤表現有信心｜答法：未直接重申 2x；改談 2026 年投資組合不利並說 2027 組合改善，語氣轉為「well positioned」
- NVMI_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問如何達到目標模型毛利率高端／是否有價值定價重新定價空間｜答法：未給具體路徑數字，以定性因素回答；定價題以「價值導向」籠統帶過，未回答是否重新定價

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

`scenario_inputs`（EPS路徑五年、終端倍數、機率、yield、second_stage、Max DD範圍與依據）——你不寫`scenario.json`，那份由程式跑`dd_scenario.py`產生。Bear機率5Y不應<20%(多數25-30%；極強護城河+短期已兌現才壓15-20%)；Bull/Bear散布5Y應比1Y/2Y寬≥50%；Base機率不應>50%；bear機率須註明依據，sourced結構性durability仍硬套bear需說明「為何不採信」否則不得高於base [§3]。
- 內生天花板sanity check：Base情境EPS CAGR貢獻vs§5.R內生天花板(同組數字不重算)→天花板內✅/超出⚠(⚠→Bear機率強制≥30%)。成長熄火：3年後成長率降至15%/10%/5%三情境×Forward P/E壓縮→估值跌幅，作Bear PE錨。三分量拆解(≤80字，Base IRR多少來自EPS複利/re-rate/股息淨回購)：re-rate貢獻≥Base合計IRR的40%→標記「估值依賴型」(`decision_inputs.valuation_dependent=true`) [§3]。
- IRR落點：<8%/yr弱、8-12%中、>12%強、>15%罕見，不作跨檔排序依據。AR=`(P_bull×|Bull5Y%|)÷(P_bear×|Bear5Y%|)`，<2平庸/2-4偏正/≥4顯著，非放鬆機率防線理由。年期硬規則：①表頭終端年=主時距終端年②終端倍數EPS分母年期與現價倍數同源③終端倍數必附≥1個同業現值comp對照 [§3]。10Y二段延伸(`runway_post_y5`=🟢且終端倍數承重，或Base IRR實質來自Y5後)：Y5→Y10 EPS CAGR/10Y累積倍數/IRR。R:R數學假象：下行>15%正常使用；5-15%警示「已接近定價」；<5%失效標「數學假象」禁引用進場判定，改極端Bear(Bear PE×0.8+Bear EPS×0.85)重算(Bear EPS=FY+1 EPS×0.9；Bear PE=成長熄火「降至10%」情境) [§3]。

**Max DD**(`premortem.max_dd`)：填範圍`lo`/`hi`(禁單點，寬度≥10pp)+`path_risk`(🟢0～−30%/🟡−30～−50%/🔴<−50%)；推導依據須寫`reasoning.premortem`。硬接線：🔴且thesis脆弱(`moat.trend`↓或`runway_post_y5`🔴或估值依賴型)→倉位上限下修(6%→≤3%)；🔴但thesis完整→不因波動砍倉，註記「深回撤心理準備」[§2問六]。

**必答項**：`scenario_inputs`三支EPS路徑、終端倍數、Bear/Base/Bull機率、`premortem.max_dd.lo/hi`、`path_risk`。

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
{"date":"20260515","verdict":"B 觀望（v12.3 unchanged）— 護城河 8/10（execution 8 + pricing power 7，二維 divergence：execution ↑ widening / pricing power → stable）+ 體質 veto 0/5 → B 級；FPE 54x 5Y 分位 95-100% + PEG 2.43 + 同業 metrology tier 中位 +54% 溢價無支撐 → 估值🔴；MA ✅ 但 BB 上軌觸及 → 短期動能透支；QC-31 規則 5「估值🔴 + thesis 完整 → 落 B 等修復」決定 final_signal = B。等 BB 中軌~$461 或 FPE 修復至 35-40x（~$362-$415）再評估進場。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"GAA + 先進封裝帶動 metrology intensity 結構性提升","columns":{"2Y 驗證點":"Nova Rev YoY ≥ WFE YoY + 10%p 連續 8 季","5Y 驗證點":"Metrology TAM 5Y CAGR ≥ 10% vs WFE CAGR ≤ 7%","10Y 驗證點":"1.4nm CFET 量產時 metrology 步驟 / 晶圓 ≥ 5nm 的 1.5 倍","驗證指標":"Rev / WFE 比、metrology 步驟數","資料來源":"2Y: §6 季財報 / 5Y: §8 A Runway / 10Y: §11 TAM 路線圖"}},{"id":"H2","text":"Nova 三平台架構讓全球前 5 大代工廠 / IDM 必選","columns":{"2Y 驗證點":"FY26 先進封裝佔產品營收 ≥ 25%（vs FY25 20%）","5Y 驗證點":"市佔率從 ~4-5% 提升至 6%+（隱含 Nova Rev CAGR &gt; TAM CAGR ≥ 5%p）","10Y 驗證點":"三平台中至少兩個成為 1.4nm GAA generation 的 standard reference tool","驗證指標":"產品營收結構、市佔","資料來源":"2Y: 季財報 / 5Y: 年報 §1 strategic / 10Y: 客戶 design win 公告"}},{"id":"H3","text":"估值修復至合理區間後支持 5Y 翻倍報酬","columns":{"2Y 驗證點":"FPE 從 54x 修復至 35-40x 後再從這個 base 出發","5Y 驗證點":"FY30 EPS ≥ $22.0 + PE 25x → 股價 $550 區（vs 現價 持平 = 5Y 報酬 0%）","10Y 驗證點":"FY35 EPS ≥ $40 + PE 22x → 股價 $880 區（vs 現價 +58%）","驗證指標":"FPE 軌跡、EPS 兌現","資料來源":"2Y: §13.1 / 5Y: §13.5 / 10Y: §8 E 壓測"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"WFE 2027 進入長 cycle 消化期（HBM capex 過峰 + 中國 over-build）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季可觸發）","監測指標":"全球 WFE YoY、SEMI World Fab Forecast；Nova vs WFE YoY 差距（TTM）","警戒閾值":"WFE YoY &lt; 0% 連 2 季 = 警戒；連 4 季 = 大動作減倉；Nova vs WFE 差距 &lt; 8pp 連 2 季 = H1 削弱"}},{"id":"R2","text":"KLA 推出整合三平台方案在 GAA 首次取單（生態攻擊型 — QC-23 🔴）","columns":{"對應假設":"H2","時間尺度":"🐢 長期結構（2-5 年慢變數；事件觸發型）","監測指標":"KLA 新品發佈、Nova 客戶集中度變化、SEMI 大會 metrology 整合相關公告","警戒閾值":"KLA 三平台整合工具公告 + Nova 季 Rev 連 2 季 −（雙條件，避免單一新聞噪音）"}},{"id":"R3","text":"估值壓縮（PE 修復過程，獨立於基本面；ASML 2021/Q3 路徑風險）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發；需快速響應）","監測指標":"Fwd P/E 趨勢、Bollinger Band 位置、共識 EPS 90d 變化","警戒閾值":"Fwd P/E &lt; 35x = 進場觸發；&gt; 60x = 減倉觸發；連 90d 共識下修 &gt; 5% = 重評"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":556.11,"archetype":null,"cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名的每一個**（含程式稍後才會算的 asym_ratio／bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct／ev5y_pct／irr_base_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261012/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
