你是 stock-analyst **v20 判斷 agent**，標的 MNST（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MNST","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MNST_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MNST_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":2563.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"MNST 8-K Ex.99-1 新聞稿（SEC EDGAR）"}},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income","value":748.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"MNST 8-K Ex.99-1 新聞稿"}},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":718.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"MNST 8-K Ex.99-1 新聞稿"}},{"id":"f_kpi3_gaap_gross_margin","label":"GAAP gross margin","value":54.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"MNST 8-K Ex.99-1 新聞稿／10-Q"}},{"id":"f_kpi4_diluted_eps_gaap_non_gaa","label":"Diluted EPS (GAAP / Non-GAAP)","value":0.29,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"MNST 8-K Ex.99-1 新聞稿"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mnst_gross_margin_pct","label":"MNST 毛利率","value":55.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mnst_operating_margin_pct","label":"MNST 營業利益率","value":29.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mnst_fcf_margin_pct","label":"MNST FCF 利潤率","value":22.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ko_gross_margin_pct","label":"KO 毛利率","value":62.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ko_operating_margin_pct","label":"KO 營業利益率","value":32.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ko_fcf_margin_pct","label":"KO FCF 利潤率","value":27.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pep_gross_margin_pct","label":"PEP 毛利率","value":54.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pep_operating_margin_pct","label":"PEP 營業利益率","value":15.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pep_fcf_margin_pct","label":"PEP FCF 利潤率","value":10.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_celh_gross_margin_pct","label":"CELH 毛利率","value":47.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_celh_operating_margin_pct","label":"CELH 營業利益率","value":17.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_celh_fcf_margin_pct","label":"CELH FCF 利潤率","value":6.09,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kdp_gross_margin_pct","label":"KDP 毛利率","value":48.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kdp_operating_margin_pct","label":"KDP 營業利益率","value":14.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kdp_fcf_margin_pct","label":"KDP FCF 利潤率","value":9.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":4.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"新聞稿 SBC $30.4M ÷ GAAP 營業利益 $718.7M 換算"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":45.72,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":5.97,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":48.83,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.15 → 1.15）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.31 → 1.31）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.48 → 1.48）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.15,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.31,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":1.48,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.15 → 1.15（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":41.56,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝67.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":67.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":9.34,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":8.96,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":39.76,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.15，分子＝快照價 45.72","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-3614.19,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 90.06、現金 3704.25（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1957.51,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":85883.25,"period":"2026-11-08","unit":"USD m","basis":"市值 89497.44 ＋ 淨負債 -3614.19","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":9837.64,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":10764.4,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":8.73,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 45.72 / W52 42.24 / W104 35.87 / W250 29.8 / W250 13週斜率 1.27%"},{"id":"f_ma_w52","label":"52 週均線","value":42.24,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":35.87,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":29.8,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.27,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 自述持續面對能量飲料、能量shot、啤酒及 beyond beer 類別的新進入者；功能性飲料業者（BODYARMOR、Prime、Starbucks 等）加入補充成分搶位，公司認為其成分含量較低、定位不同。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"We have experienced and continue to experience competition from new entrants in the energy drink, energy shot, beer and beyond beer categories.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"競爭對手整併與配銷結盟：KDP 配銷 C4、Bloom 並同意收購 GHOST；Celsius 收購 Alani Nu；PepsiCo 2022 年與 Celsius 簽長期配銷協議。","source":"SEC EDGAR 10-K FY2025 Item 1 / Item 1A","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"KDP, which distributes C4 and Bloom, entered into a long-term sales and distribution agreement with Black Rifle Coffee Company as well as a definitive agreement to acquire GHOST Lifestyle LLC and GHOST Beverages LLC. In addition, Celsius Holdings, Inc. (“CELSIUS”) acquired Alani Nutrition LLC (“Alani Nu”).","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"公司風險因子承認競爭壓力可能導致價格侵蝕與市占下滑，並無法保證維持現有市占。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"Competitive pressures in the energy drink category could impact our revenues, cause price erosion and/or lower our market share, any of which could have a material adverse effect on our business and results of operations.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Monster 投資人簡報（8-K 附件）引 Nielsen 美國能量飲料金額份額：Red Bull、Celsius、Alani Nu 等對手份額。","source":"SEC EDGAR 8-K Ex.99.1 (2025)","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465925117647/tm2532419d1_ex99-1.htm","excerpt":"40 JAN 24 FEB 24 MAR 24 APR 24 MAY 24 JUN 24 JUL 24 AUG 24 SEP 24 OCT 24 NOV 24 DEC 24 JAN 25 FEB 25 MAR 25 APR 25 MAY 25 JUN 25 JUL 25 AUG 25 SEP 25 OCT 25 MEC MONSTER RED BULL CELSIUS ALANI NU GHOST C4 ROCKSTAR Source: Nielsen Total US xAOC + Conv TNA Energy SHARE TRENDS TOTAL U.S.","as_of":"2025-11-06","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2026 Q3 10-Q：Coca-Cola Europacific Partners 約占淨銷售17%（單季），為最大客戶；Coca-Cola Consolidated 約9%","source":"Monster Beverage 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0000865752/000110465926123503/mnst-20260930x10q.htm","excerpt":"Coca-Cola Europacific Partners accounted for approximately 17% of the Company’s net sales for both the three-months ended September 30, 2026 and 2025.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：Coca-Cola Europacific Partners 占淨銷售約 15%（2025）、14%（2024）、13%（2023）；Coca-Cola Consolidated 各年約 10%。","source":"Monster Beverage FY2025 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"Coca-Cola Europacific Partners accounted for approximately 15%, 14% and 13% of our net sales for the years ended December 31, 2025, 2024 and 2023, respectively.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Q3 2025 10-Q：Coca-Cola Consolidated 前九個月約 10%，Reyes Holdings 約 9%；美國與國際全服務裝瓶商／經銷商各占當季 44%。","source":"Monster Beverage Form 10-Q (Sep 30, 2025)","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465925107944/mnst-20250930x10q.htm","excerpt":"Reyes Holdings, LLC accounted for approximately 9% of the Company's net sales for both the nine-months ended September 30, 2025 and 2024.","as_of":"2025-11-06","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"S&P 於 2025 年 11 月維持 Coca-Cola Consolidated BBB+，展望由穩定調為負面（買回 24 億美元股票後）；2026 年未查到評等下調。","source":"investing.com 報導 S&P 展望調整","url":"https://ng.investing.com/news/stock-market-news/cocacola-consolidated-outlook-revised-to-negative-by-sp-global-93CH-2211279","excerpt":null,"as_of":"2025-11-20","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"CCEP FY2025 20-F：Moody's A3、Fitch A-，2026 年 3 月有 Moody's 升評至 A3 的報導；未見下調。","source":"Coca-Cola Europacific Partners FY2025 Form 20-F","url":"https://www.sec.gov/Archives/edgar/data/1650107/000165010726000029/cce-20251231.htm","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"美國能量飲料品類 2025 年零售額 269 億美元，五年來高個位數成長（Monster 主管所述）","source":"Nasdaq/Zacks: Energy Drinks Drive Monster Beverage Growth: Can It Continue?","url":"https://www.nasdaq.com/articles/energy-drinks-drive-monster-beverage-growth-can-it-continue","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Celsius 組合（含 Alani Nu）Q3 2026 占美國 RTD 能量飲料金額份額約 20.7%，貢獻無糖能量品類 7.73 億美元成長的約 28%","source":"Pulse 2.0: Celsius Holdings: Brands Drive 30% Of Zero-Sugar Energy Category Growth","url":"https://pulse2.com/celsius-holdings-brands-drive-30-of-zero-sugar-energy-category-growth-as-portfolio-sales-jump-31/","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：公司僅列一般例行訴訟，未列反壟斷調查；管理層認為整體不致對財務有重大不利影響，2025 年底或有損失準備 3,620 萬美元（2024 年 1,680 萬）。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"Although it is not possible to predict the ultimate outcome of such litigation, based on the facts known to the Company, management believes that such litigation in aggregate will likely not have a material adverse effect on the Company’s financial position or results of operations.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"歐盟執委會對 Red Bull 展開競爭調查（限制競爭對手大於 250ml 產品），Monster 表示支持調查、自稱為 Red Bull 反競爭手法的對象。","source":"Reuters via checkout.ie / bluewin","url":"https://www.bluewin.ch/en/news/eu-initiates-competition-proceedings-against-red-bull-2961423.html","excerpt":null,"as_of":"2025-11-13","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"英國政府確認 16 歲以下高咖啡因能量飲料禁售將自 2027 年 4 月起生效（待國會批准）。","source":"The Drinks Business","url":"https://www.thedrinksbusiness.com/2026/08/monsters-energy-drinks-surge-as-alcohol-sales-fall-15/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 揭露：美國加徵鋼鋁關稅並擴大適用範圍，另對多數進口商品課關稅；額外關稅或他國報復可能推高原料（鋁罐）成本，公司若無法轉嫁將影響獲利。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"After imposing tariffs on steel and aluminum imports, in recent years, the United States has recently increased those tariffs and expanded the scope of their application.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 揭露：美國對全球、中國、加拿大、墨西哥等提出或實施關稅，貿易夥伴可能報復，可能擾亂國際市場並推高成本；海外銷售占 41%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"The threat, implementation, or modification of new U.S. trade restrictions, as well as any retaliatory measures adopted by affected U.S. trading partners, could prove disruptive to the international market in which we operate and may lead to increased costs of raw materials and finished products.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"管理層稱關稅與鋁價影響屬『溫和』，預期成本至少到 2026 年底續小幅上升，可能再調價；搜尋摘要未見針對 MNST 的中國專屬關稅或出口管制事件。","source":"FoodNavigator-USA / Food Dive 報導","url":"https://www.fooddive.com/news/monster-faces-modest-tariff-impact-from-aluminum-costs/806157/","excerpt":"We do not believe, based on our business model, that the current tariffs will have a material impact on the company's operating results.","as_of":"2025-11-06","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"CEO稱2026Q1關稅與鋁價對毛利影響小於1%，預期成本至少到2026年底續升；鋁罐成本部分來自50%鋁關稅與中西部鋁溢價飆升；波斯灣中斷與荷莫茲海峽問題收緊鋁供給","source":"FoodNavigator-USA / BeverageDaily: Monster Beverage Corp may raise prices as aluminum costs surge amid global tensions","url":"https://www.beveragedaily.com/Article/2026/05/08/monster-beverage-corp-weighs-price-hikes-as-aluminum-costs-rise/","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K風險因子：部分代工(co-packing)合約允許代工廠依其自身成本上升調高費用；美國已提高鋼鋁關稅並擴大適用範圍；鋁罐等包材業界曾短缺、可能再發生，公司通常不避險","source":"Monster Beverage FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":null,"as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2026Q1 EMEA營收$586.22M占24.9%、亞太$201.89M占8.6%","source":"Zacks via Finviz: Why Monster Beverage (MNST) International Revenue Trends Deserve Your Attention","url":"https://finviz.com/news/327045/why-monster-beverage-mnst-international-revenue-trends-deserve-your-attention","excerpt":null,"as_of":"2026-05-10","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Monster Q3 2026 合併淨銷售約 $2.56B，年增 16.7%；毛利率 54.7%（去年 55.7%）；配送費用占銷售 4.5%（去年 3.8%）","source":"Monster Beverage 8-K Ex.99.1 (Q3 2026)","url":"https://www.sec.gov/Archives/edgar/data/0000865752/000110465926123387/tm2629095d1_ex99-1.htm","excerpt":null,"as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Monster Energy Drinks 部門前九個月淨銷售 $6.92B，年增 21.8%（前期 $5.68B），公司歸因於 Monster Energy 品牌全球需求增加；Strategic Brands 九個月 $426.8M，年增 19.0%","source":"Monster Beverage 10-Q 期間 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0000865752/000110465926123503/mnst-20260930x10q.htm","excerpt":null,"as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"美國便利商店通路：零售商預期 2026 全年能量飲料銷售雙位數成長，2027 降溫至 7%；Goldman Sachs 數據顯示 Q3 c-store 能量飲料銷售年增 11%","source":"NACS convenience.org 'Sustained Momentum' / CStore Dive","url":"https://convenience.org/stay-current/news/2026/october/9/sustained-momentum","excerpt":null,"as_of":"2026-10-09","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Jefferies 認為 Red Bull 新口味主要從 Celsius、其次從 Monster 取得份額（市佔競爭面）","source":"TipRanks/The Fly: Red Bull's new flavors gaining share from Celsius, Monster says Jefferies","url":"https://www.tipranks.com/news/the-fly/red-bulls-new-flavors-gaining-share-from-celsius-monster-says-jefferies","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 揭露：iced tea、咖啡、果汁、強化水、運動飲料等業者(BODYARMOR、Vitamin Water、CORE、Arizona、Powerade、Prime、Starbucks 等)加入補充成分，主打「功能性/能量」飲料;公司認為其成分含量較低、定位不同。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"a number of companies which market and distribute iced teas, coffees, juice cocktails, enhanced waters and sports drinks in various larger volume packages in glass and plastic bottles (including BODYARMOR, Vitamin Water, CORE, Arizona, Ocean Spray, Powerade, Prime and Starbucks), have added supplement ingredients to their products with a view to marketing their products as “functional” or energy beverages or as having “functional” benefits.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：多數銷售來自能量飲料，預期新進者使競爭持續激烈，可能面臨價格壓力與市占波動。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"Most of our sales are currently derived from our energy drinks. Any decrease in the sales of our Monster Energy® brand and other energy drinks could significantly adversely affect our future revenues and net income.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025：美國所有經銷區與國際絕大部分經銷區已轉到可口可樂體系裝瓶／經銷商；通路轉換已完成，非進行中的新轉變。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"All distribution territories in the United States, and substantially all distribution territories internationally have been transitioned to TCCC network bottlers/distributors.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"毛出貨額客戶組成：美國全服務裝瓶商 45%（2024年46%、2023年47%），國際 43%（41%、40%），俱樂部與電商 8% 持平；未見朝 D2C／訂閱的結構轉移。","source":"SEC EDGAR 10-K FY2025 Item 1 Customers","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"U.S. full service bottlers/distributors 45% ​ 46% ​ 47% International full service bottlers/distributors 43% ​ 41% ​ 40% Club stores and e-commerce retailers 8% ​ 8% ​ 8%","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026年Q2 10-Q：美國以外淨銷售額年增34.6%。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0000865752/000110465926092193/mnst-20260630x10q.htm","excerpt":"Net sales to customers outside the United States were $1.16 billion for the three-months ended June 30, 2026, an increase of approximately $298.9 million, or 34.6% higher than net sales to customers outside of the United States of $864.2 million for the three-months ended June 30, 2025.","as_of":"2026-08-07","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FN2 指出 Monster 不提供正式前瞻 guidance，分析師以自身 EPS 預估為錨；因此無法做共識 vs 公司 guidance 的直接比較。","source":"FN2 Monster Beverage FY2026 Q1","url":"https://fn2.ai/earnings/mnst/2026-q1","excerpt":"Monster Beverage does not provide formal forward guidance.","as_of":"2026-06-15","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Tickergate 彙整 44 位分析師，12 個月平均目標價約 $90.58，區間 $77–$103（資料日期未標，約 2026-06 後）。","source":"Tickergate MNST stock forecast","url":"https://www.tickergate.com/stocks/mnst/stock-forecast","excerpt":"predicts a 12-month average price target of $90.58, with a high of $103.00 and a low of $77.00","as_of":"2026-06-15","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Barchart 報導 24 位分析師共識為 Moderate Buy：12 Strong Buy、1 Moderate Buy、11 Hold；個別目標價有 Morgan Stanley $103（2026-06-01）、Bernstein $95（2026-06-11）。","source":"Barchart: do wall street analysts like monster beverage stock","url":"https://www.barchart.com/story/news/3525200/do-wall-street-analysts-like-monster-beverage-stock","excerpt":"Among the 24 analysts covering MNST stock, the consensus is a \"Moderate Buy.\" That's based on 12 \"Strong Buy\" ratings, one \"Moderate Buy,\" and 11 \"Holds.\"","as_of":"2026-06-15","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026（2026-11 公布）調整後 EPS $0.30 小幅優於共識 $0.2984，營收 $2.56B 優於預估 $2.49B；毛利率 54.7%（去年 55.7%）、營業利益率 28.0%（去年 30.7%），股價財報後下跌。未找到 Q4／全年 guidance 或財報後預估修正。","source":"24/7 Wall St: Monster Beverage Q3 2026 Beat Overshadowed by Margin Slide","url":"https://247wallst.com/cards/monster-beverage-q3-2026-earnings-mnst-01m6ptakhn2emp53phwh351d0r","excerpt":null,"as_of":"2026-11-06","retrieved_at":"20261108","affects":["valuation","thesis.R","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 營收 +16.7% 至 $2.56B，運費配送費用 $116.3M 占 4.5%。","source":"SEC 8-K Ex99.1","url":"https://www.sec.gov/Archives/edgar/data/0000865752/000110465926123387/tm2629095d1_ex99-1.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月10份8-K中僅2份含重大項目（5.07/8.01：股東會表決與回購、7/8 2拆1股票分割），無1.01/2.01併購、4.02重編等項目；FY2025 10-K Item 3 稱訴訟合計預期無重大不利影響，損失或有負債$36.2M（上年$16.8M）。","source":"SEC EDGAR 8-K 申報清單；10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"Although it is not possible to predict the ultimate outcome of such litigation, based on the facts known to the Company, management believes that such litigation in aggregate will likely not have a material adverse effect on the Company’s financial position or results of operations.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-07-08董事會核准2拆1股票分割（100%股票股利），預計8/11以分割後價格交易；屬資本結構事件非併購。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926081842/tm2619964d1_8k.htm","excerpt":"Monster Beverage Corporation (the “Company”) today announced that its Board of Directors has approved and declared a 2-for-1 split of its common stock that will be effected in the form of a 100% stock dividend.","as_of":"2026-07-08","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單無1.01/2.01等併購相關項目，僅2份重大項目為5.07/8.01（回購授權、股票分割）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000865752&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K Item 3：公司常規涉訴（含消費者集體訴訟），管理層預期合計無重大不利影響；或有損失準備$36.2M（2024年$16.8M）。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm","excerpt":"As of December 31, 2025 and 2024, $36.2 million and $16.8 million, respectively, of loss contingencies were included in the Company’s accompanying consolidated balance sheets.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單無Item 4.02（財報不可信賴/重編）項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000865752&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"MNST","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.55,"operating_margin_pct":29.16,"fcf_margin_pct":22.58,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNST","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":62.32,"operating_margin_pct":32.11,"fcf_margin_pct":27.97,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KO","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PEP","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":54.17,"operating_margin_pct":15.32,"fcf_margin_pct":10.66,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PEP","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CELH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.95,"operating_margin_pct":17.5,"fcf_margin_pct":6.09,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CELH","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KDP","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.04,"operating_margin_pct":14.84,"fcf_margin_pct":9.11,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KDP","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MNST"},"financial_history":{"ticker":"MNST","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":6311050000.0,"revenue_yoy_pct":null,"gross_margin_pct":50.3,"operating_margin_pct":25.11,"net_income":1191624000.0,"diluted_eps":0.5575,"free_cash_flow":675546000.0,"fcf_margin_pct":10.7,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":7140027000.0,"revenue_yoy_pct":13.14,"gross_margin_pct":53.14,"operating_margin_pct":27.36,"net_income":1630988000.0,"diluted_eps":0.77,"free_cash_flow":1483029000.0,"fcf_margin_pct":20.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":7492709000.0,"revenue_yoy_pct":4.94,"gross_margin_pct":54.04,"operating_margin_pct":25.76,"net_income":1509048000.0,"diluted_eps":0.81,"free_cash_flow":1622099000.0,"fcf_margin_pct":21.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":8294343000.0,"revenue_yoy_pct":10.7,"gross_margin_pct":55.85,"operating_margin_pct":29.17,"net_income":1905432000.0,"diluted_eps":0.97,"free_cash_flow":1940648000.0,"fcf_margin_pct":23.4,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MNST/MNST_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Monster Beverage Corporation** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Good day, and welcome to the Monster Beverage Corporation Third Quarter 2026 Financial Results Conference Call. [Operator Instructions] Please note, this event is being recorded. I would now like to turn the conference over to Mr. Hilton Schlosberg, CEO. Please go ahead.

**Hilton Schlosberg** (Executives):
Good afternoon, ladies and gentlemen. Thank you for attending this call. I'm Hilton Schlosberg, Vice Chairman and Chief Executive Officer; Also on the call are Tom Kelly, our Chief Financial Officer; Rob Gehring, our CEO of Americas; Guy Carling, our CEO of EMEA & OSP; Mike Rodriguez, our COO; and Emelie Tirre, our Chief Strategy Officer. As many of you know, this will be Rob's last earnings call. I want to thank him and wish him the best in his new role at the Coca-Cola Company. Mark Astrachan, our Senior Vice President of Investor Relations and Corporate Development, will now read our cautionary statement.

**Mark Astrachan** (Executives):
Before we begin, I would like to remind listeners that certain statements made during this call may constitute forward-looking statements within the meaning of Section 27A of the Securities Act of 1933 as amended and Section 21E of the Securities Exchange Act of 1934 as amended and are based on currently available information regarding the expectations of management with respect to revenues, profitability, future business, future events, financial performance and trends. 
Management cautions that these statements are based on our current knowledge and expectations and are subject to certain risks and uncertainties, many of which are outside of the control of the company that may cause actual results to differ materially from the forward-looking statements made during this call. 
Please refer to our filings with the Securities and Exchange Commission, including our most recent annual report on Form 10-K filed on February 27, 2026, and quarterly reports on Form 10-Q, including the section contained therein entitled Risk Factors and Forward-Looking Statements for a discussion on specific risks and uncertainties that may affect our performance. 
The company assumes no obligation to update any forward-looking statements, whether as a result of any new information, future events or otherwise. I would also like to note that an explanation of the non-GAAP measures, which we refer to as adjusted where applicable, mentioned during the course of this call, is provided in the notes in the condensed consolidated statements of income and other information attached to the earnings release dated November 5, 2026.
A copy of this information is also available on our website, www.monsterbevcorp.com in the Financial Information section. Please note regional scanner data is included in an exhibit filed with our 8-K. We point out that certain market statistics that cover single months or 4-week periods may often be materially influenced positively or negatively by promotions or other trading factors during those periods. 
I would now like to hand the call over to Hilton Schlosberg.

**Hilton Schlosberg** (Executives):
Good afternoon, and thank you for joining us. We are pleased to report another quarter of strong financial results and cash generation with net sales once again crossing the $2.5 billion threshold in a single quarter. Net sales increased 16.7% compared to the prior year with solid growth across all geographies, driven by the strength of our core offerings as well as our new product innovations. This is especially evident outside the United States, where net sales increased 28.1% compared to the prior year, reflecting share gains in many of our global markets.
Turning to an update on the energy drink category. The global energy drink category remains healthy with continued robust growth. We believe household penetration continues to increase in the energy drink category driven by functionality and lifestyle positioning, diverse offerings that appeal to an increasingly broad and loyal consumer base and affordable value offerings in addition to premium offerings. All said, we think this serves to recruit new consumers to the category, while driving greater purchase frequency among existing consumers. 
We believe our portfolio of existing recently launched and planned energy drink offerings is well positioned to participate in the growing global energy drink category appealing to a broad range of consumers across geographies, price points, need states and day parts. Our business continues to be supported by strong marketing programs, impactful retail engagement and our solid partnership with the Coca-Cola Company and its global bottling partners. 
In the United States, according to Nielsen, for the recently reported 13-week period through October 24, 2026, sales in dollars in the energy drink category, including energy shots, for all outlets combined, namely convenience, grocery, drug and mass merchandisers, including Amazon and Costco increased by 12.4% versus the same period a year ago. In EMEA, the energy drink category, according to Nielsen for our tracked markets for the recently reported 13-week period, which differ from country to country, grew 14.7% versus the same period last year, FX neutral. 
In APAC, the energy drink category, according to Nielsen, Circana and INTAGE for our tracked channels for the recently reported 13-week period which differ from country to country, grew 11.3% versus the same period last year, FX neutral. In LatAm, the energy drink category according to Nielsen, for our tracked markets for the 3 months ended September 30, 2026, grew 28.3% versus the same period last year, FX neutral. 
Turning now to marketing initiatives. Monster maintained strong momentum in the third quarter with efforts focused on growing our core business, attracting new consumers and increasing household penetration. Similar to last quarter, selling expenses were elevated as we increased spending across a variety of new and existing platforms and partnerships. This included increased investments in social and digital media to support both our existing products and our innovation with the goal of recruiting new energy drink consumers, increasing household penetration and reaching a broader consumer base. 
In the third quarter, Monster Energy's roster of athletes, events and ambassadors showcase the brand on a global stage and scale. In a dominant end to the Motocross World Championship Season, Jeffrey Herlings, won 8 consecutive MXGPs to take his sixth overall title, further cementing his legend status in the sport. In MotoGP, the Monster Energy branded Ducati and the recently signed Aprilia factory racing teams dominated the championship with Marc Marquez winning in Germany, Aragon and San Marino. 
Additionally, Monster Energy riders achieved notable victories in AMA and SMX Motocross. In Formula 1, Lando Norris, equipped in Monster Energy branded suit, helmet and cap won back-to-back victories for the McLaren Mastercard Formula 1 team in the Hungarian and Dutch races. Monster Energy's arrival in the UCI Mountain Bike World Series was sealed with Victory for Max Alran in his home race in Les Gets, France equipped with the Monster Energy helmet. Over 60,000 fans lined his descent in a result that transcended sports and resonated across social and mass media with the President of France posting the moment on his social media. 
In Australia, Monster Energy's renewed partnership with the Australian Football League, the AFL culminated in the season ending Grand Final in Melbourne, with 100,000 fans in attendance and millions of watching on TV, Monster Energy pitch-side branding was present for the game winning kick in the last seconds of the game as part of a full stadium LED takeover within Monster Time. In the United States, our successful sponsorships of Morgan Wallen's, Still The Problem tour and UFC continued in the third quarter. Monster Energy athletes also achieved notable victories in X Games New Orleans, the X Games XGL Championship and NASCAR. Lastly, our partnership with the Big 12 conference commenced in the quarter, which includes naming rights for Monster Energy for the conferences, football and basketball regular seasons and a co-branded Monster Energy and Big 12 conference logo that appears on fields and courts and jerseys. There are currently five Big 12 football teams in the AP Top 25 poll. 
Turning to tariffs. During the third quarter of 2026, the impact of tariffs and the increase in the price of aluminum on our operating results was modest. Despite the modest impact on our business in the third quarter, the tariff landscape continues to be complicated and dynamic. For instance, tariffs significantly impacted the Midwest Premium for aluminum, which increased the cost of our aluminum cans. 
We also import some raw materials into the United States, export some raw materials for local markets and export limited quantities of finished goods. We do not believe, based on our business model that the current tariffs will have a material impact on the company's operating results. However, based on current aluminum pricing and the Midwest Premium, we expect a continued modest sequential increase in our aluminum costs through at least the first quarter of 2027. 
We will continue to recognize tariffs on aluminum due to the higher Midwest Premium and continue to implement hedging strategies across the business where possible. 
Turning to our third quarter 2026 financial results. Net sales were $2.56 billion for the 2026 third quarter or 16.7% higher than net sales of $2.20 billion in the 2025 third quarter. Net sales, excluding the Alcohol Brands segment, increased 17.1% in the 2026 third quarter. 
Net changes in foreign currency exchange rates had a favorable impact on net sales for the 2026 third quarter of $8.1 million. Net sales on a foreign currency adjusted basis increased 16.7% in the 2026 third quarter. Net sales, excluding the Alcohol Brands segment on a foreign currency adjusted basis, increased 16.7% in the 2026 third quarter. Excluding the Alcohol Brands segment from our reported results is purely illustrative as it remains part of our ongoing operations. 
Net sales for the company's Monster Energy Drinks segment increased 17.1% to $2.37 billion for the 2026 third  quarter from $2.03 billion for the 2025 third quarter. Net sales on a foreign currency adjusted basis for the Monster Energy Drinks segment increased 16.7% in the 2026 third quarter. Net sales for the company's Strategic Brands segment increased 19.8% to $156.4 million for the 2026 third quarter from $130.5 million in the 2025 third quarter. Net sales on a foreign currency adjusted basis for the Strategic Brands segment increased 19.3% in the 2026 third quarter. 
Net sales for the Alcohol Brands segment decreased 13.6% to $28.5 million for the 2026 third quarter from $33.0 million in the 2025 third quarter. Gross profit as a percentage of net sales for the 2026 third quarter was 54.7% compared with 55.7% in the 2025 third quarter. Adjusted gross profit as a percentage of net sales, excluding the Alcohol Brands segment, for the 2026 third quarter was 54.9% compared with 56.2% in the 2025 third quarter. The decrease in gross profit as a percentage of net sales for the 2026 third quarter was primarily the result of increased aluminum can costs, geographical sales mix and increased freight-in costs partially offset by pricing actions. 
From a gross profit percentage perspective, our pricing actions largely offset higher aluminum can and other input costs. with geographic sales mix significantly driving the lower year-on-year gross margin percentage in the third quarter, again, highlighting our geographical sales mix net sales to customers outside the United States increased to 47% of total net sales in the 2026 third quarter. Distribution expenses for the 2026 third quarter were $116.3 million or 4.5% of net sales compared with $82.6 million or 3.8% of net sales in the 2025 third quarter, largely reflecting higher freight and fuel costs. 
Selling expenses for the 2026 third quarter were $260.1 million, or 10.1% of net sales compared with $214.6 million or 9.8% of net sales in the 2025 third quarter. The increase in selling expenses for the 2026 third quarter was primarily due to increased social, digital media and other marketing expenses, including sponsorships and endorsements in order to reach a broader consumer audience and increase household penetration. 
General and administrative expenses for the 2026 third quarter were $305.7 million or 11.9% of net sales compared with $251.9 million or 11.5% of net sales for the 2025 third quarter. Stock-based compensation was $30.4 million for the third quarter compared to $32.8 million in the 2025 third quarter. General and administrative expenses in the 2026 third quarter included a property and equipment impairment charge of $19.9 million and expenses of $14.7 million related to our digital transformation initiatives. 
Adjusted general and administrative expenses for the 2026 third quarter were $274.4 million compared with $230.9 million in the 2025 third quarter. Adjusted general and administrative expenses as a percentage of net sales, less the Alcohol Brands segment were 10.8% and 10.7% for the 2026 and 2025 third quarters, respectively. 
Operating expenses for the 2026 third quarter were $682 million compared with $549.1 million in the 2025 third quarter. Adjusted operating expenses for the 2026 third quarter were $644.4 million compared with $517.8 million in the 2025 third quarter. Operating income for the 2026 third quarter increased 6.4% to $718.7 million from $675.4 million in the 2025 comparative quarter. Adjusted operating income for the 2026 third quarter increased 7.1% to $748.1 million from $698.4 million in the 2025 third quarter. 
The effective tax rate for the 2026 third quarter was 24.6% and compared with 23.9% in the 2025 third quarter. The increase in the effective tax rate was primarily due to a lower stock-based compensation reduction and an increase in income from higher income tax jurisdictions, partially offset by a lower valuation allowance on foreign tax credit carryforwards. Net income per diluted share for the 2026 third quarter increased 7.8% to $0.29 from $0.27 in the third quarter of 2025. Adjusted net income per diluted share for the 2026 third quarter increased 8.5% to $0.30 from $0.28 in the third quarter of 2025. 
Turning now to the U.S. and North America. Moving to geographic results. We're pleased with our performance in the U.S. and Canada with net sales increasing 9.5% in the 2026 third quarter compared to the 2025 third quarter. Sales growth was broad-based across channels. Our sales performance reflected healthy category growth with solid contribution from our core brand families complemented by innovation and disciplined execution across our organization and bottling partners. 
Our portfolio of Zero Sugar or sugar-free energy drinks remained a significant contributor to U.S. growth. According to Nielsen, the Ultra brand family grew 19% in dollars in the 2026 third quarter compared to the 2025 third quarter. Monster's full sugar portfolio also continued to contribute to sales growth and was led by the Juice Monster family, which increased 21% in dollars compared to the prior year. 
Innovation remained a meaningful contributor to growth in the third quarter complemented by limited time offerings, celebrating America's 250th anniversary across our Ultra, Juice Monster, REIGN and Bang brand families. We were also encouraged by the consumer response to our FLRT Apple Bottoms Up LTO and are planning additional LTOs in 2027 for the brand. LTOs, by the way, mean limited time offers. Additionally, during the quarter, we began shipping our fall innovation to bottlers ahead of the October launches of Java Monster Dubai Chocolate and Monster Energy Vanilla shots in full sugar and Zero Sugar versions. 
Encouragingly, we continue to gain traction in FSOP, which is Food Service On-Premise and are excited to highlight recent collaborations with Carl's Jr. and Tim Hortons. In addition to the previously announced agreement between Marriott and the Coca-Cola Company, which includes Monster. Looking ahead, we will keep investing in an innovation pipeline that serves our core consumers and brings new consumers into our brand families. 
Our robust 2027 new product offerings include planned phase launches starting in January with Monster Ultra Aloha POG, REIGN Dirty Soda, FLRT Blue Snow Cone and the Valentine's Day focused LTO from FLRT. In February, we will introduce Juice Monster Razz Rocket, Monster Energy Candy Apple Red, Monster Rehab Classic Tea, Bang Pineapple Whip and 2 new Monster Killer Brew espresso offerings. In March, we will launch Monster Protein in chocolate and vanilla flavors into the fast-growing ready-to-drink Protein category. 
We will reintroduce NOS Cherried Out in April due to consumer demand and again feature Monster Ultra Red, White & Blue Razz and Juice Monster Strawberry Lemonade as summer LTOs. We will also launch Monster Energy McLaren Zero Sugar as part of a coordinated launch in many markets in the summer of 2027. Lastly, as previously disclosed, we implemented pricing adjustments through frontline price increases and/or reductions in promotional allowances by packaging channel in the United States effective November 1, 2026. 
We anticipate minimal impact on volumes, supported by the category's favorable value proposition and the relatively modest pace of energy drink price increases compared to other NARTD beverages over the past decade. Revenue growth management will remain a key component of our North American strategy. 
Turning to sales International. Outside the United States, net sales to customers increased 28.1% to $1.20 billion or approximately 47% of total net sales in the 2026 third quarter, compared to $937.1 million or approximately 43% of total net sales in the 2025 third quarter. Net sales to customers outside the United States, on a foreign currency adjusted basis, increased 27.2% to $1.19 billion in the 2026 third quarter. 
Now looking at EMEA. Turning to EMEA. Our net sales in the region at 2026 third quarter increased by 24.9% in dollars and increased 25.1% on a currency-neutral basis over the same period in 2025. Gross profit in this region as a percentage of net sales for the 2026 third quarter was 37.2% versus 37.0% in the same period in 2025. We implemented a price increase in certain markets in the EMEA in the 2026 third quarter and are proposing price increases in certain other EMEA markets in the 2026 fourth quarter. 
According to Nielsen, the MEC portfolio of brands gained 190 basis points of value market share across the region in the 2026 third quarter compared to the prior year quarter. The Energy Drink category continues to grow double digits in EMEA with our Monster brands growing more than 60% faster than the category. Notably, the MEC portfolio has gained value share leadership in Great Britain, Egypt and Serbia. 
According to Nielsen for the last reported 13-week period, which vary by country. Our MEC portfolio delivered 39% of the value sales growth of the energy drink category in EMEA. This reflects contributions from both our core offerings and innovation across our brand families. Our portfolio of Zero Sugar or sugar-free SKUs continues to be a significant contributor to growth. 
According to Nielsen for the last 13-week period, the Ultra brand family grew 42% in the third quarter compared to the 2025 third quarter, led by the continued strength of Monster Ultra White. The Zero Sugar segment continues to grow ahead of the Energy Drink category in Europe, where we are the market leader in the Zero Sugar segment of the category with a 46.0% value share according to Nielsen. During the quarter, we delivered well-balanced growth across our portfolio, established full-sugar products, including Monster Green and Juice Monster Mango Loco continued to grow year-on-year. This growth reflects strong execution across markets enabled by close collaboration with our Coca-Cola bottling partners to expand distribution, enhance in-store execution and increase portfolio visibility. 
Innovation was a meaningful driver of performance with the rollout of Juice Monster Viking Berry and Monster Ultra Vice Guava to markets across EMEA. This was complemented by special limited edition offerings of Oscar Piastri in both Monster Energy and Zero Sugar variants. Our affordable portfolio continues to gain momentum, and according to Nielsen, we increased share in Egypt, Morocco and Nigeria. This portfolio remains an important growth driver, broadening consumer access to the category and strengthening our positioning across developing energy drink markets. 
We also continued to gain traction in FSOP in the region with recent collaborations with Subway restaurants in the U.K. and Ireland and Wingstop in France. Turning to Asia Pacific. Net sales in Asia Pacific in the 2026 third quarter increased 12.3% in dollars and 14.9% on a currency-neutral basis over the same period in 2025. Gross profit in this region as a percentage of net sales for the 2026 third quarter was 42.1% versus 40.7% in the same period in 2025. 
Net sales in Japan in the 2026 third quarter decreased 2.0% in dollars and increased 7.8% on a local currency basis. Our Japan results benefited from the previously announced agreement to sell Monster Energy Green and vending machines owned by Coca-Cola Bottles Japan Inc. Depletions were positive, excluding these sales. Net sales in South Korea in the 2026 third quarter decreased 5.1% in dollars and increased 2.0% on a local currency basis as compared to the same quarter in 2025. 
Net sales in China in the 2026 third quarter increased 43.8% in dollars and increased 35.5% on a local currency basis as compared to the same quarter in 2025. Net sales in India in the 2026 third quarter increased 67.2% in dollars and increased 86.5% on a local currency basis as compared to the same quarter in 2025. Results in India in the quarter were impacted by FSSAI, that's the Food Safety and Standards Authority of India, orders issued in June and July of 2026, directing industry members, including Monster, to stop using the description energy drinks on caffeinated beverages. 
Monster challenged orders in the High Court of Delhi, which in October granted interim relief permitting the sale of existing energy drink labeled stock and the use of existing can and bottle inventory. While the matter remains pending, the recent court decision has enabled Monster to resume production and distribution in accordance with the Court's order. We began selling Monster in Mongolia and Cambodia and Bang in Vietnam in the third quarter. 
We remain optimistic about the long-term prospects for our brand in Asia Pacific and the expansion of our affordable brands in China and India. In Oceania, net sales in the 2026 third quarter increased 7.6% in dollars and increased 1.3% on a currency-neutral basis as compared to the same quarter in 2025. Net sales in the quarter were impacted by bottling inventory fluctuations as according to Nielsen, MEC sales increased 22%, and the portfolio gained 150 basis points of value market share across the region compared to the prior year quarter, extending its leadership position. 
Turning now to Latin America and the Caribbean. Net sales in Latin America, including Mexico and the Caribbean, in the 2026 third quarter increased 48.8% in dollars and increased 40.0% on a currency-neutral basis over the same period in 2025. Gross profit in this region as a percentage of net sales was 47.7% for the 2026 third quarter versus 46.8% in the 2025 third quarter. 
Net sales in Brazil in the third quarter increased 70.0% in dollars and increased 60.4% on a local currency basis. Net sales in Mexico increased 20.6% in dollars and increased 10.8% on a local currency basis in the 2026 third quarter. Net sales in Chile in the 2026 third quarter increased 13.5% in dollars and increased 10.2% on a local currency basis. Net sales in Argentina in the 2026 third quarter decreased 6.1% in dollars and increased 13.2% on a local currency basis. 
Turning to Monster Brewing. On Alcohol Brands, net sales for the segment were $28.5 million in the 2026 third quarter, 13.6% lower than the 2025 comparable quarter. With regard to our share repurchase programs during the 2026 third quarter, we repurchased 2.3 million shares of our common stock at an average purchase price of $43.87 per share for total amount of approximately $100 million. 
As of November 4, 2026, approximately $800 million remained available for repurchase under the previously authorized repurchase programs. Turning to October sales. We estimate that October 2026 sales on a non-foreign currency adjusted basis, excluding the Alcohol Brands segment, were approximately 11.6% higher than the comparable October 2025 sales, and 11.1% higher on a non-foreign currency-adjusted basis, including the Alcohol Brands segment. 
We estimate that on a foreign currency adjusted basis, excluding the Alcohol Brands segment, October 2026 sales were approximately 11.2% higher than the comparable October 2025 sales and 10.7% higher on a foreign currency adjusted basis, including the Alcohol Brands segment. October 2026 had 1 fewer selling day than October 2025. 
In this regard, number one, we caution again that sales over a short period are often disproportionately impacted by various factors such as, for example, selling days, days of the week in which holidays fall, timing of new product launches, the timing of price increases and promotions in retail stores, distributor incentives as well as shifts in the timing of production. In some instances, our bottlers are responsible for production and determine their own production schedules. This affects the dates on which we invoice such bottlers.
Furthermore, our bottling and distribution partners maintain inventory levels according to their own internal requirements, which they may alter from time to time for their own business reasons. And number two, we reiterate that sales over a short period such as a single month should not necessarily be imputed to or regarded as indicative of results for a full quarter or any future period. 
In our conclusions -- in conclusion, I'd like to summarize some recent positive points. We are pleased with our strong financial results and cash generation in the third quarter. We had solid sales growth across all of our geographic regions, especially outside the United States in the quarter. We gained share in many markets globally in the quarter. 
We remain focused on the growth of our existing core offerings as well as the continued introduction of product innovations, which remain central to our long-term growth strategy. We continue to expand our sales in non-Nielsen tracked channels, and we are especially pleased with the recently announced collaborations in our FSOP business. The energy drink category continues to grow globally and consumer demand, as measured by scanner data remains strong. 
We believe that household penetration continues to increase in the energy drink category due to product functionality and affordable value proposition and lifestyle positioning. We are also seeing increases in purchase frequencies as well as usage occasions expanding across day parts. We continue to review opportunities for price increases, both domestically and internationally. We will continue our digital transformation in order to modernize our enterprise platforms and strengthen end-to-end business capabilities across commercial, operations and supply chain, including our upgrade to SAP S/4HANA with a planned go-live date of January 1, 2028. 
Lastly, as a reminder, we are hosting an Investor Day in New York City on December 1, and we hope you can join us in person or online. I would now like to open the floor to questions about the quarter.

**Operator** (Operator):
[Operator Instructions] The first question comes from Dara Mohsenian with Morgan Stanley.

**Dara Mohsenian** (Analysts):
So remarkable international revenue growth, obviously, in the quarter, but this business is also really sustained high-growth levels over a longer period of time in the international business. And it's sort of defying gravity that normally CPG businesses slow at much higher revenue levels as you approach $5 billion annually in revenue internationally. So, a, I'd just love a view of what's driving the sustained success. Maybe as you look at the last couple of years, what have been some of the more positive factors that have developed. 
And b, also what I'm really curious about is now that you've had this historical success, what does it unlock going forward, restaurants, I'm sure, take notice or food service in general, right, traditional retailers are probably thinking about a broader product offering, maybe you get bolder with pricing, whatever it may be. But just now that you have these proof points with retail partners, seemingly greater permissibility at the consumer level, what are sort of incremental opportunities going forward as you think about the international business broadly?

**Hilton Schlosberg** (Executives):
So Dara, I don't know where you are. I hear you're in the Far East. So I'm not going to comment on good evening, but welcome to the call. It's actually really interesting if one analyzes this category because we're part of a very large nonalcoholic ready-to-drink category. And so it's not as such that we have a category on its own that's growing. But we have a category that's part of a very substantial category that's growing within that category and growing in itself outside of that category. 
And we get back to the basic premises that we've spoken on previous calls about and that is consumer acceptance continues to grow. The mainstreaming of energy drinks continues to increase. We are seeing increasing household penetration gains. We're moving into multi-packs and you're seeing increasing buy rates because of the fact that we're now in multi-packs. And other drivers of the category include the value proposition. It's -- energy drinks always have been regarded as an affordable luxury. 
The functionality, which is really important, the image, the lifestyle, the innovation, the absolute need for energy from consumers and the usage across more day-part occasions, which is not only true in the U.S., but it's true in EMEA and across the world. And generally, the acceptance among consumers is also increasing and aiding growth and category penetration. 
So just to summarize, our durable attributes are image, value proposition and functionality. So when we look at data that's available to us, and you'll recall that at our last meeting -- in last investor meeting, we put up a chart which was formed by GlobalData where they showed the growth in the category through 2030. Now that's not our data. That's a third-party independent evaluation of the category, and they are seeing growth in the category going forward to 2030 in high single-digit numbers across -- really across the world. 
So I don't know if Guy wants to add anything from an international perspective, particularly EMEA because Guy runs EMEA and OSP. So Guy, I don't know if you've got anything to add.

**Guy Carling** (Executives):
Thank you, Hilton. Thank you, Dara. I think the trends reinforce exactly what Hilton has been saying. The Energy category continues -- it's relatively young compared to other beverage categories. But we -- the category continues to recruit new consumers. In EMEA, in Europe, we see 30% of new consumers coming into the category on an annual basis. We also see rising frequency. More and more drinking the number of products per week. 
It's all underpinned, as Hilton said, by strong functionality, brand image, and then ever-expanding, you kind of raised the question, a range of consumption occasions. The with food opportunity remains huge. We've made progress in America and around the world in FSOP, 31% of consumers in Europe drink energy with food on an ongoing basis. And ultimately, consumption of energy drinks is becoming habitual with more consumers and more people. 
We're well positioned within it. We've got a balance between -- in growth between existing products and innovation. We've got Ultra White, which is over a decade old, growing over 40% and Zero Sugar itself, Zero Sugar Energy grows at twice the rate of full sugar, and Monster delivered 57% of the Zero Sugar growth, as Hilton talked about on the call. And we gained 3 share points within Zero Sugar Energy in Europe. 
And I think lastly, our system partnership gets ever increasingly stronger with the Coca-Cola bottling partners. It increases our availability, our average SKU assortment. It allows scaled innovation launches, expanding Monster led energy zones with key retailers and crucially accelerating our branded cooler footprint and all of this drives our growth as well as the categories.

**Hilton Schlosberg** (Executives):
Thanks, Guy. And as we said earlier, it's Rob's last call, then we have to get some good information from Rob. So Rob, if you could maybe address Dara's point on FSOP and the food service on-premise opportunity.

**Rob Gehring** (Executives):
You bet. Dara, we believe there's an immense opportunity ahead of us with FSOP,and you heard Hilton allude to some of our recent collaborations with retailers. When you look at the frequency at which the U.S. consumer or for any case, any of our geographies, where the consumer is consuming food outside of home on that occasion, we know they constantly are seeking a beverage, and we want energy to be at the forefront of those choices and move from discovery to conversion. 
And so we're very pleased with the recent announcements. We continue to work with the Coca-Cola Company and the partnerships around the world, such as Marriott, and things like that because the consumer is using our beverages more and more outside of the traditional occasions, and we believe it's an incredible opportunity for us to capture growth.

**Operator** (Operator):
The next question comes from Peter Galbo with Bank of America.

**Peter Galbo** (Analysts):
Hilton, I know your favorite topic is to talk about gross margins often in gross profit dollars. But I was wondering if we can maybe ask the question this quarter in a little bit of a different light. Obviously, the international growth has been impressive. And I know that, that comes in at a lower margin percentage. So just curious if there's any way we could kind of discern what the impact from the international growth is in terms of the year-over-year margin pressure just because I think there's so much focus on that number, obviously. And again, if you're growing faster in those regions and the dollars are faster, it may help to just kind of understand what the percentage impact is from international.

**Hilton Schlosberg** (Executives):
Yes. Thanks for that question. I mean, if you look at where we are today, 47% of our growth is international. 47% -- not of our growth, I'm sorry, 47% of our sales is international. Last quarter, same period a year ago, it was 43%. So international is growing as a percentage of our business, which is very encouraging for us because we do see ourselves as an international business today. We're in 160 countries. And we're really proud of the progress that we've made in growing the business on an international footprint. 
So we disclose every quarter, we disclose our margins, our gross margins in every part of the world. So you've got to -- I think I don't have those tools in front of me to answer your question specifically, but you've got the information. You know that we moved from 43% to 47% in this quarter. You also know what the margins were a year ago because we've spoken about them on the call and they are available, and we have the numbers that we gave you today. So -- by region. 
So if there's still a question after this, then maybe you could give us a call and we could talk about it offline. But all the tools are there for you to be able to compute the answer that you're looking for.

**Operator** (Operator):
The next question comes from Kaumil Gajrawala with Jefferies.

**Kaumil Gajrawala** (Analysts):
The last quarter was sort of the beginning of seeing the outcomes of some of the shift in focus to capturing more Gen Z and capturing more of the sort of new energy drink consumers. And so can you just talk about that a little bit more? And how is that process going now that we're a little further along. And I don't know if you have some statistics on how many people have entered the category and how much of them you've been able to get for yourselves?

**Hilton Schlosberg** (Executives):
Yes. So we know that there's an opportunity with female-forward consumers. And FLRT is growing nicely. We spoke about some of the innovation and so we're quite excited about the opportunity through that brand. We're spending a lot of money, as you realize and as we spoke about on social media. And we feel we are reaching the right 18- to 24-year-old consumer. We -- not only are we working on repeat, but we're building a solid base. 
So if -- just been looking at some stats. So household penetration has grown as we spoke earlier, purchase intent has grown and Gen Z household incidence is now at 58%. So we think that what we're doing is hitting the target. We know that there's more to come, but that consumer is very important to us. And we believe we have a broad range of products to be able to address that consumer needs and we'll continue to evaluate as we go forward. 
We've got our protein products that are being launched next year. We have an array of interesting innovation next year. So we believe that we're doing the right things. And we believe that the social media activity that we're doing is generating good results, as indeed are our sponsorships, endorsements. And we're just going to follow on with the strategy that we started because we do think it's working. And we believe that FLRT will grow through LTOs, and we spoke a little bit on the call about the first LTO, which is one for Valentine's Day.

**Operator** (Operator):
The next question comes from Bonnie Herzog with Goldman Sachs.

**Bonnie Herzog** (Analysts):
All right. I actually wanted to go back to gross margins and just maybe hoping for a little more color and maybe phasing expectations moving forward. Should we expect another sequential deceleration for margins in Q4? And then how should we think about phasing next year? Does it make sense to think about 1H being more pressured than the second half, for instance? And I think I understand the headwinds, Hilton, that you've certainly called out, but what about the levers you can pull to help mitigate some of the pressures like whether it's further pricing actions, are they greater versus last year, any more pricing opportunities internationally, et cetera?

**Hilton Schlosberg** (Executives):
So we do have a price adjustment that's going through November 1. We've spoken about that. And I think we -- this whole aluminum context is something that is a headwind to gross margins, generally across all of our territories. And if we just think about it, aluminum has increased -- raw aluminum has increased 36% since a year ago. So those are the numbers that you're dealing with. 
Now yes, we do hedge, and we evaluate hedges in the best way we can. But at the end of the day, aluminum does have an impact. We call it a modest impact, but it does have an impact on margins. And there are other factors, and the biggest factor is this whole geographical mix. Because as we grow internationally, our margins, our gross margins reduce as percentages. And as the previous caller said, it's certainly, as a percentage, yes, but we bank dollars, we don't bank percentages.
So we don't give guidance. It's hard for me to talk about the fourth quarter because we don't give guidance. We -- outside the U.S., if you examine the numbers, you'll see that gross margins increased year-on-year in all 3 geographic regions. So we're doing the very best we can to increase margins internationally and increase pricing internationally. In the U.S., I mentioned that we have a price increase that will take effect from November 1. So given everything that we mentioned on the call, I think it is difficult territory, and I know you want a percentage for your model. But unfortunately, I just can't give it. 
You've got the rudiments of where we are. And as we continue to grow internationally, there will be a drag. And then when we look at EMEA, there's a further drag in EMEA as they expand their portfolio in the various countries in which they operate. Against that, we have efficiencies, which we're always working on efficiencies. That's number one. And number two, with the growth of Zero Sugar products, those products have higher margins than the full-sugar products. So it's really a balance. It's really a mix, and there are pluses and minuses. But at the end of the day, it's not something that we neglect. I mean, we actively are engaged in improving margins. Guy had a price increase in the EMEA in the last 6 months. 
So we are addressing where we can. But I repeat at the end of the day, as we grow internationally, margins percentages are going to be a drag on the overall company gross profit, and that's something as a percentage, and that's something that we all have to live with.

**Operator** (Operator):
Next question comes from Matthew Smith with Stifel.

**Matthew Smith** (Analysts):
I wanted to come back to your commentary on innovation, and we saw that a lot of the 2027 new items at NACS. But 2026 featured a pretty robust lineup of new products into the market. And I wanted to hear your opinion of an evaluation of the phasing of innovation. Do you feel like with that amount of activity, the base products and the innovation products were able to reach their full potential? Or do you think the pacing of innovation stymied some of the lift you could have gotten as these products fall into the base and you anniversary the innovation?

**Hilton Schlosberg** (Executives):
Yes. I think that if you look at our 2027 innovation pipeline, we believe it's robust and that it really compares favorably to the lineup we had in 2026. As -- I think you were at NACS, right? So we presented the innovation slate and the feedback was really positive, not only from the bottlers, but also from our retail customers and our retail partners. 
We have expanded our own innovation program. We're getting to Monster Protein. And I think that as we look at 2027, we're going to do a better phaseout of our innovation. So we really hope that -- and we believe that the bottlers focus will be better than it was in 2026. Maybe we had a little bit too much in 2026, but we regard '27 innovation as quality over quantity. We're bringing back some of the innovation, the America250 innovation, which was very well received as LTOs over the Independence Day. So some of that innovation that we did in '26 will continue to live in '27.

**Operator** (Operator):
The next question comes from Peter Grom with UBS.

**Peter Grom** (Analysts):
So Hilton, you kind of started the call discussing your optimism for the category. And clearly, the performance this year has been impressive. But -- and I know we've talked about international markets to Dara's question earlier, but I'm curious how you see kind of U.S. category growth evolving as you look out next year. I know you don't give guidance, but we have seen some slowing in the data in the U.S. of late. I'm curious what you think is driving that? And just as you think about cycling some tougher comparisons, like how -- what do you think is a realistic growth rate for the industry as you look ahead?

**Hilton Schlosberg** (Executives):
Well, category data is actually starting accelerating, which is interesting. The category is healthy. It's becoming a big category, and it's hard to grow at the same rate as we have achieved historically with a much larger category. But I think what I'd like to do is get some insight on the U.S. from Rob. Rob, If that's okay.

**Rob Gehring** (Executives):
You bet. Thanks for the question. We did see, I would say, a little slowing at the end of the summer versus our traditional trends, but it's bounced back. I mean, even in the most recent weeks, on scanner data, we're looking at is over 15% growth. So it's rebounded nicely. Even though there's been headwinds throughout the year that everyone is speaking about, whether it be NACS or fuel price -- I'm sorry, SNAP or fuel prices, things of that nature. 
We constantly monitor consumer behavior. We've noticed as a lot of different manufacturers have taken retail inflation that the category has been resilient, and we're proud of the ability to grow both price and volume concurrent with the many competitors we have because we do believe in the health of the category. So as the consumer makes choiceful decisions with where they spend their money, we're bullish about the future. We believe in the value that innovation brings to the category. 
And the goal for us is to constantly evaluate our innovation and ensure it's elevating our base. We want to elevate our core brands. So we look at all of those variables and constantly work with our retailers to ensure we're providing the right value proposition that our consumers are seeking.

**Operator** (Operator):
This concludes our question-and-answer session. I would like to turn the conference back over to Hilton Schlosberg for any closing remarks.

**Hilton Schlosberg** (Executives):
Thank you. On behalf of Monster, I'd like to thank everyone for the interest in the company. We're confident in the strength of our brands and the talent of our entire Monster family throughout the world, and I'm excited to be working with them and thank them all for their contributions. We believe in the company and our growth strategy and are committed to innovating, developing and differentiating our brands and expanding the company both at home and abroad. 
We're proud of our relationship with the Coca-Cola system and the opportunity this presents to us. We believe that we are well positioned in the beverage industry and are optimistic about the future of our company. And I'd like to make a special tribute to Rob, who's leaving us to join the Coca-Cola Company in a very senior capacity. And Rob, we wish you all the best. Thank you for everything and look forward to working with you in your future role because we believe that Rob's future role is going to be synergistic to both ourselves and the Coca-Cola Company as we move forward in some critical areas like FSOP and the opportunities that all of that presents to all of us. 
FSOP is also important from a marketing perspective because it gives access and image to our products. So very excited about that. So Rob, thank you for that. And thank you, everyone out there for your attendance. Thank you.

**Operator** (Operator):
The conference has now concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MNST_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Hilton Schlosberg｜guidance：管理層說美國已啟動與夥伴討論，擬於2026年第四季實施選擇性漲價（原話："pricing actions effective during the 2026 fourth quarter"）
- 2026-08-06｜Hilton Schlosberg｜guidance：管理層預期鋁成本至少到2026年底持續溫和環比上升（原話："aluminum costs through at least the end of 2026"）
- 2026-08-06｜Hilton Schlosberg｜guidance：7月銷售（排除酒類、未調匯率）約年增14.3%（原話："approximately 14.3% higher than the comparable"）
- 2026-08-06｜Hilton Schlosberg｜margin：Q2毛利率55.9%，上升來自訂價與產品組合，被鋁罐、地區組合、進貨運費部分抵銷（原話："pricing actions and product sales mix partially offset by"）
- 2026-08-06｜Hilton Schlosberg｜margin：配送費用占比由3.9%升至4.7%，歸因運費與燃料（原話："largely reflecting higher freight and fuel costs"）
- 2026-08-06｜Hilton Schlosberg｜margin：銷售費用占比由9.3%升至10.6%，歸因社群數位等行銷、贊助與代言（原話："increased social, digital media and other marketing"）
- 2026-08-06｜Hilton Schlosberg｜margin：管理層說明國際銷售的毛利率較美國低，並稱重視金額而非百分比（原話："we bank dollars, we don't bank percentages"）
- 2026-08-06｜Hilton Schlosberg｜margin：Q2調整後營業利益年增13.3%，低於淨銷售年增20.2%（為兩個數字的並列陳述）（原話："drive revenue ahead of volume and profit ahead of revenue"）
- 2026-08-06｜Rob Gehring｜margin：管理層對訂價與利潤的目標說法：營收快於銷量、利潤快於營收（原話："a very limited market that we have hedged, but probably not"）
- 2026-08-06｜Hilton Schlosberg｜risk：鋁對沖：管理層承認Midwest premium的對沖可能不足（原話："current tariffs will have a material impact on the company's"）
- 2026-08-06｜Hilton Schlosberg｜risk：管理層稱目前關稅預期不會對營運結果造成重大影響（原話："depletions far exceeded our shipments"）
- 2026-08-06｜Hilton Schlosberg｜risk：南韓Q2銷售因經銷商庫存波動而下滑，出貨遠低於實際銷售（原話："depletions far exceeded our shipments in the quarter"）
- 2026-08-06｜Hilton Schlosberg｜risk：管理層提醒單月銷售不宜視為整季或未來的指標（原話："should not necessarily be imputed to or regarded as"）
- 2026-08-06｜Hilton Schlosberg｜competition：美加Monster品牌家族Q2價值市占增加70個基點（原話："gained 70 basis points of value market share"）
- 2026-08-06｜Hilton Schlosberg｜competition：EMEA旗下品牌貢獻該地區能量飲料品類價值成長的46%（原話："our portfolio delivered 46% of the value sales"）
- 2026-08-06｜Hilton Schlosberg｜competition：歐洲零糖區隔：Monster價值占有率44.5%並為領導者（原話："market leader in the Zero Sugar segment of the category"）
- 2026-08-06｜Rob Gehring｜competition：家戶調查中Monster拉新客的速度約為品類的兩倍（原話："bringing in consumers at twice the rate of the category"）
- 2026-08-06｜Hilton Schlosberg｜product：Ultra Red, White and Blue限量品自5月全國上市占Circana銷售5%（原話："accounted for 5% of sales in Circana"）
- 2026-08-06｜Hilton Schlosberg｜product：今年創新改為分批上市，不同於過去的一次性上市（敘事變化）（原話："staggered launches of our innovation versus onetime launches"）
- 2026-08-06｜Hilton Schlosberg｜product：FLRT：行銷6月才開始，管理層稱言之過早但仍承諾投入（原話："too early to tell, but we remain committed to the brand"）
- 2026-08-06｜Hilton Schlosberg｜product：零糖占品類成長逾75%，管理層稱家戶滲透率尚未見頂（原話："zero sugar accounts for more
than 75% of category growth"）
- 2026-08-06｜Hilton Schlosberg｜customer：Marriott與可口可樂的合作被管理層視為食品服務通路的重大配送機會（原話："open significant distribution opportunities for Monster"）
- 2026-08-06｜Hilton Schlosberg｜customer：管理層稱許多FSOP客戶現在要求供應能量飲料（原話："a lot of FSOP customers now are requiring energy drinks"）
- 2026-08-06｜Hilton Schlosberg｜customer：日本於6月起進入可口可樂裝瓶商持有的自動販賣機（原話："sales commenced in June
and are off to a good start"）
- 2026-08-06｜Hilton Schlosberg｜customer：國際淨銷售Q2年增34.6%，占總銷售約46%（去年同期約41%）（原話："Net sales to customers outside the United States increased"）
- 2026-08-06｜Hilton Schlosberg｜capital_allocation：Q2未回購股票，截至8月5日回購授權剩約9億美元（原話："no shares of the company's common stock were repurchased"）
- 2026-08-06｜Hilton Schlosberg｜capital_allocation：董事會批准1拆2，預計8月11日以拆分後價格交易（原話："approved
and declared a 2-for-1 split of its common stock"）
- 2026-08-06｜Hilton Schlosberg｜capital_allocation：巴西等地加大冷藏櫃投資；管理層稱未來有重大冷櫃投資（原話："we have major
investments going forward with coolers"）
- 2026-08-06｜Hilton Schlosberg｜commitment：SAP S/4HANA升級預計2028年1月1日上線（原話："SAP S/4HANA with a planned go-live date of January 1, 2028"）
- 2026-08-06｜Hilton Schlosberg｜commitment：計畫2026年12月1日在紐約舉辦投資人會議（原話："SAP S/4HANA with a planned go-live date of January 1, 2028"）
- 2026-08-06｜Hilton Schlosberg｜commitment：管理層將於10月NACS展示2027年完整創新時程（原話："host an investor meeting in New York City on December 1"）
- 2026-08-06｜Hilton Schlosberg｜commitment：EMEA歐洲部分市場已漲價，另提議年內在其他市場再漲價（原話："we have a full innovation calendar that we will be"）

### 問答異常語氣（迴避／改口／保留）
- MNST_Q2_2026_Earnings_Call_20260806.md｜問：Kaumil Gajrawala（Jefferies）請求漲價的地點與幅度細節｜答法：Rob Gehring談訂價哲學與目標，未給美國漲價幅度或範圍；Guy Carling僅給EMEA『aggregate low single-digits』，未給細節
- MNST_Q2_2026_Earnings_Call_20260806.md｜問：Kevin Grundy（BNP）問國際成長的可持續性與跑道（市占）｜答法：Guy Carling與Hilton講各地區驅動因素與品類佔比，未直接回答持續性或跑道的量化
- MNST_Q2_2026_Earnings_Call_20260806.md｜問：Bonnie Herzog（Goldman）問每箱配送與銷售費用Q2是否為合理run rate、後續是否下降｜答法：Hilton解釋運費燃料與行銷活動原因，未回答run rate或後續是否下降
- MNST_Q2_2026_Earnings_Call_20260806.md｜問：Chris Carey（Wells Fargo）問無全球大幅漲價下對保護毛利率的信心是否提升｜答法：Hilton談通膨、鋁對沖、國際毛利率較低，未直接回答信心變化，並以『we bank dollars』收尾

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
{"date":"20260518","verdict":"Q1 26 數字爆表(Rev +27%／EPS +29%／國際 +45%／China/India +95%)；新 .5B 回購；但估值已追平 5Y median；PEG 2.44 仍在 🟠 區；現價 .09 貼 BB 上軌(.70)+ 接近 52W 高 .77。Thesis 完整(品質 A／長期信心高／護城河 9/10)但時機不到 → B 觀望。等 PEG <2.0 或 MA 短回測 W52(./股) 再加碼。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"國際擴張持續：EMEA / APAC / LatAm 三 region 加總增長 ≥ 30% 連 2-3 年，國際 mix 從 45% → 55%","columns":{"2Y 驗證點":"2027 國際合計 ≥ 30% YoY；EMEA / APAC / LatAm 三個都不能個別跌至 15% 以下","5Y 驗證點":"2030 國際 mix ≥ 55%；其中 APAC ≥ 25% 的全球 mix","10Y 驗證點":"2035 國際 mix ≥ 65%；中國 + 印度 + 巴西 三個合計 ≥ 25% 全球","具體數字門檻 + 來源":"30% / 55% mix（公司法說 Q1 26 Schlosberg 言論）","漂移觸發條件":"連 2 季 TTM 國際合計 &lt; 25%（季節性過濾 QC-34）"}},{"id":"H2","text":"美國 Monster Energy 主品牌維持 ≥ 10% 美加成長：剔除 Bang/Reign 衰退，主力品牌 不能 falter","columns":{"2Y 驗證點":"2027 美加 Monster Energy 品牌 ≥ 10%","5Y 驗證點":"2030 美加 Monster Energy 品牌 ≥ 8%（成熟區較低但 still positive）","10Y 驗證點":"2035 美加 Monster Energy 品牌 ≥ 5%","具體數字門檻 + 來源":"13.3% Q1 26 美加（Schlosberg Earnings Call 5/8）","漂移觸發條件":"連 2 季 美加 Monster Energy &lt; 8%（核心防線）"}},{"id":"H3","text":"毛利率反彈：Q3-Q4 26 H2 GM 回到 55%+，FY27 全年 GM 56%+（pricing actions 抵銷成本）","columns":{"2Y 驗證點":"FY27 全年 GM ≥ 56%","5Y 驗證點":"FY30 全年 GM ≥ 57%（國際 scale 後 mix 改善）","10Y 驗證點":"FY35 全年 GM ≥ 58%","具體數字門檻 + 來源":"55.8% FY25 GM（Macrotrends Income Statement）","漂移觸發條件":"連 2 季 GM &lt; 54%（結構性質變閾值）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"美國 Celsius/Alani 搶 Monster Energy 主品牌份額（不只搶 Reign/Bang）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Monster Energy 美加 YoY%","警戒閾值":"連 2 季 &lt; 8%"}},{"id":"R2","text":"毛利率結構性下移（國際 mix + 鋁罐 + Midwest premium 持續）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季度 GM YoY 變動","警戒閾值":"連 2 季 GM &lt; 54%"}},{"id":"R3","text":"監管：caffeine 強制標示 / 18+ 限制 / 廣告限制（美國跟進 EU）","columns":{"對應假設":"整體","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"FDA / Congress 動向","警戒閾值":"需 ≥ 50% 機率才砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":87.09,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MNST_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
