你是 stock-analyst **v20 判斷 agent**，標的 XOM（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"XOM","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/XOM_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/XOM_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_adjusted_earnings_identi","label":"Adjusted earnings（排除 identified items）","value":17505,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m（每股 $4.23）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi1_gaap_earnings_attributab","label":"GAAP earnings attributable to ExxonMobil","value":15413,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m（稀釋每股 $3.72）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi2_cash_flow_from_operation","label":"Cash flow from operations","value":25650,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi4_cash_capex","label":"Cash capex","value":7002,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi5_upstream_adjusted_earnin","label":"Upstream adjusted earnings","value":7300,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi6_energy_products_adjusted","label":"Energy Products adjusted earnings","value":9100,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi7_chemical_products_adjust","label":"Chemical Products adjusted earnings","value":725,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi8","label":"產量","value":4496,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"koebd","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi9","label":"股東回饋：股利＋買回","value":9400,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m（股利 4.3B＋買回 5.1B）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi10_net_debt","label":"Net debt","value":22100,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m（總債務 34.3B－現金 12.2B）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}},{"id":"f_kpi11","label":"管理層指引","value":"2027 年買回 $20B（假設市況合理）；Q4 股利 $1.07/股（12/10 發放，11/16 登記）。新聞稿未提供 Q4／全年產量或 capex 指引","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"—","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_xom_gross_margin_pct","label":"XOM 毛利率","value":20.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XOM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_xom_operating_margin_pct","label":"XOM 營業利益率","value":10.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XOM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_xom_fcf_margin_pct","label":"XOM FCF 利潤率","value":8.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XOM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cvx_gross_margin_pct","label":"CVX 毛利率","value":32.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CVX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cvx_operating_margin_pct","label":"CVX 營業利益率","value":12.37,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CVX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cvx_fcf_margin_pct","label":"CVX FCF 利潤率","value":12.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CVX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_shel_gross_margin_pct","label":"SHEL 毛利率","value":18.69,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHEL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_shel_operating_margin_pct","label":"SHEL 營業利益率","value":14.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHEL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_shel_fcf_margin_pct","label":"SHEL FCF 利潤率","value":11.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHEL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_tte_gross_margin_pct","label":"TTE 毛利率","value":32.33,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTE.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tte_operating_margin_pct","label":"TTE 營業利益率","value":16.25,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTE.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tte_fcf_margin_pct","label":"TTE FCF 利潤率","value":10.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTE.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cop_gross_margin_pct","label":"COP 毛利率","value":27.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COP.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cop_operating_margin_pct","label":"COP 營業利益率","value":21.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COP.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cop_fcf_margin_pct","label":"COP FCF 利潤率","value":15.89,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF，公司定義）","value":19109,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":187.25,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":24.22,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":72.99,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":13.46,"period":"2026-11-02","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-02","citation":"yfinance earnings_estimate"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":12.01,"period":"2026-11-02","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-02","citation":"yfinance earnings_estimate"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":19.26,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.97,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.02,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.2,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":22097.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 34250.0、現金 12153.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":4079.0,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":785889.79,"period":"2026-11-02","unit":"USD m","basis":"市值 763792.79 ＋ 淨負債 22097.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":409366.33,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（3 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":420143.61,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.92,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 187.25 / W52 146.01 / W104 126.01 / W250 107.43 / W250 13週斜率 1.88%"},{"id":"f_ma_w52","label":"52 週均線","value":146.01,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":126.01,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":107.43,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.88,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Exxon Q2 2026 Permian output exceeded 1.8 million oil-equivalent b/d, a company record, consistent with planned 9% CAGR through 2030.","source":"Exxon Mobil Q2 FY26 / oilnow.gy search results","url":"https://oilnow.gy/featured/exxonmobil-records-highest-upstream-production-in-more-than-two-decades/","excerpt":"Permian production exceeded 1.8 million oil-equivalent barrels per day during the quarter, the highest in more than two decades. ExxonMobil said this was a company record and remained consistent with its planned compound annual growth rate of 9% through 2030.","as_of":"2026-07-31","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Analyst noted European majors Shell and bp have anemic growth profiles to 2030 versus US competitors.","source":"Argus price target note via Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/articles/argus-hikes-exxon-mobil-price-144256830.html","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Chevron holds 30% of the Exxon-operated Stabroek Block via Hess acquisition, so it shares Guyana growth; no 2026 market-share data found.","source":"Argus price target note via 247wallst","url":"https://247wallst.com/investing/2026/05/07/argus-hikes-exxon-mobil-price-target-to-169-as-permian-guyana-production-power-2026/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"第三方網站稱 ExxonMobil 評等為 S&P AA-、Moody's Aa2，展望穩定（2026 Q1）","source":"investmentgrade.com Exxon / Mobil Credit Rating & NNN Cap Rate","url":"https://investmentgrade.com/exxon-mobil-credit-rating-nnn-cap-rate/","excerpt":"Credit Ratings S&P: AA- / Moody’s: Aa2 Investment Grade Status Investment Grade Sector Energy / Convenience & Gas US Branded Sites 10,206 at year-end 2025, in the distributor and reseller category;","as_of":"2026-03-23","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"IEA June 2026 first 2027 balances: supply up ~8 mb/d to 110.3 mb/d vs demand 105.3 mb/d, implying ~5 mb/d surplus, tied to Gulf production recovery and OPEC+ higher targets","source":"The Logic / Argus Media: IEA cuts 2026 demand forecast, sees huge 2027 surplus","url":"https://thelogic.co/briefing/oil-market-could-see-a-significant-supply-surplus-again-in-2027-iea/","excerpt":"the IEA's first 2027 projections show supply surging by around 8 mb/d to 110.3 mb/d, versus expected demand of 105.3 mb/d, leaving an excess of roughly 5 mb/d","as_of":"2026-06-11","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"EIA expects 2027 global oil balance surplus of ~3.7 MMBbl/d, driven by UAE output outside OPEC quotas and softer demand","source":"Aegis Hedging: EIA outlook points to oversupplied oil market by 2027","url":"https://aegis-hedging.com/insights/eia-outlook-points-to-oversupplied-oil-market-by-2027","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Rystad projects non-OPEC liquids production peaks around 2027 at ~72 mb/d, then declines to just under 60 mb/d by 2040","source":"oilnow.gy: Rystad Energy forecast for Guyana","url":"https://oilnow.gy/news/rystad-energy-offers-conservative-forecast-for-guyanas-entry-into-top-10-non-opec-oil-producers-by-2031/","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Stabroek Yellowtail/Uaru/Whiptail expected combined ~1.3 mb/d capacity by end-2027; Exxon sees 1.7 mb/d by 2030 with eight developments, Longtail under regulatory review","source":"oilnow.gy","url":"https://oilnow.gy/?p=98075","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ExxonMobil Global Outlook: oil demand stays above 100 mb/d through 2050; argues ~15%/yr natural decline requires new investment","source":"ExxonMobil Global Outlook coverage (DieselNet / ChemicalProcessing)","url":"https://dieselnet.com/news/2026/02exxon.php","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"OPEC Sept 2026 MOMR: 2026 demand growth ~380 kb/d, 2027 growth ~2.36 mb/d to 108.19 mb/d; IEF comparison shows agencies converging on ~1.9-2.0 mb/d 2027 growth","source":"Oilprice.com / IEF","url":"https://oilprice.com/Latest-Energy-News/World-News/OPEC-Sees-Oil-Demand-Growth-Explode-Sixfold-in-2027.html","excerpt":"OPEC now expects global oil demand growth to jump from just 380,000 barrels per day this year to 2.36 million bpd in 2027","as_of":"2026-09-11","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Clean Hydrogen Works 在德州商業法院把 Exxon 加為被告，指控 Exxon 封鎖對手使用 CO2 管線網路後啟動自家潔淨能源專案（反壟斷主張）；為私人訴訟，非政府調查。","source":"Bloomberg Government - Exxon Pulled Into Pipeline Monopoly Spat in Texas Business Court","url":"https://news.bgov.com/states-of-play/exxon-pulled-into-pipeline-monopoly-spat-in-texas-business-court","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"密西根州指控 ExxonMobil、Chevron 等石油大廠合謀減緩能源轉型、壓低再生能源產出（Sherman Act 第 1 條等）；被告已聲請駁回，搜尋結果未確認後續狀態。","source":"WebSearch 摘要（Global Competition Review / 新聞聚合）","url":"https://globalcompetitionreview.com/organisations/exxonmobil","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"搜尋未發現 2026 年針對 Exxon 的聯邦 DOJ/FTC 或歐盟競爭執法行動；FTC 已於 2025 年 7 月重啟並撤銷 Exxon-Pioneer 的最終同意令。","source":"WebSearch 摘要（FTC / PBS）","url":"https://www.pbs.org/newshour/politics/federal-trade-commission-is-investigating-exxonmobils-60-billion-deal-to-acquire-a-texas-oil-company","excerpt":null,"as_of":"2025-07-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#none","axis":"reg_tariff_export","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Exxon CEO Woods called Venezuela 'uninvestable' after Maduro's removal, citing two prior expropriations; Guyana Stabroek (Exxon 45%) has ~30% acreage unexplored due to Guyana-Venezuela territorial dispute.","source":"Reuters via BOE Report: Geopolitics loom large over Big Oil earnings as investors seek Venezuela details","url":"https://boereport.com/2026/01/29/geopolitics-loom-large-over-big-oil-earnings-as-investors-seek-venezuela-details/amp/","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Two Qatar LNG trains (S4, S6) at ExxonMobil-QatarEnergy JV damaged amid Hormuz disruption; ~3% of Exxon global production, multi-year repair; Golden Pass Texas started LNG March 2026.","source":"Exxon Mobil FY2026 Q1 earnings summary (fn2.ai)","url":"https://fn2.ai/earnings/xom/2026-q1","excerpt":"Guyana production, the first LNG cargo from Golden Pass Train 1 in March, and a 200,000 barrel-per-day increase in Gulf Coast refining throughput from February to March. However, the market reaction was negative -- the stock showed a -1.3% abnormal move on the report session and drifted an additional -2.2% afterward, suggesting investors focused on the damaged Qatar LNG trains (3-5 year repair","as_of":"2026-07-28","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"Qatar-Exxon Golden Pass LNG plant in Texas starts production.","source":"E&E News","url":"https://www.eenews.net/articles/qatar-exxon-golden-pass-lng-plant-in-texas-starts-production/","excerpt":"Qatar-Exxon Golden Pass LNG plant in Texas starts production By | 03/31/2026 06:41 AM EDT Exxon says exports from Golden Pass are likely to begin in the second quarter of this year.","as_of":"2026-03-31","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"XOM 2026Q3: Upstream earnings fell vs Q2 on lower crude prices; Energy Products adjusted earnings rose to ~$9.1B from $4.1B on higher margins; Chemical Products $735M reported, down from ~$1.2B in Q2 on lower margins; Specialty Products ~$1.3B on higher base-stock margins (search summary of the press release).","source":"ExxonMobil Announces Third-Quarter 2026 Results (investor.exxonmobil.com)","url":"https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Agencies' oil demand views diverge for 2026 (IEA Aug: contraction of 1.6 mb/d; Strait of Hormuz disruption and EV adoption cited) and converge on a 2027 recovery of about 1.9-2.0 mb/d (July summary).","source":"IEF Comparative Analysis of monthly reports on the oil market (Aug 2026)","url":"https://www.ief.org/_resources/files/news/comparative-analysis-of-monthly-reports-on-the-oil-market/august-2026/ief-comparative-analysis-08-2026.pdf","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Guyana fifth FPSO on track to start in Q4 2026 adding 250 kb/d capacity; Permian Q2 2026 production reportedly above 1.8 MMboe/d with plan of ~2.5 MMboe/d by 2030; no market share figure found.","source":"Zacks: Will ExxonMobil's Guyana, Permian assets power its upstream business","url":"https://www.zacks.com/stock/news/2990692/will-exxonmobils-guyana-permian-assets-power-its-upstream-business","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"IEA Global EV Outlook 2026 稱2025年EV已替代全球約170萬桶/日石油消費（2020年為40萬），2025全球EV銷量約2,000萬輛、占新車四分之一；預期2030年替代量近三倍至約500萬桶/日。2026Q1全球EV銷量因中美政策放緩年減8%。","source":"ThisDay, Report: Electric Vehicles Cut Global Oil Demand by 1.7m bpd as Sales Top 20m (引IEA Global EV Outlook 2026)","url":"https://www.thisdaylive.com/2026/06/01/report-electric-vehicles-cut-global-oil-demand-by-1-7m-bpd-as-sales-top-20m","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"IEA分析：中東戰爭致油價波動，至4月EV駕駛人運行成本節省提高20%-45%，為EV替代提供助力","source":"S&P Global / Hellenic Shipping News, Global oil shock offers boost for EV switching, fossil phaseout: IEA","url":"https://www.hellenicshippingnews.com/?p=1143253","excerpt":"countries in Southeast Asia, including Vietnam, have already unveiled plans to broaden EV tax incentives as a result of the crisis, while 30 countries broke records for monthly EV sales in March, the IEA said. After over a month of oil price volatility linked to the war in the Middle East, running cost savings for EV drivers had risen between 20% and 45% by April, according to IEA analysis.","as_of":"2026-07-30","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"ExxonMobil 與 Chandra Asri 簽約出售新加坡 Esso 加油站網絡，轉向 branded wholesale 模式","source":"ExxonMobil corporate news release","url":"https://corporate.exxonmobil.com/locations/singapore/singapore-updates/news-releases/20251024-em-to-sell-service-station-network-in-sg","excerpt":null,"as_of":"2025-10-24","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"TickFlow 頁面（2026-08-01）列 XOM 34 位分析師平均目標價 $170.08、共識 Buy；MarketBeat 2026-07-20 共識目標價 $164.45；Benzinga 頁（9/11 更新）19 位分析師共識 $158（8 買 11 持有）。各聚合站 as-of 與分析師樣本不一，無單一定論。","source":"TickFlow / MarketBeat / Benzinga 聚合頁","url":"https://www.tickflow.io/stock/XOM/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026 年 10 月分析師動作：Barclays 10/19 維持 Overweight、目標價升至 $200；Morgan Stanley 10/15 維持 Overweight、目標價 $185；Wells Fargo 10/1 由 Overweight 降為 Equal-Weight、目標價 $182。","source":"Benzinga analyst ratings 頁","url":"https://www.benzinga.com/quote/XOM/price-targets","excerpt":null,"as_of":"2026-10-19","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Erste Group 於 2026-07 將 XOM FY2026 EPS 預估由 $11.32 下修至 $11.00，FY2027 上修至 $10.80；Chartmill 顯示 2026-10-24 FY2026 EPS 共識 12.71 美元（27 位分析師），與 Erste 差距大。","source":"MarketBeat (Erste Group) / Chartmill","url":"https://www.marketbeat.com/instant-alerts/erste-group-bank-predicts-weaker-earnings-for-exxonmobil-2026-07-20/","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 Q3 2026（2026-10-30 公布）：GAAP 盈餘 $15.4B（$3.72/股），調整後 $17.5B（$4.23/股）；公司 10/16 預告 Q3 煉油利潤使 Energy Products 較 Q2 增加 $4.5B，上游液態價格逆風 $1.3B。第五艘 Guyana FPSO 預計 2026 Q4 開始生產。未找到 capex guidance 數字。","source":"ExxonMobil Form 8-K Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0002115436/000211543626000018/livef8k3q26991.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"+","claim":"2026-05-14 達拉斯聯邦陪審團在 Ramirez v. Exxon Mobil 證券集體訴訟（2015 10-K 儲量／減損揭露，原告求償約 30 億美元）判 ExxonMobil 與三位前高管完全勝訴。","source":"Paul, Weiss client news：ExxonMobil wins complete defense verdict in rare securities class action jury trial","url":"https://www.paulweiss.com/insights/client-news/exxonmobil-wins-complete-defense-verdict-in-rare-securities-class-action-jury-trial","excerpt":null,"as_of":"2026-05-14","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"經查 SEC EDGAR 近 12 個月 8-K 共 6 份，內容為財報、Reg FD、債券發行與贖回，未見併購、重編（Item 4.02）等重大項目。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002115436&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"加州檢察總長就 Exxon 先進塑膠回收計畫起訴，指其誤導大眾（頁面日期 2026-06-23）。","source":"Energy Intelligence：California Sues Exxon Over Plastics Recycling","url":"https://www.energyintel.com/00000192-206d-dc93-abde-30fda89f0000","excerpt":null,"as_of":"2026-06-23","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"OGJ 調查：六大整合型majors 2026年資本支出約1102億美元，低於2025年的1141億美元，文章形容2026年以紀律與組合優化為主。","source":"OGJ, 2026 capital spending stays disciplined","url":"https://www.ogj.com/general-interest/economics-markets/article/55363514/2026-capital-spending-stays-disciplined","excerpt":"Exxon Mobil plans to add 500,000 barrels of oil equivalent per day by 2027, while Chevron expects annual production growth to exceed 3% through at least then.","as_of":"2026-01-15","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Energy Intelligence：XOM計畫至2027年新增50萬boe/d，Chevron預期年產量成長超過3%；多數majors上游產量持續成長，成長來自Ballymore、Uaru等新專案（產能擴張而非收縮）。","source":"Energy Intelligence, No End in Sight for Oil Majors' Upstream Growth","url":"https://www.energyintel.com/00000189-8aa1-d451-a7e9-ffb932df0000","excerpt":"Exxon Mobil plans to add 500,000 barrels of oil equivalent per day by 2027, while Chevron expects annual production growth to exceed 3% through at least then.","as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Exxon對LNG供給擴張維持指引，但美國、莫三比克、PNG專案出現延遲。","source":"Energy Intelligence, Interview: Exxon on Track to Double LNG Supply","url":"https://www.energyintel.com/00000192-111d-dc93-abde-31dd83e10000","excerpt":"Exxon said it is confident that it will deliver a big expansion of its global LNG supply capacity in line with previous guidance, despite delays at projects in the US, Mozambique and Papua New Guinea.","as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.H","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"EIA週度數據（週終10/9）：美國原油庫存減少860萬桶至4.156億桶，市場預期僅減28.8萬桶；Cushing增190萬桶，蒸餾油降至1.026億桶（去化）。後續週數據各來源互相矛盾，未核對。","source":"Shafaq News: US crude inventories drop 8.6 million barrels","url":"https://www.shafaq.com/en/Economy/US-crude-inventories-drop-8-6-million-barrels","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"JPMorgan下修Brent預測：2026Q3均價約86美元、Q4約80美元、年底78美元、2027均價64美元（價格預期走低方向）。","source":"KuCoin News: JPMorgan downgrades Brent crude outlook for 2026 and 2027","url":"https://www.kucoin.com/news/flash/jpmorgan-downgrades-brent-crude-outlook-for-2026-and-2027","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"BofA因荷莫茲海峽中斷上調2026 Brent預測","source":"BofA raises Brent forecast Hormuz","url":"https://www.webull.ca/zh-hant/news-detail/14008681197970432","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"XOM 2020 全年虧損 224 億美元（主因資產減損），為 1999 合併以來首次年度虧損；扣除減損約虧 14 億，2019 同口徑盈 96 億","source":"abc17news (AP) ExxonMobil reports its first annual loss since its merger","url":"https://abc17news.com/money/2021/02/02/exxonmobil-reports-its-first-annual-loss-since-its-merger/","excerpt":null,"as_of":"2021-02-02","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"XOM 股價 2020 年下跌約 40.9%（S&P Global Market Intelligence）","source":"Motley Fool, Why Exxon Mobil stock lost more than 40% in 2020","url":"https://www.fool.com/investing/2021/01/05/why-exxon-mobil-stock-lost-more-than-40-in-2020","excerpt":null,"as_of":"2021-01-05","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2014–2016 週期：2015 年 XOM 全年獲利約 162 億美元，約為 2014 年 325 億的一半；2015Q4 獲利年減 58% 至 28 億，為 2002 年以來最低單季","source":"IndustryWeek, ExxonMobil Profits Drop 58% in 4Q","url":"https://www.industryweek.com/finance/exxonmobil-profits-drop-58-4q","excerpt":null,"as_of":"2016-01-29","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Brent 2014 下半年跌約 50%；2016 年初較 2014 高點（逾 $100）低約 70%，跌破 $30","source":"Motley Fool, Big problems ahead for Big Oil in 2016","url":"https://www.fool.com/investing/general/2015/12/20/big-problems-ahead-for-big-oil-in-2016.aspx","excerpt":null,"as_of":"2015-12-20","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"+","claim":"2026-05-14 達拉斯聯邦陪審團在 Ramirez v. Exxon Mobil 證券集體訴訟判 ExxonMobil 完全勝訴。","source":"Paul, Weiss client news","url":"https://www.paulweiss.com/insights/client-news/exxonmobil-wins-complete-defense-verdict-in-rare-securities-class-action-jury-trial","excerpt":null,"as_of":"2026-05-14","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"加州檢察總長就塑膠回收計畫起訴 Exxon（頁面日期 2026-06-23）。","source":"Energy Intelligence：California Sues Exxon Over Plastics Recycling","url":"https://www.energyintel.com/00000192-206d-dc93-abde-30fda89f0000","excerpt":null,"as_of":"2026-06-23","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"經查 SEC EDGAR 近 12 個月 8-K 共 6 份，無 Item 4.02 重編類項目，內容為財報、Reg FD、債券發行與贖回。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002115436&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"XOM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.63,"operating_margin_pct":10.72,"fcf_margin_pct":8.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XOM","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CVX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":32.36,"operating_margin_pct":12.37,"fcf_margin_pct":12.94,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CVX","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SHEL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":18.69,"operating_margin_pct":14.36,"fcf_margin_pct":11.63,"rd_intensity_pct":0.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHEL","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"TTE","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":32.33,"operating_margin_pct":16.25,"fcf_margin_pct":10.5,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTE","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":27.68,"operating_margin_pct":21.92,"fcf_margin_pct":15.89,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COP","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"XOM"},"financial_history":{"ticker":"XOM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":398675000000.0,"revenue_yoy_pct":null,"gross_margin_pct":25.85,"operating_margin_pct":16.06,"net_income":55740000000.0,"diluted_eps":13.26,"free_cash_flow":58390000000.0,"fcf_margin_pct":14.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":334697000000.0,"revenue_yoy_pct":-16.05,"gross_margin_pct":25.14,"operating_margin_pct":13.28,"net_income":36010000000.0,"diluted_eps":8.89,"free_cash_flow":33450000000.0,"fcf_margin_pct":9.99,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":339247000000.0,"revenue_yoy_pct":1.36,"gross_margin_pct":22.62,"operating_margin_pct":11.69,"net_income":33680000000.0,"diluted_eps":7.84,"free_cash_flow":30716000000.0,"fcf_margin_pct":9.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":323905000000.0,"revenue_yoy_pct":-4.52,"gross_margin_pct":21.99,"operating_margin_pct":10.48,"net_income":28844000000.0,"diluted_eps":6.7,"free_cash_flow":23612000000.0,"fcf_margin_pct":7.29,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/XOM/XOM_Q3_2026_Earnings_Call_20261030.md）

# Q3 2026 Earnings Call
**ExxonMobil Holdings Corporation** | Earnings Calls | 2026-10-30

**James Chapman** (Executives):
Good morning, everyone. Welcome to ExxonMobil's Earnings Call. Today's call is being recorded. We appreciate you joining us. I'm Jim Chapman, and I'm joined by Darren Woods, Chairman and Chief Executive Officer; and Neil Hansen, Senior Vice President and Chief Financial Officer.  
This quarter's presentation and prerecorded remarks are available on the Investors section of our website. They're meant to accompany this quarter's earnings release, which is posted in the same location. During today's presentation, we'll make forward-looking remarks, including comments on our long-term plans, which are subject to risks and uncertainties. Please read our cautionary statement on Slide 2. 
You can find more information on the risks and uncertainties that apply to any forward-looking statements in our SEC filings on our website. We also provide supplemental information at the end of our earnings slides, which are also posted on our website.  
And now I'll turn it over to Darren for opening remarks.

**Darren Woods** (Executives):
Good morning, and thank you for joining us. In the third quarter, conflict in the Middle East continued to create uncertainty across the region and beyond, disrupting trade flows and constraining supplies of crude, diesel, gasoline and other finished products critical to economies around the world. This lack of supply led to short markets and higher market prices. We recognize the impact high prices have on people's lives and economic growth. We always have, which is why we have been constantly focused on efficiently growing advantaged production to keep markets supplied. That focus and commitment pays off in times like this.  
Over the past decade, we've invested more than $200 billion. We've stayed focused on the fundamentals of demand and developing competitively advantaged projects that grow supply across the commodity cycle. That discipline has helped us build a bigger, stronger business that outperforms our competitors. Our manufacturing complex in Beaumont, Texas, is a good example of that. In 2023, we completed a $2 billion expansion that added the equivalent of a medium-sized refinery. That investment paid for itself in about 3 years and is playing a critical role in meeting today's demand. 
That is just one of the many decisions we've made over the years that are helping address current market challenges, particularly in refining. We are the largest nonstate-owned refiner in the world. Every day, we run about 3.6 million barrels of crude through our refineries and sell about 5.7 million barrels of gasoline, diesel and other finished products into markets around the world. With products in short supply, our teams have done everything they can to keep prices down by maximizing production. Year-to-date, we have produced industry-leading volumes of diesel, roughly 1.1 million barrels per day. Global utilization of our fuels manufacturing facilities, excluding Middle East impacts, is at its highest level on record. That helped put more products into the market when they were needed most. 
We're continuing to make investments to help meet future demand. Our U.S. Gulf Coast asset reconfiguration projects are expected to increase distillate yield by about 100,000 barrels per day with the first phase already underway at Baytown. We have additional phases planned across our U.S. manufacturing sites to increase yields of diesel, lubricants and chemical feedstocks. Our global outlook projects that global energy demand will continue to grow through 2050, with oil and natural gas supplying more than half of the world's energy. Meeting that demand reliably will require continued investment across the industry, including in the Middle East.  
The value of our investments is increasing with the organizational changes we've made. This quarter, our global supply chain and trading teams moved quickly as markets shifted, securing feedstocks, redirecting molecules and moving products where they were needed most. Since 2019, Energy Products unit earnings per barrel on a constant price and margin basis are up threefold. We're seeing the benefits of our investments in Upstream as well. Excluding Middle East impacts, production volumes are up year-over-year, supported by continued growth in the Permian and Guyana. 
In Guyana, production from the Stabroek Block surpassed 1 billion barrels of oil, just 11 years after discovery. No other major offshore development has reached that milestone as quickly. The closest took roughly 3 years longer. We expect our fifth development, Uaru, to start up in the fourth quarter. 
In LNG, we're continuing to strengthen our portfolio. Cumulative LNG production in PNG has now surpassed 100 million tons with plans on track to further grow PNG production with the Papua LNG project, where we agreed to increase our working interest and assume operatorship. In Mozambique, we reached an agreement with Eni that will increase our operated interest in Rovuma LNG to 50% and exit our nonoperated acreage position. Together, these developments represent a significant step forward in building an advantaged LNG portfolio. We're also continuing to build our Low Carbon Solutions business. We received approval for the Rose carbon storage project and began carbon capture and storage operations for Nucor, our third CCS start-up for a third-party customer and second this year. Technology continues to drive performance across the business.  
In the Permian, we're the only operator currently using automated drilling rigs. We have 3 in operation today. In addition to significantly improving safety, they are delivering some of the strongest drilling performance in our fleet. We expect to expand their use to about 25% of our Permian fleet next year and approximately half by 2028, helping us continue to grow U.S. production safely and at a lower cost. 
Structural cost savings since 2019 are $16.9 billion, well on our way to $20 billion of cumulative savings by 2030. Our stronger earnings power was reflected in $15.4 billion of GAAP earnings and $25.7 billion of cash flow from operations this quarter. That financial strength gives us the capacity to keep investing in advantaged opportunities while returning cash to shareholders. This quarter, we invested $7 billion in the business and returned $9.4 billion to shareholders through dividends and share repurchases. 
Today, we announced a 4% increase in our dividend per share, marking our 44th consecutive year of annual dividend per share growth. We also announced plans to maintain share repurchases at $20 billion in 2027, assuming reasonable market conditions, reflecting our confidence in the strength of the business and our strategy to consistently grow shareholder distributions across commodity cycles. 
Finally, I'd like to recognize a positive development in Europe. As you all know, I've been very critical of European policymakers and their ill-informed attempts to reduce emissions with impractical regulations that suffocate their economy and weaken the continent's energy security. They've done a lot of damage that their citizens will be paying for far into the future. The EU Methane Regulation was the most recent example.  
We support the objective of reducing methane emissions, and we've backed that support with action. Since 2016, we've reduced methane intensity by more than 60% and recently received Gold Standard recognition from the UN's Oil & Gas Methane Partnership. The problem with the Methane Regulation is the unachievable schedule. The EU passed the law and set a compliance date without putting in place the regulations needed to implement it. They, in effect, required companies to follow a rulebook before the rules were written. The result was an unworkable compliance problem for industry.  
We made clear that ExxonMobil would comply with the law. And without a workable path to do so, we would stop importing into Europe. 
Fortunately, last week, the European Parliament voted to delay implementation by 3 years, giving the global industry time to implement systems to comply once the steps required to comply are defined. We are encouraged by this decision and hope it is a sign of things to come. The message is simple. Sound policy must work in practice. It should reduce emissions without sacrificing affordability, reliability or energy security. It also shouldn't seek to penalize companies that are meeting the critical needs of their people.  
Stepping back, the third quarter reinforced the strength of our strategy and the value of choices we've made over many years. The results we're delivering today were made possible by disciplined investments through the last decade, and we're not done. We'll continue to invest and strengthen the business, helping meet society's need for reliable, affordable energy and products while growing earnings, cash flow and long-term value for shareholders. Thank you.

**James Chapman** (Executives):
Thank you, Darren. Before we kick off Q&A, just one housekeeping item to note. Unlike the approach over the last several years, we do not plan to host a formal corporate plan update event in December. Instead, following approval of this year's plan by our Board of Directors, we will reaffirm key 2027 planning metrics through a press release later this quarter, and we expect to provide additional color during our fourth quarter earnings call in late January. 
We continue to be enthusiastic about our outlook and our execution against the long-term plans we have previously communicated. So with that, we can move to Q&A. Throughout Q&A, references made to earnings may be related to adjusted earnings. [Operator Instructions]  
And operator, we'll ask you to please open the line for the first question.

**Operator** (Operator):
[Operator Instructions] Our first question will come from Devin McDermott with Morgan Stanley.

**Devin McDermott** (Analysts):
So I wanted to start on to start on refining. It was really strong operational and financial results this quarter. And it looks like you're also able to optimize feedstocks to improve Asia throughput a bit in light of everything going on. But I really wanted to dive in further, Darren, on some of your comments around the what's next. You're one of the only companies that's materially expanded U.S. refining capacity over the last decade with the Beaumont project that you highlighted. You've been a leader in reconfigurations. You've got another one underway in the U.S. Gulf Coast. So I guess, like looking beyond the near-term, how are you thinking about the longer-term outlook for refining? What does that mean for your appetite for further expansions, reconfiguration projects and give us some details on the specifics or steps that you're undertaking to continue to boost the profitability of that business.

**Darren Woods** (Executives):
Sure. And thanks for the question, Devin. As you know, we've been really on this journey of transforming the competitiveness of our refining circuit by investing selectively in refineries, which have scale, which have an integrated portfolio of high-value products, whether it's lubricants, chemicals, high-value petroleum products. And so the work we've been doing is either investing to improve the yields and make them more competitive on a global cost of supply curve or and for refineries that didn't have the scale or some of that diversified product slate looking to find value where others see more opportunity than we do. 
And so we've been on that journey. I think we're at a stage today where the portfolio we have, we feel real good about. And the organization has now been very focused on how can we continue to high grade our product slate and improve the yields across those refineries. And that's in our traditional petroleum products, but we're also expanding the aperture and not limiting those facilities to historical products, but thinking more broadly about how can we transform, further transform hydrogen carbon molecules to make products that meet the needs of modern life. 
And some of those examples that we've been talking about more broadly, Proxxima and carbon materials. And my view is we'll continue to look for ways that we can leverage existing facilities to continue to make products that have high margins, high value. In the short term, what we see is an opportunity to invest at a much lower than grassroots cost. You can think about leveraging the existing facilities and infrastructure at a site you can bring on capacity at half the cost roughly of grassroot facility. So the economics work very well and it's just a function of what technology can you bring to bear.  
And with our now global technology organization, and the focus that the organization has on growing earnings and delivering bottom line value, we're finding more and more opportunities. So today, we're investing in Baytown. Our plans include investments in Baton Rouge and Beaumont and that will significantly improve our production of diesel, chemical feedstocks and lubricants. And so that's the path we're on.

**Neil Hansen** (Executives):
Yes. And Devin, maybe I can provide just a little bit of context on the benefit that we're seeing from having that approach of investing based on long-term fundamentals, having the financial capacity, the capital discipline to do that. If you just look at the diesel yield that was mentioned, we're up about 3.5% higher on diesel yield compared to 2019.  
For this year alone, that represents another $1.5 billion of quarterly margins or if you look at it from a year-to-date perspective, it's $3.5 billion. So that approach to investing is really resulting in a more competitive, more resilient business. And I think we highlighted in the slides that on a constant margin basis, those investments have improved that volume and mix combined with lower structural costs have tripled the underlying unit earnings of energy products since 2019.

**Devin McDermott** (Analysts):
Great results. Appreciate the thoughts.

**Operator** (Operator):
Your next question will come from Neil Mehta with Goldman Sachs.

**Neil Mehta** (Analysts):
Yes. Want to spend some time on capital returns, another dividend bump this morning, but also gave some clarity into 2027 where you fixed the buyback at around $20 billion. So just your perspective on that and that $20 billion, is that a variable payment? Or should we think of it as fixed? In other words, if oil was not $120 and oil was $60, is that still a commitment that you'd be able to make?

**Darren Woods** (Executives):
Yes. Sure. Neil, thanks for the question. I'll start off here and then let's see if the Neil here wants to jump in with any comments. But the way -- you know from the time really early on that I got into the job, we've been really focused on breaking out of this commodity cycle and chasing the cycle, but instead trying to drive a consistency across the business. And that manifested itself very early on by investing countercyclically, which was, at the time, pretty unusual in the industry.  
And we continue to stay very focused on that, that we do not want to be subject to the market forces and have to flex our -- what we believe are foundational value pillars with capital investments based on the commodity cycle. We want to ride through those. Similarly, we want to provide a level of certainty, reliability and a shareholder distributions and primarily manifested in a continuously growing dividend. That's something we've talked about for a long time and our track record demonstrates our commitment to that 44 consecutive years of increasing annual dividends.  
And so we're -- our strategy is to map a path to continue on that pace. And obviously, to do that and remain robust to bottom-of-cycle conditions, you want to be very cognizant of the dividend obligation that you create with that strategy because from our perspective, we're not going to ever cut our dividend. So any increases we add becomes an obligation that we've got to commit to the future.  
Share buybacks help us maintain that. And so you can think of the strategy is as we continue to grow dividends, we continue to buy back shares, and we maintain a fairly consistent level of dividend obligation we think makes sense. And we do that across the cycles. And so in the good times when prices are high and income is high, cash generation has been high, we don't get overexuberant and commit to things that we don't feel like we can sustain for the long term.  
And likewise, when times are a little tougher, and you're at the bottom of the cycle, we don't pull back from that commitment and continue and we use the balance sheet to supplement that. And we think, over time, that results in a more effective capital allocation strategy, one that's more consistently engaged in the marketplace with respect to buybacks and one that satisfies our shareholders with continued growth that they can count on.

**Neil Hansen** (Executives):
Yes. And Darren, maybe just to add. I mean our ability to undertake that strategy and eliminate really the distribution volatility across cycles with a deliberate growth in the dividend and ratable share purchases. You're only able to do that if you have the financial capacity to do it. And as we've talked about, that is something that's really important to us.  
We further strengthen that balance sheet this quarter, lowering net debt by more than $9 billion. Our net debt to capital is the strongest in the industry and really stronger than any, maybe except for one large cap industrial. So you have to have the financial capacity to be able to provide that certainty or less volatility in your distributions across cycles. 
And we've talked about it's the 44th year in a row that we've increased the dividend. And if you look back from the time that the ExxonMobil merger occurred, we have bought back $345 billion in shares and that represents across that time frame, which is about 27 years, an average about of $13 billion of share buybacks every single year. 
So again, the strategy to do that only allows you -- you're only allowed to execute that strategy if you have the financial capacity to do so. And if you go back to the beginning of this year, at the beginning of the year, we were actually leaning into the balance sheet a little bit to keep those distributions consistent. Of course, now in this price and margin environment, we're building cash. But that financial capacity allows you to undertake that strategy.

**Operator** (Operator):
Your next question will come from Arun Jayaram with JPMorgan.

**Arun Jayaram** (Analysts):
I was wondering if you could take a step back and discuss your global gas strategy, you announced kind of increasing your interest in Mozambique and recently in Papua. I was wondering if you could just talk about those projects, obviously, you're ramping at Golden Pass and perhaps you could weave in just maybe a little bit of an update on Qatar, which is clearly a pillar of your natural gas portfolio.

**Darren Woods** (Executives):
Sure. Happy to do that, Arun. Thanks for the question. I would say maybe just starting with the fundamental strategy and where you've seen us increase our ownership and then move into operatorship is that's pretty fundamental from our perspective. Over the last decade, we have really concentrated on growing a capability set that essentially is the best in the industry with respect to developing projects. We've developed, I think, best in the industry technology capability, and we've established a global operating organization to continue to increase the differentiation we have and our ability to operate facilities. 
And from my perspective, those 3 areas, technology, projects and operations are fundamental value pillars that form the foundation for everything else that we do. And in order to bring that advantage to bear and have it manifest itself in returns and bottom line results is we've got to operate facilities and bring that capability set to each of the projects in each of the operations we're involved in. So that's, I would tell you, a fundamental strategy that we're executing across the portfolio. And you're seeing that today in our LNG portfolio and some of the changes that we recently announced with respect to Papua and Rovuma and part of that is making sure that we have a share that's large enough to warrant the dedication of resources.  
So that's, I would say, what you see playing out in the short term here that we've announced. I think more longer term, we have -- we recognize the role that natural gas is going to play in powering the world far into the future and bringing those capabilities to bear to meet that need, we're growing our natural gas LNG portfolio, and our intention is to continue to do that. So you see continued growth, the steps that we're taking in Mozambique and Papua, Papua New Guinea are, I would say, stepping stones and actually represent what we think are even greater opportunities in those areas to grow the gas business. And so very focused on that and using our equity portfolio to then trade around the world. And so that's what you see kind of happening and having supply points geographically distributed that brings a lot of optionality and flexibility to supply the customer base. 
With respect to Qatar, I don't have much of an update. I think QE has been out very explicit about what they see happening with the damages they've had at their facilities. I would just say we continue to see Qatar as being an incredibly important source of supply for the world for LNG that somehow some way that issues in the Middle East are going to have to be resolved and the Strait is going to have to open because those resources are critically needed and we have a continuing commitment to Qatar to participate in their business and their ventures with them and continue to find ways to maximize the value, and I see that relationship going far into the future.

**Operator** (Operator):
Your next question will come from Bob Brackett with Bernstein.

**Bob Brackett** (Analysts):
Had a question around Golden Pass. Third-party data suggests it's pushing nameplate capacity on Train 1. You've got Train 2 and 3 coming next year. What have you learned from Train 1? And how should we think about the pace of ramp of Train 2 and 3?

**Darren Woods** (Executives):
Yes. Thank you, Bob. You're right. We've made good progress on Train 1. Obviously, we had the challenges a while ago with the contractor that we had engaged going bankrupt. It's been a challenge to come in and take it over like we did and progress it on the schedule that we did. And so I think everything that we learned through that process and bringing on Train 1 and some of the challenges we've experienced in that have been learned and embedded in what we're doing with Train 2 and Train 3. 
So we have very high expectations that as we bring those trains on that we're going to see all the benefits of working through the challenges on Train 1. We're making good progress on Train 2. Our expectation is we're going to basically be substantially complete by December, start the facilities commission and get that underway and then expect to achieve mechanical completion on Train 3 in mid-2027 is kind of the time frame that we're working on.
But I think our organization have really leaned into the opportunity there, and we've challenged ourselves to make sure that everything that we've learned through this challenging period with the contractors and then working with the remaining contractors and with QatarEnergy that we take those and build them into the go-forward plans. We feel pretty good about that.

**Operator** (Operator):
Your next question will come from Steve Richardson with Evercore.

**Stephen Richardson** (Analysts):
Darren, I was wondering if you could come back to Lower 48. You hit your Permian guidance number earlier in the year, production is holding in there from the outside perspective. I was wondering if you could give us a sense of what you're seeing in the program. I'm assuming you're pushing forward with some of the efficiencies and some of the technologies. And your 2030 numbers haven't changed, but how should we think about the kind of cadence of either growth or CapEx changes as we get into '27 from the Lower 48?

**Darren Woods** (Executives):
Yes. Thanks, Steve. Appreciate the question. You're right, we've made good steady progress in the Permian. We never -- we've always said that production will be a bit lumpy as we come in. And so when we talk about a year-end number, and what you've seen in this case is we've achieved that a little ahead of schedule. That's not inconsistent with think our history where we -- as the work and the wells are coming on, we're managing that. We're not real focused, as you know, on necessarily the volume target. It's really around making sure that we're executing it efficiently, deploying the capital efficiently and then very importantly, leveraging the technology work that we've been doing to maximize the value of that development project. 
That's been one of the, I think, real challenges is I feel really good about the effort between our -- the operation and the technology organization around continuing to innovate and find opportunities to deploy first in the world approaches to what we're doing there in the Permian. And I would tell you, the energy level in the company and the expectation of meeting the challenge I laid out several years ago about doubling recovery. We think there's a line of sight to that. It's really a function of deploying the technology and then giving it time to manifest itself. And I think that's probably the biggest frustration is with the size of that development as we start to feather in these technologies, see some early signs of improved productivity, just takes time for that to manifest itself in the portfolio given the base size of it. 
But we feel really good about what we're seeing and we're early in, I would say, the demonstration of the benefits but extremely enthusiastic with what we're seeing. And I think as we get a little more time under our belt, little more wells where that's deployed and a little more run time on those wells when we deployed it, we'll continue to adjust what we expect to deliver based on what we're learning there. But I would say I'm very, very optimistic.

**Operator** (Operator):
Your next question will come from Betty Jiang with Barclays.

**Wei Jiang** (Analysts):
Steve teed me up perfectly because I have a follow-up on the Permian technology discussion. And I want to specifically if I can ask about secondary recovery technologies. Just wondering if there's things that you have tested today and how big that opportunity could be in helping you achieve that aspiration of doubling resource recovery?

**Darren Woods** (Executives):
Yes. Thank you, Betty. I think you touched on a really important element of that, meeting that objective. So yes, it will be an important part of achieving the ultimate objective. And yes, the team is working on ideas for how we can improve secondary recovery. And I think again, in that space are pretty enthusiastic. What I will tell you is in order to maximize the opportunity set there, the primary recovery needs to be optimized and thought about with that in mind as well. And so it's not just come back around and think about it after you finish the primary, it is you've got to think about secondary as you're developing your plans on the primary. 
And that understanding and the interdependencies of the technologies and how we're thinking about it, we feel really, really good about. And so my sense is that piece of the equation will start to manifest itself further down the line, probably much more materially in the outer years beyond 2030 than what we're seeing here in the early years, which is really focused on the primary side of the equation. But absolutely critical part of what we're trying to do, and the team is very focused on that as well.

**Operator** (Operator):
Your next question comes from Doug Leggate with Wolfe Research.

**Douglas George Blyth Leggate** (Analysts):
Darren, I realize you're not going to do an update in December, but the portfolio seems -- the longer-term portfolio seems like it's continuing to evolve with some of the changes you've made specifically LNG. So I wonder if you could just touch on how you see the trajectory evolving post-2030. I know it's early, but I want to be specific on Guyana because you've had a number of additional discoveries. It looks like you're maybe lining up a ninth or 10th boat there. Any color you can offer would be great.

**Darren Woods** (Executives):
Yes. Well, as usual, Doug, you're kind of right in my way of thinking with respect to going longer term, we are very clearly focused as an organization in all the businesses and centralized organizations are clearly planning beyond the 2030 horizon because in this business, you've got to think long term and be trying to develop discrete plans well past in the horizon that we -- I think the Street cares about. 
And so we have been working those plans. We've got a pretty good line of sight to those plans beyond 2030. And frankly, the thing that we're working on is increasing the level of confidence and specificity of those opportunities before we kind of bring them out and start talking about them publicly. 
So we're working to bring that and to get it out, so people can see the things that we are planning to do beyond 2030, but your observation is the right one, which is we've got a really good portfolio of projects that's going to manifest itself well beyond 2030, and we're anxious to share that with you, but I want to make sure that when we do that, we've got the level of confidence necessary to make those commitments.
Because as you know, when we put a plan out within the organization and externally, I view those as commitments. And so that's how we think about it, and we don't want to get ahead of ourselves, but it's looking pretty promising. Your point about Guyana I think it's a good one. There's -- we think there's still a lot of room to run.
The team is working on that pretty focused. And I think, again, we will continue to bring that on. You've accused us of being conservative in the past, I share that conviction with you. That's generally my management philosophy when I'm working with our teams is -- and it comes back to making sure that we can deliver on the commitment.
So we don't want to be forecast heroes here. But -- my expectation is we'll do better than what we've come out and talked about simply because as we go forward, we'll learn and we'll take those learnings into what we're doing and we'll get better than what we thought. And hopefully, as we go forward, we'll keep rolling that -- those expectations out and defining those for you more clearly.

**Neil Hansen** (Executives):
And maybe just to highlight a few other areas. Doug, you mentioned Guyana, obviously, going to be -- continue to be a contributor to that growth post-2030. We talked about Papua and Rovuma. I think another key critical driver for our growth going forward is exploration. And it's a core component of our portfolio. We're committed to it. We, I think, invested $1 billion a year over the last 5 years. You mentioned the discoveries in Guyana, but we've also had discoveries in Angola and Cyprus, and we continue to expand our acreage portfolio and the rights for exploration. So I think that's going to continue to be a key part of that story post-2030. And then if you look at the Product Solutions side, we've talked a lot about the strategy of upgrading lower-value products into higher-value products. And that's certainly the case with the investments that we've made to produce more diesel, but it also extends to areas like graphite materials and Proxxima systems.
So those areas, again, I think, will be a key part of that growth going 2030. So it's certainly Guyana, but it is a portfolio of activities with a strong focus on the desire to continue to grow the business after 2030. And certainly excited when we get to the right point to disclose those plans with you as we go forward.

**Operator** (Operator):
Your next question will come from Biraj Borkhataria with RBC.

**Biraj Borkhataria** (Analysts):
I wanted to follow up on Mozambique. It was a very interesting announcement today where it looks like you're swapping the interest in the floating development for the larger onshore part. And I completely understand the rationale for that deal on both sides. I think it makes a lot of sense. Just wondering if you're still targeting an FID for Rovuma 4Q this year? And can you just touch on the sort of the remaining gating factors or anything outstanding there?

**Darren Woods** (Executives):
Yes. I appreciate the question, Biraj. I'm glad that you see the logic behind what we're trying to do there in Rovuma. And yes, we are working with the partners and the government to advance that FID. We're still very much expect to FID that here as we get through the back end of this year, that is the current plan and expectation. But as you know, with all these projects, you've got a number of stakeholders and a number of hurdles to clear, and the team is working with those folks to kind of clear all those, but we're pretty optimistic that we'll close it by the end of the year here, and then we'll get busy on execution. 
I do feel again, by bringing that -- making that change and bringing the upstream part of that development into the portfolio and managing it as one continuous project. We're already beginning to see opportunities to improve upon the capital and make that even more efficient. So feel really good about the changes that we've made here and the ability now today to bring the full weight capabilities and capacity of ExxonMobil to the full development, end-to-end development. So I think we're going to see some benefits from that, that we've yet to quantify. So feel good about the changes that we've made there and looking forward to getting started on it.

**Operator** (Operator):
Your next question will come from Manav Gupta with UBS.

**Manav Gupta** (Analysts):
You have one of the biggest global refining footprints. I'm trying to understand, given all the capacity downtime that we are seeing globally, how long do you think it will take to replenish this depleted product inventory? I'm trying to understand when could we see normalization of the refining cracks that are out there right now.

**Darren Woods** (Executives):
Well, thanks for the question, Manav. As you know, it's a hard one because there are a lot of variables impacting that, that, frankly, I certainly don't have a line of sight on in terms of how they're going to play out. So the way we've been thinking about it is different scenarios in what could develop. But I think the first thing that's ultimately going to have to happen is the world's capacity has to get back to where it was prior to these conflicts. And that's certainly the Strait of Hormuz opening up and the attacks on refining capacity in the region to stop and for those facilities to get repaired and then product moving out of them consistently, that's going to be a critical piece of the equation right now, I'd say 1/3 of the shortage out there roughly is just the inability to get clean products out of the Middle East and into the world markets.
The impact of Ukrainians bombing Russian refineries is significant as well. Russia, we estimate kind of see roughly about half of Russia's refining capacity has been taken offline. And so a country that used to be a net exporter of clean products is now a net importer. And so that's a material impact on the world balances. And that, I suspect, it's going to take some time ultimately, when the conflict stops for those refineries to get rebuilt.
So my expectation is -- and again, that's probably a little over 1/3 of the capacity that's capable of restoring balance. And so my view is that's going to be a lot longer to come online because 2 things have to happen, stop the hostilities and then start the repairs. And then the third area where there's an opportunity is China has got capacity they could bring online and run at a little higher rate to put more exports out there. I think that's the other piece of the equation that can help bring markets back into balance. So I think those are the 3 variables that I see, difficult to predict any one of those, frankly. My guess would be it will take certainly well through next year before we see things getting back closer to normal, but it could be longer than that, frankly.

**Neil Hansen** (Executives):
And I think, Darren, without knowing exactly how or when things will normalize. I think the one thing we are seeing is our ability to impact supply at scale. And you've certainly seen that with the investments that we've made over the last decade, our ability to bring on additional supply when the world needs it.
But it's also the operational excellence. I mean the fact that we've been able to run our refineries at record utilization levels of around 84%, running our Gulf Coast refineries at crude unit utilization around 100%. And so even though we don't know exactly how things will normalize and when they'll come back to normal levels, what we are seeing is the organization is responding and our ability to provide supply to society at scale, I think, is a differentiator.

**Operator** (Operator):
Your next question will come from Jean Ann Salisbury with Bank of America.

**Jean Ann Salisbury** (Analysts):
You noted in the prepared remarks that trading and optimization volumes are 4x what they were in 2019. Can you talk about whether that's mostly due to a structural strategy to build that business and maybe any specific examples that you've done there versus 2026 being an extremely volatile year and perhaps not representative of the norm?

**Darren Woods** (Executives):
Sure. Thanks for the question, Jean Ann. Let me maybe just start with a broader context because I think our trading organization has over the years, people have kind of come in and out of that and asking questions. The way we look at that for a long time, we didn't have what I would say is a typical trading organization. And in 2018, as we moved the organization to value chain. So kind of coming out of that functional construct that we had, where we had refining and marketing separate, but instead piecing all that together and running the business as the value chain, we recognize the opportunity to take advantage of these integrated global businesses take advantage of the scale that we had and the breadth that we had across the world and across these integrated value chains to use trading as a channel to optimize our assets.
And I think that's a really important distinction between maybe many of the trading houses out there who tend to be more taking positions on the marketplace. Our trading organization has been focused and is focused on maximizing the value of our assets. And so I look at it as just another channel to market. And their job is to basically in understanding the value chain, having a line of sight all along that value chain, we should be better informed and able to optimize and take positions and move barrels in a way that maximizes the value of the assets. And that's exactly what you see happening. And so rather than simply going out and taking positions or capturing arbitrage, there's, I think, a much more sophisticated approach to thinking about our footprint and how we maximize the value of that. And we look at trading as a channel to market, just like we do retail and I&W and other parts of the business.
And so that's the context I'd ask you to think about that organization and their primary objective. And that has been working very, very well. And we have slowly been growing it. And that's the other thing is we're not rushing to bring in what I would say are traditional merchant traders, we're looking to bring in people who recognize this is a unique opportunity to contribute to the value of the corporation in a unique way with access to a very unique and advantaged portfolio. And so it's a very different approach to trading, and we're finding the right kind of people who value that approach. 
And so that's been a slow growth and one that we're quite willing to take our time on to make sure we have the right capability in place. That's been happening and what you see in terms of the volume, one is just because that organization continues to bring people on and get bigger. And my expectation is we'll continue to do that in the right way with the quality of the individuals coming in, the key kind of critical path in terms of how quickly we grow. 
And then the final point I'll make is you can't discount the market and the size of the opportunity. So certainly, that is weighing in on the results. But I would say it's on top of that broader strategy and approach that we're taking.

**Neil Hansen** (Executives):
And maybe just to reiterate that point. I mean as you would imagine, those optimization capabilities are critically important, and they're more manifest when trade flows shift like we're seeing. And so that global reach that we have gives us more options to secure feedstock, redirect molecules, move products where they generate the most value for society and for the corporation. 
So as Darren mentioned, it is a channel for us. It is an opportunity or a way for us to maximize the value of our assets and the products that we sell. It gives us the optionality and the flexibility and it particularly is manifest when you see things like today when those trade flows shift but our ability to then place products where they generate the most value, where they're most needed, the ability to place feedstocks in our refineries is a true differentiator for us. But it's, again, all around this desire to maximize the assets and the value of our fully integrated value chain.

**Operator** (Operator):
Your next question will come from Jason Gabelman with TD Cowen.

**Jason Gabelman** (Analysts):
In the spirit of kind of exploring the portfolio beyond 2030. There's been reports both on your interest in Venezuela, which maybe has moved to the fore a bit more quickly than we had anticipated earlier in the year and then also interest in expanding your operational footprint in Kazakhstan with the Kashagan project. So I was hoping you could just touch on your aspirations in both of those regions.

**Darren Woods** (Executives):
Yes, sure. Happy to do that, Jason. I think, first of all, I would just caution everybody to take what's reported in the press with respect to Venezuela and ourselves with a little pinch of salt. 
I think sometimes there's some maybe a little more exuberance than is warranted. We're -- in my mind, we're not behind or ahead of anything that I talked about going all the way back to January. We recognize, and I think as the world does, that Venezuela has a lot of resource, it's a challenged resource with respect to the qualities of that crude and the challenges of producing it. So we absolutely see a need for that resource at some point in the future, but it's going to have to be produced and developed at a very competitive cost in order for it to compete on the world markets. That's going to require a scale and a technology capability and an operating capability that, frankly, very few companies have.
We believe we have advantages in that space and therefore, ultimately, we'll have a role, but like I said earlier, it's going to require some substantial changes to the way things have historically been done in Venezuela. There is progress being made on those areas, working on fiscal regimes, working on legal regimes, working on investor protections. A number of things that are kind of in progress, but there's a way to go. And I would just tell you, we're going to make sure that before we commit that those are in place, and we have confidence that we have a viable project that's sustainable and will generate the returns required to compete in our portfolio, and I expect that to take time.
So we're working our way through it. We're not in a rush. We think that opportunities are going to be there for a while. And so we're trying to be methodical and thorough. And I'd say that's how it's working. With Kazakhstan, I just think, again, another potential opportunity. I think some of the constructs of the past have introduced a lot of complexity that hasn't allowed us and the industry to effectively develop those resources. And so we've left a lot of, I think, potential trapped. And as these ventures kind of proceed, we think there's an opportunity to optimize that, and we're working with the partners there. We're working with the governments to see if we can find a better win-win proposition for all the players there, including ourselves and for the government of Kazakhstan and we see a line of sight to that.
But again, it will take time to work our way through, and we've got some very constructive discussions happening today. And hopefully, those will come to fruition sometime here in the near future, but it's a work in progress.

**Operator** (Operator):
Your next question will come from Sam Margolin with Wells Fargo.

**Sam Margolin** (Analysts):
I guess continuing on the theme of bringing an advantage to wherever you are. On the inorganic side, and the industry transaction pace is picking up, but some of what's going on is probably small for you. 
But nevertheless, it seems fairly active. And you're moving to a place where the balance sheet has a tremendous amount of capacity. And so just wondering what your latest thoughts are on the capability to do something inorganic and deliver some of your proprietary edge to an asset that could stand for some improvement?

**Darren Woods** (Executives):
Yes. Well, thank you, Sam. I agree with your kind of your thesis in the way you're thinking about it. And frankly, going all the way back when we started this effort to really focus on these core capabilities, try to build an advantage so we can improve our own operations and organic investment opportunities as well as inorganic one. So our view is this lever was going to help us across the board. And frankly, as we look forward with the ambitions that we have to grow earnings and cash flow, we're going to need every lever available to us. So we're going to need exploration and going out and finding new resources, we're going to need the ability to optimize the resources that we have and maximize recovery.
And then we're going to need to take advantage of inorganic opportunities that are value accretive to the portfolio. And so I would tell you, we're actively working all aspects of that because we recognize it that all aspects are going to be required. So I think that opportunity is there. Obviously, it's a function of finding the right partner organization and one where you can arrive at a mutually agreed value share, but I definitely think there's something there, and we're continuing to work it. And my suspicion is that as we get better and better and realize the advantages, the more deal space opens up and potentially more opportunity, but that's kind of, I'd say, an evolving space.

**Neil Hansen** (Executives):
Sam, maybe -- I mean, you referenced this in your question that we bring a set of unique competitive advantages that inherently create deal space. And if you just look back on the prior acquisitions we've done recently, taken for an example, with Pioneer, and we've been able to double the synergies of that acquisition from $2 billion to $4 billion a year. If you look at Denbury and the acquisition of the green line and the impact that's having on our approach to building out a CCS business. I mean we now have, I think, 11 MTA under contract across 8 customers.
So the history and the experience we've had is we've been able to demonstrate bringing those advantages those things that we do really well, more unique than anyone and we're able to accrete additional value to shareholders. And so again, as Darren mentioned, certainly a tool that we'll continue to look at, but we have to be patient and find those opportunities where we can bring that value and accrete additional value for shareholders.

**Operator** (Operator):
Your next question will come from James West with Melius Research.

**James West** (Analysts):
Something we've been looking into and thinking more about and occurred over a longer period of time is as Exxon has evolved over the last decade or 2, you've taken much more of an operatorship or a control stake in projects. And I'm assuming that's something that you've done -- you've tried to do this, but you've also proven that you have that operational expertise. And so curious if you could just talk about, has this been a disciplined approach? Is this the approach going forward? Is this how you're thinking about the business? Or are we thinking about it correctly that you have meaningfully increase your operatorship percentage over time?

**Darren Woods** (Executives):
Yes. Thanks, James. You're spot on. I think what you're observing is a reflection of the approach that we're moving towards, and we won't be able to execute it in all circumstances. But if you go back to the value thesis that we've been executing for the last decade. It's really -- we are uniquely positioned with a scale that, frankly, none of our competitors have and a portfolio of businesses with the synergies that none of our competitors have. 
And so as we started transforming the organization and creating value chains and then centralizing these core capabilities, so think technology, projects, and operations, we're now, for the first time in the corporation's history, capable of learning -- taking all the best practices and learnings across our portfolio and in projects, whether those practices came from our traditional or historical refining projects organization or upstream project organization or chemical projects organization or, in fact, from our technology company, those are all now in one organization. 
And that organization is taking the best of the thinking that we have across the company, irrespective of what business or function it was in and applying that to the portfolio. And for projects, which was the first organization where we started that, we've seen huge, huge benefits and improvements in kind of bringing the best thinking of ExxonMobil across our entire portfolio together and to bring those to bear on our toughest challenges. 
Technology was the second core organization that we did that. And again, we're seeing the real benefits of that where rather than organize ourselves around the company and the businesses that we've set up instead organized ourselves around the capabilities and then apply the best capabilities to the hardest problems. And I'll give you just one quick example of how that paid off, the lightweight proppant that we're now seeing deployed throughout the Permian and bringing significant value that was refining technologists who work on cokers, applying their understanding of coke morphology to a challenge in the upstream organization and coming up with a brand-new proppant, a cost-effective proppant. 
So we wouldn't have had that without technology. And we're seeing that again across all aspects of technology. And so that's bringing a huge advantage. And then we just, for the first time ever in the company, established one operating organization so that people running LNG facilities are working with and collaborating with people who run refineries or traditional chemical plants and same with our offshore platform. So today, we're seeing a great mix across that. And that learning is unique to ExxonMobil in the industry and that -- and we see huge value from that. And then in order to realize that value, we've got to be in a position where we can bring it to bear on the projects that we're engaged with, which means we need to be an operator. 
And in order to justify that effort and that allocation of resource, we need to be an operator with a significant level -- a significant share of the project. And so that's how we're thinking about it. We think we bring real value there. We bring value to our partners, and we bring value to the resource owners. And to date, that's really beginning to demonstrate itself.

**Neil Hansen** (Executives):
And maybe I'll just add, Darren, that desire for more direct control over operations and project execution really is the direct result of the confidence we have in the organization. And we've talked about the operational excellence this quarter. But you look at Darren mentioned global projects, and their performance over time, we're executing double the number of mega projects than any of our IOCs, and that performance is yielding results. They're delivering projects at 20% lower cost and 20% faster scheduled time. And so part of this desire to take more direct control of operations and project execution is the organization continues to perform really well in those areas.

**Operator** (Operator):
We have time for one more question. Our final question comes from John Royall with Piper Sandler.

**John Royall** (Analysts):
So my question is on the Middle East. You guided to a 350 kbd impact unchanged in 4Q. And I know a lot of that is wrapped up in Qatar LNG where you've had some damage. But can you speak to the egress side in the UAE in terms of what you've been able to get out of the Strait or divert barrels elsewhere if applicable and just how that's evolved over the past quarter or so since the MOU ended?

**Darren Woods** (Executives):
Sure. Yes. Thanks for the question, John. I think you're right. The impact that we're seeing from a volume standpoint is concentrated in Qatar in the loss of those trains and the inability to flow at the rates and transport LNG at the rates we were prior to the conflict. UAE production has been back up again, essentially consistent with where we've historically been. The sales though have been deferred just based on the constraints. And so what we're seeing is while the production is being booked, the realization of that production is delayed simply as a function of the logistics and the ability to move the barrels out. 
We're working to basically improve upon that. I know the UAE is very focused on developing more logistics routes to get barrels out and we're working with them on that. So our expectation is with time, we'll start to see the sales revenue catch up with the production numbers, but that today is certainly impacting us in the short-term.

**James Chapman** (Executives):
All right. Thanks, John. Thanks, everybody, for joining this call and for your questions. We're going to post a transcript of this call to the Investors section of our website by early next week, and have a good weekend.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### XOM_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜Neil Hansen｜guidance：CFO 稱 2030 年 Guyana 自由現金流將為 2025 年的 2 倍（原話："we're going to see 2x the level of free cash flow in 2030 than we saw in 2025"）
- 2026-07-31｜Neil Hansen｜commitment：結構性成本節省累計目標 2030 年達 200 億美元（原話："we plan to get to $20 billion by 2030"）
- 2026-07-31｜Darren Woods｜margin：結構性成本節省自 2019 年累計達 163 億美元（原話："Cumulative structural cost savings have increased to $16.3 billion since 2019"）
- 2026-07-31｜Darren Woods｜margin：排除生產稅與能源價格後，現金成本年增持平（原話："we're basically holding cash costs flat"）
- 2026-07-31｜Darren Woods｜risk：Q2 暫時損失約 10% 上游產量（中東衝突）（原話："approximately 10% of our upstream production"）
- 2026-07-31｜Darren Woods｜margin：化學品利潤相較 Q1 增約 180%（原話："roughly 180% increase in chemical product margins"）
- 2026-07-31｜Neil Hansen｜margin：Energy Products 占各事業線獲利比重五年由約 9% 升至約 23%（原話："it's gone from about 9% to about 23% in the last 5 years"）
- 2026-07-31｜Darren Woods｜guidance：CEO 預期煉油市場維持高利潤（原話："a very robust refining market with very high margins"）
- 2026-07-31｜Neil Hansen｜margin：CFO 回應煉油獲利低於市場預期：歸因於變數多，稱無根本疑慮（原話："no underlying concerns with how that business has performed"）
- 2026-07-31｜Darren Woods｜product：第五艘 FPSO Errea Wittu 預計年底前投產（原話："remains on track for start-up by the end of the year"）
- 2026-07-31｜Darren Woods｜product：Longtail 朝最終投資決策推進（原話："Longtail is on the path toward final investment decision"）
- 2026-07-31｜Darren Woods｜capital_allocation：正在評估第九艘 FPSO；計畫將於年底定案（原話："we are evaluating the potential for a ninth FPSO"）
- 2026-07-31｜Darren Woods｜guidance：Guyana 成本回收提前，產量權益（entitlement）將調整並反映在 2030 計畫（原話："our volume entitlements will change"）
- 2026-07-31｜Neil Hansen｜guidance：CFO 說明 Guyana 已回收 550 億美元投資，稱此為自由現金流轉折點（原話："we fully recovered the $55 billion of investment"）
- 2026-07-31｜Neil Hansen｜guidance：回應分析師框架提問：CFO 同意是自由現金流轉折而非單純權益下降（原話："That's very much an inflection into free cash flow."）
- 2026-07-31｜Darren Woods｜product：Guyana 去飽和（desaturation）時點因價格與執行而提前，原預期為今年稍晚或明年初（原話："that's obviously come forward now with where prices have been"）
- 2026-07-31｜Darren Woods｜product：Guyana 長期探勘仍有潛力，AI 工具辨識新探勘機會（原話："the tape hasn't run out on this play yet"）
- 2026-07-31｜Darren Woods｜product：Permian 單季產量創紀錄，超過 180 萬油當量桶/日（原話："more than 1.8 million oil equivalent barrels per day"）
- 2026-07-31｜Darren Woods｜competition：CEO 稱技術組合接近 2018 年提出的「採收率倍增」目標（原話："we're getting really close to that objective"）
- 2026-07-31｜Darren Woods｜guidance：Permian 新增外送管線後，CEO 認為驅動力是無瓶頸外送與最大化油產（原話："the real driver will be unconstrained takeaway capacity"）
- 2026-07-31｜Neil Hansen｜competition：管理層自稱大型專案數量約為最近 IOC 對手的兩倍（原話："twice the number of mega projects in our nearest IOC"）
- 2026-07-31｜Darren Woods｜capital_allocation：新機會的投資門檻：須相對同業具備優勢（原話："have an advantage versus what others in the industry can do"）
- 2026-07-31｜Neil Hansen｜competition：Permian 逾 3 英里長水平井數量為對手的數倍（原話："we have 1,200 wells"）
- 2026-07-31｜Darren Woods｜product：管理層稱將持續擴大餾分油（distillate）、航煤與基礎油產量，墨西哥灣沿岸有專案開發中（原話："continue to grow distillate, jet, and basestock production"）
- 2026-07-31｜Neil Hansen｜margin：今年歲修相較上一輪成本與工期的改善幅度（原話："a 30% improvement in cost and a 60% improvement in duration"）
- 2026-07-31｜Darren Woods｜risk：歐洲暴利稅：CEO 稱上次課徵後公司取消了對歐洲的規劃投資（原話："So we canceled investments that we had planned for Europe"）
- 2026-07-31｜Darren Woods｜risk：荷莫茲海峽：CEO 預期即使清除阻礙後航運恢復仍需時間（原話："there's going to be a continued inhibition for movement"）
- 2026-07-31｜Darren Woods｜risk：CEO 表示無法預測海峽何時恢復通行（原話："I can't really predict when it will happen"）
- 2026-07-31｜Darren Woods｜commitment：與卡達能源討論協助修復受損 LNG 產線（原話："We're in discussions with QE about that."）
- 2026-07-31｜Darren Woods｜risk：LNG 中東曝險：不把當前事件外推為長期區域穩定性改變（原話："we're not extrapolating current events"）
- 2026-07-31｜Darren Woods｜guidance：Mozambique LNG 目標今年稍晚做最終投資決策（原話："we hope to FID that project later this year"）
- 2026-07-31｜Darren Woods｜commitment：管理層稱未來尋找新機會時不會迴避中東地區（原話："we won't shy away from the region"）
- 2026-07-31｜Darren Woods｜margin：Specialty Products 基礎油利潤創高（原話："best ever basestock margins"）
- 2026-07-31｜Darren Woods｜product：Proxxima 產能擴建：下一階段摻配廠今年稍早已 FID，管理層稱滲透需時（原話："FID-ed the next large step in our Proxxima blending plant"）
- 2026-07-31｜Darren Woods｜capital_allocation：本季資本支出約 70 億美元（原話："Cash capital expenditures were roughly $7 billion"）
- 2026-07-31｜Darren Woods｜capital_allocation：本季透過股息與回購回饋股東超過 90 億美元（原話："we returned more than $9 billion to shareholders"）
- 2026-07-31｜Darren Woods｜guidance：全公司流程與數據平台轉型，大規模部署排在 2027（原話："larger rollouts in 2027"）
- 2026-07-31｜Darren Woods｜commitment：上游併入全球營運組織後，管理層預期改善利潤（原話："we expect to deliver improved margins"）
- 2026-07-31｜James Chapman｜commitment：公司預告 9 月發布年度全球展望（原話："we plan to publish our annual global outlook in September"）
- 2026-07-31｜Darren Woods｜customer：供應鏈調度避免約 7.5 億美元年化中斷成本（原話："helped avoid roughly $750 million in annual disruption cost"）
- 2026-07-31｜Darren Woods｜risk：Kashagan 擴建討論：管理層稱仍處早期（原話："we're too early in that process"）

### 問答異常語氣（迴避／改口／保留）
- XOM_Q2_2026_Earnings_Call_20260731.md｜問：Arun Jayaram（JPMorgan）問荷莫茲海峽現況與 7 月情形｜答法：CEO 表示沒有太多額外的現場觀點，轉述媒體已報導，並改談市場影響與航運意願，未給 7 月具體情況
- XOM_Q2_2026_Earnings_Call_20260731.md｜問：Neil Mehta（Goldman）問煉油獲利低於獨立煉廠預期，以及 Q3 走勢｜答法：CEO 與 CFO 以產品組合差異、變數多、預測難度解釋，未提供 Q3 數字或具體時點/營運因素拆解
- XOM_Q2_2026_Earnings_Call_20260731.md｜問：Biraj Borkhataria（RBC）問歐洲暴利稅發生的可能性及與決策者的討論｜答法：CEO 以政策批評作答，說「不確定是否能阻止他們」，未給出可能性判斷或對公司影響數字
- XOM_Q2_2026_Earnings_Call_20260731.md｜問：Bob Brackett（Bernstein）問歲修延後與把握高價機會的取捨｜答法：CFO 說「若能安全延後則納入考量」，改談歲修成本與工期改善，未說明本年實際延後的規模

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

## ⑥ 條件附卡（archetype_hint='循環/商品' 命中）：judge_addendum_cyclical.md

<!-- source: .claude/skills/stock-analyst/references/cyclical-lens.md sha256:b13d95972edd47ea git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary 或 secondary ∈ {循環/商品，EMS/ODM}（QC-43 判定，含 capex 建設循環／需求量循環子型） -->

# QC-42 循環交易讀數（附錄 B）附卡

循環股的錢在 Game 2（投降買、延伸賣）。本附卡是平行、明標投機的交易讀數，不改長抱裁決。[§WHY]

## 一、觸發與子型判定
無循環 sleeve（純成長 mis-route）→ 整段省略。[§①]
商品子型（下列≥2命中→用商品 through-cycle 錶）：近5-7年≥1個GAAP虧損年｜peak-to-trough毛利率擺動>~20pp｜營收主由商品ASP驅動(price-taker)｜產業∈{記憶體/DRAM/NAND、礦業/材料/稀土、化工、航運、鋼鐵、太陽能、油氣E&P、部分晶圓/設備}｜capex/rev結構性>15%且ROIC高度擺動。未達≥2仍判循環→依驅動來源選capex建設循環錶或需求量循環錶。[§商品子型]

## 二、循環位置錶族（三選一，錨自身 through-cycle 區間非動能；位置落 深谷投降/早循環/中循環/晚循環/過熱頂部，多數決+sourced 裁決）
商品 through-cycle（MU 型，6 訊號）：P/B vs 自身區間(近1x/下緣=買，>中位2x/上緣=賣)｜量 vs 價(量增領先=買，ASP-only量平降=賣)｜GM vs自身區間(近谷/負=買，近峰=賣)｜供給紀律(減產=買，新產能洪水=賣)｜庫存(去化乾淨=買，通路+公司堆積=賣)｜情緒/部位(投降PT>價=買，狂熱PT<價=賣)。[§B.1商品]
capex 建設循環（ORCL 型，6 訊號）：capex/折舊比(低/正常化=買，遠高於1=賣)｜產能利用率爬坡(低基期回升=買，滿載見頂=賣)｜RPO(backlog)vs capex覆蓋(backlog領先=買，capex超前需求=賣)｜交易對手信用(客戶分散信用強=買，集中燒錢客戶=賣)｜情緒/部位(同上)｜量vs價(量增領先=買，ASP承壓量見頂=賣)。[§B.1capex]
需求量循環（EMS/ODM，JBL 型，5 訊號）：book-to-bill/需求量拐點(>1拐點向上=買，<1量見頂=賣)｜客戶庫存去化(去化乾淨=買，通路+客戶堆積=賣)｜倍數vs自身歷史re-rate均值回歸(近下緣=買，>5Y中位×1.5/貼峰=賣)｜終端·hyperscaler capex週期位置(早週期=買，晚週期見頂=賣)｜情緒/部位(同上)。[§B.1需求量]

## 三、交易姿態 + 反動能硬閘（跨子型通用，逐條檢查，觸發即 override 向保守）
位置→姿態：深谷投降→積極分批建立｜早→分批建立｜中→持有不加｜晚→分批了結｜頂→清光不碰。[§B.2]
閘1 位置=晚/頂→姿態不得為任何「建立」。閘2 成長=ASP-only+量持平/降→最多「持有」。閘3 P/B>自身中位2x→禁新建立。閘4 訊號矛盾→標「位置不明，觀望」不硬給姿態。閘5 TTM/Fwd本益比或EV倍數>自身歷史高區(>5Y中位×1.5、或貼/破歷史峰)→禁新建立。[§閘1-5]

## 四、落欄與 §13 row 8b 接線
`cycle_position`(深谷投降｜早循環｜中循環｜晚循環｜過熱頂部)＋`cycle_verdict`(右側可追蹤｜等回踩｜頂部觀望｜未觸發)；非循環 archetype 不填，整欄省略。[§落欄]
接 §13 row 8b：位置∈{深谷投降，早循環}+五閘全過+moat底線+獨立critic冷讀通過→落「進場・條件式(循環衛星)」(倉位上限3%)；任一不成立→只落研究提名，§13維持觀望。驗證失敗不得升級，只能降回觀望。`trade_stance`僅進HTML不入dd-meta。[§row8b]

## 五、雙制度與兩軌背離
有 secular sleeve + commodity sleeve → 循環鏡頭只套 commodity sleeve，secular sleeve 一句話另計(不隨循環賣)。[§⑤]
投資軌(§13長抱視角) vs 交易軌(本鏡頭位置)：底部背離(長抱視角迴避 + 循環位置深谷投降/早循環)是本鏡頭獨門訊號；頂部多收斂(皆遠離)。[§B.3]


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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/XOM_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
