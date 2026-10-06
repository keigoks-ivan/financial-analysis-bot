你是 stock-analyst **v20 判斷 agent**，標的 3017（20261005）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"3017","date":"2026-10-05","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3017_20261005/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3017_20261005/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP 合併）","value":49.1,"period":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","unit":"十億 TWD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","citation":"公司 Q2 2026 Earnings Call 逐字稿（3017_Q2_2026_Earnings_Call_20260812.md）"},"note":"查無"},{"id":"f_kpi1","label":"毛利率","value":32.57,"period":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","citation":"公司 Q2 2026 Earnings Call 逐字稿"},"note":"查無"},{"id":"f_kpi2_gaap_ifrs_non_gaap","label":"GAAP 營業利益率（台灣 IFRS，無 non-GAAP 口徑）","value":27.44,"period":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","citation":"公司 Q2 2026 Earnings Call 逐字稿；營業利益約 13.5 十億為 49.1×27.44% 推算"},"note":"查無"},{"id":"f_kpi3_eps","label":"EPS","value":24.37,"period":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","unit":"TWD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","citation":"公司 Q2 2026 Earnings Call 逐字稿"},"note":"查無"},{"id":"f_kpi5","label":"管理層指引","value":null,"period":"Q2 2026 法說（2026-08-12）","unit":"文字","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 2026 法說（2026-08-12）","citation":"公司 Q2 2026 Earnings Call 逐字稿"},"note":"不適用","needs_sonnet":true},{"id":"f_kpi6","label":"存貨天數","value":145,"period":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","unit":"天","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 2026（季末 2026-06-30，法說 2026-08-12）","citation":"公司 Q2 2026 Earnings Call 逐字稿"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-12","period":"2026-08-12","unit":"date","basis":"距今 None 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-12"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_vrt_gross_margin_pct","label":"VRT 毛利率","value":38.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_operating_margin_pct","label":"VRT 營業利益率","value":19.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_fcf_margin_pct","label":"VRT FCF 利潤率","value":25.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_etn_gross_margin_pct","label":"ETN 毛利率","value":35.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_operating_margin_pct","label":"ETN 營業利益率","value":17.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_fcf_margin_pct","label":"ETN FCF 利潤率","value":13.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_gross_margin_pct","label":"2308.TW 毛利率","value":35.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_operating_margin_pct","label":"2308.TW 營業利益率","value":16.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_fcf_margin_pct","label":"2308.TW FCF 利潤率","value":11.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4","label":"自由現金流（上半年累計）","value":19.2,"period":"H1 2026（季末 2026-06-30，法說 2026-08-12）","unit":"十億 TWD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"H1 2026（季末 2026-06-30，法說 2026-08-12）","citation":"公司 Q2 2026 Earnings Call 逐字稿；營業現金流 26.3 十億（YoY +176%），資本支出約 7.1 十億（逐字稿誤植為 71）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":3585,"period":"2026-10-05","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-05"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.62,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.24 → 3.26）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.0 → 5.05）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":1.59,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.28 → 6.38）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.26,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":5.05,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":6.38,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":9.4,"period":"2026-06-23 → 2026-09-26","unit":"%","basis":"FY1 共識 EPS 2.98 → 3.26（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-10-05","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-05","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price None / W52 None / W104 None / W250 None / W250 13週斜率 None%"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"搜尋摘要稱奇鋐在 GB200／GB300 水冷板市場握有 40–50% 市占，1Q26 營收年增約一倍（摘要未標明確切來源頁，市占數字未經原頁驗證）","source":"WebSearch 摘要（查詢：奇鋐 3017 市占 液冷 競爭 雙鴻 2026）","url":null,"excerpt":"在GB200與GB300水冷板市場上，奇鋐握有40-50%市占率，1Q26營收較去年同期翻倍成長。","as_of":"2026-04-21","retrieved_at":"2026-10-05","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"GB300 認證名單水冷板點名奇鋐、快接頭點名富世達（奇鋐子公司）；雙鴻 GB300 水冷板已量產、水冷營收占比快速提升，對奇鋐形成競爭（來自討論區／摘要，非官方）","source":"股市爆料同學會 cmoney 討論串／搜尋摘要","url":"https://www.cmoney.tw/forum/article/178570808","excerpt":"在GB300認證名單中，水冷板點名奇鋐，快接頭點名富世達（奇鋐子公司），而雙鴻GB300水冷板量產、水冷營收占比快速提升，對奇鋐形成實質競爭。","as_of":"2025-10-28","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"雙鴻稱已取得全球四大 CSP 的 ASIC 冷板訂單，2H26 起量產出貨（摘要中公司名稱寫作 Auras／3324.TW，實指雙鴻 3324，非 3017）","source":"BigGo Finance 摘要","url":"https://finance.biggo.com/news/1T1Dvp4B6BW68sl_ASd1","excerpt":"Auras has secured ASIC cold plate orders from the world's four largest CSPs, with related products set to begin mass production and shipment starting in the second half of 2026.","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Nvidia 在 Vera Rubin 世代集中採購冷板並點名四家供應商（AVC＝奇鋐、Cooler Master、Jentech、Delta），奇鋐為四家之一，非獨家","source":"Digitimes: Nvidia standardizes Vera Rubin liquid cooling, names four cold plate suppliers","url":"https://www.digitimes.com/news/a20260318PD231/nvidia-rubin-liquid-cooling-ai-server-launch.html","excerpt":"Nvidia will centralize procurement of cold plates, naming four suppliers: Asia Vital Components (AVC), Cooler Master, Jentech, and Delta Electronics.","as_of":"2026-03-18","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"法人個股報告稱 VR200 水冷產品 8-9 月開始出貨，明年預計新美系客戶加入採購，奇鋐將成為水冷板及機殼供應商之一（客戶端為多來源）","source":"BlueJay on X 個股報告 2026/08/05 奇鋐","url":"https://x.com/BlueJay87476298/status/2087661307352977719","excerpt":"VR200水冷產品於8-9月開始出貨，明年預計將有新美系客戶加入採購，奇鋐將成為水冷板及機殼供應商之一。","as_of":"2026-08-05","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025 年度年報揭露：前三大客戶合計占銷貨淨額 51.97%，最大客戶（甲）占 22.74%，丙客戶占比由 10.50% 升至 19.73%。客戶皆以代號揭露，未具名。","source":"WebSearch 摘要（引述奇鋐 2025 年度年報；搜尋結果未指明確切頁面網址，未逐頁核對年報原文）","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Digitimes 報導將客戶集中度列為奇鋐主要風險之一（與執行、價格並列）；摘要未提供具名客戶或比重。此為搜尋摘要轉述，未讀頁面原文。","source":"Digitimes, Asia Vital Components sees stronger AI server demand and faster liquid cooling adoption（經搜尋摘要轉述）","url":"https://www.digitimes.com/news/a20260813PD220/avc-ai-server-liquid-cooling-demand-adoption.html","excerpt":null,"as_of":"2026-08-13","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"液冷供應鏈原按每年 5～8GW 建置，現需求達 17GW 以上；新增產能需 18～36 個月才能上線（來源為搜尋摘要，原頁未讀）。","source":"thecoolingreport.com / nVent 新聞稿相關搜尋摘要（Where Cooling Components Come From and Why They're Late: The 2026 Data Center Cooling Supply Chain Guide）","url":"https://thecoolingreport.com/intel/data-center-cooling-supply-chain-guide-2026.html","excerpt":"the supply chain was built for 5 to 8 gigawatts per year, but the market is now demanding 17-plus gigawatts, requiring additional manufacturing capacity that takes 18 to 36 months to bring online.","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"同業 nVent 宣布租下 Blaine 16 萬平方呎廠房擴充液冷產能，預計 2027 上半年投產；為其三年內第三次液冷擴產、累計新增逾 40 萬平方呎。","source":"nVent Electric 新聞稿：nVent Expands Data Center Liquid Cooling Capacity","url":"https://investors.nvent.com/press-releases/press-release-details/2026/nVent-Expands-Data-Center-Liquid-Cooling-Capacity/default.aspx","excerpt":"The new site is expected to begin production in the first half of 2027. This marks nVent's third data center liquid cooling capacity expansion in three years, adding more than 400,000 square feet of new space overall.","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Goldman Sachs 預測 AI 伺服器液冷滲透率 2024 年 15%、2025 年 54%、2026 年 76%；新建 AI 資料中心液冷滲透率 2028 年預期逾 75%。","source":"搜尋摘要彙整（Goldman Sachs 預測，聚合頁轉述；原始報告日期未取得）","url":null,"excerpt":"Goldman Sachs forecasts AI server liquid cooling penetration rising from 15% in 2024 to 54% in 2025 and 76% in 2026.","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"機架功率持續上升：GB200 NVL72 約 132kW，NVIDIA Rubin Ultra NVL576（2027 年）預計近 600kW／機架；L2L 液冷預期自 2027 年起快速放量。","source":"搜尋摘要彙整（TrendForce 等，Data Center Liquid Cooling 市場報告）","url":"https://www.trendforce.com/presscenter/news/20250821-12682.html","excerpt":"liquid-to-liquid (L2L) cooling is expected to gain rapid traction beginning in 2027, offering higher efficiency and stability.","as_of":"2025-08-21","retrieved_at":"2026-10-05","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"奇鋐 2026-08-12 法說會表示水冷滲透率將持續上升；Google TPU 預計成為其第二大水冷客戶，TPU V8 水冷板 2026 Q3 起供貨、初期份額 40～45%，預估 2026 年貢獻約 NT$100 億營收（為搜尋摘要轉述，非公司原文）。","source":"敏捷投資的貓（vocus）：奇鋐 3017: 液冷散熱滲透率持續上升(2026 08 12法人說明會)","url":"https://vocus.cc/article/6a801565fd8978000125a246","excerpt":"Chi Kuen noted that water cooling penetration rates will continue to rise.","as_of":"2026-08-12","retrieved_at":"2026-10-05","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"市場研究預估全球資料中心液冷市場 2026 年約 60 億美元，2035 年 271 億美元，年複合成長 18.2%（供市場規模參考；各家報告 CAGR 範圍 18%～31%）。","source":"GM Insights：Data Center Liquid Cooling Market Size & Share 2026-2035（搜尋摘要）","url":"https://www.gminsights.com/industry-analysis/data-center-liquid-cooling-market","excerpt":"The global data center liquid cooling market is set to expand from USD 6 billion in 2026 to USD 27.1 billion by 2035, growing at 18.2% CAGR.","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"零組件端：GPU 伺服器供給正常化預期不早於 2027 年中；CPU 伺服器較快，約 2026 年底至 2027 年初（為二手彙整站搜尋摘要，涵蓋電源、記憶體、散熱 IC 等整體伺服器零組件，非專指液冷散熱）。","source":"limchip.com：AI Server Component Shortage 2026: Power, Memory and Thermal Supply Pressure","url":"https://www.limchip.com/news/i-server-component-shortage-2026.html","excerpt":"Significant normalization in the GPU-based server segment is not expected before mid-2027, though the CPU server and VPS markets will stabilize faster","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["thesis.R","triggers"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國 2026-04-02 公告改制 Section 232：鋁、鋼、銅產品加徵 50%，以鋁／鋼／銅為主要成分的衍生品加徵 25%，改按完整海關價值計算，4/6 生效。此為一般性規定，來源未提及 3017 或其產品。","source":"Perkins Coie, restructured and additional Section 232 tariffs: aluminum, steel and copper","url":"https://perkinscoie.com/insights/update/restructured-and-additional-section-232-tariffs-aluminum-steel-and-copper","excerpt":"On April 2, 2026, President Trump signed a proclamation that changes how Section 232 tariffs are calculated, now applying to the full customs value of products containing steel, aluminum, and copper, effective April 6.","as_of":"2026-04-02","retrieved_at":"20261005","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"奇鋐越南5期廠啟動興建，土建與機電工程合約合計約新台幣77.81億元（土建65.77億、機電12.04億）。","source":"中央社 CNA：東協財經/奇鋐越南5期廠啟動興建 土建與機電計投入77.8億元","url":"https://cna.com.tw/news/afe/202609080176.aspx","excerpt":"合計投下新台幣約77.81億元","as_of":"2026-09-08","retrieved_at":"20261005","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"董座表示散熱風扇用永久磁鐵屬稀土、低溫錫膏涉及管制金屬；公司預先備貨，並把所有錫膏留給水冷產品。","source":"TechNews 科技新報：奇鋐 Feynman 相關報導","url":"https://finance.technews.tw/2025/06/06/feynman/","excerpt":"奇鋐只能預先備貨，確保短期供應無虞，並將所有錫膏保留給水冷產品","as_of":"2025-06-06","retrieved_at":"20261005","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"董座稱越南為「中國+1」主要據點，已開工三棟新廠並購置20公頃土地準備擴建；另規劃在德州北部或墨西哥設打樣線，量不大、需客戶支持才大規模投入。","source":"TechNews 科技新報：奇鋐 Feynman 相關報導","url":"https://finance.technews.tw/2025/06/06/feynman/","excerpt":"目前規劃在德州北部或墨西哥設立打樣線","as_of":"2025-06-06","retrieved_at":"20261005","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026上半年伺服器應用營收占比66.14%（去年同期48.41%）；伺服器與網通營收649.19億元，年增153.38%；Q2營收491.21億元年增65.98%；上半年981.59億元年增85.46%","source":"富果直送 奇鋐法說會重點內容備忘錄 20260812","url":"https://blog.fugle.tw/post/earnings-call-3017-2026-08-12","excerpt":null,"as_of":"2026-08-12","retrieved_at":"2026-10-05","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"公司未對外拆分水冷營收占比；水冷板月產能由2025年底20萬組提升至2026年底100萬組","source":"富果直送 奇鋐法說會重點內容備忘錄 20260812","url":"https://blog.fugle.tw/post/earnings-call-3017-2026-08-12","excerpt":null,"as_of":"2026-08-12","retrieved_at":"2026-10-05","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2毛利率創高32.57%（季增2.8pp、年增8.16pp），伺服器相關營收占約66%；Q2營收季增0.17%、年增65.98%","source":"Taipei Times, Asia Vital Components' Q2 earnings and margins surpass expectations","url":"https://www.taipeitimes.com/News/biz/archives/2026/08/13/2003862391","excerpt":null,"as_of":"2026-08-13","retrieved_at":"2026-10-05","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"工商時報報導奇鋐ASIC水冷訂單放量、Q3營運優於Q2；BigGo整理法說：ASIC明年將超越GPU","source":"工商時報 / BigGo Finance","url":"https://www.ctee.com.tw/news/20260812701734-430201","excerpt":null,"as_of":"2026-08-12","retrieved_at":"2026-10-05","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"市場規模預估（第三方研究機構，口徑差異大）：AI伺服器液冷2026年>170億美元 vs 2025年89億美元（約+91%）；另有報告給出2025年66億美元→2034年618億美元（CAGR 28.7%）","source":"WebSearch 彙整（Technavio／MarketsandMarkets／Marketintelo 等聚合結果）","url":"https://www.digitimes.com/news/a20260408PD227/ai-server-liquid-cooling-heat-sink-demand-avc-revenue.html","excerpt":null,"as_of":"2026-04-08","retrieved_at":"2026-10-05","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"微通道蓋板（MLCP/MCL）被視為 Rubin 架構的優選方案，預期 2026 下半年隨 Rubin 放量規模化應用；為傳統冷板之後的下一代方案","source":"TrendForce／搜尋摘要（NVIDIA Rubin GPU Liquid Cooling Revolution: Rise and Challenges of MCL Tech）","url":"https://www.trendforce.com/research/download/RP251104EC","excerpt":"Microchannel Lids (MLCP), with advantages like high thermal conductivity efficiency and low flow resistance, are considered the preferred solution for the Rubin architecture and are expected to achieve scaled application alongside the Rubin architecture launch in the second half of 2026.","as_of":"2025-11-04","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"台積電先進封裝研發主管在 SEMICON Taiwan 2026 稱，五年內系統總功耗可能升約 6 倍，散熱與供電為兩大挑戰；TrendForce 報導台積電評估晶片級微通道冷卻","source":"TrendForce News: TSMC Eyes Chip-Level Microchannel Cooling as AI System Power Could Rise 6× in Five Years","url":"https://www.trendforce.com/news/2026/09/02/news-tsmc-eyes-chip-level-microchannel-cooling-as-ai-system-power-could-rise-6x-in-five-years/","excerpt":"total system power could rise around sixfold over the next five years, making power delivery and thermal management two key challenges for next-generation AI systems.","as_of":"2026-09-02","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Corintis 微流體冷卻可作為標準冷板的直接替代品或整合進 GPU 封裝，稱晶片溫度較標準冷板低至 3 倍；計畫 2026 年底前產能達百萬片冷板","source":"Data Centre Insight: How Microfluidics and Immersion Cooling is Key for Data Centre Cooling 'Breakthrough'","url":"https://datacentreinsight.co.uk/2025/12/23/how-microfluidics-and-immersion-cooling-is-key-for-data-centre-cooling-breakthrough/","excerpt":"Corintis' microfluidic technology uses generatively designed microfluidic channels directly at the chip, either as a drop-in replacement for standard cold plates or integrated into the GPU package itself.","as_of":"2025-12-23","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"產品組合由風扇／3DVC 氣冷轉向液冷系統，ASP 與獲利結構改善（產品／商業模式轉移，非銷售通路轉移）","source":"富果直送 奇鋐法說會重點內容備忘錄 20260514","url":"https://blog.fugle.tw/post/earnings-call-3017-2026-05-14","excerpt":"奇鋐的產品組合正從傳統風扇和3DVC氣冷技術轉向液冷系統，不僅提升了產品平均售價（ASP），也顯著改善了獲利結構。","as_of":"2026-05-14","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"公司角色由單一散熱零組件供應商擴大為涵蓋水冷板、分歧管、機箱／機櫃及部分系統產品的 Rack-level thermal solution supplier","source":"共識之外 Beyond Consensus（vocus）奇鋐進軍AI伺服器rack level散熱系統","url":"https://vocus.cc/article/6aa60718fd89780001f1a1d7","excerpt":"公司於AI伺服器供應鏈中的角色正在由單一散熱零組件供應商，逐步擴大為涵蓋水冷板、分歧管、機箱／機櫃及部分系統產品的Rack-level thermal solution supplier。","as_of":"2026-10-05","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"董事長稱 2026 為液冷元年，液冷模組產能由每月 20 萬套擴至 100 萬套（Digitimes）","source":"Digitimes: Asia Vital Components plans major liquid cooling expansion, expects market shift","url":"https://apps.digitimes.com/news/a20260312PD226/avc-liquid-cooling-chassis.html","excerpt":"AVC chairman Ching-hang Shen said the company will significantly expand liquid cooling production in 2026, calling the year the \"liquid cooling era,\"","as_of":"2026-03-12","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"搜尋結果未見銷售通路去中介化／D2C／訂閱化的具體證據；客戶端 ASIC 伺服器占伺服器營收 20–30% 並預期成長","source":"Digitimes / 搜尋摘要","url":"https://www.digitimes.com/news/a20260813PD220/avc-ai-server-liquid-cooling-demand-adoption.html","excerpt":"ASIC servers featuring custom chips designed by cloud giants as alternatives to Nvidia GPUs already contributing 20–30% of server revenue, and that share is expected to grow.","as_of":"2026-08-13","retrieved_at":"2026-10-05","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FactSet 調查（2026-09-22）：奇鋐 2026 年 EPS 預估中位數上修至 104.82 元（前值 104.03），預估範圍高 109.44、低 93.05；預估目標價 4000 元。","source":"鉅亨速報 - Factset 最新調查：奇鋐(3017-TW)EPS預估上修至104.82元，預估目標價為4000元","url":"https://m.cnyes.com/news/id/6612647","excerpt":null,"as_of":"2026-09-22","retrieved_at":"2026-10-05","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"工商時報報導：法人喊買，目標價 3,580 元，營收創高、輝達與 ASIC 訂單進補。","source":"工商時報：奇鋐營收創高 輝達、ASIC訂單進補 擴產再擴產 法人也喊買 目標價3,580元","url":"https://www.ctee.com.tw/news/20260809700357-430201","excerpt":null,"as_of":"2026-08-09","retrieved_at":"2026-10-05","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Yahoo 目標價一覽（Q2 財報後）：凱基 2026 EPS 102.78 元、目標價 4,000；元大投顧 EPS 100.86、目標價 3,855；群益 EPS 99.52、目標價 3,580；內外資最高喊 4 字頭。日期未明確，約在 Q2 財報後。","source":"Yahoo 股市：目標價1表看》奇鋐第2季獲利炸裂！內外資同看好最高喊「4字頭」","url":"https://tw.stock.yahoo.com/news/%E7%9B%AE%E6%A8%99%E5%83%B91%E8%A1%A8%E7%9C%8B-%E5%A5%87%E9%8B%90%E7%AC%AC2%E5%AD%A3%E7%8D%B2%E5%88%A9%E7%82%B8%E8%A3%82-%E5%85%A7%E5%A4%96%E8%B3%87%E5%90%8C%E7%9C%8B%E5%A5%BD%E6%9C%80%E9%AB%98%E5%96%8A-4%E5%AD%97%E9%A0%AD-%E6%8F%9AAI%E6%B0%B4%E5%86%B7%E4%B8%8B-033218008.html","excerpt":null,"as_of":"2026-08-13","retrieved_at":"2026-10-05","affects":["valuation"],"status":"ok"},{"id":"major_events#none","axis":"major_events","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"三到四年財務歷史序列","question":"q4_capital","why":"evidence.numbers.financial_history 無資料（yfinance 年度財報抓取失敗或缺此欄），§7 財務歷史表（e9b）缺此塊時印資料缺口，不得由判斷者用其他口徑頂替。","tried":["evidence.numbers.financial_history"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"3017","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3017"},"is_subject":true,"note":"quarterly_income_stmt 無資料"},{"name":"VRT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.04,"operating_margin_pct":19.4,"fcf_margin_pct":25.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ETN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.9,"operating_margin_pct":17.71,"fcf_margin_pct":13.1,"rd_intensity_pct":2.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"3324.TW","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3324.TW"},"note":"quarterly_income_stmt 無資料"},{"name":"2308.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.69,"operating_margin_pct":16.78,"fcf_margin_pct":11.7,"rd_intensity_pct":8.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"3017"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/3017/3017_Q2_2026_Earnings_Call_20260812.md）

# Q2 2026 Earnings Call
**Asia Vital Components Co., Ltd.** | Earnings Calls | 2026-08-12

**Operator** (Operator):
Good afternoon, everyone, and welcome to Asia Vital's Second Quarter 2026 Earnings Conference Call. We are pleased to have with us today, Mr. [ Eric Chen, ] Vice President; Mr. [ Matthew Shen, ] Executive Assistant to CEO; and Mr. Bill Chen, Senior Finance Manager, who will provide an overview of the company's operating results for the second quarter of 2026. [Operator Instructions]
And now I would like to turn the call over to Asia Vital management team.

**Bill Chen** (Executives):
Okay. Thank you. Good afternoon, everyone, and welcome to AVC's 2026 Second Quarter Investor Conference. I will now walk you through our financial and operating performance for the second quarter and the first half of 2026.
Before we begin, please take a moment to review the disclaimer on this slide. Today's presentation is based on information currently available, and the actual results may differ due to various risks and uncertainties.
Second quarter revenue reached TWD 49.1 billion, remaining stable and quarter-over-quarter and increasingly 66% year-over-year. The key point on this slide is gross margin, which improved to 32.57%, up to 2.8 percentage points quarter-over-quarter and 8.16 percentage points year-over-year. This improvement was mainly driven by a more favorable product mix and higher revenue contribution from server applications, demonstrating that revenue growth is translating into better earnings quarterly. Operating margin reached 27.44% and EPS rose to TWD 24.37, up 21% quarter-over-quarter and 137% year-over-year.
And let's quickly walk you through the first half 2026 income statement. And I will skip through the CAGR numbers here. The full presentation will be available on our website after the call for anyone who would like to review the details. Quarterly revenue entered a new growth phase in 2025 and remain at a high level of approximately TWD 49.1 billion in the second quarter of 2026, although revenue was broadly stable sequentially. EPS Increased from TWD 20 to TWD 24, highlighting further improvement in earnings quality.
Full year 2025 revenue reached TWD 139.6 billion, which -- with EPS of TWD 49.70. Both metrics increased substantially compared with prior year, and the earnings grew faster than revenue. And thermal and chassis general combined revenue of TWD 81.9 billion in the first half, accounting for 83.4% of the total revenue and growing 104% year-over-year. Thermal growth, [ 96% ] with chassis increased 134%, making the main driver of product growth. Second quarter thermal revenue remained strong at TWD 30.6 billion. Chassis revenue increased sequentially from TWD 9.9 billion to TWD 10.1 billion. Overall, our core thermal and chassis business remained robust, while system assembly and other products also recovered from the first quarter.
Server and network was the primarily growth driver in the first half. Revenue reached TWD 54.9 billion, up 153% year-over-year, and its share of total revenue increased from 48.4% to 66.1%. The higher server contribution not only support revenue growth but also improves our overall product mix, which was an important factor before the improvement in the gross margin. Looking ahead, as the demand for the high-power computing increase, we expect the liquid cooling application to become more widely adopted, further increase the importance of server-related products in our revenue mix.
Second quarter server revenue reached TWD 32.4 billion, up 113% year-over-year and represent 53% of total revenue. This [ strong ] shift from also an important factor behind the continued improvement in the gross margin. As liquid cooling expand from select high-end platform into a broader range of server application, we believe server-related business will become increasingly important within our overall revenue mix.
And in nonoperating breakdown, second quarter nonoperating income was TWD 457 million, improving significantly from a loss of TWD 40 million in first quarter. The main change was net interest income of TWD 255 million and a shift from an exchange loss of TWD 305 million in Q1 to an exchange gain of TWD 49 million in Q2. First half nonoperating income was 417 million, lower than the same period last year. The main factor was a shift from exchange gain of TWD 759 million to an exchange loss of TWD 256 million. Higher net interest income, partially offset this change.
Now the consolidated balance sheet at the end of June. Cash and cash equivalents reached TWD 77.7 billion, an increase of TWD 9.8 billion from the first quarter, equally attributable to parent also increased 22% to TWD 55.2 billion. Inventory increased 14% sequentially, while accounts receivable declined 17%. And the balance sheet maintained and [ grow liquidity. ]
And the key financial ratio, the current ratio and the quick ratio improved to 126% and 59% (sic) [ 76%, ] respectively, while the debt ratio declined to 68%. Accounts receivable days improved to 20 days. Inventory days increased sequentially to 145 days, mainly because mismatch in the availability of components with different lead times and extend the customer pull in cycle for certain orders. So inventory days remained below 174 days a year later -- a year earlier.
And our cash flow. First half operating cash flow reached TWD 26.3 billion, up 176% year-over-year after capital expenditure of TWD 71 billion. Free cash flow reached TWD 19.2 billion, approximately 3x the level of the prior year period. Strong operating cash flow was the key driver behind the higher end cash balance.
To conclude, AVC delivered significant year-over-year improvement in revenue scale, product and application mix, profitability and the cash flow during the first half of 2026.
This concludes our financial presentation. Thank you, and we will now open the floor for questions. Thank you.

**Operator** (Operator):
[Operator Instructions] We have received several questions in advance. And the first question is 2026 and 2027 CapEx plan and capacity expansion process in Vietnam.

**Unknown Executive** (Executives):
Okay. This is Eric. We have a few questions we take before the meeting. So I will answer those questions first. And if you guys have any other questions, feel free to enter it in monitor or raise your hand to ask. So I will also reply later. Thank you.
So the first question, 2026 and 2027 CapEx plan, also capacity expansion progress in Vietnam. CapEx of this year, 2026 is around [ TWD 18 billion.] For next year, we are still working on the expansion plan to be above this level. And our operating cash flow and existing bank facility as a fit to find an expansion plan already. So we have no financing plan at this time. We will release, of course, if circumstance develop.
As a principle, CapEx is allocated against actual customer project requirement and customer demand where we order, we continue to expand capacity to meet customer demand. Capacity expansion continue across the board. Detailed capacity figures are still being finalized internally. What we can confirm right now is that our new facility has already entered mass production for the next-generation GPU solutions, and we will begin contribution revenue from third quarter of this year.

**Operator** (Operator):
And our next question is liquid cooling penetration rate in ASIC in 2027 and [ rolling ] Ultra Taiwan.

**Unknown Executive** (Executives):
Thank you, Annie. We don't disclose penetration rate or share for a specific customer or specific project information. This is what we cannot share. What we can share right now here is liquid cooling penetration rate in the data center area continue to rise, and we believe it should be passed more than 50% next year. And on the time frame of [indiscernible] and other next-generation product, our approach is very consistent.
We discussed the road map with different clients with every important client, we set priority together and we put the best -- the more resources behind the program that matter most that is the most important one. So client will have the right solution. And when they go mass production, it can make product smoothly. Delivery time and other -- on any project is ultimately driven by client, their own schedule. So what we can do is we follow the schedule, make sure when they go mass production, it's smooth, and we will be one of the major supplier.

**Operator** (Operator):
And the next question is, ASIC demand accelerating enough to offset any future NVIDIA digestion period?

**Unknown Executive** (Executives):
Okay. For AVC, it's not either for GPU for ASIC product. both products need thermal and mechanical solutions, power consumption and rig density while in the stage keep rising on both solutions. So we continue to ship in both solutions, which means either way we benefit from it. ASIC client will be one of the major growth engine for our company in next stage. More broadly, we believe AI is real. What we observe is clients continue to come in more, put more people, put more money, put more resource, continue, continue, continue. The trend is ongoing.

**Unknown Executive** (Executives):
Yes. Thanks, Eric. Here, I'm just going to pitch in and add to the answer. I think the question in itself signifies a slowdown of NVIDIA and/or a slowdown of NVIDIA's growth. As a matter of fact, on our end, we're continuing to see strength both in ASIC and in NVIDIA. And I thought it was important to make that clarification that as Eric has said, we are committed to delivering the best thermal solutions, the best mechanical solutions for the leaders in tech. This was always our mission. That's what we've been doing, and that's what we'll continue to do. And so -- yes, I think it was just important to clarify that we're not particularly seeing a slowdown in NVIDIA. And I'm not unsure what it means by the question by digestion period, but we are continuing to view NVIDIA as an important customer that we are keen to continue to work with.

**Operator** (Operator):
And the next question, can management provide an update on AVC's expected cooling content per rack and supply share for Vera Rubin, Google TPU, V8, AWS [indiscernible]?

**Unknown Executive** (Executives):
Okay. Sorry, again, we are not able to disclose share or content value for an individual customers' individual project. What we can share here is that AVC continue to hold a major supplier share across those programs. And how it's generally a complexity judgment according to your capability and capacity, shipment record, delivery stability, quality, geographic diversity and of course, price, supply chain resilience. So our objective in every program is that we will try to be the customers' main source, one of the main source, and that has been considered through all the projects we cowork with clients. And not to the subsidiary project, but overall, we do see a trend that product penetration rate will keep continue increasing, increasing, increasing the change for sure on this way.

**Operator** (Operator):
And the next question, visibility of demand beyond 2026.

**Unknown Executive** (Executives):
Okay. Thank you. Customers are still adding more and more resource rather than going back, and this is what's in front of our view. Liquid cooling penetration rate in the data center should pass 50% next year. And while liquid cooling module drive most of our visible growth, the CAGR of the chassis rig and other mechanical business is actually comparable. AVC, we always say we are a total thermal and mechanical solution provider.
We are able to design thermal and mechanical part with clients in a system together at the same time. So that has always been our strength and our goal to provide a one-stop shop to all of our major clients, and we will continue to remain this strategy. So overall, the mechanical business should maintain a stable strong growth in the coming quarter and the years along with our thermal product. And our CapEx plan for next year reflects this view that both of mechanical and thermal product will have another phase of capacity plan next year.

**Operator** (Operator):
And the next question, with first quarter gross margin at 29.8%, is a roughly 30% level sustainable as liquid cooling and new capacity ramp?

**Unknown Executive** (Executives):
We don't comment on the margin of any individual product like any product itself. But at the company level, corporate level, our product line going into mass production is about in the second half of this year, which is right now, and we are also bringing more and more automation equipment online, which will help us overall to provide a better gross margin. This is the goal we are aiming to.
On the mechanical side, rising rig density means specification are upgrading with it. The chassis today is not only the simple chassis. The chassis today has to carry liquid cooling module, manifold and fan while still continue meeting structurally their flow and serviceability requirement. All of these requirements will still need to be met in this area. So both design, difficulty and content value per rig are, of course, moving up. Overall, we remain optimistic about the company's outlook.

**Operator** (Operator):
And the next question, how's third quarter margin outlook?

**Unknown Executive** (Executives):
We remain the outlook we have given previously. And -- but of course, we are not guiding a specific gross margin number for this quarter and also next quarter. Direction-wise, the shift into mass production across the board, across all the product portfolio across all the thermal and mechanical products and the contribution -- continuous introduction of the automation equipment should help, should benefit us to make supportive of our margin trend.

**Operator** (Operator):
And the next question, what is the sequential revenue growth outlook for second half 2026?

**Unknown Executive** (Executives):
This is similar with the previous one. We maintain the outlook we have given previously of our product begin entering mass production in the second half this quarter and the next quarter. So second half of 2026 should be better than the first half, and this should be a reasonable expectation. That said, it depends on clients [ pooling ] timing. Overall, our situation is broadly in line with the industry, and we continue to build our company future optimistically.

**Operator** (Operator):
And the next question, the ASIC market share outlook and contribution from switch trade for Vera Rubin, is the company holding a dominant position for switch trade?

**Unknown Executive** (Executives):
Okay. Thank you. Again, we don't -- we are not able to answer specific project and the clients' information. But what we can share is along with GPU market for the ASIC market share, we also have a major market share in ASIC product, including Coplay, including manifold. So this is the first question -- answer for the first question. Secondly, we continue to hold a major supplier position in the switch product. From the generation 1 until now, we are still the major switch solution provider. Thank you.

**Operator** (Operator):
And the next question, ASIC project update and competition.

**Unknown Executive** (Executives):
Again, I can still only answer this question broadly in general. In general, price competition among different ASIC solutions is getting more and more. So we see lots of different new ASIC product launch in different client sites. And AVC continue to be major thermal and mechanical supplier for those ASIC products. And we have high confidence about this product segment as well.

**Operator** (Operator):
And we will now take questions from online participants. [Operator Instructions]
We have a question from [ Tim Stanley ].

**Unknown Analyst** (Analysts):
Congrats on the really nice results. I guess just a direction question or a big picture question of beyond 2026, how should we look at your products in terms of specs and the direction of this sort of the coplay market going forward? Just a big picture and directional sort of view.

**Unknown Executive** (Executives):
Okay. So in general, both GPU, I mean I'm only referring to coplay itself. In general, both GPU and ASIC product design complicity of coplay is getting more and more complicated. So it may be when we say one piece of coplay, it means a chip, and it's really a simple piece of coplay. Now when we say one set of coplay, it may be contained like several pieces coplay and it may contain -- it has lots of different type, maybe 1 to 3, 1 to 4, maybe side and bottom side, both has a coplay. So I mean, in general, the complexity of coplay itself become more and more complicated.
So that's why we are able to provide our key value to start to work with clients in a very early stage to contribute our capability and go through the NPI process and in the end, successfully smoothly go mass production. And during the phase -- during the NPI phase, of course, when the product getting more and more complicated, the [indiscernible] for sure will increase. So this is a general trend we see in both GPU and ASIC market for coplay itself.

**Unknown Executive** (Executives):
Yes. Thanks, Eric. I'm Matthew. And I would just like to add to that answer. I think Eric already gave a very complete answer, but what I'd like to add is when we look at spec in terms of thermal, we really are looking at a multitude of factors. So TDP would be one, weight would be another, form factor is another. System complexity, as Eric mentioned earlier, is another. And all of these have a direct impact on the design complexity of what we deliver to our customers.
Now if we look past the '26 into '27, I suppose already on very many exhibitions such as GTC, such as Computex, you -- our investors and including ourselves would have already gained some insight into the immediate next generation or next 2 generation. Past that point, our thermal is really heavily dictated by what the customer system level solution looks like. And what that means is before our customers have decided what they want, specifically when they want their system, they want their rack, they want their trace to look like, it becomes very difficult for us to share in a nonspeculative manner what we think the future trajectory is.
Now that being said, I think history is always a good feature. And if we look at the previous generations leading up to this moment in time, what we will be -- what we can clearly see is that system complexity has continued to increase. From NVIDIA's HGX platform to their MGX platform, going from 8x -- 8 cards in an HGX tray into 72 GPUs in an MGX system. So that massive step-up in complexity also was what was driving a lot of our growth in the past few quarters.
If we look on the ASIC side, the same story is developing where to meet more complicated system-level solutions where customers are trying to put more components in a tray, trying to put hotter components in a tray, that's then driving a significant architectural change in the tray level design, which then gives us a boost not only in content, but also in margins. We should continue to expect seeing this going forward. Now I understand that was maybe a bit of a nonanswer.
If we look at what we're working on right now and what we are trying and exploring right now with our customers with our future future -- on our future projects, the things that we're investigating right now include changing the tin material, changing the material of the cold plate, controlling for weight, controlling for hotspots on the cold plate, continuing to push for higher TDP, continuing to push for higher flow speeds and also looking into 2-phase liquid cooling.
So all of these directions are potential directions that customers will continue to want further improvements on. And because every system is so different, we are having to look at all of these different aspects, look at these different development trajectories to really make sure that we can continue to stay on top of what our customers' future -- well, current and then future system architectures will look like. So just to add some color there.

**Unknown Analyst** (Analysts):
Yes. Now shifting gears to maybe more of a short-term question. Would you say you are more optimistic in terms of, let's say order demand on some certain projects versus, say, a quarter ago or a couple of months ago?

**Unknown Executive** (Executives):
I will answer this first. And if, Matthew, you have other input, please go ahead later, yes. Like what I mentioned previously, the AI demand is real. The demand is still very strong, and we continue to expand based on our clients' real order, real forecast, and we even received some payment first before our expenditure. So we are still optimistic for the overall AI product trend. And we have high confidence that we will be part of the journey growth with our client  [ LCD ].

**Unknown Executive** (Executives):
Yes. I would just like to add to that. If we're looking at the last few quarters, it always is the case where when we are further away from the delivery, the mass production date, we are more cautious about forecast that our customers give us. And I think Eric mentioned a key point earlier, which is that we have received prepayment on our expansion or received prepayment on the capacity that we are delivering to our customers.
Ultimately, the forecasts have -- well, on select projects have continued to be revised upwards. What really gives us the confidence that this forecast is real, that we can continue to expect strength in AI is customer willingness to pay us beforehand. And at this current moment, many of our customers are willing to do this for us to prepay us for expansion, to prepay us for capacity, to prepay us for building buffer stock and inventory for them. And so as we approach the end of Q3, these are the signals that we are paying more attention to rather than just looking at the forecasted figures, which are historically always prone to change.

**Operator** (Operator):
[Operator Instructions] [indiscernible]

**Unknown Analyst** (Analysts):
I'm wondering whether you can shed some light on the art and the science of setting ASP on products that are going through a significant capacity expansion. So is there any rules of thumb saying, for example, your ASP will go down X percent if capacity go up by Y percent because you can then share a lot of that value with your customers, and that will help you getting further orders because you are very competitive on capacity delivery and the price. So like how do you -- like what's your philosophy of setting that ASP right? Is gross margin a target or goal in doing so? Or is that just an outcome?

**Unknown Executive** (Executives):
Thank you. Overall, I would say it's an outcome is a result. We do not -- there's no methodology or a secret recipe that we can see, okay, I do this percentage of expansion and I can gain how many percent of the ASP. We do not. What we can do in corporate level is -- the only principle is the more complicated product, usually, we can go to more better margin. And when it's a small volume project, we also charge higher margin when it's -- if it's a super big volume, then this is, of course, this is negotiable. But there's no clear cut, no methodology that how many percentage increase on capacity equal to how many percentage of ASP increase. This is my [indiscernible].
Matthew, do you want to add more color on this?

**Unknown Executive** (Executives):
Yes. Thank you, Eric. And thank you, Pam, for the question. It's really one that is difficult to answer directly. And between it being a science and an art, it definitely is more of an art. And the reason it's more of an art is because when we do pitch an ASP or when we do work on a project with our customers, the ASP content is heavily dependent on a multitude of factors. What can be said that is common across all sorts of different thermal solutions, whether it's fan, whether it's chassis, whether it's liquid cooling module is that we, as a company, continue to value a long-term partnership with our customers, right?
So what we are trying to do is to be a long-term solutions partner with our customer. What that means is the ASP price isn't something whereby we just try to insensitively push up our price, we try to exploit market capacity gaps. We are trying to pitch prices at a reasonable amount that means we can cover the 100, 200 engineers that we put in on each project, but also means that we can continue to form a long-standing relationship with our customers to continue to be their main source to -- for our customers to continue to be happy for us to be their main source.
And it definitely is a balance between many things. It's a balance between how many engineers we have to put in. It's a balance between what time to market the customers want, system complexity, how much time -- the time lines that we have to work to as well as some of the other specs that was mentioned earlier, weight, TDP, et cetera. And I suppose what is good for our ASP is always higher spec, higher difficulty and higher complexity products will always be accretive to our ASP and margins, which is actually what we've seen in the past few quarters and also why AI data centers and AI server solutions will continue to drive our margin profile upwards because it is fundamentally a more complex solution than the historical products that we made in laptops, in desktops, et cetera.

**Unknown Analyst** (Analysts):
Okay. That's super helpful. I have 2 more, please, if that's okay. The first one is just that if we think about your supply chain and anything that's really important to delivering the capacity growth that you have planned for, is there anything that particular of concern? Are your supply chain ready? Do you -- or are you still able to recruit and retain the engineering talent that you'd like to have? So that's the first question. And the second question is, I wonder whether you can comment a bit more on growth potential in China AI customers or in that market in general?

**Unknown Executive** (Executives):
Thank you for the question. It's a very good question. So I will answer the first one first. Yes, the question itself is also a good improvement to our overall capability. When we say capability, it's not only a design capability. It's end-to-end, how we can make the product mass production smoothly with certain volume continuously. So for those tools coplay itself, [indiscernible] itself, they are also a module, which contain lots of sub-tier components. So to us, the key principle is, first of all, I need to have the design capability of this module.
Secondly, I want to have an in-house manufacturing capability for those important sub-tier component. Take some example, coplay, 2D is a very important stuff. So that's why we have our subsidiary [indiscernible]. They are -- they have a talent team working on this. Another example is the tube, the host.  A lots of competitors, lots of clients, they think the host is like when you take a shower in your home, that's what it's a normal stuff, but to us, no. It's a very important product that you need to keep it very precise. It cannot have leakage and you need to have a stable, sufficient output.
So alternatively, you can have the whole module shipment smoothly. So we also have the -- so we have those in-house capability -- manufacturing capability for those important components. And then the least is continuous to be reviewed to [indiscernible] still the host itself. In the first generation, when we cowork with clients, almost, I would say, all of the module makers, including AVC, the main capacity is outsourced.
[indiscernible] is normal component starting from the second generation to us. This is very important. So we -- internally, we urge to the management team and we start to establish of our in-house capability. Before we already have the design capability, but then we adopt more manufacture capability. So this is a very good case to help us overall to continue to improve our supply chain company, improve our shipment and also improve our cost structure. And those make us continue outstanding among the competition. This is the first question. And the second one...

**Unknown Executive** (Executives):
Yes. I think the second one was a question on our opportunity in China. But just before we jump to the second question, I'd just like to add to Eric's answer, Pam, which is on talent and talent retention, we are -- there are several things that we're doing. Number one, we understand that talent -- to acquire talent isn't always just to pay the big bucks. We continue to offer the best engineers in the field an opportunity to be working on the most critical projects in all of technology right now. This is an edge that only AVC has. We are participating in absolutely every project that every CSP has, that NVIDIA has, and we're continuing to work on next-generation solutions even for robotics, space or autonomous vehicles.
So I suppose in talent retention, not only do we offer the best opportunity to work on, well, the most exciting projects, we are also setting up new offices, new locations to cater to different potential hires as well as I think probably if we come back to the monetary part, we have about TWD 10 billion of options outstanding at this moment to continue to retain our best talent. And this is what enables us to have an engineering team that's more than 1,800 people to continue to have them build experience with us and continue to contribute their expertise into the most exciting projects.
Now the next question on China, I'll let Eric answer first.

**Unknown Executive** (Executives):
Thanks, Matthew. For China, what we can share right now is since day 1, even before pandemic, AVC was able to join all the major ASIC project with China-based client and the trend is still ongoing. We continue to join those ASIC project development, not only the green product, but also they are still much and many projects there are air cooling, not liquid cooling. So we participate both of land and also for not only coplay itself, but also other products, even [indiscernible], those products, we are also part of that. So we believe we will continue to have a healthy growth in China market.
Matthew? Thank you.

**Unknown Executive** (Executives):
Yes. Thank you, Eric. To add to that answer, we have continued to be long-standing partners with China CSPs even before AI infrastructure or AI ASIC took the spotlight of the tech world. So we are very familiar with China customers. We have continued to form once again, a long-standing partnership relationship with Chinese suppliers. 5 of our 6 manufacturing facilities are in China, which enables us to supply to them relatively flexibly. And the main difference between AVC and Chinese local producers is, number one, we are maybe 5x, 10x the size of our Chinese competitors. And number two, our Chinese competitors don't meet us in terms of the design capability, the architectural solutions design capability that we are able to provide.
Our Chinese competitors are, for the most part, really good competitors in their ability to manufacture, but the ability to design is something that needs to be built up over time. It needs to be built up over working on very many projects. And as such, for Chinese CSPs and Chinese start-ups in AI, we continue to be #1 choice across the board.
Now in terms of our opportunity in China, once again, this is heavily dependent on what our customers want to do in their own ramp. We continue to remain committed to supporting their journey. But the growth trajectory and the forecast and the growth outlook, whether it's this year, next year, '28 is heavily dependent on what our customers' own strategic plans in AI are.

**Operator** (Operator):
Are there any questions from other investors?

**Unknown Analyst** (Analysts):
It's Pam again. I can always have one more if there's nobody else asking.

**Unknown Executive** (Executives):
Sure, go ahead, please.

**Unknown Analyst** (Analysts):
Well, just because you mentioned in the -- when we talk about talent to attract them, you mentioned robotics, space and autonomous. Just out of curiosity to the extent that you could disclose, what would be your involvement or focus in the space?

**Unknown Executive** (Executives):
Okay. Okay. For this part, I can only share very wildly, very roughly. Our client in space area, we do work with a few clients right now. And they are 2 separate business model there. First of all, satellite itself. Secondly, the so-called AI data center on the space. We do work with clients, different clients in both area and some of clients, they have -- they are under one big umbrella. So we work with the -- maybe the [ BUA ] in the past. Now we were able -- we are able to work with their [indiscernible] together because in the end, it is a technology. It's a product. So we have a very good track record.
We have a long history co-working with clients in many products, many fields. So when clients jump from A to B to C, AVC can help them cowork with them to work on the journey and in the end, make to the product that they want and follow the regulation. Take an example, [indiscernible], take some example the requirement they have either human itself, either location, either on product, we can always pull in. So they feel comfortable to work with us.
Matthew you want to add more?

**Unknown Executive** (Executives):
I don't have much to add, but that I suppose what does excite us is the space piece because, well, it's going to space is objectively a very interesting segment. And as Eric mentioned, we continue to support our customers. We continue to leverage our long-term relationship with the leaders in tech to enable ourselves to continue to be #1 in any tech generation. Maybe 5 years down the line, there's -- we're going to Mars or 10 years down the line, we're going to Pluto. We have full confidence that in any tech iteration, in any solution iteration, we continue to be our customers' #1 choice.
Well, just to clarify, like going to Mars and Pluto is not currently in our pipeline. But just as I mentioned to say, we are committed to that long-term trajectory rather than just trying to win project by project.

**Unknown Analyst** (Analysts):
Okay. That's super helpful. And I know it's a tricky question. But I'm also more thinking about like what would be the cooling method in the space, if not conduction convection. So I'm just wondering, is there anything on the sort of science breakthrough front that you might be able to share? Or I'm also happy to wait and see when you move to product?

**Unknown Executive** (Executives):
Very high level speaking. It's very advanced version, super improved version of existing product, existing technology. It's also conduction, it's also convection, it's also kind of evaporation. Those technologies are all in review, are all in discussion. But in the end, it's just a more advanced version of existing product.

**Unknown Executive** (Executives):
Yes. I think to add tohat in space, our conduction, our convection, our evaporation can only happen in combined components. Ultimately, to expel the heat into space, we would have to rely on radiative cooling, which is the same way that the heat from the sun gets to the earth. This is less effective and more unavailable compared to, say, air cooling on earth. But this is exactly why we need to continue to work on finding the best way to run it, not only to dispel the heat, but also to run it in a way that enables reliability because we're not able -- once something is sent into space, there's no serviceability. There's no way to fix it if something goes wrong. So we are pushing our boundaries in multiple directions, not just in how do we excel the heat, but also how do we make something that can be in space that can last the lifetime of the space data center. And these requirements are higher, significantly higher than what we would expect on earth.

**Operator** (Operator):
And are there other questions? And if there are no further questions, let's end today's call. And thank you all for joining us today, and thank you, Eric, Matthew and Bill, for your time and insight. Have a good day. Bye-bye.

**Unknown Executive** (Executives):
All right. Thanks, everyone, and thanks, Pam. Thanks, Timson, for the questions, and everyone else who submitted early. See you in the next quarter.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

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
{"date":"20260711","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"奇鋐維持 4 大 CSP 冷板 40-50% 份額，Rubin／Rubin Ultra 世代不被雙鴻搶走 &gt;5pp","columns":{"2Y 驗證點":"GB300 量產後份額 ≥ 40%","5Y 驗證點":"Rubin 世代仍主供 ≥ 3 家 CSP","10Y 驗證點":"FY35 營收 ≥ 6,000 億","具體數字門檻":"份額 floor 35%；雙鴻 ceiling 25%；月營收 YoY floor +30%","信息來源":"NVIDIA GB300 供應商認定（鉅亨 2026-02）；公司法說 2026-05-14；ID_LiquidCooling（AVC 40-50% 份額）","漂移觸發":"連 2 季 TTM 月營收 YoY &lt; +30% → 削弱；連 4 季 → 削弱升級"}},{"id":"H2","text":"富世達 UQD／分歧管領先性維持，每代機櫃快接頭數量上升推升 ASP 與 mix（信心：中——媒體多把奇鋐/雙鴻/富世達並列受惠鏈，「獨家」缺強佐證，改述為「領先」）","columns":{"2Y 驗證點":"富世達營收 YoY +40%＋，UQD Rubin 放量（出貨規劃 150-200 萬件→300 萬件）","5Y 驗證點":"競爭者 UQD 份額 ≤ 30%","10Y 驗證點":"子公司估值貢獻 ≥ 母公司市值 25%","具體數字門檻":"富世達 6805 月營收 YoY floor +30%；快接頭數量 GB200 ~54/櫃 → Rubin 100+","信息來源":"富世達已通過 NVIDIA UQD 認證（2025-12）；富世達 H1 2026 營收 +62.6%；公司持股 16.87%（財報 2025）","漂移觸發":"連 2 季富世達月營收 YoY &lt; +30% 且競爭者取得 CSP UQD 認證 → 削弱"}},{"id":"H3","text":"毛利率自 25.8%(FY25) 維持在 28-30% 區間，不因冷板大宗化回落","columns":{"2Y 驗證點":"GP% 站穩 28-30%（Q1 26 已 29.77%）","5Y 驗證點":"GP% 維持 28-30%（液冷比重 &gt; 50%）","10Y 驗證點":"穩定 27-30%，領先雙鴻 3-5pp","具體數字門檻":"GP% floor 26%（連 2 季跌破警戒）；液冷/熱管理比重 floor 60%（Q1 26 已 63.6%）","信息來源":"Q1 2026 法說（GP% 29.77%）；FY2025 年報（GP% 25.8%）","漂移觸發":"連 2 季 GP% YoY 下滑 ≥ 1.5pp→ 削弱；連 4 季 → 推翻"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"雙鴻於 Rubin 冷板／CDU 大幅搶單","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"4 大 CSP 冷板訂單分佈；雙鴻月營收 YoY vs 奇鋐差距；雙鴻「整合方案」CSP 導入進度（非僅冷板份額）","警戒閾值":"連 4 季雙鴻營收 YoY 高於奇鋐 ≥ 10pp；或雙鴻於 Rubin 取得 ≥ 30% 份額；或雙鴻整合方案打入 ≥ 3 家 CSP 主供"}},{"id":"R1b","text":"健策 MCL 封裝層級散熱侵蝕冷板 TAM（架構替代，非份額競爭）——MCL 獲 NVIDIA 驗證、預期 2H26 Rubin 雙晶片導入、2027 主流化，若把散熱價值鏈上移到封裝層，奇鋐「機櫃冷板模組」TAM 本身縮小","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Rubin+1/Fowler 世代 MCL 滲透率；奇鋐 DB/MLCP 防禦技術認證進度；沈慶行後續法說對 MCL 表態","警戒閾值":"MCL 於 Rubin 世代主流機種滲透 ≥ 30%（媒體/NVIDIA 確認），且奇鋐 DB 防禦未取得對應認證 → §7 護城河 −2、H1 重評"}},{"id":"R2","text":"冷板大宗化＋AI capex 消化期 → 量價齊挫、GP% 回落、EPS 共識下修＋倍數壓縮（股價漂移警示）","columns":{"對應假設":"H3 / 估值","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季 GP% YoY；月營收 YoY；hyperscaler capex guidance；Fwd PE 5Y 分位","警戒閾值":"GP% 連 2 季 YoY −1.5pp 且月營收 YoY 連 2 月 &lt; +30%（兩者同時觸發，過濾單季噪音）"}},{"id":"R3","text":"capex 過度擴張（2026 150 億、2027 170 億）遇需求放緩 → 稼動率崩、ROIC 自 26% 滑落＋越南 ramp 不順","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"年度 capex/Rev 比；ROIC 年度趨勢；越南廠稼動率（法說揭露）","警戒閾值":"連 2 季 capex/Rev &gt; 12% 且 ROIC 年度 YoY −5pp；需連 2 年偏離（長變數漂移分級）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼＝回踩 2,100（W52 附近）或 Rubin Ultra MCCP 認證／富世達 UQD ASP 上修；減碼＝雙鴻於 Rubin 冷板取得 ≥30% 份額或 GP% 連 2 季 YoY −1.5pp","irr_base_pct":9.4,"ev5y_pct":61.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"A","val":"🟢","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.2,"ev5y_pct":61.0,"irr_base_pct":9.4,"max_dd_pct":-55.0,"bull_5y_price":5770,"bear_5y_price":1560,"p_bull_pct":30,"p_bear_pct":25,"rearm_trigger":"加碼＝回踩 2,100（W52 附近）或 Rubin Ultra MCCP 認證／富世達 UQD ASP 上修；減碼＝雙鴻於 Rubin 冷板取得 ≥30% 份額或 GP% 連 2 季 YoY −1.5pp","price_at_dd":2350,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3017_20261005/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
