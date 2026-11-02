你是 stock-analyst **v20 判斷 agent**，標的 VALE（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"VALE","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_pro_forma_ebitda","label":"Pro forma EBITDA","value":3.5,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$ bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories"}},{"id":"f_kpi1_net_operating_revenue_ga","label":"營收（net operating revenue，GAAP）","value":10.6,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$ bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Investing.com 財報電話會議摘要（媒體轉載，IR 頁未列營收，待核對 Vale 完整財報）"},"note":"consensus US$10.51bn，beat 0.9%（Investing.com）"},{"id":"f_kpi2_eps","label":"EPS","value":0.29,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$/ADS","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Investing.com 財報電話會議摘要（媒體轉載）"},"note":"consensus US$0.4035，miss 28.1%"},{"id":"f_kpi3_free_cash_flow_total","label":"Free cash flow（total）","value":2.2,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$ bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories"}},{"id":"f_kpi4_capex","label":"Capex","value":1.3,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$ bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories"}},{"id":"f_kpi5_expanded_net_debt","label":"Expanded net debt","value":16.4,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$ bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories"}},{"id":"f_kpi6_realized_fines_price","label":"鐵礦砂 realized fines price","value":85.1,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$/t","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories"}},{"id":"f_kpi7_c1_cash_cost","label":"鐵礦砂 C1 cash cost","value":23.1,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$/t","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories"}},{"id":"f_kpi8_realized_price","label":"銅 realized price","value":15314,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$/t","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories"}},{"id":"f_kpi9_realized_price","label":"鎳 realized price","value":16898,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"US$/t","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories"}},{"id":"f_kpi10","label":"鐵礦砂產量","value":88.4,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"Mt","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories"}},{"id":"f_kpi11_2026","label":"管理層指引（2026）","value":null,"period":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）","citation":"Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories；Investing.com 電話會議摘要"},"needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_vale_gross_margin_pct","label":"VALE 毛利率","value":34.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VALE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vale_operating_margin_pct","label":"VALE 營業利益率","value":28.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VALE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vale_fcf_margin_pct","label":"VALE FCF 利潤率","value":8.62,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VALE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":11.48,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-25.39,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":27.99,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.75,"period":"2026-11-03","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-03","citation":"yfinance earnings_estimate"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.88,"period":"2026-11-03","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-03","citation":"yfinance earnings_estimate"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":71.81,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.23,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.62,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":5.45,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 2.09，分子＝快照價 11.39","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":9.303,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":83856.0,"period":"2026-11-03","unit":"BRL m","basis":"yfinance 最新一季：總債務 109950.0、現金 26094.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"財報幣別 BRL ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 BRL，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":4255.76,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"財報幣別 BRL ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 BRL，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":41167.4,"period":"2026-11-03","unit":"BRL m","basis":"yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"財報幣別 BRL ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 BRL，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":41090.05,"period":"2026-11-03","unit":"BRL m","basis":"yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"財報幣別 BRL ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 BRL，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 11.4 / W52 14.35 / W104 11.56 / W250 11.01 / W250 13週斜率 0.32%"},{"id":"f_ma_w52","label":"52 週均線","value":14.35,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":11.56,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":11.01,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.32,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"20-F FY2025：Vale 在亞洲鐵礦市場主要對手為 BHP、Rio Tinto、Fortescue；競爭因素為價格、品質、可靠度、營運與運輸成本。","source":"SEC EDGAR 20-F FY2025 §1.1.7 Competition","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"Asia. Our main competitors in the Asian market are located in Australia and include subsidiaries and affiliates of BHP Group Limited (BHP), Rio Tinto Ltd (Rio Tinto) and Fortescue Metals Group Ltd.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"20-F FY2025：Vale 在全球客製銅精礦市場 2025 年份額約 2.8%；精煉銅陰極參與度屬邊際。","source":"SEC EDGAR 20-F FY2025 §2.2.6 Competition","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"Our market share in 2025 was about 2.8% of the total custom copper concentrate market.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Wood Mackenzie 預期 Simandou 2026 年出口約 1,600 萬噸並續升，滿產 120 Mtpa 約占海運鐵礦近 7%；搜尋摘要稱巴西生產商（尤其 Vale）在品質上與其正面競爭（二手摘要，未核原文）。","source":"Wood Mackenzie 新聞稿 / Mining Weekly：Guinea's Simandou to become largest driver of seaborne iron ore supply growth","url":"https://www.miningweekly.com/article/guineas-simandou-to-become-largest-driver-of-seaborne-iron-ore-supply-growth-woodmac-2026-04-01","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"RBC 稱 Vale 為 Simandou 延遲的「clear winner」，預期其高階產品溢價擴大。","source":"itiger/Bloomberg: Vale Emerges as 'Clear Winner' From Simandou Delay, RBC Says","url":"https://www.itiger.com/news/2590531042","excerpt":"Vale Emerges as 'Clear Winner' From Simandou Delay, RBC Says MT Newswires Live 2025/12/11","as_of":"2025-12-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"S&P Global 指出 Simandou 區塊是中國將鐵礦供應從澳洲、巴西分散的核心；首船商業貨 2026-01 運抵中國並交給中國寶武。","source":"S&P Global Market Intelligence, Simandou's iron ore shipments signal major industry shift","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/04/simandous-iron-ore-shipments-signal-major-industry-shift","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Vale CFO Bacci 稱與 CMRG 無長約或固定定價，關係正面，並提出方案解決 CMRG 提出的物流問題。","source":"mining.com, Vale says China, iron ore suppliers are mutually dependent","url":"https://www.mining.com/web/vale-says-china-iron-ore-suppliers-are-mutually-dependent/","excerpt":"long-term contracts or fixed pricing arrangements with CMRG, Bacci said. CMRG said earlier this week the way the industry sets prices is “irrational” and vowed to address what it called a value imbalance between miners and steelmakers. The company’s research arm said the current market mechanism is “unfair and unreasonable” and driving prices higher. Vale has a “pretty positive relationship”","as_of":"2025-10-31","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 十大客戶占鐵礦砂及球團銷量 36.3%、營收 35.8%；中國占出貨 63%；2025 與 2024 無單一客戶占營收 10% 以上（2023 有一家占 10%）。","source":"SEC EDGAR Vale 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"Our ten largest customers collectively purchased 114.0 million metric tons of iron ore and iron ore pellets from us, representing 36.3% of our 2025 iron ore and iron ore pellet sales volumes and 35.8% of our total iron ore and iron ore pellet revenues. In 2025 and 2024, no customer individually represented 10% or more of our revenue.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"鎳業務客戶全球分散，2025、2024、2023 皆無單一客戶占淨營收 10% 以上。","source":"SEC EDGAR Vale 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"No customer individually represented 10% or more of our net operating revenue in 2025, 2024 and 2023.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"UBS 預期澳洲與巴西鐵礦產量 2026、2027 每年約增 3%（約 +1.2 億噸供給），並預期中國鋼需未來 3–5 年每年約降 1%（搜尋摘要轉述，未核原文）","source":"Market Index: iron ore prices set to fall as global markets shift to surplus (UBS)","url":"https://www.marketindex.com.au/news/iron-ore-prices-set-to-fall-as-global-markets-shift-to-surplus-ubs","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Rio Tinto 預期 Simandou 2026 年出 5–6 百萬噸、2028 年達 60 Mtpa；RBC 認為 30 個月爬坡「技術上偏樂觀」，預估 48–60 個月；Platts 消息人士稱供過於求 2027 年起可能明顯加劇（搜尋摘要轉述，未核原文）","source":"Rio Tinto Guinée / S&P Global Platts ferrous week 搜尋摘要","url":"https://riotintoguinee.com/en/media/press-release/simfer-advances-the-simandou-project-at-pace-reaching-new-operational-milestones/","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"worldsteel 2026 年 10 月將全球 2026 鋼需預測由 +0.3% 下修為 -0.1%，並提及鐵礦砂觸及四年低點；4 月預估中國 2027 鋼需與 2026 大致持平；印度 2026 +7.4%、2027 +9.2%（搜尋摘要轉述，未核原文）","source":"worldsteel forecast via GMK Center (搜尋摘要)","url":"https://gmk.center/en/news/global-steel-demand-is-expected-to-grow-by-0-3-in-2026-worldsteel/","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Vale 2026 指引：鐵礦 335–345 Mt、銅 360–380 kt（8 月上調下限）、鎳 185–200 kt；Q2 2026 淨利年減 35% 至 13.8 億美元；公司策略預期基本金屬占未來十年稅前利潤 30–35%（搜尋摘要轉述，未核原文）","source":"Mining.com / MiningReporters 搜尋摘要","url":"https://www.miningreporters.com/noticia/news/2026/08/vale-lifts-copper-nickel-2026-production-outlook","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"BHP 預期鐵礦供過於求再持續約十年（日期不明）","source":"Mining.com: BHP just forecast another 10 years of iron ore glut","url":"https://www.mining.com/bhp-just-forecast-another-10-years-of-iron-ore-glut/","excerpt":"BHP just forecast ‘another 10 years’ of iron ore glut Cecilia Jamasmie | June 21, 2016 | 5:33 am Top Companies Australia China Europe Latin America Iron Ore","as_of":"2016-06-21","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"20-F 揭露產業特定監管：EU ETS 自2026年起對航運全面實施、FuelEU Maritime 自2025年生效，可能提高 Vale 未來運費；REACH 合規。","source":"SEC EDGAR 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"As of 2026, full implementation for the shipping sector is in effect, with the requirement to ship operators to purchase allowances for greenhouse gas emissions generated during voyages to, from, and between EU ports.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026年 Vale 收到 ANM 對 Pico、Mar Azul、Gongo Soco 礦及 Fábrica 溢流的違規通知（罰款），公司列為可能損失並提出異議。","source":"Vale 6-K 3Q26","url":"https://www.sec.gov/Archives/edgar/data/0000917851/000129281426005056/valedfifrs3q26_6k.htm","excerpt":"the state court authorized the partial resumption of operations at the Fábrica Complex in September 2026. The total amount estimated across the actions is US$604 (R$3,131 million), and the likelihood of loss has been classified as possible. Civil litigations - Notices of Infraction issued by the National Mining Agency (\"ANM\")","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"巴西 Minas Gerais 當局因 Viga 礦侵蝕與水溢流下令停工，Vale 暫停兩座礦場。","source":"Engineering News: Vale halts two units after water overflow triggers permit suspension","url":"https://www.engineeringnews.co.za/article/vale-halts-two-units-after-water-overflow-triggers-permit-suspension-2026-01-27","excerpt":null,"as_of":"2026-01-27","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"印尼 Vale Indonesia 僅獲約30%的 RKAB 配額申請，尋求修訂。","source":"investortrust.id: Vale Seeks RKAB Revision After Only 30% Approval","url":"https://investortrust.id/market/91787/vale-seeks-rkab-revision-after-only-30-approval-threatens-hpal-projects","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Vale 20-F 揭露：2025 年對中國客戶銷售占淨營收 51%；關稅、制裁環境或中國需求變動可能降低產品需求與營收。","source":"SEC EDGAR 20-F FY2025 風險因素","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"The percentage of our net operating revenue attributable to sales to customers in China was 51% in 2025. Therefore, any contraction of China’s economic growth or change in its economic profile, or changes in tariffs or in the political or sanctions environment globally could result in lower demand for our products, leading to lower revenues, cash flow and profitability.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Vale 20-F 揭露：作為鐵礦與鎳供應商，面臨關稅、進出口管制及貿易壁壘對自身及客戶產品的影響，整體衝擊難預測。","source":"SEC EDGAR 20-F FY2025 風險因素","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"As a supplier of iron ore, nickel and other raw materials to the global integrated steel industry and to other metal-consuming sectors such as battery production and other specified, industrial end-uses we are subject to additional risk from the imposition of duties, tariffs, import and export controls and other trade barriers impacting our products and the products our customers produce.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"20-F 指出 2025 年日本、南韓粗鋼產量分別年減 4.0%、2.8%，反映關稅不確定性影響出口與需求。","source":"SEC EDGAR 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"Compared with 2024, steel production in 2025 declined by 4.0% in Japan, to 80.7 Mt and 2.8% in South Korea, to 61.9 Mt, reflecting an industrial environment marked by uncertainties related to tariffs, which affected exports, weakened demand, and intensified competition from Chinese steel exports.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋未見 2026 年針對 Vale 的中國官方貿易限制；2026 年 3 月中國限制的是 BHP 鐵礦（非 Vale）。Section 232 2026 調整僅涵蓋鋼、鋁、銅，搜尋結果未提及鐵礦或鎳。","source":"WebSearch 摘要（Vale China tariff 查詢；Section 232 查詢）","url":null,"excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"第三方分析指 Carajás 至 Ponta da Madeira 港為單一約 900 公里鐵路，中斷即癱瘓最大鐵礦出口節點（非 Vale 官方說法）","source":"energy-solutions.co, Annual Production (Vale Brazil Iron Ore Carajás)","url":"https://energy-solutions.co/supply-chain/manufacturers/vale-brazil-iron-ore-carajas","excerpt":"The rail line is a single 900-kilometer railway to the coastal port, and any disruption, whether from flooding, protests, or mechanical failure, instantly paralyzes the largest iron ore export node on the planet.","as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2022 年 3 月 Carajás 鐵路因山崩停運；Vale 稱礦場與港口靠庫存管理照常運作，維持 320-335 Mt 指引","source":"Vale press release: temporary stoppage of Estrada de Ferro de Carajás railway operations","url":"https://vale.com/w/vale-informs-about-temporary-stoppage-of-estrada-de-ferro-de-carajas-railway-operations","excerpt":null,"as_of":"2022-03-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國占 Vale 鐵礦砂銷量比重 2021 至 2024 由 65% 降至 61%（聚合站報導，來源品質混雜）；另有報導 Oman 球團廠因中東衝突延後至 2026 Q3 重啟","source":"Search summary: Panjiva / gmk.center","url":"https://es.panjiva.com/research/vales-china-exposure-rises-more-to-come-if-australia-china-relations-worsen/37941","excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"3Q26 營收約 $10.6B、年增約 2%；鐵礦砂粉占淨銷售 61%、球團 11%、銅鎳等其他 27%；基礎金屬銷售年增 42%，抵銷對中國出貨下降","source":"Finsee Vale Q3 2026 earnings review / SteelOrbis","url":"https://finsee.ai/earnings/vale/2026/q3/en/","excerpt":"The Brazilian miner grew third-quarter revenue by 2% from a year ago to $10.6 billion","as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"3Q26 鐵礦砂粉平均實現價 $85/t，年減 10%；淨利年減 53%","source":"Kitco / SteelOrbis","url":"https://www.steelorbis.com/steel-news/latest-news/vales-q3-2026-net-profit-falls-53-percent-as-iron-ore-fines-prices-drop-1487435.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"worldsteel 2026年10月展望：全球鋼需 2026 持平、2027 +1.7%；中國 2026 -2%、2027 -1%","source":"Engineering News: Global steel demand to remain flat this year on China slowdown","url":"https://www.engineeringnews.co.za/article/global-steel-demand-to-remain-flat-this-year-on-china-slowdown-2026-10-12","excerpt":null,"as_of":"2026-10-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Vale 3Q26 all-in premium 約 US$4.4/t 與上季持平；粉礦溢價下降，被球團溢價（+US$1.4/t，直接還原球團占比提高）抵銷","source":"Vale 3Q26 Form 6-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000917851/000129281426005058/vale20261029_6k.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"2Q26 球團平均實現價 US$137.0/t，年增 2.2%；2026 球團產量指引 30–34 Mt","source":"Vale 2Q26 Form 6-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000917851/000129281426004002/valepr2q26_6k.htm","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Vale 在 20-F 自述：可使用較低品位鐵礦的技術可能降低其高品位產品組合的相對使用價值，對鐵礦產品需求與溢價造成負面影響；公司持續監控顛覆性技術。","source":"SEC EDGAR 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"Technologies that can allow the competitive use of lower grade iron ores could reduce the relative value in use of our higher-grade portfolio and have a negative impact on the demand and premium of our iron ore products. We continue to monitor disruptive technologies and market trends to deliver appropriate supply answers.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"S&P Global 2026 Q1 亞洲鎳市場回顧：買方預期 NMC 電池需求upside有限，電池廠轉向無鎳 LFP。","source":"S&P Global Commodity Insights trade review","url":"https://www.spglobal.com/energy/en/news-research/latest-news/metals/011526-trade-review-asian-nickel-market-faces-q1-pressure-as-oversupply-outweighs-output-cuts","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Mysteel：Vale Indonesia 管理層稱鎳仍有成長空間，LFP 滲透率已逾全球電動車電池 55%。","source":"Mysteel flash","url":"https://www.mysteel.net/news/5140713-flash-vale-indonesia-flags-indonesian-nickel-supply-growth-as-near-term-price-challenge","excerpt":"On demand, Bernardus said nickel still has room to grow despite rising LFP battery penetration, which now exceeds 55% of global EV batteries. Outside China, however, about 80% of EV batteries still use nickel-based chemistry.","as_of":"2026-09-11","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"IEEFA 報告：新製程組合可讓 DRI 使用 62-65% 一般品位鐵礦，減少對高品位礦需求。","source":"IEEFA","url":"https://ieefa.org/articles/new-tech-promises-solve-steels-iron-ore-problem-met-coal-miners-face-uncertain-future","excerpt":null,"as_of":"2022-01-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Vale Base Metals 加速 IPO 準備，但 Vale 表示尚未決定（組織／商業模式層面的線索，非通路轉移）","source":"Mining Reporters: Vale Base Metals fast tracks IPO readiness but Vale says no decision","url":"https://www.miningreporters.com/noticia/news/2026/03/vale-base-metals-fast-tracks-ipo-readiness-but-vale-says-no-decision","excerpt":"Vale Base Metals fast-tracks IPO readiness, but Vale says no decision has been made Agustín de Vicente / March 4, 2026 | 23:43 Vale Base Metals is aiming to be ready for a potential IPO by mid-2026, according to CEO Shaun Usmar.","as_of":"2026-03-04","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026 更新 guidance：鐵礦 C1 現金成本上調至 22.5–23.5 美元/噸、all-in 58–62 美元/噸（匯率與油價）；產量目標維持鐵礦 335–345Mt、銅 360–380kt、鎳 185–200kt；capex 維持 5.4–5.7 十億美元（搜尋摘要轉述，未核原文）","source":"renovainvest.com.br — Vale (VALE3) revisa guidance 2026","url":"https://renovainvest.com.br/blog/vale-guidance-2026/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Benzinga 表列 VALE 2026 Q3 EPS 實際 0.29 美元 vs 預期 0.33 美元（10/29 公布），Q2 亦低於預期；各來源 Q2 數字不一致（未核原文）","source":"Benzinga VALE earnings-forecasts","url":"https://www.benzinga.com/quote/VALE/earnings-forecasts","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價共識各源不一：StockAnalysis 平均約 17.25 美元（25 位分析師、Buy）；MarketBeat 7 月底約 16.31 美元（Moderate Buy）；Benzinga 9 月共識 15 美元；高標 21 美元（JPMorgan），低標約 11–12 美元（未核原文）","source":"StockAnalysis / MarketBeat / Benzinga 聚合頁","url":"https://stockanalysis.com/stocks/VALE/","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Investing.com 列出 Goldman Sachs 於 2026-07-27 將 VALE 降至 Hold（未核原文）","source":"Investing.com VALE consensus estimates","url":"https://www.investing.com/equities/vale-s.a.--americ-consensus-estimates","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-07-24 分析師平均評級 Moderate Buy 與平均目標價","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/vale-sa-nysevale-receives-average-rating-of-moderate-buy-from-analysts-2026-07-24/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"Vale 20-F FY2025 披露：Vale 與前高管在紐約東區聯邦法院被列為美國證券集體訴訟被告，涉 Brumadinho 尾礦壩及風險管理揭露；另有 Southern Bahia 市政府 2025-06-27 對 Samarco/BHP/Vale 提起公民訴訟（無法可靠估算曝險）、Itabira 市訴訟求償約 US$5.5 billion。","source":"SEC EDGAR 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"We and certain of our former executive officers were named defendants in securities class action suits, under U.S. federal securities laws, brought before the United States District Court for the Eastern District of New York by holders of our securities.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Vale 與共同投資人將 Thompson（加拿大鎳礦）轉入新公司，夥伴持 81.1%、Vale 保留 18.9%，夥伴承諾投入最多 US$200 million；搜尋摘要來源，未讀原文。","source":"Vale 6-K 2026-02-19（搜尋結果）","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426000428/vale20260219_6k.htm","excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Vale 取得鐵礦商 Ligga 30% 少數股權，增資約 US$190 million；Vale 稱非重大事實。","source":"GMK Center: Vale has acquired a 30% stake in the Brazilian iron ore producer Ligga","url":"https://gmk.center/en/news/vale-has-acquired-a-30-stake-in-the-brazilian-iron-ore-producer-ligga/","excerpt":null,"as_of":"2026-09-25","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2026-01 Congonhas 的 Fábrica 與 Viga 兩處因水溢流遭暫停營運許可，兩處合計年產約 8 百萬噸；Vale 重申 2026 鐵礦砂指引 335–345 百萬噸。","source":"Mining Weekly: Vale halts two units after water overflow triggers permit suspension","url":"https://www.miningweekly.com/article/vale-halts-two-units-after-water-overflow-triggers-permit-suspension-2026-01-27","excerpt":null,"as_of":"2026-01-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"S&P Global估Simandou鐵礦出貨2026年約15-20Mt、2027年40-50Mt，2028年約70Mt；6月報告稱爬坡快於預期","source":"S&P Global, Ferrous Week: Guinea's Simandou ramp-up boosts iron ore exports surpassing forecasts","url":"https://www.spglobal.com/energy/en/news-research/latest-news/metals/061726-ferrous-week-guineas-simandou-ramp-up-boosts-iron-ore-exports-surpassing-forecasts","excerpt":null,"as_of":"2026-06-17","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Vale 2026鐵礦產能目標335-345Mt、2030年360Mt；S11D與Serra Sul壓碎項目2026下半年投產；鐵礦capex 2026年$4B、2027起$3.9B/年","source":"Nasdaq/Zacks: After a 47% Run in 2025, is the VALE Stock Still a Buy in 2026?","url":"https://www.nasdaq.com/articles/after-47-run-2025-vale-stock-still-buy-2026","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"BHP FY2026鐵礦產量指引258-269Mt，WAIO中期預期超過305Mt/年（RTP1、Western Ridge Crusher）","source":"Nasdaq/Zacks: BHP vs. VALE","url":"https://www.nasdaq.com/articles/bhp-vs-vale-which-global-mining-powerhouse-better-buy-now","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"印尼2026鎳礦產量目標約250-260Mt，較2025約379Mt下降；Vale Indonesia 2026 RKAB初期未核准致1月停採","source":"S&P Global Market Intelligence: Indonesia finalizing reduced nickel ore output target for 2026","url":"https://www.spglobal.com/market-intelligence/en/news-insights/articles/2026/1/indonesia-finalizing-reduced-nickel-ore-output-target-for-2026-97045526","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Simandou出貨預估15-20Mt(2026)、40-50Mt(2027)","source":"S&P Global","url":"https://www.spglobal.com/energy/en/news-research/latest-news/metals/010526-iron-ore-industry-challenges-simandous-pilbara-killer-status","excerpt":null,"as_of":"2026-01-05","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"SMM 35-port China iron ore inventory about 148.3 Mt on 2026-10-16, up ~2.85 Mt m/m; weak steel output and slower pick-up; accumulation expected to continue (來源摘要轉述)","source":"SMM: Iron Ore Port Inventory and Port Pick-up Volume on October 16, 2026","url":"https://news.metal.com/newscontent/104160762-iron-ore-port-inventory-and-port-pick-up-volume-on-october-16-2026","excerpt":null,"as_of":"2026-10-16","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"Vale Q3 2026 net profit fell 53% on lower iron ore prices and higher costs; iron ore output 88.4 Mt (-6% y/y), below consensus","source":"Mining Weekly: Vale's profit falls 53% in Q3 on lower iron-ore prices, higher costs","url":"https://www.miningweekly.com/article/vale-posts-53-decline-in-third-quarter-net-profit-2026-10-30","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Vale Q3 2026 6-K 含產銷與庫存調節表（Q2 庫存欄 648，Q3 未核）","source":"Vale Form 6-K 2026-10-29","url":"https://www.sec.gov/Archives/edgar/data/0000917851/000129281426005058/vale20261029_6k.htm","excerpt":"2 Iron ore agglomerates guidance, including iron ore pellets and briquettes. Sales Summary-1% 4% 4% 8% 335-345 Mt 30-34 Mt² 360-380 kt 185-200 kt 000’ metric tons Iron ore Fines¹ 3Q26 86,285 75,513 3Q25 85,997 75,020 ∆ y/y 0% 1% 2Q26 79,747 ∆ q/q 9M26 Pellets 8,720 ROM Copper Nickel 1 Including third-party","as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Vale 2015 調整後 EBITDA 為 70.81 億美元，較 2014 年低 47%，主因售價下跌；全年 EBITDA 利潤率 27.7%，4Q15 為 23.6%（該輪低點），1Q16 回升至 35.1%。","source":"Vale S.A. Form 6-K (SEC) FY2016 filing","url":"https://www.sec.gov/Archives/edgar/data/0000917851/000110465916099889/a16-5291_16k.htm","excerpt":null,"as_of":"2016-04-28","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"鐵礦砂現貨價自 2011 年 2 月高點約 191.9 美元/噸，跌至 2015 年底低點約 38.8 美元/噸，跌幅約 80%，歷時約 4.5–5 年（跌幅為搜尋摘要數字推算）。","source":"Bloomberg / mining.com 鐵礦價格報導（2015-12）","url":"https://www.bloomberg.com/news/articles/2015-12-10/billionaire-s-iron-ore-mine-begins-exports-amid-price-collapse","excerpt":null,"as_of":"2015-12-10","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"IMF 文獻：商品超級週期上升段約 10–35 年","source":"IMF Cuddington 2008","url":"https://www.imf.org/external/pubs/ft/staffp/2008/04/pdf/cuddington.pdf","excerpt":null,"as_of":"2008-04-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Vale 取得鐵礦商 Ligga 30% 少數股權，增資約 US$190 million。","source":"GMK Center","url":"https://gmk.center/en/news/vale-has-acquired-a-30-stake-in-the-brazilian-iron-ore-producer-ligga/","excerpt":null,"as_of":"2026-09-25","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"Thompson 鎳礦轉入新公司，夥伴持 81.1%、Vale 保留 18.9%。","source":"Vale 6-K 2026-02-19（搜尋結果）","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426000428/vale20260219_6k.htm","excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Vale 與前高管為紐約東區聯邦法院美國證券集體訴訟被告（Brumadinho 相關揭露）；Southern Bahia 市政府另於 2025-06-27 提起公民訴訟。","source":"SEC EDGAR 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm","excerpt":"We and certain of our former executive officers were named defendants in securities class action suits, under U.S. federal securities laws, brought before the United States District Court for the Eastern District of New York by holders of our securities.","as_of":"2026-03-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"VALE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.82,"operating_margin_pct":28.71,"fcf_margin_pct":8.62,"rd_intensity_pct":1.76},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VALE","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"RIO","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RIO"},"note":"quarterly_income_stmt 無資料"},{"name":"BHP","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BHP"},"note":"quarterly_income_stmt 無資料"},{"name":"FMG.AX","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FMG.AX"},"note":"quarterly_income_stmt 無資料"}],"subject":"VALE"},"financial_history":{"ticker":"VALE","currency":"BRL","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":43839000000.0,"revenue_yoy_pct":null,"gross_margin_pct":45.19,"operating_margin_pct":40.59,"net_income":18788000000.0,"diluted_eps":4.05,"free_cash_flow":6039000000.0,"fcf_margin_pct":13.78,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":41784000000.0,"revenue_yoy_pct":-4.69,"gross_margin_pct":42.35,"operating_margin_pct":37.95,"net_income":7983000000.0,"diluted_eps":1.83,"free_cash_flow":7245000000.0,"fcf_margin_pct":17.34,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":38056000000.0,"revenue_yoy_pct":-8.92,"gross_margin_pct":36.24,"operating_margin_pct":29.17,"net_income":6166000000.0,"diluted_eps":1.44,"free_cash_flow":2919000000.0,"fcf_margin_pct":7.67,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":38403000000.0,"revenue_yoy_pct":0.91,"gross_margin_pct":35.04,"operating_margin_pct":29.54,"net_income":2352000000.0,"diluted_eps":0.55,"free_cash_flow":2795000000.0,"fcf_margin_pct":7.28,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/VALE/VALE_Q3_2026_Earnings_Call_20261030.md）

# Q3 2026 Earnings Call
**Vale S.A.** | Earnings Calls | 2026-10-30

**Operator** (Operator):
Good morning, ladies and gentlemen. Welcome to Vale's Third Quarter 2026 Earnings Call. This conference is being recorded, and the replay will be available on our website at vale.com. The presentation is also available for download in English and Portuguese from our website. [Operator Instructions] We would like to advise that forward-looking statements may be provided in this presentation, including Vale's expectations about future events or results, encompassing those matters listed in the respective presentation. We caution you that forward-looking statements are not guarantees of future performance and involve risks and uncertainties. 
To obtain information on factors that may lead to results different from those forecast by Vale, please consult the reports Vale files with the U.S. Securities and Exchange Commission, SEC, the Brazilian Comissão de Valores Mobiliários, CVM, and in particular, the factors discussed under forward-looking statements and Risk Factors in Vale's annual report on Form 20-F. 
With us today are Mr. Gustavo Pimenta, CEO; Mr. Marcelo Bacci, Executive Vice President of Finance and Investor Relations; Mr. Rogério Nogueira, Executive Vice President, Commercial and Development; Mr. Carlos Medeiros, Executive Vice President of Operations; and Mr. Shaun Usmar, CEO of Vale Base Metals. 
Now I will turn the conference over to Mr. Gustavo Pimenta. Sir, you may now begin.

**Gustavo Duarte Pimenta** (Executives):
Hello, everyone, and thank you for joining Vale's Third Quarter 2026 Conference Call. Let me start by saying how proud I am of the progress our teams have been able to make on our strategic priorities, even under very volatile market conditions. We continue to consistently execute on our plans with discipline, focusing on operational excellence and unlocking the enormous potential of our endowment and unique supply chain. All these actions are translating into tangible results, protecting our margins and helping us build a more resilient and valuable company. 
Let me now turn to the highlights of the quarter. Starting with iron ore, production declined 6% year-on-year, mainly reflecting Serra Norte's performance. Despite lower production, sales remained solid at 86.3 million tonnes, slightly above last year, supported by strong performance at S11D in the Southeastern system, along with the sale of inventories built in previous quarters. At Serra Norte, which has been operating since 1985, production has gradually declined in recent years as run-of-mine availability has decreased. This reflects the natural evolution of the ore body together with the operational constraints in areas close to cave-related exclusion zones. 
In addition, the quarter's mine plan was impacted by a lower quality section of the ore body, which temporarily affected processing efficiency across our plants. We have taken a series of actions to mitigate these impacts, including the increased access to hematite ore in newly licensed areas and expect these initiatives to increase ore availability and support year-on-year production growth in the fourth quarter. Combined with the resumption of Fábrica and Viga and a solid performance across the rest of our asset base, including S11D, we remain well positioned to deliver at the low end of our production guidance for the year. 
Looking further ahead, we remain confident in our operational performance and more importantly, in our ability to generate value for shareholders. Projects such as Capanema, S11D Plus 20 and the Compact Crushing plant are adding flexibility while improving the resilience of our portfolio. At the same time, we remain fully committed to our value over volume strategy. Our focus is not simply on producing more tonnes, but on delivering the right volumes at the right cost and quality to maximize value creation. 
On the next slide, I would like to spend a few minutes on freight and explain how our strategy has protected our business. The spot freight market rose sharply in 2026, affecting the entire iron ore industry. In this context and in order to understand how our freight strategy has created substantial value, it is important to look at 2 main variables: the cost of the vessels or time charter and the cost of fuel or bunker. Each has different market dynamics, and our initiatives address both. 
On the time charter side, our medium- to long-term vessel contracting strategy provides greater predictability and supports a more competitive cost base. Over the coming years, around 75% of Vale's shipping needs are covered by long-term contracts at fixed rates. Most of the remaining 25% is managed through shorter-term contracts, generally lasting 1 to 2 years. This structure provides flexibility while limiting direct exposure to the spot market. 
For the fourth quarter, we are fully covered on our freight needs. And for 2027, we have already secured over 80%, giving us time and flexibility to capture opportunities for the remaining requirements. The fleet composition also provides an important advantage. Larger and more efficient vessels, including Valemax and Guaibamax ships consume less fuel per tonne transported and operate at structurally lower cost. On the fuel side, our hedging program provides another layer of protection and reduces our exposure to fuel cost volatility. Marcelo will discuss this in more detail shortly. 
To put all of this into perspective, since the first quarter, spot freight rates on the Brazil-China route have increased by $12 per tonne, while rates on the Australian-China route have risen by $4.9 per tonne. Over the same period, Vale's realized freight cost increased by only $4.7 per tonne. This shows that despite the increase in spot freight rates, our relative margin position has been preserved. Altogether, our freight strategy is generating a total benefit of more than $3 billion vis-a-vis the spot market in 2026. Overall, the message is clear. The freight environment has become more challenging, but our scale and strategy provided meaningful protection and preserved our competitiveness. 
Turning now to base metals. I'm very pleased with the progress we continue to make at VBM. Copper production declined 6% year-on-year, while sales were 4% lower, reflecting the planned maintenance at Sossego as expected. At the same time, Salobo delivered its highest third quarter production on record. This is a very positive result and reinforces the strength of our copper platform as we prepare for further growth. In nickel, production increased 6%, while sales grew 16% year-on-year. The Sudbury refinery delivered its highest quarterly output since the fourth quarter of 2013. 
Onça Puma also achieved its strongest third quarter performance, supported by the commissioning of the second furnace. Year-to-date, copper production has increased 4%, while nickel production has grown 8%. Based on these results and on the operational performance we are already seeing in October, we are confident in reaching the upper half of the production guidance for both metals. In October, we also completed the Thompson transaction. Vale Base Metals retained an 18.9% interest and secured a multiyear offtake agreement for nickel concentrate, allowing us to preserve strategic exposure while maintaining access to nickel units for our downstream assets. 
Looking ahead, we continue to advance our corporate growth strategy with the approval of the coarse particle flotation or CPF project at Salobo. The project is part of the new Carajás Program and will add 6 million tonnes per year to Salobo's core processing capacity, bringing the total to 42 million tonnes. Once fully ramped up, it is expected to add approximately 30,000 tonnes of copper per year contained in concentrate as well as approximately 15,000 ounces of gold as a byproduct. Start-up is expected in the first half of 2028. 
Together with Bacaba and our productivity initiatives in Canada, this project reinforces our confidence in achieving our production target of up to 500,000 tonnes of copper by 2030. We have also quadrupled our drilling meters in Carajás compared with 2 years ago. The results we are seeing give us even greater confidence in the copper potential, and we look forward to sharing more of this at our Vale Day in December. We believe Vale is well positioned to deliver above-average copper growth over the coming years. 
Much of this potential comes from brownfield opportunities that leverage our existing assets, infrastructure and technical capabilities, allowing us to pursue growth with low capital intensity and attractive returns. This creates a strong foundation for long-term value creation. With that, I'll hand over to Marcelo Bacci to discuss our financial performance. I'll return later for my closing remarks before the Q&A session. Marcelo, please.

**Marcelo Bacci** (Executives):
Thanks, Gustavo, and good morning, everyone. Pro forma EBITDA totaled $3.5 billion in the third quarter of 2026, 20% lower year-on-year. The decline mainly reflected external pressures on the iron ore business, including a 10% decline in realized prices, higher bunker costs and the appreciation of the Brazilian real. At Vale Base Metals, EBITDA reached $1.1 billion, increasing more than 60% year-on-year and representing 31% of Vale's EBITDA in the quarter. This solid performance was supported by higher realized prices across the portfolio, combined with solid and consistent operational execution, as Gustavo presented. 
Let's take a closer look at this quarter's details. Starting with iron ore, our C1 cash cost, excluding third-party purchases, was $23.1 per tonne. This was 12% higher year-on-year and 4% lower quarter-on-quarter. The all-in cost was $60.4 per tonne, increasing 21% year-on-year and declining 2% sequentially. The year-on-year increase reflected mostly a combination of currency and energy-related pressures. In the quarter, the stronger Brazilian real affected both the C1 and the all-in, while higher diesel and bunker fuel prices had an additional impact on operational costs and freight. 
Even in this more challenging environment, we expect both C1 and all-in costs to finish 2026 within their respective guidance ranges. Our hedging program continues to play an important role in managing this volatility. Including the cash benefit from the oil hedge, all-in cost was $59 per tonne in the quarter. At the same time, we are intensifying our focus on the factors that we can control. We recently launched a company-wide productivity program structured around specific work streams across operations, procurement, maintenance and logistics. 
The objective is not only to offset short-term pressures, we are targeting sustainable efficiency gains that can structurally improve our cost base. We will provide more details on first results and many opportunities at the Vale Day in December. Together with the ramp-up of lower-cost assets, these initiatives should strengthen Vale's position and improve competitiveness through the cycle. At Vale Base Metals, cost performance remains under control. In copper, all-in costs came at a negative $200 per tonne, improving by $1,200 per tonne year-on-year. This result was supported by strong byproduct revenues and lower unit expenses, even with the planned maintenance carried out during the quarter. 
Based on year-to-date performance, we expect copper all-in cost to finish 2026 near the lower end of the guidance range. The outcome will also depend on byproduct prices during the fourth quarter. In nickel, all-in cost was $14,600 per tonne, 18% higher year-on-year. This increase was expected and mainly reflected planned maintenance at the Canadian operations. With these maintenance activities now completed, we expect nickel costs to decline in the fourth quarter and return to levels broadly in line with the second quarter. We also remain confident in delivering our 2026 nickel cost guidance of $10,000 to $11,500 per tonne. 
Before moving to cash generation, let me provide more detail on our hedging program and how it supports the business. As discussed earlier, hedging plays an important role in managing market volatility. Our objective is not to predict market movements, but to reduce cash flow volatility, improve financial visibility and protect the execution of our business plan. This strategy is already delivering tangible benefits. So far in 2026, our currency and oil hedges have generated over $700 million in cash benefits. 
Starting with bunker fuel, we have already hedged 67% of our expected 2027 consumption, maintaining a level of coverage broadly consistent with 2026. Our average hedge price stands at $78 per barrel on a Brent equivalent basis through a combination of forward contracts and 0 cost collars. This gives us greater visibility on an important component of our freight costs as we enter 2027. On currency, our strategy has traditionally focused on protecting BRL-denominated debt and reparation commitments, while we also hedge a portion of our operational expenses in reais. 
So far this year, our currency hedge settlements have generated $456 million in cash benefits, and we entered 2027 with a solid hedge position at an average BRL of BRL 5.72, providing additional visibility on our BRL-denominated cash flows. Together with the freight strategy discussed by Gustavo, these positions demonstrate a disciplined approach to managing external risks. They reduce cash flow volatility, improve financial visibility and help protect Vale's competitiveness through the cycle. 
Now let me turn to cash generation. Free cash flow was solid in the third quarter despite the lower EBITDA. Free cash flow totaled $2.2 billion, supported by working capital release and the cash benefits from the hedging program I just discussed. Capital expenditures totaled $1.25 billion in the quarter, reflecting continued capital discipline and ongoing project efficiency initiatives. Based on the year-to-date performance, we expect CapEx to finish 2026 towards the lower end of the $5.4 billion to $5.7 billion guidance range. 
Overall, solid cash flow generation and disciplined capital allocation provide Vale with financial flexibility to execute its business plan, pursue capital-efficient growth and continue delivering attractive returns to shareholders. Expanded net debt ended the quarter at $16.4 billion, decreasing by approximately $200 million and remaining comfortably within the $10 billion to $20 billion target range. Importantly, net debt declined even after the payment of $1.7 billion in dividends and interest on capital in September. This demonstrates the strength of Vale's cash generation and balance sheet even in a more challenging market environment. 
Before handing the call back to Gustavo, I would like to reinforce that we remain focused on strengthening competitiveness across the company. Despite external pressures, our priorities remain unchanged. We continue advancing productivity and efficiency initiatives, improving asset performance and optimizing the cost structure. The freight and hedging strategies provide an additional layer of protection, while the ramp-up of lower-cost assets supports a more competitive cost base. Together, these actions help protect margins, support consistent cash generation and strengthen Vale's position through the cycle. Gustavo, please.

**Gustavo Duarte Pimenta** (Executives):
Thanks, Marcelo. Before we move to the Q&A session, let me go over the key takeaways of today's call. First, we remain on track to deliver our production guidance for the year across our portfolio, highlighting the continuous focus on operational excellence and asset reliability. 
Second, cost competitiveness remain a clear priority, and we are confident in delivering on all of our 2026 cost guidances. We are also accelerating efficiency initiatives, improving operational performance and unlocking further value across the portfolio. At Vale Day, we'll provide further details on our cost efficiency program and the opportunities ahead. 
Third, we continue to strengthen our business resilience. Our freight and hedging strategies provide meaningful protection in a more volatile market environment, helping preserve competitiveness and free cash flow generation. We also continue to advance our corporate growth strategy. The approval of the Salobo CPF project brings us closer to producing around 500,000 tonnes of copper in 2030 and on track to double our copper capacity to 700 kilotons by 2035. 
And finally, we remain disciplined in capital allocation. We continue to balance investments in operations and capital efficient growth with strong and consistent shareholder returns. 
Now let's open for the Q&A session. Thank you.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Mr. Leonardo Correa from BTG.

**Leonardo Correa** (Analysts):
So a couple of questions on my side. First, maybe moving back to the Serra Norte discussion at Carajás, right? I mean we've been -- I think Gustavo, you mentioned, right, this has been a multiyear process, right, of ore grade degradation and depletion. And I think the cave issue, the market has been following for quite some time. Maybe over the past quarters, I think the issue was probably less of a focus, right? And we saw several headlines on a potential new cave decree in Brazil, which I think brought some expectations, some hopes. 
So just on this theme, right, which probably remains one of the biggest challenges, right, operationally for the company. What have you been doing over the past, let's say, weeks and months? And what are expectations going forward on how to navigate these challenges, right, at Serra Norte? And if this level of production is a low, it would be great to hear you on those factors and maybe Rogério. 
And the second question, still on iron ore, 2 questions on iron ore, back to iron ore focus. Just on the supply rationalization, right? I think some weeks ago, Vale came out with a message saying that the company wasn't ready to adjust production levels even with these, let's say, very weak iron ore prices and very high freight rates. I think everyone knows that you guys work quite significantly on third-party purchases, right, which probably economics are reduced. You also have some higher cost mines in your portfolio. 
So I just wanted to review those if there's any decision on potentially streamlining your iron ore operations and adjusting to this much tougher reality that we've been living in. So those are the 2 questions.

**Gustavo Duarte Pimenta** (Executives):
Gustavo here. Thanks for your questions. Let me start with the northern range with Carajás. I'll have Carlos also help me here with what we've been doing there. But at a bigger picture, as you all know, we have 3 systems there. So we have S11D, which is doing very well, should be doing about 90 million tonnes with the potential to get to 100 million tonnes as we bring plus 20 online. So this is a system that it's operating and delivering quite strongly. Serra Leste, which we don't talk much, but we see potential for further growth there. We are doing about 8 million tonnes, should be getting to 10 million tonnes in the shorter term with the potential to get to 20 million to 30 million tonnes. 
So making sure those 2 systems continue to expand is very important for us in the Carajás province, and we are accelerating the development of those 2 systems. On the Northern range, the key challenge, as I pointed out in my prep remarks, is the caves-related restriction. We continue to be hopeful that this will come. It is -- as you know, it is not only beneficial for mining, for Vale, but for all infrastructure investments in Brazil. We see an opportunity for that -- for the caves to be modernized. 
So we continue to monitor that closely. But internally, we work and guide you guys and guide the market independently of having the caves released or published. So we develop plans, assuming the caves will take substantially longer to make sure we continue to have alternatives in our plans. And that's the way we've been working on. But I'll hand over to Carlos to cover what we've been doing there, and then he can send me back for the market comment as well.

**Carlos Medeiros** (Executives):
Thank you, Gustavo. So a bit of an update on Serra Norte. First, on Q3, we had, I think, 3 points that are important to share with you. So the first one was reliability issue related to our fleet. So mechanical problems, but most importantly was the start-up of 28 new autonomous trucks. So as of today, we have 42 autonomous trucks up and running in Serra Norte. And all of these problems are behind us. Everything is back to normal in terms of performance. 
Second, we also were mining at the bottom of the pit and therefore, due to some rains that we had during this period, we lost a few days, and now we are back on track. And third, we are mining in an area where all the contact ore there had a high content of manganese and alumina. And therefore, these 2 elements carry with them a lot of clay, which end up clogging our hoppers. So all in all, all these 3 factors combined together led us to a lower performance. 
Today, during October, we are already operating at 15% higher daily average production at Serra Norte. So we are totally back to normal. Now when we think further ahead, I would say for next year, we should move sideways in Serra Norte as far as volumes are concerned. And by 2028, I think there are 2 important steps that you all should have in mind. The first one is this expansion at Serra Leste, where we should move from the current 8 million tonnes a year to 10 million tonnes a year and also a new ore body called N3 that is expected to produce around 6 million tonnes per year. And the combination of these factors give us confidence that Serra Norte should be in the near future back to its normal production levels. So I'll hand back to Gustavo.

**Gustavo Duarte Pimenta** (Executives):
Thanks, Carlos. Leo, on your second question on the market, you've heard us saying our view today is that about 10% of seaborne or 160 million tonnes is actually losing money and should be over time shut down or adjusted. We've seen some of that capacity going off the market. In our particular case, in the case of Vale, every single vessel that we sell has some margin, right? So we are very focused on the value over volume strategy. And I would say that sitting where we are today for next year, we probably have about 5 million tonnes between third-party and own production at risk that could be eventually adjusted down but we'll provide more details at Vale Day.

**Operator** (Operator):
Our next question comes from Mr. Rodolfo Angele from JPMorgan.

**Rodolfo De Angele** (Analysts):
Can you hear me now? Okay. Sorry. I have -- my 2 questions are on iron ore. The first one, I wanted just to do a follow-up on the discussions on the Northern range. So clearly, there were unique situations in this quarter, but there is a declining trend in Serra Norte, which is -- I think it's fair to say that it is an older mine and there's an effect of depletion. So can you talk a little bit more when you talk about the additional hematite that we could see in the coming quarters? 
And is there without a change in Caves legislation, a strategy that could at least maintain production in current levels? Or what is the status quo of the future of those operations? And the second question, we were, of course, given where prices are of iron ore and given especially the stronger currency we saw during the third quarter, there is an increased concern on what can be done on the cost side. We had the impression here that there were a few items that surprised us a little bit to the upside. And I just wanted to hear from you, how do you feel about costs? Is there something that can be done just overall, thinking about 2027. I know guidance is going to be given on Vale Day, but just at least a framework for us to think about cost.

**Carlos Medeiros** (Executives):
So Rodolfo, this is Carlos. On the hematite, the reason our performance improved in October is because we are back on mining on the hematite front, and we expect to remain on this front until the end of the year. That's why we are confident that our guidance projection will be met. So what we saw was a type of ore that jeopardized a bit our performance in Q3, but it's back to normality, as I mentioned. 
And going forward, on the -- I think our main project outside the FLONA, the National Forest is the expansion of Serra Leste. So Serra Leste, as I mentioned, is today producing 8 million tonnes. First step will be to move it to 10 million tonnes. And the second step will be taking this capacity to 30 million tonnes. So the combination of all these numbers will restore the Northern performance to levels that we expect. So I will hand over to Marcelo to talk about the cost.

**Marcelo Bacci** (Executives):
Thank you, Carlos. Rodolfo, the cost, we've been working very hard on compensating some of the inflationary effects that we see on the cost. You saw some effects already on Q3 with costs at the C1 level a bit below the previous quarter. For Q4, we expect to see both at the C1 level and all-in level relatively stable costs in relation to this quarter within the guidance range. C1 probably a bit below and all in a bit above, but within the range of the guidance. For 2027, I would prefer to leave this discussion for Vale Day.
We have a series of initiatives that we're going to discuss there to further enhance our cost position. The idea is to continue to have countermeasures in relation to the inflationary effects that we have. And I would like also to mention that on the CapEx side, we've been working very hard in bringing the number closer to the lower end of our guidance for this year, also working on efficiency on the CapEx as well.

**Operator** (Operator):
Our next question comes from Mr. Rafael Barcellos from Bradesco BBI.

**Rafael Barcellos** (Analysts):
So first question on iron ore, but a bit connected with capital allocation. So given the pressure that the iron ore market has been facing, I just wanted to understand whether the company could consider any sort of tactical M&A initiatives. I mean we saw recently the announcement of the acquisition of Ligga. So I just wanted to understand better your thoughts on this M&A given the market situation. And second question then moving to base metals. If you could provide any updates on Alemão, which is the most important project here, particularly on the timing could be interesting as well.

**Gustavo Duarte Pimenta** (Executives):
Rafael, Gustavo, I'll do the first one, and then Shaun will add on VBM and Alemão. Look, we continue to have very constructive views on iron ore despite the recent challenges we are seeing in the marketplace. If you look in terms of global population growth, industrialization, there's a series of long-term macro trends that support the iron ore industry from our perspective. So we are certainly looking into opportunities. You've seen us doing some. We've done Ligga, but we also had done before the acquisition of 15% of Minas-Rio. So those type of transactions that create value and leverage existing infrastructure are certainly something we are excited about and we are exploring. So stay tuned. Hopefully, we'll be able to consider to -- continue to look for those type of opportunities going forward.

**Shaun Usmar** (Executives):
Rafael, it's Shaun. On your question on Alemão, I mean, you've seen the progress on the first 2 projects where we've been able to accelerate them. On Alemão specifically, we're seeing good cooperation with IBAMA. The engineering and the work on the project is well on track. So IBAMA has completed the review and published the project's environmental impact report. So that has set up the groundwork for the public hearing, which will happen next month. That was delayed slightly because of the election. I think the key thing for us is the timing for the LP, we believe, is on track. And we're looking for our FID next year and should be on track for what we've been targeting, which is 2030 on production.

**Operator** (Operator):
Our next question comes from Mr. Carlos De Alba from Morgan Stanley.

**Carlos de Alba** (Analysts):
Yes. Maybe just on copper, the Salobo CPF project obviously is coming about a year ahead of schedule. What does that tell us? Is it possible maybe to extrapolate that the entire copper pipeline could be pushed forward and come earlier than expected? Or maybe, as you just pointed out, Shaun, on Alemão is going to be on a case by case, and we should not get too ahead of our skis on that. And then on iron ore, iron ore, I guess, freight, just wanted to see if there was a significant or a meaningful impact on cost, C1 cash cost or all-in cash cost in the fourth quarter from the one-off impact of the fleet issue that Carlos alluded to earlier. 
And on freight, any views given the, I guess, visionary hedging strategy that you guys put in place for next year? Any views on how your freight costs might move in 2026 versus 2020 -- sorry, in 2027 versus 2026?

**Shaun Usmar** (Executives):
Carlos, it's Shaun. On your first question, I guess the way that we've approached this is multifold. I mean copper in the sector as a whole traditionally undersupplies or underdelivers by about 5%. And I think this year is probably on track for the first annual decline since something like 2017 on the supply side. So for us, it's been multifaceted, and this will tie into, I think, hopefully, context on your question. First is, operationally, we've had to deliver. You saw we beat guidance last year. 
We revised cost guidance at the half year positively. And you heard from Gustavo, we're on track for delivery on that and importantly, at the upper end again. And that's at a time with obviously the significant planned maintenance activities, particularly at Sossego. I think it's noteworthy that Sossego, even with that, will be on track to produce more copper this year than they did last year, and that's including the planned maintenance. Vinny and his team have really had a record half year despite it being a pretty old mine. 
And at Salobo, you saw the record. We're also bringing on autonomous fleets. And what we see with the CPF and the acceleration by a year, that coarse particle flotation, that extra 6 million tonnes, that ability to take Salobo up to sort of 230,000 to 250,000 tonnes a year in the future, plus additional optionality on Salobo 1 and 2, which is not really in the plan right now. So I give that to you because at the same time, as you heard from Gustavo, we quadrupled -- more than quadrupled drilling in Pará just over the last 18 months or so. There's more to go, and we keep finding more copper. 
So I think to answer your question, when you consider the exploration, you consider the operating performance that lowers costs and actually enables projects, capital intensities are low. And we're looking at this on a district scale and that ability to be able to see in each and every one of these, where is the physical constraint, how do we take advantage of these relatively sort of low capital intensity, quite favorable risk opportunities as a portfolio. And a number of these, we've accelerated quite significantly and some we pushed out. And so we'll unveil more at Vale Day. 
I think the first thing is building the credibility, which hopefully the market is now starting to appreciate. And I think the real opportunity is not just giving certainty around that sort of 2030 -- not just the current time, that sort of 2030 time frame. But I think there's, as I've said before, significant opportunity beyond that. And the market still is really only pricing in essentially flat copper coming out of this business, which is slightly unusual.

**Marcelo Bacci** (Executives):
On the cost side, I think at the C1 level, as I mentioned before, we expect to have in the fourth quarter, something similar to what we had in the third quarter, which is going to lead us to be within the guided cost that we have closer to the upper range. On C1, on all in, we expect to have Q4 closer or closing the year closer to also the high end of the guidance within the guidance. But for the fourth quarter, it's going to be higher than the third quarter. 
For 2027 on freight, I think if we were to close our position today, hiring what we have not hired both in terms of the daily rates and in terms of fuel at current market prices, this would lead us to something close to the range of 24 to 25. We are not doing that because we think the market will offer better opportunities to close that gap, but just to give you an idea of where we are.

**Operator** (Operator):
The next question comes from Mr. Christopher LaFemina from Jefferies.

**Christopher LaFemina** (Analysts):
I have 2. The first one is on iron ore and the second one is on buybacks versus M&A. So in your product mix, you've had pretty significant changes over the last few quarters in the mix. And I'm wondering if that is a function of the restrictions at Serra Norte or a function of how the market is changing in order to kind of optimize pricing in a weaker market and how we should expect the product mix to look going forward? That's the question on iron ore. And then the question on buybacks versus M&A. 
I mean looking at what your share price has done, if you're constructive on the outlook for iron ore, it seems like the optimal capital allocation strategy might be to buy back your own shares. You don't have to pay a premium to do that. You're not taking a lot of risk around doing that. You can do that at your own discretion. And your stock is very inexpensive and it's a way to kind of grow volumes on a per share basis. So I'm wondering, you mentioned earlier just looking at opportunities around M&A. How do you weigh that up against the potential to buy back your own very inexpensive shares?

**Rogério Nogueira** (Executives):
Chris, this is Rogério. On your first question on product mix, whether our adjustment was based on the market or the mine. It is on both. We have been saying all the time that we are optimizing for total results, not only prices, not only production, not only costs, but optimizing the total contribution. I think, as you know, the market is challenging. A lot of our competitors are working with very thin or even negative margins. They don't require productivity. Thus, for example, putting a lot of high-grade iron ore into the market does not necessarily translate into higher premiums. 
We have then optimized our product mix, as an example, selling more mid-grade products from Carajás. So the answer is both. We're constantly looking into the market and the mines to flex our supply chain and product portfolio offering.

**Marcelo Bacci** (Executives):
Chris, on capital allocation, I think we agree with you that the share looks inexpensive and buybacks are very attractive. And to the extent that we generate capital over the coming months, that's always a possibility. We have a program open. As I mentioned before, additional capital that we generate, we tend to be in the future more balanced between buybacks and dividends. That's always something that we're looking at. It's difficult to compare that with M&A because M&A carries, of course, the market momentum, but also carries a strategic component that may be important. And this may be a moment where M&A opportunities become relatively inexpensive and they can bring us other advantages that we can see more on the long term. So we don't foresee at this point any major M&A alternative, but we're going to be looking at the possibilities.

**Operator** (Operator):
The next question is from Daniel Sasson from Itaú BBA.

**Daniel Sasson** (Analysts):
My first question is related to the following -- to the recent agreements between CMRG and Rio Tinto, if you see any risk that Vale becomes relatively disadvantaged in commercial negotiations in China? Or do you think that Vale's product quality, blending capabilities and the relationships you have with specific customers make your position fundamentally different in those negotiations? 
And my second question, maybe, Gustavo, you mentioned that you see 160 million tonnes of seaborne supply being currently loss-making, right? If Chinese steel demand weakens further from where we are, do you expect the market to rebalance primarily through high-cost supply leaving the market? Or do you think that the majors could also -- or would also need to adjust volumes because you mentioned that you do have maybe something around 5 million tonnes of your own production that might be at risk, if I understood correctly, right? Those are my questions.

**Rogério Nogueira** (Executives):
Daniel, this is Rogério. I'll take your first question. And on CMRG, you have recently seen that Rio Tinto has settled. They have been in conversations now with FMG. We also have been in conversations with CMRG for a long time. I think you pointed it right. We have a good relationship. We're trying to build with them a win-win solution. We have, as you said, a product quality that puts us in a better position to negotiate, and we have very good relationships. So all in all, we have nothing to add to the discussions or to the points we've made before. We're confident that we'll come to a good conversation and agreement with them when time comes.

**Gustavo Duarte Pimenta** (Executives):
On the second question, Daniel, look, we believe most of the capacity that should exit the market are the ones that are marginal producers, right? So they have less ability to contract long term the freight. So they are more exposed vis-a-vis, for example, what we have. But having said that, I think to your question on potential scenario of further deterioration, for example, in China, I could see some of the majors also adjusting their capacity going forward. So we'll have to see how the market evolves. Most of our understanding of the capacity probably will be from the marginal producers.

**Operator** (Operator):
Next question comes from Mr. Jon Brandt from HSBC.

**Jonathan Brandt** (Analysts):
Sorry to come back to iron ore and the cost side and supply rationalization, but I think it's an important subject. I think, Gustavo, you mentioned that all of the vessels that sailed in the third quarter were margin positive. But I know in the past, you've talked about not just being margin positive, but being above your cost of capital. So I guess if you could maybe give us a little more detail on were all the shipments that left, were they earning a return above your cost of capital? And I guess kind of related to that, I guess I'm a little surprised to hear that there's only about 5 million tonnes that may come offline next year. 
I would have expected a lot of the third-party ore that you buy, which I think is around 30 million tonnes a year. Could potentially be at risk, particularly since if you didn't buy it, you wouldn't have to go out into the spot market and buy higher freight. So I'm hoping you can give us a little bit more details on just kind of the profitability of this third-party ore and if that's something that could be cut if we were to see weaker iron ore prices next year?

**Gustavo Duarte Pimenta** (Executives):
Thanks, Jon. I'll have Rogério covering some of the details, please.

**Rogério Nogueira** (Executives):
Thanks, Jon. Look, I think first to say that and reinforce that all the volumes that we have commercialized from third parties are contribution margin positive. Second point is that we do have flexibility if those margins turn negative to shut down those volumes, okay? So we generally work with very short-term contracts or the pricing mechanism on such that gives us that flexibility. It's important to say that we have a different margin because we have our own ports only based on costs. We have special rates for the railways. We have contracted long-term contracts on TCs, which are much lower than the traditional market. But rest assured that if any of those volumes come into negative territory, we'd stop it.

**Operator** (Operator):
The next question is from Caio Ribeiro from Bank of America.

**Caio Ribeiro** (Analysts):
So my first question is on cash return prospects. I just wanted to see how you are thinking about extraordinary dividends this year and next. And if you see room linked to this, right, for a divestment of a stake in Hu'u that could eventually lead to an eventual extraordinary dividend payment if this transaction is concluded at some point? And then more of a question on the outlook for the iron ore industry. 
I wanted to ask, given that strong ramp-up of Simandou this year and assuming that the recent run rate per month, which suggests that there's still a material increase contracted for next year, if you see that impacting the strategic relevance, right, of your Carajás ore, in particular, given the high iron ore grade that Simandou ore provides, I know that there are some differences in the alumina and silica content of that ore versus your grades, which suggests that Vale can still be used as a corrective ore for Simandou. 
But as far as blending with Chinese lower-grade ore, does that ramp-up provide a viable substitute for your Carajás product? And also on the market outlook, the recent presale policy reform in China, I'm curious to hear from you how do you see that impacting construction-related steel demand in 2027?

**Marcelo Bacci** (Executives):
Caio, I'll take the first one. In terms of extraordinary dividends for this year, we believe it's unlikely given not so much about the cash flow that we're going to generate this year, which is going to be strong anyway. But given the uncertainties of the outlook on the geopolitical side for next year, we will prefer to be on the safe side, retaining a bit more cash and having a lower level of indebtedness. And with Hu'u, we are not, at this point, considering a divestment. We are still discussing with potential partners a way to develop this project in the future.

**Rogério Nogueira** (Executives):
Caio, let me just give you first a little bit of an overview of the market, okay? When you look into global crude steel production, we see a market which is relatively stable up to now in the 9 months 2026. There's been a slight decline of 0.7% a year. When you look into China, China declined 3% in crude steel production, same in pig iron production when you look into official numbers. But if you take independent surveyors, this number is more closer to a decline of 0.6%. The domestic market, as you know, is challenging, is weak and China has relied a lot on the exports. 
Now we estimate that about 130 million tonnes of crude steel would be exported from China. But interesting, when you look into the imports of iron ore into China, there has been an increase of 4.1% in the 9 months 2026. And at the same time, the inventories were kept at a stable level compared to last quarter at 165 million tonnes. I think -- and plus, this is explained by some shutdowns or some reduction in the domestic production of iron ore in China. So market is still balanced, right? Seaborne iron ore, as we look at, is quite stable. There has been no growth in the seaborne supply. 
Even though Simandou, as you pointed out, has increased is actually producing at a run rate that we estimate at 50 million tonnes at this point in time. So even with that, we see a market supply, which is relatively stable, as I just mentioned. And when you look outside China, crude steel production is growing. I'll give you just some example of some regions, Vietnam growing 26%, India growing 6%, the United States, 6% and even Europe with all these measures of CBAM and the tariffs and quotas with a very positive outlook. 
So we have some sort of a relatively optimistic view. And specifically, when you ask about Simandou, as you point out, Simandou in terms of quality is high alumina, it's good quality Fe, but it's high alumina. It does compete with Carajás. At this point in time, it has a little bit less of a quality. But then our flexibility in the supply chain, we will work with our Carajás volume to manage and be able to still have good premiums. 
On the blending side, as you just talked, yes, I think given the fact that they are high alumina, low silica, there is a requirement for blending, and that actually is a good signal for other products that we have, such as the high silica, such as the pellet feed that we concentrate in China. So we see that when we look into the comprehensive portfolio, provided the flexibility that we have in the supply chain, we will manage to maintain our price realization, the premiums for our products, okay? And on the incentive for housing, we don't see much of a change in the market for that.

**Operator** (Operator):
The next question comes from Marcio Farid from Goldman Sachs.

**Marcio Farid Filho** (Analysts):
A couple of follow-ups on my side. I think the first one on Serra Norte. I think, Carlos, you mentioned plus 15%. I just wanted to understand if that's quarter-on-quarter. If so, I think that would imply minus 20% year-on-year. So -- and then you mentioned expectations for production to run sideways into 2027. I mean we've seen some depletion of between 15% to 20% year-on-year, right? So just trying to understand what is the base? And how should we think about volumes into next year for Serra Norte. 
And then a follow-up on the product mix. Rogério, I'm sure it's going to be you're probably scratching your head thinking about next year because there is so many moving parts with your portfolio, your mining availability and obviously, Simandou ramp-up and China's requirements as well. So I mean, as you think into next year, right? So what sort of base portfolio you're thinking about? Obviously, IOCJ is representing less than 5% of the portfolio today. And like you mentioned, mid-grade kind of just being replaced a lot of that. So how do you think about consolidating all those moving parts as you potentially work on the guidance for next year?

**Carlos Medeiros** (Executives):
So Marcio, this is Carlos. talking about Serra Norte. So what happened in Q3 is that we -- September volumes were -- I'm talking about daily -- average daily production. September was higher than August and August was higher than July. What I'm saying is that in October is now higher than September by a factor of 15%, just to give a sense of normality. So when I think about Serra Norte production, we are talking about approximately 64 million tonnes a year. That's the reference number. This should be added with 8 million for Serra Leste and another 90 million of Serra Sul. These are the numbers in general terms that we work with, totaling 160 for the entire northern corridor. I think that summarized well.

**Rogério Nogueira** (Executives):
Marcio, on the product mix, important again to reinforce that we do have flexibility and we will adjust accordingly. But when we look into next year, we don't expect much of a change in the steel margins for the steelmakers and not even for coal prices. So the base load that we're working with are our mid-grade products, which is PFC1, which is commanding $3 to $4 premium over MB61 when you sell it in China, our mid-grade Carajás and our BRBF, which is commanding a $6 premium over MB61. 
So base case, as we see it today, focus the portfolio base load being on the mid-grade products and we'll play IOCJ depending on how the market goes, depending on productivity requirements.

**Operator** (Operator):
And the last question comes from Ms. Timna Tanners from Wells Fargo.

**Timna Tanners** (Analysts):
Can you hear me?

**Gustavo Duarte Pimenta** (Executives):
Yes, we can hear you.

**Timna Tanners** (Analysts):
Just quick ones. On base metals, I mean, we understand that your endowment already allows Vale to grow target ambitions by 2030 and '35. But I mean, you have been very vocal about drilling and exploration initiatives. So just trying to understand how has that evolved? And where do you see most upside, thinking of potential additions to your reserves and resources over time. And a quick follow-up on freight, but Bacci, you mentioned $24 to $25 per tonne as potential freight rates after market conditions for 2027. Just thinking that, that already includes the oil hedges and how could that affect your kind of net freight expenses after the oil hedges for next year, considering your coverage for Brent prices?

**Shaun Usmar** (Executives):
Thanks for the question on the drilling. Look, our organization and base metals normally does around $170 million a year on exploration. Just to remind you and others of the changes in the 2 years, we've kept that rate steady and in years ahead, we'll continue, but we've changed the allocation, obviously, towards copper and specifically on Pará. And what we're finding is notwithstanding the relative maturity of the district, it is actually underexplored for copper. So we've focused there. If the traditional run rate, say, in '24 and before was about 20,000, 30,000 meters of drilling a year. Last year, we went to 65,000. This year, we're on track for over 120,000 meters, and I want to do more. We've lowered the unit cost on that about 40% in Pará at the same time. So it's just allowing us to be more efficient. 
And we are targeting areas to add NPV and life around projects that are in the nearer term as well as further out as well as with our existing operations. And we're finding good success. So to remind you on that, and we'll provide more detail on Vale Day, we said last year that from 2024 levels, we were looking to add over 20% to reserves and resources, for example, by next -- late next year. You would have seen our statements we put out around the time of our Investor Day earlier this year, we're very well on track, and we keep finding more opportunity. 
And we're building this into iterative life of business planning. And you'll see, again, more detail when we get to Vale Day. But if you go back to the materials last year, you'll see even below the Sequeirinho pit at Sossego, the intercepts are ridiculous, like they're really good, and we have none of them in our plans currently. And to one of the earlier questions that was posed about future growth and acceleration, I really think when you go beyond the fact that it's nearer life, it's giving us a portfolio of possibilities to potentially accelerate and derisk growth on a regional basis. 
The one thing that's been missed, I think, and we'll talk more again on Vale Day is the polymetallics. Remember, we've sold down on Thompson, which was just nickel. The rest of the portfolio, particularly in Canada, is polymetallic. And we are preferentially targeting copper in those ore bodies. In this month, for example, at Coleman, part of the change in byproduct credits from Q3 into Q4 is a stope of 7% copper that we're mining there right now. If you have LinkedIn, you go and look at myself or my Chief Operating Officer's feed, you'll get a visual of that. 
And I think there's more opportunity also to preferentially target copper growth in that in the nearer term in what was traditionally seen as a nickel business. And so that's how we're looking to take advantage of these ore bodies and frankly, to increase our value addition through the drill bit.

**Marcelo Bacci** (Executives):
On the freight side, as you know, there are 2 components to the freight. One is the time charter, the other is the fuel and they respond to different market dynamics today. On the time charter, we expect that as the market adjusts supply and demand, there may be opportunities to hire the exposure that we have at better terms than what we see today in the market. 
All this imbalance that we have on the pricing side between supply and demand with a significant portion of the players underwater will have to be adjusted in a combination of time charter rates and price on a relative weight that we cannot precise at this point, but this leads us to believe that we're going to have a better opportunity to do it. Our long-term contracts, nothing of those will mature next year. So we don't have to worry about renewals so soon. 
And on the fuel side, this is responding basically to the dynamics of the conflicts in the Middle East. When the market gives us opportunities, we try to gradually close the gap that we have for next year.

**Operator** (Operator):
This concludes today's question-and-answer session. Vale's conference is now concluded. We thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### VALE_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜Marcelo Bacci｜guidance：鐵礦 C1 現金成本 2026 指引上調至 22.5–23.5 美元/噸，原為 20–21.5。（原話："with our previous guidance of $20 to $21.5 per ton."）
- 2026-07-31｜Marcelo Bacci｜guidance：鐵礦 all-in 成本指引更新為 58–62 美元/噸（原 52–56）。（原話："updating the all-in cost guidance to $58 to $62 per ton"）
- 2026-07-31｜Marcelo Bacci｜guidance：銅 all-in 成本指引下調為 0–500 美元/噸（原 1,000–1,500）。（原話："now expect all-in cost to range between $0 and $500 per ton"）
- 2026-07-31｜Marcelo Bacci｜guidance：鎳 all-in 成本指引下調為 10,000–11,500 美元/噸（原 12,000–13,500）。（原話："all-in cost to range between $10,000 and $11,500 per ton"）
- 2026-07-31｜Gustavo Pimenta｜guidance：CEO 表示對達成全年所有產量指引有信心。（原話："reinforcing our confidence in achieving all production"）
- 2026-07-31｜Marcelo Bacci｜margin：新成本指引的匯率假設為 BRL 5.13（原 5.60）。（原話："average BRL exchange rate of BRL 5.13 compared to BRL 5.60"）
- 2026-07-31｜Marcelo Bacci｜margin：新成本指引的布蘭特油價假設為 86 美元/桶（原 68）。（原話："average Brent oil price of $86 per barrel versus $68"）
- 2026-07-31｜Marcelo Bacci｜margin：管理層拆解 C1 上調約 70% 來自匯率與柴油等外部因素。（原話："combined impact of external effects such as FX and diesel"）
- 2026-07-31｜Marcelo Bacci｜margin：Q2 鐵礦 C1 現金成本（不含第三方採購）24.1 美元/噸，年增 9%。（原話："was $24.1 per ton, an increase of 9% year-on-year."）
- 2026-07-31｜Marcelo Bacci｜margin：布蘭特油避險帶來約 1 億美元效益，約 1.6 美元/噸，扣除後 all-in 為 60 美元/噸。（原話："approximately $100 million benefit equivalent to $1.6 per ton"）
- 2026-07-31｜Marcelo Bacci｜margin：效率計畫與 S11D 等低成本資產使 C1 年減 0.50 美元/噸。（原話："$0.50 per ton reduction in C1 cost year-on-year"）
- 2026-07-31｜Marcelo Bacci｜margin：Q2 pro forma EBITDA 41 億美元，年增 19%。（原話："representing a strong 19% increase year-on-year"）
- 2026-07-31｜Marcelo Bacci｜margin：管理層解釋下半年 C1 下降而 all-in 持平，因 all-in 的油價權重較高。（原話："the C1 reducing in the second half of the year"）
- 2026-07-31｜Marcelo Bacci｜margin：Q2 自由現金流含匯率與油價避險交割 3.37 億美元正向現金影響。（原話："contributed a positive cash impact of $337 million"）
- 2026-07-31｜Gustavo Pimenta｜capital_allocation：董事會核准 17 億美元股息與資本利息，9 月支付。（原話："approved $1.7 billion in dividends and interest on capital"）
- 2026-07-31｜Marcelo Bacci｜capital_allocation：新庫藏股計畫最多 1 億股、18 個月，約占流通股 2.3%。（原話："a new share buyback program of up to 100 million shares"）
- 2026-07-31｜Marcelo Bacci｜capital_allocation：擴大淨債務 Q2 收在 167 億美元，管理層預期朝 150 億參考水位收斂。（原話："converging towards our reference level of $15 billion"）
- 2026-07-31｜Marcelo Bacci｜capital_allocation：管理層說明股東回饋總額取決於下半年現金流。（原話："remuneration will depend on cash flow generation"）
- 2026-07-31｜Marcelo Bacci｜capital_allocation：管理層稱大部分現金流發生在下半年，新成本指引不致實質改變下半年現金流潛力。（原話："most of our cash flow generation comes in the second half"）
- 2026-07-31｜Marcelo Bacci｜commitment：CFO 對年底擴大淨債務接近 150 億美元表達信心。（原話："we should be approaching close to $15 billion"）
- 2026-07-31｜Gustavo Pimenta｜commitment：Bacaba 試車提前至 2027 年第三季（原 2028 上半年）。（原話："commissioning in Q3 2027, significantly ahead of"）
- 2026-07-31｜Gustavo Pimenta｜commitment：銅產量目標：2035 年倍增至約 70 萬噸/年。（原話："ambition to double copper production to approximately 700,000 tons"）
- 2026-07-31｜Carlos Medeiros｜commitment：Brucutu 導入 Conceição 同類技術，預計明年上半年完成。（原話："expect to complete during the first half of next year."）
- 2026-07-31｜Shaun Usmar｜commitment：Salobo 粗顆粒浮選預計數週內正式公告。（原話："publish the coarse particle flotation announcement"）
- 2026-07-31｜Shaun Usmar｜commitment：VBM 執行長稱 Alemão 為本十年末第一個大型專案，進度符合計畫，不暗示提前。（原話："is Alemão, and we're on track for that"）
- 2026-07-31｜Gustavo Pimenta｜product：Serra Sul +20 與 Compact Crushing 合計新增 2,000 萬噸產能。（原話："will deliver 20 million tons of incremental capacity at Serra Sul"）
- 2026-07-31｜Shaun Usmar｜product：Bacaba 重組後資本支出降近 50%，報酬率由約 50% 升至近 70%。（原話："a couple of hundred million dollars, nearly 50% reduction"）
- 2026-07-31｜Shaun Usmar｜product：Bacaba 先前報酬率約 50%，現接近 70%。（原話："the returns that we had previously at about 50% are"）
- 2026-07-31｜Shaun Usmar｜product：Salobo 粗顆粒浮選預計 2029 年時間框。（原話："that's sort of the 2029 time frame"）
- 2026-07-31｜Carlos Medeiros｜product：Conceição 專案後產品組合由 50/50 變為 75% 直接還原級、25% 高爐級。（原話："the mix has changed to 75% direct reduction and 25% blast"）
- 2026-07-31｜Shaun Usmar｜product：VBM 執行長談 2028–2035 年可能超越 70 萬噸的探勘與規劃方向。（原話："go perhaps beyond the 700 because the rocks are there"）
- 2026-07-31｜Shaun Usmar｜product：整體投資組合目標 18 個月至 2 年內儲量與資源增加逾 20%。（原話："more than 20% increase in reserves and resources"）
- 2026-07-31｜Shaun Usmar｜product：Bacaba 加上 Sossego 後端，增量約 1.5–2.5 萬噸。（原話："15,000 to 25,000 ton incremental"）
- 2026-07-31｜Shaun Usmar｜risk：Sossego SAG 磨機停機 110 天（8–11 月），影響下半年銅成本與產量。（原話："That's the 110 days of downtime from August through"）
- 2026-07-31｜Gustavo Pimenta｜risk：洞穴法令（Caves Decree）修訂細節未明，對影響的評估尚早。（原話："So it's early to say what is the potential impact."）
- 2026-07-31｜Gustavo Pimenta｜risk：Fábrica 與 Viga 營運面已就緒，待州與聯邦授權；管理層稱不影響全年指引。（原話："we are not expecting to have an impact in our annual guidance"）
- 2026-07-31｜Rogério Nogueira｜risk：Oman 球團廠 10 月將停機進行新選礦廠併接。（原話："We'll have a stoppage in October to do a tie-in for the new"）
- 2026-07-31｜Marcelo Bacci｜risk：公司未在近期進行營運成本相關的短期匯率避險。（原話："we have not been operating short-term cost-related FX"）
- 2026-07-31｜Rogério Nogueira｜competition：管理層認為中國需求面比國內指標顯示的更平衡。（原話："China story is more balanced than the domestic indicators"）
- 2026-07-31｜Rogério Nogueira｜competition：管理層模擬成本曲線：每噸 95 美元時約 1.2 億噸鐵礦達成本極限。（原話："you'd have about 120 million tons of iron ore that would actually"）
- 2026-07-31｜Rogério Nogueira｜competition：海運現貨曝險由 25% 降至約 10%，下半年曝險亦低。（原話："decrease the exposure that we had of 25% to about 10%"）
- 2026-07-31｜Marcelo Bacci｜competition：2027 年燃油避險約 70%，布蘭特均價約 77 美元。（原話："70% hedging for 2027 at an average price of about $77"）
- 2026-07-31｜Gustavo Pimenta｜customer：CEO 稱公司希望持續投資銅，並預期未來更高度投入。（原話："you should expect us to continue to be highly invested"）

### 問答異常語氣（迴避／改口／保留）
- VALE_Q2_2026_Earnings_Call_20260731.md｜問：Marcio Farid（Goldman）：新簽長期海運合約的費率是否與舊約相近、有無被現貨價格影響｜答法：Rogério 稱「I cannot disclose exactly the numbers, but the numbers have been pretty good」，未給費率數字
- VALE_Q2_2026_Earnings_Call_20260731.md｜問：Daniel Sasson（Itaú BBA）：成本上調下，回購加速或發特別股息 vs 保守保資產負債表的取捨｜答法：Bacci 未表態偏向，稱視年底淨債務而定，決定留待第三季末或第四季初，並說回購與股息之選擇要看股價與稅務
- VALE_Q2_2026_Earnings_Call_20260731.md｜問：Daniel Sasson（Itaú BBA）：Bacaba 的做法能否複製到其他專案、是否可能提前達成 2035 目標｜答法：Shaun 先答「the short answer is yes」，但隨後稱不想在此階段暗示 Alemão 會提前，並說待年底更新生命週期規劃
- VALE_Q2_2026_Earnings_Call_20260731.md｜問：Alex Hacking（Citi）：Bacaba 提前後未來 2–3 年 Sossego 該如何建模｜答法：Shaun 未給 Sossego 逐年數字，談成本下降、鑽探upside 未納入礦山計畫，並請「stay tuned」待年底更新

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
{"date":"20260525","verdict":"衛星候選 / 高股息 deep value 觀察","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Vale Base Metals EBITDA 持續 ramp 至 FY28 $5B+","columns":{"2Y":"FY26 全年 BM EBITDA &gt; $4B + Q4 26 nickel +50% YoY","5Y":"FY28 BM EBITDA $5B + Salobo Stage 4 evaluation","10Y":"VBM IPO 或新銅項目 evaluation","門檻":"BM EBITDA YoY &gt; +30%（Q1 26 + 116% 基數）","來源":"Vale Q1 26 results","漂移":"連 2 季 BM EBITDA YoY &lt; +20% → 削弱"}},{"id":"H2","text":"2026 dividend 維持 $1.2-1.3/share（7%+ yield）","columns":{"2Y":"FY26 dividend &gt; $1.0/share；payout 80-100%","5Y":"FY28 dividend &gt; $1.2/share 與 FCF 同步","10Y":"dividend 政策結構化年化 $1.5","門檻":"2026 dividend $1.2+","來源":"Vale dividend history","漂移":"2026 dividend &lt; $1.0/share → 削弱（payout cut signal）"}},{"id":"H3","text":"Brumadinho 費用 2027 後 normalize 至 &lt; $0.3B/yr","columns":{"2Y":"FY26 持續 ~$0.7B / FY27 &lt; $0.5B","5Y":"FY28+ &lt; $0.3B","10Y":"2030+ 零增量","門檻":"$0.7B 2026 → $0.3B 2028","來源":"Vale 6-K filings","漂移":"FY27 仍 &gt; $0.7B → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"中國鋼鐵需求結構性負成長 + Carajas 高品位溢價收斂（Simandou ramp 完成 + ESG demand 不如預期）","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"(1) 中國 crude steel production YoY；(2) Vale Carajas 高品位 vs 62% Fe 基準 premium 月均；(3) Simandou 出貨量年度","警戒閾值":"中國鋼產 -8% YoY 連 2 年 + Carajas premium &lt; +$5/t 連 4 季 → R1 觸發；Vale 鐵礦 EBITDA -30% → 立即減倉"}},{"id":"R2","text":"Lula 政府 mining royalty 加碼 / corporate tax 加碼 / 工會權利強化三重壓制","columns":{"對應假設":"H2, H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"(1) 巴西 Senate / Câmara royalty 法案進度；(2) Lula 政府重要政策聲明；(3) 2026-10 巴西總統大選候選人 polls","警戒閾值":"Royalty +5pp 或 tax +5pp 落地 → R2 觸發；2026-10 大選 Lula 繼承人勝選 → R2 加重"}},{"id":"R3","text":"Brumadinho 持續費用 + 新 dam 事件 + 監管加碼","columns":{"對應假設":"H2, H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"(1) Vale 季度 Brumadinho 公告；(2) Vale dam safety reports；(3) 巴西 CVM 調查狀態","警戒閾值":"2026 全年費用 &gt; $1.0B 或新增 dam 事件 → R3 觸發；新 dam 事件 → 立即評估清倉（風險質變不可逆）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":16.48,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
