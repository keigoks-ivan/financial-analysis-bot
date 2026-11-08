你是 stock-analyst **v20 判斷 agent**，標的 WLDN（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"WLDN","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_contract_revenue_gaap","label":"Contract revenue（GAAP 營收）","value":214.5,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"查無單季共識，省略"},{"id":"f_kpi1_net_revenue_non_gaap","label":"Net revenue（non-GAAP，扣分包）","value":112.2,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"查無"},{"id":"f_kpi2_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未揭露 non-GAAP 營業利益，以此代之）","value":28.3,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"查無"},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":16.3,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"新聞稿損益表；利益率為本表計算：占 contract revenue 7.6%、占 net revenue 14.5%"},"note":"查無"},{"id":"f_kpi7_fy2026","label":"FY2026 指引（上修）","value":"net revenue 435–445；Adj. EBITDA 109–111；Adj. EPS 5.15–5.25","period":"Q3 FY2026 公告（2026-11-05）","unit":"USD m／USD per share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026 公告（2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1；假設 15.9m 稀釋股、稅率 0%、不含未來併購"},"note":"consensus_revision 快照 FY1 EPS 5.07（財報前快照）；指引中點 5.20"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_wldn_gross_margin_pct","label":"WLDN 毛利率","value":37.79,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WLDN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wldn_operating_margin_pct","label":"WLDN 營業利益率","value":7.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WLDN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wldn_fcf_margin_pct","label":"WLDN FCF 利潤率","value":8.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WLDN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ttek_gross_margin_pct","label":"TTEK 毛利率","value":18.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTEK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ttek_operating_margin_pct","label":"TTEK 營業利益率","value":11.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTEK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ttek_fcf_margin_pct","label":"TTEK FCF 利潤率","value":10.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTEK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_acm_gross_margin_pct","label":"ACM 毛利率","value":5.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_acm_operating_margin_pct","label":"ACM 營業利益率","value":4.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_acm_fcf_margin_pct","label":"ACM FCF 利潤率","value":1.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_j_gross_margin_pct","label":"J 毛利率","value":22.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.J.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_j_operating_margin_pct","label":"J 營業利益率","value":4.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.J.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_j_fcf_margin_pct","label":"J FCF 利潤率","value":4.53,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.J.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_gaap_eps","label":"GAAP 淨利／稀釋 EPS","value":11.9,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"USD m（EPS 0.76）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"查無"},{"id":"f_kpi5_ytd_9_32_9_5_2","label":"自由現金流（YTD 9 個月：營業現金流 32.9 − 資本支出 5.2）","value":27.8,"period":"YTD 至 Q3 FY2026（2026-10-02，公告於 2026-11-05）；新聞稿未揭露單季現金流","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"YTD 至 Q3 FY2026（2026-10-02，公告於 2026-11-05）；新聞稿未揭露單季現金流","citation":"新聞稿現金流量表，FCF 為本表計算"},"note":"查無"},{"id":"f_kpi6_sbc","label":"SBC 占營業利益","value":30.5,"period":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"SBC 4.972 ÷ GAAP 營業利益 16.304，本表計算；占 contract revenue 2.3%"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":66.22,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-25.08,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":32.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.07 → 5.07）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.42 → 5.42）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.07,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":5.42,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 5.07 → 5.07（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":16.07,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.31,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝43.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":43.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.37,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝40.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":40.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":13.06,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 5.07，分子＝快照價 66.22","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":43.14,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 82.3、現金 39.16（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":15.33,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":1058.29,"period":"2026-11-08","unit":"USD m","basis":"市值 1015.15 ＋ 淨負債 43.14","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":826.8,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（1 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":960.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（1 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.28,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 66.22 / W52 90.04 / W104 75.79 / W250 45.8 / W250 13週斜率 1.37%"},{"id":"f_ma_w52","label":"52 週均線","value":90.04,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":75.79,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":45.8,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.37,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K稱市場高度分散，公司認為沒有單一對手有足夠份額影響其市場；並提示大型全國/國際工程或營建公司可能成為新進入者。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm","excerpt":"We believe that no single competitor has sufficient market share to influence the markets in which we operate.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K風險因子：大量營收來自競標，輸標可能多年失去該市場機會，得標也可能因壓價而侵蝕利潤。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm","excerpt":"To the extent we engage in competitive bidding and are unable to win particular contracts, we not only incur substantial costs in the bidding process that negatively affect our operating results, but we may lose the opportunity to operate in the market for the services provided under those contracts for a number of years.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"CSIMarket 估計 Willdan 占其追蹤同業群營收份額約0.2%，Q2 2026上升。","source":"CSIMarket WLDN Competitors","url":"https://csimarket.com/stocks/WLDN-Competitors","excerpt":"Willdan Group Inc's Competitiveness A competitive positioning analysis and financial ratio benchmarking of Willdan Group Inc (WLDN) against its publicly traded competitors: sales growth, net income, profitability, valuation and market share, plus each peer's market capitalization, revenue, income and employees.","as_of":"2026-08-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025：兩大客戶 Clark County School District 與 Southern California Edison 合計占合併合約營收 23.2%；前10大客戶占 50.7%（FY2024 51.3%、FY2023 52.7%）；FY2024、FY2023 無單一客戶超過10%。","source":"SEC EDGAR 10-K FY2025（申報 2026-02-27）Item 8 客戶集中度","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm","excerpt":"For fiscal years 2025, 2024, and 2023, the Company’s top 10 customers accounted for 50.7%, 51.3%, and 52.7%, respectively, of the Company’s consolidated contract revenue. For fiscal year 2025, the Company had individual customers that accounted for more than 10% of its consolidated contract revenue; for fiscal year 2025, the Company derived 23.2% of its consolidated contract revenue from two customers, Clark County School District and Southern California Edison.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Energy 分部 FY2025 有27.4%來自上述兩客戶；截至2026-01-02及2024-12-27，無單一客戶占應收帳款超過10%。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm","excerpt":"As of January 2, 2026, and December 27, 2024, the Company had no individual customers that accounted for more than 10% of the Company’s billed outstanding receivables, respectively.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"S&P 於2025-09 將 Edison International 與 SCE 下調一級至 BBB-（野火基金縮減）；SCE 為 WLDN 前兩大客戶之一。","source":"SCE Form 424B5 / 搜尋結果","url":"https://www.sec.gov/Archives/edgar/data/92103/000119312526071092/d25997d424b5.htm","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"WLDN 管理層在 Q4 2025 財報電話會議稱 APG 已取得創紀錄 backlog，預期 2026 年 APG 成長逾 50%，並因長約而把 backlog 往 2027、2028 擴；公司總 backlog 約 10 億美元（2026-01-02）。","source":"MarketBeat / Willdan Q4 2025 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/willdan-group-q4-earnings-call-highlights-2026-02-27/?.tsrc=rss","excerpt":null,"as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"IEEE Spectrum 引 Kearney/IEEE 研究：全球電力部門到 2030 年需多 45 萬至 150 萬名工程師；另有來源指出美國投資者所有公用事業資本支出 2026 年預估 2,278 億美元（2024 年約 1,730 億），工程人才短缺與許可延遲並列為電網專案準時交付最大障礙（各 30%，招募業者部落格）。","source":"IEEE Spectrum, A Shrinking Workforce Threatens the Future of the Grid; Spencer Ogden survey","url":"https://spectrum.ieee.org/power-engineering-workforce-gap","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K Item 3 僅揭露工程顧問業常見的專業疏失／遺漏類索賠，由專業責任險承保；未列反壟斷或監管調查。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm","excerpt":"We are subject to claims and lawsuits from time to time, including those alleging professional errors or omissions that arise in the ordinary course of business against firms that operate in the engineering and consulting professions.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K MD&A 稱公司經歷設備材料成本上升與設備供應鏈延遲，對經營結果與財務狀況不重大；關稅、價格上漲等對完成品成本的影響難以精確衡量。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm","excerpt":"While immaterial to our results of operations and financial condition, we have experienced higher cost of materials and delays in our supply chain for equipment. The prices of finished products from manufacturers are subject to fluctuation and increases. It is difficult to accurately measure the impact of inflation, tariffs, price escalation, raw material costs, and other factors that impact the cost of finished goods due to the imprecise nature of the estimates required.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子提及供應鏈限制與勞力短缺推高材料與勞力成本、使交付與專案時程延長；並依賴分包商","source":"Willdan Group Form 10-K (FY ended 2026-01-02)","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm","excerpt":"● our ability to manage supply chain constraints, labor shortages, elevated interest rates, and elevated inflation; ● our ability to obtain financing and to refinance our outstanding debt as it matures;","as_of":"2026-03-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 摘要：合約營收年增33.2%至2.31億美元，淨營收年增23.5%至1.17億美元，部分來自近期併購（第三方摘要，Q3 2026 結果搜尋未取得）","source":"Quartr: Willdan Group (WLDN) Q2 2026 earnings summary","url":"https://quartr.com/events/willdan-group-inc-wldn-q2-2026_oqkNXTIK","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 2025 電話會議（2026-02）：能源段約占營收85%；客戶別公用事業約41%、州/地方政府約48%、商業11%；APG 相關業務預期2026年成長逾一倍；AI／資料中心推升用電需求","source":"MarketBeat: Willdan Group Q4 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/willdan-group-q4-earnings-call-highlights-2026-02-27/","excerpt":null,"as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Wedbush 指公司上調2026展望、能源業務加速；並稱資料中心與電氣化負載支撐成長","source":"itiger: Willdan Lifts 2026 Outlook as Energy Business Accelerates, Wedbush Says","url":"https://www-web.itiger.com/news/2634463893","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 財報電話會議/摘要（fintool）","source":"fintool Q3 2026 WLDN","url":"https://fintool.com/app/research/companies/WLDN/earnings/Q3 2026","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Simply Wall St community narrative argues automation/technology-driven alternatives needing fewer staff could undermine Willdan's consulting model (opinion, not company forecast)","source":"Simply Wall St community narrative: Automation Disruption And Public Sector Cuts Will Undermine Performance","url":"https://simplywall.st/community/narratives/us/commercial-services/nasdaq-wldn/willdan-group/8aw674ad-automation-disruption-and-public-sector-cuts-will-undermine-performance","excerpt":"Willdan Group Published 13 Jul 25 Updated 07 Oct 26 Views 65 Not Invested Willdan GroupWLDN Fair Value US$130 Share price07 Oct US$66.2249.1% undervalued intrinsic discount Loading 1Y-27.18% 7D-10.01% Share Like votes Follow Fair Value 1 Automation And AI Pressures Will Challenge Consulting Margins Yet Long-Term Contracts","as_of":"2025-07-13","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Willdan 商業客戶（含 Burton Energy 收購）占營收比重升至約 25%（2024 年為 7%），Burton 帶來經常性收入；搜尋摘要未見銷售通路／GTM 結構性改變的明文。","source":"briefglance／搜尋摘要：Willdan Boosts Margins, Acquires Burton Energy to Expand Commercial Footprint","url":"https://briefglance.com/companies/willdan-group-inc/pulses/29105","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 財報電話會摘要：商業擴張提供部署工程、軟體、採購與能源管理能力的另一路徑","source":"MarketBeat Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/willdan-group-q2-earnings-call-highlights-2026-08-07/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-07-30：共識評級 Moderate Buy、共識目標價 $112.67","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/willdan-group-wldn-expected-to-post-quarterly-earnings-on-thursday-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-06 公司上調 FY2026 EPS guidance 至 $5.00–$5.15，高於分析師共識 $4.77（營收區間各來源不一）","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/willdan-group-nasdaqwldn-updates-fy-2026-earnings-guidance-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Clear Street 目標價由 88 上調至 112","source":"TipRanks/TheFly","url":"https://www.tipranks.com/news/the-fly/willdan-group-price-target-raised-to-112-from-88-at-clear-street-thefly","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-30 完成收購 Mantis Intermediate Holdings 100% 股權，價款約 2.85 億美元，以 3,500 萬循環信貸＋2.5 億信貸協議借款支付","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926123327/wldn-20261030x8k.htm","excerpt":"On October 30, 2026, the Company completed the Transaction and, pursuant to the Purchase Agreement, Energy Solutions acquired all the equity interests of Mantis. Pursuant to the Purchase Agreement, Energy Solutions paid approximately $285,000,000, subject to certain customary post-closing adjustments.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-09-22 簽署 Mantis 收購協議，基本價款 2.85 億美元現金","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926110002/tm2625947d1_8k.htm","excerpt":"Seller will sell the Subject Securities to Energy Solutions for a base purchase price of $285,000,000 (the “Base Purchase Price”), which is subject to adjustment, in cash","as_of":"2026-09-23","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"10-K 法律程序僅有一般專業疏失類索賠，無重大訴訟","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm","excerpt":"We are subject to claims and lawsuits from time to time, including those alleging professional errors or omissions that arise in the ordinary course of business against firms that operate in the engineering and consulting professions.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-30 完成 Mantis 收購，約 2.85 億美元，舉債支付","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926123327/wldn-20261030x8k.htm","excerpt":"On October 30, 2026, the Company completed the Transaction and, pursuant to the Purchase Agreement, Energy Solutions acquired all the equity interests of Mantis.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"+","claim":"2025-11 宣布、2026-01-02 完成收購 Compass Municipal Advisors，條款未揭露（搜尋摘要）","source":"Business Wire／Nasdaq 報導 Willdan Expands Financial Services With Acquisition of Compass Municipal Advisors","url":"https://www.businesswire.com/news/home/20251121025503/en/Willdan-Expands-Financial-Services-With-Acquisition-of-Compass-Municipal-Advisors/","excerpt":null,"as_of":"2025-11-21","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"經查 10-K 法律程序僅一般專業疏失索賠，搜尋無集體訴訟","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm","excerpt":"We are subject to claims and lawsuits from time to time, including those alleging professional errors or omissions that arise in the ordinary course of business against firms that operate in the engineering and consulting professions.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"WLDN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.79,"operating_margin_pct":7.05,"fcf_margin_pct":8.4,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WLDN","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TTEK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":18.78,"operating_margin_pct":11.73,"fcf_margin_pct":10.81,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTEK","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ACM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":5.68,"operating_margin_pct":4.65,"fcf_margin_pct":1.32,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ACM","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"J","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":22.07,"operating_margin_pct":4.57,"fcf_margin_pct":4.53,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.J","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"WLDN"},"financial_history":{"ticker":"WLDN","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":429138000.0,"revenue_yoy_pct":null,"gross_margin_pct":33.46,"operating_margin_pct":-1.65,"net_income":-8448000.0,"diluted_eps":-0.65,"free_cash_flow":-169000.0,"fcf_margin_pct":-0.04,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":510095000.0,"revenue_yoy_pct":18.87,"gross_margin_pct":35.24,"operating_margin_pct":4.33,"net_income":10926000.0,"diluted_eps":0.8,"free_cash_flow":29289000.0,"fcf_margin_pct":5.74,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":565798000.0,"revenue_yoy_pct":10.92,"gross_margin_pct":35.84,"operating_margin_pct":5.54,"net_income":22570000.0,"diluted_eps":1.58,"free_cash_flow":63660000.0,"fcf_margin_pct":11.25,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":681552000.0,"revenue_yoy_pct":20.46,"gross_margin_pct":37.51,"operating_margin_pct":6.48,"net_income":52557000.0,"diluted_eps":3.49,"free_cash_flow":70697000.0,"fcf_margin_pct":10.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WLDN/WLDN_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Willdan Group, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Greetings. Welcome to the Willdan Group Third Quarter Financial Year 2026 Financial Results Conference Call. [Operator Instructions] Please note, this conference is being recorded. I will now turn the conference over to Al Kaschalk, Vice President. Thank you. You may begin.

**Al Kaschalk** (Executives):
Thank you, Bill. Good afternoon, everyone, and welcome to Willdan Group's Third Quarter 2026 Earnings Call. Joining our call today are Mike Bieber, President and Chief Executive Officer; and Kim Early, Executive Vice President and Chief Financial Officer. Our conference call remarks will include both GAAP and non-GAAP financial results. Reconciliations between GAAP and non-GAAP measures can be found in today's press release and in the presentation slides, all of which are available on our IR website. 
Please note that year-over-year commentary or variances on revenue, adjusted EBITDA and adjusted EPS discussed during our prepared remarks are on an actual basis unless otherwise specified. We will make forward-looking statements about our performance. These statements are based on how we see things today. While we may elect to update these forward-looking statements at some point in the future, we do not undertake any obligation to do so. As described in our SEC filings, actual results may differ materially due to risks and uncertainties. 
With that, I'll hand the call over to Mike, who will begin on Slide 2.

**Michael Bieber** (Executives):
Thanks, Al, and good afternoon or evening to everyone on the call. We had a strong operational performance in Q3. In the third quarter, contract revenue and net revenue each grew 18% to $215 million and $112 million, respectively. Organic net revenue growth was a healthy 12% and was a stronger 17% in our Energy segment. Adjusted EBITDA increased 22% year-over-year to $28.3 million, and our adjusted EBITDA margin expanded to 25.2% of net revenue. Our margin has expanded by more than 80 basis points year-over-year. We've achieved this kind of double-digit growth all year long, which has led us to a record 9-month performance in 2026. 
Two important things have happened since our last call. First, on October 30, we closed the acquisition of Mantis Innovation, which significantly scales our commercial and industrial energy management business. Second, with 9 strong months behind us and Mantis now closed, we are raising our full year 2026 targets again. And today, we are introducing preliminary 2027 targets that call for continued double-digit growth. Before I move on, I want to congratulate our team on excellent business execution and thank our customers for entrusting us with some of their most difficult challenges. 
On Slide 3. Back in 2024, I talked about our strategy to significantly increase our presence in the commercial market to balance our customer exposure. We believe then that a broader customer base would add stability, create new growth opportunities and support higher margins. That strategy has been effective. Just 2 years ago, commercial work was about 7% of our business. Today, it's about 1/4 of our work. And with Burton and Mantis acquisitions on a full year pro forma basis, commercial work is equally balanced with work for state and local governments and utilities. We've now achieved what we set out to do, grow an equal third leg of the stool that diversifies our risk and leads to more consistent results. 
Commercial end markets have the additional benefit of growing faster than our company average and providing higher margins. Compared with 2 years ago, on a pro forma basis, Willdan has -- now has no customers over 10% of revenue, and our work now covers all 50 states. We've significantly reduced our customer concentration risk and heavy concentration of work in California and New York. On Slide 4, we've now finished the HSR process with financing in place, and we closed the Mantis transaction last Friday. Mantis is headquartered in Houston, has more than 220 employees across the country. It provides energy management services primarily to large commercial and industrial customers, C&I customers. 
These energy services include efficiency, procurement, consulting, and controls. As you can see on the slide, Mantis adds an almost entirely new list of blue-chip clients to Willdan, including Sabey, DataBank, Giovanni, Hershey, Frito-Lay, Molson Coors, and ASSA ABLOY. In 2026, Mantis is expected to generate about $120 million in contract revenue. The accountants have taken a closer look at the components that build up net revenue, and under those new guidelines, we now expect Mantis to add about $75 million in net revenue, not the $120 million as previously communicated. 
That change also means that Mantis' margin will be accretive to Willdan's and will be about 35% of EBITDA to net revenue. Strategically, Mantis has a strong management team, a differentiated set of capabilities, and long-standing relationships with blue-chip commercial and industrial clients. Next on Slide 5. We've had another strong stretch of contract wins, and here are 6 notable examples since our last earnings call. 
For the New York Power Authority, NYPA, we were awarded a 10-year multiple award IDIQ contract with a total budget of about $3.3 billion. This represents the recompete of one of our largest contracts. We perform $50 million to $60 million per year of work for NYPA on a variety of energy-related projects in New York, and this vehicle will support continuation and further program growth. There was a press release today about this. 
Secondly, Con Edison and National Grid decided to combine several existing smaller programs into one contract and award us a $25 million per year energy efficiency and electrification program serving gas and electric customers in downstate New York. This work will include our existing Con Ed multifamily and small business work and add National Grid. This is the 17th year in a row supporting Con Ed's energy efficiency program and is a significant expansion of the work we're currently performing. For Menlo Digital, we were awarded a $20 million substation project, which is 50 megawatts in size. For Bodkin, in Texas, we were awarded a $16 million, 75-megawatt battery energy storage system. 
I mentioned in the last call how popular these BESS projects are becoming because they provide owners reserve grid capacity, higher grid resiliency, and improved power quality. Lastly, we were awarded 2 projects in California for $9 million and $8 million, respectively. One is the solar and HVAC project and the other is a solar BESS project. It was another strong quarter full of new wins and pipeline solid heading into the end of the year. On Slide 6, there are some macro trends that are fundamentally reshaping the energy sector and creating opportunities for Willdan. First, artificial intelligence is driving data center development. 
Second, the changing climate is bringing hotter summers, more wildfires and more severe storms. Third, new technologies like batteries, solar and digital controls are being connected to a grid that in many places is 50 to 100 years old. And fourth, inflation and global conflict are raising the cost of commodities and power equipment. These 4 trends are having a profound probably once in a generation impact on the energy sector. We've been talking for the past 11 quarters about the return to electric load growth, driven by the confluence of data centers, electrification and more extreme weather patterns. This is making will end services more valuable to customers. There is a massive need for reinvestment in the utility and power equipment space. 
But the trend that has emerged as the most important to our customers, regulators and now even the public is energy affordability. While the average retail electricity rate rose by 5% year-over-year, many specific locations in the grid have increased by more than 30% in the same period. Residential heating oil prices have increased 75% year-over-year. The factors described on this slide have converged to make power affordability the most important consideration for most will end clients. 
Communities and policymakers want low growth, but not at the expense of customer bills. Will then sits at the epicenter of this grid challenge, working with all 3 of our customer groups, utilities with the planning and energy efficiency programs, state and local governments on siting, permitting and regulatory frameworks and commercial clients with energy procurement and efficiency. These trends are all playing towards our strength. Kim, over to you.

**Creighton Early** (Executives):
Thanks, Mike, and good afternoon, everyone. We delivered another strong quarter with net revenue up 18% and adjusted EBITDA up 22% on healthy demand, disciplined execution and margin expansion. Year-to-date, adjusted EBITDA is up 34%, and our adjusted EBITDA margin on net revenue has expanded more than 300 basis points. Even after deploying $56 million for acquisitions this year, we ended the quarter at 0.2x net leverage, which positioned us to close the Mantis Innovation acquisition after the quarter end. 
Turning to the third quarter results on Slide 8. Contract revenue and net revenue each grew 18% to $215 million and $112 million, respectively. Organic net revenue growth was 12%, with the balance of the growth from recent acquisitions, including Burton and Compass. Gross profit grew 23% to $82.5 million and gross margin expanded about 150 basis points to 38.4% of contract revenue. The improvement reflects a favorable revenue mix, including higher incentive revenue under some of our utility programs and increasing revenue from our LADWP Street Lighting Project. Adjusted EBITDA increased 22% to $28.3 million, a 25.2% margin on net revenue, up 80 basis points from the year ago quarter. G&A expenses increased 27% to $66.1 million, or 30.8% of Contract Revenue versus 28.7% a year ago. 
Growth from non-cash expenses accounted for most of the increasing percentage of revenue with stock compensation rising 58% to $5.0 million on new grants at a higher stock price and depreciation and amortization increasing 48% to $5.8 million on the acquired intangibles. Salary and benefit costs grew 24%, in line with the acquisitions and revenue growth. Interest expense rose 19% to $1.1 million, reflecting increased borrowings to fund the Burton acquisition. The higher stock comp and intangible amortization slowed the pretax income growth to 8% over the prior year quarter or $15.4 million. 
Our effective tax rate rose to 23% from 4% a year ago, reflecting higher pretax income and lower discrete benefits from stock option exercises and facility energy efficiency deductions. As a result, net income was $11.9 million or $0.76 per diluted share versus $13.7 million or $0.90 per share a year ago. Adjusted earnings per share was $1.20, essentially flat with $1.21 in the prior year as the higher tax rate offset the 22% growth in adjusted EBITDA. On an operating basis, it was another very good quarter. 
Turning to the year-to-date results on Slide 9. For the first 9 months, contract revenue grew 18% to $601 million and net revenue grew 17% to $322 million or 21% and 20% of net revenues, respectively -- of growth, respectively. Normalizing for last year's extra week. Gross margin expanded 80 basis points to 38.8%, again, reflecting a favorable revenue mix and increasing utility revenue. G&A expenses grew 19%, in line with contract revenue. Pretax income grew 41% to $41.7 million, helped by the higher gross profit margin, a bit of operating leverage despite the increasing noncash charges and the absence of last year's onetime refinancing and lease charges. 
We recognized a $3.0 million tax benefit for the 9 months compared to a $4.2 million benefit a year ago. Net income rose 32% to $44.7 million or $2.89 per diluted share, up 28%. Adjusted EBITDA rose 34% to $79.4 million or 24.7% of net revenue, up from 21.6% a year ago and adjusted earnings per share grew 25% to $4.18, all are records for a 9-month period. 
On Slide 10, our trailing 12-month results show the consistency of underlying growth of the business and our ability to convert that growth into higher margins. Contract revenue of $774 million was up 19% net revenue of $411 million, up 16%, but adjusted EBITDA of $99.5 million was up 29% and adjusted earnings per share of $5.75 reflects a 41% increase. Earnings continue to grow faster than revenue, driven by project management productivity, AI-enabled efficiency and G&A that grows more slowly than revenue. 
On Slide 11, the consistency of growth in earnings and margins is on display. Our adjusted EBITDA has grown at a 48% CAGR over the past 4 years from $23 million in 2022 to the $110 million midpoint of our guidance in 2026. That record has been derived from a combination of organic revenue growth and acquisitions, but also by increasing our adjusted EBITDA margins through a combination of greater project profitability and operating leverage from disciplined cost control. Our long-term goal remains adjusted EBITDA margins in the high 20% range and the margins of 25.2% in the quarter and 24.7% year-to-date keep us on track to expand from 21.8% in 2025 to about 25% this year. 
The acquisitions of Burton and Mantis will accelerate our progress toward our high 20s goal. Turning to cash flow and the balance sheet on Slide 12. Year-to-date, operating cash flow was $32.9 million compared to $40.1 million a year ago, reflecting a temporary working capital lag in September expected to reverse in Q4. Over the last 12 months, free cash flow was $64.5 million or $4.17 per share. On a long-term basis, we expect free cash flow to exceed 70% of adjusted EBITDA, aided by the $31 million in deferred tax assets on our balance sheet. 
We ended the quarter with $23 million in net debt or 0.2x the trailing 12 months adjusted EBITDA, down from $33 million and 0.3x at the end of the second quarter. After repaying another $5 million on our revolver, we had approximately $174 million in available liquidity at the end of the quarter, including $85 million on our revolver, our $50 million undrawn delayed draw term loan and $39 million in cash. Turning to Slide 13. With the closing of the Mantis transaction after the end of the quarter, this slide shows our capitalization on a pro forma basis, including Mantis and the related financing. 
After reducing our revolver balance to 0 after the September month end, we funded the acquisition of Mantis with a new $250 million term loan and a $35 million draw on our $100 million revolver, bringing total debt to $332 million at the close and net debt to $293 million. This results in net leverage of approximately 2.3x the pro forma trailing 12-month adjusted EBITDA and $154 million in available liquidity for the future. 
We will focus the majority of our strong free cash flow profile on debt reduction and expect to report a net leverage ratio below 2.0x the adjusted EBITDA by the end of the third quarter of 2027. We're comfortable with the state of our balance sheet after completing the Mantis acquisition and expect to continue to support a robust organic growth while exploring smaller acquisition opportunities that expand our markets and accelerate our growth while we reduce leverage. 
Now to Slide 14. Based on our results through the third quarter and visibility into our book of business, we're raising our full year 2026 targets. We now expect net revenue of $435 million to $445 million. Adjusted EBITDA of $109 million to $111 million and adjusted diluted earnings per share of $5.15 to $5.25. This outlook assumes approximately 15.9 million diluted shares and a 0% effective tax rate for the year on GAAP earnings. These numbers include Mantis from October 30 and assume no further acquisitions. 
I'll now turn it back to Mike to preview 2027 on Slide 15.

**Michael Bieber** (Executives):
Yes. Thanks, Kim. So on Slide 15. With less than 2 months to go this year and having closed Mantis, let me provide you a preview of what we think 2027 shape up to look like. We see a continued strong market for our services and anticipate the kind of continued strong execution you come to expect. We're working toward becoming a trusted adviser to our clients. I see this in our work, but investors can also see this because more than 80% of our work comes from the same repeat clients. We've now become a trusted expert at helping solve some of the electricity grid constraints in and around our major metropolitan hubs. 
Coming into 2027, we have a fresh set of new technical capabilities and client relationships. So we'll be focusing on internal cross collaboration. As a company, we've become far more effective at this collaboration and more of our teams are interdisciplinary than ever before. For clients, that means that we can assemble the kind of national expertise they need for their unique challenge. We think this picture will come together in 2027 such that for the first time in the company's history, we will achieve $1 billion in contract revenue, implying about 19% annual growth. That kind of top line number will be complemented by more than $0.5 billion in net revenue. 
We're now expecting more than $140 million in EBITDA for 2027, which represents more than 25% annual growth and continued margin improvement over 2026. Our track record of consistent growth shows that we've got the right management team, the right systems and processes and the right long-term customer relationships to drive us past the $1 billion revenue milestone in 2027. On the last slide, in summary, we've generated record results this year and are raising our 2026 financial targets again. As a reminder, we are on the cusp of achieving an adjusted EBITDA of 48% CAGR over the last 5 years. 
The Burton and Mantis acquisitions in the last 6 months have significantly strengthened our capabilities for commercial and industrial customers and have now equally balanced our customer portfolio. Electric load growth and the massive need for grid modernization are driving the majority of our customers to increase spending. We are in an excellent -- we are an excellent cash generator. So we are targeting to reduce our leverage ratio below 2x by the third quarter next year. And finally, we're introducing preliminary 2027 targets, which continue our double-digit performance and which achieves $1 billion revenue next year. 
Operator, let's now open up the call to questions.

**Operator** (Operator):
[Operator Instructions] Our first question is from Craig Irwin of ROTH Capital Partners.

**Craig Irwin** (Analysts):
First, congratulations on another really solid quarter in here, impressive execution in this market. The equities the last few days have been dominated by concerns about data center, right? You're tripling your business at APG, $75 million this year, up from $25 million last year. And Mantis actually brings you some really interesting assets in that market. Mike, you have a real-world level of visibility on the market right now. The customers obviously talk to you daily because you're executing projects for them. 
Can you maybe talk a little bit about fair expectations for data center that might be included in your guidance for $1 billion in revenue next year? Are you expecting a triple again at APG? Are you expecting Mantis to have a similar growth rate? Or do you have sort of moderated expectations around that? And how fungible are the resources that you have positioned at data center to address some of these significant problems elsewhere in the grid? -- like NYPA, I guess, was a good example that you shared on the call today.

**Michael Bieber** (Executives):
Yes, Craig, this has received obviously a lot of press. I'd characterize it as the political wave running against data centers might allow supply chain and the labor market to catch up with the current demand for data centers. Remember, demand for these data centers is not wavering. It's not going away. No, we're not expecting a major slowdown, major change in what's already happening. Our pipeline goes out past 2029 right now on projects that we've been permitting, evaluating, engineering this year. 
So it's a long -- it's a long-term pipeline. It's receiving a lot of short-term press, and we're not expecting any major changes in the data center world. It's a robust market out there. More importantly for Willdan, though, that we're the people that solve grid constraints. And the grid constraints aren't just coming from data centers, it's climate change I mentioned, electrification. These changes are real across the country. No one factor is driving it. It's multiple factors. 
The grid is just undersized right now for this modern world that we live in. We're in the business of solving that. And so our utility customers, in particular, and even state and local customers have high demand for these types of services that look at constraints, evaluate them, help plan for those changes and alleviate the stress points. Business is good.

**Craig Irwin** (Analysts):
So second question, if I may. Anyone that knows you knows that you're a very conservative guy. You have ambitious goals and you're about to meet one of those with $1 billion in revenue, but you plan for a range of scenarios, right? So when I step back and I look at this Mantis acquisition, I find the property extremely interesting for the lack of overlap between your data center customers, the fact that they're mostly unique to each of the 2 companies. 
And then the fact that Willdan with APG has significant expertise, a great resume in high voltage, while Mantis has a great resume and expertise experience in medium voltage. Can you maybe talk about how transferable these services might be between your customers and whether or not Mantis customers could eventually be served by Willdan. I'm not asking for a time line or specific impact on the revenue outlook. But the bigger picture as far as whether or not these 2 key things sort of fit together longer term.

**Michael Bieber** (Executives):
We think there's a great opportunity here for cross-selling. I mentioned that the cross-collaboration is going to be a primary focus, especially in the next 6 months, and we have our kickoff meeting for that in 2 weeks. We think there's a great opportunity because Mantis is coming, you're right, with a set of blue-chip clients that is all new to Willdan. There's essentially no overlap there and vice versa. So we've got a great opportunity here to focus on cross-selling all of the capabilities and energy that we provide those types of clients.

**Craig Irwin** (Analysts):
Then last question, if I may. You gave us a preliminary look on '27 as far as revenue, net revenue EBITDA. Is it fair for us to expect your free cash flow generation to more or less track your EBITDA in '27 similarly to the way it's developed in '26?

**Creighton Early** (Executives):
Yes, I think that's a fair assumption, Craig. That's what we would expect.

**Craig Irwin** (Analysts):
So more than $100 million in cash flow is probably a fair starting point. Is that something that we can say?

**Creighton Early** (Executives):
Well, we said more than 70% and 70% of $140 million be $98 million. So we are in the right neighborhood, yes.

**Operator** (Operator):
Our next question is from Tim Moore with Clear Street.

**Timothy Michael Moore** (Analysts):
We appreciate you providing preliminary guidance for next year, and it was nice to see that net debt leverage target for next September or so provided. I have a question that is really an industry expertise question. It's a little bit different than the one you just got because mine has been teed up since sunrise yesterday after the election results, partially due to maybe the outcome in the Texas gubernatorial election and even Ohio, we've been getting a lot of calls on this with data center permitting moratoriums and restrictions. 
I just want to bounce off for you, Mike, if you don't mind sharing -- can you kind of show me the rough timing on interconnection permitting? Isn't that usually early design phase? I mean some of these big data centers take 18 to 24 months to construct. So like an interconnection moratorium or a pause really be for data centers that might not power on until late 2028 anyway, right because it's early stages. I'm just kind of trying to wrap our head a little bit better around the delay, and it doesn't seem to be impacting next year's power on because the queue is pretty far out anyway. Just if you could share anything on what you're aware of on just interconnection permitting timing?

**Michael Bieber** (Executives):
It's a great question. I'm glad you asked it because we just researched this. In fact, one of our people put together a chart on this by geography. And interconnection times, by and large, across the country take years. It's not months, it's years. It's a multiyear process typically. And so you really start your other permitting with data centers, you may even design, build, and construct the data center without the interconnect. 
You may be able to operate that if it has additional power sources, which many of these do have. The interconnect may be the last thing that happens. But eventually, most of these data centers do get connected to the grid. It's just way on down the process and generally does not stop from what we've seen the actual upfront, sometimes the design and actual construction of these facilities. multiyear.

**Timothy Michael Moore** (Analysts):
I just had another question on battery energy storage. It's growing so rapidly. Is there any way you could share maybe what your battery energy storage systems maybe are as a percentage of your revenue this year or maybe how much they've grown over the last year?

**Michael Bieber** (Executives):
Good question. I don't have a number on that. I think it's an interesting question. We'll get back to you offline on it. I'm guessing it's in total, 5% or less right now, something like that. You're right, it's growing very quickly. And I just looked at a queue of a bunch of new projects that clients are asking us about. So it's a really interesting area and something that we're very good at. So clients tend to seek out Willdan for that particular expertise.

**Timothy Michael Moore** (Analysts):
I noticed in the last couple of presentations that you had that -- Yes, I mean, BESS is growing 20% to 30%. So I imagine you're doing pretty good with it.

**Operator** (Operator):
Our next question comes from Steven Wahrhaftig from Wedbush Securities.

**Steven Wahrhaftig** (Analysts):
Congrats on another very strong quarter. I kind of want to turn my attention to the fiscal year '27 guidance. I mean the numbers themselves are very strong. We're looking at contract revenue of $1 billion, net revenue of $500 million and then very strong EBITDA numbers. I want to get a better understanding of the split between the commercial, the utilities and the state and local government into fiscal year '27 because you laid out the long term of 1/3, 1/3, 1/3 split between those 3 businesses. But can we get a better understanding of what your expectations are for fiscal year '27 if that's going to be reaching that long-term target? Or what kind of -- what are you baking in there?

**Michael Bieber** (Executives):
No, we're there already on a pro forma basis. So for 2027, it will be about equal 1/3, 1/3, 1/3, for our 3 customer segments.

**Steven Wahrhaftig** (Analysts):
And then was maintained throughout fiscal year '27, is that the assumption? And then for that guidance, I mean, you also got a little bit of an understanding of what that split is going to be between the energy revenue and the rest of the business?

**Michael Bieber** (Executives):
Good question there. From a gross revenue perspective, it's going to revert right now, 15% is in our Engineering segment, and that's going to shrink to more like 10-ish percent of our total revenue, maybe even a little less than that with the remainder 90-plus percent of our revenue being focused on energy and in the Energy segment.

**Steven Wahrhaftig** (Analysts):
And then specifically on the Mantis acquisition because you mentioned how it was originally going to be $120 million of contract revenue. And you mentioned that the margins were a little bit lower from a contract revenue -- from a net revenue standpoint, but it's actually going to generate about $75 million of net revenue. Can you kind of give us a better understanding of what your expectations are from an organic basis? What's really going to drive the organic growth? And what's going to be that split between organic and inorganic heading into fiscal year '27 as well?

**Michael Bieber** (Executives):
Sure. We don't have a bottoms-up on that yet. We're just starting our planning process for Willdan and Mantis for 2027. So we're not going to provide specific guidance on that until late February next year. But if you look historically, and this trend line is continuing right now, it's low double-digit type organic growth business. And we expect that for the rest of Willdan. We're seeing that right now, and we think that's going to continue. So it's similar to the rest of Willdan.

**Steven Wahrhaftig** (Analysts):
And then just last question from me, specifically on the de-leveraging path because it was great to get some color on reaching below 2x by 3Q '27. But if I'm doing the math right, we're getting to around that $100 million of free cash flow, it seems like this is a pretty conservative target. Is that what -- is that why the time line is basically 12 months and not really closer to 6 to 9 months because it seems like it's a very strong cash-generating business and you can pay down that debt pretty aggressively. But does that -- is it more so you're giving yourself wiggle room to do some of those smaller tuck-ins? Or is there something else that I'm missing?

**Creighton Early** (Executives):
Well, the cash flow is -- it's not consistent throughout the year. Our first quarter tends to be a little heavier use of the cash flow. And so first quarter tends to be a little bit weaker. And as you'll see this year in the past couple of years, our fourth quarter tends to be the strongest in terms of the way the cash flow goes. So that's why we're giving ourselves plenty of room there to get through the first quarter. 
We'll have really good cash flow this fourth quarter. So we only got 2 months left of that. Q1 will be a little weaker and then Q2 a little stronger, and it's possible that we reach that goal in the second quarter. But again, just trying to be conservative and making sure that we've got room there then by the third quarter, it should be solidly below the 2.0 mark.

**Operator** (Operator):
This now concludes our question-and-answer session. I would like to turn the floor back over to management for closing remarks.

**Michael Bieber** (Executives):
Well, thank you for your interest in Willdan. We appreciate it very much to all our stakeholders out there. And we will talk to you in late February, where we'll plan to give full year 2027 guidance. Thanks a lot, and talk to you then.

**Operator** (Operator):
Ladies and gentlemen, thank you for your participation today. This concludes today's teleconference call. Please disconnect your lines, and have a wonderful day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### WLDN_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：CFO 上調 2026 全年財測：淨收入、調整後 EBITDA、調整後 EPS 區間（原話："range of $415 million to $430 million"）
- 2026-08-06｜CFO｜guidance：財測假設：全年有效稅率 0%、年底稀釋股數約 15.9 百萬股（原話："a 0% effective tax rate for the year"）
- 2026-08-06｜CFO｜guidance：CFO 稱下半年稅率約 15%–20%，因 179D 效益於 6 月底到期（原話："it's going to be a tax rate somewhere between 15% and 20%"）
- 2026-08-06｜CFO｜guidance：CFO 說 Q3、Q4 大致類似 Q2，Q2 有部分業務自下半年提前認列（原話："Q3 and Q4 are probably going to look something similar"）
- 2026-08-06｜CEO｜guidance：CEO 解釋財測偏保守：LADWP 放量速度為最大變數，可能延至 2027 初（原話："we don't know how quickly LADWP will ramp up"）
- 2026-08-06｜CFO｜margin：Q2 毛利率下滑 150 bp，管理層歸因於收入組合轉向績效工程與商業專案（原話："The gross margin declined 150 basis points"）
- 2026-08-06｜CFO｜margin：管理層說明商業專案毛利較低但間接費用率較低，調整後 EBITDA 利潤率較高（原話："they also carry a lower overhead rate, and resulting higher"）
- 2026-08-06｜CFO｜margin：Q2 調整後 EBITDA 利潤率 28.2%，稱為公司史上單季最高（原話："the highest quarterly margin in the company's history"）
- 2026-08-06｜CFO｜margin：Q2 利潤率不預期全年維持；全年預估約 25%（2025 年 21.8%）（原話："we do not expect that margin to hold throughout the year"）
- 2026-08-06｜CFO｜margin：G&A 占合約收入比由 32.6% 降至 29.3%；股權激勵費用年增 51%（原話："declined to 29.3% of contract revenue"）
- 2026-08-06｜CFO｜margin：Q2 淨收入年增 23%，扣除 Burton 併購的有機成長為 18%（原話："the organic growth rate"）
- 2026-08-06｜CFO｜margin：Q2 帳面含 $5.3 百萬稅務利益，GAAP 淨利 $24.3 百萬（原話："We recognized a $5.3 million tax benefit for the quarter."）
- 2026-08-06｜CFO｜commitment：CFO 重申長期調整後 EBITDA 利潤率目標在高 20% 區間（上季提出）（原話："a clear path to achieving margins in the high 20% range"）
- 2026-08-06｜CFO｜commitment：CFO 稱可將調整後 EBITDA 超過 70% 轉為自由現金流（年度）（原話："convert more than 70% of adjusted EBITDA into free cash flow"）
- 2026-08-06｜CFO｜commitment：CFO 預期（若無新併購）循環信貸於年底前還清（原話："we would expect the revolver to be fully repaid by year-end"）
- 2026-08-06｜CFO｜capital_allocation：季末淨負債 $33 百萬、淨負債/EBITDA 0.3x，總流動性 $165 百萬；Burton 動用 $30 百萬循環信貸，已還 $10 百萬（原話："$165 million in total available liquidity at quarter end"）
- 2026-08-06｜CFO｜capital_allocation：管理層持續尋找併購以擴大服務並加速成長（原話："accelerate growth through acquisition"）
- 2026-08-06｜CFO｜capital_allocation：179D 條款 6 月底到期，但遞延稅資產 $34 百萬仍帶來現金流效益（原話："$34 million in deferred tax assets on our balance sheet"）
- 2026-08-06｜CEO｜customer：CEO 稱商業客戶約占營收四分之一，為第三條支柱（原話："It is currently about a quarter of"）
- 2026-08-06｜CEO｜customer：CEO 稱商業營收中最大部分為資料中心電力，成長最快（原話："is the fastest growing part of Willdan"）
- 2026-08-06｜CEO｜customer：APG 收購貢獻預計今年約 $75 百萬，近乎三倍（原話："is projected to nearly triple this year over"）
- 2026-08-06｜CEO｜customer：LADWP 新增 $110 百萬太陽能路燈合約擴充；CEO 稱 2027 可能成為最大客戶（原話："could be our largest customer in 2027"）
- 2026-08-06｜CEO｜customer：LADWP 擴充案已有一半取得開工授權（原話："authorization to proceed on half of that $110"）
- 2026-08-06｜CEO｜customer：Burton 5/4 完成後自 5 月起新增 Walgreens、Carter's、Five Below 等客戶（原話："relationships with Walgreens, Carter's, and Five Below"）
- 2026-08-06｜CEO｜customer：其他新合約：SoCal REN 5 年 $49 百萬、紐約市立學院 $53 百萬中央電廠升級（原話："a new 5-year, $49 million energy efficiency contract"）
- 2026-08-06｜CEO｜product：Burton 帶來建築 HVAC 與能源控制技術及商業能源採購新業務線（原話："a new line of business in commercial energy procurement"）
- 2026-08-06｜CEO｜product：管理層稱電池儲能機會管線成長，常與規劃、工程、微電網合併（原話："a growing pipeline of battery storage opportunities"）
- 2026-08-06｜CFO｜product：CFO 稱 AI 採用有助效率，是獲利成長快於營收的原因之一（原話："AI adoption"）
- 2026-08-06｜CEO｜competition：CEO 稱加州 REN 正承接傳統投資者擁有公用事業在能效領域的更大角色，後續有更大機會（原話："The California RENs are assuming a larger role"）
- 2026-08-06｜CEO｜risk：CEO 承認 LADWP 放量時程不確定，Q3 貢獻難估（原話："It's too early to tell exactly what the Q3 contribution"）
- 2026-08-06｜CEO｜risk：CEO 稱人才市場偏緊、資深人員薪資上升，但未見人力短缺（原話："but labor is tight."）
- 2026-08-06｜CEO｜risk：CEO 稱資料中心專案遍及全美，並新設佛州、喬治亞、北卡、肯塔基、德州據點（原話："projects in New Mexico and Montana, and some in Utah"）

### 問答異常語氣（迴避／改口／保留）
- WLDN_Q2_2026_Earnings_Call_20260806.md｜問：Wedbush 分析師：本季大幅超預期但財測上調幅度不大，是否缺乏能見度？｜答法：CEO 承認刻意偏保守，歸因於 LADWP 放量速度不確定，未給出下半年具體區間拆解；CFO 僅說 Q3/Q4 類似但略低於 Q2
- WLDN_Q2_2026_Earnings_Call_20260806.md｜問：Roth 分析師：LADWP 專案 Q2 放量情形及下半年走勢｜答法：CEO 自述「we were appropriately conservative, but in fact, we were not」語句前後矛盾，且未給 Q3 數字，稱太早無法判斷

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
{"date":"20260703","verdict":"進場","role":"衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"APG 段 2026-2028 至少 3 倍成長，from ~$37M FY24 → $100-130M FY27","columns":{"2Y 驗證點":"Q2-Q4 FY2026 APG cumulative ≥ $75M；FY27 APG ≥ $110M","5Y 驗證點":"FY30 APG ≥ $200M + 數據中心客戶 ≥ 5 家（去集中）","10Y 驗證點":"FY35 APG ≥ $500M（成 WLDN 最大段）","具體數字門檻":"FY26 APG +100% YoY / FY30 $200M / FY35 $500M","信息來源":"CEO Bieber Q1 FY26 法說「APG more than double 2026」+ backlog 延伸 2027-2028","漂移觸發":"連 2 季 APG YoY &lt; +60% → 削弱；連 4 季 → 反轉"}},{"id":"H2","text":"Adj EBITDA margin 2026-2028 維持 24-26%（FY25 21.8% → FY27 25-26%）","columns":{"2Y 驗證點":"FY26 全年 ≥ 24%（guide $102.5M / $417.5M = 24.6%）；Q2-Q3 連 2 季 ≥ 24%","5Y 驗證點":"FY28 sustainable 25%+ 且 FCF/NI ≥ 1.0","10Y 驗證點":"FY30 達 industry leader 27%+","具體數字門檻":"Q2 FY26 ≥ 24% / FY28 25% / FY30 27%","信息來源":"公司 FY26 guide adj EBITDA $100-105M / net rev $410-425M；FY25 actual $79.5M/$364.8M = 21.8%","漂移觸發":"連 2 季 &lt; 22% → 削弱；連 4 季 → 反轉"}},{"id":"H3","text":"現金轉換 OCF/NI 全年維持 ≥ 1.2、FCF ≥ $70M（證偽 screener「賺不到錢」）","columns":{"2Y 驗證點":"FY26 全年 OCF/NI ≥ 1.2、FCF ≥ $65M（吸收 Q1 營運資金季節後回補）","5Y 驗證點":"FY28 FCF ≥ $110M、FCF/NI ≥ 1.0（roll-up 攤銷後仍現金為王）","10Y 驗證點":"FY32 FCF ≥ $180M、cumulative FCF &gt; 併購支出","具體數字門檻":"FY26 OCF/NI ≥ 1.2 / FY28 FCF $110M","信息來源":"FY25 OCF $80.1M / NI $52.6M = 1.52；FCF $71M（gurufocus / 公司）","漂移觸發":"連 2 季 TTM OCF/NI &lt; 1.0 → 削弱；FY 全年 &lt; 1.0 → 反轉（陷阱重評）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"APG doubling 跳票——1-2 個大型數據中心客戶專案遞延","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季度 APG revenue YoY、法說中 APG 描述 tone","警戒閾值":"Q2 FY26 APG YoY &lt; +80% → 削弱；連 2 季 &lt; +50% → 反轉"}},{"id":"R2","text":"IRA 能效條款 / federal 能效資金被削（QC-39 C 軸法規）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"federal budget、DOE/EPA 預算、utility program funding","警戒閾值":"utility 能效 funding 連 2 季 YoY &lt; +5% → 削弱"}},{"id":"R3","text":"roll-up 整合失敗 / 現金轉換惡化（one-too-many acquisition）","columns":{"對應假設":"H1 / H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"Burton retention / margin 貢獻；APG × Energy Solutions cross-sell；全年 FCF/OCF","警戒閾值":"FY27 全年 OCF/NI &lt; 1.0 或 Burton net rev &lt; $30M → 削弱"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":13.5,"ev5y_pct":80.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星持倉","signal":"A","val":"🟢","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":6.0,"ev5y_pct":80.0,"irr_base_pct":13.5,"max_dd_pct":-45.0,"bull_5y_price":198.0,"bear_5y_price":52.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":76.3,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
