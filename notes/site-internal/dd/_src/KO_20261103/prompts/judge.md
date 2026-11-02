你是 stock-analyst **v20 判斷 agent**，標的 KO（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"KO","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KO_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KO_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_operating_revenues_g","label":"Net operating revenues (GAAP)","value":13380,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000021344/000162828026067403/a2026q3earningsreleaseex-9.htm"}},{"id":"f_kpi1_non_gaap_comparable_oper","label":"Non-GAAP (comparable) operating margin","value":32.9,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":4465,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","unit":"USD m（利益率 33.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000021344/000162828026067403/a2026q3earningsreleaseex-9.htm"}},{"id":"f_kpi3_free_cash_flow_non_gaap_","label":"Free cash flow (non-GAAP), YTD 9M","value":11408,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000021344/000162828026067403/a2026q3earningsreleaseex-9.htm"}},{"id":"f_kpi5_comparable_eps","label":"Comparable EPS","value":0.91,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance"}},{"id":"f_kpi6_organic_revenue_unit_cas","label":"Organic revenue / unit case volume growth","value":7,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","unit":"%（單季有機營收；全球 unit case volume +5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance"}},{"id":"f_kpi7_fy2026_management_guidan","label":"FY2026 management guidance（本季上修）","value":"有機營收成長 ≥5%（原約 5%）；comparable EPS 成長 ≥11%（原 9–10%）；comparable 貨幣中性 EPS 成長 ≥9%（原 7–8%）；FCF ≥$13.0B（原約 $12.4B，營運現金流 ≥$15.2B、資本支出約 $2.2B）","period":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ko_gross_margin_pct","label":"KO 毛利率","value":62.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ko_operating_margin_pct","label":"KO 營業利益率","value":31.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ko_fcf_margin_pct","label":"KO FCF 利潤率","value":25.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pep_gross_margin_pct","label":"PEP 毛利率","value":54.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pep_operating_margin_pct","label":"PEP 營業利益率","value":15.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pep_fcf_margin_pct","label":"PEP FCF 利潤率","value":10.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mnst_gross_margin_pct","label":"MNST 毛利率","value":55.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mnst_operating_margin_pct","label":"MNST 營業利益率","value":29.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mnst_fcf_margin_pct","label":"MNST FCF 利潤率","value":22.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_celh_gross_margin_pct","label":"CELH 毛利率","value":48.76,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_celh_operating_margin_pct","label":"CELH 營業利益率","value":18.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_celh_fcf_margin_pct","label":"CELH FCF 利潤率","value":15.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kdp_gross_margin_pct","label":"KDP 毛利率","value":49.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kdp_operating_margin_pct","label":"KDP 營業利益率","value":16.62,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kdp_fcf_margin_pct","label":"KDP FCF 利潤率","value":9.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_ytd_9m","label":"SBC 占營業利益 (YTD 9M)","value":1.44,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-10-27）","citation":"SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000021344/000162828026067403/a2026q3earningsreleaseex-9.htm（SBC 194 ÷ 營業利益 13,496，本 agent 換算）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":95.25,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":23.33,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":65.85,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.34 → 3.34）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.52 → 3.52）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.26,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.78 → 3.79）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.34,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.52,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.79,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":28.1,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":8.03,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":8.53,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":28.52,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.34，分子＝快照價 95.26","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.205,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":25883.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 42478.0、現金 16595.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":4301.9,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":435682.23,"period":"2026-11-03","unit":"USD m","basis":"市值 409799.23 ＋ 淨負債 25883.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":50482.81,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":48892.74,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（19 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":8.63,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 95.2 / W52 79.61 / W104 72.52 / W250 62.99 / W250 13週斜率 1.06%"},{"id":"f_ma_w52","label":"52 週均線","value":79.61,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":72.52,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":62.99,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.06,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 將新進入者與零售商自有品牌列為競爭挑戰，並稱主要競爭對手之一為百事。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"Our competitive challenges include strong competitors in all geographic regions; in many countries, a concentrated retail sector with powerful buyers able to freely choose among Company products, products of competitive beverage suppliers and individual retailers’ own store or private-label beverage brands; new industry entrants;","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：競爭可能限制公司維持或提升份額的能力，並壓抑定價。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"Our ability to maintain or gain share of sales in the global market or in regional or local markets may be limited as a result of actions by competitors. Competitive pressures may cause the Company and our bottling partners to reduce prices we charge customers","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Coca-Cola 報告全球單位箱量成長 5%、北美持平，並在非酒精即飲飲料取得價值份額成長，上調 2026 EPS 展望。","source":"EconoTimes","url":"https://econotimes.com/Coca-Cola-Raises-2026-Earnings-Outlook-as-Global-Volume-Gains-5-1764514","excerpt":"volume rose 16%, while North American volume was unchanged in the quarter ended Oct. 2. By Helena WardOct 27, 2026, 5:25 PM UTC Updated Oct 27, 2026, 5:25 PM UTC2 min read Share article A shopper reaches for a small bottled drink in a supermarket aisle in Atlanta, Georgia. / EconoTimes.ai Coca-Cola raised its 2026 earnings growth outlook after global unit case volume grew 5% in the quarter","as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Coca-Cola 推出 Simply Pop 益生元汽水，對標 Olipop 與 Poppi。","source":"CNBC via NBC Washington","url":"https://www.nbcwashington.com/news/business/money-report/coca-cola-takes-on-olipop-and-poppi-with-new-prebiotic-soda-brand-simply-pop/3847012/","excerpt":"Coca-Cola takes on Olipop and Poppi with new prebiotic soda brand, Simply Pop By Amelia Lucas, CNBC • Published February 18, 2025 • Updated on February 18, 2025 at 8:10 am","as_of":"2025-02-18","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"KO 10-K FY2025 風險因素僅談零售通路整併、零售商可能壓價並推自有品牌，以及電商成長；未提及最大客戶導入第二供應商或將濃縮液環節自製。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"Retailers may seek lower prices from us and our bottling partners, may demand increased marketing or promotional expenditures in support of their businesses, and may be more likely to use their distribution networks to introduce and develop private-label brands, any of which could negatively affect the Coca-Cola system’s profitability.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 有一家裝瓶商占淨營收 10%（分布於 EMEA 與亞太分部）；2024、2023 無任何裝瓶商或客戶達 10%。公司稱信用風險集中度有限。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"For the year ended December 31, 2025, one bottler accounted for 10% of our net operating revenues, which are reflected in our EMEA and Asia Pacific operating segments. No bottlers or customers represented 10% or more of our net operating revenues for the years ended December 31, 2024 and 2023.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026 年 7 月 28 日 Q2 財報時上調 2026 全年調整後 EPS 與有機營收成長指引；本次搜尋未見 2026 年評級下調。","source":"WebSearch 摘要（finanzen.at：Coca-Cola boosts FY26 outlook）","url":"https://www.finanzen.at/nachrichten/aktien/coca-cola-boosts-fy26-outlook-update-1036371532","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026 全球單位箱量成長 5%，印度、中國、墨西哥、巴西領漲；Coke Zero Sugar +16%；北美量持平（部分歸因假日時點與成品飲料營運暫時性問題）；管理層上調 2026 展望（comparable EPS 成長至少 11%）","source":"Zacks: KO Q3 earnings call highlights raised outlook and volume growth","url":"https://www.zacks.com/stock/news/3017130/ko-q3-earnings-call-highlights-raised-outlook-and-volume-growth","excerpt":null,"as_of":"2026-10-21","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q2 2026 Trademark Coca-Cola 量成長 5%，為 17 年來最強（不含疫情復甦），部分來自 FIFA 世界盃行銷；分析師提醒 H2 面對較高基期、Q4 少 6 天，可能不易重複","source":"Hudson Labs / 搜尋摘要彙整（Q2 2026 earnings preview 等）","url":"https://hudson-labs.com/research/coca-cola-q2-2026-earnings-preview-ko-revenue-and-outlook","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"產業供給端：北美鋁罐 2026 年供給已售罄（2025 罐量 +4.8%）；橙汁等原料供給吃緊至 2027 年中；未找到把非酒精飲料供需定性為結構性或週期性的來源","source":"BevNET 2026: Ball North American can supply sold out in 2026","url":"https://www.bevnet.com/news/2026/ball-north-american-can-supply-sold-out-in-2026-can-volume-4-8-in-2025","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素：法規變動、執法優先順序變化可能造成更高合規成本、資本支出與生產成本，或須重新配方。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"Changes in applicable laws or regulations or evolving interpretations thereof, changes in enforcement priorities of regulators, and differing or competing regulations and standards across the markets where our products or raw materials are made, manufactured, distributed or sold, have in the past resulted in, and could continue to result in, higher compliance costs, higher capital expenditures and higher production costs, or make it necessary for us to reformulate certain of our products, resulting in adverse effects on our business.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"歐盟執委會 2025 年 3 月突擊檢查非酒精飲料業者，疑涉市場劃分；報導稱可口可樂為受查者之一，官方未點名，無法定結案期限。搜尋未見 2026 年進展。","source":"Fidelity/Bloomberg: Coca-Cola Facilities in Europe Targeted in EU Antitrust Raids","url":"https://fidelity.com/news/article/company-news/202503261254MIDNIGHTUSEQUITY_A3342258","excerpt":null,"as_of":"2025-03-26","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"土耳其競爭委員會 2025 年 6 月對 Coca-Cola Satış ve Dağıtım AŞ 啟動調查，涉零售獨家性，審查是否遵守 2021 年承諾。","source":"Turkish Competition Authority: Investigation Launched on Coca-Cola Satış ve Dağıtım AŞ","url":"https://www.rekabet.gov.tr/en/Guncel/investigation-launched-on-coca-cola-sati-6374dfd70846f01193e80050568585c9","excerpt":null,"as_of":"2025-06-10","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"佛州檢察長辦公室 2026 年 4 月向可口可樂、聯合利華、雀巢等發出資料調取，涉及與環保團體減塑合作是否違反反壟斷與消費者保護法；屬傳票階段，非壟斷訴訟。","source":"Bloomberg Government: Coca-Cola, Nestle, Unilever Targeted in Florida Antitrust Push","url":"https://news.bgov.com/litigation/coca-cola-nestle-unilever-targeted-in-florida-antitrust-push","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"KO 10-K 列出新增、擴大或報復性關稅（含推高供應商採購成本的關稅）、進口許可要求等為可能衝擊獲利的風險；原料與包材價格受關稅、制裁、配額、貿易障礙影響","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"new, expanded or retaliatory tariffs, including tariffs that increase suppliers’ sourcing costs; import authorization requirements; and other restrictions on business activities, which have been or may be imposed or expanded as a result of political and economic instability, deterioration of economic relations between countries or otherwise, could impact our profitability.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"KO 2025 年美國以外營運產生 288 億美元淨營收，且 10-K 將貿易爭端、關稅、制裁列為匯率波動來源","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"In 2025, we derived $28.8 billion of net operating revenues from operations outside the United States.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"報導稱川普政府可能下調 232 鋼鋁關稅（自 25% 升至 50%），範圍可能含鋁罐；KO 非直接進口商，成本由裝瓶商吸收，並表示若關稅不撤將推動更多 PET 包裝","source":"AOL 文章 president trump plans roll back","url":"https://www.aol.com/articles/president-trump-plans-roll-back-195555609.html","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"KO CEO 稱鋁關稅若不調整，可能讓更多產品改用 PET 包裝","source":"Just Drinks","url":"https://www.just-drinks.com/newsletters/trump-aluminium-tariffs-may-mean-coca-cola-uses-more-pet-ceo-says","excerpt":null,"as_of":"2025-02-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"KO FY2025 10-K 稱 2025 年因國際衝突營運受到干擾，並列示供應商產能、關稅、港口壅塞等原料供應風險","source":"SEC KO 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":null,"as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"KO 2026 IR 簡報：裝瓶商占系統銷量約 80%、約 3,100 條產線","source":"KO 2Q26 IR Overview Presentation","url":"https://investors.coca-colacompany.com/_assets/_902d893cff594df6990c43137cb7d900/cocacolacompany/db/861/11134/pdf/2Q26+IR+Overview+Presentation.pdf","excerpt":"~80% of Total System Volume(b) KO Bottling Investments Group UNMATCHED REACH(c) Execution What Our Bottlers Do Best Innovation People Servicing ~6M the Coca-Cola Network ~30,000 Red Trucks ~125,000 Suppliers Revenue Growth Management ~3,100 Production Lines","as_of":"2026-07-21","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 全球單位箱量 +5%（印度、中國、墨西哥、巴西領軍），price/mix +1%，並在整體 NARTD 飲料取得價值市佔提升","source":"Coca-Cola Q3 2026 earnings release","url":"https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance","excerpt":"Unit case volume grew 5%, led by India, China, Mexico and Brazil. Price/mix grew 1%, primarily driven by pricing actions in the marketplace, partially offset by unfavorable mix. The company gained value share in total nonalcoholic ready-to-drink (“NARTD”) beverages.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"北美 Q3 單位箱量持平：Trademark Coca-Cola 成長被水、運動飲料、咖啡茶下滑抵銷","source":"Coca-Cola Q3 2026 earnings release","url":"https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance","excerpt":"Unit case volume was even, as growth in Trademark Coca-Cola was offset by a decline in water, sports, coffee and tea.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"拉美 Q3 量 +6%、price/mix +7%（定價與有利組合）；亞太量 +6% 但 price/mix -2%（定價被不利組合抵銷）","source":"Coca-Cola Q3 2026 earnings release","url":"https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance","excerpt":"Price/mix grew 7%, primarily driven by pricing actions in the marketplace and favorable mix.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"亞太 Q3 price/mix 下滑 2%","source":"Coca-Cola Q3 2026 earnings release","url":"https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance","excerpt":"Price/mix declined 2%, as pricing actions in the marketplace were more than offset by unfavorable mix.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"全年 2026 有機營收指引上調為至少 5%（前為約 5%）","source":"Coca-Cola Q3 2026 earnings release","url":"https://investors.coca-colacompany.com/news-events/press-releases/detail/1176/coca-cola-reports-third-quarter-2026-results-and-raises-full-year-guidance","excerpt":"At least 5% growth","as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"Q2 2026 EMEA 價值市佔下滑（法國、英國流失大於奈及利亞、摩洛哥增益）","source":"Coca-Cola Q2 2026 results coverage (BeverageDaily/FoodNavigator)","url":"https://www.beveragedaily.com/Article/2026/07/28/coca-cola-raises-2026-guidance-after-q2-volume-revenue-and-profit-growth/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"非酒精飲料市場 2026 年約 +4.8%（614.72B→644.11B 美元，TBRC）","source":"The Business Research Company via giikorea","url":"https://www.giikorea.co.kr/report/tbrc1997988-non-alcoholic-beverages-global-market-report.html","excerpt":"It will grow from $614.72 billion in 2025 to $644.11 billion in 2026 at a compound annual growth rate (CAGR) of 4.8%.","as_of":"2026-03-25","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Cornell/Numerator 研究（經 AlixPartners 引用）估計 GLP-1 開始使用後六個月，軟性飲料購買約降 7%，為所追蹤飲料類別中降幅最大。","source":"AlixPartners, GLP-1 drugs stir change in the beverage industry","url":"https://www.alixpartners.com/insights/102jz6g/glp-1-drugs-stir-change-in-the-beverage-industry/","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"可口可樂 CEO Quincey 在 2025 年財報電話會議稱 GLP-1 對整體飲料業並非大因素，公司持續監測並朝補水與功能性、高蛋白、零糖/低卡產品創新。","source":"FoodNavigator-USA, Coca-Cola leans into protein, 'zeros and diets' as GLP-1 users reshape beverage habits","url":"https://www.foodnavigator-usa.com/Article/2025/10/21/coca-cola-rides-zero-sugar-protein-boom-amid-glp-1-shift/","excerpt":null,"as_of":"2025-10-21","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"可口可樂計畫在可口可樂零糖、Sprite 零糖與 Fresca 加入 6 克益生元纖維，列為 2027 創新計畫；PepsiCo（已收購 Poppi）的益生元可樂預計 2026 秋季上市。","source":"Food Dive, Coca-Cola prebiotic soda functional beverage innovation","url":"https://www.fooddive.com/news/coca-cola-prebiotic-soda-functional-beverage-innovation/832361/","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 描述的通路架構仍以獨立裝瓶夥伴、經銷商、批發商與零售商為主；直接面向消費者僅限 Costa 自營門市（計入 EMEA），未見訂閱化或平台化的結構性轉變描述。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"Additionally, we sell directly to consumers through retail stores operated by Costa. These sales are included in our EMEA operating segment, regardless of the physical location of the retail stores.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 將「消費者購物方式與模式因數位環境快速演變而劇烈轉變」列為競爭挑戰之一。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"dramatic shifts in consumer shopping methods and patterns due to a rapidly evolving digital landscape.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Coca-Cola 同意將美國 Aldi 門市的汽水由 DSD 改為倉儲配送（換取部分包裝獨家）；日期未確認。","source":"Beverage Digest","url":"https://www.beverage-digest.com/articles/1443-coke-to-shift-soda-to-warehouse-delivery-from-dsd-at-us-aldi-stores","excerpt":"Home » Exclusive » Coke to Shift Soda to Warehouse Delivery From DSD at U.S. Aldi Stores To access the full article, Subscribe today. Coke to Shift Soda to Warehouse Delivery From DSD at U.S.","as_of":"2026-07-22","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"KO 2026-10-27 公布 Q3：調整後 EPS $0.91 vs 共識 $0.88，營收 $13.4bn vs $12.92bn；公司把 2026 可比 EPS 成長指引上調至至少 11%（原 9–10%）。各來源對有機營收指引是否上調（至少 5% vs 原約 5%）說法不一。","source":"Finimize/Stocktwits/Finviz/Roic.ai/Newsquawk（搜尋摘要彙整）","url":"https://www.roic.ai/news/coca-cola-beats-q3-forecasts-lifts-full-year-earnings-outlook-on-volume-strength-10-27-2026","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-29 MarketBeat：共識評級 Moderate Buy，平均目標價 $95.56（14 Buy、3 Hold）；TD Cowen 目標價 $90→$100，Citigroup $97→$100。其他聚合站數字較低（StockAnalysis $86.06、Benzinga $89），as-of 較舊；Barchart 最高目標價 $104。2026-09 的 24/7 Wall St. 平均 $94.70。分布 as-of 不一致，未見 10 月財報後的更新共識。","source":"MarketBeat 2026-07-29; 24/7 Wall St. 2026-09-01; Barchart","url":"https://www.marketbeat.com/instant-alerts/cocacola-nyseko-stock-price-expected-to-rise-td-cowen-analyst-says-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"UBS 指出「至少 11%」的 EPS 指引措辭使 Q4 成為真正檢驗；Roic.ai 稱前次指引含約 3 點匯率利益，Newsquawk 稱上調為 currency-neutral 口徑。","source":"Roic.ai / Newsquawk 2026-10-27","url":"https://www.newsquawk.com/headlines/coca-cola-company-ko-q3-2026-usd-adj-eps-091-exp-088-revenue-134bln-exp-1292bln","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 後 2026 指引上調","source":"Stocktwits","url":"https://stocktwits.com/news-articles/markets/equity/coca-cola-raises-fy-2026-outlook-ceo-cites-sustained-momentum-after-q3-earnings-beat/cZUeJfIRBCO","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-07-16 8-K：子公司 fairlife 遭勒索軟體攻擊，美國產線暫停；公司當時尚未判定是否對公司有重大影響。","source":"SEC EDGAR 8-K Item 8.01 (2026-07-16)","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026048466/ko-20260716.htm","excerpt":"production operations at fairlife in the United States are temporarily suspended. fairlife’s Canada production operations are not currently impacted.","as_of":"2026-07-16","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Coca-Cola 表示 fairlife 已恢復多數美國產能（四座工廠），並稱預期不致對財務狀況或營運結果造成重大影響。","source":"搜尋摘要彙整（AJC／Food Dive 等，2026-07-27 報導）","url":"https://www.fooddive.com/news/coca-cola-restores-fairlife-production-after-ransomware-attack/826333/","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Coca-Cola HBC 於 2025-10 同意向 Coca-Cola 公司與 Gutsche 家族購入 Coca-Cola Beverages Africa 75% 股權（合計 26 億美元）；南非競爭法庭 2026-09 有條件核准。Coca-Cola 為賣方（持有 66.5%）。","source":"搜尋摘要彙整（Coca-Cola Beverages Africa／HBC 交易報導）","url":"https://www.privsource.com/acquisitions/deal/coca-cola-hbc-to-acquire-75-of-coca-cola-beverages-africa-path-to-full-ownership-x7SWmM","excerpt":null,"as_of":"2026-09-12","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2025-10 Coca-Cola Southwest Beverages 召回 4,228 罐（金屬污染，FDA Class II），屬裝瓶商區域性小規模召回。","source":"Top Class Actions (2025-11-04)","url":"https://topclassactions.com/lawsuit-settlements/coca-cola-recalls-more-than-4000-soda-cans-over-metal-contamination-concerns/","excerpt":null,"as_of":"2025-11-04","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Coca-Cola HBC 購入 Coca-Cola Beverages Africa 75% 股權，Coca-Cola 公司為賣方之一；南非競爭法庭 2026-09 有條件核准。未見 Coca-Cola 公司自身新收購。","source":"搜尋摘要彙整（HBC／CCBA 交易報導）","url":"https://www.privsource.com/acquisitions/deal/coca-cola-hbc-to-acquire-75-of-coca-cola-beverages-africa-path-to-full-ownership-x7SWmM","excerpt":null,"as_of":"2026-09-12","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K Item 3 列示的訴訟為 Aqua-Chem 石棉案與美國聯邦所得稅爭議；管理層認為除稅務爭議外不致造成重大不利影響。搜尋未見近期證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm","excerpt":"Management believes that, except as disclosed in “U.S. Federal Income Tax Dispute” below, the total liabilities of the Company that may arise as a result of currently pending legal proceedings will not have a material adverse effect on the Company taken as a whole.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"2025-10 Coca-Cola Southwest Beverages 因金屬污染召回 4,228 罐，FDA Class II；2026 年未見新召回。","source":"Top Class Actions (2025-11-04)","url":"https://topclassactions.com/lawsuit-settlements/coca-cola-recalls-more-than-4000-soda-cans-over-metal-contamination-concerns/","excerpt":null,"as_of":"2025-11-04","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"KO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":62.02,"operating_margin_pct":31.66,"fcf_margin_pct":25.83,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PEP","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":54.17,"operating_margin_pct":15.32,"fcf_margin_pct":10.66,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MNST","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.55,"operating_margin_pct":29.16,"fcf_margin_pct":22.58,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CELH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.76,"operating_margin_pct":18.81,"fcf_margin_pct":15.19,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KDP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.39,"operating_margin_pct":16.62,"fcf_margin_pct":9.78,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"KO"},"financial_history":{"ticker":"KO","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":43004000000.0,"revenue_yoy_pct":null,"gross_margin_pct":58.14,"operating_margin_pct":28.0,"net_income":9542000000.0,"diluted_eps":2.19,"free_cash_flow":9534000000.0,"fcf_margin_pct":22.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":45754000000.0,"revenue_yoy_pct":6.39,"gross_margin_pct":59.52,"operating_margin_pct":28.63,"net_income":10714000000.0,"diluted_eps":2.47,"free_cash_flow":9747000000.0,"fcf_margin_pct":21.3,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":47061000000.0,"revenue_yoy_pct":2.86,"gross_margin_pct":61.06,"operating_margin_pct":29.8,"net_income":10631000000.0,"diluted_eps":2.46,"free_cash_flow":4741000000.0,"fcf_margin_pct":10.07,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":47941000000.0,"revenue_yoy_pct":1.87,"gross_margin_pct":61.63,"operating_margin_pct":31.1,"net_income":13107000000.0,"diluted_eps":3.04,"free_cash_flow":5296000000.0,"fcf_margin_pct":11.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/KO/KO_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**The Coca-Cola Company** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to Coca-Cola Company's Third Quarter 2026 Earnings Results Conference Call. [Operator Instructions]
I will now hand the conference over to Todd Beiger, Vice President and Head of Investor Relations. Mr. Beiger, please go ahead.

**Todd Beiger** (Executives):
Good morning, and thank you for joining us. I'm here with Henrique Braun, our Chief Executive Officer; and John Murphy, our President and Chief Financial Officer. We've posted schedules under Financial Information in the Investors section of our company website. These reconcile certain non-GAAP financial measures that may be referred to this morning to results as reported under generally accepted accounting principles. You can also find schedules in the same section of our website that provide an analysis of our gross and operating margins.
This call may contain forward-looking statements, including statements concerning long-term earnings objectives, which should be considered in conjunction with cautionary statements contained in our earnings release and in the company's periodic SEC reports. Following prepared remarks, we will take your questions. [Operator Instructions]
Now I will turn the call over to Henrique.

**Henrique Braun** (Executives):
Thanks, Todd, and good morning, everyone. Our third quarter results reinforce the continued strength of the Coca-Cola system. We are acting with speed and discipline, enabling us to deliver strong results in an uneven environment. I want to start by thanking all our associates and bottling partners around the world. Every day, they serve customers, support communities and bring our brands to life. This year has required resilience, agility and strong execution and our people have continued to rise to the occasion. Their efforts reinforce my confidence in our updated 2026 guidance and in the long-term opportunities ahead.
This morning, I will provide an update on the global landscape and review our third quarter business performance. Then I will discuss how our system is delivering at scale and adapting locally to create durable growth. John will close with our financial results for the quarter, full year 2026 guidance and some early considerations for 2027.
First, the global operating environment continues to evolve. Geopolitical disruptions affect several parts of the world, cost pressures have accelerated and all of this has an impact on many consumers. Yet our confidence in the long-term opportunity remains unchanged. We have a strong portfolio of 32 billion-dollar brands and unmatched system reach with our bottling partners. These advantages matter, but so does what we do with them. For several years, we have been strengthening capabilities around consumer recruitment, digital, revenue growth management and system execution. By staying close to consumers and remaining constructively discontented, we continue to adapt in a dynamic environment. We're increasingly seeing that work reflected in our performance, including this quarter.
Volume grew 5% and organic revenue grew 7%. Stepping back, our longer-term performance reflects a more balanced contribution to top line growth. We expanded margins, while continuing to invest in our business. We delivered double-digit comparable earnings per share growth and gained value share.
Beyond the headline numbers, I'm encouraged by how we are growing. Our disciplined investments in digital capabilities are creating momentum across many of our markets and brands, yet we know there is still more work to do. We continue to sharpen how we turn consumer insights into innovation, and we are balancing scale and intimacy to drive stronger execution across our system. Our focus is simple: keep learning and do a little better every day.
This quarter, I spent much of my time with our people and bottling partners in several of our markets. These experiences always reinforce the importance of understanding local needs and responding to consumers, a strength of our system across the world. While every market is different, 3 themes were consistent: one, affordability is working; two, both Zero Sugar and Original Taste are recruiting consumers; and three, execution and local relevance are helping us win. Let me bring each of these to life across our business.
Starting in North America. We grew revenue and gained value share for the quarter. Volume was even, due in part to the timing of the July 4 holiday and temporary challenges in certain finished goods businesses, but performance improved sequentially each month during the quarter. Across our total beverage portfolio, we had strong volume growth from many brands, including Trademark Coca-Cola, fairlife, Powerade, FRESCA and smartwater. Mr. Pibb continued its success with another quarter of double-digit volume growth.
We are applying our learnings from our strong sports playbook with the next iteration of Fan Work Is Thirsty Work, which brings Coca-Cola into football fandom through team packaging, retail activation and locally relevant fan experiences. For Halloween, we are pairing Fanta's Haunted Universe with limited edition Ghost Face Punch and collectible packaging that brings the experience from screen to shelf. We're also creating new opportunities across our portfolio. Fairlife expanded its Nutrition Plan offerings with the return of fan favorite Vanilla. While BODYARMOR FIT brings sports hydration beyond the workout with a sparkling, Zero Sugar format with caffeine, electrolytes and metabolism support.
In Latin America, several key markets started the year facing difficult conditions, but our teams responded with market-specific actions that drove meaningful acceleration in the third quarter. We grew volume, delivered balanced top line growth and gained value share with broad-based improvement across the region.
In Mexico, the environment remains challenging, but we are seeing encouraging progress by combining affordability, strong revenue growth management capabilities and locally relevant marketing and disciplined execution.
In Brazil, momentum remained strong across our total beverage portfolio. Trademark Coca-Cola delivered another strong quarter, while Sprite and sports beverages also performed well. We continue to connect our brands with locally relevant passion points, including the Rock in Rio music festival, while also investing behind growth opportunities across our total beverage portfolio.
In Argentina, the environment remains challenging. We have strong plans in place, and while there is still more work to do, we're encouraged by progress across the region.
Moving to EMEA and starting with Europe. For the quarter, we grew volume, but we lost value share in a few key markets in Western Europe, and we are taking actions to improve performance. Following the FIFA World Cup, we transitioned into soccer activations around the English Premier League and Bundesliga, while continuing to build everyday consumption occasions through our Meals platform. We are complementing this effort with affordable propositions like our 500ml Supercan and are continuing to focus on price/pack architecture to help us recruit consumers and drive transactions.
In Africa, despite cycling a tough volume comparison, we gained value share and delivered high single-digit volume growth. We celebrated 75 years of Coca-Cola system in Nigeria with an end-to-end activation. To meet evolving consumer needs in South Africa, we adapted an affordable single-serve package from India, given it a locally relevant name, Mashesha, meaning quick. We also activated our Springboks rugby team partnership with the Be a Bok campaign and limited edition collectible players cans.
In the Eurasia and the Middle East, ongoing geopolitical conflicts continue to disrupt business in parts of the region. Our system was resilient, delivering another strong quarter with volume growth and value share gains. From Coke Studio featuring Pakistani artists to affordability initiatives to locally relevant taste innovations like Sprite Cool Mint and Fanta Pomegranate, our teams are adapting to dynamic market conditions. 
Finally, in Asia Pacific, performance varied across our operating units, but we are encouraged by the progress in many markets. We gained value share and grew volume, revenue and profit, while price/mix remained pressured due to negative geographic mix and affordability initiatives.
India delivered strong volume growth with each of our top 10 brands growing double digits. We're expanding our consumer base by scaling both affordability and premiumization, strengthening execution and leaning into emerging channels. For example, we expanded our Sprite and Spicy platform into the QSR channel in India with meal, combo activations, social media content and influencer collaborations, which contributed to Sprite's volume growth of nearly 20% in the region.
In China, the consumer environment remains subdued with cautious spending and soft domestic demand. Despite this, we delivered another strong quarter of volume growth with strength in Trademark Coca-Cola and Fanta. We continue to advance our digital capabilities to create more consumption occasions and connect with consumers in new ways. These actions are helping us drive immediate consumption packages and accelerate significant growth across digital commerce and emerging channels.
In Japan, volume declined as consumers remained pressured in a challenging macroeconomic environment that was heavily impacted by adverse weather. For the quarter, we gained share, expanded our consumer base in Trademark Coca-Cola and accelerated Zero Sugar volume growth. We are adapting our offerings and executing to meet changing needs.
In ASEAN and South Pacific, volume growth was broad-based across many key markets. Affordability, Zero Sugar offerings, innovation and strong execution are helping us recruit consumers and create new growth opportunities, including the launch of Coca-Cola Zero Zero in Thailand. In Vietnam, we are expanding our affordable single-serve package, which is now available in over 400,000 outlets with high repurchase rates.
To sum it all up, while the global operating environment remains uneven, we are encouraged by the momentum across our business and believe in our ability to deliver more from more markets and more from more brands. I'm energized by the progress we're making across the Coca-Cola system. We are learning as we go, continue to raise the bar and finding new ways to create value. The actions we are taking are helping us deliver today, while strengthening our ability to create value for the long term.
With that, I'll turn the call over to John.

**John Murphy** (Executives):
Thank you, Henrique, and good morning, everyone. Our results once again demonstrate the strength and adaptability of our business. For the quarter, organic revenue grew 7%. Our unit cases grew 5%. Our 2-year year-to-date volume growth average of 2% reflects a more sustained and balanced contribution to top line revenue growth. Concentrate sales were 2 points ahead of unit case volume due to the timing of concentrate shipments. Price/mix grew 1%. This was driven by 4 points of pricing actions, partially offset by 3 points of unfavorable mix primarily due to geographic mix, timing of investments and category mix.
Comparable gross margin increased approximately 170 basis points and comparable operating margin increased approximately 110 basis points. Both reflect underlying expansion, currency tailwinds and a favorable structural impact from last year's sale of our finished product operations in Nigeria. Importantly, margin expansion did not come at the expense of investment, and we continue to drive greater productivity and efficiency across our operations. We are investing behind our brands and executing revenue growth management strategies that help us better serve consumers across brands, packages, price points and occasions.
Putting it all together, third quarter comparable earnings per share of $0.91, reflected an 11% increase, including a 2-point benefit from currency tailwinds. Year-to-date, free cash flow was $11.4 billion, an increase versus the prior year. Our balance sheet remains strong with our net debt leverage of 1.3x EBITDA, which is below our target range of 2 to 2.5x.
We're continuing to judiciously manage our balance sheet as we await a court decision related to our ongoing dispute with the IRS. We are confident in our long-term free cash flow generation and the optionality it gives us as we move through the fourth quarter and into 2027. Our priorities remain the same: invest in our business and return capital to shareowners.
Now let me turn to guidance for full year 2026. We now expect organic revenue growth of at least 5%, which includes the impact of slight destocking and 6 fewer days in the fourth quarter. Our commodity exposure overall remains manageable. However, we are seeing elevated cost pressures in aggregate, driven by increased logistics and transportation costs. We now expect comparable currency-neutral earnings per share growth excluding acquisitions and divestitures of at least 9%.
Divestitures are now expected to be an approximate 2% headwind to comparable net revenues, and we continue to expect an approximate 1% headwind to comparable earnings per share. This assumes the pending sale of Coca-Cola Beverages Africa closes during the fourth quarter, subject to regulatory approvals. Based on current rates and our hedge positions, we continue to expect an approximate 1 point currency tailwind to comparable net revenues and continue to expect an approximate 3-point currency tailwind to comparable earnings per share for full year 2026. Our underlying effective tax rate for 2026 is now expected to be 19.7%. This reflects certain benefits in the current year that we do not expect to repeat going forward. All in, we now expect comparable earnings per share growth of at least 11% versus $3 in 2025.
Finally, we now expect to generate at least $13 billion of free cash flow in 2026. There are some considerations to keep in mind for the rest of the year. As a reminder, the fourth quarter will have 6 fewer days versus the prior year. We also now expect slight destocking in the fourth quarter, therefore, we expect concentrate shipments to slightly trail unit case volume for the full year.
For the fourth quarter, following the anticipated refranchising of CCBA, we expect a 4-point headwind to comparable net revenues, a 3-point headwind to comparable earnings per share and slight margin benefits. While it is too early to provide specific guidance for 2027, we do want to share some considerations based on what we know today. Overall, we expect consumer behavior to remain largely unchanged with value being a very important consideration across all markets and income groups. The investments we've made to date and the actions we've taken across our business position us to enter 2027 ready to execute.
With respect to commodities, we continue to manage various cost pressures and look for ways to navigate the environment through productivity initiatives with our Cross Enterprise Procurement Group and using all of our revenue growth management levers. At the same time, we'll continue to invest behind our brands, maintain disciplined cost management and focus on expanding margins over time.
With the anticipated refranchising of CCBA, we expect an 8-point headwind to comparable net revenues and a 2-point headwind to comparable earnings per share, but expect positive impacts to both our margins and the return profile of our business. Additionally, as previously announced, we are exploring a potential IPO of our bottling operations in India, and we'll provide further updates as appropriate.
Regarding currency, if we assume current rates and our hedge positions there would be a slight headwind to both comparable net revenues and comparable earnings per share for full year 2027. Many factors could impact both our currency outlook and broader business outlook between now and when we expect to provide guidance in February.
To summarize, we are pleased with our third quarter performance. Our proven all-weather strategy continues to be our best ally to sustain our momentum for the rest of the year and into 2027. Across our many markets and operating environments, our people continue to rise to the occasion, and we are grateful for their dedication every day.
And with that, operator, we are ready to take questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Dara Mohsenian from Morgan Stanley.

**Dara Mohsenian** (Analysts):
Obviously, another very strong unit case result in Q3 on top of Q2 strength, but the summer results were aided by events such as the World Cup and favorable weather. So, a, I wanted to touch on those events. It'd be helpful just what you learned from the summer events with the World Cup and even America's 250? How you're using technology investments to enable the system to better activate those events, but also really how you're working to hold on to incremental customers or greater demand from the existing customers during the events as you look across your brand portfolio? And then, b, just maybe taking it broader, as you look out to 2027 across the business globally, can you just discuss the challenge you see from cycling some of these tougher comparisons on the unit case side? And how you think about the system's ability to continue to sustain volume growth going forward?

**Henrique Braun** (Executives):
Thank you, Dara. It's great to hear from you. Look, first of all, we are really excited with the results that we had on Q3 because it shows sustained and steady momentum that we had from the first half was important to continue that through to the Q3, if you're seeing the numbers that we're getting more from more markets and more from more categories. And that showed up also in how we continue to gain value share globally. So it's 22 consecutive quarters of value share gains. So we're feeling that we got the right momentum. The strategy is working in an environment that continues to be very dynamic.
To your point about the World Cup and specifically here in the U.S., also the 250 campaign, those were great moments for us to pressure test our end-to-end activation going from the brand strategy, the innovations that we brought to life, the revenue growth management and execution coming in a very integrated way, and we showed up really well as a system, not only in North America but globally, and we leveraged that into Q3, and we're going to continue to leverage this in Q4 and 2027.
Part of the tech data and AI that we used during the World Cup, you're seeing on campaigns like Fanta Halloween that you can see the connected packaging really with great content and going all the way down to a transaction, which brings that ability for us to start pressure test the opportunities to drive more engagement all the way to transactions moving forward.
So the plans continue to be addressed market by market in an environment that continues to be very dynamic. And we feel good about where we are right now for Q3 and building the plans for 2027 as well.
To the point that you asked as well on what we're going to be bringing in for next year, I always start with the energy that we see with our bottlers, our customers when they see our plans year-to-date and what we are laying up for the rest of the year and next year. Yes, we're cycling year-to-date high volume year, but we earned that, right, with getting closer to the consumer and building the flexibility on our plans to develop the right foundations to get where we are. So we believe in our momentum, we believe in the plans. A lot still to happen until we get to next year. But we believe that we have everything that is under our control to guarantee that we continue to deliver on our long-term algorithm.

**Operator** (Operator):
Our next question comes from Chris Carey from Wells Fargo Securities.

**Christopher Carey** (Analysts):
A key strategy coming into the year was to drive more balanced top line across volume and price/mix. Certainly, as noted with Dara's question, you're on track for an exceptional year from a volume delivery standpoint, and then you'll have to compare against that going into next year as just you noted. But one of the things that I wanted to drill into a bit was the price/mix side, which if it turns out to be about 2% this year, we'll see could prove one of the lower price/mix years in about a decade. So the question is really, as you go into 2027, how do you think the price/mix strategy evolves so as to continue to deliver on the commitments that you have around your top line algorithm?
And within that, can you perhaps provide a bit of perspective on how much control you have over that price/mix line? There's clearly a geographic mix, there's category mix, you have pricing investments this year. And I think underlying the question is just your ability to have control over the complexion of your top line as opposed to there are just these headwinds coming at the price/mix line that are perhaps out of your control as you go into next year. So I'd love any context on that.

**John Murphy** (Executives):
Thanks, Chris. A topic close to our hearts here. Let me just take a step back from the quarter, in fact, the last 2 quarters. And just a reminder that when you think about the 2-year volume CAGR, it's still around the 2% mark, maybe slightly above that given the last 2 quarters. So we still feel good about the objective to deliver a balanced revenue algorithm, 2 to 3 points volume, 2 to 3 points price/mix as we move forward.
When you take into account some of the factors that have impacted our price/mix numbers recently, there are -- it's worth unpacking a little bit. We mentioned in the script that we had 4 points of underlying pricing in the quarter. And that's pretty consistent with our year-to-date numbers, a little bit of higher inflation from the couple of markets in the emerging world, but pretty consistent. And then it's the -- I think, it's the mix piece that has had a bigger impact on that PMO number and maybe a little bit of a surprise to some. But within that, about 2/3 of it relate to actions that either we have taken ourselves proactively or reflect some -- just some of the inherent mix that has taken place this year, particularly with the finished goods performance.
If you were to factor in the Topo Chico situation we've had this year, and you factor in the timing of investments and you take those out, our price/mix for the year is pretty much within the band that we would look to deliver.
Now as we go into 2027, it's a little early to give specifics on what we expect for 2027, but just look at the volume CAGR, the volume momentum that we have been delivering. We're continuing to look closely across the world at pricing dynamics going into 2027. Inflation is one factor. But we also take into account a number of other factors, the state of the consumer market by market, the competitive environment, the customer environment, et cetera. 
We'll provide a little more color on that in Feb. But the mix piece, we'll continue to see some geo mix headwinds just given the nature of the overall portfolio globally with the developing markets will continue, I believe, to outgrow some of the developed markets volumetrically. But 2/3 of the mix, as I said, this quarter were due to factors which we think are manageable going into next year.

**Operator** (Operator):
Our next question comes from Lauren Lieberman from Barclays.

**Lauren Lieberman** (Analysts):
Great. Wanted to talk a little bit about reinvestment. I know the mantra is more with more. And it looks like this quarter in terms of the reinvestment that went into SG&A, there was a lot of more. So if you could just talk a bit about how much advertising and marketing was up? How much of this is sort of set the stage into '27 because the gross margin -- and also while we're on margins. Underlying gross margin, I think, in the slide was up 70 basis points. So just curious how to think about that, right? You've talked about mix has actually been a headwind. So is it just the absolute strength of the volumes flowing through that's driving that gross margin strength. So marketing investments, where the SG&A dollars went and then drivers of the underlying 70 basis points in gross margin?

**John Murphy** (Executives):
Yes. Lauren, thank you. Let me start with the gross margin numbers. As you're well aware, we think of gross margin in 3 distinctive buckets, the underlying strength of the business, the structural, and currency. We're benefiting from some currency headwinds or some currency tailwinds this year. But the underlying numbers just reflects the quality of top line and the ongoing focus we have on managing our cost base. So as you think about the underlying going forward, implied in our algorithm is modest expansion, and we believe we have the ability to sustain that as we go forward.
Regarding the marketing investments, yes, we have taken a number of actions in recent months to set us up for a strong start to 2027. We have double-digit growth in above the line, and we have a number of programs that we're working in partnership with our bottlers on to, as I said, to be ready for a strong start into 2027. I would expect as we go forward that we'll have marketing investments growing more or less in line with our -- with margins, with gross margins to get the shape of the P&L where we want it to be, not just for '27, but beyond.

**Operator** (Operator):
Our next question comes from Steve Powers from Deutsche Bank.

**Stephen Robert Powers** (Analysts):
We've spoken about this before, but just the reality is that a lot of the inflationary pressures facing the system today sit more heavily with your bottling partners than with the concentrate business itself. And I guess as you -- in that context, as you approach collective 2027 planning, how would you characterize bottler economics today and their stance relative to those inflationary pressures? And any impacts that may be having on considerations around future pricing, investment levels or just the way that system economics are shared as you think about the year ahead?

**Henrique Braun** (Executives):
Thank you, Steve. Look, first of all, we always look at that from a system point of view. Everything starts from how we're going to first grow our plans aligned with our brand plans per market. And we feel that we have great plans for 2027, and we are actually anticipating that with investments this year as we have done in previous years to be ahead of the curve, right, to get the momentum that we have and the flexibility that we built during the year to continue to invest on those plans.
Regarding costs, which is one input into the plan, the environment remains very fluid. The commodities have been manageable for us at this time. Looking forward, we are working with the bottlers right now through all the levers that we have as a system. One of them is our Cross Enterprise Procurement Group that we procure the number -- the big commodities that we have for next year together. And with that, we bring also other levers into the equation, which is productivity, cost management and our RGM tools to ensure that we have an operational environment that can be totally linked with our growth plans for next year.
So more to come as we learn during the next few months, but so far, it has been something that we believe it's going to be manageable on the overall scheme of things.

**Operator** (Operator):
Our next question comes from Filippo Falorni from Citi.

**Filippo Falorni** (Analysts):
I wanted to go back to the North America business. Henrique, you mentioned that there were a few impacts on the volume being flat in the quarter, timing of 4th of July and some changes in the finished good business. Can you expand a little bit more on that? And given we see solid consumption data in tracked channels. Are you expecting some improvement as we move forward?
And then on price/mix, I know you were cycling a difficult comp in Topo Chico and fairlife. How should we think about that, particularly that mix component as we look ahead on the price/mix in North America?

**Henrique Braun** (Executives):
Yes. Filippo, thank you. So on North America, let me step back and talk a little bit about the quarter and the year so far. We continue to see solid performance in North America. We grew this quarter, right, revenue, we gained value share, we expanded margins. We got pricing in line with inflation that was really important that shows that the brands have the equity and the rights to take price, and we kept investing in our brands. The impact that you're mentioning on the price/mix was definitely impacted by the cycling of a very strong prior year on some of the premium brands that were generated through our finished goods, including Topo Chico with one of them that you know, and BODYARMOR as well. So with that into the equation, if you take that out actually and you take the impact of the July 4th that fell into the second quarter, and we mentioned that before, we would see volume growth, right? So we see the momentum is still there.
Now in terms of the strength of our strategy and our brands, we also feel confident that we have pretty good momentum, especially of Trademark Coca-Cola that grew again this quarter. Diet Coke and Coca-Cola Zero, especially Coca-Cola Zero growing double digit again. And fairlife continues to do really well. Powerade also grew. And we have other areas that we have work to do, which is always good for us also to instill here our motto of being constructively discontent that there are areas for us to work on. And one of them is to do a better performance on Sprite and BODYARMOR, and our supply chain going into next year. So all in all, we believe that we have the good momentum as a system and the right plans to navigate through the rest of the year in 2027.

**John Murphy** (Executives):
Yes. And I would just add, Filippo, if you're looking at the overall volume number, the restaurant industry continues to be under pressure. And so when you're looking at the scanner data, et cetera, I think you're seeing a stronger business at-home versus away-from-home largely driven by those consumer pressures that we've talked about in the past. And while our own business continues to have a lot of momentum across those channels, I think the underlying pressure across the consumer landscape is there, and I think it will be there for the rest of the year as we go into '27.

**Operator** (Operator):
Our next question comes from Andrea Teixeira from JPMorgan.

**Andrea Teixeira** (Analysts):
So I have a question on exploiting the theme of affordability, and of course, among all the CPGs, you have significantly -- significant brand equity. How should we be thinking about the list pricing and your bottling partners have historically been able to take pricing in the low single digits. If we put the geo mix, the geographical mix aside, do you think you still can count on RGM capabilities and would still allow some selective pricing, while protecting the entry price points?
And then a clarification on the fourth quarter. You obviously raised guidance and you have the 6 fewer selling days. John, you called out also the destocking comment, but you had -- also had said that in the third quarter. So it was ahead of the third quarter. So I was hoping to think about like how -- it's a wide range, of course, minimum 5 allows you to have a wide range there. But just thinking of how demand and destocking and how we should be think how many points of headwind that could be?

**Henrique Braun** (Executives):
Okay, Andrea. So I'll start with your question on -- especially on our strategy on the affordability, and John can chime in on the outlook.
So look, the affordability, you need to look at this on the full context of revenue growth management. It's one of the legs of how we get closer to the consumer these days. The premiumization is equally important. So we always look at both. What we are seeing across the world, and this is something that, especially in my travel the last quarter going -- divide and conquering here with John going in different parts of the world, we have seen that value continues to be something that cuts across every market and every consumer that we see all over the world. And value means different things for the consumer, which then touches into affordability and premiumization in a way that we capitalize that in our plans.
Let me elaborate on that. On the affordability, what we always look at is do we have the right value, the relevance of that brand and the worth choosing option for the consumer to keep them in the franchise? And if the answer is yes, we continue to push forward and get more coverage of that packaging format. If not, we adapt our plans and put that in place. A good example of that is what we did in Africa, a piggybacking from what we've learned in India, where they had one package, which is a single-serve PET package with plasma technology that can allow you to go in longer routes and still keep the shelf life high. Now we imported that into Africa, and that plays on affordability in both of these markets. And it's going to continue to be very important moving forward because the consumer loves the brands, but needs to be closer to what they can afford.
On the premiumization side that's equally important in this equation, we play at the category mix. There are a few brands that continue to help us with that. In North America, you got Core Power, you got smartwater and you got in other parts of the world, also different packaging sizes that allows us to play with the convenience and that value equation for the consumer also works really well. And the overall RGM strategy, we end up delivering what we need. So it goes in tandem, affordability and premiumization. And that's what you're going to see, not only the rest of the year, but building into 2027.
John, if you want to add on that?

**John Murphy** (Executives):
Yes, Andrea, the whole marriage of unit cases with our concentrate shipments this year has proven to be maybe the more challenging year since I've been around for a few reasons. You've got the first quarter and the fourth quarter, the plus 6 to minus 6 days. We have, as we've seen since the start of the year around the world, an external environment that's quite unpredictable. And I think our system has a tendency to want to get ahead of that.
And so the expectation that we highlighted in guidance reflects the best information we have at the moment. There's a couple of our segments where we do expect to see some destocking on the back of what has happened year-to-date, but we've still got some distance to go in the year, and we're keeping a close eye on this area. And as we -- with 6 less days, it's difficult to predict with accuracy just the cutoffs as we move towards the end of the year. So that's the best information we have at the moment. And based on all the inputs we get from around the world and if there's changes through the quarter, we'll certainly have the opportunity to update closer to the end of the year.

**Operator** (Operator):
Our next question comes from Robert Ottenstein from Evercore.

**Robert Ottenstein** (Analysts):
Great. You had a pretty nice increase in your guidance for free cash flow. Your leverage is down to, I think, 1.3 you said. So I was wondering if you could talk about the drivers on the free cash flow. And then you mentioned in the opening comments about increased optionality from your strong free cash flow and balance sheet going into '27. So maybe if you could elaborate on that and then put these comments in the context of potential outcomes from the IRS case?

**John Murphy** (Executives):
Yes. Thank you. Let me take those one by one. So free cash flow year-to-date 3 primary drivers. The first and the most important one is underlying business performance has been strong. We continue to make progress on working capital initiatives. Our cash conversion cycle, if I get it correct, is as good as it's been for many years at the moment. And then we have some timing that will play its way through the rest of the year. For example, our CapEx year-to-date is a little behind what you would typically expect, and we've got -- we expect that to make up in the fourth quarter. So key message, though, is free cash flow is strong, and we've got momentum as we close out the year into next year. 
We've used the word optionality very deliberately over the last number of months because we are in a situation where we're anticipating a decision in the coming months in the IRS case. And at the same time, we continue to think ahead as to the various outcomes that, that decision could generate and feel good where we are with respect to being able to manage a best and worst-case scenario. So the name of the game has really been to strengthen the balance sheet. I believe our balance sheet today is in as good a shape as it's been for many years. And to be ready in '27 to deliver on the priorities that we outlined in the script, we'll continue to invest in the business, primarily in the short term organically.
We remain open to other opportunities. We don't see them in the immediate horizon. And as always, we're here to return capital to our shareowners. And again, in the -- at the moment, that's primarily through our dividend. So think of the work to date has been focused on strengthening the balance sheet, being ready for a decision and the outcome of that decision to do the right thing for the business and to be ready for whatever that might mean in '27 and '28.

**Operator** (Operator):
Our next question comes from Peter Grom from UBS.

**Peter Grom** (Analysts):
Great. So I wanted to follow up on Filippo's question on North America. You touched on some of the timing dynamics, but you also mentioned that you saw sequential improvement in volume performance each month throughout the quarter. So I was wondering if you could elaborate on that? And have you seen that momentum continue into the fourth quarter? And then, John, you touched on the at-home versus away-from-home component. I'm just curious if you've seen any notable shifts in that dynamic as the years has progressed.

**Henrique Braun** (Executives):
So on the volume, yes, we saw that improvement month-on-month on the quarter. And the biggest impact in that was really what we said before was the July 4 impact that fell into the Q2. So we knew that we would start the first month of the quarter lagging behind it. What we have seen and I mentioned, when you look at the overall flat volume for the quarter, we're cycling a good performance of Topo Chico last year as well, which has also an impact on that. And we just got back with Topo Chico in Texas. So it's great news, I think, to everybody and to the consumers that have been waiting for too long. It's the first step back and we will sequence that moving into 2027, right? So that volume will start to come back. So definitely, it's something that we're looking forward to.
The other ones, really the momentum that we have. We grew Coca-Cola Trademark like we mentioned really good growth on the Zero variant as well, fairlife continues to grow, Powerade grew as well, FRESCA, Mr. Pibb has been another very good surprise, still small in the overall volume to impact the overall volume for North America. But within the innovation pipeline is something that we're very excited with that.
So all in all, what we see is, we have the momentum, we got the right plans in place, but we have also, going into the Q4, which is important to reinforce, the biggest quarter that we had in North America last year, and we have 6 less days. So you need to compose that with the equation. But when you look into a daily average sales, we have the momentum that was built over the quarter.

**Operator** (Operator):
Our next question comes from Peter Galbo from Bank of America.

**Peter Galbo** (Analysts):
John, I was just hoping to get maybe a clarification and then the question is tied to that. But on the currency FX guidance for 2027, I just wanted to understand if that was updated through yesterday and the context of it being, obviously, there's been some pretty big currency movements even in the last 48 hours in some big important markets for you. I know you caveated your commentary that there's many factors that could impact currency between now and February. But just want to understand kind of in real time how you're thinking about that given some of the moves that we've had? And whether that's embedded in the slight headwind kind of outlook that you have for '27 at this point?

**John Murphy** (Executives):
Yes. Great question. And the short answer is no. We need to take into account what's unfolded over the last 24 to 48 hours, and we'll continue to do so. There's been quite a -- as you've seen throughout the year, there's been quite a lot of movement. So it's one we're watching very carefully. And if there's sufficient movement over the course of the next number of weeks, we'll certainly would want to provide an update on that. And as I said, there's been quite a lot of swings throughout the course of this year and it's one to keep watch on. But the numbers that I talked about in the script do not reflect the movement in the real, particularly over the last day or 2.

**Operator** (Operator):
Our next question comes from Kaumil Gajrawala from Jefferies.

**Kaumil Gajrawala** (Analysts):
I guess, first on, sorry to belabor the point, but just for purposes of clarity, on the destocking, is the full year intended to be sort of below, in line or above in terms of concentrate versus shipments? And then maybe if there are particular regions where the destocking is expected to occur, I think that would be useful.
And then on gross margin, you had -- with such a strong concentrate shipment number, can you give some context of leverage on the GM and maybe leverage on the SG&A line as well and how it sort of works top to bottom because you probably won't have the spread going forward. And so to what degree can we -- can you help us forecast what margins would look like in the context of maybe better aligned unit case volume and gross margins?

**John Murphy** (Executives):
Sure. On the destocking, as I said in the previous question on this topic, it's a somewhat of an anomalous year in trying to predict exactly. Right now, if you ask me, we expect shipments to run slightly behind volumes for the full year. That's our ingoing assumption that's linked to the guidance that we've provided. And as I've said, there's a lot happening around the world. And there is every possibility that, that could deviate, but that's the ingoing assumption as we head into the rest of the year.
On your margin question, if I line up cases, shipments, everything else, we expect to have margin expansion for the full year. And again, the exact amounts that we're anticipating it's really on trend with what we've seen thus far this year.

**Operator** (Operator):
Our next question comes from Kevin Grundy from BNP Paribas.

**Kevin Grundy** (Analysts):
Great. Congrats on another strong quarter. We mentioned the brand twice, but haven't spent a lot of time on the strategy and that's fairlife, which has been a fantastic success story. Additional capacity came on this year, so we've seen a nice reacceleration in the scanner data. So a few questions related to the brand. One, can you talk about updated plans and how you're defining success? Two, where you see the brand sourcing occasions at the moment? And then three, maybe an update on the opportunity for the brand outside of the U.S., understanding the supply chain complexities?

**Henrique Braun** (Executives):
Okay. Thanks, Kevin. Look, we love the brand, as you know, fantastic performance, and we're pleased to see, number one, another quarter of strong and double-digit growth across all the variants, right? So fairlife, the Nutrition Plan and also on the Core Power, and that has been really encouraging. You remember that at the beginning of the year, we're still lagging behind. The demand and supply with the ramp-up of Webster. So we're getting better and better at with the ramp-up of the plant. And to the extent that we were able to launch also a new flavor for a Nutrition Plan, the Vanilla flavor, which is doing really well as well, and we announced already that we're going to have in the pipeline going to 2027, the Banana flavor, which is great, right? We have a lot of fans for that flavor. And it's something that we always wanted to start expanding. So good news is, we're getting the product back on the shelf to keep up with the demand and the pipeline looks strong going into 2027.
When you look at overall investment ahead of United States and Canada that we have today, we're still working around it. The brand has tremendous equity value, and that is going to be embedded into our long-range plan. So more to come on that. But the #1 priority for us right now is to keep up with the demand in these markets because there's still plenty of growth opportunities for us, and it's an important component of our growth moving forward.

**Operator** (Operator):
Our last question today comes from Bonnie Herzog from Goldman Sachs.

**Henrique Braun** (Executives):
Bonnie? Maybe on mute.

**John Murphy** (Executives):
There's no Bonnie.

**Henrique Braun** (Executives):
So I think we got to the end then. Okay. Great. Look, to close us out, our performance reflects the hard work of our teams and partners around the world who continue to stay close to consumers and doing a little bit better every day, and we are very pleased with that. We are confident in our ability to deliver our 2026 and long-term objectives and thank you for your interest, for your investment in our company and for joining us this morning. Thank you so much.

**Operator** (Operator):
Ladies and gentlemen, this concludes today's conference call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### KO_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜John Murphy (CFO)｜guidance：FY2026 comparable EPS growth guidance raised to 9%-10% vs $3 in 2025（原話："All in, we now expect comparable earnings per share growth"）
- 2026-07-28｜John Murphy (CFO)｜guidance：Organic revenue growth guided to about 5%, high end of prior range; currency-neutral EPS 7%-8%（原話："comparable currency-neutral earnings per share growth,"）
- 2026-07-28｜John Murphy (CFO)｜guidance：Divestitures now a 2%-3% headwind to comparable net revenues（原話："Divestitures are now expected to be a 2% to 3% headwind"）
- 2026-07-28｜John Murphy (CFO)｜guidance：Q3 concentrate shipments expected to lag unit case volume（原話："lag unit case volume by 1 point during the third quarter"）
- 2026-07-28｜John Murphy (CFO)｜guidance：Q4 gross and operating margin to benefit from CCBA refranchising（原話："operating margin to benefit from the refranchising of CCBA."）
- 2026-07-28｜John Murphy (CFO)｜guidance：Commodity cost basket described as manageable（原話："overall impact of our cost basket to be"）
- 2026-07-28｜John Murphy (CFO)｜margin：Q2 comparable operating margin +~90bp, driven by underlying expansion and currency tailwinds（原話："comparable operating margin increased"）
- 2026-07-28｜John Murphy (CFO)｜margin：Price/mix +2% split: 3pts pricing, 1pt unfavorable mix mostly investment timing in Asia Pacific（原話："This was driven by 3 points of pricing actions"）
- 2026-07-28｜John Murphy (CFO)｜margin：CFO says company has levers to expand implied margin in the algorithm（原話："we have the levers to continue to expand the implied margin"）
- 2026-07-28｜John Murphy (CFO)｜margin：CFO notes FX has turned from headwind to tailwind this year（原話："it has turned into a tailwind"）
- 2026-07-28｜Henrique Braun (CEO)｜margin：APAC price/mix decline broken into three roughly equal parts incl. geo mix（原話："the other 1/3, it's just the geo mix"）
- 2026-07-28｜Henrique Braun (CEO)｜margin：APAC price/mix decline: one third is investment timing（原話："One was investment timing, 1/3 of it."）
- 2026-07-28｜John Murphy (CFO)｜commitment：Management commits to investing ahead of the curve（原話："we're committed to continuing to invest ahead of the curve"）
- 2026-07-28｜John Murphy (CFO)｜commitment：Focus on quality rather than quantity of investment, using AI and digital（原話："rather than just focus on the quantity of investment"）
- 2026-07-28｜John Murphy (CFO)｜commitment：Ambition stated to be at higher end of 4%-6% long-term algorithm on sustained basis（原話："the ambition clearly is to be at the higher end of that"）
- 2026-07-28｜Henrique Braun (CEO)｜commitment：Said in advance that 2026 would see balanced volume and price/mix growth（原話："a year that we would have a balanced growth on volume"）
- 2026-07-28｜John Murphy (CFO)｜capital_allocation：Net debt leverage 1.4x EBITDA, below 2-2.5x target range（原話："net debt leverage of 1.4x"）
- 2026-07-28｜John Murphy (CFO)｜capital_allocation：Flexibility to both reinvest and return capital（原話："we have increased flexibility and optionality"）
- 2026-07-28｜John Murphy (CFO)｜risk：IRS dispute: management will vigorously defend position after 11th Circuit oral arguments（原話："We will continue to vigorously defend our overall position"）
- 2026-07-28｜John Murphy (CFO)｜risk：Appellate decision timing unknown, previously referenced 6 to 12 months（原話："that being 6 to 12 months out"）
- 2026-07-28｜Henrique Braun (CEO)｜risk：Low-income consumer pressure continues globally（原話："low income levels continues to be there across the globe"）
- 2026-07-28｜Henrique Braun (CEO)｜risk：China sentiment cautious and selective（原話："sentiment remains cautious and spending continues"）
- 2026-07-28｜Henrique Braun (CEO)｜risk：Mexico described as difficult environment（原話："continue to navigate a difficult environment in Mexico"）
- 2026-07-28｜John Murphy (CFO)｜risk：Q2 volume aided by weather, World Cup, easy comp（原話："favorable weather in certain markets"）
- 2026-07-28｜Henrique Braun (CEO)｜risk：Asia Pacific comparable operating income declined（原話："Comparable operating income declined during the quarter"）
- 2026-07-28｜Henrique Braun (CEO)｜risk：EMEA profit declined due to investment phasing（原話："profit declined due to the phasing of investment"）
- 2026-07-28｜John Murphy (CFO)｜risk：fairlife: no material impact expected in H2 from production incident（原話："nor do we anticipate any material impact to our results"）
- 2026-07-28｜Henrique Braun (CEO)｜product：Mr. Pibb relaunch grew volume more than 20%（原話："Mr. Pibb grew volume more than 20%"）
- 2026-07-28｜Henrique Braun (CEO)｜product：fairlife grew 18% in the quarter（原話："We grew 18%"）
- 2026-07-28｜Henrique Braun (CEO)｜product：Trademark Coca-Cola volume growth strongest in 17 years（原話："strongest volume growth in 17 years"）
- 2026-07-28｜Henrique Braun (CEO)｜product：Coca-Cola Zero Zero redesigned to target evening occasions（原話："evening occasions remain a meaningful untapped opportunity"）
- 2026-07-28｜Steve Powers (Deutsche Bank analyst)｜competition：Analyst notes value share losses in India（原話："you cited some value share losses in India."）
- 2026-07-28｜Henrique Braun (CEO)｜customer：Marriott contract won back after loss（原話："we lost that right to be with them"）
- 2026-07-28｜Henrique Braun (CEO)｜customer：Monster included as part of the Marriott opportunity（原話："Monster being part of our overall portfolio"）

### KO_Cola_Company_Shareholder_Analyst_Call_The_Coca_Cola_Company_20260429.md
- 2026-04-29｜James Quincey｜guidance：管理層對銷量的展望：預期穩健銷量成長（原話："we continue to expect to see steady volume growth"）
- 2026-04-29｜James Quincey｜margin：管理層談國際市場定價：預期定價大致回歸正常（原話："we expect the pricing to broadly normalize."）
- 2026-04-29｜James Quincey｜margin：管理層稱部分市場須隨通膨調價以反映投入成本（原話："we have to price with inflation as that affects"）
- 2026-04-29｜James Quincey｜customer：管理層引述 Q1 北美銷量成長 4%（原話："we reported strong results in North America with 4%"）
- 2026-04-29｜Jennifer Manning｜competition：股東提問：如何在價格上保持競爭力並留住消費者（由秘書宣讀）（原話："staying competitive on price and retaining consumers"）
- 2026-04-29｜James Quincey｜competition：管理層說明以多元包裝規格與價位提供選擇（原話："providing choice and meeting consumers where they are"）
- 2026-04-29｜James Quincey｜product：管理層稱 GLP-1 對整體非酒精飲料支出影響有限（原話："a limited overall impact on total nonalcoholic"）
- 2026-04-29｜James Quincey｜product：管理層引用 2024 年低/無卡飲料占全球銷量比重（原話："30% of it was low or no calorie beverages."）
- 2026-04-29｜James Quincey｜product：管理層引用前 20 大品牌中減糖或零糖比重（原話："18 of our top 20 brands are reduced or zero sugar products"）
- 2026-04-29｜James Quincey｜product：管理層稱新增兩個十億美元品牌，總數 32 個（原話："have added 2 more billion-dollar brands"）
- 2026-04-29｜James Quincey｜product：管理層稱對乳製品業務有數十億美元投資（原話："multibillion-dollar investments, for example, in our dairy"）
- 2026-04-29｜James Quincey｜product：管理層說明可重複填充包裝非即插即用方案（原話："refillables aren't a simple plug-and-play solution."）
- 2026-04-29｜James Quincey｜product：管理層引用 2024 年可重複填充包裝占全球銷量比重（原話："14% of our overall beverage volume"）
- 2026-04-29｜Henrique Braun｜product：CEO 談 AI 在聖誕廣告製作的成本影響（原話："we're doing that actually with a fraction of the cost"）
- 2026-04-29｜Henrique Braun｜commitment：CEO 談數位／AI 投入將帶來財務成果與報酬（原話："we're going to deliver a real finance results and returns"）
- 2026-04-29｜Henrique Braun｜commitment：CEO 定位公司為非科技公司，技術用於降低複雜度（原話："we are not a tech company, but we use the technology"）
- 2026-04-29｜Henrique Braun｜product：CEO 對復出 TaB 的回應：不確定是否有計畫（原話："While I can't say whether there is anything planned"）
- 2026-04-29｜James Quincey｜capital_allocation：管理層稱資本配置先從再投資事業開始（原話："always start by focusing on what do we need to reinvest"）
- 2026-04-29｜James Quincey｜capital_allocation：管理層列出再投資後的資金用途（原話："share buybacks, opportunistic opportunities for bolt-on M&A"）
- 2026-04-29｜James Quincey｜capital_allocation：管理層稱目前淨負債槓桿低於目標區間（原話："now we are below our target net debt leverage"）
- 2026-04-29｜James Quincey｜capital_allocation：管理層稱股利由長期自由現金流支持（原話："it is importantly well supported by our long-term"）
- 2026-04-29｜James Quincey｜commitment：管理層承諾優先事業投資（原話："absolutely committed to prioritizing business investment"）
- 2026-04-29｜James Quincey｜commitment：Quincey 卸任 CEO 後續任執行董事長（原話："continue to serve as executive chair."）
- 2026-04-29｜James Quincey｜risk：管理層稱永續策略已整合入全天候策略（原話："fully integrated into the company's all-weather strategy"）
- 2026-04-29｜Paul Chesser｜risk：股東提案方稱公司於 2024 年 12 月將包裝目標期限延至 2035（原話："rolled back all of its goals pushing every deadline to 2035"）
- 2026-04-29｜James Quincey｜risk：管理層對成分風險提案回應：成分獲各地食安機關授權（原話："authorized for use by leading food safety"）
- 2026-04-29｜James Quincey｜risk：管理層承認科學會演進（原話："We recognize that science evolves"）
- 2026-04-29｜Jennifer Manning｜risk：高層薪酬諮詢投票結果（原話："compensation has received an affirmative vote of 91%"）
- 2026-04-29｜Jennifer Manning｜risk：成分風險提案得票結果（原話："vote of 11.12% and, therefore, did not pass."）
- 2026-04-29｜Jennifer Manning｜risk：永續揭露提案得票結果（原話："vote of 22.11% and, therefore, did not pass."）

### 問答異常語氣（迴避／改口／保留）
- KO_Q2_2026_Earnings_Call_20260728.md｜問：Falorni: how much uplift from the World Cup and does it continue into Q3｜答法：Did not give a number; said it is difficult to quantify the impact
- KO_Q2_2026_Earnings_Call_20260728.md｜問：Carey: capital allocation if tax case outcome is positive｜答法：CFO covered timing and best/worst case but did not address capital allocation
- KO_Q2_2026_Earnings_Call_20260728.md｜問：Herzog: less spending in H2 vs H1 and advertising strategy｜答法：No yes/no on H2 spend; answered on investment quality and said guidance reflects below-the-line benefits
- KO_Q2_2026_Earnings_Call_20260728.md｜問：Gajrawala: should growth be at high end of algorithm as a base｜答法：CEO restated degrees of freedom and not to read one quarter; CFO added ambition is higher end sustained, no base-level commitment
- KO_Q2_2026_Earnings_Call_20260728.md｜問：Dara: is Webster capacity ramp on track｜答法：CEO said plan in line for rest of year without a specific Webster timing
- KO_Cola_Company_Shareholder_Analyst_Call_The_Coca_Cola_Company_20260429.md｜問：股東問為何不願出資建設可重複填充包裝基礎設施｜答法：未直接回答是否投資，改談需多方投資、各地差異與回收再利用
- KO_Cola_Company_Shareholder_Analyst_Call_The_Coca_Cola_Company_20260429.md｜問：股東問是否考慮限量復出 TaB｜答法：未給計畫，稱不確定目前是否有安排，僅說會納入考量

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
{"date":"20260729","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"全球商業飲料的量能基礎不被 GLP-1 與健康監管結構性破壞——KO 的兩年平均單位箱量成長維持在 +2% 上下，且無糖化與小包裝策略足以承接需求形態的改變"},{"id":"H2","text":"定價與組合每年能貢獻 3-4pp 的營收成長，且不抑制需求——這是 KO 長期演算法中最關鍵的一項，因為它是無資本成本的成長"},{"id":"H3","text":"市場對「確定性」的溢價不會系統性下移——退出倍數維持在前瞻本益比 20-22x 的區間，而非回到 2018-2019 年的 20x 以下或成熟必需消費品的 16-18x"}],"extra_text":"# | 具體數字門檻（floor） | 信息來源 | 漂移觸發條件\nH1 | 兩年平均單位箱量成長 ≥ +1.5%（本季 +2%）；單季單位箱量不連續兩季轉負 | 兩年平均 +2%、本季 +5%、商標可口可樂 +5%（剔除疫後修復後 17 年最強）、Powerade +8%：KO Q2 2026 法說（2026-07-28）；管理層另明言「回看 2017 年以來大致就在 2% 這個水準」 | 連 4 季兩年平均低於 +1%（5Y 假設）→ 削弱；出現連續兩年的年度負成長 → 反轉。單季受天氣或活動影響不觸發。\nH2 | 價格／組合年度貢獻 ≥ +3%；可比營業利益率年度不下滑 | 本季價格／組合 +2%（定價 +3pt、組合 −1pt，管理層明言組合逆風主要來自亞太投資時點）、可比毛利率 +120bp、可比營業利益率 +90bp：KO Q2 2026 法說；全年有機營收指引約 +5%（上修至原區間上緣）：同上 | 連 2 季價格／組合轉負（2Y 假設）→ 削弱；連 4 季轉負 → 反轉。\nH3 | 前瞻本益比（FY+2）≥ 20x | 本報告自算之 5 年前瞻本益比（FY+2 口徑）分布：低 16.94x／p25 19.23x／中位 20.06x／p75 21.06x／高 25.22x，現值 25.22x（即區間高點）；第三方資料庫記錄之前瞻本益比 24.6x 較同業非酒精飲料中位 16.5x 溢價 49%（2026） | 連 4 季低於 18x（5Y 假設）→ 削弱（市場重新以成熟必需消費品框架定價）；連 6 季低於 16x → 反轉。"},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"下半年比較基礎轉為逆風，本季的強勁被證實為一次性。管理層已主動預告三項：易比較基期消失、第四季少 6 天（日曆調整）、非洲裝瓶事業出售帶來 2-3% 的營收逆風。本季 +5% 的銷量另有天氣與世界盃助力，兩年平均僅 +2%。"},{"id":"R2","text":"估值均值回歸。前瞻本益比（FY2027E）25.22x 為本報告 5 年區間高點，PEG 3.73。回到 5 年中位 20.06x 即為 −20% 的價格重估，且不需要任何基本面惡化。"},{"id":"R3","text":"美國國稅局移轉訂價案敗訴。案件源自 2007-2009 稅務年度的查核，爭點是國稅局單方面放棄雙方沿用多年、且載於 1996 年結案協議的「10-50-50」分配方法。總曝險約 200 億美元（稅款加利息），公司已支付約 60 億（勝訴可回收），敗訴另需約 140 億；但帳上僅提列 4.93 億美元準備（以「較可能不成立」基礎認列）。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE(FY2027E) ≤ 21x（約 $73.5，＝自身 5 年中位）；或 FY2027 共識上修使該倍數自然回落至 21x 以下","irr_base_pct":5.3,"ev5y_pct":7.4,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.1,"ev5y_pct":7.4,"irr_base_pct":5.3,"max_dd_pct":-40.0,"bull_5y_price":126.0,"bear_5y_price":62.0,"p_bull_pct":22.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE(FY2027E) ≤ 21x（約 $73.5，＝自身 5 年中位）；或 FY2027 共識上修使該倍數自然回落至 21x 以下","price_at_dd":88.27,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KO_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
