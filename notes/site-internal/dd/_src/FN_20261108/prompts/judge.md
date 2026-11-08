你是 stock-analyst **v20 判斷 agent**，標的 FN（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"FN","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1474.5,"period":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","citation":"FN Q1 FY27 新聞稿（8-K Ex.99.1）"},"note":"新聞稿稱超出公司指引區間；共識數字未查證"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":158.5,"period":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","unit":"百萬美元（利益率 10.8%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","citation":"FN Q1 FY27 新聞稿（8-K Ex.99.1）"},"note":"未查證"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":146.0,"period":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","unit":"百萬美元（利益率 9.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","citation":"FN Q1 FY27 新聞稿（8-K Ex.99.1）"},"note":"未查證"},{"id":"f_kpi5_q2_fy2027_2026_12_25","label":"下一季指引（Q2 FY2027，季末 2026-12-25）","value":"營收 1,600–1,650 百萬美元；GAAP EPS 3.81–3.96；non-GAAP EPS 4.77–4.92（約 36.2 百萬稀釋股）","period":"Q1 FY2027（公告於 2026-11-02）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027（公告於 2026-11-02）","citation":"FN Q1 FY27 新聞稿（8-K Ex.99.1）"},"note":"指引中點營收 1,625，約較 Q1 +10.2% QoQ；共識未查證"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-02","period":"2026-11-02","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-02"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_fn_gross_margin_pct","label":"FN 毛利率","value":11.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fn_operating_margin_pct","label":"FN 營業利益率","value":10.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fn_fcf_margin_pct","label":"FN FCF 利潤率","value":-3.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cls_gross_margin_pct","label":"CLS 毛利率","value":11.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cls_operating_margin_pct","label":"CLS 營業利益率","value":8.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cls_fcf_margin_pct","label":"CLS FCF 利潤率","value":2.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_jbl_gross_margin_pct","label":"JBL 毛利率","value":9.23,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_jbl_operating_margin_pct","label":"JBL 營業利益率","value":5.11,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_jbl_fcf_margin_pct","label":"JBL FCF 利潤率","value":3.82,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_lite_gross_margin_pct","label":"LITE 毛利率","value":45.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lite_operating_margin_pct","label":"LITE 營業利益率","value":23.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lite_fcf_margin_pct","label":"LITE FCF 利潤率","value":9.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_gross_margin_pct","label":"COHR 毛利率","value":38.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_operating_margin_pct","label":"COHR 營業利益率","value":14.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_fcf_margin_pct","label":"COHR FCF 利潤率","value":-23.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_non_gaap_fcf","label":"自由現金流（non-GAAP FCF）","value":-137.4,"period":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","citation":"FN Q1 FY27 新聞稿（營業現金流 21.3 − 資本支出 158.7）"},"note":"n/a"},{"id":"f_kpi4_sbc_non_gaap","label":"SBC 占 non-GAAP 營業利益","value":7.1,"period":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","unit":"%（SBC 11.2 百萬；占營收 0.76%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）","citation":"FN Q1 FY27 新聞稿（SBC 11,225 千：銷貨成本 4,203＋SG&A 7,022；除以 non-GAAP 營業利益 158.5 自行計算）"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":327.13,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-47.35,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":42.93,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.97,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.53 → 19.72）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.56,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.74 → 24.11）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（29.74 → 29.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":19.72,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":24.11,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":29.74,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":42.8,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 13.81 → 19.72（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":24.69,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝29.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":29.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.27,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝23.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":23.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.14,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝20.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":20.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":16.59,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 19.72，分子＝快照價 327.13","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-677.43,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 78.32、現金 755.75（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":35.72,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":11006.84,"period":"2026-11-08","unit":"USD m","basis":"市值 11684.27 ＋ 淨負債 -677.43","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6596.57,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":8072.31,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（7 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.67,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 327.13 / W52 505.94 / W104 388.86 / W250 249.7 / W250 13週斜率 1.4%"},{"id":"f_ma_w52","label":"52 週均線","value":505.94,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":388.86,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":249.7,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.4,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列出光學製造服務對手含 Benchmark、Celestica、InnoLight、Jabil、Sanmina、Venture、Eoptolink 及客戶自製能力；公司稱進入門檻高（銷售週期長、須證明精密光電製造能力、保護客戶 IP）","source":"SEC EDGAR 10-K FY2026 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"Competitors in the market for optical manufacturing services include Benchmark Electronics, Inc., Celestica Inc., InnoLight Technology (Suzhou) Ltd., Jabil Inc., Sanmina Corporation, Venture Corporation Limited and Eoptolink Technology Inc., Ltd., as well as the internal manufacturing capabilities of our customers.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：其他代工、ODM 或封測公司可能進入目標市場，產業整併可能產生更大對手；新競爭可能導致降價、毛利下降或失去份額","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"Other existing contract manufacturing companies, original design manufacturers or outsourced semiconductor assembly and test companies could also enter our target markets.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素揭露：客戶整併在部分情況下已導致需求下降，因客戶取得自製產能（in-house）；未點名最大客戶正在自製或導入第二供應商。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"In some cases, consolidation among our customers has led to a reduction in demand for our services as customers have acquired the capacity to manufacture products in-house.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K MD&A：公司依賴少數客戶，任一大客戶減單或流失會有重大不利影響。","source":"SEC EDGAR 10-K FY2026 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"Because we depend upon a small number of customers for a significant percentage of our total revenues, a reduction in orders from, a loss of, or any other adverse actions by, any one of these customers would reduce our revenues and could have a material adverse effect on our business, operating results and share price.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"0","claim":"搜尋未找到最大客戶（Nvidia）正導入第二供應商或將Fabrinet環節自製的具名報導或公告；FY2025 10-K 顯示 Nvidia 占 27.6%、Cisco 18.2%。","source":"SEC EDGAR 10-K FY2025（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871025000039/fn-20250627.htm","excerpt":"During fiscal year 2025, NVIDIA Corporation and Cisco Systems, Inc. contributed 27.6% and 18.2%, respectively, of our revenues.","as_of":"2025-08-15","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026（截至2026-06-26）10%以上客戶：Cisco 19.9%、NVIDIA 16.3%、Nokia 10.7%、Amazon 10.5%；NVIDIA 占比由FY2024的35.1%、FY2025的27.6%降至16.3%，Cisco由13.4%升至19.9%。","source":"SEC EDGAR 10-K FY2026 Item 8 Significant customers","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"Cisco Systems, Inc. 19.9 % 18.2 % 13.4 % NVIDIA Corporation 16.3 % 27.6 % 35.1 % Nokia Corporation 10.7 % * * Amazon.com, Inc. 10.5 % * *","as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2026-06-26應收帳款集中：Cisco 16.1%、Nokia 14.2%、Amazon 11.5%；NVIDIA 前一年25.5%，本年低於10%。","source":"SEC EDGAR 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"Cisco Systems, Inc. 16.1 % 13.7 % Nokia Corporation 14.2 % 12.0 % Amazon.com, Inc. 11.5 % * NVIDIA Corporation * 25.5 %","as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"公司10-K風險因素揭露：客戶集中增加應收帳款集中與客戶違約風險；許多客戶負債重或財務困難，部分客戶曾倒閉、破產或退出光學市場（為一般性揭露，未點名特定客戶惡化）。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"Further, our customer concentration increases the concentration of our accounts receivable and our exposure to payment default by any of our key customers. Many of our existing and potential customers have substantial debt burdens, have experienced financial distress or have static or declining revenues","as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"FN 財報 Q3 FY2026 call：Datacom 出貨受廣泛零組件短缺限制，儘管需求極強","source":"Motley Fool FN Q3 2026 earnings transcript","url":"https://www.fool.com/earnings/call-transcripts/2026/05/04/fabrinet-fn-q3-2026-earnings-transcript/?.tsrc=rss","excerpt":"Management highlighted that \"shipments and revenue were well below demand levels\" in datacom due to component supply shortages in lasers, memory, and ASICs, which \"is not demand risk;","as_of":"2026-05-04","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FN FQ4 2026 營收創高約 13.2 億美元、年增 45%，FQ1 2027 指引 13.8–14.3 億","source":"Sentisense: Fabrinet Posts Record Q4 2026 Revenue","url":"https://app.sentisense.ai/stories/fabrinet-posts-record-q4-2026-revenue-beats-estimates-but-shares-slip-08182026","excerpt":null,"as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Utmel 2026 Q4 報告：市場為結構性分化而非 2021 式短缺","source":"Utmel 2026 Q4 Electronic Components Market Analysis Report","url":"https://www.utmel.com/blog/categories/semiconductor/2026-q4-electronic-components-market-analysis-report-supply-pricing-and-procurement-outlook","excerpt":"This Q4 2026 electronic components market analysis examines the structural supply bifurcation behind projected US$975 billion semiconductor revenues.","as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2026 10-K Item 3 only discloses a PRC unjust-enrichment suit against Casix (RMB 400 million claimed); PRC Supreme Court accepted retrial on 2026-07-30, no merits determination, liability not quantifiable. No antitrust/DOJ/FTC matter listed.","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"The acceptance of the case for retrial does not represent a determination on the merits of the Plaintiffs' claims. At this time, we are not able to quantify any potential liability in connection with this litigation because of the early stage of this litigation.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 揭露公司與供應商可能受關稅、禁運等貿易限制影響，可能限制材料供應並推高成本，且已經歷較長交期與加急費。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"We and our suppliers and service providers could be affected by tariffs, embargoes, or other trade restrictions, as well as laws and regulations enacted in response to concerns regarding climate change, conflict minerals, responsible sourcing practices, public health crises, contagious disease outbreaks, or other matters, which could limit the supply of our materials and increase their cost.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：公司受泰國、中國、以色列、美國出口進口管制；美國對中國的技術出口禁令可能延伸至泰國，限制其製造某些產品。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"The export of certain technologies from the United States and other nations to the PRC is barred by applicable export controls, and similar prohibitions could be extended to Thailand, thereby limiting our ability to manufacture certain products.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：關稅雖部分調降或延後，但再升級風險仍在；若無法轉嫁成本，毛利率與業績可能受重大不利影響。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"Although certain tariffs have been reduced or delayed, the potential for future escalation or the imposition of new trade restrictions remains.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2026 北美以外出貨地客戶占營收 77.3%，主要製造設施在泰國；福州有客製光學廠。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"Revenues from the ship-to-location of customers outside of North America accounted for 77.3%, 78.4% and 81.8% of our revenues for fiscal year 2026, fiscal year 2025 and fiscal year 2024, respectively.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2026-09 10-Q 提到 CBP 已宣布關稅退款行政程序的步驟（公司預期金額未述）。","source":"SEC EDGAR 10-Q (period ended 2026-09-25)","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000041/fn-20260925.htm","excerpt":"Customs and Border Protection has since announced steps toward an administrative process to address potential tariff refunds.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q 稱多數資產與製造營運位於泰國，泰國政治、社會、經濟狀況對業務有重大影響；未來政治不穩可能阻礙出貨、中斷製造","source":"Fabrinet Form 10-Q (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000041/fn-20260925.htm","excerpt":null,"as_of":"2026-09-25","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K 稱預期持續投資中國製造營運，須承擔當地經營風險；出口管制（泰國、中國、以色列、美國）與新增或提高關稅列為風險","source":"Fabrinet Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000028/fn-20260626.htm","excerpt":null,"as_of":"2026-06-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"早期 10-K（FY2019）稱關鍵材料依賴單一或有限供應商；10-Q 稱為某客戶採購的多數材料通常無法用於其他客戶產品","source":"Fabrinet Form 10-K FY2019 / 10-Q (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1408710/000119312519225268/d766673d10k.htm","excerpt":null,"as_of":"2019-08-23","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 營收 $4,641.1M（FY2025 $3,419.3M，+36%）；自 Q4 FY26 起改分 data center／communications infrastructure／automotive, industrial and other。automotive/industrial/other FY26 $869.6M（占 18.8%，FY25 23.1%）。","source":"Fabrinet Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000028/fn-20260626.htm","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 FY26：data center 營收 $669M，YoY +68%、QoQ +13%，占 51%；communications infrastructure $413M，YoY +40%、QoQ +1%，占 31%。","source":"Nasdaq, Fabrinet Q4 Earnings Call Highlights","url":"https://www.nasdaq.com/articles/fabrinet-q4-earnings-call-highlights","excerpt":null,"as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"FY26 單一客戶占營收 ≥10%：Cisco 20%、Nvidia 16%、Nokia 11%、Amazon 11%。","source":"Fabrinet Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000028/fn-20260626.htm","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q1 FY27 營收 $1.474B，YoY +51%；Q2 FY27 指引 $1.6–1.65B；產能預計 1 月達約 $10B（FY26 底約 $5.8B）；客戶預測提供 FY27 後能見度但非確定訂單；NPO 預計 FY27 下半年貢獻。","source":"MarketBeat, Fabrinet Q1 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-fabrinet-q1-earnings-call-highlights-2026-11-02/","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Zacks 報導：Fabrinet 手上 1.6T 訂單逾 $200M，預期 2026 年第四季 1.6T 營收逾 $70M；hyperscaler-direct transceiver 專案預計下季開始放量；競爭者列 Lumentum、AAOI。未查到市佔或價格趨勢數字。","source":"Zacks/Nasdaq, FN's AI Optical Growth Accelerates: Can It Challenge LITE & AAOI?","url":"https://www.nasdaq.com/articles/fns-ai-optical-growth-accelerates-can-it-challenge-lite-aaoi","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"第三方 Porter 五力分析稱 CPO 等新技術可能改變價值鏈，且大客戶（如 NVIDIA）自行製造為持續風險；非公司一手文件。","source":"dcf-analysis.com｜Fabrinet (FN): 5 FORCES Analysis [Apr-2026 Updated]","url":"https://dcf-analysis.com/products/fn-porters-five-forces-analysis","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"第三方分析指出，若全電短距連結取代部分 AI 應用的光學，Fabrinet 可服務市場可能縮小；CPO 與 linear-drive pluggable 可能擾動現有組裝製程、需新能力或資本。","source":"statementdog.com 與第三方個股分析（搜尋摘要）","url":"https://statementdog.com/analysis/FN","excerpt":null,"as_of":"2026-03-25","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"公司已與三家客戶進行 CPO 相關合作並少數股權投資 Raytek Semiconductor；另有報導稱 CPO 原型測試對應 2027–2028，尚非主要營收來源。CPO 對公司同時是機會。","source":"Finviz/Yahoo：Fabrinet Eyes 800ZR and Co-Packaged Optics as Growth Catalysts","url":"https://finviz.com/news/327428/fabrinet-eyes-800zr-and-co-packaged-optics-as-growth-catalysts","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"搜尋未在 FY2026 10-K 找到明文寫 CPO 取代其收發器業務的風險語言；10-K 競爭因素列「參與新興技術成長的工程能力」。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"our ability to strengthen and broaden our engineering services and know-how to participate in the growth of emerging technologies;","as_of":"2026-08-18","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 描述 Fabrinet 仍是 OEM 客戶的外包製造夥伴，多數產品為唯一外包製造商；業態為代工，未見訂閱／D2C／平台化轉型描述。","source":"SEC EDGAR 10-K FY2026 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"In many cases, we are the sole outsourced manufacturing partner used by our customers for the products that we manufacture for them.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 第四季起地理別揭露由客戶帳單地改為出貨地，屬揭露口徑變更，非通路變化；另營收分類改為三類。","source":"SEC EDGAR 10-K FY2026 / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000028/fn-20260626.htm","excerpt":"Beginning in the fourth quarter of fiscal year 2026, the Company updated its geographic area presentation from the bill-to-location of its customers to the ship-to-location of its customers","as_of":"2026-08-18","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ1'27 (2026-11-02) 8-K：公司給 FQ2'27（至 2026-12-25）營收指引 $1.6B–$1.65B、non-GAAP EPS $4.77–$4.92（搜尋摘要轉述，未逐字取得原文）","source":"SEC 8-K Exhibit 99.1 Q1 FY2027 (via search summary)","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000034/fn-20261102xex991q127.htm","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-17 FQ4 財報：non-GAAP EPS $4.10 vs 共識約 $3.79–3.81；FQ1'27 指引 EPS $4.10–4.25 高於共識 $3.95，營收指引約 $1.38–1.43B 高於共識約 $1.3B（聚合站數字略有不一致）","source":"MarketBeat / Benzinga (via search summary)","url":"https://www.marketbeat.com/instant-alerts/fabrinet-nysefn-issues-q1-2027-earnings-guidance-2026-08-17/","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布因來源與日期差異大：stockanalysis 快照（11-02 財報後）9 位分析師平均 $624.33；MarketBeat（2026-05）平均 $664.25、5 Buy/5 Hold；Investing.com 平均約 $734（7 Buy 2 Hold）；Benzinga 平均 $413（13 位，疑似過期）；個股：JPMorgan 降評至 Neutral 目標 $700、Rosenblatt $750 Buy、Needham $800 Buy；另有未註明日期的下調（JPMorgan $465、B. Riley $385、Susquehanna $600）","source":"stockanalysis / MarketBeat / Investing.com / Benzinga (via search summary)","url":"https://stockanalysis.com/stocks/fn/forecast/","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-05 FQ3 後 Northland 微降 Q1'27 EPS 估計但上調 FY2027 EPS 至 $17.23","source":"MarketBeat Northland Securities","url":"https://www.marketbeat.com/instant-alerts/northland-securities-expects-weaker-earnings-for-fabrinet-2026-05-08/","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"子公司 Casix 的中國不當得利訴訟（求償 RMB 4 億）：2025-11 二審駁回，2026-04 原告上訴最高人民法院，2026-07-30 最高院裁定受理再審；受理不代表實體判斷，公司無法量化潛在負債。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"In April 2026, the Plaintiffs appealed the Appellate Court’s ruling to the Supreme People’s Court of the People’s Republic of China (the “PRC Supreme Court”). The PRC Supreme Court held an initial hearing on July 2, 2026 and, on July 30, 2026, rendered a ruling accepting the case for retrial. The acceptance of the case for retrial does not represent a determination on the merits of the Plaintiffs' claims.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 5 份 8-K 中僅 1 份含重大項目（2026-08-17 Item 1.01：泰國子公司與 Bank of Ayudhya 修改授信並借入 THB 25 億定期貸款，用於資本支出）。","source":"SEC EDGAR 8-K 清單；8-K 2026-08-17 Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000026/fn-20260811.htm","excerpt":"The proceeds of the Term Loan, together with cash on hand, were used to support the Company’s capital expenditures.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-03-25 同意以約 NT$10.2 億（約 $3,240 萬）取得 Raytek Semiconductor 16.0% 股權，為少數股權投資、成本法；搜尋未見 Fabrinet 本身被併購或大型併購。","source":"SEC EDGAR 10-Q FY2026（截至 2026-03-27）","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000016/fn-20260327.htm","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"ems_utilization_capex_cycle#0","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"FQ1'27 財報會議（2026-11 初）：Building 10 接近完工、部分已貢獻營收；預期 1 月底總營收產能約 $100 億（FY26 底約 $58 億）；Building 10 約增 $35 億產能，Navanakorn 約 $4 億、Santa Clara 擴建約 $3 億。","source":"MarketBeat, Fabrinet Q1 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-fabrinet-q1-earnings-call-highlights-2026-11-02/","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"ems_utilization_capex_cycle#1","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"-","claim":"Building 11（Chonburi）預計 Building 10 完工後（1 月）動工，約 150 萬平方呎、增約 $30 億營收產能，預計 FY2028 底前後完工；另有來源稱含潛在 Building 12 總產能目標由 $140 億升至 $160 億。","source":"MarketBeat, Fabrinet Q1 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-fabrinet-q1-earnings-call-highlights-2026-11-02/","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"ems_utilization_capex_cycle#2","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"-","claim":"FY2026 營收 +36% 至 $46 億，營運現金流 $2.57 億、自由現金流僅 $400 萬，因持續投入產能；capex 季度升至 $1.69 億（含 $7,700 萬 Santa Clara 第二園區收購），FY2027 計畫提高資本支出。","source":"Nasdaq, Fabrinet Q4 Earnings Call Highlights; MarketBeat Q1 call highlights","url":"https://www.nasdaq.com/articles/fabrinet-q4-earnings-call-highlights","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"ems_utilization_capex_cycle#3","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"搜尋未找到 Fabrinet 公布的稼動率數字；分析師稱 FQ1 是首次觀察 Building 10 稼動率的時點，新空間稼動率尚未揭露。","source":"Nasdaq/MarketBeat 搜尋摘要（Q4 FY26 call highlights）","url":"https://www.nasdaq.com/articles/fabrinet-q4-earnings-call-highlights","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ems_utilization_capex_cycle#4","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"EMS 產業 2026 年元件（記憶體等）供應瓶頸再現，可能使產能閒置或增加緩衝庫存；未找到產業稼動率數據。","source":"Elisa IndustriQ, EMS Industry Update: Where the Market Sits Going Into 2026","url":"https://www.elisaindustriq.com/calcuquote/accelerate2026/ems-industry-update","excerpt":"Memory and select components are reappearing as supply-chain bottlenecks","as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#0","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"opencapital.sh 顯示 FN ROIC 23.7%（Q1 2026）；同站同業 Celestica 約 39.5%、Jabil 29.8%（Q4 2025）、Flex 19.2%、Sanmina 11.3%、Benchmark 5.4%（Q2 2026）；口徑為稅後營業利益／(平均負債＋權益−現金)，各頁期間不一致、非同口徑。stockanalysis 顯示 FN 約 30.53%，兩來源不一致。","source":"opencapital.sh metrics/roic 各標的頁（fn、cls、jbl、flex、sanm、bhe）；stockanalysis.com FN ratios","url":"https://www.opencapital.sh/stocks/fn/metrics/roic","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#1","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"資產週轉：FN 約 1.34–1.4x；同業 Flex 1.4x、Sanmina 1.5x、Jabil 1.6x（opencapital），FN 位於同業區間偏低端；Celestica 未取得。","source":"opencapital.sh asset_turnover；stockanalysis.com FN ratios","url":"https://www.opencapital.sh/stocks/fn/metrics/asset_turnover","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#2","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"-","claim":"FY2026 營運現金流 256.7M（FY2025 為 328.4M）；季度（截至 2026-09-25）營運現金流 21.3M 對去年同期 102.6M，公司歸因於應收帳款增加；現金及短投 875.1M、無負債。第三方 VCP Scanner 列 CCC 約 62–82 天、最新約 65.45（欄位期間未標，未核）。","source":"Fabrinet 10-K FY2026、10-Q 2026-09-25；VCP Scanner","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000041/fn-20260925.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-03-25 同意以約 NT$10.2 億（約 $3,240 萬）取得 Raytek Semiconductor 16.0% 股權，少數股權、成本法；未見大型併購或 Fabrinet 被收購。","source":"SEC EDGAR 10-Q FY2026（截至 2026-03-27）","url":"https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000016/fn-20260327.htm","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"唯一重大訴訟為子公司 Casix 的中國不當得利案（非集體訴訟）；2026-07-30 最高院受理再審，公司無法量化潛在負債。搜尋未見近 12 個月證券集體訴訟（僅 2014 年律所調查公告）。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm","excerpt":"The PRC Supreme Court held an initial hearing on July 2, 2026 and, on July 30, 2026, rendered a ruling accepting the case for retrial. The acceptance of the case for retrial does not represent a determination on the merits of the Plaintiffs' claims.","as_of":"2026-08-18","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"FN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.95,"operating_margin_pct":10.04,"fcf_margin_pct":-3.73,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FN","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CLS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.46,"operating_margin_pct":8.29,"fcf_margin_pct":2.99,"rd_intensity_pct":0.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"JBL","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.23,"operating_margin_pct":5.11,"fcf_margin_pct":3.82,"rd_intensity_pct":0.08},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL","as_of":"TTM ending 2026-08-31（4季加總）"}},{"name":"LITE","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.91,"operating_margin_pct":23.35,"fcf_margin_pct":9.52,"rd_intensity_pct":12.47},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"COHR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.16,"operating_margin_pct":14.11,"fcf_margin_pct":-23.28,"rd_intensity_pct":10.18},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"FN"},"financial_history":{"ticker":"FN","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":2645237000.0,"revenue_yoy_pct":null,"gross_margin_pct":12.71,"operating_margin_pct":9.78,"net_income":247913000.0,"diluted_eps":6.73,"free_cash_flow":151039000.0,"fcf_margin_pct":5.71,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":2882967000.0,"revenue_yoy_pct":8.99,"gross_margin_pct":12.35,"operating_margin_pct":9.63,"net_income":296181000.0,"diluted_eps":8.1,"free_cash_flow":364729000.0,"fcf_margin_pct":12.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":3419327000.0,"revenue_yoy_pct":18.6,"gross_margin_pct":12.09,"operating_margin_pct":9.53,"net_income":332527000.0,"diluted_eps":9.17,"free_cash_flow":206549000.0,"fcf_margin_pct":6.04,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":4641097000.0,"revenue_yoy_pct":35.73,"gross_margin_pct":11.99,"operating_margin_pct":9.98,"net_income":473027000.0,"diluted_eps":13.05,"free_cash_flow":3041000.0,"fcf_margin_pct":0.07,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/FN/FN_Q1_2027_Earnings_Call_20261102.md）

# Q1 2027 Earnings Call
**Fabrinet** | Earnings Calls | 2026-11-02

**Operator** (Operator):
Good afternoon, and welcome to Fabrinet's Financial Results Conference Call for the first quarter of fiscal year 2027. [Operator Instructions] As a reminder, today's call is being recorded. I'll now turn the call over to your host, Garo Toomajanian, VP, Investor Relations.

**Garo Toomajanian** (Executives):
Thank you, operator, and good afternoon, everyone. Welcome to today's conference call to discuss Fabrinet's financial and operating results for the first quarter of fiscal year 2027, which ended September 25, 2026. With me on the call today are Seamus Grady, Chairman and Chief Executive Officer; and Csaba Sverha, Chief Financial Officer. This call is being webcast, and a replay will be available at investor.fabrinet.com. During this call, we will present both GAAP and non-GAAP financial measures. Please refer to the Investors section of our website for important information, including our earnings press release and investor presentation, which include our GAAP to non-GAAP reconciliation as well as additional details of our revenue breakdown. 
In addition, today's discussion will contain forward-looking statements about the future financial performance of the company. Forward-looking statements are subject to risks and uncertainties that could cause actual results to differ materially from management's current expectations. These statements reflect our opinions only as of the date of this call, and we undertake no obligation to revise them in light of new information or future events, except as required by law. 
For a description of the risk factors that may affect our results, please refer to our recent SEC filings, in particular, the section captioned Risk Factors in our Form 10-K filed on August 18, 2026. We will begin the call with remarks from Seamus and Csaba, followed by time for questions. I would now like to turn the call over to Fabrinet's Chairman and CEO, Seamus Grady. Seamus?

**Seamus Grady** (Executives):
Thank you, Garo. Good afternoon, everyone, and thank you for joining our call today. We are off to an excellent start to fiscal 2027 with first quarter revenue that was well above our guidance range and represented another quarter of accelerating growth. First quarter revenue of $1.474 billion increased a remarkable 51% from a year ago and 12% from the fourth quarter with strong year-over-year and sequential growth from all 3 of our key revenue categories. 
In addition to delivering our highest top line growth in 10 years, our revenue performance helped generate record non-GAAP earnings per share of $4.34, also well above the high end of our guidance range. Our impressive results are being driven by broad-based demand across multiple product areas, including continued strong momentum for data center interconnect, growing demand for data center transceivers and expansion in high-performance computing. Looking to the second quarter, we expect new program wins and ramps in addition to growth from existing programs to further enhance our growth profile while also supporting our industry-leading margins. 
We have discussed some of the new programs that we expect to contribute to our growth this year, in particular, hyperscale direct transceivers and merchant transceivers for the data center market. We are installing capacity to meet demand for optical circuit switches and multi-rail systems. We are also working with a number of customers on NPO and CPO opportunities and expect contributions from these programs toward the end of fiscal 2027. We continue to be extremely enthusiastic about these opportunities and their role in further scaling our business. In order to support the rapidly increasing demand and new program wins across our business, we have taken a number of important steps. During the first quarter, we completed our purchase of a new site in Santa Clara, more than doubling our capacity in Silicon Valley. We're already in discussions with a handful of customers about leveraging this additional capacity. In Thailand, we have been expanding at multiple sites. We are just a few months away from completing Building 10, adding more than 50% to our global footprint. 
Having accelerated construction and qualification on portions of Building 10, we are already generating initial revenue from the facility. Our manufacturing expansion at Pinehurst and our new Navanakorn site, which is now up and running, are further helping us to stay ahead of increasing customer demand. However, even with this significant expansion, we foresee the need for additional space based on rapid growth from current engagements, combined with new programs that will be ramping in the quarters ahead. As such, we have made the decision to begin construction of Building 11 at our Chonburi campus as soon as Building 10 is completed in January. Building 11 will add approximately 1.5 million square feet with incremental revenue capacity of approximately $3 billion. 
Even as we begin executing plans for Building 11, we are already exploring potential new sites to further support the unprecedented levels of customer activity we are experiencing. In summary, we delivered an excellent first quarter for a strong start to the fiscal year. We are seeing growing demand across the markets we serve and remain focused on executing to meet the exacting needs of our customers. At the same time, we are rapidly scaling up our manufacturing capacity to meet anticipated demand from the pipeline of opportunities in front of us. All of this makes us more excited than ever about our prospects for continued profitable growth. 
Now I'd like to turn the call over to Chaba for more details on our first quarter results and our outlook for the second quarter of fiscal 2027. Csaba?

**Csaba Sverha** (Executives):
Thank you, Seamus, and good afternoon, everyone. We are off to an excellent start to fiscal year 2027 with first quarter revenue that was well above our guidance range. Revenue of $1.474 billion grew 51% from a year ago for another quarter of accelerating revenue growth. These results flow through the bottom line, producing record non-GAAP EPS of $4.34, which was also well above our guidance range. Looking at the details of the quarter. We had a very strong performance from data center products, which grew 78% from a year ago and 16% from Q4 to $777 million or 53% of total revenue. 
Growth in data center revenue was broad-based, driven by strong demand across transceivers, data center interconnect and high-performance computing with continued momentum across all 3 categories. We continue to see growing demand and improving visibility from customers across the data center market, giving us strong confidence in our outlook for Q2. Looking ahead, the full year also looks very promising, supported by continued growth in existing programs and additional contribution from new transceiver programs as they begin to ramp. 
Communications infrastructure revenue was $444 million, an increase of 35% from a year ago and 8% from Q4. Growth was broad-based across a diverse range of customer programs and applications, including telecom systems, components and satellite communications. Automotive, industrial and other revenue was $253 million, up 20% from a year ago and 8% from Q4. In the first quarter, the laser market contributed the most to our sequential growth in this category as we make headway with customers who have historically focused on in-house manufacturing. 
As I discuss the details of our P&L, all expense and profitability metrics will be presented on a non-GAAP basis, unless otherwise noted. Gross margin in the first quarter was 12.1%, a 10 basis point decline from Q4, primarily due to annual merit increases that take effect in Q1. Gross margin declined 20 basis points from a year ago, primarily due to FX headwinds. Operating expenses remained well controlled at 1.3% of revenue in the first quarter, consistent with Q4. 
As a result, operating margin was 10.8%, down 10 basis points sequentially, but up 20 basis points year-over-year. Our operating model continues to deliver leverage with operating margin increasing from a year ago despite a slight decline in gross margin. Interest income was $6 million, and we had a relatively small foreign exchange revaluation loss of $220,000. Our non-GAAP tax expense was $6 million, excluding a $20 million noncash Pillar 2 top-up tax provision, resulting in a non-GAAP effective tax rate of 4% Tax credits intended to mitigate the impact of Pillar 2 are progressing in Thailand, but have not yet been implemented. As a result, we expect some variability in our reported tax expense over the coming quarters. 
In addition to the top-up tax provision, GAAP net income includes a $21 million noncash unrealized loss related to our minority investment in Raytek, which is also excluded from our non-GAAP results. GAAP net income was $103 million or $2.86 per diluted share. Non-GAAP net income reached $157 million or $4.34 per diluted share, marking another all-time high for the company. Turning to our balance sheet. We ended the first quarter with cash and short-term investments of $757 million, down $119 million from the end of Q4. Operating cash flow for the quarter was $21 million. CapEx increased to $159 million, driven by investments in growth and capacity expansion. 
This included the $77 million acquisition of our second campus in Santa Clara as well as continued construction costs associated with Building 10 in Chonburi and another capacity expansion initiatives. As a result, free cash flow was an outflow of $137 million in the quarter. In the first quarter, we repurchased approximately 77,000 shares at an average price of approximately $380 per share for a total cash outlay of $29 million. Since the end of the quarter, our Board authorized an additional $103 million for repurchases, bringing the total remaining authorization to [ $200 million. ] Turning to our guidance for the second quarter of fiscal 2027. We are encouraged by the increasing demand trends that we are seeing across our business. 
We expect that our growth will again be led by data center revenue with expansion from data center interconnect and transceiver programs, further bolstered by new program ramps that we expect to continue increasingly over the course of the year. Data center growth will be complemented by sequential and year-over-year growth in communication infrastructure as well as in automotive, industrial and other revenue. For the second quarter, we anticipate revenue to be in the range of $1.6 billion to $1.65 billion, representing year-over-year growth of 43% at the midpoint. 
From a profitability perspective, we expect to see efficiencies and leverage drive incremental improvements in margins. We anticipate non-GAAP EPS to be between $4.77 and $4.92. In summary, our impressive first quarter results represent a strong start to fiscal year 2027. With multiple significant programs ramping over the next few quarters, we are also very optimistic that we can deliver a terrific second quarter with momentum extending through the rest of the fiscal year. 
Operator, we are now ready to open the call for questions.

**Operator** (Operator):
[Operator Instructions] 
And our first question comes from the line of Christopher Rolland of Susquehanna.

**Christopher Rolland** (Analysts):
I guess my first one, like in your prepared remarks and also the press release, you talked about broad-based demand across multiple significant programs and then new product ramps further supporting growth. I guess, first, the existing programs, were those specifically the hyperscale and merchant opportunity? 
And secondly, the new programs, was that OCS and multi-rail? And if you could provide any more color as to these new opportunities, the size, engagements, that would be great.

**Seamus Grady** (Executives):
Yes. The growth -- Christopher, the growth we're seeing is pretty broad-based. The heartening thing from our point of view is it's across really all of the industries that we serve and all of the customers. The growth has been very strong in our data center business, in our communications infrastructure business and even our automotive and industrial and other business has been growing nicely. And some of that growth is with the programs you mentioned. 
Our DCI business continues to be very strong, and we're just starting to get going with the 2 programs that you mentioned, multi-rail and OCS. So the growth vectors, if you like, are multiple and across really all aspects of our business. Even though we've grown, as we said in the prepared remarks, we were up 51% compared to the same quarter a year ago. We're looking at continued very strong momentum as we go into Q2. And a lot of these newer programs are really just beginning to get going. So we're pretty excited about what's in front of us.

**Christopher Rolland** (Analysts):
And maybe another one, just the NPO CPO opportunity. I think there's a lot more discussion about early programs starting in late '27. Maybe if you can talk about the parts of that opportunity you might be able to supply? Is it just NPO? Is it also HPC boards? And how big do you think this can be for you overall?

**Seamus Grady** (Executives):
Yes. We have a number of NPO programs that we're confident we will start to see revenue from those towards the latter half of this fiscal year and also some CPO programs with several customers. The nice thing, I suppose, about our business is it's not really either/or. We've always said that NPO and CPO will be complementary to pluggables. So we see pluggables continuing for a long time. We'll probably see more immediate opportunities with NPO. CPO seems to be still a little bit further out, but we have several programs on both -- for both NPO and CPO. We're finding, as the years go by, we're engaging much earlier with the customers. 
So we're getting involved right at the very early stage, in some cases, at the concept stage with the customers and really helping the customers figure out how to build these remarkable products that they design. So our manufacturing expertise is a real benefit to our customers in that we're able to help them figure out how to make the products manufacturable with a predictable yield. So that's really being a benefit to us and our customers in that we're involved very early and really getting to see those latest and greatest products, in many cases, years before they're being talked about. So we're very excited about that.

**Operator** (Operator):
Our next question comes from the line of Karl Ackerman of BNP Paribas.

**Karl Ackerman** (Analysts):
Seamus or Csaba, could you speak to the main drivers of your December quarter outlook by segment? I guess, in particular, within data center, I think you've got a merchant transceiver program layering into your existing datacom scale-out transceiver business as well as the new customer ramping across coherent pluggables. So maybe you could discuss how you see the scale-out versus scale across growth opportunity progressing?

**Seamus Grady** (Executives):
Yes. We don't guide by segments. We -- obviously, we talk about the segments when we report the quarter just ended. We don't break out the guidance by segment in -- for the quarter in front of us. But I would say that the growth is broad-based and it's across really all the segments, including the programs that you just mentioned, the merchant programs are beginning to get going as are the hyperscale direct. We're ramping those currently. So we have several programs. Again, I wouldn't want to call out or give specific guidance in any one segment or any one product, but we're on track, I would say, to deliver good solid growth in Q2.

**Karl Ackerman** (Analysts):
Got it. Maybe for Csaba, if I could sneak one more in, please. I know your share repurchases are opportunistic, but does the expansion of your repurchase program suggests you'll be more aggressive given where the stock is here? I guess, why the need to broaden the repurchase program today and given the capital requirements for Building 10, 11, is there a minimum cash level you need to run and invest in the business?

**Csaba Sverha** (Executives):
Karl, so let me give you some brief regarding our capital allocation. So our strategy hasn't changed. So our #1 priority is to continue to invest in growth. As you pointed out, we are using cash and we are using our balance sheet to expand our capacity and working capital requirement as we are going through this staggering growth. Nevertheless, as we have always been opportunistic, we have always been strategic with our share buyback program that we continue to designate surplus cash flow to the 10b5 plan as well as remain opportunistic on the market when we see fit and when we are in an open window. 
So last quarter, purchases were mostly driven by our 10b5 plan. And it just happened to be in our first quarter when we review our capital allocation strategy and we launch our new 10b5 plan. So we believe that we will continue to adhere to our policy of, number one, financing growth. Number two is designating surplus cash to the 10b5 plan; and number three, also being opportunistic with buybacks. So those are the footings of our increased authorization as well. So our Board has just increased the buyback to $200 million. So that will be deployed between 10b5 and an opportunistic program as well.

**Operator** (Operator):
Our next question comes from the line of Joseph Cardoso of JPMorgan.

**Joseph Cardoso** (Analysts):
On the results. Maybe for my first one, bigger picture question. You had some large players in the industry announced an acquisition this morning, and I believe they happen to be customers of yours. So maybe curious if you could opine on both whether this -- how you guys are thinking about this relative to an opportunity for Fabrinet as well as any bigger picture thoughts on the consolidation between optics and semis and what this means for the industry going forward more broadly? And then I do have a follow-up.

**Seamus Grady** (Executives):
Joe, yes, so we're not familiar with the terms of the deal. It's obviously late-breaking news for all of us, and we haven't had a chance to speak with either company. I will say both companies are customers of Fabrinet. Lumentum has been a customer for a very long time, really since the foundation of our company. Lumentum has been a customer of Fabrinet and continues to be a really excellent customer for us. Marvell has become a customer more recently. And so we're excited about the opportunity in front of us. 
Historically, when there's been consolidation in the industry, it has tended to benefit Fabrinet. If you look back at some of the consolidations that happened over the last several years, I think at the time, there was maybe a thought that it might be -- some of those consolidations might be bad for Fabrinet. But in all cases, it turned out to be positive for Fabrinet, whether you look at the, let's say, the Lumentum acquisition of NeoPhotonics or when Infinera acquired Coriant or even the more recent one when Nokia has acquired Infinera. 
In all cases, we've seen our business subsequently grow with the combined entity. So we hope and expect that this will be the same. Obviously, our relationship with both companies is really excellent, and we look forward to learning more about the merger and understanding what that means for us and how we can continue to help and support both companies or the new company. As regards to the overall, let's say, merger between electronics and photonics, it's something that we've been really benefiting from and pointing to for a long time really. There is this, if you like, overarching migration from the electronics world to the photonics world. 
And it was originally, of course, over vast distances, subsea and the like, and now we're down to much closer distances. And when you get right down to co-packaged optics and near packaged optics, you're down to very, very close connections and including products like optical circuit switching and the like, which are really exciting products. And really, we are seeing the convergence of solid-state and photonics. And fortunately, Fabrinet, we're right in the middle of that, and we feel perfectly poised to benefit as that convergence unfolds and continues. So we're very excited about it. We're excited about the opportunity, not just with the Lumentum-Marvell transaction, but in general, this convergence that's going on and has been going on for some time. And we're really just at the start of this. This is really the very first innings, I would say, of this kind of overarching convergence that's going on.

**Joseph Cardoso** (Analysts):
Got it. I appreciate the thoughts there, Seamus. And then maybe as my second one, I believe you guys are calling for 1Q to kind of be a trough year for gross margins and then sequential improvement in 2Q. But kind of wanted to take a step back and just -- can you maybe outline how you guys are thinking about the contribution between some of these ramping programs, FX and then anything else maybe that I'm missing there that are drivers there? And then as we think about maybe the full year here, are those tailwinds likely to continue? 
And sorry, the last piece of this would just be, obviously, you guys are talking about new -- some of these new opportunities around OCS, multi-rail, MPO/CPO. Could these programs be margin accretive to the model? Or should we think about them kind of triangulating into the average that you guys have talked about in terms of that range?

**Csaba Sverha** (Executives):
All right, Seamus. So Joe, let me take this step by step. So if you look at historically, one thing we are very pleased is to see the consistency of our gross margins and incremental improvement of our operating margin as we continue to grow the top line. So we have been very disciplined with spending. So our operating leverage does show as the company grows, and we are going through this huge phase of growth. Obviously, this comes with challenges as well. 
Sometimes our gross margin got pressured from early ramp expenses. We want to make sure that we hire ahead of the ramp to support our customer needs. But those initial phases of headwinds tend to fade away after a short period of time. The biggest variable in our business model is and has been exchange rate, which we continue to hedge and try to take out this volatility as much as we can. So -- for the rest of the year, exchange rate seems to be flattening out based on the hedges we foresee. So we don't anticipate any more headwinds from exchange rates going to the second half of fiscal 2027. 
With regards to leverage, obviously, we have a very resilient cost structure with fixed cost being about 5% of our cost. You don't get a lot of fixed cost leverage at gross margin level. However, we do anticipate that our operating margin will continue to expand as we grow. With regards to new programs, again, new program wins and early stage of the life cycle tend to be beneficial from a gross margin perspective. 
Obviously, as the company goes through this transformation, as you also and Seamus mentioned, this convergence between photonics and electronics we provide a much greater level of value add to our customers, which we do anticipate to accrete our margins. So if you look at strategically, we do anticipate our gross margins to improve over time as we continue to deliver higher level of value to our customers. I think we are doing a good job with managing and mitigating the exchange rate environment and also being disciplined with our OpEx structure, we continue to expect operating margin to grow as we go through 2027 and the years ahead. I hope it covers all your questions.

**Operator** (Operator):
Our next question comes from the line of Steven Fox of Fox Advisors.

**Steven Fox** (Analysts):
I had 2 questions as well. First of all, maybe just to follow up on the last comment in terms of how convergence with electronics, you were able to add more value. Can you give a couple of examples of how that happens and what kind of impact it has on your profitability? And then I had a follow-up.

**Seamus Grady** (Executives):
I think the main example is several examples where we're able to help the customers bring the products to market. The customers tell us that we help them bring the products to market earlier than if they worked with, we call it, a traditional contract manufacturer. Our expertise in really figuring out early how to put these products together in a way that's cost effective, but also high yield and repeatable really helps the customer to get the time-to-market advantage. 
There are several examples. I wouldn't want to get too specific, but it's everything from the leading-edge transceivers to some of the high-performance compute products and these newer products such as optical circuit switching, NPO and CPO. So I think having the knowledge on really how to put these photonics products together in a cost-effective way and a high-yield way gives our customers a big advantage that results in them continuing to reward us with more and more business.

**Steven Fox** (Analysts):
Got it. That's helpful. And then as a follow-up, just looking at this big revenue beat and raise, I'm not quite sure if I understand all the dynamics of it. Like you mentioned new programs, but you also mentioned demand. So were you seeing forecasts get upside? Were you able to pull in production? Were you able to add capacity to better meet demand? I'm just not sure what happened here and what were the big -- just sort of broad drivers forgetting about the product segments for a second.

**Seamus Grady** (Executives):
Well, I mean, what happened was our revenue accelerated significantly. Q1 marked our 14th -- it wasn't kind of a onetime event. Q1 marked our 14th consecutive quarter of growth and our seventh consecutive quarter of accelerating year-over-year growth. In Q1, we grew a pretty remarkable 51% year-over-year. That's an increase of $496 million versus the same quarter a year ago. It really is just extraordinary momentum, which we expect to continue into Q2. And the growth we are seeing is broad-based. It's across several customers and segments. It wasn't a onetime big upside from one customer. It's just significant increase in demand across all of our customers. In Q1, our data center business was up $340 million versus -- year-on-year versus the same quarter a year ago or 78%. So data center business up 78%. Our communications infrastructure business was up 35% or $114 million versus Q1 of last year. And our industrial, automotive and other business was up 20% or $42 million. 
So overall, up $496 million versus the same quarter a year ago across all the industry segments. And then for Q2, we don't break out by segment for Q2, but for Q2 at the midpoint of our Q2 guidance, we would be up again versus Q2 of last year, we would be up $151 million at the midpoint or 43%. So just remarkable growth, and we believe sustainable growth that's broad-based and continuing into Q2 and hopefully throughout fiscal '27.

**Steven Fox** (Analysts):
But just to be clear, this was mainly from existing programs where you're able to upside versus original expectations as opposed to new program ramps going faster than expected?

**Seamus Grady** (Executives):
It's both. It's both existing programs. And I mean, new programs, as we ramp them, their immediate impact on revenue is not that significant because we're just beginning to ramp them. Obviously, new programs then become existing programs and they ramp rapidly, but it's a combination of both. We have a very healthy pipeline of new programs that we're ramping, but also programs that were new programs a couple of quarters ago that are now existing programs that we're ramping. So it's a combination of all of the above.

**Operator** (Operator):
Our next question comes from the line of George Notter of Wolfe Research.

**George Notter** (Analysts):
I wanted to ask about Building 11. It looks like you upsized the size of that building. Can you remind us how big the plan was for that building previously and then what it is now? And then also just looking at the bigger supply chain environment, it feels like maybe componentry is becoming more readily available for you. I guess I'm inferring that based on the upside here and then the upside in terms of the guidance for the December quarter. But maybe some comments on the supply chain environment would be great.

**Seamus Grady** (Executives):
Sure. Thanks, George. So first of all, on the capacity. So just to recap, our revenue capacity at the end of fiscal 2026 was about $5.8 billion. We have been aggressively increasing our capacity, and we expect our revenue capacity to be around $10 billion at the beginning of January, so in just a few months from now. But the biggest -- so a significant increase in capacity. The biggest factor driving this will be the completion of Building 10 in Chonburi, which adds 2 million square feet or about $3.5 billion in revenue capacity. 
To put that in context, just in terms of the physical size, 2 million square feet is about the surface area taken up by 35 American football fields. So it's quite gigantic. And that revenue increase is about 75% of our actual FY '26 revenue. We have commissioned our campus in Nava, we call it Nava 1, the campus that we purchased recently, and that adds about $400 million of revenue capacity as well as our expanded footprint in Santa Clara, which adds about $300 million. So all told, we'll start the year at about $10 billion of capacity. And we continue to invest ahead of the demand. We're going to rapidly expand our manufacturing footprint to make sure we stay ahead of the demand we're seeing from our customers. 
To that end, we're not stopping with Building 10. We will be breaking ground on Building 11 in Chonburi in January. We will probably coincide the ribbon cutting for Building 10 with the groundbreaking for Building 11. Building 11 will add about 1.5 million square feet. You're right, that's maybe a little bit bigger than we originally thought. We tend to get a bit smarter as we go along, we learn a few things. And for Building 11, we don't need much office space in Building 11 because we're more than covered with the other buildings on the campus. We don't need much warehousing space. So it's a lot of, let's say, as a percentage of the total space, a lot more of Building 11 will be manufacturing space. 
So about 1.5 million square feet or about $3 billion in revenue capacity. And it will take us about 18 months to build and should come online at the end of fiscal 2028. But based on the pipeline of business we see in front of us, we're already looking for potential new sites, both land but also buildings to make sure we stay ahead of the demand. It's important to note, of course, that this expansion, we funded with our own cash on our balance sheet. As you would have seen, our CapEx was significant last year as we purchased the Santa Clara operation. So we continue to fund this growth with our very strong balance sheet, and we continue to deliver ROIC north of 30%. So it's a very compelling business model that we have. 
All told, if you look at the total, let's say, capacity that we have, if you take Building 10 plus what we had before Building 10 plus Nava plus Santa Clara plus Building 11. And if we build a Building 12 in the future, which we can on the campus in Chonburi. Previously, we had sized all of that at about $14 billion of capacity. We've now revised that up to about $16 billion. So Building 11, we originally said it was about $2.1 billion of capacity. We now think that's closer to $3 billion as the revenue kind of per square foot continues to go in our favor, smaller, denser, more revenue dense products improve the revenue per square foot. 
So that revenue capacity that we're bringing on will be, like I said, about $10 billion in January. But when Building 11 is completed, that will add another $3 billion to take us to $13 billion. Building 12 will add another $3 billion to take us to $16 billion, plus whatever we add in the meantime in terms of other capacity that we uncover as we continue to search for capacity. In terms of components, we -- I'm sorry, go ahead.

**George Notter** (Analysts):
I was just going to ask about the follow-up question, the component supply chain question. Go ahead, please.

**Seamus Grady** (Executives):
Yes, I say about the components. Yes, we have been making good progress and getting our fair share and thankfully, in some cases, our unfair share of the available components. Components are in tight supply across the board. Obviously, demand for everyone is very strong. But we've been fortunate we've been able to keep ahead of that. 
And obviously, we could always ship more if we have more, but our approach is really to work with the customers and the suppliers to make sure we get what we need to meet the customers' demand and continue to add capacity to make sure that we're never capacity gated in terms of our ability to grow. So -- and like I said, we'll continue to add capacity ahead of the demand, and we'll continue to work with the customers and the suppliers to make sure we keep the component supply lined up as well.

**Operator** (Operator):
Our next question comes from the line of Mike Genovese of Rosenblatt Securities.

**Michael Genovese** (Analysts):
First of all, on the transceiver OEMs that are coming in, how many -- are we talking about? Or are we talking about more than one transceiver OEM that's ramping with the company?

**Seamus Grady** (Executives):
We have more than 1.

**Michael Genovese** (Analysts):
Is it more than 2?

**Seamus Grady** (Executives):
We're not going to say much more than that because, again, these are always -- as always, Mike, they're confidential sensitive conversations are going on with the customers, and we don't like to say too much, but we have more than one. Yes, and we continue to ramp those nicely. And they're becoming -- as you can see, our growth in the data center business was up 78%, and we continue to see good strong growth going into Q2.

**Michael Genovese** (Analysts):
Perfect. And just -- most of my questions have been asked. So I'm going to ask about the CapEx and the financing. There was about $75 million of long-term borrowing in the quarter. What's the fiscal '27 CapEx plan? And why borrow rather than fund from cash?

**Csaba Sverha** (Executives):
So let me address the borrowing section first. So we have actually favorable interest rate environment in Thailand where the cost of borrowing is cheaper than breaking up our cash that is being invested in the U.S. So that's a simple financial decision when we need cash for investment in Thailand, it's cheaper to borrow there than breaking the investment that it earns. 
So secondly, our CapEx plan, as you have seen, we had an outsized CapEx number in Q1 because of the Santa Clara campus purchase. Other than that, our CapEx is running at about 5% of revenue run rate, which has been somewhat consistent in the last fiscal year. So obviously, as Building 10 comes online, will be done by January, we will start Building 11, so that will layer on, on the CapEx spending. As well as Seamus mentioned, we continue to search for additional capacity. So that should come through. We should see some -- even further increase in our CapEx spending for 2027. Having said that, if you take this large chunky capacity additions aside, our normal, I would say, CapEx run rate to support this outsized growth would be at about 5% of the revenue run rate for the year.

**Operator** (Operator):
Our next question comes from the line of Tim Savageaux of Northland Capital Markets.

**Timothy Savageaux** (Analysts):
Congrats on the results and guidance. Kind of want to pick up where we left off last quarter, where you expressed some optimism of being able to accelerate revenue growth in fiscal '27 versus '26. I imagine you're feeling far more confident about that now. So I wanted to kind of follow up on that, which is your first half growth rate was 47% given where you guided. Talked about that growth being sustainable and indeed some new program ramps in the second half of the year. So I guess a 2-part question. We can get an update on your feelings about accelerating growth? And can you sustain something in that range that you're seeing in the first half for the second?

**Seamus Grady** (Executives):
Thank you, Tim. You are nothing if not consistent. Yes, I think if you look at the growth we've been seeing, it's pretty remarkable really to consider the growth, and it's across the industry segments, as I mentioned, the numbers I walked through a moment ago, 51% in Q1. Q2, our guidance would have us at 43% growth or up $151 million year-on-year at the midpoint of the guidance. And we're continuing to add capacity as fast as we can. Building 10, we have a clear line of sight to what's going into Building 10 and when it's going into Building 10. 
Hence, our decision to pull the trigger on Building 11, but also to look for additional capacity that we can bring on hopefully before Building 11 is completed. Building 11 will take about 18 months from when we start, so somewhere around the middle of calendar 2028, so 18, 20-something months from now. That's when Building 11 will come on stream, but we think we'll need capacity before that. So we're actively looking right now. There's a few projects we're working on, but we're actively looking to bring on additional capacity. Again, both land, but also a factory space that if we can get our hands on to bring on additional capacity. So my -- I suppose my feelings about the accelerating growth are as positive as they were when we spoke approximately 90 days ago, if not a little bit more positive, I would say. 
Sustainability, certainly based on the signals we see from the customers who are really happy to show us the demand picture really as far as the eye can see as far ahead as you can see. it appears to be very sustainable. But the nice thing, I suppose, about our business, Tim, as you know, is we tend to have an asset-light model. So -- and our fixed cost is very low. So even in the doomsday scenario, if there is a downturn, we haven't added any real significant fixed costs. So we'll continue to grow and make sure we benefit from this upside environment that we're in, but also we're always mindful of being ready for if there is any kind of a downturn. So we're very -- I'd say, very optimistic about the future, but also we're pragmatic and we're doing it in a way that we think is low risk and sustainable. 
So yes, to answer the question, I think we're as optimistic as we were, if not a little bit more so than when we spoke 90 days ago, and we do believe that the growth continues to be sustainable, again, because it's across all industry segments that we serve and many, many customers.

**Timothy Savageaux** (Analysts):
Okay. Great. Appreciate that. And I wanted to follow up on the NPO, CPO front. Obviously, Lumentum talked about a $5 billion win here this morning and they talked about similar type of numbers in OCS. I guess, how do you look at those 2 opportunities in terms of relative potential for Fabrinet? And it sounds like each of these could be multi-hundred million, if not billion dollar businesses for you guys. Is that crazy to think about?

**Seamus Grady** (Executives):
I think that's a fair way to think about it. And they're not even in the -- if you like, the numbers yet. They're only just getting started. But they both look to be very -- have very strong demand. OCS the demand forecast we see for OCS is very strong. And also for these various NPO programs that we're working on looks to be very strong. Yes, either of these or both of these could be multi-hundred million dollar opportunities on their own. And as I said, they're just getting started. We haven't even really started to ship anything yet. But yes, they're very positive, we think, for our business.

**Operator** (Operator):
Our next question comes from the line of Ryan Koontz of Needham & Co.

**Ryan Koontz** (Analysts):
Real nice numbers. I want to ask your view kind of at the macro level about the transceiver market in light of investor concerns that CPO and NPO are going to be highly cannibalistic. And maybe from your perspective, you have a little different view there from talking to your customers and your customers' customers about how you think about the durability of the datacom transceiver market and maybe how the fulfillment models might be changing a bit. Obviously, you're seeing some real nice growth in new green shoots there. So anything you can share about the transceivers would be appreciated.

**Seamus Grady** (Executives):
Yes. Thanks. I think the idea that it's kind of either/or or that CPO was just going to kind of cannibalize the pluggable transceiver market is I suppose I'd be kind and call it reductive. I think it's a bit overly simplistic to think that it's one or the other. We believe that pluggables will continue for a very long time, but that NPO and ultimately, CPO will also continue to grow. So we don't really think it's one or the other for a long time to come. You saw the recent announcement from Cisco and NVIDIA, they announced a road map for ultra-dense small form factor pluggables, this USFP product, which looks to, I guess, continue the pluggable architecture for many years to come. 
So we think we're ideally positioned to produce all the products in the space, pluggables, NPO, CPO. We're happy to work with the customers. And really, our mission is to just always be ready to produce the customers of the future -- sorry, the products of the future for the customers, whatever that might entail, whether it's more dense pluggables or NPO or CPO or all of the above. So we don't see it as an either/or situation. We see it as an and also situation.

**Ryan Koontz** (Analysts):
Helpful. And maybe just a follow-up there with regards to your strength in the datacom side of the world as well as telecom side of the world. The middle ground there is coherent lite. Have you announced any coherent light wins? Or is that a market you feel like you're well positioned for?

**Seamus Grady** (Executives):
Yes. I mean we feel we're very well positioned. Those products fit perfectly into our kind of capabilities. We haven't announced anything specific in that market. But yes, we would -- they would fit very well with our capabilities.

**Operator** (Operator):
I'm showing no further questions at this time. I'll now turn it back to Seamus Grady for closing remarks.

**Seamus Grady** (Executives):
Thank you for joining our call today. We're off to an excellent start in fiscal 2027 with year-over-year top line growth of nearly $500 million or 51% and strong momentum continuing into Q2. We are staying ahead of the incredible demand by aggressively expanding our capacity as we see contributions from existing programs and new program ramps driving our rapid growth. We look forward to speaking with you again next quarter. Thanks again, and goodbye.

**Operator** (Operator):
Thank you for your participation in today's conference. This does conclude the program. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FN_Q4_2026_Earnings_Call_20260817.md
- 2026-08-17｜Csaba Sverha｜guidance：FQ1'27營收財測區間（原話："revenue to be between $1.375 billion and $1.425 billion"）
- 2026-08-17｜Csaba Sverha｜guidance：FQ1'27 EPS財測區間（原話："we anticipate EPS to be between $4.10 and $4.25"）
- 2026-08-17｜Csaba Sverha｜guidance：管理層稱只按季給財測，但客戶提供延伸至FY27之後的能見度（原話："we are more confident than ever in our longer-term outlook"）
- 2026-08-17｜Csaba Sverha｜guidance：管理層說明客戶長期預測並非訂單承諾（原話："customer forecasts are not order commitments"）
- 2026-08-17｜Seamus Grady｜guidance：被問FY27成長是否再加速，管理層表示有可能（原話："we could see another year of accelerating growth"）
- 2026-08-17｜Csaba Sverha｜margin：Q4毛利率12.2%（原話："Gross margin in the fourth quarter was 12.2%"）
- 2026-08-17｜Csaba Sverha｜margin：Q4營業利益率10.9%（原話："operating margin of 10.9%, our highest level in three years"）
- 2026-08-17｜Csaba Sverha｜margin：Q1費用季節性造成暫時性利潤率逆風（原話："expense seasonality will create a temporary margin headwind"）
- 2026-08-17｜Csaba Sverha｜margin：成長模式不需大幅增加營業費用（原話："growth model does not require significant incremental"）
- 2026-08-17｜Csaba Sverha｜margin：Raytek重新衡量利得依一致處理方式排除於non-GAAP（原話："We intend to apply the same treatment consistently"）
- 2026-08-17｜Csaba Sverha｜margin：泰國OECD補足稅準備列為non-GAAP排除項（原話："$57.4 million provision related to Thailand's top-up tax"）
- 2026-08-17｜Csaba Sverha｜margin：新營收分類僅為呈現方式變更（原話："This change is purely presentational"）
- 2026-08-17｜Csaba Sverha｜margin：新分類依產品最終部署處歸類（原話："everything else goes into the communication infrastructure"）
- 2026-08-17｜Csaba Sverha｜margin：資料中心Q4營收與成長（原話："Data center revenue was $669 million in the fourth quarter"）
- 2026-08-17｜Csaba Sverha｜margin：DCI年化營收運行率超過10億美元（原話："annualized revenue run rate exceeding $1 billion"）
- 2026-08-17｜Csaba Sverha｜margin：通訊基礎設施Q4營收與年增率（原話："Revenue was $413 million, an increase of 40% from a year ago"）
- 2026-08-17｜Csaba Sverha｜customer：FY26十%以上客戶占比（原話："Cisco at 20%, NVIDIA at 16%, Nokia at 11%"）
- 2026-08-17｜Seamus Grady｜customer：Nokia升為10%以上客戶（原話："Yes, they rose to be more than a 10% customer."）
- 2026-08-17｜Seamus Grady｜customer：資料中心客戶供應：部分零組件需求高於供給（原話："certain components is higher than the available supply"）
- 2026-08-17｜Seamus Grady｜customer：管理層稱已把供應缺口納入財測（原話："taken any potential gaps in supply into account"）
- 2026-08-17｜Seamus Grady｜customer：HPC表現優於預期（原話："continues to perform, I would say, ahead of expectations"）
- 2026-08-17｜Seamus Grady｜customer：系統整合業務盼未來數季新增1至2案（原話："we hope to have 1 or 2 to add in the coming quarters"）
- 2026-08-17｜Seamus Grady｜product：新收發器專案時程：一個merchant專案12月季開始（原話："merchant programs to begin in the December quarter"）
- 2026-08-17｜Seamus Grady｜product：NPO被視為較CPO近期的機會（原話："probably represents a more near-term opportunity than CPO"）
- 2026-08-17｜Seamus Grady｜product：積極參與多條multi-rail專案（原話："heavily engaged with number of customers on these programs"）
- 2026-08-17｜Seamus Grady｜product：OCS目前規模仍小（原話："OCS is quite small today"）
- 2026-08-17｜Seamus Grady｜competition：中國收發器禁令尚未定案，公司不為中國業者製造（原話："We don't manufacture for any Chinese providers"）
- 2026-08-17｜Seamus Grady｜competition：對中國收發器禁令的說法（原話："The proposed ban on new transceivers from China"）
- 2026-08-17｜Csaba Sverha｜risk：存貨增加歸因於成長與為後續ramp備料（原話："the inventory increase has to do with our growth"）
- 2026-08-17｜Csaba Sverha｜risk：Q4資料中心中datacom子類持平（新分類下）（原話："our datacom was somewhat flat"）
- 2026-08-17｜Csaba Sverha｜capital_allocation：Q4自由現金流為流出（原話："Free cash flow was an outflow of $37 million in the quarter"）
- 2026-08-17｜Csaba Sverha｜capital_allocation：回購額度剩餘約1.69億美元（原話："approximately $169 million available at the end of"）
- 2026-08-17｜Csaba Sverha｜capital_allocation：再投資於業務是最具吸引力的現金用途之一（原話："reinvesting in the business remains one of the most"）
- 2026-08-17｜Seamus Grady｜commitment：Building 10預計2027年初完工（原話："we remain on track to complete Building 10 by early 2027"）
- 2026-08-17｜Seamus Grady｜commitment：產能規劃上看125億至140億美元營收（原話："between $12.5 billion and $14 billion over the coming years"）
- 2026-08-17｜Seamus Grady｜commitment：Building 10新增產能30至35億美元（原話："Building 10 will add $3 billion to $3.5 billion of capacity"）
- 2026-08-17｜Seamus Grady｜commitment：未來數年持續積極擴產（原話："continuing to expand aggressively over the next few years"）
- 2026-08-17｜Seamus Grady｜commitment：每平方呎營收提升（原話："We are actually increasing our revenue per square foot."）

### 問答異常語氣（迴避／改口／保留）
- FN_Q4_2026_Earnings_Call_20260817.md｜問：Tim Long問NVIDIA業務年度下滑與競爭格局｜答法：不談單一客戶細節，改談資料中心整體與供應鏈管理，未直接回答競爭格局
- FN_Q4_2026_Earnings_Call_20260817.md｜問：Amol問最大datacom客戶1.6T營收時程｜答法：拒絕更新，請分析師去問NVIDIA
- FN_Q4_2026_Earnings_Call_20260817.md｜問：Karl Ackerman問是否有支撐1.6T ramp的雷射供應承諾｜答法：未給具體答案，只說零組件供應已納入財測
- FN_Q4_2026_Earnings_Call_20260817.md｜問：Yash Shah問datacom單季下滑原因（供應、轉換或需求時序）｜答法：改以新分類下datacom持平回應，未拆解各因素占比

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

## ⑥ 條件附卡（archetype_hint='EMS/ODM' 命中）：judge_addendum_cyclical.md

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
{"date":"20260905","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"11 月 Q1 FY27 財報總資料中心 QoQ >0 且 datacom QoQ ≥0；或回檔至 ≤$350（FY2027 本益比約 19x）且 H1-H3 檢核無損","irr_base_pct":8.8,"ev5y_pct":46.4,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.8,"ev5y_pct":46.4,"irr_base_pct":8.8,"max_dd_pct":-45,"bull_5y_price":1012.0,"bear_5y_price":227.5,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"11 月 Q1 FY27 財報總資料中心 QoQ >0 且 datacom QoQ ≥0；或回檔至 ≤$350（FY2027 本益比約 19x）且 H1-H3 檢核無損","price_at_dd":407.4,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
