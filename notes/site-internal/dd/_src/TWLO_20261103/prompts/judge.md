你是 stock-analyst **v20 判斷 agent**，標的 TWLO（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TWLO","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TWLO_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TWLO_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":1559.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（YoY +20% 報導、+16% 有機；QoQ +4.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results ；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000106/twloq326ex991.htm"},"note":"未取得（新聞稿無共識；consensus_revision 僅有 EPS）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":325.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（利益率約 21%，YoY +39%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results ；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000106/twloq326ex991.htm"},"note":"未取得（新聞稿無共識；consensus_revision 僅有 EPS）"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":148.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（利益率約 10%，YoY +263%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results ；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000106/twloq326ex991.htm"},"note":"未取得（新聞稿無共識；consensus_revision 僅有 EPS）"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":369.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（利益率 24%；去年同期 247.5、19%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results ；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000106/twloq326ex991.htm"},"note":"未取得（新聞稿無共識；consensus_revision 僅有 EPS）"},{"id":"f_kpi5_dollar_based_net_expansi","label":"Dollar-based net expansion rate (NRR)","value":114,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%（去年同期 109%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results ；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000106/twloq326ex991.htm"},"note":"未取得（新聞稿無共識；consensus_revision 僅有 EPS）"},{"id":"f_kpi6_guidance_q4_2026","label":"Guidance Q4 2026","value":null,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"營收 1,595–1,605 USD M（報導 +17–17.5%，有機 +11–12%）；non-GAAP 營業利益 300–310 USD M；non-GAAP EPS 1.48–1.53（163M 股）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results ；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000106/twloq326ex991.htm"},"note":"未取得（新聞稿無共識；consensus_revision 僅有 EPS）","needs_sonnet":true},{"id":"f_kpi7_guidance_fy2026","label":"Guidance FY2026（上調）","value":null,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"報導營收成長 20%（前 18–18.5%）；有機 15%（前 13–13.5%）；non-GAAP 營業利益 1,190–1,200 USD M（前 1,135–1,155）；FCF 1,190–1,200 USD M（前 1,135–1,155）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results ；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000106/twloq326ex991.htm"},"note":"未取得（新聞稿無共識；consensus_revision 僅有 EPS）","needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_twlo_gross_margin_pct","label":"TWLO 毛利率","value":48.51,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TWLO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_twlo_operating_margin_pct","label":"TWLO 營業利益率","value":6.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TWLO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_twlo_fcf_margin_pct","label":"TWLO FCF 利潤率","value":17.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TWLO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_band_gross_margin_pct","label":"BAND 毛利率","value":36.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAND.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_band_operating_margin_pct","label":"BAND 營業利益率","value":-2.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAND.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_band_fcf_margin_pct","label":"BAND FCF 利潤率","value":8.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAND.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_sinch_st_gross_margin_pct","label":"SINCH.ST 毛利率","value":36.22,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SINCH.ST.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sinch_st_operating_margin_pct","label":"SINCH.ST 營業利益率","value":3.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SINCH.ST.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sinch_st_fcf_margin_pct","label":"SINCH.ST FCF 利潤率","value":9.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SINCH.ST.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rng_gross_margin_pct","label":"RNG 毛利率","value":71.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RNG.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_rng_operating_margin_pct","label":"RNG 營業利益率","value":7.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RNG.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_rng_fcf_margin_pct","label":"RNG FCF 利潤率","value":22.98,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RNG.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC 占營收","value":9.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%（SBC 153.9 USD M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results ；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000106/twloq326ex991.htm"},"note":"未取得（新聞稿無共識；consensus_revision 僅有 EPS）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":208.56,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":10.14,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":32.17,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.93 → 5.93）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.8 → 6.8）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.78 → 7.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.93,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.8,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.78,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":3.85,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 5.71 → 5.93（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":26.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.53,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.22,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":35.21,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 5.93，分子＝快照價 208.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-1834.47,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 1057.0、現金 2891.47（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":154.73,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":30437.63,"period":"2026-11-03","unit":"USD m","basis":"市值 32272.1 ＋ 淨負債 -1834.47","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6069.59,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6755.76,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.01,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 210.46 / W52 178.16 / W104 144.85 / W250 103.74 / W250 13週斜率 0.08%"},{"id":"f_ma_w52","label":"52 週均線","value":178.16,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":144.85,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":103.74,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.08,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 自述：競爭者為 CPaaS、區域電信網路商、CRM/CX 廠商、獨立 CDP 與其他軟體公司；預期新進入者與新產品使競爭加劇。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"With the introduction of new products and services and new market entrants, we expect competition to intensify in the future.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：市場高度分散、部分領域進入門檻相對低，競爭對手可能以較低價格或 AI 更快整合搶客，迫使降價。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"Our competitors or other third parties may incorporate AI into their products, offerings, and solutions more quickly or more successfully than us, which could impair our ability to compete effectively and adversely affect our results of operations.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Gartner 2026 CPaaS Magic Quadrant：Twilio 與 Infobip 為領導者，Vonage 回到頂層，新增三家廠商入列。","source":"CX Today: Gartner Magic Quadrant for CPaaS 2026","url":"https://www.cxtoday.com/service-management-connectivity/gartner-magic-quadrant-cpaas-2026/","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"第三方分析稱 Bland AI、Vapi、Retell 等 AI 語音新創正從 Twilio 搶語音支出，但未在 CPaaS 份額追蹤中明顯可見。","source":"Swfte: Twilio Competitors 2026","url":"https://www.swfte.com/compare/twilio-competitors","excerpt":"2024-2025: Voice-AI challengers (Bland AI, Vapi, Retell) raise large rounds and cannibalise Twilio voice spend. 2025: Twilio sells Segment business unit, refocuses on CPaaS core after activist investor pressure.","as_of":"2026-05-06","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素提及企業客戶可能選擇自行開發不含 Twilio 產品的解決方案（一般性風險，未指名客戶）","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"Enterprise customers may not use our products enough for us to generate revenue that justifies our cost to obtain such customers, or may choose to develop their own solutions that do not include our products.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-Q 稱無單一客戶占營收或應收帳款逾 10%","source":"SEC EDGAR 10-Q Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000092/twlo-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2025、FY2024、FY2023 三年皆無單一客戶組織占總營收逾10%；2025與2024年底也無客戶占應收帳款毛額逾10%。","source":"SEC EDGAR 10-K FY2025 Item 8 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"During the years ended December 31, 2025, 2024 and 2023, no customer organization accounted for more than 10% of the Company’s total revenue.\n\nAs of December 31, 2025 and 2024, no customer organization represented more than 10% of the Company’s gross accounts receivable.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"公司稱客戶廣泛、對重要客戶做信用評估、不要求擔保品；任何重要客戶財務惡化可能影響營運結果。用量計費收入占比74%（2025）、72%、71%。","source":"SEC EDGAR 10-K FY2025 Item 8 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"The Company sells its services to a wide variety of customers. If the financial condition or results of operations of any significant customer deteriorate substantially, operating results could be adversely affected. To reduce credit risk, management performs credit evaluations of the financial condition of significant customers","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Twilio Q1 2026 coverage: voice AI drove fastest growth in three years and FY revenue forecast raised; per search summary Q2 FY2026 coverage cited self-serve voice (AI-native entry point) growing >50% y/y. Sources do not analyze long-term durability; AI-native accounts described as small but high-growth cohort.","source":"The Next Web: Twilio raises full-year revenue forecast as voice AI drives fastest growth in three years","url":"https://thenextweb.com/news/twilio-q1-2026-voice-ai-revenue","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Infrastructure software (e.g., Twilio per-message) uses consumption pricing vs seat-based application SaaS; commentary argues AI agents threaten seat-based software, not usage-based. Opinion-level source.","source":"Nasdaq index presentation NQRPCI / SaaS pricing commentary","url":"https://indexes.nasdaqomx.com/docs/NQRPCI Presentation.pdf","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素：發送簡訊／語音／email 不當可能引發消費者保護法規與執法風險（含 TCPA，FCC、FTC、州檢察長罰款）；屬產業特定監管風險揭露，非反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"The actual or perceived improper sending of text messages, voice calls, or e-mail may subject us to potential risks, including liabilities or claims relating to consumer protection laws and regulatory enforcement, including fines.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Twilio 向 Ofcom 2026/27 工作計畫諮詢提交回覆，要求新規與其他監管機構協調、避免與 Telecommunications (Security) Act 2021 重複。","source":"Ofcom consultation response - Twilio","url":"https://www.ofcom.org.uk/siteassets/resources/documents/consultations/category-1-10-weeks/consultation-plan-of-work-2026-27/responses/twilio.pdf","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：關稅與貿易政策不確定性可能影響全球經濟與公司業務；關稅與通膨導致的價格上升可能提高營運費用；客戶受關稅衝擊可能降低使用量。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"Additionally, increased prices resulting from the effects of tariffs and inflation could increase our operating expenses.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 揭露：公司產品受美國出口管制、海關與經濟制裁法規約束；部分產品含加密技術，可能受出口管制；已知有少數個人／實體涉及制裁地區的往來。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"Encryption products and the underlying technology may also be subject to export control restrictions. Governmental regulation of encryption technology and regulation of exports of encryption products, or our failure to obtain required approval for our products, when applicable, could harm our international sales and adversely affect our revenue.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露：Twilio 依賴 AWS 作為主要雲端基礎設施，AWS 中斷會影響服務；AWS 可因未補正違約終止或暫停合約，切換替代供應商可能造成平台中斷（搜尋摘要轉述，未逐字取得原文）","source":"Twilio FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2026 年 10-Q 風險因子列出國際營運、出口管制/制裁合規、匯率，並提及依賴網路服務商與 ISP 提供連線（搜尋摘要轉述，未逐字取得原文）","source":"Twilio Form 10-Q (quarter ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001447669/000144766926000092/twlo-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Twilio Q3 2026 營收 $1.56B，reported +20%、organic +16%；Q4 指引 $1.595–1.605B，organic +11–12%；全年 organic 指引 15%、reported 20%。頁面未提供分段營收。","source":"Twilio press release: Twilio announces third quarter 2026 results","url":"https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results","excerpt":"Revenue of $1.56 billion, up 20% reported and 16% organic year-over-year","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Q4 organic 成長指引 11–12%，低於 Q3 organic 16%（報導稱股價盤後跌逾 15%）。","source":"Twilio press release: Twilio announces third quarter 2026 results","url":"https://www.twilio.com/en-us/press/releases/twilio-announces-third-quarter-2026-results","excerpt":"an organic revenue growth range of 11% to 12% year-over-year","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"CPaaS 市場規模與預測差異極大（IMARC 2025 年 $14.9B、2026–2034 年成長率 20.23%；其他機構 CAGR 28%+），僅供方向參考。","source":"WebSearch result summary (IMARC / Fortune Business Insights / Global Growth Insights)","url":"https://www.imarcgroup.com/report/en/communications-platform-as-a-service-market","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Gartner CPaaS MQ 2026 概述：2025 重點為 SMS 漲價與 carrier-plus 模式，2026 轉向 AI 編排與 outcome-based pricing；Twilio 與 Infobip 為領導者。","source":"CX Today: Gartner Magic Quadrant CPaaS 2026","url":"https://www.cxtoday.com/service-management-connectivity/gartner-magic-quadrant-cpaas-2026/","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Twilio FY2025 10-K 風險因素：客戶可能因價格壓力、預算限制或業務優先順序改變而改用替代方案，且競爭對手可能推出功能相近或單一功能、較低價的產品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"In addition, customers may reduce or delay spending on our products or substitute alternative solutions in response to pricing pressures, budget constraints or changing business priorities.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Twilio 10-K 稱持續投資 AI 能力，並提及在快速技術變動下持續創新。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"We are continuing to invest in AI-powered capabilities, which we believe have the potential to enhance our offerings’ value to customers, as well as to automate processes and help our business run more efficiently.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Twilio SIGNAL 2026 推出 conversation layer，定位從純 CPaaS 轉向對話基礎設施。","source":"BlogGeek.me: Twilio SIGNAL 2026","url":"https://bloggeek.me/twilio-signal-2026/","excerpt":"Twilio SIGNAL 2026: the pivot from CPaaS to conversation infrastructure MarketAugust 6, 2026· 5 min read TL By Tsahi Levent-Levi Twilio just told the market it doesn't want to be a CPaaS anymore.","as_of":"2026-08-06","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"業界人士稱透過 MCP 包裝與 AI 編排，品牌無需單一 CPaaS，可自動跨多供應商路由。","source":"CX Foundation: CPaaS providers","url":"https://cxfoundation.com/blog/cpaas-providers","excerpt":"“With MCP wrappers and AI orchestration, brands don’t need a single CPaaS solution, and they can route across multiple vendors automatically. That’s a major shift, and a big disruption.”","as_of":"2026-04-02","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Twilio Q1 2026 後管理層稱 voice AI 仍僅占語音量一小部分。","source":"MEF: Twilio Q1 2026","url":"https://mobileecosystemforum.com/2026/05/07/twilios-q1-2026-milestone-quarter-a-big-bounce-and-a-guide-for-the-cpaas-market/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Twilio 10-K FY2025 describes strategy of consolidating into one platform combining communications channels, contextual data and AI orchestration, with pre-built solutions and cross-channel orchestration (platform consolidation, no D2C/channel disintermediation described).","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm","excerpt":"Our strategy is rooted in streamlining our platform and delivering a trusted, intuitive customer experience.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Futurum summary of Q1 FY2026: Twilio described go-to-market changes combining account executive coverage with specialist motions, plus enablement/compensation to drive cross-sell of software add-ons (Verify, ConversationRelay); self-serve and ISV cohorts grew 25%+ YoY.","source":"Futurum Group, Twilio Q1 FY 2026 Earnings Show Accelerating Voice and Messaging Demand","url":"https://futurumgroup.com/insights/twilio-q1-fy-2026-earnings-show-accelerating-voice-and-messaging-demand/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Third-party tracker reports Twilio restructured pricing plans (Free Trial, Pay-as-You-Go, Enterprise) in April 2026.","source":"costbench Twilio Pricing Change April 2026","url":"https://costbench.com/changelog/twilio-plans-renamed-2026-04/","excerpt":null,"as_of":"2026-04-25","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-06 Q2 報告後，公司把 FY2026 reported revenue growth 指引由 14–15% 上調至 18–18.5%（organic 13–13.5%）；非 GAAP 營業利益與 FCF 指引上調至 $1.135–$1.155B。2026 年每次更新皆上調，未見 2026 下調。","source":"Futurum / Seeking Alpha / Benzinga 彙整（搜尋摘要）","url":"https://futurumgroup.com/insights/twilio-q2-fy-2026-ai-communications-gain-commercial-traction/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 指引：營收 $1.505–$1.515B、非 GAAP EPS $1.42–$1.47；MarketBeat 稱其高於共識 EPS 1.250。","source":"MarketBeat: Twilio releases Q3 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/twilio-nysetwlo-releases-q3-2026-earnings-guidance-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價共識約 $210.72（Investing.com/Walnut，31 位分析師，中位數 $210，區間 $120–$300，26 Buy/4 Hold/2 Sell）；MarketBeat 8/6 載共識 $220.59；TickFlow 8/1 為 $208.62；Benzinga 平均 $196、高 $285 低 $99（日期不明）。BTIG 升至 $245、Citizens 升至 $250（2026-07）。目標價快照均為 2026-08 前後，未找到 8 月後的更新。","source":"Walnut Invest / Investing.com / MarketBeat / TickFlow（搜尋摘要）","url":"https://walnutinvest.com/stocks/twlo/forecast","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Seeking Alpha 共識 FY2026 EPS 2026 年 5 月快照由 5.423 升至 5.695（7 日內 +5.0%），顯示上修；Q2 非 GAAP EPS 報告 vs 共識有大幅 beat（Investing.com：EPS $1.47 vs $1.32）。10/29 的 Q3 實際結果本軸未查得。","source":"Baselight daily insights / Seeking Alpha revisions / Investing.com","url":"https://baselight.app/daily-insights/stocks/2026-05-10/twlo-21-fy-eps-upgrades-near-52w-high-bofa-225-fastest-growth-since-2022","excerpt":null,"as_of":"2026-05-10","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"SEC EDGAR 8-K 清單：2025-11-03 至 2026-11-03 共 6 份 8-K，含重大項目者 0 份（無併購、重編、下市等 8-K 事件）。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001447669&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月 8-K 清單無含重大項目（如 2.01 併購完成）者。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001447669&type=8-K","excerpt":"其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 4.02（財報不可信賴/重編）項目。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001447669&type=8-K","excerpt":"其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers","decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TWLO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.51,"operating_margin_pct":6.99,"fcf_margin_pct":17.35,"rd_intensity_pct":18.62},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TWLO","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"BAND","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.86,"operating_margin_pct":-2.06,"fcf_margin_pct":8.52,"rd_intensity_pct":17.75},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAND","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"SINCH.ST","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.22,"operating_margin_pct":3.77,"fcf_margin_pct":9.11,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SINCH.ST","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"RNG","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.85,"operating_margin_pct":7.34,"fcf_margin_pct":22.98,"rd_intensity_pct":12.44},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RNG","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"TWLO"},"financial_history":{"ticker":"TWLO","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":3826321000.0,"revenue_yoy_pct":null,"gross_margin_pct":47.4,"operating_margin_pct":-26.94,"net_income":-1256145000.0,"diluted_eps":-6.86,"free_cash_flow":-334550000.0,"fcf_margin_pct":-8.74,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":4153945000.0,"revenue_yoy_pct":8.56,"gross_margin_pct":49.2,"operating_margin_pct":-9.4,"net_income":-1015441000.0,"diluted_eps":-5.54,"free_cash_flow":363517000.0,"fcf_margin_pct":8.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":4458036000.0,"revenue_yoy_pct":7.32,"gross_margin_pct":51.1,"operating_margin_pct":-0.91,"net_income":-109403000.0,"diluted_eps":-0.66,"free_cash_flow":657455000.0,"fcf_margin_pct":14.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5067220000.0,"revenue_yoy_pct":13.66,"gross_margin_pct":48.92,"operating_margin_pct":3.45,"net_income":33834000.0,"diluted_eps":0.21,"free_cash_flow":945427000.0,"fcf_margin_pct":18.66,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TWLO/TWLO_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Twilio Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to Twilio's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please be advised that today's conference call is being recorded. 
I would now like to hand the conference over to your first speaker today, Rodney Nelson. 
Please go ahead.

**Rodney Nelson** (Executives):
Good afternoon, everyone, and thank you for joining us for Twilio's Third Quarter 2026 Earnings Conference Call. Joining me today are Khozema Shipchandler, Chief Executive Officer; Aidan Viggiano, Chief Financial Officer; and Thomas Wyatt, Chief Operating Officer. 
As a reminder, we will disclose non-GAAP financial measures on this call. Definitions and reconciliations between our GAAP and non-GAAP results can be found in our earnings presentation posted on our IR website at investors.twilio.com. We will also make forward-looking statements on this call, including statements about our future outlook and goals. Such statements are subject to known and unknown risks and uncertainties and that could cause actual results to differ materially from those described. 
Many of those risks and uncertainties are described in our SEC filings, including our most recent Form 10-K and our forthcoming Form 10-Q. Forward-looking statements represent our beliefs and assumptions only as of the date such statements are made. We disclaim any obligation to update any forward-looking statements, except as required by law. 
With that, I'll hand it over to Khozema and Aidan, who will discuss our Q3 results, and then we'll open the call for Q&A.

**Khozema Shipchandler** (Executives):
Thanks, Rodney. Good afternoon, everyone, and thank you for joining us today. Twilio had a great third quarter. Revenue grew 16% organically while non-GAAP gross profit grew 18% year-over-year. We generated $326 million in non-GAAP income from operations and $370 million in free cash flow, record quarters for both. We are in the very early stages of an AI super cycle. Voice and consumer AI have gained early traction, but penetration is still extremely low. This bodes very well for Twilio. 
Developers and enterprises alike choose Twilio because of our fast, trusted and reliable infrastructure that works seamlessly with their existing technology stacks. Customers grow with Twilio because we provide global scale and rich context and integrate to virtually any technology as companies continue experimenting with which AI environments are optimally tuned for their purposes. 
In short, we provide fast ROI, so our customers can take advantage of the incredible innovation spurred by AI today and the inevitable innovations to come tomorrow. The leading voice and consumer AI companies are using our platform to power the first wave of agentic experiences. While the growth rates of these companies are incredible, and the technology is awesome as consumers, most of us have limited interactions with both voice and consumer AI in daily life. Part of this is just the natural adoption cycle which should create enormous tailwinds for the company. Part of this has to do with trust, knowing who or what an agent represents and always understanding what it's doing, why and for how long. 
And finally, ROI has been hard to come by. This is a good setup for Twilio. We are building a company to accelerate AI adoption. We have long provided a context layer that allows every customer to utilize personalized data to enrich every interaction with the consumer, yielding increased revenue and lower cost, plus a better consumer outcome. We have also provided tools such as Branded Calling and verification capabilities, which lead to higher conversion rates plus reinforced trust. At our SIGNAL Conference, we included all of these capabilities in a massively simplified console that is easier than ever for developers to utilize and a purpose built for agents as tools like frontier models and vibe coding applications take off. 
In addition, we wrapped all of these offerings together so customers can utilize what they need, basic infrastructure, data hydrated channels or a complete solution such as Conversation Relay, which remains technology agnostic at the application layer, allowing customers to make their own technology decisions while ensuring easy integration to our technology partners. We launched these capabilities as part of a broader conversations layer which is gaining real momentum in the marketplace. More recently, we launched an identity offering into private beta, so businesses are able to safely validate who an agent is representing irrespective of the AI modality they utilize, application, channel or technology protocol. 
While it is extremely early, we have been encouraged by customer feedback and intend to launch an offering into general availability next year. The breadth of the AI opportunity was particularly evident at our annual Exec Connect customer event that we hosted a few weeks ago for top executives from Twilio's largest customers. The input from customers was encouraging relative to our recent releases and product road map. Businesses need trusted channels. They need global scale. They need context they need higher conversion rates. And increasingly, they need secure identity, governance and observability. They want Twilio to help them innovate at AI speed. 
Our results reflect this demand. In Q3, we saw continued strong growth in self-serve and ISVs as well as ongoing strength in Voice and Messaging. Our go-to-market team landed notable wins, including our first 8-figure conversations deal with a health insurance provider. This company's voice AI agent is powered by Conversation Relay and Conversation Intelligence's real-time transcription to enhance call tracking and reduce agent wrap-up time. We also signed deals with Chapter, Eltropy, ElevenLabs, Gong, HUGO BOSS, Meera.ai, Rivian and Ushur. Our customers continue to expand their usage of the platform across multiple products as their customer needs become more complex and revenue growth from multiproduct customers continues to outpace our corporate average. 
For example, Meera.ai and AI reachability platform connecting humans and AI agents with hard-to-reach consumers expanded their messaging use case to include voice and our conversations layer. They're using both to coordinate multichannel outreach, preserve conversation context and support consultative sales conversations with proper lead qualification or Ushur the AI native platform for agentic customer experiences in health care, insurance and the public sector signed a 7-figure expansion with Twilio. Ushur uses Twilio Voice, Messaging and WhatsApp for multichannel engagement and is expanding its voice AI capabilities with Conversation Relay. 
Major health plans use Ushur to engage millions of members through multilingual 2-way conversations and have achieved 3x higher Medicaid re-enrollment completion rates compared with human led outreach. Beyond Medicaid, Ushur's AI agents resolve inquiries and complete complex customer journeys end-to-end with customers automating 20% or more of inbound call volume. Another example is Gong, the leading revenue AI company which signed a 7-figure deal to continue using voice and other software add-ons for Gong Engage. It's AI-powered sales engagement solution. 
Or Eltropy, an agentic AI platform for credit unions and community banks, which is invested in Twilio's conversations layer and its voice agents now resolve up to 70% of routine member calls on their own. 
In Q3, the company signed an expansion deal to use both RCS and Branded Calling to improve its trusted customer interactions across multiple channels. And finally, Chapter, a consumer services company signed a 7-figure deal to migrate its contact center onto Flex, standing up a fully live deployment in a matter of weeks as part of a broader move to make Twilio the backbone of its customer service operations. In addition, they will leverage Messaging, Voice and software add-ons like Branded Calling to power a multichannel experience for their customers. 
With these customer examples, you can see the power of Twilio. Consumers dictate the terms of how they want businesses to engage with them in their preferred channels and at their preferred time, and they want the ability to seamlessly escalate in interaction to a human agent whenever they want. This richness and flexibility requires significant breadth in technology capabilities and our innovative platform continues earning validation from analysts as we were named a major player in IDC's 2026, Conversational Intelligence and Analytics MarketScape during the quarter. 
Over the past 3 years, we have accelerated revenue and gross profit growth, increased operating leverage, generated substantial free cash flow and reduced dilution. We operate from a position of strength. We are committed to creating great financial outcomes for investors and also have the capacity to invest organically and move nimbly on capital allocation whether additional share repurchases or M&A. We will continue to innovate with focus, discipline and rigor anticipating our customers' needs so they can focus on building their companies. 
We have been building Twilio for this moment. Since inception, we provided essential technology infrastructure that accelerated customers through a variety of technology cycles. And today, our newest generation of technology allows another wave of companies in the AI era to move faster than ever. We continue to see an incredibly meaningful set of problems to solve on behalf of our customers in a landscape that is moving fast. We have the financial strength, trusted infrastructure and innovation wherewithal to win through any cycle. 
And with that, I'll turn it over to Aidan.

**Aidan Viggiano** (Executives):
Thank you, Khozema, and good afternoon, everyone. Twilio had a great Q3 and delivering record revenue of $1.56 billion, up 20% year-over-year on a reported basis and 16% year-over-year on an organic basis, which excludes incremental U.S. carrier pass-through fees. Non-GAAP gross profit grew 18% year-over-year. We also generated record non-GAAP income from operations of $326 million and record free cash flow of $370 million. Top line performance was driven by broad-based strength across our product portfolio and key go-to-market focus areas. Our self-serve channel delivered 30% plus revenue growth, while ISV revenue grew 20% plus. 
Messaging revenue growth was 24%, driven primarily by strong volumes and aided by growth in WhatsApp and RCS. Incremental carrier fees contributed roughly 7 points to messaging's growth. Voice revenue grew 20% plus, once again, driven by a balance of volume growth and software add-ons. We continue to see strong growth from AI native and adoption of software add-ons such as Branded Calling, Conversation Intelligence, Conversation Relay and Verify. 
Finally, total software add-on revenue growth was 25% plus and support and services grew 30% plus. Our Q3 dollar-based net expansion rate was 114% reflecting the improved growth trends we've seen in our business over the last several quarters. Incremental carrier fees contributed roughly 4 points to DBNE. We delivered record non-GAAP gross profit of $768 million, growing 18% year-over-year, our third consecutive quarter of 15% plus non-GAAP gross profit growth. This was driven by continued momentum in our higher-margin products in addition to our proactive efforts to deliver meaningful cost efficiencies across our platform. 
Non-GAAP gross margin was 49.2%, down 90 basis points year-over-year and up 20 basis points quarter-over-quarter. We incurred incremental U.S. carrier pass-through fees of $53 million, which drove the year-over-year decline. Without these incremental fees, non-GAAP gross margin would have been up 80 basis points year-over-year and up 30 basis points quarter-over-quarter. Q3 non-GAAP income from operations came in ahead of expectations at $326 million, up 39% year-over-year and our fastest growth rate in over 2 years, driven by strong gross profit growth and continued cost leverage. 
Non-GAAP income from operations benefited from roughly $11 million in platform credits, which was higher than we anticipated. Non-GAAP operating margin was 21%, up 290 basis points year-over-year and up 190 basis points quarter-over-quarter. Our Q3 non-GAAP operating margin includes a roughly 70 basis point headwind from incremental U.S. carrier fees. We generated $149 million in GAAP income from operations, up 263% year-over-year. Q3 stock-based compensation as a percentage of revenue was 9.9%, down 230 basis points year-over-year and up 40 basis points quarter-over-quarter. We generated record free cash flow of $370 million in the quarter. Additionally, we completed $127 million in share repurchases in Q3 and have roughly $700 million remaining on our current buyback authorization. 
Turning to guidance. For Q4, we're initiating a revenue target of $1.595 billion to $1.605 billion, representing 17% to 17.5% reported growth and 11% to 12% organic growth. Our Q4 reported revenue guidance assumes approximately $75 million in incremental U.S. carrier fees. As a reminder, our organic revenue excludes the contribution from incremental increases to U.S. carrier fees and acquisition-related revenue. In addition, we expect non-GAAP gross profit growth to be similar to organic revenue growth in Q4 due to higher hosting costs for the holiday shopping season and with our e-mail cloud migration now behind us. 
Based on our year-to-date performance and our Q4 guidance, we're raising our full year 2026 organic revenue growth outlook to 15%, up from 13% to 13.5% previously. We are raising our reported revenue growth outlook to 20%, up from 18% to 18.5% previously. In addition, we continue to expect full year non-GAAP gross profit growth to be similar to our organic revenue growth rate. Our full year revenue guidance assumes approximately $245 million in incremental pass-through revenue from U.S. carrier fees. 
As a reminder, while the pass-through fees have no impact on our gross profit, income from operations or free cash flow dollars, they do impact our margin rates. For modeling purposes, we would expect the incremental fees to reduce our full year 2026 non-GAAP gross margin by roughly 200 basis points when compared with our full year 2025 non-GAAP gross margin, all else equal. 
Turning to our profit outlook. For Q4, we expect non-GAAP income from operations of $300 million to $310 million. We are raising our full year 2026 non-GAAP income from operations range to $1.19 billion to $1.2 billion, up from $1.135 billion to $1.155 billion previously. Similarly, we are raising our full year free cash flow guidance to $1.19 billion to $1.2 billion. 
Before we open the call for questions, we also wanted to provide a preliminary outlook for 2027. We've delivered 9 consecutive quarters of double-digit organic revenue growth alongside consistent operating leverage and are in a strong position heading into the year-end. Based on the trends we see in the business, we expect full year 2027 organic revenue growth of at least 10%, well above our 2025 Investor Day framework of 7% to 8% annual organic revenue growth. We expect 2027 non-GAAP gross profit growth to be similar to organic revenue growth. 
Turning to profitability. We expect 2027 non-GAAP income from operations of at least $1.35 billion above our most recent guidance of at least $1.23 billion, which we provided on our Q4 2025 earnings call. We also expect free cash flow of at least $1.35 billion. 
We will provide more commentary on our fiscal 2027 outlook on our Q4 '26 earnings call. Finally, Twilio will host an Investor Day in conjunction with our upcoming SIGNAL Conference taking place in San Francisco on April 13 and 14, 2027. I'm very pleased with the strong revenue and gross profit growth we delivered in the third quarter as well as our ongoing financial discipline that is driving strong profitability and free cash flow. We remain focused on our key go-to-market initiatives and on delivering the essential infrastructure that will help our customers win in the AI era. 
And with that, we'll now open it up for questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Elizabeth Porter from Morgan Stanley.

**Elizabeth Elliott** (Analysts):
I just had a first question, just in the first half of the year, you saw organic revenue growth outperform guidance by a bit of a larger-than-normal magnitude in the first 2 quarters, whereas the magnitude of beat now is just a little bit more modest and more normalized in Q3. So could you help us unpack what drove the upside relative to your expectations this quarter? And were there any tailwinds that particularly benefited growth in the first half of the year that began to change in Q3 and how that trends through Q4?

**Aidan Viggiano** (Executives):
Yes. Thanks, Elizabeth. So yes, I want to make a couple of points on that. So first, as we have said kind of consistently since the last earnings call, we didn't and still don't expect 5%-plus beats that we saw in both the first and second quarter to kind of be the new normal. We beat the Q3 guidance, high end of our guidance by roughly 4 points. And over the last 3 or so years, if you look at our quarterly beat, they kind of range from 2% to 4%, so kind of just in the mix there. When you look at this quarter, I'd say the smaller revenue beat in the quarter was primarily driven by Messaging, which decelerated modestly from 18% growth in Q2 to 17% organic growth in Q3.
The rest of the business, if we look at voice, the software add-ons, the self-serve business, they kind of grew consistently quarter-to-quarter. So a modest deceleration in Messaging. And that is our biggest product at about 60% of our revenue, and that's really what the primary driver was.

**Operator** (Operator):
Our next question comes from the line of Alex Zukin of Wolfe Research.

**Aleksandr Zukin** (Analysts):
I guess maybe on the point about Messaging decelerating slightly. I mean, we're seeing all of the personal agent kind of stuff going on between multiple vendors. Maybe when -- what is the tailwind there, if any, for Twilio? When would you start to see that show up and then maybe because what is Twilio's right to win in this kind of compliance identity space? And maybe any reason -- that given some of the incremental products that you're putting out there and the success of the initiatives with conversation, any reason why gross profit growth shouldn't outpace organic revenue growth next year?

**Aidan Viggiano** (Executives):
Alex, let me start a little bit on Messaging. It wasn't your direct question. But as we look at the quarter and the deceleration that we saw, the primary driver of that was the ISVs. They did moderate a bit as we started to lap tougher comparisons back in the third quarter of '25, that's when we saw that sales segment kind of accelerate above 20%. So the Messaging deceleration was really just a tougher comparison relative to the first half of the year. All right, I'll hand it over to Khozema to talk about consumer agents.

**Khozema Shipchandler** (Executives):
Yes. I mean, Alex, I would say on the consumer agent side, I mean, we definitely have a right to win. I think -- I mean it's been a few weeks, obviously, since all of these different agent platforms have launched, we're working with all the leading companies, I'm not going to get into specific names, but you can take some signal from that. From our perspective, it's very much on the come, but it's going to take some time. I mean the way that we characterize voice AI in our prepared remarks is that it's about 1% of what the voice interactions are so far. I mean, that's very, very underpenetrated, which means that there's a lot of sort of tailwind on the come.
As it relates to consumer AI, it's a fraction of that. So again, I think there's a lot of activity that's on the come, and I think we'll be a beneficiary of that. So we're very excited about what's coming and what's still developing. And I think, honestly, like fragmentation is actually relatively useful for us here as well. That kind of goes to identity. In the identity space, I mean, I think it's just like a natural add-on for many of the things that we're already doing. We're already in the transactional flow as I said a moment ago, there's a lot of fragmentation. I think the idea of having every one of these agents, if you're the consumer being validated on the way in and having a neutral party be able to adjudicate that, like that's kind of the idea behind it. And the customers that we've spoken to are very excited about the prospect of that. 
Similarly, business adoption has been slow so far, but as it starts to pick up, they're going to require the same technology. And so that kind of works both ways, which is why we're excited about it. And then I think over time, you're right that conversations or some of the other products, like they will help with respect to gross margins and gross profits. But I think as Aidan has said, like very consistently over the last many years, like Messaging is really the weight of the business. And the growth characteristics of messaging, just given that it is structurally lower, they tend to drive the overall margin rate of the business. But on balance, when you start to exclude fees and some stuff like that, like we have been doing pretty well from a margin perspective, and I would attribute it to some of our more software-like products, if you will.

**Operator** (Operator):
Our next question comes from the line of Taylor McGinnis.

**Taylor McGinnis** (Analysts):
Maybe, Aidan, one for you and then Khozema, one for you. Aidan, just on despite the decel in Messaging, if I look at the 4Q organic growth guide, it's very similar to how you guided 3Q. So could you just maybe walk through some of the drivers of that I know there's the holiday season, there tends to be a seasonal uptick in the Messaging business. So could you just walk us through like the guide there? 
And then secondly, Khozema for you, you guys mentioned a bunch of big voice wins, and it sounds like momentum of the pipeline is going really well. But you made the comments about it still being early in some of the stuff taking time. So just in comparison to the over 20% growth, like when could we reach that inflection point? And where are we with the customers in that?

**Aidan Viggiano** (Executives):
Thanks, Taylor. I'd say on the guide, like we're really encouraged by the revenue trends, the performance that we've seen in the business, both in terms of volumes, but as well as our go-to-market execution. And importantly, it's been really broad-based. So Messaging did decel a point. But when you look at the guidance trends, we're guiding to 11% to 12%, that's consistent with Q3, but that's our strongest quarterly revenue guidance in several years. So we feel pretty good about that. 
Now that said, consistent with how we've guided for the last few years, and as you know, we continue to plan prudently. We are a usage-based business. Q4 is a more volatile quarter for us just given holiday seasons and things like that. And as I said earlier, we've historically kind of delivered organic revenue base of 2% to 4%. We view that range is more than norm than kind of what we saw in the first half of the year. Beyond that, I wouldn't really call out anything unusual for Q4.

**Khozema Shipchandler** (Executives):
Taylor, with respect to the Voice wins and kind of the overall momentum, I mean, it's definitely progressing well from our perspective. It's definitely driven some of the elevated growth that you see on the Voice channel, like that's been very exciting, obviously, for us, and it's great to see that channel doing so well. I think in terms of like broader, more mainstream adoption I think a lot of that is still on the come. Like the customers that tend to drive the biggest volumes tend to be in regulated industries, traditionally, financial services, health care and insurance, like those 3, in particular, drive a lot of volume. I think they're still experimenting a lot, I mean, heavily with AI. But I think for the -- once they adopt some of these Voice AI use cases, like then you'll start to see it really pick up. 
For now, it's predominantly been retail, e-commerce, foodservice, stuff like that. And obviously, you've seen some pickup in customer service as well. But as I mentioned in my answer to the prior question, it's still 1% penetration in terms of the total available voice minutes out there. And so from our perspective, this is a great setup, right? I mean we have 99% of it to go in a market that's probably growing. And so there's just a lot of tailwind here and a lot of growth available for Twilio.

**Operator** (Operator):
Our next question comes from Samad Samana of Jefferies.

**Samad Samana** (Analysts):
I will also give one for Khozema, one for Aidan. Kho, for you, just on the identity product, can you help us think about how monetization there looks? And you said it's early in the release. But if you could just give us some examples of what the price uplift looks like when that's attached. And is that the use case there for agent to human, human to agent or agent to agent. So maybe just digging deeper into identity. 
And then Aidan for you on the 2027 preliminary outlook, thanks for giving that, I think it's very helpful to look ahead. Can you just help us unpack what you're assuming around messaging and the nonmessaging products and whether we should think about messaging is stable versus accelerating what we saw this year, just dig deeper into both those?

**Khozema Shipchandler** (Executives):
Yes. Let me start, Samad. So on monetization, look, we haven't quite worked out the model yet. I mean it's -- again, it's a private beta. It's very early. I think what you can probably anticipate is it'll be usage-based kind of in conformance like with the rest of our revenue model. I think that puts us in the right set of customers. You can imagine like having identity resolution happen based on different times that an agent, human, et cetera, is interacting with a different business. The product is meant to suit all of the use cases that you referenced. So agent to human, human to agent, agent to agent. So in that way, it will be quite versatile. 
Finally, I would expect that it does provide a gross margin uplift that will have more software margin like characteristics. And so that's another reason that we're pretty encouraged by it. But again, quite, quite early days. It's in private beta. We'll talk about it in a more fulsome way, including pricing, packaging and margin characteristics when we get into GA next year.

**Aidan Viggiano** (Executives):
And then on your 2027 question, we were intending to give some directional guidance here. I mean we feel really good about the trends in the business. Messaging is performing quite well. Voice, the software add-ons, some of our largest products. So all of those kind of factor into the outlook. We're not going to get much more specific than that right now. We will dive deeper into 2027 at our Q4 earnings call.

**Operator** (Operator):
Our next call comes from the line of Samik Chatterjee of JPMorgan.

**Samik Chatterjee** (Analysts):
Maybe on the voice side, you've had this 20%-plus growth consistently in the recent past. And you highlighted that it comes both from volume and software add-ons. Is there any way you can sort of break that down a bit more granularly for us in terms of how does the balance of volume versus software add-ons sort of contribute to that 20%-plus growth right now? And particularly, as you think about next year, I know you said that overall for voice is still early days, but how are you thinking as you sort of think about next year or maybe in the next couple of years, where does the greater sort of growth opportunity lies? Is it volumes or do you see a bigger opportunity around software add-ons?

**Aidan Viggiano** (Executives):
Yes, I'll start with just the split of the voice growth. It's actually pretty balanced. I mean we're seeing a lot of strength in the software add-ons. We see triple-digit growth in some of the Branded Calling, Conversation Intelligence to name a couple. And so really, we are seeing minutes grow, so volumes grow, and we're seeing the attach rate with the software add-ons grow quite quickly as well.

**Khozema Shipchandler** (Executives):
Yes. Just to add to that a little more on some of the use cases that we're seeing, particularly with voice AI. A couple of quarters ago, it was a lot of proof of concepts. Those concepts have now rolled into production. We're starting to see real realization of our customers, whether it's AI natives or some of the traditional ISVs that are embedding voice into their platforms, really start to reach some significant scale with their voice usage, and we talked about a few of those customers already in terms of the return that they're getting on it. But we're really encouraged with the overall mix that we're seeing, Branded Calling the conversation suite in general, is really helping us accelerate the software add-on part of our business, which grew well over 25% this quarter.

**Operator** (Operator):
Our next call comes from the line of Ittai Kidron of Oppenheimer & Company.

**Ittai Kidron** (Analysts):
Maybe a couple for me. First, Khozema, as you think about the business going forward, help us think from your perspective, what is the right KPI to follow here because revenue is going to swing back and forth with Messaging. And clearly, that's a very important part of your business. But a lot of the focus and a lot of the value that investors put on your business is really tied into your nonmessaging business longer term, right? 
And so I guess the question is, if those businesses are small and even though they're ramping, it's going to be hard to move the dial from a revenue standpoint. Is gross profit the right way to look at it or any other KPI? And in that context -- and I understand, Aidan, this is a preliminary '27 guide, why should gross profit grow in line with revenue? Why should it not grow faster? I would appreciate that.

**Khozema Shipchandler** (Executives):
Yes. I mean, I can start. Look, I think, Ittai, we're in general, trying to drive a balanced P&L. And I mean if you look at just like what we've accomplished over the last several years, I mean, we've accelerated revenue pretty substantially. I mean we're up very significantly from the preliminary guidance that we gave at our Investor Day 2, 3 years ago. We've driven significant operating leverage. We've driven a ton of cash. We've reduced dilution. So I think when you look at like the totality of the P&L, like that's generally been a pretty good payoff for investors. 
As we look forward, I mean, clearly, the goal is to be able to continue driving growth at elevated levels. I think that this quarter and certainly the last couple have provided evidence that we're able to do that both as a result of significant effort and investment on the self-serve side as well as great go-to-market execution in terms of both our enterprise as well as our ISV customers. We're just seeing really good balanced growth across the board. Now more specifically to some of the line items in the P&L. I mean, the thing that we focus on day-to-day is predominantly gross profit growth. 
So now we get asked this question like a lot of different ways from you all and from other investors. We don't do it necessarily like at the expense of revenue growth. And we don't work it the other way, and it's a balance, like we're trying to drive whatever the best long-term outcomes are overall for the business. And so given the usage-based nature of it, given that the mix can tilt a little bit from quarter-to-quarter, you do have like a little bit of these up and down dynamics. 
Like we certainly understand that as the people that are running the business day to day, I think you guys understand it as folks that have followed the business for a long time, and we just have to kind of roll with that. But over a long period of time, we think that there's a great balanced P&L outcome for investors. In the last 3 years, I think it provided very, very compelling evidence that we're going to continue driving that.

**Aidan Viggiano** (Executives):
Yes. I mean, Khozema covered a lot there. Maybe just a couple of other things I'll hit on gross profit. I do want to talk about Q4 a minute because I said Q4 would be -- gross profit growth would be in line with revenue. Remember, in Q4, we have the big holiday season, we tend to provision more from a hosting perspective in that period. So that does come with additional costs. In addition to that, we have started to lap some of the cost tailwinds that we've seen in the business. 
So we moved to e-mail, for example, from on-prem to the cloud that provided a gross margin tailwind for the better part of this year. That's fully in our run rate now. So those kind of GM tailwinds go away. Now that said, when you look at what really drives gross profit outpacing revenue, it is the higher-margin products growing quite well, as well as continued cost actions. We're going to continue to do both of those things. But as Khozema said Messaging has lower gross margin, carries low gross profit for every dollar of revenue, and it's 60% of our business. So that can obviously influence outcomes.

**Operator** (Operator):
Our next question comes from the line of Callie Valenti of Goldman Sachs.

**Carolyn Valenti** (Analysts):
I wanted to ask on the Voice part of the business, realize when we get the numbers quarterly, they're not exactly the growth numbers that you guys see in front of you. But Voice been roughly kind of 20% plus over the last couple of quarters now after accelerating more in the quarters prior to that. What are some of the pieces that could bring that up further over the next couple of quarters? And have you continued to see this demand step up on a quarterly basis? Or do you think we have reached a more stable environment as companies roll out AI in a more measured way?

**Thomas Wyatt** (Executives):
Callie, it's Thomas here. So just to think about Voice by the particular cohorts of customers that we have, starting with self-service, growth in voice has been over 50%, and that's a good leading indicator of the adoption of the channel itself. And then, of course, adding software -- voice software add-ons on top of that continues to accelerate that. So we're seeing that as a good leading indicator for momentum. The second is the AI natives, the ones that have been born with voice use cases, they're continuing to expand with us, and they were growing as they're growing. And we're also seeing them adopt second and third channel. 
So a number of our voice AI customers are now adding WhatsApp or Messaging or other types of Brand Calling and other services. And so we're seeing that as a nice accelerant as well. And then additionally, there's a lot of consolidation in the enterprise space where traditional contact centers, customers are looking for a more agentic way of doing voice services in enterprise motions and in that case, moving more to a headless type of voice interaction experience combined with the other messaging types that we offer along with orchestration of memory. And so that's been a nice catalyst for us as well. 
So as I mentioned earlier, there's been a lot of proof of concepts that have gone into production recently. We're encouraged by the momentum and the results our customers are getting. And so we think that's a pretty good indicator of future success with voice.

**Operator** (Operator):
Our next call comes from the line of Siti Panigrahi of Mizuho.

**Sitikantha Panigrahi** (Analysts):
Just a follow-up to the prior question, where the value accrues, if you see -- I know you call it early stages now in AI super cycle. But frontier labs, even agent builders, they're all moving into voice. Voice is exciting. But as you look forward to next maybe over 5 years, where do you see the value accrues like Twilio can bring? Is it on the connectivity context, identity side or any other layer that you are pretty confident that you can keep? And also like what has to change for the voice AI to move beyond like these AI native and nonregulated verticals? Like what are the leading indicators you are watching?

**Khozema Shipchandler** (Executives):
A lot there, Siti. So let me just kind of start with our value proposition and you mentioned like a number of players kind of moving into the space. I mean the one thing is that I think what really advantages us relative to other players is like we're the neutral party. And so virtually every player in the space who are predominantly participating at the application layer, they are running off of Twilio's rails. Like that is a really, really great spot to be in because ultimately, we're providing underlying infrastructure on top of which we're able to add capabilities like Intelligence, like Memory, like Orchestration, as Thomas alluded to a second ago. 
We can also add things like Branded Calling to be able to improve conversion rates and things of that nature. And so the ability to provide this full service offering at the infrastructure level allows us to win with every single one of the providers irrespective of what it is that they're trying to build and how they're going to market with their different customers. So I would say it's a starting point, like that's a major advantage in the broader ecosystem. 
Customers continue to come to us for that infrastructure, for that programmability, for the different aspects of the conversation suite that I mentioned a second ago. I think it's just the technology adoption cycle. Like I mean, I don't think there's a number of like KPIs that necessarily have to be unlocked here, it's just going to happen as time goes on. I mean as consumers become more and more comfortable with the utilization of AI, it will pick up more as businesses start pushing the technology out to their consumers additionally, like we'll start to see the pick up more and more. I mean the reality is like, when we sell it, the ROI is very compelling. I mean we're able to generate more revenue, reduce costs, create a better consumer experience, but it's going to take time. 
And I'm not surprised that the regulated industries have taken more time. That's how every technology cycle has played out. So I'm very, very optimistic about the way that it's played out so far. It certainly feels great about the way that I would expect it to play out going forward. And as Thomas alluded to a second ago, when you look at the top of the funnel, which is really like vis-a-vis self-serve, like growing at over 50% on voice there, like that's a pretty encouraging signal. So I think we just have to continue executing and there's a lot of demand on the come.

**Operator** (Operator):
Our next call comes from the line of Arun (sic) [ Arjun ] Bhatia of William Blair.

**Arjun Bhatia** (Analysts):
Two, if I can. One for Aidan, maybe I want to ask the P&L question directed to a different metric for this quarter. I saw obviously, the op income growth was very strong. I think even after I back out the $11 million in credits, it was very healthy, and it seems like that's sort of being given back next quarter. I'm just curious if there's additional investments and growth investments you're planning to make or if there's something else at play there? 
And then Khozema, one for you. I'm just curious how you view sort of these emerging agent to agent protocols? I know it's super early, but is that a tailwind for Twilio given some opportunity around orchestration and governance and identity as you talked about? Or does it potentially take some volume off of sort of traditional telephony and move it to other rails? I'm curious how you think that might evolve over time.

**Khozema Shipchandler** (Executives):
Yes. Maybe I'll start, and then Aidan can talk about op income here in a second. I think it's all tailwind. I mean I think the reality is like it's a very fragmented landscape right now. You've got a number of these different companies. As I said earlier, all of the leading companies are already working with us. I mean it's not just like the messaging and e-mail content, like there's the service operations that go with it as well. There'll be voice content. So we see what's been playing out so far as like a lot of tailwind going forward for the overall business. 
In terms of the protocols themselves, I would call them probably policies over protocols, like what they've stipulated is kind of a set of things that one should follow as these agent to agent interactions are transpiring. We certainly conform to the different policies that are being written. They're also quite varied. And so here again, I think fragmentation kind of plays to Twilio's strengths, like our ability to work across any policy framework, any protocol framework, any technology, that's a great setup, not just for our core business in channels. It also helps to sell a lot more context and then I would say, going forward, it's a great setup for identity. So no matter how you kind of cut it, we look at the whole thing as a lot of tailwind for Twilio.

**Aidan Viggiano** (Executives):
Hey, Arjun, on your profit question, yes, we delivered very high op profit in Q3, $326 million, it was up nearly 40% year-over-year, it's up 14% quarter-over-quarter. As you called out and as I mentioned in the prepared remarks, we did benefit from roughly $11 million in platform credits, which were higher than we had anticipated. So that creates a slightly larger optical gap in our Q4 guidance. .
The other thing I'd say is we did make some investments in head count in the quarter, both R&D and go-to-market. Those are incorporated into our guidance as well. And then lastly, of course, as you know, we continue to just plan prudently just given the usage-based nature of the business.

**Operator** (Operator):
Our next call comes from the line of Nick Altmann of U.S. Bancorp.

**Nicholas Altmann** (Analysts):
I wanted to ask a question about how some of the AI use cases in software add-ons have this pull-through dynamic, which results in higher volumes. Because Khozema, you've talked about how voice AI agent use cases actually result in longer duration calls and then there's products like Branded Calling, which can actually drive higher answer rates and allow customers to do more outbound calling. And so my question is, how should we think about the overall uplift in terms of the volume of minutes or messages when it comes to customers that begin to embed voice AI agents or when they have products like Branded Calling or Conversation Memory or other offerings?

**Khozema Shipchandler** (Executives):
Yes. I mean, I think, broadly speaking, you should expect call duration to go up from where it is today. Like I think most calls and service environments today are measured on cycle time. I think going forward, the way that customer service operations will probably measure contact centers is based on the outcomes that are being created for the consumers on the other side. So I'm certainly not suggesting that like what used to be a 60-second call is going to go up to like 10, 20 minutes, I'd say that's not a great outcome necessarily. But I do think there will be an uplift as a means to being able to, a, solve the consumer's problem. 
But b, there's also like a big opportunity for real revenue uplift on the part of the business, right? So they can cross-sell, upsell their customers a lot better. And especially if they're using a context layer underneath their ability to source details about the consumer that they're serving in real time and then be able to create like kind of packages and prices of additional items like that's pretty compelling. 
Beyond all that stuff, the Branded Calling and other intelligence capabilities as part of the conversation suite, like that's all uplift. And so those, as you know, like provide price adders. But ultimately, like ROI is, I think, what wins the game here. And I think Twilio has an offering when you combine our channels, combine it with context and then add in things like Branded like makes for a really, really compelling offering leads to better conversion, better revenue, lower cost and ultimately better consumer outcomes. And I think that's why you've seen the growth characteristics that you have.

**Operator** (Operator):
Our next call comes from the line of Koji Ikeda of Bank of America.

**Koji Ikeda** (Analysts):
I wanted to follow up on an answer you gave earlier about self-service voice growing 50%. And so how predictive has self-service historically been around broader voice growth? And what sort of lag do we expect from self-service growth -- self-serve customers growing versus the revenue going up from it?

**Khozema Shipchandler** (Executives):
I mean I could talk a little bit about the use cases and then, Aidan, maybe if you want to get into more of some of the historicals on it. But when you think about the use cases we're typically seeing with voice with self-service, a lot of it is the autonomous AI-powered customer engagement use case. And it often starts with an AI native that's beginning to unlock a new vertical application or agent. From there, they need to complete sort of a holistic customer journey as they get some product market fit, they start to increase their volumes then we typically see that they'll add a second channel because most voice experiences are only just one channel is not enough. You need to be able to communicate to customers with -- through omnichannel experiences. 
So then we tend to see the Messaging get added, the conversation suite get added and ultimately, I think, as we said in previous conference calls that 60% plus of our enterprise customers started in self-service, and we see that natural expansion of our self-service customers continue and even this quarter, if you look at our $1 million customer cohort growth, it's growing as fast as it has in a long time. So we're really encouraged about the trends starting in self-service, how that translates into enterprise adoption over time and how these companies become $1 million-plus customers for us.

**Aidan Viggiano** (Executives):
Yes. And then from a self-serve perspective, I'm not going to give any numbers specifically, right? But this is where we do our customer acquisition, right? This is where the AI native kind of all get started on our platform. When you think about voice in context to our kind of voice self-serve, just for context, right, our total self-service is roughly like 15% of our revenue. Voice is a small -- relatively a smaller portion of that, obviously, just given the size of Messaging and some of the other businesses. 
So first of all, it's a relatively small part of our revenue. It's growing very quickly. As Thomas said earlier, it's growing about 55%. And with a lot of these natives, we partnered very closely with them over the last couple of years, they typically come in, started on voice rails from a kind of programmable voice perspective. We've added software add-ons on top of that. 
In many of these cases, we've seen growth really accelerate and they're meaningful customers today. I mean, last quarter, we called out a horizontal conversational AI company that started building with Twilio in the Voice channel. In Q1 of '25, they were generating kind of low 6 figures quarterly spend on Twilio, and it was almost all voice connectivity. Since then, their quarterly connectivity spend has tripled, their software add-ons has gone from essentially nothing to nearly $0.5 million in the most recent quarter. 
And so you can see they've gone from a relatively small customer, now they're leveraging our media streams, our conferencing capabilities, answering machine detection, a lot of our software add-ons, and they're over $6 million annual run rate, growing like 65% with us. So that's the kind of thing we're seeing. It's happening. It's a relatively small part of our business today, but it's growing really quickly. And it's exciting to think about what it could be.

**Operator** (Operator):
Our next call comes from the line of Ryan MacWilliams of Wells Fargo.

**Ryan MacWilliams** (Analysts):
I'd love to hear about how the AI opportunity is evolving for the Messaging business. Are your customers starting to see higher ROI on AI SMS use cases? Like maybe they're trying more customer service SMS AI use cases or starting to get more interested in RCS? And then separately, how are trends for e-mail in the quarter? And did you see any positive or negative impacts from AI within e-mail?

**Aidan Viggiano** (Executives):
Yes. Email was pretty consistent. Business is growing pretty well. It's a little bit lower than our kind of company average, but nothing to call out from a change in trend perspective. And I'd say early days from an AI perspective on e-mail.

**Khozema Shipchandler** (Executives):
In terms of the AI opportunity on Messaging, I mean, I think you're certainly seeing it start based on like just the take off with some of the consumer stuff, you're definitely seeing some activity there. I think you asked a slightly different question in terms of RCS and the ROI there. The ROI in RCS has been very, very significant. I mean it's been a very fast-growing product for us. 
It's little bit more challenging adoption cycle, if you will, just based on some things that have to be done as part of the onboarding process. But the technology is fantastic. Customers who are using it are getting a ton out of it. It obviously comes with a lot of branding built into it as well. And so customers who are on it are really enjoying it and getting superior ROI relative to kind of traditional messaging, I would say.

**Operator** (Operator):
Our next call comes from the line of Derrick Wood of TD Cowen.

**James Wood** (Analysts):
Khozema, when it comes to these new consumer AI agents, I know you're saying it's still early, but you did indicate you're working with leading product companies already. So can you just help us frame kind of where you see the lowest hanging fruit when looking across your various communication channels? And then when it comes to the consumer brand side,  do you see them starting to feel a need to stand up more agentic support systems to handle all the inbound agent volumes? And how would you frame the opportunity for Twilio there?

**Thomas Wyatt** (Executives):
Derrick, it's Thomas here. A couple of points. So we are working with all the major players, but this is an interesting area where the consumer agents also has a long tail of smaller, lesser-known consumer agent companies that we're also working with. And it could be everything from outbound voice, helping these companies set up the telephony infrastructure to make calls on the consumers' behalf. There's the messaging and texting capability. There's the verification and OTP capability resulting in authenticating these agents properly. 
So we're participating and helping the consumer side of this with blueprints so that these companies can set up their communication infrastructure powered by Twilio to be able to have these agents transact on behalf of the consumers. On the flip side, I'd say there's even more acceleration of businesses trying to get ready for these consumer agents. And that's accelerating the conversations in the demand for helping our business customers set up virtual agents to be able to field the consumer agents that are coming more inbound. 
And so it's really an interesting flywheel effect that's early days. So it's very early, but a lot of proof of concepts, a lot of early experimenting going on, and we're excited about the long-term potential for it.

**Operator** (Operator):
Our next call comes from the line of Parker Lane of Stifel.

**J. Lane** (Analysts):
Aidan, earlier, you talked about the impact of Messaging you saw from ISVs moderating off the tough compares. Is that a comment or something that you saw across all the ISV relationships broadly or were some of the long-tenured ISVs versus the AI natives more impacting that figure?

**Aidan Viggiano** (Executives):
Yes, I'd say it was not every ISV we sell in the quarter, obviously. So overall, they did tended to be focused on a few of them. But nothing specifically to call out there or give more on.

**Operator** (Operator):
Thank you. At this time, this concludes our question-and-answer session. Thank you for your participation in today's conference. This now concludes our program, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TWLO_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：Q3 營收財測區間（原話："revenue target of $1.505 billion to $1.515 billion"）
- 2026-08-06｜CFO｜guidance：Q3 財測對應的報告與有機成長率（原話："16% to 16.5% reported growth and 11% to 12% organic growth"）
- 2026-08-06｜CFO｜guidance：全年有機營收成長財測上調（原話："raising our organic revenue growth range to 13% to 13.5%"）
- 2026-08-06｜CFO｜guidance：全年報告營收成長財測上調（原話："raising our reported revenue growth range to 18% to 18.5%"）
- 2026-08-06｜CFO｜guidance：全年非 GAAP 毛利成長預期（原話："we continue to expect full year non-GAAP gross profit"）
- 2026-08-06｜CFO｜guidance：全年財測含美國電信業者附加費轉嫁收入約 2.5 億美元（原話："approximately $250 million in incremental pass-through"）
- 2026-08-06｜CFO｜margin：附加費對 2026 全年非 GAAP 毛利率的建模影響（原話："roughly 210 basis points when compared with our full year"）
- 2026-08-06｜CFO｜guidance：Q3 非 GAAP 營業利益財測（原話："income from operations of $285 million to $295 million"）
- 2026-08-06｜CFO｜guidance：全年非 GAAP 營業利益財測上調（原 10.8 億至 11 億）（原話："up from $1.08 billion to $1.1 billion previously"）
- 2026-08-06｜CFO｜guidance：全年自由現金流財測（原話："free cash flow guidance to $1.135 billion to $1.155 billion"）
- 2026-08-06｜CFO｜guidance：CFO 指 Q3 有機成長財測為三年來最高（原話："the highest guidance that we've offered in 3 years"）
- 2026-08-06｜CFO｜commitment：CFO 表示 Q1、Q2 超標幅度不預期成為常態（原話："We don't expect that to be the new norm for the business."）
- 2026-08-06｜CFO｜risk：CFO 提到 Q3、Q4 語音與軟體加值的比較基期較高（原話："comparisons in Q3 and Q4 in Voice and software add-ons"）
- 2026-08-06｜CFO｜margin：Q2 非 GAAP 毛利率及年減幅度（原話："was 49.1%, down 160 basis points year-over-year"）
- 2026-08-06｜CFO｜margin：扣除附加費後的毛利率變化（原話："margins would have been up 60 basis points year-over-year"）
- 2026-08-06｜CFO｜margin：Q2 增加的美國業者轉嫁費用金額（原話："incremental U.S. carrier pass-through fees of $71 million"）
- 2026-08-06｜CFO｜margin：附加費對 Q2 非 GAAP 營業利益率的影響（原話："includes a roughly 90 basis point headwind from"）
- 2026-08-06｜CFO｜margin：DBNE 受附加費貢獻約 5 點，剔除後仍季增約 1 點（原話："we did see DBNE accelerate even adjusting for the fees"）
- 2026-08-06｜CFO｜margin：Messaging 成長中附加費貢獻約 10 點（原話："contributed roughly 10 points to Messaging's growth"）
- 2026-08-06｜CFO｜margin：Messaging 扣除附加費後成長約 18%（原話："ex the fees, it grew about 18%"）
- 2026-08-06｜CFO｜margin：毛利成長由高毛利產品推動（原話："continued momentum in our higher-margin products"）
- 2026-08-06｜CFO｜margin：CFO 說明雲端遷移專案基期效應帶動 email 毛利率改善（原話："we lap the cloud migration project"）
- 2026-08-06｜CFO｜margin：與美國主要業者直連 10DLC 與免付費簡訊（原話："secure direct connections for 10DLC and toll-free messaging"）
- 2026-08-06｜CFO｜margin：RCS 毛利率假設（原話："just assume it's roughly in line with the rest of Messaging"）
- 2026-08-06｜CEO｜risk：CEO 承認電信業者加費對小型企業客戶造成壓力（原話："recognize the pressure it creates for our customers"）
- 2026-08-06｜CEO｜product：新版 Console 轉換率提升（原話："90% plus uplift in conversions when compared to the old"）
- 2026-08-06｜CFO｜product：CFO 稱新版 Console 本季對多產品營收貢獻甚微（原話："It didn't contribute much at all in terms of"）
- 2026-08-06｜CEO｜product：CEO 稱 Console 表現高於預期（原話："console has like certainly been above our expectations"）
- 2026-08-06｜CEO｜product：新一代對話平台宣布上線（原話："Our next-generation conversational platform is live."）
- 2026-08-06｜CEO｜customer：Car Finance 247 從 private beta 轉為七位數合約（原話："a move that quickly evolved into a 7-figure deal to"）
- 2026-08-06｜CEO｜customer：本季簽下與領先 AI 公司的八位數合約（原話："The team signed an 8-figure deal with a leading AI company"）
- 2026-08-06｜CRO｜customer：CRO 舉例：AI 原生客戶年化營收 600 萬美元、年增 65%（原話："now a $6 million annual run rate customer growing 65% a year"）
- 2026-08-06｜CRO｜customer：CRO 舉例：垂直型對話 AI 客戶為 900 萬美元客戶（原話："now they're a $9 million customer with software add-ons"）
- 2026-08-06｜CRO｜customer：百萬美元以上客戶群成長逾 20%（原話："$1 million-plus customers, that's growing over 20% as well"）
- 2026-08-06｜CRO｜customer：自助服務通路語音成長逾 50%（原話："was very strong growth with over 50%"）
- 2026-08-06｜CFO｜customer：AI 原生客戶 DBNE 遠高於公司平均（原話："DBNE is way higher than the average for the company"）
- 2026-08-06｜CFO｜guidance：CFO 稱 AI 客群 DBNE 已納入下半年財測（原話："that's factored into the guidance that we're providing"）
- 2026-08-06｜CEO｜product：CEO 稱多數 AI 活動仍在語音（原話："most of the activity continues to be in Voice"）
- 2026-08-06｜CRO｜product：CRO 稱新平台帶動客戶整合支出（原話："there is a trend toward consolidating spend with"）
- 2026-08-06｜CEO｜customer：CEO 稱新創客戶趨勢為整合而非分散（原話："Instead, we're seeing consolidation"）
- 2026-08-06｜CFO｜customer：AI 公司在 messaging 的用量屬傳統用途（原話："companies on messaging is much more a traditional use case"）
- 2026-08-06｜CEO｜competition：CEO 說明中立定位（原話："positioning as being kind of the Switzerland of it all"）
- 2026-08-06｜CEO｜competition：對 OpenAI 類生態夥伴的定位（原話："I think, by and large, partner in this case."）
- 2026-08-06｜CEO｜competition：對 Salesforce、ServiceNow 等紀錄系統業者的看法（原話："they could be a complementor, they could be coopetition"）
- 2026-08-06｜CEO｜risk：CEO 預期 AI 帶動的成長可能有起伏（原話："going to be some ups and downs as the AI story unfolds"）
- 2026-08-06｜CEO｜risk：CEO 稱短期仍以人對人互動為主（原話："it's going to be mostly human-oriented"）
- 2026-08-06｜CEO｜risk：CEO 稱全面代理人對代理人仍需時間（原話："I still think it's going to be a while before it's"）
- 2026-08-06｜CEO｜commitment：CEO 對 AI 順風持續性的說法（原話："significant durability, not just into like 1 or 2 years"）
- 2026-08-06｜CEO｜product：CEO 稱語音 AI 處於很早期階段（原話："it's pretty early innings, very early innings"）
- 2026-08-06｜CFO｜customer：新客戶增加受新對話層與 Console 推動（原話："aided by the release of our new Conversations Layer"）
- 2026-08-06｜CFO｜capital_allocation：Q2 股票回購金額（原話："we completed $66 million in share repurchases in Q2"）
- 2026-08-06｜CFO｜capital_allocation：股權報酬占營收比重下降（原話："compensation as a percentage of revenue was 9.5%"）
- 2026-08-06｜CFO｜commitment：CFO 稱 GAAP 減損不影響未來結果（原話："and will not impact future results"）
- 2026-08-06｜CFO｜commitment：CFO 重申毛利成長與有機營收成長相近（原話："We expect gross profit to grow at a similar rate to"）
- 2026-08-06｜CFO｜guidance：Q2 自由現金流創高（原話："record free cash flow of $353 million"）

### 問答異常語氣（迴避／改口／保留）
- TWLO_Q2_2026_Earnings_Call_20260806.md｜問：UBS 請 CFO 拆解 Q3 財測背後各區塊（messaging、Verify、自助）的假設｜答法：CFO 表示不談 Q3 各區塊，改談 Q2 各通路與產品表現，並說不預期 Q1、Q2 超標 5% 以上成為常態
- TWLO_Q2_2026_Earnings_Call_20260806.md｜問：Morgan Stanley 問第二產品綁定何時開始貢獻營收、是否為 2027 年因素｜答法：CRO 談轉換漏斗與領先指標，未給貢獻營收的時點
- TWLO_Q2_2026_Earnings_Call_20260806.md｜問：U.S. Bancorp 問新 Console 的近期營收影響｜答法：CFO 稱本季貢獻很少；CRO 稱樂觀但說很難預測營收何時實現，未給時程

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
{"date":"20260522","verdict":"B（觀望，等回測 BB 中軌 $140 或 W52 $126 再分批進場；thesis 完整 Q1 FY26 大 beat + FY26 guide raised + GAAP 轉正但估值🟠 + MA ❌ rolling window 數學假象）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"CPaaS organic growth re-accelerate 至 mid-teens 持續，AI agentic overlay 為新成長引擎","columns":{"2Y 驗證點":"FY26-FY27 organic growth 維持 +12-15%；Voice + Messaging YoY 雙位數加速","5Y 驗證點":"5Y organic growth CAGR +10-13%；AI agentic 業務佔 Rev 從 0 升至 ≥ 15%","10Y 驗證點":"10Y organic growth ≥ +7%（through-cycle）","具體數字門檻":"FY26 reported growth 14-15%（management Q1 FY26 raised guide）；organic +12-15%","信息來源":"Q1 FY26 法說會 management 上修 + Mordor Intelligence CPaaS market report 2026-2031","漂移觸發條件":"連 2 季 organic growth TTM 偏離 -3pp → 削弱（QC-34/35）"}},{"id":"H2","text":"Non-GAAP Operating Margin 持續擴張至 25%+，operating leverage 兌現","columns":{"2Y 驗證點":"FY26 Non-GAAP Op Margin 達 19-20%（vs FY25 15%）；FY27 達 22-24%","5Y 驗證點":"FY30 Non-GAAP Op Margin 達 27-30%；FCF Margin 達 25%+","10Y 驗證點":"10Y mature OpM ~30% (mature SaaS)","具體數字門檻":"FY26 Adj OI $1.1B (guidance raised)；FY27 ~$1.4-1.5B；Q1 FY26 GAAP OpM 7.6% +540bps YoY","信息來源":"Q1 FY26 earnings transcript + 2024 Investor Day OpM target","漂移觸發條件":"連 2 季 OpM 擴張 &lt; +50bps → 削弱"}},{"id":"H3","text":"Segment (CDP) + AI agentic 提供差異化護城河，避免 commoditization 陷阱","columns":{"2Y 驗證點":"Segment ARR YoY +10-15%（從 ~$500M 起）；ConversationsRelay 客戶數達 100+","5Y 驗證點":"Segment + AI 業務佔 Rev ≥ 20%（從當前 ~12% Segment only）","10Y 驗證點":"10Y Segment + AI 業務佔 Rev ≥ 30%","具體數字門檻":"Segment ARR YoY +10%；ConversationsRelay 案例如 Scorpion +39% booking 規模化","信息來源":"2024 Investor Day + 2026 SIGNAL conference + JPMorgan Tech Conference","漂移觸發條件":"Segment ARR YoY &lt; +5% 連 2 季 → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"CPaaS commoditization 加速：AWS Pinpoint / Azure Communication Services / Sinch / Bandwidth 持續搶 enterprise 客戶","columns":{"對應假設":"H1","時間尺度":"🔥 中期","監測指標":"NRR (Net Revenue Retention) 季度趨勢；Voice + Messaging organic growth 軌跡；AWS / Azure CPaaS revenue 披露","警戒閾值":"NRR &lt; 100% 連 2 季；organic growth 跌破 +10% 連 2 季"}},{"id":"R2","text":"Segment (CDP) 整合失敗，AI agentic ramp 慢於預期","columns":{"對應假設":"H3","時間尺度":"⚡ 短期","監測指標":"Segment ARR 季度披露；ConversationsRelay 客戶數；agentic AI 案例規模化","警戒閾值":"Segment ARR YoY &lt; +5% 連 2 季；ConversationsRelay 客戶數 &lt; 50 在 FY27 end"}},{"id":"R3","text":"SMS 監管收緊 / RCS 取代 SMS / hyperscaler 全棧整合終局","columns":{"對應假設":"H1, H2","時間尺度":"🐢 長期","監測指標":"美國 A2P SMS 監管 (FCC + CTIA)；Apple/Google RCS interop 進展；AWS Pinpoint / Azure Communication revenue","警戒閾值":"SMS revenue 連 4 季 YoY 萎縮；AWS Pinpoint 公開披露 &gt; $500M ARR；major enterprise customer (top 10) 流失"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"❌","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":183.3,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TWLO_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
