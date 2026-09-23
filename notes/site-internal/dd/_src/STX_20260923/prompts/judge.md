你是 stock-analyst **v20 判斷 agent**，標的 STX（20260923）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"STX","date":"2026-09-23","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20260923/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20260923/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":3629,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"$M（YoY +48.5%，QoQ +16.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 investors.seagate.com Q4 FY26 press release（表格對照 SEC 8-K 附件 stxq42026pressreleasefinan.htm）"},"note":"共識約 $3.48–3.50B（媒體彙整兩個版本 $3.48B／$3.50B，非單一權威來源）；亦高於公司 Q4 指引上緣 $3.55B（$3.45B ±$0.1B）"},{"id":"f_kpi1_non_gaap_gross_margin","label":"Non-GAAP gross margin","value":52.7,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）"},"note":"未取得共識"},{"id":"f_kpi2_non_gaap_operating_incom","label":"Non-GAAP operating income／margin","value":44.6,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%（營業利益 $1,619M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks（QoQ +710 bps，non-GAAP opex $293M＝營收 8%）"},"note":"未取得共識（僅查到營收與 EPS）"},{"id":"f_kpi3_gaap_operating_income_ma","label":"GAAP operating income／margin","value":43.0,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%（營業利益 $1,559M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release（表格對照 SEC 8-K 附件）"},"note":"未取得共識"},{"id":"f_kpi4_non_gaap_diluted_eps","label":"Non-GAAP diluted EPS","value":5.71,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"$（GAAP $5.58；QoQ +39%，YoY +121%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks"},"note":"共識約 $5.09–5.10（媒體彙整兩個版本）；亦高於公司 Q4 指引上緣 $5.20（$5.00 ±$0.20）"},{"id":"f_kpi5_free_cash_flow","label":"Free cash flow","value":1118,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"$M（FCF margin 約 31%；營運現金流 $1,305M − capex $187M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release（表格對照 SEC 8-K 附件）；FY2026 全年 FCF $3,105M"},"note":"未取得共識"},{"id":"f_kpi7_guidance_q1_fy2027_reven","label":"Guidance — Q1 FY2027 revenue","value":4100,"period":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027（2026 年 9 月季）的指引","unit":"$M（區間 $4,000–4,200M；中點 YoY +56%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027（2026 年 9 月季）的指引","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks"},"note":"未取得 Q1 FY27 共識"},{"id":"f_kpi8_guidance_q1_fy2027_non_g","label":"Guidance — Q1 FY2027 non-GAAP operating margin（營收中點）","value":50,"period":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引","unit":"%（約；non-GAAP opex 約 $300M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引","citation":"CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）"},"note":"未取得 Q1 FY27 共識"},{"id":"f_kpi9_guidance_q1_fy2027_non_g","label":"Guidance — Q1 FY2027 non-GAAP diluted EPS","value":7.3,"period":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引","unit":"$（區間 $7.10–7.50；稅率約 16%、稀釋股數 231M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引","citation":"公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks"},"note":"未取得 Q1 FY27 共識"},{"id":"f_kpi10_guidance_fy2027","label":"Guidance — FY2027 全年營收成長（定性，無數字區間）","value":"> 34","period":"Q4 FY2026 公告（2026-07-28）","unit":"%（管理層僅稱 FY27 營收成長將高於 FY26 的 34%；capex 維持 4–6% 營收目標區間）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q4 FY2026 公告（2026-07-28）","citation":"CEO／CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）"},"note":"未取得"},{"id":"f_kpi11_exabytes_shipped","label":"Exabytes shipped（總出貨）","value":218,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"EB（YoY +34%，QoQ +9.5%；其中資料中心 195 EB，占 89%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）"},"note":"未取得"},{"id":"f_kpi12_revenue_per_exabyte_asp","label":"Revenue per exabyte（ASP 替代指標，自算）","value":16.6,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"$M／EB（營收 $3,629M ÷ 218 EB；QoQ +6.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"自算：IR 新聞稿營收 ÷ 法說逐字稿總出貨 EB；公司未揭露單價（ASP）"},"note":"不適用"},{"id":"f_kpi13_price_per_exabyte_yoy","label":"Price per exabyte（YoY）","value":10,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%（6 月季；9 月季指引隱含約 20% 以上，為 Morgan Stanley 分析師推算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[13]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"Q4 FY26 法說 Q&A（Morgan Stanley 分析師引述公司數字，CFO 答覆確認供需缺口擴大、定價較佳；Koyfin 逐字稿）"},"note":"不適用"},{"id":"f_kpi14_inventory_days","label":"Inventory days（期末庫存天數，自算）","value":82.6,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"天（期末庫存 $1,571M ÷ 單季銷貨成本 $1,731M × 91 天）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[14]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"自算：IR 新聞稿資產負債表與損益表（SEC 8-K 附件 stxq42026pressreleasefinan.htm）；公司未揭露 DIO"},"note":"不適用"},{"id":"f_kpi15_nearline_exabyte_lta_bac","label":"Nearline exabyte 長約（LTA）覆蓋（backlog 替代；公司未揭露數字 backlog／book-to-bill／產能利用率）","value":"vast majority 已配置至 CY2028","period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"定性；HAMR 占 nearline exabyte 出貨run rate 約 40%（6 月）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[15]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"CEO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）；訂單須先簽約定義規格與價格才開始生產，涵蓋整個 CY2027"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-07-28","period":"2026-07-28","unit":"date","basis":"距今 41 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-07-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_stx_gross_margin_pct","label":"STX 毛利率","value":45.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_stx_operating_margin_pct","label":"STX 營業利益率","value":34.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_stx_fcf_margin_pct","label":"STX FCF 利潤率","value":25.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mu_gross_margin_pct","label":"MU 毛利率","value":72.57,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_mu_operating_margin_pct","label":"MU 營業利益率","value":65.67,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_mu_fcf_margin_pct","label":"MU FCF 利潤率","value":28.99,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_000660_ks_gross_margin_pct","label":"000660.KS 毛利率","value":76.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_operating_margin_pct","label":"000660.KS 營業利益率","value":68.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_fcf_margin_pct","label":"000660.KS FCF 利潤率","value":47.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_gross_margin_pct","label":"005930.KS 毛利率","value":57.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_operating_margin_pct","label":"005930.KS 營業利益率","value":36.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_fcf_margin_pct","label":"005930.KS FCF 利潤率","value":28.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi6_sbc_non_gaap","label":"SBC 占 non-GAAP 營業利益","value":3.3,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","unit":"%（SBC $54M；占營收 1.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）","citation":"公司 IR 新聞稿 Q4 FY26 press release non-GAAP 調節表（FY2026 全年 SBC $213M − 前三季 $159M＝Q4 $54M，與新聞稿單季數相符）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":914.72,"period":"2026-09-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":121.52,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":59.16,"period":"2026-09-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（35.78 → 35.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（55.37 → 55.37）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（78.29 → 78.29）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":35.78,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":55.37,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":78.29,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":140.3,"period":"2026-06-23 → 2026-09-19","unit":"%","basis":"FY1 共識 EPS 14.89 → 35.78（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":65.9,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":17.07,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":17.25,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":24.52,"period":"2026-09-19","unit":"x","basis":"分母＝FY1 EPS 35.78，分子＝快照價 877.33","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-19"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-09-23","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 914.27 / W52 561.16 / W104 338.19 / W250 182.94 / W250 13週斜率 7.26%"},{"id":"f_ma_w52","label":"52 週均線","value":561.16,"period":"2026-09-23","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":338.19,"period":"2026-09-23","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":182.94,"period":"2026-09-23","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":7.26,"period":"2026-09-23","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Tom Coughlin 估 2025 全年 HDD 三家出貨份額：以台數計 WDC 42.3%、STX 40.8%、Toshiba 17%；以容量（EB）計 WDC 約 47%、STX 約 42%、Toshiba 約 11%。","source":"Forbes (Tom Coughlin), 'C4Q 2025 And 2025 Hard Disk Drive Industry Update' https://www.forbes.com/sites/tomcoughlin/2026/02/02/c4q-2025-and-2025-hard-disk-drive-industry-update/ （數字取自搜尋摘要，WebFetch 未能讀全文）","as_of":"2026-02-02","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026 年第二季全球 HDD 出貨 504.3EB，季增 5.6%；估計營收 85 億美元，季增 14.9%；上半年 HDD 產業營收逾 150 億美元，全年有機會超過 300 億美元。","source":"Forbes (Tom Coughlin), 'HDD Industry Revenue Could Top $30B In 2026' https://www.forbes.com/sites/tomcoughlin/2026/08/09/hdd-industry-revenue-could-top-30b-in-2026/ （數字取自搜尋摘要，WebFetch 遇 403）","as_of":"2026-08-09","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"STX 10-Q（期間結束 2026-04-03）披露 nearline 容量出貨由 497EB 增至 695EB，成長 39.8%。此為 STX 自身絕對出貨量，非份額數字。","source":"SEC EDGAR, Seagate Form 10-Q https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000088/stx-20260403.htm （數字取自搜尋摘要；as_of 取財報期間結束日，實際比較期間未核）","as_of":"2026-04-03","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Blocks & Files 報導 Toshiba 推出 11 碟 34TB SMR 硬碟（僅據文章標題「Toshiba goes glassy-eyed with 11-platter 34TB SMR drive」，內文未讀）。","source":"Blocks & Files https://www.blocksandfiles.com/disk/2026/03/31/toshiba-goes-glassy-eyed-with-11-platter-34tb-smr-drive/5213568","as_of":"2026-03-31","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Seagate FY2026 10-K (fiscal year ended 2026-07-03) states that one customer accounted for about 14% of consolidated revenue; the excerpt retrieved does not name the customer and does not list other customers above 10%.","source":"Seagate FY2026 Form 10-K (SEC accepted 2026-08-04), via StockTitan: https://www.stocktitan.net/sec-filings/STX/10-k-seagate-technology-holdings-plc-files-annual-report-6e534d62e382.html","as_of":"2026-08-04","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"Forbes (Tom Coughlin) headline reports Seagate qualified its 40TB-class HAMR (Mozaic) HDDs at two leading data center companies and ships them to those customers; this is a qualification/ramp fact, not a second-source or in-house disclosure.","source":"Forbes, Tom Coughlin, 'Seagate Ships Highest Capacity Hard Drives To Leading Data Center Companies': https://www.forbes.com/sites/tomcoughlin/2026/03/03/seagate-qualifies-40tb-hamr-hdds-at-two-leading-data-center-companies/","as_of":"2026-03-03","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 10-K (fiscal year ended 2026-07-03): one customer accounted for approximately 14% of Seagate's consolidated revenue. Two secondary sources (Stock Titan 10-K summary and GuruFocus SWOT) give the same figure.","source":"Stock Titan, 'Seagate outlines data storage strategy and risks | STX Annual Report (10-K)' https://www.stocktitan.net/sec-filings/STX/10-k-seagate-technology-holdings-plc-files-annual-report-6e534d62e382.html ; GuruFocus, 'STX SWOT Analysis: Financial Strength and Market Challenges Revealed in 10-K Filing' https://www.gurufocus.com/news/9004434/stx-swot-analysis-financial-strength-and-market-challenges-revealed-in-10k-filing","as_of":"2026-08-04","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Trefis reports Seagate management said nearline capacity is almost fully allocated through calendar 2027 (headline: 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand'), following the Q3 FY2026 earnings call of 2026-04-28.","source":"Trefis, 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand' https://www.trefis.com/stock/stx/articles/597921/seagate-is-sold-out-through-2027-as-ai-reshapes-hard-drive-demand/2026-04-30","as_of":"2026-04-30","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"The Register 標題稱硬碟（HDD）2026 年已售罄，並把原因歸給 AI 需求（僅據標題；內文未取得）。","source":"The Register, 'AI blamed again as hard drives are sold out for this year', https://www.theregister.com/on-prem/2026/02/20/ai-blamed-again-as-hard-drives-are-sold-out-for-this-year/4285453","as_of":"2026-02-20","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"24/7 Wall St. 標題稱 Seagate 與 Western Digital 的 AI 儲存需求『已反映在定價權上』（僅據標題；內文未取得）。","source":"24/7 Wall St., 'Seagate and Western Digital: AI Storage Demand Is Now Showing Up in Pricing Power', https://247wallst.com/investing/2026/05/16/seagate-and-western-digital-ai-storage-demand-is-now-showing-up-in-pricing-power/","as_of":"2026-05-16","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Morgan Stanley 研究被轉載為：預期 HDD 出現『更嚴重的缺貨』，至少持續到 2028 年，供應商報價將明顯高於現況，並大幅調升儲存類公司目標價。","source":"P Equity Research (X 貼文) 轉述 Morgan Stanley 研究, https://x.com/pequityresearch/status/2068189826310930478；同文另見 Futu News, https://news.futunn.com/en/post/74636545/morgan-stanley-research-forecasts-a-more-severe-shortage-of-hard","as_of":"2026-06-20","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Forbes（Tom Coughlin）標題主張：儲存與記憶體的價格飆升支撐 AI 需求，但『可能是暫時的』（僅據標題；內文未取得）。屬週期性論點，與『結構性缺貨』說法相反。","source":"Forbes, Tom Coughlin, 'Storage And Memory Price Surges Supporting AI Demand Likely Temporary', https://www.forbes.com/sites/tomcoughlin/2025/10/10/storage-and-memory-price-surges-supporting-ai-demand-likely-temporary/","as_of":"2025-10-10","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"2026-01-08 美國第九巡迴上訴法院撤銷地方法院判決並發回重審，讓 Seagate 對日本 NHK Spring 的懸吊組件（suspension assemblies，硬碟零件）價格壟斷民事求償得以繼續。NHK 已就此向美國最高法院申請調卷（cert）。Seagate 在此案是原告（求償方），不是被調查方。","source":"US Court of Appeals for the Ninth Circuit, No. 24-4470, opinion filed 2026-01-08 (https://cdn.ca9.uscourts.gov/datastore/opinions/2026/01/08/24-4470.pdf); Reuters via TradingView 'US appeals court revives Seagate antitrust claims against Japan's NHK Spring'; Law360 'NHK Says Seagate Antitrust Revival Cries Out For Justices'","as_of":"2026-01-08","affects":["triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2023-04-18 Seagate 與美國商務部工業安全局（BIS）達成和解：因 2020 年 8 月至 2021 年 9 月向被列入實體清單的華為出貨逾 740 萬顆硬碟，被處 3 億美元民事罰款；另有暫緩執行的拒絕出口令，在令發出滿五年且付款與稽核義務履行後豁免。","source":"CNBC 'Seagate hit with $300 million penalty for continuing $1 billion relationship with blacklisted firm Huawei' (2023-04-20); Paul, Weiss 'BIS Imposes $300 Million Penalty Against Seagate for Export Control Violations'; BIS order e2836.pdf","as_of":"2023-04-20","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2026 10-K（會計年度止於 2026-07-03，簽署日 2026-08-04）前瞻聲明仍提到「按時支付與 BIS 和解協議的每季款項」的預期；風險因素寫明部分產品與服務受出口管制法規約束，法規變動或違反可能對業務、營運結果、財務狀況與現金流造成重大不利影響；製造據點含中國、馬來西亞、北愛爾蘭、新加坡、泰國與美國。10-K 法律程序段擷取內容僅見智慧財產權與環境事項，未見對 Seagate 的反壟斷或競爭主管機關調查。","source":"Seagate Technology Holdings plc Form 10-K FY2026 (https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm)","as_of":"2026-08-04","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Seagate FY2026 10-K risk factors state that changes in U.S. trade policy, including the imposition of sanctions or tariffs and the resulting consequences, may have a material and adverse impact on its business and results of operations; the 10-K also lists the impact of trade policy (including tariffs) and FX on the cost of producing its products and the effective price to customers as a factor.","source":"Seagate Technology Holdings plc Form 10-K, fiscal year ended 2026-07-03, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","as_of":"2026-07-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Seagate FY2026 10-K states that component manufacturing, subassembly and final test and assembly are performed at facilities in China, Malaysia, Northern Ireland, Singapore, Thailand and the United States.","source":"Seagate Technology Holdings plc Form 10-K, fiscal year ended 2026-07-03, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","as_of":"2026-07-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Seagate FY2026 10-K states that some of its products and services are subject to export control laws, that changes to or violation of these laws could have a material and adverse effect on the business, and that if it were prohibited from selling to key customers for any reason, such as export regulations, revenues and results could be materially and adversely affected.","source":"Seagate Technology Holdings plc Form 10-K, fiscal year ended 2026-07-03, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","as_of":"2026-07-03","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"In April 2023 the U.S. Commerce Department's BIS imposed a $300 million civil penalty on Seagate Technology LLC and Seagate Singapore for selling over 7.4 million HDDs to Huawei (added to the Entity List in May 2019) in violation of the Foreign Direct Product Rule; BIS also imposed a multi-year audit requirement and a five-year suspended Denial Order. This is the largest standalone administrative penalty in BIS history.","source":"CNBC, 'Seagate hit with $300 million penalty for continuing $1 billion relationship with blacklisted firm Huawei, despite U.S. export controls', https://www.cnbc.com/2023/04/20/seagate-to-pay-300-million-penalty-over-billion-dollar-deal-with-huawei.html ; Orrick, 'Seagate Export Control Penalty Shows New, Aggressive China-Trade Enforcement'; Arnold & Porter Enforcement Edge blog (2023-04)","as_of":"2023-04-20","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"The Section 232 proclamation imposing a 25% U.S. tariff on certain semiconductors took effect 2026-01-15; per search-result descriptions it covers a narrow range of advanced computing chips (above TPP and DRAM-bandwidth thresholds, e.g. NVIDIA H200, AMD MI325X) and their derivative assemblies. The search results did not show hard disk drives as covered.","source":"EY Global Tax News, 'US Section 232 proclamation imposes 25% tariff on certain semiconductors', https://globaltaxnews.ey.com/news/2026-0209-us-section-232-proclamation-imposes-25-percent-tariff-on-certain-semiconductors ; C.H. Robinson client advisory 2026-01-15, 'Guidance on Section 232 Semiconductor Import Duties for 2026'","as_of":"2026-02-09","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#5","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"A Yahoo Finance article on Western Digital (HDD peer) states that the proposed tariffs focus on a wider set of chip-related products, including hardware used in data center servers and storage, and that this could influence WDC's component and system costs and where it sources and assembles drives for hyperscale and AI customers. The article is about WDC, not STX, and does not name Section 232 or Seagate.","source":"Yahoo Finance, 'How Exposed Is Western Digital (WDC) To New Semiconductor Tariffs?', https://finance.yahoo.com/technology/articles/exposed-western-digital-wdc-semiconductor-021558493.html","as_of":"2026-08-30","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#6","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Bloomberg reported that the U.S. and China are discussing tariff concessions to extend their trade truce; search-result text says both sides are eyeing tariff cuts on goods including American energy and agricultural products ahead of the leaders' summit.","source":"Bloomberg newsletter, 'China, US Discuss Tariff Concessions to Extend Trade Truce', https://www.bloomberg.com/news/newsletters/2026-09-16/us-and-china-trade-truce-and-tariffs","as_of":"2026-09-16","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#7","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Fortune headline reports that Trump is readying a new tariff to punish China for its flood of cheap exports, structured so as not to endanger the trade truce or the summit with Xi Jinping (only the headline/summary was read; details not fetched).","source":"Fortune, 'Trump readies a new tariff to punish China for its flood of cheap exports—without endangering his trade truce or his summit with Xi Jinping', https://fortune.com/2026/08/24/trump-new-tariff-china-cheap-exports-trade-war-truce-summit-xi-jinping/","as_of":"2026-08-24","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Seagate 10-K (FY ended 2026-07-03) states: 'Component manufacturing, subassembly and final test and assembly operations are performed at facilities in China, Malaysia, Northern Ireland, Singapore, Thailand and the United States.' The excerpt read gives no per-site percentage split.","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","as_of":"2026-07-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Seagate 10-K risk-factor language: 'Shortages or delays in the receipt of, or cost increases in, critical components, equipment or raw materials necessary to manufacture our products, as well as reliance on single-source suppliers, have in the past and may in the future affect our production.' Also: 'Certain components and raw materials are available from a limited number of suppliers.'","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","as_of":"2026-07-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Seagate 10-K states production requires 'commodities and specialty materials, including certain rare earth elements, precious metals and specialized alloys, which may be subject to supply constraints or price volatility.'","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","as_of":"2026-07-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Seagate 10-K states: 'Changes in U.S. trade policy, including the imposition of sanctions or tariffs and the resulting consequences, may have a material and adverse impact on our business and results of operations.' It also says some products are subject to export control laws. The excerpt read has no explicit Taiwan-specific or Middle East/Iran language.","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","as_of":"2026-07-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Third-party supply-chain mapping (Gillware, estimate) says Seagate's Springtown, Northern Ireland wafer fab is long reported to produce on the order of one third of all HDD read/write heads globally. It names TDK (Japan) as the merchant head supplier.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","as_of":"2026-07-06","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#5","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Third-party mapping (Gillware, estimate) says Japan's Nidec makes on the order of 80% of the world's HDD spindle motors. MinebeaMitsumi is a second source with Thailand manufacturing.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","as_of":"2026-07-06","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#6","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Third-party mapping (Gillware) says China accounted for roughly 60% of world mined rare-earth supply and around 90% of refining of magnet-grade material used in HDD magnets. Japan produces the finished magnets.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","as_of":"2026-07-06","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#7","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Third-party mapping (Gillware) says HDD controller silicon is designed by Broadcom and Marvell and manufactured by TSMC (Taiwan), with OSAT assembly in Taiwan and elsewhere in Asia. This is an industry-level map; it does not name Seagate's own controller vendors.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","as_of":"2026-07-06","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#8","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Third-party mapping (Gillware) says HDD final assembly is centered in a Thailand cluster (primary), with Malaysia and China also involved. It says the 2011 Thailand floods eliminated up to half of global HDD manufacturing capacity within weeks and roughly doubled drive prices.","source":"Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/","as_of":"2026-07-06","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center／nearline] FQ4 FY2026（截至 2026-07-03）總營收 $3.629B，YoY +48%；FY2026 營收 $12.2B，YoY +34%（FY2025 為 $9.097B）；FQ1 FY2027 指引營收 $4.1B ±$0.1B、non-GAAP EPS $7.30 ±$0.20。","source":"Seagate IR press release「Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2026 Financial Results」https://investors.seagate.com/news/news-details/2026/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2026-Financial-Results/default.aspx","as_of":"2026-07-28","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center] FQ4 FY2026 Data Center 營收 $2.9B，YoY +57%，占總營收 81%（去年同期 76%）；nearline 出貨 195 EB，YoY +43%，占出貨容量 89.4%；總出貨 218 EB，YoY +34%。","source":"Blocks & Files「Seagate HAMRing customers - generating more and more $/TB」https://www.blocksandfiles.com/disk/2026/07/30/seagate-hamring-customers-generating-more-and-more-/tb/5281058","as_of":"2026-07-30","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center／價格] 報導稱上季每 TB 均價 YoY +10%；分析師在電話會議上談到 9 月季指引的價格成長「closer to maybe 20 percent year-over-year or even above」。Seagate FQ4 non-GAAP 毛利率 52.7%（紀錄新高）。","source":"Blocks & Files 2026-07-30（同上）；毛利率取自 Investing.com「Earnings call transcript: Seagate beats Q4 2026 forecasts」https://www.investing.com/news/transcripts/earnings-call-transcript-seagate-beats-q4-2026-forecasts-as-shares-rebound-after-hours-93CH-4818284","as_of":"2026-07-30","affects":["thesis.H","valuation","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center／需求能見度] 管理層稱大部分 nearline 出貨 EB 已配置到 2028 曆年，且不少客戶正尋求把規劃期延長到 2029 年以後；FQ4 結束時 HAMR 產品約占 nearline EB 出貨 run rate 的 40%；長期 EB 成長目標為 mid-20%。","source":"Investing.com「Earnings call transcript: Seagate beats Q4 2026 forecasts as shares rebound after hours」https://www.investing.com/news/transcripts/earnings-call-transcript-seagate-beats-q4-2026-forecasts-as-shares-rebound-after-hours-93CH-4818284；配置到 2028／2029 引述另見 Blocks & Files 2026-07-30","as_of":"2026-07-28","affects":["thesis.H","moat_trend","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"[Edge IoT／legacy] FQ4 FY2026 Edge IoT 營收 $697M，YoY +20%、QoQ +14%，占總營收 19%；同季非 nearline 出貨 23 EB，YoY -10%。","source":"Blocks & Files 2026-07-30（Edge IoT $697M／+20%／19%、非 nearline 23 EB／-10%）；QoQ +14% 取自 Yahoo Finance「Can Seagate Extend the Growth Momentum in Its Edge IoT Business?」https://finance.yahoo.com/markets/stocks/articles/seagate-extend-growth-momentum-edge-131300564.html","as_of":"2026-07-30","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"[Data Center／產業供需] 搜尋摘要引述 X 帳號 pequityresearch 一則標題為「Morgan Stanley research forecasts a 'more severe ...'」的貼文，內容稱：2026 年 nearline HDD 供給缺口約 300 EB（10%–15%），2027、2028 年擴大到約 400 EB；未來 2–3 年 nearline EB 供給受限，CAGR 約 30%–35%，需求成長 40%–50%。","source":"X post by pequityresearch（轉述 Morgan Stanley 研究）https://x.com/pequityresearch/status/2068189826310930478","as_of":"2026-06-20","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"TrendForce 稱 AI 推論需求使 nearline HDD 交期由數週拉長到 52 週以上；高容量 QLC SSD 出貨 2026 年『可能爆發式成長』；與 nearline HDD 相比，QLC SSD 效能較高、功耗約低 30%。該文未給 QLC 出貨量或每 TB 成本的數字。","source":"TrendForce Press Center, 'Soaring Inference AI Demand Triggers Severe Nearline HDD Shortages; QLC SSD Shipments Poised for Breakout in 2026' https://www.trendforce.com/presscenter/news/20250915-12714.html","as_of":"2025-09-15","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"TrendForce 報導標題指 Seagate 財測優於預期，且 nearline HDD 產能到 2026 年已全數被訂走（fully booked through 2026）。內文細節未逐字核對。","source":"TrendForce News, '[News] Seagate Q3 Guidance Tops Estimates, Nearline HDD Capacity Fully Booked Through 2026' https://www.trendforce.com/news/2026/01/28/news-seagate-q3-guidance-tops-estimates-nearline-hdd-capacity-fully-booked-through-2026/","as_of":"2026-01-28","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Seagate Mozaic 4+ HAMR 平台已通過兩家頂級超大規模雲端業者資格認證並進入量產，支援單碟／整機容量最高 44TB，並提到未來朝單碟 10TB、整機 100TB 擴展。","source":"Yahoo Finance, 'Seagate (STX) Expands HAMR With Hyperscalers: Is Mozaic 4+ the Margin Story Investors Missed?' https://finance.yahoo.com/news/seagate-stx-expands-hamr-hyperscalers-043020641.html","as_of":"2026-03-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"同一篇文章列出的風險：若需求或價格轉弱，Seagate 的負債與資本密集度是否可控；並提到謹慎的分析師擔心能源效率需求上升，可能限縮 Mozaic 4+ 的上行空間。文章未量化 SSD 替代幅度，也未寫 WD 的 HAMR 時程。","source":"Yahoo Finance, 'Seagate (STX) Expands HAMR With Hyperscalers: Is Mozaic 4+ the Margin Story Investors Missed?' https://finance.yahoo.com/news/seagate-stx-expands-hamr-hyperscalers-043020641.html","as_of":"2026-03-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Western Digital 公布路線：40TB UltraSMR（ePMR 為基礎）預計 2026 下半年推出，已在兩家超大規模客戶認證中；HAMR 預計 2027 完成客戶認證並量產；目標 2029 年推出 100TB HAMR。另據報導 WD 計畫將 ePMR 延伸到 60TB 級。這是 HDD 同業路線，非 SSD 替代，但顯示 HAMR 第二供應商預計 2027 進場。","source":"Western Digital press release 'Western Digital Accelerates Storage Innovation for AI Era' https://www.westerndigital.com/company/newsroom/press-releases/2026/2026-02-03-western-digital-accelerates-storage-innovation-for-ai-era（細節同見 Tom's Hardware / Guru3D 報導）","as_of":"2026-02-03","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#5","axis":"substitute_technology","section":"coverage","direction":"+","claim":"搜尋到 Seagate FY2026 10-K（期間止於 2026-07-03）的摘要指出：財年末 HAMR 產品約占 nearline 每季出貨 exabyte 執行率的 40%；Mozaic 3 已在所有主要雲端客戶通過認證；Mozaic 4（最高 44TB）正與兩大雲端業者放量。此條摘自搜尋結果摘要，未開 10-K 逐字核對。","source":"Seagate Technology Holdings plc Form 10-K FY2026 https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","as_of":"2026-07-03","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Seagate FY2026 營收通路占比：OEM 81%、經銷商 13%、零售 6%；對比前一年 OEM 80%、經銷商 12%、零售 8%（零售降 2 個百分點）。","source":"Seagate FY2026 10-K / ARS（SEC EDGAR，stx-20260703.htm；stxq426filingx2026x08x31x1.pdf）；百分比取自搜尋結果摘要，WebFetch 只抓到 10-K 部分段落，未能親眼對到該表","as_of":"2026-07-03","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Seagate 10-K 寫明：主要客戶（含 OEM 與超大型雲端業者）依主採購協議（master purchase agreements）購買，依客戶採購單與需求預測出貨；針對高容量 nearline 硬碟，與關鍵客戶建立較長期的需求預測與供應承諾，並在特定情況下設有取消費用條款。","source":"Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm","as_of":"2026-07-03","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"DIGITIMES 報導標題與開頭：Seagate 正走向以合約為主的商業模式，因雲端與超大型客戶更重視供應可預期性，勝過短期採購彈性。（全文付費牆，僅確認標題與開頭一句。）","source":"DIGITIMES Asia, Sherri Wang, 'Seagate leans on long-term contracts as storage demand stabilizes', https://www.digitimes.com/news/a20260429VL218/seagate-demand-business-capacity-hdd.html","as_of":"2026-04-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FQ3 2026 法說（搜尋摘要轉述）：Seagate 已與幾乎所有主要雲端／超大型客戶簽有 exabyte 規模供應協議，nearline 產能到 2027 日曆年幾乎全數配置；正在敲定涵蓋到 FY2027 年底的 build-to-order 合約（定義規格與價格）；規劃討論已延伸到 2028 年以後，多年期客戶協議延伸至 2028–2029。細節取自搜尋摘要，未逐字對到逐字稿。","source":"Seagate Q3 FY2026 earnings call（Alpha Spread 逐字稿頁 https://www.alphaspread.com/security/xber/847/investor-relations/earnings-call/q3-2026；Seagate 8-K stx-20260428.htm）","as_of":"2026-04-28","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#4","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Seagate 32TB 容量硬碟開始向通路（channel）與零售夥伴全球出貨。","source":"Business Wire, 'Seagate 32TB Capacities Now Shipping to Channel and Retail Partners Globally', https://www.businesswire.com/news/home/20260112624971/en/Seagate-32TB-Capacities-Now-Shipping-to-Channel-and-Retail-Partners-Globally","as_of":"2026-01-12","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#5","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"同業對照（非 STX）：Western Digital 與前七大客戶有確定採購單，其中兩家簽有 2027 日曆年長約、一家簽有 2028 日曆年長約（搜尋摘要轉述）。","source":"Blocks & Files, 'Western Digital blows hard disk drive future wide open', https://www.blocksandfiles.com/ai-ml/2026/02/03/western-digital-blows-hard-disk-drive-future-wide-open/4090494","as_of":"2026-02-03","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"賣方共識目標價平均 $1,125（S&P Global 口徑，25 位分析師）；評等分布為 4 strong buy、18 buy、2 hold、0 sell、1 strong sell（88% 偏多）。","source":"24/7 Wall St.《Seagate Went From $207 to $1,144. Where Does It Go Next?》https://247wallst.com/investing/2026/09/22/seagate-went-from-207-to-1144-where-does-it-go-next/","as_of":"2026-09-22","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY2027 EPS 共識由 90 天前的 $26.58 上修至 $35.78（+$9.20，約 +34.6%），過去 30 天有 20 次上修。","source":"24/7 Wall St.《Seagate Went From $207 to $1,144. Where Does It Go Next?》https://247wallst.com/investing/2026/09/22/seagate-went-from-207-to-1144-where-does-it-go-next/","as_of":"2026-09-22","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 FY2026 Q4 財報（2026-07-28 公布）：FY2026 營收 $12.195B、non-GAAP 稀釋 EPS $15.58；Q1 FY2027 guidance 營收 $4.1B ± $0.1B（區間 $4.0–4.2B）、non-GAAP 稀釋 EPS $7.30 ± $0.20（區間 $7.10–7.50）。","source":"Stock Titan 轉載 Seagate 8-K（Seagate Technology (NASDAQ: STX) grows FY 2026 revenue 34%, sets Q1 2027 guidance）https://www.stocktitan.net/sec-filings/STX/8-k-seagate-technology-holdings-plc-reports-material-event-cc26f1efc96e.html","as_of":"2026-07-28","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 FY2027 營收 guidance $4.0–4.2B，對照當時營收共識 $3.79B（搜尋摘要所述，來源文章標題為 The Sell-Off Was Wrong? Here's the Proof）。","source":"TOPONE Markets《Seagate Stock (STX): The Sell-Off Was Wrong？Here's the Proof》https://www.top1markets.com/news/seagate-stock-stx-q4-2026-earnings-bea-fm26","as_of":"2026-07-28","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY2026 Q3 財報（約 2026-04-28）時，公司給 Q4 FY2026 guidance：營收 $3.45B ± $0.1B、non-GAAP EPS $5.00 ± $0.20；對照當時共識營收 $3.16B（guidance 高約 9%）、EPS $3.97（guidance 高約 26%）。同一份 Q4 實際營收為 $3.629B（YoY +48.49%）。","source":"Bitget News《Seagate Technology (STX) FY2026 Q3 Earnings Highlights: Revenue +44% YoY, Q4 Guidance Significantly Ahead, Nearline Capacity Booked Through 2027》https://www.bitget.com/news/detail/12560605390341；MarketBeat《Seagate Technology (NASDAQ:STX) Issues Q4 2026 Earnings Guidance》https://www.marketbeat.com/instant-alerts/seagate-technology-nasdaqstx-issues-q4-2026-earnings-guidance-2026-04-28/；Q4 實際營收見 24/7 Wall St. 2026-09-22 文章","as_of":"2026-04-28","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"Seagate 同意支付 1.75 億美元和解證券集體訴訟（每股約 1.03 美元）；原告指控公司隱瞞對中國客戶（Huawei）銷售規模且違反美國出口管制。集體期間 2020-09-14 至 2023-04-19，N.D. Cal. 受理；被告（Seagate、CEO Mosley、CFO Romano）否認指控。法院於 2026-07-07 初步核准和解，最終聽證會 2026-11-17，請求權申報截止 2026-10-19。","source":"Seagate Securities Litigation 和解網站 https://seagatesecuritieslitigation.com/（金額、期間、聽證日、截止日）；初步核准日 2026-07-07 見 Kessler Topaz https://www.ktmc.com/new-cases/seagate-technology-holdings-plc/ 與 Levi & Korsinsky https://zlk.com/cases/seagate-technology-holdings-plc-class-action-lawsuit-stx 的搜尋摘要（該日期未在和解網站頁面正文中出現）","as_of":"2026-07-07","affects":["decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2023-04-18 Seagate 與美國商務部 BIS 簽和解協議，處理對 Huawei 販售硬碟一案；公司同意向 BIS 支付 3 億美元，自 2023-10-31 起五年內每季分期 1,500 萬美元。截至 FY2026 Q2 10-Q（期末 2026-01-02），資產負債表列示應計餘額 6,000 萬與 1.05 億美元兩筆。","source":"Seagate Technology Holdings plc Form 10-Q（期末 2026-01-02）https://www.sec.gov/Archives/edgar/data/1137789/000113778926000026/stx-20260102.htm，Legal Proceedings / Contingencies","as_of":"2026-01-02","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"同一份 10-Q 載明證券集體訴訟修正後起訴書於 2024-09-12 提出，法院於 2025-05-12 部分准許、部分駁回被告的駁回動議；此後的和解見另一條。10-Q 亦列出待決專利爭議（Lambeth Magnetic Structures、Godo Kaisha IP Bridge 1），以及一件對懸臂組件（suspension assembly）供應商的反壟斷案，該案於 2026-01-08 有上訴進展。","source":"Seagate Technology Holdings plc Form 10-Q（期末 2026-01-02）https://www.sec.gov/Archives/edgar/data/1137789/000113778926000026/stx-20260102.htm，Legal Proceedings / Contingencies","as_of":"2026-01-02","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"Seagate 於 2025-03-31 完成收購 Intevac（薄膜製程設備供應商），全現金，每股 4.00 美元；協議 2025-02-13 公告，要約收購 2025-03-28 到期。此事件發生在近 12 個月窗口之前。","source":"Business Wire「Seagate Completes Acquisition of Intevac」https://www.businesswire.com/news/home/20250330889241/en/Seagate-Completes-Acquisition-of-Intevac；「Seagate Announces Agreement to Acquire Intevac」https://www.businesswire.com/news/home/20250213031336/en/Seagate-Announces-Agreement-to-Acquire-Intevac","as_of":"2025-03-31","affects":["moat_trend"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"2026-02-19 Seagate HDD 完成以私下協商方式交換 6 億美元本金的 3.50% 2028 年到期可交換優先票據。","source":"Seagate IR 新聞頁 https://investors.seagate.com/news/default.aspx（引自搜尋摘要，原始新聞稿未開啟）","as_of":"2026-02-19","affects":["valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Seagate is expanding its HDD head facility in Bloomington, MN by almost 3X, from 11,000 sq ft of clean room space to 19,000 sq ft. The article says the added capacity is expected 12-18 months out, i.e. later 2027 or 2028.","source":"Yahoo Finance (Forbes/Tom Coughlin syndication), 'Hard Disk Drive Unit Shipments Could Grow To Support AI Workloads', https://finance.yahoo.com/technology/articles/hard-disk-drive-unit-shipments-031628090.html","as_of":"2026-07-09","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"TDK announced increased HDD head production capacity in April 2026, to support demand from Toshiba and possibly other HDD makers.","source":"Yahoo Finance (Forbes/Tom Coughlin syndication), 'Hard Disk Drive Unit Shipments Could Grow To Support AI Workloads', https://finance.yahoo.com/technology/articles/hard-disk-drive-unit-shipments-031628090.html","as_of":"2026-07-09","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Seagate and Western Digital both prioritize raising storage capacity (exabyte) shipments over raising HDD unit volume. The article's unit-shipment scenarios: +1.2% from 2025 to 2026; about +11% over 2026-2030 (median); up to +30% over 2026-2030 (high case, tied to capacity expansion announcements).","source":"Yahoo Finance (Forbes/Tom Coughlin syndication), 'Hard Disk Drive Unit Shipments Could Grow To Support AI Workloads', https://finance.yahoo.com/technology/articles/hard-disk-drive-unit-shipments-031628090.html","as_of":"2026-07-09","affects":["moat_trend","thesis.H","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Seagate FY2026 capex was $569M, up from $265M the prior year, about 4.7% of revenue. The article gives no FY2027 capex guidance.","source":"XenoSpectrum, 'Seagate's Gross Margin Hits 52.7%, HDDs in the AI Era Earn Through Density, Not Unit Volume', https://xenospectrum.com/en/seagate-fy2026-hamr-margin/","as_of":"2026-07-29","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Seagate nearline HDD supply allocations are largely filled through 2028, and customers are already discussing 2029 and later procurement. Cloud providers want to lock in capacity over several years rather than buy spot. The article says Seagate must meet demand through areal density rather than unit volume growth.","source":"XenoSpectrum, 'Seagate's Gross Margin Hits 52.7%, HDDs in the AI Era Earn Through Density, Not Unit Volume', https://xenospectrum.com/en/seagate-fy2026-hamr-margin/","as_of":"2026-07-29","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Trefis 引述 Seagate 管理層：nearline 產能『almost fully allocated through calendar 2027』（已被預訂到 2027 年底）。","source":"Trefis, 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand', https://www.trefis.com/stock/stx/articles/597921/seagate-is-sold-out-through-2027-as-ai-reshapes-hard-drive-demand/2026-04-30","as_of":"2026-04-30","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"同篇 Trefis 文章寫：Seagate 現在是『setting terms with customers rather than reacting to market fluctuations』，走多年期 build-to-order 合約；並稱傳統的庫存過剩風險『no longer a near-term concern』（此為 Trefis 的描述，非公司財報數字）。","source":"Trefis, 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand', https://www.trefis.com/stock/stx/articles/597921/seagate-is-sold-out-through-2027-as-ai-reshapes-hard-drive-demand/2026-04-30","as_of":"2026-04-30","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"同篇 Trefis 文章引述：非 GAAP 毛利率 Q3 達『all-time high of 47.0%』，去年同期為 36.2%。","source":"Trefis, 'Seagate Is Sold Out Through 2027 As AI Reshapes Hard Drive Demand', https://www.trefis.com/stock/stx/articles/597921/seagate-is-sold-out-through-2027-as-ai-reshapes-hard-drive-demand/2026-04-30","as_of":"2026-04-30","affects":["valuation","moat_trend"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2023（截至 2023-06）營收 $7.384B，FY2022 為 $11.661B；GAAP 毛利率 18.3%（FY2022 為 29.7%）、non-GAAP 毛利率 21.1%（FY2022 為 30.1%）；GAAP 淨損 $529M（FY2022 為淨利 $1.649B）；營運現金流 $942M（FY2022 為 $1.657B）。","source":"Seagate IR — Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2023 Financial Results, https://investors.seagate.com/news/news-details/2023/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2023-Financial-Results/default.aspx","as_of":"2023-07-26","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2023 第四季（2023-06 季）營收 $1.602B，去年同期 $2.628B；GAAP 毛利率 19.0%（去年同期 28.9%）、non-GAAP 毛利率 19.5%（去年同期 29.3%）；GAAP 淨損 $92M。","source":"Seagate IR — Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2023 Financial Results, https://investors.seagate.com/news/news-details/2023/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2023-Financial-Results/default.aspx","as_of":"2023-07-26","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"過去十二個月（至 FY2023 結束）產能閒置費用（扣除折舊攤銷後）合計 $171M，公司揭露原因含無錫廠疫情封控與生產計畫調整。","source":"Seagate IR — Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2023 Financial Results, https://investors.seagate.com/news/news-details/2023/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2023-Financial-Results/default.aspx","as_of":"2023-07-26","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2023 第三季（2023-03 季）營收約 $1.9B、毛利率 17%，為搜尋摘要所見 FY2023 各季中最低的一季（搜尋摘要轉述 10-Q 與 Seagate IR 第三季新聞稿；未抓全文核對，as_of 取季末日）。","source":"SEC Form 10-Q for quarter ended 2023-03-31, https://www.sec.gov/Archives/edgar/data/1137789/000113778923000029/stx-20230331.htm","as_of":"2023-03-31","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#4","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Blocks and Files 報導：FY2023 營收較前一年下滑 37%，為 17 年來最低年度營收，也是 13 年以上來首次全年虧損；CEO Mosley 稱「a profound downturn in demand」，原因包含中國復甦不均、雲端庫存消化、企業支出謹慎；最大買家超大規模雲端業者的 nearline 硬碟採購大減。","source":"Blocks and Files — Seagate cites 'profound downturn in demand' as revenues dip... and it won't get better soon, https://www.blocksandfiles.com/disk/2023/07/27/seagate-cites-profound-downturn-in-demand-as-revenues-dip-and-it-wont-get-better-soon/1613546","as_of":"2023-07-27","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#5","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Tom Coughlin（Forbes）：2023 年第二季全產業硬碟出貨總容量（EB）較第一季下降約 19.3%；2023 全年出貨容量估約 875EB，較前一年下降約 29%（搜尋摘要彙整自 Coughlin 系列文章，全年數字對應文章為 2023-12-10 的 2024 年預測，未抓全文核對）。","source":"Forbes / Tom Coughlin — C2Q 2023 Hard Disk Drive Industry Update, https://www.forbes.com/sites/tomcoughlin/2023/08/14/c2q-2023-hard-disk-drive-industry-update/ ；Digital Storage And Memory Projections For 2024, Part 1, https://www.forbes.com/sites/tomcoughlin/2023/12/10/digital-storage-and-memory-projections-for-2024-part-1/","as_of":"2023-08-14","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#6","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"Coughlin 硬碟產業歷史文章：硬碟營收自 1956 年起長期成長至 2012 年見頂（該年因前一年泰國水災造成硬碟短缺而墊高），出貨顆數高點在 2010 年（6.51 億顆）；此後營收與顆數均下滑（搜尋摘要轉述，未抓全文）。","source":"Forbes / Tom Coughlin — Hard Disk Drive Revenue History From 1957 To Today, https://www.forbes.com/sites/tomcoughlin/2024/01/02/hard-disk-drive-revenue-history-from-1957-to-today/","as_of":"2024-01-02","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#7","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"+","claim":"對照點：Seagate FY2026 第三季 non-GAAP 毛利率為創紀錄的 47%，較上季增 480 bps、較去年同期增約 1,080 bps。","source":"Yahoo Finance — Can Seagate Sustain Its Gross Margin Expansion Momentum?, https://finance.yahoo.com/markets/stocks/articles/seagate-sustain-gross-margin-expansion-135900141.html","as_of":"2026-05-22","affects":["valuation","moat_trend"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Seagate 於 2025-03-31 完成收購 Intevac（薄膜製程設備供應商），全現金，每股 4.00 美元；協議 2025-02-13 公告。此事件發生在近 12 個月窗口之前。","source":"Business Wire「Seagate Completes Acquisition of Intevac」https://www.businesswire.com/news/home/20250330889241/en/Seagate-Completes-Acquisition-of-Intevac；「Seagate Announces Agreement to Acquire Intevac」https://www.businesswire.com/news/home/20250213031336/en/Seagate-Announces-Agreement-to-Acquire-Intevac","as_of":"2025-03-31","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Seagate 同意支付 1.75 億美元和解證券集體訴訟（每股約 1.03 美元）；集體期間 2020-09-14 至 2023-04-19，N.D. Cal. 受理；被告否認指控。法院於 2026-07-07 初步核准和解，最終聽證會 2026-11-17，請求權申報截止 2026-10-19。","source":"Seagate Securities Litigation 和解網站 https://seagatesecuritieslitigation.com/（金額、期間、聽證日、截止日）；初步核准日 2026-07-07 見 Kessler Topaz https://www.ktmc.com/new-cases/seagate-technology-holdings-plc/ 搜尋摘要","as_of":"2026-07-07","affects":["decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2026 Q2 10-Q（期末 2026-01-02）另列待決專利爭議（Lambeth Magnetic Structures、Godo Kaisha IP Bridge 1）與一件對懸臂組件供應商的反壟斷案（2026-01-08 有上訴進展）。","source":"Seagate Technology Holdings plc Form 10-Q https://www.sec.gov/Archives/edgar/data/1137789/000113778926000026/stx-20260102.htm，Legal Proceedings","as_of":"2026-01-02","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 15 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"STX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.58,"operating_margin_pct":34.65,"fcf_margin_pct":25.46,"rd_intensity_pct":6.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STX","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"MU","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.57,"operating_margin_pct":65.67,"fcf_margin_pct":28.99,"rd_intensity_pct":5.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU","as_of":"TTM ending 2026-05-31（4季加總）"}},{"name":"000660.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.27,"operating_margin_pct":68.04,"fcf_margin_pct":47.8,"rd_intensity_pct":4.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"005930.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.48,"operating_margin_pct":36.88,"fcf_margin_pct":28.95,"rd_intensity_pct":9.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"285A.T","period":"TTM ending 2025-12-31（3季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.285A.T","as_of":"TTM ending 2025-12-31（3季加總）"},"note":"Total Revenue 缺失，無法算利潤率；僅 3 季可得，非完整 TTM"}],"subject":"STX"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STX/STX_Q4_2026_Earnings_Call_20260728.md）

# Q4 2026 Earnings Call
2026-07-28

Q4 2026 Earnings Call
Seagate Technology Holdings plc | Earnings Calls | 2026-07-28
Operator (Operator)
Welcome to the Seagate Technology Fiscal Fourth Quarter and Fiscal Year 2026 Conference Call.
[Operator Instructions] Please note this event is being recorded. I would now like to turn the
conference over to Shanye Hudson, Senior Vice President, Investor Relations. Please go ahead.
Shanye Hudson (Executives)
Thank you. Hello, everyone, and welcome to today's call. Joining me are Dave Mosley, Seagate's Chair
and Chief Executive Officer; and Gianluca Romano, our Chief Financial Officer. We've posted our
earnings press release and detailed supplemental information for our Q4 and fiscal 2026 year-end
results on the Investors section of our website.
During today's call, we'll refer to GAAP and non-GAAP measures. Non-GAAP figures are reconciled to
GAAP figures in the earnings press release posted on our website and also included on our Form 8-K.
We've not reconciled certain non-GAAP outlook measures because material items that may impact
these measures are out of our control and/or cannot be reasonably predicted. Therefore, a
reconciliation to the corresponding GAAP measures is not available without unreasonable effort.
Before we begin, I'd like to remind you that today's call contains forward-looking statements that reflect
management's current views and assumptions based on information available to us as of today and
should not be relied upon as of any subsequent date. Actual results may differ materially from those
contained in or implied by these forward-looking statements as they're subject to risks and
uncertainties associated with our business.
To learn more about the risks, uncertainties and other factors that may affect our future business
results, please refer to the press release issued today and our SEC filings, including our most recent
annual report on Form 10-K and quarterly report on Form 10-Q as well as the supplemental
information, all of which may be found on the Investors section of our website.
Following our prepared remarks, we'll open the call up for questions. [Operator Instructions]
With that, I'll hand the call over to you, Dave.
William Mosley (Executives)
Thanks, Shanye, and hello, everyone. Seagate delivered a very strong finish to an outstanding fiscal
2026. Our June quarter results outperformed our expectations for both revenue and non-GAAP EPS,
and we expanded our non-GAAP gross margin for a 13th consecutive quarter. Our performance led to
free cash flow margins of 31%, which totaled more than $1.1 billion, our strongest quarter in over a
decade.
Our impressive fiscal 2026 financial performance was underpinned by the 3 structural growth pillars
that I outlined last quarter: sustainable market demand, our differentiated technology road map and
disciplined operational execution.

First, sustainable market demand. As our results show, demand for mass capacity storage is strong and
growing. We delivered fiscal year revenue growth of 34%, led by cloud customers' demand for data
storage solutions amplified by the adoption of AI-enhanced applications. Given our momentum and the
improved visibility we have into demand, we expect fiscal 2027 revenue growth to outpace our
performance in fiscal 2026.
Second, we are executing our differentiated technology road map, anchored by our HAMR-based
Mozaic platform. HAMR enables us to increase areal density and store more data on each disk. As a
result, we can scale exabyte shipments to meet rising demand in a highly capital-efficient manner to
capture more value per drive. Exiting the year, HAMR-based products represented approximately 40%
of our nearline exabyte shipment run rate, and we continue to invest in HAMR capabilities to support
our mid-20% exabyte growth target while further enhancing profitability and capital efficiency.
Our third pillar centers on translating demand strength and technology advancements into profitable
growth. In fiscal '26, we increased non-GAAP gross margin 10 percentage points, grew non-GAAP EPS
more than 90% and generated record free cash flow of $3.1 billion. Looking ahead to fiscal '27, we
expect to deliver sequential margin and cash generation growth throughout the year.
Our confidence is supported by the scale, quality and duration of our data center customer
commitments in a strengthening demand environment. Data center demand now represents
approximately 90% of our exabyte shipments. Based on the long-term supply agreements in place
today, the vast majority of our nearline exabytes are now allocated into calendar 2028. Importantly, we
are not seeing customers pull back on planning horizons.
As our strategic relationships deepen, many are actively seeking to extend planning horizons through
2029 and beyond, which we believe reflects growing confidence in their own long-term infrastructure
needs. These engagements reinforce our view of demand durability while providing customers greater
supply assurance and support for the key technology transitions. We remain disciplined in securing
orders from these customers prior to initiating drive production with contracts that define both product
configuration and pricing terms covering the entirety of calendar 2027.
We continue to execute our value-based pricing strategy, balancing a stronger demand environment
with our objective of supporting sustainable, profitable growth over the long term. Cloud customers
remain the largest driver for nearline demand today with 3 years of sequential quarterly exabyte growth
and no evidence of a slowdown as AI adoption now builds on demand for traditional data-intensive
applications, including video.
We continue to benefit from cloud infrastructure deployments, which fuel the need for scalable, cost-
efficient and reliable storage. At the same time, we believe storage demand will prove durable through
investment cycles. First, new data is constantly being created across existing cloud and enterprise
infrastructure. And second, customers are retaining and reusing more of that data over time as its value
extends beyond its initial use. AI is reinforcing these trends and illustrating how data is not only
growing, it is compounding.
With the transition from AI model training to inference to agentic applications, more data is generated
and retained for historical context, compliance and future reuse. As these data center environments
become larger and more complex, customers must balance performance, energy consumption and cost
across distributed infrastructures. Cloud providers have long addressed these challenges through tiered

storage architectures that combine high-performance memory and SSDs with mass capacity hard
drives to optimize performance and economics at scale.
Our recent white paper with SK hynix illustrates the importance of tiered storage for inference and
agentic AI workloads, which show a direct benefit to hard drive storage. These workloads rely on
persistent context across user interactions and key value or KV cache is used to retain and reuse that
context efficiently. KV cache can expand significantly as the number of users increase and interactions
become longer and more sophisticated.
Our research found that by extending KV cache data across memory, SSD and hard drive tiers,
organizations can retain more context and avoid recomputing previously generated data. This drives
the need for increased hard drive storage and reduces GPU usage during the most compute-intensive
phases of an agentic application. As a result, GPU resources are available for additional revenue-
generating workloads.
Additionally, we are now seeing the relevance of tiered storage extend beyond large cloud data centers
into enterprise deployments. As enterprises increasingly operate across public cloud, private cloud and
on-prem environments, they must manage growing volumes of structured and unstructured data while
facing similar performance, cost and energy consumption trade-offs that hyperscalers have addressed
for years. We see this broadening of demand in our business.
Enterprise nearline revenue increased for a fifth consecutive quarter in June and we are engaging more
frequently with neocloud operators and leading model developers. As their data management needs
scale, these providers are starting to adopt modern tier storage architectures where hard drives provide
the trusted mass capacity foundation.
Looking ahead, we believe physical AI applications such as robotics and autonomous vehicles will drive
the next step function expansion in data creation and retention at the edge. These applications rely on
world models trained on millions of hours of historical and synthetic video content in order to
understand and reliably interact with the physical world. Taken together, these trends reinforce a
structural change in storage demand. Applications are creating, retaining and reusing more data across
cloud and enterprise environments than ever before, extending the role of mass capacity storage across
modern tiered architectures and creating additional opportunities for Seagate over time.
Our technology road map plays an integral role in Seagate's ability to capitalize on growing storage
demand. Advancing areal density is our North Star. We believe that increasing the amount of data
stored on every disk we produce is the fastest, most capital-efficient path to supporting long-term
exabyte growth while maintaining relatively stable hard drive unit output.
Our expertise across material science, precision manufacturing, advanced photonics and nanoscale
wafer production has enabled us to pioneer HAMR technology and the Mozaic platform, which have
increased storage density per disk and per drive. We continue to push the boundaries of innovation as
demonstrated by our vertically integrated laser manufacturing capabilities, which yielded tens of
millions of edge-emitting lasers last quarter.
Our team's achievements underscore the scale, maturity and supply chain resilience behind our Mozaic
platform. These innovations are improving the total cost of ownership for our customers while
expanding our exabyte output and enhancing efficiency across our operations and supply chain. We
ended fiscal 2026 on schedule with our HAMR-based product ramp. Our Mozaic 3 products are now
qualified and operating in production environments across all major cloud customers.

Our second-generation Mozaic 4 platform capable of supporting up to 44 terabytes per drive continues
to ramp with the 2 largest global CSPs and additional customer qualifications are underway. We expect
to achieve our next ramp milestone by exiting calendar '26 with 50% of our HAMR exabytes on our
Mozaic 4 platform.
Looking further ahead, Mozaic 5, our 5-plus terabyte per disk platform, remains on track for
qualification shipments in late calendar 2027. Wrapping up, we delivered across the board in fiscal
2026 with each quarter building on the momentum of the last, and we expect that momentum to
continue through fiscal 2027. The growth in data creation, retention and utilization continues to elevate
the importance of hard drive storage and modern data architectures. Together, our demand outlook,
differentiated technology strategy and disciplined execution position Seagate to capture the significant
opportunities ahead and create long-term value for our stakeholders.
I'll close by thanking our global team for another year of outstanding execution. I'd also like to thank
our customers, suppliers, partners and shareholders for their continued support and trust in the
company.
With that, I'll turn it over to Gianluca.
Gianluca Romano (Executives)
Thank you, Dave. We capped fiscal 2026 delivering strong sequential double-digit top and bottom line
growth in the June quarter, supported by disciplined operational execution and both revenue and gross
margin expansion across every end market we serve.
June quarter revenue was $3.6 billion, up 17% sequentially and up 48% year-over-year, exceeding the
high end of our guidance range. We achieved record profitability levels across gross margin, operating
margin and earnings per share.
Non-GAAP gross margin came in at 52.7%, up 570 basis points sequentially. Non-GAAP operating
margin increased 710 basis points sequentially to 44.6% and non-GAAP EPS was $5.71, up 39%
quarter-over-quarter and 121% year-over-year, exceeding the high end of our guidance range by a wide
margin.
As Dave noted earlier, we generated free cash flow of more than $1.1 billion, rounding out our best
quarterly performance in over a decade. Sustained data center demand continued to outpace broader
company growth. In the June quarter, we shipped a total of 218 exabytes, up 34% year-over-year, with
data center representing 89% of the total. We shipped 195 exabytes into the data center market, up 11%
sequentially and 43% year-over-year, with data center revenue coming in at $2.9 billion, up 17%
sequentially and 57% year-over-year.
Global cloud customers are driving the vast majority of data center revenue and exabyte demand. At the
same time, demand trends in the enterprise OEM data center markets have strengthened, reflecting
growing storage requirements across a broader set of customers and workloads, many of which Dave
highlighted earlier.
In the June quarter, we delivered strong double-digit year-over-year growth across both revenue and
exabyte shipments into the enterprise OEM markets. To support long-term demand growth, we
continue to expand the deployment of HAMR technology across our product portfolio. Our goal is to
transition an increasing portion of production to HAMR-based products first to address cloud
customers and over time, to broaden adoption across enterprise deployments.

As we make this transition, we are strategically investing in additional tools and technology to support
the manufacturing of our HAMR products. These investments enable us to maintain relatively stable
drive unit output as customers mix up to higher capacity drives and manufacturing cycle time increase.
We believe this action will enable us to deliver nearline exabyte growth in the mid-20% range over the
next few years.
Beyond the data center, our edge IoT market made up 19% of revenue at $697 million, up 14%
sequentially and 20% year-over-year due in part to ongoing tight supply conditions and increasing
NAND pricing.
Moving on to the rest of the income statement. Non-GAAP gross profit increased significantly to $1.9
billion, up 31% quarter-over-quarter and more than doubling year-over-year. Non-GAAP gross margin
expanded to 52.7%, up from 47% in the prior period. This improvement reflects continued execution of
our long-term pricing strategy and a stronger product mix. We expect these trends to remain favorable,
underpinned by strong demand. Non-GAAP operating expenses were $293 million or 8% of revenue,
reflecting our discipline in cost management. Non-GAAP operating profit increased 39% sequentially to
$1.6 billion, representing 44.6% of revenue and underscoring the scalability of our financial model,
continued areal density innovation, supply discipline and pricing strategy execution.
In the June quarter, other income and expenses were $58 million, and we project OI&E to decrease
further in the September quarter to approximately $45 million, reflecting the benefit from lower
interest expense as we continue to reduce our outstanding debt balance. Non-GAAP net income grew to
$1.3 billion with corresponding non-GAAP EPS of $5.71 per share based on tax expense of $242 million
and a diluted share count of approximately 231 million shares, including the net impact of our 2028
convertible notes.
Turning now to the cash flow and the balance sheet. In the June quarter, we invested $187 million of
capital expenditures, with total fiscal 2026 CapEx representing 4.7% of revenue. Looking ahead, we
expect capital expenditures for fiscal 2027 will remain well within our target range of 4% to 6% of
revenue. Free cash flow generation expanded to $1.1 billion, up 17% from the prior quarter. We expect
cash generation to further improve throughout fiscal 2027, supported by sustained demand,
operational efficiencies and CapEx investment discipline.
During the June quarter, we returned approximately $283 million to shareholders through dividends
and share repurchases. Strengthening the balance sheet was a key objective for fiscal 2026 and we
delivered on our plans. We ended the year with cash and cash equivalents of $1.7 billion and strong
liquidity of $3 billion, including our undrawn revolving credit facility.
Our gross debt balance was approximately $3.6 billion exiting fiscal '26, down $1.4 billion year-over-
year, including $300 million that we retired in the June quarter. Our resulting net leverage ratio
improved to 0.4x based on adjusted EBITDA of $1.7 billion for the June quarter, up 37% quarter-over-
quarter and 142% year-over-year.
During the September quarter, we are retiring an additional $1.2 billion in debt. We have already
extinguished $1 billion in high-yield senior notes in July and plan to retire the remaining balance on
our convertible notes in September.
Turning now to the September quarter outlook. Visibility from our BTO model reinforces our
confidence in sustained demand for high-capacity nearline drives as AI adoption accelerates. We see
continued revenue and profitability expansion in the September quarter, supported by our Mozaic

ramp and pricing strategy. We expect September quarter revenue to be in the range of $4.1 billion, plus
or minus $100 million, which represents a 56% year-over-year improvement at the midpoint.
Non-GAAP operating expenses are expected to be approximately $300 million. Based on the midpoint
of our revenue guidance, non-GAAP operating margin is expected to be around 50%. Non-GAAP EPS is
expected to be $7.30, plus or minus $0.20, based on a tax rate of about 16% and non-GAAP diluted
share count of 231 million shares, including estimated dilution from our 2028 convertible notes of
approximately 2 million shares.
To close, Seagate's financial results and outlook demonstrate our ability to deliver profitable growth,
expand margins and drive significant cash generation. We remain confident in delivering sequential
revenue growth and margin expansion through fiscal 2027, while creating long-term value for
customers and shareholders.
Operator, let's open the call up for questions.
Operator (Operator)
[Operator Instructions] Our first question comes from Aaron Rakers with Wells Fargo.
Aaron Rakers (Analysts)
Congrats on the results. I want to dig a little bit deeper into the gross margin. I guess, given the
guidance that you've outlined, it looks like your guide is implying like a mid-57% or so gross margin
into this next quarter. So I guess my question is, one, is that kind of the guidance that you're providing?
And two, how do you think about the cost down execution as we move through Mozaic 3 to Mozaic 4?
You've been operating at like a mid-teens kind of cost down per year on a per terabyte basis. Do you
think that's sustainable? Or how should we think about modeling that over the longer term?
William Mosley (Executives)
Aaron, I'll let Gianluca answer this quantitatively, but the way we're thinking about these product
transitions is and I think you know this well, we have to actually put our factories on pause to go
through the product and transition a little bit. So as we're moving product from 3 terabytes to 4
terabytes to 5 terabytes. And then there's yield issues. And as we out-execute our plan, what happens is
we have opportunity for cost to drive better cost than we thought. So that answers the second part of
your question. Gianluca?
Gianluca Romano (Executives)
Aaron. So yes, very good result, I would say, on gross margin already in fiscal Q4. So strong
improvement sequentially, and we are guiding up again. So our pricing strategy is continuing as we
have discussed now for several quarters. I would say we have adopted this strategy more than 12, 13
quarters ago. So we are continuing in that direction. Every quarter is a bit different, but the strategy is
the same. The mix is helping. We are moving more and more into the high-capacity nearline product.
You have seen another strong increase in nearline exabyte in the quarter.
So everything is continuing in the same direction that we have driven the company for many quarters.
Dave discussed about the cost, of course, moving the mix from 3 terabyte to 4 terabyte per disk is, of
course, giving us another boost in terms of profitability.

Operator (Operator)
The next question is from Ben Reitzes with Melius.
Benjamin Reitzes (Analysts)
Great to be covering you again. I wanted to talk about 2 longer term -- ask you about 2 longer-term
demand drivers potentially. I mean this key value cache use of the HDD tier at hyperscalers. How much
is that helping right now? Is it on the come? And do you expect it to kind of ease into your exabytes?
And how do we look at that? And when do you think physical AI really starts helping your exabytes as
well?
William Mosley (Executives)
Right. Ben, I think that's good. Both very, very early days. I would say that the agentic flows that we're
seeing are actually what -- that's the reason we pointed to the KV cache discussion. I think the keyword
here is context. When you set up these agents, you really need to give them context and sometimes
that's a very broad set of rules across your business or your problem set or whatever. And as you do
that, then you don't want to have to redo that context every time. You don't want to have to recompute
all that context every time. So that's what's driving storage, but still very early days.
Physical AI, we are quite excited about. I think I hear a lot about robotics. We've all seen autonomous
vehicles. People focus very much on the end product, the robot, if you will, but I actually think it's a lot
more of a data play. These robots have sensors on them, they're sensor networks, in order for them to
learn, the data actually comes back up into a local cloud or a bigger cloud. And so when people say
physical AI to me, I think it's a lot more about the data, the data processing, what kind of learning
you're getting from that. And exactly to your question, how much you have to store to make sure you
have that context long term.
So we think these are both great opportunities. In particular, the physical AI stuff is largely more about
video. So it's a very unstructured type of data coming. It's not like the days of old where you had
spreadsheets or checklists to fill out that were complete structured data. This is very unstructured data
that the machines are learning from and they might want to learn again and again and again, but you
don't want to have to repromote that into the memory tier. So we think that's a great opportunity for us.
Operator (Operator)
The next question is from Erik Woodring with Morgan Stanley.
Erik Woodring (Analysts)
Congrats on the really nice results and guide. Gianluca, for a number of quarters, you've been quite
steadfast that price per exabyte growth would be kind of this mid-to-high single digits year-over-year.
You just reported 10% year-over-year price per exabyte growth in June. I think the September quarter
guide implies pricing growth closer to maybe 20% year-over-year or even above that.
Can you maybe just provide an update for us on how we should be thinking about pricing looking
forward, why this trend we're seeing in the September quarter shouldn't sustain or maybe even
accelerate just given supply-demand imbalance, customer demand strength, delivering more value to
customers, et cetera?

Gianluca Romano (Executives)
Erik, you are correct. As I said before, it's not that we are changing our strategy, but for sure, the gap
between supply and demand is now a little bit bigger than a few quarters ago. And our volume was a
little bit higher in fiscal Q4. Now we think it can be maybe a little bit of output available in fiscal Q1.
And of course, we are pricing that increased output at a very good price right now.
So I would say not really a change in our strategy, but a very good execution and with demand being
particularly strong right now, we take a little bit more pricing benefit. Now of course, every quarter is
different. We will see in the following few quarters how the pricing will evolve. But I think we were very
clear, both Dave and I in our prepared remarks, we see every quarter revenue to improve and every
quarter gross margin and profitability in general to increase. So of course, pricing is a part of the
sequential improvement through the fiscal year.
Operator (Operator)
The next question is from Asiya Merchant with Citigroup.
Asiya Merchant (Analysts)
Great results here. And if I may, just on the exabyte CAGR growth, I think you guys reiterated sort of
this mid-20%. You guys obviously have been executing too much greater than that. I think I heard
about some investments that you're doing. Just help us understand like this above 30% exabyte growth
rate, could that sustain as you enter fiscal '27, especially as you're migrating more towards your second-
generation HAMR and then you're ramping into -- further out into your Mozaic 5.0. So if you could just
help us understand why exabyte CAGR could or could not sustain at this 30% as we look into fiscal '27?
William Mosley (Executives)
Thanks, Asiya. As we said before, we're not really increasing the box count. We are working really hard
to get the heads and media inside the boxes to be able to go up in the technology capability to get
exabytes out. And exactly to your point, what's the ultimate CAGR? It's how fast we can do that, how
successfully we can do that. We are going through product transitions. I mentioned this earlier. So as
you do that, there's a little bit of inefficiency in your factories. But long term, you actually get many,
many more exabytes out as we go from 3 to 4 to 5. And that's the way we're focused. What you've seen
so far is the transition largely to 3. We are ramping the 4 right now and the 5 is coming.
And so how we play that is depending upon how we see end customer demand, what the qualification
schedule is like for those customers. And we need visibility because that's 3 to 4 quarters out from when
we do wafer start. But also, we get a little bit better yields. We can add a few more exabytes here and
there, and the team has been doing fantastic on that front. So all of these dynamics are how we actually
have to predict the next few years. And that's one of the reasons we say mid-20s. Could we execute a
little bit better? Conceivably, there's a lot of invention required still.
Operator (Operator)
The next question is from C.J. Muse with Cantor Fitzgerald.
Christopher Muse (Analysts)

A follow-up on pricing. I'm curious if you could kind of speak to like-for-like versus the benefit of newer
products. And then moreover, if you could speak to how we should be thinking about contracts rolling
off, renegotiating of existing contracts and how that is impacting the relative kind of year-over-year
pricing, particularly as it relates to that strong 20-plus percent number embedded in the September
guide and how to think about the moving parts into December and beyond?
William Mosley (Executives)
Thanks, C.J. As we said in the prepared remarks, we're trying to be predictable for at least the next year
because that's what we have visibility to in our factories, and that's when we know the exact
configuration and we determine pricing with our customers. But as various customers are rolling
through those periods, interesting things happen. First, there's product qualification. Like-for-like is
kind of tough because we are moving products so quickly through transitionary periods. That benefits
us. It also benefits them if they're building a data center, they get a better TCO out of those products.
And then there's other architectural reasons that may slow down or speed up their ability to ingest
these things. So it is fairly complicated. What we're seeing over time is not only what we lock in for that
period of a year is we also see our ability to execute a little bit better, and that's usually 2 or 3 quarters
out. That's not in quarter, but we execute a little bit better. We have more exabytes to give, and we
determine how hungry the market really is for those exabytes. And usually, they'll pay more than that
contract price, if you will, for those exabytes. And so that's why you see these step functions.
And therefore, I think we're all confident about the demand that we're seeing, both ourselves and our
customers, but also they're voting every day with that by signing up to pricing that is even higher than
some of the contractual stuff that we have done together.
Gianluca Romano (Executives)
C.J., you were asking about the new orders that we are negotiating and the new LTAs that we are
negotiating. The trend is the same of the past. So we see strong demand and, of course, opportunity for
us to continue to push on our pricing and pricing strategy and continue in the same direction. Every
quarter is a bit different depending how many contract we negotiate, what is the volume for different
customers, what is the upside volume, if any, that is available and what is the price.
So it's not a straight line. But I would say the trend is clear. I'd say we have really performed in the
same way for more than 3 years. At this point is -- right now, it's particularly strong in terms of supply-
demand and pricing. But it's going to continue. We're already discussing about the next 2 or 3 quarters
going in the same direction.
Operator (Operator)
The next question is from Tom O'Malley with Barclays.
Thomas O'Malley (Analysts)
I just had a 2-parter here. So you guys have previously said 70% of nearline exabytes will be HAMR by
June of 2027. How are you tracking to that? And then I saw on the preamble that you specifically called
out as you're transitioning there, you're strategically investing in additional tools, technology and
manufacturing. Is that just something that you normally put in the preamble? It stood out a little bit to

me. Can you maybe be more specific on what you're investing in there to help you get to that percentage
of the total mix?
William Mosley (Executives)
Yes. Tom, we're still pushing HAMR well, and it's reacting exactly what we thought it would a couple of
years ago. We have -- as time has marched on, we have pushed maybe PMR a little bit harder than we
thought. So transitionary, I think we're still on generally the same trends and everything is going well.
Relative to the investment, most of the tools that we're investing in are directly contributing to those
heads and media that are driving those technology transitions. I'm very happy with how the team has
executed on that front, 3 to 4 to 5 like we've talked about before, very optimistic about it. And I think
ultimately, HAMR is going to completely take over the portfolio because of it. We're learning more and
more about the tools all the time, and that's part of how we do areal density development is to get the
latest tools on, learn how to run them and see what we can do with them. And I would say, long term, I
think there's probably more favorability for areal density than I had thought a couple of years ago.
Gianluca Romano (Executives)
In terms of HAMR percentage of exabytes, we have actually just achieved our first milestone, which was
to achieve 40% of nearline exabyte sold on HAMR drive by June. So we just did that. And so I would
say we are on track to achieve the future goals. I'd say on the new investment, there is, of course, a big
difference between components and hard disk drive units. Now if you -- for example, if you look at our
last year, and if you look at the number of disk and the number of heads inside the box, they probably
grew between 15% and 20% and the units were absolutely flat.
So there is always a mix up of drives going more and more into the nearline and going more and more
close to the 10 disk and 20 heads. But of course, there is a strong shift year over year over year. This
happened for the last 10, 20 years. So it's normal that even with flat hard disk drive units, we need to
increase heads and media through time. That's normal part of the business.
Operator (Operator)
The next question...
William Mosley (Executives)
Sorry, one more thing on that point because I think a lot of people still don't understand this. So the
thing that's actually driving factory complexity is not just drive numbers or heads numbers or media
numbers. It's actually the product transitions. These new products, say, 4 terabytes going to 5 terabytes,
there will be more time in the tools, more time through the tools. Sometimes it has to touch the tool
multiple times. The factory complexity is what's driving a lot of the investment that you made reference
of, Tom.
Operator (Operator)
The next question is from Mark Newman with Bernstein.
Mark Newman (Analysts)
Congrats on another great quarter. Lots of questions on the pricing. So I wanted to talk more about the
technology and the cost. Could you update us on the HAMR portion of your shipments? I think you've

guided before 40% exiting the fiscal year on HAMR and 50% exiting calendar year '26. Are we on target
for that or tracking ahead of that guidance you can say on that?
And then also Mozaic 4, you said ramping to global CSPs. So is that going to -- I think you said it's a
very small portion of revenue in the previous quarter, but it's going to become more significant in the
first -- in the September quarter. I just want to clarify that. And then, given all that, should we expect
that cost declines should be potentially accelerating given this upcoming ramp of Mozaic 4 and now you
have almost -- you're now at the sharpest part of the S-curve for the HAMR adoption. So just wanted to
see if anything you can comment on that would be really appreciated.
William Mosley (Executives)
Thanks, Mark. Yes, we're on target for all the metrics that you talked about. I would say relative to
Mozaic 4, it was pretty consequential last quarter even, and it's ramping quite nicely. We intentionally
have maybe throttled the Mozaic 4 ramp because of qualification cycles and everything else and other
customers as they qualify, they're full of the last generation product as well. So things are fairly
complicated in the supply chain. But Mozaic 4 is quite successful out in the market. It will continue to
ramp over the course of this next fiscal year.
Gianluca Romano (Executives)
Yes. No, just to clarify, we started shipping Mozaic 4 in March. So March quarter volume was pretty
low, but June quarter was a good ramp-up. It's also a strong contributor to our financial performance
and will be even better in the September quarter. And then of course, we are already all focusing on the
next step, that will be the 5 terabyte per disk and the 50 terabyte drive in next calendar year.
Operator (Operator)
The next question is from Wamsi Mohan with Bank of America.
Wamsi Mohan (Analysts)
I was wondering if you could maybe just clarify on how much of your fiscal '27, fiscal '28 exabyte view is
locked in via build-to-order versus maybe not under LTAs. And as you think about the pricing uplift in
September, part of that is coming from one of your initial HAMR customers that have more favorable
pricing rolling off. So should we still expect the price momentum to continue at those levels for the rest
of the fiscal year? I know you said that you would see revenue and margin increase every quarter, but
any thoughts on sort of the magnitude of either sequential or year-on-year given those comments
around the initial customer?
William Mosley (Executives)
Yes. Wamsi, you're right. On the second point, I think it's important to realize that as we do roll
through, there's different phases that different customers are under and that renegotiation occurs. We
are pretty predictable, I think, through FY '27. So we have good line of sight, but we are also getting a
little bit more product out as we continue these product ramps because we're working the yields and
scrap really aggressively on new products. So to the extent that we can, since there's such strong
exabyte demand out there, we'll offer that to people out in the market that are showing us that
opportunity.

Gianluca Romano (Executives)
Yes. Relatively to that particular customer, the volume that was sold at the preferential price in June
was minimum. So September, we will not have any. So there is a little bit of positive impact from that.
But it's not the major reason why pricing is a little bit better in September than June. Of course, it's
more overall demand and all the customers that are chasing a bit more volume right now.
Operator (Operator)
The next question is from Joseph Cardoso with JPMorgan.
Joseph Cardoso (Analysts)
Maybe just a clarification from my end on not really seeing or trying to increase the box count here.
Does that encompass your visibility into nearline allocations into 2028 and the planning that you're
seeing extending into '29? And then how should we think about visibility into pricing in those outer
years as well?
William Mosley (Executives)
Thanks, Joseph. Yes, I mean, you're right. Thanks for the question because many investors are new to
the stock, so we'll try to explain this again. So our strategy coming out of the last down cycle has been to
keep the number of drives flat, and we're still on that path. Inside the drives, however, there's all these
critical components, heads and media, and that is rising slightly. I think Gianluca made reference to
this before. So that puts strain on our internal heads and media fabs, which are under our control, and
we're going through these aggressive transitions. That's the big story.
The big story is the process content, the manufacturing complexity as we move from 3 terabytes to 4
terabytes to 5 terabytes. The routes get more complicated and the technology transitions are putting a
large strain on these -- on our internal components. But with the curves that we're on, we believe that
this is the best way to bring more exabytes out in the world is to stay focused this way. And so that's our
strategy.
Operator (Operator)
The next question is from Karl Ackerman with BNP Paribas.
Karl Ackerman (Analysts)
Dave, you spoke about qualifications on Mozaic among hyperscalers, but how should we think about
Seagate's growing exposure to neoclouds and foundational model companies? I was hoping you could
parse between demand from traditional hyperscale, neocloud and maybe on-prem implicit in your
September outlook?
William Mosley (Executives)
Thanks, Karl. Yes, 2 years ago, I would have said neocloud is probably largely compute-based. But we're
starting to see that even some of the large neoclouds, they need a lot of data coming at them. And where
do they get that data in the past, they might have got that from traditional hyperscalers but there are
some places where neoclouds are saying, I need instances close to me.

By the way, I do not think that's necessarily competitive with the hyperscalers. I mean there are so
many different application-specific reasons for people to have an exabyte or 2 who is sitting around,
especially training, various types of training for applications.
So we are starting to have exactly the dialogues that you talked about. Everyone knows the hyperscaler
architectures and the efficiency of the hyperscaler architectures because they know that they want that
same efficiency. And in some cases, we're talking about systems level discussions with these customers.
In other cases, we're just talking about drives. They also -- since they're going to be running this gear
for a long time, they want to be on the cutting edge of technology transition. Sometimes that's hard
because of feature sets and they may not be as robust as some of the other people so they need help
with that, and it is a very complicated qualification space.
Operator (Operator)
The next question is from Amit Daryanani with Evercore.
Amit Daryanani (Analysts)
I guess, Dave, as you look at the LTAs and the visibility on exabyte demand that you have for '28 and
even calendar '29, can you meet all the exabyte demand that's out there in '28, '29 entirely through
areal density gains? And maybe just touch on how secure do you think your own upstream supply chain
is for specialized components, especially as HAMR start to scale up. I'd love to just kind of understand
the component side from your perspective. And Gianluca, I'd love to understand where you're going to
get to 80% gross margins, if you want to oblige and answer that.
William Mosley (Executives)
Thanks, Amit. So on the supply chain piece, working with our supply partners that have been through a
lot like we were a few years ago, as you know, we're making sure that everybody is kind of lined up and
it's well orchestrated. That's an important part of our supply chain. We cannot have people kind of
individually doing investments and then someone else not doing the investment and not be well-
orchestrated because that drives cost the wrong way.
How confident are we in demand long term? Very confident. I do think that there's a lot of people out
trying to understand all these new applications that are coming at us and saying, what does that mean
for the storage tier? I also think that there's well-tractioned applications already in the market, whether
they're pre-AI, which was huge, right, some of the video applications we've talked about before or
whether they're now AI enabled that are driving the storage tier even higher.
And so the forecasting, especially for some of those new applications is relatively harder. I think there's
a lot of optimism around it. But I also think that the existing data sphere, if you will, inside of these
cloud service providers is growing at a certain large clip anyway. I do not think that probably our areal
density transitions are going to be sufficient. But I do think that they are strong, and I think it allows
people to plan their businesses well, and that's one of the reasons we're having good conversations out
in that time frame.
Gianluca Romano (Executives)
On the gross margin, Amit, I would say our incremental gross margin has been very strong for the last
several quarters. Overall gross margin is improving sequentially very well. So we don't have a specific

target. We will continue to improve based on the business situation. And we know already that for the
rest of the fiscal year, we will have sequential improvement every quarter. And then we will see at a
certain point where we are, but we don't have a specific number that we are trying to achieve.
Operator (Operator)
The next question is from Steven Fox with Fox Advisors.
Steven Fox (Analysts)
I just wanted to ask a free cash flow question, if I could. So off of a 10-year high, like can you talk about,
I guess, the dynamics that drive from just a manufacturing standpoint, a higher free cash flow margin
in the future? Because as the areal density increases, the increases as a percentage are smaller. So I
don't know if that helps or, Dave, to your other point about passing through the same equipment makes
it more capital intensive, et cetera. And just as a follow-up to that, just can you maybe talk about where
-- remind us where you want to get debt levels to and when buybacks could start?
William Mosley (Executives)
Yes. Thanks, Steve. So we'll stay within our capital model. I mean we talked about 5% -- 4% to 6% of
revenue is our range for CapEx. The tools we're buying are modern tools, and we're refreshing part of
the fleet even with that 5% of CapEx -- 5% of revenue as CapEx, we're refreshing the fleet and doing
quite well with that.
So we'll turn all that into areal density, and that's what we're really excited about. I think relative to free
cash flow, from an OpEx perspective, we don't see the need to add a bunch of OpEx. We feel our team is
doing really well on all the innovation vectors, whether it's a servo-mechanical vector or it's a quantum
device vector in the recording fabs or lasers now or whatever. I mean, we think that the team is funded
well and doing well. And so we think we have visibility to continue areal density without raising CapEx
too much. So I think all of that translates into free cash flow that's growing like we talked about.
Gianluca Romano (Executives)
On the debt part, we ended our fiscal '26 with $3.6 billion in debt. That is already a huge reduction
from about $5 billion that we had at the beginning of the fiscal year. We will reduce debt even more
during the quarter. Actually, we have already done a good step in the month of July, but we will
probably end fiscal Q1 at $2.4 billion in debt. And we still have one note that has a fairly high interest
rate that I would like to address in the near future, maybe next quarter, maybe the following quarter.
But we are doing already more share buyback than what we have done in the prior quarter. So this
quarter, we are having -- we are executing a higher level of share buyback and we will continue in the
next several quarters.
Operator (Operator)
The next question is from Vijay Rakesh with Mizuho.
Vijay Rakesh (Analysts)
Congratulations, Dave and Gianluca. Just a couple -- two quick questions. One, when you look at the
hard disk drive, the nearline attach rate, is there a way to look at how the attach rate has changed on

the GPU ASIC side per rack with agentic AI or KV cache picking up? How is that trend looking this year
versus last year, let's say, when there was no agentic AI?
And Gianluca, on the margin side, should we expect margins to kind of get to the 60% plus? Or if you
can give us what the incremental margins are on HAMR 4 versus prior? Or is there a way to look at mix
of HAMR 4, I guess?
William Mosley (Executives)
I'll take the attach rate discussion. I know there are people out there in the world trying to model this,
and it's a noble effort, but I think it all comes down to application space. So there are certain
applications where you may need a lot more context and there are certain applications where maybe
you don't need as much. And so depending on the application pickup on this agentic AI, we talked
about KV cache in the prepared remarks. It could be a little. I think we're still trying to factor that in.
And that's some of the stuff that as we get into modeling '29 and '30 and beyond, I think we're going to
have to work steady with our customers to watch those applications carefully. Pretty excited about it.
And that's not the discussion about physical AI either. That's just on what I would call more enterprise
type applications.
Gianluca Romano (Executives)
Yes. On the margin, we -- last quarter, we were at almost 53%. We are guiding higher in September.
Our incremental gross margin is well above the 60% that you were indicating. So I'm not guiding for
the future, but the trend is, of course, to have a stronger and stronger gross margin. And we will see
what we will achieve in the next few quarters. But as you know, we are guiding something that is not too
far from that number already in September.
Operator (Operator)
The next question is from Ananda Baruah with Loop Capital.
Ananda Baruah (Analysts)
Dave, maybe just sort of dovetailing off your comments about application type. Is there easy way or a
simple way to think about currently, what you guys see as the more prominent applications driving
demand right now? And before you get to physical, maybe how you see those meaningful application
types manifesting over the next couple of years?
William Mosley (Executives)
Thanks, Ananda. Yes, the way I think about it, and I've been around for a long time, we know, so you
have to be careful with me. But if you're taking small blocks of text, whether it's forms that somebody
filled out or an ERP or something like that, in the -- and I say small blocks of text kind of jokingly
because that could still be terabytes worth of text. I think that's probably not what we're talking about.
But when you start to have a lot of unstructured data like video data or multiple sources of unstructured
data, sometimes it maybe sensor data, it may actually still be text, but it's just necessarily coming in
from all kinds of different sources. Those are the applications that I think are going to require a lot
more processing power, and you don't want to redo that processing power over and over again.

So this is happening in enterprises. It's not just happening in hyperscalers. It's happening at the
extreme edge as well. And I think these trends are very favorable for us before we ever get into
something like physical AI.
Operator (Operator)
This concludes our question-and-answer session. I would like to turn the conference back over to
management for any closing remarks.
William Mosley (Executives)
Thanks, Gary, and thanks, everyone, for joining us today. Fiscal 2026 was an outstanding year for
Seagate, reflecting strong execution by our global team and deep engagement with our customers. As
we move into fiscal 2027, we are well positioned to address the opportunities in front of us. We remain
focused on executing our technology road map, capturing profitable revenue growth and delivering
long-term value creation for all of our stakeholders. We look forward to updating our progress with you
in the quarters ahead.
Operator (Operator)
The conference has now concluded. Thank you for attending today's presentation. You may now
disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### STX_Q3_2026_Earnings_Call_20260428.md
- 2026-04-28｜CFO｜guidance：CFO 給 6 月季（FQ4）營收財測：34.5 億美元，上下 1 億美元。（原話："range of $3.45 billion, plus or minus $100 million"）
- 2026-04-28｜CFO｜guidance：CFO 給 6 月季 non-GAAP EPS 財測：5 美元，上下 0.20 美元。（原話："Non-GAAP EPS is expected to be $5 plus or minus $0.20"）
- 2026-04-28｜CFO｜guidance：CFO 給 6 月季 non-GAAP 營業費用約 2.95 億美元（上一季實際 2.96 億）。（原話："operating expenses are expected to be approximately $295"）
- 2026-04-28｜CFO｜guidance：CFO 以營收財測中點計，6 月季 non-GAAP 營業利益率的口徑是「lower 40% range」，未給確切數字。（原話："in the lower 40% range"）
- 2026-04-28｜CFO｜guidance：CFO 預期自由現金流在 2026 日曆年剩餘季度持續改善。（原話："free cash flow generation to improve further"）
- 2026-04-28｜CFO｜guidance：CFO 預期 6 月季其他收支（其他收入與費用）與本季大致持平。（原話："other income and expense to remain relatively flat"）
- 2026-04-28｜CEO｜guidance：CEO 把年營收成長長期目標，從原本低至中十位數百分比，調高為至少 20%（未給明確期限，只說未來幾年）。（原話："target from the low to mid-teens to a minimum of 20%"）
- 2026-04-28｜CEO｜guidance：CEO 表示公司績效已超前一年前分析師日所訂的財務目標。（原話："driving performance ahead of the financial targets"）
- 2026-04-28｜CEO｜guidance：CEO 總結中把公司定位為進入「結構性成長期」，這是本次新增的敘事框架。（原話："Seagate is entering a period of structural growth"）
- 2026-04-28｜CFO｜guidance：CFO 稱每噸（每 TB）資料中心營收的年增中個位數趨勢，預期會延續。（原話："We expect this trend to continue"）
- 2026-04-28｜CFO｜commitment：CFO 在準備稿結尾表示有信心在 FY2027 持續季增營收並擴張利潤率。（原話："growth and margin expansion through fiscal 2027"）
- 2026-04-28｜CFO｜commitment：CFO 在問答中把同一承諾說成「有很好的機會」讓利潤與營收在 FY27 逐季增加，措辭比準備稿的 confident in delivering 略軟。（原話："increase our profit and our revenue sequentially"）
- 2026-04-28｜CEO｜commitment：CEO 重申資料中心 exabyte 供給成長目標為 20% 中段。（原話："supply data center exabyte growth in the mid-20%"）
- 2026-04-28｜CEO｜commitment：CEO 說 Mozaic 5（50TB）研發按計畫進行，客戶驗證出貨目標是 2027 日曆年末。（原話："qualification shipments targeted for late calendar 2027"）
- 2026-04-28｜CFO｜commitment：CFO 在回答 Krish 時再確認 50TB 第三代 HAMR 在下一個日曆年年底進入驗證。（原話："the end of next calendar year, we will be already in qual"）
- 2026-04-28｜CFO｜commitment：CFO 澄清先前的百分比口徑：目標是 nearline exabyte 中 70% 建在 HAMR 硬碟上。（原話："we will achieve 70% of exabyte, nearline"）
- 2026-04-28｜CFO｜commitment：CFO 講 70% 目標的時點時當場自我更正，從 calendar '27 改口為 fiscal '27。（原話："by the end of calendar '27, actually by fiscal '27, sorry"）
- 2026-04-28｜CEO｜commitment：CEO 準備稿說正在與雲端客戶敲定涵蓋到 FY2027 年底的 build-to-order 合約。（原話："finalizing build-to-order contracts with these customers"）
- 2026-04-28｜CFO｜commitment：CFO 在問答中用完成式，說 FY27 的 build-to-order 已經敲定（準備稿是進行式 finalizing）。（原話："now finalized our build-to-order for our fiscal '27"）
- 2026-04-28｜CFO｜margin：CFO 報 3 月季 non-GAAP 毛利率 47%，較上一季增加 480 個基點。（原話："47%, up 480 basis points sequentially"）
- 2026-04-28｜CFO｜margin：CFO 報 non-GAAP 營業利益率較上一季擴張 560 個基點，至 37.5%。（原話："operating margin by 560 basis"）
- 2026-04-28｜CFO｜margin：CFO 說毛利率改善來自長期定價策略加產品組合，兩者帶動資料中心每 TB 營收年增中個位數。（原話："Together, this drove a mid-single-digit increase"）
- 2026-04-28｜CFO｜margin：CFO 報 non-GAAP 營業費用 2.96 億美元，占營收 9.5%。（原話："at $296 million or 9.5% of revenue"）
- 2026-04-28｜CFO｜margin：CFO 說營收成長加費用紀律，讓長期營業利益率目標比原訂時程提早達成。（原話："earlier than originally planned"）
- 2026-04-28｜CFO｜margin：CFO 拆解過去幾季成本下降兩大來源是高容量組合與產線滿載，並說未來產能已滿，滿載這一項不再是成本下降來源。（原話："now we are full, so that part maybe will not"）
- 2026-04-28｜CFO｜margin：CFO 說未來成本下降的主要驅動力是每台硬碟 TB 數提高，同時不增加物料清單。（原話："not adding more bill of materials to the hard disk"）
- 2026-04-28｜CFO｜margin：CFO 澄清 FY27 營業費用「持平」是指金額持平，不是占營收比率持平。（原話："flat on a dollar basis, not as a percentage of revenue"）
- 2026-04-28｜CFO｜margin：CFO 說相較一年前的規劃，定價表現更好，是毛利率優於預期的原因之一。（原話："I say pricing was actually better"）
- 2026-04-28｜CFO｜margin：CFO 被問到增量毛利率能否維持 70% 以上時，只說看不出未來不能重複過去幾季的表現，隨即補上每季不同。（原話："I don't see a reason why we should not do the same"）
- 2026-04-28｜CFO｜margin：CFO 說定價策略沒有改變，已連續 12 季利潤成長，且 FY27 趨勢相同。（原話："there are no changes to our pricing strategy"）
- 2026-04-28｜CFO｜margin：CFO 被問到 FY27 底每 exabyte 價格年增幅度時，表示不對這麼遠的時點給指引。（原話："we probably don't guide so far out in time"）
- 2026-04-28｜CFO｜margin：CFO 說利潤改善的大部分來自定價，其餘來自產品組合與 40TB HAMR 硬碟帶來的成本下降。（原話："profitability improvement is coming from pricing"）
- 2026-04-28｜CEO｜margin：CEO 回答定價問題時說，公司透過多出貨幾顆硬碟來測試需求，看到的是市場價格。（原話："we're seeing what the market price, if you will, is"）
- 2026-04-28｜CEO｜margin：CEO 談 FY27 定價時說，最終價格由客戶（需求）決定，公司持續與客戶談預見性。（原話："they'll determine what the price is"）
- 2026-04-28｜CFO｜margin：CFO 報資料中心營收成長快於 exabyte 出貨量（營收季增 12%、年增 55%；exabyte 季增 6%、年增 47%）。（原話："Data center revenue increased even faster"）
- 2026-04-28｜CFO｜capital_allocation：CFO 說 FY2026 資本支出預期落在占營收 4% 至 6% 的目標區間內，用於 HAMR 產品轉換與放量。（原話："2026 to be inside our target range of 4% to 6% of revenue"）
- 2026-04-28｜CFO｜capital_allocation：CFO 報自由現金流 9.53 億美元，較上一季增 57%。（原話："$953 million, up 57% from the prior quarter"）
- 2026-04-28｜CFO｜capital_allocation：CFO 報本季以股利與買回向股東回饋約 1.91 億美元。（原話："approximately $191 million to shareholders"）
- 2026-04-28｜CFO｜capital_allocation：CFO 報本季以現金清償 6.41 億美元債務，其中含 6 億以上 2028 年到期可交換債。（原話："$641 million in debt, including over $600 million"）
- 2026-04-28｜CFO｜capital_allocation：CFO 報淨槓桿比率降至 0.7 倍，並預期隨獲利與現金增加持續下降。（原話："Net leverage ratio improved to 0.7x"）
- 2026-04-28｜CFO｜capital_allocation：CFO 說 Fitch 最近把 Seagate 信用評等調升到投資等級。（原話："upgraded Seagate's credit to investment grade"）
- 2026-04-28｜CFO｜capital_allocation：CFO 說仍有約 4 億美元可轉換債未處理，預計本季或下季處理。（原話："We still have about $400 million of the convertible"）
- 2026-04-28｜CFO｜capital_allocation：CFO 說少量還債之後，現金大部分會用於股票買回，且目前已在市場上買。（原話："majority will probably go to share buybacks"）
- 2026-04-28｜CEO｜capital_allocation：CEO 說下一步資金去向是回到先前的做法，也就是回饋股東。（原話："which is returning value to shareholders"）
- 2026-04-28｜CEO｜capital_allocation：CEO 回顧去年的資金重心在營運資金與供應鏈修復，之後才轉向還債與股東回饋。（原話："last year we were focused very much on working capital"）
- 2026-04-28｜CFO｜capital_allocation：CFO 被問到客戶預付款時說目前沒有把重心放在預付款，但也沒有排除未來實施。（原話："so far, we have not focused on that part"）
- 2026-04-28｜CEO｜capital_allocation：CEO 說若把人力從提升面密度轉去多做零件，未來幾年淨出貨的 exabyte 反而會更少，所以不以增加產能單位為路線。（原話："we would probably net-net fewer exabytes"）
- 2026-04-28｜CEO｜customer：CEO 說已有 2 家全球最大 CSP 通過 4TB 以上每碟片產品驗證。（原話："2 of the world's largest CSPs now qualified on our 4+"）
- 2026-04-28｜CFO｜customer：CFO 報 3 月季已對 75% 的主要全球雲端客戶出貨 Mozaic 硬碟並認列營收。（原話："75% of the leading global cloud customers"）
- 2026-04-28｜CFO｜customer：CFO 說剩下 2 家雲端客戶的驗證預計在本季（FQ4）完成。（原話："remaining 2 customers in the current quarter"）
- 2026-04-28｜CEO｜customer：CEO 說來自雲端客戶的營收已連續第 10 季成長。（原話："our 10th consecutive period of revenue growth"）
- 2026-04-28｜CEO｜customer：CEO 以剩餘履約義務（RPO）作為未來營收潛力代理指標，稱前三大 CSP 的 RPO 已近乎翻倍至 1.1 兆美元。（原話："nearly doubled their RPO to a staggering $1.1 trillion"）
- 2026-04-28｜CEO｜customer：CEO 說與幾乎所有大型雲端客戶簽有 exabyte 級供給協議，nearline 產能到 2027 日曆年幾乎全數分配完畢。（原話："capacity almost fully allocated through calendar 2027"）
- 2026-04-28｜CEO｜customer：CEO 說與客戶的策略規劃討論已延伸到 2028 日曆年及以後。（原話："planning discussions now reaching into calendar 2028"）
- 2026-04-28｜CEO｜customer：CEO 說開始看到主權（sovereign）與 neocloud 資料中心對企業級 nearline 硬碟與系統方案有興趣。（原話："interest from sovereign and neocloud data centers"）
- 2026-04-28｜CFO｜customer：CFO 說企業 OEM 資料中心市場營收季增明顯，原因是 AI 應用部署與混合／分層儲存架構需求回升。（原話："we saw a notable sequential revenue increase"）
- 2026-04-28｜CFO｜customer：CFO 說用戶端與消費市場，供給偏緊與 NAND 成本上升，抵銷了 3 月季的典型季節性需求走弱。（原話："tight supply and higher NAND cost offset the typical"）
- 2026-04-28｜CFO｜customer：CFO 被問到 FY27 產能有多少已鎖價時，只答 nearline 產能「絕大部分」已分配，沒有給比例。（原話："the vast majority of our nearline capacity is allocated"）
- 2026-04-28｜CEO｜product：CEO 說 Mozaic 4 單碟最高可達 44TB，較第一代 Mozaic 多 30% 以上容量。（原話："can deliver up to 44 terabytes per drive"）
- 2026-04-28｜CEO｜product：CEO 說 Mozaic 4 於 3 月下旬開始有營收出貨。（原話："revenue shipments for Mozaic 4 in late March"）
- 2026-04-28｜CEO｜product：CEO 預期到 2026 日曆年底，Mozaic 4 會占 HAMR exabyte 出貨的多數。（原話："HAMR exabyte shipments exiting calendar 2026"）
- 2026-04-28｜CEO｜product：CEO 說技術策略以面密度創新優先於增加出貨單位數。（原話："areal density innovation over increasing unit volumes"）
- 2026-04-28｜CEO｜product：CEO 說目前絕大多數 HAMR 供給都分配給雲端與超大規模客戶，並預期放量後才會把 4／5TB 每碟片技術用到較低容量產品。（原話："the vast majority of HAMR supply is allocated to cloud"）
- 2026-04-28｜CEO｜product：CEO 說公司刻意控制 Mozaic 4 的投入比重，因為其他產品家族仍對部分客戶重要且表現不差。（原話："We're not leaning too hard into the Mozaic 4"）
- 2026-04-28｜CEO｜product：CEO 回答用 HAMR 做 20TB 低容量款時說，Mozaic 4 高階需求太高，預期不會看到很多這類產品。（原話："I don't think you'll see very many of those"）
- 2026-04-28｜CFO｜product：CFO 說公共雲需求太強，沒有足夠產量再往低容量 4TB 每碟片策略延伸，可能較晚才處理。（原話："possibly, we will address it a bit later out in time"）
- 2026-04-28｜CEO｜product：CEO 談效能分層需求時說，過去出貨過數千萬 exabyte 級的堆疊式 actuator 設計，可以重新拿出來用。（原話："certainly pull those designs back down off the shelf"）
- 2026-04-28｜CEO｜product：CEO 回答 agentic AI 提問時說，部分 AI 應用屬於資料量很小的應用。（原話："are fairly small data applications"）
- 2026-04-28｜CEO｜product：CEO 說 agentic AI 帶來的儲存需求並非全部與大容量儲存相關，但已開始看到明顯增加。（原話："not entirely related to mass capacity storage"）
- 2026-04-28｜CEO｜product：CEO 回答 Tim Arcuri 時說，出貨顆數沒有成長，只有每顆平均磁頭數可能增加。（原話："The total number of units is not really increasing"）
- 2026-04-28｜CEO｜competition：CEO 談硬碟與 NAND 的成本差時說，因目前的經濟性，客戶正在回頭找硬碟。（原話："people are coming back to hard drives"）
- 2026-04-28｜CEO｜competition：CEO 認為資料中心儲存架構在未來很長一段時間內都很難改變。（原話："these architectures pretty sticky for a long, long time"）
- 2026-04-28｜CFO｜risk：CFO 說 HAMR 週期時間比 PMR 長，因此仍用一些 PMR 磁頭維持出貨顆數，否則顆數會下降。（原話："Otherwise, the units will actually go down"）
- 2026-04-28｜CFO｜risk：CFO 談中東衝突等地緣政治緊張時，表示目前預期不會對業務造成重大影響。（原話："do not currently expect material impacts"）

### STX_Citi_s_2026_Global_TMT_Conference_20260909.md
- 2026-09-09｜CFO｜guidance：CFO 說依現有 PO，整個 FY27 營收與獲利都會改善（原話："we see improvement also for the entire fiscal '27"）
- 2026-09-09｜CFO｜guidance：CFO 重述本財年每一季營收與獲利都會比前一季改善（原話："see an improvement in both revenue and profitability"）
- 2026-09-09｜CFO｜guidance：CFO 說 exabyte 目標是未來 2–3 年年複合成長至少 25%（原話："targeting that at least 25% CAGR in the next 2 or 3 years"）
- 2026-09-09｜CFO｜guidance：CFO 提到 9 月季財測給的是營收與獲利都大幅增加（原話："very significant increase in revenue and in profitability"）
- 2026-09-09｜CFO｜guidance：CFO 說本財年 OpEx 財測為每季約 3 億美元，大致持平（原話："OpEx fairly stable at around $300 million per quarter"）
- 2026-09-09｜CFO｜guidance：談完 OpEx 後，CFO 說未來 3–4 季看不到需要改變的理由（原話："next 3, 4 quarters, we don't see any reason for change"）
- 2026-09-09｜CFO｜guidance：CFO 說人力（headcount）會維持相當穩定（原話："we will be fairly stable in terms of headcount"）
- 2026-09-09｜CFO｜guidance：CFO 說供需缺口沒有縮小，反而略為擴大（原話："gap between supply/demand is not decreasing"）
- 2026-09-09｜CFO｜guidance：CFO 說需求成長速度比公司原先預期還快（原話："demand growing even faster than what we were thinking"）
- 2026-09-09｜CFO｜commitment：CFO 說手上有未來 4–5 季的採購訂單（PO）（原話："purchase orders in place for the next 4 or 5 quarters"）
- 2026-09-09｜CFO｜commitment：CFO 說已有涵蓋未來 2–3 年的長約（LTA）（原話："We have LTAs in place for the next 2, 3 years"）
- 2026-09-09｜CFO｜commitment：CFO 說長約配置不會超過確定能生產的量，彈性不大（原話："we don't allocate more than what we are sure we can produce"）
- 2026-09-09｜CFO｜commitment：CFO 回答分析師：長約條款沒有加入很多彈性（原話："No, not a lot of flexibility."）
- 2026-09-09｜CFO｜commitment：CFO 說 50TB 新一代硬碟約一年後開始認證（qual）（原話："we will start to qualify about in a year from now"）
- 2026-09-09｜CFO｜commitment：CFO 說第三代 HAMR 幾季後開始認證（原話："third-generation HAMR qual in just a few quarters from now"）
- 2026-09-09｜CFO｜commitment：CFO 說靠技術（單顆容量）成長，而非靠增加出貨顆數（原話："growing the content of the drive, not the units"）
- 2026-09-09｜CFO｜commitment：CFO 說 HAMR 讓公司不必增加顆數就能成長（原話："we can grow without the need to increase the units"）
- 2026-09-09｜CFO｜commitment：CFO 說擴產與零組件增加都放在 CapEx 佔營收 4%–6% 的區間內（原話："Everything in our CapEx range, so between 4% and 6%"）
- 2026-09-09｜CFO｜commitment：CFO 說 3–4 年後需要的容量會遠高於 50TB，公司只承諾做得到的量（原話："a capacity that is way higher than 50 terabytes"）
- 2026-09-09｜CFO｜margin：CFO 說漲價是每個客戶區段都有，不只企業 OEM（原話："it's in every segment"）
- 2026-09-09｜CFO｜margin：CFO 說調價方式不會過度激進，目的是讓逐季改善能持續很久（原話："we do this in a way that is not super aggressive"）
- 2026-09-09｜CFO｜margin：CFO 說前一季價格與成本表現都好，價格貢獻可能更大（原話："maybe even more on pricing than cost"）
- 2026-09-09｜CFO｜margin：CFO 說本季有一批高量新合約，帶來價格支撐（原話："we have a good level of new contracts with high volume"）
- 2026-09-09｜CFO｜margin：CFO 談價格空間：認為未來可得到與過去類似的結果（原話："no reason why we should not get a similar result"）
- 2026-09-09｜CFO｜margin：CFO 說 Seagate 佔客戶 CapEx 比重不大，漲價不會明顯影響客戶支出（原話："we are not a big part of our customer CapEx"）
- 2026-09-09｜CFO｜margin：CFO 總結各季雖有變數，但結果是營收與獲利都上升（原話："Revenue will go up and profitability will go up."）
- 2026-09-09｜CFO｜margin：CFO 說自製的磁頭與碟片，單位成本不隨容量變動（原話："the unit cost actually is not changing"）
- 2026-09-09｜CFO｜margin：CFO 說自製部分每 TB 成本降幅很好，但沒給數字（原話："a very good cost per terabyte decline on what we produce"）
- 2026-09-09｜CFO｜margin：CFO 說外購零組件的成本變化每年不同、公司較難控制（原話："it's less under our control"）
- 2026-09-09｜CFO｜margin：CFO 說換代轉換成本是正常現象，一直都有（原話："I would say it's normal for the business"）
- 2026-09-09｜CFO｜product：CFO 說 30TB 升到 40TB 容量增加 33%（原話："you increase 33% your capacity"）
- 2026-09-09｜CFO｜product：CFO 說 40TB 升到 50TB 再增加 25%（原話："Then going from 40 to 50 is another 25%."）
- 2026-09-09｜CFO｜product：CFO 說 HAMR 只用在高容量端，2TB 到 28TB 基本上是 PMR（原話："Between 2 terabytes and 28 is basically PMR."）
- 2026-09-09｜CFO｜product：CFO 說 PMR 產品要加容量就得多加碟片與磁頭（原話："you need to have 1 more disk and 2 more heads"）
- 2026-09-09｜CFO｜product：CFO 說 HAMR 加碟片（10 片到 11 片）只增加約 10%，目前不划算（原話："If you go from 10 disks to 11 disks, you only gain 10%."）
- 2026-09-09｜CFO｜product：CFO 說第二代 HAMR 客戶認證進行得很快（原話："Second generation is going very, very fast."）
- 2026-09-09｜CFO｜product：CFO 說客戶現在把第二代 HAMR 當成已熟悉技術上的新產品（原話："it's just a new product on something that they already know"）
- 2026-09-09｜CFO｜product：CFO 說第一代 HAMR 認證較困難，客戶測試時間也較長（原話："the first-generation HAMR was a little bit more difficult"）
- 2026-09-09｜CFO｜product：CFO 說 HAMR 換代時 exabyte 出貨會有較大的季度波動，年複合仍約 25%（原話："a little bit more variability on exabyte volume"）
- 2026-09-09｜CFO｜product：CFO 說 HAMR 磁頭製程週期較長，需要多一點空間（原話："we need a little bit more space"）
- 2026-09-09｜CFO｜product：CFO 說顆數不變、exabyte 約增加 25%（原話："the same number of units, but about 25% more exabytes"）
- 2026-09-09｜CFO｜product：CFO 談 KV cache：只有部分層級與 NAND 有少量重疊，硬碟可以參與（原話："a little bit of overlap between NAND and our disk"）
- 2026-09-09｜CFO｜product：CFO 說參與 KV cache 不需要與快閃記憶體廠合作（原話："I don't think we need to partner with flash"）
- 2026-09-09｜CFO｜competition：CFO 說資料中心裡硬碟沒有替代品（原話："no replacement in data center for our disk storage"）
- 2026-09-09｜CFO｜competition：CFO 說公司想維持供需平衡，認為目前情況有助逐季改善（原話："we want to keep a good balance between supply and demand"）
- 2026-09-09｜CFO｜risk：被問到這次循環有何不同，CFO 承認現在不是循環的起點，已超過 3 年（原話："not for sure the beginning of the cycle"）
- 2026-09-09｜CFO｜risk：被問到未來 2–3 年是否需要消化已部署容量，CFO 說目前沒看到趨勢改變（原話："we don't see today any change in the trend"）
- 2026-09-09｜CFO｜risk：CFO 說有長約且客戶要求更多量，所以不認為是短期循環（原話："we feel comfortable that it's not a short-term cycle"）
- 2026-09-09｜CFO｜risk：CFO 說每一季受量、新合約、去年基期等多個變數影響，各季不同（原話："every quarter is different, there are a lot of variables"）
- 2026-09-09｜CFO｜risk：CFO 說外購零組件有的年度上升、有的下降，是好壞參半（原話："a mixed bag, some components are increasing"）
- 2026-09-09｜CFO｜customer：CFO 說公有雲買最高容量的硬碟（原話："Public clouds buy the highest-capacity drive."）
- 2026-09-09｜CFO｜customer：CFO 說企業 OEM（地端資料中心）需求又開始成長（原話："more on-prem data center demand, to start to grow again"）
- 2026-09-09｜CFO｜customer：CFO 說地端資料中心約 2 年後才會用到 40TB 硬碟（原話："on-prem data center will consume a 40-terabyte drive"）
- 2026-09-09｜CFO｜customer：CFO 說 40TB 產品還有其他客戶即將完成認證（原話："other customers that will be qualified fairly soon"）
- 2026-09-09｜CFO｜customer：CFO 說每次重談長約，客戶都要求更多量而不是更少（原話："our customers are asking for more volume, not less volume"）
- 2026-09-09｜CFO｜customer：CFO 說主權 AI 資料中心目前仍由同一批大型公有雲業者建置（原話："they're still built by the same big public cloud companies"）
- 2026-09-09｜CFO｜customer：CFO 說 neocloud 與 Seagate 客戶相同：Seagate 賣儲存、neocloud 賣算力（原話："We sell storage, they sell compute"）
- 2026-09-09｜CFO｜customer：CFO 說未來部分目前賣給公有雲的量會轉到 neocloud（原話："Tomorrow, some of that volume will go to the neoclouds."）
- 2026-09-09｜CFO｜customer：CFO 說量體變化不大，但對客戶分散度是好事（原話："it's good from a customer diversification"）
- 2026-09-09｜CFO｜customer：CFO 說最被低估的成長來源是所有和影像相關的應用（機器人、自駕等）（原話："everything that is based on video"）
- 2026-09-09｜CFO｜capital_allocation：CFO 說債務處理接近完成（原話："in terms of debt, we are almost done"）
- 2026-09-09｜CFO｜capital_allocation：CFO 說還剩一筆高利率票據，可能下一季處理（原話："one note with high interest rate that we want to address"）
- 2026-09-09｜CFO｜capital_allocation：CFO 說債務處理完後，回到更多股票回購並維持股息（原話："so higher share buyback and still focusing on a good return"）
- 2026-09-09｜CFO｜capital_allocation：CFO 說前一季自由現金流為 11 億美元，高於 10 億（原話："was already above the $1 billion, was $1.1 billion"）
- 2026-09-09｜CFO｜capital_allocation：被問自由現金流率目標，CFO 說沒有公布目標（原話："We didn't share a target."）
- 2026-09-09｜CFO｜capital_allocation：CFO 說本季與下季持續回購，之後可能做得更多（原話："after that, we will probably do even more"）

### STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說依手上訂單，本財年每一季營收和毛利率都比前一季高（原句同時提 higher margin）。（原話："every quarter of this fiscal year having higher revenue"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說未來 4 到 5 季已有客戶訂單在手，依這些訂單營收上升、獲利改善。（原話："purchase orders in place for the next 4 or 5 quarters"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說近幾季增量毛利率遠高於先前的 50% 框架，落在 70% 以上。（原話："I would say, in the 70-plus percent"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說未來幾季用 70% 以上的增量毛利率看這門生意是合適的（回答分析師對新增量框架的提問）。（原話："So for the next few quarters, I think that is a good way"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說過去 3 年的定價策略加上技術帶來的 exabyte 成長，讓毛利率幾乎變成三倍。（原話："allow us to almost triple our gross margin"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說希捷的產品佔客戶資本支出的比重是低到中個位數。（原話："Now we are low to middle single digit of their CapEx."）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說需求比去年投資人日時看到的強很多。（原話："Demand is much, much stronger than what we were seeing"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說需求強讓公司能把價格調得比投資人日討論的還高一些，帶動毛利率、營業利益率與 EPS 更好。（原話："raise pricing a little bit more than what we were"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說自己認為未來數季業績會持續改善（未給數字）。（原話："results continue to improve in the next several quarters"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說自投資人日以來情況持續轉好。（原話："the situation from our Investor Day has continued to improve"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說 40TB HAMR 硬碟已在賣給兩家最大的超大規模雲端客戶，另有幾家還在驗證。（原話："we're already selling to the 2 biggest hyperscalers"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說下一代 50TB 產品的量會落在 2027 曆年（原句：through the end of calendar year '27）。（原話："50 terabyte will be more calendar '27"）
- 2026-09-10｜Gianluca Romano (CFO)｜commitment：分析師問 HAMR 出貨量交叉（超越 PMR）是否有變，CFO 答計畫穩固，12 月前 40TB 與整體 HAMR 都會到那個水準。（原話："I think by December, so just a few months from now"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說約兩年後，希捷資料中心產品有八到九成的量會走 HAMR。（原話："80%, 90% of the volume will be sold through HAMR"）
- 2026-09-10｜Gianluca Romano (CFO)｜competition：CFO 說傳統 PMR 技術追不上 HAMR（沒點名競爭對手，談的是技術路線）。（原話："no way that the PMR technology can keep up with HAMR"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 舉例：從 30TB 換到 40TB 硬碟，單顆內容量多 33%。（原話："a 40-terabyte drive, we can have 33% more content"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說 40TB 硬碟正在美國與亞洲的多家客戶驗證中。（原話："a good number of customers, both in U.S. and in Asia"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說 30TB HAMR 硬碟大約一年內就驗證完前 8 到 10 大客戶。（原話："we qualified the top 8, 10 customers in basically a year"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說所有大客戶都已經在買 HAMR。（原話："all the big customers are already buying HAMR, everyone"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說客戶每季買進的 HAMR 硬碟是數十萬顆等級。（原話："all buying hundreds of thousands of units every quarter"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 定調：HAMR 現在對希捷是產品開發，不再是技術開發（與客戶討論的重點已是單顆容量）。（原話："It's not anymore a real technology development"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說自製雷射搭配磁頭的成本，比外購雷射再組裝低很多。（原話："produce the laser together with the head is much lower"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說第二代 HAMR 起開始混用：部分產品用自家雷射，部分仍用外購雷射（第一代全用外購）。（原話："Some are still using external laser"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說未來自家雷射的占比會愈來愈高。（原話："more the mix will go into the internal laser"）
- 2026-09-10｜Gianluca Romano (CFO)｜risk：分析師問需求過熱後客戶砍單的下行情境，CFO 答目前看不到這種情況。（原話："Today, we don't see that situation happening."）
- 2026-09-10｜Gianluca Romano (CFO)｜risk：CFO 列舉客戶即使需求很高也可能放慢建資料中心的原因：電力限制、建照延誤、零組件缺料。（原話："a power constraint, can be a delay in building permit"）
- 2026-09-10｜Gianluca Romano (CFO)｜risk：CFO 說客戶若放慢建設，需求只是往後延，沒有消失。（原話："pushing that demand out in time is not going away"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說產業對資本支出與產能增加要保持紀律，希捷 2、3 年來一直如此。（原話："disciplined with CapEx and with capacity addition"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說成長來自技術升級（每顆內容更多），不是出貨顆數增加。（原話："growing because of technology, not because of more units"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 的數字口徑：這個產業賣的是 exabyte，不是顆數。（原話："this industry is selling exabytes, not units"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 的數字口徑：看 exabyte 成長時，他更看重絕對數字而不是百分比。（原話："I always look more at the absolute numbers and percentages"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 舉例：今年比 3 年前成長 25% 或 30%，換算成 exabyte 數量可能是 50% 以上，所以看營收要看賣出的 exabyte 與單價。（原話："that is maybe 50-plus percent if you look at the number"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：分析師問長期 exabyte 成長目標是否仍是 20%，CFO 提到先前給過約 3、4 年的 mid-20% CAGR，並說每季每年都不同。（原話："We gave this mid-20% CAGR for a fairly long period of time"）
- 2026-09-10｜Gianluca Romano (CFO)｜commitment：CFO 說公司有能力靠技術維持很好的 exabyte 年複合成長（未給數字）。（原話："grow through technology at a very good exabyte CAGR"）
- 2026-09-10｜Gianluca Romano (CFO)｜commitment：CFO 說目前沒有理由改變現行的技術加定價策略。（原話："we don't see any reason today to change it"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說漲價是策略的一部分，對毛利率與營業利益率貢獻很大。（原話："huge contribution to our gross margin and operating margin"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 給定價策略有效的第一個原因：供需平衡和 4、5 年前不同。（原話："the supply-demand balance is different"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說客戶把資料存起來的成本，比日後重新運算那份資料低很多。（原話："the cost of storage is minimal comparing to recompute"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說資料中心占營收 80%（大容量硬碟），其餘 20% 是低容量的 edge（消費、用戶端、部分影像監控）。（原話："This is today 80% of our revenue."）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說 edge 低容量市場因為沒有長期訂單與大客戶，近幾季已調整定價策略。（原話："we have changed a little bit our pricing strategy there"）
- 2026-09-10｜Gianluca Romano (CFO)｜competition：CFO 說目前 NAND 價格偏高，讓低容量硬碟有機會漲價並維持出貨量（低容量段硬碟與 SSD 有重疊）。（原話："Today, the NAND price is fairly high"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說各個區隔的需求都大於供給，所以要配貨，優先給資料中心大客戶。（原話："demand is above supply in every segment today"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說從客戶資本支出看，AI 投資仍在前段階段。（原話："still being in the first part of the phase of AI investment"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說近來除大型公有雲外，企業自建機房（on-prem）需求也有不錯成長，企業 OEM 通路也成長。（原話："a fairly good growth on enterprise OEM"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說本季後還剩一筆高利率票據想買回，可能下一季處理。（原話："still have one note that I would like to repurchase"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說 2027 曆年起庫藏股規模會更高（債務還清後自由現金流更多）。（原話："calendar year '27, I would say you will see a higher level"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說股利每年約 10、11 月與 CEO 內部檢討，這種強勁時期通常會加股利。（原話："we will probably increase the dividend"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說股東回報中股利只是一部分，庫藏股占大得多。（原話："A much bigger part will be share buyback."）

### 問答異常語氣（迴避／改口／保留）
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Erik Woodring（Morgan Stanley）：agentic AI 具體如何帶動硬碟需求，並且是否改變對 nearline exabyte 20% 中段年複合成長率的看法？｜答法：CEO 只描述 agentic 工作流參照大型資料集並產生新資料，並加註部分應用資料量小、「not entirely related to mass capacity storage」，沒有回答 CAGR 是否調整。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Wamsi Mohan（BofA）：FY27 產能有多少比例已鎖價、多少仍浮動？｜答法：CFO 答的是產能「已分配」（vast majority、not 100%、very high percentage），沒有給鎖價比例，也沒有區分已分配與已鎖價。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Samik Chatterjee（JPMorgan）：新合約進入損益後，為何定價不會加速上升？｜答法：CEO 轉向談需求上升與提供客戶可預測性，CFO 重申定價策略不變、FY27 有機會逐季增加，兩人都沒有正面回答加速與否。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Mark Newman（Bernstein）：每 exabyte 價格季增中個位數，是新合約占比較高，還是新合約漲幅擴大？此幅度是否每季延續？｜答法：CFO 答「策略不變、每季不同、取決於新合約數與產品組合」，說未來 4 季趨勢相同且可能更久，沒有區分兩種原因，也沒有給幅度。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Jim Schneider（Goldman）：FY27 底的長期訂單，每 exabyte 價格年增是低、中還是高個位數？｜答法：CFO 明確表示不對這麼遠的時點給指引，只說每季會略好，利潤改善主要來自定價、組合與 40TB HAMR 成本下降；CEO 補充最終由需求決定價格。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Amit Daryanani（Evercore）：分析師日的 50% 增量毛利率已被 70% 以上超越，FY27 模型是否用 70% 增量毛利率當框架？｜答法：CEO 先請 CFO 談量化，CFO 沒給數字，只說過去執行優於預期、看不出未來不能重複，並加上「每季不同，let's see」。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Karl Ackerman（BNP Paribas）：HAMR 多快會超過總 exabyte 出貨的一半？｜答法：CFO 沒回答何時過半，改為重述並更正先前說過的百分比（70% nearline exabyte 建在 HAMR 上，講到一半把 calendar '27 改為 fiscal '27），CEO 補說產線相對滿載、不會過度押 Mozaic 4。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Ananda Baruah（Loop Capital）：Mozaic 4 是否為切入 20TB 低容量 HAMR 的機型，何時可能做？｜答法：與準備稿說預期把 4／5TB 每碟片用於較低容量產品相比，問答中 CEO 說不預期看到很多、CFO 說產量不夠並可能較晚才處理，時程未定。
- STX_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：第二代 HAMR 良率提升後，每 TB 成本下降幅度該怎麼看？｜答法：回答 'It's very good'，拆成自製（磁頭、碟片）與外購兩類，沒有給任何降幅數字；外購部分只說每年不同、較難控制
- STX_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：40TB 換到 50TB 時的製造無效率（送認證品不能認列營收等）該怎麼看？｜答法：回答換代成本是正常現象、一直都有，沒有量化；轉向說 exabyte 季度波動會變大
- STX_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：HDD 相對 NAND 還有多少價格彈性？｜答法：沒有給價格幅度或上限，回答改談供需缺口略增、調價不會過度激進，並說未來可得到與過去類似的結果
- STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：上一季 price per exabyte 年增 11%，這個數字能否當作本財年建模的參考、未來幾季定價成長節奏如何？｜答法：CFO 沒給任何數字或節奏，改談定價策略 3 年前改變、供需平衡不同、資料價值較高等原因。
- STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：公司剛上調長期營收展望，這個目標能維持多久、可持續性如何？｜答法：CFO 沒給期間或數字，只說看不出趨勢會改變、未來數季業績會繼續改善。
- STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：長期 exabyte 成長目標 20% 是否仍正確，還是可持續超越？｜答法：CFO 沒有確認或修改 20%，改說先前給的是約 3、4 年的 mid-20% CAGR，並強調每季每年不同、應看絕對數字。
- STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：有沒有辦法用絕對 exabyte 數字來表達產業成長？｜答法：CFO 先答 No，只給一個百分比對絕對量的舉例，沒有提供絕對 exabyte 數字。

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
{"date":"20260729","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 近線儲存需求為結構性而非週期性，且合約化程度足以把可預測期拉到 2028-2029"},{"id":"H2","text":"HAMR／Mosaic 的面密度領先，讓 STX 在機櫃數持平下持續擴 exabyte 並取得定價權"},{"id":"H3","text":"市場願意給這門「合約化的循環商品生意」高於歷史中樞的倍數（16-18x 前瞻以上）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"中國稀土出口管制打到硬碟音圈馬達的 NdFeB 永磁——含鏑／鋱重稀土的釹鐵硼永磁驅動硬碟讀寫臂，自 2025 年起納入中國非自動出口許可制，核准延遲普遍 60-120 天以上，ex-China 重稀土瓶頸預期延續至 2027；域外「0.1% 規則」暫緩期於 2026-11-10 屆滿，第三國產品只要含 0.1% 中國源稀土即受管。這是雙面刃：既支撐定價，也威脅交期與毛利。"},{"id":"R2","text":"供給端追上：WD HAMR 2027 量產 ＋ Toshiba 40TB 級 ＋ 新產能投產，使定價權見頂——WD HAMR 已在兩家超大規模客戶認證中、2027 年量產爬坡（36TB CMR／40TB SMR／44TB UltraSMR），12 碟平台 2028 年到 60TB；Toshiba 市佔穩定 17%，2026 年 4 月起出貨 M12（30-34TB）、2027 年瞄準 40TB 級。同時 hyperscaler 需求端若進入 AI capex 消化期，缺口收斂會更快。"},{"id":"R3","text":"QLC 固態硬碟總持有成本交叉 × STX 自身漲價的負回饋迴路——QLC 在熱／溫資料層已於總持有成本勝出，業界預期 QLC 位元產出 2027 年超越 TLC；Meta 目標 2026 年底至 2027 年初部署 10-12EB QLC flash（效果為「限制硬碟成長率、尚未逆轉需求」）。關鍵在於：業界目標定價 $25-30/TB（現行 $14.30-14.90/TB）會直接壓縮硬碟對 flash 的每 TB 價差，定價權主張越強，越可能加速溫資料層遷移。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"$505-630（16-18x FY2027 指引隱含 EPS ~$34，即前份 $400-500 門檻按 EPS 基數 +26% 平移）；或循環位置由中轉早","irr_base_pct":-3.5,"ev5y_pct":-6.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.1,"ev5y_pct":-6.3,"irr_base_pct":-3.5,"max_dd_pct":-75.0,"bull_5y_price":1200.0,"bear_5y_price":144.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"$505-630（16-18x FY2027 指引隱含 EPS ~$34，即前份 $400-500 門檻按 EPS 基數 +26% 平移）；或循環位置由中轉早","price_at_dd":747.3,"archetype":"循環/商品","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20260923/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
