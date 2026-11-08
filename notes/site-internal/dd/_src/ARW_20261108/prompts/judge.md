你是 stock-analyst **v20 判斷 agent**，標的 ARW（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ARW","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARW_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARW_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":10717.7,"period":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":436.1,"period":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","unit":"百萬美元（利益率 4.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":430.3,"period":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","unit":"百萬美元（利益率 4.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi5_q4_2026","label":"管理層 Q4 2026 指引","value":"營收 11.55–12.15 十億美元；Non-GAAP EPS 7.00–7.20；GAAP EPS 6.25–6.45","period":"Q3 2026 新聞稿（公告於 2026-11-05），指引期間 Q4 2026","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026 新聞稿（公告於 2026-11-05），指引期間 Q4 2026","citation":"公司新聞稿 8-K Ex.99.1；Global Components 8.15–8.55 十億、ECS 3.40–3.60 十億；稅率 23–25%；利息費用約 50 百萬；匯率對 EPS 影響 −0.14（對去年同期）"},"note":"未查（consensus_revision 僅有 FY EPS 快照，未含季指引比較）"},{"id":"f_kpi6_backlog_book_to_bill","label":"硬體／設備追加：backlog 與 book-to-bill","value":"未量化","period":"Q3 2026（公告於 2026-11-05）","unit":"文字描述","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1：backlog 持續成長、Global Components book-to-bill 「well above parity」，無數字"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_arw_gross_margin_pct","label":"ARW 毛利率","value":11.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_arw_operating_margin_pct","label":"ARW 營業利益率","value":4.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_arw_fcf_margin_pct","label":"ARW FCF 利潤率","value":4.03,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_avt_gross_margin_pct","label":"AVT 毛利率","value":10.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_avt_operating_margin_pct","label":"AVT 營業利益率","value":3.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_avt_fcf_margin_pct","label":"AVT FCF 利潤率","value":-1.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_snx_gross_margin_pct","label":"SNX 毛利率","value":6.89,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNX.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_snx_operating_margin_pct","label":"SNX 營業利益率","value":2.71,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNX.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_snx_fcf_margin_pct","label":"SNX FCF 利潤率","value":-1.08,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNX.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cdw_gross_margin_pct","label":"CDW 毛利率","value":21.0,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cdw_operating_margin_pct","label":"CDW 營業利益率","value":7.03,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cdw_fcf_margin_pct","label":"CDW FCF 利潤率","value":3.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wcc_gross_margin_pct","label":"WCC 毛利率","value":21.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WCC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wcc_operating_margin_pct","label":"WCC 營業利益率","value":5.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WCC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wcc_fcf_margin_pct","label":"WCC FCF 利潤率","value":1.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WCC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_441_4_26_9","label":"自由現金流（營業現金流 −441.4 減資本支出 26.9，自行換算）","value":-468.3,"period":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1（OCF、capex 為原文，FCF 為換算）；原因為支應客戶需求的營運資金投入，存貨 7,306.0 對 2025 年底 5,081.9"},"note":"n/a"},{"id":"f_kpi4_sbc_sbc_11_6_non_gaap_43","label":"SBC 占營業利益（SBC 攤銷 11.6 ÷ Non-GAAP 營業利益 436.1）","value":2.7,"period":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1（SBC 11.6 百萬為原文，比率為換算）"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":181.09,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-7.11,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":30.73,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（21.64 → 21.64）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.93 → 23.93）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（27.2 → 27.2）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":21.64,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":23.93,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":27.2,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 21.64 → 21.64（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":9.19,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝39.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":39.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.24,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝50.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":50.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":8.37,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 21.64，分子＝快照價 181.09","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":2536.37,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 2751.98、現金 215.61（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":50.56,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":11691.83,"period":"2026-11-08","unit":"USD m","basis":"市值 9155.46 ＋ 淨負債 2536.37","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":41598.69,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（4 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":46474.97,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（4 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.28,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 181.09 / W52 176.54 / W104 146.76 / W250 131.33 / W250 13週斜率 0.88%"},{"id":"f_ma_w52","label":"52 週均線","value":176.54,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":146.76,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":131.33,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.88,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 稱公司面對大型跨國與本國電子元件／企業運算分銷商及眾多專注小型對手競爭，並面臨進入物流、電子目錄、電商供應鏈服務者及供應商本身的競爭；擴張新領域可能難以維持或提高市占。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"As the company continues to expand its business into new areas to stay competitive in the market, the company may encounter increased competition from current and/or new competitors, making it difficult to retain or increase its market share.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"CSIMarket 以同業集合營收推算 ARW 2Q26 市占約 14.49%，營收年增 31.82%（聚合站自行推算，非產業官方數據）；搜尋未找到一手市占研究。","source":"CSIMarket ARW Competitors","url":"https://csimarket.com/stocks/ARW-Competitors","excerpt":null,"as_of":"2026-07-31","retrieved_at":"2026-11-08","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：2025 年無單一客戶占合併銷售超過 2%（客戶高度分散，無「最大客戶」可導入第二供應商或自製）；供應商無單一超過 8%","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"No single customer accounted for more than 2% of the company's 2025 consolidated sales.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K 描述：多數客戶要求的交期或量，通常無法直接向原廠取得；經查未見 2026 年有客戶導入第二供應商或自製的申報或報導","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"Most of the company’s customers require delivery of their orders on schedules or volumes that are generally not available directly from manufacturers.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2025 10-K：沒有單一客戶占 2025 合併營收超過 2%（供應商單一最高不超過 8%）","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"No single customer accounted for more than 2% of the company’s 2025 consolidated sales.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Octopart/Altium 報導：Samsung、SK Hynix 公開表示無塵室擴產受限加上 HBM 需求，供給短缺可能延續到 2027","source":"Altium/Octopart, The Memory Market Shift: Shortages, Allocation, and the Road to 2027","url":"https://octopart.com/pulse/p/memory-market-shift-shortages-allocation","excerpt":"Samsung Electronics and SK Hynix have publicly indicated that limited cleanroom expansion capacity and unprecedented growth in high-bandwidth memory demand could extend supply shortages through 2027.","as_of":"2026-03-01","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"通路庫存已在近年下調，Anglia 預期需求上升下將出現缺貨與交期拉長，但時點不確定","source":"Evertiq, Anglia warns of longer lead times as market picks up","url":"https://evertiq.com/design/2026-02-10-anglia-warns-of-longer-lead-times-as-market-picks-up","excerpt":"With excess stock largely cleared, Anglia expects shortages and longer lead times to emerge as demand continues to rise, though the timing remains uncertain.","as_of":"2026-02-10","retrieved_at":"2026-11-08","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ARW 2026Q3 營收 107 億美元年增 39%，高於財測上緣；管理層稱 Global Components 需求廣泛、積壓訂單成長、book-to-bill 遠高於 1；報導稱記憶體漲價約占近期零組件成長三分之一","source":"Arrow Electronics 8-K Q3 2026 press release / finviz","url":"https://finviz.com/news/416841/arrow-electronics-reports-record-quarterly-revenue-and-eps","excerpt":null,"as_of":"2026-11-05","retrieved_at":"2026-11-08","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"ARW Q3 營運現金流 -4.41 億美元，主因支應客戶需求的營運資金投入；另有 Beyond Distribution 外包安排相關費用","source":"finviz / RTTNews Arrow Q3 2026 coverage","url":"https://finviz.com/news/416841/arrow-electronics-reports-record-quarterly-revenue-and-eps","excerpt":null,"as_of":"2026-11-05","retrieved_at":"2026-11-08","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Global Electronics Association 調查：2026Q2 認為零組件供給惡化者為改善者 4 倍以上（44% 對 10%）","source":"Global Electronics Association blog, The Supply Chain Is Tightening Again","url":"https://www.electronics.org/blog/supply-chain-tightening-again-data-makes-it-hard-look-away","excerpt":null,"as_of":"2026-07-01","retrieved_at":"2026-11-08","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ARW Q3 2026 8-K：book-to-bill 遠高於 1、積壓訂單成長","source":"SEC 8-K Arrow Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000000753626000150/arw-ex99d1.htm","excerpt":"“Global Components continues to benefit from broad-based demand across geographies, customer segments and industry verticals, with a growing backlog and book-to-bill ratios well above parity.","as_of":"2026-11-05","retrieved_at":"2026-11-08","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 揭露公司受進出口、國際貿易限制、反壟斷等多項法規約束，且曾／可能面臨調查與法規程序，屬一般性風險因子，未點名具體反壟斷案件。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"The company has in the past and may in the future be subject to claims, investigations, regulatory proceedings, and lawsuits in and outside the ordinary course of business","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2025-10 美國 BIS 曾將 Arrow 三家中國子公司列入實體清單，其後據報導已撤銷；屬出口管制而非反壟斷。","source":"搜尋摘要：Arrow Electronics says that US trade curbs on its Chinese affiliates are being reversed","url":"https://www.itiger.com/news/2576904244","excerpt":null,"as_of":"2025-10-19","retrieved_at":"2026-11-08","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未發現 2026 年針對 Arrow 的 DOJ／FTC／歐盟反壟斷調查或拆分事件；舊有 2014 FTC CID（資料庫共享計畫）僅見於 2014–2017 年舊申報。","source":"WebSearch 結果（SEC 舊 10-K/10-Q）","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000166635917000005/arw1231201610-k.htm","excerpt":"no proceedings have been instituted against any person","as_of":"2017-02-24","retrieved_at":"2026-11-08","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K：2025-10-08 起三家中國子公司被列入 BIS Entity List，期間無法收到多家供應商出貨，2025-11-11 正式移除；對 Q4 2025 營運結果有不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"on October 8, 2025, three of the company’s subsidiaries in China were added to the “Entity List” of the BIS, which restricted their ability to receive exports of U.S. technology from suppliers. On October 17, 2025, the BIS issued a temporary authorization that allowed these entities to resume their normal business activities, and the entities were formally removed from the Entity List on November 11, 2025","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025 10-K MD&A：Entity List 事件造成亞太區 Q4 2025 少量銷售損失，公司預期不影響 2026 Q1 及之後。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"which resulted in marginal lost sales by global components in the Asia/Pacific region in the fourth quarter of 2025. The company does not anticipate that this event will have a negative impact on sales in the first quarter of 2026 or future periods.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K：關稅可能抬高採購價並影響營業利益；IEEPA 關稅訴訟（最高法院）結果可能帶來新增關稅、難以收回的退款或第三方訴訟；關稅退稅(drawback)需供應商資料，不保證取得。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"Tariffs and other protectionist measures, and the additional operational costs incurred in minimizing the number of products subject to them, could adversely affect the operating profits for certain of the company’s businesses and customer demand for certain products, which could have an adverse effect on the company’s business and results of operations.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025 10-K MD&A：關稅使 global components 營收與銷貨成本小幅上升（價格上漲），公司持續採取供應鏈優化等緩解措施，無法預測是否延續。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"Global components continues to see a marginal increase in revenue and cost of sales due to price increases. Given the uncertain and evolving nature of U.S. and foreign tariff policies, the company cannot currently predict whether this trend will continue or how it may impact future quarters.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Arrow 2026 Q2 10-Q（期末 2026-07-04）稱關稅政策不確定，無法預測對未來季度影響。","source":"SEC EDGAR 10-Q 2026-07-04","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000110465926091983/arw-20260704x10q.htm","excerpt":"and foreign tariff policies and is continuing to evaluate and further implement mitigating actions, including supply chain optimization and improved solutions around processing tariffs. Given the uncertain and evolving nature of U.S. and foreign tariff policies, the company cannot currently predict how tariffs may impact future quarters.","as_of":"2026-08-01","retrieved_at":"2026-11-08","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子列出國際貿易政治發展、關稅與貿易爭端（特別是美中）、戰爭或武裝衝突為風險","source":"Arrow Electronics 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"Political developments impacting international trade, trade disputes and increased tariffs, particularly between the United States and China; political instability, such as wars or other armed conflicts;","as_of":"2026-02-15","retrieved_at":"2026-11-08","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"供應商整併可能使 Arrow 被排除，導致價格上升與依賴較少供應商","source":"Arrow Electronics 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"to experience consolidation, which could negatively impact the company if the surviving, consolidated suppliers decide to exclude the company from their supply chains, and which could expose the company to increased pricing and dependence on a smaller number of suppliers, among other risks.","as_of":"2026-02-15","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"最新 10-Q 稱關稅政策不確定，無法預測對未來季度的影響","source":"Arrow Electronics 10-Q Q3 FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000110465926123063/arw-20261003x10q.htm","excerpt":"and is continuing to evaluate and further implement mitigating actions, including supply chain optimization and improved solutions around processing tariffs. Given the uncertain and evolving nature of U.S. and foreign tariff policies, the company cannot currently predict how tariffs may impact future quarters.","as_of":"2026-11-05","retrieved_at":"2026-11-08","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Global Components 銷售年增 43%、Global ECS 年增 29%；Components 需求廣泛、積壓訂單增加、book-to-bill 遠高於 1。","source":"Arrow Electronics Q3 2026 earnings release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000000753626000150/arw-ex99d1.htm","excerpt":"Global Components continues to benefit from broad-based demand across geographies, customer segments and industry verticals, with a growing backlog and book-to-bill ratios well above parity.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 2026 指引：Global Components 銷售 81.5–85.5 億美元、Global ECS 34.0–36.0 億美元，合併 115.5–121.5 億美元。","source":"Arrow Electronics Q3 2026 earnings release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000000753626000150/arw-ex99d1.htm","excerpt":"Global Components sales of $8.15 billion to $8.55 billion","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 區域 Components：美洲 +58%、EMEA +41%、亞太 +33%；ECS 美洲 +27%、EMEA +30%；營運現金流 -4.41 億美元（營運資金投入）。","source":"搜尋摘要（Q3 2026 release 彙整）","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000000753626000150/arw-ex99d1.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：Arrow 除同業外也與自己的供應商及物流、電商、設計服務、供應鏈服務業者競爭；供應商若縮減或停止經銷通路銷售會對業務造成重大不利影響。未點名特定替代技術。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"The company also faces competition from its own suppliers and from companies in the logistics and product fulfillment, catalog distribution, e-commerce, design services, and supply chain services markets.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：產業技術快速變化，若 Arrow 數位平台、雲端平台與 AI 工具跟不上競爭者與客戶期待，營收與客戶留存會受影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"If the company is unable to sufficiently maintain and enhance its digital platforms, cloud platforms, and AI tools to keep pace with competitors and align with evolving customer and supplier expectations and demands, there could be an adverse impact on the company's sales revenues and ability to retain existing, and attract new, customers.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"10-K：約 56% 存貨受供應商協議保護（退貨、報廢補貼、價格保護），涵蓋技術變遷造成的存貨減值風險。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"Certain agreements with suppliers protect the company against the potential write-down of inventories due to technological change or suppliers' price reductions.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"10-K 說明 ECS 部門透過 ArrowSphere 雲端市集與管理平台（含 AI 數位 go-to-market）協助 VAR/MSP 銷售雲端產品，屬平台化方向","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"Enabling customer cloud-based solutions through ArrowSphere, the company’s cloud marketplace and management platform, which helps VARs and MSPs to manage, differentiate, and scale their cloud businesses while providing the business intelligence and tools that IT solution providers need to drive growth.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"10-K 競爭段落指出公司亦與供應商爭奪客戶，並面對進入物流、電子目錄經銷與電商供應鏈服務市場的競爭者","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926012765/arw-20251231x10k.htm","excerpt":"The company also competes for customers with its suppliers.","as_of":"2026-02-11","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Edgewater 2026 年 1 月報告：TI 增加直接銷售、TE 將部分車用銷售轉入經銷，ADI 亞太整合有利 Arrow","source":"passive-components.eu component distribution supply chain January 2026","url":"https://passive-components.eu/component-distribution-supply-chain-january-2026/?amp=1","excerpt":null,"as_of":"2026-01-15","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"公司 Q4 2026 guidance：合併銷售 $11.55B–$12.15B，non-GAAP 稀釋 EPS $7.00–$7.20（8-K 新聞稿，2026-11-05）","source":"Arrow Electronics 8-K Ex.99.1 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000000753626000150/arw-ex99d1.htm","excerpt":"Consolidated sales of $11.55 billion to $12.15 billion","as_of":"2026-11-05","retrieved_at":"2026-11-08","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Tickflow：8 位分析師共識 Hold，平均目標價 $215（資料至 2026-08-03）","source":"Tickflow ARW forecast","url":"https://tickflow.io/stock/ARW/forecast","excerpt":null,"as_of":"2026-08-03","retrieved_at":"2026-11-08","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga：5 位分析師均價 $190，高 $250、低 $132（無日期）","source":"Benzinga ARW sentiment","url":"https://www.benzinga.com/quote/ARW/sentiment","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-11-08","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat：2026-05-12 共識 Moderate Buy，均價目標 $183.75","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/arrow-electronics-nysearw-reaches-new-52-week-high-should-you-buy-2026-05-12/","excerpt":null,"as_of":"2026-05-12","retrieved_at":"2026-11-08","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共7份，僅1份含重大項目：2026-09-04 Item 1.01 應收帳款證券化額度修訂（到期延至2029-09-02、額度由15億增至17.5億美元、加入重大併購時槓桿比率臨時上調條款）；無併購、重編（4.02）、下市等重大項目。","source":"SEC EDGAR 8-K 申報清單／8-K 2026-09-04","url":"https://www.sec.gov/Archives/edgar/data/7536/000110465926105516/tm2624328d1_8k.htm","excerpt":"extending the maturity date from September 10, 2027, to September 2, 2029; (ii) increasing the facility limit from $1.5 billion to $1.75 billion; (iii) adding a step-up provision temporarily raising the maximum permitted leverage ratio in the event of certain material acquisitions","as_of":"2026-09-04","retrieved_at":"2026-11-08","affects":["valuation","triggers"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Avnet 計畫擴建比利時 Tongeren 配送中心作元件物流（出售 Technology Solutions 後釋出倉容），屬同業有限度的物流產能調整；未見 2026-2027 時程。","source":"Evertiq: Avnet European logistics (Tongeren)","url":"https://evertiq.com/design/43577","excerpt":"Avnet is planning to invest in its European logistic operations, and to expand its existing distribution centre in Tongeren, Belgium.","as_of":"2025-12-01","retrieved_at":"2026-11-08","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Avnet FY2026 Q4（截至2026-06-27）庫存天數季減6天至71天，管理層強調庫存投資與成本紀律平衡。","source":"Avnet 8-K ex99.1 2026-08-05","url":"https://www.sec.gov/Archives/edgar/data/0000008858/000000885826000066/avt-20260805xex99d1.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-11-08","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Arrow 2026年Q3營收年增39%，Global Components 回補需求下 backlog 與 book-to-bill 遠高於 1；Q3 營運現金流 -$441M，主因為支應客戶需求的營運資金投入（庫存/應收增加）。","source":"Arrow Electronics 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000000753626000150/arw-ex99d1.htm","excerpt":"Arrow Electronics (NYSE:ARW) today announced financial results for its third quarter of 2026.","as_of":"2026-11-05","retrieved_at":"2026-11-08","affects":["moat_trend","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Arrow 2026年Q2：三個地區 book-to-bill 皆明顯高於1，backlog 累積至2027上半年；庫存約$5.08B（8月），年增7.9%（聚合站數據，非公司披露）。","source":"Arrow Q2 2026 earnings presentation / 10-Q (July 4, 2026)","url":"https://www.sec.gov/Archives/edgar/data/0000007536/000110465926091983/arw-20260704x10q.htm","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-11-08","affects":["moat_trend"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"2026年電子零組件現貨價大漲：MLCC交期約40週、現貨較合約價高30-80%；ADI於2026年2月全線漲價15%；DRAM現貨價年增近700%（供應商部落格引述，方向性參考）。","source":"Accuristech / Utmel 2026 component price trend articles","url":"https://accuristech.com/blog/blog-electronic-component-cost-increase-2026/","excerpt":null,"as_of":"2026-05-31","retrieved_at":"2026-11-08","affects":["moat_trend","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Arrow Q4 2025 財報電話會議：管理層對2026仍謹慎，提及庫存正常化持續、宏觀地緣不確定；book-to-bill 回到1以上、backlog連續四季成長、庫存週轉正常化。","source":"MarketBeat Arrow Q4 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/arrow-electronics-q4-earnings-call-highlights-2026-02-06/?.tsrc=rss","excerpt":null,"as_of":"2026-02-06","retrieved_at":"2026-11-08","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Macrotrends 年均營業利益率：2022 約 5.41%、2023 約 4.95%、2024 約 3.35%（季度平均）；2024 單季 Q4 GAAP 營業利益率 2.7%（前年同期 4%）","source":"Macrotrends Arrow Electronics Operating Margin 2010-2025；StockStory Q4 CY2024","url":"https://m.macrotrends.net/stocks/charts/ARW/arrow-electronics/operating-margin","excerpt":null,"as_of":"2025-02-01","retrieved_at":"2026-11-08","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2024 年 Arrow 合併營收年減 16% 至 279 億美元，Global Components 年減 21%，歸因於週期性下行與客戶高庫存","source":"Panabee: Arrow Electronics Sales Plunge 16% to $27.9 Billion Amidst Semiconductor Downturn","url":"https://www.panabee.com/news/arrow-electronics-arw-q4-2024-earning-results","excerpt":null,"as_of":"2025-02-01","retrieved_at":"2026-11-08","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"Avnet FY2024 10-K 稱元件市場有週期性下行後接需求回升的歷史，本輪下行始於 2023 下半年，持續時間不確定","source":"Avnet Form 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/8858/000000885824000030/avt-20240629x10k.htm","excerpt":null,"as_of":"2024-08-01","retrieved_at":"2026-11-08","affects":["triggers","thesis.R"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 共7份，無 Item 4.02（財報不可信賴／重編）；僅1份含重大項目（證券化額度修訂）。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000007536&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"ARW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.43,"operating_margin_pct":4.02,"fcf_margin_pct":4.03,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARW","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AVT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":10.43,"operating_margin_pct":3.11,"fcf_margin_pct":-1.28,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVT","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SNX","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":6.89,"operating_margin_pct":2.71,"fcf_margin_pct":-1.08,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNX","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CDW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.0,"operating_margin_pct":7.03,"fcf_margin_pct":3.81,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDW","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WCC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.5,"operating_margin_pct":5.57,"fcf_margin_pct":1.6,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WCC","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"ARW"},"financial_history":{"ticker":"ARW","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":37124422000.0,"revenue_yoy_pct":null,"gross_margin_pct":13.03,"operating_margin_pct":5.61,"net_income":1426884000.0,"diluted_eps":21.8,"free_cash_flow":-111913000.0,"fcf_margin_pct":-0.3,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":33107120000.0,"revenue_yoy_pct":-10.82,"gross_margin_pct":12.53,"operating_margin_pct":4.7,"net_income":903505000.0,"diluted_eps":15.84,"free_cash_flow":622164000.0,"fcf_margin_pct":1.88,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":27923324000.0,"revenue_yoy_pct":-15.66,"gross_margin_pct":11.79,"operating_margin_pct":3.26,"net_income":392074000.0,"diluted_eps":7.29,"free_cash_flow":1037710000.0,"fcf_margin_pct":3.72,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":30852935000.0,"revenue_yoy_pct":10.49,"gross_margin_pct":11.24,"operating_margin_pct":3.04,"net_income":571266000.0,"diluted_eps":10.93,"free_cash_flow":-37205000.0,"fcf_margin_pct":-0.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ARW/ARW_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Arrow Electronics, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Good day, and welcome to the Arrow Electronics Third Quarter 2026 Earnings Call. Today's conference is being recorded.
At this time, I would like to turn the conference over to Michael Nelson, Arrow's Vice President of Investor Relations. Please go ahead.

**Michael Nelson** (Executives):
Thank you, operator. I'd like to welcome everyone to the Arrow Electronics Third Quarter 2026 Earnings Conference Call.
Joining me on the call today is our Interim Chief Executive Officer, Bill Austen; our Chief Financial Officer, Raj Agrawal; our President of Global Components, Rick Marano; and our President of Global Enterprise Computing Solutions, Eric Nowak.
During this call, we'll make forward-looking statements, including statements about our business outlook, strategies, plans and projections regarding future financial results, which are based on our predictions and expectations as of today. Our actual results could differ materially due to a number of risks and uncertainties, including due to the risk factors and other factors described in this quarter's associated earnings release and our most recent annual report on Form 10-K and other filings with the SEC.
We undertake no obligation to update publicly or revise any of the forward-looking statements as a result of new information or future events. You can access our earnings release at investor.arrow.com, along with a replay of this call. We've also posted a slide presentation on this website to accompany our prepared remarks and encourage you to reference these slides during this webcast.
As a reminder, some of the figures we will discuss on today's call are non-GAAP measures, which are not intended to be a substitute for our GAAP results. We've reconciled these non-GAAP measures to the most directly comparable GAAP financial measures in the accompanying slide presentation. Following our prepared remarks today, Bill, Raj, Rick and Eric will be available to take your questions.
I'll now hand the call over to our Interim CEO, Bill Austen.

**William Austen** (Executives):
Thank you, Michael, and good morning, everyone. We appreciate you joining us for a discussion of our third quarter 2026 results. I would like to start by recognizing our global teams for their continued dedication and disciplined execution. Their commitment to supporting our customers and suppliers has been instrumental in driving another quarter of excellent performance.
Beginning on Slide 3, we delivered another quarter of strong results with record total revenue and EPS. Total revenue of $10.7 billion increased 39% year-over-year, while non-GAAP operating margin expanded 130 basis points year-over-year to 4.1%. Strong revenue growth and positive operating leverage resulted in non-GAAP diluted EPS of $6.22, representing a significant year-over-year earnings growth of 158%.
Our strong performance this quarter was fueled by 4 key drivers that contributed meaningfully to our performance. First, focused execution across the business, including effective management of expenses and working capital while serving strong customer demand. Second, positive operating leverage resulting in meaningful year-over-year margin improvement. Third, sustained unit volume demand, combined with pockets of limited capacity resulted in increased benefit from price inflation. And fourth, continued contribution of higher-margin value-added services.
From a segment perspective, both global components and global ECS contributed to our strong performance. Our global components demand remains strong and broad-based across geographies, verticals and customers, and our leading indicators continue to give us confidence in the durability of demand and the sustainability of growth. Book-to-bill ratios remain well above parity, while our backlog continues to build into mid-2027, improving our visibility. We have also seen lead times gradually extend but remain lower than a pervasive shortage environment.
ECS posted a strong quarter, exceeding expectations through a combination of robust customer demand and improved backlog conversion. Demand continues to build across key technology categories, including AI, cloud, cybersecurity and hybrid infrastructure, driving healthy growth in our billings and backlog.
Turning to Slide 4. Arrow remains well positioned to deliver long-term growth. We've discussed 4 pillars of our investment thesis over the past several quarters, and we continue to execute in these areas to further drive strength in our business model to solidify our competitive positioning.
First, Arrow maintains a strong position across its 6 large and growing core end markets: industrial, transportation, aerospace and defense, medical, consumer electronics and data centers. Each of these markets is supported by an attractive secular demand trends that continue to create growth opportunities.
Second, our differentiated capabilities continue to drive profitable growth as we expand into higher-margin value-added services.
Third, Arrow's combination of global components and ECS creates a diversified business model that provides financial flexibility. I'd like to spend a moment here on ECS and highlight the progress we have made against our strategy to become the leading aggregator of AI and hybrid cloud solutions for the mid-market.
Central to this strategy is our highly scalable value-added model, which provides technology suppliers with significant reach while expanding access and capabilities for our channel partners. Arrow's scale is especially important because it allows us to connect the world's leading technology providers with channel partners and end customers as demand continues to grow for AI, cloud, cybersecurity and hybrid infrastructure solutions.
The ongoing build-out of AI is driving customers to modernize their technology environments. Customers are investing in additional compute, storage, networking and cybersecurity capabilities to support growing data and performance requirements while also expanding their use of cloud-based solutions. For Arrow, these trends are being driven primarily by mid-market and enterprise customers who are increasingly deploying hybrid environments that blend cloud adoption with upgrades to their on-premise infrastructure. As a result, we're seeing healthy demand across the core technologies that underpin AI readiness, digital transformation and long-term IT modernization.
We're seeing continued validation of our strategy through recognition from some of the industry's most important players, including NetApp, where we were recognized as the North America Distributor of the Year for 2026, reflecting the strength of our partnership and success driving growth across the channel. HPE, where we extended our partnership through the addition of distribution rights for the Juniper product lines across North America and select EMEA markets, further enhancing our ability to deliver HPE's full portfolio to channel partners.
IBM, where we expanded our long-standing relationship through additional distribution coverage across 7 additional countries in EMEA, increasing our reach and scale with this strategic supplier. Oracle, where we were recognized as the Global Cloud Distributor of the Year, reflecting accelerated Oracle Cloud adoption through partner recruitment, technical enablement and joint go-to-market initiatives. And finally, IDC, where we were recognized as a cloud platform leader, reflecting ArrowSphere's differentiated cloud life cycle management capabilities reinforced by recent Microsoft and AWS Distributor of the Year recognitions.
These achievements highlight the strength of ECS' value proposition underpinned by our expanding ecosystem and category leadership, our deepening strategic supplier relationships and our growing exposure to high-growth technologies. ECS continues to be uniquely positioned as a critical enabler of technology adoption, and we remain confident in our ability to drive long-term growth and value creation for this segment in the years ahead.
Turning back now to our investment thesis. Fourth and finally, our capital allocation priorities remain unchanged. We are focused on maximizing long-term shareholder value by deploying capital towards opportunities that offer attractive long-term risk-adjusted returns while maintaining our investment-grade rating.
Turning to Slide 5. Our strong third quarter performance reflects the continued momentum and strong operational execution across the business. We remain focused on expanding our portfolio of solutions and capabilities across both global components and ECS for higher-margin value-added services. We are confident these offerings will deepen customer engagement, broaden our market opportunities and drive sustainable growth.
We are equally committed to delivering profitable growth and driving positive operating leverage through disciplined execution and effective financial management. We're encouraged by the strength across our business and are excited about the opportunities ahead as we continue executing our strategy to deliver sustainable long-term shareholder value.
With that, I'll turn it over to Raj to discuss our financial performance in more detail.

**Rajesh Agrawal** (Executives):
Thanks, Bill. On Slide 6, sales for the third quarter increased $3 billion year-over-year to $10.7 billion, representing a record level and up 39% versus prior year. Third quarter consolidated non-GAAP gross margin as a percent of sales was 10.8%, flat versus the prior year. Our third quarter non-GAAP operating expenses increased $104 million year-over-year to $719 million, primarily driven by variable costs. Importantly, non-GAAP OpEx as a percent of gross profit declined 11.6 percentage points year-over-year to 62.3%.
We remain focused on disciplined profitable growth and our improved operational efficiency is driving substantial operating leverage in the business model. In the third quarter, non-GAAP operating income increased $219 million year-over-year to $436 million. Non-GAAP operating margin rate expanded 130 basis points year-over-year to 4.1% of sales. Interest and other expense was $40 million in the third quarter as we benefited from lower average debt levels throughout the quarter, and our non-GAAP effective tax rate was 19% as we benefited from a tax settlement.
Finally, non-GAAP diluted EPS for the third quarter increased 158% year-over-year to $6.22, a record EPS for Arrow. This was above our guidance range driven by a number of factors, primarily favorable sales volume and operational leverage from our productivity initiatives, along with lower interest expense and the aforementioned tax settlement.
Turning to Slide 7. Let's take a closer look at our Global Components business. Global components sales increased $577 million sequentially to $7.9 billion in the quarter, above our guidance range and up 8% versus prior quarter. Global components non-GAAP operating income increased $16 million sequentially to $413 million, up 4% from the prior quarter. Non-GAAP operating margin declined 20 basis points sequentially to 5.2% and was up 160 basis points versus the prior year and well ahead of expectations.
Our strong results reflect continued momentum across the business. Our growth remains broad-based, spanning geographies, end markets and customer segments, reinforcing our confidence that demand is being driven by a diverse and healthy set of underlying factors.
First, book-to-bill ratios remain well above parity. Second, lead times extended further during the quarter, though they remain well below prior peak levels. Third, our backlog continued to build and now extends into the middle of 2027, providing us with greater visibility and supporting our view that demand remains durable. Lastly, interconnect, passive and electromechanical components, or IP&E, continues to grow, surpassing $1 billion in sales for the third consecutive quarter.
These leading indicators strengthen our confidence in both the sustainability of current growth trends and the underlying health of the market. Importantly, demand trends remain resilient from a unit volume perspective, demonstrating continued stability in end market consumption. However, pockets of limited capacity are leading to price inflation with certain component categories, most notably memory. Higher prices are benefiting both revenue and profit dollars.
In addition to product distribution, our value-added capabilities remain an important differentiator. Customers continue to leverage our supply chain services, engineering and design and integration services to navigate an increasingly complex environment. These higher-value engagements not only deepen customer relationships, but also contribute meaningfully to profitability and reinforce the strategic role we play across the electronics ecosystem.
Taking a closer look at each of the regions. In the Americas, sequential sales growth was broad-based, highlighted by strength in aerospace and defense, industrial, transportation and computing. In EMEA, the market was underpinned by sequential strength in aerospace and defense and networking. And finally, in Asia, sequential growth was driven by industrial, networking and transportation.
Turning to Slide 8 and our global ECS business. In the third quarter, global ECS sales increased $619 million year-over-year to $2.8 billion, above our guidance range and up 29% versus the prior year or up 30% year-over-year on a constant currency basis. Total ECS billings were $5.9 billion, up 14% year-over-year.
Third quarter non-GAAP operating income increased $34 million year-over-year to $99 million, up 53% from the prior year. Non-GAAP operating margin increased 60 basis points year-over-year to 3.6%. Our third quarter results significantly exceeded expectations, driven by strong demand and our ability to convert a larger percentage of backlog into revenue. Strong execution across the organization, combined with product availability and customer readiness enabled us to accelerate backlog conversion and deliver results ahead of expectations.
We also made important progress on 2 underperforming multiyear contracts with one of our beyond distribution partners. We terminated one contract, which we discussed last quarter as well as successfully restructured another key contract with the same partner this quarter. The result of both of these actions put the business on a healthier trajectory and has created a stronger foundation for future growth and profitability. We are encouraged by the early results and believe these actions better align the business with our long-term strategic objectives.
Demand trends remain favorable with investments in AI and broader infrastructure modernization continuing to shape technology spending. Consistent with these trends, we delivered year-over-year growth across nearly every major area of strategic focus within the business, including compute solutions, business applications, storage, security and cloud and hybrid cloud offerings. As organizations continue to modernize their environments and prepare for the next wave of AI-driven adoption, we believe Arrow remains well positioned to help customers navigate that transition while driving profitable growth across the business.
Turning to the balance sheet on Slide 9. Net working capital grew sequentially in the third quarter by approximately $900 million, ending the quarter at $7.7 billion. Inventory grew sequentially by $1.4 billion, ending the third quarter at $7.3 billion. Nearly half of the inventory build was related to data center activity within our Arrow Intelligent Solutions. In this offering, we're helping to design, build and test the compute and storage infrastructure needed to run AI workloads. And this value-added service is a margin-accretive business for Arrow.
As we continue to experience robust demand, we will strategically invest in inventory that is needed to support our customers. Importantly, our investments are driving attractive returns and the financial metrics that we monitor continue to illustrate a healthy business profile. Non-GAAP return on working capital increased 10.6 percentage points year-over-year, finishing the third quarter at 22.6%. Likewise, non-GAAP return on invested capital increased 7.8 percentage points year-over-year, finishing at 15.1%. Working capital as a percent of sales finished the third quarter at approximately 18% and our cash conversion finished at 78 days.
Cash flow used for operating activities in the third quarter was $441 million. On a year-to-date basis, cash flow generated from operating activities was $577 million. Gross balance sheet debt at the end of the third quarter grew sequentially by $581 million and declined year-over-year by $378 million, finishing at $2.8 billion. Overall, our lower debt levels, along with increased profitability have improved our adjusted leverage ratio by over 1 turn the past 12 months to 1.9x, which provides us with increased financial flexibility. Finally, we repurchased $93 million in shares in the third quarter.
Now turning to Q4 guidance on Slide 10. We expect sales for the fourth quarter to be between $11.55 billion and $12.15 billion, representing an increase of 36% year-over-year at the midpoint of the range. We expect global component sales to be between $8.15 billion and $8.55 billion, representing sequential growth of 5% at the midpoint. Enterprise Computing Solutions should benefit from typical fourth quarter seasonality, which historically has been the strongest quarter of the year. We expect sales to be between $3.4 billion and $3.6 billion, which is up 22% year-over-year at the midpoint.
We're estimating a tax rate in the range of 23% to 25% and interest expense of approximately $50 million. Our non-GAAP diluted earnings per share is expected to be between $7 and $7.20. Details about the impacts of changes in foreign currencies can be found in our earnings release.
I'd like to offer some additional color on both of our segments. In Global Components, the sequential growth in our outlook is expected to be driven primarily by unit volume as the majority of supplier price increases took effect in the third quarter. Overall, the business remains healthy, supported by a more favorable geographic mix, continued mass market momentum, contributions from value-added services and ongoing leverage from our productivity initiatives.
In ECS, we expect hardware to represent a larger portion of revenue in the fourth quarter, which will drive a higher mix of sales recognized on a gross basis as we've seen throughout the year. We expect margins on a billings basis to be relatively unchanged from the prior year, demonstrating the resilience of the overall business. Altogether, our focused execution and financial discipline across the business position us to continue to build momentum against our strategic priorities while enhancing operating leverage and supporting long-term earnings growth.
With that, I'll now turn the call back over to Bill for closing remarks.

**William Austen** (Executives):
Thanks, Raj. Turning to Slide 11. As we look ahead, we remain focused on disciplined execution, building on the operational momentum we have established and further improving the quality of our growth. Arrow remains uniquely positioned at the intersection of several powerful secular growth trends. In global components, continued investment in artificial intelligence, aerospace and defense, industrial automation and the broader digitization of the mass market continues to create opportunities across our portfolio. We are increasingly seeing these trends expand beyond early adopters and large customers into a much broader base of enterprises and industrial customers.
At the same time, in ECS, as AI deployments continue to expand, customers are investing to modernize their technology stacks. Demand remains strong for compute, storage, networking, cybersecurity and cloud solutions as organizations build the infrastructure required to support increasingly sophisticated workloads.
The quality of growth across Arrow continues to improve. We are benefiting from a healthier mix of customers, geographies and value-added services, while strong execution is driving positive operating leverage throughout the business. As a result, we are not only delivering growth but doing so in a way that strengthens profitability and positions us for sustained performance. We are proud of the progress we have made, confident in the path ahead and remain focused on delivering sustainable long-term value for all of our stakeholders.
Finally, I'd like to share some recent leadership changes. After 22 years with Arrow, ECS President, Eric Nowak, has announced his plans to retire. He will remain in his role through the end of the year and will then serve as an adviser until the end of Q1 2027. I want to thank Eric for his exceptional leadership and many contributions to Arrow over the years.
We're pleased to welcome Rodney Clark, who will join Arrow on November 9 and will succeed Eric as President of ECS effective January 1. Rodney brings significant global leadership experience across the commercial, channel and technology sectors, having spent his career working closely with suppliers and customers. We look forward to welcoming Rodney as we continue to build on the success of ECS, deepen customer relationships and execute our strategic priorities.
Also, we're excited to welcome Anuj Gore as our Chief Information and Technology Officer effective November 9. Anuj brings extensive experience leading IT organizations and business transformations through prior senior leadership roles overseeing significant technology investments, acquisition integrations and AI frameworks.
I would also like to thank Raime Leeby, our Chief Strategy Officer, for her interim leadership of our global IT organization during this transition.
With that, Raj, Rick, Eric and I would be happy to take your questions. Operator, please open the call for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Will Stein with Truist Securities.

**Aidan Wilson** (Analysts):
It's Aidan on for Will. I was wondering if you could discuss the impact that memory prices had maybe in both segments, please?

**William Austen** (Executives):
Go ahead, Raj.

**Rajesh Agrawal** (Executives):
Yes. For the third quarter, memory prices were certainly up quite a bit. Most of our revenue growth in the components business was driven by price increases in the third quarter. We have not assumed a lot in terms of memory price increases or other things in the fourth quarter. That's primarily unit volume driven. Having said that, the demand environment continues to be extremely strong. If we had gotten our hands on more product, we would have sold more. And so the environment itself is very, very strong. We feel very good about where things are, and that's what we've assumed at this stage.

**Aidan Wilson** (Analysts):
Great. And then if I could sneak in another one. Could you maybe quantify how much the value-added services are contributing to profitability today?

**Rajesh Agrawal** (Executives):
Well, for last year, they contributed about 30% of our operating profit as a company. This year, because we've had so much growth in the rest of the company and in our core components business, that number is going to be lower than it was last year. We haven't quantified it yet, but it's certainly going to be drifting lower, not because it's not performing well, but primarily because everything else is growing so much this year. So it's still a significant contributor to our bottom line.

**Aidan Wilson** (Analysts):
Awesome.

**Operator** (Operator):
Your next question comes from the line of Ruplu Bhattacharya from Bank of America.

**Ruplu Bhattacharya** (Analysts):
My first question relates to working capital. Raj, a couple of things. The inventory was up $1.4 billion sequentially. You mentioned Arrow Intelligent Solutions, and you said something about building compute and storage. Can you just kind of describe what that business is? Is this a manufacturing business? What are the margins in that business? And how big is it from a revenue standpoint?
And the second question I have on working capital is, if we look at Slide 9, it looks like DSO and DPO both have increased about 100 days year-on-year. So what -- is it that you're having to give more payment terms, extended payment terms to clients? Or is this related to supply chain services business? If you can just kind of explain or describe what's happening with the DSOs and the DPOs, and I have a follow-up.

**Rajesh Agrawal** (Executives):
Yes. Maybe I can start with the -- you want to start, Bill?

**William Austen** (Executives):
Ruplu, this is Bill. On the AIS, what we call Arrow Intelligent Solutions, that's AIS. That's what we've talked about in the past. It's part of our value-added services. And that's where we build specific appliances that are low volume, high-mix for customers. So we have got business with lots of customers building racks, storage, compute racks. And the inventory is up because we have large orders in the pipeline that didn't ship within the quarter, and they're just going to ship within the next quarters. We need to bring that inventory in ahead of time so that we can build it, test it, and then ship it. So that's all going to go through. And of the $1.4 billion of inventory, about $600 million of that would have been related to AIS.

**Rajesh Agrawal** (Executives):
Yes.

**William Austen** (Executives):
And I'll let Raj answer the other part of the question.

**Rajesh Agrawal** (Executives):
Yes. And the second part of your question, Ruplu, you're right, the DSOs and DPOs are up about 100 days year-on-year. That's being primarily driven by our supply chain services offering. Just as a reminder, that's a working capital-light offering that we have, but we are settling AR and AP in that business. And so you will see those things ballooning out. So nothing different than we've been calling out every call. So it's the same factors that are driving it. So nothing unusual there.

**Ruplu Bhattacharya** (Analysts):
Okay. Can I ask a follow-up on margins, specifically for the ECS segment margins? The fourth quarter is typically a strong quarter. And when we look year-on-year, I mean, it typically has good growth. I mean you get into the 6 handle in terms of operating margins. You made a point that this year, you're going to have more hardware versus software and services. So how does that impact -- was there any -- is there anything to keep in mind as we model out operating margin for ECS in the fourth quarter?

**Rajesh Agrawal** (Executives):
Yes. Yes, let me start and then, Eric, please feel free to add in. The margins for ECS, the net sales are driven by more hardware sales, as we had mentioned. And so that does depress reported margins on a net sales basis, but you also have to look at billings-based margins, Ruplu, in that business in particular because the mix can change quite a bit between hardware and software, that has a direct impact to net sales reported margins. But billings-based margins in the third quarter were up actually year-over-year. And then in the fourth quarter, we see billings-based margins being relatively flat year-on-year. And so that's a great indicator of the true health of the performance of that business.
So the business is firing on all cylinders. Yes, you're right, the net sales margins have historically been above 6% in the fourth quarter. But -- and we're implying something that's lower than that in this fourth quarter, but nothing has really changed there, and we're actually doing very well in the business.
Eric, do you want to add anything to that?

**Eric Nowak** (Executives):
Yes. It's exactly as Raj described. It's difficult for us to basically manage the mix of the business. We had much more hardware sales in Q3. It will be the same in Q4 because our suppliers are very efficient in our ability to ship the hardware. And that's why basically on a net sales basis, the margins are down. But on a billings basis, which is what we are looking for, it's -- but it's flat. So basically, it's on track.

**Operator** (Operator):
Your next question comes from the line of Melissa Fairbanks with Raymond James.

**Melissa Dailey Fairbanks** (Analysts):
Doing well. Drinking from the firehose, it feels like. But -- yes, congrats on the results, and I know it's extremely difficult to model these businesses. 
Raj, I think in answering -- I think it was Will Stein's question, the first question, you mentioned if you had been able to get more inventory, you could have shipped more through. And I know what we've heard from some of your supplier partners over the past couple of weeks is that lead times are extending, channel inventories are probably at record lows in Asia, in particular, starting to come down in Europe. U.S. is a little bit higher. But just wondering what you are seeing in terms of lead times, channel inventories, availability, your ability to meet end market demand?

**Rajesh Agrawal** (Executives):
Melissa, maybe I'll give it to Rick Marano. He's the expert here, and so I will let him speak to it.

**Richard Marano** (Executives):
Yes. Melissa, I guess I'd answer the question this way overall. We've talked about this in the past. We've talked about the recovery and how the recovery has gradually come along. And if you think about it through that lens, as what we call the mass market customer base comes back and continues to come back, they come back to lead times that are expanding as well. And as lead times expand, obviously, our ability to turn inventory or get inventory becomes a little bit more constrained. It doesn't mean in any way, shape or form that we believe that we're not getting our fair share of inventory. What we're saying is the contribution of a market that's recovering, lead times are expanding and those converging just means it gets more difficult to get inventory in when we want to get inventory in.
What I would say is this is look at it from a perspective of the health of the market overall and take outside of it, look outside the traditional verticals to which we look at, if you expand it and look at areas like robotics or automation or power, things of that nature, all those segments are coming back, and they're coming back strong, and they're coming back globally as well. So it's a nice healthy recovery. It continues to recover. Lead times continue to expand, but lead times have not expanded like we saw in the COVID period in any way, shape or form yet. So it's -- of course, if we can get more inventory, we could turn more inventory, but we are getting a fair amount of inventory, and it's reflective of what we see in our bookings and our backlog out in future quarters.

**Melissa Dailey Fairbanks** (Analysts):
Okay. That's super helpful. Maybe as a follow-up, you mentioned some of these end markets where there are higher value end markets like in aerospace and defense and some of the industrial automation, robotics, all of those types of areas. Are you starting to see any behavior on behalf of the suppliers where they're going to hold more internally and not push inventory out to distributors like what we saw during the COVID times? Or is this still -- we're still business as usual? It's just extended lead times?

**Richard Marano** (Executives):
I think it's business as usual and extended lead times. And I think, quite honestly, that's reflective of what we're seeing, Melissa, when we look out in time, and Bill and Raj both talked about visibility as we move out into the first half of '27. And that visibility is reflective of a recovery across the mass market and these vertical markets as well. So I don't, in any way, shape or form, see suppliers in any way not giving us product based off the end market or technology.

**William Austen** (Executives):
Yes. No, Melissa, our backlogs and our -- if you look at our sales sequentially in some of the markets that Rick talked about, robotics, power conversion, energy, automation, sequentially, these are increasing rapidly on a -- from a sales basis, and our backlog is increasing in those categories as well. So we see this as a very broad-based cycle, if you will, beyond just storage and compute, transportation, aerospace and defense. We're now starting to see the mass market coming back with a lot of momentum.

**Melissa Dailey Fairbanks** (Analysts):
Great. Keep up the good work, guys.

**Richard Marano** (Executives):
Thanks, Melissa.

**William Austen** (Executives):
Thanks.

**Operator** (Operator):
There are no further questions at this time. I will now turn the call back to Bill Austen for closing remarks.

**William Austen** (Executives):
Thank you. Thank you, everyone, for joining today, and I look forward to speaking with all of you soon. I also want to take a moment to thank all of my Arrow colleagues for delivering an excellent result in Q3, and I'm really looking forward to Q4. Have a great day, everybody.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ARW_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：Q3 總營收財測區間（原話："We expect sales for the third quarter to be between $9.6"）
- 2026-08-06｜CFO｜guidance：Q3 Global Components 營收財測與季增中點（原話："We expect Global Component sales to be between $7.5 billion and $7.9 billion"）
- 2026-08-06｜CFO｜guidance：Q3 非 GAAP EPS 財測區間（原話："Our non-GAAP diluted earnings per share is expected to be between $4.83 and $5.03."）
- 2026-08-06｜CFO｜guidance：Q3 ECS 財測年增僅約 2%，管理層歸因於去年大型夥伴加入的基期（原話："reflects growing over a large"）
- 2026-08-06｜CFO｜guidance：供應鏈服務 Q3 獲利回到正常水準，下半年零組件優於季節性（原話："Supply Chain Services is expected to return to"）
- 2026-08-06｜CFO｜guidance：ECS 全年帳單成長預期維持低雙位數（原話："We still expect to"）
- 2026-08-06｜CFO｜margin：營業費用占毛利比下降至 64.1%（原話："non-GAAP OpEx as a percent of"）
- 2026-08-06｜CFO｜margin：Components 營益率季減 10bp 至 5.4%，年增 180bp（原話："modestly declined 10 basis points sequentially to 5.4%"）
- 2026-08-06｜CFO｜margin：漲價約貢獻 Components 季增營收的三分之一（原話："Price inflation contributed roughly 1/3 of the sequential revenue"）
- 2026-08-06｜CFO｜margin：記憶體占 Components 營收低雙位數百分比（原話："Memory now represents a low double-digit percentage of"）
- 2026-08-06｜CFO｜margin：ECS 營益率因一次性合約費用下滑 100bp，約 2,700 萬美元（原話："That equates to $27 million."）
- 2026-08-06｜CFO｜margin：排除該費用，ECS 營益率會明顯高於 4%（原話："Had it not been for the charges, the margins would have"）
- 2026-08-06｜CFO｜margin：Components 上半年營益率約 5.5%，Q3 預期回到 5% 左右（原話："I would be surprised if we didn't get to 5% margins"）
- 2026-08-06｜CFO｜margin：營運現金流部分來自供應鏈服務時點效應，可能回吐（原話："may partially unwind as the year progresses"）
- 2026-08-06｜CFO｜commitment：管理層預告下半年 ECS 還會有費用，但規模小於 Q2（原話："I do expect some more charges in the second half of the year"）
- 2026-08-06｜CFO｜commitment：預期 Q4 ECS 仍有很高的營益率，但提醒出貨日數差異（原話："we'll expect to see very high margins"）
- 2026-08-06｜CEO｜commitment：CEO 表示在董事會結束接班程序前持續擔任代理 CEO（原話："I'm not going"）
- 2026-08-06｜CFO｜capital_allocation：Q2 回購 4,300 萬美元（原話："we repurchased $43 million in shares in the second quarter."）
- 2026-08-06｜CFO｜capital_allocation：調整後槓桿降至 1.75x（原話："improved our adjusted leverage ratio by over a turn"）
- 2026-08-06｜CEO｜capital_allocation：資本配置框架：再投資、併購、回饋股東並維持投資等級（原話："while maintaining an investment-grade credit rating"）
- 2026-08-06｜CFO｜customer：訂單出貨比在三大區域均明顯高於 1，積壓訂單延伸到 2027 上半年（原話："Book-to-bill ratios continue to increase and remain well above 1 in all 3 regions."）
- 2026-08-06｜CFO｜customer：ECS 積壓訂單年增逾 75%，創新高（原話："healthy backlog growth of over 75% year-over-year"）
- 2026-08-06｜President, Global Components｜customer：客戶正在把緩衝庫存加回供應鏈（原話："Customers are now adding"）
- 2026-08-06｜CEO｜customer：管理層說未見需求被價格破壞（原話："No, we don't see demand destruction in"）
- 2026-08-06｜CEO｜customer：一家供應商關係結束，營收規模約 7 億美元而非報導的 14 億（原話："It was a misreport on the $1.4 billion."）
- 2026-08-06｜President, ECS｜customer：ECS 主管表示該供應商合約結束對營收與獲利無影響（原話："there will be no impact in terms of revenue and margin and profits for ECS"）
- 2026-08-06｜President, ECS｜competition：ECS 主管說分歧原因是對方要能同時做 PC 量販的經銷商，Arrow 不是（原話："we are not a volume distributor, a"）
- 2026-08-06｜CFO｜product：記憶體與 SSD 短缺壓抑地端硬體，ECS 轉向軟體與公有雲方案（原話："hardware solutions for on-premise storage and compute remain constrained by thin supply"）
- 2026-08-06｜CEO｜product：ECS 各產品線年增：資安 21%、運算 51%、商用軟體 26%（原話："security is up 21%, compute is"）
- 2026-08-06｜CFO｜product：IP&E 營收連續第二季超過 10 億美元（原話："surpassing $1 billion in sales for the second consecutive quarter"）
- 2026-08-06｜CFO｜risk：ECS 與一家策略夥伴的 beyond-distribution 合約虧損，已終止一項並仍在重整另一項（原話："We have now terminated one key element of our beyond-distribution agreement with this partner"）
- 2026-08-06｜CFO｜risk：交期持續拉長但管理層稱仍低於全面缺貨環境（原話："they remain lower than a pervasive shortage"）
- 2026-08-06｜CFO｜risk：管理層承認有多項因素可能影響季間時點與線性（原話："a number of"）
- 2026-08-06｜CEO｜risk：CEO 回答週期位置：自稱處於第二局（原話："I would say we're in the second inning"）


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

## ⑥ 條件附卡（archetype_hint='循環/商品' 命中）：judge_addendum_cyclical.md

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
{"date":"20260523","verdict":"B（衛星觀望·thesis 完整 AI 半導體 duopoly + ECS 結構成長，但 cycle peak 估值已透支、Pure MA 🟡 + BB 上軌突破，等回測 4W 均 $201 以下或 BB 中軌 $156 分批進場）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 半導體超級週期持續支撐 components 雙位數成長 + ARW pricing power 從 cycle 中真實提升","columns":{"2Y 驗證點":"FY26-FY27 components 平均 YoY +20-30%；GM 連 2 季 &gt; 11.5%","5Y 驗證點":"FY28-FY30 components 維持 mid-single 成長，GM 結構性站上 12.0%+","10Y 驗證點":"FY32-FY35 distribution 角色仍為 OEM 主流選擇（&gt; 60% mid-OEM 客戶 still ARW + AVT route）","具體數字門檻":"Q4 26 GM ≥ 11.7%（YoY 連 4 季正向）；FY28E EPS ≥ $18（共識若跌破 $16 觸發削弱）","信息來源":"SIA 半導體 2026 全球銷售預測 $975B、Counterpoint AI infra capex outlook、ARW 法說 2026 GM 目標","漂移觸發條件":"連 2 季 TTM GM 跌回 ≤ 11.2%（FY25 base）→ 削弱 🟡；連 3 季 + FY27 共識 EPS 下修 &gt; 15% → 反轉 🔴"}},{"id":"H2","text":"ECS（AI / Cloud / Network 整合）轉型為非 cyclical 結構成長段，2030+ 達到 35-40% 營收占比","columns":{"2Y 驗證點":"ECS YoY 維持 +20-30%（Q1 26 +39% 不可持續但 baseline 要在 +20% 以上）；ArrowSphere 訂閱 base 公開（目標：&gt; 25,000 active customers）","5Y 驗證點":"ECS 達到營收 30%+ 占比（vs FY25 base 28%）；ECS Op margin &gt; 5%（vs Components 4-5%）","10Y 驗證點":"ECS 占比 35-40%；變成 ARW 主要 valuation anchor 點，cyclical multiple 降為次要","具體數字門檻":"每季 ECS Op Income $200M+（vs Q1 26 $130M est.）；ArrowSphere TAM grow &gt; +30% YoY","信息來源":"ARW Investor Day 2024 ECS 目標、Gartner Cloud Marketplace 報告","漂移觸發條件":"連 2 季 ECS YoY &lt; +10%（成長放緩）→ 削弱；連 1 季 &lt; 0% → 反轉"}},{"id":"H3","text":"估值修復路徑：市場最終接受 ARW 為「半 cyclical / 半 secular」混合估值，Fwd PE re-rate 至 12-13x（vs 5Y 中位 ~10x）","columns":{"2Y 驗證點":"市場 EPS 共識 FY27 上修至 $25+（目前 $21.30）；分析師 Long-term EPS estimate 上修至 $20+","5Y 驗證點":"5Y 平均 Fwd PE rerate at 11-12x（vs 過去 5Y avg ~10x）","10Y 驗證點":"長期估值錨點 11-13x（不再被視為純 cyclical 6-10x business）","具體數字門檻":"Fwd PE 12 個月持續 &gt; 11x（不破壞 normalize 區間）；分析師 mean PT 上修至 $250+","信息來源":"Sell-side EPS revision Refinitiv、ARW investor relations re-rating thesis","漂移觸發條件":"連 6 個月 Fwd PE 跌回 &lt; 9x（市場拒絕 re-rate）→ 削弱；連 12 個月 + 跌破 8x → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Cyclical down cycle 提前 2027H1 啟動（vs 預期 2027H2/2028）→ EPS 跌回 $10-14 區間","columns":{"對應假設":"H1","時間尺度":"⚡ 短期 (1-2 季可觸發)","監測指標":"HBM/DRAM spot price 連 2 季 QoQ &lt; -10%、ARW components Op margin 連 2 季 &gt; -50bps YoY","警戒閾值":"連 2 季觸發即減倉 50%；spot price &gt; -20% QoQ 立即減倉至 0"}},{"id":"R2","text":"ECS 段成長失速（AI capex digestion 提前、ArrowSphere TAM 進入飽和）→ 結構性 thesis 破裂","columns":{"對應假設":"H2","時間尺度":"🔥 中期 (4-6 季)","監測指標":"ECS YoY &lt; +15% 連 2 季、ArrowSphere 新增客戶數 YoY &lt; 0","警戒閾值":"連 4 季 ECS &lt; +10% → 結構性 thesis review；連 1 季 ECS &lt; 0% → 立即降級 B → C"}},{"id":"R3","text":"Distribution 通路被結構性繞過（D2C e-commerce 大廠擴張、EMS 一條龍化）→ 10 年 share 由 18% 跌至 12-14%","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期 (2+ 年慢變數)","監測指標":"ARW 全球 share（Gartner / IBS Reports）、ARW top 50 大客戶 wallet share、annual revenue per active customer","警戒閾值":"跨 3 年觀察累積證據；需 ≥ 50% 機率才砍倉（避免短期新聞驚嚇）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":217.33,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARW_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
