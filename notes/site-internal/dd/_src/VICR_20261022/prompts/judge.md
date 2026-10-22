你是 stock-analyst **v20 判斷 agent**，標的 VICR（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"VICR","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":197.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm"},"note":"未查證"},{"id":"f_kpi1_gaap","label":"毛利率（GAAP）","value":68.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm"},"note":"未查證"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益","value":72.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"百萬美元（利益率約 36.6%，由 72.148/197.114 推算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm"},"note":"未查證"},{"id":"f_kpi5_backlog","label":"在手訂單 backlog","value":406,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm"},"note":"不適用"},{"id":"f_kpi6","label":"現金及約當現金","value":513.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-20","period":"2026-10-20","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_vicr_gross_margin_pct","label":"VICR 毛利率","value":56.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VICR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vicr_operating_margin_pct","label":"VICR 營業利益率","value":18.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VICR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vicr_fcf_margin_pct","label":"VICR FCF 利潤率","value":10.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VICR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mpwr_gross_margin_pct","label":"MPWR 毛利率","value":55.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mpwr_operating_margin_pct","label":"MPWR 營業利益率","value":28.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mpwr_fcf_margin_pct","label":"MPWR FCF 利潤率","value":17.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_gross_margin_pct","label":"2308.TW 毛利率","value":35.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_operating_margin_pct","label":"2308.TW 營業利益率","value":16.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_fcf_margin_pct","label":"2308.TW FCF 利潤率","value":11.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vrt_gross_margin_pct","label":"VRT 毛利率","value":38.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_operating_margin_pct","label":"VRT 營業利益率","value":19.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_fcf_margin_pct","label":"VRT FCF 利潤率","value":25.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_gaap_eps","label":"GAAP 淨利／稀釋 EPS","value":1.33,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"美元/股（淨利 63.3 百萬）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm"},"note":"未查證"},{"id":"f_kpi4_69_7_16_1","label":"自由現金流（營運現金流 69.7 − 資本支出 16.1，推算）","value":53.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm（FCF 為自算）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":213.42,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-19.46,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":41.15,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.12 → 4.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.12 → 6.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.31 → 8.31）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":4.12,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.12,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":8.31,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":34.2,"period":"2026-07-16 → 2026-10-21","unit":"%","basis":"FY1 共識 EPS 3.07 → 4.12（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":55.72,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝7.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":7.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":17.55,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":16.65,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":51.8,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 4.12，分子＝快照價 213.42","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-10-22","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-22"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-505.98,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 7.16、現金 513.14（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":46.11,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":9334.12,"period":"2026-10-22","unit":"USD m","basis":"市值 9840.1 ＋ 淨負債 -505.98","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":642.1,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（4 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":943.02,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（4 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":14.54,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 213.42 / W52 198.16 / W104 124.38 / W250 82.75 / W250 13週斜率 2.44%"},{"id":"f_ma_w52","label":"52 週均線","value":198.16,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":124.38,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":82.75,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.44,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 自述：Vicor 在整體商用電源市場份額很小，競爭對手多為資源遠大於己的 IDM 與無晶圓廠電源半導體商；公司認為其差異化技術仍保有有利競爭位置。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"Despite our minor share in the overall merchant market and the competitive presence of numerous, far larger vendors in the market segments we serve with both Advanced Products and Brick Products, we believe we maintain an advantageous competitive position in those market segments based on our differentiated technology.","as_of":"2026-03-02","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：大型對手常以大幅折扣價守住份額與客戶關係，Vicor 可能無法跟進。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"Larger competitors frequently seek to maintain market share and protect customer relationships through heavily-discounted pricing, which we may not be able to match.","as_of":"2026-03-02","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"SemiAnalysis 報導 Monolithic Power 在 Nvidia H100 GPU 供電上取代 Vicor（2023 文章）。","source":"SemiAnalysis Newsletter: Energizing AI Power Delivery Competition","url":"https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition","excerpt":"However, Vicor’s fortunes have changed rapidly more recently given the dynamic nature of the power market. As we exclusively discovered and disclosed over a year ago, Monolithic Power Systems was able to supplant Vicor in Nvidia’s H100 GPU.","as_of":"2023-08-01","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Vicor 預期 2026 下半年與一家超大規模雲商及數家 OEM 接洽，相關專案最快 2027 年 Q3/Q4 量產；Advanced Products Q2 2026 營收 $94.2M、backlog 約 $380M。","source":"Zacks/Chartmill: Vicor Q2 Earnings Call Highlights AI Power and Fab Push","url":"https://www.chartmill.com/news/external/87162/vicor-q2-earnings-call-highlights-ai-power-and-fab-push","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K 風險因素：Vicor 成長取決於 OEM/ODM 開發新產品的步調、對 Advanced Products 的接受度與客戶產品成功；未提及第二供應商或自製的具體事件。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"Our growth is therefore dependent on: the pace at which these OEMs and ODMs develop their own new products; the acceptance of our Advanced Products by these OEMs and ODMs; and the success of the customers’ products incorporating our Advanced Products.","as_of":"2026-03-02","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"管理層稱競爭者仿製第一代 VPD 方案、且有專利與供應連續性風險；首要運算客戶處於晶圓級引擎陡峭量產爬坡，第二代 VPD 其他客戶接洽待其轉換之後（公司自述）。","source":"MarketBeat Vicor Q2 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/vicor-q2-earnings-call-highlights-2026-07-21/","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 載明 Advanced Products 營收相當大部分來自少數客戶；公司稱此集中反映技術採用早期，策略是先鎖定市場領先創新者。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"While, overall, the Company has a broad customer base and sells into a variety of industries, a substantial portion of the Company’s revenue from its Advanced Products line has been derived from a limited number of customers. This concentration of revenue is a reflection of the relatively early stage of adoption of the technologies, architectures and products offered in the Advanced Products line","as_of":"2026-03-02","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 風險因素：公司預期銷售將集中於相對更少的客戶，少數客戶的行動可能不成比例地影響經營結果。","source":"SEC EDGAR 10-K FY2025 Item 1/1A（WebFetch 讀取）","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"we expect to experience a greater concentration of sales among relatively fewer customers.","as_of":"2026-03-02","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Vicor Q2 2026 backlog $380M，較Q1的$301M季增26%、較去年同期增145%（8-K）","source":"Vicor Form 8-K Q2 2026 press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000751978/000119312526309538/d115827dex991.htm","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Vicor 2026-09-11 宣布購入New Hampshire Merrimack與Hooksett場址供ChiP Fab-2/Fab-3；Fab-1稼動率接近滿載；Fab-2約一年到初期部署（公司自述，無獨立佐證）","source":"Vicor press release 'Vicor acquires sites for additional ChiP fabs' (GlobeNewswire)","url":"https://energydigital.com/globenewswire/3360412","excerpt":null,"as_of":"2026-09-11","retrieved_at":"20261022","affects":["thesis.H","thesis.R","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Vicor管理層稱Andover Fab-1年產出可由約$10億升至至少$15億；Q1財報會議稱近期產能近乎售罄","source":"Yahoo Finance: Vicor Q1 earnings call highlights","url":"https://finance.yahoo.com/markets/stocks/articles/vicor-q1-earnings-call-highlights-144517950.html","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261022","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Citi預估全球800VDC在新增資料中心容量的採用率由2027年16.0%升至2030年79.1%","source":"The Standard (HK): AI data center power shift to 800VDC to reach 79pc adoption by 2030 Citi","url":"https://www.thestandard.com.hk/innovation/article/337678/AI-data-center-power-shift-to-800VDC-to-reach-79pc-adoption-by-2030-Citi","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Gartner預測至2027年40%的AI資料中心將受電力供應限制（2024年11月預測，屬電網端而非電源晶片端缺口）","source":"Gartner via Data Center Knowledge","url":"https://www.datacenterknowledge.com/energy-power-supply/power-shortages-will-restrict-40-of-ai-data-centers-by-2027-gartner","excerpt":null,"as_of":"2024-11-12","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"USITC 於 2026-10-09 依 Vicor 申訴啟動 Section 337 調查，涉及垂直電力輸送（VPD）系統，列 20 家被訴方（含 Delta、Infineon、Monolithic Power、Foxconn 等）；Vicor 為原告，屬專利執法非反壟斷","source":"USITC news release er1009","url":"https://www.usitc.gov/press_room/news_release/2026/er1009_69342.htm","excerpt":null,"as_of":"2026-10-09","retrieved_at":"20261022","affects":["moat_trend","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 Section 301 關稅成本約 $7.375M（較 2024 的 $4.189M 增 76.1%），占營收約 1.8%，壓低毛利率；已申請 duty drawback，2025 回收 $907K；2025 年 7 月起加收 10% 關稅附加費。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"For the year ended December 31, 2025, Section 301 Tariffs totaled approximately $7,375,000, an increase of 76.1% compared to $4,189,000 incurred for 2024.","as_of":"2026-03-02","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2025 年對中國與香港出口約 $48.3M，占營收約 11.9%；產品屬 EAR99，不需出口許可。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"our products are designated EAR99 commodities under the Export Administration Regulations of the U.S. Department of Commerce and are not subject to export licenses","as_of":"2026-03-02","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子指出美國持續擴大實體清單，出口管制規則與中美政府行動的影響不確定，可能對業務造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"In recent years, the U.S. government has continued to expand the number of foreign entities on the Entity List (a restricted party list that imposes additional licensing requirements on shipments to listed parties).","as_of":"2026-03-02","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Vicor 10-K FY2025 稱先進產品與部分半導體由有限數量晶圓代工廠製造，封裝與測試由少數第三方處理；並稱尚未因美中貿易爭端（含 2018 年 Section 301 關稅）出現重大延遲或原料供給減少。","source":"Vicor Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":null,"as_of":"2026-02-27","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"policyrisk.com 彙整：中國（含香港）占 Vicor 淨營收約 11.9%（2025）、12.6%（2024）、17.7%（2023）；美國對中先進運算晶片出口管制被公司列為不確定風險。（二手整理）","source":"policyrisk.com VICR company page","url":"https://policyrisk.com/world/company/VICR","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"FY2022 10-K：已於 2020–2022 年為部分大量原料與零件合格化非中國供應商","source":"Vicor Form 10-K FY2022","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312523053976/d425264d10k.htm","excerpt":"We continue to evaluate alternative sources of raw materials, and in 2020, 2021, and 2022 we qualified non-Chinese vendors for certain high-volume raw materials and components.","as_of":"2023-03-01","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026（截至9/30）產品與權利金營收$197.1M，季增約37.5%、年增約78.5%；毛利$134.7M（Q2 $83.1M、去年同期$63.5M）。Q3 分段未取得。","source":"Vicor 8-K Exhibit 99.1（2026-10-20 新聞稿）","url":"https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 Advanced Products（含權利金）季增45%至$94.2M，Brick 季增2.4%至$49.2M；Advanced 占營收65.7%；Q2 含新授權約$15M權利金。","source":"MarketBeat Q2 2026 call highlights","url":"https://www.marketbeat.com/instant-alerts/vicor-q2-earnings-call-highlights-2026-07-21/","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 期末 backlog 約$380M，季增26%、年增145%；管理層預期2026全年營收逾$600M，需求超過產能、交期略增；長期目標$2.5B營收、70%毛利率。","source":"Vicor Q2 2026 call 逐字稿摘要（roic.ai）","url":"https://www.roic.ai/quote/VICR/transcripts","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"競爭：ADI（含Empower）、MPS、TXN、Infineon 等；分析稱 Vicor 在部分 Nvidia GPU 平台輸給較低成本的整合方案而失去 socket。未找到市佔或價格趨勢的量化資料。","source":"Chartmill / Easternprogress 二手分析","url":"https://www.chartmill.com/news/external/80627/vicor-stock-outlook-as-ai-demand-capacity-and-royalties-align","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q1 2026 book-to-bill 高於2，一年期 backlog $300.6M、季增70%。","source":"Chartmill 彙整","url":"https://www.chartmill.com/news/external/80627/vicor-stock-outlook-as-ai-demand-capacity-and-royalties-align","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"0","claim":"MarketsandMarkets：資料中心加速器市場2025年$170.81B至2030年$372.68B","source":"MarketsandMarkets","url":"https://www.marketsandmarkets.com/Market-Reports/data-center-accelerator-market-48984803.html","excerpt":"According to Marketsandmarkets, the global data center accelerator market size was valued at USD 170.81 billion in 2025 and is projected to reach USD 372.68 billion by 2030, growing at a CAGR of 16.9% from 2025 to 2030.","as_of":"2025-10-10","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子載明電源系統產業競爭激烈、技術變動快、產品快速過時，成熟產品有價格侵蝕；公司策略押注差異化 Advanced Products，並稱無法保證新產品獲客戶接受。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"The power system industry and the industries in which many of our customers operate are characterized by intense competition, rapid technological change, quickened product obsolescence, and price erosion for mature products, each of which could have an adverse effect on our results of operations.","as_of":"2026-03-02","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"聚合文章稱 Vicor、MPS、Infineon 皆推垂直／封裝上供電設計；並有 ADI 傳聞以約 15 億美元收購 Empower（未證實）。","source":"borecraft.com 報導","url":"https://borecraft.com/?p=15174","excerpt":"Analog Devices’ reported $1.5B Empower bid targets vertical power delivery By NewMaxx / May 19, 2026 Direct:","as_of":"2026-05-19","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Vicor Q1 2026 電話會議稱競品方案電流密度不足，並反駁 800V 轉 6V 匯流排架構。","source":"Yahoo Finance Vicor Q1 earnings call highlights","url":"https://finance.yahoo.com/markets/stocks/articles/vicor-q1-earnings-call-highlights-144517950.html","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 揭露的銷售通路為直銷團隊、歐亞非庫存授權經銷商，加上 Arrow、Digi-Key、Avnet、Mouser 四家庫存經銷商；直銷聚焦高量 Advanced Products 的全球 OEM／ODM。文件未描述通路或商業模式的結構性轉變。","source":"SEC EDGAR 10-K FY2025 Item 1 Marketing and Sales","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"We reach and serve customers through several sales channels: a direct sales force; independent, authorized non-stocking distributors in Europe and Asia; and four authorized stocking distributors world-wide: Arrow Electronics, Inc., Digi-Key Corporation, Avnet Electronics, and Mouser Electronics, Inc.","as_of":"2026-03-02","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Vicor 擴大智慧財產授權業務，視授權金為高毛利、與硬體互補的收入管道","source":"IIPLA News","url":"https://iipla.org/news/vicor-advances-long-term-growth-through-expanded-intellectual-property-licensing","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 彙整 4 位分析師平均目標價 $382、最高 $450、最低 $320；Needham 2026-07-21 由 $400 降至 $320，Craig-Hallum 2026-06-22 由 $400 升至 $450（快照日期不一，未標 as-of）","source":"Benzinga VICR price-targets","url":"https://www.benzinga.com/quote/VICR/price-targets","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Investing.com 共識頁平均 12 個月目標價 386.25 美元，高 450、低 320（快照日未知；另一頁顯示 406.25，高 450、低 375，較舊）","source":"Investing.com VICR consensus estimates","url":"https://www.investing.com/equities/vicor-corp-consensus-estimates","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-09-30 公司將 Q3 季增指引由 >20% 上調至 >30%，原因為首筆 VPD 非獨家授權的權利金；Q3 實績（10-20 公布）產品與權利金營收 $197.1M，季增 37.5%，毛利率 68.3%，稀釋 EPS $1.33","source":"Finviz/Vicor 公告彙整；SEC 8-K","url":"https://finviz.com/news/397273/vicor-corporation-raises-q3-2026-revenue-guidance","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 公布前第三方共識歧異：MarketBeat EPS $1.32／營收 $187.03M，Benzinga $0.79／$158.6M，Earnings Whispers $0.71／$160M；Benzinga 列 Q4 2026 營收共識 $198.9M（非公司指引，未查到公司 Q4 指引）","source":"MarketBeat／Benzinga／Earnings Whispers","url":"https://www.benzinga.com/quote/VICR/earnings-forecasts","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 實績與指引新聞稿","source":"SEC 8-K Exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2024年7月由放空者提起的證券集體訴訟（In re Vicor Securities Litigation），被告於2025年1月20日聲請駁回；10-K 附註16 載明該案。","source":"SEC EDGAR 10-K FY2025 Note 16","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"The Defendants filed their motion to dismiss the amended complaint on January 20, 2025 and, on June 6, 2025, the U.S.…","as_of":"2026-03-02","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"2025年5月1日與多方就智財糾紛達成和解，公司收到 4,500 萬美元，並支付 510 萬美元法律費用。","source":"SEC EDGAR 10-K FY2025 Note 16","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"a total of $45,000,000 was paid to the Company in May 2025 (collectively, the “patent litigation settlement”). The Company incurred $5,100,000 in legal fees in connection with the patent litigation settlement","as_of":"2026-03-02","retrieved_at":"20261022","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"2026-08-25 董事會核准新的 1.5 億美元庫藏股授權，取代舊計畫。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526370420/d161606d8k.htm","excerpt":"the Company announced that its Board of Directors approved a new share repurchase authorization for the repurchase of up to $150,000,000 of shares of the Company’s common stock","as_of":"2026-08-27","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 7 份 8-K 中僅 1 份含重大項目（8.01 庫藏股）；無併購類項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000751978&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單無 1.01／2.01 等併購類項目，僅 8.01 庫藏股。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000751978&type=8-K","excerpt":"其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"放空者提起的證券集體訴訟，2025年1月聲請駁回；Foley 稱法院於2025年6月無偏見駁回。","source":"SEC EDGAR 10-K FY2025 Note 16","url":"https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm","excerpt":"The Defendants filed their motion to dismiss the amended complaint on January 20, 2025 and, on June 6, 2025, the U.S.…","as_of":"2026-03-02","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"VICR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.63,"operating_margin_pct":18.64,"fcf_margin_pct":10.82,"rd_intensity_pct":17.58},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VICR","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"MPWR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.2,"operating_margin_pct":28.72,"fcf_margin_pct":17.8,"rd_intensity_pct":12.62},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2308.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.69,"operating_margin_pct":16.78,"fcf_margin_pct":11.7,"rd_intensity_pct":8.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"VRT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.04,"operating_margin_pct":19.4,"fcf_margin_pct":25.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"VICR"},"financial_history":{"ticker":"VICR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":399079000.0,"revenue_yoy_pct":null,"gross_margin_pct":45.24,"operating_margin_pct":8.44,"net_income":25446000.0,"diluted_eps":0.57,"free_cash_flow":-41027000.0,"fcf_margin_pct":-10.28,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":405059000.0,"revenue_yoy_pct":1.5,"gross_margin_pct":50.59,"operating_margin_pct":12.68,"net_income":53595000.0,"diluted_eps":1.19,"free_cash_flow":41076000.0,"fcf_margin_pct":10.14,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":359058000.0,"revenue_yoy_pct":-11.36,"gross_margin_pct":51.24,"operating_margin_pct":5.07,"net_income":6129000.0,"diluted_eps":0.14,"free_cash_flow":27240000.0,"fcf_margin_pct":7.59,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":452701000.0,"revenue_yoy_pct":26.08,"gross_margin_pct":57.31,"operating_margin_pct":18.08,"net_income":118556000.0,"diluted_eps":2.61,"free_cash_flow":119230000.0,"fcf_margin_pct":26.34,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/VICR/VICR_Q3_2026_Earnings_Call_20261020.md）

# Q3 2026 Earnings Call
**Vicor Corporation** | Earnings Calls | 2026-10-20

**Operator** (Operator):
Ladies and gentlemen, thank you for standing by. Welcome to the Third Quarter 2026 Vicor Earnings Conference Call. [Operator Instructions] Please be advised that today's conference is being recorded. I would now like to turn the conference over to Jim Schmidt, Chief Financial Officer. Please go ahead.

**James Schmidt** (Executives):
Thank you. Good morning, and welcome to Vicor Corporation's earnings call for the third quarter ended September 30, 2026. I'm Jim Schmidt, Chief Financial Officer; and I'm in Andover with Patrizio Vinciarelli, Chief Executive Officer; and Phil Davies, Corporate Vice President, Global Sales and Marketing.  
Earlier this morning, we issued a press release summarizing our financial results for the 3 and 9 months ended September 30, 2026. This press release has been posted on the Investor Relations page of our website, www.vicorpower.com. We also filed a Form 8-K today related to the issuance of this press release. 
I remind listeners, this conference call is being recorded and is the copyrighted property of Vicor Corporation. I also remind you various remarks we make during this call may constitute forward-looking statements for purposes of the safe harbor provisions under the Private Securities Litigation Reform Act of 1995. 
Except for historical information contained in this call, the matters discussed on this call, including any statements regarding current and planned products, current and potential customers, potential market opportunities, expected events and announcements and our capacity expansion as well as management's expectations for sales growth, spending and profitability are forward-looking statements involving risks and uncertainties. 
In light of these risks and uncertainties, we can offer no assurance that any forward-looking statement will, in fact, prove to be correct. Actual results may differ materially from those explicitly set forth in or implied by any of our remarks today. The risks and uncertainties we face are discussed in Item 1A of our 2025 Form 10-K, which we filed with the SEC on March 2, 2026. This document is available via the EDGAR system on the SEC's website. 
Please note the information provided during this conference call is accurate only as of today, Tuesday, October 20, 2026. Vicor undertakes no obligation to update any statements, including forward-looking statements made during this call, and you should not rely upon such statements after the conclusion of this call. A webcast replay of today's call will be available shortly on the Investor Relations page of our website. 
I'll now turn to a review of our Q3 financial performance, after which Phil will review recent market developments, and Patrizio, Phil and I will take your questions. In my remarks, I will focus mostly on the sequential quarterly changes for P&L and balance sheet items and refer you to our press release or our upcoming Form 10-Q for additional information. 
As stated in today's press release, Vicor recorded product and royalty revenue for the third quarter of $197.1 million, up 37.5% sequentially from the second quarter of 2026 total of $143.4 million and up 78.5% from the third quarter of 2025 total of $110.4 million. Advanced Products revenue, which includes royalty revenue, increased 47.5% sequentially to $138.9 million, and Brick Products revenue increased 18.4% sequentially to $58.3 million. 
Royalty revenue increased 119.1% sequentially to $66.6 million. A fraction of this increase due to initial royalty payments from the new licensee was nonrecurring. As we add more licensees, growth in royalty revenues will be less lumpy. Shipments to stocking distributors increased 24.8% sequentially and increased 16.2% year-over-year. Exports for the second quarter decreased sequentially as a percentage of total revenue to approximately 36.1% from the prior quarter's 46%. 
For Q3, Advanced Products share of total revenue increased to 70.4% compared to 65.7% for the second quarter of 2026, with Brick Products' share correspondingly decreasing to 29.6% of total revenue. 
Turning to Q3 gross margin. We recorded a consolidated gross profit margin of 68.3%, a 1,030 basis point increase from the prior quarter. Q3 gross margin increased 1,080 basis points from the same quarter last year. Gross margin improved both as a result of increased royalty revenue as well as better product gross margins as we achieved gains in volume, efficiency and mix. 
I'll now turn to Q3 operating expenses. Total operating expense increased 29.6% sequentially from the second quarter of 2026 to $62.5 million. Within operating expense, legal expense, a substantial portion of which is contingent on royalty revenue, increased by approximately $11.1 million from the second quarter to $16.1 million. On a run rate basis, we expect legal expense to average approximately 20% of royalty revenue in the near term. 
The amounts of total equity-based compensation expense for Q3 included in cost of goods, SG&A and R&D was $1.203 million, $2.655 million and $1.483 million, respectively, totaling approximately $5.3 million. 
Turning to income taxes. We recorded a tax provision for Q3 of approximately $15.4 million, representing an effective tax rate for the quarter of 19.6%. Net income for Q3 totaled $63.3 million. GAAP diluted income per share was $1.33 based on a fully diluted share count of 47,609,000 shares. 
Turning to our cash flow and balance sheet. Cash and cash equivalents totaled $513.1 million in Q3, an increase of $59.6 million sequentially. Accounts receivable net of reserves totaled $102.5 million at quarter end, with DSOs for trade receivables at 34 days. Inventories net of reserves increased 6.2% sequentially to $110.9 million. Annualized inventory turns were 2.3. Cash flow provided by operating activities totaled $69.7 million for the quarter. 
Capital expenditures for Q3 totaled $16.1 million. We ended the quarter with a construction in progress balance primarily for manufacturing equipment of approximately $26.4 million and with approximately $48.6 million remaining to be spent. 
I'll now address bookings and backlog. Q3 book-to-bill came in above 1 and 1-year backlog increased 7% from the prior quarter, closing at $406 million. 2026 is the year in which Vicor's innovative products and technology licensing practice came into focus within the industry. With incremental capacity, we expect a 10% increase in Q4 product revenue and at least $43 million in royalty revenue, assuming no new license agreements are closed this quarter. 
To achieve the product revenue growth objective, we are expecting another double-digit sequential increase in product revenue in our Advanced Products portfolio. In Q3, we achieved operating ratios for both profitability and expense approaching our long-term financial model. Further revenue growth will result in further margin expansion. Phil?

**Philip Davies** (Executives):
Thank you, Jim. Demand across our main business segments and in our IP licensing practice is strong with $100 million in bookings in the first 2 weeks of Q4, which included a large order for second-generation VPD modules from our lead customer. 
The purchase of 2 sites for Chip Fab-2 and Chip Fab-3 reflects the need to expand capacity in support of increased demand. Substantial capacity expansion will be necessary based on AI industry trends and customer enthusiasm for our second-generation VPD. Meetings held with major hyperscalers and OEMs at last week's Open Compute confirmed that first-generation VPD systems using VRs, which infringe Vicor patents, are struggling to keep up with the requirements of next-generation AI systems. Our targeted audience was impressed by Vicor's second-generation VPD with its distinct manufacturability and performance advantages. 
Open Compute this year focused on 800-volt DC rack distribution through inefficient intermediate bus voltages from 12 volts to 6 volts or possibly 1.8 volts to a point of load approaching 0.5 volts, underscoring the inherent limitations of VRs and IVRs. Lack of adequate current density and current gain at the point of load sets the stage for broader adoption of Vicor's second-generation VPD, providing high current density and much higher current gain. 
With its transient performance eliminating voltage undershoots, Vicor's proprietary all-FPA enables a 10% to 15% reduction in AI processor power loss with over 40x the current gain of IVRs and 3x the current density of VRs. Demo systems for second-generation VPD and all FPA have been set up in our Silicon Valley applications laboratory and are available for selected OEM and hyperscaler engagements. 
On the licensing front, we granted our first VPD license to a leading AI OEM based on Stage 2 unit royalty rates and responded to inquiries from 2 hyperscalers seeking all-inclusive licenses quoted at Stage 2 and Stage 3 prior to the recent ITC decision to investigate VPD infringement. Even though leading OEMs have already obtained a license to our VPD patents, others may not have yet realized that they are importing or planning to import infringing products. 
Catching their attention, Vicor has requested the ITC to issue a limited exclusion order barring importation of unlicensed computing systems that infringe Vicor's VPD, like the ITC did before in an earlier investigation involving our NBM patents. As hyperscalers and other OEMs come to realize the impact of an importation ban, they will take licenses based on escalating royalty rates established in our licensing practice, which favors early adopters. 
The decision to focus on a set of top 100 customers and top channel accounts or TCAs with our global distribution partners across our 4 markets and 4 regions globally is clearly paying off with both bookings and opportunity pipeline growth. Our customers are on the cutting edge of high-growth applications with the toughest power delivery challenges and specifications. Our leading ATE customers for ASIC and memory test systems, which now represents over $100 million in annual revenues shows no signs of slowing down, and we are actively discussing capacity reservations to ensure supply in coming years. 
Major new product introductions are also underway in our industrial and aerospace and defense businesses with market expansion now occurring with new nontraditional companies that have entered the A&D market with new autonomous technologies. Successful execution is achieved with focus, and we are very focused. 
Thank you, and we will now take your questions.

**Operator** (Operator):
[Operator Instructions] 
And the first question is going to come from Quinn Bolton with Needham & Company.

**Quinn Bolton** (Analysts):
Congratulations on the strong product and licensing outlook. I guess I wanted to start, Jim, just you had mentioned that the royalty revenue in the third quarter of $66.6 million did include some catch-up royalties. Wondering if you could help size that in the third quarter? And then I've got a couple of follow-ups.

**James Schmidt** (Executives):
It might be best to just think about the $43 million that I mentioned, Quinn, as the baseline amount that we can count on now with no new deals as a starting point for Q4.

**Patrizio Vinciarelli** (Executives):
Yes so thinking -- Quinn, thinking about this, what's the meaning of nonrecurring? I think that which was level nonrecurring has been recurring pretty periodically, right? So as we pointed out, in Q3, there was a contribution that is nonrecurring. But then early in Q4, we got some other contribution. 
So I think we should all expect that our licensing income is going to be growing, while we're still in a licensing arrangement with a relatively small subset of all of the hyperscalers and OEMs. It is still going to be lumpy. There's going to be more "nonrecurring contributions." It's not going to be until there's a crossing of the chiasm with respect to the need to license Vicor technology for freedom to operate in AI applications given the strong component of a Vicor IP that is inherently involved in these systems. 
But with some lumpiness, it is going to be a significant growth business that we're now estimating to reach levels next year and the year after that beyond the levels that I had forecasted a year ago.

**James Schmidt** (Executives):
And Quinn, I'll just add to what Patrizio said, it's better for, I think, the audience and the analysts to think about the royalty stream as recurring now and not a nonrecurring activity, just to put it in perspective. The nature of the agreements are recurring.

**Quinn Bolton** (Analysts):
Got it. Yes. No, I think I understand that if you sign new licenses, there may be catch-ups with those additional license agreements, but the $43 million sounds like a good go-forward base. And then obviously, we can add on to that as the company signs new licenses. 
I wanted to turn to the second and third chip fab. I think we're all expecting you to announce a second site. So it was great to see you announce both a second and a third site. But can you give us a sense for the second site, when would you think that, that facility would come online and begin contributing to product revenue? Is that a sort of 12-month time line? Is it 18 months? What's a good sort of time line for investors to be thinking about with that second site?

**Patrizio Vinciarelli** (Executives):
We're likely going to have some initial equipment deployment in Q2 -- Q2 of '27.

**Quinn Bolton** (Analysts):
And would that be able to produce sort of full set? Or is that just first equipment deliveries, Patrizio?

**Patrizio Vinciarelli** (Executives):
Yes. So it's going to be incremental steps with respect to those processes where we first ran into capacity limitations in Fab-1, right? So in Fab-2, we're going to bring up lines that address the shorter-term limiting factors and move on from those to other ones.

**Quinn Bolton** (Analysts):
Got it. So it may not be sort of full production in the mimic of Fab-1, but you'll bring in those production steps where you're most constrained. So the impact would be to increase the company's total manufacturing beginning in the second quarter?

**Patrizio Vinciarelli** (Executives):
That's right, yes. For those process steps where we still have ample capacity at Federal Street, there is no need, there is no rush to deploy additional equipment there. So we're going to be able to do it incrementally and more cost effectively and more predictably.

**Quinn Bolton** (Analysts):
Got it. And then the last one for me. Phil, you mentioned good meetings at Open Compute last week. And just kind of wondering if you could address what kind of demand are you seeing for the factorized power, the 48 core solutions as the VRs and IVRs do look increasingly challenged. When do you think you might see sort of adoption of a second-gen VPD outside of your lead customer based on some of those conversations?

**Philip Davies** (Executives):
So conversations are still early, Quinn, in that regard. We do have line of sight to new chips that are under development that are sort of further out, if you like. But I do think that there could be opportunities in the shorter term based upon the inefficiencies of VRs and IVRs. So we'll be taking a look at that as we move forward.

**Patrizio Vinciarelli** (Executives):
So again, we're looking at all these opportunities in [ December ] reference of capacity limitations over the next 12 months. It's not that we can engage with any hyperscaler OEM that has got a need. Virtually, all of them do. Because as you know well, there's been a lot going on with respect to an 800-volt bus and converting that to 6 volts or 12 volts or back to 6 volts on the way to 1.8 volt. 
The real issue with respect to enabling AI doesn't have to do with what happens in effect some distance away on 800-volt bus or even intermediate bus, the real constraints have to do with the point of load. And they have to do, as we've been articulating because of the fact that IBA, the intermediate bus architecture, which is how the competitive industry has been doing it, is gathering in tension between efficient power distribution and efficient duty cycle and the requisite current density and current gain at the point of load. 
As I've been saying for quite some time, I think all the focus about 800 volt is really missing the boat with respect to the real challenge. It's not that there isn't a benefit to 800 volt. There is a benefit. It's a few percentage points of system efficiency. But in that point of load, power system will keep AI from progressing on its performance trajectory, and that's what we're focused on.

**Operator** (Operator):
And our next question is going to come from Justin Clare with ROTH Capital Partners.

**Justin Clare** (Analysts):
First, I wanted to start off. So backlog increased to $406 million this quarter. And I was just wondering if you could discuss the visibility that you have now into kind of fully utilizing Fab-1, when you expect to reach that milestone. So just looking beyond the backlog, kind of what visibility do you have into additional customer orders or commitments from customers that would support that full utilization?

**Patrizio Vinciarelli** (Executives):
So as of yesterday, the backlog is actually closer to $400 million. But beyond that, we see robust demand. Phil and I were on a call yesterday with a major customer seeing demand doubling every year for the next several years. And they have a lot of visibility with respect to the request for their systems. 
So the challenge in the short term is to bring up additional capacity to do so ahead of demand, taking care of customers. We have many customers, most customers that are single source with us, where we have obviously a particular responsibility with respect to ensuring that we're not going to be getting their growth. A lot of it is directly AI related, but some of it is indirectly related in that the AI growth path is fueling, as you know, a growth path for all of the portions of the industry that play one support role or another.

**Justin Clare** (Analysts):
Got it. Okay. And then just shifting to the capacity announcements here that you made for Fab-2 and Fab-3. I was wondering if you could just clarify, you indicated that those additional sites could increase capacity nearly 5x. Is that 5x figure related to kind of physical manufacturing space, production output or revenue-generating capacity? And I'm just wondering if you could potentially share what the revenue potential might be as you move from Fab-1 to Fab-2 and Fab-3, assuming full utilization of those facilities?

**Patrizio Vinciarelli** (Executives):
So around Fab-1, we are space constrained. In other words, we have a relatively small parcel of land. So we made sure with both Fab-2 and Fab-3 to avoid getting limited by, in effect, elbow room within that particular site. Both sites have significant upside that could support even more than a 5x expansion. 
And again, the methodology for expanding capacity, as you might recall, we looked first at just industrial parcels, then looked at buildings in order to reduce the time to accessing a new facility. We ended up doing one of each within a triangle is about 30 miles off to the west and to the north of Fab-1, relatively short distance, but with a significant level of dependency with respect to power fees and all that would be a consideration regarding redundancy with respect to this incremental capacity. The 5x is a conservative number. It could be more than that because, again, unlike Fab-1, we're not going to be limited by elbow room within either one of these sites.

**Justin Clare** (Analysts):
Got it. Okay. And then just one more. Wondering if you could share what you expect in terms of the capital investment for Fab-2 and Fab-3 and what the anticipated timing of that investment would be?

**Patrizio Vinciarelli** (Executives):
So we are not prepared to share any details today. We're in the planning phase with respect to Fab-2. I think possibly as of our next conference call, we will share some quantitative data with respect to capital investment. But it's safe to say that we're going to be able to fund Fab-2 and in due course, Fab-3 without need for raising any capital. We're adding cash at an increasing rate. And Fab-2, with this investment, is well within our capability. We want to make a dent with respect to our cash flow.

**Operator** (Operator):
And the next question is going to come from Richard Shannon with Craig-Hallum Capital Group.

**Richard Shannon** (Analysts):
Jim, I'd love to put the numbers you mentioned in your prepared remarks here to get to a fourth quarter revenue number. You mentioned a royalty number. I think you mentioned Advanced Products' growth or total product growth, I'm not sure which one. That was coming up with revenues kind of in the $180 million to $185 million range for the fourth quarter. Am I doing the math right? Or if not, can you correct me?

**James Schmidt** (Executives):
I'm going to give you a specific question (sic) [answer], but I do want to make clear, Richard, that the number I quoted for 10% product revenue growth is total product revenue growth, okay? And what I said about Advanced Products' revenue growth within Advanced Products will be yet again another double-digit increase in that category of products.

**Patrizio Vinciarelli** (Executives):
Let me give you more color with respect to this. So as we discussed earlier, the licensing side of the business has got lumpiness, potential for additional deals. We are taking the long-term horizon. We're not in a hurry to get any deal done. As time goes on, the cost to hyperscalers and OEMs for VPD license goes up at a pretty fast clip as we progress through the investigation of the ITC. 
But there could be deals done this quarter. And for that reason, we really can't give you a guidance that we would be comfortable with given the level of uncertainty. And for that reason, what we provided with in terms of helping you set expectations is with respect to products side, that which we can predictably expect to deliver, which is a low double-digit increase in product revenue, right, hardware revenue, separate apart from licensing income for which we provided a minimum of $43 million, and that assumes no new deals are done within Q4.

**James Schmidt** (Executives):
Richard, one other point to mention. The $43 million, as we've said and Patrizio just said, doesn't rely on any new deals. But inherent in the licensing agreement we have, there's potential for incremental royalty revenue just as a function of the existing arrangement, and we can't predict that exactly.

**Patrizio Vinciarelli** (Executives):
That's right. So it could be that the number that we are forecasting at the minimum of $43 million ends up larger than that even without new deals. So it's a very conservative number.

**Richard Shannon** (Analysts):
It's a baseline, and that's what investors like to see. So I just want to verify that. 
My second question is related to licensing kind of the notion of run rate here. You mentioned kind of a $43 million run rate, again, assuming nothing else gets done, and let's start with that notion in mind here. You've mentioned that most of the licenses you've done here in the past have been 2-year terms here. And I think the first one is coming up for renewal and will be expired in the not-too-distant future. And so I want to get a sense of your expectation of renewals of those so that we can assume a real recurring run rate that's going to go for many quarters in a row. So if you could comment on that, that would be great, please.

**Patrizio Vinciarelli** (Executives):
Yes. So I think it's becoming more and more apparent that Vicor pioneer role with respect to a density power system is multifaceted, right? As of -- as recently as a year ago, even within a shorter time frame, all the focus was on NBMs as part of IBA sort as a stepping stone to the pal road for competitive alternatives. Again, we don't use NBMs because the factorized power system doesn't require intermediate bus converter, but virtually all of the competitive alternatives do. 
The focus clearly has recently shifted to VPD, which is on a different scale of significance, right? Its significance in terms of enabling AI power systems is much greater than NBMs because it's not the intermediate bus converter, but it's the point of load system, which is where the spotlight, where the focus should be. And so there is greater value associated with that, and we're capturing that value. We capture that value with the first VPD license. We'll be capturing that value with additional VPD licenses or inclusive licenses that involve the combination of NBMs, VPD and other vital technology that over time is also to become an issue for unscrupulous competitors to contend with.

**Operator** (Operator):
And the next question will come from [ John Dillon ] with DNB Capital.

**Unknown Analyst** (Analysts):
Congratulations to the whole Vicor team, incredible quarter. Phil, my question is really for you. It's, with the exception of Vicor, I've never heard of any company claiming that power supplies could enable higher performance processors. Yet Cerebras just announced a new CS4 AI processor and Angela Yeung, the Senior VP of Products, stated that the wafer scale engine stayed the same as the CS3. 
So the CS3 had the same memory and logic, but had 2x the increase in speed. And with 3 of these together, they had 10x the throughput of 3 wafers. And she contributed a big part of the increase was the ability to deliver higher density power to the same wafer. So Phil, I find this extraordinary. Can you walk us through that and let us know what the reactions are from your new target customers now that you're demonstrating the benefits of the second-gen VPD?

**Patrizio Vinciarelli** (Executives):
So John, we're not going to make any comments that are specific to any customer, right? I'm going to answer your question in general terms with specificity.
Every generation of AI processor is stepping up its current requirements by a dramatic percentage increase. What used to be very high current requirements not that long ago, a few hundred amps, right, following the era of Intel processors that were barely consuming 100 amps. It's now at the 1,000 amp level and on its way to thousands of amps. And then there are leading-edge applications such as wafer-scale engines where you're dealing with tens of thousands of amperes going to 100,000 amperes. 
That's where the action is. That's where inference and other AI enabling capabilities get realized, and they're fundamentally fueled by current. They're fueled by current at ever decreasing voltages, which makes factorized power with current multiplication, the technology of choice. And conversely, fundamentally handicaps the competitive approach where the upper voltage is, in effect, averaged down by mixing a low-voltage source, i.e., one that is inefficient in terms of its power distribution with ground, which is fundamentally [ Joules ].
That kind of technology is inherently handicapped with respect to keeping up with AI demands. And conversely, our technology was envisioned a long time ago, and we kept on improving it, right? We got lots of new developments related to factorized power, it's IP, it's components. And these are reflected in the level of performance that we're bringing out with every new generation, right? 
The initial demonstration wiggles for second-gen VPD reached 3 amps per square millimeter. We are not that far away from a 5, 6 amp per square millimeter capability. We're going from what used to be in a time frame where we're powering a GPU many, many years ago with current multipliers to the level of 3, 3.5 millimeters, we're now 1.5 millimeter. In 6 months, we're going to be at 1 millimeter. So it's this kind of technology, the packaging technology, power conversion engines, control systems, unique components that enables AI.

**Philip Davies** (Executives):
So John, just to build on that, I think just to build on what Patrizio said, I think that, that was on display last week at Open Compute with our meetings with several big customers in terms of their level of excitement around our second-generation VPD. They've been waiting a while to see it. We've been focused on our lead customer. But now we're here. We've got the demo system set up. They were excited by what we showed them. So I think it's now up to us to roll this forward and to bring these deals home.

**Patrizio Vinciarelli** (Executives):
Within our capacity constraints -- near-term capacity constraints.

**Unknown Analyst** (Analysts):
Okay. Now before you've talked about pricing per watt. So with twice the power with the fifth gen solutions, are average selling prices going up?

**Patrizio Vinciarelli** (Executives):
Let's not get into that. I think what we can say is that our total competitive standing, which obviously leads with performance, but needs to deal with cost is becoming stronger and stronger because we have the right approach to solving these point-of-load challenges. And with that right approach, inherently, there are scalability and cost advantages that will materialize as we scale up from a nearly full Fab-1 to Fab-2 and Fab-3. We're going to have the economies of scale. We believe we're on the right track and the rest of the industry is foolishly going down at that end road.

**Unknown Analyst** (Analysts):
Excellent. And the IVR customers you mentioned last time, how is that progressing? And that will be my last question.

**Philip Davies** (Executives):
So again, as we talked about, John, IVRs, it's very early days for IVRs in terms of really delivering solutions to customers. They're intrigued by using IVRs on some of the rails. I think for the high current rails, we have the best solution. So it might be all Vicor. It might be some Vicor and some IVRs. We don't know yet. We'll see how that plays out. But IVRs have a way to go yet in terms of proving their performance sort of claims.

**Patrizio Vinciarelli** (Executives):
So we had several meetings last week on the IVR front with 2 IVR companies and an hyperscaler interested in solutions, IVR solutions, using one of these 2 companies. And so we were told by the hyperscaler that when it comes to feeding the IVRs at 1.8 volt, we will be the only solution. 
I think it remains to be seen. The jury is still out with respect to how soon these IVRs will become a practical reality. The good news is that the hyperscalers saw that we have a solution that doesn't involve IVRs. So fundamentally, they can come to us for either alternative, one that involves IVRs with that which IVRs provide, which is to be honest and fair, they provide flexibility, at least now in theory. But in reality, they will, over time, provide flexibility. But that flexibility comes at a significant cost. 
Whenever you sit down and you deal with the real numbers, not the marketing numbers, the insertion cost to, in effect, process power through an IVR stage is close to -- it's upwards of 10%, and it could be pretty close to 15%. And for that 10%, 15% of extra power dissipation, all that you're getting, all that the customer is getting is a current gain of 2.5. Now, it does provide flexibility. But from a power system efficiency perspective, it's a very challenged proposition. 
We're open-minded though. We're perfectly willing, eager to play a support role with respect to IVR application. And fundamentally, the same point-of-load technology enables us to deliver dozens of apps at 0.5 volts with the requisite current density, bandwidth and all the right attributes. That same technology can deliver 1.5 volt to an IVR. And if customers, for whatever combination of reasons, want to go down that path, we'll be there to support them.

**Operator** (Operator):
And our next question will come from Richard Shannon with Craig-Hallum Capital Group.

**Richard Shannon** (Analysts):
Let me ask a follow-on here. In the press release and in the call here today, you've used a couple of terms that I'm unfamiliar with, Stage 2 and Stage 3 licenses. If you can explain those, that would be a big help here.

**Patrizio Vinciarelli** (Executives):
Yes, I'd be happy to. Actually, if you go to our website, we now have a licensing page. And on the licensing page, you can get an answer to the question. And it's a quantitative answer to the question as it relates to royalty rates, which change as a function of the stage. 
So fundamentally, for any Vicor patent in our portfolio that has not been asserted, a prospective licensee can take a license at Stage 0. That's the most cost-effective license. It is most cost effective because Vicor has an edge to get into deals with law firms to assert the IP and go through, in effect, the enforcement effort. But if the patents are being infringed and we have to assert them to the fact that there's a cost to doing that as time progresses and the enforcement effort advances, we increase the royalty rate in relationship to what we call Stage X. 
So after Stage 0 comes Stage 1, 2, 3. So 3 begins when the ITC institutes an investigation. And the first roughly 10 months of that time frame, which is during all the phases of the ITC process before a hearing, we have increments in the royalty rate, as you can see from the website page at the level of about 5% per month. As we get into the hearing and then the initial determination by the administrative law judge at the ITC, the final determination, an exclusion order and enforcement of the exclusion order by Customs and Border Patrol, the cost to, in effect -- late licensee that in effect, has taken a wait-and-see attitude or has approached this from the perspective of taking its chances, it keeps escalating because our cost has gone up. And with that, we deserve to fetch more with respect to the patent and its value. 
So all of this is intended to encourage early adoption, encourage licensee not to take their chances, not to roll the dice. We got a track record of knowing what we're doing, and we're going to keep doing that. And we're very determined that we're very well equipped with partners that have a vested interest in the right outcome, which is not the case for our opponents. So that's how the various stages of this process relate to time and the cost of the license, its royalty rate. And if you look at the web page, there are curves that define this progression. 
And part of the reason for this is to have a level playing field, right? It's very important that we treat each and every licensee fairly. All of these licensees have got most favored the licensee provisions, which means that you can grant to a following licensee a license on better terms than a prior licensee under similar conditions. Well, similar conditions, among other things, means at what stage the prior licensee took a license as compared to a new licensee. So we have documented our practice, among other things, to ensure that we have a complete transparency and fairness and consistency in our methodology.

**Richard Shannon** (Analysts):
Patrizio, thanks for that detail here, and I see the web page here, very comprehensive and complete. My follow-on question is regarding the AI OEM that you signed a license with in the third quarter. A 2-part question. The first one is, why was that seemingly mostly a nonrecurring or onetime license versus something that might be ongoing? And second of all, can you state which stage this third quarter AI OEM was licensed at?

**Patrizio Vinciarelli** (Executives):
So we didn't say that that's nonrecurring to the contrary. Maybe, the source of potential confusion was my comment to the fact that, that which has been characterized now several times as nonrecurring keeps recurring. So by definition, it's not nonrecurring. 
But beyond that, what we recorded in Q3 from this first pure VPD license is far from nonrecurring, whichever way you want to look at that word. In fact, there was at the beginning of Q4, another significant license PO that came from the same new licensee. So these licenses are structured, whether they're all inclusive or per unit to be, in effect, proportionate to the use of the technology by the licensee. 
And obviously, as time goes on and licensees make greater use, they pay royalties in direct proportion to that. We have different ways of making this happen, fundamentally 2 approaches, either on a per unit basis or by estimating what the use by the licensee is going to be over a couple of years and having an all-inclusive license that deals with that time frame before we take on the next couple of years.

**James Schmidt** (Executives):
Richard, just to amplify what Patrizio said, it's better to think about the royalty revenue as recurring, okay? It's a licensing practice that is now up and running. It's generating royalty revenue. It's proportional to the use of what otherwise would have been infringing technology. So it's very important that everybody understand that. We've used a couple of quarters of catch-up, but really think about this as recurring revenue now. It's in the P&L.

**Patrizio Vinciarelli** (Executives):
They keep on coming at increasing levels. So I think it was perfectly appropriate, let's say, a couple of years ago to look at a lump sum contribution in one quarter as nonrecurring. Back then, that was obviously the conservative way to think about it. But now to Jim's point, obviously, there's been a lot of recurrences of nonrecurring things, and they're no longer nonrecurring.

**Operator** (Operator):
And our next question will come from Justin Clare with ROTH Capital Partners.

**Justin Clare** (Analysts):
Just wanted to follow up on the capacity expansion here, particularly for Fab-3. Wondering how we should interpret the land acquisition that you made for Fab-3 at this point. Is that a commitment to add additional capacity? Or is that -- or should we view that more as an option to potentially accommodate longer-term growth? And then just trying to think through how long it might take for you to get to fully utilizing 5x the capacity that you have with Fab-1.

**Patrizio Vinciarelli** (Executives):
So we bought that land. We closed a week ago or thereabouts. So -- but we're not going to act on it in terms of putting up a building there for now. The logic of having that flexibility was in effect, to make the most of the process that we went through earlier this year in investigating these various options that carry different trade-offs, right? 
So on a new campus, we have total flexibility with respect to the complement of buildings, how they relate to each other in terms of next fabs. That's very valuable in terms of medium, longer-term planning as distinct from the need to act in the very short term with respect to expanding capacity within an existing building. So we now have the wherewithal to take very short-term steps with the time scale of 5, 6 months on the one hand, within existing infrastructure, including a 330,000 square foot building as well as doing it from the ground up in a different site. 
We're going to act first on the Fab-2, which is in Merrimack to the west of Andover. And it's yet to be determined when we want to pull a trigger on Fab-3. Again, Phil and I yesterday were having a call with the CEO of a major customer wanting to, in effect, reserve capacity over the next few years. These kinds of discussions are going to facilitate decisions with respect to when to pull the trigger on the next incremental capacity.

**James Schmidt** (Executives):
And it might be worth mentioning the call they had was not with an AI customer.

**Justin Clare** (Analysts):
Okay. Interesting. And then just one other follow-up. You mentioned that you plan to, I think, start adding equipment in Q2 for Fab-2. And so just wondering, do you anticipate running at near full capacity for Fab-1 next year and that kind of justifies the ramp-up of Fab-2 into next year?

**Patrizio Vinciarelli** (Executives):
Yes. Yes. So unfortunately, for the near term, we have certain capacity limitations, right? And they are, to be clear, dependent on specific platforms related to particular process steps. They are such that we can grow revenues. As Jim pointed out earlier, we expect low double-digit increase in product revenues this quarter. But as we've been explaining over the last several calls, we're getting closer to getting to full capacity utilization of Fab-1, hence, the need to step with some of the process steps into Fab-2 starting Q2 of next year.

**Operator** (Operator):
Thank you. And this is all the time that we do have for questions today. So this will conclude today's conference call, and thank you for participating, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### VICR_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO｜guidance：CFO 給 Q3 營收約增 10%、2026 全年營收逾 6 億美元（原話："we expect a nearly 10% increase in Q3 revenue"）
- 2026-07-21｜CFO｜guidance：計畫 Advanced Products 產品營收連續季增雙位數（原話："we are planning for double-digit sequential increases in"）
- 2026-07-21｜CFO｜guidance：財測對授權採保守假設，新授權可能要等第二個 ITC 案 2027 年終裁（原話："this guidance is based on conservative assumptions"）
- 2026-07-21｜CFO｜guidance：新授權權利金會計認列：Q2 認列 1,500 萬，Q3 降為 500 萬，之後每季 1,000 萬（原話："contribute $5 million in Q3 and $10 million per quarter"）
- 2026-07-21｜CFO｜margin：Q2 合併毛利率 58%，季增 280 基點（原話："gross profit margin of 58%, a 280 basis point"）
- 2026-07-21｜CFO｜margin：產品毛利率受 fab 內搬移設備的一次性費用拖累，無法資本化（原話："did not get capitalized and cannot be capitalized"）
- 2026-07-21｜CFO｜margin：CFO 稱隨稼動率與吸收提高，產品毛利率將回升（原話："there will be a lift in the GM, product GM going forward"）
- 2026-07-21｜CFO｜margin：Q2 營運費用季增 6.1%，主因授權案的或有律師費大增（原話："substantial increase in contingent legal expenses"）
- 2026-07-21｜CFO｜customer：Advanced Products 營收季增 45% 至 9,420 萬美元（原話："Advanced Products revenue increased 45% sequentially"）
- 2026-07-21｜CFO｜customer：訂單出貨比大於 1，一年期在手訂單季增 26% 至 3.797 億（原話："1-year backlog increased
26% from the prior quarter"）
- 2026-07-21｜CEO｜customer：被問在手訂單增加有多少來自新授權，答相對很少（原話："Relatively little."）
- 2026-07-21｜CEO｜customer：ATE 市場來自關鍵客戶的業務量為過去的數倍，歸因於 AI 建置（原話："a large
multiple of what it has been in past years"）
- 2026-07-21｜Sales VP｜customer：銷售主管稱訂單出貨比低於先前近 2 的水準，但各終端市場強勁（原話："I don't see any weakness at all going forward."）
- 2026-07-21｜Sales VP｜commitment：新財務目標：營收 25 億美元、毛利率 70%、營業利益率 40%，取代 2023 年的 10 億／65%（原話："$2.5 billion in revenues at 70% gross margins"）
- 2026-07-21｜CEO｜capital_allocation：CEO 明言達 25 億營收必須有第二座晶圓廠（原話："It's going to take a second fab to get there."）
- 2026-07-21｜CEO｜capital_allocation：第二廠選址仍在進行，數週內可能決定（原話："we'll probably be making decisions in the next few
weeks"）
- 2026-07-21｜CEO｜capital_allocation：選址對象可支援第一廠的 2 至 3 倍規模（原話："as much as 2x, potentially 3x the first fab."）
- 2026-07-21｜CEO｜capital_allocation：第二廠分階段建置，初期約使產能加倍，避免過早折舊（原話："unnecessary or premature depreciation"）
- 2026-07-21｜CFO｜capital_allocation：Q2 現金 4.536 億美元，7/13 收到 CHIPS 法投資稅額抵減退稅 1,430 萬（原話："Cash and cash equivalents totaled $453.6 million in Q2"）
- 2026-07-21｜CEO｜risk：第一廠接近滿載，但稱尚未售罄，將挑選參與的案子（原話："We're not sold out, but we're approaching capacity"）
- 2026-07-21｜CEO｜risk：第一廠產能上限仍未定，且比一年前的目標高很多（原話："will top out is, I think, yet TBD"）
- 2026-07-21｜CEO｜risk：交期略為拉長，管理層稱與產業趨勢一致（原話："Lead times have stretched out a little bit"）
- 2026-07-21｜CEO｜product：第二代 VPD 基線 3 A/mm² 已完成開發，年底至明年初要超過 5 A/mm²（原話："raising the bar past 5 amps
per square millimeter"）
- 2026-07-21｜Sales VP｜product：本季起向選定客戶提供第二代 VPD 開發系統與工具（原話："development systems and tools starting this quarter"）
- 2026-07-21｜Sales VP｜product：預期明年第三季末至第四季進入量產爬坡（原話："late third quarter, fourth quarter of next year"）
- 2026-07-21｜CEO｜product：有兩家公司找上門，希望 Vicor 提供 IVR 部署所需的關鍵構件（原話："We've been approached by 2
companies wishing us to provide a building block"）
- 2026-07-21｜CEO｜competition：CEO 稱競爭者實際只能做到略高於 1 A/mm²（原話："slightly over 1 amp per square millimeter"）
- 2026-07-21｜CEO｜competition：CEO 稱產業依賴負載點電壓調節器的路線有根本缺陷（原話："That's fundamentally a flawed strategy."）
- 2026-07-21｜CEO｜competition：第二貨源：短期重心轉向自控的第二座晶圓廠，與替代來源討論的時程不符近兩年擴產所需（原話："a shift with respect to relative focus"）
- 2026-07-21｜CEO｜competition：授權對象涵蓋任何 OEM 與超大規模業者，不含競爭者（原話："It does not involve competitors."）
- 2026-07-21｜CEO｜customer：Q2 新授權首兩年不含採購關係，但預期與第二代 VPD 搭配納入未來關係（原話："does not, for the first couple of years, provide for a"）
- 2026-07-21｜CEO｜customer：授權對象公開揭露為多家 OEM、目前一家超大規模業者（原話："a multiplicity of OEM licensees, one hyperscaler as of now"）
- 2026-07-21｜CEO｜commitment：CEO 拒絕預測 25 億目標中授權收入占比，只稱未來數年授權收入將顯著擴大（原話："a significant expansion in licensing income in years to come"）

### VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md
- 2026-06-19｜Philip Davies｜guidance：宣布長期目標營收由10億美元提高到25億美元（原話："target revenue from $1 billion to $2.5 billion"）
- 2026-06-19｜Philip Davies｜margin：新長期目標毛利率與營業利益率（原話："gross margins from 65% to 70% and operating income of 40%"）
- 2026-06-19｜James Schmidt｜guidance：安靜期，不評論Q2及未來財務表現（原話："Vicor is in its quiet period for the second quarter of 2026"）
- 2026-06-19｜Patrizio Vinciarelli｜guidance：CEO談25億目標時程：不願推測（原話："it would be, I think, unwise for me to speculate"）
- 2026-06-19｜Patrizio Vinciarelli｜guidance：CEO稱25億可能很快達成但不給時點（原話："But I won't tell you exactly when for various reasons."）
- 2026-06-19｜Philip Davies｜margin：工業業務2027年底前倍增（原話："well on track to do that by the end of 2027"）
- 2026-06-19｜Philip Davies｜customer：工業設計導入與設計贏單數量以「數千萬」描述（原話："they're tens of millions, okay?"）
- 2026-06-19｜Philip Davies｜customer：ATE領先客戶已下大額早期訂單（原話："has placed large early orders for this chipset"）
- 2026-06-19｜Philip Davies｜product：新ATE晶片組第四季推向其他ATE公司（原話："we'll be launching that chipset out to all the other ATE"）
- 2026-06-19｜Philip Davies｜product：航太國防新增AC-DC，可觸及SAM 8.5億美元（原話："offers us a new $850 million SAM to target"）
- 2026-06-19｜Philip Davies｜competition：航太國防產品功率密度為最近競爭者5到10倍（原話："5 to 10x the nearest competitor"）
- 2026-06-19｜Philip Davies｜customer：衛星聚焦LEO/MEO，不做低成本星鏈類（原話："We're focused on LEO and MEO, where performance matters"）
- 2026-06-19｜Philip Davies｜competition：稱產品功率密度為最近競爭者3到10倍（原話："3 to 10x the power density of our nearest competitor"）
- 2026-06-19｜Philip Davies｜competition：批評NVIDIA與OCP的800V轉6V架構選擇（原話："bad power architecture choice being made by NVIDIA"）
- 2026-06-19｜Philip Davies｜risk：領先客戶時程比去年股東會所示晚約9個月（原話："we're about 9 months later than what we showed you"）
- 2026-06-19｜Philip Davies｜risk：時程延後原因為系統層訊號完整性需新增隔離式電流倍增器（原話："development of a new isolated current multiplier"）
- 2026-06-19｜Philip Davies｜product：2027年Q1電流密度提升47%（原話："a step-up of 47% in current density"）
- 2026-06-19｜Philip Davies｜commitment：領先客戶預量產與早期量產預計2027年Q4末（原話："will probably start towards the end of 4Q '27"）
- 2026-06-19｜Philip Davies｜commitment：第三季向策略客戶提供開發板（原話："development board that will be provided to our strategic cus"）
- 2026-06-19｜Patrizio Vinciarelli｜product：CEO提議以提前投入治具縮短Q1'27時程（原話："we may be able to beat the Q1 '27 time line"）
- 2026-06-19｜Patrizio Vinciarelli｜product：電流倍增比由40:1升到56:1（原話："from 40:1 to 56:1"）
- 2026-06-19｜Patrizio Vinciarelli｜competition：CEO糾正：競品方案昂貴而非真正商品化（原話："it's actually extremely expensive"）
- 2026-06-19｜Patrizio Vinciarelli｜competition：CEO糾正副總對競爭者為商品的說法（原話："he referred to the competition in AI market as commodity"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：第二貨源夥伴尚未定案（原話："on second thoughts, they may not be the best choice"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：第二貨源決策不急（原話："We shouldn't feel compelled to make an instant decision."）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：七月初與更大公司洽談（原話："I'm having some conversations at the beginning of July"）
- 2026-06-19｜Patrizio Vinciarelli｜customer：最新授權客戶約一個月前簽約，談判3到4週（原話："the license came about a month ago"）
- 2026-06-19｜Patrizio Vinciarelli｜commitment：授權結構個案不同，已有談判方法（原話："a structure, a methodology for negotiating these deals"）
- 2026-06-19｜Patrizio Vinciarelli｜customer：授權戶數：最大AI OEM兩份（原話："the largest OEM in AI, we've had 2 licenses"）
- 2026-06-19｜Patrizio Vinciarelli｜risk：ITC第二案進行中，將有更多（原話："The second one is in progress. There's going to be more."）
- 2026-06-19｜Patrizio Vinciarelli｜guidance：Q2財測上調來自產品需求與新授權（原話："The second one is in progress."）
- 2026-06-19｜Patrizio Vinciarelli｜commitment：新產線預計Q3末Q4初投產（原話："operational by the end of Q3, beginning of Q4"）
- 2026-06-19｜Patrizio Vinciarelli｜product：VPD約占今年營收15至20%（原話："In '27, it will jump to a substantially larger percentage."）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：第二廠已洽購土地與建物（原話："We made a number of offers for both plots of land"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：現有聯邦街廠產能今年底明年初到極限（原話："gets to its limits as we get to the end of this year"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：現有廠產能目標由10億擴至15億美元（原話："has been expanded to the $1.5 billion level"）
- 2026-06-19｜Patrizio Vinciarelli｜product：第二代VPD每片面板營收可約倍增（原話："raise the revenue per panel by about 2x"）
- 2026-06-19｜Patrizio Vinciarelli｜product：CS4單顆電流倍增器電流輸出近乎倍增（原話："deliver double the current or nearly double the current"）
- 2026-06-19｜Patrizio Vinciarelli｜commitment：CEO對需求與製造能力表示百分之百有信心（原話："100% confidence both with respect to the demand"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：產能緊時將更挑選客戶與應用，可能不再接NBM（原話："We may not want to take on more NBM business."）
- 2026-06-19｜Patrizio Vinciarelli｜customer：新授權費率今年為明年一半（原話："the royalty rate this year is half of the royalty rate"）
- 2026-06-19｜Patrizio Vinciarelli｜guidance：授權貢獻2億至3億美元屬保守數字（原話："$200 million, $300 million contribution from licensing"）
- 2026-06-19｜Patrizio Vinciarelli｜commitment：將加快ITC行動節奏（原話："We're going to be accelerating that pace."）
- 2026-06-19｜Patrizio Vinciarelli｜customer：電動車尚無大型OEM平台突破（原話："We haven't had that breakthrough, right, with a big OEM"）
- 2026-06-19｜Patrizio Vinciarelli｜risk：電動車歐洲一家客戶明年量產（原話："going to ramp into production next year"）
- 2026-06-19｜James Schmidt｜capital_allocation：拆股議題僅早期討論（原話："it's a very, very early kind of conversation"）
- 2026-06-19｜Patrizio Vinciarelli｜customer：領先客戶明年占比可能25%至30%（原話："certainly, a significant step-up next year could be 25%, 30%"）
- 2026-06-19｜Unknown Executive｜guidance：明年航太國防加工業約占50%，其餘為高效能運算（原話："it's probably aerospace and defense, industrial, about 50%"）
- 2026-06-19｜Patrizio Vinciarelli｜risk：對太空資料中心持懷疑（原話："I'm a bit skeptical with respect to that"）

### 問答異常語氣（迴避／改口／保留）
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：第二代 VPD 設計定案是否會在 2027 下半年放量｜答法：CEO 明說不對具體日期做承諾，改談客戶興趣與競爭者能力
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：是否仍預期明年 Cerebras 占營收 25%–30%｜答法：CEO 不談客戶具體數字，僅稱關係良好，未回答該比例是否仍成立
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：Cerebras 在 Q2 是否為 10% 客戶｜答法：CEO 反問是否能說；CFO 稱留待 10-Q 揭露，並稱不確定是否達 10%
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：扣除權利金後產品毛利率比前幾季低約數百基點，趨勢是否反轉｜答法：CEO 先以「Jim 提過毛利率會增加」帶過，未給數字，CFO 補述一次性設備搬遷費用與稼動率
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：25 億目標中權利金是否占 50%｜答法：CEO 稱無法對組合做具體預測，改談授權前景
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：OEM 具備第二貨源能力是否成真及進度｜答法：CEO 未直接回答是否會成為第二貨源，改稱重心轉向自控的第二座晶圓廠，並稱「不是長期策略改變」
- VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md｜問：分析師問工業設計導入/贏單的具體數字｜答法：先說有數字但不能展示，拒絕私下提供，僅說「tens of millions」
- VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md｜問：Q2財測上調1400萬美元中多少來自權利金｜答法：CFO稱屬營運問題；CEO只答兩項貢獻（產品需求與新授權），未給比例
- VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md｜問：25億美元目標是3、5或10年｜答法：稱可能很快也可能較久，不願預測時點，「won't tell you exactly when」
- VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md｜問：第二廠何時完成交易、何時預生產｜答法：說不能告知何時成交，只談已出價與產能壓力

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
{"date":"20260524","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Fab 1 ramp 至 $1.5B run-rate：管理層 4/21/26 法說明確路徑，process bottleneck 已識別 + 部分外包 + 收購鄰近建物為過渡","columns":{"2Y 驗證點":"FY27 全年 product revenue（剝離 royalty）≥ $1.2B（Q4 26 run-rate 至少 $300M/季）","5Y 驗證點":"FY30 product revenue $2.5-3.0B（Fab 1 滿載 + Fab 2 ramp 50%）","10Y 驗證點":"10Y 維持 $3B+ 與第二代 VPD 架構替代風險之間取得平衡","具體數字門檻":"FY27 product rev ≥ $1.2B；Q4 26 季 run-rate ≥ $300M","信息來源":"4/21/26 Q1 26 法說、4/22/26 transcript","漂移觸發條件":"連 2 季 product rev YoY &lt; 15% → 削弱；連 3 季 &lt; 10% → 反轉（QC-34 採 TTM 過濾）"}},{"id":"H2","text":"IP licensing 進入結構化年收入 $80-120M run-rate：ITC LEO 強制執行後 hyperscaler 排隊上桌；管理層公開預期 2025-26 settlement contribution ~$300M","columns":{"2Y 驗證點":"FY27 royalty revenue ≥ $80M（FY25 $57.4M 基期）","5Y 驗證點":"FY30 royalty $100-150M（加上對 Delta / Foxconn 二輪訴訟成功）","10Y 驗證點":"10Y 取決於 '761 + '481 專利 2028-2030 到期前能否成功取得下一代 VPD 專利布局","具體數字門檻":"FY27 royalty ≥ $80M；單一 hyperscaler license 公告金額 ≥ $50M","信息來源":"2025/10/20 IP licensing practice press release；2025 IP rev growth +23.2%","漂移觸發條件":"連 4 季 royalty &lt; $15M（即年化 $60M）→ 削弱；單一大客戶 license 終止 → 反轉"}},{"id":"H3","text":"Trailing PE 從 89x 收斂至「FY27 ramp 兌現後」40-50x 區間：EPS 兌現 + 共識 catch-up，市場逐步認可 sustainable 25-30% CAGR 而非 2026 一次性 inflection","columns":{"2Y 驗證點":"FY27 末 trailing PE ~40-45x（股價未來 24 個月可維持平穩 / 緩漲，等 EPS 補上來）","5Y 驗證點":"FY30 trailing PE 25-30x（成長放緩至 15-20% CAGR 對應）","10Y 驗證點":"10Y PE 跟同等 quality 工業 / 半導體公司收斂至 20-25x（如 ADI / TXN tier）","具體數字門檻":"FY27 末 trailing PE ≤ 45x 且 ROIC &gt; 25%","信息來源":"歷史對標 MPWR 2018-2022 / ASML 2014-2018 inflection 期 PE 軌跡","漂移觸發條件":"5Y 假設，連 4 季 TTM 偏離 ≥ 5% 才削弱（QC-35：5Y 假設連 4 季）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"單一大客戶 attribution risk — Cerebras 為 lead customer，集中度極高；若 Cerebras 自身 funding round / NVDA 競爭壓力造成減單，Vicor 短期 product revenue 立即可見","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"季度 product rev QoQ 顯著下滑；管理層在法說提到「one major customer ramp delay」","警戒閾值":"單季 product rev QoQ -10%+；連 2 季觸發即減倉"}},{"id":"R2","text":"Fab 1 capacity 撞牆 + Fab 2 推遲 — process bottleneck 排除進度不如預期，或 Fab 2 建物收購談判破裂，2027 run-rate 卡在 $1B 而非 $1.5B","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"backlog QoQ 從 $300M 平 / 跌；管理層 Q4 26 / Q1 27 法說對 Fab 2 timeline 從 2028H2 改口至 2029","警戒閾值":"backlog 連 2 季 QoQ -5%+ 或單季 -15%+；book-to-bill 跌破 1.3；連 4 季觸發大動作（QC-35：5Y 假設連 4 季）"}},{"id":"R3","text":"NVDA / hyperscaler 扶持替代陣營 — Vicor royalty 索取過度 → NVDA 在 Rubin / Vera Rubin 公開支持 MPWR 或 Infineon 的 next-gen single-stage GaN 方案 → 25% 市佔 2027 目標推遲至 2030+","columns":{"對應假設":"H1, H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"NVDA 法說 / GTC 公開 power partner 名單；OCP power spec 變化；MPWR / Infineon 法說明確宣告 next-gen GPU socket win","警戒閾值":"NVDA Rubin / VeraRubin 公開供應商名單缺 Vicor；MPWR Q2-Q3 26 法說明確點名 attaching to NVIDIA digital power；需 ≥ 50% 機率才砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":267.99,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
