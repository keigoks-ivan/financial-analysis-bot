你是 stock-analyst **v20 判斷 agent**，標的 LEU（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"LEU","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":55.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）"},"note":"查無（未取得可核實的季度共識）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income (loss)","value":-24.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）"},"note":"查無（未取得可核實的季度共識）"},{"id":"f_kpi2_gaap_operating_income_lo","label":"GAAP operating income (loss)","value":-29.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）"},"note":"查無（未取得可核實的季度共識）"},{"id":"f_kpi3_gross_profit_loss","label":"Gross profit (loss)","value":-10.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）"},"note":"查無（未取得可核實的季度共識）"},{"id":"f_kpi4_gaap_net_income","label":"GAAP net income","value":31.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）"},"note":"查無（未取得可核實的季度共識）"},{"id":"f_kpi5_free_cash_flow_derived","label":"Free cash flow (derived)","value":-126.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）；Q2 8-K https://www.sec.gov/Archives/edgar/data/0001065059/000162828026053433/ex991-10q2026_08x05.htm（上半年累計值）"},"note":"查無（未取得可核實的季度共識）"},{"id":"f_kpi7_cash_and_cash_equivalent","label":"Cash and cash equivalents","value":2236.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）"},"note":"查無（未取得可核實的季度共識）"},{"id":"f_kpi8_total_backlog","label":"Total backlog","value":7.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）"},"note":"查無（未取得可核實的季度共識）"},{"id":"f_kpi9_guidance_fy2026_revenue","label":"Guidance FY2026 revenue","value":"450–500","period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）"},"note":"查無（未取得可核實的季度共識）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_leu_gross_margin_pct","label":"LEU 毛利率","value":23.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEU.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_leu_operating_margin_pct","label":"LEU 營業利益率","value":-1.25,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEU.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_leu_fcf_margin_pct","label":"LEU FCF 利潤率","value":-65.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEU.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ccj_gross_margin_pct","label":"CCJ 毛利率","value":25.49,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CCJ.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ccj_operating_margin_pct","label":"CCJ 營業利益率","value":14.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CCJ.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ccj_fcf_margin_pct","label":"CCJ FCF 利潤率","value":10.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CCJ.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_uec_gross_margin_pct","label":"UEC 毛利率","value":45.36,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UEC.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uec_operating_margin_pct","label":"UEC 營業利益率","value":-357.65,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UEC.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uec_fcf_margin_pct","label":"UEC FCF 利潤率","value":-288.16,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UEC.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bwxt_gross_margin_pct","label":"BWXT 毛利率","value":22.61,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWXT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bwxt_operating_margin_pct","label":"BWXT 營業利益率","value":9.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWXT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bwxt_fcf_margin_pct","label":"BWXT FCF 利潤率","value":10.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWXT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi6_sbc_adjustment_sg_a_and_","label":"SBC adjustment (SG&A) and % of revenue","value":1.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）"},"note":"查無（未取得可核實的季度共識）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":104.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-49.55,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":42.42,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.7 → 3.7）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.44 → 4.44）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.73 → 3.73）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.7,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":4.44,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.73,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":7.56,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 3.44 → 3.7（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":31.04,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝36.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":36.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.75,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝28.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":28.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.42,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝8.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":8.1,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":28.27,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 3.7，分子＝快照價 104.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-1057.3,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 1178.8、現金 2236.1（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":20.62,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":1099.39,"period":"2026-11-08","unit":"USD m","basis":"市值 2156.69 ＋ 淨負債 -1057.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":476.09,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":503.04,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.31,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 104.6 / W52 196.58 / W104 176.23 / W250 97.82 / W250 13週斜率 0.98%"},{"id":"f_ma_w52","label":"52 週均線","value":196.58,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":176.23,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":97.82,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.98,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Centrus 全球 LEU 濃縮份額不到 5%；前四大供應商（Rosatom/TENEX、Urenco、CNEIC、Orano）合計逾 95%，競爭對手皆為外國政府持有。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"Our global market share of enrichment for the LEU market is less than 5%. Global LEU suppliers in our highly competitive industry compete on the basis of price and reliability of supply. The four largest LEU suppliers comprising over 95% of market share combined are as follows:","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"2026-01-05 DOE 宣布 LEU 與兩個 HALEU 任務單各 9 億美元給三家公司；Centrus 子公司 ACO 取得一個 HALEU 單，但未獲 LEU 生產任務單。","source":"Centrus 10-Q／8-K FY2026（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001065059/000162828026046801/leu-20260630.htm","excerpt":"On January 5, 2026, the DOE announced one LEU and two HALEU task order awards to three companies for $900 million each, including one $900 million task order to Centrus subsidiary, ACO, under the HALEU Production Contract.","as_of":"2026-07-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"BWXT 揭露將申請新濃縮設施執照；UBS 預期競爭壓力在 2030 年代後期累積；General Matter 在肯塔基設濃縮廠（搜尋摘要，未核原文）。","source":"Yahoo Finance: UBS Flags Competitive Headwind for Centrus Energy; Energy Intelligence","url":"https://finance.yahoo.com/news/ubs-flags-competitive-headwind-centrus-134849930.html","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K 揭露客戶集中度：前十大核燃料客戶占 2025 營收約 77%，前兩大客戶約 31%；客戶多為長約，流失後難以重新取得。未見最大客戶導入第二供應商或自製的揭露。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"In 2025, our ten largest nuclear fuel customers represented approximately 77% of total revenue and our two largest customers represented approximately 31% of total revenue.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025年前十大核燃料客戶占總營收約77%，前兩大客戶約31%；客戶減購或財務狀況變化可能影響業績。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"In 2025, our ten largest nuclear fuel customers represented approximately 77% of total revenue and our two largest customers represented approximately 31% of total revenue.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2025年客戶A/B/C/D分別占總營收約16%/15%/13%/11%；2024年客戶A 20%、B 13%；單一最大客戶占比由20%降至16%。","source":"SEC EDGAR 10-K FY2025 Note 19","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"Revenue from Customers A, B, C, and D represented approximately 16%, 15%, 13%, and 11%, respectively, of total revenue for the year ended December 31, 2025.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"公司依各客戶財務狀況評估授信並定期監控信用風險；搜尋未見2026年客戶破產或信用降評事件。","source":"SEC EDGAR 10-K FY2025 附註（信用風險集中）","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"Extension of credit is based on an evaluation of each customer’s financial condition. Centrus regularly monitors credit risk exposure and takes steps intended to mitigate the likelihood of such exposure resulting in a loss.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"WNA 燃料報告：新礦開發期由 8–15 年拉長到 10–20 年；現有礦產 2030 後十年約減半，需新礦與重啟；短期礦端供給足夠","source":"World Nuclear News: Investment decisions needed to avoid fuel cycle supply gaps","url":"https://world-nuclear-news.org/articles/fuel-cycle-players-respond-to-supply-gaps","excerpt":"the time to develop new mines is actually getting longer, not shorter","as_of":"2025-09-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"同來源：全球濃縮供給至少到 2030 年代初期仍超過需求（對濃縮廠商偏負面的供需說法，與 LEU 管理層『供需失衡擴大』說法並存）","source":"World Nuclear News: Investment decisions needed to avoid fuel cycle supply gaps","url":"https://world-nuclear-news.org/articles/fuel-cycle-players-respond-to-supply-gaps","excerpt":"supply exceeds demand through to at least the early 2030s","as_of":"2025-09-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"WNA 2025 Nuclear Fuel Report：2030 年反應爐鈾需求較現在高約 28%，2040 年前年複合成長 5.3%（前版 4.1%）；2027–2028 無 WNA 官方數字","source":"Mining Weekly: Uranium demand set to surge 28% by 2030, WNA says","url":"https://www.miningweekly.com/article/uranium-demand-set-to-surge-28-by-2030-as-nuclear-power-gains-momentum-wna-says-2025-09-05","excerpt":"Global uranium demand is expected to soar as nuclear power cements its role in the clean energy transition","as_of":"2025-09-05","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Centrus 2026 Q2 公告：LEU/HALEU 濃縮 backlog 達 30 億美元（24 億已 definitized），總 backlog 45 億美元延伸至 2040；CEO 稱濃縮供需失衡擴大、公告 LEU 價格續升；DOE 9 億美元 HALEU 獎助支持首批新產能約 2029 年上線（皆為公司自述）","source":"Centrus Energy 8-K Q2 2026 earnings release / MarketBeat Q2 call highlights","url":"https://www.marketbeat.com/instant-alerts/centrus-energy-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"部落格/行銷類來源多稱鈾缺口為結構性（2026 初級供給缺口約 3,100 萬磅 U3O8，需求 2.04 億磅 vs 礦產 1.73 億磅）；來源品質低，作者不明，數字未經一手核對","source":"Skillings: Uranium market outlook 2026 widening supply gap","url":"https://www.skillings.net/uranium-market-outlook-2026-widening-supply-gap-and-long-term-contracting-dynamics/","excerpt":"Primary Reactor Demand 204 Million lbs U₃O₈; Primary Mine Production 173 Million lbs U₃O₈; Global Supply Deficit 31 Million lbs U₃O₈","as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"經查搜尋結果未見 Centrus 面臨反壟斷（DOJ/FTC）調查；其 10-Q 將俄羅斯 LEU 進口豁免、Graham Act 制裁/關稅、Piketon 租約（2027-10-01 到期）列為監管風險。","source":"搜尋摘要（針對 SEC 10-Q 2026-09-30 的彙整）","url":"https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070557/leu-20260930.htm","excerpt":"The search didn't turn up any antitrust, DOJ, or FTC scrutiny of Centrus Energy.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"俄羅斯 TENEX 供貨受制裁、關稅、出口管制與俄方法令影響；加拿大運輸許可證延至 2027 年 3 月，進一步限制可能對業務造成重大負面影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"A Canadian permit issued to our shipper was extended to March 2027, but for so long as the sanctions remain in place, the shipper will require further extensions beyond the current validity of the permit for continued shipments of LEU imports.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國於 2025-09-08 取消鈾進口關稅；國會另有對俄貨物課重稅草案；關稅可能增加設備成本，也可能提高美國產鈾需求。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"On September 8, 2025, the U.S. officially removed import tariffs on uranium as part of a broader executive order aimed at strengthening domestic supply chains and supporting strategic industries. However, there is draft legislation in the U.S. Congress designed to impose potentially significant tariffs on Russian goods.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Section 232 關鍵礦物（含鈾）調查後，2026-01-14 公告 11001 要求 180 天談判，視結果可能再考慮加徵部門關稅。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"Proclamation 11001 indicated that, depending on the status or outcome of those negotiations, alternative remedies may be considered in the future, including the imposition of an additional sectoral tariff.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026 年 10-Q 稱至 2027 年預計交付客戶的 LEU 逾半來自 TENEX 合約；未承諾量的豁免是否核准不確定（搜尋摘要，未讀頁面）。","source":"SEC EDGAR 10-Q Q3 2026（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070557/leu-20260930.htm","excerpt":"through 2027, well over one-half of the LEU that we expect to deliver to customers was sourced under the TENEX Supply Contract","as_of":"2026-09-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Centrus 依賴與俄羅斯 TENEX 的供應合約履行交貨義務，10-Q 自述此依賴為重大風險","source":"Centrus Form 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070557/leu-20260930.htm","excerpt":"The two parties agreed to extend the agreement through 2040 and to set aside a significant portion of the quota for Centrus’ shipments to the United States through 2028 to perform under our TENEX Supply Contract.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"DOE 2024 年豁免僅涵蓋已承諾對美國客戶的交貨；2026-2027 未承諾交貨的豁免決定被延後","source":"World Nuclear News / mining.com","url":"https://www.mining.com/web/centrus-gets-waiver-on-uranium-imports-from-russia/","excerpt":null,"as_of":"2024-07-19","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 LEU segment revenue $31.8M vs $44.8M (-29%), attributed to contract mix shift; total revenue $55.5M vs $74.9M; contingent LEU+HALEU enrichment backlog $5.4B","source":"Centrus Q3 2026 results (SEC 8-K ex99.1 / oilprice coverage)","url":"https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 SWU average price +10%, volume +19%; LEU segment revenue down 29%","source":"Centrus Reports Third Quarter 2026 Results","url":"https://finviz.com/news/416081/centrus-reports-third-quarter-2026-results","excerpt":"Revenue from the LEU segment was $31.8 million and $44.8 million for the three months ended September 30, 2026 and 2025, respectively, a decrease of $13.0 million or 29%.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"WNA 2025 Nuclear Fuel Report: reactor uranium demand >150,000 tU by 2040, upper case 204,000 tU","source":"World Nuclear News","url":"https://www.world-nuclear-news.org/articles/nuclear-fuel-report-sees-upward-trend","excerpt":"a series of reports published by World Nuclear Association and its predecessor organisation the Uranium Institute at roughly two-yearly intervals since 1975. Launched in London today at World Nuclear Association Symposium 2019, it includes three scenarios - designated Reference, Upper and Lower - covering a range of possibilities for nuclear power to 2040.","as_of":"2019-09-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"DOE does not currently plan to exercise further options under HALEU operation contract; FY2027 budget omits HALEU cascade funding","source":"Centrus Q2 2026 earnings call highlights (MarketBeat)","url":"https://www.marketbeat.com/instant-alerts/centrus-energy-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"GLE 雷射濃縮（SILEX）：NRC 於 2025-08 受理完整執照申請，2026-03 發布 EIS 草案，首次商業生產目標約 2030 年；2026-01 DOE 選定其最高 2850 萬美元獎助。雷射法被稱有效率與成本潛力，但數十年來未在全球達商業規模。","source":"搜尋摘要彙整（ANS、Energy Intelligence、SMR Intel）","url":"https://www.ans.org/news/article-7652/doe-awards-27b-for-haleu-and-leu-enrichment","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Centrus 取得 DOE 9 億美元 HALEU 濃縮任務單，Piketon 擴建以離心機技術進行；2026-01-05 DOE 宣布，需待最終協議談判，無資金保證。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"On January 5, 2026, the DOE announced that ACO was awarded a $900.0 million task order to expand its uranium enrichment facility in Piketon, Ohio, to include commercial-scale production of HALEU under the HALEU Production Contract.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 財報電話會：商業積壓訂單 45 億美元（至 2040），含約 30 億美元待條件的 LEU/HALEU 濃縮銷售，其中 24 億美元已有正式協議","source":"MarketBeat Centrus Energy Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/centrus-energy-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 8-K（2026-11-04）：FY2026 營收指引 4.5–5 億美元、資本投入 3.5–5 億美元；公司稱更新部分指引，但未列前次數字，唯一明示變動為 Piketon 招聘由 100 提高到至少 175 人","source":"SEC 8-K Ex.99.1 Centrus Q3 2026 results","url":"https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm","excerpt":"Total revenue to be in the range of $450 million to $500 million","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026 調整後每股虧損 0.46 美元，遠差於共識約 -0.13（二手摘要）；營收約 5,550 萬美元，與預期約 5,520 萬相近；GAAP 獲利來自認股權證負債重估利益 4,640 萬","source":"247wallst / oilprice 對 Q3 2026 的報導（搜尋摘要）","url":"https://247wallst.com/cards/centrus-energy-q3-2026-earnings-leu-01m6m7spt5xjjztyrtph8ya99a","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價共識依來源與日期分歧：Tickflow（2026-08-03）10 位分析師 Hold、均價約 229.17 美元；Investing.com 約 207、Benzinga 約 216、Pricetargets 約 259（後三者未標日期）；高點 390（Evercore ISI，2026-01），Citi 2026-05 目標 218","source":"Tickflow／MarketBeat／Investing.com／Benzinga 聚合（搜尋摘要）","url":"https://www.tickflow.io/stock/LEU/forecast","excerpt":"The consensus among 10 analysts covering Centrus Energy Corp. (LEU) is Hold with an average price target of $229.17.","as_of":"2026-08-03","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-16 Centrus 以約 1.16 億美元（現金 9,500 萬、股票 2,100 萬）收購 Westerman Holdings 100% 股權，Westerman 成為全資子公司。","source":"SEC EDGAR 8-K（Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026066212/leu-20261016.htm","excerpt":"The aggregate purchase price for the LLC Interests was approximately $116.0 million (“Purchase Price”), which was paid by the Company $95.0 million in cash, and $21.0 million in shares (the “Stock Consideration Shares”) of the Company’s Class A common stock","as_of":"2026-10-19","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"2026-06-30 子公司 ACO 與 DOE 簽訂固定價格 9 億美元的 HALEU 濃縮產能合約，2032 年 3 月前交付。","source":"SEC EDGAR 8-K（Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026046801/leu-20260630.htm","excerpt":"The Contract establishes a firm fixed price of $900 million, to be paid incrementally as performance-based milestone payments, to deploy a specified amount of enrichment capacity and deliver, by March 2032, one metric ton of uranium (MTU) enriched as HALEU UF6","as_of":"2026-07-02","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026-09-09 公司與 Guggenheim 簽承銷協議，發行 50 萬股普通股、預融資認股權證（最多 2,005,513 股）及普通認股權證（最多 6,992,382 股），有稀釋效果。","source":"SEC EDGAR 8-K（Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1065059/000110465926107103/tm2625019d5_8k.htm","excerpt":"providing for the offer and sale of (i) 500,000 shares (the “Shares”) of the Company’s Class A common stock, par value $0.10 per share (the “Common Stock”), (ii) pre-funded warrants to provide for the purchase, upon exercise, of up to 2,005,513 shares of Common Stock","as_of":"2026-09-11","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露 McGlone 等人 2019 年起對 Centrus 等 DOE 承包商提起的 Portsmouth 場址外污染集體訴訟仍在進行。","source":"SEC EDGAR 10-K FY2025（Note 17 Legal Matters）","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"On May 26, 2019, the Company, Enrichment Corp., and six other DOE contractors who have operated facilities at the Portsmouth GDP (including, in the case of the Company, the American Centrifuge Plant site located on the premises) were named as defendants in a class action complaint filed by Ursula McGlone","as_of":"2026-02-11","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"-","claim":"2025-12-01 8-K 含 Item 3.01（上市規則未達標通知）；近 12 個月共 20 份 8-K，其中 14 份含重大項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001065059&type=8-K","excerpt":"2025-12-01 8-K Items 3.01 Notice of Delisting or Failure to Satisfy a Listing Rule；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits","as_of":"2025-12-01","retrieved_at":"20261108","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Urenco USA 現行 70 萬 SWU 擴建：2026 年 6 月底前五組 cascade 上線，2027 初再三組；另一座 210 萬 SWU 新廠預計 2029 動工、2032 首產（搜尋摘要轉述，未核原文）","source":"ANS / Urenco USA news (2026-06)","url":"https://www.ans.org/news/2026-06-02/article-8085/urenco-to-add-21-million-swu-of-enrichment-capacity-at-its-new-mexico-plant/","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Orano Georges Besse II 由 7,500 擴至 10,000 tSWU/y，預計 2028 起生產；Urenco Almelo 2030 前升至約 6,600 tSWU/y（二手來源轉述）","source":"fissilematerials.org, Plans to expand the enrichment capacity","url":"https://fissilematerials.org/blog/2026/06/plans_to_expand_the_enric.html","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Centrus 自家新增產能預計 2029 年上線；2026-10-29 第一支新離心機出貨至俄亥俄，早於年底目標；DOE 9 億美元 HALEU 任務單（10-Q/8-K）","source":"Centrus 8-K 2026-10-29 / 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001065059/000162828026068047/ex991_firstcentrifuge.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Kazatomprom 2026-11-03 維持 2026 全年指引不變：100% 基準產量 27,500–29,000 tU，礦業實體資本支出 KZT 435–450bn（摘要轉述）","source":"Quartr Kazatomprom Q3 2026 trading update","url":"https://quartr.com/events/national-atomic-company-kazatomprom-jsc-kzap-q3-2026-tu_F3ACbZuh","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Urenco USA 擴建過半、第四組 cascade 上線","source":"Urenco USA news","url":"https://www.urenco.com/news/uusa/2026/urenco-usa-reaches-half-way-point-of-current-u.s-capacity-expansion","excerpt":"Urenco USA Reaches Half-Way Point of Current U.S. Capacity Expansion 02 April 2026 UUSA Urenco USA has completed installation and startup of its fourth new cascade of gas centrifuges at its uranium enrichment facility in New Mexico, marking the half-way point of its current U.S.","as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"TradeTech 長約價指標 2026-10-31 達 US$99.00/lb，為 1996 年系列開始以來最高；9/30 為 96.50；現貨約 US$89.9（10/15）、9 月底 89.63，長約高於現貨","source":"Crux Investor - Record US$99 uranium contract price","url":"https://www.cruxinvestor.com/posts/record-us-99-uranium-contract-price-favors-miners-with-supply-left-to-sell","excerpt":"US$99 Uranium Contract Price Favors Miners Yet to Sell 2030s Output Record US$99 Uranium Contract Price Favors Miners Yet to Sell 2030s Output November 3, 2026 Ryan Charles Share: Uranium’s long-term contract price hit a record US$99/lb, but older contracts delay gains. Miners with supply left to sell into the 2030s stand to benefit most. Example H2 Example H3 Example H4 TradeTech's","as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"EIA 2025 鈾行銷年報：美國商業庫存 2025 年底 170 百萬磅（2024 年 156），電廠持有 118 百萬磅、供應商 51 百萬磅","source":"Crux Investor - Rising uranium inventories buy time","url":"https://www.cruxinvestor.com/posts/rising-uranium-inventories-buy-time-but-new-mines-typically-need-15-20-years","excerpt":"EIA reported 170 million pounds of US commercial uranium inventory at year-end 2025, up from 156 million pounds in 2024.","as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"Centrus 2026 Q3 業績（11/4）：營收 55.5 百萬美元（去年同期 74.9）、LEU 部門 31.8 百萬、調整後淨損 9.4 百萬","source":"Centrus Q3 2026 results (SEC 8-K ex99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm","excerpt":"Centrus generated total revenue of $55.5 million and $74.9 million for the three months ended September 30, 2026 and 2025, respectively, a decrease of $19.4 million or 26%. Revenue from the LEU segment was $31.8 million and $44.8 million for the three months ended September 30, 2026 and 2025, respectively, a decrease of","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"EIA 資料：鈾現貨 2016 年由 1 月 $34.65/lb 跌至 11 月 $17.75/lb，為 2004 年 5 月以來最低月均價；2016–2020 平均低於 $25/lb；美國鈾精礦產量 2014–2016 年減少 40%。","source":"U.S. EIA, Today in Energy (id=31772)","url":"https://www.eia.gov/todayinenergy/detail.php?id=31772","excerpt":null,"as_of":"2017-01-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"現貨自 2007 年 6 月高點約 $135/lb 起大致下行；2011 年福島前高點約 $73，其後跌逾一半，2016 年底跌至約 $18（較 2011 年 3 月低約 70%），低迷歷時約 5–9 年（依起點 2011 或 2007）。","source":"Bloomberg via republicofmining / Business Day: World's worst commodity is radioactive for investor portfolios","url":"https://republicofmining.com/2017/01/09/worlds-worst-commodity-radioactive-for-investor-portfolios-by-joe-deaux-natalie-obiko-pearson-and-klaus-wille-bloomberg-news-january-6-2017","excerpt":null,"as_of":"2017-01-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Centrus 上一輪下行期：2016 全年毛利 $45.1M／營收 $311.3M，毛利率 14.5%（2015 為 16.5%、毛利 $68.9M），淨損 $67.0M；2017 上半年毛損 $6.8M（2016 同期毛利 $21.3M），2017 全年毛利回升至 $56.8M，其中 contract services 毛損 $2.5M。","source":"Centrus Energy 10-K FY2016 / FY2017 and 8-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001065059/000106505918000006/leu-20171231x10k.htm","excerpt":null,"as_of":"2018-03-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Centrus 2016 毛利 $45.1M、14.5%","source":"Centrus 8-K Mar 2017","url":"https://centrusenergy.gcs-web.com/node/16446","excerpt":null,"as_of":"2017-03-28","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-16 Centrus 以約 1.16 億美元收購 Westerman Holdings 100% 股權（現金 9,500 萬＋股票 2,100 萬）。","source":"SEC EDGAR 8-K（Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026066212/leu-20261016.htm","excerpt":"As a result of the Acquisition, Westerman is a wholly owned subsidiary of the Company.\nThe aggregate purchase price for the LLC Interests was approximately $116.0 million (“Purchase Price”), which was paid by the Company $95.0 million in cash, and $21.0 million in shares","as_of":"2026-10-19","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"McGlone 等人 2019 年起的 Portsmouth 污染集體訴訟仍列於 FY2025 10-K；搜尋未見證券詐欺集體訴訟。","source":"SEC EDGAR 10-K FY2025（Note 17 Legal Matters）","url":"https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm","excerpt":"The McGlone Plaintiffs are seeking to represent a class of (i) all current or former residents within a seven-mile radius of the Portsmouth GDP site and (ii) all students and their parents at the Zahn’s Corner Middle School from 1993-present.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"LEU","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.28,"operating_margin_pct":-1.25,"fcf_margin_pct":-65.02,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEU","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CCJ","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.49,"operating_margin_pct":14.35,"fcf_margin_pct":10.31,"rd_intensity_pct":1.48},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CCJ","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"UEC","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.36,"operating_margin_pct":-357.65,"fcf_margin_pct":-288.16,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UEC","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"BWXT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":22.61,"operating_margin_pct":9.83,"fcf_margin_pct":10.34,"rd_intensity_pct":0.44},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWXT","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"LEU"},"financial_history":{"ticker":"LEU","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":293800000.0,"revenue_yoy_pct":null,"gross_margin_pct":40.13,"operating_margin_pct":20.49,"net_income":52200000.0,"diluted_eps":3.38,"free_cash_flow":19900000.0,"fcf_margin_pct":6.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":320200000.0,"revenue_yoy_pct":8.99,"gross_margin_pct":35.01,"operating_margin_pct":16.36,"net_income":84400000.0,"diluted_eps":5.44,"free_cash_flow":7500000.0,"fcf_margin_pct":2.34,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":442000000.0,"revenue_yoy_pct":38.04,"gross_margin_pct":25.23,"operating_margin_pct":10.86,"net_income":73200000.0,"diluted_eps":4.47,"free_cash_flow":32900000.0,"fcf_margin_pct":7.44,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":448700000.0,"revenue_yoy_pct":1.52,"gross_margin_pct":26.19,"operating_margin_pct":11.19,"net_income":77800000.0,"diluted_eps":3.9,"free_cash_flow":31300000.0,"fcf_margin_pct":6.98,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/LEU/LEU_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Centrus Energy Corp.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Good morning, ladies and gentlemen, and welcome to the Centrus Energy Q3 2026 Earnings Conference Call. [Operator Instructions] This call is being recorded on Thursday, November 5, 2026.
I would now like to turn the call over to Mr. Neal Nagarajan, Senior Vice President, Investor Relations. Please go ahead.

**Neal Nagarajan** (Executives):
Good morning. Welcome, and thank you to all of our callers, as well as those listening to our webcast. Today's call will cover the results for the third quarter 2026, ended September 30.
Today, we have Amir Vexler, President and Chief Executive Officer; and Todd Tinelli, Senior Vice President, Chief Financial Officer and Treasurer.
This conference call follows our earnings news release issued yesterday. We have filed our report for the third quarter on Form 10-Q earlier today. All of our news releases and SEC filings, including our 10-K, 10-Qs, and 8-Ks, are available on our website. A replay of this call will also be available later this morning on the Centrus website.
I would like to remind everyone that certain information we may discuss on this call today may be considered forward-looking information that involves risks and uncertainty, including assumptions about the future performance of Centrus. Our actual results may differ materially from those in our forward-looking statements. Additional information concerning factors that could cause actual results to materially differ from those in our forward-looking statements is contained in our filings with the SEC, including our annual report on Form 10-K and quarterly reports on Form 10-Q. The forward-looking information provided today is time-sensitive and accurate only as of today, November 5, 2026, unless otherwise noted. Please note that we report results using non-GAAP financial measures, which we believe provide investors with additional understanding of the company's financial performance as well as its strategic financial planning, analysis, and period-to-period comparability. A reconciliation to the most directly comparable GAAP measurements is included in the Financial Results section of our earnings release.
This call is the property of Centrus Energy. Any transcription, redistribution, retransmission, or rebroadcast of the call in any form without the expressed written consent of Centrus is strictly prohibited. Thank you for your participation.
I'll now turn the call over to Amir. Amir?

**Amir Vexler** (Executives):
Thank you, Neal, and thank you all for joining us today. I am happy to report that Centrus is continuing to build its reputation on meeting its commitments, growing its credibility, which is leading us to capturing more market share. We made significant progress during the third quarter across our commercial, operational, and financial objectives, capped off by the recent completion of our first centrifuge in Oak Ridge, Tennessee, ahead of our year-end target.
We now proved that U.S. centrifuge manufacturing is a reality. It is a historic milestone for Centrus and the United States. This landmark occasion was the culmination of a number of other achievements by the team, including the strategic acquisition of one of our key suppliers, Westerman. This marks us officially locking in all of the suppliers we deem critical while also completing our first certified for construction packages to additional 2026 operational targets we have achieved ahead of our year-end target.
Furthermore, we grew our enrichment backlog from $3 billion to $5.4 billion, and successfully raised funds in a prudent manner that keeps us well capitalized. Finally, we are excited to announce that we are now using the existing 16 centrifuge cascade to enrich HALEU for the commercial market, making Centrus the first U.S.-owned commercial enricher for the market since our gases diffusion space.
And against this backdrop, we see continued and growing commercial validation across all three of our addressable markets: commercial LEU for the existing commercial nuclear reactor fleet for baseload electricity; a growing national security imperative that continues to increasingly diversify; and HALEU to support the next-generation reactors that will also require LEU feedstock. It is important to distinguish Centrus' unique opportunity set from those of the broader nuclear market. We are positioned to capitalize on all three of these markets.
First and most importantly, our primary focus is on baseload electricity from contracts with investment-grade utilities. There is a significant existing and growing gap in commercial LEU supply and demand. And remember, much of our long-dated enrichment backlog that runs through 2040 is for LEU to service these existing investment-grade utilities.
The second addressable market is for growing national security needs. A recent U.S. GAO report raised the alarm on the nation's entire domestic nuclear fuel supply chain, in particular, the domestic supply chain suitable to meet national security demand. Notably, the report highlighted the government's $37 billion plan to rebuild the unobligated supply chain by 2052.
As announced last week, we have confirmed that our supply chain is fully unobligated. Centrus' proven derisked technology is additionally the only production-ready option for the national security establishment. In this light, we continue to work with the NNSA on its intent to sole source certain uranium enrichment activities from Centrus and stand ready to support this important mission. And then there is the HALEU and advanced reactor market. This market's demand represents an incremental growth opportunity that continues to mature.
We have positioned ourselves to capitalize on this potential market if and when it matures to provide ourselves with further optionality. This optionality includes our flexibility to use planned HALEU capacity for various assays of LEU and LEU+, if needed. And importantly, we are securing prepayments to fund our expansion from the HALEU offtake agreements we are signing. And yet durable LEU demand for investment-grade reactor operators is what we're primarily focused on.
We continue to observe this gap between supply and demand widen, driven by updates, mothballed facilities coming back online and potential new builds, both in the U.S. and abroad. This widening disparity is demonstrated by the continually increasing spot and long-term contract LEU pricing curves that continue their upward trajectory.
Let me now dive into the progress we made against our three objectives. First, turning to our operations. We could not be more excited about last week's event in Oak Ridge, Tennessee, to celebrate our first centrifuge's completion, marking the beginning of our ramping of scaled centrifuge manufacturing. This important milestone achieved well ahead of our year-end target demonstrates that we have successfully stood up our core manufacturing operations in Oak Ridge, including having qualified our process that are tested and proven. The team is now focusing on decreasing the cycle times and increasing throughput rates, reducing inefficiencies and scaling up our infrastructure alongside our supply chain while hiring and training employees.
Furthermore, we are very excited about our recent acquisition of Westerman, which should drive growth for both organizations through commercial and operational synergies as well as cost savings while derisking our build-out. The acquisition represents a significant milestone for Centrus.
In one strategic move, we have simultaneously derisked our build-out by securing a key supplier and best-in-class manufacturer of centrifuge casing and other critical components; captured cost savings synergies related to Westerman's expansion and tied to our expansion; and derisked our entire business model in the near- and medium-term with an established, high-quality industrial fabricator manufacturer with revenues in nuclear and non-nuclear industries.
Second, turning to commercial backlog. We saw material growth in the third quarter, growing our enrichment backlog to $5.4 billion in contingent LEU and HALEU sales commitments. Our announced agreements with X-energy, Radiant and Antares all included prepayments to support our build-out. Furthermore, our agreement with X-energy includes production of LEU as a feedstock for HALEU, helping us push more volume through our facility. And finally, our offtake agreements with Radiant and Antares further validate and reinforce our first-mover advantage in the microreactor market. They also demonstrate our ability to produce unobligated enriched uranium that can also support U.S. national security applications, including defense and space missions.
And finally, on the third pillar, financial progress, Centrus secured an additional $500 million with the potential addition of $2 billion in the future. To this end, Centrus ended the quarter with roughly $2.2 billion of unrestricted cash on our balance sheet. Todd will discuss this in more detail shortly.
Now moving on to guidance. We are reaffirming our 2026 annual guidance for total company revenue of $450 million to $500 million as well as our annual capital spend of $350 million to $500 million. We are similarly reaffirming our 2026 annual guidance for Piketon workforce additions to over 175 new hires as well as our target of new employees at Oak Ridge to at least 100.
With us now having finalized contracts with 100% of the partners we deem critical, we were able to complete and begin shipping our first centrifuge. Our acquisition of Westerman represents another important step in further strengthening our supply chain. We have simultaneously completed our first certified for construction package for Piketon. We will discuss these in more depth at our upcoming Investor Day this coming December.
With that, I will turn the call over to Todd, and return with some final thoughts and comments. Todd?

**Todd Tinelli** (Executives):
Thank you, Amir, and good morning to everyone on today's call. Ahead of walking through our results, I want to first quickly discuss the impact of our recent capital raise. In the third quarter, we recognized a $46.4 million book gain due to a decrease in the liability associated with the valuation of the warrants from our recent capital raise. This was a noncash impact on our books, but led to a $46.4 million positive impact to the quarter's operating income, net income, and earnings per share that is not part of our due course of business. As such, throughout my comments, the operating income, net income and earnings per share, excluding the $46.4 million gain, will be referred to as normalized as well as those same adjusted figures that account for growth costs.
Our normalized results were in line with our internal projections and reflected the typical quarter-over-quarter shift in contractual mix that can transpire based on customer orders and deliveries. Our strong financial execution continues to support the execution of our multibillion-dollar domestic enrichment expansion. As noted on previous calls, I will be presenting financials on a quarterly and trailing 12-month basis.
Total revenue for the third quarter was $55.5 million, a decrease of $19.4 million or 26% versus the same period last year. TTM revenue was $454.5 million, ahead of fiscal 2025 revenue. The LEU segment generated $31.8 million in revenue in the third quarter, a 29% decrease versus the same period last year. SWU revenue in the quarter increased by $3.4 million due to a 19% increase in volume of SWU sold and a 10% increase in the average price of SWU sold. The Technical Solutions segment revenue was $23.7 million in the third quarter, a $6.4 million or 21% decrease over the same period last year, due primarily to a $10.2 million decrease in revenue generated by the HALEU operations contract as well as a change related to other contracts.
Centrus generated a loss of $10.6 million and a gross profit of $105.8 million for the third quarter and TTM, respectively, compared to a gross loss of $4.3 million in Q3 2025.
The LEU segment's third quarter cost of sales was $38.7 million, a decrease of $13.9 million or 26% over the previous year's period, driven by a decrease in the volume of uranium sold. SWU costs increased as a result of a 28% increase in the average unit cost of SWU sold and a 19% increase in the volume of SWU sold. Technical Solutions cost of sales of $27.4 million increased $0.8 million or 3% from Q3 2025, primarily attributable to an increase in costs related to customer contracts, partially offset by a $1.7 million decrease in costs incurred under the HALEU operation contract.
Normalized operating loss for the third quarter was $25.1 million compared to a loss of $16.6 million in the same period last year. The company generated normalized net loss of $10.2 million and $9.4 million of adjusted net loss in the third quarter compared to normalized net income of $3.9 million and adjusted net income of $5.2 million, respectively, in Q3 2025. The change in third quarter normalized net loss was primarily attributed to a decrease in income tax benefit of $9 million, an increase in gross loss of $6.3 million and an increase in advanced technology costs of $3 million. This change in normalized net loss was partially offset by an increase of $4 million in investment income. On a fully diluted basis, this equates to third quarter 2026 normalized loss per share of $0.49 and adjusted loss per share of $0.46, respectively, compared to $0.19 and $0.25, respectively, in Q3 2025.
On a trailing 12-month basis, Centrus generated normalized net income of $34.4 million and adjusted net income of $77.3 million, respectively. Third quarter adjusted net income excludes $2.4 million of gross expenses and a $1.3 million benefit to our SG&A related to our stock compensation, which combined and tax adjusted equates to $800,000. Please refer to our Financial Results section of our earnings release issued yesterday for a reconciliation of net income, normalized net income and adjusted net income. Going forward, we continue to expect to have certain level of these types of growth expenses to flow through our income statement as we continue to build out.
Centrus' backlog across both segments grew to $7 billion at the end of the third quarter and extends out to 2040. The growth was driven by an approximate $2.4 billion in LEU and HALEU enrichment sales in the LEU segment. Of the approximate $5.4 billion in contingent LEU and HALEU sales commitments, $5.1 billion are under definitive agreements.
Turning to our capital spend, which are CapEx and non-CapEx attributed to costs and investments such as prepayments to suppliers or growth costs. In the third quarter, we had total capital spend of $134 million with $131.6 million coming from CapEx and the remainder coming from non-CapEx growth costs. We finished the third quarter with approximately $2.2 billion in unrestricted cash without using our ATM.
In September, we completed an approximately $500 million underwritten public offering of Class A common stock and prefunded warrants together with accompanying common warrants. This important transaction allowed us to access near-term capital at a premium while setting the company up for significant future capital in four future tranches with progressively higher excess prices only if our share price appreciates and we continue to execute against our milestones. If exercised in full, the warrants could provide approximately $2 billion of additional gross proceeds with exercise prices ranging from approximately $2.27 to $3.63 per share. We believe this structure reflects investor confidence in the long-term value of Centrus while providing additional financial flexibility.
We continue to feel confident in our existing cash balance, and we believe we are sufficiently funded to meet our near-term capital requirements.
Subsequent to quarter-end, we acquired Westerman for approximately $116 million, funded through a combination of cash on hand and equity, including $95 million in cash and $21 million in equity. We expect the acquisition to lower project costs for Centrus and drive greater efficiencies across our supply chain.
Turning to our outlook for the remainder of 2026. As Amir noted, we are reaffirming our annual guidance for revenue of $450 million to $500 million and total capital spend of $350 million to $500 million. The target excludes the Westerman acquisition. We look forward to having a more fulsome conversation about Westerman build-out at our upcoming December Investor Day. We are simultaneously reaffirming our operational guidance for the workforce additions in Piketon and Oak Ridge.
With that, I will turn the call back to Amir. Amir?

**Amir Vexler** (Executives):
Thank you, Todd. I am proud of the progress we made during the third quarter across our commercial, operational, and financials broadly. We have made significant progress in and are continuing to derisk our build-out. We are now beginning to manufacture and ship centrifuges from our Oak Ridge facility. We have locked in 100% of the suppliers we deem critical and have completed our first CFC package. We have significantly grown our commercial enrichment backlog. We are sitting on a healthy cash balance that empowers our buildup. We have furthermore bolstered and derisked our business profile, especially in near-term revenues and profitability with our recent Westerman transaction. And all of our progress is happening as our addressable market continues to grow, a strong backdrop that supports our expansion.
We are also excited to host our upcoming Investor Day on December 7, at our American Centrifuge Plant in Piketon, Ohio. We look forward to sharing more about our strategy and build-out at that event.
With that, I will turn the call over to the operator for questions. Operator?

**Operator** (Operator):
[Operator Instructions] Your first question comes from Mark Shooter from William Blair.

**Mark Shooter** (Analysts):
Amir, I just had a question on the first centrifuge. So the first centrifuge production, that's a big milestone for the company and also national security. But a key point for us on that front was that these new centrifuges are unobligated. And I was hoping you could give us some update on the engagement with the NNSA and speaking to the funding be outlined from the GAO as well.

**Amir Vexler** (Executives):
Yes. Well, good morning Mark, thank you for that good question. I'll remind the listeners and yourself that one of the great values that we bring to the market and the technology that we bring to the market is the capability to have unobligated production that can serve national security needs. Just as a reminder as well in form of background, in November of 2025, the NNSA published a notice-of-intent to issue Centrus, a sole-source contract for the production of certain low enriched uranium that's suitable for use in support of the national security mission. So that is sort of the backdrop to our needs and our drive to have unobligated production.
And specifically to your question, our production will be unobligated. And we have been working to configure the supply chain, working with all our suppliers to make sure that that is going to be implemented.
I hope I answered the question, Mark.

**Mark Shooter** (Analysts):
Yes, thank you, Amir. I thought they cut me off for the next question. Thank you.

**Operator** (Operator):
Your next question comes from Mark Bianchi from TD Cowen.

**Esteban Mario Albarracin** (Analysts):
This is Esteban Albarracin on for Mark Bianchi. My question is really around the current LEU backlog. I know you mentioned excluding the LEU to HALEU contract, is that all tied to the existing reactor fleet? I ask because I'm trying to understand the opportunity for new light water reactors there and there's 10 new large reactors moving through the DOE EDF loan program. So I'm trying to think how should we think about the timing of potential LEU backlog opportunities for Centrus there if enrichment RFPs could follow relatively soon for new reactors or would utilities likely weigh closer to a reactor startup?

**Amir Vexler** (Executives):
Good morning. Let me just talk maybe in general, and then we'll address specifically the question about the new build. We very much are excited and are obviously prioritizing firm and -- firm commitments from customers, and the ones for LEU are typically the ones that are able to make those in large numbers. So a good size -- a large part of our backlog is LEU for operating reactors here in the United States and abroad as well.
Specifically, to the question of how to think about the new reactors that are yet to be built, it really is a question to them as to at what point they would feel they would need to go out and secure fuel supply. I think based on what we're seeing the advanced reactors do, they do prioritize fuel supply, and they put that right at the front to ensure that they derisk their projects. I would expect that the new builds, whether it's going to be AP1000s or whatever other large reactor design is going to be, there's going to be tremendous need for enrichment supply as well.
I would tend to think that in today's markets and some of the availability and some of the long cycles around capacity expansion of enrichment, I would absolutely encourage them to put that at the very front of their planning cycle as they plan to expand. And so we absolutely intend to compete for it, and we intend to make that a big part of our business as well.

**Operator** (Operator):
Your next question comes from Joseph Osha from Guggenheim Securities.

**Peyton Durand** (Analysts):
This is Peyton Durand on for Joe Osha this morning. I guess could you just provide a little bit more color on what enabled the accelerated time line for the first completed centrifuge? And do you see this time line as sort of replicable for future units? And I guess the third part, what learnings are you going to take from this first one to apply to nth of kind?

**Amir Vexler** (Executives):
Okay. Thank you for the question. I think I've been very consistent on all of our calls in trying to explain and emphasize to the investors how critically important it is for us to gain market credibility, to be able to meet and exceed our commitments. We have an incentive to -- from the market, we have an incentive to beat the timelines that we have advertised. And so organizationally, we are creating the same incentives and the same expectations of exceeding, meeting the timelines. But more specifically, what enabled is we do run process improvement teams in parallel. I mean, one example that I gave before, which I'm sure we'll get to talk about at some point from -- I'm sure a question will come up about our partnership with Palantir and some of the work we're doing there.
So we really are attacking this on multiple fronts, and we're doing a lot of progress with our supply chain and all of this with the intent of expediting, lowering cost, derisking. Westerman is another example of derisking and building efficiencies into our supply chain. And I'm sure there will be a question on that as well at some point.
So the lessons learned here is that when you align the goals in the organization, provide the tools, expectations and make a proper investment in rapid improvements, it pays off, and we certainly intend to implement those learnings. And these are coincidentally to your second part of your question. These really are the learnings -- and we certainly are looking forward to providing a more wholesome update details and examples at our Investor Day that I've announced earlier. And hopefully, that answers the question.

**Operator** (Operator):
Your next question comes from Nate Pendleton from Texas Capital.

**Nathaniel Pendleton** (Analysts):
Congrats on the continued progress. Amir, I wanted to go back to the strong macro picture that you alluded to in your prepared remarks. With the strong SWU pricing relative to uranium, as we look ahead, how are customers changing tails of say, if at all? And how much Western SWU demand could be met with overfeeding as we look out in the future?

**Amir Vexler** (Executives):
Great question. So you're asking an enrichment person about a question that involves a lot more consideration than just enrichment. Obviously, uranium pricing fits into this very strongly. Each customer and supplier approached this question individually on a contract-by-contract basis. In the past, obviously, when SWU prices were cheap, this goes back a few years ago, we've seen a different behavior around tails assay. We've seen a different behavior around underfeeding versus overfeeding. Obviously, that dynamic has changed now that SWU prices have gone up considerably. And I would expect that this continues to be just an optimization for each contract, case by case, as to how they view their uranium supply pricing versus how they want to optimize it versus enrichment.
I will add as a final thought that I would tend to give the upper hand here to enrichment. By that, I mean, I think ultimately, you would see the seesaw pendulum swing towards sort of erring on the side of favoring enrichment capacity is just because I don't see that there is that much ability to expand capacity as quickly as the market grows. I mean, we're seeing that disparity now, and I think it will take a while before that disparity sort of settles. So I think you will see that reflected in the tails and in the overfeeding versus underfeeding. I hope that answers the question.

**Operator** (Operator):
Your next question comes from Bill Peterson from JPMorgan.

**William Peterson** (Analysts):
Nice job on the quarterly execution. I wanted to ask a follow-up on a prior question on the backlog. So I guess we think about your commercial strategy, is there a preferred mix of, I guess, existing utilities, say LEU versus newer companies, SMR? And I guess with the shape of the backlog, you talked about backlog going up to 2040. Is that more front-loaded or back-loaded? I'm just trying to get a sense of what that could mean for implication on CapEx as you, I guess, continue to grow your backlog.

**Amir Vexler** (Executives):
Yes. Thank you for that question. I'll start off by just saying that it would be -- we typically do not break down and separate the amounts. That said, the vast majority of our backlog is LEU-- it's either for LEU customers or its feedstock for future HALEU offtake.
Now you asked a pretty interesting question as to who do we favor and who do we like more. That would be a dangerous answer to give. I'll give you the pros and cons. And obviously, we want both and we pursue both. The established LEU customers provide a lot of certainty. They provide a lot of volume. They provide very, very solid terms to be able to offtake. And that is precisely what we need when we are expanding facilities -- expanding our facilities and investing capital. However, I do not want to, in any way, underestimate the HALEU customers who just in the last 6 months, a year have become a lot more committed to the supply chain, and we're seeing them being able to make sort of take-or-pay type contracts and legally binding contracts.
They provide a huge promise to a company like ours. If there is a large expansion of any of these SMRs or microreactors, if there is a large build-out, that's going to create a substantial need for HALEU and an exponential need for LEU. And so we honestly are trying to keep our finger on both triggers. And I will just remind the investors and listeners as well that the third leg of the stool here is we are pressing really hard on national security. We position ourselves to be able to serve the needs when called upon for national security. And I hope that, that gives you enough detail that I answered the question, Bill.

**Operator** (Operator):
Your next question comes from Nick Amicucci from Evercore ISI.

**Nicholas Amicucci** (Analysts):
Well, you opened the door, so I'll allow you to either walk through it or close it on me. Just wanted to kind of dig into the $300 million of Palantir potential savings. And basically how much represents validated procurement or engineering changes versus the opportunities that are still under evaluation? And should we think of any of those as an accelerant to capacity delivery?

**Amir Vexler** (Executives):
Yes. Good question, Nick. As previously communicated, a day 1 focus for us is to really maximize cost savings while we really are bringing in lead times and deployment times for our expansion. We want to use state-of-the-art technology tools, capability, individuals -- and hence, the reason for the partnership. We did announce amount of savings that we put out there, and then you quoted $300 million. A lot of it has been a strong contributor to our capability to deliver ahead of schedule.
From where I sit, and I'm fairly connected to the project, I think that most of the opportunities and most of the potential savings and value we're going to derive is still ahead of us, so much so that we are in active mode of learning as to what we achieved and how we potentially accelerate and expand that. So stay tuned for more announcements. Stay tuned for more information.
And as one of the answers that I gave earlier, we do intend to have a much more wholesome conversation on this in our Investor Day. This really is the purpose for such conversations. We'd love to address it there, and we're preparing to do that. And I will also add as a last statement that the first centrifuge is really a great example of the value creation-based agreement and partnership that we have with companies like Palantir. And I think the very first milestone that we set out there, we've been able to capitalize on it, and we're looking to do that eventually for all the other milestones that we're facing.

**Operator** (Operator):
Your next question comes from Jon Windham from UBS.

**David Choe** (Analysts):
This is David on for Jon Windham. Just wanted to touch base on -- can you give us an indication or kind of a status update on where you are in negotiations with the DOE and the potential to convert your demonstration cascade to commercial offtake and the potential to bring some of those volumes online a little bit quicker to market.

**Amir Vexler** (Executives):
Yes. So we are in discussions. Again, as I typically answer my questions, I'll give a little bit of backdrop and sort of the context for the answer just for the benefit of all the other listeners.
We've embarked on a demonstration program with the DOE. They've been a great supporter. We worked collaboratively really well to demonstrate our technology now for 3 years. It's been hugely successful, and it provided the impetus and the capability to expand that into commercial operations.
The natural next step for the -- the natural next step for the 16 centrifuge demo cascade is to place that into commercial operations. The cascade is producing. We are in discussions with the Department of Energy about how to amend and how to make a more wholesome agreement where this continues to serve the market and some of the reactors that are getting into the market now and would require some of that material.

**Todd Tinelli** (Executives):
Yes. To Amir's point, we -- the centrifuge is currently spinning for commercial use. And as part of the larger agreement, it's our ambitions and the DOE's ambition to keep those centrifuges spinning throughout their life cycle, and we are currently working that in through our long-term arrangement with the DOE. We have -- they have given us rights to use those commercial -- those centrifuges for commercial use currently, and that's what they're using.  So currently, we are enriching for HALEU for commercial needs at this moment.

**Operator** (Operator):
Your next question comes from Eric Stine from Craig-Hallum.

**Unknown Analyst** (Analysts):
This is Luke on for Eric. So as it relates to your supply chain strategy, should we expect to see vulnerable areas addressed through vertical integration like with Westerman? Or was that more of a sort of a one-off event from a strategic perspective?

**Amir Vexler** (Executives):
The -- I think your question specifically asks about vulnerable. I would say that the Westerman deal was a whole lot about an opportunity to derisk our supply chain, to derisk the build-out and to derisk the business model as well as to be able to capitalize on a lot of efficiencies that we see out there. So all in all, we're very satisfied with it. But I mean, there's other tools in our arsenal over there that we're deploying in setting up a supply chain that is predictable, capable, and produces high-quality product. I mean, these things are done every day by our team, are not necessarily advertised. They're not necessarily how they're communicated to the broader community. But this is the kind of stuff that we do every day that goes unadvertised.
You use the word vulnerability. This is going to be a major project. We have a lot of suppliers. Each supplier has their own strengths and weaknesses. We have built -- we are building and we've built resilience in our supply chain where possible. We're using quality oversight. We're using partnership with different suppliers. So we're not taking anything off the table. I think what you saw with Westerman is an example where you had really a perfect fit of all these factors come together, and there was no coincidence that this deal was made.

**Todd Tinelli** (Executives):
Yes. I will just comment. We view Westerman as a world-class operation, especially in the nuclear space, and they reach over into other industries. This allows diversity to Centrus' income stream and revenue. It's immediately accretive in year 1. And it really serves as a platform for us to expand on supply chain integration, take out some of those vulnerabilities if we see. They present themselves through either organic growth, now through Westerman ,or through additional M&A activities. We are extremely excited about this.
I will just comment that on our investor day, we plan on providing a significant more information around the acquisition. And we hope that all of those on the call today are able to dial in or join us, and where we can provide a long-term view of our vision for Westerman and our supply chain. Thank you.

**Operator** (Operator):
Your next question comes from Rob Brown from Lake Street Capital.

**Robert Brown** (Analysts):
Just wanted to kind of follow-up on the centrifuge manufacturing ramp with the first one now done. How do you -- I know you can't give exact numbers, but how do you sort of see that ramp happening? Is it over the next year? Is it sort of ramp quickly? Or just a sense of how that develops?

**Amir Vexler** (Executives):
Yes. Good morning, Rob. Could you -- just to make sure I answer your question and I understand it. When you say the ramp, you're talking about the cadence of the centrifuges as offline? Or what specifically were you thinking of?

**Robert Brown** (Analysts):
Yes. I think you mentioned focusing on ramping up the level of production of centrifuges -- just for the color on how that happens.

**Amir Vexler** (Executives):
Yes. So just as a general backdrop again, when we announced the first centrifuge, obviously, the big announcement there is not in the centrifuge itself, but the announcement is that now we have a functioning, operating production line that produces centrifuges, and we really are celebrating the first off that come off of this line. So there is a certain cadence, rhythm that we are currently engaged in and we're producing.
At this point, we're probably going to reserve a lot of that detail for our investor day where we have a lot more wholesome conversation on this and presentation, but do expect to see more information announcement come out on that. The point is that we have an operating manufacturing line that is in current production.

**Operator** (Operator):
Your next question comes from Lawson Winder from Bank of America Securities.

**Lawson Winder** (Analysts):
Amir and Todd, I appreciate today's update. And I look forward to the investor day very much. The thing I'd like to kind of better understand is commercial HALEU. So you've disclosed that the existing 16 cascades are now enriching HALEU for the commercial market. Can you just confirm whether that's against the Oklo, X-energy, Radiant or Antares contracts? Or is there another customer? And then when we think about revenue and economics from that, I mean, when do you expect first commercial HALEU revenue to start showing up in the P&L? And then how should we think about the margins versus the DOE HALEU contracts? I mean, are these going to be similar margins? Or could commercial HALEU possibly have significant superior economics?

**Amir Vexler** (Executives):
Yes. So a lot of questions there, and thank you for that, Lawson. Let me try to jot them down. I'll try to answer all of them. The -- your first question around the commercial HALEU and who specifically it goes to. The answer that I'll have for you is it will be supplied to the commercial market that requires HALEU. And -- I mean, everybody read our announcement. There's no more detail further to that, but we're absolutely looking forward to supporting the start-up of the commercial market of HALEU. I mean, these new reactors are becoming real. They require fuel, and we are the first ones out there that are going to be fueling them. And having the only HALEU cascade in the Western world that's able to supply them right now gives us a huge advantage, and we're looking forward to providing that support.
Now to your -- I think the next question you had was comparing contrasting margins on these contracts versus the DOE. Todd will give you the word on that.

**Todd Tinelli** (Executives):
Yes. Look, there's two different types of contracts that are present. The DOE, obviously, with the demo project that allowed us to prove our capability while providing enrichment that can potentially be used for the start-ups of many of these SMRs and microreactors.
On the commercial, there's a lot more that goes -- that's involved around the commercial contract terms. Obviously, we don't not get into those types of economics, but there's various different items and every contract is different as to who provides the fee, whether it's LEU or we are providing it. So the overall price there can have some variability. And -- but we are obviously confident in their ability in the HALEU market to provide significant upside to the company and optionality.
So we're rooting for all of the SMRs and advanced reactors. And as Amir said, we're extremely excited to be the only one enriching commercially HALEU fuel right now and are standby to meet all of our customer needs.

**Operator** (Operator):
Your next question comes from Joseph Reagor from ROTH Capital Partners.

**Joseph Reagor** (Analysts):
I guess for me, on the Westerman acquisition, can you give us any additional color on what the margins look like there at the gross margin level? And what, if any, seasonality there is to their business?

**Todd Tinelli** (Executives):
Yes. Yes, we are really excited, as I said, about the Westerman. I think I will put a pause on one of your comments, but we believe there's significant upside to the Centrus revenue stream.
This industry has very strong margins in the supply chain. It does two things. One is it as one of our larger suppliers, it allows us to derisk our supply chain and have cost savings while diversifying our revenue base. Westerman also is involved in other high-growth industries and also oil and gas. The margins vary in each one of those segments. The high-growth segment is obviously in high demand and the margin's a little bit higher. Nuclear has strong margin profile. And the last is the oil and gas has been a mainstream for the Westerman throughout their operations. And we will provide more information on our investment day, including breakdowns of their margin profile in each segment and their contribution of revenue to Centrus in the current year and over the next future years. I hope that helps.

**Amir Vexler** (Executives):
Joe, I want to add a couple of other things here since we're talking about Westerman. So I made a comment to this earlier that this was really no coincidence. This is -- this was not one of those things, hey, we want to buy somebody. Let's look at a list of 100 people. No, this was not the case. So Westerman, folks in our industry -- know that Westerman is one of the strong fabrication pillars that has a nuclear grade fabrication capability. They're a high-precision fabricators. They're very versatile, as Todd mentioned. This is a great fit. And not only are we looking at, as I said, a lot of the derisking of the supply chain build-out and the business model that we've communicated, but we also have a very strong eye to the future potential and what other things could be done to support our build-out in the business as a whole.
So as Todd said, I'll echo again, we're very excited about the things that are yet to come. And hopefully, we'll have a much broader conversation December 7.

**Operator** (Operator):
Your next question comes from Jeff Brand from Northland Capital Markets.

**Jeffrey Grampp** (Analysts):
I had a question on the capital deployed kind of cadence here. Hoping to get any additional clarity you guys can provide in terms of kind of Q4 spending. Obviously, it could be a wide range of outcomes and still hit the full year guide. So just kind of wondering how we should think about spending into Q4 and any early thoughts on spending trajectory into '27. Thanks.

**Todd Tinelli** (Executives):
Thanks for the question, Jeff and good morning. So we have maintained our capital spend guidance. So obviously, you can kind of back into our fourth quarter spend. What I will say is we are now crossing the threshold into deploying capital at a more accelerated rate. We have started our first construction package. As you can see, we have our first centrifuge rolling off the line. We have secured our supply chain and have orders on -- for all of our materials currently placed, and we're moving forward with our build-out.
All of these numbers are ex-Westerman. I just want to make that point. So often in GAAP and other areas, an acquisition will be considered CapEx and growth CapEx. But to maintain status quo and quarter-over-quarter continuity, we've excluded Westerman from that. Now to be said, we will look to provide more guidance in our Investment Day on December 7.
As for 2027, what I said earlier this year and on previous calls, we're going to get to a point where we start to see some real cadence of capital deployed. And we're now in that ramp-up. We only started our Fluor contract midyear as we signed the contract. And so now as that's beginning to come to fruition and we are -- have boots on the ground, our spend increases in addition to the manufacturing side. So stay tuned. We'll provide more guidance as for 2027. Obviously, we will be looking to give a more wholesome number in future discussions.

**Operator** (Operator):
Your next question comes from Jayad from Stifel.

**Unknown Analyst** (Analysts):
As we head into the next Congress, do you guys see any change in the outlook for federal support for domestic enrichment? Or is that support largely insulated from the political cycle?

**Amir Vexler** (Executives):
Yes. Good apropos type question. I will tell you with firm belief that this ought to not change the momentum of our industry, this ought not to change the momentum of the investment, the interest and the focus that -- and the support that the U.S. government provides to the fuel cycle and specifically to enrichment. And the reason why I'm saying this is we have now been through this cycle of two administrations at least during my time, and I have not seen a change in support, focus or dedication. I've seen it increase. I mean, some of the conversations around clean energy needing to increase -- I mean, all of these things don't go away. They're still there. The conversations around reindustrialization, providing jobs, it becomes even more important now. So the answer to your question is I absolutely don't see any change. I see a necessity for even stronger support and focus, and we're looking forward to working with the new Congress on this as well.

**Operator** (Operator):
Your next question comes from Sean Milligan from Needham & Company.

**Drew Scott** (Analysts):
This is Drew Scott on for Sean. With the first centrifuge ahead of schedule and backlog growth tracking well, are you seeing HALEU demand pull forward ahead of expectations at all? Or are you even enough to say you consider pulling forward capacity even further?

**Amir Vexler** (Executives):
I'm sorry, I did not hear the last part of the question. Could you please repeat the question again?

**Drew Scott** (Analysts):
Yes. So are you seeing HALEU demand pulling forward kind of ahead of your expectations? And would that even make you pull capacity forward ahead kind of what you originally planned?

**Amir Vexler** (Executives):
Yes. Thank you for that. I'm not seeing as much of pulling of demand ahead by the reactor developers. What we are seeing, and I mentioned it earlier, is we're seeing a lot stronger commitments and a lot more aggressive focus on actually locking in agreements and derisking the fuel supply part of the equation when it comes to their build-out. So no, there is really no changes in terms of the cadence that we're planning in terms of rolling out our capacity. We obviously, as I'll repeat it again, are looking for every opportunity that we have in shortening lead times and creating efficiencies, and we will execute on that. But from the customer side, we're not seeing that yet.

**Operator** (Operator):
Your next question comes from Sameer Joshi from H.C. Wainwright.

**Sameer Joshi** (Analysts):
My quick question is on the 4Q outlook. Basically, if you look at the annual outlook, it looks like 4Q will be $142 million to $192 million revenues. Like are there any takes and puts on this? And then part 2 of that question is the SWU pricing versus SWU cost management, how are you looking at it? Should we expect another sort of negative gross margin quarter -- this quarter?

**Todd Tinelli** (Executives):
Thank you for your question and good morning. Yes, as you expected, we maintained our guidance. We are optimistic, and we feel, obviously, that the fourth quarter provides a full year view of our strong results. As we've always noted that we see significant seasonality, including when we actually have sales that come -- that are being delivered, but also receive our shipments. That quarter-over-quarter mix provides some fluctuation in our gross margin profile. That's why we've been discussing this on a TTM basis to provide a more normalized view. The negative gross margin and everything, there's a lot of timing around when we receive product and mismatch of when we deliver product. So as such, we are very confident in our full year view. That's why we have maintained our guidance. We believe that the revenue and guidance that we have provided is also ex any Westerman upside. So I just want to make that note. And we will be providing updated guidance on our December 7 Investor Day.

**Operator** (Operator):
Your last question comes from Ryan Pfingst from B. Riley Securities.

**Ryan Pfingst** (Analysts):
Maybe just a quick one on the backlog increase here. Was that fully from the 3 recently announced advanced reactor customers? Or were there other undisclosed customers in there?

**Amir Vexler** (Executives):
Yes. That's not something that we disclose, but I can say that this was a mix of both LEU and HALEU. Unfortunately, I can't give the details. We don't provide the breakdown and separate the amount. The vast majority of the backlog is LEU, either for LEU customers or as feedstock for our future HALEU off takers. I hope that answers the question, Ryan.

**Operator** (Operator):
Thank you. At this time, we have no further questions. I would like to turn the call back over to Mr. Neal Nagarajan, Senior Vice President. Please go ahead.

**Neal Nagarajan** (Executives):
Thank you, operator, and thank you to everybody who listened on today's call. We're very excited about our upcoming investor day on December 7 at Piketon, Ohio, and we look forward to providing the market with more details at that time. Thank you.

**Operator** (Operator):
Ladies and gentlemen, this does conclude your conference call for today. We thank you very much for your participation, and you may now disconnect. Have a great day, everyone.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LEU_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Amir Vexler (CEO)｜guidance：CEO 重申 2026 全年營收指引 4.5 億至 5 億美元與資本支出 3.5 億至 5 億美元。（原話："We are reaffirming our 2026 annual guidance for total"）
- 2026-08-06｜Amir Vexler (CEO)｜guidance：Piketon 2026 年淨新增員工指引由 100 以上上調至 175 以上。（原話："from over 100 net new employees to over 175 net new"）
- 2026-08-06｜Todd Tinelli (CFO)｜guidance：CFO 表示不提供逐季指引，也不提供 2026 年以後的資本支出指引。（原話："We're not going to provide"）
- 2026-08-06｜Todd Tinelli (CFO)｜guidance：CFO 預期資本支出與非資本支出的步調會在年內加速。（原話："the pace of our CapEx and non-CapEx spend to accelerate"）
- 2026-08-06｜Amir Vexler (CEO)｜margin：管理層說明單季波動大，因此以年度（含 TTM）結果衡量進展。（原話："we believe our annual results are more indicative of"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：CFO 拆解 SWU 營收：量減 23%，平均價格增 3%。（原話："due to a 23% decrease in volume of SWU sold, partially"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：CFO 說明 SWU 單位成本較去年同期上升 13%，且本季有 5,340 萬美元鈾銷售。（原話："partially offset by a 13% increase in the average cost of"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：本季毛利 4,990 萬美元，去年同期為 5,390 萬美元。（原話："compared to a gross profit of $53.9 million in Q2"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：CFO 說明淨利下滑主因：SG&A 增 1,280 萬美元（股票補償），先進技術成本增 750 萬美元。（原話："$12.8 million increase in SG&A costs, driven by an increase"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：調整後淨利加回先進技術成本 1,060 萬與股票補償 1,770 萬，稅後合計 2,190 萬；預期此類費用持續流經損益表。（原話："we continue to expect to have a certain level of"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：被問成本為何上升，CFO 以庫存成本、合約組合與會計處理回應，稱利潤率符合預期，未給具體成本拆解。（原話："Our margins are coming in line with"）
- 2026-08-06｜Todd Tinelli (CFO)｜capital_allocation：季末無限制現金 19 億美元，ATM 本季僅募得 5,390 萬美元。（原話："We finished the second quarter with $1.9 billion in"）
- 2026-08-06｜Todd Tinelli (CFO)｜capital_allocation：本季總資本支出 8,220 萬美元，其中 CapEx 7,160 萬、非 CapEx 1,060 萬。（原話："total capital spend of $82.2 million with $71.6"）
- 2026-08-06｜Todd Tinelli (CFO)｜capital_allocation：CFO 稱現金足以應付近期資本需求，並表示或有積壓訂單中的財務或有條件已全數移除。（原話："we believe we are sufficiently funded to meet our near-term"）
- 2026-08-06｜Amir Vexler (CEO)｜capital_allocation：CEO 表示簽署 DOE 濃縮標案帶來非稀釋、非債務資金。（原話："we have unlocked substantial nondilutive, non-debt funding"）
- 2026-08-06｜Amir Vexler (CEO)｜capital_allocation：CEO 表示持續評估供應鏈相關併購機會。（原話："We also continue to evaluate M&A opportunities in our"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：管理層表示打算在未來 HALEU 承購合約持續採用預付款結構。（原話："is a structure we intend to utilize in"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：CEO 宣布 Oak Ridge 第一台離心機預計 2026 年內完成。（原話："we plan to have our first centrifuge completed at our Oak"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：被問商業生產時點，CEO 去掉「後期」字眼，稱目標為 2029 年，可能縮短但無承諾。（原話："I would remove the adjective late and just say in 2029"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：縮短時程方面，CEO 稱正在探索但沒有可宣布事項與承諾。（原話："there is nothing to announce and no commitments at this"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：管理層預告 12 月在 Piketon 舉辦首次 Investor Day。（原話："we are excited to host our first Investor Day in December"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：CEO 說明首個新產能預計 2029 年上線，過渡期正與 DOE 洽談以民營方式營運現有 16 台離心機 HALEU 串級。（原話："the first new capacity from this transition is expected to"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：已與約 75% 的關鍵供應商完成合約；全年指引為 100%。（原話："We have finalized contracts"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：積壓訂單成長至 45 億美元，延伸至 2040 年；LEU 部門 37 億、技術解決方案 8 億。（原話："We grew our backlog to $4.5 billion"）
- 2026-08-06｜Todd Tinelli (CFO)｜customer：CFO 拆解積壓：LEU/HALEU 濃縮銷售增約 6 億美元；約 30 億濃縮積壓中 24 億已為確定協議。（原話："$3 billion in the segment's enrichment"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：分析師問積壓是否含 DOE 與 LOI，CEO 稱不含 DOE，增加來自商業協議，不提供更多細節。（原話："this does not include the"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：與 Oklo 簽署意向書，自 2029 年起供應 HALEU 給至多 5 座 Aurora powerhouse。（原話："signing of a letter of intent with Oklo for Centrus to"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：宣布與 X-energy 的 HALEU 承購合約，CEO 稱為確定性協議並含預付款。（原話："It's definitive, which is very important, and we're looking"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：CEO 指出客戶願意簽具法律約束力協議的能力提高，Oklo 為朝確定合約推進中。（原話："a much greater ability from our customer base to actually"）
- 2026-08-06｜Todd Tinelli (CFO)｜customer：CFO 稱近期市場上公用事業已因俄羅斯禁令確保部位，目前 RFP 與討論針對未來有產能的期間。（原話："utilities have secured their position."）
- 2026-08-06｜Amir Vexler (CEO)｜customer：CEO 稱與公用事業的洽談並非線性，時間點不規則。（原話："They're lumpy and how they're being delivered."）
- 2026-08-06｜Amir Vexler (CEO)｜competition：CEO 稱 SWU 價格上升來自需求超過供給，且未來 2、3 年才有新產能陸續上線。（原話："you have demand that is outstripping supply."）
- 2026-08-06｜Amir Vexler (CEO)｜competition：CEO 稱長約價格持續攀升，現貨價維持在去年高點。（原話："spot pricing"）
- 2026-08-06｜Amir Vexler (CEO)｜competition：CEO 稱公用事業關注新進入者以確保市場有競爭，且財務或有條件移除後風險較低。（原話："we're getting a lot of advantages"）
- 2026-08-06｜Amir Vexler (CEO)｜competition：CEO 稱 Centrus 現為 HALEU 的首選供應商，並視 HALEU 為額外收益、LEU 為確定性業務。（原話："LEU is the sure business, the sure thing in the market."）
- 2026-08-06｜Amir Vexler (CEO)｜product：CEO 稱已提前兩週完成示範合約下所有 HALEU 生產要求。（原話："2 weeks ahead of schedule."）
- 2026-08-06｜Amir Vexler (CEO)｜product：建設規劃上，LEU 與 HALEU 的建置比例目前不變，依客戶確定承諾決定。（原話："we're not really"）
- 2026-08-06｜Amir Vexler (CEO)｜product：CEO 稱與 Palantir、EPC 夥伴合作降低成本，並鎖定大量訂單以爭取供應商節省，未提供數字目標。（原話："that's not something that we've talked about on this phone"）
- 2026-08-06｜Amir Vexler (CEO)｜product：CEO 稱縮短前置時間可轉為更早實現營收，商業協議要求更快時程。（原話："lead times really translate into enhanced revenue"）
- 2026-08-06｜Amir Vexler (CEO)｜risk：CEO 稱單季因業務性質有顯著波動。（原話："there can be a significant"）
- 2026-08-06｜Amir Vexler (CEO)｜risk：CEO 稱 HALEU 是補充成長機會與預付款資金來源；NNSA 有意向向 Centrus 單一來源採購部分濃縮活動。（原話："its intent to sole source certain enrichment activities"）
- 2026-08-06｜Todd Tinelli (CFO)｜risk：分析師問營運合約資金可能到期，管理層未直接回答該部分在營收指引中的位置，僅重申維持指引。（原話："We're not providing"）

### 問答異常語氣（迴避／改口／保留）
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：UBS：X-energy 交付節奏，以及是否來自示範串級轉商業營運。｜答法：稱無法提供交付與合約條款細節，改談 HALEU 領導地位與預付款。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Citigroup：營運合約資金可能到期，位於營收指引區間何處。｜答法：CFO 未回答該項位置，改談季間波動、維持指引、Piketon 增員；CEO 轉談離心機。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：H.C. Wainwright：SWU 價格增 3% 但成本增約 30%，成本驅動因素為何。｜答法：CFO 未拆解成本，稱為 SWU 與鈾的組合、庫存會計，並說利潤率符合預期。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Needham：承購協議的定價結構（固定或指數）。｜答法：稱受 NDA 限制不評論定價，改談合約為確定性與規模經濟；未回答想簽多少承購量。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Guggenheim：HALEU 與 LEU 完全放量後的獲利能力。｜答法：兩位主管均稱不提供額外指引，CEO 改談示範串級轉商業的技術驗證意義。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Evercore：下半年與 2027 年資本支出節奏。｜答法：CFO 稱不提供 2026 年以後指引；CEO 改談首台離心機，稱不給數字。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Craig-Hallum：進一步成本節省的幅度。｜答法：CEO 稱列為優先事項並列舉做法，但未給數字或目標。

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
{"date":"20260525","verdict":"B 觀望；等估值/MA 修復至 $120-150 + DOE final agreement + Russia 2027 末 waiver 確認後再分批","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"HALEU 商業化執行：Piketon 16-cascade 試線（已運轉）→ 商業擴產（Oak Ridge 製造 + Piketon 安裝）→ 2029 首批新產能上線","columns":{"2Y 驗證點":"2026-Q4 DOE 簽 final $900M agreement；2027 末 Geiger Bros 完成 Piketon 設計","5Y 驗證點":"2029-Q4 首批新產能上線（≥ 12 mt/year HALEU）","10Y 驗證點":"2030-2035 累積 50+ mt/year HALEU 產能 + 商業 ROIC &gt; WACC","具體門檻":"Piketon 2029 上線、12+ mt/year HALEU","信息來源":"DOE 公告 + 10-K MD&amp;A","漂移觸發":"連 2 季 Piketon milestone 延後 ≥ 6 個月 → 削弱"}},{"id":"H2","text":"$2.4B contingent backlog 兌現：商業客戶（utilities）的 contingent contracts 隨 Centrus 募資成功逐步轉為 firm orders","columns":{"2Y 驗證點":"2026 末 $1B+ Capex funding plan 公告；2027 首批 contingent → firm 轉換","5Y 驗證點":"2028-2029 至少 $1.5B contingent 轉 firm","10Y 驗證點":"2030+ 全 $2.4B 訂單 monetized 為 revenue","具體門檻":"2027 末轉換比例 ≥ 30%","信息來源":"Investor Day + 10-K backlog disclosure","漂移觸發":"連 2 quarter backlog YoY 停滯或下滑 → 削弱"}},{"id":"H3","text":"估值倍數收斂至合理區：當前 Fwd PE 45x 預期 5Y 收斂至 25-30x（同 industrial nuclear infra）","columns":{"2Y 驗證點":"2026-2027 共識 EPS 持續上修 + Fwd PE 跌至 30x 以下","5Y 驗證點":"2028-2029 Fwd PE 25-30x，EPS $6-8","10Y 驗證點":"2030+ 進入「成熟 utility」估值區 15-20x","具體門檻":"2027 末 Fwd PE ≤ 30x，EPS ≥ $4.50","信息來源":"sell-side + Bloomberg","漂移觸發":"連 2 quarter 共識 EPS 下修 ≥ 10% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Russia TENEX waiver 2028 切斷未延期，$1.2B Russia 來源 backlog 灰飛煙滅","columns":{"對應假設":"H1 / H2","時間尺度":"⚡ 短期（2027-2028）","監測指標":"DOE waiver 公告；TENEX 出口許可進度","警戒閾值":"2027-Q3 前未獲新 waiver / bridge 合約 → 連 2 季觸發即砍倉"}},{"id":"R2","text":"$3B+ Capex 募資失敗 / dilutive，contingent $2.4B backlog 無法 firm 化","columns":{"對應假設":"H2","時間尺度":"🔥 中期（2026-2027）","監測指標":"10-Q「Liquidity &amp; Capital Resources」段；DOE Loan Programs Office 進度；equity raise SEC filings","警戒閾值":"2026 末未公告 $1B+ funding plan → 削弱；2027 上半年實際 dilution &gt; 25% → 大砍 thesis"}},{"id":"R3","text":"laser enrichment（SILEX / GLE）規模化或 Urenco USA HALEU 商業核照通過","columns":{"對應假設":"H1 / H3","時間尺度":"🐢 長期（2028+）","監測指標":"GE-Hitachi GLE 進度；NRC HALEU 商業核照核發給 Urenco / Orano","警戒閾值":"跨年度 ≥ 50% 機率出現 → 砍倉；單一新聞不觸發"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"🟢","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":179.36,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
