你是 stock-analyst **v20 判斷 agent**，標的 CARR（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CARR","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CARR_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CARR_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":6263,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）"}},{"id":"f_kpi1_adjusted_operating_profi","label":"Adjusted operating profit","value":1091,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）"}},{"id":"f_kpi2_adjusted_operating_margi","label":"Adjusted operating margin","value":17.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）"}},{"id":"f_kpi3_gaap_operating_profit_lo","label":"GAAP operating profit (loss)","value":-2273,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）"}},{"id":"f_kpi4_free_cash_flow","label":"Free cash flow","value":674,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）"}},{"id":"f_kpi5_stock_based_compensation","label":"Stock-based compensation","value":7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）"}},{"id":"f_kpi6_fy2026_guidance","label":"FY2026 guidance","value":"2.85–2.90","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD adj. EPS","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）"}},{"id":"f_kpi7_backlog","label":"Backlog","value":8500,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m（over）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_carr_gross_margin_pct","label":"CARR 毛利率","value":24.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_carr_operating_margin_pct","label":"CARR 營業利益率","value":8.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_carr_fcf_margin_pct","label":"CARR FCF 利潤率","value":10.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_tt_gross_margin_pct","label":"TT 毛利率","value":34.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_operating_margin_pct","label":"TT 營業利益率","value":17.92,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_fcf_margin_pct","label":"TT FCF 利潤率","value":16.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_gross_margin_pct","label":"JCI 毛利率","value":36.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_operating_margin_pct","label":"JCI 營業利益率","value":14.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_fcf_margin_pct","label":"JCI FCF 利潤率","value":6.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lii_gross_margin_pct","label":"LII 毛利率","value":33.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lii_operating_margin_pct","label":"LII 營業利益率","value":19.94,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lii_fcf_margin_pct","label":"LII FCF 利潤率","value":15.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":54.68,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-16.36,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":44.59,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.35,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.88 → 2.87）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-1.52,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.3 → 3.25）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-1.58,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.79 → 3.73）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.87,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.25,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.73,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.96,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.42,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝5.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":5.9,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.05,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 2.87，分子＝快照價 54.68","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.756,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":10522.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 11876.0、現金 1354.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":818.16,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":55259.0,"period":"2026-11-03","unit":"USD m","basis":"市值 44737.0 ＋ 淨負債 10522.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":23719.49,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":25152.57,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（25 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.33,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 54.43 / W52 59.75 / W104 62.71 / W250 54.64 / W250 13週斜率 0.2%"},{"id":"f_ma_w52","label":"52 週均線","value":59.75,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":62.71,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":54.64,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.2,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 稱各業務面對全球眾多區域性或專業型至大型公私營競爭者；主要競爭因素為技術差異化、產品性能、服務、交期與價格；公司自稱在各主要產品與服務均為重要競爭者，且失去任一合約或客戶不致造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"The most significant competitive factors we face are technology differentiation, product performance, service, delivery schedule and price. Brand reputation, service to customers and quality are also important competitive factors for our products and services.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子揭露：運輸冷凍業務有客戶的關係企業生產與公司競爭的貨櫃冷凍機組，另一客戶生產拖車冷凍機組；客戶或競爭者可能引入非傳統商業模式或破壞性技術。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"For example, an affiliate of a customer in our transport refrigeration business produces refrigeration units for shipping containers that compete with our products, and another one of our transport refrigeration customers produces refrigeration units for truck trailers that compete with our refrigeration units.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Carrier 2026-02 推出資料中心用空冷式冰水機 AquaEdge 30CF；資料中心訂單Q4成長約400%（投資評論類來源，需核實）","source":"TIKR blog","url":"https://www.tikr.com/blog/carrier-global-data-center-transformation-how-a-400-order-surge-fuels-the-93-target","excerpt":"Carrier Global Data Center Transformation: How a 400% Order Surge Fuels the $93 Target Wiltone Asuncion • 6 minute read Reviewed by: David Hanson Last updated Mar 27, 2026","as_of":"2026-03-27","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 揭露 2023–2025 年無單一客戶銷售占比超過 10%。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"There were no individually significant customers with sales exceeding 10% of total sales for the years ended December 31, 2025, 2024 and 2023.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Carrier Q3 2026：總訂單約+35%、商用 HVAC 約 +60%、資料中心約 +300%，積壓訂單超過 85 億美元；管理層稱積壓與含最低量承諾的長約支撐成長至 2027 年及之後","source":"Carrier Q3 2026 earnings (8-K exhibit 99) via search summary","url":"https://www.sec.gov/Archives/edgar/data/0001783180/000178318026000035/a99-q32026earningsexhibit.htm","excerpt":"record backlog levels give us confidence to sustain this momentum into 2027 and beyond","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Carrier 稱現有產能可支撐約 25 億美元資料中心營收run rate，但需要額外產能；2027 年起預期增加美國投資","source":"MarketBeat, Carrier Global Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/carrier-global-q2-earnings-call-highlights-2026-07-28/","excerpt":"existing capacity could support a data center revenue run rate of about $2.5 billion, but additional capacity is needed","as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Q4 2025 財報：住宅量大幅下滑，管理層預期需求偏弱直到房貸利率與消費者信心改善；假設 2026 美國產業銷量下滑 10–15%","source":"MarketBeat, Carrier Global Q4 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/carrier-global-q4-earnings-call-highlights-2026-02-06/?.tsrc=rss","excerpt":"management assumes U.S. industry units will be down 10–15% in 2026","as_of":"2026-02-06","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Linesight 2026 年 6 月美洲報告：關鍵設備需求超過全球現有製造產能；新增產能可能在 2026 下半年至 2027 年緩解壓力","source":"Linesight Construction Market Insights, June 2026 (Americas)","url":"https://www.linesight.com/insights/construction-market-insights-construction-industry-trends-and-supply-chain-dynamics-americas/","excerpt":"demand has outstripped existing global manufacturing capacity for critical equipment","as_of":"2026-06-24","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"經查 FY2025 10-K Item 3 Legal Proceedings 列示的訴訟為石棉與 AFFF（水成膜泡沫）案，未見政府反壟斷調查；Item 1A 僅有一般性反壟斷合規風險揭露。","source":"SEC EDGAR 10-K FY2025 Item 3 / Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"We must comply with U.S. Foreign Corrupt Practices Act (“FCPA”), antitrust, anti-money laundering, and other anti-corruption and anti-collusion laws.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"AFFF 訴訟：截至 2025-12-31，公司、KFI 等被列為被告的案件超過 17,000 件，已併入南卡羅來納 MDL。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"As of December 31, 2025, the Company, Kidde-Fenwal, Inc. (\"KFI\") and others have been named as defendants in more than 17,000 lawsuits filed in United States state or federal courts and a single case in Canada alleging that the historic use of Aqueous Film Forming Foam (\"AFFF\") caused personal injuries and damage to property and water supplies.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026 年 3 月起 Carrier 與其他 HVAC 製造商被列為 HVAC 聯合訂價推定集體訴訟（美國密西根東區聯邦地院）被告，公司稱無理由並於 2026-10-09 聲請駁回，簡報預計延至 2027。","source":"SEC EDGAR 10-Q Q3 FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001783180/000178318026000037/carr-20260930.htm","excerpt":"several other HVAC manufacturers, has been named as a defendant in putative class-action lawsuits alleging violations of federal and state antitrust laws on behalf of direct and indirect purchasers of HVAC equipment. These lawsuits are currently pending in the United States District Court for the Eastern District of Michigan and generally allege that the Company and other industry","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025 10-K：公司2025年透過供應鏈調整、生產力措施與約2億美元增量產品調價，完全抵銷關稅影響；迄今關稅對業務無重大影響。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"Based on our updated analysis, we fully mitigated the impact of tariffs during 2025 through a combination of supply-chain adjustments, productivity initiatives and approximately $200 million of incremental product pricing actions. To date, tariffs have not had a material impact on our business","as_of":"2026-02-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K風險因子：公司在中國、墨西哥等地銷售、生產或採購，貿易限制（關稅）過去曾對業務造成負面影響，未來可能再影響；亦須遵守EAR出口管制，出口限制可能造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"The implementation of more restrictive trade policies, including tariffs, by the U.S. or by other countries, such as China and Mexico, where we sell or produce our products and services or procure materials, or unpredictability or rapid shifts in trade policies, including as a result of trade conflict between the U.S. and other countries, have in the past negatively impacted, and could in the future negatively impact, our business, results of operations and financial condition.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Q3 2026 10-Q：認列1.33億美元IEEPA關稅退款利益（多數沖減銷貨成本）；2026-04-02更新的Section 232鋼鋁銅關稅，公司預期沿用2025策略緩解。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001783180/000178318026000037/carr-20260930.htm","excerpt":"a benefit of $133 million related to refunds of IEEPA tariffs previously paid that we determined are probable and estimable. The benefit was recorded primarily as a reduction to Cost of products sold on the accompanying Unaudited Condensed Consolidated Statement of Operations. On April 2, 2026, updated Section 232 tariffs applicable to steel, aluminum and copper were announced.","as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露：部分產品線僅有單一工廠可生產，天災等中斷可能使該產品停產","source":"Carrier Global FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"in some cases, we have one factory that can manufacture a specific product or product line","as_of":"2026-02-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露：海外工廠與供應商眾多，新關稅、制裁或邊境限制可能影響營運","source":"Carrier Global FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"The imposition of tariffs or additional sanctions, which we continue to monitor and mitigate, as necessary, or unusually restrictive border crossing rules could affect operations.","as_of":"2026-02-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-K：俄烏地區的銷售、營運與供應鏈對 Carrier 不重大（2022 年 3 月起暫停俄羅斯新業務）","source":"Carrier Global FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2026 年 10-Q：2025 關稅已由供應鏈調整、生產力與定價完全抵銷；Section 232 鋼鋁銅更新關稅 2026-04-02 公布，尚無重大影響","source":"Carrier Global 10-Q (2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001783180/000178318026000032/carr-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"Carrier Alliance 供應商計畫宣稱要將供應鏈單點失效降到最低（與 Deloitte 合作、三年 6 億美元成本節省）","source":"StockTitan","url":"https://stocktitan.net/news/CARR/carrier-introduces-carrier-alliance-to-strengthen-optimize-supply-26n3yp7oibe1.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 (reported 2026-10-29): total net sales $6,263M +12%, organic +15%. Climate Solutions Americas $3,354M +24% (organic +25%); Europe $1,335M +3% (organic +12%, offset by divestiture/FX); AMEA $848M +2% (organic +3%); Transportation $726M -3%. Riello and NORESCO divestitures reduced revenue.","source":"Carrier Reports Third Quarter 2026 Results (carrier.com) / 8-K ex99","url":"https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 call transcript summary: orders up ~40%, commercial HVAC orders +65%, data-center orders up fourfold, backlog >$8B, full-year data center sales outlook raised to ~$2B (secondary summary, unverified against primary).","source":"MarketBeat Carrier Global Q2 2026 Earnings Call Transcript","url":"https://www.marketbeat.com/earnings/reports/2026-7-28-carrier-global-co-stock/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Pricing actions of about 2% for FY2026, roughly three-quarters tariff-related (aggregator summary of Q1 2026 results); Q2 adjusted operating margin down 190bp to 17.2% as mix and input costs outran pricing (MarketBeat per search summary). No direct market share data found.","source":"fn2.ai Carrier Q1 2026 / MarketBeat","url":"https://fn2.ai/earnings/carr/2026-q1","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Commercial sales in Americas expected to exceed residential within next couple of years; residential price increases remain part of outlook","source":"ACHR News","url":"https://www.achrnews.com/articles/166689-price-increases-remain-part-of-the-residential-hvac-outlook","excerpt":null,"as_of":"2026-09-15","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"CARR 10-K 風險因素：競爭對手可能開發出先於或取代其產品被市場接受的競爭技術；客戶亦可能引入非傳統商業模式或顛覆性技術與產品；運輸冷凍客戶的關係企業已生產競爭的冷凍機組。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"Our competitors may develop competing technologies that gain market acceptance before or instead of our products.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"ACHR News 2026 展望：預期2026年有一波併購潮，大型業者競相取得技術、工程人才與智慧財產權。","source":"ACHR News, 7 predictions for HVAC in 2026","url":"https://www.achrnews.com/articles/165646-7-predictions-for-hvac-in-2026","excerpt":"Expect a wave of acquisitions in 2026, as both outside investors and HVAC's largest players race to secure technology, engineering talent, and intellectual property","as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K：產品與服務仍以直銷建築承包商／業主，及間接透過合資、獨立業務代表、經銷商、批發商、經銷點與零售通路銷售；運輸部門含訂閱式貨物監控，未顯示通路結構性轉移。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"Products and controls, services and systems are sold directly to building contractors and owners and indirectly through joint ventures, independent sales representatives, distributors, wholesalers, dealers and retail outlets.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"10-K：運輸部門的服務與售後擴張包含隨需與訂閱式貨物監控（小規模訂閱化）。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"our focus on digitalization and innovation is expanding our offering of service and aftermarket solutions, including on-demand and subscription-based monitoring of customer cargo.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Carrier 稱土耳其 Alarko Carrier 合資持股出售後將改採新營運模式、自行承接 Carrier 與 Toshiba 產品的經銷（預計 2026 Q4 完成）。","source":"Refindustry 報導（搜尋摘要）","url":"https://refindustry.com/news/carrier-to-adopt-new-turkiye-operating-model-after-alarko-carrier-stake-sale/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"管理層稱要將住宅現場庫存於 2025 年底降 30% 年減，按經銷商與 SKU 管理。","source":"Carrier Goldman Sachs Industrials Auto Week 2025-12-04 transcript","url":"https://s205.q4cdn.com/164393362/files/doc_events/2025/Dec/04/2025-12-04-CARR-Goldman-Sachs-Industrials-Auto-Week-CORRECTED-Transcript.pdf","excerpt":"down 30% year-over-year. We have a very specific number in our heads of where we want field inventory numbers to be. We not only have it at an absolute number, we have it by distributor, we have it by SKU.","as_of":"2025-12-04","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"channel_business_model_shift#4","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Carrier 推出 Cooling-as-a-Service 服務化商業模式，客戶以固定費用取代前期設備支出。","source":"Carrier 官網新聞：Carrier Launches New Service-Based Model","url":"https://carrier.com/commercial/en/us/news/news-article/carrier-launches-new-service-based-model-for-comfort-and-energy-solutions.html","excerpt":"Carrier Cooling-as-a-Service allows customers to contract for long-term performance and predictable payments rather than incurring an up-front capital cost for system or equipment purchases.","as_of":"2025-01-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 8-K earnings exhibit：FY2026 銷售指引上調至 $23.8–24.0B（有機成長約 10%，前次約 $23B）；調整後 EPS 指引 $2.85–2.90（前次約 $2.90）；調整後營業利益約 $3.5B 與 FCF 約 $2B 不變；Q3 另有 Climate Solutions Europe 非現金商譽減損 $3.1B。此為搜尋摘要轉述，未讀原頁。","source":"SEC 8-K Exhibit 99 Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001783180/000178318026000035/a99-q32026earningsexhibit.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","thesis.H","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 後公司上調 FY2026 調整後 EPS 指引 $2.80→$2.90、銷售 $22.0B→$23.0B；初始指引 EPS 約 $2.80 低於當時共識 $2.99（搜尋摘要轉述）。","source":"Benzinga / MarketBeat FY2026 guidance 2026-07-28; 搜尋摘要","url":"https://www.marketbeat.com/instant-alerts/carrier-global-nysecarr-releases-fy-2026-earnings-guidance-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價：TickFlow 截至 2026-08-01 共識 Buy、12 位分析師平均目標價 $68.86；MarketBeat 2026-03 為 Moderate Buy（12 Buy/8 Hold/1 Sell）平均目標 $70.82；FN2 2026-07 平均 $66.71；Benzinga 目標區間高 $90、低 $58（無日期）。各源分歧、無 11 月最新值。","source":"TickFlow CARR forecast; MarketBeat 2026-03-29; FN2","url":"https://www.tickflow.io/stock/CARR/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Barchart 指 CARR 有 14 個 Strong Sell 評等（三個月前 13 個）；Zacks Rank #1（Q2 後）；Q3 共識 EPS $0.78、營收 $6.187B。","source":"Barchart; Chartmill 搜尋摘要","url":"https://www.chartmill.com/news/external/136414/why-is-carrier-global-carr-down-2-since-last-earnings-report","excerpt":null,"as_of":"2026-08-28","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"AFFF 訴訟：截至 2025-12-31，Carrier、KFI 等被列為超過 17,000 件訴訟被告，已合併於南卡羅來納 MDL；並簽有 Settlement and Plan Support Agreement。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"As of December 31, 2025, the Company, Kidde-Fenwal, Inc. (\"KFI\") and others have been named as defendants in more than 17,000 lawsuits filed in United States state or federal courts and a single case in Canada alleging that the historic use of Aqueous Film Forming Foam (\"AFFF\") caused personal injuries and damage to property and water supplies.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 6 份 8-K 中，含重大項目（1.01/1.02/1.03/2.01/2.05/2.06/3.01/4.02/5.01/8.01 等）者 0 份。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001783180&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"搜尋摘要稱 Carrier 2025-12 同意將 Riello 賣給 Ariston，2026-07-01 完成，現金 $438M；2026-05-18 宣布將 Noresco 賣給 Opterra（預計 Q3 2026 完成，未見完成確認）。未核原文。","source":"Web search summary pointing to Carrier 10-Q (Q2 2026)","url":"https://www.sec.gov/Archives/edgar/data/0001783180/000178318026000032/carr-20260630.htm","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2026-07-28 Q2 財報後股價跌 8.9%，多家原告律所（Pomerantz、Levi & Korsinsky）發佈調查公告；僅為律所徵求投資人，未見已提起之訴狀。","source":"Pomerantz 新聞稿（placera.se 轉載）","url":"https://www.placera.se/pressmeddelanden/carrier-global-investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-carrier-global-corporation-carr-20260828","excerpt":null,"as_of":"2026-08-28","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"搜尋摘要稱 Riello 出售予 Ariston 於 2026-07-01 完成（現金 $438M）；Noresco 出售予 Opterra 於 2026-05-18 宣布。未核原文；未見 2026 年新收購。","source":"Carrier 10-Q Q2 2026（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001783180/000178318026000032/carr-20260630.htm","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"AFFF MDL：超過 17,000 件訴訟，Carrier 與 KFI 為被告。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm","excerpt":"As of December 31, 2025, the Company, Kidde-Fenwal, Inc. (\"KFI\") and others have been named as defendants in more than 17,000 lawsuits filed in United States state or federal courts and a single case in Canada alleging that the historic use of Aqueous Film Forming Foam (\"AFFF\") caused personal injuries and damage to property and water supplies.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Pomerantz 等律所於 Q2 財報後股價跌 8.9% 後發佈投資人調查公告；未見已提起之證券集體訴訟。","source":"Pomerantz 新聞稿（placera.se 轉載）","url":"https://www.placera.se/pressmeddelanden/carrier-global-investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-carrier-global-corporation-carr-20260828","excerpt":null,"as_of":"2026-08-28","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CARR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":24.64,"operating_margin_pct":8.05,"fcf_margin_pct":10.43,"rd_intensity_pct":2.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"TT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.99,"operating_margin_pct":17.92,"fcf_margin_pct":16.43,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"JCI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.65,"operating_margin_pct":14.45,"fcf_margin_pct":6.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"LII","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":33.1,"operating_margin_pct":19.94,"fcf_margin_pct":15.34,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"6367.T","period":"TTM ending 2026-06-30（2季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6367.T","as_of":"TTM ending 2026-06-30（2季加總）"},"note":"Total Revenue 缺失，無法算利潤率；僅 2 季可得，非完整 TTM"}],"subject":"CARR"},"financial_history":{"ticker":"CARR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":17288000000.0,"revenue_yoy_pct":null,"gross_margin_pct":24.86,"operating_margin_pct":11.01,"net_income":3534000000.0,"diluted_eps":4.1,"free_cash_flow":1426000000.0,"fcf_margin_pct":8.25,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":18951000000.0,"revenue_yoy_pct":9.62,"gross_margin_pct":27.24,"operating_margin_pct":10.88,"net_income":1349000000.0,"diluted_eps":1.58,"free_cash_flow":2168000000.0,"fcf_margin_pct":11.44,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":22486000000.0,"revenue_yoy_pct":18.65,"gross_margin_pct":26.6,"operating_margin_pct":9.33,"net_income":5604000000.0,"diluted_eps":6.15,"free_cash_flow":44000000.0,"fcf_margin_pct":0.2,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":21747000000.0,"revenue_yoy_pct":-3.29,"gross_margin_pct":25.86,"operating_margin_pct":8.77,"net_income":1484000000.0,"diluted_eps":1.72,"free_cash_flow":2121000000.0,"fcf_margin_pct":9.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CARR/CARR_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Carrier Global Corporation** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good morning, and welcome to Carrier's Q3 2026 earnings release.
I would like to introduce your host for today's conference, Michael Rednor, Vice President of Investor Relations. Michael, please go ahead.

**Michael Rednor** (Executives):
Good morning, and welcome to Carrier's Third Quarter 2026 Earnings Conference Call. On the call with me today are David Gitlin, Chairman and Chief Executive Officer; and Patrick Goris, Chief Financial Officer. Except where otherwise noted, the company will speak to results from continuing operations, excluding restructuring costs and certain significant nonrecurring items. A reconciliation of these and other non-GAAP financial measures can be found in the appendix of the webcast.
We also remind listeners that the presentation contains forward-looking statements, which are subject to risks and uncertainties. Carrier's SEC filings, including our Form 10-K and quarterly reports on Form 10-Q, provide details on important factors that could cause actual results to differ materially.
With that, I'd like to turn the call over to Dave.

**David Gitlin** (Executives):
Well, thanks, Mike, and good morning, everyone. We delivered a strong third quarter. Organic sales grew 15%. Adjusted operating profit increased about 35% with adjusted operating margins expanding 260 basis points. Adjusted EPS increased 30% or approximately 15%, excluding the impact of IEEPA refunds. Year-to-date free cash flow was also very strong at $1.5 billion. Our strategy is working, and we are winning.
Global orders increased 35% in the quarter with global commercial orders up over 60%. Data center orders increased 300% and year-to-date data center orders have exceeded $3 billion, an increase of nearly 350%. We delivered more than $550 million in data center sales in the third quarter, exceeding our target, and we remain on track to deliver our full year commitment of $2 billion. This momentum has contributed to record backlog of more than $8.5 billion. And remember, that backlog excludes minimum volume commitments under long-term agreements.
Earlier this month, we signed an agreement with a hyperscaler for more than $3 billion with a significant portion of that covered by a minimum volume commitment. Our team is also working with several other leading hyperscalers and large colo customers to secure future agreements across our differentiated commercial HVAC portfolio, including chillers, CDUs and building management systems. It is also encouraging that data center sales are margin accretive to our Applied business.
Importantly, we see strength beyond data centers. Non-data center commercial orders increased 20% in the quarter. Residential sales in CSA increased more than 30%. Residential and light commercial sales in Europe grew 13%. Aftermarket grew 9% and the installed base created by today's commercial growth positions our aftermarket for sustained long-term expansion.
The quarter was strong, but the bigger story is how fundamentally Carrier's growth profile has changed, as you can see on Slide 4. We now have a powerful combination of long-cycle commercial growth, expanding aftermarket revenue and improving short-cycle residential and light commercial markets. This gives us both increased visibility and multiple avenues for sustained growth.
Our commercial HVAC and aftermarket businesses have grown at double-digit rates every year since spin. By the end of this year, we expect these businesses to be approximately twice their size versus spin. And by the end of next year, we expect them to represent nearly half of our portfolio.
We are winning in commercial through differentiation, as you see on Slide 5. We have fundamentally transformed our commercial HVAC business. Our sales are up 2x since spin and our backlog is up 4x. We invested in a new and innovative product portfolio with us seeing great demand for our new 2- and 3-megawatt air-cooled chillers and our new family of CDUs.
In addition to products, we have significantly enhanced our digital, BMS, AI and system offerings, complemented by a far more expansive field network of technicians, spec engineers and selling professionals, all to provide our customers with differentiated outcomes, namely intelligent, autonomous and efficient buildings.
We are also winning because of our execution and customer support. Just in the past month, 2 key hyperscalers have doubled down on their commitments to us based in part on our performance, not only product, digital and systems performance, but also our on-site commissioning and field support.
Our strong demand and backlog require additional capacity. Last week, we announced a new advanced manufacturing and engineering site in Fort Worth, Texas. The facility will add approximately 1,500 highly skilled jobs, in-source critical subassemblies and components and expand our test lab capacity. We plan to begin customer deliveries from this site in the late summer of next year.
Given the tremendous backlog and growth opportunities within our CSA segment, we are appointing 2 proven leaders to ensure that we fully realize our growth and earnings potential in both commercial and RLC in this segment. We announced earlier this week that Gaurang Pandya, who has been a driving force of our commercial transformation and has shown great leadership running CSA will focus all of his efforts on the CSA commercial business, while Ed Dryden, who has been a driving force of our operational, digital and engineering transformation within CST will now take responsibility for CSA RLC. Both are great leaders and will continue to report to me. I will take on responsibility for overall CSA segment, and we will continue to report CSA as such.
In addition to a transformed commercial business, we have market-leading resi and light commercial businesses where markets are improving, as you can see on Slide 6. We had expected the CSA residential market to be below 7 million units this year. It now appears to be tracking to between 7.5 million and 8 million units. In Europe, the heating market is stabilizing. Germany has returned to growth and demand for both heat pumps and air conditioning is extremely strong.
Beyond market recovery, we continue to outperform through product, digital and systems differentiation. The combination of Carrier, Toshiba and Viessmann gives our 5,000 engineers a unique collection of technologies to scale globally. We are leveraging compressors, inverters, controls, drives and software developed across our global centers of excellence to deliver our residential customers globally with intelligent, personalized and efficient comfort. For example, in the U.S., we recently launched a mid-tier heat pump using Toshiba's variable frequency drive and rotary compressor technology and initial orders have been strong.
In Europe, the Viessmann Vitocal 200-A has launched across more than 10 countries with record presales. We are also applying Viessmann's One Base digital framework to our digital offerings in CSA, and our systems approach continues to gain traction. System Profi installers in Europe delivered 70% growth in the third quarter, while in CSA, we will be initiating field trials of our first integrated air-to-air heat pump and domestic hot water solution in the first half of 2027, with full launch expected by the end of next year.
Carrier Energy is progressing our integrated battery heat pump offering through key partnerships, including our selection as the first new technology partner for PG&E's SHARE program funded by Google, and we are installing our first revenue-producing units this quarter. We are also applying the same strategy across buildings and homes, differentiated and cost-competitive products, digital and controls, system solutions, life cycle solutions and go-to-market excellence.
Before I put 2026 in perspective, I want to address Climate Solutions Europe. I am obviously disappointed with the impairment. As I've shared with you before, I remain confident in the strategic rationale and the benefits of the acquisition. In hindsight, our timing was unfortunate. I am, however, very encouraged by what we see ahead. Markets are improving.
Demand for heat pumps and air conditioning is very strong. We are launching compelling new product, digital and system offerings, expanding our channel partnerships and building record commercial backlog. I am confident that Thomas Donato and the team will deliver the growth and margin expansion that we expect going forward.
Before I turn it over to Patrick, a few comments on Slide 7. When Carrier became an independent company in 2020, there were questions about our ability to generate sustained growth. The investments we have made, the portfolio we have built and the way we now operate the company have changed that outlook. Carrier is better positioned for strong growth today than we have been in a long time.
In addition to top line growth, by overdriving on price, productivity and volume, we expect to deliver double-digit EPS growth this year despite facing unexpected in-year input cost headwinds of $550 million to $600 million, driven by tariffs, commodities and supply chain inefficiencies. Gross productivity alone this year will be about $600 million.
We recognize that these actions have been insufficient to drive the margin expansion this year that we expect of ourselves. But we -- but given that we expect the inflationary environment to carry over and continue into 2027, we have already announced a number of price increases. For example, in CSA, we have announced price actions across the portfolio of up to 10%. We will also continue to be very aggressive on driving productivity, restructuring and cost actions and supply chain resiliency.
Though it is too early to give guidance for 2027, thanks to the great work of our nearly 50,000 team members across the world, we expect to enter next year with record backlogs accelerating commercial and data center demand, recovering residential markets, growing aftermarket revenue and differentiated technologies across the portfolio, positioning us for another year of double-digit EPS growth.
With that, I will turn it over to Patrick. Patrick?

**Patrick Goris** (Executives):
Thank you, Dave, and good morning, everyone. Please turn to Slide 8. As Dave mentioned, we had a strong quarter. Reported sales growth of 12% was driven by 15 points of organic sales growth with strong global commercial sales, particularly in the Americas and continued improvement in resi and light commercial in the Americas and Europe. The divestitures of Riello and NORESCO were a net 3-point headwind to reported sales.
The year-over-year adjusted operating margin expansion of 260 basis points reflects the benefit of strong organic growth, including price, partially offset by increased input costs, including tariffs and supply chain challenges. In addition, we recorded an approximate $130 million benefit from IEEPA refunds. And as you can see, free cash flow was very strong at close to $700 million.
Moving on to Slide 9, which shows the Q3 year-over-year earnings bridge. Adjusted EPS increased 30%, driven by operating profit growth and a lower share count, partially offset by a higher effective tax rate.
Let's move on to the segments, starting with CSA on Slide 10. As you can see on the slide, orders continue to be exceptionally strong in this segment. Organic sales growth was also broad-based across resi, light commercial and commercial. Resi was up over 30%, benefiting from the absence of destocking and light commercial was up high single digits. As expected, resi field inventory levels ended Q3 about flat to the prior year, and we continue to expect year-end field inventories to be about flat versus the prior year as well.
Commercial sales were up over 25%, driven by a significant ramp-up in data center deliveries, and our data center sales in this segment increased about 2.5x sequentially. We expect continued strong data center sales growth in the fourth quarter, both year-over-year and sequentially.
Segment operating margin of 22.2% was ahead of our guide due to the benefit of the IEEPA refunds. Excluding the refunds, margins were lower than we expected. The combination of positive but lower-than-expected price realization, increased input costs and supply chain challenges put pressure on margins. As Dave mentioned, we are addressing these 3 areas.
I will review the other segments briefly as the main drivers for Carrier performance are what I just reviewed for CSA. So let's move on to Slide 11, CSE. This segment also had broad-based strong orders growth, up 30%. Organic sales in this segment were up 12%, driven by strong performance in residential light commercial up low teens with heat pump and air conditioning sales both up approximately 35%. As expected, boiler sales declined high single digits.
Commercial sales reflect strong data center growth. Similar to the CSA segment, we expect data center sales to remain strong into year-end. As to profitability, it is encouraging to see the segment deliver double-digit margins.
Turning to Asia on Slide 12. This segment delivered about 5% orders growth with commercial up about 10%. Organic sales grew 3%, reflecting strong performance in commercial HVAC, up double digits, including in China, partially offset by continued softness in residential China. Aftermarket continues to be really strong in this region, up low teens, and segment operating margin expansion was driven by volume growth and strong productivity.
Transportation on Slide 13. Organic sales were down 3% with growth in container more than offset by a mid-single-digit decline in the higher-margin global truck and trailer business.
Turning to Q3 orders on Slide 14. Total company orders in the quarter were very strong, up 35% with growth across all segments and particularly strong in the Americas and in Europe. Our commercial businesses in the Americas and Europe achieved strong data center order intake. Excluding data centers, commercial orders were up 20% globally. Within transport, North America truck and trailer orders were up mid-teens, encouraging, though too early to call for the recovery.
Moving on to Slide 15 and shifting to our updated 2026 organic sales outlook. We now expect full year sales to be nearly $24 billion with organic growth of about 10%, up from our prior outlook, which was a little over $23 billion in sales. The most notable changes are improvements in resi and light commercial in the Americas and in Europe, and we also expect commercial sales in the Americas to be up a bit versus our prior guide.
Moving on to profit and cash guidance on Slide 16. There is no change to our outlook with respect to adjusted operating profit, free cash flow or share repurchases. The most notable change here is in CSA, where we now expect full year operating margin of about 19%. The reasons for the reduction in the margin outlook for this segment are the same that Dave and I covered earlier on this call, positive but lower-than-expected price realization and the impact of increased input costs and supply chain challenges. This takes us to our adjusted EPS outlook of $2.85 to $2.90 for the full year.
You will find the full year bridge and additional guide items on Slide 19 and 20.
Finally, moving on to Slide 17, our key takeaways. As you can see on this slide and as Dave mentioned, we are set up well for a strong 2027.
With that, I would ask the operator to open it up for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Julian Mitchell with JPMorgan Chase & Co.

**Julian Mitchell** (Analysts):
Maybe first question would just be around the margin outlook in the Americas segment. It looks like the guide is implying a sort of maybe low 20s incremental margin year-on-year in the fourth quarter. Just wondered sort of as you look into next year, how quickly do you think that can step up? Or are those price cost headwinds likely to linger for some time?

**Patrick Goris** (Executives):
Yes, Julian, maybe a comment about the Q4 margins. What we expect to happen in Q4 is similar to what we saw in Q3, i.e., strong organic growth, and we expect that to fall through the bottom line. In Q3, our conversion was a little north of 30%. And the benefit of the IEEPA refunds offset the headwinds we saw from increased input costs, lower-than-expected pricing in Q4, and that story is the same for CSA as it is for Carrier.
In Q4, the story is very similar, strong organic growth. We'll see the benefits of that, but we no longer see the impact of IEEPA refund to offset increased input cost headwind and somewhat lower-than-expected pricing. With respect for next year, we think that this will improve sequentially, but I don't think we'll see a snapback in the first or the second quarter.
In terms of outlook for the -- for next year in general, obviously, it's still a little bit early to say, but the bottom line is the following. We'll have a lot of moving pieces. As you know, we start with a very strong backlog. Short-cycle businesses are improving. We'll see some carryover headwinds from our input cost. We also mentioned that we're implementing additional price and cost actions. And the bottom line, frankly, is that we'll target double-digit EPS growth. And I think we'll keep it at that for next year rather than talking about margins at this point.

**Julian Mitchell** (Analysts):
That's very fair. And then just my follow-up would be around that price cost point. So I think you said that the pricing realization has been a little bit underwhelming versus what you had hoped recently, but you also talked about up to 10% price increase to offset higher costs. So maybe just help us sort of understand where is that price sticking and not sticking? And maybe what are you doing differently on price now than before to try and get it to stick better?

**David Gitlin** (Executives):
Yes. Julian, this is David. I assume we're primarily focused on resi pricing in CSA. Look, we had last quarter expected mid-single-digit pricing. We ended up realizing low single digits. If you kind of step back and look at what happened this year, we saw a really big and immediate increase in input costs, especially tariffs when that hit us in April. And I can't speak for the others, but that did have a big impact on us when the 232 tariffs in April went into effect. And in that month, we pretty much immediately announced and implemented additional price increases.
And as Patrick said, the price realization has been improving sequentially but the pace has been a little bit slower than we expected. We have experienced additional cost increases, things like steel, copper, aluminum, some of the freight charges with the higher fuel prices. And that's led us to announce additional price increases. It's up to 10% in CSA. I think it's 8% for resi, and that goes into effect towards the end of this quarter.
But unlike tariffs, where perhaps we were a bit impacted a bit more, we believe that the additional input costs have likely impacted the entire industry proportionately. I would say that in addition to the price increases that we've announced, we've also done a number of other actions as we head into 4Q and we head into 2027. We do have some new pricing tools that help us make very good decisions by customer with some more rigor.
There's some AI behind some of that dynamic pricing model that we're using. We've introduced a new brand for over-the-counter sales. It's called WeatherMaker by Carrier, and we're confident that's already gotten some traction, we'll continue to. And we have some new and improved side discharge and vertical discharge units. So we -- look, we -- I think this year, we were chasing pricing a little bit, and our plan is to get out in front of it as we go into next year.

**Operator** (Operator):
Your next question comes from the line of Scott Davis with Melius Research.
Your next question comes from the line of Nigel Coe with Wolfe.

**Nigel Coe** (Analysts):
I guess Scott is speechless this morning. So just coming back to the price and obviously, looking to push price looks to be fairly aggressive in 2027, but it seems like the pricing power in residential has really deteriorated. So I'm just wondering how we sort of reconcile that dichotomy? And then just on top of that, Dave, maybe just talk about what is the principal problem in resi? Is it really the consumer is tapped out? Is the competition? We hear about Asian imports. What is the big problem right now on realizing price in resi?

**David Gitlin** (Executives):
Yes. Look, Nigel, I would say the resi business is a great business. I think that if you look at what's happened this year, the input cost increases impacting that specific business were very significant and very, very sudden. So we all -- and I could just speak for us, for Carrier, I know that for us, we, of course, raised price coming into the year. And when we saw those additional input cost increases, we announced additional pricing, and we've gotten more pricing this year than we expected coming into the year, but just not as much to cover what were pretty extreme impacts from things like tariffs and inflation.
The market -- the business is a great business. It's a business that we have really good share in and that we continue to introduce new products, system offerings, digital solutions have been coming and will continue to be forthcoming. And it's a very, very unique and good business. I think that this year was a bit extreme in that price/cost dynamic. But I think these questions around has something fundamentally changed in resi, I would tell you the answer is no.
And as we look into next year, we're very clear-eyed about the carryover inflation, the expected inflation, the carryover tariff impact. So yes, we announced an 8% price increase effective later this quarter. And I expect us to be incredibly disciplined and tenacious going forward, both on price and all things, productivity and supply chain resiliency. So yes, this year, we -- it impacted our margins. I feel very confident in the margin profile of this business.

**Nigel Coe** (Analysts):
Okay. That's great, Dave. And then obviously, recognizing that price cost is the major driver of the Americas margin kind of revision. How much though is coming from mix of commercial? And I'm curious about the data center investment ramp specifically. I'm just wondering if that is also a factor. And then just kind of feather in how this new Texas facility might impact margins going into 2027.

**Patrick Goris** (Executives):
Nigel, Patrick here. Within the Americas, mix was not a big driver in Q3 from a margin perspective. Actually, it was close to neutral. The cost this year of the new facility, there will be a couple of pennies in line with what we said basically last quarter. And then for next year, in terms of the margin profile, as I mentioned to Julian, we're not ready on this call to talk about margins for next year. There will be lots of puts and takes. We're targeting double-digit EPS growth.

**Operator** (Operator):
Your next question comes from the line of Steve Tusa with Wells Fargo.

**Charles Stephen Tusa** (Analysts):
So just on this resi business, and you mentioned the side discharge product. Can you just talk about the market dynamics there? I know you guys have had a product for a little while, how you're approaching that strategically? And what percentage of the market -- out of that 7.5 million to 8 million unit market, what percentage do you see it today? And where do you see that going in the next few years?

**David Gitlin** (Executives):
Steve, we do see an increased demand for the side discharge product. And it's mostly the ductless product, but also the unit that we call as a crossover. I know you've been asking since we spun about the hybrid units, which -- that you were right, that continues to gain more traction. And we feel really good about our product portfolio on that ductless hybrid area. It's very good margin for us. We have a very good position.
We have a long-standing partnership with Midea. We work closely with Paul and his team on that space, and we continue to be pleased with that partnership, which we fully expect will continue. And we continue to have a great product offering. One of the great things about the Toshiba acquisition is they have a complete set of technology that fits perfectly for that side discharge unit. So we're using a lot of the technology for introduction here in the United States.
So we're very well positioned. It's a good and growing market. And look, it's probably -- in terms of your question of what percent of the overall market, it's probably about 20% of the 8 million or so that we're going to see this year, the 8 million market. The market is 7.5 million to 8 million, and I think it's about 20%.

**Charles Stephen Tusa** (Analysts):
Got it. And how does that work with Midea? Because I think that they have their own brands that are out there. How is that like structured? Are you -- are there certain regions of the country where you have exclusive distribution? Or like is it just a -- you stick -- you put your sticker on it and it just goes and competes in the wild? Or how is that structured?

**David Gitlin** (Executives):
Yes. I can't, Steve, get too into the details of it. But what I will say is that it's been a great partnership. They have technology. We have a certain relationship as it relates to both Carrier branded and Midea branding, some through our channel, some through others. And we're just -- we're pleased that the partnership has positioned us very well in the ductless space and that hybrid space, and we expect that to continue.

**Operator** (Operator):
Your next question comes from the line of Joe Ritchie with Goldman Sachs.

**Joseph Ritchie** (Analysts):
Dave, can you just elaborate a little bit on the LTAs that you signed? You mentioned minimum volume commitments. I'm just curious if there's like a -- is there a margin profile of that business? And then like what pricing mechanisms do you have embedded in those contracts? I'm basically asking how protected you are against input cost inflation over the life of the LTAs.

**David Gitlin** (Executives):
Yes. I think we feel well protected both on the minimum volume side of it and on the margin side. The margins for our data center business -- those applied sales, they're accretive to our overall applied margins. And -- look, we're not blind to the fact that we've been in an inflationary environment. So that does weigh into how we contract with our customers to make sure that we do our best to not get stuck eating that as inflation continues to increase. So we feel well protected both on the load side as we invest in new capacity, and we feel well protected on the margin side.
Look, if you look at -- I'm really proud of the team. A couple of these -- a number of these hyperscalers, when we started talking to them a few years ago, I'll tell you one of them that I met with asked, are we in the chiller market. Now we have 2 hyperscalers that have said to us that we are amongst, if not their favorite partner across their entire supply chain. And it's because of what we do to not only deliver on time, deliver high-quality, reliable product.
We delivered products. In some cases, we designed and developed products that would have taken 18 months, we did them in 6 months. And when the customer was there to witness the first-of-kind testing, we exceeded the competition and the spec in terms of restart time and operating at full efficiency at high ambient temperatures, and we continue to support our customers.
These 2- and 3-megawatt air-cooled chillers have been very, very well received by key customers. It's resulted in great orders. We support them through commissioning. And then even after we commission and the data center is up and running, we stay there shoulder to shoulder with our customer to ensure that the units are performing as they expect. So they appreciate the customer support.
So we've been winning, and now we're at a point where our execution is helping us drive more wins in the marketplace. So we're really excited with the backlog. So I'm sorry, Joe, to give such a long answer to a simple question, but I'm really proud of the fact that these wins have resulted in the backlog that position us extremely well for these next few years.

**Joseph Ritchie** (Analysts):
Okay. No, great data. I appreciate the color. And I guess maybe just -- I know we've talked a little bit about the pricing and also input cost inflation. You did reference supply chain challenges at all. I was wondering if there was anything specific products that -- or components that you're struggling to get access to today? Or is it more just around kind of like ramping your own capacity just given the strength that you're seeing in the data center business?

**David Gitlin** (Executives):
Yes. I would say that if you look at the fact that we introduced these new 2- or 3-megawatt air-cooled chillers over the past, say, 4 months or so, that there have been some initial teething pains with the supply chain. And that's not unusual for your first production units because it's hard to dual source right out of the gate.
So as I look ahead, here's the things that I feel really good about. Number one is that the designs are -- they're all complete and we're shipping the units. I look at the war room that we have for all things data center production. We are on track to the internal commitments we've made on dual and multi-sourcing.
We're on track to a very specific materials management strategy of what parts do we want where in the world. And the design is behind us, and that's been resulting in the takt time in our factories coming way down significantly, like kind of night and day.
So have there -- were there some initial issues? Yes, things like fans and a couple of other components where we've had to fly units that we otherwise would have put on a ship. Yes, there have been some of that upfront, and that has impacted some of the input costs that we've seen. But as we go into 2027, a lot of those initial teething pains should start to subside now that we've implemented that we can do more of our dual sourcing and we start to see more materials in the places that we want them. And the design is now, of course, stable, and we're producing the units at more rate.

**Operator** (Operator):
Your next question comes from the line of Scott Davis with Melius Research.

**Scott Davis** (Analysts):
All right. Can you finally hear me, guys?

**David Gitlin** (Executives):
We got you.

**Scott Davis** (Analysts):
Phone was muted, I promise. Anyway, I'll move on. So look, I wanted to ask about this Fort Worth facility and the timing of it and such because -- I guess the main question being, does this allow you to bid on or at least more stuff more aggressively? Or is it more done just to kind of release perhaps some of the overburden on your other facilities that are running pretty hot right now?

**David Gitlin** (Executives):
It's both. We -- if you look at the investments, Scott, that we've made in the Americas, we've increased our capacity significantly over these last few years, both for air-cooled and water-cooled chillers, but given our backlog and given our pipeline, just not enough to keep up with all the demand.
So Fort Worth, we have a great relationship with Ross Perot Jr. and the Hillwood team in this AllianceTexas area. The facility shell should be complete here in the coming months. And then we'll do all the tenant improvements and be up and running here by mid- to late summer of next year. And that's to keep up not only with the backlog that we've committed to over these coming couple of years, but it's also to keep up with the pipeline and the win rate that we're seeing.
It's going to effectively more than double our capacity in the Americas, which we need, and it's a wonderful problem to have all the growth that we've seen. An important point, Scott, is that it is not just for data centers. I mentioned that our growth in orders for non-data centers last quarter was 20%. And we've actually, frankly, been constraining ourselves a little bit because of capacity in the non-data center space, things like semiconductor fab, hospitality, higher education, a lot of these key verticals where we're really well positioned with the product portfolio we built. We've had to constrain our sales folks a little bit. The capacity can free up a lot of space for those wins as well.

**Scott Davis** (Analysts):
Yes. That makes sense. And David, it looks like Europe is showing some -- more than green shoots, I suppose, I should say, but they're behind the states and the ramp on D.C., but they're coming. Do you feel like you have the capacity and the infrastructure in place to be able to supply that? Or do you need to get ahead of that also with some capacity adds around something similar like you did in Fort Worth?

**David Gitlin** (Executives):
Yes. What we look at, Scott, is we do a pretty good SIOP planning for our global capacity for all things commercial HVAC. So we have capacity in France, in Montluel. We have capacity in Poland. It's primarily been for residential, but it could free itself up for commercial capacity as well, something that we're looking at. And then we have capacity in places like China, Mexico, multiple now we'll have the U.S. So as we look at it, we're doing our best to -- we're, of course, building Sri City in -- near Chennai in India.
So -- we're doing our best to maximize the capacity we have. We may look at Eastern Europe for a little bit more for the demand we're seeing in Europe. I will tell you that we have plenty of capacity on the residential side. Max Viessmann and the team started it and we kind of saw it through. But in Legnica, Poland, I will tell you, it is the single most state-of-the-art industrial site that I have ever seen. It's highly automated, highly impressive. So we're trying to maximize a lot of our residential heat pump demand that we're seeing in that site. And that site, I encourage folks to visit. It's quite impressive.

**Operator** (Operator):
Your next question comes from the line of Andy Kaplowitz with Citigroup.

**Andrew Kaplowitz** (Analysts):
Dave, just focusing a little more on CSE. I mean, it was nice to see the margins pick up, as you said, organic sales growth double digits. Maybe give a little more color into the improvements the team has begun to make and the visibility into continued heat pump and air conditioning improvement in '27.

**David Gitlin** (Executives):
Yes. I'd say -- let me start on the growth side and then the cost side. On the growth side, as you said, Andy, we're kind of having the moment that we had expected a few years back. It's just coming later than we expected. Heat pump up 35% in the quarter, very, very strong in Germany. Of course, we're well positioned. Air conditioning, long overdue, but that plays right to our strength. So air conditioning up close to 35% in the quarter. We think that continues given, of course, what we saw this past summer.
So both -- not only the Toshiba product that is a really good business for us in Europe, but we've now introduced the Viessmann branded air conditioning that we can put through our traditional channels. So we have Toshiba through its distribution channel and the direct-to-installer selling air conditioning.
So -- and then boilers down, we had always thought it'd be down kind of in the mid-single-digit range. It was down high single digits in the quarter. So pretty much as expected. And the ratio of electricity to natural gas at about 2.5x in Germany. So that's favorable for continued heat pump adoption. So demand very, very good right now, and we saw it with resi sales up about 13%.
On the cost side, Thomas Donato and the team are very clear-eyed about a very comprehensive cost-out program. So it's a combination -- we do have to look at footprint optimization, of course. We are working our supply chain in a very, very rigorous way. We have a very broad network of suppliers globally, and we got to make sure that we optimize that for Europe. And then it's still -- if you look at the G&A that we have across Carrier, it's our highest G&A segment that we have. So there's still opportunity there.
So Thomas is working a very, very comprehensive plan on the cost takeout to get us back to the margin levels that we had always expected. It won't happen overnight, but we will sequentially continue to drive the margins year-over-year improvements that we expect.

**Andrew Kaplowitz** (Analysts):
Great. And then maybe back to CSA light commercial. I think it was up high single digits you guys said. I think, Dave, you said it would be up mid-single. So it's been trending a little bit better than the whole year. Maybe give us sort of focus on like what is going on here and what do you expect moving forward? What markets are sort of driving that strength, would you say?

**David Gitlin** (Executives):
Yes. We were up a little bit more than we thought, and this year is shaping up to be up probably about 10%, and we thought it was going to be down high single digits or so. What's better than we thought is K-12, that had been very strong, then it got very weak. And now that's returning quicker and better than we had thought.
The good news is that we've been winning a lot in some of our strategic national accounts. In fact, as soon as we end this call, I'm going to get on a plane and go meet with the strategic national accounts. So we've been winning. We've been very aggressive on some of our portfolio replacement programs, very structured programs. We've gotten some nice share gains. Retail is good. Health care is good. And as I mentioned, K-12.
What's also encouraging is that field inventory is very, very healthy. We ended 3Q down 20%. So we feel good about this space and 4Q should be up about 20%. It could be up even a bit more than that because customer demand has been strong. So it's nice to see some of the recovery in the light commercial space. And you know that's a good margin business for us.

**Operator** (Operator):
Your next question comes from the line of Joe O'Dea with Vertical Research.

**Joseph O'Dea** (Analysts):
First question just related to the inflation you've seen year-to-date, that $0.55 to $0.60 on input cost and tariffs. Could you give a little bit of color of the split between the 2? How much of that is tariffs? And then looking forward, how do you think about the inflationary headwinds? Any perspective on sizing what is still to come as hedges roll off where you just start to absorb a little bit more of the inflation that's out there on the input cost side?

**Patrick Goris** (Executives):
Yes, Joe, this is Patrick. What you saw on the slide that you were referring to is the incremental input cost headwinds versus the February guide, but that guide had some input cost headwinds in it. If you look at it from a full year perspective, our input cost headwinds are about $800 million. Of that, a little less than half is tariffs. And so some of the input costs, of course, relate to fuel surcharge and material costs and so on. But that is a high-level number, $800 million, a little less than that is tariffs.
For next year, we expect there to be a carryover inflation. As you know, some of these tariffs didn't go into effect until April or so of this year. And so from planning purposes, we are assuming that we'll have another large headwind of inflation next year as we have this year.

**Joseph O'Dea** (Analysts):
That's helpful. And then Dave, just in terms of developments in the U.S. resi HVAC market this summer, it seems like -- it just appears like there was a pretty sharp change in the status quo in that market in a relatively short period of time, in that the industry has long been considered to have a strong ability to get price for cost inflation. We managed through a lot of inflation over the last 5 years.
On the competition side, non-U.S. competition has been part of the conversation for a while, but it appears that maybe it's a little bit more relevant now than it has been in the past. And so the question is just what changed over the last several months for that status quo to potentially have shifted a little bit? And is this more transitory? Or is this a longer duration impact?

**David Gitlin** (Executives):
Look, I will tell you, I do not believe there has been a fundamental change in the nature of this business. We work with a number of phenomenal distributors, and we have over 100,000 dealers. And the nature of the selling process in the Americas, in the United States has not changed. So if you look at it, what happened this year was very, very unique.
When you wake up in April and all of a sudden that you have a sudden influx -- a sudden increase in input costs that is in the hundreds of millions of dollars that it proved to be very difficult to offset dollar for dollar right away. So we knew that there would be some challenges offsetting dollar for dollar, the increase not only driven by tariffs, but we also saw -- where we saw a sudden and fairly unexpected increase in things like copper, steel and aluminum, and then it was exacerbated by some of the fuel surcharges.
So what you want to do in this business is have a good anticipation of what the input cost will be and get out in front on pricing, and we've always been able to do that, and we expect to be able to do that next year. So that's why normally, we would have announced our price increases for 1Q. We've made them effective in 4Q. We're going very clear-eyed into some of the price cost challenges next year that we didn't fully foresee this year.
So for me, that's just -- we didn't fully anticipate the level of input cost increases that we were going to see this year. We believe we have a much better handle on it next year, and we're going to get out in front of it pricing. That's not a fundamental change in the nature of this market. Is there more ductless than there had been in the past? Yes. Do we make great margins and are we really positioned on that side? For sure. So we feel very well positioned in the market, and we think the dynamics of the market are fundamentally the same as they have always been.

**Operator** (Operator):
Your next question comes from the line of Andrew Obin with Bank of America.

**Andrew Obin** (Analysts):
Maybe going to Europe and just talking about what are you seeing on boilers. I think you sort of talked about that, that market is -- is it getting better? Can you just give us more color because obviously, important to profitability? And what's the momentum like in that market?

**David Gitlin** (Executives):
Look, I think the fundamental shift is to heat pumps. So we've always expected boilers to decline. Will it be low, mid-, high single digits as we go forward? It's going to be somewhere in that range. But we expect that boilers will decline.
If you're replacing an existing boiler, you're much more likely nowadays, whether it's because of some of the subsidies or because some of the regulation or because of the instability around fuel prices and oil prices, you are much more likely to want to shift to a heat pump if you possibly can. And that is not just in Germany. We're seeing the same in Italy. We're seeing the same in Spain and Poland and Benelux.
So very, very good demand for heat pumps almost throughout Europe, and that's going to naturally have an impact on boilers. I think it will -- the declines will be in the single-digit range, and it will probably be somewhere in the mid, sometimes it will be closer to high.
If I may, the margins are very good on heat pumps, too. Obviously, good margins on boilers. But the new heat pump that we just introduced in Europe, I mentioned this Vitocal 200-A, those margins are very good as well.

**Andrew Obin** (Analysts):
And just a follow-up on commercial HVAC. We're sort of having some questions coming in on pricing on commercial HVAC side. There seems to be more competition there with all the capacity coming in, particularly sort of lower-tier players. What does the pricing on commercial HVAC look like, not resi, but how do you feel about commercial HVAC pricing?

**David Gitlin** (Executives):
I feel good. I mean, globally. So certainly, here in the Americas and Europe, I think a lot of our customers are focused on the performance of the product, the quality of the product, the support that we give them, our capacity and ability to deliver when they need the product. So I think the pricing has been fair and the pricing has been good.
Will there be certain parts of China or certain parts of Asia where there might be a bit more pricing pressure? Yes. But I would say, generally, globally, that pricing has not been the biggest factor in some of the wins that we're seeing.

**Patrick Goris** (Executives):
We've seen positive pricing in every segment in Q3, Andrew, and we expect the same in Q4. That includes commercial HVAC.

**Operator** (Operator):
Your next question comes from the line of Nicole DeBlase with Deutsche Bank.

**Nicole DeBlase** (Analysts):
Just a few tie-ups here. I think a lot of ground has been covered already. But the non-data center commercial HVAC orders up 20%, definitely interested in that. Dave, could you just talk about like what verticals are driving the strength there?

**David Gitlin** (Executives):
Yes. It's actually been pretty widespread. What we're seeing is very strong for things like the reshoring that we've seen in places like the United States. Industrial has been extremely strong. Hospitality has been good. I'd say the one -- the couple of areas that we watch are commercial real estate has continued to be a bit on the soft side. We actually saw orders pick up, but I don't think enough to make any kind of trends there.
We actually saw -- government has been a little bit weak and higher ed has been a little bit weak. But beyond that, when we look across health care, pharmaceuticals, industrial, semiconductor fab, in Asia, we see some really good demand even for renewables and battery factories. So generally, we're seeing encouraging trends in those areas.
We've actually -- especially in the Americas, been constraining ourselves. So we're excited to get this additional capacity on board because we've transformed the business, as I mentioned in my prepared remarks, that we're really well positioned to win. We just need some additional capacity.

**Nicole DeBlase** (Analysts):
Understood. And then just on the data center bookings, obviously, really strong growth and you guys have talked a lot about the chiller demand there. But what about what you're seeing for the liquid cooling offering, CDUs, ZutaCore, et cetera?

**David Gitlin** (Executives):
Yes. Very, very good demand there as well. So we introduced our 1 megawatt. We have a 2.6 close to 3-megawatt unit that's coming out here in the next couple of months. And then we have a 5-megawatt unit that comes out towards the end of this year. We're already booking orders for even the 5-megawatt unit that even comes out later this year. So -- and it's not just with colos, with some of the hyperscalers, they're looking -- they've been placing orders for the CDUs.
We looked at some acquisitions in the space, and we said, effectively, a CDU is a mini chiller. We can -- we have phenomenal engineers we can organically produce and design our own. So that's what we've done. We're very, very pleased with the demand we're seeing.
And what's really exciting, Nicole, is when we push and we receive orders for our QuantumLeap offering, which integrates the traditional cooling, these liquid cooling CDUs and then our BMS that -- and then we apply digital twins to differentiate the entire system. That's where we see the puck going. That's where we see a lot of differentiation, and it's nice to see some orders for our full QuantumLeap offerings as well.

**Operator** (Operator):
We've reached the end of our Q&A session. I will now turn the call back to David Gitlin for closing remarks.

**David Gitlin** (Executives):
Well, thank you all for joining. What I would ask is folks, look at the last page of our prepared materials, which has our 5 key messages on there. We're very pleased with how we've restructured the portfolio. Data center is strong, growth is broad-based. We are addressing the cost headwinds. We're going in very clear-eyed into next year. So we'll get out in front, both on the productivity and on the pricing side. And our free cash has been very, very strong. So I just want to close by thanking our 50,000 colleagues around the world who show up every day for our customers and to support the results that we expect. So thank you all.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CARR_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CEO｜guidance：CEO 開場宣布上調全年銷售、營業利潤與 EPS 財測。（原話："we are raising our full year guidance on sales"）
- 2026-07-28｜CFO｜guidance：CFO 給出新的全年調整後營業利潤指引約 35 億美元（前次 34 億）。（原話："We now expect adjusted operating profit of about $3.5"）
- 2026-07-28｜CFO｜guidance：CFO 給出全年調整後 EPS 約 2.90 美元（前次 2.80）。（原話："adjusted EPS of about $2.90, up from our prior guide of $3.4"）
- 2026-07-28｜CFO｜guidance：下半年營業利潤與 EPS 預期年增約 50%。（原話："will both be up about 50% year-over-year"）
- 2026-07-28｜CEO｜guidance：全年資料中心銷售展望由 15 億上調至約 20 億美元。（原話："full year data center sales outlook to about $2 billion"）
- 2026-07-28｜CFO｜guidance：Q3 有機成長指引約 10%（營收略低於 60 億，營業利潤率約 16.5%、EPS 約 0.75）。（原話："Organic growth is expected to be about 10%"）
- 2026-07-28｜CFO｜guidance：自由現金流指引不變，較高獲利被新美國廠增加的資本支出抵銷。（原話："No change in outlook with respect to free cash flow"）
- 2026-07-28｜CEO｜guidance：CSA 住宅銷售全年指引上調至高個位數成長。（原話："to be about high -- to be up high single digits"）
- 2026-07-28｜CEO｜guidance：管理層預期今年北美住宅市場約 700 萬至 750 萬台，與去年大致持平。（原話："market to be around 7 million to 7.5 million units"）
- 2026-07-28｜CEO｜guidance：歐洲商用空調下半年預期成長中個位數，依據為 Q2 訂單與在手訂單。（原話："give us confidence in the second half being up mid-single"）
- 2026-07-28｜CEO｜guidance：CEO 說明 CSA 輕型商用 Q3 與 Q4 的成長節奏。（原話："Q3 will be up mid-single digits."）
- 2026-07-28｜CFO｜guidance：CFO 說明 NORESCO 出售對全年營收的影響約 1.25 億美元。（原話："about $125 million year-over-year"）
- 2026-07-28｜CFO｜margin：CFO 稱 Q2 調整後營業利潤率 17.2%，略優於預期。（原話："Adjusted operating margin of 17.2% was a bit better"）
- 2026-07-28｜CFO｜margin：CFO 將 Q2 利潤率下滑部分歸因於關稅減緩措施的時間差。（原話："there is also the timing of the tariff mitigation and"）
- 2026-07-28｜CFO｜margin：CFO 稱 CSA 新建案占比高於預期，拉低整體利潤率。（原話："was a little bit higher mix than what we expected"）
- 2026-07-28｜CFO｜margin：Q3 營業利潤率指引 16.5%，CFO 列出生產力與量能槓桿為驅動。（原話："margin of 16.5% driven by strong productivity and"）
- 2026-07-28｜CFO｜margin：CFO 說明關稅相關的定價僅用於抵銷關稅，不帶來利潤率好處。（原話："we don't really get a margin benefit from that"）
- 2026-07-28｜CFO｜margin：CFO 給出 Q3 CSA（美洲）利潤率約 22%。（原話："For the Americas will be at around 22%."）
- 2026-07-28｜CFO｜margin：CFO 說明 CSA 全年利潤率約持平，商用部分低於整體。（原話："this year we expect the margins to be about flat"）
- 2026-07-28｜CFO｜margin：CFO 給出 CSA 商用利潤率區間。（原話："So they would be in the mid- to high teens."）
- 2026-07-28｜CFO｜margin：CFO 稱資料中心利潤率對整體商用空調利潤率具增益。（原話："margins with data centers are accretive to the overall"）
- 2026-07-28｜CFO｜margin：CFO 說明 2027 年起增量轉換率的區間假設（兩者同速成長下）。（原話："expect us to remain in the 25% to 30% conversion"）
- 2026-07-28｜CFO｜margin：CFO 說明今年投資額約 1 億美元，是財測上調未全額轉換為獲利的原因之一。（原話："will be roughly in the $100 million range."）
- 2026-07-28｜CFO｜margin：CFO 稱關稅減緩的時間差預期明年仍為逆風。（原話："we'd expect that to be a headwind next year"）
- 2026-07-28｜CEO｜margin：CEO 說明 CSE 區段 Q2 利潤率表現。（原話："Segment margins in 2Q were disappointing."）
- 2026-07-28｜CEO｜commitment：CEO 承諾歐洲區段在未來數年內達到中雙位數（mid-teen）營業利潤率。（原話："mid-teen operating margins over the next few years."）
- 2026-07-28｜CEO｜commitment：CEO 在問答中再次表示有信心達成歐洲 mid-teen 利潤率，並指出將更嚴守定價並削減成本。（原話："I'm confident we'll get there"）
- 2026-07-28｜CEO｜commitment：CEO 承認歐洲成本管控過去不夠積極，並表示現在會積極進行。（原話："we should have been more aggressive on cost"）
- 2026-07-28｜CEO｜commitment：CEO 表示維持售後市場全年雙位數成長的目標。（原話："We remain on track for double-digit aftermarket growth."）
- 2026-07-28｜CEO｜commitment：CEO 設定新美國廠投產目標時程為 Q1 底，預計一兩個月內決定廠址。（原話："facility up and running by the end of the first quarter"）
- 2026-07-28｜CEO｜commitment：CEO 說明歐洲新品 Vitocal 200 的上市時程。（原話："We are on track to formally launch in the fall"）
- 2026-07-28｜CEO｜commitment：CEO 對資料中心客戶交付的承諾說法。（原話："Our commitment to our customers is to be perfect quality"）
- 2026-07-28｜CFO｜capital_allocation：CFO 說明全年資本支出因新美國廠上調至約 6 億美元。（原話："We now expect full year CapEx to be about $600 million."）
- 2026-07-28｜CFO｜capital_allocation：CFO 稱全年股票回購維持 15 億美元。（原話："expected to remain at $1.5 billion for the year."）
- 2026-07-28｜CEO｜capital_allocation：CEO 稱 Q2 回饋股東約 6.4 億美元。（原話："returned about $640 million to shareholders"）
- 2026-07-28｜CEO｜capital_allocation：CEO 稱 Riello 出售已完成，NORESCO 出售於前一日宣布。（原話："the divestiture of Riello complete"）
- 2026-07-28｜CEO｜capital_allocation：CEO 說明收購 75F 後 BMS 可觸及市場擴大約 200 億美元。（原話："75F expands our TAM by about $20 billion"）
- 2026-07-28｜CEO｜capital_allocation：CEO 談及擴產風險控管：擔心資料中心資本支出放緩時過度擴張。（原話："we're very careful not to get out over our"）
- 2026-07-28｜CEO｜capital_allocation：CEO 表示液冷領域目前選擇專注自行成長，而非收購。（原話："the decision for now to focus on organic growth"）
- 2026-07-28｜CEO｜customer：CEO 稱 Q2 總訂單年增約 40%。（原話："2Q orders were very strong, up about 40%"）
- 2026-07-28｜CEO｜customer：CEO 稱資料中心訂單為去年同期的 4 倍。（原話："data centers where orders were up 4x over last year"）
- 2026-07-28｜CEO｜customer：CEO 稱總在手訂單超過 80 億美元（不含超大規模與託管業者長約預期訂單）。（原話："is now over $8 billion, up about 40% versus last year"）
- 2026-07-28｜CFO｜customer：CFO 拆解在手訂單中資料中心占比。（原話："and 40% of that is data centers."）
- 2026-07-28｜CFO｜customer：CFO 拆解全年 20 億資料中心營收：上半年約 5 億。（原話："in the first half, we saw about $500 million"）
- 2026-07-28｜CFO｜customer：CFO 說明 CSA 商用 Q2 下滑為資料中心交付時程所致，預期 Q3 大幅回升。（原話："significant sequential and year-over-year pickup in Q3"）
- 2026-07-28｜CEO｜customer：CEO 回應客戶延後交付疑慮：下半年已訂滿。（原話："we're fully booked for the second half"）
- 2026-07-28｜CEO｜customer：CEO 稱客戶要求加速交付，而非延後。（原話："they are pushing us to accelerate deliveries"）
- 2026-07-28｜CEO｜customer：CEO 回應重複下單疑慮。（原話："we're not concerned about double demand"）
- 2026-07-28｜CEO｜customer：CEO 說明輕型商用上調的來源之一為贏得全國性策略客戶。（原話："we've won some really big strategic national accounts"）
- 2026-07-28｜CEO｜competition：CEO 稱公司在資料中心領域持續取得市占。（原話："we've been gaining a lot of share in the data center space"）
- 2026-07-28｜CEO｜competition：CEO 說明公司美國商用空調起始市占低於同業。（原話："we started with very low share for commercial"）
- 2026-07-28｜CEO｜competition：CEO 預期北美住宅今年市占小幅增加。（原話："that we gain a tiny bit of share, but we want"）
- 2026-07-28｜CEO｜competition：CEO 說明與超大規模業者簽訂的長約（LTA）。（原話："give us tremendous contractual confidence in the kind of"）
- 2026-07-28｜CEO｜product：CEO 說明 CDU 液冷產品規劃：1.3MW 已有需求，2.5～2.6MW 本季推出。（原話："We have a 1.3 megawatt CDU that we've seen good demand for"）
- 2026-07-28｜CEO｜product：CEO 說明歐洲 Q2 熱泵銷售與鍋爐的表現。（原話："heat pumps up about 20% and boilers down high single digits"）
- 2026-07-28｜CEO｜product：CEO 說明北美住宅 Q2 價格實現約 3%，下半年改善 1～2 個百分點，全年約 4%。（原話："in 2Q, we were around 3%"）
- 2026-07-28｜CEO｜product：CEO 說明北美住宅下半年約 20% 成長中，10 個百分點來自去年去庫存不再重現。（原話："the absence of destocking in the second half"）
- 2026-07-28｜CEO｜risk：CEO 稱全球卡車、拖車冷鏈業務的復甦時點仍不明朗。（原話："the recovery in Global Truck, Trailer remains unclear"）
- 2026-07-28｜CEO｜risk：CEO 談中國住宅業務長期疲弱。（原話："in China, it's been soft for a while"）
- 2026-07-28｜CEO｜risk：CEO 表示團隊需思考中國住宅業務要投入多少才能根本改善。（原話："investment required to fundamentally improve the business"）

### 問答異常語氣（迴避／改口／保留）
- CARR_Q2_2026_Earnings_Call_20260728.md｜問：Scott Davis 問 Q2 利潤率下滑中，mix 與價格／成本各占多少、其中多少是時間差。｜答法：CFO 列出 mix、關稅減緩時間差與合資收益等因素，但未量化各項占比或時間差大小。
- CARR_Q2_2026_Earnings_Call_20260728.md｜問：Joe Ritchie 問新產能的潛在營收run-rate 能到多少、規劃延伸到多遠。｜答法：CEO 回以現有產能可支撐 25 億、並談市占與避免過度擴張，未給出新廠的營收規模數字。
- CARR_Q2_2026_Earnings_Call_20260728.md｜問：Andrew Obin 問全年 20 億、下半年 15 億與年底出貨率 25 億之間的算術落差。｜答法：CFO 稱 25 億是興建新廠前的數字，Q4 年化將遠高於 25 億，但未給出 Q4 或新的出貨率具體數字。
- CARR_Q2_2026_Earnings_Call_20260728.md｜問：Chris Snyder 問住宅 20% 下半年成長對照 2 年疊加並未改善，憑什麼確信需求轉好。｜答法：CEO 改談剔除去庫存後的 mid-single-digit 終端動能、經銷商來電量與房市積壓需求，未直接回應 2 年疊加數字。

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
{"date":"20260729","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"資料中心散熱是可持續的第二成長曲線，而非一輪資本支出脈衝——Carrier 由約 10% 份額往 15–20% 走，且新增產能不會在需求放緩時變成閒置資產"},{"id":"H2","text":"美國住宅暖通空調的更換週期已經觸底回升——通路去庫存結束，市場自 700–750 萬台往正常化的 900 萬台走"},{"id":"H3","text":"調整後營益率的下滑是時間差與 mix，不是結構性侵蝕——關稅定價時間差消化、歐洲成本結構修好、商用規模吸收後，營益率回到並超越 2025 年水準"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"下半年 15 億美元資料中心出貨的執行風險——全年 EPS 上修完全建立在 2H 調整後營益與 EPS 各 +約 50% YoY 之上，而 Q3 指引 EPS $0.75 已低於財報前共識 $0.857；執行長自承「這純粹是執行問題」，並已把資源投入供應鏈、供應商品質與自家工廠品質"},{"id":"R2","text":"歐洲分部的結構性成本問題 ＋ 關稅時間差在 2027 續為逆風——CSE 分部 Q2 營益率「令人失望」，執行長承認「我們應該在成本上更積極」；新任總裁的修復目標是「未來幾年」走到中十位數，即這是多年工程不是一季修正。同時財務長明示關稅定價時間差明年還會是逆風"},{"id":"R3","text":"Viessmann 併購的資本回報無法證明 ＋ HVAC 價格聯合訴訟——155 億美元商譽（超過股東權益）對應的 ROIC 僅約 10.2%、僅高於 WACC 1.3pp；另有一件在密西根聯邦法院提起的集體訴訟，指控 Carrier、Trane、Daikin、Bosch、Lennox、Rheem、AAON 七家業者以六年時間串謀抬價"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3；加碼＝Q3 資料中心出貨兌現（營收 ≥$5.9B 且 OM ≥16.5%）或回落 $55 以下","irr_base_pct":9.4,"ev5y_pct":53.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":3.7,"ev5y_pct":53.0,"irr_base_pct":9.4,"max_dd_pct":-50.0,"bull_5y_price":154.0,"bear_5y_price":38.0,"p_bull_pct":24.0,"p_bear_pct":30.0,"rearm_trigger":"starter 1/3；加碼＝Q3 資料中心出貨兌現（營收 ≥$5.9B 且 OM ≥16.5%）或回落 $55 以下","price_at_dd":63.16,"archetype":"品質複利成長","cycle_position":"早循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CARR_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
