你是 stock-analyst **v20 判斷 agent**，標的 CDNS（20260924）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CDNS","date":"2026-09-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260924/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260924/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":1584.451,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$M（YoY +24.2%，QoQ +7.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release；YoY／QoQ 由 Q2 2025 $1,275.441M、Q1 2026 $1,474.22M（H1 $3,058.671M 減 Q2）自算"},"note":"共識 $1.577B（媒體報導，Benzinga／Yahoo 引述，非 IR）；公司自家 Q2 指引 $1.555–1.595B，落在區間內偏上"},{"id":"f_kpi1_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":45.5,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release（Q2 2025 為 42.8%）"},"note":"公司自家 Q2 指引 44.5–45.5%，落在區間上緣；第三方共識值未取得"},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":28.4,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"%（營業利益 $450.3M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release／8-K Ex99.1（Q2 2025 為 19.0%、營業利益 $241.8M）"},"note":"公司自家 Q2 指引 28.5–29.5%，實際略低於區間下緣 0.1pt；新聞稿調節表列併購／整合成本占營收 2.1%；第三方共識值未取得"},{"id":"f_kpi5_non_gaap_diluted_eps","label":"Non-GAAP diluted EPS","value":2.11,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$（GAAP EPS $1.33）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release"},"note":"共識 $2.06（媒體報導，非 IR）；公司自家 Q2 指引 $2.02–2.08，高出上緣 $0.03"},{"id":"f_kpi6_backlog","label":"Backlog（在手訂單）","value":8.1,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$B（創新高）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release"},"note":"無共識值可比"},{"id":"f_kpi7_rpo_12_crpo","label":"RPO 未來 12 個月內認列（cRPO）","value":4.2,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 investor.cadence.com Q2 2026 press release"},"note":"無共識值可比"},{"id":"f_kpi8_guidance_q3_fy2026","label":"Guidance — Q3 FY2026","value":"營收 $1,595–1,625M（YoY +19–21%）；non-GAAP 營業利益率 43.5–44.5%；GAAP 營業利益率 27.5–28.5%；non-GAAP EPS $2.01–2.07；GAAP EPS $1.11–1.17；預計回購約 $200M","period":"Q2 FY2026 財報（公告於 2026-07-27）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2026 財報（公告於 2026-07-27）","citation":"公司 CFO commentary（8-K Ex99.2，2026-07-27）＋新聞稿 investor.cadence.com Q2 2026 press release"},"note":"Q3 共識值未取得；註：指引中點營收 $1.61B 較 Q2 僅 +1.6% QoQ，non-GAAP 營業利益率中點 44.0% 低於 Q2 實績 45.5%"},{"id":"f_kpi9_guidance_fy2026","label":"Guidance — FY2026（本次調升）","value":"營收 $6.26–6.34B（YoY +18–20%）；non-GAAP 營業利益率 43.75–44.75%；GAAP 營業利益率 27.75–28.75%；non-GAAP EPS $8.05–8.15；GAAP EPS $4.76–4.86；營運現金流約 $2.0B；non-GAAP／GAAP 稅率約 16.5%／26%；回購約占 FCF 50%","period":"Q2 FY2026 財報（公告於 2026-07-27）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q2 FY2026 財報（公告於 2026-07-27）","citation":"公司 CFO commentary（8-K Ex99.2，2026-07-27）＋新聞稿 investor.cadence.com Q2 2026 press release"},"note":"2026-09-19 共識 FY2026 non-GAAP EPS $8.14（dd_numbers_extra.py consensus_revision），落在指引區間上緣；此為財報後共識，非財報前預期"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-07-27","period":"2026-07-27","unit":"date","basis":"距今 43 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-07-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cdns_gross_margin_pct","label":"CDNS 毛利率","value":85.87,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cdns_operating_margin_pct","label":"CDNS 營業利益率","value":30.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cdns_fcf_margin_pct","label":"CDNS FCF 利潤率","value":28.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_snps_gross_margin_pct","label":"SNPS 毛利率","value":72.38,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_operating_margin_pct","label":"SNPS 營業利益率","value":11.03,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_fcf_margin_pct","label":"SNPS FCF 利潤率","value":29.18,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_arm_gross_margin_pct","label":"ARM 毛利率","value":97.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_arm_operating_margin_pct","label":"ARM 營業利益率","value":17.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_arm_fcf_margin_pct","label":"ARM FCF 利潤率","value":28.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_gross_margin_pct","label":"QCOM 毛利率","value":54.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_operating_margin_pct","label":"QCOM 營業利益率","value":23.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_fcf_margin_pct","label":"QCOM FCF 利潤率","value":23.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_free_cash_flow_635m_53m","label":"Free cash flow（營運現金流 $635M 減資本支出 $53M）","value":582,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"$M（占營收 36.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司 CFO commentary（8-K Ex99.2，2026-07-27）；與 H1 營運現金流 $990.711M 減 Q1 $355.8M 對得上"},"note":"無共識值可比；全年營運現金流指引由 Q1 時未提供，調升後為約 $2.0B"},{"id":"f_kpi4_sbc_gaap_sbc_146_89m_9_3","label":"SBC 占 GAAP 營業利益（SBC $146.89M，占營收 9.3%）","value":32.6,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）","citation":"公司新聞稿 SBC $146,890 千美元；營業利益 $450,315 千美元；占比自算"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":309.09,"period":"2026-09-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":9.84,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":52.65,"period":"2026-09-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.14 → 8.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.55 → 9.55）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.15 → 11.15）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":8.14,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.55,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":11.15,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.26,"period":"2026-06-23 → 2026-09-19","unit":"%","basis":"FY1 共識 EPS 7.96 → 8.14（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":61.45,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝35.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":35.9,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":14.58,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝40.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":40.2,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":14.77,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝43.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":43.8,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":37.97,"period":"2026-09-19","unit":"x","basis":"分母＝FY1 EPS 8.14，分子＝快照價 309.09","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-19"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-09-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 309.09 / W52 324.73 / W104 313.03 / W250 257.51 / W250 13週斜率 0.7%"},{"id":"f_ma_w52","label":"52 週均線","value":324.73,"period":"2026-09-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":313.03,"period":"2026-09-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":257.51,"period":"2026-09-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.7,"period":"2026-09-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"At DAC 2026, all three EDA leaders shipped agentic chip-design stacks: Cadence presented the AuraStack AI Super Agent for PCB and advanced packaging (cited up to 20x faster multiphysics performance) and positioned its four agents, including ChipStack for verification, as a complete silicon-to-system agentic stack; Siemens announced self-verifying agentic workflows in Fuse EDA AI Agent (cited more than 10x faster library characterization); Synopsys announced its own agent portfolio. Futurum's read is that all three are shipping toward the same destination on NVIDIA's stack, with NVIDIA and AMD as lead customers pulling the roadmaps.","source":"Futurum Group, 'Synopsys, Cadence, and Siemens Take Agentic Chip Design Autonomous at DAC' — https://futurumgroup.com/insights/synopsys-cadence-and-siemens-take-agentic-chip-design-autonomous-at-dac/","as_of":"2026-07-29","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"At DAC 2026, Synopsys introduced a fully autonomous design verification agent that it says gives up to 50x faster time-to-validated RTL and 20% additional coverage improvement, plus the first autonomous EDA workflows on Microsoft Discovery with AMD (25-40% reduction in debug cycle time). These are the vendor's own claims as reported by Futurum, not independent benchmarks.","source":"Futurum Group, 'Synopsys, Cadence, and Siemens Take Agentic Chip Design Autonomous at DAC' — https://futurumgroup.com/insights/synopsys-cadence-and-siemens-take-agentic-chip-design-autonomous-at-dac/","as_of":"2026-07-29","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Cadence 10-Q: no single customer accounted for 10% or more of total revenue in the three and six months ended June 30, 2026 or June 30, 2025; and as of June 30, 2026 and December 31, 2025 no single customer accounted for 10% or more of total receivables. The 10-Q text fetched shows no disclosure of a named customer moving to a second EDA supplier or taking the tools in-house.","source":"Cadence Design Systems Form 10-Q for quarter ended 2026-06-30 (StockTitan filing page: https://www.stocktitan.net/sec-filings/CDNS/10-q-cadence-design-systems-inc-quarterly-earnings-report-8a625afc5b99.html)","as_of":"2026-06-30","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Cadence FY2023 10-K（財年結束 2023-12-31）揭露：截至 2023-12-31 與 2022-12-31，沒有任何單一客戶占應收帳款總額 10% 以上。此為應收帳款口徑，非營收口徑；引自搜尋摘要，未逐字讀原文。","source":"SEC EDGAR, Cadence Design Systems Form 10-K FY2023, https://www.sec.gov/Archives/edgar/data/813672/000081367224000034/cdns-20231231.htm","as_of":"2024-02-14","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Cadence Q2 2026 revenue was $1.584 billion, with record backlog of $8.1 billion; FY2026 revenue guidance $6.26–6.34 billion.","source":"Cadence Design Systems Form 8-K, Exhibit 99.01, Q2 2026 results press release (https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cdns07272026ex9901.htm)","as_of":"2026-07-27","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY2026 guidance was raised: revenue $6.26–6.34B (from $6.125–6.225B), non-GAAP EPS $8.05–8.15 (from $7.85–7.95), operating cash flow ~$2B (from $1.875–1.975B), non-GAAP operating margin 43.75%–44.75% (from 43.5%–44.5%).","source":"Yahoo Finance, 'Cadence Raises 2026 Outlook as AI Agents Drive Broader EDA Demand' (https://finance.yahoo.com/technology/ai/articles/cadence-raises-2026-outlook-ai-164000799.html), published 2026-08-15; underlying figures from company Q2 2026 release dated 2026-07-27","as_of":"2026-07-27","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2 2026 growth by product group per the Zacks-style earnings recap: Core EDA +18%, Systems Design & Analysis +37%, IP +40%; all product groups grew double digits. Backlog was $8.0B in Q1 2026 and $8.1B in Q2 2026.","source":"Yahoo Finance, 'Cadence Q2 Earnings Top Estimates on AI Demand, Backlog Hits $8.1B' (https://finance.yahoo.com/technology/ai/articles/cadence-q2-earnings-top-estimates-142400668.html); figures from search-result summary, article body not fetched","as_of":"2026-07-27","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CEO Anirudh Devgan on the Q2 2026 release: 'accelerating demand for our AI-driven solutions across both Design for AI and AI for Design fronts'; Cadence is 'uniquely positioned to capitalize on this massive TAM expansion opportunity as the only provider with agentic solutions spanning the full electronic system design flow.' Release cites expansions with hyperscalers and leading AI innovators.","source":"Cadence Form 8-K Exhibit 99.01, Q2 2026 results (https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cdns07272026ex9901.htm)","as_of":"2026-07-27","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Cadence describes agentic AI as a 'durable tailwind'; ViraStack reported more than 25 engagements with 2X–10X productivity gains versus traditional flows (company-reported). The article's analyst (Vaishali Doshi) flags the open question of whether agentic AI becomes a durable source of EDA usage rather than a short-lived boost, noting only early support for the durable thesis.","source":"Yahoo Finance, 'Cadence Raises 2026 Outlook as AI Agents Drive Broader EDA Demand' (https://finance.yahoo.com/technology/ai/articles/cadence-raises-2026-outlook-ai-164000799.html)","as_of":"2026-08-15","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Cadence agreed to plead guilty to conspiracy to commit export control violations (selling semiconductor design tools to a restricted PRC military university via its China subsidiary). Criminal penalties about $118M plus BIS civil penalty over $95M; after coordinated credits, combined net penalties and forfeiture exceed $140M. Cadence must implement an export compliance program; the release says the plea is subject to federal district judge approval.","source":"U.S. Department of Justice, Office of Public Affairs, 'Cadence Design Systems Agrees to Plead Guilty and Pay Over $140 Million for Unlawfully Exporting Semiconductor Design Tools to a Restricted PRC Military University' https://www.justice.gov/opa/pr/cadence-design-systems-agrees-plead-guilty-and-pay-over-140-million-unlawfully-exporting","as_of":"2025-07-28","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Cadence's Q2 2026 CFO commentary (8-K exhibit) lists in its forward-looking statements the company's 'ongoing obligations under its July 2025 settlement agreements with the U.S. Department of Justice and Bureau of Industry and Security', and the risk of 'any further inquiries or adverse actions by the DOJ, BIS or other governmental authorities and any impact of the settlements on Cadence's operations and business dealings'.","source":"Cadence Design Systems Form 8-K, CFO Commentary Q2 2026 (Ex. 99.2) https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cfocommentary07272026ex9902.htm","as_of":"2026-07-27","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"BIS 對 Cadence 課處 9,500 萬美元行政罰款，事由為未經許可向實體清單機構出口 EDA 硬體、軟體與晶片設計技術；Cadence 承認 2015 年 9 月至 2020 年 9 月間有 56 項違反 EAR，經由別名 Central South CAD Center 售予國防科技大學（NUDT），出口價值約 4,530 萬美元；同時與美國司法部達成協議，含 4,500 萬美元沒收。","source":"BIS press release: Cadence Design Systems to Pay $95 Million Penalty to BIS for Unauthorized Exports to Chinese Entities (bis.gov); BIS Final Order 2025-07-28 (bis.gov/media/documents/cadence-design-systems-final-order-7.28.2025.pdf)","as_of":"2025-07-28","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國解除 2025 年 5 月對中國 EDA 軟體的出貨限制（Synopsys 表示），屬美中貿易休戰的一環；EDA 廠商可恢復對中國客戶的交付與支援。","source":"CNBC: U.S. lifts chip software curbs on China in sign of trade truce, Synopsys says (cnbc.com/2025/07/03/us-lifts-chip-software-curbs-on-china-amid-trade-truce-synopsys-says-.html)","as_of":"2025-07-03","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Cadence 2026 年第二季 10-Q 揭露：BIS 於 2025-09-29 生效的暫行最終規則，把實體清單／軍事終端用戶清單的出口限制擴及持股 50% 以上的關係企業；BIS 於 2025-11-11 公布為期一年的暫停，目前預定於 2026-11-09 到期，除非再延長。","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30 (sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm)","as_of":"2026-06-30","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Cadence 2026 年第二季 10-Q 風險揭露列出「擴大的貿易管制法規、新增或提高的關稅與地緣政治衝突」為風險來源；並指出美國增加使用 Section 232 對部分商品（含鋼、鋁、銅）課稅。10-Q 該段未量化財務影響，也未拆出中國營收占比。","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30 (sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm)","as_of":"2026-06-30","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Cadence FY2025 10-K 寫明：先前對中國的出口限制「have had, and any subsequent restrictions may have, an adverse effect on our business, results of operations or financial condition」。10-K 該段未拆出中國營收占比。","source":"Cadence Design Systems Form 10-K for fiscal year ended 2025-12-31 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm)","as_of":"2025-12-31","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-K states Cadence hardware (Palladium emulation, Protium FPGA prototyping), including all PCBs, custom ICs and FPGA-based prototyping components, is manufactured, assembled and tested by subcontractors before delivery to customers.","source":"Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","as_of":"2025-12-31","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K risk factor: 'We depend on a single supplier or a limited number of suppliers for certain hardware components and contract manufacturers for production of our hardware products, making us vulnerable to supply disruption and price fluctuation.' The filing does not name the manufacturers, their locations or the FPGA supplier.","source":"Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","as_of":"2025-12-31","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"On May 23, 2025 BIS informed Cadence that a license was required to export, re-export or transfer EDA software and technology where a party is in China or a Chinese military end user. On July 2, 2025 BIS rescinded those license requirements effective immediately.","source":"Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","as_of":"2025-12-31","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K states Cadence cannot predict whether or when further changes will eliminate, decrease or change the duration of the export restrictions, and that increased restrictions on China exports may lead to additional retaliation by the Chinese government and further escalate geopolitical tensions. It also states that trade regulations limiting or banning sales into certain countries or to certain companies have impacted its ability to transact business in certain countries and with certain customers.","source":"Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm","as_of":"2025-12-31","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q (quarter ended 2026-06-30) states BIS issued an interim final rule effective 2025-09-29 extending export restrictions to entities 50% or more owned by Entity List or Military End-User List parties. On 2025-11-11 BIS published a one-year suspension of that rule, currently set to expire 2026-11-09.","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30, https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm","as_of":"2026-06-30","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#5","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q states Cadence settled with BIS and DOJ in July 2025 over export violations that took place between 2015 and 2021; it paid aggregate net penalties and forfeitures of $140.6 million in the quarter ended 2025-09-30, agreed to plead guilty to one count of conspiracy to commit export controls violations, and booked a $128.5 million charge in Q2 2025.","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30, https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm","as_of":"2026-06-30","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#6","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-Q lists supply chain constraints, expanded trade control laws, new or higher tariffs and geopolitical conflicts among factors affecting its global business. Per search-result summaries of the company's filings, Cadence monitors tariffs for their effect on its hardware business and the cost of imported components, and says geopolitical conflicts have not materially limited its ability to develop or support its products or had a material impact on results, financial condition, liquidity or cash flows.","source":"Cadence Design Systems Form 10-Q for period ended 2026-06-30, https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm","as_of":"2026-06-30","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 FY2026 revenue was $1.584B, up 24.2% YoY; non-GAAP EPS $2.11, up 27.9% YoY.","source":"Cadence Reports Second Quarter 2026 Financial Results (Business Wire via Morningstar); 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cdns07272026ex9901.htm","as_of":"2026-07-27","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"IP revenue grew more than 40% YoY in Q2 FY2026, driven by AI, HPC and advanced-node activity.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/ ; BigGo Finance CDNS Q2 2026 earnings call https://finance.biggo.com/news/US_CDNS_2026-07-27","as_of":"2026-07-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"System Design and Analysis (SD&A) revenue rose 37% YoY in Q2 FY2026.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/ ; BigGo Finance https://finance.biggo.com/news/US_CDNS_2026-07-27","as_of":"2026-07-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Core EDA grew 18% YoY in Q2 FY2026, attributed by the source to AI-enhanced digital implementation and sign-off tools; every product group posted double-digit growth.","source":"BigGo Finance, CDNS Q2 2026 earnings call https://finance.biggo.com/news/US_CDNS_2026-07-27 ; Futurum https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","as_of":"2026-07-27","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Hardware (Palladium Z3 / Protium X3) delivered another record quarter in Q2 FY2026 and added 12 new logos; the source says AI and HPC customers treat hardware-assisted verification as a strategic capacity layer.","source":"BigGo Finance, CDNS Q2 2026 earnings call https://finance.biggo.com/news/US_CDNS_2026-07-27 ; Futurum https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","as_of":"2026-07-27","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Backlog reached a record $8.1B (up 27%), with $4.2B expected to convert to revenue within 12 months.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","as_of":"2026-07-29","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 guidance was raised to revenue of $6.26B-$6.34B (about 19% growth at midpoint), non-GAAP EPS $8.05-$8.15, non-GAAP operating margin 43.75%-44.75%, operating cash flow about $2B.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","as_of":"2026-07-29","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"0","claim":"Company guidance assumes export-control exposure stays broadly unchanged; the article does not disclose China revenue share.","source":"Futurum, 'Cadence Q2 FY 2026 Earnings Climb on Agentic AI and Record Backlog' https://futurumgroup.com/insights/cadence-q2-fy-2026-earnings-climb-on-agentic-ai-and-record-backlog/","as_of":"2026-07-29","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Moonshot AI's Kimi K3 model reportedly completed a full semiconductor chip design flow autonomously in a single 48-hour run using only open-source EDA tools, with no licensed Cadence or Synopsys software. Demo chip: 4mm² die, 100MHz, Nangate 45nm Open Cell Library, over 8,700 tokens/s simulated inference throughput, no human intervention. CDNS fell 9.6% on the day and SNPS also fell sharply.","source":"Investing.com, 'Why is Cadence Design Systems stock plummeting today?' https://www.investing.com/news/stock-market-news/why-is-cadence-design-systems-stock-plummeting-today-93CH-4798909","as_of":"2026-07-17","affects":["moat_trend","thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"The same article says analysts noted the 45nm node used in the Kimi K3 demo is several generations behind the 3nm and 2nm nodes where Cadence's tools remain deeply embedded and hard for open-source alternatives to replicate.","source":"Investing.com, 'Why is Cadence Design Systems stock plummeting today?' https://www.investing.com/news/stock-market-news/why-is-cadence-design-systems-stock-plummeting-today-93CH-4798909","as_of":"2026-07-17","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"At TSMC's 2026 Technology Symposium, Cadence announced support for four TSMC nodes (N3, N2, A16, A14), described as the broadest explicit node span among the three vendors' announcements. Siemens EDA's stated approach centers on agentic orchestration rather than broad node coverage.","source":"Futurum Group, 'EDA Vendors Race to Align With TSMC's Angstrom-Era Roadmap at Technology Symposium' https://futurumgroup.com/insights/eda-vendors-race-to-align-with-tsmcs-angstrom-era-roadmap-at-technology-symposium/","as_of":"2026-04-24","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Futurum notes TSMC-COUPE (co-packaged optics) becoming a production technology creates a near-term opening favoring vendors with cross-domain simulation capabilities already in hand. Cadence had not disclosed specific COUPE enablement, which could cede this segment to Synopsys.","source":"Futurum Group, 'EDA Vendors Race to Align With TSMC's Angstrom-Era Roadmap at Technology Symposium' https://futurumgroup.com/insights/eda-vendors-race-to-align-with-tsmcs-angstrom-era-roadmap-at-technology-symposium/","as_of":"2026-04-24","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Cadence VP of Investor Relations Richard Gu (Nasdaq 54th Investor Conference, 2026-06-09) described agentic AI monetization as subscription-plus-consumption: 'The value is commensurate with what a physical human engineer can do. It's definitely not priced like an LLM token. It's worth tens of thousands of dollars.'","source":"TIKR.com, 'Cadence Design Systems Just Unveiled Its Agentic AI Revenue Model...' https://www.tikr.com/blog/cadence-design-systems-just-unveiled-its-agentic-ai-revenue-model-heres-why-it-could-reset-the-stocks-growth-ceiling","as_of":"2026-06-10","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Per the same TIKR write-up of the Nasdaq conference remarks, management confirmed consumption-based agentic AI revenue is excluded from current guidance. It also cited one customer willing to spend 50% of a human engineer's annual cost on AI agent tokens, and framed EDA's share of chip-company R&D budgets as moving from roughly 11-12% toward about 33%. The 33% figure is the company's/article's framing, not an independently verified number.","source":"TIKR.com, 'Cadence Design Systems Just Unveiled Its Agentic AI Revenue Model...' https://www.tikr.com/blog/cadence-design-systems-just-unveiled-its-agentic-ai-revenue-model-heres-why-it-could-reset-the-stocks-growth-ceiling","as_of":"2026-06-10","affects":["thesis.H","valuation","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 earnings call summary: customers keep buying the underlying EDA software and separately buy agent licenses. Revenue comes from both new agentic workflow product licenses and increased consumption of underlying core EDA engines. Management avoided assuming a sudden near-term revenue spike from these tools.","source":"Yahoo Finance, 'Cadence Design Systems, Inc. Q2 2026 Earnings Call Summary' https://finance.yahoo.com/technology/ai/articles/cadence-design-systems-inc-q2-123000589.html","as_of":"2026-07-28","affects":["moat_trend","thesis.H","triggers"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"The Q2 2026 earnings call summary says Cadence's strategy has 'shifted toward becoming a more central partner for hyperscalers and foundries', with deepened collaborations with Intel, Samsung and TSMC. No quantified channel-mix change was disclosed. This is a summarizer's phrasing, not a company-reported change in sales channel.","source":"Yahoo Finance, 'Cadence Design Systems, Inc. Q2 2026 Earnings Call Summary' https://finance.yahoo.com/technology/ai/articles/cadence-design-systems-inc-q2-123000589.html","as_of":"2026-07-28","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 results (reported 2026-07-27): FY2026 revenue guidance raised to $6.26B-$6.34B (about 19% YoY growth at the midpoint), non-GAAP EPS guidance raised to $8.10 (midpoint), operating cash flow guidance raised to about $2B. Simply Wall St describes this as the largest single-quarter guidance increase in the company's history.","source":"Cadence Form 8-K Ex.99.01 https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cdns07272026ex9901.htm ; Simply Wall St News 'Cadence Design Systems (CDNS) Lifts 2026 Outlook, Is The Stock Fully Priced?' (figures taken from search summaries; the 8-K was not opened)","as_of":"2026-07-27","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"At the Q1 2026 report (2026-04-27), Cadence had raised FY2026 revenue growth guidance to about 17% at the midpoint. The Q2 raise to 19% is the second guidance increase in 2026.","source":"Investing.com 'Earnings call transcript: Cadence Design tops Q1 2026 estimates, raises guidance'; Cadence Form 8-K CFO commentary https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000044/cfocommentary04272026ex9902.htm (from search summaries; not opened)","as_of":"2026-04-27","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Guidance vs consensus at the Q2 report: StockStory says the FY2026 revenue guidance midpoint of about $6.3B was 1.5% above analysts' estimates. Q2 revenue was $1.58B vs $1.58B consensus (0.5% beat). Q2 non-GAAP EPS was $2.11, 2.7% above consensus of $2.06.","source":"StockStory 'Cadence Design Systems (NASDAQ:CDNS) Beats Q2 CY2026 Sales Expectations, Full-Year Outlook Slightly Exceeds Expectations' https://stockstory.org/us/stocks/nasdaq/cdns/news/earnings/cadence-design-systems-nasdaqcdns-beats-q2-cy2026-sales-expectations-full-year-outlook-slightly-exceeds-expectations","as_of":"2026-07-27","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Consensus after the Q2 report (S&P Global data shown on StockAnalysis): FY2026 revenue $6.32B (guidance midpoint about $6.30B) and EPS $8.14 (guidance midpoint $8.10). FY2027 revenue $7.17B (+13.43%) and EPS $9.55 (+17.23%).","source":"StockAnalysis.com 'Cadence Design Systems (CDNS) Stock Forecast & Price Targets' https://stockanalysis.com/stocks/cdns/forecast/ (S&P Global data, page shows 'last updated Sep 11, 2026')","as_of":"2026-09-11","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Analyst price target distribution: 27 analysts polled by S&P Global. Average target $403.38, median $405, range $300 (low) to $470 (high). Ratings: 18 Strong Buy, 6 Buy, 2 Hold, 0 Sell, 0 Strong Sell.","source":"StockAnalysis.com 'Cadence Design Systems (CDNS) Stock Forecast & Price Targets' https://stockanalysis.com/stocks/cdns/forecast/","as_of":"2026-09-11","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Recent rating actions: FBN Securities (Shebly Seyrafi) initiated at Buy with $375 target (2026-09-11); Stifel (Ruben Roy) maintained Buy, $432 (2026-08-28); Bank of America (Vivek Arya) reiterated Buy, $420 (2026-08-20); Mizuho (Siti Panigrahi) reiterated Buy (2026-08-03); J.P. Morgan (Harlan Sur) reiterated Buy, $405 (2026-07-29).","source":"StockAnalysis.com 'Cadence Design Systems (CDNS) Stock Forecast & Price Targets' https://stockanalysis.com/stocks/cdns/forecast/","as_of":"2026-09-11","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2025-09-04 Cadence 與 Hexagon Smart Solutions AB 簽訂 definitive agreement，收購 Hexagon 的設計與工程事業，總對價約 €2.70bn（約 70% 現金、30% Cadence 股票，現金部分約 €1.89bn，以手上現金加既有債務額度融資）。","source":"Cadence 新聞稿：Cadence to Acquire Hexagon's Design & Engineering Business — https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-to-acquire-hexagons-design--engineering-business.html ；亦見 CDNS Form 10-Q（期間 2025-09-30）https://www.sec.gov/Archives/edgar/data/813672/000081367225000148/cdns-20250930.htm","as_of":"2025-09-04","affects":["moat_trend","valuation","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Hexagon 設計與工程事業收購於 2026-02-23 完成；Cadence 向 Hexagon Smart Solutions AB 發行 3,224,473 股普通股作為部分對價。","source":"GuruFocus：Cadence Design Systems (CDNS) Completes Strategic Acquisition of Hexagon Smart Solutions AB — https://www.gurufocus.com/news/8642949/cadence-design-systems-cdns-completes-strategic-acquisition-of-hexagon-smart-solutions-ab ；Stock Titan 8-K 摘要 https://www.stocktitan.net/sec-filings/CDNS/8-k-cadence-design-systems-inc-reports-material-event-328ea5d3fcaa.html","as_of":"2026-02-23","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Cadence 對該收購的財務影響指引：預期為 2026 年增加約 $160M 營收、2026 年非 GAAP EPS 稀釋約 $0.28、2027 年轉為增益。（數字取自搜尋摘要，未逐頁核對原文。）","source":"Cadence 新聞稿（同上 cadence.com 連結）及搜尋摘要彙整（GuruFocus／Stock Titan／ts2.tech）","as_of":"2025-09-04","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2025-07-27 Cadence 與美國商務部 BIS 及司法部 DOJ 達成和解，解決 2015–2021 年間的出口違規事項（Cadence 子公司對中國客戶銷售價值合計 $45.3M 的產品與服務，並將相關技術轉給中國第三方，未取得 BIS 授權）；Cadence 於 2025 年前九個月支付 BIS 與 DOJ 合計淨罰款與沒收 $140.6M，和解含持續的稽核與合規義務。","source":"CDNS Form 10-Q（期間 2025-09-30），法律程序／或有事項段 — https://www.sec.gov/Archives/edgar/data/813672/000081367225000148/cdns-20250930.htm","as_of":"2025-07-27","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"-","claim":"2025-05-23 BIS 通知 Cadence：對含中國或中國「軍事終端使用者」為交易一方的 EDA 軟體與技術（ECCN 3D991、3E991）之出口／再出口／境內轉移，改為須申請許可；Cadence 表示正與 BIS 洽談進一步釐清並評估對業務與財務結果的影響。（此事件日期早於近 12 個月窗口起點，列為背景。）","source":"StreetInsider：Cadence Design Systems (CDNS) is engaging with BIS to obtain further clarification on license — https://www.streetinsider.com/Corporate+News/Cadence+Design+Systems+(CDNS)+is+engaging+with+BIS+to+obtain+further+clarification+on+license/24870481.html","as_of":"2025-05-23","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2025-09-04 Cadence 與 Hexagon Smart Solutions AB 簽訂 definitive agreement，收購 Hexagon 設計與工程事業，總對價約 €2.70bn（約 70% 現金、30% Cadence 股票）；2026-02-23 交割完成，發行 3,224,473 股普通股作為部分對價。","source":"Cadence 新聞稿 https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-to-acquire-hexagons-design--engineering-business.html ；GuruFocus https://www.gurufocus.com/news/8642949/cadence-design-systems-cdns-completes-strategic-acquisition-of-hexagon-smart-solutions-ab","as_of":"2026-02-23","affects":["moat_trend","valuation","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"2025-05-23 BIS 通知 Cadence：對含中國或中國「軍事終端使用者」為一方的 EDA 軟體與技術（ECCN 3D991、3E991）之出口／再出口／境內轉移，改為須申請許可。這是出口管制通知，不是產品召回，也不是 FDA warning letter。","source":"StreetInsider：Cadence Design Systems (CDNS) is engaging with BIS to obtain further clarification on license — https://www.streetinsider.com/Corporate+News/Cadence+Design+Systems+(CDNS)+is+engaging+with+BIS+to+obtain+further+clarification+on+license/24870481.html","as_of":"2025-05-23","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"2025-07-27 Cadence 與 BIS 及 DOJ 達成和解，解決 2015–2021 年間出口違規（對中國客戶銷售價值合計 $45.3M，並轉移技術給中國第三方，未取得 BIS 授權）；2025 年前九個月支付合計淨罰款與沒收 $140.6M，含持續稽核與合規義務。此為 DOJ/BIS 執法，不是 SEC 調查。","source":"CDNS Form 10-Q（期間 2025-09-30）法律程序段 — https://www.sec.gov/Archives/edgar/data/813672/000081367225000148/cdns-20250930.htm","as_of":"2025-07-27","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 14 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CDNS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":85.87,"operating_margin_pct":30.82,"fcf_margin_pct":28.64,"rd_intensity_pct":33.02},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CDNS","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"SNPS","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.38,"operating_margin_pct":11.03,"fcf_margin_pct":29.18,"rd_intensity_pct":30.6},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"ARM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":97.54,"operating_margin_pct":17.3,"fcf_margin_pct":28.55,"rd_intensity_pct":57.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"QCOM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":54.23,"operating_margin_pct":23.28,"fcf_margin_pct":23.64,"rd_intensity_pct":22.45},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"688521.SH","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688521.SH"},"note":"quarterly_income_stmt 無資料"}],"subject":"CDNS"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q2_2026_Earnings_Call_20260727.md）

# Q2 2026 Earnings Call
2026-07-27

Q2 2026 Earnings Call
Cadence Design Systems, Inc. | Earnings Calls | 2026-07-27
Operator (Operator)
Ladies and gentlemen, good afternoon. My name is Abby, and I will be your conference operator today.
At this time, I would like to welcome everyone to the Cadence Second Quarter 2026 Earnings
Conference Call. [Operator Instructions] Thank you.
And I will now turn the call over to Richard Gu, Vice President of Investor Relations for Cadence.
Please go ahead.
Richard Gu (Executives)
Thank you, operator. I would like to welcome everyone to our second quarter of 2026 earnings
conference call. I'm joined today by Anirudh Devgan, President and Chief Executive Officer; and John
Wall, Senior Vice President and Chief Financial Officer. The webcast of this call and a copy of today's
prepared remarks will be available on our website, cadence.com.
Today's discussion will contain forward-looking statements, including our outlook on future business
and operating results. Due to risks and uncertainties, actual results may differ materially from those
projected or implied in today's discussion. For information on factors that could cause actual results to
differ, please refer to our SEC filings, including our most recent Forms 10-K and 10-Q, CFO
commentary and today's earnings release. All forward-looking statements during this call are based on
estimates and information available to us as of today, and we disclaim any obligation to update them.
In addition, all financial measures discussed on this call are non-GAAP unless otherwise specified. The
non-GAAP measures should not be considered in isolation from or as a substitute for GAAP results.
Reconciliations of GAAP to non-GAAP measures are included in today's earnings release.
For the Q&A session today, we would ask that you observe a limit of one question only. If time permits,
you can requeue with additional questions.
Now I'll turn the call over to Anirudh.
Anirudh Devgan (Executives)
Thank you, Richard. Good afternoon, everyone, and thank you for joining us today.
I'm very pleased to report that Cadence delivered outstanding financial results for the second quarter of
2026, with all key metrics exceeding our guidance. We exited the quarter with record backlog that was
above our expectations. We are seeing growing demand for our AI-driven solutions across our
expanding customer base. The AI transformation is driving strong broad-based performance across
both design for AI and AI for design fronts. Given the growing business momentum and accelerating
demand, we are raising our guidance for the year to 19% revenue growth and with higher profitability
as we become more central to our customers as a strategic and trusted partner. John will provide more
details on both our Q2 results and the updated financial outlook.
Let me start with the overall environment. Design activity is growing as AI drives exponential design
complexity and a new generation of system architectures spanning hyperscaler infrastructure and

physical AI. Customers are investing aggressively in these opportunities, led by AI and HPC, and we are
also seeing continued signs of improvement across the more traditional analog and consumer verticals.
Chip and system design present demanding engineering challenges that require deterministic physics-
based engines, proprietary silicon correlated data and deep design knowledge. Our Three-Layer Cake
framework uniquely brings these capabilities together with accelerated compute and data at the bottom
layer, physically accurate simulation and optimization solvers in the middle layer and AI agents and
orchestration at the top layer. Agentic AI is a demand accelerator for Cadence as autonomous agents
expand the design exploration space and call our underlying physically accurate engines more often,
creating a durable tailwind that represents a significant long-term TAM expansion opportunity.
We extended our leadership in Agentic AI with AuraStack AI Super Agent, delivering up to 15x higher
productivity and 2x faster time to market for PCB and advanced packaging design. Cadence is now the
only provider with agentic solutions spanning the full electronic system design flow from digital analog
design and verification to advanced packaging and PCB. We see strong early traction across our AI
Super Agent portfolio with initial customer results demonstrating meaningful productivity
improvement and better design outcomes.
Our ChipStack AI Super Agent, enabling higher verification productivity and faster design cycles has
more than 20 customer engagements and is already deployed in production across multiple chip
designs. At COMPUTEX 2026, together with NVIDIA, we introduced the industry's first fully
autonomous virtual AI design engineer, extending ChipStack to even higher levels of autonomy. Early
customer results include more than 40x faster RTL validation, reducing a typical five-week verification
cycle to less than a day on a state-of-the-art advanced node design.
In analog and custom design, ViraStack is seeing strong customer interest with more than 25 customer
engagements, achieving 2x to 10x productivity improvements compared to traditional design flows.
InnoStack is also building momentum as customers adopt Agentic AI for advanced node SoC design.
During the quarter, Rapidus announced a collaboration to integrate the Cadence InnoStack AI Super
Agent into its AI agent design solution, targeting up to a 2x faster design turnaround.
We continue to deepen our strategic partnerships across the ecosystem. We expanded our collaboration
with Intel through a multiyear engagement focused on enabling its 14A process, leveraging our design
IP and agentic AI-based EDA to co-optimize tool flows and methodologies for next-generation HPC and
mobile designs. This agreement is expected to be a meaningful driver of growth over the next few years.
We also deepened our collaboration with Samsung Foundry on 2-nanometer and 3D-IC technologies,
combining our AI-driven flows and design IP to enable next-generation AI, HPC and mobile systems.
Now turning to our businesses. We are pleased that all product groups delivered double-digit year-
over-year growth. Our IP business had an outstanding quarter, growing over 40% year-over-year. AI
performance is increasingly constrained by data movement, memory bandwidth and advanced
packaging. And our differentiated IP portfolio continued to see strong adoption. This was reflected in
the strong demand for our Star IP portfolio in AI and HPC applications, including PCIe, UCIe, HBM
and LPDDR6. We also expanded engagement with leading memory, semiconductor and aerospace
customers. We secured our first-ever Tensilica DSP design win with STMicroelectronics, reinforcing
our strength in automotive and audio applications.
Core EDA grew 18% year-over-year, driven by growing adoption of our AI solutions. Proliferation of our
digital full flow solutions continued, and we saw expanded adoption of Tempus and Certus signoff tools

on leading-edge designs with wins across hyperscalers, top semiconductor companies and startups. We
also expanded our implementation and sign-off footprint at frontier AI companies as well as at a
marquee ASIC silicon vendor, underscoring their differentiated value in enabling the industry's most
advanced designs.
In analog, we had a significant competitive win with Spectre at a leading semiconductor supplier and
our FastSPICE simulator Spectre FX noted several production wins at leading customers. Our
hardware business delivered another record quarter, driven by continued strength in Palladium Z3 and
Protium X3. As designs approach unprecedented scale, hardware-assisted design and verification is
becoming a strategic capacity layer for our customers' AI road map. These customers are designing
some of the most complex chips and systems in the world, and they critically depend on our scalable,
high-performance hardware platforms to realize their designs.
Demand remains especially strong from AI and HPC customers, including hyperscalers and leading
semiconductor companies. We added 12 new logos and saw meaningful expansion with several
marquee AI customers as well as a notable competitive win with a major AI infrastructure provider.
System design and analysis revenue grew 37% year-over-year. As AI system complexity increases,
customers are increasingly turning to our advanced packaging and PCB solutions. Allegro X AI was
adopted by several customers, driven by significant layout design time reduction. With our 3D-IC
technology and collaboration with TSMC's 3D fabric advanced packaging solutions, we are enabling
customers to confidently design cutting-edge silicon for increasingly demanding AI workloads.
In structural simulation, our BETA CAE business had several competitive displacements, while the
integration of recently acquired Hexagon's D&E business is progressing well with key deals closed with
top customers. There is strong customer interest in our integrated full flow that combines our
multiphysics products across the electrical, CFD and structural domains to best address next-
generation system design needs, including in the emerging field of physical AI.
In summary, Q2 was a great quarter for Cadence, and I'm delighted with the continued momentum of
our business. With accelerating design activity, we continue to execute strongly. and our competitive
position has never been better as we lead the transformation to agentic AI in chip and system design.
With that, I will turn it over to John to provide more details on our Q2 results and our updated 2026
outlook.
John Wall (Executives)
Thanks, Anirudh, and good afternoon, everyone. Cadence delivered excellent results for the second
quarter of 2026 with accelerating momentum in AI and broad-based strength across all our businesses.
Robust design activity and customer demand drove 24% year-over-year revenue growth for Q2 with
double-digit growth across all our product groups. With strong execution, we generated Q2 operating
margin of 45.5% and second quarter bookings resulted in a record backlog of $8.1 billion.
Here are some of the financial highlights from the second quarter, starting with the P&L. Total revenue
was $1.584 billion. GAAP operating margin was 28.4%. Non-GAAP operating margin was 45.5%. GAAP
EPS was $1.33, and non-GAAP EPS was $2.11.
Next, turning to the balance sheet and cash flow. Our cash balance was $1.440 billion, while the
principal value of debt outstanding was $2.5 billion. Operating cash flow was $635 million. DSOs were
65 days, and we used $200 million to repurchase Cadence shares.

Before I provide our updated outlook, I'd like to highlight that it contains the useful (sic) [ usual ]
assumption that export control regulations that exist today remain substantially similar for the
remainder of the year. For our updated outlook for 2026, we now expect revenue in the range of $6.260
billion to $6.340 billion. GAAP operating margin in the range of 27.75% to 28.75%, non-GAAP
operating margin in the range of 43.75% to 44.75%; GAAP EPS in the range of $4.76 to $4.86, non-
GAAP EPS in the range of $8.05 to $8.15. Operating cash flow of approximately $2 billion, and we
expect to use approximately 50% of our free cash flow to repurchase Cadence shares in 2026.
For Q3, we expect revenue in the range of $1.595 billion to $1.625 billion. GAAP operating margin in
the range of 27.5% to 28.5%; non-GAAP operating margin in the range of 43.5% to 44.5%, GAAP EPS in
the range of $1.11 to $1.17 and non-GAAP EPS in the range of $2.01 to $2.07. And as usual, we
published a CFO commentary document on our Investor Relations website, which includes our outlook
for additional items as well as further analysis and GAAP to non-GAAP reconciliations.
In conclusion, I'm pleased with our strong first half results and the robust pipeline and momentum
heading into the second half of the year. At the midpoint, we now expect revenue growth of 19%,
operating margin of 44.25%, EPS of $8.10 and operating cash flow of $2 billion for the year.
As always, I'd like to close by thanking our customers, partners and our employees for their continued
support. And with that, operator, we will now take questions.
Operator (Operator)
[Operator Instructions] And our first question comes from the line of Joe Quatrochi with Wells Fargo.
Joseph Quatrochi (Analysts)
Maybe first, just wondered if you could give us any help. You talked about Agentic AI as being a long-
term TAM expansion opportunity. Is there any quantification that you could give us on that TAM at this
point? And maybe how do we think about that as driving EDA as a percent of R&D expense to maybe
higher over time?
Anirudh Devgan (Executives)
Yes. Joe, thanks for the question. So, like we've said before, I mean, the great thing about Agentic AI is
it opens up a new TAM opportunity. At the same time, it calls more of our underlying physically
accurate software. So going back to the three-leg framework. So it's a new opportunity at the top layer
and reinforces the middle layer. And I think we are pleased by the interest. I mean the interest is
amazing, actually, almost all the big customers, almost all customers want to engage in our agent stack.
And now we have four super agents. So I think it's a great opportunity for us.
Now in terms of results, what I -- of course, we had great results in Q2 and the year so far, and there's a
lot of strength in different parts of the business. But what I'm particularly proud of is the strength in the
software businesses, if you look at our recurring growth, and that was particularly driven by strength of
add-on business. And so both -- we are seeing add-ons driven both basically for design for AI as our
customers design more chips and also AI for design, which is our Agentic and AI portfolio. And you can
see that in our results.
So, what is particularly impressive, and this is, I think, the highest raise we ever had is that it is broad-
based, including software and AI contributing to that growth. So we'll see how things progress for rest
of the year.

John Wall (Executives)
Yes, Joe, I'll just add that like -- if I could just add, the customer engagement, as Anirudh said,
continues to accelerate. We're seeing increased evaluations and pilots and early deployments. And we
continue to expect monetization through both new workflow products as well as increased usage of
underlying engines. But just to be clear, we're still not assuming a sudden step function in our
guidance. The opportunity is continuing to develop well though.
Operator (Operator)
And our next question comes from the line of Joe Vruwink with Baird.
Joseph Vruwink (Analysts)
Staying on this topic, I wanted to ask about open source models designing chips. And maybe if I just
take Kimi at face value, it seems like an agent sought out EDA tools and then orchestrated the flow
when tasked with chip design. So I guess my question is the implication for Cadence from all of this and
two things come to mind. One, if customers now have agents capable of accessing your EDA tools, does
that drive higher usage and more net consumption ultimately? And then two, where do you think the
differentiation lies with a customer buying the Cadence mental models for orchestration versus
customers maybe deciding to build on their own?
Anirudh Devgan (Executives)
Yes. Thanks for the question. I mean, like I said before, I've said this for years now, like four, five years
that the real AI orchestration and monetization will happen through this Three-Layer Cake. Just to
remind everybody, the top layer is AI agents and orchestration, the middle layer is these -- our
traditional physically accurate tools, ground truth and bottom layer is compute and data. So the recent
news just confirms that framework. And by the way, this will happen in all markets. The value of AI will
go more and more vertical than horizontal and I've said this for a long time.
So even in chip design, the value is in the Agentic framework and all the mental model, all the
knowledge graphs, then calling the physically accurate tools on a rich set of hardware. And this latest
news in case of Kimi doing that, I mean, I think that the -- I mean, they said a chip, but I think it's a
small block, which is about technology, which is like 20 years old on frequency that is 20, 30x lower
than current frequency. So even to design a small block at such an old node, they needed kind of EDA
tools to do that. So this is going to happen again and again. And there is -- there have been open source
EDA tools for a while, I don't know, for decades, and they're used in some university or specialized
settings. But to really do real designs, people use Cadence to do that.
Now the differentiation will be in all three. We want to differentiate in all three parts of the cake. So our
Knowledge Graph and our mental model and how we do the reinforcement loops at the agents is really
differentiated. How we call then the middle layer through deep API access and the strength of our
middle traditional tools is differentiated. And then even in the bottom layer, as you know, we have
Palladium, we have Millennium, we have special hardware to do that. So our differentiation will be in
all three. And then all three together, we are more differentiated than we have ever been. So I'm very
proud of our differentiation of the moat we have. And then the fact that these three layers will reinforce
each other.

Now the customers may always have their own agents, just like they have their own flows right now.
But to really do mission-critical tasks, they increasingly depend on Cadence as you're seeing that in our
engagements.
John Wall (Executives)
Yes. Joe, Anirudh has always said that like Agentic AI actually increases demand because agents invoke
EDA tools continuously while exploring more design alternatives and Kimi was a really good example
of that.
Operator (Operator)
And our next question comes from the line of Vivek Arya with Bank of America Securities.
Vivek Arya (Analysts)
I know the IP business has accelerated to over 40% growth. I'm curious what's driving this? How much
is organic versus inorganic? And what is kind of the sustainable growth rate for IP? And then if we
zoom out, I just wanted to clarify with John, what the contribution is now with Hexagon and the EPS
dilution.
Anirudh Devgan (Executives)
Yes. John, do you want to start on that?
John Wall (Executives)
Yes, sure, sure. Just in terms of Hexagon contribution, I mean, Hexagon is delivering as we originally
expected, and it continues to contribute to SD&A growth, but the strength in our SD&A numbers is
much broader. We're seeing momentum in 3D-IC in advanced packaging, in PCB, multiphysics and
physical AI. And the integration of Hexagon D&E is progressing well, and we see a significant
opportunity to strengthen both the technology portfolio and go-to-market over time.
But yes, also, I guess, on the IP side, IP had an outstanding quarter, driven by AI, HPC, advanced node
activity, memory bandwidth, chiplets and advanced packaging. There were strong customer
engagements and meaningful wins, but IP revenue can be timing dependent from quarter-to-quarter.
We're pleased with the momentum, but I wouldn't annualize any one quarter. Our competitive position
continues strengthening across interface IP, memory IP and foundation IP. Intel, as Anirudh called out,
it represents another example of customers choosing broader strategic engagement with us.
Anirudh, would you like to add?
Anirudh Devgan (Executives)
Yes, absolutely. Yes. Thanks, John. So, Vivek, very pleased with the IP performance and SDA
performance. I mean before I get into specific IP, the good thing is, I mean, these things are growing. Of
course, IP is growing very well. SD&A is growing very well, but also they have enough scale now. So,
EDA, we are always I believe, the leading EDA provider with analog, digital verification, packaging, 3D-
IC. But both our -- roughly speaking, both IP and SD&A are approaching like $1 billion run rate, okay?
So at this point, it gives a lot of strength in our portfolio to engage with our customers.

Now IP, particularly -- and I've mentioned this before, as you know, like I think there are three big
megatrends. One is, of course, our IP is much better than before. The quality of our IP, the PPA, power
performance in area for like TSMC and the leading nodes is better. So we are getting a lot of
competitive wins in IP that two years ago, we would not participate in. So that's one thing. Second
reason is our IP strategy is more focused, has always been focused and will continue to be focused to
leading nodes to star IP to AI and HPC segments.
So I've talked about these five key IPs, which interface IP, memory IP. And then we have expanded to
foundation and other, but this especially chip-to-chip IP, memory IP, interface IPs are super critical,
and they are growing well, okay? And then the third thing is, there are more and more foundries we
talked about Intel. I'm very proud of this new partnership with Intel and it's, of course, much broader
than IP, but IP is a part of it. And then our engagement with Samsung, we mentioned last quarter and
Rapidus. So the foundry ecosystem is much more diverse than before.
So I think these three reasons, our IP business is doing phenomenal. And also, most of it is, just to
clarify, is organic growth. I mean this great growth we posted, most of it is organic growth. Now how
does it proceed in the future, we'll see, but all the signs are positive at this time.
Operator (Operator)
And our next question comes from the line of Siti Panigrahi with Mizuho.
Sitikantha Panigrahi (Analysts)
Apologies for the background noise. I'm at DAC conference. And I can tell you the key theme here is
Agentic AI, which kind of validated what you said. So my key question is, you talked about some of this
agent, Super Agent, ChipStack, ViraStack that your customers has been using. So wondering what kind
of feedback you are getting and the cost saving and the value that you bring to the customer?
And then I know, John, earlier, you talked about monetization, which might take contract renewal or
cycle time. But as you see the usage, are you seeing any kind of accelerating adoption where the time
line can be compressed?
Anirudh Devgan (Executives)
Yes, Siti, the demand is great, like I mentioned, for these agents. And we have -- I mean, the exciting
thing is that the use cases are -- I mean, we have publicly talked about so many of them and like 2x to
10x to, in some cases, 40x improvement. And this is only the ones that we can publicly talk about. This
is a very small subset of our engagement. So the amount of use cases and the benefit is real, okay? And
the interest is definitely real in terms of number of engagements and how many customers want to
engage with us. And our strength of our portfolio with the Three-Layer Cake is very well differentiated.
So I'm very pleased. I mean this is like we are maybe six months into our launch of these products. We
launched them in Q1, but we're working, I would say, roughly six months with our customers. And we'll
see how it progresses. But like I said, the early add-on business is encouraging, but we have to -- still in
the early days. So we'll see how it goes. But so far, the demand is tremendous.
John Wall (Executives)
Yes, Siti, I think we view this as a demand accelerator. Customers are not trying to do any less design
work. They're trying to keep up with design complexity, which is accelerating faster than engineering

headcount and scale. We've always said that. As agents expand the design exploration space and call the
underlying cadence engines more often, that creates opportunities for new Agentic workflow products
and increased use of our core tools.
Operator (Operator)
And our next question comes from the line of Jim Schneider with Goldman Sachs.
James Schneider (Analysts)
Continuing on the Agentic AI theme, could you maybe talk a little bit about some of the add-on
engagements you're seeing for those tools? And to what extent you're seeing them across more than the
sort of 20 to 25 customers you've already noted. And maybe if you could quantify the impact of those
add-ons in terms of either the guidance raise or what it could mean for core EDA software revenue in
the next year, that would be great.
Anirudh Devgan (Executives)
Yes. I think like you know us, right, we are very careful about projecting future, next year numbers. But
I think to step back a little bit, I think the three things that I'm super excited about is, one is that the
overall environment is much better. I mean this also helps us a lot. I mean not just the AI companies,
the hyperscalers are -- I mean the commitment to silicon is much higher than like 12 months ago. And
you can see that you're following all the hyperscalers. So the amount of designs and the number of
designs each hyperscaler is doing is impressive.
And then the AI semi companies are growing immensely. And then like the analog and memory and the
consumer semi companies are also doing well now. So overall environment is much better than one
year ago, which, of course, helps us, right? So that's number one. Number two, I think I just want to
emphasize our competitive position, I feel, has never been better. So we are taking a lot of share in
different customers, getting to much, much deeper engagements, whether it's Agentic AI or hardware
or IP. And you can see that in the numbers. And then the third part is this new TAM expansion
opportunity, which is Agentic, which we are clearly super excited about. We're still in the early stages.
So if you combine those three things, I think that is what is leading to such good results and such good
guidance. Just to remind you, this is the highest we have raised annual revenue in a single quarter,
okay, and to about 19% revenue growth with improved profitability.
So I think I would like to say that some of the benefit is already there of the Agentic and other next year
and year after, I mean, you know us, we are prudent as ever, and we'll see how things progress.
John Wall (Executives)
Yes. Jim, I think just -- I know we get a lot of questions about Agentic AI, but I think it's important to
highlight that the raise that we just did for Q2 for the rest of the year reflects broad-based strength
across the business rather than any single customer or product. We saw strong Q2 execution across
core EDA, IP, hardware and SD&A. That, of course, is all benefiting from continued strength in AI-
driven demand as well. But the strength is broad-based across all businesses and across all regions.
Operator (Operator)
And our next question comes from the line of Harlan Sur with JPMorgan.

Harlan Sur (Analysts)
Anirudh, as the volume of AI inferencing compute workloads surpassed training workloads in the
second half of last year. And we know that inferencing is much more memory intensive, right? So we've
seen this diversification of different types of memory architectures emerging to address inferencing. In
addition to HBM DRAM, we've seen development of SRAM-based offload architectures. We've seen
CXL-based conventional DRAM offload and even using enterprise SSD or flash-based memory, right?
So given all of the focus on these memory architectures and memory controller architectures, is this
translating into some tailwinds for your custom Virtuoso family of EDA tool solutions or tailwinds for
your CXL-based or memory compiler IP portfolios or both?
Anirudh Devgan (Executives)
Yes, Harlan, that's a great point. So yes, like John mentioned, the strength is broad-based. And
definitely, the analog group, which is part of EDA, is also seeing very strong momentum because all of
these -- whether it's memory or analog is all done and Virtuoso is the leading platform for analog and
mixed signal and custom design in the industry. So I'm very pleased to see overall environment plus the
special -- all this innovation that is driven by inferencing, helping both all our businesses, analog,
digital and verification.
But what is exciting to me in this -- I mean, you know this anyway, with this inferencing is that there is
much more varied architectures you mentioned and also much more varied customers. So all the big
customers believe at this point that, of course, they will use standard products from semiconductor
companies, from the really big semiconductor companies like NVIDIA, who are doing great, but also
believe that they will have their own custom silicon. And then on top of that, different versions of that
custom silicon for memory access and also networking, right? There's a lot of activity in networking as
well. And then I would say, like over the last six months, I see a lot more activity in start-ups. Start-ups
were kind of dormant. But in the last six months, there are like some very high-profile start-ups that are
starting, not just in AI, but in networking and even CPU, right?
So I think the overall environment is good, and it is affecting all our businesses. Analog for sure,
verification with hardware, IP business, digital implementation, 3D-IC is a big thing where we have
leadership. So that's what leading to this broad-based trend. But the conviction of the hyperscalers to
do their own silicon and try, like you pointed out, different architectures, and that's bound to happen. I
mean if there is one bottleneck, the customers come up with different memory architectures to solve
that bottleneck or different networking architecture.
So I expect this to continue. I mean this is -- as the market gets bigger, you know that, as the AI
infrastructure market gets bigger, there will be more and more innovation to optimize each part of that
market. And all that innovation will require Cadence products to make that happen.
Operator (Operator)
And the next question comes from the line of Charles Shi with Needham & Company.
Yu Shi (Analysts)
Anirudh, I can ask about AI for 100 ways, but I think the most important question top of many people's
mind right now or I should say, the scenario, a very extreme scenario that people fear about the most is
where you actually prompt, I don't know when we could get that, but prompt on a very, very powerful

LLM in the future with your chip design requirement, then that LLM can autonomously generate GDSII
codes that get sent to foundry directly for tape-out without running them through any of the
commercial EDA tools. So this is one of the scenarios that some people were envisioning. We strongly
disagree, but do you think this end-to-end, so-called end-to-end LLM-based chip design is a real
possibility after all -- at all or since you mentioned the Three-Layer Cake.
Anirudh Devgan (Executives)
Yes, Charles, I mean, like I said -- I mean, before, I said this for years, the way this improvement will
happen and of course, there will be a lot of improvements with AI, will be through this Three-Layer
Cake. So we will have agents like we have Super Agents. Our tools are central, will continue to be
central to that. And of course, we'll run on a varied set of hardware. I don't see that changing. Of course,
some people may get worried about it from time to time. But the ground truth will prevail, okay? This
Three-Layer framework will prevail.
And what -- if you talk about commoditization, I mean, I think what is likely to happen is not the EDA
tools get commoditized. What is likely to happen is at the Agentic layer, there will be a lot of choices for
LLM. So if you look at what is really happening right now in the marketplace is that the customers are
demanding choice in their LLMs. And so -- which is Kimi is an example of that and GLM 5.2 and
Nemotron, of course, great release by NVIDIA and then all the commercial models. So what the
customers are asking me is like, can you -- can the agent be more intelligent in choosing the right model
for the right task given the rapid progress in the LLMs. I think that's most likely to happen. But the
Three-Layer framework, criticality of our tools will be here to stay.
Operator (Operator)
And our next question comes from the line of Lee Simpson with Morgan Stanley.
Lee Simpson (Analysts)
I mean I think most of my questions have been asked, but maybe I'll ask a generic sort of competitive
one. It does look as though Cadence has expanded DTCO collaborations now with Intel, building out its
Samsung road map and you've also deepened relationships with TSMC. So your positioning in stack die
and multichip designs is pretty much equal or better relative to peers, you'd say now. So its exposure to
digital design and IP interface maybe differs from Synopsys.
So I guess the question here is really, where are you seeing the most competitive pressure from some of
your peers in contested accounts? And is the -- and in the context of some of the other Agentic AI push
at your rivals, are you winning or losing share in that digital implementation and verification at the
leading edge?
Anirudh Devgan (Executives)
Yes. Thanks for the question, Lee. So first thing, I just want to say that I'm very proud of this new Intel
collaboration because Intel is a company we tried to work closer for a very long time. I mean this is not
a 1- or 2-year-old problem. This is like a 10- or 20-year-old problem, okay? So -- but finally, we have a
great collaboration with Intel, with Lip-Bu and his new team. And I think we are working on it for a
while now, but it's good to announce it in Q2. And it's a pretty broad-based collaboration, of course,
starting with what we had announced a month or two ago, 14A and DTCO, our Agentic EDA solutions,

our IP portfolio, which is much stronger. But I think it goes beyond that. And you'll see that we are
engaging Intel in all parts of Intel with all parts of our product portfolio. So I'm really pleased to see our
position improving at Intel and our collaboration being just like it is in all the other leading companies.
And same thing happened with Samsung over the last 6 to 12 months.
So in terms of what we were weak at before a few years ago was, we were doing great with the TSMC
ecosystem, we have a great partnership with TSMC, but I've said for a while, we were weak at Intel and
Samsung, and that definitely has changed. And there's still more to go, but at least the trajectory has
definitely changed, in my opinion. And then -- and especially -- and that especially applies to digital
and verification businesses. And even in digital, we are always very, very strong in implementation,
place and route. But now as we had mentioned in my prepared remarks, also strong in sign-off. So the
depth of our digital engagement is also improving at all customers.
So, overall, I'm pretty pleased with our position. And we just always believe in simple things, right,
team, technology and customers. We have the best team, I believe, develop the best products and listen
to these demanding customers, and that's how we stay ahead. We're not looking at who is doing -- who
else is doing that, but are we really satisfying the demanding workload of our customers, and I believe
right now, we are in a great position.
Operator (Operator)
And our next question comes from the line of Jason Celino with KeyBanc Capital Markets.
Jason Celino (Analysts)
Great to hear another record hardware quarter. I know, John, you kind of mentioned this is always as a
pipeline business and you kind of wait to the middle of the year to get better visibility for the second
half. But maybe can you speak to the type of demand activity you are seeing for hardware? I did notice
that inventory ticked up nicely in the second quarter, both on a year-over-year and a quarter-over-
quarter basis.
John Wall (Executives)
Yes. Great question, Jason. Yes, we continue to see strong hardware demand, particularly from AI and
HPC customers. Hardware-assisted verification is becoming a strategic capacity layer for customers
designing the most complex chips and systems. There could be quarterly timing effects, but demand
remains solid, and we continue to expect 2026 to be another record hardware year. And I would profile
hardware is that it still remains supply constrained by customer demand rather than demand
constrained. And we're building the systems as quickly as we can to deliver against the backlog. And
yes, part of the increase was for the year was due to hardware strength, but we are seeing strength right
across the board.
Operator (Operator)
And our next question comes from the line of Gianmarco Conti with Deutsche Bank.
Gianmarco Conti (Analysts)
So yes, amazing performance on IP. Maybe if you could share a few more words on Intel win, exactly
what does that entail? What parts of the portfolio? Was that displacement? How big is roughly the

contract meant to draw down over how much time? And is this in guide? Just kind of like the layout on
the details, if you could share any of that, please?
Anirudh Devgan (Executives)
Sure. I can comment a little bit more. I mean -- but this is a multiyear arrangement. And of course,
some of the benefit is this year, but most of it is to come, okay? And then we will also invest more, right,
in Intel and Intel customers, which is to be expected.
But in terms of IP, I mean, it's much broader than IP because it includes EDA and DTCO. But in terms
of IP, we have a pretty good portfolio, so we will make that available on Intel process. Now this doesn't
include as Intel Foundry gets more customers, they're buying IP from us. This is just our arrangement
with Intel right now, as you know we are always conservative in those projections. But still, I mean,
Intel Foundry is, as you know, talking to a lot of customers. So it's a possibility those customers will
acquire these IPs and any differentiated tools that come out from this DTCO. So we will see how it goes.
But IP strength is, of course, Intel is a part of it, but it's much more broad-based.
And even our overall strength, I think I want to highlight and John already mentioned, is not coming
from one particular thing. So I mean there are four or five things that are driving this raised outlook. So
Intel is one of them for sure. IP is one of them. Hardware is a key focus, but it's hardware -- if you look
at our recurring growth is very good, right? So hardware is important growth, but so is EDA and
Agentic solutions and 3D-IC and SD&A. So I feel right now, there are like four or five engines that are
driving our growth. But we are definitely very proud of the Intel agreement and the new partnership.
John Wall (Executives)
Gianmarco, I know your question is primarily around revenue and things like that. But I want to
highlight that there is some kind of expense in the second half as well because we're investing around
these opportunities like Intel as well as trying to integrate Hexagon's D&E business because we're very
focused on improving margins for next year.
So you'll notice that the second half is kind of slightly lower margins than the first half, but that's a
reflection of our -- of us making targeted investments. These are deliberate investments and not a
deterioration in the underlying model by any means. It's this organic -- our organic incremental
margins remain very attractive. And we expect kind of acquisition profitability and profitability of IP to
continue to improve as we go into 2027.
Operator (Operator)
And our next question comes from the line of Ruben Roy with Stifel.
Ruben Roy (Analysts)
John, I think you just answered my question. So let me just make sure I understand that. So yes, I was
looking at the implied operating margin near 43% and expenses -- R&D expense is up probably 19%
year-over-year based on implied guidance for the full year versus around 10% growth last year. Of
course, Hexagon accounts for a part of that. But I guess, how much of this is sort of the core business?
And I guess I was thinking through Agentic AI and go-to-market. Is that sort of hiring you're already
committed to? Is that driving some of the expense increase? And how do you expect that to roll into
2027?

John Wall (Executives)
Yes. It's not just hiring, but it's investment in systems and everything that -- we're trying to invest
heavily in making sure we do a full and proper integration of Hexagon's design and engineering
business as well as some of the other businesses, the smaller businesses that we've pulled into System
Design and Analysis. But -- and we're very focused on that in the second half of this year. I think I
highlighted it last year that we had, I think, $20 million, $25 million set aside specifically for
investments in the second half of the year.
Now there's always some prudence in our expense expectations. Anirudh and I always want to give the
team enough scope to be able to invest and capture the increased profitability opportunities that they
can get. But our focus is really on -- in the second half of this year to grab those opportunities and set
ourselves up so that we have better operating margins next year.
Operator (Operator)
And our next question comes from the line of Kelsey Chia with Citi.
Wei Chia (Analysts)
So regarding Intel, is the engagement around 14A more likely an incremental driver to the sort of 20%,
25% growth that the team has been delivering for the IP business? And also, will it be a meaningful
driver to your EDA business in the coming quarters? Or how long should we think about that trajectory
as they're [indiscernible] your EDA business?
Anirudh Devgan (Executives)
Yes, I mean, just to make sure I understand the question. I think the Intel business that we announced
is all incremental to our business, 100% because we already had existing Intel agreement. So this one is
a new agreement on top of that and it's a multiyear agreement with multiple parts of that business. And
then I'm also -- and I think Lip-Bu has said that publicly also, I mean, we announced 14A, but I think
Intel to be successful in the foundry business has to do more than 14A. So we are already talking to
them other future road map of Intel Foundry. And then, of course, there is different parts of Intel, as
you know, the product groups and they're investing in their server business and their client business.
So again, we are proud to be working with Intel closely and just like we work with other big customers.
So I think it's more a normalization of our relationship with Intel, like we work with all the other
household names you know. So I'm very proud of this development.
Operator (Operator)
And our next question comes from the line of Jay Vleeschhouwer with Griffin Securities.
Jay Vleeschhouwer (Analysts)
Anirudh, I'd like to ask you about the practical implications of or requirements for implementing AI
and agents and all that you've spoken of this evening. That is to say, when you think about the presale
and post-sale support and customer support that you have to provide, how would that compare to, let's
say, what you used to have to do for classical EDA? Is there something quantitatively or qualitatively or
technically different now that you need to do that you hadn't had to do before?

And what I have in mind, for example, is that over the last few months, there's been a very clear
uptrend in your AE openings. It's a classic leading indicator for customer adoption. You've also said
that Gen AI is on quote, "the critical path for Agentic adoption." So maybe you could talk about that as
well.
Anirudh Devgan (Executives)
Yes. Thanks, Jay, for that question. That's a great question. I mean, in general, of course, we are
growing. So we will invest, right, both in R&D and application engineering. Agentic AI, it does not
require some massive step increase in investment. I just want to be clear about that. It is more of our
traditional business because we are, of course, very, very asset-light, right? We don't -- we're not
building compute forms. All this is done by our customers, okay, just to be clear.
Now of course, some of the skills are different, but our team anyway is expert in computational
software, as you know, and they can pick up Agentic AI. Some hiring, we will do. So it's more of a
business as usual, I will say. And also, we can make AI -- there are implications that we have not -- we
are applying a lot of AI internally, okay, to make things even more efficient. So, for example, AEs, yes,
we are hiring AEs, but AI can dramatically reduce AI workload and make them much more productive.
So then more of the AEs can participate in presales activity rather than post-sales support, right? And
same thing in R&D, of course, we are deploying AI for software development. And of course, AI --
deploying our agent stack and all our agents for IP development to make them more efficient. So -- and
this is what John was saying earlier. So we'll see how that progresses.
I think AI has the opportunity to even reduce our cost in some cases. But we are not -- you should not
model in some massive investment. I think the investment we talked about is more for SD&A, right, for
the integration. And you have always talked about, Jay, that how we need to have a full flow. And I feel
that finally, we have a full flow in SD&A. So investing in that, investing in Intel. But the Agentic AI will
go through our regular sales motion and regular AI and R&D support.
Operator (Operator)
And our next question comes from the line of Joshua Tilton with Wolfe Research.
Joshua Tilton (Analysts)
Maybe just one clarification and one thematic question for Anirudh. On the clarification side, could you
just maybe unpack for us what's driving the strength in other recurring revenue that kind of stood out
to us this quarter? And any commentary there would be helpful. And then maybe on the thematic side,
Anirudh, unless I misheard you, in your prepared remarks in the beginning, you talked about becoming
more of a strategic partner for your customers.
The question is for you, but John, feel free to jump in here. Maybe like help us as financial analysts like
understand what that means from a business perspective? Like are you growing wallet share? Are you
taking more -- are you able to charge more? Like how are you as a company capturing value financially
because you are now becoming more of a strategic partner to your customers, if that makes sense.
John Wall (Executives)
Shall I start, Anirudh, with just -- so Josh, I'll take the recurring revenue question. I mean recurring
revenue grew about 24% year-over-year in Q2, and that was driven primarily by strong core EDA

growth, some AI-driven demand, share gains and healthy renewals and expansions through add-on
business. Within that, probably Hexagon contributed roughly 4 points. But even adjusting for that,
recurring revenue is like high teens to 20% on a normalized pro forma basis, which we view as a very
strong result. And we also -- we would continue to expect the full year mix to be roughly 80% recurring
and 20% upfront.
On the Agentic AI stuff, that's essentially like when you look at the way we sell that, first of all,
customers continue purchasing our underlying EDA software. And then what they do is they purchase
Cadence agent licenses that orchestrate engineering workflows. so generally, our economics scale with
customer adoptions.
Anirudh, would you like to add to address the rest of Josh's question?
Anirudh Devgan (Executives)
Yes. I think, Josh, what we are saying is that, I mean, we were always strategic to our semiconductor
customers, right? Of course, we are part of engineering. We're part of R&D, right? I mean we are not
like other kinds of -- enterprise kind of software, this is engineering software. So we are central to them
making their products and their revenue.
I think what has happened lately over the last, let's say, one year is even in semi companies, our
engagement is at a much higher level in the company because EDA and chip design and Agentic AI
opportunities are very meaningful to our customers. As there's more demanding road map as Moore's
Law is kind of slowing down, this is well known, not producing enough improvement. So the
improvement has to come with design efficiency, better optimization, better use of AI agents and also
the middle layer, right, the PPA provided by -- and we do this with the foundries and with the
customers and DTCO is part of it for better optimization of power and performance area than was
possible if Moore's Law was delivering -- was really moving fast.
Right now, it has slowed down. So that's on the semi side. And on the system side, I think the
realization that semiconductor is essential has happened now in the last 6 to 12 months or so. So all the
MAG 7 companies, all the big really household norms, silicon is a critical part of their road map. So
therefore, Cadence engagement is super critical at these customers. And the way to monetize that is we
provide more value to them and then we can get more value for us as you see in our results.
Operator (Operator)
And our final question comes from the line of Gary Mobley with StoneX.
Gary Mobley (Analysts)
This maybe a question more for John. One thing that stands out is what appears to be about a 55%
increase in your bookings in the first half of the year versus the same period last year. And I assume
you're going to build on what is normally a seasonally strong second half of the year. And I thought this
was a low renewal period for some more substantial customers. So maybe if you can speak to what's
driving that bookings strength? Is it a reflection of the strength of the chip cycle? Is it the strength of --
a function of the strong chip design activity? Or is it a function of some of the AI tools driving
increasing usage of more copies of classic EDA tools?
John Wall (Executives)

Sure, Gary. I mean it's a great question. I think Anirudh spoke to it a little bit there to Josh's question.
But I mean we've been -- we always say it's strategy first, right? I mean we've been continuing to
execute against our intelligent system design strategy. Anirudh has mapped that out for us for the last
decade or so. But the -- and what we're seeing is that all the underlying like structural demand drivers
continue to strengthen the semiconductor complexity, AI infrastructure investment, engineering
productivity, physical AI, agentic workflows, all of those trends seem to still be in their early stages. And
I think that's feeding into really solid bookings for us. And this year is probably one of the low years
when you look at the kind of a three-year cycle on renewals. This year is kind of probably one of the
lower of the three years that -- but we're seeing very, very good strength in add-on opportunities, as
Anirudh mentioned earlier in the call. I'm very, very pleased with progress and how things are going.
Anirudh, anything to add?
Anirudh Devgan (Executives)
No, John, that's a great summary. I mean, like John said, Gary, that, yes, this year is a low bookings
year. And also normally, first half, we draw down on our backlog, but this year has been good growth.
So we'll see how that progresses. But we are very pleased. And like John mentioned, the environment is
good.
And I'd just like to point out that I feel the three big reasons are like John was also saying the
environment is great, both like the AI -- new AI comers, the traditional AI and the regular companies.
Our products and competitive position is fabulous. And then this new TAM opportunity with Agentic
AI. So if you combine all these three things, I mean, the first half has been great. It sets up nicely for
rest of the year, and then we'll see how things progress, right?
Operator (Operator)
And I would now like to turn the call back over to Mr. Anirudh Devgan for closing remarks.
Anirudh Devgan (Executives)
Yes. Thank you all for joining us this afternoon. It's an exciting time for Cadence as we enter the second
half of 2026 with AI-driven product leadership and strong business momentum.
On behalf of our employees and our Board of Directors, we thank our customers, partners and investors
for their continued trust and confidence in Cadence.
Operator (Operator)
And ladies and gentlemen, thank you for participating in today's Cadence Second Quarter 2026
Earnings Conference Call. This concludes today's call, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CDNS_Q1_2026_Earnings_Call_20260427.md
- 2026-04-27｜CEO｜guidance：CEO 說 2026 營收成長展望上調到 17%（原話："we are raising our 2026 revenue growth outlook to 17%"）
- 2026-04-27｜CEO｜guidance：CEO 說預期首次達成 Rule of 60（同一句前半為上調 17% 展望）（原話："60 for the first time"）
- 2026-04-27｜CFO｜guidance：CFO 給 2026 全年營收區間 $6.125B–$6.225B（原話："revenue in the range of $6.125 billion to $6.225 billion"）
- 2026-04-27｜CFO｜guidance：CFO 給 2026 全年 non-GAAP 營業利益率 43.5%–44.5%（標籤在前一行）與 GAAP EPS $4.39–$4.49（原話："43.5% to 44.5%. GAAP EPS in the range of $4.39 to $4.49."）
- 2026-04-27｜CFO｜guidance：CFO 給 2026 全年 non-GAAP EPS 區間下緣 $7.85（上緣 $7.95 在下一行）（原話："Non-GAAP EPS in the range of $7.85 to"）
- 2026-04-27｜CFO｜guidance：CFO 給 Q2 營收區間 $1.555B–$1.595B（原話："revenue in the range of $1.555 billion to $1.595 billion"）
- 2026-04-27｜CFO｜risk：CFO 說財測含出口管制維持與現況大致相同的常規假設（原話："regulations that exist today remain substantially similar"）
- 2026-04-27｜CEO｜guidance：CEO 說 $8B 記錄積壓訂單優於計畫（原話："Our record backlog of $8 billion was ahead of plan"）
- 2026-04-27｜CFO｜guidance：CFO 說 Q1 訂單優於預期（原話："First quarter bookings were ahead of expectations"）
- 2026-04-27｜CFO｜margin：CFO 報 Q1 non-GAAP 營業利益率 44.7%（原話："Non-GAAP operating margin was 44.7%"）
- 2026-04-27｜CFO｜guidance：CFO 說 Hexagon 設計與工程事業今年貢獻約 $160M 營收，已在財測內（原話："we expect $160 million of revenue this year"）
- 2026-04-27｜CFO｜margin：CFO 說 Hexagon 預期對 2026 EPS 稀釋約 $0.28（原話："We expect it to be dilutive to the tune of about $0.28"）
- 2026-04-27｜CFO｜margin：CFO 說 Hexagon $160M 營收的利潤率影響落在 5%–10% 區間（前文為 margin impact on the $160 million）（原話："in the 5% to 10% range"）
- 2026-04-27｜CFO｜capital_allocation：CFO 解釋 Hexagon 稀釋主因：收購價 30% 以股票、70% 以現金支付，損失利息收入（原話："because we paid 30% of the acquisition price in"）
- 2026-04-27｜CFO｜commitment：CFO 預期 Hexagon 2027 年轉為增益（原話："We'd expect it to be accretive in 2027."）
- 2026-04-27｜CFO｜margin：CFO 把 2026 定位為整合年（原話："2026 is an integration year"）
- 2026-04-27｜CFO｜margin：CFO 說營收上調、但 EPS 與營業利益率低於二月財測（原話："while EPS and operating margin are lower"）
- 2026-04-27｜CFO｜margin：CFO 說 Q1 Hexagon 約貢獻 $20M 營收，EPS 稀釋僅約 $0.01（前後句）（原話："we had about $20 million of revenue from Q1 from Hexagon"）
- 2026-04-27｜CFO｜margin：CFO 說有機成長的增量利潤率（organic incremental margin）接近 60%（原話："margin, it's closer to 60% these days than 50%"）
- 2026-04-27｜CFO｜margin：CFO 說併購案通常要 12 到 18 個月才把獲利拉近公司預期（原話："takes us 12 to 18 months to improve the profitability"）
- 2026-04-27｜CFO｜commitment：CFO 預期 Hexagon 在 26／27 年重演 BETA 收購後的利潤率先稀釋再改善模式（原話："a similar pattern for '26 and '27 when it comes to Hexagon"）
- 2026-04-27｜CFO｜guidance：CFO 說扣除 Hexagon 後，全年營收在中點上調 $65M（原話："raising the year by $65 million at the midpoint for revenue"）
- 2026-04-27｜CFO｜guidance：CFO 說營運現金流財測含約 $180M Hexagon 收購前稅負，會計上歸類為營運現金流（原話："$180 million of preclose Hexagon tax liabilities"）
- 2026-04-27｜CFO｜guidance：CFO 說調整該稅負後的營運現金流展望約 $2.1B，比原財測高約 $100M（原話："operating cash flow outlook is approximately $2.1 billion"）
- 2026-04-27｜CFO｜guidance：CFO 形容下半年財測含適度審慎（原話："I'd describe as containing appropriate prudence."）
- 2026-04-27｜CFO｜guidance：CFO 說 Hexagon D&E 事業營收偏上半年集中（原話："more kind of first half weighted in terms of their profile"）
- 2026-04-27｜CFO｜guidance：CFO 說 Q1 太強所以提前上調財測，不等兩季（原話："We couldn't help but raise the guide"）
- 2026-04-27｜CFO｜commitment：CFO 說下半年財測要等到 7 月才更新（原話："we just wanted to wait until July to update the second"）
- 2026-04-27｜CFO｜guidance：CFO 說 2026 財測沒有假設 AI 變現出現階梯式跳升（原話："not assuming a sudden step function in AI monetization"）
- 2026-04-27｜CEO｜guidance：CEO 說 agentic AI 變現沒有放進財測（原話："we are not putting it in our guide"）
- 2026-04-27｜CEO｜product：CEO 說 agentic AI 變現可能早於他過去講的「兩個合約週期」（前文他稱長期說 2 contract cycles）（原話："agentic AI could happen sooner than 2 contract cycles"）
- 2026-04-27｜CFO｜guidance：CFO 說 2026 年到期續約的年化金額比 2025 年輕（原話："2026 is kind of lighter than 2025 for actual renewals"）
- 2026-04-27｜CFO｜guidance：CFO 對 Q1 訂單強勁的保留說法：只是一季（原話："But look, it's just one quarter."）
- 2026-04-27｜CEO｜guidance：CEO 說這是 Q1 最強的幾次財測上調之一（原話："this is one of the strongest raises we have had in Q1"）
- 2026-04-27｜CFO｜customer：CFO 說中國占 Q1 營收 13%（原話："China, it was 13% of Q1 revenue"）
- 2026-04-27｜CFO｜risk：CFO 說中國全年預期約占 13%（前句 we still expect China to be），並稱季度間可能不平均（原話："I think it can be lumpy from quarter-to-quarter"）
- 2026-04-27｜CEO｜product：CEO 報 IP 業務 Q1 年增 22%（原話："22% year-over-year revenue growth"）
- 2026-04-27｜CEO｜product：CEO 報核心 EDA 業務 Q1 年增 18%（原話："revenue growing 18% year-over-year"）
- 2026-04-27｜CEO｜product：CEO 報系統設計與分析（SD&A）Q1 年增 18%（原話："Design and Analysis business delivered 18% year-over-year"）
- 2026-04-27｜CEO｜product：CEO 說硬體（emulation）Q1 為史上最佳單季（原話："resulting in our best quarter ever"）
- 2026-04-27｜CEO｜product：CEO 說 ChipStack 引發大量客戶評估（原話："ChipStack generated tremendous customer interest"）
- 2026-04-27｜CEO｜product：CEO 說 AI 驅動與 agentic 方案正成為客戶續約與擴充的重要部分（原話："are becoming an important part of customer renewals"）
- 2026-04-27｜CEO｜product：CEO 說預期 super agents 會顯著擴大 EDA 使用量（consumption 在下一行）（原話："we expect them to materially expand EDA"）
- 2026-04-27｜CEO｜product：CEO 說新的 agentic 工具（過去客戶自己手做的環節）以訂閱加用量模式計價（原話："priced as a subscription plus consumption model"）
- 2026-04-27｜CEO｜product：CEO 說 base tool 的使用量正顯著上升（原話："our usage of base tool is going up"）
- 2026-04-27｜CFO｜product：CFO 說訂閱模式仍是與客戶的主軸安排；agentic 加值走用量與 token／card 模式（原話："Our subscription model remains the anchor"）
- 2026-04-27｜CFO｜product：CFO 說 agentic AI 不取代核心 EDA 引擎，而是更頻繁且更聰明地呼叫（原話："It calls them more often and it calls them intelligently"）
- 2026-04-27｜CFO｜customer：CFO 說定價環境已改善，且仍為價值導向定價（原話："has improved. Pricing obviously remains value-based"）
- 2026-04-27｜CEO｜competition：CEO 回應 AI 寫軟體疑慮：不擔心別人能寫出更好的 base tool（原話："other party will be able to write any better base tools"）
- 2026-04-27｜CEO｜competition：CEO 說數位（digital）平台在先進製程持續搶市占（原話："our digital platform continues to gain share"）
- 2026-04-27｜CEO｜competition：CEO 說 Palladium Z3 是 emulation 的黃金標準並搶下多個競品客戶（原話："continues to be the gold standard for emulation"）
- 2026-04-27｜CEO｜competition：CEO 說 Palladium 領先至少 10 年（因自研晶片）（原話："at least a 10-year lead in that in Palladium"）
- 2026-04-27｜CEO｜competition：CEO 說客戶看過 super agents 後認為不必自寫同類 agent（原話："there's no point writing these kind of agents"）
- 2026-04-27｜CEO｜competition：CEO 承認大多數客戶仍會自寫部分 agent（原話："most of our customers are writing some of their own agents"）
- 2026-04-27｜CEO｜customer：CEO 說客戶對 agentic 方案沒有抵制，只要能給生產力就願意採用（原話："the customer is more than willing to engage"）
- 2026-04-27｜CEO｜customer：CEO 轉述一位大客戶說每個新設計需要 2 倍工程師（原話："every new design, they require 2x more engineers"）
- 2026-04-27｜CEO｜customer：CEO 說客戶端環境在過去 3 到 6 個月明顯改善（原話："So that's actually a pretty marked improvement"）
- 2026-04-27｜CEO｜customer：CEO 說客戶為產能分散多個晶圓廠或節點會直接增加設計活動（原話："So that would directly lead to more design activity for us"）
- 2026-04-27｜CEO｜customer：CEO 說 EDA 占客戶 R&D 比重從約 7% 升到約 11%（原話："EDA used to be 7% of R&D and now it's more like 11% of R&D"）
- 2026-04-27｜CEO｜customer：CEO 說與 MediaTek 的合作擴大到 agentic AI 與核心 EDA 等（原話："we furthered our long standard partnership with MediaTek"）
- 2026-04-27｜CEO｜customer：CEO 說與一家領先全球晶圓廠簽下創紀錄 IP 交易（原話："We closed a record deal with a leading global foundry"）
- 2026-04-27｜CEO｜customer：CEO 說該 IP 大單由新先進節點（2 奈米）與更多 IP 內容驅動（原話："more specifically 2-nanometer and more content in IP"）
- 2026-04-27｜CEO｜customer：CEO 澄清該 IP 大單的晶圓廠不是 Intel（原話："And just to clarify, that is not Intel, okay?"）
- 2026-04-27｜CEO｜customer：CEO 說 Intel 體認到 14A 需要投入更多（原話："Intel realizes they need to invest more in 14A"）
- 2026-04-27｜CEO｜commitment：CEO 說與 Intel 的合作近期會有更多可說（原話："soon, we'll have more to say on our engagement"）
- 2026-04-27｜CEO｜commitment：CEO 保證 2030 年前會有 Z4 系統（原話："we'll have a Z4 system before 2030"）
- 2026-04-27｜CEO｜commitment：CEO 說會整合 SD&A 的整套方案（CFD、結構、多體動力學、前後處理）（原話："we will integrate the whole solution"）
- 2026-04-27｜CEO｜commitment：CEO 說將推出用於系統設計的 agentic flow（原話："you will see from us an agentic flow to do system design"）
- 2026-04-27｜CFO｜capital_allocation：CFO 報 Q1 用 $200M 回購股票（原話："we used $200 million to repurchase Cadence shares"）
- 2026-04-27｜CFO｜capital_allocation：CFO 說 2026 預計用約 50% 自由現金流回購股票（approximately 在前一句尾／同行）（原話："50% of our free cash flow to repurchase Cadence shares"）
- 2026-04-27｜CFO｜capital_allocation：CFO 報未償債務本金為 $2.925B（原話："principal value of debt outstanding was $2.925 billion"）
- 2026-04-27｜CEO｜capital_allocation：CEO 說併購 Hexagon 同時收購了經銷商以強化 go-to-market（原話："we also acquired some resellers to strengthen"）
- 2026-04-27｜CEO｜product：CEO 說 physical AI 會遠大於資料中心 AI（他稱五年來一直這樣說）（原話："physical AI will be bigger than data center AI"）
- 2026-04-27｜CEO｜product：CEO 說併購後 SD&A 營收規模約 $1B 年化（billion 在此行開頭，roughly $1 在前一行）（原話："billion of run rate"）

### CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說今年營收成長約 19%。（原話："We're growing this year at a clip of 19%"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：IR 主管給今年 non-GAAP 營業利益率 44.25%。（原話："44.25% of kind of non-GAAP op margin"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說今年成長率加營業利益率會超過 Rule of 60。（原話："we're going to surpass Rule of 60 this year"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說最近一季（Q2）營收成長約 24%。（原話："the revenue is growing like 24%, okay?"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管給 Q2 核心 EDA 成長 18%–19%。（原話："the core EDA is growing 18% to 19%"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管給 Q2 系統設計與分析（SD&A）成長約 35% 以上。（原話："SD&A growing at about like 35% -- north of 35%"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管給 Q2 IP 成長 40% 以上。（原話："IP growing north of 40%, okay?"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說公司約 70% 業務在「Codea」（逐字稿原字，疑為轉錄用字）。（原話："70% of our business is in Codea"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：IR 主管把公司整體增量利潤率目標說成 50%。（原話："that 50% incremental margin in general for the company"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：回答 IP 占比上升與利潤率的問題時，IR 主管說要在 IP 高成長下不犧牲公司整體利潤率。（原話："not sacrificing the overarching company margin"）
- 2026-08-26｜Richard Gu (Head of IR)｜commitment：IR 主管稱利潤率成長與 EPS 成長是公司的北極星。（原話："EPS growth is always a North Star for us"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 IP 年底前將達到年化 10 億美元的規模。（原話："going to be at a $1 billion clip by the end of the year"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 IP 策略是聚焦先進製程與連接類 IP（HBM 等）。（原話："focus on the advanced nodes IP designs, IP titles, HBM"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 IP 策略不是包山包海。（原話："we're not going to be everything for everyone"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：IR 主管以成長率說公司正在市場中拿下份額。（原話："you can tell we're gaining share in the market"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：談中國本土競爭者，IR 主管說它們規模還小。（原話："they're still a lot smaller"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：IR 主管說本土競爭者只有點工具、沒有完整流程。（原話："they don't have full flow"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：IR 主管說本土競爭者不是近中期威脅。（原話："it's not a near-term or medium-term threat for us"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：被問與最大對手的份額變化，IR 主管表示對相對地位有信心，未給分產品的份額數字。（原話："versus our peer company, we feel very confident"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說今年中國成長「至少」與公司平均相同。（原話："going to grow at least at the company average this year"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管把 Q2 中國強勁歸因於過去幾季的加購與訂單。（原話："add-on deals we had for the past couple of quarters"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管說晶圓代工生態已不只台積電、英特爾，也含三星與 Rapidus，且公司都有合作。（原話："it's not just TSMC, Intel, it's Samsung, it's Rapidus"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管提到與英特爾簽了協助其 14A 製程設計的合約，並稱其對 EDA 工具與 Agentic AI 產品也有幫助。（原話："we signed a meaningful kind of deal with Intel"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說公司已推出包含 ChipStack 在內共 4 個 super agent，涵蓋前段驗證到後段與封裝。（原話："ChipStack and also the other 3 super agents we launched"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 4 個 super agent 會另設價目表。（原話："separate price books for these 4 super agents"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 super agent 的定價比照人類設計師技能，數萬美元等級。（原話："it will be worth tens of thousands of dollars"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說客戶用量超出約定工作量時，會再依 token 與額外用量計費。（原話："additional consumption in terms of tokens and extra usage"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 agent 是人類設計師的替代，對公司是全新（greenfield）市場。（原話："This is a complete greenfield for us."）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說設計工作量未來 5、6 年將成長 30 至 40 倍。（原話："for the next 5, 6 years to the tune of even 30, 40x"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說目前 EDA 占設計端 R&D 支出的比重約 10%–11%。（原話："it's still like low teens, call it, 10%, 11%"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管說有客戶告知願意把花在人類設計師的 50% 以上再投入自動化。（原話："spend more than 50% of what we spent on a human being"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管把上述客戶說法換算成約占 R&D 預算的 33%。（原話："it's almost like 33% of the R&D budget"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管以 Cerebrus 為例，說新產品可拉動既有數位全流程工具的用量。（原話："One copy of Cerebrus can drive 10 copies of the full flow"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說最複雜的晶片電晶體數將在 5 至 6 年內成長到 1 兆（逐字稿現況數字為「[ 10 billion ]」，標為不確定）。（原話："grow to like 1 trillion in a matter of 5 to 6 years"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說定價仍有調升空間，與工作量成長並列為營收驅動。（原話："still an opportunity for us to flex further"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管轉述 Jensen 提到 40 倍生產力提升（逐字稿寫 the CHIPS Act）。（原話："they are seeing 40x productivity benefit"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管稱客戶從標準品走向 ASIC、混合 COT、COT 的路徑，客戶越多走這條路對公司越有利。（原話："going from merchandise to ASIC to hybrid COT to COT"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：IR 主管說 EDA 只能買、不能自建。（原話："EDA can only buy, you cannot build"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：被問 EDA 是否不受自研軟體與 AI 影響，IR 主管稱 EDA 是決定性、物理精確的，位置不可取代。（原話："The position of EDA is unassailable and impracticable."）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：被問 R&D 下行週期時，IR 主管承認半導體客戶會經歷週期。（原話："Semis and our customers will go through cycles"）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：同一段回答中，IR 主管說這次 AI 週期可能不同（未說明如何不同）。（原話："I think AI could be different."）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：IR 主管說客戶的 R&D 是最受保護、最不易被砍的支出。（原話："R&D typically is the most sacred, right, most insulated"）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：IR 主管說公司較不受出貨量面影響。（原話："much more insulated from the volume side of the equation"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：IR 主管稱過去 10–20 年公司營收平滑成長、利潤率擴張，EPS 成長快於營收。（原話："EPS will outpace the revenue growth"）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：被問 AI capex 見頂的疑慮，IR 主管說公司是 AI 受益者。（原話："Cadence will be an AI beneficiary and winner regardless"）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：IR 主管說公司營收驅動是設計案數與設計複雜度，而非出貨量。（原話："It's driven by design starts and design complexities"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說 Q2 底積壓訂單（backlog）為創紀錄的 81 億美元。（原話："the $8.1 billion record backlog exiting Q2"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說該 backlog 是在兩個訂單季節性偏淡的季度中依序累積出來的。（原話："in 2 seasonally down quarter from a booking standpoint"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：IR 主管給 Q2 cRPO 占 RPO 的覆蓋比率約 58%（他說高於同業）。（原話："Our ratio in Q2 is about 58%"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說 EDA 軟體合約週期通常 2.5 至 3 年，且按期認列。（原話："Our contract cycle typically runs for 2.5 to 3 years."）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說硬體是約 6 個月的管線型業務，財測每約 6 個月更新一次。（原話："we'll update the guide every kind of 6 months"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：被問 Hexagon 整合進度，IR 主管說符合預期，並說已與 BETA CAE 整合成一個完整流程。（原話："It's tracking well against our expectations."）
- 2026-08-26｜Richard Gu (Head of IR)｜capital_allocation：被拿來與對手大額併購比較時，IR 主管說公司不需要買下整間百貨公司。（原話："you don't need to buy the entire department store"）
- 2026-08-26｜Richard Gu (Head of IR)｜capital_allocation：IR 主管說 SD&A 只聚焦兩個「capstone」領域（貼近矽的封裝／3D-IC，與運算最吃重的實體模擬）。（原話："we are focused on the 2 capstone areas in the SD&A"）
- 2026-08-26｜Richard Gu (Head of IR)｜capital_allocation：IR 主管提到公司的現金流與股票回購計畫，作為長期複利模式的一部分。（原話："great kind of cash flow and share buyback kind of program"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 Millennium 已獲 NVIDIA 公開背書，並稱生產力提升 50 至 60 倍。（原話："I think we talked about the productivity of 50 to 60x."）
- 2026-08-26｜Richard Gu (Head of IR)｜commitment：被問未來 12–18 個月該追蹤什麼，IR 主管說公司自己盯的是經常性營收成長。（原話："we're closely watching is the recurring revenue growth"）

### CDNS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md
- 2026-09-09｜CEO｜customer：CEO 說 2026 年半導體、系統公司、超大規模雲端業者整體都好，對晶片的投入是他見過最強的（原話："the commitment to silicon is the strongest that I have seen"）
- 2026-09-09｜CEO｜guidance：CEO 對這波景氣還能走多久的定性說法，無財測數字（原話："it looks like party is only getting started"）
- 2026-09-09｜CEO｜competition：CEO 列出成長三個原因之一：產品表現好、相對競爭位置強（原話："our comparative position is very strong"）
- 2026-09-09｜CEO｜product：CEO 說 agentic 是傳統產品之上的新增 TAM，頂層原本由人做的工作（原話："the top layer is a brand-new TAM opportunity for us"）
- 2026-09-09｜CEO｜product：CEO 談三層蛋糕（運算資料／物理模擬／AI agent），主張價值最終落在垂直應用而非水平層（原話："the real value will accrue to the vertical application"）
- 2026-09-09｜CEO｜competition：回應「前沿模型從 prompt 直接自動化晶片設計、繞過商用 EDA」的看空論點，CEO 稱沒有晶片不用 Cadence 工具設計（原話："There's no chips being designed without using our tools"）
- 2026-09-09｜CEO｜competition：CEO 主張 AI 模型做不了古典物理模擬的中間層，需與物理引擎並用（原話："mathematically, it's not possible to do the middle layer"）
- 2026-09-09｜CEO｜competition：被問為何不能由他人提供頂層或底層，CEO 承認有客戶自寫 agent 去呼叫 Cadence 工具（原話："some customers are writing some agents that call our tools"）
- 2026-09-09｜CEO｜competition：CEO 稱外部 agent 呼叫 Cadence 工具在部分情境可行，但效率較差；Cadence 自己寫了中間層與頂層，能取用未對外開放的內部介面（原話："agent could call our tools, but it is not that efficient"）
- 2026-09-09｜CEO｜competition：CEO 表示頂層 agent 市場不需要百分之百由 Cadence 拿下，客戶可有約 10 個 agent，4 個大的由 Cadence 提供（原話："we don't need to get 100% of that market"）
- 2026-09-09｜CEO｜product：CEO 說頂層有 4 個 super agent（同段點名：前端設計、實體設計、類比設計、PCB 與封裝），中間層約 30、40 個產品（原話："The top layer, we have 4 super agents"）
- 2026-09-09｜CEO｜capital_allocation：CEO 提到研發團隊規模，同時撰寫頂層與中間層（原話："We have like 10,000 people in R&D"）
- 2026-09-09｜CEO｜product：被問 agentic 怎麼變現，CEO 說頂層採新商業模式（消費加訂閱），中間層維持原有模式；未給營收數字（原話："which is consumption plus subscription"）
- 2026-09-09｜CEO｜risk：針對「效率提升 5 倍就只買 1/5 中間層」的市場疑慮，CEO 以 2006 年模擬器快 10 倍的舊例反駁（原話："people will buy like 10x less, but that never happens"）
- 2026-09-09｜CEO｜customer：CEO 引述 TSMC 路線圖：未來 5 年晶片複雜度或尺寸成長倍數，作為工作量呈指數成長的依據（原話："chips complexity or size will go up by 48x"）
- 2026-09-09｜CEO｜customer：CEO 稱客戶要靠 5 到 10 倍的自動化才撐得住設計規模成長，不可能等比例增聘工程師（原話："this 5 to 10x improvement to even sustain the growth"）
- 2026-09-09｜CEO｜customer：CEO 對比歷史：90 年代末、2000 年代初設計 CPU 約 5 年、500 人，現在的人力與時程（原話："you can design a CPU with 30, 40 people within 6 months"）
- 2026-09-09｜CEO｜customer：CEO 引述 Imec 路線圖，稱指數成長預計持續到 2042 年（原話："exponential is still projected to go until 2042"）
- 2026-09-09｜CEO｜product：被問 agentic 與過去 Cerebrus／GenAI 有何不同，CEO 稱 agentic 對 Cadence 的意義大於 GenAI（原話："agentic is much more meaningful to us than GenAI"）
- 2026-09-09｜CEO｜product：CEO 說人一次約跑 3、4 個實驗，agent 跑的實驗數量（同段對比）（原話："when the agent runs it, it runs, like, 100 experiments"）
- 2026-09-09｜CEO｜product：CEO 稱 agentic 帶動底層基礎工具用量上升，並說在財報中看得到（原話："the usage of the base tools is also going up"）
- 2026-09-09｜CEO｜customer：CEO 稱已與頂尖客戶接洽全套 agentic 方案（原話："we have engaged with all the top companies"）
- 2026-09-09｜CEO｜competition：被問競爭優勢在哪，CEO 稱 Cadence 在 agentic 領先（原話："we are definitely leading in agentic"）
- 2026-09-09｜CEO｜competition：CEO 稱現在各產品線同時表現良好、不依賴單一領域（原話："we are hitting in all cylinders"）
- 2026-09-09｜CEO｜product：CEO 給 IP 業務今年成長幅度；原文未說明是營收、訂單或其他口徑（原話："our business is up 30% this year"）
- 2026-09-09｜CEO｜product：CEO 談 IP 去年成長幅度，用語帶不確定（I think、probably）（原話："Was up, I think, 30% last year, probably"）
- 2026-09-09｜CEO｜capital_allocation：CEO 承認 IP 過去是 Cadence 的弱項，先前投入較少（原話："IP was the weak point of cadence historically"）
- 2026-09-09｜CEO｜margin：CEO 說明過去少投資 IP 的原因：獲利性不如 EDA（未給利潤率數字）（原話："because it's not as profitable as EDA"）
- 2026-09-09｜CEO｜capital_allocation：CEO 說現在因 AI 與 3D IC，看到 IP 有更多機會（與前述「過去少投資」對照）（原話："there is more opportunities in IP"）
- 2026-09-09｜CEO｜product：CEO 說 IP 聚焦先進製程與 HPC，並選 5、6 種關鍵 IP（SerDes、PCIe、UCIe、HBM、DDR）（原話："we focus on lower nodes and HPC IP"）
- 2026-09-09｜CEO｜capital_allocation：CEO 說其他晶圓廠（Samsung、Intel、Rapidus）也要進入，Cadence 需為它們開發 IP（原話："we need to develop IPs for them"）
- 2026-09-09｜CEO｜product：CEO 談硬體（模擬驗證系統）需求，稱近 6 年來每年創紀錄；原文未指明指標與數字（原話："it has been a record year for, I don't know, last 6 years"）
- 2026-09-09｜CEO｜guidance：CEO 對硬體需求的定性看法，無財測數字（原話："I don't think that's going to slow down"）
- 2026-09-09｜CEO｜product：CEO 拆解硬體需求三個來源之一：硬體採購量與晶片尺寸成正比（原話："hardware you buy is proportional to the size of the chip"）
- 2026-09-09｜CEO｜competition：CEO 稱 Cadence 自研硬體系統領先 10 到 15 年（並說是唯一在 TSMC 自行設計晶片的公司）（原話："a 10-, 15-year lead in designing our own"）
- 2026-09-09｜CEO｜competition：CEO 稱這類硬體系統是複雜晶片設計不可缺（用來在晶片回來前跑 OS／軟體驗證）（原話："cannot design any complicated chip without these systems"）
- 2026-09-09｜CEO｜product：被問 SDA 對 Boeing 與 NVIDIA 是否策略不同，CEO 稱兩者相近，並說 SDA 演算法比 EDA 簡單（原話："SDA is easier than EDA"）
- 2026-09-09｜CEO｜capital_allocation：CEO 說明 SDA 的擴張範圍：做與晶片設計有綜效的項目（熱、電磁、3D IC）（原話："things which are synergistic to chip design"）
- 2026-09-09｜CEO｜commitment：CEO 陳述一貫優先順序：EDA 要做到第一，避免擴張時失去核心焦點（原話："our always focus from the beginning is EDA should be #1"）
- 2026-09-09｜CEO｜risk：CEO 談三個垂直應用（資料中心、實體 AI、科學 AI）各有自己的高峰期，說資料中心目前在高峰（原話："I think data center is in peak"）
- 2026-09-09｜CEO｜guidance：CEO 對實體 AI 週期高峰時點的看法（同段稱科學／生命科學約 5 到 10 年後）；無營收數字（原話："physical AI may peak in the next 3 to 7 years"）
- 2026-09-09｜CEO｜capital_allocation：CEO 說明為實體 AI 布局，投資 Hexagon D&E 業務取得模擬能力（原話："we invested in Hexagon D&E business for simulation"）
- 2026-09-09｜CEO｜commitment：CEO 陳述投資原則：在大趨勢之前提前投入，幅度不會太大（原話："we always over invest ahead of it, not too much"）
- 2026-09-09｜CEO｜commitment：CEO 表示三個垂直應用（資料中心、實體 AI、科學 AI）都要投資（原話："we want to invest in all these three slices"）
- 2026-09-09｜CEO｜customer：CEO 稱與所有 Mag 7 合作，並說可在財報看到（原話："We are working with all the Mag 7"）
- 2026-09-09｜CEO｜customer：CEO 談剛從中國回來，前一句點名 Xiaomi、BYD、NIO 都在設計晶片，稱它們是客戶（原話："they're all designing chips, they're all our customers"）
- 2026-09-09｜CEO｜customer：CEO 說核心 EDA 與 TSMC、ARM 長期合作，現在也與 Intel、Samsung 合作（原話："and now with Intel and Samsung"）

### 問答異常語氣（迴避／改口／保留）
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Andrew DeGasperi (BNP)：那家擴大使用 sign-off 的 marquee AI infrastructure 公司是不是雲端業者｜答法：CEO 未回答是或否，只說「主要的 AI infrastructure/ASIC 公司」，轉談 Innovus 與 sign-off 在 TSMC 的採用
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Gianmarco Conti (Deutsche)：Palladium／Protium 下一代（Z4、X4）是否 12–18 個月內推出｜答法：CEO 明說不談新品時程，改談 Z3 容量足夠與競爭領先，只承諾 2030 年前會有 Z4
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Joseph Quatrochi (Wells Fargo)：EDA 占客戶 R&D 比重未來可以到多少｜答法：CEO 給歷史 7%→11%，但說寧可印出結果不預測，「多少我們看看」，未給目標數字
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Lee Simpson (Morgan Stanley)：physical AI 的價值何時會出現在數字裡｜答法：CEO 談三層蛋糕、TAM 與矽晶片需求，沒有給何時反映在財報的時點
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Harlan Sur (JPMorgan)：財測隱含下半年季均營收略低於 Q2，是 Hexagon 還是核心業務不均｜答法：CFO 用「appropriate prudence」與 Hexagon 上半年偏重回應，說等 7 月再更新下半年，未給下半年拆解數字
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Siti Panigrahi (Mizuho)：Rapidus、Intel Foundry 等新晶圓廠是否已對 IP 需求有實質貢獻｜答法：CEO 未量化貢獻，稱與 Intel 進展良好但「soon we'll have more to say」，並澄清創紀錄大單不是 Intel
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：市場對 EDA 與 AI capex 見頂的疑慮，到底看錯了什麼？｜答法：先說「the market is the market」，再轉談策略、領導團隊與「AI 受益者」，沒有直接回答市場哪裡看錯，也沒談 capex 見頂情境的數字。
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：若客戶 R&D 進入下行週期，公司營收是否有一個底？｜答法：沒有正面確認「有底」，也沒給數字；回頭講過去 10–20 年平滑成長、R&D 最受保護，並加了一句「I think AI could be different」，語氣有保留。
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：81 億 backlog 的能見度與長期目標拆分？是否考慮其他領域的併購（bolt-on）？｜答法：回答 backlog 品質（cRPO 覆蓋率 58%）、合約週期與 Hexagon 整合，沒有回應是否找其他 bolt-on，也沒給 backlog 分業務拆分。
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：3 年後中國在公司成長中扮演什麼角色？｜答法：只回答今年（至少與公司平均相同）與 Q2 加購訂單，未談 3 年後；結尾用「We'll keep a close eye on it」帶過。
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：R&D 預算中軟體占比何時會到 20%–25%？｜答法：沒給時點；改引客戶說願意花人力成本 50% 以上於自動化、換算約 33% 的說法，並轉談長期順風。
- CDNS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：分析師問：agentic 與過去 Cerebrus 等 AI 功能相比，以營收角度看，什麼在推動經常性收入加速成長？｜答法：CEO 回答談 agent 跑實驗數量（約 100 個 vs 人跑 3、4 個）、workflow 與生產力，未提供 agentic 營收、占比或貢獻幅度的任何數字；前一題問變現時也只答商業模式（消費加訂閱）
- CDNS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：分析師問：你曾說硬體需求受供給限制，結構上是什麼在推動需求？｜答法：CEO 回答談硬體不可取代、設計數量增加、晶片尺寸變大三點，未回應「供給受限」這個前提，也未提交貨或產能
- CDNS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：分析師問：實體 AI 長期對 Cadence 營收貢獻的量級該怎麼看？｜答法：CEO 回答談市場是兆美元級、週期高峰在未來 3 到 7 年、已收購 Hexagon D&E，未給對 Cadence 營收的任何量級或時程數字

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
{"date":"20260905","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價 ≤$260（FY2027 本益比 27x）或 token 營收首次揭露 → 加第二個三分之一；BIS 50% 規則落地無 EDA 許可 → 第三段","irr_base_pct":10.7,"ev5y_pct":50.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"A","val":"🟡","ma":"-","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":3.7,"ev5y_pct":50.8,"irr_base_pct":10.7,"max_dd_pct":-50,"bull_5y_price":669.6,"bear_5y_price":206.8,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"價 ≤$260（FY2027 本益比 27x）或 token 營收首次揭露 → 加第二個三分之一；BIS 50% 規則落地無 EDA 許可 → 第三段","price_at_dd":292.7,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260924/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
