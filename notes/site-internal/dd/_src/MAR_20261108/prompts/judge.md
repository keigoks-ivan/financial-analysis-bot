你是 stock-analyst **v20 判斷 agent**，標的 MAR（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MAR","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MAR_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MAR_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenues_gaap","label":"Total revenues (GAAP)","value":7005,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"未查得"},{"id":"f_kpi1_adjusted_operating_incom","label":"Adjusted operating income","value":1267,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"未查得"},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":1274,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"n/a"},{"id":"f_kpi3_adjusted_ebitda","label":"Adjusted EBITDA","value":1512,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"未查得"},{"id":"f_kpi4_adjusted_diluted_eps","label":"Adjusted diluted EPS","value":3.02,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"未查得"},{"id":"f_kpi5_gross_fee_revenues","label":"Gross fee revenues","value":1522,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"n/a"},{"id":"f_kpi6_worldwide_revpar_growth","label":"Worldwide RevPAR growth","value":6.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"% YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"n/a"},{"id":"f_kpi7_guidance_q4_2026_adjuste","label":"Guidance: Q4 2026 Adjusted EPS","value":null,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"n/a","needs_sonnet":true},{"id":"f_kpi8_guidance_fy2026_adjusted","label":"Guidance: FY2026 Adjusted EPS","value":null,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"consensus FY1 11.96（dd_numbers_extra consensus_revision，2026-11-07 快照）","needs_sonnet":true},{"id":"f_kpi9_net_rooms_pipeline","label":"Net rooms／pipeline","value":634000,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","unit":"rooms（管線）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 Q3 2026（https://marriott.gcs-web.com/node/37681；SEC 8-K Ex.99 mar-2026q3xex99earningsrel.htm）"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-02","period":"2026-11-02","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-02"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mar_gross_margin_pct","label":"MAR 毛利率","value":19.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_operating_margin_pct","label":"MAR 營業利益率","value":15.93,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_fcf_margin_pct","label":"MAR FCF 利潤率","value":12.71,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_gross_margin_pct","label":"HLT 毛利率","value":30.13,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_operating_margin_pct","label":"HLT 營業利益率","value":24.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_fcf_margin_pct","label":"HLT FCF 利潤率","value":14.49,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_h_gross_margin_pct","label":"H 毛利率","value":20.58,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_h_operating_margin_pct","label":"H 營業利益率","value":8.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_h_fcf_margin_pct","label":"H FCF 利潤率","value":2.45,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chh_gross_margin_pct","label":"CHH 毛利率","value":50.18,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chh_operating_margin_pct","label":"CHH 營業利益率","value":25.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chh_fcf_margin_pct","label":"CHH FCF 利潤率","value":6.8,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":416.47,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":18.39,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":69.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.25,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.93 → 11.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.15,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.37 → 13.39）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.04 → 15.04）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":11.96,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":13.39,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":15.04,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.4,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 11.68 → 11.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":41.52,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":14.15,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":16.42,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":34.82,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 11.96，分子＝快照價 416.47","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.672,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":17225.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 17678.0、現金 453.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":257.5,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":124467.86,"period":"2026-11-08","unit":"USD m","basis":"市值 107242.86 ＋ 淨負債 17225.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":27965.37,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（22 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":29612.86,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.45,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 416.47 / W52 347.51 / W104 305.65 / W250 237.3 / W250 13週斜率 1.66%"},{"id":"f_ma_w52","label":"52 週均線","value":347.51,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":305.65,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":237.3,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.66,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K FY2025 列出主要對手（Hilton、IHG、Hyatt、Wyndham、Accor、Choice、Best Western）及 Airbnb/Vrbo 等短租平台作為替代選項；一手紀錄未載明份額消長數字。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm","excerpt":"We encounter strong competition in the short-term lodging market from regional, national, and international chains that operate lodging properties or franchise their brands, lodging properties that are not affiliated with a chain, and online platforms, including Airbnb and Vrbo, that allow travelers to book short-term rentals of homes and apartments as an alternative to hotel rooms.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：新增客房供給可能壓抑部分市場的房價與入住率。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm","excerpt":"Further, new lodging supply in individual markets could have a negative impact on the hotel industry and hamper our ability to maintain or increase room rates or occupancy in those markets.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Marriott 2026 Q2 全球 RevPAR 成長 3.4%，美加 5.0%，國際 -0.5%","source":"Hotel Dive Marriott Q2 2026 earnings","url":"https://www.hoteldive.com/news/marriott-earnings-q2-2026/826812/","excerpt":"Marriott International saw worldwide RevPAR increase 3.4% year over year in the second quarter of 2026, bolstered by 5% year-over-year growth in the U.S.","as_of":"2026-08-03","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"MAR 10-K 設有「Relationship with Major Customer」附註，披露來自 Host Hotels & Resorts 物業的營收（含代墊成本收入）：2021 年 $1,192M、2020 年 $1,037M、2019 年 $2,406M。此為 FY2021 10-K，非 2026 資料；本軸未查到最新年度占比、客戶信用狀況，也未查到 2026 降評/破產/下修指引來源。","source":"Marriott International FY2021 Form 10-K (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1048286/000162828022002666/mar-20211231.htm","excerpt":"Over the last three years, we recognized revenues, including cost reimbursement revenue, of $1,192 million in 2021, $1,037 million in 2020, and $2,406 million in 2019 from those lodging properties.","as_of":"2022-02-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MAR Q3 2026 公布：全年全球 RevPAR 成長指引上調至 4.5%–5%（原 3%–3.5%）；管理層對 2027 全球 RevPAR 初步看法 3.5–4.5%，預算仍在編製中","source":"Marriott International Q3 2026 results / earnings call (via hotelmanagement.net, asianhospitality.com)","url":"https://www.hotelmanagement.net/data-trends/following-strong-q3-marriott-raises-2026-full-year-guidance","excerpt":"Our preliminary view is that the 2027 year-over-year global RevPAR growth could be 3.5 to 4.5","as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MAR Q3 2026 淨增房間約 20,100 間，淨房數年增 4.6%；管線 4,209 處、逾 634,000 間，其中施工中逾 278,000 間；轉換型占前九個月開業逾 40%","source":"Marriott International Reports Third Quarter 2026 Results","url":"https://marriott.gcs-web.com/node/37681","excerpt":"Conversions continued to be an important driver of growth, representing over a third of signings and over 40 percent of openings during the first nine months of the year.","as_of":"2026-11-02","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"美國供給端：CoStar 預測 2026 供給成長約 0.4%、2027 約 0.6%，在建量為 12 年低點；Lodging Econometrics 預測 2026–2027 供給成長 1.4%，HVS 為 0.8%／1.1%（各家預測不一）","source":"CoStar/STR; Lodging Econometrics; HVS (search summary)","url":"https://www.costar.com/products/str-benchmark/resources/press-releases/us-hotel-construction-down-15-consecutive-months","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"CoStar/Tourism Economics 2026年8月預測：2026 美國 RevPAR +4.4%（世足賽溢價），2027 放緩至 +2.1%；2月預測 2027 為 +1.4%、2028 為 +2.0%，長期平均約 3%","source":"CoStar/Tourism Economics U.S. Hotel Forecast Assumptions – August 2026","url":"https://www.hospitalitynet.org/news/4133888/us-hotel-forecast-assumptions-august-2026","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"英國 CMA 對 CoStar、Hilton、IHG、Marriott 展開調查，懷疑經由酒店數據服務商共享競爭敏感資訊，可能違反 Competition Act 1998 第 I 章；案件狀態 Open，2026-03-02 開案，2026-08-05 更新行政時程。","source":"UK CMA case page：Suspected anti-competitive conduct in relation to hotel accommodation services","url":"https://www.gov.uk/cma-cases/suspected-anti-competitive-conduct-in-relation-to-hotel-accommodation-services","excerpt":"The Competition and Markets Authority (CMA) is investigating the suspected sharing of competitively sensitive information","as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K Item 3：EPA 就 Marriott 管理的一家酒店涉嫌違反 Clean Air Act 提出和解討論；公司認為不會有重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm","excerpt":"In the 2025 second quarter, we received a letter from the U.S. Environmental Protection Agency (the “EPA”) offering to engage in settlement discussions in relation to violations of the Clean Air Act that the EPA alleges occurred at a hotel we manage.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美中峰會後美方暫緩對中國加徵報復性關稅至至少 2026-11-10，並把對中關稅由 20% 降至 10%（產業背景，未點名 Marriott）","source":"FashionUnited: US government suspends additional tariffs on China until end of 2026","url":"https://fashionunited.com/news/business/us-government-suspends-additional-tariffs-on-china-until-end-of-2026/2025110469007","excerpt":"The US will not implement its threatened retaliatory tariffs on Chinese imports until at least November 10, 2026.","as_of":"2025-11-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"美國延後上掛家具、廚櫃、浴室櫃的 Section 232 關稅加碼，酒店業歡迎（翻修成本壓力）","source":"Hotel Management Network: US hotel industry welcomes tariff delay amid trade policy shift","url":"https://www.hotelmanagement-network.com/newsletters/us-hotel-industry-welcomes-tariff-delay-amid-trade-policy-shift","excerpt":"in hotel construction and refurbishment. Mohamed Dabo January 09 2026 Industry groups say the tariff delay helps hotel operators manage costs and plan renovations amid ongoing economic pressures. / Credit: Valery Evlakhov via Shutterstock The US hotel industry has responded positively to President Donald Trump’s decision to postpone planned increases in import tariffs on upholstered furniture,","as_of":"2025-12-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"CoStar：關稅推高建材與 FF&E 成本，高建造成本是新酒店交易的主要障礙","source":"CoStar: while more hotels open in california fewer enter development pipeline","url":"https://www.costar.com/article/1608061149/while-more-hotels-open-in-california-fewer-enter-development-pipeline","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中東約占全球房量4%、開發管線7%、費用4%；伊朗衝突造成中東旅遊需求下滑","source":"Skift, Marriott Sees Middle East Travel Dip, Expands AI Tools","url":"https://skift.com/2026/03/12/marriott-middle-east-dip-expands-ai-tools/","excerpt":null,"as_of":"2026-03-12","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026Q3 全球 RevPAR +6.5%；美加 +7.4%、國際 +4.4%；美加豪華／度假型約 +12%；亞太 >9%、EMEA >4%（中東衝突仍拖累但較Q2改善）","source":"Lodging Magazine / Marriott Q3 2026 results","url":"https://lodgingmagazine.com/marriott-international-reports-q3-2026-results/","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Marriott 將 2026 全球 RevPAR 成長預期上調至 4.5–5%（前次 3–3.5%）；Q4 國際 RevPAR 成長預期較Q3放緩，主因 EMEA 預期年減","source":"Hotel Management: Following strong Q3, Marriott raises 2026 full-year guidance","url":"https://www.hotelmanagement.net/data-trends/following-strong-q3-marriott-raises-2026-full-year-guidance","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Marriott 對 2027 全球 RevPAR 成長的初步看法為 3.5–4.5%；各營運段 2027 細部預測仍在擬定，預期2月公布","source":"CityBiz: Marriott Raises 2026 Growth Outlook, Sees Further Gains in 2027","url":"https://www.citybiz.co/?p=927948","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"CoStar／Tourism Economics 預期 2027 美國旅館 RevPAR 續增但步調較2026緩；美國供給 2027 僅增約 0.6%、營建量為12年低點；2027 ADR 成長預期低於通膨；2026 世界盃造成Q2/Q3高基期","source":"CoStar: US hotel forecast assumptions August 2026","url":"https://www.costar.com/products/str-benchmark/resources/data-insights-blog/us-hotel-forecast-assumptions-august-2026","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"2026Q2 淨客房成長 4.5%（逾180萬間、10,082家）；全年預期落在4.5–5%區間低端（中東工程延誤）；開發管線Q2達629,000間；Q3新增約20,100間淨客房","source":"Quartr / Webull Q2 2026 call summaries","url":"https://quartr.com/events/marriott-international-inc-mar-q2-2026_3sD3LI0T","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 earnings release RevPAR by region","source":"SEC 8-K Ex99 Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001048286/000104828626000040/mar-2026q3xex99earningsrel.htm","excerpt":"Over half of the rooms in the quarter-end pipeline were located in international markets. In the 2026 third quarter, worldwide RevPAR increased 6.5 percent (a 6.4 percent increase using actual dollars) compared to the 2025 third quarter. RevPAR in the U.S. & Canada increased 7.4 percent (a 7.3 percent increase using actual dollars), and RevPAR in international","as_of":"2026-11-02","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子載明：若訂房偏好由自有數位通路移向網路旅遊中介，將推高訂房成本並損及獲利；搜尋引擎也可能把業務導離自有通路。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm","excerpt":"Internet search engines may also divert business away from our direct digital channels to intermediaries.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 載明公司正進行訂房、物業管理與忠誠度系統的多年轉型，部署可能有延遲、系統中斷或資安影響；且若技術更新不如競爭對手快，競爭地位可能受損。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm","excerpt":"We are undertaking a multi-year transformation of our reservations, property management, and loyalty systems. The development and deployment of our new systems could involve delays, system interruptions, compromises of data security, or other operational impacts, including impacts on our financial reporting or internal control environment.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Mews 預期 2035 年前多數飯店搜尋與訂房將透過單一 AI 對話進行（產業預測，非實測）。","source":"Hotel Management: Mews Outlook","url":"https://www.hotelmanagement.net/data-trends/mews-outlook-ai-consolidate-hotel-search-booking-and-service-2035","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Morgan Stanley 分析認為 agentic AI 對訂房平台的衝擊疑慮可能被高估。","source":"Hospitality Today: Morgan Stanley","url":"https://www.hospitality.today/article/morgan-stanley-agentic-ai-unlikely-to-disrupt-booking-com","excerpt":"Morgan Stanley: Agentic AI unlikely to disrupt Booking.com Analysts argue AI-driven travel discovery could reinforce OTAs’ central role in distribution","as_of":"2026-02-25","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 稱 Marriott.com、Bonvoy app 等直銷數位通路為重點，並推進多年期訂房／物業管理／忠誠度系統改造","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm","excerpt":"Our focus on creating frictionless experiences across our direct digital channels is foundational to our worldwide technology systems transformation.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"業界分析（2026-05-28）稱大型飯店集團十年來提升利潤與忠誠度掌控，但未明顯降低 OTA 占比；Marriott 專屬直訂 vs OTA 比重未查到","source":"Hospitality.today 分析（搜尋摘要）","url":"https://www.hospitality.today/article/hotels-barely-moved-ota-share-in-a-decade-the-terms-did-all-the-moving","excerpt":null,"as_of":"2026-05-28","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Bonvoy 會員 2026 Q2 達 2.95 億；加盟與基本管理費年增 14% 至 13.7 億美元，主因聯名卡費；2026 聯名卡費預期增約 35%（含重新議定的權利金率），加盟業主對 Bonvoy 成本分攤與分享卡費提出反彈（二手來源）","source":"Pulse 2.0：Marriott Bonvoy Membership Tops 295 Million（二手）","url":"https://pulse2.com/marriott-bonvoy-membership-tops-295-million-as-credit-card-fees-help-franchise-revenue-rise-19/","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261108","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-03 Q2 報告：FY2026 調整後 EPS 指引上調至 $11.64–$11.81（前次 $11.38–$11.63），高於當時共識 $11.61；Q2 EPS $3.19 對共識 $3.03，營收 $7.07B 低於預期 $7.21B","source":"MarketBeat：Marriott International releases FY 2026 earnings guidance (2026-08-03)","url":"https://www.marketbeat.com/instant-alerts/marriott-international-nasdaqmar-releases-fy-2026-earnings-guidance-2026-08-03/","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026 EPS 指引 $2.74–$2.82，低於共識 $2.88（近期指引較共識保守）","source":"MarketBeat：Marriott International updates Q3 2026 earnings guidance (2026-08-03)","url":"https://www.marketbeat.com/instant-alerts/marriott-international-nasdaqmar-updates-q3-2026-earnings-guidance-2026-08-03/","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布因來源而異：Tickerleague 8 位分析師低 $350／共識 $390.85／中位 $386／高 $446；Pricetargets.com 均價 $384.73（$345–$446）；MarketBeat 5 月均價約 $376.13；Stockanalysis $345.44；各站 as-of 不同，最新約 2026 年 7 月","source":"Tickerleague / Pricetargets.com / MarketBeat / Stockanalysis 搜尋摘要","url":"https://tickerleague.com/companies/MAR/estimates","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill：FY2026 EPS 共識 11.83（31 位分析師，截至 2026-10-17），高於 8 月指引區間中段；下一期營收預估 3 個月內下修 0.46%","source":"Chartmill MAR estimates","url":"https://www.chartmill.com/stock/quote/MAR/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 後 Marriott 再度上調 2026 全年指引（細節待核）","source":"Hotel Management：Following strong Q3, Marriott raises 2026 full-year guidance","url":"https://www.hotelmanagement.net/data-trends/following-strong-q3-marriott-raises-2026-full-year-guidance","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K：Starwood 資料外洩案約100件消費者訴訟合併於馬里蘭 MDL；2025-06-03 第四巡迴上訴法院推翻集體認證（集體訴訟豁免條款有效），公司與原告正進行調解。","source":"SEC EDGAR 10-K FY2025 Item 8 Note 7","url":"https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm","excerpt":"On June 3, 2025, the U.S. Court of Appeals for the Fourth Circuit reversed the District Court’s certification of a class of consumer plaintiffs, holding that a class-action waiver signed by putative class members was enforceable.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K Item 3：2025 Q2 收到 EPA 信函，就某管理飯店涉嫌違反 Clean Air Act 提議和解討論；公司認為無重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm","excerpt":"In the 2025 second quarter, we received a letter from the U.S. Environmental Protection Agency (the “EPA”) offering to engage in settlement discussions in relation to violations of the Clean Air Act that the EPA alleges occurred at a hotel we manage.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 10 份 8-K，其中重大項目3份（1.01 信貸協議修訂、8.01 發債等）；2026-09-23 循環信貸由45億增至50億美元並展期至2031-09-23，屬融資事件非併購。","source":"SEC EDGAR 8-K 2026-09-24 Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1048286/000119312526401051/d145370d8k.htm","excerpt":"The Amended Agreement increases the aggregate commitments under the Prior Agreement from $4.50 billion to $5.00 billion","as_of":"2026-09-24","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 2.01／1.01 併購類協議；1.01 僅為信貸協議修訂。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001048286&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Starwood 資料外洩消費者集體訴訟：2025-06-03 第四巡迴推翻集體認證，部分原告改在紐約州法院個別提告，MDL 原告調解中。","source":"SEC EDGAR 10-K FY2025 Note 7","url":"https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm","excerpt":"Following the Fourth Circuit’s reversal of class certification, some plaintiffs filed lawsuits in New York state court on an individual basis, alleging violations of New York statutory law and seeking monetary damages, attorneys’ fees, and other related relief. We have been engaged in mediation discussions with the consumer plaintiffs in the MDL.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 無 Item 4.02（財報不可信賴）；重大項目僅3份，不含重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001048286&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"MAR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.87,"operating_margin_pct":15.93,"fcf_margin_pct":12.71,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HLT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":30.13,"operating_margin_pct":24.01,"fcf_margin_pct":14.49,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"H","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.58,"operating_margin_pct":8.38,"fcf_margin_pct":2.45,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"IHG","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IHG"},"note":"quarterly_income_stmt 無資料"},{"name":"CHH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.18,"operating_margin_pct":25.1,"fcf_margin_pct":6.8,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MAR"},"financial_history":{"ticker":"MAR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":20773000000.0,"revenue_yoy_pct":null,"gross_margin_pct":21.94,"operating_margin_pct":16.72,"net_income":2358000000.0,"diluted_eps":7.24,"free_cash_flow":2031000000.0,"fcf_margin_pct":9.78,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":23713000000.0,"revenue_yoy_pct":14.15,"gross_margin_pct":21.0,"operating_margin_pct":16.55,"net_income":3083000000.0,"diluted_eps":10.18,"free_cash_flow":2718000000.0,"fcf_margin_pct":11.46,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":25100000000.0,"revenue_yoy_pct":5.85,"gross_margin_pct":19.81,"operating_margin_pct":15.31,"net_income":2375000000.0,"diluted_eps":8.33,"free_cash_flow":1999000000.0,"fcf_margin_pct":7.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":26186000000.0,"revenue_yoy_pct":4.33,"gross_margin_pct":19.94,"operating_margin_pct":15.81,"net_income":2601000000.0,"diluted_eps":9.51,"free_cash_flow":2608000000.0,"fcf_margin_pct":9.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MAR/MAR_Q3_2026_Earnings_Call_20261102.md）

# Q3 2026 Earnings Call
**Marriott International, Inc.** | Earnings Calls | 2026-11-02

**Operator** (Operator):
Hello, and welcome, everyone joining today's Marriott International Q3 2026 Earnings. [Operator Instructions] Please note this call is being recorded. We are standing by if you should need any assistance.
It is now my pleasure to turn the meeting over to Jackie McConagha, Senior Vice President of Investor Relations. Please go ahead.

**Jackie McConagha** (Executives):
Thank you. Good morning, everyone, and welcome to Marriott's Third Quarter 2026 Earnings Call. On the call today are Tony Capuano, our President and Chief Executive Officer; Jen Mason, our Executive Vice President and Chief Financial Officer; and Pilar Fernandez, Senior Director of Investor Relations.  
Before we begin, I would like to remind everyone that many of our comments today are not historical facts and are considered forward-looking statements under federal securities laws. These statements are subject to numerous risks and uncertainties as described in our SEC filings, which could cause future results to differ materially from those expressed in or implied by our comments. Unless otherwise stated, our RevPAR, occupancy, ADR and property level revenues comments reflect system-wide constant currency results for comparable hotels and all changes refer to year-over-year changes for the comparable period.
Statements in our comments and the press release we issued earlier today are effective only today and will not be updated as actual events unfold. You can find our earnings release and reconciliations of all non-GAAP financial measures referred to in our remarks today on our Investor Relations website.
And now I will turn the call over to Tony.

**Anthony Capuano** (Executives):
Thanks, Jackie. Good morning and good afternoon, everyone. We're joining you today from the beautiful JW Marriott Grosvenor House in London, and we're excited to share our third quarter results. We reported an excellent quarter this morning with RevPAR and financial results above our prior expectations. Development activity remains strong, and we grew net rooms by 4.6% over the 12 months ending September 30.
Third quarter global RevPAR rose 6.5%. RevPAR in the U.S. and Canada region rose 7.4%, improving on a strong first half of the year and reflecting strength in both World Cup and non-World Cup markets. Excluding the World Cup, third quarter RevPAR in the U.S. and Canada rose 6.2%. Growth continued to be broad-based across customer segments and chain scales.
Luxury and resort hotels again led the region in the quarter with luxury RevPAR increasing 12%, while select service RevPAR had its third quarter of solid year-over-year growth, rising over 6% compared to the prior year quarter. Third quarter international RevPAR rose over 4%, led by the APEC region, where RevPAR increased more than 9%. Performance in APEC reflected broad-based sustained demand across the region, supported by robust intra-regional and long-haul international travel.
RevPAR in Greater China was around flat in the quarter, reflecting an uneven consumer spending environment and the impact of major typhoons across the region. Continued strength in luxury and in the Hong Kong, Taiwan and Hainan markets was offset by slower domestic leisure demand across much of the rest of the Chinese Mainland.
RevPAR in the Caribbean and Latin American region rose over 3% in the third quarter, driven by strong luxury and leisure demand across the Caribbean, which offset continued softness in Mexico.
RevPAR in EMEA rose over 4% with Europe and the Middle East both outperforming prior expectations. RevPAR in Europe rose over 6% in the third quarter, with strength broad-based across key markets, chain scales and customer segments.
Middle East RevPAR declined 12% in the quarter, a meaningful improvement from the second quarter when RevPAR declined over 40%, helped by healthy local and regional demand.
As Jen will discuss further, with strong base demand across chain scales generally expected to continue, we are again raising our full year 2026 guidance. We now expect 4.5% to 5% global RevPAR growth. This is well above the 1.5% to 2.5% growth range we initially forecast on our year-end 2025 earnings call as travel demand has been remarkably robust this year despite geopolitical uncertainty.
Turning to results by customer segments. In the third quarter, leisure RevPAR rose 7% globally and 9% in the U.S. and Canada as people around the world continue to prioritize in-person experiences like travel. Group RevPAR rose 6% globally and 7% in the U.S. and Canada. Third quarter business transient RevPAR rose 4% globally and 5% in the U.S. and Canada.
On the development front, signings activity remained strong, particularly in international markets, and we achieved record global organic signings in the first 9 months of the year. We continue to have the largest pipeline in the industry. Our global pipeline grew over 6% year-over-year to a new record of over 634,000 rooms at the end of September with an industry-leading 278,000 rooms under construction, including pending conversions. We are still seeing terrific momentum in conversions, including multiunit deals given the many top and bottom line benefits of joining the Marriott portfolio.
In the first 9 months of the year, conversions accounted for over 1/3 of our signings and over 40% of our openings. For the full year 2026, we still expect net rooms growth towards the low end of our prior 4.5% to 5% range, including our typical assumption of between 1% and 1.5% room deletions. With our growing pipeline and conversion momentum, we still expect net rooms growth to grow in the mid-single-digit range over the next several years.
Our relationships with our hotel owners are of paramount importance to us. We remain deeply committed to working alongside them to continue to leverage our industry-leading scale to enhance property level economics and deliver sustainable long-term value. As we've discussed before, we've taken a number of steps to drive hotel level economics. These steps include lowering loyalty charge-out rates, enhancing reimbursement for Bonvoy redemption stays on high-demand nights, rolling out flexible renovation scopes and streamlined brand standards and introducing an intent to recommend incentive in the U.S. and Canada.
Our owners, associates and guests are also expected to benefit from our significant multiyear technology transformation, which is well underway. We are excited about the benefits this transformation will deliver across our stakeholder groups. One recent innovation developed in-house on our proprietary technology platform is an in-app complimentary upgrade list that is currently in beta. The feature will give eligible Elite members greater visibility into potential upgrades before arrival by showing their position on the upgrade list and an estimate of available upgrades that match their reservation while still preserving premium room upsell opportunities for our owners.
Additionally, we're expanding our use of AI across the enterprise to enhance hotel performance, drive measurable business value and enhance the associate and guest experience. As AI reshapes how people discover, plan and book travel, we are focused on optimizing Marriott's presence in the AI-generated arena, introducing conversational AI in our own channels through features such as Ask Bonvoy and testing new search and commerce experiences through integrations with leading platforms like Google and OpenAI.
Our powerful award-winning Marriott Bonvoy loyalty program now has approximately 309 million members around the world. Members continue to engage with us across our unmatched portfolio of brands and experiences as well as through our numerous collaborations, including our co-branded credit cards. Marriott Bonvoy deepens our relationships with guests, drives valuable direct bookings for our owners and is a key reason owners and developers choose to join the Marriott system.
Before I conclude, I want to thank our Marriott teams around the world whose hard work and dedication helped make these strong results possible.
And now I'll turn the call over to Jen for more details on our financial results. Jen?

**Jennifer Mason** (Executives):
Thank you, Tony. I will start by reviewing our strong third quarter results.
Total gross fee revenues rose 14% year-over-year to $1.52 billion, driven by higher RevPAR, rooms growth and higher co-branded credit card fees. We delivered this growth even as residential branding fees declined 35% due to timing of unit sales.
Incentive management fees, or IMF, rose 22% to $181 million in the third quarter, led by a meaningful increase in the U.S. and Canada that reflected strong RevPAR growth and a solid improvement in hotel margins. Third quarter IMF also grew year-over-year in all international regions, including EMEA, where strong results in Europe more than offset a decline in the Middle East.
Owned, leased and other revenue, net of owned, leased and other expenses totaled $41 million compared to $70 million in the third quarter of last year. The decline reflected lower owned, leased hotel results, including the impact of renovations, the second quarter sale of a hotel in the U.S. and higher costs associated with a third-party agreement, partially offset by a $12 million expected insurance recovery associated with the accrual taken in the second quarter for a property-related litigation matter. Our disciplined focus on controlling costs, combined with lower litigation expenses led to third quarter G&A rising just 2% year-over-year.
Third quarter adjusted EBITDA increased 12% to $1.51 billion and adjusted diluted EPS rose 22% to $3.02.
Now let's talk about our outlook. As Tony mentioned, we are raising our full year 2026 global RevPAR guidance to 4.5% to 5%, reflecting our third quarter global outperformance as well as a stronger outlook in the fourth quarter. Recall that the strong World Cup performance in June and July provided a slightly larger boost to full year global RevPAR than expected at around 45 basis points.
Global RevPAR in the fourth quarter is anticipated to increase 4.5% to 5%. In the U.S. and Canada, we expect the strong demand trends that we saw in the third quarter across chain scales and customer segments to continue, although there could be a small negative impact from the November midterm elections. Internationally, fourth quarter RevPAR growth is expected to decelerate compared to third quarter growth, primarily due to an anticipated year-over-year RevPAR decline in EMEA.
In EMEA, continued strength in Europe is anticipated to be more than offset by declines in the Middle East. As we have discussed, the Middle East faces difficult comparisons from the fourth quarter of 2025 when several large events drove meaningful ADR increases. Saudi Arabia has also recently seen the cancellation of some large events followed by heightened -- following the heightened tensions there. As a result, we expect a more meaningful year-over-year RevPAR decline in the Middle East in the fourth quarter than in the third. And because the Middle East enters its peak tourism season in October, the Middle East region's performance will have a greater impact on EMEA's fourth quarter results than it did in the third quarter.
As we look ahead to next year, while we are still working on our budget, we currently expect continued strong demand trends. Our preliminary view is that the 2027 year-over-year global RevPAR growth could be 3.5% to 4.5%. Note that while we are comping the World Cup, this is expected to be offset by easier comparisons in EMEA.
Turning to this year's financials. In the fourth quarter, gross fees could rise 13%,  reflecting robust RevPAR and rooms growth as well as strong growth in residential branding fees and credit cards. IMFs are expected to be around flat year-over-year with increases in the U.S. and Canada, APEC  and Europe, offset by declines in the Middle East and Greater China.
Fourth quarter adjusted EBITDA is expected to increase 12% to 14%. For the full year, we are raising our gross fee guidance to an increase of around 13% with IMF now expected to rise in the high single-digit range. The sensitivity of 1% change in full year 2026 RevPAR versus 2025 could be around $55 million to $65 million of RevPAR-related fees.
Full year co-branded credit card fees are still expected to rise in the high 30% range. Residential branding fees are now expected to rise over 90%. Timeshare fees are still expected to be relatively in line with the prior year at $110 million to $115 million. Owned, leased and other revenue, net of owned, leased and other expenses is now anticipated to total $170 million to $175 million in 2026.
Note that the full year outlook reflects the sale of 2 U.S. hotels. One was sold in the second quarter and one is expected to be sold later this quarter. The first hotel is now under a new long-term management agreement, and we expect the second hotel will be as well upon closing. We are pleased with the sale of these 2 properties and remain focused on recycling owned and leased assets when the timing and pricing are right.
2026 G&A expense is anticipated to rise just 1% to 2% compared to 2025 levels. Full year adjusted EBITDA is expected to rise around 13%. Strong adjusted EBITDA growth, combined with a meaningful reduction in share count leads to expected full year adjusted diluted EPS growth of 20% to 21%.
Our outlook for full year 2026 key money and total investment spending has not changed. Investment spending is still expected to be $1.25 billion to $1.35 billion, with key money anticipated to be 40% to 45% of the total amount. Spending on technology is expected to be another 25% to 30% and the remaining portion is spending related to renovations at owned and leased hotels as well as other investing activities.
Our capital allocation philosophy also remains the same. We are committed to our investment-grade rating and investing in growth that is accretive to shareholder value. Excess capital is returned to shareholders through a combination of share repurchases and a modest cash dividend, which has risen meaningfully over time. Considering our strong year-to-date cash flow performance and our higher adjusted EBITDA outlook, our full year 2026 capital returns to shareholders are now expected to be at least $4.8 billion. Full year guidance details for the fourth quarter and the full year are in our press release.
Tony and I are now happy to take your questions. Operator?

**Operator** (Operator):
[Operator Instructions] We'll take our first question from the line of Shaun Kelley with Bank of America.

**Shaun Kelley** (Analysts):
Tony, Jen, congrats on the strong results. It's great to see the travel environment where it sits. Tony, I want to take it in a slightly different direction though. I'd love to just get an updated -- your updated thoughts on the owner relation topic. You gave a lot of color on this last quarter. And mostly, what I wanted to get your sense was from -- as we sit a quarter later, some of the feedback you received from owners, specifically around the ITR incentive, things you're looking to adjust or improve and just kind of where we sit from this time right here today.

**Anthony Capuano** (Executives):
Of course. Thank you for the question, Shaun. The -- yes, I do have some more to add. We've continued to be engaged with a broad cross-section of the owner community. To state the obvious, our owners are foundational to our business. The health of the owner and franchisee community is of paramount importance. And we are across the leadership team, appreciative of the consistent and in many cases, decades-long engagement we've had with those owners. We also appreciate the mutual recognition of how intertwined our success is.
And we're equally appreciative of the recognition that structurally, our business models are different. And I think it's that long-standing recognition that leads to the sort of regular constructive discussions we have on a wide range of issues, normally quite proactively in the case of a subset of the owners in a reactive way. But I think that communication is reflective of how we approach the business more broadly.
We are laser-focused on hotel level economics, both on driving top line and looking at every expense line in the P&L. You heard in my prepared remarks a number of the steps we've already taken and continue to take to try and drive hotel level economics. We'll continue to talk to this subset of owners, but we'll continue to talk to all of our owners regularly. And I think we'll continue to make progress with this specific group.
The tenor of these discussions that I've been involved with, I would describe as transparent, I would describe as collaborative and I would describe as constructive. The other thing I would share with you, since we spoke about this a quarter ago, many of Marriott's senior leaders were down in Miami for a U.S. and Canada Full-Service and Luxury Owner Conference we had the middle of last month.
Again, lots of candid productive conversations, lots of mutual acknowledgment of how inexorably linked our success is and lots of focus on Marriott's ability to leverage its industry-leading scales in a way that directly impacts their economic performance.
And then the last thing I would say to you, sometimes I get the sense there is an expectation of a big reveal. We will continue to focus on each of the constituents we serve every day. We work every day to create opportunities for our associates. We work every day to enhance the travel experiences of our guests and Bonvoy members. And we have and will continue to work every day to drive economic performance for our owners.

**Operator** (Operator):
And we'll take our next question from Richard Clarke with Bernstein.

**Richard Clarke** (Analysts):
I guess you use in your prepared remarks language broad-based demand across the different chain scales. But if I look at the gap between your luxury performance in the U.S. and the select service, I think it's actually widened a bit to 5.5% RevPAR growth. If you look ahead to kind of Q4 and maybe into your remarks you gave on 2027, are you expecting that to continue? Or are you expecting the gap between the different chain scales maybe to actually contract from here?

**Jennifer Mason** (Executives):
Yes. We're certainly pleased with the performance across all chain scales. You're correct that luxury continued to outperform, but select service being up 6%, and that's an improvement quarter-over-quarter. So -- and we continue in bookings through October to feel good about the performance of our select brand hotels.

**Anthony Capuano** (Executives):
Yes. I think that's right, Richard. The -- maybe not a surprise that luxury continues to be so strong, but a really encouraging sign to see 3 consecutive quarters of such strong RevPAR performance at the other end of the chain scales.

**Operator** (Operator):
And our next question comes from Stephen Grambling with Morgan Stanley.

**Stephen Grambling** (Analysts):
So your comments on the owner relationship is probably a good segue into agentic AI actually. I recognize this is still an evolving topic, but would love to hear any color on the initial impact to distribution as we think about mix or commissions? And then more broadly, just how you think about both the near-term and maybe longer-term impact to both owners and your business?

**Anthony Capuano** (Executives):
Yes. Thank you. There's a lot in there, Steve. I'll give it a shot. Jen may jump in and help me a little bit. I continue to be a firm believer that AI is going to profoundly impact virtually every industry, certainly the travel vertical. As we've discussed in the past, the real challenge and opportunity for us is to take advantage of these emerging technologies without losing the human-centric approach that's guided us for nearly a century.
In some ways, we're in the early innings of AI's entry into travel. Right now, our view is that AI is largely reshaping travel discovery. That doesn't mean at some point, it won't have a similar impact on bookings, but that piece seems to be moving more slowly. So we are very engaged with a number of the AI platforms to ensure that as discovery, as search is out there, that we are populating these platforms with as accurate and rich a set of content as possible. So those users really have terrific insights into all that our portfolio has to offer.
In terms of distribution costs, again, I think it's early. A number of the platforms, if they are looking to monetize, they're leaning more towards more traditional advertising monetization as opposed to booking. They are starting to dip their toes, some of them into what that might look like. Intuition would suggest it would be compelling from an economic perspective for our owners, but I think that's a story that largely remains to be told.

**Operator** (Operator):
And our next question comes from Patrick Scholes with Truist Securities.

**Charles Scholes** (Analysts):
Tony, when we think about that initial 3.5% to 4.5% RevPAR guidance for next year, within that, what is your expectation for the composition of room rate growth versus occupancy? Certainly, in the most recent quarter, with the upside for incentive management fees and high ADR growth increasingly important to think about the composition. So just your thoughts around that.

**Anthony Capuano** (Executives):
Sure. It's probably a little early for me to give you too much insight. We are up to our eyeballs in the budget process right now. What I can tell you, and I might ask Jen to give you a little more texture to this. But when we look at the performance through the first couple of quarters of this year, one of the things that's been encouraging is in many of the markets, we've seen a nice blend of both room night and ADR growth, and we'll obviously be investigating that closely as we put the finishing touches on the '27 budget.

**Jennifer Mason** (Executives):
Yes. Well said, Tony. On your question on IMF, right, for Q4, while certainly, we see upside in U.S., Canada and APEC and other places, the Middle East, as we've talked about on our call, we expect to be impacted -- continue to be impacted in Q4. So that offsets the upside from the other comments.

**Operator** (Operator):
And our next question comes from Trey Bowers with Wells Fargo.

**Raymond Bowers** (Analysts):
I think we talk about this most of these calls, but maybe you guys could just dig in a little bit on capital intensity thoughts as we move forward, especially around key money kind of in that now $500 million to $600 million range. Is that the new normal from here? Is that expected to grow from here? And just any color around that would be great.

**Anthony Capuano** (Executives):
Sure. Thank you for the question. I'll let Jen give you a little perspective on a go-forward basis. But to state the obvious, it is a competitive environment out there, particularly given the increasing importance of conversions. Whether we like it or not, key money seems to be the weapon of choice against that competitive landscape.
The 2 things I would want to leave you with: one, the rigor that we've always applied to the use of MI capital, irrespective of what type of capital remains. We put all deals where we consider investment through that rigorous evaluation. And anticipating we might have some conversation about that, we did a little work. One of the things that's quite interesting, I think, deals that use key money historically have yielded significantly more value than deals without key money.
And I'll just give you 2 statistics to frame that. If you look at all the deals we did in calendar 2025, the deals where Marriott participated with key money had an average value premium per room of about 65%. Year-to-date through the first 3 quarters this year, those deals where we deployed key money had an average premium per room of about 75%.

**Jennifer Mason** (Executives):
Yes. And on your question on broadly investment spending, as we talked about in the prepared remarks, we still expect investment spending this year to total $1.25 billion to $1.35 billion. As a reminder, 40% to 45% of that is for contract acquisition costs, which includes both new and existing units, 25% to 30% of that is for the digital technology transformation and the rest is spending at renovations on owned, leased hotels.
For next year, it's really still too early, right? We're working through our budgets, but you could expect kind of similar color and market dynamics on that. Key money and contract acquisition costs are likely to continue to rise given the system growth. And while DTT and technology spend is expected to come down a bit, we'll continue to invest heavily in technology. And then for owned, lease and other investment, some of our properties undergoing renovations in '26 will be done, but we'll also have others that will go under renovation next year.

**Operator** (Operator):
And our next question comes from Michael Bellisario from Baird.

**Michael Bellisario** (Analysts):
Tony, on development, can you just update us on the trajectory of construction starts and how that part of the pipeline is trending in both the U.S. and ex U.S. markets? And also any early kind of directional comments on your view of rooms growth into next year versus this year's 4.5%?

**Anthony Capuano** (Executives):
Yes, of course, Michael. Thank you for the question. The new build construction starts in the U.S. and Canada last year were up about 7% versus the prior year. Through the first 3 quarters this year, new build construction starts are up 20% year-over-year. Again, we're not quite back to where we were in 2019, but the trend line is certainly encouraging.
Globally, which I think was the second part of your question, year-to-date through the first 3 quarters of the year, new build construction starts were down about 24%. But I would maybe put an asterisk on that data. The quality of the data we get is maybe not as precise as what we get in the U.S. But I think the fact that construction starts while building are not back to where we were pre-pandemic, probably illustrates the importance of the success we're having on the conversion side, where, as I mentioned, about (sic) [ above ] 1/3 of our signings, above 40% of our openings are being derived through the very deliberate approach our development teams are taking to capturing a disproportionate share of the conversion opportunities that are out there.

**Operator** (Operator):
And our next question will come from David Katz with Jefferies.

**David Katz** (Analysts):
Thanks for all the detail and information. I wanted to just focus on the Middle East. And if we were to use an assumption of kind of an ongoing low-intensity circumstance over there, I assume you're looking through various permutations of what could be for the market. But given it's so important for NUG and RevPAR, how can we think about that market? Can we be comfortable that the units that have been in the pipeline can still get done? And can that market get back to at least flat RevPAR or enough where it's not an offset to otherwise pretty strong results everywhere else in the world?

**Anthony Capuano** (Executives):
Thank you, David. Maybe before I try to answer your couple of questions, let me just for the group, remind you or ground you, while a critically important market through a lot of different -- or set of markets through a variety of lenses, the Middle East represents just 3% of our open rooms globally, about 6% of our pipeline and last year represented about 3% of our global gross fees.
Your intuition is right as we start to take an early peek into what 2027 might look like. On one hand, we'll benefit once we get through the first quarter from relatively easier comps. We're currently assuming ongoing travel disruption with some gradual improvement during the course of 2027. I wish I had a better crystal ball. It's obviously a highly volatile situation. But what I will tell you is we are not seeing fallout from the pipeline, whether it be in the Middle East or on a global basis, that is anywhere close to outside what we have experienced around the world in normal circumstances.
I will tell you, I was in Dubai for a few days last week. I had dinner with 65 of our UAE general managers who expressed an enormous amount of confidence in the steepness of the recovery curve when they get a sense in the region that there is some stability or resolution to the conflict.
And the other thing I would tell you, you asked about pipeline and NUG. Just last week, I was with our local partners and the Ruler of Ras Al Khaimah signing 3 new deals in that Emirate. And so the teams continue to move projects forward. Our owner community continues to invest based on their long-term confidence in the region.

**Operator** (Operator):
And our next question will come from Dan Politzer with JPMorgan.

**Daniel Politzer** (Analysts):
I just wanted to follow up again on the 2027 kind of early puts and takes as you think about that 3.5% to 4.5% RevPAR growth. Could you maybe unpack that across business, leisure and then kind of where group is pacing?

**Anthony Capuano** (Executives):
Yes. I would love to, Dan. We're just not there yet. We are early in the budget process, as I mentioned. We are giving you a sneak peek into what we're hearing having just gone through our quarterly business reviews around the world. But we're probably a month or 2 premature to be able to give it to you with the sort of specificity that you're looking for.

**Operator** (Operator):
And our next question will come from Lizzie Dove with Goldman Sachs.

**Elizabeth Dove** (Analysts):
Going back to net rooms growth, you mentioned that conversions are about (sic) [ above ] 40% of openings and that you're capturing a disproportionate share of those opportunities. How do you think about that environment? We've heard mixed things this earnings season and the impact of higher rates there and other dynamics. And as we look into kind of next year and beyond, should we think about conversions as being a bigger or kind of smaller part of net rooms growth?

**Anthony Capuano** (Executives):
Yes. Lizzie. Thank you. I love the question. I spent a big portion of my career leading the company's development organization. And for a long time, you used to see the relative volume of new builds and conversions ebb and flow based on the macroeconomic environment. In strong economic environments, you'd see a big uptick in new build and you'd see conversion activity start to recede a bit, and then that would invert in weaker economic times.
As I've talked about on the last few calls, we've been quite deliberate in terms of how we think about conversions. And what I mean by that, we've built what we think is an extraordinary stack of conversion-friendly brands. We are aligned between our development organization and our operating organization to show not at the expense of quality, but a level of creativity and flexibility in deal making. We have development teams who are specifically focused on driving conversion volume, both in the categories of individual asset conversions and portfolio conversions, which has been a tremendous success story for us.
And so my expectation is while the percentages may move around a little bit, even when we get to an environment where we see a meaningful uptick in new build, I don't anticipate that it will be at the expense of conversion volume. We've built this super tanker that's really built to take advantage of the wide range of conversion opportunities that are out there, and we intend to continue to stand on that accelerator.
And then the last thing I would say to you is, as we've discussed, we are in our relative infancy of entering the mid-scale tier. It's going great between open and pipeline. We're already approaching 600 hotels in the system. But it's early. And what that earliness demonstrates to me is we've got lots and lots of conversion opportunities to be discovered in that quality tier as well.

**Operator** (Operator):
And our next question will come from Brandt Montour with Barclays.

**Brandt Montour** (Analysts):
So Tony, I was hoping you could give us a little bit of a state of the union on the China business. You called out slowing domestic leisure demand over there. But remind us the split between business and leisure, if you have a view on maybe the near- to medium-term operating outlook and then if that's affected capital formation at all and how that affects, yes, the net rooms growth outlook there?

**Anthony Capuano** (Executives):
Sure. Let me talk sort of broadly, and I might ask Jen to jump in with some statistics. We went from negative in RevPAR to essentially flat. We continue to see pretty good strength in the lower chain scales, both in terms of development activity and relative performance. We continue to see pretty broad strength across what we call the Tier 1 markets, and you heard me talk about Hainan and Taiwan and some of the other Tier 1 markets that are driving particularly strong performance. But Jen, do you want to talk a little bit about mix between segments in China?

**Jennifer Mason** (Executives):
Yes. So broadly speaking, in Greater China, our leisure segment is the largest segment followed by business and then group. In terms of performance, I'd say group, at least for the quarter was a bit less of the mix than leisure and business transient. But overall, to Tony's point, right, it's kind of a softening of consumer sentiment and spending and the environment is certainly difficult in terms of growth.

**Operator** (Operator):
And our next question will come from Duane Pfennigwerth with Evercore ISI.

**Duane Pfennigwerth** (Analysts):
Similar question, different region. I wonder if you could weigh in on what is driving what seems to be acceleration in European RevPAR. Is this primarily a seasonal leisure dynamic with U.S. point-of-sale demand? Or is there something else at work?

**Anthony Capuano** (Executives):
Well, without question, leisure is sort of the bright shining star, particularly when you look at Western and Southern Europe. Beyond that, you almost have to go submarket by submarket to look at the relative contribution from each segment. But if your question is for a broad generalization, I would say leisure is among the most impactful drivers of our RevPAR performance.

**Operator** (Operator):
And our next question will come from Robin Farley with UBS.

**Robin Farley** (Analysts):
Thank you for the early 2027 commentary. Just kind of circling back to...

**Anthony Capuano** (Executives):
That was for you, Robin. I knew you'd want. So I pushed Jen to make sure we gave you a little peek.

**Robin Farley** (Analysts):
Okay. Excellent. So drilling in on that, yes. So just looking at rooms under construction today in the release, they're a little bit lower than they were in July. And just the comments about conversion next year, it sounded like you were sort of saying conversion is going to stay like -- is going to be as good as new construction or maybe the suggestion was sort of like the same percent of room openings next year.
Is it -- would it actually -- should we think about conversions maybe being higher? I know they're elevated a little bit this year, but would they be higher next year just given the rooms under construction kind of just like slight downtick sequentially? Or I don't know if that's just something seasonal or onetime in nature?

**Anthony Capuano** (Executives):
You see, Robin, I give you an inch and you try and take a mile. I'm not quite ready to really give you much more of a peek into '27. But let me try at least qualitatively to address your question. The point I was trying to make, while I can't tell you with certainty what the percentage mix will be because a lot of that will be driven by whether we continue to see this continuation in an uptick in construction starts.
The point I was attempting to make was our focus, the focus of our teams on trying to continue to drive brand-accretive conversion volume, we won't let up. And so we would expect strong conversion volume, again, both single asset and portfolio to continue to be a top growth priority and a big driver of NUG into '27 and beyond.

**Operator** (Operator):
And our next question is from Conor Cunningham with Melius Research.

**Conor Cunningham** (Analysts):
Just on BT, I was a little surprised by the growth in the quarter. I thought it would be a little bit stronger just given what we've heard from some of the other travel companies. You can feel free to push back on that. But just curious on how you're viewing the corporate travel market, large, managed versus small and medium. And just I would suspect that the performance throughout the quarter was a little bit more diverse. So if you could just talk about how you started to how you ended, I think that would be helpful.

**Jennifer Mason** (Executives):
Yes. So I'll take that. We continue to see strength across all segments, right, both group, BT and leisure. BT revenue was up about 4% in the quarter, predominantly driven by rate growth. And we expect those trends will continue. Obviously, leisure was our strongest performer and continues to be so, and our group has also been strong this year as well. So we feel good across the segments and kind of across small, medium, large business.

**Operator** (Operator):
And we'll take our next question from Aryeh Klein with BMO Capital Markets.

**Aryeh Klein** (Analysts):
Tony, you touched a little bit on tech investments you've been making. Curious about the PMS rollout, where that stands and what kind of impact you've seen so far?

**Anthony Capuano** (Executives):
Yes. Of course. It's a terrific story, and I think our global tech team will appreciate you asking the questions so that Jen and I can thank them in a public forum. As of yesterday, we had successfully moved more than 3,000 of our hotels to the new technology ecosystem. We've successfully achieved scale for our deployment wave size. Full waves will continue throughout 2027. We have largely finished deployment in a lot of our U.S. select service hotels. We've started to cut over some of the full-service hotels. So lots of good learnings there.
We were quite deliberate in starting with some of the, I say this in "simpler hotels" so that we could learn along the way. Now as we move into full service and luxury, there will be some additional layers of complexity, but our teams are well prepared to do that. And I think we're quite pleased both with the pace at which we're moving, the speed with which the integration is improving with every wave. And again, it's anecdotal as opposed to particularly statistically valid, but really encouraging about the on-property impact that we're seeing from the cutover.

**Operator** (Operator):
And we'll take our next question from Alex Brignall with Rothschild & Co.

**Alex Brignall** (Analysts):
Just one question, please. If we look at your fee growth and we strip out the year-on-year increase in credit card fees and then obviously, you've changed your residential fees, which is quite a meaningful change year-on-year, then your underlying fee growth is lagging net unit growth and RevPAR growth or put differently, there's a slight compression in your effective royalty rate if we looked at sort of gross system sales. Could you just talk about that?
And then in the context of FY '27, if you could give us anything on the trajectory of credit card fees and residential fees, so then we can have a think about what that royalty rate might do next year.

**Jennifer Mason** (Executives):
Yes. In terms of fee growth overall from -- to your question on royalties, franchise royalty and base fee royalty, there is no compression there. And we are pleased with the year-over-year growth in our franchise fees. In terms of 2027, as Tony's referenced, we are still early days in terms of giving any guidance yet on fee growth.

**Operator** (Operator):
And we'll take our next question from Chad Beynon with Macquarie.

**Chad Beynon** (Analysts):
On the leisure side, I wanted to ask about the booking window. Obviously, we've seen some really nice consistent strength. You kind of gave us a preview into '27. I don't think this has expanded, but can you just kind of drill into that a little bit and what we've seen from some of the elevated airline prices, if you think that will remain compressed?

**Anthony Capuano** (Executives):
Sure. So on the booking window, in Q3, the global average booking window was about 21 days. BT was at 17 days and leisure was about 24 days, which was relatively flat year-over-year. So not a dramatic change on any of those fronts.

**Operator** (Operator):
At this time, we have reached our allotted time for questions. So we'll take our final question from Smedes Rose with Citi.

**Bennett Rose** (Analysts):
I just wanted to ask if you could share a little more on the investment (sic) [ incentive ] management fees. What percent of the North American portfolio is generating fees for you? And if you're able to do, say, the midpoint of that RevPAR range for next year, would those properties continue to sort of "be in the money?" Or would the expenses that will also be going up next year, maybe mute that fee stream a little bit? Just kind of wondering how that might work.

**Jennifer Mason** (Executives):
Yes. So maybe I'll start with your second question first. Again, it's too early to give you a read on what incentive management fees would be next year as we need to work through our budgets certainly around the world. In terms of percentage of hotels earning incentive fees, that varies around the world, as I know we've talked about in the past. But kind of weighted average around the world, it's about over 60-some percent.

**Operator** (Operator):
At this time, I would like to now turn the call back over to Tony Capuano. Please go ahead.

**Anthony Capuano** (Executives):
Well, I want to thank you all again for your interest and your terrific coverage in Marriott. I wish you safe travels, and I look forward to seeing many of you at our analyst reception in New York in December. Thank you.

**Operator** (Operator):
Thank you. This brings us to the end of today's meeting. We appreciate your time and participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MAR_Q2_2026_Earnings_Call_20260803.md
- 2026-08-03｜CEO｜guidance：CEO 宣布將 2026 全年全球 RevPAR 財測上調至 3%～3.5%（原話："raising our full year 2026 guidance range to 3% to 3.5%"）
- 2026-08-03｜CFO｜guidance：第三季全球 RevPAR 預期成長 3.5%～4%（原話："global RevPAR is expected to increase 3.5% to 4%."）
- 2026-08-03｜CFO｜guidance：全年總費用收入預期上調至 60.3～60.6 億美元（原話："could rise 11% to $6.03 billion to $6.06 billion"）
- 2026-08-03｜CFO｜guidance：全年 IMF（獎勵管理費）預期年增 3%～5%（原話："IMF are now expected to rise 3% to 5% year-over-year."）
- 2026-08-03｜CFO｜guidance：全年調整後 EBITDA 預期成長 11%～12%（原話："Full year adjusted EBITDA could increase between 11% and 12%"）
- 2026-08-03｜CFO｜guidance：全年調整後稀釋 EPS 成長預期 16%～18%（原話："adjusted diluted EPS growth between 16% and 18%."）
- 2026-08-03｜CFO｜guidance：第三季調整後 EBITDA 預期成長 7%～9%（原話："Adjusted EBITDA is expected to increase 7% to 9%."）
- 2026-08-03｜CFO｜guidance：全年自有／租賃及其他淨收入指引 1.75～1.85 億美元，並計入 ITR 獎勵影響（原話："$175 million to $185 million in 2026"）
- 2026-08-03｜CFO｜guidance：全年 G&A 仍預期年增 1%～3%，下半年（尤其第四季）有時點效益（原話："G&A expense is still anticipated to increase just 1% to 3%"）
- 2026-08-03｜CFO｜guidance：2026 全年投資支出上調至 12.5～13.5 億美元（原話："$1.25 billion to $1.35 billion, an increase versus our prior"）
- 2026-08-03｜CEO｜guidance：全年淨房數成長較可能落在原 4.5%～5% 區間的低端，主因中東工程延誤（原話："towards the low end of our previous 4.5% to 5% range"）
- 2026-08-03｜CFO｜guidance：全年信用卡費用預期成長高 30% 區間（含新約，部分被日圓貶值抵銷）（原話："credit card fees to rise in the high 30% range"）
- 2026-08-03｜CFO｜guidance：管理層提示第四季美加不再有世足賽加持（原話："a small negative impact from November's midterm elections"）
- 2026-08-03｜CEO｜guidance：CEO 談 2027：可能延續強勁的全球 RevPAR 成長，但提到時機尚早（原話："We could see continued strong global RevPAR growth next year"）
- 2026-08-03｜CEO｜guidance：CEO 指出 2027 EMEA 可望因中東復甦而強勁成長（原話："over-year growth in EMEA as the Middle East recovers"）
- 2026-08-03｜CFO｜guidance：CFO 描述 2027 團體訂房目前走勢：持平、價升量微降（原話："it looks flattish, rate up and room nights down slightly"）
- 2026-08-03｜CFO｜margin：第二季 IMF 6% 增至 2.12 億美元，美加大增抵銷 EMEA（中東）下滑（原話："rose 6% to $212 million in the second quarter"）
- 2026-08-03｜CFO｜margin：第二季自有／租賃及其他淨額下滑，管理層歸因於 2,700 萬美元訴訟應計等（原話："primarily due to a $27 million property-"）
- 2026-08-03｜CFO｜margin：ITR 獎勵由 Marriott 自行負擔、記入自有／租賃及其他費用，而非系統基金（原話："paid for by Marriott and not the system fund"）
- 2026-08-03｜CFO｜margin：ITR 獎勵規格：最高相當總客房收入 50 個基點的費用返還（原話："up to 50 basis points of gross room revenue"）
- 2026-08-03｜CFO｜margin：管理層說明 Q4 是中東全年營收最大的一季，並面對高基期 ADR（原話："35% of the Middle East full year revenue happens in Q4"）
- 2026-08-03｜CFO｜margin：管理層量化中東對全年全球 RevPAR 的拖累約 100 個基點（上季為 100～125）（原話："full year global RevPAR to be about 100 basis points"）
- 2026-08-03｜CFO｜margin：世足賽對全年全球 RevPAR 的貢獻上修為約 45 個基點（原 30～35）（原話："closer to 45 basis points globally"）
- 2026-08-03｜CEO｜margin：第二季中東 RevPAR 大幅下滑 43%，略優於預期（原話："Middle East RevPAR declined 43% in the quarter"）
- 2026-08-03｜CEO｜margin：美加第二季 RevPAR 成長 5%，為 13 季以來最高（原話："the highest quarterly increase in 13 quarters"）
- 2026-08-03｜CFO｜margin：2026 全年團體訂房 pace 約 +5%，與上季相同（原話："Full year group pace is up about 5%."）
- 2026-08-03｜CFO｜commitment：管理層重申資本配置原則未變（原話："Our capital allocation philosophy has not changed."）
- 2026-08-03｜CFO｜commitment：2026 年預計回饋股東超過 45 億美元（原話："return over $4.5 billion to shareholders in 2026."）
- 2026-08-03｜CEO｜commitment：CEO 量化新信用卡約對 2028 全年共品牌卡費用的影響為 1～1.25 億美元（版稅率 26%）（原話："somewhere between $100 million and $125 million"）
- 2026-08-03｜CEO｜commitment：CEO 重申未來數年淨房數維持中個位數成長（原話："in line with the broad guidance we've provided"）
- 2026-08-03｜CFO｜commitment：科技轉型（DTT）相關支出管理層預期長期會下降，但持續投資科技（原話："On tech and DTT spend, that over time will go down"）
- 2026-08-03｜CFO｜capital_allocation：管理層預期 key money 隨系統規模成長而增加（原話："key money grow with that"）
- 2026-08-03｜CFO｜capital_allocation：管理層說明投資支出組成：合約取得成本占 40%～45%（原話："Contract acquisition costs are now expected to be around"）
- 2026-08-03｜CEO｜capital_allocation：CEO 稱 key money 為競爭中常見的武器，且已出現在新中階品牌（原話："key money seems to be the weapon of choice"）
- 2026-08-03｜CEO｜competition：CEO 稱新中階品牌開始少量使用 key money（原話："we are seeing some small amounts of key money being used"）
- 2026-08-03｜CEO｜competition：CEO 稱相較同業，Marriott 談判的 key money 較少（自述為軼事觀察）（原話："negotiate a bit less key money than some of our peers"）
- 2026-08-03｜CEO｜competition：CEO 回應中階品牌 RevPAR 轉強是否降低業主對品牌需求：稱觀察相反（原話："what we see and what we hear from the owner community"）
- 2026-08-03｜CEO｜customer：CEO 以首半年簽約量創歷史新高說明業主信心（原話："we signed more deals in the first half of 2026, than in any"）
- 2026-08-03｜CEO｜customer：年初起忠誠計畫 charge-out 費率下調約 5%（管理層稱為業界最低）（原話："charge-out rates across our global system by roughly 5%"）
- 2026-08-03｜CEO｜product：全球開發管線創新高，約 62.9 萬間（原話："a new record of approximately 629,000 rooms"）
- 2026-08-03｜CEO｜product：轉換案占上半年簽約 34%、開業 40%（原話："34% of signings and 40% of openings"）
- 2026-08-03｜CEO｜product：CEO 說明大中華將導入 Series by Marriott，約 100 間（原話："add approximately 100 hotels under this collection brand"）
- 2026-08-03｜CEO｜product：CEO 不認為景氣好轉、新建案回升會以轉換案為代價（原話："believe that will be the trend going forward"）
- 2026-08-03｜CEO｜product：AI：與 Google 等 AI 平台合作，因應旅遊搜尋與商務工具演進（原話："leading AI platform providers as their travel search"）
- 2026-08-03｜CEO｜risk：CEO 承認業主社群來信（owner letter）並稱雙方討論中，但不公開回應（原話："I'm not going to give an official response"）
- 2026-08-03｜CEO｜risk：被問及費用轉嫁與自行吸收比重，CEO 稱財測已反映討論對 P&L 的預期影響（原話："guidance is reflective of our expectations of the impact"）

### 問答異常語氣（迴避／改口／保留）
- MAR_Q2_2026_Earnings_Call_20260803.md｜問：Truist 的 Scholes 請 CEO 對業主公開信（owner letter）給出具體正式公開回應｜答法：CEO 明確表示不給官方回應，改談業主與 Marriott 利益相連、已開過多次會議、對進展感到鼓舞，未給具體內容或數字
- MAR_Q2_2026_Earnings_Call_20260803.md｜問：Jefferies 的 Katz 詢問平台費／報銷項目的調整，以及 Marriott 轉嫁與自行吸收的比重｜答法：CEO 只稱討論『collaborative and constructive and ongoing』，並說財測已反映預期影響，未拆分轉嫁與吸收金額
- MAR_Q2_2026_Earnings_Call_20260803.md｜問：JPMorgan 的 Politzer 詢問未來幾年淨投資支出走向｜答法：CFO 稱談 2027 太早，僅對各類別給方向性描述（科技支出長期下降、key money 隨規模增加），未給數字

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
{"date":"20260710","verdict":"觀望","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"全球旅遊需求後疫情正規化，RevPAR 維持低單位數正成長","columns":{"2Y 驗證點":"FY26-27 全球 RevPAR 2-3%","5Y 驗證點":"穿越一次完整需求週期仍正","10Y 驗證點":"10Y RevPAR CAGR ≥ 2%","具體數字門檻":"全球 RevPAR YoY ≥ 1.5%（floor，2026 guide 下緣）；國際 RevPAR ≥ 4%","來源":"MAR Q1 FY26 release 2026-05-06（全球 +4.2%／US +4.0%／intl +4.6%）；PwC US Hospitality Directions May 2026（2026 RevPAR ~2.8%）","漂移觸發":"連 2 季全球 RevPAR YoY"}},{"id":"H2","text":"資產輕模式下 pipeline 持續轉化為淨房間成長 ≥ 4%，推動 fee revenue 有機成長","columns":{"2Y 驗證點":"淨房間 +4.5-5%、pipeline ≥ 600K","5Y 驗證點":"fee revenue 5Y CAGR ~7-8%","10Y 驗證點":"系統規模再擴 ~40-50%（國際轉化）","具體數字門檻":"淨房間成長 ≥ 4%（floor，當前 +4.5%）；pipeline ≥ 600K（當前 618K）；Bonvoy 會員淨增 > 0","來源":"MAR Q1 FY26（pipeline 618K，conversions 40% openings）；MAR IR FY30 target","漂移觸發":"淨房間"}},{"id":"H3","text":"估值不進一步擴張，但在品質溢價支撐下維持 Forward PE 24-31x 區間","columns":{"2Y 驗證點":"Fwd PE 維持 24-31x（不跌穿 22x）","5Y 驗證點":"倍數均值回歸至 ~26-27x（5Y 均）","10Y 驗證點":"倍數守住複利級（非收租級","具體數字門檻":"Fwd PE(FY+2) 24-31x；分析師中位 PT ≥ $340（floor，當前中位 $381-394）","來源":"yfinance / 分析師共識 2026-07；5Y PE 分布","漂移觸發":"Fwd PE 連 6 月 5% → 反轉（估值燈 🟠→🟡→進場機會）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"全球衰退壓制旅遊需求，RevPAR 轉負 2-3 季，fee revenue 下滑；同時倍數 de-rate（樞紐變數，同打 H1+H3）","columns":{"對應假設":"H1 / H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"全球 RevPAR YoY；商務差旅指標；Fwd PE","警戒閾值":"RevPAR 連 2 季"}},{"id":"R2","text":"淨房間成長份額流失——Hilton/Hyatt 淨單位成長 6-7% 持續領先 MAR 的 4.5-5%，pipeline 轉化放緩或加盟商離心","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"淨房間成長；signings/openings 比；vs peer NUG 差距","警戒閾值":"淨房間 3pp 連 2 半年"}},{"id":"R3","text":"AI travel agent 去中介化 + OTA 佣金侵蝕削弱 Bonvoy 直訂護城河，忠誠度溢價壓縮，倍數收租化","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Bonvoy 直訂/會員房晚份額；直訂率；AI 訂房平台市佔","警戒閾值":"會員房晚份額連 2 半年"}},{"id":"R4","text":"資料隱私監管拖尾——20 年 FTC consent order 合規成本 + 消費者集體訴訟（44M 消費者、6 州，MAR + Accenture）判賠或和解放大","columns":{"對應假設":"H1（間接）","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"consumer class action docket；合規費用","警戒閾值":"不利集體認證 + 大額和解（> 市值 1%）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE(FY+2) 回落至 ~24x（~$310）或全球 RevPAR 連 2 季轉負（衰退重置）；或 Fwd PE 連 6 月 <22x 且分析師目標中位下修","irr_base_pct":5.5,"ev5y_pct":24.2,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"核心","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.3,"ev5y_pct":24.2,"irr_base_pct":5.5,"max_dd_pct":-55.0,"bull_5y_price":670.0,"bear_5y_price":266.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE(FY+2) 回落至 ~24x（~$310）或全球 RevPAR 連 2 季轉負（衰退重置）；或 Fwd PE 連 6 月 <22x 且分析師目標中位下修","price_at_dd":372.47,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MAR_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
