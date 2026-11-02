你是 stock-analyst **v20 判斷 agent**，標的 AXTI（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"AXTI","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AXTI_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AXTI_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":73.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 業績新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001051627/000143774926033941/ex_1013304.htm；axt.com IR 頁未取得"},"note":"Q3 公司指引約 66.0 M（來源：MarketBeat 2026-07-30，未回查原稿）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income","value":29.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 業績新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001051627/000143774926033941/ex_1013304.htm；axt.com IR 頁未取得"}},{"id":"f_kpi2_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":40.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 業績新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001051627/000143774926033941/ex_1013304.htm；axt.com IR 頁未取得"}},{"id":"f_kpi3_gaap_operating_income","label":"GAAP operating income","value":28.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 業績新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001051627/000143774926033941/ex_1013304.htm；axt.com IR 頁未取得"}},{"id":"f_kpi4_gaap_operating_margin","label":"GAAP operating margin","value":38.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 業績新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001051627/000143774926033941/ex_1013304.htm；axt.com IR 頁未取得"}},{"id":"f_kpi6_gross_margin_gaap","label":"Gross margin (GAAP)","value":56.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 業績新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001051627/000143774926033941/ex_1013304.htm；axt.com IR 頁未取得"}},{"id":"f_kpi7_net_income_gaap_attribut","label":"Net income (GAAP, attributable)","value":25.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 業績新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001051627/000143774926033941/ex_1013304.htm；axt.com IR 頁未取得"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_axti_gross_margin_pct","label":"AXTI 毛利率","value":32.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXTI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_axti_operating_margin_pct","label":"AXTI 營業利益率","value":4.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXTI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_axti_fcf_margin_pct","label":"AXTI FCF 利潤率","value":-15.59,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXTI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohr_gross_margin_pct","label":"COHR 毛利率","value":37.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohr_operating_margin_pct","label":"COHR 營業利益率","value":12.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohr_fcf_margin_pct","label":"COHR FCF 利潤率","value":-14.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":3.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 業績新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001051627/000143774926033941/ex_1013304.htm；axt.com IR 頁未取得"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":52.31,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-50.59,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":40.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.87 → 0.87）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.89,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.25 → 2.23）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.29 → 3.29）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":0.87,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.23,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.29,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":190.0,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 0.3 → 0.87（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":106.89,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":20.09,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":17.77,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":60.2,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 0.87，分子＝快照價 52.38","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-396.13,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 116.61、現金 512.74（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":65.57,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":3038.27,"period":"2026-11-03","unit":"USD m","basis":"市值 3434.4 ＋ 淨負債 -396.13","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":239.41,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（5 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":516.68,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（5 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":12.69,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟢","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 52.36 / W52 55.78 / W104 29.18 / W250 14.63 / W250 13週斜率 5.1%"},{"id":"f_ma_w52","label":"52 週均線","value":55.78,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":29.18,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":14.63,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":5.1,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出主要對手為 Sumitomo、JX、Freiberger、Umicore、CCTC、Vital Materials；稱競爭強度過去幾年增加、預期持續增加，競爭壓力已造成價格下降，可能壓縮份額與毛利。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"The level and intensity of competition has increased over the past years and we expect competition to continue to increase in the future. Competitive pressures have resulted in reductions in the prices of our products, and continued or increased competition could reduce our market share, require us to further reduce the prices of our products, affect our ability to recover costs and result in reduced gross margins and profitability.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 稱客戶通常至少有兩家合格基板供應商；InP 與低 EPD GaAs 競爭者較少，品質為關鍵因素。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"Other products, such as InP and low EPD GaAs wafers, have fewer competitors and quality is a key competitive factor in addition to price.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K：中國鎵供應商（合資企業所處）為爭奪國內市占而降價，合資企業權益收益由 3.4 百萬美元降至 0.8 百萬美元。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"Further, gallium suppliers in China reduced their pricing as they competed for market share within their domestic market.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"JX Advanced Metals 計畫投資至多 1,200 億日圓至 FY2030，InP 產能擴至最多 10 倍。","source":"TrendForce News 2026-06-16","url":"https://www.trendforce.com/news/2026/06/16/news-jx-advanced-metals-to-invest-jpy-120b-through-fy2030-expand-inp-capacity-up-to-10x-as-cpo-demand-accelerates/","excerpt":"[News] JX Advanced Metals to Invest JPY 120B Through FY2030, Expand InP Capacity Up to 10x on CPO Demand 2026-06-16 Emerging Technologies editor","as_of":"2026-06-16","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"中國新進入者（雲南鍺業、Vital Materials）擴 InP 產能；InP 基板瓶頸加劇。","source":"LEDinside 2026-08-03","url":"https://ledinside.com/news/2026/8/2026_08_03_01","excerpt":"Yunnan Germanium: Officially initiated a high-quality InP single-crystal wafer project with a total investment of CNY 189 million in April 2026. The expansion targets an additional annual capacity of 300,000 InP wafers, bringing the company’s total annual output to 450,000 wafers, primarily serving mid-to-low-end transceivers and standard telecom components. Vital Materials/ Guangdong","as_of":"2026-08-03","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Q2 2026 財報電話會議：前五大客戶占營收約30%，無單一客戶超過10%（客戶集中度低）。","source":"AXT Q2 2026 Earnings Call Transcript (Webull)","url":"https://www.webull.com/news/15341695014478848","excerpt":null,"as_of":"2026-08-04","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"AXT 2026-07-29 公告 Lumentum 承諾 InP 最低年度採購至2031年，初始預付款 $43.5M；另有 Casela 2027年約 $25.4M 採購承諾、Coherent 6吋 InP 三年開發與供應協議（來自搜尋摘要彙整，未讀原文）。","source":"AXT 8-K FY2026 / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001051627/000143774926024883/ex_993544.htm","excerpt":null,"as_of":"2026-07-29","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K 稱 InP 基板進入門檻高，目前僅三家主要供應商（含 AXT）；搜尋未見最大客戶導入第二供應商或自製 AXT 所供基板的來源。","source":"AXT 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":null,"as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 無單一客戶占營收超過10%；前五大客戶占營收29%（2024年30%、2023年25%）。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"No customer represented more than 10% of our revenue for the years ended December 31, 2025, 2024 and 2023. Our top five customers, although not the same five customers for each period, represented 29% of our revenue for the year 2025, 30% of our revenue for 2024 and 25% of our revenue for 2023.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"原材料銷售：FY2025 三大客戶合計占原材料銷售25%（2024年31%）；海外（北美以外）銷售占營收約98%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"For the year ended December 31, 2025, three customers of our consolidated subsidiaries, in aggregate, accounted for 25% of raw material sales. For the year ended December 31, 2024, three customers of our consolidated subsidiaries, in aggregate, accounted for 31% of raw material sales","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"應收帳款有一家客戶占比超過10%（2025與2024年底），公司不要求擔保品；風險因信用評估與地理分散而降低。","source":"SEC EDGAR 10-K FY2025 財報附註 Credit Risk","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"We perform ongoing credit evaluations of our customers’ financial condition, and limit the amount of credit extended when deemed necessary, but generally do not require collateral. The credit risk in our accounts receivable is mitigated by our credit evaluation process and the geographical dispersion of sales transactions. One customer accounted for more than 10% of our accounts receivable as of December 31, 2025 and 2024.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"風險因素：客戶無義務採購特定數量，可減少、延後或取消訂單；過去曾遇訂單推遲與取消。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"Our customers are not obligated to purchase a specified quantity of our products or to provide us with binding forecasts of product purchases. In addition, our customers may reduce, delay or cancel orders. In the past, we have experienced a slowdown in bookings, significant push-outs and cancellation of orders from customers.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TrendForce 描述 InP 短缺為需求快速上升與供給受限的結構性錯配，分析師預期失衡延續至 2027 年後；新基板通過下游認證需 12-18 個月以上（搜尋摘要轉述，未逐字核對）","source":"TrendForce News: InP Shortage Emerges as AI Optical Interconnect Bottleneck","url":"https://trendforce.com/news/2026/08/06/news-inp-shortage-emerges-as-ai-optical-interconnect-bottleneck/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"AXT 於 2026-08 達成年初設定的 InP 產能翻倍目標，預期 2026 年底達 2025 年底的約 2.75-3 倍，並計畫 2027 年再翻倍；生產滿載、需求仍高於供給（Q3 財報會議摘要）","source":"Nasdaq: AXT's Order Backlog Surge & Capacity Push / MarketBeat Q3 2026 call transcript","url":"https://www.nasdaq.com/articles/axts-order-backlog-surge-capacity-push-fuel-growth-expectations","excerpt":null,"as_of":"2026-10-29","retrieved_at":"2026-11-03","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"供給端擴張：Sumitomo 目標 FY2028 產出為 FY2024 的 3 倍；Lumentum 美國 6 吋 InP 廠 2028 年中才量產；Lumentum 預計 2026 年底 InP 產量較 2025 年底倍增（轉述自搜尋摘要）","source":"Compound Semiconductor / TrendForce / 搜尋彙整","url":"https://compoundsemiconductor.net/article/125737/AI_optics_a_435b_market_waiting_on_InP","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"2027 供需缺口估計分歧：一說 10-20%（1.6T 升級週期），一說 McKinsey 模型 800G 短缺 40-60%、1.6T 至 2029 短缺 30-40%；另有分析師稱紙面上基板產能約為需求兩倍；LightCounting 預期 2026-2027 價格大致穩定，除非由短缺轉為產能過剩","source":"搜尋彙整（LightCounting LightTrends、compoundsemiconductor.net 等）","url":"https://www.lightcounting.com/newsletter/en/may-2026-silicon-photonics-lpolro-and-npocpo-377","excerpt":null,"as_of":"2026-05-01","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"中國 InP 出口管制（2025-02-04 起）造成許可延遲；2026 年 5 月起中國開始核准新批次出口但緩解有限；AXT 稱 Q3 營收約 $66M 已有許可或無需許可","source":"Nasdaq / 搜尋彙整","url":"https://www.nasdaq.com/articles/axtis-ai-driven-indium-phosphide-boom-hypergrowth-sustainable","excerpt":null,"as_of":"2026-08-15","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"經查 10-K Legal Proceedings，公司僅列股東集體訴訟與衍生訴訟（證券法 10b-5），無反壟斷調查或拆分相關程序；搜尋亦未找到 2026 年 AXT 的反壟斷／DOJ／FTC／EU 調查。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"The amended complaint alleges violations of Sections 10(b) and 20(a) of the Securities Exchange Act of 1934, as amended (the “Exchange Act”), and Rule 10b-5 promulgated thereunder by the defendants, and seeks unspecified monetary relief, interest, and attorneys’ fees.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"公司聲明中國政府對 VIE、資料安全或反壟斷的近期表態與行動，未影響其業務或 Nasdaq 上市。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"Recent statements and regulatory actions by China’s government on the use of VIEs and data security or anti-monopoly concerns have not impacted our ability to conduct our business or continue to list our common stock on the Nasdaq Global Select Market.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Q2 2026 10-Q 更新中國出口許可與美國關稅對 InP 基板營收的影響。","source":"AXT 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001051627/000143774926027677/axti20260630_10q.htm","excerpt":"On February 4, 2025, China added indium phosphide substrates to its export control list. As a result, the three wafer substrate product families manufactured by Tongmei all require permits from China’s Ministry of Commerce before they can be exported from China. InP export permits represent the most significant challenge we currently face.","as_of":"2026-08-10","retrieved_at":"2026-11-03","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國自2025-02-04起對InP基板實施出口許可；10-K稱InP出口許可是目前最大挑戰，且無法保證取得許可或中國不再加碼管制","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"On February 4, 2025, China added indium phosphide substrates to its export control list. On March 4, 2025, the United States further increased the tariff on imports of many products, including our wafer substrates, to 70%. InP export permits represent the most significant challenge we currently face.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國對含晶圓基板的中國進口品關稅升至70%，北美營收2025年僅約2%；IEEPA關稅於2026-02-20被最高法院推翻，但232與301仍有效","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"On February 20, 2026, the U.S. Supreme Court invalidated many of the global tariffs previously imposed under the International Emergency Economic Powers Act of 1977 (the \"IEEPA\") and the U.S. Customs and Border Protection subsequently announced that IEEPA-based tariff provisions would be terminated effective February 24, 2026.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"搜尋摘要：最新424B5稱對美國客戶的InP出口許可處於最終審查階段、尚未核發；Q2 2026 10-Q稱仍有未取得許可的訂單積壓且無法預測審批時點","source":"SEC EDGAR 424B5 / 10-Q Q2 2026（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001051627/000143774926027677/axti20260630_10q.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-11-03","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"AXT 所有基板與原料產品皆由中國子公司與合資企業在中國製造，亞洲總部在北京，三處廠區均在中國","source":"AXT 10-Q (period ended 2026-06-30), via search summary","url":"https://www.sec.gov/Archives/edgar/data/0001051627/000143774926027677/axti20260630_10q.htm","excerpt":"All of its substrate products and raw material products are manufactured in the PRC by its PRC subsidiaries and joint ventures.","as_of":"2026-08-01","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國自 2025-02-04 將 InP 基板納入出口管制；2026 年 6 月 10-Q 稱尚無輸美 GaAs 出口許可獲批，輸美 InP 許可於春季募股說明書時仍在最後審查","source":"AXT 10-Q 2026-06-30 / 424B5 (search summary)","url":"https://www.sec.gov/Archives/edgar/data/0001051627/000143774926027677/axti20260630_10q.htm","excerpt":"As of the spring 2026 prospectus, U.S.-bound InP permits were in the final stages of review but had not yet been issued.","as_of":"2026-08-01","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"出口許可時程不在 AXT 控制範圍，造成階段性供給衝擊；InP 首張許可 2025 年 6 月底取得","source":"Capital Blueprint Substack, AXT Deep Analysis Report","url":"https://capitalblueprint.substack.com/p/axt-inc-axti-deep-analysis-report","excerpt":"This creates episodic supply shocks even when demand is robust.","as_of":"2026-01-01","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"AXT 垂直整合：持有中國原料合資股權，並開始精煉高純銦（緩解原料面風險）","source":"Capital Blueprint Substack via search summary","url":"https://capitalblueprint.substack.com/p/axt-inc-axti-deep-analysis-report","excerpt":"The company recently began refining high-purity indium, giving it greater control over a particularly important input for InP production.","as_of":"2026-01-01","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 營收 $47.6M（Q1 $26.9M、去年 Q2 $18.0M）；InP 營收 $30.7M 創高，主因資料中心需求。","source":"AXT Q2 2026 results (SEC 8-K / Barchart)","url":"https://www.barchart.com/story/news/3560661/axt-inc-announces-second-quarter-2026-financial-results","excerpt":"Revenue for the second quarter of 2026 was $47.6 million, compared with $26.9 million for the first quarter of 2026 and $18.0 million for the second quarter of 2025.","as_of":"2026-07-30","retrieved_at":"2026-11-03","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026（9/30 止）營收約 $73.4M，去年同期 $28.0M；高於公司指引約 $66.0M（來源為 8-K 表格片段，未見完整新聞稿）。","source":"AXT 8-K FY2026 exhibit","url":"https://www.sec.gov/Archives/edgar/data/0001051627/000143774926033941/ex_1013304.htm","excerpt":"Revenue $73,410 three months ended September 30, 2026","as_of":"2026-11-02","retrieved_at":"2026-11-03","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Yole 預估 InP 基板 2031 年前 CAGR 逾 18%，動能來自 AI 資料中心、高速光模組與 CPO；管理層稱未來 3–5 年基板市場擴張 4–6 倍（次級來源，低信心）。","source":"Nasdaq/Chartmill: AXTI's AI-Driven Indium Phosphide Boom","url":"https://www.nasdaq.com/articles/axtis-ai-driven-indium-phosphide-boom-hypergrowth-sustainable","excerpt":null,"as_of":"2026-06-01","retrieved_at":"2026-11-03","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：公司自述市場技術變動快，競爭對手推出新技術可能使現有產品過時；且競爭者採用類似長晶技術的基板愈來愈多，已侵蝕公司的技術差異化。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"If our competitors introduce products employing new technologies or performance characteristics, our existing products could become obsolete and unmarketable. Over time, we have seen our competitors selling more substrates manufactured using a crystal growth technology similar to ours, which has eroded our technological differentiation.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Fraunhofer ISE 與 III/V-Reclaim 開發 InP-on-GaAs 基板（至 150mm），定位為可取代 prime InP 晶圓的較低成本替代方案","source":"Fraunhofer ISE 新聞稿 InP on GaAs substrates can replace prime indium phosphide wafers","url":"https://www.ise.fraunhofer.de/en/press-media/news/2025/InP-on-gaas-substrates-can-replace-prime-indium-phosphide-wafers.html","excerpt":"phosphide on gallium arsenide substrates (InP-on-GaAs wafers) with up to 150 mm diameter. These new wafers can effectively replace classic indium phosphide in a variety of applications, offering a scalable pathway to lower cost. The research team developed a process to deposit a thin layer of high-quality InP on GaAs.","as_of":"2025-05-21","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 描述通路：美國、中國、歐洲直銷，日本、台灣、韓國等地用獨立業務代表與經銷商；未見通路結構轉變的描述","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"We sell our substrate products directly to customers through our direct salesforce in the United States, China and Europe. We also use independent sales representatives and distributors in Japan, Taiwan, Korea and other areas.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"AXT 與 Lumentum 簽定 InP 基板供應及產能預留協議，產能預留至 2031-12-31，Lumentum 付兩筆各 $43.5M 預付款並抵作出貨額度","source":"AXT 8-K Ex 99 (2026-07-29)","url":"https://www.sec.gov/Archives/edgar/data/0001051627/000143774926024883/ex_993544.htm","excerpt":"Announces Long-Term Supplier Agreement with Lumentum FREMONT, Calif., July 29, 2026 – AXT, Inc. (Nasdaq: AXTI), a leading manufacturer of compound semiconductor substrates, today announced that it entered into a definitive agreement with Lumentum Operations, LLC for the supply and capacity reservation of indium phosphide wafer substrates.","as_of":"2026-07-29","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-30 公司給 Q3 2026 指引：非GAAP EPS $0.30–0.32、營收 $66.0M；MarketBeat 稱對照當時共識 EPS 0.10、營收 $38.7M，屬上調；營收口徑為依現有出口許可或非受限產品、高信心者。","source":"MarketBeat: AXT issues Q3 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/axt-nasdaqaxti-issues-q3-2026-earnings-guidance-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-11-03","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布因來源而異：Investing.com／Walnut／Bullstory 約 $91.60 均值（5 位，Buy，區間 $55–125，2026-08）；TickFlow $84.33（7 位，2026-08-01）；MarketBeat $77（2026-09-22，1 Strong Buy/3 Buy/1 Hold/1 Sell）；StockAnalysis $57（Hold，僅 2 位，$21–93）。B. Riley Neutral 目標價 $55（2026-07-31）。各源 as-of 不一，無單一統一共識。","source":"Investing.com / StockAnalysis / MarketBeat / TickFlow 聚合","url":"https://uk.investing.com/equities/axt-inc-consensus-estimates","excerpt":null,"as_of":"2026-09-22","retrieved_at":"2026-11-03","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"First Principles Partners 於 2026-08-31 以 Sell、目標價 $45 首次覆蓋（德文站轉述）。","source":"boerse-express AXT Aktie Prognose 2026 & Kursziel","url":"https://www.boerse-express.com/analyse/axt-aktie-kaufen-oder-verkaufen","excerpt":null,"as_of":"2026-08-31","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"預估上修：TIKR 稱分析師於 2026-06-30 至 09-30 間將 2027 營收預估由約 $222M 提高到約 $461M，Q4 共識營收 $77.45M；Chartmill 顯示 FY2026 EPS 共識 0.88（7 位，2026-10-24），次季營收預估 3 個月上修 76.83%。","source":"TIKR blog; Chartmill AXTI estimates","url":"https://www.tikr.com/blog/axt-stock-fell-10-in-a-day-even-as-analysts-more-than-doubled-their-2027-revenue-estimates-heres-where-the-stock-could-go","excerpt":null,"as_of":"2026-10-24","retrieved_at":"2026-11-03","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2024-05-06 起的股東集體訴訟（10b-5，class period 2021-03-24～2024-04-03）移轉至北加州地院，FY2025 10-K 申報時駁回動議已briefing完畢、待法院裁定。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"Defendants’ motion to dismiss is fully briefed and pending before the Court.","as_of":"2026-03-17","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-27 Tongmei 與 AXT 簽署股份認購等協議，投資人最低約 US$285M、最高約 US$545M 投入 Tongmei；AXT 同時以約 US$400M 增資 Tongmei。為子公司融資/增資，非併購標的。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1051627/000121390026113058/ea0309774-8k_axt.htm","excerpt":"The Agreements provide for an investment by the Investors of a minimum of RMB 1,912,350,000 (approximately US$285 million) (the “Minimum Amount”) and up to a maximum of RMB 3,668,639,053.25 (approximately US$545 million) (the “Maximum Amount”) in the ordinary shares of Tongmei","as_of":"2026-10-28","retrieved_at":"2026-11-03","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"2026-07-26 與 Lumentum 簽 InP 基板產能預留協議，6 年期，首期預付款 US$43.5M。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926024883/axti20260715_8k.htm","excerpt":"Lumentum has agreed to pay AXT (i) an initial deposit of $43,500,000, due within thirty (30) business days after entry into the Agreement","as_of":"2026-07-29","retrieved_at":"2026-11-03","affects":["moat_trend","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"AXT Q2 2026 call: expects to exit 2026 at ~$60M quarterly InP capacity and to more than double to ~$130M in 2027 with an additional adjacent-site expansion; CEO said could pursue more than the planned doubling; InP backlog 'well over $100 million'.","source":"MarketBeat, AXT Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/axt-q2-earnings-call-highlights-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"AXT Q3 2026 call: surpassed goal to double InP capacity in August; expects ~2.75-3x end-2025 capacity by end-2026 and to double again in 2027; definitive private-equity financing agreement for InP and raw-material capacity expansion in China via Tongmei.","source":"MarketBeat, AXT Q3 2026 earnings call transcript","url":"https://www.marketbeat.com/instant-alerts/transcript-what-axt-axti-said-on-its-q3-earnings-call-2026-10-29/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Peers expanding rather than constraining: Sumitomo Electric reportedly plans ~3x InP substrate capacity 2024-2028; JX Advanced Metals reportedly 7-10x by 2030 (unconfirmed against primary filing; another source says no announced plan).","source":"Substack / aggregated reports via search (the indium phosphide squeeze; Global Semi Research)","url":"https://abhayterminal.substack.com/p/the-indium-phosphide-squeeze","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"New China competitor project approved in Zhejiang: ~RMB 2B investment, planned 3M GaAs and 3M InP substrates/year, construction Aug 2026 to Aug 2029.","source":"TrendForce News, GaAs and InP Substrate Project Approved in Chinese Zhejiang Province","url":"https://www.trendforce.com/news/2026/07/23/news-gaas-and-inp-substrate-project-approved-in-chinese-zhejiang-province/","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"InP基板價格自2025Q4起已三度調漲，基板廠考慮Q4再漲逾10%(第四次);價格趨勢向上","source":"Economic Daily News via xenospectrum, 2026-08-17","url":"https://xenospectrum.com/en/inp-shortage-ai-optical-supply/","excerpt":"substrate makers are considering additional price hikes of more than 10% for the October-December quarter; InP substrate prices have already risen three times since the October-December 2025 quarter","as_of":"2026-08-17","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"2吋InP基板價格由2025年底500人民幣升至6月最高880人民幣(Nomura轉述)","source":"search summary citing Nomura","url":"https://xenospectrum.com/en/inp-shortage-ai-optical-supply/","excerpt":"the price of a 2-inch InP substrate rose from 500 yuan at the end of 2025 to as high as 880 yuan ($130.54) in June","as_of":"2026-06-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"AXT Q1 2026後通路庫存正常化至約兩個月，訂單排到2027","source":"Nasdaq/Zacks: AXTI's AI-Driven Indium Phosphide Boom","url":"https://www.nasdaq.com/articles/axtis-ai-driven-indium-phosphide-boom-hypergrowth-sustainable","excerpt":"bookings now extend into 2027, channel inventory has normalized to near two months","as_of":"2026-05-15","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"AXT Q2 2026存貨9,630萬美元，季增約620萬;積壓訂單逾1億美元，需求超過產能擴充速度","source":"AXT Q2 2026 earnings call transcript (Motley Fool)","url":"https://www.fool.com/earnings/call-transcripts/2026/08/03/axt-axti-q2-2026-earnings-call-transcript/","excerpt":"Inventory -- $96.3 million, an increase of approximately $6.2 million during the second quarter.","as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2019 下行：全年毛利率由 2018 的 36.2% 降到 29.8%，2020 回升至 31.7%；原因為銷量下滑、製造成本（尤其 GaAs）未同步下降。","source":"AXT 10-K FY2019 / FY2020 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1051627/000155837021003377/axti-20201231x10k.htm","excerpt":"Gross margin in 2019 was 29.8% as compared to 36.2% in 2018.","as_of":"2020-03-16","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2019 年第四季毛利率低點約 21%，對比 Q1 2019 的 33.1%。","source":"AXT 8-K 新聞稿 (SEC 搜尋結果)","url":"https://www.sec.gov/Archives/edgar/data/1051627/000155837020002561/axti-20191231x10k.htm","excerpt":"21 percent for the fourth quarter of 2019, which compares with 33.1 percent of revenue for the first quarter of 2019.","as_of":"2020-02-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2023 下行：毛利率由 2022 的 36.9% 降到 17.6%，毛利減少 $38.8M；營收 $141.1M 降至 $75.8M；2024 毛利率回升至 24.0%。","source":"AXT 10-K FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1051627/000155837025003004/axti-20241231x10k.htm","excerpt":"Gross margin in 2023 was 17.6% as compared to 36.9% in 2022. The decrease in gross profit is attributed to lower revenue resulting in fixed costs being spread over less units and an unfavorable change in product mix.","as_of":"2025-03-01","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2023 北美營收年減 67.7%，主因 InP 與 GaAs 基板需求下滑。","source":"AXT 10-K FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1051627/000155837025003004/axti-20241231x10k.htm","excerpt":"Revenue from customers in North America decreased in 2023 by 67.7% primarily due to lower demand for InP wafer substrates and GaAs wafer substrates used in LED and wireless applications","as_of":"2025-03-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#4","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2025 年 Q1 毛利率 -6.4%、Q2 為 8.0%（前一年 Q2 為 27.4%），InP 出口許可延遲為因素之一。","source":"Nasdaq/Motley Fool data-news: AXT Q2 revenue drops 36%","url":"https://www.nasdaq.com/articles/axt-axti-q2-revenue-drops-36","excerpt":null,"as_of":"2025-08-01","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"未見 AXT 被併購或併購他人；2026-10-27 為 Tongmei 增資/外部投資人入股協議（子公司層級融資）。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1051627/000121390026113058/ea0309774-8k_axt.htm","excerpt":"Concurrently with the Agreements, AXT agreed to recapitalize Tongmei by subscribing for 342,998,797 ordinary shares for the RMB equivalent of US$400 million","as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"股東集體訴訟（2024-05-06 提起）仍未裁定駁回動議。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm","excerpt":"Defendants’ motion to dismiss is fully briefed and pending before the Court.","as_of":"2026-03-17","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"AXTI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":32.18,"operating_margin_pct":4.18,"fcf_margin_pct":-15.59,"rd_intensity_pct":8.02},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXTI","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"SOI.PA","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SOI.PA"},"note":"quarterly_income_stmt 無資料"},{"name":"IQE.L","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IQE.L"},"note":"quarterly_income_stmt 無資料"},{"name":"COHR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.5,"operating_margin_pct":12.67,"fcf_margin_pct":-14.48,"rd_intensity_pct":10.16},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"AXTI"},"financial_history":{"ticker":"AXTI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":141118000.0,"revenue_yoy_pct":null,"gross_margin_pct":36.93,"operating_margin_pct":10.11,"net_income":15811000.0,"diluted_eps":0.37,"free_cash_flow":-37230000.0,"fcf_margin_pct":-26.38,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":75795000.0,"revenue_yoy_pct":-46.29,"gross_margin_pct":17.57,"operating_margin_pct":-25.08,"net_income":-17881000.0,"diluted_eps":-0.42,"free_cash_flow":-7072000.0,"fcf_margin_pct":-9.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":99361000.0,"revenue_yoy_pct":31.09,"gross_margin_pct":23.99,"operating_margin_pct":-12.64,"net_income":-11624000.0,"diluted_eps":-0.27,"free_cash_flow":-17883000.0,"fcf_margin_pct":-18.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":88326000.0,"revenue_yoy_pct":-11.11,"gross_margin_pct":12.73,"operating_margin_pct":-23.34,"net_income":-21260000.0,"diluted_eps":-0.49,"free_cash_flow":-18778000.0,"fcf_margin_pct":-21.26,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/AXTI/AXTI_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**AXT, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good afternoon, everyone, and welcome to AXT's Third Quarter 2026 Financial Conference Call. Leading the call today is Dr. Morris Young, Chief Executive Officer; and Gary Fischer, Chief Financial Officer. In addition, Tim Bettles, VP of Business Development, will be participating in the Q&A portion of the call. My name is Tracy, and I will be your coordinator today. I would like to now turn the call over to Leslie Green, Investor Relations for AXT. Leslie, please go ahead.

**Leslie Green** (Attendees):
Thank you, Tracy, and good afternoon, everyone. Before we begin, I would like to remind you that during the course of this conference call, including comments made in response to your questions, we will provide projections or make other forward-looking statements regarding, among other things, the future financial performance of the company, market conditions and trends, emerging applications using chips or devices fabricated on our substrates, our product mix, global economic and political conditions, including trade tariffs and import and export restrictions, ability to obtain China export permits, timing and receipt of export permits, our plan to list our subsidiary, Tongmei in Hong Kong, the closing of the intended investment into Tongmei by a leading Asia-based asset manager our ability to increase orders in succeeding quarters to control costs and expenses, to improve manufacturing yields and efficiencies or to utilize our manufacturing capacity. 
We wish to caution you that such statements deal with future events, are based on management's current expectations, are subject to risks and uncertainties that could cause actual events or results to differ materially. In addition to the matters just listed, these uncertainties and risks include, but are not limited to, the financial performance of our partially owned supply chain companies and increased environmental regulations in China. In addition to the factors just mentioned or that may be discussed in this call, we refer you to the company's periodic reports filed with the Securities and Exchange Commission. These are available online by link from our website and contain additional information on risk factors that could cause actual results to differ materially from our current expectations. 
This conference call will be available on our website at axt.com through October 29, 2028. I also want to note that shortly following the close of market today, we issued a press release reporting financial results for the third quarter of 2026. This information is available on the Investor Relations portion of our website at axt.com. 
I would now like to turn the call over to Gary Fischer for a review of our third quarter results. Gary?

**Gary Fischer** (Executives):
Thank you, Leslie, and good afternoon to everyone. Our financial results highlight the continuing inflection in our business trajectory and the early stages of a multiyear growth phase for AXT. Revenue for the third quarter of 2026 was $73.4 million. This is an increase of 54% from $47.6 million in the second quarter of 2026 and an increase of 162% from $28.0 million in the third quarter of 2025. To break down our Q3 '26 revenue for you by product category, indium phosphide was $54.3 million, primarily from data center applications. Gallium arsenide was $9.1 million, germanium substrates were $344,000. 
Finally, revenue from our consolidated raw material companies in Q3 was $9.7 million. The top 5 customers generated approximately 35% of total revenue and 1 customer was over the 10% level. Gross margin showed continued gain in the third quarter, driven by an increase in total volume and a favorable product mix. In addition, market prices for indium phosphide have increased and a shift from 3-inch to 4-inch wafers has also contributed. Morris will give more color on this in a moment. 
Non-GAAP gross margin was 56.1% compared with 45.0% gross margin in Q2 and 22.4% gross margin in Q3 of 2025. For those who prefer to track results on a GAAP basis, gross margin in the third quarter was 56.0% compared with 44.9% in Q2 and 22.3% in Q3 2025. Moving to OpEx. Our total non-GAAP operating expense in Q3 was $11.7 million compared with $10.2 million in Q2 and $6.7 million in Q3 of 2025. On a GAAP basis, total OpEx in Q3 was $12.7 million compared with $10.9 million in Q2 of 2026 and $7.3 million in Q3 of 2025. Our non-GAAP operating profit for the third quarter of 2026 was $29.5 million or 40.2% of revenue compared with a non-GAAP operating percent in Q2 of 2026 of $11.2 million and a non-GAAP operating loss of $384,000 in Q3 of 2025. 
For reference, our non-GAAP operating line for the third quarter of 2026 was a profit of $28.4 million or 38.7% of revenue compared with an operating profit of $10.4 million in Q2 and an operating loss of $1.1 million in Q3 of 2025. Nonoperating income and expense and other items below the line of the operating line for the third quarter of 2026 was a net loss of $2.7 million. The details can be seen in the P&L included in our press release today. We are pleased to report a non-GAAP net profit of $26.8 million or $0.41 per diluted share. This compares with a non-GAAP net profit of $11.9 million or $0.19 per share in the second quarter of 2026. Non-GAAP net loss in Q3 of '25 was $1.2 million or $0.03 a share. On a GAAP basis, net profit in Q3 was $25.7 million or $0.39 per diluted share. By comparison, net profit was $11.1 million or $0.17 per share in the second quarter of 2026. GAAP net loss in Q3 of 2025 was $1.9 million or $0.04 per share. 
The weighted average diluted shares outstanding in Q3 was 65.9 million. Cash, cash equivalents and investments increased by $77 million to $825.9 million as of September 30. By comparison, at June 30, it was $748.8 million. Accounts receivable increased by only $3 million. In Q3, DSO improved to 49 days as a result of multiple customer prepayments. During Q3, we signed a long-term supply agreement with Lumentum. Under the terms of the agreement, we received a prepayment for wafers of $43.5 million. This type of agreement with significant upfront cash is an additional signpost regarding the important use of indium phosphide for high-speed optical data transmission required in the AI data centers. This prepayment is posted on our financial statements as a liability and will be converted to revenue as we ship products against the agreements. 
Depreciation and amortization in the third quarter was $2.6 million. Total stock comp was $1.1 million. Net inventory was up by approximately $7.4 million in the third quarter. This concludes the discussion of our financials. Before I turn the call over to Morris, I want to note that yesterday, we announced that our majority-owned subsidiary, Tongmei, has entered into a definitive agreement for a private equity financing, selling its own shares, not AXTI shares, to provide RMB directly into its operations. This is an exciting milestone for Tongmei as it works towards a public offering on the Hong Kong Stock Exchange. Funds will be used to advance capacity expansion for indium phosphide wafers at a time when demand for these wafers is outpacing supply. 
Proceeds will also be used to increase capacity at our raw material companies in China. Assuming the maximum amount of the investment at USD 545 million, AXT will maintain control of Tongmei with approximately 73.4% ownership, down approximately 12.1% following the completion of the transaction. This transaction turns the spotlight on Tongmei, reflecting its substance and generating momentum towards the future. And finally, as previously stated, Tongmei is proceeding with its efforts towards a listing on the Hong Kong Stock Exchange. We continue to believe that an IPO in China is highly beneficial as expanding both the substrate and raw material capacity in China is the most efficient way to support the rapidly evolving AI infrastructure build-out. Okay. Thank you. With that, now, I'll turn the call over to Dr. Morris Young for a review of our business and markets. Morris?

**Morris Young** (Executives):
Thank you, Gary. This is a pivotal and exciting period for AXT. As Gary noted, our business has reached an inflection point driven by exceptional strong customer demand for our indium phosphide material, which seems to increase with every review cycle. We entered 2026 with a commitment to double our indium phosphide capacity, and I'm pleased to report that we surpassed that goal in August and continue our expansion as an ongoing effort. We are currently in the design phase of converting a newly acquired adjacent building for indium phosphide production with work expected to begin within the next several months. Even with more significant events, our revenue opportunity in indium oxide has more than quadrupled in 2026 from where we were coming into the year. We were expecting substantial additional node expansion also in 2027. 
Three developments are fueling this progress. First, as I mentioned, we are aggressively adding capacity to address the massive market opportunity. Second, new proprietary crystal growth furnace designs are delivering meaningful gains in manufacturing productivity and output. Third, customers are transitioning to large diameter substrates and higher-value products. Together, these developments are creating a step change in our revenue potential. We have well surpassed our historical record levels for both indium phosphide revenues and corporate revenues. We are in a brand-new territory with backlog now above $500 million, including long-term multiyear agreements, short-term contracts of less than 12 months and spot purchase orders. Demand remains ahead of supply even as we accelerate the pace of our capacity addition. 
According to AI data center market, the need for optical connectivity is growing rapidly. As hyperscalers deploy increasing GPU dense systems, they require faster, more powerful efficient photonics to move enormous volume of data. Today, the transition to 800G and 1.6T transceiver modules is generating strong demand for indium phosphide-based lasers and detectors that enables these high-performance optical links. 
Looking further ahead, the industry is moving towards near packaged and co-packaged optics, which should expand the role of our material even further. Taken together, these developments support a sustained build-out of high-density optical infrastructure and a multiyear growth opportunities for our indium phosphide business. As many of you are aware, the competitive landscape for high-quality indium phosphide is limited to just a few players due primarily to the very high technical barriers to entry and the ongoing difficulty and sensitivity of crystal growth and proprietary processes technologies. 
Among our peers, we believe AXT is in the strongest position to scale our business for massive industry growth while continuing to meet the most stringent performance requirements for high-speed data center AI connectivity. Case in point, we continue to make great strides in development of our 6-inch indium phosphide capability. Our 6-inch lines are now moving to power production status with productivity increasing steadily. We believe this further differentiates us from our field of competitors and put us in a leadership position for next-generation devices. 
I want to thank our customers who are partnering with us throughout this process. We're excited to support them as we move forward with our own capability. Looking at demand by region, the large-scale build-out of AI infrastructure in the United States as well as in the significant capital investment plan for cloud services and AI platform providers is driving strong demand for EML and silicon photonics-based optical transceivers and high-speed total detectors with developing demand for CW lasers for scale-up applications. We believe our materials are already deployed across multiple U.S. hyperscalers, and we expect adoptions among the customers to continue to expand. 
China is also emerging as an important growth market as it accelerate investment across the AI supply chain. Our revenue into China indium phosphide-based laser market increased strongly at the end in Q3, and all of our customers there remain on our location. This momentum reflects China's growing role in building AI infrastructure for the global market and represent a compelling opportunity for AFC, particularly because shipments within China do not require an export license. 
Turning to gallium arsenide. Several of our key customers are now showcasing slow and wide VCSEL lasers for data center applications based on both 6- and 8-inch gallium arsenide. We believe this can be an exciting future market for AXT, and we are in a pole position as the world leader in both 6- and 8-inch gallium arsenide substrates. In Q3, demand for both semi-insulating and semiconductor material across wireless devices, industry robotics and data center lasers applications grew sequentially from the prior quarter. We do expect several of them to be seasonally down in Q4 but we continue to see opportunity for market share expansion in the continuing year for our gallium arsenide substrates. 
Finally, our raw material business continue to be highly strategic to our growth plan. Our subsidiary, Jin Mei, is now refining high-purity Indian, which gives us direct control of a guaranteed supply of yet other critical material for our indium phosphide substrates. We're also investing to help Jin Mei to expand their capacity so that AFC can depend on them on our growth. Jin Mei will continue to provide a meaningful portion of our raw material requirements. We'll continue to invest in our portfolio as we believe it is a major competitive differentiator. 
In summary, AXT is operating from a position of growing strength at an important moment for our industry. Demand for indium phosphide continues to exceed supply, and we're moving quickly to expand our capacity, improve our productivity and advance large diameter substrates. We always believe that indium phosphide will represent a big opportunity for AXT, but I can honestly say we didn't expect it to be so big. We're happy to see it, and we are also humbled by it. Through the years, we have created a great product to serve the market. As I have said, we are stepping up to embrace this massive opportunity. We are off to a fantastic start and remain laser-focused on execution. We believe we are well positioned for transformational growth as our market continues on its extraordinary trajectory. 
With that, I will turn the call back to Gary for our fourth quarter guidance. Gary?

**Gary Fischer** (Executives):
Thank you, Morris. As of today, we have approximately $90 million in revenue that can be realized in Q4 across our substrate product lines and raw materials for which we either already have a permit to ship or for which a permit is not required. We have a high degree of confidence in recognizing this revenue in Q4. We have delivered strong gross margin improvement over the past several quarters and are very pleased with the progress. Further improvement depends on a number of factors, including total revenue as it relates to revenue mix by product, absorption of fixed costs and our ability to continue to drive better manufacturing efficiency. 
With regards to operating expense, we expect that it will be approximately $13 million in Q4 on a non-GAAP basis and approximately $14 million on a GAAP basis. With these factors in mind, we believe our non-GAAP net income will be in the range of $0.57 to $0.59 and GAAP net income will be in the range of $0.56 to $0.58. We estimate the share count for Q4 will be approximately 66.1 million shares. Okay. This concludes our prepared comments. We will be glad to answer your questions now. Tracy?

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Richard Shannon with Craig-Hallum.

**Richard Shannon** (Analysts):
I'll congratulate you guys again on another very strong quarter, keep up the great work here. My first question is on gross margins. We've had a discussion in the last few conference calls, particularly the last one about how high they could go and you were suggesting they could get above 50%, and you cleared that significantly here. Gary, you gave us a little bit of language here how to think about it going forward. I didn't have enough time to run through your guidance-driven model to see where this might be aiming here. So I'd love for you to discuss gross margins, particularly in the context of what's built in your guidance up, down, flat as well as whether it can go up meaningfully from here. And maybe if you can maybe touch on some dynamics here about the things that you touched on the call here like wafer diameter increases here to the degree to which you have customers or contractors or spot pricing, ASP trends, et cetera. If you could help us kind of delineate all that, that would be great.

**Gary Fischer** (Executives):
Yes. We thought about this in advance, and I'm glad to make comments and Tim and Morris are prepared to add a little more depth and color. As usual, the gross margin is hugely driven by volume. which we've always said, and it's hugely driven by mix. And by that, we mean that since indium phosphide is a profitable product for us, the more indium phosphide we have, the happy we are in terms of gross margin prospects. So those are the 2 baseline variables that are fundamental. Now as we look at the recent developments, we're also looking at productivity improvements. And what I would say, and I have a manufacturing background, but good manufacturing companies should improve if volume goes up because you get a larger database, you can use statistical process control from a larger database to modify your processes. 
And our business model is extremely intensive in terms of process technology and process steps. So these higher volumes are helping us become more efficient. So that's a third element besides volume and mix. A fourth element that you also listed is customers moving to higher value, larger diameter substrates. So what's happening is that we have a history of migration. When Morris started the company, the wafer size for gallium arsenide and indium phosphide was 2 inches. And over the decades, we've migrated to 3-inch, 4-inch and in the case of indium phosphide, we're now moving to 6-inch. 
As we move up because there's more real estate in a 4-inch than there is in a 3-inch, obviously, the price goes up, but it just opens up a dynamic in which the customer expects the price to go up. So it's not surprise. And so then it's easy to agree on a fair price. So the larger diameter substrates also have a higher ASP, which becomes another element. So 6-inch right now is not impacting much, but next year, it will. So let me have Tim and/or Morris fill in some of the blanks here.

**Timothy Bettles** (Executives):
Yes. I want to add a few points on productivity as well. Morris mentioned that we're moving to a new generation of crystal growth furnace. This has been bought out really for the development and manufacturing of 6-inch indium phosphide. What we're seeing with this new technology is a significant increase in productivity as we move forward. So it not only enables us to move more efficiently from 2-inch to 3-inch and then 3-inch to 4 and eventually 6. But as we do that, it gives us much greater productivity in doing so. So that's going to help the gross margin significantly as we employ more and more of these new generation furnaces. It's really going to set us apart from the competition and give us a massive lead in on this technology.

**Morris Young** (Executives):
Yes. So let me add to add a point. I think one of the things which we saw a significant customer yesterday, and they were asking us on the much better EPD requirement on their high-power laser. And that is music to our ears. In other words, low EPD is our forte. And if they have a higher requirement for lower EPD, then there's less competition and that's a premium to the price. So that adds to our gross margin, okay? And also is the larger diameter 6-inch, of course, when we first were to ramp, we do expect productivity or yield to be low. But as we add more furnaces, we expect the yield improvement to expand significantly going forward. 
And lastly, but perhaps not very significant is the raw material prices going up significantly. So we're going to have some deduction on that side. But I think as you sum up all the other things that we're gaining, our efficiency, productivity, low EPD, et cetera, et cetera, it overwhelms the increase in our raw material costs.

**Gary Fischer** (Executives):
So Richard, one more thing. I guess I would say, I mean, you and I have known each other for even longer than I've been in my 12.5 years at AXT, but you probably never would expect me to say something like this on an open call, but I do think our gross margin will go up some more. I don't think we've peaked -- and I think it's reasonable to expect that it could begin with a 6 in the next quarter, not a high 6, but all of the things that we just described in terms of efficiency and migration and sizes and things like that, it's a work in progress. And so it should have a natural effect.

**Richard Shannon** (Analysts):
Let me ask one more question and I will jump on the line here, and that's on the capacity. It sounds like you had some great progress in expanding capacity faster than expected. You asked a question on the last call about what your indium phosphide revenue potential will be exiting both this year and last year. And if I wrote down the numbers correctly, where did I put those things? I forgot what they are, but I think they were like maybe 60 and then 130 each of the next few years. It sounds like it's a lot higher than that. Can you quote what your expected potential indium phosphide revenue capacity is exiting this year and next?

**Timothy Bettles** (Executives):
Yes. I can give some idea on that. It is a lot higher than we projected recently, of course. And that's in part because of this migration to larger wafer sizes. And it's also in part to an increase in ASPs. And we've been building out an ASP plan as we move forward. In Q3, we recorded an indium phosphide revenue of $54.3 million, and that's probably going to go up in Q4. Total projection of Q4 being around the $90 million mark, I would anticipate that the split of indium phosphide, all of the growth is going to be indium phosphide. So you should probably think about adding all of that additional on to indium phosphide. And then we'll just see continued growth into next year.

**Operator** (Operator):
Your next question comes from the line of Charles Shi with Needham.

**Charles Shi** (Analysts):
Gary and Tim, I think this is probably a high-level question because from time to time, there are some chatters within the investment community, they have a view on where things are going. And the most recent thing seems to be that they are worried about AXT adding a good amount of capacity and that could lead to overcapacity for indium phosphide substrates next year. I'm not sure if I buy that because it kind of mimics what we heard about HBM overcapacity into late 2024. It's a high-growth market and supply is getting a little bit ahead. I don't think that really is a big worry. But -- you guys know the forecast, customer forecast. You guys have intelligence into what your competitors are doing. You guys know what you are doing, how much capacity is going to be added. Mind if you address this question here and provide us your insight on this whole supply-demand situation maybe into next year.

**Timothy Bettles** (Executives):
Yes. Charles. So as we stand right now, we are significantly overbooked. All of our customers are on allocation. And the market out there, every month, we see additional growth. As we look at our capacity moving into '27 and then beyond into '28, the opportunities for us here and the demand for us outstrips any capacity that we can put in place. So the demand is just growing faster than we can add capacity today. We're seeing this, as we've pointed out, Morris has already pointed out with long-term multiyear agreements, short-term contracts of 12 months or less and then spot orders. Again, every customer is on allocation right now. It is impossible to keep up with demand. Even long-term supply agreements that we're having off of customers, we're being asked to increase 2x or 3x. 
So the plans that we have to, again, double our capacity in 2027. I'm not sure we'll even get our head above water with 2027. I can tell you as far as competition goes, I think -- I believe that we are still the leaders out there. We are certainly one of the fastest to grow capacity on indium phosphide. But Morris has just made an excellent point, and we've been saying this for years. Our low EPD substrates give us a massive value proposition advantage against our competition. As product moves towards high-power CW lasers and UHP lasers for scale out and scale up, low EPD, low defect density is absolutely essential for high laser bar yields and high reliability. And AXT offers the world-class in that marketplace. 
So customers are turning to us not only because we're the fastest to build out capacity, they're turning to us because our value proposition model is stronger than anyone else's. So worries about adding capacity through next year? No, I don't have any.

**Morris Young** (Executives):
Yes. Well, so let me add a few points. So let me give you an angle from the Chinese competitor. I mean, indium phosphide substrate is really hot. Last I heard, there are a number of new entries in China market wants to get into indium phosphide substrates. But do I worry about them? But I really don't think I do. I'll tell you the reason, indium phosphide is not an easy material to work with. We worked with it for 40 years. And we know how long it took us to grow from 2-inch to 3-inch and that 3-inch gradually to 4, and we move into 6. And the EPD level, I mean, although it's highly technical, but when we first enter into a major laser maker in the U.S. market, their requirement of EPD is less than 500. 
Now we're delivering less than 1/10 of it, okay? So I think those just take time and really experience to advance. And we're not standing still, and we're advancing. So I think to give you more assurances, I think HBT or the storage device market, I believe, doesn't have as high entry barrier as indium phosphide is, okay? So I think I'm reasonably confident about this and at least for the next 2 years. 3 years out, it's hard to say. But yesterday, we were talking to a major customer of ours. They were telling us, instead of the market is to expand by 20x, they're telling me actually it's 1,000x. I don't know how it comes to that, but it started to scale across, scale out and scale in and scale up. So every level is almost a 10x increase. And optical connectivity is at the heart of it. 
So my answer is I don't think we're going to reach that point. Ask me next year, perhaps that we worry about it. And hopefully, we still don't have to worry about it.

**Gary Fischer** (Executives):
Yes. Let me summarize. We have a long look forward, and we pay attention to it. It's visible all the way up to our Board level. So as CFO, I'm not at all worried about 2027 CapEx. I know it's less than is going to be needed. And I feel the same about 2028. So those 2 years, what we're planning to spend, I think, is very reasonable, and I don't think it's going to be overspending. When we get closer to 2029, we need to look at that. And we're growing us on this stuff. We're going to measure it and pay attention to it.

**Charles Shi** (Analysts):
Maybe I'll ask a second question. If I heard you correctly, I think you announced a second supply agreement with Lumentum with -- I forgot the exact amount, but going into Q2, you had another agreement. Is this a follow-on agreement or expansion of the previous agreement or something else? And related to that, if I think I heard you talking about backlog is now over $500 million. It was over $100 million, I think, a quarter ago. So probably 4x, maybe 5x expansion of the backlog over the course of last -- maybe 90 days, mind if you give a little bit of color. Those are highly related, that's a 2-part question.

**Timothy Bettles** (Executives):
I got you, Charles. So no, the Lumentum contract is the contract that we signed in Q3. So it's not a double up. It's not a secondary. It is the one that was signed and announced earlier in Q3. So we're just reiterating that for the course of this conference call. As backlog goes, yes, we're -- obviously, we mentioned before that we're more than $100 million. We're a little bit vague on exactly how much more than $100 million that we were. But now we're happy to say that as we see growth, we've surpassed the $500 million barrier. And that's made up of a number of things in terms of long-term supply agreements, again, short-term, 12-month or less supply agreements and spot POs that go through 2027. 
So really, that just gives us more encouragement and gives us more confidence that we're seeing growth into the rest of 2026 and through into 2027 with some significant backlog there. I'll make another noteworthy change here, and that's the demand from China is increasing in a significant way, right? Historically, we've built and shipped for China because we don't need permits. Again, everybody is now on allocation. We're accepting backlog as we see this, but we're also seeing a longer lead time out 9-plus months on a lot of this stuff. So of course, as we see longer lead times, we see more of these supply agreements, we see more demand coming this way. The backlog is just going to grow.

**Operator** (Operator):
Your next question comes from the line of Tim Savageaux with Northland Capital Markets.

**Timothy Savageaux** (Analysts):
Congrats on the results and outlook and especially on the backlog increase. First question, sort of taking the discussion back to gross margins and kind of where you can go there. And yes, doing that math, I think you're solidly in the 60s in terms of where you're guiding. Your incremental gross margins in Q3 were 77%, which is pretty significant. And Gary, I know you're hesitant to talk about where these margins can go over time. But to the extent we were talking about lower levels just a few quarters ago, is it fair to look at that 60% level as kind of a new baseline with upside potential given what you're seeing on incremental gross margins? Or how are you looking at that now?

**Gary Fischer** (Executives):
Well, it's hard to comment. It gets into a vocabulary that's so strange for me. But yes, it's -- we don't want the horse to run away with and get out of the racetrack and just be way ahead of us, but on our comments to you. So yes, it's pretty obvious that we're going to cross over 60% -- and -- but I have to say, and I don't mean it in a dodging way, but it's a fast-moving change. And we're hesitant to predict because things are moving so fast.

**Morris Young** (Executives):
Let me add perhaps to this point is the moving market. I'll tell you, this year, the fastest growth segment in 2026 was 3-inch. And next year, the high growth we expect is going to be 4-inch. But that is more of a new territory, okay? And high-power laser require low EPD. And again, that's a new territory. And 6-inch is going to be -- although it's still going to be single digit for 2027, but it's going to grow, and that's going to command a good gross margin.

**Timothy Savageaux** (Analysts):
And looking at the revenues and results and the guidance, I know it seems like you've incorporated a significant portion of the long-term agreements in your backlog. I guess, if you look at Q3 and the guide for Q4, how significant a contributor are the initial ramps of those long-term agreements to what you saw in Q3 and are guiding for in Q4?

**Timothy Bettles** (Executives):
Yes. We're definitely starting to see some contributions coming from the long-term supply agreements in Q3 -- Q4, sorry. That will continue to build as we go into 2027. But I want to make a point in that when we talk about the long-term supply agreements, we don't have a whole lot of them at the moment. They're not a big part of our backlog. So although some of them extend out for several years, the LTSAs are still a relatively small percentage of the multiyear LTSAs, still a relatively small part of our capacity as it goes forward. So a lot of this is still being built up on spot purchase orders, annual contracts, that type of stuff. But as I said before, our lead time is increasing. So it just adds -- keeps on adding to that backlog as we accept orders.

**Gary Fischer** (Executives):
And Tim, I would say that our Tim and Morris and our VP of Asia, Savan, they kind of pulled back on formal long-term agreements. And we don't want to lock up in that way. So we're maintaining flexibility. We are making commitments beyond 90 days or beyond 6 months, but we want to protect on price, and we also want to protect our ability to -- if we can do more or do less, we don't want to be locked in. So you're not going to -- the point is we're not going to be announcing multiple long-term agreements. There may be some more and plenty of customers want us to sign up for them, but it's not what we think is the right strategy for AXT.

**Timothy Savageaux** (Analysts):
That was going to be my next question. So that's good. So you're saying backlog is up $300 million or $400 million sequentially that is not majority or even materially driven by LTSAs. That's just kind of run rate business?

**Timothy Bettles** (Executives):
Yes, that's correct. That's run rate business.

**Operator** (Operator):
Your next question comes from the line of Matt Bryson with Wedbush Securities.

**Matthew Bryson** (Analysts):
I have one longer one and one quick one. Just for the longer one, it seems like low APV and your ability to deliver larger substrates is a substantial advantage. Is there any more color you can give us around what portions of shipments might be 4-inch and above or if there's a rule of thumb that we can think about in terms of either pricing or gross margin benefit that you get from shifting from 3-inch to 4-inch to 6-inch? And then I guess, also part of that, what portion of your competitors are able to deliver 4-inch or 6-inch substrates at this point?

**Timothy Bettles** (Executives):
Yes. Thanks, Matt. So the majority -- if you're looking at pure wafer volumes, the majority of the business has transitioned to 3-inch. Now a lot of the non-China business has been on 3-inch for a long time. And we're seeing a lot of the Chinese business move up into the 3-inch wafer size. We saw a couple of years ago that we started to see a transition. We made an announcement that we were seeing a 4-inch substrate going into AI-type data centers. And this was predominantly for detector material, photodetector material. Obviously, we continue to see that. That's been the market driver for 4-inch so far. And a lot of the photodetector material, especially the high-speed photodetector material is now firmly based on 4-inch. 
What we're going to see next year, and we're starting to see that transition in Q3 and Q4 this year is a lot of the laser material is now going to also transition to 4-inch. So in 2023 -- sorry, 2023, in 2026, a lot of the business is running on 3-inch for lasers, 4-inch for detectors. In 2027, we're going to see a big shift as we go through the year. And I think towards the end of the year, we could be looking -- if you're looking at wafer volumes, just single wafer volumes, you could be looking at something equal in 3-inch and 4-inch by the end of the year. So this does give us a significant ASP boost. It also gives us a significant gross margin opportunity here as well. 
What can our competitors deliver? It's variable, right? A lot of them still are stuck predominantly on 3-inch. The move to 4 is especially on the laser material and especially keeping the high-quality, low defect material is incredibly challenging. Morris said we've spent decades on building this up and the move to 4 in itself is a huge challenge, let alone the move to 6. I mentioned earlier that we've got this new furnace, this new crystal growth furnace. This gives us massive productivity improvements, not just on 6-inch. It's not just there for 6, gives us massive productivity improvements for 4-inch laser type material as well. 
So as we build out new furnaces, we're going to be really heavily focused on putting the new design furnace in there with a real commitment on scaling from 3-inch to 4-inch and then to 6-inch beyond 2027. So I think as you look into '27, we're going to see a meaningful number coming from 4-inch and you're going to start to see 6-inch come on board. And I think we're leading the game there.

**Morris Young** (Executives):
Yes. I think one of the Matt's question you have -- we have not answered is how many competitors can provide 4-inch and 6-inch. I think 4-inch is a bit harder to answer. But I think 6-inch so far, actually, I think we're climbing very fast, right? I think other than Us, there's a company called Us, and they are probably now equal to us. And the third is a very distant third.

**Timothy Bettles** (Executives):
Yes. Yes, there's 2 main players at 6-inch.

**Morris Young** (Executives):
But the point is we're adding a huge number of capacity all based about 6-inch. And we're glad that it is going into pilot production now.

**Matthew Bryson** (Analysts):
And then I just have one other quick one. Going back to Richard's kind of question around capacity. I know initially, I think you guys have talked about being able to double indium phosphide capacity in 2027. Is that still roughly how we should be thinking about things that from Q4 '26 to Q4 '27, numbers roughly doubling.

**Gary Fischer** (Executives):
The challenge is this. I think we're going to be more than double in 2026. So if you take end of 2025 as one, we're probably going to be at 2.75 or 3 at the end of 2026, right? And I think right now, our goal is to double again in 2027. Hopefully, by midyear, we can tell you we're still ahead of the planning.

**Operator** (Operator):
There are no further questions at this time. I will now turn the call back to Leslie Green for closing remarks.

**Leslie Green** (Attendees):
Thanks, Tracy, and thank you all for participating in our conference call. We will be participating in the UBS Global Technology and AI Conference and the Northland Growth Conference in December as well as the Needham Growth Conference in January. We hope to see many of you there. And as always, please feel free to contact us if you'd like to set up a call. We look forward to speaking with you in the near future.

**Operator** (Operator):
And this concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AXTI_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Gary Fischer｜guidance：CFO 給 Q3 已可認列營收約 6,600 萬美元（已有許可或無需許可），並稱有高度信心（原話："$66 million in revenue that can be realized in"）
- 2026-07-30｜Gary Fischer｜guidance：CFO 表示若取得額外訂單許可，Q3 可能有顯著上行，但無法預測許可時間（原話："We could see upside, even significant upside to this number"）
- 2026-07-30｜Gary Fischer｜guidance：Q3 non-GAAP 營業費用與每股盈餘財測（原話："non-GAAP net income will be in the range of $0.30 to $0.32"）
- 2026-07-30｜Gary Fischer｜guidance：Q3 non-GAAP OpEx 約 1,050 萬美元（原話："it will be approximately $10.5 million in Q3 on a non-"）
- 2026-07-30｜Morris Young｜guidance：CEO 稱磷化銦營收機會至 2026 年底將超過三倍，2027 持續大幅擴張（原話："on track to more than triple by the"）
- 2026-07-30｜Timothy Bettles｜guidance：BD 副總確認年底磷化銦季產能約 6,000 萬美元（原話："About $60 million there or
thereabouts."）
- 2026-07-30｜Timothy Bettles｜guidance：BD 副總稱明年再翻倍多，2027 年底季營收約 1.3 億美元（原話："about $130 million a quarter exiting the year"）
- 2026-07-30｜Timothy Bettles｜guidance：BD 副總建議中國占營收比重以 40%–60% 建模；Q2 中國高於 50%（原話："model that as a China being 40% to 60% of our revenue"）
- 2026-07-30｜Gary Fischer｜margin：Q2 non-GAAP 毛利率 45.0%，對比 Q1 29.9%、去年 Q2 8.2%；歸因於量與產品組合（原話："Non-GAAP gross margin was 45.0% compared"）
- 2026-07-30｜Gary Fischer｜margin：CFO 稱毛利率目標以 4 開頭，建議暫時維持現水準，並說「繫好安全帶」（原話："put your seatbelts on."）
- 2026-07-30｜Gary Fischer｜margin：CFO 稱毛利率進一步改善取決於營收組合、固定成本吸收與製造效率（原話："absorption of fixed costs"）
- 2026-07-30｜Morris Young｜margin：CEO 說明磷化銦毛利高於砷化鎵與合資公司，Q3 成長全在磷化銦所以毛利會更好（原話："the gross margin is going to be better."）
- 2026-07-30｜Gary Fischer｜margin：CFO 稱整條磷化銦產線滿載、能產就能賣，有助毛利（原話："whatever we can produce, we can sell."）
- 2026-07-30｜Gary Fischer｜commitment：CFO 稱應以 5 開頭的毛利率為目標，但不希望分析師據此建模（原話："definitely be targeting a number that begins with the 5"）
- 2026-07-30｜Morris Young｜commitment：CEO 稱已承諾 2026 磷化銦產能翻倍且進度超前（原話："committed to doubling our indium phosphide capacity in 2026"）
- 2026-07-30｜Morris Young｜commitment：CEO 稱 2027 於鄰近地點再次產能翻倍，已進入規劃（原話："planning process to double our capacity again in 2027"）
- 2026-07-30｜Morris Young｜commitment：CEO 稱 2027 計畫至少翻倍，目標為移動靶（原話："we think it's going to be more than
double in 2027"）
- 2026-07-30｜Timothy Bettles｜capital_allocation：BD 副總稱擴產不需大量額外 CapEx，確認先前 CapEx 計畫不變（原話："there is actually not a lot of
additional CapEx spend here"）
- 2026-07-30｜Gary Fischer｜capital_allocation：二次增發於 4/22 完成，約募得 6.32 億美元，現金升至 7.488 億美元（原話："generated approximately $632 million before expenses"）
- 2026-07-30｜Gary Fischer｜capital_allocation：通美撤回科創板 IPO 申請，改往香港上市，約需一年；PE 基金 4,900 萬投資有贖回權但目前皆願續投（原話："they all wish to continue their investment"）
- 2026-07-30｜Gary Fischer｜capital_allocation：CFO 稱現金足以應付贖回（原話："We have sufficient cash to redeem"）
- 2026-07-30｜Gary Fischer｜customer：Q2 簽署 Casela 與 Coherent 長約，分別預收 2,230 萬與 2,540 萬美元，列為負債，出貨後轉營收（原話："prepayments for wafers of $22.3 million and $25.4 million"）
- 2026-07-30｜Morris Young｜customer：CEO 宣布本週與 Lumentum 簽協議；BD 稱不揭露整體營收影響（原話："we're very pleased to announce an agreement with Lumentum"）
- 2026-07-30｜Timothy Bettles｜customer：長約對 Q2 貢獻不大，Q3 起放大；Casela 合約 2027 才開始（原話："So they don't move the needle too much on Q2."）
- 2026-07-30｜Gary Fischer｜customer：前五大客戶約占 30%，無單一客戶超過 10%（原話："no customers are over the 10% level"）
- 2026-07-30｜Timothy Bettles｜customer：BD 稱 Q2 中國占營收高於 50%（原話："China
right now is definitely above 50% of our revenue in Q2"）
- 2026-07-30｜Morris Young｜customer：管理層稱積壓訂單超過 1 億美元且持續成長，不給精確數字（原話："it's well over $100 million. It exceeds 2 quarters for sure."）
- 2026-07-30｜Gary Fischer｜customer：CFO 稱因產能已排滿，公司不再接超出規劃產能的訂單，故 backlog 不是同一口徑（原話："honestly, we're not taking orders."）
- 2026-07-30｜Gary Fischer｜risk：出口許可時間與成功與否無法預測，管理層自行強調（原話："we cannot predict the future timing of permits or success"）
- 2026-07-30｜Timothy Bettles｜risk：BD 稱許可仍是隱憂，但特定區域流程較規律（原話："Permits always remain a bit of an issue"）
- 2026-07-30｜Timothy Bettles｜risk：申請許可須先有訂單（原話："we cannot apply for a permit without an order in place."）
- 2026-07-30｜Morris Young｜competition：CEO 稱高品質磷化銦競爭者僅少數，技術門檻高，AXT 最有能力快速擴產（原話："limited to just a few players"）
- 2026-07-30｜Morris Young｜competition：被問 VCSEL 替代時，BD 稱磷化銦雷射、矽光與砷化鎵 VCSEL 並存；CEO 稱 200G 需磷化銦（原話："it has to be indium phosphide detectors"）
- 2026-07-30｜Morris Young｜product：營收增長三因素：擴產快於預期、新長晶爐提升產出、客戶轉向大尺寸高價值產品（原話："larger diameter substrates and higher-value products"）
- 2026-07-30｜Gary Fischer｜product：Q2 營收 4,760 萬美元創史上新高；磷化銦 3,070 萬美元（原話："Indium phosphide was $30.7 million,"）
- 2026-07-30｜Morris Young｜product：CEO 稱 6 吋磷化銦量產難度遠高於 3、4 吋，並稱團隊有進展（原話："exponentially more difficult to produce in volume"）
- 2026-07-30｜Morris Young｜product：子公司晶美精煉高純銦，確保磷化銦基板原料供應（原話："Jin
Mei, is now refining high-purity indium"）

### 問答異常語氣（迴避／改口／保留）
- AXTI_Q2_2026_Earnings_Call_20260730.md｜問：Richard Shannon 追問 backlog 是否遠高於 1 億美元，以及 2027 有多少被 backlog 涵蓋｜答法：管理層拒絕給精確 backlog 數字，只重複「超過 1 億美元」並改談長約與不接單的理由；CEO 稱 2027 並非全部已被認購
- AXTI_Q2_2026_Earnings_Call_20260730.md｜問：Charles Shi 追問 backlog 僅略高於兩季 Q3 營收速率，為何不多接單、能否揭露更多｜答法：CEO 與 CFO 均不給更高數字，稱不接超過規劃產能的訂單、口徑不同，改強調長約與能見度 3–4 季
- AXTI_Q2_2026_Earnings_Call_20260730.md｜問：Richard Shannon 問毛利率能否到 5 開頭、離漸近線多遠｜答法：CFO 稱應以 5 開頭為目標，但同時說不希望分析師據此建模、要小心對外說法；先前對 Matt Bryson 則建議維持現水準（45%）
- AXTI_Q2_2026_Earnings_Call_20260730.md｜問：Tim Savageaux 問 Lumentum 協議的整體規模｜答法：BD 只確認有預付款，明確表示不討論整體營收影響

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
{"date":"20260524","verdict":"B（觀望·thesis 真實但價格徹底透支｜InP 供需週期上行 + AXT 36% 市佔 + 產能 2026/27 各 doubling，但 FY27E EPS $0.75 對應 FwdPE 187x ＋ P/S 95x，5Y Base 目標價 $90-110 vs 現價 $140，等回測 $70-90 或 BB 中軌後再評估）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"InP supply tightness 持續 18-24 個月，AXT 受惠最大","columns":{"2Y 驗證點（2026-27）":"Q2 26 InP 收入達 $17M+ guidance；Q4 26 達 $25M+；季產能 ramp 至 $35M/季 end-2026","5Y 驗證點（2026-30）":"FY28-30 AXT InP 收入 ≥ $200M（從 2025 $50M ramp 4x）+ 市佔守住 35%+","10Y 驗證點（2026-35）":"InP 全市場 2030 達 $1-2B（4-10x growth from 2025）+ AXT 維持 top-3 地位","具體數字門檻":"InP 季收入連 2 季 ≥ $17M（2026 Q2-Q3）；FY27 InP 收入 ≥ $80M","信息來源":"Q1 2026 法說會（4/30）+ Mordor Intelligence InP wafer market report + 36Kr 分析","漂移觸發條件":"連 2 季 TTM 偏離 -10% → 削弱；連 3 季 -10% → 反轉（2Y 假設按 QC-35）"}},{"id":"H2","text":"Sumitomo 與 JX Nippon 在 2026-27 內無法 disrupt AXT 36% 市佔","columns":{"2Y 驗證點（2026-27）":"Sumitomo 2027 加 40% 產能不前提至 2026 H2；JX 維持 13% 不擴產","5Y 驗證點（2026-30）":"Sumitomo 2027 後產能擴張僅消化內部需求（vertical integration optical chips/modules）→ AXT 為唯一 merchant supplier ramp 受惠者","10Y 驗證點（2026-35）":"產業維持 top-3 = 90%+ 寡占，無中國 disruptor 進入 4-6 inch InP grade","具體數字門檻":"Sumitomo capex commitment 公告不超過 $500M（vs AXT $632M）；JX 無 capex announcement","信息來源":"Sumitomo Electric Q1-Q4 法說會（季度監控）；36Kr 中國 InP 產業報告","漂移觸發條件":"Sumitomo 公告 2026 H2 額外擴產 → 削弱；Yunnan Germanium 達 4-inch InP commercial → 削弱（5Y 假設按 QC-35 連 4 季 TTM）"}},{"id":"H3","text":"市場將維持 FY27-FY30 高速成長共識 + 估值高分位","columns":{"2Y 驗證點（2026-27）":"FY27 EPS 共識 ≥ $0.75 維持 90 天不下修；FY28 EPS 共識上修至 $1.50+","5Y 驗證點（2026-30）":"Forward PE 維持 80x+ 至 2028 中，allowing time for EPS catch-up","10Y 驗證點（2026-35）":"Stock 維持 $80-150 區間，long-term 透過 EPS growth 消化倍數","具體數字門檻":"FY27 EPS 共識 ≥ $0.75；FY28 EPS 共識上修至 $1.50","信息來源":"yfinance 5 位分析師共識（季度更新）；Needham/Stifel research notes","漂移觸發條件":"分析師 FY27 EPS 連 2 季下修 -10% → 削弱；下修 -25% → 反轉（H3 為估值假設，QC-35 2Y 軌跡）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI capex 2027 H1 air pocket：hyperscaler GPU 庫存消化 → optical demand 推遲 6-12 個月","columns":{"對應假設":"H1, H3","時間尺度標記":"⚡ 短期（1-2 季可觸發）","監測指標":"NVIDIA 季 GPU shipments；hyperscaler capex YoY 增長率；optical module ASP","警戒閾值":"連 2 季 hyperscaler capex 增長率 &lt; 15% YoY → 削弱（vs 當前 25-35%）"}},{"id":"R2","text":"Sumitomo 2027 擴產提前 + ASP 戰：日本同業搶 AI 客戶","columns":{"對應假設":"H2","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"Sumitomo 法說 capex commitment；季 InP ASP；AXT 季 GM 變化","警戒閾值":"連 2 季 AXT GM 環比 -3pp + Sumitomo 公告 2026 H2 提前擴產 → 削弱"}},{"id":"R3","text":"地緣 / Tongmei 整合：MOFCOM 2026-11-27 後反轉收緊；Tongmei IPO 永遠 paused；母公司 cash trapped","columns":{"對應假設":"H1, H2","時間尺度標記":"🐢 長期（2+ 年慢變數）","監測指標":"美中關係（出口管制 announcements）；Tongmei IPO 進度；母公司 cash flow from China","警戒閾值":"MOFCOM 反轉 + license 拒絕率 &gt; 30% → 反轉；Tongmei IPO 2-3 年無進展 → 削弱長期 valuation"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":140.83,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AXTI_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
