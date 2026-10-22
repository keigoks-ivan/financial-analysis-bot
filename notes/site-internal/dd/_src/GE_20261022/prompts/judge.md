你是 stock-analyst **v20 判斷 agent**，標的 GE（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GE","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":14118,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"調整後營收 $13,285M vs 財報前共識約 $12.84B（來源：itiger 財報預覽，聚合站，僅供參考）"},{"id":"f_kpi1_adjusted_revenue_non_gaa","label":"Adjusted revenue (non-GAAP)","value":13285,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"同上，共識約 $12.84B"},{"id":"f_kpi2_operating_profit_non_gaa","label":"Operating profit (non-GAAP)","value":2988,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"新聞稿無；查無共識"},{"id":"f_kpi3_operating_margin_non_gaa","label":"Operating margin (non-GAAP)","value":22.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"查無"},{"id":"f_kpi4_gaap_profit_net","label":"GAAP profit (net, 新聞稿口徑)","value":2805,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"查無"},{"id":"f_kpi5_adjusted_eps","label":"Adjusted EPS","value":2.25,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"財報前共識約 $1.99（來源：itiger 財報預覽，聚合站，僅供參考）"},{"id":"f_kpi6_free_cash_flow_non_gaap","label":"Free cash flow (non-GAAP)","value":2042,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"查無"},{"id":"f_kpi7_orders","label":"Orders","value":19.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"查無"},{"id":"f_kpi8_commercial_services_back","label":"Commercial services backlog","value":170,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD bn（「over」）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（CEO 引述）"},"note":"n/a"},{"id":"f_kpi9_segment_operating_profit","label":"Segment operating profit CES / DPT","value":"CES $2,887M（margin 27.9%，-10bps）；DPT $475M（margin 13.7%，+20bps）","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"mixed","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"查無"},{"id":"f_kpi10_fy2026_guidance","label":"FY2026 guidance（本次上修）","value":"調整後營收成長約 19–20%；營業利益 $10.9–11.0B；調整後 EPS $8.00–8.10；FCF $9.1–9.4B","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"mixed","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm"},"note":"FY1 EPS 共識 7.96（財報後 10-21 快照，consensus_revision；落在指引下緣之下，尚未完全反映）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-20","period":"2026-10-20","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ge_gross_margin_pct","label":"GE 毛利率","value":31.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ge_operating_margin_pct","label":"GE 營業利益率","value":18.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ge_fcf_margin_pct","label":"GE FCF 利潤率","value":16.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ba_gross_margin_pct","label":"BA 毛利率","value":2.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ba_operating_margin_pct","label":"BA 營業利益率","value":-7.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ba_fcf_margin_pct","label":"BA FCF 利潤率","value":-1.22,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rtx_gross_margin_pct","label":"RTX 毛利率","value":20.35,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RTX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rtx_operating_margin_pct","label":"RTX 營業利益率","value":11.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RTX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rtx_fcf_margin_pct","label":"RTX FCF 利潤率","value":11.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RTX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tdg_gross_margin_pct","label":"TDG 毛利率","value":59.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tdg_operating_margin_pct","label":"TDG 營業利益率","value":46.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tdg_fcf_margin_pct","label":"TDG FCF 利潤率","value":19.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gd_gross_margin_pct","label":"GD 毛利率","value":15.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gd_operating_margin_pct","label":"GD 營業利益率","value":10.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gd_fcf_margin_pct","label":"GD FCF 利潤率","value":11.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":295.88,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":7.39,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":31.81,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.38,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.93 → 7.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.11 → 9.11）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.41 → 10.41）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":7.96,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.11,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":10.41,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":5.29,"period":"2026-07-16 → 2026-10-21","unit":"%","basis":"FY1 共識 EPS 7.56 → 7.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":34.89,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝2.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":2.1,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.06,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝74.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":74.1,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.27,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝73.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":73.7,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":37.17,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 7.96，分子＝快照價 295.88","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.598,"period":"2026-10-22","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-22"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":10285.0,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 20230.0、現金 9945.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1037.56,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":317278.99,"period":"2026-10-22","unit":"USD m","basis":"市值 306993.99 ＋ 淨負債 10285.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":50645.4,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（14 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":56338.72,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.26,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 295.88 / W52 318.55 / W104 270.94 / W250 165.57 / W250 13週斜率 2.46%"},{"id":"f_ma_w52","label":"52 週均線","value":318.55,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":270.94,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":165.57,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.46,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"2026年2月美國空軍就ACP（自主協同平台）無人機發動機開發合約授予四支團隊：Beehive Industries、Honeywell、Pratt & Whitney 與 GE Aerospace–Kratos 聯隊；空軍稱要多供應商。Beehive 為新進入者（Rampart 引擎）。","source":"ePlane AI: GE Aerospace secures contract to develop engine for US Air Force autonomous aircraft（聚合站，低可信）","url":"https://www.eplaneai.com/news/ge-aerospace-secures-contract-to-develop-engine-for-us-air-force-autonomous-aircraft","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"GE 與 RTX（Pratt & Whitney）競逐波音／空巴發動機供應，售後支援為關鍵；文章內容前後不一致，低可信","source":"ePlane AI: GE and RTX compete to supply engines for Boeing and Airbus","url":"https://www.eplaneai.com/news/ge-and-rtx-compete-to-supply-engines-for-boeing-and-airbus","excerpt":"delays, demand for maintenance and spare parts surges, benefiting suppliers across both new equipment and aftermarket services. Intensifying Competition Amid Backlogs and Bottlenecks The rivalry between GE and RTX is further intensified by the global order backlog and the focus on CFM56-powered narrowbody aircraft, heightening the competition to secure contracts with Boeing and Airbus.","as_of":"2026-08-10","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"GE 2026Q3 財報新聞稿（SEC 8-K），可核對訂單、LEAP 交付等競爭面事實","source":"GE Form 8-K 3Q2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm","excerpt":"•Increased material input from priority suppliers double-digits year-over-year, contributing to strong year-to-date Commercial Engines & Services (CES) services revenue and total engine deliveries, including LEAP growing 26%.","as_of":"2026-10-21","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"+","claim":"GE 10-Q 風險因子：依機型，航空公司可在 GE 與其他製造商引擎間選擇；部分 Boeing 機型 GE 引擎為該機型唯一來源引擎","source":"GENERAL ELECTRIC CO Form 10-Q FY2026 (period ending 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000049/ge-20260630.htm","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"GE 10-K FY2025 風險段揭露：公司對部分最大客戶有重大業務與信用曝險，且業界活動受少數大型 OEM 與大型航空公司影響；未在該段列出單一客戶占營收百分比。","source":"SEC EDGAR 10-K FY2025（申報 2026-01-29）","url":"https://www.sec.gov/Archives/edgar/data/40545/000004054526000008/ge-20251231.htm","excerpt":"Activity in our sector is also particularly influenced by the actions of a small group of large original equipment manufacturers, as well as large airlines in various geographies. We have significant business with, and credit exposure to, some of our largest customers","as_of":"2026-01-29","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"GE 2026 年第三季財報新聞稿：依年初至今表現與第四季展望上調全公司指引。","source":"GE 8-K 3Q2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm","excerpt":"Year-to-date orders, revenue and total engine deliveries up over 20%, raising full-year guidance Third Quarter 2026: •Total orders of $19.0B, +49%; •Total revenue (GAAP) of $14.1B, +16%;","as_of":"2026-10-21","retrieved_at":"20261022","affects":["triggers","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"IATA 供應鏈研究：2018 年起的交機放緩已超越多次供應鏈衝擊，呈結構性限制，供需真正再平衡不太可能早於 2030 年代初","source":"IATA, supply chain study highlights","url":"https://www.iata.org/en/iata-repository/pressroom/presentations/supply-chain-study-highlights","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Boeing 2026 年 7 月展望：2026 年初約 2,000 架飛機供給不足，單走道缺口約到本十年末、寬體缺口持續到 2030 年代初；2026 至 2045 年需求 43,625 架","source":"Boeing Commercial Market Outlook via Tribune, Boeing shrugs off ME war impact, maintains forecast","url":"https://tribune.com.pk/story/2619039/boeing-shrugs-off-me-war-impact-maintains-forecast","excerpt":null,"as_of":"2026-07-19","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"GE Aerospace 2026 年第三季：訂單年增 49% 至 $190 億，商用服務訂單增 23%；年初至今訂單、營收、引擎交付皆增逾 20%，上調全年指引","source":"GE 3Q2026 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm","excerpt":"Year-to-date orders, revenue and total engine deliveries up over 20%, raising full-year guidance","as_of":"2026-10-20","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"GE 宣布以 117.5 億美元收購鑄件供應商 Consolidated Precision Products，自述積壓訂單延伸至下個十年；RTX 亦擴充結構鑄件產能","source":"Leeham News, GE Aerospace Moves to Secure Critical Engine Casting Capacity","url":"https://leehamnews.com/2026/09/09/ge-aerospace-moves-to-secure-critical-engine-casting-capacity/","excerpt":null,"as_of":"2026-09-09","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"BCG：鑄鍛件製程前置期 6 至 18 個月以上；PwC/AIA 調查顯示需求為現況 2 倍時僅 47% 的 A&D 受訪者能在 18 個月內交付","source":"BCG, Fixing aerospace's supply chain for casting and forging; PwC State of the Ramp","url":"https://www.bcg.com/publications/2024/fixing-aerospaces-supply-chain-for-casting-and-forging","excerpt":null,"as_of":"2024-01-01","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Aviation Week 預估 2026 年商用機交付 1,686 架，高於 2019 年以來各年但仍低於 2018 年的 1,753 架","source":"Aviation Week, 2026 Airliner Deliveries To Be Short Of 2018","url":"https://aviationweek.com/air-transport/aircraft-propulsion/2026-airliner-deliveries-be-short-2018-aviation-week-forecasts","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"GE Aerospace 擬以 117.5 億美元收購 Consolidated Precision Products，預計 2027 下半年完成，須經監管核准","source":"SEC EDGAR 10-Q（截至 2026-09-30）","url":"https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000064/ge-20260930.htm","excerpt":"acquire Consolidated Precision Products (CPP), a leading manufacturer of highly engineered castings and sub-assemblies primarily for the commercial aerospace and defense markets, with a purchase price of $11.75 billion. We plan to fund the acquisition with approximately $7 billion in cash and the remainder in new debt. This transaction is expected to close in the second half of 2027 and will","as_of":"2026-10-21","retrieved_at":"20261022","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-07-09 總統公告對民用飛機、噴射引擎與零件的 Section 232 不加關稅，開啟 180 天談判期，保留日後課稅選項；Commerce/USTR 須於 2027-01-05 前報告進度","source":"GHY Section 232 Aerospace trade talks","url":"https://www.ghy.com/trade-compliance/section-232-aerospace-trade-talks/","excerpt":"Trade Representative to negotiate agreements with trading partners on imports of commercial aircraft, jet engines, and associated parts. The order imposes no new duties but opens a 180-day negotiation window and reserves the option of tariffs or other measures.","as_of":"2026-07-10","retrieved_at":"20261022","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"GE 10-Q 揭露：與歐盟、英國、日本、韓國有航太設備零關稅協議；最高法院裁定 IEEPA 關稅無效，GE 已申請並收到部分已繳 IEEPA 關稅退款","source":"GE Form 10-Q (period ended 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000064/ge-20260930.htm","excerpt":"established a zero-for-zero tariff agreement on aerospace equipment with the EU, UK, Japan and Korea, establishing a mutual elimination of tariffs. In 2026, the Supreme Court ruled against tariffs imposed under the International Emergency Economic Powers Act (IEEPA). In the first nine months of 2026, GE Aerospace submitted refund requests and received a portion of","as_of":"2026-10-21","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026 年 4 月 GE Aerospace 與美國國務院和解 116 項 AECA/ITAR 疑似違規（涉及對中國未授權技術資料出口），民事罰款 3,600 萬美元，其中 1,800 萬暫緩","source":"Lexology: GE Aerospace to pay $36m for alleged US export breaches","url":"https://www.lexology.com/pro/content/ge-aerospace-to-pay-36m-for-alleged-us-export-breaches","excerpt":"GE Aerospace to pay $36m for alleged US export breaches Updated as of: 20 April 2026 Malavika Devaya The company self-reported 116 violations over six years, including sending a Chinese supplier data on a military jet engine, the State Department’s export enforcer said in its first public settlement since 2024.","as_of":"2026-04-20","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2025 年 7 月美國商務部解除對 GE 向中國商飛(COMAC)出口 LEAP-1C 與 CF34 引擎的暫停","source":"Mexico Business News: US Lets GE Resume Jet Engine Exports to China's COMAC","url":"https://mexicobusiness.news/aerospace/news/us-lets-ge-resume-jet-engine-exports-chinas-comac","excerpt":"The restored licenses allow GE to export LEAP-1C engines—developed through a joint venture with France’s Safran—for COMAC’s C919 narrow-body aircraft. The authorization also includes GE’s CF34 engines, which power the C909 regional jet.","as_of":"2025-07-08","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"GE Aerospace 2026-09 同意收購鑄件供應商 Consolidated Precision Products（LEAP、GEnx 關鍵供應商），鑄件產能被視為關鍵瓶頸；仍續與 ATI、Howmet 合作","source":"Leeham News: GE Aerospace Moves to Secure Critical Engine Casting Capacity","url":"https://leehamnews.com/2026/09/09/ge-aerospace-moves-to-secure-critical-engine-casting-capacity/","excerpt":"GE Aerospace’s plan to implement a similar model with Consolidated Precision Products could therefore boost casting capacity across the supply chain. Notably, GE Aerospace is not abandoning other casting suppliers. It will continue working with companies such as ATI and Howmet Aerospace.","as_of":"2026-09-09","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"美國 2025-07 解除對 GE 供應 COMAC 引擎（LEAP-1C、CF34）出口許可的暫停","source":"Finviz: GE Aerospace resumes jet engine shipments to China amid easing trade tensions","url":"https://finviz.com/news/98846/ge-aerospace-resumes-jet-engine-shipments-to-china-amid-easing-trade-tensions","excerpt":"Aircraft Corporation of China/COMAC. The decision signals a de-escalation of US-Sino trade tensions, which also involved concessions from Beijing regarding rare earth exports. This followed the US’s suspended licenses for these shipments several weeks prior as part of an ongoing trade dispute. The lifted restrictions specifically apply to GE’s LEAP-1C engines, which are manufactured by","as_of":"2025-07-01","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026：訂單年增49%至190億美元，GAAP營收年增16%至141億美元；2027年商用服務預期低雙位數成長，商用服務在手訂單逾1,700億美元（搜尋摘要轉述自公司Q3財報，未取得逐字原文）","source":"GE 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026：商用服務營收季增26%（上半年32%），總引擎交付+31%、LEAP+41%；LEAP全年交付成長預期上調至高十位數；上半年航班數大致持平；供給而非需求為主要限制（二手轉述）","source":"Leeham News: Q2 2026 earnings: GE Aerospace keeps the beat despite a few missed notes","url":"https://leehamnews.com/2026/07/16/q2-2026-earnings-ge-aerospace-keeps-the-beat-despite-a-few-missed-notes/","excerpt":null,"as_of":"2026-07-16","retrieved_at":"20261022","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 財報電話會議：>95% 第三季備件營收已在在手訂單，計畫拆機數超過全年維修廠進廠展望40%以上；LEAP維修廠進廠至2030年約年增25%","source":"Motley Fool: GE Q2 2026 earnings call transcript","url":"https://www.fool.com/earnings/call-transcripts/2026/07/23/ge-ge-q2-2026-earnings-call-transcript/","excerpt":"more than 95% of spare parts revenue in backlog, similar to second quarter. Engines already off wing and the pipeline of planned removals in the third quarter exceed our full-year shop visit guide by over 40%. This provides us with ample visibility into demand to fulfill our outlook for 2026. We now expect commercial equipment to grow around 20%, up from mid to high teens, with LEAP deliveries","as_of":"2026-07-23","retrieved_at":"20261022","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Morgan Stanley：需求超過供給，備件交付延遲（delinquency）上升，約2,100億美元在手訂單提供能見度","source":"Placera: GE Aerospace Backlog, Demand Strength Likely to Offset Oil Price Concerns, Morgan Stanley Says","url":"https://www.placera.se/telegram/ge-aerospace-backlog-demand-strength-likely-to-offset-oil-price-concerns-morgan-stanley-says-20260422","excerpt":"GE's roughly $210 billion backlog, including about $170 billion in Commercial Services, provides visibility into Q2 and full-year 2026, supported by strong \"spare parts\"demand and \"shop visit\"activity. Analysts at Morgan Stanley said \"demand continues to outpace supply,\"pointing to rising spare parts delinquency alongside revenue growth, according to the report.","as_of":"2026-04-22","retrieved_at":"20261022","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"Q1 2026：GE維持展望，警示燃油成本上升將使飛行量成長放緩","source":"CP24: GE Aerospace keeps outlook, flags slower flight growth as fuel costs rise","url":"https://www.cp24.com/news/money/2026/04/21/ge-aerospace-keeps-outlook-flags-slower-flight-growth-as-fuel-costs-rise/","excerpt":"GE Aerospace keeps outlook, flags slower flight growth as fuel costs rise By Reuters Opens in new window Published: April 21, 2026 at 9:24a.m. EDT The General Electric (GE) logo is shown on Oct.","as_of":"2026-04-21","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Simply Wall St 敘事（非公司指引）指出電動與氫能推進為 GE 噴射引擎業務的長期競爭風險；氣候政策亦可能削弱引擎與售後需求。","source":"Simply Wall St narrative: Global decarbonization and geopolitical strife will undermine aerospace margins","url":"https://simplywall.st/community/narratives/us/capital-goods/nyse-ge/general-electric/boc8w8u1-global-decarbonization-and-geopolitical-strife-will-undermine-aerospace-margins","excerpt":null,"as_of":"2025-06-01","retrieved_at":"20261022","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"CFM（GE 與 Safran 合資）推進 RISE 開放式風扇計畫，目標燃油消耗較現行引擎至少降 20%；2026 年 7 月報導指出整合渦槳與渦扇特性面臨工程挑戰。GE 與 Safran 亦進行混合電動地面測試，替代推進路線由 GE 自身參與。","source":"eplaneai: CFM gains confidence in open fan technology after RISE series success","url":"https://www.eplaneai.com/news/cfm-gains-confidence-in-open-fan-technology-after-rise-series-success","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"GE 預期外部服務通路占 LEAP 服務組合比重由中段十餘%升至 2030 年約 30%","source":"Leeham News, Q2 2026 earnings: GE Aerospace keeps the beat despite a few missed notes","url":"https://leehamnews.com/2026/07/16/q2-2026-earnings-ge-aerospace-keeps-the-beat-despite-a-few-missed-notes/","excerpt":"At the same time, GE expects its external services channel to grow from the mid-teens of its LEAP services portfolio today to about 30% by 2030, expanding capacity as maintenance demand accelerates.","as_of":"2026-07-16","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 後（2026-07-16）GE 將 2026 調整後 EPS 指引上調至 $7.65–7.85（原 $7.1–7.4），FCF $8.9–9.2B；當時共識 EPS 約 $7.54，股價反跌逾 4%，TD Cowen 認為上調幅度「may not be good enough」。","source":"Benzinga/Barchart/TIKR 彙整（搜尋摘要）","url":"https://www.barchart.com/story/news/3663603/ge-aerospace-stock-analyst-estimates-ratings","excerpt":null,"as_of":"2026-07-16","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布（2026 年 10 月初）：Investing.com 21 位分析師平均 $396.81、高 $450、低 $347；Barchart 平均 $396.45、高 $455；Wells Fargo 於 2026-09-30 由 $390 降至 $380 維持 Overweight；Yahoo 引述共識 $361.89；Daiwa 中立、目標 $301，警告 2027–2028 共識可能有風險。","source":"Autobound（引 Investing.com）、Barchart、Yahoo Finance 搜尋摘要","url":"https://www.autobound.ai/companies/ge-aerospace/news/ge-aerospace-stock-reports-21-1-percent-revenue-growth-7da5e27c","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026（2026-10-20 公布）：訂單 $19.0B（+49%）、調整後營收 $13.3B（+18%）、調整後 EPS $2.25（+36%，共識約 $1.99）；Culp 表示「raising our 2026 guidance across the board」，並預期 2027 商用服務低雙位數成長。新指引數字摘要未見。","source":"GE 8-K Q3 2026 earnings release（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-09-08 GE Aerospace 宣布以 117.5 億美元現金收購鑄件製造商 Consolidated Precision Products（CPP），預計 2027 下半年交割，須監管核准。","source":"SEC EDGAR 8-K（2026-09-08, Item 8.01）","url":"https://www.sec.gov/Archives/edgar/data/40545/000095014226002501/eh260827362_8k.htm","excerpt":"the Company issued a press release announcing the\nentry into an agreement to acquire Consolidated Precision Products (“CPP”), a leading manufacturer of highly engineered castings,\nfor a cash purchase price of $11.75 billion, subject to closing adjustments. The transaction is expected to close in the second half of\n2027 and is subject to regulatory approvals and other customary closing conditions.","as_of":"2026-09-08","retrieved_at":"20261022","affects":["valuation","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 披露兩件股東衍生訴訟（Lindsey、Priest/Tola）仍在紐約州法院待決；Sjunde AP-Fonden 案已於 2025 年 4 月和解。","source":"SEC EDGAR 10-K FY2025 法律事項附註","url":"https://www.sec.gov/Archives/edgar/data/40545/000004054526000008/ge-20251231.htm","excerpt":"Two shareholder derivative lawsuits are currently pending: the Lindsey and Priest/Tola cases, which were filed in New York state court. The allegations in these two cases relate to substantially the same facts as those underlying the Sjunde AP-Fonden case, which settled in April 2025.","as_of":"2026-01-29","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"FAA 於 2026 年 7 月發布 GEnx-1B/-2B AD 2026-14-03（燃油熱交換器連接軟管缺陷致漏油），2026-08-21 生效，要求更換受影響軟管。","source":"EASA AD 資料庫 AD US-2026-14-03","url":"https://ad.easa.europa.eu/blob/2026-14-03.pdf/AD_US-2026-14-03_1","excerpt":null,"as_of":"2026-08-21","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-09-08 GE Aerospace 宣布以 117.5 億美元現金收購 CPP，預計 2027 下半年交割，須監管核准。","source":"SEC EDGAR 8-K（2026-09-08, Item 8.01）","url":"https://www.sec.gov/Archives/edgar/data/40545/000095014226002501/eh260827362_8k.htm","excerpt":"the Company issued a press release announcing the\nentry into an agreement to acquire Consolidated Precision Products (“CPP”), a leading manufacturer of highly engineered castings,\nfor a cash purchase price of $11.75 billion, subject to closing adjustments.","as_of":"2026-09-08","retrieved_at":"20261022","affects":["valuation","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"兩件股東衍生訴訟（Lindsey、Priest/Tola）在紐約州法院待決；相關 Sjunde AP-Fonden 案 2025 年 4 月和解。搜尋未見 2026 新提起的證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 法律事項附註","url":"https://www.sec.gov/Archives/edgar/data/40545/000004054526000008/ge-20251231.htm","excerpt":"Two shareholder derivative lawsuits are currently pending: the Lindsey and Priest/Tola cases, which were filed in New York state court.","as_of":"2026-01-29","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"FAA AD 2026-14-03 針對 GEnx-1B/-2B 燃油熱交換器連接軟管缺陷，要求辨識並更換，2026-08-21 生效。","source":"EASA AD 資料庫 AD US-2026-14-03","url":"https://ad.easa.europa.eu/blob/2026-14-03.pdf/AD_US-2026-14-03_1","excerpt":null,"as_of":"2026-08-21","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.04,"operating_margin_pct":18.68,"fcf_margin_pct":16.58,"rd_intensity_pct":3.48},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GE","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"BA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":2.86,"operating_margin_pct":-7.44,"fcf_margin_pct":-1.22,"rd_intensity_pct":3.98},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BA","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"RTX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.35,"operating_margin_pct":11.21,"fcf_margin_pct":11.75,"rd_intensity_pct":3.02},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RTX","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"TDG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":59.57,"operating_margin_pct":46.47,"fcf_margin_pct":19.26,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"GD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.38,"operating_margin_pct":10.32,"fcf_margin_pct":11.75,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GD","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"GE"},"financial_history":{"ticker":"GE","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":29139000000.0,"revenue_yoy_pct":null,"gross_margin_pct":25.94,"operating_margin_pct":12.34,"net_income":336000000.0,"diluted_eps":0.05,"free_cash_flow":5255000000.0,"fcf_margin_pct":18.03,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":35348000000.0,"revenue_yoy_pct":21.31,"gross_margin_pct":26.94,"operating_margin_pct":13.34,"net_income":9482000000.0,"diluted_eps":8.36,"free_cash_flow":4327000000.0,"fcf_margin_pct":12.24,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":38702000000.0,"revenue_yoy_pct":9.49,"gross_margin_pct":30.92,"operating_margin_pct":17.47,"net_income":6556000000.0,"diluted_eps":5.99,"free_cash_flow":3678000000.0,"fcf_margin_pct":9.5,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":45855000000.0,"revenue_yoy_pct":18.48,"gross_margin_pct":31.49,"operating_margin_pct":18.93,"net_income":8704000000.0,"diluted_eps":8.14,"free_cash_flow":7264000000.0,"fcf_margin_pct":15.84,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GE/GE_Q3_2026_Earnings_Call_20261020.md）

# Q3 2026 Earnings Call
**General Electric Company** | Earnings Calls | 2026-10-20

**Operator** (Operator):
Good day, ladies and gentlemen, and welcome to the GE Aerospace Third Quarter 2026 Earnings Conference Call. [Operator Instructions] My name is Liz, and I will be your conference coordinator today. [Operator Instructions] As a reminder, this conference is being recorded.
I would now like to turn the program over to your host for today's conference, Blaire Brown (sic) [ Blaire Shoor ] from the GE Aerospace Investor Relations team. Please proceed.

**Blaire Shoor** (Executives):
Thanks, Liz. Welcome to GE Aerospace's Third Quarter 2026 Earnings Call. I'm joined by Chairman and CEO, Larry Culp; and CFO, Rahul Ghai.
Many of the statements we're making are forward-looking and based on our best view of the world and our business as we see them today. As described in our SEC filings and website, those elements may change as the world changes. Additionally, Larry and Rahul will speak to total company and corporate financial results and guidance today on a non-GAAP basis.
Now over to Larry.

**H. Culp** (Executives):
Blaire, thank you, and good morning, everyone. At any moment, nearly 1 million people are flying on aircraft powered by our technology. That's the responsibility behind everything we do at GE Aerospace, and it underscores our purpose to invent the future of flight, lift people up and bring them home safely.
In the third quarter, we delivered strong results. Demand continues to be solid across the business even in a dynamic environment. Third quarter orders were up 49%, led by Commercial Engines & Services, or CES, which was up 58%. We continue to see strength in commercial services with orders up 23% in the third quarter and 30% year-to-date. Combined with our backlog of over $170 billion, we're well positioned to close out 2026 and now expect low double-digit services growth in 2027.
We had a historic Farnborough Airshow announcing commitments for more than 1,800 engines, including an agreement with IndiGo for the largest LEAP agreement ever for more than 1,000 LEAP-1A engines to power its A320neo aircraft. And just last week, we announced an agreement with Turkish Airlines for more than 300 LEAP-1B engines to power its 737 MAX fleet, along with a long-term service agreement for its entire LEAP-1B fleet of over 600 engines.
In the quarter, total company revenue increased 18%, with CES up 21% and Defense & Propulsion Technologies, or DPT, up 7%. Operating profit grew 30%, and margins of 22.5%, up 220 basis points year-over-year. EPS increased 36%, and we generated more than $2 billion of free cash flow.
These results reflect the impact of FLIGHT DECK fundamentals to drive continued output momentum with year-to-date commercial services revenue and total engine deliveries both up over 20%. And we remain focused on investing to meet customer needs with our recently announced agreement to acquire Consolidated Precision Products, or CPP, to expand capacity of mission-critical castings. At the same time, we're advancing current and future technologies with over $3 billion in annual R&D spend.
This quarter's performance builds on progress from the first half with year-to-date orders now up 49%, revenue up 23%, EPS growing 28% and 105% free cash flow conversion. Given the strength of our results, combined with our fourth quarter expectations, we're raising our 2026 guidance. I want to take a moment here and thank the entire GE Aerospace team and our supplier partners for their commitment to delivering for our customers.
Turning to Slide 4. FLIGHT DECK is at the center of how we drive safety, quality, delivery and cost, always in that order. We're making meaningful progress with year-to-date commercial services revenue up 26% and total engine deliveries up 21%. With the LEAP installed base expected to more than double between 2025 and 2030, our team focused on increasing capacity for the LEAP fan assembly.
Using FLIGHT DECK, the team reoriented the layout of the production line and developed standard work at various workstations, resulting in greater capacity with output more than doubling. To improve F/A-18 readiness for the U.S. Navy, we partnered with a key supplier to reduce repair times for a critical F414 component. Using FLIGHT DECK to improve the flow of parts, we doubled output, helping meet our customers' needs. These actions demonstrate the power of collaborative problem solving to unlock constraints, which contributed to priority supplier material input increasing double digits year-over-year again in the third quarter.
Thanks to the work of our team and the partnership with our suppliers, this quarter marks the 10th consecutive quarter of sequential material input growth, which contributed to LEAP engine deliveries growing 26% year-to-date. The gains we're driving with FLIGHT DECK are further accelerated with AI. At Celma, our largest MRO site, the team developed an AI-enabled tool to automate collection of technical records required for each CFM56 shop visit. This helped decrease record processing time by around 25%.
Actions like this across our network resulted in another quarter of record internal shop visit output with turnaround time down by over a week since the end of 2025, including LEAP now down 2 weeks. This progress, combined with other efforts, has reduced LEAP engine-driven grounded aircraft to nearly 0 since the summer. All in, while there is always more to do to meet customer expectations, we're making meaningful progress.
Shifting to Slide 5. Given airframer order books are full through the end of the decade, along with strong growth in aftermarket and defense, we're continuing to invest to ensure timely delivery for our customers. Our agreement to acquire CPP, a long-term supplier, is a significant investment to build adequate capacity of mission-critical castings for the entire aerospace industry. Beyond increasing delivery, acquiring CPP allows us to accelerate the introduction of new engine technologies that improve cooling and enhance durability and efficiency of our current fleet and future programs.
And we're making meaningful progress on next-generation programs while building additional capabilities through partnering with disruptors to move at pace. It was a moment of great pride for our team this summer when alongside our partners at BETA Technologies, we completed the world's first high-altitude hybrid electric flight. We're grateful for the collaborative partnership with BETA to demonstrate that hybrid electric technologies are viable for commercial aviation through NASA's electrified powertrain flight demonstration program.
Together with Kratos, our GEK800, now known officially as the F143, was designated as a second source propulsion for the Joint Air-to-Surface Standoff Missile, or JASSM, moving it from development to a funded U.S. Air Force program. Our XA102 adaptive cycle engine was selected by the U.S. Air Force for the next phase of the NGAP program, moving into hardware procurement and subcomponent testing. The U.S. Navy's recent announcement of the F/A-XX is another example of the administration's leadership in moving forward important sixth-generation programs that ensure the U.S. maintains air superiority building off last year's F-47 news.
We're excited about the progress our Edison Works team has made on advanced engines and how it positions us well to support the U.S. administration's efforts in modernizing our military. Stepping back, we continue to position GE Aerospace for long-term growth by focusing on what matters most to our customers.
Rahul, over to you.

**Rahul Ghai** (Executives):
Larry, thank you, and good morning, everyone. GE Aerospace delivered another strong quarter with double-digit growth across orders, revenue, profit and EPS. Orders were up 49%, with CES up 58% and DPT up 18%. Revenue increased 18%. CES was up 21%, marking our sixth consecutive quarter of at least 20% growth, and DPT grew 7%. Operating profit was $3 billion, up 30%, and margins increased 220 basis points to 22.5%, driven by services volume, productivity and price, partially offset by inflation. EPS was $2.25, up 36%, from increased operating profit and a reduced share count. Free cash flow was $2 billion.
Working capital was a use as receivables grew from timing of services billings and an increase in balance due from airframers. Net contract assets and liabilities were a source in the quarter from strong utilization billings. Our results build on the strength from the first half, with year-to-date orders up 49%, revenue up 23%, operating profit growth of $1.5 billion or 22%. Free cash flow is up 13% to $6.7 billion from higher earnings and a meaningful reduction in inventory growth. This reflects 105% conversion with continued favorability in net contract assets and liabilities.
Going deeper on our 36% EPS growth this quarter. Higher operating profit drove $0.55 or over 90% of the improvement in EPS. Both segments grew profit and corporate cost was lower by about $160 million from timing of accruals and cost management initiatives, partially offset by a slight increase in eliminations. The remainder of the EPS growth in the quarter was driven by a reduction in share count from our previously announced capital allocation actions, while the tax rate was roughly flat at around 15%.
Turning to CES. In the third quarter, orders grew 58%, with services orders up 23% year-over-year and nearly $300 million sequentially. Spare parts orders grew faster than total services, including continued strength in CFM56. Equipment orders more than tripled. Revenue increased 21%, with services growing 17%. Internal shop visit revenue grew 12%. Higher volume and heavier wide-body work scopes were partially offset by customer and product mix with LEAP volume up over 40%. Spare parts increased over 20% from improved material availability that helped fulfill strong customer demand, growth in LEAP external channel and price.
Work scopes remained stable for CFM56. Even with strong revenue growth, spare parts delinquency increased sequentially, reflecting strong underlying demand. Equipment revenue grew 38% with engine deliveries up 8%, including LEAP up 5%. This reflects continued sequential improvement, marking our fifth consecutive quarter of at least 500 LEAP engine deliveries. Wide-body engine deliveries were up over 50% and GEnx shipments nearly doubled. While we delivered GE9X engines this quarter, the impact from these shipments will be recognized post mid-seal certification.
Profit was $2.9 billion, up 21% with margins of 27.9%, driven by higher services volume and price, partially offset by mix and inflation. Year-to-date, CES orders are up 54%, with services up 30%, which positions us well for 2027. Revenue is up 27%, including services up 26%, supporting operating profit growth of $1.4 billion while delivering 25% increase in engine deliveries.
Turning to DPT. Orders increased 18%. In the quarter, we were awarded a 5-year contract worth $2.9 billion to provide ongoing support for the F414 engines powering the U.S. Navy's F/A-18 and EA-18G fleets, focused on keeping the fleet mission ready. Defense book-to-bill was 1.0x in the quarter and 1.5x year-to-date. Total DPT backlog was over $30 billion, up over $5 billion since the start of the year. Revenue grew 7%. Defense & Systems revenue was up 5%, driven by growth in both services and equipment with engine deliveries up 4%. Propulsion & Additive Technologies grew 10%, with growth driven by Avio Aero and Unison. Profit grew 8% and margins were up 20 basis points to 13.7% from increased volume and price, partially offset by mix and inflation. Year-to-date, DPT has delivered 33% orders growth, 13% revenue growth and $1.3 billion of profit, up 14%.
Moving to guidance on Slide 10. Given the strong year-to-date performance and visibility entering the fourth quarter, we are raising our total company guidance across the board. We are now expecting revenue growth of 19% to 20% from high-teens previously. We expect CES growth of low 20s, up from prior outlook of around 20%. Commercial Services is at the higher end of the prior outlook, and we now expect approximately $5.5 billion of year-over-year revenue growth, up approximately $400 million at the midpoint from our prior expectation.
We now expect Commercial Equipment to grow low 20s, up from around 20% previously. And we continue to see DPT growth of low double digits. Operating profit is now expected to be in the range of $10.9 billion to $11 billion, up $300 million from our prior outlook at the midpoint. CES operating profit is now expected to be in the range of $10.5 billion to $10.6 billion, up $250 million at the midpoint from our prior outlook. Of the increase, around $100 million is from reduced impact from GE9X in the second half.
We continue to deliver engines to Boeing with the upgraded mid-seal and are working to achieve FAA certification by the end of 2026. However, given the expected certification timing, we have assumed fewer units in the year. The remaining $150 million increase reflects the drop-through from higher services growth. We have over 100% of the engines' fourth quarter internal shop visits currently in the shop with additional engines waiting for induction. And we are entering the quarter with more than 95% of spare parts in backlog, similar to prior quarters.
We continue to expect DPT profit of $1.6 billion to $1.7 billion. Corporate costs and eliminations are trending toward the lower end of the $1.2 billion to $1.3 billion range. Taken together, we are raising our EPS guidance to a range of $8 to $8.10, up $0.30 at the midpoint. This reflects higher profit, combined with a lower tax rate of around 16% for the year, down from our prior outlook of below 16.5%. We are also raising our free cash flow guidance to $9.1 billion to $9.4 billion, up $200 million from our prior guide, reflecting higher earnings and above 100% conversion for the year.
Overall, we are set to close out another excellent year in 2026 with around $1.9 billion of profit growth and $1.6 billion of free cash flow growth. And given our commercial installed base continues to grow low to mid-single digits annually, ongoing work scope favorability, combined with price and elevated backlog, we are positioned for low double-digit commercial services growth in 2027.
With that, Larry, back to you.

**H. Culp** (Executives):
Rahul, thank you. We're encouraged by the momentum we see across the company. It's a testament to the strength of our leadership team and the positions that we enjoy across commercial and defense, and we remain focused on what matters most, delivering for our customers. Our performance is underpinned by our sustained competitive advantages. With the industry's largest fleet, 80,000 engines and growing and more than 2.3 billion flight hours, we operate at scale across decades-long life cycles, which keeps us close to our customers and supports continued services momentum.
Our field experience enables continuous improvement in time on wing and cost of ownership, results our customers value most. Across our narrow-body, wide-body, regional and defense platforms, we offer the best-performing products under wing, supported by deep technology expertise and a growing services network. To build on our current leadership positions in both commercial and defense propulsion, we invest over $3 billion in annual R&D and over $1 billion in CapEx to develop next-gen technologies with improved durability and performance that will meet the evolving needs of both our commercial and defense customers.
And with FLIGHT DECK, we're turning strategy into results with a focus on safety, quality, delivery and cost, always in that order. Taken together, we're confident in the path ahead and our ability to deliver exceptional value. Thank you to the GE Aerospace team for your continued commitment to deliver for our customers and our shareholders.
With that, let's go to questions.

**Blaire Shoor** (Executives):
[Operator Instructions] Liz, can you please open the line?

**Operator** (Operator):
[Operator Instructions] Our first question comes from Doug Harned with Bernstein.

**Douglas Harned** (Analysts):
So this was certainly a strong quarter on services. You've got a big backlog across your platforms in CES. But we're looking Brent is at $111 today. You can have -- as we look at GE90 is totally backed up for shop visits, hard to get parts, hard to get an engine. CFM56 utilization is down a little bit. But how do you all look at the next couple of years in terms of with fuel up, looking at airline profitability and your planning for growth in that segment? It looks like we're in a very challenging environment, even though your results are really strong.

**H. Culp** (Executives):
Well, Doug, I think that as we look at the environment, there's no question that it is dynamic, right? We've seen that over the last 6 months, and there are a number of questions out there. But I think we just -- we see -- we're close to the airlines. We see what they're doing to navigate, and we're helping where we can, be that by making sure that the planes they have in their fleets are in the air. That's why we were so pleased to see the LEAP AOG number down to near 0 since the summertime, working on durability, working on cost of ownership and obviously, not only improving deliveries, but bringing those turnaround times that we talked about in our prepared remarks.
There's a lot that we can do operationally to be supportive to our customers at a time when they're navigating some of these fuel pressures. We saw that last Friday with Delta. We do see departures growth, right? Schedules perhaps are being trimmed, but we saw the third quarter up 1%, wide-bodies particularly strong. And we do anticipate that we'll see departures growth in 2027. From a services perspective, and Doug, you know this as well as anybody, I mean that really is what drives this business.
Again, in the third quarter, we saw a very strong performance, orders up 23%, spare parts up even more. I think as a window on how the airlines are preparing not only for the next several months, but the other side of some of these current pressures, the parking lot that we see with respect to our shops is up 20% since the beginning of the year. Removal rates have stayed steady. And just over the last quarter, we've seen parked aircraft and retirements down quarter-on-quarter.
So I think as we look at our business and our overall growth algorithm, we know that we're well positioned to deliver low to mid-single-digit growth in the installed base. We see both LEAP and the nx more or less doubling here over the next 5 years. That, coupled with work scope expansion as the fleet ages, the opportunities we have with respect to price, and I think, again, the airline posture to make sure that they're ready for the other side of this, positions us very well. That's what's behind the bump in the guide for 2026 and what we're saying with respect to 2027.
Now that doesn't mean that we're not mindful of some of these headline pressures that you've cited. We may see some of that pressure down the road. But as we think about 2027, from a GE Aerospace perspective, we think that's primarily driven by the backlog and the cycles that have already been flown by the airlines and how we will support them in addition to what we're doing with our OEM customers, the airframers with respect to new engine and new aircraft deliveries. So net-net, a lot of positives at GE Aerospace, doing what we can to support the airlines as they work through this, and we'll all get to the other side. There's no doubt about that.

**Operator** (Operator):
Our next question comes from Scott Deuschle with Deutsche Bank.

**Scott Deuschle** (Analysts):
Rahul, can you characterize the internal shop visit revenue growth you saw in the wide-body portfolio this quarter and whether there was anything specific that prevented that wide-body growth from being stronger than it was?

**Rahul Ghai** (Executives):
Scott, the overall demand for wide-body shop visits remains really strong. Larry mentioned the removal rates for wide-bodies. And if you see the GE90 and nx, I think we've seen like single-digit retirements all year. So really, really strong fleet performance. The departures were up strongly as well. So that is translating to strong shop visit demand. And in addition to that, the work scopes for wide-body shop visits continue to grow as well, especially on GE90 as they're transitioning from first to second shop visit, which is to be expected, just given the fact that 70% of the GE90 fleet has not seen a second shop visit. And nx is also now moving from kind of the quick turns to the first shop visit. So that is transitioning well as well.
So the total volume is up just given the fleet dynamics around wide-body, very few retirements, the parking lot is up and then the increase in work scopes. So the overall wide-body did really well for us in the quarter. Now overall, for shop visits, the wide-body mix was kind of partially offset by our total customer mix, skewed a little bit towards more long-term service agreements versus the time and material contracts. And then LEAP was obviously up 40% year-over-year. And while the work scopes on LEAP are growing, they're still -- it's an early-stage fleet. So that impacts our overall shop visit revenue growth. But wide-body specifically was very strong.

**Operator** (Operator):
Our next question comes from Myles Walton with Wolfe Research.

**Myles Walton** (Analysts):
I think there was some expectation, at least on my part, that CES service orders might decline sequentially given delinquencies building and the macro backdrop that obviously didn't play out here. Is that something we should normalize to expect that delinquencies will have a role? And then just, Rahul or Larry, within the context of your low double-digit expectation for '27 growth, do you see a burn down of delinquency? Or are you just assuming you're kind of holding this level?

**Rahul Ghai** (Executives):
Yes. I can start, Myles, on services orders and Larry can jump in here as well. So as you pointed out, really strong quarter on CES orders. Orders up 23% year-over-year in the quarter, as Larry said earlier, up 30% year-to-date, with spare parts actually growing faster than the overall strong growth in both CFM56 and LEAP. And the other thing we mentioned in our prepared remarks as well that what was really good to see that the orders growth actually accelerated from 22% growth in the second quarter to now 23% and then orders grew sequentially as well. So both from a year-over-year perspective and quarter-over-quarter perspective, the CES orders did well for us. 
And we are entering the fourth quarter with about 95% of our revenue in our backlog, which has been consistent. It is up maybe 10 points from where it used to be, but I think it's consistently hovered in that range throughout the year. So -- and that is what gave us the confidence to increase our total services revenue guide for the year. Most of the increase that you see here for about $0.5 billion that we are doing in the full year is coming from incremental spare parts sales due to the strong orders that we are seeing.
The internal shop visit revenue is kind of hanging in there in that mid-20s range as well. So no change on that front. But our total backlog is up on spare parts sales, delinquency is up slightly, even though material availability continues to get better, and we are seeing good flow-through from that, just given the strong demand, the backlog and the delinquency grew in the quarter.
So Larry, anything you want to add?

**H. Culp** (Executives):
I think the only thing I would add is when we talk about the services backlog, obviously, the bulk of that are the long-term service agreements. Spare parts is just that, a part of it. And it's spare parts where we're going to see delinquency move in a -- with more frequency. That said, Myles, to the last part of your question, operationally, I think we want to stay focused on bringing down that delinquency. We'd rather take the backlog up to make sure we're satisfying customers with respect to lead times. That said, as Rahul highlighted there at the end, a lot of progress from a supply chain perspective. That's the expectation going into '27.
So I'm hopeful that we can continue to increase our backlog, but at the same time, bring down delinquency because that will be more in line with customer expectations, but work to do.

**Operator** (Operator):
Our next question comes from Sheila Kahyaoglu with Jefferies.

**Sheila  Kahyaoglu** (Analysts):
Maybe I wanted to ask, switching gears a little bit, on wide-body equipment sales in Q3. It reads like you benefited from the GE9X just timing shift on the mid-seal certification. And then if you could also talk about the GEnx, where you are in production ramps for that program as you think about 787 deliveries for your customer, and you've highlighted 50% year-over-year growth in output there.

**H. Culp** (Executives):
We'll talk 9X, then nx. Let me start just with respect to the 9X. Obviously, proud, Sheila, as you know, to be sole source on the 777X, I think we now are looking at in excess of 1,300 engines on order. And the voice of the customer from the airlines is that they love the aircraft, love to see it certified and to see deliveries. With respect specifically to the mid-seal, we've been delivering engines to Boeing with the upgraded mid-seal since August. I think that is just the ultimate proof point with respect to our confidence that we've begun not only production, but also deliveries, working hard to achieve the certification of the upgraded mid-seal, and we're aiming to do that by the end of the year. Obviously, that is subject to FAA approval.

**Rahul Ghai** (Executives):
Okay. And then on GEnx, Sheila, the deliveries were up, as we said in our prepared remarks, more than doubled year-over-year, up more than 60% kind of year-to-date. So we delivered more than 50 engines to Boeing in the quarter. And that delivery to Boeing continued to increase throughout the quarter. So July, August, September, each month was better than the prior month. So clearly, more work to do here to stabilize at the rates that we achieved in September, along with the broader supply chain for what Boeing needs to do in the future, but good to see the growth that we saw in the third quarter and what we've seen year-to-date.
And as Boeing has indicated previously, we're not pacing deliveries. And in fact, Boeing has more than 30 shipsets on and off wing and the number of engines in Boeing inventory has grown over the last few months as the engine deliveries have outpaced the aircraft deliveries. So we're confident we'll continue to grow this and help Boeing get to [ rate 10 ] along with the rest of the supply chain here.

**Operator** (Operator):
Our next question comes from Seth Seifman with JPMorgan.

**Seth Seifman** (Analysts):
I wanted to ask, when we think about the order growth that we're seeing this year and where we are year-to-date, and that's fairly significantly ahead of the outlook that you guys have for sales next year. Can you maybe help to level set us in terms of thinking about how we should consider the relationship between orders and sales and including the relationship within that in terms of shop visits and how those drive orders because you obviously have visibility to a lot more shop visits in the future than what's considered orders. And now that there's this increased focus on the order number, kind of how we should look at this to gauge the outlook?

**Rahul Ghai** (Executives):
Yes. So Seth, again, just going back to the orders, listen, it's been good to see the growth that we've been seeing from all the things that we've discussed here already on the call. If you look at the orders where we're getting the orders growth, a lot of orders growth in CFM56 in the quarter on the spare part sales, CFM56 retirements are trending lower than what we thought at the beginning of the year. Remember, we said 3% to 4%, then at the beginning of the year, we said expecting CFM56 retirements to be 2% to 3%. And now we are expecting somewhere between 1.5 points to 2 points of CFM56 retirements.
So even though we are in the environment that we are in, CFM56 retirements have been lower than where we were at the beginning of the year. And the shop visits for next year, we continue to expect based on the number of cycles flown, as Larry said earlier, at the 2,400 -- closer to the 2,400 mark than the 2,300 mark. So trending higher than -- at the higher end of our range. And along with that, the LEAP spare parts revenue obviously continues to grow as the engine is seeing increased utilization. And then you spoke to the wide-body earlier.
So the order trends have been very strong. And you would expect these orders to convert into revenue typically in the 6- to 9-month time frame. It's been trending longer given the entire expectation from our supply chain, what's happening on the OE side. And even though the material deliveries have been up now for 10 consecutive quarters with double-digit growth this quarter, the conversion time is longer. But if you look at our services growth and our revenue growth, they are trending closer to each other. Services up 30% -- services orders up 30% year-to-date, revenue up 26% year-to-date.
So the trends are converging. And as we think about next year, that is -- it's the backlog that we enjoy right now of $170 billion plus with the -- most of the engines that we need to work in first half of next year already in our shop, plus removals expected for the first half to be up more than 10% year-over-year. So that is what underwrote our confidence here to increase our 2027 outlook to what we were saying kind of double digits previously to low double digits now. But strong backlog, we are anxious to convert that backlog into revenue, as Larry said earlier, but good to be in a position here where we can continue to drive services growth.

**Operator** (Operator):
Our next question comes from Kristine Liwag with Morgan Stanley.

**Kristine Liwag** (Analysts):
So I just wanted to follow up more on -- hey, Larry, following up more on oil prices. I guess your 2027 outlook, you guys are clear that it's driven by what's already in backlog. But for incremental engines coming off wing with service slots beyond that period, are you seeing any changes in customer behavior considering the high oil prices? Are they becoming more price-sensitive? Are they thinking about having lower work scopes? Or when you look at that incremental order, is their decision still factoring maximizing time on wing considering spare parts are still at a scarcity? So just understanding what their trade-off is for that incremental engine kind of beyond your existing backlog?

**H. Culp** (Executives):
Well, Kristine, I think it's important to look not only at the backlog, but what we see kind of in process that's not necessarily in our reported backlogs, but what is indicative of the airline behavior. And again, I think as we look at '27, to the comment that Rahul just made, a good bit of this is a function not only of the backlog, but the cycles that have already been flown.
So when we were talking earlier not only about the very strong spare parts order book that we've seen, but the parking lots of engines that are to be inducted, let alone the engines that are coming off wing, that's been fairly steady and even further back in kind of the operational work stream when we look at parked aircraft and retirements, again, those are down sequentially here in the third quarter. So we think that is in part a function of some of the supply chain constraints that we've touched on a couple of times already in this call, but also the airline posture to navigate through the short term and to be ready for the other side. That just seems to be, in many of the conversations we have with airlines, the enduring lesson of COVID.
They want to be ready for the return to a more stable operating environment. And fortunately, given the combination of the backlog and cycles have been flown, there's an important role that we're going to have to play in that regard as we work through 2027 on top of everything else that we're doing to limit AOGs, reduce turnaround times and improve new engine deliveries to support the airlines as best we possibly can.

**Rahul Ghai** (Executives):
And Kristine, just to add one comment on work scopes. We spoke about the wide-body earlier, just given that we've seen very, very, very few retirements, I think our customers expect to fly those fleets for a long period of time. So we're not seeing any impact to wide-body work scopes. And in fact, the wide-body work scopes are increasing as we discussed earlier. On the narrow-body side, a lot of what we are seeing for CFM56 as an example, is driven by life limited parts, which need to get replaced at this point in their life cycle. And given lack of used material in the market, just given lower retirements, we're not seeing any change to CFM56 work scopes either. And LEAP obviously will continue to grow just given as the fleet matures and we go from quick turns to first shop visits to second shop visits.
In fact, LEAP shop visit revenue on a dollar per shop visit is kind of half that of CFM56, just given how early it is in its life cycle. So I think on both narrow-body and wide-body, overall, we expect the work scopes to increase next year.

**Operator** (Operator):
Our next question comes from John Godyn with Citi.

**John Godyn** (Analysts):
I wanted to just follow up on and maybe get as much color as possible on CFM56 retirement rates. Rahul, you mentioned that it wasn't that long ago that this year was supposed to be a 3% to 4% retirement rate year. And even a year ago, I think we were talking about 2% to 3%. It's obviously much, much lower. We also have things around the edges like aeroderivatives coming up in the conversation. Best thinking today, how are you guys thinking about retirement rates from here? And is it realistic that they can even just snap up quickly from the levels that they're at, given everything that you're seeing? I'd just love your thoughts.

**H. Culp** (Executives):
Well, John, we think about that a lot for perhaps all the obvious reasons. But it's important to step back and just remember that the CFM56 is fundamentally still a young fleet, right? We've got a lot of life left in those engines. 2/3 of the fleet haven't seen their second shop visit. And we know from history that 85% or thereabouts of our near-term volume is going to come from engines that are less than 20 years old, and that's important to remember because retirements tend to kick in for aircraft and engines that are older than 20 years.
I think you saw that again in this very strong third quarter services number that we've talked about, and the CFM56 demand as a component of that was strong. I talked earlier to Kristine's question about what we see from the airlines in terms of capacity management post COVID and how that's playing out both in parked and retired aircraft. We did expect retirements to be, call it, 2% this year. Right now, we're trending below that level. And I think that's probably where we're going to end up.
I think as we think about '27, maybe more importantly, we do think that we'll see a step up. Can that happen operationally? We'll see, but I think it probably is just prudent modeling at a minimum from our perspective to assume that. But even with that assumption, we've raised our expectations for CFM56 shop visits to 2,400 in the summertime. So I think that, again, that speaks to just the strength of the backlog and the demand that we see. And that really is before we factor in some of these power gen effects that you alluded to.

**Rahul Ghai** (Executives):
And on the power gen side, John, what -- we're approaching it kind of 2 ways. One, we are looking at if there is a technical solution that we can offer to some of these customers who are trying to enter that market, right? So there's a technical side to it. But at a minimum, we are selling spare parts because they will need to as they refresh those engines, given the lack of used material, that is creating another revenue stream for us. And it obviously absorbs used material from the market.
So net-net, the power gen is going to be a plus up to our CFM56 revenue stream, which we had not previously factored in when we had given 2028 guidance in the summer of last year. So it should be a positive over and above everything that Larry just said here on kind of the aerospace side.

**Operator** (Operator):
Our next question comes from David Strauss with Wells Fargo.

**David Strauss** (Analysts):
So you've talked about or you've guided to this low double-digit aftermarket growth number in '27. I think you've also previously talked about kind of high single-digit DPT growth. We've got this 9X piece now as we think about kind of the margins on CES in '27. So I just threw out a couple of the different moving pieces. I was just wondering if you could kind of talk puts and takes as we start to think about where 2027 lands.

**H. Culp** (Executives):
David, well, I would -- maybe if I start, I think we're mindful of the puts and takes. We will, as we always do, come back and guide more fully the new year in January at earnings. In addition to some of the company level dynamics that you've referenced, we're obviously mindful that we're going to exceed our 2028 cash outlook here in '26, and we're going to come close to achieving our '28 profit outlook this year as well. So things on balance are clearly trending better despite some of the headlines that we've touched on during the course of this call. So that will all play out, and we'll update the guide for '27 when we're together [ 1st ] of the year.

**Rahul Ghai** (Executives):
Yes. And then as we think about kind of on the revenue side, I think you've hit on the key things here, David, expecting we've hit that multiple times on the call. Services up kind of low double digits for the year. And again, to Seth's earlier question, the orders growth has been very strong year-to-date. But obviously, early in the cycle, we'll update that here in Jan. But given where we are in the cycle and given the environment, maintaining some level of conservativeness in our low double-digit number for next year. DPT, as you said, should be high single digits for next year.
So as we think about our profit dynamics here, the big thing is going to be the drop-through expectation from our low double-digit services growth number. So -- and this is off the higher jumping off point here in 2026. So at the low double-digit level, that's about $3.5 billion to $4 billion of revenue growth and expecting services margins to be flat. Even though LEAP is growing and LEAP is not yet at the overall CES service margins levels, we do expect that given the performance in the other product lines, we'll be able to more than hold the overall CES service margins for next year.
Now the other part is that OE is going to continue to grow and perhaps grow faster than services and 9X is going to ramp as well. And on 9X, there are kind of 2 things happening. One, our number of engines that we're going to ship to Boeing is going to grow from what we've done this year. The cost per unit is coming down meaningfully as we go from even '25 to '26, expecting another step down here as we get into 2027. But the combination of volume growth and -- partially offset by cost, the 9X losses, we think, is going to be about another $300 million of headwind on a year-over-year basis as we get into 2027 over 2026.
And then on DPT, as you said, we expect high single-digit revenue growth and then a little bit of margin expansion on that. So you put all that together, we expect strong profit growth driven by services contribution, DPT contribution and partially offset by OE. But we think that just as we are doing this year with the 9X ramping, we also expect that 2027 margin should stay in line with where we are in 2026. So we've said it all along that even though 9X is growing, we should be able to maintain our margins for the year. We've demonstrated that in 2026 with margins up maybe slightly now over 2025 and then expecting to hold margins in line with 2026 for '27.
And then as we get into '28 and beyond, we should start seeing margin expansion as the 9X headwind starts to come down and LEAP services margins get to overall total services margin. So that is another offset that we should see as we get into '28 and beyond.

**Operator** (Operator):
Our next question comes from Noah Poponak with Goldman Sachs.

**Noah Poponak** (Analysts):
Rahul, there's been a decent amount of discussion on -- here on the aftermarket inputs. Just given you have 2026 and 2027 growth guidance now, can you quantify what you have in '26 growth and '27 growth for LEAP shop visit growth and CFM56 shop visit growth just as we continue to try to understand the shape of the narrow-body handoff within your aftermarket?

**Rahul Ghai** (Executives):
Yes. So on CFM56, Noah, I would think that it's largely flat. I don't think we're seeing a lot of growth in CFM56 shop visits. It's in that, as you said previously, 2,300 to 2,400 range, kind of in that, 2027, maybe you see a little bit of growth towards the higher end that Larry said a minute ago on the CFM56 question. So we expect maybe a little bit of growth. And LEAP, we are -- we haven't quantified the number of shop visits, but we are experiencing strong growth this year, as we said, about 40% growth in the quarter. And then we had similar growth in the first half as well. So I think the LEAP shop visits were up more than kind of in that 50% range even for first half.
So strong growth on LEAP shop visits this year. And then as we get into 2027, it gets to be what -- along with our long-term guidance that we provided that the LEAP shop visit should be up kind of in that 25% CAGR from now till 2030. So a little bit of steadiness in the LEAP shop visit growth maybe from that 40% growth that we're seeing in the third quarter to about maybe 25%, 26% growth in 2027.

**Blaire Shoor** (Executives):
Liz, we have time for one last question.

**Operator** (Operator):
This question comes from the line of Gavin Parsons with UBS.

**Gavin Parsons** (Analysts):
I know it's still a little bit early, but I was hoping you could go into the CPP-enhanced cooling in a little bit more detail given for years, it's all just been engines running hotter.

**H. Culp** (Executives):
Well, it is early. I think what we wanted to make sure everybody understood was, in effect, the primary reason we're at CPP clearly is to have a platform to continue to invest in capacity for ourselves and for others. We think CPP is a wonderful business in that regard. We have no intention of being a captive provider. We'll support ourselves and others as we grow that business. But this idea of being able to partner up more closely with CPP to bring development and manufacturing closely together with respect to these next-gen airfoils is really an important part of the value proposition from a GE Aerospace perspective.
It's important to remember that when we talk about this, it comes back to these customer requirements for durability and efficiency. What we're working on will be applicable to both the current fleet and next-generation programs. So it's not just about technology that will be fielded in the next decade. There'll be more to come later, but what I'd say is I think we're about 3,000 endurance cycles along in the development process. So good learning, good progress in that regard. More to come with respect to just the levels of improvement in engine performance and the timing with respect to commercialization. And everything we've talked about, at least with respect to '27 and even our longer-term outlook, doesn't take any of the potential time on wing benefits into account yet.
So it's early. We've got to work through the regulatory process, obviously, continue to think that we're looking at next summer with respect to approvals, but the customer feedback has been good. The response from the CPP team, the broader team, as they have learned about our partnership, has been very positive. And I'd say 6, 7 weeks in since the announcement, we're even more excited about the potential here than we were when we brought forward the formal news.

**Blaire Shoor** (Executives):
Larry, any final comments to wrap the call?

**H. Culp** (Executives):
Blaire, thank you. Just to close, I'd say our focus remains clear: deliver for customers, improve time on wing and lower cost of ownership. With FLIGHT DECK, we are turning these focus areas into measurable results. We have more to do, for sure, but we are confident in our path ahead and the long-term value creation for our customers and our shareholders. So I'll wrap by just thanking everybody for their time today and your continued interest in GE Aerospace.

**Operator** (Operator):
Thank you, ladies and gentlemen. This concludes today's conference. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GE_Q2_2026_Earnings_Call_20260716.md
- 2026-07-16｜CFO｜guidance：全年營收財測上調至高個位數後段（high teens），原為低雙位數（原話："revenue to grow high teens, up from prior outlook of low"）
- 2026-07-16｜CFO｜guidance：CES 成長財測上調至約 20%，原為中十位數（原話："We expect CES growth of around 20%, up from prior outlook"）
- 2026-07-16｜CFO｜guidance：CES 營業利潤財測區間上調（原話："CES operating profit is now expected to be in the range of"）
- 2026-07-16｜CFO｜guidance：全年 EPS 財測上調，中點加 0.35 美元（原話："we are raising our EPS guidance to a range of $7.65 to $7.85"）
- 2026-07-16｜CFO｜guidance：自由現金流財測上調（原話："We are also raising our free cash flow guidance to $8.9"）
- 2026-07-16｜CFO｜guidance：稅率預期低於 16.5%（原話："below 16.5% for the year"）
- 2026-07-16｜CEO｜guidance：下半年出勤（departures）預期溫和回升（原話："a gradual return to modest departures growth"）
- 2026-07-16｜CFO｜margin：第二季公司毛利率（營業利潤率）年減 130bp 至 21.7%，管理層歸因（原話："decreased 130 basis points to 21.7% from installed engine"）
- 2026-07-16｜CFO｜margin：CES 利潤率年減 160bp 至 27.3%，歸因含 GE9X（原話："160 basis points to 27.3% from installed engine growth"）
- 2026-07-16｜CFO｜margin：管理層定義 spare parts delinquency 的口徑（原話："which represents shipments that have been delayed due to"）
- 2026-07-16｜CFO｜margin：spare parts delinquency 第二季較上季成長 20%（原話："grew 20% sequentially in the second quarter"）
- 2026-07-16｜CFO｜margin：管理層稱利潤率壓力為時間性而非結構性（原話："There's nothing structural that is causing us to have this"）
- 2026-07-16｜CFO｜margin：GE9X 虧損預期 2028 年見頂（原話："we expect those losses to peak by the time we get into 2028."）
- 2026-07-16｜CFO｜commitment：LEAP 服務利潤率 2028 年與整體服務組合持平（原話："LEAP services margins to be in line with our total services"）
- 2026-07-16｜CFO｜commitment：2028 年起 CES 與公司整體利潤率擴張（原話："would expect margin expansion in '28 and beyond."）
- 2026-07-16｜CFO｜commitment：2026 年 spare parts 目錄價格策略與去年一致（原話："our pricing approach for on spare parts catalog for this"）
- 2026-07-16｜CFO｜margin：較高單價的 shop visit 約 2028–29 年起反映於營收，LEAP 2030 年利潤率回到 CFM56 水準（原話："higher-priced shop visits will start showing up"）
- 2026-07-16｜CEO｜commitment：LEAP-1B 耐久套件全面切換時程（原話："full MRO and new-make cutover expected early next year"）
- 2026-07-16｜CEO｜commitment：2027 年 Commercial Services 維持雙位數成長的中期框架（原話："no reason '27 should diverge from that double-digit"）
- 2026-07-16｜CFO｜commitment：自由現金流隨獲利成長，但轉換率會正常化（原話："So we do expect cash flow to grow here with earnings, but"）
- 2026-07-16｜CFO｜guidance：第三季 95% 以上 spare parts 營收已在 backlog（原話："more than 95% of spare parts revenue in"）
- 2026-07-16｜CFO｜guidance：已下機與計畫拆下引擎超出全年 shop visit 指引 40% 以上（原話："exceed our full year shop visit guide by over 40%."）
- 2026-07-16｜CEO｜customer：上半年出勤大致持平，未見客戶行為改變（原話："First half departures were roughly flat, but we have not"）
- 2026-07-16｜CEO｜risk：管理層稱需求可能變動（原話："demand could evolve from here"）
- 2026-07-16｜CEO｜risk：管理層稱瓶頸在供給端而非需求（原話："it's much more a supply side challenge than it is demand"）
- 2026-07-16｜CFO｜customer：年中 spare parts 訂單約 40% 的高點已出現正常化（原話："Those are exceptional results and kind of honestly"）
- 2026-07-16｜CFO｜product：LEAP 外部通路占比預期 2030 年升至約 30%（原話："we expect that to grow to, say, 30% by the time we get to"）
- 2026-07-16｜CFO｜product：LEAP shop visit 2030 年前年複合成長約 25%（原話："a 25%-ish CAGR from now till 2030"）
- 2026-07-16｜CEO｜product：LEAP-1A 已有逾四成機隊裝耐久套件（原話："we now have over 40% of the fleet equipped with the"）
- 2026-07-16｜CEO｜product：耐久套件不會帶來工作量提前加速（原話："It really won't be something that will trigger an"）
- 2026-07-16｜CEO｜customer：管理層承認客戶對持有成本與翼上時間的疑慮（原話："So not in any way declaring victory here."）
- 2026-07-16｜CFO｜capital_allocation：股數年減 2400 萬股（約 2%），來自先前宣布的資本配置行動（原話："Share count was down 24 million from 2% --"）
- 2026-07-16｜CEO｜competition：第二季後敘事：管理層稱四月不上調財測的決定會重來一次（原話："play April all over again in the same way that we did."）
- 2026-07-16｜CFO｜customer：spare engine 比率因安裝引擎出貨成長而下降，LEAP 終身約 10–12% 成熟水準（原話："very close to 10% to 12%"）
- 2026-07-16｜CFO｜risk：CFM56 工作範圍預期穩定至 2028–29（原話："work scopes should remain stable from now till '28, '29"）
- 2026-07-16｜CEO｜risk：Ryanair 1879 航班調查，CFM 協助（原話："assisting with the investigation into Flight 1879."）
- 2026-07-16｜CEO｜product：XA102 適應循環引擎完成組裝準備審查（原話："We completed an assembly readiness review for the XA102"）

### 問答異常語氣（迴避／改口／保留）
- GE_Q2_2026_Earnings_Call_20260716.md｜問：Seifman：今年強勁是否為提前拉貨（pull forward）？｜答法：Culp 未正面回答是否提前拉貨，改談供應鏈進展與 2027 年框架
- GE_Q2_2026_Earnings_Call_20260716.md｜問：Liwag：是否對 CES 利潤率 >30% 有明確能見度｜答法：Ghai 未給 30% 數字，僅說 2028 年後利潤率擴張並列三項壓力

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
{"date":"20260717","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"裝機基數年金按引擎老化的物理節奏自動兌現——收入來自法規強制的維修義務，不來自客戶的採購意願"},{"id":"H2","text":"2028 年 margin 拐點兌現——GE9X 虧損見頂、LEAP 服務利潤率對齊組合、post-launch 定價入帳，三者同時發生使 CES margin 由收縮轉擴張"},{"id":"H3","text":"終端倍數收斂而非維持——2031 年市場給一家成長減速至約 10% 的成熟航發franchise 約 30x，而非現在的 44.6x"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"FR1879 調查導向 CFM56-7B 強制檢查 AD，低毛利合規工作排擠高毛利大修產能。機制：2026-07-10 Ryanair FR1879（737-800，CFM56-7B）非包容性風扇葉片失效，碎片擊碎客艙窗、旅客部分被吸出；北馬其頓 AAIIC 主導，NTSB／FAA／EASA／Boeing／CFM 參與。先例極具體：2018 年西南航空 1380（同型引擎、致命）後 FAA 發出的 AD 要求全機隊風扇葉片榫槽超音波／渦流檢查＋重新設計進氣道，合規期限一路展延至 2028-07-31——這類強制檢查案的執行週期是數年且長期佔用 MRO 產能。而 GE 的 MRO 系統目前超訂 40%、備品延交環比 +20%，沒有任何餘裕吸收插隊工作。直接撞 H2（2028 margin 拐點）。"},{"id":"R2","text":"GE 自建的外部 MRO 通路稀釋自身捕捉的經濟價值——LEAP 第三方 shop visit 占比 2024 年約 10% → 2025 年約 15%（近乎翻倍）→ 2030 年目標約 30%；MTU 沃斯堡新廠 2026-07-08 導入首具 LEAP-1B。這是產能瓶頸下的必要選擇（否則無法消化 25% 年複合的量），但代表越來越大比例的 shop visit 毛利流向第三方。「LEAP shop visit 總量 +25% 年複合」與「GE 自身捕捉的毛利成長」不是同一件事——若把前者當後者用，2028 年後的 margin 擴張斜率會被系統性高估。"},{"id":"R3","text":"航空需求結構性放緩 → 航空公司信用惡化 → shop visit 遞延。已出現的第一個數據點：1H26 departures 大致持平（管理層預期下半年才「回到溫和成長」）；高油價擠壓航空公司（分析師 Scott Mikus 直接就此提問）；CEO 自承航空公司重整「很難想像會在明年下半年或 '28 之前大量出現」——亦即他認為會出現，只是不在 12 個月內。裝機基數決定「是否要修」，departures 決定「何時要修」——而後者驅動 1-2 年的 EPS 節奏，正是 IRR 最敏感的變數。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"次年度共識 Fwd PE ≤ 35x（今日＝$305，為 13 週前價位）；或 FY2028 財測確認 CES margin 擴張＋GE9X 虧損見頂 → 門檻升至 ~$350","irr_base_pct":5.4,"ev5y_pct":19.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":1.3,"ev5y_pct":19.0,"irr_base_pct":5.4,"max_dd_pct":-50.0,"bull_5y_price":540.75,"bear_5y_price":196.4,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"次年度共識 Fwd PE ≤ 35x（今日＝$305，為 13 週前價位）；或 FY2028 財測確認 CES margin 擴張＋GE9X 虧損見頂 → 門檻升至 ~$350","price_at_dd":345.73,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
