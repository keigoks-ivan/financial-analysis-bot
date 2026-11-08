你是 stock-analyst **v20 判斷 agent**，標的 CELH（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CELH","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":847.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m（YoY +16.8%，QoQ +3.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm"},"note":"查無共識（新聞稿未載）"},{"id":"f_kpi1_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未報 non-GAAP 營業利益，以此代）","value":198.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m（利益率 23.4%，YoY −3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm"},"note":"查無共識（新聞稿未載）"},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":172.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m（利益率 20.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm"},"note":"查無共識（新聞稿未載）"},{"id":"f_kpi3_free_cash_flow_ocf_capex","label":"Free cash flow（OCF−capex，由 10-Q 累計數相減推算）","value":127.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m（Q3 OCF 153.9 − capex 26.2）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"SEC 10-Q Q3 2026 celh-20260930.htm 九個月累計 450.2/51.2 減 10-Q Q2 六個月 296.3/25.0"},"note":"查無共識（新聞稿未載）"},{"id":"f_kpi5_adjusted_diluted_eps","label":"Adjusted diluted EPS","value":0.41,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD（GAAP 0.39）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm"},"note":"goldesel.de 二手：預期 0.34（未經 IR 證實，僅參考）"},{"id":"f_kpi6_gross_margin","label":"Gross margin","value":46.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm"},"note":"查無共識（新聞稿未載）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_celh_gross_margin_pct","label":"CELH 毛利率","value":47.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_celh_operating_margin_pct","label":"CELH 營業利益率","value":17.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_celh_fcf_margin_pct","label":"CELH FCF 利潤率","value":6.09,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ko_gross_margin_pct","label":"KO 毛利率","value":62.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ko_operating_margin_pct","label":"KO 營業利益率","value":32.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ko_fcf_margin_pct","label":"KO FCF 利潤率","value":27.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pep_gross_margin_pct","label":"PEP 毛利率","value":54.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pep_operating_margin_pct","label":"PEP 營業利益率","value":15.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pep_fcf_margin_pct","label":"PEP FCF 利潤率","value":10.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mnst_gross_margin_pct","label":"MNST 毛利率","value":55.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mnst_operating_margin_pct","label":"MNST 營業利益率","value":29.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mnst_fcf_margin_pct","label":"MNST FCF 利潤率","value":22.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kdp_gross_margin_pct","label":"KDP 毛利率","value":48.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kdp_operating_margin_pct","label":"KDP 營業利益率","value":14.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kdp_fcf_margin_pct","label":"KDP FCF 利潤率","value":9.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":5.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%（SBC 8.7 USD m；占營收 1.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm"},"note":"查無共識（新聞稿未載）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":32.16,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-0.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":68.01,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.42 → 1.42）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.7 → 1.7）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.96 → 1.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.42,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.7,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":1.96,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-1.39,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.44 → 1.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":36.13,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.54,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.53,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":22.65,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.42，分子＝快照價 32.16","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-25.92,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 674.7、現金 700.62（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":250.56,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":8031.97,"period":"2026-11-08","unit":"USD m","basis":"市值 8057.89 ＋ 淨負債 -25.92","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":3184.67,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":3450.04,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.52,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 32.16 / W52 36.47 / W104 38.36 / W250 40.93 / W250 13週斜率 0.43%"},{"id":"f_ma_w52","label":"52 週均線","value":36.47,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":38.36,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":40.93,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.43,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：公司自述功能性飲料競爭激烈，可能難以維持營收、市佔；私有品牌與其他健康／運動表現品牌競爭可能加劇，造成價格侵蝕、市佔下降或促銷費用增加","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"In addition, competition from private-label and other wellness or performance brands could intensify. These competitive pressures may result in price erosion, reduced market share or increased promotional expenses, any of which could have a material adverse effect on our business, financial condition, results of operations and cash flows.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"FY2025 10-K MD&A：公司自述新進入者或採激進定價的競爭者增強，會顯著衝擊市佔與獲利","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"The entry of new or strengthening competitors who employ aggressive pricing strategies can significantly impact our market share and profitability.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 合併品牌（Celsius、Alani Nu、Rockstar）占美國能量飲料約20.9%美元份額，較Q1 2025 Celsius單一品牌高1,000bp；Celsius品牌零售額+6%、Rockstar -13%（Zacks摘要）","source":"Zacks／Metatrader 轉載「Celsius Holdings' Portfolio Reaches 20.9% Share: More Gains Ahead?」","url":"https://www.metatrader.com/en/news/1736574-celsius-holdings-portfolio-reaches-209-share-more-gains-ahead","excerpt":"the Celsius Holdings portfolio reached an approximate 20.9%-dollar share of the U.S. energy drink category in tracked channels; portfolio share was up 1,000 basis points compared with CELSIUS' standalone share in the first quarter of 2025","as_of":"2026-05-08","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Q3 2025 Celsius品牌美元份額年減約0.5點至11.2%（零售額+13%）","source":"Zacks／Metatrader 轉載","url":"https://www.metatrader.com/en/news/1736574-celsius-holdings-portfolio-reaches-209-share-more-gains-ahead","excerpt":"the CELSIUS brand posted 13% retail sales growth but experienced a 0.5-point year-over-year decline in dollar share to 11.2%","as_of":"2026-05-08","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K 揭露 PepsiCo 占營收與應收款高比例，且限制公司快速轉換其他經銷安排的彈性","source":"Celsius FY2025 10-K","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"Given the significant concentration of our supply chain with Pepsi, Pepsi can influence our strategic decision making as we seek to expand and grow our product lines, and any significant disagreement or a termination of our arrangements with Pepsi could prevent us from distributing our products and would have a material adverse","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：多數製造外包給 co-packer，2024-11-01 收購一家 co-packer，仍難以快速轉換替代 co-packer","source":"Celsius FY2025 10-K","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"of our co-packers to manufacture our products as required, we would need to secure the services of alternative co-packers. We may be unable to procure alternative packing facilities at commercially reasonable rates or within a reasonably short time period, and any such transition could be costly. In addition, although we acquired one of our co-packers on November 1, 2024, such","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：2025 年對 Pepsi 銷售占總營收 43.2%，Pepsi 應收占總應收 46.2%；失去 Pepsi 可能造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"In 2025, sales to Pepsi constituted 43.2% of our total revenue. As of December 31, 2025, receivables from Pepsi represented 46.2% of our total receivables. The loss of Pepsi or Pepsi's affiliates as our customers could significantly impact our operations, potentially resulting in a material adverse effect on our financial results.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Q3 2026 10-Q：Pepsi 占截至 2026-09-30 九個月營收 61.3%、應收帳款 58.5%。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000062/celh-20260930.htm","excerpt":"Revenue from customers accounting for more than 10.0% of total revenue is as follows: Three Months Ended September 30, Nine Months Ended September 30, 2026 2025 2026 2025 Pepsi 64.6 % 35.4 % 61.3 % 38.5 %","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q3 2026（13週至2026-09-27）Celsius 組合美國追蹤通路零售額年增14.7%、RTD能量飲料美元份額約20.7%；Alani Nu +57.9%（份額9.8%），CELSIUS 品牌 -7.0%（份額9.1%，主因產品組合優化），Rockstar -13.2%（SKU精簡）","source":"Celsius Holdings 8-K Q3 2026 earnings release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q1 2026 Celsius 組合貢獻美國零糖能量飲料品類 $8億成長的45%；2025全年貢獻品類 $33億零糖成長的33%（公司自述）","source":"Celsius Holdings Q1 2026 results / Nasdaq-Zacks 'CELH and Zero-Sugar Energy Trends to Watch Through 2026'","url":"https://www.nasdaq.com/articles/celh-and-zero-sugar-energy-trends-watch-through-2026","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Statista 預測全球能量與運動飲料營收成長率2024–2027連續下降，2027年約3.32%（第四年下滑）；各研調機構預測差異大（CAGR 5.7%–7.8%）","source":"Statista, revenue growth energy drinks worldwide","url":"https://statista.com/statistics/1345618/revenue-growth-energy-drinks-worldwide","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"管理層點出商品與運費波動、品類促銷強度為風險；另有Costco Kirkland能量飲料等競品","source":"Celsius Holdings Q1 2026 results (BusinessWire)","url":"https://www.businesswire.com/news/home/20260507453822/en/Celsius-Holdings-Reports-First-Quarter-2026-Financial-Results/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K FY2025 Item 3 述及公司受監管機關之檢查、資訊要求、傳票與調查，但未點名反壟斷調查；一手紀錄中無反壟斷／拆分事件。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"We are also subject to regulatory and governmental examinations, information requests and subpoenas, inquiries, investigations and threatened legal actions and proceedings.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"廣告與促銷受 FTC 法及州消費者保護法規範；任何政府或私人訴訟行動可能產生重大不利影響（風險因子，非已發生案件）。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"Any actions or investigations initiated against our business by governmental authorities or private litigants could have a material adverse effect on our business, financial condition, results of operations and cash flows.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：關稅（含鋁）可能提高原料與包裝成本；至今未對營運結果造成重大影響，但價格轉嫁能力受競爭限制。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"While tariffs have not materially impacted our results of operations to date, inflationary trends affecting commodities, freight, labor and fuel can also increase our cost base and reduce margins.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K MD&A：關稅已影響且可能持續影響供應鏈（含鋁包材成本），未來影響難以合理估計。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"The rapidly changing nature of global trade policies and tariff regulations introduces uncertainty, making it difficult to reasonably estimate potential future impacts from such policies and regulations.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：出口管制／制裁及進出口法規變動可能影響產品出口與國際經銷。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"Changes in export and import regulations, economic sanctions and related laws, shifts in the enforcement or scope of existing regulations, changes in the countries, governments or persons targeted by such regulations and the imposition of tariffs may create delays in the introduction and sale of our products in international markets","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Celsius 不自有工廠，生產外包給第三方 co-packer；FY2023 10-K 稱已建北美 co-packer 與倉儲網路以限制單一區域曝險；FY2024 10-K 稱 12 oz 專有罐只有少數供應商可供，且曾因鋁罐短缺進口海外罐子影響 2021–22 毛利。","source":"Celsius Holdings 10-K FY2022/FY2023/FY2024（搜尋摘要彙整）","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176625000024/celh-20241231.htm","excerpt":null,"as_of":"2025-02-28","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q1 2026 10-Q 將鋁罐成本列為主要市場風險，公司目前未使用避險工具，且轉嫁成本能力受競爭限制；FY2025 10-K 有獨立的關稅／全球供應鏈中斷風險因子。","source":"Celsius Holdings Form 10-Q Q1 2026 / 10-K FY2025（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000039/celh-20260331.htm","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 營收 $847.2M，年增 16.8%；Alani Nu 約 +24% 至 $410.1M，CELSIUS 品牌約 -6% 至 $356.8M（SKU 精簡、出貨時點、club 通路疲弱），Rockstar $80.3M；毛利率 46.8% 對 51.3%（鋁與燃料成本、DSD 占比）","source":"Celsius Q3 2026 earnings coverage (搜尋摘要，引 8-K/10-Q)","url":"https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000062/celh-20260930.htm","excerpt":null,"as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q1 2026 Circana 口徑：Celsius 組合占美國 RTD 能量飲料金額約 20.9%（CELSIUS 9.9%、Alani Nu 約 9%、Rockstar 2.0%）；Alani Nu 零售額 +100%、CELSIUS +6%、Rockstar -13%","source":"Celsius Q1 2026 results via Seeking Alpha / MarketChameleon (搜尋摘要)","url":"https://marketchameleon.com/articles/b/2026/5/7/celsius-holdings-record-q1-2026-energy-drinks-market-share-leadership","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"CFO 警告 Q4 因年底促銷時點、整合工作與大客戶現金管理而有雜訊，Alani Nu 在 Pepsi 體系擴大舖貨","source":"Stocktwits","url":"https://stocktwits.com/news-articles/markets/equity/celsius-cfo-warns-of-q4-noise-amid-alani-nu-pepsi-rollout-but-retail-goes-contrarian/cL2twoqRERY","excerpt":null,"as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 風險因子僅談共同包裝商、原料、關稅與資安，未列出取代 Celsius 核心產品的新興技術；替代壓力見於競品與自有品牌（搜尋摘要）","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"The Alani Nu and Rockstar acquisitions have expanded our portfolio into new energy and wellness segments, which may create overlap in consumer bases, retail placement or brand positioning.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Costco Kirkland 自有品牌能量飲 2026 年 3 月底推出，對 Celsius 股價形成壓力","source":"Fool/Yahoo Finance: Where Will Celsius Stock Be in 5 Years?","url":"https://finance.yahoo.com/markets/stocks/articles/where-celsius-stock-5-years-134000688.html","excerpt":"Costco Wholesale, for example, launched cheaper energy drinks under the Kirkland private label in late March, which hit Celsius shares. Celsius isn't a fad product.","as_of":"2026-04-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"AlixPartners 模型估 GLP-1 藥物使能量飲與咖啡約 4% 年化下滑","source":"AlixPartners: GLP-1 drugs stir change in the beverage industry","url":"https://www.alixpartners.com/insights/102jz6g/glp-1-drugs-stir-change-in-the-beverage-industry/","excerpt":"Consumers on GLP-1 medications had a stronger tendency to shift from high-sugar, high-calorie dietary content. Soft drinks were unsurprisingly the most disrupted in the beverage category, followed by coffee, energy drinks and juices.","as_of":"2025-08-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Pepsi 成為 Celsius、Alani Nu、Rockstar 在美加的主要經銷商；Alani Nu 原經銷商被終止、區域權利移轉給 Pepsi，Pepsi 補償終止費最多 2.75 億美元（遞延收入、約 17 年攤銷）。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"In connection with expanding Pepsi’s distribution responsibilities to include Alani Nu, we terminated certain former Alani Nu distributors and transitioned territory rights to Pepsi. Pepsi agreed to reimburse us for distributor termination fees up to $275.0 million, to facilitate this transition.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026-05-21 修約再把部分前 Alani Nu 區域移給 Pepsi，Pepsi 補償 8,110 萬美元終止費（摘要轉述）。","source":"WebSearch 摘要（引 10-Q FY2026）","url":"https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000050/celh-20260630.htm","excerpt":"A May 21, 2026 amendment moved more former Alani Nu territories to Pepsi. Pepsi agreed to reimburse $81.1 million in related distributor termination fees, and the company says it has now received and used all of that money.","as_of":"2026-08-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"2026Q3 毛利率 46.8%（去年同期 51.3%），10-Q 歸因於通路組合（DSD 比重上升）與鋁、燃料成本；CELSIUS 品牌營收約 -6%，原因含 SKU 優化、庫存再平衡出貨時點與量販（club）通路疲弱。","source":"Celsius 10-Q 2026Q3（經 WebSearch 摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000062/celh-20260930.htm","excerpt":"The decrease in gross profit margin was primarily driven by channel mix, including a higher mix of DSD sales, and increased commodity costs, primarily aluminum and fuel.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Chartmill 截至 2026-10-25：FY2026 EPS 共識 $1.47（28 位分析師）；下一季營收預估近 3 個月下修 7.57%，下一財年 EPS 約下修 11%（Q3 財報 11/5 前快照）","source":"Chartmill CELH Earnings & Revenue Estimates","url":"https://www.chartmill.com/stock/quote/CELH/estimates","excerpt":"The next earnings revenue estimate has been revised downward by 7.57% in the past 3 months.","as_of":"2026-10-25","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Investing.com：12 個月平均目標價約 41.10 美元，高 64、低 26；頁面列 2026-10 JPMorgan、UBS 更新；與其他聚合站（約 55–66）差距大，來源日期不一致","source":"Investing.com UK CELH","url":"https://uk.investing.com/equities/celsius-holdings","excerpt":"The average 12-month price target for Celsius is 41.10 USD, with a high estimate of 64 USD and a low estimate of 26 USD.","as_of":"2026-10-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"StockAnalysis 引 S&P Global 23 位分析師共識 Buy、平均目標價 $60.57；Benzinga 24 位分析師共識目標 $54.96（高 75、低 37），兩者 as_of 未明","source":"StockAnalysis CELH forecast / Benzinga","url":"https://stockanalysis.com/stocks/celh/forecast/","excerpt":null,"as_of":"2026-10-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Morgan Stanley 2026-05 目標價由 $64 降至 $55；Citigroup 2026-04 由 $65 降至 $60 維持買進","source":"MarketBeat Citigroup issues pessimistic forecast for Celsius","url":"https://www.marketbeat.com/instant-alerts/citigroup-issues-pessimistic-forecast-for-celsius-nasdaq-celh-stock-price-2026-04-15/","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露仍有重大未決訴訟（證券、衍生、合約爭議）；Ingrao 衍生訴訟 2025-04 和解（律師費 100 萬美元），並於 2025-12-26 新增原專利/配方方版稅訴訟（每箱 10 美分）。","source":"SEC EDGAR 10-K FY2025 Item 3／Note 17","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"On December 26, 2025, the same plaintiffs filed a new lawsuit against the Company, alleging that they are entitled to perpetual royalties at ten cents per case on each case of Sparkling Orange Celsius sold domestically from January 1, 2021, and asserting two causes of action, one for breach of contract and a second for an accounting.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 11 份 8-K 中僅 1 份含重大項目（2026-07-15 Item 1.01 信貸協議相關），無 2.01 併購完成、4.02 重編、1.03 破產等項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341766&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 2.01 併購完成；唯一重大項目為 2026-07-15 Item 1.01（UBS 信貸協議再融資相關），非併購。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341766&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K 載明有針對公司的 channel stuffing 集體訴訟、虛假廣告集體訴訟，及重大證券、衍生、合約爭議未決。","source":"SEC EDGAR 10-K FY2025 Item 1A／Item 3","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"Certain of these matters involve pending legal proceedings that are material to the Company, including securities, derivative and contractual disputes.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2025-12-26 新增版稅訴訟（每箱 10 美分、自 2021-01-01），公司否認並將抗辯，結果無法預估。","source":"SEC EDGAR 10-K FY2025 Note 17","url":"https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm","excerpt":"The Company has not yet been served with process in the lawsuit but denies any wrongdoing and intends to vigorously defend the suit. The Company cannot predict or estimate the duration or ultimate outcome of this matter.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#2","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Pomerantz 於 2026-06 宣布調查 CELH 證券詐欺主張（律所新聞稿，非法院申報）。","source":"Pomerantz Law Firm 新聞稿（Barchart／AccessNewswire）","url":"https://www.barchart.com/story/news/2431814/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-celsius-holdings-inc-celh","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"CELH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.95,"operating_margin_pct":17.5,"fcf_margin_pct":6.09,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":62.32,"operating_margin_pct":32.11,"fcf_margin_pct":27.97,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PEP","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":54.17,"operating_margin_pct":15.32,"fcf_margin_pct":10.66,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MNST","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.55,"operating_margin_pct":29.16,"fcf_margin_pct":22.58,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KDP","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.04,"operating_margin_pct":14.84,"fcf_margin_pct":9.11,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"CELH"},"financial_history":{"ticker":"CELH","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":653604000.0,"revenue_yoy_pct":null,"gross_margin_pct":41.44,"operating_margin_pct":-24.14,"net_income":-187282000.0,"diluted_eps":-0.88,"free_cash_flow":99918000.0,"fcf_margin_pct":15.29,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":1318014000.0,"revenue_yoy_pct":101.65,"gross_margin_pct":48.04,"operating_margin_pct":20.21,"net_income":226801000.0,"diluted_eps":0.77,"free_cash_flow":123785000.0,"fcf_margin_pct":9.39,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":1355630000.0,"revenue_yoy_pct":2.85,"gross_margin_pct":50.18,"operating_margin_pct":11.49,"net_income":145074000.0,"diluted_eps":0.45,"free_cash_flow":239508000.0,"fcf_margin_pct":17.67,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":2515269000.0,"revenue_yoy_pct":85.54,"gross_margin_pct":50.39,"operating_margin_pct":18.63,"net_income":107999000.0,"diluted_eps":0.25,"free_cash_flow":323375000.0,"fcf_margin_pct":12.86,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CELH/CELH_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Celsius Holdings, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Hello, everyone. Thank you for joining, and welcome to the Celsius Holdings Third Quarter 2026 Earnings Conference Call. [Operator Instructions].
I will now hand the call over to Paul Wiseman, Investor Relations. Please go ahead.

**Paul Wiseman** (Executives):
Good morning, and thank you for joining Celsius Holdings Third Quarter 2026 Earnings Webcast. With me today are John Fieldly, Chairman and CEO; Jarrod Langhans, Chief Financial Officer; and Toby David, Chief of Staff. We'll take questions following the prepared remarks. Our third quarter earnings press release was issued this morning with all materials available on our website, ir.celsiusholdingsinc.com and on the SEC's website, sec.gov. An audio replay of this webcast will be accessible later today.
Today's discussion includes forward-looking statements based on our current expectations and information. These statements involve risks and uncertainties, many beyond the company's control. Celsius Holdings disclaims any duty to update forward-looking statements, except as required by law. Please review our safe harbor statements and risk factors in today's press release and in our most recent filings with the SEC, which contain additional information and a description of risks that may result in actual results differing materially from those contemplated by our forward-looking statements.
We will present results on both a GAAP and non-GAAP basis. Non-GAAP measures like adjusted EBITDA, adjusted EBITDA margin, adjusted diluted earnings per share, adjusted SG&A and adjusted SG&A as a percentage of revenue and their GAAP reconciliations are detailed in our third quarter press release, and non-GAAP financial measures should not be used as a substitute for our results reported in accordance with GAAP.
With that, I'll turn it over to John.

**John Fieldly** (Executives):
Thank you, Paul. Good morning, everyone, and thank you for joining us today to discuss our third quarter 2026 results. We delivered the third quarter revenue of approximately $847 million, up approximately 17% year-over-year. Alani Nu delivered the strongest quarter in the brand's history, led by Witch's Brew, the largest limited time offer in our portfolio's history. Brand CELSIUS performed in line with expectations we set out last quarter, setting the stage for the brand being back to expected growth across 2027. Rockstar remained stable quarter-over-quarter, and we have begun seeing green shoots in a number of areas. And our combined portfolio held approximately 21% dollar share of the energy category in tracked channels, roughly 1 in 5 energy drinks purchased in the United States. As we just saw at NACS, the largest convenience store showcase in the U.S., Energy remains one of the strongest performing categories in beverage, and our portfolio is key to driving that growth. Our modern energy brands contributed approximately 28% of Zero Sugar energy category growth in the third quarter.
Retail sales for our portfolio and tracked channels grew approximately 15% year-over-year in the third quarter, consistent with the second quarter, and we continue to bring new consumers into the category and win new occasions with them. We manage the business as a portfolio with each brand playing a distinct role. CELSIUS is the performance brand for active, health-conscious consumers. Alani Nu wins on flavor and self-expression and is an entry point for new female consumers to the category. Rockstar reaches the traditional energy consumer through gaming, motorsports and music. Together, these brands give us ways of growing across more channels, more occasions and more price points. That is the power of managing a portfolio and the third quarter is a good example of it.
To fully capitalize on these opportunities, we're also evolving how we organize and lead our business. Today, we announced the establishment of 3 brand-led business units: CELSIUS, Alani Nu and Rockstar and Emerging Growth, each led by a dedicated brand President responsible for its strategy, growth and performance. This structure is designed to bring greater focus and speed to each brand while continuing to leverage the scale and capabilities of Celsius Holdings. We're excited to welcome Alex Zigliara as President of Brand CELSIUS in the U.S., bringing more than 2 decades of global CPG and beverage experience, and to announce Rishi Daing's expanded role as President, Rockstar Energy and Emerging Growth. Rishi currently serves as Celsius Holdings' Chief Marketing Officer and will transition from that role as the new organizational structure is implemented. We believe this brand-led structure will enable us to better execute with discipline against our total energy portfolio strategy to drive durable long-term growth by expanding consumer reach and consumption occasions through differentiated brands gaining distribution and shelf space, sustaining innovation, scaling internationally and realizing greater opportunities and efficiencies.
Before moving on, I want to take a moment to acknowledge the recent passing of our Chief Supply Chain Officer, Paul Storey. Paul was a valued member of our leadership team. We are deeply grateful for his many contributions to Celsius Holdings, including the deep bench and the talented team that he developed at Celsius. Our thoughts remain with his family, friends and colleagues during this difficult time. To ensure continuity across our supply chain operations, Seth Nicholas has assumed the role of Executive Vice President, Operations and Interim Chief Supply Chain Officer.
Turning now to our brand performance. Let me start with brand CELSIUS. The quarter played out the way we expected. Retail sales in tracked channels were down approximately 7% year-over-year as we cycled last year's innovation. And on a dollar basis, the quarter ran a lot like the second, as we said it would. Brand CELSIUS is not yet where we want it to be. We have spent this year strengthening the sequencing of the planograms or said another way, getting our faster cars on the track, and that work continues. But it is important to keep in mind that a brand is built with the consumer, not on the shelf. CELSIUS was built one consumer at a time, in the gyms, the run clubs, the daily routines of people who live an active lifestyle. LIVE. FIT. GO is not just a tagline to us. It is a lifestyle of the consumer we serve.
So this fall, we sharpened our focus on the consumer with a multiyear partnership with ESPN College GameDay, putting CELSIUS in front of college football fans every Saturday and every weekend during the season. We are on campus, putting our product in the hands of the next generation of active consumers. We are doing this within the marketing investments we laid out, and we are measuring it the way we measure everything; brand health, new consumers coming into the brand and most importantly, repeat purchases. That is the foundation. This growth comes from what we talked about on our last earnings call, a core set of national SKUs. Retailers are planning 2027 with us earlier than they ever have. And innovation, which was not there to bridge the gap this year, but will be much more prominent in 2027. I'll come back to that in a moment.
Alani Nu delivered the biggest quarter in brand's history with net sales of approximately $410 million, up approximately 24% year-over-year and accelerating from the second quarter. Retail sales in tracked channels grew approximately 58% year-over-year. The story of the quarter was Witch's Brew. Last quarter, we said Witch's Brew would be the biggest limited time offer in the brand's history, and it was. It was the largest limited time offer in our portfolio's history with more than $130 million in retail sales across traditional retail and club. And our core 12-ounce Witch's Brew was nearly 80% ahead of last year. At its peak, it delivered the biggest single week of any item in the Celsius Holdings portfolio has ever delivered on record, more than double the next best. And in that peak week, if Witch's Brew had been its own brand, it would have ranked as the fifth largest energy drink in tracked channels.
What is most important is what sits underneath. Excluding Witch's Brew, core Alani Nu sales in tracked channels grew approximately 50% year-over-year in the third quarter. This is continued evidence that we are bringing new consumers into the brand and keeping them. We are graduating top-performing SKUs into permanent core, which adds stability as the brand scales. And the program sold through at retail, which sets up well for the fourth quarter. Alani Nu's share of the category in tracked channels reached approximately 9.8% in the quarter, up nearly 3 points year-over-year. Importantly, Alani Nu is still underpenetrated in channels where our portfolio is strong, and that remains a clear road map for growth in 2027. Given the brand's tremendous momentum and the opportunities ahead, we're excited to bring dedicated leadership to Alani Nu as part of our new brand-led organizational structure.
For Rockstar, our focus this year has been stabilizing the brand. The brand is tracking in line with expectations we set at the time of acquisition. While total retail sales remained down year-over-year as we cycle the SKUs we exited, the SKUs we are carrying forward are getting healthier. In fact, the year-over-year trend has improved in each quarter since we acquired the brand with the remaining SKUs being within about 1% of last year in the third quarter. We're also seeing broader geographic momentum, more than twice as many states now growing since the end of last year. Our plan for Rockstar in 2027 is simple: Expand distribution, accelerate the velocity of the core and recruit the next generation of Rockstar's consumers. We will do that by going deeper into the platforms that built this brand; music, motorsports and by taking Rockstar into college towns in a way that only Rockstar can. With Rishi Daing now leading the Rockstar and Emerging Growth business unit, we're bringing dedicated leadership and greater focus on these opportunities ahead.
That brings me to innovation. It is one of the biggest growth drivers in the category, and it was a piece missing from the CELSIUS brand this year. 2027 will look very different. We purposely delayed innovation on brand CELSIUS this year while we brought Alani Nu and Rockstar into the system and that is now behind us. For 2027, we have incredible innovation planned across both CELSIUS and Alani Nu; new flavors, new lines, new permanent SKUs. It's going to be an exciting year. And innovation is already landing in the fourth quarter. CELSIUS Spritz Vibe Shirley Temple is on shelf. Two more Celsius SKUs land around Thanksgiving, and Alani Nu Winter Wonderland, our winter limited time offer launches at the end of November.
Now turning to markets outside the United States. Last quarter, we laid out a road map, focused market entries, strong local partnerships and disciplined launch plans with markets outside the U.S. expected to grow to more than 15% of total revenue over the next 5 years. The third quarter was another step on that path with our non-U.S. market revenue up approximately 56% year-over-year. And when you look at the runway in front of us, the ready-to-drink energy category across our key international markets is in excess of $8 billion and expected to grow double digits next year. Our playbook in Europe is working. In the U.K., France, Ireland, the Netherlands, Belgium, Spain, Portugal, we are building awareness and trial. We are seeing it in the metrics underneath. Our brand tracking shows aided awareness have roughly doubled in both the U.K. and France since early last year. And our share of the category is up year-over-year in every one of our new European markets.
Growth is coming from the right places, quality distribution where our consumers shop and rising rate of sale, not price, Ireland is a great example. Energy has been the growth engine for immediate consumption beverages this year with Modern Energy being the fastest-growing segment. In Australia and New Zealand, growth is well ahead of last year, and Orange has become the #1 CELSIUS flavor in every Australian account. We are also finalizing the select international markets where Alani Nu is planned to launch in 2027. And we'll leverage the learnings, market entry playbooks that have helped Celsius grow globally.
With that, I'll turn the call over to Jarrod to walk through our financials. Jarrod?

**Jarrod Langhans** (Executives):
Thanks, John, and good morning, everyone. I will walk through the quarter by brand, then cover profitability, operating discipline and capital allocation. I will then close with how we are thinking about the fourth quarter as well as a few comments on 2027 planning.
We delivered third quarter revenue of approximately $847 million, up approximately 17% year-over-year as a portfolio. On net sales, there is one timing item I want to call out upfront. Relative to the expectations that we set in August, we did see some benefit from timing of shipments moving into the third quarter that were planned for the fourth quarter. Brand CELSIUS came in a little stronger, and part of that was as a result of the shipment timing as did Rockstar and Alani Nu. This was in the range of $20 million to $25 million.
Looking at the brands, starting with Brand Celsius. Reported net sales were down approximately 6% year-over-year. Retail sales in tracked channels were down approximately 7%. Within that, U.S. orders ran below scans as the system continued to work through inventory, offset by growth in International and Powders, which is not in the tracked data. Dollars per point of distribution improved again versus the second quarter on fewer points of distribution, so the productivity gains we delivered in the second quarter helped. What is most important to stress is that the trade investment on brand CELSIUS as a percentage of gross sales improved year-over-year. That is the revenue growth management program beginning to flow through on the brand. I will go into more detail on this in a bit.
Turning to Alani Nu. Net sales were approximately $410 million, up approximately 24% year-over-year and retail sales in tracked channels grew approximately 58%. Excluding the timing item, Alani Nu growth still accelerated from the second quarter. We have again included a bridge in our earnings deck, so I will focus on the main drivers. The largest item this quarter was Witch's Brew, and the performance was phenomenal. Shipments ahead of the August launch landed in July and August and the products sold through quicker than we had anticipated. The remaining items are the same dynamics we walked through last quarter, a higher mix of DSD volume, which carries higher trade investment and pack mix. As it relates to DSD mix, the third quarter was more consistent with the second quarter as these quarters have largely been fully impacted by the transition to our new DSD system, including bringing on some new markets in the second phase of transitions during 2026. Two points on that. While Witch's Brew was the largest driver of the quarter, the base Alani Nu business grew without it, with core Alani Nu retail sales in tracked channels up approximately 50% year-over-year, excluding the limited time offer.
For Rockstar, net sales were approximately $80 million, up from approximately $67 million in the second quarter. Third quarter revenue was partially driven by a strong performance in Canada due to the timing of orders across the second and third quarter of 2026. With the integration complete and the reconfigured assortment in place, the brand is working towards stability. I want to spend a moment on how we think about the path to stability and then to growth because it is a question we get often. On a scanner basis, total Rockstar retail sales were down approximately 13% year-over-year, and that is in large part from the items we exited. The way I think about the brand is velocity times distribution. Productivity is moving the right way with dollars per point of distribution up approximately 14% versus the second quarter on a more focused assortment. Distribution is where the declines have been. As we cycle the rationalization, that distribution headwind narrows, and that is what allows the velocity gains to show up in the top line. We are not calling a return to growth today, but the building blocks are coming into place.
Third quarter gross margin was 46.8% compared with 48.1% in the second quarter and 51.3% a year ago. In August, we said that at current diesel and aluminum levels, margin expansion was largely offset and that we would expect the third quarter to remain in the high 40s. Since then, both diesel and aluminum prices have moved higher. Aluminum costs remain elevated on both the LME and the Midwest premium and diesel reached its highest level in several years. Outbound freight as a percentage of revenue was slightly favorable versus the second quarter, which reflects the work the operations team has done on freight and the benefit largely offset the increase in diesel. For the full year, depending on commodity fluctuations, we would expect gross margin in the high 40s.
On contra, trade investment as a percentage of gross sales increased modestly from the second quarter. In August, we said the price pack architecture work would deliver an initial impact in the back half and help offset the mix impact of more cases moving through DSD. The initial impact is there. The actions we took earlier in the year began to flow through and slotting fees declined as a percentage of revenue as Alani Nu scaled. This quarter, though, it was outweighed by mix as Alani Nu's growth, including Witch's Brew, moved more volume through DSD. That is why the much larger opportunity sits in the 2027 program, which I will come to.
The 3 buckets I walked through last quarter; integration, structural costs and revenue growth management, have not changed. I will update the first 2 briefly and spend more time on the third. On integration, the improved case costs for Alani Nu and Rockstar are now flowing through, but they are being offset by aluminum. On structural costs, our second manufacturing line in North Carolina is now running with the full benefit to be realized in 2027 and vertical integration and direct sourcing continue to advance.
On revenue growth management, we have seen the initial impact this year and the much larger opportunity is in 2027 because it is a different program than the one we ran this year. In 2026, we built the capability and used it to fix what was in front of us, post-event analysis by promotion and by account and elasticity work at the SKU and account level so that trade dollars go where they earn a return. For 2027, we are moving from tactical decisions to a portfolio level program, and it has 3 parts. First, a clear brand ladder across CELSIUS, Alani Nu and Rockstar so that each brand's pricing reflects its role in the portfolio. Second, a pack architecture that is consistent across the brand, which gives us a cleaner price slope from singles to multipacks and supports the formats coming with the 2027 innovation. And third, a multiyear road map, so pricing and trade are managed as a system rather than as a 1-year event. We are planning 2027 around that program with our retail partners and our DSD partner now, and we would expect trade investment as a percentage of gross sales to improve as it takes hold with the benefits building through 2027 and into 2028.
Selling, general and administrative expenses were $221 million or approximately 26.1% of revenue compared with 29% in the second quarter and 28.4% a year ago. Sales and marketing was $162 million, including the investment behind the fall programming John described and general and administrative expenses was $59 million. Adjusted EBITDA was approximately $199 million or approximately 23.4% of revenue compared with $184 million or 22.5% in the second quarter. The sequential improvement came from operating leverage with SG&A as a percentage of revenues more than offsetting the lower gross margin. Year-to-date, adjusted EBITDA was $578 million or approximately 23.6% of revenue. The year-over-year comparison reflects the gross margin pressure from commodities and the investments we are making behind the brands.
On capital deployment, our balance sheet remains a source of strength and flexibility. During the third quarter, we repurchased approximately $45 million of stock, bringing year-to-date repurchases to approximately $169 million with approximately $91 million remaining under the $300 million authorization. The reason we continue to lean into repurchases is the same as last quarter. Our cash flow return on investment is among the strongest in the beverage category. And at current levels, we view repurchasing our own stock as an attractive use of capital. Our approach continues to be grounded in the same 3 priorities: Investing to support brand growth and execution, maintaining the strength of our balance sheet and returning capital to shareholders.
Moving to the fourth quarter. To give you some context on the factors that will influence reported revenue as we close out the year. First, the comparison. A year ago, the fourth quarter included the inventory build that came with moving Alani Nu into the DSD system, partly offset by inventory reductions on brand CELSIUS. As we noted when we reported the fourth quarter of 2025, that was a net benefit of approximately $25 million to our reported results, and it does not recur. Second, shipment timing. Separate from last year's item, the approximately $25 million of shipments that moved into the third quarter this year comes out of the fourth. Third, contra. Trade investment as a percentage of gross sales will be higher than it was a year ago because a year ago, Alani Nu was not yet carrying a full quarter of DSD economics. Our DSD partner began delivering the brand in the first week of December.
Partly offsetting those, in terms of the timing and sequencing of the 2027 innovation, the first wave loads into the system in November and December with the balance in the first quarter. So some innovation revenue lands in the fourth quarter ahead of the January launches. Putting it together, the fourth quarter is the most difficult comparison of the year on a reported basis, and we expect that reported revenue growth will be below what we delivered through the first 3 quarters. That is a function of the comparison and the timing items I just walked through, not underlying demand, which you can see in the scanner data.
For Rockstar, the fourth quarter is the first quarter with the brand fully in both periods. As a reminder, a portion of last year's fourth quarter Rockstar sales was recorded in other income during the integration, so reported growth will be elevated. On an underlying basis, we would expect sales to trend closer to what we delivered in the first and second quarters of this year. For the full year, we would expect gross margin in the high 40s. And from a portfolio perspective, our focus is on strengthening our brands and execution, service through the network, product displays on the floor and winning at the register through the holiday selling season and into 2027.
Moving to 2027. We are currently wrapping up key meetings with our retail partners and the innovation plans, promotional calendar and activations are being locked in. In addition, our commercial teams are meeting with Pepsi this week to finalize our priorities as well as the timing and sequencing of our various programs and launches. From a 10,000-foot perspective, our plans include brand CELSIUS returning to growth, Rockstar continuing to work towards stability and then growth and Alani continues to benefit from its entrance into the PepsiCo DSD system as well as the outsized growth the brand is delivering as it drives the modern energy category.
With that, I will turn the call back to the operator to open lines for questions.

**Operator** (Operator):
Your first question comes from the line of Peter Grom with UBS.

**Peter Grom** (Analysts):
So I wanted to ask about brand CELSIUS. Can you maybe just talk about expectations for the brand as you look out to 4Q and into '27?
And then related, Jarrod, you touched on all the different moving pieces in 4Q across the total portfolio. But just any thoughts on how we should be thinking about CELSIUS itself, maybe relative to what we might see from a tracked trend standpoint?

**John Fieldly** (Executives):
Yes. Peter, thank you for the question. And great question, fair question. The way we're looking at it, when you look at the third quarter, it played out the way we said it would. On scan dollars, it ran a lot like the second. Year-over-year rate moved down about 7% because of the comparisons. And then a year ago, the brand grew about 3% in tracked channels in the second quarter and about 13% in the third quarter. So when you're looking at the fourth quarter, it's really a lot of the same dynamic. Last year's fourth quarter was up approximately 13% on scanner, including our first limited time offer with the CELSIUS portfolio.
So the turn in consumption shows up as we move through 2027 when we really cycle the rationalization and the innovation is back in the brand and what we've been talking about for '27. We simplified the portfolio in '26. And now we're back to innovation. We have really robust plans. The way we're looking at it, and you look at the kind of the run rate on a weekly basis based on the scanner data. The brand has been running in the $50 million to $55 million range on a weekly basis. As we're exiting the year, there is a few weeks, 2 weeks, where the brand last year dipped down into the $49 million range. So the way we're looking at it, if we can hold within the $50 million range, the brand will be back to slight growth breakeven in a variety of weeks exiting the year.
We do have innovation launching as we talked in our prepared remarks, but that distribution will build over time in 2027. So when you're looking at it, that's the way we're thinking about it. When we're seeing it, we're highly confident. Brand health is strong. We got a variety of tent poles and strategies in place for '27 that we're excited about. But at the end of the day, the register is the scoreboard, and that's what we're focusing on. We're adding additional focus, enhancements to our commercialization from revenue management, portfolio management and we're highly confident in the Celsius portfolio.

**Operator** (Operator):
Your next question comes from the line of Bonnie Herzog with Goldman Sachs.

**Bonnie Herzog** (Analysts):
I had a question on your gross margins. I guess I was hoping you could touch on your expectations for gross margin and the pace of recovery, I guess, maybe in the fourth quarter and then into next year, just in light of the stubborn inflation. And I guess, what levers do you have to help mitigate some of the pressures? And I'm thinking about this in the context of pricing actions. I believe you've already raised prices at certain retailers. So if you could talk about your pricing strategy, that would be helpful.

**John Fieldly** (Executives):
Bonnie, thank you. I'm going to let Jarrod cover that question. As we all know, everyone has been affected by some of the commodity prices, and we are no different. But I'm going to let Jarrod talk about some of those key drivers there.

**Jarrod Langhans** (Executives):
Yes. So let me talk pricing first, and then we can talk the other margin drivers. So our posture is to follow the category rather than lead it. We're positioning CELSIUS and Alani as premium brands. So we don't want to become value brands. And so we don't want to be priced out of that. So with the category leaders taking pricing, it's created room for us, which has created opportunity. We are taking a look at the elasticities to make sure it sticks.
But for our perspective, as we look at 2027, it's not necessarily about that headline price. It's really about the revenue growth management program we're putting into place, looking at price pack architecture by channel, looking at pack strategy, looking at disciplined promotion. So the bigger near-term prize for us is really bringing that contra line down. So price is a part of that infrastructure and a part of that program, but not necessarily the biggest driver and not necessarily where we're just saying there's -- we're taking price everywhere. It's all about going account by account and really working to see what's the best position we can put the portfolio in, whether it's about price pack architecture, different promotions, price increases, those kind of things. So there's a variety of everything within our revenue growth management program, and we're really excited to put that into play in 2027, which will be the first year we're really able to take all 3 brands and really put a focus to that by account.
So that's what kind of where we're thinking on pricing in '27. And then that kind of revenue growth management program will really play out across 2027 and into 2028 and then should be in a really great place from there forward. As we're looking at gross margin outside of pricing, we've got the same key strategies that I talked about on the call. In terms of the -- there's 3 buckets under our control. Those haven't changed. We've got the revenue growth management opportunity. We've got the improvements that we're doing across the board when it comes to our plant in North Carolina as well as some direct sourcing. And then we've got some other things we're doing as a part of the integrations to really drive cost out of the bonds within our portfolio. So we are working through those processes. Improvements in commodities will help us get to the low 50s goal quicker. Unfortunately, right now, the commodities aren't really moving. So it's really working through those other 3 buckets to get our margin expansion, which, unfortunately, because of the commodities, it's going to take a little longer than we had anticipated a year ago.

**John Fieldly** (Executives):
Yes. And as Jarrod mentioned, we really have invested a lot in the revenue management piece. And now that the integration is done, it's time to leverage scale. And that's what really 2027 is all about, maximizing the revenue management, gaining leverage with the portfolio, gaining productivity with our space and allocations. That's going to enhance our margin structure, driving the purchase strategies and unlocking that leverage and then maximizing the benefit. We have a scaled portfolio, almost 21% share in the Energy category. Now the opportunity is to really drive that through.

**Operator** (Operator):
Your next question comes from the line of Kaumil Gajrawala from Jefferies.

**Kaumil Gajrawala** (Analysts):
A couple of quick ones. Just, Jarrod, I know you gave us some back and forth on the timing. But just to make sure, it sounded like you had mentioned that -- or John, you had mentioned that CELSIUS is trending around what you had expected, which was about a down 12%. But does that include $25 million buy ahead, which case it would obviously maybe on run rate be down more than that? And then maybe we take that -- and I think from a modeling perspective, Jarrod, it was the intention to take $25 million out from last year, $25 million from the pull forward out of 4Q. But then how much should we -- like what are your intentions in terms of the inventory build for 2027s innovations?

**John Fieldly** (Executives):
Thank you, Kaumil. What I was referencing is really the scanner data, what's happening at the registers. And that's really -- looking at the overall health of the portfolio, as I mentioned, on a weekly basis, running in the low 50s. So that's what we're really looking at. Now there's puts and takes on the GAAP revenue recognition, and that's what Jarrod really outlined in his prepared remarks. So with that, I'll turn it over to Jarrod to talk more about that. But what I was referencing is specifically the scans at the register, which ultimately is how we track the business and how we scorecard it.

**Jarrod Langhans** (Executives):
Yes. So like John said, mine was more of the GAAP movements. We set some expectations back in August with brand CELSIUS and in particular, brand CELSIUS came in a little bit stronger as did Alani Nu, and that was really, in part, driven by some inventory timing. There was still -- if you go to the deck, we've got kind of a bridge for brand CELSIUS, and it shows kind of the orders versus the scans were still down. They're probably a little less down than we had anticipated, and that was part of the timing of when we had some inventory movement across the very end of the quarter. So there was a little bit of benefit that rolled into Q3 and out of Q4 in terms of that really orders versus scan comparison. So that was where that 2025 comes into play. Some of that was also Rockstar where you see that Rockstar benefited in Canada from some timing of orders where Q2 and Q3 would have had a little bit of a blend of what we delivered in Q3. So that was really mainly just a GAAP thing.
So as we're looking to Q4, there's kind of 3 things to focus on. One is, we talked about Rockstar being more like the Q1, Q2 GAAP reported results as opposed to what we saw in Q3 because of some of that timing. And then if you look at last year, if you combine CELSIUS and Alani as one number, they had a benefit of about $25 million with some inventory being built for Alani and some being pulled down to offset for CELSIUS. And then we had the pull forward that we talked about. That was a bit of all 3 brands benefiting from some pull forward. So those kind of are the 3 things I would factor in as you look at Q4 from a modeling perspective, from a GAAP perspective.

**Operator** (Operator):
Your next question comes from the line of Gerald Pascarelli with Needham & Company.

**Gerald Pascarelli** (Analysts):
Question on Alani regarding the scans versus the reported results. It's been pretty consistent between like negative 34 to 35 percentage points. I understand there are many considerations this year between the DSD mix, the continuation of nonenergy, which you've telegraphed. But just looking ahead, if you can maybe provide some color or thoughts on when you would expect or when we should expect scans and reported results to maybe start to align a little bit more closely?

**Jarrod Langhans** (Executives):
Yes. Probably Q2 next year is the best to kind of get the cleanest. If you look at Q2 and Q3, if you back out kind of the non-RTD, if you back out some of that amortization from the contract, which the amortization will be the same year-over-year. So you won't see that impact next year. And then some of the non-GAAP -- or sorry, non-RTD stuff will be clean once we get to Q1. But because we also had some more transition and we had a second wave of distributors that we brought on in Q1, Q1 was a little bit different. Also we were just rolling into the full DSD system in Q1. So Q1 didn't get impacted as much this year as Q2 and Q3. If you look at Q2, Q3, kind of the delta is in that kind of 24%, 25% range. So that's been pretty consistent over the last 2 quarters. So once we get to Q2, it should be a lot cleaner. But Q1 will still have a little bit of activity in there as we're transitioning more into the DSD system.

**Operator** (Operator):
Your next question comes from the line of Eric Serotta with Morgan Stanley.

**Eric Serotta** (Analysts):
Great. One housekeeping item for Jarrod. Just wanted to come back. I think you made a comment about the fourth quarter growth being, I think, in line or maybe slightly below what you did year-to-date. Can you unpack that since -- are you talking organic or reported since you had additional quarters of the acquisitions in there? And is the way to think of it, you're basically cycling kind of $50 million of timing benefits or cycling $25 million plus another $25 million from the third quarter timing and then whatever is partially offset by inventory trade-ins -- inventory sell-in. So basically minus $50 million plus whatever we assume on the inventory side.
And then zooming back out, John, in terms of the actual CELSIUS takeaway performance during the quarter, it was a bit choppy kind of on a month-to-month basis. TDPs on a year-on-year basis, got a little bit worse. Just wondering what -- if you have any color as to what was happening in terms of the TDP trend and your confidence as to when TDPs start to improve both sequentially and year-on-year. I know there's a lot there.

**Jarrod Langhans** (Executives):
Yes, I'll jump in first from a GAAP basis. I think your summary is reasonable. It's probably more simple than what I said. So kind of that makes the most sense. Now one is from one year, one is from another year. So how do you combine all that? And you kind of laid it out pretty simply from that perspective. But for -- John, do you want to jump in on the other piece?

**John Fieldly** (Executives):
Yes, absolutely, Eric. I think when you look at the choppiness within the quarter, there was a timing on Amazon, and now that's reported. And so there were some timing issues there that we saw, also timing of LTO last year. So those are the main drivers of that. I mean when we look at TDPs, we're going to be cycling the rationalization. So those TDP -- those SKUs will come out. But then we also have more permanent SKUs coming in, in -- will flow through the rest of 2027. So we're really looking at the productivity of the core portfolio, which is extremely important. That's going to not only drive increased top line revenue, but also gross profits and productivity on shelf.

**Jarrod Langhans** (Executives):
Yes. And one more thing, there was a second part of the question you asked me. The kind of the Q4 versus year-to-date, and you mentioned it, it's the acquisition timing. So we didn't have Alani in Q1. We didn't have Rockstar in Q1, Q2, et cetera. So when you're looking at kind of the growth rate in Q4, you're not going to have those benefits. So it's going to be more with the kind of the simple factor you talked about with the $50 million plus the innovation, et cetera.

**Operator** (Operator):
Your next question comes from the line of Michael Lavery with Piper Sandler.

**Michael Lavery** (Analysts):
Just wanted to come back to some of the innovation and brand CELSIUS expectations for next year. I know you pointed to how you expect it to return to growth and you're well positioned for how you see 2027 starting. Maybe can you just touch on how much of that is driven by something like the Energy Plus hydration launch specifically? Or would that be kind of expected to carry the weight? Is that over and above expectations for some base underlying brand CELSIUS growth on kind of existing brands? Or how do those play together? And maybe just touch a little bit too on what's driving such better performance in international.

**John Fieldly** (Executives):
Yes. No. Excellent, Mike. Let me just start off with some of the innovation there. In regards to Energy Plus, which we really showcase at the upcoming NACS. And when you look at Energy Plus, we're really continuing to drive new category consumers and occasions. We know the Energy category continues to grow in new occasions, bringing new consumers in. So this is really incremental to the core and adds benefit and enhancements to the overall trademark. We've done a lot of research. CELSIUS has the right and permission to expand in this adjacent category and opportunity, ties into fitness and health and wellness. The category is expanding and CELSIUS and our modern energy portfolio is leading that.
And when you look at some of the opportunities we have or incrementality, that's where we're playing with this portfolio. But we are extremely focused on the core. And the portfolio growth is not 100% reliant on Energy Plus success. We have a variety of core innovation coming in. As we mentioned in the prepared remarks, we're rolling out in the back half of Q4, and then it will start gaining further distribution throughout '27 as resets take place. We have some great flavor innovation that we're leaning into. Cranberry Apple is a new flavor that's launching, just some really, really core flavors. We're really excited about doing a variety of multipacks. We're also expanding categories and looking at further pack size configurations. As Jarrod mentioned, we're going after 8-ounce, just driving incrementality with that core trademark.
So really excited about the innovation that's in works, already been aligned with key retailers as well. So I think with the enhancements in our investments, strategic alignment, focus and most importantly, as integration is behind us, now we get to maximize this portfolio and the infrastructure we've built with focus on execution and top performance. So really excited there. International did phenomenal this quarter, and we've talked about the last several quarters. I see great opportunity and momentum. We saw great growth. The playbook is working. We're adding -- aided awareness has roughly doubled in the U.K. and France. We're seeing -- we mentioned in prepared remarks, Orange in Australia, #1 flavor in all accounts. We're going to continue with our disciplined approach. We're being very calculated. We have invested in a variety of strategic initiatives, sales, marketing, commercial. And the same growth trends we see in North America, the same growth trends we see internationally. Health and wellness gets stronger. CELSIUS has a right to play within the category. We are building great relationships with international retailers.
And then Alani, we're bringing that to new markets in '27, which we're excited about. We're going to run that same exact playbook, being extremely disciplined. And as we continue to get trial, but most importantly, loyalty and repeat purchases, we're going to continue to invest in. And that will be a big growth driver for the foreseeable future and years to come.

**Operator** (Operator):
And we've reached the end of the Q&A session. I will now turn the call back to Mr. John Fieldly for closing remarks.

**John Fieldly** (Executives):
Thank you for joining us today. The third quarter showed the power of our portfolio, a record quarter for Alani, stability from Rockstar and the foundation set on brand CELSIUS. We entered the fourth quarter with a clear set of priorities. We have innovation landing on shelf with more around Thanksgiving and the Alani Nu Winter limited time offer at the end of November. Brand CELSIUS is back with the consumer who built it, and we are measuring it. And we are planning 2027 with retailer partners earlier than we ever have before, with strong innovation across CELSIUS and Alani Nu behind it.
I want to take this opportunity to thank our employees, our partners and all of our customers for their focus and their teamwork, which has made this all possible. To everyone listening today, we appreciate your support, and we look forward to updating you next quarter. Until then, grab a CELSIUS and LIVE FIT.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CELH_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜John Fieldly (CEO)｜guidance：CELSIUS 品牌第三季預期與第二季相近，年底前回到成長（原話："quarter to look a lot like the second quarter, before we"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：第三季毛利率預期與第二季一致、維持高 40% 區間（原話："we would expect the third quarter to be consistent with the"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：第三季銷售與行銷費用預期與第二季大致一致（原話："We would expect sales and marketing in the third quarter"）
- 2026-08-06｜John Fieldly (CEO)｜guidance：CEO 說明第三季 CELSIUS 週銷速率預期大致相近（原話："somewhat similar within the CELSIUS portfolio."）
- 2026-08-06｜John Fieldly (CEO)｜guidance：分析師問第三季持平指的是金額或比率，CEO 答是看掃描資料的金額（原話："Yes. I think we're talking about the dollars, looking at"）
- 2026-08-06｜John Fieldly (CEO)｜guidance：第四季 CELSIUS 恢復的形狀為緩慢累積（原話："So it will be more of a slow build on the CELSIUS portfolio."）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：CFO 表示掃描資料不會直接反彈（原話："Wouldn't necessarily look for a direct snapback, but that's"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：CFO 說明第四季帳面基期較軟（原話："we do have a softer comp year-over-year that would be seen"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：第四季 CELSIUS 基期較易、Alani 基期較難，均有新品（原話："So we've got an easier comp with brand CELSIUS plus new"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：2027 新品進貨時程尚未定案，下季財報再提供更多資料（原話："It's not fully baked in."）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：CFO 表示下季法說會提供第四季與第一季的更多資料（原話："we'll be able to provide more data on that"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：第二季毛利率約 48%（原話："Second quarter gross margin was approximately 48%, in line"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：毛利率擴張分三塊來談（原話："As we look towards margin expansion, I think about it in 3"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：整合後舊庫存仍使成本有遞延影響（原話："some carryover of higher costs this quarter"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：北卡第二條產線下半年開始生產（原話："Our second manufacturing line in North Carolina begins"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：大宗商品通膨主要為鋁，運費改善抵銷（原話："commodity inflation, primarily aluminum."）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：第二季調整後 EBITDA 金額與占比（原話："Adjusted EBITDA was $184 million or approximately 22.5%"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：上半年調整後 EBITDA（原話："For the first half, adjusted EBITDA was $380 million"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：調整後 SG&A 占營收比（原話："Adjusted SG&A was 28.6% of revenue."）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：CELSIUS 品牌掃描與帳面差距拆成三項（原話："The gap to reported net sales came from 3 things:"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：出貨與消耗差異約占掃描與帳面差距一半（原話："accounted for roughly half of the gap between scanner"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：Alani 剔除加拿大與非即飲後的總營收成長口徑（原話："all-in gross revenue growth was approximately 39%."）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：Alani 第二季淨銷售額（原話："Net sales were approximately $364 million"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：Alani 淨銷售成長對照掃描成長（原話："approximately 21% year-over-year, while retail sales grew"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：Rockstar 第二季淨銷售額（原話："For Rockstar, net sales were approximately $66 million in"）
- 2026-08-06｜John Fieldly (CEO)｜margin：CELSIUS 品牌每配銷點金額較第一季成長（原話："Dollars per point of distribution are up 16% from the first"）
- 2026-08-06｜Jarrod Langhans (CFO)｜capital_allocation：第二季買回約 1 億美元股票（原話："we repurchased approximately $100 million of stock"）
- 2026-08-06｜Jarrod Langhans (CFO)｜commitment：管理層表示將在今年用完 3 億美元買回授權（原話："We intend to continue utilizing the $300 million"）
- 2026-08-06｜Jarrod Langhans (CFO)｜capital_allocation：7 月降息 25 個基點（原話："We also reduced our interest rate by 25 basis points in July"）
- 2026-08-06｜Jarrod Langhans (CFO)｜capital_allocation：買回股票的理由（原話："The reason why we are leaning into repurchases is"）
- 2026-08-06｜John Fieldly (CEO)｜commitment：海外市場未來五年占營收超過 15%（原話："outside of the U.S. to represent more than 15% of our"）
- 2026-08-06｜John Fieldly (CEO)｜commitment：問答中海外占比說法為 15% 且可能更高（原話："15% over time, that we're looking at, and it could be even"）
- 2026-08-06｜John Fieldly (CEO)｜commitment：2027 年將於部分海外市場推出 Alani Nu（原話："markets in which to introduce Alani Nu in 2027"）
- 2026-08-06｜John Fieldly (CEO)｜commitment：Rockstar 整合依 9 個月時程在 6 月完成（原話："we completed the integration in June"）
- 2026-08-06｜Jarrod Langhans (CFO)｜commitment：下半年已開始導入收益管理，2027 年有更大機會（原話："we see a significantly larger opportunity to drive better"）
- 2026-08-06｜Jarrod Langhans (CFO)｜risk：CELSIUS 與 Alani 的貿易促銷與通路組合影響（原話："we saw some negative mix and channel impact"）
- 2026-08-06｜Jarrod Langhans (CFO)｜risk：俱樂部通路疲軟列為帳面落後原因之一（原話："increased trade and promotional investment, and softness in"）
- 2026-08-06｜Jarrod Langhans (CFO)｜risk：第三季 DC 庫存移轉帶來一次性時點影響（原話："This movement will have some onetime timing"）
- 2026-08-06｜John Fieldly (CEO)｜risk：週轉下調 CELSIUS 品牌剔除 SKU 的影響仍存在，管理層承認剔除過深（原話："We went too deep on the CELSIUS"）
- 2026-08-06｜John Fieldly (CEO)｜competition：Alani 在競爭者更多的品類中成長（原話："more competition than ever before, with more entrants and"）
- 2026-08-06｜John Fieldly (CEO)｜competition：CEO 談到同類模仿者（原話："me-too competition out there."）
- 2026-08-06｜John Fieldly (CEO)｜product：CEO 回顧 SKU 剔除決策，表示不會再剔除這麼多（原話："I definitely would have not cut as many SKUs"）
- 2026-08-06｜John Fieldly (CEO)｜product：新品策略改為以永久新品取代尾端 SKU（原話："new innovation that's permanent throughout the year."）
- 2026-08-06｜John Fieldly (CEO)｜product：16 盎司產品線仍是弱處，2027 年初有新品（原話："Where we still have work is our 16-ounce line, and we have"）
- 2026-08-06｜John Fieldly (CEO)｜product：Fizz-Free 追蹤通路美元銷售較上季成長（原話："growing with dollar sales in tracked channels up over 20%"）
- 2026-08-06｜John Fieldly (CEO)｜product：Purple Cotton Candy 為最暢銷新口味（原話："it quickly became our top-selling new flavor in tracked"）
- 2026-08-06｜John Fieldly (CEO)｜product：Witch's Brew 預計為最大限定口味（原話："biggest LTO in history. We have a comp there."）
- 2026-08-06｜John Fieldly (CEO)｜product：Rockstar 被描述為已穩定（原話："Rockstar has stabilized."）
- 2026-08-06｜John Fieldly (CEO)｜product：Rockstar 銷售符合收購時預期（原話："our sales expectations, which we set upon acquiring the"）
- 2026-08-06｜John Fieldly (CEO)｜customer：零售商提早進行 2027 規劃（原話："retailers are leaning in on 2027 planning earlier than they"）
- 2026-08-06｜Jarrod Langhans (CFO)｜customer：陳列空間取得時程比原預期晚（原話："was a bit off from our initial expectations"）
- 2026-08-06｜John Fieldly (CEO)｜customer：百事年度營運會議對齊 2027 計畫（原話："working on our plans for '27 and aligning on plans and"）

### 問答異常語氣（迴避／改口／保留）
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Salera：第四季 CELSIUS 回升幅度是否為中個位數、是快速反彈或漸進｜答法：CEO 未給數字，改說「slow build」並轉給 CFO；CFO 也未給幅度，改說下季再提供資訊
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Teixeira：第四季 Alani 面對高基期怎麼看，以及經銷商相關費用雜訊何時消退｜答法：CFO 表示新品時程「not fully baked in」、下季再提供；未回應費用何時消退
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Serotta：新品擴張的 SKU 增生防護欄為何｜答法：CEO 以持續優化尾端、用永久新品取代作答，未說明具體防護機制或數字
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Grom：未來 6 到 9 個月成功長什麼樣、為何有信心｜答法：CEO 以定性描述（品牌健康、零售商會議、2027 新品）作答，未給指標
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Herzog：SKU 剔除是否正確、第三季是否有更大壓力風險｜答法：CEO 承認剔除過深、會做不同決定，與開場稱此為刻意選擇的框架不同；第三季只答週速率相近、略增

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
{"date":"20260518","verdict":"thesis 仍活 — Q1 26 strong beat(Rev .6M／Adj EPS .41 beat .29 by 41%)、Alani Nu integration ahead of schedule(M synergies)、21% US share(+1000bps YoY)、PepsiCo 11% 戰略持股 + 美加獨家配銷。但 CELSIUS 核心品牌 YoY 僅 +6%(從 +50%+ 大幅減速)、Q1 GM 48.3%(-400bps YoY)、Mgmt FY26 organic Rev guide 僅 +2-4% — 估值🟢(Fwd PE 18.5x／PEG 0.86／分位 <10%) + Pure MA ❌(現價跌穿三條週均)。等 W104 站回或 Q3 26 核心品牌動能回升再建倉 — 訊號 B 觀望，非 C 迴避。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"CELSIUS 核心品牌雖然減速，但能在 2026-2027 重回雙位數成長（+10% to +15%）— 因 (a) 國際擴張接力 + (b) shelf space gains（Q1 26 已獲 +17% shelf space）+ (c) sugar-free 子賽道結構性順風延續","columns":{"2Y 驗證點":"Q4 26 CELSIUS standalone YoY 重回 +10%+（vs Q1 26 +6%）","5Y 驗證點":"CELSIUS standalone 2030 達 .0B Rev（2024 ~.3B → 2030 .0B = ~7% CAGR）","10Y 驗證點":"2034 CELSIUS standalone 達 .5-.0B（國際 50%+ 占比）","具體數字門檻":"2027 CELSIUS standalone YoY ≥ +10%；國際年率 ≥ 0M（vs 2025 ~0M 年率）","信息來源":"Q1 26 earnings call + Mgmt FY26 guidance + Goldman Sachs / Morgan Stanley reports","漂移觸發條件":"連 2 季 TTM CELSIUS YoY"}},{"id":"H2","text":"Alani Nu 整合執行成功 — 透過 PepsiCo 配銷實現 0M+ synergies（vs 已實現 M），且 Alani Nu standalone 維持 +40% pro forma YoY 連 2 年（2026-2027）","columns":{"2Y 驗證點":"Q4 26 Alani Nu pro forma YoY ≥ +40%；累積 synergies ≥ 0M","5Y 驗證點":"2030 Alani Nu Rev .0-.5B（vs 2024 ~.6B standalone = 2-2.5x）","10Y 驗證點":"2034 Alani Nu 達 .0-.0B（建立完整 Gen Z 女性品牌 ecosystem）","具體數字門檻":"2027 Alani Nu YoY ≥ +40%；synergies 累積 ≥ 0M；GM 回到 50%+","信息來源":"Mgmt Q1 26 earnings call disclosure + Investor presentations","漂移觸發條件":"連 2 季 Alani Nu YoY"}},{"id":"H3","text":"估值倍數修復 — 5Y Fwd PE 從當前 5% 分位（18.5x）回升至中位（25-28x），對應 +35-50% 股價 re-rating 空間。前提：H1/H2 任一兌現 → 市場 derisk thesis 後 re-rate","columns":{"2Y 驗證點":"2027 Fwd FY27 PE 回到 22-25x","5Y 驗證點":"2030 Fwd PE 維持 22-25x 區間","10Y 驗證點":"2034 Fwd PE 落在 18-22x（成熟期合理區間）","具體數字門檻":"FY26 EPS 共識上修至 ≥ .80（vs 當前 .63）；Fwd PE 站回 22x+ 連 4 週","信息來源":"共識 EPS estimate（yfinance / Zacks）+ 5Y PE 歷史區間 28-45x（剔除 hypergrowth 期極端值）","漂移觸發條件":"Fwd PE 連 4 週 10% → 削弱；連 8 週"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"CELSIUS 核心品牌結構性份額流失 — Alani Nu 內部蠶食 + Monster Reign / Red Bull Zero 等大廠 sugar-free SKU 反撲 + Liquid Death 等 functional water 新 entrant 切入","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Nielsen scan CELSIUS standalone 4 週滾動 YoY；CELSIUS Q2 / Q3 standalone YoY","警戒閾值":"Nielsen scan 連 3 個月"}},{"id":"R2","text":"GM 結構性 mix dilution（Alani Nu 永久性稀釋） — Q1 26 GM 48.3%（-400bps YoY），Mgmt guide H2 26 回到 low-50s 若未兌現，估值倍數 derate 15-20%","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 GM 軌跡；Mgmt 法說會 H2 GM guidance 細節","警戒閾值":"Q2 26 GM"}},{"id":"R3","text":"Pepsi 戰略重新評估 / 監管風險 — Pepsi 2027 若啟動飲料業務分拆 / 重議 CELH 配銷條款；或美國 FDA 推 caffeine + minor 法規（18+ purchase）→ 直接砍 TAM 15-25%","columns":{"對應假設":"H1+H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Pepsi 公開 IR statements；FDA / California / NY 立法進度","警戒閾值":"Pepsi 公開表態「重新評估飲料業務」；任一州通過 18+ purchase 法案 → 觸發；需 ≥ 50% 機率才考慮砍倉（避免短期新聞驚嚇）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"❌","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":30.16,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
