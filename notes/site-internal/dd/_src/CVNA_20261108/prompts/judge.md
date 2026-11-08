你是 stock-analyst **v20 判斷 agent**，標的 CVNA（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CVNA","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":8040,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）"},"note":"未查得"},{"id":"f_kpi1","label":"零售銷量","value":217385,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"輛","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）"},"note":"未查得"},{"id":"f_kpi2_ebitda_non_gaap","label":"調整後 EBITDA（公司不報 non-GAAP 營業利益，以此代之）","value":800,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"百萬美元（利益率 10.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）"},"note":"未查得"},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":714,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"百萬美元（利益率 8.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）"},"note":"未查得"},{"id":"f_kpi4_gaap","label":"GAAP 淨利","value":483,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"百萬美元（淨利率 6.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）"},"note":"EPS 約 $0.39 對共識約 $0.47–0.48（Zacks 等第三方，低於預期）"},{"id":"f_kpi6","label":"管理層指引","value":"Q4 零售銷量較 Q3 季增；2026 全年調整後 EBITDA 落在先前區間 27–30 億美元的偏高端（假設環境穩定）","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"文字","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）"},"note":"無數值型 Q4 指引"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 8 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cvna_gross_margin_pct","label":"CVNA 毛利率","value":19.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CVNA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cvna_operating_margin_pct","label":"CVNA 營業利益率","value":8.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CVNA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cvna_fcf_margin_pct","label":"CVNA FCF 利潤率","value":4.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CVNA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kmx_gross_margin_pct","label":"KMX 毛利率","value":10.31,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KMX.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kmx_operating_margin_pct","label":"KMX 營業利益率","value":-1.4,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KMX.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kmx_fcf_margin_pct","label":"KMX FCF 利潤率","value":4.15,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KMX.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_an_gross_margin_pct","label":"AN 毛利率","value":17.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_an_operating_margin_pct","label":"AN 營業利益率","value":4.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_an_fcf_margin_pct","label":"AN FCF 利潤率","value":0.8,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lad_gross_margin_pct","label":"LAD 毛利率","value":15.14,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LAD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lad_operating_margin_pct","label":"LAD 營業利益率","value":3.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LAD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lad_fcf_margin_pct","label":"LAD FCF 利潤率","value":-1.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LAD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_acva_gross_margin_pct","label":"ACVA 毛利率","value":50.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACVA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_acva_operating_margin_pct","label":"ACVA 營業利益率","value":-7.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACVA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_acva_fcf_margin_pct","label":"ACVA FCF 利潤率","value":-0.87,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACVA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":3.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%（SBC 25 百萬；占營收 0.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）；比例為自算 25/714"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":73.57,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-5.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":62.82,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.52 → 1.52）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_largecap_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.12 → 2.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_largecap_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.73 → 2.73）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_largecap_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.52,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_largecap_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.12,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_largecap_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":2.73,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_largecap_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":35.37,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝90.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":90.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.07,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝87.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":87.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":48.4,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.52，分子＝快照價 73.57","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":2091.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 5697.0、現金 3606.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1491.91,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":111850.68,"period":"2026-11-08","unit":"USD m","basis":"市值 109759.68 ＋ 淨負債 2091.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":29731.63,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":37481.56,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.76,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 73.57 / W52 71.08 / W104 63.94 / W250 33.9 / W250 13週斜率 1.4%"},{"id":"f_ma_w52","label":"52 週均線","value":71.08,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":63.94,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":33.9,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.4,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K：Carvana 估計占美國二手車零售約 1.6%，前十大二手車零售商合計不到 10%，市場高度分散。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"Carvana currently has an estimated market share of only approximately 1.6%.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出的競爭者包括 CarMax、Amazon、Costco Auto Program、車廠（Ford、GM、Toyota、Tesla、Rivian、Lucid 等），並預期新舊競爭者持續進入。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"We also expect that competitors, both new and existing, will continue to enter the online and traditional automotive retail industry with competing brands, business models, products, and services","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"搜尋摘要：Carvana 2026 Q2 零售銷量 197,325 輛、年增 38%，連續第 10 季領先業界成長，同期業界下滑；公司稱約占二手車市場 2%。","source":"Quartr / CVNA 2Q26 transcript 摘要","url":"https://quartr.com/events/carvana-co-cvna-q2-2026_3PG9FNED","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Amazon Autos 擴及二手與認證二手車，被視為對 Carvana 的潛在新進入者威脅，但目前僅限單一城市、單一車廠，短期影響有限（2025-08 分析）。","source":"247WallSt: Carvana Surged 8,200% in 2+ Years. Is Amazon About to Wreck Its Rally?","url":"https://247wallst.com/investing/2025/08/06/carvana-surged-8200-in-2-years-is-amazon-about-to-wreck-its-rally/","excerpt":null,"as_of":"2025-08-06","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Carvana Q3 2026 零售銷量 217,385 輛、年增 39%，營收 $8.04B 年增 42%；調整後 EBITDA 利潤率 10%（去年同期 11.3%）；管理層預期 Q4 零售量季增（假設市況穩定）。","source":"Finviz/BusinessWire: Carvana Announces Record Third Quarter 2026 Results","url":"https://finviz.com/news/410551/carvana-announces-record-third-quarter-2026-results","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Cox Automotive 2026 展望：二手零售量約 20.3M（-0.7%），後調升至 20.4M；新車負擔能力壓力推動消費者轉向二手車；未找到 Cox 對 2027–2028 的預測。","source":"Cox Automotive 2026 forecasts full year","url":"https://www.coxautoinc.com/insights/2026-cox-automotive-forecasts-full-year/","excerpt":null,"as_of":"2026-01-07","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Manheim 預測租賃退場車 2026 年 2.4M、2027 年 3.1M，二手車價 2026 年約 +2%","source":"32cars.ru US used car market outlook 2026","url":"https://www.32cars.ru/en/posts/id11456-us-used-car-market-outlook-2026-steady-demand-high-prices","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"批發二手車價創近三年高點，供給偏緊、新車均價逾 $49,000 推動需求轉向二手","source":"ConsumerAffairs: Used-car prices climb as tight supply makes it tougher for buyers","url":"https://www.consumeraffairs.com/news/used-car-prices-climb-as-tight-supply-makes-it-tougher-for-buyers-040926.html","excerpt":null,"as_of":"2026-04-09","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 法律程序章節：2025年6月收到SEC傳票，主要涉及做空機構報告的指控，公司表示全面配合；未提及反壟斷調查或拆分。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"In June 2025, we received a subpoena from the SEC requesting information that we believe primarily relates to the allegations raised by the report. We are fully cooperating with the SEC Staff.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 列明受CFPB、FTC、DOT、DOJ、SEC等聯邦及各州經銷商監管機關管轄，屬一般產業監管，未列特定新規。","source":"SEC EDGAR 10-K FY2025 Item 1 Government Regulation","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"the advertising, sale, purchase, financing, and transport of motor vehicles are highly regulated by states in which we do business and by the U.S. federal government.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"2026年搜尋未見DOJ/FTC/反壟斷對Carvana的調查報導；結果均為2026-01-28 Gotham City做空報告後原告律所的證券詐欺調查公告（非主管機關行動）。","source":"WebSearch 結果摘要（BFA Law、Kirby McInerney等新聞稿）","url":"https://www.businesswire.com/news/home/20260129225947/en/CARVANA-CO.-INVESTOR-ALERT-Kirby-McInerney-LLP-Announces-Investigation-Into-Potential-Securities-Fraud","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子將美國聯邦政府關稅或貿易限制的實施／暫停列為可能影響業務的汽車生態系因素。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"Finally, the imposition or suspension of tariffs or other trade restrictions implemented by the U.S. federal government or other countries, including changes to the import tariffs implemented by the U.S.…","as_of":"2026-02-18","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"公司於 MD&A 表示 2025 年關稅對財務與營運結果無重大影響。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"For the year ended December 31, 2025, tariffs did not materially impact our financial or operating results.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因子比對：關稅風險因子擴充至美國車輛與零件進口關稅，並新增拉丁美洲地緣條件措辭（第三方摘要，未核原文）","source":"footnotefox CVNA risk factor changes","url":"https://footnotefox.pages.dev/samples/cvna-riskfactor-changes","excerpt":"tariff changes affecting supply costs and consumer behavior — \"changes to the import tariffs implemented by the U.S. on vehicles and parts, and uncertainty regarding the same, may change vehicle supply or the supply or cost of important vehicle parts and components\" Escalated Geopolitical risk broadened to add new flashpoints, specifically naming U.S.-Venezuela military action and Latin America","as_of":"2026-02-19","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026（2026-10-28 公布）：零售 217,385 台（+39% YoY），總營收 $8.040B（+42%）；分段：零售 $6.144B（+54%）、批發 $1.302B（+11%）、其他 $594M（+25%）；零售 GPU $3,625（+2.4%），總 GPU $7,093（-$410 YoY）","source":"Carvana Q3 2026 results (finviz news / aggregator summary)","url":"https://finviz.com/news/410551/carvana-announces-record-third-quarter-2026-results","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"公司計畫自 Q4 財報起停止給指引、2027 轉 GAAP 導向；長期目標每年 300 萬台、2030–2035 GAAP 營業利益率 12.5%","source":"Carvana Q3 2026 results (aggregator summary)","url":"https://finviz.com/news/410551/carvana-announces-record-third-quarter-2026-results","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Cox Automotive 2026 展望：二手車總銷量 -0.9% 至 38.3M、零售二手 20.3M（-0.7%）；Manheim 二手車價格指數年底預估約 +2%；4月據報上修零售二手至 20.4M，但下半年可能放緩（次級來源）","source":"Cox Automotive 2026 used outlook (via am-online / aggregators)","url":"https://www.am-online.com/news/cox-forecasts-stable-2026-used-market-but-flags-supply-risks","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Carvana 占美國二手車市場約 1.5%–2%（來源間分歧）；管理層 300 萬台目標約相當美國二手車市場 10%；Wedbush 相關筆記預期若持續搶占份額，批發對零售價差 12–24 個月內壓縮約 100–200bps（次級聚合來源）","source":"aggregator pages incl. Q2 2026 transcript (statementdog)","url":"https://statementdog.com/analysis/CVNA/earnings_calls/315906","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：公司自述日益依賴第三方生成式 AI 平台與內部軟體，AI 表現不如預期可能造成轉換率下降、營運中斷與品牌受損（屬自身技術風險，非外部替代品）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"We increasingly develop and deploy AI technology through third party generative AI platforms and internal software, in connection with our proprietary systems and customer experiences, including automated, self-service workflows, AI-enabled customer support tools, internal work efficiencies, and enhancement of our recruiting and hiring processes.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 業務章節：美國二手車零售高度分散，前十大零售商 2024 年合計市占不到 10%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"the top 10 used auto retailers in the U.S. accounting for less than 10% of the market share in 2024","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"經銷商產業人士預測 agent-to-agent 購車 2029 年成為常態（預測，非事實）。","source":"Car Dealership Guy newsletter","url":"https://news.dealershipguy.com/p/car-dealership-guy-founder-ceo-shares-9-auto-retail-predictions-by-2029","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Hertz 宣布推出直接向消費者線上銷售二手車平台，與 Carvana、CarMax 競爭。","source":"Bloomberg Government","url":"https://news.bgov.com/bankruptcy-law/hertz-pushes-into-online-car-sales-in-competition-with-carvana","excerpt":"Hertz Enters Online Car Sales in Competition With Carvana (1) Sept. 30, 2025, 5:32 PM UTC David Welch Bloomberg News Hertz Global Holdings Inc. and Carvana Co.","as_of":"2025-09-30","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Carvana 買下亞利桑那州 Casa Grande 的 Chrysler-Dodge-Jeep-Ram 特許經銷商，為其首次進入新車銷售（先前自 2013 年起只賣二手車）；另有來源稱已取得第六家 Stellantis 經銷商（聚合站，需另核）。","source":"CBT News｜Carvana acquires Arizona dealership in bold move toward new car sales","url":"https://www.cbtnews.com/carvana-acquires-arizona-dealership-in-bold-move-toward-new-car-sales/","excerpt":null,"as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 載明公司定位為二手車電商平台，結合線上銷售與垂直整合供應鏈，估計市占約 1.6%；競爭者含 CarMax、Amazon、Costco Auto Program 及車廠。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"Carvana is the leading e-commerce platform for buying and selling used cars.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Carvana Q3 2026 未上調全年 guidance，預期全年 Adjusted EBITDA 在先前 $2.7–3.0B 區間高端；稱從 Q4 2026 財報起停止提供季度/年度展望；燃油與利率上升使單位經濟下降約 $200/台","source":"SEC 8-K ex99 Q3 2026 / Auto Dealer Today","url":"https://www.sec.gov/Archives/edgar/data/0001690820/000169082026000066/ex99_2q32026.htm","excerpt":"•Adjusted EBITDA1 in the higher end of our previously communicated range of $2.7 to $3.0 billion for the full year 2026.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 共識目標價約 $84.14（24 位分析師，區間 $48–$120，Moderate Buy），as-of 2026-08-05","source":"MarketBeat CVNA forecast","url":"https://www.marketbeat.com/stocks/NASDAQ/CVNA/forecast/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"SEC 於 2025-06 對 Carvana 發出傳票（主要涉及空頭報告指控）；FY2025 10-K 稱公司全力配合。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"In June 2025, we received a subpoena from the SEC requesting information that we believe primarily relates to the allegations raised by the report. We are fully cooperating with the SEC Staff.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"2026-09 SEC 告知已結束調查、不擬建議執法行動（10-Q FY2026 Q3，搜尋摘要引述）。","source":"SEC EDGAR 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001690820/000169082026000067/cvna-20260930.htm","excerpt":"In September 2026, the SEC informed us that it had concluded its investigation and did not intend to recommend an enforcement action against us in connection with the matter.","as_of":"2026-10-28","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2022 年證券集體訴訟 In re Carvana Co. Securities Litigation 仍列於 FY2025 10-K 法律事項（非近12月新案）。","source":"SEC EDGAR 10-K FY2025 Note 16","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"On August 3, 2022, a putative class action complaint titled John Brent v. Carvana Co., et al. was filed in the United States District Court for the District of New Jersey against the Company and certain of the Company's executive officers.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2026-01-28 Gotham City Research 發空頭報告後股價單日跌約14.2%，多家原告律所宣布調查；搜尋未見 2026 新集體訴訟起訴。","source":"Pomerantz 投資人通知（placera.se 轉載）","url":"https://www.placera.se/pressmeddelanden/carvana-investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-carvana-co-cvna-20260130","excerpt":null,"as_of":"2026-01-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"2026-05 收購七家 Stellantis 經銷店進入新車銷售（聚合站報導，規模小）；2026-08-14 8-K 簽 $1.66B 定期貸款B 以再融資 2030 年到期票據。","source":"pulse.bot 聚合；SEC 8-K 2026-08-14","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000059/cvna-20260814.htm","excerpt":"The Credit Agreement provides for a $1.66 billion senior secured term loan B facility maturing on August 14, 2033 (the “Term Loan B Facility”).","as_of":"2026-08-14","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12月僅小型經銷店收購（七家 Stellantis 經銷店，2026-05-18 公布，聚合站報導）；一手 8-K 清單無 2.01 項目，未見大型併購。","source":"pulse.bot 聚合；SEC 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001690820&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2022 年證券集體訴訟仍列於 10-K；2026-01 Gotham 空頭報告後多家律所宣布調查，未見新案起訴。","source":"SEC EDGAR 10-K FY2025 Note 16","url":"https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm","excerpt":"The two cases were then consolidated and subsequently transferred to the United States District Court for the District of Arizona (the \"Arizona District Court\") as In re Carvana Co. Securities Litigation, United States District Court for the District of Arizona (Case No. CV-22-2126-PHX-MTL).","as_of":"2026-02-18","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"+","claim":"SEC 2025-06 傳票；2026-09 SEC 告知結束調查、不建議執法；未見重編財報。","source":"SEC EDGAR 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001690820/000169082026000067/cvna-20260930.htm","excerpt":"In September 2026, the SEC informed us that it had concluded its investigation and did not intend to recommend an enforcement action against us in connection with the matter.","as_of":"2026-10-28","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"CVNA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.04,"operating_margin_pct":8.74,"fcf_margin_pct":4.05,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CVNA","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KMX","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":10.31,"operating_margin_pct":-1.4,"fcf_margin_pct":4.15,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KMX","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":17.73,"operating_margin_pct":4.28,"fcf_margin_pct":0.8,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AN","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"LAD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.14,"operating_margin_pct":3.59,"fcf_margin_pct":-1.12,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LAD","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ACVA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.98,"operating_margin_pct":-7.09,"fcf_margin_pct":-0.87,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACVA","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"CVNA"},"financial_history":{"ticker":"CVNA","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":13604000000.0,"revenue_yoy_pct":null,"gross_margin_pct":9.16,"operating_margin_pct":-11.06,"net_income":-1587000000.0,"diluted_eps":-3.148,"free_cash_flow":-1836000000.0,"fcf_margin_pct":-13.5,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":10771000000.0,"revenue_yoy_pct":-20.82,"gross_margin_pct":16.01,"operating_margin_pct":-0.74,"net_income":450000000.0,"diluted_eps":0.15,"free_cash_flow":716000000.0,"fcf_margin_pct":6.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":13673000000.0,"revenue_yoy_pct":26.94,"gross_margin_pct":21.03,"operating_margin_pct":7.24,"net_income":210000000.0,"diluted_eps":0.318,"free_cash_flow":827000000.0,"fcf_margin_pct":6.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":20322000000.0,"revenue_yoy_pct":48.63,"gross_margin_pct":20.63,"operating_margin_pct":9.26,"net_income":1407000000.0,"diluted_eps":1.69,"free_cash_flow":889000000.0,"fcf_margin_pct":4.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CVNA/CVNA_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**Carvana Co.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Good day, and welcome to Carvana's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please note, this event is being recorded. I would now like to turn the conference over to Austin Knutson with Investor Relations. Please go ahead.

**Austin Knutson** (Executives):
Thank you very much. Good afternoon, ladies and gentlemen, and thank you for joining us on Carvana's Third Quarter 2026 Earnings Conference Call. Please note that this call is being webcast and can be accessed along with our Q3 shareholder letter and supplemental financial tables on the Investor Relations section of the company's corporate website at investors.carvana.com.
Joining me on the call today are Ernie Garcia, Chief Executive Officer; and Mark Jenkins, Chief Financial Officer. Before we start, I would like to remind you that this discussion contains forward-looking statements within the meaning of the relevant federal securities laws, including, but not limited to, Carvana's market opportunities and future financial results that involve risks and uncertainties that may cause actual results to differ materially from those discussed here.
A detailed discussion of these risk factors can be found in the Risk Factors section of Carvana's most recently filed Forms 10-K and 10-Q. These forward-looking statements are based on current expectations as of today, and Carvana assumes no obligation to update or revise them. Our commentary today also will include non-GAAP financial metrics. GAAP reconciliations can be found in the shareholder letter posted on our IR site.
With that, I'd like to turn the time -- turn the call over to Ernie Garcia. Ernie?

**Ernest Garcia** (Executives):
Thanks, Austin, and thanks, everyone, for joining the call. Also a shout out to Meg, who's at home with her second and should be on a walk, but is almost certainly listening to this call. So Meg, go for a walk, it's nice out. We got this.
The third quarter was another exciting quarter for Carvana. Our focus remains on building the machine to deliver 3 million units per year and 13.5% adjusted EBITDA margin, and the steady drumbeat of results heading in that direction is evidence of both the team's execution and the achievability of those goals.
First, let's look at the progress we are making scaling the machine. This is our first quarter with over 200,000 sales. Our run rate is now 870,000, double what it was just 2 years ago. This was also our first quarter with $8 billion of revenue. Our run rate is now $32 billion, more than double what it was 2 years ago.
Next, let's look at the financial results our machine continues to post despite the pressures of growth and an imperfect backdrop of increasing interest rates and gas prices.
Our adjusted EBITDA in the third quarter was $800 million, a run rate over $3 billion, almost double what it was 2 years ago. And our net income was $480 million, a run rate of almost $2 billion, more than double what it was 2 years ago. We are the fastest-growing automotive retailer with 8 consecutive quarters of approximately 40% growth in an industry that's flat. And we are the most profitable automotive retailer with margins that are approximately twice the industry average for the 10th quarter in a row. The experience we deliver our customers has always been the foundation for the success and the team's hard work as well as the positive feedback in the model continues to separate us further from the pack here as well. Over the last 2 years, our NPS has improved by 9 points as we are delivering cars to our customers 2 days faster, we've lowered the interest rate our customers pay by over 100 basis points, and we've made the entire Carvana experience simpler and more intuitive. The machine is getting better.
Despite the market share gains from doubling in 2 years in a flat industry and despite our scale of 870,000 unit run rate, we still have just over 2% of used market share and 1.5% share overall. We are still extremely early in the game. In the letter, we briefly touched on another benefit of our vertically integrated model. In building it to serve our core business, we have created a very capable, scaled platform. Our early success with Stellantis new cars is a clear demonstration of the platform value of Carvana's operations, technology, brand and infrastructure. 
In addition, our model is structurally different in a way that it not only met the moment of the last 14 years, but also meets the moment of today. A question that we constantly ask ourselves in every part of the business is this. If we were building this today from scratch, what would we build? With a rapid increase in the capabilities of AI and with the first early looks at the opportunities agentic commerce will provide, it's a relevant question with an exciting answer. If we were starting from scratch today, we would build Carvana.
AI is most powerful when decisions are automated and deterministic, when technology is architected to rapidly surface those answers, when there's a steady stream of differentiated data to feed it and in the presence of vertical integration where experiences get simpler and frictions between layers disappear. Carvana has all of this. Agentic commerce is much earlier in its maturity, but it seems likely to accelerate digital adoption to reward companies who have put their effort into building fundamentally better solutions and to put pressure on supply chains to be as low cost and fast as possible. Carvana also has all of this. It's an exciting time. If we keep building the machine, good things are going to keep happening. The march continues. Mark?

**Mark Jenkins** (Executives):
Thank you, Ernie, and thank you all for joining us today. Unless otherwise noted, all comparisons will be on a year-over-year basis. Q3 was another strong quarter for Carvana. We set new company records for retail units sold, revenue, gross profit, GAAP operating income and adjusted EBITDA. These results were driven by our company-wide focus on driving profitable growth and efficient operational execution.
Retail units sold totaled 217,385 in Q3, an increase of 39% and a new company record. Revenue was $8.04 billion, an increase of 42% and a new company record. Consistent with past quarters, our growth in the third quarter was driven by our 3 long-term drivers of growth: a continuously improving customer offering; increasing awareness, understanding, and trust; and increasing inventory selection and other benefits of scale.
The third quarter marked our 11th consecutive quarter of industry-leading retail unit growth and [ industry-leading ] adjusted EBITDA margin. Non-GAAP retail GPU increased by $85, primarily driven by wider spreads between retail and wholesale market prices, partially offset by higher non-vehicle costs.
Non-GAAP wholesale GPU decreased by $196, primarily driven by our 39% retail units sold growth outpacing our wholesale gross profit growth.
Non-GAAP other GPU decreased by $299, primarily driven by our decision to give back to customers in the form of lower interest rates relative to benchmark rates as well as by rising benchmark rates in the third quarter, partially offset by higher average amount financed and hedging gains.
Non-GAAP SG&A expense per retail unit sold was approximately flat. Operations expense increased $109 per retail unit sold, primarily due to higher fuel and logistics costs. This increase was more than offset by a $159 per retail unit sold reduction in overhead expense, driven by our 39% growth rate.
Advertising expense increased by $45 per retail unit sold as we continue to invest in building awareness, understanding and trust in our customer offering.
We continue to see opportunities for significant SG&A leverage over time as we scale, driven by both continued improvements in operational expenses as well as leverage in the fixed components of our cost structure.
Net income was $483 million, an increase of $220 million. Net income was negatively impacted by a onetime $53 million pretax expense related to the early redemption of senior secured notes.
Net income margin was 6%, an increase from 4.7%. Adjusted EBITDA was a record $800 million, an increase of $163 million. Adjusted EBITDA margin was 10%, a decrease from 11.3%, primarily driven by selling a mix of higher-priced vehicles and giving back to customers in other GPU.
GAAP operating income was $714 million, or 89% of adjusted EBITDA, an increase of $162 million and a new company record.
Before turning to the balance sheet, I want to spend a moment on what sits underneath these results, the machine we are building to deliver on our long-term goals. With the scale of our ambition, building the machine is a continuous exercise, and our execution is the pacesetter for our growth. That machine has 3 components: selection, speed and experience. Each of these maps to one or more major operational groups. Our inspection and reconditioning centers drive selection. Our logistics and delivery network drives speed. And these plus our customer care centers drive customer experience. Within those groups, the work is carried out by our people, including technicians and cosmetic associates, vehicle transporters, last-mile delivery and customer care advocates, and many more. As we grow at 39%, our ability to hire and train these teams and to give them better tools and processes directly determines how we scale. We are actively working on each of these areas, and we are encouraged by the progress we are making.
Turning to the balance sheet. We continue to drive toward investment-grade quality credit ratios. Early in the third quarter, we further strengthened our balance sheet by refinancing the remaining $1.7 billion of senior secured notes due 2030 with a senior secured Term Loan B, resulting in approximately $45 million of annual interest expense savings. This transaction, along with the successful execution of our operational plan in Q3, resulted in a net debt to trailing 12-month adjusted EBITDA ratio of 0.8x and a trailing 12-month adjusted EBITDA to interest expense ratio of 6.9x, both new company records and again placing us in our strongest financial position ever.
Our results through Q3 position us well for a strong finish to 2026. Looking forward, we expect the following as long as the environment remains stable: a sequential increase in retail units sold and adjusted EBITDA in the higher end of our previously communicated range of $2.7 billion to $3.0 billion for the full year 2026.
In closing, we are excited by what our team accomplished in Q3. We remain focused on executing at a high level, delivering profitable growth, and making consistent progress toward our goals of becoming the largest and most profitable auto retailer and buying and selling millions of cars.
Thanks for your attention. We'll now take questions.

**Operator** (Operator):
[Operator Instructions] The first question comes from Marvin Fong with BTIG.

**Marvin Fong** (Analysts):
Congratulations on managing all this growth. A question on other GPU and the interest rate environment, a lot of conversations among investors heading into this. Just, how are you managing that kind of -- into the fourth quarter? Are you -- you continue to talk about the 100 basis points of improvement to consumers. Are you passing along the full increase in the benchmarks? Or how should we kind of think about how you're approaching that?

**Mark Jenkins** (Executives):
Sure. Yes, I can take that one. So I think I would break that question into a couple of different concepts. The one is the idea of giving back to customers. And there, I think an important moment was in late 2025, we elected to pass back some of the fundamental gains that we had driven in other GPU over the preceding time periods to customers in the form of lower customer interest rates relative to benchmark rates. And so that's a component of the question and a place where we've long talked about, hey, as we drive fundamental gains, over time, we'd love to pass back some of those fundamental gains to customers to improve our customer offering, increase our competitive differentiation and continue to just build the best offering for customers as we strive toward our long-term goals. So that's the -- this idea of passing back gains to customers in the form of lower interest rates.
Now the second part of your question relates to the interest rate environment over the last couple of quarters. And it has been now over the last couple of quarters, really actually this full year, a rising rate environment. And so when we're in a rising rate environment, generally speaking, our mindset is to pass back -- pass gain movements in a rising rate environment, that means increases in the benchmark rate to customers. Now we won't always do that in full necessarily, and there can often be delays or lag times between when benchmark rates rise and when we pass back gains to customers. But as we've seen these rising rates in the past couple of quarters, we have been passing back some of those benchmark rate moves to customers.
And I think we -- that was definitely delayed in the second quarter. We saw that in our other GPU results in Q3, benchmark rates continued to rise meaningfully over the course of the quarter. But we didn't see a meaningful change in other GPU quarter-over-quarter, in part because we had sort of started the motion on passing some of those benchmark rates through. So that's a pretty fulsome description of the dynamics. I think of those 2 things separately. One is what was sort of the strategic path back to fundamental gains last year and then how are we responding to these recent rate moves?

**Marvin Fong** (Analysts):
That was great. And a follow-up, if I may. Just on retail GPU, pretty flat quarter-over-quarter. That was actually a very good performance relative to some of the other publics. How -- you're still talking about some inefficiencies in the business. The ones that emerged sort of in the fourth quarter of last year, where are we in catching up to that? And just kind of comment in general how you kind of feel about retail GPU.

**Mark Jenkins** (Executives):
Sure. Yes. No. So I think it was a strong quarter for retail GPU. I think if we look on a year-over-year basis, I think we break it down as we see retail-to-wholesale spreads up year-over-year, partially offset by higher non-vehicle costs; some of those higher non-vehicle costs were driven by inbound fuel costs. So that was a place where rising fuel prices impacted the business in the quarter. But overall, I think we're pleased with certainly the gains that we made in reconditioning efficiency since early Q4/early Q1 area where we were talking more about some of the cost inefficiencies that have crept into the system. So I think overall, good trends there. I think a dual part of reconditioning, there's cost and then there is production capacity.
And so Q3 was a quarter where we did make gains in production capacity. We set a record for units produced in the quarter. It was our first quarter producing more than 200,000 units in a single quarter. That's a nice milestone. Our year-over-year growth in production also accelerated slightly relative to Q2, which I think is the direction that we want to head, and we slightly outgrew retail units sold from a -- or we slightly outproduced retail units sold in Q3, which is also definitely a direction that we want to head. So I think we made some nice gains in production.
Having said that, there's still more work to do, and continuing to increase production capacity is going to be a key area of focus as we look forward. As one example of that, growth in the number of cars that are on the website immediately available to customers is still up year-over-year at a rate that is much below what our sales growth is year-over-year. And so that's something we want to change, and we're going to continue to invest in getting the right people, process and systems in place in the reconditioning centers to efficiently scale production.

**Operator** (Operator):
The next question comes from Daniela Haigian with Morgan Stanley.

**Daniela Haigian** (Analysts):
Great. Mark, first one for you. Where do you think the biggest area of opportunity is in SG&A for leverage? Can you kind of talk through the puts and takes? Ad spend is higher, as you mentioned, on a per unit basis, assuming that remains similar into the fourth quarter and '27 and fuel costs remain elevated, how should we think about other line items leveraging?

**Mark Jenkins** (Executives):
Sure. Yes. So I mean, I think if we take a step back and think about the opportunities through the entire SG&A stack, I think there's opportunities in every area. So let me start with overhead. We do have a high fixed cost business where we make significant technology investments. We have large investment in infrastructure that we think levers well over time. And so we see significant opportunities to further lever overhead expenses over time. I think that's an area where we have shown really significant leverage over the past several years as well, but I do believe that's an area that affords significant further leverage as we look out over time on a per retail unit sold basis.
Next, I'll talk about advertising expense. We made the point before that advertising expense is a place where not necessarily in the near term, but certainly in the longer term, see opportunities for meaningful advertising leverage as we continue to raise awareness, understanding and trust, build out our selection, improve speeds, et cetera, enhancing the customer offering. A good data point on that is just the fact that our most mature markets that have -- the most nearby inventory at the fastest delivery times have historically had a much lower advertising expense per unit than the company as a whole. And so advertising, not necessarily in the near term, but certainly in the long term, is a significant SG&A leverage opportunity.
Last, I'll talk about operations expenses. So operations expenses did tick up in Q3. I think fuel and logistics cost was definitely a component of that, and certainly the largest component of that. And so that bucks sort of a longer-term secular trend on operations expense per unit declining. I think if we look in the longer term, there's significant opportunities there, driven by AI and by scale and logistics network density that can cause operations expense per unit to come down on a per retail unit sold basis in the fullness of time as well. So that's a lot of different components. But really, as we do look across those major SG&A categories, we see opportunity for leverage as we look out into the future.

**Daniela Haigian** (Analysts):
Great. Second one is for you, Ernie. You mentioned in opening remarks, opportunities in agentic AI. What's the opportunity for Carvana there? How are you positioning the business to capitalize on that shift in consumer behavior?

**Ernest Garcia** (Executives):
Sure. Well, first, I would say that we were excited by the fact that we think that we've been positioning the business for that kind of a shift for 14 years. And I think what agentic AI is basically just putting general AI capabilities that can also take actions into the pockets of consumers. And we think it has a lot of things that are very good for us. We think just through habit formation, in general, it pushes people more in the direction of digital transactions. And then we think that it also, as a general matter, has kind of the capacity to effectively reduce digital friction to 0 while leaving physical friction largely unchanged.
What I mean by that is, if a customer comes to Carvana through their agent and we're able to verify that the agent has a customer behind it, and that agent has access to everything that is necessary for that customer to get a trade-in value and knows which cars to shop for, and is able to apply for credit and has access to their documents to provide information we need for verifications, the customer's experience there is going to basically be: we found the car, here's the picture, here's the trade-in value. Here's how it compares to benchmarks.
We applied for financing. Here's your down payment and your monthly payment with the trade-in applied. If you'd like this one, it can be here today. If you want this one, it can be here tomorrow. And if you want one of these 2, it can be here in 2 days. And it's kind of, say, yes or no. It's kind of like the logical extreme of where that can go. I think when you compare that to what we compete with, which is what's important: whenever there's technological change, what matters is what we can do, but also what the competition can do. The experience the customer is going to get is likely to be very different.
First of all, the odds that the agent can even find a car that is similar in the entirety of the city is not certain. I think in many large metropolitan areas today with the inventory that we have, we already have more cars than the sum of dealers in many, many areas, and that's a strength that continues to get stronger. So there's -- the agent will figure out what's the best match that it's got. Then it will probably say here's the process to get a trade-in value.
If you go in, this dealer has this doc fee associated with it, and they may have additional add-ons that are either part of the car that you'll run into as you go through that process, make sure you keep me in your pocket so I can keep you informed along the way. We can't yet see what your interest rate is going to be. But given benchmarks and tools that we can find online, here is roughly what we think the range is likely to be. If you'd like to apply for a loan before you go, here's a series of steps that you can go through. And so you can kind of see where not only is it reducing the digital friction, it is also fully revealing and articulating the physical friction.
And so we think that's a huge advantage for us. We think, like we said in the prepared remarks, if we were building from scratch today, we would build Carvana. And so we think it's a huge opportunity for us. We're excited by it. I think it's very early days. I think it's one of many tools that will be in the pockets of consumers over time. And we think that sum of those tools is just going to put pressure on businesses to build fundamentally better solutions. And we're 14 years into building a completely different supply chain and a completely different approach to this business that is more efficient and more vertically integrated and benefits from all these changes. So we're extremely excited by it.

**Operator** (Operator):
The next question comes from Brad Erickson with RBC Capital Markets.

**Bradley Erickson** (Analysts):
Just 2 on the other GPU. I guess just when you think about gain on sale levels going forward and kind of across your 3 major selling channels there, just -- what should we expect in terms of these levels going forward kind of in the 7% range? And then how will each of those channels kind of perform within that?
And then second, you upsized the ABS deal, I think you did during the quarter for the first time. And I guess the question is like, should we expect future deals to look like that? And if so, kind of what would you recommend investors read into a deal that gets upsized versus one that does not?

**Ernest Garcia** (Executives):
Sure. So let me start with -- you framed the question in kind of premium space instead of dollar space. And I think that it's useful to look at it both ways. I think over the last year or so as we've given rate back to customers, and that rate has been disproportionately in the primary, we've seen more prime customers, and we've seen more expensive transactions, all else constant, that has also kind of served our inventory goals over that period. So it is natural that we move in that direction, often premiums go down, but they're applied against a bigger balance.
And so if you look at it in dollar space, that line item is a line item that I think it's an exercise that I would suggest everyone is, go look at the last 12 quarters, graph that out over time and just look at the stability in the absolute dollars, it bounces around inside of a very, very tight range. And I think if you look at it over a longer period than that, as a general matter, it's been upward sloping as we've continued to find fundamental gains and get more efficient as a business and add various loan buyer partners that lower our effective cost of funds. So I think we will continue to utilize these different channels that we've got.
We'll continue to seek out fundamental gains in every part of the finance flows. But I think something that we're very excited by is I think this line item that obviously gets a lot of attention, and there's a lot of numbers that bounce around quarter-to-quarter that people can watch and kind of push through the math. Despite all of that, we think the most important thing is we found a lot of stability there. And it's because the platform that we've built generates a lot of real fundamental value, and then we're able to capture that value, while also passing value back to our customers.

**Operator** (Operator):
The next question comes from Michael Baker with D.A. Davidson.

**Michael Baker** (Analysts):
I just wanted to follow up on the agentic question and understanding the advantage you guys have. But where are you with that now? Is there anything that you need to invest in to take advantage of that? Because if you just sort of -- I know it's very early in this whole process, but if I just did a random sample of going on to some of these bots and say, find me a used car, you guys come up sometimes, but your competitors still come up quite a bit as well. So I'm wondering what you need to do to invest to take advantage of your benefits.

**Ernest Garcia** (Executives):
Sure. Well, I think there's a series of things that probably sit underneath that question. And I think the one that you specified there was the search question. We think we've got to make our cars readily available. We've got to make sure we're pushing out data in all the ways that these different bots can see it. We've got to make sure that we continue to scale and get our information out there. And I think there's lots of things that go into that. But I think the great news is that the bigger we get, the more often we're going to show up in all those different places.
And then I think in terms of changes in the underlying business, there's really not a lot of fundamental things that we need to change. A lot of these tools are tools that we use ourselves, a lot of these tools are tools that are now in the hands of consumers. But because our entire consumer-facing system is deterministic and we can present all of the information for every part of the transaction through an API to any part of our website, any UX that we create on our website or any UX that is available to consumers through whatever bots they have, it's very straightforward.
And then because the underlying processes for even how we do a lot of the operational things that touch customers are also pushed through a wire. There's customer care work, verifications work, title and registration work that is done in a way where we have articulated all the rules, we have made clear exactly what documentation we need, we have business rules and flows where data is pulled off of paper and pushed those flows to get us to answers.
That also means that we're very well positioned to utilize these tools in our business itself because the underlying systems are already there and the underlying rules are already articulated inside of the system that's able to execute against them. So we think in customer-facing ways and in our own managing of the business, we just think there's opportunities to get better everywhere. And I think like everything else we're working on in the business, it's just a matter of prioritization and how well we execute, but the opportunity is all over the place.

**Operator** (Operator):
The next question comes from John Healy with Northcoast Research.

**John Healy** (Analysts):
Congrats on the progress. Ernie, I wanted to ask your thoughts on the FTC dynamics in the quarter. Would love to get your thoughts on how you see the industry kind of evolving from here? Do you think the industry is kind of caught up now in terms of practice? Do you feel like your position is strengthened by this? And do you view this as a benefit more to units or maybe even your ability to push ASP and maybe GPU higher? I'd love to get your thoughts on that topic.

**Ernest Garcia** (Executives):
Sure. So I think -- as a general matter, we think this makes it clear for consumers to compare offers more easily for different cars that they can purchase. And we think that directionally, that benefits us, whether it's the kind of doc fee direction or if it's a direction that has also been issued by the FTC around disclosing any additional products that are required to be purchased with the car in the price of the car. So if a car, for example, has like tint pre-installed or has fabric protection pre-installed or VIN etching or whatever it is pre-installed, that also is supposed to be disclosed as part of the price. So we think that that's helpful because it kind of -- it brings all the information forward in a way that is easier for the customer to see.
In many ways, that's not materially different than a customer that has ChatGPT in their pocket or is using an agent to complete these purchases because they also will kind of bring information forward in similar ways. We think for us, that's great because we think it makes it simpler. It's upfront and easy for customers to see what they're getting into and to understand what the steps are likely to be down the path. And so we think that that's a benefit to us broadly. I think whether it shows up in units or margin, I think, is largely a choice. I think to the extent that we -- the value that we offer is easier to discover for consumers, that will generate value.
And we -- given where we are and given how clear the path is to 13.5%, I think that we would prefer for that value to show up in unit growth, but that requires that we continue to scale the supply chain as quickly as possible. To the extent that we're unable to scale the supply chain as quickly as we'd like, which we would like to be scaling it even faster, then it's likely to show up in margins or somewhere else. But we think as a general matter, it's good for us. And what I'd also say is we feel like the way those economics flow through.
If you were to look at the last 25 or 30 years of automotive retail, generally speaking, what has happened is EBITDA margins or net income margins have been relatively flat over a very long period of time. And basically, vehicle profits have decreased, and F&I profits have increased and the underlying cost structure of dealerships have been in a similar spot relative to the value of the car that's being purchased. And so I think the simplification of that story is just that dealers have a pretty clear cost structures. This is a long-standing, extremely mature industry that has profits that are associated with it, that are profit levels that are pretty well established.
And the particular place where that shows up, it just doesn't matter all that much to the bottom line. So we think to the extent there's more clarity and these other line items are simplified, what that will likely lead to is just increases in the prices that other dealers list their cars for. And it probably won't change the underlying economics very much. So it just aids in price discovery and value understanding for our customers, and we think that's great.

**John Healy** (Analysts):
Very helpful. And I'll take a swing at this. A couple of quarters ago, you told me to have a different question, but I wanted to ask about the franchise dealer model a little bit. Clearly, a lot of things have been written about the success you're having in that vertical. Is that opening doors for other manufacturers and more movement there? Would love to get your thoughts about that expansion opportunity ahead for the company?

**Ernest Garcia** (Executives):
Yes, sure. Thank you. Well, I think -- I apologize to be so cutesy on this, but unfortunately, we don't have a ton more detail to add. I would say we spoke a bit in our opening remarks about our work there with Stellantis dealerships as kind of being an early indication of the platform value that we're building. We think that we have built a platform that has real value to it. We -- the customer offering that we provide to customers is very clear and it's very high quality and it's very clear that customers like it. The economics work. So I think there's a lot of good things there, but it's also very early in the game, and we still got a lot to learn.

**Operator** (Operator):
The next question comes from Sharon Zackfia with William Blair.

**Sharon Zackfia** (Analysts):
As you kind of embark upon the full ADESA conversions or build out, are there any inefficiencies that we should expect to kind of see hit the P&L? And are there any learnings from the kind of mini conversions that you did that will inform kind of how these larger conversions come up to speed?

**Mark Jenkins** (Executives):
Sure. I can hit that. So I do think when we are launching a new facility, I do think that there -- those facilities tend to have higher costs, other things being equal, than facilities that are at a greater level of maturity and scale. Some of that is just basically levering as production facilities are ramping up, levering some of the more fixed components of the cost structure. Part of it can also be related to just getting all the systems and processes up to be operating at the highest level of efficiency. So I do think there can be some effects there. Now I would note that we've been -- we have been integrating facilities and now we'll start integrating fully constructed facilities here over time.
And so I think we -- that's been part of our business for a long time. We did talk a little bit in late 2025 about how, hey, actually adding facilities did have some outsized impacts on costs. That's led to a lot of focus over the course of this year on making sure that we have the right management infrastructure and leadership development infrastructure, making sure we have the right systems, making sure that we have the right day-to-day operational focus on managing costs as the network gets bigger and bigger. There's always more to do there, but I think we've made gains that leave us feeling good about our ability to bring on new sites at a reasonable level of efficiency.

**Sharon Zackfia** (Analysts):
And Mark, I guess I was thinking more about the people side because that seems like it's a tougher part to scale. So have you kind of increase the number of managers in training or mechanics in training or so on as we think about this acceleration in '27?

**Mark Jenkins** (Executives):
Yes, sure. Yes. So on the people side, I think there's a couple of different components. So one is we've talked about the idea of just making the job of managing an inspection and reconditioning center simpler. So that can involve things like better manager reporting that provides more real-time data faster and deeper into the operations of the inspection and reconditioning center. That's something that we've been using AI over the course of this year to rapidly scale systems that give managers better real-time day-to-day operating visibility. In addition, I do think part of it is making sure that we are bringing on the right number of leaders in the inspection and reconditioning centers, giving them grounds for training and getting up to speed before moving on to new facilities. And so that's a place where we have ongoing development and further opportunity. So I think through systems and through making sure we have the right people in place, I think those are some of the key things that will allow us to scale into more facilities at the level of efficiency that we hope to do so.

**Operator** (Operator):
The next question comes from Rajat Gupta with JPMorgan.

**Rajat Gupta** (Analysts):
I wanted to ask about just EBIT margin expansion or just EBIT per unit going forward. I mean, last few quarters, there have been a lot of different type of margin headwinds, fuel costs, benchmark rates, reconditioning issues. Do you think starting fourth quarter, you should be back to margin expansion or EBIT per unit expansion for the company, assuming all else equal, just curious to get your thoughts there? Maybe the last time you're going to guide, so might as well ask, and I have a quick follow-up.

**Ernest Garcia** (Executives):
Sure. I would say earlier in the call, Mark gave examples of areas where we think that there's additional opportunities for leverage. I would put that question back in kind of the context of our goal of 13.5% EBITDA margin leverage, which kind of maps to 12.5% operating income margins. And I think that those different line items that he provided are enough to get us to 12.5% operating income margins. And that leaves all the revenue line items where we still think that there's fundamental gains to be had and all the variable cost line items where we think that there's significant fundamental gains to be had, many of which will be aided and hopefully accelerated by the various AI tools that we've been discussing on the call. So we think the path there is extremely clear.
And then, of course, there's always going to be little things that we face. This quarter, it was pretty significant moves in gas prices and in interest rates, which impacted us to the tune of about $200 per unit. But in the grand scheme of things, those things tend to zero out and we're just kind of steadily on this march. So we think the path is very clear. We're going to continue to move forward. We can see our way very clearly to 13.5%. And we plan to get there slowly but surely continually over time.

**Rajat Gupta** (Analysts):
Got it. And then just on third quarter advertising, a pretty sharp sequential pickup. I know you've given us like some color on like leverage going forward, but are you able to unpack a couple of areas where you invested more this quarter within advertising? Any examples that you could highlight, that would be helpful.

**Ernest Garcia** (Executives):
Sure. I think we continue to test things all over or through many different advertising channels. I don't think there's anything too notable to call out there. As we discussed last quarter, inventory was growing a little slower than we kind of ideally would have liked. We are putting a little bit more into advertising to keep pressure up on the rest of the business. I think we're still a 2% market share holder. So it remains very early in the game and there are areas of opportunity all over the place in marketing, both for more dollars to be spent and then also for us to save significantly in dollars per unit. So I think we'll continue to manage that equation over time, but you can kind of see what we've done over the last several quarters.

**Operator** (Operator):
The next question comes from Jeff Lick with Stephens.

**Jeffrey Lick** (Analysts):
Congrats on an awesome quarter. Either Mark or Ernie, your units were up 39.4%, which is actually an acceleration, whether it's a 1-, 2-, 3-year basis. And that's in an environment where whether it's NADA or Cox, the used car business was actually down and SAAR was down in the quarter as well. I was wondering if you could maybe just force rank the factors as to why you think the acceleration might have happened. In the past, you've talked about better production inventory availability, maybe the FTC has helped financing rate elasticity and then you also mentioned before about broadening the mix on the price bandwidth selling more expensive cars. I'm just curious, if you can maybe force rank why you think your business accelerated in an environment where the market decelerated?

**Ernest Garcia** (Executives):
Sure. I mean I think that there's many micro factors that we could probably point to, but our general premise and kind of belief over a multiyear period is that our rate of growth is constrained by our ability to scale the supply chain. And so we think that is by far and away the biggest driver. Mark talked about us increasing our production growth sequentially quarter-over-quarter pretty significantly, but also even our year-over-year growth increased a little bit sequentially from Q2 to Q3. So we think that that's probably the most important thing. We think that there's clearly additional demand available to us if we can produce the cars in many, many different areas, many different car segments, customer segments, income segments, credit segments, all over the board.
And that's why we think that when we focus in on a particular type of car, we tend to see outsized growth in that particular area. The most notable area where that's occurring, right now, is in prime where we've seen our prime mix really shift up as we've focused on producing more expensive later-model cars as we try to catch up. I think the team is doing a great job, and we're making a lot of progress in recon. But you heard in the detail of Mark's answer, this is definitely an area that we are going to continue to put a lot of effort for the foreseeable future for a very long time.
Operations and complicated physical operations are never easy and scaling them at the speed that we're growing is very, very difficult. And so it requires a ton of focus and attention, and we're continually working hard to come up with new ways to get more efficient there, so we can keep growing that supply chain. Mark is putting a ton of effort in right now, personally spending a ton of time there. So I think that will continue to be an area of focus, but we think that is the biggest driver of our growth. And so we just got to stay dialed in there and keep turning the wheel.

**Jeffrey Lick** (Analysts):
Just a quick follow-up. You mentioned to Rajat's question, advertising more put pressure on the business. And you guys have mentioned the notion of actually trying to generate better production by actually putting pressure on the business. I'm just curious, how do you know when it's too much? And how do you measure like how much more you can go by trying that tactic?

**Ernest Garcia** (Executives):
I think that's obviously a feel, and that's hard to precisely know. And I think you're probably never exactly right. But as a general matter, I think we've got a lot of people at Carvana that are competitive and want to win and want to find ways to make a difference, and they want that pressure on themselves, and we think that that's the best way for us to grow as quickly and effectively as we can and keep making the machine better. So I think, yes, we generally try to make decisions that keep pressure on the business because a lot of times, the areas where you need to focus your attention are revealed by pressure because they are the areas that struggle first. And if you aren't applying that pressure, you don't find those areas that you need to improve to get better. And then once you improve those areas, you move on to the next area that you need to improve. And as you continually do that, you just get a more and more efficient machine. So we do try to make sure that we are keeping pressure up. We would like to think we do a pretty good job of it. I think that's definitely an art, not a science.

**Operator** (Operator):
The next question comes from Michael McGovern with Bank of America.

**Michael McGovern** (Analysts):
On agentic risk, on the financing side of the business, could agents hypothetically drive higher competition proactively searching for lower rates, either at competitors or third-party financing options? And how much does your moat in financing help with that risk going forward?

**Ernest Garcia** (Executives):
Sure. That's a -- there's a lot to that question. So let me try to swing at that maybe a couple of different ways. I think first, the frame is a very reasonable frame. As people have more information in their pocket and the ability to take action in their pocket, it makes everything kind of easier and therefore, price discovery is easier along the lines of all the things that we discussed before. And so I think in kind of like a comparative static, what changes given the introduction of this technology, it's reasonable to assume there will be things like higher prepayments.
And then what exactly does that mean? So I think that is -- that's not a crazy thought direction. Approaching the problem from a different side, financing -- and this is kind of bigger than Carvana. We'll talk about like financing in general and then we can zoom into Carvana what that means. Financing in general is very clearly a value-added function in the economy. It's something that is important and necessary. And I think if you look at finance companies that provide consumer financing to consumers, maybe banks is a good example, and there are others as well. These aren't companies that are earning excessively high profits. They are generally companies that are earning kind of pretty reasonable profits relative to the work that they do.
And the reason I say that is because I think that when some of these things are taken to their extreme, like if you think of financing as like an insurance business where you originate a pool of customers and some get better and some get worse, if all the customers get better instantly refinance and you're left only with the customers that got worse, they basically have like a premium that was the average of the expectation, the finance business basically just doesn't work. It just kind of like wouldn't function. So there will be market evolutions to resolve those sorts of things.
In other markets, those have taken the form of upfront fees or prepayment fees or whatever it could be. So what I would say is, I think if you look at what happens in a vacuum, I think you can arrive at one conclusion. If you take into account the fact that these things exist in a system and they exist in a market and there's value being provided, I think that it is unclear what the sum of all of the market evolutions will be, but it is unlikely to be as dramatic as the comparative static kind of approach might cause you to think. And then as we zoom into Carvana in particular, I think Carvana has a number of advantages versus 2 horizontally stacked businesses that make our system more efficient.
They allow us to build better models and to price more effectively and to avoid certain types of risks that emerge through imperfect alignment of incentives between 2 stacked horizontal businesses. And we would expect that to remain the same. So I think we'll see how all this evolves over time. That will be complicated, and it's obviously a thing that's going to get a ton of attention. But I do think it's useful to take a step back sometimes and remember that these things exist in the market, and there are generally many moves that occur.

**Michael McGovern** (Analysts):
Got it. That's super helpful. And then maybe just one more quick one for Mark. I was curious the note on 2027 reporting, could you speak to kind of why now is the right time for that change, just focusing more on GAAP earnings than non-GAAP earnings, maybe focusing more on GAAP operating income than EBITDA, for example?

**Mark Jenkins** (Executives):
Sure. Yes. So I think it's a natural step in our evolution as a company. I think adjusted EBITDA has been an important metric for tracking our progress over the past many years. I think the -- as we become more profitable on a GAAP basis, I think the value of adjusted EBITDA goes down. And that's why I think when we look out at the world, some of the biggest and most successful technology companies out there, they're not reporting adjusted EBITDA. They're focused on operating income, they're focused on net income. And we think that's just a natural evolution for us as we seek to really grow this business into a very large and very profitable one.

**Operator** (Operator):
The next question comes from Brian Nagel with Oppenheimer.

**Brian Nagel** (Analysts):
Congrats, great quarter. So my question is -- look, it may not be a fair one. But clearly, as we all know, you operate in a very fragmented space, and you've been performing remarkably well. But you do have what I view as a significant or a larger competitor out there now that's starting to show much better growth, still nowhere as near to what Carvana is putting up. The question I want to ask is as you're seeing this dynamic change, are you -- is there more -- are you seeing anything in your business that you have a stronger competitor now reemerging?

**Ernest Garcia** (Executives):
I mean, I would say, and we'll say this from our perspective, we're approximately a 2% market share holder. I think for a long time, we've been the second largest seller of used cars in the country. I think we're knocking on the door of becoming the largest. And so I think when we evaluate others in the market, they are going to be similar in size to us or smaller. And what we've historically seen is it's very hard for us to tease out the impacts of any of those individual players in our results. So we are focused on delivering the best experience we possibly can, making our business more efficient, making everything in the business just function better.
And we think that that's been our focus since day one 14 years ago, and that will continue to be our focus. And then we think that a lot of the things that are emerging in the world around us, generally technology rewards scale, and there's been a lot of technological evolution recently. We're excited by that. And we think it, in many ways, provides a tailwind for us over time. So I think we have not seen anything in particular from any given competitors that we believe has had any notable impact on our results.

**Brian Nagel** (Analysts):
That's very helpful. Then I have a follow-up question. I think someone else asked about the changes the FTC have made in these companies to level the playing field changes. So the question I want to ask is, look, Carvana has been on the right side of this for a while with these fees. Do you believe though now with these FTC changes, that has been an incremental driver of your business? And if so, how should we think about the duration of that? Is it a 1-year type phenomenon? Or is this something that goes on for a while?

**Ernest Garcia** (Executives):
I think it's very hard to massage out in the results. We clearly think it's directionally better for us. We'll see what the overall impacts are over time. But I would take that opportunity to make a slightly bigger point. I think you graciously use the terminology, we've been on the right side of this for a while, so I appreciate that characterization. But what I would say is I think doc fees are a great example of the type of innovation that can occur in markets that is not fundamental. It's not a make the pie bigger innovation. It's a presentation innovation.
And that is the type of innovation that we think is less likely to be successful in a world where people have a lot of intelligence in their pockets. And so something that I had my personal agent do is go through Carvana conference calls and all the Q&A where Mark talks too fast and look and see how many times we said fundamental gains over the last several years. And we said fundamental gains 350 times over the last several years in our various communications. And to me, what excites me about that is that very, very clearly shows you where our head is.
That's why we've made choices like not having doc fees and trying to make things as simple as we possibly can because we put our effort into trying to build solutions that are fundamentally better and that generate more pie. They don't just kind of shift pie around on the plate. So this is an example where not all innovation in the market was pointed in that same direction, but we think that the tools that are emerging and in this case, this FTC directive, they all point in the direction of rewarding fundamental progress, and we're excited about that.

**Operator** (Operator):
The next question comes from Ron Josey with Citi.

**Ronald Josey** (Analysts):
Ernie, we'll see if you can use fundamental gains again here. I wanted to ask about inventory overall. I think it was up around 30% in the quarter. Last quarter, we just talked about the importance to drive and grow more inventory and what that can do to overall conversion rate. So talk to us more about where we are in inventory. Are we at a good mix in terms of what you believe is needed to attract, call it, the higher earners or whatever it is? And then how that's driving conversion rates? That's question one on inventory.
And then, Mark, I want to get back to the advertising comment. With Net Promoter Scores up 9 points overall, just how does that change Carvana's view on growth? Meaning, does that mean we move significantly forward on advertising spend to raise awareness, drive greater conversion rates, et cetera?

**Ernest Garcia** (Executives):
Sure. I'll give a quick high-level answer on inventory. I think, again, to reiterate, we think the team has done a great job. We've made progress in building more cars. We would certainly like to make faster progress, and we're working hard to do that. If we could press the button and have many, many, many thousands of additional cars on Carvana, we would instantaneously very happily convert cash to more reconditioned cars. But that's a process that requires a ton of time and energy. And so we're doing the work to try to do as quickly as we can. In the quarter, we did outproduce sales by a little bit. So that's definitely progress we're excited about, but there's a lot more wood to chop there.

**Mark Jenkins** (Executives):
Great. Yes. And then on the advertising question, I actually think it's useful to just take a step back and talk about our 3-part growth algorithm. So we've been talking about this, I think, over the past couple of years, but there's really 3 drivers of our long-term growth. One is continuously improving the customer offering. That just means making simpler, faster, more informative, seamless experiences for our customers. And that's something that we have focused on and plan to continue to focus on, but just making the customer offering better is a big part of our long-term growth story.
I think second is increasing awareness, understanding and trust. That's really the pillar where advertising comes in. We think we're relatively early still in our long-term journey of telling our story to customers and having them really understand all the things that Carvana brings to the table. I think we've got a long growth way -- growth runway in front of us. And so investing in advertising and telling our story is definitely a place we expect to continue to invest.
Last, increasing selection and other benefits of scale, that links back to your first question, where certainly, we want to continue to grow selection, add more inventory pools, drive faster delivery times and get those benefits as part of the long-term growth algorithm. So those are the 3 big areas. Advertising plays a key role in area #2, and we do expect to continue investing in telling our story.

**Operator** (Operator):
This concludes our question-and-answer session. I'd like to turn the conference back over to Ernie Garcia for any closing remarks. Please go ahead.

**Ernest Garcia** (Executives):
Thanks. Thanks, everyone, for joining the call, and thanks again to the Carvana team. Another awesome quarter. Please walk around and give each other high fives. This is another great one, and then let's come back tomorrow and do it again. Thanks, everyone.

**Operator** (Operator):
The conference has now concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CVNA_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：CFO 給 2026 全年調整後 EBITDA 區間（附帶「環境維持穩定」前提）（原話："adjusted EBITDA of $2.7 billion to $3.0 billion"）
- 2026-07-29｜CFO｜guidance：CFO 預期 Q3 零售銷量較 Q2 季增（原話："a sequential increase in retail units sold in Q3"）
- 2026-07-29｜CFO｜guidance：CFO 說 Q3 營收成長將與零售銷量成長較一致（總額法認列的同比影響自 Q3 消失）（原話："revenue growth to be more in line with retail unit growth"）
- 2026-07-29｜CFO｜guidance：CFO 預期 Q3 廣告費用金額增加（原話："We expect an increase in advertising expense dollars in Q3."）
- 2026-07-29｜CFO｜guidance：CFO 解釋今年 EBITDA 區間的給法與前兩年相同，下半年才給具體 EBITDA 護欄（原話："same style of guidance that we've applied the last 3 years"）
- 2026-07-29｜CFO｜margin：Q2 調整後 EBITDA 利潤率 10.4%，年減（CFO 歸因於總額法認列使每台零售營收上升）（原話："Adjusted EBITDA margin was 10.4%, a decrease from 12.4%"）
- 2026-07-29｜CFO｜margin：營收成長高於銷量成長的原因之一：向大型零售市集夥伴取得之部分車輛改採總額認列（原話："traditional gross revenue treatment for certain vehicles"）
- 2026-07-29｜CFO｜margin：非 GAAP 零售 GPU 年減 $105，主因是對比去年約 $100 關稅相關利益（原話："Non-GAAP retail GPU decreased by $105"）
- 2026-07-29｜CFO｜margin：非 GAAP 批發 GPU 年減 $158，CFO 歸因於零售銷量成長快於批發毛利（原話："Non-GAAP wholesale GPU decreased by $158"）
- 2026-07-29｜CFO｜margin：非 GAAP 其他 GPU 年減 $192，CFO 提到讓利給客戶降低利率與基準利率上升（原話："Non-GAAP other GPU decreased by $192"）
- 2026-07-29｜CEO｜margin：CEO 拆解其他 GPU：讓利約 100bp 利率，單純算應降約 $500，實際只降約 $200，差額為基本面增益（原話："give or take, $300 of fundamental gains in there"）
- 2026-07-29｜CFO｜margin：CFO 說 Q2 非 GAAP SG&A 每台零售單位下降 $157（管理費用 −$272、營運費用 +$88）（原話："$157 reduction in non-GAAP SG&A expense per retail unit"）
- 2026-07-29｜CEO｜margin：CEO 拆解每台 EBITDA 年減約 $300 的原因之一：油價上升的成本估計（原話："That probably cost us something on the order of $75"）
- 2026-07-29｜CEO｜margin：CEO 指出去年同期有約 $100 的關稅利益（影響每台 EBITDA 年比）（原話："Last year, we had a tariff benefit that was around $100."）
- 2026-07-29｜CFO｜margin：CFO 稱仍看到顯著的 SG&A 規模槓桿空間（原話："opportunities for significant SG&A expense leverage"）
- 2026-07-29｜CEO｜margin：CEO 說明 FTC 要求經銷商報價含文件費等後，Carvana 定價演算法跟隨市場，造成零售 GPU 出現超額收益（原話："the FTC put out guidance to all dealers"）
- 2026-07-29｜CEO｜commitment：CEO 說基本面增益將隨時間回饋給客戶，作為邁向 3 百萬台／13.5% 的路徑（原話："we've elected to pass those back over time"）
- 2026-07-29｜CEO｜commitment：CEO 重申中期目標：2030–2035 年每年賣 300 萬台、調整後 EBITDA 利潤率 13.5%（原話："3 million cars per year at 13.5% adjusted EBITDA margin"）
- 2026-07-29｜CEO｜commitment：CEO 表示管理層有信心庫存成長會追上銷售並可能超越（原話："we're confident they'll catch up and hopefully surpass it"）
- 2026-07-29｜CEO｜commitment：CEO 說新零件工具（Roll Call、Leader Hub）尚未全面上線，將在未來數季推出（原話："we'll be rolling it out over the coming quarters"）
- 2026-07-29｜CEO｜risk：CEO 承認庫存成長落後銷售，是對業務的逆風（原話："inventory has undergrown sales over the last several months"）
- 2026-07-29｜CEO｜risk：CEO 說庫存偏低影響轉換率，近期用行銷費用填補（原話："Inventory is a little lighter relative to where we wish"）
- 2026-07-29｜CEO｜risk：CEO 承認對客戶讓利利率在庫存吃緊下，可能未在成長上獲得完整回報（原話："we probably didn't get fully paid for it"）
- 2026-07-29｜CFO｜risk：CFO 的展望以環境穩定為前提（原話："as long as the environment remains stable"）
- 2026-07-29｜CEO｜product：CEO 說明庫存計畫三步驟的第三步：回到較傳統的車齡／里程組合（原話："we plan now to shift to cars that are closer to our"）
- 2026-07-29｜CEO｜product：CEO 說明偏向較新較貴車款的庫存組合轉變並非結構性（原話："So I would say definitely not structural."）
- 2026-07-29｜CEO｜product：CEO 以客服成本逐年下降說明 AI／網站自助的效果，今年再降 10%（原話："This year, we went down an additional 10% year-over-year."）
- 2026-07-29｜CEO｜product：CEO 談新車（新經銷據點）業務：目前有獲利，但不願多提細節（原話："New cars are profitable for us today."）
- 2026-07-29｜CEO｜customer：CEO 說年收入逾 10 萬美元客群銷售年增逾 60%（原話："customers with over $100,000 of income"）
- 2026-07-29｜CEO｜customer：CEO 解釋區域數據：庫存增 57% 的兩區銷售成長 54%（庫存與銷售相關）（原話："In those markets, sales grew in the second quarter by 54%."）
- 2026-07-29｜CFO｜customer：CFO 提供 Q2 零售銷量與年增率（原話："Retail units sold totaled 197,325 in Q2, an increase of 38%"）
- 2026-07-29｜CFO｜competition：CFO 對比產業背景：產業年減約 4 個百分點，Carvana 零售銷量成長 38%（原話："the industry is down, call it, on the order of 4 points"）
- 2026-07-29｜CEO｜competition：CEO 談護城河：規模建立後，其他人不願跨越（原話："a big moat behind us that nobody else wants to run across"）
- 2026-07-29｜CFO｜capital_allocation：CFO 稱淨負債對近 12 個月調整後 EBITDA 降至 1.0x（原話："net debt to trailing 12-month adjusted EBITDA ratio to 1.0x"）
- 2026-07-29｜CFO｜capital_allocation：CFO 答資本回報提問：現金首要用途是投資業務、取得回報，未談股東回報（原話："investing in the business and generating returns"）
- 2026-07-29｜CFO｜capital_allocation：CFO 提供營運資產報酬率：近 12 個月營業利益約 $2.2B，淨營運資產約 $7.5B（原話："on the order of 30% operating return on net operating assets"）

### 問答異常語氣（迴避／改口／保留）
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Rajat Gupta（JPMorgan）：下半年 EBITDA 指引暗示較上半年下滑，為何如此保守、是否遺漏什麼｜答法：CEO 說「stick with guidance」，不解釋上下半年動態，改談執行力與機器模型
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Joseph Spak（UBS）：下半年獲利與上半年接近，是基期還是成本因素｜答法：CEO 同樣回「stick with our guidance」，未回答基期或成本拆分，轉向執行
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Sharon Zackfia（William Blair）：Q3 GPU 逐季降幅是否收斂｜答法：CEO 拒絕逐項 GPU 說明，僅稱季節性可能與過去相似
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Jeff Lick（Stephens）：上季提到的 GPU $200–300 逆風是否未如預期發生｜答法：CEO 不確認或否認該 $200–300，重申整體指引，改談庫存不足造成轉換率下降
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：John Babcock（Barclays）：7 月至今 GPU 與成本（油價、整備）概況｜答法：CFO 只指向全年展望，不提供 6 月到 7 月的細節
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Joseph Spak（UBS）：新車經銷據點是否已開始幫助二手車庫存｜答法：CEO 說「早期」、不給可評論的內容，只提及 NPS 高
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Rajat Gupta（JPMorgan）：每台 EBITDA 連續三季下滑，何時回到成長（年底或 2027）｜答法：CEO 未給時間點，拆解年比因素（關稅、油價、基準利率）後轉談庫存成長與執行

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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
