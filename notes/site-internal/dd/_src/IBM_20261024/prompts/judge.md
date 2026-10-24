你是 stock-analyst **v20 判斷 agent**，標的 IBM（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"IBM","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":17103,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","citation":"IBM Q3 2026 新聞稿（8-K Ex.99.1）"}},{"id":"f_kpi1_operating_non_gaap","label":"Operating（non-GAAP）稅前利益","value":3295,"period":"Q3 FY2026（公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（公告於 2026-10-21）","citation":"IBM Q3 2026 新聞稿（8-K Ex.99.1）"}},{"id":"f_kpi2_gaap","label":"GAAP 稅前利益","value":2497,"period":"Q3 FY2026（公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（公告於 2026-10-21）","citation":"IBM Q3 2026 新聞稿（8-K Ex.99.1）"}},{"id":"f_kpi3_operating_non_gaap_eps","label":"Operating（non-GAAP）EPS","value":2.95,"period":"Q3 FY2026（公告於 2026-10-21）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（公告於 2026-10-21）","citation":"IBM Q3 2026 新聞稿；超預期幅度取自媒體彙整（非 IR）"},"note":"媒體報導高於華爾街預期 $0.08（隱含約 $2.87，未以 IR 驗證）"},{"id":"f_kpi6_fy2026","label":"管理層全年指引（FY2026）","value":"固定匯率營收成長 4%–5%（維持）；FCF 年增逾 $10 億（上調）","period":"Q3 FY2026（公告於 2026-10-21）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（公告於 2026-10-21）","citation":"IBM Q3 2026 新聞稿（8-K Ex.99.1）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-21","period":"2026-10-21","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-21"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ibm_gross_margin_pct","label":"IBM 毛利率","value":58.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ibm_operating_margin_pct","label":"IBM 營業利益率","value":18.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ibm_fcf_margin_pct","label":"IBM FCF 利潤率","value":19.02,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_acn_gross_margin_pct","label":"ACN 毛利率","value":32.01,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACN.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_acn_operating_margin_pct","label":"ACN 營業利益率","value":15.75,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACN.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_acn_fcf_margin_pct","label":"ACN FCF 利潤率","value":17.21,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACN.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_orcl_gross_margin_pct","label":"ORCL 毛利率","value":63.96,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ORCL.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_orcl_operating_margin_pct","label":"ORCL 營業利益率","value":34.23,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ORCL.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_orcl_fcf_margin_pct","label":"ORCL FCF 利潤率","value":-40.01,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ORCL.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_msft_gross_margin_pct","label":"MSFT 毛利率","value":67.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msft_operating_margin_pct","label":"MSFT 營業利益率","value":46.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msft_fcf_margin_pct","label":"MSFT FCF 利潤率","value":20.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hpe_gross_margin_pct","label":"HPE 毛利率","value":36.73,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HPE.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_hpe_operating_margin_pct","label":"HPE 營業利益率","value":7.84,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HPE.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_hpe_fcf_margin_pct","label":"HPE FCF 利潤率","value":9.93,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HPE.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_fcf","label":"自由現金流（FCF）","value":3027,"period":"Q3 FY2026（公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（公告於 2026-10-21）","citation":"IBM Q3 2026 新聞稿（8-K Ex.99.1）"}},{"id":"f_kpi5_sbc_operating","label":"SBC 占 operating 稅前利益","value":16.2,"period":"Q3 FY2026（公告於 2026-10-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（公告於 2026-10-21）","citation":"自算：SBC 535 ÷ operating 稅前利益 3,295（SBC 取自新聞稿）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":253.56,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":10.9,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_rsi14","label":"RSI(14)","value":71.22,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.42 → 12.42）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.08,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.23 → 13.24）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（14.48 → 14.48）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":12.42,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":13.24,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":14.48,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.73,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 12.33 → 12.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":20.42,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 12.42，分子＝快照價 253.56","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.658,"period":"2026-10-24","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-24"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 253.56 / W52 258.54 / W104 250.24 / W250 184.07 / W250 13週斜率 1.09%"},{"id":"f_ma_w52","label":"52 週均線","value":258.54,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":250.24,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":184.07,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.09,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"IBM 10-K 列出各業務線主要對手（軟體：Google、Amazon、Microsoft、Oracle、Salesforce、SAP 等；顧問：Accenture、Capgemini、印度服務商；基礎設施：Dell、HPE 等），並稱公司「經常面對新競爭者」，自述為各業務線領先者之一。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231.htm","excerpt":"Across our business segments, we recognize hundreds of competitors worldwide and as we execute our hybrid cloud and AI strategy, we are regularly exposed to new competitors.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"第三方分析（依 SEC 申報）：2026 年第二季基礎設施營收下滑 7.4%，IBM Z 大型主機營收年減 42.0%；全年軟體成長預期下修至 6%–8%（原 10% 以上）。頁面未提供份額數據。","source":"sec-api.io insights：IBM stock after the Q2 2026 guidance cut","url":"https://sec-api.io/insights/ibm-ibm-stock-after-the-q2-2026-guidance-cut-software-growth-confluent-acquisition-debt-dividend-cover-and-scenarios-to-fy2029","excerpt":"Infrastructure fell 7.4% with IBM Z mainframe revenue down 42.0%","as_of":"2026-10-12","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"IBM FY2025 10-K：無客戶占總營收 10% 以上（2023–2025）","source":"IBM Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231.htm","excerpt":null,"as_of":"2026-02-24","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"IBM FY2025 10-K：2025、2024、2023 年無任何客戶占總營收 10% 以上","source":"IBM Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231_d2.htm","excerpt":null,"as_of":"2026-02-24","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"IBM 2026 年 Q3 10-Q 列示評等：S&P A-、Moody's A3、Fitch A-，與 6 月底相同","source":"IBM Form 10-Q period ended 2026-09-30 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000051143/000005114326000095/ibm-20260930.htm","excerpt":"Service Fitch Ratings Senior long-term debt A- A3 A- Commercial paper A-2 Prime-2 F1 We have financial flexibility, supported by our strong liquidity position and cash flows, to operate at a single A credit rating.","as_of":"2026-10-22","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"IBM 2026 Q2 後下調全年財測（二手分析文章）","source":"sec-api insights: IBM stock after the Q2 2026 guidance cut","url":"https://sec-api.io/insights/ibm-ibm-stock-after-the-q2-2026-guidance-cut-software-growth-confluent-acquisition-debt-dividend-cover-and-scenarios-to-fy2029","excerpt":"22 July 2026 and kept guidance for free cash flow on its own measure to rise about $1bn; the FY2026 Software growth expectation moved to 6% to 8% from 10% or more (earnings call, 22 July 2026). Net debt was $53.81bn at 30 June 2026 against $46.79bn at 31 December 2025, on debt of $61.99bn and cash, restricted cash and marketable securities of $8.18bn, after the Confluent acquisition closed on","as_of":"2026-10-12","retrieved_at":"20261024","affects":["thesis.R","triggers"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"IBM 10-Q（截至 2026-06-30）：z17 於 2025-06 推出、為史上最強的大型主機開局，但 Q2 2026 低於預期，主因 IBM Z 及相關軟體（主要為交易處理）短缺；Network World 報 z 主機營收該季年減 42%。","source":"IBM Form 10-Q FY2026 Q2 / Network World","url":"https://www.sec.gov/Archives/edgar/data/0000051143/000005114326000078/ibm-20260630.htm","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"IBM 歸因 Q2 缺口為客戶把預算轉去採購供給吃緊的伺服器、儲存、記憶體以搶在漲價前；2026 營收成長指引由「>5%」下修為 4–5%；管理層稱 z17 為史上最佳換機週期、未見客戶離開大型主機（公司說法）。","source":"Network World：Despite tough quarter, IBM says mainframe will continue to put the big in Big Blue","url":"https://www.networkworld.com/article/4200347/despite-tough-quarter-ibm-says-mainframe-will-continue-to-put-the-big-in-big-blue.html","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261024","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"2025-02 投資人日：IBM 長期營收成長目標 >5%/年，軟體中期目標 10%、基礎設施 1–3%；Bloomberg 報分析師對 FY2026、FY2027 平均預期約 4% 固定匯率成長。查無 2028 共識。","source":"Benzinga/Goldman Sachs：IBM Story Is Underappreciated","url":"https://www.benzinga.com/analyst-ratings/analyst-color/25/02/43504732/ibm-story-is-underappreciated-goldman-sachs-says-stock-can-re-rate-higher","excerpt":null,"as_of":"2025-02-25","retrieved_at":"20261024","affects":["valuation","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026-04-10 美國司法部與 IBM 就 False Claims Act 達成 1,710 萬美元和解，指控涉及不實證明遵守反歧視要求（非反壟斷案）。","source":"Digital Policy Alert｜DOJ investigation into IBM over alleged false certification of compliance with anti-discrimination requirements","url":"https://digitalpolicyalert.org/change/19078-department-of-justice-investigation-into-international-business-machines-corporation-ibm-over-alleged-false-certification-of-compliance-with-anti-discrimination-requirements","excerpt":null,"as_of":"2026-04-10","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"IBM CEO Krishna 稱監管環境對 AI 併購「更友善」（2026 年 3 月報導）；2026 年搜尋未見針對 IBM 的新反壟斷調查、拆分或 DOJ/FTC/EU 競爭案，反壟斷搜尋結果皆為 2009–2011 年舊案（EU 與 DOJ 大型主機調查）。","source":"Bloomberg Law｜IBM CEO Sees More AI Deals in 'Friendlier' Regulatory Climate","url":"https://news.bloomberglaw.com/tech-and-telecom-law/ibm-ceo-sees-more-ai-deals-in-friendlier-regulatory-climate","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"IBM 10-K 風險因素：業務遍及 175 國以上、約六成營收來自美國以外，並列出貿易關係惡化（adverse changes in trade relationships）為可能影響業績的因素；未見針對關稅或出口管制的 IBM 專屬量化揭露。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231.htm","excerpt":"The company is a globally integrated entity, doing business in over 175 countries worldwide and deriving about sixty percent of its revenues from sales outside the United States.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"IBM CEO Krishna 表示伊朗戰爭與地緣不確定性開始影響展望，影響主要經由客戶端","source":"idnfinancials: IBM CEO Arvind Krishna: Iran war starts to weigh on outlook","url":"https://www.idnfinancials.com/news/63279/ibm-ceo-arvind-krishna-iran-war-starts-to-weigh-on-outlook","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"IBM Q3 2026（2026-10-21 公布）營收 $17.1B，年增 5%（固定匯率 6%）；軟體 $7.8B +8%（固定匯率 +9%，Red Hat 及混合雲 +11%、資料 +19%、交易處理 +9%）；顧問 $5.3B 持平（固定匯率 +2%）；基礎設施 $3.7B +4%（固定匯率 +5%），其中 IBM Z -20%；全年固定匯率營收成長指引維持 4–5%","source":"Constellation Research, IBM delivers strong Q3, sees 4% to 5% revenue growth in 2026","url":"https://www.constellationr.com/insights/news/ibm-delivers-strong-q3-sees-4-5-revenue-growth-2026","excerpt":null,"as_of":"2026-10-21","retrieved_at":"20261024","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"IBM Q2 2026 Z 大型主機營收年減 42%，IBM 稱為 z17 週期尾段及客戶把六月底資本支出轉向供給吃緊的伺服器／儲存／記憶體；全年營收成長指引由 >5% 下修至 4–5%；管理層稱 z17 為史上最佳換機週期、無客戶離開大型主機的證據","source":"AI Weekly, IBM Cuts 2026 Outlook as Q2 Mainframe Revenue Falls 42%","url":"https://aiweekly.co/alerts/ibm-cuts-2026-outlook-as-q2-mainframe-revenue-falls-42","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"顧問段：2026 年 6 月季簽約（固定匯率）成長 6% 但營收僅成長 1%；Q2 2026 起 IBM 不再公布生成式 AI 累計業務量（最後為 FY2025 年報的逾 $12.5B），改稱生成式 AI 約占當季簽約 50%、占積壓訂單逾 30%。未找到定價或市占資料","source":"Trefis, Should You Worry That IBM Has Gone Quiet On Its AI Total?","url":"https://www.trefis.com/articles/614396/should-you-worry-that-ibm-has-gone-quiet-on-its-ai-total/2026-09-04","excerpt":null,"as_of":"2026-09-04","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"IBM Q3 2026 8-K 新聞稿分部營收","source":"SEC 8-K ex99.1","url":"https://www.sec.gov/Archives/edgar/data/0000051143/000005114326000093/ibm-20261021xex991.htm","excerpt":"–Software revenue up 8 percent, up 9 percent at constant currency –Consulting revenue flat, up 2 percent at constant currency –Infrastructure revenue up 4 percent, up 5 percent at constant currency","as_of":"2026-10-21","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"IBM 10-K FY2025 風險因素：若未能及時因應顛覆性技術與新商業模式，客戶對其產品或服務的需求可能下降、成本可能上升","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231.htm","excerpt":"If the company does not adequately and timely anticipate and respond to changes in customer and market preferences, competitive actions, disruptive technologies, emerging business models and ecosystems, the client demand for our products or services may decline or IBM’s costs may increase.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"The Register 報導 IBM 2025 全年大型主機銷售增長，執行長主打 AI 上大型主機、以生成式 AI 補 COBOL 人才缺口","source":"The Register, IBM says AI is insane in the mainframe as z17 sales surge","url":"https://www.theregister.com/2026/01/29/ibm_q4_2025/","excerpt":"IBM's leader has trumpeted an AI-on-the-mainframe future as generative AI fills in the COBOL gap left by earlier generations of techies.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"報導稱 Anthropic 宣布 Claude Code 可用於含 COBOL 的程式現代化後，IBM 股價單日重挫（約 13%，單一來源）","source":"BusinessDay, Anthropic AI tool sparks plunge in IBM stock","url":"https://businessday.ng/technology/article/anthropic-ai-tool-sparks-plunge-in-ibm-stock-signalling-potential-turning-point-in-tech/","excerpt":"The sell-off was triggered by Anthropic’s unveiling of Claude Code, an AI system capable of automating the analysis and modernisation of COBOL, a decades-old programming language that still underpins critical systems in banking, government, and other enterprise environments.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"IBM i 授權由永久授權轉為訂閱制（Power10 P05/P10 自 2024-05 起買硬體須訂閱授權，延伸至 Power11）","source":"2-data.com IBM i's Perpetual Licence Era Is Over","url":"https://2-data.com/knowledge-hub/ibm-is-perpetual-licence-era-is-over/","excerpt":"of subscription-based licensing became mandatory starting in May 2024, with that requirement now extending naturally into the current IBM Power11 generation. Why This Matters More on Power11 Than It Did on Power10 The subscription requirement was easier to overlook when it applied narrowly to specific Power10 tier machines, since many organisations simply continued running existing perpetually","as_of":"2026-09-21","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Think 2026 主題演講：IBM 合作夥伴分 Sell／Build／Service 三種角色；分析師認為以成交付費的夥伴方案與夥伴經濟錯位","source":"Techaisle IBM partner ecosystem curation doctrine Think 2026","url":"https://techaisle.com/blog/698-ibm-partner-ecosystem-curation-doctrine-kareem-yusuf-think-2026","excerpt":"Yusuf's keynote built the partner story on three personas: the Sell Partner, the Build Partner, and the Service Partner. The framing matters because it organizes the entire ecosystem investment portfolio around what partners actually do, not what they resell.","as_of":"2026-05-25","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Ingram Micro 不再擔任 IBM 澳紐經銷商，轉向以服務與軟體為主的新夥伴","source":"Channel Insider IBM shuffles ANZ distribution to support MSP play","url":"https://www.channelinsider.com/news-and-trends/ibm-shuffles-anz-distribution-to-support-msp-play","excerpt":"it has brought on NEXTGEN Group and Arrow Electronics to act as its distributors in Australia. Meanwhile, Melbourne-based Meier Business Systems will handle the company’s hardware and technology life cycle services. The big change to the channel blend here is that Ingram Micro will no longer be a distributor for IBM in Australia.","as_of":"2023-09-22","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"7月中下旬多家券商下調IBM目標價：Citigroup 255（原375）、JPMorgan 250（原291）、Stifel 235（原290）、Barclays 288（原350）、Jefferies 260（原320）；MarketScreener顯示平均目標價約244、25位分析師覆蓋，多數維持評級。","source":"MarketScreener, Evolution of the Average Target: IBM","url":"https://www.marketscreener.com/quote/stock/IBM-69000/consensus/","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"HSBC於7月16日給IBM目標價175、評級reduce；MarketBeat七月底平均目標價265.40、共識Moderate Buy（各聚合站數字不一致）。","source":"MarketBeat, FY2026 earnings estimate for IBM issued by Erste Group Bank","url":"https://www.marketbeat.com/instant-alerts/fy2026-earnings-estimate-for-ibm-issued-by-erste-group-bank-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 2026營收17.2B（年增1%）、調整後EPS 2.93，低於共識（Benzinga：EPS預期3.02、營收預期17.86B）；全年指引原為固定匯率營收成長5%以上、FCF較去年增加約10億美元，7月14日初步數字顯示該指引仍有效，7月22日8-K標題為更新全年預期但摘要未含數字。","source":"MarketBeat, IBM updates Q2 2026 earnings guidance (2026-07-14); Benzinga IBM earnings forecasts; SEC 8-K 2026-07-22","url":"https://www.marketbeat.com/instant-alerts/international-business-machines-nyseibm-updates-q2-2026-earnings-guidance-2026-07-14/","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Erste Group於7月27日將IBM FY2026 EPS估計由12.39微降至12.36（共識12.34），FY2027為13.14；Bank of America先前因Confluent併購稀釋與諮詢趨勢轉弱，將2026 EPS由12.20降至11.98。","source":"MarketBeat, FY2026 earnings estimate for IBM issued by Erste Group Bank","url":"https://www.marketbeat.com/instant-alerts/fy2026-earnings-estimate-for-ibm-issued-by-erste-group-bank-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"IBM 2026-07-22 8-K第二季新聞稿含更新後全年預期","source":"SEC 8-K IBM 2026-07-22 Ex.99.1","url":"https://www.sec.gov/Archives/edgar/data/0000051143/000005114326000077/ibm-20260722xex991.htm","excerpt":"We now expect constant currency revenue growth in the range of four-to-five percent, and we continue to expect free cash flow to increase by about $1 billion year-over-year for the full year.” Full-Year 2026 Expectations","as_of":"2026-07-22","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"IBM 宣布收購資料串流公司 Confluent（聚合來源列約 110 億美元全現金，2026-01-15）；德國聯邦卡特爾局 2026-02-09 核准該併購。","source":"Concurrences｜German competition authority clears IBM/Confluent (2026-02)","url":"https://www.concurrences.com/en/bulletin/news-issues/february-2026/the-german-competition-authority-clears-a-merger-in-the-it-sector-ibm-confluent","excerpt":null,"as_of":"2026-02-09","retrieved_at":"20261024","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"IBM 簽約收購 HRL Laboratories（Boeing 與 GM 合資研究機構），以強化超導量子位元計畫，財務條件未揭露（搜尋結果未載日期）。","source":"RTTNews｜IBM to buy HRL Laboratories to expand quantum computing","url":"https://www.rttnews.com/3670011/ibm-to-buy-hrl-laboratories-to-expand-quantum-computing.aspx?type=maa","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"律所 Bleichmar Fonti & Auld 因 2026-07-14 Q2 財報後股價下跌，調查 IBM 是否就大型交易簽約速度誤導投資人；屬調查，未見已提起集體訴訟。","source":"Bleichmar Fonti & Auld｜IBM class action lawsuit investigation page","url":"https://www.bfalaw.com/cases/ibm-class-action-lawsuit","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 13 份 8-K 中僅 1 份含重大項目（2026-06-23 Item 1.01，為信貸協議展期），無 4.02 等重編項目。","source":"SEC EDGAR｜8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000051143&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"Confluent 併購案併購完成狀態未於搜尋結果確認","source":"IBM Newsroom mergers and acquisitions","url":"https://newsroom.ibm.com/mergers-and-acquisitions?l=100","excerpt":"IBM Completes Acquisition of HRL Laboratories to Accelerate the Future of Quantum IBM to Acquire HRL Laboratories to Power the Future of Quantum IBM Completes Acquisition of Confluent, Making Real Time Data the Engine of Enterprise AI and Agents","as_of":"2026-10-01","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"IBM 宣布收購 Confluent（聚合來源列約 110 億美元全現金，2026-01-15）；德國聯邦卡特爾局 2026-02-09 核准。","source":"Concurrences｜German competition authority clears IBM/Confluent","url":"https://www.concurrences.com/en/bulletin/news-issues/february-2026/the-german-competition-authority-clears-a-merger-in-the-it-sector-ibm-confluent","excerpt":null,"as_of":"2026-02-09","retrieved_at":"20261024","affects":["valuation","thesis.H"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"IBM 簽約收購 HRL Laboratories，強化超導量子位元計畫，條件未揭露。","source":"RTTNews｜IBM to buy HRL Laboratories","url":"https://www.rttnews.com/3670011/ibm-to-buy-hrl-laboratories-to-expand-quantum-computing.aspx?type=maa","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Bleichmar Fonti & Auld 於 2026-07-14 Q2 財報後股價下跌，調查 IBM 是否誤導投資人大型交易成交速度；僅為調查。另有 2023 年起訴於 SDNY 的主機營收重分類集體訴訟，搜尋結果未載結案狀態。","source":"Bleichmar Fonti & Auld｜IBM class action lawsuit page","url":"https://www.bfalaw.com/cases/ibm-class-action-lawsuit","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 13 份 8-K 中僅 1 份含重大項目（Item 1.01 信貸協議展期），無 4.02 重編項目；搜尋亦未見 2026 年 SEC 調查。","source":"SEC EDGAR｜8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000051143&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"IBM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":58.1,"operating_margin_pct":18.39,"fcf_margin_pct":19.02,"rd_intensity_pct":12.67},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBM","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"ACN","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":32.01,"operating_margin_pct":15.75,"fcf_margin_pct":17.21,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACN","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ORCL","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":63.96,"operating_margin_pct":34.23,"fcf_margin_pct":-40.01,"rd_intensity_pct":14.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ORCL","as_of":"TTM ending 2026-08-31（4季加總）"}},{"name":"MSFT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.94,"operating_margin_pct":46.78,"fcf_margin_pct":20.19,"rd_intensity_pct":10.72},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"HPE","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.73,"operating_margin_pct":7.84,"fcf_margin_pct":9.93,"rd_intensity_pct":8.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HPE","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"IBM"},"financial_history":{"ticker":"IBM","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":60530000000.0,"revenue_yoy_pct":null,"gross_margin_pct":54.0,"operating_margin_pct":13.5,"net_income":1640000000.0,"diluted_eps":1.8,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":61860000000.0,"revenue_yoy_pct":2.2,"gross_margin_pct":55.45,"operating_margin_pct":15.17,"net_income":7502000000.0,"diluted_eps":8.14,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":62753000000.0,"revenue_yoy_pct":1.44,"gross_margin_pct":56.65,"operating_margin_pct":16.05,"net_income":6023000000.0,"diluted_eps":6.43,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":67536000000.0,"revenue_yoy_pct":7.62,"gross_margin_pct":58.19,"operating_margin_pct":18.5,"net_income":10593000000.0,"diluted_eps":11.17,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/IBM/IBM_Q3_2026_Earnings_Call_20261021.md）

# Q3 2026 Earnings Call
**International Business Machines Corporation** | Earnings Calls | 2026-10-21

**Operator** (Operator):
Welcome, and thank you for standing by. [Operator Instructions] Today's conference is being recorded. If you have any objections, you may disconnect at this time. 
Now I will turn the meeting over to Olympia McNerney, IBM's Global Head of Investor Relations. Olympia, you may begin.

**Olympia McNerney** (Executives):
Thank you. I'd like to welcome you to IBM's Third Quarter 2026 Earnings Presentation. I'm Olympia McNerney, and I'm here today with Arvind Krishna, IBM's Chairman, President and Chief Executive Officer; and Jim Kavanaugh, IBM's Senior Vice President and Chief Financial Officer. 
We'll post today's prepared remarks and a replay of today's webcast on the IBM investor website within a couple of hours. The earnings presentation is already available. To provide additional information to our investors, our presentation includes certain non-GAAP measures. For example, all of our references to revenue and signings growth are at constant currency. We provided reconciliation charts for these and other non-GAAP financial measures at the end of the presentation, which is posted to our investor website.
Finally, some comments made in this presentation may be considered forward-looking under the Private Securities Litigation Reform Act of 1995. These statements involve factors that could cause our actual results to differ materially. Additional information about these factors is included in the company's SEC filings.
So with that, I'll turn the call over to Arvind.

**Arvind Krishna** (Executives):
Thank you for joining us today. Revenue growth in the third quarter accelerated to 6%, above the base case we laid out in July. This performance reflects acceleration across our segments, led by Software growth of 9%, Infrastructure growth of 5% and modest improvement in Consulting. We entered the quarter focused on disciplined execution, which also drove strong performance in profitability and free cash flow. These results demonstrate the strength of our portfolio, the continued value clients place in mission-critical platforms and our confidence in both our strategy and the outlook for the balance of the year.
Technology innovation in both Hybrid Infrastructure and Super Intelligence is leading to better business performance. This quarter's results reinforce the strategic choices we have made over the last several years to advance IBM as a software-led hybrid cloud and AI platform company. 
In Software, Red Hat again grew 11% with bookings growth accelerating back to the high teens. OpenShift ARR growth accelerated to over 30% and as organizations scale Super Intelligence applications and agents into production, reinforcing our conviction that we remain in the early stages of a long-term application modernization cycle.
Transaction Processing grew 10%, underscoring the strategic importance of the mainframe and validating our view that the softness we saw in the second quarter reflected timing rather than underlying demand. Data grew 20%, supported by continued strength in Confluent. Infrastructure was up 5%, driven by continued momentum in Distributed Infrastructure, growing 32% this quarter. 
AI continues to increase demand for storage, and we are gaining share through differentiated offerings across Flash, Fusion, tape and IBM Z storage, including AI-enabled capabilities that help clients scale and manage data for AI. Consulting revenue grew 2% as clients modernize to deploy AI securely and at scale. The durability of our portfolio remains a defining feature of IBM today.
z17 continued the strongest innovation cycle in the platform's history, generating more than $1 billion of incremental revenue over 6 quarters compared with prior programs. This reflects the security, reliability, scalability and compelling economics of the platform. As infrastructure costs rise, IBM Z delivers a 2 to 15x total cost of ownership advantage versus off-platform alternatives, positioning us to capture additional value as AI workloads grow.
Building on that advantage, we introduced new single frame and rack mount on IBM Z systems in July that help clients address data center space, cost and deployment constraints without compromising performance or security. Client response has been strong, contributing to the highest mid-range revenue launch in IBM Z this quarter in nearly 2 decades.
Last quarter, we told you Lightwell represents a multibillion-dollar opportunity for IBM and Red Hat to help clients secure their open source software. Since then, some of the world's largest enterprises have signed up as clients, and we have built a pipeline approaching $700 million in a short period of time. We have released more than 40,000 remediated packages to the Lightwell network, demonstrating the rapid scale-up of our remediation capabilities.
Now turning to our AI strategy. Enterprise AI is entering its next phase. Deploying more models or building more agents will not be enough. The advantage will belong to a company that can operate AI securely, efficiently and sustainably across the enterprise. Organizations are recognizing that AI is only as effective as the system around it. The data that provides context, the workflows that orchestrate action, the infrastructure that secures and optimizes operations and the hybrid cloud foundation that provides flexibility without lock-in.
IBM has assembled these capabilities across 4 platforms. Confluent provides continuous business context through a real-time data foundation. watsonx, including Bob and Orchestrate, support AI-driven software development and agent orchestration. HashiCorp and Apptio automate identity, access and policy while optimizing cost and performance. Red Hat provides the open hybrid architecture, spanning public cloud, on-premises, sovereign environments and the edge. Together, these platforms help clients move from isolated deployments to AI operating at enterprise scale.
Data sits at the center of the AI operating model. 72% of organizations report insufficient real-time data infrastructure, which holds back AI at scale. Agents need the current state of the business. That is why we are excited about Streamhouse, a capability from Confluent that continuously captures, transforms and queries real-time data. It complements warehouses and lakehouses. 
A Streamhouse makes real-time, governed data continuously available to applications, analytics and AI, unifying operational and analytical data into a single architecture. We believe Confluent is uniquely positioned with a complete open and hybrid approach that helps clients avoid lock-in while deploying wherever the data resides. As AI scales, clients ask 2 questions, what will it cost and who controls it? We are innovating on both.
Apptio now connects AI spend to business results, providing visibility into AI usage, token consumption and the cost of running it across the enterprise. llm-d, an open source project developed with Red Hat and Google, reuses previously processed context, helping clients run large AI models at 5 to 10x lower cost by making more efficient use of existing GPU infrastructure. And Bob now runs on-prem. So clients in regulated and sovereign environments can keep code and models on their own infrastructure. 
Governance matters as much as intelligence. As agents multiply, enterprises need to know who each agent is, what authority it has and what it can access. HashiCorp Vault allows clients to register, authorize, audit and revoke agents and secure their credentials. IBM Agent Identity and HashiCorp Vault are partnering with NVIDIA Open Agent Safety Platform to strengthen agent security. We believe agent identity will become as foundational to enterprise AI as identity has become to the Internet.
Finally, Quantum remains a strategic area of differentiation for IBM and a significant long-term opportunity. In July, 3 independent demonstrations of quantum advantage were achieved on IBM hardware with the University of Chicago, Algorithmiq and Qedma providing further evidence that quantum computing is moving from scientific promise towards practical value.
Our Nighthawk r2 processor has achieved important road map milestones across speed, scale and quality, delivering 7,500 gates, executing 100,000 circuits per second and enabling performance improvements of up to 19x over prior generation systems. That performance changes both time-to-solution and the economics of quantum computation. Workloads costing approximately $100 to run on IBM could cost up to $10 million on slower competitive modalities. 
Recently, IBM was selected for Stage C, the third phase of the Quantum Benchmarking initiative led by DARPA, the United States Defense Advanced Research Projects Agency, another validation of the strength of IBM's path to building a fault-tolerant quantum computer. Commercial momentum is also growing. This year, IBM Quantum has signed 16 enterprise engagements across industries, including automotive, aerospace, telecommunications, financial services and manufacturing. This includes AT&T and General Motors, amongst many others, who are now all part of the IBM Quantum Network, the world's largest network of quantum innovators. 
We are also advancing the technology and infrastructure required for industrial scale fault-tolerant computing, including the successful connection of our first modular cryogenic systems and continued progress on our 300,000 square foot  Poughkeepsie manufacturing facility. This, along with the closing of the $1 billion award from the Department of Commerce in Anderon for manufacturing quantum wafers gives us confidence that after the Starling demonstration, we are ready to scale. We look forward to talking more about our progress at our Quantum Day on December 10. 
In closing, our third quarter performance reflects the strength of our portfolio and the progress we are making against our strategic priorities of delivering both sustainable revenue growth and higher profitability. Our results reinforce our confidence in delivering revenue growth for 2026 in a range of 4% to 5% and enable us to raise our year-over-year free cash flow growth expectation to more than $1 billion. 
With that, let me hand it over to Jim.

**James Kavanaugh** (Executives):
Thanks, Arvind. In the third quarter, we delivered solid results with 6% revenue growth, 70 basis points of operating pretax margin expansion and 11% diluted operating earnings per share growth. And through the first 9 months, we generated about $8 billion of free cash flow, up 8% year-over-year. These results reflect strength across our portfolio and solid execution against our priorities.
Let me walk through the performance in each of our segments. Software revenue growth accelerated 4 points sequentially to 9% this quarter, including over 4 points of organic growth. This performance was driven by our high-value annual recurring revenue base, which grew 8% to $24.9 billion. Three of our 4 software subsegments grew revenue double digits, led by the combination of strong new business performance and pipeline closure rates, including the successful closure of around 2/3 of the large deals that slipped from the second quarter. Our results represent the high end of the range we outlined in July, reinforcing our confidence in the strength of our portfolio.
Turning to our subsegments. Red Hat revenue grew 11% again this quarter, fueled by bookings accelerating back to the high teens. Lightwell was recently made generally available, and we have strong early demand with a pipeline that is already approaching $700 million. OpenShift is now $2.4 billion ARR business with growth accelerating to more than 30%. Our virtualization offering continues to scale with nearly $800 million in contracts signed since early 2024 and about $750 million in pipeline.
Data grew 20%, driven by another strong performance from Confluent with bookings growth of about 20%. Transaction Processing grew 10% in the quarter, driven by demand for this mission-critical software and strong execution against our pipeline. HashiCorp continues to perform well, growing bookings across all geographies and accelerating revenue growth sequentially. However, automation was impacted by a tougher compare.
Turning to Infrastructure. Revenue growth accelerated to 5%, driven by 32% growth in Distributed Infrastructure. Storage delivered record revenue growth and continue to gain market share with broad-based demand across Flash, Fusion, tape and IBM Z storage. Strength across Storage and Power reflects the growing importance of Differentiated Infrastructure as clients modernize their environments, address data growth and support AI at scale. 
With a sizable backlog in Distributed Infrastructure exiting the quarter, we are well positioned for continued momentum in the fourth quarter. z17 continues to perform exceptionally well, wrapping on the strongest start to a Z program last year. Program-to-date performance remains well ahead of the prior generation, up over $1 billion. And this quarter, we had the strongest mid-range launch in IBM Z in nearly 2 decades.
Beyond the strength of the program, IBM mainframe clients representing approximately 85% of installed MIPS capacity are maintaining or growing their capacity, and aggregated installed capacity has tripled over the last few programs. Consulting revenue grew 2% this quarter, reflecting continued client demand for AI-enabled transformation. Growth was led by strategy and technology, up 4%, with strength in application modernization and data and AI transformation, while cybersecurity delivered nearly double-digit growth in Intelligent Operations. AI is increasingly embedded in broader transformations our clients are undertaking, representing about 30% of our Consulting revenue in the quarter and 35% of our backlog.
We are also expanding the ecosystem of capabilities we bring to clients, including through our new strategic partnerships with OpenAI and our expanded relationship with Google Cloud as we help clients scale enterprise AI. Clients remain at different stages of adoption, but we continue to see them modernizing applications, strengthening their data foundations and reengineering workflows as they move forward toward embedding AI into core business processes at scale. Our integrated model, combining deep domain expertise, technology and reusable assets positions us to help clients capture business value from AI while accelerating time to value. 
Let me now discuss profitability. Adjusted EBITDA and operating pretax margins expanded by 60 and 70 basis points, respectively. As I mentioned last quarter, we accelerated our productivity initiatives to help enhance our operating profit margin and free cash flow commitments while continuing to invest for growth. We made significant progress this quarter, driving efficiencies across G&A and sales, reinforcing the power of our productivity flywheel. Segment profit margins expanded by 210 basis points in Software and 120 basis points in Infrastructure, driven by ongoing productivity actions. Consulting segment profit margin declined modestly as we reinvested productivity gains into digital assets, accelerating our transition towards a Services-as-Software model to capture the growing AI opportunity.
Through the first 9 months of the year, we generated about $8 billion of free cash flow, up about $600 million year-over-year, driven by about $1 billion increase in adjusted EBITDA, offset by higher CapEx, cash taxes and net interest expense. Our free cash flow margin for the first 9 months of the year is the highest in reported history, highlighting our strong execution against productivity initiatives and laser focus on operational discipline. 
We exited the third quarter with a strong liquidity position and a solid investment-grade balance sheet with cash of $11.1 billion. We returned $4.8 billion to shareholders in the form of dividends through the first 9 months of the year. Our debt balance ending the quarter was $63.8 billion, including debt of $12.7 billion for our financing business with a receivables portfolio that is almost 80% investment grade.
Now let me talk about what we are seeing going forward. The strength and diversity of our portfolio, disciplined capital allocation and sustained productivity execution underpin our revenue growth, earnings expansion and free cash flow performance. Through the first 9 months of the year, we delivered over 4% revenue growth, 9% operating pretax income growth, 10% operating earnings per share growth and 8% free cash flow growth. We continue to expect revenue growth for 2026 in the range of 4% to 5% and are raising our expectation for free cash flow growth to more than $1 billion. 90 days ago, we provided a full year revenue growth range with profit and free cash flow expectations anchored to a 4% base case. We continue to take the same approach for the full year, anchoring profit, free cash flow and segment expectations to that base case.
Given our strong third quarter Software performance, our confidence in the full year outlook has increased. We now expect full year Software growth of approximately 7% to 8%, with about 7% as the revised base case. For the full year, we expect double-digit growth in Hybrid Cloud, mid-teens growth in Data and low single-digit growth in Automation. For Transaction Processing, we are raising our expectations for the full year with growth expected to be flat. Infrastructure growth accelerated in the third quarter with significantly stronger program-to-program performance of z17, underscoring the durability of the platform and the value it delivers to clients. Combined with continued strength in Distributed Infrastructure, we continue to expect low single-digit Infrastructure revenue growth for the full year.
In Consulting, backlog quality and momentum in generative AI continue to support a modest acceleration to low to mid-single-digit revenue growth for the year. In the third quarter, our operational discipline and accelerated productivity initiatives allowed us to enhance margins and deliver free cash flow commitments while continuing to invest for growth. These actions include deploying AI and automation at scale across our company, reducing third-party spend, improving sales and marketing efficiency, using AI to drive more efficient software development, optimizing our supply chain and enhancing services delivery. 
We continue to expect 100 basis points of operating pretax margin expansion for the full year, reflecting the flow-through from the third quarter earnings beat and continued operational discipline. And our operating tax rate expectation for the year remains in the mid-teens. For the full year, we are raising our expectation for free cash flow growth to more than $1 billion. The primary driver of this growth will be adjusted EBITDA, offset by higher CapEx, higher cash tax and net interest expense. Our free cash flow continues to be driven by growth in adjusted EBITDA and demonstrates consistent free cash flow realization of about 130% over the last few years.
Let me close by saying that our third quarter performance reinforces our confidence in our portfolio, the resilience of our business model and our outlook for the year. At the same time, we continue to invest in the technologies that will shape IBM's next chapter of growth. As Arvind mentioned, Quantum continues to advance across technology, ecosystem adoption and scale up. While still early, the progress we're seeing from enterprise engagements to government validation reinforces our confidence in both our road map and the long-term opportunity ahead. We look forward to discussing in more detail at our Quantum Day in December. 
Arvind and I are now happy to take questions. Olympia, let's get started.

**Olympia McNerney** (Executives):
Thank you, Jim. Before we begin Q&A, I'd like to mention a couple of items. First, supplemental information is provided at the end of the presentation. And then second, as always, I'd ask you to refrain from multipart questions. Operator, let's please open it up for questions.

**Operator** (Operator):
[Operator Instructions] And our first question comes from Amit Daryanani with Evercore.

**Amit Daryanani** (Analysts):
Great to see some nice software acceleration here. Arvind, I think last quarter, we discussed a lot about customers prioritizing Infrastructure over Software purchases. This quarter, it seems like Transaction Processing is at double-digit growth, while Infrastructure has remained very strong for you folks. Can you just talk about what changed in customer spending priorities? Are you primarily just recovering deferred transactions at this point? Or are you actually starting to see Infrastructure investments starting to create more incremental demand for IBM Software? And with Red Hat bookings actually growing at high teens, is that an early indication that Software can actually accelerate as you go into '27?

**Arvind Krishna** (Executives):
So Amit, thanks for that question, and also thank you for observing the numbers. Let me comment on the overall customer priorities, the tie towards Infrastructure and Red Hat, and I'm going to ask Jim to cover the Transaction Processing piece a little bit. So first, as we look at customer spending priorities, customer spending priorities in trying to leverage AI remain strong. But as you begin to leverage it, how does the average customer get value? They have to rewrite an application. They have to modernize an existing application. 
And you then ask the question, where do those run? That tends to be a tailwind for Red Hat OpenShift. And I think we are at the very beginning of this cycle. So I expect that to carry on for a long time. Then the moment they get to saying, "Okay, I'll write the application on Red Hat OpenShift." You then get to how do I unlock the data from all of the enterprise data that I need to power that AI application. Remember, 90% of enterprise data is not on the cloud. It's very much inside the enterprise. So Confluent tends to be a tailwind. I expect these to carry on for a long time. 
The Automation portfolio will get a benefit when these applications all get to scale and people start worrying about managing hundreds and thousands of them. At that point, Automation will also get a tailwind. On the point you're making on Red Hat, look, we are very comfortable saying that based on what we can see, we are comfortable about double-digit growth in the fourth quarter of this year. Right now, we don't really want to comment on '27 growth. But generally speaking, I can say when we get these kinds of booking growth, it translates into good revenue growth going forward. 
Jim, maybe a comment on TP.

**James Kavanaugh** (Executives):
Yes. Just to build on your points, Arvind. And Amit, thank you very much for the comment and the question. We're very pleased overall with our Software performance. Team executed extremely well, 4 points sequentially to 9% printed here in the third quarter, and it was all organically driven. Pervasively, across our portfolio, 3 of our 4 subcategories accelerated and grew double digits overall. And that was a reflection of both. 
We talked a lot last quarter about the 80% high-value recurring revenue growing nicely at high single digit, but we saw a very nice rebound in our transactional business, that remaining 20% that grew actually double digits, led by our ELAs that were up north of 20% with an NRR of north of 130% overall. That's a function of, yes, disciplined execution on slipped deals, but also a function of net new business contribution in the quarter. And I would tell you before all of you ask, about 1/4 of it is the slipped deals with regards to overall software acceleration and about 3/4 of it is net new business that we are capturing overall, so to build on Arvind's point.
Now on TP. TP, we're obviously pleased, double-digit growth. I think this instantiates the demand for our mission-critical strategic mainframe software. A lot of discussions a quarter ago about demand destruction versus timing. I think this puts this to rest right now because when you take a look at it, we've been talking all year long about the reinforcement of confidence we have in our mainframe platform and how we monetize the strong z17 performance, right? 
That model is -- the monetization model is the more capacity you put in the marketplace, the higher monetization opportunity, the higher price opportunity, a higher value creation opportunity. z17 today, installed MIPS are up high teens, 6 quarters in. Shipped MIPS are up over 100%. That is the future monetization opportunity that we feel extremely confident about as to the acceleration potential of TP in the future. So I appreciate the question and a great place to start.

**Operator** (Operator):
Your next question comes from Wamsi Mohan with Bank of America.

**Wamsi Mohan** (Analysts):
Thanks for the color you just shared on TP, but maybe if we could just double-click on that. I mean last quarter, you were thinking that TP might be down low to mid-single digits for the second half, and you called it a '27 growth vector. It grew 10% instead. So maybe, Jim, as part of those like 1/4 of Software upside really came from those pushed deals. Could you share some color more specifically with respect to TP if that was similar or higher in relation to the deals that closed from those pushed deals? And how many of those low 10s of slipped deals have now closed? Because you've not really changed your 4% to 5% for the year, but your commentary and your numbers would suggest that you're gravitating much more towards the higher end of that. If you could share any more incremental color. And on through-cycle TP performance, is that still something that we should think of as mid-single digit? That would be great.

**Arvind Krishna** (Executives):
Wamsi, I know you addressed the question to Jim, but I'm going to start and then ask Jim to color -- give a lot of color on both the slipped deals, the TP performance and the cycle-to-cycle compare, if I sort of paraphrase your question short.
So let's just talk about TP. The question that everybody had last quarter was, does this imply that overall demand for mainframe has gone down? And we were very confident that this was a timing question, not a destruction question. And so at the macro level, as people deploy all of that hardware, as they deploy that MIPS, as the volumes of the underlying transactions increase, they need this mainframe software to support that mission-critical business. That's why we were confident it would come back.
Now to your point of us saying low to mid-single-digit decline, we want to be cautious and we want to be prudent. We want to see the absolute baseline, and we don't want to call above it. I think what really happened was we got not only the deferral from 2Q, we got a normal 3Q buying cycle on mainframe. So kind of got it both together. I would be candid and tell you, I don't expect double-digit performance in TP to keep going, but I would expect to see now more normalized performance, especially going into next year and perhaps a moderation from 3Q going into the fourth quarter. But it speaks to the underlying demand for the mainframe around resilience, around the economics, around the architecture that supports 8, 9s of availability.
Let me point it out, 8, 9s of availability, but the transactions in the mainframe tend to be almost the opposite of what happens in AI. Here, you need things that are completely deterministic, that are repeatable and that you can look at it with a financial cold eye that they're meeting all the requirements of those kinds of transactions. And there's plenty of other things that will happen on Distributed Infrastructure. I think in terms of the numerics, I'm going to hand it to Jim to cover with you.

**James Kavanaugh** (Executives):
Yes. Wamsi, thanks for the question overall. Let me just kind of reiterate a little bit about where I ended the last question to Amit. When you look at the health of our Software business that accelerated 4 points quarter-to-quarter, it was a function of both the high-value recurring revenue. And again, the underpinnings of that is the Red Hat strength and acceleration. It's excellent start to our Confluent acquisition. It's record performances in Hashi overall, and that part of the business is doing well. The transactional is where the big difference changed. 
Last quarter, it impacted our software growth by 4 to 5 points when we were down double-digit transactional. This quarter, we were up double-digit transactional. And I'll remind you, that's 20% of our software book. Annual book is about $32 billion, give or take. And that today offers about 2/3 to 3/4 of that is ELAs. ELAs are strong incumbency positions that we've earned trust of our clients for decades around mainframe running their core architectures. On top of that, we build a moat and we build a software distributed business model that captures that very attractive economic multiplier of $3 to $5 of software for every dollar we land on mainframe. 
Now within that, TP is disproportionate. But with that moat, we give clients flexibility on where they want to choose that ELA spend as to where it goes between data, between automation and between TP. Red Hat is not part of our ELAs overall. And what we saw here both is a contribution in the quarter on slipped deals. Let's put this in perspective. We printed a number, what, $7.6 billion (sic) [ $7.8 billion ] of software, the slipped deals were 10s of slipped deals. So let's kind of put them in a ballpark from 2Q of, what, $400 million which is what we missed software by. We closed 2/3 of those. That's $250-plus million. That is the 25% of the contribution of the growth that we've had of 4 points. 
By the way, that was disproportionate to TP. That's why you see TP well up at double digits overall. We didn't get a lot out of that in Data and in Automation and some of that should be fourth quarter. Now fourth quarter, we gave a guide, I think, to use Arvind's word, anchored in our philosophy 90 days ago, prudent, cautious. We're anchoring this thing at the low end, approximately 7%. By the way, put that in perspective, I think the current Street estimates for the year are about $32 billion of revenue. We feel comfortable with that $32 billion of revenue. So that's kind of where we're at. I think I covered most of your questions.

**Operator** (Operator):
Your next question comes from Ben Reitzes with Melius Research.

**Benjamin Reitzes** (Analysts):
I wanted to ask about your long term -- the short-term puts and takes we get. But at your latest Analyst Day, you laid out that you would approach double digits in Software as a long-term target. Based on what you're seeing, do you still feel confident in that? And how is M&A going to play a role in terms of achieving that? Because in order to hit it, I guess you got to accelerate a point or 2 after this year. So a lot of folks are wondering where M&A plays in that?

**James Kavanaugh** (Executives):
Thanks, Ben. I appreciate the question overall. Obviously, it's not going to surprise you. We'll spend a lot more time on this question here in January. We got the team extremely focused already. We're 21 days into arguably the most important quarter we have in a fourth quarter overall. But let me take a step back first around IBM. And then as Arvind and I have been talking here as we're heading into our planning cycle and laying out all of our investment and capital structure strategies for '27. 
Talk a little bit about IBM, then hit your question on Software. We've got a lot of confidence in our strategy and our portfolio is well positioned to deliver sustainable, durable growth on our model. We feel extremely confident in that. Why? We got an attractive TAM, market backdrop of technology, the diversity of our portfolio, leveraging our hybrid cloud and AI platform-centric model, our continued portfolio optimization to shift to higher growth end markets, new innovation we continue to bring to market around Lightwell, around GenAI, and around to your question, M&A growth synergies. All of that will play out. 
But from a segment perspective, since you asked about Software, I'll give you some early indicators. One, we got a high-value recurring revenue stream that's been accelerating all year long, $25 billion ARR book of business, high single-digit growth. We execute to what our guide is here, we should be approaching double digits here in the fourth quarter on that 80% high value. That's one critical indicator. Two, new innovation we're bringing to market. We're extremely excited to, Arvind's point, around Red Hat, the acceleration to high teens growth. We've got $700 million worth of pipeline on Lightwell alone in front of us right now with a $1 trillion TAM opportunity around open source vulnerabilities. 
We got virtualization, a tremendous opportunity. We got hybrid cloud containerization opportunity. So we feel pretty good about the markets we're in, the investment and the portfolio that we had built up overall. Three, we got -- 2027 is a year of growth synergies, right? '26 was about integrating and getting Confluent into our mode of operation and go-to-market and scale, '27 is around the growth synergies. And finally, to the TP question, we've got high-teens growth in installed MIPS out in the marketplace. Last 5 years, our MIPS are up 2x. Last 10 years, our installed MIPS are up 10x. That is the monetization vehicle at TP, and Arvind talked about it, I talked about it. We think that's a growth acceleration back to our model overall. We'll quantify that in January, but that gives you a little bit of perspective of our early thinking about '27 on Software and IBM.

**Operator** (Operator):
The next question comes from Raimo Lenschow with Barclays.

**Raimo Lenschow** (Analysts):
Perfect. Two quick ones, if I may. First, congrats on the Software performance. On Data, 20% growth. Obviously, some of that is Confluent. But like what are you seeing there on upsell and cross-sell on Confluent? You have it for a few quarters now, but that looks like it's starting to click for you. So can you kind of double-click on that one? And then one for Jim. Gross margins came up with investors. Can you just give us a comment there, what drove the performance there?

**Arvind Krishna** (Executives):
Raimo, thanks for the question, and thanks for noticing the Data growth. If I look at Confluent, I actually want to broaden it. There is Confluent, which is important for moving data in real time, allows data to remain in place, but still be available for AI. But coupled to that are what I call lakehouses, and we are very excited about the upcoming cross-sell opportunity with Streamhouse, which is also another way to store data that is sort of in-flight. So the Confluent piece unlocks your data, be it inside the enterprise, be it in an application, be it in a SaaS application, be it on a cloud, but still have it completely available for AI agents as well as for inferencing. Really important capability, and you saw that growth pull through. 
But lakehouses are also important as people are beginning to cleanse their data for leverage in AI, and we saw growth there also. And then we are excited about what is going to come with the capability we are about to announce in a couple of weeks around the Streamhouse, which is also then going to be directly a cross-sell and upsell on top of Confluent. So unlocking data for AI, making sure that you don't have to create multiple copies because that creates a lot of extra cost, but still have it available as quickly as you need it is the fundamental capability we believe is going to be unlocked in the enterprise, leveraging all of these capabilities, and that contributes to the overall growth there. Jim, I'll give it to you for the gross margins question.

**James Kavanaugh** (Executives):
Raimo, thank you very much for noticing the operating leverage engine that we've been driving across this company. You look at, what, the last 4 years were probably up, what, about 1,000 basis points of operating leverage across this company. By the way, that has delivered high-quality, sustainable cash generation. Over the last 4 years, our cash is up roughly $7 billion of growth and 700 basis points of free cash flow margin on that 1,000 basis points of operating leverage. But when you look underneath it, we continue to improve the structural competitiveness of this business model. We still believe we got a lot of headroom here. When you take a look at our profit, earnings up double digits, our operating margins are up 70 basis points. It's delivered by we are driving in the third quarter, 500 basis points of gross productivity in our model. 
We've always said in our model, about 1/3 is for margin protection. About 2/3 enables us to drive that productivity flywheel where we reinvest back into the business around R&D, innovation, go-to-market model ecosystem to drive that flywheel of growth and competitive advantage. 500 basis points is well above what our model is overall. How are we doing that? We're running our playbook. That playbook, we believe, has headroom. It's reimagining everything between Arvind and myself about how we execute and run this company. And that gets into leveraging data, a whole new way of workflow reimagination, embedding technology, digitization, AI into our company. 
We've been talking about in prepared remarks, how do you reimagine a whole new way for software development? How do we reimagine a whole new way on go-to-market models? How do we redesign the G&A structure, the way we run our company? And I think there's a lot of headroom there. A few years in, we are now north of $5.5 billion of productivity out of this company. That is a great flywheel for investment flexibility and capability. So most important thing is it provides that free cash flow generation engine, and it applies that investment flexibility so we can continue to compete both organically and inorganically to invest.

**Operator** (Operator):
Your next question comes from Brent Thill with Jefferies.

**Brent Thill** (Analysts):
Arvind, I'm curious, in some of the deals maybe early in the year, there was a little bit of an AI bright light. I don't know what to do. I need to kind of wait and investigate and maybe the investigation period went on and they realized maybe some of the systems couldn't actually achieve what the claims were. And I'm curious if you're maybe seeing some element of this in some of the deals recouping where the claims were big, but perhaps the reality wasn't matching the claim and you're able to deliver on that. Is that something you've seen? Or is that not a scenario that you've experienced?

**Arvind Krishna** (Executives):
So Brent, let me make sure I parse the question correctly, but I'm going to sort of maybe answer it in my own words. I think what we are seeing is that at least larger enterprises are becoming a lot more cognizant and a lot more aware of what is the true ROI of all of their AI spend. They're also getting worried if some of the AI spending completely out of control with no real return. But the way I've always characterized it is, there is no question to us, and this is the advice I give every C-suite member that I meet that what we're trying to give people on AI, the productivity, the advantages of AI, the way it's going to change work is very real. So let me not make any confusion around that. 
That said, a lot of people are underplaying how much work it is to integrate AI into your workflows to fundamentally sit back and say, how do I redesign the workflow to take advantage of AI? It's not a little RPA tool that you bolt on and you get something. If you do not spend the time and energy to redesign your workflow, you're not going to get the full benefit. So if you're willing to do that, there's a huge benefit to be had. But that implies you've got to pick a few, you've got to learn how to scale them for full impact across the enterprise and don't do 100 little experiments where you then do not have enough investment to get them to scale. That is what I think we are seeing. 
So I think what we're seeing, Brent, is now enterprises as they're getting mature, as they're stopping the experimentation are saying, all right, who can help me get through this bigger piece of workflow design as well as integration into our existing systems because you're not likely going to throw out your ERP system. So how do you leverage it but still get the benefits of AI?
And then they're picking their partners in terms of which software do they -- are they willing to trust to do this? Which people have the knowledge to come do this with them as well as can you be really efficient about your token spend as opposed to leave it completely uncontrolled. So I agree, I think, with your thesis, but maybe a slight redirection in terms of why we're seeing that change. And yes, that is a tailwind for us. That is why I kind of repeat what I said at the beginning. That is why OpenShift, Confluent, mainframe with fraud are all seeing the benefits of that play go on as we are proceeding down this path.

**Operator** (Operator):
The next question comes from Fatima Boolani with Citi.

**Fatima Boolani** (Analysts):
I wanted to go back to the discussion around Transaction Processing simply because it was such a remarkable sequential recovery in that franchise. And Jim, I understand so much of that is piggybacking off of the ELA momentum that you regained in the quarter from the transactional side of the business. But I'm curious if you can help us unpack a little bit more on that strength I think you talked about high-teens growth in MIPS shipped. So wondering if you could unpack and break down for us the quantity and shipped MIPS growth in some of those slipped deals because those were existing customers. And to the extent you've been able to leverage a little bit of pricing power in this situation because I know that's not historically a lever that you've used. So I would love to get a little bit more second order detail on that Transaction Processing slope of recovery between quantity and quantity growth as well as pricing uplift.

**James Kavanaugh** (Executives):
Thanks, Fatima. I appreciate the question. Let's double-click back down on TP. First, let me just reiterate, what is the modernization model, right? TP is transaction processing that runs a mission-critical software on top of the most enduring platform, that being mainframe. By the way, as we've talked about many times before, mainframe runs 70% of the industry's transaction volumes in terms of value. 45 of the top 50 banks, 4 to 5 top airlines, 7 of the top 10 retailers around the world. I think 75%, 78% last number I've seen of the Fortune 100 run mainframe as a core architecture. So TP is the core mission-critical software that enables the most secure, reliable and scalable platform around. 
The way we monetize that value is the more capacity out there, the more opportunity to monetize value, the more opportunity to monetize price, the more opportunity to monetize value creation of TP. So when you take a look at our last 2, 3 cycles, we run 145 million MIPS around the world. Some of those are standard MIPS on the platform. Some of those are new Linux specialty MIPS, new cloud-native applications, which is why the mainframe has been a growth vehicle over the last 2 to 3 cycles overall. That 145 million MIPS, our z17, 6 quarters in, 125%, the highest recorded program to date above z16, which was the prior highest program to date. 
We're up, I think, 18% shipped MIPS through 6 quarters. We're up over 100% of shipped MIPS. Why do I differentiate between the 2? Read the first one as consumption, capacity and workload. We can monetize value immediately. The second is the opportunity. It's the TAM, right, and us driving workloads on that. So when you take a look at it, that's what's been driving the step function change in growing meaningful over time. It was only a handful of years that our TP portfolio was down, what, mid-single digit, high single-digit growth. 
We then stabilized that growth about 4 years ago. And then through z16, we saw an acceleration. But I'll reiterate that z16, when you look at the launch year, it was about flat the launch year, then it kind of went up to about mid-single digit year plus 1, and then it went up to high single digit year plus 2. Right now, in z17, we were about flat launch year. We got different dynamics playing out right now. So we're about prudently cautious calling flat for the year. But with 100% shipped MIPS and 18% installed MIPS, I would say that's a pretty good future monetization opportunity in 2027 going forward.

**Operator** (Operator):
Your next question comes from Brian Essex with JPMorgan.

**Brian Essex** (Analysts):
Congrats on the software acceleration from me as well. Arvind, I caught the prepared remarks or at least some of the news -- remarks that you had about clients deploying Super Intelligence in ways that transform entire operating models. And I appreciate that that's more than just increasing operating efficiency. But the question I have for you is as your customers assess those transformation efforts, how focused are they on sovereign AI? Is that becoming a more meaningful part of your conversations? And how are you seeing your customers focus on the protection of their data and IP as they assess how they deploy AI for their transformation efforts?

**Arvind Krishna** (Executives):
Brian, thank you first for the question, and thank you for noticing the precise words I did use in the prepared remarks. So to get to sovereign AI, sovereign AI is definitely becoming a much larger conversation. While we have talked about it for the last 1.5 years, I would not tell you that in '24, it had much traction. In '25, a few people began to pay some attention. And in '26 it is now beginning to pick up. And let me explain for everybody else exactly what we mean by that. 
If you're going to use a large public LLM, effectively, while they're certainly not stealing your data, though they're implicitly maybe learning what kind of questions are asked, there are traces left in the underlying logs and so on that are not the full, but that do give some indication of what all it is being used for as well as some elements of the data that is being used. So sovereign becomes, how do you make sure that none of that happens. So people are turning now to 2 kinds of answers. That is why I think there is such a big boom in AI infrastructure on-premise, and we can see some of the companies that benefit from that. By the way, so will we in our mainframe with our Spyre cards as time goes on. 
The other part of this is what is driving the boom behind open-weight models because there you have the permission and the IP rights to run them on either on-premise infrastructure or on private clouds where the enterprise controls what is happening to the underlying logs and data. That is definitely what is happening there, and we can see that and the boom behind some of the companies that are creating open-weight models is also increasing behind that. 
I'll reflect on a conversation I had with a large bank CEO. In this case, it was outside the U.S., but it's a very large and friendly country. And their view was, look, we'll do some early experiments on the larger frontier LLMs. But for what we're doing inside the bank, we need to run it in a way that is sovereign, meaning nobody can take any of the underlying data or underlying logs that are there. I was talking to somebody who does trading and they are on, we're not going to expose our underlying proprietary models or anything outside, but we need to run this in a sovereign way. I believe this is going to turn into a tailwind for many players in the industry, certainly the infrastructure and semiconductor players, but also for those of us who help enterprises deploy in a secure and in a private way.

**Operator** (Operator):
And our last question comes from Matt Swanson with RBC Capital Markets.

**Matthew Swanson** (Analysts):
Great. And maybe this is just kind of a natural follow-up to what Brent was asking. But you had mentioned earlier that what AI costs and who controls it have kind of been like the 2 primary questions that enterprises start off with you. Who controls it obviously fits right into that sovereign AI conversation. But could you just kind of talk a little bit about how people are addressing the trade-offs, if there are trade-offs between those 2 segments and how they're architecting their networks in order to maximize for both those things and just how kind of like symbiotic they can be?

**Arvind Krishna** (Executives):
So Matt, thanks for the question and also allowing me to give a bit more detail on this topic. If I go back to late '24, the difference between the most advanced model, which, let's acknowledge, is mostly a frontier LLM model and alternate models was a 2:1 or 3:1 gap, meaning if you ran some assessment, some benchmark and it was broad-based, not narrow, the top model might score a 70 and the open model might score a 20 or 30. You kind of react with, that's a lot of capability we're giving up. And we all know that performance in some sense, outcome for the enterprise is highly dependent upon that. That's too big a gap. Nobody is going to accept that. 
In late '25, we began to see that gap shrink where maybe the gap was not 70 to 20 or 30, it was 70 to 50. But when you looked at those curves and you looked at the improvement and you looked upon the sequential improvement, we were very comfortable that we'd get this to probably 100 for the top and 90 for the alternate model. So now the question becomes, how do you do that? Now the question that the enterprise struggles with is where are my kernel engineers? Where are the people who worry about the underlying network? Who can make sure that the model is clustered on GPUs that are close to each other in network proximity? Who can make sure that you're doing the right caching of results so you get an incredible response?
I'm telling you that, that gap is probably still there, except for the most sophisticated enterprise. So then you kind of go to, all right, I got it that the answer is 4x more expensive, but it's an easy answer. As those of us who work in this world produce much more sort of easy button software that can give you that capability for the alternate models. And I would say it's not a huge amount of infrastructure. Our computation is that for an average large enterprise, you can get going with maybe 2 or 3 racks, which is not a huge amount of infrastructure, but it gives you the ability to run those open-weight models currently anywhere from 25% to 10% of the token cost of the frontier models, that is very attractive given that they are now 90% as effective. 
It's a simple question for any enterprise. Would you like something that's 10% of the cost if it's 90% as good as the best? Or do you want to pay that 10x higher cost? And then the question is, how many tasks require that? I would tell you some do, but the vast majority, summarizing an e-mail, examining a contract, answering a customer call, composing an e-mail, all of those can be done as well with a much cheaper answer, and that is what is going to drive a lot of this. 
So Matt, and everybody else, thanking you for those questions. Look, we are pleased with our performance this quarter and all our segments' accelerated growth. Our portfolio strength, disciplined execution and relentless focus on productivity reinforce my confidence in our trajectory. I look forward to sharing our progress with you as we close out the year, and we'll talk to you in January about that.

**Olympia McNerney** (Executives):
Thank you, Arvind. Operator, let me turn it back to you to close out the call.

**Operator** (Operator):
Thank you for participating on today's call. The conference has now ended. You may disconnect at this time.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### IBM_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜Arvind Krishna｜guidance：全年營收成長預期下修為 4% 至 5%，自由現金流仍預期增加約 10 億美元（原話："revenue growth for the full year in a range of 4% to 5%"）
- 2026-07-22｜James Kavanaugh｜guidance：CFO 稱營收區間低端為基本情境（原話："We believe the low end of the revenue range appropriately"）
- 2026-07-22｜James Kavanaugh｜guidance：軟體全年成長預期下修為 6% 至 8%，低端假設近期支出型態在下半年持續（原話："the low end of the software range assumes that recent"）
- 2026-07-22｜James Kavanaugh｜guidance：基礎設施全年預期上調為低個位數成長（90 天前為下降低至中個位數）（原話："we now expect Infrastructure to grow"）
- 2026-07-22｜James Kavanaugh｜guidance：第三季固定匯率營收成長與全年一致，匯率為 1.5 個百分點逆風，營業稅前利潤率與第二季相近（原話："we now expect currency to be a 1.5 point headwind to revenue"）
- 2026-07-22｜James Kavanaugh｜guidance：下半年交易處理軟體（TP）預期下降低至中個位數，管理層把它放在 2027 年才作為成長動能（原話："we've got TP down low single digits"）
- 2026-07-22｜James Kavanaugh｜margin：全年營業稅前利潤率預期擴張 100 個基點，生產力行動抵銷營收相關逆風（原話："we now expect to deliver 100 basis points of operating"）
- 2026-07-22｜James Kavanaugh｜margin：第二季營業毛利率下降 70 個基點，原因為營收落差與組合；營業稅前利潤率仍擴張 30 個基點（原話："Operating gross profit margins were down 70 basis points"）
- 2026-07-22｜James Kavanaugh｜margin：分部利潤率：顧問 +160bp、軟體 +110bp、基礎設施 −150bp（IBM Z 組合逆風）（原話："segment profit margin declined 150 basis points"）
- 2026-07-22｜James Kavanaugh｜margin：數字口徑：軟體約 80% 為經常性收入，ARR 246 億美元、年增 8%；其餘 20% 為交易型，與大型主機授權協議（ELA）綁定（原話："other 20% of software revenue is transactional in nature"）
- 2026-07-22｜James Kavanaugh｜risk：數字口徑：第二季軟體落差來自大客戶資本支出型交易延後；TP 下降 9%、資料 +18%、自動化 +3%（原話："processing revenue declining 9%, while data grew 18%"）
- 2026-07-22｜James Kavanaugh｜risk：六月最後幾週客戶把預算轉向伺服器、儲存與記憶體採購，數十件大單未如期成交（原話："tens of large deals failed to close on the time lines"）
- 2026-07-22｜Arvind Krishna｜risk：CEO 表示約三分之一遞延交易已在三週內成交，並判斷為遞延而非流失，但自稱尚非完整證據（原話："not yet full evidence, but a good indication"）
- 2026-07-22｜James Kavanaugh｜risk：CFO 對遞延交易成交比例的說法（約 40%）與 CEO（約 1/3）略有不同；高端假設全數成交（原話："Our high-end range says we close all of them"）
- 2026-07-22｜Arvind Krishna｜customer：CEO 解釋客戶因替代採購價格季增約 30% 而挪移預算，IBM 七月未漲價（原話："held our price so far in the month of July"）
- 2026-07-22｜Arvind Krishna｜product：z17 週期至今約為 z16 的 130%（program-to-program），管理層稱沒有客戶離開主機證據；第二季主機營收年減 42%，因去年同期上市基期高（原話："z17 remains at nearly 130% program-to-program"）
- 2026-07-22｜James Kavanaugh｜product：主機年減 42%，管理層歸因於去年上市季成長 70% 的基期（原話："Mainframe overall, yes, down 42%. It's off a 70% growth"）
- 2026-07-22｜Arvind Krishna｜product：分散式基礎設施單季成長 37%，創紀錄（原話："best quarter of revenue growth on record, growing 37%"）
- 2026-07-22｜James Kavanaugh｜product：Red Hat 成長較上季加速 1 點至 11%，RHEL 仍受硬體供應受限影響（原話："Red Hat growth accelerated 1 point sequentially to 11%"）
- 2026-07-22｜James Kavanaugh｜product：顧問簽約成長 6%，生成式 AI 約占簽約 50%、占在手訂單超過 30%（原話："Generative AI represented about 50% of our signings"）
- 2026-07-22｜Arvind Krishna｜product：Lightwell 開源安全修補訂閱，每年 100 萬美元；管理層稱 TAM 為數十億美元，目標數百家客戶（原話："Clients can subscribe to Lightwell for $1 million per year"）
- 2026-07-22｜Arvind Krishna｜capital_allocation：量子運算：宣布五年內投資逾 100 億美元（原話："invest more than $10 billion in Quantum"）
- 2026-07-22｜James Kavanaugh｜capital_allocation：上半年自由現金流 48 億美元，與去年持平；為因應供應吃緊提前備貨，庫存年增約 6 億美元，下半年預期轉為順風（原話："Our inventory exiting the first half is up $600 million"）
- 2026-07-22｜James Kavanaugh｜capital_allocation：季末現金 82 億美元，債務 620 億美元（含融資業務 130 億美元），上半年股利支出 32 億美元（原話："We returned $3.2 billion to shareholders"）
- 2026-07-22｜Arvind Krishna｜commitment：維持全年自由現金流增加約 10 億美元的承諾（原話："expect to grow free cash flow by about $1 billion"）
- 2026-07-22｜Arvind Krishna｜commitment：CEO 重申軟體長期雙位數成長承諾不變（原話："we are not going to back off from our commitment of long-"）
- 2026-07-22｜James Kavanaugh｜commitment：CFO 稱下半年自由現金流將不低於 10 億美元增幅，且自由現金流利潤率創新高（原話："maintain growing free cash flow, at least $1 billion"）
- 2026-07-22｜Arvind Krishna｜competition：敘事：價值將轉向編排與資料層，IBM 強調中立與企業級控制（原話："shift towards the orchestration and data layers"）
- 2026-07-22｜Arvind Krishna｜customer：調整市場進入模式，擴大涵蓋數千家額外客戶，並增加前線部署工程師（原話："expand coverage across thousands of additional clients"）
- 2026-07-22｜Arvind Krishna｜risk：CEO 承認本季在執行面未達標（原話："That is where we fell short in the second quarter"）
- 2026-07-22｜Arvind Krishna｜risk：CEO 說軟體落差約 4–5 億美元，TP 約占大額資本支出型交易的 50–60%，資料軟體也受波及（原話："$500 million of the miss was in software overall"）

### 問答異常語氣（迴避／改口／保留）
- IBM_Q2_2026_Earnings_Call_20260722.md｜問：Ben Reitzes 問 TP（−9%）與主機（−42%）如何改善，以及 4–5% 指引是否可信｜答法：CFO 未給 TP 恢復的時間點，改談主機基礎與 MIPS 容量，並稱 TP 下半年仍下降低至中個位數、改列為 2027 年成長動能
- IBM_Q2_2026_Earnings_Call_20260722.md｜問：Fatima Boolani 追問 85% 穩定或成長的 MIPS 容量之外，另外 15% 發生什麼事｜答法：CEO 只回答遞延交易成交原因，沒有回答另外 15% 的去向
- IBM_Q2_2026_Earnings_Call_20260722.md｜問：Erik Woodring 問為何 IBM 自家有機資料軟體（約年減中個位數）表現落後非 TP 軟體｜答法：CEO 未確認或否認有機資料的下滑數字，以大額資本支出交易受影響和預期未來 12 個月表現良好回應

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
{"date":"20260723","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"軟體段（Red Hat+HashiCorp+Confluent+watsonx）恢復並維持 ~雙位數成長，交易型滑單為遞延非破壞","columns":{"2Y 驗證點":"FY27 軟體 ARR ≥ $28B；交易型軟體回正","5Y 驗證點":"FY30 軟體占公司營收 >50%；80/20 經常性占比升至 >85%","10Y 驗證點":"FY35 軟體 ARR >$45B、經常性 >90%","具體數字門檻 / Sourced Floor":"Sourced：管理層 FY26 軟體 guide 下修至 6–8%（原 10%，Q2'26 逐字稿）；ARR $24.6B +8%（Q1 為 +10%，已放緩）；80% 經常性 +8% 「approaching 10%」狀態：削弱中（guide 破 10% 底、有機 flat）","漂移觸發":"連兩季 ARR YoY"}},{"id":"H2","text":"Consulting 不因 AI 結構性崩塌（Claude Code 衝擊是逆風非 thesis-killer）","columns":{"2Y 驗證點":"Consulting signings YoY ≥ +1%；GenAI signings 比例 ≥ 40%","5Y 驗證點":"FY30 Consulting 段營收 ≥ $22B；backlog GenAI >40%","10Y 驗證點":"Consulting 段轉型為 AI 部署主導","具體數字門檻 / Sourced Floor":"Sourced：Q2'26 signings +6%（第二個連續成長季）、GenAI ~50% 之 signings、>30% backlog、段利潤率 +160bps（逐字稿）狀態：holding／略強化（signings 正、margin 擴張）","漂移觸發":"連兩季 signings YoY ≤ 0% → 削弱；單一 top-100 client 公開 migrate 案例 → 立即降級 trap 🔴"}},{"id":"H3","text":"估值自崩盤位置修復（FCF 續增 + 軟體回升驅動 re-rate）","columns":{"2Y 驗證點":"FY27 Fwd PE 回 ~17–18x；股價 $240+","5Y 驗證點":"FY30 Fwd PE 穩定 16–19x；股價 $280+（5Y target）","10Y 驗證點":"與 ACN/成熟軟體中位收斂","具體數字門檻 / Sourced Floor":"Sourced：現 Fwd PE 16.9x（FY26 non-GAAP $12.16 基）；EV/EBITDA 15.1x vs 5Y 中位 17.1x（近 5Y 低）；但非同業折價——HSBC 指 IBM 仍在 CY27e 22x（同業中位 16.9x）之溢價（GuruFocus/HSBC）狀態：反轉（市場 de-rate 而非 re-rate）","漂移觸發":"連四季 Fwd PE 停在"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI capex 對企業軟體錢包的排擠從 20% 交易型軟體外溢至更廣（記憶體/HBM 超級循環延續至 2027–28，逼單機制不退）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（2–3 年結構背景）","監測指標":"交易型軟體 TPP YoY；80% 經常性軟體 YoY 是否也開始鬆動","警戒閾值":"經常性軟體連兩季跌破 +6% → 排擠外溢確認、H1 反轉"}},{"id":"R2","text":"Claude Code／Cursor 等 AI coding 工具侵蝕 Consulting COBOL 現代化與 IBM Z 綁定","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4–6 季）","監測指標":"Consulting signings YoY；單一 top-100 client 公開 migrate off mainframe","警戒閾值":"signings 連兩季 ≤0% → 觸發；公開 migrate 案例 → 立即 trap 🔴（並見 §3.F）"}},{"id":"R3","text":"有機軟體長期 flat，成長依賴越來越貴的併購（出價紀律惡化 + 整合失利）","columns":{"對應假設":"H1／H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"剔除併購後有機軟體成長率；HashiCorp/Confluent 整合 churn 與 ARR","警戒閾值":"剔併購有機成長連四季 ≤ +3% → 品質降級、re-rate thesis 破"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Q3 2026（~10 月）軟體回升至 ≥ 高個位數 cc + 滑單 ≥ 75% 收回 + 無第三次砍 guide；或 Fwd PE ≤ 13.5x（~$165）之同業折價","irr_base_pct":6.7,"ev5y_pct":30.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.0,"ev5y_pct":30.5,"irr_base_pct":6.7,"max_dd_pct":-35.0,"bull_5y_price":370.0,"bear_5y_price":161.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Q3 2026（~10 月）軟體回升至 ≥ 高個位數 cc + 滑單 ≥ 75% 收回 + 無第三次砍 guide；或 Fwd PE ≤ 13.5x（~$165）之同業折價","price_at_dd":205.77,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
