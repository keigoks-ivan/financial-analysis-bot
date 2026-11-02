你是 stock-analyst **v20 判斷 agent**，標的 CDNS（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CDNS","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":1584.451,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$M（YoY +24.2%，QoQ +7.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release；YoY／QoQ 由 Q2 2025 $1,275.441M、Q1 2026 $1,474.22M（H1 $3,058.671M 減 Q2）自算"},"note":"共識 $1.577B（媒體報導，Benzinga／Yahoo 引述，非 IR）；公司自家 Q2 指引 $1.555–1.595B，落在區間內偏上"},{"id":"f_kpi1_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":45.5,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release（Q2 2025 為 42.8%）"},"note":"公司自家 Q2 指引 44.5–45.5%，落在區間上緣；第三方共識值未取得"},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":28.4,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"%（營業利益 $450.3M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release／8-K Ex99.1（Q2 2025 為 19.0%、營業利益 $241.8M）"},"note":"公司自家 Q2 指引 28.5–29.5%，實際略低於區間下緣 0.1pt；新聞稿調節表列併購／整合成本占營收 2.1%；第三方共識值未取得"},{"id":"f_kpi5_non_gaap_diluted_eps","label":"Non-GAAP diluted EPS","value":2.11,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$（GAAP EPS $1.33）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release"},"note":"共識 $2.06（媒體報導，非 IR）；公司自家 Q2 指引 $2.02–2.08，高出上緣 $0.03"},{"id":"f_kpi6_backlog","label":"Backlog（在手訂單）","value":8.1,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$B（創新高）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release"},"note":"無共識值可比"},{"id":"f_kpi7_rpo_12_crpo","label":"RPO 未來 12 個月內認列（cRPO）","value":4.2,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release"},"note":"無共識值可比"},{"id":"f_kpi8_guidance_q3_fy2026","label":"Guidance — Q3 FY2026","value":"營收 $1,595–1,625M（YoY +19–21%）；non-GAAP 營業利益率 43.5–44.5%；GAAP 營業利益率 27.5–28.5%；non-GAAP EPS $2.01–2.07；GAAP EPS $1.11–1.17；預計回購約 $200M","period":"Q2 FY2026 財報（公告於 2026-07-27）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2026 財報（公告於 2026-07-27）","citation":"公司 CFO commentary（8-K Ex99.2，2026-07-27）＋新聞稿 investor.cadence.com Q2 2026 press release"},"note":"Q3 共識值未取得；註：指引中點營收 $1.61B 較 Q2 僅 +1.6% QoQ，non-GAAP 營業利益率中點 44.0% 低於 Q2 實績 45.5%"},{"id":"f_kpi9_guidance_fy2026","label":"Guidance — FY2026（本次調升）","value":"營收 $6.26–6.34B（YoY +18–20%）；non-GAAP 營業利益率 43.75–44.75%；GAAP 營業利益率 27.75–28.75%；non-GAAP EPS $8.05–8.15；GAAP EPS $4.76–4.86；營運現金流約 $2.0B；non-GAAP／GAAP 稅率約 16.5%／26%；回購約占 FCF 50%","period":"Q2 FY2026 財報（公告於 2026-07-27）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q2 FY2026 財報（公告於 2026-07-27）","citation":"公司 CFO commentary（8-K Ex99.2，2026-07-27）＋新聞稿 investor.cadence.com Q2 2026 press release"},"note":"2026-09-19 共識 FY2026 non-GAAP EPS $8.14（dd_numbers_extra.py consensus_revision），落在指引區間上緣；此為財報後共識，非財報前預期"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-26","period":"2026-10-26","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-26"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cdns_gross_margin_pct","label":"CDNS 毛利率","value":85.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cdns_operating_margin_pct","label":"CDNS 營業利益率","value":29.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cdns_fcf_margin_pct","label":"CDNS FCF 利潤率","value":28.65,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_snps_gross_margin_pct","label":"SNPS 毛利率","value":72.38,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_operating_margin_pct","label":"SNPS 營業利益率","value":11.03,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_fcf_margin_pct","label":"SNPS FCF 利潤率","value":29.18,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_arm_gross_margin_pct","label":"ARM 毛利率","value":97.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_arm_operating_margin_pct","label":"ARM 營業利益率","value":17.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_arm_fcf_margin_pct","label":"ARM FCF 利潤率","value":28.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_gross_margin_pct","label":"QCOM 毛利率","value":54.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_operating_margin_pct","label":"QCOM 營業利益率","value":23.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_fcf_margin_pct","label":"QCOM FCF 利潤率","value":23.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_688521_sh_gross_margin_pct","label":"688521.SH 毛利率","value":34.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688521.SH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_688521_sh_operating_margin_pct","label":"688521.SH 營業利益率","value":-21.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688521.SH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_688521_sh_fcf_margin_pct","label":"688521.SH FCF 利潤率","value":12.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688521.SH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_free_cash_flow_635m_53m","label":"Free cash flow（營運現金流 $635M 減資本支出 $53M）","value":582,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$M（占營收 36.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司 CFO commentary（8-K Ex99.2，2026-07-27）；與 H1 營運現金流 $990.711M 減 Q1 $355.8M 對得上"},"note":"無共識值可比；全年營運現金流指引由 Q1 時未提供，調升後為約 $2.0B"},{"id":"f_kpi4_sbc_gaap_sbc_146_89m_9_3","label":"SBC 占 GAAP 營業利益（SBC $146.89M，占營收 9.3%）","value":32.6,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 SBC $146,890 千美元；營業利益 $450,315 千美元；占比自算"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":327.89,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-3.83,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":49.46,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.42 → 8.42）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.85 → 9.85）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.6 → 11.6）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":8.42,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.85,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":11.6,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":3.31,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 8.15 → 8.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":65.19,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝49.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":49.6,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":14.67,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝41.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":41.8,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":14.88,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝45.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":45.7,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":38.94,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 8.42，分子＝快照價 327.89","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1269.31,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 2812.52、現金 1543.21（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":274.38,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":91235.44,"period":"2026-11-02","unit":"USD m","basis":"市值 89966.13 ＋ 淨負債 1269.31","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6409.88,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（22 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":7333.71,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":14.23,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 327.89 / W52 324.75 / W104 316.26 / W250 260.72 / W250 13週斜率 0.95%"},{"id":"f_ma_w52","label":"52 週均線","value":324.75,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":316.26,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":260.72,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.95,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"At DAC 2026, all three EDA leaders shipped agentic chip-design stacks: Cadence presented the AuraStack AI Super Agent for PCB and advanced packaging (cited up to 20x faster multiphysics performance) and positioned its four agents, including ChipStack for verification, as a complete silicon-to-system agentic stack; Siemens announced self-verifying agentic workflows in Fuse EDA AI Agent (cited more than 10x faster library characterization); Synopsys announced its own agent portfolio. Futurum's read is that all three are shipping toward the same destination on NVIDIA's stack, with NVIDIA and AMD as lead customers pulling the roadmaps.","source":"Futurum Group, 'Synopsys, Cadence, and Siemens Take Agentic Chip Design Autonomous at DAC' — https://futurumgroup.com/insights/synopsys-cadence-and-siemens-take-agentic-chip-design-autonomous-at-dac/","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"At DAC 2026, Synopsys introduced a fully autonomous design verification agent that it says gives up to 50x faster time-to-validated RTL and 20% additional coverage improvement, plus the first autonomous EDA workflows on Microsoft Discovery with AMD (25-40% reduction in debug cycle time). These are the vendor's own claims as reported by Futurum, not independent benchmarks.","source":"Futurum Group, 'Synopsys, Cadence, and Siemens Take Agentic Chip Design Autonomous at DAC' — https://futurumgroup.com/insights/synopsys-cadence-and-siemens-take-agentic-chip-design-autonomous-at-dac/","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Cadence 10-Q: no single customer accounted for 10% or more of total revenue in the three and six months ended June 30, 2026 or June 30, 2025; and as of June 30, 2026 and December 31, 2025 no single customer accounted for 10% or more of total receivables. The 10-Q text fetched shows no disclosure of a named customer moving to a second EDA supplier or taking the tools in-house.","source":"Cadence Design Systems Form 10-Q for quarter ended 2026-06-30 (StockTitan filing page: https://www.stocktitan.net/sec-filings/CDNS/10-q-cadence-design-systems-inc-quarterly-earnings-report-8a625afc5b99.html)","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Cadence FY2023 10-K（財年結束 2023-12-31）揭露：截至 2023-12-31 與 2022-12-31，沒有任何單一客戶占應收帳款總額 10% 以上。此為應收帳款口徑，非營收口徑；引自搜尋摘要，未逐字讀原文。","source":"SEC EDGAR, Cadence Design Systems Form 10-K FY2023, https://www.sec.gov/Archives/edgar/data/813672/000081367224000034/cdns-20231231.htm","url":null,"excerpt":null,"as_of":"2024-02-14","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Cadence Q2 2026 revenue was $1.584 billion, with record backlog of $8.1 billion; FY2026 revenue guidance $6.26–6.34 billion.","source":"Cadence Design Systems Form 8-K, Exhibit 99.01, Q2 2026 results press release (https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cdns07272026ex9901.htm)","url":null,"excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY2026 guidance was raised: revenue $6.26–6.34B (from $6.125–6.225B), non-GAAP EPS $8.05–8.15 (from $7.85–7.95), operating cash flow ~$2B (from $1.875–1.975B), non-GAAP operating margin 43.75%–44.75% (from 43.5%–44.5%).","source":"Yahoo Finance, 'Cadence Raises 2026 Outlook as AI Agents Drive Broader EDA Demand' (https://finance.yahoo.com/technology/ai/articles/cadence-raises-2026-outlook-ai-164000799.html), published 2026-08-15; underlying figures from company Q2 2026 release dated 2026-07-27","url":null,"excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2 2026 growth by product group per the Zacks-style earnings recap: Core EDA +18%, Systems Design & Analysis +37%, IP +40%; all product groups grew double digits. Backlog was $8.0B in Q1 2026 and $8.1B in Q2 2026.","source":"Yahoo Finance, 'Cadence Q2 Earnings Top Estimates on AI Demand, Backlog Hits $8.1B' (https://finance.yahoo.com/technology/ai/articles/cadence-q2-earnings-top-estimates-142400668.html); figures from search-result summary, article body not fetched","url":null,"excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CEO Anirudh Devgan on the Q2 2026 release: 'accelerating demand for our AI-driven solutions across both Design for AI and AI for Design fronts'; Cadence is 'uniquely positioned to capitalize on this massive TAM expansion opportunity as the only provider with agentic solutions spanning the full electronic system design flow.' Release cites expansions with hyperscalers and leading AI innovators.","source":"Cadence Form 8-K Exhibit 99.01, Q2 2026 results (https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cdns07272026ex9901.htm)","url":null,"excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Cadence describes agentic AI as a 'durable tailwind'; ViraStack reported more than 25 engagements with 2X–10X productivity gains versus traditional flows (company-reported). The article's analyst (Vaishali Doshi) flags the open question of whether agentic AI becomes a durable source of EDA usage rather than a short-lived boost, noting only early support for the durable thesis.","source":"Yahoo Finance, 'Cadence Raises 2026 Outlook as AI Agents Drive Broader EDA Demand' (https://finance.yahoo.com/technology/ai/articles/cadence-raises-2026-outlook-ai-164000799.html)","url":null,"excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261102","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Cadence agreed to plead guilty to conspiracy to commit export control violations (selling semiconductor design tools to a restricted PRC military university via its China subsidiary). Criminal penalties about $118M plus BIS civil penalty over $95M; after coordinated credits, combined net penalties and forfeiture exceed $140M. Cadence must implement an export compliance program; the release says the plea is subject to federal district judge approval.","source":"U.S. Department of Justice, Office of Public Affairs, 'Cadence Design Systems Agrees to Plead Guilty and Pay Over $140 Million for Unlawfully Exporting Semiconductor Design Tools to a Restricted PRC Military University' https://www.justice.gov/opa/pr/cadence-design-systems-agrees-plead-guilty-and-pay-over-140-million-unlawfully-exporting","url":null,"excerpt":null,"as_of":"2025-07-28","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Cadence's Q2 2026 CFO commentary (8-K exhibit) lists in its forward-looking statements the company's 'ongoing obligations under its July 2025 settlement agreements with the U.S. Department of Justice and Bureau of Industry and Security', and the risk of 'any further inquiries or adverse actions by the DOJ, BIS or other governmental authorities and any impact of the settlements on Cadence's operations and business dealings'.","source":"Cadence Design Systems Form 8-K, CFO Commentary Q2 2026 (Ex. 99.2) https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cfocommentary07272026ex9902.htm","url":null,"excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"BIS 對 Cadence 課處 9,500 萬美元行政罰款，事由為未經許可向實體清單機構出口 EDA 硬體、軟體與晶片設計技術；Cadence 承認 2015 年 9 月至 2020 年 9 月間有 56 項違反 EAR，經由別名 Central South CAD Center 售予國防科技大學（NUDT），出口價值約 4,530 萬美元；同時與美國司法部達成協議，含 4,500 萬美元沒收。","source":"BIS press release: Cadence Design Systems to Pay $95 Million Penalty to BIS for Unauthorized Exports to Chinese Entities (bis.gov); BIS Final Order 2025-07-28 (bis.gov/media/documents/cadence-design-systems-final-order-7.28.2025.pdf)","url":null,"excerpt":null,"as_of":"2025-07-28","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國解除 2025 年 5 月對中國 EDA 軟體的出貨限制（Synopsys 表示），屬美中貿易休戰的一環；EDA 廠商可恢復對中國客戶的交付與支援。","source":"CNBC: U.S. lifts chip software curbs on China in sign of trade truce, Synopsys says (cnbc.com/2025/07/03/us-lifts-chip-software-curbs-on-china-amid-trade-truce-synopsys-says-.html)","url":null,"excerpt":null,"as_of":"2025-07-03","retrieved_at":"20261102","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Cadence 2026 年第二季 10-Q 揭露：BIS 於 2025-09-29 生效的暫行最終規則，把實體清單／軍事終端用戶清單的出口限制擴及持股 50% 以上的關係企業；BIS 於 2025-11-11 公布為期一年的暫停，目前預定於 2026-11-09 到期，除非再延長。","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30 (sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm)","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Cadence 2026 年第二季 10-Q 風險揭露列出「擴大的貿易管制法規、新增或提高的關稅與地緣政治衝突」為風險來源；並指出美國增加使用 Section 232 對部分商品（含鋼、鋁、銅）課稅。10-Q 該段未量化財務影響，也未拆出中國營收占比。","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30 (sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm)","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Cadence FY2025 10-K 寫明：先前對中國的出口限制「have had, and any subsequent restrictions may have, an adverse effect on our business, results of operations or financial condition」。10-K 該段未拆出中國營收占比。","source":"Cadence Design Systems Form 10-K for fiscal year ended 2025-12-31 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm)","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-K states Cadence hardware (Palladium emulation, Protium FPGA prototyping), including all PCBs, custom ICs and FPGA-based prototyping components, is manufactured, assembled and tested by subcontractors before delivery to customers.","source":"Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K risk factor: 'We depend on a single supplier or a limited number of suppliers for certain hardware components and contract manufacturers for production of our hardware products, making us vulnerable to supply disruption and price fluctuation.' The filing does not name the manufacturers, their locations or the FPGA supplier.","source":"Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"On May 23, 2025 BIS informed Cadence that a license was required to export, re-export or transfer EDA software and technology where a party is in China or a Chinese military end user. On July 2, 2025 BIS rescinded those license requirements effective immediately.","source":"Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K states Cadence cannot predict whether or when further changes will eliminate, decrease or change the duration of the export restrictions, and that increased restrictions on China exports may lead to additional retaliation by the Chinese government and further escalate geopolitical tensions. It also states that trade regulations limiting or banning sales into certain countries or to certain companies have impacted its ability to transact business in certain countries and with certain customers.","source":"Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q (quarter ended 2026-06-30) states BIS issued an interim final rule effective 2025-09-29 extending export restrictions to entities 50% or more owned by Entity List or Military End-User List parties. On 2025-11-11 BIS published a one-year suspension of that rule, currently set to expire 2026-11-09.","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30, https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#5","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q states Cadence settled with BIS and DOJ in July 2025 over export violations that took place between 2015 and 2021; it paid aggregate net penalties and forfeitures of $140.6 million in the quarter ended 2025-09-30, agreed to plead guilty to one count of conspiracy to commit export controls violations, and booked a $128.5 million charge in Q2 2025.","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30, https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#6","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-Q lists supply chain constraints, expanded trade control laws, new or higher tariffs and geopolitical conflicts among factors affecting its global business. Per search-result summaries of the company's filings, Cadence monitors tariffs for their effect on its hardware business and the cost of imported components, and says geopolitical conflicts have not materially limited its ability to develop or support its products or had a material impact on results, financial condition, liquidity or cash flows.","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30, https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 FY2026 revenue was $1.584B, up 24.2% YoY; non-GAAP EPS $2.11, up 27.9% YoY.","source":"Cadence Reports Second Quarter 2026 Financial Results (Business Wire via Morningstar); 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cdns07272026ex9901.htm","url":null,"excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"IP revenue grew more than 40% YoY in Q2 FY2026, driven by AI, HPC and advanced-node activity.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/ ; BigGo Finance CDNS Q2 2026 earnings call https://finance.biggo.com/news/US_CDNS_2026-07-27","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"System Design and Analysis (SD&A) revenue rose 37% YoY in Q2 FY2026.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/ ; BigGo Finance https://finance.biggo.com/news/US_CDNS_2026-07-27","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Core EDA grew 18% YoY in Q2 FY2026, attributed by the source to AI-enhanced digital implementation and sign-off tools; every product group posted double-digit growth.","source":"BigGo Finance, CDNS Q2 2026 earnings call https://finance.biggo.com/news/US_CDNS_2026-07-27 ; Futurum https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","url":null,"excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Hardware (Palladium Z3 / Protium X3) delivered another record quarter in Q2 FY2026 and added 12 new logos; the source says AI and HPC customers treat hardware-assisted verification as a strategic capacity layer.","source":"BigGo Finance, CDNS Q2 2026 earnings call https://finance.biggo.com/news/US_CDNS_2026-07-27 ; Futurum https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","url":null,"excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Backlog reached a record $8.1B (up 27%), with $4.2B expected to convert to revenue within 12 months.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 guidance was raised to revenue of $6.26B-$6.34B (about 19% growth at midpoint), non-GAAP EPS $8.05-$8.15, non-GAAP operating margin 43.75%-44.75%, operating cash flow about $2B.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"0","claim":"Company guidance assumes export-control exposure stays broadly unchanged; the article does not disclose China revenue share.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","url":null,"excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Moonshot AI's Kimi K3 model reportedly completed a full semiconductor chip design flow autonomously in a single 48-hour run using only open-source EDA tools, with no licensed Cadence or Synopsys software. Demo chip: 4mm² die, 100MHz, Nangate 45nm Open Cell Library, over 8,700 tokens/s simulated inference throughput, no human intervention. CDNS fell 9.6% on the day and SNPS also fell sharply.","source":"Investing.com, 'Why is Cadence Design Systems stock plummeting today?' https://www.investing.com/news/stock-market-news/why-is-cadence-design-systems-stock-plummeting-today-93CH-4798909","url":null,"excerpt":null,"as_of":"2026-07-17","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"The same article says analysts noted the 45nm node used in the Kimi K3 demo is several generations behind the 3nm and 2nm nodes where Cadence's tools remain deeply embedded and hard for open-source alternatives to replicate.","source":"Investing.com, 'Why is Cadence Design Systems stock plummeting today?' https://www.investing.com/news/stock-market-news/why-is-cadence-design-systems-stock-plummeting-today-93CH-4798909","url":null,"excerpt":null,"as_of":"2026-07-17","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"At TSMC's 2026 Technology Symposium, Cadence announced support for four TSMC nodes (N3, N2, A16, A14), described as the broadest explicit node span among the three vendors' announcements. Siemens EDA's stated approach centers on agentic orchestration rather than broad node coverage.","source":"Futurum Group, 'EDA Vendors Race to Align With TSMC's Angstrom-Era Roadmap at Technology Symposium' https://futurumgroup.com/insights/eda-vendors-race-to-align-with-tsmcs-angstrom-era-roadmap-at-technology-symposium/","url":null,"excerpt":null,"as_of":"2026-04-24","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Futurum notes TSMC-COUPE (co-packaged optics) becoming a production technology creates a near-term opening favoring vendors with cross-domain simulation capabilities already in hand. Cadence had not disclosed specific COUPE enablement, which could cede this segment to Synopsys.","source":"Futurum Group, 'EDA Vendors Race to Align With TSMC's Angstrom-Era Roadmap at Technology Symposium' https://futurumgroup.com/insights/eda-vendors-race-to-align-with-tsmcs-angstrom-era-roadmap-at-technology-symposium/","url":null,"excerpt":null,"as_of":"2026-04-24","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Cadence VP of Investor Relations Richard Gu (Nasdaq 54th Investor Conference, 2026-06-09) described agentic AI monetization as subscription-plus-consumption: 'The value is commensurate with what a physical human engineer can do. It's definitely not priced like an LLM token. It's worth tens of thousands of dollars.'","source":"TIKR.com, 'Cadence Design Systems Just Unveiled Its Agentic AI Revenue Model...' https://www.tikr.com/blog/cadence-design-systems-just-unveiled-its-agentic-ai-revenue-model-heres-why-it-could-reset-the-stocks-growth-ceiling","url":null,"excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Per the same TIKR write-up of the Nasdaq conference remarks, management confirmed consumption-based agentic AI revenue is excluded from current guidance. It also cited one customer willing to spend 50% of a human engineer's annual cost on AI agent tokens, and framed EDA's share of chip-company R&D budgets as moving from roughly 11-12% toward about 33%. The 33% figure is the company's/article's framing, not an independently verified number.","source":"TIKR.com, 'Cadence Design Systems Just Unveiled Its Agentic AI Revenue Model...' https://www.tikr.com/blog/cadence-design-systems-just-unveiled-its-agentic-ai-revenue-model-heres-why-it-could-reset-the-stocks-growth-ceiling","url":null,"excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261102","affects":["thesis.H","valuation","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 earnings call summary: customers keep buying the underlying EDA software and separately buy agent licenses. Revenue comes from both new agentic workflow product licenses and increased consumption of underlying core EDA engines. Management avoided assuming a sudden near-term revenue spike from these tools.","source":"Yahoo Finance, 'Cadence Design Systems, Inc. Q2 2026 Earnings Call Summary' https://finance.yahoo.com/technology/ai/articles/cadence-design-systems-inc-q2-123000589.html","url":null,"excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["moat_trend","thesis.H","triggers"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"The Q2 2026 earnings call summary says Cadence's strategy has 'shifted toward becoming a more central partner for hyperscalers and foundries', with deepened collaborations with Intel, Samsung and TSMC. No quantified channel-mix change was disclosed. This is a summarizer's phrasing, not a company-reported change in sales channel.","source":"Yahoo Finance, 'Cadence Design Systems, Inc. Q2 2026 Earnings Call Summary' https://finance.yahoo.com/technology/ai/articles/cadence-design-systems-inc-q2-123000589.html","url":null,"excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-27 Q2 報告後，Q3 EPS 指引 $2.01–2.07，高於 Benzinga 所列共識 $1.84；Q2 non-GAAP EPS $2.11、營收 $1.584B 皆優於 Zacks 共識（EPS +2.9%、營收 +0.5%）","source":"Benzinga CDNS earnings forecasts / Zacks","url":"https://www.benzinga.com/quote/CDNS/earnings-forecasts","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FY2026 指引在不同聚合站數字互相矛盾：多數來源稱營收上調至 $6.26–6.34B、EPS $8.05–8.15；Hudson Labs 與 Zacks 稱營收 $6.125–6.225B、EPS $7.85–7.95；Benzinga 稱 EPS 展望調降；未對帳，需以公司 8-K 為準","source":"MarketBeat / Hudson Labs / Zacks / Benzinga（搜尋摘要）","url":"https://www.hudson-labs.com/research/cadence-q2-2026-earnings-preview-cdns-revenue-guidance-margins","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價均值：Tickflow 截至 2026-07-31 為 $412.83（25 位分析師）；FN2 個別目標區間 $300（Oppenheimer）至 $450（Benchmark）；MarketBeat 均值 $405.69、Moderate Buy；TickerLeague 均值 $418.14（31 筆評等）；較早 Barchart 4 月底均值 $383.29","source":"Tickflow / FN2 / MarketBeat / TickerLeague","url":"https://tickflow.io/stock/CDNS/forecast","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill 稱 Q3 2026 共識 EPS $2.09、營收 $1.645B（預定 2026-10-26 發布），下一季營收預估近 3 個月上修 4.31%；Seeking Alpha 修正頁顯示 EPS 0 上修 7 下修、營收 7 上修 0 下修（無時間窗）。未找到 Q3 實際結果","source":"Chartmill / Seeking Alpha revisions","url":"https://www.chartmill.com/stock/quote/CDNS/estimates","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Cadence 於 2026-02-23 完成收購 Hexagon 設計與工程（D&E）事業（約 €2.7B，2025-09 簽約）","source":"SEC EDGAR 10-Q FY2026 (Q1)","url":"https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000047/cdns-20260331.htm","excerpt":"On February 23, 2026, we completed our acquisition of the design and engineering (“D&E”) business of Hexagon Smart Solutions AB.","as_of":"2026-04-27","retrieved_at":"20261102","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"近12個月8-K共8份，其中含重大項目者僅1份（2026-10-26 Item 8.01：董事會追加 $2.5B 庫藏股授權）；無重編（4.02）或下市等項目","source":"SEC EDGAR 8-K 申報清單／8-K 2026-10-26","url":"https://www.sec.gov/Archives/edgar/data/813672/000081367226000116/cdns-20261023.htm","excerpt":"On October 23, 2026, the board of directors of Cadence approved the repurchase of up to an additional $2.5 billion of the Company’s common stock under its existing share repurchase program.","as_of":"2026-10-26","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"10-K 風險因素載明 2025 年認罪協議／行政和解／緩刑之持續義務，違反可能招致進一步刑事、民事或行政程序","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","excerpt":"Failure to comply with the terms of the plea agreement, the administrative settlement agreement or our probation could result in further criminal, civil, or administrative proceedings or denial of export privileges.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-02-23 完成收購 Hexagon D&E 事業（約 €2.7B，70% 現金＋30% 股票）；2025-10-30 完成收購 Secure-IC（淨對價 $139.6M）","source":"SEC EDGAR 10-Q FY2026 (Q1)","url":"https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000047/cdns-20260331.htm","excerpt":"On February 23, 2026, we completed our acquisition of the design and engineering (“D&E”) business of Hexagon Smart Solutions AB.","as_of":"2026-04-27","retrieved_at":"20261102","affects":["valuation","moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K 風險因素載明認罪協議／行政和解／緩刑義務持續；搜尋未見近12個月集體訴訟","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","excerpt":"Failure to comply with the terms of the plea agreement, the administrative settlement agreement or our probation could result in further criminal, civil, or administrative proceedings or denial of export privileges.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K 8份，重大項目僅1份（庫藏股授權），無Item 4.02重編；搜尋未見2026年SEC調查或重編","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000813672&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CDNS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":85.68,"operating_margin_pct":29.64,"fcf_margin_pct":28.65,"rd_intensity_pct":33.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"SNPS","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.38,"operating_margin_pct":11.03,"fcf_margin_pct":29.18,"rd_intensity_pct":30.6},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"ARM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":97.54,"operating_margin_pct":17.3,"fcf_margin_pct":28.55,"rd_intensity_pct":57.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"QCOM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":54.23,"operating_margin_pct":23.28,"fcf_margin_pct":23.64,"rd_intensity_pct":22.45},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"688521.SH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.18,"operating_margin_pct":-21.28,"fcf_margin_pct":12.94,"rd_intensity_pct":46.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688521.SH","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"CDNS"},"financial_history":{"ticker":"CDNS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":3561718000.0,"revenue_yoy_pct":null,"gross_margin_pct":89.57,"operating_margin_pct":30.15,"net_income":848952000.0,"diluted_eps":3.09,"free_cash_flow":1117679000.0,"fcf_margin_pct":31.38,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":4089986000.0,"revenue_yoy_pct":14.83,"gross_margin_pct":89.36,"operating_margin_pct":30.86,"net_income":1041144000.0,"diluted_eps":3.82,"free_cash_flow":1246673000.0,"fcf_margin_pct":30.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":4641264000.0,"revenue_yoy_pct":13.48,"gross_margin_pct":86.05,"operating_margin_pct":29.79,"net_income":1055484000.0,"diluted_eps":3.85,"free_cash_flow":1118009000.0,"fcf_margin_pct":24.09,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5296759000.0,"revenue_yoy_pct":14.12,"gross_margin_pct":86.36,"operating_margin_pct":31.15,"net_income":1108888000.0,"diluted_eps":4.06,"free_cash_flow":1586910000.0,"fcf_margin_pct":29.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2026_Earnings_Call_20261026.md）

# Q3 2026 Earnings Call
**Cadence Design Systems, Inc.** | Earnings Calls | 2026-10-26

**Operator** (Operator):
Good afternoon. My name is Jade, and I will be your conference operator today. At this time, I would like to welcome everyone to the Cadence Third Quarter 2026 Earnings Conference Call. [Operator Instructions]  
I will now turn the call over to Richard Gu, Vice President of Investor Relations for Cadence. Please go ahead.

**Richard Gu** (Executives):
Thank you, operator. I'd like to welcome everyone to our third quarter of 2026 earnings conference call. I'm joined today by Anirudh Devgan, President and Chief Executive Officer; and John Wall, Senior Vice President and Chief Financial Officer. The webcast of this call and a copy of today's prepared remarks will be available on our website, cadence.com. 
Today's discussion will contain forward-looking statements, including our outlook on future business and operating results. Due to risks and uncertainties, actual results may differ materially from those projected or implied in today's discussion. For information on factors that could cause actual results to differ, please refer to our SEC filings, including our most recent Forms 10-K and 10-Q, CFO commentary and today's earnings release. All forward-looking statements during this call are based on estimates and information available to us as of today and we disclaim any obligation to update them. 
In addition, all financial measures discussed on this call are non-GAAP, unless otherwise specified. The non-GAAP measures should not be considered in isolation from or as a substitute for GAAP results. Reconciliations of GAAP to non-GAAP measures are included in today's earnings release. For the Q&A session today, I would ask that you observe a limit of one question only. If time permits, you can re-queue with additional questions. 
Now I'll turn the call over to Anirudh.

**Anirudh Devgan** (Executives):
Thank you, Richard. Good afternoon, everyone, and thank you for joining us today. I'm pleased to report that Cadence delivered another outstanding quarter with all key metrics coming in well above our guidance. Backlog reached a record of $8.2 billion, reflecting strong bookings driven by growing customer demand. Given our strong business momentum, expanding technology leadership and compelling AI growth opportunities, we are raising our revenue outlook for the year to 21% growth, and our EPS outlook by $0.30 to $8.40. John will provide more details on both our Q3 results and the updated financial outlook. 
Agentic AI represents a transformational market opportunity, and Cadence is exceptionally well positioned to capitalize on it. Our differentiated 3-layer framework is anchored by our physically accurate simulation and optimization engines in the critical middle layer, tightly integrated with AI agents and orchestration at the top and accelerated compute and proprietary data at the base. Agentic AI continues to evolve at a remarkable pace. With our AI super agents gaining strong traction, we are now addressing the long-standing customer demand for domain-specialized models. We believe the future of agentic AI-based design is increasingly domain specialized models combined with intelligent model routing for performance, and reinforcement learning loops with underlying tools for recursive self-improvement. 
Today, I'm excited to introduce Maestro, a portfolio of domain-specialized AI models, purpose-built for chip and system design. By controlling all 3 layers, our AI super agents, Maestro models and proven EDA and SDA tools, we are uniquely positioned to deliver optimal performance, efficiency and throughput results for our customers. Initial results are very compelling, demonstrating up to 30% higher quality and up to 5x greater token efficiency versus general purpose foundation models. Moreover, the Maestro models can be further posttrained on customers' proprietary data to deliver even better outcomes. 
Our model router chooses among our models and other leading frontier and open-weight models as needed for optimal results. Customers can opt to deploy Maestro models in the cloud or in their on-prem environment. Maestro is gaining strong early customer traction with several deployments underway. Momentum of our AI super agents continues to accelerate with compelling early results and more than 100 active customer engagements. We added a new agent to ChipStack for RTL generation and early PPA optimization. That created RTL delivering an average of 24% area and 18% power reduction versus pure foundation model-generated code. Importantly, this demonstrates the power of combining our AI super agents with AI models and our underlying EDA engines to achieve outcomes that foundation models alone cannot deliver. 
Honda is using the RTL generation agent and AI-powered automation to improve productivity from specification to RTL development. In Q3, MediaTek deployed ChipStack into its production digital verification flow, achieving 50% to 70% improvement in verification coverage and 1.4 to 2x reduction in engineering efforts with deployment now scaling across design teams. In analog and custom design, ViraStack saw 4x increase in customer engagement with deployments in various production designs at multiple customers. The combination of agentic workflow, embedded skills and our Virtuoso platform is unlocking significant new productivity opportunities in a traditionally difficult-to-automate domain. We are seeing strong customer interest in InnoStack, our digital AI super-agent, as customers push to improve PPA, accelerate design closure and boost productivity. 
In Q3, the Renesas MCU team successfully deployed InnoStack across a wide range of engineering tasks, achieving a 34x productivity improvement with plans to expand its usage to layout automation. Also in Q3, Samsung Foundry successfully used InnoStack to dramatically improve engineering efficiency and accelerate PPA exploration, reshaping its approach to technology migration and DTCO optimization. 
Socionext is deploying InnoStack in its production design environment and expects its combination with our advanced physical design tools to deliver up to 5x overall productivity gains while maintaining design quality. In PCB and 3D-IC design, the early response to our AuraStack AI Super Agent has been overwhelmingly positive. Nokia is deploying AuraStack on our Millennium supercomputer to advance electronic system design at scale. By unifying agentic AI, our physics-based solvers and accelerated compute in a secure on-prem platform, Nokia is achieving a 5x acceleration in key design and analysis workflows. 
Moving on to our businesses. We are delighted that all product groups delivered outstanding results with year-over-year revenue growth of 20% in core EDA, 24% in IP and 30% in SD&A. Accelerating design activity continues to drive strong demand for our core EDA, SDA and IP products. At the same time, we are seeing amazing customer momentum for our agentic AI portfolio, which is also fueling increased demand for our underlying products. We are pleased that recurring revenue sustained its strong momentum, growing 18% year-over-year. I'm particularly proud of the significant wide-ranging agreements we have signed with top customers. We furthered our long-standing partnership with a global marquee systems customer through a significant wide-ranging expansion of our core EDA, hardware and SDA solutions. 
In Q3, Cadence and a top telco deepened their long-term strategic partnership with a broad expansion across our AI offering, EDA software, hardware and SDA solutions, establishing Cadence as their primary design partner. Core EDA revenue growth was driven by broad-based strength across the portfolio. Our digital and sign-off business continue to expand, achieving 16 new full flow wins during the quarter. As agentic flows increasingly require full vertical workflows, there is growing demand for our synthesis and sign-off solutions. 
Our sign-off product saw growing adoption and our verification software product had strong growth in big digital and memory designs with increasing usage at major hyperscaler and memory companies. As AI and HPC designs continue to grow in scale and complexity, hardware-assisted verification has become an increasingly strategic capability for our customers. This is driving sustained unprecedented demand for our Palladium and Protium emulation platforms, which delivered yet another record quarter. We added several new logos and saw a meaningful expansion with marquee customers across a wide range of verticals. 
Our hardware cloud offering showed strong growth with a leading semiconductor company adopting more hardware cloud services to accelerate new product development. In analog and custom design, Spectre FX continues to gain momentum, highlighted by major competitive displacement at a marquee infrastructure silicon provider with multiple new 2-nanometer projects adopting our platform. Our IP business delivered another outstanding quarter, driven by deepening engagements with leading hyperscalers and semi customers. 
We continue to benefit from strong AI-driven tailwinds, fueling accelerating AI infrastructure investments, growing adoption of custom silicon and increasing demand for high-performance IP. Along with the transition to advanced nodes and chiplet-based architectures, these AI-driven trends are creating a strong pull for our differentiated STAR IP portfolio across interface, memory and foundation IP. We are well positioned for sustained growth as we continue to deliver superior power, performance and area across our expanding advanced IP portfolio. 
A leading space technology company selected our IP portfolio for their custom chip program, paving the way for a broader services and silicon engagement. Tensilica delivered a record revenue quarter and we announced a joint development with Analog Devices across next-generation audio applications. 
Our system design and analysis business delivered another strong quarter, driven by growing adoption of our integrated solutions and proliferation of our expanded electronics and physical systems intelligence portfolio. Allegro momentum continued, including a competitive displacement at a leading EV customer that chose Cadence's integrated PCB design and multiphysics analysis platform as its primary solution. Our Millennium platform had strong adoption driven by deployment of our GPU-accelerated electronic and mechanical systems suite, along with our Reality Digital Twin solution. 
During the quarter, Switch, a leader in sustainable high-density AI infrastructure selected our Millennium and Reality Digital Twin solutions to advance the design and simulation of its next-generation AI factories. The MSC business is the integral part of our physical AI strategy, and its integration is progressing well. MSC Adams, our industry-leading multibody dynamics solution, helped secure a competitive displacement at a leading power company, along with adoption of other Cadence products. 
In summary, Cadence delivered exceptional Q3, and I'm delighted with the accelerating momentum of our business. We are executing extremely well in a vibrant AI market, have a strongest competitive position ever and are extending our leadership in AI. Our highly recurring and ratable business model, combined with growing customer R&D investments is positioning us very well for continued strength in this dynamic AI environment. 
With that, I will turn it over to John to provide more details on our Q3 results and our updated 2026 outlook.

**John Wall** (Executives):
Thanks, Anirudh, and good afternoon, everyone. Cadence delivered strong third quarter results driven by robust demand across our businesses and growing momentum from AI-driven designs. Growth is accelerating and broadening. Q3 revenue grew 22% year-over-year with strong double-digit growth across all product groups. We exceeded our guidance on every key financial metric and ended the quarter with record backlog of $8.2 billion. Here are some of the financial highlights from the third quarter, starting with the P&L. Total revenue was $1.633 billion. GAAP operating margin was 26.2%. Non-GAAP operating margin was 44.1%. GAAP EPS was $1.05. Non-GAAP EPS was $2.11. 
Next turning to the balance sheet and cash flow. Our cash balance was $1.452 billion, while the principal value of debt outstanding was $2.650 billion. Operating cash flow was $424 million. DSOs were 66 days, and we used $400 million to repurchase Cadence shares during the quarter, reflecting our confidence in the business and our commitment to returning capital to shareholders. Underscoring that commitment, our Board has authorized an additional $2.5 billion for our share repurchase program. 
Before I provide our updated outlook, I'd like to highlight that it contains the usual assumption that export control regulations that exist today remain substantially similar for the remainder of the year. For our updated outlook for 2026, we now expect revenue in the range of $6.387 billion to $6.417 billion. GAAP operating margin in the range of 28.2% to 29.2%. Non-GAAP operating margin in the range of 44.2% to 45.2%. GAAP EPS in the range of $4.84 to $4.90. Non-GAAP EPS in the range of $8.37 to $8.43. Operating cash flow of approximately $2 billion. We expect to use more than 50% of our free cash flow to repurchase Cadence shares in 2026. 
For Q4, we expect revenue in the range of $1.695 billion to $1.725 billion. GAAP operating margin in the range of 30% to 31%. Non-GAAP operating margin in the range of 44% to 45%. GAAP EPS in the range of $1.23 to $1.29, and non-GAAP EPS in the range of $2.19 to $2.25. And as usual, we published a CFO commentary document on our Investor Relations website which includes our outlook for additional items as well as further analysis and GAAP to non-GAAP reconciliations. 
Overall, I'm pleased with our Q3 results, especially our recurring revenue growth of 18% year-over-year. At the midpoint of our updated 2026 outlook, we now expect revenue growth of 21%, operating margin of 44.7%, and EPS of $8.40. As always, I'd like to close by thanking our customers, partners and our employees for their continued support. 
And with that, operator, we will now take questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Jason Celino from KeyBanc Capital Markets.

**Jason Celino** (Analysts):
Anirudh, really nice to see the Maestro  announcement. You know I'm not an EDA engineer, I'm not an AI scientist, so maybe can you just explain what this is a little bit better. It sounds like it's part model router, but also maybe domain-specific models. So is Cadence developing these domain-specific models? Maybe just elaborate and then how the monetization of this new product will work.

**Anirudh Devgan** (Executives):
Yes. Jason, and thank you for the question. Yes, there's a lot in that release. So let me try to unpack it a little bit. First of all, we are very pleased with the momentum of our AgentStack and all the 4 super agents. And you can see there are like more than 100 engagements now. So as we work with customers over the last 6 to 9 months, several trends became pretty clear, okay? And to me, we are launching Maestro as what I would call the next generation of agents. And there are 3 big factors in the next generation of agents. 
So one is, like what has happened in the last one year is that, of course, we worked with all the frontier labs from the very beginning, whether they're doing chip design themselves, or we are using their LLMs. But over the last one year, there is this emergence of very, very good open-weight models, okay? And I always wanted to do like domain-specialized models, but now it's finally possible with open-weight models. And it's actually very cost effective to posttrain these models, to deliver like domains intelligence, which is remarkable. 
We're getting up to 30% better quality by using our tools and data to posttrain these models. And also, you don't need like -- it's a portfolio of models. So all the way to like small decisions LLMs to small and medium LLM all the way up to frontier class open-weight models posttrained on our data and intelligence. So that's the first part of Maestro. So it gives really customization for chip and system design and gives much, much better results. It's actually quite remarkable how much these models can be improved by posttraining, okay. 
Now the second part of that is in our agents and when they do these tasks have a variety of tasks, right? So we don't need only one size or type of model to do the task. So the second part is model routing. Just like you don't need to use an airplane to go to your local grocery store, right? So similarly with agents, you have a variety of tasks that we need to do from simple task to like deep thinking and reasoning tasks. So the model router will efficiently, knowing what the task is from our super agents, use the right model. And that can easily give like up to 5x improvement in token efficiency. So either much lower cost or much more work for the same cost. 
And then the third thing is which I always talked about, this reinforcement learning loop with the underlying tools. And we have great examples, for example, we talked about our new RTL agent that one of the customers publicly endorsed Honda, gave 24% area and 18% power because the integration with the underlying tools, and how we call them, and continuous self-improvement whether it's skills or models gives us a unique advantage. 
So if you combine these 3 things together, domain-specialized models, domain specialized family of models, plus model routing, plus deep integration with our tools and data, it gives a unique differentiation that nobody else can do. And it also allows us to control all 3 layers of the cake and innovate in all 3 layers of the cake. So I'm actually super excited. And I think this is what's going to happen in all industries as these LLMs mature, this domain specialized intelligence model routing and integration with underlying agents.

**Operator** (Operator):
Your next question comes from the line of Jim Schneider from Goldman Sachs.

**James Schneider** (Analysts):
I was wondering if you could maybe give us an update on the monetization of the agentic AI solutions you're seeing. I believe last quarter, you talked about recurring revenue growth of 20%. This quarter was 18%. Maybe talk about what the difference there and the recurring was, and maybe underlying that, whether there was any acceleration in the agentic part of that recurring revenue.

**Anirudh Devgan** (Executives):
Yes. Thanks for the question. I'll start, and then John can comment. The -- I'm very proud of the recurring growth. And I mean, this quarter, there were some specific things. Like if you compare it to Q3 of last year, there were some specific things with China revenue moving around, which is not there this year. But in general, recurring revenue is doing phenomenally well. And if you step back and compare last year, recurring revenue was 11%, and it's 18% for this quarter, and it was very good last quarter. 
So I expect recurring revenue to do very well in 2026. And this is a result of, of course, our agentic AI solutions, but also agentic AI solutions driving more usage of our base tools, which, as we always said, is going to happen. So that's what we see. A lot of engagement with agentic and a lot of usage of our base tools. So that provides a lot of growth for recurring and then you add that with our ongoing strength in IP and hardware, and you get a very, very good set of results.

**John Wall** (Executives):
Yes, I'd agree with that, Anirudh. I mean it basically reflects strong demand across our software portfolio and healthy customer expansions and continued strength in core EDA. Yes, I think that's the way to look at it in terms of strong high-teen growth and recurring revenue. We're very pleased with this.

**Operator** (Operator):
Your next question comes from the line of Vivek Arya from Bank of America Securities.

**Vivek Arya** (Analysts):
Anirudh, we recently heard 3 things from your competitors that they can grow sales kind of at a mid-teens pace next year and then compound it to 30%, that they can achieve 50% operating margins. And then also, interestingly, there is a royalty-based model that can help add nearly $1 billion to their top line over the next several years. So I realize, right, this is not the call to give a multiyear growth outlook, but I was just hoping to get your perspective on how you envision sort of this growth and royalty component of Cadence, and how well is Cadence is positioned to maintain or expand your market share and your leading operating margins over time?

**Anirudh Devgan** (Executives):
Yes. Thanks for the question, Vivek. So overall, I'm very pleased with our growth and not just growth, but profitability and margin. And we always talk about like a Rule of 40 metrics, or revenue growth plus margin. So I think we will end the year, if you look at our guide, about 21% revenue growth and slightly less than 45% margin. So we will end up north of 65% in 2026, okay? That's the important thing to point out, okay. And we still have one more quarter to go. So we'll see -- it's an important quarter for us. Fourth quarter is always important. So we'll see how that finishes, and we can update you, like we usually do, in February for the next year. But overall, the environment, I think, is very positive for us. 
As you know, the AI build-out continues, the amount of design activity in all aspects of AI and even the traditional companies in analog mixed-signal companies, digital company, memory companies, system companies, so the amount of design activity is the strongest that I have seen. And our -- we're gaining share in almost all segments of our business, whether it's IP or hardware or EDA, agentic AI. So our product portfolio, I think, is the strongest it has ever been. And then we have this huge opportunity with agentic AI. And I think we are redoing how agentic AI will be defined for all industries with our own domain-specialized models and the flexibility to continue to work with all the frontier models. 
So if you look at all these 3 things, I feel Cadence is in a very, very strong position. Now in terms of your specific question on royalty, we are always looking at different kind of business models. So in IP, we always had royalty for a while in Tensilica, and now we have royalty in our design IP business as well. But to me, that's just one vector. We're always looking at how to best serve -- give value to our customers and then get, of course, value and return.

**Operator** (Operator):
Your next question comes from the line of Siti Panigrahi from Mizuho.

**Sitikantha Panigrahi** (Analysts):
I just want to ask on the hardware, I see even the inventory again grew this quarter. I'm wondering hardware is a strong quarter. How sustainable hardware growth for heading into next year 2027? Any color would be helpful there. And a quick clarification, John. There was a spike in G&A expense in Q3. Was there anything onetime there?

**John Wall** (Executives):
Yes. Sure, Siti. Great. Look, I'll take the hardware question first. The hardware continues to perform exceptionally well. I mean we delivered another record quarter, supported by strong demand from AI and HPC customers. And we're also seeing growing interest in cloud-based hardware access. The hardware-assisted verification is becoming increasingly important because customers are designing systems of unprecedented complexity. They need the capacity to verify those designs before committing to silicon. 
We have a strong pipeline entering Q4. We continue to expect another record year for hardware and as always, hardware can be lumpy from quarter to quarter depending on product deliveries and customer installation schedules. But the underlying demand environment remains very strong, very healthy, and we're very, very encouraged by the pipeline of customer engagement. 
In terms of inventory, the increase in hardware inventory is to support customer orders that we have a significant backlog that we're trying to work our way through, but there are no capacity or supply chain constraints in terms of addressing that. We're just building inventory to hit that -- to hit those numbers. I think you asked about G&A. That's in part of the quarterly movement this quarter reflects the timing of annual charitable contributions, which occurred in Q3 this year compared to Q4 last year. So I wouldn't extrapolate that timing difference into the underlying G&A run rate. So there's a slight impact in G&A in Q3 because of that -- those charitable contributions.

**Anirudh Devgan** (Executives):
Yes. And Siti, just to add on the hardware piece. I mean Palladium and Protium performing exceptionally well. Not just for AI. And of course, we are working with all the major AI companies, but also even any other kind of chip design right now, hardware became indispensable, almost indispensable way to design these things. Now one thing is always like will this trend continue? And we'll see, but there's one megatrend, okay? So hardware is -- you probably know this already, but just to highlight it even further. Hardware is normally sold or consumed based on design size. So if the design size is bigger, then you need more and more hardware. 
So actually, I was recently -- just an example of what is going to happen to design size, I mean the design sizes are already big, but what's going to happen to design sizes in the future. So just to give you an example, I was at imec recently, I gave a talk at imec, which is a European research consortium. And TSMC also gave a talk same session. So TSMC showed their process road map and said in the next 5 years, the chip size will go up by 48x. Now typically, this would happen to be like 5 to 10x in the old days, but I think it's going to be 48x because you have to add regular technology scaling plus 3D-IC. So all these 3D-IC packaging wafer scale integration. 
So that's going to even further create more and more demand for hardware and die-to-die IP and things like that. But -- so now our customers are not only verifying 1 chip or 1 chiplet, they're verifying those chiplets working with other chiplets and the size of the chiplets is going up and then amount of chiplets is going up. So I think this trend, one criticality of hardware-based design and verification combined with the growth in size is going to continue for some time.

**Operator** (Operator):
Your next question comes from the line of Joe Quatrochi from Wells Fargo.

**Joseph Quatrochi** (Analysts):
I was curious if you could just kind of talk about the change in the '26 outlook, particularly from an operating profit perspective because I think when you flow through just kind of the incremental margin on the upside of revenue, it's quite significant relative to maybe your kind of targeted over 50%. So maybe just any help there in terms of understanding what's going on there.

**John Wall** (Executives):
Sure. Yes. Look, we continue to be very pleased with the underlying profitability of the business, despite integrating Hexagon's D&E business and making targeted investments in our strategic growth opportunities, we're now expecting approximately 44.7% non-GAAP operating margin for 2026, which is slightly above last year. But if you look at the revenue growth this year over last year, it's about $1.1 billion. Non-GAAP operating profit is growing about $500 million. And when you consider the Hexagon's D&E being part of that. And that's not really contributing much in the way of operating profit at all this year. But -- and I think we said at the start of the year, we're expecting Hexagon D&E to be about $160 million for the year. It's doing slightly better than that, but it's pretty much on target. 
But I mean, if you back that out, we'd be where you typically expect us to be, which is kind of mid-teens for revenue growth, high teens for EPS growth and in our usual kind of 54%, 55% incremental margin range. So the Hexagon D&E is kind of impacting the incremental margin for this year. But we'd expect that to help us next year because the integration has gone really well. And we're taking steps now to improve things for next year in the same way as we did with BETA in the last couple of years.

**Operator** (Operator):
Your next question comes from the line of Charles Shi from Needham & Company.

**Yu Shi** (Analysts):
Glad to hear about the Maestro model portfolio just announced today. In light of your competitor who announced the GPT-Synopsys, can you tell us what your thoughts are regarding collaborating maybe with the frontier labs for a specialized model, given that Maestro based on what you just described, it sounds like it's a collection of open models posttrained by Cadence. And I think now your customers also have choices between your model portfolio, and let's say GPT-Synopsys, what do you tell your customers when they have both choices and why they should pick Cadence?

**Anirudh Devgan** (Executives):
Yes. Thanks for the question, Charles. So first of all, I just want to point out that we have worked with OpenAI from the very beginning of when they got started. So in terms of chip design -- and we have all kinds of collaborations with OpenAI. And same thing with Anthropic and Gemini, the 3 leading frontier models. So we always discuss all kinds of collaborations with them. 
Now in terms of what we want to make sure as -- in Maestro, the key thing is Maestro is not just our own model, but it still has maximum flexibility to use the right model for the right task. So let's say, if certain -- for a certain percentage of task, a certain frontier model is better, we will, of course, use that to give the best performance to our customers. But the key thing in our solution is that we want to control the 3 layers of the cake, and we want to control the interaction with our customers. We want to be the primary interface to our customers, which is what our customers want. And in return, our agents will provide them a lot of value, and we'll use the right LLM for the task, okay? But the critical thing is as we became the primary interface, and we guarantee the confidentiality of our data and their data. 
So the other thing we will allow with Maestro is if a customer wants to posttrain Maestro further, and this is another request from our customers, we will allow that. If the customers want to have it on-prem, we will allow that. If the customer wants to host on the cloud, we will allow that, okay? So it gives maximum flexibility and maximum performance by combining all 3 layers and only Cadence can provide this. And that will give without any doubt, the best results for our customers.

**Operator** (Operator):
Your next question comes from the line of Harlan Sur from JPMorgan.

**Harlan Sur** (Analysts):
Last quarter, you mentioned the pickup in the more traditional analog power microcontroller segments of the market, right, targeting industrial, automotive, consumer IoT, that's the positive cyclical dynamics we're seeing now as excess customer inventories have bottomed in these end markets. Are you continuing to see the positive demand trends in this segment? And do these same companies are now very focused on embedding next-generation physical AI-based capabilities into their chip designs, right. Your MCU customers, for example, are adding NPU capabilities to their chip designs, your analog customers are designing more sensor-related capabilities into their chips, more AD/DA converters on-chip DSP processing. Is this also translating into a better book of business for the Cadence team?

**Anirudh Devgan** (Executives):
Yes, Harlan, that's a great point. So I think the momentum is very strong in analog and mixed signal, and you can look at their results as well, driven by physical AI and overall recovery of the market. And of course, memory, which we work with all the big memory companies is having, of course, amazing improvement from a year or 2 ago. And I think what it shows up is, first of all, we are very, very strong in mixed-signal companies. So because we have the most complete portfolio with both analog and digital, so these are designs like you mentioned, are more and more mixed signals. So that plays to Cadence's strength. 
And also ViraStack. I'm really pleased by the momentum in ViraStack because as analog customers, whether they are mixed signal companies or these big AI companies also have huge analog teams. I don't know if you realize that. Some of these big AI companies designing their own IPs and all have huge analog teams. So there is a massive demand for analog productivity, which we could not provide earlier. I mean we always wanted to. But with agentic AI, now we can do a lot more in analog productivity. And you can see that in some of the customer codes we have seen and the amount of engagements we have with ViraStack. So overall, I'm pretty pleased not just with the environment of analog mixed signal, but also the new capabilities we are launching with ViraStack.

**Operator** (Operator):
Your next question comes from the line of Joe Vruwink from Baird. Joe Vruwink, a reminder to unmute your device. Your line is open.
Your next question comes from the line of Lee Simpson from Morgan Stanley.

**Lee Simpson** (Analysts):
Anirudh, it does seem as though you and your peer are pursuing very distinct routes to monetizing agentic AI in chip design. I mean I thought you answered one of the previous questions quite well. It really does ring out that you're looking to have your own control on the modeling. Your deployment flexibility comes through. So you can see that adoption, as you see it versus a frontier model-centric partnership is something you think will gain quite good adoption. But is there something in the performance that we need to better appreciate or even in the delivery costs that really led you to go down this route in strategy? And maybe just a follow-up question. You did mention that a leading space company was adopting some of your IP. Just wonder if there's anything specific to call out there. Are they taking just typical IP blocks, or does it come with any broader IP services attached?

**Anirudh Devgan** (Executives):
Yes. Let me answer the second part first, I will come back to the first one. I mean, in general, like we have mentioned that now 45% of our business is coming from the system companies, the nontraditional versus the traditional semi, so these are new customers. And what is also encouraging to see is that it's not just the big AI, hyperscalers where they are doing design. But we are seeing a lot of other system companies like the one we highlighted like a space company even companies in finance doing their own chips. Okay, this is -- as we make chip design easier and easier, this is always the promise that more and more companies will do that. 
And when these new companies do design, we naturally have IP opportunities, but also hardware and also naturally design services because they're getting started. And we have one of the best design services capabilities as we are the best at using our own products. So I think this is some space we have to watch, but I'm pretty encouraged by more system companies doing chip design. 
Now coming back to the AI solution, we want to have control and we want to give flexibility to our customers. So this is the right way to look at it. So -- and there is a lot of value in the model itself, and it is actually pretty cost economical to posttrain a frontier class model. Okay, this could not have happened like 2 years ago. But now it's actually pretty manageable cost to -- and we get pretty remarkable results, like I mentioned, by very incremental cost to posttrain a frontier model. And of course, that's an important thing to have in the bag along with a commercially available frontier model. It's just choosing the best solution of the 2. And then in our own agentic development, right? We have our own IP team, a lot of people using our -- of course, using AgentStack and all the solutions. So the benefits of costs apply to us as well. 
So even though there is some incremental expense to train them, there's also incremental saving in our own deployment of AI. So overall, I think it should not affect any financial model of Cadence. It only gets stronger as we add like a new kind of revenue capability and all the margin progression and all should go as we have planned for a while. But what Maestro does is this flexibility, but also gives customization ability, it gives control and then it gives cost savings. So this is best of all worlds.

**John Wall** (Executives):
Yes, Lee, if I could add there. I think that that's a very, very important point that Anirudh makes in terms of the flexibility. We really want customers to have choice and control over the models they use while benefiting from Cadence's domain expertise and deep integration with our design tools. I mean our strategy remains centered on delivering high-value engineering software rather than building a large general purpose AI infrastructure business. We're focused on improving the efficiency and the value of agentic workflows and maintaining attractive software economics as customer adoption scales, but we think the flexibility works in our model. 
Our model allows customers to use their own LLM infrastructure and bear their associated model compute cost if they want to. And Cadence monetizes the underlying design agents and our agentic orchestration capabilities. The economics of particular deployment options could vary, of course, but the principle is that greater customer usage should create greater value for Cadence. And I think that's where we differentiate ourselves.

**Operator** (Operator):
Your next question comes from the line of Joe Vruwink from Baird.

**Joseph Vruwink** (Analysts):
Can you hear me?

**John Wall** (Executives):
Yes.

**Anirudh Devgan** (Executives):
Yes, Joe, please go ahead.

**Joseph Vruwink** (Analysts):
I want to go back to ViraStack and InnoStack. I think it's fair that the analog and back-end areas haven't seen the AI proliferation yet like front-end design has. Are you seeing this change? Is specialized models and posttraining something that helps better address these domains? And if all of this is starting to happen, is there a commensurately higher revenue implication for Cadence relative to even what has been seen to date?

**Anirudh Devgan** (Executives):
Joe, I mean, first of all, I mean there is -- we started with ChipStack, but then we have launched like 3 other major super agents, as you know, ViraStack for analog, InnoStack for back end, and AuraStack, the latest one, for package and PCB. And I have to say the demand is actually phenomenal. Demand is phenomenal, and especially because these -- ChipStack is doing great, but also these other agents are even more integrated with our base tools. So InnoStack, if you look at our endorsement, typically, when we work with customers to get a public endorsement is only happens like 1 out of 10 customers because not everybody wants to talk about what they're doing, but we have maybe 10 endorsements this quarter. So that tells you the extent of the deployment of all these agents. And if you look at InnoStack, Renesas talking about like 34x productivity improvement, Samsung Foundry, see, there are other use cases that can happen, not just physical design. 
One big use case is design technology co-optimization with the foundry. So the InnoStack is critical agent for that. Socionext talked about 5x productivity improvement. Rapidus Corporation talked about 2x improvement. So there's a multiple x improvement happening with InnoStack. ViraStack, I already said that demand is off the charts. And AuraStack, this is the latest area where innovation hasn't happened. So Nokia showed 5x productivity improvement with AuraStack. So ChipStack is probably a year now in deployment, and these are maybe 6 to 9 months, but there is acceleration deployment of these -- the newer, but they are even more tightly integrated with the base tools. And then Maestro adds further differentiation on top of these capabilities. 
So I feel very, very confident. And what's going to happen is we have a lot of R&D investment in our traditional tools in the middle layer, but now we are putting significant differentiation and investment in the top layer. We are defining, I believe, what will be the agentic flow for the future in all industries. So as we make the agentic, the top layer, and more and more complicated, more and more integrated, more and more differentiated, is very difficult to compete with Cadence in the agentic AI, whether you're a start-up or if you are trying to write -- a customer trying to write some agents, but the capabilities with model routing, with domain-specific models, with tight integration with agent and the tools. This is something that our customers can't do themselves. So that also bodes very well for all of these customers realizing that and working more and more closely not just in the middle layer, but in the top layer with us. So I feel very good in terms of how the speed and differentiation of our agentic offerings.

**Operator** (Operator):
Your next question comes from the line of Jay Vleeschhouwer from Griffin Securities.

**Jay Vleeschhouwer** (Analysts):
Anirudh, in your prepared remarks, you made some important references to the components of your core EDA, particularly in digital. It's demonstrable that over the last number of years, you've gained considerable share in core EDA. But I'd like to delve into what the components of that share gain have been. In other words, when we think about the various large categories that comprise core EDA, especially digital, would it be fair to say that the single largest difference in terms of the dollar and share gain you've had over the last number of years has been with Innovus in implementation and perhaps, to a lesser degree, in areas like synthesis, RTL simulation, analysis and so forth. Or perhaps you can speak about the breadth of where that incremental revenue and shares come from in core EDA to the extent that it's not really largely concentrated in place and route.

**Anirudh Devgan** (Executives):
Yes, Jay, great question. So yes, I mean, over the years -- if you look at over 5, 7 years, we have gained so much in digital implementation, with Innovus becoming basically the platform of choice for advanced nodes design. And then what is particularly encouraging in the last 6 to 12 months is not just Innovus, but all the tools around Innovus. And we always -- I have talked about for 10 years now. Of course, there's integration at lower nodes. So that was going to happen anyway as we go to 3-nanometer, 2-nanometer, it's difficult to separate sign-off from implementation or synthesis from implementation. But then with this agentic AI, there's a further kind of need for vertical flows, which are well integrated. 
So what I -- and I mentioned this last quarter also, I'm particularly pleased to see -- I mean, not only our tools and synthesis and sign-off are much, much better now versus a few years ago. That we are getting this real full flow deployment at not just small or medium customers, but some very, very large customers are deploying our full digital flow, and this is a great trend for Cadence. 
At the same time, we maintain our undisputed leadership in analog, okay? And then because of the strength of Palladium, strength of Jasper, strength of Verisium and agentic flows, ChipStack, it is also helping our verification business and logic simulation. So overall, that's what I was saying, I feel that all the 3 big parts of EDA, we are in a very, very strong position and gaining momentum, not just individual tools being better and proven by large companies, but also this integration at advanced nodes, integration with the agentic solution. So we'll see how it proceeds. But overall, I feel pretty good about it.

**Operator** (Operator):
Your next question comes from the line of Gary Mobley from StoneX.

**Gary Mobley** (Analysts):
Your bookings in the first -- somewhere in the ballpark of, I don't know, mid-20%, call it, 26% year-over-year. If I recall correctly, this was supposed to be a low renewal period 2026 was supposed to be. So my question is, what's driving the strong backlog, the strong bookings? Is it utilizing traditional EDA tools as a result of AI agent workflows? Is it a reflection of the strength of the semiconductor industry? Any color that you can add there would be helpful.

**John Wall** (Executives):
Sure. Thanks, Gary. I mean we're very pleased with both the bookings performance and the growth in backlog, particularly given that 2026, as you mentioned, is a comparatively lighter renewal year for us. The strength reflects healthy underlying design activity, expanded customer engagements and strong add-on opportunities across our portfolio. And what we're seeing is that Cadence is becoming increasingly important to customers as they look to accelerate their engineering road maps and address more complex design challenges. The backlog itself provides good visibility into that. But it's important to remember that backlog and bookings number reflects the timing of revenue recognition that depends on the structure and delivery of individual arrangements and stuff like that. But -- so there's always a blend of time and value in those. But strong bookings in a lighter renewal year are particularly encouraging because they reflect expanding customer engagements and not simply the renewal calendar. But we're very, very pleased with that booking strength.

**Anirudh Devgan** (Executives):
So Gary, needless to say, I mean, we've done 3 quarters. There's still one more quarter to go, which is traditionally our strongest quarter. So we'll see where we end up...

**Operator** (Operator):
Your next question comes from the line of Lachlan Brown from Rothschild.

**Lachlan Brown** (Analysts):
Are you seeing much evidence that new AI design tools like ChipStack are lowering the barriers to entry for custom silicon for nontraditional designers? And I appreciate that land and expand naturally takes time, but are there signs that new logos could become more of a meaningful growth driver for that TAM expansion going forward?

**Anirudh Devgan** (Executives):
Yes, absolutely. I mean like I've talked about this for years that as we make chip design easier to do, there will be more and more people doing chip design. And if you step back, we made chip design maybe over the last 20 years, 100x easier to do because maybe 20 years ago, all these IBM, Intel would do like CPU design with 500 people in like 5 years. Now you can do a CPU design in 6 months with like 50 people. So that's like 100x better. And that's what led to more and more designs. And with AI, we can have and add another 5 to 10x. So it will be like 1,000x easier than probably 20, 25 years ago. And this will invariably lead to more and more design activity. And you can see that even with the hyperscalers, if you go back 1 or 2 years ago, it was not clear that the hyperscalers will do or we always get questions will they continue to do, but now with Google and Meta and Microsoft and Amazon and Tesla, everybody is doing more and more designs. 
Now at the same time, the traditional semiconductor companies are also doing well, of course, the big semi companies. And this is only going to accelerate, in my opinion, with -- like we talked about space companies, finance companies, physical AI, car companies, the amount of design activity we are seeing in automotive is actually quite remarkable and robotics and things like that. And then these things, robotics also require a lot of different chips, right? The amount of chips that are there in one hand, there are like 25 chips in one hand of a humanoid robot to control all the individual motors. So I think we are -- I believe this for years, and I think you will see more and more of this. And our job is to make these things easier to use, have more -- give more flexibility to our customers, like we did with our agent solution in Maestro, so they can do more themselves.

**Operator** (Operator):
Your final question comes from the line of Kelsey Chia from Citi.

**Wei Chia** (Analysts):
Anirudh and John, congrats on great results. My question is on EDA. EDA growth has been very strong for the last 3 quarters, 18%, 19% year-on-year growth, well above the historical growth rate. And it sounds like a majority of that growth is primarily driven by hardware and agentic AI attribution is still quite small. Is that a fair characterization? Or could you give us a sense of customer adoption levels for agentic workflow today? And if much of the sort of revenue acceleration from agentic AI is still ahead of us?

**Anirudh Devgan** (Executives):
Yes, thanks for the question. Yes, of course, we are very proud of the hardware growth. But as you know, we will break out recurring and nonrecurring growth. So like I was mentioning earlier, and John mentioned also, our recurring growth has improved from 11% last year to 18%. So that is not hardware. That's ex hardware because hardware will typically show up in nonrecurring growth. So that's a major improvement of our recurring growth from last year to this year. And that is a combination of agentic AI plus the growth of underlying tools and design starts on the software side.

**John Wall** (Executives):
Yes. Kelsey, I think based on like listening to Anirudh answer Lachlan's question there a few minutes ago that essentially, we believe that agentic AI is a demand accelerator for EDA. I mean customers have always built their own workflows around Cadence tools. And we expect them to continue to develop their own agents as well. Our strategy accommodates that. What's exciting is that agents could perform much more designed exploration than an individual engineer, calling our underlying agents repeatedly, and that creates a potential for significantly more consumption of our core EDA tools. And I think you're starting to see that reflected in our EDA growth this year.

**Operator** (Operator):
At this time, there are no further questions. I will now turn it back to Anirudh Devgan for closing remarks.

**Anirudh Devgan** (Executives):
Thank you all for joining us this afternoon. It's an exciting time for Cadence as we finish our Q3 with AI-driven product leadership and strong business momentum. The Wall Street Journal ranked Cadence's Board #2 among all S&P 500 companies in its 2026 Best Boards list. And on behalf of our employees and of our Board of Directors, we thank our customers, partners and investors for their continued trust and confidence in Cadence.

**Operator** (Operator):
Thank you for participating in today's Cadence Third Quarter 2026 Earnings Conference Call. This concludes today's call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CDNS_Q2_2026_Earnings_Call_20260727.md
- 2026-07-27｜CEO｜guidance：CEO 說全年營收財測上調至約 19% 成長，並稱為單季最大上調幅度（原話："raising our guidance for the year to 19% revenue growth"）
- 2026-07-27｜CFO｜guidance：CFO 給出全年營收財測區間（原話："we now expect revenue in the range of $6.260"）
- 2026-07-27｜CFO｜guidance：CFO 給出 Q3 營收財測區間（原話："revenue in the range of $1.595 billion to $1.625 billion"）
- 2026-07-27｜CFO｜guidance：財測假設出口管制維持現狀（原話："export control regulations that exist today remain"）
- 2026-07-27｜CFO｜guidance：CFO 稱財測中點：營收成長 19%、營業利益率 44.25%、EPS 8.10（原話："operating margin of 44.25%, EPS of $8.10"）
- 2026-07-27｜CFO｜guidance：CFO 稱財測未假設 Agentic AI 出現突然的階梯式增量（原話："we're still not assuming a sudden step function in our"）
- 2026-07-27｜CFO｜guidance：CFO 說本次上調反映廣泛面向，非單一客戶或產品（原話："reflects broad-based strength"）
- 2026-07-27｜CFO｜guidance：CFO 稱全年營收組合預期約 80% 經常性、20% 前置認列（原話："roughly 80% recurring"）
- 2026-07-27｜CFO｜margin：CFO 說明下半年利潤率略低於上半年，為刻意投資而非模型惡化（原話："These are deliberate investments and not a"）
- 2026-07-27｜CFO｜margin：CFO 說下半年利潤率略低於上半年（原話："slightly lower margins than the first half"）
- 2026-07-27｜CFO｜margin：CFO 稱預期併購標的與 IP 獲利能力到 2027 持續改善（原話："acquisition profitability and profitability of IP to"）
- 2026-07-27｜CFO｜margin：CFO 稱去年預留 2000～2500 萬美元用於下半年投資（原話："$20 million, $25 million set aside specifically for"）
- 2026-07-27｜CFO｜margin：CFO 拆解經常性營收：成長約 24%，Hexagon 貢獻約 4 點（原話："Hexagon contributed roughly 4 points."）
- 2026-07-27｜CFO｜margin：CFO 稱扣除 Hexagon 後經常性營收（pro forma）高十位數到 20%（原話："high teens to 20% on a normalized pro forma basis"）
- 2026-07-27｜CEO｜margin：CEO 稱 Agentic AI 不需大幅增加投資，AI 甚至可能降低成本（原話："Agentic AI, it does not"）
- 2026-07-27｜CEO｜margin：CEO 稱不應模型化大規模投資（原話："you should not"）
- 2026-07-27｜CFO｜capital_allocation：CFO 稱 2026 年約以 50% 自由現金流回購股票（原話："approximately 50% of our free cash flow to repurchase"）
- 2026-07-27｜CFO｜capital_allocation：CFO 報告 Q2 回購 2 億美元（原話："we used $200 million to repurchase Cadence shares."）
- 2026-07-27｜CFO｜capital_allocation：CFO 稱投入整合 Hexagon D&E 與 Intel 等機會（原話："integrate Hexagon's D&E business because we're very"）
- 2026-07-27｜CEO｜product：CEO 稱 IP 業務年增逾 40%，且大部分為內生成長（原話："most of it is organic growth"）
- 2026-07-27｜CFO｜product：CFO 提醒 IP 收入有季度時點性，不要將單季年化（原話："I wouldn't annualize any one quarter."）
- 2026-07-27｜CEO｜product：CEO 稱核心 EDA 年增 18%、系統設計與分析年增 37%（原話："System design and analysis revenue grew 37% year-over-year."）
- 2026-07-27｜CEO｜product：CEO 稱硬體業務再創單季紀錄（原話："Our hardware business delivered another record quarter"）
- 2026-07-27｜CEO｜product：CEO 稱 ChipStack 已有逾 20 個客戶接觸、ViraStack 逾 25 個（原話："more than 25 customer"）
- 2026-07-27｜CFO｜product：CFO 說明 Agentic AI 的變現方式：客戶先買底層軟體再買 agent 授權（原話："they purchase Cadence agent licenses"）
- 2026-07-27｜CEO｜product：CEO 稱 agent 產品上市約六個月，早期 add-on 令人鼓舞但仍在早期（原話："the early add-on business is encouraging"）
- 2026-07-27｜CFO｜product：CFO 稱硬體仍受供給限制而非需求限制，並預期 2026 再創硬體紀錄年（原話："expect 2026 to be another record hardware year"）
- 2026-07-27｜CEO｜competition：CEO 稱競爭地位前所未有地好、正在多家客戶取得份額（原話："we are taking a lot of share in"）
- 2026-07-27｜CEO｜competition：CEO 回應 LLM 端到端設計晶片的疑慮：認為受商品化的是 LLM 選擇而非 EDA 工具（原話："I think what is likely to happen is not the EDA"）
- 2026-07-27｜CEO｜competition：CEO 稱 Cadence 過去在 Intel 與 Samsung 較弱，現已改變（原話："we were weak at Intel and"）
- 2026-07-27｜CEO｜competition：CEO 回應開源模型 Kimi 設計晶片：稱僅為舊製程小區塊且仍需 EDA 工具（原話："they needed kind of EDA"）
- 2026-07-27｜CEO｜competition：CEO 稱不看對手而看是否滿足客戶工作負載（原話："We're not looking at who is doing -- who"）
- 2026-07-27｜CEO｜customer：CEO 稱 Intel 合約為多年期、全數為既有協議之外的增量（原話："all incremental to our business, 100%"）
- 2026-07-27｜CEO｜customer：CEO 稱 Intel 協議為多年期，今年有部分貢獻，大部分在未來（原話："most of it is to come, okay?"）
- 2026-07-27｜CEO｜customer：CEO 稱超大規模雲端業者對矽晶片的投入高於 12 個月前（原話："the commitment to silicon is much higher than like 12 months"）
- 2026-07-27｜CEO｜customer：CEO 稱近六個月新創公司活動回溫（原話："Start-ups were kind of dormant."）
- 2026-07-27｜CEO｜customer：CFO 與 CEO 說今年為三年續約週期中的低點年，但 add-on 強勁（原話："this year is a low bookings"）
- 2026-07-27｜CEO｜customer：CEO 稱硬體新增 12 個新客戶（原話："We added 12 new logos"）
- 2026-07-27｜CEO｜risk：CEO 稱對 2027 以後預測審慎，不量化 Agentic 對明年的貢獻（原話："very careful about projecting future, next year numbers"）
- 2026-07-27｜CFO｜risk：CFO 稱硬體有季度時點效應（原話："There could be quarterly timing effects"）
- 2026-07-27｜CFO｜commitment：CFO 稱下半年專注投資，目標讓明年營業利益率更好（原話："we have better operating margins next year"）
- 2026-07-27｜CFO｜commitment：CFO 稱正專注於改善明年利潤率（原話："focused on improving margins for next year."）

### 問答異常語氣（迴避／改口／保留）
- CDNS_Q2_2026_Earnings_Call_20260727.md｜問：Quatrochi（Wells Fargo）問 Agentic AI TAM 能否量化及對 EDA 占 R&D 比重的影響｜答法：CEO 未給 TAM 數字，改談 super agents 與 add-on 強度；CFO 補充財測未假設階梯式增量
- CDNS_Q2_2026_Earnings_Call_20260727.md｜問：Schneider（Goldman）問 add-on 對財測上調或明年核心 EDA 營收的量化影響｜答法：CEO 以「我們對明年數字很謹慎」回應，未給量化，改談三項驅動因素；CFO 強調上調為廣泛面向
- CDNS_Q2_2026_Earnings_Call_20260727.md｜問：Conti（Deutsche）問 Intel 合約規模、提取期間與是否在財測內｜答法：CEO 只說多年期、今年有部分、大部分在未來，未給金額或是否在財測內，轉談四五個成長引擎
- CDNS_Q2_2026_Earnings_Call_20260727.md｜問：Arya（BofA）問 IP 可持續成長率及 Hexagon 貢獻與 EPS 稀釋｜答法：CFO 未給 Hexagon 具體貢獻數字與 EPS 稀釋，僅稱符合預期；對 IP 成長率稱不要年化單季

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
{"date":"20260924","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"設計案數與設計複雜度帶動經常性營收維持中高雙位數有機成長","columns":{"驗證點":"2Y：FY2027 經常性營收有機年增 ≥15%、在手訂單年增 ≥10%","具體數字門檻":"經常性營收有機年增 ≥15%（Q2 扣 Hexagon 約 4 點後為高十幾到 20%）","信息來源":"每季 CFO commentary 與法說；在手訂單見季報新聞稿","漂移觸發條件":"連 2 季低於門檻 5% 以上（&lt;14.25%）為削弱；連 3 季低於門檻 10% 以上（&lt;13.5%）為反轉"}},{"id":"H2","text":"有機增量利潤率 50–60% 加上 Hexagon 轉增益，非 GAAP 營業利益率續擴張，EPS 成長快於營收","columns":{"驗證點":"2Y：FY2027 非 GAAP 營業利益率 ≥45%（FY2026 指引中點 44.25%）","具體數字門檻":"FY2027 非 GAAP 營業利益率指引或實績 ≥45%","信息來源":"2027 年 2 月全年財測、每季 CFO commentary","漂移觸發條件":"連 2 季低於 42.75% 為削弱；連 3 季低於 40.5% 為反轉"}},{"id":"H3","text":"agent 成為可揭露的新營收線，並帶動底層工具用量，EDA 占客戶研發預算續升","columns":{"驗證點":"5Y：2028 年底前揭露 agent 營收或占比；2031 年 EDA 占客戶研發支出 ≥13%（現約 11%）","具體數字門檻":"首次揭露 agent 營收，且當期核心 EDA 年增 ≥15%","信息來源":"法說、投資人會議、10-K","漂移觸發條件":"核心 EDA 年增連 4 季低於 14.25% 為削弱；連 6 季低於 13.5% 為反轉"}},{"id":"H4","text":"先進製程投片仍離不開商用 EDA 的簽核與硬體驗證，Cadence 在數位實作、類比、硬體驗證維持前二","columns":{"驗證點":"10Y：到 2036 年，7 奈米以下量產投片仍全數使用商用簽核流程","具體數字門檻":"前十大晶片設計公司無一在 7 奈米以下以非商用工具量產投片","信息來源":"產業新聞、台積電技術論壇、法說","漂移觸發條件":"跨 2 個年度出現繞過案例為削弱；跨 3 個年度為反轉"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價≤$260（約FY2027本益比27倍）加碼一段；11/9關係企業出口規則到期後EDA未受限且全年財測維持→再加一段","irr_base_pct":9.5,"ev5y_pct":46.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"A","val":"🟡","ma":"🟠","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":3.1,"ev5y_pct":46.7,"irr_base_pct":9.5,"max_dd_pct":-50,"bull_5y_price":691.2,"bear_5y_price":206.8,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"價≤$260（約FY2027本益比27倍）加碼一段；11/9關係企業出口規則到期後EDA未受限且全年財測維持→再加一段","price_at_dd":309.09,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
