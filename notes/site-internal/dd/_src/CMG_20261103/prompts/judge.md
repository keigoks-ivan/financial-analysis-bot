你是 stock-analyst **v20 判斷 agent**，標的 CMG（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CMG","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMG_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMG_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenue_gaap","label":"Total revenue (GAAP)","value":3293.162,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD million；YoY +9.6%（Q3 2025 $3,003.4M）；QoQ -1.65%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm"},"note":"revenue 高於共識（Zacks；具體共識值未取得）"},{"id":"f_kpi1_gaap_operating_income","label":"GAAP operating income","value":451.964,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm"}},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":13.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%（Q3 2025: 15.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm"}},{"id":"f_kpi3_restaurant_level_operati","label":"Restaurant level operating margin (non-GAAP)","value":23.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%（Q3 2025: 24.5%）；公司不揭露 non-GAAP 營業利益率，以此替代","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm"}},{"id":"f_kpi4_adjusted_diluted_eps_non","label":"Adjusted diluted EPS (non-GAAP)","value":0.27,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD（Q3 2025: 0.29）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm"},"note":"Zacks 稱 EPS 低於共識（具體值未取得）"},{"id":"f_kpi5_free_cash_flow_derived","label":"Free cash flow (derived, 非公司揭露)","value":347.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD million；9M OCF 1,922.1 - 9M capex 640.6 再減 H1（OCF 1,332.0 - capex 397.6）自行推算","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm ；https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000063/cmg-20260729xex991.htm"}},{"id":"f_kpi7_guidance_fy2026","label":"Guidance FY2026","value":null,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"comps 低個位數成長；新店 350–370（含國際夥伴 10–15）；約 80% 新店含 Chipotlane；有效稅率 24–26%；Q4 comps 約 +2%（CFO 口徑，來自媒體轉述）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm"},"needs_sonnet":true},{"id":"f_kpi8_guidance_fy2027","label":"Guidance FY2027","value":null,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"北美公司店新開 340–360；北美以外 15–25","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm"},"needs_sonnet":true},{"id":"f_kpi9_comparable_restaurant_sa","label":"Comparable restaurant sales","value":2.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%（客單 +1.3%、交易數 +0.8%）；媒體轉述自新聞稿，共識約 1.5%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"新聞稿 https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm ；彙整 capital.com／NRN（僅輔助）"},"note":"共識約 1.5%（媒體轉述）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cmg_gross_margin_pct","label":"CMG 毛利率","value":23.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmg_operating_margin_pct","label":"CMG 營業利益率","value":14.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmg_fcf_margin_pct","label":"CMG FCF 利潤率","value":11.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mcd_gross_margin_pct","label":"MCD 毛利率","value":57.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mcd_operating_margin_pct","label":"MCD 營業利益率","value":45.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mcd_fcf_margin_pct","label":"MCD FCF 利潤率","value":28.02,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cava_gross_margin_pct","label":"CAVA 毛利率","value":24.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAVA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cava_operating_margin_pct","label":"CAVA 營業利益率","value":7.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAVA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cava_fcf_margin_pct","label":"CAVA FCF 利潤率","value":3.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAVA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wing_gross_margin_pct","label":"WING 毛利率","value":49.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WING.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wing_operating_margin_pct","label":"WING 營業利益率","value":27.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WING.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wing_fcf_margin_pct","label":"WING FCF 利潤率","value":15.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WING.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sbux_gross_margin_pct","label":"SBUX 毛利率","value":21.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SBUX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sbux_operating_margin_pct","label":"SBUX 營業利益率","value":10.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SBUX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sbux_fcf_margin_pct","label":"SBUX FCF 利潤率","value":9.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SBUX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi6_sbc_derived","label":"SBC (derived)","value":31.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD million；占 GAAP 營業利益 7.0%、占營收 0.97%；9M 86.4 - H1 54.5 推算","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm ；https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000063/cmg-20260729xex991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":32.94,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":3.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":61.03,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":1.85,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.08 → 1.1）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.74,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.35 → 1.34）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-1.27,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.57 → 1.55）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.1,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.34,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":1.55,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-2.65,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 1.13 → 1.1（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":30.79,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.28,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.65,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":29.95,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 1.1，分子＝快照價 32.94","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":4696.47,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 5599.03、現金 902.56（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1264.97,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":46364.74,"period":"2026-11-03","unit":"USD m","basis":"市值 41668.27 ＋ 淨負債 4696.47","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":12999.43,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（32 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":14381.87,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（32 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.57,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 32.85 / W52 34.42 / W104 42.38 / W250 41.54 / W250 13週斜率 -0.02%"},{"id":"f_ma_w52","label":"52 週均線","value":34.42,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":42.38,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":41.54,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.02,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：競爭者（含非傳統參與者如雜貨即食餐、餐盒、幽靈廚房、外送平台）同樣主張高品質原料、無人工添加，可能削弱 CMG 差異化。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm","excerpt":"many of our competitors also make claims related to the quality of their ingredients and lack of artificial flavors, colors and preservatives. The use of these claims by competitors, even if such claims are not accurate or comparable, may lessen our differentiation and make it more difficult for us to compete.","as_of":"2026-02-04","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"搜尋摘要：CAVA 2026 Q2 同店銷售 +9%、客流 +5.3%；CMG 2026 Q2 comps +2.2%、交易數 +1%，CAVA 成長快於 CMG（摘要轉述，未取得逐字原文）。","source":"Nasdaq/Zacks 與 QSR Magazine 搜尋摘要","url":"https://www.qsrmagazine.com/story/cava-and-chipotle-take-different-paths-to-traffic-growth/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"CMG 2026 Q3 comps +2.1%、交易數 +0.8%、客單 +1.3%。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000104/cmg-20260930.htm","excerpt":"•Comparable restaurant sales increased 2.1% •Diluted earnings per share was $0.27, a 6.9% decrease from $0.29 Sales Trends. Comparable restaurant sales increased 2.1% for the three months ended September 30, 2026. The increase is attributable to a 1.3% increase in average check and a 0.8% increase in transactions.","as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Bank of America 報告稱餐飲供給擴張快於消費者需求，單位數成長作為估值訊號的可靠度下降；僅 casual dining 單位數下降並維持低位。","source":"BofA State of the Restaurant Industry 2026","url":"https://business.bofa.com/en-us/content/restaurant-industry-report-2022/industry-overview.html","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"一項 2026 年 6 月營運商調查：2025 年僅 14% 回報客流成長超過 1.5%，71% 預期 2026 年客流大致持平。","source":"Coleman Report, Main Street Monday: Restaurant Operators Prioritize Catering, M&A, and New Unit Growth for 2026","url":"https://colemanreport.com/main-street-monday-restaurant-operators-prioritize-catering-ma-and-new-unit-growth-for-2026","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"CMG 2026 Q3 同店銷售 +2.1%，交易量 +0.8%、客單價 +1.3%，管理層稱連續三季正向交易量；餐廳層級營業利益率 23.3%（去年同期 24.5%），牛肉與運費成本上升；維持全年同店銷售低個位數成長指引。","source":"NRN / Zacks / Finsee Chipotle Q3 2026 earnings coverage","url":"https://finsee.ai/earnings/cmg/2026/q3/en/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Placer.ai：CMG 到訪人次 2026 Q2 年增 5.8%、Q3 年增 6.0%，高於同類別 2.2% 與 1.9%；18–29 歲佔其客群 18.1%（快休閒整體 17.3%）。","source":"Placer.ai, Chipotle's bet on younger diners is paying off","url":"https://www.placer.ai/anchor/articles/chipotles-bet-on-younger-diners-is-paying-off","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Black Box Intelligence Q3 2026 更新對 2027 的預測：銷售小幅成長、客流大致持平；NRA 2026 展望為實質銷售成長 1.3%。","source":"Black Box Intelligence State of the Restaurant Industry Q3 2026 webinar; NRA 2026 State of the Industry","url":"https://blackboxintelligence.com/event/webinar-state-of-the-restaurant-industry-q3-2026/","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Chipotle 8-K 揭露 FDA 與明尼蘇達衛生部調查與供應鏈相關的沙門氏菌疫情；明州機關無持續疑慮，問題追溯至單一批次墨西哥辣椒並已下架","source":"SEC EDGAR 8-K 2026-08-04","url":"https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000069/cmg-20260804.htm","excerpt":"We are aware that public health authorities such as the Food and Drug Administration and the Minnesota Department of Health are investigating the source of a salmonella outbreak in the supply chain impacting several food service retailers in Minnesota and other states.","as_of":"2026-08-04","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 載明部分食材（酪梨、番茄、牛肉、豬肉、萊姆、辣椒、香料）、設備與包材來自美國境外（墨西哥、加拿大、中國），可能面臨關稅、貿易制裁或稅負上升。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm","excerpt":"we source some ingredients (including avocados, tomatoes, beef, pork, limes, peppers and spices), restaurant equipment, packaging and paper products outside the U.S. (including from Mexico, Canada and China), which could subject them to increased tariffs, trade sanctions or taxes.","as_of":"2026-02-04","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025 年已實施關稅使食品飲料包材成本占營收比增加 0.2 個百分點，公司估計持續性影響約 15 bps。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm","excerpt":"We estimate that the tariffs enacted in 2025 will impact food, beverage and packaging costs by about 15 basis points on an ongoing basis. These estimates could vary based on future tariff policy changes.","as_of":"2026-02-04","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"公司約一半酪梨來自哥倫比亞、秘魯、多明尼加，非墨西哥；CEO 表示傾向吸收關稅成本、維持菜單價格（2025 年初報導）。","source":"NBC News: Chipotle downplays looming Trump tariffs, says only half of its avocados are from Mexico","url":"https://www.nbcnews.com/business/business-news/chipotle-downplays-looming-trump-tariffs-only-half-avocados-mexico-rcna190858","excerpt":"Chipotle buys about half of its avocado supply from Colombia, Peru and the Dominican Republic","as_of":"2025-02-05","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K 揭露：部分食材（酪梨、番茄、牛肉、豬肉、萊姆、辣椒）、設備與包材來自美國境外（墨西哥、加拿大、中國），可能面臨關稅、貿易制裁或稅負；公司以遠期合約、關鍵供應商夥伴、分散供應基礎與原產國來緩解，但未必能完全避免價格上漲。","source":"Chipotle FY2024 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1058090/000105809025000014/cmg-20241231.htm","excerpt":"In addition, we source some ingredients (including avocados, tomatoes, beef, pork, limes and peppers) restaurant equipment, packaging and paper products outside the U.S. (including from Mexico, Canada and China), which could subject them to increased tariffs, trade sanctions or taxes.","as_of":"2025-02-06","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"管理層稱目前約一半酪梨供應來自墨西哥，其餘來自哥倫比亞、秘魯、多明尼加（已分散原產國）。","source":"CNBC/NBC DFW: Chipotle downplays looming Trump tariffs, says only half of its avocados are from Mexico","url":"https://www.nbcdfw.com/news/business/money-report/chipotle-downplays-looming-trump-tariffs-says-only-half-of-its-avocados-are-from-mexico/3759317/","excerpt":"only about 50% of our avocado supply today is coming out of Mexico","as_of":"2025-03-04","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 摘要：2025 年已生效關稅預估持續影響食品、飲料與包材成本約 15 個基點（此為摘要轉述，未核 10-K 原文）。","source":"Chipotle FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"CMG 2026Q3 可比店銷售 +2.1%（客單 +1.3%、交易數 +0.8%），連續第三季交易數正成長；全年維持低個位數可比成長，Q4 預期約 +2%，餐廳層級營業利益率略低於 22%。10-Q 稱 7 月起有低個位數逆風（食安疑慮與地緣政治），8 月底回到事件前水準。","source":"Chipotle Q3 2026 8-K / 10-Q（SEC）；NRN","url":"https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000104/cmg-20260930.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"CMG 2026 計畫漲價約 1%–2%，低於預期成本通膨 3%–4%，擠壓餐廳層級利潤率約 150bp；2025 可比銷售 -1.7%；2026Q2 可比 +2.2%、交易數 +1%。同業 CAVA 2026Q2 同店 +9%（客流 +5.3%），Sweetgreen 同店 -6.2%。","source":"Nasdaq/Zacks: Chipotle's Pricing Lags Inflation; Chipotle Eyes Low-Single-Digit 2026 Comps","url":"https://www.nasdaq.com/articles/chipotles-pricing-lags-inflation-how-deep-margin-squeeze","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"NRA 2026 年 7 月更新：全美餐廳與餐飲服務銷售 2026 年預期 +4.3%（原 +4.8%），扣除通膨 +0.8%（原 +1.3%）；2027 預期升至 +4.8%。","source":"National Restaurant Association 2026 forecast update","url":"https://restaurant.org/research-and-media/research/restaurant-economic-insights/analysis-commentary/restaurants-remain-resilient-despite-challenging-business-conditions/","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"CMG 10-K 自述持續投資 AI／機器學習等新技術以減少人力與提升效率，但可能達不到預期效益並帶來資安、隱私、幻覺、智慧財產等新風險（公司自身採用技術，非外部替代品取代其核心產品）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm","excerpt":"We continue to invest in and utilize emerging technologies that have potential to make business tasks easier, more efficient and less labor intensive, including artificial intelligence and machine learning. These new technologies may not deliver the expected efficiencies and could expose us to new risks, including risks related to cybersecurity, data privacy, inaccuracies, hallucinations, bias or discrimination and claims of intellectual property infringement.","as_of":"2026-02-04","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"廠商指南稱：2026 年全菜單廚房自動化僅在極高量、有限菜單的 QSR 具商業可行性；送餐機器人最成熟。","source":"roboticscenter.ai Restaurant Robots in 2026: What Actually Works（廠商部落格）","url":"https://roboticscenter.ai/en/blog/restaurant-robot-guide","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Digital 佔食品飲料營收 38.3%（2026 Q2），去年同期 35.5%；Q1 為 38.6%","source":"CMG Form 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000066/cmg-20260630.htm","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026-04-13 重推忠誠計畫 Rewards on Repeat，新平台；報告 2100 萬活躍會員；Q1 call 稱每日註冊上升近 25%，忠誠佔 Q1 銷售 32%","source":"Chipotle IR press release 2026-04-13; Customer Experience Dive","url":"https://ir.chipotle.com/2026-04-13-CHIPOTLE-RELAUNCHES-REWARDS-WITH-REWARDS-ON-REPEAT,-DELIVERING-MORE-VALUE-WITHOUT-TRADE-OFFS","excerpt":null,"as_of":"2026-04-13","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Recipe for Growth 五大支柱之一為以科技現代化商業模式；新設 chief digital officer 與 emerging technologies VP。搜尋未見訂閱制","source":"Nation's Restaurant News","url":"https://www.nrn.com/fast-casual/chipotle-sharpens-its-focus-on-emerging-technology-loyalty","excerpt":null,"as_of":"2026-02-10","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Tickflow 彙整頁（2026-08-01）：共識目標價約 $42.94，評級 Buy（2.32/5），41 位分析師；頁面當時價 $37.37（此為來源頁數字，非 DD 現價）","source":"Tickflow CMG forecast","url":"https://www.tickflow.io/stock/CMG/forecast","excerpt":"Based on 41 analyst ratings, CMG has a consensus rating of Buy (2.32/5) with a +16.4% upside to the consensus target of $42.94.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布：Nasdaq 文章稱分析師目標價區間 $35–$45；TickerLeague 稱共識 $42.80、區間 $36–$52（單一來源、日期不明）","source":"Nasdaq / MarketBeat 'Is Chipotle's 2026 playbook the secret sauce for a reversal'; TickerLeague","url":"https://www.nasdaq.com/articles/chipotles-2026-playbook-secret-sauce-reversal","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY26 可比店銷售 guidance 年初約持平；Q2（7/29）後多個來源稱公司上調全年可比店銷售展望至低個位數（二手來源，未見原始新聞稿）","source":"247WallSt Chipotle Q2 2026 / 搜尋摘要","url":"https://247wallst.com/cards/chipotle-mexican-grill-q2-2026-earnings-cmg-01kyqrvm90jmcveyq1trebtwwy","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Wells Fargo 把 2026Q4 同店成長預估降至 1%（共識 3.2%）；TD Cowen EPS 預估低於共識（Q4 0.26 vs 0.28）——部分分析師低於共識，共識高於持平的原始 guidance","source":"搜尋摘要（Wells Fargo、TD Cowen 預估修正）","url":"https://finance.yahoo.com/markets/stocks/articles/chipotle-gets-mixed-calls-q1-153234562.html","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill：FY2026 EPS 共識 $1.16（2026-10-24 最新紀錄，38 位分析師）；下一季 EPS 1 個月修正約 -0.13%","source":"Chartmill CMG estimates","url":"https://www.chartmill.com/stock/quote/CMG/estimates","excerpt":"Latest recorded estimate: 1.16 USD · Oct 24, 2026 · 38 analysts","as_of":"2026-10-24","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Seeking Alpha 營收修正：8 上修 vs 24 下修（無日期快照）","source":"Seeking Alpha CMG revisions","url":"https://seekingalpha.com/symbol/CMG/earnings/revisions","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"FT 報導 Starbucks 曾評估收購 Chipotle（2026-10-08），未見正式出價，Starbucks 稱不評論市場傳聞","source":"roic.ai news：Starbucks explored takeover of Chipotle but no bid materializes","url":"https://www.roic.ai/news/starbucks-explored-takeover-of-chipotle-but-no-bid-materializes-10-08-2026","excerpt":null,"as_of":"2026-10-08","retrieved_at":"20261103","affects":["valuation","triggers","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026 年 8 月起沙門氏菌疫情與墨西哥墨西哥辣椒（jalapeño）有關，Chipotle 於 2026-07-20 為受影響店換供應商；供應商層級召回，非 Chipotle 自有產品召回","source":"WGCU News：Fresh jalapenos recalled, link to salmonella cited, FDA investigation ongoing","url":"https://www.wgcu.org/health/2026-08-05/fresh-jalapenos-recalled-link-to-salmonella-cited-fdas-investigation-is-ongoing","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Stradford v. Chipotle 股東集體訴訟：2025-12-18 法院准許駁回第一修正訴狀（可補件），2026-01-20 原告提第二修正訴狀，公司擬再聲請駁回","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm","excerpt":"On December 18, 2025, the court issued an order granting Chipotle’s motion to dismiss the first amended complaint, with leave to amend, and on January 20, 2026, plaintiffs filed a second amended complaint repeating substantially the same allegations as the original complaints.","as_of":"2026-02-04","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"FT 報導 Starbucks 曾評估收購 Chipotle，未見正式出價","source":"roic.ai news","url":"https://www.roic.ai/news/starbucks-explored-takeover-of-chipotle-but-no-bid-materializes-10-08-2026","excerpt":null,"as_of":"2026-10-08","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Stradford v. Chipotle 股東集體訴訟仍在審理，第二修正訴狀已提","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm","excerpt":"on January 20, 2026, plaintiffs filed a second amended complaint repeating substantially the same allegations as the original complaints. Chipotle intends to file a motion to dismiss the second amended complaint.","as_of":"2026-02-04","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"沙門氏菌疫情關聯進口墨西哥辣椒，Chipotle 於 2026-07-20 換供應商；供應商 Coast Citrus 召回，非 Chipotle 自有召回","source":"WGCU News","url":"https://www.wgcu.org/health/2026-08-05/fresh-jalapenos-recalled-link-to-salmonella-cited-fdas-investigation-is-ongoing","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"CMG","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.84,"operating_margin_pct":14.95,"fcf_margin_pct":11.88,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MCD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.38,"operating_margin_pct":45.71,"fcf_margin_pct":28.02,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CAVA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":24.64,"operating_margin_pct":7.32,"fcf_margin_pct":3.57,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAVA","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WING","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.37,"operating_margin_pct":27.74,"fcf_margin_pct":15.97,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WING","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SBUX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.9,"operating_margin_pct":10.17,"fcf_margin_pct":9.44,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SBUX","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"CMG"},"financial_history":{"ticker":"CMG","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":8634652000.0,"revenue_yoy_pct":null,"gross_margin_pct":23.88,"operating_margin_pct":14.03,"net_income":899101000.0,"diluted_eps":0.6408,"free_cash_flow":844015000.0,"fcf_margin_pct":9.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":9871649000.0,"revenue_yoy_pct":14.33,"gross_margin_pct":26.2,"operating_margin_pct":16.54,"net_income":1228737000.0,"diluted_eps":0.8868,"free_cash_flow":1222746000.0,"fcf_margin_pct":12.39,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":11313853000.0,"revenue_yoy_pct":14.61,"gross_margin_pct":26.67,"operating_margin_pct":17.55,"net_income":1534110000.0,"diluted_eps":1.11,"free_cash_flow":1511473000.0,"fcf_margin_pct":13.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":11925601000.0,"revenue_yoy_pct":5.41,"gross_margin_pct":25.38,"operating_margin_pct":16.88,"net_income":1535761000.0,"diluted_eps":1.14,"free_cash_flow":1447590000.0,"fcf_margin_pct":12.14,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CMG/CMG_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**Chipotle Mexican Grill, Inc.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Good afternoon, and welcome to Chipotle Mexican Grill's Third Quarter Fiscal 2026 Earnings Call. [Operator Instructions] Please note this event is being recorded. I would now like to turn the conference over to Christian D'Souza, Vice President, Investor Relations. Please go ahead.

**Christian D'Souza** (Executives):
Hello, everyone, and welcome to Chipotle Mexican Grill's Third Quarter Fiscal 2026 Earnings Call. By now, you should have access to our earnings press release. If not, it can be found on our Investor Relations website at ir.chipotle.com. Additionally, supplemental investor information is available on our site as a reference for today's call. 
I will begin by reminding you that today's discussion includes forward-looking statements, including projections about our future business, financial and other performance results. These statements are based on management's current business and market expectations, and our actual results could differ materially from those projected in the forward-looking statements. Please see today's earnings release and the risk factors contained in our annual report on Form 10-K and in our Form 10-Qs for a discussion of risks that may cause our actual results to vary from these forward-looking statements.
Our discussion today will include non-GAAP financial measures. A reconciliation to GAAP measures can be found via the link included on the Presentations page within the Investor Relations section of our website. We will start today's call with prepared remarks from Scott Boatwright, Chief Executive Officer; and Adam Rymer, Chief Financial Officer, after which we will take your questions. And with that, I will turn the call over to Scott.

**Scott Boatwright** (Executives):
Thank you, Christian, and good afternoon, everyone. We are pleased to see the momentum in our business continue in the quarter as we delivered revenue growth of 9.6%, once again including positive comparable sales and transactions. These results were fueled by our Recipe for Growth strategy as we continue to improve restaurant execution, deepen engagement with our Rewards members, bring new craveable innovation to the menu and expand occasions. 
Additionally, our marketing connected with consumers in new and culturally relevant ways, including through our 100 Creators campaign. And we've been opening a new restaurant nearly every day of the year and see tremendous opportunity to continue to do so even in our most dense markets. Our focus remains clear: Strengthen what differentiates Chipotle, execute with greater consistency, and create more reasons for guests to choose us. 
Broader consumer and industry headwinds may continue, but initiatives across our Recipe for Growth strategy are building and giving us more tools to win in any environment. We are still in the early stages of this work, and it's gaining traction. The progress we delivered this quarter gives us even greater conviction in our strategy and the multiple avenues we have to drive sustained growth at scale. In short, we are a category leader. We have a uniquely differentiated brand with strong fandom, and we believe much of our growth opportunity is still in front of us. 
Now I'll walk through our progress across each of the 5 strategic pillars, starting with our first pillar, protecting and strengthening the core because everything begins with running great restaurants. For our guests, that means delicious food made from high-quality ingredients, generous and consistent portions, exceptional throughput, on-time and accurate digital orders, clean restaurants and genuine hospitality. These are fundamental to our brand promise, and we remain focused on delivering them consistently throughout the day across every restaurant globally. 
Our high-efficiency equipment package is showing how targeted investments in our restaurants can drive better outcomes for our guests, our teams and our business. Restaurants with HEEP are delivering hundreds of basis points of comparable sales uplift, improvements in guest satisfaction and taste of food scores and over 2 additional entrees during the peak 15-minute period. HEEP is now installed in over 1,700 restaurants, and we continue to work toward approximately 2,000 restaurants by year-end. 
HEEP is designed to simplify morning prep and grill operations, improve culinary consistency and flavor, reduce menu outages and help our teams deploy more effectively during peaks. Importantly, we continue to reinvest the labor efficiencies created by the equipment back into our restaurants, giving our teams greater capacity to focus on throughput and hospitality. 
Throughput remains a key focus and one of the most important ways we believe we can improve the guest experience and drive incremental transactions. When we have the 4 pillars of throughput in place, our teams can move guests through the line faster while creating more opportunities to engage with them in a genuine and hospitable way. We have been focused on Linebacker and Expo deployment for the past several quarters and have made great progress on execution. We are now expanding our focus to drive consistent execution across all 4 pillars, including Mise en Place and Aces in their places, which is happening in fewer than half our restaurants today. 
We fully recognize the importance of exceptional throughput and know this is our strategic advantage. While we've made progress, I know we can be better. We will be emphasizing this evolution in Q4, so we are well prepared for the seasonal ramp in 2027, and we enter the new year with the momentum necessary to be great. At the same time, we are reinforcing accountability around hospitality and execution. I attended our Team Director conference during the quarter, and this year's agenda was focused on being brilliant at the basics that bring guests back time after time. 
Preparing exceptional food is central to this, and Jason Kidd, our Chief Operating Officer, had a simple message for our teams, "Run to the food. Taste it every time and ensure it's delicious for our guests." That focus is already paying off with Taste of Food scores up nearly 1 point year-over-year. We're proud of that progress, but just like throughput, we know we can be even better. 
Great execution starts with great leadership in the restaurants, and we continue to optimize general manager and apprentice deployment to ensure our busiest dayparts are supported. These efforts are collectively leading to the better outcomes we are seeing in operational metrics, and we have made meaningful progress, but we know there's more opportunity ahead. Our goal is to deliver the Chipotle experience with consistency in every restaurant every day. 
Turning to our second pillar, modernizing our business through technology and digital innovation. Our goal is straightforward: Use technology to make our teams more effective and make the Chipotle experience easier, faster and more rewarding for our guests. Under Chief Digital Officer Arlie Sisson's leadership, we are building the capabilities to accelerate progress, and Arlie is strengthening her team with the addition of AI and architecture leadership to help accelerate innovation across the business. 
We are still in the early stages of what AI can do. One example is our AI-enabled cook-to-needs tool, which entered pilot during the third quarter and is now rolled out to over 500 restaurants. The tool, which we plan to roll out nationally early next year, uses AI-based demand forecast to recommend the right amount of freshly prepared food at the right time. This helps reduce manual data entry, increase prep efficiency and readiness, reduce waste and support better deployment and more consistent culinary execution. 
Alongside this, we are also developing Ava Cado, our in-restaurant AI assistant, and see the potential to expand its scope and assist general managers with operational insights and actionable coaching that can help our team leaders make better decisions in real time. Our proprietary digital makeline interface, which we call Chipotle Kitchen, is also currently rolling out to our restaurants with plans to reach several hundred by year-end. 
The technology is designed around improving the outcomes that matter most for our teams and guests: order accuracy, on-time fulfillment, speed, ease of integrating new menu items and guest satisfaction. We will continue scaling to the entire system throughout 2027. In April, we revamped Chipotle Rewards and are continuing to see strong results from the program with our highest comps consistently coming from loyalty occasions. 
In-store enrollment has also remained elevated, driving our active membership to reach over 24 million guests for the quarter, and we continue to see significant opportunity to deepen engagement with members. Summer of Extras was a strong example with 6.8 million Rewards members opting into the program, an increase over last year. Members earned 25 million badges and completed approximately 600,000 challenges. Most importantly, our loyalty share of sales increased to over 33%, our highest ever. This is exactly what the program is designed to do, deepen engagement and give guests more reasons to visit Chipotle. 
We also continue to progress with our frictionless rewards pilot. Around 30% of our guests use Apple Pay in-store, and they will be able to automatically earn points while paying, eliminating the need for a separate rewards scan. It's a simple change, but an important one because it reduces a key friction point while also supporting throughput. We will advance the test through stage gate in Q4 and plan to take the technology across the enterprise in 2027. 
Longer term, we see a significant opportunity for technology to make rewards increasingly personalized, improve in-restaurant identification and help us more effectively reengage lapsed members. Our third strategic pillar is evolving our brand messaging, accelerating menu innovation and expanding the occasions where guests choose Chipotle. At the center of this work is the value proposition that has defined Chipotle for more than 3 decades, real food made with high-quality ingredients, freshly prepared using classic culinary techniques, served with generous portions and speed at an accessible price point. Our brand tracker revealed that our value scores and overall brand health remained strong in Q3 with sequential gains in both amount and quality of food for the money. 
Under Chief Brand Officer Fernando Machado's leadership, we are supercharging how we communicate our value proposition and connecting what makes Chipotle different with what matters to consumers today. And we are doing it in ways that are more ambitious, culturally relevant and distinctive to the brand. We are showing up across creator content, sports and entertainment, gaming, fashion and other spaces to meet guests where they are, and guests are recognizing the differentiation. 
We saw stable or improving wallet share across the quarter with broad strength across income and age cohorts. Importantly, we saw lower income cohorts outperform higher income cohorts for the first time this year, with the greatest strength in September when promotional activity was at its lowest. Driving this in Q3 was our 100 Creators campaign, which brought popular creators directly into Chipotle kitchens to experience the brand firsthand and capture the care, craft and fresh preparation that goes into our food every day. 
Our work with Cardi B and the Bardi Bowl created another meaningful connection while promoting our Chili Lime Chips. The Salish Matter Kid's Meal helped us engage families with younger guests, while our PGA 2K25 integration allowed us to tap into the strong affinity between Chipotle and the golf community. And recently, we revealed that the music within our 100 Creators campaign was the result of a partnership with the London Vegetable Orchestra. We enlisted them to record an original track at the legendary Abbey Road Studios with instruments made from our 53 real ingredients. 
These activations are designed to do more than generate attention. They help us tell the story in fresh ways, broaden our reach and keep the brand top of mind. Menu innovation is another important factor in enhancing our value proposition, attracting new guests and giving existing guests more reason to visit, all while staying true to our Food with Integrity commitment and the culinary principles that define Chipotle. 
On August 31st, we broke new ground by launching 2 limited time offerings together, bringing back Pollo Asado with an all-new recipe and our Chili Lime Chips, our first innovation in the category. Pollo Asado features freshly grilled Adobo chicken seasoned with garlic and Mexican spices, hand-cut cilantro and bright citrus. Guest response has exceeded our expectations, driving incremental transactions and an attachment rate in the low 20% range, which is significantly higher than our prior launch. 
Chili Lime Chips were inspired by a viral fan food hack and are made fresh daily and hand seasoned with fresh squeeze lime and chili peppers. Guest response has been very positive, driving incremental growth in overall chip incidents. Cilantro Lime Sauce also remained on the menu throughout the quarter and has maintained a strong attachment rate while outperforming the benchmark set by prior sauce innovation. 
Next week, we are excited to bring back smoked brisket for a limited time with a new and even more delicious recipe, featuring responsibly raised beef that is seasoned with spices, including smoked serrano and Chipotle chili peppers before being smoked over mesquite wood. Once in our restaurants, teams sear the brisket on the plancha, finish it with spices, sauce it in a savory sauce made with smoky chili peppers and hand chop it in small batches throughout the day. 
Smoked Brisket has demonstrated both broad guest appeal and incremental transaction growth in the past, and we look forward to bringing it back. We have been hard at work this year on our innovation pipeline, which remains strong. In 2027 and beyond, we see considerable opportunity across proteins, sides, and beverages, giving us multiple ways to create fresh news around Chipotle while staying true to who we are. 
We also continue to make progress on our efforts to expand catering nationally, and we intend to begin rolling it out in Q1 of 2027. We have been working on refining our approach and developing bespoke load balancing tools to help optimize the process. And our pilots have delivered the operational, marketing and technology insights we need to feel confident we can grow without disrupting the core lunch and dinner business. 
Catering guests have heightened expectations, and we intend to deliver flawless execution as we scale. Additionally, Chipotle Family Meals, which are also available in Canada, are resonating as a convenient, high-value solution for groups of 4 to 6. To drive awareness for the family meal offering, this month, we launched a memorable marketing campaign, which I'll just say, like its name, is an enormous bag to highlight the oversized meal offering. This was a fun and distinctive way to connect the brand to culture, drive buzz and showcase value. 
Early results have shown a step-up of over 30% in Family Meal sales. Together, Catering and Chipotle Family Meals represent approximately 3% of sales today. Both remain highly incremental and operationally efficient, giving us another meaningful runway for growth. 
Turning to our fourth pillar, Cultivating the Best Talent in the Industry. Our people remain our greatest competitive advantage. Quality of our restaurant teams and leadership directly influences consistency, hospitality, restaurant performance and our ability to sustain growth. We continue to make progress building the pipeline of general managers, apprentices and field leaders needed to support new restaurant openings, and we're proud to see both general manager and crew turnover down year-over-year. 
We also understand the value of a second tenured manager in the restaurant with better operational and guest-facing outcomes occurring in restaurants that do have an apprentice. 3/4 of our restaurants have apprentices today, and we will begin expanding coverage incrementally in 2027. We will keep a keen focus on hospitality and measuring the sustained benefit of this investment, and we believe the returns will justify further expansion across the year. Central to our people strategy is offering world-class benefits and educational assistance continues to be a strong driver of retention. 
In August, we celebrated the 10-year anniversary of our partnership with Guild, which provides debt-free education and greater career mobility for our team members. Nearly 25,000 team members have enrolled in the education program and more than 14,000 have completed one. Those programs reinforce something fundamental to our culture. Chipotle is a place where people build meaningful long-term careers. 
And as we strengthen leadership across the organization, we're continuing to add capabilities and expertise at the Board level to support our long-term ambitions. In September, we added Sabir Sami to our Board of Directors. Sabir brings extensive global restaurant leadership and operating experience with capabilities that align with our international growth ambitions. 
Finally, turning to our fifth pillar, we are expanding our global footprint. Our approach to development remains disciplined, site selection, restaurant economics, expected returns and the strength of our talent pipeline all inform the pace of growth and each remains strong. Chipotlanes continue to be an important part of that model. They provide greater convenience, drive higher digital mix, generate stronger sales and returns, and reduce friction for our guests. During the third quarter, we reached an important milestone with the opening of our 1,500th Chipotlane. In the U.S. and Canada, we opened 83 new restaurants during the quarter, including 53 Chipotlanes. 
We continue to see significant white space in both countries and remain confident that we will open around 350 restaurants this year. Looking ahead to 2027, we expect to open approximately 340 to 360 company-owned restaurants in the U.S. and Canada. Our company-owned international business also continued to expand during the quarter with a new restaurant in the U.K., which has seen opening performance consistent with our strongest London restaurants.
Alongside our company-owned growth, our partner-operated model is allowing us to enter new markets with experienced local operators and expand access to Chipotle around the world. The third quarter marked an important step forward in our ambition to build Chipotle into an iconic global brand as we entered Mexico, Saudi Arabia and South Korea, meaning Chipotle is now available to enjoy in 11 countries across the globe. 
Each region has demonstrated strong local demand, which can be seen in the long lines of guests waiting for us to open the doors on day 1 in each new market we enter. In Mexico, our first restaurant opened in July to an extremely positive reception in the Monterrey metropolitan area with our partner, Alsea. Opening volumes exceeded our initial expectations, and this has reinforced the appeal of the Chipotle brand within the country. We plan to open our next restaurant nearby as well as our first location in Mexico City in 2027. 
We entered Saudi Arabia this quarter in partnership with Alshaya Group, and we were thrilled to see new opening volumes set yet another record and build on the demand we have seen across the Middle East. We also opened new restaurants in the UAE and Kuwait, bringing our total across the region to 18 restaurants. Our long-term outlook in the region remains unchanged, and we continue to believe it can support hundreds of Chipotle restaurants over time. 
Additionally, our first restaurant in South Korea opened last month near Gangnam Station, where lines stretched several city blocks for weeks and average daily sales trends built throughout the quarter. In fact, earlier today, we opened our second location in Seoul and have additional restaurants in development as we build the business with SPC Group, including our planned opening in Singapore next spring. So far in 2026, 8 restaurants have opened outside the U.S. and Canada, and the response we are seeing across markets reinforces our belief that the appeal of Chipotle is borderless. 
Consumers around the globe value high-quality food, prepared fresh with real ingredients, giving us confidence that our model can resonate well around the globe. In 2027, we expect to open around 15 to 25 restaurants outside the U.S. and Canada. To close, our third quarter results reinforce that our Recipe for Growth strategy is gaining traction and creating multiple levers to navigate a dynamic industry and consumer environment and drive sustained growth. 
We are improving restaurant execution, throughput and hospitality. We are scaling technology and AI while building a more engaging rewards ecosystem. We are accelerating menu innovation and evolving our marketing to keep Chipotle relevant and top of mind. We are also building new occasions through Catering and Family Meals. We continue to develop a deep pipeline of talent and are expanding globally with discipline. I'm confident we have the right strategy, the right leadership team and a significant opportunity ahead as we continue to build Chipotle into an iconic global brand. With that, I'll turn it over to Adam.

**Adam Rymer** (Executives):
Thanks, Scott, and good afternoon, everyone. Our third quarter results reflect the continued traction of our Recipe for Growth strategy as well as our ability to respond quickly and decisively when we see shifts in demand. In the third quarter, sales grew 9.6% to $3.3 billion, including a comparable restaurant sales increase of 2.1% and a positive transaction comp of 0.8%. Digital sales of $1.3 billion were 38.8% of total sales compared to 36.7% in the prior year. 
Restaurant level margin was 23.3%, a decline of 120 basis points year-over-year. Adjusted diluted earnings per share was $0.27, down 7% versus last year. And we opened 84 company-owned restaurants and 5 partner-operated restaurants, expanding into 3 new markets: Mexico, Saudi Arabia and South Korea. We entered the quarter with strong sales trends supported by our Recipe for Growth initiatives. However, industry headwinds beginning in mid-July slowed our momentum. We quickly acted to reengage our guests with promotional offers, and I am proud of how thoughtfully our teams responded. 
We were pleased to see trends normalize by late August, and we saw further improvement in September after the launch of Pollo Asado and Chili Lime Chips as well as our 100 Creators campaign. October trends have softened, consistent with the broader industry. However, we continue to see positive underlying engagement with our menu innovation and activations. We look forward to building momentum with the launch of Smoked Brisket next week, and we are confident we will deliver on our guidance of low single-digit comps for 2026. 
On pricing, the impact in Q3 was around 2.7%. We anticipate it will increase to about 3% in Q4, bringing total pricing in 2026 to around 2%. As we look ahead to 2027, we currently anticipate overall inflation to remain in the low to mid-single-digit range and expect to continue managing that inflation over the long run with our new approach to menu pricing. 
Before I walk through the P&L, I want to take a moment to highlight the economics behind our promotional strategy and how we approach our overall marketing investment. Promotions such as our BUY-ONE-GET-ONE activations and protein limited time offers are designed to connect with our guests in a culturally relevant way. They do more than drive a single day or a single quarter of sales. They bring new and lapsed guests into our restaurants, increase frequency among existing guests and keep Chipotle top of mind. 
As we shared earlier this year, our protein limited time offers typically generate a few hundred basis points of transaction lift over the life of the promotion. And we generally sustain part of that lift longer term as many new guests continue to dine with us after the offer ends. Our BUY-ONE-GET-ONE activations have followed a similar pattern and the benefit is amplified when we find opportunities to connect at the cultural moment. It is this stickiness that makes these investments so productive over time. 
We evaluate marketing and promotional investments through a return-focused lens. When we have great ideas that deliver attractive returns, we will lean in as we did this quarter. This discipline gives us the flexibility to respond quickly to shifts in demand while protecting the long-term strength of our economic model. 
With that, I will go through the key P&L line items, beginning with cost of sales. Cost of sales in the quarter was 29.5%, a decrease of about 50 basis points from last year. The benefits of menu pricing and tariff relief were more than enough to offset inflation, which was primarily driven by beef and freight. For Q4, we anticipate cost of sales to be around 30.5%, primarily due to the impact of our Smoked Brisket limited time offer. On an underlying basis, this puts cost of sales inflation at around 3% for Q4. 
Labor costs for the quarter were 25.7%, an increase of about 50 basis points from last year. The increase was driven by sales volumes, wage inflation and higher labor usage in support of promotional activity. In addition, we recognized some discrete costs related to insurance. These factors were partially offset by the benefit of menu price increases. Excluding these discrete impacts, we saw underlying inflation in the low single-digit range, and we expect this to continue into Q4 with labor costs around 26%. 
Other operating costs for the quarter were 16%, an increase of about 100 basis points from last year, primarily driven by higher marketing, delivery mix and inflation across several items, including utilities and maintenance. Marketing costs were in the mid-3% range during the quarter, an increase of about 40 basis points from last year as we leaned into promotional activity to reengage guests following the industry headwinds mid-quarter. 
In support of the Brisket campaign in Q4, we expect marketing costs to land in the high 3% range, bringing other operating costs to around 16%. Altogether, this will put Q4 margins at just under 22%, which is roughly 150 basis points lower than last year. After normalizing for a 70 basis point gift card breakage benefit in the prior year and the shift in marketing spend to support Brisket, the decline is driven by sales volume. 
With pricing now in line with inflation, our unit economic model remains intact, and we expect margins to expand as we drive additional transaction growth. G&A for the quarter was $185 million on a GAAP basis or $184 million on a non-GAAP basis, excluding retention equity awards granted to key executives in August of 2024. G&A included $155 million of underlying G&A, $29 million of noncash stock compensation, offset by $0.5 million related to lower bonus accruals and payroll taxes. 
For Q4, we expect G&A to be around $189 million on a non-GAAP basis, which will include $156 million in underlying G&A, $31 million in noncash stock compensation, although this amount could move up or down based on our actual performance and $2 million in higher bonus accruals and payroll taxes. As we continue to scale, our G&A growth is predominantly driven by field leadership roles supporting new restaurants, and we have leveraged G&A over the past several years, thanks to our disciplined approach to investments in technology and other areas. 
In 2027 and beyond, we intend to fuel our Recipe for Growth strategy while also leveraging G&A. Depreciation for the quarter was $103 million or 3.1% of sales. And in Q4, we expect it to remain in the low 3% range. Our effective tax rate for Q3 was 25.6% on a GAAP and non-GAAP basis. For fiscal 2026, we continue to expect our underlying effective tax rate to be in the 24% to 26% range, though it may vary based on discrete items. 
Our balance sheet remains strong as we ended the quarter with $1 billion in cash, restricted cash and investments and no debt. Share repurchases are an important part of our capital allocation program in a meaningful way to return value to shareholders. Year-to-date, we've repurchased $1.4 billion at an average price of $34.32, and we have about $1.6 billion remaining under authorization. During the quarter, there was a period where we were unable to repurchase our stock. However, we believe our shares are undervalued, and we look forward to returning to the market as soon as the earnings blackout lifts. 
To close, this quarter demonstrated the strength of our Recipe for Growth strategy and our ability to respond quickly and effectively when we see shifts in demand. Few brands can invest in the highest quality ingredients, offer an accessible price point and still deliver industry-leading economics. That unique model gives us the flexibility to invest behind our guests while protecting the long-term strength of the business. We are optimistic about closing out 2026 on a strong note, and we remain well positioned to continue creating long-term value for our guests, our teams and our shareholders. And with that, we can open it up for questions.

**Operator** (Operator):
[Operator Instructions] The first question comes from David Palmer with Evercore ISI.

**David Palmer** (Analysts):
I wanted to ask about this fourth quarter and what you think it means so far. I think you know that this quarter was supposed to be a payoff quarter of sorts where pricing was ramping through the year. You got the new kitchen equipment. You have more stores with that, the marketing improvement, the renewed focus on operations, the diminishing cyclospora headwinds and comparisons. And I think there was some expectation out there that the comps would continue to ramp maybe 3% plus, and you were kind of going there, it looked like in the third quarter. 
I think there's a perception that comps are down so far in October. And so that's making people jump to conclusions about wondering what's working, what's not working. So perhaps you can comment more specifically on October to date, what's happened? And then what's your diagnosis? What is -- what implications does this have for your strategy? And what sort of same-store sales expectation you might have for '27?

**Scott Boatwright** (Executives):
David, Scott here. Thank you for the question. I'll tell you, we entered the quarter -- I'll tell you how we finished September up 3.8% with little to -- very little promo activity, which gave us a lot of confidence that we're on the right track. We saw some broader industry pullback in the first part of October. I'll tell you we have since regained positive transactions, and we have high confidence in the balance of the quarter on the back of what is an extraordinary product in Brisket, which has had incredible demand over the past few years when we offered it. We see no difference this year. We think the product is improved and even better. And so we feel very confident that November and December set up very well for us with a potential exit rate on the year of 3% to 4%.

**Adam Rymer** (Executives):
Yes. And I'll add to that, David, just to give you an idea for Q4. So taking into account the choppy start for the quarter and the dynamic consumer environment, we anticipate that our Q4 comps will actually be around a plus 2%. But like Scott said, we'll have an exit rate in that 3% to 4% range. And again, that's going to be fueled by the launch of Brisket next week as well as several marketing initiatives that we have planned. And we're really excited really to continue to build upon this momentum in 2027. Too early to give any kind of guide at this point for comps. We'll do that at the next call, but it's still early days with many of our sales building initiatives from our Recipe for Growth strategy. So you can imagine that we're excited as this continues to build into 2027 and beyond.

**Scott Boatwright** (Executives):
Yes, David, I'll just -- one more I'll add on there. I think it's a really important note to say that there's only a few core tent poles of the strategy that are actually working for us here in 2026. Much of the strategy is yet to continue to build, scale and unfold and most of the growth is still well ahead of us.

**Operator** (Operator):
The next question comes from Sara Senatore with Bank of America.

**Sara Senatore** (Analysts):
Just maybe a question on throughput and then a quick question on, Adam, your comment on marketing. I think with the throughput piece, one of the things that we've heard from others is that maybe there's been too much focus on speed of service at the expense of hospitality. Just curious, I know you mentioned both, but as you think about measuring some of these other metrics to ensure that your -- the experience is better, has that changed what you are -- your checklist or your metrics that you measure for your management teams or how they're compensated? 
And then the question for Adam was you mentioned normalizing for marketing behind Brisket. I guess I was trying to understand that comment about normalizing since it sort of seems like just this is a step-up in spending around marketing that has worked for you, but it's not necessarily onetime.

**Scott Boatwright** (Executives):
Sara, Scott here. I'll start with the throughput question. I'll flip over to Adam on promo spending. I think it's important to note that Q3's performance in throughput was very consistent with what we saw in Q2. Bonus is still tied. So crew bonus is still tied to quarterly throughput measures. In the restaurants where we have HEEP into -- fully loaded, it's about 1,700 restaurants today. We're seeing plus 2 entrees in those restaurants as compared to the base, which gives us confidence that the HEEP investment is the right investment for our brand. 
And we'll finish that rollout as we've talked about or near complete that rollout by the end of 2027. I assure you, we are going as absolutely fast as we possibly can there. Also important to note, we are -- Jason and team are about to go under the tent once again with Throughput 2.0 and cascade the throughput fundamentals back through the organization once again, which is something we do on an annual basis. That work is starting here this quarter to ensure we are front-footed going into 2027. 
Can we get better? I am absolutely positive we can get better. Is it still an absolute focal point for this organization? It is core and center to Jason's operational strategy. We all know full well how critically important it is to our brand, and we're going to lean into that momentum that's building in a really meaningful way here in Q4.

**Adam Rymer** (Executives):
Yes. Sara, it's Adam. So to answer your question on marketing, you have to think about the fact that switching to this 4 protein LTO strategy that we've had this year is causing some shifts in marketing. So with Brisket coming on in November, there's a little bit more spend in the last 2 months of the year than kind of prior year. So that's where -- when we kind of talk about in support of that campaign, we expect marketing cost to be a little bit higher in Q4. So that was where that comment was based on.

**Operator** (Operator):
The next question comes from Danilo Gargiulo with Bernstein.

**Danilo Gargiulo** (Analysts):
Great. Scott, I wanted to expand on the comment that you were making earlier regarding your bias to action. I mean it's clear that so far, you've demonstrated greater bias to actions. You had 4 LTOs, greater marketing spending, more occasions being driven. Yet the -- on the traffic level, especially on the third quarter, it has been relatively flattish this year. So I know you're not giving any guidance for 2027, but just directionally, what's your expectations on traffic? Meaning do you think that you can get into positive traffic over there even if the market overall is not improving? And if so, can you help us understand maybe the building block of this traffic -- of this positive traffic growth into 2027?

**Scott Boatwright** (Executives):
Yes. Danilo, I think I heard you asking about traffic. I'll tell you, we've had positive transactions all 3 quarters of the year thus far. And we feel like we're in early days of the Recipe for Growth strategy, which is designed to do just that. It's a demand-driving strategy across the core tenets of technology, restaurant execution, innovation, brand messaging, group occasions. And we feel like we're in early days of that strategy. So if you're asking, can we drive transactions in a really challenging consumer environment? I think we've demonstrated for the past 3 quarters, we can do that. And the strategy is only in the early days and we'll continue to build and scale as the year unfolds and as we enter 2027. So if you're asking me if I have confidence in this team's ability to drive transactions in this environment, the answer is absolutely yes.

**Operator** (Operator):
The next question comes from Dennis Geiger with UBS.

**Dennis Geiger** (Analysts):
Wondering if you could talk a little bit more about the 4Q margin expectations, Adam, great color by line item, always helpful. I guess just relative to the comp expectation for the quarter, any other moving pieces? I get that the marketing seems like a pretty big piece of this. Any other moving pieces for the 4Q margins that maybe you didn't touch on, if anything on labor hours, investment in some of the labor programs that you've got, anything on promo impacts? Anything else to flag beyond some of those items you called out earlier?

**Adam Rymer** (Executives):
Yes. Sure, Dennis. So yes, what we called out earlier, of course, when you're kind of looking at it on a year-over-year basis, it's down about 150 basis points. Half of that is that gift card benefit that we got in the prior year. So you kind of have to look at that as a discrete item based off of that comparison. And then really the ad promo shift to support Brisket, call out another 30 basis points or so, and then the remainder is really sales volume. 
So we're expecting with that 2-ish percent guide about a flat transaction, but a mix impact of probably about a minus 1%. And then, of course, you've got the year-over-year impact from new restaurant openings. And so that gives you the bridge. But taking a step back and really thinking about margins in total, that will get you -- based off of our guidance, it will get you to about a 2026 margin of somewhere in that like mid-23% range. However, you have to remember that, that includes about 100 basis points of kind of that price inflation dislocation, right? Because we're going to be around 2% pricing this year, but our OpEx inflation is closer to 3%. 
And so when you're thinking about 2027, I would consider that 23.5% plus that 100 basis points, so call it a mid-24% margin is kind of the baseline, assuming that we're able to utilize price to offset inflation and then drive at least a point of trans to offset the impact of our NROs next year. And then any additional traffic growth on top of that, that will be margin accretive at our usual pass-through of somewhere around 40%. So I think those give you the pieces, not only for Q4, but kind of looking forward.

**Operator** (Operator):
The next question comes from Chris O'Cull with Baird.

**Christopher O'Cull** (Analysts):
Just as a follow-up, Adam, on the response to the margin question. The company has been making some sizable investments, obviously, to increase traffic. What comp do you believe is necessary to stabilize margin performance with this inflation outlook?

**Adam Rymer** (Executives):
Yes. I mean assuming that we're covering our inflation with pricing, which is what we intend to do. We might not get that right every quarter, but we intend to get that right over time. We need about 1 point of trans to offset the impact of new restaurant openings. So when you get north of that 1% trans comp, that's when you start to see that 40% flow through.

**Christopher O'Cull** (Analysts):
So if you're looking at 3% inflation, you're thinking a 4% nominal comp might be necessary to stabilize margin?

**Adam Rymer** (Executives):
Yes, that's correct.

**Christopher O'Cull** (Analysts):
Okay. And then how are you thinking about overall level of marketing investment that's right for the business as you go into '27? I think your spend is up over 20% year-to-date. So I'm just curious if you expect a similar rate of growth in marketing spend next year.

**Scott Boatwright** (Executives):
Chris, this is Scott. I think 3% is the right range for us to think about, and that could flex up or down. We will lean into return-generating opportunities and pull back when we don't see that same opportunity is how I would think about it. Right now, the baseline for that budget for the upcoming year will be in that 3% range. And we think that gives us a really strong calendar to support what I believe to be a best-in-class LTO platform for the upcoming year. But we'll see. There could be opportunities where we want to lean in, where we know there will be a return to be gained or to be had. And so that's where we'll spend our dollars.

**Operator** (Operator):
The next question comes from John Ivankoe with JPMorgan.

**John Ivankoe** (Analysts):
The question is on the physical asset itself. And outside of the High-Efficiency Equipment Package, really looking at the aesthetics of the box. We have talked about this before, but as over 2,000 Chipotle restaurants are over 10 years old. How much of an opportunity from both an employee and a customer perspective might a refresh give you? I say that because the vast majority of Chipotle customers, they might not dine in your restaurants, but they actually come to your restaurants, whether to order on-premise or pick up a digital order. So that must be a very important touch point for a lot of people. So as you've begun to stage gate the process in terms of refreshes, how big of an opportunity do you think it might be to modernize the brand further?

**Scott Boatwright** (Executives):
John, thank you. I think it could be a really big opportunity for the brand. We're in the very early days of testing a group of restaurants here in California, Florida and Texas. We're almost through. We're done with California. Texas is up and running. I think Florida is still in the early days of the remodel program. And what we're looking to do is really resurrect some of the legacy restaurants that are, let's call it, the first 1,000 restaurants we built in the brand, gosh, now over 20, 30 years ago. And what we're looking to do is bring them up to date, more open format, more modern, more differentiated. 
We think there's a strategic opportunity. We're seeing early signs that give us confidence that we're on the right track. But we'll have more to say in the -- probably in the Q1 earnings call on how we think about our remodel program, if you will, or a remodel strategy, but we think we're on the right track. We know there's an opportunity to make the environment more appealing, soften up the environment a bit and make the consumer feel more welcome in our restaurants.

**Operator** (Operator):
The next question comes from Peter Saleh with U.S. Bank BTIG.

**Peter Saleh** (Analysts):
Scott, you had just mentioned a great LTO lineup for 2027. Just trying to understand if you guys can help us out with how many of those LTOs next year will be new products versus existing LTOs that are coming back to the menu?

**Scott Boatwright** (Executives):
Yes, it's a great question, Peter. So we'll bring in some new innovation you'll see on the calendar -- you won't see it on the calendar, but you'll see it as we launch those products in the marketplace. And then you'll see some tried and true favorites, items that we know consumers want because they tell us daily to bring them back. And so we have -- we're setting up the calendar to have about 4 center-of-the-plate LTOs. And then we'll continue to lean into sides, dips, and we're going to really be a little more front-footed on beverage innovation in the upcoming year. 
We think there's a really strategic opportunity for our brand to drive incidents in a meaningful way through our partnerships with our beverage partners. And so you'll see more of that. But I don't want you to think that LTO, and I get this all the time means additional complexity necessarily for our restaurant teams. Our center-of-the-plate LTOs are really just a sauce change on our core protein. 
Our teams are executing that with ease in our restaurants and transition from one to the next is more simple than you would find in most brands that have an LTO strategy. So don't be discouraged by the pace of innovation there. Just know that we're going to put forward products that are on trend, on market, on brand and that will drive demand and create value. We've learned that our consumers are looking at value in different ways. Price isn't the only way they look at value. They look at innovation, menu innovation is a really meaningful point in the overall value equation.

**Operator** (Operator):
The next question comes from Andrew Charles with TD Cowen.

**Andrew Charles** (Analysts):
You talked about high 3% of sales spend on marketing or plan for marketing in the fourth quarter. And I'm curious if Fernando in place for the full quarter, should we expect this to be a fair run rate for the first half of 2027 and beyond?

**Adam Rymer** (Executives):
We haven't gotten to the point yet where we're going to kind of give an idea of how it's going to be from quarter-to-quarter next year. But as Scott said earlier, we're somewhere in that low 3% range or around 3% for next year, but we'll ebb and flow that as we see fit, whether it aligns with what we're doing from a TV standpoint or from a big advertising standpoint around when certain LTOs drop, or different investments that we want to make that we believe we can get a great return from.

**Andrew Charles** (Analysts):
And then just on the pricing side as well, we know there was a ramp throughout this year. Are you guys happy with the 2% rate? Do you see this as a sustainable level? I know you talked about, Adam, for instance, low to mid-single-digit inflation for 2027. What's kind of your philosophy on pricing as you look ahead?

**Adam Rymer** (Executives):
Yes. I mean it really hasn't changed. I mean I'd say, over the long run, we're going to continue to look at utilizing price to offset inflation, but we want to do it in a very measured patient way. And I say that because if there's temporary or transitory increases in inflation that we know is only going to last a few months, we won't utilize that opportunity, of course, to pass it on. We'll eat those costs. And so it's more of that longer-term inflation. But primarily in the past, it's been closer to that 2% range. And so we hope to get back to that sooner rather than later. It's just not looking like that's going to happen in 2027 at this point, but we'll give more color on that as we get into next year.

**Scott Boatwright** (Executives):
But I think it's important to note that the way we're rolling out pricing across the system allows us to measure pre and post net of control the impact of that price lift to ensure we don't see resistance greater than we should. And so we're able to flex pricing up or down or discontinue altogether based on what we're seeing happening in the consumer environment.

**Operator** (Operator):
The next question comes from Brian Harbour with Morgan Stanley.

**Brian Harbour** (Analysts):
The High-Efficiency Equipment Package is -- does that comp lift that you talked about sustain quite nicely? I mean has this been like an increasing contributor through the course of this year to your same-store sales? Is that what you expect in '27 as well?

**Adam Rymer** (Executives):
Yes. I mean I expect it to continue to build. So as we talked about on the call or in the prepared comments, we're at about 1,700 restaurants. But as we've said in the past, it takes a few months for us to really start to see that comp lift come into fruition, right? The teams have got to get used to the new equipment, and then it takes a little while for the guests to really see kind of that better hospitality, taste of food going up, all of those elements take a little bit longer as well. And so there's a bit of a lag. 
And so I would look at it as even though we're through 1,700 restaurants, it's probably only half of those restaurants that we're actually seeing that have been in place long enough to get that comp lift. So I expect this to continue to build. And everything that we look at, whether it's that first phase of restaurants or the ones that have kind of hit that 2- or 3-month mark, those comp lifts have sustained in that couple of hundred basis point range. And so we're excited to continue to build on this because I think it will build on our comps in 2027 and also in 2028.

**Scott Boatwright** (Executives):
Yes. And important note there as well to follow on is we're seeing in those restaurants where we're fully loaded, stronger guest satisfaction scores, stronger taste of food scores and better throughput at Max 15, which tells us we're on the right track. And as that continues to roll out to the entire system, we'll continue to scale and build.

**Brian Harbour** (Analysts):
Do you still expect kind of the mix dynamics that you've been seeing just within same-store sales, do you still expect that to continue?

**Adam Rymer** (Executives):
Yes. I mean for the near term, I do -- so mix impact in the quarter, for example, was about a minus 1.4%. It's still driven by lower group size, which again is being driven by increased Rewards engagement. And our Rewards percent of sales has been growing nicely. I think we're at around 33% or so right now. We were at about 30% or 31% last year at that same time. And so seeing nice improvement there. So think of that as people coming in and redeeming for free entrees or certain elements there, that's lowering that group size. 
And so that we expect to continue, especially as we continue to lean in on rewards. But we're also seeing a nice offset from extra meat, for example. So still up about 20% from the protein campaign that we launched in January. We'll, of course, start to lap that this January. But we're also seeing offsets in Cilantro Lime Sauce. We only had about a month of Chili Lime Chips, but that was in there as well. And then, of course, Family Meals. But again, I expect that roughly 100 basis point drag from group size to continue as we continue to lean into Rewards, but it will ebb and flow based off of some of this LTO activity.

**Operator** (Operator):
The next question comes from Jon Tower with Citi.

**Jon Tower** (Analysts):
I'm curious if you could speak to the delivery business, what you saw in the quarter and frankly, if there's any channel shifts you're seeing with consumers? And specifically, are there any initiatives underway to try and build the value perception with consumers in that channel specifically?

**Adam Rymer** (Executives):
Yes. I kind of start with just kind of what we're seeing. I mean it was kind of a low single-digit comp. But in all honesty, it was the least in terms of growth in the digital channels. Order ahead was our primary grower. I mean there's a lot of things going on in there, especially around Rewards. And as Scott mentioned earlier, 1,500 Chipotlanes, that's driving a lot of people to order ahead. And then Catering actually out-comped Delivery as well. But Delivery is still seeing growth on a year-over-year basis, just not as much as the other digital channels. Scott, I don't know if you want anything to add.

**Scott Boatwright** (Executives):
Yes. I think Delivery is still a huge growth channel, and we've seen a lot of growth over the last 3 quarters. But we're seeing a lot of progress with loyalty. I think loyalty comps are up over in-restaurant comps for the quarter. The relaunch has really paid huge dividends. We now have 24 million people in the Rewards program that are driving 33% of our transactions for the entire system. We think that number can move much higher. If you talk to Arlie, she'd tell you it should be in the 40%, 50% range and has aspirations and plans to get there. But there's a lot under the hood that's being worked on to continue to drive demand through the channel.

**Operator** (Operator):
The next question comes from Brian Bittner with Oppenheimer & Co.

**Brian Bittner** (Analysts):
It's interesting to hear that you're going to begin this catering rollout in the first quarter. Can you talk to us about what percentage of your markets you can scale the catering strategy to? Or should we actually be thinking of this as a national strategy? And can you give us an idea of the performance you've been seeing in these pilot markets that maybe give you the confidence to really get after this opportunity?

**Scott Boatwright** (Executives):
Yes. Thanks for the question. We think it's a really strategic opportunity for us. So it's more of a national rollout in the upcoming quarter, but we'll continue to add elements of the offering that will continue to have it scale and ramp for the consumer, whether that's third-party marketing, third-party delivery and/or the technology advancements we need to make to ensure we're load balancing correctly across restaurants. 
We think today -- so group occasions today represent 2% to 3% of sales. If you look at what some of our competitors in the space are doing upwards of 5%, 10% there, I'd say, 15% of total sales in Catering. We know there's an enormous opportunity. We're not trying to get to 15% tomorrow morning. What we'd like to do is see 1 or 2 points of growth year-over-year in the next couple of years, and we continue to ramp and scale. The goal here is to ensure we can deliver an incredible consumer experience and not disrupt the core business, which is priority #1 for us.

**Operator** (Operator):
I understand there is time for one last questioner, that will be Gregory Francfort with Guggenheim Securities.

**Gregory Francfort** (Analysts):
My question is just on international and maybe what you're seeing there. I think you called out kind of opening up 15 to 25 stores overseas next year. I'm not sure if you guys are willing to break out how many of those might be company-operated? And then kind of what sort of ramp maybe we should expect from there in the next couple of years?

**Scott Boatwright** (Executives):
Yes. So those 15 to 25 will be all partner-operated across the regions where we're open today. The 340 to 360 will be equity owned. So I think U.S., Canada and Western Europe. With some limited growth in Western Europe, we are now actively building a development pipeline there, which takes time, as you can imagine. So most of that growth will come through partner-operated. Alshaya Group in the Middle East, our Middle Eastern partner has really aggressive plans for growth there. We'll expand to Singapore in Q1 with our partner, SPC and then open up Mexico City early Q1 as well or Q1, Q2 of next year. So that's where the growth is coming. Can they go faster? Perhaps. It will really depend on what's going on with the conflict in the Middle East and how fast our partners in Latin America and Southeast Asia can get up to speed.

**Adam Rymer** (Executives):
Yes. And I would just add one thing on our company-operated in Europe. We continue to show better economics, and we actually had comps in the low double-digit range in Q3. I think we mentioned they were in the high single-digit range in Q2. So that is driving increased restaurant margins and our cash-on-cash returns in Central London and Frankfurt are still very attractive. So like Scott mentioned, we're going to continue to grow in those areas.

**Operator** (Operator):
This concludes our question-and-answer session. I would like to turn the conference back over to Scott Boatwright for any closing remarks.

**Scott Boatwright** (Executives):
Well, thank you for joining us today. I'm really proud of the progress our teams delivered in the third quarter. The 140,000 team members out in our restaurants that work so hard for us every single day to deliver an incredible experience to our support center staff here in Newport Beach and Columbus. 
We're in the early days of our Recipe for Growth strategy and believe much of the growth is still to come. And I think that's a really important note. And we've seen measurable progress across 2026 with positive transactions in every quarter. And we've seen promising results in multiple areas of the 5 pillars of our strategy. Looking forward, we're going to continue to build momentum in this dynamic environment, and many of our initiatives are in early stages of the rollout. 
As I said earlier, I know we have the right strategy and the right team and more growth levers in place today than any point in our history. And I'm confident in our ability to build Chipotle into a global iconic brand while creating long-term value for our guests, our teams and our shareholders. 
I think it's a really important note to say that we are still a category-defining brand that is the way people want to eat in the world today. And so I think that's an important note and that there's more growth in front of us than there is behind us. And if you're asking a question, are we still a growth brand, we absolutely are. We have industry-leading economics. We have incredible growth in front of us and an extraordinary team of professionals that are committed to our strategy. That said, I just want to say thank you for your continued support, your confidence in Chipotle, and we look forward to updating you on our continued progress next quarter.

**Operator** (Operator):
The conference has now concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CMG_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：CFO 表示全年同店銷售成長預期調整為低個位數區間（原話："expect full year comp sales growth in the low single-digit range"）
- 2026-07-29｜CFO｜guidance：CFO 給 Q3 同店約 +1%，並假設約 200bp 影響持續（原話："around a plus 1% in Q3, which does assume a continuation"）
- 2026-07-29｜CFO｜risk：CFO 說 7 月下半月出現約 200bp 的轉弱，與產業的 cyclospora 事件同時（原話："we did see a softening, call it about 200 basis points"）
- 2026-07-29｜CFO｜risk：CFO 提醒 Q3 的比較基期是今年最難的（原話："toughest lap that we have this year"）
- 2026-07-29｜CEO｜risk：CEO 說公司銷售受影響，但菜單不使用牽涉 cyclospora 的產品（原話："we are impacted from a sales perspective"）
- 2026-07-29｜CFO｜guidance：CFO 說 Q2 價格貢獻約 1.6%（原話："On pricing, the impact in Q2 was around 1.6%"）
- 2026-07-29｜CFO｜guidance：CFO 說全年價格貢獻預期落在先前 1%～2% 區間的高端（原話："we expect to land near the high end of the 1% to 2% range"）
- 2026-07-29｜CFO｜margin：Q2 餐廳層級利潤率 25.2%，年減 220bp（原話："Restaurant-level margin was 25.2%, down 220 basis points"）
- 2026-07-29｜CFO｜margin：Q2 銷貨成本率 29.7%，年增約 80bp（原話："were 29.7%, an increase of about 80 basis points"）
- 2026-07-29｜CFO｜margin：Q2 人力成本率 25%，年增約 30bp（原話："were 25%, an increase of about 30 basis points"）
- 2026-07-29｜CFO｜margin：Q2 其他營運成本率 14.9%，年增約 90bp（原話："were 14.9%, an increase of about 90 basis points"）
- 2026-07-29｜CFO｜guidance：Q3 銷貨成本率指引略低於 30%（原話："For Q3, we anticipate cost of sales to be just under 30%"）
- 2026-07-29｜CFO｜guidance：Q3 人力成本率指引在 25% 中段，工資通膨低個位數（原話："be in the mid-25% range with wage inflation in the low single-digit range"）
- 2026-07-29｜CFO｜guidance：Q3 其他營運成本率指引在 15% 中段（原話："For Q3, we anticipate other operating costs to be in the mid-15% range"）
- 2026-07-29｜CFO｜guidance：Q3 非 GAAP G&A 指引約 1.8 億美元（原話："G&A to be around $180 million on a non-GAAP basis"）
- 2026-07-29｜CFO｜guidance：全年有效稅率預估 24%～26%（原話："underlying effective tax rate will be in 24% to 26% range"）
- 2026-07-29｜CFO｜guidance：2026 折舊預期維持約占銷售 3%（原話："For 2026, we expect it to remain around 3% of sales."）
- 2026-07-29｜CFO｜margin：CFO 說價格與通膨的落差在上半年最大，Q3 起縮小，Q4 起預期兩者相當（原話："but from Q4 forward, we expect those 2 to match"）
- 2026-07-29｜CFO｜margin：CFO 預期 Q3 通膨約 3%，價格在 2% 中段（原話："in Q3, I would expect inflation to be closer to about 3%"）
- 2026-07-29｜CFO｜margin：CFO 將價格與通膨的落差描述為時間點因素，並說會續用滾動式調價（原話："That was really just a timing impact."）
- 2026-07-29｜CFO｜margin：CFO 說未來幾年可持續投入 Recipe for Growth 並對 G&A 取得槓桿（原話："we can continue to fuel our Recipe for Growth strategy and"）
- 2026-07-29｜CFO｜margin：Q2 同店成長 2.2% 含 1% 交易數成長（原話："including a transaction comp of 1%"）
- 2026-07-29｜CFO｜margin：Q2 調整後 EPS 0.33 美元，與去年持平（原話："per share was $0.33, flat to last year"）
- 2026-07-29｜CFO｜customer：數位銷售占比由 35.5% 升至 38.3%（原話："38.3% of total sales compared to 35.5% in the prior year"）
- 2026-07-29｜CFO｜capital_allocation：CFO 說 Q2 回購 6.31 億美元，董事會再增授權 13 億美元（原話："the Board authorized an additional $1.3 billion"）
- 2026-07-29｜CFO｜capital_allocation：Q2 回購金額與均價（均價 32.55 美元）（原話："$631 million in the second quarter at an average price"）
- 2026-07-29｜CEO｜commitment：CEO 維持今年約開 350 家公司自營餐廳（原話："expect to open approximately 350 restaurants this year"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說 350 家是團隊認可的開店速度，並提到超過可能的風險（原話："could possibly fracture the base if you get too aggressive"）
- 2026-07-29｜CEO｜capital_allocation：CEO 對 350 家的表態（原話："But I like 350 number. The team likes it."）
- 2026-07-29｜CFO｜capital_allocation：新店生產力與第二年現金投資報酬（原話："restaurant productivity has remained stable in the 80% range"）
- 2026-07-29｜CFO｜capital_allocation：第二年 cash-on-cash 報酬約 60%（原話："year 2 cash-on-cash returns continue to be around 60%"）
- 2026-07-29｜CFO｜capital_allocation：新店對既有店同店的淨影響約 100bp（原話："comparable restaurant sales is approximately 100 basis points"）
- 2026-07-29｜CFO｜commitment：CFO 說對北美至少 7,000 家的營運能力有信心（原話："our ability to operate at least 7,000"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說翻新方案處於階段性驗證，每店試投 10 萬至 30 萬美元（原話："think between $100,000 and $300,000 per"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說西歐續自營、其餘地區以合作夥伴營運（原話："own and operate Western Europe and grow from that base"）
- 2026-07-29｜CEO｜product：HEEP 設備目標年底約 2,000 家餐廳（原話："approximately 2,000 restaurants by year-end"）
- 2026-07-29｜CEO｜commitment：CEO 希望 2027 年內全系統完成 HEEP 安裝（原話："to have the entire portfolio completed sometime in 2027"）
- 2026-07-29｜CEO｜product：CEO 說 HEEP 餐廳尖峰 15 分鐘多出 2～3 份，並說對同店有數百 bp 的改善（原話："translating into hundreds of basis points of improvement in"）
- 2026-07-29｜CEO｜margin：CEO 說 HEEP 每日省 2～4 小時人力，並留在餐廳內再投資（原話："2 to 4 hours of efficiency depending"）
- 2026-07-29｜CFO｜product：CFO 說系統整體 max 15 約在 30 出頭至中段（原話："to mid-30s on our max 15 for each restaurant each day"）
- 2026-07-29｜CEO｜customer：店內交易使用 Rewards 的比例偏低，對比自有數位通路（原話："compared to nearly 90% of owned digital transactions"）
- 2026-07-29｜CEO｜commitment：CEO 說 8 月起試行店內免掃碼的 Rewards（原話："in-restaurant Rewards experience beginning in August"）
- 2026-07-29｜CEO｜customer：Rewards 活躍會員數（原話："With 23 million active members in our"）
- 2026-07-29｜CEO｜customer：CEO 引用品牌追蹤調查，說明價值認知改善（原話："Our affordability scores were better in Q2 than"）
- 2026-07-29｜CFO｜customer：CFO 說年輕與低收入族群改善幅度最大（原話："They really have improved the most"）
- 2026-07-29｜CEO｜competition：CEO 說 2026 年每個月都在搶市占（原話："we have taken share in each month of 2026"）
- 2026-07-29｜CEO｜product：CEO 說 LTO 重推有邊際遞減的可能（原話："think there's a point of diminishing returns"）
- 2026-07-29｜CEO｜product：CEO 說菜單創新量已為數年前的 4 倍（原話："ramped up innovation in menu 4x what it was"）
- 2026-07-29｜CEO｜product：下半年再推兩款限時蛋白質品項（原話："2 additional limited time protein options"）
- 2026-07-29｜CFO｜product：CFO 說 LTO 帶來的交易數提升多數在活動期間持續（原話："we typically see hundreds of basis points of trans lift"）
- 2026-07-29｜CFO｜product：CFO 將 LTO 描述為長期拉升 AUV 的槓桿（原話："we see this as a multiyear lever of increasing our AUVs"）
- 2026-07-29｜CEO｜commitment：CEO 說外帶團膳與 Build-Your-Own 占銷售 2%～3%，目標 2027 年全國推出（原話："national launch in 2027"）
- 2026-07-29｜CEO｜customer：團膳與 Build-Your-Own 目前占銷售比重（原話："represent 2% to 3% of sales today"）
- 2026-07-29｜CEO｜competition：CEO 說新品牌方向不是大轉彎而是 For Real 的演進（原話："it's not a 180 pivot. It's really the next evolution of what"）
- 2026-07-29｜CEO｜commitment：CEO 說新品牌訊息的第一批元素本季稍晚出現（原話："Later this quarter, we will begin to see the first elements of"）
- 2026-07-29｜CEO｜capital_allocation：歐洲各國同店達高個位數成長（原話："each country deliver high single-digit comp sales growth"）
- 2026-07-29｜CEO｜commitment：CEO 說墨西哥市場 2027 年擴展至墨西哥城（原話："Mexico City in 2027"）
- 2026-07-29｜CEO｜commitment：CEO 說今年開首爾店、新加坡接續（原話："Seoul, South Korea this year with Singapore"）
- 2026-07-29｜CEO｜risk：CEO 說中東近期發展取決於地緣政治（原話："near-term development remains dependent on geopolitical"）
- 2026-07-29｜CEO｜commitment：CEO 說計畫進入沙烏地阿拉伯市場（原話："enter the Saudi Arabian market in the near future"）
- 2026-07-29｜CFO｜risk：CFO 說世足賽對整體季度的影響不到 5bp（原話："the impact was less than 5 basis points"）
- 2026-07-29｜CEO｜commitment：CEO 說公司在規劃明年初的投資人活動（原話："we're working on a plan to gather many of the"）

### 問答異常語氣（迴避／改口／保留）
- CMG_Q2_2026_Earnings_Call_20260729.md｜問：Evercore（David Palmer）：如何確信 2027 年動能會增強、而非只是花很多錢換 1%～2% 同店｜答法：CEO 以 green shoots、早期證據、尚在早期等描述回應，沒有給 2027 的數字或量化指標
- CMG_Q2_2026_Earnings_Call_20260729.md｜問：UBS（Dennis Geiger）後 CEO 補述 cyclospora 對公司的影響｜答法：CEO 先說 not impacted，隨即改口 or we are impacted from a sales perspective，再說不涉入該事件
- CMG_Q2_2026_Earnings_Call_20260729.md｜問：Bernstein（Danilo Gargiulo）：餐廳翻新方案的增量資本支出規模與預期銷售提升｜答法：CEO 只給每店 10 萬至 30 萬美元的試驗區間，說 I have nothing to report today，未給 capex 總額與預期銷售提升
- CMG_Q2_2026_Earnings_Call_20260729.md｜問：Stephens（Jim Salera）：LTO 對交易數的貢獻比重與歷史基準｜答法：CFO 說未提供個別 LTO 的細節，改以定性描述與數百 bp 的區間回應，未給占整體交易的比重

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
{"date":"20260730","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"美國同店回到「價量同正」的正循環，且交易量成長可在 MCD／Taco Bell 三美元價格帶戰下維持（最關鍵的結構性假設——它決定 §11 該用複利尺還是成熟連鎖尺）"},{"id":"H2","text":"餐廳層營業利潤率在 FY2026 見底（H1 為 24.4%），並於 FY2028 前回到 26%+（成長兌現的操作性假設——三個成因裡兩個是自選、一個是外生循環）"},{"id":"H3","text":"Y5 之後的成長不必只靠北美開店：國際夥伴店與外燴／Build-Your-Own 構成可量化的第二曲線（估值修復的市場假設——市場願意給幾倍，取決於它相信不相信這條）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"成本橋比管理層說的長：牛肉／貨運通膨在 2027 再創新高，迫使菜單提價拉到 3%+，餐廳層利潤率結構性卡在 23-24%。管理層 Q2 明示「Q4 起價格與通膨對齊、之後不再有錯位」，但 USDA 自己的預估是 2027 育肥牛價 $254.25/cwt 高於 2026 的 $251.10、2026 產量 −1.8%、存欄 86.2 百萬頭仍在收縮"},{"id":"R2","text":"零和客流市場裡份額拿不夠：業界整體客流成長 &lt; 1%（Circana 2026），CAVA 客流 +6.8% 對 CMG 的 +1.0%；同時 MCD／Taco Bell 的三美元價格帶戰進入第三年，&lt; $40k 家戶年收入的客群外食頻次與單次消費雙降。CMG 被夾在「向下的價值戰」與「向上的高成長品類」之間"},{"id":"R3","text":"本輪最被前一份報告漏掉的一軸：勞動供給與法規成本的雙重收緊。美國餐飲廚師 37% 為外籍出生、2026 年全國工作場所執法約每日 900-1,000 件逮捕（橘郡 8 週產出損失約 $5,900 萬、洛杉磯部分商業區人流一度 −80%）；加州快餐委員會保留在 $20/小時之上加碼至多 $0.70/小時的裁量權且正在評估；USMCA 2026 聯合檢視期會影響墨西哥生鮮與酪梨的成本基礎。這一軸直接威脅 §7 execution 護城河的支柱（總經理流動率多年新低、HEEP 人工效率）——效率設備省下的工時，需要有人在崗才能被再投入"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"單一條件：餐廳層營業利潤率連 2 季 YoY 轉正（等價於絕對值連 2 季 ≥ 26.0%）——此一條件同時解除衰退燈、陷阱定性 🔴 與 PEG > 2.0 三個限制。價格回落至 $29.4 只降低進場成本、不解除限制。","irr_base_pct":10.3,"ev5y_pct":43.2,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🟠","ma":"❌","trap":"🔴","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.6,"ev5y_pct":43.2,"irr_base_pct":10.3,"max_dd_pct":-48.0,"bull_5y_price":71.5,"bear_5y_price":25.5,"p_bull_pct":20.0,"p_bear_pct":33.0,"rearm_trigger":"單一條件：餐廳層營業利潤率連 2 季 YoY 轉正（等價於絕對值連 2 季 ≥ 26.0%）——此一條件同時解除衰退燈、陷阱定性 🔴 與 PEG > 2.0 三個限制。價格回落至 $29.4 只降低進場成本、不解除限制。","price_at_dd":34.24,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMG_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
