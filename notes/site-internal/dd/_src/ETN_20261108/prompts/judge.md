你是 stock-analyst **v20 判斷 agent**，標的 ETN（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ETN","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ETN_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ETN_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":8947,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Eaton 新聞稿 8-K Ex.99（SEC）"},"note":"未查得"},{"id":"f_kpi1_segment_eaton_non_gaap","label":"Segment 營業利益／利益率（Eaton 以此替代 Non-GAAP 營業利益）","value":25.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%（營業利益 $2,263M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Eaton 新聞稿 8-K Ex.99（SEC）"},"note":"未查得"},{"id":"f_kpi2_eps_non_gaap","label":"調整後 EPS（Non-GAAP）","value":3.68,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Eaton 新聞稿 8-K Ex.99（SEC）"},"note":"未查得"},{"id":"f_kpi4_backlog_book_to_bill","label":"Backlog 與 book-to-bill","value":"Electrical 總 backlog 年增 +46%（Americas +33%、Global +121%）；Aerospace +33%；滾動 12 個月 book-to-bill：Electrical 1.2、Aerospace 1.2","period":"Q3 2026（截至 2026-09 底，公告於 2026-11-03）","unit":"YoY／倍","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（截至 2026-09 底，公告於 2026-11-03）","citation":"Eaton 新聞稿 8-K Ex.99（SEC）；美元 backlog 金額未揭露"},"note":"不適用"},{"id":"f_kpi5","label":"管理層指引","value":"Q4：有機成長 13–15%、segment margin 25.4–25.8%、調整後 EPS $4.05–$4.15、GAAP EPS $3.28–$3.38；全年：有機成長 13–15%（上修）、segment margin 24.1–24.5%、調整後 EPS $13.70–$13.80、GAAP EPS $10.39–$10.49","period":"Q3 2026（公告於 2026-11-03）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（公告於 2026-11-03）","citation":"Eaton 新聞稿 8-K Ex.99（SEC）；未提供 FCF 指引"},"note":"全年 FY1 共識 EPS 13.67（來源：consensus_revision，2026-11-07 快照），指引區間上緣略高"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-03","period":"2026-11-03","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_etn_gross_margin_pct","label":"ETN 毛利率","value":35.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_etn_operating_margin_pct","label":"ETN 營業利益率","value":17.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_etn_fcf_margin_pct","label":"ETN FCF 利潤率","value":11.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2308_tw_gross_margin_pct","label":"2308.TW 毛利率","value":35.27,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2308_tw_operating_margin_pct","label":"2308.TW 營業利益率","value":16.98,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2308_tw_fcf_margin_pct","label":"2308.TW FCF 利潤率","value":9.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_vrt_gross_margin_pct","label":"VRT 毛利率","value":38.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_operating_margin_pct","label":"VRT 營業利益率","value":20.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_fcf_margin_pct","label":"VRT FCF 利潤率","value":23.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_2301_tw_gross_margin_pct","label":"2301.TW 毛利率","value":23.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2301.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2301_tw_operating_margin_pct","label":"2301.TW 營業利益率","value":11.41,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2301.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2301_tw_fcf_margin_pct","label":"2301.TW FCF 利潤率","value":-6.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2301.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":1034,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Eaton 新聞稿 8-K Ex.99（SEC）：營業現金流 $1,310M－資本支出 $275M"},"note":"未查得"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":341.72,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-14.68,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":36.99,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.15,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.65 → 13.67）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.18,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.31 → 16.28）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.05,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（18.93 → 18.94）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":13.67,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":16.28,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":18.94,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.18,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 13.51 → 13.67（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":34.14,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝88.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":88.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.15,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝49.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":49.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.78,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝58.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":58.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":25.0,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 13.67，分子＝快照價 341.72","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.966,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":20104.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 20922.0、現金 818.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":388.5,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":152862.22,"period":"2026-11-08","unit":"USD m","basis":"市值 132758.22 ＋ 淨負債 20104.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":33685.48,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":37420.13,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（27 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.54,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 341.72 / W52 382.26 / W104 357.58 / W250 268.53 / W250 13週斜率 1.27%"},{"id":"f_ma_w52","label":"52 週均線","value":382.26,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":357.58,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":268.53,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.27,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K 自述 Eaton 在電氣類與航太類分部競爭地位強、多數產品屬市場領導者之列；競爭要素為效能、技術、服務與價格。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000007/etn-20251231.htm","excerpt":"Eaton has a strong competitive position in these segments and, with respect to many products, is considered among the market leaders.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子承認新進入者可能衝擊其產品或區域市場地位；漲價等因應措施也可能損及市占。未點名具體新進入者。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000007/etn-20251231.htm","excerpt":"Our positions may also be impacted by new entrants into our product or regional markets.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"搜尋未找到具名新進入者或替代供應商搶單的來源；MarketsandMarkets 稱 Schneider、ABB、Eaton、Vertiv、Delta 合計約占資料中心電源市場 41–43%，無 Eaton 單獨份額與消長方向。","source":"MarketsandMarkets Top Data Center Power Companies","url":"https://vapt.marketsandmarkets.com/ResearchInsight/data-center-power-market.asp","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Eaton 2026Q2 資料中心有機營收成長約 65%，高於市場成長約 23%（轉述來源）。","source":"rallies.ai","url":"https://rallies.ai/news/eaton-jumps-as-ai-data-center-power-demand-narrative-reasserts-amid-strong-2026-outlook","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Eaton FY2024 10-K：2024/2023/2022 無單一客戶占淨銷售超過 10%","source":"capedge ETN 10-K FY2024","url":"https://capedge.com/filing/1551182/0001551182-25-000006/ETN-10K-2024FY/file/144/data","excerpt":null,"as_of":"2025-02-28","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Eaton FY2025 10-K 揭露 2025、2024、2023 年皆無單一客戶占淨銷售超過 10%。","source":"SEC EDGAR 10-K FY2025 Other Information","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000007/etn-20251231.htm","excerpt":"Other Information No single customer represented greater than 10% of net sales in 2025, 2024 or 2023, respectively.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Eaton Q3 2026: Electrical Americas data-center sales +54%，電力業務積壓訂單超過 $20B（+46%），管理層上調 2026 展望（搜尋摘要轉述，未讀原頁）","source":"MarketBeat, Eaton Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-eaton-q3-earnings-call-highlights-2026-11-03/","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Eaton 新產能時程：南卡羅來納變壓器廠（$340M）預計 2027 投產；內布拉斯加中壓開關設備廠預計 2027 上半年開工；變壓器全球擴產潮預計 2026 起至 2028，大型變壓器交期仍 >12～24 個月（Rystad）","source":"搜尋彙整：Rystad Energy grid equipment market outlook / 產業報導","url":"https://www.rystadenergy.com/insights/grid-equipment-market-outlook","excerpt":null,"as_of":"2026-06-06","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Power Magazine 摘要：斷路器與開關設備市場有顯著供給過剩，但產能投資有限，限制可能在採購與專案排程而非產能；另有觀點認為缺口是採購做法造成","source":"POWER Magazine, Making the Connection executive summary (Sept 2025)","url":"https://www.powermag.com/wp-content/uploads/2026/01/making-the-connection-executive-summary-september-2025.pdf","excerpt":null,"as_of":"2025-09-30","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"JPMorgan（經 Nasdaq 引述）：2027 規劃資料中心容量超過 60% 尚未開工；分析指 Eaton 資料中心訂單成長由 Q1 的 240% 降至 Q2 的 85%，電力 Americas 積壓成長由 44% 降至 33%（皆為搜尋摘要，來源品質混雜）","source":"Nasdaq, data center delays create opportunity","url":"https://www.nasdaq.com/articles/data-center-delays-create-opportunity-these-3-stocks","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Eaton 資料中心美國 backlog 307 GW（Q2 2026），相當 15 年建置量","source":"Fool Q1 2026 transcript / pulse2","url":"https://pulse2.com/eaton-electrical-global-backlog-more-than-doubles-as-orders-rise-33/","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Eaton 2026 Q2 10-Q 法律或有事項列有反壟斷類訴訟，公司認為不致對財報有重大不利影響","source":"SEC EDGAR 10-Q（2026-06-30 季）","url":"https://www.sec.gov/Archives/edgar/data/0001551182/000155118226000030/etn-20260630.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Eaton 2026 Q3 10-Q 法律或有事項列有反壟斷與貿易管制類事項，最終結果若不如預期可能有重大不利影響","source":"SEC EDGAR 10-Q（2026-09-30 季）","url":"https://www.sec.gov/Archives/edgar/data/0001551182/000155118226000040/etn-20260930.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Eaton 10-K FY2025 風險因素：貿易政策變動（關稅、制裁、配額）可能實質增加成本、衝擊產品毛利，並使出口至他國更困難或昂貴；供應商面臨關稅與貿易限制風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000007/etn-20251231.htm","excerpt":"Changes in various countries’ trade policies, including tariffs and duties, can materially increase costs for goods imported into the United States, which can lead to broader cost pressures even for goods that are not imported. If Eaton is unable to take mitigating actions, it could negatively impact product margins and our financial performance.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Eaton Q1 2026 10-Q：最高法院推翻部分 IEEPA 關稅，公司無法合理估計退款財務影響，截至2026-03-31未入帳。","source":"SEC EDGAR 10-Q Q1 2026","url":"https://www.sec.gov/Archives/edgar/data/0001551182/000155118226000013/etn-20260331.htm","excerpt":"previously imposed under the International Emergency Economic Powers Act (IEEPA), and thereafter, the Court of International Trade (CIT) ordered the Customs and Border Protection (CBP) to develop a process to refund tariffs imposed under IEEPA. We are evaluating the impact of these developments on our business and financial statements and cannot reasonably estimate the financial impact nor deem","as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Eaton FY2025 10-K 風險因子列出國際營運面對政治不穩、關稅與貿易限制、地緣事件造成供應鏈中斷（一般性揭露，無特定國家集中度）","source":"Eaton Corp plc Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000007/etn-20251231.htm","excerpt":"war or armed conflict, changes in government policies, expropriation, nationalization, and other political, economic, or social developments; complex and continually changing government laws, regulations and policies; increased tariffs, trade barriers, trade agreements, and other restrictions on international trade; trade laws and trade treaties that impact our effective tax rate; supply chain","as_of":"2026-02-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"Eaton 投資 3.4 億美元擴增美國三相變壓器產能，回應產業變壓器短缺","source":"Utility Dive","url":"https://www.utilitydive.com/news/eaton-transformer-production-shortage-investment/739932/","excerpt":"Wednesday that it will invest $340 million to increase U.S. production of its three-phase transformers in response to the ongoing transformer shortage. The company aims to help meet “record demand … from utility, large commercial, industrial and data center customers.” Production and hiring is expected to begin in 2027 at an Eaton production facility in Jonesville, South Carolina.","as_of":"2025-02-12","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026：Electrical Americas 營收 41.72 億美元、有機 +22%，資料中心銷售 +54%；Aerospace 12 億美元、+11%（有機 +6%）、營業利益率 24.9%（年減 100bp）；Electrical Global 27 億美元、+58%（含 Ultra PCS 併購）","source":"Eaton Q3 2026 8-K Exhibit 99 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001551182/000155118226000037/etn09302026exhibit99.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 滾動 12 個月有機訂單：Electrical Americas +39%、Electrical Global +51%、Aerospace +20%；電力備貨訂單 (backlog) 超過 200 億美元、年增 46%；全年有機成長指引由 11–13% 上調至 13–15%","source":"Eaton Q3 2026 results press release (Business Wire syndicated)","url":"https://offshoresource.com/business-wire/eaton-reports-record-third-quarter-2026-results-with-strong-organic-growth-accelerating-record-orders-and-backlog-raises-organic-growth-guidance/","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 財報電話會議：美國資料中心整體待建容量 307GW（約 2025 年建置速度的 15 年），僅約 20% 預期近期轉換，多數於 2028 年後交付；Electrical Americas book-to-bill 1.3；SST 試點訂單預計下半年下，出貨 2027 年底至 2028 初。未見 2027 營收指引","source":"MarketBeat, Eaton Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/eaton-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Eaton 10-K 風險因子自述：其產品所服務的資料中心等市場曾出現並可能持續出現突發的破壞性技術，可能衝擊終端市場；且新進入者可能影響其地位。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000007/etn-20251231.htm","excerpt":"Our products and services support innovative technology and mega trends, including, for example, data centers. These markets have experienced and may continue to experience the abrupt introduction of disruptive technologies, which may, in turn, negatively impact our end markets.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Siemens 與 Reinhausen 開發中壓固態變壓器供 800V DC AI 資料中心；Sungrow 2026-07 推出 800V DC SST（競爭者進入同一替代架構）","source":"Bayern Innovativ: New Transformer for Data Centers","url":"https://www.bayern-innovativ.de/en/emagazine/detail/new-transformer-for-data-centers","excerpt":"Siemens and Reinhausen plan to develop a solid-state transformer for medium-voltage grids up to 36 kV that will supply AI data centers with 800 V DC.","as_of":"2026-09-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Eaton 2025-08 以 8600 萬美元收購 SST 開發商 Resilient Power Systems，CEO 稱 AC 轉 DC 遷移為真","source":"Utility Dive: Eaton CEO AC-to-DC migration","url":"https://www.utilitydive.com/news/eaton-ceo-ac-to-dc-migration-is-real-because-of-large-power-savings/873887/","excerpt":"Eaton CEO: AC to DC migration for data centers ‘is real’ The electrical equipment giant says it’s poised to capitalize on the trend by investing in solid-state transformers.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Eaton 將成立以資料中心為核心的新事業部（由 Angie McMillin 領導，4/1 生效），整合分散的資料中心團隊，提供端到端電力與散熱方案；Boyd Thermal 收購已交割。屬組織／go-to-market 整合，非通路去中介或訂閱化。","source":"Manufacturing Dive, Eaton data center-focused segment","url":"https://www.manufacturingdive.com/news/eaton-ai-data-center-focused-segment-angie-mcmillin-liquid-cooling-boyd/815896","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Eaton 與 Proponent 延長經銷協議並擴大產品範圍（既有經銷通路延續，無去中介跡象）。","source":"Business Wire, Eaton Expands Product Offerings and Extends Distribution Agreement With Proponent","url":"https://www.businesswire.com/news/home/20251014642705/en/Eaton-Expands-Product-Offerings-and-Extends-Distribution-Agreement-With-Proponent","excerpt":null,"as_of":"2025-10-14","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Eaton 10-Q：2026-06-10 與 Dana 簽署 Reverse Morris Trust 分拆 Mobility 事業。","source":"SEC 10-Q FY2026 Q2","url":"https://www.sec.gov/Archives/edgar/data/0001551182/000155118226000030/etn-20260630.htm","excerpt":"Planned Separation of Mobility Business On January 26, 2026, Eaton announced its intention to separate its Mobility business segment from the rest of Eaton via a spin-off. On June 10, 2026, Eaton entered into definitive agreements with Dana Incorporated (Dana), whereby Eaton will separate the Mobility business and combine it with Dana in a Reverse Morris Trust (RMT) transaction (the","as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 (2026-11-03)：Eaton 調高全年調整後 EPS 指引至 $13.70–13.80（前次 $13.40–13.60），有機成長指引由 11–13% 上調至 13–15%；Q3 調整後 EPS $3.68，高於 Zacks 共識 $3.54；Q4 EPS 指引 $4.05–4.15","source":"Eaton Q3 2026 press release (Business Wire 轉載) / Zacks 引述","url":"https://offshoresource.com/business-wire/eaton-reports-record-third-quarter-2026-results-with-strong-organic-growth-accelerating-record-orders-and-backlog-raises-organic-growth-guidance/","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-31 Q2 後：全年 EPS 指引上調至 $13.40–13.60，高於當時共識約 $13.34；Q3 EPS 指引 $3.46–3.56 涵蓋共識 $3.51","source":"MarketBeat: Eaton releases Q3 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/eaton-nyseetn-releases-q3-2026-earnings-guidance-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-05 初次全年指引 $13.05–13.50、Q2 指引 $3.00–3.10，中點略低於當時共識（Q2 共識約 $3.12、全年約 $13.30）","source":"MarketBeat: Eaton updates Q2 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/eaton-nyseetn-updates-q2-2026-earnings-guidance-2026-05-05/","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價：Investing.com 快照平均 12 個月目標價 485.47（23 買、4 持有、1 賣，依 2026-10-20 Baird 重申）；Walnut 2026-08 平均 $457.75（25 位、中位 $480）；TickFlow 2026-07-31 平均 $431.88（11 位）；各源日期與家數不一致","source":"Investing.com consensus estimates / Walnut / TickFlow","url":"https://www.investing.com/equities/eaton-consensus-estimates","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"UBS 將 ETN 降至 Neutral，12 個月目標價由 $440 降至 $360，理由為估值偏高、近期盈餘上行空間有限（發布日期搜尋結果未載明）","source":"iTiger: UBS Downgrades Eaton to Neutral","url":"https://www.itiger.com/news/1127460499","excerpt":null,"as_of":"2026-11-08","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Eaton 於 2026-06-10 同意將 Mobility 業務與 Dana 以 Reverse Morris Trust 合併（Eaton 股東持 50.1%，另收約 11 億美元現金），預計 2027 Q1 完成；Boyd Thermal 於 2026-03-12 完成收購（約 95.5 億美元），2026-09-25 另同意以 8.1 億歐元收購 COL Group。","source":"WebSearch 摘要（Bloomberg Law／Eaton 8-K 彙整）","url":"https://news.bloomberglaw.com/mergers-and-acquisitions/eaton-to-merge-mobility-business-with-dana-in-10-billion-deal","excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K 法律或有事項附註：公司認為各項訴訟不會對合併財報造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Note 11","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000007/etn-20251231.htm","excerpt":"Although it is not possible to predict with certainty the outcome or cost of these matters, the Company believes they will not have a material adverse effect on the consolidated financial statements.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-16 8-K 僅為重編分部資訊（新增 Mobility 分部），明確不是 10-K 的修正或重編。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000034/etn-20261016.htm","excerpt":"The information in this Form 8-K is not an amendment to or restatement of the 2025 Form 10-K.","as_of":"2026-10-16","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"NHTSA 召回 25E076000（Eaton E-Locker 差速器，約 289 輛，2025-11-14 通報），規模小。","source":"vehiclesafetyrecalls.com／NHTSA","url":"https://vehiclesafetyrecalls.com/recall/25E076000","excerpt":null,"as_of":"2025-11-14","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Boyd Thermal 2026-03-12 完成收購（約 95.5 億美元）；2026-06-10 同意 Mobility 與 Dana 以 Reverse Morris Trust 合併，預計 2027 Q1 完成；2026-09-25 同意以 8.1 億歐元收購 COL Group。","source":"WebSearch 摘要（Bloomberg Law／Eaton 8-K 彙整）","url":"https://news.bloomberglaw.com/mergers-and-acquisitions/eaton-to-merge-mobility-business-with-dana-in-10-billion-deal","excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K 法律或有事項附註：公司認為各項訴訟不會造成重大不利影響；近 12 個月搜尋未見新的證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Note 11","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000007/etn-20251231.htm","excerpt":"Although it is not possible to predict with certainty the outcome or cost of these matters, the Company believes they will not have a material adverse effect on the consolidated financial statements.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"NHTSA 召回 25E076000（Eaton E-Locker 差速器，約 289 輛），2025-11-14 通報。","source":"vehiclesafetyrecalls.com／NHTSA","url":"https://vehiclesafetyrecalls.com/recall/25E076000","excerpt":null,"as_of":"2025-11-14","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"2026-10-16 8-K 僅重編分部資訊，明確非 10-K 修正或重編；搜尋未見 SEC 調查。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1551182/000155118226000034/etn-20261016.htm","excerpt":"The information in this Form 8-K is not an amendment to or restatement of the 2025 Form 10-K.","as_of":"2026-10-16","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ETN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.05,"operating_margin_pct":17.32,"fcf_margin_pct":11.87,"rd_intensity_pct":2.75},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"2308.TW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.27,"operating_margin_pct":16.98,"fcf_margin_pct":9.46,"rd_intensity_pct":8.39},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"VRT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.12,"operating_margin_pct":20.35,"fcf_margin_pct":23.74,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SU.PA","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SU.PA"},"note":"quarterly_income_stmt 無資料"},{"name":"2301.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.4,"operating_margin_pct":11.41,"fcf_margin_pct":-6.21,"rd_intensity_pct":5.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2301.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"ETN"},"financial_history":{"ticker":"ETN","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":20752000000.0,"revenue_yoy_pct":null,"gross_margin_pct":33.19,"operating_margin_pct":14.43,"net_income":2462000000.0,"diluted_eps":6.14,"free_cash_flow":1935000000.0,"fcf_margin_pct":9.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":23196000000.0,"revenue_yoy_pct":11.78,"gross_margin_pct":36.36,"operating_margin_pct":16.75,"net_income":3218000000.0,"diluted_eps":8.02,"free_cash_flow":2867000000.0,"fcf_margin_pct":12.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":24878000000.0,"revenue_yoy_pct":7.25,"gross_margin_pct":38.2,"operating_margin_pct":18.62,"net_income":3794000000.0,"diluted_eps":9.5,"free_cash_flow":3519000000.0,"fcf_margin_pct":14.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":27448000000.0,"revenue_yoy_pct":10.33,"gross_margin_pct":37.59,"operating_margin_pct":18.98,"net_income":4087000000.0,"diluted_eps":10.45,"free_cash_flow":3553000000.0,"fcf_margin_pct":12.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ETN/ETN_Q3_2026_Earnings_Call_20261103.md）

# Q3 2026 Earnings Call
**Eaton Corporation plc** | Earnings Calls | 2026-11-03

**Operator** (Operator):
Thank you for standing by, and welcome to the Eaton's Third Quarter 2026 Earnings Results Conference Call. [Operator Instructions] As a reminder, today's program is being recorded. And now I'd like to introduce your host for today's program, Yan Jin, Senior Vice President of Investor Relations. Please go ahead, sir.

**Yan Jin** (Executives):
Good morning. Thank you all for joining us for Eaton's Third Quarter 2026 Earnings Call. With me today are Paulo Ruiz, Chief Executive Officer and Dave Foster, Executive Vice President and Chief Financial Officer.
Our agenda today includes opening remarks by Paulo, then we'll turn it over to Dave, who will highlight the company's performance in the third quarter. As we have done in our past calls, we'll be taking questions at the end of the Paulo's closing commentary. The press release and the presentation we'll go through today, including reconciliations to non-GAAP measures have been posted on our website and a replay of this webcast will be accessible on our website after the call.
Before we begin, I would like to remind you that our commentary today will include forward-looking statements with respect to sales, earnings and other matters. Our actual results will differ materially from our forecasted projections due to a wide range of risks and uncertainties that are described in our recent SEC filings.
With that, I will turn it over to Paulo.

**Paulo Sternadt** (Executives):
Thanks, Yan, and thanks, everyone, for joining us. Starting on Page 3, our very strong third quarter shows the power of demand meeting execution. We said the second half would show the benefit of our capacity investments. And in Q3, our teams delivered on that promise. We came in above the high end of our guidance on every key metric.
Organic growth was 19%. The segment margins were all-time record at 25.3%. Our adjusted EPS was $3.68, an all-time record and $0.17 above the midpoint of our guidance. Revenue reached a record of $8.9 billion, up 28%. Our strategy is working, and Electrical Americas is a strong proof point. Organic growth accelerated to 22% and margins reached 29.8%, up 230 basis points from Q2.
Our new capacity is now turning into output and into margin. Growth in Electrical Global was even stronger with 27% organic growth and strength across all end markets. And across the business, demand is both accelerating and broadening. Our Electrical and Aerospace combined book-to-bill remained strong at 1.2 with Americas strong at 1.3 and Aerospace at 1.2. While demand is broad-based across end markets, you can see here that the data center orders for the 12 months rolling are over 100% and revenues up 65% remained really strong.
Overall, accelerating orders and growing backlogs are a clear proof point that our customers are choosing Eaton because we bring end-to-end critical power solutions. Our performance in the year give us confidence to raise our guidance for the third time this year. We are raising organic growth by 200 basis points to a midpoint of 14% and our adjusted EPS midpoint by $0.25 to $13.75.
Dave and I will walk you through Q3 and the rest of the year outlook. But first, let's turn to Slide 4. We continue to drive Eaton forward with our bold strategy to lead, invest and execute for growth. The strategy is working, and we are transforming our company at fast pace. All 3 pillars are designed to accelerate our growth and create sustained value for our shareholders.
Today, we will talk about how our strategy is fueling growth in the Americas and Global and we'll conclude with a short update on Boyd. Now starting with Electrical Americas, this Page 5 shows what we are seeing right now. Demand is strong and broad-based, well beyond data centers and every leading indicator is pointing up. First, customer investment keeps building. Mega project announcements are up 85% so far this year. These are large multiyear infrastructure and electrification projects, and they will turn into demand for our products and solutions.
Second, our negotiations pipeline is up about 55% year-to-date. That's our earliest signal of future orders, and it's broad across every end market we serve. Third, backlog is up 33% to another record and is still growing even as we grow top line at 22% rate. Demand continues to run ahead of what we can convert. Finally, orders up 39% on a 12-month basis with book-to-bill of 1.3.
Orders can be lumping quarter-to-quarter, as you know, but the pipeline and the backlog keep building. Taken together, this is a business that continues to benefit from powerful secular trends, utility investment, grid modernization, industrial reshoring, AI-driven data center expansion and broader electrification. We remain focused on execution and bringing new capacity online.
Our strong pipeline orders and backlog give us the confidence in the durability of growth in Electrical Americas, and that's a great growth story for Eaton.
Turning now to Slide 6. Electrical Global continues to outperform expectations. We now expect organic growth about 16% in 2026 well above our prior guidance and more than double the 7% we delivered in 2025. This acceleration is no accident. It reflects the deliberate strategic moves we made over the past few years. We took the lessons we learned and applied the pillars of our lead, invest and execute for growth strategy to our global business, and we are growing with better margins. There are the 4 moves behind this performance.
First, we restructured early. We realigned Europe well ahead of the demand acceleration, building a leaner organization that's closer to our customers, and centered on solving their biggest challenges. Those efforts are now paying off. Second, we scale globally, our brand, our trusted technology and our relationships with global customers travel with us.
Our differentiated solutions let us compete in complex applications where reliability, safety and performance are critical. And we are following our global customers whatever they build. Third, we shifted our portfolio to high-growth areas. We are in the right markets at the right time, data centers, but also utility and machine OEM. So we expanded in modular power with NordicEPOD and our agreement to acquire COL Group will add even more scalable technologies, capabilities and capacity in Europe.
Finally, we are winning share through strong execution. Growth is broad-based with revenue and orders rising together, and we are outgrowing our markets in GEIS, EMEA and APAC. We are seeing the strongest competitive growth in APAC, and that give us real confidence in what's ahead. And there is more to come. Starting March '27, Boyd Thermal becomes part of organic growth, adding one of the fastest-growing business in the data center market to organic base.
Taken together, these strengths give us confidence not only in 2026 but in our long-term ambitions. Our current target for Electrical Global growth is 5%, 5-year CAGR from 2026 to 2030 with Boyd Thermal organic and the strength we continue to see across Global, we expect to update that target in 2027.
Turning to Page 7. Boyd Thermal is an important accelerator for Electrical Global. Since our last update, Boyd has continued to significantly outperform our expectations, reinforcing the strategic rationale for the acquisition and validating the strength of Eaton's position in the data center infrastructure market. The business delivered nearly triple-digit year-over-year growth with demand remaining exceptionally strong across the portfolio.
Growth has been supported by accelerating customer investments in AI and next-generation data center infrastructure. And orders continue to accelerate at similar rates as well, highlighting strong customer adoption of liquid cooling, architectures and Boyd's differentiated capabilities in thermal management. Demand strength is also reflected in the backlog, which saw 3x growth year-over-year providing strong visibility into future growth and reinforcing confidence in the long-term outlook.
Beyond the near-term financial performance, we are increasingly seeing the strategic benefits of combining Boyd with Eaton. Boyd's industry-leading thermal management capabilities, combined with Eaton's global scale, balance sheet strength, channel reach and supply chain capabilities are creating opportunities to accelerate growth beyond Boyd's stand-alone potential.
So this momentum is why we are raising Boyd's full year revenue outlook again. The third increase this year to $1.9 billion. Specifically, Eaton is helping expand Boyd's customer access through our global sales channels, accelerating commercialization of new solutions and enabling broader participation in large-scale data center projects. At the same time, our combined expertise in electrical power and thermal management position us to help customers to move towards more integrated power and cooling architectures and increased important requirement as AI workloads drive higher power densities.
Overall, Boyd strengthens Eaton's ability to deliver differentiated grid-to-chip solutions while increasing our exposure to some of the fastest-growing segments of the data center market.
Now I'll pass it on to Dave to walk through the financials.

**David Foster** (Executives):
Thanks, Paulo. I'll start by providing a brief summary of our strong Q3 results on Page 8. Total revenue grew by 28%, with a strong contribution of 8 points from acquisitions. Our acquisitions continue to deliver at or above our expectations for growth and margins.
Organic growth for the quarter was 19%, driven by strength in Electrical Americas and Electrical Global. Excluding mobility, our organic growth would have been 21%. Adjusted EPS of $3.68 was an all-time record, up 20% over prior year and $0.12 above the high end of our guidance. We generated a strong $0.32 segment profit beat versus our guidance with incremental margins of 26%, stepping up from 19% last quarter.
Now let's move to the segment details. On Slide 9, we highlight our Electrical Americas segment. Organic sales growth accelerated to 22% driven by strength in data centers up 54% along with strong growth in machine OEM and commercial and institutional. Our sequential margin improvement continues. Margins reached 29.8%, up 230 basis points from Q2 and more than 400 basis points since Q1. A clear sign our Execute for Growth strategy is working. From a year-over-year perspective, the majority of the margin decline was driven by temporary commodity cost headwinds.
The pricing actions we took in Q2 and early Q3 are working as price/cost was positive on a dollar basis in Q3. Demand keeps building. We had record orders of over $5 billion. Our negotiations pipeline was up 55% year-to-date and rolling 12-month orders were up 39% with book-to-bill held at 1.3. Electrical Americas is exiting 2026 with real momentum, and we are well positioned for a strong 2027.
Now I will summarize the strong results for our Electrical Global segment on Slide 10. Total growth of 58%, included organic growth of 27% from strength in data center, utility and machine OEM, along with 31% attributed to the Boyd acquisition. Organic revenue growth was broad in all regions with particular acceleration in APAC up nearly 50%. Boyd continues to outperform. Sales grew 24% from Q2, with triple-digit growth year-over-year. Backlog nearly tripled year-over-year giving us strong visibility into the liquid cooling demand ahead.
Operating margin of 21.1% was up 200 basis points over prior year, driven largely by higher sales. Each region posted strong year-over-year margin improvement. Demand in Global is accelerating fast. We had record orders in the quarter as rolling 12-month orders were up 51% with momentum across our end markets and exceptional strength in data centers. Electrical Global is built for this moment and with orders and backlog at these levels, we see a long runway of above-market growth ahead. Before moving on to our industrial businesses, I'd like to briefly recap the combined electrical segment's performance.
For Q3, we posted organic growth of 24% and total growth of 34%, a great third quarter. Segment margins were 26.4%, 190 basis points higher than Q2. On a rolling 12-month basis, orders accelerated up 43%, and our book-to-bill ratio for our electrical sector was 1.2. Our total electrical backlog reached another record of more than $20 billion, up 46% from last year.
Page 11 highlights our Aerospace segment's performance for the quarter. Organic sales growth of 6% resulted in Q3 record sales and segment profit with particular strength in commercial OEM. Ultra PCS added 5 points of growth this quarter with margins well above the segment average, it continues to be accretive to Aerospace. Total aerospace margins were 24.9% up more than 200 basis points from Q2. Year-over-year, margins were down 100 basis points, driven by mix.
Demand in aerospace has never been stronger with record orders driving backlog expansion and book-to-bill remaining a strong 1.2. We are well positioned to convert that backlog into growth in earnings.
Moving to our mobility segment on Page 12. Mobility had a strong quarter. Sales grew 10% with 9% organic growth and 1 point from currency, a clear return to growth. Meanwhile, margins increased 370 basis points to 17.2%, the highest level since 2018, driving incremental margins of more than 50%.
Now I will turn it back to Paulo to discuss our updated guidance and close out the presentation.

**Paulo Sternadt** (Executives):
Thanks, Dave. Moving to Page 13, we summarize our updated 2026 organic growth and margin guidance. Following another strong quarter, we now expect total company organic growth to be between 13% and 15%, up 200 basis points at the midpoint from the prior 11% to 13% range. This increase is driven by strength in Electrical Americas, up 400 basis points to a midpoint of 19%, and Electrical Global, up 400 basis points to a midpoint of 16%. We are maintaining our total segment guidance range of 24.1% to 24.5%.
On the next page, we have the balance of our guidance for '26 and Q4. For 2026, we are raising our adjusted EPS guide. Now we expect full year EPS to be between $13.70 and $13.80, $13.75 at the midpoint, up 14% from 2025. We also reaffirming our cash flow expectations for the year. Additionally, we have provided guidance for Q4 on this page. As a reminder, we also provide supplemental guidance, which includes raising Boyd's full year revenue to $1.9 billion, of which $1.6 billion will be Eaton's books for the year.
Continued strength across end markets combined with our record backlog provides strong visibility into our outlook for the year. This is the third time we've raised organic growth and adjusted EPS guidance this year. With the industry best positioned portfolio, and demand still building, we are not just finishing 2026 strong, we are carrying real momentum into 2027 and beyond.
So now shifting our perspective ahead to 2027 on Page 15, we provide our view of our end market growth assumptions for the next year. I won't go line by line, but the key takeaway here is simple. None of our end markets are expected to decline in 2027. Approximately 90% of our portfolio is in markets we expect to grow and the rest being residential and light vehicles should hold flat. Data centers and distributed IT along with commercial aerospace remain our strongest markets, both expected to grow strong double digits.
Together, that's roughly a 1/3 of our sales. All in, that adds up to about 11% growth across our end markets in total with some outgrowth on top of that, 2027 growth would be well ahead of our 2026 to 2030 organic growth target of 6% to 9% CAGR. Let me be clear, that's double-digit market growth again in 2027. We have the right portfolio in the right markets at the right time, and we expect 2027 to be another year of differentiated growth and strong returns for our shareholders.
Now let me wrap on Page 16. This quarter showed what Eaton can do when robust demand meets strong execution, and we are just getting started. First, demand is accelerating and broadening. Electrical orders are up 43% and backlog is up 46%. Let's not forget, this isn't just data centers. We are seeing strength across commercial and institutional, utilities, industrial facilities, machine OEM and residential. We are winning at a pace we've never seen before.
Second, execution is compounding. Electrical Americas margins reached 29.8%, up 230 basis points sequentially in a single quarter. And 18 of our 25 expansion projects are complete, with the steepest part of the ramp behind us. The results are clear, new capacity is turning into output and output into earnings. Third, our lead invest and execute strategy is working and is gathering pace. We are transforming our portfolio and evolving our culture. We are positioning the company to capture strong demand to accelerate growth and to beat our own short and long-term commitments, so we can deliver meaningful value creation for our shareholders.
And finally, when you put it all together, strong demand, improving execution, higher shipments and growing earnings, it gives us real confidence in both our near-term outlook and our long-term commitments. You can see that in the organic growth and EPS guidance we are raising today for the third time this year, and we are remaining focused staying close to customers, innovating with speed, leading and investing in growth and executing with discipline. So the best years are still ahead of us.
With that, let's open up for your questions.

**Yan Jin** (Executives):
Thanks, Paulo. Moving to the Q&A, we ask you to please limit your opportunity just one question per person. We appreciate your cooperation. So we can accommodate as many participants as possible today.
With that, I will turn it over to the operator for guidance.

**Operator** (Operator):
And our first question for today comes from the line of Nigel Coe from Wolfe.

**Nigel Coe** (Analysts):
So just one question. Maybe just -- Paulo, maybe talk about where we are in sort of the transition to next-generation 800 Volt DC solutions. I think the sidecar kind of rack-based solutions for the first half of next year. Just wondering, are you starting to see orders for kind of facility level DC power at this point? And where are we on the solid-state transformer commercialization and production?

**Paulo Sternadt** (Executives):
Thanks, Nigel. Thanks for the question. It's also top of mind for investors. We get that question all the time. So thanks for that. So we remain -- I would say this, I'll leave with the tagline. We remain a strong leading position for our solid-state transformers, both in U.S. and globally. Let me just give you an update of what happened in the last quarter. In the U.S., for example, in October, our 15 kV 2-megawatt unit, the medium-voltage solid-state transformer successfully passed all the UL tests. 
There's a new UL norm. And to our knowledge, we are the first multi-megawatt unit that successfully cleared all those steps, which is a great thing. And I would say this more importantly than being the first -- the system is truly unique. That's the most important part. It's unique in the market. It's the only system in the market, which is, at the same time, liquid cooled. It's multiport, meaning you have AC and DC port that gives maximum flexibility to customers. It is also outdoor ready. So this provides with customers the most flexible and compact brains, as you will, for the next generation of either complete DC architectures or to your question, to hybrid architectures with AC and DC playing together. And then also in parallel, our teams -- our global teams also advanced our technology here. 
So in the [ IEC ] markets, which are the European and the Asian markets, the Eaton Indoor unit also passed all the tests this time with the TUV, the [indiscernible], the German Institute, which is the global third-party testing certification organization. So we're really excited that we are pushing this leadership even further in this case. For me, the good thing for us to keep in mind is that this direction of travel in terms of migrating from AC to DC is real because of the large power savings that the customers see in this new technology, but the timing of that transition is not in under our control. 
So the industry is definitely moving to DC distribution as alternative to AC because of those savings. And I remind you that you asked about solid-state transformer, which is a key part of this new architecture, but it's only 1 of the 4 key building blocks that you need to have to win in this new era. And I would say Eaton is leading all other 3 as well, and I'll name them again, so you guys can remember. So the other one is DC breaker technology. 
The third one is power quality. So think about power electronics and UPS in distribution and advanced cooling with Boyd. So we are leading all 4 of them. And then the other thing I want you and investors to have in mind is that the current architectures, the AC architectures are not best, and we are fine either way. Eaton's positions that we sell powertrain in both architectures. We are architecture agnostic, and we will win either way, win in either path. So we want you to frame this as an opportunity more than a bet and a good option for us in the future. 
So specifically on the pilots we are running, we have 10 pilots running in parallel and multiple 15 kV projects that we're going to ship this year, and we expect this to turn into volume moving to next year. And here, the conclusion for us is very simple. We are a leader today in the current data center architectures. We will continue to be a leader in the future. We are ready for that future with the DC portfolio we are building.

**Operator** (Operator):
And our next question comes from the line of Nicole DeBlase from Deutsche Bank.

**Nicole DeBlase** (Analysts):
Clearly, data center markets remain robust. We all see that. But how are the balance of your electrical end markets performing in terms of growth?

**Paulo Sternadt** (Executives):
Yes. Thanks for the question. Let me make a comment on data centers first because we keep checking this market and it keeps surprising us on the upside. So data centers continue to represent an enormous opportunity for us. We track the projects that were announced, and now they amount to 366 gigawatts. In contrast to the last update we gave you in the earnings call was 307. So that keeps building. So that's good for us. Just think about contrast that with the installed capacity of 50 gigawatts is an enormous build-out. 
In my opinion, this will last for many years to come. But if you look beyond that, we are doing really well in that market in data centers. We grew 65% sales, and it's the ninth consecutive quarter we printed growth beyond 35%, which is amazing. And orders were up 101%. So we remain very excited about this business. I will just recall in our long-term plan, we baked 17% growth in our long-term plan. And here, year-to-date, we grew 60%. So it's an incredible opportunity for us.
But the beauty to the core of your question, Nicole, the beauty of our strategy and our portfolio is that we are anchored on secular trends that are even broader than data centers. So we have meaningful growth opportunities beyond data center. So just to give you some examples here, if you look at organic revenue, we had mid-teens for commercial, institutional, which remains a big segment for us. So mid-teens growth there, mid-30s growth, incredible growth for machine OEM in the quarter, double digits for industrial facilities, mid- to high single-digit growth for other markets like utilities, resi and distributed IT. 
So that's the look back. If you try to have a look forward on markets that are not data center, we better look at our orders here. So our Q3 orders were also very strong on a 12-month basis. Utility orders were up around 20%, resi, 25% and machine OEM 55%. So just to conclude here, I think it's pretty clear to everyone that demand is strong and is broadening much beyond data centers.

**David Foster** (Executives):
Yes. I would even add, Paulo, commercial and institutional were both up north of 25% in the quarter.

**Operator** (Operator):
And our next question comes from the line of Andrew Obin from Bank of America.

**Andrew Obin** (Analysts):
It's been a popular topic this quarter is modular capabilities. Can we just talk about what it is you guys have and what's your competitive differentiation in terms of modular on data centers?

**Paulo Sternadt** (Executives):
Great. Great question. Thanks for the question. I think the most important thing is that to highlight first that our business is doing really well in terms of execution. And there is a great pull from customers. That's why you're asking this question, because we take labor away from their job sites and we push this activity to our factories, which is much better and better controlled, but also increase the speed of deployment for this incredible backlog our customers have that I just mentioned. 
And last, but not least, when the models are put outside the data hall, it also free up space for the service where our customers generate revenue. So it's a great value proposition for our customers to start with. What differentiates Eaton from most other players is that we actually are experts in everything that goes inside those models, inside those boxes, right? Think about everything we design and manufacture because we do that not only for the models, but we design and manufacture the transformers, the switchgear, the circuit breakers and the UPSs that go inside those models. 
Then we can and we always do integrate them both in enclosed solutions, but also skidded solutions. And many of the companies that talk about modular today, they are integrators or assemblers. They don't make the breakers or the transformers that go inside, and that's a big difference. So when you have all those elements that go inside the model like Eaton, this vertical integration gives us the cost position, the lead time control and also supply certainty. If you think about hyperscale and colocation customers, that's what they're looking for. 
And for the customers, those customers, it means one vendor, one warranty, one commissioning team, fewer interfaces and fewer single points of failure. So that's the biggest differentiation between us and other players. And then just to give a proof point here, Fibrebond, we acquired them April last year, in their first year at $375 million in revenue. In the first year of us owning the business, they jumped already to $600 million, and margins are accretive to Electrical Americas. 
So it's a great business growing at fast pace with great margins. So we decided to double the capacity we had for Fibrebond in their existing sites. They had one site. And now we're going to double that again with the facility we announced in Arkansas, which comes online in 2029. So if you think about the business we already had before Boyd and the business we have with Boyd in modular business, only in the Americas, that business is going to reach $1 billion in revenue already in 2026. 
And just to conclude, let's not forget modular isn't new for us. We invested in NordicEPOD in EMEA in 2024. So we have a partner there. We have a joint venture. And we acquired Boyd. We acquired FibreBond in '25. And in Asia, we have multiple partners that we can also work with the modular solutions. And now as you think about the white space, we're going to start exploring as a company, we can take that expertise all the way down to the white space as well. So it's a great moment for us. Thanks for the question.

**Operator** (Operator):
And our next question comes from the line of Scott Davis from Melius Research.

**Scott Davis** (Analysts):
Paulo, I wanted to follow up a little bit on that and talk about M&A a bit because you've been busy. You just mentioned the Fibrebond deal and the partnership with NordicEPOD, the COL that was announced today did Boyd probably some stuff that not even remembering. But seems like you're going down a strategy of trying to fill in some product gaps that are perhaps more aggressively than if you look in the history of Eaton, I assume that is a strategy, so I'm asking that as part of the question. And are the remaining product gaps, I guess, is the better way to ask it? And if so, do you -- are you guys kind of done with the M&A stuff? Or are you going to be equivalently aggressive over the next 12 months or so.

**Paulo Sternadt** (Executives):
Well, thanks, Scott. We remain very consistent with what we shared with you in New York during our Investor Day. We would put our M&A dollars to work in Electrical and Aerospace, and that's exactly what we did. So our pipeline stays active, mostly on the electrical side this time. But let me set the expectations to be very clear. I think that's the core of your question. We've already put $14 billion to work in our acquisitions. And as you heard from Dave, we are happy that every acquisition we made is delivering better numbers than what we initially forecasted. 
We underwrote for the deals with great performance for all the acquisitions we made. And we always talk about the organic growth. But if you look at our total growth for the company, incredible 28%. So that's another mark we would like to highlight in Q3, very strong number and better margins, accretive margins for the company. 
So great moves so far. So for now, I would say this the big deals are behind us. We don't see any large acquisitions in the short term. That, I think, is the core of your question. And honestly, we are in this integration phase. We have a lot of organic and inorganic growth to deal with right now and executing on this growth is our top priority. We are executing on it. We'll continue to execute on it. On gaps, which was the second part of your question, we don't see any gaps in North America. Just look at our data center portfolio, it goes all the way from the grid to the chip. So we don't see any product gap here. 
Where we'd like to scale more if we find the right deal with the right bolt-on will be in Europe and perhaps in Asia as well. And the agreement we just made with COL to acquire this company based in Italy is a good example. It adds -- this bolt-on adds technologies, capabilities and capacity in Europe to accelerate the organic plans we had on the deck anyways. So you should expect more bolt-ons on the electrical side. We'll keep this flexibility if something comes along, but don't expect any Boyd size deal in the next 12 months. I think that's the key takeaway.

**Operator** (Operator):
And our next question comes from the line of Jeffrey Sprague from Vertical Research Partners.

**Jeffrey Sprague** (Analysts):
Maybe pick up on Boyd actually. It looks like your revenue forecast for Q4 is roughly flat sequentially, and you made the point about it's going to flip into organic and be a growth driver into next year. So just looking at that revenue trajectory, is this particular business capacity constrained at this point? Do you have new capacity coming on? And maybe give us an early thought on how 2027 may play out in that business?

**Paulo Sternadt** (Executives):
Yes. So it was breaking up. So I think you're inquiring about Boyd's growth, right, in Q4 next year. So the first thing I want to say that this team is always surprising us on the upside. Every quarter is the same. And the reason is that they are winning with a number of different platforms. And since they engage early in the design phase, the ramp process is pretty smooth. It's not easy. No business grows at the pace they are growing without problems, but they are always ahead of the other competitors. 
So we remain excited. So on Q4, I wouldn't be surprised if, again, they beat their own numbers, to be honest. And as we think about 2027, I think that's the core of your question, we see at least a $2.7 billion business for next year, which is roughly 50% growth over our previous 1.8% guide. So strong growth once again, they have the design wins, they have, the orders and the backlogs to sustain that. And we're really excited to keep winning on new platforms or things that are going to come live '28 and beyond. So strong performance, winning new business and ramping at speed. So we are confident here.

**Operator** (Operator):
And our next question comes from the line of Andrew Buscaglia from BNP Paribas.

**Andrew Buscaglia** (Analysts):
I wanted to touch on what caught my eye this quarter. Electrical Global accelerated 27%, so that's up. Last quarter, it was up about 18%. So I'm wondering what's beyond that step change? And then should we assume that this segment now kind of entered in an elevated growth base?

**Paulo Sternadt** (Executives):
Yes. No, thanks for the question. I'm glad you raised that point because this segment really surprised all of us on the upside this quarter. But all the actions behind that growth were deliberate. It was not an accident. So if you look at the growth rate of this business, we started Q1 at 9% and then Q2, 18% growth, and now Q3, 27%. So incredible progression here. And just to remind you, the last question I got from Jeff Sprague was on Boyd. Boyd is not included in those numbers. So Boyd actually adds 31 points of growth to a total of 58% growth and will become organic in March '27. 
So I think if you look at the legacy Electrical Global business we have, is accelerating specifically across the complete portfolio, and Boyd add significant organic growth on top of it. So really exciting platform. I'm going to go to the sustainability of that growth in a minute. If you cut this growth and you look at the growth regionally business by business, I will lead with the affirmation that every business inside Electrical Global did the work. APAC led was fantastic almost 50% organic growth. 
GEIS and EMEA both grew around 20%, which is clearly ahead of the market. If you think about this Asian performance, we are beating local players on growth. And in Europe and Asia, we are winning with the same hyperscale customers and multi-tenant customers we serve in North America, which is great news. They want us to be successful with them everywhere they build. We talked about that in the past. 
Now the reality is here to prove us right in that case. And then if you -- I made the cut by business. If you cut by end market and you look at the performance by end market, also a very strong performance. Our data center business grew almost 100%, in Global, so 97%, machine OEM, 29% and utilities 21%. So really broad-based here as well. So with that in mind that every business is doing well and every end market is doing well, we believe -- we truly believe this Electrical Global business has entered what we call a sustained growth phase and the order book sustains that with our orders are up 51% on a 12-month basis. 
So that gives us the confidence. And if you look at the backlog as a result of that, even with the strong organic growth, they more than doubled the backlog in a year-over-year basis. And even if they exclude the Boyd backlog, I always get that question, it's still 76% up. So everywhere you look, end market, business by business with or without Boyd, you see it come to the same conclusion. So those drivers, in our opinion, are structural. They are not cyclical. And again, it didn't happen by accident. We restructured Europe well ahead of this demand. 
We were early. We are adding capacity in Asia. We are focusing on winning share and not looking at PMIs. That's the way this team is wired. They really want to win, and we want to grow faster than the market. So let's not forget, once again, Boyd will add to that when it becomes part of the organic. And just to conclude, we are rigorously applying our strategy, the 3 pillars of our strategy here in the global business. And we are all proud of this team because we believe we turned this segment into another high-growth platform for Eaton. So we continue to deliver the strong growth moving forward, and we keep expanding margins for Electrical Global.

**David Foster** (Executives):
Yes. So I want to add to that. If you look at the GEIS business, you can talk about Execute for growth, the expanded margins almost 400 bps from H1 to H2, through price, cost out and productivity. So really executing the global playbook that Paulo just talked about.

**Paulo Sternadt** (Executives):
400 bps.

**David Foster** (Executives):
400 bps, yes, I'm sorry.

**Operator** (Operator):
And our next question comes from the line of Steve Tusa from Wells Fargo.

**Charles Stephen Tusa** (Analysts):
Just on the margin, I think your 4Q incremental in EA is like -- I know it's a bit of a range, but something in the 40% to 45% range. Can you just talk about how you kind of feel about that next year? There's probably an easy comp in the first half, a little bit tougher in the second half? And then somewhat related to that, on pricing strategy, are you guys pricing similar products within the data center channel the same way as you would be pricing them if it's the same product like in a more standard application like in a C&I application or something like that? Maybe just talk about how you manage that price across the channels as well.

**Paulo Sternadt** (Executives):
Great question. So on the ESA margin, I will lead with the bottom line message here that we are in line with the full year margin guidance range and 3 quarters under our belt give us the confidence to make that point. And as you know, we are still operating in a very high inflationary environment. So we are managing that very well, I would say, if you look at the performance quarter-by-quarter and first half versus second half. And on your point on incremental discussions for ESA, we will continue to improve our incrementals from Q3 to Q4. So we had high 20s in Q3. That's going to get high 30s to close to 40% incrementals moving to Q4. 
So that's going in the right direction again. And that for us, I would say, again, I'm proud of the team because taking that the way they did and the margin development from -- if you look at the margin development from the first half or the second half, the progression will be over 400 basis points, which is a great result in this environment specifically. 
And then specifically on the question about pricing, I would say this, we have pricing power, and we have also good contracts in place where we have correction for commodities, et cetera. And we see that we are leading with pricing announcements as well when required on price list, and we negotiate pretty well with our project by project as well. So we have, in this environment, the pricing power and also the good relationship with the customers to have those debates.

**David Foster** (Executives):
Yes. The only thing I would add to that is, in October, we finalized negotiations with 2 of our large customers. We have a handful to finalize in Q4. I kind of talked about this in the last earnings call that we'd have discrete price negotiations with larger customers. And then we just announced today that we would have general price increases in ESA, EMEA and GEIS effective January 2. So it's going to be a combination of those going forward, and that's how we're going to price in the market. And we are on the right trajectory. And just to make a short commentary on October, we just got the top line, it looks really strong. So it's a good start of the quarter as well.

**Operator** (Operator):
And our next question comes from Amit Mehrotra from UBS.

**Amit Mehrotra** (Analysts):
I guess I just wanted to follow up on that question. It was nice to see the EBITDA margins in the quarter and [ used for ] the fourth quarter, but it's got a big prepaid customer plan that's found online, I think the first half of next year. So is there any color initially you can provide on [indiscernible] '27? I assume it's going to be better than the full year '26, but just trying to think about the headwind from this [indiscernible] transformer plant.

**Paulo Sternadt** (Executives):
Okay. It was breaking up a lot, but I think you're inquiring about margin development into '27 and also the fact that we have a new summer plant coming online, correct?

**Amit Mehrotra** (Analysts):
Yes. Just the size of that 3 space transformer facility, I think is orders of magnitude larger than sort of the 18 that's been put up over the last 1.5 years. And I'm just trying to understand what amount of impact that could have on '27.

**Paulo Sternadt** (Executives):
Yes. So first of all, so we are really excited about the margin development for Electrical Americas, as I said before. I would just caution you not to take Q4 and multiply it by 4 because there's some seasonality with the business, especially in the distribution business, et cetera. So there's some seasonality there. But the direction of travel is very clear. We have a strong start. We have record backlogs. So we feel really good about it. On the specific question about the transformer facility, yes, it's larger than the other ones we did, but we also learned our lessons -- we hired early. 
We hired workers early. We are training them in our Wisconsin plants already. So when we start to ramp, we go with -- it's going to be a learning curve in the new facility, but they're already trained in a facility that runs those products today. So we are taking lessons here. I would also tell you that we are dealing with 6 expansions now versus 18. So it's a much easier setup, and we have a much stronger team dealing with this expansion. So we learned our lessons. It's less disruptive than it was for the full year last year and the first half of this year. And I think we have a good team around it. So we feel confident as we meet with them every week to check progress.

**Operator** (Operator):
And our next question comes from the line of Andy Kaplowitz from Citi.

**Andrew Kaplowitz** (Analysts):
Can you give us some more color into the health of the aero markets and in particular, your aero supply chain at this point? It would seem since you didn't change your aero organic revenue guidance for the year that you think you have your arms around any supply chain issues and that revenue growth could even improve a bit in Q4. But maybe you could give us a little more color on the markets and what you're seeing and doing to mitigate supply chain risk.

**Paulo Sternadt** (Executives):
Yes. Thank you. So I believe it's clear that demand for aerospace is strong. You just look at our orders, were up 20% and specifically defense OEMs up 36%. So there's a lot of growth, and we keep growing our backlog as well now to a record of $5.6 billion, which is 33% higher year-over-year. So the demand signals are clear and very strong. In terms of execution, we faced some specific supplier issues in some commodities. There are [ punctual ] problems. We are working on them, and we are solving them with different strategies, helping those suppliers to ramp is one of them, creating second source in partnership with our customers is the second type of measure we are taking. 
The third one, in some cases, we are in-sourcing where we see some suppliers struggling, we have the machining capability and capacity, we are in-sourcing that. So we are taking that holistic approach in partnering with our customers to approve that, because in aerospace, you can't shift a supplier without authorization from your customers. 
So we are working in collaboration with them. So that's what I would say here. The demand is pretty clear. It's strong. We are winning. We have those platforms for today and tomorrow. And we are dealing with those [ punctual ] problems in supply chain that are cut across the whole industry. And we are both collaborative with customers, but also with the supplier base, and we continue to develop in that direction. So we still think our Q4 is going to be a bit better in terms of top line and growth. We're just cautious that this situation of the supply chain is fully behind us, then we can start liquidating more of the backlog. We keep winning. It's just a matter of conversion of that backlog.

**Operator** (Operator):
And our next question comes from the line of David Raso from Evercore ISI.

**David Raso** (Analysts):
Just trying to get a little more granular on the numbers for '27 versus '26. Can you characterize for us how price cost will play out this year? And just what's the base case of how you're thinking about how you're setting pricing now for '27? And also the level of inefficiencies, you alluded already to obviously a little bit easier to ramp up 6 factories than 18. Maybe just some sense of -- I don't know, Dave, how you might quantify it some way, the inefficiencies in '26, and I would assume less in '27. And also just any sense of capacity available to you in '27 versus '26 given the ramp you've done on the 18 factories?

**Paulo Sternadt** (Executives):
So I'll go first and then Dave can add color. So we're still planning, Dave. We're not ready to share the 2027 guidance yet, but I can give you a good framework for your model as you start thinking about our business in 2027. So you saw from the end market perspective, for example, that we see our end markets growing at least 11% next year. You know that we usually plan to outperform the market. So think about a growth path, which is higher than 11% here. 
We also expect to improve incremental margins from 2026. We are looking at '26 around 23%. So we're certainly going to do something higher here. But again, it's premature for us to guide. We're going to do that in February when the complete planning process is done. If you think about adjusted EPS for a moment, when we gave you the targets for the 5-year plan last year, we said we will go every year beyond 12% organic EPS growth. This year, with the guidance we just shared with you for '26, we are aiming at 14% growth of EPS. 
And if you look at the second half of this year, it's a 20% growth. So we are in the right path here as a company. And that embeds much of the questioning you're asking about inefficiencies, capacity turning into earnings, et cetera. Most of it is already here, right? So again, the 2 portfolio items I want everyone to remind in 2027 that shouldn't be confused with underlying performance, and they are material for 2027 are the following. 
First of all, Boyd, we are planning -- I just said I got that question around Boyd. We are planning on $2.7 billion for that business, which is 50% growth again next year. And that growth, again, becomes organic after mid-March. So think about 3/4 of this year being organic for us. That would double charge the growth for Electrical Global, the organic growth rate. And on the other direction, though, mobility will contribute around $800 million in revenue only, reflecting a close with the Dana transaction around Q1. So those are things I want you and investors to keep in mind as you start modeling and comparing our 2026 to 2027 framework.

**David Foster** (Executives):
Yes. I think, Paulo, you covered really the -- where we are in the process right now. The segments are reviewing it with their leaders this week. I've seen some preliminary looks and I'm feeling good about 2027. Paulo and I will review it here in the third week of November. And -- but that's where we stand right now. Too early to share any real concrete numbers.

**Operator** (Operator):
And our next question comes from the line of Chad Dillard from Bernstein.

**Charles Albert Dillard** (Analysts):
So my question is on just how you're winning in Europe on the data center build-out. Can you just talk about sort of what you're doing from a shares perspective? And then maybe if you can share how you're thinking about win rates in Electrical Global maybe versus what you've been seeing in Electrical Americas?

**Paulo Sternadt** (Executives):
So I'm not sure it was really fitted, but the question is on EMEA data center. Is that...

**Charles Albert Dillard** (Analysts):
Yes, exactly. Just on just your win rate and how you're gaining share in that market?

**Paulo Sternadt** (Executives):
Yes. So you could see that with those growth rates, we are clearly gaining share in Europe and in Asia, et cetera. The fact -- the actions behind these numbers are that we were traditionally for data centers in Europe, specifically to your question, we were and we remain leaders in UPS business in Europe. And what we are doing today, step by step, we are building the same fortress, the same leadership in our portfolio as we have in the Americas. 
So building the power distribution portfolio that we're going to speed up now with the acquisition of COL when that comes to fruition. So we are building that power distribution portfolio. We also, over time, increased our transformer capacity in Turkey in our plants. So think about it, we looked at our strong leadership position in Electrical Americas, and we are taking every action we need to take in Europe to build the same strong portfolio over there. 
This is something that our customers are requesting us to do, because we work with them in the U.S. And as they go overseas and then build over there, they would like to count on our support as well. So we are building that over time. There are still things for us to go do. So we are far away from being done in that area. And despite all those fantastic growth numbers, no one is taking a victory lap in that team. They remain focused. They know what they need to do. So all hands on deck, we're going to keep building that portfolio.

**Operator** (Operator):
This does conclude the question-and-answer session of today's program. I'd like to hand the program back to Paulo Ruiz for any further remarks.

**Paulo Sternadt** (Executives):
Thank you. So I mean, this is a very, very good call, very good questions. Let me add some closing remarks. First, I'd like to thank you, all the analysts and investors are on the call for your interest in Eaton, your analysis, your deep questions today. I also wanted to thank the Eaton team. I'm pushing you hard, guys. I know you're listening to this call, but you keep delivering quarter after quarter. I'm proud of the progress. And we are committed to keep improving, which has been the most important thing. No one is taking victory laps here. We remain focused and I love the culture we are building here. And I will leave with this to investors. It's clear that our strategy is working. Our lead, invest and execute growth strategy is working, is gathering pace. 
And you can see the results already, right? Record sales growth, earnings above the high end of our guidance. So we are really happy with the progression we have here. The demand keeps accelerating and is broadening beyond data centers. We talked about that. So I think it's important we highlight this. It's cutting across different end markets, which is good to see. And data centers, despite all the discussions on the market today, they have a long runway. 
They have a very long runway beyond '28 and '29 and many projects. And with this large backlog is going to come in terms of multiple years of work for us. So this is a great platform. And the new Eaton, as we put this all together, this new Eaton is taking shape. Our portfolio moves have structurally transformed the company. And then if you add the future of this technology in terms of 800 volts, et cetera, we are ready for that transformation. 
So we feel really good about it. We are also very proud. I think I want to highlight that the Electrical Global is the new growth engine for the company. We restructured early. We're scaling globally. So we turned this business into a next growth platform, and we all feel really proud of it. And as you look at it, we are really focused on execution as well. Electrical Americas see the capacity coming online turning into output and into margins and earnings. So that's great to see as well. And I'm also -- I think this was all a lot of work from the team. We're also satisfied with the third beat and raise this year. This is what we want to do constantly now, give us confidence in '27 in our 2030 commitment. So I will conclude to say thank you once again, and we believe the best years ahead of us. Have a great day.

**Operator** (Operator):
Thank you ladies and gentlemen for your participation in today's conference. This does conclude the program. You may now disconnect. Good day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ETN_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜Paulo Sternadt｜guidance：全年有機成長指引上調至 11%–13%（中點 +200bp）（原話："total organic growth to be between 11% and 13%"）
- 2026-07-31｜Paulo Sternadt｜guidance：全年調整後 EPS 指引 13.40–13.60 美元，中點 13.50（原話："we expect full year EPS to be between $13.40 and $13.60"）
- 2026-07-31｜Paulo Sternadt｜guidance：Electrical Americas 有機成長中點上調 200bp 至 15%（原話："up 200 basis points to a midpoint of 15% growth"）
- 2026-07-31｜Paulo Sternadt｜guidance：Electrical Global 有機成長中點上調 450bp 至 12%（原話："basis points to a midpoint of 12% growth."）
- 2026-07-31｜Paulo Sternadt｜guidance：各部門利潤率指引區間維持不變（原話："confidence to reaffirm our segment margin guidance ranges"）
- 2026-07-31｜Paulo Sternadt｜guidance：全年現金流預期維持不變（原話："We are reaffirming our cash flow expectations for the year."）
- 2026-07-31｜Paulo Sternadt｜guidance：Boyd 全年營收上調至 18 億美元，其中 15 億計入 Eaton（原話："Boyd's full year revenues to $1.8 billion of which $1.5 billion"）
- 2026-07-31｜Paulo Sternadt｜guidance：全年有機成長指引逐次上調的軌跡（年初 8%）（原話："We started the year saying we'll grow 8%."）
- 2026-07-31｜Paulo Sternadt｜guidance：CEO 對下半年指引的描述：仍屬審慎（原話："We are very prudent here"）
- 2026-07-31｜Paulo Sternadt｜guidance：管理層估計今年整體可服務市場成長約 10%（原話："our total addressable market will grow about 10% this year"）
- 2026-07-31｜David Foster｜margin：Electrical Americas Q2 利潤率 27.5%，較 Q1 高 190bp（原話："margins of 27.5%, 190 basis points higher than Q1"）
- 2026-07-31｜David Foster｜margin：Americas 年減的利潤率降幅主要來自暫時性負價格/成本（原話："margin decline was driven by temporary negative price/cost."）
- 2026-07-31｜David Foster｜margin：下半年價格/成本影響預期回到大致中性（原話："this will return to a roughly neutral impact"）
- 2026-07-31｜David Foster｜margin：Q1→Q2 Americas 190bp 拆解：約 100bp 價格/成本、90bp 產出（原話："About 100 points of that was price/cost and the other 90 points was pure output"）
- 2026-07-31｜David Foster｜margin：Americas 下半年對上半年利潤率改善 450–500bp，其中 300bp 來自價格/成本、150–200bp 來自產出與生產力（原話："We'll be up 450 to 500 basis points."）
- 2026-07-31｜David Foster｜margin：漲價措施已在 Q2 或 8 月初全部落地（原話："our pricing actions have either been implemented in Q2 or early August."）
- 2026-07-31｜David Foster｜margin：Q2→Q3 Americas 改善 250bp（150bp 價格/成本、100bp 產出生產力）（原話："Q2 to Q3, which is a 250 basis point improvement"）
- 2026-07-31｜David Foster｜margin：Q3→Q4 Americas 改善 200–250bp（150bp 價格/成本、50–100bp 產出生產力）（原話："it's a 200 to 250 basis point improvement"）
- 2026-07-31｜David Foster｜margin：CFO 稱 7 月初步數據較 Q2 續有改善（原話："I have early reads on July as of this morning."）
- 2026-07-31｜David Foster｜margin：Q3 與 Q4 利潤率改善部分來自非加班、較少溢價成本（原話："we're going to be doing it on regular time versus overtime"）
- 2026-07-31｜David Foster｜margin：Electrical Global Q2 利潤率 19.8%，年減 30bp（原話："Operating margin of 19.8% was down 30 basis points"）
- 2026-07-31｜David Foster｜margin：Electrical Global 一般性漲價由 Q4 提前至 Q3（原話："pulled in our planned general price increase from Q4 to Q3"）
- 2026-07-31｜David Foster｜margin：Aerospace 利潤率擴張 60bp 至 22.8%（原話："Total Aerospace operating margin expanded by 60 basis points to 22.8%"）
- 2026-07-31｜David Foster｜margin：EPS 口徑：分部利潤優於指引 0.25 美元，被較高稅率 0.15 美元部分抵銷（原話："offset by $0.15 from a higher tax rate."）
- 2026-07-31｜Paulo Sternadt｜margin：IEEPA 退款對 Q2 影響低於 300 萬美元（不到 0.01 美元 EPS）（原話："IEEPA refunds is less than $3 million"）
- 2026-07-31｜Paulo Sternadt｜margin：回應分析師澄清：IEEPA 退款精確數字為 280 萬美元（原話："$2.8 million, if you want to be precise."）
- 2026-07-31｜Paulo Sternadt｜margin：下半年關稅退款影響不重大且已含在指引內（原話："the impact of the tariffs for the second half is immaterial"）
- 2026-07-31｜David Foster｜commitment：CFO 重申 2030 年 32% 利潤率承諾（原話："we're still committed to our 32% margin by 2030."）
- 2026-07-31｜Paulo Sternadt｜commitment：CEO 表示對 2026 與 2030 承諾有信心（原話："delivering on our 2026 and 2030 commitments."）
- 2026-07-31｜Paulo Sternadt｜commitment：Americas 下半年利潤率將進一步改善（原話："will improve further in the second half of the year"）
- 2026-07-31｜Paulo Sternadt｜commitment：Boyd 達成全年 18 億預測的信心表述（原話："I will be shocked if they cannot overdeliver on"）
- 2026-07-31｜Paulo Sternadt｜commitment：Boyd 預計 2027 年併入有機成長計算（原話："looking forward to Boyd to join the organic growth in 2027."）
- 2026-07-31｜Paulo Sternadt｜commitment：CEO 稱將改善部分產品線的交期並擴充工程支援（原話："we know the product lines where our lead times are extended"）
- 2026-07-31｜Paulo Sternadt｜commitment：CEO 表示無人在慶功，團隊聚焦於達成承諾（原話："no one is taking a victory lap here"）
- 2026-07-31｜David Foster｜customer：Electrical Americas 資料中心有機成長約 65%（原話："data centers, up about 65%"）
- 2026-07-31｜David Foster｜customer：Americas 滾動 12 個月訂單成長 41%（創紀錄）（原話："record orders up 41% on a rolling 12-month basis"）
- 2026-07-31｜Paulo Sternadt｜customer：全公司訂單出貨比 1.2（原話："total company book-to-bill remains strong at 1.2"）
- 2026-07-31｜David Foster｜customer：電氣業務整體積壓訂單年增 43%（原話："total electrical business increased 43% over prior year."）
- 2026-07-31｜Paulo Sternadt｜customer：美國資料中心積壓達 307GW（15 年，前次為 12 年）（原話："Total U.S. data center backlog has grown to 307 gigawatts"）
- 2026-07-31｜Paulo Sternadt｜customer：該積壓僅約 20% 於近期轉化，多數為 2028 年後交付（原話："Only roughly 20% of this backlog converts near term."）
- 2026-07-31｜Paulo Sternadt｜customer：Electrical Global 資料中心營收成長 65%，高於底層市場 23%（原話："faster than the underlying market that is growing at 23%"）
- 2026-07-31｜Paulo Sternadt｜customer：Electrical Global 有機積壓訂單成長 54%（扣除 Boyd）（原話："organic backlog is up 54%"）
- 2026-07-31｜Paulo Sternadt｜customer：Electrical Global 指引由 7.5% 上調至 12% 的說明（原話："to raise our guidance from 7.5% to 12%"）
- 2026-07-31｜Paulo Sternadt｜customer：管理層稱每檔資料中心內容價值 340 萬美元/MW 為建模適用數字（原話："The $3.4 million is the right number to think about"）
- 2026-07-31｜Paulo Sternadt｜customer：資料中心連續 8 季成長超過 35%（原話："8 consecutive quarters of growth beyond 35% in data centers"）
- 2026-07-31｜Paulo Sternadt｜customer：2030 承諾模型僅假設資料中心成長 17%（原話："17% of the data center growth in our model."）
- 2026-07-31｜Paulo Sternadt｜competition：Boyd 在液冷（冷板與 CDU）為市場領導者（原話："they are the market leaders for liquid cooling"）
- 2026-07-31｜Paulo Sternadt｜competition：Boyd 為廣泛晶片供應商的設計夥伴（原話："design partner for broad-based chip providers."）
- 2026-07-31｜Paulo Sternadt｜competition：CEO 指部分競爭者出現品質問題（原話："some are actually showing some quality issues from the get-go"）
- 2026-07-31｜Paulo Sternadt｜competition：CEO 稱 Eaton 在固態變壓器技術上領先（原話："we are clearly ahead in terms of technology"）
- 2026-07-31｜Paulo Sternadt｜competition：CEO 認為 800V DC 轉型必然發生（原話："I believe this is going to happen"）
- 2026-07-31｜Paulo Sternadt｜competition：預製模組化解決方案的趨勢（缺工）（原話："So there is a push towards more modular solutions."）
- 2026-07-31｜Paulo Sternadt｜product：Boyd 帶來從電網到晶片的完整產品組合（原話："we have the full portfolio"）
- 2026-07-31｜Paulo Sternadt｜product：Boyd Q2 營收 4.32 億美元，高於其承諾與 Q2 指引 20%（原話："delivered $432 million in revenue"）
- 2026-07-31｜David Foster｜product：Ultra PCS 收購符合預期（原話："acquisition is performing to our expectations."）
- 2026-07-31｜David Foster｜product：Aerospace 需求強勁預期延續（原話："Aerospace continues to see strong demand now and into the"）
- 2026-07-31｜Paulo Sternadt｜capital_allocation：投資超過 10 億美元擴充產能（原話："investing more than $1 billion in capacity expansion"）
- 2026-07-31｜David Foster｜capital_allocation：CFO 稱各項收購均達到或超越成長與利潤率預期（原話："Each acquisition is at or above"）
- 2026-07-31｜Paulo Sternadt｜capital_allocation：以 Reverse Morris Trust 剝離移動出行（汽車）業務（原話："the tough call once again on the Reverse Morris Trust"）
- 2026-07-31｜Paulo Sternadt｜risk：產能爬坡的主要陣痛已在 Q4 與 Q1 發生（原話："most of the pain now is behind us, happened in Q4 and Q1"）
- 2026-07-31｜Paulo Sternadt｜risk：Q1→Q2 為模型中最大的單季產出爬坡，管理層稱已完成（原話："the largest quarterly ramp in production output"）
- 2026-07-31｜Paulo Sternadt｜risk：Americas 每日營收自 2025 年初累計成長約 25%（原話："roughly 25% growth in revenue per day"）
- 2026-07-31｜David Foster｜risk：Mobility 有機成長 -2%，管理層提及刻意退出低利潤業務（原話："Excluding the impact of the intentional exit"）

### 問答異常語氣（迴避／改口／保留）
- ETN_Q2_2026_Earnings_Call_20260731.md｜問：Andrew Obin（BofA）：Boyd 第三季與第四季的營收節奏（cadence）為何？｜答法：CEO 談 Boyd 的競爭優勢、Q2 超標與整合進度，未給 Q3／Q4 分季數字或節奏
- ETN_Q2_2026_Earnings_Call_20260731.md｜問：Jeffrey Sprague（Vertical）：指引隱含 Electrical Americas 營收 Q2→Q4 大致持平，但利潤率要靠價格與產出，是否過於保守？｜答法：CFO 回答以加班轉正常時間、溢價成本下降、生產力與價格為主，未直接回應營收持平的假設或是否保守
- ETN_Q2_2026_Earnings_Call_20260731.md｜問：Nicole DeBlase（Deutsche）：Electrical Global 隱含下半年有機成長減速，是否有需求提前或指引保守？｜答法：CEO 回以「很審慎」並列舉指引逐次上調的軌跡與「沒有下行」，未回答是否有拉貨提前，也未給下半年 EG 分季數字
- ETN_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Hammond（KeyBanc）：交期改善後，何時能取得更多公平市占？目前長交期品項的交期狀況？｜答法：CEO 強調資料中心成長 65%、連續 8 季成長，並稱知道哪些產品線交期偏長，未提供交期天數或取回市占的時間點

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
{"date":"20260905","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤$355（FY26E 13.55×26x 或 FY27E 16.07×22x），或 FY27 共識 EPS 上修 ≥10%（≥$17.7）且股價未同步上漲 → 重跑 DD、衛星首倉 1/3","irr_base_pct":8.9,"ev5y_pct":43.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.97,"ev5y_pct":43.0,"irr_base_pct":8.9,"max_dd_pct":-45,"bull_5y_price":887.6,"bear_5y_price":277.2,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤$355（FY26E 13.55×26x 或 FY27E 16.07×22x），或 FY27 共識 EPS 上修 ≥10%（≥$17.7）且股價未同步上漲 → 重跑 DD、衛星首倉 1/3","price_at_dd":410.85,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ETN_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
