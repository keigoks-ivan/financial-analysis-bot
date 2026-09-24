你是 stock-analyst **v20 判斷 agent**，標的 DDOG（20260924）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"DDOG","date":"2026-09-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20260924/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20260924/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":1121.454,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；YoY +35.6%（去年同期 826.760）、QoQ +11.4%（+115.0M，公司稱為史上最大單季增量）"},"note":"Zacks 共識約 1.08B，超出約 3.8%（來源：Yahoo Finance／Zacks 轉載）；也高於公司自家 Q2 指引上緣 1.08B（指引 1.07–1.08B）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income／margin","value":257.031,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（利益率 22.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；含 DASH 年會成本約 15M（CFO 電話會）"},"note":"高於公司自家指引 225–235M（利益率 21–22%）；分析師共識未查得"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income／margin","value":5.455,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（利益率 0.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）"},"note":"未查得共識（GAAP 端與 non-GAAP 差 251.6M，主要是股權激勵）"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":278.704,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（FCF 利益率 24.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；營業現金流 315.872M，扣 capex 與資本化軟體後（Q2 單季由上半年累計減 Q1 推得約 9.9M + 27.3M）"},"note":"未查得共識"},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation（占營收／占 non-GAAP 營業利益）","value":220.251,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（占營收 19.6%；占 non-GAAP 營業利益 85.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；分項：營收成本 9.256M、R&D 131.682M、S&M 47.098M、G&A 32.215M。GAAP 營業利益僅 5.5M，故不以 GAAP 為分母"},"note":"不適用"},{"id":"f_kpi5_guidance_q3_fy2026_reven","label":"Guidance: Q3 FY2026 revenue","value":"1135–1145","period":"Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026","unit":"USD M（YoY +28–29%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；CFO 稱指引已計入最大客戶用量下降（該客戶已續約）"},"note":"Q3 營收共識未查得"},{"id":"f_kpi6_guidance_q3_fy2026_non_g","label":"Guidance: Q3 FY2026 non-GAAP operating income／EPS","value":"營業利益 260–270M（利益率 23–24%）；non-GAAP EPS 0.63–0.65（約 378M 稀釋股數）","period":"Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026","unit":"USD M／USD per share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）"},"note":"未查得 Q3 共識"},{"id":"f_kpi7_guidance_fy2026_revenue_","label":"Guidance: FY2026 revenue／non-GAAP operating income／EPS","value":"營收 4450–4470M（YoY +30%）；non-GAAP 營業利益 1010–1030M（利益率 23%）；non-GAAP EPS 2.50–2.54（約 376M 稀釋股數）","period":"Q2 FY2026 財報公告於 2026-08-06，指引期間 FY2026","unit":"USD M／USD per share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2026 財報公告於 2026-08-06，指引期間 FY2026","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；CFO 另給：淨利息及其他收入約 180M、現金稅 30–40M、non-GAAP 稅率 21%、capex＋資本化軟體占營收 4–5%"},"note":"FY1 EPS 共識 2.53（2026-09-19 快照，來源：dd_numbers_extra.py consensus_revision），落在指引 2.50–2.54 內"},{"id":"f_kpi8_non_gaap_gross_margin_pr","label":"Non-GAAP gross margin（公司未單獨揭露 product gross margin）","value":79.6,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）：non-GAAP 毛利 892M；GAAP 毛利 881.341M（78.6%）出自 8-K Ex-99.1"},"note":"未查得共識；管理層稱毛利率長期在 80% 上下波動"},{"id":"f_kpi9_customers_with_arr_100k","label":"Customers with ARR ≥ $100k","value":4720,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"家（占 ARR 約 91%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 investors.datadoghq.com Q2 2026 press release；占 ARR 比率出自 Q2 財報電話會"},"note":"不適用"},{"id":"f_kpi10_total_customers","label":"Total customers","value":33400,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"家","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CEO 準備稿（2026-08-06）"},"note":"不適用"},{"id":"f_kpi11_ai_native_1m_1m_arr_ai","label":"AI-native 客戶群：年支出 ≥$1M 家數（公司未揭露全公司 ≥$1M ARR 家數，此為 AI 群組口徑）","value":31,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"家（其中年支出 ≥$10M 為 8 家；AI 客戶群共約 750 家）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）"},"note":"不適用"},{"id":"f_kpi12_net_revenue_retention_tr","label":"Net revenue retention（trailing 12 個月）／gross revenue retention","value":"NRR 低 120%（low 120s）；GRR 中後段 90%（mid- to high 90s）","period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"%（公司只給區間，未給精確值）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）"},"note":"不適用"},{"id":"f_kpi13_rpo_current_rpo","label":"RPO／current RPO","value":3470,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（YoY +43%；cRPO YoY 約 +40%，RPO 期間拉長）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[13]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）；公司稱營收比 billings／RPO 更能反映業務趨勢"},"note":"未查得 RPO 共識"},{"id":"f_kpi14_billings","label":"Billings","value":1180,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD M（YoY +38%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[14]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CFO 準備稿（2026-08-06）"},"note":"未查得共識"},{"id":"f_kpi15_ai_yoy","label":"非 AI 客戶營收 YoY 成長","value":"高 20%（high 20s）","period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"%（公司只給區間）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[15]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"Q2 2026 財報電話會 CEO／CFO 準備稿（2026-08-06）"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-06","period":"2026-08-06","unit":"date","basis":"距今 35 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-06"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ddog_gross_margin_pct","label":"DDOG 毛利率","value":79.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ddog_operating_margin_pct","label":"DDOG 營業利益率","value":0.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ddog_fcf_margin_pct","label":"DDOG FCF 利潤率","value":27.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pltr_gross_margin_pct","label":"PLTR 毛利率","value":84.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pltr_operating_margin_pct","label":"PLTR 營業利益率","value":42.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pltr_fcf_margin_pct","label":"PLTR FCF 利潤率","value":54.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_crm_gross_margin_pct","label":"CRM 毛利率","value":77.28,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_operating_margin_pct","label":"CRM 營業利益率","value":21.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_fcf_margin_pct","label":"CRM FCF 利潤率","value":34.49,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_now_gross_margin_pct","label":"NOW 毛利率","value":74.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_now_operating_margin_pct","label":"NOW 營業利益率","value":11.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_now_fcf_margin_pct","label":"NOW FCF 利潤率","value":31.03,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msft_gross_margin_pct","label":"MSFT 毛利率","value":67.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msft_operating_margin_pct","label":"MSFT 營業利益率","value":46.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msft_fcf_margin_pct","label":"MSFT FCF 利潤率","value":20.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":251.49,"period":"2026-09-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":103.98,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":59.86,"period":"2026-09-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.53 → 2.53）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.97 → 2.97）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.75 → 3.75）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.53,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.97,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.75,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.55,"period":"2026-06-23 → 2026-09-19","unit":"%","basis":"FY1 共識 EPS 2.42 → 2.53（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":502.98,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝40.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":40.8,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":22.77,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":21.83,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":99.4,"period":"2026-09-19","unit":"x","basis":"分母＝FY1 EPS 2.53，分子＝快照價 251.49","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-19"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-09-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 251.49 / W52 177.7 / W104 153.06 / W250 125.94 / W250 13週斜率 0.65%"},{"id":"f_ma_w52","label":"52 週均線","value":177.7,"period":"2026-09-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":153.06,"period":"2026-09-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":125.94,"period":"2026-09-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.65,"period":"2026-09-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Ramp 供應商頁：截至 2026 年 9 月，在有採用可觀測性(Observability)類供應商的組織中，34% 使用 Datadog，較去年同期持平（頁面寫 0% YoY、up <1 percentage point）；Datadog 在該類別排名第 2，月對月維持排名。搜尋摘要另出現 8 月版本文字為 down <1pp，方向皆為約持平。頁面未載明樣本口徑。","source":"https://ramp.com/vendors/datadog (Ramp「Datadog Ramp Rate: A Data-Backed Look」)","as_of":"2026-09-01","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Gartner 2026 Magic Quadrant for Observability Platforms：Datadog 連續第 6 年入選 Leader，並在 Ability to Execute 軸位置最高（Datadog 新聞稿自述）。","source":"GlobeNewswire：Datadog Named a Leader in the 2026 Gartner Magic Quadrant For Observability Platforms For Sixth Consecutive Year — https://www.globenewswire.com/news-release/2026/07/15/3328024/0/en/datadog-named-a-leader-in-the-2026-gartner-magic-quadrant-for-observability-platforms-for-sixth-consecutive-year.html","as_of":"2026-07-15","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"FinancialContent 評論文章稱：Palo Alto Networks 收購 Chronosphere、Snowflake 收購 Observe，是把資料儲存、資安與監控合併成單一平台的趨勢，文章形容為對 Datadog 的「Pincer」夾擊威脅；並稱 Dynatrace 是企業市場「chief rival」（Davis AI 歷來被視為較成熟，但 Bits AI 推出後差距縮小），Cisco 正把 Splunk 的日誌優勢與網通硬體整合、主攻傳統企業。此為第三方評論文章的描述，非份額數據。","source":"FinancialContent：Datadog (DDOG) and the 2026 Observability Frontier: Navigating the AI Re-Architecting Phase — https://www.financialcontent.com/article/finterra-2026-1-27-datadog-ddog-and-the-2026-observability-frontier-navigating-the-ai-re-architecting-phase","as_of":"2026-01-27","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Datadog's largest customer renewed a nine-figure agreement but reduced its usage; per the search summary of the TheStreet article, this affected the company's Q3 and full-year 2026 forecasts. Article body not retrieved (WebFetch returned 403), so the exact contract figures and whether the usage cut involved in-house or a second vendor are not confirmed.","source":"TheStreet, 'Datadog's largest customer renews deal but cuts usage' https://www.thestreet.com/investing/stocks/datadogs-largest-customer-renews-deal-but-cuts-usage","as_of":"2026-08-06","affects":["thesis.R","decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"SaaStr states 'OpenAI is Datadog's biggest single customer' (analyst assessment, not a company-named disclosure), and that the AI-native cohort including it grew only 'high single digits' in Q1 2026.","source":"SaaStr, 'Datadog Stock Is Up +66%. Here Are 5 Reasons Why...' https://www.saastr.com/datadogup/","as_of":"2026-05-25","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"+","claim":"SaaStr reports the largest new logo in Datadog's history was consolidating onto Datadog from 'more than five open-source, commercial, hyperscaler, and in-house' tools, and states 'the AI labs themselves are now choosing Datadog over building in-house'. SaaStr's read is that the new logo is most likely Anthropic; this identity is the outlet's inference, not a company disclosure.","source":"SaaStr, 'Datadog Stock Is Up +66%. Here Are 5 Reasons Why...' https://www.saastr.com/datadogup/","as_of":"2026-05-25","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Per a secondary summary of the FY2025 10-K, Datadog identified an 'AI-native cohort' that 'includes our largest customer', and quantified the cohort's contribution at about seven percentage points of YoY revenue growth for the quarter ended 2025-12-31.","source":"Mungomash, 'Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail' https://mungomash.com/orgs/datadog/financials/ (summarising Datadog FY2025 10-K)","as_of":"2025-12-31","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#4","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Per the same secondary source, one large AI-native customer's decision in early 2024 to scale down and partially re-platform its observability stack onto internal tooling drove the public growth deceleration that began with the Q1 2024 print.","source":"Mungomash, 'Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail' https://mungomash.com/orgs/datadog/financials/","as_of":"2024-05-07","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Q2 2026 法說會：管理層不點名最大客戶，只說是「一家領先的 AI 公司」，使用 17 項 Datadog 產品，剛完成一筆「九位數美元」的續約。續約後用量有下降（usage reduction），已納入 Q3 與 FY2026 財測；CEO Pomel 稱今年剩餘時間的財測已「fully derisked」。","source":"The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","as_of":"2026-08-13","affects":["thesis.R","decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q2 2026 法說會：管理層表示剔除最大客戶後，其餘業務的成長率與整體「幾乎相同」（pretty much the same growth rate as the rest of the business）。","source":"The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","as_of":"2026-08-13","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q2 2026：AI 原生客群超過 750 家，其中 31 家年支出逾 100 萬美元、8 家逾 1,000 萬美元；管理層稱前 10 大 AI 公司「全數」是客戶。公司未在此次法說會把 AI 原生客群量化為占營收的百分比。","source":"The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","as_of":"2026-08-13","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q2 2026：非 AI 客戶營收年增加速至 20% 後段（high 20s%），Q1 為 20% 中段（mid-20s），去年同期為 18%。","source":"GuruFocus, Datadog Inc (DDOG) Q2 2026 Earnings Call Highlights: Revenue Surges 36% to $1.12B, https://www.gurufocus.com/news/9014386/datadog-inc-ddog-q2-2026-earnings-call-highlights-revenue-surges-36-to-112b-aidriven-growth-accelerates","as_of":"2026-08-13","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#4","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q2 2026：過去 12 個月淨營收留存率（NRR）為 120% 出頭（low 120s），毛營收留存率（GRR）為 90% 中後段（mid- to high 90s），管理層稱流失（churn）維持低檔。","source":"The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","as_of":"2026-08-13","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#5","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K（2026-02-18 提交）有「AI-native cohort」一詞，並註明該客群「包含我們最大的客戶」；該客群對 2025 年 12 月底當季營收年增的貢獻約 7 個百分點。（二手來源轉述，未讀到 10-K 原文；未查到 10-K 是否列出單一客戶占營收 ≥10% 的具體百分比。）","source":"mungomash.com「Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail」（搜尋摘要轉述 FY2025 10-K；頁面 WebFetch 回 404，未能直接驗證）","as_of":"2026-02-18","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#6","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Q1 2026 10-Q（2026-05-07 提交）沿用「AI-native cohort 包含最大客戶」的措辭，並把該客群對 2026 年 3 月底當季營收年增的貢獻改寫為「high single digits」（個位數高段）。（二手來源轉述，未讀到 10-Q 原文。）","source":"mungomash.com「Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail」（搜尋摘要轉述 Q1 2026 10-Q；頁面 WebFetch 回 404，未能直接驗證）","as_of":"2026-05-07","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#7","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"外部資料點（Datadog 本身未點名最大客戶是誰，此處的對應是分析師/媒體推測，未經公司確認）：OpenAI 於 2026-03-31 完成 1,220 億美元募資，募後估值 8,520 億美元，同時把循環信貸額度擴大到約 47 億美元，交割時未動用。另有報導稱 OpenAI 帳上無負債，但 2026 年 Q1 燒錢約 37 億美元。","source":"搜尋摘要轉述 Sacra「OpenAI revenue, valuation & funding」(https://sacra.com/c/openai/) 與 The Next Web「OpenAI's suspiciously clean balance sheet is about to get a hard look」(https://thenextweb.com/news/openai-light-balance-sheet-ipo-scrutiny)；各事實對應哪一篇未逐條核對","as_of":"2026-03-31","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner projects the observability platform market will reach $14.2 billion by 2028, driven by complexity in hybrid and cloud-native environments.","source":"Network World, 'In crowded observability market, Gartner calls out AI capabilities, cost optimization, DevOps integration' https://www.networkworld.com/article/4032218/in-crowded-observability-market-gartner-calls-out-ai-capabilities-cost-optimization-devops-integration.html","as_of":"2025-08-06","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Gartner's observability report says more than 40 vendors compete in the space (20 evaluated in the Magic Quadrant), that 'questions about total cost of ownership are now standard', and that leading platforms must offer granular data retention controls, tiered storage and usage-based pricing.","source":"Network World, 'In crowded observability market, Gartner calls out AI capabilities, cost optimization, DevOps integration' https://www.networkworld.com/article/4032218/in-crowded-observability-market-gartner-calls-out-ai-capabilities-cost-optimization-devops-integration.html","as_of":"2025-08-06","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Datadog Q1 2026 revenue was about $1.01B, up 32% YoY (vs 29% in Q4 2025 and 25% in Q1 2025); sequential growth of 6% was the strongest since 2022.","source":"BigGo Finance, '[DDOG Q1 2026 Earnings Call] Datadog Surpasses $1B in Quarterly Revenue as AI Workloads Fuel 32% Growth' https://finance.biggo.com/news/US_DDOG_2026-05-07","as_of":"2026-05-07","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Per the Q1 2026 call as reported, trailing-12-month net revenue retention improved to the low 120% range and gross retention stayed in the mid-to-high 90s.","source":"BigGo Finance, '[DDOG Q1 2026 Earnings Call] Datadog Surpasses $1B in Quarterly Revenue as AI Workloads Fuel 32% Growth' https://finance.biggo.com/news/US_DDOG_2026-05-07","as_of":"2026-05-07","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Datadog guided Q2 2026 revenue to $1.07B-$1.08B (29-31% YoY) and full-year 2026 revenue to $4.30B-$4.34B (25-27% YoY), as reported in the Q1 2026 call summary.","source":"BigGo Finance, '[DDOG Q1 2026 Earnings Call] Datadog Surpasses $1B in Quarterly Revenue as AI Workloads Fuel 32% Growth' https://finance.biggo.com/news/US_DDOG_2026-05-07","as_of":"2026-05-07","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q1 2026 call summary: 22 customers spend over $1M a year on Datadog's AI products (5 above $10M); two hyperscale labs signed seven- and eight-figure annualized deals for training-workload monitoring; 6,500 customers (20% of total, 80% of ARR) use AI integrations.","source":"BigGo Finance, '[DDOG Q1 2026 Earnings Call] Datadog Surpasses $1B in Quarterly Revenue as AI Workloads Fuel 32% Growth' https://finance.biggo.com/news/US_DDOG_2026-05-07","as_of":"2026-05-07","affects":["thesis.H","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner predicts 40% of organizations deploying AI will use AI observability to monitor model performance by 2028.","source":"Gartner press release 'Gartner Predicts 40% of Organizations Deploying AI Will Use AI Observability to Monitor Model Performance by 2028' https://www.gartner.com/en/newsroom/press-releases/2026-05-12-gartner-predicts-40-percent-of-organizations-deploying-ai-will-use-ai-observability-to-monitor-model-performance-by-2028","as_of":"2026-05-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#7","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Grafana Labs reached $400M+ ARR with 7,000 customers as of September 2025 (competitor scale figure cited in a vendor comparison blog; blog publish date not shown, as_of day set to the first of the stated month).","source":"OpenObserve blog, '10 Best Datadog Competitors & Alternatives in 2026' https://openobserve.ai/blog/datadog-competitors/","as_of":"2025-09-01","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Datadog's own export control page (effective 2026-05-05) classifies its observability and security services as ECCN 5D002.c.1 under license exception ENC/740.17(b)(1); automation, incident management and AI products (e.g. Bits AI) as 5D992.c.1 under ENC/740.17(b)(1); and the Datadog Agent and other downloadable products (SDKs, IDE plugins) as EAR99 / NLR (no license required).","source":"Datadog, 'Export Control Information' https://www.datadoghq.com/legal/export-control-information/2026-05-05/","as_of":"2026-05-05","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K（截至 2025-12-31，2026-02-05 提交）把「political turmoil, natural catastrophes, outbreaks of contagious diseases, warfare and terrorist attacks ... such as the conflicts in Ukraine and the Middle East」列為國際營運風險，並提到對俄制裁可能加劇相關趨勢。","source":"Datadog, Inc. Form 10-K FY2025, SEC EDGAR https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm","as_of":"2026-02-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K 經 WebFetch 抽取，全文未出現 China、Taiwan、半導體供應鏈或製造依賴的字樣（純 SaaS，10-K 未揭露實體製造環節）。此為抽取結果，非逐頁人工確認。","source":"Datadog, Inc. Form 10-K FY2025, SEC EDGAR https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm","as_of":"2026-02-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K 載明約 44% 全職員工位於美國以外，其中 34% 在法國。","source":"Datadog, Inc. Form 10-K FY2025, SEC EDGAR https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm","as_of":"2026-02-05","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Datadog 官方部落格稱：「Following a March 2023 outage of our own, Datadog launched a company-wide initiative to improve regional isolation across Datadog sites」，並推出 Disaster Recovery 產品，讓客戶在雲端供應商中斷時維持可觀測性。","source":"Datadog Blog, 'Maintain observability during cloud outages with Datadog Disaster Recovery' https://datadoghq.com/blog/ddr-mitigates-cloud-provider-outages","as_of":"2026-06-09","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"產業層面：雲端集中風險來自過多關鍵流程依賴單一供應商、單一區域或中央服務；AWS us-east-1 是最老、最大的區域，並承載其他區域所依賴的全域控制功能（如 IAM 更新、DynamoDB Global Tables），該區失效會擴散到區域之外。此文為通論，未指名 Datadog 受影響。","source":"cloudmagazin.com, 'One Region Fails, Half of the Supply Chain Grinds to a Halt' https://www.cloudmagazin.com/en/2026/07/12/one-region-fails-half-of-the-supply-chain-grinds-to-a-halt","as_of":"2026-07-12","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 Q2 營收約 $1.12B，年增 36%；上半年營收約 $2.1B，年增 34%（Q1 為 $1,006M、年增 32%）。","source":"Datadog 8-K ex-99.1 (period ended 2026-06-30) https://www.sec.gov/Archives/edgar/data/0001561550/000162828026053829/ex-991x20260630x8k.htm ；GuruFocus「Datadog Q2 2026 Earnings Call Highlights」","as_of":"2026-08-06","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"AI 原生客戶群超過 750 家，其中 31 家年支出逾 $1M、8 家逾 $10M；全球前 10 大 AI 公司皆為客戶。非 AI 營收年增加速至 20% 後段（Q1 為 20% 中段，去年同期 18%）。","source":"Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/ ；GuruFocus Q2 2026 highlights","as_of":"2026-08-06","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"最大客戶出現用量下滑（同時簽了九位數美元續約）；管理層稱已把此影響完整反映在 Q3 與全年 2026 指引，並稱排除該客戶後整體趨勢與加速一致。","source":"Motley Fool, Datadog Q2 2026 Earnings Call Transcript（WebFetch 摘要）https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/ ；GuruFocus Q2 2026 highlights","as_of":"2026-08-06","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"指引：Q3 營收 $1.135B–$1.145B（年增 28%–29%，低於 Q2 的 36%）；全年 2026 營收 $4.45B–$4.47B（年增約 30%）。","source":"GuruFocus, Datadog Q2 2026 Earnings Call Highlights https://www.gurufocus.com/news/9014386/datadog-inc-ddog-q2-2026-earnings-call-highlights-revenue-surges-36-to-112b-aidriven-growth-accelerates","as_of":"2026-08-06","affects":["valuation","thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"客戶結構：總客戶約 33,400（年增約 2,000）；年 ARR≥$100k 客戶約 4,720（去年同期約 3,850，年增 23%），占總 ARR 91%；新客戶貢獻年增量的 30%（Q1 為 25%）；過去 12 個月淨留存率在 120% 出頭，毛留存率在 90% 中後段。","source":"Motley Fool, Datadog Q2 2026 Earnings Call Transcript https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/ ；Datadog 8-K 2026-06-30","as_of":"2026-08-06","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"產品線 ARR（截至 2025 年底、2026-02 報導）：基礎設施監控 ARR 逾 $1.6B；日誌管理與 APM 各自突破 $1B ARR，兩者年增皆在 30% 中段。這是 Q4 2025 資料，非 Q2 2026 最新值。","source":"Yahoo Finance/Zacks, Will Datadog Stock Sustain Growth on Rising AI Cloud Monitoring Spend? https://finance.yahoo.com/news/datadog-stock-sustain-growth-rising-144300289.html","as_of":"2026-02-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"RUM（真實使用者監控）ARR 超過 $200M，年增逾 50%。","source":"Motley Fool, Datadog Q2 2026 Earnings Call Transcript https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/","as_of":"2026-08-06","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"0","claim":"外部分析師共識（Zacks）2026 全年營收預估 $4.08B（年增 19.17%），為 2026-02 舊值，已低於公司 2026-08 指引 $4.45–4.47B；文中無 2027 共識。","source":"Yahoo Finance/Zacks https://finance.yahoo.com/news/datadog-stock-sustain-growth-rising-144300289.html ；GuruFocus Q2 2026 highlights（指引）","as_of":"2026-02-19","affects":["valuation"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"0","claim":"定價結構：APM Pro 約 $23/host/月、APM Enterprise 約 $34/host/月（2026 年牌價），日誌、基礎設施、RUM、Synthetics、SIEM 另計；同類報告稱 New Relic、Dynatrace、Splunk 成本與 Datadog 相近而非大幅便宜，企業議價可壓 35%–55% 牌價。Datadog 與 Dynatrace 投入 OpenTelemetry 相容以維持定價能力。來源為第三方部落格比較，非公司揭露。","source":"Uptrace, Top 10 Observability Tools in 2026 https://uptrace.dev/tools/top-observability-tools ；VendorBenchmark, Observability Platform Pricing Benchmarks 2026 https://vendorbenchmark.com/blog/observability-platform-pricing-benchmark-comparison","as_of":"2026-08-31","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#9","axis":"end_markets","section":"coverage","direction":"0","claim":"市佔（僅為網站偵測指標，非營收佔比）：2026 年 8 月偵測到 Datadog 在 APM 與錯誤追蹤類別占 5.78%，排在 Sentry、New Relic 之後第三；Dynatrace 3.38%、Grafana 2.43%。該指標反映瀏覽器代理程式部署，非客戶數或營收。","source":"Uptrace, Top 10 Observability Tools in 2026 https://uptrace.dev/tools/top-observability-tools","as_of":"2026-08-31","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#10","axis":"end_markets","section":"coverage","direction":"0","claim":"可觀測性市場規模第三方估計落差極大：2026 年 Mordor Intelligence $3.35B（2031 年 $6.93B，CAGR 15.62%）、Coherent $3.40B（CAGR 11.1%）、Business Research Insights $4.35B、MarketsandMarkets $11.91B（CAGR 14.1%）、Research Nester $34.1B。各家 CAGR 在 11%–16%。","source":"Mordor Intelligence https://www.mordorintelligence.com/industry-reports/observability-market ；MarketsandMarkets https://www.marketsandmarkets.com/Market-Reports/observability-tools-and-platforms-market-69804486.html ；Research Nester https://www.researchnester.com/reports/observability-tools-and-platforms-market/8139","as_of":"2026-01-01","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"groundcover（Datadog 競品廠商）2026-07-29 的指南結論稱：2026 年可觀測性品類的轉變是架構面的——以 eBPF 取代語言 agent、以 BYOC（資料留在客戶自己的 VPC）取代純 SaaS、以「依基礎設施計價」取代「依用量計價」。此為競品自家行銷文章的說法，非中立第三方量測。","source":"groundcover, 'Datadog Alternatives for Full-Stack Observability in 2026', https://www.groundcover.com/guides/datadog-alternatives-for-full-stack-observability","as_of":"2026-07-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"IT Connection（Currentanalysis）2026 年觀測性預測稱：應用開發工具類新創將透過在自家產品組合內增加可觀測性功能，對整個可觀測性市場產生破壞性影響（標題：Makers of Dev Tools to Disrupt Space）。搜尋摘要只取得此論點，未取得內文細節與具體廠商名單。","source":"IT Connection / Currentanalysis, 'Observability Predictions 2026: Makers of Dev Tools to Disrupt Space', https://itcblogs.currentanalysis.com/2026/01/29/observability-predictions-2026-makers-of-dev-tools-to-disrupt-space/","as_of":"2026-01-29","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Splunk 官方部落格 2026-03-24 載明：2025 年底至 2026 年初，Palo Alto Networks 收購 Chronosphere、LogicMonitor 收購 Catchpoint、Snowflake 宣布擬收購 Observe Inc.。該文未提及 Datadog、eBPF、OpenTelemetry 或 AI SRE agent 為競爭威脅。","source":"Splunk, 'Ahead of the Curve: How Recent M&A Forecasts New Observability Trends for 2026', https://www.splunk.com/en_us/blog/observability/new-observability-trends-for-2026.html","as_of":"2026-03-24","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"As of Q1 2026, Datadog had over 26 products, of which 5 had crossed $100M ARR and 3 were between $50M and $100M ARR; 18 products were still early in their lifecycle. (Secondary-source figure from a search-result summary; not checked against the primary earnings release.)","source":"Capital Blueprint (Substack), 'Datadog, Inc. (NASDAQ: DDOG) — Deep Investment Analysis', https://capitalblueprint.substack.com/p/datadog-inc-nasdaq-ddog-deep-investment","as_of":"2026-03-31","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 FY2026 財報（2026-08-06）公司把全年營收指引上調至 $4.45B–$4.47B，FactSet 當時共識為 $4.35B；指引區間高於共識約 $100–120M。","source":"MarketScreener — (DDOG) Datadog Expects 2026 Revenue Range $4.45B - $4.47B, vs. FactSet Est of $4.35B — https://www.marketscreener.com/news/ddog-datadog-expects-2026-revenue-range-4-45b-4-47b-vs-factset-est-of-4-35b-ce7f50dddb8df021","as_of":"2026-08-06","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 FY2026 全年非 GAAP EPS 指引為 $2.50–$2.54；營收指引由前次 $4.30–$4.34B 上調至 $4.45–$4.47B（搜尋摘要另稱 Street 為 $4.354B）。","source":"Datadog Q2 FY2026 earnings call transcript (Yahoo Finance) — https://finance.yahoo.com/quote/DDOG/earnings/DDOG-Q2-2026-earnings_call-662123.html（數字取自搜尋摘要，未逐字核對原文）","as_of":"2026-08-06","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 FY2026 財報（2026-05-07）全年營收指引由 $4.06–$4.10B 上調至 $4.30–$4.34B；2026 年內累計為第二次上調。","source":"Datadog Form 8-K Ex-99.1（季度截至 2026-03-31）— https://www.sec.gov/Archives/edgar/data/0001561550/000162828026031677/ex-991x20260331x8k.htm（數字取自搜尋摘要，未 fetch 原文）","as_of":"2026-05-07","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"搜尋摘要稱 Q2 上調全年指引的同時，公司揭露最大客戶用量下降，並引述企業需求與 AI 產品採用為上調依據；Simply Wall St 標題稱股價在此消息後下跌 14.9%（該文未在摘要中註明計算區間）。","source":"Simply Wall St News — Datadog (DDOG) Is Down 14.9% After Raising 2026 Outlook And Deepening AI, Log Partnerships — https://simplywall.st/stocks/us/software/nasdaq-ddog/datadog/news/datadog-ddog-is-down-149-after-raising-2026-outlook-and-deep/amp（僅取搜尋摘要，未 fetch 原文）","as_of":"2026-08-06","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價共 46 位：平均 $285.28、中位數 $295、最高 $330、最低 $158；評級分布 Strong Buy 31／Buy 10／Hold 4／Sell 0／Strong Sell 1，共識評級 Strong Buy。（與現價比較請引 numbers.price_at_dd。）","source":"StockAnalysis — Datadog (DDOG) Stock Forecast & Analyst Price Targets — https://stockanalysis.com/stocks/ddog/forecast/","as_of":"2026-09-16","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"近期個別目標價動作：Wedbush（Steven Wahrhaftig）2026-09-10 開始覆蓋，目標價 $260→$275；Mizuho（Gregg Moskowitz）2026-08-17 重申 $300；Baird（William Power）2026-08-17 維持 $300。","source":"StockAnalysis — Datadog (DDOG) Stock Forecast & Analyst Price Targets — https://stockanalysis.com/stocks/ddog/forecast/","as_of":"2026-09-10","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#6","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"賣方共識 FY2026 營收 $4.47B（年增 30.48%）、EPS $2.53；FY2027 營收 $5.48B（年增 22.53%）、EPS $2.97。FY2026 營收共識位於公司指引 $4.45–$4.47B 區間上緣，EPS 共識 $2.53 落在指引 $2.50–$2.54 區間內。","source":"StockAnalysis — Datadog (DDOG) Stock Forecast & Analyst Price Targets — https://stockanalysis.com/stocks/ddog/forecast/（指引數字引自 MarketScreener／Yahoo 逐字稿摘要）","as_of":"2026-09-16","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Datadog 於 2026-06-30 宣布收購 Adaptive ML（前沿 AI 新創），併入其 AI Research 部門，用於強化可觀測性所需的 world models 與 agentic LLM post-training 研究；文章未揭露價格與交易條款。","source":"GuruFocus, 'Datadog (DDOG) Expands AI Capabilities with Acquisition of Adaptive ML' https://www.gurufocus.com/news/8939503/datadog-ddog-expands-ai-capabilities-with-acquisition-of-adaptive-ml","as_of":"2026-06-30","affects":["moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"10-Q（截至 2026-06-30 的六個月）揭露：期間內簽訂三筆企業收購協議，總購買價格 $191.5M，含現金（扣除取得現金後）$98.5M、遞延收購保留款 $14.3M、發行 796,509 股限制性 Class A 股票。as_of 為期末日，10-Q 實際遞交日未讀取。","source":"Datadog, Inc. Form 10-Q (period ended 2026-06-30) https://www.sec.gov/Archives/edgar/data/0001561550/000162828026054458/ddog-20260630.htm（經搜尋摘要引用，未全文查證）","as_of":"2026-06-30","affects":["moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K 揭露：2025 全年簽訂三筆企業收購協議，總購買價格 $178.4M（現金 $109.3M 扣除取得現金後、遞延保留款 $16.1M、發行 770,044 股限制性 Class A 股票），公司認定個別與合計均不重大。此為全年數字，各筆交易日期未逐筆核對，其中含 2025-05-05 宣布的 Eppo（早於近 12 個月窗口）。","source":"Datadog, Inc. Form 10-K FY2025 https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm（經搜尋摘要引用，未全文查證）","as_of":"2025-12-31","affects":["moat_trend"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"Law360 列有 FUISZ v. DATADOG, INC.（D.D.C.，案號 1:24-cv-01568，2024-05-29 提起，法官 Amit P. Mehta），案件類型標為 'Civil Rights: Jobs'（僱傭類），頁面未顯示目前程序狀態。搜尋未找到針對 Datadog 的證券集體訴訟。","source":"Law360 case page 'FUISZ v. DATADOG, INC.' https://www.law360.com/cases/66573a6e48322902d22d32c8","as_of":"2024-05-29","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Datadog 於 2026-06-30 宣布收購 Adaptive ML（前沿 AI 新創），併入其 AI Research 部門；文章未揭露價格與交易條款。","source":"GuruFocus, 'Datadog (DDOG) Expands AI Capabilities with Acquisition of Adaptive ML' https://www.gurufocus.com/news/8939503/datadog-ddog-expands-ai-capabilities-with-acquisition-of-adaptive-ml","as_of":"2026-06-30","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"10-Q（截至 2026-06-30 的六個月）揭露：期間內簽訂三筆企業收購協議，總購買價格 $191.5M（現金淨額 $98.5M、遞延保留款 $14.3M、796,509 股限制性 Class A 股票）。as_of 為期末日。","source":"Datadog, Inc. Form 10-Q (period ended 2026-06-30) https://www.sec.gov/Archives/edgar/data/0001561550/000162828026054458/ddog-20260630.htm（經搜尋摘要引用，未全文查證）","as_of":"2026-06-30","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#2","axis":"ma_merger","section":"events","direction":"0","claim":"FY2025 10-K 揭露：2025 全年三筆企業收購，總購買價格 $178.4M，公司認定個別與合計均不重大。全年數字，各筆日期未逐筆核對；含 2025-05-05 宣布的 Eppo（早於近 12 個月窗口）。","source":"Datadog, Inc. Form 10-K FY2025 https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm（經搜尋摘要引用，未全文查證）","as_of":"2025-12-31","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"Law360 列有 FUISZ v. DATADOG, INC.（D.D.C.，案號 1:24-cv-01568，2024-05-29 提起），案件類型標為 'Civil Rights: Jobs'（僱傭類，非證券集體訴訟），頁面未顯示目前程序狀態。","source":"Law360 case page 'FUISZ v. DATADOG, INC.' https://www.law360.com/cases/66573a6e48322902d22d32c8","as_of":"2024-05-29","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 23 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"DDOG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.51,"operating_margin_pct":0.43,"fcf_margin_pct":27.04,"rd_intensity_pct":43.69},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"PLTR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":84.8,"operating_margin_pct":42.8,"fcf_margin_pct":54.55,"rd_intensity_pct":10.42},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"CRM","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":77.28,"operating_margin_pct":21.52,"fcf_margin_pct":34.49,"rd_intensity_pct":14.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"NOW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.77,"operating_margin_pct":11.4,"fcf_margin_pct":31.03,"rd_intensity_pct":22.14},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MSFT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.94,"operating_margin_pct":46.78,"fcf_margin_pct":20.19,"rd_intensity_pct":10.72},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"DDOG"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/DDOG/DDOG_Q2_2026_Earnings_Call_20260806.md）

# Q2 2026 Earnings Call
2026-08-06

Q2 2026 Earnings Call
Datadog, Inc. | Earnings Calls | 2026-08-06
Operator (Operator)
Good day, and thank you for standing by. Welcome to the Q2 2026 Datadog Earnings Conference Call.
[Operator Instructions] Please be advised that today's conference is being recorded. I would now like to
hand the conference over to your first speaker today, Yuka Broderick, Senior Vice President of Investor
Relations. Please go ahead.
Yuka Broderick (Executives)
Thank you, Lauren. Good morning, and thank you for joining us to review Datadog's second quarter
2026 financial results, which we announced in our press release issued this morning. Joining me on the
call today are Olivier Pomel, Datadog's Co-Founder and CEO; and David Obstler, Datadog's CFO.
During this call, we will make forward-looking statements, including statements related to our future
financial performance, our outlook for the third quarter and the fiscal year 2026 and related notes and
assumptions, our product capabilities and our ability to capitalize on market opportunities.
The words anticipate, believe, continue, estimate, expect, intend, will and similar expressions are
intended to identify forward-looking statements or similar indications of future expectations. These
statements reflect our views today and are subject to a variety of risks and uncertainties that could
cause actual results to differ materially. For a discussion of the material risks and other important
factors that could affect our actual results, please refer to our Form 10-Q for the quarter ended March
31, 2026.
Additional information will be made available on our upcoming Form 10-Q for the fiscal quarter ending
June 30, 2026, and other filings with the SEC. This information is also available on the Investor
Relations section of our website, along with a replay of this call. We will discuss non-GAAP financial
measures, which are reconciled to their most directly comparable GAAP financial measures in the
tables in our earnings release, which is available at investors.datadoghq.com.
With that, I'd like to turn the call over to Olivier.
Olivier Pomel (Executives)
Thanks, Yuka. Thank you all for joining us to go over our Q2 results. Let me begin with this quarter's
business drivers. Our revenue growth in Q2 has accelerated across our customer base. On one hand,
our AI native customer cohort continued to grow and diversify, both in the number of customers we
serve and the scale of those customers.
On the other hand, and as a great illustration of the breadth of trends across our business, revenue
growth for our non-AI customers also accelerated again this quarter to the high 20s percent year-over-
year, up from the mid-20s last quarter and 18% in the year ago quarter. Overall, we continue to see
healthy trends in customer demand. Our broad base of customers, from the most nimble startups to the
largest and most established enterprises, are all adopting AI. We think this is accelerating their usage of
cloud and modern technologies, as well as their usage of the Datadog platform to observe, secure, and
act on their cloud and AI workloads.

Regarding our Q2 financial performance and key metrics, revenue was $1.12 billion, an increase of 36%
year-over-year and above the high end of our guidance range. We ended Q2 with about 33,400
customers, up from about 31,400 a year ago. We also ended with about 4,720 customers with an ARR
of $100,000 or more, up from about 3,850 a year ago. These customers generated about 91% of our
ARR. And we generated free cash flow of $279 million with a free cash flow margin of 25%.
Turning to product adoption. Our platform strategy continues to resonate in the market. For example,
58% of our customers now use 4 or more products, up from 52% a year ago. 37% of our customers use 6
or more products, up from 29% a year ago, and 13% of our customers use 10 or more products, up from
7% a year ago. We're landing more customers and delivering value across more products, our products
are broadly delivering strong growth in usage and ARR. As an example, RUM, or Real User Monitoring,
now exceeds $200 million in ARR and accelerated at its scale to over 50% growth year-over-year. Our
customers are sending more user sessions and using RUM in conjunction with our newer Product
Analytics to optimize their business outcomes.
Moving on to R&D. We held our DASH user conference in June, where we announced over 100 exciting
new products and features for our users. Let's go through some of the announcements. First, we
expanded Bits AI to accelerate and automate the DevOps loop. This is the loop that goes from detection
to investigation to remediation that engineers go through each time something breaks. At DASH, we
announced a lot of new Bits capabilities for the DevOps loop. Bits can now create and maintain
monitors, identify root causes within minutes of a negative signal, recommend and implement fixes,
follow guardrails to add safety and controls, continuously learn and improve from prior incidents, and
detect symptomatic behaviors early to repair infrastructure issues before they escalate.
Second, we announced Bits AI products to address the development loop. This is the loop that goes
from coding to delivery to evaluation that developers navigate to get code to production. For this loop,
Bits Release now acts as an AI release validation agent, analyzing the impact of code changes, running
end-to-end checks, and verifying production rollouts. Bits Code generates code fixes, guaranteeing
every fix and reproduction behavior and Bits Testing also automates synthetic test generation and
maintenance.
Third, we expanded Datadog for AI, our products that observe, secure, and optimize the AI stack from
end to end.
Data Observability enables companies to trust the data being used by AI with lineage quality
monitoring and jobs monitoring. Bits Data Analysis uses a rich data context to accurately answer
business questions. And Agent Console provides visibility into AI agent usage, cost, and effectiveness.
In Agent Observability, our patterns capability automatically clusters user interactions into behavior
groups to identify quality or cost issues and Bits Evals handles the repetitive parts of the agent
development loop in order to improve the outcomes of agents.
Fourth, we are broadening our platform to ingest, correlate, analyze, and act on more data, whether on-
prem or in the cloud. In Network Monitoring, we launched Network Path and Network Configuration
Management to trace changes that cause complex network issues. Within Database Monitoring, Bits
Database Optimizer now automatically simulates and evaluates the impact of AI-generated changes in
order to optimize [ slow ] queries. In Log Management, federating logs enables users to query external
data stores, including Databricks and ClickHouse.

And With Bring Your Own Cloud, or BYOC, customers can now use the full Datadog experience on logs
that are kept within their infrastructure. We've also announced that we're bringing BYOC to metrics
and traces as well. In the digital experience space, Journey Monitoring automatically gives a single
shared view for every critical user flow. And for custom metrics data, we introduced Infinite Cardinality
Metrics, which allow our users to answer arbitrarily complex questions as they generate larger amounts
of data with AI agents without incurring any extra costs.
Finally, we launched a number of innovations to secure the AI stack and defend against a new class of
AI-powered attacks. AI Guard agent discovery finds and maps every known and unknown custom agent
so security teams can see what is protected and what is not. AI Guard for custom agents provides
runtime protections to block attacks that can only be detected with real-time observability data. AI
Guard for coding agents applies the same deep observability to block malicious skills and packages in
code. We also announced Runtime Prioritization Engine to cut vulnerability noise by over 95%.
And finally, we expanded Bits Security Analyst to run on [ non ] Datadog SIEMs so customers can
benefit from the smarts and the learnings of a broad data set regardless of which SIEM they deploy. As
we continue to innovate, we are being rightfully recognized by independent research. We are pleased to
see that for the sixth year in a row, Datadog has been named a leader in the 2026 Gartner Magic
Quadrant for Observability Platforms.
Let's move on to sales and marketing and look at a few of the deals our GTM teams have closed in what
has been a very strong quarter. First, we landed a 6-figure annualized deal with a Fortune 10 company.
This company is expanding its e-commerce business, and they plan to use Datadog Log Management
alongside 10 other Datadog products to improve customer experience and business outcomes.
This win validates our [ expanded ] go-to-market approach to focus on the world's largest companies
and win opportunities in the most complex environments. Next, we landed 7-figure annualized deals
with two neuro labs. These AI labs are rapidly scaling their AI model training workloads and preparing
for major product launches.
By deploying observability using Datadog, they gain visibility across their training infrastructure and
GPU fleets and can iterate faster on their AI models. They are also using Bits AI to rapidly build
monitors, dashboards, and alerts for deep observability context. Next, we landed a 7-figure annualized
deal with a South American bank.
This bank's fragmented legacy monitoring stack and manual triaging caused significant application
downtime that was often called in by customers. By consolidating into Datadog with 11 products, this
customer enables visibility from their mainframe all the way to their microservices and has already
reduced mean time to resolution on live production incidents.
They are adopting Cloud SIEM and Data Security and evaluating other Datadog security products to
improve their security posture. Next, we signed a 7-figure annualized expansion for an 8-figure
annualized deal with a Fortune 100 health insurance company. This customer's biggest pain point is to
deliver great experience to their members throughout their care while protecting PII across dozens of
business units. Datadog's HIPAA compliance and PII handling in RUM, Log Management, and Cloud
SIEM allowed us to differentiate and win over competitive solutions.
And Bits AI investigation is already speeding up incident resolution and reducing expensive escalations.
This customer will expand to 19 Datadog products. Next, we signed a multiyear, over $30 million TCV
deal with one of the world's largest online media companies. This customer chose to standardize on

Datadog across its business, displacing 4 commercial and internal tools. Datadog also proved value
beyond core observability with Product Analytics, CI Visibility, Data Observability, and Cloud Cost
Management. This deal includes our largest win to date for Bring Your Own Cloud, displacing their
legacy commercial logging tool at a petabyte scale.
And finally, we signed a 9-figure renewal with a leading AI company. This longtime, very large
customer uses 17 Datadog products to enable unified visibility on production workloads at a very large
scale, albeit with a user reduction starting in Q3, which we considered in our guidance and which David
will speak to.
Before I turn it over to David for a financial review, let me offer a few words on our longer-term
outlook. There is no change to our overall view that digital transformation and cloud migration are
long-term secular growth drivers for our business. but we now have an additional growth driver with AI
as we help our customers deliver value with this transformative new technology. We are tremendously
excited about our opportunities in AI. To summarize where we are and where we're going. First, AI is a
tailwind for Datadog today as cloud consumption grows and drives more use of our platform.
As of Q2, over 750 AI customers use Datadog to monitor and improve their tech stacks. When we look
at the largest companies driving AI, all 10 of the top 10 AI leaders are Datadog customers. Beyond AI
natives, we see AI activity growing across our broader customer base. We are also seeing signs of rapid
growth in agentic activity with a number of MCP tool calls quadrupling again quarter-over-quarter and
growing more than 22x when compared to Q4 2025.
Second, we are delivering AI for Datadog to deliver more value and greater platform capability to our
customers. This includes our Bits AI products, chat, investigation, detection, code, testing, release, and
many, many others. Third, next-gen AI introduces new complexity and observability challenges. We are
addressing this with what we call Datadog for AI to observe and secure the AI stack from end to end.
This includes GPU Monitoring, Agent Observability, Agent Console, Data Observability, AI Guard, and
many other products.
Finally, our AI research team and our large volume of rich data using critical workflows enable us to
conduct groundbreaking research. We have shown some of our work already with the second version of
our time series model, Toto, in May. Toto version 2 was exciting for 2 reasons. First, we've shown it to
be state-of-the-art on key benchmarks. But more importantly, we've demonstrated for the first time
true scalability for time series models, allowing us to target the same improvement path language
models have followed since 2020.
So now beyond Toto, we are working on larger and more ambitious dedicated models, post-training
models to power Bits AI and bringing other modalities beyond time series data into world models that
we think can lead to a step change in capabilities for our customers.
And we plan to accelerate these research efforts with the acquisitions of Adaptive ML, which will close
in June. Because of all of that, now more than ever, we feel ideally positioned to have customers of
every size and every industry, as well as all types of users, whether humans or AI agents, so they can
transform, innovate, and drive value to AI and cloud adoption.
And with that, I will turn it over to our CFO, David.
David Obstler (Executives)

Thanks, Olivier. Our Q2 revenue was $1.12 billion, up 36% year-over-year. Within that, our 11%
quarter-over-quarter revenue growth is the highest since Q2 2022. And our quarter-over-quarter
revenue added of $115 million is a record by a significant margin. We continue to see robust usage
growth from existing customers as well as a strong ramp in our new customers. Revenue growth
accelerated with our broad base of customers, excluding AI customers to the high 20s year-over-year,
up from the mid-20s percent last quarter and 18% in the year ago quarter. We saw robust growth across
our customer base with broad-based strength across customer size, spending bands and industries.
Meanwhile, our AI customers continue to grow rapidly and diversify in the quarter. This 750 strong
customer group includes a broad range of AI start-ups as it has in the past, but now also includes
hyperscalers using Datadog for in-house AI labs. In Q2, this includes 31 customers spending more than
$1 million annually, of which 8 customers spent more than $10 million annually. We also achieved
strong new logo dollar bookings with particular strength in enterprise, where new logo annualized
bookings more than doubled from a year ago.
And we are seeing new logos ramping faster and contributing more to revenue growth. The portion of
our year-over-year revenue growth that relates to new customers was about 30% in Q2, up from 25% in
Q1. Geographically, we're performing well in all regions with growth acceleration across the regions. We
see particular strength in the Americas as much of the AI activity is occurring in the U.S. as well as in
addition, we are executing strongly in LatAm. Regarding retention metrics, our trailing 12-month net
revenue retention percentage was in the low 120s, similar to last quarter, and churn remains low with
gross revenue retention in the mid- to high 90s. We believe this metric highlights the mission-critical
nature of our platform for our customers.
Now moving on to our financial results. Billings were $1.18 billion, up 38% year-over-year. Remaining
performance obligations, or RPO, was $3.47 billion, up 43% year-over-year. Current RPO grew about
40% year-over-year, and RPO duration increased year-over-year. As we previously mentioned, we
continue to believe revenue is a better indication of our business trends than billing and RPO. Now let's
review some of the key income statement results. Unless otherwise noted, all metrics are non-GAAP.
We have provided a reconciliation of GAAP to non-GAAP financials in our earnings release. Our Q2
gross profit was $892 million for gross margin of 79.6%.
This compares to a gross margin of 80.2% last quarter and 80.9% in the year ago quarter. As we've
discussed in the past, our gross margin varies from quarter-to-quarter with investments into
innovations for our customers, offset by efficiency efforts. There's no change in our expectations for
gross margin, which has been in the 80% plus or minus range historically. Q2 OpEx grew 26% year-
over-year versus 31% last quarter and 36% in the year ago quarter. We held our DASH conference --
user conference in June, and as expected, the event cost about $15 million. Q2 operating income was
$257 million for a 23% operating margin compared to 22% last quarter and 20% in the year ago
quarter. Turning to our balance sheet and cash flow statements.
We ended the quarter with $5 billion in cash, cash equivalents and marketable securities. Cash flow
from operations was $316 million in the quarter. After taking into consideration capital expenditures
and capitalized software, free cash flow was $279 million for a free cash flow margin of 25%. And now
for our outlook for the third quarter and the fiscal year 2026. Our guidance philosophy overall remains
unchanged. As a reminder, we base our guidance on trends observed in recent months and imply

conservatism on these growth trends. Regarding our largest customer, we have seen a usage reduction,
which is incorporated in our Q3 and full year 2026 guidance.
As Olivier noted, this customer has recently renewed with us. For the third quarter, we expect our
revenue to be in the range of $1.135 billion to $1.145 billion, which represents a 28% to 29% year-over-
year growth. Non-GAAP operating income is expected to be in the range of $260 million to $270
million, which implies an operating margin of 23% to 24%. And non-GAAP net income per share is
expected to be in the $0.63 to $0.65 per share range based on approximately 378 million weighted
average diluted shares outstanding.
For the full fiscal year 2026, we expect revenue to be in the range of $4.45 billion to $4.47 billion,
which represents a 30% year-over-year growth. Non-GAAP operating income is expected to be in the
range of $1.01 billion to $1.03 billion, which implies an operating margin of 23%. And non-GAAP net
income per share is expected to be in the range of $2.50 to $2.54 per share based on approximately 376
million average diluted shares outstanding. And for some additional notes on guidance, we expect net
interest and other income for the fiscal year 2026 to be approximately $180 million.
We expect cash taxes in 2026 to be about $30 million to $40 million. We continue to imply a 21% non-
GAAP tax rate for 2026 and going forward. And finally, we expect CapEx and capitalized software
together to be in the 4% to 5% of revenue range in fiscal 2026. Now finally, to summarize, we are
pleased with our execution in Q2. Our investments in R&D and go-to-market are yielding positive
results, and they position us well for continued execution. I want to thank all the Datadogs worldwide
for their efforts.
And with that, we'll open the call for questions. Operator, let's begin the Q&A.
Operator (Operator)
[Operator Instructions] Our first question comes from the line of Sanjit Singh with Morgan Stanley.
Sanjit Singh (Analysts)
On the acceleration in revenue growth again this quarter. David, thank you for giving us the color on
some of the guidance assumptions, particularly headed into Q3 with respect to the largest customer. I
was wondering if you could share any additional details in terms of the new contract? Was it a similar
duration? And in terms of the lower usage, is that a function of the customer getting lower unit price
because of making a new commitment? Or is there some churn downsell that we're seeing through not
only for Q3 but for the balance of the year?
Olivier Pomel (Executives)
Yes. So maybe I'll take this one. I think we -- so overall, we -- as usual, we don't want to comment too
much on any specific customer because we also don't really control what's happening with any specific
customer. We wanted to be transparent about this on the call because we did see a reduction in usage,
and we took the liberty to fully derisk the guidance for the rest of the year with respect to that customer.
And again, the reason for that is we don't control what's happening to a specific customer, but we do
have a great amount of control on what's happening to everything else in the business, and the business
is booming, and we don't want that to overshadow basically the acceleration we see pretty much
everywhere else in the business. So the -- as we mentioned on the call, we renewed the customer. We --
it's a long-time customer using many of our products, but there's not a lot more we can share.

David Obstler (Executives)
Yes. I think just to get specific on the guidance, we last quarter and previous quarters said that we
essentially have a level of commit, and we can derisk our guidance by using that. And then as you know,
in most of our large customers, we have variability relating to the commit, so take that into
consideration.
Olivier Pomel (Executives)
Yes. The last thing I will say because I know so it's on people's minds is if you back out our largest
customer from our growth, you get pretty much the same growth rate as the rest of the business has
been accelerating very steadily. Actually, we've seen, I think, now 5 quarters of continuous acceleration
from the rest of the business, and we feel very good about the -- what we see in the market.
Sanjit Singh (Analysts)
Yes. No, I appreciate the thought. Let's talk about maybe the rest of the business. What we've seen in
the past couple of years sort of AI native sort of leading the charge. It sounds like the enterprises are
getting on board with their AI initiatives. And so just in terms of like the enterprise AI app dev cycle,
what does that look like for Datadog over the last couple of quarters?
Olivier Pomel (Executives)
We do see broad adoption, and we see it in two ways. One is we see it manifest itself in just more
transformation, more cloud adoption, more workloads, more modernization from customers. And
that's what drives the majority of the known AI customer acceleration. So we mentioned also we've seen
continuous acceleration from customers that existed before AI and that are not majority AI businesses.
And that's been pretty remarkable, like the acceleration that we gave the numbers on the call, but the
acceleration since last year has been constant and very significant, and we -- it keeps happening as far
as we can tell. So it's a very positive trend there. That's the first thing we see. The second thing we see is
a very rapid increase in the usage of all of our AI-first surfaces. So that Would be the products that
measure agents and LLMs, we see an explosion of traffic in terms of the LLM and tool calls we're
getting. That would be the amount of calls we're getting to our MCP endpoints. So we see that explode
completely over the past two quarters.
Operator (Operator)
Our next question comes from the line of Raimo Lenschow with Barclays.
Raimo Lenschow (Analysts)
Perfect. Could I stay on that AI theme, please? At the moment, like if you think about the large
customers, there's a lot of model training, et cetera. But if we broaden it out, inference is really
becoming the bigger part. Can you talk a little bit about like how much more observability is needed?
And I'm thinking there, if I do inference, I need to think about vector databases, I need to think
guardrails, all of these agents are going to be in containers that need to be monitored, et cetera. So what
do you see in real life at the moment in terms of if some people do more inference, how much more
observability gets triggered by inference? Is that kind of an opportunity that we should probably pay
more attention than at renewal? And I had one follow-up.

Olivier Pomel (Executives)
There's opportunity at every layer of the stack in inference. So we do think at the end of the day,
inference will be the dominant workload. That's -- any time you train, you probably will want to infer
more than you train as a rule of thumb. We see opportunity at the low level when it comes to the
infrastructure, the GPUs and the consumption you have there. There's opportunities at the very top end
when you measure what the agents are doing and whether you're getting the right outcomes and
whether you're getting the right alignment.
And there's opportunities that every layer in between, just looking at the LLM itself, just looking at the
tool calls and the applications that are being called by the agents, like everything is an opportunity in
there. We see growing adoption from the products we already have there. We mentioned our GPU
monitoring product is actually getting quite a bit of usage in a number of neuro Labs and very AI-first
types of customers. We're also seeing an explosion of volume in our agent monitoring product.
And so we're well positioned there. But we think this market is going to change quite a bit and the
procurations of customers, they also change over time. So for example, last year, our customers were
mostly trying to validate correctness and validate that they were getting some form of outcomes that
they could then scale up. I would say 3 to 6 months ago, the focus has moved quite a bit towards cost.
Now customers were spending a lot on AI and they were wondering what to optimize cost. And I think
we'll see some variations in the concerns over time as customers get further into the adoption and new
products emerge for them.
David Obstler (Executives)
I just want to add that when you look at what we described as some of our deals in the quarter and you
look down our description, you'll see that a number of them have the AI products included. And so that
is indication that those large enterprises are using the platform and buying the AI products as well.
Raimo Lenschow (Analysts)
Okay. Perfect. And then, David, one for you. It's like it's obviously -- you're always in a tough position if
you have to guide and there's these large contracts. How did you do it historically? So did you always
kind of put in the base level and then what happened happens? Or has that approach changed? Or I
don't envy you on having to do this.
David Obstler (Executives)
No, we essentially use -- as we've talked about over the many years, we kind of use the inputs of what
we see. And what we said, I think, in the last quarter or 2 is that we have certain base levels. As you
know, we have a commitment and a usage model. And we've factored that in and providing our
guidance. So our -- as we said in the prepared remarks, our methodology for guidance hasn't changed.
We've always used those inputs and looked at the commitment and usage and doing that.
Olivier Pomel (Executives)
Yes. I mean the only thing I'd say is, in this case, we did chose to fully derisk our largest customer. And
the reason for that is we don't want that to be an overhang on what is otherwise business that is
accelerating and performing extremely well. So we extended that we have the same overall

conservatism as we always do when we look at our numbers. But in this case, we also weighted this one
a little bit differently.
Operator (Operator)
Our next question comes from the line of Gabriela Borges with GS.
Gabriela Borges (Analysts)
I wanted to ask you both about one of our observations at DASH, which is the engineers love the pace of
innovation. They talk very positively about the product. The CFOs love to complain a little bit about
their Datadog bills. So my question for you is talk to us a little bit about how the CFO level
conversations are evolving. Clearly, the ROI is there, but maybe give us a little bit more on where the
budget is coming from. And something like Infinite Cardinality, is that now part of the conversation
with CFOs in solving some of those very particular cardinality cost questions?
Olivier Pomel (Executives)
I mean, look, at a high level, there's only 2 reasons people buy software. It makes them more money or
it saves them money. And anytime we sell, anytime we go out in a renewal, we go out an upsell, or we
land a new customer, that's because we do one of those 2 things for them, and we always have to make
that case. So I wouldn't say that's any different from what we've seen before. The -- what we do for our
customers today, especially as they keep adopting AI, is we help them save a lot of the money they
would spend on building, running operations or running AI agents.
When we have a concern with customers, that's the one thing they kept mentioning is, Hey, how can
you help me rein in my AI costs. This is growing very fast, and I don't have any control on it, and I don't
know whether I'm reaching the right outcomes with that. And so that's one of the reasons we've
invested in all those products we've mentioned earlier. And also we're seeing some of the great returns
on that products already. In terms of Infinite Cardinality, that's -- I would say it's been one of the
longest-standing source of frustration for customers, when sometimes they send more data or they
send more fine-grained tags with their data, and they get some unpredictability on the bills because of
that, because it increases the cardinality of the data we're getting.
And we've solved that from a technical perspective and from a commercial perspective by packaging
our metrics a little bit differently. And we think it's particularly important and relevant as customers
are building more applications with AI and as they want to send basically more tags and more
information and ask more complex questions and get more fine-grained answers to those questions.
And so that fits well within their plans, basically. So we've got great feedback on that so far, but it's still
early. If sometimes we'll get it right, sometimes we'll get it slightly wrong, and when we get it slightly
wrong, we fix it. That's not different from what we've done in the past.
Operator (Operator)
Our next question comes from the line of Mike Cikos with Needham.
Michael Cikos (Analysts)
I wanted to come back to the significant size of the lands that you had this quarter, and it's great to see
the sustained traction, especially with those AI labs. But if I'm thinking about the 2 7-figure AI labs that

you landed this quarter and then going to David's commentary around winning some of these in-house
AI labs with the hyperscalers, are those one and the same here? Or are those 2 separate customers that
were -- customer sets we're talking to?
Olivier Pomel (Executives)
These are different customers. The ones we mentioned on the new lands are neuro Labs. So these are
companies that didn't exist a few years ago. And what's interesting about them on the use case there is
that very often, we land customers when they go into production and they release products and they
start serving their customers. In this case, these are customers we're getting as they are training
models, and they're using us to observe and improve and optimize the training of the models.
And so that's an exciting new area that was not really a business area for us a couple of years ago, and
we've seen a number of new proof points around that. In addition to that, and we've mentioned in
previous calls, we've also landed the AI lab or super intelligence labs of a number of hyperscalers. And I
would say the workloads are similar in that it's largely training of the models, but the customers are a
little bit different. These are very large companies that, in that case, previously had a lot of a lot of
homegrown technology to observe and run workloads.
Michael Cikos (Analysts)
Excellent. And for a follow-up, I know you had cited the new logos ramping more strongly than what
we've seen historically. And correct me if I'm wrong, but I feel like that's a newer phenomenon that you
guys are calling out this quarter. When I think about those new logos ramping, is that a function of pull-
through where maybe some of these AI capabilities are pulling through the broader platform? Or is it
vice versa? Anything you can do to help us think through what is creating that catalyst, if you will, when
the new logos are contributing to the model?
David Obstler (Executives)
It's been happening and building up the number that we have in our Qs, which is the percent from
customers of growth that we didn't have a year ago, -- that number, we said has gone from [ 25 ] to [ 30
]. So this has been building, and we wanted to point that out because of that disclosure, indicating that
the customers that we're landing that it's not only the new logos, but it's also the growth of the new
logos that we've added over the last couple of years -- last year, sorry. So it's a compounding of that.
Operator (Operator)
Our next question comes from the line of Alex Zukin with Wolfe Research, LLC.
Aleksandr Zukin (Analysts)
Oli, maybe first for you, just on the -- a lot of headlines around security over the course of the last few
weeks, particularly AI breaking containment. And it occurs to me that with your positioning in
observability and security increasingly, the notion of a Guardian model and development around that
could meaningfully increase kind of your ambit on what you can do and achieve for clients, both AI
natives and legacy. Can you maybe talk to what -- the increasing opportunity around this crossover in
this AI age and what that means for Datadog? And then I've got a quick follow-up for David.
Olivier Pomel (Executives)

I mean, look, there's a complete switch in the way the security products need to work. So you can't wait
basically for putting humans in the loop. You can't have the typical path when you have 12 or 15
different products that are going to aggregate signal, then you put that signal into a system and to
prioritize them for humans, and humans will review them when they can. Like you need to integrate
everything a lot more. You need to operate a lot closer to the application and to the infrastructure, and
you need to have AI agents solve the issues first. So it's a complete rebuild for most of the industry.
And I think it plays into our approach, which is to have an integrated platform and have all of the
different data streams come directly from observability straight into the security agent and have all that
being integrated from end-to-end. So obviously, this is a field that's moving very fast. We see new
classes of issues pretty much every week at this point. We are quite busy building that up, but we think
it displays into our strength and into where we are basically already are and we're building for our
security products.
Aleksandr Zukin (Analysts)
Perfect. And then, David, maybe just for you. On the largest customer renewal, is there anything you
can tell us around maybe just any changes around the duration or anything that makes this new
contract maybe a little stickier in terms of the discounted rate card, the amount of products that they're
able to kind of use for better value, anything that increases the conviction level around stickiness?
David Obstler (Executives)
I won't comment on this other than to say that most of our enterprise customers, as we talked about for
a long time, have annual plus and then the pricing is generally volume-based pricing. So I would say,
overall, our customers transact with us in that way. And then we have that level of commitment. And
then as we talked about over a lot of years, then there's usage and then we transact. So similar to what
we have with most of our larger enterprise customers. Oli, anything you want to add there?
Olivier Pomel (Executives)
No, I think there's a lot of continuity in that renewal. I think that's what you wanted to put it.
Operator (Operator)
Our next question comes from the line of Eric Heath with KeyBanc Capital Markets.
Unknown Analyst (Analysts)
This is [ Tracy Prachef ] on for Eric Heath. I would love to get more color on your Q3 guide specifically.
It seems like it's a little below your sequential levels of how you've guided your previous Q3s. I would
love to just hear more about what trends you're seeing going into Q3 and maybe what some of the
assumptions of the guide are.
David Obstler (Executives)
Yes. I think it's similar to the methodology. We take what we see and provide some conservatism. And I
think we had mentioned in the script that we've been renewed our largest customer, but we've seen us
declines relative to the previous quarter. We said that. So that's all taken into consideration in trying to
develop a guidance that is consistent with the methodology of conservatism that we've used as a public
company.

Unknown Analyst (Analysts)
Got you. And if I could just ask one more for Oli. I'd love to just get your thoughts on the impact of
diversification of AI model usage in your customers and what you're seeing there?
Olivier Pomel (Executives)
Well, we think it's great. Like there's a lot more options for customers to choose from in general. That
creates --that opens up a lot of doors and opportunities for them. It also creates a lot of complexity, and
we're here to help deal with that complexity. So for us, these are great opportunities. And by the way,
we see -- like we've had that thesis since the early days of AI that we would not just end up with one or
two big AI companies and everybody using them, the same way we didn't just end up with one or two
big cloud companies and everybody just using software from them.
Like the ecosystems are very, very rich. They have -- there are lots of providers. There are very large
providers. There are smaller providers, and everything in between. And there's many compositions of
those different systems that are used by any given customer. And so we think the same is going to
happen in AI. We think also that the multiplication of models, and open source models in particular,
opens the door to customers doing a lot more training on their own. And so that's a new market for us.
We see some signs that we have a very good role to play there. And we're building towards that as well.
So overall, I would say it's very positive for everyone.
Operator (Operator)
Our next question comes from the line of Koji Ikeda with Bank of America.
Koji Ikeda (Analysts)
Just one for me here. I wanted to ask on Bits AI. All the commentary that you guys are saying on Bits AI
and all the work that we've been doing intra-quarter, it sounds like Bits AI is really taking off for you
guys. And so just thinking that Bits AI is going to be increasingly automating activities that historically
has created observability workflows. I'm curious and really wonder how do you ensure that greater
automation that might be driven by Bits AI doesn't eventually reduce the volume of activity that
traditionally drove Datadog consumption?
Olivier Pomel (Executives)
Well, look, if we provide more value, we get more -- as I was saying earlier on the call, like we sell more
software by helping customers make more money or save money or both. And I think if we can
automate more and let them do more, we'll provide more value. That's as simple as that. I think the
future of observability is not just observing, it's fixing. It's not waking up people in the middle of the
night because something book, but fixing it for them.
It's not letting people do damage control on the security incident because an attacker is in. It's
preventing the attacker from getting in to start with by auto mediating issues, and we're very, very busy
building all of that. And we're super confident that this will yield great business outcomes for us in the
end. And that's what we see from customers in the market. Like when they use Bits AI, they use more of
our product. They deploy more of it. They create more dashboards and alerts and everything else. They
have more users inside of our product, like it's not a zero-sum game.

Operator (Operator)
Our next question comes from the line of Samik Chatterjee with JPMorgan.
Samik Chatterjee (Analysts)
Maybe just on the non-AI part and the acceleration that you're seeing related to the non-AI part of the
business. I just wanted to sort of get your thoughts on the sustainability and whether this acceleration
that you're seeing is driven by some of the new customer logos that you're pointing out or more usage
going up? And as CFOs get more sort of cautious around their budgets, do you see more sensitivity
around non-AI eventually relative to some of the AI products and how they're doing at this point? And I
have a quick follow-up.
Olivier Pomel (Executives)
So I mean from what we can tell, it's very broad-based. And it's largely driven by existing customers
because that's the majority. Like when you think of what it takes to move that number, that's basically
the majority of our business, we're not just going to move that with a few newer customers. It's largely
driven by the existing customers. And it's driven by both increases in volume and because they are
moving more and more close to the cloud and adoption of our newer products as they consolidate on to
us. We think it's sustainable.
For one thing, if you compare to what we have seen in the heady days of 2021 or the growth rates are
accelerating, but they're still far below what we were seeing at that time. And so we don't create the
same issue of customers having to digest very large increases multiple years in a row. I think in this
case, we're very well within the range of sustainability. And as has been a theme in this call, remember
like when customers adopt and they consolidate, they have an eye towards the financial side of the
equation, basically, how much money are they going to make or save by doing that at the end. And we
are very good at helping customers understand that and making that case and helping them save money
at the end of the day. So we feel good about that.
David Obstler (Executives)
And I want to just add one thing, and we talked about this last quarter that some of this has to do with
the investments that we're making in our platform and our product, but it also has to do with the
investments that we're making in our go-to-market. We've successfully expanded quota capacity, the
geography of it. And essentially, that's, as we talked about last quarter, providing returns. So that's also
being a growth driver in our non-AI or enterprise type business.
Olivier Pomel (Executives)
That's right. And you see it also in our continuing investment there. So we keep investing in R&D,
obviously, because we're shipping more products that are successfully being adopted and consolidated
into -- by our large number of existing customers but we also are adding to our go-to-market teams.
We're still not at the scale we want to be in terms of getting to all of the customers worldwide in all of
the segments that are relevant to us. So we're investing as we see the returns of those investments.
Samik Chatterjee (Analysts)

Got it. Got it. And for my quick follow-up here, you talked about the FedRAMP High certification last
quarter. Just curious if there's anything to sort of update us on the pipeline and how -- if there's any
momentum on that front on the pipeline yet.
Olivier Pomel (Executives)
Yes. Well, we're investing quite a bit in the buildup of our federal and government sales in general. And
we see pipeline there. These are -- in general, these are not deals that happen overnight, but this is a
very large market, and we see great traction there, and we're investing to take full advantage of it. A lot
of that was a buildup to get to the right level of certification so we can deliver SaaS to various levels of
government. And we've done quite a bit there. There's actually even more we're planning to do there.
And -- but we're happy with the results so far.
Operator (Operator)
Our next question comes from the line of Howard Ma with Guggenheim Securities.
Howard Ma (Analysts)
Great. Congrats on the strong quarter and the full year guidance raise. I have 2 questions. I'll just ask
them together. The first is on Bits AI. I'm curious how adoption and contribution compares to the
previous major feature expansions in the past. And then my other question is the $30 million TCV deal
with the -- I think you guys said it's the largest online -- or sorry, one of the largest online media
companies. I'm assuming this company did mostly DIY before. So if you could share some light on the
decision-making process and if they're using multiple Datadog products and why now? That would be
really helpful. L.
Olivier Pomel (Executives)
Yes. I'm sorry, I missed some part of your second question.
Yuka Broderick (Executives)
It was -- are they taking multiple products, I think, right, Howard?
Howard Ma (Analysts)
Are they -- yes, the nature of the sale.
Olivier Pomel (Executives)
The nature of the sale.
Howard Ma (Analysts)
Why now?
Olivier Pomel (Executives)
Yes, yes. So I mean I would say -- so first on Bits AI. Yes, and one thing that happened is Bits AI used to
be fairly specific. It used to be dedicated to alerts. Like, Bits AI would pick up an alert and would run an
investigation for you. Now the surface of contact is a lot wider with the customer. So Bits AI, you can

access it through chat. You can, of course, still do the investigations, and we've done quite a bit more
there.
You can have Bits AI manage your monitoring and manage your detection for you. You can have it code
for you. You can have it generate managed tests. Like there's all sorts of different use cases that we built
into it that broaden the surface of contact, and we see a lot of adoption across all of those different
areas.
We also are changing the way we package it. So we have a new model with AI credits that we're rolling
out just because the surface of contact is so much wider now than the specific feature. So we -- there's
quite a bit that is going on there. The explosion of activity that I mentioned earlier about other parts of
our other AI surfaces is happening also in Bits AI.
So that's something we're looking forward to. So that's on that. On the second one, on the products that
are being adopted in the sale, look, we typically land with two or more products that the balance we try
to strike there is always to land enough of the platform without slowing down the deals too much.
Because the more you try to do at once, the more stakeholders you get, and the longer it takes.
And so we found that two products in general is a good land, and then we can expand from there. On
the calls, we tend to mention a lot of consolidation deals because they tend to be the larger ones. Like if
you land with 12 products, you're going to be larger than if you land with two in general. That's not the
majority of the deals. The consolidation typically happens later than when we land, but this make for
very interesting examples of what our customers are doing when they're consolidated on us all at once.
Operator (Operator)
Our next question comes from the line of Andrew Sherman with TD Cowen.
Andrew Sherman (Analysts)
Congrats on the core growth acceleration. Oli, CPUs have had a renaissance lately driven by Agentic AI.
It would be great to hear your thoughts on this topic, if it can be an incremental growth driver for your
infrastructure monitoring. Have you seen any evidence of this yet? That's it for me.
Olivier Pomel (Executives)
Look, we do see an acceleration of consumption of our infrastructure products in general. So that's -- at
a high level, we do see that across the customer base. I don't know that if we see specifically the CPUs
that get attached to GPUs in the new build-out. I think a lot of it has more to do with the fact that the AI
agents are largely spending a good amount of their time, like sometimes the majority of their time,
coding tools. And tools are just applications that already existed, and those applications typically run on
CPUs, and so we see quite a bit of that.
Operator (Operator)
Our next question comes from the line of Brad Reback with Stifel.
Brad Reback (Analysts)
Oli, given your commentary around how strong the core is and that your largest customer was not
additive to growth here in 2Q, should we assume that if we ex out the sequential downtick in that
customer that the core guide would have been probably 300 or 400 basis points higher?

Olivier Pomel (Executives)
Well, I can't speculate. But what I will say is, look, the business overall is growing at the same rate. if
you exclude that customer, as I said. And the business has been accelerating overall. So that's why we
feel good, like when we look at whether we're getting the right returns and the right outcomes for our
investments in R&D or investments in go-to-market and when we look at our pipelines and all of the
signs we have about the business, we feel great about the business. It's a good time to be in business.
David Obstler (Executives)
Yes. I think we commented in the remarks that the non-AI has accelerated and the AI, excluding the
largest customer continues. So I think we gave those trends in describing the business.
Olivier Pomel (Executives)
And of course, customers are growing a lot faster than non-AI.
David Obstler (Executives)
And that AI is growing. Yes, exactly.
Operator (Operator)
Our next question comes from the line of Ittai Kidron with Oppenheimer & Co.
Ittai Kidron (Analysts)
Congrats on the great quarter. I wanted to ask about new customer additions. This probably was the
weakest quarter I ever remember for you guys, especially in the quarter where you had DASH, where
historically DASH has been an accelerant of new customer additions. Any color there would be great.
David Obstler (Executives)
Yes. Yes, I think we -- essentially, it's very similar to what we talked about before. Our gross customer
additions continue to be strong and on trend line. and that's the vast majority of our revenues. We have
at the very low end, the border between free and contract, and that has variability, very low effect on
revenues. So if you -- that accounts, as we talked about in many quarters, that accounts for the
variability of the customer count, and it really has to do with something that has very little effect on
revenues.
Olivier Pomel (Executives)
Yes. When you look at the customers above certain thresholds, like whether it's above $1 million, above
$100,000 1000 all of those are trending very well.
Ittai Kidron (Analysts)
Very good. And then as a follow-up, Oli, for you, perhaps, I want to follow up on the questions around
Bits, which sounds super interesting. I guess longer term and as you try to push deeper also into the
security side of things, could this be evolving into a broader AI SOC automation kind of platform? Is
that a reasonable direction to think that this is where it's going to go?
Olivier Pomel (Executives)

Well, there's definitely -- we're taking moves towards that, right? So we -- Initially we built the SIEM
first for that, then we built the agent into the SIEM. So our Bits AI Security Analyst. And now we've
actually separated the agent from our SIEM so customers can use it with other SIEMs. And we do that
because the agent performs just so well, and it's been such a differentiator when we pitch the SIEM that
we think we're limiting our sales market-wise if we just go after customers that want to re-platform
their SIEM, and it can have a much broader appeal as an AI SOC. So we are definitely taking moves
towards that.
Operator (Operator)
Our next question comes from the line of Andrew DeGasperi with BNP Paribas.
Andrew DeGasperi (Analysts)
I just wanted to ask a question on the non-AI natives, specifically in terms of the growth that you saw in
the quarter. I was wondering, did you see rising demand for the AI monitoring tool, particularly with
open source tools being deployed across enterprises?
Olivier Pomel (Executives)
Sorry, I missed the second part of your question.
David Obstler (Executives)
I think you're asking about within that, the AI, what we used to call AI monitoring. LLM, et cetera, the
growth trend there.
Olivier Pomel (Executives)
And look, the volume -- like there used to be very little volume a year ago. It started growing quite a bit
into the second half of last year. And now it's been very rapidly accelerating over the past couple of
quarters. So we've seen an explosion, basically, of the volume we're getting there. And we get more
usage from different kinds of companies, so we definitely see that. We see it also across traditional
companies and some more recent AI natives. So we see a little bit of both. I would say for that category,
it's still super early. Like we expect the products to change quite a bit. We expect the usage, maybe also
the packaging to change over time quite a bit.
Andrew DeGasperi (Analysts)
Got it. Thank you.
Olivier Pomel (Executives)
All right. So I think that was the last question. So I want to thank all of you for attending the call today.
I also want to, again, thank the teams, everyone at Datadog. I think everybody's been doing a fantastic
job, both on the product side and the go-to-market side. I know we have a lot more lined up for the end
of the year on the product side, and I know also we have very large and very happy pipelines to tend to
on the go-to-market side. So I hope to talk to you again in a quarter. Thank you all.
Operator (Operator)

Thank you for your participation in today's conference. This does conclude the program. You may now
disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DDOG_Q1_2026_Earnings_Call_20260507.md
- 2026-05-07｜CEO Olivier Pomel｜guidance：CEO 表示 Q1 營收高於財測區間上緣（原話："year-over-year and above the high end of our guidance range"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 給 Q2 營收財測 10.7 億至 10.8 億美元（年增 29%–31%）（原話："in the range of $1.07 billion to $1.08 billion"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 說 Q2 財測隱含季增 6400 萬至 7400 萬美元、季增 6%–7%（原話："$64 million to $74 million or 6% to 7%"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 給 Q2 non-GAAP 營業利益率財測 21%–22%（原話："an operating margin of 21% to 22%"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 說 DASH 用戶大會 Q2 成本約 1500 萬美元，已計入營業利益財測（原話："$15 million and which we have reflected in our operating"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 給 FY2026 營收財測 43 億至 43.4 億美元（年增 25%–27%）（原話："in the range of $4.3 billion to $4.34 billion"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 給 FY2026 non-GAAP 營業利益率財測 22%–23%（營業利益 9.4 億至 9.8 億美元）（原話："which implies an operating margin of 22% to 23%"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 說明財測方法：以近月趨勢為基礎並打折（原話："apply conservatism on these growth trends"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 說對最大客戶的財測與上季一樣採更高程度的保守（原話："a higher degree of conservatism to our largest customer"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 答分析師：最大客戶與整體的財測方法與上季相同、沒有改（原話："The answer is no. It's the same methodology"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 說 4 月的 ARR 成長延續 Q1 每月加速的趨勢（原話："a continuation of these healthy growth trends in April"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 重申看營收比看 billings 與 RPO 更能反映業務趨勢（口徑）（原話："we continue to believe revenue is a better indicator of"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 報 RPO 34.8 億美元、年增 51%（原話："RPO, was $3.48 billion, up 51% year-over-year"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 說 RPO 天期拉長，因 Q1 多年期合約占比上升（原話："RPO duration increased year-over-year as the mix"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 報 Q1 gross profit 8.07 億美元、毛利率 80.2%（上季 81.4%）（原話："gross profit was $807 million with a gross margin of 80.2%"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 解釋毛利率逐季波動的口徑：創新投入與效率措施互抵（原話："investments into innovations for our customers, offset by"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 報 Q1 OpEx 年增 31%（上季 29%）（原話："Our Q1 OpEx grew 31% year-over-year versus 29% last quarter"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 說 OpEx 成長反映招聘計畫的執行（原話："is an indication of our execution of our hiring plans"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 報 Q1 營業利益率 22%（上季 24%）（原話："22% operating margin compared to 24% last quarter"）
- 2026-05-07｜CFO David Obstler｜capital_allocation：CFO 報 Q1 自由現金流 2.89 億美元、FCF 利潤率 29%（原話："was $289 million and free cash flow margin was 29%"）
- 2026-05-07｜CFO David Obstler｜capital_allocation：CFO 給 FY2026 資本支出加資本化軟體占營收 4%–5%（原話："together to be 4% to 5% of revenue in fiscal 2026"）
- 2026-05-07｜CEO Olivier Pomel｜capital_allocation：CEO 說多數工作負載跑在雲端，成本走 OpEx 不走 CapEx（原話："meaning you'll see all of that in OpEx, not in CapEx"）
- 2026-05-07｜CEO Olivier Pomel｜commitment：CEO 承諾若資本支出模式改變會告知市場（原話："If it changes, we'll tell you"）
- 2026-05-07｜CEO Olivier Pomel｜capital_allocation：CEO 說正在加碼投資，特別是 R&D 與自家訓練的模型規模（原話："We are definitely ramping up our investments, in particular"）
- 2026-05-07｜CFO David Obstler｜capital_allocation：CFO 說 go-to-market 投資與銷售產能擴張正在見效（原話："are paying off and were the right decision"）
- 2026-05-07｜CFO David Obstler｜capital_allocation：CFO 說公部門業務在 FedRAMP 認證之前就先投資業務與通路（原話："we invested ahead of the certifications"）
- 2026-05-07｜CEO Olivier Pomel｜capital_allocation：CEO 把 bring-your-own-cloud 產品列為投資方向之一（原話："area of investment is our bring your own cloud products"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說非 AI 客戶營收成長加速到 20% 中段（上季 23%）（原話："to mid-20s percent year-over-year up from 23% last quarter"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 說 AI 原生客戶成長明顯快於其餘業務（原話："AI native customer growth continues to significantly outpace"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 報 TTM 淨營收留存率低 120%（上季約 120%）（原話："the low 120%, up from about 120% last quarter"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 說新客戶年化 bookings 創歷史新高（原話："New logo annualized bookings set a new all-time record"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 說 Q1 ARR 新增分布廣、不集中（原話："was very broad-based and was not very concentrated"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說扣掉 Q4 簽下、Q1 貢獻營收最多的那位客戶，ARR 新增仍創紀錄（原話："we still had a record quarter in terms of ARR adds"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說 Q1 新簽了幾家目前尚無營收貢獻、預期未來會很大的客戶（原話："customers in Q1 that don't contribute any revenue yet"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說 Q1 與兩家大型科技公司的 AI 研究部門簽下一筆七位數與一筆八位數年化合約（原話："a 7-figure and an 8-figure annualized deals"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說送出 AI 整合資料的客戶約占客戶數 20%、占 ARR 約 80%（原話："they represent about 80% of our ARR"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說 56% 客戶使用 4 個以上產品（一年前 51%）（原話："56% of our customers now use 4 or more products"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說其餘 18 個較早期產品各自有潛力長到超過 1 億美元 ARR（原話："potential to grow to more than $100 million over time"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說 Bits AI SRE agent 的調查次數 12 月到 3 月翻倍以上（原話："have more than doubled from December to March"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說 Bits Assistant 訊息數該期間成長 12 倍（原話："Bits Assistant messages increased by a factor of 12"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 把 AI 列為除數位轉型與雲端遷移之外的新增長期成長動能（原話："we now have an additional secular growth driver with AI"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 答 agent 與人類用量問題：看到 agent 用量大幅成長（原話："we see both a stratospheric increase of agent usage"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說用量由人或 agent 產生對計價模式沒差，因為是用量計價（原話："we don't care whether most of the usage is humans"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 自述與去年說法不同：去年說訓練還不是 Datadog 的市場（原話："workloads and training is not really a market for us yet"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說客戶自家環境部署（cloud prem）目前不是市場最大的部分（原話："Today, it's not the largest part of the market"）
- 2026-05-07｜CEO Olivier Pomel｜commitment：CEO 預告 DASH 大會將發布多項新產品與公告（原話："sharing many new products and future announcements"）
- 2026-05-07｜CEO Olivier Pomel｜commitment：CEO 預告 agent 安全與權限機制的內容將在大會上多談（原話："you should expect to hear more about that at our conference"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 說 Datadog 在規模上勝過所有競爭對手並在搶市占（原話："all of our competitors at scale, and we're taking share"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 描述客戶常見狀況：各部門散落多套工具，來找 Datadog 整併（原話："customers have 4, 6, 7, 15, 25 different things"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 說超大型雲端業者通常有自己全部自建的文化（原話："typically have a culture of building everything themselves"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 說這些超大型雲端業者這季來找 Datadog 取代部分原本自用的東西（原話："like they come to us to replace some of the things"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 舉例：一家財星 500 大銀行把剩餘日誌資料遷入，完全取代原日誌供應商（原話："replacing their legacy log vendor"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 舉例：一家對沖基金以 Datadog 取代整個地端開源監控層（原話："replace their entire on-prem observability layer"）
- 2026-05-07｜CFO David Obstler｜risk：CFO 答地緣與消費景氣提問：目前在消費與電商業務尚未看到影響（原話："any particular effect in the consumer businesses"）
- 2026-05-07｜CEO Olivier Pomel｜risk：CEO 說超大型雲端業者訓練負載的採用還早，不宣稱勝利（原話："So again, it's too early in the product life cycle"）
- 2026-05-07｜CEO Olivier Pomel｜risk：CEO 說擁有異質晶片環境的公司目前仍是極少數（原話："that is still a very small number of companies"）

### DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md
- 2026-02-12｜David Obstler (CFO)｜guidance：毛利率規劃維持在正負 80% 左右，並保留彈性投資平台、資料中心與產品（原話："planning our gross margins plus or minus 80%"）
- 2026-02-12｜David Obstler (CFO)｜commitment：重申長期營業利益率目標 25% 以上，並稱與上一次投資人日所說相同（原話："long-term target of an operating margin at 25% plus"）
- 2026-02-12｜David Obstler (CFO)｜margin：R&D 占營收比重的目標約 30%，並稱有波動（原話："this has been our target around 30%"）
- 2026-02-12｜David Obstler (CFO)｜margin：稱 AI 的使用可能成為 R&D 占比的槓桿之一，未量化（原話："some things about the use of AI that might be levers here"）
- 2026-02-12｜David Obstler (CFO)｜margin：銷售與行銷費用占營收比重，原文下一行接「roughly the mid-20s range」（原話："keep that sales and marketing as a percentage of revenues"）
- 2026-02-12｜David Obstler (CFO)｜margin：G&A 占營收約 5%（原話："Thank you for all the hard work you do there at around 5%"）
- 2026-02-12｜David Obstler (CFO)｜margin：去年 non-GAAP 營業利益率 22%；前一句稱現金流利潤率 27%（原話："So, it's all non-GAAP, and it was 22%"）
- 2026-02-12｜David Obstler (CFO)｜margin：解釋營業利益率有波動：消費型模式的變動快過招聘速度（原話："that changes faster than we can hire people"）
- 2026-02-12｜Unknown Executive｜margin：答覆 $10M 客戶與 $10 萬客戶的獲利結構差異時，改談加權平均後毛利率大致不變（原話："maintain our margins the same at the gross"）
- 2026-02-12｜David Obstler (CFO)｜capital_allocation：淨股數稀釋目標為 2.5% 至 3%（原話："our target in net share dilution, which is 2.5% to 3%"）
- 2026-02-12｜David Obstler (CFO)｜capital_allocation：併購策略強調審慎，過去聚焦補技術能力（前後文提到 Eppo、Metaplane）（原話："a thoughtful and disciplined acquisition strategy"）
- 2026-02-12｜Olivier Pomel (CEO)｜capital_allocation：長期以約 30% 營收投入 R&D，2025 年超過 $10 億、約 4,000 名工程師（原話："we've invested about 30% of revenues into R&D"）
- 2026-02-12｜Sean Walters (CRO)｜capital_allocation：宣布開始試行資安專屬銷售團隊（原話："we decided to start a pilot of security-focused sales teams"）
- 2026-02-12｜Adam Blitzer (COO)｜competition：稱 R&D 支出約為最接近同業的 3 倍（原話："about 3x the R&D spend of our next closest peer"）
- 2026-02-12｜Sean Walters (CRO)｜competition：稱資安市場的競爭對手正在整併（原話："competitors in this space consolidating"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：承認事後排查類需求用 Claude Code 這類工具也能得到不錯結果（逐字稿拼作 Cloud Code）（原話："you can get a pretty good result if you ask Cloud Code"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱預防性、主動式場景無法靠通用 coding agent 完成，因資料不會流經它們（原話："that just doesn't work at all because the data doesn't flow"）
- 2026-02-12｜Michael Whetten｜competition：回應通用 LLM 的程式碼資安能力：稱自家優勢是看得到程式碼在正式環境的部署狀況（原話："we can see how that code is deployed in production"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱 coding agent 會持續存在且做更多，公司定位是補充而非取代（原話："the agents are here to stay and they're going to do more"）
- 2026-02-12｜Alexis Le-Quoc (CTO)｜competition：被問進入門檻時，承認小模型沒有明確的資金門檻，護城河放在資料品質（原話："don't think there's a clear financial barrier of entry"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：回應 OpenTelemetry：稱資料收集從來不是護城河（原話："The collection has never been the moat"）
- 2026-02-12｜Adam Blitzer (COO)｜competition：自我定位為觀測市場中的高價位產品（原話："Datadog is a premium product"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱觀測市場占有率仍只在十幾個百分點中段（原話："our market share is still only in the mid-teens"）
- 2026-02-12｜David Obstler (CFO)｜competition：觀測市場規模 $300 億以上；擴大到資安、軟體交付等後 TAM 稱超過 $1,000 億（原話："a $30 billion-plus market"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：基礎設施監控 ARR 達 $16 億，日誌與 APM 各超過 $10 億（原話："$1.6 billion of ARR in infrastructure monitoring"）
- 2026-02-12｜Tim Knudsen｜product：資安產品 ARR 已超過 $1 億（原話："we've now surpassed $100 million in ARR"）
- 2026-02-12｜Tim Knudsen｜product：百萬美元客戶中 70% 用至少一項資安產品，但資安只占其 Datadog 支出 2%（原話："together is only 2% of their Datadog spend"）
- 2026-02-12｜Yrieix Garnier｜product：Flex Logs 的 ARR 接近 $1 億且快速成長（原話："approaching $100 million ARR and growing very rapidly"）
- 2026-02-12｜Yrieix Garnier｜product：BYOC（自帶雲）已有大型公司在預覽，並預期打開更多機會（原話："engaged with very large companies and previewing BYOC"）
- 2026-02-12｜Yanbing Li (CPO)｜product：Bits AI SRE 一月單月就有超過 2,000 家客戶跑調查（原話："more than 2,000 customers run investigation with Bits AI"）
- 2026-02-12｜Yuka Broderick｜product：Bits AI SRE 公開定價為每 20 次調查 $500（原話："Bits AI SRE $500 per 20 investigations"）
- 2026-02-12｜Yanbing Li (CPO)｜product：MCP server 自推出後用量呈指數式成長（原話："we've seen also exponential adoption and growth"）
- 2026-02-12｜David Obstler (CFO)｜product：LLM Observability 的 span 量一年增加 10 倍（原話："the last year, that has increased 10x"）
- 2026-02-12｜Alexis Le-Quoc (CTO)｜product：訓練時序模型 Toto 2025 年花費約 $75 萬（原話："We spent about $750,000 to train this"）
- 2026-02-12｜David Obstler (CFO)｜product：數位體驗監控（DEM）已大到公司也稱之為第四支柱（原話："we are also calling that a fourth pillar"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：承認對功能旗標與實驗平台的看法改變（過去視為商品化）（原話："we've changed our minds quite a bit on the topic"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：資料可觀測性過去被視為周邊市場，現在升到優先清單前列（原話："We thought also this was an interesting market"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：被問自主營運何時到來，稱無法判斷是一年或三年（原話："hard to tell whether we get there in a year or in 3 years"）
- 2026-02-12｜Unknown Executive｜product：被問自主營運的計價模式時，稱距離談定價還太遠（原話："too far away to be talking about pricing models"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：預期今年會有相當多公司把 AI 寫程式的轉換推進（原話："I would expect quite a bit of that to happen this year"）
- 2026-02-12｜Unknown Executive｜guidance：把財測保守度歸因於用量計價模式（原話："some of the conservatism we put in guidance"）
- 2026-02-12｜Unknown Executive｜commitment：稱對中期走勢很有信心，短期用量則不確定（原話："we're very confident about where we'll be in the midterm"）
- 2026-02-12｜Sean Walters (CRO)｜commitment：銷售團隊剛開完年度啟動會，稱全面投入 AI 銷售並已訓練每位業務（原話："we are going all in on AI"）
- 2026-02-12｜Unknown Executive｜risk：承認短期用量走勢無法確知（原話："how the usage is going to trend in 1 month from now"）
- 2026-02-12｜Unknown Executive｜risk：承認客戶會定期做用量優化，有時是公司主動建議（原話："we do see optimization on a regular basis"）
- 2026-02-12｜Olivier Pomel (CEO)｜risk：稱多數公司仍處於 AI 寫程式轉換的早期（原話："most companies are still early in the transition there"）
- 2026-02-12｜David Obstler (CFO)｜customer：新增客戶貢獻每年 ARR 成長約四分之一（原話："about 1/4 of that ARR growth each"）
- 2026-02-12｜David Obstler (CFO)｜customer：ARR 成長其餘約四分之三來自既有客戶多用產品與交叉銷售（原話："the remaining approximately 3/4 comes from"）
- 2026-02-12｜David Obstler (CFO)｜customer：客戶數超過 32,000，占約 50 萬目標客戶的邏輯數僅 7%（原話："that's a penetration in logos of only 7%"）
- 2026-02-12｜David Obstler (CFO)｜customer：百萬美元客戶今年成長到超過 600 家（原話："our $1 million customers, which this year grew to over 600"）
- 2026-02-12｜David Obstler (CFO)｜customer：首度揭露年花費超過 $1,000 萬的客戶指標；逐字稿數字為「over 60% growth, and that's now 34%」，未給明確客戶數，原文口徑不清（原話："growing quite rapidly, over 60% growth, and that's now 34%"）
- 2026-02-12｜David Obstler (CFO)｜customer：AI 原生客戶去年底占營收約 11%（原話："at the end of last year was about 11% of revenues"）
- 2026-02-12｜Adam Blitzer (COO)｜customer：前 20 大 AI 原生公司中有 14 家用 Datadog，AI 原生客戶群超過 650 家（原話："14 of the top 20 AI native companies are using Datadog"）
- 2026-02-12｜David Obstler (CFO)｜customer：整體毛留存率 97% 以上（企業 98% 以上，中小與中型 96% 以上）（原話："retention percentage. It's 97% plus in the company"）
- 2026-02-12｜David Obstler (CFO)｜customer：只有約一半客戶同時使用三大支柱（原話："only about half of our customers use all three pillars"）
- 2026-02-12｜David Obstler (CFO)｜customer：三大支柱都用的客戶，花費是其他客戶的 15 倍（原話："In fact, they spend 15x more"）
- 2026-02-12｜David Obstler (CFO)｜customer：一半客戶用 4 項以上產品，用 10 項以上的僅 9%（原話："half of our customers have 4-plus products"）
- 2026-02-12｜Sean Walters (CRO)｜customer：Key accounts 業務第二年的目標從開會數轉向營收與成交（原話："goals are shifted much more to revenue and closing deals"）
- 2026-02-12｜Sean Walters (CRO)｜customer：Key accounts 2025 年有比預期快的成交，且正快速擴張（原話："wins that are already expanding very rapidly"）
- 2026-02-12｜Sean Walters (CRO)｜customer：財星 500 大客戶的花費中位數不到 $50 萬（原話："is still modest at less than $0.5 million per customer"）
- 2026-02-12｜Sean Walters (CRO)｜customer：拉美約占營收 5%，成長遠快於整體（原話："they're growing far faster than our overall revenue"）
- 2026-02-12｜Sean Walters (CRO)｜customer：只稱 2025 訂單表現「stellar」，未給金額（原話："shows our bookings by year, including a stellar 2025"）
- 2026-02-12｜Adam Blitzer (COO)｜customer：計價為用量基礎並有量、承諾、多產品、期限等折扣，稱客戶越成長曲線越彎（原話："We have volume-based pricing"）
- 2026-02-12｜Unknown Executive｜customer：解釋客戶 ARR 出現短期下滑：簽更長期承諾換折扣時可能暫時下降（原話："it might drop you temporarily from where you were"）
- 2026-02-12｜Unknown Executive｜customer：承認過去幾年偏重從既有大客戶擴張，較少花力氣從零開發新客戶（原話："bit victims of our own success"）

### DDOG_Canaccord_Genuity_s_46th_Annual_Growth_Conference_20260812.md
- 2026-08-12｜David Obstler｜guidance：CFO 說明財測做法：拿長期觀察到的成長率，再打折留緩衝。（原話："we take that growth rate that we see over a long period"）
- 2026-08-12｜David Obstler｜guidance：CFO 稱過去 beat and raise 的實績是客戶實際支出高於財測扣掉的折數。（原話："spend more than the amount we're discounting"）
- 2026-08-12｜David Obstler｜guidance：CFO 稱公司每天看得到客戶用量，稱之為近乎完整的資訊（作為財測依據）。（原話："So it's almost perfect information."）
- 2026-08-12｜David Obstler｜guidance：CFO 稱每天早上醒來就能按客戶切分看到用量。（原話："I can see the usage when I wake up in the morning"）
- 2026-08-12｜William Kingsley Crane｜margin：分析師在提問中描述公司目前自由現金流在高 20% 區間（分析師口述，非管理層）。（原話："free cash flow in the high 20s"）
- 2026-08-12｜David Obstler｜margin：CFO 稱利潤率沒有變化。（原話："You can see our margins haven't changed, right?"）
- 2026-08-12｜David Obstler｜margin：CFO 把 token 支出描述為資源重新分配，而非利潤率侵蝕。（原話："it's more of a distribution than a margin erosion"）
- 2026-08-12｜David Obstler｜margin：CFO 稱研發投入的配置會更偏向 token，而非人力。（原話："is going to move more towards tokens than it is to humans"）
- 2026-08-12｜David Obstler｜margin：CFO 說明淨留存率的口徑：講的是 120% 出頭（low 120s）。（原話："net retention that we talked about in the 120s, low 120s"）
- 2026-08-12｜David Obstler｜margin：CFO 說明多產品採用數（cross-sell 指標）的口徑：每年擴大定義。（原話："we expand the definition of cross-sell"）
- 2026-08-12｜David Obstler｜commitment：CFO 稱銷售產能會繼續投資。（原話："So that we're going to continue to invest in."）
- 2026-08-12｜David Obstler｜commitment：CFO 稱研發會以高比率持續投入。（原話："invest at a high rate, but it's very likely"）
- 2026-08-12｜David Obstler｜commitment：CFO 說明揭露慣例：不預告某產品會做到 $1 billion。（原話："We don't go like we're going to have $1 billion of this"）
- 2026-08-12｜David Obstler｜commitment：CFO 說明揭露慣例：達到某個量級後才對外公布。（原話："when we get to certain amounts, we tell everybody"）
- 2026-08-12｜David Obstler｜commitment：CFO 劃定安全產品範圍：不做桌面安全。（原話："we're not saying we're going to secure desktops"）
- 2026-08-12｜David Obstler｜capital_allocation：CFO 稱全球銷售配額產能已成功擴張。（原話："successfully ramped quota capacity on a global basis"）
- 2026-08-12｜David Obstler｜capital_allocation：CFO 稱配額產能的擴張幅度與營收大致相當。（原話："it's been roughly in line with revenues"）
- 2026-08-12｜David Obstler｜capital_allocation：CFO 稱市場尚未飽和，銷售仍有拓展空間。（原話："we're not at the point where we saturated the market"）
- 2026-08-12｜David Obstler｜capital_allocation：CFO 提到公司剛完成一筆收購（分析師後續提問稱之為 Adaptive ML 研究實驗室，該名稱為分析師以 I think 帶出）。（原話："We just made an acquisition."）
- 2026-08-12｜David Obstler｜competition：CFO 稱平台整合帶動交叉銷售與搶市占。（原話："That's enabled us to cross-sell and also take market share"）
- 2026-08-12｜David Obstler｜competition：CFO 稱上一季營收環比增加 $115 million。（原話："I think we said sequentially, we grew $115 million of"）
- 2026-08-12｜David Obstler｜competition：CFO 把該季度增量以季度基礎看作超過 $400 million 的業務規模，並拿來與競爭對手比較。（原話："think of that as over $400 million of business"）
- 2026-08-12｜David Obstler｜competition：CFO 稱與競爭對手相比，市占增幅非常大。（原話："the market share gains are very substantial"）
- 2026-08-12｜David Obstler｜competition：CFO 稱大客戶自建與外購並存，但整體淨傾向是買 Datadog。（原話："towards not doing it yourself but buying Datadog"）
- 2026-08-12｜David Obstler｜competition：CFO 稱公司從零成長到超過 $4.5（下一行接 billion）；原文未標明是營收或 ARR。（原話："That's what's produced from 0 Datadog to over $4.5"）
- 2026-08-12｜David Obstler｜competition：CFO 稱在 observability 領域有很大的競爭優勢，不是在通用模型訓練上。（原話："there's just a tremendous competitive advantage"）
- 2026-08-12｜David Obstler｜competition：CFO 稱他人跨界進攻（Snowflake、Palo Alto、Splunk 之類）並未改變競爭態勢。（原話："And it hasn't changed the competitive dynamic"）
- 2026-08-12｜David Obstler｜competition：CFO 稱對這段期間來說，結果是 Datadog 的競爭地位增強而非削弱。（原話："a strengthening of the competitive position of Datadog"）
- 2026-08-12｜David Obstler｜product：CFO 稱目前主要監控生產環境，並開始做更多訓練端的監控。（原話："We're starting to do more in training."）
- 2026-08-12｜David Obstler｜product：CFO 稱 AI 監控（Datadog for AI）領域成長良好。（原話："we've been seeing very good growth in that area"）
- 2026-08-12｜David Obstler｜product：CFO 指出已對外揭露的 AI 指標包括 agent 監控與 MCP 呼叫成長。（原話："the growth of agent monitoring, the growth of MCP calls"）
- 2026-08-12｜David Obstler｜product：CFO 稱這些指標成長率很高，但仍在早期。（原話："these things are growing at a very high rate"）
- 2026-08-12｜David Obstler｜product：CFO 稱 AI 監控的變現方式是產品 GA 時公布定價。（原話："monetizing it through pricing we publish as we put into GA"）
- 2026-08-12｜David Obstler｜product：CFO 稱 AI for Datadog（Bits）有動能，管理層持樂觀態度。（原話："we're seeing traction in that, which we're optimistic"）
- 2026-08-12｜David Obstler｜product：CFO 稱推動需求的是客戶把 LLM 應用放上生產環境。（原話："clients are putting LLM-enabled applications in production"）
- 2026-08-12｜David Obstler｜product：CFO 稱公司投資於 observability 專用的智能。（原話："specialized intelligence that we're investing in"）
- 2026-08-12｜David Obstler｜product：CFO 描述產品方向是往自我修復（self-remediation）走。（原話："something that's going to move towards self-remediation"）
- 2026-08-12｜David Obstler｜product：CFO 承認自我修復尚未達成，仍在路上。（原話："We're not quite there yet, but that's what the vision is"）
- 2026-08-12｜David Obstler｜product：CFO 稱 Bits 的定價正在試驗（與分析師所述的按調查計價轉為按 token 計價有關）。（原話："We play around with pricing"）
- 2026-08-12｜David Obstler｜product：CFO 稱 Bits 新定價早期反應與使用良好。（原話："early signs are a lot of good reception and use"）
- 2026-08-12｜David Obstler｜product：CFO 稱 Bits 從可靠性調查擴展到安全與軟體開發。（原話："we're also investing in security and software creation"）
- 2026-08-12｜David Obstler｜product：CFO 稱安全業務聚焦在雲端工作負載相關領域。（原話："working on the security of modern cloud workloads"）
- 2026-08-12｜David Obstler｜risk：CFO 承認疫後 ZIRP 時期曾有一些過度使用。（原話："was probably some usage that was over usage"）
- 2026-08-12｜David Obstler｜risk：CFO 承認 AI 原生客群可能有波動。（原話："is there going to be volatility there? Yes, there might be"）
- 2026-08-12｜David Obstler｜risk：CFO 稱公司不是按席位計價，模式與工作負載由 agent 或人處理無關。（原話："we're not a seat model"）
- 2026-08-12｜David Obstler｜risk：CFO 稱收費依據是流經平台的工作負載。（原話："monetizing based on the workloads that go through"）
- 2026-08-12｜David Obstler｜customer：CFO 稱客戶端有強勁的平台投資，部分是為了 AI 做準備。（原話："there's a strong investment in platform right now"）
- 2026-08-12｜David Obstler｜customer：CFO 回答非 AI 原生客群時稱，企業客戶的加速已進入 upper 20s。（原話："upper 20s, and that's enterprises and stuff"）
- 2026-08-12｜David Obstler｜customer：CFO 稱 AI 原生客戶名單分散：750 個以上，其中 30 個以上超過 $1 million。（原話："We had over 750 names, over 30 of them having $1 million"）
- 2026-08-12｜David Obstler｜customer：CFO 稱 AI 原生客群佔 ARR 的比重比疫情高峰時小得多。（原話："a much smaller group as a percentage of ARR"）
- 2026-08-12｜David Obstler｜customer：CFO 說明合約結構：採 take-or-pay 合約。（原話："we have take-or-pay contracts"）
- 2026-08-12｜David Obstler｜customer：CFO 說明合約設有基本承諾額，客戶不能低於該額度。（原話："we have a base of commitment, so they can't spend less"）

### DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md
- 2026-09-08｜CEO｜customer：CEO 憑記憶引述上季營收年增 36%，並先說明數字可能有些微出入（引述自一個月前財報，非本場新揭露）。（原話："we accelerated to the, I think, 36% year-over-year growth"）
- 2026-09-08｜CEO｜customer：CEO 說非 AI 客戶群一年前年增約 18%，現在已到 20% 後段（原話 high 20s）；數字為口述、非本場新揭露。（原話："18% year-over-year growth for that part of the business"）
- 2026-09-08｜CEO｜competition：CEO 說可觀測性大概是 AI 轉型後唯一留下的軟體類別。（原話："Observability is probably the only category that remains."）
- 2026-09-08｜CEO｜competition：CEO 引述自家在可觀測性市場的占有率約 13%–14%。（原話："We have about 13%, 14% market share."）
- 2026-09-08｜CEO｜guidance：CEO 說以現有市占與市場成長，光核心業務就有 5 到 10 倍成長空間；無時間框架、非正式財測。（原話："how we can grow 5 or 10x from that"）
- 2026-09-08｜CEO｜product：CEO 說 AI 建置約八九成與雲端建置相同。（原話："80% or 90% of the AI build-out actually looks like"）
- 2026-09-08｜CEO｜product：CEO 說目前成長最快的是「Datadog for AI」（觀察 AI 整條技術堆疊）。（原話："growing the fastest is Datadog for AI"）
- 2026-09-08｜CEO｜product：CEO 說 AI 技術堆疊今天約 7 到 8 成和非 AI 相同（與前面「AI 建置 8–9 成像雲端」是兩個不同口徑的比例）。（原話："like 70%, 80% of the stack is the same"）
- 2026-09-08｜CEO｜product：CEO 說 AI 介面（agent、traces）流量暴增，但那是指出未來方向，目前還不是營收主要驅動。（原話："rather than already today being the driving part"）
- 2026-09-08｜CEO｜product：被問 Bits AI 在財報哪裡看得到，CEO 說目前財報上還看不出來。（原話："you won't really see it yet on the results"）
- 2026-09-08｜CEO｜product：CEO 說 Bits AI 原本是單一調查用 SKU，正在改包成可跨多個介面使用的 AI credits。（原話："now we're packaging it to a set of AI credits instead"）
- 2026-09-08｜CEO｜commitment：CEO 說之後大概會對 Bits AI 改包裝再做說明，未給時間。（原話："we probably will comment on that in the future"）
- 2026-09-08｜CEO｜product：CEO 說整個業界還不確定怎麼替 agent 收費，Datadog 自己是完全用量計價。（原話："doesn't quite know how to charge for agents just yet"）
- 2026-09-08｜CEO｜product：CEO 提到已宣布把資安 agent 與 Cloud SIEM 脫鉤，可用在自家未收進來的資料上。（原話："the decoupling of our security agent from our Cloud SIEM"）
- 2026-09-08｜CEO｜product：CEO 說 AI credits 是疊加在原有資料用量之上另外賣。（原話："buy on top of the rest of the data consumption"）
- 2026-09-08｜CEO｜product：CEO 說 AI credits 目前客戶接受度看起來很好，並補一句還要再觀察，必要時可換包法。（原話："So far, it seems to be very well accepted."）
- 2026-09-08｜CEO｜customer：CEO 說客戶合約中跨產品的用量可互換（fungible），是客戶集中採購的原因之一。（原話："what they use across different parts of Datadog is fungible"）
- 2026-09-08｜CEO｜customer：CEO 說客戶合併成單一供應商，好處是只管一個承諾額度池，不必管理 12 個。（原話："one big pool of commitment and spending with one vendor"）
- 2026-09-08｜CEO｜customer：CEO 說公司進入了約一半的 Fortune 500。（原話："we are in about half of the Fortune 500"）
- 2026-09-08｜CEO｜customer：CEO 說平均年化合約約 40 萬美元；主持分析師當場插話說實際「高一點」，CEO 未再補數字。（原話："annualized contract is $400,000, something like that"）
- 2026-09-08｜CEO｜customer：CEO 說客戶完全滲透時，在可觀測性與資安等花費約占其雲端帳單的 10%–20%。（原話："around 10%, maybe between 10% and 20% of their cloud bill"）
- 2026-09-08｜CEO｜customer：CEO 說預期這個花費占比的某個版本在 AI 世界也會成立；無數字、無時間。（原話："some version of that will remain true in the AI world"）
- 2026-09-08｜CEO｜customer：CEO 解釋分開報 AI 原生客戶的口徑：這些公司實質上整個業務都在做 AI，即使不是新公司。（原話："because they're substantially all about AI"）
- 2026-09-08｜CEO｜customer：CEO 說長期來看可能不再把 AI 原生客戶分開揭露（揭露口徑可能改變，無時間點）。（原話："we probably won't separate them out anymore"）
- 2026-09-08｜CEO｜customer：CEO 說前沿實驗室的使用方式（同時操作數千上萬個 agent）與一般企業不同，有免費推論、誘因極端。（原話："you have free inference and all the incentives"）
- 2026-09-08｜Analyst (Fatima Boolani, Citi)｜customer：主持分析師稱 AI 原生客戶群約 750 家（分析師講的數字，CEO 未確認也未更正）。（原話："So that 750 customers in the AI native cohort."）
- 2026-09-08｜CEO｜risk：被問 AI 原生客戶集中風險，CEO 回顧疫情期間雲端/數位原生客戶曾占公司業務約 40%，之後遭遇收縮。（原話："it was about 40% of our business at peak"）
- 2026-09-08｜CEO｜risk：CEO 說對 AI 原生客戶的曝險比當年對雲端原生客戶小很多。（原話："the exposure we have to these AI is much smaller"）
- 2026-09-08｜CEO｜risk：CEO 說整體看上行空間大於潛在下行。（原話："we see a lot more upside there than potential downside"）
- 2026-09-08｜CEO｜customer：CEO 在談 AI 原生客戶時提到「其他 85% 的業務」在意成本；原話未明確給出 AI 原生占比。（原話："companies in the other 85% of our business"）
- 2026-09-08｜CEO｜competition：CEO 說 OpenTelemetry 降低導入門檻，對公司是順風。（原話："it's actually a tailwind for us"）
- 2026-09-08｜CEO｜customer：CEO 說最近一次財報電話會提到 5、6 件客戶整併案，通常包含把多個開源產品併進 Datadog。（原話："we call it like 5 or 6 customer consolidations"）
- 2026-09-08｜CEO｜margin：被問價格通縮與開源壓力，CEO 說公司一向擅長維持利潤率與交付給客戶的價值。（原話："we've been pretty good at maintaining margins"）
- 2026-09-08｜CEO｜margin：CEO 說產品毛利率相當高，因此有餘裕把約 30% 營收再投入研發。（原話："we can reinvest about 30% of our top line into R&D"）
- 2026-09-08｜CEO｜competition：CEO 說公司結構上的差異化之一是非常精實的銷售模式，能同時兼顧投資與獲利。（原話："very lean, very efficient go-to-market"）
- 2026-09-08｜CEO｜competition：CEO 說第二個差異化是身為 SaaS 廠商，握有可拿來訓練模型的乾淨營運資料。（原話："extremely clean, operationally relevant data"）
- 2026-09-08｜CEO｜product：CEO 說已發布兩個開源時間序列模型 Toto 與 Toto 2.0。（原話："we've released 2 models of Toto and Toto 2.0"）
- 2026-09-08｜CEO｜capital_allocation：CEO 提到數月前宣布收購 Adaptive ML（強化學習調校客製模型），團隊已併入研究團隊。（原話："the acquisition of Adaptive ML"）
- 2026-09-08｜CEO｜commitment：CEO 說之後會在自建模型這個主題上有更多消息；未給時間或規模。（原話："you should expect to hear and see more from us"）
- 2026-09-08｜CEO｜risk：CEO 承認有客戶決定自建可觀測性而流失，其中有些後來又回來。（原話："a number of them have churned off"）
- 2026-09-08｜CEO｜risk：CEO 說自建後流失的客戶只占客戶群很小一部分。（原話："It's a very small fraction of our customer base."）
- 2026-09-08｜CEO｜customer：CEO 說總體毛留存率在 90% 後段，口徑涵蓋從 SMB 到大型企業的整體業務。（原話："gross retention is extremely high. It's in the high 90s"）
- 2026-09-08｜CEO｜customer：CEO 說有數家最大的超大規模雲端業者（原本全自建）回頭找 Datadog，並說幾次財報前已提過。（原話："a number of the largest hyperscalers come to us"）
- 2026-09-08｜CEO｜customer：CEO 轉述這些超大規模業者的說法：AI 建置需要 Datadog 協助。（原話："For our AI build-out, we need your help."）
- 2026-09-08｜CEO｜margin：CEO 說研發投入的總額度大致不變（約營收 30%），但內部組成會改變。（原話："the overall envelope doesn't change all that much"）
- 2026-09-08｜CEO｜margin：CEO 說內部工程師用 agent 讓 token（模型用量）與算力帳單暴增，且還不清楚多少是必要的。（原話："we're seeing our compute bill or token bill explode"）
- 2026-09-08｜CEO｜margin：CEO 說公司也開始在 GPU 上花更多錢（訓練自家模型）。（原話："we also started spending a lot more on GPUs"）
- 2026-09-08｜CEO｜guidance：CEO 說模型訓練規模會擴大，後續在這塊會看到更多支出；純定性，無金額。（原話："you should see more spend there also"）
- 2026-09-08｜CEO｜margin：CEO 說客服工單需要的人力過去隨客戶數成長，現在這條曲線反過來了，人力轉去做主動服務。（原話："Now that curve has gone the other way."）
- 2026-09-08｜CEO｜commitment：被問 AI 生產力是否減少招聘需求，CEO 說工程團隊還在擴編。（原話："we're definitely still scaling the engineering teams"）
- 2026-09-08｜CEO｜commitment：CEO 說如果每一塊研發投入產出變多，公司會做更多研發而非縮減。（原話："we will just do more R&D"）
- 2026-09-08｜CEO｜product：CEO 說公司的限制在內部能做出多少產品，而非客戶需求。（原話："We're more limited internally by what we can produce."）
- 2026-09-08｜CEO｜competition：CEO 說過去三個月資安工具被徹底顛覆，數年前做的資安產品幾乎都過時。（原話："security tooling has been completely upended"）
- 2026-09-08｜CEO｜competition：CEO 說這讓資安領域被抹平，在位者優勢消失；他預期未來幾年逐步展開。（原話："completely flattens the space and negates any advantage"）
- 2026-09-08｜Analyst (Fatima Boolani, Citi)｜product：主持分析師稱資安 SKU 約滲透 1/4 客戶群、約 1 億美元 ARR（分析師數字，CEO 未確認）。（原話："It's a $100 million ARR franchise."）
- 2026-09-08｜CEO｜competition：CEO 說資安產品用戶群很小，Datadog 的差異是讓開發與維運大量使用者每天用。（原話："Security products have a very small user bases."）
- 2026-09-08｜CEO｜competition：CEO 說做不到被業務員硬綁在一起的孤島產品，要靠整合平台。（原話："siloed products that just happen to be bundled together"）
- 2026-09-08｜CEO｜product：CEO 說公司過去講三支柱（指標、追蹤、日誌），現在把數位體驗拆出來當第四支柱。（原話："now we consider that we have 4 pillars"）
- 2026-09-08｜CEO｜product：CEO 說第四支柱（RUM 與 Synthetic Testing）成長快，且隨規模變大成長率還在加速。（原話："accelerating growth over time as it gets bigger"）
- 2026-09-08｜CEO｜commitment：CEO 說新產品的目標是做到 1 億美元以上，並希望有機會跨過 10 億美元。（原話："we have hopes that they can cross the $1 billion mark"）
- 2026-09-08｜CEO｜capital_allocation：CEO 說沒有哪個類別是非買不可，做法是機會主義；過去收購多半是為了買團隊，省下 2、3 年。（原話："there's no category where we think, oh, we need to buy there"）
- 2026-09-08｜CEO｜capital_allocation：CEO 說歷史上收購主要是為買團隊與產品優勢，省下的時間約 2、3 年。（原話："we're going to take a shortcut of maybe 2, 3 years"）
- 2026-09-08｜CEO｜capital_allocation：CEO 說若某公司能帶來差異化通路，也可能為通路而收購。（原話："We might also do the same thing for distribution."）
- 2026-09-08｜CEO｜capital_allocation：CEO 說大型併購合適標的機率很低。（原話："are very, very low for larger deals"）
- 2026-09-08｜CEO｜capital_allocation：CEO 說只要能加速通往目標並整合進統一平台，什麼都可以考慮，包括大型併購。（原話："nothing is out of the question"）
- 2026-09-08｜CEO｜competition：CEO 說這個市場最後會是 Datadog 加上一兩家其他公司。（原話："It's going to be us, maybe 1 or 2 other companies."）

### DDOG_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md
- 2026-09-10｜David Obstler｜guidance：CFO 說明因投資人關注最大客戶波動，公司把財測改成只放進合約承諾額（commitment）。（原話："putting in our guidance only the commitment"）
- 2026-09-10｜David Obstler｜guidance：CFO 補充該客戶在財測裡的下限就是承諾額。（原話："It can't go below the commitment."）
- 2026-09-10｜David Obstler｜customer：CFO 說上季財報已講過，最大客戶續約、續留 Datadog 並延長合約。（原話："that customer renewed with us, staying with Datadog"）
- 2026-09-10｜David Obstler｜customer：CFO 說最大客戶一直在成長，且用量高於合約承諾額（「一直以來的說法」）。（原話："growing rapidly and spending above the commitment"）
- 2026-09-10｜David Obstler｜risk：CFO 承認最大客戶的用量有波動，這是改財測寫法的原因之一。（原話："So we had some volatility."）
- 2026-09-10｜David Obstler｜risk：CFO 說把超大客戶自建可觀測性視為邊緣情況。（原話："we've always said that's a fringe case"）
- 2026-09-10｜David Obstler｜customer：CFO 給出毛留存率口徑：高 90 多趴，大型企業客戶落在高端。（原話："upper 90s with larger enterprise being at the high end"）
- 2026-09-10｜David Obstler｜risk：CFO 直說並非每個客戶都留得住。（原話："we don't retain every customer"）
- 2026-09-10｜David Obstler｜risk：CFO 表示雲端軟體永遠有成長與優化交替，看的是加權平均。（原話："a yin and yang of growth and optimization in cloud software"）
- 2026-09-10｜David Obstler｜risk：CFO 對比 2021-2023 優化期：當時成長約 70%，現在成長良好但不是 70%。（原話："We're growing well, but we're not growing at 70%."）
- 2026-09-10｜David Obstler｜risk：CFO 說當年雲原生客戶占比比現在高很多。（原話："We also had a much higher percentage of these cloud-natives"）
- 2026-09-10｜David Obstler｜customer：CFO 以淨留存率上升為據，稱目前整體處在成長環境。（原話："we're net-net in a growth environment"）
- 2026-09-10｜David Obstler｜risk：CFO 稱公司如今更大、更分散（地理與客戶類型）。（原話："We're much more diversified in all ways"）
- 2026-09-10｜David Obstler｜customer：CFO 說高成長的 AI 原生客戶很重要，但規模遠小於雲原生客戶群。（原話："it's much smaller than that cloud native"）
- 2026-09-10｜David Obstler｜risk：CFO 稱客戶群沒有忘記上一輪優化期，行為更節制。（原話："our customer base has not forgotten what happened"）
- 2026-09-10｜David Obstler｜risk：CFO 列出降低優化風險的工具：合約延長、量價折扣等。（原話："volume pricing, a number of things to ameliorate the risk"）
- 2026-09-10｜David Obstler｜margin：CFO 說把客戶轉到 Infinite Cardinality SKU，對留存和毛利兩邊都有利。（原話："retentive and also margin enhancing for us"）
- 2026-09-10｜David Obstler｜product：CFO 說公司主動把適用客戶轉到 Infinite Cardinality SKU（與 Flex Logs、Frozen Logs、Metrics Without Limits 同屬一組產品創新）。（原話："proactively converting those customers that can benefit"）
- 2026-09-10｜David Obstler｜product：CFO 說明 Federated Logs：不必所有日誌都流入 Datadog。（原話："not all logs have to flow into Datadog"）
- 2026-09-10｜David Obstler｜product：CFO 說 Federated Logs 目前對接的外部儲存是 ClickHouse 和 Databricks。（原話："In this case, it was ClickHouse and Databricks."）
- 2026-09-10｜David Obstler｜product：CFO 說這類開放架構（Federated Logs、Bring Your Own Cloud）可接到原本拿不到的業務。（原話："business that we would not have had otherwise"）
- 2026-09-10｜David Obstler｜customer：CFO 回答日誌外放的取捨：用戶越集中在 Datadog，每客戶平均營收越高（未給數字）。（原話："we get higher average revenue per customer"）
- 2026-09-10｜David Obstler｜margin：CFO 說請客戶少送用不到的日誌進 Datadog，在許多情況下對公司毛利有利。（原話："in many cases, is margin enhancing for us"）
- 2026-09-10｜David Obstler｜product：CFO 說公司近期收購 Adaptive ML（專長強化學習，用在 IT 管理與可觀測性）。（原話："an acquisition of a company called Adaptive ML"）
- 2026-09-10｜David Obstler｜product：CFO 提到公司先前已推出自家時序模型 Toto。（原話："we put out a model a while ago called Toto"）
- 2026-09-10｜David Obstler｜competition：CFO 稱用自有觀測數據訓練的模型，預期會成為競爭優勢。（原話："what we think will be a very strong competitive advantage"）
- 2026-09-10｜David Obstler｜commitment：CFO 說公司正在人力、GPU、推論上加碼投入自有 AI 模型。（原話："both in terms of people, the GPUs, the inferences"）
- 2026-09-10｜David Obstler｜margin：CFO 預期把 GPU/token 成本逐步重新配置到自有模型（需要前期投入）。（原話："a reallocation of the cost of our GPU -- our token costs"）
- 2026-09-10｜David Obstler｜product：CFO 描述 Bits 自動修復願景：目前尚未達成。（原話："when we get there, we're not there yet"）
- 2026-09-10｜David Obstler｜product：CFO 說願景是讓客戶自選哪類問題可由平台自動修復，哪類仍需人工確認。（原話："the platform can auto remediate"）
- 2026-09-10｜David Obstler｜product：CFO 說 agent observability（監控 AI 應用）已有數千客戶使用。（原話："we're seeing thousands of customers use this"）
- 2026-09-10｜David Obstler｜product：CFO 說 agent observability 已開始產生營收（未給金額）。（原話："we're starting to get the revenue streams from it"）
- 2026-09-10｜David Obstler｜product：CFO 以 Bits 與 MCP Server 呼叫量作為 AI 應用活動增加的指標之一。（原話："MCP Server calls and other indications, a lot of activity"）
- 2026-09-10｜David Obstler｜customer：CFO 說 AI 原生客戶有外包給 Datadog（而非自建）的趨勢。（原話："we're seeing a pattern of outsourcing to Datadog"）
- 2026-09-10｜David Obstler｜customer：CFO 說 AI 原生客戶的主要現象是成長加速。（原話："But the main thing we're seeing is accelerated growth."）
- 2026-09-10｜David Obstler｜customer：CFO 說有大型雲端業者等客戶要把 Datadog 用在訓練與後訓練工作負載，公司原本沒預期。（原話："we want to use you for training or post-training workloads"）
- 2026-09-10｜David Obstler｜competition：敘事變化：CFO 說公司原本認為 Datadog 是生產環境（推論）公司，不會有多少訓練需求，後來被大客戶的訓練用途打破此預期。（原話："We're really not going to see a lot of demand on training."）
- 2026-09-10｜David Obstler｜risk：CFO 對訓練用途設下保留：證據還不夠說公司會成為訓練領域的公司。（原話："We don't believe we have the evidence to say"）
- 2026-09-10｜David Obstler｜competition：CFO 稱極少或沒有公司能有機成長出整合式可觀測性平台，多半靠併購拼湊。（原話："have been able to organically grow an integrated platform"）
- 2026-09-10｜David Obstler｜competition：CFO 稱有一家（未點名）公司正在對外談要做同樣的事。（原話："It's easier said than done."）
- 2026-09-10｜David Obstler｜competition：CFO 說能否守住位置取決於自己是否持續創新，並提到「AI for Datadog、Datadog for AI」兩條線。（原話："This is AI for Datadog and Datadog for AI."）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說 R&D 一貫占營收約 30%，金額超過 10 億美元。（原話："consistently invested 30% of its revenues in R&D"）
- 2026-09-10｜David Obstler｜competition：CFO 稱 Datadog 的研發投入超過市場上其他人。（原話："That is out investing everybody else in the market"）
- 2026-09-10｜David Obstler｜commitment：CFO 承諾持續大幅投入研發以維持創新領先。（原話："that's why we're investing significantly"）
- 2026-09-10｜David Obstler｜customer：CFO 引用研究機構說法：雲端應用占比約高 20 多到 30%。（原話："somewhere upper 20s, 30% of applications are in the cloud"）
- 2026-09-10｜David Obstler｜customer：CFO 稱雲端遷移與現代化的急迫性因 AI 上升，並點出非 AI 業務在加速。（原話："we're seeing the non-AI business accelerate"）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說由下而上的銷售需要越來越多由上而下的企業銷售補強。（原話："has to increasingly be complemented by top-down"）
- 2026-09-10｜David Obstler｜capital_allocation：敘事變化：CFO 說公司先前以為銷售週期是離散的、佣金制度也照此設計，現改設重點客戶組，每位業務只負責 1–2 個大帳戶。（原話："Our commission plans were done that way."）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說大型企業客戶的業務員不能一人負責 10 個帳戶。（原話："can't have an enterprise salesperson covering 10 accounts"）
- 2026-09-10｜David Obstler｜customer：CFO 舉財報中提到的產業案例：銀行、保險、汽車、製造、航空。（原話："banking, insurance, automotive, manufacturing, airlines"）
- 2026-09-10｜David Obstler｜product：CFO 說公司開始看到用 coding agents 提高研發速度的實際效率跡象，但仍在早期。（原話："we are starting to see signs of real efficiency"）
- 2026-09-10｜David Obstler｜product：CFO 說公司用 A/B 團隊測試 coding 工具的取用程度對產出的影響。（原話："we have teams that are access to more of the coding tools"）
- 2026-09-10｜David Obstler｜commitment：CFO 說公司過去快速擴編人力，預期仍需繼續增加人力投資。（原話："we believe we'll continue to have to do that"）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說公司在自有模型上大量投入。（原話："we are investing significantly behind our own models"）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說研究實驗室的投入開始在研發預算中占到一定比重。（原話："starting to result in the weight of the R&D budget"）

### 問答異常語氣（迴避／改口／保留）
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Patrick Colville（Scotiabank）確認「對最大客戶更高程度保守」的說法，並問是相對其他客戶還是相對過往財測｜答法：CFO 先答「兩者都是」並稱措辭很明確；CEO 隨後說「不要對特定措辭賦予太多意義」；CFO 再補一句方法沒變
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Karl Keirstead（UBS）問 Q2 財測信心來源，以及一家 Q4 續約、一家剛簽的大型研究實驗室 Q2 的放量情況｜答法：CFO 與 CEO 都以 Q1 ARR 新增創紀錄且分散回答；沒有直接談那兩家實驗室 Q2 的放量幅度；CEO 只說 Q1 有幾家新客戶尚無營收貢獻
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Gabriela Borges（Goldman Sachs）問訓練相對推論的觀測性支出附著率，以及觀測性占推論支出比例是否改變｜答法：CFO 沒給占比或基準數字，改引用 6,500 位客戶、占客戶 20%、占 ARR 80% 的整合附著數據，並說訓練還早
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Fatima Boolani（Citi）問遙測量暴增下如何維持資本密集度與毛利率｜答法：CEO 只談資本支出（雲端跑、走 OpEx）與資料主權投資，沒有回應毛利率的部分
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Sanjit Singh（Morgan Stanley）問 agent 大量使用平台時，計價模式是否會出現新形態｜答法：CEO 說難以預測四五年後，並稱用量計價不在乎用量來自人或 agent；沒有直接回答是否會有新的計價模式
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Mark Murphy（JPMorgan）問異質晶片環境是否帶來順風｜答法：CEO 自述立場改變：去年說訓練還不是市場，現在說開始看到訓練成為市場，並拿超大型雲端業者客戶的超級智慧實驗室當驗證
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Sanjit Singh (Morgan Stanley)：自主營運一年後、三年後長什麼樣？是否需要自己掌握軟體交付管線（build vs buy）？｜答法：Olivier Pomel 稱時程 'hard to tell whether we get there in a year or in 3 years'，未給具體里程碑；build vs buy 只點名功能旗標與資料可觀測性兩個已改變看法的領域，並稱 'a few other areas... I'm not going to tell you about it'
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Fatima Boolani (Citi)：自主營運商業化後，計價模式是否會根本改變（結果導向計價）？｜答法：回答 'too far away to be talking about pricing models'、'It doesn't mean we have a pricing packaging in mind just yet'，未給計價方向，改談用量計價較容易適應
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Fatima Boolani (Citi)：$1,000 萬客戶與 $10 萬客戶的增量獲利／單位經濟是否有實質差異？｜答法：Unknown Executive 只答量折扣與加權平均後毛利率大致不變，未直接拆解大客戶的獲利結構差異
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Andrew Sherman (TD Cowen)：三大支柱使用率 53% 通常缺哪一塊產品？未來幾年會到多少？｜答法：Sean Walters 稱每個客戶情境不同、不強推三支柱，Yuka Broderick 補 'I wouldn't think of it as one particular pillar that's missing'；兩人都沒給未來使用率數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Keith Bachman (BMO)：資安產品組合的邊界在哪、哪些領域不打？｜答法：Tim Knudsen 談既有成熟預算與統一平台優勢、AI 帶來新領域，未指出任何不打的領域
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Ittai Kidron (Oppenheimer)：小模型成本只要 $75 萬，第三方進入門檻多高？AI 對公司業務的風險是什麼？｜答法：Alexis Le-Quoc 談資料與評測集的護城河、並承認沒有明確的資金門檻；Olivier Pomel 補 R&D 投入金額；兩人都沒列出 AI 對業務的具體風險
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Koji Ikeda (BofA)：財星 500 大客戶如何把花費中位數拉高？2025 年 TCV 訂單（分析師稱 $45 億以上）中大客戶與中型客戶各占多少？｜答法：Unknown Executive 談長銷售週期、工具整併與 key accounts，未拆分 TCV 訂單的客群貢獻，也未確認分析師提出的 $45 億數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Eric Heath (KeyBanc)：BYOC 的可服務客群、何時廣泛推出、進入市場策略？｜答法：Yrieix Garnier 稱已在預覽並有付費客戶，客群點名資料在地化與合規產業、超大規模客戶；未給一般上市時程
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Arti Vula (JPMorgan)：目前 AI 產生的程式碼量能否量化、是否已進到正式環境並帶動用量？｜答法：Unknown Executive 只做定性回答（訊號與開源都顯示程式碼變多），稱多數公司仍在早期，未給量化數字；改以 'we should see where we are at the end of the year' 收尾
- DDOG_Canaccord_Genuity_s_46th_Annual_Growth_Conference_20260812.md｜問：分析師問 agent 流量占比上升後，這塊業務可能做到多大、客戶是否在改變。｜答法：CFO 沒給任何規模數字，回答為「Where it's going to wind up, I don't know」，改談 Datadog 不是按席位計價。
- DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問目前業務中有多少來自「觀察 AI 系統」與「用 AI 強化 Datadog」，請他們切分規模與對業務的影響。｜答法：CEO 講品牌框架與哪塊成長較快（Datadog for AI），並給「堆疊 70%–80% 相同」的比例，未給兩塊各占營收多少的數字。
- DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師指出大型資安公司與 ServiceNow 等正切入可觀測性，問 go-to-market 訊息如何改變。｜答法：CEO 回到自家整合平台與使用者規模的差異，未直接回應資安大廠與 ServiceNow 進入可觀測性這件事。
- DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問下一個 10 億美元產品線會是哪一個。｜答法：CEO 只說內部有數個候選，未點名；轉去講第四支柱（數位體驗）成長，再談新產品目標 1 億美元以上、希望跨過 10 億。
- DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問「大於歷來規模」的併購，門檻與參數長什麼樣。｜答法：CEO 說沒有硬性規則、大型交易少見，未給任何規模或條件參數，只說「nothing is out of the question」。
- DDOG_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：分析師問：怎麼知道我們不是快要進入新一輪優化期？公司用什麼預測工具、為何這次不同？｜答法：沒有說明任何預測工具或領先指標，改用與 2021–2023 的結構差異（成長率、雲原生占比、多元化）和淨留存率作答。
- DDOG_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：分析師問：會不會有更多大客戶願意承擔自建（DIY）複雜度來省錢？｜答法：沒有量化大客戶占比或自建趨勢；以毛留存率『高 90 多趴』、最大客戶續約、『邊緣情況』作答，並承認最大客戶用量有波動。
- DDOG_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：分析師問：客戶群是否正從外部前沿模型 API 轉向自建/自營 AI 堆疊？｜答法：只說在『前面提到的用量指標』看到，未說明是哪個指標或數字，並轉去談 Datadog 自己把 token 成本轉向自有模型。

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

**`contradictions[]`**：先列一致判斷，再列矛盾(矛盾點/A側/B側/性質：可調和=程度差異、不可調和=方向相反)；⚖不可調和矛盾必填裁決：選哪邊/依據(非「直覺」)/硬數據點/執行路徑(≥1 if-then＋1反向條件，動作具體如加碼至X%/清倉，禁「再評估」)；Steelman義務：觀望迴避寫「現在就買的最強論證」，進場寫「現在就賣的最強論證」。前份漂移歸因：`drift_watch`20欄按`cause`三選一(`價格變動`/`新證據`/`方法變動`)分組，`prior_field`填涵蓋欄名陣列，漏一欄＝FAIL；門檻或Single Thing與前份不同須歸因「舊→新＋理由」，`rearm_trigger`不得寫「相同」；觀望須點名binding constraint，`rearm_trigger`=該約束的否定，多因素模糊觀望=重寫 [§5]；前次觀望/迴避且報酬>+30%須明寫翻面理由；90天內翻面須引用前次觸發器已發火，引不出填`qc49_inherit_prior=true`+`prior_verdict`+`prior_role` [§4]。

**負向證據強制處置（硬擋）**：`findings_digest[]`每條`direction="-"`的finding必落於`contradictions[]`/`blind_spots[]`/`triggers[]`/`moat.threats[]`/`thesis.R[]`之`evidence_refs`，或寫進`evidence_dismissed[]`(`{"ref":…,"reason":…}`，理由需指出證據本身問題，禁「影響不大」)。`triggers[]`每列`n`/`text`/`type`/`maps_to`/`metric`/`threshold`/`action`/`source_freq`/`date`；type僅八值(假設驗證/風險/Single Thing/估值rearm/加碼/減碼/清倉/複審日期)，H1-H3或R1-R3寫`maps_to`不塞`type`。`kill_metrics[]`陣列，每條`metric`/`bear_threshold`/`window`＋`source`；`rearm_trigger`=估值rearm/進場首倉列；`catalysts[]`type英文六值`product`/`regulatory`/`capacity`/`guidance`/`macro`/`other`(禁中文)。QC-39產業態勢三軸(必填一句)：A競爭惡化/B結構轉好與durability/C其他結構變數(法規/關稅/反壟斷/通路/商模/替代技術/客戶結構)→裁決=競爭惡化中/結構性轉好中/其他結構變動中(指名哪軸)/雙向拉鋸/靜態＋一句sourced依據，禁只報單向 [§6]。重大事件：M&A(>市值5%)/集體訴訟/臨床或FDA讀數/CEO或CFO離職或SEC調查/客戶流失皆🔴，涉核心假設或護城河須入`thesis.R`或`moat.threats` [§5][§6]。

**必答項**：三視角blind_spots各至少一條、不可調和矛盾的⚖裁決、`evidence_dismissed[]`(若有負向finding未落點)、`kill_metrics[]`、`rearm_trigger`。

---

## ⑤決策輸入與行動條件

**`decision_inputs`**（值可`null`，`dd_decision.py`機械路由裁決）七欄：`thesis_irreconcilable`(§4不可調和)｜`valuation_dependent`(re-rate貢獻≥Base IRR 40%)｜`market_wrong_reason_given`(市場錯在哪的具體理由)｜`week26_return_pct`(26週漲幅)｜`momentum_overheated`(RSI 14d>70或4週漂移>+10%)｜`cycle_gates_pass`(反動能五閘全過，循環股)｜`consensus_rev_3m_pct`(FY1/FY2共識近3月上修%)，缺值`null`。覆寫層：`val_denominator_disputed`/`qc49_inherit_prior`+`prior_verdict`+`prior_role`/`held_now`(bool三態不可`"unknown"`代`null`)；`asym_ratio`/`irr_base_pct`/`ev5y_pct`一律`null` [§5]。

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
{"date":"20260516","verdict":"觀望（衛星候選 B，thesis 完整但估值🔴 + 4 週 +45% 漂移 + BB 上軌外 14%，等回測 BB 中軌 $131 或 W52 $139 + Fwd PE 修復至 55-60x 再分批）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Datadog 是 AI inference 經濟學的觀測層核心玩家，AI native cohort 持續高增長","columns":{"2Y 驗證點":"AI native cohort YoY +60%（vs 當前 +90~240%）；OpenAI 客戶分散度提升（top 3 AI 客戶","5Y 驗證點":"AI native ARR > $1B；LLM Observability ARR > $500M（從 Q1 26 估 $250M annualized）","10Y 驗證點":"AI inference 經濟學 TAM 觸 $50B+ 時 DDOG 觀測層市佔 > 25%","具體數字門檻":"AI native cohort YoY +60% 連 4 季（從當前 +90~240% 衰減但維持高位）","信息來源":"Datadog Q1 26 earnings call + Investor Day 揭露","漂移觸發":"連 2 季 TTM AI native YoY"}},{"id":"H2","text":"Non-GAAP OM 從 FY25 22% 擴張至 FY28 26-28%，在 Rev 繼續 22%+ 下達成","columns":{"2Y 驗證點":"FY26 Q4 Non-GAAP OM ≥ 23%；GM ≥ 78%（LLM infra 壓力可控）","5Y 驗證點":"FY27 OM ≥ 25%；FY28 OM ≥ 27%；SBC/Rev 從 22% 壓至 18%","10Y 驗證點":"FY30 OM ≥ 30%；FCF Margin > 30%（vs FY25 27%）","具體數字門檻":"FY26 全年 Non-GAAP OM ≥ 22%（guide 22-23%）","信息來源":"FY26 guidance 法說","漂移觸發":"連 2 季 TTM OM"}},{"id":"H3","text":"市場給予 Datadog AI infra 觀測層的「pure-play premium」，Fwd PE 維持 50-80x range","columns":{"2Y 驗證點":"NTM Fwd PE 5Y 分位 30-70%；vs CRWD 倍數 ratio","5Y 驗證點":"Fwd PE 50-65x（成熟期）；ARR > $7B","10Y 驗證點":"Fwd PE 40-50x（穩定期）","具體數字門檻":"NTM Fwd PE 維持 60-75x range 連 8 季","信息來源":"Macrotrends + Yahoo Finance 倍數歷史","漂移觸發":"NTM Fwd PE > 90x 連 2 季 → R4 觸發（同業溢價極端）；"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"LLM Observability inference cost 結構性壓 GM","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Non-GAAP GM 連續季度；FY26 GM guide","警戒閾值":"連 2 季 GM"}},{"id":"R2","text":"OpenAI / 大型 AI native 自建 monitoring stack 或合約縮減","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"10-K 揭露 single customer concentration；OpenAI 雲端 spend 變化","警戒閾值":"10-K 單一客戶 > 10% = 觸發風險警示；OpenAI 縮減合約或 self-host monitoring 公告 → 護城河 -1 分"}},{"id":"R3","text":"Cisco Splunk + AppDynamics + Galileo 推 unified observability 大規模搶大客戶","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Cisco unified observability launch；DDOG 大客戶流失公告（DBNR","警戒閾值":"Cisco unified launch 後 6 個月內 DDOG DBNR 連 2 季"}},{"id":"R4","text":"SaaS 同業溢價收斂：CRWD/SNOW/ZS 為比較組，市場校準合理倍數","columns":{"對應假設":"H3","時間尺度":"🔥 中期","監測指標":"DDOG/CRWD forward PE ratio（當前 ~1.0x）；SaaS ETF 倍數","警戒閾值":"NTM Fwd PE > 90x 連 2 季 = 極端化 → 觸發 mean revert → -30%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":207.98,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20260924/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
