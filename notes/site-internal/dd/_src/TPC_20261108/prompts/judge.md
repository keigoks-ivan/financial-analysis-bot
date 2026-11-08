你是 stock-analyst **v20 判斷 agent**，標的 TPC（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TPC","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":1720.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000077543/000007754326000218/tpc20261104ex991.htm"},"note":"StockStory 稱共識約 1.63B（單一聚合站來源，未獨立驗證）"},{"id":"f_kpi1_income_from_construction","label":"Income from construction operations (GAAP 營業利益)","value":125.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿（同上）"}},{"id":"f_kpi2_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":null,"period":"Q3 FY2026","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026","citation":"公司未揭露 non-GAAP 營業利益；僅揭露 adjusted diluted EPS"},"needs_sonnet":true},{"id":"f_kpi3_free_cash_flow_derived","label":"Free cash flow (derived)","value":291.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿：營業現金流 330.9 − capex 39.6；FCF 為自行推算，公司未報"}},{"id":"f_kpi4_share_based_compensation","label":"Share-based compensation","value":19.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿"}},{"id":"f_kpi5_guidance_fy2026_adjusted","label":"Guidance: FY2026 adjusted diluted EPS","value":"5.90–6.10","period":"Q3 FY2026 新聞稿（2026-11-04）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026 新聞稿（2026-11-04）","citation":"公司 Q3 2026 新聞稿"}},{"id":"f_kpi6_backlog","label":"Backlog","value":20353.3,"period":"Q3 FY2026（2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 新聞稿"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-03","period":"2026-11-03","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tpc_gross_margin_pct","label":"TPC 毛利率","value":11.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tpc_operating_margin_pct","label":"TPC 營業利益率","value":5.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tpc_fcf_margin_pct","label":"TPC FCF 利潤率","value":10.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gva_gross_margin_pct","label":"GVA 毛利率","value":16.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GVA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gva_operating_margin_pct","label":"GVA 營業利益率","value":7.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GVA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gva_fcf_margin_pct","label":"GVA FCF 利潤率","value":8.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GVA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_strl_gross_margin_pct","label":"STRL 毛利率","value":23.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_strl_operating_margin_pct","label":"STRL 營業利益率","value":18.62,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_strl_fcf_margin_pct","label":"STRL FCF 利潤率","value":10.93,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_gross_margin_pct","label":"PWR 毛利率","value":15.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_operating_margin_pct","label":"PWR 營業利益率","value":6.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_fcf_margin_pct","label":"PWR FCF 利潤率","value":8.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_gross_margin_pct","label":"FIX 毛利率","value":25.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_operating_margin_pct","label":"FIX 營業利益率","value":16.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_fcf_margin_pct","label":"FIX FCF 利潤率","value":19.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":89.89,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":8.69,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":65.12,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.38 → 5.38）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.07 → 6.07）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.38,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.07,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 5.38 → 5.38（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":34.18,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.76,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.65,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":16.71,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 5.38，分子＝快照價 89.89","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.3,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-634.34,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 476.71、現金 1111.05（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":52.61,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":4095.2,"period":"2026-11-08","unit":"USD m","basis":"市值 4729.54 ＋ 淨負債 -634.34","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6481.93,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（2 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":7338.17,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（4 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.63,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 89.89 / W52 78.74 / W104 58.97 / W250 31.14 / W250 13週斜率 3.67%"},{"id":"f_ma_w52","label":"52 週均線","value":78.74,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":58.97,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":31.14,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.67,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K 稱近年大型固定價格土木基建案競爭者減少，業主有時需努力吸引投標者；Civil 主要對手含 FlatironDragados、Kiewit、Lane、OHL USA、Skanska、Walsh。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm","excerpt":"We have seen diminished competition in recent years for large, fixed-price civil infrastructure projects as fewer firms have been pursuing such projects and customers have at times had to make concerted efforts to attract bidders.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：競爭激烈，失敗可能降低市占與利潤；漸進式設計建造趨勢可能增加競爭、壓低部分案件毛利。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm","excerpt":"If we are unable to compete successfully in such markets, our relative market share and profits could be reduced. In addition, evolving changes in the construction industry, such as the trend toward an increased use of the progressive design-build project delivery method that may reduce project risks for both owners and contractors, could result in increased competition and potentially lower margins on certain projects in the future.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"單一客戶（多專案，跨 Civil/Building/Specialty）占合併營收 2025 年 14.1%、2024 年 17.6%、2023 年 16.3%；2025 年另有第二大客戶占 11.4%，兩者合計約 25.5%。","source":"SEC EDGAR 10-K FY2025 Major Customers 附註","url":"https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm","excerpt":"Revenue from a single customer with multiple projects impacting the Civil, Building and Specialty Contractors segments represented 14.1%, 17.6% and 16.3% of the Company’s consolidated revenue for the years ended December 31, 2025, 2024 and 2023, respectively. Revenue from an additional customer with multiple projects, impacting the Civil, Building and Specialty Contractors segments, represented 11.4% of the Company’s consolidated revenue for the year ended December 31, 2025.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TPC 2026年Q1新增約6.7億美元訂單，3/31 backlog 198億美元，較年底小幅下降（訂單時點與大型專案執行）。","source":"TPC 8-K Q1 2026 earnings release (tpc20260506ex991)","url":"https://www.sec.gov/Archives/edgar/data/0000077543/000007754326000112/tpc20260506ex991.htm","excerpt":"The company booked approximately $670 million of new awards and contract adjustments in the first quarter of 2026, which resulted in a backlog of $19.8 billion as of March 31, 2026. As expected, backlog declined modestly compared to the end of 2025 due to award timing and the execution of major projects in backlog.","as_of":"2026-05-06","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TPC 管理層稱2027年調整後EPS將遠高於2026年指引上緣（4.90–5.30美元），並預期大量投標機會延續至2027年之後（管理層預測）。","source":"TPC 8-K Q1 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000077543/000007754326000112/tpc20260506ex991.htm","excerpt":null,"as_of":"2026-05-06","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"JLL 2026年中報告：資料中心需求至少強勁至2028年；JPMorgan估2027年規劃完工容量約60%尚未動工（產業背景，非TPC專屬）。","source":"BDC Network: Data center demand likely to be strong through at least 2028","url":"https://www.bdcnetwork.com/building-sector-reports/data-centers/article/55402995/data-center-demand-likely-to-be-strong-through-at-least-2028","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"ABC 稱資料中心榮景掩蓋整體經濟疲弱；FMI 對2027成長趨謹慎、可能2028起多年回升；ABC backlog 4月8.8個月為10個月高點，有資料中心業務者12.2個月 vs 無者8.3個月。","source":"Pulse/ABC Construction Backlog Indicator summaries","url":"https://contractorplus.app/blog/construction-backlog-indicator-april-2026","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：通膨與關稅曾使公司成本上升，且可能無法在固定價格、單價與 GMP 合約中完全回收；法規與關稅變動會影響材料或設備價格。2025 年國際營收 $489.7M（9%）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm","excerpt":"Economic factors, including inflation and tariffs, have also previously subjected us, and could in the future subject us, to higher costs, which we may not be able to fully recover in future projects that we are bidding","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"10-K MD&A：公司表示預期關稅不會造成重大衝擊，採事前（估價含成本上升、談判價格調整條款）與事後（鋼材、混凝土、大型設備提早買斷、固定價格分包）策略轉嫁風險。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm","excerpt":"Once the project is awarded, the Company’s strategy shifts to entering into purchase orders or “buy-outs” of materials, such as steel and concrete, as well as large pieces of equipment at the onset of projects, which mitigate the risk of future equipment and commodity price increases by passing that risk to vendors.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K：公司以發包後採購（steel、concrete buy-out）與固定價分包，把材料價格上漲風險轉給供應商／分包商；無單一地緣集中生產地，屬工程營造業態","source":"SEC Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm","excerpt":"Once the project is awarded, the Company's strategy shifts to entering into purchase orders or \"buy-outs\" of materials, such as steel and concrete, and enters into fixed-price contracts with its key project subcontractors whereby the risk of unforeseen escalation is transferred to the subcontractors.","as_of":"2026-02-28","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 國際（含美國屬地）營收 $489.7M、占 9%；政府客戶占積壓訂單 86%","source":"SEC Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm","excerpt":"derived $489.7 million, or 9%, of revenue from its work on projects in international locations, including U.S. territories","as_of":"2026-02-28","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 revenue 約$1,720.3M，年增22%；Civil +16%、Building +29%、Specialty Contractors +26%","source":"Tutor Perini 8-K Q3 2026 earnings release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000077543/000007754326000218/tpc20261104ex991.htm","excerpt":"Revenue for the Civil, Building, and Specialty Contractors segments for the third quarter of 2026 was up 16%, 29%, and 26%, respectively.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"2026年6月30日 backlog 組合約 Civil 50%、Building 35%、Specialty 15%","source":"Tutor Perini 10-Q Q2 2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000077543/000007754326000186/tpc-20260630.htm","excerpt":"mix of backlog by segment was approximately 50% for Civil, 35% for Building and 15% for Specialty Contractors","as_of":"2026-08-05","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 後上調2026調整後EPS指引至$5.15-$5.45，Civil利潤率預期12%-15%","source":"Barchart/StockStory Q2 2026 deep dive","url":"https://www.barchart.com/story/news/3693970/tpc-q2-deep-dive-margin-expansion-and-project-pipeline-drive-upbeat-outlook","excerpt":"2026 Adjusted EPS Guidance: Raised to $5.15-$5.45, up from $4.90-$5.30.","as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#none","axis":"substitute_technology","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q1 2026 電話會議：CEO 稱已在 specialty 端做部分資料中心工案並探索擴大，但對該熱門領域採謹慎、聚焦核心業務（無正式通路/商業模式轉換）","source":"Construction Dive, Tutor Perini Q1 2026 earnings data centers","url":"https://constructiondive.com/news/tutor-perini-Q1-2026-earnings-data-centers/819716/","excerpt":"it would be cautious in its approach to the high-flying sector while staying focused on its core business.","as_of":"2026-05-07","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q3 2026 新接案約 22 億美元、訂單出貨比連兩季大於 1.0x，在手訂單 204 億美元（屬專案組合，非通路轉變）","source":"Tutor Perini 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000077543/000007754326000218/tpc20261104ex991.htm","excerpt":"The Company booked approximately $2.2 billion of new awards and contract adjustments in the third quarter of 2026, a second straight quarter with a book-to-burn ratio greater than 1.0x, which resulted in backlog of $20.4 billion as of September 30, 2026.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 2026-11-04 發布 Q3 業績，將 2026 調整後 EPS 指引由 $5.15–5.45 上調至 $5.90–6.10。","source":"Panabee: Tutor Perini Raises 2026 EPS Guidance Amidst Operational Scaling（引 TPC Q3 2026 新聞稿）","url":"https://www.panabee.com/news/tutor-perini-earnings-q3-2026","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 調整後 EPS $1.83，StockStory 引 S&P 共識 $1.34（beat 36.6%）；營收 $1.72B 對共識 $1.63B。","source":"StockStory: Tutor Perini beats expectations in strong Q3 2026","url":"https://stockstory.org/us/stocks/nyse/tpc/news/earnings/tutor-perini-nysetpc-beats-expectations-in-strong-q3-2026","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-08 報導共識評等 Hold、共識目標價 $86.50（早於 Q3 財報；各聚合站分歧：StockAnalysis $113.25、TIKR $91.50、Benzinga $76 且未標日期）。11-04 後新共識未查到。","source":"MarketBeat: Tutor Perini updates FY 2026 earnings guidance (2026-08-05)","url":"https://www.marketbeat.com/instant-alerts/tutor-perini-nysetpc-updates-fy-2026-earnings-guidance-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月8-K共10份，僅1份含重大項目（2026-07-06 Item 1.01：發行$400M 6.625% 2033優先票據，用於贖回$400M 11.875% 2029票據）；屬再融資，非M&A／訴訟／監管事件","source":"SEC EDGAR 8-K 申報清單／8-K 2026-07-06","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000077543&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K附註所載WSDOT案已結案（2022年付款）；保險人案2024-09-30保密和解並於2024-10收款；未見近12個月新增重大訴訟","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm","excerpt":"As a result, the lawsuit between STP and WSDOT has concluded.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"證券集體訴訟僅見2008-2009年舊案（2009已駁回）；FY2025 10-K所載WSDOT案已結案","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm","excerpt":"As a result, the lawsuit between STP and WSDOT has concluded.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單中無Item 4.02（財報不可信賴）項目，僅1份含重大項目且為票據再融資","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000077543&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"TPC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.75,"operating_margin_pct":5.64,"fcf_margin_pct":10.75,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPC","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"GVA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.08,"operating_margin_pct":7.11,"fcf_margin_pct":8.36,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GVA","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"STRL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.78,"operating_margin_pct":18.62,"fcf_margin_pct":10.93,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PWR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.76,"operating_margin_pct":6.81,"fcf_margin_pct":8.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"FIX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.57,"operating_margin_pct":16.66,"fcf_margin_pct":19.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"TPC"},"financial_history":{"ticker":"TPC","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":3790755000.0,"revenue_yoy_pct":null,"gross_margin_pct":0.78,"operating_margin_pct":-5.4,"net_income":-210009000.0,"diluted_eps":-4.09,"free_cash_flow":147191000.0,"fcf_margin_pct":3.88,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":3880227000.0,"revenue_yoy_pct":2.36,"gross_margin_pct":3.62,"operating_margin_pct":-2.95,"net_income":-171155000.0,"diluted_eps":-3.3,"free_cash_flow":255518000.0,"fcf_margin_pct":6.59,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":4326922000.0,"revenue_yoy_pct":11.51,"gross_margin_pct":4.55,"operating_margin_pct":-2.4,"net_income":-163721000.0,"diluted_eps":-3.13,"free_cash_flow":466135000.0,"fcf_margin_pct":10.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5543039000.0,"revenue_yoy_pct":28.11,"gross_margin_pct":11.68,"operating_margin_pct":4.18,"net_income":80440000.0,"diluted_eps":1.51,"free_cash_flow":567211000.0,"fcf_margin_pct":10.23,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TPC/TPC_Q3_2026_Earnings_Call_20261104.md）

# Q3 2026 Earnings Call
**Tutor Perini Corporation** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Good day, ladies and gentlemen, and welcome to the Tutor Perini Corporation Third Quarter 2026 Earnings Conference Call. My name is Mike, and I will be your coordinator for today. [Operator Instructions]
As a reminder, this conference call is being recorded for replay purposes. I'll now turn the conference over to your host for today, Mr. Jorge Casado, Senior Vice President of Investor Relations. Please proceed.

**Jorge Casado** (Executives):
Hello, and thank you all for joining us. With us today are Gary Smalley, CEO and President; and Ryan Soroka, Executive Vice President and CFO. 
Before we discuss our results, I'll remind everyone that during this call, we will be making forward-looking statements, which are based on management's current assessment of existing trends and information. There is an inherent risk that our actual results could differ materially. You can find our disclosures about risk factors that could contribute to such differences in our Form 10-Q, which we are filing today and in our Form 10-K, which was filed on February 26, 2026. 
The company assumes no obligation to update forward-looking statements, whether due to new information, future events or otherwise, other than as required by law. In addition, during today's call, management will be referring to certain non-GAAP financial measures. You can find information and a reconciliation of these non-GAAP financial measures in our earnings release and in our Form 10-Q, both of which can be found in the Investors section of our website. 
Thank you. And with that, I will turn the call over to Gary Smalley.

**Gary Smalley** (Executives):
Thanks, Jorge. Hello, everyone, and thank you for spending time with us today. We delivered another quarter of outstanding results that featured record operating cash flow, revenue, operating income and earnings. Our consistent execution and continued backlog growth give us tremendous confidence and visibility into our ability to continue creating value for shareholders over the near and long term.
This marked our seventh consecutive quarter reporting outstanding results. Our operating cash flow for the third quarter and the first nine months of 2026 was up 14% and 16% year-over-year, respectively, each setting new all-time records with the third quarter result of $331 million, representing the largest of any quarter ever. Our record cash flow this year has been driven by higher volume, strong execution, record earnings and collections on various large projects that are very profitable. 
Our third quarter revenue was a record $1.7 billion, up 22% year-over-year, driven by contributions from various projects, most of which are in the early stages with significant scope of work remaining. As a result of our strong revenue growth and project execution, we generated record operating income of $125 million, which more than tripled compared to the same quarter last year, and we produced $0.39 of GAAP earnings per share and $1.83 of adjusted earnings per share, up 457% and 59%, respectively, compared to the third quarter last year. Ryan will delve into the details of our financial results shortly. 
Our operating margins were also outstanding. Our Civil segment's third quarter operating margin was a solid 14%. Our Building segment's operating margin was also strong at 5% with operating income that was nearly double that of the third quarter of last year. Our Specialty Contractors operating margin was 3.5% for the third quarter, up 130 basis points compared to the prior quarter margin and reflecting the continued margin expansion we have anticipated this year. 
We believe that the Specialty segment's margin will continue to improve as its electrical mechanical work ramps up on several of our large Civil and Building segment projects. Overall, we are extremely pleased with the continued upward trajectory of our business and the substantial revenue, earnings, margins and cash we are generating from our growing and profitable backlog. 
Let's turn to the details of our third quarter new awards and backlog. We booked an impressive $2.2 billion of new awards and contract adjustments, a solid book-to-burn of 1.3x and finished the quarter with a near-record backlog of $20.4 billion. 
The largest additions to backlog included $1 billion of additional work for a Civil segment project that includes a substantial amount of electrical and mechanical work to be performed by the Specialty Contractors segment, $577 million of new awards for several federal government projects for Perini Management Services, $145 million of new awards and additional funding for various military facility projects in the Indo-Pacific region for Black Construction, $126 million for various bridge projects in the Midwest for Lunda Construction, $108 million of additional funding for the Choctaw Casino and Resort Pocola renovation and expansion project in Oklahoma and $89 million of additional funding for several mass transit projects in California. 
As a reminder, our strong backlog, which includes nine mega projects totaling $16 billion of awarded value with significantly improved contractual terms that we have won over the past few years, continues to provide us with excellent visibility for future revenue, earnings and cash flow over the next several years. We expect that our backlog will continue to drive impressive revenue and earnings growth, solid profitability and strong cash flow in 2027 and beyond. 
We continue to have numerous significant project bidding opportunities, particularly in the Indo-Pacific region as well as in California, the Midwest, the Northeast and the Mid-Atlantic. Our massive pipeline of more than $200 billion in potential project opportunities over the next three to four years is broad geographically and diverse across end markets and about 3x larger than the pipeline we had just a couple of years ago. We expect that many of these opportunities will bid over the next year or two and are confident that we are well positioned to win our fair share of them. 
We remain highly selective and disciplined in our approach to bidding and winning new projects with our key objective being to maximize shareholder value. Our focus remains on bidding projects conservatively so that our project budgets reflect safe costs, adequate contingency, higher margins and favorable contractual terms that balance risks between us and our customers. We continue to see limited competition across the markets for the larger fixed price projects, which should help us win important and profitable contracts that will enable us to further grow our revenue and earnings and expand our margins. 
Now I'll review some of the specific bidding opportunities we are targeting this year and over the next couple of years. In the Indo-Pacific region, Black Construction continues to pursue more than $4.6 billion of federal opportunities, including major Wharf, Harbor, military and aviation projects across Guam, Palau, Yap, Wake Island and Tinian. In fact, we have submitted bids for three large projects in the region valued at nearly $1 billion for which we are awaiting the customer's decision.
In the U.S., we plan to bid on several multibillion-dollar infrastructure projects, including the initial contract for the Sepulveda Transit Corridor program in Southern California, a program believed to be valued at approximately $12 billion and expect to be awarded under multiple contracts as well as the Merced to Madera segment of the California High-Speed Rail project. 
We also have in Southern California, the $4 billion Southeast Gateway, the $2 billion East Side Transit Corridor Phase 2 and the $1.5 billion Sea Line extension to Torrance projects. 
On the East Coast, we will pursue the $3 billion Hudson Tunnel Systems and fit-out project in New York, the $3 billion Newark Liberty International Airport Terminal B project in New Jersey and the $1.2 billion Newark Bay Bridge project. Late next year or the following year, we expect to bid on the second phase of the multibillion-dollar Midtown Bus Terminal replacement project in New York, the phase that will demolish the existing bus terminal and build this permanent replacement.
Around the same time, we also plan to pursue a multibillion-dollar opportunity in Maryland for which we previously bid and had been selected in 2022, but the project did not move forward at that time. We're also targeting various new large healthcare hospitality and gaming opportunities, mostly in California and the Southwest. In addition to these numerous sizable pursuits, we continue to have certain Building segment projects currently in the preconstruction phase that are anticipated to advance to the construction phase later this year and over the next two years. 
Our massive pipeline of prospective opportunities, together with our experience and other competitive strengths give us confidence in our ability to drive backlog growth over the medium to longer term as we continue to focus on earnings growth, margin expansion, strong free cash generation, quality and safety. We are confident that these opportunities, along with our existing backlog will provide the catalyst for continued enhancement of shareholder value. 
Finally, let's turn to our outlook and guidance. As I mentioned earlier, we are extremely pleased with the financial results we have delivered thus far this year, results that were well ahead of our expectations. We continue to benefit from strong customer demand and favorable macroeconomic tailwinds. Our business is resilient through economic cycles and changes in the political environment, and we remain confident that our future is bright with the expectation for continued strong revenue and earnings growth. 
Because of the favorable outlook and our record financial results to date, driven by stronger-than-expected execution of our backlog and mitigation of previously identified project risks, we are raising our 2026 adjusted EPS guidance to the range of $5.90 to $6.10 per share, up from the previous range of $5.15 to $5.45. Importantly, our guidance continues to factor in contingency for unknown or unexpected outcomes and developments this year. 
We also continue to expect strong operating cash generation for the remainder of 2026 and beyond due to increasing project execution activities on our newer mega projects and the anticipated resolution of remaining legacy disputes. Looking to 2027 and based on our outlook and assessment of the current market, we continue to anticipate double-digit revenue and earnings growth as construction activities advance on many of our newer large projects in backlog. Thank you. And with that, I will turn the call over to Ryan to discuss the details of our financial results.

**Ryan Soroka** (Executives):
Thanks, Gary, and good day, everyone. I'll review our results for the third quarter, then provide commentary on our balance sheet and the assumptions related to our increased 2026 guidance. All comparative references will be against the third quarter of last year, unless otherwise stated. 
Gary mentioned, we generated $331 million of operating cash in the third quarter, up 14%, which set a new record as the highest result of any quarter ever. For the first nine months of 2026, operating cash flow was $665 million, up 16% compared to the first nine months of 2025 and the highest of any first nine months ever. 
The record cash flow was driven by higher revenue, outstanding project execution, record earnings and collections on various large projects that are very profitable as well as effective working capital management with only a negligible amount attributable to collections from legacy dispute resolutions. We expect to continue generating solid cash flow this year and beyond with most of our cash to be sourced from organic operations and occasionally enhanced by cash collected from dispute resolutions. 
Revenue for the third quarter of 2026 was a record $1.7 billion, up 22% and the highest of any quarter ever with the growth primarily due to increased project execution activities on certain higher-margin projects, including in the Northeast, California, Texas and the Indo-Pacific region. 
Civil segment revenue was $894 million, the segment's highest quarterly revenue ever and up 16% with the growth driven by increased project execution activities on the Midtown Bus Terminal Phase 1 project, the Manhattan Tunnel, the Manhattan Jail, the Kensico East View Connection Tunnel, the Honolulu Rail Project and the Apra Harbor Waterfront Repairs project in Guam, all of which have substantial scope of work remaining. 
Building segment revenue was $541 million, up 29%, primarily due to increased activities on the Brooklyn and Manhattan Jail projects in New York as well as on three large health care projects and a hospitality and gaming project in California. All of our major Civil and Building segment projects continue to run very smoothly. Specialty segment revenue was $286 million, up 26%, with the segment's growth continuing to be primarily driven by increased activities on various electrical and mechanical projects in New York and Texas. 
The strong revenue growth helped to drive our third quarter operating income to a record $125 million, up 213% year-over-year. Civil segment operating income was $125 million, up 26% compared to $99 million. The Civil segment continues to execute well and once again delivered a healthy segment operating margin of 14%, up from 12.9% in the third quarter of last year and running well within the 12% to 15% range we expect for the segment. 
Building segment operating income was $27 million, up 88% compared to $14 million with a strong increase driven by contributions from certain newer higher-margin projects in New York and California with substantial scope of work remaining. Segment's operating margin was 5%, up nicely compared to 3.4% in the third quarter of last year and also running well within the 3% to 6% margin range we expect for the segment. 
Specialty Contractors segment operating income was $10 million for the third quarter, up 64% compared to $6 million for the same quarter last year. The Specialty segment's operating margin was 3.5% this quarter, up from 2.7% in the third quarter last year. We are pleased with the Specialty segment's continued margin expansion this year, which has been primarily driven by contributions related to the increased volume on the New York and Texas electrical mechanical projects that I mentioned earlier. 
We expect to see further margin expansion as we continue toward our goal of eventually sustaining Specialty margins in the 5% to 8% range. Corporate G&A expense for the third quarter of 2026 was $37 million compared to $80 million last year, with a decrease largely due to a $40 million reduction in share-based compensation expense this year as some of the liability classified awards that previously caused elevated share-based compensation expense vested at the end of 2025. 
As a reminder, most but not all of the remaining liability classified awards will vest at the end of this year. So next year, we expect that our share-based compensation expense will be significantly reduced compared to this year. Other income was $16 million for the third quarter of 2026 compared to $7 million last year, with the increase primarily due to higher interest income earned on larger cash balances this year compared to last year. 
Interest expense for the third quarter was $7 million compared to $14 million last year, primarily due to the successful refinancing of our senior notes that we completed in July, which reduced the coupon rate of our senior notes from 11.875% to 6.625% and will save us $21 million in interest expense annually. We are now in a net interest income position and expect this trend to continue. We recorded two significant nonoperating adjustments in the third quarter of 2026 that we previously signaled would occur in the second half of this year. 
First, a $51 million loss on the extinguishment of debt tied to the recent successful refinancing we completed in early July, of which $16 million was noncash; and second, a noncash $34 million charge associated with the settlement of our former pension plan obligations. We terminated our pension plan because we wanted to eliminate future cash contributions and ongoing administrative expenses. 
Income tax expense for the quarter was $11 million, with a corresponding effective tax rate of 22.7% for the period compared to $15 million last year with a corresponding effective tax rate of 44.6% in that period. The lower effective tax rate this year is mostly attributable to the lower nondeductible share-based compensation expenses estimated for 2026 relative to 2025. Net income attributable to Tutor Perini for the third quarter of 2026 was $21 million or $0.39 of GAAP earnings per share, up more than 5x compared to $4 million or $0.07 of GAAP earnings per share in the third quarter of last year. 
Excluding the impacts of share-based compensation expense, the loss on extinguishment of debt and the pension settlement charge, net of all the associated tax benefits, adjusted net income attributable to Tutor Perini for the third quarter of 2026 was $98 million or $1.83 of adjusted earnings per share compared to $62 million or $1.15 of adjusted earnings per share in the same quarter last year. 
This was a 59% improvement in our adjusted EPS compared to last year's third quarter, reflecting the high-margin contributions and operational excellence we continue to see as we execute our projects backlog. 
Now I'll address the balance sheet. Our total debt stood at $404 million at the end of the third quarter. We ended the quarter with cash and cash equivalents exceeding total debt by $707 million, a very robust net cash position and $425 million better than we were one year ago. Our cash available for general corporate purposes was $504 million at the end of the third quarter of 2026, up 150% compared to the year ago level. 
In addition, our cost and estimated earnings in excess of billings, or CIE, as of September 30, 2026, was $767 million, the lowest balance since the end of 2014 and a decline of 9% compared to $848 million as of September 30, 2025, reflecting our significant continued progress in resolving and collecting on a reduced number of disputed matters. 
Our balance sheet has continued to strengthen throughout this year, and our sizable net cash position provides us with tremendous flexibility to allocate our capital efficiently and strategically. 
Lastly, let me update you on our latest assumptions related to our increased 2026 guidance. G&A expense for 2026 is expected to be between $380 million and $400 million. Depreciation and amortization expense is anticipated to be approximately $45 million in 2026, with depreciation at $43 million and amortization at $2 million. Interest expense for 2026 is now expected to be between $40 million and $42 million, of which about $3 million will be noncash. 
Our effective income tax rate for 2026 is expected to be approximately 26% to 29%. We now anticipate noncontrolling interest to be between $65 million and $75 million. We expect approximately 54 million weighted average diluted shares outstanding for 2026, and capital expenditures are anticipated to be approximately $125 million to $135 million, with the majority of the CapEx in 2026 or approximately $75 million to $85 million being owner-funded for large equipment items on certain large new projects. Thank you. And with that, I'll turn the call back over to Gary.

**Gary Smalley** (Executives):
Thanks, Ryan. To summarize, we delivered record financial results for the third quarter and through the first nine months of 2026, highlighted by the largest quarterly and first nine months of operating cash flow ever, record revenue that reflected strong double-digit growth, record operating income that was more than triple last year's third quarter results, solid segment operating margins, very strong earnings and continued backlog growth. 
As I mentioned earlier, this was the seventh consecutive quarter that we have reported extraordinary financial results. Our near-record backlog, together with the $200 billion-plus pipeline of project opportunities provides us with great confidence in our ability to deliver double-digit revenue and earnings growth and continued strong cash flow in 2027 and beyond. Our business trajectory has been and continues to be fantastic, and our results this year reflect strong operational performance and the excellent revenue, earnings and cash flow potential embedded in our backlog. 
Given our country's multi-decade history of underinvesting in its infrastructure, a trend that has finally begun to reverse in recent years, we expect that strong customer demand, favorable macroeconomic tailwinds and solid public and private customer funding will persist and continue to support an abundance of bidding opportunities well into the future. 
We firmly believe that Tutor Perini offers a compelling value proposition for investors, especially when you consider our record financial and operating performance to date, our near-record backlog, the massive pipeline of bidding opportunities over the next several years that should sustain our long-term success and the recent significant pullback in valuations across the stock market. 
We are confident in our future trajectory, which we believe will be propelled by the outstanding earnings and cash flow potential embedded in our backlog, and we expect to continue benefiting from generational investment opportunities to refresh and modernize the U.S. infrastructure. Thank you. With that, I will turn the call over to the operator for your questions.

**Operator** (Operator):
[Operator Instructions] 
Our first question is from Adam Thalhimer with Thompson Davidson Company.

**Adam Thalhimer** (Analysts):
Congrats on the strong Q3. I want to start off with data centers. I know you won two small jobs earlier this year. I'm just curious how much of a focus is that area for you going forward?

**Gary Smalley** (Executives):
Yes. Thank you, Adam. Look, you're right. We booked a couple of projects, about $70 million. If you look at the backlog that we have, that's data center related and that is not -- it's 0.2% of our backlog as of the end of September. So very negligible. However, having said that, we'll continue to look for selective and opportunistic opportunities. We have talented resources. There's a shortage of electricians to do the data center work. And the demand sometimes comes our way as it did with these projects, and there are a few more that appear that they might be in the pipeline. 
But look, with the just immense pipeline, and I mentioned the $200 billion plus of opportunities and the traditional infrastructure opportunities that we're used to pursuing and that we excel in. Data centers is not going to be a focus for us. Can we do the work? Sure, we can do the work. But why should we with all the opportunities we have in front of us in the more traditional work.

**Adam Thalhimer** (Analysts):
Got it. Okay. And then you said double-digit revenue growth next year. I'm curious, as you look out to revenue next year, how much of that sales is already in your Q3 ending backlog?

**Gary Smalley** (Executives):
Yes. Really a lot. I won't give you an exact percentage, but we'll say more than 3/4. So that's a very high percentage in our industry. In fact, I would say that if I look back at 2026 when we put the budget together for 2026, that was probably the highest level of certainty that I had seen in backlog in my career, and I've been doing this for 35 years in the industry. And 2027 is going to be similar in that we're going to have a very strong opportunity just to execute the work that we have and have this double-digit growth. 
Just a matter of how high a double-digit growth we have from our opinion because we think it's we have this visibility because of these huge awards that we booked in recent years, and that's going to go on for some time still. And some of that work has not fully kicked in, has it fully ramped up. So as that continues to ramp up and the work that is already ramped up continues to produce revenue margins and cash, then it's only going to improve from here.

**Adam Thalhimer** (Analysts):
Last one for me. Operating segment level operating margins have been great this year, particularly in Civil and in Building. Curious if you think that there is additional improvement possible over the next couple of years?

**Gary Smalley** (Executives):
Yes, there absolutely is. In fact, there could be improvement. I'm looking for improvement for 2027 really. We've talked internally, we've guided in the past certain margin ranges for the various segments. And I'll give you an example with Civil segment. We've been guiding 12% to 15% for the last few years. Going back a few more years ago, it was 8% to 10%, but we lifted that up as we saw the change in the landscape where we were getting work with better terms and the competition was diminishing. 
As I look forward, we're, what, 14%, I think, year-to-date right now in Civil. I think that as we go forward, I see upward pressure on that. So we've talked recently about maybe we shift that margin up a little bit, but I'd really rather wait a quarter or so just to make sure. But I see a very good chance that in the short term and as well as the medium term that we're going to see margin elevation, not just for Civil, but for the others as well. 
Building, it really depends more on a mix of things. Specialty, you can see that we really improved the margins again this quarter, about 3.5% and up, what, 50% or something like that from the second quarter. And that is a little short still where we want to be in the 5% to 8% range. I will tell you that the work that we're executing in Specialty right now, the newer work exceeds or at least meets that range. So we're very comfortable with the new work that we're generating. 
The reason the margins are not quite where we need them to be is because we still have some legacy things, really more minor on the Specialty side that come trickling through that we continue to settle. And sometimes where we settle that, sometimes it's at a profit, sometimes it's not. It's never material, but it does put a little bit downward pressure on the margin. So as those legacy items continue to rotate off, we'll continue to see margin expansion in Specialty and get into that 5% to 8% range sometime in 2027.

**Operator** (Operator):
Our next question is from Min Cho with Texas Capital Securities.

**Min Cho** (Analysts):
Congratulations on a really good quarter here. My first question has to do with the value of your bids outstanding that are awaiting awards. I think, Gary, you mentioned it's about $1 billion for Black Construction. But just curious how much you have out there across all of your businesses.

**Gary Smalley** (Executives):
Yes. So I mentioned Black. I said it was, as you mentioned, almost $1 billion. Just to put it in perspective, we have two in the region that we think we're well positioned for, and they're about $200 million each. And then we have another one that's just a little short of $600 million that also we feel that we're well positioned for. In addition to that, we've talked for some time a couple of years now about work that we have in preconstruction on the Building side and that work, usually, there's about a 97% to 99% likelihood that it manifests itself into backlog going forward. 
We have, over the next, call it, 12 to 15 months, we have another $0.75 billion roughly in that type work that we would expect to make its way to backlog. And then there are other things here and there and some of the other business units, but not to that magnitude. So somewhere around $2 billion of things that at any point in time could result in backlog, especially the Black work because that's been outstanding for some months, and we are hoping by now that we hear positive news on those things. But we'll continue to be patient. Things are moving in the right direction, and this will just make things even better when it hopefully comes our way.

**Min Cho** (Analysts):
Excellent. I know that Black Construction is a very important part of your business, tends to be smaller but very high margin. Can you talk a little bit about the capacity that you have there? If you do win these awards, are you able to kind of schedule work? I know that you were talking about growing this business. Just any update on the progress in terms of adding headcount there?

**Gary Smalley** (Executives):
Yes. We're in a constant recruiting mode along a variety of fronts, including there. Right now, we have capacity of the $4.6 billion of opportunity that we've talked about coming up in the next couple of years or so with $1 billion of that pending. We could probably hold right now $3 billion of that work or $3.5 billion maybe. But we are looking at putting more talent in Black. We have some things in the works. And in some cases, it's internal talent that would be moving there. So we're really excited about what Black offers. It is just a phenomenal operation. The $4.6 billion, that's only going to grow. The only reason it might not -- when we report it in the future, maybe you won't hear it growing because things will be going into backlog and it will be coming out of the pursuits, but there are going to be more and more pursuits.

**Min Cho** (Analysts):
Excellent. And then just a quick question for Ryan. Obviously, again, your operating margins have been very strong across all of your segments. When you look at just even the fourth quarter, should we expect margins, especially on the Civil side to come down a little bit due to seasonality? Or could we actually see it maintain kind of third quarter levels or even be up just based on the timing of the projects lapping?

**Ryan Soroka** (Executives):
Yes. I mean, look, from a forecast perspective, obviously, there's seasonality and then you think about the particularly strong winter that's expected with El Nino. So I think there's a little bit of headwind there. But at the same time, I think there's still opportunity to continue to perform. So if I'm trying to look at it sequentially, I think Q3 is a good barometer for Q4, and that could tick up or tick down just based on some of the impacts that we've talked about.

**Operator** (Operator):
Our next question is from Michael Dudas with Vertical Research Partners.

**Michael Dudas** (Analysts):
So Gary, you booked $16 billion in seven or eight large projects in an environment where the pipeline was much, much lower than it is today. As you look out the next three to four years, can you get a sense of how we can scope that given the limited competition and how confident and selective you are on some of these major bids that you have -- that you cited and some others I'm sure are going to come out over the next 6 to 18 months.

**Gary Smalley** (Executives):
Mike, we're confident we're going to get our share of what's out there. We think more than our share. There was a stretch where when we booked that $16 billion, that's made up of 9 projects, and I think it was something like we won 9 out of 12. I don't expect the same type of hit rate. But when you start to get the work, you can be a little bit more greedy in how you approach things. We bid this work at high margins. And then as time went on, higher margins and still higher margins, and that's really our approach. So we expect not that we won't win every one of them. 
But look, we're well positioned for a few very large programs that are coming out and some are accelerating beyond what we had expected. So we feel really good about building the backlog from here and building it in a profitable way.

**Michael Dudas** (Analysts):
Very helpful. And then Ryan, you've been generating a cash flow machine that you're driving over there. How is that going to help bid, I assume like you're going to be sole sourcing many of these bidding projects with surety support, et cetera, given your very strong financial profile. So many of these larger projects, I guess, Gary, you talked about that you won't be needing joint venture partners unless there's some technical aspects that you may want to see.

**Ryan Soroka** (Executives):
Yes, that's certainly the intent, obviously, with the cash balance at $1.1 billion as we sit here as of the end of September, that was certainly the intent is having that strength going into those bids and certainly approaching it to the extent that we can from a sole source perspective. From our perspective, that's a pretty good return, keeping that noncontrolling interest in-house.

**Operator** (Operator):
Our next question is from Liam Burke with B. Riley Securities.

**Liam Burke** (Analysts):
Could we get some color on preconstruction activity? You talked about it in previous quarters being pretty elevated. Has that past preconstruction activity rolled into backlog? Or is that something we could anticipate for 2027?

**Gary Smalley** (Executives):
Yes, Liam, the preconstruction activity, if you go back 2, maybe 2.5 years, something like that, over that period of time, when we first started talking about preconstruction activities, we put about $3 billion of that work into backlog. And I'll say that every prospect that was in preconstruction turned into backlog other than those that are still pending. And as I commented a few minutes ago, we still expect probably about $0.75 billion, so $750 million roughly over the next year to 15 months. And that will -- and maybe a year, 15 months, 18 months, something like that, that should come into backlog as well from preconstruction activities. 
Now what we're seeing also is now starting to see more opportunities of things going into preconstruction. So we'll start to replenish that a little bit. We've been working down a $4 billion, $4.5 billion amount for some time with little dribs and drabs going into preconstruction. I think we'll see more going into preconstruction. So after this 12-, 15-, 18-month period, we'll still have things that will be going into backlog from preconstruction. So the pipeline continues there, too.

**Liam Burke** (Analysts):
Great. And getting back to Specialty contracting, you talked about a little bit of external work, but very profitable work that you're doing for projects for Civil. Is there a capacity challenge that you see based on your opportunity pipeline?

**Gary Smalley** (Executives):
No. There are some shortages of electricians around the country in certain pockets, but we are very good with that right now. We are not facing any shortages there. And we don't anticipate having those issues. But at the same time, we're always trying to manage to make sure that we stay ahead of the curve. And with the work that we have, you're right, it's very profitable. The work that we have in-house that is supporting primarily Civil projects, but also Building projects. And then in some cases, it's third parties as well. Everything that has been awarded in the last two, three years is performing extremely well.

**Operator** (Operator):
Our next question is from Steven Fisher with UBS.

**Steven Fisher** (Analysts):
Just wanted to ask you about the black construction work. It sounds like some of that activity has been sort of in process for a while. Any particular uncertainties? Is it perhaps federal budget or anything that's holding that up? And then I guess, similarly, on the Civil side, curious what you're hearing from transportation agencies about kind of funding situation and whether uncertainties there about policy may be kind of holding up any or elongating the awards process?

**Gary Smalley** (Executives):
Yes. First part of your question, we're not anticipating well, there's a lot of work there. The biggest amount of work that's pending right now, there's some environmental reviews that need to be completed, and then that will allow those projects or this large particular project to be awarded. That region, the Indo-Pacific region is a very important part of our company and a growing part, as you know, following us over the past few years. But it's even more important to the country, to the United States. The Fed's Pacific Deterrence initiative and working with the federal government in this part of the world, these programs are not going to be derailed. They won't be defunded in any way, and it is something that both sides of the aisle agree upon the importance of it. So there may be some delays what we're seeing from time to time. And sometimes it takes government a while to make a decision. But this work is going to proceed. And as I mentioned just a few minutes ago, there's going to be more of it than the $4.6 billion we're tracking right now. And then on the second part of your question, could you repeat that again?

**Steven Fisher** (Analysts):
Just on the Civil side, what you're hearing from transportation agencies in terms of any particular uncertainties around funding and highway policy, et cetera, that may be holding up award?

**Gary Smalley** (Executives):
Yes, there's nothing holding up awards right now. Most of what we're doing, most of the funding is coming from the state and local level, and that's full steam ahead. On the federal side of things, what we have read and what we've heard is that there appears to be some momentum and maybe that momentum will increase based on the results of the midterms for a new transportation bill and additional funding. 
So we are in great shape if there is no more federal funding, but expecting that there will be some more, it's going to really just add to the outstanding position we have in the backlog that we currently have. We have not factored that into guidance in consideration of when we talk about '27 and double-digit growth. We're not assuming any additional funding coming from the Feds. But I would expect that, to be quite honest with you, and that should be another positive as we look at 2027 and beyond.

**Steven Fisher** (Analysts):
Great. And then just with the backlog that you have today, you mentioned earlier that you're still ramping up on some of these programs. Just curious if there's any way to frame when you think you'd hit a peak level of burn, just to kind of gauge when we might be able to start thinking about having some visibility to taking in some of the contingencies that you have. Do you think you'd still be ramping through all of 2027 and maybe you're not even going to hit kind of a full burn rate on these in 2028? I'm just curious how to kind of frame the duration of this ramp.

**Gary Smalley** (Executives):
Yes. I think if you look at what we currently have in backlog, then I would say that the peak is probably somewhere in 2028, maybe the latter part of 2028, something like that. But keep in mind that when you come off the peak, you just don't follow the nothing for the peak. It starts to wind down after the peak, if we were not to book anything else, after the peak is still going to be very good times for us. 
But certainly, between now and then, we're going to be booking other work, and that work is going to be profitable, and it's going to replace some of the work that burns off as well. So I wouldn't say that '28 would be a peak for the company that we would never be able to grow from. I'm just saying that based on the work that we have right now. But I would say we're going to continue to grow beyond '28 also. There's just too many opportunities, and we're so well positioned on too many of them for us not to continue to grow.

**Operator** (Operator):
We have reached the end of the question-and-answer session. I would like to turn the floor back over to Gary Smalley for closing comments.

**Gary Smalley** (Executives):
Thank you, everyone, for your interest and participation today. We look forward to continuing to deliver shareholder value, strong shareholder value and also reporting an eighth consecutive quarter of outstanding results when we speak to you again next time. Really excited about where this company is. We've come a long way over the last few years. A lot of you have been with us for a long time and waited for this story to develop. We appreciate your patience, and you can see the good things coming together now. 
And I keep saying that this is just the tip of the iceberg or make comments. There are a lot more good quarters to come. I really believe that as we continue to have this wonderful visibility into our future work, and we continue to even surpass our high expectations. So we hope to continue to create value and to demonstrate that your faith, confidence and patience with us was the right thing. So thank you again, and we'll talk to you soon.

**Operator** (Operator):
This concludes today's teleconference. You may disconnect your lines at this time. Thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TPC_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜Gary Smalley｜guidance：CEO 宣布上調 2026 年調整後 EPS 財測至 5.15–5.45 美元（原 4.90–5.30）（原話："we are raising our 2026 adjusted EPS"）
- 2026-08-05｜Gary Smalley｜guidance：管理層預期 2027 年盈餘高於 2026（原話："with even higher earnings expected in 2027, by which time"）
- 2026-08-05｜Gary Smalley｜guidance：管理層說財測內含大量不確定事項的準備金（contingency）（原話："As usual, our guidance continues to factor in a significant"）
- 2026-08-05｜Ryan Soroka｜guidance：CFO 更新 2026 有效稅率假設為 26%–29%（原話："Our effective income tax rate for 2026 is now expected to"）
- 2026-08-05｜Ryan Soroka｜guidance：CFO 維持 2026 資本支出 1.25–1.35 億美元的預期（原話："capital expenditures are still anticipated to be"）
- 2026-08-05｜Ryan Soroka｜guidance：CFO 說下半年營運現金流不會再創紀錄（去年全年 7.5 億美元），可能是史上第二佳（原話："we're not going to set a new record."）
- 2026-08-05｜Ryan Soroka｜guidance：CFO 說 2027 年股權報酬費用預期大幅下降（原話："we expect that our share-based compensation expense will be"）
- 2026-08-05｜Ryan Soroka｜margin：Civil 部門營業利益率 15.3%，CFO 說高於 12%–15% 預期區間上緣（原話："above the top end of the 12% to 15% margin range we expect"）
- 2026-08-05｜Ryan Soroka｜margin：CFO 拆解 Civil 去年同期營業利益含 2,800 萬美元有利調整，今年營業利益 1.25 億對去年 1.40 億（原話："large favorable adjustment of $28 million."）
- 2026-08-05｜Ryan Soroka｜margin：Building 部門利益率 5.6%，接近 3%–6% 預期區間上緣（原話："upper end of the 3% to 6% margin range we expect for the"）
- 2026-08-05｜Ryan Soroka｜margin：Specialty 部門長期利益率目標 5%–8%（本季 2.2%）（原話："eventually sustaining specialty margins in the 5% to 8%"）
- 2026-08-05｜Gary Smalley｜margin：CEO 說 Civil 利益率區間的歷史演進：先前講的是 8%–12%（原話："too long ago, we were talking about 8% to 12% margin."）
- 2026-08-05｜Ryan Soroka｜margin：調整後 EPS 口徑：排除股權報酬費用（扣除相關稅務利益）（原話："Excluding the impact of share-based compensation expense,"）
- 2026-08-05｜Ryan Soroka｜margin：CFO 說上半年現金流中僅小部分來自爭議和解（原話："with only a small amount attributable to dispute"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 預期九大專案至少以承接時利潤率交付，並預期後期可釋放準備金增加利潤（原話："deliver those projects at least at the as-sold margins."）
- 2026-08-05｜Gary Smalley｜commitment：CEO 稱大型專案內含的利潤高於目前認列（原話："more profit, we believe, in those projects than what we're"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 說投標與承接維持紀律、不為充實積壓訂單而接案（原話："We're not going to try to book projects just because we"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 表示現金運用將保守（原話："be conservative in how we administer the cash"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 預期 Building 預建階段專案將於第三、四季及 2027 年轉入積壓訂單（原話："it's greater than 90% hit rate"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 預期年內 Midtown 公車總站專案再獲約 10 億美元資金（原話："We still anticipate approximately $1 billion of additional"）
- 2026-08-05｜Gary Smalley｜capital_allocation：季股利由 0.06 升至 0.09 美元（+50%）（原話："increase compared to the previous $0.06 dividend."）
- 2026-08-05｜Gary Smalley｜capital_allocation：管理層預期未來再做機會性庫藏股買回（授權餘額 1.7 億美元）（原話："we expect to make additional opportunistic share buybacks"）
- 2026-08-05｜Ryan Soroka｜capital_allocation：CFO 列出現金用途順序：機會性買回、股利、再投資與保證人支持，最後是併購（原話："the last component would really be M&A"）
- 2026-08-05｜Gary Smalley｜capital_allocation：CEO 解釋保留大量現金是為取得保證人核准、單獨承接大案而不必與合資夥伴分潤（原話："We like to pursue projects without joint ventures as much"）
- 2026-08-05｜Gary Smalley｜capital_allocation：CEO 說股利與回購對公司是新事物（原話："We haven't paid a dividend in some time."）
- 2026-08-05｜Ryan Soroka｜capital_allocation：7 月再融資：以 6.625% 新票據取代 11.875% 票據，到期延至 2033（原話："annual cash interest savings of $21 million going forward."）
- 2026-08-05｜Ryan Soroka｜capital_allocation：循環信貸額度重訂，未動用額度由 1.7 億增至 3.5 億美元、到期延至 2031（原話："We also amended and restated our revolving credit facility,"）
- 2026-08-05｜Ryan Soroka｜capital_allocation：淨現金口徑：現金減總負債為 5.42 億美元（原話："We ended the quarter with cash and cash equivalents"）
- 2026-08-05｜Gary Smalley｜customer：季末積壓訂單 199 億美元，近歷史高點，較上季略增（原話："record backlog of $19.9 billion, up slightly compared to"）
- 2026-08-05｜Gary Smalley｜customer：CEO 稱潛在機會管線逾 2,000 億美元，約為數年前三倍（原話："we have a massive pipeline of more than $200 billion in"）
- 2026-08-05｜Gary Smalley｜customer：九大巨型專案合計約 160 億美元，為未來營收能見度來源（原話："backlog, which includes 9 mega projects we have won over"）
- 2026-08-05｜Gary Smalley｜customer：CEO 希望擴大 Black Construction（關島）規模，視得標率與機會而定（原話："We certainly would like to double it."）
- 2026-08-05｜Gary Smalley｜product：資料中心業務僅追求電氣面、以德州電工短缺處有餘力承接為主，並強調仍以核心業務為重（原話："electricians are short, but we have the available capacity"）
- 2026-08-05｜Gary Smalley｜competition：CEO 重申大型固定價格案競爭有限（原話："we continue to see limited competition for the larger fixed"）
- 2026-08-05｜Gary Smalley｜competition：被問到區域業者回歸時，CEO 重申先前說法並提及得標紀錄（原話："We won 9 out of 11."）
- 2026-08-05｜Gary Smalley｜risk：被問通膨風險，CEO 說非巨型案也用預購（buydown）與合約條款保護（原話："There's also contractual terms that many times protect us"）
- 2026-08-05｜Gary Smalley｜risk：CEO 強調多項專案的「剩餘舊爭議」現金流預期仍在，且收入認列採保守原則（原話："the anticipated resolution of remaining legacy disputes."）

### 問答異常語氣（迴避／改口／保留）
- TPC_Q2_2026_Earnings_Call_20260805.md｜問：Steven Fisher：區域業者似乎回歸大型案，是個案還是更廣泛趨勢？｜答法：CEO 未直接評論區域業者是否回歸，改重申『競爭有限』並談得標紀錄（9/11、此前 0/4~0/5）與管線規模
- TPC_Q2_2026_Earnings_Call_20260805.md｜問：Michael Dudas：淨現金組成、營運資金需求、保證人（surety）定位如何支持積壓訂單成長？｜答法：CFO 只答下半年現金流與資本配置順序，未給營運資金需求或保證額度的數字

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
{"date":"20260525","verdict":"B 衛星候選","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Adj EBITDA margin 從 5% → 8-9% 結構改善持續","columns":{"2Y 驗證":"FY26-27 Adj EBITDA margin 連 4 季 ≥ 7.5%","5Y 驗證":"FY28-30 達 mid-cycle 9-10%","10Y 驗證":"結構持平於 9-10% mid-cycle","數字門檻":"FY26 全年 ≥ 8.0%（mgmt guide mid）","來源":"mgmt FY26 guide $4.90-5.30 隱含 Adj EBITDA $470M / Rev $6.27B = 7.5%","漂移觸發條件":"連 2 季"}},{"id":"H2","text":"Backlog 持續創高 + mega-project 連續中標","columns":{"2Y 驗證":"Backlog 維持 $19B+ rolling 4Q","5Y 驗證":"Backlog $22B+ by FY30 Q4","10Y 驗證":"Civil + Building 雙引擎結構升級","數字門檻":"book-to-bill ≥ 1.0 rolling 4Q + 每年至少 2-3 個 mega-project win","來源":"Q1 26 法說：「9 mega-project win 過去 1-3 年」","漂移觸發條件":"連 2 季 book-to-bill"}},{"id":"H3","text":"Ronald Tutor 18M 退出 + 估值倍數修復（trap 🟡 → 🟢）","columns":{"2Y 驗證":"2027 Q3 前 Tutor 完成主要持股賣出 + Fwd PE 修復至 15-17x","5Y 驗證":"FY29 Fwd PE 達 18x mid-cycle","10Y 驗證":"機構持股比例升至 90%+","數字門檻":"2027 Q3 法說期間 confirmed Tutor 持股","來源":"Form 4 / 13D 公告","漂移觸發條件":"Tutor 退出進度落後（2027 Q3 仍 > 8% 持股）→ trap 🟡 持續"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Ronald Tutor 18M 計畫退出觸發機械性賣壓","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Form 4 賣出量 + 股價短期 panic","警戒閾值":"單次 > 1M 股賣出 + 股價 -15% 急跌 → 視 fundamentals 決定加碼 / 觀望"}},{"id":"R2","text":"新一輪 mega-project cost overrun + 法律 disputes（重演 2018-2023 噩夢）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"任一 mega-project cost overrun 公告 + Adj EBITDA margin 連 2 季崩","警戒閾值":"任一 cost overrun > $200M 公告 且 Adj EBITDA margin 連 2 季崩 50bp+ → 反轉，重評持倉"}},{"id":"R3","text":"聯邦 budget 不確定 / Trump admin 削減大型基建 spend","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"federal infrastructure 撥款進度 + Trump admin 行政命令","警戒閾值":"FY27 federal civil spend YoY"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":72.76,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
