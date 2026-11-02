你是 stock-analyst **v20 判斷 agent**，標的 MA（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MA","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenue_gaap","label":"Net revenue (GAAP)","value":9807,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 3Q26 Earnings Release"}},{"id":"f_kpi1_adjusted_non_gaap_operat","label":"Adjusted (non-GAAP) operating margin","value":60.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 3Q26 Earnings Release"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":59.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 3Q26 Earnings Release"}},{"id":"f_kpi3_free_cash_flow_9m_ytd_q3","label":"Free cash flow (9M YTD，Q3 單季未揭露)","value":10718,"period":"9M FY2026（至 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"9M FY2026（至 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 3Q26（OCF 11,859 − capex 1,141 推算）"}},{"id":"f_kpi5_adjusted_diluted_eps","label":"Adjusted diluted EPS","value":5.31,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 3Q26 Earnings Release"}},{"id":"f_kpi6_management_guidance","label":"Management guidance","value":"Q4 與全年淨營收（cc、不含 inorganic）成長 high end of low double digits","period":"Q3 FY2026 法說會（2026-10-29）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026 法說會（2026-10-29）","citation":"Q3 2026 earnings call transcript（CFO 準備稿）"}},{"id":"f_kpi7_purchase_volume_cross_bo","label":"Purchase volume / cross-border volume growth (local currency)","value":"9% / 11%","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 3Q26 Earnings Release"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ma_gross_margin_pct","label":"MA 毛利率","value":78.42,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ma_operating_margin_pct","label":"MA 營業利益率","value":60.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ma_fcf_margin_pct","label":"MA FCF 利潤率","value":42.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_gross_margin_pct","label":"V 毛利率","value":79.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_operating_margin_pct","label":"V 營業利益率","value":65.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_fcf_margin_pct","label":"V FCF 利潤率","value":44.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_axp_fcf_margin_pct","label":"AXP FCF 利潤率","value":19.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cof_fcf_margin_pct","label":"COF FCF 利潤率","value":45.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COF.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pypl_gross_margin_pct","label":"PYPL 毛利率","value":45.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pypl_operating_margin_pct","label":"PYPL 營業利益率","value":18.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pypl_fcf_margin_pct","label":"PYPL FCF 利潤率","value":18.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_9m_ytd","label":"SBC 占營業利益 (9M YTD)","value":3.2,"period":"9M FY2026（至 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"9M FY2026（至 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 3Q26（SBC 525M ÷ GAAP 營業利益 16,356M 推算）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":638.01,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":29.18,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":70.74,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.4,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.96 → 20.04）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.26,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.07 → 23.13）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.34,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（26.85 → 26.94）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":20.04,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":23.13,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":26.94,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.93,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 19.66 → 20.04（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":33.39,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":15.32,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":15.69,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":31.84,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 20.04，分子＝快照價 638.01","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.545,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":13474.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 23938.0、現金 10464.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":871.18,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":569293.07,"period":"2026-11-02","unit":"USD m","basis":"市值 555819.07 ＋ 淨負債 13474.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":37348.49,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（34 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":42060.51,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（34 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":15.24,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 638.01 / W52 538.68 / W104 542.77 / W250 451.48 / W250 13週斜率 0.94%"},{"id":"f_ma_w52","label":"52 週均線","value":538.68,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":542.77,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":451.48,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.94,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出競爭者含 Visa、AmEx、JCB、銀聯、Discover，並指即時帳戶對帳戶支付系統可能侵蝕 P2M/P2P 份額；部分對手在特定地區份額高於 MA","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"As these real-time account-based propositions mature, we face a possible increase in competition for our existing domestic person-to-merchant (“P2M”) and person-to-person (“P2P”) transaction market share.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：部分客戶與對手有近乎排他關係，且 MA 自這些客戶取得可觀營收，客戶可能將業務轉給對手","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"Furthermore, we earn substantial revenue from customers with nearly-exclusive relationships with our competitors. Such relationships could provide advantages to the customers to shift business from us to the competitors with which they are principally aligned.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Nilson：2025 年美國 Visa 購買量 7.028 兆美元（佔 70.38%），MA 2.958 兆美元、成長 6.3%，略低於 Visa 的 6.8%","source":"Nilson Report, Mastercard and Visa cards in the US 2025（經搜尋摘要轉述）","url":"https://nilsonreport.com/articles/mastercard-and-visa-cards-in-the-us-2025/","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"MA 收購 BVNK 並開放結算予穩定幣，穩定幣被視為潛在替代威脅，MA 採參與策略","source":"Decrypt: Mastercard Brings Its Fraud-Fighting Tools to Stablecoin Payments","url":"https://decrypt.co/381365/mastercard-brings-its-fraud-fighting-tools-to-stablecoin-payments?amp=1","excerpt":"Mastercard said Stablecoin Security builds on existing tools like Crypto Credential and Crypto Secure, and that it plans to extend the product’s reach in 2027, including through BVNK.","as_of":"2026-10-19","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因子：Mastercard 多數客戶關係非排他，客戶可依合約重新評估承諾，也可能自行開發競爭服務。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"Many of our customer relationships are not exclusive. Our customers can reassess their future commitments to us subject to the terms of our contracts, and they separately may develop their own services that compete with ours.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 競爭段列出數位錢包等金融科技可用內部帳戶轉帳、帳戶對帳戶即時支付網路處理付款，不經卡網路。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"Many of these providers have developed payments systems focused on online activity in e-commerce and mobile channels (in some cases, expanding to other channels), and may process payments using in-house account transfers, real-time account-based payments networks or global or local networks, in addition to card.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Lloyds Banking Group 與 Visa 續約擴大，約 1000 萬張信用卡與簽帳卡由 Mastercard 轉至 Visa。","source":"Banking Exchange: Lloyds to Transfer 10 Million Cards to Visa","url":"https://www.bankingexchange.com/news-feed/item/10023-lloyds-to-transfer-10-million-cards-to-visa","excerpt":"Lloyds to Transfer 10 Million Cards to Visa The majority of consumer and commercial credit cards will migrate to Visa by 2026 06/26/2024 - 10:48 | Written by Banking Exchange staff Tweet Approximately 10 million Lloyds Bank Group credit cards will transition from Mastercard to Visa over the next two years, as part of a newly secured","as_of":"2024-06-26","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"前五大客戶 2025 年淨營收約 69 億美元，占總淨營收 21%；失去任一客戶或其重要卡方案可能衝擊營收。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"In 2025, the net revenue from these customers was approximately $6.9 billion, or 21%, of total net revenue. The loss of any of these customers or their significant card programs could adversely impact our revenue.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2023–2025 年沒有任何單一客戶占淨營收超過 10%。","source":"SEC EDGAR 10-K FY2025 Item 8 附註","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"Mastercard did not have any individual customer that generated greater than 10% of net revenue in 2025, 2024 or 2023.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"風險因子揭露營收集中於前五大客戶，失去其中任一家可能有重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"a significant portion of our revenue is concentrated among our five largest customers. Loss of business from any of our large customers could have a material adverse impact on our overall business and results of operations.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2026 年 6 月發債文件載明 Mastercard 發行人評等為 Moody's Aa3／S&P A+，展望皆穩定；搜尋未見 2026 年評等調降。","source":"SEC EDGAR Form FWP（2026-06 債券定價）","url":"https://www.sec.gov/Archives/edgar/data/0001141391/000119312526257761/d148721dfwp.htm","excerpt":"Issuer Ratings*: Aa3 / A+ by Moody's / S&P (stable / stable)","as_of":"2026-06-30","retrieved_at":"20261102","affects":["valuation","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MA 2026 Q2：GDV 本幣+8%、跨境+12%，跨境含委內瑞拉美元可得性帶動的一次性因素；管理層預期7月跨境非旅遊CNP成長趨緩；全年淨營收指引低十位數成長；過去12個月淨增逾2.3億張卡。","source":"MarketBeat/Nasdaq Q2 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/mastercard-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261102","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MA 2026 Q3（10/29公布）：淨營收約98億美元+14%，GDV本幣+7%、購買量+9%、跨境+11%、交易筆數+9%；加值服務+19%；回扣與誘因+18%。","source":"Mastercard 3Q26 earnings release (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001141391/000114139126000122/ma09302026-exx991xearnings.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026 net revenue up 14%, GDV +7%, cross-border +11%","source":"Mastercard 3Q26 Earnings Release","url":"https://s25.q4cdn.com/479285134/files/content_files/3Q26-Mastercard-Earnings-Release.pdf","excerpt":"was attributable to growth in our payment network and value-added services and solutions. ▪ Payment network net revenue increased 11%, as reported and on a currency-neutral basis. Primary drivers of the increase were as follows: • Gross dollar volume growth of 7% on a local currency basis to $3.0 trillion. • Cross-border volume growth of 11% on a local currency basis.","as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Mastercard 10-K FY2025 披露其為多起民事訴訟及監管調查的被告，包括指控違反競爭與反壟斷法者；若在反壟斷主張下敗訴可能面臨三倍賠償，對業務與經營成果造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"We are a defendant in a number of civil litigations and regulatory proceedings and investigations, including among others, those alleging violations of competition and antitrust law and those involving intellectual property claims","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"DOJ 反壟斷司對 Mastercard 美國簽帳金融卡業務發出 CID，Mastercard 配合調查；10-Q 列示 ATM 附加費訴訟與歐盟執委會資訊請求","source":"Mastercard 10-Q 2026-03-31","url":"https://www.sec.gov/Archives/edgar/data/0001141391/000114139126000031/ma-20260331.htm","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Visa/Mastercard 與商家和解：平均有效信用卡交換費降低10bp五年，並限制附加費；參議員 Durbin 稱其不足，信用卡競爭法案2026-01重新提出","source":"Digital Transactions / Payment Expert","url":"https://paymentexpert.com/2025/11/18/us-senator-attacks-visa-and-mastercard-swipe-fee-deal-as-falling-short/","excerpt":null,"as_of":"2025-11-18","retrieved_at":"20261102","affects":["valuation","triggers","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MA 10-K 風險因子將關稅相關的不確定全球貿易政策列為可能對業務（含消費與企業支出）及利害關係人關係產生不利影響的因素；屬間接暴露，未量化。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"Uncertain global trade policies and related government actions (including those related to tariffs), which could have an adverse impact on our business (including with respect to consumer and business spending) and relationships with stakeholders","as_of":"2026-02-11","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MA 10-K 指出地緣事件、OFAC 制裁與不利貿易政策可能引發相關司法管轄區報復行動而不利業務；OFAC 制裁限制與特定國家／實體往來。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"Geopolitical events and any resulting OFAC sanctions, adverse trade policies, enforcement of U.S. laws related to countering the financing of terrorism, economic sanctions and anti-corruption, or other types of government actions could lead affected or other jurisdictions to take actions in response that could adversely affect our business.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q2 2026 財報電話會議（2026-07-30）：管理層指中東衝突造成的地緣不確定性趨緩但仍壓抑跨境旅遊與支出。","source":"GuruFocus, Q2 2026 Mastercard Inc Earnings Call Transcript","url":"https://www.gurufocus.com/stock/XKAZ:MA_KZ/transcripts/8996568","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Marqeta 狀態頁記錄 2026-09-03 Mastercard 端平台故障，使其整合服務降級約 7.5 小時；根因是否共用未見揭露。","source":"isdown.app Marqeta incident 648879","url":"https://isdown.app/status/marqeta/incidents/648879-integration-service-degradation-on-master-card","excerpt":null,"as_of":"2026-09-03","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"3Q26 淨營收 $9.8B，+14%（匯率中性亦 +14%）；支付網路淨營收 +11% 至 $5.7B；VAS 淨營收 +19% 至 $4.06B；跨境量 +11%（當地幣），跨境 assessments +16%，差距主要來自國際定價與組合","source":"Mastercard 3Q26 earnings release (SEC 8-K, 2026-10-29)","url":"https://www.sec.gov/Archives/edgar/data/0001141391/000114139126000122/ma09302026-exx991xearnings.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"3Q26 GDV +7%（當地幣）至 $3.0T，購買量 +9%，交易筆數 +9%；跨境非旅遊 CNP +15%（Q2 為 20%）；歐洲內跨境成長放緩至 10%（去年同期 16%）","source":"Mastercard 3Q26 earnings release / PPC Land coverage","url":"https://ppc.land/mastercard-revenue-gains-14-to-9-8bn-as-services-rise-19/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"VAS 前九個月營收 $11,334M，+20%；Q2 +20%（中性匯率 +18%），Q1 +22%；全年中性匯率營收成長維持低雙位數高端，且管理層預期落在區間更高處；約 60% VAS 營收與網路連動","source":"Mastercard 10-Q 3Q26 / Q2 earnings call highlights (MarketBeat)","url":"https://www.sec.gov/Archives/edgar/data/0001141391/000114139126000124/ma-20260930.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"美國 interchange 和解於 2026 年 6 月獲初步核准：平均費率降 0.1pp 五年、標準消費信用卡費率上限 1.25% 八年；Mizuho 認為上限限制中期定價權，Baird 認為降低風險；Walmart 為主要反對者","source":"TipRanks/The Fly (Baird), Kavout, TIKR 報導","url":"https://www.tikr.com/fr/blog/mastercard-cleared-its-biggest-legal-overhang-in-june-does-a-880-target-still-hold","excerpt":null,"as_of":"2026-06-11","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"3Q26 營收分段與跨境數據（原文）","source":"Mastercard 3Q26 Earnings Release PDF","url":"https://s25.q4cdn.com/479285134/files/content_files/3Q26-Mastercard-Earnings-Release.pdf","excerpt":"currency-neutral basis versus the comparable period in 2025. The increase was attributable to growth in our payment network and value-added services and solutions. ▪ Payment network net revenue increased 11%, as reported and on a currency-neutral basis. Primary drivers of the increase were as follows: • Gross dollar volume growth of 7% on a local currency basis to $3.0 trillion. • Cross-border","as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 自述：即時帳戶對帳戶支付成熟後，國內 P2M/P2P 市佔競爭可能增加，跨境市佔也可能被基礎設施互連所擾動；多項產業倡議在試驗帳戶型全球機制，可能擾動清算結算選項。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"As these real-time account-based propositions mature, we face a possible increase in competition for our existing domestic person-to-merchant (“P2M”) and person-to-person (“P2P”) transaction market share. Similarly, as interlinking of these infrastructures is further explored, they could disrupt our existing cross-border P2M and P2P market share.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 自述：穩定幣與加密貨幣可能隨監管（如 GENIUS Act）更普及，加密原生業者有能力擾動傳統金融市場；對公司既是機會也可能與其產品競爭。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"Digital currencies and emerging players (such as crypto natives) have the ability to disrupt traditional financial markets. The increased prominence of digital currencies creates an opportunity for us, but could also compete with our products and services.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：新技術可能優於或使現有技術過時，並促使使用其技術的客戶（含金融科技與科技公司）改用自有技術與之競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"These changes could result in new technologies that may be superior to, or render obsolete, the technologies we currently use in our programs and services.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Mastercard 據報評估出售 Nets 即時支付單位，轉向穩定幣（BVNK）","source":"paymentexpert.com: Mastercard nets sale next rtp play","url":"https://paymentexpert.com/2026/03/30/mastercard-nets-sale-next-rtp-play/","excerpt":null,"as_of":"2026-03-30","retrieved_at":"20261102","affects":["moat_trend","triggers"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 描述 Mastercard 的數位授權與驗證能力橫跨店內、電商與 agentic 介面等所有數位通路，並列出數位錢包、BNPL 等 fintech 為競爭來源（通路擴張與競爭並存）","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"We offer global digital enablement and authentication capabilities that operate across all digital channels including in-store environments, e-commerce platforms and agentic interfaces.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"10-K 指出 fintech 與新興支付業者可能以內部帳戶轉帳、即時帳戶對帳戶網路等非卡軌處理支付，對客戶與資料構成競爭","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"we face increasing competition from fintechs and other emerging payments providers, both for customers and data.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Mastercard 推出 Agent Suite，協助企業部署內建支付與安全控制的 AI agent","source":"Mastercard Newsroom 新聞稿","url":"https://newsroom.mastercard.com/news/eemea/en/newsroom/press-releases/en/2026/mastercard-launches-agent-suite-as-the-agentic-ai-era-reshapes-digital-commerce/","excerpt":"Mastercard launches Agent Suite as the agentic AI era reshapes digital commerce • Mastercard introduces Mastercard Agent Suite to help businesses integrate agentic AI into their operations","as_of":"2026-03-10","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026 年累計重組費用 2.02 億美元，目的為支持長期成長機會的再投資","source":"Mastercard 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001141391/000114139126000124/ma-20260930.htm","excerpt":"Restructuring charge •In the nine months ended September 30, 2026, we recorded a restructuring charge of $202 million ($158 million after tax, or $0.18 per diluted share). The savings from the restructuring action are primarily intended to enable reinvestment to support the realization of our long-term growth opportunities.","as_of":"2026-10-30","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師平均目標價約 $660（38 位，中位 $667.5，區間 $550–$735；38 buy/3 hold/0 sell），as of 2026-08；BullStory 2026-08-23 列 37 位、均值 $667.30。Q3 後更新目標價未查到。","source":"Walnut Invest MA forecast; BullStory MA forecast","url":"https://walnutinvest.com/stocks/ma/forecast","excerpt":null,"as_of":"2026-08-23","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026（7/30）財報後 UBS 目標價升至 $670（自 $640）、Macquarie 升至 $670（自 $665）。","source":"MarketBeat MA price target page","url":"https://www.marketbeat.com/stocks/nyse/ma/price-target","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026 年初 guidance（淨營收約 +11–12%，成本 +10–11%）與市場共識一致；Q1（4/30）維持未調升；Q2（7/30）轉述稱上調至低雙位數高端、淨營收 +12%。","source":"stockanalysis.com MA Q2 2026 transcript summary; TIKR","url":"https://stockanalysis.com/stocks/ma/transcripts/658075-q2-2026/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 調整後 EPS $5.04 對共識 $4.77，營收 $9.277B（+14%）對共識 $9.068B，連續八季優於預期。","source":"Barchart / Tiger Brokers 'Mastercard Analysts Boost Their Forecasts After Better-Than-Expected Q2 Results'","url":"https://www.itiger.com/news/2655366840","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill（2026-10-18）FY2026 EPS 共識約 $20.55（47 位）；Q3 預期 EPS $5.31、營收 $9.932B（Q3 報告預定 10/29，結果未查到）；下一期營收預估 3 個月內下修 0.11%。MarketBeat 7/30 另列全年共識 $19.61，兩源不一致。","source":"Chartmill MA estimates; MarketBeat Erste Group note","url":"https://www.chartmill.com/stock/quote/MA/estimates","excerpt":null,"as_of":"2026-10-18","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Macquarie 曾因中東衝突總經影響下調目標價至 $665；Raymond James 下調目標價至 $631（自 $707）。","source":"Munich startup insights feed; TipRanks/The Fly","url":"https://il.tipranks.com/news/the-fly/2856188","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2025-11-10 8-K：Mastercard 與 Visa 就商家禁制令類（injunctive rules relief class）簽訂更新版集體和解協議，涉及網路規則與附加費規則。","source":"SEC EDGAR 8-K Item 8.01（2025-11-10）","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139125000197/ma-20251110.htm","excerpt":"On November 10, 2025, Mastercard Incorporated (the “Company”) announced that the Company and its operating subsidiary, Mastercard International Incorporated (collectively, \"Mastercard\"), have entered into an updated Class Settlement Agreement (the \"Agreement\") with court-appointed counsel for an injunctive rules relief class of merchants to settle their claims related to business practices, including network rules.","as_of":"2025-11-10","retrieved_at":"20261102","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露英國集體訴訟（索賠逾 £10 億英鎊）及美國 EMV 責任轉移集體訴訟（原告主張單一損害逾 $10 億）。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"The plaintiffs submitted expert reports that allege aggregate single damages in excess of $1 billion against the four Network Defendants.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"10-Q（2026Q3）載明 2026-08-03 以現金 $14 億收購 BVNK（穩定幣基礎設施），另有最高 $3 億或有對價；Q1 10-Q 載明 2026 年 3 月簽約。","source":"SEC EDGAR 10-Q FY2026 Q3（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001141391/000114139126000124/ma-20260930.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"10-Q（2026Q3）載明 2026-08-03 以現金 $14 億收購 BVNK，另有最高 $3 億或有對價。","source":"SEC EDGAR 10-Q FY2026 Q3（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001141391/000114139126000124/ma-20260930.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"2025-11-10 更新版商家禁制令類集體和解協議（Mastercard 與 Visa）。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139125000197/ma-20251110.htm","excerpt":"On November 10, 2025, Mastercard Incorporated (the “Company”) announced that the Company and its operating subsidiary, Mastercard International Incorporated (collectively, \"Mastercard\"), have entered into an updated Class Settlement Agreement (the \"Agreement\") with court-appointed counsel for an injunctive rules relief class of merchants to settle their claims related to business practices, including network rules.","as_of":"2025-11-10","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"英國集體訴訟索賠逾 £10 億英鎊；美國 EMV 責任轉移集體訴訟原告主張單一損害逾 $10 億。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm","excerpt":"The plaintiffs submitted expert reports that allege aggregate single damages in excess of $1 billion against the four Network Defendants.","as_of":"2026-02-11","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":78.42,"operating_margin_pct":60.07,"fcf_margin_pct":42.52,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"V","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.75,"operating_margin_pct":65.57,"fcf_margin_pct":44.91,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AXP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":19.82,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXP","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COF","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":45.04,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COF","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PYPL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.76,"operating_margin_pct":18.52,"fcf_margin_pct":18.37,"rd_intensity_pct":9.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"MA"},"financial_history":{"ticker":"MA","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":22237000000.0,"revenue_yoy_pct":null,"gross_margin_pct":76.33,"operating_margin_pct":57.21,"net_income":9930000000.0,"diluted_eps":10.22,"free_cash_flow":10098000000.0,"fcf_margin_pct":45.41,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":25098000000.0,"revenue_yoy_pct":12.87,"gross_margin_pct":76.01,"operating_margin_pct":58.29,"net_income":11195000000.0,"diluted_eps":11.83,"free_cash_flow":10892000000.0,"fcf_margin_pct":43.4,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":28167000000.0,"revenue_yoy_pct":12.23,"gross_margin_pct":76.31,"operating_margin_pct":57.96,"net_income":12874000000.0,"diluted_eps":13.89,"free_cash_flow":13586000000.0,"fcf_margin_pct":48.23,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":32791000000.0,"revenue_yoy_pct":16.42,"gross_margin_pct":77.89,"operating_margin_pct":59.51,"net_income":14968000000.0,"diluted_eps":16.52,"free_cash_flow":16433000000.0,"fcf_margin_pct":50.11,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MA/MA_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Mastercard Incorporated** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good morning. My name is Elodie, and I will be your conference operator today. At this time, I would like to welcome everyone to the Mastercard Incorporated Q3 2026 Earnings Conference Call. [Operator Instructions] Mr. Devin Corr, Head of Investor Relations, you may now begin your conference.

**Devin Corr** (Executives):
Thank you, Elodie. Good morning, everyone, and thank you for joining us for our third quarter 2026 earnings call. With me today are Michael Miebach, our Chief Executive Officer; and Ling Hai, our Chief Financial Officer. Following comments from Michael and Ling Hai, the operator will announce your opportunity to get into the queue for the Q&A session. It is only then that the queue will be open for your questions. 
You can access our earnings release, supplemental performance data and the slide deck that accompany this call in the Investor Relations section of our website, mastercard.com. Additionally, the release was furnished with the SEC earlier this morning. Our comments today regarding our financial results will be on a non-GAAP currency-neutral basis unless otherwise noted. Both the release and the slide deck include reconciliations of non-GAAP measures to GAAP reported amounts. 
Finally, as set forth in more detail in our earnings release, I would like to remind everyone that today's call will include forward-looking statements regarding Mastercard's future performance. Actual performance could differ materially from these forward-looking statements. Information about the factors that could affect future performance are summarized at the end of our earnings release and in our recent SEC filings. A replay of the call will be posted on our website for 30 days. With that, I will now turn the call over to our Chief Executive Officer, Michael Miebach.

**Michael Miebach** (Executives):
Thank you, Devin. Good morning, everyone, and thank you for joining us. Three quarters into the year, our performance continues to demonstrate the strength and consistency of our business. Net revenue growth was up 14%, and net income up 18% in the third quarter on a year-over-year non-GAAP currency-neutral basis. While there continues to be economic and geopolitical uncertainty, consumers continue to spend, businesses continue to invest and commerce continues to expand. The economy, our overall business and our network have a resilient backdrop. 
At its core, our network helps people and businesses transact and participate in the economy, and our advantage here is clear: a diversified business, a trusted global network and the ability to help our customers grow. We're building on that advantage by expanding the reach and utility of our network. We now have more than 200 million acceptance locations and 300 million more digital access points around the world. That is unmatched. 
On a year-over-year basis in the first half of 2026, merchant acceptance is up 20% and growing. This includes initiatives like our Pay Local program, which expands acceptance by embedding cards into local wallets, and Tap on Phone, a smart acceptance solution. However, we're not only expanding how merchants accept payments, we're also finding valuable ways to get more Mastercard credentials to more people. That spans the full consumer spectrum from premium offerings for affluent consumers and business owners to products that give people their first access to the financial system. 
There are huge numbers of financially underserved people around the world. Our new Essential Debit product builds on our long-standing work to help open the door to broader financial opportunities and economic resilience. We have signed 15 Essential Debit programs this year across 7 markets. These programs give our partners tools to address up to 70 million unbanked adults in those markets. This means more people have a new payment option or cards that offer protections and broad acceptance not offered by local payment options. 
We're seeing early traction across a range of partners. These credentials are now issued within Airtel's scaled mobile wallet ecosystem, launching next quarter in Nigeria and by Financoop, which supports a large network of cooperative institutions in Ecuador. This year, we have already won 100 new affluent credit and debit programs and launched more than 25 World Legend programs. Mastercard affluent portfolios have higher engagement and higher cross-border spend. In fact, our affluent spend is growing 2x faster than overall credit. 
This quarter, UBS launched a super-premium invitation-only Mastercard credit product in Switzerland's highly competitive affluent market. It includes our concierge service and frequent traveler benefits. Core to our programs is making a real connection with people and offering a product that appeals to their needs. That focus on meeting new people where they are led to our new partnership and co-brand program with Beast Industries. This program spans consumer and small business creator cards. With more than 1 billion followers across social media, MrBeast is one of the most influential creators in the world. But that work is not just about clicks. It's capturing the cultural power of digital communities and driving economic and social opportunity. 
Together, we will connect creators and their communities in new ways, bringing Mastercard scale and capabilities to the next generation as their financial lives evolve. What does all of this tell us? Mastercard products are in demand, and that demand continues to grow. More cards and more acceptance points drive more transactions and data, strengthening the power of our network and the value we deliver. Across over 200 countries and territories, every market and region is unique. And we're winning, leveraging our global capabilities and that local expertise. 
Let's look at a few wins from this quarter. In the Nordics, we renewed our partnerships with Handelsbanken and Swedbank, following a previously signed exclusive agreement with SEB. These wins include services like fraud detection and loyalty, strengthening our position in one of the most advanced digital payment markets. At the same time, we renewed DSGV and DZ Bank, 2 of Germany's largest banking organizations. 
Let's put that in context. These renewals deepen our relationships with 2 of the leading credit issuers in Europe's largest economy. They position us to capture the substantial secular opportunity in Germany. In China, our teams on the ground are very busy building and solidifying our position in the local market. This strong foundation for long-term growth is rooted in the growing acceptance and signing issuer deals to make Mastercard the preferred brand. 
This includes new programs with China's top 15 issuers. This quarter, we added to that with the new World Hilton co-brand with Bank of Communications and a consumer debit deal with Bank of China, who alone serves hundreds of millions of retail customers. Two fantastic deals to capture domestic and cross-border spend and deliver value-add services and solutions in the market. In the United States, we secured a major win with Pinnacle Financial Partners. The newly combined bank's entire issuing portfolio will move onto our network starting in 2027. This includes consumer credit, debit, small business and commercial cards. 
And finally, moving to India. With a large domestic scheme, this is one of the world's most competitive markets. This quarter, we signed an important small business deal with HDFC Bank. It's India's largest private sector bank with nearly 10,000 branches, over 100 million customers. This deal includes value-add services and solutions and is expected to add 3 million cards to the Mastercard network. Beyond small business, we see a sizable opportunity across commercial payments, including invoice payments. Our work in invoice payments helps transform dated, cumbersome accounts payable processes into automated digital workflows with virtual cards. We focus on bringing more virtual cards to market and embed them directly into tools businesses already use. 
Tungsten Automation is adding Mastercard's virtual card technology into its automated accounts payable offerings. A leader in intelligent document processing, Tungsten serves more than 25,000 customers. This will enable their enterprise customers to generate virtual cards seamlessly, and with that, accelerate supplier payments, reducing cost, friction and risk. That is tangible value. And we've seen those results play out. For example, a large U.S. retailer consolidated more than $100 million in supplier payments using Mastercard virtual cards through our partner Coupa. This one decision reduced the number of suppliers that needed to be onboarded, saving an estimated $35 million in onboarding costs. That's valuable savings for just one of their many clients, and Coupa is one of many partners working with us on improving B2B supplier payments. 
There's similar value in the travel vertical, where today we partner with 8 out of the 10 largest players to capture the secular opportunities. Add to that, our expanded relationship with Checkout.com in the UAE, and you have another channel to bring Mastercard virtual cards to travel businesses at scale. The aggregate of our travel-related wins from just this quarter is expected to generate more than $20 billion in incremental spend on our network over the lives of the agreements. These wins reflect our differentiated capabilities that address specific customer needs, but also create opportunities to deliver more value through value-added services and solutions. 
Now many of our services directly support growth in our payment network. Our analytics, marketing, loyalty and consulting services helps clients acquire, engage and retain customers while building healthier portfolios and driving more payment activity. For example, through our strategic partnership with Qatar National Bank Group, we're deploying these capabilities across QNB's presence in more than 28 countries to strengthen customer relationships and drive growth. 
And American Airlines is one of the industry's largest airline credit card programs. We are supporting customer acquisition for its refreshed premium offering, the Citi / AAdvantage Executive World Legend Mastercard. These capabilities, powered by our data, can deliver meaningful results. Across Mastercard marketing services campaigns on a global basis, our clients see an average incremental spend growth of 8 percentage points over the measurement period. 
As commerce becomes more digital and AI changes elements of payments, our security solutions are becoming more relevant. As a reminder, security solutions include fraud, identity and cybersecurity. Our portfolio is carefully designed to help our partners protect the ecosystem, and we see demand across the board. This quarter, we added or extended fraud and identity wins with Standard Bank, Monzo and Starling Bank. Starling, for example, extended its use of Fraud Rule Manager, helping it respond faster to emerging attacks, reduce false declines and protect the customer experience at scale. 
Within cybersecurity, we continue to scale one-to-one platform sales, but even more so new network products like our newly launched Digital Risk Protection. This capability helps organizations identify vulnerabilities in their own digital environments. After only a few months in market, it now serves nearly 800 enterprise customers. Additionally, our enhanced third-party risk offering brings together RiskRecon and Recorded Future capabilities in one solution. It helps identify, prioritize and respond to risks before they become business disruptions. 
But AI is not only changing the demand for our security solutions, it's also changing how commerce happens. The foundation I described earlier, broad participation, global acceptance and trusted capabilities, positions us to help shape the next evolution of commerce. That includes agentic commerce, where a buyer uses AI agents to discover, select and purchase a product or service. There are 2 forms, machine-to-machine and traditional e-commerce. Combined, they create significant opportunity for Mastercard, from more transactions to new B2B carded payments as businesses utilize agents. 
And eventually, an entirely new addressable market of microtransactions, all the while creating more opportunity for our services from fraud to longer-term potential in insight and loyalty. Consumers are already beginning to use agents to discover and purchase products. We expect that trend to build as holiday shopping ramps up and to continue well beyond the season. 
It is still early days, and the numbers are not yet significant in the grand scheme. But as the AI agentic assistants have emerged, agentic transactions are ramping up at impressive weekly growth rates. We're now seeing the early stages of consumer adoption. For this type of agentic commerce to function at scale, we need 4 things: trust in the payment, the agent, the ecosystem and ubiquitous reach. Mastercard has built capabilities for each of these 4. 
For trust in the payment, tokenization is embedded in Agent Pay and backed by the franchise rules everyone expects today. For trust in the agent, Agent Pay ensures agents are verified and authorized by the buyer, that the merchant and issuer are aware. For trust in the ecosystem, we bring transparency and continuity through the payment flow. Verifiable Intent captures the buyer intent, and our recently launched Agentic Trust Intelligence solution helps banks and merchants evaluate transactions initiated by any AI agent. And that allows these transactions to occur wherever Mastercard is accepted. That is the unparalleled and growing reach I talked about earlier. 
At the same time, we are helping merchants ready themselves and be more discoverable to agents with our new Agent Connect solution. Many partners are putting all of this into practice. For example, Shopify, through Shop Pay, is using Agent Pay and our network tokens to make agentic payments more secure and seamless by preserving the integrity of the consumer's credential end-to-end. Shop Pay is already available on multiple agentic platforms with more to follow. And with OpenAI this quarter, we signed a broad strategic partnership that includes the use of Agent Pay and goes well beyond. Our agreement establishes collaboration across payments, joint services growth and AI transformation. 
And we cannot forget the other technology that is part of virtually every conversation, digital assets and stablecoins. Our customers and partners are continually thinking about how they might use the technology in their offerings. To be useful, digital assets need to work with existing financial and commercial services. That means enabling customers to connect digital asset capabilities with the accounts, payment systems and money movement experiences already in use. That is why we acquired BVNK. Through BVNK, we are expanding the infrastructure that connects stablecoins with traditional payment and money movement experiences. Financial institutions and fintechs today struggle to offer both fiat and stablecoin accounts, creating the risk of customer deposits moving to competing stablecoin accounts. 
Our first combined Mastercard BVNK product is the Mastercard Global Money Platform, enables financial institutions and fintechs to offer accounts where customers can hold, convert, send and receive across fiat currencies and stablecoins. Mastercard Move is also integrated, bringing its 17 billion endpoints to the platform. This enables businesses to pay out stablecoin balances directly into recipients' local bank accounts. Nuvei and Marqeta will be among the first customers to integrate the platform, with more partners to be announced soon. And all of this is complementary to our existing stablecoin offerings such as crypto co-brands and stablecoin settlement. 
So stepping back, the quarter demonstrates the breadth and consistency of our strategy. We're expanding the reach and utility of our network, solidifying differentiation. We continue to win important relationships and deepen those relationships with differentiated services, growing payments and protecting the ecosystem. And we're extending our trusted capabilities into agentic commerce and digital assets. We're executing and delivering today while investing and solidifying our position for the future. And with that, I will turn it over for the very first time to Ling Hai.

**Ling Hai** (Executives):
Thank you, Michael. Turning to Page 3, which shows our financial performance for the third quarter on a currency-neutral basis, excluding where applicable, special items and the impact of gains and losses on our equity investments. Net revenue was up 14%, reflecting continued growth in our payment network and our value-added services and solutions, with minimal impact from acquisitions and dispositions. These revenues were above our expectations, primarily due to the continued strength of our business and the timing of both services projects and payment network deals. 
Operating expenses increased 12%, including a 1 ppt increase from acquisitions and dispositions, and operating income was up 15%. Net income and EPS increased 18% and 21%, respectively, driven primarily by the strong operating income growth in the quarter. EPS was $5.31, which includes a $0.16 contribution from share repurchases. During the quarter, we repurchased $3 billion worth of stock and $648 million of additional stock through October 26 of this year. 
Now turning to Page 4, where I'll speak to the growth rates of our key volume drivers for the third quarter on a local currency basis. Worldwide gross dollar volume, or GDV, increased by 7% year-over-year. In the U.S., GDV increased 6%, with credit growth of 10% and debit growth of 1%, which includes the impact of the Capital One debit migration. Outside of the U.S., GDV increased 8%, with credit growth of 6% and debit growth of 10%. Cross-border volume increased 11% globally for the quarter, reflecting continued growth in both travel and non-travel-related cross-border spending. 
Turning to Page 5. Switched transactions grew 9% year-over-year in Q3. We continued to drive contactless penetration, which in Q3 stood at 81% of all in-person switched purchase transactions. This is up 5 ppt since the same period last year. In addition, card growth was 5%. Globally, there are now 3.8 billion Mastercard and Maestro-branded cards issued. 
Turning to Slide 6 for a look into our net revenue growth rates for the third quarter discussed on a currency-neutral basis. Payment network net revenue increased 11%, primarily driven by domestic and cross-border transaction volume growth as well as pricing. It also includes growth in rebates and incentives. Value-added services and solutions net revenue increased 19%. This includes a minimal impact from acquisitions and dispositions and now reflects the contributions from BVNK. Excluding these impacts, the increase was driven primarily by growth in our underlying drivers, strong demand across consumer acquisition and engagement, business and market insights, security solutions as well as digital and authentication, and finally, pricing. 
Now let's turn to Page 7 to discuss key metrics related to the payment network. Again, all growth rates are described on a currency-neutral basis unless otherwise noted. Looking quickly at each key metric. Domestic assessments were up 13%, while worldwide GDV grew 7%. The 6 ppt difference is primarily driven by pricing and mix. Cross-border assessments increased 16%, while cross-border volumes increased 11%. The 5 ppt difference is driven primarily by pricing in international markets and mix. Transaction processing assessments were up 14%, while switched transactions grew 9%. The 5 ppt difference is primarily related to pricing and a favorable mix, partially offset by lower revenue from FX volatility. Other network assessments were $285 million this quarter. 
Moving on to Page 8. You can see that on a non-GAAP currency-neutral basis, excluding special items, total adjusted operating expenses increased 12%, including a 1 ppt increase from acquisitions and dispositions. The growth in operating expenses was primarily driven by spending to drive the execution of our strategic priorities, including product innovation, geographic expansion and continued investments in our technology. 
Turning to Page 9. Let me comment on the operating metric trends for Q3 and the first 3 weeks of October. Starting with Q3, switched volume and transaction metrics are generally in line with Q2 and remained strong. Of note, the sequential increase in the U.S. switched volume was primarily due to recent commercial wins. Looking at cross-border. First, lower-yielding intra-Europe volumes were down sequentially from Q2 to Q3, driven by the impacts related to a new customs fee in the EU, timing of large retail promotional events and lower crypto purchases in the quarter compared to last year. 
These impacts on intra-Europe cross-border were the primary reasons for the decline in Card-Not-Present ex-travel sequentially. And growth in higher-yielding other cross-border remained stable and slightly higher quarter-over-quarter. As we look to the first 3 weeks of October, spend remained strong with metrics generally in line. A few points to note. In the U.S., switched volume improved sequentially as we begin to see the lapping of the Capital One debit migration, the lift from recent commercial wins and higher spend on gas. 
As a reminder, the Capital One debit migration began towards the end of Q3 last year and continued through Q1 '26. Looking at cross-border, the sequential impacts remain predominantly intra-Europe. Growth in cross-border Card-Not-Present ex-travel continued to see the impact from 2 of the areas I noted earlier, notably the customs fee and a tougher comp due to higher spend on crypto purchases last year. And the slight deceleration in cross-border travel was due to timing of holidays. Overall, underlying spend remains strong and consumers and businesses are spending. 
Turning to Page 10. I wanted to share our thoughts for the remainder of the year. As mentioned, consumer and commercial spend was healthy in Q3 and so far into Q4. Our business fundamentals are strong, and we continue to deliver solid growth across both our payment network and value-added services and solutions. These results reflect our winning strategy, strength of our innovations, diversification of our business and our relentless commitment to serving our customers. This is all underpinned by a supportive macroeconomic environment with balanced labor markets, strong household balance sheets and continued wage growth. 
To date, consumers and businesses have demonstrated resilience, but there is heightened geopolitical uncertainty, which has persisted for some time, driving energy prices higher and putting more focus on monetary policy around the world. We will continue to monitor the situation just as we always do. Our outlook on growth for the remainder of the year continues to remain positive. 
So turning to our expectations. For the full year 2026, we expect net revenue growth to remain at the high end of low double digits range on a currency-neutral basis, excluding inorganic activity. As a reminder, in Q2 earnings, we told you that our expectations were higher in the range compared to earlier in the year. Our full year remains in line with these expectations. We anticipate minimal impact from acquisitions and dispositions and a tailwind of approximately 1 ppt from foreign exchange. 
We also expect full year operating expenses growth to remain in line with previous expectations at a low double digits range versus a year ago on a currency-neutral basis, excluding inorganic activity. We expect a minimal impact from acquisitions and dispositions and a headwind of 0.5 to 1 ppt from foreign exchange on a full year basis. As it relates to our expectations for the fourth quarter of 2026, year-over-year net revenue growth is expected to be at the high end of low double digits range on a currency-neutral basis, excluding inorganic activity. 
We expect minimal impact from acquisitions and dispositions and a headwind of approximately 1 ppt from foreign exchange, primarily driven by the strengthening of the U.S. dollar over the past quarter. From an operating expense standpoint, we expect Q4 growth to be at the high end of low double digits range versus a year ago, again, on a currency-neutral basis, excluding inorganic activity. 
We anticipate a 1 ppt drag from acquisitions and dispositions, while foreign exchange is forecasted to be a tailwind of approximately 0.5 ppt for the quarter. On other income and expense, in Q4, we expect an expense of approximately $115 million. This excludes gains and losses on our equity investments, which are excluded from our non-GAAP metrics. And finally, we expect a non-GAAP tax rate in the range of 20% to 21% for both the full year and Q4. And with that, I will turn the call back over to Devin.

**Devin Corr** (Executives):
Thank you. Elodie, you may now open the line for questions.

**Operator** (Operator):
[Operator Instructions] Your first question is from the line of Harshita Rawat with Bernstein.

**Harshita Rawat** (Analysts):
Michael, I want to ask about agentic commerce. A lot has been happening here, and it feels like there's a lot of patchwork of checkout options ranging from single-use virtual cards to wallets. My question is, how important it is for you that Mastercard agent tokens are being used as opposed to wallets or virtual cards? And I know you have your own probability-based risk signals with Agent Pay now as well. And how can you drive adoption for Mastercard Agent Pay? I know you talked about Shop Pay and OpenAI as well.

**Michael Miebach** (Executives):
Thanks, Harshita. So the -- this is an important question. So agentic commerce, first of all, we think is the next evolution of digital commerce. It is -- went through a year and a bit in terms of getting the ecosystem ready. There's Agent Pay out there. There are the solutions out there. And you just [ raised ] an additional -- you just listed an additional set of checkout ways that are out there. 
So the ecosystem is kind of balancing out. So when you think about what matters, what I said in my prepared remarks is the trust in the payment is key. The trust in the agent is key. The trust in the ecosystem is key, and generally, reach is key. So if we think that, that matters to merchants, that matters to consumers, altogether, I think this is the direction that the ecosystem is going into. So it's also true, though, that not everybody is ready at the same time. 
So there's a lot of patchwork going on right now, and I wouldn't call that solutions. It's kind of patching towards what is the golden goal here, and the golden goal I just listed is, you have a protected transaction that works in the same way as consumers are used to and merchants are used to. So one of the things that need to happen before this to really take off is consumers need to feel comfortable. So use of Agent Pay and having registered agent is a key thing. And the other thing is merchants need to be actually discoverable because then the other side of the transaction isn't really working. 
So that's a piece that is slightly behind the first one. So if everybody uses Agent Pay, that doesn't mean that every merchant is still discoverable. And by the way, there are other solutions out there similar to Agent Pay, but it's not virtual cards. So on the merchant's discoverable side, so how do I get my product catalog as a merchant into an agentic experience that a consumer is choosing? That's the key thing. So our Agent Connect solution helps to bridge that one. So we're kind of ready to take off. 
It is in everybody's best interest to use Agent Pay and equivalent. We are not supporting solutions that take a onetime VCNs out there as fronting a transaction. That fundamentally breaks a transaction that is important from a consumer perspective. They made a choice. It's important from a rewards perspective, from a control perspective, and so forth. So I think we're at this turning point where everybody is pushing in the same direction. We are very clear that fully tokenized all the way through agentic pay or an equivalent is the way to go. If we get this all right, it will truly be the next evolution of digital commerce.

**Operator** (Operator):
Your next question is from the line of Tien-Tsin Huang with JPMorgan.

**Tien-Tsin Huang** (Analysts):
Great results here. Ling Hai, welcome to the call. I wanted to ask on just the outperformance and growth for the quarter and the 2 points of acceleration in revenue growth. It seemed pretty broad-based, but just want to maybe just give us a little bit more detail on that, anything that was more onetime in nature, et cetera.

**Ling Hai** (Executives):
Thank you, Tien-Tsin, for the question. Yes, if I look at the overall performance in Q3, it really speaks to the strength of the business, and it's very much broad-based, especially in value-added services and solutions. I do want to point out, as you probably heard in my prepared remarks, there is also a little bit timing of services projects and also the signing of deals moving from Q4 to Q3. So that really means it is a revenue benefit for Q3. You will see a similar offset in Q4. 
But overall, we continue to see strength. The underlying business is very strong. Consumers and businesses are spending. The overall environment remains very supportive. Consumer sentiment is positive. So all those things are very good. But we also know there's uncertainty, there's puts and takes. But overall, Q3 is very strong and we're very, very glad about the accomplishment.

**Operator** (Operator):
Your next question is from the line of Adam Frisch with Evercore ISI.

**Adam Frisch** (Analysts):
Cross-border is slower a little bit, still obviously strong, but I know there were some portfolio changes in recent quarters. So should we expect some modest acceleration there as you move forward and lap the comps? Or are there some underlying trends that are having a larger effect? And then, Michael, just a clarification. If there's a processor that is using a virtual card to facilitate agentic transaction, so if I put my Mastercard in this particular wallet and they use a virtual card to facilitate the transaction, are you not supporting that scenario?

**Ling Hai** (Executives):
Thanks, Adam. Let me take the first part of the question first. First off the bat, I would say when you look at cross-border volume at 11%, that is very strong. And then not to also minimize the revenue side, cross-border assessment is 16% growth, so that's very strong performance. If we break it out a little bit, as you heard me talk about, if you look at the cross-border Card-Not-Present excluding travel, you're seeing Q2 20% going to 15%, but 15% is also very strong, and I provided the explanations for why we are seeing a little bit of a downward trend in terms of the volume. And mostly, it's intra, which is lower yielding and the other cross-border volume, which is the inter volume remains very healthy, very resilient. 
Now as I have always said, we benefit from our diversification. So you can have impacts hitting in one segment, one geography, but we can handle that because we're diversified and also benefit from upticks in other areas. A great example this year is we saw some negative impact out of the Middle East, the GCC countries, but then we see this benefit in terms of outbound from Venezuela, right? So -- and in terms of where cross-border travel stands, I alluded to the fact that, yes, the Middle East conflict will -- continues to have an impact. But as we look at the balance of the year, as we've told you before, we are expecting a level that's similar to the end of Q2, and that's what we see in Q3. 
So I think about the Middle East conflict, I think about the share shifts you mentioned, both are discrete and do not represent any fundamental change to our proposition. I think the underlying spend remains strong and we're very focused on driving cross-border travel. We have those services that's called Optimization Travel Rewards. So we'll continue to do that. So what's important to note is that we will continue to be focused on giving our consumers the right propositions for cross-border, whether it's travel or non-travel.

**Michael Miebach** (Executives):
And Adam, to your clarification question on agentic. So let me be very clear. What we're not supporting is VCN as a solution in between. That is not the consumer scenario that actually you asked. You said, "If you put your card somewhere into an agent as an agent-first solution or whatever it is," consumers do what they do, and it's their choice, and we try to give them many choices to choose Mastercard. A VCN is a processor decision that is a bridge to get ready for a fully tokenized transaction all the way through for a period of time. We are cognizant that this ecosystem needs to get there, no question about it, but that's not a long-term solution that we will support.

**Operator** (Operator):
Your next question is from the line of Andrew Schmidt with KeyBanc Capital Markets.

**Andrew Schmidt** (Analysts):
Maybe you could just touch on the competitive environment in developing markets like India and Brazil, where there are entrenched A2A systems. The HDFC deal sort of piqued my interest, but there's been some interesting developments there. UPI pricing has increased. It seems like the markets might be broadening out a little bit. But if you could just talk about positioning, any changes there, that would be helpful.

**Michael Miebach** (Executives):
All right. Thank you for your question. So let me just frame up the payment ecosystem to start with. Super competitive, and there's nothing new there. So it's been competitive for some time. And you have these wide ranges of competitors that are coming in, into payments and seeing the potential that we're seeing. So if I go through some categories, before I find my way all the way to India, digital players, wallets, buy now, pay later providers have come in and, in the end, found a way to partner because we provide scale and protections and so forth. So that's one angle on how we deal with -- how we partner with new entrants. 
Stablecoin has been another kind of shift in the ecosystem. We've integrated that into our system to make that available because we believe in consumer choice. And we partner with governments and central banks around the world, and we do that on financial inclusion. We do that on protecting their economies. There are so many ways on how we're engaged in these 220 countries and territories around the world. Now you mentioned India in particular. India is a somewhat unique situation, but not totally unique. You could draw some comparison to Brazil as well, where there's 2 large economies that had one particular issue that wasn't solved by the private sector, and that was financial inclusion with very large population sets where people don't have access. 
I talked about this in my prepared remarks, that we as the private sector and Mastercard in particular, is very focused on financial inclusion. So we are driving that. Now -- but it is true that in India, one of the most competitive and dynamic payments markets in the world, the Indian government has led the setup of UPI, which is a tremendous system and has brought a lot of people into the financial ecosystem, which is generally fantastic. Now this has grown to considerable scale, but if we go by reports, there are reports that are saying that the government is considering, the kind of owners of UPI are considering to have some additional fees in there that will, presumably, I mean, I can't talk for them, but is really the interest of taking this amazing ecosystem that they have built and continue to fund it in a way that works for all parties as it continues to grow. So that is a decision that we fundamentally welcome. 
We continue to engage in India very effectively with the government, with the private sector. We have, meanwhile, spent the time to strengthen our debit proposition, which competes in the market. But fundamentally, I see what UPI has done is bringing a funnel of people into the digital ecosystem that will grow and that will grow. They will graduate to different sets of products, which will include debit and then eventually credit. So there is so much opportunity in India as well as in Brazil, where we essentially pursue the same strategy. So it's partner and compete. It's a market where we are open to compete. Same for Brazil, and that is kind of the key aspect for that. So overall, I think no news on the India front, but the HDFC deal is news. So winning with the largest private sector bank in India is fundamentally something we're very excited about. So we continue to lean in.

**Operator** (Operator):
Your next question is from Darrin Peller with Wolfe Research.

**Darrin Peller** (Analysts):
Nice job. Just maybe when we look at VAS, and again, I know there was some onetime or near-term items, but the overall strength is consistent. And so maybe just touch again on the key drivers, honing in a little bit on cyber and what you're seeing there. I know Recorded Future has had some really good success with a lot of governments that are maybe even incremental to just payments offerings. 
So can you help us expand on what that could mean for the overall business going forward? And then just a quick question on the puts and takes for Q4, if you don't mind, just if you could quickly just give us a sense. We know comps get a little bit easier, the Capital One conversion has started, and pricing continues to be strong for our checks for fourth quarter. So what are the puts and takes on guide for Q4?

**Ling Hai** (Executives):
Okay. Well, let me start with the color on the financials first. So Darrin, you're absolutely right, broad-based strength in value-added services. If I think about where the strength and the durability come from, I think about the following. First of all, as we have told you, 60% of our services are network linked. So the drivers themselves create the tailwind. So that ability to have payment volume where we can then apply services, and the services then create the differentiation, that's the flywheel effect. And we're very proud of this business model. 
Secondly, if I look at services, just if I think about existing services, there's room for further penetrating our existing customer base, right? So we have a very disciplined approach in terms of cross-sell, upsell, in terms of looking at our customer base and where the penetration gap is. And the third one I would say is, you mentioned it. There's room for new services in cyber, in a new world of agentic or the evolution towards that. And by the way, I don't think agentic is going to be the only mode of commerce. It is going to be multimodal. So therefore, we have to be versatile and cut across all these different modes, whether it's in-person transactions, online and agentic down the road. 
They can all coexist. And that speaks to the versatility of the network, and our services can apply across the board. And cyber is a big issue. AI will create more vulnerabilities. And therefore, we will need to come up with the best solutions to help our customers and consumers, customers safeguard the network but -- and their systems, and the consumers to safeguard their payments and their wealth. So fundamentally, those are the things that are driving. Before I hand over to Michael, you also asked about the Q4 guidance and the puts and takes. I would say, again, I talked about the timing of revenue. So you see a little bit acceleration and services play a big role because we accelerated a lot of the services projects in Q3. And therefore, accordingly, you're going to see an offset in Q4. Michael, please?

**Michael Miebach** (Executives):
Yes. You gave a very holistic answer. I just want to kind of remind everybody. So this situation where AI is not only driving productivity upside and is fueling new products for us, but it's also unfortunately, a tool in the hand of fraudsters and scammers and so forth. So that's a situation that is fairly new. What is not new is that we stepped into the security market like a decade ago. So we are very deeply invested in this space. And this has been a significant contributor to our growth rate for that past decade. So overall, that business was initially fraud related, then we expanded into identity, and now we're in cybersecurity in a significant way, and I talked about that in my prepared remarks. 
I don't want to take too much credit, but our investment in Recorded Future kind of looked ahead and said, in this kind of a world where the threats are coming from all sides, it is so critical for us to provide threat intelligence to people because nobody can really defend themselves against all these risks. So if you knew with higher probability where your risk is going to be, particularly on the payment side and the fraud side, what are the compromised cards, et cetera. So this has been a long arc for us, and it just meets the moment. But that business has been growing very fast all the time. So we're not expecting a significant kind of jump from one day to the other. So all of this is kind of playing out at the right time and as predicted and expected for us.

**Operator** (Operator):
Your next question is from the line of Will Nance with Goldman Sachs.

**William Nance** (Analysts):
I heard some of the commentary on some of the intra-Europe volumes. And I was just wondering if you could kind of take a step back, talk holistically about what you're seeing around the European consumer. Peeling back some of the noise, there's been a lot of focus on energy shocks. When you take out some of the discrete impacts, how are you kind of feeling about the trajectory of consumer spending there?

**Ling Hai** (Executives):
Thank you, Will. I'll take this one. So of course, before this job, I also oversaw Europe. It's a very important market for Mastercard, very sizable. I would say if I take a look at the macro environment right now, the European consumers are very resilient. That's probably the best description. And the other thing that I would say is, I see in our own business, in the payment business, we see a lot of innovation. That innovation comes from our customers, whether the banks, the fintechs, the digital players, but also our teams on the ground, right? And that is going to be a very important driver in terms of our growth. 
To your specific question about intra-Europe, I talk about the reasons, right? Nothing structural. It's more about timing and comparisons. And -- but I think overall we see the market being stable and consistent right now. We've got some shifts, but we'll continue to win deals in this market as well. And we are seeing tremendous success in value-added services and solutions. Europe is probably a standout on this front. So that's also very important for us to achieve that sustainability.

**Michael Miebach** (Executives):
And if I can add one point, I think it's important to remind us, when we look across Europe, very evolved economies, but it's still also true that at the same time, you still have a significant secular opportunity, as I mentioned in my prepared remarks earlier. So DSGV and DZ Bank are just 2 big wins that are going to help us eat into that secular opportunity in parts of rural Germany, for example. So it's not just about spend, it's also about the secular opportunity and the tools that Ling Hai referred to are going to help us to go after that in many different ways, including our real-time payment position in Europe and our services and our card propositions.

**Operator** (Operator):
Your next question is from the line of Timothy Chiodo with UBS.

**Timothy Chiodo** (Analysts):
Great. I also want to touch on some of the mechanics around agentic commerce. So appreciating that we're moving past the onetime use virtual card at some point and moving more towards the long term of agentic network tokens. Specifically, I'd like to dig into some of the steps for merchant readiness. You mentioned earlier some of the discoverability aspect, and I totally appreciate that. But I want to focus a little bit more on the ability to accept a network token and some of the work that's being done by either merchant acquirers or the merchants themselves to be ready for that. And whether or not the standard website can be that acceptance tool or if separate endpoints might be needed in certain cases. Any of that mechanic and the progress being made there would be much appreciated.

**Michael Miebach** (Executives):
Right. It's -- Tim, this is a wide, wide spectrum on kind of where merchants are on that. Take a small business that is -- just has moved from a physical-only business to having some sort of digital component of their business. They're going to need all the help they can get to set that up. And you take a large merchant, they're going to probably consider a first merchant or first agentic agent experience themselves and putting their own agent out there. 
So -- and everything in between. So the community of PSPs and ISVs and processors are going to be absolutely critical to cater to all of that. We will -- with our solutions, Agentic Pay, Agent Connect, et cetera, what we're solving for is that, the individual merchant will not have to go with one solution for one partner and with some other solution for some other partner because we're going to be that interface that deals with a lot of that. So that's kind of where we are. There's a lot of details and nitty-gritties in that. 
Our Chief Digital Officer, Jorn, loves talking about this in all the detail that you want, but currently that is the situation. So we are covering the base that we can cover as a network, and we're engaging the processor community to ensure that things like VCNs are only a bridge because that's not a good long-term solution. But some of these issues that you highlighted, Tim, need to be addressed because otherwise it's not going to take off, and we believe it will take off.

**Operator** (Operator):
Your next question is from the line of Sanjay Sakhrani with KBW.

**Sanjay Sakhrani** (Analysts):
I guess, Michael, it's been 3 months since the BVNK acquisition, and the stablecoin ecosystem continues to evolve. And I know there's a lot also happening with agentic as well. So I'm just curious like what your observations are with BVNK. Do you think the opportunity is sort of moving forward, any learnings? And obviously, any other types of deals you might do in the space?

**Michael Miebach** (Executives):
Right. Thanks, Sanjay. Always good to hear your voice. So BVNK, it closed between the last call and this call. So that's the first big piece. And we are very happy that it closed. We're getting really strong out of the gate from day 1. The joint new product that I referred to in my prepared remarks, the Global Money account is out there. So that takes our capabilities on the Mastercard side, our global reach, and it takes the stablecoin capabilities of send, receive, store, convert and puts it all together to enable our customers to choose between fiat and stablecoins on the other side for our [ customers' customers as well ]. So tremendous product, very good, great in demand. So this is really good. This just came at the perfect time on where the ecosystem is going.
BVNK, if I just go a step back and say, what are they doing for us? What is, in its simplest form, the reason for them to join us? And here it is, it's really providing that choice between and all these capabilities, send, receive, convert and store. That's very much it. But there are some other reasons for choosing BVNK and not choosing to build this our own. One is they have the full licensing footprint that is needed, and then have a very established compliance function. So if you do all the send and receive that you want, we want to make sure that it's totally fully compliant, very visible, easily managed too for our customers, and that we're very reliable taking that responsibility on. That's a piece. And the other is really the native talent in the digital asset space. So we now have a set of colleagues. So we just had our global leadership meeting and they were there. And you just see a very different mindset coming into Mastercard, which is excellent. 
So all those, so new product is out, different mindset is in, compliance is ready, and we're out in the market and we're seeing great demand. As this is very straightforward for our customers to say, all right. I want to somehow -- and let's take a bank. I have really no conversation with a bank CEO where this topic doesn't come up. What should I be doing in a digital asset space? Obviously, there's a bunch of banks who are very clear what they want to do, but there are many others who are not very clear, and they're asking us the question. Our crypto consulting team comes in. And of course, with BVNK, we can now not only offer consulting, but also cover a set of solutions. 
So people come in, and it's kind of an on-behalf service that BVNK provides, along with the money move capabilities that they have, but it's not just about stablecoin. So they want to choose for my customer that is a buyer in the United States and is importing from somewhere in Asia, what is the best way to send this money? And they might choose stablecoins or they might just choose something else, and we have all the rails together. So it comes at the perfect moment. BVNK bringing everything that we're looking for, but it's early days. We just closed in August, so we're 2 months in. Integration goes well. That's a nonissue. So we're ready to go.

**Operator** (Operator):
Your next question is from the line of Trevor Williams with FT Partners.

**Trevor Williams** (Analysts):
I wanted to ask on pricing. I think it was called out as a driver across pretty much every revenue line in the quarter. So it'd just be helpful to hear how sustainable you think this level of contribution from pricing is. And then just to clarify on the VAS growth in Q3, I know M&A was not material to total company growth, but how much of an impact BVNK had on the VAS growth rate in Q3 would be helpful.

**Ling Hai** (Executives):
Trevor, thank you. So first of all, regarding pricing. As we have told you before, we price for value. So we will always look for opportunities to price because we deliver value. And token pricing is probably a good example for me to illustrate this point. I feel -- like I said before, from a VAS perspective, especially, you have more room for penetration. You have new functionalities you can build, especially in the world of agentic. As you see, we're using MDES as the platform to enhance our token for the agentic world. And of course, there will be new use cases. 
So I think that ability for us to further penetrate existing customers, create new use cases and penetrate new verticals is there, and we'll price for the value we deliver. So that's going to be the first point. And of course, our pricing in Q3 has a component of previous pricing, but also some new pricing. We will expect some lapping of the pricing as we head into Q4, but again, we will continue to look for opportunities. You asked about VAS and impact from M&A. So I would say as far as BVNK is concerned, the impact is really minimal. It is a revenue-generating enterprise already, but it's off a small base.

**Operator** (Operator):
Your next question is from Fahed Kunwar with Rothschild & Co Redburn.

**Fahed Kunwar** (Analysts):
Could I just get an update on incentives? I think you talked about it last quarter being broadly stable. Sorry, slightly higher, and it came in pretty stable. Was there any deal timings affecting incentives? Can we expect any of the Q3 impact you thought would happen going into Q4? And any sense of how large the renewal cycle is for Mastercard going into 2027?

**Ling Hai** (Executives):
Thank you, Fahed, for the question. Let me take this one. Well, look, I have a tendency to call this a contra, but it's rebates and incentives. Well, this contra revenue is a reflection of our solid deal momentum. If that goes down, sometimes I worry about it. So that's one thing to keep in mind because the deals are what drive our business growth. And we have not given guidance for 2026, so I'm not going to do that. But as a reminder, though, we use rebates and incentives to drive volume and transaction onto the network. I'm just going to reiterate my flywheel point. 
You get the volume, then we deliver services on the volume, and then the services in turn become the differentiation that will drive even more volume. So we'll continue to do that. And we have been winning -- we have been winning deals and -- with new customers and expanding our customers in terms of our deal base. And -- but we've been very disciplined. We've been very disciplined and -- in terms of how -- what deals we want to win, what deals we want to walk away. We're not just going to win every deal, and we're not going to do that. We don't want to do that. 
We're going to win deals that gives us a higher growth momentum that's accretive to the growth trajectory. We're going to win deals that are additive to the cross-border flows, and we're going to win deals that will allow us to deliver services as well. So the punchline is we'll use R&I as a tool to drive the growth momentum and the growth algorithm. 
Now at the end of the day, I also want to remind everybody, we measure ourselves on driving net revenue growth and expanding overall net revenue yield, right? So R&I, in my mind, is an input, but the ultimate measurement should be net revenue yield. I also want to maybe take this moment to mention that for Q4, we would expect our rebates and incentives as a percent of gross assessments to be higher than Q3.

**Operator** (Operator):
Your last question will be from Dan Dolev with Mizuho.

**Dan Dolev** (Analysts):
I just had a question. I know you're not giving any formal guidance for '27, but maybe, given the strong exit rates that you've highlighted, like anything that we should keep in mind, especially as we're lapping things in 2026? I think it would be very useful for investors, any puts and takes on the growth and what we should expect. And congrats again on great results.

**Ling Hai** (Executives):
Yes. Okay. Let me also -- Dan, very nice to talk to you, but let me take this one as well. I also maybe want to quickly clarify, when I talk about guidance previously in my answer, I'm talking specifically about rebates and incentives. It's not so much '26 versus '27. So it is rebates and incentives, which we don't guide. But for '27, I guess, Dan, maybe the first answer is we're going to give our formal guidance in our next quarter's release, so please stay tuned. We'll get into the detailed discussion. Now remember, there are so many puts and takes in our business throughout the year, and there are just so many different factors at play. So sometimes it's really hard to say, hard to predict. The macro environment can play a role. Wins and losses can play a role. 
Demand for our VAS can play a role, right? We have to continue to develop new things and drive new penetration. FX volatility, that's another factor. And just so many other things. And the other thing I would say, yes, you're right, some of the headwinds can become tailwinds, but some of the tailwinds can also become headwinds because they're lapping. So there's all those things. So all I can say is we have a very strong business model. We have a very diversified business model. We are optimistic about the future, but do stay tuned for 2027.

**Devin Corr** (Executives):
Thank you very much. Michael, any closing comments?

**Michael Miebach** (Executives):
Yes. And Dan, thanks for the question. That's a great question to end the call on. So thank you again for all of your questions and all your support in the past quarter, and we look to talk to you over the coming quarter as we engage. All of these strong results, not possible without the amazing team at Mastercard. So I want to thank all of our colleagues around the world who make this happen every day. And I want to close this first call with Ling Hai. Thank you very much, and we'll speak to you next quarter. Thank you. Bye-bye.

**Ling Hai** (Executives):
Thank you all.

**Operator** (Operator):
This concludes today's call. Thank you for attending, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MA_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Sachin Mehra｜guidance：CFO 給 Q3 淨收入成長指引：幣別中性、排除併購後落在低雙位數區間的高端（原話："expected to be at the high end of low double-digit"）
- 2026-07-30｜Sachin Mehra｜guidance：全年淨收入指引區間不變，但表示因上半年較強，預期落在區間內較高位置（原話："we now expect to be higher within the range than"）
- 2026-07-30｜Sachin Mehra｜guidance：Q3 營業費用成長指引為低雙位數，並有 0.5 ppt 併購逆風（原話："Q3 growth to be at the low double-digits range versus"）
- 2026-07-30｜Sachin Mehra｜guidance：Q3、Q4 非 GAAP 稅率預期 20%–21%（原話："20% to 21% for both Q3 and Q4."）
- 2026-07-30｜Sachin Mehra｜guidance：全年外匯對淨收入預期為約 1 ppt 順風；Q3 則為約 0.5 ppt 逆風（原話："a tailwind of approximately 1 ppt from foreign exchange."）
- 2026-07-30｜Sachin Mehra｜guidance：下半年基本情境假設消費維持健康，且中東衝擊維持 Q2 末水準（原話："our base case continues to assume spending remains healthy."）
- 2026-07-30｜Sachin Mehra｜guidance：Q3 回扣與誘因占網路評估費的比率預期略高於 Q2（原話："slightly higher than it was in Q2."）
- 2026-07-30｜Sachin Mehra｜guidance：BVNK 收購預期 Q3 完成，淨收入影響極小、營業費用有些影響，皆已納入指引（原話："Minimal impact from a net revenue standpoint."）
- 2026-07-30｜Sachin Mehra｜margin：Q2 營業費用成長 10%（含處分 1 ppt 效益），營業利益成長 14%，淨利 16%、EPS 19%（原話："Operating expenses increased 10%, including a 1 ppt benefit"）
- 2026-07-30｜Sachin Mehra｜margin：費用成長主因為執行策略優先事項的支出：強化基礎設施、地理擴張、產品創新（原話："to further harden our infrastructure, geographic expansion"）
- 2026-07-30｜Sachin Mehra｜margin：Q2 EPS 5.04 美元，含 0.14 美元回購貢獻（原話："EPS was $5.04, which includes a $0.14 contribution from"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：國內評估費成長 10% 對 GDV 成長 8%，差距主要來自定價（原話："The 2 ppt difference is primarily"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：跨境評估費成長 20% 對跨境量 12%，差距 8 ppt 主要來自國際市場定價與組合（原話："The 8 ppt difference is driven primarily by pricing in"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：交易處理評估費 12% 對交易筆數 9%，差距來自組合與定價，部分被 FX 波動帶來的較低收入抵銷（原話："due to favorable mix and pricing, partially offset by lower"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：美國借記 GDV 成長 1%，剔除 Capital One 遷移後為 8%（原話："our U.S. debit GDV growth would have been 8%."）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：網路評估淨收入成長 8%，VAS 成長 18%（原話："Payment network net revenue increased 8%,"）
- 2026-07-30｜Michael Miebach｜margin：數字口徑：VAS 約 60% 淨收入與網路連結（network linked）（原話："about 60% of our value-add services and solutions net"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：Q2 上行來源含委內瑞拉跨境支出回升（中東衝擊較預期輕、VAS 需求強）（原話："an uptick in cross-border spend out of Venezuela"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：美國排除 Capital One 後交換量成長 10%，較上季高 2 ppt，歸因於燃油支出與整體消費（原話："U.S. switched volume growth was 10% or 2 ppt"）
- 2026-07-30｜Sachin Mehra｜capital_allocation：Q2 回購 49 億美元，另至 7/27 再回購約 7 億美元（原話："we repurchased $4.9 billion worth of stock and approximately"）
- 2026-07-30｜Michael Miebach｜capital_allocation：預期本季完成 BVNK 收購，定位為可信的互通層（原話："We expect to close the BVNK acquisition this quarter."）
- 2026-07-30｜Devin Corr｜capital_allocation：IR 宣布 Ling Hai 8/3 起接任 CFO（Sachin Mehra 轉任 Chief Business Officer）（原話："incoming CFO effective August 3."）
- 2026-07-30｜Sachin Mehra｜commitment：管理層表示不追求無利潤的量；舉放棄 Lloyds Credit 為例（原話："Volume for the sake of volume is not what this company"）
- 2026-07-30｜Sachin Mehra｜commitment：管理層稱只追求能提高淨收入收益率（net revenue yield）的量（原話："Profitable volume, which is"）
- 2026-07-30｜Michael Miebach｜commitment：對在地交換合作設定條件：須技術可行、經濟上合理（原話："the give and take has to work for us."）
- 2026-07-30｜Michael Miebach｜commitment：Open USD 預計年內上線，且 Mastercard 稱會同時支援多種幣別（原話："Open USD is set to go live later this year."）
- 2026-07-30｜Michael Miebach｜competition：交換滲透率升至 72%，管理層歸因於相對在地網路的價值主張（原話："switching penetration now reaching 72%."）
- 2026-07-30｜Michael Miebach｜competition：阿聯酋：與央行子公司合作建置國內交換，Mastercard 為 Jaywan 聯名信用卡的主要國際品牌，屬增量交易（原話："These transactions are incremental to what we process"）
- 2026-07-30｜Michael Miebach｜competition：歐洲被描述為高度競爭市場，數位歐元在籌備；目前以卡片主張為主，保留彈性（原話："Europe it's a very competitive market"）
- 2026-07-30｜Sachin Mehra｜competition：歐洲購買量成長從 2024 Q2 的 16% 放緩，管理層歸因於先前大型贏單的基期效應與放棄部分交易（原話："back in Q2 of"）
- 2026-07-30｜Michael Miebach｜competition：管理層稱 Mastercard 是唯一能做機器對機器支付的網路（原話："Mastercard is the only network enabling"）
- 2026-07-30｜Michael Miebach｜product：穩定幣定位：對 B2B 與 P2P 有明確效用，P2M 無待解問題（原話："but no problem to solve"）
- 2026-07-30｜Michael Miebach｜product：代理式商務：管理層預期卡片在代理世界仍佔優（原話："we expect cards will prevail in an agentic world"）
- 2026-07-30｜Michael Miebach｜product：加密聯名卡量兩年增逾三倍（原話："Our crypto co-brand"）
- 2026-07-30｜Michael Miebach｜product：Threat Intelligence 前三季辨識逾 700 萬筆卡片測試交易，估計阻止 1.72 億美元詐欺（原話："prevented an estimated $172 million in fraud linked to"）
- 2026-07-30｜Sachin Mehra｜product：代幣滲透率逾 40%（非接觸 80%，卡片成長 5%）（原話："token penetration reached over 40% of all switched"）
- 2026-07-30｜Michael Miebach｜customer：上半年贏得數百筆轉換與擴約，預期未來十年帶來數兆美元增量交易量（原話："which are expected to drive trillions of dollars in"）
- 2026-07-30｜Michael Miebach｜customer：續約 JPMorgan Chase Freedom Flex 與 Banamex（原話："renewed a key partnership"）
- 2026-07-30｜Michael Miebach｜customer：過去 12 個月淨新增逾 2.3 億張 Mastercard（原話："added over 230 million net new Mastercards"）
- 2026-07-30｜Michael Miebach｜customer：商用借貸記量成長 12%（原話："commercial debit and credit volumes grew at 12%"）
- 2026-07-30｜Sachin Mehra｜customer：美國消費廣泛健康，涵蓋信用與借記、消費與商用，大眾與富裕客群皆穩，富裕端成長較高（原話："it's broad-based. We see it across credit and debit."）
- 2026-07-30｜Michael Miebach｜risk：管理層持續監控地緣政治與其潛在經濟影響（原話："monitor geopolitical uncertainty and its potential"）
- 2026-07-30｜Sachin Mehra｜risk：中東情勢仍具動態性，管理層以多元化業務作為緩衝（原話："the environment in the Middle East remains dynamic."）
- 2026-07-30｜Sachin Mehra｜risk：Q2 跨境強勁部分來自委內瑞拉美元可得性提高（2018 年已解併）（原話："increased availability of U.S. dollars"）
- 2026-07-30｜Sachin Mehra｜risk：美國成長受惠於較高燃油價格；世界盃可能有貢獻但無法量化（原話："a tailwind, which has come on account of higher fuel prices"）

### 問答異常語氣（迴避／改口／保留）
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Sanjay Sakhrani 問跨境 4–6 月加速的幅度是否受世界盃影響、是否會回落｜答法：未直接回答世界盃占比與是否回落；稱「難以辨識是否與世界盃有關」，改談中東復甦與委內瑞拉
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Tien-Tsin Huang 問美國 10% 成長是否有持續力、是否廣泛｜答法：承認燃油價格與世界盃有貢獻但稱無法量化，未給持續性判斷，轉述基本面健康
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Andrew Jeffrey 問阿聯酋式國內交換還會鎖定哪些市場、歐洲是否適用｜答法：未點名其他目標市場，稱各地有「不同版本」，並強調須符合經濟原則；歐洲「目前」以卡片為主但保留彈性
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Harshita Rawat 問歐洲購買量成長減速的原因與未來成長｜答法：以基期效應與放棄 Lloyds 等交易解釋，未給歐洲未來成長數字或區域指引
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Tim Chiodo 問 VAS 中安全類占比是否更新（先前約 40%）｜答法：未提供安全類占比數字，只重申約 60% 網路連結並說收購不會顯著改變

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
{"date":"20260703","verdict":"進場","role":"核心持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"無現金化 secular 滲透持續 + V/MA 雙寡頭定價權維持（卡網路仍是陌生人信任層的主軌）","columns":{"2Y 驗證點":"GDV YoY lc &ge; +7%、switched txns &ge; +9%","5Y 驗證點":"MA 處理筆數複合 &ge; +8%/yr；net take rate 不下滑","10Y 驗證點":"穩定幣/A2A 占 MA 可及流量 &lt; 5%（繞道未跨門檻）","具體數字門檻":"Q1 FY26：GDV +7%lc、switched txns +9%（達標）","信息來源":"MA FY26 Q1 法說（2026-04-30）、MA Investor Day 2025","漂移觸發條件":"net take rate 連 4 季下滑 或 A2A 占比 &ge; 5% → 反轉（5Y 假設，QC-35 連 4 季）"}},{"id":"H2","text":"跨境復甦 + VAS/Move 高速成長兌現 15-16% EPS CAGR（三引擎接力）","columns":{"2Y 驗證點":"跨境 YoY cc &ge; +10%；VAS cc &ge; +15%；Move &ge; +30%","5Y 驗證點":"VAS 占 Rev &ge; 40%；Move 年化 &ge; $8T","10Y 驗證點":"VAS 占 incremental revenue &ge; 55%；Move $15T+","具體數字門檻":"Q1 FY26：跨境 +13%cc、VAS +18%cc、Move +32%（達標）","信息來源":"MA FY26 Q1 法說、MA Investor Day 2025、Mastercard Move whitepaper","漂移觸發條件":"跨境連 2 季 &lt; +8% 或 VAS 連 4 季 cc &lt; +15% → 削弱（QC-34/35）"}},{"id":"H3","text":"估值從 5Y 低位（Fwd PE 23.7x）修復（板塊 de-rate 過度、基本面加速被錯殺）","columns":{"2Y 驗證點":"Fwd PE 分位回升至 5Y 中段（&ge; 40th）","5Y 驗證點":"倍數回到 26-30x（A 級複利應得）","10Y 驗證點":"非依賴 re-rate；EPS 複利本身即達標","具體數字門檻":"當前 Fwd PE FY27 23.7x = 5Y ~5th 分位（5Y 區間 24-40x）","信息來源":"yfinance / GuruFocus 5Y forward PE band、本報告 §11.1","漂移觸發條件":"此為市場假設，非動作觸發；若倍數不修復但 EPS 複利，報酬仍 12-13%（§11.6 非估值依賴）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"全球旅遊 + 跨境放緩（MA 比 V 對跨境更敏感；管理層 Q1 已示警 4 月起 YTD cross-border 減速）","columns":{"對應假設":"H1/H2","時間尺度":"⚡→🔥 短中期（1-2 季可觸發，4-6 季確認）","監測指標":"MA 跨境體積 YoY cc、UNWTO 國際旅客增速、單月消費信心","警戒閾值":"連 2 季跨境 YoY cc &lt; +8% → 削弱"}},{"id":"R2","text":"DOJ v Visa（借記壟斷案）連帶 + FTC 對 MA 推 consent decree / interchange 監管收緊","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"DOJ v Visa 進度（fact discovery 2026-10-16 截止、expert discovery 至 2027-04-08 → 裁決預估 2027-2028；惟 2026-06 已有法院初步核准的 Equitable Relief 和解對 V/MA 皆具約束，近期訴訟尾部偏降溫）；FTC 是否啟動 MA inquiry；CCCA 2026（Durbin/Marshall 重提、傳獲行政部門支持，歷來最接近通過）；歐盟 interchange 上限","警戒閾值":"① V 遭強制拆分/重大和解 → MA 連帶 reprice 向 18x；② FTC 對 MA 啟動 inquiry → 立即重評"}},{"id":"R3","text":"穩定幣 / A2A / Capital One-Discover 三軌結構替代（繞卡去中介化）","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數，需 &ge; 50% 機率才砍倉）","監測指標":"① 穩定幣（USDC/USDT）商戶結算量；② A2A（Pix/UPI/FedNow/Wero）在主力市場的消費滲透；③ Capital One 把 credit 卡量遷至 Discover 網路的比例；④ MA net take rate 趨勢","警戒閾值":"① 穩定幣/A2A 結算量達 MA 可及流量 5%；② Capital One 把 &gt; 20% credit 卡轉至 Discover；③ MA net take rate 連 4 季結構下滑"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":13.0,"ev5y_pct":75.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心持倉","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":7.0,"ev5y_pct":75.0,"irr_base_pct":13.0,"max_dd_pct":-45.0,"bull_5y_price":1310.0,"bear_5y_price":405.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":539.39,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
