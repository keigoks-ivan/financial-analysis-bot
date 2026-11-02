你是 stock-analyst **v20 判斷 agent**，標的 PYPL（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"PYPL","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenues_gaap","label":"Net revenues (GAAP)","value":8584,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"PayPal Q3 2026 earnings release（8-K 附件）"},"note":"第三方媒體報 consensus 約 $8.71B、未達（僅單一媒體、未經一手來源驗證）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":18.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%（營業利益 $1,613M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"PayPal Q3 2026 earnings release（8-K 附件）"},"note":"未查得"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":16.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%（營業利益 $1,402M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"PayPal Q3 2026 earnings release（8-K 附件）"},"note":"未查得"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":1431,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"PayPal Q3 2026 earnings release（8-K 附件）"},"note":"未查得"},{"id":"f_kpi5_guidance_q4_fy2026","label":"Guidance（Q4 與 FY2026，皆為點估非區間）","value":"Q4 non-GAAP EPS 約 $1.43、GAAP EPS 約 $1.37；FY non-GAAP EPS 約 $5.60、GAAP EPS 約 $5.07","period":"Q3 FY2026（公告於 2026-10-27）","unit":"USD/share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（公告於 2026-10-27）","citation":"PayPal Q3 2026 earnings release（8-K 附件）；FY non-GAAP TM$ 同步上調（第三方報約 $15.6–15.7B，未經一手驗證）"},"note":"dd_numbers_extra.py consensus_revision：FY1 EPS 5.55（2026-10-31 快照），指引 $5.60 略高於共識"},{"id":"f_kpi6_active_accounts_12_mau","label":"Active accounts（12 個月基礎，非 MAU）","value":440,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"PayPal Q3 2026 earnings release（8-K 附件）"},"note":"未查得"},{"id":"f_kpi7_total_payment_volume_tpv","label":"Total payment volume（TPV）","value":487.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"PayPal Q3 2026 earnings release 摘要（YoY +6%）"},"note":"未查得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_pypl_gross_margin_pct","label":"PYPL 毛利率","value":45.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pypl_operating_margin_pct","label":"PYPL 營業利益率","value":18.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pypl_fcf_margin_pct","label":"PYPL FCF 利潤率","value":18.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_xyz_gross_margin_pct","label":"XYZ 毛利率","value":46.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XYZ.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_xyz_operating_margin_pct","label":"XYZ 營業利益率","value":12.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XYZ.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_xyz_fcf_margin_pct","label":"XYZ FCF 利潤率","value":15.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XYZ.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_v_gross_margin_pct","label":"V 毛利率","value":79.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_operating_margin_pct","label":"V 營業利益率","value":65.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_fcf_margin_pct","label":"V FCF 利潤率","value":44.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_afrm_gross_margin_pct","label":"AFRM 毛利率","value":68.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_afrm_operating_margin_pct","label":"AFRM 營業利益率","value":20.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_afrm_fcf_margin_pct","label":"AFRM FCF 利潤率","value":23.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_non_gaap","label":"SBC 占 non-GAAP 營業利益","value":14.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%（SBC $233M ÷ non-GAAP 營業利益 $1,613M；占營收 2.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"PayPal Q3 2026 earnings release（8-K 附件），占比為本 agent 換算"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":58.58,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":16.86,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":63.94,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.55 → 5.55）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.88 → 5.88）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.16,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.41 → 6.4）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.55,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":5.88,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":6.4,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":3.16,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 5.38 → 5.55（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":11.18,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝2.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":2.1,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.42,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.53,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":10.55,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 5.55，分子＝快照價 58.57","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.956,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":3971.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 14251.0、現金 10280.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":830.66,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":52626.81,"period":"2026-11-03","unit":"USD m","basis":"市值 48655.81 ＋ 淨負債 3971.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":34540.98,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（35 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":35976.46,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（40 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.52,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 58.7 / W52 51.71 / W104 62.4 / W250 69.07 / W250 13週斜率 -2.71%"},{"id":"f_ma_w52","label":"52 週均線","value":51.71,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":62.4,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":69.07,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-2.71,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出的競爭者包含銀行、支付網路、數位錢包、BNPL、即時支付、加密貨幣與穩定幣等，並稱新競爭者可能出現、競爭可能加劇。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","excerpt":"Competition also may intensify as new competitors emerge, businesses combine or enter into new partnerships, and established companies in other segments expand to become competitive with various aspects of our business.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"PayPal 線上結帳帝國遭對手擠壓；Q1 品牌結帳僅成長2%","source":"AP via NY1","url":"https://ny1.com/nyc/all-boroughs/ap-top-news/2026/05/26/paypals-online-checkout-empire-is-under-siege-as-rivals-squeeze-its-core-business","excerpt":"PayPal said in its first-quarter earnings report that branded checkout — the company’s most profitable business by margin — grew just 2%.","as_of":"2026-05-26","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Seeking Alpha：品牌結帳流失份額，Apple Pay、Google Pay、Shop Pay 搶份額","source":"Seeking Alpha","url":"https://seekingalpha.com/article/4857713-paypals-branded-checkout-is-bleeding-market-share-while-management-blames-macro","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2023-2025 無任何客戶占淨營收超過10%；2025年底一個客戶與一個夥伴機構分別占應收帳款淨額12%與23%；兩家支付處理商占交易費用56%（2024年48%）。","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","excerpt":"During the years ended December 31, 2025, 2024, and 2023, no customer accounted for more than 10% of net revenues. During the years ended December 31, 2025 and 2024, two payment processors accounted for 56% and 48% of transaction expense, respectively.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"截至2026-06-30，PayPal仍獲S&P、Fitch、Moody's投資等級評等（搜尋未見2026年信評調降）。","source":"SEC EDGAR 10-Q Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/0001633917/000163391726000082/pypl-20260630.htm","excerpt":"As of June 30, 2026, we continue to be rated investment grade by Standard and Poor's Financial Services, LLC, Fitch Ratings, Inc., and Moody's Investors Services, Inc.","as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Q3 2026：線上品牌結帳 TPV 成長連四季維持 1%–2%，管理層預期 Q4 同為 1%–2%；歐盟取消小額免稅造成約 70bp 逆風；2026 非 GAAP EPS 指引上調至約 $5.60","source":"MarketBeat, Transcript: PayPal Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-paypal-q3-earnings-call-highlights-2026-10-27/","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Morgan Stanley 重申 Sell，理由為 take rate 持續承壓與品牌結帳再加速速度；2027 將加碼投資（約三分之二投向品牌結帳與 BNPL）","source":"Zacks, PayPal Q3 earnings call highlights growth and 2027 investments","url":"https://www.zacks.com/stock/news/3017136/paypal-q3-earnings-call-highlights-growth-and-2027-investments","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"分析師共識 2027 營收約 $35.9–36.2B，年增約 4.1–4.4%（Simply Wall St 聚合，約 41–42 位分析師）","source":"Simply Wall St, PayPal Holdings Future Growth","url":"https://simplywall.st/stocks/ch/diversified-financials/vtx-pypl/paypal-holdings-shares/future","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素載明 PayPal 受美國及國際反壟斷／競爭法主管機關審視，可能面臨訴訟、罰款與被迫改變業務做法。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","excerpt":"We are subject to scrutiny by various government agencies regarding antitrust and competition laws and regulations in the U.S. and internationally, including in connection with proposed or implemented business combinations, acquisitions, investments, partnerships, commercial agreements and business practices.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"英國 FCA 對 PayPal、Visa、Mastercard 展開競爭法調查，涉及 PayPal 數位錢包的資金來源與使用相關合約條款。","source":"PYMNTS：PayPal, Visa and Mastercard Face UK Competition Investigation","url":"https://www.pymnts.com/antitrust/2026/paypal-visa-and-mastercard-face-uk-competition-investigation/","excerpt":"The investigation is to determine whether the three companies engaged in “anti-competitive conduct linked to the funding and usage of PayPal’s digital wallet,” the Financial Conduct Authority (FCA) said in a Wednesday (May 6) press release.","as_of":"2026-05-06","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"PayPal 10-Q（2026Q3）揭露 FTC CID、CFPB CID（PayPal Credit）、德國 Bundeskartellamt 程序與英國調查。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001633917/000163391726000088/pypl-20260930.htm","excerpt":null,"as_of":"2026-11-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：跨境交易是重要營收與獲利來源，且可能受新增或變動關稅、貿易爭端、制裁、進出口管制影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","excerpt":"Cross-border trade (i.e., transactions where the merchant and consumer are in different countries) is an important source of our revenues and profits.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K MD&A：關稅等因素造成的總體環境惡化可能影響消費與信用損失，公司無法合理估計對財務的總影響。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","excerpt":"We are unable to reasonably estimate the total potential impact on our financial results that may ultimately result from such changes in the macroeconomic environment.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Truist 調降 PayPal 目標價，理由為跨境交易量疲弱。","source":"247wallst: Truist Cuts PayPal Price Target as Cross-Border Volume Weakness Bites","url":"https://247wallst.com/investing/2026/05/12/truist-cuts-paypal-price-target-as-cross-border-volume-weakness-bites/?.tsrc=rss","excerpt":"Russell 20002,822.60+0.30% S&P 5007,596.20+0.12% Dow Jones52,224.00+0.83% Nasdaq 10028,296.80−0.40% Russell 20002,822.60+0.30% S&P 5007,596.20+0.12% Dow Jones52,224.00+0.83% Nasdaq 10028,296.80−0.40% Russell 20002,822.60+0.30% S&P 5007,596.20+0.12% Dow Jones52,224.00+0.83% Nasdaq 10028,296.80−0.40% Russell 20002,822.60+0.30% Investing Truist Cuts PayPal Price Target as Cross-Border Volume","as_of":"2026-05-12","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-Q風險因素將地緣緊張、武裝衝突與貿易措施列為可能降低需求的總體因素；2022年曾暫停俄羅斯交易服務","source":"PayPal Form 10-Q (period ended 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001633917/000163391726000088/pypl-20260930.htm","excerpt":"Adverse global and regional economic conditions—including political unrest and turmoil, geopolitical tensions, armed conflicts, or military escalation—affecting the banking system or financial markets, including, but not limited to, tightening in the credit markets;","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 品牌結帳 TPV 幣別中性成長約 1%，連續第四季維持 1–2%；歐盟取消 de minimis 免稅約拖累 70bp","source":"MarketBeat/PayPal Q3 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-paypal-q3-earnings-call-highlights-2026-10-27/","excerpt":"Branded checkout TPV growth has remained stable in the 1 to 2 percent range for the fourth consecutive quarter.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Venmo 與 Braintree TPV 皆雙位數成長；交易毛利額(TM$)年增 2% 至 $4.0B，不含客戶餘額利息增 3%","source":"PayPal Q3 2026 earnings summary (briefglance / SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001633917/000163391726000086/pypl3q-26earningsrelease.htm","excerpt":"Venmo and Braintree each delivered double-digit TPV growth and are making important contributions to transaction margin dollar growth.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Apple Pay 等對手侵蝕 PayPal 品牌結帳；Q1 品牌結帳僅成長 2%","source":"AP: PayPal's online checkout empire is under siege as rivals squeeze its core business","url":"https://www.ny1.com/nyc/all-boroughs/ap-top-news/2026/05/26/paypals-online-checkout-empire-is-under-siege-as-rivals-squeeze-its-core-business","excerpt":null,"as_of":"2026-05-26","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"分析師共識：2027 營收約 $36B、年增約 4.4%；RBC 預期 2027 仍為投資期，營運槓桿 2028 才明顯","source":"Simply Wall St 預測頁 / Beinsure (2026-10-29)","url":"https://beinsure.com/news/paypal-stock-forecast-new-targets-after-q3-earnings/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"品牌結帳 TPV 連四季 1–2% 成長","source":"PayPal 3Q26 IR Newsletter","url":"https://s205.q4cdn.com/875401827/files/content_files/PYPL-3Q-26-Earnings-IR-Newsletter.pdf","excerpt":"Transaction margin dollars grew 2%, with strong contribution from Venmo and Braintree. Financial services are a key growth driver across all three businesses. Together with 1% non-transaction operating expense growth, nonGAAP earnings per share exceeded our guidance, increasing 8% to $1.45. Branded checkout TPV growth has remained stable in the 1 to 2","as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"PayPal 10-K 自述：生成式 AI 與自主 AI agent 等新技術可能優於或使其現有技術過時；第三方可能以降低客戶對其產品需求的方式部署 AI。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","excerpt":"We expect that new technologies applicable to the industries in which we operate, including the development, adoption, and use of generative AI technologies and autonomous AI agents, will continue to emerge and may be superior to, or render obsolete, the technologies we currently use in our products and services.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"PayPal 10-K 列出瀏覽器儲存卡資訊、即時支付、代幣化、虛擬貨幣/區塊鏈、NFC 等顛覆性支付技術變動。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","excerpt":"web browser technologies that enable users to easily store their payment card information for use on any retail or e-commerce FY 2025 FORM 10-K 15 Table of Contents website; AI; developments in technologies supporting our regulatory and compliance obligations; and in-store, digital, agentic and social commerce.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"PayPal 將 agentic payments 納入長期成長策略，2025-10 與 OpenAI 合作 Agentic Commerce Protocol，並支援 Google Universal Commerce Protocol。","source":"Nasdaq 文章 PayPal Agentic Payments","url":"https://www.nasdaq.com/articles/paypal-agentic-payments-can-they-reshape-future-commerce","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 列示『增加全通路參與』為策略：以 PayPal 簽帳/信用卡、回饋方案與數位錢包整合，推動店內及線上（含 agentic）購買。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","excerpt":"Increasing omnichannel engagement: through the PayPal-branded debit and credit cards, rewards programs, and seamless integration into digital wallets that support in-person payments, we are giving consumers more reasons to use PayPal and Venmo for in-person as well as online (including agentic) purchases.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"PayPal 自 2025 年 10 月推出 agentic commerce 服務（Store Sync、Agent Ready），並採用 OpenAI 的 Agentic Commerce Protocol 使 ChatGPT 內可用 PayPal 付款；2026 年 1 月收購 Cymbio。","source":"Digital Commerce 360 / 搜尋摘要彙整","url":"https://www.digitalcommerce360.com/2025/10/28/paypal-agentic-commerce-ai-driven-shopping-services/","excerpt":null,"as_of":"2025-10-28","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"Q3 2026 財報簡報：品牌結帳 TPV 按固定匯率成長 1%，已部署 playbook 的商家趨勢改善。","source":"PYPL 3Q 26 Earnings Presentation","url":"https://s205.q4cdn.com/875401827/files/content_files/PYPL-3Q-26-Earnings-Presentation.pdf","excerpt":"◦ Improving branded checkout TPV trends at merchants where playbook is deployed (experience, presentment, selection) ◦ Braintree: double-digit TPV growth;","as_of":"2026-10-28","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"無品牌結帳（Braintree、PayPal Complete Payments）為策略重點，但獲利低於品牌按鈕。","source":"Digital Transactions","url":"https://www.digitaltransactions.net/paypal-makes-unbranded-checkout-a-strategic-imperative-as-its-ceo-prepares-to-retire/","excerpt":"So-called unbranded checkout, led by the company’s Braintree processing platform along with a relatively new service called PayPal Complete Payments, is expected to help drive e-commerce volume for PayPal at a time when consumers are turning increasingly to online buying.","as_of":"2023-05-09","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"S&P Global 共識：Hold，12 個月目標價 $56.74，44 位分析師（約 2026-10-21）","source":"Beinsure - PayPal stock price forecast: Wall Street consensus and analyst ratings","url":"https://beinsure.com/news/paypal-stock-forecast-new-targets-after-q3-earnings/","excerpt":"The latest analyst consensus is Hold, with a 12-month price target of $56.74, based on 44 analysts surveyed by S&P Global.","as_of":"2026-10-21","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-10-27 Q3 財報上調全年 non-GAAP EPS 指引至約 $5.60，高於事前共識 $5.39；營收 $8.58B 低於預期 $8.71B","source":"geekchamp - PayPal Q3 2026 revenue misses estimate, EPS outlook raised","url":"https://geekchamp.com/paypal-q3-2026-revenue-rises-2-to-8-58b-misses-estimate-as-tpv-grows-6-3-eps-outlook-raised/","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 後分析師預測仍受弱品牌結帳成長與 2027 投資計畫限制","source":"Beinsure search snippet","url":"https://beinsure.com/news/paypal-stock-forecast-new-targets-after-q3-earnings/","excerpt":"PayPal raised its 2026 adjusted earnings guidance to $5.60 per share, but weak branded checkout growth, revenue below expectations and planned investment in 2027 continue to limit analysts' forecasts.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026 年初共識 EPS 於財測偏弱後下修（Zacks 2026 共識 $5.38，近一週下修）；Zacks Rank #4/#5","source":"Zacks/Nasdaq - PYPL Falls 9.6% Despite Earnings Growth","url":"https://www.nasdaq.com/articles/pypl-falls-96-despite-earnings-growth-stock-hold-or-fold","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Citigroup 於 2026-10-28 將目標價自 $61 降至 $58，維持 Neutral；Q3 後平均目標價約 $57.19、中位 $58","source":"Beinsure / search aggregate","url":"https://beinsure.com/news/paypal-nasdaq-pypl-stock-price-forecast-new-wall-street-targets/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"PayPal Q3 2026 8-K 財報稿：全年指引（non-GAAP EPS、TM$）","source":"SEC 8-K PayPal Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001633917/000163391726000086/pypl3q-26earningsrelease.htm","excerpt":"“I’m pleased with our third-quarter performance and the momentum we are seeing across the business, and we are raising our full-year non-GAAP guidance for transaction margin dollars and EPS.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026年7月報導 Stripe 與 Advent 聯合提出每股 60.50 美元、逾 530 億美元的收購 PayPal 要約；PayPal 與出價方均未置評，未見簽約確認。","source":"The Paypers：Stripe, Advent offer USD 53 bln for PayPal, sources say","url":"https://thepaypers.com/payments/news/stripe-advent-offer-usd-53-bln-for-paypal-sources-say","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"In re PayPal Branded Checkout Securities Litigation：Darcy 案（2026-02-24 提起）與 Norfolk 案（2026-04-02）於 2026-05-21 合併，指稱誤導投資人關於品牌結帳改善；衍生訴訟 2026-07 合併並暫停。","source":"PayPal 10-Q FY2026（經搜尋摘要）／Labaton 新聞稿","url":"https://www.labaton.com/News-Insights/Labaton-Keller-Sucharow-Llp-Announces-Expanded-Securities-Class-Action-Lawsuit-Filed-Against-PayPal-Holdings-Inc-And-Certain-Executives","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"10-10Q 揭露 2026年3月收到英國 FCA 依 Competition Act 1998 的調查通知與資訊要求，公司配合中。","source":"PayPal 10-Q（搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/0001633917/000163391726000088/pypl-20260930.htm","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"+","claim":"Hawai‘i 消保案於 2025-12-17 完成最終和解。","source":"SEC EDGAR 10-K FY2025 Item 3/附註","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","excerpt":"We executed a final settlement in this matter on December 17, 2025.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共 11 份，重大項目含 2025-11 兩份 Item 1.01（BNPL 應收款最高 €65 billion 遠期出售、50 億美元商業本票計畫）；無 4.02 重編項目。","source":"SEC EDGAR 8-K 清單與 8-K 2025-11-17","url":"https://www.sec.gov/Archives/edgar/data/1633917/000119312525284822/d93754d8k.htm","excerpt":"to sell up to €65 billion of UK and European buy now, pay later (BNPL) loan receivables originated by the Seller.","as_of":"2025-11-17","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026年7月報導 Stripe 與 Advent 聯合提出每股 60.50 美元、逾 530 億美元的收購要約；未見簽約確認。","source":"The Paypers","url":"https://thepaypers.com/payments/news/stripe-advent-offer-usd-53-bln-for-paypal-sources-say","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"In re PayPal Branded Checkout Securities Litigation 於 2026-05-21 合併，class period 最長 2024-02-08 至 2026-02-02，指稱 Section 10(b)/20(a) 違法。","source":"Labaton 新聞稿／PayPal 10-Q","url":"https://www.labaton.com/News-Insights/Labaton-Keller-Sucharow-Llp-Announces-Expanded-Securities-Class-Action-Lawsuit-Filed-Against-PayPal-Holdings-Inc-And-Certain-Executives","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"經查近12個月 8-K 清單無 Item 4.02 重編；搜尋未見 SEC 調查，僅見律所徵集與 2026-03 英國 FCA 調查。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001633917&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"PYPL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.76,"operating_margin_pct":18.52,"fcf_margin_pct":18.37,"rd_intensity_pct":9.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"ADYEN.AS","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADYEN.AS"},"note":"quarterly_income_stmt 無資料"},{"name":"XYZ","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":46.36,"operating_margin_pct":12.49,"fcf_margin_pct":15.5,"rd_intensity_pct":12.26},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XYZ","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"V","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.75,"operating_margin_pct":65.57,"fcf_margin_pct":44.91,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AFRM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.07,"operating_margin_pct":20.44,"fcf_margin_pct":23.3,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"PYPL"},"financial_history":{"ticker":"PYPL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":27518000000.0,"revenue_yoy_pct":null,"gross_margin_pct":50.05,"operating_margin_pct":14.7,"net_income":2419000000.0,"diluted_eps":2.09,"free_cash_flow":5107000000.0,"fcf_margin_pct":18.56,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":29771000000.0,"revenue_yoy_pct":8.19,"gross_margin_pct":46.03,"operating_margin_pct":16.61,"net_income":4246000000.0,"diluted_eps":3.84,"free_cash_flow":4220000000.0,"fcf_margin_pct":14.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":31797000000.0,"revenue_yoy_pct":6.81,"gross_margin_pct":46.1,"operating_margin_pct":18.12,"net_income":4147000000.0,"diluted_eps":3.99,"free_cash_flow":6767000000.0,"fcf_margin_pct":21.28,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":33172000000.0,"revenue_yoy_pct":4.32,"gross_margin_pct":46.62,"operating_margin_pct":19.28,"net_income":5233000000.0,"diluted_eps":5.41,"free_cash_flow":5564000000.0,"fcf_margin_pct":16.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/PYPL/PYPL_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**PayPal Holdings, Inc.** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Good morning, and welcome to PayPal's Second (sic) [ Third ] Quarter 2026 Earnings Conference Call. My name is Alexandra, and I will be your conference operator today. As a reminder, this conference is being recorded. I would now like to turn the program over to your host for today's conference, Steve Winoker, PayPal's Chief Investor Relations Officer. Please go ahead.

**Steven Winoker** (Executives):
Thanks, Alexandra. Welcome to PayPal's Third Quarter 2026 Earnings Call. I'm joined by CEO, Enrique Lores; and Chief Financial and Operating Officer, Jamie Miller. Our remarks today include forward-looking statements that involve risks and uncertainties. Actual results may differ materially from these statements. Our commentary is based on our best view of the world and our businesses as we see them today. As described in our earnings press release, SEC filings and on our website, those elements may change as the world changes. Over to you, Enrique.

**Enrique Lores** (Executives):
Thank you, Steve, and good morning. Today, I will discuss our third quarter progress, our multiple growth engines across PayPal and how our work on cost, technology and AI is helping us move faster and deliver for our customers. We are building on PayPal's unique strengths, the trust in our brands, our global scale and the power of our 2-sided network while expanding beyond checkout into financial services. This is an increasingly important part of our value proposition and a larger driver of our growth.
Financial services expand our total addressable market, deepen customer relationships, increase lifetime value and allow us to become a more relevant financial partner in consumers' everyday lives. Over the past several months, we have moved quickly to simplify PayPal, clarify accountability across our 3 businesses and improve our cost structure and productivity. We now have greater clarity on where our biggest opportunities are and how we will capture them.
This quarter, we are beginning to see our strategy translate into financial results. We delivered a solid quarter with transaction margin dollars growing approximately 2% and non-GAAP earnings per share growing 8%. We also delivered $2 billion of adjusted free cash flow and returned over $1.6 billion through buybacks and dividends. Our key growth areas continue to perform well. We saw strong momentum across financial services, including Buy Now, Pay Later, credit and debit. Venmo and Braintree each delivered double-digit TPV growth and are making important contributions to transaction margin dollar growth.
Branded checkout TPV growth has remained relatively stable in the 1% to 2% range for 4 quarters, despite various headwinds. While there is more work to do, we're encouraged by the improvement relative to the market, continued momentum in the U.S. and strength in BNPL and Pay with Venmo. These results show that our financial performance is increasingly coming from multiple parts of the business.
Last quarter, I outlined 5 changes we are making to build a stronger, more diversified PayPal. We have made good progress. And today, each of our businesses has a clear plan for how it will contribute to durable, profitable growth. First, financial services are becoming a much more important part of our business. They already represent more than 20% of transaction margin dollars in 2026 and are growing double digits. For example, we continue to see good momentum in Pay Later with broader distribution this quarter through leading merchants like Amazon in Germany and Austria, American Eagle, Aerie and DICK'S Sporting Goods. And the momentum extends beyond Pay Later, with strong growth across consumer offerings like credit, debit and tap to pay as well as merchant lending.
Second, we continue to build momentum in Venmo and PSP. We are building on the strength of the Venmo brand to broaden adoption of financial services, deepen customer relationships and increase ARPA. The Venmo debit card reached 6.7 million monthly active accounts, up more than 55%, with a record 1.6 million first-time users in the third quarter. We also relaunched the Venmo Credit Card with a differentiated value proposition that rewards customers for splitting purchases with friends. In PSP, we are strengthening our position with large enterprises and leading commerce partners through unified processing and a broader portfolio of premium value-added services such as risk as a service, payouts and merchant lending. PSP volume grew 8%, while value-added services attach increased to 6% from 5% a year ago.
Third, we remain convinced that a consumer-led approach is the right catalyst for durable, profitable growth. We have done significant work to understand who our highest value consumers are, what they need from PayPal and how we can deepen our relationships with them and become more relevant in their everyday lives. Transaction margin dollar growth is our North Star. To drive that growth, we are placing greater emphasis on monthly active accounts and ARPA among these consumers. That means increasing adoption of financial services and improving retention, while also making PayPal easier to find and use at the merchants where these consumers shop. Over time, our opportunity is to serve more of their financial needs with checkout increasingly just one part of a broader relationship. 
This consumer-led approach also informs how we work with merchants. As you can see on Slide 5, across many of our largest U.S. merchants, we are improving the checkout experience, strengthening presentment and partnering on consumer marketing to drive PayPal selection. Where we have implemented multiple elements of this playbook, we are beginning to see improvement in our checkout performance. We are scaling this approach merchant by merchant and country by country.
Fourth, we are changing how we operate to drive better execution. We have clearer accountability, faster decision-making and simpler ways of working. We have reduced headcount by more than 2,000 and removed 3 organizational layers across most areas of the company. We're also using AI and automation to drive productivity. For example, our AI chat agents now support customer service across 190 countries and 6 languages and have resolved more than 24 million contacts year-to-date. Actions like these are creating capacity to reinvest in our highest return opportunities. We are on track to achieve our target of at least $1.5 billion in gross run rate cost savings over 2 to 3 years, including more than $700 million exiting the fourth quarter.
Fifth, we are modernizing our technology and leveraging AI to innovate faster and at scale for our customers. We are making solid progress. This quarter, we migrated 7.5 billion customer records to cloud infrastructure. Our new modular risk platform is using real-time data and AI to cut credit decision times nearly in half in Canada, Italy and Spain. Venmo has started processing select payments on PayPal rails, and Venmo authentication now runs entirely on PayPal's identity platform. These are important steps toward a more unified technology foundation. 
We completed the global rollout of our new PayPal mobile app, built on modern architecture that will enable faster data-driven innovation. And we are building for what comes next, collaborating with Meta and other AI companies to integrate PayPal into AI personal agents and bring our trusted value proposition to agentic commerce. We are still early in these changes. This is a multiyear transformation and there is much more work to do, but the progress we are seeing reinforces our conviction in the strategy.
As I look further ahead, I'm increasingly confident in PayPal's earnings growth potential. Over time, we believe the changes I have described can drive sustainable total company transaction margin dollar growth in the mid-single-digit range. Combined with operating leverage and disciplined capital allocation, including share repurchases, this should enable us to deliver solid double-digit EPS growth. Importantly, we are building the business to make that growth durable.
The key is a more diversified contribution across the business. We expect financial services, Venmo and payment services to contribute a significantly greater share of transaction margin dollar growth over time, with each growing double digits. While we expect branded checkout TPV to improve, this algorithm does not require it to return fully to historical growth rates. The increasing contribution from the rest of the business can drive total company transaction margin dollar growth in the mid-single-digit range.
We also have a significant cost opportunity. The at least $1.5 billion in savings we have identified gives us the capacity to both reinvest and drive operating leverage over time. And PayPal remains a strong cash-generating business, giving us the flexibility to invest where we see the greatest potential while continuing to return capital to shareholders. Getting there will require investment. Our U.S. playbook is showing encouraging early results. And in 2027, we plan to scale what is working across more merchants in the U.S. and internationally.
We plan to invest further in both transaction margin dollars and operating expenses. We are targeting 2027 non-GAAP EPS growth similar to this year as we position the business for faster, more durable growth over time. What gives me confidence is that many of the changes we are making are structural. We have a clear strategy, a simpler operating model, and we are improving execution, and we have started to see the results. Thank you to the PayPal team for your hard work and continued focus. Jamie, over to you.

**Jamie Miller** (Executives):
Thanks, Enrique. Let me start with the financial performance in the quarter. At a high level, transaction margin dollars came in above our expectations while operating expenses were below our forecast, resulting in non-GAAP EPS above our guidance. One point I'd highlight is the tangible progress we're seeing from our transformation. That's showing up not only in the cost structure, but also in technology modernization and in the growth areas Enrique discussed, including financial services and Venmo. Importantly, the savings are creating capacity to self-fund more of our growth investments, such as improving the consumer experience, strengthening merchant presentment and building and scaling our financial services products. And as we learn what's working, we're being deliberate about where we invest more and where we pull back.
With that context, turning to the next slide, let me give you some additional color across the business. Starting with branded checkout, TPV growth remained relatively stable, with continued improvement in the U.S. for the third consecutive quarter and stabilization in Germany. As we communicated in September, the removal of the EU de minimis tax exemption impacted select merchants and created about 70 basis points of headwind in total. In U.S. branded checkout, we're seeing encouraging evidence that the work on experience, presentment and selection, focused largely on our high-value consumers and the merchants where they shop, is having an impact. Over the last 4 quarters, we have seen a significant improvement in relative share of checkout at the cohorts of merchants where we have implemented our full playbook.
We also maintain strong momentum in Buy Now, Pay Later and Pay with Venmo, which outpaced the market, growing 25% and 43%, respectively. We're still early, but what we're learning is increasing our confidence in the playbook and helping us be more targeted about where we invest in 2027. On Venmo, TPV sustained double-digit growth for our eighth consecutive quarter. More importantly, engagement and monetization continue to deepen, with ARPA also growing double digits, driven by strong adoption of our monetized products.
We're also seeing newer cohorts ramp their product usage faster with a record number of new users activating the Venmo debit card within their first 30 days. Monthly active accounts using both the debit card and Pay with Venmo nearly doubled year-over-year, building on similarly robust growth in this cohort last year. At the same time, we're also broadening the places where consumers can use Pay with Venmo, from travel and college tuition to prediction markets, while maintaining strong retention across our established merchant base. That combination of greater utility, deeper product adoption and higher engagement is the model we're building toward with Venmo.
In PSP, our focus is on profitable growth, not simply volume. Braintree's TPV grew 10%, supported by profitable front book wins, high retention and expansion with existing merchants. We're also driving higher attachment of value-added services to our processing relationships, which we expect to support margin expansion over time. Third quarter revenue grew 2% on a spot basis and 1% currency neutral, with growth in Braintree and Venmo growth as well as FX favorability contributing to performance, offset in part by higher contra revenue investments made in the quarter and the de minimis headwinds mentioned earlier.
We benefited from a lower transaction expense rate due largely to mix and partner incentives, lower transaction loss reflecting our team's ongoing work to improve and strengthen onboarding, fraud prevention and risk management capabilities, and lower credit loss driven by a reserve release related to expected credit externalization and supported by disciplined underwriting. Transaction margin dollars grew 2%, or 3% excluding interest on customer balances. What's important is that we're increasingly seeing contribution from multiple areas of the portfolio while continuing to fund both transaction margin and OpEx investments required to strengthen branded checkout and grow financial services, Venmo monetization and PSP value-added services attach. That's the more diversified growth model we're building.
Moving down the P&L on operating expenses, we're beginning to see tangible benefits from the operating rigor we've put in place and faster progress on the transformation, including increasing spans of control, reducing management roles by more than a quarter and rightsizing procurement spend. Non-transaction operating expenses grew just 1% in the quarter and helped drive non-GAAP operating income growth of 3%. That said, I would not simply annualize the third quarter expense performance. We intend to remain disciplined on costs while investing where we are seeing results, in places such as financial services, product growth, consumer life cycle marketing and specialized sales teams.
The combination of stronger transaction margin performance and lower operating expenses resulted in non-GAAP earnings per share growth of 8% to $1.45, above our guidance. Our cash generation remains a strategic advantage. Adjusted free cash flow, which excludes the timing impact from the origination and sale of Pay Later receivables, was $2 billion. We completed $1.5 billion in share repurchases, bringing the trailing 12-month total to $6 billion. More broadly, our strong liquidity and cash generation give us the flexibility to invest in the business without sacrificing our ability to return significant capital to shareholders. That's particularly important as we look toward 2027 and selectively increase investment behind the opportunities where we're building the greatest conviction.
Turning to guidance. For the fourth quarter and the full year 2026, our year-to-date performance demonstrates continued progress across PayPal, even as we execute significant organizational change with increasing clarity and confidence in the growth plans for each of our 3 businesses. With that as a backdrop, we are raising guidance for the full year. We now expect transaction margin dollars to increase to approximately $15.7 billion or $14.6 billion, excluding interest on customer balances, mid-single-digit growth in non-transaction operating expenses, and non-GAAP EPS to increase to approximately $5.60.
Our guidance now includes at least $6.5 billion of adjusted free cash flow and continues to incorporate approximately $6 billion in share repurchases. For online branded checkout, we continue to expect low single-digit TPV growth on a currency-neutral basis for the full year, in line with our prior expectations. This assumes that headwinds in Europe, including the impact from the removal of the de minimis exemption, continue to persist and result in similar 1% to 2% online branded growth throughout the fourth quarter.
We remain on track to achieve at least $1.5 billion in gross run rate cost savings over the next 2 to 3 years and are increasing our expectations exiting the fourth quarter to a run rate of more than $700 million. As we've shared, we intend to reinvest a significant portion of these savings into our highest priority growth initiatives while improving operating leverage over time. For the fourth quarter, we expect low single-digit revenue growth on a currency-neutral basis, slightly positive growth in transaction margin dollars, TM dollars excluding interest on customer balances to be slightly positive and flat to low single-digit growth in non-transaction operating expenses and non-GAAP EPS of approximately $1.43.
In summary, we're seeing encouraging signs that the changes we're making are translating into better performance across the business. We have more work ahead of us, but we're operating with greater clarity and discipline, and we're building a stronger foundation for more durable growth and stronger financial performance over time. I'd like to wrap up by thanking the PayPal team for everything they've accomplished this quarter. With that, Steve, let's go to Q&A.

**Steven Winoker** (Executives):
[Operator Instructions] Alexandra, please open the line.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Andrew Schmidt of KeyBanc Capital Markets.

**Andrew Schmidt** (Analysts):
Maybe just start a little bit higher level. Just given your prior comments about strategic alternatives, you and the Board obviously see more value than whatever offers were on the table. Could you just talk about what's driving your view of intrinsic value? And then, of course, the confidence in achieving that, that'd be helpful.

**Enrique Lores** (Executives):
Sure. Andrew, thank you for the question. So let me share that we have strong conviction in our ability to execute the plan that we have outlined in our prepared remarks and to achieve sustainable double-digit EPS growth in the midterm. And this will be driven by, first, sustainable mid-single-digit transaction margin growth driven by Venmo, processing and more modestly by branded checkout, all supported by the growth of financial services that we -- and we have highlighted how critical we think that part of the business is.
We expect also to see operating leverage as we drive the cost reduction program. And of course, we will continue to utilize our strong free cash flow to drive share buybacks and in some cases, selective M&A that will help us accelerate our plan. But as you said, the Board and the management team have a clear objective to maximize shareholder value, and we have been and we will be open to analyze objectively any option that is presented to us, and we will always choose the alternative that will create more shareholder value. And at this point, that alternative is to execute our plan, and the team is fully focused on driving the progress that we have outlined in the call.

**Operator** (Operator):
Your next question comes from the line of Dan Dolev with Mizuho.

**Dan Dolev** (Analysts):
Enrique, Jamie, really nice work here on the OpEx and the guide raise. Congratulations. I wanted to talk about Venmo. It keeps growing, and it looks really strong, I think, in the double digits. I mean how can we make this a bigger part of the portfolio? And obviously, the usual question on monetization and great work again.

**Enrique Lores** (Executives):
Sure. Thank you. I'll take the question. So our goal, as I briefly mentioned in the prepared remarks, is to make Venmo increasingly central to our customers' everyday financial lives. And we are doing that by building from the strength that we see today in the business and expanding into financial services. The growth that we see today is driven by 3 things. New experiences, and for example, this quarter, we launched the ability for our customers to do P2P transfer by scanning and splitting receipts, which is having very well reception by continuing to invest in financial services that help us to monetize better our customers. 
And just to mention, only 23% of our customers are using today some of the financial services we have today. And this quarter, we saw very strong growth of the debit card with more than 60% growth year-on-year. And finally, we are seeing also very good progress on Pay with Venmo and Pay with Venmo TPV grew more than 40% this quarter. So the growth in the future will be driven by continuing to drive these areas, and we expect to continue to see double-digit TPV growth for Venmo in the coming years.
What is very exciting for us is when we look at ARPA, that is going to become one of the key metrics of the business going forward. And we look at -- and we benchmark ourselves with other companies in our space. We have a 4 to 5x opportunity to increase ARPA, which gives us both the conviction about the opportunity and shows us where we need to invest and where we need to grow. So we expect Venmo to continue to grow, and the results this quarter just show the potential that this business continues to have.

**Operator** (Operator):
Your next question comes from the line of Tien-Tsin Huang with JPMorgan.

**Tien-Tsin Huang** (Analysts):
Just there was good color here on financial services. I was hoping maybe you can update us on the product road map here for financial services. How do you see financial services adding to transaction margin dollars in the near term or even the midterm? And is the bias still to stay balance sheet light?

**Enrique Lores** (Executives):
Yes. So let me start, and then maybe Jamie wants to complement some of the comments. So yes, we see -- we continue to see financial services as a key driver of future transaction margin dollar growth. And this is why we highlighted it during the call. And this is true for all segments. So it's true for consumers and merchants, but also for the 3 businesses, both for Braintree, for Venmo and for PayPal itself.
And within financial services, we include things like Buy Now, Pay Later, debit and credit. Today, and in the future, these businesses or these products offer attractive economics. They open a larger TAM and help us to complement our value proposition to customers. In fact, as I was mentioning before, ARPA is going to become a key metric for us going forward. And we see that when consumers use financial services, their ARPA is between 2x and 5x bigger than for those consumers that don't.
You are going to see us continue to invest in this space. For example, with Buy Now, Pay Later, we are going to be extending the portfolio of offerings that we have, both in terms of products and also in terms of geography to continue to complement our offering in that space. We will be offering cards that will have the flexibility of Buy Now, Pay Later, so we can extend the value proposition from online to stores. And you will see us expanding the portfolio of different credit offerings that we have. So again, a very important business for us where we see a lot of momentum and a lot of demand from our customers to offer.

**Jamie Miller** (Executives):
Yes. And I'd just chime in on the funding question. We have had a balance sheet light strategy towards credit funding over the last couple of years. And what I'd say about the next few years is we'll continue to take a balanced approach between on-balance sheet and off-balance sheet growth. We have a lot of flexibility in our funding sources, and we've demonstrated that through the European Buy Now, Pay Later, the U.S. Revolve partnership we have, the U.S. Pay in 4 funding program that we have underway that we started last year.
And I think what underpins that, which is really important, is that we've got really strong credit underwriting and very attractive paper. So while we'll continue to use the balanced approach with both on and off, in some cases retain the economics, in some cases share those, I think what's important is we have the flexibility going forward to manage that and navigate that depending on what we're doing.

**Operator** (Operator):
Your next question comes from the line of Timothy Chiodo with UBS.

**Timothy Chiodo** (Analysts):
I want to touch on the comments you made around collaborating with Meta and some of the other AI agents. I know from prior discussions, some of the advantages that PayPal might have would relate to the transaction history that you bring to the table, and then also the fact that PayPal does provide both consumer and merchant protections. I was hoping you could expand upon those or maybe other reasons why PayPal may be well positioned for agentic commerce.

**Enrique Lores** (Executives):
Yes. I'll take that one. We really see agentic commerce as a great opportunity for the company. So we really are making this a priority for us, both in terms of the internal work that we do and in terms of partnering with other companies such as Meta. The key advantage that we have is really driven by our core value proposition to consumers and merchants. PayPal -- when PayPal started, the key value proposition was around trust and security. This was needed in e-commerce. This will be even more -- needed more in agentic commerce. And what we are doing is translating that value proposition into the new world.
If you think about consumer agents that will be buying from agents, from merchants, both will have to validate that this is a real consumer that can pay. This is a real merchant that have the product. And that's the value that we see PayPal playing going forward. So it's really all about trust and about the security that we will be providing both to merchants and to consumers.
And this is why we are working with all the key leaders in this space on the -- for personal agents to make sure that consumers can transact using PayPal and using us as kind of the key vehicle to make sure that these transactions are real. And we look at this as just the beginning because what is true for commerce will be expanded to other types of the portfolio of activities that we provide to customers, like P2P or peer-to-peer transfers. All this is part of the value proposition we bring to customers, and this is why we are so excited about the opportunity that AI brings to PayPal.

**Operator** (Operator):
Your next question comes from the line of Harshita Rawat with Bernstein.

**Harshita Rawat** (Analysts):
Can you maybe expand upon the market dynamics in Europe? You have the de minimis drags and competitive pressures in certain markets, but then you're also investing in the consumer value proposition, things like Buy Now, Pay Later. So what's your confidence level with respect to improving branded growth in Europe? And also, Jamie, what's the expectations on the de minimis for the fourth quarter? I know you said headwinds persist, but I just wanted to kind of double-check that.

**Jamie Miller** (Executives):
Sure. And maybe I'll start with the last part of that first. Our expectation on the EU de minimis tariff impacts is that they'll persist into the fourth quarter. When that happened in the U.S. last year, it tended to dissipate within a few months, actually. This -- we're still seeing the impacts from the tariff policy change into October, and we do expect that to last through the fourth quarter.
If I pull back and really look at the market dynamics in Europe, and maybe I'll talk through that, and Enrique, maybe you want to talk about the investment side of it. The core European markets outside of de minimis really are, I would say, relatively consistent this year and to a degree, stabilizing and in some cases, improving. You look at Germany, for example, that has been stable all year for us. 
And I would say as we're moving through the third quarter, I would call it slightly improving. We launched Buy Now, Pay Later in Germany and Austria over the last couple of months, and that's off to -- with Amazon, and that's off to a really nice start. The U.K. continues to be challenging, but it's been consistent this year. And Italy and France are stable and good growers.
So I think what's important is exactly your question, though. We've spent a lot of time in the last 6 months with Enrique focusing on our country-to-country approach and really strengthening our consumer teams in Europe and are now actively positioning to take the playbook that we talked about on the call with merchants into Europe next year. And all of this is really important to our continued transition in branded checkout. But Enrique, you may want to comment a little bit more on the investment side of it.

**Enrique Lores** (Executives):
Yes. I think what we have done in Europe is really to invest to create the right local infrastructure, especially to manage our consumer business. We didn't have teams, local teams that understood the local trends, that were able to create the right programs and activities to drive consumer demand. And this is what we have been building during the last 2, 3 -- 3, 4 months, and we are starting to see the results.
As Jamie mentioned, our relative performance in Europe has improved. This doesn't mean that we don't have room for improvement, which we do, and we will continue to do, but we are positive about the progress that we have seen. And especially as we see the progress that we have made in the U.S., and we highlighted in the call the progress that we have made with some of our key merchants, applying that same playbook in Europe will help us to drive growth and to continue to improve the performance in those countries.

**Operator** (Operator):
Your next question comes from the line of Bryan Keane with Citi.

**Bryan Keane** (Analysts):
I just also wanted to follow up on international. It looks like the TPV is relatively flat, the growth on FX neutral. But the revenue growth slipped to negative 4% growth on an FX-neutral basis. Sounds like there's a lot of stability in Germany and Italy and some of the European markets. What's dragging, I guess, international down further? Is there Asia markets that are weakening? And then how long will it take to get back to normalized positive growth in international as we get into next year?

**Jamie Miller** (Executives):
Yes. So the TPV side of things, we saw some translation, minor impacts there. But when you start to look at revenue, and in particular international, that's where you're seeing the impact of the EU tariffs and branded checkout. And you have to remember that the number I gave you on impact from the tariffs, which is 70 bps to branded checkout, that's a global number. It's not the international specific number. So that number is bigger when you start to apply it just to international revenue. But that's really the primary difference there.
And then when you start to look at international going into next year, we've been encouraged by some of the growing -- growth that we've seen, and I mentioned before across Germany, Italy, France and a few other parts of Europe. But I think, more importantly, the playbook that we started rolling out really over a year ago around not only experience, presentment and selection, but also around Buy Now, Pay Later and really reaching into the consumer and greater penetration.
While we started that in the U.S., that is moving to Europe, and you're seeing some of that with the actions we've talked about with expansion of the Buy Now, Pay Later portfolio across Europe and across other places and with respect to increasing levels of penetration around the merchant playbook as well.

**Operator** (Operator):
Your next question comes from the line of Andrew Bauch with BMO Capital Markets.

**Andrew Bauch** (Analysts):
I just wanted to hone in on the '27 transaction margin dollar algorithm. I know you outlined the eventual path to mid-single digits growth, but you also said that '27 was going to be an investment year. I guess what should we expect for the TM dollar growth to look like in '27 specifically? And what are the -- like the biggest bridges between the 2% growth you're at today and the mid-single-digit target?

**Jamie Miller** (Executives):
Okay. So let's first talk about the mid-single-digit point of view, it's really around our medium term. So it's an over time point of view. And if I start with that, as Enrique talked about before, we expect stronger transaction margin dollars growth over the next coming years, a more balanced composition with Venmo, PSP and financial services increasing growth over time. And I think, importantly, it doesn't require branded checkout to get back to historical growth levels to really see that mid-single-digit growth. But when I look to '27, I think what I'd say first is it's a little too early for us to give '27 guidance. We'll do that at our next call in February.
But you've seen from us this year nice performance across multiple areas. So we've seen branded checkout stabilization. We've seen Venmo. We've seen processing growth. And we do expect further transaction margin dollar and OpEx investment in 2027. But if I level up, what we're really targeting as a profile is similar non-GAAP earnings per share growth next year as what we are guiding to this year. So that's probably how I would talk about it, and '27 being relatively consistent with how we've operated in '26. We are making good progress. Our focus is on building momentum and looking at '28 and beyond as well.

**Enrique Lores** (Executives):
And maybe just let me emphasize these last 2 comments. We think we have an opportunity to continue to invest in the areas where we are seeing progress, whether it's transaction margin and OpEx. This is what we are planning to do in '27. We think it will be critical to drive stronger growth in '28 and beyond. And despite of that, we expect and we are targeting to grow EPS at the same rate as we did -- as we will this year.

**Operator** (Operator):
Your next question comes from the line of Sanjay Sakhrani with KBW.

**Sanjay Sakhrani** (Analysts):
I guess when I look at Slide 5 and those cohorts that seemingly are headed in the right direction, when we look at the difference between like the first one and the last one, there seems to be a bifurcation between when you apply to a direct merchant versus a marketplace, right? So I'm just curious like what are the nuances. Because it seems like a lot of the technologies are implemented there. So I'm just curious, is it because the marketplace has other options for payment and that merchant doesn't? I'm just curious, as we think about the opportunity ahead and how you implement these changes, like where are the opportunities most significant?
And then just a quick follow-up, Jamie. Just as we think about the comparisons this year versus next year, it seems like the comps are much easier next year. So shouldn't we expect a little bit of an acceleration in TMD growth because the comps are easier? Or maybe you could just explain how we should think about it.

**Enrique Lores** (Executives):
So let me take the first part of the question on North America. When we look at our playbook, the playbook has different elements. One element is to improve the experience and to get the merchants to use the latest checkout pages. Another element is to integrate in the offer, Buy Now, Pay Later and some of the other financial services. Another element is to build co-marketing activities with the merchant.
What you see in the graph -- and we don't have the same -- exactly the same formula applied to every merchant. It depends on specific conditions of the merchant and what are the economic situation and the interest that we work with. And this is what is driving the valuation -- variation across the different customers that you have in the chart. We thought it was important to share this chart because it shows the trend. 
And yes, there are differences merchant to merchant, but the important thing is how the overall TPV growth is growing and how we are also starting to grow our relative share in these accounts. And we have great examples of the progress that we are making. We don't specifically mention them in the call, but for example, with one of the leading U.S. sports entertainment platforms, where we drove and we renewed our partnership at the beginning of the year, we are seeing more than 40% growth in the last 6 months.
With Venmo as well growing more than 50%. With one of the leading U.S. omnichannel retailers, we expanded our Pay Later offering to them, and growth of BNPL grew from 7% to 20%, with significant growth of monthly active users. So we have many examples where we see that the impact of the playbook that we have implemented is really starting to gain traction. And again, this is why we think continuing the investment and continuing the work is going to be so critical for us going forward.

**Jamie Miller** (Executives):
And Sanjay, when you look at, in particular, fourth quarter or 2027, I would just echo what Enrique is saying. We are really encouraged by the results we're seeing, but it's early, and we've got more work to do. And one of the things I would mention is that in the U.S., in particular, we saw nice sequential growth over the past few quarters in U.S. branded checkout TPV growth. So we're seeing good signs, but we also don't want to get ahead of ourselves. We are underwriting these investments generally in branded checkout to about a 2- to 3-year time horizon. And on the largest merchants, it really is more like 3 years. So it's going to take some time for these to come through. And as we've said before, we're beginning that process in Europe, and we're excited to see where it goes and go from there.

**Operator** (Operator):
Your next question comes from the line of Darrin Peller with Wolfe Research.

**Darrin Peller** (Analysts):
Just a quick 2-part on investments in general. First, for Enrique on M&A. Just if you can give us an update again, you touched on it earlier, but your appetite for M&A in terms of size, timing and type, what you're seeing? And then really, Jamie, when we think about the investments you're talking about for next year, I mean, again, you came in strong, better at about 1% growth, I think a little below what we had thought for OpEx expectations. But how should we think about margins for next year in terms of what you're building into that similar EPS profile?

**Enrique Lores** (Executives):
So let me start on the M&A side. And I want to start by saying that our plan is to maintain our approach to significantly return capital to shareholders through share buybacks and dividend. But that over time, we believe that M&A should also play a role in value creation. Any M&A action that we will do will have to go through what I call 3 filters. Filter number one is strategy. It will have to support the strategies that we have outlined. For example, to drive growth of financial services or accelerate the growth of Venmo or of processing. That's really aligned to the strategy that we have explained.
Second, it needs to have a strong financial case and a strong financial return. And given that share buybacks, that our -- we believe that our share is undervalued, the minimum value, of course, will have to be -- provide more value than just buying shares compared to versus the model that we have. And third, and very important, we need to also have a very strong operational plan. And we'll have to have the conviction and the plan that we'll know how to integrate the company and how to extract the value that the financial case will bring. So these are the 3 filters that we will apply in any case. We will remain very disciplined, but we think that with M&A, we can accelerate the plan that we have been discussing today.

**Jamie Miller** (Executives):
Great. And then, Darrin, with respect to 2027 investment, I guess what I'd say is we've had nice performance in the third quarter, and it was much better than we expected, and we expect to have a good profile on this in the fourth quarter as well. But I would not run rate the second half OpEx across '27. While we're off to a really strong start, we are ramping investment along the lines of a lot of the things that Enrique and I've talked about here, the product build, go-to-market build, marketing and other things like that.
And I think one of the things you're going to see is it's hard to fully synchronize the pace of the cost out with the pace of the investment, and you are going to see some mismatch across the quarters. But overall, if I look at the '27 profile, when you look at transaction margin, when you look at OpEx, when you look at EPS, like I said before, we expect a roughly consistent profile and we'll unpack that and get into more specifics on the call in February.

**Operator** (Operator):
Your next question comes from the line of Dan Perlin with RBC Capital Markets.

**Daniel Perlin** (Analysts):
I wanted to just hit on PSP for a second. It sounds like part of that strategy is to continue to drive higher attach rates for value-added services. So I guess the first part is just what does that sales motion look like as we sit here today? And how do you have to invest in that going forward? Or are you kind of where you want and just need to push it harder? And then I thought I heard you say the percentage of that was high single digits, so if there's any clarification on that, that would be great.

**Enrique Lores** (Executives):
So let me take the first part. So in PSP, what we need to do and where we see the biggest opportunity is from one side to continue to drive growth or what I would call the basic processing capabilities, and we have been making very good progress and making it profitable during the last few quarters, but also to improve attach of value-added services. Services like payouts or risk as a services -- risk as a service or invoicing, these are all great services that provide a lot of value to our customers. And either we have not been able to attach them properly or we have not been able to monetize them properly during the last quarters.
And that's going to be a key priority for us going forward. We are investing, not only in the products themselves, but especially in a specialized sales force that will be driving attach, that will have as their unique goal to improve attach and to sell value-added services. I want to acknowledge that we have started to make progress. So we grew our attach from 5% to 6%, so year-on-year, one point, but we have much more room for improvement, and this is where we're going to be focused.

**Operator** (Operator):
Your last question comes from the line of Jason Kupferberg, Wells Fargo.

**Jason Kupferberg** (Analysts):
So nice to see some of the broad-based stabilization, obviously pockets of improvement in the business. I did want to come back to the topic of branded growth. I know we're talking about Q4 being in this kind of steady 1% to 2% range, and you are assuming that the EU tariff headwinds continue. But you did also talk about some U.S. momentum. So just curious why Q4 wouldn't potentially accelerate. I know you've got a material easier compare, and maybe if you can just quantify some of the U.S. acceleration in recent quarters, that would be great.

**Jamie Miller** (Executives):
Sure. I mean the short answer on the fourth quarter is that we expect the EU tariff headwind to continue, and we're really planning for consistency. If I unpack that a little bit, the forecast is really based on our view of historical performance and our view of the market. And the holiday season is more heavily retail, but we have a really good and strong depth in services, travel and some of the other verticals, and we've got really good growth rates in areas that we're deep. But the EU de minimis, we assume that continues to impact us.
As I mentioned before, Europe has been consistent this year, but it's an area we're watching with some of the macro overlay and the EU de minimis that I mentioned. And we're really encouraged by the U.S. merchant playbook work we've done. And we do believe that we're entering the holiday season in a better position than we were last year at this time, but it's all still very early. And we've got more work to do ahead. And I would just say that as we take it all in, that's what's leading us to the guide around the 1% to 2% for fourth quarter.

**Steven Winoker** (Executives):
Enrique, any final thoughts?

**Enrique Lores** (Executives):
Yes. I want to close by first acknowledging the progress that we have made so far. Last quarter, we outlined 5 key priorities for the company, and we are making progress in all of them. We have talked about the progress we have made in financial services that are growing double digits and especially around areas like BNPL is showing really our ability to expand and to grow in this area.
Second, we have talked about the progress we're making with Venmo and PSP. Significant growth both on revenue and transaction margin and great plans to continue to drive that going forward. Around branded checkout, the business has stabilized. We have a clear view of what is the playbook that we need to apply to continue to drive growth and especially centered around high-value customers. We see what we need to do, and we are going to continue to do that in the coming quarters.
And finally, both around cost and simplification and embracing AI, we have made tangible progress as the results show. So good progress made in Q3 that shows that we are in the right direction, more work to do. But thank you to the PayPal team, and also thank you to all of you for participating with us today.

**Jamie Miller** (Executives):
Thank you.

**Operator** (Operator):
Thank you. This concludes today's conference. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### PYPL_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CEO｜guidance：CEO表示上調全年交易毛利金額與非GAAP EPS財測（原話："raising our full year guidance for transaction margin"）
- 2026-07-28｜CFO｜guidance：CFO給出全年TM美元約156億（扣除客戶餘額利息為145億）（原話："approximately $15.6 billion or $14.5 billion"）
- 2026-07-28｜CFO｜guidance：CFO給出非交易營運費用成長7%-8%與EPS 5.38美元（原話："approximately 7% to 8% growth in non-transaction operating"）
- 2026-07-28｜CFO｜guidance：CFO給出第三季非交易費用高個位數成長、EPS低個位數衰退（原話："non-GAAP earnings per share to decline"）
- 2026-07-28｜CFO｜guidance：CFO表示第四季TM美元成長略為正（原話："transaction margin dollar growth to be slightly positive."）
- 2026-07-28｜CFO｜guidance：CFO上調全年品牌結帳TPV預期至低個位數（原話："For online branded checkout, we now expect low single-"）
- 2026-07-28｜CFO｜guidance：CFO預期第三季品牌結帳成長約2%（原話："branded checkout growth at about 2%"）
- 2026-07-28｜CFO｜guidance：CFO表示成長投資對全年TM美元的拖累小於原先3個百分點（原話："a modestly lower headwind to transaction margin dollars"）
- 2026-07-28｜CFO｜guidance：CFO表示FCF與買回財測維持（原話："at least $6 billion of adjusted free cash flow"）
- 2026-07-28｜CFO｜guidance：CFO表示不預期年內再有利率變動（原話："we're not expecting or not planning, I should say, any more"）
- 2026-07-28｜CFO｜margin：CFO說明交易take rate下滑7bp至1.61%（原話："Transaction take rate declined by 7 basis points to 1.61%."）
- 2026-07-28｜CFO｜margin：CFO說明交易費用占TPV 90bp，因Braintree占比上升而略增（原話："expense as a percentage of TPV was 90 basis points"）
- 2026-07-28｜CFO｜margin：CFO說明TM美元表現受外匯有利與損失降低貢獻（原話："FX favorability and lower losses across PayPal and Venmo"）
- 2026-07-28｜CFO｜margin：CFO說明部分費用增加屬時間差，先投資再享節省（原話："It's important to note that part of the increase is timing."）
- 2026-07-28｜CFO｜margin：CFO說明非GAAP營業利益年減8%（原話："income was down 8% in the quarter to $1.5 billion."）
- 2026-07-28｜CFO｜commitment：CFO表示至少15億美元成本節省目標維持（原話："achieve at least $1.5 billion in gross run rate cost"）
- 2026-07-28｜CFO｜commitment：CFO表示年底前已識別約4億美元新增節省（原話："identified actions to unlock approximately $400"）
- 2026-07-28｜CFO｜guidance：CFO預告下半年轉型相關費用約1.2億至1.4億美元（原話："approximately $120 million to $140 million during the second"）
- 2026-07-28｜CFO｜commitment：CFO表示成本節省第四季起更顯著（原話："cost savings initiatives to become more meaningful"）
- 2026-07-28｜CFO｜commitment：CFO表示將把大部分節省再投資於策略領域（原話："we do expect to reinvest much of those"）
- 2026-07-28｜CEO｜commitment：CEO表示多數投資由節省自行支應（原話："will be self-funded with the savings that Jamie described."）
- 2026-07-28｜CFO｜commitment：CFO表示若未達ROI門檻將重新配置資金（原話："even more focused with Enrique on redeployment of those"）
- 2026-07-28｜CEO｜commitment：CEO表示成長動能預計2027下半年起累積（原話："momentum expected to build in the second half of 2027"）
- 2026-07-28｜CEO｜product：CEO表示2028年後代理支付與數位身分預期更具貢獻（原話："agentic payments and digital identity"）
- 2026-07-28｜CFO｜capital_allocation：CFO表示本季買回15億美元（原話："we completed $1.5 billion in share repurchases,"）
- 2026-07-28｜CFO｜capital_allocation：CFO說明過去12個月買回60億美元與期末現金（原話："trailing 12-month total to $6 billion."）
- 2026-07-28｜CEO｜capital_allocation：CEO談M&A傳聞：不評論，但保持開放（原話："remain open and objective in evaluating opportunities."）
- 2026-07-28｜CEO｜capital_allocation：CEO在Q&A表示目前聚焦執行自身策略（原話："our focus is on executing our own strategic"）
- 2026-07-28｜CFO｜competition：CFO提到歐洲成長正常化且競爭強度上升（原話："certainly, there's more competitive intensity as"）
- 2026-07-28｜CFO｜risk：CFO提到旅遊類別季初出現壓力（原話："We saw some pressure in the travel vertical that was"）
- 2026-07-28｜CEO｜product：CEO說明Venmo多產品使用者ARPA高於純P2P用戶（原話："more than 9x higher ARPA than peer-to-peer only users"）
- 2026-07-28｜CFO｜product：CFO說明Venmo TPV連續七季雙位數成長（原話："seventh consecutive quarter of double-digit growth."）
- 2026-07-28｜CFO｜product：CFO說明Pay with Venmo與BNPL優於市場（原話："continue to outpace the market"）
- 2026-07-28｜CFO｜product：CFO表示金融服務營收今年成長至少為整體兩倍（原話："at least twice as fast as the total company"）
- 2026-07-28｜CEO｜product：CEO表示金融服務占TM近20%（原話："part of the transaction margin of the company, close to 20%"）
- 2026-07-28｜CEO｜customer：CEO提到與Amazon在德國與奧地利的消費信貸合作（原話："consumer lending partnership with Amazon for"）
- 2026-07-28｜CEO｜customer：CEO舉社群電商平台整合計畫後量與TM成長50%（原話："we saw 50% growth in volume and transaction margin"）
- 2026-07-28｜CEO｜customer：CEO舉時尚零售商簽獨家BNPL後TPV由下滑轉為成長（原話："signed an exclusive BNPL agreement during the last month"）
- 2026-07-28｜CFO｜customer：CFO表示策略將帶來雙位數獲利成長輪廓（原話："attractive double-digit earnings growth profile"）

### 問答異常語氣（迴避／改口／保留）
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：Wells Fargo：再投資有多少在交易利潤線之上、多久才見效於TM美元成長｜答法：CFO與CEO談再投資方向與自籌資金，未給出占比或見效時間
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：JPMorgan：潛在控制權變動是否影響商家合作｜答法：CEO先指出問題實為兩題，對傳聞不評論，只講董事會會客觀評估並聚焦自身計畫，未直接回答商家張力
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：Wolfe：第四季品牌結帳成長預期（較易比較基期）｜答法：CFO未給第四季數字，僅稱假期競爭且財測審慎
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：RBC：美國以外品牌結帳動態與結構性或地緣因素｜答法：CFO與CEO描述歐洲略改善、競爭加劇，未給海外數字
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：Cantor：7月品牌結帳相對6月退出率的趨勢｜答法：CFO只給第三季約2%，未直接回答7月對6月

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
{"date":"20260710","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"品牌結帳於 FY2026 下半年觸底並回升至低個位數 YoY（+2~4%），停止份額流失","columns":{"2Y 驗證點":"Q3/Q4 2026 branded YoY ≥+2%","5Y 驗證點":"Fastlane＋agentic commerce 使 branded 重回 5-8%","具體數字門檻":"branded YoY，Q4 FY2025 僅 +1%；FY2026 guidance transaction margin dollars 持平","信息來源":"PayPal 季度法說 branded/unbranded 拆分（Q1 FY2026 IR，2026-05-05）","漂移觸發":"連 2 季 branded YoY &lt;0% → 反轉、moat_trend 下修 ↓、thesis 削弱至 X"}},{"id":"H2","text":"FY2026-27 調整後 FCF 年化維持 ≥$5.5B，回購 ~$6B 不靠大幅舉債","columns":{"2Y 驗證點":"滾動 TTM FCF ≥$5.5B、FCF/NI ≥0.90","5Y 驗證點":"FCF 隨 margin 擴張與 Venmo 貨幣化維持","具體數字門檻":"FY2025 FCF $5.56B（yfinance）；FY2026「約 $6B 回購」（管理層 Q4 FY2025 法說）","信息來源":"PayPal FY2025 10-K；yfinance cashflow","漂移觸發":"滾動 TTM FCF 連 2 季 &lt;$5.0B → H2 削弱、重評估值錨；&lt;$4.0B → thesis 根本動搖"}},{"id":"H3","text":"total transaction take rate 年降幅收窄至 &lt;3bps/年（定價壓力趨穩）","columns":{"2Y 驗證點":"連 2 年降幅 &lt;3bps","5Y 驗證點":"Venmo／信貸／高毛利 VAS 佔比上升抵住 mix shift","具體數字門檻":"現約 6bps/年降幅（Rev +7% vs TPV +11%，Q1 FY2026）；transaction take rate ~1.66%","信息來源":"PayPal 10-K TPV／Revenue 自算；Q1 FY2026 IR","漂移觸發":"連 2 年降幅 &gt;7bps 且 Braintree 佔比續升 → mix 結構性惡化、定價能力消失確認"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"品牌結帳份額加速流失給 Apple Pay／Shop Pay／卡網直連（產業態勢競爭惡化回填）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"branded checkout YoY、branded TPV 佔比","警戒閾值":"連 2 季 branded YoY &lt;0%"}},{"id":"R2","text":"take rate 壓縮加速（unbranded/Braintree 負向 mix shift 結構化）","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"Rev÷TPV 年降幅、branded/unbranded TPV mix","警戒閾值":"連 2 年降幅 &gt;7bps"}},{"id":"R3","text":"agentic commerce 去中介：AI agent 在 API 層直接調用卡網／穩定幣結算，繞過 PayPal 錢包 UI（比「品牌結帳被 Apple Pay 搶」更根本）。三方軌道戰 Visa Intelligent Commerce／Mastercard Agent Pay／Coinbase x402（Circle/Stripe/AWS/Cloudflare 背書、首年 ~1.69 億筆）主導，PayPal 不在核心玩家名單；且最大落地案例 Shopify×ChatGPT 原生軌是 Shop Pay 非 PayPal（產業態勢其他結構變數）","columns":{"對應假設":"H1＋第二曲線","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"PayPal 在 agentic 結帳份額、ACP 採用 vs Shop Pay/卡網/x402 軌道、PYUSD agentic TPV","警戒閾值":"agent 支付軌道主導權落 Visa/MA/Coinbase/Shop Pay 而 PayPal 錢包被架空"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"品牌結帳 YoY 連 2 季回到 ≥+2%（止穩證明），或 transaction margin dollars 重回 YoY 成長；否則維持追蹤","irr_base_pct":9.2,"ev5y_pct":48.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🟢","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":4.3,"ev5y_pct":48.0,"irr_base_pct":9.2,"max_dd_pct":-55.0,"bull_5y_price":109.0,"bear_5y_price":35.0,"p_bull_pct":25.0,"p_bear_pct":40.0,"rearm_trigger":"品牌結帳 YoY 連 2 季回到 ≥+2%（止穩證明），或 transaction margin dollars 重回 YoY 成長；否則維持追蹤","price_at_dd":45.32,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
