你是 stock-analyst **v20 判斷 agent**，標的 COHR（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"COHR","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":2370.3,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 Q1 FY27（GlobeNewswire 2026-11-04，finviz 轉載全文）"},"note":"查無（本次未取得可靠共識營收數字）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":23.2,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"%（營業利益 550.3 百萬美元）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 Q1 FY27（GlobeNewswire 2026-11-04，finviz 轉載全文）"},"note":"查無"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":15.9,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"%（營業利益 377.9 百萬美元）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 Q1 FY27（GlobeNewswire 2026-11-04，finviz 轉載全文）"},"note":"查無"},{"id":"f_kpi5_guidance_q2_fy2027_non_g","label":"Guidance: Q2 FY2027 營收／non-GAAP EPS","value":"營收 2,550–2,750 百萬美元；non-GAAP 毛利率 40%–42%；non-GAAP 營業費用 430–450 百萬美元；non-GAAP 稅率 18%–20%；non-GAAP EPS 2.28–2.48","period":"Q1 FY2027 新聞稿（公告於 2026-11-04）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027 新聞稿（公告於 2026-11-04）","citation":"公司新聞稿 Q1 FY27（GlobeNewswire 2026-11-04，finviz 轉載全文）"},"note":"媒體稱優於華爾街預期（technews 2026-11-05），具體共識數字查無"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cohr_gross_margin_pct","label":"COHR 毛利率","value":38.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_operating_margin_pct","label":"COHR 營業利益率","value":14.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_fcf_margin_pct","label":"COHR FCF 利潤率","value":-23.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lite_gross_margin_pct","label":"LITE 毛利率","value":45.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lite_operating_margin_pct","label":"LITE 營業利益率","value":23.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lite_fcf_margin_pct","label":"LITE FCF 利潤率","value":9.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cien_gross_margin_pct","label":"CIEN 毛利率","value":44.07,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cien_operating_margin_pct","label":"CIEN 營業利益率","value":14.12,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cien_fcf_margin_pct","label":"CIEN FCF 利潤率","value":13.53,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_aaoi_gross_margin_pct","label":"AAOI 毛利率","value":28.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAOI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_aaoi_operating_margin_pct","label":"AAOI 營業利益率","value":-10.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAOI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_aaoi_fcf_margin_pct","label":"AAOI FCF 利潤率","value":-100.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAOI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtsi_gross_margin_pct","label":"MTSI 毛利率","value":57.13,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mtsi_operating_margin_pct","label":"MTSI 營業利益率","value":18.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mtsi_fcf_margin_pct","label":"MTSI FCF 利潤率","value":9.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_free_cash_flow_capex","label":"Free cash flow (營業現金流 − capex，自行推算，新聞稿未直接揭露)","value":-868.2,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿現金流量表：營業現金流 -92.7、PP&E 增加 -775.5"},"note":"查無"},{"id":"f_kpi4_sbc_non_gaap","label":"SBC 占 Non-GAAP 營業利益 %","value":13.3,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"%（SBC 73.2 百萬美元；占營收 3.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 Q1 FY27；比率為 73.2/550.3 自行推算"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":192.81,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-42.49,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":37.16,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.42 → 9.42）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.97 → 13.97）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.13 → 19.13）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":9.42,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":13.97,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":19.13,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-0.42,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 9.46 → 9.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":39.92,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝44.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":44.1,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.13,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝41.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":41.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":20.47,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 9.42，分子＝快照價 192.81","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":2592.05,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 4346.98、現金 1754.93（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":196.96,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":40567.65,"period":"2026-11-08","unit":"USD m","basis":"市值 37975.6 ＋ 淨負債 2592.05","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":11163.49,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":15504.21,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.63,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 192.81 / W52 271.08 / W104 181.49 / W250 105.98 / W250 13週斜率 2.2%"},{"id":"f_ma_w52","label":"52 週均線","value":271.08,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":181.49,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":105.98,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.2,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2026 風險因素：公司承認可能面臨更激烈競爭，且可能誤判客戶或競爭對手向後整合、取代公司的意願與能力；未量化份額消長。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"We may encounter increased competition, and we may fail to accurately estimate our competitors’ or our customers’ willingness and capability to backward integrate into our competencies and thereby displace us.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 稱公司致力於擴大終端市場份額，但不保證能達成，且客戶要求可能導致市占流失。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"We continue to make investments in programs with the goal of gaining a greater share of end markets, including the key components for fast growth markets. We cannot guarantee that our investments in capital and capabilities will be sufficient.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"FCC 考慮禁止中國來源光收發模組，Innolight 全球份額約 27%，Coherent 與 Lumentum 可能受益（單一來源報導）。","source":"borecraft 2026-08-04","url":"https://borecraft.com/2026/08/04/the-fcc-mulls-banning-china-sourced-optical-transceivers-threatening-innolights-27-global-market-share-as-coherent-and-lumentum-prepare-to-pounce/","excerpt":"The FCC Mulls Banning China-Sourced Optical Transceivers, Threatening Innolight’s 27% Global Market Share As Coherent And Lumentum Prepare To Pounce By NewMaxx / August 4, 2026","as_of":"2026-08-04","retrieved_at":"20261108","affects":["moat_trend","triggers"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"HyperLight 薄膜鈮酸鋰調變器新進者威脅範圍有限，主要競爭收發引擎一部分而非 InP 雷射本身。","source":"marketanalysis.com HyperLight threat","url":"https://marketanalysis.com/the-hyperlight-threat-to-coherent-and-lumentum-ends-where-indium-phosphide-begins/","excerpt":"The HyperLight Threat to Coherent and Lumentum Ends Where Indium Phosphide Begins June 19, 2026 HyperLight’s $80 million Series C arrives with a clean narrative: a foundry-aligned thin-film lithium niobate pure-play, freshly funded by MediaTek, UMC, Jabil, and Foxconn, attacking the modulator layer of the optical stack at the precise moment AI","as_of":"2026-06-19","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"中文報導稱 Innolight 將拿下 2027 年 2.4T 新世代約 60–70% 量，Coherent 約 20–30 萬件（單一來源估計）。","source":"36kr","url":"https://eu.36kr.com/en/p/3983266637118208","excerpt":"Coherent's share ranks steadily among the top overseas manufacturers. The next-generation 2.4T track is dominated by Google's demand. The total industry shipment is expected to be 1-2 million units in 2027. Domestic leading player Innolight will take 60%-70% of the share, and Coherent will take 200,000-300,000 units.","as_of":"2026-09-15","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"非獨立 bear-case 研究頁稱某大客戶約占 D&C 營收 25–35%，並提及 NVDA 可能於 CY2028+ 自製 CPO 光源雷射（未核實）","source":"cohr-research.pages.dev bear case","url":"https://cohr-research.pages.dev/07_thesis/bear_case","excerpt":null,"as_of":"2026-11-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 10-K：一家主要客戶占合併營收 20%（FY2025、FY2024 各 10%），第二大客戶占 12%；主要來自 Datacenter & Communications 部門。","source":"SEC EDGAR 10-K FY2026 Item 8 Major Customers","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"One major customer accounted for 20%, 10%, and 10% of consolidated revenue during fiscal 2026, 2025 and 2024, respectively. A second major customer accounted for 12% of consolidated revenue during fiscal 2026.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 風險因素：兩家客戶在 FY2026 各占營收逾 10%，預期集中度將持續。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"A small number of customers have consistently accounted for a significant portion of our revenues, with two customers each contributing more than 10% of total revenues in fiscal 2026.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"管理層5月稱有望於本曆年底把內部InP產能翻倍（較原計畫提前一季），2027年底再翻倍以上；InP為主要供給瓶頸（組裝測試不受限）","source":"Coherent FY26 Q3 earnings call 摘要（搜尋結果彙整）","url":"https://www.insidermonkey.com/blog/coherent-inc-nysecohr-q3-2026-earnings-call-transcript-1756968/","excerpt":null,"as_of":"2026-05-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FQ3 紀錄訂單與在手訂單延伸至2028；資料中心與通訊占營收75%（去年同期65%）；FQ2 資料中心 book-to-bill 超過4倍；長約延伸至本十年底；幾乎所有資料中心產品線供給受限","source":"Zacks/Nasdaq 摘要（搜尋結果彙整）","url":"https://www.nasdaq.com/articles/ai-infrastructure-demand-reshaping-coherents-growth-story","excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"FQ4 capex 5.56億美元（去年同期1.31億）；Zacks指出現金轉換偏弱、多項ramp重疊；工業部門疲弱","source":"Zacks/Nasdaq 摘要（搜尋結果彙整）","url":"https://www.nasdaq.com/articles/ai-infrastructure-demand-reshaping-coherents-growth-story","excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY2027訂單基本已滿；無CPO延遲","source":"Webull 轉述 Coherent Q4 法說","url":"https://www.webull.com/news/15393555909010432","excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lumentum CEO稱InP短缺將比記憶體更嚴重","source":"Tom's Hardware","url":"https://www.tomshardware.com/tech-industry/semiconductors/lumentum-ceo-says-the-indium-phosphide-shortage-will-become-worse-than-memory","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K Item 3：公司涉及業務附帶的各類索賠與訴訟，管理層諮詢法律顧問後認為最終責任不會對財務狀況、流動性或經營結果造成重大影響；未列反壟斷調查。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"The Company and its subsidiaries are involved in various claims and lawsuits incidental to its business. The resolution of each of these matters is subject to various uncertainties, and it is possible that these matters may be resolved unfavorably to the Company.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：美國對半導體、關鍵礦物及衍生電子產品啟動 Section 232 調查，可能新增關稅；公司在美國與海外製造採購，自認可能比國際化程度低的企業更易受影響；並提及 AI／資料中心相關產品可能出現新出口管制。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"In addition, the U.S. government has initiated investigations under Section 232 of the Trade Expansion Act of 1962 to evaluate whether additional tariffs may be necessary on certain commodities, including semiconductors, critical minerals, and derivative electronics products, on national-security grounds","as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：美國政府持續擴充實體清單，已對公司營收及銷售能力造成不利影響；若出口管制在產能與採購承諾後加嚴，可能需認列庫存與不可取消採購義務的鉅額費用。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"The U.S. government may continue to add companies to its restricted entity list and/or technologies to its list of prohibited exports to specific countries, which have had and may in the future have an adverse effect on our revenue and our ability to sell our products.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K MD&A：2026-02-20 最高法院判 IEEPA 關稅無效；公司為進口記錄人，FY2026 Q4 認列退稅，金額不重大；公司稱全球製造佈局有一定緩解能力。","source":"SEC EDGAR 10-K FY2026 MD&A","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"The amounts recorded were not material to the Company.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Coherent 2023 評估中國鎵、鍺出口限制：預期影響極小或無，理由為庫存充足且可從中國以外取得（2023 資料，未反映 2024-25 升級）","source":"Coherent Corp. press release: Coherent Corp. Provides Initial Assessment Of Expected Export Restrictions Of Gallium And Germanium From China","url":"https://coherent.com/news/press-releases/coherent-corp-initial-assessment-expected-export-restrictions","excerpt":"Coherent Corp. expects minimal to no impact from the upcoming export restrictions of gallium and germanium from China due to its ample inventories and ability to source these materials outside of China.","as_of":"2023-07-04","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國對美鎵鍺銻出口禁令於 2025-11-09 暫停，期限至 2026-11-27（Fastmarkets、CIRS 報導）；與 COHR 的直接關聯未見公司揭露","source":"Fastmarkets: China suspends export prohibition on gallium, germanium, antimony, superhard materials to US","url":"https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us","excerpt":null,"as_of":"2025-11-10","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"產業層面：磷化銦(InP)基板供應集中，中國出口管制使供應不確定（IQE CEO 說法）；未找到 Coherent 自身 InP 採購揭露","source":"TheNextWeb: China has 70% of a material AI needs, IQE's CEO warns, Bloomberg reports","url":"https://thenextweb.com/news/iqe-indium-phosphide-china-export-controls-supply-risk","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Coherent 於 FY2021 關閉中國南京與美國 Tucson 營運，產品與組件移往新加坡與馬來西亞製造（舊年度 10-K，非現況）","source":"Coherent Inc 10-K FY2021","url":"https://www.sec.gov/Archives/edgar/data/21510/000002151021000060/cohr-20211002.htm","excerpt":null,"as_of":"2021-10-02","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026（截至2026/6/30）總營收年增23%至71.18億美元；Datacenter & Communications 段增40%（+15.19億），由AI資料中心需求帶動","source":"Coherent FY2026 Form ARS (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000820318/000110465926114851/tm264290d2_ars.pdf","excerpt":"Revenues increased $1,519 million, or 40%, in the Datacenter & Communications segment. Revenue growth in our Datacenter business was fueled by continued strong AI datacenter demand while our Communications business benefited from increased demand in data center interconnect, scale across and traditional telecom applications.","as_of":"2026-09-30","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"FY2026 Industrial 段營收年減10%（-2.11億），主因出售航太國防與慕尼黑業務","source":"Coherent FY2026 Form ARS (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000820318/000110465926114851/tm264290d2_ars.pdf","excerpt":"In the Industrial segment, revenue decreased $211 million, or 10%, primarily due to the divestitures of our aerospace and defense business on September 2, 2025 and our Munich, Germany business on January 30, 2026.","as_of":"2026-09-30","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Industrial 在 Q4 FY2026 與全年 pro forma 大致持平；半導體與顯示設備需求季增年增，管理層預期後續季度由半導體資本設備帶動成長（二手摘要）","source":"Futurum, Coherent Q4 FY 2026 Earnings","url":"https://futurumgroup.com/insights/coherent-q4-fy-2026-earnings-1-6t-transceivers-ramp-cpo-revenue-approaches/","excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026/2 Q2財報電話會議：CEO稱需求訊號顯示日曆年內工業業務成長回升，由半導體設備客戶強勁訂單領動","source":"Motley Fool Q2 FY2026 call transcript","url":"https://www.fool.com/earnings/call-transcripts/2026/02/04/coherent-cohr-q2-2026-earnings-call-transcript/","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"市場規模：TrendForce 估 AI 光收發模組市場2026年約260億美元；2026–2027為1.6T供應鏈卡位關鍵期；市占數字各家方法不一，Coherent 與 Innolight 收發模組營收約相當（次級來源，未核）","source":"iconnect007, Global AI Optical Transceiver Market to Reach US$26 Billion in 2026","url":"https://iconnect007.com/article/149678/global-ai-optical-transceiver-market-to-reach-us26-billion-in-2026/149675","excerpt":"The years 2026 to 2027 are crucial for establishing a foothold in the 1.6T supply chain, where success in design-in at tier-one customers will likely be a key factor in determining future market share.","as_of":"2026-01-15","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K FY2026 風險因子自述：產品可能因替代或更具成本效益的技術推出而競爭力下降；亦有客戶/競爭對手向後整合而取代公司的風險。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"Otherwise, our product offerings may become less competitive given the frequent introduction of alternative or more cost-effective technologies.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"CPO 被視為可插拔收發器（含 DSP）的結構性替代；Coherent 路線圖稱 1.6T/3.2T 可插拔可能延後 CPO 損益平衡至 2028 年後，並同時展示多種 CPO 技術（OFC 2026）。","source":"DatacenterDynamics 分析：Optical illusion – is co-packaged optics the savior","url":"https://datacenterdynamics.com/en/analysis/optical-illusion-is-co-packaged-optics-the-savior-the-data-center-industry-has-been-waiting-for","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Coherent 於 OFC 2026 展示多種 CPO 技術，採技術中立多平台布局。","source":"Coherent 新聞稿 CPO technologies OFC 2026","url":"https://www.coherent.com/news/press-releases/coherent-co-packaged-optics-cpo-technologies-ofc-2026","excerpt":"> Coherent Demonstrates Multiple Technologies for Co-packaged Optics (CPO) at OFC 2026 3/17/2026 For Immediate Release COHERENT DEMONSTRATES MULTIPLE CO-PACKAGED OPTICS (CPO) TECHNOLOGIES AT OFC 2026","as_of":"2026-03-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K 描述銷售仍為直銷團隊加代表與經銷商，主要靠大型 OEM／終端客戶的關鍵客戶關係；未提訂閱化、D2C 或平台化轉型。","source":"SEC EDGAR 10-K FY2026 Item 1 Business（Sales and Marketing）","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"We market our products and services through a direct sales force and through representatives and distributors around the world.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Coherent 於 2026-08-12 發布新一季營收 guidance，Benzinga 記載較前次區間 $1.91B–$2.05B 上調（BingX 稱新區間 $2.2B–$2.4B，高於共識 $2.14B）；季別標示在來源間不一致","source":"Benzinga COHR earnings-forecasts","url":"https://www.benzinga.com/quote/COHR/earnings-forecasts","excerpt":"Coherent (COHR) last issued guidance on August 12, 2026 for Q1 2027.","as_of":"2026-08-12","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-05 Q1 報告時，下一季（CY Q2 2026）營收 guidance 中點 $1.98B 高於分析師預估 $1.92B","source":"Barchart, Coherent surprises with Q1 CY2026 sales but stock drops","url":"https://www.barchart.com/story/news/1753138/coherent-nysecohr-surprises-with-q1-cy2026-sales-but-stock-drops","excerpt":"Revenue Guidance for Q2 CY2026 is $1.98 billion at the midpoint, above analyst estimates of $1.92 billion.","as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 目標價頁：共識目標價、分析師家數與近期調整","source":"Benzinga COHR price-targets","url":"https://www.benzinga.com/quote/COHR/price-targets","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 分析師評級頁：Deutsche Bank 2026-09-01 初評 Buy 目標價 $400","source":"Benzinga COHR analyst-ratings","url":"https://kr.benzinga.com/quote/COHR/analyst-ratings","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Seeking Alpha COHR 預估修正頁：EPS 下修 0、營收上修 18","source":"Seeking Alpha COHR earnings revisions","url":"https://seekingalpha.com/symbol/COHR/earnings/revisions","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Coherent 宣布以 4 億美元把航太與國防事業賣給 Advent；FY2026 年報載明 2025-09-02 完成處分。","source":"Coherent FY2026 Annual Report to Shareholders (Form ARS)／搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0000820318/000110465926114851/tm264290d2_ars.pdf","excerpt":null,"as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Coherent 2025-10 宣布把慕尼黑材料加工工具事業賣給 Bystronic，年報顯示 2026-01-30 完成；FY2026 認列處分利得 1.24 億美元。","source":"Coherent FY2026 ARS／Converge Digest 報導","url":"https://www.sec.gov/Archives/edgar/data/0000820318/000110465926114851/tm264290d2_ars.pdf","excerpt":null,"as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"多家原告律所（Schall、Pomerantz、Rosen）於 2025-09 至 2025-10 公告調查 COHR；導火線是 2025-08-13 的 A&D 出售消息，股價 2025-08-14 單日跌 19.6%。這是律所徵求原告的調查公告，搜尋未找到已提起的集體訴訟案號。","source":"Pomerantz 調查公告（Barchart／Placera 轉載）","url":"https://www.barchart.com/story/news/35730673/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-coherent-corp-cohr","excerpt":null,"as_of":"2025-10-28","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"10-K Item 3 稱公司涉及營運附帶的各類索賠與訴訟，管理層諮詢法律顧問後認為最終責任不會對財務狀況、流動性或經營成果有重大影響。","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"Management believes, after consulting with legal counsel, that the ultimate liabilities, if any, resulting from such legal proceedings will not materially affect the Company’s financial condition, liquidity, or results of operations.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 10 份 8-K 中含重大項目者 3 份，清單內無 1.01／2.01／4.02 等併購或重編項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000820318&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"以 4 億美元把航太與國防事業賣給 Advent，FY2026 年報載明 2025-09-02 完成處分。","source":"Coherent FY2026 ARS／搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0000820318/000110465926114851/tm264290d2_ars.pdf","excerpt":null,"as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"材料加工工具事業賣給 Bystronic，2026-01-30 完成。","source":"Coherent FY2026 ARS／Converge Digest","url":"https://www.sec.gov/Archives/edgar/data/0000820318/000110465926114851/tm264290d2_ars.pdf","excerpt":null,"as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"多家原告律所公告調查 COHR（Pomerantz 2025-10-28），起因為 2025-08 A&D 出售消息後股價大跌；未找到已提起的集體訴訟案號。","source":"Pomerantz 調查公告（Barchart）","url":"https://www.barchart.com/story/news/35730673/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-coherent-corp-cohr","excerpt":null,"as_of":"2025-10-28","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K Item 3：管理層認為各項訴訟最終責任不會有重大影響。","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm","excerpt":"Management believes, after consulting with legal counsel, that the ultimate liabilities, if any, resulting from such legal proceedings will not materially affect the Company’s financial condition, liquidity, or results of operations.","as_of":"2026-08-14","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 清單無 Item 4.02（非可信賴財報）項目；2025-12-16 的 8-K 僅為分部變更後的歷史財報重編列示，非更正錯誤。","source":"SEC EDGAR 8-K 申報清單／8-K 2025-12-16","url":"https://www.sec.gov/Archives/edgar/data/820318/000082031825000024/iivi-20251216.htm","excerpt":"The Company is filing information under Item 8.01 of this Current Report on Form 8-K (this “Form 8-K”) to (i) provide investors with recast historical financial information for periods prior to the segment change","as_of":"2025-12-16","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"COHR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.16,"operating_margin_pct":14.11,"fcf_margin_pct":-23.28,"rd_intensity_pct":10.18},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"LITE","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.91,"operating_margin_pct":23.35,"fcf_margin_pct":9.52,"rd_intensity_pct":12.47},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"CIEN","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.07,"operating_margin_pct":14.12,"fcf_margin_pct":13.53,"rd_intensity_pct":15.36},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AAOI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":28.92,"operating_margin_pct":-10.58,"fcf_margin_pct":-100.9,"rd_intensity_pct":18.06},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAOI","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MTSI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.13,"operating_margin_pct":18.97,"fcf_margin_pct":9.44,"rd_intensity_pct":23.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"COHR"},"financial_history":{"ticker":"COHR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":5160100000.0,"revenue_yoy_pct":null,"gross_margin_pct":31.36,"operating_margin_pct":1.59,"net_income":-259458000.0,"diluted_eps":-2.93,"free_cash_flow":197965000.0,"fcf_margin_pct":3.84,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":4707688000.0,"revenue_yoy_pct":-8.77,"gross_margin_pct":30.93,"operating_margin_pct":2.62,"net_income":-156154000.0,"diluted_eps":-1.84,"free_cash_flow":198915000.0,"fcf_margin_pct":4.23,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":5810115000.0,"revenue_yoy_pct":23.42,"gross_margin_pct":35.17,"operating_margin_pct":9.21,"net_income":49364000.0,"diluted_eps":-0.52,"free_cash_flow":192764000.0,"fcf_margin_pct":3.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":7118181000.0,"revenue_yoy_pct":22.51,"gross_margin_pct":37.5,"operating_margin_pct":12.67,"net_income":804998000.0,"diluted_eps":4.12,"free_cash_flow":-1030569000.0,"fcf_margin_pct":-14.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/COHR/COHR_Q1_2027_Earnings_Call_20261104.md）

# Q1 2027 Earnings Call
**Coherent Corp.** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Greetings, and welcome to the Coherent Corp. First Quarter Fiscal Year 2027 Earnings Webcast. [Operator Instructions] Please note this event is being recorded.
It is now my pleasure to introduce your host, Mr. Paul Silverstein, Senior Vice President of Investor Relations for Coherent. Please go ahead.

**Paul Silverstein** (Executives):
Thank you, operator, and good afternoon, everyone. With me today are Jim Anderson, Coherent's CEO; and Sherri Luther, Coherent's CFO. During today's call, we will provide a financial and business review of the first quarter of fiscal 2027 and the business outlook for the second quarter of fiscal 2027. Our earnings press release can be found in the Investor Relations section of our company website at coherent.com.
I would like to remind everyone that during our conference call, we may make projections or other forward-looking statements regarding future events or the future financial performance of the company. These are subject to a number of significant risks and uncertainties, and our actual results may differ materially. For a discussion of factors that could affect our future financial results and business, please refer to the disclosure in today's earnings release, our most recent Forms 10-K and 10-Q and the reports that we may file on Form 8-K with the Securities and Exchange Commission.
All our statements are made as of today, November 4, 2026, based on information currently available to us. Except as required by law, we assume no obligation to update any such statements. During this call, we will discuss non-GAAP financial measures. You can find a reconciliation of these non-GAAP financial measures to GAAP financial measures in our earnings release and investor presentation that can be found on the Investor Relations section of our website at coherent.com.
Let me now turn the call over to our CEO, Jim Anderson.

**James Anderson** (Executives):
Thank you, Paul, and thank you, everyone, for joining today's call. Q1 marked a strong start to fiscal 2027. Revenue increased 16% sequentially and 56% year-over-year on a pro forma basis. Non-GAAP EPS increased 80% year-over-year, reflecting continued gross margin expansion and operating leverage. Strong customer demand and our rapid capacity expansion are supporting this growth with near-term bookings and newly signed LTAs providing multiyear visibility. We remain on track to achieve our first $3 billion revenue quarter by the end of fiscal '27. We expect the full year pro forma revenue growth rate to exceed 60%, more than double our fiscal '26 pro forma growth rate. We also have a clear line of sight to our first $4 billion revenue quarter in fiscal '28.
Coherent is a photonics platform company, bringing together technologies across the optical signal chain from materials and components through subsystems and complete solutions. Our breadth positions us to support customers across Datacenter & Communications networks. We're at the center of an extraordinary expansion in optical networking infrastructure, driven by rapid AI growth, the transition from copper to optical connectivity and rising demand for bandwidth and energy efficiency across increasingly large and complex datacenter architectures.
Our established businesses continue to grow rapidly, with datacenter revenue up 85% year-over-year in Q1. At the same time, new growth areas are ramping as well. For example, scale-across datacenter interconnect revenue is growing rapidly with Q1 revenue roughly quadrupling year-over-year and reaching a nearly $1 billion annualized revenue run rate.
In addition, PhotonLink, our newly announced integrated optics platform, is also beginning to ramp, and we expect PhotonLink revenue to exceed $100 million in our March quarter. Accelerating revenue growth, continued gross margin expansion and operating leverage position us to grow profitability faster than revenue. We expect fiscal '27 to be an exceptional year for Coherent.
Moving to our Datacenter & Communications segment. Revenue increased 21% sequentially and 79% year-over-year, marking a fourth consecutive quarter of accelerating growth on both a sequential and year-over-year basis. The segment now accounts for 82% of Coherent's total revenue.
Near-term demand remains strong and our visibility into long-term demand continues to improve. Order coverage through calendar '27 is exceptional, and customer orders increasingly extend into calendar '28. We signed multiple new LTAs in Q1, and customer LTAs typically extend through the end of the decade. We continue to see no signs of attenuation in demand. Within the segment, Datacenter revenue increased 17% sequentially and 85% year-over-year, marking our fourth consecutive quarter of double-digit sequential growth. We expect another quarter of strong sequential and year-over-year growth in the current quarter.
In Datacenter transceivers, we're ramping 1.6T products with multiple customers, while continuing to grow 800-gig revenue. We expect strong transceiver revenue growth in Q2, driven by both 1.6T and 800 gig. We expect 1.6T revenue to continue ramping rapidly over the coming quarters, while 800-gig revenue continues to grow through calendar '27.
At ECOC in September, we demonstrated our progress beyond 1.6T with a 3.2T OSFP pluggable transceiver built with our 400-gig differential EMLs and photodiodes. We expect pluggable transceivers to remain the dominant form factor for scale-out networks over the coming years. Coherent is helping shape the industry ecosystem for emerging formats, demonstrating XPO at OFC and also supporting the new USFP form factor.
Turning to OCS. Customer engagement is broadening across scale-across, scale-out and scale-up networks, spanning our 320x320 platform and denser configurations. We're expanding production at 2 sites to meet demand. As capacity ramps, we expect OCS to become an increasingly meaningful contributor to revenue growth and margin expansion.
At ECOC in September, we launched PhotonLink, our new platform for integrated optics. It's designed to address the transition from copper to optical connectivity in AI datacenters, creating a significant opportunity for Coherent. We estimate that CPO, NPO and chip-to-chip optical interconnects represent approximately $30 billion of market opportunity by 2030, bringing our total market opportunity for Datacenter & Communications to about $90 billion in 2030.
PhotonLink brings together Coherent's photonic technologies and manufacturing capabilities in an end-to-end platform that spans the optical signal chain from generating and shaping light through transmission and detection to converting the signal to electrical form. The platform is designed for a wide range of architectures and applications, including CPO and NPO, scale-out and scale-up networks and scale-in chip-to-chip links. It includes lasers, laser modules, complex fiber assemblies and other optical components and supports indium phosphide-based CW lasers and VCSEL-based technologies. We believe this breadth and depth differentiates us. For an xPU or switch chip with 100 terabits per second of bandwidth, we estimate our content opportunity can reach approximately $15,000 per chip.
Customer engagement is validating the opportunity. In Q1, we signed another significant PhotonLink LTA with a major AI company. The total revenue value of this new LTA is approximately $20 billion over 5 years, with revenue beginning to ramp in early calendar '28. This is in addition to our previously announced LTA with NVIDIA. Beyond these 2 anchor customers, we have more than 10 additional CPO engagements, more than 10 NPO engagements and more than 5 chip-to-chip engagements.
We expect PhotonLink revenue to ramp quickly over the coming quarters. We expect revenue to exceed $100 million in our March quarter and to exceed $250 million per quarter before the end of calendar '27. Expected shipments in the current quarter include a range of CPO products, including our ultra-high power 400-milliwatt CW laser, our fiber assembly solutions and other products.
PhotonLink is initially being deployed in CPO scale-out applications. We expect to begin shipping PhotonLink products for CPO and NPO scale-up applications in the second half of calendar '27. Over time, we expect PhotonLink to become a multibillion-dollar product line for Coherent.
Expanding our indium phosphide capacity is a key enabler of growth in both indium phosphide pluggable transceivers and indium phosphide-enabled PhotonLink solutions. Our 6-inch indium phosphide expansion is progressing well. We doubled our internal indium phosphide output capacity year-over-year in Q1, 1 quarter ahead of our original plan. Q1 was our highest production quarter ever for EMLs, including both 100-gig and 200-gig devices. The ramp contributed meaningfully to datacenter growth, and we expect it to remain an important driver of revenue and gross margin.
Most of the gross margin benefit of our indium phosphide expansion is still ahead of us as the expansion will enable us to increase our mix of internally sourced indium phosphide components, which have a tremendous cost advantage. We remain on track to more than double our internal indium phosphide output capacity again by the end of calendar '27. We've secured the substrates and other critical inputs needed to support this ramp. And given the strength of customer demand are planning additional capacity expansion beyond 2027.
Our 6-inch lines in Texas and Sweden are producing EMLs, CW lasers and high-speed photodiodes with yields that continue to exceed those of our 3-inch lines. Production includes our 400-milliwatt CW laser for CPO, which is covered by our NVIDIA partnership and is expected to begin generating revenue this quarter. We also remain on track to begin 6-inch indium phosphide production in Zurich in the first half of calendar '27, further extending what we believe is a meaningful manufacturing advantage.
Moving to Communications. Revenue increased 34% sequentially and 84% year-over-year, and we expect another quarter of strong sequential and year-over-year growth in the current quarter. Traditional telecom continued to grow, but the primary growth driver was scale-across, which has quickly become the largest source of revenue within Communications.
Over the past year, we've expanded our datacenter interconnect portfolio to help customers connect datacenters with greater capacity and efficiency. Building on our leadership in pump lasers and our broad component portfolio, we've introduced higher level products, including modules, line cards, subsystems and our new multi-rail solution. These offerings are seeing strong customer demand and help customers make better use of existing fiber while scaling high-capacity links between distributed AI datacenters.
In Q1, scale-across revenue exceeded $200 million, up 53% sequentially and nearly fourfold year-over-year. That puts the business at a nearly $1 billion annualized revenue run rate, making it one of our fastest-growing businesses. With multi-rail beginning to ramp in our March quarter, we expect quarterly scale-across revenue to roughly double from the Q1 level by the end of calendar '27.
Turning to Industrial. Q1 revenue was flat sequentially and year-over-year on a pro forma basis. Bookings were strong, led by semiconductor capital equipment customers. And we expect growth to resume in the current quarter. Near-term growth is being driven by semiconductor capital equipment, AI infrastructure and fusion energy. In semiconductor equipment, our lasers, precision optics and engineered materials serve front-end applications and we've seen a strong uptick in bookings.
In AI infrastructure, our CO2 lasers and zinc selenide optics are used to drill advanced circuit boards for AI servers. Demand is also growing for our pulsed laser deposition systems used to produce high-temperature superconductor tape for magnetic fusion.
Over the longer term, we see significant opportunities in datacenter xPU cooling and quantum technologies. For AI datacenters, our Thermadite material can enable higher xPU performance and token generation. We're shipping prototypes to several strategic customers this quarter, and we expect revenue to begin ramping in the second half of calendar '27.
In quantum, we supply lasers and materials to leading quantum technology developers and are engaged in next-generation programs. Given the multiple growth areas, we expect our Industrial segment to return to growth and build momentum over the coming quarters.
In summary, Q1 demonstrated the strength of our growth momentum and the breadth of our opportunity. Demand remains strong, customer commitments continue to deepen our visibility and we are expanding capacity ahead of plan.
Established businesses continue to grow rapidly while new growth areas are ramping quickly. Our focus is on execution, expanding capacity, delivering for our customers and improving profitability as we grow. We believe this combination positions Coherent for sustained growth in fiscal '27 and beyond.
I want to thank our team for their outstanding work this quarter. I'll now turn the call over to Sherri.

**Sherri Luther** (Executives):
Thank you, Jim. I'm extremely pleased with the outstanding Q1 financial results. Our performance in the first quarter represents a powerful continuation of our growth trajectory, characterized by accelerating top line momentum, durable structural gross margin expansion and significant operating leverage. The compounding impact of these operational drivers fuels non-GAAP EPS growth to significantly outpace revenue growth. We achieved this strong performance while preserving balance sheet flexibility and strategically directing capital toward targeted capacity expansions and making investments in our product road map to support robust AI Datacenter & Communications demand.
Let me now provide a summary of our results. First quarter revenue was a record $2.37 billion, representing a sequential acceleration of 16% and a substantial 50% increase year-over-year. This performance was driven by the continued AI infrastructure build-out across our Datacenter & Communications businesses. On a pro forma basis, excluding the financial impact of the Aerospace and Defense business, and the Munich, Germany, product division, both of which were divested in 2026, revenue increased 16% sequentially and 56% year-over-year.
Our non-GAAP gross margin for the first quarter was 40.6%, representing a 37 basis point increase sequentially and a 184 basis point improvement as compared to the year ago quarter. This continuous expansion reflects durable pricing optimization and structural cost improvements, particularly within our Datacenter & Communications segment.
The improvements in gross margin, both sequentially and year-over-year, were driven primarily by pricing optimization, lower product input costs and improved manufacturing yields. We have made significant progress with our pricing optimization strategy to ensure that we price our highly differentiated products for the value they provide to our customers.
Our gross margin profile is also benefiting from the transition to 6-inch indium phosphide as we continue to scale our production capacity. Given the progress that we have made over the past couple of years and our current trajectory, it is clear that we need to raise our gross margin target. We now expect to achieve our first quarter with gross margin above 45% before the end of calendar 2028. We believe the drivers of this gross margin expansion are continued pricing optimization, ramp of new growth platforms, full operational leverage of our 6-inch indium phosphide capacity and other cost improvements.
I also want to note that the new over 45% target is 300 basis points higher than the long-term target we provided to the investment community only 18 months ago.
First quarter non-GAAP operating expense was $412 million compared to $377 million in Q4 and $304 million in the year ago quarter. Non-GAAP operating expenses as a percentage of revenue decreased meaningfully to 17.4%, down from 18.4% in the prior quarter and 19.2% in the year ago quarter. This improvement reflects enhanced operational discipline and underscores the powerful operating leverage inherent in our business.
From an R&D perspective, we are strategically directing our capital toward high conviction long-term growth drivers, which Jim outlined in his remarks. This disciplined approach ensures our investments are concentrated where they generate the highest financial returns and drive sustainable revenue growth.
Our first quarter non-GAAP operating margin increased to 23.2% from 21.8% in the prior quarter and 19.5% in the year ago quarter. The sequential and year-over-year increases were driven by strong revenue growth, expanding gross margin and structural expense discipline. First quarter non-GAAP earnings per diluted share was $2.09, up 20% from the prior quarter and up 80% from the year ago quarter. Earnings growth continued to exceed revenue growth, demonstrating gross margin expansion and operational leverage accelerating our bottom line profitability.
Turning to the balance sheet. We closed the quarter with a healthy cash balance of $2.34 billion compared to $2.59 billion at the end of the prior quarter and $1.55 billion at the end of the year ago quarter. Our debt leverage ratio at the end of Q1 was 1.1x as we continue to maintain a highly resilient and flexible balance sheet. Consistent with our capital allocation priorities, we strategically invested in opportunities that will drive long-term growth and profitability.
Capital expenditures for the first quarter increased sequentially to $776 million, up from $556 million in the prior quarter and $104 million in the year ago quarter. These investments directly support the future growth of our Datacenter & Communications businesses with excellent financial returns. Our conviction to deploy this capital at an accelerated rate is backed by exceptional customer visibility, a robust pipeline of committed purchase orders and additional multiyear supply agreements.
Furthermore, this capacity offers significant fungibility as our infrastructure can be efficiently repurposed to support multiple product lines. Given the strong visibility and record backlog, we expect capital expenditures to increase sequentially again in the second quarter. With our strong balance sheet and profitability trajectory, we possess the scale and flexibility to continue investing capital toward high ROI growth initiatives while supporting customer demand.
I will now turn to our guidance for the second quarter of fiscal 2027. We expect revenue to be between $2.55 billion and $2.75 billion. We expect non-GAAP gross margin to be between 40% and 42%. We expect total operating expenses of between $430 million and $450 million on a non-GAAP basis. We expect the tax rate for the quarter to be between 18% and 20% on a non-GAAP basis. We expect non-GAAP diluted EPS to be between $2.28 and $2.48.
In summary, fiscal 2027 is off to a powerful start with strong financial momentum backed by deep demand visibility. Our focus remains on rapidly ramping capacity to meet demand, expanding our gross margin, capitalizing on the immense operating leverage in our model and executing a disciplined capital allocation strategy focused on maximizing returns that drive long-term shareholder value.
That concludes my formal comments. Operator, please open the line for the Q&A session.

**Operator** (Operator):
[Operator Instructions] The first question today comes from Joseph Cardoso with JPMorgan.

**Joseph Cardoso** (Analysts):
Really appreciate some of the disclosures that you provided this quarter. And I wanted to first start with PhotonLink and the initial visibility you provided there. I was hoping you could provide more color with respect to the ramp itself, especially just given the backdrop of the $20 billion agreement that you've highlighted? And then I have a follow-up.

**James Anderson** (Executives):
Yes. Thanks, Joe. So first of all, yes, we're certainly really pleased with the momentum that we have around PhotonLink and kind of whether you measure it by customer engagement or LTAs, as you mentioned, or just the revenue outlook that I mentioned in the prepared remarks, we're just really pleased with the progress there.
And just as a reminder, PhotonLink is -- we kind of consider it a one-stop shop for integrated optics. It's basically our platform for allowing customers to basically have a platform that allows for the optical link from end to end. It's the complete optical signal chain and all the technology along the optical technology along that path. And really excited about the progress, as I mentioned in the prepared remarks, over 20 customer engagements on CPO, over 10 -- or sorry, over 10 on CPO, over 10 on NPO and then over 5 chip-to-chip engagement. So the customer engagement is very extensive and they continue to grow.
You mentioned or asked about the LTA. Really pleased about that major AI customer and that LTA is, as I said, $20 billion over a 5-year period. And the revenue for that would start at the beginning of calendar '28. But the PhotonLink revenue ramp is starting ahead of that. We'll ship a little bit of -- a small amount of PhotonLink revenue this quarter, but we expect to ship over $100 million in our March quarter. And then before the end of calendar '25 (sic) [ '27 ], expect to ship over $250 million a quarter. So really pleased with all of that progress.
And I guess the other thing that I would add is, if we look further out, we're expecting this over time to become a multibillion dollar product line. The initial shipments of PhotonLink are all around CPO in the scale-out network. But when we start to ship into CPO and NPO and to scale-up networks, I think that drives another huge leg of demand for this technology. I think that will be the much bigger adoption that we see. And that we expect to start to ship revenue into CPO and NPO applications in the scale-up domain towards the end of calendar '27. So yes, we're excited about the progress and expect this to become a major product line for us.

**Joseph Cardoso** (Analysts):
And maybe in a similar vein, I wanted to touch on the scale-across DCI opportunity. Particularly curious how we should think about the customers and products that are underpinning the revenue outlook to double by the end of the next calendar year.

**James Anderson** (Executives):
Yes. Thanks again. This has been a really great growth area for us over the past year. In fact, it's surprised us a little bit how quickly this has grown. So overall, so DCI and scale-across that falls within our Communications part of our business, which is essentially everything outside of -- all communications outside of the Datacenter. And if we look at that segment overall, Communications grew 84% year-over-year. But while telecom grew most of that -- the vast majority of that growth was driven by DCI. And so what's going on there is you're seeing these large AI workloads that are spanning multiple datacenters. And so that's driving the need for much greater bandwidth and connectivity -- optical connectivity between datacenters. And so that's what's driving. That's the underlying market dynamic that's driving the growth.
And then you asked about customers and products. So customers would be either equipment makers. So we're certainly selling into multiple different equipment makers that -- whose equipment goes into scale-across applications, but also selling directly to hyperscalers as well. And so it's a mixture of both types of customers. And then the products, it's interesting, we sell -- in this part of the market, we sell products at multiple levels of the value chain. So we sell in components like, for instance, pump lasers that go into a wide range of different equipment. At one level up in the value chain, we sell subsystems and modules, so ZR/ZR+ modules, line cards, amplifiers, ROADMs, et cetera. And then one level up from that, in some cases, sell complete solutions to our customers as well. So we're selling across multiple levels of the value chain. And so I think that's helped us really maximize the growth here as well.
And as I mentioned in the prepared remarks, if we look at our Q1 revenue, it was over $200 million. So we're basically at about $1 billion annualized revenue run rate now. And that's -- that Q1 growth had quadrupled year-over-year. And we expect that if you take that Q1 baseline, we expect the revenue to double again before the end of calendar '27. And so that growth that we've seen to date, that's ahead of multi-rail. So we expect multi-rail revenue, which is a -- multi-rail is a great solution, some great technology that we have there. We expect that to start -- that revenue to start to ramp in our March quarter. And so it's been a really good area of growth, and we expect this to continue to be a very good area of growth over the coming quarters as well.

**Operator** (Operator):
The next question comes from Simon Leopold with Raymond James.

**Simon Leopold** (Analysts):
First, Jim, I want to thank you for the increased transparency on Slide 7. I know this is something I've been probably annoying you about. So thank you. The slide did not mention OCS. I know you talked about the product group in your prepared remarks. But could you update us on your progress and expectation for this product group? And then I've got a follow-up, please.

**James Anderson** (Executives):
Yes, sure. Thanks, Simon. Thanks for the feedback, as always. We're always looking to improve. So I appreciate the feedback. But yes, in OCS, I did mention in the prepared remarks OCS falls within our Datacenter part of our business. And just reiterating, Datacenter was up 85% year-over-year in our Q1. OCS continues to make good progress. We've got really extensive customer engagement. We've seen that customer engagement, continue to expand across more applications and not just scale-out applications, but scale-across and scale-up applications as well. And that's across -- in terms of products, that's across both 320x320 systems, which are shipping as well as denser configurations. I think the denser configurations will be used more in the scale-up applications.
We're ramping production at 2 different sites in parallel, and that's really to meet the demand that we're seeing. We have a very differentiated technology. It's liquid crystal. It's nonmechanical technology, has better power efficiency and better reliability than MEMS-based solutions. So we feel really well positioned. We're ramping production. And I think it will be an increasingly larger contributor to our revenue growth in the quarters to come. And maybe last thing to add is we see the market opportunity for OCS as at least $4 billion by 2030. It could be larger than that.

**Simon Leopold** (Analysts):
And as a follow-up, I have a hard question, one that I imagine you anticipate getting is, what does the proposed consolidation of Lumentum and Marvell mean to you?

**James Anderson** (Executives):
Yes. Thanks, Simon. No, I don't think that's a hard question at all. I think happy to answer that. I'd give a few thoughts on this. I think number one is it definitely demonstrates that optics and photonics is becoming an absolutely critical part of datacenter architecture.
As we look forward, as we convert the entire scale-up network and then even the scale-in chip-to-chip communication links, over time, all of that getting converted from copper to optical. Photonic technology is absolutely critical to making that happen to driving the innovation in datacenter architecture. So I think it's a proof point around just the criticality of optics and photonics.
And then I think for Coherent, I think it just -- it highlights the tremendous strategic value of the portfolio that is within Coherent. There's no other company, I believe, on the planet that has a broader and deeper set of photonic and optical technology. If you look at the entire optical signal chain from the generation of the light to the transmission through our fiberoptic cable that we make to the detection on the other side, I don't think there's any other company that's got a better portfolio of technology.
So I think it definitely highlights the strategic importance of our technology platform. And then look, I think from a customer perspective, I think that -- I think a lot of -- for a lot of the customers, our customers, I think it's really important that they have an independent photonic optical supplier and partner. And so I think it positions us really well to be that independent optical supplier that's going to support -- without any competitive conflict can support multiple different customers and support both hyperscaler customers, can support semiconductor customers.
And so I think it positions us really well to be that partner of choice in terms of optics for the industry. So look, we think we're really well positioned from both a technology standpoint, manufacturing standpoint and strategically and I think we're on a really great growth trajectory. And I think you can see some of that already in the PhotonLink technology and the PhotonLink revenue ramp.

**Operator** (Operator):
The next question comes from Tom O'Malley with Barclays.

**Thomas O'Malley** (Analysts):
I guess the first part of the question for you, Jim, is why now in terms of giving the longer-term forecast? It's been something that you've kind of held off on doing for a while. You gave $3 billion and then $4 billion next year.
And then the second part of the question is, is that all backed with supply? How are you able to get visibility that far out? Is that already in the books today? Or perhaps you could give us like what percentage of that is backed with supply today? Or if you need to add any to get you to those numbers?

**James Anderson** (Executives):
Yes. Thanks, Tom. I think it is a little bit different. We are providing a little bit longer-term visibility than we normally would. I think it's really backed by the -- just extraordinary level of visibility that we have on the business. When I look at the backlog, the bookings both -- so both near-term visibility and long-term visibility. If I look at just the backlog that we have, I mean, calendar '27 is basically booked out and the customers are booking out calendar '28 now. So from a near-term booking demand perspective, we have great visibility.
We've signed a number of new LTAs over the past quarter. I mentioned one of the big LTAs as part of the PhotonLink prepared remarks. But the LTAs also give us really good visibility because they include very high-quality forecast, long-term forecast. So I think that's -- given that really good visibility, that's certainly giving us confidence.
And then also, great that you mentioned supply. We've done a number of things within our supply base to make sure that we've got the right supply in place to support that as well. So yes, I would say that, that's -- those views that we gave, whether it's the $3 billion this year and the $4 billion quarter next year is underpinned by supply agreements. Also, remember that we're highly vertically integrated. So a lot of that's underpinned by our own internal supply that we're ramping, right?
One of the constraints, if we look back over the past year or 1.5 years, one of the constraints has been indium phosphide. And I'm just really pleased with how the team has executed very, very well on the indium phosphide production ramp. We've doubled production capacity a quarter earlier than what we thought we would, and that gives me the confidence that they're going to achieve -- the team is going to achieve our plan to more than double capacity again by the end of calendar '27. So you put all that together and yes, we're feeling really good about the outlook and the visibility for the business.

**Thomas O'Malley** (Analysts):
Super helpful. And then just as my follow-up for that LTA. Obviously, $20 billion, a pretty robust number over that 5 years. Could you just give us any color just around that customer perhaps? And then if you can't talk about the customer around some of the solutions that, obviously, it's PhotonLink, so it spans a large number of your products, but any more specificity would be really helpful, just given the size of that customer.

**James Anderson** (Executives):
Yes, sure. So definitely a leading AI datacenter customer name you will definitely recognize, right? And so we're really proud of that partnership, excited about it. That's all -- that LTA for $20 billion is all around PhotonLink technology. I would call it -- I would say it's anchored by our laser, our 400-milliwatt CW laser. That's kind of the anchor of that LTA. But there's -- it's more than -- we're selling more than just that laser. So we're selling more, call it, a higher level solution than that. So more than just that laser.
So we're really, really pleased by that. As I mentioned, the revenue -- we expect the revenue to start to flow from that in early 2028 and to ramp over the course of the quarters and years after that. And so really pleased with that. And I think given the engagement that we have on PhotonLink across many different customers, many different solutions, we certainly expect to sign more long-term agreements and partnerships with PhotonLink over the coming quarters as well.

**Operator** (Operator):
The next question comes from George Notter with Wolfe Research.

**George Notter** (Analysts):
I guess I just wanted to ask you a question about the 45% gross margin outlook before the end of '28. So I guess I'm curious like what does that assume about your transceiver business? I'm just wondering if, to hit that, you need to gate your transceiver supply or transceiver ramp? Or is this just a case where everything can ramp in unison as naturally would ramp and you wind up at 45% gross margins? What's the view there?

**James Anderson** (Executives):
Yes. Thanks, George. I'll start and then see if Sherri has any color to add. But yes, we haven't assumed that we're kind of artificially gating the transceiver business. So there's no assumption on that. We're assuming that the transceiver business grows at what we think is a reasonable growth rate to expect from the transceiver business. But on top of that, we do have new products that are ramping on top of that. PhotonLink, a number of new products in datacenter interconnect, OCS ramping over time as well. And so you put all those products ramping over time. And those products are accretive to the company's margin. I think the new product ramp helps as well.
And then in addition to that, the other thing that I would add more on the cost side is a number of different cost activities that we're driving. But certainly, a big one of it is we expect additional leverage in terms of gross margin from our indium phosphide ramp. I think there's -- as I mentioned briefly in the prepared remarks, I think most of the benefit from indium phosphide expansion is still ahead of us. And so I think there's a good component of the margin expansion that's kind of underpinned by the indium phosphide expansion as well.

**George Notter** (Analysts):
Is it possible to get the company to higher margins than 45% over time? I mean, I guess I'm maybe looking at Lumentum as an example. Those guys obviously have had quite a bit of margin expansion. Obviously, the fastest-growing parts of that business are many of the areas where you're kind of looking for growth going forward. Is 45% just a stop in a bigger picture or a bigger number? What do you think?

**James Anderson** (Executives):
I don't think there's any structural barrier to us driving gross margin above 40%. In fact, I think Sherri, in her remarks, I think she said over 45% before the end of calendar '28, I think, is the way she said it, right? So I -- yes, we certainly don't view just like our old target of 42%, where we said over 42%, we never viewed that as a stopping point. We viewed that as a stop along the way. And I would say 45% is -- yes, a stop along the way, and I don't see any structural reason why the company couldn't continue to drive gross margins beyond that.

**Sherri Luther** (Executives):
Yes. I would just add that the target that we put out about 18 months ago at our Investor Day of over 42%, that was a 3- to 4-year target that we put out, but we pulled that in, right, in only 18 months now raising our target to over 45%. So as we get close to that target, we'll certainly reevaluate and look at what makes sense beyond that, but it's just a stop along the way.

**James Anderson** (Executives):
Yes. And George, maybe the other thing I'd add is we're certainly super focused on gross margin expansion. But the other thing that we're very focused on is operating leverage, right? And I think we're quite pleased to see that we're gaining operating leverage in terms of OpEx as a percentage of sales, and we expect that to continue as well. So I think you should expect continued operating leverage as well.

**Operator** (Operator):
The next question comes from Gianmarco Conti with Deutsche Bank.

**Gianmarco Conti** (Analysts):
Yes. Great. Congrats on the quarter. Maybe starting with PhotonLink. I wanted to touch on the scale-in/scale-up opportunity with micro-VCSEL. You mentioned you had 5 engagements, I believe, chip-to-chip. I'm curious if you could talk in a little bit more detail here whether there is anything you can quantify in terms of revenue to come online next year? Anything around micro-VCSEL?

**James Anderson** (Executives):
Yes. So thanks for asking about micro-VCSEL. So certainly, when I look across the PhotonLink engagements, there is, I would say, many VCSEL, micro-VCSEL, we call it multi-core VCSEL because it -- the multi-core VCSEL attaches to our multi-core fiber that we produce. And so -- but multiple of those engagements involve our VCSEL technology. I mean maybe just as a reminder of the company's sort of depth in VCSEL technology. Number one is we've shipped over 700 million VCSELs into datacenter applications over the past year. So we have enormous manufacturing expertise in VCSELs.
Also at the ECOC conference, when we launched PhotonLink, we talked about our technology in VCSELs, micro-VCSELs, VCSEL arrays, et cetera. We showed that -- one of the things that we showed was that we had industry-leading energy efficiency around VCSELs of -- we showed a 1 picojoule per bit capability, which I think is very industry-leading capability. And so VCSEL is definitely a core technology, something that the company has a long history in and we have multiple engagements.
I think you'll see that deployed in NPO applications relatively in scale-up NPO applications in relatively short amount of time. I think you also asked about scale-in chip-to-chip. I think that's a little further out in time. I think PhotonLink and scale-in applications is more in the 2029 to 2030, but we'll definitely see, I think, VCSELs deployed in NPO applications well before that.

**Gianmarco Conti** (Analysts):
If I could just ask a follow-up. It's going to be a tough question, sorry to put you on the spot. But I've been receiving a lot of questions from investors around Chinese laser suppliers. I was wondering if you could provide any kind of thoughts on basically more supply coming in online? And whether you see them competing for ultra-high-powered lasers for CWs?

**James Anderson** (Executives):
Yes. So I don't see that those competitors in terms of ultra-high power. If you're talking about like the 400-milliwatt CW laser, we're not seeing competition from really -- we really only have one competitor there as far as we can see, right? So really not seeing any other competitors out there with high-power CW laser capability.

**Paul Silverstein** (Executives):
Operator, before we go to the next analyst, if we could ask all the other analysts to limit themselves to one question with the goal of trying to accommodate everybody on the call. All right. Thank you.

**Operator** (Operator):
The next question comes from Dan Zhu with Bernstein.

**Daniel Zhu** (Analysts):
You mentioned that scale-up optics should start towards the end of calendar 2027. Anything you can share about whether the initial deployments are NPO or CPO? And also about how -- whether sort of this is primarily going to be on VCSELs or will this start with InP-based lasers?

**James Anderson** (Executives):
Yes. Thanks, Dan. So I think what we'll see -- we'll definitely see CPO in scale-up. We certainly believe that. I think we'll see NPO scale-up soon after that as well. If not by the end of calendar '27, I think we'll certainly see deployment in the early part of '28. So I think in scale-up, both CPO and NPO within either that late '27 or early '28 time frame in the scale-up applications.
And then I think -- did you ask -- what was the second part of your question, Dan?

**Daniel Zhu** (Analysts):
How much of it is VCSEL versus InP?

**James Anderson** (Executives):
Yes. I think the initial deployment is indium phosphide, the high-power CW lasers. That's for CPO in both initially scale-out and then in scale-up. And then I think VCSELs will happen in that NPO kind of early '28 time frame.

**Operator** (Operator):
The next question comes from Ryan Koontz with Needham.

**Jeffrey Hopson** (Analysts):
This is Jeff Hopson on for Ryan. You noted ramping the indium phosphide supply for your own laser supply and that'd be able to lead to the margin expansion from weaning off external sources. I was just curious if there's any color on what the split is currently versus internal versus external? And kind of how -- or the time line of that over time as it relates to the margin expansion?

**James Anderson** (Executives):
Yes. Thanks, Jeff. We haven't broken out the split, but I can tell you the split hasn't changed much in a year. We're using about the same mix of internal versus external now as we were a year ago. So although we've doubled our internal indium phosphide supply our -- the primary usage of our internal indium phosphide parts is in our datacenter transceivers.
And if you look at the growth rate of our datacenter business, datacenter transceivers, it's basically tracked the growth of our indium phosphide capacity, although -- basically one quarter later because when -- in the quarter we produce the lasers, the next quarter is when we ship the transceivers. And so essentially, our transceivers have been -- business has grown at the same rate as our internal indium phosphide, which means that our mix of internal versus external really hasn't changed much over the past year.
Now as we continue to expand indium phosphide now looking forward, more than doubling it by the end of '27, we do believe over the coming quarters,  we'll start to shift more of the mix from external towards internal.
Now we always think -- we always believe we'll have some portion of our supply from external for our transceiver business. But we believe over the coming quarters, we'll start to shift more towards internal. And that's really because it's a tremendous cost advantage for us to use our internally produced lasers, especially the ones that are made on the 6-inch platform. And in my prepared remarks, when I said the majority of the benefit from 6-inch indium phosphide is ahead of us, that's actually what -- really what I'm referring to is that benefit of changing the mix towards internal is largely ahead of us and that's a much bigger cost structure improvement.

**Operator** (Operator):
The next question comes from Papa Sylla with Citi.

**Papa Sylla** (Analysts):
Congrats on the very impressive results. Jim, I wanted to maybe double-click on the $15,000 of content per, I think, 100-terabit chip you mentioned earlier and at ECOC. So assuming that is probably the full stack opportunity, which might be a longer-term figure. But I thought it would be helpful to also have a sense, even qualitatively, on what percentage, I guess, of that $15,000 you expect to capture in the near term versus longer term and how it may change kind of beyond '27?

**James Anderson** (Executives):
Yes. Thanks, Papa. Yes, the $15,000 basically represents -- if you take an example of a chip that needed 100 terabit of I/O and if you were using our full PhotonLink portfolio, which would include not just the lasers, but all the other components, isolators, thermoelectric coolers, laser modules, our full fiber assembly kit, all the connectors, et cetera. So everything that we do, if you use all of that, the content per chip would be we estimated about $15,000 per chip.
Now it will depend on the customer and their particular application, how much of that content they utilize, whether they utilize a portion of that, all of it, that will really depend on the particular engagement. But that $15,000 is sort of the opportunity that's out there for us. I think we'll see over the next year or 2 as PhotonLink ramps, I think we'll see customers that leverage the vast majority of that. And I think we'll also see customers that leverage a subset of that. So I think we'll definitely -- we'll see a mix of that.
And we're happy to support our customers, whether they want the entire solution or they want a portion of it, we'll work with them on whatever works best for them. But regardless of the amount of content they take, for us, this -- we see this as all greenfield growth because most of PhotonLink adoption over time will be driven by scale-up. And again, that's all greenfield growth for us because that's us and the industry converting copper links to optical links over time. So we see it as greenfield revenue growth.

**Operator** (Operator):
The next question comes from Cody Acree with StoneX Financial.

**Cody Grant Acree** (Analysts):
Sherri, maybe for you, if we can go back to the gross margin discussion. Can you maybe help to stratify the contribution part of that? You talked about the indium phosphide 6-inch ramp yields increasing utilization rates, maybe even your mix thoughts? And just if you can also factor into that the competitive dynamics on your module and your transceiver piece of more global Chinese competition and what's inherently just a more price-sensitive market?

**Sherri Luther** (Executives):
Yes. Sure, Cody. I think you cut out a little bit, but I think you were asking for more color on what the drivers are to gross margin expansion over 45%. That's what I think your question is.

**Cody Grant Acree** (Analysts):
Yes, yes, that's right.

**Sherri Luther** (Executives):
Yes. Okay. So if I were to rank order, I think that the largest contributors are going to be our new product ramps and that full operational leverage of our 6-inch indium phosphide capacity and then pricing optimization, followed by cost reduction. That's kind of how I would rank order it. And the timing of some of those things kicking in, right, will vary.
But certainly, new product ramps. I mean those are gross margin accretive, the new products that Jim referred to earlier in his prepared remarks. Those are gross margin accretive. And so that will benefit our gross margin. As we continue to shift our supply from external to internal, as Jim talked about a little bit ago, that's going to drive significant opportunity in our gross margin.
And then pricing optimization, rather, I mean, that is an area where I think we will continue to have benefit there fully in our Datacenter & Communications segment, certainly in our Industrial too, but definitely in Datacenter & Communications, there's opportunity for that. We saw that to be a large contributor during the current quarter as well as in prior quarters. And so that will continue to be a benefit as well to drive to over 45% and cost reductions that will always continue to be something that we focus on, but that's how I would rank order them.

**Operator** (Operator):
The next question comes from Karl Ackerman with BNP Paribas.

**Karl Ackerman** (Analysts):
Jim, you spoke about how customers are beginning to book out to calendar 2028 that gives you confidence in your growth forecast. At the same time, there is investor concern about the financing and permitting of data centers here in the United States. In light of this, how does the team align its laser production capacity plans with your major customers? And has the team considered customer prepayments for additional laser production capacity?

**James Anderson** (Executives):
Yes. Thanks, Karl. The answer to the last part of the question is yes, definitely. Maybe I'll start with the end of the question. So we've signed a number of LTAs over the past quarters. The one public LTA that is the one with NVIDIA that we signed back in March, but we've signed a number of other LTAs. The LTAs follow -- all follow a general pattern. And one part of the LTA is typically some sort of upfront payment from the customer either -- it could be either a prepayment or NRE. There's different forms of payment, but there's some sort of upfront payment from the customer.
And what we do that for is for 2 reasons. Number one is it makes sure that the customers have skin in the game. But number two is we use that upfront payment to help fund the CapEx to build the capacity for that customer, right? We think it's important that if we're going to go build the capacity that the customers either fund that or help co-fund that. And so far, we've had customers to be very, very willing to do that. And I think that's worked really well for us. And so I would say almost every LTA that we've signed has that general pattern. And so that certainly gives us better confidence and helps offset the risk in terms of our own capital deployment.
But I guess on the first part of your question, we certainly work very, very closely with our customers on planning out the demand. I think one thing that -- to keep in mind with indium phosphide capacity, is remember that it's not just being driven by datacenter demand. There's 2 things driving optics -- in general, optics demand, right? Number one is datacenter growth. But number two is in the case of integrated optics, it's the conversion of the copper links to optical over time. And that is a technology trend that in my view is independent of the market demand. That's a technology trend that will happen and regardless of the datacenter demand because that's necessitated by the ability to achieve the bandwidth and the link speeds that we need to achieve in the scale-up domain or chip-to-chip is we have to switch to optics over time. And so that's an independent technology trend. And that's certainly part of what's driving the indium phosphide capacity demand over the long term.

**Operator** (Operator):
The next question comes from Meta Marshall with Morgan Stanley.

**Meta Marshall** (Analysts):
Maybe just a question on substrate availability. I think there had been some concern in the market around availability of 6-inch versus 3-inch. I know you noted in the prepared remarks that you had gotten capacity, but maybe if you could just speak about kind of 6-inch versus 3-inch substrate availability and how that's impacting expansion plans.

**James Anderson** (Executives):
Yes. Thanks, Meta. So we have over -- on 6-inch in particular, but 3-inch as well, we do continue to buy 3-inch wafers. We do still have 3-inch production, but all of our expansion is mostly on 6-inch moving forward.
And we have over 5 different suppliers of substrates. We've signed long-term agreements with a number of those suppliers. And when I look at our next step of more than doubling the capacity by the end of calendar '27, we believe we've secured the necessary substrates for that capacity expansion. And then we've certainly -- we have plans in place to further expand capacity beyond '27, and we're certainly working with or already have in place, substrate capacity for that as well. So I think the summary is we have multiple different suppliers, and we've made sure that we have the substrate capacity for the expansion.

**Operator** (Operator):
The next question comes from Sean O'Loughlin with TD Cowen.

**Sean O'Loughlin** (Analysts):
Great. I'll make it quick. Jim, can you just talk about how fungible your capital installed base is across indium phosphide versus gallium arsenide, if we -- maybe we end up in a world that is more VCSEL or multi-core VCSEL heavy than it is ultrahigh-power CW?

**James Anderson** (Executives):
Sure. I would say there's some fungibility, but not -- it's not like you can easily switch a line from indium phosphide to gallium arsenide or vice versa. But I will note that we have a tremendous amount of gallium arsenide capacity. One of the stats that we shared at the PhotonLink launch is that today, we have capacity to produce over 1 billion VCSEL arrays annually. So we have a tremendous amount of capacity that we could deploy.
And so to the extent that we saw a broad-based adoption and rapid ramp of VCSEL technology, I don't think we -- there's probably anybody else in the industry that's better positioned to source or to supply that demand than Coherent is. And so we feel really well positioned on gallium arsenide VCSEL technology and/or capacity. And then on indium phosphide, obviously, we're ramping that very, very quickly. And so I think on both, we're on a good path.

**Operator** (Operator):
Our last question today comes from Ananda Baruah with Loop Capital.

**Ananda Baruah** (Analysts):
Yes, congrats on the progress here. And I guess, Jim, let me just ask you a capacity question -- supply -- capacity supply question from the other direction. Yes, there's also been a conversation just in the financial community about at an industry level excess InP EML capacity at some point in calendar '28. You're also -- now you're also talking about sort of contract agreements going sort of well into that time frame. So I would love to get your opinion on sort of how you view the potential for an oversupply situation at an industry level going through '28.

**James Anderson** (Executives):
Yes. I think through '27 and into '28, I don't see that as a risk, given that -- given not just the demand that pluggable transceivers is creating, but also the demand that integrated optics is going to create for lasers as well as there's quite a bit of indium phosphide, that's also used in some of the DCI applications, too. So when I look across all of that, I don't see an oversupply risk through calendar '28.
I also think for us because most of our indium phosphide gets used in our -- well, I guess today all of it, today, all of our indium phosphide gets used in our own products. And we don't even produce enough today for -- to meet all the demand of our own products. For us, I don't -- that's not a primary concern for us. If I think if we were -- if there were more supply externally, that may affect us if we were supplying indium phosphide lasers externally, but we're not. And I think our plan is to -- over time, start to use more indium phosphide -- more of our internal indium phosphide production in our -- to change to increase the mix towards internal over time. So yes, I guess the short answer to your question is we don't see any big oversupply situation into '28.

**Operator** (Operator):
This concludes our question-and-answer session. I would like to turn the conference back over for any closing remarks.

**James Anderson** (Executives):
Thanks, operator, and thanks, everybody, for joining us on the call today. So we certainly enter the remainder of the year with great momentum, exceptional customer demand and as we were just talking about rapidly expanding capacity. I just want to say thanks to -- especially to all of our employees, our customers, our partners and, of course, our shareholders for the continued support. And we look forward to updating you again next quarter. Thank you.

**Operator** (Operator):
The conference has now concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### COHR_Q4_2026_Earnings_Call_20260812.md
- 2026-08-12｜CFO｜guidance：FY27 Q1 營收財測區間 $2.2–2.4B（原話："$2.2 billion and $2.4 billion."）
- 2026-08-12｜CFO｜guidance：FY27 Q1 non-GAAP EPS 財測區間 $1.85–2.05（原話："between $1.85 and $2.05 on a non-GAAP basis."）
- 2026-08-12｜CFO｜guidance：FY27 Q1 non-GAAP 營業費用財測 $400–420M（原話："operating expenses of between $400 million and $420 million"）
- 2026-08-12｜CEO｜guidance：CEO 預期 FY27 底前出現首個營收逾 $3B 的季度（原話："our first quarter with over $3 billion of revenue"）
- 2026-08-12｜CEO｜guidance：CEO 稱本季資料中心年增率預期超過 80%（下一句接雷射已備妥）（原話："certainly got the lasers this quarter to make that happen"）
- 2026-08-12｜CFO｜margin：Q4 non-GAAP 毛利率 40.2%（原話："Our Q4 non-GAAP gross margin was 40.2%"）
- 2026-08-12｜CFO｜margin：毛利率改善來源：良率與效率（另有 6 吋 InP、定價優化）（原話："improved manufacturing yields and efficiencies"）
- 2026-08-12｜CFO｜margin：CFO 說 6 吋晶圓產出為 3 吋 4 倍、成本約一半，毛利率效益來自成本結構而非良率（原話："right, 4x, but it's at half the cost."）
- 2026-08-12｜CFO｜margin：管理層稱公司仍處毛利率擴張策略早期（原話："we are early in our strategy for gross margin expansion"）
- 2026-08-12｜CFO｜commitment：毛利率目標大於 42%（分析師提 42.5%，CFO 答投資人日目標為 >42%）（原話："it was greater than 42%."）
- 2026-08-12｜CFO｜commitment：CFO 承諾達標後會調高毛利率目標（原話："greater than 42%, we will no doubt raise the target."）
- 2026-08-12｜CFO｜margin：CFO 稱 Q1 財測中點營業費用已低於 18% 目標模型（原話："in fact, of 18% for OpEx."）
- 2026-08-12｜CFO｜margin：SG&A 共享服務效益超出原預期，預期 FY27 續增（原話："exceeded our original expectations"）
- 2026-08-12｜CFO｜capital_allocation：資料中心投資回收期約 18 個月（原話："have a roughly 18-month payback period."）
- 2026-08-12｜CFO｜capital_allocation：預期 Q1 資本支出再季增（原話："capital expenditures to increase sequentially again"）
- 2026-08-12｜CFO｜capital_allocation：FY26 償還債務 $513M，槓桿降至 0.7x（原話："we made $513 million in debt payments"）
- 2026-08-12｜CEO｜commitment：承諾本季末內部 InP 產能年增一倍，較原計畫提前一季（原話："double our internal indium phosphide output capacity"）
- 2026-08-12｜CEO｜commitment：承諾 CY27 底前 InP 產能再翻倍以上（原話："more than double our internal indium phosphide output"）
- 2026-08-12｜CEO｜product：蘇黎世 6 吋 InP 產線預計 CY27 上半年開始生產（原話："begin 6-inch production in Zurich during"）
- 2026-08-12｜CEO｜product：1.6T 拉貨比三個月前預期更快（原話："1.6T is ramping incredibly fast"）
- 2026-08-12｜CEO｜product：CPO 超高功率 CW 雷射收入預期 12 月季開始（原話："We expect in our December quarter."）
- 2026-08-12｜CEO｜product：PhotonLink 平台初期收入預期自 12 月季開始（原話："initial revenue from PhotonLink-related products"）
- 2026-08-12｜CEO｜product：OCS 可及市場估計逾 $4B（原話："OCS represents more than $4 billion of"）
- 2026-08-12｜CEO｜product：OCS TAM 於 OFC 由 $2B 上調至逾 $4B，且稱可能仍偏保守（原話："we doubled it from $2 billion to over $4 billion"）
- 2026-08-12｜CEO｜product：Multi-rail 收入預期 CY27 上半年起跑（原話："revenue to ramp in the first half of calendar '27"）
- 2026-08-12｜CEO｜product：Thermadite XPU 散熱收入預期 CY27 下半年起跑（原話："revenue to begin ramping in the second half of calendar '27"）
- 2026-08-12｜CEO｜product：CPO 用於 scale-up 的收入時程為 CY27 下半年，管理層稱時程一貫（原話："start to flow in the second half of calendar '27"）
- 2026-08-12｜CEO｜customer：管理層稱 CPO 需求沒有遞延，反而被提前（原話："we've seen absolutely no pushout of CPO demand"）
- 2026-08-12｜CEO｜customer：FY27 訂單已全數排滿（原話："Fiscal '27 is basically completely booked out."）
- 2026-08-12｜CEO｜customer：客戶訂單已延伸到 CY28（原話："Customer orders now extend into calendar '28"）
- 2026-08-12｜CEO｜customer：管理層稱無需求衰減跡象（原話："no signs of attenuation in customer demand"）
- 2026-08-12｜CEO｜customer：LTA 含最低需求保證（take-or-pay）（原話："take-or-pay agreements"）
- 2026-08-12｜CEO｜customer：LTA 幾乎都載明協議價格，期間最長至本十年末（原話："the pricing is set for, I think, all or almost all"）
- 2026-08-12｜CEO｜customer：進口限制報導促使部分客戶來談製造選項與供給（原話："spurred some new customer demand and supply discussions"）
- 2026-08-12｜CEO｜customer：稱幾乎所有產品線都供給受限（原話："any product line we're not supply constrained on"）
- 2026-08-12｜CEO｜customer：漲價（含 LTA 內約定調價）為 $3B 季度驅動因素之一（原話："pricing improvements that we're driving"）
- 2026-08-12｜CEO｜competition：近期不會對外銷售 InP 雷射（原話："I don't see any time in the near future"）
- 2026-08-12｜CEO｜competition：長期仍有部分資料通訊收發器使用外部來源（原話："supported by external sources"）
- 2026-08-12｜CEO｜risk：進口限制報導被稱為臆測，公司認為若成真將受惠（原話："report is speculative at this point"）
- 2026-08-12｜CEO｜risk：工業部門其他市場持續疲弱（原話："continued weakness across broader industrial markets"）
- 2026-08-12｜CEO｜risk：目前主要限制是 InP 產出爬坡（逐字稿原句開頭疑有轉錄錯誤），組裝測試產能不受限（原話："We're really just constrained by the ramp of the"）

### 問答異常語氣（迴避／改口／保留）
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Vivek Arya：9 月季財測毛利率有何特殊因素、FY27 增量毛利率如何看｜答法：CFO 未給增量毛利率數字，改談成本與定價時程不一、新產品推升，並轉向營業費用已低於 18% 目標模型
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Meta Marshall：明年毛利率改善中良率、產品組合、定價各占多少｜答法：CFO 未拆分比重，改談 6 吋成本結構（4 倍產出、一半成本），CEO 補充 6 吋良率高於 3 吋
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Karl Ackerman：$3B 季度營收中 1.6T、OCS、multi-rail、積壓訂單、價格各占多少｜答法：CEO 列出驅動因素但未給任何分項金額或比重
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Karl Ackerman：CY28 LTA 的承諾量是否高於 CY27、近 90 天承諾量改善多少｜答法：CEO 稱各年供給一般遞增，但未給量化承諾數字或近 90 天變化
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Simon Leopold：毛利率目標（分析師引述過去 42.5%）更新，CEO 轉交 CFO｜答法：CEO 先稱進展良好後轉交；CFO 稱投資人日目標為 >42%，Q1 中點 40.5%，未給時間表

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
{"date":"20260901","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 資料中心光互連需求結構性持續（DCC 段量＋mix 雙升，且四個新引擎陸續貢獻）","columns":{"2Y 驗證點":"DCC YoY 維持 >30%，OCS／CPO 開始認列營收","5Y 驗證點":"3.2T／多軌系統／熱管理接棒，DCC 段營收季度化突破 $30 億","10Y 驗證點":"光互連仍是 AI 算力擴張的物理必要層","數字門檻":"DCC YoY ≥ +30%；FY27 Q4 單季營收 >$30 億（管理層自訂目標）","來源":"Coherent 法說、2026-08-12 財報稿","漂移觸發條件":"連 2 季 TTM DCC YoY 跌破 +25% → 削弱"}},{"id":"H2","text":"毛利率結構性擴張持續（6 吋磷化銦成本結構＋定價優化＋新產品組合）","columns":{"2Y 驗證點":"Non-GAAP GM 站穩 40%+","5Y 驗證點":"GM 邁向管理層目標 >42%，營運槓桿放大 EPS","10Y 驗證點":"垂直整合維持結構性成本優勢","數字門檻":"Non-GAAP GM ≥ 39%（現 40.2%，Q1 FY27 guide 39.5-41.5%）","來源":"Coherent Q4 FY26 財報、法說","漂移觸發條件":"連 4 季 TTM GM 偏離 ≥ 5% → 削弱（5Y 假設）"}},{"id":"H3","text":"資本支出暴增係產能超前建置而非資本紀律鬆動，FY2027 內 OCF／FCF 應見回升軌跡","columns":{"2Y 驗證點":"FY2027 各季 OCF 較 FY26Q4 低點回升","5Y 驗證點":"FCF margin 回到正值並向歷史常態（3-4%）靠攏","10Y 驗證點":"資本配置紀律維持（無重大 M&A 失控、SBC 稀釋可控）","數字門檻":"FY2027 全年 OCF 由 FY26 的 $0.08B 轉正並成長","來源":"Coherent 10-K/10-Q、法說 capex 指引","漂移觸發條件":"FY2027 全年 OCF 未轉正 → 反轉（10Y 假設，因涉及資本紀律根本判斷提前列入反轉門檻）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"CPO 蠶食 pluggable：NVIDIA 自家 Spectrum-X Photonics 已於 2026 下半年進入商用部署（CoreWeave／Lambda／OCI 為早期客戶），若標準化與量產速度快於 Coherent 在 CPO socket 拿到的份額，DCC 段每季 pluggable 飯碗（現約 $16 億）可能被稀釋而 CPO 補不回缺口","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"NVIDIA CPO 部署滲透率 >30% 且 Coherent CPO 營收未同步補上 pluggable 流失"}},{"id":"R2","text":"AI 資本支出消化期：超大雲廠 capex 指引連續下修，同時 Coherent 自身超前建置的產能（FY26 資本支出 $11.1 億，capex/revenue 15.6%）若利用率不如預期，會同時打擊營收成長與 FCF 轉正時程","columns":{"對應假設":"H1／H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"連 2 季雲廠 capex 指引下修 >20%，或 FY2027 全年 OCF 仍未轉正"}},{"id":"R3","text":"Merchant 競爭、磷化銦原料成本與中國反制：中國 Innolight／Eoptolink 在 1.6T 世代的全球份額（約 50-70%）較 800G 世代（35-40%）不降反升；中國 2025 年 2 月起的磷化銦出口許可制度已使 6 吋晶圓價格上漲約 250%（約 $1,400→$5,000/片）；若 FCC 對中國光模組的進口禁令正式生效，不排除中國以磷化銦／鎵出口許可進一步收緊作為反制（中國官方已表態「必要時將回應」），使 Coherent 的「垂直磷化銦」原料成本曝險進一步惡化","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"連 4 季 GM 下滑（原料成本傳導），或 Coherent 在 1.6T 世代對主要客戶份額續降（sourced），或磷化銦出口許可再度收緊"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已達進場門檻，本欄示意持有期加碼觸發：GM連2季>41.5%或CPO/OCS單季合計營收破$300M","irr_base_pct":14.8,"ev5y_pct":88.9,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":5.1,"ev5y_pct":88.9,"irr_base_pct":14.8,"max_dd_pct":-60.0,"bull_5y_price":843.0,"bear_5y_price":168.0,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":"已達進場門檻，本欄示意持有期加碼觸發：GM連2季>41.5%或CPO/OCS單季合計營收破$300M","price_at_dd":277.83,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
