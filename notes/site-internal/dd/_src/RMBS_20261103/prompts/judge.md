你是 stock-analyst **v20 判斷 agent**，標的 RMBS（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"RMBS","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":218.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm"},"note":"高於公司自家指引 210–216"},{"id":"f_kpi1_product_revenue","label":"Product revenue","value":114.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm"},"note":"—"},{"id":"f_kpi2_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":102.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"USD m（利益率 46.8%，新聞稿四捨五入 47%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm"},"note":"未查得可靠共識值"},{"id":"f_kpi3_gaap_operating_income_ma","label":"GAAP operating income / margin","value":83.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"USD m（利益率 38.3%，新聞稿四捨五入 38%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm"},"note":"未查得可靠共識值"},{"id":"f_kpi4_free_cash_flow","label":"Free cash flow","value":91.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"USD m（OCF 102.5 − capex 11.2；非公司定義，自行推算；占營收 41.8%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm"},"note":"未查得可靠共識值"},{"id":"f_kpi6_non_gaap_product_gross_m","label":"Non-GAAP product gross margin","value":60.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm"},"note":"落在公司 60–63% 區間低端；管理層稱因供應鏈投入成本"},{"id":"f_kpi7_guidance_q4_2026_revenue","label":"Guidance Q4 2026 revenue","value":"227–233","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm；Q4 指引另含 product 127–133、royalties 68–74、contract 26–32、non-GAAP opex 120–124、GAAP EPS 0.68–0.76、non-GAAP EPS 0.84–0.92"},"note":"FY1 營收共識 838.4（yfinance，全年口徑），無單季 Q4 共識值"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-26","period":"2026-10-26","unit":"date","basis":"距今 6 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-26"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_rmbs_gross_margin_pct","label":"RMBS 毛利率","value":79.14,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RMBS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_rmbs_operating_margin_pct","label":"RMBS 營業利益率","value":36.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RMBS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_rmbs_fcf_margin_pct","label":"RMBS FCF 利潤率","value":39.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RMBS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_688008_ss_gross_margin_pct","label":"688008.SS 毛利率","value":65.82,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688008.SS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_688008_ss_operating_margin_pct","label":"688008.SS 營業利益率","value":43.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688008.SS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_688008_ss_fcf_margin_pct","label":"688008.SS FCF 利潤率","value":42.26,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688008.SS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrvl_gross_margin_pct","label":"MRVL 毛利率","value":52.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_operating_margin_pct","label":"MRVL 營業利益率","value":16.81,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_fcf_margin_pct","label":"MRVL FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_arm_gross_margin_pct","label":"ARM 毛利率","value":97.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_arm_operating_margin_pct","label":"ARM 營業利益率","value":17.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_arm_fcf_margin_pct","label":"ARM FCF 利潤率","value":28.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_snps_gross_margin_pct","label":"SNPS 毛利率","value":72.38,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_operating_margin_pct","label":"SNPS 營業利益率","value":11.03,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_snps_fcf_margin_pct","label":"SNPS FCF 利潤率","value":29.18,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":20.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"%（SBC 17.1m；占營收 7.8%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm"},"note":"未查得可靠共識值"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":85.71,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-23.13,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":39.73,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.11 → 3.11）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.88 → 3.88）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.89 → 4.89）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.11,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.88,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":4.89,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.64,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 3.03 → 3.11（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":35.42,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝55.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":55.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":11.53,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝41.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":41.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":10.58,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝29.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":29.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":27.56,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.11，分子＝快照價 85.71","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-756.69,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 20.22、現金 776.91（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":107.1,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":8422.77,"period":"2026-11-03","unit":"USD m","basis":"市值 9179.46 ＋ 淨負債 -756.69","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":838.42,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":1010.31,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（8 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":10.05,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 84.1 / W52 105.43 / W104 85.8 / W250 62.41 / W250 13週斜率 1.51%"},{"id":"f_ma_w52","label":"52 週均線","value":105.43,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":85.8,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":62.41,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.51,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列示記憶體介面晶片主要對手為 Monolithic Power Systems、Montage、Renesas、Texas Instruments；矽 IP 對手為客戶自家設計團隊及 Cadence、Synopsys；許多對手規模較大。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"In the memory interface chip market, we compete with international semiconductor companies, including but not limited to Monolithic Power Systems, Montage Technology, Renesas and Texas Instruments. In the Silicon IP market, Rambus competes with the in-house design teams at our potential customers, as well as with third-party IP suppliers, such as Cadence and Synopsys.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：部分客戶內部評估或開發主張無需向 Rambus 授權的技術；公司無法預測在 AI 等目標市場能取得或維持的市占。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"We believe some of the competition for our technologies may come from our prospective customers, some of which are internally evaluating and developing products based on technologies that they contend or may contend will not require a license from us.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Rambus 管理層稱 2025 年底 DDR5 RCD 市占約 mid-40%，高於 2024 年 early 40s（管理層自述）。","source":"MarketBeat Rambus Q4 2025 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/rambus-q4-earnings-call-highlights-2026-02-02/?.tsrc=rss","excerpt":null,"as_of":"2026-02-02","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"第三方分析稱 Rambus Q1 2026 產品營收成長約 15% 低於市場成長，Montage、Renesas 在搶市占。","source":"munich-startup insights: Rambus misses Q1 targets as rivals capture AI memory market share","url":"https://insights.munich-startup.de/news/feed/rambus-misses-q1-targets-as-rivals-capture-ai-memory-market-share-despite-70-8m-licensing-revenue","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q2 2026 財報會：HBM 新設計案為與美國 hyperscaler 的 IP 機會，非產品晶片設計案；並推出 DDR5 9600 晶片組。","source":"MarketBeat Rambus Q2 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/rambus-q2-earnings-call-highlights-2026-07-27/","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K 明列：矽 IP 業務與潛在客戶的 in-house 設計團隊競爭；介面晶片市場競爭者含 Monolithic Power、Montage、Renesas、TI（既有競爭揭露，非新導入第二供應商事件）","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"In the memory interface chip market, we compete with international semiconductor companies, including but not limited to Monolithic Power Systems, Montage Technology, Renesas and Texas Instruments. In the Silicon IP market, Rambus competes with the in-house design teams at our potential customers, as well as with third-party IP suppliers, such as Cadence and Synopsys.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"2026 年搜尋未查得最大客戶導入第二供應商或自製 RMBS 產品環節的來源；10-Q 摘要稱記憶體介面晶片賣給 Micron、Samsung、SK hynix 及系統廠/雲端業者（客戶集中度屬背景事實）","source":"SEC EDGAR 10-Q (period ending 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000917273/000119312526321000/rmbs-20260630.htm","excerpt":"Our memory interface chips are sold to major DRAM manufacturers, Micron, Samsung and SK hynix, as well as directly to system manufacturers and cloud providers, for integration into server and client memory modules.","as_of":"2026-08-05","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 前五大客戶占合併營收約 66%（2024、2023 皆 62%），公司預期集中度將持續。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"Our top five customers for each reporting period represented approximately 66% of our consolidated revenue for the year ended December 31, 2025 and 62% of our consolidated revenue for both the years ended December 31, 2024 and 2023. We expect to continue to experience significant revenue concentration for the foreseeable future.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2025 年總部在美國以外的客戶占營收 82%（2024 為 64%、2023 為 62%）。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"Our revenue from companies headquartered outside of the United States accounted for 82% of total revenue in 2025 as compared to 64% in 2024 and 62% in 2023.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未發現 2026 年 Rambus 主要客戶信用降評、破產或客戶端下修財測的報導；僅見分析師對 Rambus 本身降評（Baird，2026-04-28）。","source":"WebSearch 結果摘要（Seeking Alpha: Rambus falls after rating cut at Baird）","url":"https://seekingalpha.com/news/4580588-rambus-falls-after-rating-cut-at-baird","excerpt":null,"as_of":"2026-04-28","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Q3 2026 累計前五大客戶占營收 63%，Customer A 23%、Customer B 18%（二手摘要）。","source":"Panabee: Rambus Earnings Q3 2026 report","url":"https://www.panabee.com/news/rambus-earnings-q3-2026-report","excerpt":"Customer dependency: High revenue concentration in a few key DRAM manufacturers (Customer A at 23%, Customer B at 18% year-to-date) emphasizes that the company's performance remains inextricably linked to the capital expenditure cycles of these specific partners.","as_of":"2026-10-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner 2Q26 庫存指標跌入中度短缺，AI 半導體需求推動，預期此趨勢持續至 2027。","source":"Gartner Insights Abstract","url":"https://www.gartner.com/en/documents/8208429","excerpt":"In 2Q26, the GIISST fell 8.5% into moderate shortage, driven by strong AI semiconductor demand. This trend is expected to persist through 2027","as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"TrendForce：NAND 2026 年供給短缺 4-5%，2027 下半年供給位元成長將超過需求成長。","source":"TrendForce via itiger: NAND Flash Supply Shortage Expected to Ease in Second Half of 2027","url":"https://www.itiger.com/news/1168527958","excerpt":"supply will fall short of demand by 4-5% in 2026, but by the second half of 2027, the growth in supply bits will outpace demand growth","as_of":"2026-07-20","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"JPMorgan 預期供給限制持續，2028 年初前無顯著產能增加；BofA 預期 2028 仍偏緊，並提示 2027 中為轉折點。","source":"Tradingpedia/itiger 彙整報導（BofA、JPMorgan）","url":"https://www.tradingpedia.com/2026/09/15/bofa-raises-us-chip-targets-on-stronger-growth-outlook/","excerpt":"JPMorgan considers that supply constraints will remain in force and estimates there will be no significant increases in production capacity before the beginning of 2028","as_of":"2026-09-15","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Rambus Q3 2026 管理層：客戶較早下 backlog 訂單、2027 需求預期轉強，但上下半年季節性仍在；Q4 營收指引 227-233 百萬美元。","source":"MarketBeat: Rambus Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-rambus-q3-earnings-call-highlights-2026-10-26/","excerpt":null,"as_of":"2026-10-26","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Rambus 10-Q（截至2026-06-30）揭露自2026年Q1起正回應美國司法部反壟斷署刑事調查的聯邦大陪審團傳票；可能結果含罰款、改變營運做法或禁制令。","source":"SEC EDGAR 10-Q（期間2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0000917273/000119312526321000/rmbs-20260630.htm","excerpt":"Commencing in the first quarter of 2026, we have been responding to a U.S. federal grand jury subpoena in connection with a criminal investigation being conducted by the U.S. Department of Justice, Antitrust Division (\"DOJ\").","as_of":"2026-07-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"MLex 報導 Rambus 依 2026-04-28 監管申報為美國司法部刑事反壟斷調查對象。","source":"MLex：Rambus targeted in US DOJ criminal antitrust probe","url":"https://www.mlex.com/mlex/articles/2471162/rambus-targeted-in-us-doj-criminal-antitrust-probe","excerpt":null,"as_of":"2026-04-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋結果未見 2026 年 FTC 或歐盟執委會針對 Rambus 的行動，亦未見 DOJ 公開起訴、和解或時程。","source":"WebSearch 結果彙整","url":null,"excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：公司為無廠半導體，關稅與貿易限制可能影響客戶需求與供應鏈；美國對半導體相關產品出口中國的管制若擴及公司主力產品/市場，可能衝擊公司。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"In addition, the U.S. government has implemented controls affecting the ability to send certain products and technology related to semiconductors, semiconductor manufacturing and supercomputing to China without an export license and added additional entities to restricted party lists in addition to other import/export and national security laws and regulations. We may be impacted by any of these current or new restrictions in the future if such controls are expanded to cover our key products/markets.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 載明貿易行動（美、中、歐等的關稅、報復性關稅）可能使客戶需求下降並間接降低對公司產品需求；公司無法預測政府行動。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"Government actions that affect our customers’ ability to sell products or access critical elements of their supply chains may result in a decreased demand for their products, which may consequently reduce their demand for our products.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 總統公告對特定先進半導體產品課 25% Section 232 關稅（範圍窄，依技術參數與用途）；搜尋結果未提 Rambus 是否適用","source":"White & Case 2026-01 alert","url":"https://www.whitecase.com/insight-alert/president-trump-orders-narrowly-targeted-25-section-232-tariff-certain-advanced","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2022 10-K 風險因素：部分第三方為唯一製造商或特定材料唯一來源，可能位於地緣政治不確定地區（例：台灣）。","source":"Rambus Form 10-K FY2022 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/917273/000091727323000008/rmbs-20221231.htm","excerpt":"may be located in regions subject to geopolitical uncertainty (e.g., Taiwan)","as_of":"2023-02-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：第三方製造商/供應商可能位於中台緊張與出口/國安限制影響地區，單一夥伴中斷可能影響出貨；地緣衝突可能限制或延遲產品供應。","source":"Rambus Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"Some of these third parties are, and may be, our sole manufacturer or sole source of certain 20 Table of Contents production materials and may be located in regions subject to geopolitical uncertainty (e.g., tensions between China and Taiwan and evolving export/import and national security restrictions).","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收 218.3M 美元，年增 22%，高於指引；產品營收 114.3M 創高（年增 22%），權利金 77.0M（去年同期 65.1M），合約及其他 27.0M","source":"Rambus Q3 2026 results coverage (finviz / SEC 8-K ex99_1)","url":"https://finviz.com/news/408070/rambus-reports-third-quarter-2026-financial-results","excerpt":null,"as_of":"2026-10-26","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q4 2026 指引總營收 227–233M，非 GAAP EPS 0.84–0.92；管理層稱達標需簽下客戶產品銷售與方案授權協議","source":"Rambus Q3 2026 results coverage (finviz / SEC 8-K ex99_1)","url":"https://finviz.com/news/408070/rambus-reports-third-quarter-2026-financial-results","excerpt":"will require that the Company sign customer agreements for various product sales and solutions licensing","as_of":"2026-10-26","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Rambus 自述 2025 年底 DDR5 RCD 市佔約 mid-40%，高於 2024 年底的 early 40s；管理層預期市佔續升（公司自述，無獨立第三方數據）","source":"Rambus Q4 2025 earnings call (Motley Fool transcript)","url":"https://www.fool.com/earnings/call-transcripts/2026/02/02/rambus-rmbs-q4-2025-earnings-call-transcript/","excerpt":"mid-40%","as_of":"2026-02-02","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"WSTS 2026 春季預測：2027 全球半導體市場成長約 27% 至約 1.9 兆美元，記憶體成長 32% 領先；2026 修正為約 1.51 兆美元","source":"TelecomLead / WSTS Spring 2026 forecast","url":"https://telecomlead.com/semiconductor/wsts-raises-semiconductor-forecast-market-to-reach-1-51-trillion-in-2026-grow-to-1-9-trillion-in-2027-126102?noamp=mobile","excerpt":"WSTS forecasts the global semiconductor market to grow a further 27 percent, reaching approximately USD 1.9 trillion. Memory is again expected to lead market expansion with projected growth of 32 percent.","as_of":"2026-06-02","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Gartner 預測 2026 半導體營收 1.555 兆美元、2027 約 1.94 兆美元，AI 資料中心生態系占 2026 營收 36.5%；供需維持吃緊","source":"Gartner press release 2026-08-24","url":"https://gcomdr.pdo.aws.gartner.com/en/newsroom/press-releases/2026-08-24-gartner-forecasts-worldwide-semiconductor-revenue-to-reach-1-trillion-dollars-in-2026","excerpt":null,"as_of":"2026-08-24","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"日本分析認為記憶體成長多來自價格飆升而非量，2027 記憶體成長可能停滯，WSTS 2027 展望偏樂觀（少數觀點）","source":"EE Times Japan 大山聡 業界スコープ(101)","url":"https://eetimes.itmedia.co.jp/ee/spv/2606/08/news023_3.html","excerpt":null,"as_of":"2026-06-08","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素自述：若替代技術以相當效能、相近或更低成本出現，或被認為需付較低/無權利金，客戶可能採用並推廣；即使認定侵權也未必能不經訴訟談成授權。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"To the extent that alternative technologies might provide comparable system performance at lower or similar cost to our technologies, or are perceived to require the payment of no or lower fees and/or royalties, or to the extent other factors influence the industry, our customers and prospective customers may adopt and promote such alternative technologies.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 業務章節同樣載明替代技術風險，且專利執行可能需訴訟、結果不確定。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"As in the past, litigation may be required to enforce and protect our IP rights, on top of the substantial investments undertaken to research and develop our innovations and technologies.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Q3 2026 法說提及記憶體 de-specing（客戶因記憶體經濟性降低模組容量）為需求風險，並討論 SOCAMM2 模組形式。","source":"Rambus Q3 2026 Earnings Call Transcript (Webull)","url":"https://www.webull.com/news/15818016771002368","excerpt":null,"as_of":"2026-10-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 仍描述通路為直銷團隊＋經銷商，同時直接與間接售予模組廠、OEM 與超大規模業者；未見通路或商業模式結構性改變的敘述。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm","excerpt":"We sell memory interface chips directly and indirectly to memory module manufacturers, OEMs and hyperscalers worldwide through multiple channels, including our direct sales force and distributors, and we employ global sales personnel to support such operations.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q3 2026 營收組合：產品收入 $114.3M、權利金 $77.0M、合約及其他 $27.0M（權利金占比下降、產品占比上升）。","source":"Rambus 8-K Ex.99.1 Q3 2026 財報","url":"https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm","excerpt":"Total revenue for the third quarter was $218.3 million, product revenue was $114.3 million, royalties revenue was $77.0 million and contract and other revenue was $27.0 million.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Rambus 2026-10-26 公布 Q3 營收 $218.3M，高於自家指引 $210–216M；Q4 指引營收 $227–233M、non-GAAP EPS $0.84–0.92","source":"Rambus 8-K ex99.1 (Q3 2026 results)","url":"https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm","excerpt":"Rambus expects fourth-quarter revenue of $227 million to $233 million and non-GAAP EPS of $0.84 to $0.92.","as_of":"2026-10-26","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-07-28：共識評等 Moderate Buy，平均目標價 $136.62，區間 $120–$172（Q3 財報前的共識，尚未反映 10-26 後的修正）","source":"MarketBeat, Rambus (RMBS) Buy rating reaffirmed at Rosenblatt","url":"https://www.marketbeat.com/instant-alerts/rambus-rmbs-buy-rating-reaffirmed-at-rosenblatt-securities-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-27 Q2 結果：營收 $207.39M 高於共識 $199.30M，調整後 EPS $0.77 高於預期 $0.05；當時平均目標價 $134.75","source":"MarketBeat, Rambus posts quarterly earnings results","url":"https://www.marketbeat.com/instant-alerts/rambus-nasdaqrmbs-posts-quarterly-earnings-results-beats-estimates-by-005-eps-2026-07-27/","excerpt":"The semiconductor company reported adjusted EPS of $0.77, exceeding estimates by $0.05, while revenue reached $207.39 million versus the $199.30 million consensus.","as_of":"2026-07-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"MarketBeat 稱 Q1 2026 指引低於預期造成股價重設","source":"MarketBeat, Why Rambus market reset might be the best news bulls get","url":"https://www.marketbeat.com/articles/why-rambus-market-reset-might-be-the-best-news-bulls-get/","excerpt":"Rambus' Q1 2026 guidance fell short of expectations, causing a market reset in the stock price.","as_of":"2026-02-15","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Stockalarm 顯示 13 位分析師共識 $145、低 $90、高 $172（Evercore ISI 2026-04 上調至 $172）；未註明快照日期，聚合站間 $136–$147 不一","source":"stockalarm.io RMBS analysts","url":"https://pro.stockalarm.io/quote/RMBS/analysts","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Rambus Q3 財報電話會議重點，可能含 Q4 指引與市場預期對照","source":"MarketBeat transcript highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-rambus-q3-earnings-call-highlights-2026-10-26/","excerpt":"Growth outlook remains strong: Rambus expects fourth-quarter revenue of $227 million to $233 million and non-GAAP EPS of $0.84 to $0.92. Management said the outlook implies approximately 18% revenue growth and 24% product-revenue growth in 2026.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-02-03 股價單日下跌 13.42%（收 98.45 美元）後，Pomerantz 律所於 2026-02 公告調查 Rambus 及其高管是否涉及證券詐欺；僅為律所調查，搜尋未見已提起的集體訴訟。","source":"Pomerantz 新聞稿（Barchart／Minster Community Post 轉載）","url":"https://business.minstercommunitypost.com/minstercommunitypost/article/gnwcq-2026-2-24-investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-rambus-inc-rmbs","excerpt":null,"as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"SEC 8-K 清單：2025-11-03 至 2026-11-03 共 10 份 8-K，含重大項目者 2 份；其中 2026-08-05 為 Item 1.01 的 1 億美元加速股票回購（ASR）協議，非併購。","source":"SEC EDGAR 8-K 申報清單／8-K 2026-08-05","url":"https://www.sec.gov/Archives/edgar/data/917273/000119312526333887/d122300d8k.htm","excerpt":"Rambus Inc. (NASDAQ: RMBS) (the “Company”) entered into a Supplemental Confirmation under the Master Confirmation (the “Master Agreement,” and together with the Supplemental Confirmation, the “ASR Agreement”) with Mizuho Markets Americas LLC","as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"搜尋摘要提及 Rambus 收到與司法部反壟斷調查相關的聯邦大陪審團傳票（未讀到頁面，待核原文）。","source":"Yahoo Finance Rambus Q1 2026 文章","url":"https://finance.yahoo.com/markets/stocks/articles/rambus-inc-rmbs-q1-2026-070454403.html","excerpt":null,"as_of":"2026-04-27","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Pomerantz 律所 2026-02 公告調查 Rambus 是否涉及證券詐欺，起因為 2026-02-03 股價下跌 13.42%；僅為調查，未確認有已提起的集體訴訟。","source":"Pomerantz 新聞稿（Barchart 轉載）","url":"https://www.barchart.com/story/news/450756/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-rambus-inc-rmbs","excerpt":null,"as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"RMBS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.14,"operating_margin_pct":36.73,"fcf_margin_pct":39.31,"rd_intensity_pct":25.11},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RMBS","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"688008.SS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.82,"operating_margin_pct":43.73,"fcf_margin_pct":42.26,"rd_intensity_pct":14.99},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.688008.SS","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MRVL","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.21,"operating_margin_pct":16.81,"fcf_margin_pct":18.23,"rd_intensity_pct":25.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"ARM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":97.54,"operating_margin_pct":17.3,"fcf_margin_pct":28.55,"rd_intensity_pct":57.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"SNPS","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.38,"operating_margin_pct":11.03,"fcf_margin_pct":29.18,"rd_intensity_pct":30.6},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNPS","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"RMBS"},"financial_history":{"ticker":"RMBS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":454793000.0,"revenue_yoy_pct":null,"gross_margin_pct":76.35,"operating_margin_pct":17.6,"net_income":-14310000.0,"diluted_eps":-0.13,"free_cash_flow":209915000.0,"fcf_margin_pct":46.16,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":461117000.0,"revenue_yoy_pct":1.39,"gross_margin_pct":77.57,"operating_margin_pct":19.84,"net_income":333904000.0,"diluted_eps":3.01,"free_cash_flow":172546000.0,"fcf_margin_pct":37.42,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":556624000.0,"revenue_yoy_pct":20.71,"gross_margin_pct":80.22,"operating_margin_pct":32.16,"net_income":179821000.0,"diluted_eps":1.65,"free_cash_flow":199902000.0,"fcf_margin_pct":35.91,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":707630000.0,"revenue_yoy_pct":27.13,"gross_margin_pct":79.59,"operating_margin_pct":36.77,"net_income":230455000.0,"diluted_eps":2.11,"free_cash_flow":333177000.0,"fcf_margin_pct":47.08,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/RMBS/RMBS_Q3_2026_Earnings_Call_20261026.md）

# Q3 2026 Earnings Call
**Rambus Inc.** | Earnings Calls | 2026-10-26

**Operator** (Operator):
Welcome to the Rambus Third Quarter Fiscal Year 2026 Earnings Conference Call. [Operator Instructions] As a reminder, this conference call is being recorded. I would now like to turn the conference over to Sumeet Gagneja, Chief Financial Officer. You may begin your conference.

**Sumeet Gagneja** (Executives):
Thank you, operator, and welcome to Rambus Third Quarter 2026 Results Conference Call. I'm Sumeet Gagneja, Chief Financial Officer at Rambus. On the call with me today is Luc Seraphin, our CEO. The press release for the results that we will be discussing today has been filed with the SEC on Form 8-K. We are webcasting this call along with the slides that we will reference during portions of today's call. A replay of this call will be available on our website beginning today at 5:00 p.m. Pacific Time.
Our discussion today will contain forward-looking statements, including our expectations for projected financial results and prospects, market growth, demand for our solutions and the potential effects of geopolitical and macroeconomic conditions. These statements are subject to risks and uncertainties that may be discussed during this call and are more fully described in our documents we file with the SEC, including our 8-Ks, 10-Qs and 10-Ks.
These forward-looking statements may differ materially from our actual results, and we are under no obligation to update these statements. In our press release and on the call today, we present both GAAP and non-GAAP financial measures to provide greater clarity regarding our financial performance.
A reconciliation of these non-GAAP financials to the most directly comparable GAAP measures has been included in our press release, in our slide presentation and on our website at rambus.com on the Investor Relations page under Financial Releases. The order of the call today will be as follows: Luc will begin with an overview of the business, followed by my review of the financial results, and then we'll open the call to Q&A. I will now turn the call over to Luc to provide an overview of the quarter. Luc?

**Luc Seraphin** (Executives):
Thank you, Sumeet. Good afternoon, everyone, and thank you for joining us. In Q3, we delivered a truly exceptional quarter. Revenue and non-GAAP earnings both reached new record highs and exceeded the top end of our guidance ranges. Strong customer demand fueled record product revenue and cash from operations, and we expect an even stronger product performance in Q4. We introduced new chip and silicon IP products that extend our leadership in data center and AI infrastructure.
In addition, as complexity and pace accelerate in semiconductor development for AI, we are also investing in the tools and infrastructure that will keep us on the leading edge of technology. As such, we engaged with a fellow pioneer in the ecosystem and announced an exciting new partnership that propels us into the age of AI agent-driven chip and IP design. As we continue to invest in our future, we are also pleased to have completed a $100 million accelerated share repurchase.
This demonstrates the strength of our business model and our ability to return value to our stockholders while advancing our product road map to drive long-term growth. Taken together, the results and progress we delivered this quarter reflect the strength and long-term resilience of a strategy we have pursued over many years, investing in technology leadership, anticipating the key trends transforming the data center and positioning the company to capture the opportunities those trends create.
Our strategy is producing strong results today, while at the same time, laying the foundation for future growth. As we outlined over previous quarters, AI continues to create strong tailwinds for Rambus across our businesses. As frontier AI training continues to advance and inference scales across a growing range of applications, customers require increasingly sophisticated memory and infrastructure architectures to move, manage and secure growing volumes of data.
Agentic AI is accelerating this trend as deployments evolve toward more distributed and heterogeneous architectures that require greater coordination across systems. At the same time, orchestration of always-on workloads puts greater demands on the CPU, lifting CPU to GPU ratios and driving requirements for more main memory bandwidth and capacity across the data center. The latest agentic implementations amplify this need even further by assigning dedicated compute and memory resources to individual users or agents.
All this creates accelerating demand for Rambus products and IP throughout the memory subsystem and across the broader infrastructure stack, while we continue to invest in the fundamental R&D and product road map required to address the ever-growing demand of memory management efficiency in the long run. Now let me turn to the quarterly results, starting with products. We delivered a new all-time high in quarterly product revenue, reaching approximately $114 million, up 15% sequentially and 22% year-over-year.
Our leadership in DDR5 RCDs and growing adoption of new generation products fueled our record results. We are seeing strong demand across multiple generations of RCDs, supporting our outlook for another record quarter of product revenue in Q4, which we expect to grow more than 30% year-over-year. Looking ahead, we have a strong pipeline of products aligned with upcoming platform ramps, positioning us well for next generation of server platforms.
As part of that pipeline, we are pleased to share that our sixth-generation RCD announced early in Q3, which supports DDR5 9600, is now sampling broadly with customers and is being very well received. We continue to execute successfully on our road map, recently expanding our product portfolio with an industry-leading PMIC for the upcoming LPDDR6 SOCAMM2. Earlier this year, we introduced our first SOCAMM2 chipset that supports LPDDR5X.
This new PMIC solution extends our server memory product road map to LPDDR6 and reinforces our leadership in advanced server memory power management. It was developed in close collaboration with customers and ecosystem partners to enhance memory subsystem power efficiency and help scale tokens per watt for AI workloads. We identified early on that power management would be critical to the success of AI deployments and have been investing in this area for many years.
We are proud of our progress and continued leadership in this space. We have consistently said that as memory speeds increase and server architectures become more sophisticated and heterogeneous, the memory subsystem will require additional intelligence, power management and control functionality. Our road map is designed to address this evolution across both DDR and LPDDR-based memory with timing management, power management and security management, creating opportunities for Rambus to participate in increasing module chip content over time.
In addition, DDR-based server platforms are expanding from 8 memory channels to 12 to 16 channels, increasing the maximum available memory bandwidth and capacity. This raises the number of modules supported in a server and amplifies demand as platforms progress. Today, Rambus offers complete chipsets across all major industry standard DDR5 and LPDDR server memory module architectures.
This broad portfolio positions us well for future server platforms and allows customers to leverage Rambus solutions across a growing range of memory architectures and deployment models. Looking ahead, we believe we are exceptionally well positioned for future server generations and for the continued expansion of memory-intensive AI infrastructure. Turning now to silicon IP. We delivered a very strong quarter with key design wins across our silicon IP portfolio.
The strength of those wins, combined with expanding strategic engagement across the industry, including custom silicon makers and hyperscalers, reinforces our confidence in the long-term growth opportunity for the silicon IP business and for Rambus. One of the defining characteristics of today's market is the rapid growth of custom silicon. The expansion of AI is fueling a new wave of custom silicon development.
Hyperscalers, AI infrastructure providers and emerging semiconductor companies are designing increasingly differentiated architectures and tailored silicon optimized for their own environments. These systems depend on advanced memory technologies, high-speed interconnects and trusted security, creating significant opportunities for Rambus silicon IP. During the quarter, we drove increasing ecosystem engagement and new Tier 1 design wins for next-generation HBM, supported by our deep architectural engagements ahead of standards being finalized.
We continue to see increasing interest in PCIe controller and switch IP for scale-up and scale-out connectivity solutions as customers seek higher levels of performance and efficiency across rapidly expanding AI infrastructure. The importance of bleeding edge IP continues to increase as customers pursue differentiated performance, power efficiency and time-to-market advantages.
As a result, we are engaging earlier in the architectural planning cycle with both our customers as well as our customers' customers and participating in a broader set of strategic programs. Leading edge memory and connectivity are fundamental to performance. And as AI infrastructure scales and becomes more heterogeneous, hardware-based security foundation is becoming fundamental.
Agentic AI relies on distributed computing architectures that execute workloads across multiple systems, which increases the available attack surface for adversaries, a growing concern in the current environment. As a pioneer and long-time leader in hardware-based security, Rambus IP solutions address that risk by providing a trusted foundation for the entire system and enhancing protection for valuable data and infrastructure.
Building on our industry-leading security offerings, we recently added a new root of trust solution designed specifically for AI and data center deployments that supports the Caliptra specification. Caliptra was developed by key leading technology companies to establish a common hardware security foundation for data center class SoCs and reflects the growing recognition that hardware-based security is essential for next-generation infrastructure.
Looking across both chips and silicon IP, we will continue to drive solutions that address the long-term foundation memory performance, high-speed connectivity and robust security demands of AI infrastructure. At the same time, we are harnessing AI to advance the underlying tools and development infrastructure that enable us to move faster, extend our leadership and scale the business more effectively.
As I mentioned at the beginning of the call, we recently announced a strategic investment and collaboration with ChipAgents, a fellow industry pioneer and leader in agentic AI design platforms. We see great opportunities to leverage the ChipAgents AI native design flows to accelerate our road map by speeding the pace of our chip and IP development, improving design quality and enhancing engineering productivity across our organization.
We believe this collaboration further strengthens our competitive position, both for products and for IP and reinforces Rambus's leadership role in next generation of AI data center infrastructure. In summary, the company delivered an exceptional third quarter, and we expect an even stronger Q4 as we continue to capitalize on the growing demand from AI.
We achieved record revenue and earnings while expanding our chip and IP offerings. And at the same time, we are investing in our development infrastructure to address the growing opportunities ahead. These results and decisions reflect the strength of our strategy and the continued alignment between Rambus technology and the most important trends shaping AI and data center infrastructure.
We are executing well and more importantly, we are continuing to invest for the future and build on a strong foundation of technology leadership and customer partnerships. We are confident in our trajectory, our road map and our ability to drive continued profitable growth in 2027 and beyond. As always, I want to thank our customers, partners and employees for their continued trust and support. And with that, I'll turn the call over to Sumeet. Sumeet?

**Sumeet Gagneja** (Executives):
Thank you, Luc, and good afternoon, everyone. We delivered an outstanding third quarter, achieving record revenue and earnings and record cash flow from operations. These results reflect the strength of our business model, growing demand for our products and technologies and disciplined execution across the company. Consistent with our balanced capital allocation strategy, we completed a $100 million accelerated share repurchase program during the quarter.
The transaction demonstrates our confidence in the business and our commitment to returning capital to shareholders while preserving the flexibility to invest in the growth. Looking ahead, we believe Rambus is well positioned to capitalize on the secular growth in AI infrastructure, data centers and advanced computing through the strength of our product and technology portfolio. With that, let me review our third quarter financial results.
Third quarter revenue was $218 million, driven by strong product and contract revenue. This represents growth of 22% year-over-year and 5% sequentially. Product revenue was $114 million, which is up 22% year-over-year and up 15% sequentially. Royalties revenue was $77 million. Contract and other revenue was $27 million, up 35% year-over-year and 13% sequentially. Contract and other revenue consist primarily of silicon IP.
As a reminder, only a portion of our silicon IP revenue is reflected in contracts and other revenue, and the remaining portion is reported in royalties revenue. Total non-GAAP operating costs, including cost of goods sold for the quarter, were $116 million. Operating expenses were $70 million, down sequentially due to slightly lower R&D and SG&A expenses. Interest and other income for the quarter was $7 million.
Using non-GAAP tax rate at 16%, non-GAAP net income for the quarter was $91.7 million, resulting in Q3 non-GAAP earnings per share of $0.84, which is up 35% year-over-year and up 10% sequentially. Now let me turn to the balance sheet details. We ended the third quarter with cash, cash equivalents and marketable securities of $777 million, down $48 million from Q2.
Record cash flow from operations of $102 million were offset by $135 million of share repurchases, including the $100 million accelerated share repurchase program. Capital allocation remains a key priority for us. We intend to continue investing in the business while returning 40% to 50% of free cash flows to shareholders over time, supported by our strong balance sheet and continued cash generation.
Our capital allocation approach reflects our focus on driving shareholder value while investing in our growth and pursue long-term opportunities ahead. We also leveraged the strength of our balance sheet to increase inventory by $12 million during the quarter, positioning us to support future product ramps and provide customers with greater supply assurance. Now let me turn to our non-GAAP outlook for the fourth quarter.
As a reminder, the forward-looking guidance reflects our best estimates at this time, and our actual results could differ materially from what I'm about to review. We expect fourth quarter revenue to be between $227 million and $233 million. Product revenue is expected to be between $127 million and $133 million. At the midpoint of the guidance, it is an increase of 34% year-over-year and an increase of 14% sequentially.
Royalties revenue is expected to be between $68 million and $74 million and contract and other revenue is expected to be between $26 million and $32 million. We expect Q4 non-GAAP total operating costs, which include cost of sales, to be between $124 million and $120 million. We expect Q4 capital expenditures to be approximately $8 million. Non-GAAP operating profit for the fourth quarter is expected to be between a profit of $103 million and $113 million.
We expect fourth quarter interest and other income to be approximately $6.5 million. Assuming a non-GAAP tax rate of 16% and 109 million diluted shares outstanding, we expect fourth quarter non-GAAP earnings per share to be in the range from $0.84 to $0.92. At the midpoint of the guidance, this represents growth of 30% year-over-year and 5% sequentially. Overall, we are very pleased with our third quarter performance.
Our record revenue, earnings and cash flow from operations demonstrate the breadth of our product and technology portfolio, the diversity of our revenue streams and the disciplined execution of our teams. The midpoint of our fourth quarter guidance implies that 2026 revenue will grow approximately 18% over 2025, including product revenue growth of approximately 24%.
With our continued focus on driving growth and operating efficiency, we expect non-GAAP earnings per share to grow approximately 24% over 2025. We remain focused on executing our strategy and capturing the opportunities created by AI infrastructure, data center and advanced computing markets. We are committed to translating these opportunities into sustainable growth, strong cash generation and long-term shareholder value. With that, I'll turn the call back to the operator for Q&A. Operator, could we have our first question, please?

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Kevin Garrigan with Jefferies.

**Kevin Garrigan** (Analysts):
Congrats on the results. Luc, so Q3 product revenue growth was 22% year-over-year. The Q4 midpoint implies about 34%. And I know you talked about strong growth across RCD generations, but can you give us a sense of how much growth is coming from other areas like companion chip ramps or any initial MRDIMM shipments?

**Luc Seraphin** (Executives):
Thanks, Kevin. Yes, we were really pleased with the results for Q3 and the growth for Q4, 34% year-over-year. We always saw that the second half of the year would be stronger than the first half of the year. I would say it's a combination of market demand going up and a lot of our products actually ramping into the market. The new generation of RCDs make the bulk of that.
At the beginning of the year, we said that our companion chips were approximately low double-digit percentage of our product revenue and that it would grow sequentially quarter-over-quarter. We see this happening. MRDIMM remains very modest, actually. We have shipped MRDIMM for Qual and preproduction this year. The AMD platform is starting to ramp. So it's still very modest. So we're really, really pleased with this 34% year-over-year growth based on the core, I would say, RCD and companion chips.

**Kevin Garrigan** (Analysts):
Okay. Great. And then as a follow-up, just on the MRDIMM opportunity. So the RCD playbook was always about being first to market and qualifying early. One of your competitors was designed for the first-generation MRDIMM platform. So what's different about this next generation that gives you confidence that you can take a leadership position?

**Luc Seraphin** (Executives):
The difference with MRDIMM is that it's associated with the launch of a platform that is very different than what we have all seen for the past few years. There's only one platform that is supporting MRDIMM now growing into the market. We don't know what the production of MRDIMM is going to be compared to the standard DIMM in that area. So it's going to be a ramp, and we're confident this ramp will happen. We still believe this is a great opportunity for us that we still size at $600 million in total.
But the ramp will be shallower, in our opinion, than the other generations of products simply because all of the platforms are not ramping at the same time. This is a new technology, and our customers have to adopt this technology and go through the initial stumbles. There's also this thing that we see in the market of memory de-specing. It's not that people decrease the number of modules, but they tend to decrease the capacity of each one of these modules.
So we do see a growth of the number of modules in the market that explains our growth in Q4. But we do see at the same time that each one of these modules tend to have lower capacity and it's due to the economics of the memory at this point in time. So between the memory economics, the stage ramp of the platforms and the introduction of new technology and supply associated with that, we see this as a great opportunity, but we see the ramp to be shallower than the standard ramp of an RCD product.

**Operator** (Operator):
Your next question comes from the line of Gary Mobley with StoneX.

**Gary Mobley** (Analysts):
Congrats on strong execution as we navigate through the second half of the year. Clearly, the second half of the year is playing out with seasonal strength on the product side as you had been communicating throughout the year. Based on what seems to be strong market environment and your existing backlog, how would you call out the seasonality of the first half of the year? Were you seeing something a little atypical, maybe slightly better than seasonal in the first half of the year? How do you see your visibility playing into the first half of the year on the product side?

**Luc Seraphin** (Executives):
Yes. So you're correct, Gary. The second half of the year, we have this seasonal effect that is advantageous to us. I would add to this for this year that I think we're really pleased with the execution. We do see our companion chip ramp in earnest, for example, a new generation being adopted at a higher rate than they used to be. When we look into 2027, I would say that we see demand strengthening.
I think this is not going down. So we're quite optimistic for 2027. The demand is strengthening. We have a better visibility into our backlog going into 2027. I think we're going to continue to see some sort of seasonality between the first half and the second half in 2027. But in aggregate, we are confident with the health of the demand growth in 2027.

**Gary Mobley** (Analysts):
As my follow-up, I wanted to ask about the silicon IP business. I think you've been communicating that this might be a $130 million annual business. I would assume that you're maybe trending above that. Can you confirm or give us any color on that?
And then with respect to custom ASIC development, do you see an opportunity, whether it be on high-speed SerDes interface IP, high-speed memory interface IP or security IP to forge a long-term development arrangement with some of the hyperscalers developing custom silicon, like what we've seen with some of the other competitors in the IP space?

**Luc Seraphin** (Executives):
Yes. So Gary, I'll start with the second question about the potential for silicon IP, and then I'll ask Sumeet to answer on the revenue and the revenue growth. We are engaging more and more with the ecosystem on the silicon IP because people are building more and more complex chips that require more and more complex integration and on the bleeding edge of technology. This is, for example, what we described in our last call with the engagement with a hyperscaler on next generation of memory.
So we see our confidence in the silicon IP keeps increasing. If you look at our product rollout, we talk about PCIe 7.0, IP PCIe 7.0 switch. HBM4, next generations of HBM, these dedicated security solutions for the data center. So we are engaged deeply with the ecosystem that gives us the opportunity going forward to potentially continue to increase our portfolio, not only organically but possibly inorganically and also to partner with our customers to develop broader system.
So as part of our thinking for silicon IP, we have that notion of working more and more with our partners on the system level. By the way, the announcement we made about agentic AI helps us do that. The ability to have agents work with us on integrating IP in much more complex systems is actually enabled by this type of things. So we're building the infrastructure to do that, that's the direction we are going into. It's going to take us time, but that is definitely a great trend for us. I'll let Sumeet answer on the numbers, yes.

**Sumeet Gagneja** (Executives):
Yes. Thanks, Luc. And just to add to that, Gary. So yes, so we've said our silicon IP business around $130 million, growing at 10% to 15%. But like Luc said, our confidence has been building throughout the year and 2026 has been a great year for our silicon IP business, along with the strong momentum in the design wins. So I would put it more like we're growing more towards the higher end of that range. We've said 10% to 15%, and we continue to make progress in all aspects from memory interface and security aspects.

**Operator** (Operator):
Your next question comes from the line of Sebastien Naji with William Blair.

**Sebastien Cyrus Naji** (Analysts):
Maybe first, I wanted to ask about the LPDDR6 PMIC that you announced. Could you maybe give us a sense for how that increases your dollar content per module versus the SOCAMM2 content that you had announced in April? I think it was 2 voltage regulators and an SPD hub. And then when do you expect maybe some initial revenue for that product?

**Luc Seraphin** (Executives):
Thanks, Sebastien. I would say that I'll be a bit discreet about the exact content on this SOCAMM2 because it's not -- the final spec has not been released yet. So I'd rather wait for the final spec to be released. But what I can say is that when you move from the first version of SOCAMM that we announced earlier this year to this new generation of SOCAMM2, the content is increasing. The power management is more complex. And as a result of that, the dollar content is going to increase from that first generation to that second generation. 
The module performance itself is going to be much better as well, which will, I would say, trigger adoption at a higher level. But as every one of these SOCAMM solutions, they provide a very good solution for these areas of AI where power performance is really, really important. But this is a small portion of the market, and that's going to be continuing -- that's continued to be the case between the first version of SOCAMM2 and the SOCAMM2. The SOCAMM2 will hit the market probably in 2028. 
And the way to look at it is we see the development of the AI infrastructure as having multiple horizons for us, if you wish. We want to make sure that we develop those solutions way ahead of the market. And when they deploy in the market, then we are present with solutions that work. This is what we've done in the past that explains, for example, our performance in Q4 this year that are based a lot on the products we developed in the past. They had little traction at the beginning, but they're starting to show revenues in Q4 of this year. 
This is going to be the same with SOCAMM. SOCAMM is going to address a niche portion of the AI stack, AI infrastructure. But the adoption of LP is going to happen. It's not going to happen fast. It's not going to be the same content as the current content of standard memory. But it's important for us to have that as part of our portfolio while we help our customers and ecosystem partners to deploy their solutions in the market.

**Sebastien Cyrus Naji** (Analysts):
Great. Okay. That's very helpful. And then maybe my second question or my follow-up for Sumeet on gross margins. It looks like non-GAAP product gross margins were about 60.4% in Q3. That's on the lower end of the, I think, 60% to 63% near-term range that you gave us.
Could you maybe give us a sense for how much of the gap here is mix in terms of just more companion chip revenue, next-generation RCDs with early yields versus how much of it is wafer substrate or OSAT cost inflation? And then how should we think about Q4 product gross margins? Do they stay in that lower 60% area? Or can they move up a little bit?

**Sumeet Gagneja** (Executives):
Yes. Thanks for the question, Sebastien. Yes. So our gross margin historically has been this tight band, 60% to 63%. And you're right, in the Q3 was slightly above 60%. Our long-term target remains, which is 60% to 65%. In the near term, it's really the margin trending towards the lower end is primarily driven by the supply chain input cost. And we've been very successful in offsetting that cost input cost by driving internal cost savings and keeping our product gross margin in the range of 60% to 63% in the near term.
Q4, it's the same sort of the setup going into Q4, but the investments and the cost reductions we have done especially in our operations side, there may be a slight uptick in the gross margin in Q4, but it's not material, but it's still within the 60% to 63%. On a full year basis, it's more important to look at from the gross margin perspective. We expect 2026 to be right in the middle of that 60% to 63% range.

**Operator** (Operator):
Your next question comes from the line of Mark Lipacis with Evercore.

**Mark Lipacis** (Analysts):
I had 2. I was hoping you could just talk about lead times from your own suppliers and any -- to the extent that you're seeing tightening supply on the front end or the back-end foundry business? And then can you talk about lead times to your customers? And are there any stretching of lead times to your customers from you? And any indication that your customers downstream or the supply chain downstream is increasing their own inventories given how tight everything seems to be becoming?

**Luc Seraphin** (Executives):
Thanks, Mark. I'll start and let Sumeet comment. I would say that on the supply side, we do see lead times increasing. We signaled this 2 calls ago. We were expecting this. But because we were expecting this, we also put in place plans to mitigate for that. So we lever our strong balance sheet to actually build inventory on products that we believe are going to grow substantially with our customers, and we're in constant relationship with our suppliers to make sure that we use our balance sheet to make sure that we can supply to our customers.
So yes, definitely longer lead times on the supply side, but it has not impacted our Q3 number, and it will not impact the Q4 number that we just talked about. So we've been able to manage that, but we have to continue to do that. Our lead times, the first approximation, our lead times to our customers have not increased at this point in time. But you understand that we are in constant discussions with them as well.
The whole chain is tightening. The good thing is our business is very focused. We have very strong partnerships with our customers, and we work with them in making sure that we can supply what they need. In summary, longer lead times on the supply side, we are using our balance sheet to deal with that. And at this point in time, we've not increased our lead times to our customers.

**Mark Lipacis** (Analysts):
And just to be clear, do you have the ability to see if customers or customers' customers downstream are increasing their inventories? Or is that like a black box to you and it's really hard to determine?

**Luc Seraphin** (Executives):
It's very hard to determine. We see -- what we see is that people place backlog earlier than what they used to a quarter ago or 2 quarters ago. I think everyone understands the current situation. So we have better visibility in the backlog. But at the same time, that gives us more opportunity to have a deeper, I would say, relationship with our customers. Once we understand the profile of their backlog, then it's easier to work with them on how we can lead that backlog. So we don't see people building inventory, but we see people placing backlog.

**Operator** (Operator):
Your next question comes from the line of Tristan Gerra with Baird.

**Tristan Gerra** (Analysts):
So if I heard well, you mentioned that your revenue in the quarter and the guidance is not constrained by supply. So it probably provides a little bit of an easy comp relative to the first half where you did face some supply issues. What's your level of confidence that you can actually meet the accelerating demand that you described into next year?
And I know you're not guiding beyond this quarter, but do you think that the acceleration that you're seeing in product revenue year-over-year is sustainable? Or do you see supply as an issue again next year? And is there any talk about longer-term agreements or anything that customers are trying to set up to ensure supply from here?

**Luc Seraphin** (Executives):
So we see demand -- thank you, Tristan. We see demand strengthening into next year, and we started to work with our supply chain partners to meet what we believe is going to be required. In all honesty, this is something that we work on almost on a weekly basis. We try all avenues to support our customer base. So demand is strong going into 2027. Supply will remain tight.
But as I said, as we did in 2026, we're working early with our supply base to look at every knob we can turn to support our customer demand. That's how we look at this. The good news is that the demand for the products we have in our portfolio is strong. The demand for CPUs, this CPU to GPU ratio is going in our favor. It's known from our customers all the way down to our suppliers, and we'll do our best to supply that growing demand into 2027.

**Tristan Gerra** (Analysts):
Great. And then as a quick follow-up, I wanted to explore the difference in content opportunity medium term for x86 CPU and stand-alone Vera and kind of come up with maybe a 4x content in x86 CPU for you versus what you would get on the SOCAMM2 side with -- but are you quantifying at all what the opportunity is and the difference that you see in terms of opportunities on the x86 and the Arm-based side of CPUs next year and the years beyond?

**Luc Seraphin** (Executives):
Yes. Thank you, Tristan. The way we look at it and the reason we are excited about this AI infrastructure deployment is that we look at this in an aggregate way. There are areas of AI like if you take the head nodes, for example, where SOCAMM and LP memory can be used. It's not always used, but it can be used. And that's an opportunity for us from a technology standpoint. It allows us to develop our LP technology on all fronts.
But in aggregate, you do have a growth in these head nodes that will create an opportunity for SOCAMM. But you have higher growth in the traditional servers with a refresh necessary in order to continue to develop the range of applications, or range of standard applications, we have higher growth in agentic, standard CPUs as well for orchestration, tools management, memory management.
So in aggregate, if you take the head nodes where you can have SOCAMM and if you take the standard servers and the agentic server, the whole market is growing. But the majority of the growth is coming from CPUs with standard memory subsystems. So that's the way we look at it. We definitely don't look at this as SOCAMM is cannibalizing the market for standard DIMM. It's actually complementary.
It makes the system more efficient. The standard memory subsystems are going to increase at a higher pace going into 2027. And the head nodes will drive new technologies like SOCAMM to maximize this kind of application. So we see this as complementary, and that's why we want to have solutions for all of that.
We really want to be agnostic to the memory subsystems while the infrastructure for AI is growing in the market because as that infrastructure is growing in the market, we're going to see heterogeneous systems, and it's important that we have solutions for each one of those. But the vast majority is going to continue to be CPU with standard DIMM configurations.

**Operator** (Operator):
Your next question comes from the line of Kevin Cassidy with Rosenblatt Securities.

**Kevin Cassidy** (Analysts):
I'll echo the congratulations on a great quarter. Just -- it's interesting, as you mentioned about the custom chips and that you're getting involved earlier into the design cycle. And I'm just wondering if -- any way, does this help you to win more modules on those designs as they come into production?

**Luc Seraphin** (Executives):
Thanks, Kevin. We're really excited with these silicon IP engagements with the ecosystem because they give us great insight into the architectural trends that these people are talking about. When we talk to hyperscalers with the opportunity for us to sell our silicon IP, we have insights into some of the architecture problems they're trying to resolve and where they see the world going.
And as a consequence of that, that helps us develop -- continue to develop the right road map of products for these types of products. But it also gives us insight as to the overall architecture of their systems and where DIMM are going to be used, where LP is going to be used and why, what generation of DDR is going to be used and why.
It just gives us that channel of information. It's almost through the discussion, and it gives us a good sense of the trends in terms of what type of technologies they are going to use, not only on the silicon IP side, but also in terms of how they will configure their systems with different types of modules.

**Kevin Cassidy** (Analysts):
Right. And it seems like a big advantage over your 2 competitors that don't have IP story. And maybe just on the inventory one more time. Are you comfortable with the days of inventory now? Or should we expect to see that continue to increase even with the increasing demand next year?

**Sumeet Gagneja** (Executives):
Yes, Kevin, good question. So inventory, as you mentioned, we've been growing inventory this year. In Q3, we grew it again $12 million, again, primarily leveraging the strength of our balance sheet to make sure we provide greater assurance to our customers. In Q4 as well, looking at just like Luc mentioned throughout the call, like we have more visibility into the backlog. And as demand is accelerating, we do plan to build or increase inventory even in Q4, similar level to like we built in Q3 and Q2.

**Operator** (Operator):
At this time, there are no further questions. This concludes the question-and-answer session. I would like to turn the conference back over to the company for closing remarks.

**Luc Seraphin** (Executives):
Thank you to everyone who has joined us today for your continued interest and support. We look forward to speaking with you again soon. Thank you.

**Operator** (Operator):
Thank you. This concludes today's conference. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### RMBS_Q2_2026_Earnings_Call_20260727.md
- 2026-07-27｜Sumeet Gagneja (CFO)｜guidance：CFO 給 Q3 總營收財測區間 2.10–2.16 億美元（原話："third quarter to be between $210 million and $216 million."）
- 2026-07-27｜Sumeet Gagneja (CFO)｜guidance：CFO 給 Q3 產品營收財測 1.10–1.16 億美元，中點季增 14%（原話："$110 million and $116 million, a sequential increase of 14% at the midpoint of guidance."）
- 2026-07-27｜Sumeet Gagneja (CFO)｜guidance：CFO 給 Q3 權利金營收財測 6,900–7,500 萬美元（Q2 實際為 8,420 萬）（原話："royalties revenue to be between $69 million and $75 million"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜guidance：CFO 給 Q3 非 GAAP EPS 財測 0.75–0.82 美元（原話："non-GAAP earnings per share range between $0.75 and $0.82."）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 表示下半年將強於上半年，並維持逐季給財測、不給一季以後（原話："our second half is going to be stronger than our first half"）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 說明財測僅逐季提供（原話："but we will continue to guide quarter-by-quarter."）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 表示矽智財業務維持年增 10%–15%（原話："we continue to see that business growing 10% to 15% a year"）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 表示 MRDIMM 於 Q4 貢獻極小，較實質貢獻在 2027（原話："The contribution for Q4 is going to be minimal."）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 指出 MRDIMM 較實質貢獻發生在 2027 平台放量時（原話："contribution is going to happen in 2027 when both platforms from the CPU guys"）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 表示新產品占產品營收比重預計到 Q4 底達中雙位數百分比（原話："And that's going to be in the mid double digits"）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 說明 Q3 產品營收年增幅度與本季相近（原話："Next quarter, we're going to see the same growth"）
- 2026-07-27｜Luc Seraphin (CEO)｜margin：管理層重申毛利率長期模型 60%–65%，並表示季間會波動（原話："Our model remains 60% to 65%"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜margin：CFO 指出近期毛利率落在 60%–63%（原話："we've been operating in the 60% to 63% gross margin"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜margin：CFO 宣布此後財報與財測只以 ASC 606 營收口徑呈現，不再揭露授權帳單（billings）（原話："guidance on an ASC 606 revenue basis going forward."）
- 2026-07-27｜Sumeet Gagneja (CFO)｜margin：CFO 報告 Q2 營收 2.074 億美元（原話："Revenue for the second quarter was $207.4 million"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 表示 Q2 無產能問題（同時提到供應鏈緊俏、交期拉長）（原話："we didn't have any capacity issue in Q2"）
- 2026-07-27｜Luc Seraphin (CEO)｜commitment：CEO 表示公司想維持或提高 DIMM 市占（標準品無漲價空間）（原話："maintain or continue to increase our share in the DIMM market."）
- 2026-07-27｜Luc Seraphin (CEO)｜commitment：CEO 表示產品投資將集中於標準品，而非 CXL 類客製 ASIC 產品（原話："we'd rather invest into standard products at this point in time."）
- 2026-07-27｜Sumeet Gagneja (CFO)｜commitment：CFO 表明其工作重點之一為審慎配置資本（原話："allocate capital thoughtfully"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜capital_allocation：CFO 報告期末現金及有價證券 8.25 億美元，較 Q1 增加 3,900 萬（原話："marketable securities totaling $825 million, up $39 million from Q1"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜capital_allocation：CFO 說明 Q2 存貨增加 1,600 萬美元，用於支援產品放量與供貨保證（原話："Inventory increased by $16 million during the quarter"）
- 2026-07-27｜Luc Seraphin (CEO)｜capital_allocation：CEO 說明公司對關鍵產品建立策略性庫存（原話："We build strategic inventory for the"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜capital_allocation：CFO 報告 Q2 自由現金流 4,900 萬美元（原話："Free cash flow in the quarter was $49 million."）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 表示 2027 年供應限制仍將存在（原話："the supply constraints will continue to be there in 2027."）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 表示對需求假設有信心，但對平台時程與供應採審慎態度（原話："we are prudent with respect to platform timing and supply"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 指出平台放量歷來比外界預期慢（原話："platform ramps typically take a little bit"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 回答客戶端無過度備貨跡象（原話："We don't see any signs of our customers building inventory"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 表示標準品沒有漲價空間（原話："we don't see any opportunity, I would say, for"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：新任 CFO 在本次法說首度亮相（原話："welcome Sumeet Gagneja to his first earnings call"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 提到 Q1 曾有製造問題，仍年增 15%（原話："despite the manufacturing issue we had, it was 15% higher"）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 說明新產品目前占產品營收低雙位數百分比（原話："were in a low double-digit percentage of the product revenue."）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 表示 LPDDR/SOCAMM 短期營收貢獻有限，但策略重要性高（原話："the short run is modest, but the strategic importance is really high for us."）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 認為產業並未轉向 LPDDR，LPDDR 屬增量機會（原話："I wouldn't say that the industry is shifting to LPDDR."）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 說明 MRDIMM 模組上的矽含量為 4 倍（原話："MRDIMM with 4x the silicon content on the module"）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 說明 PCIe 7.0 授權收入在未來幾季出現，不需等終端產品放量（原話："in the coming quarters, because it's a licensing business"）
- 2026-07-27｜Luc Seraphin (CEO)｜competition：CEO 描述 CXL 產品市場呈客製 ASIC、分散化（原話："a custom ASIC business that is fragmented for us"）
- 2026-07-27｜Luc Seraphin (CEO)｜competition：CEO 回應 CXMT：記憶體廠商都需與 Rambus 簽授權（原話："has to have a license agreement with us"）
- 2026-07-27｜Luc Seraphin (CEO)｜competition：CEO 表示伺服器單位成長預期由中高個位數升至雙位數，公司自認成長快於市場（原話："Now it's double-digit growth."）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 揭露與一家美國一線超大規模雲端業者的下一代 HBM 設計案（原話："an exciting design win with a Tier 1 U.S. hyperscaler"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 確認該設計案為 IP 而非晶片產品（原話："It's an IP design win"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 說明該 IP 為授權模式而非按量計價（原話："it's a license or multi-license"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 表示超大規模雲端業者在定義自家架構上角色日增（原話："hyperscalers are playing a growing role"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 表示對需求的信心持續增加（原話："I think our confidence is continuing to build."）

### 問答異常語氣（迴避／改口／保留）
- RMBS_Q2_2026_Earnings_Call_20260727.md｜問：Gary Mobley 問 Q4 能見度與上季相比如何｜答法：CEO 說信心增加，但未給 Q4 具體數字，改談 Q3 年增與逐季給財測
- RMBS_Q2_2026_Earnings_Call_20260727.md｜問：Tristan Gerra 問 2027 年成長是否能高於 20%｜答法：CEO 稱不給一季以後的財測，只列正面需求因素並強調供應與平台時程審慎，未給成長數字
- RMBS_Q2_2026_Earnings_Call_20260727.md｜問：Mehdi Hosseini 問拉高市占是否使產品毛利率停在 60% 初段｜答法：CEO 與 CFO 未直接回答取捨，重申 60%–65% 長期模型並說季間波動、宜看年度

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
{"date":"20260620","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"RMBS 守住 DDR5 RCD co-leader 份額並把領先延伸至 MRDIMM/HBM4","columns":{"2Y 驗證點":"RCD 份額維持 mid-40%；MRDIMM 2026 量產","5Y 驗證點":"HBM4/MRDIMM 成為 product 主要成長源","10Y 驗證點":"不被 Montage 在新一代奪份額","具體數字門檻":"RCD 份額 ≥ 40%；product 年成長 ≥ 15%","信息來源":"Rambus 法說（2026-04-27）+ 產業數據","漂移觸發條件":"product 連 2 季 QoQ 下滑或份額 &lt; 40% → 削弱"}},{"id":"H2","text":"AI 伺服器記憶體內容量價齊升，TAM 從 RCD $800M 擴至 $2B+","columns":{"2Y 驗證點":"MRDIMM + companion chips TAM 開始貢獻","5Y 驗證點":"HBM4/CXL 內容成為新成長曲線","10Y 驗證點":"記憶體介面晶片 TAM 持續擴張","具體數字門檻":"buffer 市場 CAGR ~35%；MRDIMM late 2026 ramp","信息來源":"產業報告（buffer 市場 $866M, CAGR 34.8%）","漂移觸發條件":"MRDIMM/HBM4 ramp 延後 2+ 季 → 削弱"}},{"id":"H3","text":"市場願意給 RMBS 成長溢價倍數（非壓回歷史授權公司倍數）","columns":{"2Y 驗證點":"FY+2 Fwd PE 維持 &gt; 25x","5Y 驗證點":"PEG 隨成長兌現回落至 &lt; 1.5","10Y 驗證點":"RMBS 估值定錨在 AI 記憶體 25-30x","具體數字門檻":"Fwd PE &gt; 25x 持續","信息來源":"§13 歷史分位 + 同業","漂移觸發條件":"Fwd PE 跌破 22x + EPS 共識下修 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Montage 在 MRDIMM/HBM4 新一代搶下份額","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"RCD/MRDIMM 份額、design-win 公告","警戒閾值":"RCD 份額 &lt; 40% 或 MRDIMM 落後 Montage"}},{"id":"R2","text":"DRAM/伺服器記憶體週期回落（庫存修正）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"product 季度 QoQ、DRAM 廠 capex/庫存","警戒閾值":"product 連 2 季 QoQ 下滑"}},{"id":"R3","text":"記憶體架構演進壓縮獨立介面晶片價值（近記憶體運算 / 內建控制）","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"次世代記憶體架構路線圖","警戒閾值":"主要 DRAM/CPU 廠推內建介面方案（需 ≥50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":141.17,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
