你是 stock-analyst **v20 判斷 agent**，標的 HLT（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"HLT","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HLT_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HLT_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenues_gaap","label":"Total revenues (GAAP)","value":3325,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}},{"id":"f_kpi1_operating_income_gaap","label":"Operating income (GAAP)","value":909,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}},{"id":"f_kpi2_adjusted_ebitda_hilton_n","label":"Adjusted EBITDA (Hilton 無 non-GAAP 營業利益揭露，以此替代)","value":1058,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}},{"id":"f_kpi3_diluted_eps_adjusted_for","label":"Diluted EPS adjusted for special items","value":2.45,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}},{"id":"f_kpi4_system_wide_comparable_r","label":"System-wide comparable RevPAR growth (currency neutral)","value":5.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}},{"id":"f_kpi5_net_unit_growth_yoy","label":"Net unit growth YoY","value":6.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}},{"id":"f_kpi7_capex_contract_acquisiti","label":"Capex + contract acquisition costs","value":133,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}},{"id":"f_kpi8_guidance_q4_2026_adj_ebi","label":"Guidance: Q4 2026 Adj. EBITDA / adj. EPS / RevPAR","value":"Adj. EBITDA $1,047–1,067M；adj. EPS $2.32–2.38；RevPAR +3.0–3.5%","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"guidance","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}},{"id":"f_kpi9_guidance_fy2026","label":"Guidance: FY2026","value":"Adj. EBITDA $4,060–4,080M；adj. EPS $9.07–9.13；RevPAR +4.0–4.5%；NUG 6.0–7.0%；資本返還約 $3.5B","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"guidance","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_hlt_gross_margin_pct","label":"HLT 毛利率","value":30.13,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_operating_margin_pct","label":"HLT 營業利益率","value":24.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_fcf_margin_pct","label":"HLT FCF 利潤率","value":14.49,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_gross_margin_pct","label":"MAR 毛利率","value":19.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_operating_margin_pct","label":"MAR 營業利益率","value":15.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_fcf_margin_pct","label":"MAR FCF 利潤率","value":11.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_h_gross_margin_pct","label":"H 毛利率","value":20.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_h_operating_margin_pct","label":"H 營業利益率","value":7.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_h_fcf_margin_pct","label":"H FCF 利潤率","value":6.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chh_gross_margin_pct","label":"CHH 毛利率","value":50.59,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chh_operating_margin_pct","label":"CHH 營業利益率","value":25.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chh_fcf_margin_pct","label":"CHH FCF 利潤率","value":7.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wh_operating_margin_pct","label":"WH 營業利益率","value":36.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wh_fcf_margin_pct","label":"WH FCF 利潤率","value":30.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi6_sbc_share_based_compensa","label":"SBC (share-based compensation expense)","value":59,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿 https://stories.hilton.com/releases/hilton-reports-2026-third-quarter-results（同 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":364.18,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":17.13,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":69.73,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.13 → 9.13）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.19,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.43 → 10.45）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.17,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.98 → 12.0）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":9.13,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":10.45,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":12.0,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.11,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 9.03 → 9.13（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":49.15,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":15.65,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":18.19,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":39.89,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 9.13，分子＝快照價 364.18","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.165,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":13198.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 13972.0、現金 774.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":222.5,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":94229.63,"period":"2026-11-03","unit":"USD m","basis":"市值 81031.63 ＋ 淨負債 13198.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":12985.53,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":14108.25,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.26,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 362.12 / W52 315.13 / W104 283.98 / W250 212.95 / W250 13週斜率 1.57%"},{"id":"f_ma_w52","label":"52 週均線","value":315.13,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":283.98,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":212.95,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.57,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列示主要競爭對手為 Accor、Choice、Hyatt、IHG、Marriott、Wyndham；風險因子提及也與小型連鎖、獨立業者、家庭/公寓分享服務及分時度假業者競爭，並提到 AI 技術落後風險。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":"On a global scale, our primary competitors are Accor S.A., Choice Hotels International, Hyatt Hotels Corporation, Intercontinental Hotel Group, Marriott International and Wyndham Hotels & Resorts.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：公司與管理及特許合約爭奪戰中，競爭對手可能提供更優條件；亦與家庭與公寓分享服務競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":"We also compete against smaller hotel chains, independent and local hotel owners and operators, home and apartment sharing services and timeshare operators. If we are unable to compete successfully, our revenues or profits may decline.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Hilton 2026 淨單位成長指引 6%–7%，Q1 管線 52.7 萬間，占全球在建客房逾 20%","source":"Lodging Magazine / TopHotel Hilton Q1 2026","url":"https://tophotel.news/hilton-pipeline-hits-527k-rooms-in-q1/","excerpt":"Home » Hilton: Pipeline Hits 527K Rooms in Q1 Hilton: Pipeline Hits 527K Rooms in Q1 by Makenzie Huff April 28, 2026 The Monarch San Antonio, Curio Collection by Hilton © 2026 Hilton","as_of":"2026-04-28","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Hilton 管線達 543,100 間（2026-09-30，年增 5%），轉換占 Q3 開業 37%，CEO 預期 2026 轉換占 30–40%","source":"CoStar: Hilton CEO calls on conversions to keep up momentum in 2026","url":"https://www.costar.com/article/682699714/hilton-ceo-calls-on-conversions-to-keep-up-momentum-in-2026","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Marriott 2026 淨客房成長指引 4.5%–5%，低於 Hilton 6–7%","source":"Yahoo Finance: Marriott reports 4.2% rise in Q1 2026 global RevPAR","url":"https://finance.yahoo.com/markets/stocks/articles/marriott-reports-4-2-rise-104758932.html","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Hilton 2026 Q3 10-Q: 2026年5月發行 10 億美元 5.500% 2031 到期優先票據；循環信貸額度無借款，截至 2026-09-30 可用額度 1,894 百萬美元。","source":"Hilton Form 10-Q (period ended 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000054/hlt-20260930.htm","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因子/收入附註可能說明業主與加盟商無單一集中","source":"Hilton FY2025 10-K","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":"increase labor costs, which could adversely affect our results of operations and the results of hotels that we manage on behalf of third-party owners. Additionally, an increase in minimum wage rates could increase costs and reduce profits for us and our franchisees, which could, in turn, lower demand from third-party owners to add hotels to our system.","as_of":"2026-02-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CoStar/Tourism Economics Aug 2026 forecast: US supply growth 0.4% in 2026 and 0.6% in 2027, construction volume lowest in 12 years; 2026 RevPAR +4.4%, 2027 +2.1%; June 2027 RevPAR -0.8% on World Cup comp. No 2028 forecast found.","source":"CoStar U.S. Hotel Forecast Assumptions – August 2026","url":"https://www.costar.com/products/str-benchmark/resources/data-insights-blog/us-hotel-forecast-assumptions-august-2026","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261103","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lodging Econometrics Q3 2026: 2027 US openings forecast 668 hotels/72,667 rooms (+1.3% supply), revised down from 824 hotels in Q4 2025 report; under-construction 1,094 projects/137,371 rooms; project announcements recovering.","source":"Lodging Econometrics U.S. construction pipeline reports (Q3 2026 / Q4 2025)","url":"https://www.hotelmanagement.net/data-trends/le-us-hotel-openings-accelerate-through-2028","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"PwC Dec 2025 outlook expected supply growth to outpace demand in 2026, though supply remained below long-term averages (dissenting view).","source":"PwC US Hospitality Directions via Hotel Dive","url":"https://www.hoteldive.com/news/PwC-hospitality-directions-outlook-lodging-2026/809205/","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Hilton Q3 2026 (8-K, Oct 27 2026): system-wide comparable RevPAR +5.8%; FY2026 RevPAR guidance raised to 4%-4.5% from 3%-3.5%; Q4 guide +3%-3.5%; Middle East war and midterms cited as Q4 impacts; adjusted EBITDA guidance trimmed slightly.","source":"Hilton Form 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","triggers","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K FY2025 風險因素：酒店業受廣泛監管（特許銷售、行銷廣告、消費者保護、資料保護等），並提及反壟斷機關對併購/投資/合作日益嚴格審查；2010 年曾與 DOJ 就 ADA 達成和解。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":"We may also experience challenges from regulatory authorities in connection with our acquisitions, investments or partnerships, including from antitrust authorities who are increasingly scrutinizing such transactions","as_of":"2026-02-11","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"搜尋摘要稱英國 CMA 於 2026 年 3 月調查 Hilton、IHG、Marriott 是否經 CoStar STR 資料工具共享敏感價格資訊；CMA 稱尚無結論。未讀到原頁。","source":"WebSearch 摘要（Global Competition Review, 2026-03-02 Briefing）","url":"https://globalcompetitionreview.com/article/the-room-where-it-happens-the-briefing-2-march-2026","excerpt":null,"as_of":"2026-03-02","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"美國加州北區 IDeaS G3 RMS 演算法定價集體訴訟，2025-07-18 法官White裁定駁回對 Hilton、Hyatt、Wyndham 的訴求（原告未充分主張水平協議）；2026 年是否上訴未查到。","source":"Bloomberg Law: Hyatt, Hilton Win Suit As Court Rejects AI Price-Fixing Claims","url":"https://news.bloomberglaw.com/antitrust/hyatt-hilton-win-suit-as-court-rejects-ai-price-fixing-claims","excerpt":null,"as_of":"2025-07-18","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FTC 垃圾費用規則自 2025-05-10 生效，要求酒店訂房顯示總價；紐約市酒店隱藏費用禁令自 2026-02-21 生效。為全產業規範，非針對 Hilton；搜尋未見 2026 年 DOJ/FTC 針對 Hilton 的行動。","source":"NYC Mayor's Office 新聞稿 2026-01；LoyaltyLobby 2025-05-13","url":"https://www.nyc.gov/mayors-office/news/2026/01/mamdani-administration-bans-hotel-hidden-fees-and-unexpected-cre","excerpt":null,"as_of":"2026-01-21","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"HLT 10-K FY2025 風險因子把關稅列為可能壓低住宿需求的總體因素之一；海外房間占系統房間約 36%（2025），並受 OFAC 制裁等貿易規範約束。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":"changes in general economic conditions, including inflation, interest rates, supply chain disruptions, low consumer confidence, tariffs, increases in unemployment levels and depressed real estate prices resulting from the severity and duration of any downturn in the U.S. or global economy and financial markets","as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"產業層面：Akerman 2026 年 1 月通訊指出營建材料成本上升、融資成本高，許多開發商擱置專案（非 HLT 專屬；HLT 為輕資產管理／特許模式，影響經開發管線間接傳導）。","source":"Akerman, Leisure Law Insider Vol. 9 (January 2026)","url":"https://www.akerman.com/en/perspectives/the-impact-of-tariffs-on-the-hospitality-sector.html","excerpt":"Construction material costs have been increasing, shrinking developer margins, which have also been negatively impacted by higher financing costs, so many developers are putting projects on hold.","as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Hilton FY2025 10-K：美國以外房間數約占系統房間數 36%（2024 年 35%、2023 年 33%）；為輕資產授權/管理模式，無自有製造地，未見台灣/中國單點曝險揭露。","source":"Hilton FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":null,"as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Hilton 2026 Q3 財報/10-Q 前瞻聲明風險列舉供應鏈中斷、關稅與地緣衝突（含伊朗衝突）；未量化衝擊。","source":"Hilton Q3 2026 10-Q / earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000054/hlt-20260930.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Hilton Q3 2026（2026-10-27 公布）系統可比 RevPAR 幣別中性 +5.8%，入住率與 ADR 皆升；FY2026 RevPAR 指引由 3-3.5% 上調至 4-4.5%；Q4 指引 +3-3.5%；淨單位成長 6-7%；Q4 受期中選舉與中東戰爭影響。","source":"Hilton Q3 2026 results coverage (Hotel Dive / Lodging Magazine / TravelPulse)","url":"https://www.hoteldive.com/news/hilton-raises-full-year-revpar-outlook-after-strong-q3/872934/","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"區域分段：美國客房營收 +7%，中東與非洲客房營收 -5.6%（二手報導，中東戰爭拖累）。","source":"Travel Extra: Hilton results dragged down by decline in revenue in Middle East","url":"https://www.travelextra.ie/?p=156146","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"CoStar/Tourism Economics 美國預測：2026 RevPAR +4.4%，2027 降至 +2.1%（ADR +1.6%、需求 +1.1%）；2027 供給成長僅 0.6%、在建為 12 年低點。","source":"CoStar: Hoteliers adapt to new more optimistic outlook; Hospitality Net; CRE Daily","url":"https://www.costar.com/article/487933133/hoteliers-adapt-to-new-more-optimistic-outlook-across-industry","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"CoStar 2026 Q3 全球假設：2027 RevPAR 歐洲 31 市場 +2.7%、中國大陸六市場 +2.7%；亞太另有報導 2027 +2.7%。未找到整合的全球 2027 數字。","source":"CoStar Global Hotel Market Forecast Assumptions Q3 2026","url":"https://www.costar.com/products/str-benchmark/resources/data-insights-blog/global-hotel-market-forecast-assumptions-q3","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Hilton 10-K FY2025 risk factor: if Hilton fails to keep pace with AI developments, competitors or third parties may incorporate AI faster and impair its competitive position.","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":"If we fail to keep pace with rapidly evolving technological developments in AI, our competitive position and business results may suffer. Our competitors or other third parties may incorporate AI into their operations more quickly or successfully than us, or develop superior offerings with the aid of AI, which could impair our ability to compete effectively and adversely affect our results of operations.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Skift: Hilton and Marriott filings flag AI platforms as risk to direct bookings, possibly steering guests to OTAs and raising distribution costs.","source":"Skift: New Marriott and Hilton Filings Reveal Risks From AI Platforms to Direct Bookings","url":"https://skift.com/2026/02/11/new-marriott-and-hilton-filings-reveal-risks-from-ai-platforms-to-direct-bookings/","excerpt":"artificial intelligence, chatgpt, direct bookings, direct channel, distribution, earnings, future of lodging, google, hilton, marriott Key Points Hilton and Marriott both flagged AI platforms such as ChatGPT as new risks to their direct booking channels in recent SEC filings. Both hotel giants warned that AI could redirect bookings to online travel agencies (OTAs), increasing distribution","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Skift (2026-05)：連鎖飯店推動直訂約十年後，OTA 市占大致維持原樣，直訂通路未出現結構性轉移。","source":"Skift《Direct Booking Tug-of-War: Hotels' Long Bid to Take Back Power》","url":"https://skift.com/2026/05/27/direct-booking-tug-of-war-hotels-long-bid-to-take-back-power/","excerpt":"Ten years after Hilton, Marriott, and other chains began coaxing travelers to book directly, online travel agencies still control roughly the same slice of the pie.","as_of":"2026-05-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Hilton 10-K：Hilton Honors 會員 2.43 億，會員經 Hilton 偏好通路訂房可享即時優惠（付款滑桿、會員折扣、免費 Wi-Fi），為直訂導向的忠誠度機制。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":"Hilton Honors members who book through preferred Hilton channels also have access to instant benefits, including a flexible payment slider that allows members to choose nearly any combination of points and money to book a stay, an exclusive member discount and free standard Wi-Fi.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Skift：Hilton B2B 重組以與 Navan 直連為核心，Hilton for Business 企業註冊數超過 40 萬。","source":"Skift（經 wwstay 摘要）","url":"https://blog.wwstay.com/p/the-otas-arent-being-disintermediated","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 earnings release：全年調整後稀釋 EPS 指引 9.07–9.13 美元，調整後 EBITDA 4,060–4,080 百萬美元（已納入中東與 timeshare 授權費下修）；Q4 EPS 指引 2.32–2.38。","source":"SEC 8-K Hilton Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000049/q32026earningsrelease.htm","excerpt":"Diluted EPS, adjusted for special items, is projected to be between $9.07 and $9.13.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 2026（7/28）：全年 EPS 指引上調至 8.89–9.01（前 8.79–8.91），惟 Q3 EPS 指引 2.28–2.34 低於分析師共識 2.42，指引與共識有落差。","source":"Benzinga/MarketBeat via search summary","url":"https://www.marketbeat.com/instant-alerts/hilton-worldwide-nysehlt-releases-q3-2026-earnings-guidance-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布：Tickflow 28 位分析師均值 342.30（Buy，隱含上行 6.9%，資料 2026-08-01）；Barchart 均值約 356、最高 400；Benzinga 20 位均值約 314（日期不明）；Susquehanna 2026-08-11 目標價 353→345 維持 Neutral。","source":"Tickflow / Barchart / Benzinga 搜尋摘要","url":"https://www.tickflow.io/stock/HLT/forecast","excerpt":"Based on 28 analyst ratings, HLT has a consensus rating of Buy (2.36/5) with a +6.9% upside to the consensus target of $342.30.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill 顯示 FY2026 EPS 共識最新 9.14（31 位分析師，2026-10-24）；下一季營收預估 3 個月內下修 0.79%（日期與數字待核）。","source":"Chartmill HLT estimates","url":"https://www.chartmill.com/stock/quote/HLT/estimates","excerpt":"9.14 USD · Oct 24, 2026 · 31 analysts","as_of":"2026-10-24","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：僅例行訴訟（侵權、員工、反壟斷、消費者保護等），公司認為不致對財務有重大不利影響；未列證券集體訴訟","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":"We currently believe that the ultimate outcome of such lawsuits and proceedings will not, individually or in the aggregate, have a material adverse effect on our consolidated financial position, results of operations or cash flows.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-20 8-K Item 3.01：HLT 自願將主要上市地由 NYSE 轉至 Nasdaq，NYSE 11/4 收盤止、Nasdaq 11/5 開盤起，代號不變（非下市風險）","source":"SEC EDGAR 8-K 2026-10-20","url":"https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000045/hlt-20261020.htm","excerpt":"The Company expects that the listing and trading of the Common Stock on the NYSE will end at market close on November 4, 2026, and that trading will begin on Nasdaq at market open on November 5, 2026","as_of":"2026-10-20","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026 Q3 10-Q 揭露 OFAC 制裁影響 Hilton Frankfurt，公司終止 Frankfurt City Centre 租約（2026-10-31 生效）並收尾營運","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001585689/000158568926000054/hlt-20260930.htm","excerpt":"The Company has terminated its lease for the Hilton Frankfurt City Centre effective October 31, 2026, and is in the process of winding down operations at that location.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月8-K 11份，無 2.01/2.05/4.02 等併購、重組、重編項目；重大項目為債務發行（2025-12 與 2026-05 各 $1B 5.5% 票據）與信貸協議修訂","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001585689&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K Item 3 僅列例行訴訟，公司認為不致有重大不利影響","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm","excerpt":"We currently believe that the ultimate outcome of such lawsuits and proceedings will not, individually or in the aggregate, have a material adverse effect on our consolidated financial position, results of operations or cash flows.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 4.02（財報不可信賴）申報；搜尋未見 2026 SEC 調查或重編","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001585689&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"HLT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":30.13,"operating_margin_pct":24.01,"fcf_margin_pct":14.49,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MAR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.81,"operating_margin_pct":15.73,"fcf_margin_pct":11.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"H","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.11,"operating_margin_pct":7.21,"fcf_margin_pct":6.35,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CHH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.59,"operating_margin_pct":25.52,"fcf_margin_pct":7.09,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":36.38,"fcf_margin_pct":30.57,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WH","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"HLT"},"financial_history":{"ticker":"HLT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":8773000000.0,"revenue_yoy_pct":null,"gross_margin_pct":30.75,"operating_margin_pct":23.87,"net_income":1255000000.0,"diluted_eps":4.53,"free_cash_flow":1579000000.0,"fcf_margin_pct":18.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":10235000000.0,"revenue_yoy_pct":16.66,"gross_margin_pct":28.63,"operating_margin_pct":22.11,"net_income":1141000000.0,"diluted_eps":4.33,"free_cash_flow":1699000000.0,"fcf_margin_pct":16.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":11174000000.0,"revenue_yoy_pct":9.17,"gross_margin_pct":27.41,"operating_margin_pct":21.17,"net_income":1535000000.0,"diluted_eps":6.14,"free_cash_flow":1815000000.0,"fcf_margin_pct":16.24,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":12039000000.0,"revenue_yoy_pct":7.74,"gross_margin_pct":28.2,"operating_margin_pct":22.37,"net_income":1457000000.0,"diluted_eps":6.12,"free_cash_flow":1944000000.0,"fcf_margin_pct":16.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HLT/HLT_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**Hilton Worldwide Holdings Inc.** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Good morning, and welcome to the Hilton Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please note this event is being recorded. I would now like to turn the conference over to Mr. Charlie Ruehr, Vice President, Corporate Finance and Investor Relations. You may begin.

**Charlie Ruehr** (Executives):
Thank you, Chuck. Welcome to Hilton's Third Quarter 2026 Earnings Call. Before we begin, we would like to remind you that our discussion this morning will include forward-looking statements. Actual results could differ materially from those indicated in the forward-looking statements, and forward-looking statements made today speak only to our expectations as of today. We undertake no obligation to update or revise these statements. For a discussion of some of the factors that could cause actual results to differ, please see the Risk Factors section of our most recently filed Form 10-K. 
In addition, we will refer to certain non-GAAP financial measures on this call. You can find reconciliations of non-GAAP to GAAP financial measures discussed in today's call in our earnings press release and on our website at ir.hilton.com. This morning, Chris Nassetta, our President and Chief Executive Officer, will provide an overview of the current operating environment and the company's outlook. Kevin Jacobs, our Executive Vice President and Chief Financial Officer, will then review our third quarter results and discuss our expectations for the fourth quarter and full year. Following the remarks, we'll be happy to take your questions. With that, I'm pleased to turn the call over to Chris.

**Christopher Nassetta** (Executives):
Thank you, Charlie, and good morning, everyone. We're pleased to report a strong third quarter with top and bottom line results exceeding our expectations. Strength in travel demand, supported by favorable macro trends, is driving RevPAR outperformance, a trend that we expect to continue into 2027. We continue to lead the industry with net unit growth at scale, with the third quarter being our largest quarter of organic openings in our history, with very strong momentum heading into the fourth quarter. 
Our award-winning brands, strong commercial engines and powerful partnerships continue to further increase industry-leading market share, while a culture of innovation creates additional growth opportunities. Together, these drivers support meaningful free cash flow generation and shareholder returns, and we remain on track to return $3.5 billion to shareholders for the full year. For the third quarter, system-wide RevPAR increased 5.8% year-over-year, with rate and occupancy growth both ahead of expectations. 
RevPAR outperformance reflected strength in business and group demand, continued momentum following the World Cup and favorable calendar and holiday shifts. Globally, business transient RevPAR was up 8.3%, driven by outperformance in the U.S., with continued strength in manufacturing, technology and workforce lodging that all grew more than 10%. Leisure transient RevPAR was up 1.6% as demand normalized following a strong summer travel period. 
Group RevPAR was up 8.2%, driven by sequentially stronger demand from the second quarter, continued rate gains and favorable demand from social events and company meetings. For the full year, we now expect RevPAR growth of 4% to 4.5% as business transient momentum carries into the fourth quarter, particularly in the U.S., where supportive policy, increased private sector investment, including AI, and ongoing public infrastructure spending are supporting demand.
In the U.S., we are seeing middle-class real wage growth despite higher inflation, contributing to broad-based strength we have described as a C-shaped economy. We believe we are uniquely positioned to benefit from this demand given our exposure to business travel, especially small and medium-sized companies. Looking beyond 2026, we remain optimistic about the strengthening demand backdrop, particularly given the close correlation between hotel demand in our segments and nonresidential fixed investment, or NRFI.
NRFI growth for the past 6, and soon to be 7, quarters has been growing nearly 2x faster than the average rate over the prior 20 years, providing an unusually strong and durable macroeconomic backdrop for our business. We expect continued growth in GDP and NRFI, together with historically low industry supply growth, to support strong RevPAR growth over the next several years. 
Turning to development. We had another robust quarter of openings, adding more than 180 hotels and over 27,000 rooms to our system, our largest quarter ever for rooms added on an organic basis. Our luxury and lifestyle portfolios continue to grow the most quickly across categories, with trailing 12-month net unit growth rates of 11% and 20%, respectively. 
For the quarter, luxury and lifestyle openings comprised approximately 30% of total openings and included Conrad openings in Saudi Arabia and Japan and the debut of Canopy in Thailand, marking our 50th Canopy globally. Our collection brands continue to drive growth with the opening of nearly 20 Tapestry and Curio hotels across nearly all regions. Additionally, we surpassed 3,000 LXR rooms with the brand's debut in India, extending LXR's presence to this fast-growing region. 
In the third quarter, we delivered conversion openings across 12 of our 28 brands, including the debut of DoubleTree in Singapore, the debut of Spark in Italy and the conversion of 10 Select by Hilton YOTEL properties across 4 countries. Over the last 12 months, we've converted hotels from almost 60 different brands into our system. Because our brands drive RevPAR index premiums, we believe there is significant opportunity to continue growing through conversions, with Europe being a strong example of that opportunity. 
Independent non-branded hotels account for approximately 60% of the region's current supply, while Hilton represents just 2% of the region's supply. Across the system, conversions represented 37% of our openings this quarter, a trend we expect to continue as we execute against this opportunity. In the quarter, we signed approximately 30,000 rooms and are on pace to deliver mid-single-digit growth in signings for the full year, driven by strong signings in EMEA. 
Only 9 months into the year, we increased our development pipeline to more than 543,000 rooms, growing both year-over-year and sequentially versus the second quarter, with expansion in strategic markets and across chain scales. The pipeline now includes approximately 250 unique brand country combinations. In the quarter, we announced the signings of debuts of Outset Collection in Spain and of Motto in Japan. We continue to expand Tempo's global footprint with new signings in Switzerland, Thailand, Saudi Arabia and additional U.S. markets. We also announced the signing of our first Signia by Hilton on the Florida Gulf Coast, increasing the brand's pipeline to over 4,000 rooms and further accelerating its momentum. 
We are also expanding our presence in the Nordics, where we recently announced the signing of a new Hilton in Copenhagen, the first hotel under a multiyear development agreement with Scandic Hotels Group, the region's largest hotel operator. The agreement creates new opportunities to grow in Sweden, Norway, Denmark and Finland, high-value markets that have historically been very difficult to enter while introducing more travelers to our brands and Hilton Honors. 
System-wide new development construction starts continue to show incredible momentum, up over 40% year-over-year in the quarter, with all regions independently up more than 20%. Nearly half of our pipeline is under construction, and we continue to have more rooms under construction than any other hotel company, accounting for nearly 20% of industry share and 3.5x our share of existing supply. Our disciplined development strategy continues to strengthen Hilton's competitive positions as owners choose to join the system to benefit from the RevPAR premiums our brands deliver and the value of our commercial platform. 
We expect fourth quarter net unit additions to be above third quarter, delivering around the midpoint of our 6% to 7% range for 2026 and continuing to grow 6% to 7% annually over the next several years. Globally, Hilton is still less than 6% of supply, providing a long runway for continued growth. As technology continues to reshape every part of our lives and business in unprecedented ways, we believe our ability to connect the physical and digital elements of hospitality will create meaningful opportunities to harness the power of our proprietary technology platform across our business. 
In the years to come, we believe technology will become an even greater strategic advantage for Hilton, empowering our team members, strengthening performance for our owners and making it easier for guests to experience the very best of Hilton. As we continue to further differentiate Hilton's technology from the competition, we recently announced the appointment of Jeff Moore as Chief Technology Officer. Jeff brings more than 2 decades of experience building and scaling consumer logistics and enterprise platforms for some of the world's most recognized brands. We're excited for Jeff to help harness our industry-leading technology platform and to add to our existing talented leadership team. 
Keeping with this people-led, tech-powered strategy, last week, we announced that our listing exchange will move to NASDAQ, providing a platform aligned with our innovation and growth ambitions and positioning Hilton alongside some of the world's most innovative companies. As we approach the end of 2026, we're pleased to report that we remain on track to deliver against the ranges we laid out for our key metrics at our 2024 Investor Day. Looking ahead, we are more confident than ever in our ability to drive algorithm growth over the next several years. This will be driven by continued net unit growth, new brand growth, RevPAR index gains and incremental non-RevPAR business opportunities. 
Making all of this possible is our family of Hilton team members who continue to spread the light and warmth of hospitality in remarkable ways. Their dedication continues to earn global recognition, with Hilton named the #1 Best Place -- Workplace by Great Place to Work in 21 countries this year, more than ever before, in addition to recognition as the #1 best workplace in several regions, including Latin America, Asia and Europe. In fact, just this week, we were named #1 on Great Place to Work's inaugural list of best workplaces in the hotels and resorts in the U.S., another meaningful recognition of the culture our team members create every day across all of our hotels. 
We remain highly optimistic about our business and the opportunities ahead globally in the years to come. Our strong leadership team, technology orientation and brand-led, network-driven strategy gives us confidence in our ability to continue meeting the evolving needs of travelers and delivering strong returns to owners and shareholders. Now I'll turn the call over to Kevin for a few more details on our results for the quarter and our outlook going forward.

**Kevin Jacobs** (Executives):
Thanks, Chris, and good morning, everyone. During the quarter, system-wide RevPAR increased 5.8% versus the prior year on a comparable and currency-neutral basis. Growth was driven by rate and occupancy, both being ahead of expectations, strength in business and group demand, continued momentum following the World Cup and favorable calendar and holiday shifts. 
Adjusted EBITDA was $1.058 billion in the third quarter, up 8.4% year-over-year and exceeding the high end of our guidance range. Growth was affected by significant renovations in the ownership portfolio, continued conflict in the Middle East and performance of timeshare license fees and timing of other license fees. Management and franchise fees grew 9.5% year-over-year. For the fourth (sic) [ third ] quarter, diluted earnings per share adjusted for special items was $2.45. 
Turning to our regional performance. Third quarter comparable U.S. RevPAR increased 7%, driven by a strong World Cup and strong business and group demand that continued throughout the quarter. For full year 2026, we expect U.S. RevPAR growth to be in the mid-single digits. In the Americas outside the U.S., third quarter RevPAR increased 6.3% year-over-year, driven by strong group and business travel demand. Performance was led by Canada, Brazil and Argentina, all driven by rate strength. For full year 2026, we expect RevPAR growth to be in the mid-single digits. 
In Europe, RevPAR grew 6.5% year-over-year, led by Continental Europe, with strong performance in the business and group segments. Türkiye, Eastern Europe and resort markets also delivered strong performance. For full year 2026, we expect RevPAR growth to be in the mid-single digits. In the Middle East and Africa region, RevPAR declined 5.6% year-over-year as conflict-related pressures in the region intensified during the quarter. We now expect full year RevPAR in the region to decline by a low double-digit percentage as the conflict continues to affect the fourth quarter high season and we face challenging year-over-year comparisons. 
In the Asia Pacific region, third quarter RevPAR was up 7.3% in APAC ex-China, led by Southeast Asia, Japan and Korea. Business and group segments drove the strength in the region's performance. RevPAR in China declined 5.4% in the quarter, driven by a decline across all segments as consumer sentiment weighed on leisure and government restraints on business travel spilled into group demand. For full year 2026, we expect RevPAR growth in Asia Pacific to be in the low single digits, with RevPAR down low single digits in China. 
Turning to development. As Chris mentioned, for the quarter, we saw net unit growth of 6.0%, with the opening of 27,000 rooms in the quarter, the highest quarter of organic openings in our history. Even in a record quarter of openings, our pipeline grew quarter-over-quarter and year-over-year and has now reached a record 543,000 rooms. We continue to have more rooms under construction than any other hotel company, with approximately 1 in every 5 hotel rooms under construction globally slated to join the Hilton portfolio. We expect fourth quarter net unit additions to be above the third quarter, ending the year around the midpoint of our 6% to 7% range for 2026. We also expect to grow 6% to 7% annually over the next several years. 
Moving to guidance. For the fourth quarter, we expect system-wide RevPAR growth to be 3% to 3.5%. We expect adjusted EBITDA to be between $1.047 million and -- sorry, $1.047 billion and $1.067 billion, and diluted EPS adjusted for special items to be between $2.32 and $2.38, both displaying strong growth despite the effects of ongoing conflict in the Middle East, significant renovations in the ownership portfolio and lower expectations for timeshare license fees. 
For the full year, we expect RevPAR growth between 4% and 4.5% continued -- driven by continued business strength, especially in the U.S. We expect adjusted EBITDA of between $4.06 billion and $4.08 billion and diluted EPS adjusted for special items of between $9.07 and $9.13. Please note that our guidance ranges do not incorporate future share repurchases. 
Moving on to capital return. We paid a cash dividend of $0.15 per share during the third quarter for a total of $34 million. Our Board also authorized a quarterly dividend of $0.15 per share for the fourth quarter. For 2026, we expect to return approximately $3.5 billion to shareholders in the form of buybacks and dividends. Further details on our third quarter results can be found in the earnings release we issued earlier this morning. This completes our prepared remarks. We would now like to open the line for any questions you may have. We would like to speak with as many of you as possible, so we ask that you limit yourself to one question. Chuck, can we have our first question, please?

**Operator** (Operator):
Today's first question will come from Dan Politzer with JPMorgan.

**Daniel Politzer** (Analysts):
Chris, I think that it would be ideal to check on just some kind of the demand environment and how you're thinking about updated thoughts for 2027. It feels like a lot has changed from a lot of people on this call and their vantage point, but maybe you could kind of opine on how you're thinking about '27, the demand environment and kind of walk through the different buckets as you see across your customer base.

**Christopher Nassetta** (Executives):
Yes, happy to do it. Obviously, one of the most important questions that we could -- we can answer. I would say if you lift up, I mean, you heard everything that Kevin and I said about the third quarter, which was quite strong in terms of the fundamentals, demand growing at a great pace and supply continuing to be in our largest market in the U.S., quite muted, which is delivering a great result. 
As we go into the fourth quarter, the RevPAR guidance is down, but that just is to do with elections and primarily to do with calendar shifts that benefited Q3 and hurt Q4. If you look at underneath all that, things are getting better. As I sit in this very spot every Monday morning with my executive committee, everybody reporting from around the world, pretty much every week that we're talking, the demand patterns we feel better about. 
And I'd say really continuing to be driven by business transient, where we're seeing really, really strong growth, both in large and corporates and SMBs. Very good strength as you saw in the quarter in the group side and continued strength in leisure transient. And so on the last call, I talked about like there's been a lot of noise this year with World Cup and like year-over-year sort of comps. 
And so what I tried to do is sort of lift up and say like, if you cleanse it all, what we're basically on a run rate basis seeing was in the second half of the year, we thought like 2.5%, 2%, 2.5%. That obviously -- well, maybe not obviously, we feel a lot better about it today. If you look at the run rate that we see in the second half of the year now versus a quarter ago, just given basic strength in the business, particularly led by the U.S., I think the U.S. run rate is more like 4% and the global run rate is like 3.5%. So a lot better.
And I think it's as a result of all the things I talked about, like the basic macro setup is quite good. So the way -- and that's the basis for our 4% to 4.5% for this year. As I would think about next year, I mean, we're not -- we're in the early stages of budgets. We've been talking. We obviously see the current trends. I'll give you a directional sense of it. I think the way to think about it is, on a global basis, if the run rate is about 3.5%, you have things that are going back and forth. 
The benefits, I think, are clearly we see the U.S. continuing to pick up. I would hope and think that Mexico and the Middle East, which have been challenged this year, are going to normalize to a large degree, as with the case of Mexico, and I am hopeful to a large degree in the Middle East. We have seen stabilization in China, and I do think there's an opportunity to see some, not huge improvements, but some basic improvement from where we are. So I think all of those things are sort of helping. 
And then you have the mathematical World Cup thing that you got to deal with just basically quarter-over-quarter and largely in the second quarter, but to a degree in the third quarter. When we do the math and we lift up and look at all of those things, the good things, and then the headwinds on comparability, I would say next year we feel pretty darn good that the global RevPAR numbers are going to be in the 3% to 4% range.

**Operator** (Operator):
The next question will come from Lizzie Dove with Goldman Sachs.

**Elizabeth Dove** (Analysts):
I just wanted to ask on, I guess, flow-through and the algo, particularly as it looks to -- I think you called out some IMF impacts in HGV. I'm wondering if you could quantify that. And then I suppose as we look to next year, this year, I think you've had some headwinds, maybe on my math, $60 million or so from Middle East, owned and leased renovations, HGV. And then as you look to next year, I think you could get, hopefully, as you said, a chunk of these back. And so I'm wondering how you think about that and whether that kind of sets up for more of an above algo year.

**Christopher Nassetta** (Executives):
Yes. I mean I made the comment in my prepared comments that we feel really good about delivering algo in the next few years. I wouldn't say that lightly. We generally deliver on what we say we're going to deliver on. I think you -- embedded in the question, I think you captured sort of what's going on sort of in the beat and the flow-through to the raise, and it really is as simple as what we put in the press release and what Kevin said in his comments. You have -- the Middle East is a little more beaten up than we thought, and license fees in the timeshare segment are not performing at the level that we had expected. And pretty much the difference, if you look at the flow-through, the 10 would have been 30. It's pretty equally split between those 2 things.
I think if you lift up, which, again, I like to do, when you sort of talked about a $60 million number, and the reason we feel confident in delivering algorithm is that it's actually at a minimum probably $60 million. This year, we have some unique, not structural, just sort of onetime related events that are impeding algorithm growth. Those are the Middle East and Mexico. Those are ultimately ownership, which you talked about, and HGV. If you add those 3 things together, and I'll come back to each of those sort of talked about it, it's probably $60 million to $70 million, maybe even a little bit more. 
And so the way I think about it is, obviously, those things aren't producing this year, so I can't add them back in. But in my own mind, they're unique things that are not like structural impediments to the business. They're just happening. We can't control certain world events. And so I look at it as algorithm's alive and well. And as you think about the forward years, the reason we feel comfortable is the business is performing well. Unit growth, we feel really, really good about. The basic fundamentals on same-store growth, we feel really good about. 
And as I said, I'm pretty confident Mexico is going to normalize. I think the Middle East will be a heck of a lot better next year than this year. I mean that's my view. Ownership will take a couple of years, but the reality is ownership's probably in and of itself a $20 million-plus drag this year. When you look forward a few years, these are really, really good decisions. We're going to more than double the EBITDA contribution from those same assets because we're completely repositioning them. 
And we feel really good about, obviously, in a constant dialogue with HGV. They have some integration that they've been dealing with, the 2 big acquisitions and some comparability year-over-year issues. But we feel quite good about their ability to be sort of on algorithm growth as we think about the world going forward. So again, these are -- this is why we feel good about next year. 
It's why I'm giving you sort of a -- we're effectively giving you a range in same-store and unit growth. And bottom line, without being specific in the sense that we believe that we will be able to deliver algorithm growth. And some of it will be because these things are normalizing. The only one that I think takes a little bit more time, it will certainly be better next year, but to get to the doubling of prior EBITDA will take 2 or 3 years on the ownership side.

**Operator** (Operator):
The next question will come from Shaun Kelley with Bank of America.

**Shaun Kelley** (Analysts):
Chris, maybe to switch gears, multiple comments in there about the development environment and the NUG side, and obviously the organic additions are a huge accomplishment in this environment. So can we just talk a little bit more about what's underlying the confidence there? And maybe just put on the hat from the developer perspective a little bit. We're in a world where I'm starting to get that question again about higher interest rates potentially weighing on development. But the flip side is now we've got this really strong RevPAR environment, which should effectively attract some new encouragement in the space. So if you could kind of put all that together for us, would appreciate your thoughts.

**Christopher Nassetta** (Executives):
Yes. I mean there's a lot of swirl out there, obviously, Shaun, on the development side, and competitors have said different things. All I can tell you is what we're seeing. And what we're seeing is real -- and we gave you a few of the data points, very strong growth. Our brands on the conversion side continue to perform really, really well. We're taking a disproportionate share within the industry of opportunities there. It'll represent circa 40% of the growth this year. We feel like we have a lot of momentum going into next year. 
And new construction starts, I gave you some of the quarterly data, but for the full year, we think new construction starts will be up -- well over 20% in the U.S. and well in the sort of mid- to high teens globally. Yes, interest rates are -- actually, in the last week, interest rates have come down a little bit, but interest rates are higher. My own bet would be a year from now, the 10-year will be lower. Said that a few weeks ago, I think, on stage with you, and so far it's moving in a little bit the right direction. 
But in any event, what is, I think, underpinning it is implied in the question you asked, which is the performance is getting so much better. I mean you're talking about a year. Think about like last year in the -- like system in the U.S. was like down 1.5 or 2. This year, you're going to have 600 or 700 basis point flip around. Margins are growing. And yes, interest rates are higher, cost to build is higher, but it hasn't -- that hasn't been going up at a crazy rate. People are still able to get things financed, probably not as much as they'd like, but they're obviously getting financed if our starts are up. 
And this is self-serving but true, we're more financeable. So in a world where not much is getting done, we just continue to take, I think, more and more share of the lesser amount that is getting done. And so it's not easy. My development team, everybody listens to these calls, they're probably saying, "Why does he make our job seem so easy?" It's not. They're out in the trenches fighting and clawing and doing the great work that our development teams do. But we feel good about our -- where we're going to end up this year. We feel good about our 6% to 7% for the next few years.
I mean, you don't like -- I mean, one stat, which I love, is that, and when we talked about it is, like, we're 5.6% of the industry in the world. We're 20% of the rooms under construction. Like, to have 6% or 7% growth over the next 15 or 20 years, you really only need to get like up high-single-digit, 10%, when you do it mathematically, of what's available. It's not like it's crazy. I know you're like, "6% to 7%, how can you keep doing it?" It's not -- it's a big world. We got 28 brands. On average, we have 4 brands in all our major markets out of our 28. 
And we're -- and in most markets, we're very, very low, much lower than the 5.6% in a lot of the major markets around the world. So honestly, I've never been more excited about our growth opportunities than I am today. I think we have the right brands. We're doing a few more things, and we're deploying those in the right markets. We continue to build extraordinary relationships with owners around the world, including, importantly, our owner community here in the U.S. And it's our job, and we're going to do it.

**Operator** (Operator):
The next question will come from Brandt Montour with Barclays.

**Brandt Montour** (Analysts):
So I wanted to ask about AI and maybe just get your thoughts, Chris, on the rapid proliferation of Muse and consumer agents. How well are you set up today to accept direct bookings from these AI agents? What can you tell us about how fast this channel has grown for you so far? And kind of put us in the position of the consumer, do you think that from what you can see so far, these agents are set up to perhaps shift some share from OTAs to yourselves?

**Christopher Nassetta** (Executives):
Listen, I am very excited by what I see vis-a-vis Muse, Instinct and a whole bunch of other activities we're in the middle of. I think it is really -- I will say this probably for a long time, I think we're in the very early days of this opportunity with AI, particularly in the distribution space, but I love what I see. You should assume we're working with each and every one of them. You can find our products pretty much everywhere, even in the newer plays, we're deep in the middle of that. 
And I think in the end, what's really important to us is that we continue to build great and direct relationships with our customers. And I think all of these tools, while it's early and it's insignificant, to be honest right now in the industry, in terms of -- what you see in terms of flow of traffic and dollars of bookings and all that, this is the future, just like the internet was the future. 
I mean when humans like things to be done fast and easy, particularly when they're done well. And all of these products, while they're early and they're developing, I suspect there are going to be many more of them. They're going to be fast. They're going to be easy. They're going to be very effective, and humans like that, and they're going to trend to that. What I like about our setup is we have a really big platform. We believe we have the best products in the industry. 
We drive the highest market share, which I think is pretty good evidence that customers really like what we do, and we're a very large -- we use the U.S. as a surrogate, like we think we're about 25% of the quality inventory in the United States of America, which we think gives us an extraordinary seat at the table as all of the ones that you're talking about, I'm talking about and probably 20 others come into the market. 
And so we're there early with everybody, working with them to make sure that we're present. We have extraordinary teams that are working on content strategies. And last but not least, I do believe our tech stack is a huge competitive advantage. We have modernized our tech stack ahead of most, if not all. And I consistently hear from many of our counterparties that it's a lot easier for us to create direct connectivity. That's why we're able to do it and do it faster. 
So I think in the end, this will be -- we will continue to have a big relationship with our OTA partners for a certain segment of our business. I don't think that's going away anytime soon, but I do think this -- these tools are ultimately going to lead to a path of our being able to drive much more direct business at lower cost structures. [indiscernible] benefit us, but benefit our owner community, which is the most important element of it.

**Operator** (Operator):
The next question will come from Steve Pizzella with Deutsche Bank.

**Steven Pizzella** (Analysts):
Chris, recognizing it's only 1 week of data, but we saw select service RevPAR outperform luxury last week. Are you seeing any early signs that the C-shaped recovery is beginning to broaden? And can you remind us of Hilton's exposure and potential benefit from a recovery in select service?

**Christopher Nassetta** (Executives):
Yes. I mean I've talked about it a lot publicly and for a long time. I think I was talking about it during the summer of 2025, to be honest. Not that it was happening, but that it was going to happen simply because, again, I like to lift up. If you lift up and you looked at what was coming from a macro point of view, limited supply additions and huge growth rates in NRFI as a result of the massive investment cycle of AI, AI infrastructure, core infrastructure, all these things. It seemed undeniable to me, just rationally that, that wouldn't happen. 
And so okay, it's happening. And so we have been seeing the lower and the mid-section of the industry continue to pick up. Luxury has done well, too, slightly less well on a growth rate as it had been, but still quite strong. And so thus, the C. It's the mid and the bottom, particularly the mid continues to come up, really driven by business transient, which has just been on a tear. I mean, interestingly, business transient, when you really dig deep into the segmentation, is approaching pre-COVID levels, which I know a lot of people said, "Oh, it never will. People aren't going to travel for business." 
Well, we said they would, and they are, and it's not quite there, but my guess is in the next couple quarters, you're going to see it back, you're going to see segmentation generally back. So I think you'll continue to see this, but because like the whole thing on NRFI is, and why it's been such a high correlation is when people are investing, people have to run around the country and do it and that is generally the middle class of our country that is making all of that happen. They're building the data centers, the energy complex, the bridges, the highways. They're the ones that are making all this happen. 
And so as long as you're seeing NRFI at these elevated levels, which I think my own view is pretty unstoppable in the next at least couple of years, you're going to see this C shape thing keep going. I mean I think it's not because of politics at the moment being toxic with the midterm next Tuesday, that's why I put the comment. I mean we're actually -- I mean, it would be much higher if you didn't have the energy issue -- energy price increases related to the war in the Middle East. But even with it, you have real wage growth in the middle class right now. Imagine what it would be if we -- if the Middle East sort of gets resolved at some level. But with or without that, you have enough investment, enough activity by the trillions in this country that I think you're going to continue to see an acceleration in those trends.

**Operator** (Operator):
The next question will come from Stephen Grambling with Morgan Stanley.

**Stephen Grambling** (Analysts):
I wanted to touch on franchisee relationships. Just given some of the noise around franchisee-franchisor relationships, Chris, could you talk to how you would frame your conversations with owners, including any feedback from the lower charge-out rates that were started last year? If there's any opportunity to take those lower and just maybe framing where owner margins or EBITDA per key are now, perhaps versus history across the platform.

**Christopher Nassetta** (Executives):
Yes. I would say broadly, and I've talked about this on a number of prior calls, it's been a rough extended period of time for owners. I mean there's just no 2 ways to -- other way to say it. You had pretty anemic growth and reasonably high expense growth pre-COVID. COVID was obviously terrible for everybody, but particularly the owners, given the operating costs that they bear. You came out of COVID, you had this sugar high where it's like the government pushed out trillions of dollars, so everybody -- and nobody had to go to work. So it felt pretty good. 
And then inflation spikes, demand was sort of a tepid, and you had a couple -- 2 or 3 years where you were basically going backwards off of COVID, off the back of pre-COVID that wasn't particularly rosy. And so it's been a -- listen, there's no -- I'd say, there's no other way of saying it. It's been a tough run. But having said that, my conversations with our franchise community, and we had our big owners conference this summer in Vegas, so we had thousands of them, and I'm talking to owners all the time. They're quite constructive. 
And generally, I think they appreciate everything that we're doing. I mean, one, you have a backdrop, which is it getting a lot better, right? Like all this, we're a pretty good index for the country. So when we're starting to produce these kinds of numbers and you're seeing really reasonable margin growth, I think, the owner community, like anybody, when things are going better, I think people are happier. 
I think the things that we did, with what we call RISE and the reduction in system fees that we launched in June of 2025, so we started working on that in 2024, I think it's been really well received. We reduced loyalty costs for everybody by 30 bps. We gave 50 bps to those that got through customer satisfaction quality gate. About half the system is getting through it. And honestly, I've heard nothing but really, really good feedback. 
I haven't heard -- I mean, by the way, people that aren't getting it want it, but that's the behavior set we want. Every hotel I walk into, if they're not in it, they're telling me what they're going to do to get it. So it's creating the right sort of outcomes, I think, for everybody. We're not done there. We have what we've told our owners, we're working on RISE 2.
I'm not going to get into it in detail, but probably in the first quarter of next year, we'll be looking again at the system side loyalty to figure out, all right, where can we, by utilization of tech, AI, process change, the benefits of leveraging our scale, where do we think there are some ways that we can be even more efficient, that can translate in a positive way to our owners? So I would expect that we'll be out in the first quarter with that, and we'll never stop. Meaning our job, like our -- of course, the customers that sleep in hotels are critically important, but our owners are equally critically important. 
We -- there is no Hilton without our owners, and there is no growth and there is no NUG unless they are doing well, feeling good and making the kind of profits that they -- that are commensurate with what they need to continue to invest in the hotel and to continue to invest, potentially, new hotels and grow their business. So I think the summary of that is, in my conversations with our broad owner community, they're quite constructive and people are starting to feel a lot better as you would think and hope they would as a result of sort of the macro conditions that we see as a backdrop.

**Operator** (Operator):
The next question will come from Smedes Rose with Citi.

**Bennett Rose** (Analysts):
I appreciate your commentary around how 2027 could shape up from a RevPAR perspective. I was wondering maybe if you could talk specifically about what you're seeing kind of in the U.S. on the group side, either with sort of larger corporate bookings or some of the strength in the smaller enterprises that you've talked about before.

**Christopher Nassetta** (Executives):
Yes, it continues to be quite strong. If you look at the big group managed hotels at this point, we're up in the mid-single digits going into next year, something like that. So strong. Again, if you were to -- somebody asked, I didn't really do this, but if you were to rank performance by segment to get to that 3% to 4% next year, I think it would be business transient, group and leisure, all of which we believe will be positive, but in that order. 
And we think we've got quite a good backdrop on the group side. I mean group demand has generally been very good, and if you think about it, with supply having been really low for a long time, there just have not been a lot of group hotels that have been built in the United States of America. And that's the practical truth. High demand, not a lot of supply. Generally, laws of economics are alive and well. 
And so we feel quite good about it. But I do think business transient will lead the way again, just because you're seeing a real surge there and you're going to get the benefit, we think, for a full year next year, where this year, you're really sort of getting -- the real growth there has been kind of a half a year phenomenon.

**Operator** (Operator):
The next question will come from David Katz with Jefferies.

**David Katz** (Analysts):
From your public side advertising and reading through the release and obviously our conversations, there seems to be some building momentum around luxury, right? And I wanted, one, for you to just talk about that strategy a little bit. And two, conventional thinking is that, that sometimes requires increased investment. And just some color to that side of it also. And it's a topic I've been asking about for a long time and needed for completing Hilton's portfolio, et cetera.

**Christopher Nassetta** (Executives):
Yes. I mean at the risk of a filibuster because this could take a while, I'll try to be succinct. Luxury and lifestyle, we have been talking about for lots of years. You're right, David, you and others have asked about it. And we have continued to invest and spend a lot of energy on it, for all the right reasons. We think it does help create a halo effect for Honors, generally. And we feel like we have made really -- you heard some of the data on sort of recent performance, we think we've made really good performance. 
I mean Waldorf is flying and doing extraordinarily well. We're going to open 5 or 6 of the best hotels in the world in the next 12, 15 months within Waldorf, but Conrad equally, LXR picking up a lot of momentum. And then all our lifestyle brands with more to come. I mean we have another -- which I've mentioned publicly, in the skunk works right now that I would hope we would get out probably early next year, in the lifestyle space. 
So that has been -- it's not a new focus, it's been a continued focus. I think we're just picking up momentum. I mean one of the interesting data points is this year, between upper upscale and above, 45% of our deliveries this year will be represented in those categories. So it is working, and we are -- we certainly this year and I think generally have tilted that way. In terms of like the cost and key money, we did incrementally move our key money up. Just to be clear on that. 
I don't think -- I think key money has obviously always been more oriented to the high-end stuff, and key money generally has gone up a smidgen. I mean if I look at it like over the last 5 or 6 years, the percentage where we have any key money in our rooms under construction has moved 100 or 200 basis points, still unbelievably low. It's gone from 9 or 10 to 11. But the bigger deals are -- so it's very low. The bigger deals are where it gets spent. 
This year, the CapEx -- we have a bunch of things going on. We have the ownership stuff, which we've talked about, which is going to pay, we think, huge dividends, and there's a little bit more waiting. We just are finishing, as we sit here, a reboot of our world headquarters, and so there's a little bit more spending that goes on there. And a bit of a key money, and if you read the recent press releases, you can see oriented towards a couple of specific deals. 
If I look at where I think we'll end up relative to the averages, I don't think it will be a whole lot different than what we've spent over the last 5 or 10 years. I mean there'll be years where we spend more, where we have big, unique opportunities like we've had and described many times before. There'll be years when it's lower, where we don't have those opportunities. But I don't think it requires -- in order for us to continue to push the envelope on luxury and lifestyle, I don't think it requires a step change relative to historical norms.

**Operator** (Operator):
The next question will come from Robin Farley with UBS.

**Robin Farley** (Analysts):
Just going back to the unit growth question, you answered part of it already, which is that your use of key money hasn't really changed. Just wanted to ask about unit growth given most other C corps have lower unit growth guides either last quarter or this quarter. And just thinking about your confidence with that 6% to 7% for next year, can you give us a sense of how much of that is already on the books in terms of it's under construction and so almost perfect visibility versus what percent are conversions that you're relying on? Like will it accelerate or decelerate from this year's conversions?

**Christopher Nassetta** (Executives):
I think the number is like what's on the books is a little over 80%. So we would need to do a similar amount, maybe not quite as much on conversions given what's on the books because over last year and this year, you've started to see new construction -- new development construction start go up. As that happens, I don't think we will have less success in conversions, but the mathematics will change. As you have more new development, you'll see that ratio come down. 
I mean 40% is very high. Historically, it's been around 30%, if you look at long-term averages. My guess is, given we have a lot -- we're better at it and we have a lot more brands we can do conversions with, that we'll end up probably in the mid-30s. But 80% plus, we think is on the books. And we're quite -- it doesn't mean we're always right. We have a lot of work to do to get it done, but we're extraordinarily granular in our analysis of unit growth. We don't -- every single hotel is identified. Every region has very specific goals by brand, and so we feel good about it.

**Robin Farley** (Analysts):
So just mathematically, if conversions are sort of the part where you have a little less visibility than new construction, you actually have -- it sounds like higher conviction in your '27 growth rate than you did going into '26 even, just based on what...

**Christopher Nassetta** (Executives):
It's about the same. Well, I have more conviction in terms of what we're carrying over. It's actually -- I'll fact check myself. I'm looking at these guys. It's easier than this year because we have more new construction deliveries this year because of the ramp over the last couple of years. But by definition, I feel better about it because we have fewer that we have to fill in.

**Operator** (Operator):
The next question will come from Meredith Jensen with HSBC.

**Meredith Prichard Jensen** (Analysts):
I was hoping you might speak a little bit more about the technology side and prioritization of innovation with the appointment of the new CTO. And combined with, I think, some changes in the marketing leadership, how we might see the opportunities evolve there, how the approach towards guest experience operations and things like that might evolve?

**Christopher Nassetta** (Executives):
Yes. That's great. Well, Jeff just got here Monday, so I'm going to give him a few more days to like get it together. But we're really excited about his joining. One important note, and I said it in my prepared comments, is Michael Leidinger, who's been our CIO and his team have done an incredible job to put us in this position. And they're not going anywhere. By the way, Michael's here. He's remaining CIO, all we're doing is -- I'm doing is giving tech more oxygen by bringing somebody more senior at an EC, executive committee, level and reporting directly to me, just to supplement the great work that is already going on. 
And I think, listen, we could talk for hours, and I won't because we're going to run out of time. But I think there are really 3 buckets which I've talked about quite a lot, that we're really focused on is, one, efficiencies in the system, corporately, but also for the system we manage on behalf of owners. We're crazy not to. That can translate to benefits to shareholders, but most importantly, could translate -- because the bulk of the cost structure for us is managing the system, it can translate into meaningful benefits to owners. 
And so we're spending a huge amount of time on that. Some of it's AI, some of it's tech, some of it's process change, but it's all interconnected and technology is a core enabler of all of that. We talked about it earlier on the call. The distribution side of the business, we're super focused there. We're super excited about the advent of all of these new ways, agents are going to make our lives easier and how we're going to connect with them with the goal, again, to be driving better customer experiences, more direct experiences at a lower cost that will translate into more profitability for owners. The more profitable owners are, obviously, the happier they are, but the more likely they are to build more hotels, which becomes a virtuous cycle. 
And then to your question, I think on the customer experience side, there are some extraordinary things we're already doing and testing in how we're connecting our whole tech ecosystem and connecting the physical and the digital that I think will afford us the opportunity when you wake up in the next 2, 3, 4, 5 years to revolutionize the way we go to market, to revolutionize the way we customize at mass scale, both how we sell, what we sell, the experience on property and problem resolution. I'm not going to get into a lot of specifics for lots of important competitive reasons, but we're very excited, and hopefully, you're a customer, you can see some of it already, view that as a small down payment on what's to come.

**Operator** (Operator):
The next question will come from Mike Bellisario with Baird.

**Michael Bellisario** (Analysts):
Chris, on Europe, you noted a huge white space there for you. I guess a couple of parts here. What is owner sentiment like across the pond? And then what's the development dynamic there, just given some of the macro headwinds that are occurring, and then also the indirect impacts from the Middle East just on both conversions and the new development front?

**Christopher Nassetta** (Executives):
Yes. I mean, obviously, Europe on the new development front has -- continues to be more difficult, simply because the economics are harder, the financing markets aren't as robust. But we continue to have good success, largely in the focus in the limited service space, because that's what makes economic sense. But as I said in my prepared comments, I mean, if you think about Europe, 60% over the pond of the inventory is basically independent hotels, and we're a flyspeck in terms of our overall market share. 
And so it won't be all conversions, but I think if there'll be a heavy component of conversions in that environment to soft brands, hard brands, sort of things across the spectrum. I would say owner sentiment is quite good throughout -- I mean, every -- Europe's a big place. So I mean, I hate to generalize, but I'd say quite good, and not surprisingly, driven by performance. 
Performance in Europe, while many of the European economies have not been extraordinarily robust and are not maybe experiencing quite the surge that we are now starting to see in the U.S., from a travel point and tourism point of view, they've been really strong for an extended period of time, and they continue to maintain that strength. 
Obviously, with things going on in Eastern Europe and now the Middle East, which they're a lot closer to, people are rattled a bit. But from a development point of view, from a same-store point of view, we're going to have a terrific year in Europe. And from a development point of view, we're going to have one of our best years ever. So I'd say sentiment is broadly good.

**Operator** (Operator):
And this will conclude our question-and-answer session. I would like to turn the conference back over to Mr. Chris Nassetta for any additional or closing remarks. Please go ahead.

**Christopher Nassetta** (Executives):
Thank you, Chuck, and thank you, as always, for taking an hour out of your life and listening to where we -- our results, but more importantly, where we think the world is going. As I said, we feel really good about what we've been able to deliver, even better about what's to come, and we'll look forward to updating you after we close out the year. Take care, and have a great day.

**Operator** (Operator):
This concludes today's conference call. Thank you for your participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HLT_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜Christopher Nassetta｜guidance：全年系統 RevPAR 成長預期上調至 3% 至 3.5%，Q3 高於全年區間、Q4 略低。（原話："we're raising our full year system-wide RevPAR growth expectations"）
- 2026-07-28｜Kevin Jacobs｜guidance：Q3 指引：系統 RevPAR 約 +4%，含中東衝突影響。（原話："expect system-wide RevPAR growth to be approximately 4%."）
- 2026-07-28｜Kevin Jacobs｜guidance：全年調整後 EBITDA 指引 40.4 億至 40.8 億美元。（原話："adjusted EBITDA of between $4.04 billion and $4.08 billion"）
- 2026-07-28｜Kevin Jacobs｜guidance：指引區間不含未來庫藏股買回。（原話："our guidance ranges do not incorporate"）
- 2026-07-28｜Kevin Jacobs｜guidance：2026 全年中東與非洲 RevPAR 預期下調為高個位數至低雙位數下滑。（原話："we now expect RevPAR in the Middle East and Africa to be down in the"）
- 2026-07-28｜Kevin Jacobs｜guidance：全年美國 RevPAR 預期為中個位數成長。（原話："we expect U.S. RevPAR growth to be in the mid-single"）
- 2026-07-28｜Kevin Jacobs｜margin：Q2 調整後 EBITDA 10.54 億美元，年增 4.6%，高於指引上緣。（原話："Adjusted EBITDA was $1.054 billion in the second quarter"）
- 2026-07-28｜Kevin Jacobs｜margin：Q2 優於預期的來源：RevPAR 優於預期與 1,700 萬美元非 RevPAR 時間性項目。（原話："better-than-expected system-wide RevPAR growth and $17 million of"）
- 2026-07-28｜Kevin Jacobs｜margin：CFO 說明全年 EBITDA 拖累之一：3 家自有策略飯店關閉或大修，影響 2,000 萬至 2,500 萬美元。（原話："that's $20 million to $25"）
- 2026-07-28｜Kevin Jacobs｜margin：中東對 IMF 與基本費的影響超過 2,000 萬美元。（原話："that's over $20 million of impact just there in terms of IMF and"）
- 2026-07-28｜Kevin Jacobs｜margin：CFO 稱還原自有酒店與中東兩項後，全年高於長期成長算式（algorithm）。（原話："So if you adjust for that, the full year is"）
- 2026-07-28｜Kevin Jacobs｜margin：自有酒店由約 100 家降至約 46 家（租賃或少數合資）。（原話："We're down to about 46 hotels in leasehold or a few JVs today."）
- 2026-07-28｜Kevin Jacobs｜margin：特許與授權費全年達 algorithm 或更好。（原話："that's algorithm or better as well."）
- 2026-07-28｜Christopher Nassetta｜margin：CEO 拆解 Q2 美國 RevPAR 5.4%：約一半為實質運行率，另一半為基期與世足賽。（原話："if we were at 5.4% in the U.S. in Q2, I would say roughly half of that."）
- 2026-07-28｜Christopher Nassetta｜margin：CEO 稱 Q2 中東對系統 RevPAR 的拖累為整整 1 個百分點。（原話："the Middle East in the quarter was a full percentage"）
- 2026-07-28｜Christopher Nassetta｜margin：世足賽約貢獻 1.5% 至 1.7%，其餘約 100bp 為較易基期。（原話："the other 100 basis points was easier comps, plus"）
- 2026-07-28｜Christopher Nassetta｜margin：CEO 稱全年隱含美國底層運行率約 2.5%，下半年預期相近。（原話："when you look at the full year in the U.S. sort of implies around 2.5%."）
- 2026-07-28｜Christopher Nassetta｜commitment：管理層重申 2026 全年將回饋股東約 35 億美元。（原話："We remain on track to return $3.5 billion to"）
- 2026-07-28｜Kevin Jacobs｜commitment：全年淨單位成長維持 6% 至 7%，下半年強於上半年。（原話："We expect to deliver between 6% to 7% growth for the full year with"）
- 2026-07-28｜Kevin Jacobs｜commitment：CFO 稱可在可預見未來維持 6% 至 7% 的淨單位成長。（原話："we think we can deliver 6% to 7%"）
- 2026-07-28｜Kevin Jacobs｜commitment：CFO 稱對 NUG 範圍中點有信心，並稱對交付有高能見度。（原話："but we feel comfortable with the midpoint."）
- 2026-07-28｜Kevin Jacobs｜capital_allocation：Q2 派息每股 0.15 美元共 3,400 萬美元；全年買回加股息合計約 35 億美元。（原話："We paid a cash dividend of $0.15 per share during the second quarter"）
- 2026-07-28｜Christopher Nassetta｜customer：Q2 商務散客 RevPAR +5.7%，較 Q1 全球加速 3 點、美國加速 4 點。（原話："Business transient RevPAR was up 5.7%, a 3-point step-up globally"）
- 2026-07-28｜Christopher Nassetta｜customer：休閒散客 RevPAR +1.6%，世足賽優於預期，但受假期錯位與中東衝突抵銷。（原話："Leisure transient RevPAR was up 1.6%, supported by World Cup"）
- 2026-07-28｜Christopher Nassetta｜customer：中小企業商務散客成長約 7% 以上，大型企業約 4.5% 至 5%。（原話："We saw SMB growth in business transient sort of 7-plus percent roughly."）
- 2026-07-28｜Christopher Nassetta｜customer：CEO 稱中檔與中高檔由去年約 -2% 翻轉至 +4% 至 6%（C 型經濟敘事）。（原話："going from circa like minus 2% to plus 4% to 6%"）
- 2026-07-28｜Christopher Nassetta｜customer：CEO 稱 Q3 賽後仍見房價、週中商務與中小企業強勁，同時承認賽後資料不多。（原話："Now we don't have a ton of data post World Cup."）
- 2026-07-28｜Christopher Nassetta｜customer：Waldorf Astoria Miami Beach 簽約：CEO 稱此類交易都有 key money，不改變 key money 指引。（原話："There's key money in every deal like that, particularly in the United States."）
- 2026-07-28｜Kevin Jacobs｜risk：中東 Q2 RevPAR 年減約 30%，優於先前預期，管理層稱復甦仍不確定。（原話："RevPAR decreased approximately 30%"）
- 2026-07-28｜Kevin Jacobs｜risk：中國 Q2 RevPAR -2.2%，因團體受政府限制；全年預期低個位數下滑。（原話："RevPAR in China decreased 2.2% in the"）
- 2026-07-28｜Christopher Nassetta｜risk：CEO 稱先前預期中國今年持平，現在將再下滑約兩個百分點（口徑改變）。（原話："it's going to be down another couple of points, something like that."）
- 2026-07-28｜Christopher Nassetta｜risk：CEO 談 2027：自 2.5% 左右基線起算，預期會更好，同時承認結果可好可壞。（原話："Things can happen,"）
- 2026-07-28｜Christopher Nassetta｜risk：CEO 對 2027 基線的表述。（原話："I would take the over, that the 2.5% that we were sort of"）
- 2026-07-28｜Christopher Nassetta｜competition：CEO 描述近年美國業主利潤率下滑，新增敘事為業主獲利措施（忠誠度費減免、RISE、RISE 2）。（原話："And so margins have been"）
- 2026-07-28｜Christopher Nassetta｜competition：CEO 稱降費與 RISE 合計為業主帶來 75 至 100bp 利潤率。（原話："somewhere between 75 and 100 basis points in margin for owners."）
- 2026-07-28｜Christopher Nassetta｜competition：RISE 設有品質門檻，目前美國約一半系統取得完整優惠。（原話："roughly half the system right now in the United States"）
- 2026-07-28｜Christopher Nassetta｜competition：CEO 稱不知道競爭對手有類似做法，降費涵蓋全部級距。（原話："I am not aware that our competitors"）
- 2026-07-28｜Kevin Jacobs｜competition：CFO 說明折扣只在計畫費（忠誠度與計畫費類）。（原話："are in the program fees, in loyalty"）
- 2026-07-28｜Christopher Nassetta｜competition：管理層稱開發商偏好 Hilton 品牌因 RevPAR 溢價，Q2 溢價進一步擴大。（原話："driven by continued developer preference for Hilton brands"）
- 2026-07-28｜Christopher Nassetta｜product：Q2 推出新中高檔品牌 Undergraduate by Hilton。（原話："we launched Undergraduate by Hilton, a new upper mid-"）
- 2026-07-28｜Christopher Nassetta｜product：Q2 簽約約 43,000 間，為史上第二大單季。（原話："we signed approximately 43,000 rooms"）
- 2026-07-28｜Christopher Nassetta｜product：管線創高至 541,000 間，近半已在施工。（原話："Our pipeline now stands at a"）
- 2026-07-28｜Christopher Nassetta｜product：預期轉換型開業占全年開業約 40%。（原話："comprising approximately 40% of total openings."）
- 2026-07-28｜Christopher Nassetta｜product：與 Navan 建立業界首創直連，繞過中介與較貴通路。（原話："This direct connection bypasses both intermediary connections"）

### 問答異常語氣（迴避／改口／保留）
- HLT_Q2_2026_Earnings_Call_20260728.md｜問：Katz 追問 Waldorf Miami Beach 是否涉及 key money。｜答法：拒絕揭露單筆交易經濟條件，僅稱每筆此類交易都有 key money，且不改變整體 key money 指引，未給金額。
- HLT_Q2_2026_Earnings_Call_20260728.md｜問：Politzer 問 Q3 +4% 與隱含 Q4 低個位數的落差。｜答法：未直接給 Q4 數字，改以拆解基期與世足賽雜訊、談 2027 預算季，稱 Q4 沒問題。
- HLT_Q2_2026_Earnings_Call_20260728.md｜問：Montour 問 Q2 EBITDA 大幅超標為何未全額傳導至全年指引中點。｜答法：CFO 否認是保守，改以自有酒店與中東兩項拖累作答，未直接量化 Q2 超標金額如何分配。
- HLT_Q2_2026_Earnings_Call_20260728.md｜問：Pizzella 問 NUG 下半年加速的驅動與 2027 展望。｜答法：稱下半年加速是算術結果，未給 2027 具體數字，僅重申 6% 至 7% 範圍。

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
{"date":"20260703","verdict":"觀望","role":"條件式核心持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"淨單位成長（NUG）6–7% 可持續，pipeline + conversion + 國際低滲透支撐","columns":{"2Y 驗證點":"NUG 維持 ≥6%、pipeline 不縮","5Y 驗證點":"系統客房由 ~1.34M 增至 ~1.8M（5 年 ~6% 複利）","10Y 驗證點":"Hilton 佔全球客房由 ~7–8% 升向 ~11–12%","具體數字門檻":"NUG ≥6%/yr；pipeline ≥500K rooms（2025 末 520.5K，Q1'26 527K）","信息來源":"公司法說（2025 年報 NUG 6.7%）+ Lodging Econometrics pipeline 數據","漂移觸發":"連 2 季 NUG &lt;5% → 削弱（對齊 QC-35 2Y 假設）"}},{"id":"H2","text":"特許費模式 + Honors 忠誠度護城河抵禦 OTA/Airbnb disintermediation、維持高 ROIC 與 pricing","columns":{"2Y 驗證點":"direct booking 佔比穩/升、fee take-rate 不降","5Y 驗證點":"mgmt+franchise fee 以 ~7–9%/yr 複利、ROIC 維持 &gt;20%","10Y 驗證點":"Honors 會員 &gt;350M、直訂通路穩固","具體數字門檻":"Honors ~250M（2025）；fee rev +6.4%（2025 弱 RevPAR 年）","信息來源":"公司（2025 fee +6.4%）+ EHL/HospitalityNet OTA 佣金 15–30% 研究","漂移觸發":"連 4 季 fee 成長 &lt;4% 或 take-rate 結構下滑 → 削弱（5Y 假設）"}},{"id":"H3","text":"每年 ~$3.5B 迴購（−4–5% 股數/yr）將 ~9–10% 的底層 EBITDA 成長放大為 ~13–16% 的 EPS CAGR","columns":{"2Y 驗證點":"股數續降 4–5%/yr、迴購未因利率停擺","5Y 驗證點":"EPS 由 FY26 $9.03 複利至 ~$17–18","10Y 驗證點":"迴購 + 內生成長維持 EPS 雙位數複利","具體數字門檻":"2026 資本回饋 $3.5B；net debt/EBITDA ≤3.5x（Q1'26 3.1x）","信息來源":"公司（2026 指引 $3.5B 回饋、2025 買回 $3.182B）","漂移觸發":"net debt/EBITDA &gt;4x 或迴購年降 &gt;30% → 削弱（10Y 假設）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"消費/商務旅遊衰退 → RevPAR 收縮 + 高倍數 de-rate（戴維斯雙殺）","columns":{"對應假設":"H3 / H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"US STR/CoStar 週度 RevPAR、團體 booking pace","警戒閾值":"system RevPAR 連 2 月轉負 → 減碼評估"}},{"id":"R2","text":"同業相對溢價收斂：市場把 HLT 由 37x 壓向 MAR(30x)/IHG(20x) 水位（純倍數風險，非基本面）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"HLT vs MAR/IHG Fwd PE 溢價幅度","警戒閾值":"溢價無新基本面支撐而持續 → 列為估值下行情境（§11.4）"}},{"id":"R3","text":"利率長期高檔：迴購依賴舉債，負股東權益 + net debt $11.8B 使再融資成本上升、EPS 放大器熄火","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"net debt/EBITDA、加權平均債務成本、迴購年額","警戒閾值":"net debt/EBITDA &gt;4x 或利息覆蓋 &lt;5x → 需 ≥50% 機率才砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":8.2,"ev5y_pct":31.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式核心持倉","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.9,"ev5y_pct":31.0,"irr_base_pct":8.2,"max_dd_pct":-55.0,"bull_5y_price":585.0,"bear_5y_price":216.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":null,"price_at_dd":338.12,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HLT_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
