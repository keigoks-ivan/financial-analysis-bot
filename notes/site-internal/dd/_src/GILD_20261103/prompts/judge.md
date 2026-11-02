你是 stock-analyst **v20 判斷 agent**，標的 GILD（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GILD","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GILD_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GILD_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"總營收（GAAP）","value":8300,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results"}},{"id":"f_kpi1","label":"產品銷售","value":8289,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results"}},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益","value":4168,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results"}},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":3462,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results"}},{"id":"f_kpi6_fy2026","label":"FY2026 指引：產品銷售","value":"31,000–31,300","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results"}},{"id":"f_kpi7_fy2026_non_gaap_eps","label":"FY2026 指引：Non-GAAP EPS","value":"-1.20 – -0.85","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results"}},{"id":"f_kpi8_fy2026_gaap_eps","label":"FY2026 指引：GAAP EPS","value":"-4.40 – -4.05","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_gild_gross_margin_pct","label":"GILD 毛利率","value":79.51,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GILD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gild_operating_margin_pct","label":"GILD 營業利益率","value":36.23,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GILD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gild_fcf_margin_pct","label":"GILD FCF 利潤率","value":39.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GILD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amgn_gross_margin_pct","label":"AMGN 毛利率","value":69.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMGN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amgn_operating_margin_pct","label":"AMGN 營業利益率","value":29.99,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMGN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amgn_fcf_margin_pct","label":"AMGN FCF 利潤率","value":26.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMGN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bmy_gross_margin_pct","label":"BMY 毛利率","value":69.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bmy_operating_margin_pct","label":"BMY 營業利益率","value":29.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bmy_fcf_margin_pct","label":"BMY FCF 利潤率","value":18.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_vrtx_gross_margin_pct","label":"VRTX 毛利率","value":86.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRTX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vrtx_operating_margin_pct","label":"VRTX 營業利益率","value":37.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRTX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vrtx_fcf_margin_pct","label":"VRTX FCF 利潤率","value":30.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRTX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mrk_gross_margin_pct","label":"MRK 毛利率","value":71.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrk_operating_margin_pct","label":"MRK 營業利益率","value":0.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrk_fcf_margin_pct","label":"MRK FCF 利潤率","value":18.72,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_ocf_5_035_capex_237","label":"自由現金流（OCF 5,035 − capex 237）","value":4798,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results"}},{"id":"f_kpi5_non_gaap_eps","label":"Non-GAAP 稀釋 EPS","value":2.55,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":169.44,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":29.26,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":71.63,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-0.45 → -0.45）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.91 → 9.91）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.73 → 10.73）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":-0.45,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.91,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":10.73,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-40.0,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS -0.75 → -0.45（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.78,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":7.37,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.918,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":18279.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 26231.0、現金 7952.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1240.34,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":228435.77,"period":"2026-11-03","unit":"USD m","basis":"市值 210156.77 ＋ 淨負債 18279.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":31289.15,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":33549.67,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.3,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 170.18 / W52 136.21 / W104 119.56 / W250 88.6 / W250 13週斜率 1.9%"},{"id":"f_ma_w52","label":"52 週均線","value":136.21,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":119.56,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":88.6,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.9,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：HIV 銷售可能因競爭產品（含學名藥）搶占份額而無法維持；學名藥進入已導致且未來可能導致份額與價格侵蝕","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm","excerpt":"We may be unable to sustain or increase sales of our HIV products for any number of reasons, including market share gains by competitive products, including generics, or the inability to introduce new HIV medications necessary to remain competitive.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Gilead PrEP 銷售 2026Q2 年增逾一倍至 10.3 億美元，Yeztugo 領先整個 PrEP 轉換市場；Apretude 為主要長效競品","source":"Fierce Pharma","url":"https://www.fiercepharma.com/pharma/gilead-hiv-prep-franchise-hits-1b-quarterly-sales-analyst-questions-yeztugo-durability","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Merck 雙藥療法 Idvynso 2026-04 獲 FDA 核准，但不適用初治患者；ViiV Dovato 對 Biktarvy 影響被分析師評為微小","source":"BioPharma Dive","url":"https://www.biopharmadive.com/news/gsks-hiv-two-drug-strategy-challenges-gilead/569852/","excerpt":"Dovato, which launched last April, brought in roughly $30 million for GSK by the end of September. Another two-drug GSK pill, Juluca, fetched around $335 million across the first nine months of the year. Yet Biktarvy sales were almost 10 times higher, coming in at $3.2 billion over the same period. RBC analysts argue that Dovato's impact on Biktarvy prescriptions has been \"negligible,\" and","as_of":"2020-01-06","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2024 10-K：三大批發商占美國產品銷售約91%、全球營收約65%（客戶集中度背景，非 second-source 證據）","source":"Gilead FY2024 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209525000006/gild-20241231.htm","excerpt":"During the year ended December 31, 2024, approximately 91% of our product sales in the U.S. and approximately 65% of our total worldwide revenues were from three large wholesalers: Cardinal Health, Inc., Cencora, Inc.","as_of":"2025-02-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 三大批發商占 Gilead 總毛產品銷售：Cardinal Health 29%、McKesson 24%、Cencora 21%（合計 74%）；2024 為 29/23/21，2023 為 28/24/22。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm","excerpt":"Cardinal Health, Inc. (“Cardinal Health”) 29 % 29 % 28 % Cencora, Inc. (“Cencora”) 21 % 21 % 22 % McKesson Corporation (“McKesson”) 24 % 23 % 24 %","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未發現 Cardinal、McKesson、Cencora 在 2026 年有信用評等調降；唯一的信用調降結果為舊的 Fitch 對 Cardinal 事件（日期不明，非 2026）。","source":"WebSearch 結果摘要（medtechdive 等）","url":null,"excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q1 2026：Gilead 上調2026 HIV 成長預期至9-10%（原8%），Q1 HIV 銷售$5.0B +10%，Biktarvy $3.4B +7%、美國份額>52%","source":"Yahoo Finance, Gilead Q1 2026 earnings call summary / GILD Q126 prepared remarks","url":"https://finance.yahoo.com/sectors/healthcare/articles/gilead-sciences-q1-earnings-call-021329822.html","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Yeztugo 2026 預期自$800M 上調至$1B；Q2 銷售$232M（季增40%），維持全年約$1B；年注射版PURPOSE-365 預計2028上市","source":"Fierce Pharma / GuruFocus Q2 2026 earnings call highlights","url":"https://www.fiercepharma.com/pharma/gilead-cranks-yeztugo-first-year-sales-forecast-1b-unprecedented-launch-trajectory","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"分析師對Yeztugo持久性有疑慮：Fierce Pharma 報導 Leerink 指「several uncertain Yeztugo signals」，PrEP 產品線共識預測自$7.7B降至$6.7B","source":"Fierce Pharma: Gilead's HIV PrEP franchise hits $1B quarterly sales, but analysts question Yeztugo durability","url":"https://www.fiercepharma.com/pharma/gilead-hiv-prep-franchise-hits-1b-quarterly-sales-analyst-questions-yeztugo-durability","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Biktarvy 專利到期：原估2033年12月，與學名藥商和解後指向2036-04-01（含標準加速條款）；2026指引含政府藥價協議之價格壓力","source":"Pharmaceutical Technology / Zacks summaries of Gilead Q1 2026","url":"https://www.pharmaceutical-technology.com/news/gilead-expects-6-of-hiv-sales-growth-in-2026-with-800m-yeztugo-target/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["moat_trend","triggers"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Gilead 規劃至2030年美國製造與研發投資$32B；2026-08-27 Foster City 生物製劑新廠動土","source":"Gilead company statement: breaks ground on new biologics facility","url":"https://www.gilead.com/company/company-statements/2026/gilead-breaks-ground-on-new-biologics-facility-as-part-of-32-billion-us-rd-and-manufacturing-investment","excerpt":null,"as_of":"2026-08-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-Q（2026Q3）揭露：政府價格計算方法可能被主管機關挑戰，若不同意可能須重編數據並承擔額外法律與財務責任","source":"SEC EDGAR 10-Q 季度報告（截至 2026-09-30）","url":"https://www.sec.gov/Archives/edgar/data/0000882095/000088209526000039/gild-20260930.htm","excerpt":"Our methodologies for calculations are inherently subject to assumptions and may be subject to review and challenge by various government agencies, which may disagree with our interpretation. If the government disagrees with our reported calculations, we may need to restate previously reported data and could be subject to additional financial and legal liability.","as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-Q 提及病人援助／共付額援助計畫受到加強審查","source":"SEC EDGAR 10-Q 季度報告（截至 2026-09-30）","url":"https://www.sec.gov/Archives/edgar/data/0000882095/000088209526000039/gild-20260930.htm","excerpt":"There also continues to be enhanced scrutiny of company-sponsored patient assistance programs, including co-pay assistance programs and manufacturer donations to third-party charities that provide such assistance.","as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"搜尋未見 2026 年 DOJ／FTC／歐盟對 Gilead 的政府反壟斷調查；HIV 藥品反壟斷（pay-for-delay）為私人訴訟，Aetna 案 Gilead 未能阻止其在州法院繼續進行","source":"Life Sciences IP Preview：Gilead loses bid to quash parallel antitrust HIV lawsuit","url":"https://www.lifesciencesipreview.com/big-pharma/gilead-loses-bid-to-quash-parallel-antitrust-hiv-lawsuit-4755","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"BIOSECURE Act 等中國相關立法可能限制供應商與對華授權交易","source":"SEC EDGAR 10-Q 季度報告（截至 2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0000882095/000088209526000031/gild-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"FY2025 10-K：2025年12月Gilead與政府達成協議，Section 232關稅對Gilead暫停三年，並含Medicaid MFN定價、Epclusa直接對患者價、海外營收回饋美國。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm","excerpt":"In December 2025, Gilead reached an agreement with the administration to (1) pause the imposition of Section 232 tariffs on Gilead for three years, (2) implement MFN prices in Medicaid for select existing and future launched products, (3) set a new direct-to-patient price for Epclusa and (4) return a portion of increased international revenues to the U.S. if the U.S. government is successful in increasing drug prices abroad.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：2025年9月政府宣布對進口品牌/專利藥課最高100%關稅（有例外），具體影響不確定；可能增加製造成本、影響供應鏈。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm","excerpt":"in September 2025, the U.S. Presidential administration announced plans to impose up to 100% tariffs on imported branded or patented pharmaceuticals, subject to certain exceptions. The specific impact remains uncertain at this time and is subject to the timing, scope and duration of any tariffs and actions imposed","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K：Gilead計畫至2030年在美國投資320億美元擴充製造與研發，面臨建廠延遲、成本膨脹等風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm","excerpt":"We are undertaking significant multi‑year capital investments to expand our U.S. manufacturing capabilities and accelerate R&D, including our initiative to invest $32 billion in the U.S. through 2030.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026年9月10-Q稱關稅長期影響不確定，且即使目前符合豁免也不保證未來不適用；提及2026年7月生效的全球Section 301關稅。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0000882095/000088209526000039/gild-20260930.htm","excerpt":"and trade actions both within and outside the pharmaceutical industry, including the global Section 301 tariffs that took effect in July 2026 as well as potential tariffs from other ongoing investigations. Even if it is determined that Gilead currently qualifies for an exemption, there can be no assurance that these or other tariffs will not apply to us in the future.","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026年6月10-Q指出相當比例原料與中間體來自美國以外供應商，地緣、貿易及BIOSECURE Act變動可能影響業績","source":"Gilead 10-Q (period ended 2026-06-30), via search summary","url":"https://www.sec.gov/Archives/edgar/data/0000882095/000088209526000031/gild-20260630.htm","excerpt":"any geopolitical or economic factors in a specific country or region, including any new, or changes in or interpretations of existing law, trade regulations, or compliance requirements (such as the recently enacted BIOSECURE Act)","as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026年9月10-Q載明部分產品與物料僅單一供應商或單一設施，難以快速替換","source":"Gilead 10-Q (period ended 2026-09-30), via search summary","url":"https://www.sec.gov/Archives/edgar/data/0000882095/000088209526000039/gild-20260930.htm","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"管理層稱絕大部分製造基地在美國；2025年12月與政府協議，品牌藥及相關原料三年內免Section 232關稅，條件為追加美國製造投資；2026年4月公告對專利藥課100%關稅","source":"Gilead 10-Q FY2026 / May 2026 earnings call, via search summary","url":"https://www.sec.gov/Archives/edgar/data/0000882095/000088209526000039/gild-20260930.htm","excerpt":"the vast majority of our manufacturing base is here","as_of":"2026-05-28","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2021 10-K：多數產品（含HIV、HCV）使用多家第三方合約製造商以保有主要與備援供應商；供應商須列於NDA/MAA，認證新供應商可能造成顯著延誤","source":"Gilead 10-K FY2021","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209522000007/gild-20211231.htm","excerpt":"Suppliers of key components must be named in the NDA or MAA, and qualifying a new supplier can cause significant delays.","as_of":"2022-02-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024年報列中國、俄羅斯、烏克蘭、以色列政治不穩為風險，且研發與製造設施位於加州（地震與野火區）","source":"Gilead Form ARS FY2024","url":"https://www.sec.gov/Archives/edgar/data/882095/000130817925000254/gild013520-ars.pdf","excerpt":null,"as_of":"2025-04-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 HIV 銷售 +18% 至 $62 億（高均價、HIV 預防需求、庫存有利）；Biktarvy $41 億 +10%；Descovy $10 億 +49%；總產品銷售 +13% 至 $83 億","source":"Gilead Q3 2026 earnings press release / Reuters","url":"https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"肝病組合 Q3 +13% 至 $9.27 億，主因 Livdelzi 需求；Trodelvy Q3 +42% 至 $5.06 億（需求），預期 2026 下半年 1L mTNBC 上市","source":"Reuters 2026-10-29 / Gilead 10-Q","url":"https://kfgo.com/2026/10/29/gilead-hikes-full-year-sales-outlook-quarterly-hiv-sales-rise-18/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 產品銷售指引上調至 $310–313 億（原 $301–304 億）","source":"Reuters 2026-10-29","url":"https://kfgo.com/2026/10/29/gilead-hikes-full-year-sales-outlook-quarterly-hiv-sales-rise-18/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Biktarvy Medicare 談判價（30 天 $2,600）自 2028-01-01 生效，CFO 稱將使 2028 Biktarvy 銷售減少約 $15 億","source":"Reuters 2026-10-29 / Gilead 10-Q","url":"https://kfgo.com/2026/10/29/gilead-hikes-full-year-sales-outlook-quarterly-hiv-sales-rise-18/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Yeztugo 上市後 Q1 2026 銷售 $1.66 億（Q4 2025 $9,600 萬）；2026 指引由 $8 億上調至 $10 億；多數病人轉自其他長效針、Descovy 或學名藥口服；Descovy 美國 PrEP 市佔 >45%","source":"Fierce Pharma / Reuters via search summary / Gilead proxy","url":"https://www.fiercepharma.com/pharma/despite-tempered-sales-outlook-gilead-positions-yeztugo-dominate-hiv-prep-market-sales-surge","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 press release 含分產品銷售與 Yeztugo 數字","source":"Gilead Q3 2026 press release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000882095/000088209526000037/exhibit991earningspressrel.htm","excerpt":"AMBISOME®, ATRIPLA®, BIXLENVO™, BIKTARVY®, CAYSTON®, COMPLERA®, DESCOVY®, DESCOVY FOR PREP®, EMTRIVA®, EPCLUSA®, EVIPLERA®, GENVOYA®, HARVONI®, HEPCLUDEX®, JYSELECA®, LIVDELZI®/LYVDELZI®, LETAIRIS®, ODEFSEY®, SOVALDI®, STRIBILD®, SUNLENCA®, TECARTUS®, TRODELVY®, TRUVADA®, TRUVADA FOR PREP®, TYBOST®, VEKLURY®, VEMLIDY®, VIREAD®, VOSEVI®, YESCARTA®, YEZTUGO®/YEYTUO® and ZYDELIG®.","as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 風險因子：藥品開發本質高風險，許多候選產品於開發過程失敗；未提供具名替代技術取代現有產品之陳述。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm","excerpt":"Drug development is inherently risky, and many product candidates and investigational therapies fail during the development process.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Merck 每月一次口服 PrEP（MK-8527/alimatravir）兩項療效試驗招募中，預估 2027 完成；與 Gilead 長效 lenacapavir PrEP 競爭；Gilead 亦已送件週服口服 lenacapavir PrEP。","source":"SFAF / TAG PrEP pipeline 2026","url":"https://www.sfaf.org/2026/01/16/as-2026-gets-underway-whats-in-the-pipeline-for-hiv-prevention-and-treatment/","excerpt":null,"as_of":"2026-01-16","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"in vivo CAR-T 被描述為 2026 骨髓瘤新興趨勢，免除 T 細胞採集、製造延遲與淋巴清除化療；對 ex vivo CAR-T（如 Yescarta）構成潛在競爭壓力。","source":"OncologyTube: Belantamab comeback, myeloma trends 2026","url":"https://oncologytube.com/belantamab-comeback-myeloma-trends-2026-dr-krishnan/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025：美國多數產品仍專走批發通路，歷來約90%美國毛銷售來自三大批發商及其特殊藥局關聯公司，未見通路結構轉變的敘述。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm","excerpt":"We sell and distribute most of our products in the U.S. exclusively through the wholesale channel. Historically, approximately 90% of our gross product sales in the U.S. have been to three large wholesalers—Cardinal Health, Inc., Cencora, Inc. and McKesson Corporation—and their specialty distributor affiliates.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Gilead 2025年12月與美國政府的藥價協議：Epclusa 經 TrumpRx.gov 連結 Gilead 直接面向病患（Direct-to-Patient）計畫，以折扣現金價供應；承諾新藥定價與主要已開發國家平價，換取三年 Section 232 關稅豁免。（搜尋摘要轉述，未讀到原文頁面）","source":"NPR, White House announces new round of drug-price deals","url":"https://www.npr.org/sections/shots-health-news/2025/12/19/nx-s1-5649920/trump-drug-prices","excerpt":null,"as_of":"2025-12-19","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Gilead Q1 2026 prepared remarks 提及通路組合對平均實現價格的影響","source":"Gilead Q1 2026 Summary of Prepared Remarks","url":"https://s29.q4cdn.com/585078350/files/doc_financials/2026/q1/GILD-Q126-Summary-of-Prepared-Remarks-7-May-2026.pdf","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Gilead 於 2026-10-29 公布 Q3 時將全年 2026 產品銷售指引由 $30.1–30.4B 上調至 $31.0–31.3B；Q3 非 GAAP EPS $2.55 vs 分析師預期約 $2.17（搜尋摘要轉述，未讀原頁）","source":"Gilead Sciences announces third quarter 2026 financial results (gilead.com)","url":"https://www.gilead.com/news/news-details/2026/gilead-sciences-announces-third-quarter-2026-financial-results","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-08-04 MarketBeat：FY2026 營收指引 $30.1–30.4B，低於當時共識 $30.5B（此指引後於 10-29 上調）","source":"MarketBeat: Gilead Sciences issues FY 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/gilead-sciences-nasdaqgild-issues-fy-2026-earnings-guidance-2026-08-04/","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 共識評等 Moderate Buy、共識目標價 $157.93（as-of 約 2026-04-04，已過時）","source":"MarketBeat: Gilead given consensus rating of Moderate Buy","url":"https://www.marketbeat.com/instant-alerts/gilead-sciences-inc-nasdaqgild-given-consensus-rating-of-moderate-buy-by-analysts-2026-04-04/","excerpt":null,"as_of":"2026-04-04","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"TickerLeague（無日期，Q2 財報前快照）：目標價共識 $159.28（4 位分析師），區間 $120–$180，評等共識 Buy；Morgan Stanley 2026-07-08 維持 Overweight","source":"tickerleague.com GILD estimates","url":"https://tickerleague.com/companies/GILD/estimates","excerpt":null,"as_of":"2026-07-08","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Gilead 於 2026-02-22 與 Arcellx 簽訂併購協議（現金 $115/股加 CVR），2026-04-28 完成收購。","source":"SEC EDGAR 8-K（2026-04-28）Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/882095/000110465926049874/tm2612748d1_8k.htm","excerpt":"In accordance with the terms of the Merger Agreement, on April 28, 2026, Gilead completed the acquisition of the Company.","as_of":"2026-04-28","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"HIV 反壟斷集體訴訟（2019/2020 起）與 Viread/Truvada 等產品責任訴訟（約 23,000 名現行原告）仍在進行；聯邦首場 bellwether 審判排定 2027 年 3 月，Missouri 集體認證 2026-01 被駁回。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm","excerpt":"The federal court set a trial date of March 2027 for the first bellwether trial of the remaining cases. In the putative class action pending in Missouri, the district court issued an order in January 2026 denying, among other things, plaintiffs’ motion for class certification.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"2026 年多項 FDA 核准：Hepcludex（HDV，2026-05-22 加速核准）、Trutakna（atacicept，IgAN，2026-07-07）等；BIC/LEN 單錠 HIV 複方獲優先審查，決策結果搜尋未證實。","source":"Yahoo Finance：Gilead Wins FDA Approval for First HDV Treatment Hepcludex／搜尋摘要","url":"https://finance.yahoo.com/sectors/healthcare/articles/gilead-gild-wins-fda-approval-060454532.html","excerpt":null,"as_of":"2026-05-22","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2025-06 FDA 對 GS-1720/GS-4182 HIV 試驗下臨床暫停；其後多家律所發布投資人調查通告（非已提起之訴訟）。","source":"Pomerantz Law Firm 投資人通告（accessnewswire）","url":"https://www.accessnewswire.com/newsroom/en/business-and-professional-services/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-1042751","excerpt":null,"as_of":"2025-07-12","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Gilead 於 2026-02-22 簽訂以 $115/股現金加 CVR 收購 Arcellx 的協議，2026-04-28 完成。","source":"SEC EDGAR 8-K（2026-04-28）Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/882095/000110465926049874/tm2612748d1_8k.htm","excerpt":"In accordance with the terms of the Merger Agreement, on April 28, 2026, Gilead completed the acquisition of the Company.","as_of":"2026-04-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"HIV 藥品反壟斷集體訴訟與產品責任訴訟（約 23,000 名原告）持續；2027-03 首場 bellwether。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm","excerpt":"The federal court set a trial date of March 2027 for the first bellwether trial of the remaining cases.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"2026 年 Hepcludex（2026-05-22）、Trutakna（2026-07-07）等獲 FDA 核准；BIC/LEN 獲優先審查。","source":"Yahoo Finance／Gilead Q2 2026 財報新聞稿摘要","url":"https://finance.yahoo.com/sectors/healthcare/articles/gilead-gild-wins-fda-approval-060454532.html","excerpt":null,"as_of":"2026-05-22","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GILD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.51,"operating_margin_pct":36.23,"fcf_margin_pct":39.59,"rd_intensity_pct":20.8},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GILD","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"AMGN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":69.52,"operating_margin_pct":29.99,"fcf_margin_pct":26.71,"rd_intensity_pct":20.03},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMGN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"BMY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":69.24,"operating_margin_pct":29.19,"fcf_margin_pct":18.56,"rd_intensity_pct":21.1},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"VRTX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":86.0,"operating_margin_pct":37.95,"fcf_margin_pct":30.16,"rd_intensity_pct":32.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRTX","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MRK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.31,"operating_margin_pct":0.87,"fcf_margin_pct":18.72,"rd_intensity_pct":53.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"GILD"},"financial_history":{"ticker":"GILD","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":27281000000.0,"revenue_yoy_pct":null,"gross_margin_pct":79.26,"operating_margin_pct":40.23,"net_income":4592000000.0,"diluted_eps":3.64,"free_cash_flow":8344000000.0,"fcf_margin_pct":30.59,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":27116000000.0,"revenue_yoy_pct":-0.6,"gross_margin_pct":76.04,"operating_margin_pct":32.59,"net_income":5665000000.0,"diluted_eps":4.5,"free_cash_flow":7421000000.0,"fcf_margin_pct":27.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":28754000000.0,"revenue_yoy_pct":6.04,"gross_margin_pct":78.26,"operating_margin_pct":36.85,"net_income":480000000.0,"diluted_eps":0.38,"free_cash_flow":10305000000.0,"fcf_margin_pct":35.84,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":29442000000.0,"revenue_yoy_pct":2.39,"gross_margin_pct":78.83,"operating_margin_pct":39.74,"net_income":8510000000.0,"diluted_eps":6.78,"free_cash_flow":9456000000.0,"fcf_margin_pct":32.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GILD/GILD_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Gilead Sciences, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good afternoon, everyone, and welcome to Gilead's Third Quarter 2026 Earnings Conference Call. My name is Rebekah, and I'll be today's host. In a moment, we'll begin our prepared remarks, followed by our Q&A session. [Operator Instructions] 
Now I'll hand the call over to Jacquie Ross, Senior Vice President, Treasurer and Head of Investor Relations.

**Jacquie Ross** (Executives):
Thank you, Rebekah. Just after market closed today, we issued a press release with earnings results for the third quarter of 2026. The press release, slides and supplementary data are available on the Investors section of our website at gilead.com. 
The speakers on today's call will be our Chairman and Chief Executive Officer, Daniel O'Day; our Chief Commercial and Corporate Affairs Officer, Johanna Mercier; our Chief Medical Officer, Dietmar Berger; and our Chief Financial Officer, Andrew Dickinson. After that, we'll open the call to Q&A where the team will be joined by Cindy Perettie, the Executive Vice President of Kite. 
Let me remind you that we will be making forward-looking statements. Please refer to Slide 2 regarding the risks and uncertainties relating to forward-looking statements that could cause actual results to differ materially. 
With that, I'll turn the call over to Dan.

**Daniel O'Day** (Executives):
Thank you, Jacquie, and thanks, everyone, for joining us on today's call. 
Gilead delivered an exceptional third quarter that highlights the strength, breadth and durability of the business. Third quarter base business sales were up 16% year-over-year, Gilead's strongest growth in more than a decade, driven by Biktarvy, Descovy and Yeztugo in HIV, Trodelvy in metastatic breast cancer, and Livdelzi in PBC. At the same time, we continue to advance our diverse pipeline as we prepare for the next phase of launches. 
In HIV, we continue to lead across treatment and prevention. In the third quarter, HIV sales grew 18% year-over-year. Biktarvy achieved an all-time high U.S. market share, and we had a modest initial contribution from Bixlenvo, which launched in August. HIV Prevention sales nearly doubled year-over-year. As expected, Yeztugo has rapidly established itself as the leading long-acting injectable option for HIV prevention. Yeztugo and Descovy for PrEP combined have 50% market share today and a $4 billion annual run rate. 
As Dietmar will cover later, we believe we have the most comprehensive and diverse HIV pipeline in the industry as well as in Gilead's history. Across daily and long-acting dosing, we are advancing a portfolio that will deliver new options for many years to come. The most near-term example is islatravir plus lenacapavir. We expect to file this year, and, if approved, this would be the first once-weekly oral treatment regimen for virally suppressed people with HIV. 
In Oncology, Trodelvy delivered another very strong quarter. Sales were up 42% year-over-year, and with growing demand across triple-negative and HR-positive/HER2-negative metastatic breast cancer, Trodelvy reached an approximately $2 billion annual run rate. In the third quarter, we received European approval of Trodelvy in combination with pembro for first-line PD-L1-positive metastatic triple-negative breast cancer, extending Trodelvy's benefits to patients earlier in treatment. Beyond Trodelvy in metastatic breast cancer, we now have 7 clinical-stage antibody-drug conjugate programs in oncology. 
In Cell Therapy, we are approaching an important catalyst with the potential approval of anito-cel toward the end of the year. This would bring our total number of approvals to 4 in 2026 alone. 
In Inflammation, our third strategic area of focus, we are advancing and expanding our broad and differentiated pipeline that we believe will establish a durable new growth area for the company. We recently shared promising 12-week data for emvistegrast in inflammatory bowel disease, and we expect to advance the program into Phase 3 studies in ulcerative colitis in 2027. Emvistegrast has the potential to be a backbone therapy for inflammatory bowel diseases, as a monotherapy or in combination with other mechanisms, including the oral IL-23 receptor inhibitor we recently agreed to acquire. 
Beyond IBD, we have our IRAK4 inhibitor for which we plan to share data at the upcoming ACR meeting, as well as gamgertamig, which represents a promising approach to B-cell-driven autoimmune diseases with additional data expected later this year. 
Overall, our inflammation pipeline now includes 13 clinical programs, giving us multiple opportunities to deliver meaningful advances for patients. 
In summary, the third quarter continues what is proving to be a stellar year of execution and performance. This has enabled us to raise our 2026 base business revenue guidance by $1.6 billion over the course of the year, while advancing our robust pipeline and preparing for the next wave of potential launches. 
This fundamental strength in our business means we are well placed to adapt to potential policy headwinds. As you know, Biktarvy was selected for the Maximum Fair Price determination process. That process is now complete, and CMS have informed us of the price they have set. As we have previously shared, this will have an impact on Biktarvy revenues in 2028. Andy will share details in his section of the call. 
And as the third quarter has reinforced again, our strategy of diversification has reshaped our business and is expected to continue to drive sustainable growth. 
Looking forward, the multiple opportunities to drive growth across all 3 of our therapeutic areas, the strength and diversity of our pipeline within and beyond HIV, and a disciplined operating model all give us confidence in the trajectory of the company. 
With that, I'll hand it over to Johanna.

**Johanna Mercier** (Executives):
Thanks, Dan, and good afternoon, everyone. Starting on Slide 7. Total product sales, excluding Veklury, of $8.2 billion, were up 16% year-over-year driven by strong HIV performance, Trodelvy and Livdelzi. This is the highest year-over-year growth for our base business since 2015. Sequentially, sales were up 8%, driven by growth in HIV, Trodelvy and Livdelzi. Including Veklury, third quarter total product sales were $8.3 billion, up 13% year-over-year and 9% sequentially. 
Moving to HIV on Slide 8. Third quarter HIV sales of $6.2 billion were up nearly $1 billion or 18% year-over-year and represented the highest year-over-year growth since the fourth quarter of 2018. This strong performance was driven by higher average realized price, higher demand and favorable inventory dynamics. Sequentially, HIV sales were up 10%, primarily driven by higher inventory, demand and average realized price. We expect these inventory dynamics to normalize by year-end. 
Looking at HIV treatment in more detail on Slide 9. Biktarvy sales of $4.1 billion were up 10% year-over-year, driven by higher demand and average realized price, in addition to favorable inventory dynamics. Sequentially, Biktarvy sales increased 8%, driven by favorable inventory dynamics and higher demand, partially offset by lower average realized price due to channel mix. 
Biktarvy reached an all-time high treatment market share of 53% in the U.S., supported by continued gains among new patients, strong retention, and improving access following adjustments to the Florida ADAP program earlier in the year. While we have not yet seen the HIV treatment market return to its typical 2% to 3% growth, we have seen signs of stabilization. Biktarvy has also demonstrated continued resilience amid changes related to the Affordable Care Act, reflecting the strength of the product profile and of our commercial teams to help people living with HIV maintain access to treatment. 
Bixlenvo, our new daily oral combination of bictegravir and lenacapavir for virally suppressed adults with HIV, was launched late into the third quarter following U.S. approval in August. While it's still early days for the launch, we're pleased with the uptake we are seeing in virally suppressed people on complex regimens, which has been in-line with our expectations. Overall, we remain focused on expanding coverage and bringing this new option for people who want to switch or simplify their HIV treatment. 
Moving to HIV prevention or PrEP on Slide 10. Sales nearly doubled year-over-year in the third quarter, once again outpacing overall U.S. market growth of 14% year-over-year. This is a clear testament to Gilead's strong commercial execution. Building on our leadership, now with 50% PrEP market share, our innovative portfolio has accounted for the vast majority of market growth since 2025. 
Additionally, demand in the long-acting injectable market doubled year-over-year, and we're pleased to share Yeztugo is now the leading injectable prevention regimen, with sales of $305 million, up 31% sequentially, and on track to deliver full year sales of approximately $1 billion. 
Importantly, we continue to see that more than 70% of users have returned for their second injection, resulting in combined protection of up to a full year. This continues to reinforce Yeztugo's best-in-PrEP persistency profile, as defined by patients returning for their reinjections after 6 months. We are particularly encouraged by the mix of new starts, with the majority continuing to come from individuals switching from other PrEP regimens, while the share of PrEP-naive individuals increased during the quarter. Looking ahead, we believe the potential launch of once-weekly oral Yeztugo could further expand choice and support continued growth by reaching additional individuals who could benefit from PrEP. 
Looking at Descovy, total sales of $1 billion were up 49% year-over-year, driven by higher average realized price and favorable inventory dynamics. PrEP sales continue to account for approximately 80% of total Descovy sales. Sequentially, total Descovy sales were up 8%, driven by higher-than-usual inventory build and higher demand. In just 3 quarters, Descovy's sales have already exceeded that of full year 2025, driven primarily by strong demand and pricing favorability. 
Moving to Livdelzi on Slide 11. Sales of $203 million were up 93% year-over-year and 21% sequentially driven by increased demand, in both the U.S. and Europe. Livdelzi is the market leader in the U.S., and is helping to drive expansion of the second-line PBC market. 
Looking ahead, we're excited to share the detailed results from Livdelzi's Phase 3 IDEAL study at the upcoming AASLD Liver Meeting. The study evaluated Livdelzi in PBC patients with ALP between 1 and 1.67x the upper limit of normal, which account for approximately half of the second-line eligible population and remain associated with an increased risk of disease progression. We are working towards global filings to update Livdelzi's label to include data from the IDEAL study and expect a U.S. label update in 2027. 
Together with sales in our viral hepatitis portfolio, Liver Disease sales were $927 million, up 13% year-over-year, reflecting increased demand for Livdelzi in PBC, as well as favorable pricing dynamics for HCV and HBV, partially offset by lower HCV starts. Sequentially, sales were up 6%, reflecting higher average realized price and inventory dynamics, partially offset by lower demand for HCV products. 
Moving to Slide 12. Trodelvy sales of $506 million for the quarter, now a $2 billion annual run-rate, was up 42% year-over-year and 11% sequentially, driven by strong demand growth in both metastatic triple-negative and HR-positive/HER2-negative breast cancer across the U.S. and Europe. 
Following the first-line approvals in the U.S. and Europe earlier this year, Trodelvy is establishing itself as the backbone of treatment in metastatic triple-negative breast cancer, and we're working to expand Trodelvy's first-line opportunity further into new markets. Triple-negative breast cancer remains one of the most aggressive and challenging forms of breast cancer to treat. Bringing Trodelvy into the first-line setting represents an important opportunity to reach significantly more patients earlier in their treatment journey, when the potential impact of treatment may be the greatest. We are incredibly pleased with the first-line metastatic TNBC uptake thus far. 
Moving to Slide 13. And on behalf of Cindy and the Kite team, third quarter Cell Therapy sales of $355 million were down 18% year-over-year, reflecting ongoing competitive headwinds. Looking ahead, we're also focused on the next potential chapter of growth for our Cell Therapy business. Our launch preparations are in full force as we approach anito-cel's December 23 PDUFA date in fourth line plus relapsed or refractory multiple myeloma. 
This includes: conducting preactivation efforts within our Authorized Treatment Centers network, with a target activation of 80% of our ATCs within the first 6 months of launch, detailed launch planning across sales, medical and access teams as well as engaging with a range of payers with a target of 90% payer coverage within the first 12 months of launch. 
Coupling our steadfast preparations with the level of health care provider and patient enthusiasm we have seen for anito-cel's profile ahead of launch, we are targeting brand leadership in the fourth line plus setting within 18 months of approval. 
As we head into the final months of the year, we remain focused on delivering strong performance across our portfolio and preparing for the upcoming launch of anito-cel. In HIV, we are building on our leadership in treatment and prevention through the early launch of Bixlenvo and the continued performance of Biktarvy, Yeztugo and Descovy. Beyond HIV, Livdelzi continues to gain share as the PBC market expands, while Trodelvy is delivering strong growth across triple-negative and HR-positive/HER2-negative metastatic breast cancer. Our outstanding performance this quarter once again reflects the incredible work of our teams across the organization, and I want to thank them for their unwavering commitment to patients. 
And with that, I'll hand the call over to Dietmar.

**Dietmar Berger** (Executives):
Thank you, Johanna, and good afternoon, everyone. The third quarter was another productive period across all 3 of our therapeutic areas. We received FDA approval of Bixlenvo, advanced our twice yearly HIV treatment programs and shared promising early data from our emerging inflammation portfolio, including our investigational oral alpha-4-beta-7. We're making strong progress across our diverse portfolio of 49 clinical programs. 
Beginning with HIV treatment on Slide 16,  we're advancing the most comprehensive HIV portfolio in both the industry and in Gilead's history.  While Biktarvy sets the standard for daily single-tablet regimens in people with HIV, we continue to innovate across daily and long-acting treatment options to address the diverse needs of the greater than 40 million people living with HIV globally. Building on Bixlenvo's approval, we are making progress in 6 long-acting treatment programs encompassing both orals and injectables. We expect to file islatravir plus lenacapavir with FDA this year with a regulatory decision in 2027.
If approved, IS/LEN would be the first once-weekly oral treatment regimen for virally suppressed people with HIV. Beyond IS/LEN, we remain on track to initiate our Phase II trials for our wholly owned weekly oral regimens, combining lenacapavir with our investigational long-acting integrase inhibitors. Earlier this month, we started the Phase II trial for the lenacapavir combination with GS-3242, and the Phase II trial for the combination with GS-1720 is expected to start in early 2027. We will select the most promising candidate for Phase III development in treatment-naive and virally suppressed people with HIV. The selected program will have the potential to be the first INSTI-containing weekly regimen. 
We're also advancing 2 distinct long-acting injectable treatment options. First, we initiated the newly named Phase III DAYBREAK 1 and 2 trials for lenacapavir plus our investigational broadly neutralizing antibodies, teropavimab and zinlirvimab during the third quarter. This has the potential to be our first complete twice-yearly HIV treatment regimen for the virally suppressed population with susceptibility to both bNAbs.
In parallel, we initiated the also newly named Phase II PULSAR-1 and 2 trials, evaluating injectable GS-3242 plus lenacapavir, our first INSTI-based long-acting injectable treatment program. These studies have already begun dosing our every 4-month cohort. We expect to initiate the twice-yearly dosing cohort following additional Phase I data.
Overall, we continue to believe that this portfolio across both long-acting oral and injectable treatments positions us well to expand choice, support Gilead's continued leadership, and reach more of the 44% of people with HIV who are not virally suppressed.
Turning to HIV prevention, we continue to build upon the unprecedented clinical profile demonstrated by lenacapavir in the PURPOSE studies with twice-yearly Yeztugo establishing a new benchmark for HIV prevention efficacy. Building on the successful commercial launch of twice-yearly Yeztugo, our application of once-weekly oral lenacapavir for PrEP is under review with the FDA, with a regulatory decision expected in early February 2027.  If approved, once-weekly lenacapavir could become the first long-acting oral PrEP regimen, complementing twice yearly Yeztugo for people who prefer an oral option. 
Looking further ahead, we continue to expect an update from the Phase III PURPOSE-365 study evaluating once-yearly intramuscular lenacapavir for PrEP in 2027. Aligning with annual preventative care visits, this option could be even more transformative in reaching more people who could benefit from PrEP, and we are targeting potential launch in 2028. 
Turning to oncology on Slide 17, we remain focused on advancing differentiated therapies for cancers with large unmet needs. Our acquisition of Tubulis earlier this year adds 4 promising clinical stage programs as well as next-generation ADC technology that further strengthen our existing ADC expertise.
Among our ADC programs, we look forward to providing an update from our Phase III ASCENT-GYN study around the end of the year. The study is evaluating Trodelvy in advanced or recurrent endometrial cancer, where patients whose disease progresses following prior treatment continue to have limited effective options. Beyond Trodelvy, we continue to advance GS-8824, our investigational NaPi2b directed ADC, in platinum-resistant ovarian cancer. 
The encouraging Phase I activity observed in heavily pretreated patients, without biomarker selection, reinforces our belief in its potential to offer a differentiated treatment option in this challenging disease. 
At the same time, we're exploring GS-8824's potential more broadly in our Phase I program for platinum-sensitive ovarian cancer. We have also initiated a new trial in advanced or recurrent endometrial cancer. 
Our commitment to oncology extends further into our earlier-stage pipeline, where we are advancing several programs designed to address high unmet needs in solid tumors. This includes a focused effort in MTAP-deleted cancers, which represent approximately 10% to 15% of solid tumors with GS-5319, our investigational MTA cooperative PRMT5 inhibitor, and GS-2426, our investigational MAT2A inhibitor, which targets a complementary pathway, both currently in Phase I clinical trials.
Moving to inflammation on Slide 18, we're excited to be at the stage where we are starting to share clinical data. As our third strategic area of focus, we have been building and leveraging deep expertise across immunological pathways and mechanisms to develop a pipeline of potential first-in-class or best-in-class approaches to target various severe immune-mediated inflammatory conditions with high unmet need. 
In inflammatory bowel disease, we shared promising 12-week data for emvistegrast, our investigational once-daily oral small molecule inhibitor of alpha-4-beta-7, at the United European Gastroenterology Meeting earlier this month. The data demonstrate the potential for best-in-class oral efficacy with a generally well-tolerated safety profile. We believe that emvistegrast could provide a much-needed oral treatment option for IBD patients who currently cycle through burdensome injectable therapies.
Following these results, we expect to advance emvistegrast monotherapy into Phase III studies in ulcerative colitis in 2027. In addition, we are exploring its potential as an oral backbone for combination regimens designed to break through the efficacy ceiling seen with approved monotherapies. We are also planning a Phase IIb/III study to evaluate emvistegrast in Crohn's disease. These programs will be conducted in both advanced-therapy-naive as well as advanced-therapy-experienced populations in line with FDA guidance.
In addition to these programs, we agreed to acquire an oral peptide IL-23 receptor inhibitor, which we believe adds a potentially differentiated oral approach for inflammatory bowel disease to our growing inflammation and immunology portfolio. The program, known as HCXT-2001, may potentially be used alone, or in combination with emvistegrast, as a daily oral treatment for people living with IBD. This reinforces our approach to build depth and optionality in selected immune-mediated diseases through multiple complementary mechanisms and modalities.
Beyond our inflammatory bowel disease programs, we are also excited by the early-stage portfolio of T-cell engager therapies acquired in our Ouro Medicines acquisition in partnership with Lakefront. As a reminder, gamgertamig is a potential best-in-class BCMAxCD3 bispecific T-cell engager that demonstrated robust clinical activity in early Phase I studies across autoimmune conditions. We will be presenting additional Phase I data for gamgertamig in immune thrombocytopenia at a medical congress later this year. 
Additionally, we are looking forward to sharing a detailed update from our Phase IIa COSMIC study at the upcoming American College of Rheumatology meeting on November 8. While still early, the study provides the first clinical proof-of-concept signal for edecesertib, our investigational IRAK4 inhibitor, in cutaneous lupus erythematosus. 
Further, at the upcoming AASLD meeting, we're excited to present detailed results from our Phase III IDEAL study of Livdelzi. This study evaluated patients with alkaline phosphatase between 1 and 1.67x the upper limit of normal or intolerance to ursodeoxycholic acid. Following positive top line results shared earlier this year, this presentation will provide a fuller view of the findings and their potential benefit for patients with PBC, and an opportunity to deepen our understanding of where Livdelzi can potentially address remaining treatment needs.
Overall, our inflammation pipeline now includes 13 clinical programs led by our inflammatory bowel disease and B-cell-depleting programs. We believe our portfolio gives us multiple opportunities to deliver meaningful advances for patients and establish inflammation as a potentially significant new growth area for Gilead.
Moving to cell therapy on Slide 19, and on behalf of Cindy and the Kite team, we are now less than 2 months away from anito-cel's December 23 PDUFA date and potential launch in fourth line or later relapsed or refractory multiple myeloma. The filing was supported by data from our Phase II iMMagine-1 study for which we expect to share additional follow-up data inclusive of the Kaplan-Meier curve for PFS at an upcoming medical congress this year. 
We're excited to deliver what we believe could be an important new treatment option for patients, reinforced by anito-cel's deep, durable efficacy, differentiated safety profile and targeted manufacturing turnaround time of less than 3 weeks. In addition to the fourth-line plus setting, the broad anito-cel program adds the potential to establish a new standard of care across the multiple myeloma landscape, reaching more patients earlier in treatment. 
We look forward to iMMagine-3 data in second to fourth line with a potential BLA filing as early as 2027. We are pleased to share that, we expect to initiate our iMMagine-6 and iMMagine-4 studies in transplant-eligible and non-eligible newly diagnosed patients in early 2027 and plan to share data from the GEM-AnitoFIRST safety lead-in study for newly diagnosed multiple myeloma at an upcoming medical congress later this year.
Beyond anito-cel, KITE-512,  our GPC-3-targeted, dual-armored CAR T cell therapy has been cleared for clinical studies by FDA, and we look forward to enrolling the Phase I trial in patients with advanced GPC-3-positive hepatocellular carcinoma soon. This marks an important milestone for extending the reach of the transformative potential of Kite's cell therapies into solid tumors. 
Turning to our next-gen cell therapies, PALISADES-1 and 2, evaluating KITE-753 in patients with second-line and third-line plus relapsed or refractory diffuse large B-cell lymphoma has been placed on a partial clinical hold while we investigate safety differences we have noted between Phase I and Phase II.
Lastly, we are pleased to share that in collaboration with Pregene, we have begun dosing patients with our in vivo BCMA CAR-T therapy in an investigator-initiated trial in China. Leveraging Kite's extensive cell therapy expertise and manufacturing capabilities, our in vivo program aims to address existing class challenges and unlock broader applications across oncology and autoimmune diseases. Our advancement in the clinic is an encouraging milestone, and we look forward to providing additional updates in due course.
Moving now to our milestones on Slide 20, I'd like to thank our research and development teams at Gilead and Kite for their dedication and execution across our clinical portfolio. We are on track for our remaining 2026 milestones, including the Phase III update for ASCENT-GYN, evaluating Trodelvy in advanced or recurrent endometrial cancer, and the FDA decision on anito-cel in fourth line or later relapsed or refractory multiple myeloma. 
Along with our planned acquisition of an oral IL-23 receptor inhibitor program, we entered 2 new collaborations that further strengthen our solid tumor portfolio. With BioNTech, we will evaluate Trodelvy in combination with pumitamig, an investigational PD-L1 VEGF-A bispecific, in first-line metastatic triple-negative breast cancer. And with Vir Biotechnology, we will develop 3 novel dual-masked T-cell engagers for solid tumors. Taken together, these updates reflect the strength of the portfolio we have built and the opportunities that lie ahead. 
Now I will turn over the call to Andy.

**Andrew Dickinson** (Executives):
Thank you, Dietmar, and good afternoon, everyone. Gilead's third quarter results demonstrate outstanding commercial and clinical execution, reinforced by continued operating expense discipline. 
As shown on Slide 22, our base business grew 16% year-over-year to $8.2 billion, driven by continued growth across Biktarvy, Descovy and Yeztugo in HIV; Trodelvy in metastatic breast cancer; and Livdelzi in PBC, partially offset by lower sales of cell therapy products. Sequentially, sales were up 8%, driven by higher HIV, liver disease and Trodelvy sales, partially offset by lower sales of cell therapy products. Total product sales of $8.3 billion were up 13% year-over-year, reflecting lower Veklury sales due to fewer COVID-19-related hospitalizations.
Moving to our non-GAAP third quarter results on Slide 23, product gross margin was 88% in the third quarter of 2026, up from 86% in the third quarter of 2025, primarily driven by the expiration of a TAF-related royalty obligation in November of 2025. R&D expenses were $1.6 billion, up 19% year-over-year and 11% sequentially, reflecting higher compensation accruals related to our financial outperformance year-to-date, as well as higher clinical costs.
SG&A expenses were $1.5 billion, up 14% year-over-year, primarily reflecting HIV promotional activities that supported our strong commercial performance, in addition to legal expenses and higher compensation accruals related to financial outperformance year-to-date. The operating margin was 50% in the third quarter and 49% year-to-date, excluding acquired IPR&D associated with the Arcellx, Tubulis and Ouro Medicines acquisitions, firmly in the top quartile of our peer group and underscoring the leverage in our business model resulting from our expense discipline. 
The non-GAAP effective tax rate was 19% in the third quarter, in line with our full year expectation for an effective tax rate of approximately 20%, excluding acquired IPR&D expenses related to our 2026 acquisitions. And finally, our non-GAAP diluted EPS was $2.55, primarily driven by higher product sales and lower acquired IPR&D expenses, partially offset by higher operating expenses compared to $2.47 in the same period in 2025.
Recall, as shown on Slide 24, our third quarter 2025 benefited from an approximately $400 million or $0.25 per share contribution reported in royalty, contract and other revenue related to an IP asset sale from 2018. Excluding this, non-GAAP EPS increased 15% year-over-year and compares to 13% total product sales growth.
Moving to our full year guidance on Slide 25. We are updating our full year sales and EPS guidance to reflect our outstanding third quarter results. We now expect base business sales to range between $30.7 billion and $31 billion. This represents an increase of $900 million at the midpoint compared to our August guidance and an increase of $1.65 billion at the midpoint compared to our initial 2026 guidance. 
Within HIV and reflecting our strong performance year-to-date, we now expect full year sales to grow approximately 12% year-over-year, driven by Biktarvy for HIV treatment as well as Yeztugo and Descovy for PrEP. Given larger inventory build than is typical for the third quarter, we expect the Q4 inventory build to be smaller than we have historically seen in the fourth quarter. We continue to expect Yeztugo sales of approximately $1 billion for the full year, allowing for more modest sequential growth, reflecting holiday seasonality. And we continue to expect cell therapy sales to decline mid-teens percentage year-over-year. 
Moving to total product sales. We now expect sales in the range of $31 billion to $31.3 billion, included in total product sales, we continue to expect Veklury sales of approximately $300 million for the full year, reflecting lower COVID-19-related hospitalizations. With regards to our non-GAAP P&L, we now expect acquired IPR&D of approximately $12.9 billion, reflecting the $1.4 billion in upfront payments expected in the fourth quarter associated with the acquisition of an oral IL-23R inhibitor program from PepStar Therapeutics and the recently announced Vir research collaboration.
Moving to operating expenses. We now expect full year 2026 R&D expenses to increase a mid- to high single-digit percentage on a dollar basis compared to 2025, and SG&A expenses to increase by a high single-digit percentage on a dollar basis compared to 2025, both reflecting higher costs related to the significant increase in our expected full year financial performance.
Moving to tax. We now expect full year 2026 effective tax rate to be between 220% and 165%, reflecting the nondeductible acquired IPR&D expenses associated with the Arcellx, Tubulis and Ouro Medicines transactions, as well as the expected acquired IPR&D expense associated with the PepStar Therapeutics transaction. Excluding these transactions, our effective tax rate would be 20%, no  change from our February guidance. Overall, we expect full year non-GAAP loss per share between $1.20 and $0.85. 
Turning to Slide 26. Excluding approximately $9.95 per share related to the acquired IPR&D expense and full year financing costs associated with the acquisitions this year and nonrecurring other revenue, our full year non-GAAP diluted EPS would be $8.75 to $9.10, raised $0.25 on both ends from our illustrative August guidance due to higher base sales, partially offset by higher operating expenses. 
Looking beyond 2026, I wanted to share an update on our discussions with CMS regarding Biktarvy pricing. As a reminder, Biktarvy was selected for the maximum fair price determination process that will impact Biktarvy revenue starting in 2028. CMS has informed us that it has set pricing for Biktarvy at $2,600 per 30-day supply, which represents an approximate 38% discount from the list price in the Medicare channel. Based on our preliminary analysis, we currently expect full year 2028 Biktarvy revenue to decline from 2027. More specifically, we expect a total net impact to Biktarvy revenue of approximately $1.5 billion in 2028, reflecting the lower price in Medicare, in addition to related impacts across other U.S. channels, including Medicaid, 340B and other payer segments.
Reflecting growth from other innovations across our HIV portfolio, we continue to expect total HIV revenue to grow in 2028 compared to 2027. Further, our growing HIV business is expected to be complemented by additional growth across our innovative oncology and inflammation portfolios. As a result, we expect both total product sales and earnings per share to grow in 2028 compared to 2027. Note that these statements are based on our current assumptions that may change and could be updated at any time, including when we share formal guidance in early 2028. 
Taking a step back, Gilead has demonstrated its ability to address policy impacts over the last few years, including the $1.1 billion headwind associated with Medicare Part D redesign in 2025, and the greater than $500 million headwind associated with the Affordable Care Act and other government policies in 2026. With more than a year before the new Biktarvy pricing takes effect, we will continue to work diligently to potentially mitigate some of the impact. 
Back to 2026 and on Slide 27, you can see we returned approximately $1.4 billion to shareholders in the third quarter, including $370 million of share repurchases. Combined with our dividend, we have returned approximately 40% of our free cash flow to shareholders in the first 3 quarters of 2026. 
In closing, and building on our track record of execution so far, we remain focused on a strong finish to a remarkable year for Gilead, and believe we are better positioned than ever with robust clinical and commercial pipelines and a strong business model that sets us up well in 2027, 2028 and beyond. 
And with that, I'll invite Rebekah to start our Q&A session.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Umer Raffat at Evercore.

**Umer Raffat** (Analysts):
I wanted to spend a quick second on your recently acquired oral IL-23 and the potential for combo with some of the recent data sets for the alpha-4-beta-7. And my question is, if the alpha-4-beta-7 requires dosing as fasted and the IL-23, which is presumably a cyclic peptide, requires overnight fasting and perhaps waiting another 30 minutes post the dose, practically speaking, for a patient, how would the co-administration or the combo actually work? Is there a way to be able to give them simultaneously or close enough while still being practically feasible?

**Dietmar Berger** (Executives):
Yes, Umer. Thank you for the question. This is Dietmar. I mean, first of all, let me say, we're really excited about the portfolio that we're building in inflammatory bowel disease. And there's obviously really the opportunity for various types of combinations, both internal and external. The IL-23 is very early. So we're still working on different types of formulations. So please stay tuned, and we'll inform you more about those details as we move along.

**Operator** (Operator):
Our next question comes from Akash Tewari at Jefferies.

**Akash Tewari** (Analysts):
Can you go over the moving pieces on the $1.5 billion IRA impact for Biktarvy pricing? How much of that is a net pricing impact for Medicare specifically versus the downstream impact on your, kind of, Medicaid best price and then the 340B impact. I want to make sure we just get those moving pieces right.

**Daniel O'Day** (Executives):
Yes. Thanks, Akash. This is Dan, and then I'll turn it over to my colleagues for some more detailed framing of your question. But before we do, just I wanted to elaborate a little bit on what was in my script and share my perspectives on the CMS price setting. First, I'd just like to say that the price set by CMS does not reflect the value of Biktarvy, the medicine that has transformed HIV treatment and widely recognized as a standard of care. And I think this is an example of how price-setting approach under the IRA, especially for highly differentiated medicines like Biktarvy in the middle of their life cycle can put investment in new medicines at risk.
We firmly believe there are ways to improve affordability for patients in America without damaging policies that undermine the U.S. patent system and the innovation it supports. I'd just go on to say that there are certain diseases that can only be addressed by small molecule medicines like HIV and others. And many of these diseases disproportionately impact underserved patients for which Gilead is firmly committed to supporting in so many ways. And so this pill penalty, which has now been applied to Biktarvy, discourages investment in these medicines.
So I just want to end with these 2 concepts, both can be true. As I said earlier, our business is strong. The quarter has been exceptional. The portfolio that you just saw, that Dietmar outlined, really has never been stronger at Gilead. And we've built a business for patients and communities we serve that can respond to these policy headwinds. And I just want to say we firmly oppose policies like this that undermine innovation. Relative to the $1.5 billion, we wanted to give you some color on our preliminary analysis and what we think the impact will be in 2028 to guide you. 
I'm going to turn it over to Johanna to give a little bit more detail on how that $1.5 billion breaks out and what we anticipated including in it. So over to you, Johanna.

**Johanna Mercier** (Executives):
Thanks, Dan. So again, obviously, this is a preliminary analysis and subject to change as we get closer to 2028. But we expect the $1.5 billion that Andy mentioned earlier, really, that's a net impact on Biktarvy revenues in 2028. So that is inclusive of the Medicare piece and all other spillovers to other channels in the U.S. And so to your question around, kind of, the split on that, we're not going to give all the details at this point in time as it's still very early. But having said that, it's primarily Medicare and then you have the spillover effect. It really is a net impact, and that's why we're giving you the total number. And this is also net of, of course, the Part D redesign impact that we saw for Biktarvy in 2025 that goes away in 2028. So it's -- the $1.5 billion is all encompassing.

**Operator** (Operator):
Our next question comes from Mohit Bansal at Wells Fargo.

**Mohit Bansal** (Analysts):
And I want to turn the attention to the anito-cel trial for newly diagnosed multiple myeloma, the iMMagine-6 trial. And I couldn't help but notice that it does have a co-primary endpoint of MRD negativity at 12 months. So I would love to understand your thought process behind this and what discussions you had with the FDA. And is there a possibility of early filing on the basis of 12-month MRD negativity here?

**Cindy Perettie** (Executives):
Thanks, Mohit. This is Cindy. If you look at both our iMMagine-3 trial as well as our newly diagnosed trials, they are co-primary endpoints looking at MRD followed by PFS. For the  GEM-AnitoFIRST and then I think you were referring to the iMMagine-4 and iMMagine-6 trials, those are MRD-negative CR rates. And those are discussions that we had with global regulatory agencies as we were designing the trial. I think the thing I would point out uniquely about the trials for iMMagine-4 and iMMagine-6 is they're transplant ineligible iMMagine-4 and transplant eligible for iMMagine-6, where we're looking at quad therapy upfront followed by anito-cel and maintenance. In the iMMagine-4 trial, we're also looking at MRD-guided maintenance so that patients could have treatment-free intervals.

**Operator** (Operator):
Our next question comes from Brian Abrahams at RBC.

**Brian Abrahams** (Analysts):
Congrats on the strong quarter. I really appreciate the details on the potential IRA impact in 2028. That's really helpful. Can you clarify, does your expectation to be able to grow the HIV franchise through that, does that include -- is that inclusive of PrEP? And then, I guess, I'm curious what, sort of, would need to happen in terms of overall market growth, new products and switches in order to be able to offset that $1.5 billion IRA impact to Biktarvy.

**Daniel O'Day** (Executives):
Yes. Johanna, why don't you start?

**Johanna Mercier** (Executives):
Yes. Thanks, Brian, for the question. Yes, so your question about our HIV, of course, we look at HIV holistically. We look at our portfolio across both treatment and prevention. And so that is inclusive of all of our portfolio today and, of course, the portfolio to come as we think about the very strong pipeline that's going to support the next 10 to 15 years of growth and leadership in HIV. The other piece of your question around -- sorry, the offset for the $1.5 billion. And what we've said is, obviously, we will look to -- we have about a year or so, we will look at different opportunities to mitigate as much as possible the $1.5 billion, but that's in addition to the overall portfolio and of course, other strategies that we can look at. So more to come on that one.

**Operator** (Operator):
Our next question comes from Chris Schott at JPMorgan.

**Christopher Schott** (Analysts):
I just want to dig into the weekly oral PrEP launch as we head into next year. I guess, can you just help frame out what portion of the market you think this could appeal to? And maybe just compare and contrast a little bit how you're thinking about that launch relative to what we've seen with Yeztugo over the last year or so.

**Johanna Mercier** (Executives):
Sure. Chris, it's Johanna again. We're really excited about the Q weekly. This will be the first long-acting oral in the prevention market potentially. And so we're excited about the opportunity. As we think about that launch, we are thinking that, that's going to really appeal to a population that might want the longer acting, but might not like injectables, for example. And if you think about the current market today, despite the very strong growth of Yeztugo, because I think people are really moving towards that long-acting as much as possible because it's truly prevention at the Q6 monthly, and that is a preference. 
There are some people that don't like the injection, and there's still a very strong oral market, both with Descovy as well as generic Truvada. And so we do think there's going to be a strong appeal for folks that are already on a daily oral to move to a Q weekly oral. And we're excited about that opportunity. And I would just add one more concept that's maybe a little bit different than a new launch because this is an extension based on Yeztugo in the weekly, we're going to be building off the access we already have on Yeztugo, specifically around the access we have in the pharmacy benefit space, which is about 70% or so. 
And so we do think that as of launch, it will really help support kind of a fast potential ramp-up as we go forward. And, of course, we'll continue to expand our access over the months to follow our launch. So more to come on that. But we're excited about that mix. And, of course, to your question about Yeztugo and how that plays out? We still believe longer-acting is going to be preferred in the HIV prevention space, not only with our Q6 monthly, but even with the potential of an annual injection with our Q12 potentially in 2028. So excited about what's to come in our HIV market.

**Operator** (Operator):
Our next question comes from Michael Yee at UBS.

**Michael Yee** (Analysts):
On the HIV treatment pipeline, you had a disclosure around 3107 monthly oral with a clinical hold. Maybe you could just give us an update on that program and what is going on there?

**Dietmar Berger** (Executives):
For the question. For 3107, this is one of our prodrug compounds. And with some of the prodrug compounds, as you know, we saw metabolites that have an unexpected impact, and that is really the reason for the clinical hold at this point. We're working through that clinical hold. At the same time, we have a broader portfolio really in the background, right, molecules coming out of research into the early development that are also aiming at the monthly space. So monthly oral treatment is still a key objective for us. We're following that working through 3107, and we're also in parallel working on backup molecules.

**Operator** (Operator):
Our next question comes from Terence Flynn at Morgan Stanley.

**Terence Flynn** (Analysts):
I was just wondering, Andy, if you can help us think about margin progression here into 2027. Obviously, you have done some business development deals. There's going to be some R&D spend behind those programs. And then also, as we think about the Biktarvy impact in '28, maybe just help us think high-level about impact to margins there, knowing it's a little early to give guidance, but just maybe directionally.

**Andrew Dickinson** (Executives):
Terence, thanks for the question. It's Andy. Look, at a high level, we continue to expect to have very strong margins not only in '27, but for the foreseeable future. And, of course, we'll provide more guidance on '27 and '28 as we get into those calendar years. You've seen this year our ability to do 3 acquisitions earlier this year and to absorb most of that spend. So when you look at our updated guidance this year, we are right on track when you parse out both our R&D spend as well as our SG&A spend, right on track for the expenses that we were targeting at the beginning of the year in our initial guidance. 
And then we added in the additional compensation accruals and expenses tied to our significant outperformance this year as our expected bonus payments have gone up. So we're really pleased with our ability to bring in these additional assets and fold them into the portfolio and absorb those expenses this year. And that's certainly our goal in future years as well. We are really focused, as you heard in my comments, on continued disciplined operating expense management and a very strong margin profile, both in terms of our gross margin as well as our operating margin. So we'll give you more specifics as we go forward, but we think the business is really set up nicely to continue to have a very strong margin.

**Operator** (Operator):
Our next question comes from Daina Graybosch at Leerink Partners.

**Daina Graybosch** (Analysts):
I wonder if you could talk more about the PALISADES partial clinical hold and Whether taking that amongst some of the other competitive clinical holds, particularly with the fast manufacturing, how you're thinking about fast manufacturing and if there's any risk you see for KITE-363 in autoimmune disease as well, and, sort of, the timing for when we might better understand the risk for both of these programs.

**Cindy Perettie** (Executives):
Thanks a lot, Daina, it's Cindy. So maybe I'll start with KITE-363 in autoimmune because we're not using rapid manufacturing with that, and that program does continue. We expect both the rheumatology and the neurology Phase I to continue and remain excited about that program. 
The second question that you had around PALISADES-1 and 2, that does have a rapid manufacturing. It's a 3-day manufacturing process that we shared with you. That is different than what I think you were referring to the other manufacturers in this space who have rapid manufacturing is a 1-day manufacturing, ours is a 3-day manufacturing. When you look at the partial clinical hold, we have made a decision to take a look at differences that we're seeing specifically with Grade 3 and Grade 4 ICANS in a small number of patients, and we have decided to take some time, pause and investigate that before we move forward. This is not -- there's no patient death. There's no Grade 5. So as soon as we have more information, we'll continue to keep you informed.

**Operator** (Operator):
Our next question comes from Louise Chen at Scotiabank.

**Louise Chen** (Analysts):
I wanted to ask you about, sort of, a more long-term view on things. Currently, around 70% of your commercial franchise is HIV. And just curious if you think out in the next couple of years, how do you expect this to change as you develop these new verticals?

**Daniel O'Day** (Executives):
Maybe I'll start, and I'll invite others to add, Louise. This is Dan. Our strategy has always been over the past 8 years or so to diversify our portfolio from a variety of different angles. I mean, first of all, within HIV, and that includes both HIV treatment and PrEP and my colleagues have spoken about that. I think you'll continue to hear how our longer-acting treatment programs continue to evolve over time. But we really are incredibly enthusiastic about how that is progressing. Of course, the PrEP options that allow for even longer dosing intervals are in our pipeline and our portfolio. 
And then we've always said that as that provides great robustness of our HIV business that we're very interested in diversifying, then, of course, outside of HIV and into oncology and inflammation. And I think the call here has really, I think, emphasized how much progress we've made on that front, both in oncology, cell therapy and our non-cell therapies in that growing portfolio. But also, I think this has really been a quarter where the inflammation and autoimmune pipeline has started to reveal itself. And you can see that we're going after highly differentiated mechanisms and a chance to really, kind of, break through efficacy barriers and bring different options for people with autoimmune diseases across all of our therapeutic platforms. I'd invite others to add as well.

**Dietmar Berger** (Executives):
I mean, this is Dietmar. Dan you said a lot of it, right? But I'm really similarly excited about both the diversification in the HIV portfolio. You look at it, we've got 6 long-acting programs currently ongoing. We're looking at up to 5 launches before 2033 in HIV therapy, which will help us to really address the needs of people with HIV and the different options that they appreciate.
On the prevention side, I'm also really excited about the weekly oral option that we have, but then also about the once every year, which so well aligns with other preventative visits that there's really, I think, a broader opportunity there. In oncology, we now have these 7 ongoing ADC programs. We look at the broader Tubulis technology that has broad applicability also together with our medicinal chemistry capabilities. And I think with the PRMT5 and MAT2A programs, we have another interesting program really focusing on synthetic lethality, which is very broadly present in different types of tumors. 
And then finally, the inflammation program currently with 13 different projects is really starting to reveal itself. And I think we have very differentiated mechanisms and really drugs there that have the potential to address large unmet medical needs, whether it's in inflammatory bowel disease, whether it's in B-cell depletion, which is a broad set of different types of diseases, or even in type 2 inflammation. So stay tuned, but I think that trajectory is starting to reveal itself.

**Operator** (Operator):
Our next question comes from Carter Gould at Cantor Fitzgerald.

**Carter Gould** (Analysts):
On gamgertamig and the update we're going to get on that front, Dietmar, can you kind of help set the stage there, the number of dosing cohorts we see -- we might see or the number of patients with over 6 months follow-up and clarify that things are still on track to enter registrational studies next year. .

**Dietmar Berger** (Executives):
So you're going to have to wait for the exact data release, right, that is coming at a conference later this year. But we're really looking forward to present more data, especially in the autoimmune cytopenia setting, also very much on the immune thrombocytopenia. I think that data is exciting. So stay tuned for that. Obviously, there's a much broader opportunity with B-cell depletion, as you know. And we're staying firm in our commitment to bring gamgertamig into a Phase III study next year in autoimmune cytopenia.

**Operator** (Operator):
Our last question comes from Geoff  Meacham at Citigroup.

**Geoffrey Meacham** (Analysts):
I get the IRA impact longer term to HIV, but maybe can you talk about the trends you're seeing in 3Q? I wasn't sure the reason why you guys are now recognizing a stronger realized price. And then related, can you talk a little bit about if there's any discernible growth trends and just the number of new patients entering the HIV treatment market?

**Johanna Mercier** (Executives):
Yes. Sure, Geoff. It's Johanna. Yes. So what we're seeing, and I'll just take Biktarvy, right, a 10% year-on-year growth. Overall HIV is 18% year-on-year, and that's obviously inclusive of Biktarvy, but also Yeztugo and Descovy. But if you think about the treatment and what's going on there, a lot of that has to do with, obviously, demand, but also inventory. And we saw a little bit of a higher Q3 inventory than we usually see across all of our HIV portfolio, which is obviously something that we're conscious of and understand that, that might mean that the seasonal -- the typical seasonal Q4 inventory that plays out in Q4 usually might be a little softer than usual, but you'll still see a ramp-up, a buildup, and that's part of our guidance, of course. 
So there was an inventory play. There was also favorable pricing and the favorable pricing has to do with the channels. So as I think I've shared before, but 1% of one channel is the channel moves if there's less of a discount in that channel versus a heavier discounted channel can play a big fluctuation in your pricing on a quarter-over-quarter,  kind of, basis. And so that's what's kind of, playing out there. And, of course, the demand piece. You see that the share for Biktarvy continues to grow. It's at an all-time high at 53%. So incredibly proud. We are #1 across naive, switch, restarts. 
And I think the team has just done an incredible job, and this is obviously not only in the U.S. but really worldwide and very proud of that work, let alone the Bixlenvo launch that we haven't really touched on, and I just closed the call on that. The Bixlenvo launch is absolutely on track versus expectations. It's very early. We launched late August, but really pleased to see incredible awareness of this molecule. And really, if you compare at similar time points post-launch, we are well ahead of recent competitor launches. So we feel very strongly that this is on the right track, and we just need to continue to build access and awareness in the field, both for complex regimen as well as virally suppressed switch patients.

**Operator** (Operator):
That completes the time we have for questions. I'll now invite Dan to share any closing remarks.

**Daniel O'Day** (Executives):
Well, first of all, I mean, I can't let a quarter go by like this without thanking the extraordinary Gilead team for delivering on this really exceptional third quarter. It's the strongest base business growth we've seen in more than 10 years. And at the same time, just the incredible advancement in our pipeline, which is getting diverse, as you can see, and we're preparing for even more launches into the future. So I'm incredibly proud of the progress that we've made as a team and the impact that we're creating for the communities and the patients we serve. 
As we look ahead, the multiple opportunities to drive growth across all of our therapeutic areas, the strength of our commercial and clinical execution, and the disciplined operating model that we are following all give us tremendous confidence in the trajectory of the company and really the fact that we can do even more for the patients and communities and shareholders that we serve. So thank you so much for joining today. As usual, we're here for your questions and comments, and we look forward to keeping you informed on our progress. Thank you again.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GILD_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CFO Andrew Dickinson｜guidance：FY2026 HIV 銷售成長預期由 8% 上調至 9–10%（原話："full year sales to grow between 9% and 10% year-over-year"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：FY2026 base business 銷售成長約 6–7%（原話："grow approximately 6% to 7% year-over-year"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：FY2026 base business 銷售區間 298–301 億美元（相對 5 月中位數加 3.5 億）（原話："range between $29.8 billion and $30.1 billion"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：cell therapy 全年預期降幅（中位數口徑）為 mid-teens（原話："cell therapy to decline mid-teens percentage year-over-year"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：Veklury 全年預期由約 6 億下修至約 3 億（原話："Veklury sales of approximately $300 million"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：排除併購與一次性項目後的 FY2026 non-GAAP EPS 區間，下緣上調 0.05（原話："$8.50 to $8.85, raised $0.05 on the bottom end"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：含收購 IPR&D 的全年 non-GAAP EPS 為負值（原話："full year non-GAAP EPS between negative $0.65 and negative"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：全年 non-GAAP 稅率因不可抵扣的 IPR&D 區間為 140% 與 115%（原文順序）（原話："effective tax rate to be between 140% and 115%"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：全年 acquired IPR&D 預期 115 億美元（原話："acquired IPR&D of $11.5 billion"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：R&D 與 SG&A 全年美元成長仍為中個位數（原話："SG&A expenses to increase a mid-single-digit percentage"）
- 2026-08-04｜CFO Andrew Dickinson｜guidance：Yeztugo 全年銷售目標維持約 10 億美元（原話："expect approximately $1 billion for Yeztugo sales"）
- 2026-08-04｜CFO Andrew Dickinson｜margin：non-GAAP 產品毛利率口徑（原話："Product gross margin was 87%"）
- 2026-08-04｜CFO Andrew Dickinson｜margin：帳面營業利益率為負，管理層同時提供排除 IPR&D 的口徑（原話："operating margin was negative 94%"）
- 2026-08-04｜CFO Andrew Dickinson｜margin：排除 IPR&D 後營業利益率約 49%（原話："quarter operating margin was approximately 49%"）
- 2026-08-04｜CFO Andrew Dickinson｜margin：排除併購與一次性收入後的 illustrative EPS 成長口徑（原話："13% compared to the same period last year."）
- 2026-08-04｜CFO Andrew Dickinson｜margin：其他收入中的版稅調整被標示為非經常、非現金（原話："This is a nonrecurring and noncash item"）
- 2026-08-04｜CFO Andrew Dickinson｜margin：SG&A 年增 12%，原因歸於 Yeztugo 推廣（原話："SG&A expenses were $1.5 billion, up 12% year-over-year"）
- 2026-08-04｜CFO Andrew Dickinson｜capital_allocation：Q2 回饋股東約 14 億美元，含 3.55 億買回（原話："we returned close to $1.4 billion to shareholders"）
- 2026-08-04｜CFO Andrew Dickinson｜capital_allocation：上半年回饋約 49% 自由現金流（原話："we have returned approximately 49%"）
- 2026-08-04｜CFO Andrew Dickinson｜commitment：管理層表示今年不預期再做大型併購，但保留機會主義（原話："anticipate pursuing additional sizable M&A transactions"）
- 2026-08-04｜CFO Andrew Dickinson｜capital_allocation：併購重心轉向整合 Arcellx、Tubulis、Ouro（原話："our near-term priorities are centered on"）
- 2026-08-04｜Johanna Mercier｜risk：Biktarvy 季增受 ACA 變動帶來的需求影響，高於預期（原話："including a greater-than-expected impact associated with"）
- 2026-08-04｜Johanna Mercier｜risk：管理層預期 HIV 治療市場成長回到 2–3%（原話："typical 2% to 3% rate of annual growth."）
- 2026-08-04｜Johanna Mercier｜margin：Biktarvy 年增 7% 的驅動口徑：價格（通路組合）、庫存、需求（原話："higher average realized price due to channel mix"）
- 2026-08-04｜Johanna Mercier｜margin：Biktarvy 營收數字在備稿與問答間說法不同（3.8 vs 3.7 億級）（原話："Biktarvy sales of $3.8 billion were up 7%"）
- 2026-08-04｜Johanna Mercier｜margin：問答中 Biktarvy Q2 數字講成約 37 億（原話："Biktarvy sales were about $3.7 billion for Q2"）
- 2026-08-04｜Johanna Mercier｜product：Yeztugo 6 個月再注射比例超過 70%（原話："More than 70% of users so far have returned for reinjection"）
- 2026-08-04｜Johanna Mercier｜product：Yeztugo Q2 銷售 2.32 億，季增 40%（原話："More than 70% of users so far have returned for"）
- 2026-08-04｜Johanna Mercier｜competition：Yeztugo 在 PrEP 轉換市場為整體第一（原話："million, up 40% sequentially and continue to target"）
- 2026-08-04｜Johanna Mercier｜competition：轉換來源約三等分：Apretude、Descovy、學名藥（原話："roughly about 1/3, 1/3, 1/3 across Apretude, Descovy and"）
- 2026-08-04｜Johanna Mercier｜competition：每日口服仍占 PrEP 市場 80–85%（原話："about 80%, 85% of the total market that are daily orals"）
- 2026-08-04｜Johanna Mercier｜competition：被問週口服是否反映長效針劑熱度不如預期，答無改變（原話："I would say nothing has changed."）
- 2026-08-04｜Johanna Mercier｜guidance：Descovy 價格有利（通路組合）預期可維持「到某個程度」（原話："we will be able to maintain that as we move forward"）
- 2026-08-04｜Johanna Mercier｜customer：Cell therapy 年減 14%，管理層歸因於類內與類外競爭（原話："expected ongoing in and out-of-class competition"）
- 2026-08-04｜Johanna Mercier｜competition：Tecartus 面臨更大競爭壓力（原話："increased competitive pressures for Tecartus"）
- 2026-08-04｜Johanna Mercier｜product：Trodelvy Q2 銷售 4.57 億（原話："sales of $457 million"）
- 2026-08-04｜Johanna Mercier｜product：Trodelvy 一線 TNBC 可及人群約為二線的兩倍（原話："addressable population almost double that"）
- 2026-08-04｜Johanna Mercier｜margin：Livdelzi 季增受降價部分抵銷（原話："partially offset by lower average realized price"）
- 2026-08-04｜Johanna Mercier｜product：Hepcludex 預期僅為小幅成長貢獻（原話："it is expected to be a modest growth contributor"）
- 2026-08-04｜Dietmar Berger｜commitment：BIC/LEN FDA 決定日 8 月 27 日（原話："anticipate a decision by August 27."）
- 2026-08-04｜Dietmar Berger｜commitment：每週口服 lenacapavir PrEP 的 FDA 決定日（原話："regulatory decision by February 2, 2027"）
- 2026-08-04｜Johanna Mercier｜commitment：ISL/LEN 預計 2027 上市（原話："the potential launch in 2027"）
- 2026-08-04｜Johanna Mercier｜commitment：anito-cel PDUFA 日為 12 月 23 日（原話："anito-cel's December 23 PDUFA date"）
- 2026-08-04｜Dietmar Berger｜product：anito-cel 第二線 iMMagine-3 最早 2027 申報（原話："potentially filing in this indication as early as 2027"）
- 2026-08-04｜Dietmar Berger｜product：anito-cel 製程成功率數據（原話："98% first-pass manufacturing success rate"）
- 2026-08-04｜Dietmar Berger｜product：GS-8824 卵巢癌 Phase I 確認 ORR 61%（原話："confirmed objective response rate of 61%"）
- 2026-08-04｜Dietmar Berger｜commitment：GS-8824 最早 2027 進入註冊性開發（原話："continue to expect entering registrational development"）
- 2026-08-04｜Dietmar Berger｜product：GS-3242 目前確定可每 4 個月給藥，6 個月待高劑量數據（原話："we're sure that this can be dosed once every 4 months"）
- 2026-08-04｜Dietmar Berger｜product：GS-3242 + lenacapavir Phase II 年底前啟動（原話："starting before the end of the year"）
- 2026-08-04｜Dietmar Berger｜product：TAB/ZAB + lenacapavir 每半年方案預計約 2030 上市（原話："potential for launch around 2030"）
- 2026-08-04｜Dietmar Berger｜product：PURPOSE 365 每年一針 PrEP 預計 2027 更新、2028 上市（原話："We expect to provide an update in 2027"）
- 2026-08-04｜CEO Daniel O'Day｜capital_allocation：管理層重申雙軌分散策略：病毒學內與腫瘤/免疫（原話："objective is still to diversify the business"）
- 2026-08-04｜CEO Daniel O'Day｜capital_allocation：HIV 長效組合被稱可延續至下個十年末（原話："durable and long-lasting well into the end of the next"）
- 2026-08-04｜CFO Andrew Dickinson｜capital_allocation：CFO：可同時分散並持續成長 HIV（原話："I think we can do both."）
- 2026-08-04｜CFO Andrew Dickinson｜product：Trodelvy 接近 20 億美元年化營收（原話："approaching a $2 billion run rate"）
- 2026-08-04｜Cindy Perettie｜risk：CAR-T 早線申報與 FDA 互動：未見重大變化（原話："have not seen major changes at this point"）
- 2026-08-04｜CEO Daniel O'Day｜commitment：CEO 結語：下半年預期兩項新上市（BIC/LEN、anito-cel）（原話："we expect the potential of 2 additional launches"）

### 問答異常語氣（迴避／改口／保留）
- GILD_Q2_2026_Earnings_Call_20260804.md｜問：Tyler Van Buren：Yeztugo 處方趨勢與 IQVIA 銷售的落差｜答法：Johanna 表示不評論 IQVIA 如何抓資料，改談自家數據與全年約 10 億目標
- GILD_Q2_2026_Earnings_Call_20260804.md｜問：Geoff Meacham：降低 HIV 集中度是否仍是目標｜答法：Dan 重申策略但未給 HIV 占比數字；邀 Andy 量化後，Andy 亦只提 PrEP 與 Trodelvy 年化營收，未給占比
- GILD_Q2_2026_Earnings_Call_20260804.md｜問：Chris Schott：Descovy 上半年價格有利是否持續｜答法：Johanna 答可維持「to a point」，未給下半年價格貢獻數字
- GILD_Q2_2026_Earnings_Call_20260804.md｜問：Anish Nikhanj：ISL/LEN 淨經濟性相對 Biktarvy／BIC/LEN，是否稀釋｜答法：Johanna 談轉換市場領導地位與 Merck 合作，未回應淨經濟性或稀釋
- GILD_Q2_2026_Earnings_Call_20260804.md｜問：Matthew Dellatorre：ISL/LEN 相對其他方案的優缺點｜答法：Dietmar 轉談自家 GS-1720／GS-3242 週口服方案，未列 ISL/LEN 的缺點

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
{"date":"20260525","verdict":"A+ 核心候選滿格訊號 — 五維齊全","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Yeztugo（lenacapavir）6 個月 LA-PrEP 在 US PrEP 市場佔據 ≥ 25% 份額並擴展至國際","columns":{"2Y 驗證點":"FY26 全年 ≥ $1B（公司 raised guide，從 $800M 起調）；FY27 ≥ $2B","5Y 驗證點":"FY30 ≥ $5B（含國際 + 一般 PrEP 滲透 + WHO/Gates Foundation Global Access $40 generic version 推 GILD pricing 結構轉型）","10Y 驗證點":"HIV 預防 TAM 從 2024 ~$2B 擴張至 2034 ~$15B 並 Yeztugo 佔 ≥ 40%","具體數字門檻":"FY26 ≥ $1B / FY27 ≥ $2B / FY28 ≥ $3B / FY30 ≥ $5B","信息來源":"2026-05-07 Earnings call + Gilead.com news release + Q1 26 prepared remarks PDF（s29.q4cdn.com）","漂移觸發條件":"連 2 季 QoQ &lt; 30% growth → 削弱；連 2 季 absolute QoQ 持平或下滑 → 反轉"}},{"id":"H2","text":"Biktarvy patent 護城河延長（2036）讓 HIV treatment 段在 2030s 之前不出現 generic erosion；HIV 整體 +5-10% CAGR","columns":{"2Y 驗證點":"FY26 HIV +8-10% / FY27 +5-8%（Yeztugo cannibalization 給 Descovy 才是淨負向）","5Y 驗證點":"HIV 2030 ≥ $25B（vs FY25 ~$20B）","10Y 驗證點":"Biktarvy LCM extension（新 formulation 如 long-acting Biktarvy）2030 後接班 — keep 50%+ US share 至 2036","具體數字門檻":"FY26 HIV $19-20B / Biktarvy ≥ $14B / Yeztugo $1B","信息來源":"USPTO settlement docs + 2026-Q1 earnings press release + fiercepharma.com 2024-09 settlement filing","漂移觸發條件":"連 2 季 HIV YoY &lt; 5% → 削弱；連 2 季 Biktarvy YoY &lt; 0% → 反轉"}},{"id":"H3","text":"Oncology pivot（三項併購 + Trodelvy 1L mTNBC + anito-cel CAR-T BCMA）將 oncology 從 ~$3B 規模成長到 ≥ $8-10B by 2030，填補 HIV patent cliff 預期","columns":{"2Y 驗證點":"FY26 Trodelvy 1L mTNBC PDUFA 通過 + anito-cel PDUFA 2026-12-23 通過；FY27 Trodelvy ≥ $2B / anito-cel ≥ $300M ramp","5Y 驗證點":"FY30 oncology ≥ $8B（Trodelvy $3B + anito-cel $2B + Ouro/Tubulis assets $1.5B + Yescarta $1.5B）","10Y 驗證點":"2032+ oncology &gt; 30% 營收佔比，HIV 集中度從 ~70% 降至 ~50% 以下","具體數字門檻":"Trodelvy 1L mTNBC PDUFA Q3-Q4 26 / anito-cel PDUFA 2026-12-23 / FY27 oncology ≥ $4B","信息來源":"Trodelvy 1L mTNBC CRL → 直接削弱 H3 50%；anito-cel CRL → 第二次重大 setback，反轉 H3"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Yeztugo 商業放量被保險覆蓋遲滯 + GSK ViiV Apretude 強力競爭攔截 — blockbuster narrative 只兌現一半","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"FY26 Q3 + Q4 Yeztugo 季銷售；US PrEP 新處方週度數據（IQVIA NRx）；保險 J-code 採用率","警戒閾值":"Q3 26 Yeztugo &lt; $250M 或 Q4 &lt; $350M → 全年 $1B guide 風險；連 2 季 QoQ &lt; 30% growth → R1 觸發"}},{"id":"R2","text":"Oncology M&A 整合失敗 — anito-cel BLA CRL 或商業化遠不及預期；管理層在 2027-2028 需要再 write-down","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"anito-cel PDUFA 2026-12-23 結果；Trodelvy 1L mTNBC PDUFA 2H26；Ouro/Tubulis Phase 1/2 readout 2027","警戒閾值":"任一 CRL → 削弱 H3 30%；連 2 個 setback → 反轉 H3，oncology pivot narrative 受損"}},{"id":"R3","text":"HIV 結構性 disruption — Merck islatravir 1 次/年 LA-PrEP 成功 + ViiV 第三代 integrase oral 替代 Biktarvy + 美國 IRA 對 HIV 議價","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Merck islatravir Phase 3 readout 2027-2028；ViiV CROI annual data；IRA negotiation list 公布（每年 2 月）","警戒閾值":"Islatravir LA-PrEP Phase 3 hit → R3 削弱 H1（不 H2）；IRA 把 Biktarvy 列入 → 削弱 H2"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A+","val":"🟢","ma":"✅","trap":"🟢","moat_trend":"加深","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":134.36,"archetype":null,"cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名中除程式欄以外的每一個**（程式稍後才會算的 p_bull_pct／p_bear_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；`asym_ratio`／`ev5y_pct`／`irr_base_pct`／`bull_5y_price`／`bear_5y_price` 的漂移歸因同樣由程式生成條目（程式用本次情境、依先換情境後換股價的順序拆量），你不要為它們開條目；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

**給讀者看的文字欄不准出現內部代號**：`thesis.H[]`／`thesis.R[]` 的各欄（信息來源／漂移觸發條件等）、`triggers[].text`、`counter_evidence.contradictions[]` 各欄、`answers.*.verdict`／`answers.*.reasoning` 這類文字，一律不得出現事實表 id（`f_` 開頭，如 `f_consensus_rev_3m_fy1_pct`）或軸／finding id（`軸名#n`，如 `competitive_share_entrants#0`）——這些是程式內部代號，不是給讀者的話。要引用哪個事實或哪個軸，寫進對應的 `fact_refs[]`／`evidence_refs[]` 陣列，文字欄本身只寫人話。

---

## 尾段：scenario_inputs 形狀與回覆格式

**本檔 FY1 共識 EPS ≤ 0（虧損），程式已把估值口徑定為 `sales_multiple`：情境樹用營收路徑 × 終端 EV/S，不用 EPS × 本益比。** 口徑由程式決定，你填什麼 `valuation_basis` 都會被覆寫。`scenario_inputs` 的鍵名與形狀必須完全照下面這份（不得增刪改名；程式據此產生 `dd_scenario.py` 的輸入檔，寫錯鍵名就是整段判斷失效）：

```json
{
  "valuation_basis": "sales_multiple",
  "terminal_label": "FY20XXE",
  "start": {"rev": <FY+1 共識營收，百萬，報告幣別；抄事實表 f_rev_consensus_fy1_m>, "ev_s": <目前 EV/S（EV÷FY+1 共識營收）；抄事實表 f_ev_s_fwd>, "basis": "<起點口徑一句話：營收取哪一年、EV/S 的分母是哪一年，須與終端 EV/S 分母同口徑>"},
  "rev": {"bull": [<Y1>, <Y2>, <Y3>, <Y4>, <Y5>], "base": [五個數], "bear": [五個數]},
  "ev_s": {"bull": <終端 EV/S>, "base": <倍數>, "bear": <倍數>},
  "net_debt_y5": {"bull": <終端年淨負債，百萬，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "shares_y5": {"bull": <終端年稀釋股數，百萬股，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "p": {"bull": <機率整數>, "base": <整數>, "bear": <整數>},
  "yield_pct": {"dividend": <股息殖利率 %>, "net_buyback": <淨回購殖利率 %>},
  "max_dd": {"lo": <負數 %>, "hi": <負數 %>, "basis": "<範圍怎麼推出來的，見判斷卡③情境樹假設段>", "trigger_time": null},
  "basis": {"bull": "<這支路徑的假設一句>", "base": "…", "bear": "…"},
  "endo_ceiling_exceeded": <true|false，共識 CAGR 是否超過 §5.R 內生天花板>
}
```

（**不要**填 `eps`、`pe`、`second_stage`、`peer_max_fpe`；`eps_meta` 仍照常寫共識三年 EPS。現價、目前淨負債（`f_net_debt_m`）、目前股數（`f_shares_diluted_m`）由程式從事實表帶進 `scenario.json`。）

**終端每股價＝max(0, (終端營收 × 終端 EV/S − 終端淨負債) ÷ 終端股數)**，股權價值為負就是 0（Bear 情境債務吃光股權時，要如實寫出讓它歸零，不要為了好看調高倍數）。`net_debt_y5` 要反映該情境下的現金流與融資（虧損公司的淨負債通常會變大，不是沿用目前值）；`shares_y5` 要反映該情境下的增資與稀釋；兩者填 null 才是沿用目前值，不是預設答案。`ev_s` 是終端年 EV ÷ 終端年營收，須與 `start.ev_s` 同口徑（前瞻 vs trailing 不可混）。

`dd_scenario.py` 會擋：`rev` 各路徑長度 ≠ 5、終端營收非 Bear＜Base＜Bull、三機率加總 ≠ 100、`p.bear` ＜ 20、`endo_ceiling_exceeded=true` 且 `p.bear` ＜ 30、`p.base` ＞ 50。另有機械閘：Bull 前兩年營收不得與 Base 相同（情境退化）、`|max_dd.lo|` 不得小於任一情境終點跌幅。機率與路徑是你的判斷，算術（IRR／倍數貢獻／AR）全由腳本算，不要自己填結果欄。

**回覆全文即 `judgment.json` 內容**：緊湊 JSON（`json.dumps(obj, separators=(",", ":"))` 等效格式），陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）。不寫 `scenario.json`（程式從 `scenario_inputs` 產生）。不填不歸你的欄（`decision_inputs` 的機械欄、`reasoning`／`plain` 頂層、`moat.spread_table`／`competitors`、`contradictions`／`triggers` 等舊形狀頂層欄）——填了機械閘會擋。`decision_inputs.asym_ratio`／`irr_base_pct`／`ev5y_pct` 一律填 `null`，由腳本從 scenario 機械算回。

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GILD_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
