你是 stock-analyst **v20 判斷 agent**，標的 SNDK（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SNDK","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":11031,"period":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results"},"note":"consensus 約 $10.7B（來源：Investing.com Q1 FY27 slides 報導，非 IR）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":8871,"period":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","unit":"USD M；margin 80.4%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":8780,"period":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","unit":"USD M；margin 79.6%（8,780÷11,031，自算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results"}},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":6309,"period":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","unit":"USD M；占營收 57.2%（自算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results"}},{"id":"f_kpi5_guidance_q2_fy2027_reven","label":"Guidance Q2 FY2027 revenue","value":"12,200–12,600","period":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results"},"note":"Non-GAAP EPS Q1 實際 $49.51 vs consensus $47.15（Investing.com）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_sndk_gross_margin_pct","label":"SNDK 毛利率","value":76.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_sndk_operating_margin_pct","label":"SNDK 營業利益率","value":68.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_sndk_fcf_margin_pct","label":"SNDK FCF 利潤率","value":61.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_wdc_gross_margin_pct","label":"WDC 毛利率","value":52.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_wdc_operating_margin_pct","label":"WDC 營業利益率","value":40.69,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_wdc_fcf_margin_pct","label":"WDC FCF 利潤率","value":29.62,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mu_gross_margin_pct","label":"MU 毛利率","value":80.72,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_mu_operating_margin_pct","label":"MU 營業利益率","value":74.59,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_mu_fcf_margin_pct","label":"MU FCF 利潤率","value":44.27,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_000660_ks_gross_margin_pct","label":"000660.KS 毛利率","value":76.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_operating_margin_pct","label":"000660.KS 營業利益率","value":68.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_fcf_margin_pct","label":"000660.KS FCF 利潤率","value":47.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_gross_margin_pct","label":"005930.KS 毛利率","value":57.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_operating_margin_pct","label":"005930.KS 營業利益率","value":36.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_fcf_margin_pct","label":"005930.KS FCF 利潤率","value":28.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":1.04,"period":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","unit":"%（SBC 91M ÷ GAAP 營業利益 8,780M，自算；占營收 0.83%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":1150.89,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-3.04,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":32.73,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":5.55,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（214.82 → 226.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":3.13,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（266.3 → 274.64）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（256.77 → 256.77）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":226.74,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":274.64,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":256.77,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":240.04,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 66.68 → 226.74（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":9.2,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.65,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝38.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":38.6,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.48,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝37.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":37.6,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":5.08,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 226.74，分子＝快照價 1150.89","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-5005.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 201.0、現金 5206.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":142.29,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":158754.41,"period":"2026-11-02","unit":"USD m","basis":"市值 163759.41 ＋ 淨負債 -5005.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":49379.2,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":60356.3,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.22,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 1150.89 / W52 1060.08 / W104 None / W250 None / W250 13週斜率 None%"},{"id":"f_ma_w52","label":"52 週均線","value":1060.08,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列名主要對手為 Kioxia、Micron、Samsung、SK Hynix、YMTC 等垂直整合供應商；風險因子稱競爭可能造成市占大幅下降","source":"SEC EDGAR 10-K FY2026 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"We compete with vertically-integrated suppliers such as Kioxia, Micron Technology, Inc., Samsung Electronics Co., Ltd., SK Hynix, Inc., Yangtze Memory Technologies Co., Ltd. and numerous smaller companies that assemble flash into products.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Counterpoint 2026 Q2 NAND 營收市占：Samsung 28%、SK hynix 19%、Micron 15%、Kioxia 14%、YMTC 14%、SanDisk 11%（較上季降 2pp）；YMTC 為快速上升的中國進入者（Q1 13%，較 2025Q1 的 8% 上升）","source":"Counterpoint Research / 搜尋摘要彙整（technews.tw 2026-09-07 報導）","url":"https://technews.tw/2026/09/07/global-nand-memory-market-share-quarterly/","excerpt":null,"as_of":"2026-09-07","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2026 10-K：前十大客戶占營收 44%（FY2025 40%、FY2024 41%），公司自述這些客戶有多家供應商可選；搜尋摘要稱無單一客戶占營收逾 10%。未查到特定最大客戶導入第二供應商或自製的公開報導。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"For 2026, 2025, and 2024, 44%, 40% and 41%, respectively, of our total revenue came from sales to our top ten customers. These customers have a variety of suppliers to choose from and therefore can make substantial demands on us","as_of":"2026-08-17","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026、FY2025、FY2024 皆無單一客戶占營收逾 10%；前 10 大客戶占營收 44%、40%、41%。","source":"SEC EDGAR｜Sandisk 10-K FY2026｜Item 8 Customer Concentration and Credit Risk","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"For 2026, 2025 and 2024, no single customer accounted for more than 10% of the Company’s net revenue. For 2026, 2025, and 2024, the Company’s top 10 customers accounted for 44%, 40% and 41% of the Company’s net revenue, respectively.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2026-07-03 應收帳款淨額 47 億美元，三家客戶分別占約 19%、12%、10%（前一年僅一家占 11%，淨額 11 億美元）；信用損失準備金不重大，一般不要求擔保品。","source":"SEC EDGAR｜Sandisk 10-K FY2026｜Item 8 Customer Concentration and Credit Risk","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"As of July 3, 2026, the Company had net accounts receivable of $4.7 billion and three customers accounted for approximately 19%, 12% and 10%, respectively, of the Company’s outstanding accounts receivable. As of June 27, 2025, the Company had net accounts receivable of $1.1 billion, and one customer accounted for 11% of the Company’s outstanding accounts receivable. Reserves for potential credit losses were not material as of each period end.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"TrendForce 2026年7月展望：2026年NAND供給缺口約4–5%，2027年供給成長將超過需求、缺口於2027下半年緩解；主因中國供應商新設備投產擴產與既有產線製程升級。","source":"TrendForce Press Center 2026-07-21","url":"https://www.trendforce.com/presscenter/news/20260721-13148.html","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"摘要指多家來源稱新晶圓廠有意義的量產不早於2027年底或2028年；並有來源稱Samsung與SK Hynix（合計>60% NAND供給）計畫進一步減產，供給紀律為反覆出現的主題。","source":"nand-research.com Memory & NAND Flash Crisis: May 2026 Update","url":"https://nand-research.com/memory-nand-flash-crisis-may-2026-update/","excerpt":null,"as_of":"2026-05-31","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Sandisk 2026年10月財報摘要：預期CY2027 NAND位元需求年增約40%，資料中心占比將超過55%；TrendForce預估AI資料中心占NAND需求2026年44%、2027年51%。","source":"Quartr Sandisk Q1 FY2027 earnings summary; TrendForce","url":"https://quartr.com/events/sandisk-sndk-q1-2027_F6lVAeGG","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Sandisk已簽八份「新商業模式」多年期協議，鎖定約940億美元未來營收；中文摘要稱FY2027逾50%產能已售、FY2028約三分之二已訂。","source":"Blocks & Files 2026-10-30; cnyes","url":"https://www.blocksandfiles.com/flash/2026/10/30/sandisks-flash-revenue-rocket-accelerates-some-more/5306734","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.H","moat_trend","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K Item 3 稱無重大法律程序（僅一般例行訴訟）。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"There are no material legal proceedings, other than ordinary routine litigation incidental to the Company, to which we or any of our subsidiaries is a party or of which any of our or our subsidiaries’ property is subject.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因子僅為一般性表述：可能涉及反壟斷訴訟及政府調查，非實際進行中的案件。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"From time to time, we may be involved in litigation, including antitrust and commercial matters, putative securities class action suits and other actions.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 揭露：國際銷售占淨營收 82%（FY2026），暴露於關稅與貿易法規風險。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"Our international sales, which include sales to foreign subsidiaries of U.S. companies but do not include sales to U.S. subsidiaries of foreign companies, represented 82%, 80% and 86% of our net revenue for 2026, 2025 and 2024, respectively.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"美國 Section 232 與 301 調查進行中，可能影響關稅；目前在美銷售的多數產品免關稅，若失去豁免或加稅將增加銷貨成本、壓縮毛利。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"Currently, the majority of our products sold in the U.S. are exempt from tariffs, but additional tariff increases, or the loss of applicable exemptions, would increase the cost of goods sold for our products sold in the U.S., which could negatively impact our margins and financial performance.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：供應商可能因關稅、配額、制裁、禁運等貿易限制而無法供貨，導致成本上升與交期拉長。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"Trade restrictions, including tariffs, quotas and embargoes, demand from other high-volume industries for materials or components used in our products, disruptions in supplier relationships or shortages in other components and materials used in our customers’ products could result in increased costs to us, longer lead times, or decreased demand for our products, which could negatively impact our business.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K：絕大部分快閃記憶體取自與 Kioxia 的 Flash Ventures 合資，合約條款限制 Sandisk 改變產出或另找貨源的能力","source":"Sandisk Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0002023554/000162828026057406/sndk-20260703.htm","excerpt":"substantially all of our flash-based memory be obtained from Flash Ventures","as_of":"2026-07-03","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K：幾乎所有產品在海外生產，地緣緊張、貿易戰可能衝擊需求、毛利與產能利用","source":"Sandisk Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0002023554/000162828026057406/sndk-20260703.htm","excerpt":"A large portion of our revenue is derived from our international operations, and substantially all of our products are produced overseas.","as_of":"2026-07-03","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Kioxia 與 Sandisk 將 Yokkaichi 合資協議延長五年至 2034 年底，Sandisk 付 Kioxia 11.65 億美元製造服務費","source":"TipRanks/The Fly","url":"https://il.tipranks.com/news/the-fly/2856516","excerpt":"Kioxia and Sandisk extended the Yokkaichi joint venture agreements by five years, to end-2034; the deal was due to expire on December 31, 2029, and Sandisk will pay Kioxia $1.165 billion for manufacturing services","as_of":"2026-01-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Digitimes 標題：2026-04-20 東北強震震央近 Kioxia 北上（Kitakami）NAND 廠，Sandisk 與群聯暫停報價；未見損害或產出影響的第二來源","source":"Digitimes semiconductors topic","url":"https://apps.digitimes.com/topic/semiconductors","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 營收 $20.25B（+175%）；Datacenter $5.15B（+437%，Q4 $2.98B）、Edge $12.16B（+195%，最大段）、Consumer +29% 主因價格；Q4 consumer 季減 32% 至 $556M","source":"Sandisk FY2026 10-K / Pulse2 coverage","url":"https://pulse2.com/sandisk-datacenter-revenue-more-than-doubles-sequentially-to-2-98-billion-as-consumer-sales-fall-32/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"TrendForce 2027 NAND 報告：企業 SSD 受 AI 需求推升、消費端 NAND 轉弱；供給緩解最早 2027 下半年","source":"TrendForce 2027 NAND: Enterprise SSD Soars, Consumer Stalls","url":"https://www.trendforce.com/research/download/RP260915MC","excerpt":null,"as_of":"2026-09-15","retrieved_at":"20261102","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"TrendForce 預測 3Q26 NAND 合約價 +10-15% QoQ（前一季 +70-75%），消費端價格容忍度到極限；Q1 2026 市占 Samsung 31.6%，Micron 13.9% 與 Sandisk 並列第四","source":"TrendForce news via secondary summaries","url":"https://www.trendforce.com/news/?p=53753","excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261102","affects":["moat_trend","valuation","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子載明：公司對產品的需求日益取決於 NAND 在 AI 基礎設施的使用，可能出現更有效率或減少每單位 AI 運算所需儲存量的新/替代技術，若大規模採用可能快速削弱公司技術的重要性與需求；新產品也可能替代現有產品使其過時。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"In particular, demand for our products depends increasingly on the use of NAND flash memory in AI infrastructure, and new or alternative technologies could emerge that perform these functions more efficiently or reduce the storage required per unit of AI compute. If adopted at scale, such technologies could rapidly reduce or eliminate the importance of, and demand for, our technology in the AI infrastructure.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Sandisk 與 SK hynix 於 2026-08 透過 OCP 發布 HBF 首版規格（最高 512GB、約 0.4–3.0 TB/s 等級），為 NAND 基產品而非外部替代；The Register 指第一代讀取頻寬 1.6 TB/s 低於 HBM4。","source":"Business Wire / The Register","url":"https://assets.theregister.com/2026/07/30/202619/","excerpt":"But where HBM uses DRAM, HBF aims to use NAND flash. Sandisk claims its first generation of high-bandwidth flash will supposedly achieve read bandwidths up to 1.6 TB/s [PDF], making it a bit faster than HBM3e but significantly slower than HBM4, which is already hitting 2.5 TB/s per 12-high stack.","as_of":"2026-07-30","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Samsung 與 Kioxia 推 XL-Flash/Z-NAND 等儲存級記憶體作為 HBM 較便宜替代，與 Sandisk 的 HBM+HBF 路線不同。","source":"TrendForce News","url":"https://www.trendforce.com/news/?p=61972","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 銷售對象為電腦廠/OEM、雲端服務商、經銷商與零售商，並對經銷零售提供有限價格保護；Datacenter 營收由 FY2025 $960M 升至 FY2026 $5,153M，Consumer 為 $2,935M（FY2025 $2,268M）","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"Revenue by end market: Datacenter $ 5,153 $ 960 $ 325 Edge 12,160 4,127 4,069 Consumer 2,935 2,268 2,269 Total revenue $ 20,248 $ 7,355 $ 6,663","as_of":"2026-08-17","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"搜尋摘要（彙整 SEC 文件）：Sandisk 於 FY2026 下半年起簽長約（New Business Models），多為多年期、固定加變動定價並有財務保證，公司預期將成為主要營運模式；此為搜尋工具轉述，未取得逐字原文","source":"Sandisk 10-Q FY2026（搜尋結果摘要）","url":"https://www.sec.gov/Archives/edgar/data/0002023554/000162828026068601/sndk-20261002.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"五份長約、Q3 三份最低合約營收約 $42B，涵蓋 FY2027 逾三分之一位元量","source":"Benzinga: Sandisk bets big on multi-year contracts","url":"https://cdn1.benzinga.com/markets/equities/26/05/52205851/sandisk-bets-big-on-multi-year-contracts-as-ai-chip-demand-booms","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-05 公司給 FQ1'27 指引：EPS $44–46、營收 $10.3B–10.8B，EPS 指引高於共識 $41.45；財報後盤後股價約跌 3%（Seeking Alpha 稱 mixed guidance）。","source":"Benzinga SNDK guidance／Seeking Alpha 'Sandisk slips as mixed guidance overshadows strong Q4 results'","url":"https://seekingalpha.com/news/4626048-sandisk-slips-as-mixed-guidance-overshadows-strong-q4-results","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-04-30 FQ4 指引營收 $7.75–8.25B、非 GAAP EPS $30–33，高於當時共識 EPS $21.76；實際 FQ4 營收約 $8.96B，EPS 約 $38.8–39.25，高於共識 $33.28。公司 2025-05 至 2026-08 六次指引中 5 次上修。","source":"Benzinga SNDK guidance","url":"https://kr.benzinga.com/quote/SNDK/guidance","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價分布極寬（FN2，as of 2026-10-26）：16 則評等、87.5% 偏多、12.5% 中性、無偏空；Susquehanna $3,250（07-23）、Evercore ISI $2,800（08-06）、Melius $2,350（05-18）、Wells Fargo $1,400（08-06）；FN2 未給單一平均目標價。","source":"FN2 SNDK Analyst Consensus","url":"https://fn2.ai/earnings/sndk/analysts","excerpt":null,"as_of":"2026-10-26","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat（2026-07-28）：26 位分析師中 18 買進、6 持有、2 強力買進，平均 12 個月目標價 $1,811.38。","source":"MarketBeat consensus recommendation of moderate buy 2026-07-28","url":"https://www.marketbeat.com/instant-alerts/sandisk-corporation-nasdaqsndk-receives-consensus-recommendation-of-moderate-buy-from-analysts-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill：FY2027 EPS 最新共識 221.23 USD（2026-10-24，32 位分析師），下一季營收預估 3 個月內上修 5.82%。","source":"Chartmill SNDK estimates","url":"https://www.chartmill.com/stock/quote/SNDK/estimates","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"FY2026 10-K Item 3：無重大法律程序，僅一般例行訴訟。","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"There are no material legal proceedings, other than ordinary routine litigation incidental to the Company, to which we or any of our subsidiaries is a party or of which any of our or our subsidiaries’ property is subject.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-03-25 子公司 Sandisk Technologies 以約 10 億美元私募認購南亞科約 3.9% 股權（策略性股權投資，非併購 SNDK）。","source":"SEC EDGAR 8-K Item 1.01 2026-03-25","url":"https://www.sec.gov/Archives/edgar/data/2023554/000119312526122705/d136592d8k.htm","excerpt":"the Company agreed to purchase approximately 139 million shares of Nanya common stock for an aggregate purchase price of approximately $1.0 billion, representing approximately 3.9% of Nanya’s outstanding common stock on a fully diluted basis following the Transaction.","as_of":"2026-03-25","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-29 董事會核准 8 比 1 正向股票分割，11/20 起以分割後交易。","source":"SEC EDGAR 8-K Item 8.01 2026-10-29","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026068243/sndk-20261029.htm","excerpt":"Sandisk Corporation (the “Company”) announced that its Board of Directors approved an eight-for-one forward stock split (the “Stock Split”) of its common stock, par value $0.01 per share","as_of":"2026-10-29","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"TrendForce：2026 因廠房空間有限且優先擴 DRAM，NAND 供給主要靠製程升級，預估供給短缺 4–5%；2027 因高層數遷移與新廠逐步爬坡，位元供給成長明顯高於 2026，供需預期 2027 下半年轉正、短缺緩解。","source":"TrendForce 研究報告 Global Memory Supply-Demand Divergence (RP260727PO) / iconnect007 轉載","url":"https://iconnect007.com/article/150870/nand-flash-supply-growth-to-outpace-demand-in-2027-easing-supply-constraints-in-2h27/150867/smt","excerpt":"Looking ahead to 2027, accelerated migration to higher-layer NAND products and the gradual ramp-up of new fabs are expected to drive significantly stronger bit supply growth than in 2026; the supply-demand balance is expected to turn positive in the second half of 2027, allowing supply constraints to gradually ease.","as_of":"2026-07-27","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Kioxia 採謹慎資本支出：FY2026–FY2028 年均約 ¥4,700 億（較 FY2025 增 66%），仍較 FY2023 高峰（¥5,104 億）低約 10%；支出集中在仍有無塵室空間的 Kitakami。","source":"TrendForce News 2026-06-18 Kioxia adopts cautious capex strategy despite NAND upcycle","url":"https://www.trendforce.com/news/2026/06/18/news-kioxia-adopts-cautious-capex-strategy-despite-nand-upcycle-reportedly-10-below-fy23-peak-key-concerns-in-focus/","excerpt":"Kioxia plans average annual capex of around ¥470 billion for FY2026–FY2028, up 66% from FY2025.","as_of":"2026-06-18","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"TrendForce 2025-11 預估 2026 NAND 資本支出約 $222 億 vs 2025 年 $211 億（約 +5%），Samsung 與 SK Hynix 限制 NAND 投資、轉向 HBM/DRAM。","source":"Evertiq / TrendForce 2025-11-13 memory industry to maintain cautious capex in 2026","url":"https://evertiq.com/news/2025-11-13-memory-industry-to-maintain-cautious-capex-in-2026","excerpt":null,"as_of":"2025-11-13","retrieved_at":"20261102","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Fab Tracker（2026-02）：Micron 新加坡 10B 已動工，2028 爬坡，產能大於 10A/X 兩倍以上；Micron 同時把 NAND 產能轉往 DRAM。","source":"Fab Tracker February 2026 (s29.q4cdn.com PDF)","url":"https://s29.q4cdn.com/619069826/files/doc_financials/2025/q4/Fab-Tracker-February-2026.pdf","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261102","affects":["thesis.R","triggers"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Kioxia 研議 Kitakami 新廠房，量產約 2029–2030 年後（次級來源，時程待核）。","source":"borecraft 2026-06-04 Kioxia weighs a new Kitakami fab for after 2030","url":"https://borecraft.com/2026/06/04/kioxia-weighs-a-new-kitakami-fab-for-after-2030/","excerpt":null,"as_of":"2026-06-04","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#5","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"海外 NAND 廠 2026–2027 受無塵室空間限制，新晶圓廠 2028 起集中投產，大規模 NAND 產能釋放要到 2029 後；近期增量主要來自中國（YMTC Fab 3、SK Hynix Dalian Fab 2）。","source":"36kr 轉載分析","url":"https://eu.36kr.com/en/p/4014344623198337","excerpt":"2026H2-2028 (dominated by Chinese capacity expansion): New fabs mainly come from YMTC (Fab 3) and SK Hynix (Dalian Fab 2).","as_of":"2026-10-07","retrieved_at":"20261102","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce 2026年10月NAND晶圓合約價停止上漲，MLC/TLC/QLC持平，市場進入高檔平台（搜尋摘要轉述，未核原文）","source":"TrendForce NAND Flash Wafer Contract Price Oct. 2026","url":"https://www.trendforce.com/research/download/RP261030YB","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["valuation","triggers","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"TrendForce 2026年2月稱供應商庫存偏低、PC OEM/手機品牌/模組廠庫存下降（搜尋摘要轉述，未核原文）","source":"TrendForce NAND Flash Market Bulletin - Feb. 11, 2026","url":"https://www.trendforce.com/research/download/RP260211TF","excerpt":null,"as_of":"2026-02-11","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"TrendForce 2026年5月公告稱供應商維持極低庫存（搜尋摘要轉述，未核原文）","source":"TrendForce NAND Flash Market Bulletin - May 20, 2026","url":"https://www.trendforce.com/research/download/RP260520ZD","excerpt":null,"as_of":"2026-05-20","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"TrendForce：模組廠庫存因消費需求疲弱、去化放慢而上升；其他買家庫存在可控範圍","source":"CTEE 工商時報","url":"https://www.ctee.com.tw/news/20260722700192-430501","excerpt":"目前NAND Flash原廠庫存水位偏低，模組廠則因消費市場疲弱、產品去化速度放緩，庫存有所上升，其他買方庫存仍處於可控範圍。 將工商時報加入Google偏好來源 相關新聞 《電週邊》光寶科邱森彬：四箭齊發 2027年營運樂觀 PC業務惡化超預期 英特爾崩28%、拖累AMD NAND Flash廠鎧俠純益估飆14倍、27年產能\"售罄\"","as_of":"2026-07-22","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#4","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce：2026年Q4 NAND合約價漲幅收斂、現貨價維持區間","source":"TrendForce eMMC/UFS note via search result","url":"https://tech-insider.org/nand-shortage-ssd-prices-2026/","excerpt":"Contract prices for NAND flash, the chip technology behind every SSD, USB drive and memory card on the planet, are set to climb another 15% to 20% quarter over quarter in the fourth quarter of 2026, according to market researcher TrendForce.","as_of":"2026-10-22","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"上一輪下行（WD 時期 flash 業務）FY2023 營收下滑約 38%、每 GB 平均售價降約 39%；毛利率由 FY2022 的 33.3% 降至 7.1%。","source":"Webull/Motley Fool: Sandisk's Sales Fell 38% in the Last Flash Memory Downturn","url":"https://www.webull.com/news/15734458362897408","excerpt":null,"as_of":"2025-10-20","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"TrendForce：NAND 4Q22 合約價下跌 20-25%，3Q22 晶圓合約價預估跌幅由 15-20% 上修至 30-35%；1Q23 跌幅收斂至約 10-15%，2Q23 預期 5-10%。","source":"TrendForce press center 2022-2023","url":"https://www.trendforce.com/presscenter/news/20230105-11526.html","excerpt":null,"as_of":"2023-01-05","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Micron 分析：記憶體前兩輪下行（2010-12、2014-16）以 EBITDA 毛利率衡量分別持續 7 與 9 季；另有評論稱 2021 高點至 2023 低點記憶體營收約降 40%，週期高點到高點約 3-5 年。","source":"Seeking Alpha: Micron: How Low Will It Go? / uncoveralpha: every memory cycle ends the same","url":"https://www.uncoveralpha.com/p/every-memory-cycle-ends-the-same","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-03-25 子公司以約 10 億美元認購南亞科約 3.9% 股權（對外策略投資，非 SNDK 被併購或併購他人）。","source":"SEC EDGAR 8-K Item 1.01 2026-03-25","url":"https://www.sec.gov/Archives/edgar/data/2023554/000119312526122705/d136592d8k.htm","excerpt":"the Company agreed to purchase approximately 139 million shares of Nanya common stock for an aggregate purchase price of approximately $1.0 billion, representing approximately 3.9% of Nanya’s outstanding common stock on a fully diluted basis following the Transaction.","as_of":"2026-03-25","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2026 10-K 經查無重大法律程序；搜尋僅見 2015 年舊 SanDisk 集體訴訟（已和解），非近12個月。","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm","excerpt":"There are no material legal proceedings, other than ordinary routine litigation incidental to the Company, to which we or any of our subsidiaries is a party or of which any of our or our subsidiaries’ property is subject.","as_of":"2026-08-17","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單中無 Item 4.02（財報不可信賴/重編）項目；清單共 11 份，主要為財報、董事異動、融資協議、股權投資與股票分割。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002023554&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 6 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 20 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SNDK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.84,"operating_margin_pct":68.43,"fcf_margin_pct":61.63,"rd_intensity_pct":5.64},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"WDC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.6,"operating_margin_pct":40.69,"fcf_margin_pct":29.62,"rd_intensity_pct":7.94},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MU","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":80.72,"operating_margin_pct":74.59,"fcf_margin_pct":44.27,"rd_intensity_pct":4.24},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU","as_of":"TTM ending 2026-08-31（4季加總）"}},{"name":"000660.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.27,"operating_margin_pct":68.04,"fcf_margin_pct":47.8,"rd_intensity_pct":4.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"005930.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.48,"operating_margin_pct":36.88,"fcf_margin_pct":28.95,"rd_intensity_pct":9.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"SNDK"},"financial_history":{"ticker":"SNDK","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":6086000000.0,"revenue_yoy_pct":null,"gross_margin_pct":7.07,"operating_margin_pct":-21.28,"net_income":-2143000000.0,"diluted_eps":-14.78,"free_cash_flow":-932000000.0,"fcf_margin_pct":-15.31,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":6663000000.0,"revenue_yoy_pct":9.48,"gross_margin_pct":16.09,"operating_margin_pct":-6.66,"net_income":-672000000.0,"diluted_eps":-4.63,"free_cash_flow":-475000000.0,"fcf_margin_pct":-7.13,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":7355000000.0,"revenue_yoy_pct":10.39,"gross_margin_pct":30.07,"operating_margin_pct":6.89,"net_income":-1641000000.0,"diluted_eps":-11.32,"free_cash_flow":-120000000.0,"fcf_margin_pct":-1.63,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":20248000000.0,"revenue_yoy_pct":175.3,"gross_margin_pct":71.47,"operating_margin_pct":61.58,"net_income":11433000000.0,"diluted_eps":73.76,"free_cash_flow":11494000000.0,"fcf_margin_pct":56.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SNDK/SNDK_Q1_2027_Earnings_Call_20261029.md）

# Q1 2027 Earnings Call
**Sandisk Corporation** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good afternoon, and welcome to Sandisk's First Quarter Fiscal Year 2027 Earnings Conference Call. [Operator Instructions] Please also note today's event is being recorded. 
At this time, I'd like to turn the floor over to Ivan Donaldson, Vice President of Investor Relations. Please go ahead.

**Ivan Donaldson** (Executives):
Before we begin, please note that today's discussion will contain forward-looking statements based on management's current assumptions and expectations, which are subject to various risks and uncertainties. These forward-looking statements include expectations for our technology and product portfolio, our business plans and performance, our capital allocation priorities, market trends and opportunities and our financial results. We assume no obligation to update these statements. Please refer to our annual report on Form 10-K and our other filings with the SEC for more information on the risks and uncertainties that could cause actual results to differ materially from expectations. 
We will also make references to non-GAAP financial measures today. Reconciliations between the non-GAAP and comparable GAAP financial measures are included in the written materials posted in the Investor Relations section of our website.
With that, I'll turn the call over to David.

**David V. Goeckeler** (Executives):
Thanks, Ivan. Good afternoon, and thank you for joining Sandisk's Fiscal First Quarter 2027 Earnings Call. We began fiscal year 2027 with another strong quarter, creating value for customers and shareholders and delivering results above guidance. Our strategy is working, and our execution is delivering strong results. Revenue for the quarter was $11 billion. Non-GAAP gross margin was 85.1% and non-GAAP earnings per share was $49.51. We generated $5.7 billion of adjusted free cash flow and returned $5 billion to shareholders through share repurchases.
Our confidence in the long-term trajectory of the business is grounded in 3 enduring strengths: technology leadership, deep customer partnerships and disciplined financial management. These strengths are reinforced by a structural increase in NAND demand, driven particularly by AI and by customer signals now extending beyond fiscal year 2030 through our new business models, our NBM partnerships. Together, they position us to invest with confidence in our technology road map, strengthen and expand our customer relationships, and deliver growing and durable free cash flow while returning capital to shareholders. 
It starts with our technology leadership. BiCS8 is the backbone of our current production portfolio and the industry benchmark for performance and density across TLC and QLC. BiCS8 introduced our CMOS Directly Bonded to Array, our CBA architecture, enabling the performance required by AI data center customers and establishing the framework for future generations. BiCS9 pairs the proven BiCS8 cell array with next-generation CMOS, significantly increasing interface performance while retaining a mature memory architecture. BiCS10 advances the full node architecture across both TLC and QLC with a 1-terabit TLC die designed for performance-intensive workloads and a 2-terabit QLC die, delivering industry-leading density and twice the read and write bandwidth of BiCS8. Together, these technologies will extend the BiCS8 foundation to meet the evolving performance and capacity requirements of next-generation infrastructure. 
Beyond the core road map, High Bandwidth Flash, or HBF, reached an important milestone in the fiscal first quarter with the tape-out of our first HBF memory die with fabrication now underway. As we outlined at Investor Day, HBF is a new memory architecture for inference that targets HBM class read bandwidth with substantially greater capacity to support larger models, longer context lengths and growing KV caches. It is designed to complement HBM by bringing NAND class capacity closer to the processor, and we remain on track to deliver samples of our first HBF-based products next calendar year. HBF remains a future innovation and is not included in the long-term financial model we introduced at Investor Day. As customer adoption, product requirements and manufacturing readiness become more clearly defined, we expect to provide further perspective on the market opportunity.
Customers recognize the strength of our innovation and increasingly view Sandisk as an important partner in achieving their growth objectives. Through our NBMs, we continue to evolve customer relationships into long-term partnerships grounded in innovation, collaboration and shared commitment. Our most recent customer engagements with the world's leading AI companies indicate further upside in demand for our technology. Our market-leading technology, product portfolio and customer partnerships are the backbone of our strong financial position, which allows us to reinvest to maintain our technology leadership and expand supply through R&D-focused CapEx.
Each of these strengths is reinforced by tailwinds from AI. The need for scalable memory and storage is expanding as inference workloads grow, making NAND increasingly integral to AI infrastructure. During inference, each generated token must reference the context that precedes it, creating a growing KV cache that serves as the model's working memory. Longer prompts, more complex reasoning, multimodal inputs and persistent user context materially increase these storage requirements. HBM and DRAM support the highest performance tier, while flash provides the capacity required to retain broader context efficiently and avoid costly recomputation. We believe this is a secular dynamic that is expanding NAND's role across the AI stack.
The memory hierarchy defines the role of each NAND architecture. TLC provides the lower latency, higher write performance and greater endurance required for active data sets, checkpointing and latency-sensitive KV cache workloads. In our AI lab comparison we presented at Investor Day, systems utilizing SSD delivered approximately 3x the token throughput while using approximately 75% less energy than comparable systems relying on volatile memory alone. QLC further increases storage density for capacity-intensive applications such as data lakes, vector databases that power AI search and retrieval repositories. 
Between these layers, a growing persistent context tier establishes data to be retained and recalled rather than regenerated. As inference costs decline, we expect the adoption and usage to expand, supporting our view that KV cache will represent approximately 1/3 of the AI data center flash market by the end of the decade and that the AI data center opportunity will approach the size of the NAND industry today. 
Turning to our end markets. In data center, our portfolio addresses the full range of AI infrastructure requirements from performance-intensive enterprise SSDs to high-capacity platforms. Demand remains strong and continues to grow, and we estimate that data center has expanded from approximately 20% of industry bits early in the decade to roughly half of the industry bits today. This structural shift in customer mix is reshaping industry economics and is central to the transformation underway at Sandisk. This quarter, data center again delivered strong growth and continued to outpace the broader market as we allocated more supply to address the growing demand from this end market.
Edge is a large and strategically important market for Sandisk, spanning smartphones, PCs, automotive, tablets and an expanding range of physical AI applications. Automotive is becoming an increasingly important growth vector in our Edge business and a meaningful long-term growth opportunity. We have deepening engagements with leading customers, reinforcing our confidence that automotive can become one of the largest markets within Edge over time.
Our Consumer business remains a differentiated strategic asset, combining direct brand engagement with hundreds of millions of end users and broad shelf presence across the world's leading channel partners. The consumer end market provides a durable foundation for our business, while its direct connection to the market informs product development and provides early insight into shifts in end-user demand. Taken together, these results reinforce the durability of the model we outlined at our Investor Day. We have established a strong level of profitability and cash generation, and our focus from here is consistent execution across the portfolio.
With that, I'll turn the call over to Luis for a detailed update on our business and outlook.

**Luis Visoso** (Executives):
Thank you, David. We're executing the strategies and plans that we outlined at Investor Day, and we're delivering attractive financial results. In the first quarter, we closed 2 NBMs. Because both deals closed before our fourth quarter earnings call, we announced these partnerships on that call. We're in active conversations with existing NBM customers that are evaluating extending existing agreements and with new customers that are evaluating new NBMs. These long-term partnerships provide greater visibility into demand and financial performance, supporting a more durable financial model.
We will remain patient and disciplined in selecting the right long-term partners as we define the optimal percentage of our bits that we allocate to NBMs, which is likely higher than our current levels.
Revenue for the first quarter was $11 billion, up 23% sequentially and 378% year-over-year. This compares favorably with our guidance range of $10.3 billion to $10.8 billion. Both volume growth and higher pricing contributed to revenue growth, with approximately 60% of the increase attributable to volume growth and 40% to higher pricing.
Data center revenue was $4.8 billion, up 61% sequentially, outpacing estimated market growth for the quarter.  Our leading products and strong customer partnerships, including 3 U.S. hyperscalers, underpin our continued expansion in this fast-growing end market. Edge revenue was $5.8 billion, up 7% sequentially, reflecting resilience in premium and mainstream markets, partially offset by contraction at the lower end. Within Edge, we saw strong growth with automotive and IoT customers. Consumer revenue was $397 million, down 29% sequentially as the market adjusts to higher pricing. We remain committed to serving all 3 end markets with a diversified portfolio that optimizes our performance over time. 
Non-GAAP gross margin for the first quarter was 85.1%, up from 84.6% in the prior quarter, driven by higher volumes and pricing. This compares favorably with our guidance range of 83% to 85%. Non-GAAP operating expenses were $513 million, representing 4.7% of revenue. Non-GAAP operating margin was 80.4% compared to 79.2% in the prior quarter. Non-GAAP EPS was $49.51, up from $39.25 in the prior quarter and $1.22 in the same quarter of the prior fiscal year. This compares favorably with our guidance range of $44 to $46. We closed the quarter with 154 million diluted shares outstanding. Key GAAP to non-GAAP reconciliation includes $91 million in stock-based compensation, representing 0.8% of revenue and $513 million gain on equity securities, primarily attributable to our investment in Nanya.
During the quarter, we repurchased approximately 3.2 million shares of our common stock for $5 billion. Over the past 2 quarters, we have repurchased 6 million shares, representing approximately 4% of our total shares outstanding. Our repurchases reflect our conviction in the long-term value of the business and our disciplined approach to capital allocation. We continue to invest appropriately in the business while returning 100% of excess cash to shareholders.
Moving on to free cash flow. Cash flow from operations was $6.4 billion. Gross capital expenditures totaled $378 million, representing 3.4% of revenue. We expect gross capital spending to increase during the balance of the year and represent mid-single-digit percentage of revenue for fiscal year 2027. During the quarter, we generated $5.7 billion in adjusted free cash flow, representing approximately 52% margin. We closed the quarter with $5.1 billion in cash and cash equivalents and no debt.
Moving on to guidance. Our confidence in the long-term health of the market is reinforced by the structural growth of the AI infrastructure and the expanding role of NAND across inference workloads. Before turning to our second quarter outlook, I will announce that the Sandisk Board of Directors has approved an 8-for-1 stock split of the company's common stock. The additional shares are expected to be distributed on November 19 and trading on a split-adjusted basis is expected to begin on November 20. 
For the second quarter of fiscal year 2027, we expect revenue between $12.2 billion and $12.6 billion. We expect non-GAAP gross margin between 84.5% and 85.5%, which includes modest like-for-like price increases. On a pre-split basis, we expect non-GAAP EPS between $55 and $57, assuming 151 million fully diluted shares. On an 8-for-1 split-adjusted basis, this equates to non-GAAP EPS between $6.88 and $7.13, assuming approximately 1,208 million fully diluted shares. For context, we expect a strong market in calendar year 2027. Data center is expected to be, again, the engine of growth and represent over 55% of the market with bit demand growing about 40% year-on-year, enabled by higher AI-driven capital spending. This is after more than doubling in 2026. Our NBM pipeline exceeds our supply throughout the end of the decade. 
With that, let me turn the call back to David.

**David V. Goeckeler** (Executives):
Thank you, Luis. We continue to execute on the strategy we outlined at Investor Day, reinforcing our confidence in Sandisk's long-term trajectory. Our technology leadership, deep customer partnership and disciplined financial management, supported by a structural increase in NAND demand driven by AI, position us to serve our customers, deliver growing and durable free cash flow and return capital to shareholders. Over the past year, we have transformed the earnings and cash generation power of the business and established a strong foundation for durable performance. We remain focused on disciplined execution, sustained value creation and delivering against our long-term financial objectives. 
With that, Ivan, let's open it up for questions.

**Operator** (Operator):
[Operator Instructions] Our first question today comes from Ben Reitzes from Melius.

**Benjamin Reitzes** (Analysts):
I wanted to ask 2, if I could. One on the NBMs. You signed 2 before the last call. So I'm just wondering if we're going to have a lot more of them because it seems like you're already capacity constrained to agree to them. And then do you mind reminding us what the bits under contract will be in the next few years, if that's changed at all? And then I have a quick follow-up.

**David V. Goeckeler** (Executives):
I'll make a few comments -- Thanks, Ben. We appreciate it. Always good to hear from you. So I'll make a few comments on NBMs, and then Luis will fill in. We've got a very strong pipeline of NBMs, and you kind of hit on all the issues there. As the portfolio gets more subscribed and more committed and we're at half the bits for this fiscal year and 2/3 for next year, it's a fitting exercise to get the next tranche of them in there. But the pipeline is very strong. 
I think we said last quarter -- I know we said last quarter that we're going to be patient and consider the next set of customers. And that's exactly what we're doing. And we expect more of them over the next several months, several quarters as we continue to allocate the rest of the portfolio. 
So the pipeline is very strong and growing, quite frankly, and it's become the predominant way we deal with our customers. And I expect that the percent of the portfolio committed to continue to go up over the next couple of quarters. Luis?

**Luis Visoso** (Executives):
Yes. I mean just a few things because I think David covered most of it. We feel very good about where we are with the NBMs. As you know, we've been very selective, very strategic in who we chose to sign these deals with. We're looking at the companies we have, and 95% of our NBMs are with companies that are investment grade, and they generated about $130 billion in operating cash flow. So we feel that we've made the right choices. 
And as David just mentioned, we'll continue to be patient. We'll continue to be selective, and the pipeline is terrific. So you should expect us to make -- continue to make progress. I think in my prepared remarks, I said that we expect the bits to continue to grow. We had shared with you that about 50% of our bits are under NBM for '27 and about 2/3 for '28. And we expect that number to continue to go a little bit higher from the 2/3.

**David V. Goeckeler** (Executives):
Ben, I'll just make one more comment. You got to ask 2 questions, so I'll make 2 comments. We're also balancing customers that are coming back for more, like that is a real thing. And in general, we're hearing from our customers that they have underestimated the amount of NAND they need to run their infrastructure. And so we have multiple customers coming back for a second round and then balancing that against bringing new customers into the portfolio. 
So there's a lot to sort out, and these are big, complicated agreements, but we feel very, very good about where the pipeline is, where the portfolio is at, the products are resonating. And we'll continue to update you as we build out the portfolio of NBMs over the next couple of quarters.

**Benjamin Reitzes** (Analysts):
Okay. Great. And just a quick follow-up. You may have seen that Intel guided down for the next quarter due to PCs, and it really -- the impact of the memory is more than anybody thought, at least with their guidance. I don't know about anybody else. Just wondering if you are seeing NBM interest from those in the PC market more? 
And how you -- if there's -- if that market, with regard to some of the device makers, is something that will become an NBM or is actually now getting more attractive because they're willing to pay more? How should we think about that as it looks like they're starved for product and missing numbers in that segment?

**Luis Visoso** (Executives):
I mean, Ben, we have -- we cannot talk about specific customers. What we've said in the past is we do have NBMs in the data center business. It's data center-centric, but we also have customers on the edge. And we've offered this construct to any customer that wants it and start a process where it makes sense. So we're not trying to restrict it from any customer. We're open for business.

**David V. Goeckeler** (Executives):
So Ben, the other thing I'll say to this. I mean, we are looking at this in our own reviews. We know that units were down this year. They're going to be slightly down next year, low single digits. I mean these 2 calendar quarters right now are really the trough of the year-over-year compares where they're the most negative. And so this is where we're feeling the biggest amount of change in that market on a unit basis, on a year-over-year basis. 
All that said, we expect the PC exabytes to grow next year. And in fact, we think our internal models are every segment in the NAND market, PCs, smartphones, data center will all show positive growth next year because of content per device continues to go up as part of that is mixing to premium. So there's no doubt there's been a market adjustment. In many ways, we're in the -- as I said, from a unit basis, we're in the teeth of that on a year-over-year basis, but we see improvement from here.

**Operator** (Operator):
Our next question comes from Joe Moore from Morgan Stanley.

**Joseph Moore** (Analysts):
It seems like the underlying story here, in addition to just how good the market is, is your presence in data center. You're up almost 20x year-on-year, up 61% sequentially. Can you talk about -- obviously, the market is good, but it seems like your participation is also a lot better. Is that because of BiCS8? Is that just because the market is different? Just what is it that's allowing you to get to those levels of penetration? And if data center is half of bits at some point, will you get to that in your own mix as well?

**David V. Goeckeler** (Executives):
Yes, Joe, so thanks for the comment. We feel very good about where we're at in data center. I mean anything where you see the kind of numbers we posted year-over-year is a combination of things. I mean it starts with the fundamental NAND node. BiCS8 is a very good node. CBA gives you very, very clean CMOS, which is very good interface speeds, all those kinds of things. 
We built the right products. We've had a TLC product in the market for several years now. It was just a couple of quarters ago that we started selling our QLC product for revenue and that -- we expected that to ramp, and that's happening. So we got the right product at the right time based on the right technology.
And then over the last quarter or so, there's been a lot more refinement of the AI inference architecture is what I would say. When I look at the market and we kind of decompose it internally, customers are just getting more refined about how they're using NAND, where they're using TLC, where they're using QLC, all different phases from KV cache to staging, to fast data lakes and all the subparts of those markets, inference and agent orchestration, model pre-training, model post-training. There's just a general -- we're seeing NAND be applied in a more, I would say, nuanced way.
In the past, QLC is being used in the right places. And you're even seeing QLC, some customers even move into like KV cache where they can be supported. On the other side of the spectrum, we're seeing SLC being pulled into the architecture. It's not really in sales yet. It's more in architectural conversations. And it's not a performance type of conversation. It's more endurance, during agentic workloads, the amount of endurance required. 
And in that place, it's kind of where can we substitute NAND for DRAM. And we think those kind of architectures will be very sticky over time. Once you make that transition, you're going to stick with it given the price differential. So we see all of these things working together. And I think these NBMs set us up for these very deep and strategic level conversations with our customers about how they're using our product, deep discussions with our engineers about how they could use our product to solve different use cases. And all of that is leading to a tremendous pull on our portfolio. 
And like I said, our biggest customers, we've already signed one second tranche of an NBM, and we're in discussions in others. So the whole setup is very strong, and we feel good about it, and we appreciate your recognition of the performance on a year-over-year basis. It really is quite outstanding.

**Joseph Moore** (Analysts):
It is surprising. And where do you think the mix goes long term in terms of good over half...

**David V. Goeckeler** (Executives):
So we're working hard to catch up to have our portfolio mix equal what the market bits are. And we're going to continue to make progress throughout calendar year '27. We'll see if we actually catch up by the end of the quarter, but I think we'll get to a substantially higher number on mix than we are if we look back at calendar year -- or fiscal year '26. We'll continue to make progress here.

**Operator** (Operator):
Our next question comes from Mark Newman from Bernstein.

**Mark Newman** (Analysts):
On the -- if I could just, first of all, talk about price and volume in the guidance. You talked about in the fiscal Q1 that you just reported, I think you said 60% of the revenue growth from volume and 40% from pricing. Baked into your guide, I mean, how do you expect that mix to progress? Any comments on pricing?
I appreciate that you've got a very high portion of the volumes on these NBMs, but still wanted to get some clarity on pricing. I think there's a comment that modest improvement in pricing in FQ2. Any further clarity on that? And then I have a follow-on question on HBF and some of the new NAND technologies as well.

**Luis Visoso** (Executives):
So let me take the first one. Yes, you're right. We reported 60% -- about 60% of the revenue growth came from volume and 40% from pricing in Q1 roughly. And we do expect both to contribute in the next quarter. We normally don't break this, Mark, into its pieces, but we do expect some modest pricing as we put in our prepared remarks. So we do expect both to contribute during the quarter, and we expect pricing to continue to increase modestly throughout the year.

**Mark Newman** (Analysts):
That's helpful. Fair enough. And follow-up question is on HBF and other new NAND technologies in the data center. So there was a comment about some progress on HBF, which was great to hear. But I wondered if there's any more comments on progress and discussions with partners and customers, anything there? 
And the other thing, Dave, you mentioned about some of the other new NAND technologies in the data center, Storage-Next, and then there's also the CMX context memory. Just what's your view on all these types of new NAND tiers in the data center? Do you think that they all win? Just any kind of comments on the interplay of all these and the roles for each and how SanDisk plays in them and the timing would be really appreciated.

**David V. Goeckeler** (Executives):
Sure. So Mark, the conversations with potential customers on HBF are robust and continue to be -- we'll continue to have those conversations as we go into putting product samples in their hands so they can start to use and understand how it's going to fit in their system. So we'll continue to update on that, but it's kind of an always-on conversation. 
Your second question, I think this is like very, very healthy for where AI inference is, which is as it scales out, it needs to be -- the architecture is just being relentlessly refined for economics. And that's a very good thing because it's going to -- if it's going to scale, the more economic it is, the better. And that's pulling NAND into more parts of the architecture because NAND is the most scalable semiconductor technology, right? 
So we're seeing -- like I said, we're seeing -- if you would go back a couple of years ago, it was all about going for more density again, going from TLC to QLC. We're still doing that, right? That's still a big part of the strategy. But now, there's some of it even going in the other direction. How do I use -- how do I get more endurance in specific parts of the architecture? Is the endurance and the performance I get out of NAND good enough to solve the use case at a part of the architecture where I can use it over competing technologies that may be significantly more expensive and difficult to acquire. 
So I would say this is a very, very dynamic discussion. There's a lot of ideas on the table. I think there should be a lot of ideas on the table. I think they'll all be pursued. And I think that it is -- the most important thing is to stay close to the people that are spending the money to scale the infrastructure because in the end, they'll make the decisions of what's right for them based on the use cases they're trying to solve at scale and where they're putting all this money behind it. 
And we're deeply engaged in those conversations, and I expect them to continue to be very robust and have a lot of different ideas about how we could stretch our technology in different directions to fit more and more use cases. And building a product, it's always the same thing. I want the right technology at the right time and the right intensity at the right cost and really not anything less or anything more. And that's what building a product is all about because you can deliver it at the right price and then you can get the right return on it. So that process is full on in AI inference architecture working with our customers.

**Operator** (Operator):
Our next question comes from David Gibson from MST Financial.

**David Gibson** (Analysts):
A really great quarter. Well done. Can you hear me?

**David V. Goeckeler** (Executives):
Yes, yes. Hi, David.

**David Gibson** (Analysts):
Just a quick one. Just wondering whether you're looking to accelerate the BiCS transition from 8 to 9, 10 and so forth as a way to accelerate the bit growth in the short term and satisfy some of that very strong customer demand?

**David V. Goeckeler** (Executives):
No. I mean we're committed to the bit growth we talked about, mid- to high teens. Those nodal transitions require a lot of planning and tool purchases and where lines are set up. So we're still -- we have that fab plan set up for the kind of bit growth we've been talking about for a long time. So no plans to change that at this point.

**David Gibson** (Analysts):
Okay. And just one follow-up. You talked about earlier about allocating more supply to the data center in Q1. Are there any limits to increasingly allocating your bits to data center?

**David V. Goeckeler** (Executives):
Well, I mean, it's very -- in some ways, yes. I mean, out of the fab, you come out with a certain mix of TLC, QLC, certain die mix, all these kinds of issues. So it's a constant fitting exercise of getting the right product to the right customer. 
And there's a lot of magic that goes on in the organization, and Luis's organization is a big part of that, working with our sales teams of what is the available inventory, what's coming out of the fab, what's the mix, and where is it all going to go. Do you want to say a little bit more about that, Luis?

**Luis Visoso** (Executives):
Yes. I think the only thing I would add, obviously, it changes depending on the time frame you're looking at. Over the short term, it's almost impossible to do anything. It takes 120 days or so to produce a wafer. But obviously, as you look further out, there are more degrees of freedom.

**Operator** (Operator):
Our next question comes from C.J. Muse from Cantor Fitzgerald.

**Christopher Muse** (Analysts):
Just a question on the comment around your NBM pipeline exceeding supply through the end of the decade in the slide deck. I guess, can you elaborate on that? And how is that changing kind of your thought process around what bit supply will look like for the industry over the next handful of years? And how are you adjusting, if at all, your CapEx plans? 
I know you talked about mid-single digits, which implies roughly $2.5 billion to $3 billion gross CapEx, fairly low kind of number. So I would love to hear kind of your thoughts on how the visibility is impacting your thoughts around bit growth and supply.

**David V. Goeckeler** (Executives):
Well, I mean, I think my -- first thing I'd say about it, C.J., is the process is working. I mean it was only 2 or 3 quarters ago, we talked about even instituting this kind of business model. And we had some customers that were like-minded, and we made some very good progress. And here we are a couple of quarters later, and it's -- we talked about this after our Investor Day, we had customers coming to us offering NBMs. 
And that now becomes -- it's not the only way we do business. There's lots of customers with lots of different volume levels and different products, and we want to meet our customers where they are. There's no doubt about that. But it's very good to see that we have a robust pipeline now through the end -- through 2030, and we're even getting beyond that, as we talked about, of customers that are really willing to give us their demand signals and financial commitments. 
And to the question earlier, those kinds of things will allow us, if we choose to, to eventually start changing supply and demand and all those kinds of things. But we're just not there yet, right? We got to go through negotiations on all of those. We've got to get commitments. We've got to get everything all aligned. 
But I would say that the process is working well, and we're very happy with where it's at, and it gives us a lot more visibility into how we plan. But the process is still underway, right? It's still underway. And we'll -- as I said, we'll continue to update you over the next couple of quarters as we make progress.

**Christopher Muse** (Analysts):
Just a quick follow-up for Luis. On these contracts and considering some have deposits, are you able to use those deposits for buybacks? Or is that cash restricted?

**Luis Visoso** (Executives):
Yes. In theory, we could, C.J. But as we explained at Analyst Day, the vast majority are financial guarantees, which are held by third-party financial institutions. So they are not in my balance sheet. The only thing that's in the balance sheet is prepayments, and we -- that's, by far, the smallest amount. But there is no legal restriction on that.

**Operator** (Operator):
Our next question comes from Karl Ackerman from BNP Paribas.

**Karl Ackerman** (Analysts):
It's encouraging to see increasing NAND content for xPU and AI servers to support KV cache demand, which, I think, compares to reductions in memory content in some server SKUs. But Dave, could you discuss how you see enterprise SSD content per server progressing in 2027 in the context of this agentic AI proliferation? Because it's certainly becoming a larger portion of your portfolio.

**David V. Goeckeler** (Executives):
That's a big question, Karl. I mean, look, what we're doing is there's no doubt in inference and agent orchestration that our product is tied to kind of CPU demand in -- for those type of applications. I mean we know at a pretty granular level the amount of demand that we expect per CPU, something 60 to 90 gigabytes per CPU is what we see in those kind of applications. I haven't run the math against what the server TAM is and kind of what the elasticity is between those 2, but we can follow up on that.
But as I said earlier, we continue to see more NAND being pulled into the inference architecture in all parts of the architecture and in very different ways, right? TLC, QLC and as I said earlier, now, people looking for high endurance solutions that will fit parts of the workload where they don't need to use DRAM and they can use that type of NAND. So it's all very encouraging, and we'll continue to stay close. But we'll do some work on the 2 TAM analysis and what the trade-offs are between them.

**Karl Ackerman** (Analysts):
Sure. If I may, a quick follow-up. Do you have an updated view or progress on your goal for enterprise SSD share? I mean, can you achieve perhaps that low to mid-teens share in 2027 because you're seeing quite success right now?

**David V. Goeckeler** (Executives):
We've tried not -- I mean, in the past, like many, many years ago, we put some share goals out there, and I've tried very hard not to put share goals out there because sometimes it leads to kind of perverse choices in the portfolio. We want to maximize the value of the portfolio across all time horizons, near term, midterm, long term. So we want to keep some balance into it. 
Clearly, we're going to mix higher into data center. I mean you see that. We talked about that earlier. I think 17x growth year-over-year. You don't see a 17x very often in a business at this scale. And as I said, I expect that to go higher as we go through '27. 
And the balance point, in some ways, will be dependent -- will depend quarter-by-quarter what we see and then what NBMs we sign, right? Those will give us a big -- a lot of visibility over the next several years where we see that mix going. So it's going higher, but I'm not going to put a specific target out there.

**Operator** (Operator):
Our next question comes from Vijay Rakesh from Mizuho.

**Vijay Rakesh** (Analysts):
Great quarter and guide. Just a quick question. As you look at data center, 2027 looks like, you mentioned, 40% demand bit growth, which is massive. As you look at this BiCS8, BiCS9, BiCS10 transition, do they help you drive some bits to meet that demand? How is the supply on that side, I guess? I have a quick follow-up.

**David V. Goeckeler** (Executives):
Look, I mean, BiCS8, BiCS9, BiCS9 is a big part of a data center strategy of being able to get faster interface speeds with the same cell and kind of what CBA gives us that flexibility we talked about at Investor Day. So in that sense, yes, those are big parts of the strategy. There's no doubt about it.
So as I said earlier, it's about getting the right product to the right customer. And the TLC product has been performing very, very well for quite some time now. And now we're seeing the ramping of QLC. And we'll see some ramp of BiCS9, but BiCS10 is still a little ways out, right? I mean we announced BiCS10, but we're still ramping BiCS8. So we've got a ways to go before we get out to some of those future BiCS nodes.

**Vijay Rakesh** (Analysts):
Got it. And then on the endurance side, as you mentioned, some of your peers talking about SLC NAND out there. Any thoughts how that plays out next year? Obviously, that could tighten up the NAND market as well in addition to what you're seeing in just overall demand growth, I guess.

**David V. Goeckeler** (Executives):
Yes, I think it's a little early to have a very strong view on that, right? We are talking to some customers that are giving us some signals of demand for SLC. I mean, clearly, you start mixing SLC and you're going to take away -- there's a clear trade ratio of 3:1, 4:1, whether it's TLC or QLC. So it will impact the overall supply in the market depending on how much SLC is used and how much really gets deployed. 
But it's a little early to put a specific forecast on it right now. What I would say, it's an architectural discussion and a request from customers of better understanding the technology and how it could fit parts of the use case as they build out their inference architecture. So we'll update you as we go over the next couple of quarters, and we'll see how this develops, but definitely something to keep an eye on.

**Operator** (Operator):
Our next question comes from Jim Schneider from Goldman Sachs.

**James Schneider** (Analysts):
I was wondering maybe on a more tactical basis, your consumer business obviously has seasonality in Q1 historically. And obviously, the PC business does too, but data center is in sort of secular growth mode. So Luis, based on your visibility at this point, I'm just wondering if you could maybe give us any kind of color on whether you'd expect Q1 to be sequentially up, down or sideways, roughly?

**Luis Visoso** (Executives):
So fiscal Q3, you mean?

**James Schneider** (Analysts):
Yes, fiscal, the March quarter.

**Luis Visoso** (Executives):
So if you look at historically, right, our Q3 is normally our weakest sequential quarter. So last quarter, for example, our bits were down 19% sequentially. So if I -- we're not guiding Q3. But for modeling purposes, I would be conservative in your sequential growth from Q2 to Q3.

**James Schneider** (Analysts):
And then just as a matter of principle on the buyback, good to see the continued execution there. I'm sort of curious, as you sort of start to run down the authorization, would you expect the Board to re-up their authorization on a quarterly basis? Or maybe you could provide us any more color on how you're thinking about executing on the actual buybacks given a much lower stock price today?

**David V. Goeckeler** (Executives):
So we're -- we have a very clear strategy. 100% of excess cash is going to go back to shareholders. We're going to execute that aggressively or appropriately. And we know how to get a hold of the Board. We have meetings every quarter. And so I don't expect any impedance on that side of the -- from us about how we execute.
I expect us to continue to be -- I don't expect us to be, we will be, continue to be faithful to our strategy, which is we're going to return 100% of excess cash to shareholders. We're off to a good start, I think, over the last couple of quarters. I think we bought back 4% of the market cap of the shares outstanding of where we started, and we're going to continue to execute that program appropriately.

**Operator** (Operator):
And our next question comes from Krish Sankar from TD Cowen.

**Kinney Chin** (Analysts):
This is Steven calling on behalf of Krish. First question I have for Dave. I guess looking at your CSP customer base, I kind of wanted to get some color on what the prevailing demand currently is between TLC versus QLC bits? And kind of going forward with the NBMs in place, does that TLC versus QLC mix shift meaningfully later this decade?

**David V. Goeckeler** (Executives):
We're still like at that 70-30 number on TLC to QLC. TLC has been a big driver of the portfolio. We are hearing more from our customers about a reacceleration of QLC in different use cases. And so we'll see how that plays out, as you said, through the end of the decade. But that's where it is. I mean, that 70-30 number is a pretty good number. 
And of course, there's some fluctuation quarter-to-quarter, a little bit up and down here and there, but that's where it's been, and that's where we expect it to be, at least for the next -- the rest of this fiscal year. Let me put that time horizon on it, and then we'll see where -- what customers are thinking about QLC as we continue to have those discussions. 
And I will say the ramp -- the Stargate product has been -- which is our QLC product. There's too many internal names here, but it's been very well received. It was not that many quarters ago that we were talking about going through qualifications. That's all 100% behind us. Customers are ramping. It's been a very, very well-received product and a very key part of the portfolio.

**Kinney Chin** (Analysts):
Got you. And as a quick follow-up, a question on the mobile edge market. Just given the double-digit unit declines in that market this year as well, but albeit concentrated in the kind of entry and mid-tier of the market. I'm kind of curious like from the demand signals that some of your customers in that market are giving you, can your mobile bits still grow next year overall?

**David V. Goeckeler** (Executives):
Yes. I think -- let's talk about the market first. I mean -- you got it. I mean the low end is under pressure, but that leads to a unit decline, but a content per unit increasing. So when you add it all up, we expect growth of exabytes in that market next year on a slightly declining unit count. As far as our portfolio, I mean, we don't -- it's kind of like data center.
I don't want to make projections on individual markets. We will manage the portfolio with agility and flexibility. We've been very clear that we want balance in the portfolio, but we're going to optimize the financial outcome over the short, mid and long term, kind of integrate those to get the best outcome. And we'll update you on what the mix of mobile is as we go forward.

**Operator** (Operator):
Our next question comes from Wamsi Mohan from Bank of America.

**Wamsi Mohan** (Analysts):
In your slide deck, you say leading AI companies could indicate further demand upside. I was wondering if these are AI labs or neoclouds? And are any of the credit concerns around the neoclouds filtering back to you in any way that you can see at the moment? And I have a follow-up.

**Luis Visoso** (Executives):
We haven't seen any of that. To the contrary, we're seeing very strong demand from our customers. And as I said, if I look at our largest customers, they're basically all investment-grade companies, right, generating very strong cash. So we're not seeing any impacts from any credit issues whatsoever if they are out in the market. And demand from our customers is, if anything, strengthening versus what it was a quarter ago.

**Wamsi Mohan** (Analysts):
So to clarify there, Luis, when you say leading AI companies, are you referring to AI labs over there?

**Luis Visoso** (Executives):
We sell to everybody in our business. We sell to hyperscalers. We sell to model makers. We sell to everybody.

**Wamsi Mohan** (Analysts):
Okay. And then just on linearity in the quarter. It seems like receivables picked up a little bit. Is that something that we should expect because of payment terms as more bits go under NBM? Or was there something else in the quarter?

**Luis Visoso** (Executives):
No. We basically saw a little bit of a change in customer mix, and that has a little bit of an impact on our receivables, a little bit on linearity, but it's mostly customer mix.

**Operator** (Operator):
Our next question comes from Amit Daryani from Evercore.

**Amit Daryanani** (Analysts):
I guess, David, just to start with on the capital allocation side, as you transition towards becoming a more predictable NBM-driven business model, does that change how you think about your capital structure? And historically, I think memory is perceived to be more cyclical, so balance sheet flexibility has been important. 
But as you become structurally, I think, less cyclical, would that support a willingness to take on leverage and potentially accelerate the capital returns? Or is the comfort still with the $5 billion a quarter buyback, which is fairly impressive? I'm just wondering, at what point do you say we can take on more leverage and take advantage of the fact that we're less cyclical?

**David V. Goeckeler** (Executives):
I mean we put a financial model out. I mean we just talked -- we just spent 3.5 hours talking about this in our Analyst Day, and we committed to a financial model through the end of the -- through 2030, which I think was pretty impressive. And we plan to execute that, and we're very comfortable with the strategy we have of staying debt-free, very strong balance sheet and then returning -- investing in our business.
We have a growing business and lots of opportunities for internal innovation, which we're going to continue to invest in like HBF and 3D Matrix Memory in addition to the BiCS road map and all the great products we build. And after we do that, we're going to return 100% of the cash flow to shareholders. And that's the plan, and we're going to go execute that for the foreseeable future until we get up at another point and tell you we're going to change it. But I don't anticipate that happening in any kind of near-term time frame.

**Amit Daryanani** (Analysts):
Fair enough. And then maybe just on HBF and rather than trying to ask you to frame how big this TAM could be. Could you just talk about what the scaling variable really is over here as inference models and context windows expand? Should we think HBF capacity will grow in line to GPU compute or potentially faster? And I think you said you'll start initial sampling in '27. What are the key milestones from there to becoming a meaningful revenue ramp as well?

**David V. Goeckeler** (Executives):
Well, I mean -- so it's a little early for your first question. But on the second question, we get the die back. We have the base die, which we'll tape out, which is the controller, we'll put them together, put it in customers' hands. And then they start to see how the product is going to work in their infrastructure. 
We've obviously done a lot of modeling on that, but actually having the actual product and then doing the integration work, that will then lead -- that kind of feedback from the customer will then lead to be able to start to answer some of the questions that people have, like what's the market opportunity, how fast is it going to happen, what's the TAM, where exactly is the architecture going to fit. We're going to follow our customers on that. 
But the big step is to actually put a product in their hands, and then that leads to a whole another set of conversations with them where we actually have the device that we're -- instead of running simulations, we're seeing exactly how it performs in their infrastructure and does it deliver the results of what they're expecting. 
And we'll also -- that also helps you continue to expand the set of use cases, right? At this point in the development process, you want to be a little bit careful. You don't engage too much because you're overwhelming your engineering team with 1,000 ideas of how the product can be used. So as we get actual device that we can put in people's hands, we can open the aperture on those kind of conversations, which will -- I think will lead to more use cases for the product. But that's still TBD. 
So I think a lot of things start to happen when you get to that next milestone of actually having a real product that people can start to -- they can start to use and understand how it impacts what they're trying to do, which is deliver a world-class inference architecture at the best cost point possible. And we think this is a fantastic technology for doing that, but we'll see when we get there and we produce it.

**Operator** (Operator):
Our next question comes from Mehdi Hosseini from SIG.

**Mehdi Hosseini** (Analysts):
David, I want to go back to -- sorry for the audio. David, I want to go back to what you said earlier. You said that AI inferencing is being refined, having an impact and more SLC needed. And my question to you is, is this having an adverse impact on adoption of TLC or the growth of TLC, or SLC is additive to the bit demand by TLC and QLC?

**David V. Goeckeler** (Executives):
No, I don't think it's a cannibalization of other NAND products. I think it's an expansion of the TAM into areas that you need different attributes of the technology. You need different endurance, you need different performance. And we can take our product and we can run anything out of the fab in an SLC mode. So there's a lot of flexibility in the product. 
And I think our people are discovering that and starting to understand how can I apply this in ways where I get the attributes I want for the problem I'm trying to solve. So it's just a more refined view of the architecture, but I don't see it as cannibalizing other parts of the NAND stack. If anything, I see it as -- and I want to be careful on this because it's still early, but it's -- is it good enough to replace places where I'm using DRAM, right? Can I get enough endurance? Can I get enough performance if I run NAND in an SLC mode? Because the cost differential is like huge, 20 to 40x. 
So I take it as a very healthy sign on many ways, Mehdi. One is that very, very real about how you scale an architecture. When you scale an architecture, you got to do it in the most cost-effective way possible. And again, NAND is the most scalable semiconductor technology. And so it doesn't surprise me that people are finding more ways to use it. In many ways, I think scalable technologies kind of attract TAM. And I think that that's what's happening here as these architectures are getting more detailed and more refined.

**Mehdi Hosseini** (Analysts):
Okay. Let me come at it from a different angle. And if there is this demand for more enduring SLC and as customers wait for commercialization of HBF, what is the JV's flexibility in adding some SLC capacity to meet that short-term demand?

**David V. Goeckeler** (Executives):
No, we don't -- I mean, we don't -- there is no -- I mean, I wouldn't think of it as SLC capacity. You can take any -- our cells are flexible enough that we can run them in whatever mode we want, SLC, MLC, TLC. So we can supply the market with the wafers we have, right? That's how we think about it. 
And I understand the question of wanting to go to the supply question right away, but it's just like super early for that. These are just conversations at this point and customers exploring how they can use the technology, starting to get some idea of what their demand would be if they use it this way. It's something to keep your eye on. It will impact the market, no doubt about that, because SLC is -- a little bit of SLC is a lot of QLC. But I guess more to come, Mehdi.

**Operator** (Operator):
And at this point, ladies and gentlemen, we'll be ending today's question-and-answer session. I'd like to turn the floor back over to management for any closing remarks.

**David V. Goeckeler** (Executives):
All right, everyone. Thanks for joining us on the call. We appreciate it. Great conversation, and we look forward to seeing you throughout the quarter. Thank you.

**Luis Visoso** (Executives):
Thank you.

**Operator** (Operator):
And with that, we'll conclude today's conference call and presentation. We do thank you for joining. You may now disconnect your lines.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SNDK_Q4_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO Luis Visoso｜guidance：FQ1'27 營收財測 $10.3–10.8B，成長來自 bit 與價格（原話："For the first quarter of fiscal year 2027, we expect revenue between $10.3 billion and $10.8 billion with"）
- 2026-08-05｜CFO Luis Visoso｜guidance：FQ1 成長由 bit 成長與較高價格共同驅動（原話："sequential growth driven by both bit growth and higher pricing."）
- 2026-08-05｜CFO Luis Visoso｜guidance：FQ1 non-GAAP EPS 財測 $44–46，假設 1.55 億稀釋股數（原話："We expect first quarter non-GAAP EPS between $44 and $46"）
- 2026-08-05｜CFO Luis Visoso｜guidance：FQ1 non-GAAP 營業費用財測 $520–540M（原話："non-GAAP operating expenses between $520 million and $540"）
- 2026-08-05｜CFO Luis Visoso｜guidance：管理層估 2026 年 NAND 市場超過 $300B、年增 3 倍（原話："$300 billion in revenue in calendar year 2026, up 3x year-over-year."）
- 2026-08-05｜CFO Luis Visoso｜guidance：管理層估 2027 年 NAND 市場接近 $500B（原話："estimate that the NAND market will approach $500 billion in revenue in calendar year 2027."）
- 2026-08-05｜CFO Luis Visoso｜guidance：管理層稱客戶需求成長快於供給（原話："Demand from our customers is growing faster than our supply."）
- 2026-08-05｜CFO Luis Visoso｜guidance：預期 bit 供給在 2027 曆年之後仍處於配貨狀態（原話："remain on allocation beyond calendar year 2027."）
- 2026-08-05｜CFO Luis Visoso｜guidance：FY27 資本支出金額增加但占營收降至約 6%（原話："relative to revenue will come down to approximately 6%"）
- 2026-08-05｜CFO Luis Visoso｜guidance：FY27 將維持較高庫存天數以支應 NBM 與零組件成本（原話："We plan to operate at higher inventory days"）
- 2026-08-05｜CFO Luis Visoso｜guidance：較高庫存使 FY27 可售 bit 成長降至中段十位數百分比（原話："The higher inventory levels reduce sellable bits to"）
- 2026-08-05｜CEO David Goeckeler｜guidance：Goeckeler 稱智慧型手機與 PC 今年單位量下滑中段十位數百分比（原話："we see units down mid-teens for both smartphones"）
- 2026-08-05｜CEO David Goeckeler｜guidance：預期手機、PC 市場於 2027 曆年恢復成長（原話："We expect these markets to return to growth in calendar"）
- 2026-08-05｜CFO Luis Visoso｜margin：FQ4 non-GAAP 毛利率 84.6%（高於財測 79–81%）（原話："Non-GAAP gross margin for the fourth quarter was 84.6%"）
- 2026-08-05｜CFO Luis Visoso｜margin：FQ4 non-GAAP EPS $39.25（前季 $23.41）（原話："$39.25, up from $23.41 in the prior quarter"）
- 2026-08-05｜CFO Luis Visoso｜margin：FQ4 營收 $8,965M，季增 51%、年增 372%（原話："Revenue for the fourth quarter was $8,965 million, up 51% sequentially and 372% year-over-year."）
- 2026-08-05｜CFO Luis Visoso｜margin：FQ4 營收季增拆解：約 1/3 量、2/3 價（原話："came approximately 1/3 from higher volumes and 2/3"）
- 2026-08-05｜CFO Luis Visoso｜margin：調整後自由現金流 $5,035M（口徑排除 NBM 預付款與保證金）（原話："We generated $5,035 million in adjusted free cash flow"）
- 2026-08-05｜CFO Luis Visoso｜margin：調整後 FCF 排除的 NBM 預付款與存款金額，原文稱仍計入營運現金流（原話："This excludes $1,938 million in NBM prepayments and deposits"）
- 2026-08-05｜CFO Luis Visoso｜margin：CFO 稱 NBM 約維持 80% 毛利率，價格上漲有部分上行空間（原話："we do expect to be around 80% for the new business"）
- 2026-08-05｜CEO David Goeckeler｜margin：CEO 將中 80% 段毛利率描述為合理回報（原話："I think mid-80s gross margin, I would characterize as a fair"）
- 2026-08-05｜CFO Luis Visoso｜margin：CFO 解釋 FQ1 毛利率財測 83–85% 為「略低、略高於」本季實績，含組合與零組件成本假設（原話："So slightly down, slightly up from what we printed"）
- 2026-08-05｜CFO Luis Visoso｜margin：CFO 稱連續 5 季毛利率擴張，終點數字為 86.5%（與稿中 FQ4 84.6% 數字並陳）（原話："starting with 22.7% all the way to 86.5%."）
- 2026-08-05｜CFO Luis Visoso｜customer：自上次財報後新簽 5 筆 NBM（3 筆新客戶、2 筆擴約）（原話："we have signed 5 additional agreements"）
- 2026-08-05｜CFO Luis Visoso｜customer：NBM 預計占 FY27 超過 50% bit、FY28 約 2/3（原話："50% of our bits in fiscal year 2027, and approximately 2/3"）
- 2026-08-05｜CFO Luis Visoso｜customer：已簽 NBM 在地板價假設下最低總營收 $93.9B（原話："is a minimum of $93.9 billion, assuming floor pricing."）
- 2026-08-05｜CFO Luis Visoso｜customer：季末 RPO $59.8B（含季後簽的 2 筆為 $91.1B）（原話："RPO, at the end of the quarter was $59.8 billion"）
- 2026-08-05｜CFO Luis Visoso｜customer：NBM 附現金與金融工具形式的財務保證，總額 $16.5B（原話："financial guarantees through a combination of cash deposits"）
- 2026-08-05｜CFO Luis Visoso｜customer：NBM 定價含固定與浮動部分，浮動部分設有地板與天花板（原話："We expect attractive margins even at"）
- 2026-08-05｜CEO David Goeckeler｜customer：CEO 稱大客戶已回頭要求加量（原話："some of our biggest customers are already coming back"）
- 2026-08-05｜CFO Luis Visoso｜customer：FQ4 消費者營收 $556M，季減 32%（原話："Consumer revenue was $556"）
- 2026-08-05｜CEO David Goeckeler｜customer：CEO 解釋消費端調價難跟上其他市場速度（原話："move the consumer up as much as possible."）
- 2026-08-05｜CEO David Goeckeler｜customer：資料中心占 bit 比重由一年前約 12% 升至本財年末 38%（原話："A year ago, Datacenter represented roughly 12% of our bits."）
- 2026-08-05｜CFO Luis Visoso｜commitment：管理層承諾對新增 NBM 保持高度挑選（原話："Going forward, we will remain highly"）
- 2026-08-05｜CEO David Goeckeler｜commitment：CEO 稱買回執行將維持一致（原話："We expect to be very consistent in our execution of this program."）
- 2026-08-05｜CFO Luis Visoso｜commitment：供給成長維持中到高十位數百分比的承諾（原話："we continue to be committed to grow bits mid- to high teens"）
- 2026-08-05｜CFO Luis Visoso｜commitment：CFO 稱 FY27 長期 bit 成長數字會略低（原話："our ongoing number, will be a little bit lower for 2027."）
- 2026-08-05｜CEO David Goeckeler｜commitment：CEO 稱計畫與市場同步成長（原話："We want to grow with the market, and we plan to grow with the market."）
- 2026-08-05｜CFO Luis Visoso｜capital_allocation：董事會再授權 $14B 買回，剩餘授權合計 $15.5B（原話："an additional $14 billion share repurchase program"）
- 2026-08-05｜CFO Luis Visoso｜capital_allocation：CFO 稱目前以買回作為股東回報方式，並說明情況可能改變（原話："things may change as time goes on"）
- 2026-08-05｜CFO Luis Visoso｜capital_allocation：CFO 以稅務效率為買回理由（原話："more tax efficient and probably the right thing for us to do"）
- 2026-08-05｜CEO David Goeckeler｜product：BiCS 8 已提升至多數 bit 產出（原話："we ramped BiCS 8 to the majority of our bit"）
- 2026-08-05｜CEO David Goeckeler｜product：QLC Stargate 平台本季開始出貨並認列營收（原話："we began shipping our QLC Stargate platform for revenue"）
- 2026-08-05｜CEO David Goeckeler｜product：CEO 談 HBF 出貨與發布時間表，僅說之後再公布（原話："So we'll have more to say as we progress with"）
- 2026-08-05｜CEO David Goeckeler｜product：CEO 稱對 BiCS 10 與 HBF 定價評論為時尚早（原話："it's a little early to talk about pricing on some of those nodes"）
- 2026-08-05｜CEO David Goeckeler｜competition：供給成長主要靠製程節點轉換而非增加晶圓（原話："primarily through nodal transitions rather than wafer additions"）
- 2026-08-05｜CEO David Goeckeler｜competition：被問在 $500B 市場是否維持市占，CEO 稱這一直是目標（原話："It's always our goal, Joe."）
- 2026-08-05｜CEO David Goeckeler｜risk：CEO 提及 $16.5B 保證金的情境：黑天鵝事件（原話："But if some black swan event happens"）
- 2026-08-05｜CEO David Goeckeler｜risk：CEO 說明保證金額度預期不會真的收到（原話："$16.5 billion in aggregate would flow to us"）
- 2026-08-05｜CEO David Goeckeler｜risk：CEO 對比一年前能見度僅 3 個月（敘事轉變：現稱 4 年以上）（原話："we were talking about visibility in this business of 3 months"）

### SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md
- 2026-08-13｜CFO Luis Visoso｜guidance：2028–2030 營收成長目標與位元成長一致（原話："we expect to grow revenue mid- to high teens"）
- 2026-08-13｜CFO Luis Visoso｜margin：2028–2030 non-GAAP 毛利率目標約 80%（原話："We expect non-GAAP gross margin to be around 80%."）
- 2026-08-13｜CFO Luis Visoso｜margin：營業利益率 75% 的拆解：OpEx 約 5% 營收（原話："We expect to spend about 5% in OpEx"）
- 2026-08-13｜CFO Luis Visoso｜guidance：75% 營業利益率之後，調整後自由現金流率 50%（原話："So you get to that 75%. And then you get to 50%"）
- 2026-08-13｜CFO Luis Visoso｜guidance：建模用資本密集度假設為中個位數 % 營收（gross CapEx）（原話："I would assume mid-single-digit capital intensity"）
- 2026-08-13｜CFO Luis Visoso｜guidance：FY27 位元成長中段十幾 %、價格逐季溫和（原話："we expect sequential prices to be modest throughout the year"）
- 2026-08-13｜CEO David Goeckeler｜commitment：承諾位元／出貨量長期中高十幾 % 成長（原話："committed to this grow volume mid- to high teens."）
- 2026-08-13｜CFO Luis Visoso｜commitment：超額現金 100% 還給股東（原話："excess cash -- will go back to shareholders."）
- 2026-08-13｜CFO Luis Visoso｜capital_allocation：董事會再授權 140 億美元庫藏股（原話："the Board authorized another $14 billion program."）
- 2026-08-13｜CFO Luis Visoso｜capital_allocation：無負債、不動用循環信貸（原話："We have no debt. We got rid of the TLB."）
- 2026-08-13｜CFO Luis Visoso｜capital_allocation：信評 BB+，打算持續改善（原話："We're at BB+ overall, and we intend to continue"）
- 2026-08-13｜CEO David Goeckeler｜capital_allocation：延長與 Kioxia 合資，確保 2030–2034 產能（原話："we had production of NAND from 2030 to 2034"）
- 2026-08-13｜CEO David Goeckeler｜capital_allocation：持有 4% 股權，本季認列約 8 億美元收益（原話："we took a 4% equity stake in the company."）
- 2026-08-13｜CEO David Goeckeler｜capital_allocation：該股權投資認列的收益金額（原話："an $800 million gain on that investment."）
- 2026-08-13｜CFO Luis Visoso｜customer：NBM 客戶共 8 家，含 3 家美國超大規模業者（原話："include 3 hyperscalers from the U.S."）
- 2026-08-13｜CFO Luis Visoso｜customer：最早一筆 NBM 僅在今年 1 月簽署（原話："the oldest deal we signed was only in January of this"）
- 2026-08-13｜CFO Luis Visoso｜customer：2 家客戶已回頭擴大合約（原話："2 customers already came back and they said"）
- 2026-08-13｜CEO David Goeckeler｜customer：客戶開始主動提出多年合約（原話："now they're proposing the agreement, not us."）
- 2026-08-13｜CFO Luis Visoso｜commitment：NBM 合約平均期間超過 4 年、最長 5 年（原話："The longest contract is 5 years"）
- 2026-08-13｜CFO Luis Visoso｜customer：NBM 合約帶有固定與變動定價（原話："there are fixed and variable components on pricing."）
- 2026-08-13｜CFO Luis Visoso｜risk：每份 NBM 皆有財務擔保（原話："every single one of these agreements has a financial"）
- 2026-08-13｜CFO Luis Visoso｜margin：NBM 底價情境下毛利率約 80%（原話："around 80% gross margin for the floor pricing."）
- 2026-08-13｜CFO Luis Visoso｜margin：重申底價下 NBM 毛利率不低於約 80%（原話："we don't expect these NBMs to be below 80%"）
- 2026-08-13｜CFO Luis Visoso｜customer：NBM 總合約價值（以底價計）（原話："the $93.9 billion, that's the Total Contract Value, TCV."）
- 2026-08-13｜CFO Luis Visoso｜customer：剩餘履約義務金額（原話："RPO, is $91.1 billion."）
- 2026-08-13｜CFO Luis Visoso｜risk：已取得的財務擔保總額（原話："we have secured $16.5 billion in financial guarantees"）
- 2026-08-13｜CFO Luis Visoso｜risk：客戶存款與信用額度已入帳 25 億美元（原話："$2.5 billion in our bank."）
- 2026-08-13｜CEO David Goeckeler｜guidance：供給有 50% 至 2/3 已在協議下（原話："50% to 2/3 of our supply is under agreements"）
- 2026-08-13｜CFO Luis Visoso｜commitment：對新增 NBM 保持挑選（原話："We'll be very selective going forward to make sure we"）
- 2026-08-13｜CFO Luis Visoso｜margin：FY26 毛利率 71.6%，前一年 30.3%（原話："Gross margin 71.6% -- that's up from 30.3% the year before."）
- 2026-08-13｜CFO Luis Visoso｜margin：FY26 第四季毛利率 84.6%（原話："We closed the year with 84.6% gross margin."）
- 2026-08-13｜CFO Luis Visoso｜margin：自由現金流口徑：排除 NBM 預付款與保證金（原話："And this excludes cash we received from our NBMs as"）
- 2026-08-13｜CFO Luis Visoso｜margin：FY26 自由現金流（不含 NBM 預付款）（原話："We generated $8.7 billion in free cash flow"）
- 2026-08-13｜CEO David Goeckeler｜margin：管理層表示不預期 2023 年那種低谷重現（原話："I don't expect '23 to come back, by the way."）
- 2026-08-13｜CFO Luis Visoso｜guidance：HBF 不在營收預測內（原話："HBF is not in the revenue projections."）
- 2026-08-13｜CEO David Goeckeler｜guidance：澄清 3000 億／5000 億美元是含中國的市場規模，非營收預測（原話："revenue forecast for '27. It wasn't, right? It wasn't."）
- 2026-08-13｜Eric Cherrstrom｜guidance：市場規模預測 2027 年近 5000 億美元（原話："again grow to nearly $500 billion in 2027"）
- 2026-08-13｜Eric Cherrstrom｜risk：邊緣裝置（PC/手機）單位數預期年減中十幾 %（原話："our expectation of unit decline year-over-year"）
- 2026-08-13｜Eric Cherrstrom｜competition：資料中心占 TAM 位元比重（原話："This year, 50% and continues to outpace the market."）
- 2026-08-13｜CTO Alper Ilkbahar｜competition：同業資本支出為公司的 2.66 倍（原話："the industry spent on average, 2.66x more capital"）
- 2026-08-13｜CTO Alper Ilkbahar｜competition：資本效率約為最近競爭對手 2 倍（原話："our capital efficiency is just about 2x that of our nearest"）
- 2026-08-13｜CTO Alper Ilkbahar｜competition：同業新世代功耗效率改善有限（原話："their power efficiency is really not moving a lot better."）
- 2026-08-13｜CEO David Goeckeler｜competition：舊世界（低於邊際成本賣 NAND）已不存在（原話："I think that world has gone, quite frankly."）
- 2026-08-13｜CTO Alper Ilkbahar｜product：BiCS10 1Tb TLC 本月開始送樣（原話："start sampling this die to our customers as of"）
- 2026-08-13｜CTO Alper Ilkbahar｜product：BiCS10 2Tb QLC 密度比 BiCS8 高逾 60%（原話："more than 60% density improvements over BiCS8"）
- 2026-08-13｜CTO Alper Ilkbahar｜product：BiCS9 已進入 NBM 供貨範圍（原話："this product is already as part of our NBMs"）
- 2026-08-13｜CEO David Goeckeler｜product：每年每片晶圓位元產出成長 27%（原話："we can grow output per wafer at a rate of 27% a"）
- 2026-08-13｜CTO Alper Ilkbahar｜product：實際只用掉 27% 生產力的三分之二（原話："we're using only two-thirds of that capability"）
- 2026-08-13｜CTO Alper Ilkbahar｜product：HBF 第一顆記憶體晶粒已 tape-out（原話："we actually taped out our first HBF memory die."）
- 2026-08-13｜CTO Alper Ilkbahar｜product：HBF 預計明年送樣給推論裝置客戶（原話："deliver our first samples to our customers of"）
- 2026-08-13｜CPO Khurram Ismail｜product：KV cache 預估占 2030 年市場 35%（原話："KV cache is going to be 35% of the"）
- 2026-08-13｜CEO David Goeckeler｜commitment：成本下降歸公司所有，價格由市場決定（原話："the market will determine what the price of our product"）
- 2026-08-13｜CEO David Goeckeler｜commitment：不再討論 cost down（原話："We're not talking about cost downs anymore."）
- 2026-08-13｜CEO David Goeckeler｜guidance：去年投資人日對價格轉正的判斷被低估（原話："if anything, we significantly undercalled it."）
- 2026-08-13｜CEO David Goeckeler｜risk：對 NBM 能否撐過下行期，管理層自承無保證（原話："Is it a guarantee? There's no guarantees."）
- 2026-08-13｜CEO David Goeckeler｜risk：管理層承認客戶可能退出合約的說法存在（原話："They could be just a big head-fake. They"）
- 2026-08-13｜CEO David Goeckeler｜customer：資料中心占比將上升，最終目標視情況（原話："Where is the final target? It depends."）
- 2026-08-13｜CFO Luis Visoso｜customer：NBM 占比隨時間調整，未給 FY29 以後上限（原話："that number will keep on evolving."）

### 問答異常語氣（迴避／改口／保留）
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Reitzes：若每季買回約 $5B，這是否是該思考的買回規模？｜答法：未給金額或節奏數字，僅稱執行將一致、對現金產生有信心
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Schneider：是否考慮股利？｜答法：回答聚焦買回的稅務效率，未直接回應股利問題
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Schneider：是否在與已簽之外的大型雲端業者談新協議？｜答法：拒絕揭露個別合約細節，改談關係長期性
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Muse：價格上漲但為何毛利率財測較低？｜答法：CEO 先說「你已用第二題回答了第一題」，轉談 durability 與 NBM 結構，未直接解釋差異（CFO 後來由 Curtis 追問時才補組合與成本假設）
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Newman：FQ4 量成長拆解與 Q1 財測偏輕的原因（量、價鎖定或保守）｜答法：給了 FQ4 1/3量、2/3價拆解，Q1 僅稱「modest price increases」，未回答是否保守
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Mohan：2027 是否預期價格正常化？｜答法：未回答價格是否正常化，改談與市場同步成長、需求訊號，並稱「I don't know what more to say about it」
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Rakers 代問：產業供需何時收斂、與三個月前看法差異？｜答法：未給時間點，改稱供需透過客戶與供應商對話匹配
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Gibson：HBF 樣品多久出現（1、2、3 年）？｜答法：未給時間，稱下週投資人日再說明
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Rakesh：BiCS 10 與 HBF 是否有價格溢價？｜答法：稱定價評論為時尚早，未給數字
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Newman 問 NBM 占比目標與 FY29 後是否維持三分之二｜答法：CFO 說會『隨時間優化』、與 FY28 數字『一致』但『會持續演變』，未給長期目標占比
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Moore 問資料中心占比倍增後邊緣業務是否被擠壓、供給不足如何平衡｜答法：CEO 自稱『squishy answer』，以『know it when we see it』回應，未給占比數字
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Reitzes 問 HBF 若成功，模型要放掉什麼、上檔怎麼算｜答法：CEO 稱『not ready to go there just yet』，改談 NBM 與等一年看客戶需求
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Rakers 問 HBF 量產後 CapEx／先進封裝資本密集度是否改變｜答法：CTO 表示『let's wait until next year』，改談生產力餘裕，未給資本密集度數字
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Rakers／Mizuho 問 HBF 定價與資本密集度｜答法：CTO 回『I feel it's priceless』，未給定價；資本密集度改以 27% 生產力餘裕回應
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Muse 問 NBM 下年度成本下降是否與客戶分享｜答法：CFO 稱『not going to get into pricing in more detail』，只重申底價約 80% 毛利率
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Feldman 問 BiCS9 及後續 NAND 成本下降幅度｜答法：CEO 表示已不談 cost down，成本下降屬公司，未給數字
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：CEO 追問 CFO 資本密集度承諾，CFO 答『low single digits』｜答法：簡報中 CFO 先前建模假設為『mid-single-digit』，此處口徑改為 low single digits，未說明差異
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Mohan 問為何本次 NBM 在下行週期會比過去更撐得住、客戶預測能力是否更好｜答法：CEO 以『有信心改變結果』『最可能的結果』回應，未直接回答客戶預測能力，並承認『Maybe not』『no guarantees』
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Unknown Analyst 問邊緣客戶去庫存與非資料中心需求展望｜答法：CFO 稱『I just can't get into too much details』，未談去庫存，只說物理 AI 有潛力
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Schneider 問減少 HBM 後需要多少 eSSD／HBF 內容｜答法：CPO 稱視工作負載、『Now could it be reduced by half, one it depends』，未給容量數字

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
{"date":"20260815","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"text","text":"核心假設 H1/H2/H3\n\nH1（升級版）：NBM floor 真實可執行，覆蓋範圍已擴大到FY27過半、FY28約2/3位元——RPO $59.8B（含季後協議 $91.1B）、財務擔保 $16.5B、8個客戶（較4月的5個再增3個）。門檻：RPO淨額不下修、財務擔保不縮水。來源：FY26 Q4 法說（2026-08-05）+ Investor Day（2026-08-13）。漂移觸發（較8/6版本強化）：覆蓋率從「FY27過半」進一步升至「FY28約2/3位元」，管理層明言「還在深度對話中」——H1可信度較上版邊際提升，但仍是合約不是護城河（見下方相依性註記）。\nH2（沿用）：AI/資料中心把NAND需求基底從PC+手機換成伺服器+推論耗材，使through-cycle正規化盈餘台階抬升。門檻：資料中心>40%位元需求。現況：Q4 FY26資料中心占營收33.2%（$2.977B/$8.965B）、占bits 38%（較去年同期12%）。Investor Day進一步預告CY2026資料中心占TAM~50%（去年僅~30%）。來源：SanDisk FY26 Q4法說、Investor Day。\nH3（本版更新）：正規化盈餘力估計自$95上修至約$105-115/股（NBM覆蓋率實質擴大的直接推論），through-cycle倍數同步自12-13倍略上修至12.5-13.5倍（反映合約段可見度真實提升，但不到賣方Goldman 20倍）。分子$110（中值）vs Goldman $110（本次巧合持平，方法論仍完全獨立）；倍數13倍vs Goldman 20倍。來源：本報告§10.7自建。\n相依性註記（沿用）：H1與H3不獨立——若NBM floor在下一輪谷底被重議（2017年記憶體長約在崩盤中曾被重議回現貨的先例），正規化盈餘力立刻退回接近FY23形狀（GAAP虧損、售價/成本比逼近1）。機率處理（本版與§10.5情境樹統一為單一組，獨立覆核後修正）：「floors大致守住」Bull 20%/Base 40%；「floors被重議」Bear **40%**（較8/6版本30%**上修**，理由並非NBM本身轉弱，而是本輪新查證到的供給端證據——Kioxia規劃FY2029前wafer產能翻倍、FY26-28年均capex較FY25+66%、四日市/北上現稼動率僅約50%〔大量待裝機空殼產能〕、Samsung V10已排定2026-10全面量產、YMTC全球位元份額已達14%〔全球第三〕——這些是供給側而非NBM條款本身的風險，但供給過剩仍會透過「非NBM段現貨價格轉弱」間接壓迫NBM段外的營收與整體估值倍數，故Bear機率上修並非否定NBM，而是承認NBM保護不了公司的全部）。"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回落至正規化盈餘力估值(約$1,485，12.5-13.5x normalized EPS $110-120)以下，或NBM覆蓋率/RPO淨額出現趨勢反轉前維持觀望；NAND合約價連2季QoQ轉負則改列迴避評估。","irr_base_pct":1.3,"ev5y_pct":-9.8,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🟠","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.6,"ev5y_pct":-9.8,"irr_base_pct":1.3,"max_dd_pct":-78.0,"bull_5y_price":3200.0,"bear_5y_price":350.0,"p_bull_pct":20.0,"p_bear_pct":40.0,"rearm_trigger":"股價回落至正規化盈餘力估值(約$1,485，12.5-13.5x normalized EPS $110-120)以下，或NBM覆蓋率/RPO淨額出現趨勢反轉前維持觀望；NAND合約價連2季QoQ轉負則改列迴避評估。","price_at_dd":1641.11,"archetype":"循環/商品","cycle_position":"晚循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
