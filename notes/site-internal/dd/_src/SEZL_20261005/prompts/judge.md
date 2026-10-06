你是 stock-analyst **v20 判斷 agent**，標的 SEZL（20261005）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
  *eps
    *bull[]: arr ≥1 num
    *base[]: arr ≥1 num
    *bear[]: arr ≥1 num
  *pe
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
- `counter_evidence.blind_spots[].view`：論點失敗｜論點成功但股東經濟變差｜價格已反映太多
- `decision_inputs.signal`：A+｜A｜B｜C｜X
- `decision_inputs.ma`：🟢｜✅｜🟡｜🟠｜❌｜-
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
{"meta":{"ticker":"SEZL","date":"2026-10-05","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261005/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261005/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenue_gaap","label":"Total revenue (GAAP)","value":149.7,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"市場彙整稿稱優於預期約 $14.6M（預期約 $135.1M；二手來源，未經 IR 稿驗證）"},{"id":"f_kpi1_gaap_operating_income","label":"GAAP operating income","value":55.0,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi2_net_income_gaap","label":"Net income (GAAP)","value":40.8,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi3_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未揭露 Non-GAAP 營業利益，以此代替）","value":58.0,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi4_free_cash_flow","label":"Free cash flow（僅上半年累計，無單季）","value":140.4,"period":"H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi5_stock_based_compensation","label":"Stock-based compensation（僅上半年累計）","value":3.4,"period":"H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi6_full_year_2026_guidance","label":"Full-year 2026 guidance（上調）","value":185.0,"period":"Q2 FY2026（公告於 2026-08-06）","unit":"USD million（Adjusted net income）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"Adjusted EPS 指引 $5.25 vs 站內共識 FY1 EPS $5.26（consensus_revision，口徑未必相同）"},{"id":"f_kpi7_active_subscribers","label":"Active subscribers","value":854000,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"人","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_kpi8_gross_merchandise_volume","label":"Gross merchandise volume (GMV)","value":1.3,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","unit":"USD billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）","citation":"公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）"},"note":"查無"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-06","period":"2026-08-06","unit":"date","basis":"距今 42 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-06"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_sezl_gross_margin_pct","label":"SEZL 毛利率","value":72.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SEZL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sezl_operating_margin_pct","label":"SEZL 營業利益率","value":37.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SEZL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sezl_fcf_margin_pct","label":"SEZL FCF 利潤率","value":51.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SEZL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_afrm_gross_margin_pct","label":"AFRM 毛利率","value":68.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_afrm_operating_margin_pct","label":"AFRM 營業利益率","value":20.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_afrm_fcf_margin_pct","label":"AFRM FCF 利潤率","value":23.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pypl_gross_margin_pct","label":"PYPL 毛利率","value":45.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pypl_operating_margin_pct","label":"PYPL 營業利益率","value":18.41,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pypl_fcf_margin_pct","label":"PYPL FCF 利潤率","value":19.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":110.85,"period":"2026-10-05（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-05（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":68.46,"period":"2026-10-05（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-05（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":37.57,"period":"2026-10-05（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-05（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.26 → 5.26）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.65 → 6.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.95 → 7.95）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.26,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.65,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.95,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":3.14,"period":"2026-06-23 → 2026-09-26","unit":"%","basis":"FY1 共識 EPS 5.1 → 5.26（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":24.31,"period":"2026-10-05（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-05（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-05（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-05（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":7.02,"period":"2026-10-05（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-05（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-05（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-05（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":7.1,"period":"2026-10-05（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-05（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-05（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-05（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":20.42,"period":"2026-09-26","unit":"x","basis":"分母＝FY1 EPS 5.26，分子＝快照價 107.41","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-26"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-10-05","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-05","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 107.41 / W52 95.35 / W104 85.37 / W250 None / W250 13週斜率 None%"},{"id":"f_ma_w52","label":"52 週均線","value":95.35,"period":"2026-10-05","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-05","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":85.37,"period":"2026-10-05","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-05","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Sezzle CEO 稱 BNPL 份額主要來自區域銀行而非 BNPL 同業；Sezzle 短天期放款模型營業利益率 61%、ROE 91.9%，高於較長天期的 Affirm、Klarna（搜尋摘要轉述）","source":"24/7 Wall St.: Sezzle CEO Says BNPL Market Share Is Coming From Regional Banks, Not Rivals, as Stock Soars 150% YTD","url":"https://247wallst.com/investing/2026/06/26/sezzle-ceo-says-bnpl-market-share-is-coming-from-regional-banks-not-rivals-as-stock-soars-150-ytd/","excerpt":"Sezzle CEO Says BNPL Market Share Is Coming From Regional Banks, Not Rivals, as Stock Soars 150% YTD","as_of":"2026-06-26","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Fed 資料：2025 年美國六大 BNPL 業者發放信貸 $156.7B；Afterpay/Block $53.7B、Affirm $41.3B、PayPal $26.5B、Klarna $23.9B、Sezzle $3.9B（Sezzle 約 2.5%，為六家中規模最小之一；彙總站轉述，非 Fed 原頁）","source":"Chargeflow 彙整 Federal Reserve 2025 credit issuance 數據；Fed FEDS Note 2026-06-05","url":"https://www.federalreserve.gov/econres/notes/feds-notes/buy-now-pay-later-beyond-pay-in-4-a-comprehensive-product-overview-20260605.html","excerpt":"Sezzle reported 3.05 million active consumers and $3.94 billion in gross merchandise volume for 2025.","as_of":"2026-06-05","retrieved_at":"2026-10-05","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 Sezzle 營收 +29%、淨利 +42%；訂閱戶 +76.4%、交易筆數 +32%、季 GMV +38% YoY（搜尋摘要轉述）","source":"搜尋彙整（Yahoo Finance／StockStory 等）","url":"https://finance.yahoo.com/markets/stocks/articles/sezzle-shares-tumble-despite-strong-123845759.html","excerpt":"Sezzle Shares Tumble Despite Strong Quarter as Growth Outlook Disappoints","as_of":"2026-08-01","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"2026 Q2 財報優於預期但警告下半年營收成長放緩，盤前股價跌 23%（as_of 為約略月份，確切日期未讀到）","source":"Yahoo Finance: Sezzle Shares Tumble Despite Strong Quarter as Growth Outlook Disappoints","url":"https://finance.yahoo.com/markets/stocks/articles/sezzle-shares-tumble-despite-strong-123845759.html","excerpt":"Sezzle Shares Tumble Despite Strong Quarter as Growth Outlook Disappoints","as_of":"2026-08-01","retrieved_at":"2026-10-05","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"競爭威脅：搜尋摘要指 Chase、Citi 等銀行發展 BNPL 產品（信用卡額度轉分期、固定手續費），以及 Apple、PayPal 等大型科技整合先買後付；Affirm、Klarna、Afterpay 規模與零售整合較深（二手彙整，未見具名 2026 新進入者）","source":"搜尋彙整（businessmodelcanvastemplate 等）","url":"https://businessmodelcanvastemplate.com/blogs/competitors/sezzle-competitive-landscape","excerpt":"What is Competitive Landscape of Sezzle Company?","as_of":"2026-08-01","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Sezzle 8-K（2026-05）披露的融資concentration limit：單一商家（Target Corporation 除外）上限 15.0%，Target 上限 35.0%，顯示 Target 為最大商家集中點。","source":"Sezzle Inc. Form 8-K FY2026 (ex10.1, 2026-05-07)","url":"https://www.sec.gov/Archives/edgar/data/0001662991/000166299126000071/sezl-20260507ex1001.htm","excerpt":null,"as_of":"2026-05-07","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"搜尋未找到 Target 與 Sezzle 協議續約、導入第二 BNPL 供應商或 Target 自建 BNPL 的任何報導。","source":"WebSearch 結果（無相關條目）","url":null,"excerpt":null,"as_of":"2026-10-05","retrieved_at":"2026-10-05","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 披露：2025 與 2024 年度無任何外部單一對象占總營收達 10% 以上。","source":"Sezzle 10-K FY2025（經 StockTitan 摘要頁讀取）","url":"https://www.stocktitan.net/sec-filings/SEZL/10-k-sezzle-inc-files-annual-report-701e205530f4.html","excerpt":"For the years ended December 31, 2025 and 2024, no external party amounted to ten percent or more of our total revenue.","as_of":"2026-02-26","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"對照：FY2022 有單一商家約占總收入 14%；FY2021 無商家超過 10%。（歷史資料，非現況）","source":"Sezzle 10-K FY2022 / FY2023 S-1 披露（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000121390023022123/ea175545-s1_sezzleinc.htm","excerpt":null,"as_of":"2023-03-01","retrieved_at":"2026-10-05","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"美國 BNPL 市場預測 2026 年 $111.6B（+14.7%）、2027 年 $124.8B（+11.9%），成長率自 2025 年 20.4% 逐年放緩；來源敘述放緩反映市場成熟而非景氣疲弱。","source":"SaleHoo / eMarketer 彙整：US Buy Now, Pay Later Market Size (2023-2027)；BNPL growth is slowing as the industry matures","url":"https://www.salehoo.com/learn/us-bnpl-market-size","excerpt":"In 2026, the US BNPL market is projected at $111.6 billion (+14.7%), and $124.8 billion in 2027 (+11.9%).","as_of":"2026-01-01","retrieved_at":"20261005","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Sezzle 2026 Q1：活躍訂閱用戶 714,000（+48.4% YoY）、活躍消費者 3.1M（+13.6%）、交易筆數 9.9M（+35.8%）；季均購買頻率 7.1 次（去年同期 6.1）。","source":"Sezzle Reports First Quarter 2026 Results（Seeking Alpha PR／Nasdaq 彙整）","url":"https://seekingalpha.com/pr/20504067","excerpt":"In the first quarter of 2026, active subscribers rose 48.4% year over year to 714,000, while the combined total of monthly on-demand users and subscribers reached 887,000, up 34.8%.","as_of":"2026-05-01","retrieved_at":"20261005","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Sezzle 面臨企業級商家費率的顯著競爭壓力；2025-03 Klarna 取代 Affirm 成為 Walmart 獨家 BNPL 供應商，顯示供給端競爭仍在重分配。","source":"CSIMarket SEZL Competitors／Business Strategy Hub 彙整搜尋摘要","url":"https://csimarket.com/stocks/SEZL-Competitors","excerpt":"Sezzle faces significant competitive pressure on merchant fees, particularly from enterprise merchants","as_of":"2026-01-01","retrieved_at":"20261005","affects":["decision_inputs.bear","thesis.R","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"Sezzle 是原告：其對 Shopify 的反壟斷訴訟（明尼蘇達聯邦地方法院）2026-05 裁定部分駁回 Shopify 的駁回動議，Sherman Act 核心主張續行，不當搭售（tying）主張被無偏見駁回。","source":"GlobeNewswire: Sezzle Provides Update on Antitrust Case Against Shopify","url":"https://www.globenewswire.com/news-release/2026/05/12/3293417/0/en/sezzle-provides-update-on-antitrust-case-against-shopify.html","excerpt":"Sezzle's core antitrust claims against Shopify under the Sherman Act will proceed, while an unlawful tying claim was dismissed without prejudice.","as_of":"2026-05-12","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"CFPB 利用監理與資料蒐集權限，向包含 Sezzle 在內的六家 BNPL 業者取得 pay-in-four 貸款資料；另有說法稱 CFPB 已撤回先前對 BNPL 的限制性規則，監管壓力暫時緩和。","source":"Richmond Fed Economic Brief: Buy Now, Pay Later: Recent Developments and Implications（搜尋摘要）","url":"https://www.richmondfed.org/publications/research/economic_brief/2026/eb_26-05","excerpt":"The CFPB used its supervisory and data-collection authority to obtain detailed pay-in-four loan data from six leading BNPL providers: Affirm, Afterpay, Klarna, PayPal, Sezzle and Zip.","as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"有律所公告調查 Sezzle 等 BNPL 業者是否就逾期費、付款時點、透支風險或分期真實成本誤導消費者（非政府機關調查）。","source":"Migliaccio & Rathod LLP: Sezzle Buy Now Pay Later Investigation","url":"https://classlawdc.com/2026/07/07/sezzle-buy-now-pay-later-investigation/","excerpt":"A law firm is investigating whether Sezzle and similar Buy Now, Pay Later companies mislead consumers about late fees, payment timing, overdraft risks, or the true cost of installment purchases.","as_of":"2026-07-07","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"多家律所2026-05公告調查 Sezzle 及部分高管／董事是否涉證券詐欺或其他不當行為（證券訴訟調查，非反壟斷）。","source":"Pomerantz Law Firm via Morningstar/PR Newswire","url":"https://www.morningstar.com/news/pr-newswire/20260514dc60536/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-sezzle-inc-sezl","excerpt":null,"as_of":"2026-05-14","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#none","axis":"reg_tariff_export","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"SEZL 10-K 風險因子：與發卡銀行夥伴的協議為非獨家，且在特定事件發生時發卡夥伴可終止（融資/發卡環節的單點依賴）。","source":"Sezzle Inc. Form 10-K FY2025（SEC EDGAR）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"SEZL 10-K 風險因子：重要供應商含雲端資料儲存、IT 方案與支付處理；服務中斷或供應商錯誤可能使其無法處理交易或入帳。","source":"Sezzle Inc. Form 10-K FY2025（SEC EDGAR）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"SEZL 10-K 風險因子：相當比重的業務與交易量集中在少數大型電商平台，任一平台不再合作或轉投競爭者會不成比例地衝擊公司。","source":"Sezzle Inc. Form 10-K FY2025（SEC EDGAR）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Sezzle CEO 稱 BNPL 市佔主要來自區域銀行與信用合作社，而非其他 BNPL 業者","source":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/06/26/sezzle-ceo-says-bnpl-market-share-is-coming-from-regional-banks-not-rivals-as-stock-soars-150-ytd/","excerpt":"Sezzle CEO Says BNPL Market Share Is Coming From Regional Banks, Not Rivals, as Stock Soars 150% YTD","as_of":"2026-06-26","retrieved_at":"2026-10-05","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Sezzle 風險揭露稱 BNPL 與其他替代支付產品的採用增加，可能吸引大型金融機構、卡網與科技公司進入，對方規模與品牌較強，可能迫使 Sezzle 降低商家費率或加碼誘因。","source":"gloom.sh Sezzle 2026 risk factors（搜尋摘要，轉述 Sezzle 風險因子）","url":"https://gloom.sh/stocks/sezl/risk-factors/2026","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Sezzle 以產品擴張回應：6 月推出 SezzleCash、8 月推出 Sezzle Send，並於 2026 推出內嵌 AT&T 網路的 Sezzle Mobile 手機方案。","source":"Sezzle Inc. Form 8-K Ex.99.1（2026 Q2 業績新聞稿）","url":"https://www.sec.gov/Archives/edgar/data/0001662991/000166299126000124/sezl-20260806ex9901.htm","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q1 2026 活躍訂閱用戶 714,000，年增 48.4%；訂閱＋隨選月付用戶合計 887,000，年增 34.8%；季均購買頻率 7.1 次（前年 6.1 次）。搜尋摘要稱此為由單次 BNPL 交易轉向訂閱式經常性收費關係，並以 Sezzle Anywhere 虛擬卡擴大可用商家範圍。","source":"Yahoo Finance / Zacks 摘要：Sezzle Recasts BNPL Model With Subscriptions Sezzle Anywhere And Eased Rules","url":"https://finance.yahoo.com/news/sezzle-recasts-bnpl-model-subscriptions-132212461.html","excerpt":null,"as_of":"2026-05-01","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"搜尋摘要稱 Sezzle 商家開發由量取向轉為優先大型企業商家；Q2 2026 新增企業商家含 Poshmark、Gymshark、Debenhams、Brookshire's、RockAuto。","source":"TradingView/Zacks：SEZL's Merchant Acquisition Strategy Vital for Its Growth Trajectory；Investing.com：Sezzle Q2 2026 slides","url":"https://www.tradingview.com/news/zacks:523b0aa6b094b:0-sezl-s-merchant-acquisition-strategy-vital-for-its-growth-trajectory/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FY2025 Q4 財報（發布日 2026-02-25）：新增 134,000 名隨選月付與訂閱用戶，總數 918,000；2026 計畫包含更高信用額度的長期借貸與更廣商家接受度。","source":"PYMNTS：Sezzle GMV Surges as Super App Plans Advance","url":"https://www.pymnts.com/earnings/2026/sezzle-gmv-surges-as-super-app-plans-advance/","excerpt":"Sezzle also added 134,000 new Monthly On-Demand and Subscribers during the quarter, bringing the total to 918,000.","as_of":"2026-02-25","retrieved_at":"2026-10-05","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 後公司給 FY2026 EPS 指引 $5.25、營收指引 $607.9M；MarketBeat 載共識 EPS $5.11、營收 $596.0M，指引高於當時共識。","source":"MarketBeat: Sezzle (NASDAQ:SEZL) Releases FY 2026 Earnings Guidance","url":"https://www.marketbeat.com/instant-alerts/sezzle-nasdaqsezl-releases-fy-2026-earnings-guidance-2026-08-06/","excerpt":"Sezzle (NASDAQ:SEZL) Releases FY 2026 Earnings Guidance","as_of":"2026-08-06","retrieved_at":"2026-10-05","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 2026 年連續上調指引：Q1 後總營收成長由 25-30% 上調至 30-35%、調整後淨利 $180.0M；Q2 後調整後淨利由 $180.0M 上調至 $185.0M，調整後稀釋 EPS 由 $5.10 上調至 $5.25。","source":"Yahoo Finance / Sezzle Reports Second Quarter 2026 Results 與搜尋彙整（Q1 稿 GlobeNewswire 2026-05-06）","url":"https://finance.yahoo.com/markets/stocks/articles/sezzle-reports-second-quarter-2026-200100451.html","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-10-05","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"賣方 2026 年共識與指引接近：EPS 預期 $5.24（指引 $5.25）；營收平均預估 $608.94M（區間 $605.8M–$613M）；近 30 天 6 次上修、0 次下修。聚合站抓取，確切 as_of 未標明。","source":"Yahoo Finance analysis 與 MarketBeat 搜尋彙整","url":"https://finance.yahoo.com/quote/SEZL/analysis/","excerpt":null,"as_of":"2026-09-25","retrieved_at":"2026-10-05","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布因來源而異：The Cerbat Gem 標題載平均目標價 $146.50（2026-09-25）；其他聚合站為 12 個月平均 $171.60（高 $196／低 $155）、S&P Global 7 位分析師平均 $168（區間 $150–$196）、WallStreetZen $158.29。各站 as_of 不一，未見明確日期；評等 6 位分析師 Moderate Buy（25% Strong Buy、25% Buy、50% Hold）。","source":"The Cerbat Gem; StockAnalysis; WallStreetZen; Public.com 搜尋彙整","url":"https://www.thecerbatgem.com/2026/09/25/sezzle-inc-nasdaqsezl-stock-has-average-target-price-of-146-50.html","excerpt":"Sezzle Inc. (NASDAQ:SEZL) Stock Has Average Target Price of $146.50","as_of":"2026-09-25","retrieved_at":"2026-10-05","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2025-06-09 Sezzle 對 Shopify 提起聯邦反壟斷訴訟（Sezzle 為原告）","source":"SEC 8-K 2025-06-09 ex99.1（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299125000132/szl-20250609ex9901.htm","excerpt":"on June 9, 2025, Sezzle sued Shopify, alleging in a federal lawsuit that Shopify's e-commerce marketplace damaged its business and violated antitrust laws.","as_of":"2025-06-09","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-04-30 起多家律所（Pomerantz、Schall、Levi & Korsinsky、Block & Leviton、Lowey Dannenberg 等）公告調查 Sezzle 是否涉證券詐欺；為調查公告，非已提起之集體訴訟","source":"Pomerantz 新聞稿（Morningstar/PR Newswire）","url":"https://www.morningstar.com/news/pr-newswire/20260430dc48764/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-sezzle-inc-sezl","excerpt":"Pomerantz LLP is investigating claims on behalf of investors of Sezzle Inc. (NASDAQ: SEZL), concerning whether Sezzle and certain of its officers and/or directors have engaged in securities fraud or other unlawful business practices.","as_of":"2026-04-30","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026-04-09 SEC 文件揭露董事 Karen Webster（審計與風險、薪酬、提名治理委員會成員）立即請辭，理由為與管理層在公司方向、關鍵決策與治理上的觀點分歧","source":"Sezzle 8-K（2026-04-09）／律所公告引述","url":"https://www.globenewswire.com/news-release/2026/05/22/3300322/0/en/sezzle-inc-nasdaq-sezl-investigated-for-potential-federal-securities-laws-violations-lowey-dannenberg-p-c.html","excerpt":"she resigned from her position as a member of the board, citing a growing difference in perspective with management concerning the Company's direction, key decisions, and governance.","as_of":"2026-04-09","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"多家律所自 2026-04 起公告調查 Sezzle 證券詐欺；本次搜尋未見已提起之集體訴訟","source":"Pomerantz 新聞稿（Morningstar/PR Newswire）","url":"https://www.morningstar.com/news/pr-newswire/20260430dc48764/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-sezzle-inc-sezl","excerpt":"Pomerantz LLP is investigating claims on behalf of investors of Sezzle Inc. (NASDAQ: SEZL), concerning whether Sezzle and certain of its officers and/or directors have engaged in securities fraud or other unlawful business practices.","as_of":"2026-04-30","retrieved_at":"20261005","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"2025-06-09 Sezzle 作為原告對 Shopify 提反壟斷訴訟","source":"SEC 8-K 2025-06-09 ex99.1（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/1662991/000166299125000132/szl-20250609ex9901.htm","excerpt":"on June 9, 2025, Sezzle sued Shopify, alleging in a federal lawsuit that Shopify's e-commerce marketplace damaged its business and violated antitrust laws.","as_of":"2025-06-09","retrieved_at":"20261005","affects":["moat_trend"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SEZL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.36,"operating_margin_pct":37.78,"fcf_margin_pct":51.12,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SEZL","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AFRM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.07,"operating_margin_pct":20.44,"fcf_margin_pct":23.3,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AFRM","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PYPL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.75,"operating_margin_pct":18.41,"fcf_margin_pct":19.3,"rd_intensity_pct":9.51},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"SEZL"},"financial_history":{"ticker":"SEZL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":125570441.0,"revenue_yoy_pct":null,"gross_margin_pct":19.89,"operating_margin_pct":-38.25,"net_income":-38093756.0,"diluted_eps":-1.14,"free_cash_flow":7503771.0,"fcf_margin_pct":5.98,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":159356772.0,"revenue_yoy_pct":26.91,"gross_margin_pct":46.3,"operating_margin_pct":13.93,"net_income":7098022.0,"diluted_eps":0.208333,"free_cash_flow":-27056025.0,"fcf_margin_pct":-16.98,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":271128000.0,"revenue_yoy_pct":70.14,"gross_margin_pct":56.89,"operating_margin_pct":25.26,"net_income":78522000.0,"diluted_eps":2.188333,"free_cash_flow":129184000.0,"fcf_margin_pct":47.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":450279000.0,"revenue_yoy_pct":66.08,"gross_margin_pct":70.06,"operating_margin_pct":36.15,"net_income":133130000.0,"diluted_eps":3.72,"free_cash_flow":207212000.0,"fcf_margin_pct":46.02,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SEZL/SEZL_Q2_2026_Earnings_Call_20260806.md）

# Q2 2026 Earnings Call
2026-08-06

Q2 2026 Earnings Call
Sezzle Inc. | Earnings Calls | 2026-08-06
Operator (Operator)
Good day, and welcome to Sezzle's Second Quarter 2026 Earnings Conference Call. [Operator
Instructions] Please note, this event is being recorded.
I would now like to turn the conference over to Charlie Youakim, CEO and Executive Chairman. Please
go ahead.
Charles Youakim (Executives)
Thank you, and good afternoon, everyone, and welcome to Sezzle's Second Quarter 2026 Earnings Call.
I'm Charlie Youakim, CEO and Executive Chairman of Sezzle. I'm joined today by our CFO, Lee
Brading; my Co-Founder and Company President, Paul Paradis; and Head of IR and Corporate
Development, Jack Fagan.
In conjunction with this conference call, we filed our earnings announcement with the SEC and have
posted it along with our earnings presentation on our Investor website at sezzle.com.
To retrieve the documents, please go to the Investor Relations section of our website. Please be advised
of the cautionary note on forward-looking statements and the reconciliation of GAAP to non-GAAP
measures included in the presentation, which also covers our statements on today's call.
Okay. With the boilerplate completed, let's get started. We know you can now see that 2026 is off to a
great start. I was remarking to our leadership team earlier this past quarter that our volume growth
curves look a lot like they did back in 2020 and 2021, which was an amazing growth period for the
company.
My tip off to that was our May GMV surpassing our December holiday GMV. In recent years, it has
taken until August for the same sort of event to occur. And as many of you know, volume isn't our
North Star, but it's a nice secondary indicator that our solutions are taking hold.
In the second quarter, we made more strides towards improving those solutions and executing on their
growth. We brought more consumers onto the subscription platform in the quarter than we have ever
done before. And we improved the subscription offering, deepening the relationship with the customer
once they joined.
SezzleCash is a new offering only available to subscribers that allows them to smooth their cash flow
needs with a product that feels familiar with a Pay-in-4 or Pay-in-5 payback period. Now the customer
can access funds at an extremely low cost relative to alternatives and budget for the payback.
As we're supporting our customers with products like SezzleCash, they become more loyal to our brand
because we keep nailing the offering. In layman's terms, our products get stickier, which is a damn good
thing. We're also winning outside the product ecosystem.
On Slide 3, you'll see we continue to receive accolades by outlets that have recognized us before. The
CNBC named us one of the World's Top Fintech Companies for 2026. Newsweek included us on
America's Best Online Platforms and U.S. News recognized us as one of the Best Companies to Work

For in 2026. We don't do this for the awards, but when the same outlets keep coming back, it tells us
the product is working for our consumers and the culture is working for our team. Both of those matter.
Now to the results. Second quarter GMV grew 37.9% year-on-year to a record $1.3 billion, and total
revenue grew 51.7% to $149.7 million. Net income was $40.8 million, a 27.2% profit margin, and
adjusted EBITDA was $58 million, a 38.8% margin.
Total revenue less transaction-related costs came in at 63.5% of total revenue, right in the upper half of
the 55% to 65% range that we target. Given the strength in the first half and the momentum we're
seeing across the platform, we are raising full year guidance again. We now expect total revenue growth
of 35%, targeting the upper bound of our prior 30% to 35% range. We are raising adjusted net income
guidance to $185 million from $180 million and adjusted net income per diluted share to $5.25 from
$5.10. Lee will give you more detail later in the call.
The engagement story behind those numbers is in the bottom right of the slide. Active subscribers
reached 854,000, up an incredible 76.4% year-over-year. And average quarterly purchase frequency hit
a record 7.2x compared to 6.1x in the second quarter of last year.
Subscribers are our highest lifetime value users, and frequency is a metric that tells us whether the
ecosystem is actually working. Both are moving in the right direction.
Turning to Slide 4. We added 140,000 net new subscribers in the quarter. That's the largest quarter-
over-quarter and year-over-year subscriber gain we've had since we launched the subscription
program. That didn't happen by accident. As you can see on the chart, marketing spend was $19.4
million in the quarter. We have said before that we would push marketing as far as we can while staying
inside a 6-month payback period. And the second quarter is us doing exactly that.
Based on the core data we have so far, payback is still under 6 months. That tells us something
important about the virality and the value of the subscription suite. When we put more dollars to work,
consumers convert and they stick.
I'd like to note that this was a deliberate step-up to test out higher levels of marketing spend and not a
new run rate. We tested to see how far channels could stretch until we became less comfortable with the
ROI. We found that we could push levels of spend higher and still stay at the sub 6-month payback. But
even with that, we feel more comfortable with better ROIs on marketing spend.
I have always had a strong feeling that business is a bit art and a bit science. And while the science says,
yes, you can do this or even yes, you should do this, perhaps, our gut is telling us that we feel more
comfortable with strong return curves at lower levels of marketing spend.
You can expect a lower level of spend in Q3, all things being equal. But for us, it's never that simple as
we have just recently launched SezzleCash and are about to launch Sezzle Send.
The mandate to the team hasn't changed. If they find places to put dollars to work that stay within our
payback threshold, we're going to test them. And even with that step-up in spend in this quarter, we're
still raising our bottom line guidance because the consumers we added this quarter begin paying back
in the third and fourth quarters.
The other half of the equation is making the subscription itself worth more every quarter. On last
quarter's call, we announced the Sezzle Mobile plan, giving Sezzle Anywhere subscribers an unlimited
5G plan on AT&T's network starting at $29.99.

At the end of the second quarter, we added another benefit, access to SezzleCash, a new cash advance
product that gives Anywhere subscribers a way to cover short-term liquidity needs through Pay-in-4 or
Pay-in-5 with no down payment required. Add in card-linked offers, more points and rewards and early
access to beta products and the subscription keeps getting harder to walk away from. And as an added
benefit in the coming quarter, Anywhere consumers will enjoy no service fees on Sezzle Send.
However, we aren't only building value for subscribers, we're expanding what every consumer gets
because retention and engagement matter across the whole base. A lot of this we're doing through
partnerships, which lets us bring benefits to everyday shoppers quickly rather than building everything
ourselves, as seen on Slide 5. That includes card-linked offers that reward virtual card spending at
partner merchants and expansion of cashback across more merchants and daily actions like gamified
surveys, trivia and giveaways that give consumers a reason to open the app even when they aren't
shopping.
And on the monetization side, we're converting engagement we already have into revenue without
changing the user experience. The more value our consumers get from Sezzle, the more valuable they
become to us. Consumer value and shareholder value move together here, and that's the test we apply
to every product decision.
You'll also see the merchant side of this. When we launched On-Demand, we said it would help us win
enterprise merchants because it lets us offer more competitive pricing to merchants with thinner
margins.
Enterprise sales cycles are long, so this takes time, but the strategy is starting to bear fruit. Recent
enterprise wins include Poshmark, Gymshark, Debenhams, and several others. Acquiring users and
driving engagement matters in any consumer business. But what matters just as much to us is the pace
at which we ship.
As you'll see on Slide 6, the second quarter was another busy one for our product and engineering
teams. We rolled out SezzleCash in June through a phased launch, reaching the full population of
eligible Sezzle Anywhere subscribers by the end of the quarter. And coming in August, we plan to
launch Sezzle Send, a peer-to-peer money transfer product that lets consumers send money by phone
number and either Pay-in-4 or use Pay-in-5. The recipient receives the full amount upfront and doesn't
need to be a Sezzle consumer to get the money. So every send is a potential introduction to the
platform.
Slide 7 goes deeper on both. Up to this point, almost everything we've built has been anchored to a
purchase, SezzleCash and Sezzle Send aren't. They're about liquidity and moving money, everyday
financial needs that have nothing to do with the checkout page. We are continually expanding beyond
our original point-of-sale offering and our never-ending race to increase the value of our platform to
our stakeholders.
SezzleCash and Sezzle Send do three things for us: drive virality; increase attraction to the platform;
and improve retention to the platform by bringing consumers back into Sezzle for reasons other than
shopping and by offering more value to them. As we continue to increase our value to the consumer,
we'll continue to earn more share in their wallet.
Although SezzleCash just launched, the initial signal is encouraging. The average advance size is
approximately $165, and nearly 10% of eligible new subscribers are requesting in advance as their first

transaction in the Sezzle Anywhere ecosystem. That tells us the product is pulling in consumers we
might not have reached through our traditional offering alone.
On Sezzle Send, I think most of us on this call use the money transfer product. So we all understand the
virality of these platforms. Our twist is to take the burden off the transfer. A consumer can send 100%
of the money to their friend upfront and repay us through Pay-in-5. And because the recipient doesn't
need a Sezzle account to get the money, every send is a potential low-cost acquisition in a new
acquisition channel our consumers drive for us.
For Sezzle Anywhere subscribers, we waived the service fee on Pay-in-5 entirely in Sezzle Send. And for
nonsubscribers, the fee is de minimis, around $3 for $100 spend.
Unlike SezzleCash, we made the Send product available to nonsubscribers because of the virality it can
help us create. But even though the fee for non-subs is small, it's still another reason to be a subscriber
and another screen in our app where we can convert the consumer into a subscriber.
I'll add the caveat I'd want to hear as an investor. As with any new lending product, we're being
conservative early and still fine-tuning the underwriting. So I'll spoil part of Lee's narrative and tell you
now that our guidance does not assume material upside from SezzleCash and assumes 0 contribution
from Sezzle Send.
A couple of items about Sezzle Send. First, we've already got about 100,000 users on the wait list. Our
users are excited about it. And second, it's the first product we produced where the vast majority of the
build was AI-driven, and a small team has taken it from concept to launch-ready in a matter of weeks
rather than months, a product that moves real money between real people built by AI.
A couple of years ago, that would have been a research project. For us, it was one quarter's worth of
work, which leads us to Slide 8. AI is embedded across this platform now, and I want to give you real
numbers rather than talking points.
On the consumer side, our AI support chatbot is deflecting 68% of consumer inbounds. And I'd note
that the bot is scoring a higher CSAT than our human agents on those answers. That frees our people
up for the complex issues that generally need a person. Our AI shopping assistant within our Discover
tab is driving a 3.6x product click-through rate versus control, and it's now live for 80% of Sezzle
Anywhere users with plans to expand to all consumers.
Internally, we've become an organization that effectively requires AI in the workflow. It's the
expectation for every employee, and the team has taken that to heart. As new models roll out, I expect
all of our internal KPIs, not just a few listed on the right side of the slide, to get better and our teams to
do more with the same headcount.
My first bots out of school told me, speed, quality and cost, pick 2 out of 3. With AI, Sezzle is taking all
three.
That brings me to Slide 9. We're building fast, shipping quickly and putting more products in front of
consumers every quarter, and that pace compounds. It shows up directly in the year-over-year
engagement metrics.
MODS increased 234,000 year-over-year to 982,000. Quarterly purchase frequency reached a new
high of 7.2x, up 1.1 turns. And repeat usage was 97.2% of total orders, up 80 basis points. While these
numbers continue to step up every quarter, the one I'd like to point out to you is the bottom left. The
average quarterly revenue per monetized user increased 16.2%.

Growth is coming from a larger user base, but it's also coming from consumers who engage with us
more often and generate better economics over time. Those two things working together are the whole
model. It's multiplication, not addition. A bigger base and a more valuable consumer within it
compound on each other, and that's what we're building for over the long run.
We are still early in what Sezzle can become for the value-focused consumer, but the flywheel is getting
stronger every quarter.
With that, I'll turn it over to Lee to walk you through the numbers in more detail.
Lee Brading (Executives)
Thanks, Charlie. I will get started on Slide 10. It's exciting to see the hard work and effort put in by our
team at Sezzle pay off. Q2 revenue increased 51.7% year-over-year. Net income rose 47.7% year-over-
year and adjusted net income expanded by 58.4% year-over-year.
Growth did not come at the sacrifice of margins, as we have always said that we will not grow for
growth's sake. We take bottom line profitability seriously, if not more so, than top line growth.
Total revenue less transaction-related costs as a percentage of total revenue increased 240 basis points
to 63.5%, which is at the upper end of our 55% to 65% target range. Revenue growth plus EBITDA
margin puts us right at a score of 91 for the Rule of 40, exceeding our 82 score for Q1.
On Slide 11, you can see the strong momentum in our business. Q2 GMV grew 15.1% sequentially,
37.9% year-over-year and exceeded our Q4 2025 holiday season peak. Q2 revenue rose 51.7% as
revenue yield expanded 110 basis points year-over-year to 11.7%. For 2026, we expect our revenue yield
will be similar to 2025's yield of 11.4%. Therefore, we project our revenue yield will continue to step
down sequentially for the remainder of 2026 with Q4 being the seasonal low point.
Turning to our unit economics on Slides 12 through 14. As a reminder, transaction-related cost is a non-
GAAP measure that combines transaction expense, provision for credit losses and net interest expense.
You might also hear us refer to revenue less transaction-related costs as net transaction margin or gross
margin.
For those that listened to our Q1 earnings call, you heard us belabor the point about the seasonality in
our business regarding the revenue yield and provision. As a quick reminder, revenue yield tends to be
the highest in Q1 and lowest in Q4, while the provision for credit losses typically reaches its lowest
point in Q1 and rises throughout the year.
This is evident on Slide 13. You can see that transaction expense and net interest expense are relatively
static as a percentage of GMV compared to the provision for credit losses. Again, Q1 tends to be a
seasonal low point in the provision led by the tax refund season.
The increase in the provision is not unexpected, and I want to remind everyone of two things when we
consider provision and its impact on our financials. First, we target a 55% to 65% net transaction
margin, which is inclusive of the provision. And second, we expect the full year provision to be in the
range of 2.5% to 3% of GMV. We are good on both accounts.
We finished Q2 with a net transaction margin of 63.5%, which is at the high end of our target range,
and we expect the provision for credit losses will be in the 2.5% to 3% range for 2026. So yes, we can
have a provision in a quarter that goes above the 3% level.

Before moving on, I want to emphasize the increase in provision was expected due to seasonality and
our push to bring on new users. As Charlie noted in his comments, we had a record quarter-over-
quarter and year-over-year gain in the number of net new subscribers. As a result, we had more new
consumers utilizing the platform and with new users comes higher provisioning.
Our hyperfocus on cost does not stop at the unit economic line. It also extends to our non-transaction-
related operating expenses, as shown on Slide 15. Non-transaction-related operating expenses consist
of personnel, third-party tech and data, marketing and G&A. The bulk of the expense is driven by
personnel and marketing. Like last quarter, we more than doubled our marketing spend year-over-year.
As Charlie noted earlier, as long as the math works for a less than 6-month payback, we will continue
spending. I'm guessing the marketing spend might be more than most people modeled for, but the
results speak for themselves, new highs in active consumers, subscribers and GMV.
Further, we were still able to raise our net income and EPS guidance while removing the low end of our
revenue guidance despite the significant growth in marketing expenditure. A large incremental increase
in spending can be a headwind initially, but will start paying dividends for us over the coming quarters.
On an apples-to-apples basis, we do expect our core marketing spend to decrease from Q2 to Q3.
However, we are in the middle of launching two important products: SezzleCash; and Sezzle Send. We
have done little to no marketing for either of these, so it will require some basic awareness expense, and
we will let the payback math dictate the magnitude of the spend.
We did incur minor costs related to our corporate strategic projects during the quarter. On May 11, the
U.S. District Court granted in part and denied in part the defendant's motion to dismiss our antitrust
suit. Most notably, the court denied the motion to dismiss our claims, a monopolization and attempted
monopolization under the Sherman Act and the parallel claims under Minnesota Antitrust Law and the
Minnesota Deceptive Practices Act. We are now entering the discovery phase, which is expected to go
through 2027.
The banking charter process continues to roll forward, and we are planning to submit our application
for National Bank charter this quarter. I believe we have one of the cleanest income statements when it
comes to add-backs and adjustments.
You can see on Slide 16, very little difference between net income and adjusted net income. Most of the
differences are attributable to discrete tax items recognized in each quarter. Further, you can see the
seasonality of our numbers with Q1 followed by Q4 as typically the best bottom line performing
quarters.
We are well capitalized and positioned with plenty of liquidity and very low leverage, as seen on Slide
17. At quarter end, we had over $205 million in liquidity between unrestricted cash and availability
under our new $300 million line of credit. Our total debt to trailing 12-month adjusted EBITDA stands
at only 0.5x and our total debt to equity is also only 0.5x.
I'm sure by now, everyone has already checked out Slide 18 and therefore, is quite aware of our updated
guidance. We are really excited about the momentum in our business and believe some of that is
captured in our updated guidance. I'll make a couple of comments before passing the call over to the
operator for Q&A.
Our guidance does not take into consideration Sezzle Send as that product is just getting to the launch
pad. Additionally, the guidance has very little impact from our recent launch of SezzleCash.

SezzleCash has been a measured rollout in terms of marketing and risk. So it is still too early to put
much emphasis on it in our guidance.
I would now like to turn the call over to the operator for Q&A.
Operator (Operator)
[Operator Instructions] The first question comes from Mike Grondahl with Northland Capital.
Michael Pochucha (Analysts)
This is Mike Pochucha on for Mike Grondahl. Maybe just on the bank charter, can you remind us what
a typical time line might look like for that application process?
Charles Youakim (Executives)
Well, the OCC has been pounding the table that from application to conditional approval or conditional
decision is around 120 days or basically, I guess, mandated at 120 days. But that's not the end of the
process. You also have to go through FDIC approval and Fed approval.
I would say our expectations are 12 to 18 months in total. I think we're being a little bit conservative
with that. But we view that as if we get our national charter in the next 18 months, we feel pretty good
about the entire process.
Michael Pochucha (Analysts)
Got it. Makes sense. And then on the new partnership funnel, if you could just characterize that maybe
versus 6 months ago or a year ago? Anything to call out there?
Charles Youakim (Executives)
Well, I would just say, just in general, a lot stronger with a lot of nice enterprise names on the
partnership side. I think On-Demand has a lot to do with that. And also our strong lifetime values of
our consumers. That math all goes in the equation.
On-Demand goes in the equation for the merchant side. It helps us model better pricing for merchants
that are sensitive to cost, which brings many more merchants into the fold. And on our side, because
our subscription products are such strong products for us on the consumer side, we do model in
winning these merchant deals and what percentage of those consumers will go into those products. And
that also helps us with more aggressive pricing, more aggressive deal making. And I think all in all, I
think that's helping quite a bit. I don't know, Paul, anything to add to that?
Paul Paradis (Executives)
I would just add to that. We started to be added alongside other BNPL providers over the last 2, 3 years.
Early days, a merchant would commit to one exclusively. And so as we create successful case studies
that show that adding a second or third brings incremental sales, it's accelerated the enterprise sales
funnel. So we expect it to continue to improve.
Operator (Operator)
The next question comes from Hal Goetsch with B. Riley Securities.
Harold Goetsch (Analysts)

A couple of questions on the new products. And I know you partnered with Pagaya for some larger loan
offerings. You've got Pay-in-5 and you have the two new initiatives you just announced today. Could
you tell us maybe what's embedded in your outlook for some of those products?
Charles Youakim (Executives)
Lee, I'll leave it to you on that one. We've already mentioned a couple of those, Hal. So on Sezzle Send,
SezzleCash, not a lot. But Lee, anything to add to that?
Lee Brading (Executives)
Yes. And I think, Hal, you were asking about Pagaya too. And Pagaya is hopeful, but it's not -- I'd say,
not a material impact at this point. So yes, nothing significant from those. I would say that materially
moves the needle.
Harold Goetsch (Analysts)
Okay. And on the marketing spend, are you suggesting that like the payoff is so good that you're going
to continue this kind of maybe dollar spend or even take that up? Because the subscriber numbers were
pretty powerful sequentially in a seasonally weak quarter, generally seasonally weak. I mean it was one
of your largest net adds in a non-holiday quarter ever.
Charles Youakim (Executives)
I think it depends, Hal. Basically, the way we're viewing it is I always like to look at visual or think of
visualization. And I think we are like hitting the gas in the car just to kind of see how the car reacted. If
we did it, and just like what the cohort pumping through would look like.
And so I think from that perspective, we're letting off the gas a little bit, all things being equal. But
that's why we mentioned like all things aren't equal because we have Sezzle Send launching. We have
SezzleCash. SezzleCash, we haven't even started marketing externally yet. It's just marketing internally
to our existing cohorts and customers seeing pickup rates, and reactivation rates. So we're really not
even spending externally on that product at this time.
So I think if you subtract SezzleCash, Sezzle Send, I probably expect a lower level on a volume basis of
marketing spend just because we wanted to pump that cycle through and see how the cohorts run out.
But what we're seeing from the cohorts running out is it is a sub-6-month return on investment.
That being said, I think we just feel a little bit more comfortable not going near the 6 months or not
going as near the 6-month edge. So that's another reason for a little bit of pullback. So some of it is just
seeing the engine react. Some of it is just we feel a little bit more comfortable pulling it back. But then
again, the reason I caveat is because now we got these two products launching. And with those two
products launching and pushing out a little bit more, that might be the offset that leads to a little bit
higher spending level. Does that make sense?
Operator (Operator)
The next question comes from Ryan Tomasello with KBW.
Ryan Tomasello (Analysts)

Congrats on a good quarter. Also I wanted to ask about the thought process around the marketing
spend. Maybe just help us understand why pull back if the payback is so strong? I know that a few of
your peers that also focus on the lower income category have also been leaning heavily into customer
acquisition. So curious if there were any signals that were suggesting pressure on the payback and why
not run rate 2Q into the second half?
And then just looking at the second half guidance, obviously, still really solid growth, but I think maybe
the hope would have been that there would have been some more meaningful flow-through of the
growth momentum in the second half. So just help us understand what's driving the deceleration in 2Q
-- sorry, in second half revenue growth as well?
Charles Youakim (Executives)
Well, on the marketing spend, again, it's just a level of comfort. The 6 months is our edge. And the
closer you get to your edge, the tighter -- the higher the risk reward, I guess, near the edge. So that's
part of the reason for maybe a little bit of a pullback in our mind, but we also want to see it pulse
through.
Again, it takes 6 months to get the return. And if you're off by 30%, it's not 6 months, it's 7-something
months, near 8 months. And -- then that starts to -- you don't know that until you a little bit further
down the month on month-on-month line. And so that's why I was kind of the analogy of like pumping
the gas on the car, we wanted to kind of hit the gas in the car, push that cycle through. Let's see how it
looks as it cycles through.
And as we start to feel more comfortable, confident, I think maybe the next time we go about an
exercise like this, we might even feather on it a little bit slower instead of just pumping on a cycle like
that. And then as far as the guidance or the growth, I don't know, Lee, if you have anything to touch on
that?
Lee Brading (Executives)
Yes. And just following up to your comments on margin. Just I think you kind of touched on that at the
end, it was more of a smoothing, right? You don't want to accelerate too hard at one time. And so it's
just a more steady process with it as well, just managing that. But from a guidance standpoint, yes, I
mean, we've guided here, got rid of the low end of our revenue guidance, did bump up our bottom line
guidance.
So yes, second half, you do the basic math, right? First half, we were up 40% year-over-year, 48% on
net income, 40% on revenue and guiding kind of 30% up here in revenue for the top line and then
bottom line 40%. Feel -- we feel very confident of those. We've talked about to -- not having some
certain things in there at this point in time in our guidance. So that will to be determined as we go
through the remaining quarters.
Ryan Tomasello (Analysts)
That's very helpful. And then in terms of the -- Charlie, how you're thinking about the overall growth
algorithm for the business over the next year or so and also looking at this disclosure in the slide deck
that I think gives you the average quarterly revenue per monetized user. It looks like the mix of revenue
growth in the quarter was, call it, 2/3 user growth and 1/3 ARPU. Is that kind of a mix that you feel
comfortable with going forward? Or should that maybe balance out heading into the back half of the

year as you pull back on the marketing and baking in these new products? Just trying to understand
that growth algorithm.
Charles Youakim (Executives)
I hear what you're saying, Ryan. I guess from my perspective, I don't really totally focus on that kind of
split. I guess when I'm focusing on us growing the business, it's really about launching products and
executing on existing products in a way that is showing that it's providing interest and value to the
consumer. So we basically looked at like take-up rates of products, attraction rates to products, like, for
instance, Pay-in-5, an absolute home run.
We said it from the start. It seems like -- it doesn't make sense to maybe the credit card user who's not
maybe a BNPL user. But we thought early with surveys, our customers really wanted Pay-in-5. We had
really high engagement rates on the product. We launched it. We saw it play through.
I think with SezzleCash, we saw some of the same dynamics with surveys. And we played it through, a
lot of our customers are up taking it. I don't know if people caught the comment we made during the
call.
But Sezzle Anywhere, the subscribers when they first joined it, 10% of the customers that are joining
Sezzle Anywhere, their first transaction is a SezzleCash transaction. And I mean that's -- I think that's
pretty incredible, especially the fact that we're not even like leading with it at the moment. It shows how
much interest there in that type of a cash flow product.
And then Sezzle Send, I think that's a product that we have a really good sense that the customer wants.
I mean the waitlist is already -- over 100,000 on the wait list, which is really exciting. We basically just
launched the waitlist. So the uptake on that is really exciting.
And so the -- with Sezzle Send, we have another avenue for providing value to existing customers, but
also acquiring new customers because as those customers use our product with P2P, they can send it to
new customers or new potential customers, non-Sezzle users. to accept their funds and get introduced
into our platform. So it creates a whole new channel for customer acquisition.
So I think from my perspective, that breakdown that you mentioned is not even something I look at.
But I -- what I think about is just like what are home run type products. And I think what I feel good
about with our business and our company is we've had just a very high percentage of home run
products. We've had only a couple of products where I call them singles or strike outs.
Like it's just -- it's been a very high hit rate. And I think we have a few more in the hopper with
SezzleCash and Sezzle Send that are going to be home runs.
Operator (Operator)
The next question comes from Kyle Peterson with Needham.
Kyle Peterson (Analysts)
I wanted to start out with some of the moving pieces in the take rate in the guide. I think you guys said
11.4% for the year should be about flat. So I understand there's some seasonality there, but just trying
to square at least some of the year-on-year impacts with some of these newer products like Pay-in-5,
which I would think would be accretive to take rate. So just want to see like how much is conservatism
versus if there's any other mix or moving pieces that we should be mindful of?

Charles Youakim (Executives)
Lee, do you want to take that one?
Lee Brading (Executives)
Yes. Yes, you're right on the Pay-in-5, can be accretive. But as we launch new products, like Pagaya can
be not accretive to the take rate. Just the nature of how that is accounted for. And then also as we
launch SezzleCash as well. So those can lower the take rates. While we still have very similar
profitability and margin standpoint, the take rates on those can be a little lower.
Kyle Peterson (Analysts)
Okay. That is helpful. And then I guess I wanted to double-click on the provision expectations moving
forward. I know there's some seasonality there. And then you guys also have some more new customers
coming on board. But I guess, is there any change on a apples-for-apples basis that you guys are seeing
in either repayment rates or consumer credit health or anything like that? Just want to be able to
understand on a going-forward basis and kind of what you're seeing real-time, especially with existing
customers' performance?
Charles Youakim (Executives)
Yes, everything seems just normal, Kyle, I'd say. It's nothing related to the customer profile or customer
and the economy. But I'd say our prior guidance on that stands 2.5% to 3% for the year, which basically
explains that there's going to be a step-up in the third quarter and fourth quarter.
I think that everyone modeling can expect that -- model for that. The only caveat I'd say is like how
these new products take up and we start to really start to push them externally, I'd say, especially with
virality around Sezzle Send, if that really does pick up a lot of new users.
So basically, it's like a trade-off of new users because new users have higher loss rates. So if new users
pick up more than expected or more than modeled for many out there modeling, then I would expect if
you have variability in your model, if you pick up new user growth, you're going to expect to have
provision to be higher than you have modeled for if you move that variable around.
Operator (Operator)
The next question comes from Rayna Kumar with Oppenheimer.
Rayna Kumar (Analysts)
Great quarter. I just want to better understand just the puts and takes of the revenue yield. Obviously, it
was up 110 basis points on my calculation year-over-year. Just want to understand like is that a mix? Is
that pricing?
And then secondly, your 2026 guidance assumes that there is going to be a sharp deceleration in
revenue growth in 2H from the second quarter. Just want to understand the drivers there?
Lee Brading (Executives)
Yes. One of the key things that we -- yes, sorry, one of the key things we pointed out heading into Q2 on
our Q1 call was that we had an easy comp on the revenue yield in Q2, which drove that revenue growth
this quarter.

So I don't know if you saw that, I think it was like a 10 handle or so last year versus the 11 handle this
year. And we had a number of items change as far as types of fees or the rates that we had. And we
mentioned on that call that going forward, I'd say more of a normalized, meaning that we weren't
having any much movement in terms of how we are charging and the fees that we did and the revenue
items that were driving our revenue yield.
So that you'd see a more consistent, I guess, you could say, from Q3, 4 and on. And that's where we
talked about seeing a more normal performance in revenue yield from a seasonality being -- Q1 being
the strongest and Q4 being the lowest because you're not seeing a lot of movement in the puts and
takes. And so that's why you'll see -- that's why you saw the -- it was down year-over-year in Q1, up in
Q2, but now you'll see an easier, more normal comparison going forward here. But overall, for the year,
we said it would be flattish for the year.
Operator (Operator)
The next question comes from Hoang Nguyen with TD Cowen.
Hoang Nguyen (Analysts)
I want to ask on, I guess, the charts on the on-demand number of users versus subscribers. So I think
since you guys made the pivot, I think On-Demand count continues to go down while subscriber count
continues to go up. And while subscriber demand has been strong, should we read this as a sign that
once you kind of limit people's ability to use On-Demand, a large percentage of these people eventually
convert to subscribers?
Charles Youakim (Executives)
Well, there is a portion that are converting. That's a good insight that as we diminish the push towards
it. But I'd say really more of the change has been just what is presented. We used to like lead with On-
Demand as the lead product. Come and try a Sezzle at a merchant site and you can pay as you go.
Now that's really not the lead. The lead is join our subscription program. And then On-Demand, the
place where that's still -- where we still the lead for On-Demand is in merchant checkouts.
So when we have these enterprise partnerships, some of these merchants coming on board, the way to
pay is with essentially a transaction with the service fee, which is On-Demand.
So that's really the only place or I shouldn't say the only because there's always edge cases here and
there. But the vast majority of the new cases for people entering On-Demand are at those checkouts. So
I think it's more about what's being presented or led as the transition product for consumers that are
moving into our MOD products.
Operator (Operator)
This concludes our question-and-answer session. I would like to turn the conference back over to
Charlie Youakim for any closing remarks. Please go ahead.
Charles Youakim (Executives)
Well, thank you, operator. I'd like to leave you all with something Warren Buffett said back in 1991. It's
not a crazy idea. It's a simple one. He said, someone is sitting in the shade today because someone
planted a tree a long time ago.

I thought that even though it's a simple concept and a simple quote, I think it nails one vector of our
thinking at Sezzle. We plan for long-term returns.
Let's take a look at the tree we planted and the tree today, which is giving us all shades. Back in July of
2019, we listed on the Australian Stock Exchange. I wanted to share some of our results from the
second quarter of that year right before we went public about 7 years ago, just to give you an idea of
how long-term growth plans play out.
Our second quarter 2019 GMV, $41.2 million versus $1.3 billion today, basically a 30x. Our second
quarter 2019 revenue, $2.6 million versus $149.7 million today, nearly 60x. Our second quarter 2019
gross margin, a negative $260,000. This quarter, $95.1 million.
As you can see, the long-term approach to growth works. I'm going to calendar this one as a reminder
to do this again in 7 years. I hope you'll all still be investors at that time. And to that 7-year time line,
many members of our team have been here for that entire 7-year journey. And to them and the rest of
the team, a big thank you for your incredible work on getting us from there to here. We'll talk again
next quarter. Thank you.
Operator (Operator)
The conference has now concluded. Thank you for attending today's presentation. You may now
disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SEZL_Q1_2026_Earnings_Call_20260506.md
- 2026-05-06｜CEO Charles Youakim｜guidance：全年營收成長財測由 25–30% 上調至 30–35%（原話："from 25% to 30% to a new range of 30% to 35%."）
- 2026-05-06｜CEO Charles Youakim｜guidance：調整後淨利財測上調 1,000 萬美元至 1.8 億美元（原話："adjusted net income guidance by $10 million to $180 million"）
- 2026-05-06｜CEO Charles Youakim｜guidance：調整後 EPS 財測由 4.70 升至 5.10，管理層稱部分來自第一季回購（原話："$5.10 from $4.70 with some benefit from repurchase activity"）
- 2026-05-06｜CFO Lee Brading｜guidance：CFO 說明財測不含開發中新產品的預測（原話："guidance does not reflect any projections for new products"）
- 2026-05-06｜CEO Charles Youakim｜guidance：CEO 說明財測含 Pay-in-5，但 Sezzle Mobile 不在預測內（原話："that's not anything we're projecting at this point"）
- 2026-05-06｜CFO Lee Brading｜guidance：CFO 說下一季營收收益率的比較基期較容易（原話："we'll have an easier comp from a revenue yield"）
- 2026-05-06｜CFO Lee Brading｜margin：管理層目標：信用損失提列佔 GMV 2.5%–3%（原話："provision for credit losses in the 2.5% to 3% of GMV range"）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 提醒 74% 單位經濟毛利率因季節性不可年化（原話："annualize a unit economic margin of 74%, we can't."）
- 2026-05-06｜CFO Lee Brading｜margin：營收減交易相關成本的長期目標區間 55%–65%（原話："transaction-related costs in the 55% to 65% range."）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 稱該利潤率一直落在區間偏高端（原話："we've definitely been trending on the higher end of that"）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 稱未必會把本季這種信用損失優於預期的幅度計入未來（原話："necessarily booking in that same kind of outperformance"）
- 2026-05-06｜CEO Charles Youakim｜margin：CEO 解釋本季提列受前期高估估計回沖影響（原話："we had overestimation leaks in the first quarter"）
- 2026-05-06｜CEO Charles Youakim｜margin：CEO 重申全年提列率計畫維持 2.5%–3%（原話："still to see 2.5% to 3% for the provision for the year"）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 說 Pay-in-5 初期損失率可能略高（原話："initially a little higher loss rates on that as well"）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 拆解年增收益率下滑 80bp 的原因（原話："revenue yield declined 80 basis points due to the mix"）
- 2026-05-06｜CFO Lee Brading｜commitment：CFO 稱預期持續提高非交易相關營運費用的槓桿（原話："continue to leverage our nontransaction-related OpEx"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱行銷支出預期逐季上升（原話："we expect it to continue to rise quarter-on-quarter"）
- 2026-05-06｜CFO Lee Brading｜commitment：CFO 稱預計 2026 年年中提交銀行執照申請（原話："We anticipate submitting our application"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱現金流管理產品預計三個月內較大規模推出（原話："we plan to launch here in the next few months"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱支票帳戶產品也將在未來幾個月內推出（原話："that's another product coming in the next few months as well"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱路線圖產品預計 2027 年底前完成推出並放量（原話："launched and scaling by the end of 2027"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱到 2027 年底一定會有存款帳戶（原話："We'll definitely have the deposit accounts in place by then."）
- 2026-05-06｜CFO Lee Brading｜capital_allocation：第一季回購 2,480 萬美元普通股（原話："repurchasing $24.8 million worth of common stock"）
- 2026-05-06｜CFO Lee Brading｜capital_allocation：季末現金 1.474 億美元（含受限現金 2,690 萬）（原話："we ended the quarter with $147.4 million in cash,"）
- 2026-05-06｜CFO Lee Brading｜capital_allocation：信貸額度明年四月到期，正進行再融資（原話："refinancing our current credit facility, which matures next April."）
- 2026-05-06｜CFO Lee Brading｜capital_allocation：行銷支出年增超過一倍（原話："spend more than doubled year-over-year in the quarter."）
- 2026-05-06｜CEO Charles Youakim｜capital_allocation：CEO 稱行銷回收期仍短於 6 個月（句子接下一行）（原話："we continue to see a payback period of less"）
- 2026-05-06｜CEO Charles Youakim｜capital_allocation：銀行執照可把銀行夥伴的變動成本轉為固定成本（原話："it does move a variable cost stream to a fixed cost stream"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 認為 Pay-in-5 是未來一年最重要的產品，因已有成效（原話："it's already proven to have results for us"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 稱 Sezzle Mobile 設計目的在留存而非營收（原話："not really designed to drive revenue, gross margin"）
- 2026-05-06｜CEO Charles Youakim｜product：加拿大虛擬卡尚未完整上線，加拿大約占 10% 交易量（原話："it's also in Canada, which is 10% of our volume"）
- 2026-05-06｜CFO Lee Brading｜product：Pagaya 合作為按交易量收取費率，Sezzle 不分擔風險（原話："We're not sharing in the risk on that product"）
- 2026-05-06｜CEO Charles Youakim｜product：AI 客服機器人解決約六到七成對話無需轉人工（原話："approximately 60% to 70% of the chats without escalation"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 稱約八成程式碼由 AI 產出、人工審閱（原話："upwards of 80% of our code"）
- 2026-05-06｜CEO Charles Youakim｜product：管理層稱 AI 讓費用成長維持遠低於營收成長（原話："while keeping expense growth well below revenue growth"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 說自己不再只是 Pay-in-4 公司（敘事擴張）（原話："we are no longer just a Pay-in-4 company"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 說 2026 年策略是不再只在結帳時被想到（原話："moving beyond being a product consumers think about"）
- 2026-05-06｜CEO Charles Youakim｜competition：CEO 預期 BNPL 像信用卡一樣從封閉迴路走向開放迴路（原話："more and more and more open loop"）
- 2026-05-06｜CFO Lee Brading｜competition：CFO 稱特約商戶已成為較不重要的業務，主要作為獲客管道（原話："it's becoming a less important part of our"）
- 2026-05-06｜CFO Lee Brading｜risk：CFO 稱反壟斷訴訟進行中、無法進一步說明（原話："Our antitrust suit is currently ongoing"）
- 2026-05-06｜CFO Lee Brading｜risk：CFO 稱銀行執照程序漫長且不保證成功（原話："We recognize this process is long and not guaranteed"）
- 2026-05-06｜CEO Charles Youakim｜risk：CEO 稱部分州與監管機關在削弱銀行夥伴模式（原話："chopping away at the bank partnership model"）
- 2026-05-06｜CFO Lee Brading｜risk：CFO 稱未見消費者異常壓力（原話："we are not seeing any unusual strains on the consumer"）
- 2026-05-06｜CEO Charles Youakim｜customer：訂閱用戶增加 4.4 萬至 71.4 萬（原話："total subscribers increasing by 44,000 to"）
- 2026-05-06｜CEO Charles Youakim｜customer：每季平均購買頻率達 7.1 次（去年同期 6.1 次）（原話："reaching 7.1x in the quarter"）
- 2026-05-06｜CEO Charles Youakim｜customer：CEO 稱客群在數字中看不到宏觀壓力（回應油價問題）（原話："we're just not seeing anything"）
- 2026-05-06｜CEO Charles Youakim｜customer：管理層稱主要獲客管道包含連網電視廣告的擴張（原話："We're pushing more into connected TV"）

### 問答異常語氣（迴避／改口／保留）
- SEZL_Q1_2026_Earnings_Call_20260506.md｜問：Kyle Peterson（Needham）問信用損失優於預期，有沒有上行空間、何時回到區間｜答法：CEO 與 CFO 都以季節性、前期估計回沖、新用戶與 Pay-in-5 為由重申 2.5%–3%，未給任何超出區間的數字或上行空間；語氣為 comfortable
- SEZL_Q1_2026_Earnings_Call_20260506.md｜問：Hoang Nguyen（TD Cowen）問銀行執照能讓 Sezzle 推出哪些現在做不到的產品｜答法：CEO 回答 Not necessarily，改談監管防禦與成本結構（變動轉固定），未直接列出可新增的產品
- SEZL_Q1_2026_Earnings_Call_20260506.md｜問：Hal Goetsch（B. Riley）問低收入客群面對油價與可負擔性壓力，即時看到什麼｜答法：CEO 以自己的推測回應（自稱 just postulating），未給具體即時數據

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

`scenario_inputs`（EPS路徑五年、終端倍數、機率、yield、second_stage、Max DD範圍與依據）——你不寫`scenario.json`，那份由程式跑`dd_scenario.py`產生。Bear機率5Y不應<20%(多數25-30%；極強護城河+短期已兌現才壓15-20%)；Bull/Bear散布5Y應比1Y/2Y寬≥50%；Base機率不應>50%；bear機率須註明依據，sourced結構性durability仍硬套bear需說明「為何不採信」否則不得高於base [§3]。
- 內生天花板sanity check：Base情境EPS CAGR貢獻vs§5.R內生天花板(同組數字不重算)→天花板內✅/超出⚠(⚠→Bear機率強制≥30%)。成長熄火：3年後成長率降至15%/10%/5%三情境×Forward P/E壓縮→估值跌幅，作Bear PE錨。三分量拆解(≤80字，Base IRR多少來自EPS複利/re-rate/股息淨回購)：re-rate貢獻≥Base合計IRR的40%→標記「估值依賴型」(`decision_inputs.valuation_dependent=true`) [§3]。
- IRR落點：<8%/yr弱、8-12%中、>12%強、>15%罕見，不作跨檔排序依據。AR=`(P_bull×|Bull5Y%|)÷(P_bear×|Bear5Y%|)`，<2平庸/2-4偏正/≥4顯著，非放鬆機率防線理由。年期硬規則：①表頭終端年=主時距終端年②終端倍數EPS分母年期與現價倍數同源③終端倍數必附≥1個同業現值comp對照 [§3]。10Y二段延伸(`runway_post_y5`=🟢且終端倍數承重，或Base IRR實質來自Y5後)：Y5→Y10 EPS CAGR/10Y累積倍數/IRR。R:R數學假象：下行>15%正常使用；5-15%警示「已接近定價」；<5%失效標「數學假象」禁引用進場判定，改極端Bear(Bear PE×0.8+Bear EPS×0.85)重算(Bear EPS=FY+1 EPS×0.9；Bear PE=成長熄火「降至10%」情境) [§3]。

**Max DD**(`premortem.max_dd`)：填範圍`lo`/`hi`(禁單點，寬度≥10pp)+`path_risk`(🟢0～−30%/🟡−30～−50%/🔴<−50%)；推導依據須寫`reasoning.premortem`。硬接線：🔴且thesis脆弱(`moat.trend`↓或`runway_post_y5`🔴或估值依賴型)→倉位上限下修(6%→≤3%)；🔴但thesis完整→不因波動砍倉，註記「深回撤心理準備」[§2問六]。

**必答項**：`scenario_inputs`三支EPS路徑、終端倍數、Bear/Base/Bull機率、`premortem.max_dd.lo/hi`、`path_risk`。

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
{"date":"20260710","verdict":"觀望","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"BNPL 信用週期不反轉，SEZL 承保維持品質：provision/GMV 維持在低檔，不因放款簿老化爆雷","columns":{"2Y 驗證點":"FY26-27 連季 provision/GMV ≤ 2.0%；30+ DPD","5Y 驗證點":"2027-2030 穿越一次完整信用週期，provision peak","10Y 驗證點":"跨多次週期維持 net loss ratio 低且承保演算法持續優化","具體數字門檻":"Q1 FY26 provision 1.2% of GMV（$13.7M）；漂移門檻 provision/GMV 連 2 季 ≥ 2.0%","信息來源":"Q1 FY26 press release／8-K；AFRM/PYPL 歷史 peer benchmark；TransUnion 2026 Q1 次級信用趨勢","漂移觸發":"連 2 季 TTM provision/GMV ≥ 2.0% → 削弱；連 3 季 ≥ 3.0% 或撥備增速連 2 季超前 GMV 增速 → 反轉"}},{"id":"H2","text":"訂閱＋購買頻率動能持續，subscription pivot moat 兌現，且不被監管壓垮","columns":{"2Y 驗證點":"FY26-27 Active Subscribers YoY ≥ +30%；購買頻率維持 7x+","5Y 驗證點":"訂閱佔營收比顯著提升、ARPU 上行，且 NY／州級監管未把訂閱費實質納入利率上限","10Y 驗證點":"訂閱成為結構性黏著層，會員基數規模化","具體數字門檻":"Q1 FY26 Active Subscribers +48.4%、購買頻率 7.1x（+1.0x YoY）、MODS 887K（+34.8%）","信息來源":"Q1 FY26 press release；NY DFS BNPL 規則草案（2026-02，Davis Wright／Orrick 法律分析）","漂移觸發":"Active Subscribers YoY"}},{"id":"H3","text":"Utah ILC 銀行牌照開放存款第二曲線，把 funding cost 從 ~12% revolving 降到 ~4% deposit","columns":{"2Y 驗證點":"2026 正式向 Utah DFI 送件；FDIC 接受文件","5Y 驗證點":"FY28-29 charter approval、checking/savings 上線","10Y 驗證點":"完整銀行 stack ＋自有存款 funding base","具體數字門檻":"截至 2026-04，CEO 表示「尚未正式送件、不預期今年內獲批」；同業 ILC 案審核期常 2-3 年","信息來源":"Banking Dive（2026）ILC 報導；Youakim 公開表態","漂移觸發":"2026 年底前未送件 → 削弱；申請被拒 → 反轉。時程已較前次 DD「18 個月內」大幅拉長，本假設降權為選擇權而非基準"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"信用週期正常化——BNPL loss rate 升向 3-4%；次級放款簿老化使 vintage 違約現形","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"provision/GMV；30+ DPD；撥備增速 vs GMV 增速差","警戒閾值":"provision/GMV 連 2 季 ≥ 2.0%；單季 ≥ 3.0%；30+ DPD > 5%"}},{"id":"R2","text":"監管——NY／州級把訂閱費納入 16% 利率上限，壓縮 H2 訂閱引擎的 take rate；其他州跟進","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"NY DFS 規則定稿內容與生效時點（定稿後 180 天生效）；其他州立法","警戒閾值":"NY 定稿把訂閱費實質納入 APR；≥2 個大州跟進"}},{"id":"R3","text":"治理升級——集體訴訟正式起訴並取得程序進展、SEC 執法、或 CEO 質押強平引發賣壓","columns":{"對應假設":"H1+H2","時間尺度":"🐢 長期（2+ 年慢變數）／⚡ 質押強平為短期尾部","監測指標":"訴訟 docket 進展；SEC 動作；股價相對 CEO 質押抵押水位","警戒閾值":"任一集體訴訟通過程序認證；SEC 正式調查；股價急跌觸發保證金追繳"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"估值回落至 Fwd PE ~20x（$130-140），或治理與監管明朗（集體訴訟撤銷＋NY BNPL 規則以可承受形式定稿＋Utah ILC 正式送件）","irr_base_pct":6.0,"ev5y_pct":29.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"核心","signal":"B","val":"🟠","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.9,"ev5y_pct":29.0,"irr_base_pct":6.0,"max_dd_pct":-65.0,"bull_5y_price":388.0,"bear_5y_price":83.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"估值回落至 Fwd PE ~20x（$130-140），或治理與監管明朗（集體訴訟撤銷＋NY BNPL 規則以可承受形式定稿＋Utah ILC 正式送件）","price_at_dd":177.08,"archetype":"品質複利成長","cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名的每一個**（含程式稍後才會算的 asym_ratio／bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct／ev5y_pct／irr_base_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261005/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
