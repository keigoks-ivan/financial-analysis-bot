你是 stock-analyst **v20 判斷 agent**，標的 NOW（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"NOW","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenues_gaap","label":"Total revenues (GAAP)","value":4106,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_kpi1_subscription_revenues_ga","label":"Subscription revenues (GAAP)","value":3988,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_kpi2_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":1338,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_kpi3_gaap_operating_income_ma","label":"GAAP operating income / margin","value":385,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_kpi4_free_cash_flow_non_gaap","label":"Free cash flow (non-GAAP)","value":822,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_kpi6_guidance_q4_fy2026_subsc","label":"Guidance Q4 FY2026 subscription revenues","value":null,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"},"needs_sonnet":true},{"id":"f_kpi7_guidance_fy2026","label":"Guidance FY2026","value":null,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"},"needs_sonnet":true},{"id":"f_kpi8_crpo","label":"cRPO","value":13650,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_kpi9_rpo","label":"RPO","value":29700,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_kpi10_customers_5m_acv","label":"Customers >$5M ACV","value":680,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"count","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_kpi11_subscription_gross_margi","label":"Subscription gross margin (non-GAAP)","value":80,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_kpi12_non_gaap_eps_diluted","label":"Non-GAAP EPS (diluted)","value":1.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_now_gross_margin_pct","label":"NOW 毛利率","value":73.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_now_operating_margin_pct","label":"NOW 營業利益率","value":9.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_now_fcf_margin_pct","label":"NOW FCF 利潤率","value":30.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pltr_gross_margin_pct","label":"PLTR 毛利率","value":84.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pltr_operating_margin_pct","label":"PLTR 營業利益率","value":42.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pltr_fcf_margin_pct","label":"PLTR FCF 利潤率","value":54.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_crm_gross_margin_pct","label":"CRM 毛利率","value":77.28,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_operating_margin_pct","label":"CRM 營業利益率","value":21.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_fcf_margin_pct","label":"CRM FCF 利潤率","value":34.49,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_msft_gross_margin_pct","label":"MSFT 毛利率","value":67.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_operating_margin_pct","label":"MSFT 營業利益率","value":47.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_fcf_margin_pct","label":"MSFT FCF 利潤率","value":17.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ddog_gross_margin_pct","label":"DDOG 毛利率","value":79.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ddog_operating_margin_pct","label":"DDOG 營業利益率","value":0.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ddog_fcf_margin_pct","label":"DDOG FCF 利潤率","value":27.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc","label":"SBC","value":633,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":105.12,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":15.31,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":26.86,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-2.46,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.07 → 3.97）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-3.4,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.0 → 4.83）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-2.15,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.05 → 5.92）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.97,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":4.83,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":5.92,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-2.46,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 4.07 → 3.97（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":75.63,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":7.07,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":7.32,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":26.48,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.97，分子＝快照價 105.12","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":3808.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 8415.0、現金 4607.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1037.92,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":112913.84,"period":"2026-11-02","unit":"USD m","basis":"市值 109105.84 ＋ 淨負債 3808.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":16233.51,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（39 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":19268.01,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（46 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.96,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 105.12 / W52 123.36 / W104 157.76 / W250 134.41 / W250 13週斜率 0.2%"},{"id":"f_ma_w52","label":"52 週均線","value":123.36,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":157.76,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":134.41,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.2,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"NOW 10-K 自述：AI 領域出現多家以資料分析與資訊生成為主的點解決方案新進入者，公司認為多數難以提供完整整合與治理；主要對手含 Microsoft、Oracle、SAP、Salesforce、Workday。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"While competitors are actively developing AI capabilities and several entrants have emerged with point solutions focused on data analysis and information generation, we believe many face challenges in delivering the comprehensive integration, workflow orchestration, governance frameworks, and enterprise-grade reliability that our customers require to operationalize AI insights.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：雲端與 AI 原生廠商可能開發更多商業應用與 AI 自動化方案與公司競爭；系統記錄廠商可能阻擋整合、對手可能捆綁降價。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"“Systems of record” operators may attempt to create technology solutions or other mechanisms that would prevent our systems from integrating with theirs. They may create pricing pressures by reducing the price of competing products, services or subscriptions or bundling their offerings, causing our offerings to appear relatively more expensive.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"The Register 評論：Salesforce 推出對 ServiceNow 迄今最可信的威脅（Agentforce ITSM）。","source":"The Register: Salesforce has come up with the most credible threat yet to ServiceNow","url":"https://www.theregister.com/2025/12/05/salesforce_agentforce_vs_servicenow/","excerpt":"Salesforce has come up with the most credible threat yet to ServiceNow, and Benioff is crowing about it Some within the CRM giant balked, but Benioff prevailed","as_of":"2025-12-05","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"ServiceNow 10-K 列出競爭來源包含客戶自行開發與內部(in-house)解決方案，以及 AI 新進者；未見單一最大客戶導入第二供應商或自製的具體事件揭露。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"custom-developed and in-house solutions; •technology consulting firms; •systems integrators; and •software resellers.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：一家美國聯邦通路夥伴/系統整合商占 2025 與 2024 年總營收各 11%，占應收帳款 11%（2025 底）與 12%（2024 底）；經定期信用評估無歷史收款疑慮；壞帳提列不重大。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"We had one customer, a U.S. federal channel partner and systems integrator, that represented 11% and 12% of our accounts receivable balance as of December 31, 2025 and 2024, respectively, and 11% of our total revenues for the years ended December 31, 2025 and 2024. Based on our periodic credit evaluations, there have been no historical collection concerns with this customer.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：2023 年無單一客戶超過 10% 營收；直銷（含 SI/MSP）占營收 78%。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"There were no customers that individually exceeded 10% of our total revenues for the year ended December 31, 2023.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2026 Q2 10-Q：同一聯邦通路夥伴占 2026 年 6/30 應收帳款 12%，占當季及上半年營收 13%（去年同期 11%），集中度上升；信用評估仍無收款問題。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001373715/000137371526000076/now-20260630.htm","excerpt":"federal channel partner and systems integrator, that represented 12% and 11% of our accounts receivable balance as of June 30, 2026 and December 31, 2025, respectively. This customer represented 13% of our total revenues for each of the three and six months ended June 30, 2026 and 11% of our total","as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"NOW Q1 2026：訂閱營收 $3,671M（固定匯率 +19%）；全年訂閱指引上調至 $15.735B–$15.775B（cc +20.5%–21%），其中約 125bp 來自 Armis 提前交割，有機指引大致持平；cRPO $12.64B（+22.5%）；Now Assist 相關營收目標由 $10 億上調至約 $15 億。","source":"comparethecloud.net / SEC 8-K Q1 FY26 搜尋摘要","url":"https://www.comparethecloud.net/news/servicenow-raises-full-year-guidance-to-1575bn-after-q1-beats-on-ai-deal-growth","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026-05-04 投資人日：NOW 預期 2030 年訂閱營收 $30B，Now Assist 約占 ACV 30%。","source":"The Next Web: ServiceNow projects $30bn by 2030, with a third of ACV from AI","url":"https://thenextweb.com/news/servicenow-30-billion-2030-now-assist-ai-revenue","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Bloomberg Intelligence 預期 AI agent 將把應用軟體定價由 seat 轉向用量／成果計價，利潤率可能壓縮 100–900bp；Global X 稱 seat-based 為最受衝擊模式。","source":"Bloomberg Intelligence Agentic AI Deep Dive / Global X ETFs","url":"https://www.globalxetfs.com/articles/product-research/software-volatility-separating-noise-from-signal","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"NOW Q1 2026 8-K 官方數字（訂閱營收、cRPO、指引）","source":"SEC 8-K","url":"https://www.sec.gov/Archives/edgar/data/0001373715/000137371526000054/erq1fy26.htm","excerpt":"and profitability metrics, raises full year subscription revenues outlook •Subscription revenues of $3,671 million in Q1 2026, representing 22% year-over-year growth, 19% in constant currency •Total revenues of $3,770 million in Q1 2026, representing 22% year-over-year growth, 19% in constant currency •Current remaining performance obligations of $12.64 billion as of Q1 2026, representing","as_of":"2026-04-29","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 揭露：公司向美國政府機關通報內部調查（Army CIO 聘用案）並配合司法部（DOJ）自行展開的調查；公司無法預測時程、結果或影響。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"The Company has informed the Department of Justice, the Department of Defense Office of Inspector General and the Army Suspension and Debarment Office of the investigation and is continuing to cooperate with the Department of Justice, which has commenced its own investigation and required the Company to deliver certain documents in connection with these matters. The Company cannot predict the timing, outcome or possible impact of the investigation.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K Item 3 稱訴訟與法律程序個別或合計不預期造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"we do not believe that the ultimate resolution of any such proceedings, whether taken individually or in the aggregate, is likely to have a material adverse effect on our business, financial position, results of operations or cash flows.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"DOJ 曾對 Moveworks 收購案做深度反壟斷審查（second request）；該收購於 2025-12-15 完成。未找到 2026 年 DOJ/FTC/歐盟針對 NOW 的反壟斷調查或拆分風險。","source":"Businesswire: ServiceNow completes acquisition of Moveworks","url":"https://www.businesswire.com/news/home/20251215128980/en/ServiceNow-completes-acquisition-of-Moveworks","excerpt":null,"as_of":"2025-12-15","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"NOW 10-K FY2025 風險因子：受海關法管轄，部分情況須自付美國及他國進口關稅，較高進口關稅會提高營運成本；亦受出口管制與經濟制裁法約束，俄烏衝突下可能有更廣的制裁與出口限制。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"In addition, we are subject to customs laws that may impose tariffs on us, either directly or indirectly. This includes tariffs imposed by the U.S. government and other countries on imports, which we are responsible to pay in certain circumstances. Higher tariffs on imports related to our operations could increase our operating costs.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"NOW 10-K FY2025 MD&A：管理層稱未因關稅等總體事件而影響流動性或營運與財務狀況。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"We have not experienced any impact to our liquidity or to our current and projected business operations and financial condition due to recent macroeconomic events.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ServiceNow Q1 2026 稱中東衝突使數筆大型地端交易延後，約拖累訂閱營收成長 75 bps","source":"CFO Dive: ServiceNow CFO says Iran conflict delayed large deals","url":"https://www.cfodive.com/news/servicenow-cfo-says-iran-conflict-delayed-large-deals/818357/","excerpt":"ServiceNow CFO says Middle East conflict delayed large deals The finance chief said several Middle East on-premise deals slipped during the first quarter though the software firm’s full-year outlook remains in tact.","as_of":"2026-04-23","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因素列出政治不穩、戰爭、貿易壁壘、制裁等地緣條件可影響業務","source":"ServiceNow FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"among others, inflation, interest rates, tax rates, foreign exchange rates, economic downturns, recession, economic uncertainty, political instability, warfare, changes in laws, trade barriers, supply chain disruptions and economic and trade sanctions.","as_of":"2026-02-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"ServiceNow Q3 2026 subscription revenue $3,988M, +21% YoY (20.5% cc); cRPO $13.65B +20.5%; 19 deals >$5M net new ACV; year-end AI net new ACV target raised from $1B to $1.7B","source":"ServiceNow Form 8-K Q3 FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001373715/000137371526000092/erq3fy26.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Management attributed part of Q3 strength to early renewals pulled into Q3 and a mix shift toward on-prem public-sector deals (secondary summary, unverified against filing)","source":"Secondary coverage of Q3 2026 results (betafinch/stockhub summaries)","url":"https://betafinch.com/episodes/NOW_2026_Q3_en","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"CEO McDermott said about half of ServiceNow net new business is not seat-based; seat offerings retained; consumption pricing layered on subscriptions","source":"itiger/press report: Servicenow Says Half of New Business Isn't Seat-based Pricing","url":"https://www.itiger.com/news/2653916047","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Gartner 3Q26 forecast (via third-party analysis): enterprise application software spend $496.3B in 2026, $812.6B by 2030; 2026 growth 13.9% USD / 12.7% cc; 2027 total revised $2.5B lower vs 2Q26","source":"Software Strategies Blog on Gartner forecast","url":"https://softwarestrategiesblog.com/2026/10/08/gartner-enterprise-application-software-forecast-812b-2030-crm-agentic-ai/","excerpt":null,"as_of":"2026-10-08","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"公司 10-K 風險因子自述：AI、低程式碼/無程式碼等能力日益重要，公司正與替代方案與做法競爭，且預期隨產品進入新鄰近市場會有更多競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"With this rapid evolution, we are increasingly competing with alternative solutions and approaches to solve customer needs, and we expect additional competition as we shift our products and services to compete with providers in new and adjacent markets.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"公司 10-K 自述平台架構可讓客戶部署 AI 強化工作流程而不必替換既有技術基礎設施，定位為 AI 分析與流程執行層之間的連接。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"our platform’s architecture, developed over years of iteration with customer feedback, allows organizations to deploy AI-enhanced workflows without replacing their existing technology infrastructure or disrupting established processes.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"二手評論稱 AI 工具（如 Claude Code）降低軟體開發門檻，企業可能自建內部工作流工具；且 agent 取代人力可能減少座位授權。","source":"247WallSt: ServiceNow was the SaaS stock AI was supposed to kill","url":"https://247wallst.com/investing/2026/07/06/servicenow-was-the-saas-stock-ai-was-supposed-to-kill-its-numbers-say-otherwise/","excerpt":null,"as_of":"2026-07-06","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Seeking Alpha 文章稱 ServiceNow 為 SaaSpocalypse 主要受害者，涉及座位制軟體模式受 AI agent 衝擊。","source":"Seeking Alpha: ServiceNow Is The Main Victim Of The SaaSpocalypse","url":"https://seekingalpha.com/article/4891314-servicenow-is-the-main-victim-of-the-saaspocalypse","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Futurum 分析稱 ServiceNow 定位為 AI 控制層，但競爭者正建立類似治理能力。","source":"Futurum: ServiceNow Q2 FY2026","url":"https://futurumgroup.com/insights/servicenow-q2-fy-2026-ai-security-and-workflow-expansion-fuel-growth/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：直銷組織占總營收 78%（2025、2024 皆 78%，2023 為 79%），其餘透過 MSP 與轉售夥伴；通路結構近三年穩定。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"Revenues from our direct sales organization represented 78% of our total revenues for each of the years ended December 31, 2025 and 2024 and 79% of our total revenues for the year ended December 31, 2023.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：以訂閱協議銷售，部分 AI 與資料方案另含超出訂閱服務點數後的用量計價成分。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"In addition to subscription offerings, certain AI and data solutions include a consumption-based pricing component that governs when customer usage exceeds the fixed number of service credits available under the customer’s subscription agreement.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"ServiceNow 2026-01 強化全球夥伴計畫：統一投資組合、簡化夥伴計價（單一年度會員費）、市場發展基金。","source":"BusinessWire: ServiceNow enhances global Partner Program to accelerate AI agent innovation","url":"https://www.businesswire.com/news/home/20260120828395/en/ServiceNow-enhances-global-Partner-Program-to-accelerate-AI-agent-innovation","excerpt":null,"as_of":"2026-01-20","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"ServiceNow 目標為訂閱加用量混合計價；AI 年度合約價值 2026 Q2 逾 10 億美元。","source":"Constellation Research / Subscription Insider","url":"https://www.constellationr.com/insights/news/servicenow-aims-goldilocks-software-model-saas-industry-likely-follow","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 (7/22 報告)：公司把全年訂閱營收中點上調 $15M 至 $15.770B（約 +21% 固定匯率）；另有摘要稱部分 beat 屬 on-prem 提前入帳、並提示短期毛利率壓力。搜尋未見 2026 年下調 guidance。","source":"ServiceNow Q2 2026 earnings call highlights (GuruFocus) / 搜尋摘要","url":"https://www.gurufocus.com/news/8973413/servicenow-inc-now-q2-2026-earnings-call-highlights-robust-growth-in-subscription-revenue-and-ai-adoption","excerpt":"Full-year subscription revenue midpoint increased by $15 million to $15.770 billion (21% YoY constant currency).","as_of":"2026-07-22","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q1 2026（4/22）全年訂閱營收 guidance 上調（一來源給 $15.735B–$15.775B），AI 營收目標由 $1B 升至 $1.5B；報告後股價單日大跌（約 17.8%，日期原文被截斷）。","source":"ServiceNow Form 8-K Q1 FY2026 / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001373715/000137371526000054/erq1fy26.htm","excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布（2026-08）：46 位分析師平均 $140.25、中位 $140、區間 $72–$248；評級 44 買/3 持有/2 賣。另一來源 65 位平均 $150.26（as of 2026-07-31）。同源報價約 $111，聚合站數據彼此不一致，未驗證。","source":"Walnut Invest ServiceNow stock forecast / Tickflow","url":"https://walnutinvest.com/stocks/now/forecast","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026 年春季目標價下修：Goldman 216→188、BTIG 200→185（BTIG 標題指 FY26 營收成長 guidance 受質疑）、Citi 177→154（4/23）；之後 Capital One 105→120（5/5）、Needham 115→155、BTIG 150→170（後兩者日期未載）。","source":"Yahoo Finance: ServiceNow Price Target Cut to $185 by BTIG / Placera telegram","url":"https://finance.yahoo.com/markets/stocks/articles/servicenow-price-target-cut-185-140659794.html","excerpt":null,"as_of":"2026-04-08","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Citi 目標價由 $177 調降至 $154，維持買進","source":"Placera telegram","url":"https://www.placera.se/telegram/citigroup-adjusts-price-target-on-servicenow-to-154-from-177-maintains-buy-rating-20260423","excerpt":"Citigroup Adjusts Price Target on ServiceNow to $154 From $177, Maintains Buy Rating MT Newswires 23 april, 15:26 Dela","as_of":"2026-04-23","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"ServiceNow 於 2026-04-20 完成約 77.5 億美元現金收購 Armis（網路暴露管理）。","source":"Pulse 2.0｜ServiceNow: $7.75 Billion Armis Acquisition Completed","url":"https://pulse2.com/servicenow-7-75-billion-armis-acquisition-completed-to-expand-ai-driven-cybersecurity-platform/amp/","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Moveworks 收購（約 28.5 億美元）於 2025-12-15 完成；Veza 於 2026-03-02 完成。","source":"BusinessWire｜ServiceNow completes acquisition of Moveworks; Start with Identity｜ServiceNow completes Veza acquisition","url":"https://www.businesswire.com/news/home/20251215128980/en/ServiceNow-completes-acquisition-of-Moveworks","excerpt":null,"as_of":"2025-12-15","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K 稱現行訴訟個別或合計預期無重大不利影響。","source":"SEC EDGAR｜10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"we do not believe that the ultimate resolution of any such proceedings, whether taken individually or in the aggregate, is likely to have a material adverse effect on our business, financial position, results of operations or cash flows.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"10-K 與 2026 年三份 10-Q 揭露 DOJ 對一項政府合約合規問題的調查（前美軍 CIO 聘僱案），公司無法預測時程與結果。","source":"SEC EDGAR｜10-K FY2025 / 10-Q FY2026（經搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"the Company has informed the Department of Justice, the Department of Defense Office of Inspector General and the Army Suspension and Debarment Office of the investigation","as_of":"2026-01-29","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Armis 收購約 77.5 億美元現金，2026-04-20 完成。","source":"Pulse 2.0｜Armis Acquisition Completed","url":"https://pulse2.com/servicenow-7-75-billion-armis-acquisition-completed-to-expand-ai-driven-cybersecurity-platform/amp/","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261102","affects":["valuation","moat_trend"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"-","claim":"Armis 收購部分現金對價由 2026-04-17 的 40 億美元定期貸款支應。","source":"SEC EDGAR｜8-K 2026-04-22 Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000054/now-20260417.htm","excerpt":"The Company used the proceeds from the Term Loan to finance a portion of the cash consideration used to acquire Armis Security Ltd.","as_of":"2026-04-22","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#2","axis":"ma_merger","section":"events","direction":"0","claim":"Moveworks（2025-12-15 完成）與 Veza（2026-03-02 完成）亦在近 12 個月內完成。","source":"BusinessWire｜ServiceNow completes acquisition of Moveworks","url":"https://www.businesswire.com/news/home/20251215128980/en/ServiceNow-completes-acquisition-of-Moveworks","excerpt":null,"as_of":"2025-12-15","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K Item 3：現行訴訟預期無重大不利影響。","source":"SEC EDGAR｜10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm","excerpt":"we do not believe that the ultimate resolution of any such proceedings, whether taken individually or in the aggregate, is likely to have a material adverse effect on our business, financial position, results of operations or cash flows.","as_of":"2026-01-29","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-10 原告律所 Levi & Korsinsky（經 SueWallSt）發出對 NOW 的投資人調查通告；搜尋未見已提起之集體訴訟。","source":"Placera｜ServiceNow Investigation Notice: SueWallSt Notifies Investors","url":"https://www.placera.se/pressmeddelanden/servicenow-investigation-notice-suewallst-notifies-investors-of-pending-investigation-into-servicenow-now-20261030","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"NOW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":73.08,"operating_margin_pct":9.68,"fcf_margin_pct":30.78,"rd_intensity_pct":22.47},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"PLTR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":84.8,"operating_margin_pct":42.8,"fcf_margin_pct":54.55,"rd_intensity_pct":10.42},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PLTR","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"CRM","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":77.28,"operating_margin_pct":21.52,"fcf_margin_pct":34.49,"rd_intensity_pct":14.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"MSFT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.66,"operating_margin_pct":47.1,"fcf_margin_pct":17.31,"rd_intensity_pct":10.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"DDOG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.51,"operating_margin_pct":0.43,"fcf_margin_pct":27.04,"rd_intensity_pct":43.69},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DDOG","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"NOW"},"financial_history":{"ticker":"NOW","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":7245000000.0,"revenue_yoy_pct":null,"gross_margin_pct":78.29,"operating_margin_pct":4.9,"net_income":325000000.0,"diluted_eps":0.32,"free_cash_flow":2173000000.0,"fcf_margin_pct":29.99,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":8971000000.0,"revenue_yoy_pct":23.82,"gross_margin_pct":78.59,"operating_margin_pct":8.49,"net_income":1731000000.0,"diluted_eps":1.684,"free_cash_flow":2701000000.0,"fcf_margin_pct":30.11,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":10984000000.0,"revenue_yoy_pct":22.44,"gross_margin_pct":79.18,"operating_margin_pct":12.42,"net_income":1425000000.0,"diluted_eps":1.368,"free_cash_flow":3375000000.0,"fcf_margin_pct":30.73,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":13278000000.0,"revenue_yoy_pct":20.88,"gross_margin_pct":77.53,"operating_margin_pct":13.74,"net_income":1748000000.0,"diluted_eps":1.67,"free_cash_flow":4533000000.0,"fcf_margin_pct":34.14,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/NOW/NOW_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**ServiceNow, Inc.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to the Third Quarter 2026 ServiceNow Earnings Conference Call. [Operator Instructions]
I will now hand the conference over to Darren Yip, Senior Vice President, Investor Relations and Market Insights. Darren, please go ahead.

**Darren Yip** (Executives):
Good afternoon, and thank you for joining ServiceNow's Third Quarter 2026 Earnings Conference Call. Joining me are Bill McDermott, our Chairman and Chief Executive Officer; Gina Mastantuono, our President and Chief Financial Officer; and Amit Zavery, President, Chief Product Officer and Chief Operating Officer.
During today's call, we will review our third quarter 2026 results and discuss our guidance for the fourth quarter and full year 2026. Before we get started, we want to emphasize that the information discussed on this call, including our guidance, is based on information as of today and contains forward-looking statements that involve risks, uncertainties and assumptions. We undertake no duty or obligation to update such statements as a result of new information or future events. Please refer to today's earnings press release and our SEC filings, including our most recent 10-Q and 10-K, for factors that may cause actual results to differ materially from our forward-looking statements. 
We'd also like to point out that we present non-GAAP measures in addition to and not as a substitute for financial measures calculated in accordance with GAAP. Unless otherwise noted, all financial measures and related growth rates we discuss today are non-GAAP except for revenues, remaining performance obligations, or RPO, current RPO and cash and investments. To see the reconciliation between these non-GAAP and GAAP measures, please refer to today's earnings press release and investor presentation, which are both posted on our website at investors.servicenow.com. A replay of today's call will also be posted on our website.
With that, I'll turn the call over to Bill.

**William McDermott** (Executives):
Thank you, Darren, and thank you, everyone, for joining today's call. For more than 7 years now, I've said ServiceNow is a one-of-one company, one of one. As you'll hear, these Q3 results represent a trifecta moment for ServiceNow, quarterly results beating expectations across the board again, significantly accelerating AI performance at the largest quantum yet, a hybrid business model shifting more to consumption.
So let's do the standard results first. Subscription revenue growth was 20.5% in constant currency, 50 basis points above the high end of our guidance. cRPO was 21% in constant currency, 100 basis points above our guidance. Operating margin was 32.5%, 150 basis points above our guidance. Free cash flow margin was 20%. We had 19 deals greater than $5 million net new ACV in Q3, up 135% year-over-year. We have a $30 billion remaining performance obligation growing at 23% year-over-year. That's growth at scale.
To my trifecta point, here is where the Q3 print gets even more dynamic. For many quarters now, we've been aggressively building the consumption engine into the business model. Our ambition is to be the governed execution layer for enterprise AI with multiple commercialization paths, all driven by customer choice. Q3 is the banner achievement to date. The strategy is working. We have tangible AI monetization. AI, net new ACV was 65% year-over-year growth in Q3. Control Tower, net new ACV grew over 6x year-over-year. Our agentic front door EmployeeWorks reached $100 million ACV in less than three quarters. The number of $1 million-plus AI deals grew 4.5x year-over-year. Year-to-date, agentic AI consumption in production is up 13x year-over-year. 
If you look at the consumption of Action Fabric assists alone, that number is up 500% month-over-month. This is not only the direction of our customers, this is where they want us to go. It's the right direction for long-term shareholder value creation as well. As a reminder, we began the year with a $1 billion AI target by year-end. We raised that target to $1.5 billion at Financial Analyst Day in May. Today, we are raising that target again this time to $1.7 billion plus by year-end. And as you've come to know me pretty well by now, I've challenged the team to even surpass that number.
Overall, the company is now full speed in our Q4, and Gina will give you the guide shortly. But I don't want you to wait too long. She will raise. As everyone on this call knows, ServiceNow always closes strong. We have no intention of delivering anything less than the best year in our history.
Let's spend a few minutes on what remains a very complex environment for the enterprise. We hosted our biannual CEO event with more than 125 CEOs a few weeks ago. Here's what I heard. All of them are investing in the intelligence revolution. They've spent billions on it so far. They all went through the token maxing phase. Here's the big lesson they all learned. All of the vibe slop flops, sprawl, and lack of integration are even greater risks in the AI world. 
When I spoke to them about ServiceNow's role as the Super Intelligence Control Tower for business reinvention, their endorsement was universal. Our SICT, Super Intelligence Control Tower, brings together the right model for the right workload to solve the right problem and unlock the right opportunity for our customers. Businesses in every industry need a harness for enterprise AI. This is more than orchestration, governance or security alone. It's the nexus of all three categories coming together.
We're now in the rules and rails phase of enterprise intelligence. 94% of enterprises report gaps in AI visibility. 88% can't even distinguish personal AI accounts from corporate instances. ServiceNow's Control Tower discovers and inventories the entire AI estate. As stories of rogue agents persist, ServiceNow controls what agents can do. That's why we introduced AI Passport to issue every agent an official attested record based on context in our platform. Who owns the agent? What's it allowed to do? What data can it access? How much risk exposure is it allowed to take? 
This enables the most capable kill switch available in the enterprise today. When our Control Tower revokes a passport, NVIDIA Sentry stops honoring it and the agent stops at the infrastructure layer. We are scaling that capacity everywhere. Our Control Tower signals Okta, Microsoft Azure AI Foundry and Google Gemini enterprise agent platform, so they can cut off the agent's access wherever it runs. ServiceNow already sits at the operational core of the world's largest enterprises, the CMDB, the Workflow Data Fabric, 20-plus years of embedded operational intelligence and context across IT, security and risk.
With Armis and Veza, we can now pinpoint specific known vulnerabilities against the cybersecurity landscape that has irreversibly changed. We call this Shift Zero. It moves security from remediation to prevention from human speed to machine speed and from blind to govern. The average enterprise runs more than 70 security tools. ServiceNow offers a single govern system with proof of what acted, why and who is accountable. This is not an incremental improvement to a reactive model. It is the replacement to consolidate a fragmented market. It is the gateway to autonomous defense. That's why we're the fastest-growing cybersecurity company at scale and why the growth is accelerating so rapidly.
When you're operating in the super intelligence era, the pace of innovation has to keep pace with the growing size of the opportunity. I'm really proud of what the ServiceNow team has delivered. Our Level 1 service desk specialist resolves incidents 85% faster than human agents. This is now in full autonomous production across customers of varying size and sector from a global automotive leader to a leading enterprise technology company. Our AIOps specialist has already reduced median time to resolution by 40% within the first month. We now have over 100 customers actively innovating with our AI specialists, AIOps, HRSD and CRM specialists are expected to become generally available in Q4.
As enterprises rethink the mandate of their CRM systems, ServiceNow is leading the way. The old CRM was built for sales teams. The new one has to work across your entire business. That's a different product. That's a different architecture. And that's why we're seeing customers rip and replace not just add alongside. Conversational voice AI is the next big leap in connecting the front office to the entire enterprise. The customer conversation is where the work starts. The platform has to carry it through every system and workflow behind it. We're redefining how enterprises engage with customers. Our tuck-in of Sweep adds deep expertise in rapid agentic deployments, giving us another gear to accelerate, while improving customer outcomes. And one year after we brought Logik.ai into ServiceNow, we've been named the leader and customer favorite in The Forrester Wave for Configure, Price, and Quote solutions. We see a similar change in gravity for the employee experience.
For the Fortune 500,000, we introduced Flow. There are many enterprises that want leading domain expertise but aren't ready for formalized ITSM. Flow fills the gap, a new conversational service desk that is self-serve and consumption billed. A customer that signs up for Flow today can begin using Flow today. That's a big reason it's off to a lightning fast start with businesses and government agencies around the world. ServiceNow EmployeeWorks continues to be a fast growth machine. This gives enterprises one place to search, knowledge, get things done and route work across IT, HR, finance and procurement. 
It also becomes the destination for employees to build AI assistants, agents and automations, all secured by enterprise guardrails. This is only scratching the surface of the groundbreaking innovation on the ServiceNow platform. Even the best platform won't deliver for enterprises alone. ServiceNow Control Tower Alliance is a new ecosystem of leading companies in AI, cloud infrastructure, security, governance and token management who will help customers adopt trusted enterprise AI safely at scale. Founding partners include Anthropic, AWS, Cisco, HiddenLayer, Kong, Okta, OpenAI, WitnessAI and Zenity.
Today, ServiceNow announced an expanded partnership with OpenAI to help enterprises move seamlessly from AI reasoning to governed action. The partnership expansion starts with a new ServiceNow plug-in for ChatGPT, enabled by Action Fabric. We aim to develop security and risk solutions powered by OpenAI cyber models, a Codex integration and AI workflow factory and voice-driven governance for ServiceNow's Super Intelligence Control Tower. 
We have very big plans for this partnership, especially in cybersecurity. We expanded the partnership between Google Gemini Enterprise and ServiceNow Action Fabric. Gemini Enterprise provides the conversational front end, while ServiceNow provides the governed industry workflow execution. Our partnership with INRY, a Cprime company, shows what happens when a partner builds on ServiceNow before they sell it. INRY went live on EmployeeWorks in six weeks. That's the new bar for time to value rather than the exception. They didn't sell the solution until they lived on it themselves. Median submission time is now down 60%, completion rates 97%. ServiceNow and Aramco Digital established an agreement to standardize and govern digital workflows across Aramco's affiliates, subsidiaries and joint ventures in more than 50 countries, and the list goes on and on.
I could end on the countless industry accolades we've earned: Three new Gartner Magic Quadrants, two new Forrester Waves, IDC reports and many more. Instead, I'll close with the ultimate measure of a defining enterprise technology company, our customers. A major Asian telecommunications leader with over 130,000 employees and contractors became the first enterprise in the region to deploy ServiceNow Autonomous Workforce for a zero-touch help desk in IT and HR. This will handle 70,000 IT requests and 6,000 HR inquiries annually. The Salvation Army, Australia is using ServiceNow AI specialists to give frontline employees more than 5,000 hours back so far, time that is redirected towards supporting community members that are in need. 
Germany's professional soccer league expanded with ServiceNow as its official CRM partner. It's about one month, only one month. They've already consolidated fan services from seven digital channels into a single ServiceNow platform, resolving 89% of inquiries at first contact, cutting previous case volumes in half.
When a global logistics leader's shipment operations were drawing terrible manual work processes across siloed systems that was soul crushing. ServiceNow built them an AI Partner, the Shipment Issue Analyzer. The result is nearly 100,000 hours saved annually, resolution from three days to less than 30 minutes. Jack Henry & Associates, one of the leading financial technology companies in the U.S. chose ServiceNow CRM to modernize its CRM capabilities with AI that automates routine tasks and strengthens post-sale operations. At a consumer finance company, spotting risk meant sending it nowhere, multiple channels, unclear ownership, legacy systems swallowing signals.
Our applied AI FDE team, fully deployed engineers, built them the AI Risk front door, a two-layer agent architecture targeting 85% accuracy. It compressed signal to routed case time by more than 85%. Nestle has started to leverage our Control Tower to scale AI with strong governance across its operations. They are progressively deploying agentic marketing operations across 60 countries with the potential to reduce marketing campaign coordination by 25%. And together, we continue to drive innovation across all key business functions. InterContinental Hotels Group, one of the world's largest hospitality and travel services companies is using Veza from ServiceNow to govern who and what can access its systems so it can safely scale across its 7,000 hotels worldwide. These amazing enterprises are putting AI to work for people. They're doing it with ServiceNow on our AI platform with the security of our Super Intelligence Control Tower. We see clear momentum in AI monetization driven by our organic innovation, our pricing, and our intelligent packaging.
Our security business is differentiated with the potential to be even bigger in a few years than all of ServiceNow is today. We're strong across industries, including the public sector, which once again delivered in its biggest quarter of the year.
We're not compute constrained. We don't have capital constraints. We're activating a hybrid business model. As you'll hear in the raised full year guidance, we're a company going from the Rule of 56 to the Rule of 57 on our way to the Rule of 60. That, of course, is free cash flow plus revenue growth. We have six businesses that have now surpassed more than $1 billion run rate with a TAM that continues to multiply and expand. What other businesses are there that can even contemplate these fundamentals? And it's only getting better as the cost of intelligence falls, the tailwind for software is strengthening. We are a one-of-one growth company. We have deep incumbency in the enterprise with proven global distribution. We're honoring the principle and the promise that the world works with ServiceNow.
I really appreciate your belief and support. I look forward to your questions. And now I'll turn things over to our President and Chief Financial Officer, Gina Mastantuono. Gina, over to you.

**Gina Mastantuono** (Executives):
Thank you, Bill. We delivered another strong quarter, exceeding the high end of our guidance across every top line and profitability metric. Q3's results reinforce that ServiceNow is becoming even more strategic as enterprises move from experimenting with AI to deploying it at scale. Customers want the productivity and growth that come with super intelligence, but they also need the visibility and security to do so with confidence. With the ServiceNow AI platform at the operational core of the world's largest enterprises, we are perfectly positioned to help customers put AI to work across their business, govern every agent in action and translate intelligence into secure, measurable outcomes. 
Q3 subscription revenues were $3.988 billion, growing 20.5% year-over-year in constant currency and 50 basis points above the high end of our guidance. RPO ended the quarter at $29.7 billion, representing 22.5% year-over-year constant currency growth as average customer contract duration continues to expand. Current RPO was $13.65 billion, representing 21% year-over-year constant currency growth, a 100 basis point beat versus our guidance. Across our workflows, we saw widespread demand. Technology workflows had 54 deals over $1 million, including 6 over $5 million. Demand for our core workflows remains robust as every new AI asset and agent introduces greater requirements to manage, monitor, secure and govern the enterprise. 
ITSM was in 11 of our top 20 deals, ITOM was in 9 of our top 20 deals with 14 deals over $1 million. Asset Management crossed $1 billion in ACV this quarter and was in 13 of our top 20 deals with 11 deals over $1 million, and our Security and Risk solutions were in 16 of our top 20 deals with 13 deals over $1 million. CRM and industry workflows maintained its rapid growth trajectory and we were in 13 of our top 20 deals with $1 million-plus deals surging to 28 in the quarter. Core business workflows had 15 deals in the top 20 with 24 deals over $1 million, and Creator workflows had 19 deals in the top 20 with 13 over $1 million. From an industry perspective, business and consumer services led the way with net new ACV growing over 3x year-over-year. Technology had robust growth as well at nearly 40%. Our U.S. Federal business also delivered an excellent quarter with deals over $1 million growing over 30% year-over-year. We expect federal net new ACV growth to accelerate further in Q4 as agencies increasingly see ServiceNow as the AI operating system for the enterprise. 
In Q3, our renewal rate remained best-in-class at 98%, reflecting the enduring value we deliver to our customers. We ended the quarter with 680 customers generating more than $5 million in ACV, with 31 additional customers surpassing $20 million in ACV over the past year. As our largest customers continue to scale with ServiceNow, they're expanding their platform adoption with 19 of our top 20 deals, including six or more products. The momentum in our AI solutions continues to build. We continue to exceed our AI expectations for the year with AI net new ACV growing 65% year-over-year in Q3, allowing us to raise our AI ACV target for the second time this year from $1 billion at the start of the year to now $1.7 billion by the end of 2026. In Q3, the number of AI deals over $1 million grew 4.5x year-over-year. We're also seeing customers embrace AI more broadly across their enterprises with deals spanning five or more AI products increasing over 8.5x year-over-year.
AI adoption is pervasive across the platform, evident in every workflow. ITSM AI deal volume increased nearly 80% year-over-year. HRSD AI deal volume nearly doubled. Newer AI solutions saw deal volume grow even faster with ITOM growing more than 7x and portfolio management more than 6.5x. We also saw strong net new ACV momentum with security and risk AI growing more than 4.5x year-over-year. App Engine AI more than 4x and Asset Management AI nearly tripling. CRM AI had a standout quarter as well with net new ACV tripling both quarter-over-quarter and year-over-year.
Just as importantly, customers are moving rapidly from adoption to production. As Bill mentioned, our year-to-date consumption of agentic AI in production is up more than 13x year-over-year. We're passionate about helping customers realize value faster. With the help of our forward deployed engineers, we've seen an accelerated time to value of 80% year-to-date. For example, one European customer went live in just 12 weeks and is on track to consume nearly 1.5 million in annual assists. When we provide deployment expertise as we've seen AI adoption move twice as fast in just the first five weeks of involvement.
Turning to profitability. Non-GAAP operating margin was 32.5%, 150 basis points above our guidance, driven by the revenue outperformance, efficiency gains and timing of spend. From a productivity standpoint, our internal use of AI is now generating more than $1 billion in annualized value, more than double the level we exited 2025. Free cash flow margin was 20%. Together, these results continue to demonstrate our ability to drive a strong balance of world-class growth, profitability and shareholder value.
Moving to our outlook. For 2026, we're raising our subscription revenues by $15 million at the midpoint from $15.77 billion to $15.785 billion, representing 21% year-over-year growth on a constant currency basis. We are raising our full year free cash flow margin target by 100 basis points from 35% to 36%, driven by lower CapEx spend. Against the backdrop of growing investor scrutiny around AI-related infrastructure spend and leverage, ServiceNow is positioned to capture the AI opportunity while reducing its CapEx and expanding free cash flow margins. 
We continue to expect subscription gross margin of 81% and operating margin of 31.5%, up 50 basis points year-over-year. Our execution has enabled us to fully offset the dilution from acquisitions this year and still deliver meaningful margin expansion across both operating and free cash flow margins, reinforcing the strength and scalability of our business model. 
Finally, we expect GAAP diluted weighted average outstanding shares of 1.04 billion. For Q4, we expect subscription revenues between $4.245 billion and $4.255 billion, representing 21.5% year-over-year growth on a constant currency basis. We expect cRPO growth of 18.5% on a constant currency basis. This reflects a higher mix of on-prem deals and excludes a rising balance of T4C backlog, both of which contribute to revenue but not cRPO. We expect an operating margin of 32%, and we expect 1.05 billion GAAP diluted weighted average outstanding shares for the quarter. 
In closing, Q3 was another strong quarter of execution and accelerating AI adoption. What excites us even more is the scale of the opportunity still in front of us. From SI Control Tower and Autonomous Security to EmployeeWorks and our growing portfolio of AI specialists, we're helping customers operationalize AI across the enterprise, turning innovation into measurable business outcomes and ROI. Just as important, we're helping customers accelerate adoption without losing control. This is where ServiceNow is differentiated. By combining workflow, data, AI and governance on a single platform, we can help customers manage the complexity of the AI era, while unlocking its full potential. This gives us confidence in the substantial growth opportunity ahead and our ability to create long-term value for customers and shareholders.
Bill and I would like to thank our employees around the world for their continued focus, execution and commitment. Their ability to innovate, while operating with discipline is what enables us to consistently deliver quarter after quarter. 
With that, I'll open it up for Q&A.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Brad Zelnick from Deutsche Bank.

**Brad Zelnick** (Analysts):
Bill, we increasingly hear about AI-native applications companies implementing outcome or value-based pricing. And I was just curious to what extent you're seeing customers asking you to go down this path? I know you have a perfect mix of subscription and consumption, but it seems like the market is moving in this direction.
And maybe for Gina, I imagine this is something you've contemplated internally. What would the impact of something like this be on the financial model?

**William McDermott** (Executives):
Brad, thank you. We have the best of both worlds in the sense that the customer likes the predictability of the seat-based pricing model for their budgeting purposes, people that run Fortune 2000 companies run on budget. So we give them that. And also, we're driving consumption. And the idea is simple: get the customer live fast. And once they're live, the token economics take off, whereby we have a chance to improve our revenue per user by a factor of 5x. And that's only because the customer derives substantially more value than that. So it's kind of a win-win.
I would also point out that with the announcement of Flow, the native AI stand-alone autonomous service desk type of provider are no longer required as we have that now shipping it globally. So you can buy it online and you can go live in the same day. So that will be yet another net new ACV engine for the company and obviously, a problem for the competition. So again, best of both worlds.
One thing that really is interesting with the Super Intelligence Control Tower, you should know a 500% growth month-over-month in terms of the AI action that's activated in that Super Intelligence Control Tower, coupled with a 13x improvement in AI consumption. So clearly, we're benefiting from our current model because we're growing 21% year-over-year. And this hockey stick formation has yet to be fully realized. And so I think that is yet another exciting point for the investors to contemplate.

**Gina Mastantuono** (Executives):
And then, Brad, from the impact on the financial model, as Bill said, our customers are very focused and quite happy with the hybrid model that we have today and are not asking at all for outcome pricing. And so you would imagine if the day were to change that we'd be ready and waiting for that. But as of now, our customers are very, very happy with the hybrid model, as Bill talked about.

**Operator** (Operator):
Your next question comes from the line of Alex Zukin from Wolfe Research.

**Aleksandr Zukin** (Analysts):
Congrats on another strong performance. I guess maybe, Bill or Gina, for you, there was some nuance on kind of some of the impacts that you're seeing on the numbers and the guide, particularly for Q4 on cRPO and subscription revenue. Maybe to the extent that, again, all of the metrics that you're citing sound like you're expanding your growth opportunity, expanding your growth potential. Obviously, the stock is down pretty meaningfully after market on some of the, I think, the 4Q guide. But any constant kind of comments on your confidence in growth going kind of either staying high or going higher, particularly even for next year as some of these nuances normalize and they don't necessarily impact subscription revenue as much as maybe the cRPO deceleration would imply?

**Gina Mastantuono** (Executives):
Thank you, Alex, and I appreciate the question. And yes, so first and foremost, we remain as confident as ever in our growth opportunities, as I hope came through very clearly in both Bill and my prepared remarks. We had strong beats across the board, revenue, cRPO, op margin, free cash flow. We raised free cash flow margin.
On the revenue beat, what I'd say is that while we actually passed through half of the beat, all of the FX and half of the beat that we saw in Q3, to the full year guide. With respect to why we didn't raise by the entire beat, there's a couple of things. And so number one, with our scale, the speed is really strong, and we feel really good about that. But to help our customers realize value even faster at scale, we've made the strategic decision to invest in their success by including delivery expertise with our platform solutions to accelerate AI deployments for select large deals.
From an accounting perspective only, the value of those deployments are carved out as subscription revenue, and they're included in professional services rather than subscription revenue. Notably, upon renewal of those contracts, the value of those services return to subscription revenue. So it provides a structural acceleration to growth. And it's not huge, about 25 bps in Q3 and expecting it to have approximately 50 bps in Q4, which is the only reason why we didn't pass through the full beat in Q3 into the rest of the year. So subscription revenue, feel really, really strong about that.
With respect to cRPO, we saw strong early renewals in Q3 that contributed about half of the beat in Q3. Now that has a negative impact in Q4 because we pulled those deals out of Q4 and into Q3. So that growth is already in Q3. A couple of other things to factor in. Strong public sector demand is driving higher on-prem mix in Q4, which is actually a great result. But that is driving a 25% -- sorry, 25 basis points headwind in Q4 cRPO, but will absolutely hit revenue and the part of revenue. 
The other thing is those incremental investments in deployment expertise, a small modest RPO headwind also does not impact revenue in the long term. And just more generally, I'd note, and we've talked about this before, right, cRPO is a very nuanced accounting metric, and it doesn't necessarily capture all of the momentum in the business. 
A good example for that is there's approximately 50 basis points of year-over-year subscription backlog growth that's excluded from cRPO in Q4 due to T4C provisions, but absolutely will be included in revenue. And so while cRPO is a good indicator of next year's revenue, it's certainly not perfect. And the momentum you're hearing in the business, especially around all of the AI amazing things will absolutely translate to strong revenue growth in 2027 and beyond. And at the end of the day, we feel as confident, if not more confident today in our growth opportunities than ever before.

**Operator** (Operator):
Your next question comes from the line of Adam Wood from Morgan Stanley.

**Sanjit Singh** (Analysts):
This is Sanjit Singh for Adam. I wanted to just zoom out a little bit and just talk about the momentum you're seeing on the AI ACV side. Gina as you noted, you've raised the guidance twice now to $1.7 billion in revenue. At the same time, if we look at just the broad story of cRPO, we could call it stable, maybe on an organic basis, modestly decelerating, but sort of generally stable. So my high-level question, Bill, is just when do you think the AI momentum will start to translate to overall top line acceleration, cRPO acceleration? And with respect to that, in terms of the go-to-market motion, you guys have made a lot of pricing and packaging changes. You guys just noted that you're doubling down on delivery. Do you feel you have the sort of AI agentic sales go-to-market motion right? Or is there room for improvement on that front?

**William McDermott** (Executives):
Thank you very much, Adam. First of all, let me just be extremely clear. The business has never been in better shape than it is right now. And I think one of the luxuries that you have when you have the Super Intelligence Control Tower and every partner, that's a hyperscaler or a lab company, these are great companies from NVIDIA all the way through to the labs are teaming up with ServiceNow and realize the importance of coming through our Super Intelligence control tower to drive enterprise value for their customers also. And that's where the network effect is really starting to kick in to extra high gear. So I want you to please register that as a significant momentum advantage that we are experiencing. 
And also, we are very cognizant of the importance of getting these customers live fast. They have to get value out of AI now. And so as Gina said, we've made the necessary decisions strategically to get them live fast, invest in doing that, so ultimately, they can not only derive the benefit from the license, but they can also activate the tokens to create the tokenomics that our shareholders are looking for and also that their shareholders are looking for. So that virtuous cycle is kicking into high gear. And as I mentioned, we have a 500% month-over-month increase in the activity on the Super Intelligence Control Tower and a 13x improvement on the AI consumption itself. So the strategy is working, and yet we're still in the early days.
You will absolutely see in some now, but also in 2027, as Gina said, the true acceleration because it's all about the customer getting these implementations and getting these tokens activated in their workflows or their business processes. But we have made a decision as a company and our ecosystem to do that because that's where the long-term value creation exists for us, for the shareholders and most importantly, for the customer. So I feel great about it.

**Gina Mastantuono** (Executives):
And then -- and I'll just take you back to Financial Analyst Day, Adam, when we talked about by 2030, our AI business would be 30% of our ACV. And so we're absolutely on path and trajectory to get there, if not actually ahead of schedule, as you can tell by our continued raise of AI, but we are well on our path.

**Operator** (Operator):
Your next question comes from the line of Samik Chatterjee from JPMorgan.

**Samik Chatterjee** (Analysts):
Maybe if I can just go back to the strategic decision to invest with your customers to accelerate AI adoption with them. It sounds like you did some of that investment in Q3 already. Any early data points in terms of those engagements that is driving the confidence about sort of expansion on AI adoption from them? And what you -- what are sort of the ideal metrics you've been focusing on to measure that outcome there with the customer?

**Gina Mastantuono** (Executives):
Absolutely. And as you can imagine, this market for AI is moving very quickly, and so are we. And we noticed that customers receiving the support saw AI adoption progress twice as fast during just the first five weeks of that support with multiples higher of assist consumption and product usage versus those without support. So that assist consumption and product usage are the metrics that we're looking at. And when we're seeing accelerating customer AI consumption, as you would expect, it unlocks a significantly larger monetization opportunity, making the ROI very compelling. Therefore, we're reacting by building more of these deployment teams into our forecast because we're seeing such incredible results.

**William McDermott** (Executives):
And I would add to that, Samik, just one very interesting move that we made, which was the acquisition of Sweep. And as you know, one of the big reasons why customers sometimes have a more difficult time changing from one CRM system to another is they have a long implementation cycle, and nobody wants to have a long implementation cycle, especially when it relates to taking care of their customers. 
And so now we're able to accelerate the deployment times for CRM to -- instead of talking years, we're talking a month. We're talking like days, 30 days, 60 days for a serious company of serious scale. This same logic also applies to the enterprise Super Intelligence Control Tower and all of the workflow processes on ITSM as an example. In 24 hours, we activated that.
So what we're looking at here is a Super Intelligence Control Tower, a completely open ecosystem feeding into the rules and the rails of the way the enterprise runs, connecting the fabric of the data and the processes, and we're going to do this at record pace. So it's going to drive implementation cycles to record speeds, which is necessary to get the tokens fully consumed, activated and generating revenue.
As I always want to remind everybody in our company and otherwise, there's no other company growing at the rule of 57 in the enterprise software industry. If you could find them, please let me know. I want to talk to them. I want to get the best practices with 21% growth on revenue and 36% growth on free cash flow, all while building the most superior super intelligent control tower that the world has ever known. So I want to meet that company.

**Operator** (Operator):
Your next question comes from the line of Peter Weed at Bernstein.

**Peter Weed** (Analysts):
I think one of the impressive things you've been doing is investing internally in productivity optimization. And I think we're seeing that come through pretty significantly in some of the headcount numbers. Can you help us understand how that's playing out because it looks like a lot of it is actually focused in maybe front office product and sales and marketing. And how are you able to get that productivity in these areas to the level that you want, while this is also what will be driving revenue looking forward?

**Gina Mastantuono** (Executives):
Thanks, Peter. So, first and foremost, so, so excited to say that we've crossed $1 billion in efficiency gains through our own internal use of AI and the lion's share of that is coming from our own use of our own products Now on Now. So it's just incredible. And yes, that efficiency gains means that we're able to not hire as many people. That being said, we're absolutely hiring folks in the right spots. And so while you might see total sales and marketing headcount come down, actually quota-bearing heads are up double digits, while sales operations, for example, is down significantly. 
And very similar in the R&D organization. As you would imagine, real increases in AI engineers in top talent, but there's lots of efficiency gains that we're driving through AI. That means that we don't have to hire as many support people, for example, or overhead in the R&D organization. And so we're absolutely still hiring across the board in both go-to-market and R&D. We're hiring in the right places, but that's being offset by incredible efficiencies that allow us to bring those more operational roles, those headcount roles down significantly.

**William McDermott** (Executives):
And I would build just to share with you, Peter, a couple of things that are very interesting. We have our own EmployeeWorks solution in the company. And so if you think about our great go-to-market machine, which is the best in the industry by far, they all have a coach, and that happens to be EmployeeWorks. And so it is autonomously activating all of the controls that are necessary to build great customer relationships and bring all of our innovation to the customer. This is being done autonomously, not that they have to even request it. They're also getting the insight pushed to them to make them more productive on the front line. 
Think about it. If you go back 3 years, that was like 100 people in the sales operations department moving around information on e-mail, that is now completely autonomous. It's a sales coach in the pocket. It's driving enormous productivity. And just to be clear, we're actually significantly improving and increasing feet on the street. And while our ultimate headcount has actually slightly declined, which is a gorgeous situation, as Gina pointed out, the 90% response time to customer service or employee service inquiries is now done autonomously in a way that is so much easier for people to deal with, and it gives them an improvement in their life experience here at ServiceNow. 
Finally, while the headcount may remain consistent, we continue to strengthen the workforce. So we continue to bring in net new talent in AI on the innovation side and on the quota-bearing side, we have a higher standard for the kind of individuals we need to take us from here to there. So while the headcount is steady, the innovation and the improvement of the human capital condition has only increased substantially. So that's a very important thing that sometimes doesn't show up in the numbers.

**Operator** (Operator):
Your next question is from the line of Arjun Bhatia from William Blair.

**Arjun Bhatia** (Analysts):
I'll add my congrats on a good Q3. I want to go back to an earlier question. Bill, one of the most important sort of biggest debates and questions that we get from investors is whether AI is cannibalistic or accretive to software companies. And we're kind of seeing this in your results where the AI adoption is increasing and accelerating and you're seeing raises on that guidance and then some of the other metrics are sort of not yet inflecting. 
And I'm just curious, and I'm sure there's a timing mismatch there. But when you look at your early adopters and your most advanced AI customers, what are you seeing in terms of how their overall spend with ServiceNow is changing as they've adopted Now Assist and your AI capabilities?

**William McDermott** (Executives):
Yes. There's no doubt. First of all, I really remind people, including at the CEO meeting that I referenced, the world GDP rests on super intelligence and this intelligence -- really this intelligence generation that we'll look back on 10 years from now and say that was a renaissance moment. And so all the business cases that are tied to return on invested capital from AI are a factor 10x greater than anything that preceded AI solutions.
So this is really like unbelievable stuff. I mean, just take ourselves. Gina talks about $1 billion, $1 billion is a lot. $1 billion in a year is a lot of money. And what's unbelievable in terms of the operational performance of the company, we continue to grow the company at a pace consistent on a much larger base than we were growing before we saved $1 billion. So less people doing extraordinary things, enjoying their work much more because the autonomy of the AI platform has taken the pressure off of them so they could do the work that really matters. So we're one example. But the business cases, and we review them all the time with Amit and Paul, they have a 10x improvement over anything that we've seen before. 
And Amit, feel free to comment on it.

**Amit Zavery** (Executives):
Yes. Arjun, on your question about the use cases and how we're seeing that adoption grow. Many of the customers typically start with one or two use cases where we help them or they decide like incident management or triaging or resolution planning. And once they see that go live, we've seen that go up to 3x, 4x usage, but also new use cases emerge because now they're seeing it in the production environment. So that's really been the growth. I mean if you see a lot of the customers we talked about in last quarter as well as now, they're re-upping their licenses and the new renewals with higher tokens because they're seeing the adoption go up as well. 
We have customers like Nestle, for example, they went live in six weeks with this marketing optimization, agentic workflow. And now they're unleashing that in 90 different countries, and they're starting to now use it across the world to get value out of one time the use case they build and grow it significantly across the world as well.
So those are kind of the common patterns we see. And then we're seeing this autonomous IT, for example, and then with that kind of use case going into AIOps, CRM optimization and other industry industrial use cases as well. So very, very easy to kind of start seeing that growth come through.

**Operator** (Operator):
Your next question comes from the line of Samad Samana from Jefferies.

**Samad Samana** (Analysts):
So, Gina, I just wanted to ask about the decision to have resources for large customers to accelerate AI deployment. I'm curious, I guess, when was that decision made? And I'm just curious how we should think about modeling that? Is this something that will be broadly available? Is it something that's on a customer-by-customer basis? And then is there anything that we need to make a consideration for given the rev rec on the margin side as well? Maybe just help unpack that for us and what you're assuming in the forward guidance given -- I know it's not the biggest thing that happened, but it did sway, I think, the guidance a little bit. And so I think investors would get some more comfort if we had more color on how to unpack that.

**Gina Mastantuono** (Executives):
Yes, perfect. So yes, as I said earlier, Samad, the market for AI is moving very quickly, and so are we. So when we saw the real inflection with customers that were receiving the support, we decided to double down because that consumption flywheel is going to drive significant incremental growth, right? And so deployment times are rapidly improving, and these services are being, as you say, provided for a select number of large deals, and we talked about it's in the number, 25 bps in Q3 and 50 bps in Q4. And we don't expect to include this delivery expertise over the long term. As with other new technology adoption cycles, it's really about optimizing the first wave of adopters and leveraging the know-how in a repeatable and scalable way. And as the AI gets better, the ability to autonomously deploy gets easier and easier. And so we don't expect this to be long term, but we absolutely believe it's the right thing for the business and is going to continue to help drive that consumption flywheel.

**Amit Zavery** (Executives):
I'll add on this, Mr. Samad. We're also building -- using AI implementation agents. So what -- when we help our customers go live, a lot of the heavy lifting is done by AI. This is really identifying the early use cases and make it simple for them to go live with it. And once they get 1 or 2 of these live, then the volume goes up very quickly. So this is not a long-term engagement. It's very short, but we get that value quickly for customers.

**Operator** (Operator):
Your next question comes from the line of Kirk Materne from Evercore ISI.

**S. Kirk Materne** (Analysts):
Bill, I was just wondering on Control Tower. Obviously, everybody is getting ready to have to build an orchestration layer to take -- to sort of manage their agents at scale. Are they doing that now? Or are they waiting until they get more deployment in production? I was just wondering how you guys see that playing out where they're going to lay out sort of a baseline and then they can drive consumption once the agentic population builds up. I was just wondering if you could give us some color on that front.

**William McDermott** (Executives):
Yes, sure, sure. First, I'll just say big picture, the Super Intelligence Control Tower is basically redesigning what the enterprise visibility, governance and security posture is of these major corporations. And if you look at the partnerships we announced today across the board and especially OpenAI, it's clear that the best and smartest companies in the world realize that this Control Tower and activating that across rules and rails that are deterministic and companies rely on to run their business is a pretty important thing to do to grow their businesses. 
So Amit can give you some color on exactly how we're driving this and the impact that it's having.

**Amit Zavery** (Executives):
Yes. Thank you, Bill. So Kirk, usually, I think if you look at last year, the concerns many customers had when we speak to them is they had no idea of what's going on with AI, how many shadow projects are going on, what agents are doing. So Control Tower really resonated very well when we introduced it last year because we are kind of putting this in front of the AI deployments. This is really the governance, the trust and the safety layer, which gives you a lot of confidence and the ability to really have trust in the system. And as we have built out the discovery capabilities across multiple third-party AI systems out there, any kind of in-house build AI agents, you have one place to monitor, manage, including cost, but also really have the ability to kill any agents which should not be going and doing something which they're not allowed to. 
So it's become a very strong part of a governance layer, but also the runtime layer. And this is where the difference comes in. So it's coming in first before AI goes in production. And the volume of usage just starts going up because as you start building out more AI as you get confidence, we are really helping them manage it. It's not about orchestration really. It's really the visibility, the control and the safety. And then we can orchestrate many things underneath the covers depending on what our systems customers might be using.
So this really upfront first investment customers are doing and unlocking a lot of value for us going forward. And it's built on our core competence we had with CMDB and the asset management and the introducing ability to do any kind of physical assets as well as physical AI and nonhuman identity in one place. So it really resonates and works very well for our customers if they want to really scale AI.

**William McDermott** (Executives):
And if it helps you, an example might be think about AI adoption, unifying IT, audit, legal, risk and this single governance framework that Amit is discussing. Accenture has over 800,000 employees, I believe. And every single corporate function now is running on ServiceNow. So they use the Control Tower to govern nearly 900 ServiceNow native AI assets, and they measure the business outcomes across all of their departments. And what it's done for them is, like it's done for us, a substantial increase in productivity across the enterprise as they scale agentic AI.
I can also tell you about a global tech leader that's basically using the Super Intelligence Control Tower and their driver was Armis and Veza because they wanted to manage the identities of obviously, the people and the agents. But at the same time, they wanted to secure the operating technology environment of the company, networks, devices, critical infrastructure and so forth, and lower their cost to serve, drive their productivity and remediate things at machine speed. That's going to be a consistent theme that you're going to hear. And when you think about it, this particular company had about 80 different security tools, and that's pretty dangerous.
And I use Nestle as an example in my remarks, but they've expanded their footprint of ServiceNow through the prism of the Super Intelligence Control Tower, and they're running their governance across a very complex large global corporation and all of their operations are governed by the Super Intelligence Control Tower, and we're just getting started with them. So there's just so much in front of us, so much bandwidth that we bring to the customer. And the word is out there now. We're ready to roll.

**Amit Zavery** (Executives):
I'll just add one thing, sorry, Bill. The idea that we can discover, but also the SecOps products we have built for many years, you're combining this ability to discover, preempt any kind of issues as well as proactively remediate in one platform. And that's when you combine this control tower with what we do in SecOps, Veza and Armis, suddenly you have a platform which completely has visibility, but also the ability to save you if something goes wrong.

**Operator** (Operator):
Your next question comes from the line of Michael Turrin from Wells Fargo.

**Michael Turrin** (Analysts):
Bill, given it's early November, I'd just be curious to hear how you characterize the tone of overall IT budget discussions you're hearing, how ServiceNow specifically is positioned where Armis and some of the agentic offerings we're talking about fit and just how that impacts where you focus the company, both into end of year and towards a successful '27.

**William McDermott** (Executives):
Yes. Thank you very much for the question, Michael. Yes, I feel really great. The most important thing is strategic relevance. And that's what we have. We have a system of record that has been trusted for a couple of decades and the net new innovation from ServiceNow is truly breathtaking. 
And what I see is solutions that don't matter or point solutions, they will get eliminated, while strategically relevant platforms will not only do well, they'll do a lot better, especially if they're relevant in this era of super intelligence. So we are seeing our pipelines grow extremely well. The Super Intelligence Control Tower, Veza, Armis, Moveworks. I mean, in three quarters, you created $100 million in ACV. All these businesses are way ahead of what we had anticipated when we brought them into the family. So too is Logik.ai. So what you're seeing is we're building lots of innovation, thanks to our great innovation machine led by Amit. We made the right strategic choices to complement what we were building and our customers really love it.
So our biggest opportunity right now is to get out there in front of the customer and make sure they understand because they're getting hit from all angles. But the one angle that is consistent everywhere is they want ROI now. And we're past the proof-of-concept phase. We're past experimentation phase, and we're past point solution or vibe coding or do-it-yourself phase. We're now in serious enterprise phase where it's all about get the job done, deliver real value. And this platform is one of a few that will do extraordinarily well now and in the future.

**Operator** (Operator):
We have time for one more question. Your last question comes from the line of Mike Cikos at Needham.

**Matthew Calitri** (Analysts):
This is Matt Calitri on for Mike Cikos over at Needham. We wanted to ask on Action Fabric monetization, particularly with the OpenAI like partnership expansion announcement that came out with earnings tonight. What sort of spread are you seeing between early adopters that are moving with EmployeeWorks versus using external agents? And what are the monetization implications of this?

**Amit Zavery** (Executives):
Sure, Matt. So I think our view always has been that we provide customer choice. Customers should be able to use whatever tools they want to access capabilities in ServiceNow and be able to do actioning, which is where we have really great differentiator and capabilities. So with Action Fabric, what we've allowed customers to do is to go through MCP and A2A kind of interactions and build any interface they want. 
What we're doing with OpenAI is allowing ChatGPT as a way to interface into ServiceNow. But all of the work happens inside ServiceNow, it's just a call coming from ChatGPT. And then the work which we were doing typically through our user experience now happens through this interface, and we get full value for it from the monetization perspective because you're burning down assists for every work you'd ask ServiceNow to do. And that work is not able to be done anywhere else because we have the context, we have the ability to understand what you're trying to do and all the connectivity to all the third-party systems as well as the workflows, which are running already inside ServiceNow for any enterprise customers.
So we're just opening up the ability for any ways to access ServiceNow, and we get an opportunity to monetize this much more than we typically would have done by just providing our own interface. Of course, EmployeeWorks is also another option for customers to use, but the EmployeeWorks provide a lot more capabilities than ChatGPT can provide or Gemini Enterprise can provide because they're just a calling part of it. What we do with EmployeeWorks, we are doing a lot of the reasoning, the orchestration, the planning as well as providing specialized agents, which gives you, again, as an employee, a lot more capability than you would get typically from other third-party front doors.
So there's a lot of differentiation built in, in EmployeeWorks. But again, we do want allowing customers to use Action Fabric in another way to interface and still get value out of ServiceNow investment they made, and we continue to monetize, so we get ability to really grow our revenue through many, many mechanisms now. As the partnership with OpenAI is great. I mean I think there's a lot of capabilities we'll deliver with them from a skills perspective, but they're depending on us to really do the work, and that's where the value gets created.

**William McDermott** (Executives):
And if you think about it, as Amit said, ServiceNow basically is the execution layer. And I believe we're the execution layer for the entire AI economy. And if you look at what's happening with the partnerships we announced today and many more to come, it's not just where the work gets done, but it's where every human and every agent in the enterprise is coming to get things done. And that's a large market. We're positioned at the center of it. And if you say, well, how should we know? Just keep in mind that Action Fabric has seen a 500% growth in assists in less than 30 days. So it's multiplying so, so quickly. And I think this represents a business model innovation that will be substantially larger in a very short period of time than the entirety of ServiceNow is today.

**Operator** (Operator):
We have reached the end of the Q&A session, and this concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NOW_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜CFO｜guidance：Q3 訂閱營收財測區間（原話："we expect subscription revenues between $3.975 billion and"）
- 2026-07-22｜CFO｜guidance：Q3 cRPO 成長財測 20%（固定匯率）（原話："We expect cRPO growth of 20% on a constant"）
- 2026-07-22｜CFO｜guidance：Q3 營業利益率財測 31%（原話："We expect operating margin of 31%"）
- 2026-07-22｜CFO｜guidance：全年訂閱營收財測中點上調 1,500 萬美元（原話："we're raising our subscription revenues by $15 million"）
- 2026-07-22｜CFO｜guidance：全年營業利益率財測 31.5%（原話："We expect operating margin of 31.5% and free cash"）
- 2026-07-22｜CFO｜margin：全年訂閱毛利率財測 81%（原話："subscription gross margin of 81%"）
- 2026-07-22｜CFO｜margin：Q2 非 GAAP 營業利益率 29.5%，高於財測 300bp（原話："Non-GAAP operating margin was 29.5%, 300 basis points above"）
- 2026-07-22｜CFO｜margin：管理層說明 Q2 利益率超標原因含行銷支出時點（原話："timing of spend, primarily in marketing"）
- 2026-07-22｜CFO｜margin：毛利率短期承壓原因：hyperscaler 與 AI 消耗；營業利益率持平（原話："both good reasons for a little bit of short-term pressure"）
- 2026-07-22｜CFO｜margin：毛利率承壓下營業利益率持平（原話："even though we had a little pressure on gross margin,"）
- 2026-07-22｜Amit Zavery｜margin：管理層稱不擔心 token 使用對利益率的影響（原話："we are not really worried about the margin impact"）
- 2026-07-22｜CFO｜guidance：Q2 超標部分來自聯邦在地部署營收由 Q3 提前（原話："Part of that outperformance was due to strong U.S. federal"）
- 2026-07-22｜CFO｜guidance：CFO 稱 Q3 與全年財測有信心（原話："I'm very confident in our Q3 and full year"）
- 2026-07-22｜CFO｜guidance：CFO 說明約一半超標為 on-prem 提前認列（原話："a pull forward of on-prem for a quarter, right?"）
- 2026-07-22｜CFO｜guidance：CFO 說明全年上調對應淨新增 ACV 超標部分（原話："we passed along all of the net new ACV overachievement"）
- 2026-07-22｜CFO｜guidance：CFO 表示下半年財測採審慎（原話："being prudent for back half as most would expect"）
- 2026-07-22｜CFO｜guidance：CFO 稱採保守審慎財測（原話："at a conservative prudent guide, right?"）
- 2026-07-22｜CEO｜commitment：McDermott 承諾 2026 年底人數回到收購前水準（原話："exact same headcount before we did the acquisitions"）
- 2026-07-22｜CEO｜commitment：管理層重申 2030 年營收目標 320 億美元（原話："we set a course to $32 billion in revenue in 2030"）
- 2026-07-22｜CFO｜commitment：CFO 重申 2030 年 Rule of 60 路徑（原話："well on our way to the Rule of 60 by 2030"）
- 2026-07-22｜CEO｜commitment：AI ACV 目標 15 億美元（2026 年底）（原話："target of $1.5 billion ACV by the end of 2026."）
- 2026-07-22｜CFO｜commitment：AI 占 ACV 30%（2030）目標，稱追蹤領先（原話："we're already tracking ahead of our target for AI to reach"）
- 2026-07-22｜CEO｜product：ServiceNow AI ACV 突破 10 億美元（原話："surpassing $1 billion, keeping us on track to beat our"）
- 2026-07-22｜CFO｜product：新 AI 原生 SKU 升級帶來價格提升 20%-30%（原話："our new AI native SKUs are driving price uplift in"）
- 2026-07-22｜CFO｜product：Pro Plus SKU 價格提升（原話："Our pricing uplift for our Pro Plus SKUs continues to"）
- 2026-07-22｜Amit Zavery｜product：L1 AI 專員客戶使用成果（原話："close to 80% to 85% of the service requests"）
- 2026-07-22｜Amit Zavery｜product：AI Control Tower 客戶數（原話："more than 500-plus customers already live"）
- 2026-07-22｜CEO｜product：預告新的 AI 原生產品與商業模式（原話："a business model evolution that expands our TAM"）
- 2026-07-22｜CEO｜product：新產品形態：對話式服務台（原話："a conversational service desk experience, no tickets"）
- 2026-07-22｜CEO｜product：新產品鎖定客群（原話："we're targeting the Fortune 500,000"）
- 2026-07-22｜Amit Zavery｜product：混合定價結構（授權加用量）（原話："where it's a combination of license and usage"）
- 2026-07-22｜Amit Zavery｜competition：管理層稱競爭對手與 LLM 無法取得其情境資料（原話："our competitors don't get access to it"）
- 2026-07-22｜CEO｜competition：管理層稱 seat 壓縮不是問題（原話："we worried about seat compression? Not at all."）
- 2026-07-22｜CEO｜competition：新增業務中非 seat 計價占比（原話："our net new business is already non-seat-based."）
- 2026-07-22｜CEO｜competition：管理層稱自建成本遠高於採用其平台（原話："it will cost 5 to 10x to build an agent versus run one"）
- 2026-07-22｜CEO｜competition：管理層談資安排名與目標（原話："move up the leaderboard from a #8 company to"）
- 2026-07-22｜CEO｜competition：管理層將 Mythos 事件定位為對公司有利（原話："Mythos was a gift to the"）
- 2026-07-22｜Amit Zavery｜competition：管理層稱 LLM 商品化（原話："There is no reason for using some of these most expensive"）
- 2026-07-22｜CEO｜risk：被問銷售週期是否受影響，管理層答無（原話："I have not. In fact, the key here, Gregg,"）
- 2026-07-22｜CEO｜risk：合約年限拉長（原話："they're actually elongating, and you see that in the cRPO"）
- 2026-07-22｜CFO｜customer：Q2 續約率 98%（原話："Our renewal rate was a best-in-class 98% in Q2"）
- 2026-07-22｜CFO｜customer：年 ACV 逾 500 萬美元客戶數（原話："658 customers generating over $5 million in ACV"）
- 2026-07-22｜CEO｜customer：Q2 百萬美元以上淨新增 ACV 交易數（原話："We had 123 deals greater than $1 million in net new ACV"）
- 2026-07-22｜CFO｜customer：RPO 與 cRPO 口徑（原話："approximately $29 billion, representing 22% year-over-year"）
- 2026-07-22｜CEO｜customer：Experian 五年期合約（原話："In a 5-year deal and many deals are going longer"）
- 2026-07-22｜CEO｜customer：Maybank 五年期合約（原話："another 5-year deal, so much for deal shortening, right?"）
- 2026-07-22｜CFO｜capital_allocation：銷售人力增加的原因含併購（原話："So it's all three."）
- 2026-07-22｜CFO｜capital_allocation：管理層預期下半年銷售人力續增（原話："As you would expect, you'll see more sales heads as a"）
- 2026-07-22｜CEO｜capital_allocation：管理層談去年底收購遭批評（原話："took some criticism for"）

### NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md
- 2026-05-04｜William McDermott｜guidance：CEO 表示 2030 年前訂閱營收承諾為 300 億美元以上。（原話："a sub revenue $30 billion plus commit between now and 2030"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 表示以目前動能，2030 年訂閱營收可達 2026 年 150 億目標的兩倍。（原話："Our momentum puts us on pace to double that target in 2030."）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 另給出較高情境：自 2026 年財測起算的 CAGR 逾 20%，2030 年訂閱營收 320 億美元；並說明不要求投資人現在就以此估值。（原話："$32 billion of subscription revenue in 2030"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明三大成長動能（資安、資料、AI）合計 2030 年前年成長率超過 25%。（原話："these three vectors compound at over 25% growth"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 表示長期目標已內含較成熟產品成長放緩的假設。（原話："this does prudently bake in a deceleration"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 將 2026 年 AI ACV 目標由 10 億美元調升至 15 億美元。（原話："we're raising our 2026 AI ACV target from $1"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 設定 2030 年 AI 產品占 ACV 比重 30% 的目標。（原話："by 2030, we expect 30% of our ACV from ServiceNow AI"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 預告 2027 年恢復正常化利潤率擴張（含 Armis）。（原話："return to normalized margin expansion in 2027"）
- 2026-05-04｜Gina Mastantuono｜commitment：CFO 承諾 2027 年 non-GAAP 營業利益率與自由現金流利潤率各擴張 100 bps（同段話口徑含 Armis）。（原話："100 basis points of free cash flow margin expansion"）
- 2026-05-04｜Gina Mastantuono｜commitment：CFO 宣布股票薪酬占營收低於 10% 的時間點為 2029 年。（原話："Today we'll tell you when, 2029."）
- 2026-05-04｜Gina Mastantuono｜commitment：CFO 表示 2030 年達成 Rule of 60+（營收成長加自由現金流利潤率）。（原話："achieving the Rule of 60+ by 2030."）
- 2026-05-04｜William McDermott｜margin：CEO 說明目前成長率加自由現金流利潤率合計 56，目標 60 以上。（原話："Right now, it's 56, it's going to 60-plus"）
- 2026-05-04｜William McDermott｜commitment：CEO 提出 AI 上線 100 天內的滿意度保證，並說明次日 Knowledge 大會會正式推出。（原話："A total satisfaction guarantee on AI go-lives"）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 說明 AI 推理僅占服務成本不到 10%，用以回應推理成本壓縮毛利率的疑慮。（原話："AI reasoning is less than 10% of our cost to serve."）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 表示訂閱毛利率將維持 80% 以上，同時承認轉向超大型雲端業者短期壓抑毛利率。（原話："our move to hyperscalers is impacting gross margins"）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 說明 2026 年自身導入代理式 AI 的年化成本節省口徑：2026 年新增 2 億、2025 年 1 億，合計 3 億美元。（原話："$300 million in expected annualized cost savings"）
- 2026-05-04｜William McDermott｜margin：CEO 表示今年年底員工人數將與年初相同。（原話："leave this year with the exact headcount that we"）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 說明 AI ACV 的計算口徑：只計增量，基本訂閱不算入。（原話："We are only counting that incremental."）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 補充 AI 營收口徑：不像部分同業把全部營收都算成 AI。（原話："we're not counting every single dollar of revenue as AI"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明新 AI 原生封裝下，客戶購買較高階套裝的平均價格提升幅度。（原話："we expect to see an average price lift of 20% to 30%"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 回答 Prime 滲透速度：模型內建與 Pro 相近的保守爬坡，實際略快。（原話："building in a similar ramp with our AI that we had with Pro."）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明 Prime 定價與 Pro Plus 相同，漲價來自低階客戶往上升級。（原話："we're not increasing pricing in our most"）
- 2026-05-04｜Gina Mastantuono｜product：CFO 揭露 Now Assist ACV 於 Q1 突破 7.5 億美元。（原話："momentum carried into Q1 with ACV crossing $750 million"）
- 2026-05-04｜Jon Sigler｜product：產品長表示 Action Fabric 讓外部 AI 代理呼叫平台時消耗 Assist 額度而計費。（原話："the flywheel is going to spin faster"）
- 2026-05-04｜Jon Sigler｜product：Sigler 說明 Now Assist 目前規模與年底預期。（原話："This will be $1.5 billion by the end of the year."）
- 2026-05-04｜Amit Zavery｜product：Amit 表示 CRM 業務 ACV 將突破 20 億美元。（原話："which will help our CRM business cross $2 billion in ACV"）
- 2026-05-04｜Gina Mastantuono｜product：CFO 揭露 2025 年資安與風險新增 ACV 成長 40%。（原話："net new ACV grew 40% year-on-year"）
- 2026-05-04｜Amit Zavery｜product：Amit 表示資料分析產品線預計成為十億美元事業。（原話："data analytics is on track to be a billion-dollar business"）
- 2026-05-04｜Pat Casey｜product：Pat Casey 說明首個自主 AI 員工（L1 服務台）目前的試點客戶數。（原話："I've got 6 live pilot customers"）
- 2026-05-04｜Amit Zavery｜product：Amit 說明為中型市場打造的 AI 原生服務管理產品，採純消耗型計價。（原話："entirely consumption-based and conversation first"）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 說明 2025 年更新的既有 Now Assist 客戶 ACV 平均擴張幅度。（原話："their ACV by an average of over 3x"）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 揭露 2025 年新增 ACV 中來自五個以上產品交易的占比。（原話："91% of our net new ACV came from deals with 5 or more"）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 以 20 人客服團隊為例，說明客戶總成本與 ServiceNow 支出的變化。（原話："ServiceNow spend grows over 5x."）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 推算 IT 事件管理一個用例的 ACV 機會，假設 75% 事件由自主勞動力處理。（原話："can be processed by an autonomous workforce"）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 說明客戶 AI 旅程第五年預計支出為起始 Assist 授權量的倍數。（原話："this AI customer would be spending 4.5x the initial Assist"）
- 2026-05-04｜Bhavin Shah｜customer：Bhavin Shah 說明 Moveworks 整合後的管線成長。（原話："we've seen a 10x pipeline build"）
- 2026-05-04｜Gina Mastantuono｜capital_allocation：CFO 說明 2026 年 Q1 的 ASR 規模。（原話："In Q1 alone, the $2 billion ASR"）
- 2026-05-04｜Gina Mastantuono｜capital_allocation：CFO 預期 2026 年稀釋淨中性，並說明剩餘買回額度。（原話："We expect to be dilution net neutral for 2026."）
- 2026-05-04｜Gina Mastantuono｜capital_allocation：CFO 列出剩餘買回授權額度。（原話："$4.2 billion in authorization remaining"）
- 2026-05-04｜Gina Mastantuono｜capital_allocation：CFO 表述資本配置第二順位：以開拓新 TAM 或加速產品路線圖的小型併購為主。（原話："with a focus on tuck-ins that open new TAMs"）
- 2026-05-04｜William McDermott｜capital_allocation：CEO 表示 300 億與 320 億的長期目標未納入大型併購。（原話："we did not put large-scale M&A in there."）
- 2026-05-04｜William McDermott｜capital_allocation：CEO 為 Moveworks、Veza、Armis 的收購辯護，稱非為買營收成長。（原話："We were buying a ticket to a bright future."）
- 2026-05-04｜Paul Fipps｜competition：Paul Fipps 回應同業稱搶走份額的說法。（原話："We just don't see them in the competitive stack."）
- 2026-05-04｜William McDermott｜competition：CEO 對同業言論表達不滿。（原話："we're getting a little annoyed"）
- 2026-05-04｜Amit Zavery｜competition：Amit 主張企業市場沒有能同時提供平台、資料、資安與自主勞動力的競爭者。（原話："In the enterprise space, there's nobody like us."）
- 2026-05-04｜Amit Zavery｜competition：Amit 引用 Gartner 預測，用於主張未受治理的 AI 專案會失敗。（原話："40% of agenetic AI projects will fail by 2027"）
- 2026-05-04｜Amit Zavery｜competition：Amit 針對自建對購買主張，稱自建 LLM 方案成本更高。（原話："customers building their own LLM-based solution"）
- 2026-05-04｜Gina Mastantuono｜competition：CFO 回應 AI 取代平台、座位壓縮的疑慮，定位為單一類別。（原話："we are in a category of one"）
- 2026-05-04｜William McDermott｜competition：CEO 表示將平台下沉至中型市場。（原話："take a platform down market a bit"）
- 2026-05-04｜Gina Mastantuono｜risk：CFO 點名市場疑慮之一：座位壓縮是否侵蝕營收。（原話："Will seat compression shrink revenue?"）
- 2026-05-04｜William McDermott｜risk：CEO 說明活躍使用者數未下降，作為座位壓縮疑慮的回應。（原話："our active users aren't going down because we go east"）
- 2026-05-04｜William McDermott｜risk：CEO 提到客戶對模型 token 化計價造成預算超支感到意外。（原話："surprised on the tokenization of models"）
- 2026-05-04｜Bhavin Shah｜risk：Bhavin Shah 承認並非所有流程都會立即代理化。（原話："not everything will be agentified immediately."）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明非座位計價占新增 ACV 的比重。（原話："half of our net new ACV has already shifted"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 回答非座位占比長期走向：預期持續上升但不會到 100%。（原話："I don't think it'll ever be 100%."）
- 2026-05-04｜Amit Zavery｜product：Amit 宣稱座位制計價無法反映 AI 價值，公司已轉向混合計價。（原話："seat-based pricing does not reflect the value of AI"）
- 2026-05-04｜Amit Zavery｜product：Amit 揭露混合與消耗型計量在過去一年新增業務中的占比。（原話："hybrid and consumptive meters accounted for more than"）
- 2026-05-04｜Gina Mastantuono｜commitment：CFO 回答兩種 2030 情境差異：因市場不確定而給區間，對 320 億有高度信心。（原話："prudent to give a range in not just one number"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明 2026 年財測高於 155 億美元，並稱有機超越 2021 年所訂 150 億目標 5 億美元。（原話："I know the guide is higher than $15.5 billion."）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 揭露來自公有雲夥伴的新增 ACV 成長。（原話："net new ACV from public cloud partners nearly tripled"）

### 問答異常語氣（迴避／改口／保留）
- NOW_Q2_2026_Earnings_Call_20260722.md｜問：Gabriela Borges 問 L1 ITSM 產品週期中客戶加碼支出的幅度｜答法：Zavery 與 Mastantuono 回以處理率、AI ACV 總量與 30% 目標，未給客戶加碼支出數字
- NOW_Q2_2026_Earnings_Call_20260722.md｜問：Michael Turrin 問 Q3 財測是否因聯邦遞延影響而偏審慎｜答法：Mastantuono 回稱管線良好；McDermott 轉談資安，未直接回答 Q3 財測審慎程度
- NOW_Q2_2026_Earnings_Call_20260722.md｜問：Brad Zelnick 問 AI 消耗與 token 價格對毛利率的上下行風險｜答法：Mastantuono 與 Zavery 談中期壓力減輕與模型組合，未提供毛利率量化區間
- NOW_Q2_2026_Earnings_Call_20260722.md｜問：Tyler Radke 問全年上調幅度相對 Q2 超標偏小的原因｜答法：Mastantuono 稱約半數為 on-prem 提前，並稱下半年審慎，同時說仍有上行空間
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：Zukin（Wolfe）問：同業說正在搶 ServiceNow 份額，競爭格局與資安如何推高目標。｜答法：Fipps 未給份額或贏率數字，稱同業在其競爭名單中看不到；McDermott 另以情緒語氣（'getting a little annoyed'）回應，未提供量化資料。
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：Weiss（Morgan Stanley）問：開放平台讓第三方代理接入時，相對自家自主員工 5 倍提升的增量是多少。｜答法：Gina 只回答第一題 Prime 爬坡；Amit 回答開放架構與計量機制，未提供第三方代理的增量倍數或金額。
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：Bhatia（William Blair）問：何時多數營收（非僅新增 ACV）會轉為消耗型／非座位制。｜答法：Gina 稱未給時間表，只說 50% 會續升但不會到 100%。
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：未具名分析師問：30% AI ACV 隱含非 AI 部分 CAGR 約 10% 以下，這是否令人擔憂。｜答法：Gina 稱這樣想是 '100% the wrong way'，改談 AI 拉動核心與 Pro 先例，未給非 AI 部分的成長數字。
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：Samana（Jefferies）問：30% AI ACV（約 90 億美元）中，現有產品與路線圖各占多少。｜答法：Gina 只回答定價與滲透假設，未拆分現有產品與路線圖的貢獻。

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
{"date":"20260723","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"工作流治理護城河（CMDB + Context Engine + agent 治理）抵禦 agentic 侵蝕，ITSM 份額不流失、有機成長守住中位數以上"},{"id":"H2","text":"消費/非座位計量新價格模型（Foundation/Advanced/Prime，>50% 新 ACV 非座位）驅動 AI 變現、抵銷座位去化——且 AI ACV 淨於 Gartner 40% 取消率後仍複利"},{"id":"H3","text":"19x 的品類 de-rating 已過度；但裁決不靠 re-rate——在 19x 上 EPS 自身複利即 carry return，倍數維持平至微降亦達標，re-rate 到 25-30x 是選擇權非論點"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"有機成長結構性減速：headline cRPO 21.5% 中 ~125bps 為 Armis 無機（MS 拆分），有機 ~17%；UBS 預測 EOY26 降至 16%；estimate-cut treadmill 使「便宜」因 E 還在被下修"},{"id":"R2","text":"agentic-workflow 新預算之爭（非古典 ITSM 座位）：Salesforce Agentforce（Benioff 稱其 IT 版為「ServiceNow killer」）/ Microsoft Copilot・Agent 365 / AI-native（Sierra $15.8B、Decagon $4.5B）競逐 NOW 尚未捕獲的增量 agentic 預算；CRM/ITSM/ERP 邊界溶解"},{"id":"R3","text":"三條獨立慢變數：(a) agentic 架構性繞過工作流層（⛔ 級，§3.F）；(b) 座位重定價在 2027-28 續約潮向下侵蝕 NRR（renewal 為滯後）；(c) 聯邦/公部門 15-17% 營收＋DOGE 2026 剪支＋兩次政府停擺（1/31-2/3、2/14-4/30）——惟 Q2 聯邦反而強（部分為 on-prem 時點前移）"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼＝站回 W104($164) 或有機 cRPO cc ≥18% 連 2 季；減碼＝有機 cRPO <16%（UBS 路徑）連 2 季或 AI ACV 淨增轉負","irr_base_pct":11.2,"ev5y_pct":70.5,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟢","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.7,"ev5y_pct":70.5,"irr_base_pct":11.2,"max_dd_pct":-40.0,"bull_5y_price":265.0,"bear_5y_price":68.0,"p_bull_pct":28.0,"p_bear_pct":30.0,"rearm_trigger":"加碼＝站回 W104($164) 或有機 cRPO cc ≥18% 連 2 季；減碼＝有機 cRPO <16%（UBS 路徑）連 2 季或 AI ACV 淨增轉負","price_at_dd":95.46,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
