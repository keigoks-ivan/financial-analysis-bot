你是 stock-analyst **v20 判斷 agent**，標的 ALV（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ALV","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":2693,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm"}},{"id":"f_kpi1_adjusted_operating_incom","label":"Adjusted operating income / margin (non-GAAP)","value":9.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","citation":"公司 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":9.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","citation":"公司 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm"}},{"id":"f_kpi3_free_operating_cash_flow","label":"Free operating cash flow","value":124,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","citation":"公司 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm"}},{"id":"f_kpi4_diluted_eps_gaap_adjuste","label":"Diluted EPS (GAAP / adjusted)","value":2.13,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-23）","citation":"公司 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm"}},{"id":"f_kpi5_management_guidance_fy20","label":"Management guidance FY2026","value":"adj. operating margin 約 10.5%；organic 約 0%；OCF 約 $1.2B","period":"Q3 2026（公告於 2026-10-23）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（公告於 2026-10-23）","citation":"公司 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-23","period":"2026-10-23","unit":"date","basis":"距今 1 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-23"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_alv_gross_margin_pct","label":"ALV 毛利率","value":19.22,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_alv_operating_margin_pct","label":"ALV 營業利益率","value":9.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_alv_fcf_margin_pct","label":"ALV FCF 利潤率","value":6.83,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_600699_ss_gross_margin_pct","label":"600699.SS 毛利率","value":18.12,"period":"TTM ending 2026-03-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.600699.SS.gross_margin_pct","as_of":"TTM ending 2026-03-31（4季加總）"}},{"id":"f_peer_600699_ss_operating_margin_pct","label":"600699.SS 營業利益率","value":5.81,"period":"TTM ending 2026-03-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.600699.SS.operating_margin_pct","as_of":"TTM ending 2026-03-31（4季加總）"}},{"id":"f_peer_600699_ss_fcf_margin_pct","label":"600699.SS FCF 利潤率","value":0.64,"period":"TTM ending 2026-03-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.600699.SS.fcf_margin_pct","as_of":"TTM ending 2026-03-31（4季加總）"}},{"id":"f_peer_mga_gross_margin_pct","label":"MGA 毛利率","value":14.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_operating_margin_pct","label":"MGA 營業利益率","value":5.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_fcf_margin_pct","label":"MGA FCF 利潤率","value":7.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_gross_margin_pct","label":"LEA 毛利率","value":6.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_operating_margin_pct","label":"LEA 營業利益率","value":3.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_fcf_margin_pct","label":"LEA FCF 利潤率","value":3.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":114.67,"period":"2026-10-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-1.23,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":48.21,"period":"2026-10-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.78,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.24 → 10.32）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.43,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.64 → 11.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.3,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.15 → 13.19）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":10.32,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":11.59,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":13.19,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.88,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 10.13 → 10.32（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":13.78,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝45.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":45.4,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.75,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝35.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":35.1,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.92,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝41.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":41.9,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":11.11,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 10.32，分子＝快照價 114.67","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.276,"period":"2026-10-24","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-24"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1891.0,"period":"2026-10-24","unit":"USD m","basis":"yfinance 最新一季：總債務 2088.0、現金 197.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":72.01,"period":"2026-10-24","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":10148.01,"period":"2026-10-24","unit":"USD m","basis":"市值 8257.01 ＋ 淨負債 1891.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":11101.11,"period":"2026-10-24","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":11371.0,"period":"2026-10-24","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.91,"period":"2026-10-24","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 114.67 / W52 117.26 / W104 108.92 / W250 95.31 / W250 13週斜率 0.4%"},{"id":"f_ma_w52","label":"52 週均線","value":117.26,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":108.92,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":95.31,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.4,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Autoliv 全球被動安全份額由 1997 年 27% 升至 2025 年約 44%；安全帶約 45%、氣囊＋方向盤約 44%","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"This has enabled Autoliv to increase its global market share in passive safety from 27% in 1997 to around 44% in 2025.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列出的其他競爭者為日本 Nihon Plast、Ashimori，中國 Yanfeng、Jinheng，韓國 Samsong，南美 Chris Cintos；合計佔其餘多數份額","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"Other competitors include Nihon Plast and Ashimori in Japan, Yanfeng and Jinheng in China, Samsong in South Korea, and Chris Cintos de Seguranca in South America.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"中國本土車廠佔 Autoliv 中國銷售由 2022 年 22% 升至 2025 年 44%；BYD 高度垂直整合，被動安全由子公司 FinDreams 供應，Autoliv 僅供應零件（主要為氣體產生器）","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"BYD has a uniquely high degree of vertical integration, with a large proportion of in-house sourcing of products and systems. This includes passive safety systems, which is supplied by its subsidiary FinDreams Technology. Autoliv supplies components, especially inflators, to FinDreams Technology.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：亞洲（中國、韓國、印度）競爭激烈，預期有更多國際與本土競爭者進入，可能導致降價、毛利下降與無法維持份額","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"We anticipate that additional competitors, both international and domestic, may seek to enter the Chinese, South Korean, and/or Indian markets resulting in increased competition.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Q3 2026：Autoliv 對中國本土 OEM 銷售有機成長約 21%，對全球 OEM 下降約 29%；本土 OEM 佔中國銷售 58%（去年同期約 46%）","source":"SEC EDGAR 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm","excerpt":"Autoliv's sales to domestic OEMs increased organically by around 21% while our sales to global OEMs decreased by around 29%. Chinese OEMs accounted for 58% of our sales in China in the quarter, compared to around 46% a year ago.","as_of":"2026-10-23","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Moody's 2026-06：Autoliv 區域份額歐洲 52%、美洲 47%、中國 33%；主要競爭者為 ZF 與 Joyson Safety Systems","source":"Moody's Credit Opinion June 2026 (autoliv.com)","url":"https://www.autoliv.com/sites/autoliv/files/2026-07/Credit%20Opinion%20June%202026.pdf","excerpt":"Q1 2026) are particularly high at 52% and 47%, respectively, compared with a 33% share in China (19% of group revenue in LTM Q1 2026). The company’s main competitors are ZF Friedrichshafen AG (Ba2 negative) and Joyson Safety Systems.","as_of":"2026-06-30","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：最大單一客戶合約約占合併營收 2%，前五大客戶約 44%、前十大約 70%；未揭露特定客戶導入第二供應商或自製的事件。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"In 2025, our top five customers represented around 44% of our consolidated sales, and our largest customer contract accounted for around 2% of our consolidated sales.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-Q 稱 BYD 高度垂直整合，被動安全系統由子公司 FinDreams 供應（Autoliv 供應氣體產生器）；Toyota 關係企業（Toyota Gosei）與 Hyundai Mobis 取得母廠大部分業務。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526306974/alv-20260630.htm","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 前五大客戶約占合併淨銷售 44%、前十大約 70%；最大單一客戶合約約占 2%。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"In 2025, our top five customers represented around 44% of our consolidated sales, and our largest customer contract accounted for around 2% of our consolidated sales.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2025 年無單一客戶占淨銷售 10% 以上；前十大約 70%。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"Sales to individual customers representing 10% or more of net sales were: In 2025: No individual customer representing 10% or more.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"中國本土 OEM 占 Autoliv 中國銷售比重由 2022 年 22% 升至 2025 年 44%；比亞迪成長 2025 年明顯放緩，且高度垂直整合，Autoliv 供應其子公司 FinDreams 零組件（主要為氣體產生器）。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"In 2022, this group accounted for 22% of Autoliv's sales in China, and in 2025 their share of Autoliv sales in China was 44%.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Moody's 2026 年 6 月信用意見：Autoliv Baa1、展望穩定。","source":"Autoliv Investor Relations, Credit Opinion June 2026 (Moody's)","url":"https://www.autoliv.com/sites/autoliv/files/2026-07/Credit%20Opinion%20June%202026.pdf","excerpt":"Baa1 Type LT Issuer Rating - Dom Curr Outlook Stable Please see the ratings section at the end of this report for more information. The ratings and outlook shown reflect information as of the publication date. Autoliv, Inc.'s (Autoliv) Baa1 long-term issuer rating is strongly positioned, supported by its leading position in the passive safety market, with a global","as_of":"2026-06-24","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Autoliv 2026年5月宣布逐步關閉土耳其廠（方向盤、氣囊、安全帶），管理層判斷EMEA產能超過未來需求；全面關廠預計2028上半年，重組費用約1.42億美元，2027起年化稅前節省4,000萬美元、2028達滿額","source":"Autoliv press release 'Autoliv to Discontinue Manufacturing Operations in Türkiye' (PRNewswire) / Q3 2026 8-K","url":"https://tools.prnewswire.com/en-us/live/20813/release/20260508EN54815","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q3 2026 有機銷售-1.1%，全球LVP-1.9%；亞洲(不含中國)與中國分別優於LVP 2.5pp與1.1pp，EMEA落後3.7pp；2026指引約0%有機成長、調整後營業利益率約10.5%","source":"Autoliv 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm","excerpt":null,"as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2 2026：有機銷售+1%、全球LVP-0.3%；印度有機銷售+36%，管理層歸因主要為單車安全內容增加；Moody's估Autoliv被動安全全球份額約44%","source":"Nasdaq 'Autoliv Q2 earnings call highlights'; Moody's Credit Opinion June 2026","url":"https://www.nasdaq.com/articles/autoliv-q2-earnings-call-highlights","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"EC 反壟斷調查已於 2019 年結案；目前仍有一名客戶在德國提起的民事反壟斷訴訟（涉及十多年前的指控），未來其他允許民事求償的國家也可能出現類似訴訟","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"We have previously been the subject of an investigation by the European Commission (“EC”) regarding possible anti-competitive behavior among certain suppliers to the automotive vehicle industry that was resolved in 2019. We are subject to a civil antitrust lawsuit in Germany filed by a customer with respect to allegations over a decade ago","as_of":"2026-02-19","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 法律程序章節僅泛稱一般營運中的訴訟，並指向附註 19；未列出新的政府反壟斷或拆分調查","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"In the ordinary course of its business, the Company is subject to legal proceedings brought by or against the Company and its subsidiaries.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"BMW 在德國對 Autoliv 提起損害賠償訴訟，求償 6,300 萬歐元加利息（合計約 9,500 萬歐元），源自 EC 調查所涉行為","source":"SEC EDGAR 10-Q 2026Q3","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429588/alv-20260930.htm","excerpt":"2024, BMW filed a complaint against the Company in Germany claiming damages of €63 million plus interest (for a total claim of approximately €95 million) related to the conduct at issue in the EC investigation (the \"BMW Complaint\"). BMW is one of two European OEMs for which the Company pled guilty in 2017 in relation to the EC investigation. The Company filed its statement of defense on June","as_of":"2026-10-23","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025：2025年新關稅未對獲利造成重大衝擊，客戶補償超過80%的關稅成本；含回收稀釋效應，營業利益率約受-20bps影響；2026年指引假設關稅與貿易限制較2026-01-23生效狀態無重大變動。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"The effects of the new tariffs imposed in 2025 did not have a significant impact on our profitability in 2025, as we achieved customer compensations for more than 80% of tariff costs. Including the dilutive effect of recovered tariffs, operating margin was negatively impacted by around 20 bps.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K風險因子：半導體與感測器採購依賴全球電子供應鏈，受出口管制、實體清單限制與制裁影響；關稅成本在固定價或終身定價合約下可能無法完全轉嫁。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"Semiconductor and sensor sourcing relies heavily on global electronics supply chains, which are increasingly affected by export controls, entity‑list restrictions, and sanctions targeting technology supply routes.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Q3 2026 10-Q：客戶補償超過80%關稅成本，淨負面影響約$6M；全年關稅對營業利益率稀釋預計與2025年相近約20bps。","source":"SEC EDGAR 10-Q FY2026 Q3","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429588/alv-20260930.htm","excerpt":"We achieved customer compensation for more than 80% of the tariff costs, resulting in a net negative impact after compensation of around $6 million, in line with the net impact in the third quarter of 2025.","as_of":"2026-10-23","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Q1 2026 10-Q：被最高法院推翻之IEEPA關稅，ALV毛曝險約$25M、淨曝險遠低於$10M；Q2回收淨正面約$3M。","source":"SEC EDGAR 10-Q FY2026 Q1","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526160472/alv-20260331.htm","excerpt":"Supreme Court's ruling that the International Emergency Economic Powers Act did not authorize the imposition of the tariffs in 2025, as our gross exposure is limited to around $25 million and the net exposure is well below $10 million.","as_of":"2026-04-30","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"RBC：管理層表示Section 232金屬修訂對Autoliv關稅狀況無重大影響。","source":"Placera/RBC Autoliv Q1 note","url":"https://www.placera.se/telegram/autoliv-s-q1-beat-driven-by-forex-and-china-india-performance-fuels-2026-expectations-rbc-says-20260420","excerpt":"Management also clarified that the section 232 revision on metals does not meaningfully impact Autoliv's tariff position, the note added. RBC said Autoliv is the best quality auto supplier in its coverage, given its market position and product offering versus competitors.","as_of":"2026-04-20","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q 風險因子：單一小型零組件缺貨即可迫使公司停產某產品、可能持續很久；列舉原因含供應商停工與貿易限制，並提到氣體產生器推進劑可能遇進出口許可問題","source":"Autoliv 10-Q (period 2026-09-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429588/alv-20260930.htm","excerpt":"The unavailability of even a single small subcomponent necessary to manufacture one of the Group's products, for whatever reason, could force the Group to cease production of that product, possibly for a prolonged period.","as_of":"2026-10-23","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q3 2026 財報：客戶拉貨準確度轉差，歸因中國發展；關稅成本已回收逾 80%，每季淨影響約 6–7 百萬美元","source":"Autoliv 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm","excerpt":"Customer call-off accuracy deteriorated slightly compared to Q3 2025 as well as compared to Q2 2026, driven by development in China. We expect call-off volatility for the full year 2026 on average to be slightly improved compared to 2025. However, the continued significant uncertainty in the geopolitical environment and future changes in tariffs and trade restrictions may","as_of":"2026-10-23","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 淨銷售 $2,693M，有機成長 -1.1%，優於全球 LVP -1.9% 約 0.8pp；亞洲（印度有機 +29%）強、EMEA 落後 LVP 3.7pp","source":"Autoliv 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm","excerpt":"Net sales decreased organically* by 1.1% , which was 0.8pp higher than the global LVP decrease of 1.9%","as_of":"2026-10-23","retrieved_at":"20261024","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"對中國本土 OEM 銷售有機約 +21%，對全球 OEM 約 -29%（客戶組合轉移）","source":"Autoliv 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm","excerpt":"Autoliv's sales to domestic OEMs increased organically by around 21% while our sales to global OEMs decreased by around 29%.","as_of":"2026-10-23","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"2026 全年指引：有機成長約 0%、調整後營業利益率約 10.5%、營運現金流約 $12 億","source":"Autoliv 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm","excerpt":"Full year 2026 guidanceAround 0% organic sales growthAround 2.5% positive FX impact on net sales","as_of":"2026-10-23","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Moody's 2026-06 信評意見估 Autoliv 被動安全全球市佔 44%；氣囊/方向盤等占營收 67%、安全帶等 33%（未找到產品單價走勢資料）","source":"Autoliv site – Moody's Credit Opinion June 2026","url":"https://www.autoliv.com/sites/autoliv/files/2026-07/Credit%20Opinion%20June%202026.pdf","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"S&P Global Mobility 預估 2027 全球輕型車產量約 93.37M 台，年增 1.55%","source":"ECG Market Outlook 2026","url":"https://www.ecgassociation.eu/wp-content/uploads/2026/02/ECG-Business-Intelligence_-Market-Outlook-2026-for-Cars-and-Light-Commercials-Fleet-Transport.pdf","excerpt":"year, but will see a 1.55% annual increase in 2027 with volume production to hit 93.37 million units across the globe. By year end 2029, global light vehicle production is expected","as_of":"2026-02-01","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 風險因子：被動安全市場競爭激烈，公司表示能否持續創新並把握新興技術是維持競爭力的關鍵；文件未點名任何可取代氣囊／安全帶的替代技術。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"Our ability to compete successfully depends, in large part, on our success in continuing to innovate and manufacture products that have commercial success with our customer and end-consumers","as_of":"2026-02-19","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Autoliv 與 Adient 合作因應自駕車非傳統座椅姿態的被動安全設計，安全帶仍是主要約束手段（舊資料，2018）。","source":"DBusiness: Adient, Autoliv to Collaborate on Vehicle Seating Challenges for Autonomous Vehicles","url":"https://www.dbusiness.com/daily-news/adient-autoliv-to-collaborate-on-vehicle-seating-challenges-for-autonomous-vehicles/","excerpt":null,"as_of":"2018-01-01","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"經查未見 Autoliv 銷售通路／商業模式（訂閱化、D2C、平台化）結構性轉變的一手紀錄；客戶結構上，2026 Q2 對中國本土 OEM 銷售有機成長約 44%，對全球 OEM 下滑約 24%，中國 OEM 占中國銷售 55%（去年同期約 40%）。","source":"Autoliv 10-Q（2026-06-30 季）","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526306974/alv-20260630.htm","excerpt":"Autoliv's sales to domestic OEMs increased organically by around 44% while our sales to global OEMs decreased by around 24%.","as_of":"2026-07-24","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026-07-08 Autoliv 與小鵬簽策略合作框架，CTO 稱關係由傳統供應轉向共同創新與共同開發。","source":"Gasgoo：Autoliv, XPENG Group Sign Strategic Cooperation Agreement","url":"https://autonews.gasgoo.com/articles/news/autoliv-xpeng-group-sign-strategic-cooperation-agreement-2075470264752984065","excerpt":"the collaboration is evolving from a conventional supply relationship into a model focused on joint innovation and co-development.","as_of":"2026-07-08","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2025 年亞洲 OEM 占合併淨銷售約 48%，中國 OEM 約 8%，歐洲品牌 30%，美系 20%；銷售仍為直接對 OEM。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"As a group Asian OEMs represented around 48% of the Company's consolidated net sales in 2025, of which Japanese OEMs accounted for almost two thirds.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026 發布的全年指引：有機成長約 0%、匯率約 +2.5%、調整後營業利益率約 10.5%、營運現金流約 $1.2B；7 月指引為 10.5-11%，即利益率落在原區間下緣","source":"Autoliv 8-K Ex99.1 (Q3 2026 earnings release)","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm","excerpt":null,"as_of":"2026-10-23","retrieved_at":"20261024","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026 銷售 $2,693M（-0.5%），有機 -1.1%，調整後營業利益率 9.7%，稀釋 EPS $2.13（-6.8%）","source":"Autoliv 8-K Ex99.1 (Q3 2026 earnings release)","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm","excerpt":null,"as_of":"2026-10-23","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價共識平均約 $134.71（stockanalysis，as of 2026-07-30；Investing.com 17 位分析師，高 148／低 118，12 買／6 持有／0 賣）；Benzinga 9 月列平均 $131（19 位，Neutral）。皆為 Q3 財報前資料","source":"stockanalysis.com / Investing.com / Benzinga","url":"https://stockanalysis.com/stocks/ALV","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"TD Cowen 於 2026-09-08 由 Buy 降至 Hold，目標價 $148→$137；BofA 於 Q2 後目標價 $140→$134 維持 Buy","source":"Benzinga / Investing.com 彙整","url":"https://www.benzinga.com/quote/ALV/sentiment","excerpt":null,"as_of":"2026-09-08","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026 全年營收共識 $11.15B，與公司指引約 $11.14B 一致（7 月 Q2 後）；Q4 利益率改善依賴客戶補償與工程收入","source":"Nasdaq/Zacks 與搜尋彙整","url":"https://www.nasdaq.com/articles/alv-stock-buy-now-or-hold-margin-risks-build-2026","excerpt":null,"as_of":"2026-07-17","retrieved_at":"20261024","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-05-11 8-K 含 Item 2.05（退出/處分成本）與 2.06（重大減損）；公司 2026-05-08 宣布逐步退出土耳其製造，EMEA 產能調整最終稅前費用約 $142M（搜尋摘要所述，未逐字核對原文）","source":"SEC EDGAR 8-K（2026-05-11，Item 2.06）","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526216107/alv-20260506.htm","excerpt":"Item 2.06 Material Impairments.\nThe information contained in Item 2.05 above is incorporated herein by reference.","as_of":"2026-05-11","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"Autoliv 為 ARC 安全氣囊氣體產生器產品責任集體訴訟（MDL 3051）被告之一，公司否認指控，已判定損失為 reasonably possible，未計提且無法估計區間，程序仍在進行","source":"SEC EDGAR 10-K FY2025 Item 8 Contingent Liabilities","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"The Company has determined pursuant to ASC 450 that a loss is reasonably possible with respect to the ARC Inflator Class Action. However, the Company continues to evaluate this matter, no accrual has been made, and no estimated range of potential loss can be determined at this time.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 8-K 共 11 份，含重大項目者 3 份（2026-05-11 的 2.05/2.06、2025-10-29 的 1.01/2.03、2025-11-12 的 8.01 股息）；清單中無 2.01 併購完成或 4.02 重編","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001034670&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Autoliv Wuhu（安徽）新氣囊廠 2026-08-10 動工，預計 2027 年投產，採自動化產線。","source":"GDELT Cloud event: Autoliv breaks ground on new Wuhu airbag plant","url":"https://gdeltcloud.com/events/autoliv-breaks-ground-on-new-wuhu-airbag-plant--cameoplus_fe7b7bc1e09d8a79","excerpt":"Autoliv Wuhu Safety Systems broke ground on a new airbag plant in Jiujiang District, Wuhu City, Anhui Province. The facility will feature automated assembly lines and is expected to begin production in 2027.","as_of":"2026-08-10","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"GlobalData 2026 年 6 月被動安全報告：全球 OE 前氣囊 2026 年約 1.677 億顆，年複合成長約 1.3%，2033 年 1.837 億顆。","source":"GlobalData Sector Innovation Report: Passive Safety (ResearchAndMarkets)","url":"https://www.researchandmarkets.com/reports/6262412/sector-innovation-report-passive-safety","excerpt":"The Global Component volume of OE front airbags is estimated at 167.7 million units in 2026 and is expected to post a CAGR of 1.3% over the forecast period. The market is expected to reach 183.7 million units by 2033.","as_of":"2026-06-01","retrieved_at":"20261024","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Autoliv 2026 Q2 10-Q：淨資本支出年減 $20 million、占營收 3.4%，主因較少 footprint optimization 與產能擴張。","source":"Autoliv 10-Q Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526306974/alv-20260630.htm","excerpt":"The level of capital expenditure, net, in relation to sales declined to 3.4% versus 4.2% a year earlier. The lower level of capital expenditure, net is mainly related to the lower activity level of footprint optimization and less capacity expansion.","as_of":"2026-07-24","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Autoliv 8-K：逐步結束土耳其製造（方向盤、氣囊、安全帶），生產移至其他 EMEA 廠，稅前費用約 $142 million。","source":"Autoliv 8-K exhibit 99.3","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526216107/alv-ex99_3.htm","excerpt":"Autoliv to Discontinue Manufacturing Operations in Türkiye (Stockholm, Sweden, May 8, 2026) – Autoliv, Inc. (NYSE: ALV and SSE: ALIVsdb), the worldwide leader in automotive safety systems, continues its strategy to align production capacity with future EMEA market requirements. As part of this strategy, Autoliv will gradually discontinue its manufacturing operations in Türkiye.","as_of":"2026-05-01","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Joyson Safety Systems 匈牙利 Miskolc 工廠擴建，總投資 HUF 16 billion（補助 4.9 billion），稱將成全球最大被動安全工廠。","source":"autopro.hu","url":"https://autopro.hu/en/news/joyson-safety-systems-expands-production-activities-in-hungary-with-huf-16-billion-investment/235654","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"Q3 2026 10-Q：2026 全年原物料漲價毛衝擊估約 1.2 億美元（Q1 時估約 0.9 億），公司預期以降本、材料組合與客戶／供應商談判抵銷大部分","source":"Autoliv Form 10-Q (period ended 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429588/alv-20260930.htm","excerpt":"For the full year 2026, we currently estimate a gross impact of around $120 million from higher raw material prices.","as_of":"2026-10-23","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"Q4 2025 財報電話會：部分 OEM 因管理庫存而短通知或無通知停產","source":"Autoliv Q4 2025 earnings call transcript","url":"https://www.autoliv.com/sites/autoliv/files/pr/Autoliv%20Inc.%20Earnings%20Call%20Q4%202025_transcript%20Final.pdf","excerpt":"much related to some OEMs deciding to -- with very short notice or no noticeat all to stop production to manage the inventory situations. We also had some cases with some customers","as_of":"2026-01-30","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2008-09 下行：Autoliv 全年營業利益率由 2007 年 7.4% 降至 2008 年 4.7%、2009 年 1.3%；2009 營業利益 6,900 萬美元，較 2008 年 3.06 億美元降 78%；2009 銷售 51.2 億美元年減 21%，毛利率 16.6%（搜尋摘要轉述，未核原文）。","source":"SEC Form 10-K FY2009 exhibit 13 (Autoliv Inc)","url":"https://www.sec.gov/Archives/edgar/data/0001034670/000119312510035083/dex13.htm","excerpt":null,"as_of":"2010-02-01","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2020 疫情：第二季銷售年減 51%，營業利益由第一季 1.7 億美元轉為第二季虧損 2.34 億美元；毛利率年減 17.2 個百分點；下半年因降本與銷售回升獲益，公司取消股利（搜尋摘要轉述，未核原文）。","source":"SEC Form 8-K Q2 2020 / Form 10-K FY2020 (Autoliv Inc)","url":"https://www.sec.gov/Archives/edgar/data/1034670/000156459020032534/alv-ex991_7.htm","excerpt":null,"as_of":"2020-07-17","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2022 供應鏈／原料成本壓力：全年調整後營業利益率 6.8%（2021 為 8.3%）；第一季調整後僅 3.2%，主因原料成本、供應鏈中斷與輕型車產量波動（搜尋摘要轉述，未核原文）。","source":"SEC Form 10-K FY2022 (Autoliv Inc)","url":"https://www.sec.gov/Archives/edgar/data/1034670/000095017023002977/alv-20221231.htm","excerpt":null,"as_of":"2023-02-01","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近 12 個月 8-K 清單未見 Item 2.01（併購完成）；搜尋亦未見 2026 年併購或處分，僅見策略合作協議","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001034670&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"ARC Inflator 產品責任集體訴訟（MDL 3051，N.D. Georgia）仍在進行，公司否認指控、未計提；搜尋未見 2026 年針對 Autoliv 的證券集體訴訟","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"The proceedings remain ongoing. The Company has determined pursuant to ASC 450 that a loss is reasonably possible with respect to the ARC Inflator Class Action. However, the Company continues to evaluate this matter, no accrual has been made, and no estimated range of potential loss can be determined at this time.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K 風險因素提及與墨西哥稅務機關就當地製造活動的爭議處於早期階段，不利結果可能對營運與財務有重大負面影響","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm","excerpt":"we are currently in the early stages of a dispute with the Mexican tax authorities in relation to various issues dealing with certain manufacturing activities that occur in Mexico.","as_of":"2026-02-19","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 清單未見 Item 4.02（財報不可依賴）；搜尋未見 SEC 調查，僅見 2003 年舊重編與 2011–2018 年反壟斷調查","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001034670&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ALV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.22,"operating_margin_pct":9.18,"fcf_margin_pct":6.83,"rd_intensity_pct":4.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALV","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"7282.T","period":"TTM ending 2026-06-30（2季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.7282.T","as_of":"TTM ending 2026-06-30（2季加總）"},"note":"Total Revenue 缺失，無法算利潤率；僅 2 季可得，非完整 TTM"},{"name":"600699.SS","period":"TTM ending 2026-03-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":18.12,"operating_margin_pct":5.81,"fcf_margin_pct":0.64,"rd_intensity_pct":5.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.600699.SS","as_of":"TTM ending 2026-03-31（4季加總）"}},{"name":"MGA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":14.71,"operating_margin_pct":5.48,"fcf_margin_pct":7.52,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"LEA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":6.86,"operating_margin_pct":3.67,"fcf_margin_pct":3.58,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"ALV"},"financial_history":{"ticker":"ALV","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":8842000000.0,"revenue_yoy_pct":null,"gross_margin_pct":15.79,"operating_margin_pct":7.45,"net_income":423000000.0,"diluted_eps":4.85,"free_cash_flow":128000000.0,"fcf_margin_pct":1.45,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":10475000000.0,"revenue_yoy_pct":18.47,"gross_margin_pct":17.39,"operating_margin_pct":6.59,"net_income":488000000.0,"diluted_eps":5.72,"free_cash_flow":409000000.0,"fcf_margin_pct":3.9,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":10390000000.0,"revenue_yoy_pct":-0.81,"gross_margin_pct":18.55,"operating_margin_pct":9.43,"net_income":646000000.0,"diluted_eps":8.04,"free_cash_flow":480000000.0,"fcf_margin_pct":4.62,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":10815000000.0,"revenue_yoy_pct":4.09,"gross_margin_pct":19.18,"operating_margin_pct":10.08,"net_income":735000000.0,"diluted_eps":9.55,"free_cash_flow":716000000.0,"fcf_margin_pct":6.62,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ALV/ALV_Q3_2026_Earnings_Call_20261023.md）

# Q3 2026 Earnings Call
**Autoliv, Inc.** | Earnings Calls | 2026-10-23

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to the Autoliv, Inc. First Quarter 2026 Financial Results Webcast and Conference Call. [Operator Instructions] Please be advised that today's conference is being recorded. I would now like to hand the conference over to your speaker today, Anders Trapp, Vice President, Investor Relations. Please go ahead.

**Anders Trapp** (Executives):
Thank you, [indiscernible]. So welcome, everyone, to our third quarter 2026 earnings call. On this call, we have our President and Chief Executive Officer, Mikael Bra; our Chief Financial Officer, Monika Grama; and me, Anders Straatliiti, Investor Relations. During today's earnings call, we will highlight some -- several key areas, including our strong performance in a challenging market environment, ongoing mitigation actions to offset cost headwinds. We're going to give an update on the latest market developments and our shareholder returns and our full year guidance and the potential impact of ongoing geopolitical and market challenges. Following the presentation, we will be available to answer your questions. As usual, the slides are available on autoliv.com. 
Turning to the next slide. We have the safe harbor statement, which is an integrated part of this presentation and includes the Q&A that follows. During the presentation, we will reference non-U.S. GAAP measures. The reconciliations of historical U.S. GAAP to non-U.S. GAAP measures are disclosed in our quarterly earnings release available on autoliv.com and in the 10-Q that will be filed with the SEC and at the end of this presentation. Lastly, I should mention that this call is intended to conclude at 3:00 p.m. Central European Daylight Saving Time. So please follow a limit of 2 questions per person. I will now hand over to our CEO, Mikael Bratt.

**Mikael Bratt** (Executives):
Thank you, Anders. Looking on the next slide.
We delivered a strong third quarter in a tough environment with adjusted operating margin exceeding our earlier indications and reflecting disciplined execution across the business. The progress we achieved during the quarter reinforces our confidence in further profitability improvement through year-end. Together with strong customer partnerships and ongoing efficiency initiatives, we believe we are well positioned to continue delivering value for our stakeholders. Our positive sales momentum in Asia continued during the quarter. In China, we once again outperformed light vehicle production, driven by strong growth with Chinese OEMs. 
Where our sales outperformed by almost 20 percentage points. In India, we grew sales by nearly 30% organically, reflecting mainly the trend of increased safety content in vehicles in India. Adjusted operating margin reached 9.7%, ahead of earlier indication, reflecting strong operational execution and higher engineering income. I am pleased that our cash flow was strong despite working capital buildup due to strong sales in September. In the quarter, we repurchased over 1.2 million shares for USD 150 million and paid dividends of USD 63 million. Based on what we know today, we reiterate our full year 2026 guidance of flat organic sales with continued significant outperformance of light vehicle production, both with Chinese OEMs and in India.
Following the first 9 months of the year and continued raw material headwinds and higher logistic costs, we have narrowed down our adjusted operating margin guidance to be around 10.5%, which is at the low end of the range of around 10.5% to 11%. This reflects the effectiveness of the mitigation actions outlined later in the presentation. Operating cash flow guidance remains unchanged. CapEx is now expected to be around 4% of sales compared with the previous expectations of less than 5% of sales. We also have several positive developments to highlight from the quarter, both in terms of our footprint and our product offering. Expanding in China is key to strengthening Autoliv's innovation, global competitiveness and long-term growth.
To support this and our growing partnerships with Chinese OEMs, we have opened our second R&D center in China. We also launched the human body Model Safety Suite, a virtual safety development platform that helps automakers evaluate occupant protection through advanced crash simulations. By helping customers improve safety performance earlier and shorten development time, it strengthens Autoliv's value proposition and growth opportunities. Looking now on the next slide. Third quarter sales were virtually unchanged despite light vehicle production declining. This was due to outperformance relative to light vehicle production, including tariff-related compensations and favorable currency effects. Adjusted operating income for the third quarter decreased by 3% to USD 262 million. 
The decline reflects a $15 million supplier compensation, which benefited the third quarter of last year. The adjusted operating margin was 9.7%, 30 basis points lower than last year. Operating cash flow was USD 239 million, a decrease of USD 19 million. Looking now on the next slide. We continue to deliver broad-based operational improvements. Our positive direct labor productivity trend continued during the quarter, supported by the execution of our strategic initiatives, including automation and digitalization. Gross profit decreased by USD 26 million with the gross margin declining from 19.3% to 18.4%. Approximately half of the year-over-year decline was attributable to the noted supplier compensation recognized in the prior year.
Looking ahead, we expect fourth quarter gross margin to develop favorably compared to Q4 2025. RD&E net expenses decreased year-over-year, driven by higher engineering income. As previously communicated, the increase in engineering income was primarily related to the timing of specific customer development projects. SG&A expense remained virtually unchanged, both year-over-year and sequentially. Turning to the light vehicle market development in the third quarter, let's move to the next slide. According to Mobility Global's October forecast, global light vehicle production declined by 1.9% in the third quarter, approximately 20 basis points below the expectations in July. The weaker-than-expected production environment was primarily driven by lower volumes in China among global OEMs as well as softer production in North America and Japan.
This was partly offset by stronger-than-expected performance in India and South America. The regional mix of global light vehicle production was approximately 90 basis points unfavorable during the quarter, mainly reflecting stronger production growth in lower content markets relative to other regions. Despite these market headwinds, our sales remained virtually unchanged year-over-year, supported by our continued outperformance relative to light vehicle production, favorable currency effects and tariff-related compensation. We will talk about the expected market development in the fourth quarter more in detail later in the presentation. Call-off accuracy has deteriorated somewhat compared with the beginning of the year, driven mainly by China, while other regions have returned to almost normal levels.
Maintaining high call-off accuracy remains critical as it enables efficient production planning, inventory management and optimal capacity utilization across our operations. Looking now on our sales growth in more detail on the next slide. Our consolidated quarterly net sales was virtually unchanged despite market headwinds. Excluding currencies, our organic sales decreased SEK 30 million or by 1% Based on the latest light vehicle production data from Mobility Global, we underperformed the market by almost 1 percentage point globally. In Asia, excluding China, we outperformed the market by almost 3 percentage points, driven by continued strong sales growth in India, where we outperformed by 11 percentage points.
Japan also contributed to the outperformance as we outperformed in Japan by almost 4 percentage points. In China, we delivered outperformance of around 1 percentage point, mainly because our sales growth to Chinese OEMs exceeded the light vehicle production growth by almost 20 percentage points. As a result, Chinese OEMs accounted for 58% of our sales in China in the quarter compared to 46% for the same period last year. While performance in Americas overall was in line with light vehicle production, North America delivered stronger results, outperforming light vehicle production by 2 percentage points. Globally, Sherry, Suzuki and NIO were the largest drivers of sales during the quarter.
Despite light vehicle production decline in China, China accounted for 20% of sales. Asia, excluding China, accounted for 20%, Americas for 34% and EMEA for only 26% due to summer shutdowns. Moving on to the next slide. The third quarter of 2026 saw a high number of new launches, primarily in China, but also in Americas. The strong launch activity in China reflects Autoliv's continued momentum in this strategically important market and supports our ongoing outperformance relative to the market. Higher content per vehicle was driven in part by the adaptation of front center airbags across many of these new vehicles as well as pedestrian protection systems. From a sales potential perspective, the BMW X5 and iX5 were the most significant launches during the quarter. Looking ahead, we expect a substantially higher number of launches in the fourth quarter compared with the same period last year, making 2026 a record year in terms of launch activity.
This record will not stand for long as we expect a new record launch year again in 2027. Let's continue with the next slide. I will now hand over to Monika.

**Monika Grama** (Executives):
Thank you, Mikael. I will talk about the financials more in detail on the next few slides. Turning to the next slide. This slide highlights our key figures for the third quarter of 2026 compared to the same quarter of 2025. Our net sales were $2.7 billion, representing an 0.5% decrease. Gross profit decreased by $26 million and gross margin decreased by 90 basis points. The driver behind the lower gross profit was mainly the $12.5 million supplier compensation in 2025, as Mikael mentioned, as well as higher costs for raw materials. This was partly offset by positive FX effects and supplier cost reduction. The adjusted operating income decreased from $271 million to $262 million and the adjusted operating margin decreased from 10.0% to 9.7% -- the reported operating income of $254 million was $8 million lower than the adjusted operating income, mainly related to capacity alignment activities.
The adjusted earnings per share diluted decreased by $0.13 to $2.19. The main drivers were $0.16 from higher taxes, $0.09 from lower operating income, partly offset by $0.11 from lower number of outstanding shares diluted. Our adjusted return on capital employed and adjusted return on equity were solid, 24% and 25%, respectively. We repurchased shares for $150 million and paid a dividend of $0.87 per share. 
Looking now on the adjusted operating income bridge on the next slide. In the third quarter of 2026, adjusted operating income decreased by $9 million year-over-year. Operational contributed $34 million despite slightly lower sales, primarily driven by cost reduction activities. RD&E and SG&A net had a $17 million positive effect, mainly reflecting $26 million higher RD&E reimbursement. This includes $2 million of unfavorable foreign exchange translation effect. This was partly offset by the $15 million supplier compensation that positively impacted last year's results. 
Raw material costs had a gross negative impact of $42 million in the quarter with nonferrous metals and oil-related components accounting for the majority of the increase. During the quarter, we achieved customer compensation covering more than 80% of tariff costs. However, tariff-related headwinds still reduced our adjusted operating margin by around 35 basis points, including dilutive effects. Looking now at cash flow on the next slide. Operating cash flow decreased by $19 million to $239 million compared to the prior year, mainly because of lower net income. Trade working capital in relation to sales was 13.5% at the end of the quarter compared to 13.9% a year ago. The improvement was mainly driven by higher payable in relation to sales, while inventories and receivables to sales were relatively unchanged. 
Free operating cash flow was positive $124 million compared to positive $153 million in the prior year. Capital expenditure net increased by $9 million year-over-year. Capital expenditure as a percentage of sales rose to 4.3% compared with 3.9% in the prior year, mainly reflecting increased investments in production and RD&E equipment. The cash conversion was 80%, in line with our target of at least 80%. Year-to-date, operating cash flow decreased by $15 million to $598 million compared to the prior year. Now looking on the next slide. Over the years, Autoliv has consistently demonstrated its ability to generate strong cash flow across a variety of market conditions. Over the last 12 months, we returned approximately USD 760 million to shareholders through dividends and share repurchases. Looking at the past 5 years, we have returned a total of $2.9 billion directly to shareholders, while at the same time, strengthening our balance sheet and improving our leverage profile. 
This includes more than $1.7 billion in share repurchases and nearly $1.2 billion in dividends. During this 5-year period, we reduced our outstanding share numbers of approximately 18%. As of quarter end, approximately USD 1.9 billion remained available for repurchase under the current Board authorized share repurchase program out of the total of USD 2.5 billion original authorization. 
Our capital allocation decisions are guided by a disciplined assessment of our balance sheet, cash flow outlook, leverage, credit ratings and market conditions with a continued focus on delivering long-term shareholder value. Now looking on our debt leverage ratio development on the next slide. Autoliv's balanced leverage strategy reflects our prudent financial management, enabling resilience, innovation and sustained stakeholder value over time. Our leverage ratio was 1.3x at quarter end compared with 1.2x a quarter ago. The increase was driven by a roughly $64 million increase in net debt during the quarter, combined with a modest $6 million decrease in trailing 12-month adjusted EBITDA. Despite the quarter-over-quarter increase, our leverage remains at a low level and well within our targeted capital structure. On to the next slide. I will now hand it back to Mikael.

**Mikael Bratt** (Executives):
Thank you, Monika. 
I will talk about the outlook for the remaining of 2026 more detail on the next few slides. Turning to the next slide. Mobility Global now expects global light vehicle production to decline by 1.9% in 2026. almost 2 percentage points downgrade from its January forecast, primarily driven by weaker outlooks for China and the Middle East. As we enter Q4, the industry continues to face the effects of the conflict in the Middle East and soft demand in China, partly offset by resilient vehicle sales in other markets. For the fourth quarter, Mobility Global forecast global light vehicle production to decline by approximately 4.5% year-over-year. 
The expected decline is largely driven by lower production in China, where softer domestic demand is only partially offset by continued strength in exports. As a result, Mobility Global has reduced its fourth quarter outlook for Chinese light vehicle production to a 9% decline. In the Americas, light vehicle production is expected to decline by approximately 2%, reflecting inventory adjustments in North America. 
In Europe, production is expected to decrease by around 1% as automakers continue to face increasing competitive pressure from Chinese manufacturers. In contrast, Mobility Global has significantly upgraded its Japan outlook to 2% growth from 12% decline -- this is driven by production recovery following Q3 plant disruptions caused by natural disasters and continued strong exports of fuel-efficient hybrid vehicles to the U.S. and Europe. Despite the expected year-over-year decline in global light vehicle production in Q4, production is forecast to increase sequentially by more than 1 million units or approximately 5%. 
Now looking on the fourth quarter development more in detail on the next slide. As we look ahead to the remainder of the year, we remain focused on managing a dynamic external environment. We are closely monitoring the potential impact of geopolitical developments in the Middle East, which continues to affect supply chains, raw material costs and overall vehicle demand. Despite this uncertainty, we expect our financial performance to strengthen in the fourth quarter versus the third quarter. 
Margin expansion is supported by higher sales volumes, increased engineering income and customer compensation related to raw material inflation. In addition, our ongoing cost efficiency initiatives, including greater automization and digitalization across our operations are expected to further enhance profitability and operating leverage. Combined, these actions are expected to result in a meaningful stronger margin profile by year-end. Despite market headwinds, we expect strong free cash flow generation to continue throughout the year, supporting the ongoing execution of our share repurchase program and dividends. 
Looking at our full year guidance, there are several factors expected to weigh on the adjusted operating margin throughout the year, we have taken proactive measures to mitigate the additional headwinds impact in 2026. These are presented in more detail on the next slide. When our original full year 2026 guidance was set in January, our assumptions reflected a significantly more favorable cost environment than what we see now. 
Since then, the business has faced additional headwinds amounting to approximately 170 to 180 basis points. To address these headwinds, we have taken a broad range of commercial, operational and cost efficiency actions, including improving direct labor productivity through optimization, digitalization and continuous improvement initiatives, accelerating value engineering and value analysis initiatives, implementing SG&A cost reduction measures and tighter spending controls. securing raw material recovery through customer negotiations and indexation, delivering savings through commercial negotiations with suppliers. 
Through disciplined execution of these initiatives, we expect to offset most of the incremental headwinds. As a result, the net impact on our full year adjusted operating margin is expected to be limited, demonstrating the resilience of our business model and our ability to proactively manage a challenging cost environment. Looking now on the next slide. This slide shows our full year guidance, which excludes effects from capacity alignment and antitrust-related matters. 
It is based on no material changes to tariffs or trade restrictions that are in effect as of October 15, 2022, as well as no significant challenges in the macroeconomic environment or changes in customer call-off volatility or significant supply chain disruptions. We expect to outperform light vehicle production by around 2 percentage points as our organic sales is expected to be flat, while global light vehicle production is expected to decline by 2% -- the currency translation effect on sales is expected to be around 2.5% positive. While market headwinds have prompted a slight adjustment to our outlook, the change is relatively minor. The guidance for adjusted operating margin is now narrowed to around 10.5%, the low end of our range of around 10.5% to 11%. Operating cash flow is expected to be around USD 1.2 billion. 
We expect CapEx to be around 4% of sales compared to previous guidance of less than 5% -- our strong cash flow generation and disciplined capital spending support our continued commitment to delivering attractive shareholder returns. We expect a tax rate of around 30%. Looking on the next slide. 
This concludes our formal comments for today's earnings call, and we would like to open the line for questions from analysts and investors. But before I do that, I would like to make a small correction then to my comments when it comes to the sales growth and regional sales split in the Q3. I accidentally said that we underperformed the market by almost 1%. It should, of course, be we outperformed the market by almost 1 percentage points globally in the third quarter. So with that correction, I would like to hand it over to Madeline, our operator.

**Operator** (Operator):
[Operator instructions]
We are now going to take our first question.
And this question comes from Tom Narayan from RBC.

**Gautam Narayan** (Analysts):
First one is on the EMEA underperformance versus the market. I know you mentioned there were some shutdowns there, but I guess I would think that would have impacted the market as a whole, not just -- perhaps it was related to the exports into Europe. I'm not sure what your indexation is to those, but just some color on the EMEA underperformance in the quarter? And then I have a follow-up.

**Mikael Bratt** (Executives):
Sure. Thank you for your question. No, I think, first of all, I would say that, I mean, yes, Europe is a challenging market. And here, we have some swings between the different OEMs. So I mean, there are elements of customer mix from our point of view. I think we have said before here that our market share ambition globally is to protect the market share we have. 
And if you come to the more -- I mean, mature markets, you have more of a stable situation there. And then when you see some shifts between the customers, of course, you get a bigger impact than normally if you're in a growth mode or so. So I should not read into much into those swings you see there. And I would also say that, of course, you are impacting this also when you see exports from China coming into Europe. But since we are on most of those vehicles also, you have maybe seemingly a minus in the European business, but we have a plus in China. And that doesn't come through when you look at the numbers region by region like that. 
And that's why I would say it's not that wide, but it's one reason why maybe we emphasize more the overall market share development and outperformance here than the regional shifts. But of course, key here is to grow for us with the OEMs that are growing and taking market shares globally, which we are doing here. And I think the strong outperformance with Chinese OEMs in the quarter here is another evidence of India.

**Gautam Narayan** (Analysts):
And for my follow-up, you described the raw material cost increase resulting in the '26 guidance cut. I believe it was a EUR 10 million impact to the '26 numbers. I know you're not giving '27 guidance today, but just curious how we should think about the raw material cost increase bleeding into '27. Is the expectation that you could get all of that with recoveries in the year? Or is it a similar dynamic that there's kind of a bleeding that happens to forward periods? So I guess how should we think about this cost increase?

**Mikael Bratt** (Executives):
I mean, as a comment here, I mean, we don't give any details around 2027 yet. It's in connection with the earnings call for Q4. But I would say that, I mean, when it comes to raw materials, I would say that we expect it to be as challenging in 2027 as it has been in 2026. 
So I would say that's as much as we can comment really on that specifically. So I would say no headwind or tailwind coming from that. But of course, we are seeing 2026 as a very challenging year that translates and moves into 2027 when we get there, but more details to come.

**Operator** (Operator):
We are now going to take our next question -- and this question comes from Emmanuel Rosner from Wolfe Research.

**Emmanuel Rosner** (Analysts):
Maybe first question, focusing on the implied fourth quarter outlook implied by your guidance. So this would obviously be a very high margin around 14% or so. Can you maybe give us some sort of sense of how much visibility and confidence you have in some of these drivers of margin step-up and in particular, to the extent the recoveries there, are those already secured? Is that -- where are you, I guess, in that negotiation process?

**Mikael Bratt** (Executives):
So I think, first of all, I mean, Q4 is the stronger quarter in the year, as you know. And I think with full year guidance here, we are confirming that that's also the case this year. And of course, one part that makes it stronger is the engineering income that will be a part also this year. We have alluded to the higher sales and also as Mobility Global sales here now also another 1 million units in Q4 compared to Q3. So it supports us in the sequential development there. But right, I mean, it is to really drive here the customer compensation and tariff recovery in line with what we have done throughout the year here. And I think we have a good momentum there. We -- I would say the difference maybe this year compared to other years is that -- and which is a part of the guidance, of course, it's nothing on top of there.
But as you understand the full year impact here is, of course, that this cost pressure continues throughout the year here and makes it very tight to also fix the full effect in the year, which more speaks to that we are on the lower end of the range than anywhere else in the range there. But I mean, we move into the fourth quarter here with confidence. I think the Autoliv team has done a great job maneuvering through this. And as you saw here, I mean, the additional headwind on top of what we expected in the beginning of the year, I mean, 1.8 percentage points more is quite meaningful, I would say, that we have a large absorbed here through price compensations and also our own cost-out activities here. And that also includes material cost optimization with the suppliers also, of course, that we do there. So I think we have a good activity plan for the fourth quarter.

**Emmanuel Rosner** (Analysts):
Okay. I appreciate the color. 
And then as a second question, maybe focusing on China. So I appreciate the color on the breakdown between -- on your performance between global and Chinese local OEMs. Can you maybe comment on what is -- what portion of your business in China is geared towards exports? And any thoughts on to the extent there are some measures being put around the world to sort of limit some of these exports, whether that would be a good thing for you or on a relative basis or a bad thing, something that we should focus on?

**Mikael Bratt** (Executives):
Yes. I think, first of all, I think as a starting point, the export vehicles tend to -- I mean, we don't have a separate supply chain for the export vehicles or the domestic vehicles for our respective customer in China. It's the same models and then the specification may differ, but in most circumstances, I mean, it's the same type of product. 
So we don't really see that difference, which vehicle goes where in that regard. But as I said, we are managing these dynamics in a good way, thanks to our global presence and high market share in the total market. And -- we have talked about that before that we have a fairly strong diversified portfolio with a wide spread representation among the different customers. So if it moves in between, we are on the platforms that also are gaining, some traditional are losing, you could say, in all this. And if there will be more, let's say, restrictions coming up between the regions and you can't export, you need to localize. 
With our footprint, we can support a customer that wants or forced to localize rather than to export from another region. So I think that's really the strength with Autoliv here is that we can offer our customers a lot of flexibility. And I mean, if you talk specifically about the Chinese OEMs exporting from China versus Europe and if you need to localize in Europe. I mean, today, we are already part of the China supply chain for them if they have that set up with CKD, for example, or if they want to localize, then we can support them with local production. So I would say we're well prepared for whatever comes in terms of that dynamic.

**Operator** (Operator):
We are now going to take our next question this question comes from Chris McNally from Evercore ISI.

**Chris McNally** (Analysts):
I just wanted to follow on to Emmanuel's question, maybe just put some numbers to it. We're all trying to figure out this Chinese algorithm, right, which kind of gets a little bit more -- the numbers just become less dramatic Q4 and next year. So for the implied Q4, are you expecting that China organic growth will go sort of back to positive? And then again, for 2027, it's early, but we all kind of know that the exports will be up, whether that's 10% or 20%, we all can debate. But is the expectation that we will still have Chinese organic growth given your sort of customer mix?

**Mikael Bratt** (Executives):
I don't know if I would like to give a number there. But what -- I mean, as we said, I mean, the light vehicle production according to Mobility Global is negative in China. But with that said, I have great confidence in our, I would say, future development of continuing to grow with the Chinese OEMs as we move forward. So yes, I think we are on the right factory here. It's the LVP that gives the delta, so to speak, at the end of the day here. But that -- I think we have to wait and see what the net number is. But we are on a good trajectory with the Chinese OEMs and expect it to continue to grow. That's my comment to that.

**Chris McNally** (Analysts):
Yes. So sorry, sort of a paraphrase that the growth over market should remain a significant driver, but you're focused on the light vehicle, which is obviously pretty negative in Q4. So maybe that's an unfair question. And then '27 is a little bit easier. Okay. Perfect. And then if we could just zone in on the inflation, right? The 180 basis points, you have so many pass-throughs, right? The timing we all know that will be somewhat of a pressure into next year. But I was curious of the 180 basis points, how much was actually the Thailand flooding and logistics, right? We heard from GM this week that logistics was a headwind in Q3, Q4. Because typically, those would not be compensated. So just curious if you can call out either or as a bucket sort of those 2 because those are kind of one-offs.

**Monika Grama** (Executives):
Connected to the Thailand flooding, we see -- we can call it not material impact in our results in Q4. Of course, this is considering coverage from our property damage and business interruption insurance. And then connected to the logistics cost, we see indeed in some of the divisions, double-digit cost increases, especially in the North America. To offset this, we have taken logistic optimization initiatives to reduce the mileage. That is partly compensating the cost. As you well know, this is a cost very difficult to pass on. So there is a limited impact that to a large extent, we are looking on other compensating effects to recover and not per se one-to-one in the same area.

**Operator** (Operator):
We are now going to take our next question. And this one comes from Winnie Dong from Deutsche Bank.

**Yan Dong** (Analysts):
I wanted to just follow up on the year's guide. I understand that you've narrowed the margin to the lower end. Was there anything that's more specific? I think you've talked a lot about costs already, but anything specific that pushes you to the low end of that range? And then -- to a certain extent, what sort of rate do you think carries into 2027?

**Mikael Bratt** (Executives):
Yes. I think -- I mean, as we have alluded to here is the higher-than-expected cost pressure that we have seen across the board here. I mean, we have had on one of the slides. I think the team has done a great job to offset such a large portion of it that we still can be in the range. So good job there. I think what is more moving into '27 is really what we talked about here before connected to the raw materials, I would say that we expect that to continue to be some headwinds. So I think that slide is really a good summary of why it's the lower end and the upper end.

**Yan Dong** (Analysts):
Got it. Separately, I kind of want to ask about mobility safety solutions and specifically, I think there's a product in terms of safety switch outside of vehicles. You're kind of marketing them for battery energy storage, et cetera, which seems like one of the few ways to get growth that's not tied to IP. So just any initial takes on how to frame the opportunities there?

**Mikael Bratt** (Executives):
No, I think it's, as you say, an interesting opportunity here in the light of the electrification that is going on in society. So we are having a dedicated team here, of course, to develop that business. And here, we're talking about both high voltage and low voltage, et cetera, to see what we are doing there. And I mean we have interesting leads, and we are also growing this business as we speak. 
Then we have decided and elected not to give too much details and numbers at this point in view point in time because we believe that it's more meaningful to come back to you when we have meaningful volumes around that and talk more in great detail. It's a little bit of a -- you could say, a start-up phase right now, but interesting opportunities in the midterm for sure.

**Operator** (Operator):
We are now going to take our next question. And this one comes from Jose Asumendi from JPM.

**Jose Asumendi** (Analysts):
Two quick questions, please. Anders, can you talk about the level of activity in '27 versus '26, just broadly, if you see more product launches coming up in '27 versus '26? And related to this, whether you are seeing any substantial production stoppages in Europe in the month of November? And question two, it's just simply a confirmation that when you think about the raw material negotiations you're having that you are not in the camp of seeing spillover and negotiations of raw materials going into '27 that you're confident with the raw material discussions in '26. We heard from our suppliers that we see some spillover of these discussions into 2027, whether you're confirming that '26 raw materials will be negotiated and closed.

**Anders Trapp** (Executives):
Thank you for your question. I think 2027 and launches here, we expect to see a higher number of launches in 2027. So we see that, that continues to increase. And I would say we have high activity level when it comes to closing new orders and new deals here that gives us this effect. So that's a positive, I think, when we look out for next year and especially then, I guess, in combination with the LVP outlook that Mobility Global have indicated for next year as well. I think when it comes to the challenge around raw material negotiations here, I wouldn't maybe say specifically raw materials alone. It's in general, the cost pressure that we see right now that has been throughout the year also continuing into Q4. But that's a part of the guidance we have for the full year. 
So the answer to your question is not changing that picture. That's important to remember. But that's a part of, as I said, the lower end of the range here is also the fact that it's difficult to finishing those locations with the cost pressure that we see coming now in November and October, November to finish that before the year-end. But that's because it's continuing to increase. So it's no indication on more difficult or complicated negotiations. It's just that the regular time between the impact and the closure becomes shorter this year as it continues. But it is, once again, it's embedded in what we have indicated for the full year. So nothing on top of very important.

**Jose Asumendi** (Analysts):
That's super helpful. And on any major production stoppages in Europe, you're not seeing anything? Or are you seeing any evidence there?

**Anders Trapp** (Executives):
No, nothing -- no, nothing to point out. I think, of course, we are always watchful for any activities there and as we come closer to the year and depending on inventory levels and so on with the OEMs, but we have no visibility or indications at this point in time. And I think also looking at the inventory levels in Europe, as far as we can see, it's quite in balance. So there is no indication for any abnormal things there. So yes, we should be in good shape as an industry.

**Operator** (Operator):
We are now going to take our next question. And this one comes from Agnieszka Vilela from Nordea.

**Agnieszka Vilela** (Analysts):
Just one question from me, and that's on R&D. I think you mentioned that you received somewhat more engineering income in the quarter than what you expected. Can you quantify by how much? And also do you still expect a positive contribution from engineering income in Q4? And then maybe in relation to that, looking forward, what kind of net R&D costs do you expect into 2027, either in relation to sales or on an absolute level?

**Monika Grama** (Executives):
Thank you, Agnieszka, for the question. Connected to Q4, as we guided, we expect a sequential improvement compared to Q3 and engineering income increase is one of the drivers of this improvement. So yes, it is a positive contributor further in Q4. And on the long-term range, we expect pretty similar RD&E net of sales as we had in the previous period. So it's no major change that we can announce at this point. This is pretty the trend that we want to maintain and in line with our expectations.

**Agnieszka Vilela** (Analysts):
And on the kind of delta that you saw in Q3 specifically, I think you mentioned that it was a bit better than what you expected on the engineering income side.

**Monika Grama** (Executives):
As mentioned, it was better compared to prior year. And in the first quarter this year, we suffered a negative impact compared to prior year, and it was part of the phasing of that we anticipated to a large extent.

**Operator** (Operator):
We are now going to take the next question. And this one comes from Hampus Engellau from Handelsbanken.

**Hampus Engellau** (Analysts):
Just one question from me. And that's maybe if, Mikael, if you could just share some, if you know, of course, the launches for 2027, are they like back-end loaded? Are they front-end loaded? Or should we like expect them like gradually throughout the year? If you have any view on that, that would be helpful.

**Mikael Bratt** (Executives):
Yes. I think it's not any dramatic phasing on it. It's, of course, not equally distributed between the quarter. There are some quarters. I don't have exactly on top of my head the distribution there. But it's no dramatic it's not like it's half of them in Q1 or something that. It's, I would say, normal fluctuation as you see in the previous year.
So very normal, I would expect it to be.

**Operator** (Operator):
We are now going to take the next question. And this one comes from Stephen Benhamou from Bank of America.

**Stephen Benhamou** (Analysts):
I have 2 questions, please. The first one is on your guidance for Q4. So your full year guidance implies around 400 bps of outperformance for the last quarter, well above the outperformance delivered in your previous quarters and despite a tougher comp base. So what gives you confidence into this acceleration? This is my first question. And my second question is about your full year guidance adjustment. So now you're expecting around 10.5% versus between 10.5% to 11%. So should we read that as a floor? Or is there any scenario where the -- yes, the full year performance could be below 10.5% this is my second question.

**Mikael Bratt** (Executives):
No, I think when it comes to the guidance for the fourth quarter, I just would like to come back to basically what I said earlier here, which is that, I mean, we enter now Q4 with, I should say, the confidence of the fact that we have a clear activities lined up here for the fourth quarter to support the numbers here. I mean, starting -- what we see here is on the sequential -- I mean, first of all, Q4 is the stronger quarter. It's always the stronger compared to the previous quarters. also this year because there is a seasonality to it. What we see now also sequentially here is that, I mean, despite the, I would say, very challenging quarter that we have been in, the team managed to deliver slightly better than what we expected into the quarter when we were here in July. 
And that is because we're delivering well on our improvement activities that we have as an incremental part of our strategy to have an earnings growth altogether. So of course, when we have all these headwinds, those activities are helping us. So the higher sales is one. The tariff compensation and customer compensation is other cornerstones that is critical here, of course, where we have a good momentum in this as we have seen. We have the higher sales of the 1 million vehicles once again on the sequential development here. And that makes us see that we should be able to deliver on what we have indicated before. And actually, it has strengthened the case for Q4 compared to July since we delivered so stronger in Q3. 
So the momentum carries through into Q4 is our expectations here, and that's why we have the confidence, as we said here, to make this step here. Then, of course, I mean, we don't guide for the future years here more than to say that -- I mean, the range for this year was a reflection of the uncertainty in the market and the volatility in the market that we see. But I'm really happy that we are able to stay within this range. And I think that's really a sign of strength here. So when we move forward here, I mean, our ambition is still -- and target is still to get to the 12%. So our earnings growth is something we're working on very hard with the different levers that we have identified and communicated before. So that still laid as the foundation. Then of course, if you come is this the floor or not, I mean, it depends, I would say, of course, on the external circumstances here. 
I mean if you have a pandemic year again, I mean, who knows. So it's a very difficult question to answer rather than to say that we believe that we have an earnings growth built into our activity plans under normal circumstances.

**Stephen Benhamou** (Analysts):
Maybe if I can just add a follow-up question regarding the top line. Coming back to China, can you please clarify why China turned negative organically in Q3 because -- so you delivered outperformance. But when I look at Q1 and Q2, the market was very challenging, and you've delivered positive organic growth. So why you turned negative in Q3 and why you are more optimistic for Q4?

**Mikael Bratt** (Executives):
No, I think, I mean, what all that is referring to is the light vehicle production development that is quite significant. I think so far, we have been compensated with the exports. I mean the domestic sales gone down, global export has gone up and offset the large part of that. I think we see that the export opportunities limits that offsetting factor, and that's really the LVP growth. I think as I said before, our own ability to continue to grow and outperform with the Chinese OEMs continues. So we feel comfortable in our own, I would say, activities and outcome that.

**Operator** (Operator):
We have time for one last quick question. And this question comes from Ita Michel [indiscernible] from TD Cowen.

**Unknown Analyst** (Analysts):
Just 2 quick questions. You've done a really good job of mitigating the 180 basis points or mostly mitigating the impact this year. But I'm curious to what degree, if any, are some of these mitigation actions a pull forward from initiatives you are planning for subsequent years? And could that affect the kind of trajectory towards your 12% margin target?

**Anders Trapp** (Executives):
I would say no. I mean what we do is, I mean, we take -- I mean, you saw in the last quarter here -- well, Q2 here, we announced in Turkey, which is an effort also to continue to strengthen our midterm and long term. So I mean we constantly work with our activities plan to make sure that we have enough activities to secure our growth journey as well as making sure that we can offset new headwinds that comes our way. So it's never done. It's a constant work on all that. So I would say what we have done now here to offset this is really, as we said before, even more strictly control SG&A activity, enhancing the productivity in our plants and applying new technology. I think that's also very, I would say, interesting and inspiring is also that when we are on this journey, I mean, with continuous improvements, you're never done, it's always another 20%, 25% potential there. 
But with the new technologies, we see that we also can take more leaps, bigger leaps in productivity here, supplying things that were not available technically maybe 2 years ago, but today it is. So the whole optimization journey, potential growth as we move forward. And that's really the focus here to keep up a high pace on that to manage the headwinds and our own growth journey.

**Unknown Analyst** (Analysts):
That's very, very helpful. As a super quick follow-up, maybe just talk through the drivers of the lower CapEx to sales guidance this year and how sustainable that might be into next year?

**Monika Grama** (Executives):
So as mentioned, we are narrowing our guidance for CapEx to around 4% it's a phasing of activities. We prefer to prioritize activities that have a higher payback, and we continue to invest now more accelerated in Q3. But it's pretty just phasing related to our investments and the prioritization to the higher payback projects.

**Operator** (Operator):
That was the last question for today. I will now hand the call back to Mikael Bratt, President and CEO, for closing remarks.

**Mikael Bratt** (Executives):
Thank you, Madlene. Looking on the next slide. Before we conclude today's call, I would like to invite you to Autoliv's Investor Day taking place on 26th and 27th of April next year, 2027 in Shanghai, China. The event will feature management presentations and visits to our operations, combined with a full day at Shanghai Auto Show 2027, the world's leading automotive exhibition. Attendees will also have the opportunity to experience Autoliv's latest safety innovations and technologies showcased at the event. We look forward to welcome you to Shanghai for an insightful and exciting 2 days. Finally, our fourth quarter call is scheduled for Friday, January 29, 2027. Thank you for your attention until next time, stay safe.

**Operator** (Operator):
Thank you. This concludes today's conference call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ALV_Q2_2026_Earnings_Call_20260717.md
- 2026-07-17｜Mikael Bratt｜guidance：CEO 重申 2026 全年有機銷售持平的財測。（原話："we reiterate our full year 2026 guidance of flat organic sales with"）
- 2026-07-17｜Mikael Bratt｜guidance：全年調整後營業利益率維持約 10.5% 至 11%。（原話："We continue to expect an adjusted operating margin of around 10.5% to 11%."）
- 2026-07-17｜Mikael Bratt｜guidance：財測假設原物料毛逆風約 1.1 億美元。（原話："a gross raw material headwind of approximately USD 110"）
- 2026-07-17｜Mikael Bratt｜guidance：全年預期優於輕型車產量約 2.5 個百分點（有機持平、產量降 2.5%）。（原話："outperform light vehicle production by around 2.5"）
- 2026-07-17｜Mikael Bratt｜guidance：全年營運現金流約 12 億美元。（原話："cash flow is expected to be around USD 1.2 billion"）
- 2026-07-17｜Mikael Bratt｜guidance：全年資本支出低於銷售的 5%。（原話："we expect CapEx to be below 5% of"）
- 2026-07-17｜Mikael Bratt｜guidance：全年稅率預期約 30%。（原話："We expect a tax rate around 30%."）
- 2026-07-17｜Mikael Bratt｜guidance：第三季調整後營業利益率預期與上半年相近。（原話："to be similar to the first half year level"）
- 2026-07-17｜Mikael Bratt｜guidance：客戶補償與工程收入偏重第四季，第四季獲利大幅跳升。（原話："a significant step-up in profitability in the fourth"）
- 2026-07-17｜Mikael Bratt｜guidance：管理層對利益率區間內偏上或偏下端不作表態。（原話："we haven't expressed upper or lower end"）
- 2026-07-17｜Mikael Bratt｜margin：第二季調整後營業利益率 9.6%，年增 30 bp。（原話："The adjusted operating margin was 9.6%, 30 basis points higher."）
- 2026-07-17｜Mikael Bratt｜margin：毛利率下滑，管理層拆解為供應商補償回沖加土耳其資產減損，合計約 80 bp。（原話："which combined reduces gross margin by almost 80"）
- 2026-07-17｜Monika Grama｜margin：第二季美國關稅回收率約 83%（不含 IEEPA），年初至今 78%。（原話："we recovered approximately 83% of our U.S. tariffs"）
- 2026-07-17｜Mikael Bratt｜margin：管理層說明下半年利益率擴張的支撐來源。（原話："we expect margin expansion to be supported by FX, engineering income"）
- 2026-07-17｜Mikael Bratt｜margin：原物料漲價抵銷分三條路：向供應商爭取、內部降本、與客戶議價。（原話："the third leg is then the price adjustments with our customers"）
- 2026-07-17｜Mikael Bratt｜margin：對客戶的價格調整細到零組件層級，並非統一百分比。（原話："It's not a general percentage adjustment"）
- 2026-07-17｜Monika Grama｜margin：IEEPA 退款：從政府拿回約 1,200 萬美元，其中約 900 萬轉給客戶，淨留 300 萬。（原話："we got back around $12 million from the government"）
- 2026-07-17｜Mikael Bratt｜commitment：決定逐步關閉土耳其製造據點，產能移轉至 EMEA 現有工廠。（原話："discontinue our manufacturing operations in Turkey"）
- 2026-07-17｜Mikael Bratt｜commitment：土耳其重組總費用約 1.42 億美元，其中 9,000 萬已於第二季認列。（原話："total restructuring charges of approximately USD 142 million"）
- 2026-07-17｜Mikael Bratt｜commitment：土耳其案預期年化稅前節省約 4,000 萬美元，2027 起顯現、2028 達滿額。（原話："annual pretax savings of approximately USD 40 million"）
- 2026-07-17｜Mikael Bratt｜commitment：土耳其工廠預計 2028 上半年完全關閉，影響約 2,200 名員工。（原話："complete closure anticipated during the first half of 2028"）
- 2026-07-17｜Monika Grama｜commitment：CFO 稱現金流與資產負債表支持持續高水準股東回報。（原話："supports our continued commitment to a high level of"）
- 2026-07-17｜Mikael Bratt｜capital_allocation：第二季買回逾 160 萬股、金額 2 億美元。（原話："repurchasing over 1.6 million shares for USD 200 million"）
- 2026-07-17｜Monika Grama｜capital_allocation：槓桿比率由 1.3x 降至 1.2x，同期股東回報合計 2.64 億美元。（原話："leverage ratio improved from 1.3 to 1.2x during the quarter"）
- 2026-07-17｜Monika Grama｜capital_allocation：近 12 個月現金轉換率 119%，高於至少 80% 的目標。（原話："months was 119% and exceeding our target of at least 80%"）
- 2026-07-17｜Mikael Bratt｜customer：中國區銷售中，中國 OEM 占比由去年 40% 升至 55%。（原話："the Chinese OEMs accounted for 55% of our sales in"）
- 2026-07-17｜Mikael Bratt｜customer：Q&A 中管理層說 2022 年以來對中國 OEM 銷售占中國區比重的提升（此處數字為 65%）。（原話："grown from 22% of our China sales in '22 to 65% China sales"）
- 2026-07-17｜Mikael Bratt｜customer：與長城汽車、小鵬簽署策略合作協議。（原話："we signed strategic cooperation agreements"）
- 2026-07-17｜Mikael Bratt｜customer：印度有機銷售成長 36%。（原話："In India, we grew sales by 36% organically"）
- 2026-07-17｜Mikael Bratt｜customer：美洲表現為負，部分歸因於關稅補償減少與低含量的南美市場成長帶來的不利組合。（原話："The negative performance in the Americas can partly"）
- 2026-07-17｜Mikael Bratt｜customer：管理層對訂單（order intake）不揭露細節，只稱有支持市占的活動。（原話："we don't disclose any details around the current order intake"）
- 2026-07-17｜Mikael Bratt｜competition：歐洲產量展望弱，提到可負擔性問題與中國進口車競爭加劇。（原話："increasing competition from Chinese imports"）
- 2026-07-17｜Mikael Bratt｜competition：管理層對守住市占表達信心。（原話："I think we are in good shape here to"）
- 2026-07-17｜Mikael Bratt｜product：新車上市多在中國，每車含量提升由前中央氣囊帶動。（原話："Higher CPV is driven by Front Center Airbags on"）
- 2026-07-17｜Mikael Bratt｜product：2026 年下半年新車上市數多，主要來自中國 OEM，抵銷美歐較少的上市。（原話："we expect a high number of new product launches"）
- 2026-07-17｜Mikael Bratt｜product：管理層提及零重力座椅作為未來內裝安全機會。（原話："So we call it the zero gravity seat"）
- 2026-07-17｜Mikael Bratt｜risk：波斯灣緊張情勢被列為汽車價值鏈風險。（原話："political tension in the Persian Gulf continue to increase risks"）
- 2026-07-17｜Mikael Bratt｜risk：S&P 自一月起將中國輕型車產量預測下修。（原話："lowered its outlook for China light vehicle production"）
- 2026-07-17｜Mikael Bratt｜risk：公司不直接採購原物料，漲價透過供應鏈傳導。（原話："we don't buy raw materials directly"）
- 2026-07-17｜Mikael Bratt｜risk：利益率區間反映市場波動與通膨壓力是否長期的不確定。（原話："the interval here reflects the"）
- 2026-07-17｜Mikael Bratt｜guidance：敘事變化：全年獲利節奏由年初預期的正常序列改為偏後段，原因是波斯灣帶來的通膨壓力。（原話："more back-end loaded is because we see the inflationary"）
- 2026-07-17｜Mikael Bratt｜customer：管理層稱與客戶就通膨補償的對話與 23–25 年相比沒有改善也沒有惡化。（原話："no change either improved or deteriorated"）
- 2026-07-17｜Mikael Bratt｜product：資本市場日的成長框架（LVP 與含量各 1–2%）管理層稱仍成立，但組合效應使含量成長未達全潛力。（原話："convey that at Capital Markets Day definitely still holds there"）

### 問答異常語氣（迴避／改口／保留）
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Colin Langan：利益率節奏先前說較線性，現在需要 Q4 約 15% 才達中點，變了什麼？｜答法：承認由年初的正常節奏改為偏後段，歸因於波斯灣帶來的成本壓力與議價時滯；未給 Q3 原物料數字。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Colin Langan：原物料是否幾乎 100% 回收？｜答法：回答「No」後改談自助、內部降本、客戶價格調整三個槓桿，未給回收比例。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Itay Michaeli：全年利益率區間有無偏上或偏下端？｜答法：不表態，稱最佳判斷就是落在區間內。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Itay Michaeli：訂單（order intake）趨勢與對美歐超越市場的影響？｜答法：稱不揭露細節，改以「感覺舒適」「活動水準尚可」概括，未給數字。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Agnieszka Vilela：中國 OEM 占比提高對含量與獲利率影響？｜答法：稱獲利率細節不能談、依平台專案而定，改談成長機會與創新。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：（準備稿與 Q&A 對照）中國 OEM 占中國區銷售比重｜答法：準備稿稱本季 55%（去年 40%），Q&A 中同一指標說成 65%；逐字稿內兩處數字不一致。

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
{"date":"20260524","verdict":"B｜衛星候選｜分批進場（建議第一批 50% 現價，第二批待 Pure MA ✅ 或拉回 W52 $115 區間加碼）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"全球市佔結構性擴大（competitor exit + 中國本土化勝出）","columns":{"2Y 驗證":"2026/2027 中國 OEM organic outperform LVP &gt; +30 ppts/yr","5Y 驗證":"全球市佔 2024 ~44% → 2030 ≥ 47%","10Y 驗證":"2035 ≥ 50%（接近 self-imposed cap）","數字門檻":"Q-on-Q 中國 outperform &gt; 30 ppts；年度市佔 ≥ 47% by 2030","信息來源":"Capital Markets Day 2025-06；公司 Investor Presentation","漂移觸發":"連 2 季中國 outperform 收斂至 &lt; +10 ppts → 削弱（2Y）"}},{"id":"H2","text":"Adj OPM 結構提升至 12% mid-cycle","columns":{"2Y 驗證":"FY 2027 Adj OPM ≥ 11.5%（FY 25 ~10.0% → 26 公司目標 10.5-11% → 27 目標 12%）","5Y 驗證":"5Y 平均 Adj OPM ≥ 11.5%","10Y 驗證":"OPM 維持 11-12% range（無 mean reversion 至 9%）","數字門檻":"FY26 ≥ 10.5% / FY27 ≥ 11.5% / FY28 ≥ 12%","信息來源":"2025-06 CMD slide deck；Q1 26 earnings call","漂移觸發":"連 4 季 OPM &lt; 9.5% → 削弱（5Y 假設）"}},{"id":"H3","text":"Fwd PE re-rate 至 13-14x（PEG ~1.2-1.3）","columns":{"2Y 驗證":"2026/2027 Fwd PE 達 12-13x（觸發 sector re-rate）","5Y 驗證":"5Y 維持 Fwd PE ≥ 12x median","10Y 驗證":"無 secular de-rate 至 8-9x（commodity 化情境）","數字門檻":"NTM Fwd PE 進入 12-14x 區間 ≥ 6 個月","信息來源":"sector 比較 GNTX / LEA Fwd PE 平均 10x；ALV 隱含 fair value 13x","漂移觸發":"連 4 季 Fwd PE &lt; 9x → 反轉（2Y 假設）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"NA / EU LVP 持續下行（衰退）拖累整體 organic 至負值","columns":{"對應假設":"H1 / H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"S&amp;P Global LVP 月報（NA / EU 區）","警戒閾值":"連 2 季 NA + EU 合計 LVP &lt; -3% → 削弱（公司 -1% LVP 假設不再成立）"}},{"id":"R2","text":"中國本土供應商搶單（Joyson、Denso-BYD JV、Toyoda Gosei 中國組 share gain）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"China outperform vs LVP gap（Q-on-Q）","警戒閾值":"連 4 季 China outperform 從 +43 ppts 收斂至 &lt; +10 ppts → 中國組 share 流失"}},{"id":"R3","text":"ARC airbag MDL 訴訟賠付 + 可能擴大 recall（類似 Takata 模式）","columns":{"對應假設":"H3（無資本損害）","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"10-K / 10-Q 法律準備金科目 / MDL 件數變化","警戒閾值":"累積準備金 &gt; $500M 或 NHTSA 強制 recall 數量 &gt; 10M 件 → 跨年度監控；單一新增 case 不觸發"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":122.73,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
