你是 stock-analyst **v20 判斷 agent**，標的 LIN（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"LIN","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LIN_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LIN_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":9404,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf"},"note":"未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）"},{"id":"f_kpi1_non_gaap_adjusted","label":"Non-GAAP（adjusted）營業利益","value":2763,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf"},"note":"未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）"},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益率","value":29.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf"},"note":"未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）"},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":2150,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf"},"note":"未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）"},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率","value":22.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf"},"note":"未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）"},{"id":"f_kpi6_2026_q4_adjusted_diluted","label":"指引：2026 Q4 adjusted diluted EPS","value":"4.40–4.50","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf"},"note":"未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）"},{"id":"f_kpi7_2026_adjusted_diluted_ep","label":"指引：2026 全年 adjusted diluted EPS","value":"17.82–17.92","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf"},"note":"未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）"},{"id":"f_kpi8_project_backlog","label":"專案積壓訂單（project backlog）","value":11000,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf"},"note":"未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_lin_gross_margin_pct","label":"LIN 毛利率","value":47.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LIN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lin_operating_margin_pct","label":"LIN 營業利益率","value":27.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LIN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lin_fcf_margin_pct","label":"LIN FCF 利潤率","value":14.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LIN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_apd_gross_margin_pct","label":"APD 毛利率","value":32.06,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_apd_operating_margin_pct","label":"APD 營業利益率","value":24.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_apd_fcf_margin_pct","label":"APD FCF 利潤率","value":-2.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_fcf","label":"自由現金流（FCF）","value":1777,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf"},"note":"未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":514.24,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":1.9,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":69.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":17.89,"period":"2026-11-02","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-02","citation":"yfinance earnings_estimate"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":18.2,"period":"2026-11-02","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-02","citation":"yfinance earnings_estimate"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":34.15,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝67.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":67.5,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.51,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":7.14,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.225,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":22755.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 26702.0、現金 3947.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":459.08,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":258834.24,"period":"2026-11-02","unit":"USD m","basis":"市值 236079.24 ＋ 淨負債 22755.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":36417.02,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":38173.24,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（25 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.11,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 514.24 / W52 476.54 / W104 461.9 / W250 399.68 / W250 13週斜率 0.74%"},{"id":"f_ma_w52","label":"52 週均線","value":476.54,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":461.9,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":399.68,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.74,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K FY2025 列示競爭對手為 Air Liquide、Air Products、Messer、Taiyo Nippon Sanso 及大量中小地方業者；管線網絡所在地為 Linde 的競爭優勢。未點名新進入者。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm","excerpt":"In locations where Linde has pipeline networks, which enable the company to provide reliable and economic supply of products to larger customers, Linde derives a competitive advantage.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Linde 10-K 稱不依賴單一客戶或少數客戶","source":"Linde plc Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm","excerpt":"Customers – Linde is not dependent upon a single customer or a few customers. International – Linde is a global enterprise with approximately 64% of its 2025 sales outside of the United States.","as_of":"2026-02-27","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Linde 自身信用：2026年1月 Standard Chartered 固收筆記列示 S&P 對 Linde plc 歐元債評等為 A；未查到評等下調或客戶破產事件。","source":"Standard Chartered, Fixed income trade note Linde plc 20 January 2026","url":"https://www.sc.com/hk/market-outlook/fixed-income-trade-note-linde-plc-20-january-2026/","excerpt":null,"as_of":"2026-01-20","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Linde FY2025 10-K 的客戶集中度/信用風險附註（單一客戶占比）","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm","excerpt":null,"as_of":"2026-02-25","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Linde Q3 2026（2026-10-29 公布）：全年調整後 EPS 指引 $17.82–$17.92（+8%–9%），Q4 指引 $4.40–$4.50；歐洲量在連降四季後回升，Chemicals & Energy 成長 12%，專案積壓約 $11B（為二手摘要，未核原文）","source":"Linde Reports Third-Quarter 2026 Results (investingnews.com 轉載)","url":"https://investingnews.com/linde-reports-third-quarter-2026-results/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q3 2025 財報電話會：電子業為成長最快區塊（約佔銷售 9%、+6%），歐洲為最弱市場、工業與化學基礎量下滑；Linde 以定價而非量推動獲利（二手摘要）","source":"Motley Fool, Linde Q3 2025 earnings call transcript","url":"https://www.fool.com/earnings/call-transcripts/2025/10/31/linde-q3-2025-earnings-call-transcript","excerpt":null,"as_of":"2025-10-31","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Linde Q3 2026 結果新聞稿含全年指引與 backlog","source":"EQS/Deutsche Börse Linde Reports Third Quarter 2026 Results","url":"https://live.deutsche-boerse.com/news/EQS-News-Linde-Reports-Third-Quarter-2026-Results-Earnings-Release-Tables-Attached-6fcd57b3-33d5-4199-9dbe-4d8d284e59a8","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 揭露 Linde 在例行業務中面臨環境、稅務、反壟斷與人身傷害等索賠、法律程序及政府調查，並已按會計判斷認列或揭露；未點名特定 DOJ/FTC/EU 案件。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm","excerpt":"Linde is subject to various claims, legal proceedings and government investigations that arise from time to time in the ordinary course of business. These actions are based upon alleged environmental, tax, antitrust and personal injury claims, among others (see Note 17 to the consolidated financial statements).","as_of":"2026-02-25","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"葡萄牙競爭機構對 Linde 收購 Acaíl Gas 啟動第二階段深入審查（2026，併購審查非濫用調查）","source":"Global Competition Review Linde 組織頁","url":"https://globalcompetitionreview.com/organisations/linde","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Linde 10-K FY2025 風險因素列出貿易衝突、關稅與進出口管制為國際營運風險，可能降低需求、售價或營收；法規面亦含貿易進出口限制與經濟制裁。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm","excerpt":"Linde has substantial international operations which are subject to risks including devaluations in currency exchange rates, transportation delays and interruptions, political and economic instability and disruptions, restrictions on the transfer of 8 Table of Contents funds, trade conflicts and the imposition of duties and tariffs, import and export controls, changes in governmental policies","as_of":"2026-02-25","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋未發現針對 Linde 的實體清單或出口管制行動；2026 年搜尋結果僅見中國對美／歐其他實體的一般性出口管制名單擴大，未提及 Linde。","source":"WebSearch: Linde China export control OR trade restriction 2026（Thomson Reuters OneSource 2026-07-28 等）","url":"https://www.thomsonreuters.com/en-us/help/onesource-global-trade/regulatory-insights/2026/july-28th/china-adds-eu-entities-export-control-list","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"俄羅斯 Amur 區仲裁法院 2026 年 1 月判 Linde 實體須賠 Amur GPP 800 億盧布，Linde 俄羅斯子公司 2 月提出上訴（俄語媒體報導）","source":"finance.mail.ru：«Дочка» Linde подала апелляцию на взыскание по иску Амурского ГПЗ","url":"https://finance.mail.ru/article/dochka-linde-podala-apellyatsiyu-na-vzyiskanie-po-isku-amurskogo-gpz-69199564/","excerpt":null,"as_of":"2026-02-15","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"卡達 Ras Laffan 約占全球氦氣 30–38%，2026 年 3 月衝突使約三分之一全球氦氣供應中斷","source":"Exiger：Iran War Disrupts One-Third of Global Helium Supply","url":"https://exiger.com/perspectives/iran-war-disrupts-one-third-of-global-helium-supply/","excerpt":null,"as_of":"2026-03-15","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"Linde 於 2026 Q2 電話會議稱，儘管荷莫茲海峽緊張，仍有信心維持供應，並提高 Q3 氦氣價格","source":"GasWorld：Linde raises helium prices in Q3","url":"https://www.gasworld.com/story/linde-raises-helium-prices-in-q3/2263012.article/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Linde/BOC 簡報（2025-10）列示俄羅斯氦氣來源因制裁無限期延後，卡達擴產預定 2027、2028","source":"BOC presentation (bcryo.org.uk)","url":"https://bcryo.org.uk/sites/default/files/BOC.pdf","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Linde 俄羅斯或有負債約 18 億美元（RCA 11 億、Amur GPP 7 億）","source":"Panabee Linde Q2 2026 report","url":"https://www.panabee.com/news/linde-earnings-q2-2026-report","excerpt":"A material risk remains regarding $1.8 billion in contingent liabilities associated with Russian engineering projects, specifically RCA and Amur GPP. Ongoing legal disputes and asset seizure risks in Russia necessitate close monitoring, as these factors create uncertainty regarding asset values.","as_of":"2026-07-31","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 銷售 94.04 億美元，年增 9%（含匯率 +1%）；10-Q 載基礎銷售 +5%（價格 +3%、量 +2%），量增主要來自電子、化工與能源、製造業。不同來源對基礎成長數字有出入（8-K 附件摘要為 +9%＝價 6%＋量 3%），需以原始文件核對。","source":"Linde 10-Q 2026-09-30 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001707925/000162828026068079/lin-20260930.htm","excerpt":"sales grew 3% from higher price attainment and 2% from higher volumes primarily driven by the electronics, chemicals and energy, and manufacturing end markets.","as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 各終端市場（剔除匯率、成本轉嫁、併購）年增：化工與能源（占22%）+12%、製造（21%）+7%、電子（10%）+15%、醫療（15%）+2%、食品飲料（9%）+3%、金屬礦業（12%）+3%。來源為搜尋摘要對投資人簡報的轉述，未讀原頁。","source":"Linde Q3 2026 investor presentation (via search summary of SEC/Business Wire release)","url":"https://www.sec.gov/Archives/edgar/data/0001707925/000165495426009199/lin_ex991.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"歐洲需求弱：管理層預期歐洲需求與量能持續疲弱；醫療、電子為亮點，化工為最受挑戰的終端市場之一（此為 2025 Q3 call 的說法）。","source":"Linde Q3 2025 earnings call transcript (Motley Fool)","url":"https://www.fool.com/earnings/call-transcripts/2025/10/31/linde-q3-2025-earnings-call-transcript","excerpt":null,"as_of":"2025-10-31","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 財報電話會議重點，含終端市場與展望評論","source":"MarketBeat Linde Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-linde-q3-earnings-call-highlights-2026-10-29/","excerpt":"Volume growth was 2%, split roughly between contributions from projects in the backlog and organic growth, while pricing increased 3%. Operating margin was 29.4%, down 30 basis points from the previous year.","as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Linde 10-K FY2025 風險因子列舉能源與原料成本、供應中斷、地緣、商譽減損、災害、資安等風險；所摘錄章節未提及具體替代技術取代其核心產品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm","excerpt":"Linde may be subject to information technology system failures, network disruptions and cybersecurity breaches or other related incidents.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 描述 Linde 銷售仍以現場供氣、液態槽車（merchant）、瓶裝三種配送方式並行整合，merchant 客戶合約為三至七年的需求合約，並以區域為單位管理客戶關係；10-K 此段未描述通路或商業模式的結構性轉變。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm","excerpt":"There are three basic distribution methods for industrial gases: (i) on-site or tonnage; (ii) merchant or bulk liquid; and (iii) packaged or cylinder gases. These distribution methods are often integrated, with products from all three supply modes coming from the same plant.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Linde Q3 2026 報告(2026-10-29)將全年調整後 EPS 指引上調至 $17.82–$17.92(+8~9%),先前為 $17.70–$17.90;Q3 調整後 EPS $4.59(+9%),高於公司 7 月指引 $4.45–$4.55;全年資本支出預期 $5.5–6.0 億美元級(原文單位 billion)。","source":"Linde Reports Third Quarter 2026 Results (finviz/EQS 轉載)","url":"https://finviz.com/news/411123/linde-reports-third-quarter-2026-results","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"7/31 Q2 後 MarketBeat:公司全年 EPS 指引 $17.70–$17.90、Q3 指引 $4.45–$4.55,低於當時分析師預期 $17.93 / $4.59;僅上調指引下緣(自 $17.60)。","source":"MarketBeat: Linde updates Q3 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/linde-nasdaqlin-updates-q3-2026-earnings-guidance-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Chartmill 顯示 2026-10-17 時 29 位分析師的 FY2026 EPS 共識為 18.05 USD、Q3 EPS $4.56;此共識高於公司當時指引區間上限 $17.90(10/29 新區間 $17.82–17.92 仍低於 18.05;摘要口徑待核)。","source":"Chartmill LIN estimates","url":"https://www.chartmill.com/stock/quote/LIN/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價分布(2026-07/08):MarketBeat 13 位分析師平均 $548.67、高 $600、低 $460,評級 Buy;Walnut Invest 25 位平均 $547.08、中位 $550(2026-08);TickFlow 14 位平均 $562.14、高 $579(2026-08-01)。各站樣本與日期不同。","source":"MarketBeat price-target page / Walnut Invest / TickFlow","url":"https://www.marketbeat.com/stocks/NASDAQ/LIN/price-target/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Argus 於 2026-05-18 將 Linde 目標價由 $535 調至 $563,維持 Buy。","source":"Placera/Argus telegram","url":"https://www.placera.se/telegram/argus-adjusts-price-target-on-linde-to-563-from-535-maintains-buy-rating-20260518","excerpt":null,"as_of":"2026-05-18","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Linde Q3 2026 官方新聞稿：全年調整後 EPS 指引 $17.82–$17.92","source":"EQS News Linde Reports Third Quarter 2026 Results","url":"https://live.deutsche-boerse.com/news/EQS-News-Linde-Reports-Third-Quarter-2026-Results-Earnings-Release-Tables-Attached-6fcd57b3-33d5-4199-9dbe-4d8d284e59a8","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月8-K共8份，重大項目僅3份：2025-12 的364天$15億循環信用額度（Item 1.01），及兩次歐元債發行（Item 8.01）；無併購完成(2.01)、重編(4.02)等項目。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001707925&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"Linde AG 前少數股東在慕尼黑法院的擠出補償價格訴訟：2023-11 法院駁回全部請求，原告已上訴；另與 RCA 的俄羅斯專案糾紛仍在 HKIAC 仲裁中，St. Petersburg 禁令未解除。","source":"SEC EDGAR 10-K FY2025 Item 8 附註","url":"https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm","excerpt":"In November 2023, the court issued a decision rejecting the plaintiffs’ claims in their entirety and determining that the cash merger squeeze-out consideration was appropriate. The plaintiffs have appealed this decision.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單中重大項目僅信用額度與債券發行，無 Item 2.01 併購完成申報。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001707925&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"未見美國證券集體訴訟；既有訴訟為慕尼黑擠出補償價格程序（原告上訴中）與 RCA 俄羅斯專案糾紛（HKIAC 仲裁進行中）。","source":"SEC EDGAR 10-K FY2025 Item 8 附註","url":"https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm","excerpt":"Despite the judgments of the Hong Kong court and similar orders issued by the HKIAC arbitration tribunals, RCA is continuing to pursue its claims in Russia and neither the St. Petersburg injunction affecting Linde’s shares and assets has been lifted, nor the proceeding in St. Petersburg been stayed. The HKIAC arbitration proceedings are ongoing.","as_of":"2026-02-25","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"第三方聚合站顯示 Linde Gas & Equipment Inc.（Livingston, TN）2025-07-25 收到 FDA Form 483（NOxBOXi 醫療器材，CAPA 缺失等）；Form 483 非警告信，未見警告信或召回。發布日在12個月窗之外，原文未核。","source":"globalkeysolutions.net FDA 483 紀錄 - Linde Gas & Equipment Inc - July 25, 2025","url":"https://www.globalkeysolutions.net/records/483/linde-gas-equipment-inc/7ad5257a-e2ee-45cb-b346-12a83755a74f/raw","excerpt":null,"as_of":"2025-07-25","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"LIN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.86,"operating_margin_pct":27.08,"fcf_margin_pct":14.02,"rd_intensity_pct":0.41},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LIN","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"APD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":32.06,"operating_margin_pct":24.85,"fcf_margin_pct":-2.39,"rd_intensity_pct":0.72},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APD","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AI.PA","period":"TTM ending 2025-09-30（1季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AI.PA","as_of":"TTM ending 2025-09-30（1季加總）"},"note":"Total Revenue 缺失，無法算利潤率；僅 1 季可得，非完整 TTM"},{"name":"4091.T","period":"TTM ending 2026-06-30（2季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.4091.T","as_of":"TTM ending 2026-06-30（2季加總）"},"note":"Total Revenue 缺失，無法算利潤率；僅 2 季可得，非完整 TTM"}],"subject":"LIN"},"financial_history":{"ticker":"LIN","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":33364000000.0,"revenue_yoy_pct":null,"gross_margin_pct":41.7,"operating_margin_pct":19.36,"net_income":4147000000.0,"diluted_eps":8.23,"free_cash_flow":5691000000.0,"fcf_margin_pct":17.06,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":32854000000.0,"revenue_yoy_pct":-1.53,"gross_margin_pct":46.76,"operating_margin_pct":24.67,"net_income":6199000000.0,"diluted_eps":12.59,"free_cash_flow":5518000000.0,"fcf_margin_pct":16.8,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":33005000000.0,"revenue_yoy_pct":0.46,"gross_margin_pct":48.06,"operating_margin_pct":26.04,"net_income":6565000000.0,"diluted_eps":13.62,"free_cash_flow":4926000000.0,"fcf_margin_pct":14.93,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":33986000000.0,"revenue_yoy_pct":2.97,"gross_margin_pct":48.83,"operating_margin_pct":27.23,"net_income":6898000000.0,"diluted_eps":14.61,"free_cash_flow":5089000000.0,"fcf_margin_pct":14.97,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/LIN/LIN_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Linde plc** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Welcome to the Linde Third Quarter 2026 Earnings Call and Webcast. [Operator Instructions] Please be advised that today's conference is being recorded. [Operator Instructions] 
I will now turn the conference over to Mr. Juan Pelaez, Head of Investor Relations. Please go ahead, sir.

**Juan Pelaez** (Executives):
Thank you. Good morning, everyone, and thanks for attending our 2026 third quarter earnings call and webcast. I'm Juan Pelaez, Head of Investor Relations, and I'm joined this morning by Sanjiv Lamba, Chief Executive Officer; and Matt White, Chief Financial Officer. 
Today's presentation materials are available on our website at linde.com in the Investors section. Please read the forward-looking statement disclosure on Page 2 of the slides and note that it applies to all statements made during the teleconference. The reconciliations of the adjusted numbers are in the appendix of this presentation. Sanjiv will provide some opening remarks, and then Matt will give an update on Linde's third quarter financial performance and outlook, after which, we will wrap up with Q&A. 
Let me now turn the call over to Sanjiv.

**Sanjiv Lamba** (Executives):
Thanks, Juan, and good morning, everyone. Three months ago, we delivered financial results that were not up to the expectation of our owners. That message was received loud and clear by the Linde organization. And so we have and will continue to take actions that increase shareholder value. During the third quarter, we recorded a $425 million restructuring charge to better align our cost base and portfolio with market conditions. Roughly half relates to severance, particularly in lower growth regions. The balance relates primarily to portfolio and asset actions, mostly in the U.S. home care business or Lincare. 
Effective this quarter, I realigned this business to report directly to Matt, which, among other reasons, has prompted us to modify the segment reporting by moving it into the Global Other segment. This will provide investors with greater insight into the underlying performance of our regional Gases businesses, while we continue to restructure Lincare and evaluate strategic alternatives. 
Turning to the quarter. While performance has improved, there is still more work to be done. Sales of $9.4 billion, operating profit of $2.8 billion and EPS of $4.59 were all quarterly records. However, operating margin, excluding cost pass-through, was essentially flat, reflecting continued headwinds from non-gas segments. Aside from the restructuring actions, we also have a series of price and productivity initiatives underway to stay ahead of the inflationary momentum building across the regions. While the overall financial performance is heading in the right direction, sales trends remain varied by geography and end market, which can be found on Slide 3. 
Starting with consumer-related markets. Electronics leads with 15% growth, primarily driven by the organic growth across APAC and the U.S. These figures exclude our 50% Taiwanese joint venture, which is growing at similar rates. We also have approximately $2 billion of electronics projects under construction in the U.S., Korea and China, providing a strong foundation for continued double-digit growth. Food & Beverage grew 3%, led by the Americas and EMEA. Structural consumer trends, including greater consumption of carbonated beverages, higher-quality prepared ready-to-eat meals and food delivery services all continue to drive demand for our gases, equipment and services. Healthcare grew 2%. However, excluding Lincare, the growth is mid-single digit, which is aligned with demographic trends. As we continue to trim the Lincare portfolio, I expect the sales trends to lag market average, but I fully expect to see improvements in both the quality and profitability of the remaining businesses. 
Turning to industrial markets. Chemicals & Energy grew 12%, reflecting stronger volumes in the U.S. and China as well as pricing actions to recover prior cost inflation, especially in the Americas. Customers along the U.S. Gulf Coast and in China are benefiting from the relative raw material advantages amid the Middle East conflict, supporting stronger demand. This has been particularly evident among more complex refiners requiring more hydrogen to process heavier and higher sulfur crude. Metals and mining was up 3%, driven primarily by the Americas, with stronger construction and industrial activity in North America. This was partially offset by slight contractions in EMEA and APAC. Importantly, pricing improvements are broad-based across all major geographies as we continue to manage inflation. 
The manufacturing end market grew 7%, reflecting broad-based price increases and stronger volumes in the U.S., China and India, including continued aerospace growth. U.S. packaged gas growth remains elevated at low teens from construction and data center activity. Rare gas sales for satellite propulsion have softened as customer payloads continue to await launch. Merchant and on-site volumes remain strongest in the U.S., including higher activity in the U.S. Gulf Coast energy and chemicals, stronger metals production and increased space propellant. China and India growth rates remain healthy with our portfolio of Tier 1 customers. 
In summary, volume growth remains concentrated in key geographies and specific end markets, while price increases are more broad-based and tracking with inflation. In addition, the $8 billion sale of gas project backlog will provide future growth and increase supply density across core geographies. That being said, we still have opportunities for improvement. The third quarter restructuring program and the ongoing productivity initiatives will expedite our efforts to better align each local cost structure with market conditions. 
Furthermore, we are accelerating pricing efforts to stay ahead of rising inflation. And at Lincare, which has weighed on the overall results, we're taking decisive actions to improve performance while evaluating strategic options. Linde's operating model is built on discipline, accountability and continuous improvement. When performance falls short, we act. When conditions change, we adapt. When attractive opportunities emerge, we invest with discipline. I remain confident that the Linde organization will continue to deliver industry-leading results that our owners expect from us. 
I'll now turn the call over to Matt to walk through our financial results.

**Matthew White** (Executives):
Thanks, Sanjiv. Please turn to Slide 4 for the consolidated results. Sales of $9.4 billion increased 9% over prior year. Currency impact of 1% continues to abate and is not expected to have a meaningful impact for the remainder of the year. Conversely, 1% of cost pass-through, which represents contractual billing of energy cost variances, has steadily increased from energy inflation. Acquisitions and engineering each contributed 1% sales growth from tuck-in M&A and higher third-party plant sales, respectively. Excluding these items, underlying sales grew 5%. Volume of 2% is roughly split between project backlog contribution and organic growth, although most of the organic growth relates to equipment sales in APAC and EMEA. As Sanjiv mentioned, organic growth is concentrated in a few key end markets and geographies, although prior year comps are becoming easier in certain regions, such as EMEA. 
Prices increased 3% in the quarter. While the majority came from ongoing price actions, a portion relates to prior and current period inflation cost recovery in the Americas. An acceleration of energy and distribution cost pressures in North America warranted incremental recovery. While we don't anticipate these costs to sustain into the fourth quarter, the team is prepared for additional measures, if necessary. Operating profit grew 8% to $2.8 billion. Operating margin of 29.4% fell 30 basis points from prior year, but was flat excluding cost pass-through, which is highlighted in the table to the right. Margin increases of the combined gas segments were offset by declines in Engineering and Global Other. As stated earlier, actions are well underway to address the underperformance. 
EPS of $4.59 grew 9% over prior year, or 8% excluding the impact of currency. Year-to-date, we're losing about 2% EPS growth from Lincare. So, negating that headwind will support the return to double-digit EPS growth for the global organization. 
Slide 5 provides a summary of capital management. Operating cash flow of $3.2 billion increased 8% over prior year, in line with EBITDA growth. As mentioned in prior calls, the second half OCF is higher due to seasonal cash timing of taxes, interest and incentives. Base CapEx, which includes growth investments as well as maintenance and repair, is flat versus prior year, or down when excluding currency impact. The excess available operating cash flow affords Linde a steady capital allocation process, which can be seen in the pie chart. We've deployed over $9 billion of capital year-to-date, with roughly half invested into the business and the remainder distributed back to shareholders. We've maintained this approach through good times and bad, and the rising interest rate environment reinforces something we have known for a long time. Balance sheets and cash flow matter. The health and stability of both provides us significant optionality regardless of the future macro. 
I'll wrap up with guidance on Slide 6. For the fourth quarter, we're guiding an EPS range of $4.40 to $4.50, or 5% to 7% growth. While no prior year currency impact is assumed, we do expect a 1% headwind sequentially. Consistent with prior guides, no economic improvement is assumed. This also applies to Lincare. Despite the recent actions, we are not yet embedding any meaningful change to Q4 profit. While I fully expect future improvement, we're taking a more cautious view for the near term. The full year guide of $17.82 to $17.92 simply rolls the fourth quarter into the year-to-date actual. However, one change you may notice is that the full year FX benefit increased from a strong 1% last quarter to a weak 2% this quarter. That's more rounding than anything else, so time will tell where the final number lands. 
Overall, the core gas business is healthy, but there are clear opportunities to improve, most notably around management actions in price and productivity against the backdrop of higher inflation. And while Lincare is a headwind to results today, we're taking significant actions to improve going forward, while simultaneously increasing transparency and executive oversight as we evaluate strategic options.  
I'll now turn the call over to Q&A.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of David Begleiter from Deutsche Bank.

**David Begleiter** (Analysts):
Sanjiv and Matt, just on the backlog, do you still expect to end the year on a sale of gas basis around the $8 billion level? And on sale of plant, how should that progress over the next few quarters? And what does that mean for engineering sales growth in 2027?

**Sanjiv Lamba** (Executives):
David, the sale of backlog sits close to $8 billion today. My expectation remains we will continue to start up for the rest of this quarter, a number of projects that might lead up to around $1 billion, as we previously mentioned. And depending on customer timings, we expect still to be able to get pretty close to that $8 billion number. So the target internally remains at 8 handle. Sometimes that's dependent on customers' final decision, but feel pretty confident we're going to be in that vicinity. As far as sale of plant backlog is concerned, that's just under $3 billion at the moment. It has sitting within that some space component today. We expect to see that to continue to grow as well. So I expect the trend line for sale of plant backlog will remain along the lines we have at this point in time, growing over the course of next year. In February next year, we'll provide you with a more pronounced guidance on what we see for the business overall. And within that, we can address that question specifically.

**Operator** (Operator):
Your next question comes from the line of Duffy Fischer from Goldman Sachs.

**Patrick Fischer** (Analysts):
Just a question on cost. If you look at your COGS line in Q3, year-over-year, you're up 13% and your acquisitions and volume are up 3%. So if you just subtract that, kind of a cheap metric would say that your per unit COGS is up about 10% per unit. Can you just walk through what that is? That seems like a fairly high number. Maybe I'm missing something around currency, but just if you kind of got to a per unit, how much is your COGS really up year-over-year?

**Matthew White** (Executives):
Duffy, it's Matt. So yes, I think there's a couple of moving parts there. So for the quarter, you got to start with FX, right? So that's up 1%. You could take that out, that will apply across all the lines. Cost pass-through is another 1%. As you imagine, that's also in there, given some of the energy that just grosses up, as you know, both sales and variable costs. In addition, as you saw, the energy market did quite strong, and a lot of that's on the back of HyCO, our hydrogen business, which tends to have, as you know, a higher variable cost just given the inputs for that business. That also is driving part of it. 
To your point, the acquisitions will come in, in that regard. And so a lot of that plays into that. But I would add that when we talked about some of this recovery we had to do, that partly plays into that as well. And maybe I can kind of take this point to talk a little bit about the pricing recovery. So this is something we mentioned last quarter that we were seeing these costs and we needed to go out and recover. That is a normal part of the business. That's something we do all the time. I would say it's a little more prominent this quarter for 2 primary reasons. The first is just we saw a more accelerated cost, both with distribution and power in the last few quarters as you read about some of the power situations, the weather and what we saw, especially in North America, that we needed to get out and recover. 
I would say, secondly, which is just more optics is as we move Lincare out of the Americas segment, while this recovery had always happened, it's going to look a little more pronounced now because you're taking Lincare out of the denominator of that calculation. So by default, you will see more elevated pricing and more prominent recovery in Americas, just given that function of the change. So I would say all of those played into that. We do expect that to kind of come back down here into the fourth quarter. But that's the reason we also needed to go out and recover some of that.

**Operator** (Operator):
Your next question comes from the line of John McNulty from BMO Capital Markets.

**John McNulty** (Analysts):
Regarding the charge that you took in terms of the severance side, so the non-Lincare portion of the restructuring and efficiency work that you're doing, I guess, can you help us to think about how that will play out going into 2027 in terms of the savings and the improved efficiency versus your kind of normal cadence that you call out most of the time in terms of efficiency improvements that we kind of know as a steady state?

**Matthew White** (Executives):
John, it's Matt. I can handle that. So I would start with the severance portion is very, very consistent with all of our prior actions we've taken. So as you may recall, the paybacks on a cash basis, undiscounted tend to be in the 1- to 2-year range. And that range is really a function of where in the world more of the severance occurred just based on certain contracts or sort of what the required severance would be. So I would say for this particular charge, it's probably closer to the higher 2-year end, but that will start taking effect here in the fourth quarter. But really, we'd expect to see the full benefits in the second half of next year on a full run rate basis. So that's pretty consistent with our other charges that we've had, 1.5- to 2-year payback, and you start to see full benefits within 3 to 4 quarters of the action itself.

**Operator** (Operator):
Your next question comes from the line of Vincent Andrews from Morgan Stanley.

**Vincent Andrews** (Analysts):
Matt, I wanted to ask you versus where we were at 2Q, when you look into the fourth quarter, where natural gas and electricity costs have gone in Europe, how much of an incremental headwind is that to you? And how much of it do you think you'll be able to price for in the fourth quarter versus having to wait to recover in the first quarter?

**Matthew White** (Executives):
Yes. So Vincent, I'll break it down between on-site and then the merchant and package. So on-site, it's recovered in the current month, and that's cost pass-through. So that would essentially be cost pass-through. When you think about merchant and package, which this North American impact is more related to, it generally can be anywhere from a 3- to 6-month sort of lag on recovery is what we tended to see. And I would say, in Europe, what we've seen in the past, and it really depends how it plays out this year is either it's a very cyclical up and down power, which means it's just a constant 3-, 4-, 5-month recovery lag that we continue to do until it stabilizes or you can have a continued power spike to the point it works into the entire inflation of the economy, which then it becomes essentially permanent price. We'll see how this one plays out. I would say when we saw this inflation spike in 2021, 2022, it was more sustained and became price, if you remember from our results then. This particular one has vacillated a little more, but we'll see how it plays out as we get into the winter months going ahead.

**Operator** (Operator):
Your next question comes from the line of Josh Spector from UBS.

**Joshua Spector** (Analysts):
I wanted to ask kind of simply here, just in terms of your EPS guidance versus what you just delivered, 9% growth versus 7% growth. What are the factors that drive the deceleration in fourth quarter versus 3Q? And what should we be inferring from fourth quarter as we look forward into 2027?

**Matthew White** (Executives):
Josh, it's Matt. So for 2027, we'll give that in February. So we'll stick with Q4 right now. And I think the best way to probably talk about it is sequentially to hopefully address your question. So if you take the midpoint, and obviously, time will tell where we deliver, but I'll just use the midpoint for simplicity's sake of the guidance range. It's about a 3% decline. 1% is FX, as we mentioned. Obviously, we're seeing the dollar strengthen across most currencies right now. So that's part of that. And time will tell, it will be what it will be when it ends up. 
Another percent, if you noticed, we had a little bit of elevated equity income this quarter and third quarter. And a lot of that was a customer true-up on a contract we were paid for that was resolved. And so that caused a bit of a spike in the equity income this quarter that will go back to run rates Q4. So that's roughly 1%. 
And the last percent, we'll see. I mean we do have a little bit of seasonality in Q4. As I mentioned, we're taking a pretty guarded view on the impact of some of the actions we're taking with both the non-gas business as well as our view on the economy right now. We're not going to take any view on continued sustained growth. But our goal is to do better than this range, and our goal is to work to get above it. But that's where we are right now. And we'll have to see. Obviously, we -- for most intents and purposes, we left the full year guide somewhat intact. And that was part of the thought process as well as laying out this Q4 guide to just leave that intact at this point because we didn't see a reason to take any bullish signals yet until we can kind of see how the rest of the economy plays out.

**Operator** (Operator):
Your next question comes from the line of James Hooper from Bernstein.

**James Hooper** (Analysts):
Can I get an update, please, on the Woodside project and when the component parts might start up and how the customer placing it on the strategic review might affect your business?

**Sanjiv Lamba** (Executives):
Thanks, James. So the Woodside project continues to make progress. When we last spoke to you, we were about to start up the air separation unit and start the nitrogen supplies. That is now underway already in Q3, and it will continue to progress for the rest of the year and into next year. We are also supplying the customer currently temporarily with hydrogen from our pipeline network, ensuring that they have an opportunity to continue to manufacture ammonia as they would want to. 
Now the ATRs, which is our on-site supply for hydrogen will get started up. There are 2 trains for the ATR. So there is always a staggered start-up. I expect that to be completed in the first half. And at the end of that 6-month period, we would then be at a point where all the facilities would be ready. And the only component left to be completed then would be the carbon capture and sequestration element, which is being worked on by ExxonMobil. So our time lines that we have communicated in the last call, I think, hold for now, and the teams are working to see what we can do and maybe even slightly improve that. So you'd only see that impact start to come through in the second half of next year. 
A quick reminder on those of you who looked at large projects like this, there is a ramp profile that always exists with projects like this on the ammonia side as well. So once we start up, then we will start going into that ramp process, which would mean there be a staggered capacity utilization of our plants until we get to that 100%, which I expect probably to be sometime in 2028. 
The conversations around the strategic review that the customer is doing, I think, will -- is something that they will have to complete. We are actively engaged with them. The only point I'd make to you is we always, in projects like this, assess the quality of the asset into which we supply, and we recognize that we have a really high-quality asset that's being supplied over here, which originally was owned by OCI, transferred to Woodside and irrespective of who the ultimate owner is, we believe this ammonia complex will have a very attractive opportunity for them to continue to make some money from the complex. So we feel good about our positioning with that asset as well.

**Operator** (Operator):
Your next question comes from the line of Matthew DeYoe from Bank of America.

**Matthew DeYoe** (Analysts):
I wanted to ask a little bit on volumes, both kind of structurally and then maybe in the quarter, starting with Europe. Sanjiv, I have a feeling what your answer will be, but are you getting any more optimistic that the Europeans are taking a bit more defensive view on industry there now with like steel antidumping and the auto import cap? Towards the quarter, it looks like volumes maybe got a little bit better in Europe in 3Q, but I don't know if that's just noise and comps on kind of what's still pretty much a tough market. And if I could tack on Europe saw a bit better performance than I would have expected on volumes. I feel like last time we caught up, there was some expectation of a deceleration in China, but maybe that doesn't feel as visible here in the print. So I want to give you an opportunity to kind of sound off on that stuff.

**Sanjiv Lamba** (Executives):
Thanks, Matt. You kind of almost predicted what my answer was going to be. So I'm not going to disappoint you sadly. Europe, unfortunately continues to be in that range that we talked about the last time we spoke. There is, at this point in time, no catalyst. Now I'm sure you've seen the 1% positive volume on Europe rounded up to 1%. But the reality is that unfortunately comes -- well, I shouldn't say unfortunately, but that comes largely on the back of sale of equipment, which has embellished that number, if you will, strip that out and the underlying number is flat. Now look, the comps have gotten better to your point, and that helps. But a flat number today for Europe actually is looking better than the minus 2, minus 3 that we've seen if you go back 12, 18 months ago. 
So there seems to be a degree of stability, but there is absolutely no catalyst, and I have absolutely no reason for any confidence that European market will pick up and give us any growth in the near-term. There is 0 catalyst. And I do not see the pragmatism that is needed across that whole European Union and the European community to take decisions that could get back industrial activity to a level where actually we start seeing some positive movement. So sadly, that disappointment will remain for some time until such decisions are taken. And I read the press as much as you do. And as I said before, nothing there suggests that, that trend is likely to change anytime soon. 
On China, you were right. In the last call, I said my expectation was a moderation in the second half. That played out for steel as an example. So steel production was down 2.5%. There is a curtailment -- production curtailment order from the government that's playing into steel. So steel is down, chemicals flat. The star of the show really has been electronics in China. And really, electronics industrial production has grown about 17% in the quarter, if I'm not wrong, and essentially driving a lot of the growth within that space. Beyond that, manufacturing also has been -- other than the green shoots that we previously referred to on EV and batteries, everything else has been rather down. Now the other point I want to make on China is the expectation was that exports would moderate, but it has been a fantastic export market in Q3. So that obviously has helped the economy a little bit. 
Domestic demand continues to not manifest itself at all. That remains my concern, to be honest. Sustained improvements in China require the domestic consumption to pick up alongside some level of export growth. We are just not seeing the domestic consumption pick up. I'll give you one number that surprised me. Domestic EV consumption or purchasing is down about 11%, 12% despite the fact that you're still seeing significant exports outside. At some stage, that export machine will face resistance at the other end, mostly Europe. And I think we'll see that moderate as well. So you know what, I'm not seeing any structural changes in China that are giving me confidence that we will see a significant rebound other than whatever forecast you might have on exports outside China into the rest of the world.

**Operator** (Operator):
Your next question comes from the line of Eric Boyes from Evercore ISI.

**Eric Boyes** (Analysts):
Does the Lincare restructuring savings take away from the usual productivity gain that's typically embedded in your normal earnings algorithm for 2027? Or will that typical productivity benefit come on top of Lincare for next year?

**Matthew White** (Executives):
Eric, it's Matt. It will be on top, right? The way we always view it is the productivity is an ongoing embedded in the culture. That is an expectation, and that is every day. These restructurings are more episodic onetime, and they're more top-down approaches that are incremental. So it's consistent with how we do the gas view as well that it will be incremental.

**Operator** (Operator):
Your next question comes from the line of Jeff Zekauskas from JPMorgan.

**Jeffrey Zekauskas** (Analysts):
It looked like helium prices moved up in Asia sequentially. Do they move up in the other geographic jurisdictions? 
And then for Matt, at least by my calculation, the decrease in Lincare EBIT in the first half was $66 million. And I know you said that it would -- Lincare would lower EPS growth by 2%, which would be about $200 million pretax. So are you rounding up? Is the number a little less than that?

**Sanjiv Lamba** (Executives):
Jeff, on helium, I'll let Matt answer the Lincare question. On helium, generally, we have seen prices up. You might recall, we had said in the last round as well that one of the things -- one of the actions we've taken as we've signed up some new contracts as well as we continue to serve all our contracted customers is that we have built in the pricing, some recoveries on the dislocation costs associated with the Middle East conflict and the sourcing and logistics challenges that we have. So we are seeing that rounded up in pricing. But of course, that is also rounded up in the cost structure. Therefore, the margin improvements don't quite show through on the helium and affect us more broadly. But clearly, we are seeing that pricing move up. And it is across the world, across all the markets in each of the segments we have. 
Matt, do you want to take the Lincare piece?

**Matthew White** (Executives):
Yes, sure. Jeff. Yes. So the -- obviously, you'll have the first half, you won't have the back half in Q3 and Q4 from that perspective spiked out. But it is about 1.5% to 2% on the year-to-date and especially when we kind of look out on holding flat what the Q4 would be. And part of that also is a function of how last year the performance was when you think about the baseline. So it is in that range, and that's the effect it's having. So whether you say it's 1.5%, 1.6% rounding how you want to look at that. But I would say it's a very strong 1 to a weak 2 is what we've seen on when we project out on the year just based on the numbers.

**Operator** (Operator):
Your next question comes from the line of Kevin McCarthy from Vertical Research Partners.

**Kevin McCarthy** (Analysts):
I was wondering if you could compare and contrast your price experience in the Americas versus your other major regions. I'm looking at plus 6% in the Americas and maybe half that in Asia and 1/3 of that in Europe. So maybe you can discuss why that's the case and whether we should continue to expect Americas to outpace ROW moving forward?

**Sanjiv Lamba** (Executives):
And I'll let Matt cover that just to get into the details of the Americas pricing, which has some recovery elements, which are beyond the quarter. Matt, why don't you just explain that?

**Matthew White** (Executives):
Yes. Sure, Kevin. So I think a couple of things. First, when you look at the 6%, I would say probably close to 2% associated with some of this recovery we talked about. So underlying run rate here in the 4% range. Globally, even excluding the recovery, we're still 3% because the 3% we have is a very strong 3%, I'll say, in terms of the global rollout. So the run rate there has probably been more in the 4% range, and that's kind of the year-to-date, if you look at it, too, through that period, excluding the 2%. And part of it is just you've seen both inflation and cost, but also general inflation. You have to remember, you have South America as well in that set of numbers where you tend to see a little higher inflation. You definitely have seen some power and distribution inflation in North America with the U.S. specifically. 
I think when you go over to EMEA, we are starting to see that pick up more. As I said earlier, it vacillated a bit. I think -- what we saw in EMEA, we would see some energy rise and then fall and rise and fall. So we would cover that through some surcharging, but it wasn't necessarily translating to significant incremental permanent pricing. But it feels like that may start to accelerate. Time will tell, but that's what we're starting to see in EMEA. 
And when you move to APAC right now, probably half of that pricing is helium, which relates more and [ Jeff ] alluded to seeing the helium price increases. The other half, we are seeing some good traction in South Pacific and places like India. But obviously, China, it's still not a high inflation region, as you can imagine. So that's continuing to put a little bit of a drag on the base business just given some of the conditions there. So I would say right now, even when you exclude this recovery we had, Americas continues to see the highest rate of inflation, just given the activity in North America and the traditional inflation you tend to see in South America.

**Sanjiv Lamba** (Executives):
Kevin, I'll only add that as we see this inflationary momentum continue to build, our pricing actions across the world. America is a great example as to how just Matt described it, but across the world, continue to be focus of attention for the management team at Linde. So including China, which is a lower inflation economy, I think for the first time after a number of quarters, we've seen positive inflation in China. Also export PPI is up, both indicators that the market is tuning into higher inflationary levels, and therefore, our pricing effort over there will continue to provide some further impact as well.

**Operator** (Operator):
Your next question comes from the line of Patrick Cunningham from Citi.

**Patrick Cunningham** (Analysts):
I was hoping you could elaborate a little bit more on any other reasons for logic of moving Lincare to the other segment, whether you're considering selling that business? And just any sort of update on the mitigation actions you plan to take? When can we expect a meaningful change in profit levels there?

**Matthew White** (Executives):
Patrick, it's Matt. I'll start with the move is driven by accounting, right, which is -- it's called CODM, the Chief Operating Decision Maker. And the combination of a series of accounting events, and I think it culminated with the trigger and the change of the executive leadership oversight and how we evaluate that business through management and the Board prompted that change to the other segment. So I think that was an accounting thing, which we'll set aside. But that being said, we absolutely, and we've said we will continue to evaluate strategic options, but we can't assure there will be a strategic option to be had. And so we have to improve this business. 
We have to run it better while running it safely and compliantly. And so that is the focus and that is the goal. Hopefully, the health care sector improves. Right now, it's not doing as well, I'll say, as a sector. But if it improves in the coming years and that market thaws a bit, maybe there can be more opportunities for strategic options. But our goal is to improve it. It is to basically make it a better business. And then hopefully, that will not only get rid of some of the headwinds we're seeing, but it will also open up other options with that business. And again, if you may recall, this is not too dissimilar if you go years back with the GIST business that traditionally was part of the EMEA segment. We had a very similar construct. We changed the oversight of it. We changed how we managed and reviewed that internally. It moved to the other segment. That business ended up a sale. We'll see what happens in this case.

**Operator** (Operator):
Your next question comes from the line of Abigail Eberts from Wells Fargo.

**Abigail Eberts** (Analysts):
Just another one on Woodside. Just wondering if there's anything else you can give us to help us size that revenue drag given those project updates.

**Matthew White** (Executives):
So Abigail, it's Matt. I think as far as a revenue drag, yes, the way I would probably characterize it is we are supplying them from our existing network. And as Sanjiv mentioned, without having the full assets up and running, those are molecules that we would have been able to route into our network system for other customers. As you can imagine, today in the U.S. Gulf Coast, hydrogen is a pretty valuable molecule because it helps desulfurize heavy crude, and it helps refiners make more middle distillates and products in high demand like ultra-low sulfur diesel and other products like that. So we would definitely have been able to resell those molecules and that's the same with some of the atmospherics as well. So I think it is something that we fully expect to be incremental when it starts up and that we will get that benefit. But right now, we are pulling those molecules from our existing supply network to support them until these assets are up and running.

**Operator** (Operator):
Your next question comes from the line of Alex Yefremov from Barclays.

**Aleksey Yefremov** (Analysts):
In Electronics, you've been growing mid- to high teens this year versus what I think MSI growth at 8% to 10%. Is this a sustainable level of outgrowth for the next few quarters? And separately, how do you feel about prospects of new additions to backlog in electronics?

**Sanjiv Lamba** (Executives):
Thanks, Aleksey. That's a great question on electronics and some of you, and I know, Aleksey, you were there were at our event in Phoenix and actually physically saw the conversations we have about electronics growth. So the growth that we saw in the quarter is really largely driven around organic growth in electronics, and I feel pretty good about the trend that we see at least for the next few quarters, looking out in terms of how that end market is going to perform for us. So feel good about that. I feel that this is something that we will sustain. The reason the confidence in the midterm also exists is because sitting within our backlog, as I mentioned briefly earlier on, we have about $2 billion of backlog projects under execution, which will have staggered start-ups over the course of the next 2, 3 years, and that will then feed into the double-digit growth that I expect from the electronics end market going forward. 
The other point I'd make around electronics also is that there is, in addition to the atmospherics, which is where most of our conversation has been and which is where the Phoenix assets, as an example, we had shown you were feeding into. We also have continuing growth around the electronic special gases. These tend to be the cylinder gases, high value, small volumes, but nonetheless, quite important. I think we continue to see growth over there as well. So between those 2 elements, I fully expect to see electronics growth in the double-digit rate going forward. 
Talking about prospects. So the point I'd make on prospects is twofold. Let me start off by just the conversations again that we had in Phoenix to illustrate that we have a robust pipeline of projects, including with TSMC here in the U.S., with some of the other players in the U.S., but also as we think about the top 10 electronics players, we have existing relationships with each of them across the world, whether it's Taiwan, South Korea, the U.S. And of course, there is a growing market I referenced earlier on in China that provides prospects as well. I expect Linde to win more than its fair share across that whole range, particularly when it comes to these larger atmospheric projects like the ones we showed you in Phoenix. So feel good about that whole prospect. 
I will say, though, that we are, as you know, very disciplined around capital allocation. And one of the things that we are playing into that has been our focus on logic. Obviously, we will do memory with some of our key customers that we have been working with for decades, but we tend to be a bit more selective around some of the memory projects and just recognizing the short cycle that memory tends to have might look different at the moment, but historically has been on a shorter cycle and which tends to be a little bit of variance to the long-term contracts that we prefer when we go out and do this level of business and project development.

**Operator** (Operator):
Your next question comes from the line of Salvator Tiano from KeyBanc Capital Markets.

**Salvator Tiano** (Analysts):
Just want to go back to the pricing, especially in the Americas, the 2% component you mentioned. So essentially, firstly, can you help us a little bit understand how much was the, I guess, excess margin from the price increase that was going to offset costs from prior quarters? So essentially, what was a little bit perhaps a little bit more one-off in the quarter? 
And secondly, it looks like some of the cyclical end markets in the U.S. and the Americas have been doing pretty well in terms of profitability. So how -- going back to Kevin's question, what do you think would have been your price power to recover these costs should conditions for these end markets have been more similar to the past few years where chemicals, earnings were poorer. Would you be able to recover them to that extent? And how should we think about future recoveries if earnings for chemicals and energy assets do not stay at current levels?

**Matthew White** (Executives):
Yes, Sal, it's Matt. So I think we'll just start with the basics. I think the recovery of cost is an integral part of our contracts. It's something we've always done. We mentioned last quarter, we needed to get out and get more recovery, especially in North America. So that aspect of it is very consistent. And this primarily relates to merchant and package just to make sure, because on-site, it's primarily cost pass-through, as you know. That is very much in the month, and it's very programmatic as part of the contract billing itself. Within the merchant and package, there are aspects of each contract to go and recover it, and we've always had this lag. And the lag can be 1, it could be 2 quarters. I would say this particular period, we saw an acceleration of cost that came a little faster. 
And of the margin itself, you got to spread it over probably 5, 6 months, if not more. So it's really hard to give a margin in any particular period because people want to break it down to quarters. But I will say on year-to-date, while it is still net in terms of the positive impact on OP, it will clearly be dilutive, right? Because you're basically going out there and trying to get back a lot of these excess inefficiencies and you're going to do it in a way that's going to be dilutive to the average American margins. So I would just say it's been spread over a couple of quarters for the most part, within the quarter itself, it would have still been net dilutive to the 35% margins that we printed just given the recovery portion. And it's something we will continue to do. 
And again, the fact that we've taken an annualized equivalent of Lincare sales of almost $2.3 billion annualized out of that segment kind of makes this a little more magnified simply because you have a smaller denominator to divide by, right? So I think that will be something going forward. And that's, again, part of the clarity and transparency. I think that will be a little easier with the way the segments are aligned today. But we will absolutely act again. And then some of this does turn into permanent pricing over time as it becomes an integral part of inflation within the economy itself. Time will tell if that happens. But right now, I feel very good about the 4% run rate on the underlying organic. And if inflation persists, then I expect in Americas, we will rise above that.

**Operator** (Operator):
Your next question comes from the line of Laurence Alexander from Jefferies.

**Laurence Alexander** (Analysts):
Two quick ones or hopefully quick. One is, what's the rough free cash flow that Lincare is contributing? 
And secondly, on the comments around kind of the European industrial policy, what's the feedback you're getting from customers as to how long this combination of malaise and cost pressures can continue before end markets need to shift to a more rapid deindustrialization strategy? I know Europe has a lot of stakeholders to coordinate before decisions get made. But is it a couple of years? Is it a decade? I mean do you have any sense or people talking yet about where the real breaking point might be?

**Sanjiv Lamba** (Executives):
So Laurence, I'll cover that, and then I'll ask Matt to cover the free cash flows on Lincare. You have probably on numerous calls, heard me, for lack of a better word, vent on the lack of consistent policy framework that allows industries in Europe to move forward and be competitive. And that is obviously compounded in the current climate with energy costs being both volatile as well as extremely high. When in parts of Europe, you have energy selling at EUR 150 per megawatt, that's for electricity. And when you have natural gas a couple of weeks ago, selling at EUR 30 per MMBtu, you know you have a structural cost disadvantage that the government needs to kind of understand how it can either offset, which some countries are trying or find a way to ease the ability to not have to comply with thousands of regulations and make the business a little bit more competitive to try and offset some of this inherent disadvantage that's there. 
There isn't a Europe per se. So if you see Scandinavia, we continue to see good industrial activity in Scandinavia. The Nordics have got the advantage of lower cost of power. It is hydroelectric power for most part, priced well, competing well, and we still see the prospect of growth and projects in the Nordics as a good example, where it's offset by significant disadvantage that sits in Continental Europe for most part. Eastern Europe is suffering because they are the back end of the supply chain that feeds into Continental Europe. Customers, much of my frustration that I'm reflecting over here is coming from conversations that I have with my peer CEOs of various companies. And I think I'll give you the example of chemicals where that has become quite visible. 
Now the Middle East conflict has helped in part to try and shore up some of the chemical industry across Europe. But clearly, a level of restructuring in that industry, which includes a number of shutdowns of facilities and specific sites, as you're aware, is all playing into this narrative. I don't think anyone has a time line, Laurence. You can take a guess. Any guess that you and I take will be wrong. It will take longer, whatever we might estimate. So I guess my frustration here just reflects that lack of activity that is allowing broader industries to both survive and do well. And I think that is -- certainly, I would not hold my breath for the medium term. 
Matt, do you want to cover the free cash flow?

**Matthew White** (Executives):
Sure. Yes, I'll start with Laurence. It's positive and it's been positive throughout the whole time. A kind of rough and simple way to think about it is the depreciation add back and the CapEx mostly offset. So your operating profit/EBIT essentially falls to the cash flow, free cash flow line. And so from that perspective, it's just a function of how you manage working capital. There is a seasonal element to working capital in this business based on how the deductibles and plan -- health care plan systems roll over. So that will create some noise within the quarters. But aside from that, the EBIT tends to be a rough proxy and then you just -- the better you can manage collections, the better you can manage that number.

**Operator** (Operator):
We will now take our final question from Tony Jones from Rothschild & Co.

**Tony Jones** (Analysts):
Just a quick one on helium. Do you expect any change to the Qatar supply situation in '27? And related to it, do you still think pricing will be positive for Linde next year? And what does that do to margin, if anything?

**Sanjiv Lamba** (Executives):
Thanks, Tony. You found a way to put in 3 questions in there, but I'm happy to respond to all of them. Helium has done -- look, as I said before, we've done a really good job. The team has done a really good job around managing the helium through this crisis period. And in doing that, not only have we served our existing customers extremely well, but we have added customers with long-term contract commitments that they've made to come on board, just recognizing the resilience of Linde's helium sourcing and supply chain that allows us to go out and ensure that we are able to serve their needs even at times like this. That has been good from a pricing perspective to address that issue. 
But our pricing actions have been very focused around ensuring that the dislocation costs that come with this increased supply chain and sourcing challenges are adequately factored into the pricing and recovered appropriately. We have not tried to use this opportunity to excessive pricing. We've been very mindful that these are long-term contracts, and I certainly want to make sure I time these molecules because longer-term, helium will be long. And we have gone through that cycle, and we know exactly where that's going to end up. So it has been important to get that done. 
Coming to Qatar specifically, our view is that Qatar is likely to get to about 75% of the production levels. The challenge is not on the production side, as you know, Tony. The challenge is the ability to get anything out unless you do a very convoluted supply chain using land routes and then get to ports, which are far off, which obviously add to both the complexity of having enough tanks that allow that helium to be carried across that very significant terrain that it needs to cross and then obviously getting ships that would then be able to take it to the rest of the world. All of that add both cost complexity, but most importantly, there aren't enough tanks in the system to be able to allow that rerouting to be effective longer-term for a sustained period of time. So I do expect -- and again, 2027 is -- your guess today is as good as mine, to be honest. And if you could give me a date by when the Strait of Hormuz issues would get resolved, I would tell you exactly what the helium would look like. But neither of us are in a position to do that today. 
All I can say to you is having the ability to source globally from various sources. I mean, we moved about 340 containers in the last quarter. That is pretty significant, and we moved it from all over the world between our sources in the U.S. to our sources in North Africa, to our sources in Europe and some sources in Asia. And I think that managing that whole supply chain has been really the strength of Linde's ability to meet customer requirements and has played into that resilience that we often talk about. I'm looking forward to seeing normalization happen out of Qatar, and that will, of course, provide a fillip to our efforts to place even more molecules into the marketplace, having now signed these long-term contracts.

**Operator** (Operator):
I would now like to turn the call back to Juan Pelaez for any additional or closing remarks.

**Juan Pelaez** (Executives):
Thank you, everyone, for participating. Have a great day.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LIN_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CFO｜guidance：全年 EPS 指引區間更新為 17.70–17.90 美元（原話："The updated full year range is $17.70 to $17.90"）
- 2026-07-31｜CFO｜guidance：第三季 EPS 指引區間 4.45–4.55 美元（原話："Third quarter guidance range is $4.45 to $4.55"）
- 2026-07-31｜CFO｜guidance：指引區間中點假設經濟無改善（原話："the range assumes no economic improvement at the midpoint"）
- 2026-07-31｜CFO｜guidance：基礎量能回升尚未納入下半年指引，需再觀察數季（原話："we'd like a few more quarters under our belt"）
- 2026-07-31｜CFO｜guidance：Q2 到 Q3 排除匯率後 EPS 中點增加 0.05 美元（原話："increase $0.05 at the midpoint when excluding FX"）
- 2026-07-31｜CEO｜guidance：2027 年 EPS 成長以 8%–12% 演算法為基準，不需總經改善；正式指引年底至明年初再給（原話："We're not looking for macro."）
- 2026-07-31｜CEO｜guidance：管理層指 EPS 演算法為 8% 至 12%（原話："we should be delivering 8% to 12%"）
- 2026-07-31｜CFO｜guidance：氦氣假設未變動：指引維持不變（原話："we left the guidance intact"）
- 2026-07-31｜CEO｜guidance：管理層對總經採中立立場，交由投資人自行判斷（原話："we have taken a neutral stand"）
- 2026-07-31｜CFO｜margin：Q2 營業利益率 29.5%，年減 60bp（排除成本轉嫁為 30bp）（原話："Operating margins of 29.5% decreased 60 basis points"）
- 2026-07-31｜CEO｜margin：CEO 表達對本季利益率不滿意（原話："we are not satisfied with our margin performance"）
- 2026-07-31｜CFO｜margin：CFO 說明美國居家醫療（Lincare）拖累美洲利益率，排除後利益率將上升（原話："Excluding this, margins would have increased."）
- 2026-07-31｜CFO｜margin：APAC 利益率下滑歸因於電子客戶的低毛利設備銷售（原話："APAC erosion is mostly due to lower margin equipment sales"）
- 2026-07-31｜CFO｜margin：管理層預期多項利益率逆風為暫時性（原話："we expect many of these margin headwinds to be temporary"）
- 2026-07-31｜CFO｜margin：氦氣定價改善但因調度成本，利潤率層面暫時稀釋；美元貢獻為正（原話："that grossing up effect right now is a little bit dilutive"）
- 2026-07-31｜CFO｜margin：CFO 估 Lincare 拖累約比分析師估算（Q2 約 3,000 萬）高 30%（原話："probably say 30% higher than that number, give or take"）
- 2026-07-31｜CEO｜margin：Lincare 面臨勞動成本通膨與給付環境變化的持續逆風（原話："persistent headwinds, right, from labor cost inflation"）
- 2026-07-31｜CFO｜margin：Q2 價格 +2%，與當地通膨大致同步；Lincare 定價不足（原話："The price increase of 2% was broad-based"）
- 2026-07-31｜CFO｜margin：回測：2025 年上半年利益率強、下半年弱，全年年比較基期有利（原話："I'm fully expecting us to see better year-over-year"）
- 2026-07-31｜CEO｜margin：回溯項目的利益率隨產能利用率爬升而改善（原話："I always expect backlog projects to continue to improve"）
- 2026-07-31｜CEO｜commitment：CEO 承諾第三季利益率環比改善（原話："I fully expect sequential improvement into the third quarter"）
- 2026-07-31｜CFO｜commitment：CFO 表示本季將採取成本行動，並於十月電話會議提供更多細節（原話："we will likely look to take some cost actions this quarter"）
- 2026-07-31｜CFO｜commitment：CFO 預告下次（十月）電話會議將說明已採取的行動（原話："what we've done in the October call"）
- 2026-07-31｜CEO｜commitment：CEO 預期年底 sale-of-gas 在手訂單仍維持 8 開頭（億美元級 80 億以上）（原話："backlog to finish the year with an 8 handle"）
- 2026-07-31｜CEO｜commitment：管理層預期氦氣回收在未來數季反映於利益率（原話："I fully expect that it will over the next couple of quarters"）
- 2026-07-31｜CEO｜commitment：太空市場於 2030 年前達 10 億美元的目標維持不變（原話："we are on track for that $1 billion opportunity"）
- 2026-07-31｜CFO｜commitment：管理層表示組織承諾達成股東期待（原話："We know our owners expect more"）
- 2026-07-31｜CFO｜capital_allocation：年初至今已部署 60 億美元資本（原話："Year-to-date, we've deployed $6 billion of capital"）
- 2026-07-31｜CFO｜capital_allocation：預期已確保成長性資本支出將持續為重大資金用途（原話："we expect this number to remain a significant use of capital"）
- 2026-07-31｜CFO｜capital_allocation：營運現金流因工程業務時點偏弱，預期下半年回升（原話："we expect the second half to step up like prior years"）
- 2026-07-31｜CFO｜capital_allocation：CapEx 預期上調，來自新增專案與商業太空基礎 CapEx（原話："The CapEx number on the estimate was bumped up."）
- 2026-07-31｜CEO｜capital_allocation：投資標準為稅後兩位數無槓桿 IRR（原話："post-tax double-digit IRR -- unlevered IRR perspective"）
- 2026-07-31｜CFO｜capital_allocation：專案決策依 IRR，不依營收或利益率（原話："we make our decisions on IRR"）
- 2026-07-31｜CEO｜capital_allocation：CEO 表示正評估美國居家醫療業務的策略定位（部分或整體）（原話："evaluate the strategic fit of this U.S. homecare business"）
- 2026-07-31｜CEO｜capital_allocation：已有 Lincare 策略選項評估並行於改善行動（原話："evaluating what the strategic options for this business are"）
- 2026-07-31｜CEO｜customer：電子業 Q2 年增 18%，預期動能延續下半年（原話："had 18% growth in second quarter"）
- 2026-07-31｜CEO｜customer：Q2 新增 10 億美元電子業新單，支援美國西部先進製程晶圓廠（原話："we added $1 billion of new electronics wins to the backlog"）
- 2026-07-31｜CEO｜customer：台灣合資公司另有約 8 億美元電子業投資，未計入 backlog（原話："invest approximately $800 million to build, own and operate"）
- 2026-07-31｜CEO｜customer：航太占製造業成長逾 1/3（原話："aerospace accounted for more than 1/3"）
- 2026-07-31｜CEO｜customer：氦氣方面簽下新長約客戶（原話："signed up new customers with long-term contracts"）
- 2026-07-31｜CFO｜customer：電子業營收／CapEx 比與前幾期相似，區間 20%–50%（原話："revenue has ranged anywhere from 20% to 50%"）
- 2026-07-31｜CFO｜competition：部分商業太空客戶有垂直整合（自購工廠）意願，僅限大氣氣體，氫氣側未見（原話："a desire to vertically integrate"）
- 2026-07-31｜CFO｜competition：預期商業太空客戶將混合 sale of gas 與 sale of plant（原話："you'll see a blend of sale of gas and some sale of plant"）
- 2026-07-31｜CEO｜product：氦氣在卡達重啟與供應鏈到位後，預期正常化進度較慢，今年不會正常化（原話："I don't think you will see normalization this year."）
- 2026-07-31｜CEO｜product：亞洲台灣與韓國皆有強勁電子業專案管線（原話："see strong pipelines in Taiwan and Korea as well"）
- 2026-07-31｜CEO｜risk：中東危機使依賴當地碳氫化合物的亞洲國家縮減工業活動（原話："have had to scale back industrial activity"）
- 2026-07-31｜CEO｜risk：地緣政治事件可能影響化學與能源市場（原話："geopolitical events that could impact one way or the other"）

### 問答異常語氣（迴避／改口／保留）
- LIN_Q2_2026_Earnings_Call_20260731.md｜問：Laurent Favre 問美國居家醫療業務目前是否獲利、拖累有多大｜答法：未直接回答是否獲利；改談排除 Lincare 後美洲利益率 +20bp、氣體業務表現良好與硬貨組合
- LIN_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Zekauskas 問是否已決定出售 Lincare、決策時程為何｜答法：未回答是否出售或時程；僅說同步評估策略選項並「with diligence」
- LIN_Q2_2026_Earnings_Call_20260731.md｜問：David Begleiter 追問 2027 年氦氣是否為順風｜答法：未確認順風；僅答氦氣將正常化，並稱需 wait and see，量價組合複雜
- LIN_Q2_2026_Earnings_Call_20260731.md｜問：Duffy Fischer 問荷莫茲海峽解決後一年後的影響｜答法：拒絕推測明年狀況，稱先看海峽問題如何解決

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
{"status":"no_prior_dd"}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LIN_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
