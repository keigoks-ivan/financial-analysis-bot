你是 stock-analyst **v20 判斷 agent**，標的 RL（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"RL","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenue_gaap","label":"Net revenue (GAAP)","value":2193.3,"period":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}},{"id":"f_kpi1_adjusted_operating_incom","label":"Adjusted operating income / margin","value":15.7,"period":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":16.6,"period":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}},{"id":"f_kpi3_free_cash_flow_derived_s","label":"Free cash flow (derived, six months)","value":504.0,"period":"Six months FY2027（截至 2026-09-26，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Six months FY2027（截至 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}},{"id":"f_kpi5_guidance_q3_fy2027","label":"Guidance Q3 FY2027","value":"固定匯率營收 +3% 至 +4%","period":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}},{"id":"f_kpi6_guidance_full_year_fy202","label":"Guidance full-year FY2027 (53 週)","value":"固定匯率營收 +6% 至 +7%（上調自 +5% 至 +6%）","period":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}},{"id":"f_kpi7_adjusted_diluted_eps","label":"Adjusted diluted EPS","value":4.64,"period":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}},{"id":"f_kpi8_inventory","label":"Inventory","value":1151.2,"period":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}},{"id":"f_kpi9_adjusted_gross_margin","label":"Adjusted gross margin","value":70.5,"period":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_rl_gross_margin_pct","label":"RL 毛利率","value":71.0,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rl_operating_margin_pct","label":"RL 營業利益率","value":17.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rl_fcf_margin_pct","label":"RL FCF 利潤率","value":16.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tpr_gross_margin_pct","label":"TPR 毛利率","value":78.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tpr_operating_margin_pct","label":"TPR 營業利益率","value":24.53,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tpr_fcf_margin_pct","label":"TPR FCF 利潤率","value":22.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pvh_gross_margin_pct","label":"PVH 毛利率","value":58.78,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PVH.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pvh_operating_margin_pct","label":"PVH 營業利益率","value":8.05,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PVH.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pvh_fcf_margin_pct","label":"PVH FCF 利潤率","value":8.01,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PVH.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_levi_gross_margin_pct","label":"LEVI 毛利率","value":62.81,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEVI.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_levi_operating_margin_pct","label":"LEVI 營業利益率","value":11.75,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEVI.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_levi_fcf_margin_pct","label":"LEVI FCF 利潤率","value":9.63,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEVI.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cpri_gross_margin_pct","label":"CPRI 毛利率","value":63.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CPRI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cpri_operating_margin_pct","label":"CPRI 營業利益率","value":2.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CPRI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cpri_fcf_margin_pct","label":"CPRI FCF 利潤率","value":5.41,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CPRI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_six_months","label":"SBC (six months)","value":64.3,"period":"Six months FY2027（截至 2026-09-26，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Six months FY2027（截至 2026-09-26，公告於 2026-11-05）","citation":"公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":376.56,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":5.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":47.64,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（18.94 → 18.94）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.9 → 20.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（22.84 → 22.84）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":18.94,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":20.9,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":22.84,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.21,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 18.9 → 18.94（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":21.62,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝85.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":85.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝96.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":96.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.75,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝97.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":97.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.88,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 18.94，分子＝快照價 376.56","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.016,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1181.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 3002.8、現金 1821.8（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":59.1,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":23436.34,"period":"2026-11-08","unit":"USD m","basis":"市值 22255.34 ＋ 淨負債 1181.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":8726.85,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（16 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":9179.85,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.69,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 376.56 / W52 364.61 / W104 312.69 / W250 202.87 / W250 13週斜率 2.24%"},{"id":"f_ma_w52","label":"52 週均線","value":364.61,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":312.69,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":202.87,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.24,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：零售業進入門檻低，新競爭者與產品快速進場，加上數位通路轉移；競爭加劇或應對失敗可能導致市占或銷售下滑（為風險揭露，未指名具體新進入者）。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"In addition, technological advances and the retail industry's low barriers to entry allow for the introduction of new competitors and products at a rapid pace, which has been further compounded by the increasing shift to digital shopping channels. Any increased competition, or our failure to adequately address any of these competitive factors, could result in reduced market share or sales, which could adversely affect our business.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Zacks/Nasdaq 文章討論 RL 品牌升級策略下是否仍在全球取得市占，提及平均單價上升與減少折扣，亞洲與歐洲較明顯。","source":"Nasdaq/Zacks: RL's Brand Elevation Strategy: Is It Still Gaining Share Globally?","url":"https://www.nasdaq.com/articles/rls-brand-elevation-strategy-it-still-gaining-share-globally","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 前三大批發客戶約占總淨營收 11%（約 70% 屬北美、30% 屬歐洲）；占應收帳款毛額約 29%（2026-03-28）。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"Sales to our three largest wholesale customers accounted for approximately 11% of total net revenues for Fiscal 2026, and these customers accounted for approximately 29% of our total gross trade accounts receivable outstanding as of March 28, 2026.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-K 附註稱批發信用風險因客戶數多、地域分散而相對有限，授信不要求擔保品。","source":"SEC EDGAR 10-K FY2026 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"For the Company's wholesale business, concentration of credit risk is relatively limited due to the large number of customers and their dispersion across many geographic areas.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"RL FY27 Q1 營收成長14%，全年固定匯率營收成長指引上調至約5-6%；DTC 平均單價漲15%、促銷減少；中國成長逾40%；歐洲受地緣與觀光疲弱影響偏謹慎；北美批發部分為一次性出貨。","source":"FashionUnited: Ralph Lauren lifts FY27 guidance, China grows more than 40 percent","url":"https://fashionunited.com/news/business/ralph-lauren-lifts-fy27-guidance-china-grows-more-than-40-percent/2026080673963","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"亞洲製衣/紡織上游庫存與產能過剩：孟加拉紡織產能約320-330萬噸對消費約180萬噸（稼動約55%），西方服飾需求疲軟5-10%（Fibre2Fashion 2026-03-31，經搜尋摘要轉述，未核原文）。","source":"Fibre2Fashion via business-humanrights.org: asia tariff uncertaintly causing excess unsold stock","url":"https://www.business-humanrights.org/zh-hant/最新消息/asia-tariff-uncertaintly-causing-excess-unsold-stock/","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"USFIA 2026 調查：85%受訪者稱關稅損害財務表現（2025為78%）；僅約10%增加美國製造採購；越南、孟加拉、印尼、印度、柬埔寨占美國服飾進口50.6%（疫情前37.1%）；美國紡織稼動率低於75%。","source":"Textalks: US apparel tariffs raise costs but deliver little reshoring, USFIA survey finds","url":"https://textalks.com/?p=85059","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"McKinsey State of Fashion 2026 預測2026年全球時尚業僅低個位數成長、總體環境波動；未找到2027-2028 McKinsey預測。","source":"Tribune India: Fashion industry braces for challenging 2026 as global pressures intensify – McKinsey","url":"https://www.tribuneindia.com/news/business/fashion-industry-braces-for-challenging-2026-as-global-pressures-intensify-mckinsey","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K Item 3：公司稱目前未決事項不會對合併財報造成重大不利影響；訴訟類別列舉未含反壟斷。Q4 FY2026 與 Visa／Mastercard 信用卡交換費訴訟和解（RL 為原告），收到淨額 $24.2 百萬並捐出。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"We believe at present that the resolution of currently pending matters will not individually or in the aggregate have a material adverse effect on our consolidated financial statements.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K Item 1：產品受 FTC、海關、CPSC 等機構的品質／安全／標示監管；公司稱實質合規，不知有可能造成重大不利影響的違規。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"We believe that we are in substantial compliance with these regulations, as well as applicable federal, state, local, and foreign rules and regulations.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"約96%產品在美國境外生產，越南約21%、柬埔寨16%、印度11%；關稅或貿易限制重大變動可能使產品成本顯著上升，且不保證能以提價或供應鏈調整抵銷。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"As approximately 96% of our products are currently produced outside of the U.S., any material change in tariffs or other trade restrictions could result in a significant increase to our product costs.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026年2月美國最高法院廢止IEEPA關稅，政府改以其他貿易法授權新關稅；3月CIT命令退還已徵IEEPA關稅，4月CBP公布退款流程，公司不保證能取得退款。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"In February 2026, the U.S. Supreme Court invalidated the IEEPA tariffs previously applied to our imports, after which the current administration announced a new round of tariffs under an alternative U.S. Trade Act authority.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"公司稱已分散供應鏈地理，並可透過庫存管理、供應商降價、變更原產國與定價緩解關稅成本，但關稅大幅上升時獲利仍會受衝擊。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"However, our profitability will be negatively impacted should tariffs increase significantly across our supply chain.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"第一手文件列示UFLPA與CAATSA等進口禁令法規為公司合規風險；經查搜尋，2026年未見RL被列入出口管制實體清單或中國貿易限制的報導。","source":"SEC EDGAR 10-K FY2026 Item 1A；WebSearch 結果","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"including, but not limited to, trade, product labeling, and product safety restrictions, as well as forced labor regulations such as the Uyghur Forced Labor Prevention Act (\"UFLPA\") and the Countering America's Adversaries Through Sanctions Act (\"CAATSA\")","as_of":"2026-05-21","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY27指引假設上半年關稅率較低、下半年在現行減免期結束後關稅逆風較上半年增加（假設稅率升至10%以上），且指引未計入任何關稅退款。","source":"just-style，Ralph Lauren Q1 FY27（搜尋摘要）","url":"https://www.just-style.com/newsletters/ralph-lauren-q1-fy27","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2026 10-K：無自有工廠，約300家供應商，單一供應商占比不超過5%；越南約21%、柬埔寨約16%、印度約11%，靠分散國家與供應商及優惠關稅國家管理風險","source":"Ralph Lauren Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001037038/000162828026037074/rl-20260328.htm","excerpt":"specifications through arrangements with approximately 300 foreign manufacturers in various countries. In Fiscal 2026, the vast majority of our products (by dollar value) were produced outside of the U.S., primarily in Asia, Europe, and Latin America, with approximately 21% of our products sourced from Vietnam, 16% from Cambodia, and 11% from India.","as_of":"2026-05-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"RL 2027財年Q2：北美營收+6%至$885M、歐洲+1%至$696M（固定匯率+3%）、亞洲+28%至$571M（固定匯率+28%）","source":"Ralph Lauren Q2 FY2027 press release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm","excerpt":"North America revenue in the second quarter increased 6% to $885 million on a reported basis.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 FY2027 DTC網絡AUR +9%，高於預期，歸因於全價銷售與地區/通路組合","source":"Ralph Lauren Q2 FY2027 press release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm","excerpt":"Increased AUR by 9% across our direct-to-consumer network in the second quarter, above expectations","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2027全年固定匯率營收成長指引上調至約6%~7%","source":"Ralph Lauren Q2 FY2027 press release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm","excerpt":"now centered around 6% to 7%","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Q1 FY27：全年北美預期低個位數成長；歐洲對EMEA消費需求持審慎觀點，含能源價格與美國關稅逆風；中國成長逾40%","source":"FashionUnited / Retail Dive","url":"https://www.retaildive.com/news/ralph-lauren-winning-streak-q1-north-america-china/827312/","excerpt":"Picicci said the company’s outlook “maintains a prudent view of consumer demand in EMEA,” and includes the expectation of certain headwinds resulting from energy pricing changes and U.S. tariffs. “By region for fiscal 2027, we still expect North America revenue to grow approximately low single digits,” Picicci told analysts.","as_of":"2026-08-07","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子指出技術進步與零售業低進入門檻使新競爭者與新產品快速出現","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001037038/000162828026037074/rl-20260328.htm","excerpt":"In addition, technological advances and the retail industry's low barriers to entry allow for the introduction of new competitors and products at a rapid pace, which has been further compounded by the increasing shift to digital shopping channels.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K：RL 描述自身為零售、批發、授權三通路並行的多通路組合；批發仍服務約 110 家第三方數位夥伴（主要在歐洲），傳統批發客戶的官網銷售也在增加。未見訂閱化或平台化的商業模式轉變描述。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"In addition to our conventional wholesale doors, our products are increasingly being sold through the websites of many of our traditional wholesale customers, as well as those of our third-party digital partners. As of March 28, 2026, our wholesale business served approximately 110 third-party digital partners, primarily in Europe.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 載明公司以地理與通路（零售、批發、授權）分散經營，表示營運結果不單靠單一通路。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"We diversify our business by geography (North America, Europe, and Asia, among other regions) and channel of distribution (retail, wholesale, and licensing). This allows us to maintain a dynamic balance as our operating results do not depend solely on the performance of any single geographic area or channel of distribution.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 FY27（11/5 公布）營收 $2.193B，年增 9%（固定匯率 10%）；全年固定匯率營收成長指引由 5–6% 再上調至 6–7%，營業利益率擴張約 60–80bps；Q3 指引營收 +3–4%、利益率 +50–70bps。調整後 EPS $4.64，對照公布前 Chartmill 共識 EPS $4.35、營收 $2.178B。","source":"modaes / Teleborsa / Chartmill（搜尋摘要）","url":"https://www.modaes.com/global/companies/ralph-lauren-grows-9-in-the-second-quarter-profits-soar-and-pressure-mounts","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 FY27 調整後 EPS $4.59 高於共識 $4.24；5 月原指引為中個位數營收成長與 40–60bps 利益率擴張，Q1 後上調為 5–6% 與 60–80bps。FY27 EPS 共識各站不一：Barchart $18.12、$18.33，Chartmill $19.48（24 位分析師，2026-10-18）。","source":"Barchart / Chartmill（搜尋摘要）","url":"https://www.chartmill.com/stock/quote/RL/estimates","excerpt":null,"as_of":"2026-10-18","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價共識分布：StockAnalysis 2026-04-13 為 16 位分析師、Strong Buy、均價 $403.87；MarketBeat 共識 $430.79（Moderate Buy）；Barchart 19 位分析師均價 $430.12（14 Strong Buy、2 Moderate Buy、3 Hold，未標日期）；TipRanks 15 位 $352.93。各站 as-of 與方法不一，未取得最新單一分布。","source":"StockAnalysis / MarketBeat / Barchart / TipRanks（搜尋摘要）","url":"https://stockanalysis.com/stocks/rl/forecast/","excerpt":null,"as_of":"2026-04-13","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 7 份 8-K 中，含重大項目（1.01/1.02/1.03/2.01/2.05/2.06/3.01/4.02/5.01/8.01）者 0 份，無併購、重編（4.02）事件。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001037038&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"FY2026 Q4 公司作為原告與 Visa、Mastercard 等就信用卡交換費訴訟達成和解，收到淨額 $24.2M，全數捐予 Ralph Lauren Corporate Foundation；10-K 稱待決事項預期無重大不利影響。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"During the fourth quarter of Fiscal 2026, we entered into settlement agreements with Visa, Inc., Mastercard Incorporated, and other named parties to resolve credit card interchange fee litigation matters in which we were a plaintiff. As a result of these settlements, we received $24.2 million of cash proceeds, net of legal fees, which were recognized as gains during the fourth quarter of Fiscal 2026.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Kaskela Law 於 2026 年 4 月公告對 Ralph Lauren 股東調查（潛在證券法／受託責任違反），僅為律所徵案，搜尋未見已提起的證券集體訴訟。","source":"AccessNewswire：Kaskela Law Firm Announces Stockholder Investigation of Ralph Lauren","url":"https://www.accessnewswire.com/newsroom/en/business-and-professional-services/kaskela-law-firm-announces-stockholder-investigation-of-ralph-la-1160476","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月 7 份 8-K 無併購相關重大項目（1.01/2.01 等）0 份。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001037038&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K 稱待決訴訟預期不會個別或合計對合併財報造成重大不利影響；FY2026 Q4 僅有公司作為原告的交換費訴訟和解收入 $24.2M。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm","excerpt":"We believe at present that the resolution of currently pending matters will not individually or in the aggregate have a material adverse effect on our consolidated financial statements.","as_of":"2026-05-21","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"Kaskela Law 2026 年 4 月公告股東調查，僅為律所徵案，未見已提起證券集體訴訟。","source":"AccessNewswire：Kaskela Law Firm Announces Stockholder Investigation of Ralph Lauren","url":"https://www.accessnewswire.com/newsroom/en/business-and-professional-services/kaskela-law-firm-announces-stockholder-investigation-of-ralph-la-1160476","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 無 Item 4.02（非可靠財報）等重大項目；搜尋亦未見近期 SEC 調查或重編。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001037038&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"RL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.0,"operating_margin_pct":17.16,"fcf_margin_pct":16.43,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TPR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":78.31,"operating_margin_pct":24.53,"fcf_margin_pct":22.95,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PVH","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":58.78,"operating_margin_pct":8.05,"fcf_margin_pct":8.01,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PVH","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"LEVI","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":62.81,"operating_margin_pct":11.75,"fcf_margin_pct":9.63,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEVI","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CPRI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":63.28,"operating_margin_pct":2.74,"fcf_margin_pct":5.41,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CPRI","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"RL"},"financial_history":{"ticker":"RL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-03-31","revenue":6443600000.0,"revenue_yoy_pct":null,"gross_margin_pct":64.65,"operating_margin_pct":11.75,"net_income":522700000.0,"diluted_eps":7.58,"free_cash_flow":193500000.0,"fcf_margin_pct":3.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-03-31","revenue":6631400000.0,"revenue_yoy_pct":2.91,"gross_margin_pct":66.83,"operating_margin_pct":12.54,"net_income":646300000.0,"diluted_eps":9.71,"free_cash_flow":904900000.0,"fcf_margin_pct":13.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-03-31","revenue":7079000000.0,"revenue_yoy_pct":6.75,"gross_margin_pct":68.55,"operating_margin_pct":13.98,"net_income":742900000.0,"diluted_eps":11.61,"free_cash_flow":1018900000.0,"fcf_margin_pct":14.39,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-03-31","revenue":8114500000.0,"revenue_yoy_pct":14.63,"gross_margin_pct":69.87,"operating_margin_pct":15.99,"net_income":941100000.0,"diluted_eps":15.11,"free_cash_flow":704900000.0,"fcf_margin_pct":8.69,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/RL/RL_Q2_2027_Earnings_Call_20261105.md）

# Q2 2027 Earnings Call
**Ralph Lauren Corporation** | Earnings Calls | 2026-11-05

**Corinna Van Ghinst** (Executives):
[Audio Gap] With me today are Patrice Louvet, the company's President and Chief Executive Officer; and Justin Picicci, Chief Financial Officer. After prepared remarks, we will open up the call for your questions, which we ask that you limit to one per caller.
During today's call, our financial performance will be discussed on a constant currency adjusted basis. Our reported results, including foreign currency, can be found in this morning's press release. We will also be making some forward-looking statements within the meaning of the federal securities laws, including our financial outlook. Forward-looking statements are not guarantees, and our actual results may differ materially from those expressed or implied in the forward-looking statements. 
Our expectations contain many risks and uncertainties. Principal risks and uncertainties that could cause our results to differ materially from our current expectations are detailed in our SEC filings. To find disclosures and reconciliations of non-GAAP measures that we use when discussing our financial results, you should refer to this morning's earnings release and to our SEC filings that can be found on our Investor Relations website. 
With that, I will turn the call over to Patrice.

**Patrice Louvet** (Executives):
Thank you, Corey. Good morning, everyone, and thank you for joining today's call. We delivered another strong quarter of progress on our Next Great Chapter: Drive plan. In a consumer landscape often shaped by ever-changing trends, the clarity of Ralph Lauren's values and purpose of inspiring the dream of a better life through authenticity and timeless style continues to set us apart. We stay true to who we are, and we have a proven ability to evolve with today's consumer. This is a powerful competitive advantage, and it is translating into sustained broad-based momentum and a resilient core consumer with significant opportunities ahead.
In the second quarter, our top and bottom line results exceeded our expectations, enabling us to take up our full year guidance once again. This performance reflects our momentum across markets, channels and categories. Revenues increased 10%, led by double-digit growth in Asia. Our retail channels also grew low double digits with similar comp growth across stores and digital, while wholesale increased at a solid mid-single-digit rate.
Our ongoing investments behind our brand, products and lifestyle experiences enabled us to stay on offense and continue our long-term elevation journey with further improvement in quality of sales and full price selling. At the same time, we continue to invest in our long-term capabilities such as talent and technology while accelerating cash returns to shareholders through our durable dividend and repurchases. This balance of investment and shareholder returns reflects the power of the Ralph Lauren model. Our strong balance sheet, cash flows and culture of operating discipline give us the flexibility to navigate a complex global backdrop while fueling future growth opportunities.
Underpinning this model, is a combination only Ralph Lauren can bring together. Authentic lifestyle authority, cultural relevance and timeless brand codes at global scale. We are building on this distinctive advantage through the 3 strategic pillars of our plan, which, as a reminder, include: first, elevate and energize our lifestyle brand; second, drive the core and expand for more; and third, win in key cities with our consumer ecosystem. Starting with our efforts to elevate and energize our lifestyle brand.
Through our rolling thunder of activations, we are engaging with consumers across the many facets of their lives from the inspiration of the runway to the biggest stages in sports, entertainment and more. This enables us to deepen our connection with existing consumers around the world as we build lifetime value while also inspiring a new generation with our cinematic storytelling and core values of optimism, quality and authenticity. Key highlights from the quarter included: first, we continue to strengthen our position as one of the world's leading luxury lifestyle brands in sports, elevating traditionally local events into globally relevant, exciting brand moments.
At Wimbledon, we combined the heritage and elegance of the tournament with Ralph Lauren's spectator style. We activated across our top cities around the world from our Sloane Square takeover in London to our Tokyo live Viewing Party and Douyin Live shopping event in Hong Kong and our Legends tennis exhibition match in New York Central Park with Andre Agassi, Caroline Wozniacki, Genie Bouchard and James Blake. At the U.S. Open, we built on our long-standing partnership with an expanded 360-degree campaign, including our vintage-inspired collection, specialty pop-ups and influencer activations. 
And at the Goodwood Revival in the U.K., we brought our sophistication to the classic motorsports event for the fourth year, including a preview of our Polo Bar experience ahead of our London restaurant opening slated for 2028. Together, these sports lifestyle campaigns allow us to showcase the breadth of the Ralph Lauren lifestyle while bringing consumers closer to the brand. They generated a combined 70 billion global impressions and more than $350 million in media value. 
Next, we immerse consumers in our vision of timeless style through our Spring '27 Women's Collection fashion show in New York City, along with key celebrity dressing moments, including BTS at their Arirang World Tour at MetLife Stadium and at our Very Ralph documentary premiere in Seoul. And beyond the quarter, we recently hosted our first-ever Polo Fest in Tokyo, bringing Polo collectors, brand enthusiasts and cultural voices together for a 3-day experience as part of our year-long celebration of 50 years in Japan. These activations are driving strong, sustainable growth in new customer acquisition and retention. 
In the second quarter, we added 1.7 million new customers to our DTC businesses, led by Ralph Lauren stores. We continue to drive progress across brand equity metrics, including increased awareness, purchase intent and net promoter score. We're also driving higher lifetime value and recruiting key consumer cohorts led once again by women, luxury and younger customers. And we increased our social media followers by mid-single digits to more than 72 million led by Instagram, LINE and Douyin with a focus on our Summer of Sports and fashion show. This diversity of activations enables us to keep the brand fresh and relevant across each of our key markets, staying true to Ralph's vision while finding new ways to bring each generation into our world. And this brand momentum is translating directly into increasing desirability and demand for our products. This takes me to our second key initiative, drive the core and expand for more. 
Ralph's vision has always been about a way of living. This quarter, our talented creative teams brought that vision to life through our enduring icons combined with seasonal newness across men's, women's and children's. By reinforcing the core, while expanding our lifestyle proposition, we are creating multiple avenues for durable growth and bringing our products to life through increasingly connected consumer ecosystems. 
Starting with our core, which represents more than 70% of our business. Core product sales grew 10% in the second quarter. Recent highlights include our cotton cable and Merino-blend sweaters, linen poplin and oxford-dyed shirts, icon Chino caps, sport coats and fleece. For the fall '26 season, our Litchfield and Red Rock collections from men's Polo resonated particularly well with consumers. In children's, we delivered a successful back-to-school with our collegiate-inspired NextGen and New England-themed Middlebury collections with strength across our sweaters, core mesh polos, sweat dresses and expanded outerwear proposition.
Our high potential categories, including women's apparel, outerwear and handbags, grew low double digits for the quarter, ahead of total company growth. In women's, we drove excitement through our new micro-cable collared cardigan and wool rugby sweaters, corduroy shirts and Polo shirt dresses. Our strong outerwear performance was driven by our lightweight Bi-Swing and Bayport cotton windbreakers for men and Icon windbreakers and barn jackets for women. And in handbags, we officially launched Polo Blaze, our most elevated foundational collection for Polo to date, marrying equestrian-inspired details with a downtown edge.
Special releases this quarter included our U.S. Open collection inspired by the heritage of tennis and the spirits of New York, delivering our strongest sell-throughs around the event to date and our collaborations with Gee's Bend and second capsule drop with TÓPA, both part of our groundbreaking Artist in Residence series, focused on empowering and celebrating artisans within the communities that have historically inspired our designs. As we turn to holiday, we will continue to invite consumers to step into the cinematic worlds that Ralph created with timeless, high-quality products, a compelling value proposition and styling that only we can deliver.
Turning to our third key initiative, Win in Key Cities with Our Consumer Ecosystem. We are creating unique lifestyle experiences to immerse consumers in the world of Ralph Lauren, bringing together product, hospitality and storytelling in our top 30 cities around the world while also laying the groundwork for long-term growth in our next 20 cities. Within DTC, which comprises the majority of our business, global comps increased 10%, led once again by our Ralph Lauren stores and digital commerce.
By region, Asia increased 28%, driven by 24% comps and growth across all key markets. China sales remained strong, increasing more than 35%, while Japan and Korea were also up double digits as we continue to invest behind localized brand activations and experiences. Europe delivered low single-digit growth this quarter, in line with our plan despite industry traffic headwinds and on top of last year's strong compares. And we drove another quarter of strong results ahead of expectations in our largest region, North America, with healthy demand in both our retail and wholesale channels.
With regards to our store base, we opened 22 new owned and partner stores globally this quarter as we deepened our presence in our top cities. Highlights included Seaport in Boston, including our first Ralph's Coffee location in Massachusetts, new men's and women's stand-alone stores in London's Sloane Square; St. Tropez, France; Beijing, Hopson One, and Galaxy Promenade in Macau. On the digital front, we expanded our RL mobile app to Japan following our successful launch in Korea earlier this year with early sales performance and downloads exceeding our expectations. We also grew our connected retail and clienteling capabilities across several markets in Asia this quarter, enabling our teams to serve consumers with greater personalization and consistency.
And finally, touching on our enablers. Our business continues to be supported by our 5 key enablers. Recent highlights include: first, as part of our focus on advanced technology, AI and analytics, we are investing in new capabilities that help our teams move faster, create more personalized consumer experiences and operate with greater precision. In addition to expanding our mobile app and clienteling in Asia this quarter, we continued our journey to enhance visibility on key LLMs. We also launched a test on WhatsApp Concierge, a digital assistant that allows customers to interact directly with our brand on the WhatsApp platform. And following our initial test with OpenAI earlier this year, we are further scaling advertising on the platform for holiday gifting and cultural moments. 
In addition, we are advancing our commitment to the communities we serve. We recently announced a new partnership with the Korea National Cancer Center Foundation to establish a new Ralph Lauren Cancer Center in Goyang, our first in Asia and fifth globally, part of our broader long-standing commitment to more equitable access to cancer care. And we were proud to be recently named one of the World's Best Employers by Forbes, reflecting the power of the people and culture that make Ralph Lauren so special. 
In closing, Ralph and I are encouraged by our team's progress in the second year of our Next Great Chapter: Drive plan in the midst of an ever-evolving global operating landscape. As we head into the important holiday season, our consumer remains at the center of everything we do. With that in mind, we will continue to lean into our long-term elevation journey, investing in our strategic priorities to deliver sustainable growth and value creation into the future, including developing innovative campaigns that build desirability and engagement, and grow lifetime value, creating timeless high-quality products that offer compelling value and earn consumers' trust and winning in our top cities through unique brand experiences that immerse consumers in the world of Ralph Lauren.
These diversified engines of growth and our increasingly elevated consumer base all underpinned by our iconic brand, continue to drive resilience in our business model and consistency in our performance. 
With that, I'll hand it over to Justin, and I'll join him at the end to answer your questions.

**Justin Picicci** (Executives):
Thanks, Patrice, and good morning, everyone. Our second quarter performance underscores our growing brand desirability around the world with results exceeding our expectations across both revenue and profitability. This reflects broad-based consumer demand and the strength of our diversified growth model against a dynamic operating backdrop. Revenues increased 10%, ahead of our mid-single-digit outlook for the quarter with growth across every region. Our branded products continue to resonate with consumers globally and full price momentum supported gross and operating margin expansion above expectations. 
Notably, we delivered this performance while continuing to invest in the strategic initiatives that will fuel sustainable long-term growth and value creation. This combination of second quarter outperformance and sustained brand momentum gives us confidence to raise our full year outlook once again. But first, let me walk you through our financial highlights from the second quarter, which, as a reminder, are provided on a constant currency adjusted basis. 
Total company second quarter revenue grew 10%, driven by better-than-expected performance in both our direct-to-consumer and wholesale channels. By region, Asia led our performance, increasing 28%, followed by North America, up 6% and Europe, up 3%. Total company retail comps also increased 10%, with growth across both our own digital and brick-and-mortar channels. Total company adjusted gross margin expanded 220 basis points to 70.2%, ahead of our outlook. The increase was driven by AUR growth, favorable geographic mix and lower product costs, which more than offset modest pressure from higher labor and non-cotton material costs in the quarter. AUR increased 9%, ahead of our plan and on top of 12% growth last year. The increase was broad-based and reflected balanced contributions from product elevation, favorable channel and geographic mix, and selective pricing actions and lower promotional activity. 
For the third quarter, we are currently planning for mid-single-digit AUR growth on top of last holiday's exceptionally strong 18% increase. Our outlook continues to be supported by our ongoing brand elevation strategy with the flexibility to further reduce discounting based on consumer demand and selling trends. Adjusted operating expenses increased 11% or 70 basis points as a percentage of sales compared to last year as higher marketing more than offset leverage in non-marketing expenses. Marketing increased to 8.6% of sales, up from 7.8% last year, reflecting increased investments to amplify key campaigns, including our New York fashion show and sponsorships of Wimbledon and the U.S. Open. 
Our multiyear progress in sustained new customer acquisition, healthy consumer metrics and attractive returns reinforces our confidence to continue expanding our marketing programs across our top cities. We now expect marketing investment to represent approximately 8% to 8.5% of sales in fiscal '27 compared to approximately 8% previously. Even with this higher investment, second quarter adjusted operating margin expanded 140 basis points to 15.5%, ahead of our plan, while operating income grew 21%. This underscores our ability to expand profitability while continuing to make investments in our brand and capabilities that support durable growth.
Turning to segment performance, and starting with North America. Second quarter revenue grew 6% at the high end of our expectations. In North America retail, second quarter comps increased 6% on top of a double-digit compare last year with balanced growth across our digital and brick-and-mortar channels. Digital comps increased 5%, supported by solid traffic, full funnel marketing activations and continued merchandising optimization. North America wholesale revenue grew 8%, driven by healthy replenishment and seasonal orders. Results included approximately 4 points of benefit from planned timing shifts from the second half of the year.
We continue to expect North America wholesale performance to moderate in the second half as we lap these timing benefits and accelerate our strategic reduction of off-price sales and lower-tier full-price stores. Our underlying growth in the channel remains healthy with strong full-price sellout trends and continued market share gains. 
Turning to Europe. Second quarter revenue increased 3%, modestly ahead of our expectations. Europe wholesale increased 4% on top of double-digit growth last year. Underlying sell-out trends remain in line with our full year outlook, and we continue to proactively manage our sell-in to align with consumer demand and maintain healthy inventories in the channel. Europe retail comps declined 1% as we lapped an exceptionally strong 10% compare last year amid a challenging macro environment. While the region continues to face pressure from weaker store traffic across several of our key markets, we are taking targeted strategic actions to drive stronger consumer engagement, increased conversion and higher basket sizes in our stores. 
Looking ahead to the second half of the year, we continue to invest behind our strongest brand and consumer opportunities in the region, including marketing activations and targeted consumer engagement, building on our growing brand desirability to support both near- and long-term growth. 
Moving to Asia. Second quarter revenue increased 28%, reflecting broad-based growth across all key markets. Retail comps grew 24% with double-digit growth across every channel. Our Asia digital ecosystem also delivered double-digit growth with strong contributions from our own digital commerce sites. By market, China continued to lead our performance with sales up more than 35% in the quarter, driven by healthy comps and high-quality new customer recruitment. Japan and Korea also delivered strong double-digit growth, supported by localized brand activations and sustained consumer engagement. Our full funnel marketing activations throughout the region are building deeper connections with consumers, and we continue to see substantial opportunity to build awareness, deepen engagement and expand our presence across key markets where our luxury lifestyle positioning continues to resonate. 
Moving to the balance sheet. Our fortress balance sheet and strong cash flow generation continue to provide meaningful strategic flexibility, enabling us to invest through periods of volatility, pursue compelling growth opportunities and return capital to our shareholders, all while maintaining prudent financial discipline. During the second quarter, we repurchased approximately $250 million in shares, bringing our year-to-date repurchases to $500 million and completing our buyback plans for fiscal '27. And we remain on track to return over $2 billion to shareholders, including through dividends and repurchases over our 3-year Drive plan. We ended the period with $1.8 billion in cash and short-term investments and $1.2 billion in total debt. 
We continue to manage inventories closely against demand in each of our regions. Second quarter net inventory decreased 8% in constant currency, reflecting last year's elevated tariff-related inventory base. Excluding the impact of tariffs, net inventory declined approximately 2%. As we enter the holiday season, our inventories remain healthy, current and well positioned to support demand across geographies and channels while preserving flexibility. 
Looking ahead, our outlook for fiscal '27 remains based on our best current assessment of the operating environment, including the geopolitical backdrop, foreign currency dynamics and broader macroeconomic conditions. For fiscal '27, we now expect constant currency revenue growth of mid- to high single digits on a 52-week comparable basis, centered around 6% to 7%, up from our prior outlook of 5% to 6%. This increase largely reflects our better-than-expected second quarter results, along with a modestly stronger outlook for the second half, supported by our continued brand momentum.
As previously discussed, we continue to expect first half growth to be stronger than second half growth, reflecting the timing of this year's marketing activations and other investments, the timing of planned wholesale shipment shifts and strategic off-price reductions, and more challenging year-over-year comparisons in certain of our key markets. Importantly, our outlook continues to assume healthy underlying growth in the second half, in line with our long-term plan. Foreign currency is now expected to negatively impact revenue growth by approximately 40 to 60 basis points this year based on current exchange rates.
As a reminder, fiscal '27 includes a 53rd week, which is expected to add approximately 1 point to revenue growth and slightly benefit operating margin. By region for fiscal '27, we now expect North America revenue to grow approximately low to mid-single digits, up from low single digits previously. We are encouraged by our strong first half performance in the region and the continued momentum across our direct-to-consumer and full-price wholesale channels. We still expect this solid underlying growth to be partly offset by accelerated strategic actions to improve quality of sales and exit lower-tier doors, notably in the back half of the year as we further elevate and strengthen our long-term position in the marketplace.
We now expect Europe revenue to grow approximately low single digits compared to low to mid-single digits previously. This outlook reflects positive underlying growth, partly offset by increased pressure on consumer traffic and broader macroeconomic volatility in the second half of the year. We remain focused on driving high-quality near-term results while continuing to invest behind long-term brand elevation and margin expansion. And we now expect Asia revenue to increase low teens, up from our prior outlook of high single to low double digits, driven by our stronger-than-expected first half results, along with ongoing brand momentum across our key markets in the region. 
We now expect full year operating margin to expand approximately 80 to 100 basis points in constant currency, up from our prior guidance of 60 to 80 basis points, largely driven by our better-than-expected second quarter results. We are also raising our full year gross margin outlook to approximately 80 to 100 basis points of expansion compared to our prior guidance of 50 to 70 basis points. This reflects our stronger-than-expected Q2 results, along with our updated view on U.S. tariffs, which assumes the prevailing rate of approximately 10% through December, followed by a return to reciprocal rates in the high teens in our fiscal fourth quarter.
We continue to expect both gross and operating margin expansion to be weighted towards the first half of the fiscal year, reflecting normalizing AUR growth and the timing of key marketing activations as well as our previously disclosed timing shifts in wholesale shipments. Our guidance continues to exclude the benefit of tariff refunds, which are not included in our adjusted non-GAAP results. As part of our long-term capital allocation strategy, related proceeds received will be primarily reinvested in the business as well as directed toward initiatives that strengthen and advance our purpose and values.
Foreign currency is now expected to benefit gross margin by approximately 10 to 30 basis points and have a roughly neutral impact on operating margin in fiscal '27. For the third quarter, we expect constant currency revenue to increase approximately low to mid-single digits, centered around 3% to 4%. This outlook includes approximately 1 point of negative impact from planned wholesale timing shifts and strategic off-price reductions in the quarter with underlying growth of roughly mid-single digits. Foreign currency is expected to negatively impact revenues by approximately 50 to 100 basis points. 
We expect operating margin to expand approximately 50 to 70 basis points in constant currency, with gross margin expansion more than offsetting higher marketing investments in the holiday period. Foreign currency is expected to benefit gross margin by about 20 to 40 basis points and have a roughly neutral to 20 basis point benefit to operating margin in the quarter. We expect our third quarter tax rate to be in the range of 23% to 24%, while the full year tax rate is still expected to be in the range of 21% to 22%. 
In closing, our teams continue to deliver against both our near-term commitments and long-term strategic priorities. This quarter's results demonstrate the strength of our diversified growth model, the benefits of our elevation strategy and the discipline with which we are investing for the future, underscoring the enduring relevance of Ralph's timeless vision around the world. While the external environment remains dynamic, we are focused on what we can control, continuing to drive brand and product desirability, enhancing quality of sales, operating with discipline and investing behind high-return growth opportunities.
Together, these actions position us well to deliver on our fiscal '27 commitments while strengthening the foundation for durable long-term value creation for all of our stakeholders. 
With that, let's open up the call for your questions.

**Operator** (Operator):
[Operator Instructions] The first question comes from Matthew Boss with JPMorgan.

**Matthew Boss** (Analysts):
Congrats on another nice quarter. So, Patrice, what does your updated fiscal '27 outlook assume for the health of your consumer in each region? Is the global operating environment getting tougher in your view? Or just any puts and takes? And then, Justin, could you elaborate on the progression of demand trends that you saw in North America during the second quarter and just drivers underlying your full year raise for top line growth in that region?

**Patrice Louvet** (Executives):
All right. Matt, thanks for your question. So, I would call out a few points. First of all, looking collectively across regions, our brand is strong and is getting stronger. And we're investing for the long term, and we're well on track toward our 3-year targets. We're actually halfway through our Next Great Chapter: Drive phase and progressing really nicely. Now we're certainly in an environment with a lot of macro noise, and I think macro noise is a new phenomenon for this industry, but just good enough right now, including our updated views on Europe, we have successfully, as a company, navigated through a variety of macro environments over the past many years, and we are well positioned looking ahead. And as you saw, we were able to take up this year's outlook once again. 
Now, specifically on the consumer, as you know, we're in an exciting elevation journey with our customer base around the world, right? We've shifted our customer base to focus on higher quality of sales, lower price sensitivity, larger basket size and younger cohorts. And today, our core consumer remains resilient across each of our key markets globally. Zooming out, our growth and value creation model is durable, in part because we have this diversity of drivers. Our brand is stronger than ever in every region with a record level of affinity scores. You heard us say earlier, we're seeing that across the regions.
We have a culture of agility and operational discipline built over years, and we have a lot of opportunity yet to build the brand in large markets like China, Korea, Germany, even in North America, where I would argue we're actually in the very early innings of our elevated journey in North America with significant growth opportunities ahead around the region, particularly in the West Coast now that we've established healthy foundations across the entire business model.
So, regardless of the macro, we're running our play. We've got an eye on the long term because we want to make sure we're continuing to build this brand in the right way for long-term success. Because we have both the diversity of growth drivers and the flexibility to pivot and take advantage of clear opportunities for Ralph Lauren in the marketplace, that's where our confidence comes moving forward. And I would call out that we're continuing to invest behind our iconic brand and reinforce our place in culture. You've heard us talk about the recent Polo Fest event, which I think is a beautiful illustration of how the Ralph Lauren brand has been weaved into the culture globally. 
We're creating timeless core products that resonate across generations, Gen Zs, but also the silver generation and across geographies. And we're offering lifestyle experiences that consumers want to be part of, and we see that every single day, including the lines at our coffee shops. So, to summarize, I would say we remain on offense. We're taking market share across markets. We're building our brand equities and healthy foundations for the long term. And we have significant runway ahead for our unique lifestyle proposition.

**Justin Picicci** (Executives):
And, Matt, the question on North America, as you mentioned, we took up our full year outlook for North America from low single digits to low to mid-single digits, and we're really encouraged by the broad-based momentum we have in that region across the whole ecosystem. Our core consumers are performing really, really well. We're seeing that ongoing shift towards a more elevated positioning really, really drive our business across channels, especially, I would say, full-price channels. And, Q2, you saw another balanced healthy growth delivery across DTC and wholesale.
As we think about sort of going forward into Q3, we're really expecting that continued momentum, both in DTC and really in that healthy full price wholesale sellout to continue partly offset by those deliberate accelerated quality of sales, investments and lower-tier door exits that we've talked about. So, when you think about the underlying trend for the region, it really continues to be on that mid-single-digit trajectory, and we're really encouraged by that brand momentum continuing.

**Operator** (Operator):
The next question comes from Jay Sole with UBS.

**Jay Sole** (Analysts):
Justin, what catalysts or metrics are you looking at to get more constructive on Europe? And for the overall business, can you also provide any color around recent performance and quarter-to-date trends? And how should we think about the implied deceleration in your second half guide? And if you can also add some color on a little bit more specificity on how you see gross margin playing out in Q3 and Q4, that would be great.
And then, Patrice, if I can just ask you one. Justin mentioned that it's great to be able to meet and exceed expectations and still reinvest in the business. I think as marketing gets higher and higher as a percent of sales, I think it was 8.6% this quarter. Do you see -- are you interested in actually taking -- keeping that number where it is and maybe even driving it higher? And can you do that while still maintaining the ROI associated with that spend?

**Justin Picicci** (Executives):
Jay, thanks for the question. Listen, we remain focused on driving high-quality sustainable growth for all 3 of our regions, and that includes Europe. I would say, importantly, for Europe, we continue to track ahead of that 3-year growth algo that we laid out, and we're delivering growth in the second year of our plan. And you heard Patrice talk about, we continue to see meaningful long-term growth opportunities across key markets, categories, channels in that region.
Now, based on what we've seen so far this fiscal year, the trends have generally, I would say, played out as we expected, right, with broader industry traffic pressure remaining the primary headwind. So, when we think about in terms of what would make us more constructive on Europe, traffic, and I would say, particularly in stores, that remains a key metric that we're watching closely. That all said, our updated guidance doesn't assume a meaningful improvement in traffic or in the macro environment.
And against that challenged backdrop, we continue to expect our brands to gain share and for Europe to deliver positive growth this year, and that includes slight growth in Q3. And while the external environment in Europe certainly remains pressured, what we're doing is we're proactively managing our business and focus on the things we can control. Our consumer brand metrics remain strong, including record NPS scores. Our teams are focused on driving conversion, basket size to help offset that near-term traffic pressure. And this is all we continue to invest behind and advance our long-term elevation strategy in the region.
To your second part of your question, what I do is I separate the underlying health of the business from the quarterly cadence. Our outlook remains consistent with the quarterly growth trajectory we planned as we came into the year. I would say with slightly stronger expectations for the second half than we previously anticipated based upon our strong brand momentum. Now, this puts our updated full year outlook for both revenue and profitability ahead of our long-term plans, similar to what we delivered last year in year 1.
The first half of this year reflected stronger top line growth, including favorable timing shifts in the second half as well as higher growth in marketing. As we move to the back half, we'll also begin to lap some exceptionally strong compares in Asia, notably for China, while also executing on those planned strategic pullbacks that I just mentioned in North America off-price wholesale. Now, those factors affect the quarterly cadence, but they don't change our view of the consistent underlying momentum in the business, which remains strong.
As you know, we don't typically comment on monthly or quarter-to-date trends. I would say our third quarter guidance incorporates the recent trends we're seeing in the business as well as our expectations for the key holiday selling periods ahead. So, just stepping back, when you adjust for timing, planned strategic actions, more difficult compares, we continue to expect healthy underlying growth in the second half, firmly in line with our long-term growth plan. 
On the second half gross margin outlook, I would say it continues to be supported by structural durable drivers. You'll see in our AUR, of course, durable drivers behind that. Our geo channel product mix, durable drivers behind that. We do have a tariff assumption in there that has the prevailing rate going back to reciprocal -- kind of, the reciprocal rates, the high teens in the fourth quarter. So, that's in there. We think that's prudent, and we'll see what happens there. But we expect our gross margin to remain healthy, albeit with a little bit of normalization on the AUR front off of a strong double-digit first half performance.

**Patrice Louvet** (Executives):
And on marketing, I would say a few things, Jay. First of all, as a company, we're in the dreams business, we're in the storytelling business. So, marketing is a core element of our business. And I'm actually really excited to see how over the past few years, we've gone from 3% to 4% of our revenue invested in marketing to now north of 8%. There's really no ceiling, right? What's important is that as we want to continue to invest in marketing as long as we get an exciting return, which we have, while expanding operating margin. So, it's not one at the expense of the other. We're always going to do them in tandem.
As we look at the types of activations that we have, right, we have a multifaceted marketing strategy that really focuses on our key consumer targets. We want to talk across generations. We want to talk across genders. We want to talk across communities. And I think our teams have done a fantastic job building a portfolio of marketing activations ranging from sports to fashion presentations to Polo Fest to social media activities that have really helped bring the brand to life in different ways across different cohorts and has been driving our momentum over the past many years.
The strategy is really focused on, one, new consumer acquisition, right, and particularly younger, higher value to higher basket size, more diverse consumers. You saw this quarter, we added another 1.7 million new consumers with fantastic profiles. Our social media followers are up to 72 million now on our way to 100 million. Second is retention rate, which is obviously very important. We have, I believe we can say the most loyal customer in the industry. So, for us, it's about lifetime value, not just one purchase. And we're driving that through increased personalization, increased clienteling and of course, trading across and trading up with leveraging our full lifestyle portfolio.
And then finally, to the ROI point, our teams are doing a fantastic job consistently looking for ways to be more efficient in the way we target, to be more efficient in the way we activate, to focus on the bigger opportunities so that through this journey of 3.5% of revenue to now this last quarter 8.6% of revenue, we all feel very good about the type of return and effectiveness that we see. That's driven by increased digital focus overall. That's driven by increased targeting. That's driven by increased personalization. And you see that across the metrics this last quarter, right? Our awareness is up. Our consideration is up, our purchase intent is up, our advocacy is up. Therefore, the investments that we are making are delivering and are driving the strong momentum and the strong comp performance that we've been talking about. 
As you look at holiday, which is obviously a key important moment for us as a company, very excited about the momentum we have going into holiday. You heard all the activations we had in Q2. We have a number of great things going on in Q3. We had the women's Polo presentation in Paris that got rave reviews. We have the Polo Fest activation in Tokyo. We have a very strong holiday campaign situated in the Adirondacks that we're very energized by. We are starting our investments earlier from a media standpoint. So, we expect higher impact. We launched, I think, ahead of most of our competitive set to really capture the full gifting season with media investment up 23% versus last year, focused on our top 30 city ecosystems. That's the first point. 
Second point is really making gifting an acquisition engine, deploying a fully integrated 360-degree gifting strategy because we are one of the premier brands from a gifting standpoint. We know we have the opportunity to lean into that even more effectively across generations. Third is we're doubling our global holiday experiences. I don't know, Jay, if you got a chance to experience ours in L.A. last year, but we're going from 4 cities last year to 8 cities this year, L.A., London, Paris, Hong Kong, Singapore, Tokyo, Sydney, Seoul. And I suspect when we talk next year, that this will even expand because we've seen very strong response to these experiences. We are at a time with AI and digital and agents where consumers more and more, they want live in-person experiences, and these events really deliver that. 
The fourth element -- sorry, this is long-winded, but I think it's important for all of you and to understand how we're thinking about this moving forward. Fourth element is really amplifying our cultural and social reach, right? We have an incredible network globally of creators, influencers, editorial partners that help us reach new audiences and help us -- will help us drive demand for key holiday categories like outerwear, like cable-knit sweaters, like our handbags across many of the different social media platforms as well as taking advantage of the LLM capabilities and platforms that are coming up and make sure that consumers can discover us on those.
And then the final point is really capitalizing on organic holiday momentum. So, you'll remember last year that Ralph Lauren Christmas was trending. Well, here's the good news. Ralph Lauren Christmas is trending again this year, emerging organically as consumers celebrate and share their love for Ralph Lauren's iconic products, particularly with Bear product and our home collection. So, this gives you a sense of the activations we have going into holiday just for this quarter, right? And as you know, our strategy is to have a rolling thunder of activations that talk to our different cohorts. And so, no, 8.6% is not the ceiling. As long as we get exciting returns, we'll continue to lean in our diversified portfolio of activation while, of course, delivering attractive value and also expanding our operating margin. 
Sorry for the long answer, but hopefully, that gives you a good sense for where we are.

**Operator** (Operator):
The next question comes from Kendall Toscano with Bank of America.

**Kendall Toscano** (Analysts):
I just wanted to see if we could zoom in on Europe a bit more. And so, as we think about that region having been challenged for a few quarters now, it does seem like the store traffic for you guys was incrementally more challenging in the second quarter compared to what you saw in the first quarter. And I know you called out a particularly tough comparison in Europe during the second quarter. But how should we think about as you move into the third quarter, you're lapping a flat comp last year versus a plus 10%. So how should we think about that versus, I think you mentioned you're expecting slight growth for the region in the third quarter? And how do you expect that consumer to behave during holiday?

**Justin Picicci** (Executives):
Sure. Maybe we can tag team this one. Thanks for the question. So, as you pointed out, the change in our EMEA outlook is really the external environment is a bit more challenged than we expected, particularly around retail traffic, consumer confidence and I would say, broader cost of living pressure. So, there's been a sort of prolonged, I would say, traffic softening that was started to ramp up in Q1, really continued into Q2, and that's reflected in our updated fiscal '27 in the outlook of low single-digit growth. And so, yes, we have assumed some, I would say, unit elasticity in the second half given that backdrop, but we're not assuming sort of a broad deterioration across all of the underlying drivers of the business.
In fact, our teams are very focused on what they can control, right? So, think driving product desirability, conversion, basket size, targeted consumer engagement, which is going to help mitigate some of that external pressure. We have a proven playbook of strategies there. But importantly, our updated outlook doesn't contemplate or depend on, I would say, a near-term macro recovery in EMEA. And I also think the broader context here is important because our Q3 outlook for the company, right, is still for that sort of low to mid-single-digit growth, which includes about 1 point of pressure from our wholesale timing and strategic off-price pullbacks.
So, that incorporates actually bit more cautious assumptions for EMEA, while if you think about taking a step back, we're still on that underlying mid-single-digit algo for total company. So we believe we've appropriately reflected the softer Europe consumer and traffic environment in the guide. But at the same time, we're continuing to see opportunities to mitigate those pressures through those strategic actions that I talked about without assuming the environment gets better. The last thing I'll say is we also continue to invest in the region. So in marketing, in new stores, in digital, really to drive long-term growth and continue to strengthen our already strong brand equity. So we're going to protect quality of sales and long-term brand equity. Flexibility doesn't mean walking back our elevation strategy.

**Patrice Louvet** (Executives):
Yes. I would add a couple of things, Kendall. First of all, I mean, we've built a strong business over the past few years in Europe that's really fundamentally well positioned and much more elevated than it was a few years back. So strong base, strong foundation. Second is our brand continues to strengthen. We saw that in our recent equity scores across the region. It's true across generations, particularly true across for the younger generation. So that's actually very promising. As Justin mentioned, we're on offense, right? We're investing more in marketing. You heard some of the comments I made earlier relative to media for Q3.
We're continuing to invest in store openings in London, in the south of France and others. So clearly on offense. Share data isn't great in this industry from my old -- compared to my old world, but from the share data that we have, we also know that we're growing market share across the business. So this is an important time for us to take advantage of the broader challenges to expand our market share. And I think I mentioned earlier on the consumer, our general consumer is -- our core consumer is resilient, and this is true across the world, and it's true in Europe.
 I think where we're seeing the pressure is traffic, particularly in outlets, right, which typically will be the consumers that will be more pressured by inflationary considerations. They've got to drive all the way to the center, et cetera. But as Justin mentioned, we want to be cautious in terms of just recognizing the macro traffic headwind reality. But certainly, from a mindset and strategy and investment, we remain clearly on offense in Europe.

**Operator** (Operator):
The next question comes from Michael Binetti with Evercore ISI.

**Michael Binetti** (Analysts):
I guess just a quick one, Justin, do the initiatives you mentioned to engage with consumers in Europe, drive conversion and basket, does that include promotions? Is that a lever you expect to pull in the holiday to -- while the traffic is tough there? And then I guess on gross margins, if you wouldn't mind breaking down the drivers a little more quantitatively for us, the expansion, I know you mentioned the drivers for AUR growth, geo mix, product costs. AUR slowed a little bit from the first quarter, not much. I don't think the geo mix was vastly different from first quarter. So I'm just -- maybe a little bit of help on the breakdown of the 250 basis points would be great.
And then I guess just a longer-term question, jump ball, you're tracking to the 17% operating margin for the year. And I think the Analyst Day last year, you contemplated the building to something closer to like maybe 16% by fiscal '28. So obviously running nicely ahead there. Would you mind just orienting us around what's driven the upside so far, what's unexpected or exogenous so we can just kind of understand how much you still see from here in the buckets that you laid out in the operating plan?

**Justin Picicci** (Executives):
Okay. Thank you, Michael. Let's see if my memory is still working like a charm. So I would say -- your second question on the gross margin, I would say for the -- if you think about Q3 and our expectation on our gross margin expansion and AUR specifically because that's really the big driver of our gross margin, I would expect sort of equal contribution like we saw pretty much in Q2 for AUR. We saw equal part contributions from product mix, from geo channel mix and from pricing and promotional pullback. I would expect that to continue as we think about heading into Q3 from an AUR perspective, which again is going to be our biggest gross margin driver. I would expect AUR to normalize a bit as we talked about, getting closer in line with that longer-term sort of mid-single-digit algo as we continue to close the gap between our AUR growth and targeted unit growth as revenue drivers. 
From a promotional perspective, we're going to stay disciplined this holiday. And we've got the flexibility, we know to be targeted where the consumer environment warrants it without compromising our long-term strategy. From a promotional standpoint, North America remains relatively stable. Europe with a challenged consumer backdrop has become more promotional quarter-over-quarter. And we're on a continuous elevation journey, as you know, that remains the priority. We'll recognize the environment, particularly in Europe. We have the flexibility to respond selectively where appropriate, but our strategy is not to broadly chase the macros.
So we will lean in and be targeted in how we use promotions and present that compelling price value proposition where that consumer is feeling that the macro is tightening up, and that can include adjusting frequency, depth duration and breadth of promos without changing our overall strategic direction, and we've demonstrated that playbook over many years and our continued AUR progress and strong price architecture we've built up has given us that targeted flexibility within those brand guardrails to respond to the consumer and the competitive environment this holiday.
On your last point on margins. So yes, so we've made really strong progress over our NGC Drive 3-year plan with margins, really driven by the increased full price gross margin expansion outpacing our expectations. And what you've seen us do is we've taken some of that gross margin outperformance and reinvested back behind the brand marketing digital keys, et cetera, to really fuel durable longer-term growth. Our operating margin that we deliver this year is not a ceiling, right? We contemplate and expect year-over-year margin expansion every year of our long-term plan. And we've got durability behind both our gross margin drivers, right, which including AUR, which is a big piece of that, but also when you think about the favorable structural mix benefits that we have from geo channel, et cetera, product, et cetera.
And then on the SG&A expense line, we know we built out the muscle -- we have a culture of operating discipline. We've built out the muscle of leveraging expenses. Now you don't always see that because we opportunistically reinvest, but we've built out the muscle of leverage, and we do expect more balanced contributions from gross margin expansion and SG&A leverage as we move forward. But we certainly feel really good about our continued ability to leverage some of the big investments that we've made, whether that's in new stores, digital infrastructure, et cetera. So going forward, I would say fiscal '27 operating margin not a ceiling, year-over-year progress expected, and we've got durability behind the drivers of both gross margin and of SG&A expense to contribute to that expansion.

**Operator** (Operator):
The next question comes from Laurent Vasilescu with BNP Paribas.

**Laurent Vasilescu** (Analysts):
I wanted to ask about Asia. Justin, last quarter, I think you explicitly guided for Asia to grow mid-teens for the second quarter. I'm just curious how we should think about Asia growth for the third quarter. And then within the full year raise for Asia to grow low teens, how do we think about China? I think you called out last quarter, it was going to grow mid-teens. Is that number going up? And then within that, I'd love to hear what you're hearing -- what you're seeing on the ground in China specifically as we've heard some other luxury players call out weakness in that marketplace.

**Justin Picicci** (Executives):
Thanks for the question, Laurent. So Asia remains our strongest growth engine. We did take up that full year outlook to low teens. And for Q3, we expect a high single to low double-digit growth. So again, another strong quarter. We are -- the comps do get tougher for us as we get into the second half. Q4 is our toughest compare of the year, specifically for China, but we feel really good about the momentum that we have in Asia. It's really broad-based. It's across markets led by China, but you've got markets like Japan and Korea growing quite nicely. We've got that ongoing brand momentum, and we've got expansion opportunities across all of our key markets in that region.
On the China front, specifically, our latest call on China in this updated outlook is mid- to high teens growth for the full year. So that's come up a bit. And again, what we see in China is, again, underlying momentum, exceptional. I would say the fact that the outlook is moderating when you get to the second half of it is really tougher compares and deliberate strategic pacing of our growth and investments in that region. It's not a change in underlying momentum or a change in confidence. I don't know, Patrice, do you want to add anything on China specifically?

**Patrice Louvet** (Executives):
Sure. In Asia, in general, and China in particular, just reiterating Justin's point around the breadth of our momentum across the region. So obviously, China from an absolute number growth rate standpoint is a highlight, but we're seeing great performance in Korea, we're seeing great performance in Japan, we're seeing really strong performance in Southeast Asia. We're going through some interesting transformation in Australia that I think will yield very promising and exciting results for that market as well.
We have an outstanding leadership group running in that region. We actually just spent some time with our Board in Japan and Korea a few weeks ago. So we're in very good hands there. Asia is really playing an innovation incubator role for us as a company. And China, in particular here, whether it's about clienteling, personalization, social media engagement, the new platforms like Douyin, for example, and so much more. And I think as Justin mentioned, we're pacing our growth. The underlying growth rate is strong and very healthy but we're pacing our growth to make sure that we're strong 3 years from now, 5 years from now, 10 years from now, we're building the right foundations for the company across these key markets.
We've certainly been very excited about the response that we're getting from consumers in China across generations. And remember, we're only in top 6 cities, right? So as you think about opportunities, just like I mentioned earlier, in North America, while we've been in this market for a while, there's still significant runway for us. Obviously, that's also true for the Chinese market. So it goes back to our diversified growth model, which is many geographic expansion opportunities for the company. 
Thank you for your question, Laurent. Given the time, we're going to stop here. So thank you, everyone, for joining us today. We wish you and your families a wonderful Ralph Lauren Christmas and holiday season, and we look forward to reconnecting in early February to share our third quarter results. Until then, take care, and have a great day.

**Operator** (Operator):
Ladies and gentlemen, that does conclude your conference for today. Thank you for your participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### RL_Q1_2027_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：FY27 固定匯率營收成長上調至 5%–6%，原 4%–5%（原話："now centered around 5% to 6%, up from 4% to 5%"）
- 2026-08-06｜CFO｜guidance：FY27 營業利益率擴張上調至 60–80bp，原 40–60bp（原話："up from our prior guidance of 40 to 60 basis points"）
- 2026-08-06｜CFO｜guidance：FY27 毛利率擴張上調至 50–70bp，原為小幅擴張（原話："gross margin outlook to roughly 50 to 70 basis points"）
- 2026-08-06｜CFO｜guidance：Q2 營業利益率預期擴張 80–100bp（原話："operating margin to expand approximately 80 to 100"）
- 2026-08-06｜CFO｜guidance：Q2 固定匯率營收預期中個位數成長（原話："currency revenue to increase approximately mid-single"）
- 2026-08-06｜CFO｜guidance：Q2 稅率 19%–20%（原話："second quarter tax rate to be in the range of 19% to 20%"）
- 2026-08-06｜CFO｜guidance：FY27 亞洲營收預期上調至高個位數到低雙位數（原話："high single to low double digits"）
- 2026-08-06｜CFO｜guidance：FY27 北美營收維持低個位數成長（原話："America revenue to grow approximately low single digits"）
- 2026-08-06｜CFO｜guidance：FY27 歐洲營收維持低到中個位數成長（原話："Europe revenue to increase approximately low to mid-single"）
- 2026-08-06｜CFO｜guidance：FY27 AUR 預期中到高個位數成長（原話："mid- to high single-digit AUR growth for the full year"）
- 2026-08-06｜CEO｜guidance：FY27 中國預期約中十位數成長，管理層表示不能期待每季 40%（原話："I don't know that we can count on 40% every quarter"）
- 2026-08-06｜CFO｜guidance：毛利與營業利益率擴張預期集中於上半年（原話："expansion to be weighted toward the first half of the fiscal"）
- 2026-08-06｜CFO｜guidance：Q2 北美預期中個位數成長（原話："balanced mid-single-digit growth quarter"）
- 2026-08-06｜CFO｜guidance：Q2 亞洲預期領先成長中十位數（原話："Asia is going to lead growing mid-teens"）
- 2026-08-06｜CFO｜margin：Q1 調整後毛利率擴張 130bp 至 73.6%（原話："adjusted gross margin expanded 130 basis points to 73.6%"）
- 2026-08-06｜CFO｜margin：Q1 調整後營業利益率擴張 150bp 至 18.5%（原話："adjusted operating margin expanded 150 basis points to 18.5%"）
- 2026-08-06｜CFO｜margin：Q1 行銷費用占營收 8.2%，去年 7.5%（原話："Marketing increased to 8.2% of sales compared to 7.5%"）
- 2026-08-06｜CFO｜margin：管理層稱毛利率擴張由結構性、可持續因素支撐（原話："underpinned by structural durable drivers"）
- 2026-08-06｜CFO｜margin：關稅假設：上半年約 10%，下半年回到高十位數互惠稅率（原話："reciprocal rates in the high teens during the second half"）
- 2026-08-06｜CFO｜margin：關稅假設上半年維持約 10%（原話："approximately 10% tariff rates through the first half"）
- 2026-08-06｜CFO｜commitment：管理層重申 FY27 行銷占營收約 8%（原話："step up to approximately 8% in fiscal '27"）
- 2026-08-06｜CEO｜commitment：CEO 對 8% 行銷投入表示維持（原話："remain comfortable with the 8% marketing investment"）
- 2026-08-06｜CFO｜commitment：CFO 對三年期 7.5%–8.5% 行銷指引表示維持（原話："feel good about the 7.5% to 8.5%, 3-year guide"）
- 2026-08-06｜CFO｜commitment：行銷比例不設上限（原話："But as Patrice always talked about, it's not a ceiling."）
- 2026-08-06｜CEO｜commitment：三年期歐洲中個位數成長目標不變（原話："deliver mid-single digit for the full 3-year period"）
- 2026-08-06｜CEO｜commitment：預期 DTC 占比未來略高於 70%（原話："probably a little more than 70% DTC moving forward"）
- 2026-08-06｜CFO｜capital_allocation：Q1 透過股息與買回向股東返還逾 3 億美元（原話："we returned more than $300 million to shareholders through"）
- 2026-08-06｜CFO｜capital_allocation：關稅退款不納入調整後非 GAAP，若有相關款項計畫再投資（原話："we expect to reinvest any related"）
- 2026-08-06｜CFO｜risk：指引排除關稅退款影響（原話："guidance continues to exclude the impact of tariff refunds"）
- 2026-08-06｜CFO｜risk：歐洲風險：中東夥伴銷售與旅遊中斷（原話："disruption to Middle East partner sales and tourism"）
- 2026-08-06｜CFO｜risk：歐洲客流整體承壓，以轉換率與客單價抵銷（原話："traffic, as you know, has been broadly pressured across"）
- 2026-08-06｜CFO｜risk：北美批發 Q1 受出貨時點與恢復出貨墊高約 15 點（原話："contributed approximately 15 points of growth in"）
- 2026-08-06｜CFO｜risk：歐洲批發 Q1 含約 5 點出貨提前效應（原話："a roughly 5-point benefit from earlier timing of shipments"）
- 2026-08-06｜CEO｜customer：Q1 新增 150 萬 DTC 新客（原話："we added 1.5 million new customers to our DTC businesses"）
- 2026-08-06｜CFO｜customer：北美批發下半年加速縮減 off-price 與低階門市（原話："exit of lower-tier full-price stores in the back half"）
- 2026-08-06｜CEO｜customer：批發重整大致完成（原話："most of the reset is complete"）
- 2026-08-06｜CEO｜product：核心產品占營收逾 70%，Q1 成長中十位數（原話："Core product sales grew mid-teens in the first quarter."）
- 2026-08-06｜CEO｜product：高潛力品類（女裝、外套、手袋）Q1 成長逾 20%（原話："increased more than 20% for the quarter,"）
- 2026-08-06｜CFO｜product：管理層稱 AUR 是策略的結果而非目標（原話："AUR is an outcome of our strategy."）
- 2026-08-06｜CFO｜product：管理層稱定價架構保留彈性（原話："built flexibility into our pricing architecture"）
- 2026-08-06｜CEO｜competition：管理層稱更健康的奢侈品市場對公司是順風（原話："a healthier luxury market would be a tailwind for us"）
- 2026-08-06｜CEO｜competition：管理層稱自身定位為 inclusive luxury（原話："what we call inclusive luxury, spanning categories"）
- 2026-08-06｜CEO｜competition：管理層稱許多奢侈品競爭者中國滲透率更高（原話："many of our luxury competitors have much greater China"）

### 問答異常語氣（迴避／改口／保留）
- RL_Q1_2027_Earnings_Call_20260806.md｜問：Jay Sole 問近期／季至今趨勢｜答法：CFO 表示通常不評論季至今趨勢，改以 Q2 指引的區域成長拆解回應
- RL_Q1_2027_Earnings_Call_20260806.md｜問：Brooke Roach 問歐洲夏季各月趨勢如何演變｜答法：CEO 表示不評論當季，轉而談品牌資產指標與先前說法，未給夏季趨勢
- RL_Q1_2027_Earnings_Call_20260806.md｜問：Michael Binetti 問行銷是否朝 FY28 指引中高端或高端｜答法：未回答具體目標點，重申 7.5%–8.5% 指引與「非上限」

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
{"date":"20260522","verdict":"B（衛星候選，Post-Q4 FY26 結構性 thesis 強化但時機過熱）：Q4 大 beat（Rev +17%、Asia +28%、China +50%+、AUR 持續高雙、$2.0B Q rev/$8.1B FY），股價 5/21 +13.9% gap up 至 $374.90（漂移 +15%/2 日，QC-22 觸發）。長期 thesis 強化（China +Asia 雙引擎、$700M+ 資本回饋、ROIC 25%），但 Fwd PE FY28 20.8x（5Y 56%ile）+ PEG 1.43 + 接近 BB 上軌 $394.65（95.5%ile），短期 R:R 0.15x 失效。建議等回測 BB 中軌 $356 或 W52 $328 分批，FY27 guidance +4-5% CC 偏保守暗示成長放緩，需觀察 H2 FY27 關稅執行成效。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Asia / China 結構成長持續：Polo 在中國中產階級渗透率仍處 S 曲線中段","columns":{"2Y 驗證點":"Asia revenue +20% 以上連續 4 季；China +35%+ 連續 4 季","5Y 驗證點":"Asia 占整體營收從 21% → 30%；OM 從 31.8% 維持 28%+","10Y 驗證點":"Asia 占整體營收 40%+；China 單獨破 $1.5B","數字門檻":"Q4 FY26 actual: Asia +28%, China +50%+；H1 FY27 預期 Asia +20%+, China +30%+","信息來源":"RL Q4 FY26 法說會（2026-05-21）+ Bernstein luxury report 2026Q1","漂移觸發":"TTM 連 2 季 Asia"}},{"id":"H2","text":"Pricing Power 持續、Brand Elevation 不退色：AUR 維持高位成長 + GM 維持 68%+","columns":{"2Y 驗證點":"AUR +5%+ 連續 6 季；Adjusted GM ≥ 68% 連續 6 季","5Y 驗證點":"AUR 從基期累積 +30%；GM 維持 ≥ 67%","10Y 驗證點":"Polo Fwd PE 與 Tapestry 之溢價 stabilize 至 +15%+","數字門檻":"Q4 FY26: AUR 高雙位數連續 5 季；Adjusted GM 69%（+40bps）","信息來源":"RL Q4 FY26 8-K + earnings call + Investor's Business Daily 2026-05-21","漂移觸發":"TTM 連 4 季 GM YoY 收縮 > 100bps → 削弱；連 6 季 → 反轉"}},{"id":"H3","text":"資本回饋 + ROIC 維持頂尖：股東回饋 ≥ FCF 的 70%，ROIC 維持 22%+","columns":{"2Y 驗證點":"FY27/28 股東回饋累計 $1.5B+；ROIC ≥ 22%","5Y 驗證點":"$2B 三年資本回饋計畫如期執行；ROIC 維持 ≥ 22%","10Y 驗證點":"$3B 五年累計回饋；ROIC ≥ 20%（成熟期）","數字門檻":"FY26 actual: $700M+ 回饋；ROIC 25% (yfinance, KoalaGains)；dividend +10%","信息來源":"RL Q4 FY26 8-K capital allocation + Macrotrends ROIC history","漂移觸發":"TTM 連 2 季 ROIC"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"中國地產 / 消費結構性收縮：中國中產階級財富萎縮，Polo 在中國從 +50% → +10% 或更低","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"中國國家統計局：城鎮居民可支配收入 YoY；LVMH/Hermes/RL 中國同店銷售 YoY","警戒閾值":"連 2 季 RL Asia"}},{"id":"R2","text":"關稅升級 + 製造成本壓縮：H2 FY27 關稅實際 GM hit 超預期","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Q2/Q3 FY27 Adjusted GM YoY change；RL 法說會關於 sourcing diversification 進度","警戒閾值":"Q2/Q3 FY27 GM 連 2 季 YoY 收縮 > 150bps 警戒"}},{"id":"R3","text":"奢侈消費結構大轉向：「炫耀消費」過時，quiet luxury（Brunello 模式）勝出","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"Brunello Cucinelli / Loro Piana 同店增長 vs RL；社群媒體「logo fatigue」discourse 趨勢；GenZ luxury preference 調查","警戒閾值":"跨年度結構性翻轉確認（≥ 50% 機率轉向時需減倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":374.9,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
