你是 stock-analyst **v20 判斷 agent**，標的 BLK（20261017）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"BLK","date":"2026-10-17","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BLK_20261017/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BLK_20261017/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":7752,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"BlackRock Q3 2026 earnings release, 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi1_as_adjusted_operating_in","label":"As-adjusted operating income","value":3330,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"BlackRock Q3 2026 earnings release, 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi2_as_adjusted_operating_ma","label":"As-adjusted operating margin (non-GAAP)","value":47.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"BlackRock Q3 2026 earnings release, 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi3_gaap_operating_income","label":"GAAP operating income","value":2328,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"BlackRock Q3 2026 earnings release, 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi4_gaap_operating_margin","label":"GAAP operating margin","value":30.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"BlackRock Q3 2026 earnings release, 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi5_diluted_eps_gaap","label":"Diluted EPS (GAAP)","value":10.57,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"BlackRock Q3 2026 earnings release, 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi6_diluted_eps_as_adjusted","label":"Diluted EPS (as adjusted)","value":15.93,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"BlackRock Q3 2026 earnings release, 8-K Ex.99.1"},"note":"未查"},{"id":"f_kpi7_assets_under_management","label":"Assets under management","value":15488,"period":"2026-09-30（Q3 2026，公告於 2026-10-14）","unit":"USD billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"2026-09-30（Q3 2026，公告於 2026-10-14）","citation":"BlackRock Q3 2026 earnings release, 8-K Ex.99.1"},"note":"不適用"},{"id":"f_kpi8_total_net_inflows","label":"Total net inflows","value":205.5,"period":"Q3 2026（公告於 2026-10-14）","unit":"USD billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（公告於 2026-10-14）","citation":"BlackRock Q3 2026 earnings release, 8-K Ex.99.1（長期 174.8、現金管理 30.7；近 12 個月 869）"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-14","period":"2026-10-14","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-14"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_blk_gross_margin_pct","label":"BLK 毛利率","value":47.15,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BLK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_blk_operating_margin_pct","label":"BLK 營業利益率","value":32.99,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BLK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_blk_fcf_margin_pct","label":"BLK FCF 利潤率","value":12.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BLK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crcl_gross_margin_pct","label":"CRCL 毛利率","value":22.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRCL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crcl_operating_margin_pct","label":"CRCL 營業利益率","value":7.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRCL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crcl_fcf_margin_pct","label":"CRCL FCF 利潤率","value":24.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRCL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_coin_gross_margin_pct","label":"COIN 毛利率","value":72.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_coin_operating_margin_pct","label":"COIN 營業利益率","value":11.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_coin_fcf_margin_pct","label":"COIN FCF 利潤率","value":27.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_v_gross_margin_pct","label":"V 毛利率","value":80.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_operating_margin_pct","label":"V 營業利益率","value":65.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_fcf_margin_pct","label":"V FCF 利潤率","value":47.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ma_gross_margin_pct","label":"MA 毛利率","value":78.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ma_operating_margin_pct","label":"MA 營業利益率","value":59.84,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ma_fcf_margin_pct","label":"MA FCF 利潤率","value":45.53,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":1134.38,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":8.98,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":63.82,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.27,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（56.26 → 56.11）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.19,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（64.29 → 64.17）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-1.28,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（74.73 → 73.77）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":56.11,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":64.17,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":73.77,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":25.83,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝57.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":57.5,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.46,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝45.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":45.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.5,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝43.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":43.4,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.29,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 56.11，分子＝快照價 1082.39","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.975,"period":"2026-10-17","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-17"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1125.0,"period":"2026-10-17","unit":"USD m","basis":"yfinance 最新一季：總債務 14968.0、現金 13843.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":162.48,"period":"2026-10-17","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":185434.74,"period":"2026-10-17","unit":"USD m","basis":"市值 184309.74 ＋ 淨負債 1125.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":29448.25,"period":"2026-10-17","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（8 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":32352.32,"period":"2026-10-17","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.3,"period":"2026-10-17","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"BlackRock 2026 年第二季淨流入 $1,990 億（ETF 占 $1,780 億），年化有機成長 6.2%，高於 3–5% 目標區間","source":"Morningstar / Advisor Perspectives 2026Q2 BlackRock 財報報導","url":"https://www.advisorperspectives.com/articles/2026/07/15/blackrock-crosses-15-trillion-192-billion-inflows","excerpt":"Net inflows of $199 billion during the second quarter represented an annualized organic AUM growth rate of 6.2%.","as_of":"2026-07-15","retrieved_at":"20261017","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"全球 ETF 市占：2025 年底 iShares 約 28%、Vanguard 21.4%、State Street 10%；2026 年 4 月底 iShares 27.7%、Vanguard 21.4%、State Street 9.9%（iShares 微幅下滑）；4 月 Vanguard 淨流入居首","source":"ETFGI 全球 ETF 報告（經 theasset.com／marketsmedia 轉載）","url":"https://www.theasset.com/article/55729/global-etf-assets-surge-33-7-to-record-us-19-85-trillion","excerpt":"BlackRock's iShares leads the industry with US$5.56 trillion in assets, a 28% market share, followed by Vanguard with US$4.25 trillion ( 21.4% ) and State Street's SPDR ETFs with $1.99 trillion ( 10% ).","as_of":"2026-01-31","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"美國 ETF 市占（2026 年 7 月底）：iShares $4.53 兆／28.8%，Vanguard $4.51 兆／28.7%，兩者幾乎持平；SPDR 13.2%","source":"ETFGI 美國 ETF 統計（經 marketsmedia 轉載）","url":"https://www.marketsmedia.com/vanguard-nears-blackrock-for-top-spot-in-u-s-etf-assets/","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"有分析稱三大業者占美國 ETF 流入比重由約 80% 降至約 55%；2026 年 1 月 Vanguard 約 $490 億、iShares 約 $190 億（次級來源，未經一手驗證）","source":"Crypto Briefing「BlackRock's share of ETF inflows drops to 55% amid rising competition」","url":"https://cryptobriefing.com/blackrock-etf-inflows-share-drops-competition/","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Ropes & Gray (2026-08)：私募基金 2026 年份平均管理費降至 1.57% 的紀錄低點，半數 $10B 以上巨型基金提供折扣；費率壓縮被列為傳統主動管理人走向整併的最常被引用結構性因素","source":"Ropes & Gray, The Principal View: Trends Shaping Private Markets, August 2026","url":"https://www.ropesgray.com/en/insights/alerts/2026/08/the-principal-view-trends-shaping-private-markets-august-2026","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Broadridge 2025 全球需求模型：專業管理資產 2027 年達 $132 兆（CAGR 約 7.6%）；主動股票三年 CAGR -0.8%，固定收益配置 2024–2027 年增 2.5%/年；營收上升但利潤率持續承受結構性壓力","source":"Broadridge Global Demand Model（經 gcn.com／funds-europe 轉述）","url":"https://gcn.com/global-asset-management-to-top-130t-by-2027/8900","excerpt":null,"as_of":"2025-06-01","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"BlackRock 官方 2026 Q1 新聞稿：季度淨流入 $1,300 億，iShares ETF 創第一季紀錄，12 個月有機基礎費用成長 10%；Q3 2026 數字僅見二手來源且與 Q3 2025 數字重疊，未驗證","source":"BlackRock Reports First Quarter 2026","url":"https://www.blackrock.com/corporate/newsroom/press-releases/article/corporate-one/press-releases/blackrock-reports-first-quarter-2026","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261017","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Sutherland：資產管理營收成長愈來愈由市場而非資金流驅動，降低可預測性並削弱營收收益率；Morningstar 稱所涵蓋公司的中期資金流『起伏不定』","source":"Sutherland Global, The Great Compression; Morningstar coverage","url":"https://www.sutherlandglobal.com/wp-content/uploads/sites/2/the-great-compression-rethinking-margin-pressure-in-asset-management.pdf","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"13 州總檢察長在德州東區聯邦法院控告 BlackRock、State Street、Vanguard 合謀壓低煤炭供給（反壟斷）；其中 4 州另提消費者保護主張。BlackRock 10-Q 稱管理層目前不預期整體責任有重大影響。","source":"BlackRock Form 10-Q (period ended 2026-06-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0002012383/000119312526337177/blk-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"彭博報導美國司法部正考慮加入德州州政府主導的 BlackRock／State Street 反壟斷訴訟；尚無最終決定，司法部也可能不採取行動。","source":"Bloomberg Law: DOJ Weighs Joining Texas BlackRock, State Street Antitrust Case","url":"https://news.bloomberglaw.com/antitrust/doj-weighs-joining-texas-blackrock-state-street-antitrust-case","excerpt":null,"as_of":"2026-09-18","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026-02-09 司法部與 FTC 向法院表示，投資人持股豁免不保護 BlackRock、State Street、Vanguard 免於以持有煤炭公司股份削減產出的指控（共同持股）。Vanguard 已於 2026 年 2 月和解（2,950 萬美元）；有摘要稱開庭訂 2028 年 1 月。","source":"Global Competition Review: DOJ and FTC target common ownership in Texas coal collusion case","url":"https://globalcompetitionreview.com/organisations/blackrock?page=1","excerpt":null,"as_of":"2026-02-09","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026 年 4–5 月二手報導（Simply Wall St，聚合站）稱國會議員與律師加強檢視 BlackRock 私募信貸工具與基金流動性做法，並提及一項司法部對旗下私募信貸基金估值做法的調查；未經 Reuters／Bloomberg／SEC 文件核實。","source":"Simply Wall St 轉述（經搜尋摘要）","url":null,"excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#4","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"BlackRock FY2025 10-K 稱，聯邦機構尚未對「僅有共同持股、無反競爭使用證據」是否違反美國反壟斷法表態；搜尋未見針對 BlackRock 的歐盟競爭法正式程序（歐盟僅為一般性風險揭露）。","source":"BlackRock Form 10-K FY2025, SEC","url":"https://www.sec.gov/Archives/edgar/data/2012383/000119312526071966/blk-20251231.htm","excerpt":"The debate on common ownership has been on the agenda of lawmakers, policymakers and competition regulators globally","as_of":"2026-02-27","retrieved_at":"20261017","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#none","axis":"reg_tariff_export","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"BlackRock FY2025 10-K 風險因子指出，Aladdin 依賴第三方基礎設施與資料；第三方若未能維持與 Aladdin 規模及成長相稱的基礎設施，可能影響其韌性與客戶。","source":"BlackRock, Inc. Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/2012383/000119312526071966/blk-20251231.htm","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261017","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2025 年 2 月，17 位共和黨州檢察長指控 BlackRock 等資產管理公司未向客戶揭露中國為「外國對手」及台海風險（聲譽／監管面，非生產地集中）。","source":"RFA, BlackRock scrutinized for alleged China investment 'misstatements'","url":"https://rfa.org/english/factcheck/2025/02/10/us-asset-manager-investigation-taiwan-02102025/","excerpt":null,"as_of":"2025-02-10","retrieved_at":"20261017","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"瑞典媒體轉述（原 Reuters 未取得）：BlackRock 2026 年 7 月將中國股票與政府債由小幅加碼降為中性，理由含總經前景轉弱與地緣疑慮。","source":"Realtid.se, BlackRock minskar sin exponering mot Kina","url":"https://www.realtid.se/spara-placera/blackrock-minskar-sin-exponering-mot-kina-okad-geopolitisk-oro/","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261017","affects":["triggers"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"BlackRock 2026Q3：營收約 $7.75B（年增 19%）、年化有機基礎費成長 11%（連續第九季 ≥5%）、單季淨流入 $205B、近 12 個月 $869B（有機基礎費成長 10%）、AUM 約 $15.5T（年增 15%）；iShares 單季流入 $135B，指數債券 ETF $61B。來源為二手摘要，未能對照 8-K 原文；發布日為估計。","source":"Pulse 2.0, BlackRock AUM Hits $15.5 Trillion Following $205 Billion Of Quarterly Net Inflows","url":"https://pulse2.com/blackrock-q3-2026-results","excerpt":"Organic base fee growth of 11% marks our ninth consecutive quarter at or above 5%.","as_of":"2026-10-15","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"競爭與費率壓力：Morningstar 數據顯示 BlackRock 在美國 ETF 資產占比約 40%（2009 年 48%），Vanguard 由 11% 升至 20%；文章日期不明，屬舊資料。","source":"InvestmentNews, BlackRock gearing up for a fee war","url":"https://www.investmentnews.com/etfs/blackrock-gearing-up-for-a-fee-war/46730","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"BlackRock 已申請 iShares Nasdaq-100 ETF，分析師估費用率約 12bp，低於 QQQ 0.18%、QQQM 0.15%；屬估計，非官方公布。","source":"Yahoo Finance, BlackRock Is Coming for the Most Profitable ETF Monopoly on Wall Street","url":"https://finance.yahoo.com/markets/stocks/articles/7-reasons-blackrock-nasdaq-100-123314029.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"產業 TAM：Moody's 預期 2026 年資管業穩定，平均有機成長率不到約 2%/年，競爭與費率壓力推動整併；Broadridge 預測專業管理資產 2027 年達 $132 兆，CAGR 約 7.6%。","source":"Moody's 2026 asset management outlook; Broadridge via Funds Europe","url":"https://www.moodys.com/web/en/us/insights/credit-risk/outlooks/asset-management-2026.html","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261017","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Bloomberg 報導 BlackRock 尋求將旗下 ETF 代幣化以支援 24/7 交易，即公司自身朝代幣化布局而非被動防禦","source":"Bloomberg: BlackRock Seeks to Tokenize ETFs After Bitcoin Fund Breakthrough","url":"https://www.bloomberg.com/news/articles/2025-09-11/blackrock-seeks-to-tokenize-etfs-after-bitcoin-fund-breakthrough","excerpt":"BlackRock Seeks to Tokenize ETFs After Bitcoin Fund Breakthrough","as_of":"2025-09-11","retrieved_at":"20261017","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"PwC 2026 夏季註冊基金刊物指出，代幣化可能大幅改變 ETF 的創設與交易方式；全球 ETF 資產 2025 年底 19.5 兆美元，預期 2030 年 6 月至少 35 兆（日期為刊物期別，確切發布日未確認）","source":"PwC, Current developments for registered funds, summer 2026","url":"https://www.pwc.com/us/en/industries/assets/pwc-current-developments-for-registered-funds-summer-2026.pdf","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261017","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Deloitte 2026 投資管理展望：長期主動基金面臨成本壓力與商品化，同時 AI 加速發展；被動 ETF 仍吸納多數資金流入","source":"Deloitte, 2026 investment management outlook","url":"https://www.deloitte.com/content/dam/insights/articles/2025/us188389_cfs_im-outlook-2026/pdf/DI_2026-investment-management-outlook.pdf","excerpt":"passive ETFs still account for the majority of inflows","as_of":"2025-10-01","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"ETF.com 文章指代幣化與 AI 被視為對 ETF 形式最具威脅的兩項數位技術；AI 工具可依提示建立客製指數，利基高費率 ETF 較難自圓其說","source":"ETF.com: Are Reports of the Death of ETFs Greatly Exaggerated?","url":"https://www.etf.com/sections/advisor-center/are-reports-death-etfs-greatly-exaggerated","excerpt":null,"as_of":"2025-05-01","retrieved_at":"20261017","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"BlackRock 2026 SEC 文件稱零售私募市場 AUM 已逾 300 億美元，並把私募進財富通路的產品擴展到更多產品與多元另類資產模型","source":"BlackRock DEFA14A (SEC, FY2026)","url":"https://www.sec.gov/Archives/edgar/data/2012383/000119312526119938/d76123ddefa14a.htm","excerpt":"It is now extending its private markets to wealth offering into a broader set of products and multi-alternatives models.","as_of":"2026-04-01","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2025 年科技服務與訂閱收入 20 億美元、年增 24%；ACV 年增 31%（不含 Preqin 為 16%）","source":"BlackRock 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/2012383/000119312526071966/blk-20251231.htm","excerpt":"technology services and subscription revenue of $2.0 billion was up 24% year-over-year. Annual contract value rose 31% year-over-year including ACV related to Preqin, and 16% excluding ACV related to Preqin","as_of":"2026-02-26","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026 年 3 月 BlackRock 與 iCapital 結盟，將另類投資科技平台接入 Aladdin Wealth","source":"FundsSociety / 搜尋摘要彙整","url":"https://www.fundssociety.com/en/news/business/blackrocks-aladdin-revenues-increase-by-13-driven-by-public-and-private-market-tech-solutions/","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Jio BlackRock（印度合資）2026-04-23 起開放共同基金經銷商，結束 2025-07 以來僅直銷的模式；屬合資公司層級變動，非 BlackRock 全球策略","source":"Cafemutual: Jio BlackRock MF starts distributor empanelment","url":"https://cafemutual.com/news/industry/38515-jio-blackrock-mf-starts-distributor-empanelment","excerpt":"After remaining a direct-plan-only fund house for over a year, Jio BlackRock has finally opened up its schemes to mutual fund distributors.","as_of":"2026-04-23","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#4","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"直接指數化：BlackRock 經 Aperio 僅與第三方金融中介合作（非 D2C）；未找到 2026 年 BlackRock 去中介化的直接報導，來源為 2022 年資料","source":"Kitces / etf.com 搜尋結果（2022 年資料）","url":"https://www.kitces.com/?p=43976","excerpt":null,"as_of":"2022-12-07","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"TickerLeague 7月快照：8位分析師目標價均值約$1,327，區間$1,145–$1,488，中位數$1,342（as_of 為月份層級，日期取月中近似）","source":"TickerLeague - Consensus EPS · Q3 2026","url":"https://tickerleague.com/companies/BLK/estimates","excerpt":"Low $1,145.00, Consensus $1,326.75, Median $1,342.00, High $1,488.00","as_of":"2026-07-15","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Tickflow 2026-08-01資料：共識目標價約$1,306（27位分析師）","source":"Tickflow - BlackRock, Inc. (BLK) Stock Forecast","url":"https://www.tickflow.io/stock/BLK/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Barchart：18位分析師共識為Strong Buy（14 Strong Buy、2 Moderate Buy、2 Hold）；Q2 2026調整後EPS $13.91、AUM創高$15.3兆","source":"Barchart - what are wall street analysts target price for blackrock stock","url":"https://www.barchart.com/story/news/4019975/what-are-wall-street-analysts-target-price-for-blackrock-stock","excerpt":"Among the 18 analysts covering BLK stock, the consensus is a \"Strong Buy.\" That's based on 14 \"Strong Buy\" ratings, two \"Moderate Buys,\" and two \"Holds\".","as_of":"2026-07-31","retrieved_at":"20261017","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026財報（約2026-10-14）：調整後EPS $15.93 vs 預期約$14.13–14.25；AUM $15.49兆；Morgan Stanley維持Overweight、目標價$1,468（聚合站，未見官方稿）","source":"beinsure.com - BlackRock stock price forecast","url":"https://beinsure.com/news/blackrock-stock-price-forecast/","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261017","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-03-06 BlackRock 對旗下 HPS Corporate Lending Fund（HLEND）首度限制贖回；BLK 當日收 955.45 美元、跌 7.69%（Pomerantz 律所公告轉述）。","source":"Pomerantz LLP investor alert via placera.se","url":"https://www.placera.se/pressmeddelanden/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-blackrock-inc-blk-20260313","excerpt":null,"as_of":"2026-03-13","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"Rosen Law Firm 2026 年 9 月通知稱正調查 BlackRock 是否向共同基金投資人提供誤導性業務資訊（屬調查徵求，非已立案集體訴訟）。","source":"Rosen Law Firm case page","url":"https://rosenlegal.com/zh/case/blackrock-inc/","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"BlackRock TCP Capital Corp. 將約 2,500 萬美元的 Infinite Commerce Holdings 貸款於 2025 年底由面值markdown至零，為其私人信貸部門近期第二次突然歸零；1 月底曾揭露該基金預備將淨資產值下調 19%。","source":"Bloomberg: BlackRock Slashed Private Loan Value From 100 to Zero","url":"https://www.bloomberg.com/news/articles/2026-03-05/blackrock-slashes-another-private-loan-value-from-100-to-zero","excerpt":null,"as_of":"2026-03-05","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"PwC 2026 全球私人信貸調查：管理人預期借款人違約與信用損失將在今年影響績效，私人信貸正進入作為大型資產類別的首次考驗，但非危機。","source":"PwC Global Private credit survey 2026","url":"https://www.pwc.com/gx/en/industries/private-equity/private-credit-survey.html","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#2","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"NY Life Investment Management：公開與私人信貸皆出現利差緊縮、分化擴大與選擇性壓力；不預期立即的系統性信用事件，但晚週期情境需更重風險意識。","source":"NYLIM GMS From the Desk: Beyond the headlines – credit","url":"https://www.nylim.com/assets/documents/perspectives/gms-from-the-desk-beyond-the-headlines-credit.pdf","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261017","affects":["thesis.R"],"status":"ok"},{"id":"financial_regulatory_capital_rules#0","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"BlackRock 2026-06-30 10-Q：受監管子公司（BTC、英國 FCA／PRA 監管實體、經紀商）須維持約 22 億美元淨資本，與 2025-12-31 相同；信託銀行 BTC 受 OCC 資本與流動資產要求。","source":"BlackRock 10-Q FY2026 (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0002012383/000119312526337177/blk-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"financial_regulatory_capital_rules#1","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"美國主管機關剩餘 Basel III 資本標準提案已於 2026-03-27 刊登聯邦公報（含 Category I 銀行 ERBA）；BlackRock 提交意見，主張規則應反映實際風險，並要求 ETF 在 GSIB 附加資本框架下依底層資產信用品質處理。搜尋結果未見最終規則或生效日。","source":"BlackRock policy spotlight 'June 2026 Basel III and GSIB surcharge' ＋ Federal Reserve 意見書 FR-2026-0007/0008/0009","url":"https://www.blackrock.com/corporate/literature/whitepaper/june-2026-basel-iii-and-gsib-surcharge-policy-spotlight.pdf","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261017","affects":["thesis.R","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"BlackRock MuniYield New York Quality Fund 併入 MuniHoldings New York Fund、MuniHoldings Quality Fund II 併入 MuniHoldings Fund，2025-06-09 宣布，2025-10-15 股東通過，預計 2026-02-09 完成（未確認已完成）。屬封閉式基金整併，非 BLK 公司層級併購。","source":"BlackRock closed-end fund merger notices (search summary)","url":null,"excerpt":null,"as_of":"2025-10-15","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Pomerantz 自 2026-03 起調查 BLK 及部分董監是否涉證券詐欺，起因為 HLEND 限制贖回與股價單日下跌 7.69%；為調查徵求，未見已提起之 BLK 集體訴訟。","source":"Pomerantz LLP investor alert via placera.se","url":"https://www.placera.se/pressmeddelanden/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-blackrock-inc-blk-20260313","excerpt":null,"as_of":"2026-03-13","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Rosen Law Firm 2026 年 9 月通知稱調查 BlackRock 是否向共同基金投資人提供誤導資訊。","source":"Rosen Law Firm case page","url":"https://rosenlegal.com/zh/case/blackrock-inc/","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"BLK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.15,"operating_margin_pct":32.99,"fcf_margin_pct":12.88,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BLK","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CRCL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":22.0,"operating_margin_pct":7.42,"fcf_margin_pct":24.43,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRCL","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COIN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.74,"operating_margin_pct":11.68,"fcf_margin_pct":27.28,"rd_intensity_pct":30.66},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"V","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":80.18,"operating_margin_pct":65.61,"fcf_margin_pct":47.23,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":78.07,"operating_margin_pct":59.84,"fcf_margin_pct":45.53,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"BLK"},"financial_history":{"ticker":"BLK","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":17873000000.0,"revenue_yoy_pct":null,"gross_margin_pct":48.59,"operating_margin_pct":36.23,"net_income":5178000000.0,"diluted_eps":33.97,"free_cash_flow":4423000000.0,"fcf_margin_pct":24.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":17859000000.0,"revenue_yoy_pct":-0.08,"gross_margin_pct":48.05,"operating_margin_pct":35.49,"net_income":5502000000.0,"diluted_eps":36.51,"free_cash_flow":3821000000.0,"fcf_margin_pct":21.4,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":20407000000.0,"revenue_yoy_pct":14.27,"gross_margin_pct":49.42,"operating_margin_pct":36.94,"net_income":6369000000.0,"diluted_eps":42.01,"free_cash_flow":4701000000.0,"fcf_margin_pct":23.04,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":24216000000.0,"revenue_yoy_pct":18.67,"gross_margin_pct":46.7,"operating_margin_pct":32.66,"net_income":5553000000.0,"diluted_eps":35.31,"free_cash_flow":3552000000.0,"fcf_margin_pct":14.67,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/BLK/BLK_Q3_2026_Earnings_Call_20261014.md）

# Q3 2026 Earnings Call
**BlackRock, Inc.** | Earnings Calls | 2026-10-14

**Operator** (Operator):
Good morning. My name is Jen, and I will be your conference facilitator today. At this time, I'd like to welcome everyone to the BlackRock, Inc. Third Quarter 2026 Earnings Teleconference. Our host for today's call will be Chairman and Chief Executive Officer, Laurence D. Fink; Chief Financial Officer, Martin S. Small; President, Robert S. Kapito; and General Counsel, Christopher J. Meade. [Operator Instructions]
Mr. Meade, you may begin your conference.

**Christopher Meade** (Executives):
Good morning, everyone. I'm Chris Meade, the General Counsel of BlackRock. Before we begin, I'd like to remind you that during the course of this call, we may make a number of forward-looking statements. We call your attention to the fact that BlackRock's actual results may, of course, differ from these statements. As you know, BlackRock has filed reports with the SEC, which lists some of the factors that may cause the results of BlackRock to differ materially from what we say today. BlackRock assumes no duty and does not undertake to update any forward-looking statements.
So with that, I'll turn it over to Martin.

**Martin Small** (Executives):
Thanks, Chris, and good morning, everyone. It's my pleasure to present results for the third quarter of 2026. Before I turn it over to Larry, I'll review our financial performance and business results. Our earnings release discloses both GAAP and as-adjusted financial results. A reconciliation between GAAP and our as-adjusted results has been included in the tables attached to today's press release. I'll be focusing primarily on our as-adjusted results.
A year ago, our clients were focused on managing uncertainty around inflation, rates and growth. Today, they're focused on capturing the opportunities created by technology and artificial intelligence. They're focused on infrastructure investment and a renaissance for income investing. They're aiming to secure returns fueled from a new wave of productivity and innovation. There's more money in motion across global capital markets, and there's expanding opportunities for BlackRock and our clients. They're powered by earnings-driven returns, higher yields and broader opportunities to diversify and manage risk through our whole portfolio approach.
The breadth of our platform is deepening our relationships with clients across all channels, retail and institutional and all over the world. Capital is flowing into the infrastructure required to power AI and digital transformation. Wealth portfolios are broadening beyond traditional allocations into personalized solutions delivered at scale, and retirement is being reshaped by growing demand for income and broader investment access.
When clients need advice on capital markets, portfolio construction or a partner to deploy capital at scale across public and private markets, they're coming to BlackRock. We've methodically invested through cycles to build a scaled platform, one that can connect clients across public and private markets with technology.
It's paying off now in our results and in the accelerating pipeline ahead. Clients entrusted us with nearly $870 billion of net inflows over the last 12 months, driving 10% organic base fee growth. That's not one product or one region carrying the firm. It's broad-based across client channels, asset classes and geographies.
As we set out in our 2030 plan at last year's Investor Day, we're driving growth in higher value, higher base fee rate categories and our business mix across public, private and technology is creating more durable and all-weather growth in revenue and earnings. Shareholders are benefiting from that growth. In our first comparable quarter since the HPS close, year-on-year EPS growth accelerated to over 35%.
High momentum across our business is translating into stronger financial outcomes. We again delivered double-digit growth in revenue, operating income and earnings per share with all 3 measures reaching new records. Our scaled and disciplined financial rubric are helping translate growth into the bottom line. Our operating margin reached 47.8%, up 320 basis points year-over-year.
In the third quarter, BlackRock generated $205 billion of net inflows. Organic base fee growth of 11% marks our ninth consecutive quarter at or above 5%. Our growth continues to broaden across active ETFs, private markets, systematic, SMAs, digital assets and technology. These capabilities are scaling simultaneously, demonstrating the power of BlackRock's platform breadth and the durability of our growth model.
Third quarter revenue of $7.8 billion was 19% higher year-over-year, driven by organic base fee growth, the impact of higher markets on average AUM, higher performance fees and higher technology services and subscription revenue. Operating income of $3.3 billion was up 27% year-over-year. Earnings per share of $15.93 increased 38% versus a year ago, also reflecting higher nonoperating income and a lower diluted share count in the current quarter. Nonoperating results for the quarter included $164 million of net investment gains, primarily due to mark-to-market noncash gains linked to our minority investments in Securitize and Circle.
Our as-adjusted tax rate for the third quarter was approximately 24%. We continue to estimate that 25% is a reasonable projected tax run rate for the fourth quarter of 2026. The actual effective tax rate may differ because of nonrecurring or discrete items or potential changes in tax legislation.
Third quarter base fee and securities lending revenue of $6 billion increased 20% year-over-year, reflecting the positive impact of market beta on average AUM, organic base fee growth and higher securities lending revenue. On an equivalent day count basis, our annualized effective fee rate was approximately flat compared to the second quarter. Sustained client demand for high-value categories, including private markets, active ETFs and systematic continues to support fee rates on net inflows that are well above the firm's blended effective fee rate.
Performance fees of $630 million increased 22% from a year ago, primarily reflecting higher revenue from alternatives, including $110 million of performance fees from HPS. Quarterly technology services and subscription revenue was up 14% compared to a year ago, reflecting sustained demand for our full range of technology offerings.
Annual contract value, or ACV, increased 12% year-over-year. On a constant currency basis, we estimate ACV would have increased 13% from a year ago. We remain committed to low to mid-teens ACV growth over the long term.
Total expense increased 14% year-over-year, primarily driven by higher compensation, sales asset and account and G&A expense. Employee compensation and benefit expense was up 12% year-over-year, reflecting higher incentive compensation linked to higher operating income and higher performance-related compensation versus the prior year period.
Sales, asset and account expense increased 22% compared to a year ago, driven by higher distribution and servicing costs and direct fund expense. G&A expense was up 6% year-over-year, primarily due to higher technology investment spend. Consistent with our G&A outlook provided in January, after annualizing for the impact of HPS and Preqin, we continue to expect a mid-single-digit percentage increase in full year G&A.
We continue to deliver margin expansion on recurring fee-related earnings. Excluding the impact of all performance fees and related compensation, our adjusted operating margin for the third quarter would have been 48.6%, up 230 basis points year-over-year.
Our capital management strategy remains consistent. We invest first in the business and then return excess cash to shareholders through a combination of dividends and share repurchases. In the third quarter, we repurchased $550 million worth of shares. At present, based on our capital spending plans for the year and subject to market and other conditions, we anticipate repurchasing at least $550 million worth of shares in the fourth quarter. That's consistent with our previous guidance communicated in July.
Turning to flows. BlackRock's third quarter net inflows of $205 billion were diversified across product types, client channels, regions and active and index strategies. ETFs generated $135 billion of net inflows in the third quarter. Index bond ETFs and precision ETFs led the way, generating $61 billion and $41 billion of net inflows, respectively.
Continued demand for our growing lineup of active ETFs added $22 billion of net inflows. Our digital asset ETPs raised $8 billion in the quarter. Our ETFs have now delivered a sixth consecutive quarter of double-digit organic base fee growth, powered by higher-value ETF categories such as active and precision.
Retail net inflows of $23 billion were driven by sustained momentum in liquid alternatives, broad-based demand for our U.S. active fixed income offerings and continued inflows across Aperio and SpiderRock. Institutional active net inflows of $44 billion were positive across all product types and were led by strength in private markets, fixed income, systematic equities and liquid alternatives.
Institutional index net outflows of $27 billion were concentrated in low fee index equities. In private markets, we saw $15 billion of net inflows, mainly from deployment across infrastructure and private credit and the onboarding of a real estate mandate.
This quarter, we updated our earnings supplement to provide greater transparency into our private markets activity and drivers of fee-paying AUM. These include metrics such as fundraising, deployment, total AUM and dry powder, which can be found on Pages 9 through 11 of our earnings supplement.
Finally, our cash management platform generated $31 billion of net inflows in the third quarter. These results include fundings into customized liquidity solutions, demand for government funds and continued growth from Circle.
At our Investor Day in June 2025, we set out a vision and a business plan for BlackRock in 2030. Five quarters into the plan, we're delivering at or well above its targets, higher and more consistent organic base fee growth, a more all-weather durable mix of asset management and technology capabilities across public and private markets, consistent operating margin expansion and higher earnings per share. This third quarter notched another strong step on our way to 2030. In more uneven markets, we generated record revenue, operating income and EPS, a more than 47% operating margin and 11% organic base fee growth.
The opportunities ahead for BlackRock continue to expand. Clients are looking for a partner that can connect the whole portfolio to navigate a new environment of capital scarcity, higher long-term yields and a redesign of diversification. I don't believe we can evaluate the investment environment as risk-on or risk-off any longer. This new environment is about capital allocation acumen. It's about financing advantages through scale, access and breadth of opportunities. And it's about redesigning diversification across the client portfolio.
Our industry is being reshaped by the blending of public and private markets and growing demand for technology and data to secure success in client portfolios. These conditions play directly to BlackRock's strengths. Client engagement is higher than ever, and we enter our seasonally strongest fourth quarter with significant momentum across the firm and a long runway for growth ahead.
With that, I'll turn it over to Larry.

**Laurence Fink** (Executives):
Thank you, Martin. Good morning, everyone, and thank you for joining the call. We've built BlackRock to be a partner to clients everywhere capital markets are moving. We advise clients holistically across public markets, private markets and technology. We do it with a global perspective, but with a local lens. And that reach, that ability to cover every corner of a client's whole portfolio puts BlackRock at the center of how capital is moving in the world today, and it's showing up in our results.
Third quarter earnings per share rose 38%. Our operating margins reached 47.8%, organic base fee growth of 11% growth, reflecting net inflows of $205 billion. Year-to-date net inflows and organic base fee growth are both more than 45% higher than this time last year.
Our results reflect the scale of BlackRock today. We generated net inflows across every asset class, every client type, every region and across both active and index. AUM is up over $2 trillion in the last year, and it has now reached $15.5 trillion. We've now operated for a full year with GIP, HPS and Preqin as part of BlackRock. This quarter is the clearest view yet of the earnings power of our integrated platform. It's helping us serve more clients' needs and create more value for shareholders.
For the first time in my career, and that's 50 years of a career, I'm seeing genuine shortages of capital. Governments are running historically large deficits, while at the same time, demand for private capital is rising across the economy. Governments need financing for infrastructure. Companies need to fund a generational AI build-out. Individuals need better ways to invest and retire.
Everyone is rethinking how they deploy capital, and BlackRock is at the center of many of these conversations. We're both a trusted adviser and a destination for global client capital. That's driving meaningful activity across the firm and a growing pipeline for the future. This is especially visible through our work with the leading companies at the center of the AI build-out.
We have long-standing relationships with these hyperscalers and sovereign wealth funds and pension funds and corporate clients around the world. These long-term relationships are now underpinning some of the largest financing engagements in the market. We partnered with Meta on the financing of its planned $14 billion data center in Texas, bringing together infrastructure investments from GIP, private financing capabilities from HPS. We're also working alongside leading technology companies to create dedicated pools of financing for their customers to expand compute capabilities and capacity.
In the near term, these can supply private placements into high-grade insurance mandates. But over time, there's even a larger opportunity to securitize them into tradable structures for a much broader set of clients.
Rob Kapito and I have lived through this playbook before. In the early 1980s, mortgages were loans sitting on banks' balance sheets, illiquid and hard to price. Fannie Mae and Freddie Mac began pooling them, but that alone didn't make them tradable. What made them tradable was data, years of performance history and understanding of how the performance would move with interest rates and with the changes of the broader economy.
Once investors had a trusted time series of data, issuers had a standard to build against and the market opened up for a much bigger group of investors. That combination took the MBS market from a few billion dollars when I started to the trillions of dollars it is today. Compute capacity is now following a similar path, and we intend at BlackRock to be the center of it as we were then in the beginnings of the mortgage-backed securities market.
BlackRock is particularly well positioned to help develop this market because we combine capital formation, but most importantly, technology and data and scale. Thousands of investment professionals just participated in the Aladdin community using our analytics and risk framework to make investment decisions. AI is amplifying the value of Aladdin as we accelerate innovation and create better analytics.
As compute capacity emerges as an asset class, the markets will need trusted data, standardized performance metrics and a common framework for risk analytics. These are the capabilities we've spent decades building. They now differentiate BlackRock in working alongside technology companies and investors to establish the infrastructure this potential new market will need and require. These opportunities underscore the strategic logic behind our private markets acquisitions.
We're already mobilizing capital at a greater scale than ever before. Our AI infrastructure partnership recently made its first deployment with the closing of the Aligned Data Centers transaction, which had an approximately $40 billion enterprise value. We raised $68 billion in private markets over the last 12 months. In private credit, higher base fees are supporting stronger income for investors, making private credit an increasingly attractive source of yield and portfolio diversification.
We raised $25 billion in private credit in our first full year with HPS. We're seeing especially strong traction with insurance companies rotating or adding to high-grade solutions. We expect that to accelerate into year-end and into 2027. Across private markets, we have a strong pipeline of future capital raises and deployment opportunities.
Clients want scaled capital markets access across their entire portfolio, and that's how iShares have led the growth of the ETF industry, iShares flows were again led by our index bond ETFs with $61 billion of net inflows as investors shifted into long and short end of the curve. We also saw a strong demand for our AI-linked exposures. Our semiconductor and South Korea ETFs were among the highest inflowing products.
What sets iShares apart is the breadth and the precision of what we offer. Whatever view an investor holds, they can express it through iShares. The ETF wrapper is also evolving how investors access actively managed strategies, and iShares is leading the industry with $60 billion of active inflows in 2026, including a record $22 billion of inflows this quarter, iShares active AUM has doubled in the last year to more than $160 billion. We're already tracking ahead of the $500 million revenue ambition that we laid out last summer.
Investment performance is what ultimately drives active net returns and flows. Performance and scale reinforces each other. BlackRock's technological-driven process delivered investment insights across vast sets of securities, and that scale is what powers consistent performance. Over 90% of our systematic equity AUM is above benchmark or peer median. That performance powered a second straight record quarter across our broader systematic active equity business.
Systematic equity generated nearly $30 billion of net inflows in the third quarter and more than $60 billion of net inflows in 2026. Our systematic equity flows are up 50% compared to last year, and the total AUM is now approaching $500 billion of active investments.
We're seeing the same dynamic in fixed income. Approximately 85% of our taxable fixed income assets are above benchmark or peer median over 3 and 5 years. That consistency is why clients keep bringing us more of their portfolio. Active fixed income net inflows of $14 billion reflected strength across both institutional and retail channels. Clients turn to strategies like Strategic Income Opportunities and Total Return to capture income in a higher rate environment. Rick and his team has built this performance over decades, and we're porting it across new wrappers, including our lineup of fixed income ETFs.
Clients are also capturing income opportunities at the short end of the curve. Cash net inflows of $31 billion included several scaled mandates from clients consolidating fragmented liquidity programs into more customized solutions with BlackRock. Income is especially critical in retirement. In recent years, we innovated to deliver an option for guaranteed income in retirement through LifePath Paycheck.
And last month, we introduced our LifePath Solutions framework. It's designed to bring capabilities historically reserved for the largest retirement plans to a broader set of plan sponsors. Our $700 billion global LifePath platform reflects more than 30 years of expertise and gives us a distinctive ability to meet the challenging client needs.
Our brand and reputation are further strengthened through initiatives like BlackRock Future Builders. As part of the program, BlackRock Foundation is deploying capital to connect workers to skilled trade training. It's also embedding financial education and digital savings tools to help workers build a more durable economic security from their first paycheck all the way through to their retirement.
Many of our international pension and corporate clients are navigating structural shifts in retirement saving plans as defined contribution models continue to grow worldwide. For example, plan sponsors in the Netherlands need a partner who can help them manage the shift from defined benefits to defined contribution at scale. And we've already onboarded multiple pension mandates in connection with this transaction.
Last month, the pension fund from the Dutch construction industry named BlackRock as its preferred candidate for an $80 billion outsourced fiduciary mandate, citing our global scale, our execution capabilities and our technology. We're advising clients and government around the world on building durable retirement systems and deepening their local capital markets. And when capital is moving across borders, much of it moves through platforms like ours.
Foreign investment is moving into the U.S. equities and funds in record amounts. That activity is benefiting BlackRock with 1/3 of our long-term net inflows coming from clients outside the United States. It's even more pronounced in systematic equity with more than 70% of the net inflows are coming from international clients.
Europe and Asia each saw double-digit organic base fee growth and the Middle East delivered over 20% global base fee growth. We have a long-term local presence and years of expertise in executing in these regions. It's showing up in strong engagement in some of our highest value growth engines, including systematic equity, private markets, retirement and technology.
Aladdin underpins everything we deliver to clients. Our ACV grew at 12% in the third quarter, reflecting both new onboardings and existing clients expanding the relationship across our technology stack. We have a comprehensive public and private market workflow and data offerings through Aladdin, eFront and Preqin.
As private markets become a larger part of client portfolios, the need for transparency, the need for risk management, the need for portfolio analytics can only increase. That's a natural extension of Aladdin's role as an operating system for our entire portfolio for investors worldwide.
Our results prove the power and potential of our integrated firm. Our shareholders are participating in that growth through a 38% increase in earnings per share, a more than 47% operating margin and double-digit organic base fee growth. BlackRock brings together issuer relationships built over decades through public market platforms, financing expertise, investment performance and the technology and data that connects it all.
That combination is differentiating BlackRock in every category where we compete and in every region in which we operate. It's why BlackRock is winning mandates at the cutting edge of the capital markets from hyperscalers to compute financing to pension outsourcing to Aladdin and Preqin partnerships.
We're having accelerated momentum and a broad pipeline spanning whole portfolios, private markets, retirement and throughout our international platforms. More clients are turning to BlackRock as a destination for capital and for a partner for their growth. I'm confident in the opportunities and growth ahead for BlackRock, for our clients and importantly, for our shareholders.
Operator, let's open it up for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from Michael Cho of JPMorgan.

**Y. Cho** (Analysts):
I just wanted to touch on organic base fee growth during the quarter. It saw some nice acceleration. And we can see from the different contributors the flows that helped drive that. And Martin, I think you called out a few drivers as well. But wondering if you can unpack maybe where you're seeing increasing and maybe increasingly sustained contribution inside some of the various businesses that you highlighted.

**Laurence Fink** (Executives):
Let's get -- Martin, why don't you take that?

**Martin Small** (Executives):
Great. Thanks, Mike. So I'd start by saying we're continuing to execute on the 2030 plan. That's to deliver that durable premium organic base fee growth. Third quarter organic base fee growth was 11%. That's 9 consecutive quarters at above -- at or above our 5% long-term target. And it's also the fifth consecutive quarter at or above 8%. I think we've demonstrated that BlackRock can sustainably deliver in that 6% to 8% range. And there's clearly the ability to move above it to high single digits, low double digits in periods of elevated client activity, and you see that in high-value category and strong markets.
That can be driven by client preferences, can be driven by increased exposure to international markets, precision semiconductors, the onboarding of large mandates and the timing also, I think, of private markets fundraising and deployment. Organic base fee growth this quarter, I think as Larry and I referenced, it was very well diversified across the platform. We had strong contributions from the systematic businesses, active management broadly, deployment from our AI partnership, fundraising and fee paying on day 1 in our infrastructure mid-market strategies, precision ETFs, Aperio and SpiderRock, tax-aware, as well as cash. Just a few financial highlights, I think might be helpful to unpack just the breadth that we're delivering in sort of core asset allocation, portfolio diversifiers, tax-aware strategies in private markets.
If you were to take the $524 billion of year-to-date flows, about $220 billion are in the 5 to 10 bps range. Let's call that broad asset allocation models, core exposures that clients use for long-term holdings. About $270 billion was in the 10 to 60 basis point range, and that's where you're going to find, kind of, active ETFs, you're going to find country funds, you're going to find exposures that are about managing diversification and also tactical opportunities. And the balance of the flows above 60 basis points are going to be in private markets. They're going to be in liquid alternatives, where we had $25 billion of flows in the quarter with $15 billion in private markets, $9 billion in hedge fund strategies and liquid alternatives.
We see that mix as being strong and durable. And we think that durability really comes from two places. It's from what we've talked about consistently as being structural growers. These are just categories that when markets are strong, they're going to grow faster. And when markets are weak, they'll still grow. That's ETFs, that's active management, private markets, systematic SMA solutions. That's showing up in our pipeline.
We've got several scaled outsourcing relationships that we expect to fund towards the end of the year and in '27. And we've won a number of these high-grade insurance mandates that are going to drive growth as they're deployed over the coming months and days. So that future organic base fee growth, I think, is strong on the come, and we have line of sight to it.
In private markets, our fundraising plan remains diversified across infrastructure, private credit, multi-alternatives. We have a mix of strategies that are fee paying on raise and others that scale with deployment. And that's going to also support near-term revenue, longer-term growth and the sustained ability to deliver at least in that 6% to 8% range.
Second, we're a consolidator. If you look at flows in the industry over the last several years, the top 5 asset managers are consolidating around 80% of the flows. But there's still just this extraordinary amount of industry fragmentation by assets and revenue. So the opportunity to consolidate share in a very, very big fragmented market where every investor wants to consolidate its relationships to get the most out of its partner, that consolidation of share for us is an avenue of sustained organic growth.
Clients really want to do more with BlackRock. You see it in the flows. We've seen it in the momentum in this quarter and this last year. I think it gives the management team here a lot of confidence that we're on the right track and a lot of optimism about our ability to deliver this sustained organic growth that's above target.

**Operator** (Operator):
Your next question comes from Michael Cyprys of Morgan Stanley.

**Michael Cyprys** (Analysts):
I wanted to ask about what you're seeing and hearing from asset owner clients given the recent moves that we've seen higher in terms of long-term interest rates. And to what extent are you seeing clients changing, how they're thinking about relative value, where they're allocating incremental capital? And if you could maybe tie this into the significant AI infrastructure build-out that's underway, how sensitive do you think that investment opportunity is to higher financing costs? And are you seeing any sort of changes in the pace or the economics of those AI projects?

**Laurence Fink** (Executives):
Let me turn it to Rob, and I'll finish up.

**Robert Kapito** (Executives):
So I remember the last time you asked that question, Michael, many years ago, and the answer was bonds are back. And I would say right now, clearly, interest rates are going to be impacted by all of the obvious things, inflation, energy prices, capital supply and demand imbalances and worldwide deficits, geopolitics, and we are expecting more volatility until we can find a balance that right now suggests slightly higher rates, especially in the longer end of the curve.
But let me say that we think fixed income demand remains at the early innings. As you know, for years, investors were forced to take equity risk to generate meaningful income. And today, that has changed dramatically. The 10-year Treasury yield is more than 5%. Real rates are close to 3%. And in strategies that you know that we have like BINC and SIO, we are able to generate yields around 7% in a diversified high-quality portfolio.
Now these are bellwether returns for creating what Larry mentioned, our goal of resiliency and durability in portfolios. But what is particularly compelling is that, historically, for intermediate-term bond portfolios, future returns usually tend to track starting yields quite closely. In other words, investors don't need a heroic market outcome. Much of the return opportunity is already embedded in today's income levels.
So we're seeing clients recognize that opportunity. Fixed income generated $78 billion of net inflows in the third quarter and $205 billion year-to-date, reflecting demand for high-quality income and more resilient portfolio construction. And that environment plays directly to BlackRock's strengths. Investors can earn attractive levels of income without taking significant duration, volatility and drawdown risk.
So if rates stabilize slightly from here, we think there is substantial room for fixed income allocations to continue to grow. And our clients now can use the better wrappers that we have for fixed income, especially in bond ETFs, and they are looking to lock in these yields going forward.

**Laurence Fink** (Executives):
Related to data centers and financing, let's put it in the context of the overall federal deficits. Federal deficits after 232 years was $8 trillion, 26 years later, that's $40 trillion. And so the demand and the need to financing the deficits are at obviously record levels. I've been talking about the need for unlocking private capital. We are seeing that unlock, which is fantastic for the United States and fantastic for potential growth.
But unlocking private capital means a lot of financing, whether it's financing for AI and data centers or financing for companies like Humana, where we announced a big financing yesterday or last week when we announced the financing for AT&T. That is one of the special ingredients for growth in the United States that the role of the capital markets is playing a larger and larger component in that.
And so the competition for capital is growing between the federal deficits, which are at record levels. And now we're unlocking private capital and demand for capital in the private sector is growing. And all that means is, at this moment, it means we're going to have structurally higher interest rates for longer, and especially out the curve. And I think that's going to be with us.
Obviously, as I spoke in my prepared remarks, it is -- I don't see us having the ability to raise trillions and trillions of dollars of bespoke transactions related to data centers. The need to create a new financing vehicle for compute for chips is imperative for the U.S. to continue to build out to the scale that is necessary. And once we build this out, the entire world is going to be needing to build this out.
If you think about a 1 gigawatt data center in the United States is about a $50 billion enterprise cost, 40% of that is the cost of GPUs and chips. The other 60% is power, grid, Core and Shell. And all of that comes together. It is -- we are now seeing financing for the data centers that are based on the lease of the credit. So that's -- but now what we are also witnessing the need to build out the scale of chips and compute.
If we're going to democratize AI, the faster we could do this, the better we'll be in broadening economic success. This is an imperative. We cannot have just 5 companies or 7 companies entirely buying out every chip production that is being produced right now. We need the ability to finance start-up AI companies, start-up companies, but each one of these companies are going to need the ability to buy these new innovative compute chips. They don't have a credit rating, obviously. And so we have to come up with innovative ways.
The best way is that we could do an asset-based financing related to the chips through data, through analytics, then we can help finance start-up companies, the growth of new and young companies, and it can transform America to grow at 3% or greater. And then the debt that I just talked about will not be as consequential because we can continue to grow our economy at 3-plus percent, our debt to GDP should fall.

**Operator** (Operator):
Your next question comes from Craig Siegenthaler with Bank of America.

**Laurence Fink** (Executives):
Craig, my team is making fun of me for my last comment.

**Craig Siegenthaler** (Analysts):
We wanted to dive a little deep into your tax-aware suite, both inside and outside the $200 billion plus that sits in Aperio. Where are you seeing the most demand? Can you quantify the 3Q flow? You gave us $7 billion of Aperio flows last quarter. And on the long/short tax-aware specifically, how are you handling the capacity constraints at the two largest RIA custodians? They've actually been tightening inflows recently and does it even matter because these products are going on so many other wealth management platforms, banks, online brokers in parallel?

**Laurence Fink** (Executives):
Martin, why don't you take that?

**Martin Small** (Executives):
Craig, thanks so much for the question. I heard basically three things is sort of demand overview flows, a little bit of a breakdown and some color on the tax-aware strategies and the like. And then second, kind of the growth of long/short strategies and the financing of them in and around the custodian.
So let me start by saying, I just -- philosophically, we put the clients at the center of these strategies. And for taxable clients, maximizing returns means managing markets and taxes. We're seeing strong demand for tax-aware solutions. That's direct indexing, it's long/short and it's SpiderRock's option-based strategy that help with concentrated stock positions and liquidity events.
The Aperio platform has grown from about $40 billion of assets on acquisition to nearly $200 billion in 5 years. It's continuing to see double-digit organic growth. Our direct indexing sort of traditional long-only AUM is $175 billion, with about $13 billion of net inflows year-to-date in '26. Long/short AUM is $19 billion, with about $12 billion of net inflows year-to-date '26.
Aperio had $5 billion of net inflows in the third quarter, including $4 billion into long/short and $1 billion into long-only. Our '26 flows in these tax-aware strategies of $25 billion are 70% higher than they were in 2025, where we had a record $15 billion, and that's our fifth straight record year in these strategies.
Through SpiderRock, we also offer options-based overlay capabilities that complement direct indexing and tax-aware long/short strategies as part of a broader whole portfolio solution. SpiderRock generated $3 billion of net inflows in '25. It's now had 3 back-to-back record quarters in 2026, including $2 billion in the third quarter. So congratulations to Eric Metz and team.
I'd say BlackRock is really differentiating in this space based on service, the breadth of the platform and obviously delivering the outcomes. We're really working with clients, not just in the SMAs, but across ETFs, SMAs, direct indexing, long/short, public/private models, whole portfolio orientation. So that continues to grow well, and we have a really strong pipeline ahead.
In terms of the growth of long/short strategies and some of the dynamics happening with the custodians, I'd again start by saying we have a broad value proposition across a whole array of tax-advantaged strategies. Long/short is a category that's seen rapid expansion. And I'd say the industry custodial model and financing models, they're adjusting.
There are really compelling return and financing economics, Craig, for banks, for broker-dealers, the custodians, and we see additional parties entering the market to finance that growth. Long/short industry assets reached $170 billion, I think. That's up -- that's 3x year-over-year. And as I mentioned, our AUM is sort of closing in on $20 billion.
Client demand for these strategies is very strong. As I mentioned, $4 billion of inflows into long/short. Our focus is really on doing everything we did in long-only. And long-only, we maximized the number of custodial attachment points we had all around the industry.
Our aim is to do the same thing and increase the number of financing counterparties for these strategies for the benefit of our clients. We're broadening our platform relationships, and we'd expect additional access points through distributors and custody partners.
There's been, I think, understandable and appropriate focus on many of these custodial changes. But we've got a diversified group of financing partners and distribution partners and several other providers that are ramping up their capacity.
We're working very, very closely with our clients who are sophisticated private wealth managers on expanding access at the custodial platforms, on broadening the delivery options through new structures, alternative SMA options like SpiderRock and direct indexing and then also just providing a lot of clear guidance, education, interfacing with all the partners and financing counterparties to make sure everybody manages the onboarding, the reporting, the operations, the financing with all the high-quality fiduciary care that our clients would expect. But I think a lot more to come in this space. It serves a valuable place in the client's portfolio.

**Operator** (Operator):
Your next question comes from Michael Brown with UBS.

**Michael Brown** (Analysts):
So clearly, very impressive margin expansion this quarter. Maybe just if you could spend a little bit of time just unpacking some of the biggest drivers there and maybe how we should think about the puts and takes into 4Q? Is kind of flattish margins quarter-over-quarter a reasonable assumption?
And then more broadly, you're on track for roughly 200 basis points of expansion this year. I appreciate you don't like to bake in beta into your outlook, but what does the margin expansion opportunity look like in 2027, assuming a typical market backdrop?

**Laurence Fink** (Executives):
Martin?

**Martin Small** (Executives):
Thanks. So we continue to deliver industry-leading margins. That's been part of our 2030 strategy. Our operating and recurring fee margins each expanded, as you mentioned, by 200 to 300 basis points year-over-year. Operating margin for the quarter was 47.8%. That's up 320 basis points. And our margin ex performance fees and related comp was 48.6%, up 230 basis points.
In terms of unpacking some of the puts and takes, our reported operating margin, I think you guys understand well, can vary quarter-to-quarter depending on the composition of performance fees, which have varied payout ranges depending on the strategy. Our operating margin was higher this quarter, partially due to the performance fee mix. But excluding performance fees and related comp, we still saw 230 basis points of expansion in our recurring fee margin.
We've talked about building BlackRock around this whole portfolio around the structural growth categories of investment solutions. Those structural growers are private markets, ETFs, SMAs, models, target date technology and flows and base fee growth in these categories, they're just all -- they're all weather. They're less market sensitive. And so we see them as playing a key part in driving structurally higher adjusted operating margins.
The markets continue to have an impact on BlackRock's margins, both up and down, as you mentioned. But our 2030 goal of reaching over 30% of revenue from private markets and technology, that's aimed to dampen that effect and power more steady double-digit EPS growth and margin expansion and also provide more resiliency in client portfolios. The difference today is that we have the engines in the private markets of Global Infrastructure Partners and HPS, both of which came to BlackRock and operate at FRE margins of north of 50%. Building on that in our other franchises, we think the outlook for margin growth is that we can propel two things.
First, we can see the margin on fee recurring earnings driving upwards towards the trajectories of all the best-in-class private markets names, so north of 50%. We can do that through the acquired businesses, but we can also do it through highly scaled franchises that we have in ETFs, digital assets and systematic equities, which have high operating leverage and the ability to grow and create more expansion and profitability.
Then with constructive markets, higher fee rates on flows, strong organic growth, we think we can lift the fully burdened adjusted operating margin of the company up even further as well. We operate today at leading margins, and we still see room to scale them going forward.

**Operator** (Operator):
Your next question comes from Alex Blostein of Goldman Sachs.

**Alexander Blostein** (Analysts):
I was hoping to pull on that string of questions around AI for maybe a couple more minutes. So obviously, lots of discussion around the need for capital. I think it's quite well understood, and you obviously articulated that well as well. So as you think about which part of the ecosystem BlackRock feels most comfortable participating in today, whether it's compute or the data center, which part of the capital structure, it feels like building a fully securitized traded market around this could take some time.
So how much of a bridge you guys are likely to provide within this over the next couple of years, how it could translate into revenue opportunities for BlackRock? And ultimately, is there room to build out a capital markets syndication business around that as well, like we've seen with some of your alternative peers?

**Laurence Fink** (Executives):
Let me start and then Martin will follow up. Good question. You're right. It's going to take time to get the data and analytics. It will take time to get rating agencies to opine on this new market and come up with metrics. It's going to take time for Aladdin and Preqin to have the data set so we can do the proper analytics and -- but it is a huge priority, and we're focused on it now.
That being said, we are in the mix of almost every conversation. In the past week, I've had conversations with every major hyperscaler. It is a large opportunity, both in the financing of GPUs. It is a large opportunity for GPU financing for our HPS team. It is a large opportunity for our GIP team in terms of the build-out and working alongside hyperscalers alongside for data centers.
As I announced, we did close on the Aligned Data Centers platform. We're actually looking at two more platforms throughout the world where we could play a larger, larger role. But what I said in my prepared remarks does really resonate. As one of the largest shareholders of every major public hyperscaler and technology platform, we're having broad-based conversations with all of them.
Obviously, many of them are looking not just to be building out in the United States, but building out in other parts of the world as compute is going to be necessary throughout the world. We're engaged in that. We're going to be a part of that. And I do believe it is going to be a major source of opportunity.
That being said, the clients worldwide are hearing from some of our competitors. At the same time, they're all looking to do the same type of financing. And so it really requires having the unique structuring capabilities, working with the hyperscalers, but then working with our clients in terms of what are they looking for, what type of structure are they looking for, what type of guarantees do they need in the back end if it's compute.
So all of this is something that we are in front and center, and we're working on. And I do believe, as indicated in our private markets growth in our announced numbers, we're involved. We're getting more involved. And I see this as a major platform for us to grow on. We're presently in the market with a very large transaction now and that we'll know in the next number of months how that plays out. But we're having conversations literally daily on opportunities that we can help out.
If you think about the need in the United States alone between the need of building out our power grid, the need for securing power and the need for the build-out of Core and Shell, we're talking $7 trillion to $9 trillion over the course of a number of years. Obviously, that is a lot of financing.
And that's just in the United States. You have other places in the world that are looking for the same type of financing capabilities, too. So it's going to be broad. It's the role that the U.S. capital markets can play, and it's a big opportunity for BlackRock to be a part of this large opportunity.
Martin, do you want to go on and talk about more of that?

**Martin Small** (Executives):
I just want to amplify, Alex, one thing that Larry said, sort of the CFO's perspective on these things. The future of Western capital markets, like it's here. It's happening right now. And when we talk about the blending of public and private portfolios, we're not just talking about the client portfolio. We're also talking about how companies finance themselves.
The options, the flexibility, the fluidity across public and private markets in financing businesses directly off balance sheet through public-private structures, there's going to be so much more of that, and it's imperative that it happens well in order to finance this incredible opportunity we have for productivity and innovation through AI.
I think for BlackRock, you're going to see more of the transactions that you've seen already where we participate in the senior investment-grade public debt markets or 144A that we're participating in kind of holdco notes and mezzanine financing through insurance accounts, and we're participating in equity and junior securities, especially through the HPS and GIP platforms.
But the ability to deliver that whole cap stack financing and do it at great breadth across geographies, client types, we think that's integral in providing financing solutions for the issuers who we also think of very much as being our clients. So there's just much more to come. I think that's why Larry's passion is so evident on these calls, which is these pockets are still specialist capital.
And if we're going to see a much broader participation, we need to see some weighting basically in the aggregate that becomes GPUs, data centers, compute, et cetera. That's going to require a tremendous amount of analytics, but it's also going to require opening up pension plans and traditional fixed income allocations to these exposures.
And so to your second question, just on syndication, we're first and foremost, a fiduciary business. And our objective is to source attractive investments and then place them in long-term client accounts that generate long-term recurring management fees. So when we originate, the focus is on where that investment can create the most value across our institutional, wealth and insurance client portfolios.
Again, our advantage is the breadth of our client base. We have substantial demand across private credit funds, insurance mandates, customized client accounts, pension funds, OCIO mandates. That gives us significant flexibility in matching assets against long-term capital. So our focus is really on growing fee-paying AUM, placing assets as a fiduciary into long-term client portfolios.
If and when there's appropriate syndication and distribution revenues to secure, we will do so. But any syndication and distribution revenues, I think you all should think of as incremental to our model, not the primary driver of value creation. We think there's a much larger opportunity that's more durable in delivering private high-grade, private credit, infra debt across our platform and just deepening our client relationships over time.

**Operator** (Operator):
Your next question comes from Dan Fannon of Jefferies.

**Daniel Fannon** (Analysts):
So Martin, I wanted to unpack some of your earlier comments around flows, and you mentioned an accelerating pipeline. So curious, as you look ahead, what you see as a bigger contributor or what might be changing in some of the mix or asset classes or products is what you've seen here thus far in the first kind of 9 months of the year?

**Martin Small** (Executives):
Thanks for the question. So the first thing I'd flag is, we are heading into our seasonally strongest fourth quarter. We tend to see sort of 30% to 40% of iShares annual flows happening in the fourth quarter. So I'd expect as we get out into the end of the year here, we'll see that typical seasonality in iShares flows. I think the difference will be that we'll continue to see this mix towards higher value, higher fee rate categories in ETFs, including precision exposures, active ETFs, digital assets, factors and the like.
Second is third quarter tends to be sort of the softest in and around private markets fundraising. And so we'd expect to close out the fourth quarter with stronger fundraising towards our annual goals, which includes fee-paying day 1 strategies. And then I'm more optimistic that we're going to start seeing evergreen funds in the private markets in the fourth quarter and into the first half of next year really turn a corner. We've got about $20 billion in evergreens. We've had about $1.2 billion basically in the quarter of flows, $800 million of gross subscriptions. So I see a turning of the corner there.
I'd flag that just I think an increase in base rates is going to bring back, I think, kind of constructive allocations to private credit and retail BDCs in the direct lending space. SOFR rates go up, private credit performance has been resilient. I think you'll see, and we're having very constructive conversations with distributors around that. We still have redemptions in the queue. The industry rates are higher than they have been. But I think we're heading for a much more constructive environment in Q4 and into the first half when it comes to the returns and the cash-on-cash yields from Evergreen structures.

**Operator** (Operator):
Ladies and gentlemen, we have reached the allotted time for questions. Mr. Fink, do you have any closing remarks?

**Laurence Fink** (Executives):
Thank you, operator. I want to thank everybody for joining this call this morning and for your continued interest in BlackRock. Our quarter's result reflects the clearest view yet of the strength of our integrated platform. I think we can all see the investments we made are showing up in the growth well above our targets, and we're just getting started on what we can achieve in the years ahead. We have growing momentum heading into the end of the year, and I'm confident in what's ahead for us, our clients and you, our shareholders. Thank you, everyone, and have a very nice quarter.

**Operator** (Operator):
This concludes today's teleconference. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BLK_Q2_2026_Earnings_Call_20260715.md
- 2026-07-15｜CFO Martin Small｜capital_allocation：CFO 將每季回購下限上調至至少 5.5 億美元，高於 1 月的先前指引。（原話："anticipate repurchasing at least $550 million of shares per"）
- 2026-07-15｜CEO Laurence Fink｜capital_allocation：董事長稱今年股息加回購預計回饋股東逾 57 億美元，較 2025 年增加 16%。（原話："we expect to return over $5.7 billion"）
- 2026-07-15｜CFO Martin Small｜guidance：CFO 維持 2026 年餘下期間調整後稅率約 25% 的估計。（原話："estimate that 25% is a reasonable projected tax"）
- 2026-07-15｜CFO Martin Small｜guidance：CFO 稱 HPS 與 Preqin 年化後，全年 G&A 仍預期中個位數百分比成長。（原話："a mid-single-digit percentage increase in full year G&A"）
- 2026-07-15｜CFO Martin Small｜commitment：技術服務與訂閱的年度合約價值（ACV）長期目標為低至中十位數成長，本季 ACV 年增 15%。（原話："We remain committed to low to mid-teens ACV"）
- 2026-07-15｜CFO Martin Small｜margin：排除績效費與相關薪酬後，第二季調整後營業利益率為 46.5%。（原話："our adjusted operating margin for the second quarter"）
- 2026-07-15｜CFO Martin Small｜margin：CFO 重申週期內調整後營業利益率目標為 45% 以上。（原話："target a 45% or greater adjusted operating margin"）
- 2026-07-15｜CFO Martin Small｜margin：CFO 稱本季利潤率不是上限，並指出 2021 年曾接近 47%。（原話："I don't see this quarter's margin as a ceiling."）
- 2026-07-15｜CFO Martin Small｜margin：CFO 拆解利潤率擴張兩大槓桿之一：費用相關收益（FRE）利潤率朝私募同業最佳水準的 50% 以上推進。（原話："so north of 50%"）
- 2026-07-15｜CFO Martin Small｜margin：CFO 稱營業利益率與經常性 FRE 利潤率年增皆超過 250 個基點。（原話："FRE margins expanding by over 250 basis points"）
- 2026-07-15｜CFO Martin Small｜commitment：2030 年目標：私募與科技占營收逾 30%（2025 年投資人日提出），用以緩衝市場對利潤率的影響。（原話："our 2030 goal of reaching over 30% of revenue"）
- 2026-07-15｜CFO Martin Small｜margin：管理層稱年化有效費率與第一季大致持平。（原話："fee rate was broadly flat compared to the first quarter"）
- 2026-07-15｜CFO Martin Small｜customer：機構指數型資金淨流出 410 億美元，集中於低費率指數股票。（原話："billion were concentrated in low-fee index equities"）
- 2026-07-15｜CFO Martin Small｜customer：現金管理本季淨流出 70 億美元。（原話："cash net outflows of $7 billion in the quarter"）
- 2026-07-15｜CEO Laurence Fink｜product：Fink 稱 GIP、HPS、Preqin 的整合表現高於原先計畫。（原話："GIP, HPS and Preqin is already delivering above our plans"）
- 2026-07-15｜CEO Laurence Fink｜product：Aligned Data Centers 交易預計數週內完成。（原話："We expect 2 iShares ETFs to be available as investment"）
- 2026-07-15｜CEO Laurence Fink｜product：兩檔 iShares ETF 預計今年稍後成為川普帳戶的投資選項。（原話："we've closed about $10 billion in high-grade and infra debt"）
- 2026-07-15｜CEO Laurence Fink｜customer：Fink 稱 2026 年至今已為保險公司簽下約 100 億美元高評級與基建債委託。（原話："if we can convert 5% or 10% of those assets"）
- 2026-07-15｜CEO Laurence Fink｜customer：Fink 稱若能轉換約 8,000 億美元保險資產的 5% 至 10%，將明顯提升平均淨費率。（原話："if we can convert 5% or 10% of those assets"）
- 2026-07-15｜CEO Laurence Fink｜risk：Fink 談私募信貸：去年第四季有個別風險，現已看到信用面穩定，付款品質無明顯變化。（原話："we're not seeing any real change in the credit quality of"）
- 2026-07-15｜CFO Martin Small｜commitment：2025 年投資人日設定 2025 至 2030 年總募資 4,000 億美元目標，管理層稱持續有進展。（原話："a target of $400 billion in gross fundraising"）
- 2026-07-15｜CFO Martin Small｜customer：私募信貸約 60 億美元流入來自部署；基建約 50 億，含募資與部署。（原話："The $6 billion of private credit is really deployment based."）
- 2026-07-15｜CFO Martin Small｜competition：針對 Merrill、Schwab 調高平台費，CFO 稱未被主要美國通路商接洽、無指數 ETF 通行費談判。（原話："We've not been approached by any major U.S. distributors"）
- 2026-07-15｜CFO Martin Small｜competition：CFO 稱主動型 ETF 與共同基金的經濟性差異不大，主動型 ETF 對通路商與發行人都更好。（原話："it's better on active ETFs for both the distributors"）
- 2026-07-15｜CFO Martin Small｜product：數位資產目標：2030 年規劃中成為營收 5 億美元的業務。（原話："we're aiming to make this a $500 million revenue business"）
- 2026-07-15｜CFO Martin Small｜product：管理 Circle 約 600 億美元穩定幣準備金，約占穩定幣市場四分之一。（原話："We already manage $60 billion of reserves for Circle"）
- 2026-07-15｜CFO Martin Small｜product：已向 SEC 遞交兩份代幣化貨幣市場基金的註冊聲明。（原話："We've recently filed 2 registration statements with the SEC"）
- 2026-07-15｜CFO Martin Small｜product：Aperio 2026 年流入已約 200 億美元，超過 2025 年紀錄的 150 億。（原話："Our 2026 flows in Aperio are about $20 billion."）
- 2026-07-15｜CFO Martin Small｜commitment：管理層再度確認技術 ACV 低至中十位數成長目標。（原話："We reiterated our"）
- 2026-07-15｜CEO Laurence Fink｜product：Fink 承認公私市場整合分析平台尚未完成。（原話："We're not 100% there yet"）
- 2026-07-15｜CEO Laurence Fink｜customer：Fink 談歐洲：投資本國的趨勢出現，非僅購買美國資產。（原話："we're seeing a real nationalization going on in so many"）

### 問答異常語氣（迴避／改口／保留）
- BLK_Q2_2026_Earnings_Call_20260715.md｜問：UBS Brown 問利潤率擴張的驅動因素及未來 12–18 個月還能擴張多少｜答法：CFO 談結構性槓桿與「不是上限」，引用 2021 年約 47%，未給 12–18 個月的具體數字或時程。
- BLK_Q2_2026_Earnings_Call_20260715.md｜問：Autonomous Davitt 問 Merrill、Schwab 調高平台費是否成為趨勢、是否有淨收入逆風｜答法：CFO 以「未被接洽、無談判」及雙贏合作關係作答，未量化潛在淨收入影響，也未回答若被接洽如何應對。

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

## ⑥ 條件附卡（archetype_hint='金融' 命中）：judge_addendum_archetype.md

<!-- source: .claude/skills/stock-analyst/references/archetype-gatesets.md sha256:d173785f92087f36 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary ∈ {金融，未獲利高成長，轉機/特殊情境，受監管公用/穩定內需} -->

# archetype 換尺 gate-set 附卡（QC-44/45/46）

## QC-44 金融（bank／insurer／broker）
archetype=金融時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：ROTCE(替FCF Margin) >15%穿越循環｜ROE且>COE~10%(替ROIC) ROE>12-15%｜跨信用循環ROTCE穩定含2008/2020壓力年(替10Y ROIC穩定) 壓力年仍正/不破底｜NIM趨勢+效率比cost/income(替毛利率定價) 效率比<~60%｜Capex/Rev不適用→operating leverage/效率比改善｜EPS+TBVPS複合+股息總回報(替EPS CAGR>20%) ~10-12%即優｜P/TBV vs ROTCE(替PEG)：Warranted P/TBV=(ROTCE−g)/(COE−g)，實際P/TBV≤warranted｜CET1 ratio(替D/E<0.7) >監管要求+緩衝(~11-13%)｜NPL/NCO趨勢+撥備覆蓋+CET1緩衝(替負債安全性)：信用品質穩、撥備足。[§QC-44]
§10估值主錨：P/TBV分位+P/E，用Warranted P/TBV判貴賤；EV/EBITDA拿掉。QC-31 signal：X改ROTCE跨循環<COE／CET1跌破監管／NPL·NCO結構惡化／重大舞弊，移除FCF·NI、EV-EBITDA、Capex觸發。§6跑道：放款·存款·AUM成長+費收業務+市佔，非TAM滲透。[§QC-44]
子型：bank＝CET1/NIM/效率比/NPL·NCO/ROTCE/P-TBV｜insurer(注意US掛牌ALV=Autoliv汽車安全件循環工業，非保險，勿誤歸)＝combined ratio<100%/float/Solvency II ratio/book value/ROE，不看NIM/CET1｜broker·交易所＝ARPU/AUC/take rate/活躍戶，常與未獲利高成長blend｜支付網絡不歸金融，走品質複利。[§子型]
batch補搜：`[ticker] CET1 ratio NIM efficiency ratio ROTCE`(bank)／`[ticker] combined ratio Solvency II book value`(insurer)；yfinance .info 給不出 CET1/NIM/效率比/NPL/ROTCE/TBV。[§batch]

## QC-45 未獲利高成長
archetype=未獲利高成長時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：Rule-of-40(營收成長%+FCF margin%，替EPS CAGR>20%) ≥40｜EV/S÷營收成長growth-adjusted或EV/gross-profit(替PEG<2)｜NRR+毛利率+增量OI margin改善軌跡(替ROIC>15%，GAAP負無意義) NRR>110%/GM>65-70%｜FCF margin+轉正軌跡(替FCF Margin>15%；已正看margin升，未正看跑道+轉正路徑)｜NI負時FCF/NI比無意義→改看FCF margin絕對值+淨現金+跑道，FCF正或跑道>12個月。[§QC-45]
§10估值主錨：EV/S(+EV/gross-profit)+Rule-of-40-adjusted，轉正後接forward P/E；trailing PE/PEG拿掉。**情境樹同步改走EV/S（2026-10-12）**：FY1共識EPS≤0時程式自動切`valuation_basis=sales_multiple`，`scenario_inputs`填營收路徑×終端EV/S×終端淨負債×終端股數（形狀見尾段），不再用EPS×本益比；負債重者(淨負債/EV>30%)Bear的`net_debt_y5`須如實反映融資缺口，股權價值為負即歸零。QC-31 signal：不因GAAP NI負觸發X；X改NRR跌破100%／Rule-of-40<20連2季／毛利結構崩／現金跑道<12個月無轉正路徑／SBC稀釋失控(股數>10%/yr無營收槓桿)。§6跑道：NRR+淨增客戶+TAM滲透+SBC-adjusted轉正時程。blend：fintech broker常＝金融×未獲利，兩套都跑、標背離。[§QC-45]

## QC-46 轉機／受監管公用（輕量尺，不展開大表）
轉機/特殊情境：§4/§10主錨→資產重估/SOTP/normalized earning power/P-TBV，非成長外推；EPS-CAGR/PEG不適用。Single Thing→轉機觸發(債務重組完成/出售虧損部門/新管理層/catalyst里程碑)，非「moat擴張」。§6/§5→「為何現在會轉」catalyst+下行保護(資產底/清算價值)。QC-31 X→流動性危機(跑道<12個月+無再融資)/重整失敗/治理舞弊。[§QC-46轉機]
受監管公用/穩定內需：§4/§10主錨→DDM/殖利率+股息成長/regulated ROE(rate base×allowed ROE)/P/B；PEG/高成長門檻不適用。§6成長→rate base成長+費率案(rate case)+准許ROE，非TAM滲透。§5護城河→監管特許/天然獨佔(single-axis)。QC-31 X→准許ROE結構下調/費率案連敗/監管轉敵/過度槓桿(利率敏感)。[§QC-46受監管]
此兩類不強制長表，但換尺與catalyst/下行保護須sourced。[§QC-46]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260716","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"再組合 &gt; 侵蝕：私募 + 科技高費率池成長快於被動費率通縮，blended 費率結構與營業利益率維持向上或持平","columns":{"2Y 驗證點":"營業利益率維持 ≥ 44%；有機基費成長 ≥ 6%","5Y 驗證點":"私募 fee-paying AUM 占比顯著提升；blended 費率不再淨降","10Y 驗證點":"私募 + 科技合計貢獻營收占比過半的路徑成形","具體數字門檻":"Q2 2026 op margin 45.9%（+260bps）、有機基費 10%、私募 fee-paying AUM +40%（HPS）","信息來源":"連 2 季 op margin &lt; 42% 且有機基費 &lt; 5% → 削弱（QC-34/35）"}},{"id":"H2","text":"Aladdin 續為產業 OS：科技服務維持雙位數 ACV 成長、公私募統一作業系統黏性擴大","columns":{"2Y 驗證點":"科技 ACV 年增 ≥ 10%","5Y 驗證點":"科技服務營收占比與絕對額續升、$2B+ 年營收","10Y 驗證點":"Aladdin + Preqin 成為公私募基準的事實標準，替代成本以年計","具體數字門檻":"Q2 2026 科技 ACV +15%、科技服務營收 +13% YoY","信息來源":"ACV 增速連 2 季 &lt; 8% → 削弱"}},{"id":"H3","text":"市場建設性 + 分銷力：大盤中性偏多使 AUM 隨市場 + 淨流入複合，$15.3T 基數持續擴大","columns":{"2Y 驗證點":"年淨流入 &gt; +5% 有機成長","5Y 驗證點":"AUM 維持破 $15T 並向上；LTM 淨流入不轉負","10Y 驗證點":"AUM 隨全球金融資產同步複合，無結構性外流","具體數字門檻":"Q2 AUM $15.34T record、Q2 淨流入 $192B、LTM $868B","信息來源":"連 2 季淨流出 或 有機成長轉負 → 削弱（市場 beta 風險見 §13c）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"大盤深度回檔使 AUM 縮水、基費與績效費同步下修（beta 1.44、AUM ∝ 市場）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"AUM 月頻、淨流入、大盤 W104","警戒閾值":"AUM 季內縮 &gt; 12% 或連 2 季淨流出"}},{"id":"R2","text":"被動 ETF 費率戰加劇、iShares 相對 Vanguard 份額續失（QC-39 閘 A 已成立）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"iShares vs Vanguard ETP 淨流入份額、blended 費率 bps","警戒閾值":"iShares 份額連 4 季 &lt; 30% 或 blended 費率連 3 季下滑無補位"}},{"id":"R3","text":"反壟斷/監管（Texas + DOJ/FTC 共同持股案、ESG 政治反挫、私募入 401k 監管）限制經營模式或增合規成本","columns":{"對應假設":"H1/H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"案件程序里程碑、州級撤資動作、SEC 私募零售規範","警戒閾值":"進入集體/不利和解，或核心投票權/持股規模受限先例確立"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"逢回檔至 W52 $1,060 或前低 $1,000 加碼；或私募+科技占比續升、blended 費率確認上行後加碼至目標倉位","irr_base_pct":10.1,"ev5y_pct":53.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.0,"ev5y_pct":53.0,"irr_base_pct":10.1,"max_dd_pct":-50.0,"bull_5y_price":2241.0,"bear_5y_price":820.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"逢回檔至 W52 $1,060 或前低 $1,000 加碼；或私募+科技占比續升、blended 費率確認上行後加碼至目標倉位","price_at_dd":1093.4,"archetype":"金融","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BLK_20261017/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
