你是 stock-analyst **v20 判斷 agent**，標的 MOD（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MOD","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":994.4,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 2026-11-03 轉載）；YoY 由新聞稿 $738.9M 計算"},"note":"未取得"},{"id":"f_kpi1_gaap","label":"毛利率（GAAP）","value":20.7,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿；法說會 CFO：三個部門毛利率皆下降，主因材料成本通膨"},"note":"未取得"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":97.8,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","unit":"USD M（利益率約 9.8%，由 97.8÷994.4 計算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 轉載）"},"note":"未取得"},{"id":"f_kpi3_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA／利益率（公司不揭露 Non-GAAP 營業利益，以 Adjusted EBITDA 為準）","value":136.2,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","unit":"USD M（利益率 13.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿；利益率 13.7% 見法說會 CFO 說明"},"note":"未取得；管理層自承實際利益率低於自身預期"},{"id":"f_kpi4_adjusted_eps_gaap_eps","label":"Adjusted EPS／GAAP EPS","value":1.35,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","unit":"USD（Adjusted）；GAAP 0.56","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿；Adjusted EPS 排除與分拆相關的法人重組所得稅費用 $29.5M"},"note":"未取得"},{"id":"f_kpi7_fy2027_performance_techn","label":"管理層全年指引（FY2027，已剔除 Performance Technologies）","value":"營收 $3.1–3.2B（+50–55%）；Adjusted EBITDA $470–500M（成長逾 50%）","period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿與法說會 CFO 準備稿；資料中心營收 +80–90%、商用空調 +10–15%（兩者皆較上季上調）；FY27 資本支出指引 $150–200M；全年 FCF 預期為正"},"note":"yfinance 共識營收 FY1 $3,283M（8 位分析師，見 capital_structure；與指引口徑可能不同，未剔除 PT 與否待確認）"},{"id":"f_kpi8_backlog_book_to_bill","label":"訂單／積壓訂單（backlog）與 book-to-bill","value":">1000 訂單；book-to-bill >2","period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03；法說會 2026-11-04）","unit":"USD M（資料中心季度新訂單，史上首次逾 $10 億）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03；法說會 2026-11-04）","citation":"法說會 CEO（連四季創紀錄訂單）與分析師問答中 book-to-bill 大於 2 的確認；backlog 金額公司未揭露，僅稱歷史新高；另獲超大型雲端客戶新案，2027 日曆年前供應逾 $400M 客製化空氣處理機組"},"note":"不適用"},{"id":"f_kpi9","label":"產能利用／擴產進度（冰水機產線）","value":13,"period":"Q2 FY2027（法說會 2026-11-04）","unit":"條運轉中，目標 FY 年底 20 條","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q2 FY2027（法說會 2026-11-04）","citation":"法說會 CEO；公司未揭露利用率百分比"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-03","period":"2026-11-03","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mod_gross_margin_pct","label":"MOD 毛利率","value":21.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MOD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mod_operating_margin_pct","label":"MOD 營業利益率","value":10.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MOD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mod_fcf_margin_pct","label":"MOD FCF 利潤率","value":-0.27,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MOD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_gross_margin_pct","label":"VRT 毛利率","value":38.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_operating_margin_pct","label":"VRT 營業利益率","value":20.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_fcf_margin_pct","label":"VRT FCF 利潤率","value":23.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aaon_gross_margin_pct","label":"AAON 毛利率","value":25.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAON.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aaon_operating_margin_pct","label":"AAON 營業利益率","value":11.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAON.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aaon_fcf_margin_pct","label":"AAON FCF 利潤率","value":-6.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAON.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_gross_margin_pct","label":"TT 毛利率","value":34.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_operating_margin_pct","label":"TT 營業利益率","value":17.92,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_fcf_margin_pct","label":"TT FCF 利潤率","value":16.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_gross_margin_pct","label":"JCI 毛利率","value":36.71,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_operating_margin_pct","label":"JCI 營業利益率","value":14.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_fcf_margin_pct","label":"JCI FCF 利潤率","value":12.03,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_fcf","label":"自由現金流（FCF）","value":-140.6,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","citation":"yfinance quarterly_cashflow（營運現金流 −98.5、資本支出 −42.1；同表 Q1 FCF −5.0 與公司 Q1 新聞稿一致）；定性說明見法說會：營運資金、資料中心投資、分拆費用 $27.7M 現金支付、較高現金稅。Q2 新聞稿原文的現金流表本次未能取得，數字待對 10-Q 複核"},"note":"不適用"},{"id":"f_kpi6_sbc","label":"SBC 占營業利益","value":4.8,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","unit":"%（SBC $4.7M ÷ GAAP 營業利益 $97.8M；占營收約 0.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）","citation":"yfinance quarterly_cashflow Stock Based Compensation 4.7M；營業利益見新聞稿。數字偏低，待對 10-Q 複核"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":96.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-64.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":24.78,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.1 → 5.1）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.61 → 9.61）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.96 → 11.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.1,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.61,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":11.96,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-33.25,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 7.64 → 5.1（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":40.42,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝37.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":37.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.42,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝29.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":29.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝31.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":31.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":18.94,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 5.1，分子＝快照價 96.61","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":716.4,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 867.0、現金 150.6（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":53.2,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":5855.75,"period":"2026-11-08","unit":"USD m","basis":"市值 5139.35 ＋ 淨負債 716.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":3283.29,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（8 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":4292.14,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（8 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.78,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 96.61 / W52 199.98 / W104 157.24 / W250 93.25 / W250 13週斜率 2.05%"},{"id":"f_ma_w52","label":"52 週均線","value":199.98,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":157.24,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":93.25,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.05,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 稱公司與眾多熱傳／HVAC&R 製造商競爭，供應鏈整併與垂直整合可能帶來新的或重組後的競爭者；並面對位於低勞動成本、低稅率地區的公司競爭。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"In addition, consolidation within the supply base and vertical integration may introduce new or restructured competitors to our markets.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：若新產品／專案未能及時推出，可能流失市占或損害客戶關係；技術落後會導致價格侵蝕。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"If we do not successfully or timely launch new products, systems and programs, we may lose market share or damage relationships with our customers, which could negatively affect our business and results of operations.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K 顯示資料中心占淨銷售由 FY2025 的 25% 升至 FY2026 的 35%，傳統車用／重型設備占比下降（結構消長，非直接市占數據）。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"Data Centers 35 % 25 % Heat Transfer Solutions 18 % 21 % HVAC Technologies 11 % 10 % On-Highway Applications 23 % 28 % Heavy-Duty Equipment 13 % 16 %","as_of":"2026-05-27","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"報導稱 Modine 與 Vertiv、Johnson Controls 等較大對手在 AI 資料中心冷卻競爭；FY2026 資料中心營收 $1.1B、年增 73%。","source":"Nasdaq/Zacks: How Modine is Positioning Itself to Benefit From the AI Push","url":"https://www.nasdaq.com/articles/how-modine-positioning-itself-benefit-ai-push","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Modine 取得約 $4B 超大規模客戶資料中心冷卻協議（2027–2029，$165M 預付），僅單一二手來源。","source":"Pulse: Modine Shares Jump Over 20% After $4B Data Center Cooling Deal","url":"https://www.pulse.bot/cro-pulse/news/modine-shares-jump-over-20-after-4-b-data-center-cooling-deal-with-hyperscaler-2dd79ec3-0a19-4beb-bfeb-871641ac491a/","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K FY2026：前十大客戶占淨銷售 49%，氣候解決方案部門有一家全球科技客戶約占 11%；FY2025、FY2024 最大客戶皆低於 10%。10-K 此處未提及該客戶導入第二供應商或自製。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"In fiscal 2026, one global technology customer in our Climate Solutions segment accounted for approximately 11 percent of our sales. In fiscal 2025 and 2024, our largest customer accounted for less than 10 percent of our net sales.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"Modine 與未具名策略客戶簽 40 億美元以上資料中心散熱長期產能協議，客戶預付 1.65 億美元（客戶身分為第三方推測，未經公司證實）","source":"Modine 8-K FY2026 Ex.99.2","url":"https://www.sec.gov/Archives/edgar/data/0000067347/000110465926066291/mod-20260526xex99d2.htm","excerpt":"– Announced plan to spin-off Performance Technologies – Reached a landmark multi-year capacity agreement with a key strategic data center customer to supply more than $4 billion of cooling products during calendar years 2027 through 2029 (In millions) $2,583.5 $3,181.1 $392.1 $471.0 15.2% 14.8% * See appendix for the full GAAP","as_of":"2026-05-26","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 前十大客戶占淨銷售 49%（FY2025 43%、FY2024 40%）；Climate Solutions 一家全球科技客戶約占 11%，FY2025、FY2024 無單一客戶超過 10%。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"Our ten largest customers, some of which are conglomerates or otherwise affiliated with one another, accounted for 49 percent of our consolidated net sales in fiscal 2026. In fiscal 2026, one global technology customer in our Climate Solutions segment accounted for approximately 11 percent of our sales.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2026-03-31 應收帳款 53% 來自前十大客戶（前一年 43%）；公司通常不要求擔保或預付款，未發生重大信用損失。","source":"SEC EDGAR 10-K FY2026 Note 20","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"At March 31, 2026 and 2025, 53 percent and 43 percent, respectively, of the Company’s trade accounts receivable were due from the Company’s top ten customers. These customers operate primarily in the data center, commercial vehicle, off-highway, commercial air conditioning and refrigeration, and automotive and light vehicle markets. The Company generally does not require collateral or advanced payments from its customers. The Company has not experienced significant credit losses to customers in the markets served.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"風險因素揭露：資料中心、Gensets 等領域大部分銷售來自少數客戶，失去主要客戶或訂單量顯著下滑會對業績與現金流造成不利影響。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"In certain areas of our businesses, including data centers, Gensets, and some portions of our vehicular businesses, a large portion of sales are attributable to a relatively small number of customers.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 稱預期 2027–2029 年對單一資料中心客戶銷售逾 40 億美元但無購買保證（搜尋摘要轉述）。","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000067347/000110465926066795/mod-20260331x10k.htm","excerpt":"capacity agreement with one of our strategic data center customers, with whom we are party to a confidentiality agreement. In connection with this capacity agreement, we received a $165 million up-front deposit from the customer to support investments necessary to meet the planned sales volume. We expect to sell more than $4 billion of data center cooling products to this customer","as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Modine 保證 2027–2029 日曆年供應逾 $4B 資料中心冷卻產品；FY2027 資料中心銷售成長指引 60–80%；冷卻機產能 FY2027 底前倍增；FY26 資料中心銷售 +73% 至 $1.1B","source":"Barchart/Nasdaq: Modine Manufacturing Q4 earnings call highlights","url":"https://www.nasdaq.com/articles/modine-manufacturing-q4-earnings-call-highlights","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Jefferies：資料中心需求大於供給，屬結構性短缺並持續數年","source":"Tribune India: AI-driven data centre demand far outstrips supply despite record hyperscaler spending - Jefferies","url":"https://www.tribuneindia.com/news/business/ai-driven-data-centre-demand-far-outstrips-supply-despite-record-hyperscaler-spending-jefferies/","excerpt":"record hyperscaler spending: Jefferies AI-driven data centre demand far outstrips supply despite record hyperscaler spending: Jefferies ANI Updated At : 11:49 AM Jun 08, 2026 IST Follow us Connect with us Advertisement New Delhi [India], June 8 (ANI): Global demand for data centres continues to significantly outpace available supply, creating a structural shortage that is expected to persist","as_of":"2026-06-08","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Motley Fool：部分分析師警告 2026 下半年至 2027 資料中心電力與冷卻產能可能過剩；論點繫於超大規模業者 capex 放緩，文中亦反駁（機櫃密度上升）","source":"Motley Fool: AI data center stock buy oversupply VRT","url":"https://fool.com/investing/2026/05/22/ai-data-center-stock-buy-oversupply-vrt/","excerpt":null,"as_of":"2026-05-22","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Dell'Oro：資料中心年度容量新增 2026 見頂後仍維持兩位數成長至 2030，熱管理為成長最快區塊；設備交期仍受限","source":"Dell'Oro Group: data center physical infrastructure market forecast to reach $120 billion by 2030","url":"https://www.delloro.com/news/data-center-physical-infrastructure-market-forecast-to-reach-120-billion-by-2030/","excerpt":"peak in year-over-year growth terms in 2026 and moderate steadily thereafter, remaining in double-digit growth territory through 2030. The market is still expanding quickly, but no longer accelerating. North America leads capacity additions over the period, followed by China. Thermal Management Leads Segment Growth: Thermal Management remains the fastest-growing DCPI segment, with liquid","as_of":"2026-08-19","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 10-K 風險因子：公司明列貿易政策／關稅變動可能衝擊供應鏈、成本與需求；2026年2月最高法院裁定2025年IEEPA關稅無效，但其他關稅仍有效，退款時程與新關稅不確定。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"In February 2026, the U.S. Supreme Court ruled that tariffs imposed in 2025 under the International Emergency Economic Powers Act were invalid (the “IEEPA Ruling”). However, other tariffs remain in effect and trade policies are unpredictable.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：製造據點或原料來源涉及墨西哥、中國、加拿大，進口限制或關稅可能重大衝擊；墨西哥廠在IMMEX計畫下享減稅，該計畫變動為風險。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"Certain of our current manufacturing facilities in Mexico operate under the Mexican Maquiladora (IMMEX) program, which provides for reduced tariffs and eased import regulations. We could be adversely affected by changes in the IMMEX program or our failure to comply with its requirements.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 Performance Technologies 銷貨成本中原料成本增加$10百萬，含關稅影響，銷貨成本率升170bp至81.9%。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"These drivers, which decreased cost of sales, were partially offset by higher raw material costs, which increased $10 million and included the impact of tariffs","as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K：公司稱無中東、烏克蘭、俄羅斯製造，亦無與伊朗等重大業務關係；制裁擴及其營運所在國（中國、德國、塞爾維亞）的部分公司，持續監控合規。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"We do not have manufacturing operations in the Middle East, Ukraine, or Russia, nor any significant business relationships in or associated with Iran, Ukraine or Russia, however we are continuing to monitor the sanctions requirements and reacting as necessary to ensure compliance.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K：資料中心產品所需部分零組件需求超過供應商產能，短缺自FY2026第四季開始，抑制資料中心產品擴產；公司正在認證新供應商。","source":"Modine 10-K FY2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0000067347/000110465926066795/mod-20260331x10k.htm","excerpt":"demand for certain components that we purchase to manufacture our data center products is currently outpacing supplier capacity","as_of":"2026-05-20","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"財報電話會議：不到10%的年度供應鏈支出受關稅影響；氣候解決方案部門有墨西哥與加拿大曝險，多數銷售可轉嫁關稅；Performance Technologies 在墨西哥有製造廠。","source":"Modine earnings call (via search summary)","url":"https://www.facilitiesdive.com/news/modine-earnings-data-centers-indoor-air-quality-hvac-systems/739513/","excerpt":"less than 10% of Modine's annual supply chain spend is subject to the proposed tariffs","as_of":"2025-02-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2025年投資人簡報：美國供應來源中國占比低於10%，公司持續降低對中國依賴；截至2025-03-31有41座製造廠（美洲18、歐洲15、亞洲8）。","source":"Modine 8-K Ex.99.2 (2025-05-20) / 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/67347/000155837025008029/tmb-20250520xex99d2.htm","excerpt":null,"as_of":"2025-05-20","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"最新10-Q（截至2026-09-30）列出美伊衝突、中東軍事衝突擴大、俄烏衝突、制裁與運費中斷為風險，可能推升能源燃料價格、延誤運輸、提高運費與製造成本。","source":"Modine 10-Q period ended 2026-09-30 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0000067347/000110465926122523/mod-20260930x10q.htm","excerpt":"conflict between the U.S. and Iran, broadening military conflicts in the Middle East and ongoing conflict between Russia and Ukraine","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 Climate Solutions 營收全年 +43%（含併購），有機 +32%；資料中心銷售約 $11 億、+73%，Q4 逾 $4 億；Performance Technologies Q4 營收 $294M vs 去年 $294.8M（持平，固定式發電需求降、車用/商用車/越野升）","source":"Nasdaq/Barchart: Modine Manufacturing Q4 earnings call highlights","url":"https://www.nasdaq.com/articles/modine-manufacturing-q4-earnings-call-highlights","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2027 指引：總營收成長 20%–35%，資料中心 +60%–80%，商用 HVAC +5%–10%，Performance Technologies 持平至 +5%；FY2027 起改報資料中心、商用 HVAC、Performance Technologies 三部門","source":"Nasdaq/Barchart: Modine Manufacturing Q4 earnings call highlights","url":"https://www.nasdaq.com/articles/modine-manufacturing-q4-earnings-call-highlights","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"連續第三季訂單創高、backlog 再大增；簽 2027–2029 日曆年逾 $40 億資料中心冷卻產品供應協議，收 $165M 預付款擴產；冰水機產能 FY2027 底前倍增；Q4 毛利率年減 320bp 至 22.5%","source":"Zacks/Nasdaq: Modine Q4 Earnings Beat Estimates on Data Center Demand","url":"https://www.nasdaq.com/articles/modine-q4-earnings-beat-estimates-data-center-demand","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 稱 HVAC&R 主要市場趨勢含冷媒替代與能效法規，預期有利商用 HVAC&R；資料中心市場 FY2026 異常強勁、預期 FY2027 續強。一手文件未將替代技術列為威脅。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"Trends influencing our primary HVAC&R markets include refrigerant substitution and energy efficiency requirements, both of which are expected to benefit the commercial HVAC&R markets.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Modine 收購 TMGcore 浸沒式冷卻 IP／資產，納入單相與兩相浸沒技術（對液冷／浸沒替代路徑的因應）","source":"Cooling Post — Modine invests in liquid immersion cooling","url":"https://www.coolingpost.com/world-news/modine-invests-in-liquid-immersion-cooling/","excerpt":"Home | World News | Modine invests in liquid immersion cooling Modine invests in liquid immersion cooling 3rd January 2024 USA: Thermal management company Modine has purchased the intellectual property and other specific assets of TMGcore, a Texas-based specialist in liquid immersion cooling technology for data centres.","as_of":"2024-01-03","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K 描述的客戶與通路仍為 OEM、批發商、經銷商、承包商與終端用戶並存，未見訂閱化／D2C／平台化等結構性商業模式轉變的描述；資料中心為新增成長客群。","source":"SEC EDGAR 10-K FY2026 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"Customers for these coolers and refrigeration products primarily include wholesalers, distributors and resellers, commercial and industrial OEMs, as well as contractors and end users in a variety of commercial and industrial applications","as_of":"2026-05-27","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Modine 北美暖通銷售主管稱產品全經經銷商、不直銷（暖通部門通路仍為經銷商模式）","source":"HVACR Trends, Modine market outlook 2026 (Richard Boothman)","url":"https://hvacrtrends.com/modine-market-outlook-2026-richard-boothman/","excerpt":"The rep, the distributor, and the contractor all play a role. Training gives us a meaningful way to add value without bypassing the channel. How do you balance that without going around the distributor? Everything runs through the distributor. They host the training and invite their contractors. We do not sell direct.","as_of":"2025-12-19","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat：FQ1'27調整後EPS $1.53高於共識$1.27；營收$874.1M略低於預期；FY2027營收指引$3.8–4.3B，中點略低於約$4.1B共識，未給明確EPS指引。","source":"MarketBeat, Modine Manufacturing given consensus recommendation of Moderate Buy","url":"https://www.marketbeat.com/instant-alerts/modine-manufacturing-company-nysemod-given-consensus-recommendation-of-moderate-buy-by-analysts-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga：9位分析師共識Buy，平均目標價$265；KeyBanc Overweight目標$280（9/2）；B. Riley 7/30目標價由$340降至$305。另一頁列12位、均值$263、高$355、低$73。","source":"Benzinga MOD price targets","url":"https://www.benzinga.com/quote/MOD/price-targets","excerpt":null,"as_of":"2026-09-02","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"各聚合站目標價分布不一：Investing.com均值$310.29（8 Buy）；MarketBeat(5月底)$298.14；TickFlow(8/1)$358.17；MarketBeat(7/30)$314.29。","source":"Investing.com / MarketBeat / TickFlow","url":"https://www.investing.com/equities/modine-manufacturing-comp-consensus-estimates","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Chartmill：FY2027 EPS共識$7.34（12位分析師，10/17記錄），次季EPS共識一個月降約5%、三個月降約7%；Q2 FY27預期EPS $1.47、營收$946.95M。","source":"Chartmill MOD estimates","url":"https://www.chartmill.com/stock/quote/MOD/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"7月Q1財報重申FY2027指引（營收+20%~35%、$3.82–4.29B；調整後EBITDA $650–680M）；性能科技出售完成後將更新持續營運展望；後續8-K有營收展望上調且排除Performance Technologies（日期與數字未確認）。","source":"Barchart / SEC 8-K (Modine Q1 FY2027)","url":"https://www.barchart.com/story/news/3534334/modine-reports-first-quarter-fiscal-2027-results","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"SEC 8-K 顯示營收展望上調並排除Performance Technologies","source":"SEC EDGAR 8-K ex99.2","url":"https://www.sec.gov/Archives/edgar/data/0000067347/000110465926122032/mod-ex99d2.htm","excerpt":"Fiscal 2027 Outlook Excluding Performance Technologies Business Metrics Guidance Comments Net Sales $3.1B to $3.2B +50% to +55% Adjusted EBITDA* $470M to $500M Growth in excess of 50% FY27 Segment Sales Outlook Data Centers +80% to +90% Commercial HVAC","as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-01-29 Modine 與 Gentherm 簽約，以 Reverse Morris Trust 合併 Performance Technologies 事業；Modine 收 2.1 億美元現金，股東持有合併後 Gentherm 約 40%。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926008087/mod-20260129x8k.htm","excerpt":"the Company's Performance Technologies business (the \"Performance Technologies Business\") will be combined with Gentherm in a Reverse Morris Trust transaction. As a result of the transaction, the Company will receive $210 million in cash, subject to adjustment as described below, and the Company's shareholders will own approximately 40% of the outstanding Gentherm common stock following the transaction","as_of":"2026-01-29","retrieved_at":"20261108","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-01 交易完成：Modine 處分 Performance Technologies 部門，收到現金分配，股東取得 Gentherm 股票。","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926112870/tm2626618d1_8k.htm","excerpt":"On the Closing Date, the Company completed the disposition of the Performance Technologies Business, which constituted the Company's Performance Technologies reportable segment, through the Separation, the Distribution and the Merger.","as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"CPSC 於 2026-08-20 公告 Modine 旗下 Airedale ClassMate／SchoolMate 熱泵通風風扇因火災風險自願召回，美國約 6,061 台、加拿大約 735 台，11 起起火、財損至少 270 萬美元，無傷亡。","source":"CPSC 召回公告","url":"https://www.cpsc.gov/Recalls/2026/Modine-Manufacturing-Company-Recalls-Airedale-Heating-and-Cooling-Ventilation-Fans-Due-to-Fire-Hazard","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"10-K（FY2026）：其他訴訟預期不致對財務狀況造成重大不利影響；搜尋未見證券集體訴訟或 SEC 調查。","source":"SEC EDGAR 10-K FY2026 Note（Other litigation）","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm","excerpt":"The Company believes that any additional loss in excess of amounts already accrued would not have a material effect on the Company's consolidated balance sheet, results of operations, and cash flows.","as_of":"2026-05-27","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-01 Performance Technologies 與 Gentherm 的 RMT 交易完成；Modine 收現金分配，股東取得 Gentherm 股票。","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/67347/000110465926112870/tm2626618d1_8k.htm","excerpt":"On the Closing Date, the Company completed the disposition of the Performance Technologies Business, which constituted the Company's Performance Technologies reportable segment, through the Separation, the Distribution and the Merger.","as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"CPSC 於 2026-08-20 公告 Airedale ClassMate／SchoolMate 熱泵風扇火災風險自願召回，美國約 6,061 台，11 起起火、財損至少 270 萬美元。","source":"CPSC 召回公告","url":"https://www.cpsc.gov/Recalls/2026/Modine-Manufacturing-Company-Recalls-Airedale-Heating-and-Cooling-Ventilation-Fans-Due-to-Fire-Hazard","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"MOD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.73,"operating_margin_pct":10.73,"fcf_margin_pct":-0.27,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MOD","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"VRT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.12,"operating_margin_pct":20.35,"fcf_margin_pct":23.74,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AAON","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.57,"operating_margin_pct":11.13,"fcf_margin_pct":-6.8,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAON","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.99,"operating_margin_pct":17.92,"fcf_margin_pct":16.43,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"JCI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.71,"operating_margin_pct":14.99,"fcf_margin_pct":12.03,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MOD"},"financial_history":{"ticker":"MOD","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-03-31","revenue":2297900000.0,"revenue_yoy_pct":null,"gross_margin_pct":16.95,"operating_margin_pct":6.76,"net_income":153100000.0,"diluted_eps":2.9,"free_cash_flow":56800000.0,"fcf_margin_pct":2.47,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-03-31","revenue":2407800000.0,"revenue_yoy_pct":4.78,"gross_margin_pct":21.83,"operating_margin_pct":10.45,"net_income":161500000.0,"diluted_eps":3.03,"free_cash_flow":126900000.0,"fcf_margin_pct":5.27,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-03-31","revenue":2583500000.0,"revenue_yoy_pct":7.3,"gross_margin_pct":24.92,"operating_margin_pct":12.07,"net_income":184000000.0,"diluted_eps":3.42,"free_cash_flow":129300000.0,"fcf_margin_pct":5.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-03-31","revenue":3181100000.0,"revenue_yoy_pct":23.13,"gross_margin_pct":22.98,"operating_margin_pct":11.66,"net_income":121500000.0,"diluted_eps":2.26,"free_cash_flow":105400000.0,"fcf_margin_pct":3.31,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MOD/MOD_Q2_2027_Earnings_Call_20261104.md）

# Q2 2027 Earnings Call
**Modine Manufacturing Company** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Good morning, ladies and gentlemen, and welcome to Modine's Second Quarter Fiscal 2027 Earnings Conference Call. [Operator Instructions] As a reminder, this conference is being recorded. I would now like to turn the conference over to your host, Kathy Powers, Vice President, Treasurer and Investor Relations.

**Kathy Powers** (Executives):
Hello, and good morning. Welcome to our conference call to discuss Modine's second quarter fiscal 2027 results. I'm joined by Neil Brinker, our President and Chief Executive Officer; and Mick Lucareli, our Executive Vice President and Chief Financial Officer. The slides that we'll be using with today's presentation are available on the Investor Relations section of our website, modine.com. 
On Slide 3 of that deck is our notice regarding forward-looking statements. This call will contain forward-looking statements as outlined in our earnings release as well as with our company's filings with the Securities and Exchange Commission. With that, I'm going to turn the call over to Neil.

**Neil Brinker** (Executives):
Thank you, Kathy, and good morning, everyone. This morning, I'm going to start out with the segment updates and then turn it over to Mick to review the financial results for the quarter. Let's jump in. Starting with data centers, we delivered another impressive quarter with revenues increasing 95% from the prior year. We achieved our fourth consecutive quarter of record orders, exceeding $1 billion in quarterly order intake for the first time in our history. 
Strong demand has pushed our backlog to another historic high. In addition, we recently received a major new program award with a strategic hyperscaler customer. Through this partnership, we will supply more than $400 million of custom air handling units through calendar year 2027 to cool next-generation data centers. We have continually added manufacturing capacity to support the surging demand for our air handling products since acquiring the Scott Springfield business in 2024. To that end, we are currently launching production at our third dedicated data center facility in Calgary and are actively increasing throughput at our facility in Franklin, Wisconsin. Demand continues to be incredibly strong across our entire data center cooling portfolio, and we are strategically using 80/20 principles to manage this growth. Regarding our overall capacity expansion, we remain firmly on track. 
We currently have 13 chiller lines up and running and remain fully committed to reaching 20 operational lines by the end of the fiscal year. A massive part of executing this capacity expansion has been stabilizing our supply chain, and I'm pleased to report that we have made significant progress during this quarter. Over the past few months, the reliability of our supply chain has steadily improved, and we have entered into multiple LTAs with key suppliers to lock in volume for critical components in 2027. 
We've also continued to share our future volume requirements with our suppliers so that they can confidently increase their own capacity but their expansions take time to ramp. This supply-demand imbalance is leading to higher prices incremental to the materials inflation and tariffs. We are working on cost sharing and pass-through mechanics, but that takes time as well. In addition, we occasionally get surprised by other smaller disruptions. While these may not result in material production impacts, they can still create delays in short-term inefficiencies. Furthermore, we continue to leverage the specialized capabilities of our Commercial HVAC segment to support the rapid growth of our data center business. Commercial HVAC is already successfully producing V-Block subassemblies for our chillers and recently passed testing for another critical component, officially adding them to our qualified supplier panel. 
Scaling our supply chain as we expand capacity to meet demand presents a number of challenges that need to be continually managed. That said, we are in a much stronger position than we were 90 days ago, and I'm incredibly proud of what the team has accomplished. Please turn to Slide 5. The Commercial HVAC segment also delivered a strong quarter with revenues increasing 23% from the prior year. Our coils business continues to benefit from higher sales to data center customers. 
Our CHVAC segment has a significant opportunity to drive incremental growth in the data center market, and we are currently executing on several strategic fronts. First, we have been selling coils directly to various external data center cooling companies for some time, which was a primary driver of our revenue growth over the past several quarters. Second, we are capitalizing on a developing trend where hyperscalers are getting involved in downstream sourcing, specifically identifying qualified Tier 2 suppliers for custom data center cooling products. We are currently in active discussions with one of our strategic customers to become a key coils provider within their supply chain. 
This represents a major incremental opportunity for our Commercial HVAC business that could lead to significant future orders. Additionally, our coil sales are creating a strong pull-through effect for our coatings business as many customers request specialized coatings to prevent corrosion in harsh environments. Our coatings business had an outstanding quarter with revenues up 28% from the prior year. Finally, CHVAC has multiple opportunities to support our own data center business. 
As I mentioned, we're currently producing  V-Block subassemblies for our chillers and plan to start supplementing our current supply needs with additional CHVAC manufactured products later this fiscal year. These are exciting opportunities that should drive revenue growth in the near term, fully supported by our disciplined 80/20 focus. We are also seeing excellent growth opportunities elsewhere in the segment. Specifically, we are expanding our product line for portable heating products that we acquired as part of the LB White transaction last year. Overall, there's a wealth of opportunities for both revenue growth and margin expansion within the CHVAC segment. Please turn to Slide 6. 
As you know, we successfully closed on the spin-off of our Performance Technologies business and merger with Gentherm on October 1 as planned. Preparing for this transaction of this scale was a massive undertaking for both teams, and I'm pleased to report that the initial phases of the transition are going smoothly. I want to extend my sincere gratitude to our internal team who tirelessly manage the complex work streams required to execute this transaction as well as to our external advisers. 
Gentherm has been an outstanding partner throughout this process, and we are confident they will provide a fantastic home for that business. For Modine, this milestone represents a clean strategic separation that allows us to focus 100% of our resources on our highest growth, highest margin thermal management opportunities. Finally, I'd like to remind everyone of our upcoming Analyst and Investor Day planned for November 18. We are holding the event in Chicago with a live webcast for those not planning to attend in person. We will provide an in-depth review of the company's strategy, including growth opportunities for both segments, along with our new long-term financial targets. It should be a great event. With that, I'll turn the call over to Mick.

**Michael Lucareli** (Executives):
Thanks, Neil, and good morning, everyone. Please turn to Slide 7 to review the Q2 segment results. Beginning with data centers, I want to highlight the exceptional rate of revenue and earnings growth, which continues to outpace the rest of the market with a 95%, increase in sales. Americas sales grew 132%, driven by strong demand from hyperscale customers and EMEA sales decreased 6%, mainly due to the timing of shipments. Adjusted EBITDA grew 66%, resulting in an adjusted EBITDA margin of 15.4%. As I discussed last quarter, we reported a nice sequential margin improvement from the first quarter. However, this was somewhat lower than we anticipated. On the positive side, we continue to see a lower impact from the fixed cost absorption and expansion costs. This was relatively in line with our expectations. 
However, the supply chain and material impacts were larger and are lingering longer than we had expected. These can be grouped into a few key baskets, including logistics with a negative impact from tariffs, raw material inflation and higher prices paid to our suppliers to secure volume. We're working on commercial actions for current and future programs to address these additional costs, and we're confident that we can recover these costs. 
We remain excited about the overall positive momentum in this segment and anticipate further margin improvements through the second half of the year. Based on our updated revenue and margin outlook, we anticipate that the Data Center segment will generate earnings growth in excess of 80% this year. Please turn to Slide 8 to review Commercial HVAC. Commercial HVAC also delivered strong revenue growth with a 23% increase in sales. 
HVAC Technologies sales increased 20% and Heat Transfer Solutions sales improved 16%. Adjusted EBITDA increased 22%, while the adjusted EBITDA margin was flat to the prior year at 15.1%. Similar to the Data Center segment, we anticipated a higher margin in the second quarter. The major driver of the flat margin was the mix of product sales along with higher material and tariff costs. Commercial HVAC remains on track for the year as the leadership team focuses on driving both growth and margin expansion through 80/20 initiatives. 
We expect double-digit earnings growth and incremental improvements in the adjusted EBITDA margin during the second half of the fiscal year. Please turn to Slide 9. For Performance Technologies, I'll keep my comments relatively brief given the recently completed spin-off and merger with Gentherm. Sales were relatively flat with Heavy-Duty up 11% and On-Highway down 5%. Adjusted EBITDA declined 3% from the prior year and adjusted EBITDA margin was 14.2%. These results were generally in line with our expectations. As Neil covered, the separation plan and merger with Gentherm was completed on October 1. We are very proud of the improvement made these past few years by the Performance Technologies business and its legacy for Modine. Gentherm and Modine are a fantastic combination with a bright future, and we wish them all the best. 
Now let's review the total company results. Please turn to Slide 10. Second quarter sales increased 35%. And I want to point out that if we just look at our remaining data center and commercial HVAC segments, revenue growth was 59%.
Gross margin declined by 160 basis points to 20.7%, driven by lower margins in all 3 segments and largely due to material cost inflation. Although we continue to invest in incremental SG&A to support growth, we're controlling the spending as a percentage of sales. Reported SG&A also includes $14.1 million of expenses directly related to the spin-off of the Performance Technologies business. 
I'm pleased to report that adjusted EBITDA increased $32.4 million or 31%, resulting in a 13.7% adjusted EBITDA margin. As I previously discussed, the actual margin was somewhat lower than we anticipated, but there continues to be sequential improvements as we launch more volume and recover material costs. In Q2, there was a 150 basis point improvement from the first quarter, and we expect to see further improvements in the second half of the year. 
Adjusted earnings per share was $1.35, 27% higher than the prior year. This excludes $29.5 million of income tax expense related to legal entity restructuring steps required to spin off the Performance Technologies business. Now moving to cash flow metrics. Please turn to Slide 11. Free cash flow was negative in the second quarter, primarily due to the working capital and capital investments in data centers, along with expenses related to the Performance Technologies spin-off. As expected, we're deploying cash for working capital to support our growing data center customer demand and protect our production from supply chain constraints. In addition, we incurred $27.7 million of cash payments, primarily for restructuring and disposition-related costs. 
Lastly, cash taxes were higher than normal due to some unique situations and significant customer LTA payments. Net debt was $211 million higher than the prior fiscal year-end, but we received approximately $200 million (sic) [ $199 million ] from Gentherm on October 1, which was used to repay debt. Based on our current outlook for earnings and cash flow, we expect the leverage ratio will decrease further by year-end. 
Now let's turn to Slide 12 for our fiscal '27 outlook. As announced in our press release, we're updating our fiscal '27 guidance to reflect our higher revenue outlook for our remaining businesses and the successful spin-off of the Performance Technologies business. Starting with the third quarter, we'll report historical results for this business as discontinued operations. So our current outlook now excludes Performance Technologies revenue and earnings for the full year. Table is available in the appendix providing a recast of financial information for net sales and adjusted EBITDA by quarter for fiscal '26 and year-to-date fiscal '27. We expect total company sales to be in the range of $3.1 billion to $3.2 billion, representing a 50% to 55% increase from the prior year, excluding Performance Technologies revenue from both periods. 
We expect data center sales to grow 80% to 90% and expect commercial HVAC sales to grow 10% to 15% from the prior year. I want to highlight that both of these ranges represent an increase from our segment outlook last quarter. With revenue expectations increasing, we're still expecting continued margin improvement in the back half of the year. However, we believe that margins will improve at a lower rate than originally anticipated, mostly due to ongoing cost increases across the supply base. 
Given the revenue outlook and ongoing improvements in margins, I'm pleased to say that we expect fiscal '27 adjusted EBITDA to be in the range of $470 million to $500 million, representing a growth rate in excess of 50%.
Again, this outlook excludes Performance Technologies from the full fiscal year. From a free cash flow perspective, we expect to generate positive cash flow for the full year, making up for the use of cash in the first 2 quarters. And as I previously mentioned, we received approximately $200 million (sic) [ $199 million ] of cash on October 1. And while it is not included in our free cash flow calculation, it was used to repay debt. And to wrap up, we remain excited about our fiscal '27 outlook with outstanding revenue and earnings growth. Very few companies are generating earnings growth in excess of 50%. 
And I'm proud to say this would represent our fifth consecutive year of adjusted EBITDA growth in excess of 20%. We're looking forward to our next chapter as Modexus Solutions as we're truly a new company and have an exciting future to share with our shareholders. As Neil mentioned, we're holding an Analyst and Investor Day on November 18. Neil and the entire team are looking forward to providing a new strategic update on this next phase of our transformation, along with an exciting financial outlook for fiscal '28 and for fiscal '29. With that, Neil and I will take your questions.

**Operator** (Operator):
[Operator Instructions]
The first question is from Matt Summerville from D.A. Davidson.

**Matt Summerville** (Analysts):
Can we maybe start with data center margins? To keep it easy, if you did roughly 15% EBITDA in the first half of the year, sort of implies you need to get to somewhere in the low 20s, let's say, in the second half of the year if data center profits are set to rise by 80% as indicated in the deck and in prepared remarks. Can you specifically spell out what gets you there? Why not maybe derisk that cadence more meaningfully? And I guess, why should investors feel that this is a dependable sort of outlook? And can you bridge how much of this gap between, say, 15% and 21% first half, second half? -- how much of that is sort of solved by price capture? And if you can comment on the cadence between the 2 quarters, that would be helpful. And then I have one follow-up.

**Michael Lucareli** (Executives):
Matt, it's Mick. So as we look at second half of the year, we continue to expect a step-up each quarter sequentially. You're right in the high-level math based on our public comments there. Q3, we'd expect to see 100 to 200 basis point sequential improvement and then another step up in Q4 with the target of getting to 20% or above in Q4. And 2 major drivers. So we've talked a lot about first half of the year around labor and overhead. Those have been, as expected, those were coming in much in line with our outlook for Q2. 
So as we talked about, materials has been a significant increase. And in the quarter, that was about 375 basis points. So when we look to the second half of the year, there's 2 big drivers. One, volume is a big one. The conversion rate on incremental volume is quite high, way above, as you can imagine, at a variable level. So more volume we're putting through is coming through at a much higher margin than our targets of being at a 20% level. Secondly, we are going to recover material costs. And we have contracts in place. We already have commercial negotiations. So that recovery of material cost is going to improve our material margin. And again, if you just look at first half, second half, again, Q2 was 375 basis points at a minimum between all of our material cost increases. This was kind of the headwind or the penalty in the quarter.

**Matt Summerville** (Analysts):
And then I'm sure you guys internally have been talking about potential election outcomes. And I would imagine if I don't ask, it's going to get asked on the call. But does this outcome change the shape of your growth trajectory or the fundamental thermal backdrop for you in the United States? And putting that aside for a second, just given that we're looking at a stock price sub-$100, how are you thinking about potential aggressive share buybacks given the state of your balance sheet?

**Neil Brinker** (Executives):
Matt, this is Neil. Yes, certainly, we've all thought about the outcome of the elections, and I don't think there's really a big surprise here in terms of what shook out last night. I know that we're seeing a robust, healthy backlog that goes well beyond 2 to 3 years, and there's an immediate demand even today. 
So there's already many data centers that are in flight that have been permitted that are going to require multiple years of building and preparing. So those things are kind of in position and in place. For us, I believe that we're going to see even increased demand from this because as you remember, when we broke into the data center market, we broke in as a sustainability play. We broke in as our first data center customers were the only customers that offered a carbon-neutral data center. 
And when you offer a carbon-neutral data center, you have to have the best power use effectiveness and the best water use effectiveness. You have to be able to ensure that you are conserving energy and water. And that has been our niche and that has been our play. And I believe going forward with data centers, particularly in many local communities here in the United States, that that's going to be important for people to understand that you're using the best technology in order to drive down energy costs and drive down water usage. 
That's our play. That's our differentiation. That's how we broke into the market. I think that's going to continue to trend that way.

**Michael Lucareli** (Executives):
And Matt, on the buyback, we're -- like everybody this morning, we're digesting the news to the elections and how the markets reacted to the data center space. But to your question, at the current share price, that will obviously be a big topic with our Board as soon as we meet with them. More to come there, but that will clearly be a topic with our Board.

**Operator** (Operator):
The next question is from Noah Kaye from Oppenheimer.

**Noah Kaye** (Analysts):
Yes, I would like to follow up on the margin trajectory as well. Mick, I think you said maybe 100 to 200 bps step-up is what you contemplated for 3Q on data center margins. Is that correct?

**Michael Lucareli** (Executives):
Yes, correct.

**Noah Kaye** (Analysts):
Yes. So that would imply 4Q margins materially above 20%. I want to confirm that. And I understand what is sort of the -- if any, outsized margin benefit you get in that quarter. I don't know if there's a timing that's anticipated on material recoveries. Or is that kind of really the right level to think about as a jumping off point going into '28. Maybe you can comment on that. And maybe even following up on that point, the visibility you now have into the cost base through some of these LTAs that I know have been a big lift for the company over the last couple of months.

**Michael Lucareli** (Executives):
Yes. I'll go first, Noah. There's a lot to what you said there, but I'll try to hit it all. Yes, the -- so Q4 would be another sizable lift from if we're in a 16.5%, 17.5% margin in Q3 and Q4. The big driver in Q4 besides continued improvement in our material cost ratios is volume. So if we look at second half implied volume that's kind of in a 80%, 90% range Q3, I would see in another like 80% type growth rate. And obviously, Q4 gets us 90% plus. So that level of volume going through is a big lift. 
Also, the more programs that we are quoting, launching and so forth are all adjusting pricing real time. What I kind of want to make sure we cover with all of you is when we've talked the last few quarters, we started seeing some of the a few key components, and we talked to all of you about that, and we've gone back to our customers to recover those. At the same time, there's just general inflation we're seeing across aluminum, copper, steel, 30% core Q1, 30% Q2. These are things we didn't necessarily anticipate in the agreement. So they've had to go back. 
And Neil can comment, our customers are very supportive about recovering those. So we have a little bit of a lag effect on that element. But then certainly, as we're quoting new programs and receiving new POs, we're negotiating that upfront, which is a combination of tariffs, raw material costs and then purchase component cost. That's what -- so that's the impact in Q2, but the opportunity set for us as we go into Q3 and Q4.

**Noah Kaye** (Analysts):
And to tie into that -- I'm sorry, Neil, I don't know if we were going to add anything else. But to tie into that, I mean, these 4 quarters of record orders, your book-to-bill was greater than 2 this quarter. I guess, how is the better pricing that you're talking about embedded in the orders in the backlog? And can we just get a sense of where this backlog coverage really puts you both for the back half and even into '28?

**Neil Brinker** (Executives):
So just to build a little bit on what Mick was saying, obviously, when we negotiate these LTAs and we negotiate these program wins, we want to make sure that we can open up the agreements when there are things that are material in terms of margins. And we have been able to display that willingness to work with our customers, and that's where you're going to see some of this improvement in the back half to Mick's point. Certainly, to your other question, there'll be a -- this will be very clear in the IR Day update for FY '28 and '29 -- next week, 2 weeks.

**Michael Lucareli** (Executives):
Mind that.

**Noah Kaye** (Analysts):
We're looking forward to it like it's next week. But I know there's a bunch of others with questions, so I'll turn it over...

**Operator** (Operator):
The next question is from Chris Moore from CJS Securities.

**Christopher Moore** (Analysts):
Obviously, lots of noise out there. Maybe just kind of how you would characterize 2 things from a customer kind of standpoint. One would be what you're hearing in terms of from availability from a cash flow perspective to build? And two is the kind of certainty in terms of the final geographic destination? Is it still -- is that still up in the air on a lot of the work that you're doing at this stage?

**Neil Brinker** (Executives):
I think for the work that we're considering that beyond '28 into '29 and 2030, certainly, there's some of that in terms of locations and exact size of gigawatt campuses, there's a little uncertainty there, but we're working through that in terms of how to close that gap. But in the immediate 24 months, it's there. Remember, Chris, we're one of the last products to go into the data center. So we can see a site that's been permitted and they start the construction of the site and that can take anywhere from 12 to 18 months. And then you start to bring our equipment in. So the equipment that we're preparing our inventories around that we're going to be building over the next several years are for sites that are permitted and are in place. 
So more of the backlog that we're working on in terms of size as well as locations where that may change from state to state, which we have seen that happen in the past, in size. They continue to get bigger rather than smaller. That's beyond 2 years from now, Chris.

**Christopher Moore** (Analysts):
Got you. Very helpful. And maybe just -- I know that with Gentherm, there's still, I think, $20 million to $25 million additional costs in the second half for the transition services agreement. Are these costs included in the EBITDA estimate or they'll be adjusted out?

**Michael Lucareli** (Executives):
Great question. In our guide is about full year and when we do disc ops, and we remove Performance Technologies from the full year, there would be about $10 million to $15 million of temporary stranded costs. Obviously, we had PT for half the year. But if you just back them out in our guide, that includes that. And when we first announced the spin-off, we said we didn't anticipate much in the way of stranded, and we still believe that where those costs will be reabsorbed is through the data center growth. So in other words, all those resources we have working on Performance Technologies at the rate of growth we're adding on data centers, those will be fully absorbed by next fiscal year. 
It's just more of an internal accounting. But to be clear, in this interim period with now with PT gone $10 million to $15 million, and it's really a half a year's impact in the second half, about, I'd say, $7 million to $8 million here that we need to redeploy into the data center business. Hope that answers your question.

**Operator** (Operator):
The next question is from David Tarantino from KeyBanc Capital Markets.

**David Tarantino** (Analysts):
Maybe following up on the data center margins. Can you just take us through how these headwinds progressed through the quarter? I'm particularly thinking back to last quarter's commentary around margins improving in June. So can you give us some color on how this evolved through the quarter and through October as you locked down more supply and worked on price with your customers?

**Michael Lucareli** (Executives):
Yes. Neil can add more color, David, that I would say that -- again, I go back to what we talked about last quarter was what's really started was we were surprised by some short shipments of a few key components. And Neil talked quite a bit about working through those. What's continued to happen, I'd say, through the quarter, it would be other suppliers coming forward either with shortages or their own volume challenges. And then what comes with that, what -- when I talk about material costs, we have expedited freight and logistics and tariffs. So a couple of things that what's happening as the quarter continued to go on. And I think Matt Summerville had asked a good question. We're trying to get in front of it and make sure why we talked about reducing our outlook for the rate of margin improvement is expecting that this will linger longer. But in some cases, we had some sheet metal suppliers or something that don't -- weren't hitting their deliveries. 
Other cases, we're getting the deliveries that we asked for, but they show up on a Friday instead of a Monday or we're shipping parts that we have in Europe over to North America, so we can utilize them. So a lot of inefficiencies getting the product in the door to keep the lines moving. And I know it's a lot, but it isn't just that, hey, someone called us and we are negotiating a price increase or an LTA that we should've known about. I think it's just almost the day-to-day evolution. Neil, any other color?

**Neil Brinker** (Executives):
No, I think that's good color. I mean, ultimately, we have a decision to make. When we have these challenges in the operations environment with the supply chain, you can look at your customer and apologize and not do anything or you can react to it and try to continue to delight your customers. And sometimes that decision to react to it and do the best you can to meet their commitments and our expectations to meet our delivery schedules is it gets quite costly. When we have to -- when we have key components that are sourced locally and they fall through, we have to then use their international sources to get the components in. And to double that, you expedite the freight at the same time. So there are many instances where we had some suppliers prior to the LTAs that were not able to meet their commitments locally, we had to go with international shipments with expedited freight in order for us to keep the delivery schedules.

**David Tarantino** (Analysts):
Okay. Great. And then maybe could you give us some color on the pricing discussions in data center? My understanding is there were pass-throughs for inflation, but securing supply at higher cost is somewhat unique. So what does the pricing look like in the LTAs from your suppliers? Where are the discussions at this point with your customers on price? And how much more work is there to do on these discussions?

**Neil Brinker** (Executives):
Well, I think the important piece here, David, is that it's not fixed. We have the -- we've got the agreement with our customers that pricing is variable, especially when we have challenges in the metals inflation as well as tariffs, expedited freight costs, those kind of things, there's a willingness to have a conversation and there's a willingness to help us in terms of making sure we can meet their delivery commitments and help share the costs in order to do that. That is a very -- those are very active conversations that take place on a sometimes weekly basis with some of our biggest customers.

**Operator** (Operator):
The next question is from Neal Burk from UBS.

**Neal Burk** (Analysts):
On the commercial HVAC guide, you guys have just done 2 quarters of pretty good double-digit organic sales growth. But I think the guide assumes a step down in the back half. Can you elaborate on that? Do comps get harder? Or is there some timing? Or is this just conservatism?

**Michael Lucareli** (Executives):
Yes. With the heating season, one thing that was positive here and helped with HVAC in the really strong Q2, we've had a really good preseason for heating, preseason orders. So we are being a little bit cautious that for those that have been with us a while, we always -- you don't know what unfortunately, weather is going to be. So there's one element of we try to go in with a relatively conservative heat outlook. Secondly, the -- that new leadership team is really going through a heavy lift on 80/20, and we have planned exits, cost reductions and attrition, much like, again, people have been with Modine for a while, we'll see because also implied in there is a pretty healthy second half margin lift. 
Again, from the first half, I think we'd probably be looking at, at least 300, 400 basis point plus improvement in the second half of the year, and part of that is from the 80/20 activities, along with price recovery on material costs because there was also a little bit of that in the HVAC segment for Q2.

**Neal Burk** (Analysts):
Yes. I want to follow up on that. I think I think last quarter, you were pointing to kind of maybe 200 basis points of margin expansion climate for the year. And so can you kind of update where we are now relative to that? I mean you kind of guided back half, but was 2Q how much worse than you expected? And what's the sort of ramp in the back half? How do you kind of break that out between cost recovery and price?

**Michael Lucareli** (Executives):
Yes. I see the full year being up, call it, 100 basis points or so. When we look to the back half of the year, I expect a 50 to 100 basis points year-over-year improvement in Q3 and then another big lift in Q4. And again, where -- in as far as Q2, we were a little bit light, and that was also majority was around material costs and mostly raw material costs on the coils business, really strong order intake, in fact, a lot of growth driven by data center business, but that's a lag in timing recovery of like copper, aluminum and steel.

**Operator** (Operator):
The next question is from Brian Drab from William Blair.

**Brian Drab** (Analysts):
Can you touch on that opportunity that you have with the data center customer within the coils business, the timing of that and how significant could that be for that segment?

**Neil Brinker** (Executives):
Yes, that is definitely significant. We're going to have to do a lot of 80/20 work there to ensure that we're using the appropriate capacity for this key customer. Definitely is significant in terms of the revenue growth. And it would be helping them supply -- helping them secure supply so that they can continue to navigate the shortages in the supply chain. We've talked about fans as a shortage in the supply chain. You've heard lots of companies talk about that. We've talked about things like evaporators and compressors. 
Coils is now bumping up as one of the one of the areas where they're seeing a severe shortage in the industry and the fact that we're the largest independent coil producer in the world is in our advantage. So we have a lot of opportunity there, and we can partner with them, and we are partnering with them. That will be a significant mix shift in that business going forward.

**Brian Drab** (Analysts):
Can you say what the specific application is for the coil? Like what type of system or units would be...

**Neil Brinker** (Executives):
Liquid cooling, rig or heat exchangers, liquid cooling for direct ship.

**Brian Drab** (Analysts):
Okay. Got it. And then you just mentioned the shortages of fans and other components. Can you sum up at this point, like how many suppliers are an issue? How many parts are an issue? This has been a very acute problem throughout the last 6 to 12 months. But is it still an acute problem? Or has it kind of broadened?

**Neil Brinker** (Executives):
Well it hasn't broadened. It was for the -- you have limited supply with 4 key components of those 4 key components fans. We have now entered into an LTA with one of the fan suppliers. We've also entered into long-term purchase agreements a blanket PO is out 12 months for a second. So we have comfort now that we will be able to get the requested supply that we didn't have that comfort 90 days ago. With the evaporator suppliers, we've entered into an LTA. With the compressor supplier, we're in negotiations, and I would expect to close an LTA on that relatively soon. It's just a matter of how much more capacity that they need to add and how many more plants they need to add to support us. So what we see now in coils, obviously, the last, and we're vertically integrated with coils. So that's a nonissue for us. It is for others. 
So with these LTAs, we have targeted the ones that were critical a quarter back that had caused a lot of disruption. And as we enter into these LTAs and we enter into these agreements with our suppliers, this is beginning to stabilize around the strategic supply chain. Now you still have the other suppliers that need to deliver. Those are more acute in terms of an issue where you kind of work through it, maybe it delays you a week or maybe it delays you a couple of weeks, but you can -- you have an alternative source that you can ramp up quicker, much quicker because they don't have the same level of technology. So that for us is a different challenge. But the first and the most important thing to do is to lock up your suppliers that are strategic and then we'll work on the ones that are more of an acute issue throughout the weeks and months.

**Brian Drab** (Analysts):
Okay. And then if I could just ask, now that you have those LTAs in place, you have an understanding of the pricing that goes along with those. And I guess this is asking you to maybe comment on a time period further out than you want to. But in the past, we've talked about the potential for EBITDA margin for the data center business to be well north of 20% once you get to some sort of steadier state. Is that still where you're trying to drive the business towards? What is the goal for EBITDA margin for this business?

**Neil Brinker** (Executives):
Yes, that's absolutely what we're trying to drive the business for. But remember, we are in the middle of a ramp. We are ramping products. We're ramping new launches. We're ramping chiller lines. We're ramping air handling units. We're adding $100-plus million of capacity and expanding in a way that we've never done in the past. So there's going to be challenges with the ramp in terms of margin compression with all the things that we talked about. We're what, 13 lines into the 20 lines for chillers now complete. You go back a quarter ago, it was half of that. So by the end of the calendar year, we'll have the capacity in place and you'll start to work through these inefficiencies. But there's often margin compression in the middle of the ramp, and that's exactly what we're in to keep up with the enormous demand that we have for the most efficient product in the industry.

**Operator** (Operator):
The next question is from Tim Wojs from Baird.

**Timothy Wojs** (Analysts):
Maybe just on the data center guidance, the midpoint going from 70% growth at the midpoint to what's 85% now. How much of that is volume versus price?

**Michael Lucareli** (Executives):
In terms of majority of that is volume driven, Tim.

**Timothy Wojs** (Analysts):
Okay. And so I guess when you're thinking about kind of the commercial actions that you need to do to kind of recover the higher component costs, I mean, how much of that have you already went and gotten versus how much you still need to get? And I guess, what is embedded in the fourth quarter? Because I mean, there's still a pretty sizable ramp from Q3 to Q4. And I'm just trying to kind of understand your ultimate visibility to that at this point.

**Michael Lucareli** (Executives):
Let me try to answer it the best way I can. I would say based on -- so 2 things we have happening at any one time. We have our 2 major long-term agreements with a couple of hyperscalers, one we announced last year. That had well-defined pricing mechanisms in there. And as Neil said, they're open to it. And in some cases, we didn't -- both sides didn't contemplate some of the things we saw coming. So we're working through those now, and there's a lag effect on getting those approved then into the system, the invoice and so forth. 
The second element is every single new discussion we're having commercially, Neil and I are having the teams ensure all of this is upfront and such that incremental programs are addressing even like if it's 6 months between award and completion, we want to be sure that if there's inflation between us getting award for a new site that we can adjust that price before we ship the product. And from what I can kind of see just on pricing we've agreed to and passing through, I see at least like a 250 basis point lift for us on discussions we've already had with customers on current activities. So I hope that gives you a little bit of transparency. And then obviously, new programs, new POs where our full intent is to get those priced upfront when those ship.

**Timothy Wojs** (Analysts):
Okay. Okay. Yes, that's helpful. So when you think about you're not necessarily guiding to put words in your mouth, but what's implied is probably a 450, 500 basis point improvement Q3 to Q4 in EBITDA margins. Part of that is price that you do kind of have visibility to and there's a lag to it. And then parts of it will also just be kind of volume growth and better efficiencies within the existing lines. It's really like those 2 main factors.

**Michael Lucareli** (Executives):
Yes, it's a good summary. I mentioned a few minutes ago, I see in Q2 a 375 basis point material headwind. And then I mentioned to you that what I can see in our system is at least, call it, 250 basis points catch-up right now that we've gone and then you have new programs. So the other thing, right, we have to get in front of and it's a little bit of what we're talking about is then make sure we're factoring in what could come that we're not aware of yet as far as asks from the supply base. And I think -- I'll let Neil comment. I think we're well in front of that. I'm not raising that because it's a message we're trying to send is that if we have all this catch-up, then we have to make sure we don't get surprised with any incremental price increases from our supply base. I think where we're at today, I feel good about. Neil, I don't know if...

**Timothy Wojs** (Analysts):
Okay. Okay. And then I guess when you think about -- just -- I guess, when you're thinking about the supply chain itself, -- is there a way to just to give us some color on just how supply has tracked for you over the last few months? I mean, are you -- I guess, for Q3, are you kind of operating at that margin level today in terms of the data center business? And are you seeing like weekly or monthly sequential improvement in supply? Or is it still pretty kind of whack-a-mole?

**Neil Brinker** (Executives):
We have seen improvement. September was the first time that we hit 100% on-time delivery from each of our chiller plants. October was the second time we hit 100% on-time delivery for our chiller plants. And that's because of some of the stability we've got back in the supply chain.

**Operator** (Operator):
The next question is from Jeff Van Sinderen from B. Riley.

**Jeff Van Sinderen** (Analysts):
You sort of just answered part of my question. I was going to ask you, though, have you seen any customers pull forward demand with more urgency considering the political backdrop?

**Neil Brinker** (Executives):
We have seen a lot of that. I don't know if it's completely driven by the political backdrop or if it's more driven by just the breakneck speed that we see around the competitive forces with AI and high-performance compute. There is a scramble for building out as much capacity as fast as possible and outpacing their competitors, and you're starting to see a lot of interesting new technologies as well as requests for us to be able to pull some of these schedules in, whether part of that is politically driven or if it's just the pure competition in order to add the capacity faster.

**Jeff Van Sinderen** (Analysts):
Okay. And so you said you're adding 100% on-time delivery for chillers now. If you could produce more data center product right now, do you have other data center customers or potential customers that want that product?

**Neil Brinker** (Executives):
Yes. It's -- we have more demand, more requests even with the amount of capacity that we're putting in place with air handling units, with CDUs, with chillers that V-dry air coolers, adiabatic coolers, all these products that go into the data center space far exceeds our capacity.

**Jeff Van Sinderen** (Analysts):
So you really -- at this point, you're having to sort of turn away some potential customers or you're having to -- I don't want to say put on allocation, but it's almost as if you're sort of allocating to some degree.

**Neil Brinker** (Executives):
We are trying to navigate these relationships. We leverage 80/20 with how we identify customers that we consider are what we call perfect prospects internally because of their cash position, because of their ability to win because of their technology, because of their strategy. It aligns with our technology road map. When there's a high degree of fit of partnership, we have preference for those customers. It would just be a longer lead time for the others.

**Jeff Van Sinderen** (Analysts):
Understood. Sounds like a good way to operate. And then just given the balance sheet considerations of some of the smaller data center players, how are you thinking about mitigating that smaller player customer balance sheet risk, if you will?

**Neil Brinker** (Executives):
We typically don't engage.
We have enough -- yes, we have enough demand from our top 10 that we don't have to engage.

**Operator** (Operator):
The next question is from Manish Somaiya from Cantor.

**Manish Somaiya** (Analysts):
My first question is on the inventory buildup and the working capital ramp that you've had in anticipation of product deliveries. And my question specifically is if customer site schedules move to the right, how fungible is that inventory across customers and projects?

**Neil Brinker** (Executives):
So typically, we build a product that is anywhere between 70% to 80% that's scalable. The last 30 -- 20% to 30% is more customizable. So the majority of the product would be able to be shared with other projects and other demand.

**Michael Lucareli** (Executives):
Yes. Most of the inventory is actually in raw state, and we try to time shipments and even negotiations of when our products are done that they take possession of them. So most of it is raw and as Neil said, and then you can reuse that for various products.

**Manish Somaiya** (Analysts):
Okay. That's helpful. And then on '27 CapEx, I think you have guided to $150 million to $200 million with the 20 chiller lines targeted by year-end. How should we think about '28? I mean, does that kind of normalize from a capital intensity perspective? And I guess, looking ahead to cash conversion, if you can just help us with that as well.

**Michael Lucareli** (Executives):
Yes. So a few items. I'm going to push out, as Neil did to our IR Day only when we're looking into '28. But directionally, we will see a more normalized level of capital spending. It will -- I expect it will decline. But as the size of the company kind of stay at a -- for sure, we'll be over $100 million a year, I'd expect just for preventative maintenance and to support future growth. And the conversion, we expect will fully improve as we go forward from a free cash. While I'd like to see -- 2 things I'd say, while I'd love to see bigger free cash flow conversion this year, I think it's a really big positive that we're generating 90% data center growth and the company is fully funding from operating cash flows, our growth, which is great. 
But also just this year is a little bit of a unique situation when you look at our full year and even year-to-date with regards to the spin-off of the company. We mentioned that we'll probably have somewhere between $30 million, $50 million this year of cash separation costs plus some capital to separate the company. And then we had talked about cash taxes, both because of the spin-off and frankly, the LTA where we got a large upfront payment, we have about $70 million plus of higher-than-normal cash taxes. So just in this year, I think we've got $100 million of non-normal operating cash items that I wouldn't expect to continue into the future.

**Manish Somaiya** (Analysts):
And then just lastly, we're sort of in the middle of the third quarter for you guys. And as I process the discussion we've had for the past 1 hour pertaining to the targets for '27 with margins, et cetera. From your perspective, Neil, what are some of the biggest risks that you are focused on that we should at least be aware of?

**Neil Brinker** (Executives):
We have to hit the schedules for our customers. The demand that we have is critical for them to be successful. And marrying the supply chain ramp with the factory ramp with the labor ramps has been a delicate balance over the last couple of quarters. We're getting better at it, no doubt about that. And just making sure that we can continue to meet our customers' delivery schedules is critical for the future of our success because they're -- the projects and programs that we have with them extend well out into 2030, so 2031. 
So we want to make sure that we're meeting the commitments early, even if it's more costly for us to do it because we see this as strategic customers with long-term potential.

**Operator** (Operator):
There are no further questions at this time. I would like to turn the floor back over to Kathy Powers for closing comments.

**Kathy Powers** (Executives):
Thank you to everyone for joining us this morning. The replay of the call will be available through our website in a couple of hours. We're looking forward to seeing many of you on November 18 in Chicago. Have a great day. Thanks. Bye.

**Operator** (Operator):
This concludes today's teleconference. You may disconnect your lines at this time. Thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MOD_Q1_2027_Earnings_Call_20260730.md
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：FY27 總營收成長指引 20%–35%，與前次相同（outlook unchanged）（原話："total company sales to grow in the range of 20% to 35%."）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：資料中心 FY27 營收成長指引 60%–80%（原話："segment, we expect sales to grow 60% to 80%."）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：FY27 調整後 EBITDA 指引 6.5–6.8 億美元（原話："EBITDA to be in the range of $650 million to $680 million"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：FY27 全年自由現金流占營收 4%–6%（原話："full year free cash flow will be between 4% and 6%"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：資料中心 FY27 盈餘成長預期超過 85%（原話："will generate earnings growth in excess of 85% this year."）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：Q1 至 Q2 毛利/EBITDA 率預期階梯上升（原話："we expect a step-up in margins from Q1 to Q2"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：Q2 全公司利潤率預期上升約 200–250 bps（原話："probably a 200, 250 basis point lift."）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：資料中心 Q2 EBITDA 率預期回到 19%–20%（原話："a lift to be back between 19% and 20%"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：資料中心 Q3、Q4 利潤率逐季再上升（原話："a step-up in Q3 from Q2 in margin"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：商用 HVAC 預期年底 EBITDA 率 18%–20%（原話："end the year somewhere between 18% and 20%."）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：資料中心 Q1 調整後 EBITDA 率 14.8%（原話："resulting in an adjusted EBITDA margin of 14.8%."）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：管理層拆解：多餘人工與較低產量下的固定費用吸收影響利潤率 450–550 bps（原話："had a 450 to 550 basis point impact on margins"）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：管理層拆解：去年同期大額保固和解造成 150 bps 差異（原話："a 150 basis point warranty variance year-over-year"）
- 2026-07-30｜Neil Brinker (CEO)｜margin：管理層將利潤率壓力定性為暫時性時間差而非結構性（原話："are a transitional timing issue, not a structural one."）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：分拆 PT 後，HVAC 與資料中心毛利率預估較現在高 7–10 個百分點（原話："somewhere between 7% to 10% type gross"）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：PT 利潤率下滑歸因於量低與金屬、關稅成本回收落後（原話："this situation will become more favorable in future"）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：管理層稱供應鏈短缺不影響長期產能協議與年度財務目標（原話："capacity agreements or our financial targets for this year."）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：管理層對未來 2–3 年營收與盈餘成長能見度表達信心（原話："visibility and confidence in revenue and earnings growth"）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：管理層重申對 FY28 資料中心 50–70% 架構信心（原話："We're confident in the numbers that we put out, Matt."）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：預計關鍵供應商 FY28、FY29 長約即將到位（原話："would expect to have that for FY '28 as well as FY '29 in"）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：管理層稱本年度供應已確保（以供應商履約為前提）（原話："we've secured supply chain for -- going forward for this yea"）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：大型超大規模客戶長約 2027 年出貨比重 20–25%（原話："it's 20% to 25% in '27."）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：大型客戶長約 2028、2029 年出貨比重 35–40%（原話："35% to 40% in '28 and '29."）
- 2026-07-30｜Mick Lucarelli (CFO)｜commitment：HVAC 目標今年再增 200 bps 利潤率（原話："the goal here is to add a 200 basis points this year."）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：預期交易於日曆年底前完成（需核准與條件到位）（原話："we are still expecting to close the transaction before the"）
- 2026-07-30｜Neil Brinker (CEO)｜risk：供應鏈短缺比預期更早發生（原話："The shortages hit faster than we anticipated."）
- 2026-07-30｜Neil Brinker (CEO)｜risk：正考慮垂直整合以因應供應風險（原話："we're even considering vertical integration."）
- 2026-07-30｜Neil Brinker (CEO)｜risk：資料中心事業負責人離職，CEO 暫代（原話："In the interim, I will step in to lead this organization."）
- 2026-07-30｜Mick Lucarelli (CFO)｜risk：Q1 資料中心營收季減，含客戶專案延遲（原話："we also had a customer program delay"）
- 2026-07-30｜Neil Brinker (CEO)｜risk：延遲根源為特定超大規模客戶新產品設計變更，非供應鏈（原話："That is based on new product launch."）
- 2026-07-30｜Mick Lucarelli (CFO)｜risk：管理層指稱非冷水機組訂單取消或遞延（原話："chiller orders getting canceled or pushed out."）
- 2026-07-30｜Neil Brinker (CEO)｜customer：新增訂單主要來自兩家超大規模客戶與一家 Neocloud（原話："So it's basically the 3 largest customers that we"）
- 2026-07-30｜Neil Brinker (CEO)｜customer：缺料時優先供應最大客戶，與小客戶有較困難對話（原話："So our largest customers get priority."）
- 2026-07-30｜Neil Brinker (CEO)｜customer：訂單與積壓：連續第三季創新高（原話："consecutive quarter of record order intake"）
- 2026-07-30｜Mick Lucarelli (CFO)｜customer：年初約 70–80% 為確定訂單（原話："we have probably 70%, 80% of it in firm orders"）
- 2026-07-30｜Neil Brinker (CEO)｜competition：回應是否可能轉單給其他供應商：稱自家非商品化產品（原話："concerned if we were a commodity, but we're not."）
- 2026-07-30｜Neil Brinker (CEO)｜product：約一半冷水機組產能屬於長約，之後比例將下降（3MW 冷水機組上線）（原話："I'd say about half of it was part of the LTA"）
- 2026-07-30｜Neil Brinker (CEO)｜product：現有 CapEx 與廠房可支撐的產能約 40 億美元（原話："the range is right around $4 billion"）
- 2026-07-30｜Mick Lucarelli (CFO)｜capital_allocation：淨負債 4.33 億美元，較上年度底增加 7,000 萬（原話："Net debt of $433 million was $70 million higher"）
- 2026-07-30｜Mick Lucarelli (CFO)｜capital_allocation：股價走低，將與董事會討論買回股票（原話："we'll always have that discussion with the Board as well."）
- 2026-07-30｜Mick Lucarelli (CFO)｜capital_allocation：分拆後需為併購展望做準備（原話："gear up with an M&A outlook post that."）
- 2026-07-30｜Neil Brinker (CEO)｜capital_allocation：商用 HVAC 以定價抵銷材料與關稅通膨（原話："inflationary cost increases, including materials and tariffs"）

### 問答異常語氣（迴避／改口／保留）
- MOD_Q1_2027_Earnings_Call_20260730.md｜問：Neal Burk 問 7 月以來資料中心量能與供應可得性的趨勢｜答法：Neil 只答本年度供應已確保（以供應商履約為前提），未給 7 月數字；Mick 後來表示不評論 7 月，只說 6 月利潤率明顯回升
- MOD_Q1_2027_Earnings_Call_20260730.md｜問：Matt Summerville 問剩餘冷水機組產線（Grenada、Jefferson City、達拉斯）啟用時點，及 FY28 50–70% 架構是否調整｜答法：Neil 答「對數字有信心」及年底前產線將在某種效率水準上建立，未給各廠具體啟用日期，也未重述 FY28 數字
- MOD_Q1_2027_Earnings_Call_20260730.md｜問：David Tarantino 問供應問題如何隨 6、7 月演變｜答法：Neil 描述供應商硬性停供與重新談判，未給 7 月狀況；Mick 稱不逐月細說，僅講 6 月回到正常利潤率水準

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
{"date":"20260710","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"DC 業務維持 50-70% 年增至 FY2028、FY2028 DC 營收 $2B+","columns":{"2Y 驗證點":"FY2027 DC 年增落在 guide +60-80% 內","5Y 驗證點":"DC 營收 $2B+（FY28）並延續成長至 $3B+","10Y 驗證點":"MOD 成為 DC 冷卻長期結構受益者","具體數字門檻":"FY26 DC 已 +73% 至 $1.1B、Q4 DC +158%、$4B Airedale LTA（CY27-29）","來源":"MOD Q4 FY26 法說 / PR 2026-05-26","漂移觸發":"連 2 季 DC seq &lt; +10%（2Y 警戒）；DC 年增 &lt; +30%（5Y 反轉）"}},{"id":"H2","text":"Climate Solutions 毛利率在 DC 產能擴張暫時性壓縮後正常化回升","columns":{"2Y 驗證點":"FY2027 Climate GM 回升向 26%+","5Y 驗證點":"Climate GM 站穩 26-28%（規模經濟＋高階液冷 mix）","10Y 驗證點":"DC 溢價 mix 使結構毛利率高於歷史 auto thermal 時代","具體數字門檻":"Q4 FY26 Climate GM 24.6%（−510bps 因產能 ramp 暫時成本＋關稅）","來源":"MOD Q4 FY26 PR [官方歸因]","漂移觸發":"Climate GM 連 2 季再退 &gt; 1pp（2Y 警戒）；GM &lt; 22%（5Y 反轉→證偽「暫時」）"}},{"id":"H3","text":"Performance Technologies 分拆（RMT 併入 Gentherm）2026Q4 完成，純化 Climate Solutions 觸發估值 re-rate","columns":{"2Y 驗證點":"2026Q4-2027Q1 完成交割","5Y 驗證點":"純 Climate Solutions 以更高倍數獨立估值","10Y 驗證點":"—（一次性結構事件）","具體數字門檻":"2026-01-29 宣布 RMT；~$1B EV；Modine 收 $210M 現金＋股東持合併後 ~40%；outside date 2027-03-31（可延至 2027-06-30）","來源":"Modine / Gentherm IR 2026-01","漂移觸發":"2026Q4 未完成 + 推遲至 2027Q2+，或交易終止（2Y 警戒；直接削弱 H3）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"RMT 分拆延宕/失敗（融資、Gentherm 股東同意、IRS 稅務裁定、監管），分拆費用先吃近中期獲利、re-rate 敘事落空","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"交割進度公告；分拆相關費用","警戒閾值":"2026Q4 未完成且無明確新時程 → 直接削弱 H3、頁首 re-rate 假設下修"}},{"id":"R2","text":"AI DC capex 增速放緩，或電力/變壓器瓶頸（交期 36-48 個月、~11GW 專案卡公告）拖延冷卻設備實際交付 → DC 營收時程風險；疊加 hyperscaler 垂直整合冷卻","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"DC sequential 成長；hyperscaler 訂單能見度；四大 capex guide","警戒閾值":"DC seq 連 2 季 &lt; +10%；某 hyperscaler 宣布自建/獨家整廠冷卻協議"}},{"id":"R3","text":"單一客戶集中：$4B LTA 客戶未揭露身分，若其冷卻架構、時程或供應策略（second-source）生變，直接衝擊產能利用；技術路線上乾式冷卻/浸沒侵蝕冰水機","columns":{"對應假設":"H1 + H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"客戶集中度揭露；immersion/乾冷市佔；產能利用率","警戒閾值":"最大客戶佔 DC 營收 &gt; 40% 且出現 second-source 動作；immersion/乾冷架構市佔 &gt; 20%（2030 前）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"分批 starter 已建；加碼待 RMT 分拆完成（2026Q4-2027Q1）確認純 Climate Solutions re-rate，或回檔至 $200-215（Fwd PE FY27 ~26-28x）","irr_base_pct":7.1,"ev5y_pct":41.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.9,"ev5y_pct":41.0,"irr_base_pct":7.1,"max_dd_pct":-60.0,"bull_5y_price":528.0,"bear_5y_price":126.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"分批 starter 已建；加碼待 RMT 分拆完成（2026Q4-2027Q1）確認純 Climate Solutions re-rate，或回檔至 $200-215（Fwd PE FY27 ~26-28x）","price_at_dd":243.5,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
