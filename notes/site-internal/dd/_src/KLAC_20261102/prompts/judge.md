你是 stock-analyst **v20 判斷 agent**，標的 KLAC（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"KLAC","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":4136.0,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","citation":"KLA Q1 FY27 新聞稿（SEC 8-K Ex.99.1）"}},{"id":"f_kpi1_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":46.1,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","citation":"KLA Q1 FY27 新聞稿；營業利益為由損益表項目推算（約 1,904.7M），新聞稿未直接列示"}},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":45.0,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","citation":"KLA Q1 FY27 新聞稿；營業利益為推算（約 1,861.7M）"}},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":1336.2,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","citation":"KLA Q1 FY27 新聞稿（營運現金流 1,530.9 − 資本支出 194.8）"}},{"id":"f_kpi5_guidance_q2_fy2027_reven","label":"Guidance: Q2 FY2027 revenue","value":"4.7B ±0.2B（4.5–4.9B）","period":"Q1 FY2027 財報（公告於 2026-10-28），指引季別＝季末 2026-12-31","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027 財報（公告於 2026-10-28），指引季別＝季末 2026-12-31","citation":"KLA Q1 FY27 新聞稿"}},{"id":"f_kpi6_non_gaap_diluted_eps","label":"Non-GAAP diluted EPS","value":1.22,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","citation":"KLA Q1 FY27 新聞稿（已調整 2026-06-11 十比一分割）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_klac_gross_margin_pct","label":"KLAC 毛利率","value":61.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_klac_operating_margin_pct","label":"KLAC 營業利益率","value":42.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_klac_fcf_margin_pct","label":"KLAC FCF 利潤率","value":27.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_asml_gross_margin_pct","label":"ASML 毛利率","value":54.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_asml_operating_margin_pct","label":"ASML 營業利益率","value":38.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_asml_fcf_margin_pct","label":"ASML FCF 利潤率","value":53.2,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amat_gross_margin_pct","label":"AMAT 毛利率","value":49.4,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amat_operating_margin_pct","label":"AMAT 營業利益率","value":31.09,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amat_fcf_margin_pct","label":"AMAT FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_lrcx_gross_margin_pct","label":"LRCX 毛利率","value":51.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LRCX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lrcx_operating_margin_pct","label":"LRCX 營業利益率","value":36.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LRCX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lrcx_fcf_margin_pct","label":"LRCX FCF 利潤率","value":25.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LRCX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_8035_t_gross_margin_pct","label":"8035.T 毛利率","value":45.56,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.8035.T.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_8035_t_operating_margin_pct","label":"8035.T 營業利益率","value":26.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.8035.T.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_8035_t_fcf_margin_pct","label":"8035.T FCF 利潤率","value":6.53,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.8035.T.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":4.5,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）","citation":"新聞稿 SBC 84.1M ÷ 推算 GAAP 營業利益 1,861.7M（占營收 2.0%）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":157.91,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-8.3,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":39.98,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":2.5,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.6 → 5.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.15,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.96 → 7.04）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.36,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.37 → 8.4）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.74,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":7.04,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":8.4,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.94,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 5.47 → 5.74（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":39.58,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝46.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":46.2,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":14.18,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝48.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":48.8,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":14.27,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝47.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":47.1,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":27.51,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 5.74，分子＝快照價 157.91","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.532,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1251.45,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 5992.64、現金 4741.19（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1302.96,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":207002.25,"period":"2026-11-02","unit":"USD m","basis":"市值 205750.8 ＋ 淨負債 1251.45","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":18856.39,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":22373.59,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":10.98,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 157.91 / W52 169.83 / W104 124.83 / W250 80.34 / W250 13週斜率 2.56%"},{"id":"f_ma_w52","label":"52 週均線","value":169.83,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":124.83,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":80.34,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.56,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"KLA 10-K FY2026 列名競爭對手為 Applied Materials、ASML、Hitachi High-Tech、Lasertec、Onto Innovation，並表示未來可能面對海內外新進入者；未載明份額消長數字。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"In each of our product markets, we have many competitors, including companies such as Applied Materials, Inc., ASML Holding N.V., Hitachi High-Tech Corporation, Lasertec, Inc. and Onto Innovation, Inc., some of which may have greater financial, research, engineering, manufacturing and marketing resources than we have.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：部分競爭對手可能捆綁產品並以顯著低於 KLA 的價格銷售競品設備，且面臨專攻局部市場的新興小公司競爭。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"These competitors may bundle their products in a manner that may discourage customers from purchasing our products, including pricing such competitive tools significantly below our product offerings. In addition, we face competition from smaller emerging companies whose strategy is to provide a portion of the products and services that we offer","as_of":"2026-08-06","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"聚合文稱 KLA 製程控制份額自2021年擴大360bp、約為最近競爭者7倍；BofA 資料晶圓檢測份額81.9%（年增83bps）；Onto 為先進封裝檢測/量測最直接對手。","source":"Nasdaq/Zacks: Is KLA the Biggest Process Control Winner From AI Spending?","url":"https://www.nasdaq.com/articles/kla-biggest-process-control-winner-ai-spending","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Onto Innovation 在先進封裝檢測、量測挑戰 KLA，Dragonfly 檢測業務 2026Q2 季增30%。","source":"Nasdaq: KLA Gains From Advanced Packaging: Can it Outpace ONTO & AMAT?","url":"https://www.nasdaq.com/articles/kla-gains-advanced-packaging-can-it-outpace-amat","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"KLA 10-K FY2026 describes a highly concentrated customer base (orders from a limited number of manufacturers are a substantial portion of sales; foundry/logic a significant portion of orders); the filing excerpt does not mention any customer second-sourcing or in-house of KLA's process control.","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"We are exposed to risks associated with a highly concentrated customer base. Our customer base, particularly in the semiconductor industry, historically has been highly concentrated due to corporate consolidation, acquisitions and business closures.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 與 FY2025 各有一家客戶約占總營收 19%（FY2024 約 13%）；10% 以上客戶為 TSMC","source":"SEC EDGAR KLA 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"In each of the fiscal years ended June 30, 2026 and 2025, one customer accounted for approximately 19% of total revenues. In the fiscal year ended June 30, 2024, one customer accounted for approximately 13% of total revenues.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"國際營收占 FY2026 總營收約 87%（FY2025、FY2024 為 89%）","source":"SEC EDGAR KLA 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"International revenues accounted for approximately 87% of our total revenues in the fiscal year ended June 30, 2026 and 89% of our total revenues in both of the fiscal years ended June 30, 2025 and 2024.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"搜尋摘要：S&P 於 2026-06-23 將 TSMC AA- 評級展望調為正向（二手來源，Moody's 評級各來源互相矛盾）","source":"letsdatascience/Insider Monkey 轉述（WebSearch 摘要）","url":"https://letsdatascience.com/news/tsmc-strengthens-credit-outlook-through-ai-chip-leadership-b2f6434f","excerpt":"S&P Global revised the outlook on Taiwan Semiconductor Manufacturing Company's AA- long-term issuer credit rating to Positive on June 23, 2026.","as_of":"2026-06-23","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 3Q26 300mm fab outlook（2026-10）：300mm 前段設備支出 2026 年 1490 億美元、年增 31%，2029 年前每年雙位數成長至 2270 億美元；2027 年 18 座新 300mm 廠動工、23 座投產或首批晶片。","source":"SEMI press release: Global 300mm Fab Equipment Spending to Reach $227 Billion in 2029","url":"https://www.semi.org/en/semi-press-release/global-300mm-fab-equipment-spending-to-reach-227-billion-in-2029-as-buildout-accelerates-semi-projects","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 年中預測：2028 年設備總銷售 2295 億美元，WFE 2027 年成長 21.8%、2028 年成長 14.1%，中國仍為最大市場但成長趨緩。","source":"SEMI press release: Global Semiconductor Equipment Sales Forecast to Reach a Record $229 Billion in 2028","url":"https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-dollars-in-2028-semi-reports","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"賣方 WFE 預估分歧：Lam 2027 年 >2000 億（2026 約 1550 億）；Deutsche Bank 1930 億/2200 億（2027/28）；Bernstein 2040 億/2590 億；Goldman 2180 億/2810 億；Morgan Stanley 2230 億/2540 億，並稱買方預期約 2300 億以上、市場預期接近飽和。","source":"Search aggregation of Lam Research call, Deutsche Bank, Bernstein, Goldman, Morgan Stanley notes (Morgan Stanley via itiger.com)","url":"https://www.itiger.com/news/2649678863","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"KLA 執行長稱依客戶投資計畫，1700 億美元 WFE 水準可達成；KLA FQ4 2026 營收約 36.6 億美元、年增 15.2%，動能來自 AI 基礎建設、先進邏輯與製程控制強度提升；混合鍵合帶來額外製程控制需求。","source":"Zacks: KLAC Q4 earnings beat on AI demand; newsquawk/JPMorgan conference coverage","url":"https://www.zacks.com/stock/news/2963607/klac-q4-earnings-beat-on-ai-demand-revenues-increase-yy","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"週期性疑慮：Lam 稱 2027 成長由 DRAM 領軍，其次先進邏輯與 NAND；Bernstein 估 DRAM 2027 +53%、2028 +37%，中國 2026–27 持平；SEMI 預測報導指出期末將面臨永續性考驗。結構性論點僅見少數分析文章，無共識。","source":"Search aggregation: Lam Research, Bernstein (techflowpost), SEMI forecast coverage","url":"https://www.techflowpost.com/en-US/newsletter/131843","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"KLA 10-K FY2026 稱遵循包含反壟斷在內之各項法規，目前對資本支出、財務狀況、營運結果或競爭地位無重大影響。","source":"SEC EDGAR 10-K FY2026 Item 1 Business - Government Regulations","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"Compliance with these laws and regulations does not presently have a material effect on our capital expenditures, financial condition, results of operations or competitive position.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因子提到美國商務部依 Section 232 對半導體及半導體製造設備進口展開國安調查，結果未知，可能帶來額外關稅與貿易限制。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"The scope of the investigations includes semiconductors, semiconductor manufacturing equipment and their derivative products, including semiconductor substrates and bare wafers, legacy chips, leading-edge chips, microelectronics and other components. While the results of the investigations are currently unknown, they may result in additional tariffs and trade restrictions, which may adversely impact our business.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"三次搜尋均未找到 2026 年針對 KLA 的 DOJ／FTC／歐盟反壟斷調查或拆分報導；僅見 2016 年與 Lam 合併因反壟斷疑慮取消等舊事。","source":"WebSearch 結果摘要（Law360 'Lam Research, KLA-Tencor Scrap $10B Merger Deal'）","url":"https://www.law360.co.uk/articles/848878","excerpt":null,"as_of":"2016-10-05","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：美國對中國出口管制（Entity List、2022/2023 BIS 規則）限制 KLA 對中國先進製程客戶的銷售、出貨與支援，無法保證出口許可會獲准，影響可能重大。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"Commerce may continue to add China-based entities to the U.S. Entity List and impose other end use or end user export restrictions, which could disrupt or prevent our product shipments to China-based entities, and further disrupt our revenue recognition, business operations and our ability to support our customers in China.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025-09 BIS 發布 Affiliates Rule（持股50%以上關聯方納入管制），2025-11 暫停一年至 2026-11。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"In November 2025, the BIS suspended the Affiliates Rule for one year until November 2026.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["triggers","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Section 232 半導體及設備調查結果未知，可能帶來額外關稅；既有關稅已推升KLA進口零組件成本；2026-02 最高法院裁定IEEPA關稅無授權，關稅與退款不確定性升高。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"The U.S. tariffs have increased our cost of revenues due to the increase in the cost of importing foreign sourced components to our U.S. facilities to build the products that we manufacture in the U.S.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026-04 BIS 出口管制更新被報導為KLA FY2026 營收逆風（限制特定先進設備出口及對特定中國客戶服務），股價當日跌約4.2%；二手聚合來源，未核一手。","source":"Yahoo Finance 文章（搜尋摘要）","url":"https://finance.yahoo.com/markets/stocks/articles/kla-corporation-lam-research-shares-035427274.html","excerpt":"A number of stocks fell in the afternoon session after a major U.S. wafer-fab equipment company disclosed an expected revenue headwind for fiscal 2026 tied to an export-control update from the Bureau of Industry and Security (BIS).","as_of":"2026-04-16","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"KLA 主要製造據點分布於美國、新加坡、以色列、中國與歐洲多地(FY2026 10-K)","source":"KLA Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000319201/000031920126000027/klac-20260630.htm","excerpt":"Its principal manufacturing activities occur in the U.S., Singapore, Israel, China and various locations throughout Europe.","as_of":"2026-08-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"部分零件與原料僅單一或少數供應商可供應，斷供會延誤出貨(FY2020–FY2025 10-K 均有此語)","source":"KLA Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920125000024/klac-20250630.htm","excerpt":"certain parts and raw materials may be obtainable only from a single supplier or a limited group of suppliers.","as_of":"2025-08-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 中國營收與前一年持平：成熟製程投資抵銷出口管制對先進技術交易的衝擊;出口管制預估至 2026 曆年累計減少營收 $300–350 百萬","source":"KLA Form 10-K FY2026 (SEC) / Q1 FY2026 earnings call","url":"https://www.sec.gov/Archives/edgar/data/0000319201/000031920126000027/klac-20260630.htm","excerpt":"Revenue in China was comparable to the prior fiscal year, as continued investments in legacy-node technologies by domestic semiconductor companies were largely offset by export control restrictions affecting certain advanced technology transactions.","as_of":"2026-08-01","retrieved_at":"20261102","affects":["thesis.R","valuation","triggers"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026（至2026-06-30）半導體製程控制段營收年增12%，由晶圓代工/邏輯與記憶體領先製程投資（AI/HPC）、先進封裝與服務帶動；PCB與元件檢測段年增21%；特殊半導體製程段年減1%（中國銷售較弱）。總營收約135.79億美元，年增11.7%。","source":"KLA Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000319201/000031920126000027/klac-20260630.htm","excerpt":"Revenue from our Semiconductor Process Control segment increased 12% in fiscal 2026 compared to fiscal 2025","as_of":"2026-08-01","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"KLA對2026年WFE的看法自1月中段130億級、4月140億以上，上修至7月低150億級美元；管理層稱2027年成長應優於2026年（來源為二手彙整，未核原文）。","source":"KLA Q4 FY2026 earnings call highlights (MarketBeat)","url":"https://www.marketbeat.com/instant-alerts/kla-q4-earnings-call-highlights-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"SEMI 2026年中預測：2026年全球設備銷售1,659億美元（年增23.2%），WFE 1,439億（+23.1%），2027年WFE +21.8%、2028年+14.1%至約2,000億，總設備2028年達2,295億（來源摘要，未核原文）。","source":"SEMI press release: Global Semiconductor Equipment Sales Forecast to Reach a Record $229 Billion in 2028","url":"https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-dollars-in-2028-semi-reports","excerpt":null,"as_of":"2026-07-14","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"KLA 10-K FY2026 risk factor：公司稱無法預測 AI 發展的步調，AI 驅動的顛覆可能以難以預測的方式影響半導體供應鏈；競爭對手可能在 AI 策略上更成功。未點名具體替代技術。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"We cannot predict the pace or trajectory of AI development or the extent to which AI-driven disruption will affect the semiconductor industry, and AI technologies may disrupt the broader semiconductor supply chain and ecosystem in ways that are difficult to predict.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子列「可能無法跟上產業技術變化」，為公司自述的技術風險之一。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"We may not be able to keep pace with trends and technological changes in the industries in which we operate;","as_of":"2026-08-06","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Yole 2026 檢測計量報告：先進邏輯、DRAM、HBM、EUV 與先進封裝使製程控制強度持續上升，另有多技術檢測與混合計量興起（摘要引述）。","source":"Yole Group, Metrology & Inspection Equipment 2026","url":"https://www.yolegroup.com/product/report/metrology--inspection-equipment-2026/","excerpt":"As advanced logic, DRAM, HBM, EUV lithography, and advanced packaging evolve, process-control intensity continues to rise","as_of":"2026-01-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Nearfield Instruments（新進計量廠商）與 imec 於 2025-11 啟動多年合作，涵蓋 High-NA EUV 光阻計量與混合鍵合特徵化，QUADRA 部署於 imec Leuven。","source":"Nearfield Instruments 新聞稿 (GlobeNewswire/Silicon Semiconductor)","url":"https://siliconsemiconductor.net/article/122993/Nearfield_Instruments_signs_multi-year_development_project","excerpt":"Nearfield Instruments will deploy its flagship system, QUADRA, at Imec's advanced R&D facility in Leuven.","as_of":"2025-11-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"KLA 2026-07-28 財報給 FQ1'27 營收指引 $3.8B–$4.2B、EPS $1.06–$1.26（Benzinga 稱較前區間 $3.38B–$3.77B 上調）；Benzinga 統計自 2022-10 起指引上調 12 次、下調 4 次。未見 2026 年下調。","source":"Benzinga KLAC earnings-forecasts","url":"https://www.benzinga.com/quote/KLAC/earnings-forecasts","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-04-30 Needham 目標價 $1,800→$2,000（Buy）；Oppenheimer $1,900→$2,000（Outperform）。","source":"Placera/Dow Jones telegram: Needham Adjusts Price Target on KLA to $2,000 From $1,800","url":"https://www.placera.se/telegram/kla-needham-adjusts-price-target-on-kla-to-2-000-from-1-800-maintains-buy-rating-20260430","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Hudson Labs 前瞻稱 FQ4'26 營收指引 $3,575M±$200M，與共識 $3,602M 大致一致（指引中點與共識無明顯落差）。","source":"Hudson Labs KLA Q4 2026 earnings preview","url":"https://www.hudson-labs.com/research/kla-q4-2026-earnings-preview-klac-revenue-and-outlook","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"UBS 2026-04-21 目標價上調 16.5% 至 $1,835，評等 Neutral","source":"UBS raises price target ahead of FQ3 2026 earnings","url":"https://1strespondernews.com/expert-time/KLA-Corporation-KLAC-UBS-Raises-Price-Target-Ahead-of-Fiscal-Q3-2026-Earnings-Release-11-1067","excerpt":null,"as_of":"2026-04-27","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共10份，無併購、重編（4.02）、破產等項目；重大項目為 5.03 章程修訂、8.01 股利／回購／10 拆 1 股票分割等例行事項。","source":"SEC EDGAR 8-K 申報清單（2025-11-02 至 2026-11-02）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000319201&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"10-K FY2026 Note 14 僅載常規訴訟（商業、IP、勞資），未揭露重大個案。","source":"SEC EDGAR 10-K FY2026 Note 14","url":"https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm","excerpt":"We are named, from time to time, as a party to lawsuits and other types of legal proceedings and claims in the normal course of our business.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-05-07 董事會核准 10 拆 1 股票分割，2026-06-11 生效；2026-03-11 新增 $70 億回購授權。","source":"SEC EDGAR 8-K 2026-05-07","url":"https://www.sec.gov/Archives/edgar/data/319201/000119312526212093/d116682d8k.htm","excerpt":"the Company's Board of Directors (the \"Board\") had approved a ten-for-one forward stock split","as_of":"2026-05-07","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"KLAC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":61.47,"operating_margin_pct":42.64,"fcf_margin_pct":27.83,"rd_intensity_pct":10.8},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"ASML","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":54.34,"operating_margin_pct":38.55,"fcf_margin_pct":53.2,"rd_intensity_pct":12.41},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"AMAT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.4,"operating_margin_pct":31.09,"fcf_margin_pct":18.23,"rd_intensity_pct":12.88},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"LRCX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":51.05,"operating_margin_pct":36.95,"fcf_margin_pct":25.02,"rd_intensity_pct":9.44},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LRCX","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"8035.T","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.56,"operating_margin_pct":26.34,"fcf_margin_pct":6.53,"rd_intensity_pct":10.96},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.8035.T","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"KLAC"},"financial_history":{"ticker":"KLAC","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":10496056000.0,"revenue_yoy_pct":null,"gross_margin_pct":59.81,"operating_margin_pct":38.06,"net_income":3387277000.0,"diluted_eps":2.415,"free_cash_flow":3328214000.0,"fcf_margin_pct":31.71,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":9812247000.0,"revenue_yoy_pct":-6.51,"gross_margin_pct":59.97,"operating_margin_pct":37.05,"net_income":2761896000.0,"diluted_eps":2.028,"free_cash_flow":3031191000.0,"fcf_margin_pct":30.89,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":12156162000.0,"revenue_yoy_pct":23.89,"gross_margin_pct":60.91,"operating_margin_pct":41.25,"net_income":4061643000.0,"diluted_eps":3.04,"free_cash_flow":3746644000.0,"fcf_margin_pct":30.82,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":13579476000.0,"revenue_yoy_pct":11.71,"gross_margin_pct":61.3,"operating_margin_pct":41.69,"net_income":4830771000.0,"diluted_eps":3.66,"free_cash_flow":3767134000.0,"fcf_margin_pct":27.74,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/KLAC/KLAC_Q1_2027_Earnings_Call_20261028.md）

# Q1 2027 Earnings Call
**KLA Corporation** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Good afternoon. My name is Stephanie, and I'll be your conference operator today. At this time, I'd like to welcome everyone to the KLA Corporation September Quarter 2026 Earnings Conference Call and webcast. [Operator Instructions] 
I will now turn the call over to Kevin Kessel, Vice President of Investor Relations and Market Analytics. Please go ahead.

**Kevin Kessel** (Executives):
Welcome to the September 2026 quarterly earnings call. Joining me are our CEO, Rick Wallace and our CFO, Bren Higgins. We will discuss today's results as well as our outlook, which we released after the market close, and it is available on our website along with supplemental materials. 
We are presenting today's discussion and metrics on a non-GAAP financial basis unless otherwise specified. All the full year references we make always refer to calendar years. The earnings material contains a detailed reconciliation of GAAP to non-GAAP results. Our comments today are subject to risk and uncertainties reflected in the disclosure of the risk factors in our SEC filings. Any forward-looking statements, including those we make on the call today, are also subject to those risks, and KLA cannot guarantee those forward-looking statements will come true.
Our actual results may differ significantly from those projected in our forward-looking statements. For any subsequent updates, please refer to KLA's IR website, which also contain investor events, presentations, corporate governance information and links to our SEC filings. 
We will begin the call with Rick providing commentary on the quarter and our overall business environment, followed by Bren with financial highlights and our outlook. 
I'll pass the call now to Rick. Rick?

**Richard Wallace** (Executives):
Thanks, Kevin. KLA's September quarter beat the midpoint of our guidance ranges across all key metrics. Revenue was another record $4.14 billion. This, coupled with our December quarter revenue guidance of approximately $4.7 billion, demonstrates the growth acceleration we planned for the second half of 2026. KLA's performance in the quarter was supported by continued strength in leading-edge foundry/logic related to AI infrastructure investments and increasing process control intensity across leading-edge devices and advanced packaging. 
Other highlights for the quarter include KLA delivering operating margins above 46% for the first time ever. Gross margin was 62.7%, and free cash flow was $1.34 billion. Over the course of calendar 2026, the AI demand environment has continued to strengthen as reflected in our performance. Additionally, our strong customer engagement has provided visibility into a more favorable outlook for wafer equipment investment for calendar 2026 and 2027. We see this reflected in our growing backlog and sales funnel forecast. 
We expect momentum across our business to continue into the December quarter, and we're positioned to deliver significant growth in calendar 2027. We have been proactively working with our strategic supply chain partners over the past year to keep up with our demand. Advanced packaging remains increasingly critical to AI infrastructure expansion, and advanced packaging road maps continue to incorporate more sophisticated wafer front-end processes, which drive additional process control requirements. 
KLA's leading process control portfolio enables the company to address these requirements across a growing range of applications. For calendar 2026, advanced packaging process control systems revenue remains on track to hit approximately $1.1 billion or more than 70% year-over-year growth, nearly twice the growth rate of the advanced packaging market. 
The growing complexity of KLA's installed base and lengthening tool life cycles continues to increase demand for services. KLA services revenue was $850 million in the quarter, up 14% year-over-year, supported by a growing installed base and continued customer focus on tool performance, productivity and availability in this tight system utilization environment. 
Finally, KLA's process, PCB and component inspection businesses are also benefiting from technology transitions and the rigorous performance requirements of high-performance computing. In summary, KLA is experiencing strengthening momentum driven by growth across the semiconductor ecosystem. The pace of our backlog growth is a key signal of accelerating momentum and provides confidence in our visibility into calendar 2027. Our September quarter results demonstrate the strength of KLA's market position and operating model execution. 
Semiconductors continue to play an increasingly important role across global industries with growth driven by investment in AI infrastructure and expanding demand across a broader range of applications and markets. Together, these trends are supporting stronger, more durable and more diversified long-term growth for the industry. Additionally, the growing complexity of AI-enabled semiconductors is increasing process control intensity throughout the manufacturing flow, reinforcing KLA's long-term growth opportunity. 
KLA's differentiated portfolio is uniquely positioned to address these requirements, while sustained AI data center investment and broader adoption of advanced packaging architectures continue to expand the company's addressable market. As we look ahead, we remain focused on supporting customer road maps, investing in innovation and scaling our global capabilities to meet expected demand growth through calendar 2027. As we progress toward our 2030 target model, we remain committed to disciplined execution, technology leadership and our proven capital allocation strategy and create -- which will allow us to create durable shareholder value. 
With that, I'll turn the call over to Bren to discuss the quarter's financial highlights.

**Bren Higgins** (Executives):
Thank you, Rick. KLA delivered strong sequential and year-over-year growth in the September quarter. For the first time in our company history, KLA delivered operating margins over 46%. These results reflect our market leadership and disciplined execution, supported by our global team's dedication and focus on customer success. 
Revenue of $4.14 billion was above the midpoint of guidance and rose 13% sequentially and 29% year-over-year. Non-GAAP diluted EPS was $1.22, and GAAP diluted EPS was $1.18, each above the midpoint of the respective guidance ranges. 
Gross margin was 62.7%, slightly above the midpoint of the guidance range. Operating expenses were $688 million including $395 million in R&D and $293 million in SG&A. Operating margin rose 240 basis points sequentially to 46.1%. 
Net income was $1.60 billion. GAAP net income was $1.55 billion. Cash flow from operations was $1.53 billion, and free cash flow was $1.34 billion. The company had 1.311 billion diluted weighted average shares outstanding for the quarter. The breakdown of revenue by reportable segments and markets, major products and regions can be found within the shareholder letter and slides. 
Moving to the balance sheet, KLA ended the quarter with $4.7 billion in total cash, cash equivalents and marketable securities and [ $5.95 ] billion of debt. The company maintains a flexible and attractive bond maturity profile supported by investment-grade ratings from all 3 major rating agencies. 
The industry outlook continues to strengthen, with visibility improving as customers increase long-term investment plans. Despite these fab space limitations, customers have been very resourceful and are accelerating delivery expectations across all segments. We are, therefore, raising our expectation for the wafer equipment market, including advanced packaging, to approximately the mid-$150 billion range in calendar 2026. KLA backlog continues to grow, and our sales funnel visibility is unprecedented, supported by new fab investments by a broad base of customers. We continue to plan for significant growth in calendar 2027. 
While we'll have more to say about market and customer segment expectations for next year in our earnings call in late January, we currently expect the wafer equipment market to exceed $200 billion in calendar 2027. Customer engagement remains robust with numerous new fab projects and greenfield facilities scheduled to come online in the quarters ahead. The primary area of focus for our customers is on delivery urgency aligned with new project plans. Against this backdrop, KLA's business momentum and critical role in leading-edge process control positions us to deliver accelerating growth for the remainder of calendar '26 and continuing into 2027. 
Our expectations of revenue growth acceleration in the second half of '26 are playing out as more capacity comes online in our long lead time supply chain areas. This is resulting in growth in the second half of calendar year '26 over the first half of approximately 25% and positions the company for continued sequential growth into calendar 2027. KLA's December quarter guidance is for revenue of $4.7 billion, plus or minus $200 million. Foundry/logic revenue for semiconductor customers is forecasted to be approximately 60%, and memory is expected to be about 40% of semiconductor process control systems revenue to semiconductor customers. 
Within memory, DRAM is expected to account for approximately 84%, with NAND representing the remaining 16%. As a reminder, these business mix approximations pertains solely to our semiconductor customers and do not fully reflect our total semiconductor process control systems revenue. 
Gross margin for the December quarter is forecasted to be 62.5%, plus or minus 1 percentage point. While the company is demonstrating expected operating leverage across the business as it grows, this is being offset by persistently high memory costs for our system image processing requirements as we have discussed in prior quarters. We are actively engaged across the portfolio to optimize memory efficiency in our systems, along with other product cost reduction initiatives. These efforts, coupled with driving our usual returns-based value sharing with our customers, should offset this headwind over time. 
Operating expenses are forecasted to be approximately $710 million in the December quarter. We will continue to prioritize next-generation product development, scaling our business execution and company infrastructure investments to support expected revenue growth over the next several years. And we anticipate these expenses to grow sequentially through 2027, but at a much slower pace than revenue growth and consistent with our business model for operating margin leverage. 
As a reminder, our business model is designed to deliver 40% to 50% incremental operating margin leverage on revenue growth over the long run. Other model assumptions include other income and expense net of approximately $25 million expense for the December quarter, and we expect it to remain at approximately this quarterly level. 
Planning tax rate is 14.5%. Our tax rate will vary quarter-to-quarter due to the geographic distribution of profit and various discrete items. The December quarter, non-GAAP diluted EPS is expected to be $1.44 plus or minus $0.11, and GAAP diluted EPS is expected to be $1.41, plus or minus $0.11. EPS guidance is based on a fully diluted share count of approximately 1.306 billion shares. 
In conclusion, process control and KLA, in particular, remain critical to the AI ecosystem build-out and benefits from numerous ongoing relevance -- inflections, including increases in leading-edge designs across foundry and logic, device size and value, rising complexity and performance requirements and the growing importance of advanced packaging. KLA is experiencing strengthening momentum and a broader set of growth drivers across the semiconductor ecosystem. The rate and pace of our backlog growth is a key signal of our accelerating momentum and increased confidence in our visibility leading into calendar 2027. 
Our September quarter results demonstrate the strength of KLA's market position and operating model execution and support continued confidence in our performance moving forward. These recent results also illustrate the strength of KLA's market-leading portfolio, disciplined operating model execution and continued confidence in improving our performance moving forward. 
Looking ahead, we remain focused on supporting customer road maps, investing in innovation and scaling our global capabilities to meet expected demand growth throughout calendar '27 and beyond. As we progress towards our 2030 target model, we remain committed to disciplined execution, technology leadership, our proven capital allocation strategy and creating durable shareholder value. 
That concludes my prepared remarks. Kevin, please begin the Q&A.

**Kevin Kessel** (Executives):
Operator, can you please give the instructions -- sorry, can you just give the instructions and we'll get started.

**Operator** (Operator):
[Operator Instructions] We will now take our first question from Jim Schneider with Goldman Sachs.

**James Schneider** (Analysts):
Good to see the accelerated growth in the back half. Relative to calendar 2027 and your view of $200 billion in WFE, obviously, you have some good things going for you with advanced packaging growth and so on. So can you maybe kind of articulate how you're thinking about the way calendar '27 shapes up and your level of confidence that you're going to be -- your ability to outgrow that 30% rough market number for 2027?

**Bren Higgins** (Executives):
Jim, thanks for the question. When we look at 2027, and we've been saying this for quite some time, is we think the construct for '27 sets up pretty favorably for us. First, we feel very good about our supply situation, right? We've been working at it for the last 12 months. We indicated we see an acceleration in the second half. Certain components get -- have very long lead times. And so getting that to come online was a bit of a challenge in the first half, and we're seeing that play through, and that certainly informs our confidence in the December quarter, but also our views into '27. 
The setup for '27 around the leading edge, both in terms of the breadth of investment at the leading edge, new node investment, we think that sets up very well for the company, greenfield investment in DRAM, the HBM dynamics and how that's affecting process control intensity. We're also seeing uplift in process control intensity in conventional memory. 
Advanced packaging has been a nice growth driver. I don't see any reason why, as we look at next year that, that part of our business wouldn't continue to grow faster than the market. So we feel overall that the setup is very leading edge centric. Packaging is augmenting the growth, and we think we're well positioned and our supply should be there to be able to enable us to meet the demand. Demand is strong. I would say that we're -- I'm still behind in supply, but I still -- I think that the trajectory is good, and we feel pretty confident about the guidance we've given.

**James Schneider** (Analysts):
Yes. Sorry. And sorry, just one quick follow-up. As you think about the way the shape of 2027 starts to materialize, anything to call out in terms of the back half of 2026 was certainly much stronger than the first half. Do you think it's going to be more ratable through 2027? Or you get, again, maybe being a little more back half loaded?

**Bren Higgins** (Executives):
Right now, I would say for the next several quarters, given the backlog growth and the visibility in the funnel that we'll see sequential growth for the next several quarters. Sort of implied second half stronger. I think it's more linear. We won't have the same -- I don't think, as of now, the same significant uptick in half-to-half growth. It looks a little more linear to us, but we would expect sequential growth moving forward.

**Operator** (Operator):
We'll take our next question from Harlan Sur with JPMorgan.

**Harlan Sur** (Analysts):
On the gross margin front, I know the team had some cost headwinds this year, memory pricing headwinds, maybe GPU, CPU pricing headwinds as well. Moving into next year, I know the team has benefit of new platforms, which carry higher pricing. Obviously, you're going to be driving higher volumes, maybe you've got other value pricing initiatives taking place. Can we expect the team to buy back into that sort of 63% plus range on a strong WFE outlook in 2027?

**Bren Higgins** (Executives):
Yes, Harlan, it's a good question. As you said, there are some new parts in it. When you look at the target range, right, our target range that we outlined back in March at Investor Day was 63% to 64%. Certainly, some of the cost inputs have been challenging. We're doing a lot of work inside the company, both in terms of broader input costs, but also memory, I'll call memory optimization work in terms of our use of memory in our systems. There'll be some mix dynamics looking forward, right? We do have more advanced packaging growth. We have growth in our non-semi PCB businesses. So that tends to be a bit of a headwind to the overall margin, although a contributor to both revenue growth and gross margin growth. 
Scale will offset some of that. We'll see some manufacturing scale given the strong revenue growth environment. And some of our pricing initiatives, we think, similar to what we're hearing from peers, we think that, that will play through as we introduce new capabilities and we're able to share in the value of those new capabilities with our customers. So I think as we move forward, the memory environment will continue to be challenging. But I think as we go forward, we'll see improvement. I don't know exactly when we'll start to see it. But I think as we move through '27, certainly, as we move into the middle to the back half of '27 into '28, we'll be, I think, consistent with the operating model for gross margin that we laid out back in March.

**Harlan Sur** (Analysts):
I appreciate that. And then on the non-AI kind of more legacy node segments, auto, industrial, IoT, obviously, cyclical dynamics are strong. Supply is tightening at a very, very rapid pace, and we are seeing new capacity addition announcements. Is this contributing to the strong growth outlook next year? And maybe what percentage of your process control systems business is mature and specialties?

**Bren Higgins** (Executives):
Yes. I would say around power. I mean, power is certainly something that is an area of focus in the industry. And there was obviously -- there was a period of time where there was some overinvestment there, but I'm starting to see some indications of some recovery in that part of the market. Obviously, what's driving the business in a more significant way is everything related to high-performance compute. 
But when I look at the customers that we are serving the more legacy-centric markets, I do think that I'm seeing some improvement. So I think year-to-year, there's some growth. I don't think it will be at the level of what we expect from the leading edge. And you'll have activities in China, which will grow, but I don't think we'll grow -- it will grow at a much slower rate. 
And so I think when you look at the overall legacy, I would expect to see some growth there. But the business is really being driven by what's happening at the leading edge. But I think that there's opportunities for us to augment growth moving forward from some more business in that part of the market. 
Process control intensity tends to be lower in legacy nodes. If it's an established node, it's fairly mature unless our customers are changing designs or design rules or have new reliability requirements that could drive inflections in intensity. But the intensity levels in legacy are lower than what they are at the leading edge.

**Operator** (Operator):
We will take our next question from C.J. Muse with Cantor Fitzgerald.

**Christopher Muse** (Analysts):
I guess a follow-up, Bren, on the gross margin side. If we isolate just to process control, you were north of 65% in June of '25. And obviously, as you've talked about, major headwinds from DRAM, in particular. But curious, as those contracts roll off and you kind of move to new contracts, should we start to see better pricing as you pass that incremental along? And is there kind of a time frame where you see process control getting back to kind of that mid-60s level?

**Bren Higgins** (Executives):
On a consistent mix, I can see it trending there as we move into the second half of '27. We start to do deals around new products beyond the existing business that we have. It's very difficult to go increase prices when you have a deal in place on existing business and existing backlog. So I think as we move forward, I don't see any reason why, assuming mix is consistent, that we won't start to see some improvement in the process control parts of the business apples-to-apples.

**Richard Wallace** (Executives):
And also, C.J., Bren mentioned in the last answer, but I'm not sure you heard it was that there are -- there is work going on to utilize less memory in the systems, engineering work, which takes some time to do it. But when we design these systems, nobody really imagined the kind of increase in memory costs. And I think the common response to that is to make the systems more efficient around using memory. Therefore, that will drive that percent content down over time. It takes a while for those to get in.

**Christopher Muse** (Analysts):
Very helpful. And I guess as a follow-up, can you kind of talk about what you've seen in the last kind of 3 to 6 months from a lead time perspective and how that informs kind of your outlook into 2028? And how you're thinking about hiring and what kind of work, specifically on the supply chain to get ready for this multiyear growth cycle?

**Richard Wallace** (Executives):
Yes, C.J., the conversations we've had with customers in the last few months have been very consistent in that there's a huge request that we prioritize their projects. And they're laying out multiple-year investment cycles with an expectation that we'll support them through those ramps. 
So when we look out at the 2030 model that we laid out before, obviously, the assumptions in that model are going to be exceeded before 2030. So there is a significant amount of investment that we need to do pretty much across the board with talent but also with facilities and our investment in supply chain. And so Bren can share some of his perspective on that.

**Bren Higgins** (Executives):
Yes. On lead times, I would say, at least, and they vary by product, but we're averaging right around 12 months or so. And I would say that on the margin, they're extending. Certain products, it can be even further out than that, for example, Gen 4 and Gen 5 product lines will have longer lead time. So it does vary. 
But I think we're in a pretty good position, as Rick said, to support it. I mean, we're making investments across the board. We'll add head count both in manufacturing and service in the volume-centric parts of the business and applications and engineering over the course of the next 12 months. We're investing in every factory we have. And so there are expansion plans, not only near-term requirements and doing things quickly, but also supporting what we believe will be a multiyear investment cycle here.
So we're encouraged by that in supply chain, particularly in those areas of long-term or long lead time items, particularly in the optics area, we are working with our key suppliers to make investments. The investments show up in different forms, but also investing to support what we expect to be a very strong outlook over the next several years.
So there's a lot of activity going on. Obviously, that flows through our numbers, activity that's supporting future revenue streams. But we think that, first of all, contemplated in the model and the guidance we've given, but certainly, a lot of focus in those areas.

**Operator** (Operator):
We'll take our next question from Timothy Arcuri with UBS.

**Timothy Arcuri** (Analysts):
Bren, you did a really nice job this year only losing like 20 basis points worth of WFE share despite what was a pretty bad mix actually. It sounds like you think WFE is going to grow like low to mid-30s next year, and your lead times are 12-plus months. So you know like exactly what you're going to ship next year. So are you going to grow more than that? Will you grow more than low to mid-30s, so you'll grow -- so you'll gain share next year, gain WFE share?

**Bren Higgins** (Executives):
Yes, Tim, on '26, I think the second half momentum highlights where I think the business is trending now. I mean the first half was weaker and wasn't so much mix of business as much as it was just our ability to supply it. The backlog is pretty significant. If I had -- I've been short all year, still short now. 
So I feel that as we look at 2027, we feel pretty good. I talked about the setup, which I think is encouraging, but we feel pretty good about our ability to maintain and drive the growing KLA relevance story that we outlined at Investor Day. The parts of the market that are inflecting are very good for process control. We think they uniquely benefit process control.
And we think that, that as we are in a better position to supply and meet the demand that we can maintain the trajectory that we laid out. It doesn't mean it happens in every 6-month period or every quarter, but we think over time, similar to what we saw over the last 5 years, the next 5 setup is pretty strong. And we feel pretty comfortable about our views of share of market growth over the next -- between now and 2030.

**Richard Wallace** (Executives):
So we think we can outgrow next year, Tim.

**Timothy Arcuri** (Analysts):
Got it. And then, Rick, I wanted to ask you about DRAM. So it's up like $450 million in December. I mean that's the plan. Your DRAM share is like 6% of WFE share. So that's like $10 billion of like DRAM WFE right there. Is there something unique going on? I know there's some big new fabs that are starting to get equipped. Is it as simple as that? Or is maybe your inspection intensity going up in DRAM? I mean that's just -- I mean, I don't think I've ever seen you grow DRAM systems that much. So can you speak to that?

**Richard Wallace** (Executives):
Yes. Intensity is definitely going up. I mean there's no question that we started seeing this a while ago, and I think it took a little while for our customers to fully understand and appreciate the challenges of making these advanced devices. And given their supply shortages, the incremental value of yield. And so if you think back to how memory worked years ago, it's a pretty different world where anything they could squeeze out in terms of yield, but also the performance expectations are much higher as these go into these mostly commercial operations. So yes, it's intensity improving, and we see that continuing as we go forward.

**Bren Higgins** (Executives):
I think the greenfield opportunity is also driving a retooling of fabs and retooling in a way where, to Rick's point, our customers' profitability levels are pretty high. And so yield is equivalent to printing money in some ways. So I think there's renewed focus there. I think that the road maps are driving the need for more investment. The performance requirements are more stringent, particularly when you look at like HBM, for example, and less redundancy, I/O counts, logic in base die. All these things are driving opportunities in this part of the market.
In some products, we see intensity levels in DRAM that are similar to leading-edge logic. So the market is definitely shifting there, and I think the new fabs is an accelerant to our views of growth. If you look at the second -- in 2027, we'd expect overall memory to be about 60% of our -- of the business. And in an environment, where to Rick's point, we feel pretty confident about our ability to perform pretty well relative to the overall market. So it's definitely changing in terms of the way you used to think about the business historically and at least in terms of the DRAM impact.

**Operator** (Operator):
We'll take our next question from Krish Sankar with TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
Just follow up on the last question on DRAM. You said you're going to outperform WFE next year. The 2 big drivers this year was DRAM and leading-edge foundry. They will be the same next year. I understand. So is it mainly because greenfield in DRAM is coming in and leading-edge foundry logic is moving to 2-nanometer. Are those the 2 key specific drivers for outperformance next year besides advanced packaging? And then I have a follow-up.

**Richard Wallace** (Executives):
So Krish, let me clarify. You're saying if the drivers are the same, why would it be different? Is that your question?

**Sreekrishnan Sankarnarayanan** (Analysts):
Yes. I'm just wondering is the mix shift going from DRAM from brownfield to greenfield and logic going from 3 to 2?

**Richard Wallace** (Executives):
So I think, yes, those are drivers. But the other thing is we just weren't set up in the first half to be able to support assumptions, if you go back 12 months, we were not for the kind of growth rate we saw. In fact, we even talked about we thought the growth was going to be happening in '27, but '26 was going to be pretty flat. So it took a little while to get things going in '26, which is why you're seeing our accelerated growth now. The demand has been there and the demand will continue as the technology nodes continue. And as we said, packaging is growing and it will outgrow the market next year. So I think it was more -- it was not a demand question for us as much as in the first half of '26, a supply question.

**Bren Higgins** (Executives):
No, I think you covered it, Rick. Look, the new facilities will, I think, create an opportunity for us that will drive some incremental as customers are setting up a new facility in a market environment that is both challenging from a complexity point of view, but also where yield is critical.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got it. Super helpful. And then as my follow-up, I understand lead times are extending. But in general, like besides ASML, KLA was in this unique position where you always have long lead times. I'm just kind of curious, one of the views from some folks in the industry is that $300 billion could be the peak WFE a few years out. I'm just wondering from what you are seeing, given the fact that you have like better visibility than us, kind of like how high do you think this WFE can grow? Obviously, there's like wildcards like Terafab, but obviously, you're also specific to how good the yield of your customers are. I guess I'm just curious, from your vantage point, what do you see the WFE potential to get to?

**Bren Higgins** (Executives):
Well, I'm not going to guide a new number for 2030. Look, at Investor Day, we talked about $220 billion, plus or minus $20 billion view. And back then, where a lot of folks, I think, thought generally that was generally a middle-of-the-road kind of plan. I would say today, it looks like a very conservative one. So we're certainly more optimistic about higher levels of industry investment. We think the flow-through and thesis in terms of KLA's participation in that is the same. 
And as we think about these growth scenarios, certainly given the lead times on some of our products and the parts that go into them, we have to contemplate those in terms of preparing our supply chain for those outcomes. We are having deep conversations with our -- some of our key suppliers about our needs in 2029 and 2030 in that time frame. So we're trying to position the company to make sure that we can continue to drive the company consistent with the way we laid it out and support those higher-end scenarios that are being discussed in the industry.

**Operator** (Operator):
We'll take our next question from Stacy Rasgon with Bernstein Research.

**Stacy Rasgon** (Analysts):
So the first one, like to go back to that 2030 model. So I mean, you're basically there on WFE next year. You're there at the high end or maybe even a little above on the operating margin target. But what stops you in that WFE environment from getting to the revenue that you talked about in 2030, next year, at least on the equipment side, I understand maybe services and some of the other stuff takes a little more time to ramp up. But is it just supply? Is it like the mix of demand? Like why shouldn't I be looking at a 2030 model more into the '27 time frame given where we're running?

**Bren Higgins** (Executives):
Well, so there were assumptions underneath it. I mean, first, there was the growth rate assumption around service, which, to your point, we won't be there. That was based on an aggregate installed base growth that would contribute to that. You also have the non-semi PC part of the business and the expected growth rate there. Within semi PC, underneath the number was an expectation of share growth over the next few years of a few points and then overall share of market would slowly tick up to -- from 2025, which was about 7.5% of overall wafer equipment to closer to 9%. So we're not there yet. But in terms of how the financial model works underneath it, I don't see any reason why the financial model would not perform consistent with the way we laid it out because that growth is more demand from the same customers for a lot of the same products. So I think we feel pretty good about the way the financial model will perform. 
Obviously, there are things like share count and other things that go into an EPS assessment. But at least from a top line point of view, I think it will be more or less consistent with the way that I laid it out. I think there were some assumptions that were implicit in there that we're going to drive to over the next few years that we're not there yet. But in terms of the overall market and the current performance, I think that flows through.

**Stacy Rasgon** (Analysts):
Got it. My follow-up, maybe to dig into that financial model. So you talked about 40% to 50% incremental operating margin. I think you called that out in the shareholder letter as well. But again, you're already running even close to the high end of that range. So if you get operating leverage from here, it sort of implies that the incremental operating margin needs to be above where you're running today. So I mean maybe the high end of that or even higher. Is there any reason I shouldn't think about that incremental operating margin range would be structurally higher given where things are running right now?

**Bren Higgins** (Executives):
It depends a lot on year-to-year growth rates, right? So if you look at -- in a more normalized growth rate environment, we'll perform at the midpoint or so of the range. If you look at over the last year with revenue growth of 25% and you take the guidance we gave for Q4, that puts you slightly above the top end of the range. And if you think about 2030, given expectations for growth in 2030, I would expect we'll be beyond that. So it was more of a marker to give some sense to our shareholders and investors about how to think about how we're going to scale the company, what kind of leverage we will drive through the model. But if we're looking at growth rates for the whole company that are closer to 20%, then I would expect we'll perform more in line with the top end of the model or better. But that's just long term, how we think about it, how we make investment decisions, how we size it. And then if the industry turns out to be stronger, then that drives upside.

**Operator** (Operator):
We'll take our next question from Joe Quatrochi with Wells Fargo.

**Joseph Quatrochi** (Analysts):
I was curious, your CapEx, I think, this quarter was the highest I think I've ever seen it. I wonder if you could just kind of give us some color on what was driving that? Is there just also related to supply chain dynamics or something else?

**Bren Higgins** (Executives):
Well, in the quarter, we made a significant land purchase in India to build a new campus there, supporting our long-term growth. So that was a large portion of CapEx. Now I do expect our CapEx, I think as I laid out at Investor Day, I talked about 2% to 3% of revenue going forward, but of course, revenue is growing. But on an absolute dollar basis, I would expect our CapEx to trend up over the next few years, somewhere between $600 million and $800 million per year. As I said earlier, we're investing at every site. And so I would expect CapEx to trend north. That will be mostly around our capacity. There will be some things, obviously, we're doing in supply chain. But that's the big needle mover in the KLA space.

**Joseph Quatrochi** (Analysts):
And then the services business, I think you talked about operating at the high end of your long-term growth algo this year. Is there any reason that, that wouldn't be the case in 2027? Or how are you thinking about the growth in '27 for services?

**Bren Higgins** (Executives):
Yes. No reason to think that, that wouldn't be the case. I mean, given the growth in the industry and what we're adding to the installed base, that our systems are running at very high utilization, the value of yield in this environment. Service, I think, is -- in terms of the target range, we're likely to operate moving forward towards the higher end of the range.

**Operator** (Operator):
We'll take our next question from Melissa Weathers with Deutsche Bank.

**Melissa Weathers** (Analysts):
I wanted to go back to the supply chain side of things. You guys are -- as you said, you've been working on this for over a year. So -- and maybe some of your competitors are just now starting to see some more acute shortages. So can you just -- like what inning would you say we're in, in terms of you guys expanding your supply? Do you see risk of further, like, tightening on the supply chain? Or do you think we're kind of through the worst of it? Just where do you think we are in that process?

**Bren Higgins** (Executives):
Yes. I talked about this at Investor Day. I think when you look at our supply, given the nature of some of our components, that what drives our ability to ship is typically around optical components. And those have the longest lead time. Now we run into all kinds of small issues. But once we set the volumes get set by those high-end components. And so we just -- I think the supply chain team does an excellent job here managing all those little issues as they happen between the time that we get things scheduled and we ship tools. 
In an environment of very strong growth, I think everybody runs into challenges of working through hedges and buffer stock and excess inventory. And then when you start living hand to mouth in terms of what your suppliers can provide and there's a lot of demand there that it starts to create challenges. I think for KLA, we don't really compete for the things that matter the most to us. We don't compete with any of our competitors. We compete within KLA sometimes for those components. But once we have visibility there, it tends to be pretty reliable and then we manage all the small component issues that happen along the way.

**Melissa Weathers** (Analysts):
So I guess your December quarter outlook, is that supply constrained at all? Could that -- not that I'm complaining, but could that have been higher if you had more supply? And then same thing with the over $200 billion WFE outlook. Is that, like, you have line of sight to that supply at this moment? Or like, I guess, how unconstrained is the number?

**Bren Higgins** (Executives):
Yes, Melissa, I kind of live in reality here. I don't get wrapped up into what if. It's what can we ship and what -- how is our supply chain positioned for that, and that then translates into how we provide the guidance. As I said earlier, move rates on key components are increasing month by month. And so that informs not only what we expected to see in December, but how we're thinking about 2027. I would say over the course of this whole year, I could absolutely have shipped more. My demand was ahead of my supply. But I do think we're in a position where moving forward, we're seeing incremental supply come online, and that is informing the visibility and guidance that we've given.

**Richard Wallace** (Executives):
Yes. I think, Melissa, one thing to add, this is Rick. I think that for some customers, they can say that they want deliveries and then what they find is they've got delays themselves in terms of facilities. So it's not just the equipment, it's the readiness of the fabs. And so I think if you look out over time, could you ship? Yes, maybe, but it doesn't mean they can utilize it right away. So that's why I think the -- when people talk about can you be there to support the industry, it's really -- you need all the equipment suppliers to be able to do it. You need the facilities, you need to build. So it's longer than just can the equipment guys ship. So there's a couple of customers right now that have asked for deliveries and then they're on hold because they're waiting for their facilities. Does that make sense?

**Operator** (Operator):
We'll take our next question from Chris Caso with Wolfe Research.

**Christopher Caso** (Analysts):
I just want to ask a follow-on to the capacity question as well and maybe in 2 parts. And one is, as you look in the business and let's say, let's look into '28, do you think that the bottlenecks are more on the KLA side or more in your supply chain? And then for '28, I guess most of us are expecting a pretty significant acceleration in '28 or continued growth in '28 as customers have more clean room space. Are there any impediments to that, that you see given we've got some preparation time here?

**Richard Wallace** (Executives):
Yes. I think, again, if you go and look at the history of a lot of these build-outs, people can have these plans, but then they get into delays when they're building clean rooms. There can be delays in having enough power for those clean rooms. I mean if you look across the supply chain over the last several years, there have been plans that have been delayed over time and equipment can be part of it, but it's only part of it. So our customers are sending very clear messages that they want to bring on these additional fabs and to do these build-outs. But we have to kind of move in concert, which is why you often find like we're part of a group that will be at supplier days for all these customers, and they'll be talking about those expansion plans. So they can have -- right now, it's theoretical how big it's going to be. But as you get closer to it, we'll see it build out. So it's not as simple as we're going to be late because we're working very closely with those customers as they're building. 
As I mentioned, there's one customer right now that's desperate for more capacity and they can't take equipment because their clean room is delayed. And that's because they don't have -- so the bottleneck moves around. Bottleneck could be construction. It could be the fact that they can't get certain raw materials or they can't get power. So you kind of have to look at it collectively in terms of -- it's a little bit like the challenges associated with data centers. It's not just the data center, it's the power for the data center, they have it. So that's why I think, yes, this industry is going to keep growing. In some ways, it's going to prolong the rate of growth because it's harder to add on as much capacity as some people are envisioning for example, for 2028. But it does, I think, mean we're going to have a longer cycle in terms of the growth. 
So our motto is we're not going to be the constraint. We said we're not going to be the bottleneck. We might have periods where we're a little behind. As Bren said, we'd like to ship. But we're doing everything we can, working with our customers, with our suppliers so that KLA is not the bottleneck. It doesn't mean there won't be bottlenecks. It's just our goal is not to be the bottlenecks.

**Bren Higgins** (Executives):
And we can do anything inside the company generally within the time frame that gets established, within our long lead time components. And what I mean by that is that we can hire the people we need. We can drive the facility utilization. Obviously, CapEx decisions around new facilities is a long-term process, which is why we're making the investments. But you can also run extra shifts and so on to ensure that we're driving facility utilization. So we are never in a situation where we're the bottleneck to Rick's earlier point. So I feel pretty very good about what -- how KLA is positioned. And if we can do anything inside the company that within the time frame that gets established by our long lead time components.

**Christopher Caso** (Analysts):
Got it. That's a helpful clarification. As my follow-up, I'll ask about China, and it looked like it was up significantly in the quarter. I know that revenue tends to be lumpy. Can you talk about what your expectations are for China? What's embedded in the Q4 guidance and what your thoughts are for the China business as you head into next year?

**Bren Higgins** (Executives):
Yes, it will come down in Q4. As I said, actually, I think I've been saying this since March is I thought that China as a percent of the total would be in the high 20 percentile. So we'll call it somewhere between 27% and 29%. And I still believe that, that, therefore, implies that the fourth quarter is in that similar range given what we've done in the previous 3 quarters. So it did pop up a little bit in September. But China is growing at a much slower rate than the overall business. And so it's coming down as a percent. And I think in 2027, that will continue. I expect China will likely grow a little bit, but not at the same rate as the growth in wafer equipment outside of China. So we're probably operating somewhere, I would say, in the low 20 percentile in 2027. 
Now within our numbers, there's also our non-semi PC that also has business in China. There is more PCB type investment that happens in China, component inspection in China. So it probably skews the numbers a bit up a little bit, but it's a small percentage of the overall, so not much. So I think the numbers I provided give you, I think, enough directional clarity about where the business is today and where it's going.

**Operator** (Operator):
We will go next to Shane Brett with Morgan Stanley.

**Shane Brett** (Analysts):
First question is on advanced packaging. At your Investor Day, you mentioned that Kronos is the workhorse of packaging. We have the next 3 systems already ready. Just are your customers requiring higher sensitivity tools? And if so, can you talk about the competitive environment at these higher sensitivity levels?

**Bren Higgins** (Executives):
Well, in advanced packaging, it's been reflecting because of the move to more front-end-like processes. Most of it, to your point, has been in the macro products. And we think the road map for those products, we're well positioned there. You are seeing more hybrid bonding and logic devices, which is driving the need for greater levels of sensitivity. We also talked about that at Investor Day. So as you start to move from micron level sensitivity down to the 100-nanometer type sensitivity, it does drive the need for more advanced systems. 
So when we talk about our overall packaging exposure, the mix of systems is starting to trend more towards higher-end systems. So the macro products are still, to use your words, the workhorse, but we're seeing more laser scanning and even in some cases, some Gen 4 deployment for packaging requirements. So we think this part of the market continues to be an opportunity for KLA. We've been able to leverage a lot of the R&D that we've done across the more advanced platforms. And so we think we're very well positioned with proven products that can meet the higher-end requirements and our customers understand that capability well. So we think we're pretty well positioned in terms of the growth opportunities in that part of the market.

**Shane Brett** (Analysts):
Got it. And my follow-up is on logic. I know you assess node-to-node share gain after certain wafer start volumes installed. But internally, is there a preliminary expectation on your share gains from 2-nanometer to 1.4 nanometer? Are there any part of your product portfolio where you think the financial market would be surprised on just the magnitude of share gains?

**Bren Higgins** (Executives):
Yes. We think the trend is in the right direction. I mean one thing about the next-generation nodes is they're starting to tune those nodes for high-performance compute requirements. And those require some of the more advanced capabilities and more sampling steps because of the value of the die. So with high-performance compute, you have large die, they're very valuable, defect density is a challenge. You also have a very rich design environment. All those are good contributing factors. I don't have a point position to give you in terms of the directional trend, but we feel pretty good about the ability to continue to grow our share of the market node-to-node.

**Richard Wallace** (Executives):
And I think our relevancy with e-beam inspection capability and the linkage we have to our optical becomes more pronounced. And so not as much share as it is adoption, but those investments were made to really -- they'll show up more as we go to smaller designs.

**Operator** (Operator):
And we will take our final question from Timm Schulze-Melander with Rothschild & Co Redburn.

**Timm Schulze-Melander** (Analysts):
I had one for Rick and one for Bren. Maybe the first one, just comparing '27 to 2026. When you look at the CapEx that was spent on or is being spent on established nodes this year as a percent of the total market and you look forward to 2027, could you just maybe describe how that ratio changes? And then I had a follow-up.

**Bren Higgins** (Executives):
You see more investment in 2-nanometer. I mean, I think 2-nanometer and 3-nanometer investments will be a focus in logic, you'll see more there. You'll also see some investment in the next-generation nodes, so 1.4-nanometer. So it's different to have any of that, that more advanced investment, and it was more 3-nanometer centric in '26. So I think it sets up, I think, good for us constructively in terms of just more 2-nanometer and more leading edge investment in 1.4-nanometer.

**Timm Schulze-Melander** (Analysts):
Very clear. And maybe just -- and then maybe one on memory in 2027. You've discussed your engineering strategy about how you're going to address that memory kind of impact to your bill of materials. Can you just maybe talk about what your purchasing strategy is for '27 for memory, please?

**Bren Higgins** (Executives):
Well, certainly, our focus early on and through this year has been mostly around securing supply. Look, when things started to ramp in early '26, we felt pretty good about ensuring we had the supply, which was no easy feat generally because of the constraints in the overall industry. And as demand has strengthened, we've had to go out and buy more at higher prices, less concerned about supply, but certainly, we're exposed to the pricing market, and that's informing the commentary that we've provided. But I think from a supply point of view, we feel pretty good about the supply we've secured to meet the requirements we have going forward.

**Operator** (Operator):
This does conclude our question-and-answer session. I'd like to turn the program back over to Kevin Kessel for any closing remarks.

**Kevin Kessel** (Executives):
Yes. Thank you. Thank you, everyone, again, for your interest in KLA. We know it's a very busy earnings day, busy earnings week. So we appreciate it. If we didn't get to your questions, hopefully, we can connect here after the call in our callback. And with that, I'll turn it back to the operator to formally close out the call.

**Operator** (Operator):
Thank you. This concludes the KLA Corporation September Quarter 2026 earnings call and webcast. Please disconnect your line at this time, and have a wonderful day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### KLAC_Q4_2026_Earnings_Call_20260728.md
- 2026-07-28｜CFO｜guidance：FY26 九月季營收財測 $4B ±$200M（原話："revenue of $4 billion, plus or minus $200 million."）
- 2026-07-28｜CFO｜guidance：九月季毛利率財測 62.5% ±1pp（原話："forecasted to be 62.5%, plus or minus 1 percentage point."）
- 2026-07-28｜CFO｜guidance：九月季 non-GAAP EPS 財測 $1.16 ±$0.10（原話："EPS is expected to be $1.16, plus or minus $0.10"）
- 2026-07-28｜CFO｜guidance：九月季毛利率財測較上季財測高 75bp，管理層歸因於營收成長的營運槓桿（原話："it is up 75 basis points from gross margin"）
- 2026-07-28｜CFO｜guidance：日曆 2026 WFE（含先進封裝）預期上修至 150 億美元出頭區間，前次為 140 億以上（原話："$150 billion range in calendar 2026, up from our prior"）
- 2026-07-28｜CFO｜guidance：2026 下半年營收較上半年成長約 20%（原話："over the first half to be approximately 20%"）
- 2026-07-28｜CEO｜guidance：預期 2026 下半年動能加速、2027 持續顯著成長（原話："significant growth to continue in calendar 2027."）
- 2026-07-28｜CFO｜guidance：2027 WFE 市場共識約 1,900 億美元，管理層稱換算為約 20% 中段成長（原話："that's somewhere in and around the $190 billion range."）
- 2026-07-28｜CFO｜guidance：$190B 對應 mid-20s 成長率，與 2026 相近（原話："$190 billion or so translates into a mid-20s type"）
- 2026-07-28｜CEO｜guidance：先進封裝製程控制系統 2026 營收約 $1.1B，年增逾 70%（原話："$1.1 billion in calendar 2026, up more than 70%"）
- 2026-07-28｜CEO｜guidance：Specialty Process、PCB、元件檢測合併產品 2026 預期成長逾 25%（原話："grow over 25% in calendar 2026, we are encouraged"）
- 2026-07-28｜CFO｜guidance：服務業務長期目標成長 13-15%，今年在區間底部，預期明年朝高端（原話："This year, we're right now at the bottom of that range."）
- 2026-07-28｜CFO｜guidance：管理層估計 backlog/RPO 約 $125 億，且預期持續成長（原話："backlog would be at about $12.5 billion"）
- 2026-07-28｜CFO｜guidance：半導體製程控制業務預期成長比公司整體快至少數個百分點（原話："it will grow at least a few points"）
- 2026-07-28｜CFO｜margin：Q 毛利率 62.4%，主因較有利的服務組合與製造規模，抵銷記憶體價格與關稅（原話："Gross margin was 62.4%."）
- 2026-07-28｜CFO｜margin：本季增量營業利益率 59%（原話："Incremental operating margin in the quarter was 59%."）
- 2026-07-28｜CFO｜margin：記憶體採購價格造成的毛利率逆風（原話："headwinds as related to memory pricing."）
- 2026-07-28｜CFO｜margin：管理層表示記憶體逆風影響可能略多於 100bp（原話："It's probably a little bit more than that."）
- 2026-07-28｜CFO｜margin：2026 全年毛利率原指引 62% 上下，本次稱將高於此（原話："gross margins likely being in the 62%, plus or minus"）
- 2026-07-28｜CFO｜margin：長期毛利率模型為 63.5% ±500bp，並稱增量毛利率 60-65%（原話："63.5%, plus or minus 500 basis point view"）
- 2026-07-28｜CFO｜margin：九月季營業費用約 $690M，之後數季每季增 $15-20M（原話："grow by roughly $15 million to $20 million sequentially"）
- 2026-07-28｜CFO｜margin：長期增量營業利益率模型 40-50%（原話："deliver 40% to 50% incremental operating margin leverage"）
- 2026-07-28｜CFO｜margin：記憶體逆風預期延續至明年，之後定價有望由逆風轉為順風（原話："memory headwinds we're experiencing today likely continues"）
- 2026-07-28｜CFO｜margin：承上，預期定價正常化（原話："start to see some normalization on the pricing front"）
- 2026-07-28｜CFO｜margin：服務收入約 80% 為合約型（原話："80% of revenue is contract-based"）
- 2026-07-28｜CEO｜commitment：新產品推出時才做新定價決定；既有產品以其他方式分享價值（原話："that's when new pricing decisions get made."）
- 2026-07-28｜CFO｜commitment：對 Arcuri 追問：已接單後難以改價，漲價主要靠新產品（原話："hard to go back to your customers after you've taken orders"）
- 2026-07-28｜CEO｜commitment：管理層稱正增加產能以支應預期需求（原話："we are adding capacity to support expected demand"）
- 2026-07-28｜CFO｜commitment：願意承擔為維持產能彈性的成本（原話："we will take the cost of that flexibility"）
- 2026-07-28｜CFO｜commitment：願意在特定產品類型押注庫存（原話："I'm willing to make bets from an inventory point of view"）
- 2026-07-28｜CFO｜commitment：與關鍵供應商洽談 2029 年以後的產能協議（原話："our needs, we believe, in the 2029 and beyond time frame."）
- 2026-07-28｜CFO｜commitment：2030 目標模型：KLA 市占較 2025 增加 150bp ±25bp（原話："150 basis points, plus or minus 25 basis points"）
- 2026-07-28｜CEO｜commitment：若市場遠高於模型假設，管理層稱公司將超越 2030 模型（原話："then we would exceed the model that we laid"）
- 2026-07-28｜CEO｜commitment：管理層稱目前不會重設 2030 目標（原話："we're in no position to reset anything as it pertains to"）
- 2026-07-28｜CFO｜risk：2026 上半年曾遇長交期物料供應短缺（原話："some supply chain shortages as it relates to some of our"）
- 2026-07-28｜CFO｜risk：光學元件等長交期項目擴產需 12-24 個月（原話："it can take 12 to 24 months to"）
- 2026-07-28｜CFO｜risk：晶圓廠空間受限（原話："fab space limitations, we continue to see the market"）
- 2026-07-28｜CFO｜risk：部分產品交期可達 18-24 個月（原話："it can be closer to 18 to 24 months."）
- 2026-07-28｜CFO｜risk：整體交期約 12 個月（原話："are in about the 12-month range, but on certain"）
- 2026-07-28｜CEO｜competition：製程控制為高混合低量市場，管理層稱公平競爭下表現佳（原話："we're allowed to compete, we do quite well"）
- 2026-07-28｜CEO｜competition：管理層否認競爭環境有變，稱為淨市占增加者（原話："we're anything but net share gainers"）
- 2026-07-28｜CFO｜competition：競爭對手能出貨進中國晶圓廠而 KLA 不能（原話："China that we haven't been able to ship into."）
- 2026-07-28｜CEO｜competition：e-beam 等原市占較低市場出現正向動能（原話："We're definitely seeing positive momentum in markets"）
- 2026-07-28｜CFO｜product：HBM 部分產品的製程控制強度可媲美先進邏輯（原話："intensity levels that are rivaling what we see in advanced"）
- 2026-07-28｜CFO｜product：先進封裝市場成長預期由年初約 20% 升至 30% 中高段（原話："the market is kind of a mid- to high 30s growth"）
- 2026-07-28｜CFO｜product：Orbotech 相關業務長期 CAGR 中段約個位數高段（原話："somewhere in the high single-digit range"）
- 2026-07-28｜CFO｜customer：九月季半導體客戶中晶圓代工/邏輯占比預計約 73%（原話："forecasted to increase to approximately 73%"）
- 2026-07-28｜CFO｜customer：2026 全年晶圓代工/邏輯占系統營收約 65% 上下（低至中 60%）（原話："closer to 65-ish percent, so call it kind of low"）
- 2026-07-28｜CEO｜customer：本季服務營收 $820M（原話："KLA Services delivered $820 million revenue"）
- 2026-07-28｜CFO｜capital_allocation：本季回饋股東 $876M（原話："KLA returned $876 million to shareholders"）
- 2026-07-28｜CFO｜capital_allocation：過去 12 個月資本回饋總額 $3.3B（原話："total capital returns were $3.3 billion"）
- 2026-07-28｜CFO｜capital_allocation：已投資營運資金與設施以支應成長（原話："meaningful investments in our working capital and facilities"）

### KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 重申 3 月季度財測：營收 33.5 億美元、non-GAAP EPS 9.08 美元。（原話："revenue at $3.35 billion, non-GAAP diluted EPS of $9.08"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 說明 WFE（含先進封裝）預期 1,350–1,400 億美元，並提到先前的「30 多%中段」輪廓。（原話："$135 billion to $140 billion. We talked about a mid-30s"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 說 2026 全公司營收年增預期落在高個位數以上的「高十幾%」。（原話："somewhere in the high teens in terms of year-over-year"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 說半導體製程控制系統成長會比全公司快。（原話："process control systems growth should be faster than that"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：Q&A 中 CFO 補充 Semi PC 2026 成長將接近 20%。（原話："Semi PC will be closer to 20%"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 說客戶對 2027 的能見度很高，並表示可看 12–24 個月。（原話："visibility 12 to 24 months out is really uncommon"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 表示 2027 產業 WFE 年增率預期與 2026 相近或更高。（原話："perhaps even higher than what we're seeing in 2026"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 在開場說暫不談上下半年的拆分，等 6 月季度再說。（原話："really want to get into it at this point"）
- 2026-03-12｜Richard Wallace (CEO)｜guidance：2030 目標：營收 260 億美元，區間正負 25 億。（原話："$26 billion in 2030 revenue, plus or minus $2.5 billion"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：2030 目標 non-GAAP EPS 84 美元，並持續產生強勁自由現金流。（原話："EPS of $84 and should continue to drive strong free cash"）
- 2026-03-12｜Richard Wallace (CEO)｜guidance：2030 模型假設的市場口徑：WFE 加封裝規模 2,150 億美元。（原話："We're showing $215 billion"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 拆解 2030 模型：半導體營收年增 11%，WFE 約 12%。（原話："semiconductor revenue is growing 11%, that WFE will grow"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 拆解 2030 模型：半導體製程控制系統年複合成長 16.5%，對比產業 12%。（原話："semi PC systems, 16.5% CAGR against"）
- 2026-03-12｜Brian Lorig (Service)｜guidance：服務業務成長率目標由 12–14% 上調至 13–15%。（原話："from 12% to 14% to 13% to 15%, which means at the upper"）
- 2026-03-12｜Brian Lorig (Service)｜guidance：服務營收目標：區間上緣下 2030 年接近 60 億美元。（原話："revenue to nearly $6 billion and at the upper end of the"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：2030 模型假設：晶圓代工/邏輯占比 60% 以上（下緣）。（原話："We expect foundry logic to be 60% plus"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2030 目標毛利率 63.5%，區間正負 50 bps。（原話："63.5% gross margin, plus or minus 50 basis points"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：CFO 說 2030 模型已吸收約 50 bps 的關稅逆風。（原話："basis point headwind related to tariffs"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2030 營業利益率目標 45–47%（中位 46%，對比目前中位 42%）。（原話："translates into 45% to 47%, so 46% at the midpoint"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2030 費用率假設：R&D 約 11%（上一版計畫為 13%）。（原話："we think the R&D stays about 11%"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：SG&A 費用率目標由約 8.5–9% 降到約 7%。（原話："SG&A basically comes down from where we were around 8.5%"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2025 營業利益率 43.6%，高於當時 41–43% 的目標區間。（原話："We said our target range was 41% to 43%"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2022–2025 增量營業利益率 51%，略高於模型上緣。（原話："incremental operating margins at 51%, so slightly ahead"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：增量毛利率相對 2022–2025 基準預期再改善約 1.3 個百分點。（原話："1.3 points of improvement in incremental gross margins"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：CFO 指出服務毛利率較低，但隨系統成長與增量改善，對整體毛利的拖累會減輕。（原話："Service carries a lower gross margin."）
- 2026-03-12｜Ahmad Khan (Systems)｜margin：2025 全公司毛利率 62.8%，CFO/系統總裁以此作為產品差異化指標。（原話："62.8% overall KLA gross margin"）
- 2026-03-12｜Richard Wallace (CEO)｜margin：CEO 說明管理市占率時以毛利率設限。（原話："but we constrain market share by gross margin"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：宣布第 17 年連續調升股利，季配息由 1.90 美元升到 2.30 美元（+21%）。（原話："a 21% increase to $2.30 per quarter from"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：新增 70 億美元庫藏股授權，加上既有餘額合計約 110 億美元。（原話："additional share repurchase authorization of $7 billion"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：2030 資本回饋目標：占自由現金流 90% 以上（先前 85% 以上）。（原話："greater than 90% of the free cash flow we'll generate"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：股利政策：每年配息占自由現金流 25–30%。（原話："consistent cadence of 25% to 30% of the free cash flow we"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：2026–2030 的資本運用以庫藏股為主。（原話："repurchases as we deploy that cash"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：槓桿目標：總槓桿 1.5–2 倍，目前約 1 倍；營運所需現金 40–50 億美元。（原話："target at 1.5 to 2x gross leverage, we're about 1x today"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：2022 以來流通股數下降約 18%。（原話："drove our shares outstanding down about 18%"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：已投入約 2.5 億美元擴充供應商產能。（原話："invested about $250 million over the last couple of years"）
- 2026-03-12｜Richard Wallace (CEO)｜commitment：CEO 表示現任管理層曾承諾 2019 年投資人日目標並達成。（原話："committed to our 2019 Investor Day and hit it"）
- 2026-03-12｜Bren Higgins (CFO)｜commitment：CFO 回顧上一版目標：市占提升目標 100 bps，實際超過 150 bps。（原話："We improved it by over 150"）
- 2026-03-12｜Ahmad Khan (Systems)｜commitment：系統總裁：2030 製程控制占 WFE 比重由 7.4% 升至約 9%。（原話："by 2030, we're assuming that it's going to get to around 9%"）
- 2026-03-12｜Bren Higgins (CFO)｜commitment：CFO：2030 計畫再取得 150 bps 的市占。（原話："We're going to gain another 150 basis points of share"）
- 2026-03-12｜Bren Higgins (CFO)｜commitment：CFO 稱對外計畫與內部計畫與激勵機制一致。（原話："There's no daylight between the external plans"）
- 2026-03-12｜Richard Wallace (CEO)｜commitment：CEO 稱管理層激勵以相對自由現金流衡量。（原話："It's on relative free cash flow"）
- 2026-03-12｜Richard Wallace (CEO)｜commitment：CEO 形容 2030 目標設定偏保守，並說這次不是「不同」而是規模更大。（原話："We're generally pretty conservative"）
- 2026-03-12｜Richard Wallace (CEO)｜competition：CEO 稱製程控制市占為最近競爭對手的 6.5 倍（7 年前為 4 倍）。（原話："we're now 6.5x our nearest"）
- 2026-03-12｜Ahmad Khan (Systems)｜competition：系統總裁給出市占口徑：製程控制市占 56.5%，自 2021 年起上升 2 個百分點。（原話："We are now at 56.5% share, up 2% since 2021."）
- 2026-03-12｜Richard Wallace (CEO)｜competition：CEO 說競爭對手無法像 KLA 在每個子系統做客製化。（原話："Our competitors do not. They can't afford it."）
- 2026-03-12｜Richard Wallace (CEO)｜competition：CEO 回應光罩檢測 DUV/e-beam/actinic 路線之爭：稱市占軌跡與競爭對手宣稱難以對上。（原話："it would be hard to reconcile the two"）
- 2026-03-12｜Richard Wallace (CEO)｜competition：CEO 對光學與 e-beam 何者勝出的辯論表示從未定論；去年 Gen 4 出貨多於 Gen 5。（原話："Last year, we sold more Gen 4 than Gen 5."）
- 2026-03-12｜Bren Higgins (CFO)｜competition：CFO 指出先進封裝市場中，傳統前段設備廠都在瞄準此機會。（原話："all the traditional front-end players are targeting"）
- 2026-03-12｜Ahmad Khan (Systems)｜competition：系統總裁說明光罩檢測需偵測 100% 缺陷，因此需組合多種系統。（原話："it's very critical that you detect 100% of the defects"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：e-beam 業務由 7,500 萬–1 億美元成長至約 4 億美元（不含光罩 e-beam）。（原話："Today, we are at $400 million"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：2025 先進封裝營收 9.5 億美元，並稱製程控制市占第一。（原話："$950 million in advanced packaging revenue in 2025"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：資料分析軟體業務目前規模約 2.5 億美元。（原話："$250 million, software business that is doing quite well"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：DRAM 設備市場成長 2 倍，KLA DRAM 營收成長 3 倍；2025 增量強度貢獻 4.5 億美元。（原話："DRAM wafer equipment market went up by 2x"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：系統總裁說 KLA 正在開發 actinic 光罩檢測系統。（原話："we're developing actinic inspection also"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：系統總裁說目前沒有 DUV 與 e-beam 抓不到的缺陷類型問題。（原話："Currently, we don't have a type of defect problem"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：Q&A 中系統總裁量化良率價值：良率每提升 1% 對應客戶至少 1.5 億美元利潤。（原話："could lead to at least $150 million in profit"）
- 2026-03-12｜Brian Lorig (Service)｜product：服務業務：設備中位退役年限由 10 年升至 24 年以上。（原話："increased from 10 years to more than 24 years"）
- 2026-03-12｜Brian Lorig (Service)｜product：服務合約占服務營收比重由 2005 年約 60% 升至 80% 以上。（原話："Today, we're more than 80%"）
- 2026-03-12｜Brian Lorig (Service)｜product：裝機基礎中個別機台兩年期間有營收的經常性比率。（原話："individual tools over a 2-year period recurs in revenue"）
- 2026-03-12｜Ahmad Khan (Systems)｜customer：系統總裁指新型光罩電子束檢測機是與 TSMC 合作開發。（原話："is TSMC because we have published a paper recently"）
- 2026-03-12｜Richard Wallace (CEO)｜customer：CEO 稱客戶結構轉向超大規模雲端業者，設計案數量大增。（原話："another hyperscaler that announced 4 new designs"）
- 2026-03-12｜Richard Wallace (CEO)｜customer：CEO 轉述前段客戶要求把 KLA 產品線改成可用於封裝，並稱不會因封裝打折。（原話："we definitely need you to take your portfolio"）
- 2026-03-12｜Richard Wallace (CEO)｜customer：CEO 稱客戶的客戶也因供給受限而感到挫折。（原話："they're all frustrated that they're supply constrained"）
- 2026-03-12｜Richard Wallace (CEO)｜customer：CEO 說 AI 贏家是誰不影響 KLA。（原話："KLA wins no matter who wins"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：開場提到出口管制對服務業務有影響。（原話："despite some of the export control effects on service"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：CFO 說上一輪服務成長在目標區間內，但受進廠限制干擾。（原話："had some disruption related to access to fabs"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：供應鏈：材料採購到出貨的自然時間柵約 60 週。（原話："the natural time fence is almost 60 weeks"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：CFO 說明上半年產能受限於前置時間，下半年彈性較大。（原話："we have a lot more flexibility and capacity"）
- 2026-03-12｜Richard Wallace (CEO)｜risk：被問及中東局勢是否造成供應中斷，CEO 回答目前沒有。（原話："Not currently any disruption."）
- 2026-03-12｜Bren Higgins (CFO)｜risk：CFO 說明產業結構轉向後，傳統（legacy）投資將占 WFE 的 25–30%。（原話："the legacy business will be 25% to 30% of overall WFE"）
- 2026-03-12｜Richard Wallace (CEO)｜product：敘事變化：CEO 針對「KLA 不是記憶體玩家」的看法表示不再成立（HBM）。（原話："think KLA is not a memory player, it's not true"）
- 2026-03-12｜Bren Higgins (CFO)｜customer：敘事變化：CFO 說先進封裝上一輪投資人日沒有談過。（原話："We didn't talk about it before"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：敘事變化：記憶體占比上升後，CFO 稱業務對產品組合的敏感度降低。（原話："it moves from that into the low 60 range"）
- 2026-03-12｜Bren Higgins (CFO)｜customer：敘事變化：記憶體與封裝客戶過去的「計費」服務心態正在改變。（原話："started to change the service mindset"）

### 問答異常語氣（迴避／改口／保留）
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Arcuri：為何不能漲價抵銷記憶體成本（ASML 都在漲 EUV 價）｜答法：未正面回答為何做不到，改談新產品時才調價、已接單難改價，並說 'pretty comfortable with our view'
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Arcuri：12 月季隱含毛利率是否同樣持平｜答法：未給數字，稱看產品組合、'could be a little bit higher, too'，回到長期 60-65% 區間
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Krish：是否漲價、何時生效、對毛利影響｜答法：Rick 稱有討論分享價值，未給漲價幅度或生效時間
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Rasgon：按最樂觀情境擴產是什麼意思｜答法：Rick 稱前述說法 'maybe it was a little unclear'，重新澄清為僅支撐產業能支撐的情境
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Malik：是否參與 SpaceX/Terafab 專案｜答法：拒答具體客戶合作，僅稱創新者都會找上 KLA
- KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md｜問：Rasgon：2026 受無塵室限制，為何 2027 WFE 成長不會更快？KLA 2027 是否會超越 WFE？｜答法：CFO 回到「至少一樣快」，改談動能與客戶參與、未給 2027 數字，說「等到那時再看」。
- KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md｜問：Rasgon：2026 高十幾% 是否意味下半年對上半年約成長 20%？｜答法：CFO 先說等季度結束與 6 月財測，再表示下半年相當強、Semi PC 約 20%，並加上「看客戶動能是否改變」的保留語氣，沒有給半年對半年數字。
- KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md｜問：Muse：2030 市占再增 150 bps 中有多少來自先進封裝？客戶是否願意為封裝付更高價？｜答法：CEO 與系統總裁以客戶要求的軼事和技術論述回答；CFO 明說不會給具體市占數字，也未直接回答封裝 ASP 溢價問題。
- KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md｜問：Arya：若記憶體占比擴大，對 KLA 市占成長潛力的影響？｜答法：CFO 說「敏感度降低」，改談產業效率、legacy 占比與 R&D 圖，未量化記憶體占比上升對市占的影響。

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
{"date":"20260729","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"製程控制份額守住或擴張，且服務業務維持 13-15% 複合成長（結構性假設：KLA 是產業複雜化的收租者）"},{"id":"H2","text":"設備支出上行延續至 2028，FY2027/FY2028 EPS 路徑兌現（成長兌現的操作性假設）"},{"id":"H3","text":"入場倍數自 37x 向 30x 以下正常化——這是進場條件，不是業務假設（估值修復的市場假設）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"設備支出在 2028 進入消化期，且市場提前 2-4 季反應。SEMI 2026 年中預測 WFE 2026 +23.1%、2027 +21.8%、2028 +14.1%——三年累計成長逾 70%，屆時的絕對基數（約 $200B）已接近管理層 2030 模型假設的 $215B，等於整輪循環被提前三年跑完。獨立研究亦指出 2028-2029 存在實質過剩情境（Samsung／SK 海力士新廠 2027 下半年才量產、Micron 愛達荷廠 2027 年中投產，供給集中在 2028 落地）。"},{"id":"R2","text":"出口管制與關稅升級。已知量化影響：華虹禁運等管制未來 5 季減少 $300-350M 營收；Section 232 對特定先進半導體品項 25% 關稅（2026-01-15 生效）已列入毛利率逆風。未知風險是管制範圍自先進節點外溢至成熟節點——中國仍占營收 26%。"},{"id":"R3","text":"虛擬量測與客戶自建檢測能力的長期侵蝕。晶圓廠與大型設備商推進以製程機台感測資料 ＋ AI 模型取代部分實體量測步驟；同時 Applied Materials 在本季度被分析師點名「談製程控制的著力增加」。這是慢變數，不會在一兩季顯形，但會逐年壓縮 KLA 在成熟節點與非關鍵層的可服務市場。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"FY27共識本益比≤34x（約$175）分批starter；≤30x（約$154）加碼；或FY27/FY28共識3個月上修≥10%使同價位倍數下修","irr_base_pct":6.2,"ev5y_pct":35.6,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":3.3,"ev5y_pct":35.6,"irr_base_pct":6.2,"max_dd_pct":-60.0,"bull_5y_price":366.0,"bear_5y_price":119.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"FY27共識本益比≤34x（約$175）分批starter；≤30x（約$154）加碼；或FY27/FY28共識3個月上修≥10%使同價位倍數下修","price_at_dd":190.8,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
