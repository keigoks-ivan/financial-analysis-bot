你是 stock-analyst **v20 判斷 agent**，標的 MMM（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MMM","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MMM_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MMM_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":6584,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"3M Q3 2026 earnings release（SEC 8-K Ex.99.1）"},"note":"consensus 約 $6.61B，略低於預期（來源：web_search）"},{"id":"f_kpi1_adjusted_operating_margi","label":"Adjusted operating margin (Non-GAAP)","value":26.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"3M Q3 2026 earnings release（SEC 8-K Ex.99.1）；調整後營業利益 $1,726M；新口徑把收購無形資產攤銷列為特殊項目"},"note":"無查得"},{"id":"f_kpi2_operating_margin_gaap","label":"Operating margin (GAAP)","value":23.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"3M Q3 2026 earnings release（SEC 8-K Ex.99.1）；GAAP 營業利益 $1,558M"},"note":"無查得"},{"id":"f_kpi3_adjusted_free_cash_flow","label":"Adjusted free cash flow","value":1197,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"3M Q3 2026 earnings release；營業現金流 $486M（web_search 引 Investing/StockTitan 之 $1.197B）"},"note":"無查得"},{"id":"f_kpi4_adjusted_eps","label":"Adjusted EPS","value":2.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"3M Q3 2026 earnings release（SEC 8-K Ex.99.1）；GAAP EPS $2.63"},"note":"consensus $2.39（來源：web_search），超預期"},{"id":"f_kpi5_fy2026_guidance_manageme","label":"FY2026 guidance（management）","value":"調整後 EPS $9.10–$9.15","period":"Q3 2026 公告（2026-10-20）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026 公告（2026-10-20）","citation":"3M Q3 2026 earnings release（SEC 8-K Ex.99.1）；調整後總銷售成長 >4.5%、有機 >3.5%、調整後 FCF 約 $4.8B（營業現金流約 $5.9B）、調整後營業利潤率約 24.6%、稅率約 20%"},"note":"FY1 共識 EPS 8.98（財報前快照，來源 consensus_revision）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-20","period":"2026-10-20","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mmm_gross_margin_pct","label":"MMM 毛利率","value":39.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MMM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mmm_operating_margin_pct","label":"MMM 營業利益率","value":20.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MMM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mmm_fcf_margin_pct","label":"MMM FCF 利潤率","value":15.83,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MMM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hon_gross_margin_pct","label":"HON 毛利率","value":36.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hon_operating_margin_pct","label":"HON 營業利益率","value":16.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hon_fcf_margin_pct","label":"HON FCF 利潤率","value":11.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_itw_gross_margin_pct","label":"ITW 毛利率","value":44.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ITW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_itw_operating_margin_pct","label":"ITW 營業利益率","value":26.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ITW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_itw_fcf_margin_pct","label":"ITW FCF 利潤率","value":17.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ITW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_emr_gross_margin_pct","label":"EMR 毛利率","value":53.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EMR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_emr_operating_margin_pct","label":"EMR 營業利益率","value":20.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EMR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_emr_fcf_margin_pct","label":"EMR FCF 利潤率","value":18.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EMR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":174.74,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":16.53,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":59.92,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.45,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.94 → 8.98）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.82 → 9.82）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.56 → 10.56）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":8.98,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.82,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":10.56,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.98,"period":"2026-07-16 → 2026-10-21","unit":"%","basis":"FY1 共識 EPS 8.72 → 8.98（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":26.08,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝97.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":97.1,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.58,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.89,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.46,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 8.98，分子＝快照價 174.74","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.757,"period":"2026-10-22","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-22"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":7857.0,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 13160.0、現金 5303.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":515.72,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":97974.34,"period":"2026-10-22","unit":"USD m","basis":"市值 90117.34 ＋ 淨負債 7857.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":25429.25,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（14 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":26610.61,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.85,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 174.74 / W52 160.67 / W104 151.03 / W250 116.58 / W250 13週斜率 0.56%"},{"id":"f_ma_w52","label":"52 週均線","value":160.67,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":151.03,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":116.58,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.56,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"MMM 10-K FY2025 風險因子列出需求受競品推出時程、競爭對手產品成功度及客戶設計變更影響；未點名具體新進入者或份額流失事件。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"Demand for the Company’s products, which impacts revenue and profit margins, is affected by, among other things: (i) the development and timing of the introduction of competitive products; (ii) the Company’s pricing strategies;","as_of":"2026-02-03","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"3M 10-K FY2025 稱其客戶基礎多元、遍布全球，無重大信用集中風險，也無對客戶延長的重大付款條件。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"The Company sells products to a diversified base of customers around the world and has no material concentration of credit risk or significant payment terms extended to customers.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"3M 2026 Q3 10-Q 列示信評 Moody's A3、S&P BBB+、Fitch A-，展望皆穩定；循環信貸 $4.25B 未動用，EBITDA/利息契約達標；負債較2025年底增加（新發歐元票據與Madison收購定期貸款）。","source":"SEC EDGAR 10-Q 2026-09-30（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000066740/000006674026000311/mmm-20260930.htm","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"3M 上調 2026 銷售成長目標，CEO Brown 仍想榨出產能","source":"IndustryWeek: 3M Hikes Sales Growth Target, CEO Brown Still Wants to 'Wring Out Capacity'","url":"https://www.industryweek.com/leadership/companies-executives/news/55392645/3m-hikes-sales-growth-target-ceo-brown-still-wants-to-wring-out-capacity","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"3M Safety & Industrial 部門 2026 年是否仍為核心強項","source":"Nasdaq/Zacks: Will MMM's Safety & Industrial Segment Remain a Core Strength in 2026?","url":"https://nasdaq.com/articles/will-mmms-safety-industrial-segment-remain-core-strength-2026","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"3M FY2025 10-K 將反壟斷與競爭法列為一般性法規風險類別之一，與產品責任、環境、反貪腐等並列；Item 3 法律程序併入 Note 17 揭露，未在該段獨立點名反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"The Company operates globally, including in some jurisdictions that pose potentially elevated risks of fraud or corruption or increased risk of internal control issues, and is subject to risks related to international, federal, state, and local treaties, laws, and regulations, including those involving product liability; securities and corporate governance; antitrust and competition; intellectual property; environmental, health, and safety; tax;","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"3M 2026 年 10-Q 稱 PFAS 法規在美加歐亞持續擴張，限值逐步下修，並可能涵蓋 3M 已不再製造的化合物；CERCLA 將 PFOA／PFOS 列為有害物質後，3M 可能需額外調查與整治。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0000066740/000006674026000246/mmm-20260630.htm","excerpt":"For example, as a result of the CERCLA designation of PFOA and PFOS as hazardous substances in 2024, and to the extent the EPA finalizes additional proposals related to PFAS, the Company may be required to undertake additional investigative, compliance, and","as_of":"2026-07-30","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K：3M 2025 年約 56% 營收來自美國以外，並明列美中貿易緊張升級可能對業務造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"During 2025, the Company derived approximately 56 percent of its revenues from outside the United States.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K：美國及其他政府已實施並擬再實施出口管制與關稅，可能造成供應鏈中斷（含稀土取得受限）、生產成本與產品定價上升。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"The U.S. and other governments have imposed, and propose to impose additional, export controls and tariffs on certain products, and financial and economic sanctions on certain industry sectors and parties.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K MD&A：2025 年銷貨成本率上升部分來自關稅；營業利益率受關稅衝擊部分抵銷。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"Increases in 2025 were primarily due to foreign currency impacts; tariffs; the exit of manufactured PFAS products;","as_of":"2026-02-03","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025 10-K：原料端關稅造成供給緊縮與通膨，但以議價供應合約與規模抵銷。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"Overall, these market conditions caused supply constraints and inflation, but were offset via negotiated supply contracts and leveraging scale across the supply base.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025 年 4 月 3M 估計年化關稅衝擊約 8.5 億美元（美中關稅占 6.75 億），中國約占進口 10%、出口略高於 10%。","source":"Manufacturing Dive：3M Q1 2025 tariff impact","url":"https://www.manufacturingdive.com/news/3m-q1-2025-850-million-tariff-impact-trade-war-china/746037/","excerpt":"3M expects to incur $850 million in tariff-related expenses this year if it takes no mitigation actions, EVP and CFO Anurag Maheshwari said in an earnings call Tuesday. China-related tariffs, both from the U.S. and retaliatory measures, are expected to cost the company $675 million in 2025.","as_of":"2025-04-25","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"3M 於 2026-01 警告美歐（格陵蘭爭端）貿易緊張可能衝擊 2026 獲利，評估關稅曝險","source":"Seeking Alpha: 3M flags tariff risk tied to Europe dispute; shares fall","url":"https://seekingalpha.com/news/4540632-3m-flags-tariff-risk-tied-to-europe-dispute-shares-fall","excerpt":null,"as_of":"2026-01-20","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2025 年中國約占 3M 全球營收 10%，進口約 10%、出口略高於 10%；關稅年化衝擊預估 8.5 億美元（美中 6.75 億）","source":"Manufacturing Dive: 3M Q1 2025 $850 million tariff impact","url":"https://www.manufacturingdive.com/news/3m-q1-2025-850-million-tariff-impact-trade-war-china/746037/","excerpt":"3M expects to incur $850 million in tariff-related expenses this year if it takes no mitigation actions, EVP and CFO Anurag Maheshwari said in an earnings call Tuesday. China-related tariffs, both from the U.S. and retaliatory measures, are expected to cost the company $675 million in 2025. The country accounts for 10% of 3M’s imports and just above 10% of exports,","as_of":"2025-04-25","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"3M Springfield 廠原用單一來源原料，2021 供應商斷貨後建立合格替代來源流程","source":"3M News: Springfield addressed supply chain challenges by qualifying alternate raw materials sources","url":"https://news.3m.com/3M-Springfield-addressed-supply-chain-challenges-by-developing-a-process-to-qualify-alternate-raw-materials-sources","excerpt":null,"as_of":"2022-01-01","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Q1 2026 全年價格貢獻約 1.3 點（含油價轉嫁約 50bp）；Q1 有機成長約 1.2%，Safety & Industrial 有機 +3.2%，Consumer 有機 -1%","source":"vectorshift 2026 Q1 summary","url":"https://vectorshift.ai/research/companies/3m-co/earnings/2026-q1-summary.html","excerpt":null,"as_of":"2026-04-21","retrieved_at":"20261022","affects":["valuation","moat_trend"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Transportation & Electronics 2026 Q2 營收成長 6.2%，半導體、航太、資料中心強勁","source":"Nasdaq: 3M Rides on Transportation & Electronics Strength","url":"https://www.nasdaq.com/articles/3m-rides-transportation-electronics-strength-sign-more-upside","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261022","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Consumer 部門需求疲弱，美國零售客流未回升","source":"Chartmill: Weak Demand Weighs on 3M's Consumer Unit","url":"https://www.chartmill.com/news/external/19037/weak-demand-weighs-on-3m-s-consumer-unit-what-lies-ahead","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 Q2 工業膠帶 +13%、個人安全 +9.4%","source":"Nasdaq: Will MMM's Safety & Industrial Segment Remain a Core Strength in 2026?","url":"https://nasdaq.com/articles/will-mmms-safety-industrial-segment-remain-core-strength-2026","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261022","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：產品需求受競爭產品推出、客戶偏好（含偏好不含第三方製造 PFAS 的產品）及客戶設計變動影響，並提及人工智慧等顛覆性技術。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"changes in customers’ preferences for our products, including preferences for products that do not contain third-party manufactured PFAS, the success of products offered by our competitors, and changes in customer designs for their products that can affect the demand for some of the Company’s products; and (v) changes in the business environment related to disruptive technologies, such as artificial intelligence and machine learning technologies","as_of":"2026-02-03","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"3M 已於 2025 年底完成退出 PFAS 製造；Novec/Fluorinert 供應 2025-12-31 結束，競爭對手已推出直接替代流體。","source":"The Engineer／廠商頁：Novec 淘汰與 ProSolv 直接替代","url":"https://theengineer.co.uk/content/product/phase-out-of-3m-novec-engineered-fluids-prosolv-direct-replacements-are-a-range-of-drop-in-alternatives-for-3m-novec-cleaning-and-degreasing-products","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"3M 退出 PFAS 後，市占重分配預期推升替代技術需求；Intel 等成立聯盟因應含氟化學品停供。","source":"Kline Group：Evolving Landscape of PFAS Regulations and Industry Response","url":"https://klinegroup.com/chemicals/the-evolving-landscape-of-pfas-regulations-and-industry-response/","excerpt":"share following 3M’s exit is expected to drive demand for substitute technologies and solutions. The Closure of 3M’s Novec Product Line- The phase-out of 3M’s Novec product line had ripple effects across various industries, particularly in semiconductor manufacturing. Intel and other leading manufacturers have formed a consortium to address the discontinuation of fluorochemicals essential","as_of":"2025-04-13","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"3M 10-K FY2025 describes sales via direct-to-user plus e-commerce and traditional wholesalers, retailers, distributors and dealers; commercial excellence initiative aims to strengthen and optimize the go-to-market channel and partner engagement. No structural shift to subscription/D2C/platform stated.","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"As part of 3M's ongoing commercial excellence initiative, the Company is focused on further strengthening and optimizing this go‑to‑market channel, enhancing partner engagement, and improving overall channel performance to support continued growth.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 2026 call: commercial excellence, cross-selling pipeline and Safety & Industrial organic growth driven by channel engagement/new products","source":"Nasdaq, 3M Q2 earnings call highlights","url":"https://www.nasdaq.com/articles/3m-q2-earnings-call-highlights","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"3M 於 2026-10-20 Q3 財報將 FY2026 調整後 EPS 指引上調至 $9.10–$9.15（7 月為 $8.80–$8.95），Q3 調整後 EPS $2.50；新口徑，細節搜尋摘要未說明","source":"3M Form 8-K Q3 2026 earnings release (sec.gov)","url":"https://www.sec.gov/Archives/edgar/data/0000066740/000006674026000308/q32026-8kerexx991.htm","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 後 3M 將 FY2026 調整後 EPS 指引由 $8.50–$8.70 上調至 $8.80–$8.95，高於當時共識約 $8.75；3 月初始指引顯著高於當時分析師預測約 $7.80","source":"Webull / MarketBeat 2026-07-21、2026-03-20","url":"https://www.marketbeat.com/instant-alerts/3m-nysemmm-issues-fy-2026-earnings-guidance-2026-07-21/","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 頁面（約 2026 年 9 月底）：14 位分析師，9 Buy／4 Hold／1 Sell，平均目標價 $165；JP Morgan 2026-10-09 維持 Overweight 但目標價由 $205 降至 $185；Wells Fargo 以 Equal-Weight 啟動涵蓋、目標價 $195；UBS 7 月上調至 $218。各來源目標價分布不一（Barchart 7 月均值 $186.12；Public.com 4 月 $171.75）","source":"Benzinga MMM price targets","url":"https://kr.benzinga.com/quote/MMM/price-targets","excerpt":null,"as_of":"2026-10-09","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-04-30 3M 與間接子公司 Fire Safety Platform Holdco 簽 14.3 億美元定期貸款＋2 億美元循環信貸（364 天期），2026-05-06 申報 8-K Item 1.01；搜尋摘要將其連到 Madison Fire & Rescue 併購。","source":"SEC EDGAR 8-K Item 1.01（2026-05-06）","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000188/mmm-20260430.htm","excerpt":"the lenders have agreed to provide the Borrower with a $1.43 billion term loan facility (the “Facility”), which is available for borrowing on the Closing Date","as_of":"2026-05-06","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露 AFFF MDL（PFAS）仍有個人、公共水system、集體成員、州政府等原告；Rome/Floyd County 集體訴訟尚未排審。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"Claims in the MDL are asserted by individuals, public water systems, putative class members, state and territorial sovereigns, and other entities.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 8-K 共 11 份，含重大項目者 3 份（含 2026-08-19 新循環信貸、2026-05-06 貸款）；清單未見 Item 4.02。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000066740&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["triggers"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"3M 2026-03-19 宣布以 19.5 億美元收購 Madison Fire & Rescue 並與 Scott Safety 合併（3M 持 50.1%、Bain 49.9%）；10-Q 稱 2026-07-01 完成。","source":"3M 新聞稿／King & Spalding","url":"https://news.3m.com/2026-03-19-3M-to-create-a-leading-fire-and-safety-business-acquires-Madison-Fire-Rescue-and-combines-with-Scott-Safety?asPDF=1","excerpt":"agreement to acquire Madison Fire & Rescue, in partnership with Bain Capital. 3M and Bain Capital will establish a new joint venture in which 3M will contribute Scott Safety, receive $700M of cash proceeds upon closing and own 50.1% of the new","as_of":"2026-03-19","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-04-30 3M 與 Fire Safety Platform Holdco 簽 14.3 億美元定期貸款，搜尋摘要連到 Madison Fire & Rescue 併購（2026-03 宣布、10-Q 稱 2026-07-01 完成）。","source":"SEC EDGAR 8-K Item 1.01（2026-05-06）","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000188/mmm-20260430.htm","excerpt":"the lenders have agreed to provide the Borrower with a $1.43 billion term loan facility (the “Facility”), which is available for borrowing on the Closing Date","as_of":"2026-05-06","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"AFFF MDL 含集體成員等原告；Rome/Floyd County 水費集體訴訟 2025-12 提出簡易判決動議，尚無審理日。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm","excerpt":"Defendants filed a consolidated motion for summary judgment in December 2025. No trial date has been set.","as_of":"2026-02-03","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 共 11 份，清單所列項目無 Item 4.02（非可靠財報重編）；搜尋亦無新 SEC 調查來源。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000066740&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["triggers"],"status":"ok"}],"gaps":[],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MMM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.4,"operating_margin_pct":20.36,"fcf_margin_pct":15.83,"rd_intensity_pct":4.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MMM","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"HON","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.57,"operating_margin_pct":16.58,"fcf_margin_pct":11.1,"rd_intensity_pct":5.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ITW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.16,"operating_margin_pct":26.5,"fcf_margin_pct":17.74,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ITW","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"EMR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.16,"operating_margin_pct":20.69,"fcf_margin_pct":18.57,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EMR","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MMM"},"financial_history":{"ticker":"MMM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":26161000000.0,"revenue_yoy_pct":null,"gross_margin_pct":39.4,"operating_margin_pct":7.32,"net_income":5777000000.0,"diluted_eps":10.18,"free_cash_flow":3842000000.0,"fcf_margin_pct":14.69,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":24610000000.0,"revenue_yoy_pct":-5.93,"gross_margin_pct":39.12,"operating_margin_pct":-43.58,"net_income":-6995000000.0,"diluted_eps":-12.63,"free_cash_flow":5065000000.0,"fcf_margin_pct":20.58,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":24575000000.0,"revenue_yoy_pct":-0.14,"gross_margin_pct":41.21,"operating_margin_pct":19.62,"net_income":4173000000.0,"diluted_eps":7.55,"free_cash_flow":638000000.0,"fcf_margin_pct":2.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":24948000000.0,"revenue_yoy_pct":1.52,"gross_margin_pct":39.91,"operating_margin_pct":19.2,"net_income":3250000000.0,"diluted_eps":6.0,"free_cash_flow":1396000000.0,"fcf_margin_pct":5.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MMM/MMM_Q3_2026_Earnings_Call_20261020.md）

# Q3 2026 Earnings Call
**3M Company** | Earnings Calls | 2026-10-20

**Operator** (Operator):
Ladies and gentlemen, thank you for standing by. Welcome to the 3M Third Quarter Earnings Conference Call. [Operator Instructions] As a reminder, this call is being recorded, Tuesday, October 20, 2026.
I would now like to turn the call over to Chinmay Trivedi, Senior Vice President of Investor Relations and Financial Planning and Analysis at 3M.

**Chinmay Trivedi** (Executives):
Thank you. Good morning, everyone, and welcome to our quarterly earnings conference call. With me today are Bill Brown, 3M's Chairman and Chief Executive Officer; and Anurag Maheshwari, 3M's Chief Financial Officer. Bill and Anurag will make some formal comments, then we will take your questions.
Please note that today's earnings release and slide presentation accompanying this call are posted on the homepage of our Investor Relations website at 3m.com.
Please turn to Slide 2 and take a moment to read the forward-looking statements. During today's conference call, we'll be making certain predictive statements that reflect our current views about 3M's future performance and financial results. These statements are based on certain assumptions and expectations of future events that are subject to risks and uncertainties. Item 1A of our most recent Form 10-Q lists some of the most important risk factors that could cause actual results to differ from our predictions.
Please note, throughout today's presentation, we'll be making references to certain non-GAAP financial measures. Reconciliations of the non-GAAP measures can be found in the attachments to today's press release.
With that, please turn to Slide 3, and I will hand the call off to Bill. Bill?

**William Brown** (Executives):
Thank you, Chinmay, and good morning, everyone. We delivered strong performance in Q3, including organic growth of 3.3%, operating margin of 26.2%, up 110 basis points, earnings per share of $2.50, up 12%, and free cash flow of $1.2 billion. We returned $600 million to shareholders in the quarter, including $400 million in dividends and $200 million of share repurchases. These results include Madison Fire & Rescue, which is now fully consolidated into our financial reporting and reflect the change in acquisition amortization reporting. Our updated guidance for the year incorporates both items, and Anurag will provide additional details later in the call.
Based on our Q3 performance and continued strong order trends, we remain confident in achieving organic growth of greater than 3.5% this year. The progress we're delivering reflects the disciplined execution of the strategy we've been implementing over the last 2 years. As we've discussed, our value creation framework is centered around 3 phases: building the foundation, driving transformation, and accelerating performance. Our results today are clear evidence that we're making progress across all 3. We're strengthening the foundation of the company and rebuilding critical capabilities to position 3M for long-term success. We've invested in sales force effectiveness and AI-enabled tools. We've sharpened our focus on priority verticals where we can win and improved how we allocate R&D resources.
Operationally, we're delivering on our goals to improve productivity, quality and supply chain performance. In the quarter, we launched 87 new products, up 24%, and we're on track to exceed our target of 350 this year. Year-to-date, 5-year new product sales are up 34% versus last year to nearly $3 billion, resulting in new product vitality in the mid-teens from a low of 11% in 2024. Cross-selling is also gaining traction with $140 million in wins booked to date and another $120 million in the pipeline, well ahead of our original $100 million 3-year goal. And in today's higher inflation environment, our price execution has been particularly strong and fully offsets material and oil cost pressures.
Across our manufacturing and supply chain network, productivity improvements, including procurement savings, higher asset utilization from increased throughput and lower downtime and improved quality drove gross margins up 230 basis points year-over-year. Cost of poor quality improved by 40 basis points, and overall equipment effectiveness improved by 20 basis points. We continue to see meaningful opportunities to further simplify and standardize, reshape the portfolio, reduce risk and improve enterprise resilience and predictability. We've closed 16 manufacturing sites and distribution centers year-to-date and are taking action on 10 more over the next 12 months, supporting further gross margin improvement beyond 2027.
And the Madison Fire & Rescue acquisition, which is now combined with our SCBA business and reported as a separate division within SIBG, is off to a good start. The JV delivered high single-digit pro forma growth and operating margins ahead of our deal model and 3M overall. And integration is well underway to capture synergies across distribution, international expansion and operational performance. And we continue our efforts to address litigation risk and are actively working with a court appointed mediator for the AFFF personal injury MDL, and more information is available in our quarterly filing.
Moving to Slide 4. I'll provide a bit more color on our end market performance. We continue to see strong momentum in general industrial and safety with second half growth accelerating to high single digits, above our prior expectations. In Electronics, we're seeing increasing strength in semiconductors and data centers, which is partially offsetting a weaker consumer electronics market, especially in LCD displays. Auto OE and aftermarket is trending in line with prior expectations with a modest improvement from down low single digits in the first half to about flat in the second and with OE a bit softer and aftermarket a bit better. The consumer business, which contributes about 20% of sales, improved sequentially to about flat in the second half as modest improvement in consumer POS spending is partially offset by channel inventory adjustments at a few specific retailers. Net-net, we still see sales accelerating in the second half and our full year above 3.5% organic.
Turning to Slide 5. Over the medium to long term, accelerating innovation across our frontier verticals, including aerospace, data centers and others will be an important driver of growth. Space materials is a great example of how we can take differentiated 3M technologies and extend them into entirely new markets. As shown on the left side of the slide, we're combining our capabilities in films, adhesives and others to solve light, thermal, energy, and weight challenges across multiple parts of a spacecraft from the satellite chassis to solar arrays. Our current pipeline supports opportunities from low Earth to geosynchronous orbits and across a range of commercial and government customers.
In Q3, we launched a lightweight reflective film for a commercial constellation to reduce light scattering toward Earth and address light pollution concerns. And we plan to launch another product in Q4 to provide a moisture-resistant barrier for solar panels. We have more than 10 other projects in development or in pre-pipeline stage that will follow in the next few years.
And on the right side of the slide, there's been a lot of interest in expanded beam optics and the opportunity ahead of us. And in light of an 8-K filing and press release last evening, I wanted to take a minute to highlight the progress we're making. As a reminder, EBO's patented ferrules technology enables faster installation, greater durability and higher density optical connections for AI infrastructure. The technology is particularly valuable in scale-out and scale across applications, including optical backplanes, where connectors at the back of a server rack can be difficult to access, install and maintain.
We previously announced a partnership and deployment with Microsoft and said we were also engaged in proof-of-concept work with 5 additional global hyperscalers, one of whom was Amazon Web Services. Last evening, we filed an 8-K stating we issued a warrant to Amazon to purchase up to 3.2 million shares or approximately 0.6% of 3M common stock based upon the achievement of $6 billion in cumulative sales of optical connectivity and other data center-related products over the next 7 years and other event-based milestones.
We also announced that we signed a contract manufacturing agreement with Genius Electronic Optical Company, or GSEO, and acquired a 4.7% stake in the company in a private placement to cement our strategic partnership. GSEO is a credible and proven supplier of premium consumer device components, and they will help us rapidly advance technology development and scale EBO manufacturing on top of our internal capacity expansion plans. But as we previously said, success in this space requires building a robust ecosystem of partners. We're actively supporting industry standardization through the EBO multisource agreement, which started with 17 members and is now up to 63. This MSA brings together hyperscalers, connectivity providers and chip designers under a common framework to establish industry standards and certify practitioners.
EBO was highlighted by many of these ecosystem partners at last week's Open Compute Project Global Summit, including by one other hyperscaler demonstrating EBO in a next-gen rack design running live traffic, and it was headlined in a recent article by SemiAnalysis, a well-respected trade journal. We believe the combination of industry collaboration through the MSA, growing ecosystem adoption and differentiated 3M know-how positions us well to benefit as EBO becomes a larger part of next-generation AI infrastructure.
Overall, we've made meaningful progress in reinvigorating our innovation engine over the last 2 years. Success requires speed and precise execution, and we're building a stronger, faster, more innovative and more resilient 3M. As this company-wide effort evolves, I'm confident it will translate into faster growth, higher margins and stronger free cash flow over time.
With that, I'll turn it over to Anurag to share the details of the quarter. Anurag?

**Anurag Maheshwari** (Executives):
Thank you, Bill. Turning to Slide 6. We delivered another strong quarter across all financial metrics. Solid organic growth, 110 basis points of margin expansion, double-digit earnings growth and robust free cash flow, all reflecting execution against our strategic priorities. Starting with the top line. We delivered organic sales growth of 3.3%, driven by general industrial and safety, both of which performed better than expected on successful execution of our commercial excellence initiatives, including pricing. We also saw continued strong double-digit growth in semiconductors and data centers as we gained traction from new product launches and good customer positioning. Together, these more than offset a weaker consumer electronics market.
Notably, the orders trend that we have seen through the year continues and grew high single digits in the quarter, led by industrial, safety, data centers, semiconductors, and aerospace. This resulted in backlog growth of high teens over last year, positioning us well for the fourth quarter. By geography, U.S. and Canada grew approximately 7%, the highest we have seen since the pandemic. Industrials grew double digits as we executed well on pricing, cross-selling, and sales effectiveness in a constructive market, which more than offset a soft consumer market. Latin America grew high single digits with broad-based growth across all 3 businesses. It was encouraging to see Europe grow for a second consecutive quarter despite a soft auto market.
In Asia, we had positive growth and saw another double-digit quarter in India as we increased penetration in automotive, industrial, and a growing consumer market. Overall, we grew in all regions except China, which was down high single digits on weak consumer electronics demand. As Bill mentioned, following the Madison acquisition starting this quarter, we now exclude the amortization of intangibles from adjusted results to better reflect the underlying performance of the business. Historical recasted financials for '25 and first half '26 are shown on Slide 13. And as you can see, have an impact of about 40 basis points to margin rate and $0.04 to EPS per quarter.
For Q3, adjusted operating margin was 26.2%, up 110 basis points with the 3 business groups up 140 basis points, partially offset by 30 basis points from corporate as expected. Operating profit increased $140 million with $260 million from sales growth and productivity, particularly in supply chain, partially offset by about $120 million of stranded costs and investments. The $0.27 of EPS growth was driven by $0.22 of operating profit growth and $0.05 of below-the-line items, including a lower share count net of a higher tax rate, resulting in adjusted EPS of $2.50, up 12% year-on-year. Q3 GAAP EPS was $2.63, up 70% year-over-year. This included the impact of costs from ongoing transformation actions, exit of certain PFAS manufacturing assets and gain from change in value of our Solventum ownership. Free cash flow was $1.2 billion in the quarter as higher earnings were offset by working capital timing, which we expect to reverse in the fourth quarter. 
Turning to the next slide, I will provide a quick overview of our growth performance for each business group. Safety and Industrial delivered another standout quarter with 7% organic sales growth, driven by the continued expansion of commercial excellence initiatives and the ramp-up of new products. Electrical Markets division continued to grow double digits as they deepened penetration with key customers in the data center market. Safety, industrial adhesives, abrasives, and industrial specialties collectively grew high single digits, driven by targeted commercial initiatives to reduce customer churn, expand sales coverage, increase sales effectiveness and drive cross-selling. Though repair claims market remains soft, auto aftermarket grew mid-single digits, driven by the new products and wins with large multi-shop operators. Year-to-date, SIBG sales are up 6.1% and importantly, orders and backlog are up double digits, giving us good visibility into the fourth quarter.
Turning to Transportation & Electronics. Third quarter sales grew 0.5% due to weaker-than-expected consumer electronics, which was down mid-teens. Outside of consumer electronics, the business grew about 5% across semiconductors, aerospace, commercial branding and auto. In addition to data center and semiconductor, aerospace grew double digits, driven by continued strength in defense, sustained civil aviation build rates and growing demand for space films. Commercial branding continued its first half momentum, growing mid-single digits, driven by graphics and personal auto demand, while auto was down mid-single digits on softer builds. Despite the weak consumer electronics and auto market for the first 9 months, TEBG sales grew 2.1%, with orders up high single digits and backlog up double digits, supporting acceleration in the fourth quarter. SIBG and TEBG, which together represent 80% of our business, delivered about 4% growth in the quarter and 4.5% year-to-date.
Finally, consumer was flat in the quarter, improving sequentially as the rate of decline in the U.S. moderated, while international continued to grow mid-single digits. U.S. point of sale grew over 2% through the quarter, but continued inventory adjustments at a few large retailers resulted in U.S. sell-in being down low single digit. As retailer inventory stabilize and POS continues to show positive momentum on the back of NPI and retailer-specific programs, we expect the growth trend to improve in the fourth quarter. Overall, we are delivering on our commitment with strong year-to-date results, including organic sales growth of 3.3%, operating margin expansion of 60 basis points to 25.2%, earnings growth of 12%, and free cash flow of $3.1 billion. Year-to-date, we returned $4.4 billion to shareholders, including $1.2 billion in dividends and $3.2 billion in share repurchases.
Please turn to Slide 8 for an update on our '26 guidance. Order momentum, a healthy backlog and easier comparisons give us confidence in organic growth of just over 4% in the fourth quarter, keeping us on track for more than 3.5% for the full year. On the back of strong year-to-date performance, continued momentum and focus on productivity, we are raising our earnings guidance from a range of $8.95 to $9.10 on a new basis to a range of $9.10 to $9.15, or $0.10 above the midpoint, resulting in growth between 11% and 12% for the year. On oil, we now estimate the inflation impact of $185 million, up from the $150 million to $175 million range we communicated in July. We expect to fully offset the increase through disciplined execution of the pricing actions we implemented in the second quarter. While this pass-through is dollar neutral, it dilutes margin rate by about 20 basis points, which we will mitigate through better productivity. For the year, we expect margin of about 24.6% on the new basis, in line with our prior expectations. Free cash flow remains at approximately $4.8 billion and adjusted tax rate at about 20%.
Turning to Slide 9. We will provide formal 2027 guidance in January, but our framework to drive profitable growth remains consistent and are confident that we will exceed all of our Investor Day targets. We expect good growth in line with our second half exit rate with more contribution coming from new product launches as we sustain commercial excellence, including pricing discipline. Alongside growth, we will continue to drive productivity largely from supply chain and transformation actions as we more than offset investments and stranded costs, resulting in margin rates exceeding our Investor Day target of 25.4% on the new basis.
For EPS, we expect operational performance to be the primary driver of earnings growth like this year. Nonoperational performance will be influenced by changes in interest rates and FX, while the tax rate should remain stable and share buybacks will continue to be accretive. Finally, we expect robust free cash flow driven by earnings growth and working capital improvements and will continue disciplined capital deployment. Having returned $9.3 billion since the start of 2025, we are well on our way to exceeding the $10 billion target. 
Before we open the call for questions, I would like to thank the 3M team for their commitment, resilience and responsiveness to drive value to all our stakeholders. Our performance to date and opportunities ahead provide us with increased confidence in delivering on our updated 2026 guidance and exceeding the commitments we laid out at Investor Day.
With that, let's open the call for questions.

**Operator** (Operator):
[Operator Instructions]
Our first question today comes from the line of Scott Davis with Melius Research.

**Scott Davis** (Analysts):
I want to ask about Amazon in a second. But before I do that, you mentioned price several times. And is it easier to get because inflation is so well telegraphed that the customer is extraordinarily well aware of what's going on out there? Or is it the new product introduction side of it that is kind of driving that? And you still seem to be a little bit -- I mean, behind PPI. So do you see an acceleration there?

**William Brown** (Executives):
So Scott, good question. I mean we -- first of all, it is pretty well publicized in the marketplace around what's happening in oil and gas prices and general inflation. I think that's well covered. But I think our ability to drive price right now is partly from the new products. I think importantly, it's from just significantly better responsiveness, service delivery rates, product availability that we're delivering to our customers. And I think that is -- that's a very important part of it. And I wouldn't discount that we're being, I'd say, a bit more aggressive here on price, holding our ground on this one.
So I think all of those things come together and what's driving price. So we'll see ourselves for the year to be slightly above 1.5%. We were saying last time about 1.5%. It will be a little bit better than that because oil price continues to come up. Back half of the year will be slightly above 2%, front half was 1%. So we're doing better. We're executing well on price. We're covering material and oil cost inflation, and we feel pretty good about the trajectory we're on right now on pricing.

**Scott Davis** (Analysts):
Okay. That's helpful, Bill. Look, it wasn't clear to me in the 8-K what Amazon is -- I mean, we know the investment they're making, but are they helping to pay for capacity or take-or-pay contracts, anything that kind of locks them into derisking a bit of your capacity adds?

**William Brown** (Executives):
So look, it's a very, very important step we've taken here with Amazon. There's no disclosure right now on other parts of the commercial agreement, but it's been in the works for some time. It's a very important strategic commercial relationship. I do believe it's a validation of the technology. It's an important milestone in this broader relationship that we've had with Amazon. It's very clear in the agreement that it's for optical connectivity, EBO and other data center-related products. They do have faith in our broad material science capabilities for acoustics, vibration, thermal kind of things inside the data centers. And -- so we're very excited about where we happen to be. As you note, it's -- there's at least something in the 8-K. It's cumulative $6 billion is where the warrant vests over 7 years. It's an increment. It's not ratable. It will start to ramp towards the back end of next year is what our expectation happens to be and become more meaningful as we get into '28.
But as we sit here today, that's as far as I think we'll be able to disclose as this continues to ramp. What's important right now is we execute well. We scale well here with Amazon. We build out the ecosystem, which they and other hyperscalers believe is very important. So a very important step is combining that with the GSEO announcement where we have solidified the supply side, the ramp-up we expect to get to support Amazon and other hyperscalers. So collectively, we think it's a very important milestone that we're at today on EBO.

**Operator** (Operator):
Our next question comes from the line of Amit Mehrotra with UBS.

**Amit Mehrotra** (Analysts):
Bill, the trajectory of organic growth has been good, plus 1% in '24, plus 2% in '25, plus 3.5% at least this year. You're making a lot of progress on pricing and NPI. Now you're maybe leaning into some growth verticals through these sort of creative solutions, which is fantastic. But I guess the question that everybody is asking is where do you think this ultimately goes to from a through-cycle growth perspective because you've got a consumer business that's a little bit more difficult. T&E is obviously a little bit difficult. Maybe just talk about not just '27, but if you want to talk about '27, great, but sort of where you think structurally you're taking the growth algorithm for this business over the next 1, 2, 3 years?

**William Brown** (Executives):
So I mean, you went through some of the numbers. I appreciate you doing that and recalling the trajectory we're on. It's a pretty broad portfolio. Not everything kind of flows positively every quarter, but you've laid out appropriately the steps that we're taking to drive organic growth in the company, something I think we've struggled to do over time. It comes back with -- back to what we are focused on very originally was around reinnovating -- innovation and driving new products to the marketplace, and we continue to progress that very, very well and is becoming more impactful. We're clearly driving a lot of commercial excellence activities, improving our capability at the front line, building a better relationship with our channel partners, more cross-selling, better performance, so we have less churn, pricing.
I mean all these things come together to kind of make this machine run better, and you went through the numbers. So we'll end the back half of the year will be close to 4%. Q4 will be touching just over 4%. As we look into '27, we continue to see growth momentum here. There are some economic tailwinds here on the industrial side. We feel pretty good about that. But more importantly, this is a self-help story. We're showing that we can grow organically even in a choppy macro environment and drive margin expansion quite substantially. So the combination of what we're trying to do, I think, is what's really turning this 3M Company around. And I'm very, very excited about where the future holds here.

**Amit Mehrotra** (Analysts):
Okay. And then, Anurag, if I could just have a follow-up because if we go back to Investor Day, there might be sort of $400 million to $500 million of extra costs that you guys have incurred since Investor Day, whether it's tariffs or oil inputs. And here we are, not only are you offsetting that with price, but there's obviously clearly productivity there because the margin, you're raising the margin guidance for longer term next year. So can you just talk about productivity? Because the '27 framing is helpful, but it's a little bit vague relative to what you did last year. Are we going to get $500 million, $600 million more of net productivity next year? Do you still expect 35% incremental margins on the growth you expect to achieve? Maybe fill in some of that color for us, please.

**Anurag Maheshwari** (Executives):
Okay. Thanks, Amit. And you're absolutely correct. At the Investor Day, what we laid out was that we had about $300 million of stranded costs at that point in time. But since then, we've had tariffs of about $280 million. We have oil now, which is $185 million. We obviously were able to offset all of that plus more, which is why we are ahead in terms of our margin expansion so far and will be next year as well. So as Bill mentioned, we're going to exit the year close to about 4% in terms of organic growth. And as we go into next year, that will accelerate because of new products, commercial excellence and pricing, which we've done a very good job this year and continue to kind of sustain that next year and drive for more pricing to offset oil.
So with the volume growth on the margin side, we have good incrementals. Historically, we said it's between 30% to 40%. I think we are more closer to the 40% right now in incrementals given the progress that we made over the past couple of years. I'll combine that with productivity on both supply chain as well as some of the transformation actions we are taking, and it should continue at the same rate as it has over the past couple of years. And while we drive volume with high incrementals, productivity will much more than offset the step-up in investments and stranded costs. So we expect good margin expansion as we go into next year and feel very confident to be ahead of the 25.4% the new Investor Day target despite all the other headwinds we had. So feeling pretty confident.

**Operator** (Operator):
Our next question comes from Joe O'Dea with Vertical Research Partners.

**Joseph O'Dea** (Analysts):
I wanted to start on just sizing of EBO. Can you talk a little bit about where you expect the revenue to be this year? How much revenue your current capacity can support? And then with the manufacturing collaboration that you've announced, how much revenue altogether you think that will be able to support?

**William Brown** (Executives):
So Joe, look, for this year, EBO is in the $40 million range, plus or minus. We've got another quarter to go here. We do expect that to ramp considerably next year, likely will double. It could be maybe a little bit better than that depending upon progress through the year. Internally, we have doubled our manufacturing capacity. So we'll be north of, say, 10 million ferrules a year. It will be a little bit better than that. We expect to increase that over time. The contract manufacturing agreement with GSEO, given their size and what they currently do for consumer devices in similar spaces, they could do potentially multiples of that per month. So I believe if we scale them as we know we will over the course of the fourth quarter into early next year, that we will see our ability to actually satisfy the market demand. 
So hopefully, it's not a capacity issue. It becomes more in comfort of hyperscalers. It's developing the ecosystem. And I just want to reiterate one of the key factors here is making sure we have diversity of supply, not just from 3M, but other partners here because that's going to be quite important for hyperscalers to sell on -- to sign on. So I believe with GSEO, we'll be in pretty good shape to scale to the market requirements as we see them now.

**Joseph O'Dea** (Analysts):
And then on just current demand tracking, can you talk a little bit about what you saw over the course of the quarter into this month with respect to acceleration, any caution? There's a tremendous amount of focus out there just given kind of all the headlines and any risk that, that poses for pause. And so kind of overall macro, how you've seen demand trends over the course of the last several months?

**William Brown** (Executives):
Okay. So look, for us, I mean, our order rates have been pretty good. We -- for the quarter, they were up about 7%. We see good backlog going into the fourth quarter year-to-date, a little bit better than 8%. It's better on the industrial side, but generally good order trends, good momentum here as we head into the back end of the year. So just from a macro perspective, we continue to see the broader industrial markets improving, especially in the U.S. And I know that part of it is driven by data centers, but it's quite a lot of other factors that go behind that. Auto build rates are likely to be down. They're down modestly in the quarter and likely for the year as well. We see the consumer electronics space worsening a little bit in the back end of the year, more like down mid-teens from the consumer electronics market. Those are the broader pieces. IPI is about where we were before, slightly better globally. U.S. IPI, U.S. GDP is slightly better from where we thought in July.
So that's getting, I'd say, a little bit better. And those are the key pieces. The U.S. consumer is sort of still a little bit soft, although what I would say is we continue to see good POS growth, which is sellout for us. It's north of 2% growth on POS, which is pretty good. So I feel it's getting at least more stability in the U.S. consumer behavior, if not maybe a little bit of improvement. So overall, I'd say the industrial is pretty good kind of mix outside of that.

**Operator** (Operator):
Our next question comes from Julian Mitchell with JPMorgan.

**Julian Mitchell** (Analysts):
Maybe I just wanted to follow up on the TEBG revenue outlook because that's where you've seen, I suppose, the most volatility in recent quarters, strong growth Q2, it evaporated in Q3. You're talking about a reacceleration in the fourth quarter despite a worsening consumer electronics market backdrop. I think you said down mid-teens. So please sort of flesh out a little bit the confidence in that TEBG acceleration? And is it something where it's just month-to-month that the numbers are kind of swinging around in that business?

**Anurag Maheshwari** (Executives):
Sure. So as we exited the third quarter, Julian, the backlog in TEBG was up quite double digit. So that gives us good visibility as we go into the fourth quarter. You are correct about the consumer electronics being pretty consistent between third and fourth quarter. But where we do see is the good backlog getting converted plus continued strength in the aerospace, defense, the semiconductor, and data center, which continues to accelerate in the fourth quarter, plus all the commercial excellence that we are driving in the commercial branding business. This, along with auto, we've had some couple of good wins in auto as well that kind of coming through. I think gives us confidence that we will accelerate the growth in the fourth quarter -- from the third quarter in TEBG.

**Julian Mitchell** (Analysts):
And then just my follow-up. I think, Anurag and Bill, your tone on the margin expansion is very confident, I think, looking at Slide 9, and you're talking about very likely exceeding that 80 basis points of sort of margin expansion next year that's guided on that Slide 9, and that's even with what's going on with cost inflation and everything else. So I suppose, is the sense that -- I think right now, in the second half, operating margins are growing about 100 basis points year-on-year in the guide. Is your sense that, that's a fairly sensible sort of run rate for the time being given inflation and productivity and stranded costs and so forth. There's nothing sort of onetime benefiting the degree of margin expansion you're seeing today?

**Anurag Maheshwari** (Executives):
Correct. There is no onetime benefit in terms of the margin expansion. It's all about controlling our cost base, driving productivity across both supply chain and G&A. Bill did mention in his prepared comments about gross margin being up 230 basis points, really good work around all the buckets being the cost of poor quality, which was better by 40 basis points, driving more productivity and automation in the factories that we have today and even in this environment, driving procurement savings. So I think it's all fundamental drivers in terms of expanding our margins.
As we go into next year, you are right, we said we had $300 million of stranded costs. We had $100 million last year, $150 million this year, incremental $50 million next year. But just on where we are in the momentum in terms of supply chain and making some structural cost changes, I think we are confident on continuing the productivity into next year as well.

**William Brown** (Executives):
Yes, Julian, I think the thing to keep an eye on is as we keep talking more about transformation and the changes that we're making, a lot this year has been around G&A. There's been investment to transform the G&A functions. It's starting to occur within our supply chain network and data center and distribution center network as well. I talked a little bit about some of the changes there. That's going to be impacting us into '27. And certainly, with the factory consolidation, given they typically be -- would be 3-, 4-, 5-year payback, that will start to become more meaningful in 2028. So when you take a step back and think about all of the work that we've done, we've seen gross margins come up from the low 40s to now touching close to the mid-40s again, up to potentially the high 40s over the next 4 or 5 years through some of the transformation that's happening.

**Operator** (Operator):
Our next question comes from Andrew Obin with Bank of America.

**Andrew Obin** (Analysts):
Just a question on Madison Fire. Just are we putting -- now that it's organic, are we putting any accretion into '26 on that just from a modeling perspective, do I need to sort of put something in?

**Anurag Maheshwari** (Executives):
Yes. It's EPS neutral to us. I mean it does grow higher than company average and margins is better, but it's -- given the size of the business, it doesn't really move the needle much on the top line. That obviously comes with operating profit, but there's a step-up in interest because of the leverage and NCI. So overall, it's EPS neutral for this year and next year.

**Andrew Obin** (Analysts):
And just going back to sort of optical and data centers. The headline numbers, I think, in the 8-K are pretty robust, and you're saying you have multiple other hyperscalers that you're talking to. Just order of magnitude relative to what you have, how big could that be? And could you also remind me overall, what was your exposure to data centers last year? And what is it this year?

**William Brown** (Executives):
So just on that last part, I mean, data center this year will be about $700 million, last year was around $550 million in that range, part outside. The bigger part would be outside, so electrical connections and part is inside around optical connections, copper, other parts with inside the data center, but most of it was on the outside. Yes, there's been a lot of conversations with really all of the other hyperscalers. Obviously, Amazon is quite substantial in that space. So that's a very important one. You recall last quarter, we talked about a strategic partnership we announced with Microsoft, where they'll be using EBO in Azure data centers.
These things will continue to evolve. Again, we've got to continue to work the ecosystem, build the scale, continue to advance the technology because each hyperscaler has some uniqueness in their configuration and architecture. So there's some work that has to happen there. But I think we're -- we have very, very good momentum here. I think this was a very important step that we've taken in the last couple of days with Amazon. And I hope in the coming months, others will follow suit.

**Operator** (Operator):
Our next question comes from Joe Ritchie with Goldman Sachs.

**Joseph Ritchie** (Analysts):
So Bill, I just wanted to follow up on that thread, right? The warrants are a pretty unique structure. I'm just curious, like how did that even come about? And then also, I think you just mentioned that you're hoping that potentially some of the other hyperscalers will follow suit. Just any other clarification around that would be helpful.

**William Brown** (Executives):
So at this conference last week, it's the Open Compute Project, which is in San Jose. I was on the West Coast and had a chance to walk around the show for a few hours and there are many other hyperscalers and a lot of ecosystem partners that were there. There's a lot of conversation around EBO, how it can be used, how it can be scaled, how do we manufacture it, partners that want to be part of it. So it's -- there's just a ton of activity happening there. So it's pretty broad-based. But again, it's evolving. I mean each quarter, each month, we're taking steps forward here. We have to keep executing and doing all the things that I've been very carefully talking about around scaling and technology development and ecosystem. All of these things are critically important.
For Amazon, look, I think the warrants conversation is really important because it cements what I believe is a very strong strategic partnership we have with Amazon. And it's an agreement. It's a union, if you will, with Amazon, where we both see win-win. We see opportunity to drive shareholder value on both sides. For us, the warrants are going to be accretive to significantly accretive to the company. So we thought that was prudent and the right thing to do. Again, it's about 0.6% of our shares. So it's not hugely meaningful, but in terms of -- it's very symbolic in terms of the overall relationship we have with Amazon.

**Joseph Ritchie** (Analysts):
That's helpful, Bill. And then I guess just my follow-up question, Anurag, you gave some parts in the framework for 2027 to see the expectation for the -- for at least 80 basis points of margin expansion. Is there a volume assumption that you're embedding? I know that you guys typically will kind of like model to trends. Just any expectations on volumes already for next year?

**Anurag Maheshwari** (Executives):
Yes. Yes, Joe, absolutely. As I was mentioning when Amit was asking the question that the volume, which typically has been a 30% to 40% incrementals for us is now getting closer to the 40% incremental. So there will be uplift from volume plus productivity, and both of them combined will drive the margin expansion for next year.

**Operator** (Operator):
Our next question comes from Nigel Coe with Wolfe Research.

**Nigel Coe** (Analysts):
Great. So just going back to the Amazon agreement. So is this a framework agreement, Bill, that's structured as a minimum -- the $6 billion is very specific. So is that a minimum purchase agreement over that 7-year time frame? And you seem to indicate that next year is more like $100 million or so of revenues from EBO. Should we then expect that to step up to close to $1 billion in 2028? Just trying to sort of frame expectations here.

**William Brown** (Executives):
So look, I think we'll sort of get through the quarter here, and then we'll go through next year. Your numbers next year, around about right. I mean it's sort of $80 million, $100 million of EBO. I mean, again, look, we've got to continue to execute and scale here. We're not going to size it beyond that. But when we talked last time, we said the total addressable market here for EBO is around $2 billion in the '28 time period. That this year, we'll do, again, $40 million roughly. This is an important initiative for us. We're maturing the technology. I think this step with Amazon, last quarter with Microsoft, others that are in conversation gives us a greater right to win in that space.
So I feel better about our ability to go after that market. We believe it will continue to grow over time as people get comfortable with EBO with a contactless sort of connection device as opposed to physical contact point-to-point devices today. So I think it's going to continue to evolve, but I won't comment on anything beyond '27, but I do believe it's going to continue to grow and grow meaningfully. Otherwise, we wouldn't have talked about where we happen to be with Amazon and the size of the contract manufacturing agreement with GSEO. All these are very important to us.

**Nigel Coe** (Analysts):
Yes. Yes, $6 billion divided by 7 is close to $1 billion. That's why I just thought I'd throw it out there.

**William Brown** (Executives):
There's no volume commitments here. It's a -- we got to earn a right to that. It's going to happen over time. But that's what -- that's the number they put out there is what is expected over the course of the next 7 years. So we think that's an important target for us.

**Nigel Coe** (Analysts):
Okay. And then just, Anurag, maybe for you. The S&I margins were very strong this quarter. Looking at the NCI line, it looks like the contribution from Madison Fire was very strong this quarter. I'm getting to math closer to $100 million of EBITDA contribution, which feels too high. But just wondering what kind of margin Madison Fire is coming in at? And what's a good number for 2027?

**Anurag Maheshwari** (Executives):
Yes. So Nigel, I would say the number is not that high as you're citing it out to be. The margins are -- we finished the quarter at 26.2% margins. They are a little bit higher than that, I would say. But that does get offset on the NCI line. So overall, it was EPS neutral to us. So the NCI was just a couple of pennies compared to last year. So it was not close to that. And as you model into next year, I would say it's again going to be EPS neutral. There will be incremental $200 million of revenue coming from Madison. You can assume a margin rate higher than the company, and the offset will be high interest in NCI.

**Operator** (Operator):
Our next question comes from Steve Tusa with Wells Fargo.

**Charles Stephen Tusa** (Analysts):
As far as the fourth quarter is concerned, can you maybe -- I know it's -- a couple of these businesses you said are going to accelerate, and that's great color. But maybe just how you're seeing things play out versus normal seasonality? Maybe seasonality really is like there is no normal seasonality with the last few years, but how you're thinking about those kind of daily sales trends? And then just lastly on that, the backlog, you mentioned the backlog was up. Maybe just a little more color. I think you gave some in the second quarter.

**William Brown** (Executives):
Yes. So look, Q4 typically is a lighter quarter, but there's nothing unusual about seasonality here in the fourth quarter. We do see it being up with the 4% that would get you to greater than 3.5% for the year. So it's got to be more than 4%. Again, it's off of a bit of an easier compare. The prior year in Q4 was a little bit softer as opposed to Q3. We had a tougher compare here in Q3, but it gets a little bit better in Q4. Look, we've had just, again, very good order trends. The backlog going into the quarter is up about 18%. So it's high teens percent year-over-year going into the quarter. We have about 25% of the revenue that's in backlog, which is pretty good and a little bit better than we typically see. So -- but again, based on where we see it today, we feel pretty good about coming in north of 4% more than 3.5% for the year.

**Charles Stephen Tusa** (Analysts):
And then just one last one on stranded costs still. Is it still -- and investments, is it still $375 million for the year? And does that step up a little bit? I know it was up $0.17 in the quarter. Does that step up a bit in the fourth quarter?

**Anurag Maheshwari** (Executives):
Yes. So I believe when you said $375 million, you meant $225 million of investments and $150 million of stranded costs for the year, Steve? It's probably what you're referring to?

**Charles Stephen Tusa** (Analysts):
Correct. Yes, correct.

**Anurag Maheshwari** (Executives):
And it is still the same. And in the fourth quarter, you have probably $125 million of that because of the $50 million of stranded costs and $75 million of investment. So no real change from the cadence that we had laid out from the beginning of the year. And that stranded cost next year is $50 million. It goes from $150 million to incremental $50 million.

**Operator** (Operator):
Our next question comes from Andy Kaplowitz with Citigroup.

**Andrew Kaplowitz** (Analysts):
Bill, can you give a little more of an update on your overall progress in innovation as we start thinking about '27? I think you previously have mentioned your cycle time of innovation target is at least 20% better. But can you use tools such as AI to push greater innovation much faster and with better margin? I think you'll do greater than 350 new products you just said. But you've also said that 3M used to do 700, 800 per year. Can you get back to those levels faster than you thought and with greater improvement in design to cost?

**William Brown** (Executives):
So look, first of all, yes, I'm very pleased with what's happening right now on NPI innovation. We're accelerating. I gave some of the numbers here, about 87 in the quarter, up about 24%. For the year, we'll be at 350 or more. So that would be up 23% year-over-year. Early last year at the Investor Day, we said we would be 1,000 products over 3 years, and we should be above that was what my expectation would be. I think what's important is we've seen the funnel remain very, very healthy. So we're bringing more projects into the funnel, into our development pipeline that we're launching. I think that remains very, very encouraging.
Cycle time has been pretty good, actually. We are -- we will be down 20%. It will move around a little bit, but I think we've already proven that so far. But as we bring more Class 4s, Class 5s into the funnel, which will drive more incremental growth over time. They're a bit of a longer development cycle. So that could push things a little bit in the other direction. But the cycle time continues to come down. Our on-time launch attainment remains around 80%, 81%. So that's all very, very good.
As you mentioned about AI, look, I do believe that this is going to be a meaningful way for us to accelerate innovation. Again, from 20% compression on cycle time, just by bringing AI in, you're ideating faster, you're eliminating some of the steps of developing and making prototypes in labs, getting out to a factory. So instead of doing physical prototypes, you could do virtual modeling and simulation. All those opportunities are happening now. So that could further compress cycle time. And what that means is we should be accelerating the numbers of new product launches without accelerating the cost to go and make that happen.
So I'm very encouraged. We're pushing very hard on this. A lot of the effort to date has been codifying this vast treasure trove of information that resides at 3M in terms of all of the patent information, all the technical papers, all the material specs, safety sheets, all of this process informatics, all the -- how you make it, it all needs to be codified. That's now being done. And when you have all that and you lay AI on top of that, it can really accelerate our journey in bringing new products to market. So I'm encouraged about the progress we're making here. And to your point, I think there's a great opportunity to accelerate that into '27 and beyond.

**Andrew Kaplowitz** (Analysts):
That's helpful, Bill. And maybe just delving a little bit more into consumer. I know you said point of sales has continued to improve, but consumer, as you know, has been a bit slow to turn. Do you see a more definitive turn coming in that business? Or can increased self-help drive a more definitive turn? And you mentioned still some select retail destocking. So maybe a little more color on what you're seeing there.

**William Brown** (Executives):
So yes, I mean, consumer, we expect will turn slightly positive in the back end in the fourth quarter of the year. Of course, we thought Q3 was going to be positive. It didn't happen. But we're on the right trajectory here. It's not necessarily going to be a big driver of growth for the company given its size and where we expect it to be in the fourth quarter. But the trends are positive. POS was kind of basically up a little bit in Q1, improved a bit more in Q2, around 2%, 2.2%, a little bit better in Q3. So POS has been pretty good. What happened over the course of this year is the inventory in the channel, especially with a couple of retailers has been pulled down a little bit, about half a week in Q3. It was about half a week in Q2. We find that to be stabilizing here a little bit going into the fourth quarter.
But again, these are -- it's hard to predict what some of these retailers are going to do. But when we take a step back and look at the way the portfolio is evolving, we see it to be slightly better in Q4, but again, not a big meaningful driver for the growth of the company. One of the things that's interesting is, I mean, the international has been pretty good. So even why -- the business is mostly U.S., about 70%, but international for us has been up mid-single digits and the trends there continue to be pretty strong. So I think if we put all together, U.S. can improve and international holds in at mid-single digits, we can actually be positive in the fourth quarter.

**Operator** (Operator):
We'll go next to Varun Govindaraj with Bernstein.

**Varun Govindaraj** (Analysts):
Quick one from my end. You had a leadership change on the R&D side with John retiring and Tushar coming in. How are you sort of driving continuity in the R&D strategy with that change just because I mean these kinds of changes during transformations are tricky. So curious how you're handling it?

**William Brown** (Executives):
So Varun, thanks for the question. I mean, look, John was here for a number of years, close to 30 and was CTO for quite a long time and was a fantastic partner to be in reestablishing, reinvigorating innovation. Tushar has been with the company for 25 years. He's a PhD. He's got a lot of experience both running the business as well as developing technology, more than 40 patents to his name. And I like the combination. He's been running the IATD business within SIBG for the last number of years, leaning forward on AI, digital tools. I think that combination is going to be very important to us. And having somebody that knows the players internally, know the technology and importantly knows our customers, that combination, I think, will drive good continuity in what we're trying to do on innovation at 3M.

**Varun Govindaraj** (Analysts):
Super helpful. And then just as a quick follow-up. We've talked a lot about EBO sizing, but you've also flagged stuff like the Nextel ceramic fibers, space got a lot of real estate in today's presentation. Any rough sense of how accretive that could be either next year or do we sort of expect that to come in more 2028 onwards?

**William Brown** (Executives):
No. I mean we think '27 will be a step up on that. So it's a couple of different things. We continue to see very good growth in our Electrical Markets division with connectors, medium voltage connection coming into data centers. That has been a good grower for us all year, double digit, and we see that continuing into next year. But there's a lot of other different technologies, you point out Nextel, which goes into a couple of different behind-the-meter type solutions outside the data center. And we are -- we continue to have momentum there. We're expanding capacity to meet the demand of that space. So I think that could be a step up into '27 and perhaps even better than that in 2028. So I think very good momentum, both inside as well as outside the data center, Varun.

**Operator** (Operator):
Our next question comes from Brandon Knutson with Morgan Stanley.

**Brandon Knutson** (Analysts):
You guys have been highlighting new product introductions. Can you quantify for us a little bit how much better pricing or margins are on these new products? And how high you think you can get that NPVI over time?

**William Brown** (Executives):
So we haven't really talked much about what we do on pricing. I mean sometimes when you bring new products, it's creating a new space. So you really have a good vantage point. But I think our ability to drive value-based pricing is becoming a lot better. We see it across a number of different product portfolios. So I would say when we bring in new products to the marketplace, once you start to hit volume ramp, we do see margin -- those products being margin accretive to the company. So price is an important part of that.

**Brandon Knutson** (Analysts):
Great. And then last one on just data center. EBO has got a lot of focus. I know the production capacity has been important there and the GSEO deal will help with that significantly. What else is key to the ecosystem to drive growth here? And then outside of EBO, how do you see your other DC content scaling?

**William Brown** (Executives):
So we provide -- we manufacture a ferrule. The fibers have to be terminated into the ferrule. They have to be put into a connector and then installed in the data center. So all those pieces are quite important. But hyperscalers have an important -- they design their own architecture, the server -- designer server manufacturers have views of where they're taking their product line, how they're shifting from copper to optics over time. So all of those various pieces, you've got to work with that broad set of players to establish EBO and then to grow it. So that's what the MSA is really for. It's developing standards and then certifying players in the space to install EBO. So that needs to happen side-by-side with technology development and scaling.

**Operator** (Operator):
Our next question comes from Nicole DeBlase with Deutsche Bank.

**Nicole DeBlase** (Analysts):
Maybe I'll just ask one since I know we're at time. Just wanted to dig in a little bit more on consumer electronics and understand what's going there with respect to -- going on there with respect to memory. But I guess, Bill, when you kind of look out into 2027, are there any green shoots that make you feel like maybe this business could turn positive again? Or is that being too optimistic?

**William Brown** (Executives):
Yes. So consumer electronics, yes, it was -- we've seen some pressure here in the quarter. We'll see some additional pressure going into Q4 as well in consumer electronics. I mean we do in consumer electronics, we provide films for -- primarily for LCD displays. We do conductives. We do OCA e-bonding a lot for phones and tablets, notebooks, et cetera. We're primarily a premium player here. So 70% of our business roughly is with premium device manufacturers. Overall, I'd say we're tracking kind of in line with or maybe slightly better than the market. We've seen pressure in 2 particular areas. One is in LCD displays. That's one area.
And the other is with China OEMs, not a very big part of our business, but that market is down quite substantially in the quarter and then for the year. So -- but we're performing very well with premium device manufacturers where performance, where thermal management for AI devices, for foldable devices, for all these new innovations, we're performing very, very well there. And as I look forward, that kind of innovation with those premium manufacturers, I think, will allow us to return to growth going into next year and beyond.

**Operator** (Operator):
Our next question comes from Brett Linzey with Mizuho.

**Brett Linzey** (Analysts):
I want to come back to Slide 5. So on the space portfolio. I was hoping you could put a finer point on the TAM or anything you can share regarding content opportunity per satellite? And if there's any constellations or customers you're currently spec'd in on or working on designs.

**William Brown** (Executives):
So we can't talk about the latter part of that, which is who we're getting spec'd in on. But I was very careful and I said it's a pretty broad space. It's both -- it's LEO and GEO. It's low Earth orbit, geosynchronous orbit, commercial customers, some government contracts we're working on. But it's a broad opportunity for us. And you can see some of the challenges here. It's around how do you lightweight these satellites, build more capability, bring more protection. So there's no light reflecting back to the earth, removing a glass solar panel as they get bigger with -- they replace it with films that allows it to work to be a lot lighter.
So there's a lot of capability here. Our content is growing in that space. Our innovation, I think, is quite important. But we expect that, that's going to grow over time, which is why we want to keep highlighting it. So I don't want to say too much more than that, but it's a great opportunity for us to grow our business.

**Brett Linzey** (Analysts):
I appreciate the detail. And then just a quick follow-up on the $185 million of oil inflation, you said fully offset by price. Is there a carryover lag into '27 we should be thinking about or modeling? And then how much of that price is go get versus in the market a little bit more surgical?

**Anurag Maheshwari** (Executives):
Yes. So we should -- we implemented the price increase starting May this year, and we started seeing the increase in our cost probably a month earlier than that. So you should see about some carryover going into next year, definitely on the oil cost piece. And at the same time, you should obviously see the price carryover. So we will be neutral between price and oil cost for next year. And the strategy was actually to be a little bit more surgical. It wasn't a peanut butter spread across the entire businesses. It was looking at areas where there was either higher cost or where some of the peers were going out with price increases, and that's what the team did. And I think we did a very, very good job by offsetting it. Last year, tariff, we did not offset the entire price increase. But over here, we did and the discipline has been really, really good.

**Operator** (Operator):
Our last question comes from Jeff Reive with RBC Capital Markets.

**Jeffrey Reive** (Analysts):
I'll keep it to one question. And on the EBO business, if the 4 hyperscalers currently in proof of concept convert, is the combined internal plus GSEO manufacturing footprint sufficient? Or should we expect further capacity investments?

**William Brown** (Executives):
No, it should be sufficient. But again, it gets back to this diversity of supply. So we are scaling internally, but we'll never be able to within 3M to be able to accommodate the market demand. GSEO has incredible capacity. But likely over time, there'll be -- there may be other players here, other manufacturing sources that just give that satisfaction of diversity of supply. So we're confident we can ramp with GSEO, but there may be others that we have to bring on board over time.

**Operator** (Operator):
This concludes the question-and-answer portion of our conference call. I will now turn the call back over to Bill Brown for some closing comments.

**William Brown** (Executives):
Okay. So thank you, everybody, and I know we're over a little bit. I appreciate everybody joining the call today. And I want to thank again all of the 3Mers for delivering another strong quarter of great execution, great value to customers and our shareholders. I'm proud of what we've achieved together, and I'm excited for what the future holds at 3M. Thank you all, and have a good day.

**Operator** (Operator):
Ladies and gentlemen, that does conclude today's conference call. We thank you for your participation and ask that you please disconnect your line.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MMM_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO｜guidance：全年有機成長指引由 3% 上調至 >3.5%（原話："We are raising our organic growth expectations from 3% to"）
- 2026-07-21｜CFO｜guidance：EPS 指引上調至 $8.80–8.95，中點增 $0.27（原話："EPS guidance is increasing from a range of $8.50 to $8.70"）
- 2026-07-21｜CFO｜guidance：自由現金流指引上調 $1 億至 $47–49 億，轉換率 >100%（原話："we have increased our free cash flow guidance by $100"）
- 2026-07-21｜CFO｜guidance：指引隱含下半年有機成長與利潤率擴張幅度（原話："The updated guidance implies second half organic sales"）
- 2026-07-21｜CFO｜guidance：Madison Fire & Rescue 合資未納入本次指引，Q3 財報再納入；稅率約 20%（原話："we'll incorporate that in our third quarter call. And just"）
- 2026-07-21｜CEO｜guidance：下半年消費品預期持平至小幅成長（原話："help us in the back half of consumer to be flat to up"）
- 2026-07-21｜CFO｜margin：Q2 調整後營業利益率 24.9%，比預期高 40bp，來自量與生產力（原話："So we finished the quarter at 24.9% margin, which is the"）
- 2026-07-21｜CFO｜margin：營業利潤增額拆解：成長與生產力 +2.4 億，投資 -3,000 萬，關稅與滯留成本 -1.1 億（原話："Operating profit increased $110 million or $0.16, including"）
- 2026-07-21｜CFO｜margin：油價相關通膨預估由 1.25 億升至 1.5–1.75 億，金額中性但壓低利潤率 20bp（原話："Though oil price cost"）
- 2026-07-21｜CEO｜margin：毛利率目前接近 45% 中段，長期可達高 40%（原話："On gross margins, we're tracking to -- close to mid-40s"）
- 2026-07-21｜CEO｜margin：管理層表示長期有能力把毛利率拉到高 40%（原話："with an ability to hit the high 40s over time."）
- 2026-07-21｜CEO｜margin：油價成本將以定價逐元抵銷，油價面價格成本中性、整體略正（原話："So price cost on oil is"）
- 2026-07-21｜CFO｜margin：滯留成本全年 1.5 億、投資 2.25 億，皆下半年較重；生產力較佳（原話："Just on the stranded cost, it's still $150"）
- 2026-07-21｜CFO｜margin：尚未收到任何關稅退款（原話："We have not received any tariff refunds to date."）
- 2026-07-21｜CEO｜margin：Q2 價格貢獻 1.6%，下半年約 2%，全年約 1.5 點（原話："Q2, our price was at 1.6%. So it was about in line with"）
- 2026-07-21｜CFO｜margin：下半年 EPS 成長約 $0.30，Q3、Q4 平均，季節性正常（原話："So I would say it's normal seasonality with the EPS growing"）
- 2026-07-21｜CFO｜margin：FCF 轉換率 107%，庫存天數改善 7 天，主因營運表現（原話："Our inventories improved by 7 days year-over-year. So just"）
- 2026-07-21｜CFO｜commitment：管理層稱進度領先投資人日承諾（超額成長、約 25% 利潤率、雙位數 EPS CAGR）（原話："we are tracking ahead of Investor Day commitments across"）
- 2026-07-21｜CFO｜commitment：高於總體的成長額預期超過 10 億承諾（原話："is on track to exceed the $1"）
- 2026-07-21｜CFO｜commitment：利潤率領先 2027 年約 25% 的目標（原話："are tracking ahead of the"）
- 2026-07-21｜CEO｜commitment：今年高於總體成長約 4.5 億，高於上季的約 3.4–3.5 億；原計畫三年為 1.25 億／3.26 億／6.27 億（原話："We think we'll be about $450 million above macro in the"）
- 2026-07-21｜CEO｜commitment：股東回饋承諾：2025 起累計 86 億，目標 2027 前 100 億以上（原話："against our commitment to return $10 billion plus through"）
- 2026-07-21｜CEO｜commitment：新產品目標：2027 年前推出逾 1,000 項，開發週期縮短約 20%（原話："launch more than 1,000 products by 2027, while reducing"）
- 2026-07-21｜CFO｜capital_allocation：上半年回購約 30 億，均價約 153 美元，超過年初 25 億預期，下半年「機會式」（原話："We've done about $3 billion at an average price of about"）
- 2026-07-21｜CEO｜capital_allocation：7/1 完成 Madison Fire & Rescue 與 Scott SCBA 合併為多數持股合資，收現金 7 億（原話："receiving $700 million in cash as part of the transaction."）
- 2026-07-21｜CEO｜capital_allocation：合資體營收 8 億、高單位數成長、利潤率高於公司平均（原話："This JV generates revenue of $800 million,"）
- 2026-07-21｜CEO｜capital_allocation：將財務、人資、客服整合為全球共享服務並委外給外部供應商（轉型下一步）（原話："partnering with an external provider to run them at scale"）
- 2026-07-21｜CEO｜product：Microsoft 成為首家部署 EBO 的超大規模業者（Azure）（原話："Microsoft, who will become the first hyperscaler to"）
- 2026-07-21｜CEO｜product：EBO 今年營收 4,000–5,000 萬，數年內可達 4–5 倍以上（原話："The revenue this year was in the"）
- 2026-07-21｜CEO｜product：EBO 今年 TAM 約 10 億，2028 年約 20 億；3M 目前份額小（原話："But the TAM this year for EBO technologies is around $1"）
- 2026-07-21｜CEO｜product：EBO 產能今年翻倍、未來 18 個月再翻倍，仍遠低於市場需求（原話："double our capacity on"）
- 2026-07-21｜CEO｜product：Q2 推出 92 項新產品（+44%），上半年 176 項，全年預計 350 項以上（原話："we launched 92 new products, up 44% versus last year"）
- 2026-07-21｜CEO｜product：新產品中 Class 3 約 75%、Class 4/5 約 25%，長期升至 30% 以上（原話："But Class 3 for us is running around 75% of the launches."）
- 2026-07-21｜CEO｜product：新品活力指數今年中段十幾%，明年 20%；五年內新品銷售約 40 億（原話："new product vitality index climbing to the mid-teens this"）
- 2026-07-21｜CEO｜competition：EBO 有約 100 項專利、50 項申請中；但 3M 不會是唯一供應商，已授權並組成 44 家多供應商協議（原話："we will not be successful as a sole provider here."）
- 2026-07-21｜CEO｜competition：成長倍數由大致等同市場提升到 2 倍（原話："improving from roughly in line to 2x and with businesses"）
- 2026-07-21｜CEO｜competition：管理層將成長歸因於內部表現而非總體順風（原話："It's not really macro tailwind."）
- 2026-07-21｜CEO｜customer：SIBG 客戶流失率改善約 200bp，仍偏高（原話："We've seen about 200 basis points of improvement in"）
- 2026-07-21｜CEO｜customer：交叉銷售已訂 1.1 億、另有 1.2 億在管線，超前投資人日目標（原話："$110 million of opportunities booked and another $120"）
- 2026-07-21｜CFO｜customer：Q2 訂單約 +10%、積壓訂單年增近 20%；75% 為即訂即出貨（原話："So our orders were up about 10% for the quarter and backlog"）
- 2026-07-21｜CFO｜customer：Q3 前兩週訂單與積壓訂單良好（原話："But so far, the first 2 weeks, orders and backlog look good."）
- 2026-07-21｜CEO｜customer：中國 Q2 雙位數成長、上半年約 8%，內銷與出口各半（原話："In the second quarter, we were double-digit growth, first"）
- 2026-07-21｜CFO｜customer：消費品 Q2 -2.1%；六月下旬數家零售商壓低庫存抵銷了 POS 動能（原話："tightening of inventory levels"）
- 2026-07-21｜CEO｜risk：觀察項：下半年消費電子裝置產量預期下滑高十幾%，與記憶體短缺與成本有關（原話："expected to be"）
- 2026-07-21｜CEO｜risk：汽車與售後市場仍弱，美國消費者保守、重視價值（原話："the U.S. consumer remains cautious"）
- 2026-07-21｜CEO｜risk：整體產能利用率約 63.5–64%，個別資產如 New Ulm 受限（原話："It's running around 63.5%, 64%."）


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
{"date":"20260722","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Brown margin 改革兌現且可延續：adj OM 從 24.9% 續升（FY27 25%+ 目標上修、gross margin mid-40s→high-40s），驅動 EPS 從 FY26 $8.88 至 FY28 $10.19","columns":{"2Y 驗證點":"adj OM 續升 + FY27 目標正式上修至 >25%；FY27 EPS ≥ $9.5","5Y 驗證點":"OM 站穩 26-28% + gross margin 逼近 high-40s","10Y 驗證點":"OM 進入頂級工業區間（ITW ~26%+）並維持","數字門檻":"adj OM FY26 >24% / FY27 目標 >25% / FY28 EPS ≥ $10","來源":"Q2 26 adj OM 24.9%（+40bp，史上最高）、FY26 EPS guide 升至 $8.80-8.95","漂移觸發":"OM 連 2 季停滯/倒退 → 削弱；FY27 目標未上修 → 改革紅利封頂"}},{"id":"H2","text":"organic 成長維持「2x macro」（3.5-5%）：commercial excellence + NPI vitality + EBO 資料中心 + 中國/印度份額，非依賴工業週期","columns":{"2Y 驗證點":"organic 維持 >3.5%；orders/backlog 不轉負；NPVI 升向 20%","5Y 驗證點":"organic 站穩 3-4% 穿越週期；EBO 貢獻可見","10Y 驗證點":"NPI 引擎使 3M 長期跑贏工業 IPI","數字門檻":"organic >3.5% / orders 正 / NPVI 升","來源":"Q2 organic +5.4%（H1 +3.3%）、orders +10%/backlog +20%、NPI +44%、EBO $40-50M→$2B TAM by 2028","漂移觸發":"organic 連 2 季"}},{"id":"H3","text":"估值：市場為改革兌現 + Dividend King 給 ~18x，且此溢價可維持（不 de-rate）；PFAS 法律尾部可控不失控","columns":{"2Y 驗證點":"Fwd PE 維持 17-18x；PFAS 現金流出如排程（不新增大額）","5Y 驗證點":"倍數隨改革兌現後成長放緩自然回落至 5Y 中位 ~16x（re-rate 為拖累）","10Y 驗證點":"倍數收斂至成熟工業 15-17x","數字門檻":"Fwd PE ≥ 16x（不跌破 5Y 中位）；PFAS 年流出可控","來源":"賣方共識 avg $172.94（+3%）、中位 $165（","漂移觸發":"PFAS 新增大額求償 或 organic 熄火 → 倍數重設（進場窗開）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"工業週期回落 + 改革紅利兌現封頂：CE H2 down high-teens（記憶體短缺）+ auto build 續降 → organic 掉回","columns":{"對應假設":"H1/H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 organic、orders/backlog、adj OM、FY27 目標","警戒閾值":"organic 連 2 季"}},{"id":"R2","text":"估值均值回歸：Fwd PE 自 70 分位 / 18x 下修回 5Y 中位 ~16x（即使 EPS 續增，倍數壓縮吞報酬）；分析師中位 $165 已","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Fwd PE 5Y 分位、共識 EPS 修正、賣方目標 vs 現價","警戒閾值":"PE 跌破 16x 且 EPS 未同步上修 → de-rating 進行中"}},{"id":"R3","text":"PFAS / 法律尾部復燃：耳塞（$6B/至 2029，~半已付）+ 供水（$10.5-12.5B/13 年）為已知排程；但州 AG（NJ $450M）+ 人身傷害求償是開放式尾部——若新增大額求償或新提列，壓 FCF/回購/股息。注意：Q2 法說全程未提法律，須從 10-Q/8-K/docket 追","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"10-Q 法律附註、8-K、州 AG docket、新提列","警戒閾值":"新增州 AG/人身傷害大額求償 或 FCF 因法律流出"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔 $150-155（Fwd PE ~16x，5Y 中位）或 FY27 OM 目標正式上修（現 24.9% 已達 ~25%，上修將重評 FY27/28 EPS）；或回測 W52 $157","irr_base_pct":6.5,"ev5y_pct":15.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.7,"ev5y_pct":15.0,"irr_base_pct":6.5,"max_dd_pct":-35.0,"bull_5y_price":234.0,"bear_5y_price":126.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"回檔 $150-155（Fwd PE ~16x，5Y 中位）或 FY27 OM 目標正式上修（現 24.9% 已達 ~25%，上修將重評 FY27/28 EPS）；或回測 W52 $157","price_at_dd":170.76,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MMM_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
