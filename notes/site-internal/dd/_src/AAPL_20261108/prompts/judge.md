你是 stock-analyst **v20 判斷 agent**，標的 AAPL（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"AAPL","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":114.477,"period":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","unit":"十億美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","citation":"Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm"}},{"id":"f_kpi1_gaap","label":"GAAP 營業利益","value":35.631,"period":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","unit":"十億美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","citation":"Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":31.12,"period":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","citation":"Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（35,631÷114,477 自算）"}},{"id":"f_kpi3_gaap","label":"GAAP 毛利率","value":47.9,"period":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","citation":"Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm"}},{"id":"f_kpi7_iphone","label":"iPhone 營收","value":57.583,"period":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","unit":"十億美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","citation":"8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm"}},{"id":"f_kpi8_services","label":"Services 營收","value":31.573,"period":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","unit":"十億美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","citation":"8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-02","period":"2026-11-02","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-02"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_aapl_gross_margin_pct","label":"AAPL 毛利率","value":48.79,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAPL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_aapl_operating_margin_pct","label":"AAPL 營業利益率","value":33.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAPL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_aapl_fcf_margin_pct","label":"AAPL FCF 利潤率","value":28.41,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAPL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_gross_margin_pct","label":"MSFT 毛利率","value":67.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_operating_margin_pct","label":"MSFT 營業利益率","value":47.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_fcf_margin_pct","label":"MSFT FCF 利潤率","value":17.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_gross_margin_pct","label":"GOOGL 毛利率","value":60.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_operating_margin_pct","label":"GOOGL 營業利益率","value":33.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_fcf_margin_pct","label":"GOOGL FCF 利潤率","value":4.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amzn_gross_margin_pct","label":"AMZN 毛利率","value":51.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_operating_margin_pct","label":"AMZN 營業利益率","value":12.89,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_fcf_margin_pct","label":"AMZN FCF 利潤率","value":-6.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sony_gross_margin_pct","label":"SONY 毛利率","value":33.03,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SONY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sony_operating_margin_pct","label":"SONY 營業利益率","value":14.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SONY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sony_fcf_margin_pct","label":"SONY FCF 利潤率","value":12.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SONY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_gaap_eps","label":"GAAP 稀釋 EPS","value":2.1,"period":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","citation":"Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm"}},{"id":"f_kpi5","label":"營運現金流","value":28,"period":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","unit":"十億美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）","citation":"Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results（CFO 談話，約數）"}},{"id":"f_kpi6_sbc_fy2026","label":"SBC 占營業利益（FY2026 全年，非單季）","value":8.72,"period":"FY2026 全年（截至 2026-09-26，公告於 2026-11-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"FY2026 全年（截至 2026-09-26，公告於 2026-11-02）","citation":"8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（13,789÷158,063 自算）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":342.37,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":16.93,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":51.46,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.53,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.45 → 9.5）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.65 → 10.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.82 → 11.82）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":9.5,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":10.65,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":11.82,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":7.95,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 8.8 → 9.5（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":38.13,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":10.39,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":10.47,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":36.04,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 9.5，分子＝快照價 342.37","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.31,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":37757.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 94479.0、現金 56722.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":14532.18,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":5013140.02,"period":"2026-11-08","unit":"USD m","basis":"市值 4975383.02 ＋ 淨負債 37757.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":477692.15,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（37 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":569273.41,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（34 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":10.49,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 342.37 / W52 292.82 / W104 259.47 / W250 208.88 / W250 13週斜率 1.38%"},{"id":"f_ma_w52","label":"52 週均線","value":292.82,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":259.47,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":208.88,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.38,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 自述：Apple 在全球智慧型手機、PC、平板、穿戴市場均為少數份額（minority market share），並警告 AI 能力若落後可能流失份額。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"The Company has a minority market share in the global smartphone, personal computer, tablet and wearables markets, and some of the markets in which the Company competes have from time to time experienced little to no growth or contracted overall.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 自述：競爭對手以激進定價與極低成本結構競爭並模仿產品，部分對手可近乎無利潤甚至虧損銷售。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"Certain competitors have the resources, experience or cost structures to provide products and services at little or no profit or even at a loss.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Counterpoint：2026Q3 蘋果全球智慧型手機份額升至約22%，為首個Q3超過20%，整體市場年減。","source":"AppleWorld.today 引 Counterpoint","url":"https://appleworld.today/2026/10/counterpoint-the-iphone-crosses-20-of-the-global-smartphone-market-share-for-the-first-time/","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"IDC：2026Q3 全球PC出貨年減20.1%，Mac出貨年減11.3%但份額由8.5%升至9.5%。","source":"9to5Mac 引 IDC","url":"https://9to5mac.com/2026/10/08/idc-mac-shipments-drop-11-in-q3-as-global-pc-market-slides-20/","excerpt":"data, Apple shipped 5.9 million Macs during Q3 2026, down 11.3% from 6.7 million in the year-ago period. The overall PC market, however, fell much more sharply, with worldwide shipments dropping 20.1% year over year to 62.7 million units. As a result, Apple’s share of worldwide PC shipments actually increased from 8.5% to 9.5%.","as_of":"2026-10-08","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"IDC：2026Q3 中國智慧型手機市場年減15.4%，華為21.1%居首，蘋果17.8%（去年同期15.8%）。","source":"9to5Mac 引 IDC","url":"https://9to5mac.com/2026/10/13/idc-apple-gains-ground-as-chinas-smartphone-shipments-plunge-15-4-in-q3-2026/","excerpt":"Apple gains ground as China’s smartphone shipments plunge 15.4% In a new report released today, IDC says that rising component costs and retail prices continue to weigh on the broader Chinese smartphone market. According to IDC, Apple accounted for 17.8% of smartphone shipments in China during Q3 2026, up from 15.8% in the year-ago period.","as_of":"2026-10-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 10-K：有一家客戶占應收帳款 10% 以上，2026 年 13%、2025 年 12%；電信業者合計占應收 33%（前一年 34%）；公司對部分客戶要求第三方信用支持或擔保品。","source":"SEC EDGAR 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"As of both September 26, 2026 and September 27, 2025, the Company had one customer that represented 10% or more of total trade receivables, which accounted for 13% and 12%, respectively. The Company’s third-party cellular network carriers accounted for 33% and 34% of total trade receivables as of September 26, 2026 and September 27, 2025, respectively. The Company requires third-party credit support or collateral from certain customers to limit credit risk.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 經間接通路（電信業者、經銷商等）的淨銷售約占總淨銷售 60%。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"During 2026, the Company’s net sales through its indirect distribution channels accounted for approximately 60% of total net sales.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Samsung預期記憶體短缺到2027年會惡化並持續至2028年（AI資料中心搶產能，屬供給面擠壓消費電子）","source":"TechCrunch: Samsung expects memory shortage to worsen through 2027 and last until 2028","url":"https://techcrunch.com/2026/07/31/samsung-expects-memory-shortage-to-worsen-through-2027-and-last-until-2028/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"IDC預估2026全球智慧型手機出貨年減12.9%至約11.2億支，2027年預期小幅回升2%，記憶體價格mid-2027趨穩但不會回到先前水準；平均售價預估創高約523美元","source":"IDC via eeNews Europe / fonearena (2026-02)","url":"https://www.eenewseurope.com/en/smartphone-memory-shortage-2026-idc/","excerpt":null,"as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"後續預測下修2027：Counterpoint 8月預估2027約10.6億支、年減1.4%；Omdia 6月預估年減0.9%；2028預期反彈約+5%（二手彙整，未核原廠）","source":"pctipp.ch: Analysten: Smartphone-Markt wird sich erst 2028 erholen","url":"https://pctipp.ch/themen/business-software/analysten-smartphone-markt-wird-sich-erst-2028-erholen","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"分析師對iPhone 17換機週期是否為前置需求（pull-forward）有分歧：Wedbush稱週期仍有動能；另有報導稱創紀錄季度可能是換機超級週期高點，質疑2027後成長；Goldman估零組件短缺使營收少2-3個百分點","source":"Wedbush via Placera; Technobezz analyst roundup","url":"https://www.placera.se/telegram/apple-s-iphone-supercycle-strong-outlook-drive-momentum-wedbush-says-20260501","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"IDC：2027年下行風險來自可能的庫存堆積","source":"IDC via fonearena","url":"https://www.fonearena.com/blog/?p=476318","excerpt":"are expected to drop by 12.9% year-over-year (YoY), bringing the total market volume down to 1.1 billion units, according to the latest data from the International Data Corporation (IDC) Worldwide Quarterly Mobile Phone Tracker. This contraction marks the lowest annual shipment volume the smartphone market has recorded in more than a decade. Key Driver: The Memory Shortage Crisis","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"歐盟執委會 2025-04-23 依 DMA Art.5(4) 對 Apple 罰 5 億歐元並下令停止限制開發者導流；Apple 已上訴；Art.6(4) 調查已有初步認定，若最終認定違規可罰至全球年淨銷售 10%。","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"On April 23, 2025, the Commission fined the Company €500 million in the Article 5(4) Investigation and issued a cease and desist order requiring the Company to remove technical and commercial restrictions that prevent developers from steering users to alternative distribution channels outside the App Store.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"美國 DOJ 與多州 2024-03-21 提起壟斷訴訟（performance smartphones／smartphones），尋求衡平救濟；另有州與聯邦民事訴訟求償。","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"The DOJ is seeking equitable relief to redress the alleged anticompetitive behavior. In addition, various civil litigation matters have been filed in state and federal courts in the U.S. alleging similar violations of U.S. antitrust laws and seeking monetary damages and other nonmonetary relief.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Google 搜尋授權安排受政府調查與訴訟影響；若上訴推翻，DOJ 原提補救（禁止 Google 向 Apple 提供搜尋分發商業條件）可能生效。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"A reversal of the order on appeal could result in the imposition of certain remedies initially proposed by the DOJ, such as those prohibiting Google from offering the Company commercial terms for search distribution.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"蘋果絕大多數製造由位於中國大陸、印度、日本、南韓、台灣、越南的外包夥伴完成；10-K 風險因素指出貿易限制（關稅與進出口管制）可能對業務與供應鏈造成重大不利影響。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"A significant majority of the Company’s manufacturing is performed in whole or in part by outsourcing partners located primarily in China mainland, India, Japan, South Korea, Taiwan and Vietnam, in addition to sourcing from partners and facilities located in the U.S.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"商務部 232 條款半導體及衍生產品調查初步結果於 2026-01-14 公布，未對蘋果產品加徵額外關稅。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"On January 14, 2026, initial results were published of the previously announced U.S. Department of Commerce investigation under Section 232 of the Trade Expansion Act of 1962, as amended, into imports of semiconductors","as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"最高法院 2026-02-20 判決推翻部分 IEEPA 關稅，蘋果已申請退稅並將收到的退稅列為產品銷貨成本減項。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"Separately, on February 20, 2026, the Supreme Court issued a ruling striking down certain tariffs previously imposed under the International Emergency Economic Powers Act of 1977. The Company has applied for a refund of tariffs paid","as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"FY2026 產品毛利率較 FY2025 上升，主因包含產品組合與關稅退款，部分被含記憶體在內的成本上升抵銷（產品毛利率 39.3% 對 36.8%）。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A Gross Margin","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"Products gross margin and gross margin percentage increased during 2026 compared to 2025 primarily due to product mix and tariff refunds, partially offset by higher costs, including memory.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"報導稱 Apple 2025 年在印度組裝約 5,500 萬支 iPhone，印度約占其全球 iPhone 產量四分之一，動機含降低關稅與地緣風險。","source":"pulse.bot: Apple Now Makes About 25% of iPhones in India After China Pivot","url":"https://www.pulse.bot/large-cap-stocks/news/apple-boosts-iphone-manufacturing-share-in-india-to-25-8691e89c-0e1d-4cfc-8817-6c15b1f37457/","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Apple 處理器由 TSMC 單一供應，地緣衝突、天災或技術故障風險被放大；Apple 約占 TSMC 營收四分之一（較舊報導）。","source":"iMore: Report says Apple's heavy reliance on iPhone chipmaker could be weakness","url":"https://www.imore.com/report-says-apples-heavy-reliance-iphone-chipmaker-could-be-weakness","excerpt":null,"as_of":"2024-01-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Taipei Times（Bloomberg 來源）報導：Apple 供應鏈彈性低於往常、晶片短缺限制成長；TSMC 鳳凰城廠僅產少量 Apple 晶片；Apple 與 Intel、Samsung 有備援代工初步洽談。","source":"Taipei Times 2026-05-06; The Edge Malaysia","url":"https://www.taipeitimes.com/News/biz/archives/2026/05/06/2003856815","excerpt":null,"as_of":"2026-05-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 Q4 營收約 $114.5B（年增約12%）；iPhone 約 $57.6B（+17.5%）、Services 約 $31.6B（+9.8%）、Mac 約 $10.8B（+23.7%）、iPad 約 $6.2B（-10.4%）、Wearables/Home 約 $8.3B（-7.9%）；全年營收 $478.8B（+15.1%）。來自多數媒體彙整，非 Apple 原始稿；MacTrast 早報數字不同。","source":"iClarified / TheDesk.net 報導 Apple FQ4 2026 業績","url":"https://www.iclarified.com/103239/apple-reports-record-q4-revenue-of-1145-billion-307-million-profit","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Counterpoint 初步數據：2026 Q3 Apple 全球智慧機出貨市佔 22%（2025 Q3 為 18%），首度在第三季超過 20%；整體市場年減約 20%；Samsung 23%。","source":"9to5Mac: iPhone hits record Q3 shipment share as global smartphone market plunges 20% per report","url":"https://9to5mac.com/2026/10/12/iphone-hits-record-q3-shipment-share-as-global-smartphone-market-plunges-20-per-report/","excerpt":null,"as_of":"2026-10-12","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"IDC 2026年8月預測：全球智慧機 2026 出貨年減 16.7%（創紀錄），因記憶體短缺 ASP 年增 27.6% 至 $581；Android 預估 -20%，iOS 預測由 -8.1% 上修為 -5.2%。","source":"IDC (idc.com) 2026-08-26 智慧機預測","url":"https://www.idc.com/?p=119475","excerpt":null,"as_of":"2026-08-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Apple 10-K 風險因素自述：市場競爭激烈且技術變化快速，公司必須持續推出新產品、服務與技術並成功管理新技術的轉換與採用。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"Global markets for the Company’s products and services are highly competitive and subject to rapid technological change, and the Company may be unable to compete effectively in these markets.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Tim Cook 公開表示 AI 新裝置是 iPhone 的互補而非替代","source":"9to5mac / wccftech 報導","url":"https://wccftech.com/tim-cook-ai-will-enhance-not-replace-iphone-future-ai-devices/","excerpt":null,"as_of":"2025-08-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Apple 服務主管 Eddy Cue 稱 AI 可能在約十年內取代 iPhone","source":"apfelpatient: Eddy Cue from Apple AI could soon make iPhones obsolete","url":"https://www.apfelpatient.de/en/news/eddy-cue-from-apple-ai-could-soon-make-iphones-obsolete","excerpt":"iPhone 17e AirTags iOS 26 iPhone 17 iPadOS iMac Mac mini Apple TV iPad Pro iPhone Air Apple Vision Pro iPhone 16 AirPods 4 Apple Watch Ultra MacBook Air iPad AirPods Max AirPods Pro 3 Mac Studio Studio Display iPad Air iPad mini watchOS 27 Apple CarPlay Apple Pay watchOS 26 Apple's Eddy Cue: AI could soon make iPhones obsolete","as_of":"2025-05-07","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Apple 智慧眼鏡報導延後至 2027 年底，定位為 iPhone 的配件而非替代","source":"ChannelNews: Apple Smart Glasses Pushed To Late 2027 As Siri Delays Bite","url":"https://www.channelnews.com.au/apple-smart-glasses-pushed-to-late-2027-as-siri-delays-bite/","excerpt":"Home › Latest News › Apple Smart Glasses Pushed To Late 2027 As Siri Delays Bite Apple Smart Glasses Pushed To Late 2027 As Siri Delays Bite Joe Gallop | 01 Jun 2026","as_of":"2026-05-30","retrieved_at":"20261108","affects":["moat_trend","triggers"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K：Apple 透過間接通路（電信商、經銷商）的淨銷售約占總淨銷售 60%，其餘經直營零售、線上商店與直銷團隊；一手文件未載明通路結構性轉變。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"During 2026, the Company’s net sales through its indirect distribution channels accounted for approximately 60% of total net sales.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"報導稱 Apple 付費訂閱達 15 億，Services 營收 307 億美元但出現 2022 年以來首次季減，CFO 歸因於手遊、部分國家 App Store 商業模式變動與美國連結外部付款裁決。","source":"ithinkdiff: Apple Hits 1.5 Billion Paid Subscriptions as Services Growth Slows","url":"https://www.ithinkdiff.com/apple-1-5-billion-paid-subscriptions-services-growth/","excerpt":"Apple Hits 1.5 Billion Paid Subscriptions as Services Growth Slows by Imran HussainJul 31, 2026 Apple announced it has surpassed 1.5 billion paid subscriptions, disclosing the figure alongside its fiscal Q3 2026 earnings on July 30. Services revenue hit $30.7 billion for the quarter, but the segment also posted its first sequential decline since 2022.","as_of":"2026-07-31","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Tickflow 頁面（2026-08-01）：49 位分析師共識 Buy，平均目標價 $327.00。","source":"Tickflow AAPL Stock Forecast","url":"https://www.tickflow.io/stock/AAPL/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 列平均目標價 $330.53（39 位分析師），最高 $400、最低 $200；Wedbush 於 2026-06-09 重申 $400，Morgan Stanley 同日由 $330 調至 $360。目標價分布 as-of 因聚合站而異。","source":"MarketBeat AAPL Forecast","url":"https://www.marketbeat.com/stocks/NASDAQ/AAPL/Forecast/","excerpt":null,"as_of":"2026-06-09","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 頁面：Apple 最近一次指引在 2026-07-30，FQ4 營收指引 $111.69B–$113.74B，較前一區間 $107.2B–$110.02B 上調；同頁營收共識 $113.47B，高於新指引中點約 $112.7B（頁面未明示該共識對應季度）。","source":"Benzinga AAPL earnings forecasts","url":"https://www.benzinga.com/quote/AAPL/earnings-forecasts","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill（2026-10-17）：FY2026 EPS 共識 9.04（45 位分析師）；下一次財報營收預估 3 個月內下修約 0.9%，次一財年 EPS 3 個月上修約 1%。","source":"Chartmill AAPL estimates","url":"https://www.chartmill.com/stock/quote/AAPL/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Barchart：Apple 在財報電話會上指引 6 月季營收年增 14%–17%，高於分析師預期的約 10%；Stocktwits 另報 Cook 警告下一季記憶體成本上升。","source":"Barchart / Stocktwits","url":"https://www.barchart.com/story/news/1633143/apple-nasdaqaapl-posts-better-than-expected-sales-in-q1-cy2026","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"HSBC 於 2026-07-17 由 Hold 升 Buy","source":"Tickerleague AAPL estimates","url":"https://tickerleague.com/companies/AAPL/estimates","excerpt":null,"as_of":"2026-07-17","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026 年 1 月 Apple 證實收購以色列音訊 AI 新創 Q.ai，金額據 FT 報導近 20 億美元，為 Beats 之後第二大收購","source":"MacRumors：Apple Just Made Its Second-Biggest Acquisition Ever After Beats","url":"https://www.macrumors.com/2026/01/29/apple-second-biggest-acquisition-ever/","excerpt":"Apple confirmed to Reuters that it bought the Israeli startup, which focuses on AI for audio. Apple paid close to $2 billion for Q.ai, according to sources cited by the Financial Times.","as_of":"2026-01-29","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"股東集體訴訟（Siri AI 與 Epic 合規）Apple 於 2026-02 聲請駁回，南韓國民年金為首席原告；無駁回裁定紀錄","source":"MacRumors：Apple Asks Judge to Toss Fraud Claims Over Siri AI, Epic Compliance","url":"https://www.macrumors.com/2026/02/27/apple-asks-judge-toss-fraud-claims-siri-epic/","excerpt":"Apple urged a federal judge to dismiss the proposed class action, filed in federal court in San Francisco.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"10-K（FY2026）Legal Proceedings：歐盟 DMA 5(4) 調查罰款 5 億歐元並已上訴；6(4) 調查有初步認定；美國 DOJ 反壟斷訴訟進行中","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"On April 23, 2025, the Commission fined the Company €500 million in the Article 5(4) Investigation and issued a cease and desist order requiring the Company to remove technical and commercial restrictions that prevent developers from steering users to alternative distribution channels outside the App Store.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R","moat_trend"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 9 份 8-K 中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01）者 0 份","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026 年 1 月 Apple 證實收購 Q.ai，金額近 20 億美元（FT 報導）","source":"MacRumors：Apple Just Made Its Second-Biggest Acquisition Ever After Beats","url":"https://www.macrumors.com/2026/01/29/apple-second-biggest-acquisition-ever/","excerpt":"Apple confirmed to Reuters that it bought the Israeli startup, which focuses on AI for audio. Apple paid close to $2 billion for Q.ai, according to sources cited by the Financial Times.","as_of":"2026-01-29","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"股東證券詐欺集體訴訟（Siri AI、Epic 合規）Apple 2026-02 聲請駁回，無裁定紀錄","source":"MacRumors","url":"https://www.macrumors.com/2026/02/27/apple-asks-judge-toss-fraud-claims-siri-epic/","excerpt":"Apple urged a federal judge to dismiss the proposed class action, filed in federal court in San Francisco.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K 披露 DOJ 反壟斷訴訟與歐盟 DMA 罰款 5 億歐元（已上訴）","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm","excerpt":"On March 21, 2024, the DOJ and a number of state and district attorneys general filed a civil antitrust lawsuit in the U.S. District Court for the District of New Jersey against the Company alleging monopolization or attempted monopolization in the markets for “performance smartphones” and “smartphones” in violation of U.S. antitrust laws.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 無 4.02（財報不可信賴）等重大項目；搜尋亦無 SEC 調查或重編紀錄","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"AAPL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.79,"operating_margin_pct":33.01,"fcf_margin_pct":28.41,"rd_intensity_pct":9.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAPL","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"MSFT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.66,"operating_margin_pct":47.1,"fcf_margin_pct":17.31,"rd_intensity_pct":10.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"GOOGL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.86,"operating_margin_pct":33.32,"fcf_margin_pct":4.19,"rd_intensity_pct":15.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"AMZN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":51.08,"operating_margin_pct":12.89,"fcf_margin_pct":-6.38,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SONY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":33.03,"operating_margin_pct":14.6,"fcf_margin_pct":12.4,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SONY","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"AAPL"},"financial_history":{"ticker":"AAPL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-09-30","revenue":383285000000.0,"revenue_yoy_pct":null,"gross_margin_pct":44.13,"operating_margin_pct":29.82,"net_income":96995000000.0,"diluted_eps":6.13,"free_cash_flow":99584000000.0,"fcf_margin_pct":25.98,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":391035000000.0,"revenue_yoy_pct":2.02,"gross_margin_pct":46.21,"operating_margin_pct":31.51,"net_income":93736000000.0,"diluted_eps":6.08,"free_cash_flow":108807000000.0,"fcf_margin_pct":27.83,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":416161000000.0,"revenue_yoy_pct":6.43,"gross_margin_pct":46.91,"operating_margin_pct":31.97,"net_income":112010000000.0,"diluted_eps":7.46,"free_cash_flow":98767000000.0,"fcf_margin_pct":23.73,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-09-30","revenue":478834000000.0,"revenue_yoy_pct":15.06,"gross_margin_pct":48.79,"operating_margin_pct":33.01,"net_income":132175000000.0,"diluted_eps":8.98,"free_cash_flow":136056000000.0,"fcf_margin_pct":28.41,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/AAPL/AAPL_Q4_2026_Earnings_Call_20261102.md）

# Q4 2026 Earnings Call
**Apple Inc.** | Earnings Calls | 2026-11-02

**Suhasini Chandramouli** (Executives):
Good afternoon, and welcome to the Apple Q4 Fiscal Year 2026 Earnings Conference Call. My name is Suhasini Chandramouli, Head of Investor Relations. Today's call is being recorded. Speaking first today is Apple's CEO, John Ternus; and he'll be followed by CFO, Kevan Parekh. After that, we'll open the call to questions from analysts.
Please note that some of the information you'll hear during our discussion today will consist of forward-looking statements, including, without limitation, those regarding revenue, gross margin, operating expenses, other income and expense, taxes and future business outlook. These statements involve risks and uncertainties that may cause actual results or trends to differ materially from our forecast, including risks related to the potential impact to the company's business and results of operations from macroeconomic conditions, tariffs and other measures, and legal and regulatory proceedings. 
For more information, please refer to the risk factors discussed in Apple's most recently filed reports on Form 10-Q and Form 10-K, and the Form 8-K filed with the SEC today, along with the associated press release. Additional information will also be in our report on Form 10-K for the year ended September 26, 2026, to be filed tomorrow, and in other reports and filings we make with the SEC. Apple assumes no obligation to update any forward-looking statements, which speak only as of the date they are made. I'd now like to turn the call over to John for introductory remarks.

**John Ternus** (Executives):
Thank you, Suhasini. Hello, everyone, and thanks for joining us. It's a privilege to be with you for the first time as Apple's CEO. I'm honored to represent our teams and the work they do every day. Today, Apple is pleased to report $114.5 billion in revenue, up 12% from a year ago, and a September quarter record. These results helped Apple achieve its best-ever fiscal year for revenue and EPS. This is an amazing time at Apple. We just completed one of the most prolific launch periods in our history. It's been a remarkable time for innovation across all of our categories. One of the greatest testaments to that is the all-new iPhone Duo, the most transformational iPhone since the original. 
We're also incredibly excited about iPhone 18 Pro and 18 Pro Max, which take massive leaps forward on camera, battery life and performance, features that our users care deeply about. Meanwhile, touch has arrived on Mac for the first time with the all-new MacBook Pro, and we were excited to announce the new iMac and 14-inch MacBook Pro. The all-new iPad mini features a stunning new OLED display and brings a super-thin design to the smallest member of the iPad family. Apple Watch now offers users the clearest window yet into their heart health. We introduced AirPods 5, which feature industry-leading active noise cancellation in an open-ear design. And we've laid the foundation for an even more intelligent smart home with the all-new HomeView, Apple TV 4K and HomePod mini. 
On top of it all, we're unlocking more powerful AI experiences across our lineup, including with the all-new Siri AI, a profoundly capable and deeply personal assistant seamlessly integrated across our platforms. And like everything we make, Siri AI is built with essential privacy protections, so no one can access users' data, not even Apple. We launched Siri AI in beta for U.S. English users in September and expanded to French, Japanese, Korean, Portuguese and Spanish in October. We're really excited to have rolled all these innovations out, and there's still so much more we plan to do. I'm feeling great about the opportunities ahead for Apple from our product road map and broad range of services to promising areas like health, emerging markets, enterprise and education. 
As one example, we recently secured our biggest education deal ever for Mac with the Department of Education in the Philippines. They're going to deploy 170,000 MacBook Neos to teachers and staff. Opportunities like this bring more users into our ecosystem and help fuel growth across our business. Apple is the greatest company in the world. We've assembled an extraordinary collection of talent, the best engineers, designers, developers and experts in every corner of our business, from our supply chain to our stores. Every day, we bring the right people together with the best ideas to build products and services that change lives, guided by a foundational set of values and a belief that the best technology should make a better world. 
We do that by making products that are powerful and intuitive and meet Apple's uncompromising standards for quality, performance, design and durability. That's the Apple experience customers love. And with our latest lineup, people have even more reasons than ever to upgrade or switch to an Apple product. At the same time, Apple services amplify the experience of every device, helping people work, play, listen, watch and stay connected to the world around them. I'm delighted with where our services business is today and where it's going. And with an installed base of more than 2.5 billion active devices, I'm looking forward to expanding our offerings and improving the lives of users around the world. 
We see tremendous opportunity in AI as well. Siri AI marks a new chapter in AI at Apple. It is a completely reimagined assistant that is powerful, personal, private and deeply relevant to our users' daily lives. Siri AI picks up what's relevant to our users, understands what's on their screen and holds a natural conversation, all to help them with the things they do every day. It's the Siri we've always wanted. We are very pleased with the reviews and feedback we've received, and we're so excited that more and more users are getting to experience it. iPhone remains at the center of our opportunity as the intelligent personal hub. It's always with you and understands your personal context from your messages to your photos, notes and apps, to deliver powerful intelligence right when you need it.
Then there's Mac, which is having an AI moment all its own. Mac is what brought me to Apple, and through the years, it has opened a world of possibilities. More than 40 years after the first Mac, the category is having its biggest moment yet, with every Mac in our latest lineup a powerful platform for AI. Mac mini and Mac Studio in particular are pushing the boundaries of local, private AI, giving users the ability to do things once considered impossible. From Mac to iPhone to iPad, we are proud that our products are the best platforms in the industry for AI, for both first-party and third-party applications, and we're excited about the opportunities that creates. Ultimately, everything we do at Apple is for our users. The success of every innovation is best measured by its impact on people's lives, and that's what drives us to keep building great products and to get them into the hands of people all around the world.
Now let's take a deeper dive into our results for the quarter. As I mentioned earlier, we had an excellent quarter at Apple. In addition to September quarter and fiscal year records in total company revenue, iPhone set a September quarter revenue record, capping its best fiscal year ever. Services achieved an all-time record during the quarter to close out our best year ever there, too. We grew in the vast majority of markets we track, setting September quarter records in the Americas, Europe, Greater China and the rest of Asia Pacific. We also set September quarter revenue records in both developed and emerging markets, in addition to an all-time record in India.
Turning to our lineup. iPhone revenue was $57.6 billion for the September quarter, up 17% from a year ago, despite supply constraints and foreign exchange headwinds. We grew strong double digits in the U.S. and Greater China to achieve September quarter revenue records. We also set a September quarter record for upgraders worldwide, as well as in the U.S., China Mainland and India, helping to deliver our best fiscal year ever for upgraders globally. 
At the launch in September, we introduced the all-new iPhone Duo. From the very beginning, we knew what we wanted to create, a foldable form factor with a larger display that feels as natural and intuitive as iPad. We designed the hardware and software together to make it unmistakably iPhone, while enabling entirely new ways to use it. The result is a series of remarkable innovations that we believe will redefine what a foldable phone can be. We're so proud of what our teams have built. Developers have been quickly adapting to this new form factor, and we're excited to see more and more apps optimized for iPhone Duo. We've been thrilled with the early response from reviewers and customers, and we are working hard to get iPhone Duo into customers' hands as quickly as we can.
We have also been thrilled with the response to iPhone 18 Pro and Pro Max. It's easy to see why customers are embracing them. Our latest models feature a dramatically improved camera system with breakthrough upgrades like variable aperture and all-new photographic styles. The A20 Pro and next-generation vapor chamber together deliver the highest sustained performance in iPhone history. And iPhone 18 Pro Max delivers the biggest increase in battery life ever on an iPhone. A20 Pro also features a new dual 16-core Neural Engine, accelerating on-device AI and computational photography.
Turning to Mac. Revenue was $10.8 billion, up 24% from a year ago, despite supply constraints. We had double-digit growth in the majority of markets we track, and particularly strong performance in our emerging markets, where we set a September quarter revenue record. We also set a September quarter record for customers new to the Mac. According to IDC, we gained share globally during the quarter and for the full fiscal year, and we have never sold more Macs in a fiscal year than we did this time, which is a truly remarkable testament to these incredible products. 
Last week, we introduced a whole new way for people to experience Mac. The all-new MacBook Pro with PROLED XDR brings touch to the Mac for the first time. It also boasts the best Pro laptop display we have ever shipped, plus all-day battery and our most immersive laptop audio. And it all comes together in a thinner and lighter design. We also brought the power of M6 to the new 14-inch MacBook Pro and the new iMac. This latest generation of Apple silicon includes the world's fastest CPU core to speed up everyday tasks, in addition to a dual 16-core Neural Engine to drive private on-device AI tasks.
Now turning to iPad, where revenue was $6.2 billion for the September quarter. Last week, we introduced the all-new iPad mini with an amazing new OLED display, super-thin design and the power of A20 Pro. With the newest addition, our iPad lineup is more capable and versatile than ever before. Anywhere our users go, there's a place for iPad, like a classroom, where it helps students explore the world in amazing ways, or a design studio, giving artists and creatives an expansive canvas to explore their ideas. 
In Wearables, Home and Accessories, revenue was $8.3 billion for the September quarter. Apple Watch makes the simple act of wearing a watch a powerful way to help take care of your health. We were thrilled to introduce our all-new Health Sensing System to help our users get the most out of health tracking. Paired with the S11 chip, Apple's most powerful wearable chip, the Health Sensing System delivers the most accurate heart rate sensing in a wearable. We were also happy to unveil new features like Health Age and Readiness, which will tell you when to push forward or hold back, as well as the all-new Health app redesign. 
And we're excited for Audio Intelligence, which will be coming in a future software update and will help you remember moments you might otherwise miss. Apple Watch Series 12 brings it all together in a beautifully light design, while Apple Watch Ultra 4 goes further with longer battery life compared to the previous generation and the most accurate on-device GPS in a sports watch. 
Meanwhile, AirPods 5 offers best-in-class open-ear active noise cancellation at an incredible price, while improving sound quality, battery life and durability. With iPhone and Apple Intelligence, including Siri AI, AirPods allow users to do remarkable things, like connect with someone who's speaking another language with live translation or get answers with broad world knowledge entirely hands-free. 
And just a few weeks ago, we introduced a whole new generation of hardware for the home. That includes Apple HomeView, which was designed to be central to the home and personal to everyone in it, bringing entertainment, connection and home management together in one place. We announced this alongside the new Apple TV 4K, now smarter with Apple Intelligence, the all-new HomePod mini and Apple Home Collection, a new program that extends Apple Home beyond our own products through deep collaboration with key partners. All of it, as always, is built on Apple's approach to privacy.
Now let's turn to services. Revenue was $31.6 billion, up 10% from a year ago, and an all-time record. We saw double-digit growth in the majority of markets that we track, and we set all-time revenue records in the Americas and Europe, as well as the September quarter record in the rest of Asia Pacific. The 78th Primetime Emmy Awards were a night to remember for Apple TV, with our shows earning more awards than any other network. Widow's Bay, the show of the summer, became the most awarded comedy ever in a single year with 14 wins. We're very excited about our programming from fan favorites like Slow Horses and Ted Lasso to the upcoming film Being Heumann. To date, Apple TV productions have earned more than 900 wins and over 3,800 nominations. 
Turning to Apple Pay. We recently launched in India with Axis Bank, bringing a seamless, safe and secure way to pay in one of the biggest markets in the world. Today, Apple Pay is available in over 90 markets, giving customers around the world peace of mind built into every transaction. Apple Music was created to bring artists and fans closer together, and with the opening of Apple Music Hall, we have a beautiful new venue for intimate shows that bring them even closer. To celebrate the opening of the site in London, we hosted an unforgettable performance by Elton John. 
People love Apple products and services for the countless ways they make life easier, more enjoyable and just plain better. They also count on Apple to create technology responsibly, built the right way, not the easy way. That means building products with even more recycled content to take less from the earth and with even better durability so they last longer. It means developing intelligent capabilities like sound recognition on Apple Watch to alert users who are deaf or hard of hearing to what's happening around them. It means designing privacy protections like on-device processing so personal data stays on a user's device. And it means introducing new child safety features to make it easier for parents to manage when and how their kids can use their devices. 
We're also pleased to be doing more and more manufacturing in the United States. Through our American Manufacturing Program, we're deepening partnerships with suppliers across the country, including Perryman, a titanium producer now supplying iPhone Duo, and Qnity Electronics, which is producing the camera technology behind iPhone 18 Pro's new variable aperture system. Nearly 100 components in our newest iPhones come from American companies in more than a dozen states. All told, Apple supports more than 450,000 American jobs with thousands of suppliers and partners across all 50 states. It's all part of our $600 billion 4-year commitment to U.S. innovation and advanced manufacturing. I am proud of what we've accomplished this quarter, and I'm excited for what's ahead. We have everything we need to be extraordinarily successful. And with this team, this vision, this mission and these values, I have no doubt that we will. With that, I'll hand it over to Kevan.

**Kevan Parekh** (Executives):
Thanks, John, and good afternoon, everyone. Here's a quick rundown of our key financial metrics. Our revenue of $114.5 billion was up 12% year-over-year, a September quarter revenue record. This strong performance was despite sequential foreign exchange headwinds of nearly 2 percentage points, as well as supply constraints on iPhone, Mac and iPad. Products revenue was $82.9 billion, up 12% year-over-year, driven by strong double-digit growth on iPhone and Mac. Our installed base of over 2.5 billion active devices has reached another all-time high across all major product categories and geographic segments. Services revenue was $31.6 billion, up 10% year-over-year. We saw strong performance in many services categories with all-time records in video, cloud services, payment services and advertising, and a September quarter record in music. 
Company gross margin was 47.9%, and products gross margin was 37.2%. These both included a benefit from tariff refunds, which had a favorable impact of approximately 1 percentage point in the September quarter. When you remove the tariff refunds from both the June and September quarter, both company and products gross margin would be down about 1 point sequentially, primarily driven by higher memory costs. As of the September quarter, we have received the vast majority of the refunds related to tariffs paid. Services gross margin was 76%, up 40 basis points sequentially. Operating expenses came in at $19.2 billion, up 21% year-over-year, as we continued to make investments in R&D. 
Net income was $30.7 billion. Diluted earnings per share was $2.10, up 14% year-over-year, and included $0.05 of favorable impact from tariff refunds. Both net income and EPS set September quarter records, even when excluding the tariff refund benefit. Operating cash flow was also very strong at $28.1 billion. This performance marked our best fiscal year yet, with $478.8 billion in revenue, up 15% year-over-year, and a fiscal year record for EPS of $8.98, up 20% year-over-year.
Now I'm going to provide some more details for each of our revenue categories. iPhone revenue was $57.6 billion, up 17% year-over-year, despite supply constraints. We grew double digits in the majority of markets we track, and we also reached September quarter revenue records across both developed and emerging markets. As John mentioned, it was a record year for the total company, and we also had our best year ever for iPhone, both worldwide and in every geographic segment. The iPhone active installed base grew to an all-time high, and iPhone had a record year for upgraders globally and in several markets, including the U.S., China Mainland, India and Japan. According to a recent survey from Worldpanel, iPhone was a top-selling model in the U.S., urban China, India, the U.K., Germany, Australia and Japan. 
Mac revenue was $10.8 billion, up 24% year-over-year, despite supply constraints. This performance was driven by the strength of the MacBook Neo and MacBook Pro. We saw double-digit growth in both developed and emerging markets, with all-time records in markets like India and Southeast Asia. Emerging markets continued to see strong performance on Mac, resulting in Mac's best fiscal year there, driven by record upgraders and customers new to the Mac. iPad revenue was $6.2 billion, down 10% year-over-year, driven by the supply constraints I mentioned earlier, as well as a continued difficult compare against the launch of the A16-powered iPad in the prior year. The iPad installed base reached an all-time high during the quarter, and over half of the customers who purchased an iPad were new to the product. 
Wearables, Home and Accessories revenue was $8.3 billion, down 8% year-over-year, as we faced a difficult compare against the launch of the Watch SE 3 and the AirPods Pro 3 in the prior year. The wearables installed base reached a new all-time high, and over half of customers who bought an Apple Watch in the quarter were new to the product. Services revenue set an all-time record of $31.6 billion, up 10% year-over-year, despite over 1.5 points of sequential FX headwinds. We set all-time revenue records in the majority of markets we track, including several emerging markets like Latin America and India. We are optimistic about the long-term future of our services business. 
With our large installed base of over 2.5 billion active devices, we have an incredibly strong foundation for growth opportunities. Our services continue to attract more customers, and both transacting and paid accounts reached new all-time highs in the quarter. We also have over 1.5 billion paid subscriptions, which grew double digits during the quarter, reaching an all-time high. And we continue to improve and expand our services offerings from iCloud+ plans that now include Apple TV and Apple Arcade in more than 100 countries and regions to ads in Apple Maps now live in the U.S. and Canada, which will give local businesses a new way to reach customers while respecting our users' privacy. 
Turning now to enterprise. Organizations are continuing to expand their fleets of Apple devices to transform operations and drive productivity. Duke Health performed the first surgical procedure using Apple Vision Pro for hip arthroscopy with an FDA-authorized app from Stryker. American Airlines is deploying over 37,000 iPhone 17 devices to flight attendants for in-flight purchases with tap to pay, in addition to 25,000 iPads for pilots and mechanics. And more companies are choosing Mac across a growing range of use cases, including for on-device AI. For example, Gap Inc. is running AI entirely on Mac mini for loss prevention across hundreds of stores, eliminating cloud token costs. Christie's, a world-leading auction house, is running local models on Mac Studio to improve core productivity workflows such as pricing estimates.
Let's turn to our cash position and capital return program. We ended the quarter with $137 billion in cash and marketable securities and $80 billion in total debt. During the quarter, we returned $28 billion to shareholders. This included $3.9 billion in dividends and equivalents and $24 billion in share repurchases. As we move ahead into the December quarter, I'd like to review our outlook, which includes the types of forward-looking information that Suhasini referred to. Importantly, the color we're providing assumes that global tariff rates, policies and their application remain in effect as of this call, and the global macroeconomic outlook does not worsen from today. We expect our December quarter total company revenue to grow between 7% and 10% year-over-year, which reflects our best view of constrained supply. We expect this to be the best quarter for revenue in the history of the company. 
We expect services revenue to grow between 8% and 9% year-over-year in the December quarter. This contemplates sequential headwinds primarily driven by third-party licensing and foreign exchange. We expect gross margin to be between 45% and 46%. This includes primarily the impact of higher memory costs, as well as some costs related to the ramp of Siri AI. We expect operating expenses to be between $20.4 billion and $20.8 billion. We expect OI&E to be around $300 million, excluding any potential impact from the mark-to-market of minority investments, and our tax rate to be around 17%. Finally, today, our Board of Directors has declared a cash dividend of $0.27 per share of common stock payable on November 16, 2026, to shareholders of record as of November 12, 2026. With that, I'll hand it back to John.

**John Ternus** (Executives):
Thanks, Kevan. Before we get into questions, I'd like to introduce Sabih Khan, Apple's Chief Operating Officer. Many of you know Sabih from his work with worldwide operations and supply chain, leading many important functions at Apple, including manufacturing, AppleCare, environmental efforts and supplier partnerships around the world. Sabih and his team are the reason we're able to build and deliver products at a scale and of a caliber unlike anyone else out there. I've asked Sabih to join Kevan and me on these calls as we take your questions.

**Suhasini Chandramouli** (Executives):
Thank you, John. We ask that you limit yourself to 2 questions. Operator, may we have the first question, please?

**Operator** (Operator):
Our first question is from Michael Ng of Goldman Sachs.

**Michael Ng** (Analysts):
I have 2. First, on the iPhone 18, the standard model was left out of the September lineup. I was just wondering if you could share some of the reasons why, whether there were some supply constraints and component-related things that led to that decision, or if it had to do with the launch of the Duo? Any color there would be helpful. And then I have a follow-up.

**John Ternus** (Executives):
Yes. Thanks, Michael. Look, we were thrilled to introduce the iPhone Duo and 18 Pro earlier this year in September. And we have iPhone 17, iPhone Air and 17e continuing to kind of round out this incredibly strong lineup for the holidays. So obviously, we don't make any comments about future road map, but we're excited about where we're at.

**Michael Ng** (Analysts):
Great. And then my second question is just around iCloud+. It seems like it's becoming a more strategic product, just given the tie-in with home security as well as the potential monetization opportunity for Apple Intelligence. So I was just wondering, what are you seeing on iCloud+? Are there any tailwinds in terms of attach rates, just particularly given the rising cost for increased storage options on iPhone and the company's push into home products?

**John Ternus** (Executives):
Yes. Thanks for the question. I think we just, in the September quarter, had an all-time record for our cloud services for revenue. And you mentioned iCloud+. This is something we're very excited about. We have these iCloud+ plans that now include Apple TV and Apple Arcade in more than 100 countries and regions where we think we can really reach new potential subscribers. 
And then, as you mentioned, we think there's good opportunities on Apple Intelligence. There's going to be some usage limits on features that rely on server-side models, which include Siri AI and intelligent photo editing and some other things like that. And so anyone who needs greater capacity will be able to purchase expanded access in the future. So kind of to your point, in the beginning, iCloud tiers were largely about storage, but we've been adding more capabilities and features to it.

**Operator** (Operator):
Our next question is from Erik Woodring from Morgan Stanley.

**Erik Woodring** (Analysts):
John, congrats on your first quarter here. So as the world of AI evolves from chatbots to consumer agents, it seems like there are growing opportunities for Apple. It also seems like there are risks. And John, I'd just love to get your perspective on what role you want Apple and Siri AI to play in kind of this consumer agentic AI landscape? And just how you look at any potential risks of some of these agents trying to encroach on your services business? And then a quick follow-up, please.

**John Ternus** (Executives):
Sure. Thanks, Erik. Look, we -- first and foremost, we are incredibly excited to launch Siri AI alongside the latest generation of Apple Intelligence features. Siri has long been popular with our users, with more than 2.5 billion requests every day. And with Siri AI, we really have the kind of the Siri that we always wanted. It's primarily request-based today. But as we talked about at WWDC, it's built on a modern orchestrator-driven architecture that gives us real room to expand its capabilities over time. 
As far as agentic capabilities, we think these are promising tools for users. We just want to make sure that users are aware of what they're giving access to. We want to make sure this is done in a way that protects security and privacy. So we're pushing really hard on that with Siri AI, but we're also really encouraged the fact that Apple devices, we think, are the best places to use all forms of AI.

**Erik Woodring** (Analysts):
Okay. Awesome. I appreciate that, John. And then just quickly as a follow-up, how should we -- if we take a big step back, how should we think about the durability of services growth? Just I realize that was 10% in the September quarter. We're a little bit below that in the December quarter. As certain things like search evolves and regulatory changes impact App Store monetization, are there new services that we should be looking towards that you believe can become a more sizable offset to maybe take some pressure off these historically important revenue streams?

**Kevan Parekh** (Executives):
Erik, it's Kevan. Thanks for the question. Let me take this one. Let me start by just talking through kind of what we did -- we talked about during the September quarter, services grew by 10% year-over-year. And we look at that relative to the June quarter, foreign exchange was the main driver in that change on year-on-year growth rate sequentially. We saw -- we continue to see strong performance in September in many of our service categories, all-time records in video, cloud services, payment services and advertising, including our first-party Apple Ads, and September quarter record in music. 
But I think it's important to kind of step back also and look at the progression of what we see in our services business over the last several quarters. I think it's an important backdrop. And so we spoke about in the last call, we expected foreign exchange to be the largest driver of the change in the year-on-year growth rate from the March to September quarter. This ended up being a significant headwind of about 4 percentage points, and we expect additional sequential headwind of about another 0.5 percentage point for the services business as we go into the December quarter.
We've also seen some factors that impacted the performance of the App Store. And during the September quarter, the performance on the App Store was similar to the prior year, and we had a record number of paid subscriptions with double-digit growth for third-party apps on the App Store. At the same time, we did see some headwinds in mobile gaming that we've talked about before and expect to see those continue into the December quarter. And keep in mind, we also made some changes to the App Store business model in certain countries. And in the U.S., we continue to operate under a court ruling impacting the link-out transactions.
As we move ahead, we expect services growth to be between 8% to 9%, as I mentioned in the prepared remarks, in the December quarter, and this outlook contemplates our best estimates on sequential headwinds, primarily from third-party licensing and the additional 0.5 percentage point of foreign exchange I just mentioned. And I'll turn it over to John to talk about some perspectives as we look ahead.

**John Ternus** (Executives):
Yes. Thanks. I guess I'd like to add to that, Erik. I think, fundamentally, we feel really good about the long-term opportunity that we have in our services business. We see continued growth in the installed base of over 2.5 billion active devices, which is fundamentally the foundation for future growth as more customers are able to experience our products and services. Example of this, during the September quarter, App Store saw a record number of nearly 1 billion average weekly visitors, and we saw growth in the number of users who are paying for at least one service, reaching an all-time high. Another good example of this, in India, we recently launched Apple Pay with Axis Bank, bringing the seamless, safe, secure way to pay to one of the biggest markets in the world. And then on top of all this, as we talked about, we think intelligence is going to be another opportunity as well. So overall, we're feeling really good about where we're headed in the long term.

**Operator** (Operator):
Our next question is from Amit Daryanani from Evercore.

**Amit Daryanani** (Analysts):
Congrats on mine as well, John, on your first earnings call here. John, you sort of described the iPhone as the intelligent personal hub in your opening comments. And as personal AI agents become more prominent, do you see the potential for the primary customer relationship to shift from the device to the agent over time? And really, given Apple's integration of silicon, hardware and software, where do you see the greatest opportunity to combine things like personal context and on-screen awareness into an agent that can perhaps move beyond answering questions? And how far along do you think Siri is in bringing those pieces together right now?

**John Ternus** (Executives):
Yes. Thank you, Amit, for the question. As I said before, and we said in our announcement, we really do think of the iPhone as the intelligent personal hub. I mean if you think about it, so much of your personal data is on your iPhone, whether it's your contacts, your communications, health data, financial data, all of that. And Siri can tap into that and help you access it in a way that's very secure and private and that nobody else has access to, even Apple doesn't have access to it. And so we think that is a core kind of differentiator that we're excited about, and we're going to continue to push on that. And so I think this is an area that we feel really, really good about.

**Amit Daryanani** (Analysts):
Got it. And then, Kevan, the December quarter gross margin, I'm wondering if you'd spend a bit of time on that. I think if I exclude all the tariff refunds, you started implying gross margin would be down about 140 basis points sequentially at least. Can you separate how much of this is maybe commodity memory inflation versus mix versus -- you called out Siri AI ramp costs as well. Could you just talk about what the different moving parts are as we think about the sequential gross margins, that would be helpful.

**Kevan Parekh** (Executives):
Yes, Amit, sounds good. Let me try to address that for you. So as you alluded, for the December quarter, we talked about a gross margin outlook of between 45% and 46%. As you said, when you remove the benefit of the tariff refunds in September, the midpoint of the range is a decline sequentially in the magnitude you mentioned. We expect most of that decline to be driven by higher memory costs, and I'll give John kind of the mic here to give you a perspective on that, and then I'll take the balance of your question.

**John Ternus** (Executives):
Yes. Let me give you an overall view on memory. What we're seeing with memory pricing right now is unprecedented. And as we said earlier in the September quarter, we did see higher memory costs as compared to the June quarter, which were partly offset by the benefit of carry-in inventory and lower costs on certain non-memory components. Now for the December quarter, we expect even higher memory costs, partly offset by a few factors. So as you know, we changed the price on many of our products, including Mac and iPad at the end of June and iPhone in September, and these price increases provided some offset. 
We also expect to see some benefit from carry-in inventory in the December quarter as well, as well as lower costs on certain non-memory components. And looking beyond the December quarter, we see the pricing for memory purchases continuing to increase. As we said before, we do believe we'll see a decreasing benefit from the carry-in inventory on memory over time. And there's one more thing I wanted to add. As we work to improve supply, our manufacturing purchase obligations have increased by $33 billion from June to the September quarter, which you'll see in our annual filing when it comes out tomorrow. Now back to Kevan for the other parts of it.

**Kevan Parekh** (Executives):
Yes, Amit, you mentioned Siri AI and what I alluded to in the prepared remarks. So as we continue to roll out Siri AI to more customers, the associated cloud costs will be recognized through services cost of sales. And consistent with how we've always accounted for Maps, Siri and iCloud for the devices we sell that include these bundled services, we defer a portion of the revenue and recognize it over the life of the device. So our hardware deferrals as of the December quarter will reflect the addition of Siri AI. Both of these items will have an impact to the gross margin. 
But as always, we look to continue to make the investments necessary to support the business, and we also see a wide range of ways that AI can contribute to revenue growth over time. So on the product side, we feel AI offers a compelling reason for customers to upgrade and switch in order to get the latest capabilities, and we also feel there are opportunities across third-party apps and partnerships as well as first-party opportunities, as John highlighted earlier, with the expanded access to server-side features of Siri AI and Apple Intelligence features as well.

**Operator** (Operator):
Our next question is from Ben Reitzes from Melius Research.

**Benjamin Reitzes** (Analysts):
John, my first question, I wanted to ask you about your cash-neutral policy. On one of the previous calls, you guys said that you weren't going to focus on that anymore and that, that was not -- no longer the policy. What do you -- how -- under your leadership, what do you mean by that? Do you mean like you may go to net debt to buy back stock or do some M&A or go the opposite way and hoard some cash again? Your thoughts on that would be welcome.

**Kevan Parekh** (Executives):
Ben, it's Kevan. Let me take that one. As you know, we did talk about the fact that we were no longer using net cash neutral as a target. I think as we explained on the last call, the last time we talked about that was the fact that we think it makes sense to evaluate our cash and debt position independently and making sure we can optimize that and giving us the right flexibility. We remain committed to our capital allocation philosophy, which is we're going to invest everything we need to put -- invest in our business and return excess cash to shareholders. And so we continue to maintain that discipline, and we do think this removal of net cash neutral gives us flexibility to optimize so we can make the right investments for the company.

**Benjamin Reitzes** (Analysts):
All right. And then I wanted to ask about services. I realize you only guide one quarter at a time, but from the 8% to 9%, when you think long term, I was wondering if you're willing to say you think whether it can accelerate from there and whether AI could help you launch new services we haven't thought of yet that are accretive to the growth rate there.

**Kevan Parekh** (Executives):
Yes. I think, Ben, on that one, I think you heard John talk about a lot of the long-term attributes that we really feel give us optimism about the long-term opportunity in our services business. Again, I think we talked about things like the installed base of over 2.5 billion active devices. We obviously saw a record number of weekly visitors in the App Store in the September quarter. We also continue to see growth in users who are paying for at least a service, reaching an all-time high in both transacting and paid accounts. We're excited about emerging markets. We talked about the launch of Apple Pay in India, but we continue to see good momentum in emerging markets in our services business, where we had double-digit growth. 
And so we continue to feel really bullish about all the different elements as we look ahead over the longer arc of time. And I think, as John mentioned, we are continuing to improve the features and reach of existing and new services as well. The example was the expansion of iCloud plans to include Apple TV and Arcade, obviously reaching a lot of new potential subscribers. AppleCare One Family is another example of that. And so we continue to look for opportunities to grow our services business.

**Operator** (Operator):
Our next question is from Wamsi Mohan from Bank of America.

**Wamsi Mohan** (Analysts):
John, great to have you on the call as CEO. I appreciate the comments on memory. Clearly, you're now competing for memory more so versus historically from pretty well-capitalized companies who are signing long-term agreements. So my question is, is Apple changing anything in the way that you are procuring memory? How do you think about the progression of memory over time? And if it continues to be a headwind, is pricing also going to remain dynamic and potentially move higher? And I have a follow-up.

**Sabih Khan** (Executives):
Wamsi, this is Sabih. Let me take that one. So as you know, we have worked with many of our suppliers for decades, and we deeply value their partnership over the years. We know our products would simply not be possible without them, and we look forward to continuing to work together. We're always working hard to improve supply. And as John said earlier, we -- our manufacturing purchase obligations have increased by $33 billion from the June to the September quarter.

**Kevan Parekh** (Executives):
And Wamsi, maybe I'll add here because you asked the question about pricing and how we're managing it. So look, we're trying to manage this with a number of actions. You heard us talk about the fact we're continuing to pursue lower costs and non-memory components. John mentioned the fact that we have some benefit of carry-in inventory. And we did reluctantly make the decision to change pricing on a number of our products, starting with the iPad and Mac in the June time frame, and then iPhone more recently in September. I think what we try to do is evaluate, and doing all that, we evaluate the unit revenue and margin, and we're really being thoughtful and deliberate at evaluating kind of the short-term and long-term considerations, and we really believe we're balancing this well.

**Wamsi Mohan** (Analysts):
Okay. And I guess my follow-up is on Siri AI. In the early days of launching this, can you give us some sense of how the token consumption associated with Siri AI is being done on-device versus Private Cloud Compute versus GCP? And have you started to see any acceleration of usage? And if it does accelerate really fast globally, would it change your outlook on what you need to spend for compute?

**Kevan Parekh** (Executives):
Wamsi, I can take that one as well. So we do envision Siri AI to kind of have queries that kind of are managed on-device and also in the Private Cloud Compute environment that we've outlined. The mix of that is still very early days, and so it's hard to predict exactly what the mix of those costs are going to look like. Obviously, on-device is very, very efficient, no real cost associated with that. But on the server side, we would have some inference costs, and that's really the connection of the Siri AI-related costs that I mentioned that would be recognized with services cost of sales. But I think, again, we've just recently launched it and made it available to more users. And so in very, very early stages of understanding the kind of mix of those costs, as well as any further requirements we might have on the compute side.

**Operator** (Operator):
Our next question is from Samik Chatterjee from JPMorgan.

**Samik Chatterjee** (Analysts):
John, Sabih, good to get a chance to talk to you guys, and Kevan, same there. Maybe on the Duo, can I just ask in terms of maybe your thoughts in terms of -- or learnings from the launch of the Duo and the demand that you've seen on that front? And what are the sort of supply chain-related issues that you're facing right now that you probably need to iron out if you're trying to meet demand on that front? Any more visibility there? And when you reach supply-demand balance on the Duo as well will be helpful. And I have a quick follow-up.

**Sabih Khan** (Executives):
Samik, this is Sabih. Let me start with that question. So we're thrilled with the initial response on the iPhone Duo. iPhone Duo is constrained as of today. The ramp is going well, and we're working hard to get this revolutionary new product into the hands of our customers as quickly as possible. But at this time, it's really hard to predict when supply and demand will be in balance.

**Samik Chatterjee** (Analysts):
Okay. Perfect. Got it. And then maybe, Kevan, for you, just in terms of -- you have mentioned supply chain constraints impacting September quarter and going into December, but any way to sort of help us think about whether those are getting overall for the company, are those increasing in terms of magnitude relative to sort of the impact on revenue? And if you are willing to sort of quantify those impacts for September and December?

**Sabih Khan** (Executives):
Yes. Let me start with that. This is Sabih. So during the September quarter, we experienced supply constraints on iPhone, Mac and iPad, and this was driven by the high levels of demand. And as we have said before, we're seeing less flexibility in the supply chain than normal. The Q4 constraints were primarily driven by the availability of the advanced nodes our SoCs are produced on. But as we have transitioned more of our lineup to the latest 2-nanometer technology nodes, our constraints on advanced nodes are easing. And for the December quarter, we expect constraints on Mac and iPad, primarily driven by memory as demand has been higher than what we expected.

**Operator** (Operator):
Our next question is from Krish Sankar from TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
First one is for either Kevan or Sabih. I understand the memory price inflation. Kevan, it seems like it's probably like 1 to 1.5 or 2 percentage points. A, is that true? And Sabih, I'm just wondering, I understand that -- is there an availability issue with memory? Are you signing LTAs with memory suppliers so that availability is not an issue, even though pricing could still be an issue down the road? And then I had a quick follow-up.

**Sabih Khan** (Executives):
Yes. Thanks, Krish. So as we said earlier, we are continuing to work to improve supply, and you'll see that our manufacturing purchase obligations have increased by $33 billion from the June to the September quarter.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got it. Got it. And any comments on the margin impact to think about going forward, Kevan, or?

**Kevan Parekh** (Executives):
Well, I think, Krish, let me maybe take that one. I know you'd asked about it. So when we look at the margin change from the June quarter to the September quarter, and you remove the impact of the tariffs from both the June quarter and September quarter, we saw about a 1-point sequential change in margin, and that was driven entirely by memory impacts. Now we did have some offsets because the gross memory impact was larger than that, but we had some offsets, as John talked about earlier, driven by the benefit of carry-in inventory, some offsets from non-memory costs, as well as some of the benefits of pricing. And so as we talked about, we expect the memory costs to continue to be a challenge for us as we look in the December quarter, and our guide contemplates that right now. If you look at the midpoint, most of the sequential decline we're expecting for the December quarter, we expect to be driven by higher memory costs.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got you. And just a quick follow-up for John. And John, congrats on the first call. It seems like consumer AI agent space is seeing increasing competition with several app-based options. I'm just wondering, when you look at the agentic capability of Siri built into the OS platform versus AI agents that are confined within an app architecture, how do you see that evolving?

**John Ternus** (Executives):
Yes. Thanks, Krish. I think as I said before, Siri right now is primarily request-based. And as we talked about before, it is built on a modern orchestrator-driven architecture. So we see opportunity to expand its capabilities over time. We think fundamentally, what's most important to us is that we're giving people these capabilities that are private and secure, and we're really focused on protecting people's data.

**Operator** (Operator):
Our next question is from David Vogt from UBS.

**David Vogt** (Analysts):
Congrats, John. And maybe one to start with Kevan. If I kind of unpack the comments around supply chain about availability of components and your outlook for the December quarter, can you help us understand sort of the difference or maybe the delta of quantity versus price across sort of the product lineup? Because it certainly looks like you're looking at double-digit growth across the iPhone and the Mac business. And we all know, I think, in the industry that there's been pretty strong price inflation across the PC Mac ecosystem, and you guys mentioned that you've reluctantly taken price as well. So can you help us understand kind of what's the driving dynamics in that market? And then I have a follow-up.

**Kevan Parekh** (Executives):
Yes, David, thanks for the question. This is Kevan. We don't normally provide that level of detail or color as we look at the outlook, other than to say, again, we did guide to the 7% to 10% year-on-year. And again, just as a reminder, that is on top of a phenomenal December quarter last year, where revenue grew 16% -- and so we don't provide the level of detail, but I would say it's early to really read price elasticity at this point in time. The iPad and Mac were constrained since kind of we made those adjustments. And again, we just recently just adjusted the price on iPhone, so it's really early to really assess any elasticity impact at this stage.

**David Vogt** (Analysts):
Great. And then maybe just as a follow-up, going back to the investment cycle, whether it's agentic, Siri-related, it looks like you guys had -- you're coming off of a year of very aggressive investments in R&D to fund the business going forward and to grow the business. If I just think about kind of the commentary on Q1 of fiscal '27, certainly sounds like that spending is moderating a little bit. Can you maybe walk through some of the puts and takes in terms of what's driving that moderation in spend across the operating line items?

**Kevan Parekh** (Executives):
Yes, David, again, here, we don't break out detail on our outlook, but I would reiterate the fact that for the December quarter, we do expect OpEx to grow between 11% and 13% year-over-year, which is driven by increased and continued investment in R&D, in particular, AI. This growth rate is coming down, as you alluded, from the levels of growth we had in FY '26. But as we've said before, we continue to significantly increase our overall investments in AI while continuing to invest in the product road map, and our December guide is a continued reflection of that.

**John Ternus** (Executives):
Yes. And I'll just add that we feel confident that we're spending what we need to spend to achieve our road map.

**Operator** (Operator):
Our next question is from Richard Kramer from Arete Research.

**Richard Kramer** (Analysts):
John, your latest MacBook Pros included more iOS features like touch and Dynamic Island, as well as obviously Siri AI. Should we anticipate further close linking of macOS and iOS features, maybe even pointing at some point to a single unified OS, either for simplicity or to reduce costs? And I have a follow-up.

**John Ternus** (Executives):
Yes, thanks for the question, Richard. Look, we are very proud of both the Mac and the iPad. And I think what you've seen over the years is, we've really enjoyed the ability to bring features and capabilities across the ecosystem and create really compelling features that span things between -- handoff between iPhone and Mac and iPad. And so when we design the products, we're looking at how can we make the best version of each and every product. And if you look at what we just did last week with the MacBook Pro, we took a huge leap forward. These MacBook Pros are better in every way than the ones that came before them, and we're really proud of that. And so we don't have any fundamentally different changes that we're planning right now nor would we talk about it anyway.

**Richard Kramer** (Analysts):
Okay. And then we saw 2 years of declines in China sales, and then this year, Apple obviously grew a very healthy 28% in FY '26. Can you talk through to what you attribute that recovery and whether you think Greater China can sustain these sort of elevated levels of growth, which are really leading the company regionally now?

**John Ternus** (Executives):
Yes. Let me give you some color on China. We were very pleased with the performance in Greater China, right? Revenue was up 21% during the September quarter, which was a quarterly record. The performance was primarily driven by iPhone, where we set a September quarter record, and by Mac, where we saw very strong double-digit growth. And taking a step back, Greater China was up 28% for the full year. Tim and Sabih were just in China meeting with customers and developers and partners, and it has been wonderful to see the customer reaction to our latest lineup of products, including iPhone Duo. Our installed base of active devices has reached an all-time high, and we had a record year for iPhone upgraders in Mainland China. 
According to a survey from Worldpanel, iPhone models were the top 3 selling smartphones in urban China, and we think we gained share on iPhone and Mac. A couple other really compelling things. On Mac, we had a record year for both upgraders and customers new to the product. And according to Counterpoint, MacBook Air and MacBook Neo were the top 2 selling laptop models, and Mac mini was the top-selling desktop model in the September quarter. So I guess to answer your question, we think the success comes from having really great products.

**Operator** (Operator):
We will now go to Ben Bollin of Cleveland Research.

**Benjamin Bollin** (Analysts):
John, I'm interested in your thoughts with higher device prices, how you think about the environment around affordability programs and the importance to volumes with respect to trade-ins, subsidies, and other options, and what Apple can do to encourage more of that independently of funding it yourselves?

**John Ternus** (Executives):
Yes. Look, when we're building products and then when we're pricing them, we're always focused on building the best products and services in the world and delivering incredible value to our customers. Obviously, as we have talked about, these memory prices are unprecedented, and so that has put pressure on our prices. But it's been great to see the success of the products, and we have been investing in programs like Apple, the Apple Upgrade Program, which is a great way to help affordability. And so these affordability programs are definitely an important factor.

**Benjamin Bollin** (Analysts):
And the last one for me would be, when you look at, I guess, the level of supply-demand balance, could you speak to where you see that at? Not necessarily where it is, where you'd like it to be and how you're thinking about the opportunity to get there across the portfolio?

**Sabih Khan** (Executives):
Yes. Let me take that one, Ben. This is Sabih. So for the December quarter, we expect constraints on Mac and iPad, and it's primarily driven by memory, and that's because the demand has been higher than what we expected. And beyond December quarter, we're not providing an outlook.

**Suhasini Chandramouli** (Executives):
All right. Thank you, Ben. A replay of today's call will be available on Apple Podcasts and at apple.com/investor. Thanks again for joining us today, everyone.

**Operator** (Operator):
Once again, this does conclude today's conference. We do appreciate your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AAPL_Q3_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO｜guidance：CFO 給九月季總營收年增 9%–11%。（原話："company revenue to grow between 9% and 11% year-over-year."）
- 2026-07-30｜CFO｜guidance：CFO 給九月季 iPhone 年增中十位數。（原話："reported growth rate for iPhone to be mid-teens year-over-year."）
- 2026-07-30｜CFO｜guidance：CFO 說九月季 Services 成長率與六月季大致相近（已扣除約 2.5 個百分點匯率逆風的口徑）。（原話："reported growth rate to be largely similar to what we"）
- 2026-07-30｜CFO｜guidance：CFO 給九月季毛利率 47%–48%。（原話："We expect gross margin to be between 47% and 48%."）
- 2026-07-30｜CFO｜margin：九月季毛利率指引含約 1 個百分點關稅退款效益。（原話："approximately 1 percentage point related to tariff refunds."）
- 2026-07-30｜CFO｜guidance：九月季營業費用指引區間。（原話："$19.1 billion and $19.4 billion."）
- 2026-07-30｜CFO｜guidance：CFO 表示九月季以後不提供財測或色彩。（原話："providing any kind of color or guidance beyond the September quarter."）
- 2026-07-30｜CFO｜risk：財測前提：關稅政策維持現況、總經不惡化。（原話："global tariff rates, policies, and their application remain in effect"）
- 2026-07-30｜CFO｜risk：CFO 預期九月季總營收受匯率逆風影響（口徑：對年增率的連續季拖累）。（原話："sequential headwind of about 2.5 percentage points"）
- 2026-07-30｜CFO｜risk：CFO 預期九月季供給限制明顯加重。（原話："impact from supply constraints to increase significantly sequentially."）
- 2026-07-30｜CEO｜risk：CEO 說供給限制主因是 SoC 先進製程節點的可得性。（原話："primarily driven by the availability of the advanced"）
- 2026-07-30｜CEO｜risk：CEO 定性供給問題的根因，並說本季供給端要趕工。（原話："the root cause of it is not a regular supply issue."）
- 2026-07-30｜CEO｜risk：CEO 描述下一季供給端的處境。（原話："we're going to be scrambling on the supply side essentially."）
- 2026-07-30｜CFO｜margin：六月季公司毛利率 50.1%，含關稅退款約 2 個百分點；扣除後落在上季指引中點。（原話："favorable impact of approximately 2 percentage points."）
- 2026-07-30｜CFO｜margin：產品毛利率 40.1%（含關稅退款逾 2.5 個百分點）。（原話："Products gross margin was 40.1%, up 140 basis points sequentially."）
- 2026-07-30｜CFO｜margin：CFO 拆解毛利率連續季下滑：記憶體成本占主要，匯率影響小。（原話："I think that FX was a pretty minimal impact"）
- 2026-07-30｜CEO｜margin：CEO 說九月季記憶體採購成本再升。（原話："For September, we expect to pay even higher memory costs"）
- 2026-07-30｜CEO｜margin：CEO 說九月以後記憶體市價續漲，對公司影響可能加大。（原話："continuing to increase, which could drive an increasing impact on our business"）
- 2026-07-30｜CEO｜margin：CEO 說明 iPad／Mac 調價的原因。（原話："a 100-year flood on the memory pricing"）
- 2026-07-30｜CEO｜margin：CEO 說定價不採單一公式，看長期而非 90 天。（原話："think about it over the long term instead of a 90-day clock."）
- 2026-07-30｜CEO｜risk：CEO 提到 DRAM 只有三家供應商，正評估所有選項。（原話："primarily the DRAM market has 3 suppliers"）
- 2026-07-30｜CFO｜capital_allocation：六月季回購與股利金額。（原話："$4 billion in dividends and equivalents and $25.8 billion"）
- 2026-07-30｜CFO｜capital_allocation：期末現金與有價證券。（原話："$147 billion in cash and marketable securities"）
- 2026-07-30｜CFO｜capital_allocation：董事會宣布每股 $0.27 股利。（原話："cash dividend of $0.27 per share of common stock"）
- 2026-07-30｜CEO｜commitment：CEO 重申對美國 6,000 億美元投資承諾。（原話："we made a $600 billion commitment to the U.S. over 4"）
- 2026-07-30｜CEO｜commitment：CEO 說將把收到的關稅退款再投入美國。（原話："reinvest the tariff refunds we've received into the U.S."）
- 2026-07-30｜CEO｜commitment：Broadcom 多年協議，預期金額超過 300 億美元。（原話："American Manufacturing program is expected to exceed $30"）
- 2026-07-30｜CEO｜commitment：CEO 稱此為最大的美國製造承諾。（原話："our largest ever American manufacturing program commitment"）
- 2026-07-30｜CEO｜commitment：休士頓廠今年稍晚開始生產 Mac mini。（原話："make Mac mini there, too."）
- 2026-07-30｜CEO｜commitment：CEO 宣布這是最後一次法說，由 John Ternus 接手主持。（原話："this will be my final earnings call, and John will lead these calls going forward."）
- 2026-07-30｜CEO｜commitment：CEO 說 Arizona 晶圓廠今年供應的元件數量。（原話："we do source over 100 million components this"）
- 2026-07-30｜CEO｜product：CEO 對 Siri AI 公測回饋的描述。（原話："we are off the charts excited about Siri AI."）
- 2026-07-30｜CEO｜product：Siri AI 運算成本回收方式：iCloud+ 升級方案，但尚無完整計畫。（原話："we will have some kind of upgrade possibilities on iCloud+"）
- 2026-07-30｜CEO｜product：CEO 說 Siri AI 在歐盟尚無法同步推出，仍與歐盟執委會協商。（原話："we're working closely with them to try to get to something"）
- 2026-07-30｜CEO｜product：中國方面僅取得原始 Apple Intelligence 功能的出貨核准，Siri AI 後續仍需工作。（原話："approval to ship sort of the original features of Apple"）
- 2026-07-30｜CEO｜product：CEO 提到 MacBook Neo 需求強、仍在努力補足供給。（原話："we're continuing to work hard to meet demand"）
- 2026-07-30｜CEO｜competition：CEO 談端側 AI 的策略地位。（原話："strategic and sort of a competitive weapon, if you will."）
- 2026-07-30｜John Ternus｜competition：Ternus 被問競爭格局（OpenAI 裝置、SpaceX AI 手機）時的回答。（原話："we're just really focused on our plans and very excited about it."）
- 2026-07-30｜CFO｜customer：CFO 說近一季美國教育機構 MacBook Neo 大單約半數取代 Windows／Chromebook。（原話："about half of the MacBook Neo large purchases"）
- 2026-07-30｜CFO｜customer：付費訂閱數里程碑。（原話："1.5 billion in paid subscriptions."）
- 2026-07-30｜CEO｜customer：CEO 對 iPhone 是否有拉貨的回答：資料上看不出來。（原話："it's not obvious in the data that what you're asking is true."）
- 2026-07-30｜CEO｜customer：CEO 說 iPad／Mac 漲價後的價格彈性尚無定論。（原話："it's just too early to come to a definitive"）
- 2026-07-30｜CFO｜risk：CFO 說 App Store 受手遊疲弱影響，六月季略遜預期。（原話："more softness on mobile gaming in the App Store."）
- 2026-07-30｜CFO｜risk：CFO 提到美國仍受法院對外部連結交易的裁決約束。（原話："we do continue to operate under a court ruling"）
- 2026-07-30｜CFO｜risk：CFO 說最高法院將審理其上訴。（原話："we're pleased that the Supreme Court will hear our appeal."）
- 2026-07-30｜CFO｜guidance：CFO 拆解 Services 匯率逆風：自三月季到九月季約 5 個百分點。（原話："foreign exchange to drive about a 5 percentage point headwind"）
- 2026-07-30｜CFO｜capital_allocation：營業費用年增 23%，主因研發投資。（原話："up 23% year-over-year, driven by investments in R&D"）
- 2026-07-30｜CEO｜capital_allocation：CEO 回答 Siri AI 對資本密集度的影響：成本與 iCloud 升級的平衡尚不確定。（原話："what the balance of that is a bit uncertain at the moment."）

### 問答異常語氣（迴避／改口／保留）
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Reitzes 追問 12 月季供給限制影響與可否給指引｜答法：CFO 明說九月季以後不提供任何色彩或指引，未回應 12 月季的數字
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Wamsi Mohan 問 Ternus 競爭格局是否改變（OpenAI 裝置、SpaceX AI 手機）｜答法：Ternus 未談競爭對手，只說機會很多、專注自己的計畫
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Wamsi Mohan 問 Siri AI 是否改變資本密集度｜答法：CEO 答混合模式、成本與 iCloud 升級的平衡尚不確定，未給數字
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Michael Ng 問 Siri AI 運算成本與 iCloud+ 回收｜答法：CEO 稱還早、沒有完整計畫，只說會有 iCloud+ 升級選項
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Reitzes 問是否可能拓寬矽晶圓供應商（含 Arizona 新晶圓廠）｜答法：CEO 改談需求超預期並稱非供應商問題，未回答是否擴大供應商

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
{"date":"20260731","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"iPhone 17/18 的 AI 換機週期是結構性升級，不是一次性拉貨"},{"id":"H2","text":"記憶體成本可經由漲價與 mix 轉嫁，公司毛利率在 FY27 守住底線"},{"id":"H3","text":"Services 能在監管切割下維持雙位數成長與約 75% 毛利，市場續給 ≥ 28x 前瞻倍數"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"記憶體成本通膨延續至 FY27，漲價觸及價格彈性 → 量價雙輸。Cook 稱這是「記憶體定價的百年一遇洪水」，且明說九月之後市場價格續漲、對業務的影響「增加中」；抵銷手段（結轉庫存利益、非記憶體零件降價）管理層自己說會遞減。"},{"id":"R2","text":"Services 監管切割：美國 link-out 裁定執行中（最高法院已受理上訴）、EU DMA 使 Siri AI 無法在歐盟的 iPhone/iPad 首發、若干國家 App Store 商業模式已變更、Google 預設搜尋協議因 Mehta 救濟裁定被迫非排他化。"},{"id":"R3","text":"AI 平台層位移：Apple 不擁有前沿模型（法說對模型來源與夥伴全程未揭露，僅稱端側＋私有雲＋「部分第三方雲」的混合架構），且旗艦 AI 功能在歐盟 iPhone/iPad 缺席、中國僅核准原版功能。若 agent 形態繞過 App／Safari 入口，或新形態 AI 裝置成為新入口，分發層租金基礎鬆動。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE（FY27 共識）≤ 27x（約 $261）且剔關稅毛利率連 2 季 ≥ 46%——雙條件 AND，缺一不進場","irr_base_pct":4.2,"ev5y_pct":19.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.8,"ev5y_pct":19.0,"irr_base_pct":4.2,"max_dd_pct":-45.0,"bull_5y_price":512.0,"bear_5y_price":210.0,"p_bull_pct":25.0,"p_bear_pct":28.0,"rearm_trigger":"Fwd PE（FY27 共識）≤ 27x（約 $261）且剔關稅毛利率連 2 季 ≥ 46%——雙條件 AND，缺一不進場","price_at_dd":309.21,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
