你是 stock-analyst **v20 判斷 agent**，標的 MTSI（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MTSI","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":424.8,"period":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"MACOM Q4 FY26 earnings release, 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001493594/000149359426000041/ex99_1earningsreleaseq4fy26.htm"},"note":"未查得"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":38.2,"period":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"% (營業利益 162.3 USD M)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"同上 8-K Ex.99.1 adjusted operating income 調節表"},"note":"未查得"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":31.6,"period":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"% (營業利益 134.2 USD M)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"同上 8-K Ex.99.1"},"note":"未查得"},{"id":"f_kpi3_stock_based_compensation","label":"Stock-based compensation（調節表列示）","value":23.9,"period":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"USD M（占營收約 5.6%；占 non-GAAP 營業利益約 14.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"同上 8-K Ex.99.1 營業利益調節表；占比為本 agent 以 23.9/424.8、23.9/162.3 計算"},"note":"n/a"},{"id":"f_kpi4_adjusted_eps_q4_non_gaap","label":"Adjusted EPS (Q4, non-GAAP)","value":2.09,"period":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","unit":"USD/股","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）","citation":"同上 8-K Ex.99.1（GAAP EPS 1.78；adjusted gross margin 61.3%、GAAP 59.9%）"},"note":"未查得"},{"id":"f_kpi5_guidance_q1_fy2027_reven","label":"Guidance: Q1 FY2027 revenue","value":"450–460","period":"Q4 FY2026 財報（公告於 2026-11-05）","unit":"USD M（季末 2027-01-01）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026 財報（公告於 2026-11-05）","citation":"同上 8-K Ex.99.1 outlook"},"note":"未查得"},{"id":"f_kpi6_guidance_q1_fy2027_adjus","label":"Guidance: Q1 FY2027 adjusted gross margin / adjusted EPS","value":"62.0–63.0% / 2.21–2.29","period":"Q4 FY2026 財報（公告於 2026-11-05）","unit":"% / USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 FY2026 財報（公告於 2026-11-05）","citation":"同上 8-K Ex.99.1（假設 non-GAAP 稅率 6%、稀釋股數 79.0M）"},"note":"未查得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mtsi_gross_margin_pct","label":"MTSI 毛利率","value":57.13,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mtsi_operating_margin_pct","label":"MTSI 營業利益率","value":18.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mtsi_fcf_margin_pct","label":"MTSI FCF 利潤率","value":9.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_swks_gross_margin_pct","label":"SWKS 毛利率","value":40.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SWKS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_swks_operating_margin_pct","label":"SWKS 營業利益率","value":8.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SWKS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_swks_fcf_margin_pct","label":"SWKS FCF 利潤率","value":9.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SWKS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_qrvo_gross_margin_pct","label":"QRVO 毛利率","value":48.22,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QRVO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qrvo_operating_margin_pct","label":"QRVO 營業利益率","value":15.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QRVO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qrvo_fcf_margin_pct","label":"QRVO FCF 利潤率","value":17.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QRVO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_adi_gross_margin_pct","label":"ADI 毛利率","value":65.8,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_adi_operating_margin_pct","label":"ADI 營業利益率","value":35.72,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_adi_fcf_margin_pct","label":"ADI FCF 利潤率","value":35.57,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cohr_gross_margin_pct","label":"COHR 毛利率","value":38.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_operating_margin_pct","label":"COHR 營業利益率","value":14.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_fcf_margin_pct","label":"COHR FCF 利潤率","value":-23.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":210.98,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-41.37,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":38.03,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":54.99,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.51 → 8.54）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":18.38,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.54 → 10.11）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":23.44,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.11 → 12.48）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":8.54,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":10.11,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":12.48,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":54.99,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 5.51 → 8.54（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":48.95,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"2 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":12.14,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":11.85,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":24.7,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 8.54，分子＝快照價 210.98","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-385.47,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 406.94、現金 792.41（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":76.37,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":15727.27,"period":"2026-11-08","unit":"USD m","basis":"市值 16112.74 ＋ 淨負債 -385.47","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":1939.58,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":2283.65,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":8.11,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 210.98 / W52 262.51 / W104 194.8 / W250 125.25 / W250 13週斜率 2.14%"},{"id":"f_ma_w52","label":"52 週均線","value":262.51,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":194.8,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":125.25,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.14,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出主要競爭者（ADI、Broadcom、Credo、Marvell、MaxLinear、Microchip、NXP、Qorvo、Semtech、Skyworks、Sumitomo），並提到中國公司競爭加劇；亦點出客戶自研與低成本矽製程大廠為潛在替代","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"our significant competitors include, among others, ADI, Broadcom, Credo, Marvell, MaxLinear, Microchip, NXP, Qorvo, Semtech, Skyworks and Sumitomo as well as increased competition from Chinese companies.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 稱主要與客戶內部設計資源及其他高性能類比半導體供應商競爭，預期有新進入者，且未來有採低成本矽製程之大量製造商的替代技術競爭","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"We expect competition in our markets to change as new competitors enter these markets, existing competitors merge or form alliances and new technologies emerge. We believe that in the future there will be increased competition from companies utilizing alternative technologies, including high-volume manufacturers using low-cost silicon process technology.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"管理層稱 1.6T 為資料中心成長主要驅動，設計案進入量產；資料中心 FY26 成長基準由 35-40% 上調至 60% 以上","source":"MarketBeat / earnings call 摘要 (MACOM Q1 FY2026)","url":"https://www.marketbeat.com/instant-alerts/macom-technology-solutions-q1-earnings-call-highlights-2026-02-05/?.tsrc=rss","excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"NXP 退出 5G RF 功率 GaN 為 MACOM 帶來份額機會，CEO 稱效益需一至兩年顯現","source":"Barchart MACOM Q1 earnings call analyst questions","url":"https://www.barchart.com/story/news/1925026/5-must-read-analyst-questions-from-macoms-q1-earnings-call","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2025 10-K：無單一直接客戶占營收 10% 以上，前十大直接與經銷客戶合計 56.7%；採購為 PO 制無最低採購量，主要客戶可能無預警終止、減少訂單、轉向競爭對手或自行開發產品（in-house）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"In the fiscal year ended October 3, 2025, no direct customers individually accounted for 10% or more of our revenue and sales to our top 10 direct and distribution customers accounted for an aggregate of 56.7% of our revenue.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因子列出客戶可能轉向競爭對手或自行開發產品，屬一般性風險揭露；兩次搜尋未找到 2026 年具體客戶導入第二供應商或 in-house 的報導或協議。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"it is possible that any of our major customers could terminate their purchasing arrangements with us with little or no warning and without penalty, or significantly reduce or delay the amount of our products that they order, purchase products from our competitors or develop their own products internally.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 無單一直接客戶達10%；兩家經銷商分別占12.4%、11.2%；前25大直接客戶占45.6%（FY24 47.0%、FY23 51.5%）","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"One of our resellers accounted for 12.4% and 11.3% of our revenue in fiscal years 2025 and 2024, respectively, but did not exceed 10% in fiscal year 2023. A second reseller accounted for 11.2% of our revenue in fiscal year 2025 but did not exceed 10% in fiscal years 2024 and 2023.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"前十大客戶占營收 FY2025 57%、FY2024 56%、FY2023 48%，集中度上升；Customer A 12%、B 11%，應收帳款三家各11%","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"In fiscal years 2025, 2024 and 2023, our top ten customers represented an aggregate of 57%, 56% and 48% of total revenue, respectively.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"採購以訂單為基礎、無最低採購量，主要客戶可無預警終止；中國占營收28.4%","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"The purchasing arrangements with our customers are typically conducted on a purchase order basis that does not require our customers to purchase any minimum amount of our products over a period of time.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"InP 雷射供給緊到 2027：Lumentum 執行長稱出貨低於客戶需求約 30%，EML 產能已被訂到 2027；緩解多在 2028 之後（次級來源）。","source":"LEDinside, InP Shortage Emerges as AI Optical Interconnect Bottleneck","url":"https://www.ledinside.com/news/2026/08/2026_08_06_01","excerpt":"undershipping customer demand by somewhere around 30%","as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"LightCounting：需求超過供給 30%，短缺預計 2026 年底消退，2027-2031 市場成長趨緩，與雲端 capex 週期高度相關。","source":"LightCounting LightTrends Newsletter April 2026","url":"https://lightcounting.com/newsletter/en/april-2026-market-forecast-379","excerpt":"If TSMC could ship more GPU than expected, the shortages for optical transceivers will stretch into 2027 and the market growth will exceed our forecast. Data on year-over-year growth in quarterly capex of cloud companies and sales of Ethernet transceivers for 2012-2025, presented in the report, shows that the cycles in","as_of":"2026-04-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MTSI 上調 FY26 資料中心成長基準至 >60%，1.6T 部署 2026 年強勁，book-to-bill 1.5:1。","source":"MarketBeat MACOM Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/macom-technology-solutions-q2-earnings-call-highlights-2026-05-08/?.tsrc=rss","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TrendForce：AI 光收發器市場 2026 年約 260 億美元，供應鏈結構性重組，Nvidia 鎖定 EML 產能使交期超過 2027。","source":"TrendForce press center","url":"https://www.trendforce.com/presscenter/news/20260420-13017.html","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：截至申報日無預期會造成重大不利影響的未決法律程序，未見反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"We were not involved in any pending legal proceedings as of the filing date of this Annual Report that we believe would have a material adverse effect on our business, operating results, financial condition or cash flows.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2025 對中國銷售占 28.4%、亞太 11.5%；10-K 提示美國 BIS 出口管制（2022、2023 年新增）為風險。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"fiscal year 2025 sales to customers in China and the Asia Pacific region accounted for 28.4% and 11.5% of total fiscal year 2025 sales, respectively.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 中國占營收 28.4%、亞太 11.5%，美國以外銷售占 56.3%；10-K 列示關稅、出口許可與貿易限制為風險，並稱多數產品受 EAR 管制，部分需 BIS 出口許可。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"Sales to customers located outside the U.S. accounted for 56.3% of our revenue for the fiscal year ended October 3, 2025. Sales to customers located in China and the Asia Pacific region typically account for a large portion of our overall sales to customers located outside the U.S. For example, fiscal year 2025 sales to customers in China and the Asia Pacific region accounted for 28.4% and 11.5% of total fiscal year 2025 sales, respectively.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 指出部分產品需出口許可、出口管制改革已造成部分國家與客戶出貨困難，並承認持續面臨合規挑戰。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"Ongoing export control reform that has changed and is expected to continue to change rules applicable to us in the future in ways we do not yet fully understand and we have experienced and will continue to experience challenges in complying with the new rules as they become effective, resulting in difficulties or an inability to ship products to certain countries and customers.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"MACOM 10-K 披露：特定製程晶圓通常僅經單一代工廠取得，並倚賴該廠供應該製程全部晶圓；另述可能對各類材料使用單一供應來源。","source":"MACOM 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"wafers procured from merchant foundries for a particular process technology are generally sourced through a single foundry on which we rely for all of our wafers in that process.","as_of":"2025-10-03","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"MACOM 10-K 披露：供應商若原料庫存不足、倒閉、產能受限或暫時停工，公司面臨供應鏈中斷風險；緩解方式為多源認證、改設計、增加庫存。","source":"MACOM 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"Our reliance on external suppliers puts us at risk of supply chain disruption if a supplier does not have sufficient raw material inventory to meet our manufacturing needs, goes out of business, experiences capacity constraints or temporary facility closures.","as_of":"2025-10-03","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q FY2026：砷化鎵等關鍵材料可能因地緣政治與出口管制而短缺；自有廠位於Lowell、Ann Arbor、RTP、法國Limeil-Brévannes","source":"MACOM 10-Q (quarter ended 2026-01-02)","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359426000019/mtsi-20260102.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 Q4 營收 $424.8M，年增 62.7%、季增 24.1%；FY2026 全年 $1,327.6M，年增 37.3%；新聞稿未分終端市場揭露營收","source":"MACOM Q4 FY26 earnings release (SEC 8-K ex99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001493594/000149359426000041/ex99_1earningsreleaseq4fy26.htm","excerpt":"Revenue was $424.8 million","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2027 Q1 營收指引 $450–460M，調整後毛利率 62.0–63.0%","source":"MACOM Q4 FY26 earnings release (SEC 8-K ex99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001493594/000149359426000041/ex99_1earningsreleaseq4fy26.htm","excerpt":"MACOM expects revenue to be in the range of $450 million to $460 million.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"管理層將 FY2026 資料中心成長預期上修（2月 35–40%、5月 60%以上），並稱 CY2027 需求仍強","source":"Barchart MTSI Q2 deep dive","url":"https://www.barchart.com/story/news/1798178/mtsi-q2-deep-dive-data-center-and-defense-demand-propel-growth-guidance-highlights-momentum","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"公司 FY2025 10-K 自述：預期未來會有採用替代技術的公司（含使用低成本矽製程的大量製造商）帶來更多競爭。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"We believe that in the future there will be increased competition from companies utilizing alternative technologies, including high-volume manufacturers using low-cost silicon process technology.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：未來競爭可能來自新替代技術、更高整合度的 IC 廠商，且客戶與供應商可能自行開發競品或取代本公司產品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"We believe future competition could also come from companies developing new alternative technologies, component suppliers based in countries with lower production costs and IC manufacturers achieving higher levels of integration that exceed the functionality offered by our products. Our customers and suppliers could also develop products that compete with or replace our products.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"搜尋摘要：有評論文章指出，若超大規模業者透過矽光子/CPO 把光學子系統內製，MACOM 的離散光電二極體、TIA、DFB 雷射市場可能縮小；該風險在財報會議未被量化，且未找到 CPO 已減少其 TIA/驅動器出貨量的硬數據。CPO 大量部署預估 2027-2028。","source":"WebSearch 摘要（聚合多來源，其中看空論述為意見文章）","url":null,"excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","triggers"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"+","claim":"搜尋摘要：MACOM 448G 驅動器採高量產矽製程，支援矽光子、EML、TFLN 多平台；公司稱新品針對 CPO/NPO 架構最佳化。","source":"ConvergeDigest／Barchart 報導 448G PAM4 驅動器（經搜尋摘要）","url":"https://convergedigest.com/macom-unveils-448g-pam4-drivers-for-1-6t-and-3-2t/","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"MACOM 維持多通路（直銷、應用工程、獨立業務代表、經銷商）；經銷商營收占比 FY2023 24.0%→FY2024 29.3%→FY2025 32.3%，兩家 reseller 各占 12.4%、11.2%。通路占比上升但屬既有通路內的比重變動，非訂閱化／D2C／平台化。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"Sales to our distributors accounted for 32.3%, 29.3% and 24.0% of our revenue in fiscal years 2025, 2024 and 2023, respectively.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ3 財報（2026-08-06）時公司 FQ4 營收指引 $415–425M，高於各家共識（MarketBeat $364.1M、Zacks $356.8M、Chartmill 約 $376M）；EPS 指引 $1.97–2.03 對共識 $1.49。","source":"MarketBeat / Chartmill 彙整（搜尋摘要）：MACOM releases Q4 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/macom-technology-solutions-nasdaqmtsi-releases-q4-2026-earnings-guidance-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"TickFlow 彙整：17 位分析師共識 Buy，平均目標價 $377.56（as-of 2026-08-01）；其他來源同期分布不一（MarketBeat 5月約 $307–317、WallStSmart 約 $389、Investing.com 約 $280 屬較舊）。","source":"TickFlow MTSI forecast","url":"https://www.tickflow.io/stock/MTSI/forecast","excerpt":"The consensus among 17 analysts covering MACOM Technology Solutions Holdings, Inc. (MTSI) is Buy with an average price target of $377.56.","as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 FQ4/FY2026 財報釋出 FQ1 FY2027 營收指引 $450–460M（季末 2027-01-01）；FY2026 營收 $1.33B、年增 37%。","source":"SEC 8-K Ex.99.1 MACOM Q4 FY26 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001493594/000149359426000041/ex99_1earningsreleaseq4fy26.htm","excerpt":"MACOM expects revenue to be in the range of $450 million to $460 million.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"經查 SEC 8-K 清單，2025-11-08 至 2026-11-08 共 7 份 8-K，含重大項目者 0 份（僅財報、董事異動、股東投票）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001493594&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K 稱公司未涉及預期會對業務、經營結果、財務狀況或現金流產生重大不利影響的未決法律程序。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"We were not involved in any pending legal proceedings as of the filing date of this Annual Report that we believe would have a material adverse effect on our business, operating results, financial condition or cash flows.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K無 1.01／2.01 等併購相關重大項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001493594&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K 稱無預期有重大不利影響的未決法律程序；風險因素僅稱未來可能成為證券集體訴訟目標。","source":"SEC EDGAR 10-K FY2025 Item 3 / 1A","url":"https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm","excerpt":"We may be the target of this type of litigation in the future.","as_of":"2025-11-14","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K 無 Item 4.02（不可信賴先前財報）等項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001493594&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MTSI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.13,"operating_margin_pct":18.97,"fcf_margin_pct":9.44,"rd_intensity_pct":23.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"SWKS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":40.75,"operating_margin_pct":8.12,"fcf_margin_pct":9.28,"rd_intensity_pct":21.4},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SWKS","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"QRVO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.22,"operating_margin_pct":15.38,"fcf_margin_pct":17.82,"rd_intensity_pct":19.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QRVO","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ADI","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.8,"operating_margin_pct":35.72,"fcf_margin_pct":35.57,"rd_intensity_pct":14.24},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"COHR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.16,"operating_margin_pct":14.11,"fcf_margin_pct":-23.28,"rd_intensity_pct":10.18},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"MTSI"},"financial_history":{"ticker":"MTSI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-09-30","revenue":675170000.0,"revenue_yoy_pct":null,"gross_margin_pct":60.16,"operating_margin_pct":19.65,"net_income":439955000.0,"diluted_eps":null,"free_cash_flow":150469000.0,"fcf_margin_pct":22.29,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-09-30","revenue":648407000.0,"revenue_yoy_pct":-3.96,"gross_margin_pct":59.5,"operating_margin_pct":16.56,"net_income":91577000.0,"diluted_eps":1.28,"free_cash_flow":142218000.0,"fcf_margin_pct":21.93,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":729578000.0,"revenue_yoy_pct":12.52,"gross_margin_pct":53.97,"operating_margin_pct":10.1,"net_income":76859000.0,"diluted_eps":1.04,"free_cash_flow":137012000.0,"fcf_margin_pct":18.78,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":967258000.0,"revenue_yoy_pct":32.58,"gross_margin_pct":54.69,"operating_margin_pct":13.4,"net_income":-54210000.0,"diluted_eps":-0.73,"free_cash_flow":153201000.0,"fcf_margin_pct":15.84,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MTSI/MTSI_Q4_2026_Earnings_Call_20261105.md）

# Q4 2026 Earnings Call
**MACOM Technology Solutions Holdings, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Welcome to MACOM's Fourth Fiscal Quarter 2026 Conference Call. This call is being recorded today, Thursday, November 5, 2026. [Operator Instructions] I will now turn the call over to Mr. Steve Ferranti, MACOM's Senior Vice President of Corporate Development and Investor Relations. Mr. Ferranti, please go ahead.

**Stephen Ferranti** (Executives):
Thank you, operator. Good morning, and welcome to our call to discuss MACOM's fourth quarter and year-end results for fiscal year 2026. I would like to remind everyone that our discussion today will contain forward-looking statements, which are subject to certain risks and uncertainties as defined in the safe harbor for forward-looking statements contained in the Private Securities Litigation Reform Act of 1995.
Actual results may differ materially from those discussed today. For a more detailed discussion of the risks and uncertainties that could result in those differences, we refer you to MACOM's filings with the SEC. Management's statements during this call will also include discussion of certain adjusted non-GAAP financial information.
A reconciliation of GAAP to adjusted non-GAAP results are provided in the company's press release and related Form 8-K, which was filed with the SEC today. With that, I'll turn over the call to Steve Daly, President and CEO of MACOM.

**Stephen Daly** (Executives):
Thank you, and good morning. I will begin today's call with a general company update. After that, Jack Kober, our Chief Financial Officer, will review our Q4 and year-end results for fiscal year 2026. When Jack is finished, I will provide revenue and earnings guidance for the first quarter of FY '27, and then we will be happy to take some questions.
Revenue for the fourth quarter of fiscal 2026 was $424.8 million, and adjusted earnings per diluted share was $2.09. Our full year FY '26 revenue was $1.3 billion, and adjusted earnings per diluted share was $5.60. On a full year basis, we achieved 37% year-over-year revenue growth and 61% year-over-year adjusted EPS growth. In Q4, our book-to-bill ratio was 1.4:1, and we ended the fiscal year with record backlog.
Orders were strong across all 3 end markets with data center outperforming. Orders booked and shipped within the quarter were 7% of total revenue, reflecting our strong backlog and extended manufacturing lead times for certain products. Q4 revenue performance by end market was as expected, with all markets growing sequentially. Data center revenue was $188.1 million, Industrial and Defense was $164.6 million and telecom was $72.1 million.
Sequentially, data center increased approximately 37%, I&D increased 23% and telecom increased 1%. Data center and I&D revenue both reached record levels again this quarter. In total, these markets contain thousands of potential customers with a combined serviceable addressable market, or SAM, that we now estimate to be in the range of $15 billion in 2027. To address the large SAM opportunity, we have invested and we will continue to invest in R&D and in expanding our engineering and manufacturing teams and capabilities.
In FY '26, our team made meaningful progress across many strategic focus areas. Three noteworthy accomplishments, which we expect will support FY '27 and FY '28 revenue growth include: first, our fab engineers recently made significant progress improving the quality of our indium phosphide lasers facet, allowing our lasers to better address CW applications. These results support MACOM's strategy to enter the multibillion-dollar CW laser market, which we are targeting for 2028.
Second, we are upgrading 2 of our existing millimeter wave GaN on silicon carbide processes to improve performance and enable advanced nodes. We believe this will make MACOM more competitive and help us better address the growing SATCOM and defense markets. And third, we are on plan expanding manufacturing capacity at 3 wafer fabs in 2 U.S.-based hybrid manufacturing sites to support our future growth.
Our fab, advanced technology and operation teams are doing an excellent job collaborating to develop new technologies for future products while also increasing production capacity for existing products. We believe these activities will enable MACOM to provide our new and compelling products at scale and meet our customers' growing demand during 2027 and 2028.
Turning to recent market trends, starting with data center. Based on our current outlook, we believe that FY '27 will be another robust year. We now believe our data center year-over-year revenue growth will exceed our FY '26 growth rate of 74%. MACOM has a strong position in the market. Notably, we believe the combination of growing 1.6T volumes with increased content opportunities provides a strong tailwind for our data center business.
In FY '27, we will continue to expand our high-speed analog portfolio to support PAM4 and coherent systems across EML, TFLN and silicon photonic-based platforms. As data center architectures evolve, we expect new optical implementations with higher I/O density, known as near-packaged optics or NPO, will be deployed. NPO architectures can vary by end customer, but what is common across all NPO customers is that they require smaller IC footprints, more lanes of data and lower power consumption compared to pluggable optical modules.
We believe NPO provides a tremendous growth opportunity for MACOM, and we are actively pursuing high-volume opportunities with multiple hyperscalers. Our indium phosphide photonics product lines also represent a large growth opportunity for MACOM. Today, we manufacture 200G photodetectors and a wide range of lasers, including 25G lasers for 100G LR4 and 100G CWDM4 applications.
As we look ahead, we expect to produce significant volumes of 200G PDs as well as 400-gig PDs and as I previously mentioned, CW lasers for 800G, 1.6T and 3.2T applications. Customer interest remains high, and we are excited to bring these products to market as quickly as possible. I'll highlight that at this year's CIOE and ECOC trade shows, we introduced a full front-end chipset solution for 3.2T optical modules, combining transmit and receive technologies optimized for PAM4 optical links.
This chipset consists of 2 400G per lane quad linear TIAs, 8 400G photodetectors with high coupling efficiency as well as 2 modulator drivers. Our 3.2T chipset solution was designed to help our customers accelerate development of their next-generation optical interconnects for AI infrastructure across thin-film lithium niobate, silicon photonics and EML-based architectures.
Turning to our I&D business. Our I&D business continues to strengthen, driven by our talented teams designing and manufacturing best-in-class IC, module and subsystem solutions. In FY '26, our I&D revenue grew 27.8% year-over-year, and we are targeting even higher growth in FY '27. We see multiple favorable trends, including the expansion of U.S. and European defense budgets, which are supporting increased development and production of radars, drone and counter UAS systems, communication systems, electronic warfare systems and hardened optical electronics for a wide range of applications.
Since 2019, we have been focused on improving the quality, performance and breadth of our products for this market. We actively engage customers, large and small, on long-term programs and work together as partners to help ensure their success. The I&D market remains a critical portion of our business, and we are pleased that our franchise and brand continue to strengthen every year as we grow.
We win because we offer customers in this market unique semiconductor processes, a broad product portfolio spanning high power, high frequency and high data rate functions and the ability to design and manufacture complex customized multifunction solutions. These solutions often combine best-in-class ICs with bumped or copper pillar flip-chip technology in LGA packages to achieve the smallest possible form factors.
Two examples include a receiver protector module that shields an RF or microwave receiver or radar from high-power jamming or interference signals and the second, a transmit receive module used in digital beamforming antenna array systems. Our primary focus in the I&D market is providing unique solutions that improve overall system performance and give our customers a competitive advantage.
Over the past 6 months, we have been awarded numerous development programs from both large defense primes and newer neo primes, which we believe will lead to meaningful long-term business. These platforms include microwave and optical EW systems, missile and drone electronics and next-generation tactical mobile radios. All these wins have one thing in common. They utilize unique MACOM semiconductor content. And finally, during Q4, we received follow-on orders to support continued long-term production of hardware we manufacture for shipborne radar systems and air-to-air missile systems.
Now moving to telecom. Telecom revenue grew approximately 11% year-over-year in FY '26, driven primarily by 5G and SATCOM. We expect similar growth in FY '27 with potential upside as we capture and execute new business during the year. The most significant growth opportunity we see within the telecom market today is the low earth orbit or LEO satellite segment. We are a supplier to a variety of these LEO networks today, and we expect our revenues in this market to grow in FY '27 and FY '28.
MACOM supports our LEO customers at various levels, including wafer foundry, standard and custom IC products and multichip module solutions. We support this market with high-power and high-frequency RF products, optical components and analog and mixed-signal ICs. We draw on our heritage in space and Hi-Rel product screening and system engineering know-how to support our customers' designs and time to market.
We were pleased to learn that one of our customers was recently awarded a new contract to support a large constellation. We anticipate this could represent approximately $20 million of new business for MACOM beginning in early 2028. I'll note that LEO satellite constellations require thousands of ground stations, which contain uplinks and downlinks that communicate with the satellites. The links often utilize microwave frequencies, for example, V-band frequencies between 40 and 52 gigahertz.
MACOM has successfully designed and is manufacturing and delivering V-band analog linearizers to be used with V-band TWTAs for these uplinks. We see this as a growing opportunity within the telecom market. As some satellite network operators move to provide D2D services, we are seeing a new opportunity. Our medium and high-power 5G technology is directly applicable to D2D systems as there is significant similarities in the requirements.
We also continue to see market share gain opportunities in the terrestrial 5G, although the overall RAN market demands remain flat. In wireless infrastructure, our teams are advancing our new GaN products for macro and massive MIMO applications. We are making steady progress, and we believe our relationships with the 2 leading Western telecom OEMs has never been stronger.
Investors should be aware that we remain focused on executing a long-term strategy to provide differentiated semiconductor solutions for the highest data rate, highest power and highest frequency applications in noncommodity markets. We believe this strategy will create a superior business model and produce strong long-term financial returns for our stockholders. Our strategy relies primarily on organic growth driven by internal product development and R&D investment.
However, we also recognize that strategic M&A can play an important role by expanding our management team and engineering teams, our technology portfolio and market exposure. We believe our recent M&A activities and investments have made MACOM a stronger company. We maintain an active pipeline of opportunities and continually evaluate potential targets. Our approach has been and will continue to be highly selective and disciplined.
In summary, we will continue to build a best-in-class and diversified company. Based on our long-term strategic plan, we believe we have the opportunity to double our revenue and profits over the next couple of years. Jack will now provide a more detailed review of our financial results.

**John Kober** (Executives):
Thank you, Steve, and good morning. Before getting into our fourth quarter results, I'd like to summarize a few items regarding our full fiscal year 2026, which ended on October 2, 2026. Bookings were strong across all of our end markets, resulting in a full year book-to-bill of 1.5:1 and marking our highest bookings year ever. We achieved record revenue of over $1.3 billion, which grew more than 37% over fiscal 2025.
Our annual adjusted operating margin grew by 660 basis points to 32%. Adjusted earnings per share grew by more than 61% to $5.60. Cash flow from operations continued to strengthen and increased by approximately 52% to $357 million. We have continued to invest in the organization by expanding our production capacity and our research and development capabilities to support our growing business.
Now on to our fourth quarter fiscal results. Fiscal Q4 revenue was $424.8 million, up 24.1% sequentially and up 62.7% year-on-year, driven by growth across all 3 of our end markets, with data center again leading, followed by solid growth within I&D and telecom. Adjusted gross profit for Q4 was $260.3 million or 61.3% of revenue. This represents a gross margin increase of 160 basis points over the prior quarter, primarily as a result of revenue growth, product mix and factory utilization.
Total adjusted operating expense for our fourth quarter was $98.1 million, consisting of research and development expense of $67.5 million and selling, general and administrative expense of $30.6 million. As anticipated, the sequential increase in adjusted operating expense compared to Q3 2026 was primarily driven by ongoing R&D investments and employee-related costs. Adjusted depreciation expense for fiscal Q4 2026 grew modestly to $9.2 million, up 2.4% from the prior quarter.
Adjusted operating income in fiscal Q4 was another record coming in at $162.3 million, up 50.6% sequentially from $107.7 million in Q3 2026 and up 142.2% year-over-year. I would like to note that our Q4 2026 operating margin was 38.2%, reflecting the leverage in our financial model as the business continues to scale. I'll also note that we expect our adjusted operating margin to continue to increase and exceed 40% as we move through fiscal 2027.
For fiscal Q4 2026, we had adjusted net interest income of $6.1 million, an increase of approximately $600,000 sequentially from $5.5 million in Q3 2026. Our adjusted income tax rate in Q4 was 3% and resulted in an expense of approximately $5.1 million. As discussed on prior calls, as a result of the growth in our profitability, combined with the utilization of our remaining historical deferred tax assets, we anticipate our adjusted income tax rate to increase from 3% to approximately 6% for fiscal year 2027 beginning in Q1.
And to close out our fiscal Q4 2026 income statement discussion, I am pleased to note our adjusted net income increased 48.8% sequentially this quarter to $163.3 million compared to $109.8 million in Q3 2026. Adjusted earnings per fully diluted share was $2.09, utilizing a diluted share count of 78.3 million shares compared to $1.40 of adjusted earnings per share in fiscal Q3 2026.
Now on to operational balance sheet and cash flow items. Our Q4 accounts receivable balance was $209.5 million, up $30.4 million compared to our Q3 2026 balance. Our days sales outstanding averaged 45 days, down 3 days compared to 48 days in the previous quarter. Inventories were $284.3 million at quarter end, up $2.8 million sequentially from $281.5 million. This increase was to support the demand across the business.
Fiscal Q4 cash flow from operations was approximately $155.5 million, up $76.6 million sequentially or an increase of 94.5%. Capital expenditures totaled $17.5 million for fiscal Q4, down from $20.8 million in Q3 2026. Our total CapEx for fiscal year 2026 was $64.4 million, in line with our projections, and we anticipate fiscal year 2027 CapEx to be between $100 million and $110 million. A majority of this CapEx will be focused on expanding capacity at our existing production facilities and enhancing our R&D capabilities in support of customer demand.
Next, moving on to other balance sheet items. Cash, cash equivalents and short-term investments as of the end of our fiscal fourth quarter were $792.4 million. These strategic assets provide us with increased flexibility to fund ongoing investments and respond quickly to new opportunities. We are in a net cash position of approximately $451.7 million as of October 2, 2026, when comparing our cash and short-term investments to the book value of our remaining $340.7 million of convertible notes, which mature in December 2029.
In closing, I'd like to recognize that the results we have achieved during fiscal year 2026 were due to continued successful new product introductions, disciplined execution and strong contributions from the entire MACOM team. I will now turn the discussion back over to Steve.

**Stephen Daly** (Executives):
Thank you, Jack. MACOM expects revenue in fiscal Q1 ending January 1, 2027, to be in the range of $450 million to $460 million. Adjusted gross margin is expected to be in the range of 62% to 63% and adjusted earnings per share is expected to be between $2.21 and $2.29 based on 79 million fully diluted shares.
We expect approximately 15% sequential growth in data center revenue, single-digit sequential growth in Industrial and Defense revenue and flat to slightly down revenue in telecom. As we look ahead, we believe our strategic plan positions MACOM to become one of the most profitable companies in the semiconductor industry. We are pleased that the midpoint of our Q1 guidance represents a 40% operating margin. I would now like to ask the operator to take any questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Harsh Kumar of BMO. Your line is now open.

**Harsh Kumar** (Analysts):
As usual, phenomenal execution. Steve, I'm going to do you a little unfair question. So humor me with this unfair question. You're the first company in my universe that plays in data center to report after the midterm. When we talk to investors, they are very comfortable with 2027 data center outlook, but really uncertain about what happens in 2028 with all these changes in the midterm, whether these data centers will get built to full capacity or not.
I'm curious if you have -- as you talk to your large customers, if you have any window or viewpoint into what they're thinking or saying about not outlook, but just viewpoint into 2028. And then I've got a follow-up.

**Stephen Daly** (Executives):
Thank you, Harsh, for the question. And certainly, the results of the election this week are very fresh. But I can tell you a lot of the work we're doing as a company revolves around installing and launching products, not only for 2027, but also 2028 and 2029. So we're keeping very much a long-term view on the market.
My personal opinion is the elections and the results aren't necessarily going to derail a lot of the work that will be done over the next 5 years inside this industry. So from our point of view, we're staying focused on executing our long-term plan.

**Harsh Kumar** (Analysts):
And then maybe one for Jack. The gross margin is going up a lot more than I would have thought. I would have thought you guys would have put up 50, 60 basis points of gross margin increases sequentially, but you've sort of hit a new trajectory of 100-plus basis points of gross margin improvement. Curious what is happening, why it's being driven the way it's being driven, if it's mix or something in manufacturing that we need to think about?

**John Kober** (Executives):
Yes. Thanks for the question, Harsh. There's a number of factors, obviously, that are contributing to the improvements that we've seen in our gross margin over the fiscal year 2026 time period. Some of it is driven by the top line growth that we've seen, being able to better utilize some of our existing manufacturing facilities has been a contributor.
The new products that we've introduced, we've been talking about new product introductions for a long time, and those generally have higher gross margins. So that's helping to support the improvements and also a credit to our operational teams. They've been doing a lot to make sure we're more efficient in terms of reducing waste and getting yields up and things along those lines.
So a number of different moving pieces that we've seen that have contributed to those improvements. And as we go forward, we would expect to try and continue to grow our gross margins, but it becomes a bit more challenging as you go forward, but we still think there's more room there to continue to grow at the gross margin level.

**Operator** (Operator):
Our next question comes from Tore Svanberg of Stifel. Your line is now open.

**Tore Svanberg** (Analysts):
Congratulations on the very strong results. Steve, as I sort of consider your segment comments for fiscal '27, it looks like you're going to approach at least -- well, you're going to approach $2 billion in revenue. I'm just curious, based on where we stand today, are you thinking about that sort of as a base case? And where could potentially there be some upside to that potential $2 billion number?

**Stephen Daly** (Executives):
Thanks, Tore. So as you know, we don't give full year guidance, and it's very early in our fiscal year, but we are very pleased that we're starting the year with record backlog. And based on the backlog and some of the order trends, as I mentioned in my script, we think we can exceed the growth rates inside the data center. We think our base case today is about 80% year-over-year growth. So we're pretty excited about that.
We also believe we're going to beat last year's year-over-year growth in I&D, which was just around 28%. Our goal is to push that over 30%. And then telecom, low double-digit growth and also very early in the year to sort of really lock that number down. I think we're going to start the year in telecom a little bit on the light side, and it's going to accelerate as we move into the year.
But I think your math is correct. If you just annualize the midpoint of our first quarter guide, you get to sort of that $1.8 billion level, which represents 37% year-over-year growth from our fiscal '26. And frankly, we would expect to do better than that. We think the second half of our fiscal '27 will be stronger than the first half. And there's structural reasons why we are bringing capacity online.
We have programs that will really ramp in production. And we have new programs coming online in really all 3 of the different markets that we serve. So I think while we don't give full year guidance, I think, certainly, we're looking at that $2 billion target and trying to scratch our way there. But there's certainly a lot of work to be done. It's early and there's risk associated with execution and, of course, market risk. But we're feeling very confident that our fiscal '27 is going to be a record year.

**Tore Svanberg** (Analysts):
Yes, that's great color. And as my follow-up, you mentioned 1 of the 3 areas where you've had some meaningful progress in fiscal '26 was on the CW laser side of things. I think you've always been a little bit cautious on the company's opportunity, but you sound much more upbeat on this particular call.
So anything else that you could share with us as far as design wins? I think you did mention you expect to start shipping CW lasers in fiscal '28. But yes, any other color you could share with us on the traction for CW lasers would be really helpful.

**Stephen Daly** (Executives):
Sure. And I think we've talked about on the last few calls that we have a CW laser that's meeting customer requirements. So from an optical performance point of view, we have a very solid product. What we've been focused on over the past 2 to 3 quarters is the quality and the reliability of the laser. And that battle is won or lost on the quality of the facet.
And so over the past 6 months, our team has really had some nice breakthroughs on the quality of the facet. And we use a very MACOM-specific approach when we create the facet. We do that in our fab using ion beam technology. And that has some pros and cons. But at the simplest level, it can leave the facet being rougher than you want.
And recently, we have made significant technology improvements, which effectively take a facet that looks like it was cut by a chainsaw and now it looks like it was cut by a sushi knife. It is absolutely unbelievable. And we think that will directly translate into an incredibly reliable facet. And that's where -- that's the hottest point in the laser.
The other thing I'll highlight is we will be a merchant supplier of lasers, and we will be one of the few U.S.-based manufacturers of this technology. So as we make progress on improving the quality of the facet, it will open up new opportunities, not only at the lower 75-milliwatt power levels, but also the 100-milliwatt power levels. And we have other interesting technology development behind that to push ourselves to even higher powers.
And certainly, that's further down the road. So the team has done a great job. We think that we still have a lot of work to do. We're not declaring success today, but I can tell you that we have some meaningful technical progress that the team is very excited about. And I congratulate them for all the hard work they're doing.

**Operator** (Operator):
Our next question comes from Tom O'Malley of Barclays. Your line is now open.

**Thomas O'Malley** (Analysts):
First one is on the linearity of telco. You're saying the full fiscal year grows faster than fiscal year '26 kind of a starting point, but you're saying kind of a slower start to the year. So you guided down 1% for December, let's just keep it flat in March. That kind of implies strong mid-teens growth in the back half of the year to kind of get there.
So can maybe you explain a little bit that dynamic? Is there a program that's ramping on? What's a little weaker in the first half of the year? And why does it step up so much?

**Stephen Daly** (Executives):
Yes. And just to highlight that the target is to get our telecom business over $300 million in our fiscal '27. And that will be the fourth or fifth consecutive year of sequential growth. So our product lines and our business units are doing a great job of growing the business. As you know, it's not linear. And so timing of orders matters, especially when you're at this level of revenue.
I will highlight that our book-to-bill for telecom during fiscal '26 was greater than 1. So we have pretty good backlog there. But we are seeing softness. We see some softness in PON. We see some softness in some of our broadband business. And while we're doing some great work with securing new 5G sockets, those programs are going to kick in later in the year.
So due to all of this, we think things should be stronger in our second half. And I also think during the course of the next 12 months, there's going to be lots of new opportunities that maybe allow us to sort of exceed these numbers. As you know, we include LEO business, LEO constellations in our telecom segment. And our LEO business is doing quite well right now.
We are building large backlog. A lot of that backlog will ship through in fiscal '27 and also in fiscal '28. So generally speaking, things are going well in the telecom market. We're moving as quickly as we can to keep it on a reasonable growth pace.

**Thomas O'Malley** (Analysts):
Great. And then just as my follow-up, just a broader market question. So you had an acquisition in the space earlier this week or last week, I don't remember. And you've seen other companies in your space like Astera Labs talk about their TIA and driver portfolios.
So I just wanted to ask, when you move from TIAs and drivers in pluggable modules and you look at NPO solutions, could you maybe talk about the competitiveness of your portfolio there? You're obviously handling more channels, but then you're going to go up against players with more integrated solutions. So maybe walk through if that means that you're going to see some share shift there and just the quality of your product as you move to handling more channels? Is there any sort of competitive dynamic on the technology side as well?

**Stephen Daly** (Executives):
Yes. Well, certainly, the product lines we sell into the data center are very competitive. And the companies you've listed are certainly -- have been and will continue to be competitors from our point of view. I think it's critical that we bring our best game to the market every day. And when we look at the technology we have and the opportunities with NPO, specifically, you've seen this migration, as you know, from LPO over to sort of XPO and now NPO.
Our technology is perfect for that application. When you start to get into more highly integrated advanced silicon CMOS-based fully integrated solutions, that's not an area we play in. So we are more of a multifunction or single-function SiGe high-performance solution. And we think the size of the opportunities that we're seeing in NPO are significant.
We think the hyperscalers are going to do market share across multiple vendors regardless of -- the data rates are regardless of the form factors. And I can tell you that we're right in the fight. So we're dealing with the major hyperscalers. We're dealing with their supply chain. We're actively sampling and developing products for NPO. And we frankly look at this opportunity as a multibillion-dollar opportunity. And I would imagine MACOM is going to get some piece of that.

**Operator** (Operator):
Our next question comes from Blayne Curtis of Jefferies. Your line is now open.

**Blayne Curtis** (Analysts):
Maybe I'll follow on behind Tommy on the NPOs. Just kind of curious, you have engagements. This seems like the Wild Wild West, everybody pursuing different flavors. Now you're starting to hear some concrete wins. So I'd just be curious, when you look at the engagements you have, when do you think those things are awarded? And then any thought on timing? It's probably not fiscal '27, but I'm curious what you're seeing.

**Stephen Daly** (Executives):
Yes. As you know, Blayne, we keep our cards close to the chest when it comes to customer engagement. So we can't really comment on the wins and engagements or the agreements and contracts and things like that. What I can tell you is we are right in the middle of supporting these opportunities, and we'll have to wait and see how things shake out over the next year.

**Blayne Curtis** (Analysts):
Got you. And then I wanted to ask a big step-up in CapEx, obviously, seeing another strong growth year, so it makes sense. I'm curious, just as you look out, you mentioned this is a multibillion-dollar opportunity, might even be more. Scale-up is a 10x multiplier, scale in is even bigger. So I'm just kind of curious versus your fab footprint, like how much runway do you have to expand your capacity here?

**Stephen Daly** (Executives):
I think that's a great question. And so when we think about expanding our fabs to support our data center business, that work is primarily here in Massachusetts. And so we have a 2-phase program that we're rolling out. We're about 2/3 the way through Phase 1. That program will provide equipment and space to support the ramps in 2027 based on existing business and new business coming in.
And then we will have a Phase 2 event, which will support a lot of the CW laser business, and we will kick that effort off probably in mid-2027 based on how things shake out with the performance of our CW lasers. When you look at the $100 million to $110 million, I would say about 60% of that is going into the fabs. Remember, we have a fab here in Massachusetts. We have the RTP fab, and we have a fab in France. Those are our 3 primary fabs.
And so most of the dollars are going into modernization or adding capacity. As you remember, last fiscal year, we talked about adding 30% capacity at our RTP fab. Our RTP fab right now is producing more wafers than they ever have and the outlook for that facility is extremely strong, primarily driven by defense, then second, telecom and even some future D2D business. So I think the health of our fabs and the spending we're doing in the fabs is quite targeted.
And then the other thing I'll highlight is because it's related, we are still actively engaged with the CHIPS program office. As you know, we announced -- we signed a PMT in January of 2025 to make major investments in our Lowell and RTP facilities. We are probably 1 or 2 quarters away from signing a DFA. That will provide significant funding to MACOM to do a lot of the things that we need to do to stay on our growth trajectory.
So the team has done a really nice job aligning the CPO program with the needs of the business. And so it's a huge opportunity for MACOM to leverage some of the support from the government. So I think we have capital under control. I will say that since 2019, the first 2 to 3 years of running the business, this management team was underspending on capital. And I would say, in the last 3 years, we've started to be very targeted. And we like to spend the money when we have the business. We don't typically lean in, build the factory and then hope the business comes. So we sort of are very careful as we spend this money.

**Operator** (Operator):
Our next question comes from Quinn Bolton of Needham & Company. Your line is now open.

**Quinn Bolton** (Analysts):
Let me add my congratulations on the nice outlook for 2027. Steve, I just wanted to follow up on the production capacity. You kind of went through the company's internal CapEx plans. I think a lot of your data center business, certainly the SiGe part is largely outsourced. You're talking about a base case growth for data center up 80%. How are you feeling about your external foundry relationships in terms of capacity support for SiGe as you look to fiscal 2027 and beyond?

**Stephen Daly** (Executives):
I think that's a great question. And I think some of the capital spending that we'll be putting in place supports scaling the back end, being assembly and test, a lot of times, that is done offshore. So I just want to sort of highlight before we get into the relationships with our foundries that some of the capital spending is supporting the back-end work. And as we talked about some of these volumes going up by orders of magnitude, we want to make sure we have enough infrastructure to support that on the back end.
You've seen many companies in the last 4 or 5 months put out press releases that they've signed long-term supply agreements with various companies like GlobalFoundries, ST, Tower, TSMC. That is not our style. We don't do that. We engage very privately and confidentially with our supply chain. We make sure that we are getting the wafers we need. I will say that some of the behaviors of the SiGe fabs is more rather than sort of target-based commitments.
They are looking for firm commitments. And MACOM won't be shy about signing up and make sure that we are securing the supply that we need to make sure we hit our growth targets. The other thing I'll highlight is our HPC and Lightwave teams that are providing these high-end products have a very strong experience not only at Tower, but ST and GlobalFoundries. And so we're keenly aware of those technologies, the strengths of those technologies, and we align the best technologies with our product road map.
We're very good at that. And so we have a very nimble and experienced team that is not only looking at the technology road maps of our suppliers, but we also look at their capacity as well. So when we think about the next 5 years, that is something that will be well managed by our supply chain staff. What we are primarily focused on is out designing the competition. You have to beat the competition with a better product and then the volume will come.

**Quinn Bolton** (Analysts):
Excellent. And then just for Jack, as we think about the gross margin progression going forward, do you think we're back to sort of a 25 to 50 basis points a quarter progression as you look through '27?

**John Kober** (Executives):
Yes, that's our current view. really haven't changed that view. We've been fortunate that we've been able to exceed it during fiscal year '26 as the top line grew quite nicely. But yes, that 25 to 50 basis points on a quarterly basis as you step your way through '27 feels appropriate.

**Operator** (Operator):
Our next question comes from Gary Mobley of StoneX Group. Your line is now open.

**Gary Mobley** (Analysts):
Given all the inflationary pressures in your supply chain, given your high utilization rate at your own fabs, I'm curious to get your thoughts on the pricing environment on a like-for-like product basis.

**Stephen Daly** (Executives):
Yes. So I think our sales and business unit leadership is very good at optimizing the pricing so that we're providing value to the customer, but also covering our costs. And when our costs go up, we study whether it's possible to pass those costs over to customer. So I would say that while our overall costs are going up across the board, whether it's raw materials, energy, labor, we've been able to manage those increases quite well.
And as you can see, over the last few years, we've moved our gross margins from the mid-50s now to the low 60s. And quite frankly, as Jack mentioned, with our new products coming out that have even higher margins, we see a path to having gross margins in the mid-60s in the not-too-distant future.

**Gary Mobley** (Analysts):
As my follow-up, I want to ask about some development earlier this week. It appears as though we might see a terrestrial build-out, 5G build-out, 6G build-out by Starlink to complement their satellite network, essentially adding another operator in North America. I'd love to get your thoughts on how that might eventually impact the RAN market.

**Stephen Daly** (Executives):
Well, that's a great question. And so we think that's an opportunity for MACOM. And as I mentioned in my prepared remarks, a lot of our 5G technology is applicable not only to D2D, but also for those that want to build out their own RAN network. And so yes, I think you're thinking about that the right way that that's an opportunity for MACOM.
I'll highlight that we are the only domestic 5G power amplifier supplier -- so if it's important for a network operator to have U.S. content in their equipment, they will turn to MACOM.

**Operator** (Operator):
Our next question comes from Karl Ackerman of BNP Paribas. Your line is now open.

**Karl Ackerman** (Analysts):
One of your competitors had an Analyst Day earlier this month and noted interconnect revenues could advance at a 65% CAGR through 2030, in part driven by higher demand for analog components using your package optical applications. You happen to address several of these areas. I'm curious if you would also underwrite that industry growth outlook.

**Stephen Daly** (Executives):
We don't typically comment on the size of markets or the growth rates of any particular market. So I wouldn't want to necessarily endorse your comments specifically. But what I will say is we are -- as we approach our customers, hyperscalers and their supply chain, we are seeing very large opportunities for scale up, and we are directly engaged in designing chips or providing samples of chips to meet those needs. And the volumes for scale-up look significant, larger than what we've seen in our past.

**Operator** (Operator):
Our next question comes from Sean O'Loughlin of TD Cowen. Your line is now open.

**Sean O'Loughlin** (Analysts):
Congrats on the results. Steve, I wanted to lean into the comments you made in the prepared remarks on the V-band and the analog linearizers are -- let's just pretend I know what those words mean. And as we think about the base or the ground station opportunity for LEO, especially in the expanding V and W bands, they sound a lot like sort of MACOM's wheelhouse.
Maybe if you could just talk about the competitive landscape on that front? Like who are you -- or is it almost a MACOM-only market? Are there other competitors that we would know about? Or is that just a sort of greenfield growth opportunity for you guys?

**Stephen Daly** (Executives):
Yes. When you look at the SATCOM market and the ground station market, there's an annual trade show in Washington called the SATCOM Show. And what you see is hundreds of companies producing uplinks and downlinks. Some of those companies are designing their own power amplifiers. Some are using TWTs. Almost all of the TWTs are linearized, and there's only one company that's here in the U.S. that produces this type of linearizer and that's MACOM.
So we do have some other international competition. But generally speaking, whether it's a military uplink or a high-volume uplink, our team is very good at supporting this market. It's not a huge market, but I would say we're #1 in this space. If you remember, we purchased a company called Linearizer Communications Group about 3.5 years ago. We purchased this company for 3 reasons.
One, they were very strong at SSPAs, so power amplifiers. Second, they had analog microwave linearizers. And third, they had RF over fiber technology. And we embraced all 3. We felt those technologies were very complementary to the work we were doing. And so as the SATCOM market has grown, we've been the beneficiary of supporting the growth and a lot of the chips that are going inside these V-band linearizers are MACOM components.
So high level of MACOM content, high dollar value, very sticky business. We form very close relationships with the various TWT companies that produce these high-power devices. We're seeing these not only on the ground station, we are actually -- we have won some linearizer business for satellite-based linearization as well. So it's a great business. It's classic MACOM, as you pointed out.

**Sean O'Loughlin** (Analysts):
Great. I'll look up a lot of those words later. As a follow-up, I wanted to maybe ask, I guess, both of you, Steve or Jack, I actually got a question intra-quarter about buybacks or dividends for MACOM, which I think is quite a milestone and reflects sort of the strength of the balance sheet and really the cash flow statement.
So just wanted to get your thoughts on the capital allocation priorities. Obviously, the CapEx is stepping up, but maybe is there any shareholder return or maybe you just want to gloat about the cash flow generation?

**Stephen Daly** (Executives):
Well, yes, thank you. So we don't have any plans at this point to do buybacks or start a dividend program. And as you highlighted, we believe cash is king, and we're accumulating cash. Certainly, in the next year, we're going to generate a lot of cash. That will be used for internal R&D and some modest expansion, but it will also be used to make sure we execute our long-term strategy.
And if you think out to 2027, let's assume for a minute, we can achieve $2 billion in, say, $10 of earnings. But if you go out to 2030, it's we want to be a company that's $5 billion. And so when we think about how to get to $5 billion, we recognize that we're going to need additional technologies, more staff. We're going to need to enter some other markets. A core part of our strategy is we like running a diversified business.
So today or in fiscal '26, I&D was 40% of our business. Data center was 38% and telecom about 20%. And you might argue that these 3 markets are disassociated and not correlated, and we like that. We think that's good for business. It protects our customers. And so when we think about achieving $5 billion in revenue, we think, okay, we want to start accumulating cash. We want to make sure that we have optionality as we move ahead.
And certainly, today, we're in a great growth environment. All the markets are strong. 2, 3 years down the road, that may not be the case. And we want to make sure that if the bottom falls out from the markets that we have a lot of dry powder. So we do keep a long-term perspective on our growth strategies. And I think Jack and I are like-minded that more cash is better. And Jack, I'll turn it over to you for additional.

**John Kober** (Executives):
No, I think you did a good job summarizing everything there, Steve.

**Operator** (Operator):
Our next question comes from William Stein of Truist Securities. Your line is now open.

**William Stein** (Analysts):
I'd like to follow up on an earlier question about profitability that's coming in better than previously expected. And when you were going through the reasons behind that, one that you didn't talk about is mix by end market. And I was just hoping you can remind us among the 3 end markets or maybe you could say even 4, if you break up industrial and defense, which of these tend to be richer in profitability? And if mix is part of what's driving this upside?

**Stephen Daly** (Executives):
Yes. Mix will always be a part of the ultimate gross margin answer, and that could be at product levels or even across some of the 3 different end markets. And we -- when we look at our end markets from a profitability standpoint, they usually fall within a bell curve and don't deviate much from that over time. So we don't necessarily break it out by each of those end markets.
But obviously, the volumes are increasing over the past number of years, and that's supporting some of the improvements that we've seen in the gross margin. And then we're also seeing, as I had mentioned earlier, some of the newer products that we're introducing that are going into these end markets and those newer products tend to have higher gross margins. So those are some of the contributing factors that we have with regard to that gross margin growth we've seen over the past year.

**William Stein** (Analysts):
And then as a follow-up, you guys have done a great job, very efficient job on investing in R&D for new product development, as you've highlighted on the call. Some companies that I cover in semis have talked about using AI tools to improve the efficiency of R&D. And I wonder to what degree you've adopted that? Or are you still evaluating it? Any early successes or direction you can talk about in that regard would help.

**Stephen Daly** (Executives):
Thank you for the question. And you're right, our spending in R&D is really the future lifeblood of MACOM. And we've been increasing our R&D spending by about 20% a year over the past few years. In 2027, we should spend somewhere around $300 million. And if you just go back to 2023, it was about $130 million. So significant growth in R&D spending over the past few years.
We absolutely are evaluating and utilizing AI in the business today. I won't get into the details as to where, but I can say that, yes, our engineering organization is absolutely looking at AI to support the design process. In fact, we have established a dedicated group to only use AI in the design process because we want to push ourselves and push the limits. And so we'll see how that goes. Using AI is not free.
And so at the end of the day, we'll do a cost-benefit analysis to see if we're getting a better result and a more efficient and faster result. The other thing I'll highlight is we've partnered recently with one of the CAD tool providers, and they have given us an incredible -- we've worked together to create an incredible transaction where we have almost unlimited simulation capacity to run some AI activity, which this capacity would have cost perhaps tens of millions of dollars if we were just buying seats.
And so we have developed a very nice strategic relationship with a leading CAD supplier. And over the next year or so, we're going to see if we're able to use AI in a way that really is meaningful to the design process. So early days, but I can assure you that, yes, we are evaluating that. We're trying to properly resource this activity, and we'll have to see how it plays out.

**Operator** (Operator):
Our next question comes from Christopher Rolland of Susquehanna International Group. Your line is now open.

**Christopher Rolland** (Analysts):
Mine is around copper and if there are any other developments around either ACCs or copper linear equalizers on PCB and kind of the outlook for next year for these products as well, would be great.

**Stephen Daly** (Executives):
Thank you for the question. Excellent progress over the past 4 months regarding our equalizer products getting traction and very, very positive results there. If you may remember, we refreshed our linear equalizer products early in FY '26. And we're starting to see the fruits of those -- that effort, and we're starting to get very, very good results from various cable companies and even one particular hyperscaler that is essentially telling us we're meeting requirements.
So we'll have to see how things shake out in this year. But right now, the team is doing great. So our latest 200-gig equalizers, to be clear, seem to be meeting system requirements. We also have multiple versions of that same equalizer that we think are even better, and we have higher data rate equalizers that we'll be providing customers as well. So from our point of view, it's a great opportunity.
It is absolutely part of the scale up application, which means there could be some significant volume there. So yes, we would expect to see some business from all this effort in our fiscal '27, most likely in the back half. But generally speaking, I think we've recovered our position in the market, and we're on track.

**Christopher Rolland** (Analysts):
Excellent. And Steve, as a follow-up, data center 80% growth is pretty enormous next year. Obviously, you're selling more of what you sold in '26, but any kind of further conversation about how composition changes, how new products roll into that portfolio and bookings for the year just as we contrast '26 versus '27 in data center for that growth?

**Stephen Daly** (Executives):
Yes. I think when we look back on 2027 and compare it to '26, I think you're going to see MACOM will have shipped more 200-gig per lane drivers and TIAs. You will see that we have more capacity to manufacture indium phosphide products, and we're shipping more there. We may be seeing early revenue in NPO. We'll have to see if it falls into this year or next fiscal year.
Coherent lite is meaningful. We think that you'll start to see coherent lite kick into gear. We just talked about the equalizers coming online in the back half. We're also -- and we don't talk about this a lot, but we're very active with PCIe. And so we have a very strong solution there. We've been demonstrating it over the past 6 months. We're getting traction there, and we feel like there may be some opportunities in our fiscal '27.
And then the last wild card, as we talked about, is the CW laser, which is more of a 2028 opportunity. However, as I mentioned, we are seeing big demand on our 25G DFB lasers as a lot of laser manufacturers are sort of shutting that business. And so that 100-gig per lane business is picking up for us, and that will grow year-over-year as well. And maybe the last thing I'll mention is LPO is doing quite well, and the business is growing significantly year-over-year.

**Operator** (Operator):
Our next question comes from Harlan Sur of JPMorgan. Your line is now open.

**Harlan Sur** (Analysts):
Great job on the quarterly execution. The team is doing just an awesome job on the innovation front, bringing your standard products to the market. That being said, I mean, more and more of your customers are building their own internal chip design teams. They want access to your technology. They want access to your design IP, advanced packaging capabilities.
Foundry and custom design services has always been a part of the MACOM strategy, right? You guys offer the most diverse set of III-V compound semiconductor processes in the industry. I think like something like 15 to 20 different process types, different device architectures, PIN diodes all the way to pHEMTs. How big is the foundry and custom products business? Is it still a focus area for the team? And your view on the growth outlook there?

**Stephen Daly** (Executives):
Yes. Foundry is a portion of our business. We would always rather sell a product. But if customers would rather design the chip themselves, we open up our fabs for them. I would say about half of our business coming out of our French fab is foundry business from European defense contractors. In the U.S., our RTP fab, the foundry business is a shrinking portion of the business, primarily because our product sales are taking off, but we have some major U.S. defense customers using the RTP fab.
And here in Lowell, we have probably about 3 or 4 major foundry customers, mostly on the defense and test and measurement market. We have recently engaged a company that wants to use our fab for LiDAR applications. So we've done a sort of a special deal supporting some of their indium phosphide work, which could turn into some interesting volume in the future.
But so yes, we embrace foundry. We think that's important to engage customers at any level they want. In fact, one of our largest LEO customers has really, over the course of 4 or 5 years, you've seen that relationship move from basically a module -- complex module product sale to a foundry relationship. And so yes, we embrace foundry. We consider ourselves having open foundry, and it is a strategic activity for us.

**Harlan Sur** (Analysts):
And then on the manufacturing footprint expansion, you mentioned expansion at 3 fabs, one being Lowell. I believe you said that the other 2 are going to be Europe and your RTP fabs. Are you guys still doing manufacturing in Ann Arbor and California? And I assume that most of the spend is just equipment buys and that you already have cleanroom space facilitized and already stood up at these locations?

**Stephen Daly** (Executives):
Correct. And just I'll very quickly walk through some of the various activities. So first, we still have our Ann Arbor facility. They are doing a significant amount of R&D on next-generation products. They are really geared towards, I would say, low and medium volume indium phosphide. They have an MBE reactor, and they are able to develop their own epi, and that's really one of the key technologies that we bring to our PD product line.
Our RTP fab is primarily GaN on silicon carbide. We have no plans to expand beyond the 4 walls of that facility. There's plenty of room inside the facility to expand. And so we're adding equipment in that fab. Our French fab is primarily moving, again, multiple buildings, plenty of space. We have no plans to build more buildings.
Instead, what we're doing is we're migrating their technology from 3-inch to 6-inch wafer sizes. We just recently installed a brand-new G10 reactor so that we'll be able to scale up and support the high-volume production that they're moving towards. And then here in Lowell, our Phase 1 and Phase 2 plans will also be executed within the 4 walls of our building.
We do not want to build another building. So we will add more capacity and we'll remove office space and maybe the cafeteria, if that's what it takes to make more wafers. So very efficient use of space, not greenfielding a fab, basically taking advantage of the market and installing capacity as quickly as we can.

**Operator** (Operator):
I am showing no further questions at this time. I would now like to turn it back to the President and CEO, Steve Daly, for closing remarks.

**Stephen Daly** (Executives):
Thank you, Amber. And just to be clear, we'll leave the cafeteria alone. We have no plans to convert that to production space yet. So in closing, I'd like to thank our employees, our supply chain partners and customers for making these results possible. Thank you.

**Operator** (Operator):
Thank you for your participation in today's conference. This does conclude the program, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MTSI_Q3_2026_Earnings_Call_20260806.md
- 2026-08-06｜CEO Stephen Daly｜guidance：FQ4 毛利率財測 60%–61%（原話："gross margin is expected to be in the range of 60% to 61%"）
- 2026-08-06｜CEO Stephen Daly｜guidance：FQ4 調整後 EPS 財測區間（原話："per share is expected to be between $1.97 and $2.03"）
- 2026-08-06｜CEO Stephen Daly｜guidance：FQ4 資料中心季增財測約 35%（原話："approximately 35% sequential growth in Data Center"）
- 2026-08-06｜CFO John Kober｜guidance：FQ4 調整後營業利益率預期約 37%（原話："approximately 37% for the fourth fiscal quarter."）
- 2026-08-06｜CFO John Kober｜guidance：FQ4 營運現金流預期超過 1 億美元（原話："operations will be in excess of $100 million."）
- 2026-08-06｜CFO John Kober｜guidance：FY26 CapEx 預估 6,000–6,500 萬美元（原話："CapEx to be in the range of $60 million to $65 million."）
- 2026-08-06｜CEO Stephen Daly｜guidance：FQ4 財測中點年化後 FY27 公司成長約 27–28%（原話："20s, 27%, 28% as a company."）
- 2026-08-06｜CEO Stephen Daly｜guidance：同樣算法下資料中心 FY27 約 50% 成長，管理層稱為 base case（原話："that number then trends to 50% year-over-year growth."）
- 2026-08-06｜CEO Stephen Daly｜guidance：電信今年預期雙位數成長，明年類似或更好（原話："similar performance or better performance next year."）
- 2026-08-06｜CFO John Kober｜guidance：稅率預告：FY27 逐步由 3% 升至個位數中段（原話："we anticipate our adjusted tax rate will begin to rise"）
- 2026-08-06｜CFO John Kober｜margin：Q3 調整後毛利 2.042 億、毛利率 59.7%（原話："was $204.2 million or 59.7% of revenue"）
- 2026-08-06｜CFO John Kober｜margin：管理層預期毛利率於 FY26 餘季與 FY27 逐季改善（原話："ongoing quarterly sequential gross margin improvements"）
- 2026-08-06｜CFO John Kober｜margin：CFO 對 FY27 毛利率改善幅度給出每季 25–50bp 的口徑(較 FY26 的速度放緩)（原話："25 basis points to 50 basis points per quarter"）
- 2026-08-06｜CEO Stephen Daly｜margin：FY27 營業利益率目標為突破 40%（原話："or breach the 40% operating margin level."）
- 2026-08-06｜CEO Stephen Daly｜margin：投入成本上漲(人工、電力、原料),不一定能轉嫁客戶（原話："We try to pass those costs on to customers"）
- 2026-08-06｜CEO Stephen Daly｜margin：管理層稱近一年通膨上升期間毛利率仍擴張（原話："we've been able to expand our gross margins"）
- 2026-08-06｜CEO Stephen Daly｜margin：產品組合：PD/雷射晶片小，少量晶圓可產出大量元件;管理層稱組合效應將在 FY27 改善（原話："These PD laser devices, as an example, are quite small."）
- 2026-08-06｜CFO John Kober｜margin：CFO 預計 OpEx 每季增加數百萬美元（原話："adding a couple, $3 million"）
- 2026-08-06｜CEO Stephen Daly｜product：Q3 資料中心季增約 40%（原話："Data Center increased approximately 40% sequentially"）
- 2026-08-06｜CEO Stephen Daly｜product：200G PD 已量產放量，400G PD 獲正面回饋（原話："200G photodetectors, which are ramping in volume production"）
- 2026-08-06｜CEO Stephen Daly｜product：400G PD 已在約一打客戶手上（原話："perhaps a dozen customers"）
- 2026-08-06｜CEO Stephen Daly｜product：75mW CW 雷射仍在認證，尚未宣告成功（原話："while we cannot declare success yet"）
- 2026-08-06｜CEO Stephen Daly｜product：CW 雷射 HTOL 測試後半段，管理層稱數據優異（原話："we are building our confidence that we have a winner"）
- 2026-08-06｜CEO Stephen Daly｜commitment：CW 雷射預計最早 2027 年底開始量產(準備小額 CapEx 與廠房空間)（原話："a potential start to production in late calendar 2027"）
- 2026-08-06｜CEO Stephen Daly｜product：Q&A 中 CW 雷射量產時點以 2028 表述（原話："If we're able to bring a CW laser into production in 2028"）
- 2026-08-06｜CEO Stephen Daly｜product：25G DFB 雷射因磷化銦 DFB 全產業短缺而需求增加（原話："Customers are coming to us with urgency"）
- 2026-08-06｜CEO Stephen Daly｜product：NPO 有 10–20 個開發專案，營收預期 2028 年起;部分專案不會量產（原話："somewhere between 10 and 20 active NPO development projects"）
- 2026-08-06｜CEO Stephen Daly｜product：NPO 專案部分不會進入量產（原話："Some of these programs will never make it to production"）
- 2026-08-06｜CEO Stephen Daly｜product：資料中心定位為晶片供應商，不做光引擎/模組（原話："we are not going to be building engines and supplying"）
- 2026-08-06｜CEO Stephen Daly｜product：一家大型超大規模業者將部署線性等化器 cable 方案，預期參與（原話："hyperscaler that is looking to deploy that type of"）
- 2026-08-06｜CEO Stephen Daly｜product：公司目前不推被動銅纜方案（原話："do not promote passive copper solutions"）
- 2026-08-06｜CEO Stephen Daly｜product：歐洲防務營收預期 2028 年起成長（原話："sometime in '28, that Defense number will start to grow."）
- 2026-08-06｜CEO Stephen Daly｜product：MESC 預期取得該廠史上最大訂單之一(英國防務客戶)（原話："one of the largest orders in MESC's history"）
- 2026-08-06｜CEO Stephen Daly｜product：衛星光通訊平台新案;管理層稱確立 MACOM 為策略夥伴（原話："This new award establishes MACOM as a strategic"）
- 2026-08-06｜CEO Stephen Daly｜product：車用業務今年預期營收翻倍（原話："is expected to double its"）
- 2026-08-06｜CEO Stephen Daly｜customer：Q3 book-to-bill 創紀錄 1.6:1（原話："Our Q3 book-to-bill ratio was a record 1.6:1"）
- 2026-08-06｜CEO Stephen Daly｜customer：年收入逾 1,000 萬美元的客戶由兩年前約 8 家增至逾 20 家（原話："we have over 20 customers above $10 million"）
- 2026-08-06｜CEO Stephen Daly｜customer：前 10 大終端客戶占比低於 40%（原話："still represent less than 40% of our total revenue"）
- 2026-08-06｜CEO Stephen Daly｜customer：資料中心成長來自美國超大規模業者與企業/運算 OEM（原話："driven by U.S. hyperscalers as well as the enterprise"）
- 2026-08-06｜CEO Stephen Daly｜customer：資料中心年成長：2024 35%、2025 48%、今年約 74%（原話："we're trending towards about 74% this year"）
- 2026-08-06｜CEO Stephen Daly｜customer：防務業務去年成長 19%,今年預期約 25%（原話："And this year, we expect it to grow by approximately 25%."）
- 2026-08-06｜CEO Stephen Daly｜customer：電信中有線纜基礎建設約 +40%、都會長程 +50% 以上（原話："year-over-year will be around 40% growth"）
- 2026-08-06｜CEO Stephen Daly｜competition：兩家 5G 競爭對手退出，公司預期取得部分市占（原話："We would expect to pick up some of that market share."）
- 2026-08-06｜CEO Stephen Daly｜competition：5G MIMO 目前業務很少，管理層稱有機會使 5G 營收翻倍以上（原話："perhaps more than double our 5G revenue"）
- 2026-08-06｜CEO Stephen Daly｜competition：與部分收發模組廠在某些業務領域互為競爭者（原話："we actually compete with."）
- 2026-08-06｜CEO Stephen Daly｜competition：Wolfspeed 關閉 Durham 廠，MACOM 低價取得設備（原話："equipment at pennies on the dollar"）
- 2026-08-06｜CEO Stephen Daly｜risk：針對中國模組廠禁令傳聞：預期客戶組合移轉而非流失（原話："I think we would see a customer mix shift"）
- 2026-08-06｜CEO Stephen Daly｜risk：對禁令傳聞回應為照常營運（原話："we're keeping our head down and it's business as usual"）
- 2026-08-06｜CEO Stephen Daly｜risk：中國無製造據點，約 85 名員工（原話："We have no manufacturing today in China."）
- 2026-08-06｜CEO Stephen Daly｜risk：產能利用率上升使交期拉長（原話："quoting longer lead times for products that are manufactured"）
- 2026-08-06｜CEO Stephen Daly｜risk：CHIPS 協議條款中有對公司『無法接受』者，談判中（原話："are sort of nonstarters for us"）
- 2026-08-06｜CEO Stephen Daly｜capital_allocation：重新向 CHIPS Office 提交改寫後的計畫（原話："we have resubmitted it to The CHIPS Office"）
- 2026-08-06｜CEO Stephen Daly｜capital_allocation：FY27 CapEx 預期與今年相近約 6,000 萬美元，含雷射量產基建（原話："sort of in that $60 million range"）
- 2026-08-06｜CFO John Kober｜capital_allocation：新增產能 CapEx 通常一年內上線（原話："installed and online in less than 1 year"）
- 2026-08-06｜CFO John Kober｜capital_allocation：投資 IQE 6,100 萬美元，說明為強化供應鏈韌性（原話："the $61 million investment we made in IQE"）
- 2026-08-06｜CFO John Kober｜capital_allocation：淨現金約 3.225 億美元（原話："approximately $322.5 million as of July 3"）
- 2026-08-06｜CEO Stephen Daly｜capital_allocation：現金哲學（原話："our philosophy is you can never have enough cash"）
- 2026-08-06｜CFO John Kober｜capital_allocation：CFO 列出現金用途：還債、內部投資、tuck-in 併購（原話："We've done a number of tuck-in type acquisitions"）
- 2026-08-06｜CEO Stephen Daly｜commitment：R&D 費用自 2023 年約 1.32 億增至今年近 2.5 億（原話："we've doubled the amount of R&D spending"）
- 2026-08-06｜CEO Stephen Daly｜commitment：將持續擴編設計中心以追逐 SAM（原話："we will continue to build-out and staff our design"）
- 2026-08-06｜CEO Stephen Daly｜commitment：擬於下季(財年末)提供 FY27 base case 並隨產能與設計案量產上/下調（原話："modulate up or down our Data Center business"）
- 2026-08-06｜CEO Stephen Daly｜commitment：SAM 上修：2027 約 150 億(I&D 60、資料中心 60、電信 30),較 26 年增 20–30%（原話："that's up about 20% to 30% from '26 to '27."）
- 2026-08-06｜CEO Stephen Daly｜commitment：承認對市場數字做了重設(上修 I&D 與資料中心)（原話："a bit of a reset on some of our market-based numbers"）

### 問答異常語氣（迴避／改口／保留）
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Tom O'Malley:FY27 成長軌跡｜答法：稱現在談 FY27 太早，但改以 FQ4 財測中點年化給出約 27–28% 與資料中心 50%,稱為 base case
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Quinn Bolton:資料中心 FY27 要再加速需要什麼｜答法：延後至下季回答，稱『not sure I'm really completely answering your question』
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Karl Ackerman:資料通訊是否會成為最大機會｜答法：先稱對方誤解其說法，改以 I&D 與資料中心 SAM 各約 60 億回答
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Tim Savageaux:雷射/偵測器內容是否大於 TIA/驅動｜答法：不同意前提，表示從未公開比較兩者 SAM,不給數字
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Tim Savageaux:PD 是否已貢獻數千萬美元｜答法：稱不想拆分產品線營收(競爭考量),僅說『more meaningful』且將顯著成長

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
{"date":"20260524","verdict":"B（衛星觀望·thesis 完整｜Q2 FY26 Adj EPS $1.09 beat + DC +48% FY25 至 $293M + 800G/1.6T 200G/lane photodetector 全 module maker design wins + Adj GM 58.5% 目標 60%；但 Fwd PE FY26 76x / FY27 56x 已 stretched + BB 107.9% 上突破 + 52w +127%，等回測 $290-330 或 BB 中軌 $257 區再評估）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"800G/1.6T optical migration + AI infra capex 持續推升 DC segment","columns":{"2Y 驗證點（2026-27）":"Q3-Q4 FY26 DC YoY 維持 +35-40%；FY27 DC revenue ≥ $450M（+50% from $293M FY25）","5Y 驗證點（2026-30）":"FY28-30 DC revenue ≥ $750M（從 2025 $293M ramp 2.5x）；DC 占公司營收 ≥ 50%","10Y 驗證點（2026-35）":"DC TAM 維持 $5B+ at 2030 + MTSI 維持 top-tier supplier 地位","具體數字門檻":"DC segment YoY 連 2 季 ≥ +35%（FY26 Q3-Q4）；FY27 DC ≥ $450M","信息來源":"Q2 FY26 法說會（5/7）+ Stifel / Needham research notes + 800G transceiver shipment forecasts","漂移觸發條件":"連 2 季 TTM 偏離 -10% → 削弱；連 3 季 -10% → 反轉"}},{"id":"H2","text":"Adj GM 達 60% 目標 + Adj OpM 達 30%","columns":{"2Y 驗證點（2026-27）":"FY26 Q3-Q4 Adj GM ≥ 58.5%；FY26 全年 Adj GM ≥ 59%；Adj OpM ≥ 28%","5Y 驗證點（2026-30）":"FY27-30 Adj GM 維持 60%+；Adj OpM ≥ 30%","10Y 驗證點（2026-35）":"FY28+ Adj GM 達 62%+（vertical integration 全效益兌現）","具體數字門檻":"Adj GM 連 2 季 ≥ 58.5%；Adj OpM 連 2 季 ≥ 28%","信息來源":"Q2 FY26 法說會 + IR guidance update","漂移觸發條件":"Adj GM 連 2 季環比 -1pp → 削弱；連 4 季環比 -1pp → 反轉"}},{"id":"H3","text":"200G/lane photodetector design-in 領先優勢維持，pricing power 不被侵蝕","columns":{"2Y 驗證點（2026-27）":"FY27 前無第二家 200G/lane photodetector 商業量產","5Y 驗證點（2026-30）":"2028-2030 仍維持 top-tier 200G/lane 供應商地位 + 400G/lane R&D 領先","10Y 驗證點（2026-35）":"2030+ 1.6T/3.2T+ photonic IC 系列產品線維持","具體數字門檻":"無 Coherent / Lumentum / Sumitomo 200G/lane 量產 announcements；季度 design-win 數量持續增加","信息來源":"analyst sell-side reports + Q4 法說會 competitive review","漂移觸發條件":"第二家 200G/lane 量產 → 削弱；3 家以上量產 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI capex 2027 H1 air pocket → DC ramp 推遲 + 800G/1.6T cycle 延後 6-12 個月","columns":{"對應假設":"H1","時間尺度標記":"⚡ 短期（1-2 季可觸發）","監測指標":"hyperscaler capex YoY；NVIDIA Blackwell shipment；800G+ transceiver shipment","警戒閾值":"連 2 季 hyperscaler capex YoY &lt; 15% → 削弱"}},{"id":"R2","text":"200G/lane photodetector competitor entry → MTSI pricing power 受壓","columns":{"對應假設":"H2, H3","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"Coherent / Lumentum / Sumitomo competitive announcements；MTSI Adj GM 變化","警戒閾值":"連 2 季 Adj GM 環比 -1pp + 競爭者量產 announcement → 削弱"}},{"id":"R3","text":"大型 M&A 失敗 / Wolfspeed integration cost 持續拖累 GAAP earnings","columns":{"對應假設":"H2","時間尺度標記":"🐢 長期（2+ 年慢變數）","監測指標":"GAAP vs Adj EPS gap；one-time charge frequency；M&A track record","警戒閾值":"GAAP NI 連 3 年不及 Adj NI 60% → 質疑 Adj EPS 信任度"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":385.98,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
